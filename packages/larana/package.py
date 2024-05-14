# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import spack.util.spack_json as sjson
from spack import *


def sanitize_environments(*args):
    for env in args:
        for var in (
            "PATH",
            "CET_PLUGIN_PATH",
            "LDSHARED",
            "LD_LIBRARY_PATH",
            "DYLD_LIBRARY_PATH",
            "LIBRARY_PATH",
            "CMAKE_PREFIX_PATH",
            "ROOT_INCLUDE_PATH",
        ):
            env.prune_duplicate_paths(var)
            env.deprioritize_system_paths(var)


class Larana(CMakePackage):
    """Larana"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larana"
    git = "https://github.com/LArSoft/larana.git"
    url = "https://github.com/LArSoft/larana/archive/v01_02_03.tar.gz"
    list_url = "https://api.github.com/repos/LArSoft/larana/tags"

    version("09.15.05", sha256="9997c564bc5b95f4949033b51930c349d93ff48a932f0a6105a451020b722489")
    version("09.15.04", sha256="25a1f5c4e32eac31890952840312df8624ad8749ef3fee7bfb6873a9c6801e4f")
    version(
        "09.03.09.01", sha256="162712cd2506c443799b5e055a63370977ce9384d7a88925f0fda030362b95bf"
    )
    version("09.03.06", sha256="e0eca0c9cdce510ec552151c5ced3e5821f97b479b632995ea43950e9a58eefc")
    version("09.03.05", sha256="017796fe891f12d1caaa17a12d753f47b263c0bdc8b44c14934b0d5d70ab82bd")
    version("09.03.04", sha256="8464e9e96f9dc3822bdd00e0bbad78004799bfab2c6ba066fe6a1770443a8fc0")
    version("09.03.03", sha256="21a81310d5f92f953cc51a7155aa524574336c7ef4a297027e63cb34e4cf74c2")
    version("09.03.02", sha256="b4a88aa04797dc74a05340d8706f543fb842e44542527fcef719b50ffa32ac7c")
    version("09.03.01", sha256="c6efb390d2af631b7efd0ddc3d709744642bad02cd8c7107fcc519d047e1a941")
    version("09.03.00", sha256="8394314e855c62735b9317eef219b7b452dcecba4d3cee24857c4764244b9b30")
    version("09.02.17", sha256="af487034b6e9106b863fbad341d47e36defac3e6ad3c2e84d97cee021407650a")
    version("09.02.16", sha256="517ee39ebdb1d55137799eb8cef5de783ad51b7c838f5271e3d5f29a0bc44105")
    version("09.02.15", sha256="95653ea8022539bf367da7938f9e9d284ce2791f80a31ba578bfdf5b5c74a75d")
    version("09.02.14", sha256="0aafe08d52d360d648e1d63905384103cfb3d167b632f3b469ad355312209f47")
    version("mwm1", tag="mwm1", git="https://github.com/marcmengel/larana.git", get_full_repo=True)
    version("develop", branch="develop", get_full_repo=True)

    def url_for_version(self, version):
        url = "https://github.com/LArSoft/{0}/archive/v{1}.tar.gz"
        return url.format(self.name, version.underscored)

    def fetch_remote_versions(self, concurrency=None):
        return dict(
            map(
                lambda v: (v.dotted, self.url_for_version(v)),
                [
                    Version(d["name"][1:])
                    for d in sjson.load(
                        spack.util.web.read_from_url(
                            self.list_url, accept_content_type="application/json"
                        )[2]
                    )
                    if d["name"].startswith("v") and not d["name"].endswith(")")
                ],
            )
        )

    patch("v09_03_06.patch", when="@09.03.06")
    patch("v09_03_09_01.patch", when="@09.03.09.01")

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("larreco")
    depends_on("cetmodules", type="build")

    def cmake_args(self):
        args = [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]
        return args

    def setup_build_environment(self, spack_env):
        # Binaries.
        spack_env.prepend_path("PATH", os.path.join(self.build_directory, "bin"))
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", os.path.join(self.build_directory, "lib"))
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(
            root=False,
            cover="nodes",
            order="post",
            deptype=("link"),
            direction="children",
        ):
            spack_env.prepend_path("ROOT_INCLUDE_PATH", str(self.spec[d.name].prefix.include))
        # Perl modules.
        spack_env.prepend_path("PERL5LIB", os.path.join(self.build_directory, "perllib"))
        # Cleaup.
        sanitize_environments(spack_env)

    def setup_run_environment(self, run_env):
        run_env.prepend_path("PATH", self.prefix.bin)
        # Ensure we can find plugin libraries.
        run_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(
            root=False,
            cover="nodes",
            order="post",
            deptype=("link"),
            direction="children",
        ):
            run_env.prepend_path("ROOT_INCLUDE_PATH", str(self.spec[d.name].prefix.include))
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        # Perl modules.
        run_env.prepend_path("PERL5LIB", os.path.join(self.prefix, "perllib"))
        run_env.append_path("FHICL_FILE_PATH", "{0}/fcl".format(self.prefix))
        run_env.append_path("FW_SEARCH_PATH", "{0}/gdml".format(self.prefix))
        # Cleaup.
        sanitize_environments(run_env)

    def setup_dependent_build_environment(self, spack_env, dspec):
        spack_env.set("LARANA_INC", self.prefix.include)
        spack_env.set("LARANA_LIB", self.prefix.lib)
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        spack_env.prepend_path("PATH", self.prefix.bin)
        spack_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        spack_env.append_path("FHICL_FILE_PATH", "{0}/fcl".format(self.prefix))
        spack_env.append_path("FW_SEARCH_PATH", "{0}/gdml".format(self.prefix))

    def flag_handler(self, name, flags):
        if name == "cxxflags" and self.spec.compiler.name == "gcc":
            flags.append("-Wno-error=deprecated-declarations")
            flags.append("-Wno-error=class-memaccess")
        return (flags, None, None)

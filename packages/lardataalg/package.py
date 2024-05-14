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


class Lardataalg(CMakePackage):
    """Lardataalg"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/lardataalg"
    git = "https://github.com/LArSoft/lardataalg.git"
    url = "https://github.com/LArSoft/lardataalg/archive/v01_02_03.tar.gz"
    list_url = "https://api.github.com/repos/LArSoft/lardataalg/tags"

    version("09.17.03", sha256="138a67d9ff190540fb6e095639aa6b0c60b753e5fdc005304b8244f0f97ffe4f")
    version("09.17.02", sha256="e4f8328453d093d0f0a792c5a6868bf93541a47fa5f7b039ef44635695846f66")
    version("09.16.04", sha256="014ce4fcb44fdc46e9a778748b13bb6a834bee567abed0be435fb193ce59104f")
    version("09.16.01", sha256="6787452aebec2e0bfb1d1b5e278547bbc23586e616b6c3f74b393d7b2ded44cb")
    version("09.15.01", sha256="dccffa4c0768ee2ae4252bfc4c3947eaedc6881c7ace7548e483e2c74b5a4603")
    version("09.07.02", sha256="bf213045ddb589c2399baee2ecf4374f7953f25b1e3f9fca8443ae27f8eb5460")
    version("09.07.00", sha256="6dd6974a7f8898e8ba4f7319b9609bd14ec5ebd52b0b7e10ba63ff7fe4d7fb7a")
    version("09.06.02", sha256="4f2a53a37952af45e1d9e89739aa084364850853c969924b6a5d21f50dcdc1ce")
    version("09.06.01", sha256="eac9afd40a35e7c1866c3d26796c47ac8c839854d82dec7bbfedfb5153b941aa")
    version("09.06.00", sha256="c59fd141f1e2ca8a7a1b3ad714940f3e240d47960f3265fdf8092f59084d2caf")
    version("09.05.01", sha256="0510e0214de3ade148623da06e0b1019caee10715bac1b8596ece3a836b67909")
    version("09.05.00", sha256="130403d30bd58bc4c4063f11746cd9f52cee141ef38017e0cacbe9bbc9ea3eee")
    version(
        "09.04.07.01", sha256="4e472a604aa4d7700841b0c7ebea095fda9dfebff75429efaedbd8840c96ca8c"
    )
    version(
        "mwm1", tag="mwm1", git="https://github.com/marcmengel/lardataalg.git", get_full_repo=True
    )
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

    patch("v09_07_00.patch", when="@09.07.00")
    patch("v09_07_02.patch", when="@09.07.02")

    def patch(self):
        with when("@:09.16.04 %gcc@13:"):
            filter_file(
                "#include <string>",
                "#include <cstdint>\n#include <string>",
                "lardataalg/DetectorInfo/RunHistoryStandard.h",
            )

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("lardataobj")
    depends_on("cetmodules", type="build")
    depends_on("messagefacility")

    def cmake_args(self):
        args = [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]
        return args

    def setup_build_environment(self, spack_env):
        spack_env.set("CETBUILDTOOLS_VERSION", self.spec["cetmodules"].version)
        spack_env.set("CETBUILDTOOLS_DIR", self.spec["cetmodules"].prefix)
        spack_env.prepend_path("LD_LIBRARY_PATH", self.spec["root"].prefix.lib)
        # Binaries.
        spack_env.prepend_path("PATH", os.path.join(self.build_directory, "bin"))
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", os.path.join(self.build_directory, "lib"))
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(
            root=False, cover="nodes", order="post", deptype=("link"), direction="children"
        ):
            spack_env.prepend_path("ROOT_INCLUDE_PATH", str(self.spec[d.name].prefix.include))
        # Perl modules.
        spack_env.prepend_path("PERL5LIB", os.path.join(self.build_directory, "perllib"))
        # Set path to find fhicl files
        spack_env.prepend_path("FHICL_INCLUDE_PATH", os.path.join(self.build_directory, "fcl"))
        # Set path to find gdml files
        spack_env.prepend_path("FW_SEARCH_PATH", os.path.join(self.build_directory, "fcl"))
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
        # Set path to find fhicl files
        run_env.prepend_path("FHICL_FILE_PATH", os.path.join(self.prefix, "fcl"))
        # Cleaup.
        sanitize_environments(run_env)

    def setup_dependent_build_environment(self, spack_env, dspec):
        spack_env.set("LARDATAALG_INC", self.prefix.include)
        spack_env.set("LARDATAALG_LIB", self.prefix.lib)
        spack_env.append_path("ROOT_INCLUDE_PATH", self.prefix.include)
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        spack_env.prepend_path("PATH", self.prefix.bin)
        spack_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        spack_env.append_path("FHICL_FILE_PATH", "{0}/fcl".format(self.prefix))
        spack_env.append_path("FW_SEARCH_PATH", "{0}/gdml".format(self.prefix))

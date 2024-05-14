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


class Larpandora(CMakePackage):
    """Larpandora"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larpandora"
    git = "https://github.com/LArSoft/larpandora.git"
    url = "https://github.com/LArSoft/larpandora/archive/v01_02_03.tar.gz"
    list_url = "https://api.github.com/repos/LArSoft/larpandora/tags"

    version("09.22.05", sha256="730140a0a909cf7a817619fab653dc7d34cd508bd5f5e6f1e02b7ec810bc7d14")
    version("09.22.04", sha256="e0339bf349a45ac77c5dd8a32d7d9e45f4e78e088e2a9d39c66b1b095a75dad7")
    version("09.21.12", sha256="8b572f10d2fed37de543f75920b306d9404ed52edf3245af127989f4c23c60b2")
    version("09.21.09", sha256="1acdc3ba6926d4715f0eccd78b1bba4e967e1c5825884a0b30ee55de4cb1cfe2")
    version("09.21.05", sha256="7b0a68ccecd556fcde56dcbbdcde2664d6456778d43ec42d5e7e3518747da88e")
    version(
        "09.10.02.02", sha256="593b9702723987060ac957127e23e306a651a1768221d513e9b437f11d5125eb"
    )
    version(
        "09.10.02.01", sha256="52c2e4e4356aa2ba75eb13e95df2b737a058d63063a538903d2611796d25acf5"
    )
    version("09.09.05", sha256="fee068f0d7b3d4056aeacd6bb40beabc470b0f3bf0a9c1e236de0930971700e0")
    version("09.09.03", sha256="5b6b1198509427b3b79b34c9b33066a84f446b1dbc4a0645052ea33171d89a1e")
    version("09.09.02", sha256="6ac1e316cfba8efce16fcb5f7b130ac5f522b5c7552b07eb3817ca6a05734f4b")
    version("09.09.01", sha256="c226f2b98cdb0f6b5a610f109a97df0306e470efce6d7fcc0f82a8092ee2c4fc")
    version("09.09.00", sha256="7a8893e57f2ca00e8c2cd925a52789fd6b65831af99e2cae91b158518232dbc6")
    version("09.08.00", sha256="f002388f0043071d3519fea18aea00ed695dcb3fefc2bd786cae3d7f46c236af")
    version("09.07.06", sha256="5995bfefa845c71945024062c89f2643627f1810fb74a97db44d7815b44c3c5b")
    version("09.07.05", sha256="c9de839586a7c504dcd099a5aa936cf1958346d3cf20c3fedee8b5fa54037fa0")
    version("09.07.04", sha256="afac457dfc09f2d4c4c68781bed1a87e2f4f168658bd79b2a207bb3ae805edef")
    version(
        "mwm1", tag="mwm1", git="https://github.com/marcmengel/larpandora.git", get_full_repo=True
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

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    patch("v09_09_05.patch", when="@09.09.05")
    patch("v09_10_02_01.patch", when="@09.10.02.01")
    patch("v09_10_02_02.patch", when="@09.10.02.02")

    depends_on("messagefacility")
    depends_on("canvas")
    depends_on("art-root-io")
    depends_on("nug4")
    depends_on("nusimdata")
    depends_on("larreco")
    depends_on("larpandoracontent")
    depends_on("py-torch")
    depends_on("root")
    depends_on("cetmodules", type="build")

    def cmake_args(self):
        args = [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define_from_variant(
                "CMAKE_PREFIX_PATH", self.spec["py-torch"].package.cmake_prefix_paths[0]
            ),
            self.define("IGNORE_ABSOLUTE_TRANSITIVE_DEPENDENCIES", True),
        ]
        return args

    def flag_handler(self, name, flags):
        if name == "cxxflags" and self.spec.compiler.name == "gcc":
            flags.append("-Wno-error=deprecated-declarations")
            flags.append("-Wno-error=class-memaccess")
        return (flags, None, None)

    def setup_build_environment(self, spack_env):
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
        # Set path to find gdml files
        run_env.prepend_path("FW_SEARCH_PATH", os.path.join(self.prefix, "fw"))
        # Cleaup.
        sanitize_environments(run_env)

    def setup_dependent_build_environment(self, spack_env, dspec):
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        spack_env.prepend_path("PATH", self.prefix.bin)
        spack_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        spack_env.append_path("FHICL_FILE_PATH", "{0}/fcl".format(self.prefix))
        spack_env.append_path("FW_SEARCH_PATH", "{0}/gdml".format(self.prefix))
        spack_env.append_path("FW_SEARCH_PATH", "{0}/fw".format(self.prefix))

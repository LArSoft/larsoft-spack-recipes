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


class Larreco(CMakePackage):
    """Larreco"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larreco"
    git = "https://github.com/LArSoft/larreco.git"
    url = "https://github.com/LArSoft/larreco/archive/v01_02_03.tar.gz"
    list_url = "https://api.github.com/repos/LArSoft/larreco/tags"

    version("09.25.00", sha256="2525808cc5257a9eb5ef253fb7d3d0078fe4abaa9b22c01f06bf1c69e9b1caf0")
    version("09.24.04", sha256="6af645abf213b9b474e404ebcf5339e0d07243ff046d730f5005b37f555d3aa7")
    version("09.23.01", sha256="168dcf19c40295cc98b6549866520da78c2a1fbaf91680b41a3255793f87e232")
    version("09.22.03", sha256="6e7c0e11bd70fb47f4f0f39e211a60dcf3c4d888415eb2cf7a48070b43aa1a7b")
    version("09.22.00", sha256="b7389f283b1ba23571022af44f3d62006d5b5e0c0f3d3b9f653e2d983c1d8541")
    version(
        "09.07.08.02", sha256="eba7aba2443f4c9efdb0f071db9ca6ffb7f6e0630283f235759c51586e33c449"
    )
    version(
        "09.07.08.vec01",
        branch="larvecutils-v09_37_01_01",
        git="https://github.com/cerati/larreco.git",
    )
    version(
        "09.07.08.01", sha256="6406a601f3f00ba1626f9f6c5ebbddf8aa6759e95da5b4d409db3131b031445a"
    )
    version("09.07.05", sha256="991a058854c730d1bcbd7056652669f5c24d37faaa879e85e0befd5f65ff7aa3")
    version("09.07.03", sha256="03921a26a025361ecda0015c0cb54eb003cf34847fef46beb15a4b60e5e971d6")
    version("09.07.02", sha256="26f215907727ff0e8567b39fcac65169b5f06948397d775009a39c0c30ed3469")
    version("09.07.01", sha256="527e23aaaad0e556a744d64abe11350746f9f5d86d6b5761cc1cbaac81bcb1b9")
    version("09.07.00", sha256="5616d751f14a1903efaebf3c193451e99f3cce674a4d00dd499241f942681cfb")
    version("09.06.17", sha256="018feacc42ba65116e3a5cf97fca91d35588b86b369b499e3b1074c46c728063")
    version("09.06.16", sha256="d616e607cca3949fe92fdb10d2552b43177b56e4281ed0b365e26f051c9a34bb")
    version("09.06.15", sha256="0008866cf4b342f5002abd736773aee3c314b1077b0f035a7c564e0e069a102d")
    version(
        "mwm1", tag="mwm1", git="https://github.com/marcmengel/larreco.git", get_full_repo=True
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

    patch("v09_07_05.patch", when="@09.07.05")
    patch("v09_07_08_01_larvecutils.patch", when="@09.07.08.vec01")
    # patch('v09_07_08_01.patch', when='@09.07.08.01')
    patch("v09_07_08_02.patch", when="@09.07.08.02")

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )
    variant("tf", default=False, description="Build tensorflow dependent libraries.")

    depends_on("cetmodules", type="build")
    depends_on("art")
    depends_on("boost")
    depends_on("canvas-root-io")
    depends_on("cetlib-except")
    depends_on("clhep")
    depends_on("eigen")
    depends_on("geant4")
    depends_on("larsim")
    depends_on("larsoft-data")
    depends_on("larvecutils", when="@09.07.08.vec01")
    depends_on("marley")
    depends_on("nutools")
    depends_on("py-tensorflow", when="+tf")
    depends_on("root+tmva")
    depends_on("rstartree")
    depends_on("tbb")

    def cmake_args(self):
        args = [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define("IGNORE_ABSOLUTE_TRANSITIVE_DEPENDENCIES", True),
            self.define("RStarTree_INCLUDE_DIR", self.spec["rstartree"].prefix.include),
        ]
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
        run_env.prepend_path("FHICL_FILE_PATH", os.path.join(self.prefix, "fcl"))
        # Set path to find gdml files
        run_env.prepend_path("FW_SEARCH_PATH", os.path.join(self.prefix, "fw"))
        # Cleaup.
        sanitize_environments(run_env)

    def setup_dependent_build_environment(self, spack_env, dspec):
        spack_env.set("LARRECO_INC", self.prefix.include)
        spack_env.set("LARRECO_LIB", self.prefix.lib)
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        spack_env.prepend_path("PATH", self.prefix.bin)
        spack_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        spack_env.append_path("FHICL_FILE_PATH", "{0}/fcl".format(self.prefix))
        spack_env.append_path("FW_SEARCH_PATH", "{0}/fw".format(self.prefix))
        sanitize_environments(spack_env)

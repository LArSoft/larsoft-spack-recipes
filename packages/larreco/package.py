# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.package import *
from spack.pkg.fnal_art.fnal_github_package import *
from spack.util.prefix import Prefix


class Larreco(CMakePackage, FnalGithubPackage):
    """Larreco"""

    repo = "LArSoft/larreco"
    version_patterns = ["v09_00_00", "09.23.09"]

    version("10.01.04", sha256="a6762f9410d2ff288f56b1e106abe0aec88ef2c75f11c97bcc6dcc6826ac8f33")
    version("10.01.03", sha256="4ba539763f2a182b056c5f23ab2c27bbb79bb4f8f57c8ba0424ff298ee581ccd")
    version("10.00.02", sha256="0502b61c043efff8519787c411d15fc57a4bda66b7f50dc355e01fd1584e45d9")
    version("09.26.01", sha256="9b291a4e52e042bfb5714ae4428cc35454a9ce2733615db682f876e20c1934ff")
    version("09.25.00", sha256="cae4f414b02a61d2cc0e1f915f71c0a6337418737e2939be0d01df931e73bc77")
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", default="17")

    depends_on("cetmodules", type="build")

    depends_on("art")
    depends_on("art-root-io")
    depends_on("boost")
    depends_on("canvas-root-io", when="@:09.25.00.01")
    depends_on("cetlib-except")
    depends_on("cetlib")
    depends_on("clhep")
    depends_on("eigen")
    depends_on("fhicl-cpp")
    depends_on("geant4")
    depends_on("larcorealg")
    depends_on("larcoreobj")
    depends_on("larcore")
    depends_on("lardataalg")
    depends_on("lardataobj")
    depends_on("lardata")
    depends_on("larsim")
    depends_on("larvecutils")
    depends_on("messagefacility")
    depends_on("nug4")
    depends_on("nurandom")
    depends_on("nusimdata")
    depends_on("range-v3")
    depends_on("root+tmva")
    depends_on("rstartree")
    depends_on("tbb")

    patch('09.25.00.patch', when='@09.25.00')

    @cmake_preset
    def cmake_args(self):
        return [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define("IGNORE_ABSOLUTE_TRANSITIVE_DEPENDENCIES", True),
            self.define("RStarTree_INCLUDE_DIR", self.spec["rstartree"].prefix.include),
        ]

    @sanitize_paths
    def setup_build_environment(self, env):
        prefix = Prefix(self.build_directory)
        env.prepend_path("PATH", prefix.bin)  # Binaries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        env.prepend_path("FHICL_FILE_PATH", prefix.job)

    @sanitize_paths
    def setup_run_environment(self, env):
        env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        env.prepend_path("FHICL_FILE_PATH", self.prefix.job)

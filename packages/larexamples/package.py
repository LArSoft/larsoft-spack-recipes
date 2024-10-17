# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.fnal_art.fnal_github_package import *
from spack.util.prefix import Prefix


class Larexamples(CMakePackage, FnalGithubPackage):
    """Larexamples"""

    repo = "LArSoft/larexamples"
    version_patterns = ["v09_00_00", "09.08.18"]

    version("10.00.02", sha256="39e801277d747cf26241c8f5abfa184577e09b1dd72ed704b77fcba865246fc6")
    version("09.09.11", sha256="a5801b1e452fc873ab5a115897f6489e786edbbbd3366242b1c523254bd484f6")
    version("09.09.05", sha256="a57de45e38b91252c42592f179355420c642cfb5af6bfeecd336bb1abde5ac9c")
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", default="17")

    depends_on("cetmodules", type="build")

    depends_on("art")
    depends_on("art-root-io")
    depends_on("boost+test")
    depends_on("canvas")
    depends_on("canvas-root-io")
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("fhicl-cpp")
    depends_on("larcorealg")
    depends_on("larcoreobj")
    depends_on("larcore")
    depends_on("lardataobj")
    depends_on("lardata")
    depends_on("larsim")
    depends_on("messagefacility")
    depends_on("nusimdata")
    depends_on("root")

    def patch(self):
        files = ["test/Algorithms/TotallyCheatTracks/CMakeLists.txt",
             "larexamples/AnalysisExample/CMakeLists.txt",
             "larexamples/Algorithms/TotallyCheatTracks/CheatTrackData/CMakeLists.txt",
             "larexamples/Algorithms/TotallyCheatTracks/CMakeLists.txt"]
        for file in files:
            filter_file("nusimdata::SimulationBase", "nusimdata::SimulationBase dk2nu::Tree", file)

    @cmake_preset
    def cmake_args(self):
        return [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]

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

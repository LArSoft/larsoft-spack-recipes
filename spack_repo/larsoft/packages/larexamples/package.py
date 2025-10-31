# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.package import *
from spack.util.prefix import Prefix
from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.fnal_art.packages.fnal_github_package.package import *


class Larexamples(CMakePackage, FnalGithubPackage):
    """Larexamples"""

    repo = "LArSoft/larexamples"
    git = "https://github.com/%s" % repo
    version_patterns = ["v09_00_00", "09.08.18"]

    version("10.00.25", sha256="8394b935b55827cc88641ef264dd72a34bd68b544146317d45381cb1110eadf9") 
    version("10.00.24", sha256="fdee1a6e7af5ed28d164d56cc1c82685d197e94f89d2e8d5f5445eee07ecefb4")
    version("10.00.23", sha256="81cfc81c2493a731d783ecfd1c45c1e0e3519437ad065f74e0a9037dd127bafb")
    version("10.00.22", sha256="9bc1839808c76c47de5d3ed70a7bf391a63bd37ee4850b3dc41a39cddb76b32f")
    version("10.00.20", sha256="4f2a73a1f921a939d36c7a0f7ed2a5a3fd019719d2875e5a2567f51ad280cdc5")
    version("10.00.17", sha256="2f86f99627cd2abfa12756670306dafe637b932ebfe347b1a83cf91fa6b810be")
    version("10.00.16", sha256="0bacbdd35c67acaaa9c22bc259e8567c52866f5ef9fdfc9ad19a8d8a8d4adce9")
    version("10.00.12", sha256="4e1e2b3c9eb82076d73f1bb0ca92540085a1ca8f898d5b4333770a7ad1fdef59")
    version("10.00.11", sha256="bae9aa81b2d3fd17b07bcbab7561a29b6850ec7711f95f9b3a1b732c617e55e6")
    version("10.00.10", sha256="a8fdd6852ec62be0474b51c629c96fa5ef13481c733812e299c39665f7fa86d6")
    version("10.00.06", sha256="0ee35d7e5c4cd5d7dc32d208ca714eb243102a655168ac71932549f4fdc67607")
    version("10.00.05", sha256="3e516bfeb580b5d073db2b9a26003a7378a76265f5c3f7fe3bb7f8e4e35f947e")
    version("10.00.02", sha256="39e801277d747cf26241c8f5abfa184577e09b1dd72ed704b77fcba865246fc6")
    version("09.09.11", sha256="a5801b1e452fc873ab5a115897f6489e786edbbbd3366242b1c523254bd484f6")
    version("09.09.05", sha256="a57de45e38b91252c42592f179355420c642cfb5af6bfeecd336bb1abde5ac9c")
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", default="17")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("cetmodules", type="build")
    depends_on("larsoft-data", type=("build", "test"))

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

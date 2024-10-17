# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.fnal_art.fnal_github_package import *
from spack.util.prefix import Prefix


class Lardataobj(CMakePackage, FnalGithubPackage):
    """Lardataobj"""

    repo = "LArSoft/lardataobj"
    version_patterns = ["v09_00_00", "09.18.00"]

    version("10.00.00", sha256="13d44ca0292338454e4857de555bb3fb8033b70bed5ed61012f2ad0c1b60e376")
    version("09.19.00", sha256="8e689900cef678fb25c161f7fc676be25b64f1d79e65a9839d4c7e5b1a7c1040")
    version("09.18.03", sha256="032a4c48473dc87c204c3aaef4bdf4953599de26cd1642cb51fd6f7692adcb6d")
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", default="17")

    depends_on("cetmodules", type="build")

    depends_on("boost+test")
    depends_on("canvas")
    depends_on("canvas-root-io")
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("nusimdata")
    depends_on("larcorealg")
    depends_on("larcoreobj")
    depends_on("messagefacility")
    depends_on("root")

    def patch(self):
        for file in ['lardataobj/Simulation/CMakeLists.txt', 'lardataobj/AnalysisBase/CMakeLists.txt']:
            filter_file('nusimdata::SimulationBase', 'nusimdata::SimulationBase dk2nu::Tree', file)

    @cmake_preset
    def cmake_args(self):
        return [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]

    @sanitize_paths
    def setup_build_environment(self, env):
        prefix = Prefix(self.build_directory)
        env.prepend_path("PATH", prefix.bin)  # Binaries.
        env.prepend_path("FHICL_FILE_PATH", prefix.job)

    @sanitize_paths
    def setup_run_environment(self, env):
        env.prepend_path("FHICL_FILE_PATH", self.prefix.job)
        env.prepend_path("FW_SEARCH_PATH", self.prefix.compatibility)

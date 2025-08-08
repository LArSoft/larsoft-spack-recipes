# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.package import *
from spack.util.prefix import Prefix
from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.fnal_art.packages.fnal_github_package.package import *


class Lardataobj(CMakePackage, FnalGithubPackage):
    """Lardataobj"""

    repo = "LArSoft/lardataobj"
    version_patterns = ["v09_00_00", "09.18.00"]

    version("10.02.00", sha256="13f7ce1e2cccfb6ca073cfb7731e103d0aed0cf112625253dc5c1094a36a1837")
    version("10.01.00", sha256="1d0306c0c0ae270335bf869852295d5c25a95d2acb99c8836f7144bac06063ec")
    version("10.00.02", sha256="5c4022c33be601fc3e7e5f06dd3a5cff2564264753868bd7ea4fbb8cd4df13a4")
    version("10.00.00", sha256="13d44ca0292338454e4857de555bb3fb8033b70bed5ed61012f2ad0c1b60e376")
    version("09.19.00", sha256="8e689900cef678fb25c161f7fc676be25b64f1d79e65a9839d4c7e5b1a7c1040")
    version("09.18.03", sha256="032a4c48473dc87c204c3aaef4bdf4953599de26cd1642cb51fd6f7692adcb6d")
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", default="17")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

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

# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.package import *
from spack.pkg.fnal_art.fnal_github_package import *
from spack.util.prefix import Prefix


class Larg4(CMakePackage, FnalGithubPackage):
    """Larg4"""

    repo = "LArSoft/larg4"
    version_patterns = ["v09_00_00", "09.18.00"]

    version("10.00.04", sha256="126814c20b77359c28aedd3b6150c9fb8677bb16a7a8c1ee77e14a8ae36d3802")
    version("10.00.03", sha256="1ffeb259e2986e185c9bef4c8ce08268c68d46938784e43745cbbe3a8a86c60e")
    version("10.00.01", sha256="89f414f6199ec8c0ca18ccb4c15ae0e4d89e5ffe4436ab3d1fe85a2610486955")
    version("09.19.03", sha256="0359f862e4a9a95f5dd1f70e37d6d577c2dc13458adf0060d13b01da30b1d751")
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", default="17")

    depends_on("cetmodules", type="build")

    depends_on("art")
    depends_on("art-root-io")
    depends_on("artg4tk")
    depends_on("canvas")
    depends_on("canvas-root-io", when="@:09.19.03")
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("clhep")
    depends_on("fhicl-cpp")
    depends_on("geant4")
    depends_on("larcorealg")
    depends_on("larcore")
    depends_on("lardataalg")
    depends_on("lardataobj")
    depends_on("messagefacility")
    depends_on("nug4")
    depends_on("nurandom")
    depends_on("nusimdata")
    depends_on("range-v3")
    depends_on("root")

    @cmake_preset
    def cmake_args(self):
        return [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]

    def flag_handler(self, name, flags):
        if name == "cxxflags" and self.spec.compiler.name == "gcc":
            flags.append("-Wno-error=deprecated-declarations")
            flags.append("-Wno-error=class-memaccess")
        return (flags, None, None)

    @sanitize_paths
    def setup_build_environment(self, env):
        prefix = Prefix(self.build_directory)
        env.prepend_path("PATH", prefix.bin)  # Binaries
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)

    @sanitize_paths
    def setup_run_environment(self, env):
        env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        env.prepend_path("FHICL_FILE_PATH", self.prefix.fcl)
        env.prepend_path("FW_SEARCH_PATH", self.prefix.G4)
        env.prepend_path("FW_SEARCH_PATH", self.prefix.gdml)

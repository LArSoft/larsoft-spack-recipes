# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.package import *
from spack.util.prefix import Prefix
from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.fnal_art.packages.fnal_github_package.package import *


class Larg4(CMakePackage, FnalGithubPackage):
    """Larg4"""

    repo = "LArSoft/larg4"
    git = "https://github.com/%s" % repo
    version_patterns = ["v09_00_00", "09.18.00"]

    version("10.01.01", sha256="7342df284cc1077ad6b0558f1d9ea9af5a57086931df3daa5be4c3b8349808b5")
    version("10.01.00", sha256="0489eae228ceaf4e83e03ff79af2f47d2b173ea85d1d1cacb2e0532dcc693475")
    version("10.00.13", sha256="a51f8f6a9333c8f2f260a61647e599c84e62e63fa378b23925f215bd87633605")
    version("10.00.12", sha256="561a02ea708fd4f1255717863f587c009b68dfe6f51f301a3f385ce1edb5ed3d")
    version("10.00.09", sha256="ffd8911bad84c0b48f441ef57091dd0a4b96abe1976dcb0ae4a8690b1206a086")
    version("10.00.08", sha256="f2c8de43173a9fbeb5812cf0e6475ede2e6deb70a8df1bc2e6db7ef9ca3f4d54")
    version("10.00.07", sha256="fa2f0ea4fec73cd0a0b34d5ef6e0d4f437831244c4c616cc45885c6125beae61")
    version("10.00.04", sha256="126814c20b77359c28aedd3b6150c9fb8677bb16a7a8c1ee77e14a8ae36d3802")
    version("10.00.03", sha256="1ffeb259e2986e185c9bef4c8ce08268c68d46938784e43745cbbe3a8a86c60e")
    version("10.00.01", sha256="89f414f6199ec8c0ca18ccb4c15ae0e4d89e5ffe4436ab3d1fe85a2610486955")
    version("09.19.03", sha256="0359f862e4a9a95f5dd1f70e37d6d577c2dc13458adf0060d13b01da30b1d751")
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", default="17")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

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

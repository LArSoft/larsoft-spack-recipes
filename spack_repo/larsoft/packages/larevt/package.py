# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.package import *
from spack.util.prefix import Prefix
from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.fnal_art.packages.fnal_github_package.package import *


class Larevt(CMakePackage, FnalGithubPackage):
    """Larevt"""

    repo = "LArSoft/larevt"
    git = "https://github.com/%s.git" % repo
    version_patterns = ["v09_00_00", "09.10.00"]

    version("10.00.11", sha256="7c15a795ad1f50f4d19057929f8bed2fbc36c8e621f5816d911c521d6353a9c8")
    version("10.00.08", sha256="026eeabce2b01c15fcd90effa6e05a2ebe125709b2b09d7ef5c1732eb09a5241")
    version("10.00.07", sha256="bafaf49674522515109e89321f13f1157e27b32999e487f4e48aac1b3bb0ff18")
    version("10.00.04", sha256="750db876087641ca736d7465e86fa6dac43a1493ef3a6e9c8e030c4d8eb615bd")
    version("10.00.03", sha256="8456cca33b8437d234ed3c4c7c8d7ea677da77805a683bfc3111a0e6a2243992")
    version("10.00.01", sha256="eb90abf975f61a4fd89ec98d42ffb02f3b4c79f2940e317dcb79498b4184cf0e")
    version("09.10.07", sha256="f8827eee1aec519a7b13c11460b505278df00fcd911abd008001fdf64dcf5762")
    version("09.10.03", sha256="3165ae94c7dab00d5e783be9c63a485ebbca435d9d43f0e19d6b822e98a17c3c")
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", default="17")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("cetmodules", type="build")

    depends_on("art")
    depends_on("art-root-io")
    depends_on("canvas-root-io", when="@:09.10.03")
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("fhicl-cpp")
    depends_on("larcorealg")
    depends_on("larcoreobj")
    depends_on("larcore")
    depends_on("lardataobj")
    depends_on("lardata")
    depends_on("libwda")
    depends_on("messagefacility")
    depends_on("nusimdata")
    depends_on("root")
    depends_on("sqlite")

    @cmake_preset
    def cmake_args(self):
        return [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define("IGNORE_ABSOLUTE_TRANSITIVE_DEPENDENCIES", True),
        ]

    @sanitize_paths
    def setup_build_environment(self, env):
        prefix = Prefix(self.build_directory)
        env.prepend_path("PATH", prefix.bin)  # Binaries
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)

    @sanitize_paths
    def setup_run_environment(self, env):
        env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        env.prepend_path("FHICL_FILE_PATH", self.prefix.job)

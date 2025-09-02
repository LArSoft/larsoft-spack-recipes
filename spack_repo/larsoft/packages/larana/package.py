# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.package import *
from spack.util.prefix import Prefix
from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.fnal_art.packages.fnal_github_package.package import *


class Larana(CMakePackage, FnalGithubPackage):
    """Larana"""

    repo = "LArSoft/larana"
    git = "https://github.com/%s" % repo
    version_patterns = ["v09_00_00", "09.14.19"]

    version("10.00.24", sha256="a0f9bcfe874655832eafcf43b2676035c1e797d70bda70336da1d75dce7d4f8c")
    version("10.00.21", sha256="c62f4c88e92d10bafa9d52fe086df40e928ac00041ceaa8dd4896a452ea39665")
    version("10.00.20", sha256="f62d136360ccd82d3beb9ba43687384b884833b7a5baa75eabde278bdce4930d")
    version("10.00.16", sha256="0ac8413d3d2c9332886a80659a764b680d104260a2773056938bad2cd4278b57")
    version("10.00.15", sha256="e1ed411bd51b15552faf1e0cd882e08b0fd19f13286bd5f31c3cae76641ef21e")
    version("10.00.14", sha256="b9a0e437aeeb0ac56db2dfcc05c24fca8ea5b4693400199d307cc9d4bc09a6fc")
    version("10.00.07", sha256="bd08f4b0115ae68622d2e5037ee57e98479dca8314c69e14cd98ceaaf0f7e5b8")
    version("10.00.06", sha256="474fa3e1cdb83fa55a2f3a4fbfe3dab7a96e6a3961155202e6b62e4079b4a317")
    version("10.00.02", sha256="67ee61f9e2cfb1878199a1580f6f2fca119efc74babed8edf76ee9e58464b6e3")
    version("09.15.14", sha256="e476411f3e8ae9b7b81dc32af011a417c5e9de1d9fda1764d78ee941fcf4e384")
    version("09.15.05", sha256="23c61e4f00d1e9d14da1da3378541b67f9852174cac4bd8965b28cbca091dc60")
    version("09.14.19", sha256="ea7de5c605cb92b73746615329a13778c769e8b24e6a04d05df8655e40912a28")
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", default="17")

    depends_on("cetmodules", type="build")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("art")
    depends_on("art-root-io")
    depends_on("canvas")
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("clhep")
    depends_on("fhicl-cpp")
    depends_on("larcorealg")
    depends_on("larcoreobj")
    depends_on("larcore")
    depends_on("lardataalg")
    depends_on("lardataobj")
    depends_on("lardata")
    depends_on("larreco")
    depends_on("larsim")
    depends_on("nug4")
    depends_on("nurandom")
    depends_on("nusimdata")
    depends_on("root +tmva")

    with when("@:09.15.05"):
        depends_on("canvas-root-io")
        depends_on("eigen")
        depends_on("larevt")
        depends_on("postgresql")

    @cmake_preset
    def cmake_args(self):
        return [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]

    @sanitize_paths
    def setup_build_environment(self, env):
        prefix = Prefix(self.build_directory)
        env.prepend_path("PATH", prefix.bin)  # Binaries
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)

    @sanitize_paths
    def setup_run_environment(self, env):
        env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        env.append_path("FHICL_FILE_PATH", self.prefix.job)

    def flag_handler(self, name, flags):
        if name == "cxxflags" and self.spec.compiler.name == "gcc":
            flags.append("-Wno-error=deprecated-declarations")
            flags.append("-Wno-error=class-memaccess")
        return (flags, None, None)

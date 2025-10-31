# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.package import *
from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.fnal_art.packages.fnal_github_package.package import *


class Larsimrad(CMakePackage, FnalGithubPackage):
    """larsimrad"""

    repo = "LArSoft/larsimrad"
    git = "https://github.com/%s" % repo
    version_patterns = ["v09_00_00", "09.08.18"]

    version("10.00.25", sha256="e5d245559960e95cd2e7ff15da8c12e4b4f30c34eccc495af0bd2baa75b2cf06")
    version("10.00.24", sha256="a7d5a5b3b991689fd24d9ad925274f51f517362e010293a552ec4add302a2dcd")
    version("10.00.23", sha256="2462df8e565428cb42ee419ef3eb237bfb519f2bbef9c4a9721082c1ff8c29e5")
    version("10.00.22", sha256="57ee6c838516848aaa4fe7a6721ef16f772b5037916ff7ad1b06603d566fc73f")
    version("10.00.20", sha256="056f5b4fe28a48651864df8b2796cb17f6a0f7b4c06b3cc495c04d7b003393b3")
    version("10.00.17", sha256="2e0f15009971e08e846882b175dc69b3e60f88d220fd2eada5379ed2eb261a0e")
    version("10.00.16", sha256="dd69b3cc7876155231f2c55e6a2d7c4c36c0e31a5d067519559a9a029688c0b8")
    version("10.00.12", sha256="9d79deea2318d52e0974e9a53201756ee2ea8881a66779971de5c55264baf635")
    version("10.00.11", sha256="b8dd47dbb9cb67804bf12714440582d3da92f99af7afa4871ab11bfddf940cb2")
    version("10.00.10", sha256="b5956533f2c298540b2e9ffa09fb9d791bcdcee47ab1f443e14264f215b9a150")
    version("10.00.06", sha256="a6f23dd95b0286f2622bb72cfb9f4cc020741dbed4e4a8233bfe3a474d074200")
    version("10.00.05", sha256="e8b90dd34f0145480ca8d70349f73acf2cd32651450df67b4b0b10dcdbfd0dfc")
    version("10.00.02", sha256="02fd6b9c39c14250526239247da75ff46a8801480d3eb2e7aa3c82148b15727f")
    version("09.09.11", sha256="f0a22b39fc77eeadb2a20bf0adc74813e680420b745cccd34fb2705a2e67656e")
    version("09.09.05", sha256="a1bc6bfbbc375593b1dc018cd6e658d0236e2165f723ea59684aa872a04191be")
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", default="17")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("cetmodules", type="build")

    depends_on("art")
    depends_on("art-root-io")
    depends_on("bxdecay0")
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("clhep")
    depends_on("fhicl-cpp")
    depends_on("larcoreobj")
    depends_on("larcore")
    depends_on("lardataobj", when="@:09.09.05.01")
    depends_on("lardata")
    depends_on("larsim")
    depends_on("nugen")
    depends_on("nurandom")
    depends_on("nusimdata")
    depends_on("root")

    @cmake_preset
    def cmake_args(self):
        return [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]

    @sanitize_paths
    def setup_run_environment(self, env):
        env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)

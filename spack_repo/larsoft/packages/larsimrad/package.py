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

    version("10.01.13", sha256="4c11d3c695ef419ee318c2e425a697e151dc21f1852803915d968fe410e5f39b")
    version("10.01.12", sha256="d27b1c5f78ddac48ebd9beecd24035034a5dab7bab877d5cb573917301bfe4d7")
    version("10.01.11", sha256="d2dd7af495c6d7e8aa770bda72ffd62bcd90cd7a84d7c4754cd51f7e441996ca")
    version("10.01.10", sha256="9ed43ef7bb79420127fe10e69c6ab8c843a95e7fe844ec4363dd3ef08bd2de62")
    version("10.01.09", sha256="6239592d70329e7162ebef08e95288b3c6cf5a2c8e83f3b7b52e38d96fcefae0")
    version("10.01.08", sha256="9a55eda54b706078d1ff5b3026ec5c6d203311cee3d1ae0ddf1491d4430f08dd")
    version("10.01.07", sha256="7de1f180e29c101fb73788e3744d91985b8c675ca93a9eb1e9579b8ae6c5ea67")
    version("10.01.06", sha256="752fd8fb6c4c3532b3ce4d1e0ddfa90ce239415b5ba7fa5e23f9572eb3c06196")
    version("10.01.05", sha256="b96d263accb6d37409176edcb898dcb203e7f71a2541bcbd882e095eb2e89bd6")
    version("10.01.04", sha256="2a7da3c10a57e20a47c8f14f94932be58fc7ea65601ef96c4e3b4355a0cf4616")
    version("10.01.03.02", sha256="6fdd24ddec11d90c343f68845d886ba825d8be169a508a7a42bba143975e8ea4")
    version("10.01.03.01", sha256="5d626bf40e7366d61d3d7e1fa8d6ad7ab55586f3ef00da17edb4d4685e470b15")
    version("10.01.03", sha256="f695391633a5d0ec9b7f1832e8f66f346ff735c190029512bc03d62799ca6666")
    version("10.01.01", sha256="f5e7c8b7dba0df5946c73c408e1bec3f27e548a1b2d4532fd195f0cf5bbd4f03")
    version("10.01.00", sha256="e2b884938bb49ddd1da4fadb632fd4486edea5454d226345a1c863af2a992d53")
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

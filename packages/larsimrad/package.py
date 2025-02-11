# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.package import *
from spack.pkg.fnal_art.fnal_github_package import *


class Larsimrad(CMakePackage, FnalGithubPackage):
    """larsimrad"""

    repo = "LArSoft/larsimrad"
    version_patterns = ["v09_00_00", "09.08.18"]

    version("10.00.06", sha256="a6f23dd95b0286f2622bb72cfb9f4cc020741dbed4e4a8233bfe3a474d074200")
    version("10.00.05", sha256="e8b90dd34f0145480ca8d70349f73acf2cd32651450df67b4b0b10dcdbfd0dfc")
    version("10.00.02", sha256="02fd6b9c39c14250526239247da75ff46a8801480d3eb2e7aa3c82148b15727f")
    version("09.09.11", sha256="f0a22b39fc77eeadb2a20bf0adc74813e680420b745cccd34fb2705a2e67656e")
    version("09.09.05", sha256="a1bc6bfbbc375593b1dc018cd6e658d0236e2165f723ea59684aa872a04191be")
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", default="17")

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

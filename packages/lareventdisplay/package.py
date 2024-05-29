# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.fnal_art.fnal_github_package import *


class Lareventdisplay(CMakePackage, FnalGithubPackage):
    """Lareventdisplay"""

    repo = "LArSoft/lareventdisplay"
    version_patterns = ["v09_00_00", "09.10.19"]

    version(
        "09.11.05.01", sha256="b438dbc1fa3a776af3a6d0ca4b4fad574efca6123126c50e1efc2e5df4568291"
    )
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", default="17")

    depends_on("cetmodules", type="build")

    depends_on("art")
    depends_on("canvas")
    depends_on("canvas-root-io")
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("eigen")
    depends_on("fhicl-cpp")
    depends_on("larcorealg")
    depends_on("larcoreobj")
    depends_on("larcore")
    depends_on("lardataalg")
    depends_on("lardataobj")
    depends_on("lardata")
    depends_on("larevt")
    depends_on("larsim")
    depends_on("messagefacility")
    depends_on("nuevdb")
    depends_on("nusimdata")
    depends_on("root")

    with when("@:09.11.05.01"):
        depends_on("art-root-io")
        depends_on("zlib")

    @cmake_preset
    def cmake_args(self):
        return [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]

    @sanitize_paths
    def setup_run_environment(self, env):
        env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        env.prepend_path("FHICL_FILE_PATH", self.prefix.job)

    def flag_handler(self, name, flags):
        if name == "cxxflags" and self.spec.compiler.name == "gcc":
            flags.append("-Wno-error=deprecated-declarations")
            flags.append("-Wno-error=class-memaccess")
        return (flags, None, None)

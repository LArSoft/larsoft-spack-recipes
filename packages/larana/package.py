# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.fnal_art.fnal_github_package import *
from spack.util.prefix import Prefix


class Larana(CMakePackage, FnalGithubPackage):
    """Larana"""

    repo = "LArSoft/larana"
    version_patterns = ["v09_00_00", "09.14.19"]

    version("09.15.05.01", sha256="83ec6fad88591adf8377e12713c6cd3dcc32d1ebcfb623ddcc0c752156963738")
    version("09.15.05", sha256="23c61e4f00d1e9d14da1da3378541b67f9852174cac4bd8965b28cbca091dc60")
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", default="17")

    depends_on("cetmodules", type="build")

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

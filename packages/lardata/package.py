# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.fnal_art.fnal_github_package import *
from spack.util.prefix import Prefix


class Lardata(CMakePackage, FnalGithubPackage):
    """Lardata"""

    repo = "LArSoft/lardata"
    version_patterns = ["v09_00_00", "09.16.00"]

    version("09.16.03", sha256="e73f75875a8e769ccc684d4adc670d5d74e4d936657b9dc9a9f3aa3631b0682e")
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", default="17")

    depends_on("cetmodules", type="build")
    depends_on("canvas-root-io", type="build")  # For dictionary-building in tests

    depends_on("art")
    depends_on("art-root-io")
    depends_on("boost +date_time+serialization+test")
    depends_on("canvas")
    depends_on("fhicl-cpp")
    depends_on("fftw")
    depends_on("larcore")
    depends_on("larcorealg")
    depends_on("larcoreobj")
    depends_on("lardataalg")
    depends_on("lardataobj")
    depends_on("larvecutils")
    depends_on("messagefacility")
    depends_on("nutools")
    depends_on("postgresql")
    depends_on("range-v3")
    depends_on("root+fftw")

    depends_on("nusimdata", when="@:09.16.03")

    @cmake_preset
    def cmake_args(self):
        return [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define("IGNORE_ABSOLUTE_TRANSITIVE_DEPENDENCIES", True),
        ]

    def flag_handler(self, name, flags):
        if name == "cxxflags" and self.spec.compiler.name == "gcc":
            flags.append("-Wno-error=deprecated-declarations")
            flags.append("-Wno-error=class-memaccess")
        return (flags, None, None)

    @sanitize_paths
    def setup_build_environment(self, env):
        prefix = Prefix(self.build_directory)
        env.prepend_path("PATH", prefix.bin)  # Binaries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        env.prepend_path("FHICL_FILE_PATH", prefix.job)

    @sanitize_paths
    def setup_run_environment(self, env):
        env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        env.prepend_path("FHICL_FILE_PATH", self.prefix.job)

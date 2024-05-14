# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.fnal_art.fnal_github_package import *
from spack.util.prefix import Prefix


class Larsim(CMakePackage, FnalGithubPackage):
    """Larsim"""

    repo = "LArSoft/larsim"
    version_patterns = ["v09_00_00", "09.40.01"]

    version(
        "09.43.00.01", sha256="397fa4d50b00d2d0535266b71a60449f00707f1572f5110ab2f554d00ec0029a"
    )
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", default="17")

    depends_on("cetmodules", type="build")

    depends_on("art")
    depends_on("art-root-io")
    depends_on("artg4tk")
    depends_on("boost")
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("clhep")
    depends_on("cry")
    depends_on("dk2nudata")
    depends_on("dk2nugenie")
    depends_on("fhicl-cpp")
    depends_on("geant4")
    depends_on("genie")
    depends_on("ifdhc")
    depends_on("larcorealg")
    depends_on("larcoreobj")
    depends_on("larcore")
    depends_on("lardataalg")
    depends_on("lardataobj")
    depends_on("lardata")
    depends_on("larevt")
    depends_on("log4cpp")
    depends_on("marley")
    depends_on("messagefacility")
    depends_on("nufinder")
    depends_on("nug4")
    depends_on("nugen")
    depends_on("nurandom")
    depends_on("nusimdata")
    depends_on("nutools")
    depends_on("ppfx")
    depends_on("range-v3")
    depends_on("root")
    depends_on("sqlite")

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
        env.prepend_path("FW_SEARCH_PATH", prefix.G4)
        env.prepend_path("FW_SEARCH_PATH", prefix.gdml)

    @sanitize_paths
    def setup_run_environment(self, env):
        env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        env.prepend_path("FHICL_FILE_PATH", self.prefix.job)
        env.prepend_path("FW_SEARCH_PATH", self.prefix.G4)
        env.prepend_path("FW_SEARCH_PATH", self.prefix.gdml)

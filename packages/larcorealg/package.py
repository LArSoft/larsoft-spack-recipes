# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.package import *
from spack.pkg.fnal_art.fnal_github_package import *
from spack.util.prefix import Prefix


class Larcorealg(CMakePackage, FnalGithubPackage):
    """Larcorealg"""

    repo = "LArSoft/larcorealg"
    version_patterns = ["v09_00_00", "09.13.00"]

    version("10.00.02", sha256="0ac325feca294c4fddd77a444aabdedd6f6351dd68632c5ec2b955aba21b6f1a")
    version("10.00.00", sha256="1c91112a634daaad55ddee5fdbf1a7eb1b0ffb4a9d0ababc90b47d51c57b9cc9")
    version("09.13.02", sha256="f386d879d10633123963577ef29a563777051ce2b5796a73d69789dff869af98")
    version("09.13.01", sha256="d339eba110757814c8522a92d421e2ae3aa6842d5088fd0440aa3eb177324e35")
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", default="17")

    depends_on("cetmodules", type="build")

    depends_on("boost+test")
    depends_on("canvas")
    depends_on("canvas-root-io")
    depends_on("clhep")
    depends_on("larcoreobj")
    depends_on("messagefacility")
    depends_on("root")

    @cmake_preset
    def cmake_args(self):
        return [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]

    @sanitize_paths
    def setup_build_environment(self, env):
        prefix = Prefix(self.build_directory)
        env.prepend_path("PATH", prefix.bin)  # Binaries
        env.prepend_path("FHICL_FILE_PATH", prefix.job)
        env.prepend_path("FW_SEARCH_PATH", prefix.gdml)

    @sanitize_paths
    def setup_run_environment(self, env):
        env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        env.prepend_path("FHICL_FILE_PATH", self.prefix.job)
        env.prepend_path("FW_SEARCH_PATH", self.prefix.gdml)

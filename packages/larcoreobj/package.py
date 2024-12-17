# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.package import *
from spack.pkg.fnal_art.fnal_github_package import *


class Larcoreobj(CMakePackage, FnalGithubPackage):
    """Larcoreobj"""

    repo = "LArSoft/larcoreobj"
    version_patterns = ["v09_00_00", "09.10.00"]

    version("10.00.00", sha256="a6e58cc8e136b05778e8a8bc9b4bdedd4b62a68871aece28a65154ddfcef01a9")
    version("09.10.02", sha256="77f84a9f7c29b8cbe17620962d97eb0835707b27241b944327b1cb0b18fbad78")
    version("09.10.01", sha256="484cf2d48b3012961f695abf67bd8f7ddf33467ad9a8086e410b299deab140d1")
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", default="17")

    depends_on("cetmodules", type="build")

    depends_on("boost+test")
    depends_on("canvas")
    depends_on("canvas-root-io")
    depends_on("fhicl-cpp")
    depends_on("root")

    @cmake_preset
    def cmake_args(self):
        return [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]

    def flag_handler(self, name, flags):
        if name == "cxxflags" and self.spec.compiler.name == "gcc":
            flags.append("-Wno-error=deprecated-declarations")
        return (flags, None, None)

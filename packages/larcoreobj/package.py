# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.fnal_art.fnal_github_package import *


class Larcoreobj(CMakePackage, FnalGithubPackage):
    """Larcoreobj"""

    repo = "LArSoft/larcoreobj"
    version_patterns = ["v09_00_00", "09.10.00"]

    version("09.10.01", sha256="08414d16d95286c0bc19fbafdbc5ac95646a27f5f4e6b461365742476c366c69")
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

# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.package import *
from spack.pkg.fnal_art.fnal_github_package import *


class Larvecutils(CMakePackage, FnalGithubPackage):
    """Larvecutils"""

    repo = "LArSoft/larvecutils"
    version_patterns = ["v09_00_00"]

    version("09.04.02", sha256="823c9496bced1f6e298cc7dfab2ca1c8d718e37e551f333329667bbc9632fcc6")
    version("09.04.01", sha256="7fea92e69149956355d5c124365a9fa54a783d30bc454f63377845cb1a945cd9")
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", default="17")

    depends_on("cetmodules", type="build")

    def cmake_args(self):
        return [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define("IGNORE_ABSOLUTE_TRANSITIVE_DEPENDENCIES", True),
        ]

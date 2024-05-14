# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Larfinder(CMakePackage):
    """Common cmake bits for larsoft"""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/LArSoft"
    url = "https://github.com/LArSoft/larfinder/archive/refs/tags/LARSOFT_SUITE_v09_79_00.tar.gz"

    maintainers = ["marcmengel"]

    version("09_79_00", sha256="af26656bca92225d0e741f6c96c50b382f5ab2170409272b107ff8e564a3b46c")

    depends_on("cetmodules", type="build")

    def cmake_args(self):
        args = []
        return args

# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Larfinder(CMakePackage):
    """Common cmake bits for larsoft"""

    homepage = "https://github.com/LArSoft"
    url = "https://github.com/LArSoft/larfinder/archive/refs/tags/LARSOFT_SUITE_v09_90_01.tar.gz"

    maintainers = ["marcmengel"]

    def url_for_version(self, version):
        html_prefix = "https://github.com/LArSoft/larfinder/archive/refs/tags"
        return f"{html_prefix}/LARSOFT_SUITE_v{version.underscored}.tar.gz"

    version("09.90.01", sha256="129d20e548eec79292dc43567aa200a65c2e48385f00000f3c54bd1e20152761")
    version("develop", branch="develop", get_full_repo=True)

    depends_on("cetmodules", type="build")

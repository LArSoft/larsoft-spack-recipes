# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.fnal_art.fnal_github_package import *


def _dependencies_for(cxxstd):
    for dep in ("gallery", "lardataalg", "lardataobj", "larvecutils"):
        depends_on(f"{dep} cxxstd={cxxstd}")


class Larsoftobj(BundlePackage, FnalGithubPackage):
    """Bundle package for art-independent LArSoft packages"""

    repo = "LArSoft/larsoftobj"
    version_patterns = ["v09_00_00", "09.35.00"]

    version("09.35.03")
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", default="17")

    depends_on("cetmodules", type="build")

    with when("cxxstd=17"):
        _dependencies_for("17")
    with when("cxxstd=20"):
        _dependencies_for("20")

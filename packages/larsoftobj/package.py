# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.package import *
from spack.pkg.fnal_art.fnal_github_package import *


def _dependencies_for(cxxstd):
    for dep in ("gallery", "lardataalg", "lardataobj", "larvecutils"):
        depends_on(f"{dep} cxxstd={cxxstd}")


class Larsoftobj(BundlePackage, FnalGithubPackage):
    """Bundle package for art-independent LArSoft packages"""

    repo = "LArSoft/larsoftobj"
    version_patterns = ["v09_00_00", "09.35.00"]

    version("10.00.03", sha256="de9ed8c99235b67fe091a392d15cd5e092a0aa6c62716b299553af3fd3ce5767")
    version("10.00.02", sha256="369104b92f8ddd0bcf813a9252a0c7fb5fb9b12648fd3e977020d338c0b0b254")
    version("10.00.00")
    version("09.36.00")
    version("09.35.03")
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", default="17")

    depends_on("cetmodules", type="build")

    with when("cxxstd=17"):
        _dependencies_for("17")
    with when("cxxstd=20"):
        _dependencies_for("20")

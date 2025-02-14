# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.fnal_art.fnal_github_package import *


def _dependencies_for(cxxstd):
    for dep in ("gallery", "lardataalg", "lardataobj", "larvecutils"):
        depends_on(f"{dep} cxxstd={cxxstd}")


class Larsoftobj(BundlePackage, FnalGithubPackage):
    """Deprecated bundle package for art-independent LArSoft packages"""

    repo = "LArSoft/larsoftobj"
    version_patterns = ["09.35.00"]

    with default_args(deprecated=True):
        # All versions are deprecated as larsoftobj is no longer necessary
        version("10.00.03")
        version("10.00.02")
        version("10.00.00")
        version("09.36.00")
        version("09.35.03")

    cxxstd_variant("17", "20", default="17")

    depends_on("cetmodules", type="build")

    with when("cxxstd=17"):
        _dependencies_for("17")
    with when("cxxstd=20"):
        _dependencies_for("20")

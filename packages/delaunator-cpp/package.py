# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class DelaunatorCpp(Package):
    """FIXME: Put a proper description of your package here."""

    url = "https://github.com/abellgithub/delaunator-cpp/archive/refs/tags/v0.4.0.tar.gz"

    version("1.0.0", sha256="27fdcbd92b3d0147a3952ee61fb34e86cfc3e87b7fb05afccca045582d0a83f4")
    version("0.4.0", sha256="8a885c5984dd586f6658276594d0a601ebe2612fe66e62fda2d19d855faddc0b")
    version("0.3.0", sha256="a796688322866502ed26a60f6bb59e2c602d13ac28d251ebb1f16902dba30471")
    version("0.2.0", sha256="e0a583c10a6a97db1153c1b37b79f05291c1b7c1d37e7d9063c161c21494b0e1")
    version("0.1.0", sha256="1a532388449ca4ff41c9ca4ebf3557b624ca4d99497c47be3d1565bee4246d13")


    def install(self, spec, prefix):
        mkdirp("{0}/include".format(prefix))
        install_tree(
            "{0}/include".format(self.stage.source_path),
            "{0}/include".format(prefix)
            )

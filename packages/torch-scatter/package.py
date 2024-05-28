# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install torch-scatter
#
# You can edit this file again by typing:
#
#     spack edit torch-scatter
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class TorchScatter(CMakePackage):

    homepage = "https://www.example.com"
    url = "https://github.com/rusty1s/pytorch_scatter/archive/refs/tags/2.1.2.tar.gz"

    version("2.1.2", sha256="6f375dbc9cfe03f330aa29ea553e9c7432e9b040d039b041f08bf05df1a8bf37")

    depends_on("py-torch")

    def cmake_args(self):
        args = []
        return args

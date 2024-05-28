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
#     spack install torch
#
# You can edit this file again by typing:
#
#     spack edit torch
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class Torch(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    url = "https://github.com/pytorch/pytorch/releases/download/v2.1.1/pytorch-v2.1.1.tar.gz"


#    version("2.3.0", sha256="69579513b26261bbab32e13b7efc99ad287fcf3103087f2d4fdf1adacd25316f")
#    version("2.2.2", sha256="57a1136095bdfe769acb87876dce77212da2c995c61957a67a1f16172d235d17")
#    version("2.2.1", sha256="8069467387b8ab7a7279671b9144d80a5c5342b4fa022eb3c1db629a6fd806c9")
#    version("2.2.0", sha256="e12d18c3dbb12d7ae2f61f5ab9a21023e3dd179d67ed87279ef96600b9ac08c5")
    version("2.1.2", sha256="85effbcce037bffa290aea775c9a4bad5f769cb229583450c40055501ee1acd7")
    version("2.1.1", sha256="1aa2aacced3c60c935d05f6d80232f8e99cdcb09eb51ceea697857b90c98d3fa")
    version("2.1.0", sha256="631c71f7f7d6174952f35b5ed4a45ec115720a4ef3eb619678de5893af54f403")
    version("2.0.1", sha256="9c564ca440265c69400ef5fdd48bf15e28af5aa4bed84c95efaad960a6699998")
    version("2.0.0", sha256="cecc38b6d4256b810336edfc6119d7a57b701fdf1ba43c50001f31e2724fd8e2")
    version("1.13.1", sha256="dbc229ee9750b02b514937d017744443a269ea0241ed3f32b9af0703589d25d4")

    depends_on("python")
    depends_on("py-bind11")
    depends_on("eigen3")
    depends_on("fftw")
    depends_on("mpfr")
    depends_on("gmp")

    def cmake_args(self):
        args = []
        return args

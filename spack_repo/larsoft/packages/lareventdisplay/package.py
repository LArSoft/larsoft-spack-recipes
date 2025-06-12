# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.package import *
from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.fnal_art.packages.fnal_github_package.package import FnalGithubPackage, cxxstd_variant


class Lareventdisplay(CMakePackage, FnalGithubPackage):
    """Lareventdisplay"""

    repo = "LArSoft/lareventdisplay"
    version_patterns = ["v09_00_00", "09.10.19"]

    version("10.00.15", sha256="e58f098e4f82daa0116a20be1f5d40d5b90ec38ff0c921664d7d5ab99d6aa1fe")
    version("10.00.14", sha256="56509d9f5fa720189d5c7619a2a4deb016d883804b0254850a441cb87210fed4")
    version("10.00.13", sha256="9058d99f79b11ff161edd28db8db62592fe75d004854547c9225da25f30c24cb")
    version("10.00.07", sha256="c8059f5c26c7858a78616ecaa8fa4460a921a70d5690f0d46b12f8edfb654054")
    version("10.00.06", sha256="8ab21409bd86e86a1d60856f59c384b46659d9fae92ccdbb7bd9e096819dd151")
    version("10.00.02", sha256="798b53cccc653f946082da1cb2cef5f645e2ada7318c1a21bd60c05f15b2e756")
    version("09.11.14", sha256="8b4f8dc4006014801795c9455718031c6de302150b49dbf08ec55fe6c801668a")
    version("09.11.05", sha256="ed021c8b5632e435026b5ebe4eb33dfceaed8764e2fa90d9735d764e93938253")
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", default="17")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("cetmodules", type="build")

    depends_on("art")
    depends_on("canvas")
    depends_on("canvas-root-io")
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("eigen")
    depends_on("fhicl-cpp")
    depends_on("larcorealg")
    depends_on("larcoreobj")
    depends_on("larcore")
    depends_on("lardataalg")
    depends_on("lardataobj")
    depends_on("lardata")
    depends_on("larevt")
    depends_on("larsim")
    depends_on("messagefacility")
    depends_on("nuevdb")
    depends_on("nusimdata")
    depends_on("root")

    with when("@:09.11.05.01"):
        depends_on("art-root-io")
        depends_on("zlib")

    @cmake_preset
    def cmake_args(self):
        return [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]

    @sanitize_paths
    def setup_run_environment(self, env):
        env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        env.prepend_path("FHICL_FILE_PATH", self.prefix.job)

    def flag_handler(self, name, flags):
        if name == "cxxflags" and self.spec.compiler.name == "gcc":
            flags.append("-Wno-error=deprecated-declarations")
            flags.append("-Wno-error=class-memaccess")
        return (flags, None, None)

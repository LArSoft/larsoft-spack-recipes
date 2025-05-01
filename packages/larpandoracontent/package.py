# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.package import *
from spack.pkg.fnal_art.fnal_github_package import *


class Larpandoracontent(CMakePackage, FnalGithubPackage):
    """Larpandoracontent"""

    repo = "LArSoft/larpandoracontent"
    version_patterns = ["v02_07_02", "04.07.01"]

    version("04.15.01", sha256="a0d89e0a163f600a0646e9db9a2b04363467d8e6a955eb5e894fc3f65285b5ca")
    version("04.15.00", sha256="144e40248e9826b093eebf0ebad990f1bb3e37f25e6a4678ace9c05f30a82d7e")
    version("04.14.01", sha256="4e9565801dc780c7da7ea09194c71ce31822211bd67fa58ff07eecf2789ea921")
    version("04.12.00", sha256="eb2490808f88fdb0934b7725b6baef8ca04bced5e27d6adc47e3b5497b6d9dbb")
    version("04.11.02", sha256="9188a37a011bc2984597621cf08e747495a08acc29856de7d135adad5e446223")
    version("04.10.00", sha256="6d09505f29835dd6f1c994491a67f4f04f06a5eb7724c9fe4f5364d2ff28ec32")
    version("04.08.01", sha256="9f46fc1183d0828f064a4ad1ab0cf6ef4b317d306920c83aa11f9a90bc45a48d")
    version("develop", branch="develop", get_full_repo=True)


    cxxstd_variant("17", "20", default="17")

    variant("monitoring", default=True, description="Enable PandoraMonitoring when building.")

    depends_on("cetmodules", type="build")

    depends_on("eigen")
    depends_on("pandora +monitoring", when="+monitoring")
    depends_on("pandora ~monitoring", when="~monitoring")
    depends_on("py-torch")

    def patch(self):
        filter_file(r"set\(PANDORA_MONITORING TRUE\)", "", "CMakeLists.txt")

        if not self.spec.variants["monitoring"].value:
            filter_file(
                r"(PandoraPFA::PandoraMonitoring|MONITORING)",
                "",
                "larpandoracontent/CMakeLists.txt",
            )

    @cmake_preset
    def cmake_args(self):
        return [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define("CMAKE_MODULE_PATH", f"{self.spec['pandora'].prefix}/cmakemodules"),
            self.define_from_variant("PANDORA_MONITORING", "monitoring"),
        ]

    @property
    def cmake_prefix_paths(self):
        return "{0}/lib/python{1}/site-packages/torch".format(
                    self.spec["py-torch"].prefix, self.spec["python"].version.up_to(2)
                )

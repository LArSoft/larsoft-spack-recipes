# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.fnal_art.fnal_github_package import *


class Larpandoracontent(CMakePackage, FnalGithubPackage):
    """Larpandoracontent"""

    repo = "LArSoft/larpandoracontent"
    version_patterns = ["v02_07_02", "04.07.01"]

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
    def cmake_prefix_paths(self)
        return "{0}/lib/python{1}/site-packages/torch".format(
                    self.spec["py-torch"].prefix, self.spec["python"].version.up_to(2)
                )

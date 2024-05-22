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

    version("develop", branch="develop", get_full_repo=True)
    version("04.08.01", sha256="6fecd809d9736a61f324a7bbb60baf0d6f36908470e233fc71b73ce455cc3f4f")

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
            self.define(
                "CMAKE_PREFIX_PATH",
                "{0}/lib/python{1}/site-packages/torch".format(
                    self.spec["py-torch"].prefix, self.spec["python"].version.up_to(2)
                ),
            ),
        ]

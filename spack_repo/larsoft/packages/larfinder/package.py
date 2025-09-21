# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *
from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.fnal_art.packages.fnal_github_package.package import *


class Larfinder(CMakePackage, FnalGithubPackage):
    """Common cmake bits for larsoft"""

    repo = "LArSoft/larfinder"
    git = "https://github.com/%s" % repo
    version_patterns = ["v09_00_01"]
    maintainers = ["marcmengel"]

    version("09.00.03", sha256="d6e8b9ee5ca183fe96dc773b0ba727cdc72937f7b26bfdda804a3d0165d6ab00")
    version("09.00.02", sha256="6eaf11a9625832a0e301d46354c06ac420eb4e3a88f26d5d9603eccd1238c380")
    version("09.00.01", sha256="5edbc7eb8a8aa17b4524b72cc1f8ab03691ea730511db0c6167731a9c2e1d659")
    version("develop", branch="develop", get_full_repo=True)

    depends_on("cetmodules", type="build")

    patch(self):
        filter_file("Modules/FindTensorFlow.cmake",
                "if (NOT TensorFlow_FOUND)",
                'if (NOT TensorFlow_FOUND)\ncmake_policy(CMP0159,"OLD")')

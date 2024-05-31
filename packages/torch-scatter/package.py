# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class TorchScatter(CMakePackage):
    """PyTorch Extension Library of Optimized Scatter Operations."""

    homepage = "https://github.com/rusty1s/pytorch_scatter"
    url = "https://github.com/rusty1s/pytorch_scatter/archive/refs/tags/2.1.2.tar.gz"
    git = "https://github.com/rusty1s/pytorch_scatter.git"

    license("MIT")
    maintainers("adamjstewart")

    version("2.1.2", sha256="6f375dbc9cfe03f330aa29ea553e9c7432e9b040d039b041f08bf05df1a8bf37")

    depends_on("python", type=("build", "link", "run"))
    depends_on("py-setuptools", type="build")

    # Undocumented dependencies
    depends_on("py-torch", type=("build", "link", "run"))

    # Historical dependencies
    depends_on("py-pytest-runner", type="build", when="@:2.0.7")

    def patch(self):
        filter_file(r'set\(CMAKE_CXX_STANDARD 14\)',
                'set(CMAKE_CXX_STANDARD 17)',
                'CMakeLists.txt')

    def setup_build_environment(self, env):
        if self.spec.satisfies("@2.0.6:"):
            if "+cuda" in self.spec["py-torch"]:
                env.set("FORCE_CUDA", 1)
                env.set("FORCE_ONLY_CUDA", 0)
                env.set("FORCE_ONLY_CPU", 0)
            else:
                env.set("FORCE_CUDA", 0)
                env.set("FORCE_ONLY_CUDA", 0)
                env.set("FORCE_ONLY_CPU", 1)
        else:
            if "+cuda" in self.spec["py-torch"]:
                env.set("FORCE_CUDA", 1)
                env.set("FORCE_CPU", 0)
            else:
                env.set("FORCE_CUDA", 0)
                env.set("FORCE_CPU", 1)

        env.prepend_path("CMAKE_PREFIX_PATH", "{0}".format(self.spec["py-torch"].package.cmake_prefix_paths[0]))


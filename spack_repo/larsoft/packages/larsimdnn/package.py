# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.package import *
from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.fnal_art.packages.fnal_github_package.package import *


class Larsimdnn(CMakePackage, FnalGithubPackage):
    """Larsim"""

    repo = "LArSoft/larsimdnn"
    git = "https://github.com/%s" % repo
    version_patterns = ["v09_00_00", "09.05.18"]

    version("10.00.19", sha256="d3e1651ffe8127a6a7584faa297497a54264d6acaae207728b607c194b1c6196")
    version("10.00.16", sha256="9634d85fcf0ec4e76cc542e80d4112007b294c648aa0b3863c1a6f5f17adedde")
    version("10.00.15", sha256="e630b4a30451d1816b21766fabb9f7d366bf8da0fb0dac8c20505866d27dea9f")
    version("10.00.11", sha256="1654f0995347543c00baef1325030d75c141cc08e86b5f9bd055e2150d860f74")
    version("10.00.10", sha256="65e3807dcca51ddbb7d159e44e342b6b7dac05e9bb0104f6edb127b157d4a1b4")
    version("10.00.09", sha256="4f7659b0fecf5ed66f0470d03c8daceb9655da16586681fbcf12fd973b7541c4")
    version("10.00.06", sha256="19e510362616e843eb73b5d8ebeeb8a962728522e65884f9481ccd8336be1c4a")
    version("10.00.05", sha256="ef4699262994a694ac843267119680dc1d3f06a3aed2f9cf36f93bbec9c102ff")
    version("10.00.02", sha256="6199d7c9d6edb7cfcaae3ea5612a2b76501cc4617ffc9f7385aae8516996fcc1")
    version("09.06.11", sha256="b220bbc3ee016ceb137a79a1445ec02a5ffc7ff4737e1c58b8b284c15d17a3b9")
    version("09.06.05", sha256="ecd14549917d696332bc05c3b4c23bdf263a99b5e76a3341b19142be5482bbad")
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", default="17")
    variant(
        "tensorflow",
        default=True,
        description="Include py-tensorflow",
    )

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("cetmodules", type="build")
    depends_on("larfinder", type="build")

    depends_on("eigen")
    depends_on("larcorealg")
    depends_on("larcoreobj")
    depends_on("larcore")
    depends_on("lardataobj")
    depends_on("larevt", when="@:09.06.05.01")
    depends_on("larsim")
    depends_on("py-tensorflow", when="+tensorflow")

    def patch(self):
        filter_file("find_package\(TensorFlow 2.6.0 QUIET EXPORT\)",
                'list(APPEND CMAKE_FIND_LIBRARY_SUFFIXES ".so.2")\nfind_package(TensorFlow 2.6.0 REQUIRED EXPORT)',
                "CMakeLists.txt"
                )

    @cmake_preset
    def cmake_args(self):
        return [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]

    @when("+tensorflow")
    def setup_build_environment(self, env):
        env.set("TENSORFLOW_DIR", self.spec["py-tensorflow"].prefix.lib)
        env.set(
            "TENSORFLOW_INC",
            join_path(
                self.spec["py-tensorflow"].prefix.lib,
                "python%s/site-packages/tensorflow/include" % self.spec["python"].version.up_to(2),
            ),
        )

    @sanitize_paths
    def setup_run_environment(self, env):
        env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        env.prepend_path("FHICL_FILE_PATH", self.prefix.job)
        env.prepend_path("FW_SEARCH_PATH", self.prefix.config_data)

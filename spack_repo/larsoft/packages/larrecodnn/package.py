# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.package import *
from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.fnal_art.packages.fnal_github_package.package import *


class Larrecodnn(CMakePackage, FnalGithubPackage):
    """Larrecodnn"""

    repo = "LArSoft/larrecodnn"
    git = "https://github.com/%s" % repo
    version_patterns = ["v09_00_00", "09.21.21"]

    version("10.01.23", sha256="5767df953821fb021a9a740d6aa347920fbd7c178c5163a9e2e17c95666dc88d")
    version("10.01.22", sha256="e27a4455c554414131168901b1e1bd1627acb1ba7dc8a6a2ae74aca6256c24e0")
    version("10.01.21", sha256="b00527da9bb6d1493f97ff5347029aa49b1e0d4f987bd812a8b303750f37feed")
    version("10.01.18", sha256="d713f6e34f69bd57a9a678e87330c919416ae0cc42fd4ba56eae2425eab205f0")
    version("10.01.15", sha256="75101a745eb655ad1f88ba0b5f112d12454911501b24f210a038b295368697e5")
    version("10.01.14", sha256="32d3e1fc865b22ce0c2c3a8e869c9fef51baf615a78b4e3461b5923395c80c90")
    version("10.01.10", sha256="86a54b2cdf067a5bcf4e494c2be1162d1e8aa6f58ea37a446962792bc962d334")
    version("10.01.09", sha256="5926ed8f470271c5e18bddfb0added760fb69eb651f549e2e46622c95506fc37")
    version("10.01.08", sha256="71f6f923bc20f66844f73dc8bee7cb0946b96c846c84af6ff1d630df1d47b660")
    version("10.01.02", sha256="85de7f26a0da870454f4d433e37629a250af3b35feba8b4c7f3da6aa9eab3ea5")
    version("10.01.01", sha256="683bd8bbf251f8f31774edc976331f585dfb7c0089a280ce00c531cc4ecb4eb5")
    version("10.00.03", sha256="8b6f1e617c5a7f4525f74b32a5f7551b84ab806ab00d7e9773954d57ec5b8228")
    version("09.23.09", sha256="27ebf2bfe36004632153dd6475bc982096499ae268502d5cb74fbb996fddeeed")
    version("09.23.00", sha256="cbf64222f14879cda5eaa2adb7ed8c07bef82afd86a3925b31cc1719fd17e236")
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

    depends_on("art")
    depends_on("art-root-io")
    depends_on("canvas")
    depends_on("cetlib")
    depends_on("cetlib-except")
    depends_on("clhep")
    depends_on("delaunator-cpp")
    depends_on("grpc")
    depends_on("hdf5")
    depends_on("hep-hpc")
    depends_on("larcore")
    depends_on("larcorealg")
    depends_on("larcoreobj")
    depends_on("lardataobj")
    depends_on("lardata")
    depends_on("larevt")
    depends_on("larreco")
    depends_on("larsim")
    depends_on("messagefacility")
    depends_on("nurandom")
    depends_on("nusimdata")
    depends_on("protobuf", when="@:09.23.00")
    depends_on("py-tensorflow", when="+tensorflow")
    depends_on("py-torch")
    depends_on("torch-scatter")
    depends_on("root")
    depends_on("tbb")
    depends_on("triton")
    depends_on("zlib")

    def patch(self):
        filter_file("LANGUAGES CXX", "LANGUAGES CXX C", "CMakeLists.txt")
        filter_file("find_package\(larfinder REQUIRED EXPORT\)",
            "find_package(Protobuf REQUIRED EXPORT)\nfind_package(larfinder REQUIRED EXPORT)",
            "CMakeLists.txt")
        filter_file("find_package\(TensorFlow 2.6.0 QUIET EXPORT\)",
                'list(APPEND CMAKE_FIND_LIBRARY_SUFFIXES ".so.2")\nfind_package(TensorFlow 2.6.0 REQUIRED EXPORT)',
                "CMakeLists.txt"
                )
        filter_file('#include "tensorflow/cc/saved_model/tag_constants.h"',
                    '#include "tensorflow/cc/saved_model/bundle_v2.h"\n#include "tensorflow/cc/saved_model/constants.h"\n#include "tensorflow/cc/saved_model/loader.h"',
                    "larrecodnn/ImagePatternAlgs/Tensorflow/TF/tf_graph.cc",
                    )
        filter_file("{tensorflow::kSavedModelTagServe},",
                    "{},",
                    "larrecodnn/ImagePatternAlgs/Tensorflow/TF/tf_graph.cc",
                    )


    @cmake_preset
    def cmake_args(self):
        args = [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define(
                "DELAUNATOR_INC",
                self.spec["delaunator-cpp"].prefix.include
            ),
        ]
        return args

    @property
    def cmake_prefix_paths(self):
        return [self.prefix,
                "{0}/lib/python{1}/site-packages/torch".format(
                self.spec["py-torch"].prefix, self.spec["python"].version.up_to(2))
                ]

    def setup_build_environment(self, env):
        env.set("TRITON_DIR", self.spec["triton"].prefix.lib)

    @when("+tensorflow")
    def setup_build_environment(self, env):
        env.set("TRITON_DIR", self.spec["triton"].prefix.lib)
        env.set("TENSORFLOW_DIR",
                join_path(
                    self.spec["py-tensorflow"].prefix.lib,
                    "python{0}/site-packages/tensorflow".format(
                    self.spec["python"].version.up_to(2)))
                )
        env.set("TENSORFLOW_INC",
                join_path(
                    self.spec["py-tensorflow"].prefix.lib,
                    "python{0}/site-packages/tensorflow/include".format(
                    self.spec["python"].version.up_to(2)))
                )

    @sanitize_paths
    def setup_run_environment(self, env):
        env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        env.prepend_path("FHICL_FILE_PATH", self.prefix.job)
        env.prepend_path("FW_SEARCH_PATH", self.prefix.config_data)

    def flag_handler(self, name, flags):
        if name == "cxxflags" and self.spec.compiler.name == "gcc":
            flags.append("-Wno-error=deprecated-declarations")
            flags.append("-Wno-error=class-memaccess")
            flags.append("-Wno-error=ignored-attributes")
        return (flags, None, None)

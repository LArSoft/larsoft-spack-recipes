# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from curses import version

from spack import *
from spack.package import *
from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.fnal_art.packages.fnal_github_package.package import *


class Larsimdnn(CMakePackage, FnalGithubPackage):
    """Larsim"""

    repo = "LArSoft/larsimdnn"
    git = "https://github.com/%s" % repo
    version_patterns = ["v09_00_00", "09.05.18"]

    version("10.02.10", sha256="58aa2099111f3d3246c784ff9fb3faee19cc7e9d7a0409936ea980254f8566ec")
    version("10.02.09", sha256="303576f1b0a2515c835133b97384a9daa646ac48c221f3d6572b08617122351c")
    version("10.02.08", sha256="cdde4e86a93739e224b1aa9618a61e20d94d8bf4ae659d0773ae8dd9a496e661")
    version("10.02.07", sha256="24f1bbaa0177584a8490870c1364dc0909e549a63540078823eb07c8a62d7f2c")
    version("10.02.06", sha256="884a5f4084fa75b7272b36703f8f7d0affba4b2b2258dba955e802943ece612c")
    version("10.02.05", sha256="ebe89f65449f0a7f96704f732a760277101141cea800d12b9171d554ff52706b")
    version("10.02.04", sha256="c132642b9441d5a804c17fa72dd931b07c38ffc3d299657006d75fbd1c475dd9")
    version("10.02.03", sha256="02577b78320dae90697f98468a7c0002e794783a2f5c0bbfe0e3e33bce3636f6")
    version("10.02.02.02", sha256="1abd751ad4bb29be88c8f15f49c611ec39e2c3c86daab3f1a61a71cabbd8b732")
    version("10.02.02.01", sha256="665f2199e2698adbdd7db0b529941ec399ecbfe6493268b5470564c3e8714b0a")
    version("10.02.02", sha256="de50b4a7426b88f609e1eee03a41840afa9df866557806762d67596148b86fb6")
    version("10.02.01", sha256="7b2fb0047f0ff30891a8d749c7256a2cce39797ef0aa5a46dc8603bf4b241465")
    version("10.02.00", sha256="885cd7305c53dec33ed7ae8a97367ac2fe93aefd28684aae5d6710c47a1f084d")
    version("10.01.03", sha256="26caefd7b77dd09df2e0bdfc3f4ab83576753350c919f1c0f64bbde038c4e129") 
    version("10.01.02", sha256="88003c94a524c28e323a34129f8b19e7252373e3d0d6bb2bff80c02fb7001d41")
    version("10.01.01", sha256="50a80d3a834105e9eb90767cca21236afaee9fa49e79329285f841112e94e592")
    version("10.01.00", sha256="de6d3dbc4b26f22916ccb56f4f3ca6394b784c1c9072edf18d0b1c1216caf87f")
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
    depends_on("grpc")
    depends_on("protobuf")

    def patch(self):
        filter_file('#include "tensorflow/cc/saved_model/tag_constants.h"',
                    '#include "tensorflow/cc/saved_model/bundle_v2.h"\n#include "tensorflow/cc/saved_model/constants.h"\n#include "tensorflow/cc/saved_model/loader.h"',
                    "larsimdnn/PhotonPropagation/TFLoaderTools/TFLoader.h",
                    )
        filter_file("{tensorflow::kSavedModelTagServe},",
                    "{},",
                    "larsimdnn/PhotonPropagation/TFLoaderTools/TFLoaderMLP_tool.cc",
                    )

    @cmake_preset
    def cmake_args(self):
        return [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]

    @when("+tensorflow")
    def setup_build_environment(self, env):
        env.set("TENSORFLOW_DIR",
                join_path(self.spec["py-tensorflow"].prefix.lib,
                "python%s/site-packages/tensorflow" % self.spec["python"].version.up_to(2),)
                + ";" +
                join_path(self.spec["py-tensorflow"].prefix.lib64,
                "python%s/site-packages/tensorflow" % self.spec["python"].version.up_to(2),)
        )
        env.set(
            "TENSORFLOW_INC",
            join_path(self.spec["py-tensorflow"].prefix.lib,
                "python%s/site-packages/tensorflow/include" % self.spec["python"].version.up_to(2),)
            + ";" +
            join_path(self.spec["py-tensorflow"].prefix.lib64,
                "python%s/site-packages/tensorflow/include" % self.spec["python"].version.up_to(2),)
        )

    @sanitize_paths
    def setup_run_environment(self, env):
        env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        env.prepend_path("FHICL_FILE_PATH", self.prefix.job)
        env.prepend_path("FW_SEARCH_PATH", self.prefix.config_data)

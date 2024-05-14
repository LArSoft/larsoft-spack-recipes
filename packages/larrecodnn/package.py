# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import spack.util.spack_json as sjson
from spack import *


def sanitize_environments(*args):
    for env in args:
        for var in (
            "PATH",
            "CET_PLUGIN_PATH",
            "LDSHARED",
            "LD_LIBRARY_PATH",
            "DYLD_LIBRARY_PATH",
            "LIBRARY_PATH",
            "CMAKE_PREFIX_PATH",
            "ROOT_INCLUDE_PATH",
        ):
            env.prune_duplicate_paths(var)
            env.deprioritize_system_paths(var)


class Larrecodnn(CMakePackage):
    """Larrecodnn"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larrecodnn"
    git = "https://github.com/LArSoft/larrecodnn.git"
    url = "https://github.com/LArSoft/larrecodnn/archive/v01_02_03.tar.gz"
    list_url = "https://api.github.com/repos/LArSoft/larrecodnn/tags"

    version("09.23.00", sha256="b6e202219627a82f219d4589a423b22b205c6a22d73bc4f0616b5b7d56492810")
    version("09.22.04", sha256="603381fff03b457ea11905528b68fb176f393962579398a99fa8ab51dd00cb31")
    version("09.21.12", sha256="ef1c843b2de317bf6a91aa75fd3737f7fb15f6294e81b44a8f88c94261abbf0e")
    version("09.21.09", sha256="5be674584e3cbb3835a75991786afa26603d8bece1d8e2131f8433274de14a50")
    version("09.21.06", sha256="c454cabc5ed191fadb16d9b9837297f653db2affb4d7cb89677a25d6e981cd61")
    version(
        "09.09.09.02", sha256="e820f2c50899979584456bfbfcab9abe27a022bd3ad50c9436167373bda9e9af"
    )
    version(
        "09.09.09.01", sha256="6fcb6e8dc331d3b0885f66b17f1147b852347b594f20435b9061bca0af8d7e65"
    )
    version("09.09.06", sha256="776c70ee0368c6d02d61382a5663494ac365eb8a595671a5efaff172aeb369da")
    version("09.09.03", sha256="c86c64e78c64fa2081f1299d0f09d3bcccafb944e34ec9c894f5e3568a8ef683")
    version("09.09.02", sha256="2de30ff1fbb6d3f67a366ff3a98a875c537d762442d64e6cef142f1d5a35e002")
    version("09.09.01", sha256="13aa9fc1725c64005ba303c30ca49d3f371c96060208db665b31e890d050ebfe")
    version("09.09.00", sha256="5df11800bf93d5a48855df6b9037a7ee7aefd3e19728b58b4bb040200cca7664")
    version("09.08.07", sha256="58e0d5d3fa8945e262e974246fecfdf77f9b98644da7f5ebf600c9099c21e491")
    version("09.08.06", sha256="5f71b2025b235eb0c5887c097714851fd4108eb129f037e32c80622220c425de")
    version("09.08.05", sha256="52330db26ddfd361776fc6a3b3350c3c9bffbf1f95bc180f66b666d7176997b1")
    version("09.08.04", sha256="d167889d60dd197ff1d725f6a3806409954eb43bf881203e7a9eccc58f45032a")
    version(
        "mwm1", tag="mwm1", git="https://github.com/marcmengel/larrecodnn.git", get_full_repo=True
    )
    version("develop", branch="develop", get_full_repo=True)

    def url_for_version(self, version):
        url = "https://github.com/LArSoft/{0}/archive/v{1}.tar.gz"
        return url.format(self.name, version.underscored)

    def fetch_remote_versions(self, concurrency=None):
        return dict(
            map(
                lambda v: (v.dotted, self.url_for_version(v)),
                [
                    Version(d["name"][1:])
                    for d in sjson.load(
                        spack.util.web.read_from_url(
                            self.list_url, accept_content_type="application/json"
                        )[2]
                    )
                    if d["name"].startswith("v") and not d["name"].endswith(")")
                ],
            )
        )

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    patch("v09_09_06.patch", when="@09.09.06")
    patch("v09_09_09_01.patch", when="@09.09.09.01")
    patch("v09_09_09_02.patch", when="@09.09.09.02")

    depends_on("cetmodules", type="build")
    depends_on("larfinder", type="build")
    depends_on("larcoreobj")
    depends_on("larcorealg")
    depends_on("larcore")
    depends_on("lardataobj")
    depends_on("lardataalg")
    depends_on("lardata")
    depends_on("larevt")
    depends_on("larsim")
    depends_on("larreco")
    depends_on("nutools")
    depends_on("nug4")
    depends_on("nurandom")
    depends_on("art")
    depends_on("art-root-io")
    depends_on("hep-hpc")
    depends_on("postgresql")
    depends_on("range-v3")
    depends_on("eigen")
    depends_on("root")
    depends_on("py-tensorflow")
    depends_on("triton")
    depends_on("protobuf")
    depends_on("tbb")
    depends_on("grpc")
    depends_on("re2")

    def cmake_args(self):
        args = ["-DCMAKE_CXX_STANDARD={0}".format(self.spec.variants["cxxstd"].value)]
        return args

    def setup_build_environment(self, spack_env):
        spack_env.set("TRITON_DIR", str(self.spec["triton"].prefix.lib))
        spack_env.set("TENSORFLOW_DIR", str(self.spec["py-tensorflow"].prefix.lib))
        spack_env.set("PROTOBUF_DIR", str(self.spec["protobuf"].prefix.lib))
        spack_env.set(
            "TENSORFLOW_INC",
            str(
                join_path(
                    self.spec["py-tensorflow"].prefix.lib,
                    "python%s/site-packages/tensorflow/include"
                    % self.spec["python"].version.up_to(2),
                )
            ),
        )
        # Binaries.
        spack_env.prepend_path("PATH", os.path.join(self.build_directory, "bin"))
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", os.path.join(self.build_directory, "lib"))
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(
            root=False, cover="nodes", order="post", deptype=("link"), direction="children"
        ):
            spack_env.prepend_path("ROOT_INCLUDE_PATH", str(self.spec[d.name].prefix.include))
        # Perl modules.
        spack_env.prepend_path("PERL5LIB", os.path.join(self.build_directory, "perllib"))
        # Set path to find fhicl files
        spack_env.prepend_path("FHICL_INCLUDE_PATH", os.path.join(self.build_directory, "fcl"))
        # Set path to find gdml files
        spack_env.prepend_path("FW_SEARCH_PATH", os.path.join(self.build_directory, "fcl"))
        # Cleaup.
        sanitize_environments(spack_env)

    def setup_run_environment(self, run_env):
        # Ensure we can find plugin libraries.
        run_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(
            root=False,
            cover="nodes",
            order="post",
            deptype=("link"),
            direction="children",
        ):
            run_env.prepend_path("ROOT_INCLUDE_PATH", str(self.spec[d.name].prefix.include))
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        # Set path to find fhicl files
        run_env.prepend_path("FHICL_FILE_PATH", os.path.join(self.prefix, "fcl"))
        # Cleaup.
        sanitize_environments(run_env)

    def setup_dependent_build_environment(self, spack_env, dspec):
        spack_env.set("LARRECODNN_INC", self.prefix.include)
        spack_env.set("LARRECODNN_LIB", self.prefix.lib)
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        spack_env.prepend_path("PATH", self.prefix.bin)
        spack_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        spack_env.append_path("FHICL_FILE_PATH", "{0}/fcl".format(self.prefix))
        spack_env.append_path("FW_SEARCH_PATH", "{0}/gdml".format(self.prefix))
        sanitize_environments(spack_env)

    def flag_handler(self, name, flags):
        if name == "cxxflags" and self.spec.compiler.name == "gcc":
            flags.append("-Wno-error=deprecated-declarations")
            flags.append("-Wno-error=class-memaccess")
            flags.append("-Wno-error=ignored-attributes")
        return (flags, None, None)

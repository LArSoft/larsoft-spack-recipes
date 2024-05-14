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


class Larsimdnn(CMakePackage):
    """Larsim"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larsim"
    git = "https://github.com/LArSoft/larsimdnn.git"
    url = "https://github.com/LArSoft/larsimdnn/archive/v01_02_03.tar.gz"
    list_url = "https://api.github.com/repos/LArSoft/larsimdnn/tags"

    version("09.06.05", sha256="48009e7f9f89f8035b27d4cd585c5bb16ab443cde3588d1e14098a1e71bec63d")
    version("09.05.10", sha256="245b7a56cb1cefca75be0ca84ee993a6a6390623223bd2b76e155ae0347be6e8")
    version(
        "mwm1", tag="mwm1", git="https://github.com/marcmengel/larsimdnn.git", get_full_repo=True
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

    depends_on("larsoft-data")
    depends_on("larevt")
    depends_on("marley")
    depends_on("genie")
    depends_on("ifdhc")
    depends_on("xerces-c")
    depends_on("libxml2")
    depends_on("clhep")
    depends_on("nug4")
    depends_on("nugen")
    depends_on("nurandom")
    depends_on("artg4tk")
    depends_on("larsim")
    depends_on("ppfx")
    depends_on("cetmodules", type="build")
    depends_on("larfinder", type="build")
    depends_on("nufinder", type="build")

    def cmake_args(self):
        args = [
            "-DCMAKE_CXX_STANDARD={0}".format(self.spec.variants["cxxstd"].value),
            "-DIFDH_INC={0}".format(self.spec["ifdhc"].prefix.include),
            "-DIFDH_LIB={0}".format(self.spec["ifdhc"].prefix),
            "-DGENIE_INC={0}".format(self.spec["genie"].prefix.include),
            "-DGENIE_VERSION=v{0}".format(self.spec["genie"].version.underscored),
            "-DLARSOFT_DATA_DIR=v{0}".format(self.spec["larsoft-data"].prefix),
            "-DLARSOFT_DATA_VERSION=v{0}".format(self.spec["larsoft-data"].version.underscored),
        ]
        return args

    def setup_build_environment(self, spack_env):
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
        # Cleaup.
        sanitize_environments(spack_env)

    def setup_run_environment(self, run_env):
        # Ensure we can find plugin libraries.
        run_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(
            root=False, cover="nodes", order="post", deptype=("link"), direction="children"
        ):
            run_env.prepend_path("ROOT_INCLUDE_PATH", str(self.spec[d.name].prefix.include))
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        # Perl modules.
        run_env.prepend_path("PERL5LIB", os.path.join(self.prefix, "perllib"))
        # Cleaup.
        sanitize_environments(run_env)

    def setup_dependent_build_environment(self, spack_env, dspec):
        spack_env.set("LARANA_INC", self.prefix.include)
        spack_env.set("LARANA_LIB", self.prefix.lib)
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        spack_env.prepend_path("PATH", self.prefix.bin)
        spack_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        spack_env.append_path("FHICL_FILE_PATH", "{0}/fcl".format(self.prefix))
        spack_env.append_path("FW_SEARCH_PATH", "{0}/gdml".format(self.prefix))

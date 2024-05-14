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


class Larcore(CMakePackage):
    """Larcore"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larcore"
    git = "https://github.com/LArSoft/larcore.git"
    url = "https://github.com/LArSoft/larcore/archive/v01_02_03.tar.gz"
    list_url = "https://api.github.com/repos/LArSoft/larcore/tags"

    version("09.11.01", sha256="2cc3cc0e90f5f4c49d3d3f8cf29d26b21686b34d88d31a9f553df5cff5d4e118")

    version("09.10.01", sha256="748ce3a30f81f2dc789be8d276fb0831c951eeef514ff4cae6e2d6ff291fb9fb")
    version("09.10.00", sha256="0686862a2cce84f54166934e83345cb5e3b23fe659e435c99ca5e368d6ad46b6")
    version("09.03.02", sha256="16f60e05edd620b6a41928f591fe062db2e9d91cf7948fa4f30d688bd547bcbb")
    version("09.03.01", sha256="bab2aa40e0d796c4f11433ea1096e0b44b1b4d1b09b1c531495ad2b19caf879f")
    version("09.03.00", sha256="d9f54979c57c94cee142e6b477a5df44a65baf4a132d48cc455f49540bf3d72b")
    version("09.02.04.01", sha256="efd3ae5d4ea699a383ab481d1efa496f19fbb57e1edf422ad773aa6eb1766876")
    version("09.02.04", sha256="b3408c26313679a872b2a875d92510b1a4a4a108ce5795b81185edf1d6c4a813")
    version("09.02.03", sha256="27fa2435c66e1e4b5dfcf0d4a0c1c3aa34623a2a50f36bd47fcf8102b17c6198")
    version("09.02.02.04", sha256="c6ea5c49f757252d8739f081638997a7815081860bcd97f7691cd852a00f0082")
    version("09.02.02.03", sha256="30ecf738c12380a9629024b84af3cd9110749f0ddd37ae3cd0834c31b42f0e18")
    version("09.02.02.02", sha256="5fa4a0040139f7e06a1219919a876dd4cc56970b01c6d8e8cd32b1119b899f93")
    version("mwm1", tag="mwm1", git="https://github.com/marcmengel/larcore.git")
    version("develop", branch="develop", get_full_repo=True)

    def url_for_version(self, version):
        url = "https://github.com/LArSoft/{0}/archive/refs/tags/v{1}.tar.gz"
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

    patch("v09_03_01.patch", when="@09.03.01")
    patch("v09_03_02.patch", when="@09.03.02")

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("messagefacility")
    depends_on("larcorealg")
    depends_on("art-root-io")
    depends_on("cetmodules", type="build")
    depends_on("cetbuildtools", type="build" , when="@:09.05.00")

    def cmake_args(self):
        args = [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]
        return args

    @run_after("cmake")
    def fix_static_boost(self):
        print("fixing filesystem.a references..")
        os.system(
            "set -x; find %s/test/Geometry/CMakeFiles %s/larcore/Geometry/CMakeFiles "
            "-type f -print  | tee /tmp/fixlist | "
            "xargs perl -pi -e 's/libboost_filesystem.a/libboost_filesystem.so/go;'"
            % (self.build_directory, self.build_directory)
        )
        print("done fixing filesystem.a references..")

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
            root=False, cover="nodes", order="post", deptype=("link"), direction="children"
        ):
            run_env.prepend_path("ROOT_INCLUDE_PATH", str(self.spec[d.name].prefix.include))
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        # Perl modules.
        run_env.prepend_path("PERL5LIB", os.path.join(self.prefix, "perllib"))
        # Set path to find fhicl files
        run_env.prepend_path("FHICL_INCLUDE_PATH", os.path.join(self.prefix, "fcl"))
        # Set path to find gdml files
        run_env.prepend_path("FW_SEARCH_PATH", os.path.join(self.prefix, "fcl"))
        # Cleaup.
        sanitize_environments(run_env)

    def setup_dependent_build_environment(self, spack_env, dspec):
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        spack_env.prepend_path("PATH", self.prefix.bin)
        spack_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        spack_env.append_path("FHICL_FILE_PATH", "{0}/fcl".format(self.prefix))
        spack_env.append_path("FW_SEARCH_PATH", "{0}/gdml".format(self.prefix))

    def flag_handler(self, name, flags):
        if name == "cxxflags" and self.spec.compiler.name == "gcc":
            flags.append("-Wno-error=deprecated-declarations")
            flags.append("-Wno-error=class-memaccess")
        return (flags, None, None)

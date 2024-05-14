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


class Larevt(CMakePackage):
    """Larevt"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larevt"
    git = "https://github.com/LArSoft/larevt.git"
    url = "https://github.com/LArSoft/larevt/archive/v01_02_03.tar.gz"
    list_url = "https://api.github.com/repos/LArSoft/larevt/tags"

    version("09.10.03", sha256="2ae46ffb4d5cf79fe4b1f75a3c97f31a93e3e9734815cfa1e4f1a830227075b6")
    version("09.10.02", sha256="321b5757c06d8eecaba2aea9c129ffeea8b8462bc82628e4464902e61cb841a4")
    version("09.09.07", sha256="e579056bcb7cdfc8ec44cc73fdbd2ef5ab4d30442733b03e97482637687dbc29")
    version("09.09.04", sha256="5c12e59d01b29f93e09fb31b70956792dbc0cc1b956f90ec7687415f30298276")
    version("09.09.01", sha256="a2e44a299d9a962241f1bdb9c77dccd46ef852f005e149a8300bdb56e7030496")
    version("09.03.05", sha256="fc3084ff2441a8358c549a0f23fae39c7b37f977ef29c0c573b2a8aeb9a07cf8")
    version("09.03.03", sha256="7ce85f65911034c354517800dd041e7a00afe7b1838168911fea5809199f5dc1")
    version("09.03.02", sha256="9c6980a93b3f2ca0bc432d885ee8eb7cd2c8c7c1a47e1e503c8fdf7891493a3c")
    version("09.03.01", sha256="5d0c3cc34eaa49e18c0c0359ac22d481bdad1d50df5787a778928d1de38fb098")
    version("09.03.00", sha256="17c0dcb65f76f24f442c4cc887746a20e07c3b118ff7d95cb5271b1f0d8e12e2")
    version("09.02.12", sha256="7dc8b575b6b54904def93d691bbe3f512a260376956ea68e3131bf8d4ca46cef")
    version("09.02.11", sha256="e2a805dcdc93d3db14101de7013eba79883aefa984c46e76bfcfdda209f2264d")
    version(
        "09.02.10.01", sha256="ff987151307ea375bffbc3f18a69b05fdf168b26b0272c0777ed13e0a67f52a2"
    )
    version("09.02.10", sha256="5afa7063640f2722d22cb9140f2b335043d5bb6d5ecf6e1fd3559b9d2c206b57")
    version("09.02.09", sha256="5f71d0182038e9cc096977047abf411819b0c47d5f4110fb66a2856d47ee7489")
    version("mwm1", tag="mwm1", git="https://github.com/marcmengel/larevt.git", get_full_repo=True)
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

    patch("v09_03_03.patch", when="@09.03.03")
    patch("v09_03_05.patch", when="@09.03.05")

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("libwda")
    depends_on("lardata")
    depends_on("sqlite")
    depends_on("cetmodules", type="build")

    def cmake_args(self):
        args = [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define("IGNORE_ABSOLUTE_TRANSITIVE_DEPENDENCIES", True),
        ]
        return args

    def setup_build_environment(self, spack_env):
        # Binaries.
        spack_env.prepend_path("PATH", os.path.join(self.build_directory, "bin"))
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", os.path.join(self.build_directory, "lib"))
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(
            root=False,
            cover="nodes",
            order="post",
            deptype=("link"),
            direction="children",
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
        # Perl modules.
        run_env.prepend_path("PERL5LIB", os.path.join(self.prefix, "perllib"))
        # Set path to find fhicl files
        run_env.prepend_path("FHICL_FILE_PATH", os.path.join(self.prefix, "fcl"))
        # Cleaup.
        sanitize_environments(run_env)

    def setup_dependent_build_environment(self, spack_env, dspec):
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        spack_env.prepend_path("PATH", self.prefix.bin)
        spack_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        spack_env.append_path("FHICL_FILE_PATH", "{0}/fcl".format(self.prefix))
        spack_env.append_path("FW_SEARCH_PATH", "{0}/gdml".format(self.prefix))

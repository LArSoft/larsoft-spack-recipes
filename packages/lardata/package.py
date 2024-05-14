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


class Lardata(CMakePackage):
    """Lardata"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/lardata"
    git = "https://github.com/LArSoft/lardata.git"
    url = "https://github.com/LArSoft/lardata/archive/v01_02_03.tar.gz"
    list_url = "https://api.github.com/repos/LArSoft/lardata/tags"

    version("09.16.03", sha256="e73f75875a8e769ccc684d4adc670d5d74e4d936657b9dc9a9f3aa3631b0682e")
    version("09.16.02", sha256="e544952c9c7ef6b225a4d91654e9d57fe83d2feccca31d5c5b6f34eeee8ee4c0")
    version("09.15.07", sha256="378cf1df2b1192d2a9e704cc5605b136660ec2d22c83afa91baeb80e964b6929")
    version("09.15.04", sha256="1d480660bbd2fe4afcd7e55427531bd11d69a61d3e3814d6965e67df13e47c08")
    version(
        "09.04.vec02",
        branch="larvecutils-v09_37_01_01",
        git="https://github.com/cerati/lardata.git",
    )
    version("09.15.01", sha256="c88fac18495aff9e245c18e288a121ed1b0fc4e78148e4483a4e8d3b0ec80ba1")
    version("09.04.02", sha256="ebca1134427b493d7f1a4a278441b59802bd05662ec995dee2ad91e489c8b454")
    version("09.04.00", sha256="a2495f4427245d6901138439750cf746a7a4bdc3633fbcb9e7c5cdffdb1e4af6")
    version("09.03.02", sha256="7e48e6caaaf6a49cf9e2b575b0fb253db7ecba9034f9c9b940758df99f25eda6")
    version("09.03.01", sha256="fb2e4779b6b70816d7c78545694e47d45aaa0eebe50d187df6fe56479d539513")
    version("09.03.00", sha256="a5edd13b0e7ec921fd343c8ce0655551511174f76c2716ff28c41448ed35c82d")
    version("09.02.10", sha256="618ddb47626f539bb19ea2b1f5ce2e4a49ab99e2570c7303348f47fa401ee021")
    version("09.02.09", sha256="fb86a4b49a7c3528930ebc8d8032fe2c902d152a56834b3a11a08c9edad4705c")
    version(
        "09.02.08.01", sha256="ef3984d58e3a33b5de291c831ba545b0d5fec664c907bb0047dce4a4aaf3952e"
    )
    version("09.02.08", sha256="cf22bba23224770b989a880f17414bcb1f2c00128f2bc6bccf6e4838e187b9c9")
    version("09.02.07", sha256="5f42749bf958f1d30201ea9a2a078fb6a77977cfc023c4eb0302da81a6a3daf9")
    version(
        "mwm1", tag="mwm1", git="https://github.com/marcmengel/lardata.git", get_full_repo=True
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

    patch("v09_04_00.patch", when="@09.04.00")
    patch("v09_04_02_larvecutils.patch", when="@09.04.vec02")
    patch("v09_04_02.patch", when="@09.04.02")

    depends_on("boost +date_time+serialization")
    depends_on("nutools")
    depends_on("nusimdata")
    depends_on("larcore")
    depends_on("lardataobj")
    depends_on("lardataalg")
    depends_on("larvecutils", when="@09.04.vec02")
    depends_on("larvecutils", when="@09.10:")  # not quite sure when the dependency came in...
    depends_on("range-v3")
    depends_on("root+fftw")
    depends_on("fftw")
    depends_on("cetmodules", type="build")

    def cmake_args(self):
        args = [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define("IGNORE_ABSOLUTE_TRANSITIVE_DEPENDENCIES", True),
        ]
        return args

    def flag_handler(self, name, flags):
        if name == "cxxflags" and self.spec.compiler.name == "gcc":
            flags.append("-Wno-error=deprecated-declarations")
            flags.append("-Wno-error=class-memaccess")
        return (flags, None, None)

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
        spack_env.prepend_path("FHICL_FILE_PATH", os.path.join(self.build_directory, "fcl"))
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
        run_env.prepend_path("FHICL_FILE_PATH", os.path.join(self.prefix, "fcl"))
        # Set path to find gdml files
        run_env.prepend_path("FW_SEARCH_PATH", os.path.join(self.prefix, "gdml"))
        # Cleaup.
        sanitize_environments(run_env)

    def setup_dependent_build_environment(self, spack_env, dspec):
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        spack_env.prepend_path("PATH", self.prefix.bin)
        spack_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        spack_env.append_path("FHICL_FILE_PATH", "{0}/fcl".format(self.prefix))
        spack_env.append_path("FW_SEARCH_PATH", "{0}/gdml".format(self.prefix))

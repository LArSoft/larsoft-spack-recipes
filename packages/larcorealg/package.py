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


class Larcorealg(CMakePackage):
    """Larcorealg"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larcorealg"
    git = "https://github.com/LArSoft/larcorealg.git"
    url = "https://github.com/LArSoft/larcorealg/archive/v01_02_03.tar.gz"
    list_url = "https://api.github.com/repos/LArSoft/larcorealg/tags"

    version("09.13.01", sha256="0a6220bb65093eec610de8c666fb0a3a302a8a25aabac65cf8cf2b4181b3ef8b")
    version("09.12.01", sha256="d85881b207008f6efb980899789757a30acbf4236965ce1a6fe941c7806f82e0")
    version("09.12.00", sha256="026ceeb0d0b776baac13184c8e1310edaa4e99cdc53bdbe37c0011f5b8d07496")
    version("09.04.00", sha256="7da808226873972bf97ca9bb3413e2fcbb1d6cf5765f218a4c04a94c236e8462")
    version("09.03.01", sha256="7280de6bc7949d6c2db1315b8700e518cff11f1527758996b22cb22f6ea7f7fb")
    version("09.03.00", sha256="343e1b833561912e743c867ccc7699c6fdd2c56d6da78cc5368291662f533d86")
    version(
        "09.02.01.01", sha256="e17829922747b30a989f97dad123330f34a9b28322159632401144d5591a0044"
    )
    version("09.02.01", sha256="1644c62a87442fb9fde3b6d5528348992d05024f5a6a615a678a85b923b23581")
    version("09.02.00", sha256="73e369e48aaa56a2b4ab1582fa9f900a23db486031d75477bc6d0fecf8bbefef")
    version(
        "09.01.02.03", sha256="843673c9a9be9520d35c9d640ed390dd6fe6ef34761d04aa6517443550c5c1db"
    )
    version(
        "09.01.02.02", sha256="f880856eddf4d629af4c4a3009a1ad832d29933beba9f7c093b9a51cd4134c0c"
    )
    version("mwm1", tag="mwm1", git="https://github.com/marcmengel/larcorealg.git")
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

    patch("v09_03_01.patch", when="@09.03.01")
    patch("v09_04_00.patch", when="@09.04.00")

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("larcoreobj")
    depends_on("cetmodules", type="build")

    def cmake_args(self):
        args = [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]
        return args

    def setup_build_environment(self, spack_env):
        spack_env.set("CETBUILDTOOLS_VERSION", self.spec["cetmodules"].version)
        spack_env.set("CETBUILDTOOLS_DIR", self.spec["cetmodules"].prefix)
        spack_env.prepend_path("LD_LIBRARY_PATH", self.spec["root"].prefix.lib)
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
        run_env.prepend_path("PATH", self.prefix.bin)
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
        run_env.prepend_path("FHICL_INCLUDE_PATH", os.path.join(self.prefix, "fcl"))
        # Set path to find gdml files
        run_env.prepend_path("FW_SEARCH_PATH", os.path.join(self.prefix, "fcl"))
        # Cleaup.
        sanitize_environments(run_env)

    def setup_dependent_build_environment(self, spack_env, dspec):
        spack_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        spack_env.prepend_path("PATH", self.prefix.bin)
        spack_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        spack_env.append_path("FHICL_FILE_PATH", "{0}/fcl".format(self.prefix))
        spack_env.append_path("FW_SEARCH_PATH", "{0}/gdml".format(self.prefix))

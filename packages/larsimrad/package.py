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


class Larsimrad(CMakePackage):
    """larsimrad"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larsimrad"
    git = "https://github.com/LArSoft/larsimrad.git"
    url = "https://github.com/LArSoft/larsimrad/archive/refs/tags/v09_01_17.tar.gz"
    list_url = "https://api.github.com/repos/LArSoft/larsimrad/tags"

    version("09.09.05", sha256="7c95a3dbc12a1cfa0f817834ae1813190da44b80ec49ef131782eb5e8fe77904")
    version("09.09.04", sha256="7640118b093b8ba74026dd3fe2db4b9d476e12416af81dadadf9439cf6d8dfe2")
    version("09.08.10", sha256="48be617a621fc1f6ff93a09ce1f8f75199fbc15db103d3aa6627818f59d71b34")
    version("09.08.07", sha256="95a4056e7617911f225581206bc4315044902bd9f679bc40fe61c80c7dafd8f6")
    version("09.08.04", sha256="b20cfda1210fb2b33c6e206f8c0da4a352a4f4bd35a0b8d76e5f19759a7e414a")
    version(
        "09.03.07.02", sha256="c3969b6b7c8c4087d7b539a1778d1ab3456920df131d652b4441d5a83a557b3b"
    )
    version(
        "09.03.07.01", sha256="5d7fbff1dac128e44a4b8cd88d9099a2bb5c54b50e951b5aff9ddbe294af3024"
    )
    version("09.03.04", sha256="74c8041fbef672eeb95941b5c785c087f1af3e834947a6ec63208302e850b712")
    version(
        "09.01.09.01", sha256="5881b66ed27237560bbc8f4a422e6c9146fcb717fa84aaea07cc17f7fbf1a0b5"
    )
    version("09.01.09", sha256="15bd7dbae42c7e7d2600202057433903c05b77b6fe046a618b1645a2ff6a7920")
    version("09.01.08", sha256="d23cb4fcff66deb82776d186298fd7201580e4a49eb7106a4c66096aeccc153b")
    version("09.01.07", sha256="1278f313ff6a9dc640cbe1b73984d178925e93ab1f55ce3826f2f5da216c60ae")
    version("09.01.06", sha256="d16504046706bc30927bc7281c1e2c5c5b4760bc476fc86c5e932c5a7bf20285")
    version("09.01.05", sha256="b6ac122533958d6412ebf200e14c2ff6d76a02859fb0f2751aa6da45832deefb")
    version("09.01.04", sha256="5367e74c6d76fb4149083fc54238d12a0c0632b532499b004e6840619e575a0f")
    version("09.01.03", sha256="7536f5e4f49c2ec3b82bfe2cb89a76a707cce00f9e09e82ca6bcc6d7157e7516")
    version("09.01.02", sha256="7c47e4483f24b2c857b8597f93516da62bd20c3150f941892c69dda2a3e4ef1e")
    version(
        "mwm1", tag="mwm1", git="https://github.com/marcmengel/larsimrad.git", get_full_repo=True
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

    patch("v09_03_04.patch", when="@09.03.04")
    # patch('v09_03_07_01.patch', when='@09.03.07.01')
    patch("v09_03_07_02.patch", when="@09.03.07.02")

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("cetmodules", type="build")
    depends_on("art-root-io")
    depends_on("bxdecay0")
    depends_on("lardata")
    depends_on("nugen")
    depends_on("larsim")
    depends_on("nusimdata")

    def cmake_args(self):
        args = [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]
        return args

    def setup_build_environment(self, spack_env):
        # Binaries.
        spack_env.prepend_path("PATH", os.path.join(self.build_directory, "bin"))
        spack_env.prepend_path("PYTHONPATH", os.path.join(self.build_directory, "bin"))
        spack_env.prepend_path("PYTHONPATH", os.path.join(self.build_directory, "python"))
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", os.path.join(self.build_directory, "lib"))
        # Ensure Root can find headers for autoparsing.
        for d in self.spec.traverse(
            root=False, cover="nodes", order="post", deptype=("link"), direction="children"
        ):
            spack_env.prepend_path("ROOT_INCLUDE_PATH", str(self.spec[d.name].prefix.include))
        # Perl modules.
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
        sanitize_environments(run_env)

    def setup_dependent_build_environment(self, spack_env, dspec):
        spack_env.set("LARSIMRAD_INC", self.prefix.include)
        spack_env.set("LARSIMRAD_LIB", self.prefix.lib)
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        spack_env.prepend_path("PATH", self.prefix.bin)
        spack_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        spack_env.append_path("FHICL_FILE_PATH", "{0}/fcl".format(self.prefix))
        spack_env.append_path("FW_SEARCH_PATH", "{0}/gdml".format(self.prefix))

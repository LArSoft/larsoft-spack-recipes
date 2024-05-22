# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.fnal_art.fnal_github_package import *


class Larsimdnn(CMakePackage, FnalGithubPackage):
    """Larsim"""

    repo = "LArSoft/larsimdnn"
    version_patterns = ["v09_00_00", "09.05.18"]

    version(
        "09.06.05.01", sha256="f7bc0d169a5c37c91e1c167006b475abb08fd1c75ccf6afffa0982ec8aade8a2"
    )
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", default="17")

    depends_on("cetmodules", type="build")
    depends_on("larfinder", type="build")

    depends_on("eigen")
    depends_on("larcorealg")
    depends_on("larcoreobj")
    depends_on("larcore")
    depends_on("lardataobj")
    depends_on("larevt", when="@:09.06.05.01")
    depends_on("larsim")
    depends_on("py-tensorflow")

    @cmake_preset
    def cmake_args(self):
        return [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]

    @sanitize_paths
    def setup_build_environment(self, env):
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

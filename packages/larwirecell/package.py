# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.package import *
from spack.pkg.fnal_art.fnal_github_package import *


class Larwirecell(CMakePackage, FnalGithubPackage):
    """Larwirecell"""

    repo = "LArSoft/larwirecell"
    version_patterns = ["v09_00_00", "09.18.00"]

    version("10.00.02", sha256="e7b25de4ae4d7e3c1728d81b15d2c1b2d8bdde515576580c20c9954c38c6f014")
    version("09.18.08", sha256="abcbc8df882045a0bb1f851a279c32c8efb9f4f6c2d5901a89c17fdc0b9ca230")
    version("09.18.04", sha256="f932e70776681fb75ca39e9e2cc709321ca5689a3bbfc229c1b67921c6e585b9")
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", default="17")

    patch('v10.00.02.patch', when="@10.00.02")
    
    depends_on("cetmodules", type="build")

    depends_on("art")
    depends_on("larcorealg")
    depends_on("larcoreobj")
    depends_on("larcore")
    depends_on("lardataalg", when="@:09.18.04")
    depends_on("lardata")
    depends_on("larevt")
    depends_on("root")
    depends_on("wirecell")

    # Dependencies for FindWireCell.cmake module
    depends_on("boost")
    depends_on("eigen")
    depends_on("jsoncpp")
    depends_on("jsonnet")
    depends_on("spdlog")
    depends_on("tbb")

    def patch(self):
        filter_file(r"list\(TRANSFORM _fwc_deps APPEND _FOUND", "", "Modules/FindWireCell.cmake")
        filter_file(
            r"OUTPUT_VARIABLE _fwc_fphsa_extra_required_vars\)",
            'set(_fwc_fphsa_extra_required_vars "")',
            "Modules/FindWireCell.cmake",
        )
        filter_file(r"Boost::stacktrace_basic", "", "Modules/FindWireCell.cmake")
        filter_file(
            r" set\(_fwc_fphsa_extra_args",
            ' STRING(REPLACE ";" " " _fwc_missing_deps_str "missing dependencies: ${_fwc_missing_deps}")\n    set(_fwc_fphsa_extra_args',
            "Modules/FindWireCell.cmake",
        )
        filter_file(
            r'REASON_FAILURE_MESSAGE "missing dependencies: \$\{_fwc_missing_deps\}"',
            'REASON_FAILURE_MESSAGE "missing dependencies: ${_fwc_missing_deps_str}"',
            "Modules/FindWireCell.cmake",
        )
        filter_file(
            r"find_package\(art ",
            "find_package(Boost COMPONENTS graph date_time exception filesystem iostreams stacktrace_basic)\nfind_package(art ",
            "CMakeLists.txt",
        )
        filter_file(
            r"jsoncpp_lib jsonnet_lib",
            "jsoncpp jsonnet",
            "Modules/FindWireCell.cmake",
        )

    @cmake_preset
    def cmake_args(self):
        return [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define("IGNORE_ABSOLUTE_TRANSITIVE_DEPENDENCIES", True),
            self.define("jsoncpp_DIR", self.spec["jsoncpp"].prefix)
        ]

    @sanitize_paths
    def setup_run_environment(self, env):
        env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        env.prepend_path("FHICL_FILE_PATH", self.prefix.fcl)

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


class Larg4(CMakePackage):
    """Larg4"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larg4"
    git = "https://github.com/LArSoft/larg4.git"
    url = "https://github.com/LArSoft/larg4/archive/v01_02_03.tar.gz"
    list_url = "https://api.github.com/repos/LArSoft/larg4/tags"

    version("09.19.03", sha256="265f26727e1aecd13c8e7a9ebb1a139fd173fd7c49a2e8173ebbd6c7df556c92")
    version("09.19.02", sha256="cb96a048634173c28da11335347a283379032667eb58f710cd3aa39a87e6dc9d")
    version("09.16.07", sha256="79d26dd47873bfea349d485241583743d83b7d0452e6f362a48c44b9d726c90f")
    version("09.16.04", sha256="8344d183ca35e5c2f50986b4228d7c569269373dca0994beab137ec9c831cdf0")
    version("09.16.01", sha256="e17520b7074a3d2ab064c40ef654a694d04770741d2c406e336fa7b5ae987f30")
    version(
        "09.06.02.01", sha256="bf7cc46e222dc095bd9b980bc1987236e6e35dd4d0453c8258705ba02facbc9f"
    )
    version("09.06.02", sha256="761e25df6c38ff2efb020b4079ce019cf43489c2977260fe71d3404cba2b7f0e")
    version("09.06.00", sha256="26213c7cafa20ee890af3abdf607df7bc0adf40b94e19bebfaed71366d1cb442")
    version("09.05.03", sha256="cbda8de6caf2bb49947b9d6a224ebcb43752054178adf973bbadbe10c16021f6")
    version("09.05.02", sha256="e3aa24be58ef507cd89951c8d426214b3f18c4ad5238621302d49ed66127eb53")
    version("09.05.01", sha256="dad253c845f50409661122d338c87d80141d82f0267d1b7a84d58ec484e74124")
    version("09.05.00", sha256="7266d68c62d0980e3d1219d7dd4c9a335f46c178f7b65c1859d8d295741aa673")
    version("09.04.00", sha256="47775a943ce76d5152f222e01e39f202bcbe0e7d4f23dafac989e32a114a1c42")
    version("09.03.15", sha256="d67038d53ae1a899ea36986c0b4095b5ec986580ecac151672c74403ddde3f48")
    version("09.03.14", sha256="c6b6e06ea6affd2c49b8501bc90e6ae765bc47ef948f34334e401dca752ecc0d")
    version("09.03.13", sha256="c9f6fe589cae2cbcac9204c4a7f8f6a9f3605f66556d4e8412a50066249f709e")
    version("mwm1", tag="mwm1", git="https://github.com/marcmengel/larg4.git", get_full_repo=True)
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

    # patch('v09_06_00.patch', when='@09.06.00')
    # patch('v09_06_02.patch', when='@09.06.02')
    patch("v09_06_02_01.patch", when="@09.06.02.01")

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("clhep")
    depends_on("artg4tk")
    depends_on("art")
    depends_on("canvas-root-io")
    depends_on("art-root-io")
    depends_on("nug4")
    depends_on("nurandom")
    depends_on("boost")
    depends_on("cetmodules", type="build")

    def cmake_args(self):
        args = [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]
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
        # Set path to find gdml files
        run_env.prepend_path("FW_SEARCH_PATH", os.path.join(self.prefix, "fw"))
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

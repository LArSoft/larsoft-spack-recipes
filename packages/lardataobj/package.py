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


class Lardataobj(CMakePackage):
    """Lardataobj"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/lardataobj"
    git = "https://github.com/LArSoft/lardataobj.git"
    url = "https://github.com/LArSoft/lardataobj/archive/v01_02_03.tar.gz"
    list_url = "https://api.github.com/repos/LArSoft/lardataobj/tags"

    version("09.18.03", sha256="598cb29ca66d2bf6bc05e158093fa8de6b0a235db5d81493359b37e9f2945d60")
    version("09.18.02", sha256="5a77fd3357b6ff25e071514717418bcf018c6a2b2b96505e17fd8279997e3ab2")
    version("09.17.01", sha256="1649ec98059ae05d579ce2d330f6e7c439627a1cb74d3a0be8f22d963665b859")
    version("09.16.02", sha256="567a55134c963bcec72c6fc6db6660694dda7bc300a487c58901057d0fb8c293")
    version("09.16.01", sha256="98e2ab76f7c512c863e7491749f97d0a0e829bbc30d521a69deecea48f292728")
    version("09.03.05", sha256="e111d36911d885c3c7ae287e299896c05c71d516f74f3906ae4190d18030daa0")
    version("09.03.03", sha256="b594929466ef1f96bf15a4f4348d9b48c2642602314f0c2931fb3b918ddbc8c1")
    version("09.03.02", sha256="54ef53dcc8f5e323017dd9d192901286152e3af018b82e462229d8def9f992ae")
    version("09.03.01", sha256="bd77759644eff165ff56f8d19df295e3b0bda8c1b10d93b185622a1bd0c14c72")
    version("09.03.00", sha256="53b99ae39eb68655a635db35402cf48630960a6c567db18c5632d8357937fa89")
    version("09.02.00", sha256="218a75c66ccdf91a15bfe976e18d98c4c5b7d4bb887928a7081fccf1daf6c0ff")
    version(
        "09.01.06.01", sha256="57258d46daa00a9444a4392ed3b2e1b8035e2012340f0ad3666dbd40bb5292d0"
    )
    version("09.01.06", sha256="d20baf87b41f1a6925345866702b86c45242b02a198e26f0d528afa10db2de0f")
    version(
        "mwm1", tag="mwm1", git="https://github.com/marcmengel/lardataobj.git", get_full_repo=True
    )
    version("develop", branch="develop", get_full_repo=True)

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    patch("v09_03_03.patch", when="@09.03.03")
    patch("v09_03_05.patch", when="@09.03.05")

    def patch(self):
        with when("@:09.81.00 %gcc@13"):
            filter_file(
                "#include <string>",
                "#include <cstdint>\n#include<string>",
                "lardataobj/RawData/AuxDetDigit.h",
            )
            filter_file(
                "#include <string>",
                "#include <cstdint>\n#include<string>",
                "lardataobj/RawData/BeamInfo.h",
            )

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

    depends_on("nusimdata")
    depends_on("larcorealg")
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

    @run_after("install")
    def create_dirs(self):
        mkdirp("{0}/fcl".format(self.spec.prefix))
        mkdirp("{0}/gdml".format(self.spec.prefix))

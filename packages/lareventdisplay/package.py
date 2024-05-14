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


class Lareventdisplay(CMakePackage):
    """Lareventdisplay"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/lareventdisplay"
    git = "https://github.com/LArSoft/lareventdisplay.git"
    url = "https://github.com/LArSoft/lareventdisplay/archive/v01_02_03.tar.gz"
    list_url = "https://api.github.com/repos/LArSoft/lareventdisplay/tags"

    version("09.11.05", sha256="538260a9f7e80a9e82daa94b63a2f8dd438f3d2eb54b3044f682bc5e921e40d7")
    version("09.11.04", sha256="ff9455cf8afc062f8820404928296092f0101bb608b855943aa2c06ad58aa506")
    version("09.10.11", sha256="13dbdac0498248f154ee7abedd813b5f7fb43e93ef5dd8dccceddbc320ca677a")
    version("09.10.08", sha256="b3875a4fdd011b8ad6c116e7eb8c21c7518e16bdd36eaa95ec4ad0c4f35b739c")
    version("09.10.05", sha256="b79ef329c22ea79ab4e4b591b8481d6e08a8d1ec80e83973854f2dd9717e43e8")
    version(
        "09.02.08.02", sha256="fe3623fbc9438f96e66927c8c5b24114b5d0fef0f2e8dd0576b290d0fc9b4147"
    )
    version(
        "09.02.08.01", sha256="38e397c789b566328c5fb05353a2d4da71d13f9c36c7d131e13eeb0c3f270046"
    )
    version("09.02.05", sha256="cf8aa4e78162cea4621b858d0603d244e2efe3a030a0fac0977fcb4fad8afdad")
    version("09.02.03", sha256="8269156d71f25b46c419c1b82f9527957b9a23419865db02bd6f478eabc2ec3d")
    version("09.02.02", sha256="38f5c75fc7b83899cf8b7c7026ed0a339d8d640f9a2a4bf6618c5b1e3a928c72")
    version("09.02.01", sha256="5ec026f061a37e3040a83f1d9442c5eb54a75eb677e1199a2e114df8c9339760")
    version("09.02.00", sha256="efc8b61fdb17bb42297e83e40c941877d71e363f49d123fb310b1d0e15a58fe9")
    version("09.01.21", sha256="691e0707046242b3be0e6dec09ea494ca3951d884323c3039215c8d208da9f8d")
    version("09.01.20", sha256="b6b8cc0299ae92f2ef7483a52437748b277c3b507a729183e299ef2932a9b5d6")
    version("09.01.19", sha256="1e75ec62ea1c657a724b09a002369d87d8be45cffe5367767240980418ddd4fe")
    version("09.01.18", sha256="a790330b9f05320d69f619bd6bb8251f69f9d21c811647e57f3754d16c1dea3b")
    version(
        "mwm1",
        tag="mwm1",
        git="https://github.com/marcmengel/lareventdisplay.git",
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

    patch("v09_02_05.patch", when="@09.02.05")
    # patch('v09_02_08_01.patch', when='@09.02.08.01')
    patch("v09_02_08_02.patch", when="@09.02.08.02")

    depends_on("larreco")
    depends_on("nuevdb")
    depends_on("cetmodules", type="build")

    def cmake_args(self):
        args = [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]
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

    def flag_handler(self, name, flags):
        if name == "cxxflags" and self.spec.compiler.name == "gcc":
            flags.append("-Wno-error=deprecated-declarations")
            flags.append("-Wno-error=class-memaccess")
        return (flags, None, None)

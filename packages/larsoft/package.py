# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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


class Larsoft(CMakePackage):
    """Larsoft"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larsoft"
    git = "https://github.com/LArSoft/larsoft.git"
    url = "https://github.com/LArSoft/larsoft/archive/v01_02_03.tar.gz"
    list_url = "https://api.github.com/repos/LArSoft/larsoft/tags"
    version("09.90.00", sha256="a474ce474713410d4fc673155b63a252267e97759a78ebae44b98ed4834b3537")
    version("09.89.01", sha256="6a4eb0685a9a5db989d416b03b4b062a3e887f44dc1339d27d32644b1dec14e0")
    version("09.81.00", sha256="0e09c369b03b1189cc38db9d7d2ec6a711a1c8dfb99e2b0badb2726c7826aa5d")
    version("09.78.06", sha256="3733332dcf15189688476558fc617873634e75d110fc816eb82305818a5f6f7b")
    version("09.78.00", sha256="c02d744cf66b2494316392a105c2ab8a2224ce5e33ae8e4f695054db77f13a12")
    version(
        "09.37.01.01", sha256="f9563d95c4cae3dca17c15ead61ac0e012d974b957f852d5832b15062e0d20d8"
    )
    version("09.35.00", sha256="49be33531de37214585ae4a84077476275c90d46585d642ef703cd6ea56c03b6")
    version("09.33.00", sha256="b472fea77002e85a0a6732fe83246cefd753ce440cedf2a104c91bcd2645a24e")
    version("09.32.01", sha256="d5cebda4bda7db7cb7500f88aa7549a109b226d2550c292dbe7df55354f735ce")
    version("09.32.00", sha256="d65e7a41807659f0eec023fb977c8ec883059f29d04b37812a7d7b91273a4976")
    version("09.31.00", sha256="5ab2dff9cf5a8c9b5c0020f69451f8d4d90b7adda098566c1deeaa09244886aa")
    version("09.30.00", sha256="8808f02f97b61b45d5a875d90975f89d0999940857cc67a8bf73113ac90d45b7")
    version("09.29.00", sha256="82a34fda06ecfc5c0b51bbd2f456ccb5c2b7ef3e2040a39809e018d0716e4f1d")
    version("09.28.05", sha256="ba65da4275d9433527c75d8a7f187ebb515a64efcbeaaef3c2a4d5f25e0c8266")
    version("09.28.04", sha256="103614e7ea8516c743934ca02fcd9d4e1db870585cb9b0c51c8abbf2bccb1c0e")
    version(
        "mwm1", tag="mwm1", git="https://github.com/marcmengel/larsoft.git", get_full_repo=True
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
    variant(
        "eventdisplay",
        default=True,
        description = "Include lareventisplay and root/geant4 with opengl and x."
    )

    variant(
        "eventdisplay",
        default=False)

    patch("v09_35_00.patch", when="@09.35.00")
    patch("v09_37_01_01.patch", when="@09.37.01.01")

    depends_on("cetmodules", type="build")
    depends_on("larfinder", type="build")
    depends_on("ifdh-art")
    depends_on("larana")
    depends_on("larexamples")
    depends_on("larg4")
    depends_on("larpandora")
    depends_on("larpandoracontent +monitoring", when="+eventdisplay")
    depends_on("larpandoracontent ~monitoring", when="~eventdisplay")
    depends_on("larreco")
    depends_on("larrecodnn")
    depends_on("larsimrad")
    depends_on("larsoft-data")
    depends_on("larsoftobj")
    depends_on("larwirecell")
    depends_on("lareventdisplay", when="+eventdisplay")
    depends_on("root +opengl+x", when="+eventdisplay")
    depends_on("root ~opengl~x", when="~eventdisplay")
    depends_on("geant4 ~opengl~x11~qt", when="~eventdisplay")
    depends_on("pandora ~monitoring", when="~eventdisplay")

    def patch(self):
        with when("~eventdisplay"):
            filter_file(
                r'find_package\( *lareventdisplay.*',
                '',
                'CMakeLists.txt'
            )

    def cmake_args(self):
        args = ["-DCMAKE_CXX_STANDARD={0}".format(self.spec.variants["cxxstd"].value)]
        return args

    def setup_dependent_build_environment(self, spack_env, dspec):
        spack_env.set("LARSOFT_INC", self.prefix.include)
        spack_env.set("LARSOFT_LIB", self.prefix.lib)
        spack_env.prepend_path("PATH", self.prefix.bin)
        spack_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        spack_env.prepend_path("PATH", self.prefix.bin)
        spack_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        spack_env.append_path("FHICL_FILE_PATH", "{0}/fcl".format(self.prefix))
        spack_env.append_path("FW_SEARCH_PATH", "{0}/fw".format(self.prefix))
        sanitize_environments(spack_env)

    def setup_run_environment(self, run_env):
        run_env.prepend_path("PATH", self.prefix.bin)

    @run_after("install")
    def rename_bin_python(self):
        import os

        os.rename(
            join_path(self.spec.prefix, "bin/python"),
            join_path(self.spec.prefix, "bin/python-scripts"),
        )

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


class Larsoftobj(CMakePackage):
    """Larsoftobj"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larsoftobj"
    git = "https://github.com/LArSoft/larsoftobj.git"
    url = "https://github.com/LArSoft/larsoftobj/archive/v01_02_03.tar.gz"
    list_url = "https://api.github.com/repos/LArSoft/larsoftobj/tags"

    version("09.35.03", sha256="5ea48218ddc8b4f185899b57abe7ea5408f3fa27ece5fc018915e95bd174e0e7")
    version("09.35.02", sha256="f8007f38f3596eaea7ae5e5100e39b122512e4453499b54b96223ecaf5efa0b6")
    version("09.34.01", sha256="292d5fdd5f47601fb3f736aee5f98ebc0739060307aeff2df034754c64be6248")
    version("09.32.01", sha256="665d91113e12a36b7cb289337ed66d371c1d48f880fc1b68b7f64d42b37468c3") # FIX ME
    version("09.31.01", sha256="68b6a1e9204e72f508cf54f8f02515c283b5a67d1b5d0bba2a49c000f7f679e3")
    version(
        "09.12.00.01", sha256="c3e9a901fca51f521fa2299182a15b50eacdc702ae0018d6e458627122b5b147"
    )
    version("09.12.00", sha256="be05f4b4c9a91ace38d8f993b886e812686bd4d9877c93ffe9029acb4f01cae7")
    version("09.11.00", sha256="fdb18a29201f8361c7b5c8a923dbfecdeb13ec774d760aabbb7b1d4ef1ff3e87")
    version("09.10.02", sha256="6baa83ca84a93738bdb732ab7d77e94278e7e2bbc2c846be3bf4c42e922d6803")
    version("09.10.01", sha256="40cf54906286b6de95b4452c8dca4cbcb7e4368cbd75b951b29d6facb6c380ee")
    version("09.10.00", sha256="7d0325b5854cebb24316b4361e106c7b6e2eb46c8f2b6cd5c5d3554c2b27b1cc")
    version("09.09.00", sha256="cb95eef62900dbd079358f551f55fc4618cbd07ccf7597a64c17997eed0bd778")
    version("09.08.00", sha256="754244c71ef8fa11b4253bdccb5b759d595cff6b3cbec5950fd7991722978e6e")
    version(
        "09.07.01.01", sha256="bced9f49dce8df06040eb2e308e09cf3fdd19f76ef36116c8f83b0265572ac2a"
    )
    version(
        "mwm1", tag="mwm1", git="https://github.com/marcmengel/larsoftobj.git", get_full_repo=True
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

    # patch('v09_11_00.patch', when='@09.11.00')
    # patch('v09_12_00.patch', when='@09.12.00')
    patch("v09_12_00_01.patch", when="@09.12.00.01")

    variant(
        "cxxstd",
        default="17",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("gallery")
    depends_on("lardataobj")
    depends_on("lardataalg")
    depends_on("cetmodules", type="build")

    def cmake_args(self):
        args = ["-DCMAKE_CXX_STANDARD={0}".format(self.spec.variants["cxxstd"].value)]
        return args

    @run_before("install")
    def install_something(self):
        """this pacakge doesn't really contain anything, but
        Spack doesn't like empty products, so put in a README..."""
        f = open(self.prefix + "/README.larsoftobj", "w")
        f.write("larsoftobj is just a bunde with dependencies")
        f.close()

    def setup_dependent_build_environment(self, spack_env, dspec):
        # Ensure we can find plugin libraries.
        spack_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        spack_env.prepend_path("PATH", self.prefix.bin)
        spack_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        spack_env.append_path("FHICL_FILE_PATH", "{0}/fcl".format(self.prefix))
        spack_env.append_path("FW_SEARCH_PATH", "{0}/gdml".format(self.prefix))
        sanitize_environments(spack_env)

    def setup_run_environment(self, run_env):
        # Ensure we can find plugin libraries.
        run_env.prepend_path("CET_PLUGIN_PATH", self.prefix.lib)
        run_env.prepend_path("PATH", self.prefix.bin)
        run_env.prepend_path("ROOT_INCLUDE_PATH", self.prefix.include)
        run_env.append_path("FHICL_FILE_PATH", "{0}/fcl".format(self.prefix))
        run_env.append_path("FW_SEARCH_PATH", "{0}/gdml".format(self.prefix))
        sanitize_environments(run_env)

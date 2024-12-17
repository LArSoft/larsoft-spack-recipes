# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *
from spack.package import *
from spack.pkg.fnal_art.fnal_github_package import *


class Larsoft(CMakePackage, FnalGithubPackage):
    """Software for Liquid Argon time projection chambers"""

    repo = "LArSoft/larsoft"
    homepage = "https://larsoft.org"
    version_patterns = ["v09_00_00", "09.85.00"]

    version("10.00.03", sha256="34252e8b8f5e5bf2178b9cfa9cf53a4f78d735c9df65166b38dabb269624c4ce")
    version("10.00.01", sha256="e8031eb61d5b7da66d20884cf23f1de007c109ecff28d3e000db8175082ad966")
    version("10.00.00", sha256="02f11cbbd668c801c1e18bc5c796eb5fe6dfef1dcd39f2c77672f468c58b3121")
    version("09.93.00", sha256="71aec2833eb14cea7a75051f2127c9b1af43638b4b0e71c2e3964bdacf2a2c04")
    version("09.90.01", sha256="93dd9ac43a6b21b73e59d9c31a59a3c2037a845348cee4c11add74eb01bd76a0")
    version("develop", branch="develop", get_full_repo=True)

    cxxstd_variant("17", "20", default="17")
    variant(
        "eventdisplay",
        default=True,
        description="Include lareventdisplay and root/geant4 with opengl and x.",
    )

    variant(
        "tensorflow",
        default=False,
        description="Include larrecodnn and larsimdnn that depend on tensorflow",
    )

    depends_on("cetmodules", type="build")

    depends_on("larfinder")
    depends_on("larsoftobj")
    depends_on("larsoft-data")
    depends_on("larana")
    depends_on("larexamples")
    depends_on("larpandora")
    depends_on("larreco")
    depends_on("larsimrad")
    depends_on("larwirecell")

    with when("+eventdisplay"):
        depends_on("lareventdisplay")
        depends_on("larpandoracontent +monitoring")
        depends_on("root +opengl+x")

    with when("~eventdisplay"):
        depends_on("geant4 ~opengl~x11~qt")
        depends_on("larpandoracontent ~monitoring")
        depends_on("root ~opengl~x")

    with when("+tensorflow"):
        depends_on("larrecodnn+tensorflow")
        depends_on("larsimdnn+tensorflow")

    with when("~tensorflow"):
        depends_on("larrecodnn~tensorflow")
        depends_on("larsimdnn~tensorflow")

    def patch(self):
        with when("@:09.90.01.01 ~eventdisplay"):
            filter_file(r"find_package\( *lareventdisplay.*", "", "CMakeLists.txt")

    def patch(self):
        with when("~tensorflow"):
            filter_file(r"find_package\( *larrecodnn.*", "", "CMakeLists.txt")
            filter_file(r"find_package\( *larsimdnn.*", "", "CMakeLists.txt")

    @run_after("install")
    def rename_bin_python(self):
        os.rename(
            join_path(self.spec.prefix, "bin/python"),
            join_path(self.spec.prefix, "bin/python-scripts"),
        )

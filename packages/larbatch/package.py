# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

class Larbatch(CMakePackage):
    """package for batch job submission featuring project.py"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larbatch-web-client/wiki"
    url = "https://github.com/LArSoft/larbatch/archive/refs/tags/v01_51_15.tar.gz"

    version("01.59.04", sha256="8158d2e1b5f208d1014b3745c347d49e3e3449c240842af5361c67fd3b269dff")
    version("1.51.15", sha256="adc956e621f36c7fbf37f85c737e793d8fc8e58ad44ec3077ea80830f1b7ad25")

    depends_on("sam-web-client", type=("run"))
    depends_on("python", type=("run"))
    depends_on("cetmodules", type="build") 

    def url_for_version(self, version):
        urlf = "https://github.com/LArSoft/larbatch/archive/refs/tags/v%s.tar.gz"
        return urlf % version.underscored

    version("1.51.15", sha256="adc956e621f36c7fbf37f85c737e793d8fc8e58ad44ec3077ea80830f1b7ad25")

    patch("cmake.patch" , when=("@:1.57.00")) 

    @run_before("cmake")
    def patch_version(self):
        print("filtering version in CMakeLists.txt")
        filter_file(
            r"project\(larbatch .*\)",
            "project(larbatch VERSION {})".format(self.spec.version),
            "CMakeLists.txt"
        )

    def cmake_args(self):
        args = [
        ]
        return args

    def setup_run_environment(self, run_env):
        run_env.prepend_path("PATH", self.prefix.bin)
        run_env.prepend_path("PYTHONPATH", self.prefix.bin)
        run_env.prepend_path("PYTHONPATH", self.prefix.python)
        run_env.prepend_path("PYTHONPATH", str(self.prefix.larbatch.v) + str(self.spec.version.underscored) + "/python")

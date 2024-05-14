# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class LarsoftData(Package):
    """LarsoftData"""

    homepage = "https://cdcvs.fnal.gov/redmine/projects/larsoft"

    url = "https://scisoft.fnal.gov/scisoft/packages/larsoft_data/v1_02_01/larsoft_data-1_02_01-noarch.tar.bz2"

    version("1.02.02", sha256="078c85d4e79d3452a3f8cd6db784d4cbd1ca3b7efe10e8b840ec78c0df3fa695") # FIX ME
    version("1.02.01", sha256="9b3e5d763f4a44f0fae7a2b59d583a8b25054f7f06645fa48e331377cf33baca")

    def url_for_version(self, version):
        url = "https://scisoft.fnal.gov/scisoft/packages/larsoft_data/v{0}/larsoft_data-{1}-noarch.tar.bz2"
        return url.format(version.underscored, version)

    def install(self, spec, prefix):
        install_tree(
            "{0}/v{1}".format(self.stage.source_path, self.version.underscored),
            "{0}".format(prefix),
        )

    def _add_paths_to_environment(self, env):
        for path_fragment in (
            "uboone",
            "Argoneut",
            "Genfit",
            "ParticleIdentification",
            "PhotonPropagation/LibraryData",
            os.path.join("pdf", "Gaisser"),
            os.path.join("pdf", "MUSUN"),
            "SupernovaNeutrinos",
            "",
        ):
            path = os.path.join(self.prefix, path_fragment)
            env.prepend_path("FW_SEARCH_PATH", path)

    def setup_run_environment(self, run_env):
        self._add_paths_to_environment(run_env)

    def setup_dependent_build_environment(self, spack_env, dep_spec):
        self._add_paths_to_environment(spack_env)

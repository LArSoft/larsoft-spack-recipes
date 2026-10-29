# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack_repo.builtin.packages.celeritas.package import Celeritas as CeleritasBuiltin
from spack_repo.fnal_art.packages.fnal_github_package.package import sanitize_paths
from typing import Dict, Set


class Celeritas(CeleritasBuiltin):
    # Override variant defaults
    variant("covfie", default=False, description="Use fields")
    variant("hepmc3", default=False, description="Directly load from HepMC3")
    variant("vecgeom", default=False, description="Use VecGeom geometry")

    conflicts("~geant4") # G4 required
    conflicts("~root") # LArSoft requires ROOT
    conflicts("+vecgeom") # Optical physics doesn't work
    conflicts("@:0.6") # Earlier versions do not support larsoft

    depends_on("cetmodules")
    depends_on("art")
    depends_on("art-root-io")
    depends_on("larcore")
    depends_on("lardataobj")
    depends_on("larsim")

    def celer_force_packages(self):
        result = super().celer_force_packages()
        result["LArSoft"] = True
        return result

    @sanitize_paths
    def setup_run_environment(self, env):
        super().setup_run_environment(env)
        spec = self.spec["celeritas"]
        env.prepend_path("CET_PLUGIN_PATH", spec.libs.directories[0]) # lib or lib64
        env.prepend_path("FHICL_FILE_PATH", spec.prefix.fcl)

    def cmake_args(self):
        if not hasattr(CeleritasBuiltin, "celer_force_packages"):
            raise InstallError("Spack builtin package repository is out of date! Ensure https://github.com/spack/spack-packages/pull/7120 is merged")
        return super().cmake_args()


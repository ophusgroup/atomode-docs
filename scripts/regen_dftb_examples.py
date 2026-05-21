"""Regenerate the DFTB+ refinement example artefacts for the
``docs/examples_dftb/`` pages.

For each chosen regime (amorphous, SRO, nanocrystalline) this script
runs the four-stage SiO₂ pipeline:

  1. Voronoi tile (cell.generate(num_steps=0) + close-pair push)
  2. Orientation refinement (cell.refine_initial_orientations)
  3. FIRE shell-relax (cell.shell_relax)
  4. DFTB+ relax (LBFGS via ASE)

At each stage it captures positions, computes a DFTB+ single-point
energy, and writes:

  docs/_static/dftb/{regime}_traj.xyz           # 4-frame trajectory
  docs/_static/dftb/{regime}_energies.json      # per-stage energies
  docs/_static/dftb/{regime}_summary.json       # peak positions, timings
  docs/_static/dftb/{regime}_gr.png             # g(r) stack at each stage
  docs/_static/dftb/{regime}_bond_hist.png      # Si-O bond length histogram
  docs/_static/dftb/{regime}_angle_hist.png     # O-Si-O + Si-O-Si angle histograms

Requires:
  * DFTB+ installed and on $PATH (``which dftb+`` returns a result)
  * matsci-0-3 Slater-Koster files unpacked somewhere on disk
  * ``DFTB_COMMAND`` env var pointing at the dftb+ binary (defaults to ``dftb+``)
  * ``DFTB_PREFIX`` env var pointing at the SK files directory
    (must include trailing slash; ASE concatenates filename onto this)

Usage:
  python scripts/regen_dftb_examples.py                 # all three regimes
  python scripts/regen_dftb_examples.py --regime amorphous
  python scripts/regen_dftb_examples.py --box 25.0      # bigger cell (slower)
  python scripts/regen_dftb_examples.py --skip-dftb     # everything except DFTB+
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import warnings
from pathlib import Path

import numpy as np


# --------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[1]
TRICOR_SRC = REPO_ROOT.parent / "tricor" / "src"
STRUCTURES = REPO_ROOT / "docs" / "structures"
OUT_DIR = REPO_ROOT / "docs" / "_static" / "dftb"

# Per-regime parameters for SiO₂.  Tuned for a 20\xb3 \xc5 cell
# (~600 atoms): grain_size shrunk for nanocrystalline so a whole grain
# fits inside the small example cell.
SIO2_REGIMES = {
    "amorphous": dict(
        grain_size=10.0, num_steps=150,
        bond_weight=1.55, angle_weight=1.25, repulsion_weight=1.25,
        hard_core_scale=0.81, nonbond_push_scale=0.7,
        displacement_sigma=0.012,
    ),
    "sro": dict(
        grain_size=12.0, num_steps=200,
        bond_weight=1.65, angle_weight=1.35, repulsion_weight=1.3,
        hard_core_scale=0.82, nonbond_push_scale=0.72,
        displacement_sigma=0.010,
    ),
    "nanocrystalline": dict(
        # Standard nanocrystalline preset is 35 \xc5; shrunk further
        # here so the grain fits inside the 15\xb3 \xc5 example cell.
        # Document this choice in the per-regime page.
        grain_size=13.0, num_steps=200,
        bond_weight=1.65, angle_weight=1.35, repulsion_weight=1.3,
        hard_core_scale=0.82, nonbond_push_scale=0.72,
        displacement_sigma=0.004,
    ),
}


def _setup_paths() -> None:
    """Make tricor importable + create the output dir."""
    if str(TRICOR_SRC) not in sys.path:
        sys.path.insert(0, str(TRICOR_SRC))
    OUT_DIR.mkdir(parents=True, exist_ok=True)


def _check_dftb_available() -> tuple[bool, str]:
    """Verify DFTB+ binary + SK files are reachable.  Returns (ok, msg)."""
    import shutil
    cmd = os.environ.get("DFTB_COMMAND", "dftb+")
    if shutil.which(cmd) is None:
        return False, (
            f"DFTB+ binary {cmd!r} not on $PATH.  Install with:\n"
            "    conda install -c conda-forge dftbplus\n"
            "and/or set DFTB_COMMAND to point at the binary."
        )
    prefix = os.environ.get("DFTB_PREFIX")
    if not prefix:
        return False, (
            "DFTB_PREFIX env var not set.  Point it at the unpacked\n"
            "matsci-0-3 (or similar) Slater-Koster directory, e.g.:\n"
            "    export DFTB_PREFIX=/Users/me/dftb_sk/matsci-0-3/\n"
            "(trailing slash required - ASE concatenates filenames onto it)."
        )
    if not Path(prefix).is_dir():
        return False, f"DFTB_PREFIX={prefix!r} is not a directory."
    # Check for one of the expected SK files
    needed = ["Si-Si.skf", "Si-O.skf", "O-O.skf", "O-Si.skf"]
    missing = [f for f in needed if not (Path(prefix) / f).exists()]
    if missing:
        return False, (
            f"DFTB_PREFIX={prefix!r} is missing SK files: {missing}.\n"
            "Get the matsci-0-3 set from https://dftb.org/parameters/download"
        )
    return True, ""


def _make_dftb_calc(atoms, label="dftb_sio2", read_charges=False):
    """Build an ASE Dftb calculator with SCC + Fermi smearing.

    Uses the s/p basis on Si and O — standard for ground-state SiO₂
    calculations with the matsci-0-3 set.  Tolerances chosen for
    "good enough" convergence (95%-ish), not strict DFT-accuracy.

    Parameters
    ----------
    read_charges
        When ``True`` (used for the FIRE relax steps after a seed SP
        has run), the SCC reads ``charges.bin`` written by the
        previous DFTB+ invocation.  Cuts initial SCC error from
        ~1.4 to ~0.01-0.1 and is the main mitigation against SCC
        sloshing partway through a relaxation.  DFTB+ errors out if
        the file doesn't exist, so pass ``False`` for the first call.
    """
    from ase.calculators.dftb import Dftb
    return Dftb(
        label=label,
        atoms=atoms,
        Hamiltonian_="DFTB",
        Hamiltonian_SCC="Yes",
        Hamiltonian_SCCTolerance=1e-2,  # loose; we relax to fmax=1.0 eV/Å anyway
        Hamiltonian_MaxSCCIterations=200,
        Hamiltonian_MaxAngularMomentum_="",
        Hamiltonian_MaxAngularMomentum_Si="p",
        Hamiltonian_MaxAngularMomentum_O="p",
        Hamiltonian_Filling_="Fermi",
        # Higher Fermi temperature smooths small-gap configurations
        # that would otherwise cause charge sloshing.  3500 K is still
        # well below the SCC's structural sensitivity threshold.
        Hamiltonian_Filling_Temperature=0.012,  # Ha (≈ 3800 K)
        Hamiltonian_Mixer_="Broyden",
        Hamiltonian_Mixer_MixingParameter=0.02,  # gentler than 0.05
        # Charge restart: each DFTB+ invocation reads the previous
        # step's converged charges from charges.bin (written
        # automatically by DFTB+).  This is the biggest single
        # mitigation for SCC blow-up during a relaxation — instead of
        # starting each step from "atomic" charges (error ~1.4) we
        # start from the previous geometry's converged solution (error
        # ~0.01-0.1).  Five iters to converge vs 30+.  DFTB+ silently
        # falls back to atomic charges if charges.bin doesn't exist
        # yet, so it's safe to set unconditionally.
        Hamiltonian_ReadInitialCharges=("Yes" if read_charges else "No"),
        Hamiltonian_WriteCharges="Yes",
        kpts=(1, 1, 1),  # Γ-only for a periodic supercell
    )


def _single_point_energy(atoms) -> float:
    """Run a DFTB+ single-point and return the total potential energy
    in eV.  Mutates atoms.calc.  Always starts from atomic charges -
    deletes any stale charges.bin so a leftover density from a
    previous (different-geometry) call doesn't poison the SCC."""
    for stale in ("charges.bin", "charges.dat"):
        p = Path(stale)
        if p.exists():
            p.unlink()
    atoms.calc = _make_dftb_calc(atoms, read_charges=False)
    return float(atoms.get_potential_energy())


def _measure_si_o_bond(atoms, cell_pbc=True):
    """Return (peak, mean, std, N) of the Si-O bond distance < 1.9 \xc5."""
    from scipy.spatial import cKDTree
    pos = atoms.positions.astype(np.float64)
    box = np.diag(atoms.cell.array).astype(np.float64)
    pw = pos - np.floor(pos / box) * box if cell_pbc else pos
    tree = cKDTree(pw, boxsize=box if cell_pbc else None)
    pairs = tree.query_pairs(2.5, output_type="ndarray")
    if len(pairs) == 0:
        return (float("nan"),) * 4
    z = atoms.numbers
    si = z[pairs[:, 0]] == 14
    sj = z[pairs[:, 1]] == 14
    sio = (si & ~sj) | (~si & sj)
    delta = pw[pairs[:, 1]] - pw[pairs[:, 0]]
    if cell_pbc:
        delta -= np.round(delta / box) * box
    d = np.linalg.norm(delta, axis=1)
    dm = d[sio & (d < 1.9)]
    if dm.size == 0:
        return (float("nan"),) * 4
    h, e = np.histogram(dm, bins=120, range=(1.3, 1.9))
    peak = 0.5 * (e[np.argmax(h)] + e[np.argmax(h) + 1])
    return float(peak), float(dm.mean()), float(dm.std()), int(dm.size)


def _measure_angles(atoms):
    """Return (O-Si-O angles, Si-O-Si angles) in degrees."""
    from scipy.spatial import cKDTree
    pos = atoms.positions.astype(np.float64)
    box = np.diag(atoms.cell.array).astype(np.float64)
    pw = pos - np.floor(pos / box) * box
    z = atoms.numbers
    tree = cKDTree(pw, boxsize=box)
    pairs = tree.query_pairs(2.5, output_type="ndarray")
    si_mask_a = z[pairs[:, 0]] == 14
    sj_mask_a = z[pairs[:, 1]] == 14
    sio = (si_mask_a & ~sj_mask_a) | (~si_mask_a & sj_mask_a)
    delta = pw[pairs[:, 1]] - pw[pairs[:, 0]]
    delta -= np.round(delta / box) * box
    d = np.linalg.norm(delta, axis=1)
    keep = sio & (d < 1.9)

    # Build per-Si list of (O_idx, vec_Si→O) and per-O list of (Si_idx, vec_O→Si)
    si_atoms = np.where(z == 14)[0]
    o_atoms = np.where(z == 8)[0]
    si_lookup = {int(s): i for i, s in enumerate(si_atoms)}
    o_lookup = {int(o): i for i, o in enumerate(o_atoms)}
    si_neighbors = [[] for _ in si_atoms]
    o_neighbors = [[] for _ in o_atoms]
    for k in np.where(keep)[0]:
        i, j = int(pairs[k, 0]), int(pairs[k, 1])
        if z[i] == 14 and z[j] == 8:
            si_neighbors[si_lookup[i]].append(delta[k])
            o_neighbors[o_lookup[j]].append(-delta[k])
        elif z[i] == 8 and z[j] == 14:
            si_neighbors[si_lookup[j]].append(-delta[k])
            o_neighbors[o_lookup[i]].append(delta[k])

    def angle_list(per_centre):
        out = []
        for vecs in per_centre:
            if len(vecs) < 2:
                continue
            v = np.array(vecs)
            v = v / np.linalg.norm(v, axis=1, keepdims=True).clip(min=1e-12)
            for i in range(len(v)):
                for j in range(i + 1, len(v)):
                    cos = float(np.clip(v[i] @ v[j], -1.0, 1.0))
                    out.append(np.degrees(np.arccos(cos)))
        return np.array(out)

    return angle_list(si_neighbors), angle_list(o_neighbors)


def _gr_per_species(atoms, r_max=6.0, dr=0.05):
    """Return (r_centres, g_SiO, g_OO, g_SiSi) — raw counts per bin."""
    from scipy.spatial import cKDTree
    pos = atoms.positions.astype(np.float64)
    box = np.diag(atoms.cell.array).astype(np.float64)
    pw = pos - np.floor(pos / box) * box
    tree = cKDTree(pw, boxsize=box)
    pairs = tree.query_pairs(r_max, output_type="ndarray")
    z = atoms.numbers
    si = z[pairs[:, 0]] == 14
    sj = z[pairs[:, 1]] == 14
    delta = pw[pairs[:, 1]] - pw[pairs[:, 0]]
    delta -= np.round(delta / box) * box
    d = np.linalg.norm(delta, axis=1)
    edges = np.arange(0.0, r_max + dr, dr)
    centres = 0.5 * (edges[:-1] + edges[1:])

    def histo(mask):
        return np.histogram(d[mask], bins=edges)[0].astype(np.float64)

    sio = (si & ~sj) | (~si & sj)
    oo = (~si) & (~sj)
    sisi = si & sj
    return centres, histo(sio), histo(oo), histo(sisi)


# --------------------------------------------------------------------
# Plotting
# --------------------------------------------------------------------

def _plot_gr_stack(stage_atoms, regime, out_path):
    """One overlaid g(r) plot per pair-type, stacked vertically.
    Top: Si-O, middle: O-O, bottom: Si-Si.  Lines per stage."""
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(3, 1, figsize=(7.5, 8.5), sharex=True)
    colors = ["#888", "#3a7", "#27a", "#c33"]
    labels = ["Voronoi", "after orient", "after FIRE", "after DFTB+"]
    for stage_idx, (name, atoms) in enumerate(stage_atoms.items()):
        r, sio, oo, sisi = _gr_per_species(atoms, r_max=6.0, dr=0.05)
        # Density-normalise: divide by r^2 to suppress shell-volume bias
        norm = np.maximum(r * r, 1e-9)
        c = colors[stage_idx]
        lab = labels[stage_idx]
        axes[0].plot(r, sio / norm, color=c, label=lab, lw=1.4)
        axes[1].plot(r, oo / norm, color=c, lw=1.4)
        axes[2].plot(r, sisi / norm, color=c, lw=1.4)
    for ax, title in zip(axes, ["Si–O", "O–O", "Si–Si"]):
        ax.set_ylabel(f"g({title}) (a.u.)")
        ax.grid(alpha=0.3)
    axes[0].legend(loc="upper right", fontsize=8)
    axes[2].set_xlabel("r (\xc5)")
    fig.suptitle(f"SiO₂ {regime} — pairwise g(r) at each refinement stage")
    fig.tight_layout()
    fig.savefig(out_path, dpi=140, bbox_inches="tight")
    plt.close(fig)


def _plot_bond_hist(stage_atoms, regime, out_path):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(7.0, 4.0))
    colors = ["#888", "#3a7", "#27a", "#c33"]
    labels = ["Voronoi", "after orient", "after FIRE", "after DFTB+"]
    for idx, (name, atoms) in enumerate(stage_atoms.items()):
        peak, mean, std, n = _measure_si_o_bond(atoms)
        # Histogram the actual bond distances
        from scipy.spatial import cKDTree
        pos = atoms.positions.astype(np.float64)
        box = np.diag(atoms.cell.array).astype(np.float64)
        pw = pos - np.floor(pos / box) * box
        tree = cKDTree(pw, boxsize=box)
        pairs = tree.query_pairs(2.5, output_type="ndarray")
        z = atoms.numbers
        si = z[pairs[:, 0]] == 14
        sj = z[pairs[:, 1]] == 14
        sio = (si & ~sj) | (~si & sj)
        delta = pw[pairs[:, 1]] - pw[pairs[:, 0]]
        delta -= np.round(delta / box) * box
        d = np.linalg.norm(delta, axis=1)
        dm = d[sio & (d < 1.9)]
        ax.hist(dm, bins=np.arange(1.30, 1.90, 0.01),
                histtype="step", color=colors[idx],
                label=f"{labels[idx]}  (⟨r⟩={mean:.3f}\xc5, σ={std:.3f})",
                linewidth=1.4)
    ax.set_xlabel("Si–O distance (\xc5)")
    ax.set_ylabel("count")
    ax.set_title(f"SiO₂ {regime} — Si–O bond length distribution")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8, loc="upper right")
    fig.tight_layout()
    fig.savefig(out_path, dpi=140, bbox_inches="tight")
    plt.close(fig)


def _plot_angle_hist(stage_atoms, regime, out_path):
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.0))
    colors = ["#888", "#3a7", "#27a", "#c33"]
    labels = ["Voronoi", "after orient", "after FIRE", "after DFTB+"]
    for idx, (name, atoms) in enumerate(stage_atoms.items()):
        osio, sios = _measure_angles(atoms)
        if osio.size:
            axes[0].hist(osio, bins=np.arange(60, 180, 2),
                         histtype="step", color=colors[idx],
                         label=f"{labels[idx]}  (⟨α⟩={osio.mean():.1f}\xb0)",
                         linewidth=1.4)
        if sios.size:
            axes[1].hist(sios, bins=np.arange(80, 180, 2),
                         histtype="step", color=colors[idx],
                         label=f"{labels[idx]}  (⟨α⟩={sios.mean():.1f}\xb0)",
                         linewidth=1.4)
    axes[0].set_xlabel("O–Si–O angle (\xb0)")
    axes[0].set_ylabel("count")
    axes[0].set_title("O–Si–O (tetrahedral, target 109.5\xb0)")
    axes[0].axvline(109.5, color="black", ls="--", alpha=0.4, lw=1)
    axes[1].set_xlabel("Si–O–Si angle (\xb0)")
    axes[1].set_title("Si–O–Si (bridge, ~140\xb0 vitreous)")
    for ax in axes:
        ax.grid(alpha=0.3)
        ax.legend(fontsize=8, loc="upper right")
    fig.suptitle(f"SiO₂ {regime} — angle distributions")
    fig.tight_layout()
    fig.savefig(out_path, dpi=140, bbox_inches="tight")
    plt.close(fig)


# --------------------------------------------------------------------
# Pipeline
# --------------------------------------------------------------------

def _run_pipeline(regime, kw, box, rng_seed, skip_dftb=False):
    """Run the 4-stage pipeline for one regime, return artefacts dict."""
    import tricor as tc
    from tricor.shells import CoordinationShellTarget
    from ase.io import read, write
    from ase.optimize import LBFGS

    print(f"\n--- {regime}   box {box:.1f}\xb3 \xc5, kw={kw['grain_size']=}A "
          f"num_steps={kw['num_steps']} ---", flush=True)

    atoms_ref = read(str(STRUCTURES / "SiO2.cif"))
    shell = CoordinationShellTarget.from_atoms(atoms_ref, phi_num_bins=36)

    cell = tc.Supercell.from_atoms(
        atoms_ref,
        cell_dim_angstroms=(float(box),) * 3,
        r_max=10.0, r_step=0.1, phi_num_bins=36, rng_seed=rng_seed,
    )

    timings = {}
    energies = {}

    # ----- stage 1: Voronoi tile (num_steps=0 → no FIRE yet) -----
    # ``num_steps`` from the regime dict drives the FIRE pass at stage 3,
    # so strip it out here.
    kw_no_steps = {k: v for k, v in kw.items() if k != "num_steps"}
    t0 = time.time()
    cell.generate(shell, num_steps=0, capture_trajectory=False,
                  show_progress=False, **kw_no_steps)
    timings["voronoi"] = time.time() - t0
    atoms_voronoi = cell.atoms.copy()
    print(f"  stage 1 (Voronoi):                 {timings['voronoi']:5.1f}s  "
          f"({len(atoms_voronoi)} atoms)")

    # ----- stage 2: orientation refinement -----
    t0 = time.time()
    if kw.get("grain_size") is not None:
        cell.refine_initial_orientations(
            shell,
            bond_weight=kw["bond_weight"],
            angle_weight=kw["angle_weight"],
            repulsion_weight=kw["repulsion_weight"],
            hard_core_scale=kw["hard_core_scale"],
            nonbond_push_scale=kw["nonbond_push_scale"],
            show_progress=False,
        )
    timings["orient"] = time.time() - t0
    atoms_orient = cell.atoms.copy()
    print(f"  stage 2 (orient refinement):       {timings['orient']:5.1f}s")

    # ----- stage 3: FIRE shell-relax -----
    t0 = time.time()
    cell.shell_relax(
        shell, num_steps=kw["num_steps"], show_progress=False,
        bond_weight=kw["bond_weight"],
        angle_weight=kw["angle_weight"],
        repulsion_weight=kw["repulsion_weight"],
        hard_core_scale=kw["hard_core_scale"],
        nonbond_push_scale=kw["nonbond_push_scale"],
    )
    timings["fire"] = time.time() - t0
    atoms_fire = cell.atoms.copy()
    print(f"  stage 3 (FIRE {kw['num_steps']:>3d} steps):       "
          f"{timings['fire']:5.1f}s")

    # ----- stage 4: DFTB+ relax -----
    # Uniform pipeline across all regimes — no regime-aware branching:
    #
    #   (a) bond_relax(20) tightens bonded pairs to their pair_peak,
    #       softly nudging atoms back to canonical distances.  Uses
    #       cKDTree at O(N log N); doesn't have FIRE's "bond springs
    #       pull pairs through walls" failure mode.
    #
    #   (b) enforce_hard_core(40) projects out any sub-hard-core
    #       pairs.  Pure geometric projection — needed because DFTB+'s
    #       atomic orbitals overlap badly at <0.9 × hard_min distances
    #       and the SCC blows up.
    #
    #   (c) DFTB+ relaxation via ASE's FIRE optimizer with maxstep
    #       limit (0.03 Å) and UnitCellFilter wrap so the cell can
    #       relax too.  The cell-volume relaxation is important for
    #       amorphous, where tricor places atoms at α-quartz density
    #       (~2.65 g/cm³) but the relaxed vitreous structure prefers
    #       ~2.20 g/cm³.
    #
    # Empirically this pipeline converges cleanly on amorphous, SRO,
    # and nanocrystalline regimes without per-regime tuning.
    cell.atoms = atoms_fire.copy()
    cell.bond_relax(shell, n_iter=20)
    cell.enforce_hard_core(shell, n_iter=40)
    atoms_dftb = cell.atoms.copy()
    last_dftb_energy = None
    if not skip_dftb:
        t0 = time.time()
        # Clear any stale charges from a previous regime run.
        for stale in ("charges.bin", "charges.dat"):
            p = Path(stale)
            if p.exists():
                p.unlink()
        # Seed SCC: one explicit single-point on the starting geometry.
        # This writes charges.bin, which subsequent SCC calls reuse as
        # their initial-guess density.  Without this seed, the FIRE
        # loop's first SCC call would error if ReadInitialCharges=Yes.
        print("  seeding SCC (one-shot single-point)...")
        t_seed = time.time()
        atoms_dftb.calc = _make_dftb_calc(atoms_dftb, read_charges=False)
        try:
            atoms_dftb.get_potential_energy()  # writes charges.bin
            print(f"    seed converged ({time.time() - t_seed:.1f}s)")
        except Exception as exc:  # noqa: BLE001
            warnings.warn(
                f"Seed SCC failed for {regime!r}: {exc!s}.\n"
                "Continuing with atomic-charges fallback for the relax.",
            )
        # Build a fresh calc that will read charges.bin every step,
        # and start the relax.
        atoms_dftb.calc = _make_dftb_calc(atoms_dftb, read_charges=True)
        from ase.filters import UnitCellFilter
        from ase.optimize import FIRE as ASEFire
        # ``hydrostatic_strain=True`` restricts the cell DOFs to
        # isotropic volume changes only (no shear).  Empirically this
        # is more SCC-stable with matsci-0-3 than full shear DOFs.
        ucf = UnitCellFilter(atoms_dftb, hydrostatic_strain=True,
                             scalar_pressure=0.0)
        traj_path = OUT_DIR / f"{regime}_dftb_traj.traj"
        opt = ASEFire(ucf,
                      logfile=str(OUT_DIR / f"{regime}_dftb_relax.log"),
                      trajectory=str(traj_path),
                      maxstep=0.03)
        try:
            opt.run(fmax=1.0, steps=40)
        except Exception as exc:  # noqa: BLE001
            warnings.warn(
                f"DFTB+ relax stopped early at {regime!r}: {exc!s}.\n"
                "Recovering best-energy frame from trajectory.",
            )
        # Whether the relax converged or crashed, pull the
        # best-energy frame from the trajectory file.  This is correct
        # for both cases: the converged run's last frame is the best;
        # a crashed run's "current atoms" is at the failed position,
        # so we explicitly seek the best valid frame.
        try:
            from ase.io.trajectory import Trajectory as _ASETraj
            with _ASETraj(str(traj_path), "r") as tr:
                if len(tr) > 0:
                    energies_list = [float(f.get_potential_energy()) for f in tr]
                    best_idx = int(np.argmin(energies_list))
                    best_atoms = tr[best_idx]
                    atoms_dftb.positions = best_atoms.positions.copy()
                    atoms_dftb.cell = best_atoms.cell.array.copy()
                    last_dftb_energy = energies_list[best_idx]
                    print(f"  best DFTB+ frame: step {best_idx}/{len(tr)-1}"
                          f" at {last_dftb_energy:.2f} eV")
        except Exception as exc:  # noqa: BLE001
            warnings.warn(
                f"Couldn't recover best frame for {regime!r}: {exc!s}",
            )
        timings["dftb_relax"] = time.time() - t0
        print(f"  stage 4 (DFTB+ relax):            {timings['dftb_relax']:5.1f}s")

        # Single-point energies at each prior stage (uses the same Dftb calc)
        print("  computing per-stage DFTB+ single-points...")
        for stage_name, atoms in [
            ("voronoi", atoms_voronoi),
            ("orient", atoms_orient),
            ("fire", atoms_fire),
        ]:
            try:
                t0 = time.time()
                energies[stage_name] = _single_point_energy(atoms.copy())
                print(f"    {stage_name:>10s}: {energies[stage_name]:12.2f} eV "
                      f"({time.time() - t0:.1f}s)")
            except Exception as exc:  # noqa: BLE001
                warnings.warn(
                    f"DFTB+ single-point failed at stage {stage_name!r}: {exc!s}\n"
                    "  This is common for the Voronoi stage (close-pair overlaps).",
                )
                energies[stage_name] = None
        # Reuse the relaxed-step energy we already captured during the
        # optimizer.  This avoids a redundant SCC, and importantly it
        # avoids a second SCC call on positions that the optimizer
        # may have left in a borderline-divergent state.
        energies["dftb_relax"] = last_dftb_energy
        if last_dftb_energy is not None:
            print(f"    {'dftb_relax':>10s}: {last_dftb_energy:12.2f} eV")
        else:
            print(f"    {'dftb_relax':>10s}: (no convergent energy captured)")

    # Stage artefacts dict
    stage_atoms = {
        "voronoi": atoms_voronoi,
        "orient": atoms_orient,
        "fire": atoms_fire,
        "dftb_relax": atoms_dftb,
    }

    # Per-stage Si–O peak summary
    summary = {"box_angstrom": float(box), "n_atoms": len(atoms_voronoi),
               "timings_s": timings, "regime": regime}
    for stage_name, atoms in stage_atoms.items():
        peak, mean, std, n = _measure_si_o_bond(atoms)
        summary[stage_name] = dict(
            si_o_peak=peak, si_o_mean=mean, si_o_std=std, n_si_o_bonds=n,
        )

    # ----- write artefacts -----
    write(str(OUT_DIR / f"{regime}_traj.xyz"),
          list(stage_atoms.values()),
          format="extxyz")
    with open(OUT_DIR / f"{regime}_energies.json", "w") as f:
        json.dump(energies, f, indent=2)
    with open(OUT_DIR / f"{regime}_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    _plot_gr_stack(stage_atoms, regime, OUT_DIR / f"{regime}_gr.png")
    _plot_bond_hist(stage_atoms, regime, OUT_DIR / f"{regime}_bond_hist.png")
    _plot_angle_hist(stage_atoms, regime, OUT_DIR / f"{regime}_angle_hist.png")

    print(f"  wrote artefacts to {OUT_DIR.relative_to(REPO_ROOT)}/")
    return summary


# --------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--regime", choices=list(SIO2_REGIMES.keys()) + ["all"],
        default="all", help="Which regime to run (default: all three).",
    )
    p.add_argument(
        "--box", type=float, default=15.0,
        help="Cubic cell side length in \xc5 (default 15, ~250 atoms; "
             "bumping to 20 quadruples DFTB+ wallclock).",
    )
    p.add_argument(
        "--rng-seed", type=int, default=2026,
        help="RNG seed for the Voronoi tile.",
    )
    p.add_argument(
        "--skip-dftb", action="store_true",
        help="Skip the DFTB+ relax + energy calculations (sanity-check run).",
    )
    args = p.parse_args()

    _setup_paths()

    if not args.skip_dftb:
        ok, msg = _check_dftb_available()
        if not ok:
            print("DFTB+ check failed:\n  " + msg.replace("\n", "\n  "))
            print("\nRe-run with --skip-dftb to test the tricor part only.")
            return 2

    regimes_to_run = (
        list(SIO2_REGIMES.keys()) if args.regime == "all" else [args.regime]
    )
    all_summaries = {}
    for name in regimes_to_run:
        try:
            all_summaries[name] = _run_pipeline(
                name, SIO2_REGIMES[name], args.box, args.rng_seed,
                skip_dftb=args.skip_dftb,
            )
        except Exception as exc:  # noqa: BLE001
            print(f"\n!! {name} failed: {exc.__class__.__name__}: {exc}")
            import traceback
            traceback.print_exc()
            all_summaries[name] = {"error": str(exc)}

    # Roll-up table for the index page
    with open(OUT_DIR / "index_summary.json", "w") as f:
        json.dump(all_summaries, f, indent=2)
    print(f"\nWrote roll-up to {OUT_DIR / 'index_summary.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

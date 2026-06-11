"""Regenerate the MACE-MP0 refinement example artefacts for the
``docs/examples_mace/`` pages — for ALL materials.

For each (material, regime) this script runs a four-stage pipeline at
40³ Å:

  1. Voronoi tile        (cell.generate(num_steps=0))
  2. Orientation refine  (cell.refine_initial_orientations,
                          capture_trajectory=True → interactive movie)
  3. Pre-MACE cleanup    (bond_relax(80) + enforce_hard_core(40))
  4. MACE+wall relax     (ASE LBFGS + mace.calculators.mace_mp +
                          MinDistanceWallCalculator, per-step capture)

MACE single-point energies are taken at every captured frame — a
subsample of the orient accepts and every LBFGS step — so the
combined energy plot (eV/atom) covers the whole refinement and the
regimes can be compared by relative stability.

Materials & regime axes
-----------------------
  copper / silicon / silicon_dioxide / strontium_titanate
      disorder axis:  liquid · amorphous · SRO · MRO · LRO · nanocrystalline
  carbon
      sp axis:        sp2_nc · mixed_nc · sp3_nc   (graphite ↔ diamond)

Per-material, per-regime artefacts land in
``docs/_static/mace/<material>/``.

Usage:
  python scripts/regen_mace_examples.py                       # everything
  python scripts/regen_mace_examples.py --material copper
  python scripts/regen_mace_examples.py --material silicon_dioxide --regime sro
  python scripts/regen_mace_examples.py --box 20.0            # smaller cells
  python scripts/regen_mace_examples.py --skip-mace           # tricor stages only
  python scripts/regen_mace_examples.py --steps 40 --no-movies
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
# Paths + global config
# --------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[1]
TRICOR_SRC = REPO_ROOT.parent / "tricor" / "src"
STRUCTURES = REPO_ROOT / "docs" / "structures"
OUT_ROOT = REPO_ROOT / "docs" / "_static" / "mace"

MACE_MODEL = "medium-mpa-0"
MACE_DEVICE = os.environ.get("MACE_DEVICE", "cpu")  # MPS lacks float64
MACE_DTYPE = "float32"

LBFGS_MAXSTEP = 0.2
LBFGS_FMAX = 1e-8     # tiny so the step cap is the real stop
LBFGS_STEPS = 50

# High-temperature MACE molecular dynamics for the liquid regime.
# Langevin NVT at the material's melting point differentiates the
# liquid (a disordered melt) from the energy-minimised amorphous
# structure.
MD_TEMP_FACTOR = 1.0
MELTING_POINT_K = {
    "copper": 1358.0,
    "silicon": 1687.0,
    "silicon_dioxide": 1986.0,
    "strontium_titanate": 2353.0,
}
MD_TIMESTEP_FS = 2.0
MD_FRICTION = 0.02
MD_STEPS = 80

# Orientation refinement (re-runs the full grain assembly per trial).
ORIENT_AMPLITUDES = (30.0, 12.0, 5.0)
ORIENT_TRIALS = 12
ORIENT_ROUNDS = 1
ORIENT_BUDGET_S = 400.0

BOND_RELAX_N_ITER = 80
BOND_RELAX_MAX_STEP = 0.1
HARD_CORE_N_ITER = 40

WALL_K = 1000.0
WALL_EXPONENT = 4
WALL_MARGIN = 0.0

# Cap on captured frames written into each interactive movie (keeps
# the HTML small).  Frames are subsampled uniformly.
MOVIE_MAX_FRAMES = 24
# Cap on orient-trajectory frames scored with MACE for the energy plot.
ORIENT_SCORE_MAX_FRAMES = 20


# --------------------------------------------------------------------
# Material registry
# --------------------------------------------------------------------
# Each material declares how to build the reference crystal, its
# regime ladder (grain_size / displacement_sigma / spring weights —
# stripped of num_steps because the MACE pipeline tiles with
# num_steps=0 and never FIREs), the primary bond pair + range used for
# the bond-length histogram, the central/neighbour species for the
# angle distributions, and the polyhedra used in the movie viewer.
#
# Regime params mirror ``scripts/regen_static_full.py`` so the MACE
# pages line up with the static / refined / DFTB+ panels.

def _bulk(symbol, structure, a):
    from ase.build import bulk
    return lambda: bulk(symbol, structure, a=a)


def _cif(name):
    from ase.io import read
    return lambda: read(str(STRUCTURES / name))


_DISORDER = ("liquid", "amorphous", "sro", "mro", "lro", "nanocrystalline")

MATERIALS = {
    "copper": dict(
        title="Cu", builder=_bulk("Cu", "fcc", 3.615),
        axis="disorder",
        bond=(29, 29, 2.0, 3.3),        # Za, Zb, r_hist_lo, r_hist_hi
        bond_cut=3.3,
        angles=[(29, 29, "Cu–Cu–Cu", 30, 180)],   # center Z, nbr Z, label, lo, hi
        gr_pairs=[(29, 29)],
        viz=dict(cuboctahedra=dict(center_symbol="Cu", vertex_symbol="Cu"),
                 cuboctahedra_color=(0.85, 0.45, 0.20),
                 cuboctahedra_opacity=0.22),
        regimes={
            "liquid":          dict(grain_size=None, displacement_sigma=0.03, bond_weight=3.0, angle_weight=0.0, repulsion_weight=1.5, hard_core_scale=0.95, nonbond_push_scale=1.00, mace_mode="md"),
            "amorphous":       dict(grain_size=None, displacement_sigma=0.03, bond_weight=3.0, angle_weight=0.0, repulsion_weight=1.5, hard_core_scale=0.95, nonbond_push_scale=1.00),
            "sro":             dict(grain_size=12.0, displacement_sigma=0.03, bond_weight=3.5, angle_weight=0.0, repulsion_weight=1.6, hard_core_scale=0.96, nonbond_push_scale=1.00),
            "mro":             dict(grain_size=18.0, displacement_sigma=0.025, bond_weight=4.0, angle_weight=0.0, repulsion_weight=1.7, hard_core_scale=0.97, nonbond_push_scale=1.00),
            "lro":             dict(grain_size=26.0, displacement_sigma=0.02, bond_weight=4.5, angle_weight=0.0, repulsion_weight=1.9, hard_core_scale=0.99, nonbond_push_scale=1.00),
            "nanocrystalline": dict(grain_size=35.0, displacement_sigma=0.01, bond_weight=5.0, angle_weight=0.0, repulsion_weight=2.0, hard_core_scale=1.00, nonbond_push_scale=1.00),
        },
    ),
    "silicon": dict(
        title="Si", builder=_bulk("Si", "diamond", 5.431),
        axis="disorder",
        bond=(14, 14, 2.0, 2.9),
        bond_cut=2.9,
        angles=[(14, 14, "Si–Si–Si", 60, 180)],
        gr_pairs=[(14, 14)],
        viz=dict(tetrahedra=dict(center_symbol="Si", vertex_symbol="Si",
                                 bond_length_tol=0.10, angle_tol_deg=18.0),
                 tetrahedra_color=(0.35, 0.45, 0.95), tetrahedra_opacity=0.45),
        regimes={
            "liquid":          dict(grain_size=None, displacement_sigma=0.12, bond_weight=0.6, angle_weight=0.20, repulsion_weight=1.3, hard_core_scale=0.86, nonbond_push_scale=0.45, mace_mode="md"),
            "amorphous":       dict(grain_size=None, displacement_sigma=0.12, bond_weight=0.6, angle_weight=0.20, repulsion_weight=1.3, hard_core_scale=0.86, nonbond_push_scale=0.45),
            "sro":             dict(grain_size=8.0,  displacement_sigma=0.06, bond_weight=1.5, angle_weight=0.5, repulsion_weight=1.8, hard_core_scale=0.91, nonbond_push_scale=0.60),
            "mro":             dict(grain_size=12.0, displacement_sigma=0.04, bond_weight=2.0, angle_weight=0.8, repulsion_weight=2.2, hard_core_scale=0.93, nonbond_push_scale=0.75),
            "lro":             dict(grain_size=15.0, displacement_sigma=0.035, bond_weight=2.4, angle_weight=1.0, repulsion_weight=2.3, hard_core_scale=0.93, nonbond_push_scale=0.85),
            "nanocrystalline": dict(grain_size=20.0, displacement_sigma=0.02, bond_weight=2.4, angle_weight=1.0, repulsion_weight=2.3, hard_core_scale=0.95, nonbond_push_scale=0.90),
        },
    ),
    "silicon_dioxide": dict(
        title="SiO₂", builder=_cif("SiO2.cif"),
        axis="disorder",
        bond=(14, 8, 1.3, 1.9),
        bond_cut=1.9,
        angles=[(14, 8, "O–Si–O", 60, 180), (8, 14, "Si–O–Si", 80, 180)],
        gr_pairs=[(14, 8), (8, 8), (14, 14)],
        viz=dict(tetrahedra=dict(center_symbol="Si", vertex_symbol="O"),
                 tetrahedra_color=(0.28, 0.62, 0.95), tetrahedra_opacity=0.42),
        regimes={
            "liquid":          dict(grain_size=None, displacement_sigma=0.012, bond_weight=1.55, angle_weight=1.25, repulsion_weight=1.25, hard_core_scale=0.81, nonbond_push_scale=0.7, mace_mode="md"),
            "amorphous":       dict(grain_size=12.0, displacement_sigma=0.012, bond_weight=1.55, angle_weight=1.25, repulsion_weight=1.25, hard_core_scale=0.81, nonbond_push_scale=0.7),
            "sro":             dict(grain_size=15.0, displacement_sigma=0.010, bond_weight=1.65, angle_weight=1.35, repulsion_weight=1.3, hard_core_scale=0.82, nonbond_push_scale=0.72),
            "mro":             dict(grain_size=20.0, displacement_sigma=0.008, bond_weight=1.65, angle_weight=1.35, repulsion_weight=1.3, hard_core_scale=0.82, nonbond_push_scale=0.72),
            "lro":             dict(grain_size=26.0, displacement_sigma=0.006, bond_weight=1.65, angle_weight=1.35, repulsion_weight=1.3, hard_core_scale=0.82, nonbond_push_scale=0.72),
            "nanocrystalline": dict(grain_size=35.0, displacement_sigma=0.003, bond_weight=1.65, angle_weight=1.35, repulsion_weight=1.3, hard_core_scale=0.82, nonbond_push_scale=0.72),
        },
    ),
    "strontium_titanate": dict(
        title="SrTiO₃", builder=_cif("SrTiO3.cif"),
        axis="disorder",
        bond=(22, 8, 1.5, 2.4),         # Ti–O octahedral bond
        bond_cut=2.4,
        angles=[(22, 8, "O–Ti–O", 60, 180)],
        gr_pairs=[(22, 8), (38, 8), (8, 8)],
        viz=dict(octahedra=dict(center_symbol="Ti", vertex_symbol="O"),
                 octahedra_color=(0.95, 0.55, 0.25), octahedra_opacity=0.42),
        angle_triplets=[("Ti", "O", "O"), ("O", "Ti", "Ti")],
        regimes={
            "liquid":          dict(grain_size=None, displacement_sigma=0.008, bond_weight=0.50, angle_weight=0.4, repulsion_weight=1.1, hard_core_scale=1.10, nonbond_push_scale=0.65, mace_mode="md"),
            "amorphous":       dict(grain_size=None, displacement_sigma=0.008, bond_weight=0.50, angle_weight=0.4, repulsion_weight=1.1, hard_core_scale=1.10, nonbond_push_scale=0.65),
            "sro":             dict(grain_size=14.0, displacement_sigma=0.005, bond_weight=1.0, angle_weight=0.7, repulsion_weight=1.2, hard_core_scale=1.10, nonbond_push_scale=0.75),
            "mro":             dict(grain_size=22.0, displacement_sigma=0.002, bond_weight=1.0, angle_weight=0.7, repulsion_weight=1.2, hard_core_scale=1.10, nonbond_push_scale=0.75),
            "lro":             dict(grain_size=28.0, displacement_sigma=0.0015, bond_weight=1.0, angle_weight=0.7, repulsion_weight=1.2, hard_core_scale=1.10, nonbond_push_scale=0.75),
            "nanocrystalline": dict(grain_size=35.0, displacement_sigma=0.001, bond_weight=1.0, angle_weight=0.7, repulsion_weight=1.2, hard_core_scale=1.10, nonbond_push_scale=0.75),
        },
    ),
    "carbon": dict(
        title="C", axis="sp",
        bond=(6, 6, 1.2, 1.7),
        bond_cut=1.8,
        angles=[(6, 6, "C–C–C", 80, 180)],
        gr_pairs=[(6, 6)],
        # carbon viz is per-regime (sp²→triangles, sp³→tetrahedra) —
        # resolved in _carbon_viz().
        sp_sources=dict(
            graphite=_cif("C_graphite.cif"),
            diamond=_cif("C_diamond.cif"),
        ),
        regimes={
            # weight tuples (graphite, diamond); grain 18, strong springs.
            "sp2_nc":   dict(grain_size=18.0, displacement_sigma=0.02, w_graphite=1.0, w_diamond=0.0, bond_weight=2.5, angle_weight=1.2, repulsion_weight=2.0, hard_core_scale=0.92, nonbond_push_scale=0.85),
            "mixed_nc": dict(grain_size=18.0, displacement_sigma=0.02, w_graphite=0.5, w_diamond=0.5, bond_weight=2.5, angle_weight=1.2, repulsion_weight=2.0, hard_core_scale=0.92, nonbond_push_scale=0.85),
            "sp3_nc":   dict(grain_size=18.0, displacement_sigma=0.02, w_graphite=0.0, w_diamond=1.0, bond_weight=2.5, angle_weight=1.2, repulsion_weight=2.0, hard_core_scale=0.92, nonbond_push_scale=0.85),
        },
    ),
}


def _carbon_viz(regime):
    if regime == "sp2_nc":
        return dict(polyhedra_groups=[dict(
            kind="triangles", center_symbol="C", vertex_symbol="C",
            bond_length=1.42, bond_length_tol=0.10, angle_tol_deg=15.0,
            color=(0.20, 0.65, 0.30), opacity=0.55)])
    if regime == "sp3_nc":
        return dict(tetrahedra=dict(center_symbol="C", vertex_symbol="C",
                                    bond_length=1.54, bond_length_tol=0.10,
                                    angle_tol_deg=15.0),
                    tetrahedra_color=(0.25, 0.35, 0.85), tetrahedra_opacity=0.45)
    return dict(polyhedra_groups=[
        dict(kind="triangles", center_symbol="C", vertex_symbol="C",
             bond_length=1.42, bond_length_tol=0.06, angle_tol_deg=5.0,
             color=(0.20, 0.65, 0.30), opacity=0.55),
        dict(kind="tetrahedra", center_symbol="C", vertex_symbol="C",
             bond_length=1.54, bond_length_tol=0.10, angle_tol_deg=15.0,
             color=(0.25, 0.35, 0.85), opacity=0.45),
    ])


REGIME_TITLES = {
    "liquid": "Liquid", "amorphous": "Amorphous", "sro": "SRO",
    "mro": "MRO", "lro": "LRO", "nanocrystalline": "Nanocrystalline",
    "sp2_nc": "sp² nanocrystalline", "mixed_nc": "Mixed sp²/sp³",
    "sp3_nc": "sp³ nanocrystalline",
}


# --------------------------------------------------------------------
# Setup
# --------------------------------------------------------------------

def _setup_paths() -> None:
    if str(TRICOR_SRC) not in sys.path:
        sys.path.insert(0, str(TRICOR_SRC))
    sys.path.insert(0, str(Path(__file__).parent))   # for _wall_calculator


_MACE_CALC = None


def _load_mace_calc():
    global _MACE_CALC
    if _MACE_CALC is not None:
        return _MACE_CALC
    from mace.calculators import mace_mp
    print(f"  loading mace_mp({MACE_MODEL!r}, device={MACE_DEVICE!r}) ...",
          flush=True)
    t0 = time.time()
    _MACE_CALC = mace_mp(model=MACE_MODEL, device=MACE_DEVICE,
                         default_dtype=MACE_DTYPE)
    print(f"    loaded in {time.time()-t0:.1f}s", flush=True)
    return _MACE_CALC


def _single_point_energy(atoms, calc) -> float:
    a = atoms.copy()
    a.calc = calc
    return float(a.get_potential_energy())


def _subsample(seq, max_n):
    """Uniformly subsample a sequence to at most ``max_n`` items,
    always keeping the first and last."""
    n = len(seq)
    if n <= max_n:
        return list(seq), list(range(n))
    idx = np.unique(np.linspace(0, n - 1, max_n).round().astype(int))
    return [seq[i] for i in idx], list(idx)


# --------------------------------------------------------------------
# Generic PBC measurements
# --------------------------------------------------------------------

def _wrapped(atoms):
    pos = atoms.positions.astype(np.float64)
    box = np.diag(atoms.cell.array).astype(np.float64)
    return pos - np.floor(pos / box) * box, box


def _measure_bond(atoms, za, zb, r_lo, r_hi):
    """Bond stats (peak, mean, std, count) for the (za, zb) pair."""
    from scipy.spatial import cKDTree
    pw, box = _wrapped(atoms)
    tree = cKDTree(pw, boxsize=box)
    pairs = tree.query_pairs(r_hi, output_type="ndarray")
    if not len(pairs):
        return 0.0, 0.0, 0.0, 0
    z = atoms.numbers
    zi, zj = z[pairs[:, 0]], z[pairs[:, 1]]
    if za == zb:
        mask = (zi == za) & (zj == za)
    else:
        mask = ((zi == za) & (zj == zb)) | ((zi == zb) & (zj == za))
    delta = pw[pairs[:, 1]] - pw[pairs[:, 0]]
    delta -= np.round(delta / box) * box
    d = np.linalg.norm(delta, axis=1)
    d = d[mask & (d >= r_lo) & (d < r_hi)]
    if not len(d):
        return 0.0, 0.0, 0.0, 0
    dbin = max((r_hi - r_lo) / 120.0, 0.002)
    hist, edges = np.histogram(d, bins=np.arange(r_lo, r_hi, dbin))
    peak = float(edges[hist.argmax()] + dbin / 2)
    return peak, float(d.mean()), float(d.std()), int(len(d))


def _measure_angles(atoms, zc, zn, cutoff):
    """Angle samples (deg) for zn–zc–zn (central atom of species zc)."""
    from scipy.spatial import cKDTree
    pw, box = _wrapped(atoms)
    z = atoms.numbers
    tree = cKDTree(pw, boxsize=box)
    nbrs = {}
    for i, j in tree.query_pairs(cutoff, output_type="ndarray"):
        zi, zj = z[i], z[j]
        if zi == zc and zj == zn:
            nbrs.setdefault(int(i), []).append(int(j))
        elif zj == zc and zi == zn:
            nbrs.setdefault(int(j), []).append(int(i))
        elif zc == zn and zi == zc and zj == zc:
            nbrs.setdefault(int(i), []).append(int(j))
            nbrs.setdefault(int(j), []).append(int(i))

    def ang(c, a, b):
        v1 = pw[a] - pw[c]; v1 -= np.round(v1 / box) * box
        v2 = pw[b] - pw[c]; v2 -= np.round(v2 / box) * box
        cosp = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-12)
        return float(np.degrees(np.arccos(np.clip(cosp, -1.0, 1.0))))

    out = []
    for c, ns in nbrs.items():
        if len(ns) < 2:
            continue
        for k in range(len(ns)):
            for l in range(k + 1, len(ns)):
                out.append(ang(c, ns[k], ns[l]))
    return np.asarray(out)


def _gr_pair(atoms, za, zb, r_max=8.0, dr=0.05):
    from scipy.spatial import cKDTree
    pw, box = _wrapped(atoms)
    z = atoms.numbers
    tree = cKDTree(pw, boxsize=box)
    pairs = tree.query_pairs(r_max, output_type="ndarray")
    delta = pw[pairs[:, 1]] - pw[pairs[:, 0]]
    delta -= np.round(delta / box) * box
    d = np.linalg.norm(delta, axis=1)
    zi, zj = z[pairs[:, 0]], z[pairs[:, 1]]
    if za == zb:
        mask = (zi == za) & (zj == za)
    else:
        mask = ((zi == za) & (zj == zb)) | ((zi == zb) & (zj == za))
    bins = np.arange(0.0, r_max + dr, dr)
    centres = bins[:-1] + dr / 2
    if not mask.any():
        return centres, np.zeros_like(centres)
    h, _ = np.histogram(d[mask], bins=bins)
    return centres, h.astype(np.float64)


# --------------------------------------------------------------------
# Plotting
# --------------------------------------------------------------------

STAGE_LABELS = ["Voronoi", "after orient", "after cleanup", "after MACE"]
STAGE_COLORS = ["#888", "#3a7", "#27a", "#c33"]
ZSYM = {6: "C", 8: "O", 14: "Si", 22: "Ti", 29: "Cu", 38: "Sr"}


def _plot_gr_stack(stage_atoms, mat, regime, out_path):
    import matplotlib.pyplot as plt
    pairs = mat["gr_pairs"]
    fig, axes = plt.subplots(len(pairs), 1, figsize=(7.5, 2.8 * len(pairs)),
                             sharex=True, squeeze=False)
    axes = axes[:, 0]
    for idx, (_, atoms) in enumerate(stage_atoms.items()):
        for ax, (za, zb) in zip(axes, pairs):
            r, h = _gr_pair(atoms, za, zb)
            norm = np.maximum(r * r, 1e-9)
            ax.plot(r, h / norm, color=STAGE_COLORS[idx],
                    label=STAGE_LABELS[idx] if ax is axes[0] else None, lw=1.3)
    for ax, (za, zb) in zip(axes, pairs):
        ax.set_ylabel(f"g({ZSYM.get(za,za)}–{ZSYM.get(zb,zb)}) (a.u.)")
        ax.grid(alpha=0.3)
    axes[0].legend(loc="upper right", fontsize=8)
    axes[-1].set_xlabel("r (\xc5)")
    fig.suptitle(f"{mat['title']} {REGIME_TITLES.get(regime, regime)} — pairwise g(r)")
    fig.tight_layout()
    fig.savefig(out_path, dpi=140, bbox_inches="tight")
    plt.close(fig)


def _plot_bond_hist(stage_atoms, mat, regime, out_path):
    import matplotlib.pyplot as plt
    za, zb, r_lo, r_hi = mat["bond"]
    fig, ax = plt.subplots(figsize=(7.0, 4.0))
    from scipy.spatial import cKDTree
    for idx, (_, atoms) in enumerate(stage_atoms.items()):
        peak, mean, std, n = _measure_bond(atoms, za, zb, r_lo, r_hi)
        pw, box = _wrapped(atoms)
        tree = cKDTree(pw, boxsize=box)
        prs = tree.query_pairs(r_hi, output_type="ndarray")
        z = atoms.numbers
        zi, zj = z[prs[:, 0]], z[prs[:, 1]]
        m = ((zi == za) & (zj == zb)) | ((zi == zb) & (zj == za)) if za != zb \
            else (zi == za) & (zj == za)
        delta = pw[prs[:, 1]] - pw[prs[:, 0]]; delta -= np.round(delta / box) * box
        d = np.linalg.norm(delta, axis=1)
        dm = d[m & (d >= r_lo) & (d < r_hi)]
        ax.hist(dm, bins=np.arange(r_lo, r_hi, 0.01), histtype="step",
                color=STAGE_COLORS[idx],
                label=f"{STAGE_LABELS[idx]}  (⟨r⟩={mean:.3f}\xc5, σ={std:.3f})",
                linewidth=1.4)
    ax.set_xlabel(f"{ZSYM.get(za,za)}–{ZSYM.get(zb,zb)} distance (\xc5)")
    ax.set_ylabel("count")
    ax.set_title(f"{mat['title']} {REGIME_TITLES.get(regime, regime)} — bond length distribution")
    ax.grid(alpha=0.3); ax.legend(fontsize=8, loc="upper right")
    fig.tight_layout(); fig.savefig(out_path, dpi=140, bbox_inches="tight")
    plt.close(fig)


def _plot_angle_hist(stage_atoms, mat, regime, out_path):
    import matplotlib.pyplot as plt
    specs = mat["angles"]
    cut = mat["bond_cut"]
    fig, axes = plt.subplots(1, len(specs), figsize=(5.5 * len(specs), 4.0),
                             squeeze=False)
    axes = axes[0]
    for ax, (zc, zn, label, lo, hi) in zip(axes, specs):
        for idx, (_, atoms) in enumerate(stage_atoms.items()):
            angs = _measure_angles(atoms, zc, zn, cut)
            if angs.size:
                ax.hist(angs, bins=np.arange(lo, hi, 2), histtype="step",
                        color=STAGE_COLORS[idx],
                        label=f"{STAGE_LABELS[idx]} (⟨α⟩={angs.mean():.1f}\xb0)",
                        linewidth=1.4)
        ax.set_xlabel(f"{label} angle (\xb0)"); ax.set_ylabel("count")
        ax.set_title(label); ax.grid(alpha=0.3)
        ax.legend(fontsize=8, loc="upper left")
    fig.suptitle(f"{mat['title']} {REGIME_TITLES.get(regime, regime)} — angle distributions")
    fig.tight_layout(); fig.savefig(out_path, dpi=140, bbox_inches="tight")
    plt.close(fig)


def _plot_energy_curve(orient_energies, mace_energies, n_atoms,
                        E_voronoi, E_cleanup, mat, regime, out_path):
    # The MACE relaxation only, starting from the post-cleanup structure
    # (step 0).  The orientation-refinement and cleanup stages happen on
    # different (pre-cleanup) geometry upstream, so plotting them on the
    # same axis would introduce a spurious jump; they are summarised in
    # the per-stage energy table instead.
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8.5, 4.6))
    pa = lambda E: E / max(n_atoms, 1)
    if mace_energies:
        x = np.arange(len(mace_energies))
        ax.plot(x, [pa(E) for E in mace_energies], "-", color="#c33", lw=1.6)
    label = "MACE molecular dynamics" if regime == "liquid" else "MACE relaxation"
    ax.set_xlabel(f"{label} step")
    ax.set_ylabel("MACE energy (eV / atom)")
    ax.set_title(f"{mat['title']} {REGIME_TITLES.get(regime, regime)}")
    ax.grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(out_path, dpi=140, bbox_inches="tight")
    plt.close(fig)


def _plot_regime_ladder(summaries, mat, out_path):
    """Final MACE eV/atom vs regime — the cross-regime stability plot."""
    import matplotlib.pyplot as plt
    order = [r for r in (_DISORDER if mat["axis"] == "disorder"
                         else ("sp2_nc", "mixed_nc", "sp3_nc"))
             if r in summaries and "energies" in summaries[r]]
    if not order:
        return
    xs = [REGIME_TITLES.get(r, r) for r in order]
    ys = [summaries[r]["energies"]["mace"] / summaries[r]["n_atoms"] for r in order]
    fig, ax = plt.subplots(figsize=(8.0, 4.4))
    ax.plot(range(len(order)), ys, "o-", color="#c33", lw=1.6, markersize=7)
    for i, y in enumerate(ys):
        ax.annotate(f"{y:.3f}", (i, y), textcoords="offset points",
                    xytext=(0, 8), ha="center", fontsize=8)
    ax.set_xticks(range(len(order))); ax.set_xticklabels(xs, rotation=20)
    ax.set_ylabel("final MACE energy (eV / atom)")
    ax.set_title(f"{mat['title']} — relative stability across regimes (MACE-MP0)")
    ax.grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(out_path, dpi=140, bbox_inches="tight")
    plt.close(fig)


def _export_movie_html(cell, frames, output_path, title, viz):
    traj = np.asarray(frames, dtype=np.float32)
    if traj.ndim != 3 or traj.shape[0] == 0:
        return
    cell.export_trajectory_html(str(output_path), title=title,
                                history={"trajectory": traj}, **viz)


class _OverviewCell:
    """Minimal stand-in for export_overview_html (needs .atoms +
    optional ._shell_target so the polyhedra detector uses the same
    per-pair bond length as the per-regime movies)."""
    def __init__(self, atoms, shell_target=None):
        self.atoms = atoms
        self._shell_target = shell_target


def _export_overview(material, mat, out_dir):
    """Interactive grid of every regime's final MACE state, with
    polyhedra.  Reads the final frame of each regime's traj.xyz so it
    always reflects the complete regime set on disk."""
    import tricor as tc
    from ase.io import read
    from tricor.shells import CoordinationShellTarget
    # Build the reference shell target so the overview's polyhedra
    # detector uses the same Ti-O / Si-O bond length as the per-regime
    # movies (auto-detection on a single panel undercounts octahedra).
    if mat["axis"] == "sp":
        ref = mat["sp_sources"]["graphite"]()
    else:
        ref = mat["builder"]()
    shell = CoordinationShellTarget.from_atoms(ref, phi_num_bins=36)
    regime_order = (_DISORDER if mat["axis"] == "disorder"
                    else ("sp2_nc", "mixed_nc", "sp3_nc"))
    pairs = []
    for r in regime_order:
        traj = out_dir / f"{r}_traj.xyz"
        if traj.exists():
            atoms = read(str(traj), index=-1)
            # Wrap atoms back into the cell so the shared overview camera
            # frames the cell (~half-box from centre) rather than the
            # diffused extent of the MD liquid, matching the zoom level
            # of the static-example overviews.
            atoms.wrap()
            pairs.append((_OverviewCell(atoms, shell), REGIME_TITLES.get(r, r)))
    if not pairs:
        return
    # Carbon spans sp² and sp³ grains across the panels, so the overview
    # needs both triangle (sp²) and tetrahedron (sp³) polyhedra — use the
    # mixed viz rather than the last regime's single-phase viz.
    viz = _carbon_viz("mixed_nc") if mat["axis"] == "sp" else mat["viz"]
    cols = 3 if len(pairs) > 3 else len(pairs)
    tc.export_overview_html(
        str(out_dir / "overview.html"), pairs, grid_cols=cols,
        title=f"{mat['title']} — final MACE structures", **viz)
    print(f"  overview HTML: {(out_dir / 'overview.html').stat().st_size/1024:.0f} KB",
          flush=True)


# --------------------------------------------------------------------
# Cell construction
# --------------------------------------------------------------------

def _build_cell(material, mat, regime, kw, box, rng_seed):
    import tricor as tc
    from tricor.shells import CoordinationShellTarget

    if mat["axis"] == "sp":
        # carbon: two grain sources (graphite + diamond)
        atoms_g = mat["sp_sources"]["graphite"]()
        atoms_d = mat["sp_sources"]["diamond"]()
        shell_g = CoordinationShellTarget.from_atoms(atoms_g, phi_num_bins=36)
        shell_d = CoordinationShellTarget.from_atoms(atoms_d, phi_num_bins=36)
        shell = CoordinationShellTarget.from_targets({"sp2": shell_g, "sp3": shell_d})
        cell = tc.Supercell.from_atoms(
            atoms_g, cell_dim_angstroms=(float(box),) * 3,
            r_max=10.0, r_step=0.1, phi_num_bins=36, rng_seed=rng_seed)
        gen = dict(
            grain_size=kw["grain_size"],
            grain_sources=[
                {"atoms": atoms_g, "species_offset": 0, "weight": kw["w_graphite"]},
                {"atoms": atoms_d, "species_offset": 1, "weight": kw["w_diamond"]},
            ],
            displacement_sigma=kw["displacement_sigma"],
            bond_weight=kw["bond_weight"], angle_weight=kw["angle_weight"],
            repulsion_weight=kw["repulsion_weight"],
            hard_core_scale=kw["hard_core_scale"],
            nonbond_push_scale=kw["nonbond_push_scale"],
        )
        return cell, shell, gen

    atoms_ref = mat["builder"]()
    shell = CoordinationShellTarget.from_atoms(atoms_ref, phi_num_bins=36)
    if mat.get("angle_triplets"):
        shell = shell.with_angle_triplets(mat["angle_triplets"])
    cell = tc.Supercell.from_atoms(
        atoms_ref, cell_dim_angstroms=(float(box),) * 3,
        r_max=10.0, r_step=0.1, phi_num_bins=36, rng_seed=rng_seed)
    gen = {k: v for k, v in kw.items() if k != "mace_mode"}
    return cell, shell, gen


def _viz_for(mat, regime):
    return _carbon_viz(regime) if mat["axis"] == "sp" else mat["viz"]


# --------------------------------------------------------------------
# Pipeline
# --------------------------------------------------------------------

def _run_pipeline(material, regime, box, rng_seed, out_dir,
                   skip_mace=False, steps=LBFGS_STEPS, want_movies=True):
    from ase.io import write

    mat = MATERIALS[material]
    kw = mat["regimes"][regime]
    has_orient = kw.get("grain_size") is not None
    print(f"\n=== {material} / {regime}   box {box:.0f}\xb3 \xc5 ===", flush=True)

    cell, shell, gen = _build_cell(material, mat, regime, kw, box, rng_seed)

    timings, energies, stage_atoms = {}, {}, {}

    # stage 1: Voronoi tile
    t0 = time.time()
    cell.generate(shell, num_steps=0, capture_trajectory=False,
                  show_progress=False, **gen)
    timings["voronoi"] = time.time() - t0
    stage_atoms["voronoi"] = cell.atoms.copy()
    n_atoms = len(cell.atoms)
    print(f"  stage 1 (Voronoi):  {timings['voronoi']:5.1f}s  ({n_atoms} atoms)",
          flush=True)

    # stage 2: orientation refinement (capture trajectory)
    orient_history = None
    t0 = time.time()
    if has_orient:
        cell.refine_initial_orientations(
            shell, bond_weight=kw["bond_weight"], angle_weight=kw["angle_weight"],
            repulsion_weight=kw["repulsion_weight"],
            hard_core_scale=kw["hard_core_scale"],
            nonbond_push_scale=kw["nonbond_push_scale"],
            amplitudes_deg=ORIENT_AMPLITUDES,
            trials_per_amplitude_per_grain=ORIENT_TRIALS,
            max_rounds_per_amplitude=ORIENT_ROUNDS,
            time_budget_sec=ORIENT_BUDGET_S,
            capture_trajectory=True, show_progress=False)
        orient_history = cell.refine_initial_orientations_history
    timings["orient"] = time.time() - t0
    stage_atoms["orient"] = cell.atoms.copy()
    n_acc = 0 if orient_history is None else max(
        0, len(orient_history.get("accepted_grain", [])) - 1)
    print(f"  stage 2 (orient):   {timings['orient']:5.1f}s  ({n_acc} accepts)",
          flush=True)

    # stage 3: cleanup
    t0 = time.time()
    cell.bond_relax(shell, n_iter=BOND_RELAX_N_ITER, max_step=BOND_RELAX_MAX_STEP)
    cell.enforce_hard_core(shell, n_iter=HARD_CORE_N_ITER)
    timings["cleanup"] = time.time() - t0
    stage_atoms["cleanup"] = cell.atoms.copy()
    print(f"  stage 3 (cleanup):  {timings['cleanup']:5.1f}s", flush=True)

    # stage 4: MACE+wall relaxation (LBFGS) or high-T MD (liquid)
    mace_mode = kw.get("mace_mode", "lbfgs")
    relax_curve = {"step": [], "energy": [], "fmax": []}
    mace_traj = []
    if skip_mace:
        timings["mace_relax"] = 0.0
        stage_atoms["mace"] = stage_atoms["cleanup"].copy()
    else:
        from _wall_calculator import (MinDistanceWallCalculator,
                                       per_pair_min_from_atoms)
        calc = _load_mace_calc()
        atoms_mace = stage_atoms["cleanup"].copy()
        rmin = per_pair_min_from_atoms(atoms_mace, margin=WALL_MARGIN)
        atoms_mace.calc = MinDistanceWallCalculator(
            calc, rmin, k=WALL_K, exponent=WALL_EXPONENT)
        last_t = [time.time()]

        def _record(it, t0):
            E = float(atoms_mace.get_potential_energy())
            F = float(np.abs(atoms_mace.get_forces()).max())
            relax_curve["step"].append(it)
            relax_curve["energy"].append(E)
            relax_curve["fmax"].append(F)
            mace_traj.append(atoms_mace.positions.astype(np.float32).copy())
            now = time.time()
            if now - last_t[0] > 8.0 or it == steps:
                tag = "MD" if mace_mode == "md" else "LBFGS"
                print(f"    {tag} {it:>3d}: E={E:.2f}  |F|={F:.2f}  "
                      f"({now - t0:.0f}s)", flush=True)
                last_t[0] = now

        t0 = time.time()
        _record(0, t0)
        if mace_mode == "md":
            from ase.md.langevin import Langevin
            from ase.md.velocitydistribution import (
                MaxwellBoltzmannDistribution)
            from ase import units
            temp_K = MD_TEMP_FACTOR * MELTING_POINT_K[material]
            print(f"  MD temperature: {temp_K:.0f} K "
                  f"({MD_TEMP_FACTOR:g} x {MELTING_POINT_K[material]:.0f} K "
                  f"melting point)", flush=True)
            MaxwellBoltzmannDistribution(atoms_mace, temperature_K=temp_K)
            dyn = Langevin(atoms_mace, MD_TIMESTEP_FS * units.fs,
                           temperature_K=temp_K,
                           friction=MD_FRICTION, logfile=None)
            dyn.attach(lambda: _record(dyn.nsteps, t0), interval=1)
            dyn.run(MD_STEPS)
        else:
            from ase.optimize import LBFGS
            opt = LBFGS(atoms_mace, maxstep=LBFGS_MAXSTEP, logfile=None)
            opt.attach(lambda: _record(opt.nsteps, t0), interval=1)
            opt.run(fmax=LBFGS_FMAX, steps=steps)
        timings["mace_relax"] = time.time() - t0
        atoms_mace.calc = None
        stage_atoms["mace"] = atoms_mace
        print(f"  stage 4 (MACE {mace_mode}): {timings['mace_relax']:5.1f}s  "
              f"({len(relax_curve['step'])} steps)", flush=True)

    # per-stage single-point energies
    if not skip_mace:
        calc = _load_mace_calc()
        for name in ("voronoi", "orient", "cleanup", "mace"):
            energies[name] = _single_point_energy(stage_atoms[name], calc)
        print("  E/atom: " + "  ".join(
            f"{n}={energies[n]/n_atoms:.3f}" for n in
            ("voronoi", "orient", "cleanup", "mace")), flush=True)
    else:
        for name in ("voronoi", "orient", "cleanup", "mace"):
            energies[name] = float("nan")

    # MACE energies along a subsample of the orient trajectory
    orient_energies = []
    if (not skip_mace and orient_history is not None
            and len(orient_history.get("trajectory", []))):
        calc = _load_mace_calc()
        probe = stage_atoms["voronoi"].copy()
        probe.calc = calc
        frames, _ = _subsample(list(orient_history["trajectory"]),
                               ORIENT_SCORE_MAX_FRAMES)
        for fr in frames:
            probe.positions = np.asarray(fr, dtype=np.float64)
            orient_energies.append(float(probe.get_potential_energy()))

    # summary
    summary = {
        "material": material, "regime": regime,
        "box_angstrom": float(box), "n_atoms": int(n_atoms),
        "timings_s": timings, "energies": energies,
        "n_orient_accepts": int(n_acc),
        "n_mace_steps": int(len(relax_curve["step"])),
    }
    for name, atoms in stage_atoms.items():
        za, zb, r_lo, r_hi = mat["bond"]
        peak, mean, std, n = _measure_bond(atoms, za, zb, r_lo, r_hi)
        summary[name] = dict(bond_peak=peak, bond_mean=mean,
                             bond_std=std, n_bonds=n)

    # extxyz of the 4 stage endpoints
    write(str(out_dir / f"{regime}_traj.xyz"),
          [stage_atoms[s] for s in ("voronoi", "orient", "cleanup", "mace")],
          format="extxyz")

    # static plots
    _plot_gr_stack(stage_atoms, mat, regime, out_dir / f"{regime}_gr.png")
    _plot_bond_hist(stage_atoms, mat, regime, out_dir / f"{regime}_bond_hist.png")
    _plot_angle_hist(stage_atoms, mat, regime, out_dir / f"{regime}_angle_hist.png")
    if not skip_mace:
        _plot_energy_curve(orient_energies, relax_curve["energy"], n_atoms,
                           energies.get("voronoi"), energies.get("cleanup"),
                           mat, regime, out_dir / f"{regime}_energy_curve.png")

    # interactive movies (subsampled frames)
    if want_movies:
        viz = _viz_for(mat, regime)
        rt = REGIME_TITLES.get(regime, regime)
        # Orientation movie: a different grain re-orients each frame, so
        # per-frame polyhedra cannot be tracked — atoms + bonds only.
        if orient_history is not None and len(orient_history.get("trajectory", [])):
            frames, _ = _subsample(list(orient_history["trajectory"]),
                                   MOVIE_MAX_FRAMES)
            cell.atoms.positions = np.asarray(frames[0], dtype=np.float64)
            _export_movie_html(cell, frames, out_dir / f"{regime}_orient_movie.html",
                               f"{mat['title']} {rt} — orientation refinement",
                               {})
        # MACE movie: continuous relaxation, polyhedra track fine.
        if not skip_mace and len(mace_traj) > 1:
            frames, _ = _subsample(mace_traj, MOVIE_MAX_FRAMES)
            cell.atoms.positions = np.asarray(frames[0], dtype=np.float64)
            _export_movie_html(cell, frames, out_dir / f"{regime}_mace_movie.html",
                               f"{mat['title']} {rt} — MACE", viz)

    # g3 distributions for the physical stages only (cleanup, MACE)
    for stage_name in ("cleanup", "mace"):
        cell.atoms.positions = stage_atoms[stage_name].positions.copy()
        cell.measure_g3(show_progress=False)
        cell.export_g3_html(str(out_dir / f"{regime}_g3_{stage_name}.html"))

    # JSON
    with open(out_dir / f"{regime}_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    with open(out_dir / f"{regime}_energies.json", "w") as f:
        json.dump(energies, f, indent=2)
    with open(out_dir / f"{regime}_relax_curve.json", "w") as f:
        json.dump({**relax_curve, "orient_energies": orient_energies}, f, indent=2)

    # standalone reproducer script
    _emit_standalone_script(material, regime, box, rng_seed,
                            out_dir / f"{regime}_generate.py")

    # leave the cell holding the final MACE positions for the overview
    cell.atoms.positions = stage_atoms["mace"].positions.copy()
    return summary, cell


# --------------------------------------------------------------------
# Standalone reproducer emitter
# --------------------------------------------------------------------

_WALL_BLOCK = '''
# ---- per-pair soft wall (silent above each per-pair minimum) ----
def per_pair_min_from_atoms(atoms, margin=0.0):
    i, j, d = neighbor_list("ijd", atoms, 8.0, self_interaction=False)
    z = atoms.numbers
    out = {}
    lo = np.minimum(z[i], z[j])
    hi = np.maximum(z[i], z[j])
    for za, zb in np.unique(np.stack([lo, hi], 1), axis=0):
        m = (lo == za) & (hi == zb)
        if m.any():
            out[(int(za), int(zb))] = float(d[m].min()) - margin
    return out


class MinDistanceWallCalculator(Calculator):
    implemented_properties = ["energy", "free_energy", "forces", "stress"]

    def __init__(self, base, rmin, k=1000.0, exponent=4):
        super().__init__()
        self.base = base
        self.rmin = {(min(a, b), max(a, b)): float(r) for (a, b), r in rmin.items()}
        self.k = k
        self.n = exponent
        self.maxr = max(self.rmin.values()) if self.rmin else 0.0

    def calculate(self, atoms=None, properties=("energy",),
                  system_changes=all_changes):
        super().calculate(atoms, properties, system_changes)
        self.base.calculate(atoms, properties, system_changes)
        E = float(self.base.results["energy"])
        F = np.asarray(self.base.results["forces"], float).copy()
        if self.maxr > 0:
            i, j, d, D = neighbor_list("ijdD", atoms, self.maxr,
                                       self_interaction=False)
            if len(d):
                z = atoms.numbers
                lo = np.minimum(z[i], z[j])
                hi = np.maximum(z[i], z[j])
                rmp = np.zeros(len(d))
                for (za, zb), r in self.rmin.items():
                    rmp[(lo == za) & (hi == zb)] = r
                act = (rmp > 0) & (d < rmp)
                if act.any():
                    gap = rmp[act] - d[act]
                    E += float(0.5 * np.sum((self.k / self.n) * gap ** self.n))
                    f = self.k * gap ** (self.n - 1)
                    np.add.at(F, i[act], -(f[:, None]) * (D[act] / d[act, None]))
        self.results = dict(energy=E, free_energy=E, forces=F,
                            stress=np.zeros(6))
'''

_RELAX_BLOCK = '''
# ---- cleanup ----
cell.bond_relax(shell, n_iter=BOND_RELAX_N_ITER, max_step=0.1)
cell.enforce_hard_core(shell, n_iter=HARD_CORE_N_ITER)

# ---- MACE + wall ----
calc = mace_mp(model=MACE_MODEL, device="cpu", default_dtype="float32")
atoms = cell.atoms.copy()
atoms.calc = MinDistanceWallCalculator(calc, per_pair_min_from_atoms(atoms),
                                       k=WALL_K, exponent=WALL_EXPONENT)
mace_traj = [atoms.positions.copy()]
opt = LBFGS(atoms, maxstep=0.1, logfile="-")
opt.attach(lambda: mace_traj.append(atoms.positions.copy()), interval=1)
opt.run(fmax=1e-8, steps=STEPS)


def _subsample(seq, n=MOVIE_FRAMES):
    if len(seq) <= n:
        return list(seq)
    idx = np.unique(np.linspace(0, len(seq) - 1, n).round().astype(int))
    return [seq[i] for i in idx]


if orient_traj is not None and len(orient_traj):
    fr = _subsample(list(orient_traj))
    cell.atoms.positions = np.asarray(fr[0])
    cell.export_trajectory_html(
        OUT_PREFIX + "_orient_movie.html",
        title=TITLE + " — orientation refinement",
        history={"trajectory": np.asarray(fr, np.float32)}, **VIZ)

fr = _subsample(mace_traj)
cell.atoms.positions = np.asarray(fr[0])
cell.export_trajectory_html(
    OUT_PREFIX + "_mace_movie.html",
    title=TITLE + " — MACE+wall LBFGS",
    history={"trajectory": np.asarray(fr, np.float32)}, **VIZ)
print("wrote movies for", TITLE)
'''


def _emit_standalone_script(material, regime, box, rng_seed, out_path):
    """Write a self-contained, runnable .py that reproduces this
    (material, regime): builds the cell, runs orient + cleanup +
    MACE+wall, and writes both interactive HTML movies."""
    mat = MATERIALS[material]
    kw = mat["regimes"][regime]
    viz = _viz_for(mat, regime)
    title = f"{mat['title']} {REGIME_TITLES.get(regime, regime)}"

    header = (
        '#!/usr/bin/env python\n'
        f'"""Standalone reproducer: {title} → orient → MACE+wall → movies.\n\n'
        'Generated by scripts/regen_mace_examples.py.  Requires tricor\n'
        '(install from GitHub), torch and mace-torch:\n'
        '    pip install torch "mace-torch>=0.3"\n'
        'Structure CIFs (for oxide / carbon cases) live in the tricor-docs\n'
        'docs/structures/ directory — run from there or edit the path.\n'
        f'    python {material}_{regime}_generate.py\n'
        '"""\n'
        'import numpy as np\n'
        'from ase.optimize import LBFGS\n'
        'from ase.neighborlist import neighbor_list\n'
        'from ase.calculators.calculator import Calculator, all_changes\n'
        'from mace.calculators import mace_mp\n'
        'import tricor as tc\n'
        'from tricor.shells import CoordinationShellTarget\n\n'
        f'BOX = {box!r}\n'
        f'RNG_SEED = {rng_seed!r}\n'
        f'KW = {kw!r}\n'
        f'VIZ = {viz!r}\n'
        f'TITLE = {title!r}\n'
        f'OUT_PREFIX = "{material}_{regime}"\n'
        f'STEPS = {LBFGS_STEPS}\n'
        f'BOND_RELAX_N_ITER = {BOND_RELAX_N_ITER}\n'
        f'HARD_CORE_N_ITER = {HARD_CORE_N_ITER}\n'
        f'MOVIE_FRAMES = {MOVIE_MAX_FRAMES}\n'
        f'MACE_MODEL = {MACE_MODEL!r}\n'
        f'WALL_K = {WALL_K!r}\n'
        f'WALL_EXPONENT = {WALL_EXPONENT!r}\n'
    )

    if mat["axis"] == "sp":
        build = (
            '\n# ---- build cell (carbon: graphite + diamond grain sources) ----\n'
            'from ase.io import read\n'
            'ag = read("C_graphite.cif")\n'
            'ad = read("C_diamond.cif")\n'
            'shell = CoordinationShellTarget.from_targets({\n'
            '    "sp2": CoordinationShellTarget.from_atoms(ag, phi_num_bins=36),\n'
            '    "sp3": CoordinationShellTarget.from_atoms(ad, phi_num_bins=36)})\n'
            'cell = tc.Supercell.from_atoms(ag, cell_dim_angstroms=(BOX,) * 3,\n'
            '    r_max=10.0, r_step=0.1, phi_num_bins=36, rng_seed=RNG_SEED)\n'
            'gen = dict(grain_size=KW["grain_size"],\n'
            '    displacement_sigma=KW["displacement_sigma"],\n'
            '    grain_sources=[\n'
            '        {"atoms": ag, "species_offset": 0, "weight": KW["w_graphite"]},\n'
            '        {"atoms": ad, "species_offset": 1, "weight": KW["w_diamond"]}],\n'
            '    bond_weight=KW["bond_weight"], angle_weight=KW["angle_weight"],\n'
            '    repulsion_weight=KW["repulsion_weight"],\n'
            '    hard_core_scale=KW["hard_core_scale"],\n'
            '    nonbond_push_scale=KW["nonbond_push_scale"])\n'
            'cell.generate(shell, num_steps=0, show_progress=False, **gen)\n'
        )
    else:
        if material in ("copper", "silicon"):
            sym, struct, a = {
                "copper": ("Cu", "fcc", 3.615),
                "silicon": ("Si", "diamond", 5.431),
            }[material]
            ref_line = (f'from ase.build import bulk\n'
                        f'ref = bulk("{sym}", "{struct}", a={a})\n')
        else:
            cif = {"silicon_dioxide": "SiO2.cif",
                   "strontium_titanate": "SrTiO3.cif"}[material]
            ref_line = ('from ase.io import read\n'
                        f'ref = read("{cif}")\n')
        triplet_line = ""
        if mat.get("angle_triplets"):
            triplet_line = f'shell = shell.with_angle_triplets({mat["angle_triplets"]!r})\n'
        build = (
            '\n# ---- build cell ----\n'
            + ref_line
            + 'shell = CoordinationShellTarget.from_atoms(ref, phi_num_bins=36)\n'
            + triplet_line
            + 'cell = tc.Supercell.from_atoms(ref, cell_dim_angstroms=(BOX,) * 3,\n'
            '    r_max=10.0, r_step=0.1, phi_num_bins=36, rng_seed=RNG_SEED)\n'
            'gen = dict(KW)\n'
            'cell.generate(shell, num_steps=0, show_progress=False, **gen)\n'
        )

    orient = (
        '\n# ---- orientation refinement (captures the orient movie) ----\n'
        'orient_traj = None\n'
        'if KW.get("grain_size") is not None:\n'
        '    cell.refine_initial_orientations(\n'
        '        shell, bond_weight=KW["bond_weight"],\n'
        '        angle_weight=KW["angle_weight"],\n'
        '        repulsion_weight=KW["repulsion_weight"],\n'
        '        hard_core_scale=KW["hard_core_scale"],\n'
        '        nonbond_push_scale=KW["nonbond_push_scale"],\n'
        '        capture_trajectory=True, show_progress=False)\n'
        '    orient_traj = cell.refine_initial_orientations_history.get("trajectory")\n'
    )

    out_path.write_text(header + _WALL_BLOCK + build + orient + _RELAX_BLOCK)


# --------------------------------------------------------------------
# Main
# --------------------------------------------------------------------

def main() -> int:
    warnings.filterwarnings("ignore")
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--material", choices=list(MATERIALS) + ["all"], default="all")
    p.add_argument("--regime", default="all")
    p.add_argument("--box", type=float, default=40.0)
    p.add_argument("--rng-seed", type=int, default=2026)
    p.add_argument("--skip-mace", action="store_true")
    p.add_argument("--steps", type=int, default=LBFGS_STEPS)
    p.add_argument("--no-movies", action="store_true")
    args = p.parse_args()

    _setup_paths()

    materials = list(MATERIALS) if args.material == "all" else [args.material]
    for material in materials:
        mat = MATERIALS[material]
        out_dir = OUT_ROOT / material
        out_dir.mkdir(parents=True, exist_ok=True)
        regimes = (list(mat["regimes"]) if args.regime == "all"
                   else [args.regime])
        # Merge with any existing roll-up so single-regime re-runs keep
        # the other regimes' entries (and the overview can still be built).
        summaries = {}
        idx_path = out_dir / "index_summary.json"
        if idx_path.exists():
            try:
                summaries = json.loads(idx_path.read_text())
            except Exception:
                summaries = {}
        for regime in regimes:
            if regime not in mat["regimes"]:
                print(f"!! {material}: no regime {regime!r}, skipping")
                continue
            try:
                summ, _cell = _run_pipeline(
                    material, regime, args.box, args.rng_seed, out_dir,
                    skip_mace=args.skip_mace, steps=args.steps,
                    want_movies=not args.no_movies)
                summaries[regime] = summ
            except Exception as exc:  # noqa: BLE001
                print(f"\n!! {material}/{regime} failed: "
                      f"{exc.__class__.__name__}: {exc}")
                import traceback
                traceback.print_exc()
                summaries[regime] = {"error": str(exc)}
        # cross-regime stability ladder
        if not args.skip_mace:
            try:
                _plot_regime_ladder(summaries, mat,
                                    out_dir / "regime_ladder.png")
            except Exception as exc:  # noqa: BLE001
                print(f"  ladder plot failed: {exc}")
        # interactive polyhedra overview of the final MACE states
        if not args.no_movies:
            try:
                _export_overview(material, mat, out_dir)
            except Exception as exc:  # noqa: BLE001
                print(f"  overview export failed: {exc}")
        with open(idx_path, "w") as f:
            json.dump(summaries, f, indent=2)
        print(f"\nWrote {material} roll-up to {idx_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

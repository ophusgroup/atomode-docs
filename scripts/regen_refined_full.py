"""Regenerate the Refined Examples assets for ALL 5 materials × 3
regimes (Carbon walks the sp²/sp³ axis instead of disorder; the
others walk amorphous → MRO → NC).  Each (material, regime) pair
produces:

  * cost-history PNG          — refine + FIRE phases on one figure
  * refine trajectory HTML    — discrete frames per accepted rotation
  * FIRE trajectory HTML      — continuous atomic relaxation, with
                                material-appropriate polyhedra
                                (cuboctahedra for Cu, tetrahedra for
                                Si / sp³-C / SiO₂, triangles for
                                sp²-C, mixed groups for sp²/sp³ C,
                                octahedra for SrTiO₃).  Bonds are
                                **never** the default — the docs
                                always render polyhedra.
  * three g3 distribution HTMLs — captured at three points on the
                                  pipeline so the algorithmic effect
                                  of each stage is visible:
                                    1. initial (post-build, post-retile)
                                    2. after refine (pre-FIRE)
                                    3. after FIRE (post-thermal-jitter)
"""
from __future__ import annotations
import sys, time
from pathlib import Path
sys.stdout.reconfigure(line_buffering=True)

# Path resolution — see regen_static_full.py for the full rationale.
_REPO_ROOT = Path(__file__).resolve().parents[1]   # tricor-docs/
DOCS_DIR = _REPO_ROOT / "docs"
STATIC_DIR = DOCS_DIR / "_static"
STRUCTURES_DIR = DOCS_DIR / "structures"
sys.path.insert(0, str(_REPO_ROOT / "scripts"))    # find regen_static_full
try:
    import tricor  # noqa: F401
except ImportError:
    sys.path.insert(0, str(_REPO_ROOT.parent / "tricor" / "src"))

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from ase.build import bulk
from ase.io import read
import tricor as tc
from tricor.shells import CoordinationShellTarget
from tricor._resample import _global_cost
import tricor._plotting as _tp


# ---------------------------------------------------------------------
# Polyhedron subsampling — per-detector caps
# ---------------------------------------------------------------------
# The refined cells are at 40 × 40 × 40 Å (8× the volume of the
# 20³ static examples) AND are more crystalline (SO(3) refinement +
# strong-spring FIRE), so the natural detector counts can be 1000+
# polyhedra per cell.  At that density the polyhedra overlap into a
# uniform mush and hide the underlying atoms — the user (correctly)
# sees "I can't see anything" for Cu MRO with 800+ cuboctahedra.
#
# Cap each detector's output at a value that matches the static-
# example visual density at 40³ scale (= 8 × the 20³ static count).
# Cu cuboctahedra are large (12 vertices, ~5 Å across) so cap is
# tighter; smaller polyhedra (tetrahedra, octahedra) can pack denser
# without obscuring the cell.  Carbon-mode caps live in the
# polyhedra_groups path.
SEED = 42

POLY_CAPS = {
    # Caps sync'd with regen_static_full.py so the static-vs-refined
    # comparison is apples-to-apples — the refined cells naturally
    # produce more clean polyhedra (better grain alignment) and a
    # too-tight cap was making the refined panels look LESS dense
    # than static.
    # 2026-05: bumped tetrahedra 2500 → 5000 and triangles 900 → 3500
    # to match the static script after the carbon detector tolerance
    # was loosened from 0.06/5° to 0.10/15°.
    "_detect_cuboctahedra": 1500,
    "_detect_tetrahedra":   5000,
    "_detect_octahedra":     280,
    "_detect_triangles":    3500,
}


def _subsample(polys, cap, seed_offset):
    if len(polys) <= cap:
        return polys
    rng = np.random.default_rng(SEED + seed_offset + len(polys))
    idx = sorted(rng.choice(len(polys), cap, replace=False))
    return [polys[i] for i in idx]


for _name, _cap in POLY_CAPS.items():
    _orig = getattr(_tp, _name)
    def _make(orig, cap, hash_seed):
        def _wrapped(*args, **kwargs):
            return _subsample(orig(*args, **kwargs), cap, hash_seed)
        return _wrapped
    setattr(_tp, _name, _make(_orig, _cap, hash(_name) & 0xFFFF))


OUT = STATIC_DIR / "refined"
TRAJ_DIR = OUT / "trajectories"
G3_DIR = OUT / "g3"
COST_DIR = OUT / "cost_history"
for d in (TRAJ_DIR, G3_DIR, COST_DIR):
    d.mkdir(parents=True, exist_ok=True)


WEIGHTS = dict(
    bond_weight=3.0, angle_weight=1.5, repulsion_weight=3.0,
    hard_core_scale=1.0, nonbond_push_scale=1.0,
)

MATERIALS = {
    "copper": dict(
        atoms=lambda: bulk("Cu", "fcc", a=3.615),
        title="Cu", mode="disorder",
    ),
    "silicon": dict(
        atoms=lambda: bulk("Si", "diamond", a=5.431),
        title="Si", mode="disorder",
    ),
    "carbon": dict(
        atoms_graphite=lambda: read(str(STRUCTURES_DIR / "C_graphite.cif")),
        atoms_diamond=lambda: read(str(STRUCTURES_DIR / "C_diamond.cif")),
        title="C", mode="sp",
    ),
    "silicon_dioxide": dict(
        atoms=lambda: read(str(STRUCTURES_DIR / "SiO2.cif")),
        title="SiO₂", mode="disorder",
    ),
    "strontium_titanate": dict(
        atoms=lambda: read(str(STRUCTURES_DIR / "SrTiO3.cif")),
        title="SrTiO₃", mode="disorder",
    ),
}

SIDE = 40.0
# SEED defined at module top alongside the polyhedron subsampler.

DISORDER_REGIMES = ("amorphous", "MRO", "nanocrystalline")
SP_REGIMES = ("sp2_nc", "mixed_nc", "sp3_nc")

# Post-FIRE thermal jitter (Å) applied just before measuring the
# **final** g3 (after-FIRE).  Models a finite-T snapshot — without
# it the FIRE-quenched cells all look like perfect crystals at T=0K
# and the regimes are visually indistinguishable.  Larger σ for
# smaller-grain (more boundary) regimes; smaller σ for bigger-grain
# (more interior) regimes.  Initial / after-refine g3s are NOT
# jittered — they already carry the stage's natural disorder.
POST_FIRE_THERMAL_SIGMA = {
    "amorphous":       0.18,
    "MRO":             0.11,
    "nanocrystalline": 0.05,
    "sp2_nc":          0.06,
    "mixed_nc":        0.06,
    "sp3_nc":          0.05,
}


def get_polyhedra_kwargs(material: str, regime: str) -> dict:
    """Return ``export_trajectory_html`` kwargs that select the
    natural polyhedron for this (material, regime) pair, using the
    same colours / opacities the static examples use so the two
    sets render consistently side-by-side.

    Default detector tolerances are used everywhere (no loosening)
    — strict tolerances give a sparse, visually clean polyhedron
    population.  Loose ones flood the panel with ~10× as many
    polyhedra and obscure the structure.
    """
    if material == "copper":
        # FCC → cuboctahedra.  Orange + 0.22 opacity to match
        # static examples' cu_mro / cu_lro / cu_nanocrystalline.
        return dict(
            cuboctahedra=dict(center_symbol="Cu", vertex_symbol="Cu"),
            cuboctahedra_color=(0.85, 0.45, 0.20),
            cuboctahedra_opacity=0.22,
        )
    if material == "carbon":
        # sp²-C → triangles (3-coord, 120°), sp³-C → tetrahedra
        # (4-coord, 109.5°).  Detector loosened from 0.06/5° to
        # 0.10/15° (2026-05) to match Si/SiO2 — the strict 5° angle
        # window rejected most boundary atoms even in pure
        # nanocrystalline graphite/diamond (only 16-32% of C passed).
        # FIRE achieves ~10° avg angle deviation; 0.10/15° captures
        # the well-formed-but-slightly-tilted boundary atoms too.
        # Greens for sp², navy for sp³ — distinct so the eye can
        # see the mix in mixed_nc.
        if regime == "sp2_nc":
            return dict(polyhedra_groups=[dict(
                kind="triangles",
                center_symbol="C", vertex_symbol="C",
                bond_length=1.42, bond_length_tol=0.10,
                angle_tol_deg=15.0,
                color=(0.20, 0.65, 0.30), opacity=0.55,
            )])
        if regime == "sp3_nc":
            return dict(
                tetrahedra=dict(
                    center_symbol="C", vertex_symbol="C",
                    bond_length=1.54, bond_length_tol=0.10,
                    angle_tol_deg=15.0,
                ),
                tetrahedra_color=(0.25, 0.35, 0.85),
                tetrahedra_opacity=0.45,
            )
        if regime == "mixed_nc":
            return dict(polyhedra_groups=[
                dict(
                    kind="triangles",
                    center_symbol="C", vertex_symbol="C",
                    bond_length=1.42, bond_length_tol=0.06,
                    angle_tol_deg=5.0,
                    color=(0.20, 0.65, 0.30), opacity=0.55,
                ),
                dict(
                    kind="tetrahedra",
                    center_symbol="C", vertex_symbol="C",
                    bond_length=1.54, bond_length_tol=0.10,
                    angle_tol_deg=15.0,
                    color=(0.25, 0.35, 0.85), opacity=0.45,
                ),
            ])
    if material == "silicon":
        # Same tightened detector as the static regen so liquid Si
        # doesn't pile up false-positive tetrahedra (default 0.15/25°
        # accepts ~20% of liquid as "tetrahedra"; 0.10/18° drops it
        # to a few percent while NC stays > 50%).
        return dict(
            tetrahedra=dict(
                center_symbol="Si", vertex_symbol="Si",
                bond_length_tol=0.10,
                angle_tol_deg=18.0,
            ),
            tetrahedra_color=(0.35, 0.45, 0.95),
            tetrahedra_opacity=0.45,
        )
    if material == "silicon_dioxide":
        return dict(
            tetrahedra=dict(center_symbol="Si", vertex_symbol="O"),
            tetrahedra_color=(0.28, 0.62, 0.95),
            tetrahedra_opacity=0.42,
        )
    if material == "strontium_titanate":
        return dict(
            octahedra=dict(center_symbol="Ti", vertex_symbol="O"),
            octahedra_color=(0.95, 0.55, 0.25),
            octahedra_opacity=0.42,
        )
    return {}


def build_disorder_pipeline(material: str, regime: str):
    """Build the cell + return the same gen_kwargs the static demo uses for
    this (material, regime) pair, so refined and static differ only in
    whether the orientation-refinement pass is applied — not in the
    underlying spring weights / grain sizes / num_steps.

    Falls back to the library ``tc.Supercell.PRESETS`` if the static
    catalogue doesn't have an entry (which currently shouldn't happen
    for the 4 disorder-axis materials × 3 refined regimes).
    """
    # Map refined regime names → static catalogue keys (refined uses
    # bare ``MRO`` while static uses the full ``medium_range_order``).
    static_key = {
        "amorphous":       "amorphous",
        "MRO":             "medium_range_order",
        "nanocrystalline": "nanocrystalline",
    }[regime]

    cfg = MATERIALS[material]
    atoms_ref = cfg["atoms"]()
    shell = CoordinationShellTarget.from_atoms(atoms_ref, phi_num_bins=90)
    # SrTiO3: whitelist the only two single-mode angle triplets, same
    # as the static catalogue.  The Sr-centred O-Sr-O distribution is
    # multi-modal (60° / 90° / 120° / 180° cuboctahedral); a
    # single-target spring through Sr fights the natural geometry and
    # prevents FIRE convergence.  Keep Ti-O-O at 90° (TiO6 octahedron)
    # and O-Ti-Ti at 180° (linear backbone).  ``from_atoms``'s
    # auto_filter has already disabled the lattice-artefact bond
    # pairs (Sr-Sr, Ti-Ti, O-O, Sr-Ti).
    if material == "strontium_titanate":
        shell = shell.with_angle_triplets([
            ("Ti", "O", "O"),
            ("O", "Ti", "Ti"),
        ])
    cell = tc.Supercell.from_atoms(
        atoms_ref, cell_dim_angstroms=(SIDE, SIDE, SIDE),
        r_max=10.0, r_step=0.1, phi_num_bins=90, rng_seed=SEED,
    )

    # Pull the same per-(material, regime) params the static demo
    # uses.  Imported here so a static-catalogue tweak automatically
    # flows through to the refined examples too.  ``regen_static_full``
    # is a sibling module under ``scripts/``; the parent script's
    # path setup already inserted that directory.
    from regen_static_full import DISORDER_REGIMES as _STATIC_REGIMES

    spec = _STATIC_REGIMES.get((material, static_key))
    if spec is not None:
        _, gen_kwargs = spec
        if isinstance(gen_kwargs, str) and gen_kwargs.startswith("preset:"):
            preset = tc.Supercell.PRESETS[gen_kwargs.split(":", 1)[1]].copy()
        else:
            preset = dict(gen_kwargs)
    else:
        # Should never happen for the 4 disorder materials; fall back
        # to the library presets in case someone added a new regime.
        preset = tc.Supercell.PRESETS[regime].copy()
        preset.update(WEIGHTS)

    # Cu uses ``angle_weight = 0`` (multi-modal cuboctahedral angles)
    # so without grain-interior freezing the FIRE quench can't
    # maintain the 12-coord crystalline order.  Same fix as the
    # static catalogue.
    if material == "copper" and preset.get("grain_size") is not None:
        preset["freeze_grain_interiors"] = True

    if regime == "amorphous":
        trials_pa = 12; rounds = 1
    else:
        trials_pa = 50; rounds = 2
    refine_kwargs = dict(
        amplitudes_deg=(30.0, 15.0, 5.0, 2.0),
        trials_per_amplitude_per_grain=trials_pa,
        max_rounds_per_amplitude=rounds,
        cost_function="pair_distance",
        score_cutoff_factor=1.5,
        time_budget_sec=180.0,
        rng_seed=2024,
        capture_trajectory=True,
        show_progress=False,
    )
    return cell, shell, preset, refine_kwargs


def build_sp_pipeline(regime: str):
    cfg = MATERIALS["carbon"]
    atoms_graphite = cfg["atoms_graphite"]()
    atoms_diamond = cfg["atoms_diamond"]()
    shell_sp2 = CoordinationShellTarget.from_atoms(
        atoms_graphite, phi_num_bins=90,
    )
    shell_sp3 = CoordinationShellTarget.from_atoms(
        atoms_diamond, phi_num_bins=90,
    )
    shell = CoordinationShellTarget.from_targets(
        {"sp2": shell_sp2, "sp3": shell_sp3}
    )
    weights_by_regime = {
        "sp2_nc":   (1.00, 0.00),
        "mixed_nc": (0.50, 0.50),
        "sp3_nc":   (0.00, 1.00),
    }
    w_g, w_d = weights_by_regime[regime]
    cell = tc.Supercell.from_atoms(
        atoms_graphite, cell_dim_angstroms=(SIDE, SIDE, SIDE),
        r_max=10.0, r_step=0.1, phi_num_bins=90, rng_seed=SEED,
    )
    # Carbon SP pipeline params 2026-05: synced with the static
    # carbon catalogue so refined and static differ only in whether
    # orientation refinement runs.  Grain 18 + 250 steps + stronger
    # springs (bw=2.5, a=1.2) gives clean sp²/sp³ grain interiors;
    # smaller grain (10) was leaving most atoms at the sp²/sp³ grain
    # boundaries.
    gen_kwargs = dict(
        grain_size=18.0,
        grain_sources=[
            {"atoms": atoms_graphite, "species_offset": 0, "weight": w_g},
            {"atoms": atoms_diamond,  "species_offset": 1, "weight": w_d},
        ],
        num_steps=250,
        bond_weight=2.5, angle_weight=1.2, repulsion_weight=2.0,
        hard_core_scale=0.92, nonbond_push_scale=0.85,
        displacement_sigma=0.02,
    )
    refine_kwargs = dict(
        amplitudes_deg=(30.0, 15.0, 5.0, 2.0),
        trials_per_amplitude_per_grain=50,
        max_rounds_per_amplitude=2,
        cost_function="pair_distance",
        score_cutoff_factor=1.5,
        time_budget_sec=180.0,
        rng_seed=2024,
        capture_trajectory=True,
        show_progress=False,
    )
    return cell, shell, gen_kwargs, refine_kwargs


def replay_components(cell, shell, trajectory, weights_kwargs):
    """Per-frame cost via the smooth ``_global_cost`` (½ k Σ Δ²)
    energy kernel — same one that drives FIRE — so all four cost
    panels are continuous across the refine→FIRE phase boundary.
    The shell_relax-based ``repulsion_loss`` is a count of pairs
    in repulsion masks (discontinuous in position) and produced
    spurious jumps at the boundary.
    """
    w = dict(
        bond_weight=float(weights_kwargs.get("bond_weight", 1.0)),
        angle_weight=float(weights_kwargs.get("angle_weight", 0.5)),
        repulsion_weight=float(weights_kwargs.get("repulsion_weight", 3.0)),
        hard_core_scale=float(weights_kwargs.get("hard_core_scale", 1.0)),
        nonbond_push_scale=float(weights_kwargs.get("nonbond_push_scale", 1.0)),
    )
    saved = cell.atoms.positions.copy()
    bond, angle, rep, total = [], [], [], []
    for frame in trajectory:
        cell.atoms.positions = np.asarray(frame, dtype=np.float64)
        cost = _global_cost(cell, shell, w)
        bond.append(cost["bond"])
        angle.append(cost["angle"])
        rep.append(cost["rep"])
        total.append(cost["total"])
    cell.atoms.positions = saved
    return (np.asarray(total, dtype=np.float64),
            np.asarray(bond, dtype=np.float64),
            np.asarray(angle, dtype=np.float64),
            np.asarray(rep, dtype=np.float64))


def make_cost_plot(out_path, refine_total, refine_bond, refine_angle,
                   refine_rep, fire_total, fire_bond, fire_angle,
                   fire_rep, label):
    n_refine = len(refine_total)
    n_fire = len(fire_total)
    refine_x = np.arange(n_refine)
    fire_x = np.arange(n_refine, n_refine + n_fire)

    fig, axes = plt.subplots(
        4, 1, figsize=(8.0, 5.6), sharex=True,
        gridspec_kw={"hspace": 0.06},
    )
    ax_total, ax_bond, ax_angle, ax_rep = axes
    series = [
        (ax_total, refine_total, fire_total, "total",  "#222222"),
        (ax_bond,  refine_bond,  fire_bond,  "bond",   "#1f77b4"),
        (ax_angle, refine_angle, fire_angle, "angle",  "#2ca02c"),
        (ax_rep,   refine_rep,   fire_rep,   "rep",    "#c2454c"),
    ]
    for ax, yr, yf, ylabel, color in series:
        if n_refine:
            ax.plot(refine_x, yr, lw=1.2, color=color, marker="o",
                    markersize=2.5, markerfacecolor=color)
        if n_fire:
            ax.plot(fire_x, yf, lw=1.0, color=color, alpha=0.7)
        if n_refine and n_fire:
            ax.plot([refine_x[-1], fire_x[0]], [yr[-1], yf[0]],
                    lw=0.5, color=color, alpha=0.5, ls=":")
        ax.set_ylabel(ylabel, fontsize=9)
        ax.tick_params(axis="y", labelsize=8)
        ax.grid(alpha=0.25)

    if n_refine:
        for ax in axes:
            ax.axvline(n_refine - 0.5, lw=0.8, ls="--", color="#888",
                       alpha=0.6)
    ax_rep.set_xlabel(
        "step  (refine accepts → FIRE quench, dashed = phase boundary)",
        fontsize=9,
    )
    ax_total.set_title(f"{label} — refine + FIRE convergence",
                       fontsize=10)
    fig.tight_layout()
    fig.savefig(out_path, dpi=140, bbox_inches="tight")
    plt.close(fig)


def install_synthetic_thermal_history(cell, trajectory, total):
    n = len(trajectory)
    n_atoms = len(cell.atoms)
    cell.thermal_relax_history = dict(
        sweep=np.arange(n, dtype=np.intp),
        T=np.zeros(n),
        cost=total,
        cost_bond=np.zeros(n), cost_angle=np.zeros(n),
        cost_rep=np.zeros(n), cost_restraint=np.zeros(n),
        accept_rate=np.full(n, 1.0),
        step_sigma=np.zeros(n),
        best_cost=np.minimum.accumulate(total),
        trajectory=np.asarray(trajectory, dtype=np.float32),
        atom_cost=np.zeros((n, n_atoms), dtype=np.float32),
        best_positions=trajectory[-1].astype(np.float64),
        best_species_idx=cell._atom_species_index.copy(),
        final_positions=trajectory[-1].astype(np.float64),
        final_species_idx=cell._atom_species_index.copy(),
        T_schedule=np.zeros(n),
    )


def regen_one(material: str, regime: str):
    cfg = MATERIALS[material]
    label = cfg["title"]
    print(f"\n{'=' * 60}")
    print(f"{material} / {regime}")
    print(f"{'=' * 60}", flush=True)
    stem = f"{material}_{regime}"

    if cfg["mode"] == "sp":
        cell, shell, gen_kwargs, refine_kwargs = build_sp_pipeline(regime)
    else:
        cell, shell, gen_kwargs, refine_kwargs = build_disorder_pipeline(material, regime)

    t0 = time.time()
    cell.generate(
        shell,
        refine_orientations=True,
        refine_orientations_kwargs=refine_kwargs,
        capture_trajectory=True,
        show_progress=False,
        **gen_kwargs,
    )
    elapsed = time.time() - t0

    n_atoms = len(cell.atoms)
    # Grain-less amorphous cells (grain_size=None) don't have
    # ``_grain_cells`` set, so use a safe accessor.  Refinement is
    # silently skipped for these cells but the FIRE quench still runs.
    n_grains = len(getattr(cell, "_grain_cells", None) or [])
    # ``refine_initial_orientations_history`` is only set when
    # refinement actually ran (i.e. the cell had grains).  For
    # grain-less amorphous cells, refinement is silently skipped by
    # ``cell.generate(refine_orientations=True, ...)`` and the
    # history attribute is missing — treat that as "no refine
    # trajectory" so we still produce the FIRE-only artefacts.
    refine_hist = getattr(cell, "refine_initial_orientations_history", None)
    n_accepts = (
        int(len(refine_hist["iteration"]) - 1)
        if refine_hist is not None else 0
    )
    fire_hist = cell.shell_relax_history
    n_fire_frames = (
        len(fire_hist.get("trajectory", [])) if fire_hist else 0
    )
    print(f"  {n_atoms} atoms, {n_grains} grains, "
          f"{n_accepts} refine accepts, "
          f"{n_fire_frames} FIRE frames, {elapsed:.1f} s",
          flush=True)

    refine_traj = refine_hist.get("trajectory") if refine_hist else None
    fire_traj = fire_hist.get("trajectory")
    if fire_traj is None:
        print("  WARN: missing FIRE trajectory; skipping HTML", flush=True)
        return
    fire_traj = np.asarray(fire_traj, dtype=np.float32)
    have_refine = refine_traj is not None
    if have_refine:
        refine_traj = np.asarray(refine_traj, dtype=np.float32)

    def _downsample(traj, target=32):
        if len(traj) <= target:
            return traj
        idx = np.linspace(0, len(traj) - 1, target, dtype=int)
        return traj[idx]

    fire_traj_ds = _downsample(fire_traj, 32)
    refine_traj_ds = _downsample(refine_traj, 32) if have_refine else None

    # ── cost replay ──
    ft, fb, fa, fr = replay_components(cell, shell, fire_traj_ds, gen_kwargs)
    if have_refine:
        rt, rb, ra, rr = replay_components(cell, shell, refine_traj_ds, gen_kwargs)
        cost_path = COST_DIR / f"{stem}.png"
        make_cost_plot(cost_path, rt, rb, ra, rr, ft, fb, fa, fr,
                       label=f"{label} {regime}")
        print(f"  cost PNG: {cost_path.stat().st_size / 1024:.0f} KB",
              flush=True)
    else:
        # Grain-less cell — only FIRE happened.  Plot just the FIRE
        # phase so the per-regime page still has a cost trace.
        cost_path = COST_DIR / f"{stem}.png"
        zeros = np.zeros(0, dtype=np.float64)
        make_cost_plot(cost_path, zeros, zeros, zeros, zeros,
                       ft, fb, fa, fr,
                       label=f"{label} {regime} (no grains → FIRE only)")
        print(f"  cost PNG (FIRE-only): "
              f"{cost_path.stat().st_size / 1024:.0f} KB", flush=True)

    # ── refine trajectory HTML — only when we have one ──
    if have_refine:
        install_synthetic_thermal_history(cell, refine_traj_ds, rt)
        refine_traj_path = TRAJ_DIR / f"{stem}_refine.html"
        cell.export_trajectory_html(
            str(refine_traj_path), history="thermal_relax",
            title=f"{label} {regime} — orientation refinement",
        )
        print(f"  refine HTML: "
              f"{refine_traj_path.stat().st_size / 1024:.0f} KB "
              f"({len(refine_traj_ds)} frames)",
              flush=True)
    else:
        # Write a tiny placeholder pointing the per-regime page at
        # the FIRE movie so the iframe doesn't 404.  The simplest
        # placeholder: copy the FIRE HTML in as the "refine" file.
        # The per-regime markdown text already explains this is a
        # FIRE-only run for amorphous regimes.
        import shutil
        refine_traj_path = TRAJ_DIR / f"{stem}_refine.html"
        # Defer until after FIRE export below — we need the FIRE
        # HTML to exist first.
        _need_refine_placeholder = True

    # ── FIRE trajectory HTML — WITH polyhedra ──
    # CRUCIAL: shell_relax restores ``cell.atoms.positions`` to the
    # frame with the lowest *shell_relax loss*, which (because the
    # repulsion term is a discontinuous pair-count) is often the
    # pre-FIRE refinement state for already-clean refined cells —
    # FIRE moves atoms slightly through repulsion thresholds and
    # the count flips a few pairs, raising the loss above frame 0.
    # The polyhedra detector runs against ``cell.atoms.positions``
    # and locks those (centre, vertex) atom indices through the
    # playback.  If we let detection run on the pre-FIRE state but
    # the trajectory's last frame shows the post-FIRE state, the
    # rendered polyhedra connect indices that aren't actually NNs
    # at the displayed positions — exactly the user-visible
    # "polyhedra are connecting the wrong vertices for the final
    # positions" bug.  Force positions to the trajectory's last
    # frame before detection so both agree.
    cell.atoms.positions = np.asarray(fire_traj[-1], dtype=np.float64)
    poly_kwargs = get_polyhedra_kwargs(material, regime)
    install_synthetic_thermal_history(cell, fire_traj_ds, ft)
    fire_traj_path = TRAJ_DIR / f"{stem}_fire.html"
    cell.export_trajectory_html(
        str(fire_traj_path), history="thermal_relax",
        title=f"{label} {regime} — FIRE quench",
        **poly_kwargs,
    )
    poly_kind = (
        list(poly_kwargs)[0] if poly_kwargs else "atoms-only"
    )
    print(f"  fire HTML: "
          f"{fire_traj_path.stat().st_size / 1024:.0f} KB "
          f"({len(fire_traj_ds)} frames, kind={poly_kind})",
          flush=True)

    # If refinement was skipped (no grains), copy the FIRE HTML in as
    # the "refine" placeholder so the per-regime page's two iframes
    # both load — the page text already explains amorphous-with-no-
    # grains skips the SO(3) search.
    if not have_refine:
        import shutil
        refine_traj_path = TRAJ_DIR / f"{stem}_refine.html"
        shutil.copyfile(str(fire_traj_path), str(refine_traj_path))
        print(f"  refine HTML: copied FIRE HTML "
              f"(no grains → refinement skipped)", flush=True)

    # ── 3 g3 distributions: initial / after_refine / after_fire ──
    saved = cell.atoms.positions.copy()
    sigma_post = POST_FIRE_THERMAL_SIGMA.get(regime, 0.0)
    rng = np.random.default_rng(SEED + hash((material, regime)) % 1000)

    if have_refine:
        g3_states = [
            ("initial",      refine_traj[0],   False),
            ("after_refine", refine_traj[-1],  False),
            ("after_fire",   fire_traj[-1],    True),  # apply jitter
        ]
    else:
        # No refinement happened — the "initial" and "after_refine"
        # states are both just the FIRE trajectory's first frame.
        g3_states = [
            ("initial",      fire_traj[0],   False),
            ("after_refine", fire_traj[0],   False),
            ("after_fire",   fire_traj[-1],  True),
        ]
    for tag, frame, apply_jitter in g3_states:
        cell.atoms.positions = np.asarray(frame, dtype=np.float64)
        if apply_jitter and sigma_post > 0:
            cell.atoms.positions += rng.normal(
                0.0, sigma_post, cell.atoms.positions.shape
            )
        cell.measure_g3(show_progress=False)
        g3_path = G3_DIR / f"{stem}_{tag}.html"
        cell.export_g3_html(str(g3_path))
        print(f"  g3 {tag:>12} HTML: "
              f"{g3_path.stat().st_size / 1024:.0f} KB"
              f"{f' (post-FIRE σ={sigma_post:.2f} Å)' if apply_jitter and sigma_post > 0 else ''}",
              flush=True)
    cell.atoms.positions = saved


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--material", default=None)
    parser.add_argument("--regime", default=None)
    args = parser.parse_args()

    if args.material:
        materials = [args.material]
    else:
        materials = list(MATERIALS.keys())

    for material in materials:
        cfg = MATERIALS[material]
        regimes = (
            SP_REGIMES if cfg["mode"] == "sp" else DISORDER_REGIMES
        )
        if args.regime:
            regimes = [args.regime]
        for regime in regimes:
            try:
                regen_one(material, regime)
            except Exception as e:
                print(f"\n  !! FAILED {material}/{regime}: {e!r}",
                      flush=True)
                import traceback
                traceback.print_exc()


if __name__ == "__main__":
    main()

"""Build the per-material before/after overview (2x3 panel) and the
g(r) overlay (3 regimes × {static, refined}) under
``_static/refined/{overview,g2_compare}/<material>.html``.

A and B builds:
  A — ``cell.generate(...)`` static path (no orientation refinement)
  B — ``cell.generate(refine_orientations=True, ...)``

Carbon walks the sp²/sp³ axis (``sp2_nc``, ``mixed_nc``, ``sp3_nc``)
instead of the disorder axis the other materials walk.
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
from ase.build import bulk
from ase.io import read
import tricor as tc
from tricor.shells import CoordinationShellTarget
import tricor._plotting as _tp


# Polyhedron subsampler — see comment in regen_refined_full.py.
# Cap detected polyhedra so the panels don't get flooded.
SEED = 42

# Per-detector caps sync'd with the static regen so the refined
# overview panels render at the same density as the static ones.
POLY_CAPS = {
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
OVERVIEW_DIR = OUT / "overview"
G2_DIR = OUT / "g2_compare"
for d in (OVERVIEW_DIR, G2_DIR):
    d.mkdir(parents=True, exist_ok=True)


WEIGHTS = dict(
    bond_weight=3.0, angle_weight=1.5, repulsion_weight=3.0,
    hard_core_scale=1.0, nonbond_push_scale=1.0,
)

DISORDER_REGIMES = ("amorphous", "MRO", "nanocrystalline")
SP_REGIMES = ("sp2_nc", "mixed_nc", "sp3_nc")
SIDE = 40.0
# SEED defined alongside the polyhedron subsampler.

# Same post-FIRE thermal jitter as regen_refined_full.py — so the
# overview panels match the per-regime g3 distributions visually.
POST_FIRE_THERMAL_SIGMA = {
    "amorphous":       0.18,
    "MRO":             0.11,
    "nanocrystalline": 0.05,
    "sp2_nc":          0.06,
    "mixed_nc":        0.06,
    "sp3_nc":          0.05,
}

MATERIALS = {
    "copper": dict(
        atoms=lambda: bulk("Cu", "fcc", a=3.615),
        polyhedra=None, title="Cu", mode="disorder",
    ),
    "silicon": dict(
        atoms=lambda: bulk("Si", "diamond", a=5.431),
        polyhedra="tetrahedra", title="Si", mode="disorder",
    ),
    "carbon": dict(
        atoms_graphite=lambda: read(str(STRUCTURES_DIR / "C_graphite.cif")),
        atoms_diamond=lambda: read(str(STRUCTURES_DIR / "C_diamond.cif")),
        polyhedra="tetrahedra", title="C", mode="sp",
    ),
    "silicon_dioxide": dict(
        atoms=lambda: read(str(STRUCTURES_DIR / "SiO2.cif")),
        polyhedra="tetrahedra", title="SiO₂", mode="disorder",
    ),
    "strontium_titanate": dict(
        atoms=lambda: read(str(STRUCTURES_DIR / "SrTiO3.cif")),
        polyhedra="octahedra", title="SrTiO₃", mode="disorder",
    ),
}


def build_disorder(material: str, regime: str, refine: bool):
    cfg = MATERIALS[material]
    atoms_ref = cfg["atoms"]()
    shell = CoordinationShellTarget.from_atoms(atoms_ref, phi_num_bins=90)
    # SrTiO3: whitelist the only two single-mode angle triplets
    # (Sr-centred angles are multi-modal cuboctahedral 60/90/120/180°).
    # Same fix as the static catalogue.
    if material == "strontium_titanate":
        shell = shell.with_angle_triplets([
            ("Ti", "O", "O"),
            ("O", "Ti", "Ti"),
        ])
    cell = tc.Supercell.from_atoms(
        atoms_ref, cell_dim_angstroms=(SIDE, SIDE, SIDE),
        r_max=10, r_step=0.1, phi_num_bins=90, rng_seed=SEED,
    )
    # Pull params from the static catalogue so refined-vs-static is
    # apples-to-apples (only difference is whether refinement is run).
    static_key = {
        "amorphous":       "amorphous",
        "MRO":             "medium_range_order",
        "nanocrystalline": "nanocrystalline",
    }[regime]
    # ``regen_static_full`` is a sibling module — the parent script's
    # path setup already inserted scripts/ into sys.path.
    from regen_static_full import DISORDER_REGIMES as _STATIC_REGIMES
    spec = _STATIC_REGIMES.get((material, static_key))
    if spec is not None:
        _, gen_kwargs = spec
        if isinstance(gen_kwargs, str) and gen_kwargs.startswith("preset:"):
            preset = tc.Supercell.PRESETS[gen_kwargs.split(":", 1)[1]].copy()
        else:
            preset = dict(gen_kwargs)
    else:
        preset = tc.Supercell.PRESETS[regime].copy()
        preset.update(WEIGHTS)

    # Cu uses ``angle_weight = 0`` (multi-modal cuboctahedral angles)
    # so without grain-interior freezing the FIRE quench can't
    # maintain crystalline order.  Same fix as the static catalogue.
    if material == "copper" and preset.get("grain_size") is not None:
        preset["freeze_grain_interiors"] = True

    if refine:
        if regime == "amorphous":
            trials_pa = 12; rounds = 1
        else:
            trials_pa = 50; rounds = 2
        cell.generate(
            shell,
            refine_orientations=True,
            refine_orientations_kwargs=dict(
                amplitudes_deg=(30.0, 15.0, 5.0, 2.0),
                trials_per_amplitude_per_grain=trials_pa,
                max_rounds_per_amplitude=rounds,
                cost_function="pair_distance",
                score_cutoff_factor=1.5,
                time_budget_sec=180.0,
                rng_seed=2024,
                show_progress=False,
            ),
            capture_trajectory=True,  # so build() can set positions
                                       # to fire_traj[-1] (see comment
                                       # in build()).
            show_progress=False,
            **preset,
        )
    else:
        cell.generate(shell, capture_trajectory=True,
                      show_progress=False, **preset)

    return cell, shell


def build_sp(regime: str, refine: bool):
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
        r_max=10, r_step=0.1, phi_num_bins=90, rng_seed=SEED,
    )
    # Carbon SP params synced with static (2026-05): grain 18 Å, 250
    # steps, bw=2.5/a=1.2 — matches build_sp_pipeline in
    # regen_refined_full.py.
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
    if refine:
        cell.generate(
            shell,
            refine_orientations=True,
            refine_orientations_kwargs=dict(
                amplitudes_deg=(30.0, 15.0, 5.0, 2.0),
                trials_per_amplitude_per_grain=50,
                max_rounds_per_amplitude=2,
                cost_function="pair_distance",
                score_cutoff_factor=1.5,
                time_budget_sec=180.0,
                rng_seed=2024,
                show_progress=False,
            ),
            capture_trajectory=True,
            show_progress=False,
            **gen_kwargs,
        )
    else:
        cell.generate(shell, capture_trajectory=True,
                      show_progress=False, **gen_kwargs)
    return cell, shell


def build(material: str, regime: str, refine: bool):
    cfg = MATERIALS[material]
    if cfg["mode"] == "sp":
        cell, shell = build_sp(regime, refine)
    else:
        cell, shell = build_disorder(material, regime, refine)
    # CRUCIAL: shell_relax restores ``cell.atoms.positions`` to the
    # frame with lowest count-based loss, which is often pre-FIRE
    # for already-clean refined cells.  Force to the trajectory's
    # last frame so the overview renders the actual FIRE-final
    # geometry (and so the polyhedra detector sees the same).  See
    # detailed comment in regen_refined_full.py.
    fire_hist = getattr(cell, "shell_relax_history", None)
    if fire_hist is not None and "trajectory" in fire_hist:
        traj = fire_hist["trajectory"]
        if traj is not None and len(traj):
            cell.atoms.positions = np.asarray(traj[-1], dtype=np.float64)
    # NB: no post-FIRE thermal jitter here (unlike the per-regime g3
    # generation in regen_refined_full).  The overview shows atomic
    # structure where bond detection wants near-perfect distances.
    cell.label = f"{regime} ({'refined' if refine else 'static'})"
    return cell, shell


def regen_material(material: str):
    cfg = MATERIALS[material]
    label = cfg["title"]
    print(f"\n=== {material} ===", flush=True)

    regimes = SP_REGIMES if cfg["mode"] == "sp" else DISORDER_REGIMES

    cells = []
    g2_pairs = {}
    for regime in regimes:
        for refine in (False, True):
            t0 = time.time()
            cell, _ = build(material, regime, refine)
            tag = "refined" if refine else "static"
            print(f"  {regime:>10} / {tag:<8} "
                  f"{len(cell.atoms)} atoms, "
                  f"{time.time()-t0:.1f} s", flush=True)
            cells.append((cell, f"{regime} ({tag})"))
            g2_pairs[f"{regime} ({tag})"] = cell

    # ── 2x3 overview (top row static, bottom row refined) ──
    ordered = []
    for refine in (False, True):
        for regime in regimes:
            for c, lab in cells:
                tag = "refined" if refine else "static"
                if f"{regime} ({tag})" == lab:
                    ordered.append((c, lab))
                    break

    overview_path = OVERVIEW_DIR / f"{material}.html"
    polyhedra_kw = {}
    if material == "copper":
        # FCC Cu → cuboctahedra.  Default detector tolerances +
        # static-example colour palette so the overview matches the
        # per-regime trajectory rendering.
        polyhedra_kw = dict(
            cuboctahedra=dict(center_symbol="Cu", vertex_symbol="Cu"),
            cuboctahedra_color=(0.85, 0.45, 0.20),
            cuboctahedra_opacity=0.22,
        )
    elif cfg["mode"] == "sp":
        # Carbon walks the sp²/sp³ axis: render BOTH a sp²-trigonal
        # group (3-coord, 120°) and a sp³-tetrahedral group (4-coord,
        # 109.5°) on every panel.  No ``virtual_species`` filter —
        # ``cell._atom_shell_species_index`` gets clobbered by the
        # refinement retile (all atoms re-tag to species 0), so
        # filtering would mislabel half the atoms.  Instead we rely
        # on the angular detectors to discriminate naturally:
        # 3-coord 120° atoms only pass ``_detect_triangles``,
        # 4-coord 109.5° atoms only pass ``_detect_tetrahedra``.
        # Tighten the triangle/tetrahedron angle tolerance to
        # discriminate sp² (120°) from sp³ (109.5°): the default
        # 18° tol overlaps both, so a diamond atom whose 3 nearest
        # neighbours sit at 109.5° gets falsely tagged as sp².
        # 10° tolerance leaves a 1° gap (109.5° → 119.5° rejected
        # for triangles, 99.5° → 119.5° rejected for tets).
        # Detector loosened 2026-05 from 0.06/5° to 0.10/15° — matches
        # the static carbon detector.  The strict 5° angle window
        # rejected most boundary atoms even in pure nanocrystalline
        # graphite/diamond; FIRE achieves ~10° avg angle deviation,
        # so 0.10/15° captures well-formed-but-tilted boundary
        # polyhedra without leaking sp² into sp³ classification.
        polyhedra_kw = dict(
            polyhedra_groups=[
                dict(
                    kind="triangles",
                    center_symbol="C", vertex_symbol="C",
                    angle_tol_deg=15.0,
                    # Graphite C-C bond length (P6₃/mmc, a = 2.467 Å,
                    # in-plane d = a / √3 = 1.424 Å).  Pin it so the
                    # detector doesn't accidentally pick up diamond
                    # atoms whose 3 nearest neighbours sit at the
                    # diamond C-C of 1.54 Å.
                    bond_length=1.42,
                    bond_length_tol=0.10,
                    color=(0.20, 0.65, 0.30),  # green for sp²
                    opacity=0.55,
                ),
                dict(
                    kind="tetrahedra",
                    center_symbol="C", vertex_symbol="C",
                    angle_tol_deg=15.0,
                    # Diamond C-C bond length (Fd-3m, a = 3.567 Å,
                    # d = a √3 / 4 = 1.544 Å).
                    bond_length=1.54,
                    bond_length_tol=0.10,
                    color=(0.25, 0.35, 0.85),  # navy for sp³
                    opacity=0.45,
                ),
            ],
        )
    elif cfg["polyhedra"] == "tetrahedra":
        cv = {
            "silicon": ("Si", "Si"),
            "silicon_dioxide": ("Si", "O"),
        }.get(material, ("Si", "Si"))
        # Static-example palettes: Si tetrahedra use navy
        # (0.35, 0.45, 0.95) at 0.45 opacity; SiO₂ tetrahedra use
        # blue-cyan (0.28, 0.62, 0.95) at 0.42.
        if material == "silicon":
            # Tightened detector to match the per-regime trajectories
            # (default 0.15/25° accepts ~20% of liquid Si as tets).
            polyhedra_kw = dict(
                tetrahedra=dict(
                    center_symbol=cv[0], vertex_symbol=cv[1],
                    bond_length_tol=0.10,
                    angle_tol_deg=18.0,
                ),
                tetrahedra_color=(0.35, 0.45, 0.95),
                tetrahedra_opacity=0.45,
            )
        else:  # silicon_dioxide
            polyhedra_kw = dict(
                tetrahedra=dict(center_symbol=cv[0], vertex_symbol=cv[1]),
                tetrahedra_color=(0.28, 0.62, 0.95),
                tetrahedra_opacity=0.42,
            )
    elif cfg["polyhedra"] == "octahedra":
        polyhedra_kw = dict(
            octahedra=dict(center_symbol="Ti", vertex_symbol="O"),
            octahedra_color=(0.95, 0.55, 0.25),
            octahedra_opacity=0.42,
        )
    else:
        polyhedra_kw = {}

    if cfg["mode"] == "sp":
        subtitle = "sp²-NC · sp²/sp³ mixed · sp³-NC"
    else:
        subtitle = "amorphous · MRO · nanocrystalline"

    tc.export_overview_html(
        str(overview_path), ordered,
        grid_cols=3,
        title=f"{label} — static (top) vs refined (bottom)",
        subtitle=subtitle,
        **polyhedra_kw,
    )
    print(f"  overview HTML: "
          f"{overview_path.stat().st_size / 1024:.0f} KB",
          flush=True)

    # ── g(r) overlay ──
    g2_path = G2_DIR / f"{material}.html"
    tc.export_g2_compare_html(
        g2_pairs, str(g2_path),
        title=f"{label} g(r): static vs refined across regimes",
    )
    print(f"  g2 HTML: {g2_path.stat().st_size / 1024:.0f} KB",
          flush=True)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--material", default=None)
    args = parser.parse_args()

    materials = [args.material] if args.material else list(MATERIALS)
    for material in materials:
        try:
            regen_material(material)
        except Exception as e:
            print(f"!! FAILED {material}: {e!r}", flush=True)
            import traceback; traceback.print_exc()


if __name__ == "__main__":
    main()

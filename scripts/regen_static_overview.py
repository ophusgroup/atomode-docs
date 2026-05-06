"""Regenerate the per-material STATIC overview + g(r) overlay HTMLs
under ``_static/overview/`` and ``_static/g2_compare/``.

Builds all six regimes (per material) at 40 × 40 × 40 Å using the
same per-regime catalogue as regen_static_full.py — the params live
there as the single source of truth.  No orientation refinement;
this is the ``Supercell.generate(...)`` static path.
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
import tricor as tc
import tricor._plotting as _tp

# Reuse the catalogue + cell builders from regen_static_full.
from regen_static_full import (
    DISORDER_REGIMES, CARBON_REGIMES,
    build_disorder, build_carbon,
    POLY_CAPS, _subsample,  # already monkey-patched at import
)


OUT = STATIC_DIR
OVERVIEW_DIR = OUT / "overview"
G2_DIR = OUT / "g2_compare"
for d in (OVERVIEW_DIR, G2_DIR):
    d.mkdir(parents=True, exist_ok=True)


# Per-material panel order (left-to-right, top-to-bottom in the 2×3
# grid).  Disorder axis runs liquid → NC; carbon walks sp²→sp³.
DISORDER_PANELS = (
    "liquid", "amorphous", "short_range_order",
    "medium_range_order", "long_range_order", "nanocrystalline",
)
CARBON_PANELS = (
    "graphite", "sp2_rich", "sp2_leaning",
    "sp3_leaning", "sp3_rich", "diamond",
)
DISORDER_LABELS = {
    "liquid":             "liquid",
    "amorphous":          "amorphous",
    "short_range_order":  "SRO",
    "medium_range_order": "MRO",
    "long_range_order":   "LRO",
    "nanocrystalline":    "nanocrystalline",
}
CARBON_LABELS = {
    "graphite":    "graphite",
    "sp2_rich":    "sp²-rich",
    "sp2_leaning": "sp²-leaning",
    "sp3_leaning": "sp³-leaning",
    "sp3_rich":    "sp³-rich",
    "diamond":     "diamond",
}


def build(material: str, regime: str):
    if material == "carbon":
        cell, shell, gen_kwargs = build_carbon(regime)
    else:
        cell, shell, gen_kwargs = build_disorder(material, regime)
    cell.generate(
        shell, capture_trajectory=True, show_progress=False, **gen_kwargs,
    )
    # Force cell.atoms.positions to fire_traj[-1] so polyhedra
    # detection sees the same geometry the panel renders.  See
    # detailed comment in regen_refined_full.py.
    fire_traj = cell.shell_relax_history.get("trajectory")
    if fire_traj is not None and len(fire_traj):
        cell.atoms.positions = np.asarray(
            fire_traj[-1], dtype=np.float64,
        )
    return cell, shell


def get_overview_polyhedra_kwargs(material: str) -> dict:
    """Material-appropriate overview polyhedra config.  Colors mirror
    the per-regime trajectory rendering."""
    if material == "copper":
        return dict(
            cuboctahedra=dict(center_symbol="Cu", vertex_symbol="Cu"),
            cuboctahedra_color=(0.85, 0.45, 0.20),
            cuboctahedra_opacity=0.22,
        )
    if material == "carbon":
        return dict(
            polyhedra_groups=[
                dict(
                    kind="triangles",
                    center_symbol="C", vertex_symbol="C",
                    bond_length=1.42, bond_length_tol=0.10,
                    angle_tol_deg=15.0,
                    color=(0.20, 0.65, 0.30), opacity=0.55,
                ),
                dict(
                    kind="tetrahedra",
                    center_symbol="C", vertex_symbol="C",
                    bond_length=1.54, bond_length_tol=0.10,
                    angle_tol_deg=15.0,
                    color=(0.25, 0.35, 0.85), opacity=0.45,
                ),
            ],
        )
    if material == "silicon":
        # Same tightened detector as regen_static_full.
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
        # Match the tightened detector used in regen_static_full so
        # the overview panels stay consistent with the per-regime
        # individual pages.  Defaults (0.15/25°) accepted too many
        # distorted SiO4 motifs in amorphous / liquid panels.
        return dict(
            tetrahedra=dict(
                center_symbol="Si", vertex_symbol="O",
                bond_length_tol=0.10,
                angle_tol_deg=18.0,
            ),
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


def regen_material(material: str):
    print(f"\n=== {material} ===", flush=True)
    if material == "carbon":
        panels = CARBON_PANELS
        labels = CARBON_LABELS
    else:
        panels = DISORDER_PANELS
        labels = DISORDER_LABELS

    cells_and_labels = []
    g2_pairs = {}
    for regime in panels:
        t0 = time.time()
        cell, _ = build(material, regime)
        elapsed = time.time() - t0
        label = labels[regime]
        cells_and_labels.append((cell, label))
        g2_pairs[label] = cell
        print(f"  {regime:>20} → {len(cell.atoms):>5} atoms, "
              f"{elapsed:.1f} s", flush=True)

    overview_path = OVERVIEW_DIR / f"{material}.html"
    poly_kw = get_overview_polyhedra_kwargs(material)
    if material == "carbon":
        subtitle = "graphite · sp²-rich · sp²-leaning · sp³-leaning · sp³-rich · diamond"
    else:
        subtitle = "liquid · amorphous · SRO · MRO · LRO · nanocrystalline"
    title_map = {
        "copper": "Cu",
        "silicon": "Si",
        "carbon": "C",
        "silicon_dioxide": "SiO₂",
        "strontium_titanate": "SrTiO₃",
    }
    tc.export_overview_html(
        str(overview_path), cells_and_labels,
        grid_cols=3,
        title=f"{title_map[material]} regimes",
        subtitle=subtitle,
        **poly_kw,
    )
    print(f"  overview HTML: "
          f"{overview_path.stat().st_size / 1024:.0f} KB", flush=True)

    g2_path = G2_DIR / f"{material}.html"
    tc.export_g2_compare_html(
        g2_pairs, str(g2_path),
        title=f"{title_map[material]} g(r) across regimes",
    )
    print(f"  g2 HTML: {g2_path.stat().st_size / 1024:.0f} KB",
          flush=True)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--material", default=None)
    args = parser.parse_args()
    materials = (
        [args.material] if args.material
        else ["copper", "silicon", "carbon",
              "silicon_dioxide", "strontium_titanate"]
    )
    for m in materials:
        try:
            regen_material(m)
        except Exception as e:
            print(f"!! FAILED {m}: {e!r}", flush=True)
            import traceback; traceback.print_exc()


if __name__ == "__main__":
    main()

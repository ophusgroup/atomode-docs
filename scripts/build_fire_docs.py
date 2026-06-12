"""Generate the docs/examples_refined/ markdown tree (Fast FIRE
Refinement) from the artefacts produced by ``regen_fire_examples.py``.

Reads ``docs/_static/fire/<material>/index_summary.json`` and emits:

  docs/examples_refined/index.md
  docs/examples_refined/<material>/index.md
  docs/examples_refined/<material>/<regime>.md

Usage:
  python scripts/build_fire_docs.py
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[1]
STATIC = REPO_ROOT / "docs" / "_static" / "fire"
PAGES = REPO_ROOT / "docs" / "examples_refined"

MATERIAL_ORDER = ["copper", "silicon", "carbon",
                  "silicon_dioxide", "strontium_titanate"]
MATERIAL_TITLE = {
    "copper": "Copper", "silicon": "Silicon", "carbon": "Carbon",
    "silicon_dioxide": "Silicon dioxide",
    "strontium_titanate": "Strontium titanate",
}
DISORDER = ["liquid", "amorphous", "sro", "mro", "lro", "nanocrystalline"]
SP = ["graphite", "sp2_rich", "sp2_leaning",
      "sp3_leaning", "sp3_rich", "diamond"]
REGIME_TITLE = {
    "liquid": "Liquid", "amorphous": "Amorphous", "sro": "SRO",
    "mro": "MRO", "lro": "LRO", "nanocrystalline": "Nanocrystalline",
    "sp2_nc": "sp² nanocrystalline", "mixed_nc": "Mixed sp²/sp³",
    "sp3_nc": "sp³ nanocrystalline",
    "graphite": "Graphite", "sp2_rich": "sp²-rich",
    "sp2_leaning": "sp²-leaning", "sp3_leaning": "sp³-leaning",
    "sp3_rich": "sp³-rich", "diamond": "Diamond",
}
REGIME_BLURB = {
    "liquid": "melt (thermostatted spring-network sampling)",
    "amorphous": "fully disordered, grain-free",
    "sro": "short-range order",
    "mro": "medium-range order",
    "lro": "long-range order",
    "nanocrystalline": "large crystalline grains with amorphous boundaries",
    "sp2_nc": "graphitic (3-coordinate) grains",
    "mixed_nc": "interleaved sp²/sp³ grains",
    "sp3_nc": "diamond-like (4-coordinate) grains",
    "graphite": "nanocrystalline graphite",
    "sp2_rich": "80 % graphite / 20 % diamond grains",
    "sp2_leaning": "60 % graphite / 40 % diamond grains",
    "sp3_leaning": "40 % graphite / 60 % diamond grains",
    "sp3_rich": "20 % graphite / 80 % diamond grains",
    "diamond": "nanocrystalline diamond",
}


def regimes_for(material):
    return SP if material == "carbon" else DISORDER


def _exists(material, regime, suffix):
    return (STATIC / material / f"{regime}_{suffix}").exists()


def _load(material):
    f = STATIC / material / "index_summary.json"
    return json.loads(f.read_text()) if f.exists() else {}


def _iframe(rel, height=560):
    return (f'<iframe src="{rel}" width="100%" height="{height}"\n'
            f'        style="border: 1px solid rgba(0,0,0,0.1); '
            f'border-radius: 6px;" loading="lazy"></iframe>')


def _img(rel, alt):
    return f'```{{image}} {rel}\n:alt: {alt}\n:width: 100%\n```'


def build_regime_page(material, regime, summ):
    mt = MATERIAL_TITLE[material]
    rt = REGIME_TITLE.get(regime, regime)
    rel = f"../../_static/fire/{material}"
    n_atoms = summ.get("n_atoms", "?")
    box = summ.get("box_angstrom", 40.0)
    n_orient = summ.get("n_orient_accepts", 0)

    lines = [f"# {rt}\n"]
    lines.append(
        f"A {box:.0f} Å cubic {mt.lower()} supercell (~{n_atoms} atoms), "
        f"{REGIME_BLURB.get(regime, regime)}.\n")

    if n_orient > 0 and _exists(material, regime, "orient_movie.html"):
        lines.append("## Orientation refinement\n")
        lines.append(_iframe(f"{rel}/{regime}_orient_movie.html") + "\n")

    if _exists(material, regime, "fire_movie.html"):
        lines.append("## FIRE relaxation\n")
        lines.append(_iframe(f"{rel}/{regime}_fire_movie.html") + "\n")

    # summary table
    rows = []
    for key, label in [("voronoi", "Voronoi"), ("orient", "after orient"),
                       ("cleanup", "after cleanup"), ("fire", "after FIRE")]:
        s = summ.get(key)
        if s:
            rows.append((label, s))
    if rows:
        lines.append("| stage | bond mean (Å) | bond σ (Å) |")
        lines.append("|---|---:|---:|")
        for label, s in rows:
            lines.append(f"| {label} | {s['bond_mean']:.3f} "
                         f"| {s['bond_std']:.3f} |")
        if summ.get("mace_sp_eV") is not None and str(n_atoms).isdigit():
            e = summ["mace_sp_eV"] / int(n_atoms)
            lines.append(f"\nMACE-MP0 single point of the final structure: "
                         f"**{e:.3f} eV/atom**.\n")
        else:
            lines.append("")

    if _exists(material, regime, "g3_fire.html"):
        lines.append("## g₃ distribution — after FIRE\n")
        lines.append(_iframe(f"{rel}/{regime}_g3_fire.html", height=480) + "\n")

    if _exists(material, regime, "bond_hist.png"):
        lines.append("## Bond length and angle distributions\n")
        lines.append(_img(f"{rel}/{regime}_bond_hist.png",
                          f"{mt} {rt} bond length distribution"))
        lines.append("")
        if _exists(material, regime, "angle_hist.png"):
            lines.append(_img(f"{rel}/{regime}_angle_hist.png",
                              f"{mt} {rt} angle distributions"))
            lines.append("")
        if _exists(material, regime, "gr.png"):
            lines.append(_img(f"{rel}/{regime}_gr.png",
                              f"{mt} {rt} pairwise g(r)"))
            lines.append("")

    page = PAGES / material / f"{regime}.md"
    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_text("\n".join(lines))


def _plot_ladder(material, summaries):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    order = [r for r in regimes_for(material)
             if r in summaries and isinstance(summaries[r], dict)
             and summaries[r].get("mace_sp_eV") is not None]
    if not order:
        return False
    xs = [REGIME_TITLE.get(r, r) for r in order]
    ys = [summaries[r]["mace_sp_eV"] / summaries[r]["n_atoms"]
          for r in order]
    fig, ax = plt.subplots(figsize=(8.0, 4.4))
    ax.plot(range(len(order)), ys, "o-", color="#c33", lw=1.6, markersize=7)
    for i, y in enumerate(ys):
        ax.annotate(f"{y:.3f}", (i, y), textcoords="offset points",
                    xytext=(0, 8), ha="center", fontsize=8)
    ax.set_xticks(range(len(order)))
    ax.set_xticklabels(xs, rotation=20)
    ax.set_ylabel("MACE-MP0 energy of FIRE result (eV / atom)")
    ax.set_title(f"{MATERIAL_TITLE[material]} — FIRE structures scored "
                 f"with MACE-MP0")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(STATIC / material / "regime_ladder.png", dpi=140,
                bbox_inches="tight")
    plt.close(fig)
    return True


def build_material_index(material, summaries):
    mt = MATERIAL_TITLE[material]
    regs = [r for r in regimes_for(material) if r in summaries
            and isinstance(summaries[r], dict)
            and "error" not in summaries[r]]
    axis = ("sp²/sp³ mixing" if material == "carbon"
            else "amorphous → nanocrystalline")
    lines = [f"# {mt}\n"]
    lines.append(
        f"{mt} supercells (40 × 40 × 40 Å) across the {axis} axis, "
        f"relaxed with the FIRE spring network.\n")

    if (STATIC / material / "overview.html").exists():
        n_panels = len(regs)
        height = 60 + ((n_panels + 2) // 3) * 300
        lines.append("## Final FIRE structures\n")
        lines.append(
            f'<iframe src="../../_static/fire/{material}/overview.html"\n'
            f'        width="100%" height="{height}"\n'
            f'        style="border: 1px solid rgba(0,0,0,0.1); '
            f'border-radius: 6px;" loading="lazy"></iframe>\n')

    if (STATIC / material / "regime_ladder.png").exists():
        lines.append("## Energy across regimes\n")
        lines.append(
            "MACE-MP0 single-point energy of each FIRE-relaxed "
            "structure — directly comparable to the "
            "[MACE refinement](../../examples_mace/" + material +
            "/index.md) ladder.\n")
        lines.append(_img(f"../../_static/fire/{material}/regime_ladder.png",
                          f"{mt} FIRE structures scored with MACE"))
        lines.append("")

    lines.append("## Summary\n")
    lines.append("| regime | atoms | orient accepts | bond σ (Å) "
                 "| MACE SP (eV/atom) |")
    lines.append("|---|---:|---:|---:|---:|")
    for r in regs:
        s = summaries[r]
        na = s.get("n_atoms", 1)
        sp = s.get("mace_sp_eV")
        spv = f"{sp/na:.3f}" if (sp is not None and na) else "—"
        bs = s.get("fire", {}).get("bond_std")
        bsv = f"{bs:.3f}" if bs is not None else "—"
        lines.append(f"| [{REGIME_TITLE.get(r, r)}]({r}.md) | {na} | "
                     f"{s.get('n_orient_accepts', 0)} | {bsv} | {spv} |")
    lines.append("")
    lines.append("## Per-regime pages\n")
    lines.append("```{toctree}\n:maxdepth: 1\n")
    for r in regs:
        lines.append(r)
    lines.append("```")
    page = PAGES / material / "index.md"
    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_text("\n".join(lines))


def build_top_index(available):
    lines = ["# Fast FIRE Refinement\n"]
    lines.append(
        "tricor-generated supercells relaxed with the built-in "
        "[FIRE spring network](../algorithms/fire_relaxation.md).  FIRE "
        "is orders of magnitude faster than "
        "[MACE-MP0 refinement](../examples_mace/index.md) at lower "
        "accuracy, and is the practical option for cells of 100³ Å and "
        "larger (see [cost and convergence]"
        "(../algorithms/fire_relaxation.md#cost-and-convergence)).  "
        "Each final structure is scored with a MACE-MP0 "
        "single point, so the FIRE and MACE pipelines can be compared "
        "directly.\n")
    lines.append("The pipeline per (material, regime) is:\n")
    lines.append("```\n"
                 "1. Voronoi tile          (cell.generate(num_steps=0))\n"
                 "2. Orientation refine    (cell.refine_initial_orientations)\n"
                 "3. Cleanup               (bond_relax + enforce_hard_core)\n"
                 "4. FIRE relaxation       (cell.shell_relax), or\n"
                 "   thermostatted sampling (cell.thermal_relax) for liquid\n"
                 "```\n")
    lines.append(
        "Shell targets are **MACE-calibrated** when the optional "
        "`mace-torch` dependency is installed "
        "(`shell.calibrate_to_mace()`): per-pair bond stiffness, "
        "per-triplet angle stiffness, Morse anharmonicity, and the "
        "hard-core wall are measured from the MACE-MP0 potential on the "
        "reference crystal, which improves accuracy over the hand-tuned "
        "defaults.  Without `mace-torch` the pipeline runs identically "
        "on the registry weights.  Carbon's composite sp²/sp³ target "
        "runs uncalibrated.\n")
    lines.append("## Materials\n")
    lines.append("```{toctree}\n:maxdepth: 1\n")
    for m in MATERIAL_ORDER:
        if m in available:
            lines.append(f"{m}/index")
    lines.append("```")
    (PAGES / "index.md").write_text("\n".join(lines))


def main():
    PAGES.mkdir(parents=True, exist_ok=True)
    available = []
    for material in MATERIAL_ORDER:
        summaries = _load(material)
        keep = set(regimes_for(material))
        ready = {r: s for r, s in summaries.items()
                 if r in keep and isinstance(s, dict) and "error" not in s}
        if not ready:
            continue
        available.append(material)
        mat_dir = PAGES / material
        if mat_dir.exists():
            for md in mat_dir.glob("*.md"):
                if md.stem not in keep and md.stem != "index":
                    md.unlink()
        for regime, summ in ready.items():
            build_regime_page(material, regime, summ)
        _plot_ladder(material, summaries)
        build_material_index(material, summaries)
        print(f"  {material}: {len(ready)} regime pages")
    build_top_index(available)
    print(f"Top index lists {len(available)} materials: "
          f"{', '.join(available)}")


if __name__ == "__main__":
    main()

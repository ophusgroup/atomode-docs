"""Generate the docs/examples_mace/ markdown tree from the artefacts
produced by ``regen_mace_examples.py``.

Reads ``docs/_static/mace/<material>/index_summary.json`` (+ per-regime
summaries) and emits:

  docs/examples_mace/index.md                      (top-level, lists materials)
  docs/examples_mace/<material>/index.md           (regime ladder + toctree)
  docs/examples_mace/<material>/<regime>.md        (movies, energy, g3, bonds)

Only materials/regimes that actually have artefacts on disk get a page,
so this is safe to run mid-batch (it regenerates what's ready).

Usage:
  python scripts/build_mace_docs.py
"""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
STATIC = REPO_ROOT / "docs" / "_static" / "mace"
PAGES = REPO_ROOT / "docs" / "examples_mace"

MATERIAL_ORDER = ["copper", "silicon", "carbon",
                  "silicon_dioxide", "strontium_titanate"]
MATERIAL_TITLE = {
    "copper": "Copper", "silicon": "Silicon", "carbon": "Carbon",
    "silicon_dioxide": "Silicon dioxide",
    "strontium_titanate": "Strontium titanate",
}
DISORDER = ["liquid", "amorphous", "sro", "mro", "lro", "nanocrystalline"]
SP = ["sp2_nc", "mixed_nc", "sp3_nc"]
REGIME_TITLE = {
    "liquid": "Liquid", "amorphous": "Amorphous", "sro": "SRO",
    "mro": "MRO", "lro": "LRO", "nanocrystalline": "Nanocrystalline",
    "sp2_nc": "sp² nanocrystalline", "mixed_nc": "Mixed sp²/sp³",
    "sp3_nc": "sp³ nanocrystalline",
}
REGIME_BLURB = {
    "liquid": "melt (Langevin MD at the melting point)",
    "amorphous": "fully disordered, grain-free",
    "sro": "short-range order",
    "mro": "medium-range order",
    "lro": "long-range order",
    "nanocrystalline": "large crystalline grains with amorphous boundaries",
    "sp2_nc": "graphitic (3-coordinate) grains",
    "mixed_nc": "interleaved sp²/sp³ grains",
    "sp3_nc": "diamond-like (4-coordinate) grains",
}


def regimes_for(material):
    return SP if material == "carbon" else DISORDER


def _exists(material, regime, suffix):
    return (STATIC / material / f"{regime}_{suffix}").exists()


def _load(material):
    f = STATIC / material / "index_summary.json"
    if not f.exists():
        return {}
    return json.loads(f.read_text())


def _movie_iframe(rel, height=560):
    return (f'<iframe src="{rel}" width="100%" height="{height}"\n'
            f'        style="border: 1px solid rgba(0,0,0,0.1); '
            f'border-radius: 6px;" loading="lazy"></iframe>')


def _img(rel, alt):
    return f'```{{image}} {rel}\n:alt: {alt}\n:width: 100%\n```'


def build_regime_page(material, regime, summ):
    mt = MATERIAL_TITLE[material]
    rt = REGIME_TITLE.get(regime, regime)
    static_rel = f"../../_static/mace/{material}"
    n_atoms = summ.get("n_atoms", "?")
    box = summ.get("box_angstrom", 40.0)
    en = summ.get("energies", {})
    has_orient = summ.get("n_orient_accepts", 0) > 0 or _exists(
        material, regime, "orient_movie.html")

    n_orient = summ.get("n_orient_accepts", 0)

    lines = []
    lines.append(f"# {rt}\n")
    lines.append(
        f"A {box:.0f} Å cubic {mt.lower()} supercell (~{n_atoms} atoms), "
        f"{REGIME_BLURB.get(regime, regime)}.\n")
    lines.append(
        f"[`{material}_{regime}_generate.py`]({static_rel}/{regime}_generate.py)"
        f" reproduces this case.\n")

    # orientation movie (grained regimes only)
    if n_orient > 0 and _exists(material, regime, "orient_movie.html"):
        lines.append("## Orientation refinement\n")
        lines.append(_movie_iframe(
            f"{static_rel}/{regime}_orient_movie.html") + "\n")

    # mace movie
    if _exists(material, regime, "mace_movie.html"):
        lines.append("## MACE+wall relaxation\n")
        lines.append(_movie_iframe(
            f"{static_rel}/{regime}_mace_movie.html") + "\n")

    # energy curve + ladder
    if _exists(material, regime, "energy_curve.png"):
        lines.append("## Energy\n")
        lines.append(_img(f"{static_rel}/{regime}_energy_curve.png",
                          f"{mt} {rt} MACE energy per atom"))
        lines.append("")
    if en and en.get("cleanup") is not None and en.get("mace") is not None:
        na = max(int(n_atoms) if str(n_atoms).isdigit() else 1, 1)
        rows = []
        if n_orient > 0 and en.get("orient") is not None:
            rows.append(("after orientation refinement", en["orient"]))
        rows.append(("after cleanup", en["cleanup"]))
        rows.append(("after MACE", en["mace"]))
        lines.append("| stage | E (eV/atom) |")
        lines.append("|---|---:|")
        for label, v in rows:
            lines.append(f"| {label} | {v/na:.3f} |")
        lines.append("")

    # g3 distributions (cleanup + MACE only)
    g3_stages = [s for s in ("cleanup", "mace")
                 if _exists(material, regime, f"g3_{s}.html")]
    if g3_stages:
        lines.append("## g₃ distributions\n")
        for s in g3_stages:
            slabel = {"cleanup": "After cleanup", "mace": "After MACE"}[s]
            lines.append(f"**{slabel}**\n")
            lines.append(_movie_iframe(
                f"{static_rel}/{regime}_g3_{s}.html", height=480) + "\n")

    # bond + angle distributions
    if _exists(material, regime, "bond_hist.png"):
        lines.append("## Bond length and angle distributions\n")
        lines.append(_img(f"{static_rel}/{regime}_bond_hist.png",
                          f"{mt} {rt} bond length distribution"))
        lines.append("")
        if _exists(material, regime, "angle_hist.png"):
            lines.append(_img(f"{static_rel}/{regime}_angle_hist.png",
                              f"{mt} {rt} angle distributions"))
            lines.append("")
        if _exists(material, regime, "gr.png"):
            lines.append(_img(f"{static_rel}/{regime}_gr.png",
                              f"{mt} {rt} pairwise g(r)"))
            lines.append("")

    page = PAGES / material / f"{regime}.md"
    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_text("\n".join(lines))
    return page


def build_material_index(material, summaries):
    mt = MATERIAL_TITLE[material]
    regs = [r for r in regimes_for(material) if r in summaries
            and "error" not in summaries[r]]
    axis = ("sp²/sp³ mixing" if material == "carbon"
            else "amorphous → nanocrystalline")
    lines = [f"# {mt}\n"]
    lines.append(
        f"{mt} supercells (40 × 40 × 40 Å) across the {axis} axis, "
        f"refined with MACE-MP0.\n")

    # interactive overview first; height tracks the number of grid rows
    # (3 panels per row) so a single-row grid isn't padded with blank space
    if (STATIC / material / "overview.html").exists():
        n_panels = len(regs)
        rows = (n_panels + 2) // 3
        height = 60 + rows * 300
        lines.append("## Final MACE structures\n")
        lines.append(
            f'<iframe src="../../_static/mace/{material}/overview.html"\n'
            f'        width="100%" height="{height}"\n'
            f'        style="border: 1px solid rgba(0,0,0,0.1); '
            f'border-radius: 6px;" loading="lazy"></iframe>\n')

    if (STATIC / material / "regime_ladder.png").exists():
        lines.append("## Energy across regimes\n")
        lines.append(_img(f"../../_static/mace/{material}/regime_ladder.png",
                          f"{mt} energy per atom across regimes"))
        lines.append("")

    # summary table
    lines.append("## Summary\n")
    lines.append("| regime | atoms | orient accepts | final E (eV/atom) |")
    lines.append("|---|---:|---:|---:|")
    for r in regs:
        s = summaries[r]
        na = s.get("n_atoms", 1)
        em = s.get("energies", {}).get("mace")
        epa = f"{em/na:.3f}" if em is not None and na else "—"
        lines.append(f"| [{REGIME_TITLE.get(r, r)}]({r}.md) | {na} | "
                     f"{s.get('n_orient_accepts', 0)} | {epa} |")
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
    lines = ["# MACE-MP0 Refinement Examples\n"]
    lines.append(
        "tricor-generated supercells refined with "
        "**[MACE-MP0](https://github.com/ACEsuit/mace)**, the universal "
        "machine-learning interatomic potential trained on the Materials "
        "Project DFT dataset.\n")
    lines.append("The pipeline per (material, regime) is:\n")
    lines.append("```\n"
                 "1. Voronoi tile          (cell.generate(num_steps=0))\n"
                 "2. Orientation refine    (cell.refine_initial_orientations)\n"
                 "3. Pre-MACE cleanup      (bond_relax + enforce_hard_core)\n"
                 "4. MACE+wall relax       (ASE LBFGS, or Langevin MD at\n"
                 "                          the melting point for liquid)\n"
                 "```\n")
    lines.append(
        "A per-pair soft wall (`scripts/_wall_calculator.py`) is added below "
        "each per-pair minimum distance to suppress MACE's near-overlap "
        "basins; it is silent above the minimum.\n")
    lines.append("## Install\n")
    lines.append('```bash\nuv pip install torch "mace-torch>=0.3" matplotlib\n```\n')
    lines.append(
        "The `medium-mpa-0` model (~76 MB) downloads automatically on first "
        "use. Each regime page links a standalone `.py` reproducer.\n")
    lines.append("## Materials\n")
    lines.append("```{toctree}\n:maxdepth: 1\n")
    for m in MATERIAL_ORDER:
        if m in available:
            lines.append(f"{m}/index")
    lines.append("```")
    (PAGES / "index.md").write_text("\n".join(lines))


def _replot_ladder(material, summaries):
    """Regenerate regime_ladder.png from the JSON summaries, honouring
    the current (liquid-free) regime list."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    order = [r for r in regimes_for(material)
             if r in summaries and "energies" in summaries[r]
             and summaries[r]["energies"].get("mace") is not None]
    if not order:
        return
    xs = [REGIME_TITLE.get(r, r) for r in order]
    ys = [summaries[r]["energies"]["mace"] / summaries[r]["n_atoms"]
          for r in order]
    fig, ax = plt.subplots(figsize=(8.0, 4.4))
    ax.plot(range(len(order)), ys, "o-", color="#c33", lw=1.6, markersize=7)
    for i, y in enumerate(ys):
        ax.annotate(f"{y:.3f}", (i, y), textcoords="offset points",
                    xytext=(0, 8), ha="center", fontsize=8)
    ax.set_xticks(range(len(order)))
    ax.set_xticklabels(xs, rotation=20)
    ax.set_ylabel("final MACE energy (eV / atom)")
    ax.set_title(f"{MATERIAL_TITLE[material]} — relative stability across "
                 f"regimes (MACE-MP0)")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(STATIC / material / "regime_ladder.png", dpi=140,
                bbox_inches="tight")
    plt.close(fig)


def main():
    PAGES.mkdir(parents=True, exist_ok=True)
    available = []
    for material in MATERIAL_ORDER:
        summaries = _load(material)
        if not summaries:
            continue
        keep = set(regimes_for(material))
        ready = {r: s for r, s in summaries.items()
                 if r in keep and isinstance(s, dict) and "error" not in s}
        if not ready:
            continue
        available.append(material)
        # Drop any stale per-regime pages no longer in the regime list
        mat_dir = PAGES / material
        if mat_dir.exists():
            for md in mat_dir.glob("*.md"):
                if md.stem not in keep and md.stem != "index":
                    md.unlink()
        for regime, summ in ready.items():
            build_regime_page(material, regime, summ)
        build_material_index(material, summaries)
        _replot_ladder(material, summaries)
        print(f"  {material}: {len(ready)} regime pages")
    build_top_index(available)
    print(f"Top index lists {len(available)} materials: {', '.join(available)}")


if __name__ == "__main__":
    main()

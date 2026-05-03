# Silicon dioxide

SiO₂ cells (40 × 40 × 40 Å) in three disorder regimes — amorphous,
MRO, nanocrystalline — built with
`Supercell.generate(refine_orientations=True)`.

## Static vs refined

Top row is `Supercell.generate()` with the static-relaxation pipeline
only (FIRE quench, no orientation search); bottom row is the same
cell with `refine_orientations=True` enabled — the SO(3) coordinate
search that aligns each grain's lattice to its local environment
before the same final FIRE quench runs.  Drag any panel to orbit;
all six rotate in sync.

<iframe src="../../_static/refined/overview/silicon_dioxide.html"
        width="100%" height="640"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

## g(r) overlay — static vs refined, all 6 cases

Six g(r) curves on a single radial axis: each regime's static and
refined post-FIRE state, overlaid for direct comparison.

<iframe src="../../_static/refined/g2_compare/silicon_dioxide.html"
        width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

## Per-regime trajectories

Click any regime for the orientation-refinement movie, the FIRE
quench movie, the cost trace, and the final-state polyhedra view.

```{toctree}
:maxdepth: 1

amorphous
medium_range_order
nanocrystalline
```

# Carbon

C cells (40 × 40 × 40 Å) walking the **sp² ↔ sp³ axis** rather than
the disorder axis the other materials walk.  Each Voronoi grain is
sampled from either graphite (sp², 3-coordinated, 120°) or diamond
(sp³, 4-coordinated, 109.5°) and the regime sets the mix:

| Regime | w_graphite | w_diamond | character |
|---|---|---|---|
| `sp2_nc`   | 1.00 | 0.00 | nanocrystalline graphite (all sp²) |
| `mixed_nc` | 0.50 | 0.50 | sp²/sp³ mixed nanocrystalline |
| `sp3_nc`   | 0.00 | 1.00 | nanocrystalline diamond (all sp³) |

Every regime is nanocrystalline (`grain_size = 18 Å`); the variable
is the grain chemistry, not the grain size.  Shell-relax weights are
fixed at `bond_weight=2.5, angle_weight=1.2, repulsion_weight=2.0`.
The
composite shell target carries two virtual species (`sp2_C`,
`sp3_C`); each grain's atoms inherit the species index of the master
they came from, so 3-coordinated graphite atoms develop bonds at
120° and 4-coordinated diamond atoms develop bonds at 109.5°
*inside the same cell*.

## Static vs refined

Top row is `Supercell.generate()` with the static-relaxation
pipeline only (FIRE quench, no orientation search); bottom row is
the same cell with `refine_orientations=True` enabled. The SO(3)
coordinate search that aligns each grain's lattice to its local
environment before the same final FIRE quench runs.  Drag any panel
to orbit; all six rotate in sync.

<iframe src="../../_static/refined/overview/carbon.html"
        width="100%" height="640"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

## g(r) overlay: static vs refined, all 6 cases

Six g(r) curves on a single radial axis: each regime's static and
refined post-FIRE state, overlaid for direct comparison.  The pair
dropdown below the plot lets you switch between the sp²-C and
sp³-C channels.

<iframe src="../../_static/refined/g2_compare/carbon.html"
        width="100%" height="480"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

## Per-regime trajectories

Click any regime for the orientation-refinement movie, the FIRE
quench movie (with sp³ tetrahedra rendered at the final state),
the cost trace, and the g3 distribution.

```{toctree}
:maxdepth: 1

sp2_nc
mixed_nc
sp3_nc
```

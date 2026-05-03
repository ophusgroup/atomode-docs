# Refined Examples

Per-material side-by-side comparisons of the static-only build path
(`Supercell.generate(...)` → FIRE quench) against the build-time
**orientation-refinement** path
(`Supercell.generate(refine_orientations=True, ...)`), at a common
40 × 40 × 40 Å cell size.  Each material walks three regimes; for
Cu / Si / SiO₂ / SrTiO₃ the axis is disorder
(amorphous → MRO → nanocrystalline), for Carbon the axis is sp²/sp³
mixing (graphite → mixed → diamond, all at NC grain size).

Per-material pages embed the static-vs-refined 2 × 3 panel and the
six-curve g(r) overlay.  Per-regime pages embed the orientation-
refinement movie, the FIRE-quench movie (with material-appropriate
polyhedra), the cost trace, and three g3 distributions captured at
the build, post-refine, and post-FIRE states so the algorithmic
effect of each stage is visible.

See [Orientation refinement](../algorithms/orientation_refinement.md)
for the algorithm description.

```{toctree}
:maxdepth: 1

copper/index
silicon/index
carbon/index
silicon_dioxide/index
strontium_titanate/index
```

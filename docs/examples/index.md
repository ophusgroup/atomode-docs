# Examples

Case studies for several materials. Each page embeds interactive
trajectory and g3 viewers for every disorder regime covered.

```{toctree}
:maxdepth: 1

copper/index
silicon/index
carbon/index
silicon_dioxide/index
strontium_titanate/index
```

## Materials at a glance

| Material | Structure | Coordination | Notes | Status |
|---|---|---|---|---|
| Copper (Cu) | FCC, *a* = 3.615 Å | 12 (close-packed) | Metallic close-packed; first-shell angles 60°, 90°, 120°, 180°. | Complete |
| Silicon (Si) | Diamond cubic, *a* = 5.431 Å | 4 (tetrahedral, 109.5°) | Covalent reference; full 6-regime walkthrough. | Complete |
| Carbon (C) | graphite + diamond blend | 3 (sp²) and/or 4 (sp³) | Grain-level sp²/sp³ mixing via composite shell target; green triangles + navy tetrahedra rendered simultaneously. | Complete |
| Silicon dioxide (SiO₂) | α-quartz reference, *a* = 4.913 Å | Si: 4, O: 2 | Corner-sharing SiO₄ tetrahedra; tetrahedra rendered as translucent polyhedra. | Initial release |
| Strontium titanate (SrTiO₃) | Cubic perovskite, *a* = 3.913 Å | Sr: 12, Ti: 6, O: 2 | Corner-sharing TiO₆ octahedra; octahedra rendered as translucent polyhedra. | Initial release |

The silicon case walks through the six standard disorder regimes in the
`Supercell.PRESETS` dictionary (liquid, amorphous, SRO, MRO, MRO_more,
nanocrystalline).  `nanocrystalline` uses a 20 Å grain so a single tile
spans the 20 × 20 × 20 Å cell with identity rotation, giving the cleanest
diamond-cubic panel of the six.

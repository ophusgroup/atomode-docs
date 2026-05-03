# Static Examples

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

| Material | Structure | Coordination | Notes |
|---|---|---|---|
| Copper (Cu) | FCC, *a* = 3.615 Å | 12 (close-packed) | Metallic close-packed; first-shell angles 60°, 90°, 120°, 180°. |
| Silicon (Si) | Diamond cubic, *a* = 5.431 Å | 4 (tetrahedral, 109.5°) | Covalent open network; single 109.5° Si-Si-Si bond angle, sp³ throughout. |
| Carbon (C) | graphite + diamond blend | 3 (sp²) and/or 4 (sp³) | Multi-modal phase blend; 120° (sp²) and 109.5° (sp³) coexist via per-grain composite shell target. |
| Silicon dioxide (SiO₂) | α-quartz reference, *a* = 4.913 Å | Si: 4, O: 2 | Corner-sharing SiO₄ tetrahedra; only Si-O is a real chemical bond — same-species peaks are lattice artefacts through the bridging atom. |
| Strontium titanate (SrTiO₃) | Cubic perovskite, *a* = 3.913 Å | Sr: 12, Ti: 6, O: 2 | Corner-sharing TiO₆ octahedra (90° O-Ti-O, 180° Ti-O-Ti); SrO₁₂ cuboctahedron held by 12 Sr-O bond springs alone. |

The silicon case walks through the six standard disorder regimes in the
`Supercell.PRESETS` dictionary (liquid, amorphous, SRO, MRO, LRO,
nanocrystalline).  `nanocrystalline` uses a 20 Å grain so a single tile
spans the 40 × 40 × 40 Å cell with identity rotation, giving the cleanest
diamond-cubic panel of the six.

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
| Carbon (C) | sp² / sp³ mixtures | 3 or 4 | Amorphous and glassy phases. | Planned |
| Silicon dioxide (SiO₂) | α-quartz | Si: 4, O: 2 | Corner-sharing SiO₄ tetrahedra. | Planned |
| Strontium titanate (SrTiO₃) | Cubic perovskite, *a* = 3.905 Å | Sr: 12, Ti: 6, O: 6 | Ternary oxide with distinct sublattices. | Planned |

The silicon case walks through the six standard disorder regimes in the
`Supercell.PRESETS` dictionary (liquid, amorphous, SRO, MRO, MRO_more,
nanocrystalline_10). The `nanocrystalline_20` preset exists in the package
but is omitted from the silicon example because a 20 Å grain does not fit
in a 20 × 20 × 20 Å cell - see
[preset summary](silicon/index.md#preset-summary).

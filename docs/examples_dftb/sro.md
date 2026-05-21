# SRO SiO₂ — DFTB+ refinement

A 20 Å cubic SiO₂ supercell (609 atoms) built with the **short-range
order** regime (`grain_size = 12 Å`, `displacement_sigma = 0.010`),
then refined through the four-stage pipeline.

To re-generate:

```bash
python scripts/regen_dftb_examples.py --regime sro --box 20.0
```

## g(r) per stage

```{image} ../_static/dftb/sro_gr.png
:alt: Pair g(r) for Si-O / O-O / Si-Si at each stage of the SRO SiO2 refinement
:width: 100%
```

## Si–O bond length distribution

```{image} ../_static/dftb/sro_bond_hist.png
:alt: Si-O bond length histogram for SRO SiO2 at each refinement stage
:width: 100%
```

| stage | Si–O peak (Å) | ⟨r⟩ (Å) | σ (Å) | # Si–O bonds |
|---|---:|---:|---:|---:|
| Voronoi | 1.62 | 1.61 | 0.079 | 665 |
| after orient | 1.62 | 1.61 | 0.079 | 665 |
| after FIRE | 1.68 | 1.70 | 0.091 | 718 |
| **after DFTB+ (40 steps)** | **1.67** | **1.73** | **0.071** | **694** |

DFTB+ narrows the Si–O bond distribution by ~22 % (σ 0.091 → 0.071 Å)
and pulls the peak toward 1.67 Å.  Residual fmax at step 40 is
8.1 eV/Å — energy continues to descend but the 40-step cap stops the
relaxation short of the 1.0 eV/Å target.

## Angle distributions

```{image} ../_static/dftb/sro_angle_hist.png
:alt: O-Si-O and Si-O-Si angle histograms for SRO SiO2 at each refinement stage
:width: 100%
```

## Energy ladder

| stage | E_total (eV) | ΔE vs previous |
|---|---:|---:|
| Voronoi | -41584.89 | — |
| after orient | -41584.89 | 0 |
| after FIRE | -43253.98 | -1669 |
| **after DFTB+ relax** | **-43382.18** | **-128** (≈ -0.21 eV/atom) |

Cell volume change Voronoi → DFTB+: +0.1 %.  DFTB+ total at 40 steps
is -71.2 eV/atom, matching the amorphous and nanocrystalline results
at the same cell size.

DFTB+ relax wallclock: 876 s for the seed SP + 40 FIRE+UCF steps
(~15 min total, ~22 s/step on average).

## Reproduction summary

| knob | value |
|---|---|
| cell side | 20 Å |
| atoms | 609 |
| grain_size | 12 Å |
| FIRE steps (tricor stage 3) | 200 |
| pre-DFTB cleanup | bond_relax(20) + enforce_hard_core(40) |
| DFTB+ optimizer | ASE FIRE, maxstep = 0.03 Å |
| DFTB+ cell DOFs | volume only (`hydrostatic_strain=True`) |
| DFTB+ fmax target | 1.0 eV/Å, 40-step cap |
| charge restart | seed SP + `ReadInitialCharges=Yes` |
| SK set | matsci-0-3 |
| k-points | (1, 1, 1) Γ-only |

Per-stage trajectory (extxyz): `docs/_static/dftb/sro_traj.xyz`

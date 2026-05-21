# SRO SiO₂

A 30 Å cubic SiO₂ supercell (2052 atoms) built with the **short-range
order** regime (`grain_size = 12 Å`, `displacement_sigma = 0.010`),
then refined through the four-stage pipeline.

To re-generate:

```bash
python scripts/regen_dftb_examples.py --regime sro --box 30.0
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
| Voronoi | 1.61 | 1.61 | 0.070 | 2224 |
| after orient | 1.61 | 1.61 | 0.070 | 2224 |
| after FIRE | 1.67 | 1.70 | 0.090 | 2415 |
| **after DFTB+ (60 steps)** | **1.65** | **1.72** | **0.076** | **2342** |

DFTB+ pulls the peak back from 1.67 Å to 1.65 Å and narrows σ by
~16 % (0.090 → 0.076).  Residual fmax at step 60 is 9.32 eV/Å — the
60-step cap stops the relax short of the 1.0 eV/Å target, but energy
descent is monotonic across all 60 steps.

## Angle distributions

```{image} ../_static/dftb/sro_angle_hist.png
:alt: O-Si-O and Si-O-Si angle histograms for SRO SiO2 at each refinement stage
:width: 100%
```

## Energy ladder

| stage | E_total (eV) | ΔE vs previous |
|---|---:|---:|
| Voronoi | -141093.01 | — |
| after orient | -141093.01 | 0 |
| after FIRE | -145637.05 | -4544 |
| **after DFTB+ relax** | **-145981.82** | **-345** (≈ -0.17 eV/atom) |

Cell volume change Voronoi → DFTB+: +0.1 %.  DFTB+ total at 60 steps
is -71.1 eV/atom, matching the nanocrystalline and smaller-cell
results.

DFTB+ relax wallclock: 11,670 s = 3.2 hr for the seed SP + 60
FIRE+UCF steps (~2.6 min/step on average).

## Reproduction summary

| knob | value |
|---|---|
| cell side | 30 Å |
| atoms | 2052 |
| grain_size | 12 Å |
| FIRE steps (tricor stage 3) | 200 |
| pre-DFTB cleanup | bond_relax(20) + enforce_hard_core(40) |
| DFTB+ optimizer | ASE FIRE, maxstep = 0.03 Å |
| DFTB+ cell DOFs | volume only (`hydrostatic_strain=True`) |
| DFTB+ fmax target | 1.0 eV/Å, 60-step cap |
| charge restart | seed SP + `ReadInitialCharges=Yes` |
| SK set | matsci-0-3 |
| k-points | (1, 1, 1) Γ-only |

Per-stage trajectory (extxyz): `docs/_static/dftb/sro_traj.xyz`

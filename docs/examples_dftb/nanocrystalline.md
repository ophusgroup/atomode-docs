# Nanocrystalline SiO₂ — DFTB+ refinement

A 20 Å cubic SiO₂ supercell (609 atoms) built with the
nanocrystalline regime (`grain_size = 13 Å` — shrunk from the
standard 35 Å so a full grain fits comfortably inside the 20 Å cell;
the structural character of "large internal crystalline region +
amorphous boundary" is preserved).

To re-generate:

```bash
python scripts/regen_dftb_examples.py --regime nanocrystalline --box 20.0
```

## g(r) per stage

```{image} ../_static/dftb/nanocrystalline_gr.png
:alt: Pair g(r) for Si-O / O-O / Si-Si at each stage of the nanocrystalline SiO2 refinement
:width: 100%
```

## Si–O bond length distribution

```{image} ../_static/dftb/nanocrystalline_bond_hist.png
:alt: Si-O bond length histogram for nanocrystalline SiO2 at each refinement stage
:width: 100%
```

| stage | Si–O peak (Å) | ⟨r⟩ (Å) | σ (Å) | # Si–O bonds |
|---|---:|---:|---:|---:|
| Voronoi | 1.61 | 1.61 | 0.067 | 671 |
| after orient | 1.61 | 1.61 | 0.067 | 671 |
| after FIRE | 1.73 | 1.70 | 0.094 | 732 |
| **after DFTB+ (40 steps)** | **1.67** | **1.72** | **0.068** | **717** |

DFTB+ pulls the peak back from the FIRE-broadened 1.73 Å to 1.67 Å
and narrows σ by ~28 % (0.094 → 0.068 Å).  Residual fmax at step 40
is 7.5 eV/Å — the lowest of the three regimes, because the
mostly-crystalline interior contributes near-zero forces.

## Angle distributions

```{image} ../_static/dftb/nanocrystalline_angle_hist.png
:alt: O-Si-O and Si-O-Si angle histograms for nanocrystalline SiO2 at each refinement stage
:width: 100%
```

## Energy ladder

| stage | E_total (eV) | ΔE vs previous |
|---|---:|---:|
| Voronoi | -41897.96 | — |
| after orient | -41897.96 | 0 |
| after FIRE | -43211.76 | -1314 |
| **after DFTB+ relax** | **-43351.54** | **-140** (≈ -0.23 eV/atom) |

Cell volume change Voronoi → DFTB+: +0.1 %.  DFTB+ total at 40 steps
is -71.2 eV/atom, matching the amorphous and SRO results at the same
cell size.

DFTB+ relax wallclock: 396 s for the seed SP + 40 FIRE+UCF steps
(~6.6 min total, ~9.9 s/step on average — the crystalline interior
converges in very few SCC iterations per FIRE step, making this the
fastest regime).

## Reproduction summary

| knob | value |
|---|---|
| cell side | 20 Å |
| atoms | 609 |
| grain_size | 13 Å (shrunk from standard 35 Å to fit the 20 Å cell) |
| FIRE steps (tricor stage 3) | 200 |
| pre-DFTB cleanup | bond_relax(20) + enforce_hard_core(40) |
| DFTB+ optimizer | ASE FIRE, maxstep = 0.03 Å |
| DFTB+ cell DOFs | volume only (`hydrostatic_strain=True`) |
| DFTB+ fmax target | 1.0 eV/Å, 40-step cap |
| charge restart | seed SP + `ReadInitialCharges=Yes` |
| SK set | matsci-0-3 |
| k-points | (1, 1, 1) Γ-only |

Per-stage trajectory (extxyz): `docs/_static/dftb/nanocrystalline_traj.xyz`

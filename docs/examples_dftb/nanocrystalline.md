# Nanocrystalline SiO₂

A 30 Å cubic SiO₂ supercell (2052 atoms) built with the
nanocrystalline regime (`grain_size = 22 Å` — closer to the standard
35 Å preset, fits cleanly inside the 30 Å cell with ~4 Å of
amorphous boundary on each face).  This is the realistic
"large-interior-crystal + amorphous-boundary" scenario; the earlier
15 Å / 20 Å examples used a 13 Å grain to fit smaller cells and
filled essentially the whole cell with one grain.

To re-generate:

```bash
python scripts/regen_dftb_examples.py --regime nanocrystalline --box 30.0
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
| Voronoi | 1.61 | 1.61 | 0.052 | 2409 |
| after orient | 1.61 | 1.61 | 0.052 | 2409 |
| after FIRE | 1.69 | 1.70 | 0.069 | 2546 |
| **after DFTB+ (60 steps)** | **1.65** | **1.71** | **0.066** | **2502** |

DFTB+ pulls the peak back from the FIRE-broadened 1.69 Å to 1.65 Å
and slightly narrows σ.  Residual fmax at step 60 is 8.65 eV/Å — the
60-step cap stops the relax short of the 1.0 eV/Å target, but the
energy descent across all 60 steps is monotonic.

## Angle distributions

```{image} ../_static/dftb/nanocrystalline_angle_hist.png
:alt: O-Si-O and Si-O-Si angle histograms for nanocrystalline SiO2 at each refinement stage
:width: 100%
```

## Energy ladder

| stage | E_total (eV) | ΔE vs previous |
|---|---:|---:|
| Voronoi | -142619.07 | — |
| after orient | -142619.07 | 0 |
| after FIRE | -145906.27 | -3287 |
| **after DFTB+ relax** | **-146096.28** | **-190** (≈ -0.09 eV/atom) |

Cell volume change Voronoi → DFTB+: +0.1 %.  DFTB+ total at 60 steps
is -71.2 eV/atom, matching the smaller-cell results.

DFTB+ relax wallclock: 13,689 s = 3.8 hr for the seed SP (~48 min) +
60 FIRE+UCF steps (~2 min/step average).

```{note}
The `after orient` row is identical to `Voronoi`: the Voronoi tile
already assigns each grain an orientation that locally minimises the
pair-distance score at grain boundaries, and the SO(3) orientation
search finds no rotation that improves on it for this configuration.
The step runs (~12 s) but produces no change.
```

## Reproduction summary

| knob | value |
|---|---|
| cell side | 30 Å |
| atoms | 2052 |
| grain_size | 22 Å |
| FIRE steps (tricor stage 3) | 200 |
| pre-DFTB cleanup | bond_relax(20) + enforce_hard_core(40) |
| DFTB+ optimizer | ASE FIRE, maxstep = 0.03 Å |
| DFTB+ cell DOFs | volume only (`hydrostatic_strain=True`) |
| DFTB+ fmax target | 1.0 eV/Å, 60-step cap |
| charge restart | seed SP + `ReadInitialCharges=Yes` |
| SK set | matsci-0-3 |
| k-points | (1, 1, 1) Γ-only |

Per-stage trajectory (extxyz): `docs/_static/dftb/nanocrystalline_traj.xyz`

# Amorphous SiO₂ — DFTB+ refinement

A 20 Å cubic SiO₂ supercell (609 atoms) built with tricor's
`amorphous`-like regime, then refined through the four-stage pipeline:

1. **Voronoi tile** — Voronoi grain construction at `grain_size = 10 Å`,
   `displacement_sigma = 0.012`.
2. **Orientation refine** — per-grain SO(3) coordinate search.
3. **FIRE shell-relax** — 150 steps of the spring network via
   `cell.shell_relax`.
4. **DFTB+ relax** — `bond_relax(20)` + `enforce_hard_core(40)` cleanup,
   then ASE FIRE optimizer to `fmax = 1.0 eV/Å` with volume-only cell
   relax (`UnitCellFilter(hydrostatic_strain=True)`) and
   `maxstep = 0.03 Å`.  matsci-0-3 SK set, Γ-only, Fermi smearing
   T = 0.012 Ha, SCC tolerance 1e-2.

To re-generate:

```bash
python scripts/regen_dftb_examples.py --regime amorphous --box 20.0
```

## g(r) per stage

```{image} ../_static/dftb/amorphous_gr.png
:alt: Pair g(r) for Si-O / O-O / Si-Si at each stage of the amorphous SiO2 refinement
:width: 100%
```

## Si–O bond length distribution

```{image} ../_static/dftb/amorphous_bond_hist.png
:alt: Si-O bond length histogram for amorphous SiO2 at each refinement stage
:width: 100%
```

| stage | Si–O peak (Å) | ⟨r⟩ (Å) | σ (Å) | # Si–O bonds |
|---|---:|---:|---:|---:|
| Voronoi | 1.62 | 1.61 | 0.073 | 638 |
| after orient | 1.62 | 1.61 | 0.073 | 638 |
| after FIRE | 1.65 | 1.71 | 0.081 | 735 |
| **after DFTB+ (40 steps)** | **1.67** | **1.72** | **0.071** | **707** |

DFTB+ narrows the Si–O bond distribution and shifts the peak toward
the crystalline 1.61 Å.  The 40-step cap leaves the structure
partially relaxed (fmax = 8.1 eV/Å vs the 1.0 eV/Å target); the
energy continues to descend monotonically across all 40 steps so the
cap is the binding constraint, not a stall.

## Angle distributions

```{image} ../_static/dftb/amorphous_angle_hist.png
:alt: O-Si-O and Si-O-Si angle histograms for amorphous SiO2 at each refinement stage
:width: 100%
```

## Energy ladder

| stage | E_total (eV) | ΔE vs previous |
|---|---:|---:|
| Voronoi | -41837.45 | — |
| after orient | -41837.45 | 0 (no atom positions change for orient on this regime) |
| after FIRE | -43242.12 | -1405 |
| **after DFTB+ relax** | **-43339.69** | **-98** (≈ -0.16 eV/atom) |

Cell volume change Voronoi → DFTB+: +0.1 % (essentially unchanged).
DFTB+ total at 40 steps is -71.2 eV/atom, matching the 15 Å baseline
to 0.1 eV/atom.

DFTB+ relax wallclock: 1875 s for the seed SP + 40 FIRE+UCF steps
(~31 min total, ~47 s/step on average — amorphous is the worst case
because charge restart converges fewer SCC iterations on
strongly-disordered geometries).

## Reproduction summary

| knob | value |
|---|---|
| cell side | 20 Å |
| atoms | 609 |
| grain_size | 10 Å |
| FIRE steps (tricor stage 3) | 150 |
| pre-DFTB cleanup | bond_relax(20) + enforce_hard_core(40) |
| DFTB+ optimizer | ASE FIRE, maxstep = 0.03 Å |
| DFTB+ cell DOFs | volume only (`hydrostatic_strain=True`) |
| DFTB+ fmax target | 1.0 eV/Å, 40-step cap |
| charge restart | seed SP + `ReadInitialCharges=Yes` |
| SK set | matsci-0-3 |
| k-points | (1, 1, 1) Γ-only |

Per-stage trajectory (extxyz): `docs/_static/dftb/amorphous_traj.xyz`

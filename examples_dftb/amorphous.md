# Amorphous SiO₂

A 30 Å cubic SiO₂ supercell (2052 atoms) built with atomode's
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
python scripts/regen_dftb_examples.py --regime amorphous --box 30.0
```

## g(r) per stage

```{image} ../figures/dftb/amorphous_gr.png
:alt: Pair g(r) for Si-O / O-O / Si-Si at each stage of the amorphous SiO2 refinement
:width: 100%
```

## Si–O bond length distribution

```{image} ../figures/dftb/amorphous_bond_hist.png
:alt: Si-O bond length histogram for amorphous SiO2 at each refinement stage
:width: 100%
```

| stage | Si–O peak (Å) | ⟨r⟩ (Å) | σ (Å) | # Si–O bonds |
|---|---:|---:|---:|---:|
| Voronoi | 1.61 | 1.61 | 0.067 | 2174 |
| after orient | 1.61 | 1.61 | 0.067 | 2174 |
| after FIRE | 1.69 | 1.70 | 0.092 | 2415 |
| **after DFTB+ (60 steps)** | **1.67** | **1.72** | **0.076** | **2313** |

DFTB+ pulls the peak back toward the crystalline 1.61 Å and narrows
the distribution by ~17 % (σ 0.092 → 0.076 Å).  Residual fmax at
step 60 is 9.38 eV/Å — the 60-step cap stops the relax short of the
1.0 eV/Å target, but energy descent is monotonic across all 60 steps.

## Angle distributions

```{image} ../figures/dftb/amorphous_angle_hist.png
:alt: O-Si-O and Si-O-Si angle histograms for amorphous SiO2 at each refinement stage
:width: 100%
```

## Energy ladder

| stage | E_total (eV) | ΔE vs previous |
|---|---:|---:|
| Voronoi | -139713.26 | — |
| after orient | -139713.26 | 0 |
| after FIRE | -145516.22 | -5803 |
| **after DFTB+ relax** | **-145892.40** | **-376** (≈ -0.18 eV/atom) |

Cell volume change Voronoi → DFTB+: +0.1 %.  DFTB+ total at 60 steps
is -71.1 eV/atom, matching the SRO and nanocrystalline results at
the same cell size and the smaller-cell baselines.

DFTB+ relax wallclock: 12,937 s = 3.6 hr for the seed SP + 60
FIRE+UCF steps (~3 min/step on average — amorphous has more SCC
iterations per FIRE step than the ordered regimes).

## Reproduction summary

| knob | value |
|---|---|
| cell side | 30 Å |
| atoms | 2052 |
| grain_size | 10 Å |
| FIRE steps (atomode stage 3) | 150 |
| pre-DFTB cleanup | bond_relax(20) + enforce_hard_core(40) |
| DFTB+ optimizer | ASE FIRE, maxstep = 0.03 Å |
| DFTB+ cell DOFs | volume only (`hydrostatic_strain=True`) |
| DFTB+ fmax target | 1.0 eV/Å, 60-step cap |
| charge restart | seed SP + `ReadInitialCharges=Yes` |
| SK set | matsci-0-3 |
| k-points | (1, 1, 1) Γ-only |

Per-stage trajectory (extxyz): `docs/figures/dftb/amorphous_traj.xyz`

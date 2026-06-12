# FIRE vs MACE-MP0

The [FIRE relaxation](fire_relaxation.md) and the
[MACE-MP0 potential](mace_mp0.md) are the two relaxers used in the
example galleries.  They sit at opposite ends of a cost–accuracy
trade-off, and the goal of the ongoing calibration work is to make
FIRE's spring weights — derived from a single reference `.cif` —
reproduce MACE-relaxed structures as closely as the harmonic form
allows.

## The two energy models

| | FIRE spring network | MACE-MP0 |
|---|---|---|
| functional form | harmonic bond + angle springs, analytic repulsion walls | learned equivariant message-passing network |
| body order | 2-body (bonds, repulsion) + 3-body (angles), fixed | 4-body messages per layer × 2 layers; effectively many-body |
| interaction range | first shell (bonds/angles), $1.5\,r^\star$ (push) | 6 Å per layer, 12 Å receptive field |
| parameters from | one reference crystal (`.cif`) + 3 user weights | ~1.5 M DFT configurations (MPtrj + Alexandria) |
| bond topology | explicit K-nearest graph, rebuilt every 10 steps | none — smooth cutoff functions |
| energy scale | arbitrary (spring units); only ratios matter | eV, transferable across materials |
| forces | analytic per term | autograd of the network |
| update | simplified FIRE integrator | LBFGS (or Langevin MD for liquid) |
| cost / step at 40³ Å | ~0.05–0.1 s | ~4–13 s (8-thread CPU) |
| practical size limit | 200³ Å+ | ~40³ Å on CPU |

## What the spring network can and cannot match

Because every FIRE term is harmonic about a single target, the model
can in principle reproduce:

- **bond-length and angle distribution positions** — the targets
  $r^\star$, $\phi^\star$ are measured from the same crystal MACE
  relaxes toward;
- **distribution widths** — set by the *ratios* of
  `bond_weight : angle_weight : repulsion_weight`, which is exactly
  what the calibration below adjusts;
- **first/second-shell separation** — via the hard-core and
  non-bonded-push walls.

It cannot match:

- **anharmonicity** — real bond-energy curves are softer under
  stretch than compression, so MACE-relaxed distributions are skewed
  while harmonic ones are symmetric;
- **chemistry changes** — coordination defects, over/under-bonded
  sites, and bond rearrangement energetics have no representation in
  a fixed-topology spring network;
- **absolute energies** — the spring cost is a fit metric, not a
  potential energy; regime stability ladders (eV/atom) require MACE
  (or DFT) single points.

## Calibrating FIRE weights from a single `.cif` against MACE

The spring targets ($r^\star$, $\phi^\star$, hard-core radii) already
come from the reference crystal.
{meth}`CoordinationShellTarget.calibrate_to_mace` measures the
**stiffnesses** from MACE's curvature around that same crystal, so
both models share one input file:

```python
shell = tc.CoordinationShellTarget.from_atoms(ref_atoms, phi_num_bins=90)
shell = shell.calibrate_to_mace()        # optional; needs mace-torch
```

The calibration runs in seconds per material (the reference cell is
tiny) and fills in:

- **`pair_k_bond`** (eV/Å²) — interatomic-Hessian projection: displace
  the representative neighbour $j$ by $\pm\delta$ along the bond axis
  and read the force change on $i$,
  $k = \hat{\mathbf u} \cdot (\mathbf F_i^+ - \mathbf F_i^-) / 2\delta$.
  This isolates the $i$–$j$ constant from the other springs attached
  to either atom.  Negative bare constants (ionic spectator pairs
  such as Sr–O, where lattice stability comes from the other terms)
  are clamped to zero with the raw value kept in
  `mace_calibration`.
- **`pair_morse_D/a/r`** — Morse fit
  $D(1 - e^{-a(r - r_e)})^2$ of a rigid bond scan, restricted to an
  energy window (default 4 eV) around the minimum.
- **`pair_hard_min_mace`** (Å) — where the compressive branch rises
  1 eV above the bond minimum.
- **`angle_k`** (eV/rad²) — rigid-bend scan of the representative
  triplet, rotating the endpoint with the fewest bonds, with the
  moving atom's bond-stretch contribution
  $\sum_n k_{an} (\mathbf v \cdot \hat{\mathbf u}_{an})^2$ subtracted
  in closed form.  Couplings to *other angles* sharing the moving
  atom are not removed and remain a known overestimate (worst for
  high-coordination centres, e.g. Ti–O–Ti in SrTiO₃).

Because tricor's force definitions make `bond_weight` ≡ $k_\text{bond}$
(energy/Å²) and `angle_weight` ≡ $k_\text{angle}$ (energy/rad²), the
calibrated ratio plugs in directly.  Measured with `medium-mpa-0`:

| material | k_bond (eV/Å²) | k_angle (eV/rad²) | angle/bond | preset ratio |
|---|---:|---:|---:|---:|
| Si | 5.8 | 20.3 | 3.5 | ~0.45 |
| SiO₂ (Si–O) | 26.3 | 14.2 / 34.0 | 0.92 | ~0.8 |
| Cu | 1.8 | 0.6 | 0.34 | 0 |
| SrTiO₃ (Ti–O) | 1.7 | 20.9 / 70.3 | — | ~0.7 |

The Si row is the headline: MACE says silicon's angle springs are
~7× stiffer relative to its bond springs than the hand-tuned presets
use.  Validation protocol: relax identical Voronoi starts with
calibrated FIRE and with MACE; compare bond/angle distribution widths
and g₂/g₃, and score the FIRE-relaxed structure with a MACE single
point.  The per-atom energy gap to the MACE-relaxed structure is the
figure of merit.

**Validated outcome (Si nanocrystalline, 40³ Å).**  Transplanting the
literal stiffness *ratio* into the quench over-constrains angles
(angle σ collapses to 12.9° vs MACE's 16.2°) and widens the energy
gap; a thermal distribution's width is not set by curvature alone,
and the fixed-step integrator under-resolves the stiffened modes.
What does transfer:

| FIRE configuration | gap to MACE-relaxed (eV/atom) |
|---|---:|
| hand-tuned weights | +0.105 |
| + literal MACE stiffness ratio | +0.179 |
| + Morse anharmonicity, MACE wall, per-pair k at the hand-tuned effective scale | **+0.081** |

The winning configuration — used by the
[Fast FIRE Refinement examples](../examples_refined/index.md) — keeps
the proven effective force scale and takes the calibration's Morse
anharmonicity, per-pair stiffness ratios between *different* species
pairs, and hard-core wall.

Composite targets (sp²/sp³ carbon) are calibrated per sub-target
before `from_targets` composes them.  Consuming the per-pair
stiffnesses and Morse parameters inside `shell_relax` is the next
implementation step.

## See also

- [FIRE relaxation](fire_relaxation.md) — the spring-network energy
  and integrator being calibrated.
- [MACE-MP0 potential](mace_mp0.md) — the reference Hamiltonian.
- [MACE-MP0 Refinement Examples](../examples_mace/index.md) — the
  measured per-material structures and energy ladders the calibration
  targets.
- [Fast FIRE Refinement](../examples_refined/index.md) — the current
  (pre-calibration) FIRE example gallery.

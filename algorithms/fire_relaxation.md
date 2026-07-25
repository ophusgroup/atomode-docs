# FIRE relaxation

`Supercell.shell_relax(shell_target, ...)` performs a deterministic
relaxation of the spring-network energy that encodes the first-shell
coordination targets.  All atoms move simultaneously each step under
three force terms (bond, angle, repulsion) plus an optional
position-restraint term, integrated with a simplified **FIRE**
scheme.  Implemented in `src/atomode/_shell_relax.py`.

**FIRE** — the *Fast Inertial Relaxation Engine* — is a structural
relaxation algorithm that mixes steepest descent with inertia: atoms
accumulate velocity while the system moves downhill, and the velocity
is reset to zero the moment the power $P = \mathbf F \cdot \mathbf v$
turns negative (the system started moving uphill).  This gives
near-conjugate-gradient convergence at steepest-descent cost and is
robust for the very-far-from-equilibrium starting points produced by
Voronoi tiling.  The canonical algorithm is

> E. Bitzek, P. Koskinen, F. Gähler, M. Moseler, and P. Gumbsch,
> *Structural Relaxation Made Simple*,
> [Phys. Rev. Lett. **97**, 170201 (2006)](https://doi.org/10.1103/PhysRevLett.97.170201).

atomode implements a simplified variant (fixed momentum mixing and a
multiplicative step-size decay schedule rather than canonical FIRE's
adaptive time step — see [Integration](#integration) below).

This is what `Supercell.generate()` calls internally during the
construct-and-relax pipeline; you can also invoke it directly as a
zero-temperature follow-up to a thermal anneal, or chain it after
`generate()` for an extra round of refinement.

## Energy

The total spring-network energy summed over the supercell is

$$
\begin{aligned}
E ={}& \tfrac{1}{2}\, k_\text{bond} \!\!\sum_{(i,j)\in\mathcal B}\!
        \big(r_{ij} - r^\star_{s_i s_j}\big)^2
  && \text{(bond springs)} \\[6pt]
{}+{}& \tfrac{1}{2}\, k_\text{angle} \!\!\sum_{(a,c,b)\in\mathcal T}\!
        \big(\phi_{acb} - \phi^\star\big)^2
  && \text{(angle springs)} \\[6pt]
{}+{}& E_\text{rep}
  && \text{(hard core + non-bonded push)} \\[6pt]
{}+{}& \tfrac{1}{2}\, k_\text{restraint} \sum_{i}
        \big\lVert \mathbf r_i - \mathbf r_i^{(0)} \big\rVert^2
  && \text{(position restraint, optional)}
\end{aligned}
$$

where $\mathcal B$ is the bond list, $\mathcal T$ the bonded-triplet
list, $r^\star_{s_i s_j}$ the species-pair bond-peak distance and
$\phi^\star$ the per-triplet target angle from `shell_target`, and
$\mathbf r_i^{(0)}$ the *initial* positions captured at the start of
the run.  All distances and displacements use the minimum-image
convention so that PBC wrapping never appears as a spurious force.

Every parameter of this energy comes from a **single reference
crystal** (one `.cif` file): `CoordinationShellTarget.from_atoms`
measures the per-species-pair bond peaks, hard-core distances,
coordination counts, and per-triplet angle modes, and the
`bond_weight` / `angle_weight` / `repulsion_weight` prefactors scale
the three terms relative to each other.  How those weights relate to a
first-principles energy surface is discussed in
[FIRE vs MACE-MP0](fire_vs_mace.md).

### Optional MACE calibration

When the optional `mace-torch` dependency is installed,
`shell_target.calibrate_to_mace()` measures per-pair bond stiffness,
per-triplet angle stiffness, Morse anharmonicity, and the hard-core
wall position from the MACE-MP0 potential on the same reference
crystal.  A calibrated target changes the relaxer in three ways:

- per-pair / per-triplet stiffness **ratios** replace the uniform
  springs (normalised to the mean bonded stiffness, so the overall
  force scale — and integrator stability — is unchanged;
  `bond_weight` / `angle_weight` still multiply on top);
- the hard-core wall position comes from the MACE repulsion rather
  than the crystal-geometry estimate;
- with `bond_potential="auto"` (the default), bonded pairs with a
  valid Morse fit use the anharmonic Morse force
  $F = (k/a)\,(1 - e^{-a\Delta r})\,e^{-a\Delta r}$ — stretch-soft and
  compress-hard like the real bond — instead of the symmetric
  harmonic force.  ``"harmonic"`` opts out.

Calibration is optional: without it the relaxer runs exactly as
before on the hand-tuned weights.  With it, the spring network
inherits MACE's local curvature, which improves structural accuracy
at zero extra relaxation cost.

## Force terms

### Bond springs

For each bonded pair $(i, j)$ with target distance
$r_\text{target} = $ `shell_target.pair_peak[z_i, z_j]`:

$$\mathbf F_{ij}^\text{bond}
  = k_\text{bond} \, (r_{ij} - r_\text{target}) \, \hat{\mathbf r}_{ij}
  \qquad
  U_{ij}^\text{bond}
  = \tfrac{1}{2} k_\text{bond} \, (r_{ij} - r_\text{target})^2.$$

### Angle springs

For each bonded triplet $(a, c, b)$ centred on atom $c$ with target
angle $\phi_\text{target} = $ `shell_target.angle_mode_deg` for the
triplet's species:

$$\mathbf F_a^\text{angle}
  = \frac{k_\text{angle} \, (\phi - \phi_\text{target})}{r_a}
      \, \mathbf e_{\perp,a},
  \quad
  \mathbf e_{\perp,a}
  = \frac{\hat{\mathbf r}_b - \cos\phi \, \hat{\mathbf r}_a}{\sin\phi}.$$

The symmetric expression applies to $\mathbf F_b$; the centre force is
$\mathbf F_c = -(\mathbf F_a + \mathbf F_b)$.

### Repulsion (hard core + non-bonded push)

Two repulsive terms prevent overlaps and create a clean gap between
the first and second coordination shells.  Let $u = r_\text{wall} / r$
and $h = u - 1$ for each interacting pair.

**Hard core** (acts on all pairs with $u > 1$; wall at
$r_\text{wall} = r_\text{hard-min}$ scaled by `hard_core_scale`):

$$F^\text{hard} = 4 \, k_\text{rep} \, (h + h^2).$$

**Non-bonded clearance** (acts on non-bonded pairs with $u > 1$; wall
at $r_\text{wall} = 1.5 \, r_\text{peak}$ scaled by `nonbond_push_scale`):

$$F^\text{push} = k_\text{rep} \, (h + h^2).$$

Both are directed along the pair axis and integrate analytically to
$U \propto k_\text{rep} \, r_\text{wall} \, (h - \ln(1 + h))$ (finite at the wall, soft outside).

### Position restraint (optional)

`shell_relax(..., k_restraint=k)` adds a global harmonic tether to the
starting configuration:

$$\mathbf F_i^\text{restraint} = -k_\text{restraint} \, (\mathbf r_i - \mathbf r_i^{(0)})$$

with min-image-corrected $(\mathbf r_i - \mathbf r_i^{(0)})$.
``k_restraint = 0`` (default) disables the term and reproduces
unrestrained relaxation; large values pin the structure in place.
The restraint trades fit quality for regime-character preservation
and is useful when chained after a thermal anneal or when the
unrestrained minimum (always single-crystal for these spring
potentials) is not the desired structure.

## Bond topology

The bond graph is rebuilt every `neighbor_update_interval` steps
(default 10) by a greedy assignment:

1. Sort all neighbour pairs within $1.5 \, r_\text{peak}$ by distance.
2. Accept a candidate bond $(i, j)$ only if:
   - Neither atom has reached its total coordination target $K_i$ or
     $K_j$,
   - Neither atom has exceeded the per-species-pair target
     $K_{ij}$ from `shell_target.coordination_target`,
   - The new bond makes $\ge 60°$ with every existing bond at both
     endpoints (prevents near-colinear bonds in covalent networks).
3. Species-pair restrictions: pairs with zero
   $K_{ij}$ cannot be bonded even if they pass the distance check.
   `from_atoms` zeroes lattice-artefact pairs automatically
   (`auto_filter_lattice_artifacts=True`) — essential for SiO₂ /
   SrTiO₃, where the second-shell Si-Si / Ti-Ti peak is close enough
   to pass a naive distance test but is not a real chemical bond —
   and `CoordinationShellTarget.with_cross_species_bonds_only` /
   `CoordinationShellTarget.with_bonded_species_pairs` set the
   bond graph explicitly.

Implementation notes (current code path):

- The greedy matching loop is JIT-compiled with **numba**
  (`src/atomode/_shell_relax_numba.py`) and produces bit-equivalent
  bonds to the pure-Python reference, which remains as the fallback
  when numba is not installed.  At 200³ Å (~600 k atoms, ~6 M
  candidate pairs) this rebuild is the largest single cost of the
  relaxation, hence the JIT.
- Bonded-pair membership tests during force evaluation use a sorted
  key array + `np.searchsorted` ($O(\log K)$ per query) instead of
  Python set lookups.
- When `angle_weight = 0` (liquid-like regimes) the triplet
  enumeration is skipped entirely, and `neighbor_update_interval`
  can be raised (e.g. to 60) since the topology rebuild does no
  useful work without angle springs.

(integration)=
## Integration

A simplified FIRE integrator.  With velocity $\mathbf v$, force
$\mathbf F$ (clipped per-atom to `max_force_clip`, default 2.0), fixed
momentum coefficient $\beta = 0.8$, and step size $\Delta t_n$:

$$\mathbf v_{n+1} = \begin{cases}
\beta \, \mathbf v_n + \Delta t_n \, \mathbf F_n,
   & \mathbf v_n \cdot \mathbf F_n > 0
   \quad\text{(downhill: accelerate)}, \\[4pt]
\mathbf 0,
   & \text{otherwise}
   \quad\text{(uphill: kill inertia)}.
\end{cases}$$

Positions update by $\mathbf r_{n+1} = \mathbf r_n + \mathbf v_{n+1}$
and wrap via fractional coordinates.  The step size decays
multiplicatively each iteration,
$\Delta t_{n+1} = 0.995\, \Delta t_n$ (defaults
`step_size = 0.1 Å`, `step_decay = 0.995`), so late iterations make
progressively finer moves.

Differences from canonical FIRE (Bitzek et al.):

| canonical FIRE | atomode variant |
|---|---|
| adaptive $\Delta t$: grows ×1.1 after $N_\text{min}$ consecutive downhill steps, shrinks ×0.5 on uphill | fixed multiplicative decay $\Delta t \mathrel{\times}= 0.995$ every step |
| velocity mixing $\mathbf v \leftarrow (1{-}\alpha)\,\mathbf v + \alpha \lvert\mathbf v\rvert\, \hat{\mathbf F}$ with annealed $\alpha$ | fixed momentum $\mathbf v \leftarrow \beta\,\mathbf v + \Delta t\,\mathbf F$ with $\beta = 0.8$ |
| MD time-step semantics | displacement-step semantics with a per-atom force clip |

The fixed-decay schedule trades some convergence speed for
predictability: a run of `num_steps` always performs exactly that many
sweeps, so wall time is deterministic across regimes.

The history (`shell_relax_history`) records loss components and best
configuration each step.  Best-position restoration (always on) writes
the lowest-loss frame back to `cell.atoms.positions`, so a momentary
overshoot late in the run can't degrade the final structure.  The
selection metric is the **weighted** spring energy — the same
objective the forces descend — so frames are ranked consistently with
the optimisation (an unweighted metric would reject frames whenever a
stiff term trades against a soft one).

Default weights are `bond_weight = 1.0`, `angle_weight = 1.0`,
`repulsion_weight = 3.0`.  The angle default sits near the geometric
mean of the MACE-calibrated angle-to-bond stiffness ratios measured
across Cu, Si, and SiO₂ (0.34, 3.5, and 0.92 respectively; see
[FIRE vs MACE-MP0](fire_vs_mace.md)).

## Cost and convergence

Per-step cost is approximately linear in atom count (the vectorised
force terms and the cKDTree neighbour query both scale near-linearly),
so wall time is set by `num_steps` × N: roughly 4 s for 300 steps on a
~4 k-atom 40³ Å cell, and ~30 min at 200³ Å (~600 k atoms).

The default `num_steps = 300` is conservative.  Scoring the final
structure with a MACE-MP0 single point (40³ Å nanocrystalline builds,
MACE-calibrated shells; energies relative to the 300-step result):

| pipeline stage | Si | SiO₂ |
|---|---:|---:|
| [cleanup sweeps](cleanup_sweeps.md) only, no FIRE | +73 meV/atom | +129 meV/atom |
| cleanup + 60 FIRE steps | +0.6 meV/atom | +8 meV/atom |
| cleanup + 300 FIRE steps | reference | reference |

The cleanup sweeps alone leave a substantial residual — mostly angle
strain, which pair-distance sweeps cannot act on — and FIRE recovers
nearly all of it within the first ~60 steps.  Where the default's
cost is noticeable (100³ Å and beyond), `num_steps = 60` is a good
operating point: within ~10 meV/atom of full convergence at one
fifth the cost.  Grain-based regimes relax locally, so the required
step count is set by the grain scale rather than the cell size.

## Per-atom cost (trajectory colour scale)

The `atom_cost` array stored per frame for the trajectory viewer is
the actual harmonic spring energy split per atom:

$$
\begin{aligned}
U_i^\text{cost}
 ={}& \tfrac{1}{2}\, k_\text{bond} \!\!\sum_{j \in \mathcal N(i)}\!
        \big(r_{ij} - r_\text{target}\big)^2
  && \text{(bond springs)} \\[6pt]
{}+{}& \tfrac{1}{6}\, k_\text{angle} \!\!\sum_{\text{triplets } (i, c, b)}\!
        \big(\phi - \phi_\text{target}\big)^2
  && \text{(angle springs)} \\[6pt]
{}+{}& \big(\text{repulsion contributions}\big)
  && \text{(hard core + non-bonded push)} \\[6pt]
{}+{}& \tfrac{1}{2}\, k_\text{restraint}
        \big\lVert \mathbf r_i - \mathbf r_i^{(0)} \big\rVert^2
  && \text{(position restraint, optional)}
\end{aligned}
$$

The viewer's global colour scale uses the 99th percentile of
`atom_cost` in the **last quarter of frames** (steady state), not
across the whole trajectory. Early frames of liquid-path runs can
have per-atom costs two orders of magnitude larger than the relaxed
state and would otherwise saturate the scale.

## See also

- [FIRE vs MACE-MP0](fire_vs_mace.md) — how this spring-network energy
  compares to the MACE-MP0 machine-learning potential, and the
  strategy for calibrating the spring weights against it.
- [MACE-MP0 potential](mace_mp0.md) — the reference potential used by
  the [MACE refinement examples](../examples_mace/index.md).
- [Orientation refinement](orientation_refinement.md) for the SO(3)
  coordinate search that runs **before** this relaxer when
  `refine_orientations=True` is passed to `Supercell.generate`,
  giving FIRE a much better starting basin for directional-bond
  materials.
- [Supercell generation](supercell_generation.md) for the Voronoi
  grain construction that produces the initial atom block fed into
  this relaxer.
- [Cleanup sweeps](cleanup_sweeps.md) — the cKDTree `bond_relax` +
  `enforce_hard_core` sweeps that remove grain-boundary overlaps
  before this relaxer starts.

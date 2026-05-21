# Static relaxation

`Supercell.shell_relax(shell_target, ...)` performs a deterministic
gradient-descent relaxation of the spring-network energy that
encodes the first-shell coordination targets.  All atoms move
simultaneously each step under three force terms (bond, angle,
repulsion) plus an optional position-restraint term.  Implemented in
`src/tricor/_shell_relax.py`.

This is what `Supercell.generate()` calls internally during the
construct-and-relax pipeline; you can also invoke it directly as a
zero-temperature follow-up to a thermal anneal, or chain it after
`generate()` for an extra round of refinement.

## Energy

The total spring-network energy summed over the supercell is

$$
E
= \underbrace{\tfrac{1}{2} k_\text{bond}\!\!\sum_{(i,j)\in\mathcal B} (r_{ij} - r_\text{target})^2}_{\text{bonds}}
+ \underbrace{\tfrac{1}{2} k_\text{angle}\!\!\sum_{(a,c,b)\in\mathcal T} (\phi - \phi_\text{target})^2}_{\text{angles}}
+ \underbrace{E_\text{rep}}_{\text{hard core + non-bonded push}}
+ \underbrace{\tfrac{1}{2} k_\text{restraint}\!\!\sum_{i} \lVert \mathbf r_i - \mathbf r_i^{(0)} \rVert^2}_{\text{position restraint, optional}}.
$$

where $\mathcal B$ is the bond list, $\mathcal T$ the bonded-triplet
list, and $\mathbf r_i^{(0)}$ the *initial* positions captured at
the start of the run.  All distances and displacements use the
minimum-image convention so that PBC wrapping never appears as a
spurious force.

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
3. Species-aware bond restrictions via
   {meth}`CoordinationShellTarget.with_cross_species_bonds_only` or
   {meth}`CoordinationShellTarget.with_bonded_species_pairs` zero
   entries of $K_{ij}$, so those pairs cannot be bonded even if they
   pass the distance check.  Essential for SiO₂ / SrTiO₃ where the
   second-shell Si-Si / Ti-Ti peak is close enough to pass a naive
   distance test but is not a real chemical bond.

## Integration (FIRE-style)

A simplified FIRE integrator with momentum coefficient $\beta = 0.8$
and decaying step:

$$\mathbf v_{n+1} = \begin{cases}
\beta \, \mathbf v_n + \Delta t_n \, \mathbf F_n, & \mathbf v_n \cdot \mathbf F_n > 0, \\
\mathbf 0, & \text{otherwise.}
\end{cases}$$

Positions update by $\mathbf r_{n+1} = \mathbf r_n + \mathbf v_{n+1}$
and wrap via fractional coordinates.  The step decays multiplicatively
each iteration ($\Delta t \leftarrow \Delta t \cdot 0.995$ by default).
Per-atom forces are clipped at `max_force_clip` before integration to
keep liquid-path runs stable when the random initial cell has close
contacts.

The history (`shell_relax_history`) records loss components and best
configuration each step.  Best-position restoration (always on) writes
the lowest-loss frame back to `cell.atoms.positions`, so a momentary
overshoot late in the run can't degrade the final structure.

## Per-atom cost (trajectory colour scale)

The `atom_cost` array stored per frame for the trajectory viewer is
the actual harmonic spring energy split per atom:

$$U_i^\text{cost}
  = \tfrac{1}{2} k_\text{bond} \sum_{j \in \mathcal N(i)} (r_{ij} - r_\text{target})^2
  + \tfrac{1}{6} k_\text{angle} \sum_{\text{triplets } (i, c, b)} (\phi - \phi_\text{target})^2
  + (\text{repulsion contributions})
  + \tfrac{1}{2} k_\text{restraint} \, \lVert \mathbf r_i - \mathbf r_i^{(0)} \rVert^2.$$

The viewer's global colour scale uses the 99th percentile of
`atom_cost` in the **last quarter of frames** (steady state), not
across the whole trajectory. Early frames of liquid-path runs can
have per-atom costs two orders of magnitude larger than the relaxed
state and would otherwise saturate the scale.

## See also

- [Orientation refinement](orientation_refinement.md) for the SO(3)
  coordinate search that runs **before** this relaxer when
  `refine_orientations=True` is passed to `Supercell.generate`,
  giving FIRE a much better starting basin for directional-bond
  materials.
- [Supercell generation](supercell_generation.md) for the Voronoi
  grain construction that produces the initial atom block fed into
  this relaxer.
- [Large-cell shortcut](large_cell_shortcut.md) — algorithmic
  description of `Supercell.bond_relax` and
  `Supercell.enforce_hard_core`, the cKDTree-based sweeps used as
  a faster alternative to a full FIRE quench at 100³ Å and larger.
- [Generating very large cells](../large_cells.md) for the matching
  how-to (when to use the shortcut, regime-aware branching, g(r) /
  g3 measurement on the result).

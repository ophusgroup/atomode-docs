# Cleanup sweeps

tricor ships two pure-geometric cKDTree-based sweeps that act
directly on pair distances, with no springs and no integrator:

- `Supercell.bond_relax` — combined attract-to-bond-peak +
  repel-from-hard-core sweep.  Brings every pair to a physically
  correct distance in O(N log N) per iteration.
- `Supercell.enforce_hard_core` — pure geometric projection that
  pushes any sub-hard-core pair apart to exactly the wall.

Together they form the **cleanup stage** of the refinement pipelines
(Voronoi tile → orientation refine → **cleanup** → FIRE or MACE).
Raw Voronoi tilings contain overlapping pairs at grain boundaries
that produce divergent forces in either relaxer — stiff calibrated
angle springs in [FIRE](fire_relaxation.md), near-singular repulsion
in [MACE-MP0](mace_mp0.md) — and the sweeps remove those overlaps at
negligible cost before the relaxer starts.

Both live in `src/tricor/_pair_relax.py`, assume orthorhombic
periodic cells, and are vectorised at the pair level via numpy.

## `bond_relax`: attract-to-peak + repel-from-hard-core

Per sweep, find every pair within `max_cut = 1.05 ·
max(pair_outer[bonded], pair_hard_min)` via `cKDTree.query_pairs`.
For each pair $(i, j)$ with species $(s_i, s_j)$ and signed gap
$\delta = r_{ij} - r_\text{peak}$:

$$\Delta r_\text{pair} =
\underbrace{\alpha \cdot (r_{ij} - r_\text{peak})}_{\text{attract (bonded \& within $r_\text{outer}$)}}
\;-\;
\underbrace{\rho \cdot \max(r_\text{hard} - r_{ij}, 0)}_{\text{repel (any pair below hard core)}}$$

with default $\alpha = 0.2$ (attract fraction) and $\rho = 1.0$ (repel
fraction).  The signed displacement is split between $i$ and $j$
along the bond axis, accumulated across all pairs with `np.add.at`,
then clipped per-atom to `max_step = 0.2 Å` to keep dense regions
stable when an atom receives many overlapping contributions.

**Bonded-pair filter.**  Only species pairs with
`coordination_target[s_i, s_j] > 0` are attracted; the hard-core
repulsion applies to every pair regardless of bonding.  This is what
prevents, e.g., the second-shell Si–Si peak in SiO₂ from being pulled
to bond distance.

**Convergence.**  20 sweeps typically bring every bonded pair within
0.01 Å of its peak.  The default `n_iter = 40` is a saturation point —
further iterations no longer move atoms.

**Why $\alpha < \rho$.**  Attract is slower than repel because
overshooting a bond peak (and then needing to pull back) is more
expensive than overshooting a hard-core wall (atoms can't sit inside
the wall).  At $\alpha = 0.2$ a pair starting 0.5 Å above its peak
needs ~10 sweeps to close the gap; at $\alpha = 1$ it oscillates.

**Limits.**  The sweeps act on pair distances only; they cannot relax
angle strain.  Stopping after cleanup leaves a substantial energy
residual relative to a full FIRE quench — measured numbers are in
[FIRE relaxation → Cost and convergence](fire_relaxation.md#cost-and-convergence).

## `enforce_hard_core`: pure projection

`bond_relax` (and FIRE) can leave a soft tail of pairs slightly below
the hard-core wall — natural for the spring potentials, but not
acceptable for some downstream consumers (DFT input, hard-sphere
analysis).  `enforce_hard_core` is a strict projection: every pair
with $r_{ij} < r_\text{hard}[s_i, s_j]$ gets pushed apart along their
bond vector by

$$\Delta r_\text{pair}
= -\tfrac{1}{2} \, (r_\text{hard} - r_{ij}) \, \hat{\mathbf r}_{ij}$$

(default `push_fraction = 0.5`, so each atom moves by half the
deficit — they meet in the middle).  The cKDTree query uses
`max_cutoff = 1.05 · max(pair_hard_min)` to bound the candidate
set.

**Convergence.**  Geometric: each iteration reduces the worst
violation by a factor of `1 - push_fraction`, so $\log_2(\text{initial
deficit} / \text{tolerance})$ iterations suffice.  Default
`n_iter = 40` covers any realistic input.  Dense clusters where many
overlapping pairs interact may need a few more.

**Cost of strict projection.**  A small delta in g(r) at $r_\text{hard}$
— atoms pile up at exactly the wall instead of distributing
naturally above it.  For visual / structural analysis the natural
soft tail is preferable; as a standalone post-processing step the
projection is opt-in.

## Pseudocode

```python
# bond_relax core loop (per sweep)
wrap = positions - np.floor(positions / box) * box        # PBC-wrap
tree = cKDTree(wrap, boxsize=box)
pairs = tree.query_pairs(max_cut, output_type="ndarray")  # (M, 2)
delta = wrap[pairs[:, 1]] - wrap[pairs[:, 0]]
delta -= np.round(delta / box) * box                      # min-image
dist  = np.linalg.norm(delta, axis=1)
unit  = delta / dist[:, None]

attract = where(is_bond & (dist <= outer),
                (dist - peak) * 0.2, 0.0)
repel   = where(dist < hard_core,
                -(hard_core - dist) * 1.0, 0.0)
disp = unit * (attract + repel)[:, None]

# Accumulate split displacement, clip per atom, apply.
atom_disp = np.zeros_like(positions)
np.add.at(atom_disp, pairs[:, 0], disp)
np.add.at(atom_disp, pairs[:, 1], -disp)
mag = np.linalg.norm(atom_disp, axis=1)
atom_disp *= np.clip(0.2 / mag, 0.0, 1.0)[:, None]
positions += atom_disp
```

`enforce_hard_core` is the same shape with `attract = 0` and a
strict (not fractional) deficit push.

## Where to read the code

- `src/tricor/_pair_relax.py::_bond_relax_sweep` — the
  `bond_relax` kernel.
- `src/tricor/_pair_relax.py::_enforce_hard_core` — the projection.
- `src/tricor/supercell.py::Supercell.bond_relax` and
  `Supercell.enforce_hard_core` — thin wrappers that pull
  per-species-pair targets out of a `CoordinationShellTarget` and
  call the kernels.

## See also

- [FIRE relaxation](fire_relaxation.md) — the spring-network quench
  that runs after the cleanup stage, including the measured cost of
  stopping at cleanup versus running the full quench.
- [MACE-MP0 potential](mace_mp0.md) — the machine-learning relaxer
  that the same cleanup stage feeds in the
  [MACE refinement examples](../examples_mace/index.md).
- API: {meth}`~tricor.Supercell.bond_relax`,
  {meth}`~tricor.Supercell.enforce_hard_core`

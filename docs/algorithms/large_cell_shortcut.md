# Large-cell shortcut

For supercells beyond ~50³ Å the per-step cost of a full FIRE quench
grows fast enough that production builds (100³–200³ Å, 80 k–600 k
atoms) become impractical.  tricor ships two pure-geometric
cKDTree-based sweeps that replace most of FIRE for these sizes:

- `Supercell.bond_relax` — combined attract-to-bond-peak +
  repel-from-hard-core sweep.  Brings every pair to a physically
  correct distance in O(N log N) per iteration.
- `Supercell.enforce_hard_core` — pure geometric projection that
  pushes any sub-hard-core pair apart to exactly the wall.  Opt-in
  cleanup, typically called after FIRE or after `bond_relax`.

Both live in `src/tricor/_pair_relax.py`, assume orthorhombic periodic
cells, and are vectorised at the pair level via numpy.  The
user-facing how-to (when to call each, regime-aware branching, g(r) /
g3 measurement on the result) is on
[Generating very large cells](../large_cells.md); this page documents
the math.

## When the shortcut beats FIRE

| cell side | atoms (SiO₂) | full FIRE | shortcut |
|---|---:|---|---|
| 40 Å  | ~5 k  | ~10 s/regime | not needed |
| 100 Å | ~80 k | ~2 min       | ~30 s |
| 200 Å | ~600 k| ~30 min      | ~5 min |

FIRE's cost is dominated by neighbour-list rebuilds and per-step force
evaluation across the bond + angle + repulsion terms.  `bond_relax`
collapses that into one cKDTree query per sweep, with an analytic
per-pair displacement.

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
soft tail is preferable; the projection is opt-in.

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

- [Generating very large cells](../large_cells.md) — when to use
  this shortcut, regime-aware branching, g(r) / g3 measurement on
  the result.
- [Static relaxation](static_relaxation.md) — the FIRE quench this
  shortcut replaces (and which the optional short finisher pass
  still calls for angle refinement).
- [DFTB+ refinement examples](../examples_dftb/index.md) — uses
  `bond_relax(20) + enforce_hard_core(40)` as the pre-DFTB cleanup
  that gives the SCC a strict-overlap-free starting geometry.

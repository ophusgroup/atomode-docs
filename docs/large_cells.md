# Generating Very Large Cells

`Supercell.generate(num_steps=N)` runs a full FIRE quench by default,
which is the right tool up to ~50³ Å (a few thousand atoms).  Beyond
that the FIRE step cost grows fast enough that production-scale cells
(200³ Å, ~600 k atoms) become impractical without a different
strategy.

This page documents the shortcut pipeline `Supercell.bond_relax` and
the matching tools for measuring `g(r)` and `g3` on a large cell.

## When to use the shortcut

| cell side | atoms (SiO₂)  | full FIRE | shortcut |
|---|---:|---|---|
| 40 Å | ~5 k | ~10 s/regime | not needed |
| 100 Å | ~80 k | ~2 min | ~30 s |
| 200 Å | ~600 k | ~30 min | ~5 min |

The shortcut splits the relaxation into two stages: a cheap O(N log N)
attract-to-bond-peak + repel-from-hard-core sweep
(`Supercell.bond_relax`) that brings every pair to a physically correct
distance, followed by an optional short FIRE finisher to refine bond
angles.  For grain-based regimes this matches full-FIRE g(r) to within
the histogram bin width at ~1/5 the wallclock.

## The pipeline

```python
import time
import tricor as tc

# Per-regime build.  `kw` is the same regime dict used with
# `Supercell.generate` (grain_size, bond_weight, angle_weight, ...).
is_disordered = kw.get("grain_size") is None

if is_disordered:
    # Liquid / featureless regimes have a broad natural bond
    # distribution that bond_relax cannot reproduce (it pre-pulls
    # bonds to nominal pair_peak and FIRE can't undo that in a short
    # finisher).  Use the full FIRE pipeline for these regimes.
    cell.generate(shell, capture_trajectory=False, show_progress=False, **kw)
else:
    # Ordered regimes: Voronoi tile → bond_relax → short FIRE finisher.
    kw_no_steps = {k: v for k, v in kw.items() if k != "num_steps"}
    cell.generate(shell, num_steps=0,                # Voronoi only
                  capture_trajectory=False, show_progress=False,
                  **kw_no_steps)
    cell.bond_relax(shell, n_iter=40)                # bring pairs to peak
    cell.shell_relax(shell, num_steps=20,            # angle refinement
                     show_progress=False,
                     bond_weight=kw["bond_weight"],
                     angle_weight=kw["angle_weight"],
                     repulsion_weight=kw["repulsion_weight"],
                     hard_core_scale=kw["hard_core_scale"],
                     nonbond_push_scale=kw["nonbond_push_scale"])
```

**Why the regime-aware branch?**  `bond_relax` is a hard pull toward
the per-pair coordination peak (e.g. Si-O at 1.61 Å).  Crystalline +
amorphous regimes are happy there.  Liquid wants a much looser
distribution (peak ~1.78 Å for SiO₂ liquid because of `hard_core_scale=1.05`
and weak bond springs); pulling the bonds tight first traps FIRE in a
basin it can't escape with 20 finisher steps.

## Measuring g(r) and g3 on a big cell

Measuring the three-body distribution directly on a 600 k-atom cell
would take minutes.  `measure_g3` accepts a `sample_fraction` knob
that uniformly subsamples *origin* atoms while leaving the full
neighbour set intact — preserves PBC, preserves shape, drops the
cost.

```python
# Measure g3 on ~1% of atoms — same statistics as a 40³ Å cell.
cell.measure_g3(sample_fraction=0.01, sample_rng_seed=2026)
```

The MC sample correlates >0.998 with the full measurement for any
sample_fraction ≥ 1/64 (validated at 60³ Å SiO₂).  Bond-peak position
is identical to three decimals at every sampling rate.

For the inline g(r) overlay viewer, the same kwargs are plumbed
through:

```python
gr_cells = {regime: c for regime, c in cells.items()}
tc.plot_g2_compare(gr_cells, r_max=8.0, r_step=0.05,
                   sample_fraction=0.01, sample_rng_seed=2026,
                   title="SiO₂ 200³ Å — full-cell g(r), MC-subsampled")
```

This measures g(r) on the **full periodic cell** with subsampled
origins — no chunking, no PBC artefacts.

## Slicing for the 3D viewer

Rendering 600 k atoms inline in Jupyter is slow.  Extracting a
smaller chunk for the 3D viewer is fine; just make sure the chunk is
not treated as itself periodic, or the g(r) measurement on it will
wrap atoms across the chunk faces and create spurious sub-Ångström
peaks.

```python
from ase.atoms import Atoms
import numpy as np

def chunk_cube(atoms, side=40.0):
    box = np.diag(atoms.cell.array)
    lo = (box - side) / 2
    hi = lo + side
    m = np.all((atoms.positions >= lo) & (atoms.positions < hi), axis=1)
    return Atoms(
        numbers=atoms.numbers[m],
        positions=atoms.positions[m] - lo,
        cell=np.diag([side, side, side]),
        pbc=False,  # critical: the chunk is a SLICE, not a periodic cell
    )
```

For *measuring* g(r) on the chunk, the missing PBC truncates the
correlation tail past ~side/2.  Prefer measuring directly on the
full periodic cell with `sample_fraction` (above).

## Optional cleanup: `enforce_hard_core`

After FIRE, a few percent of pairs may sit slightly below the
hard-core wall (a natural soft tail in the distribution that matches
the full-FIRE reference).  If you need a strict zero-overlap
guarantee for some downstream consumer, call:

```python
cell.enforce_hard_core(shell, n_iter=40)
```

This is a pure geometric projection — every violating pair gets
pushed apart to exactly `shell.pair_hard_min[s_i, s_j]`.

**Trade-off:** the projection creates a sharp delta in g(r) at the
hard wall (atoms pile up at exactly the wall instead of distributing
naturally above it).  For visual/analysis purposes the natural soft
tail is preferable; the projection is opt-in.

## Knob reference

| knob | default | role |
|---|---:|---|
| `bond_relax(n_iter=...)` | 40 | cKDTree attract-to-peak + repel-from-hard-core sweeps.  40 is the saturation point for SiO₂. |
| `shell_relax(num_steps=...)` finisher | 20 | Short FIRE pass for angle refinement after `bond_relax`.  Set to 0 to skip; bond-only convergence is usually already good. |
| `measure_g3(sample_fraction=...)` | 1.0 | MC subsampling of origin atoms.  Use `~(small_box/big_box)**3` to match a smaller reference cell's statistics. |
| `neighbor_update_interval` (liquid) | 10 | Bump to 60 for liquid (`angle_weight=0`) — the topology rebuild does no useful work when no triplet forces are active. |
| `enforce_hard_core(n_iter=...)` | 40 | Opt-in zero-overlap projection.  Creates a delta at the wall; usually leave off. |

## See also

- [Large-cell shortcut](algorithms/large_cell_shortcut.md) — math
  and pseudocode for the `bond_relax` and `enforce_hard_core`
  sweeps.
- [Static relaxation](algorithms/static_relaxation.md) — FIRE force-term
  definitions used by both `shell_relax` and the finisher pass.
- [Generating order variety](order_variety.md) — the small-cell
  pattern, useful as a reference when comparing shortcut output
  against the full FIRE baseline.
- API: {meth}`~tricor.Supercell.bond_relax`,
  {meth}`~tricor.Supercell.enforce_hard_core`,
  {meth}`~tricor.G3Distribution.measure_g3`

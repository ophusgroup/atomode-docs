# Orientation refinement

`Supercell.refine_initial_orientations(shell_target, ...)` walks each
grain through a sequence of progressively-finer SO(3) rotation
perturbations, accepting any rotation that lowers a fast topology-free
score against the grain's local environment.  It runs **between** the
Voronoi build and the final FIRE quench, so the quench starts from a
configuration where every grain's lattice is already aligned with the
neighbours it actually has — not the random orientation the seed
draw happened to produce.

The algorithm is most useful for **directional-bond** materials
(diamond, silicon, graphite, …) where a small mis-rotation of a grain
adds large angle-spring strain across its boundary.  FCC metals like
copper are nearly invariant under SO(3) (high crystallographic
symmetry → many indistinguishable orientations) so the search is a
near no-op there.

The integrated entry point is
`Supercell.generate(refine_orientations=True,
refine_orientations_kwargs=...)`; the standalone method is
`Supercell.refine_initial_orientations` (see
``src/tricor/_resample.py``).

## Why orient grains *before* FIRE

`shell_relax` (FIRE) has two failure modes when grain orientations
are bad at the start:

1. **Stuck across grain boundaries.**  When a grain is rotated wrong,
   its surface atoms sit far from the angles their cross-grain
   neighbours want.  FIRE pulls those atoms perpendicular to the
   gradient and they thrash without converging — angle-spring energy
   stays high.
2. **Crystal interior is correct but useless.**  FIRE will happily
   leave the misaligned grain's *interior* alone (locally minimal
   bonds + angles) while paying a huge boundary cost forever.  The
   final cell ends up at a high-energy plateau that no amount of
   FIRE can escape because there is no low-frequency mode that
   coherently rotates the whole grain.

A whole-grain rotation is exactly that low-frequency mode that FIRE
cannot find.  The orientation refinement supplies it explicitly.

## Algorithm

For each grain $g$ and each rotation amplitude $a \in
\{30°, 15°, 5°, 2°\}$ (the default schedule), the refinement repeats:

1. **Propose.**  Draw $T$ random rotations
   $\mathbf R_t \in \mathrm{SO(3)}$ with axis uniform on $S^2$ and
   angle uniform in $[-a, +a]$ (Haar-uniform truncated bounded
   rotations).  Default $T = 50$.
2. **Score.**  For each candidate, retile the grain $g$ to its master
   block under $\mathbf R_t \cdot \mathbf R_g^{(0)}$ and compute the
   *pair-distance* score (defined below) against the atoms in $g$'s
   neighbourhood.  No FIRE is run per trial — the scoring kernel is
   pure geometry.
3. **Accept the best.**  If the lowest-scoring candidate beats the
   current orientation by more than `score_cutoff_factor`, commit it:
   update $\mathbf R_g$ and $\mathbf{r}_g$, refresh species indices
   for multi-species grains.  Otherwise the grain stays put.
4. **Iterate within an amplitude.**  Repeat the above for
   `max_rounds_per_amplitude` rounds (default 2) — every grain gets
   another shot now that its neighbours have moved too.
5. **Step down the schedule.**  Move to the next (smaller) amplitude
   and repeat.  Smaller amplitudes refine the basin chosen at coarser
   amplitudes.

Total work is **trials × amplitudes × rounds × grains**, which sounds
expensive but is dominated by the per-trial score that's
sub-millisecond on a typical grain (no FIRE inner loop, no neighbour
list, just $O(K)$ pair distances).

## Pair-distance score

The score quantifies how well a grain's atoms match the lattice
spacing of its environment, *without* needing a bond list:

$$
S_g(\mathbf R) = \sum_{i \in g} \sum_{j \in N(i)}
                 \left( d_{ij}(\mathbf R) - r^\star_{s_i s_j} \right)^2
$$

where $N(i)$ is the geometric neighbourhood of $i$ within
`pair_outer`, $d_{ij}$ is the post-rotation min-image distance, and
$r^\star_{s_i s_j}$ is the species-pair peak from `shell_target`.
Two crucial properties:

- **Topology-free.**  No bond graph is built; the kernel just sums
  over geometric neighbour pairs.  This is what makes per-trial
  scoring sub-millisecond — the bottleneck of any
  retile-then-FIRE-test alternative is the bond rebuild.
- **Boundary-weighted.**  Atoms deep inside a grain see only same-
  grain neighbours and contribute a constant baseline to $S_g$ for
  any rotation.  Atoms on the grain boundary see foreign neighbours
  and dominate the score.  The accepted rotation is the one that
  best aligns the boundary against its environment, which is exactly
  where the cost lives.

A grain near a perfect crystal boundary scores
$S_g \approx \mathrm{const} \cdot (a - r^\star)^2$ where $a$ is the
grain's lattice spacing.  Tilting the grain by $\theta$ adds
roughly $\theta^2 \cdot K$ for some prefactor — the score is locally
quadratic in mis-rotation, which is what makes the coordinate-descent
schedule converge predictably.

## Multi-species grains

For grains drawn from a multi-species master (SiO₂'s SiO₄
tetrahedra, SrTiO₃'s perovskite cube, …) the retile operation must
permute *both* `atoms.numbers` and `species_idx` along with positions
— otherwise an O slot can land at a Si index and the species-pair
shell-target lookups produce nonsense.  This is handled automatically
by the kernel.

## What gets tuned

- `amplitudes_deg` (default `(30, 15, 5, 2)`) — rotation schedule.
  Larger first amplitude lets the search escape mis-oriented basins
  drawn by the seed RNG.
- `trials_per_amplitude_per_grain` (default 50) — number of
  candidate rotations sampled per (grain, amplitude).  Higher gives
  a denser SO(3) sampling at the cost of wall time.
- `max_rounds_per_amplitude` (default 2) — number of full passes
  over all grains within one amplitude phase.  More rounds let
  late-touched grains revisit their own orientations after their
  neighbours moved.
- `cost_function` (default `"pair_distance"`) — the score above.
  Alternative `"bond_angle"` builds a topology per trial; usually
  not worth the slowdown.
- `score_cutoff_factor` (default 1.5) — accept threshold relative to
  the per-trial baseline.  Larger values accept more aggressively.
- `time_budget_sec` — wall-time guard rail; the search bails after
  this even if amplitudes remain.

## Cost of the search vs the FIRE that follows

Empirically (40 × 40 × 40 Å cells, 2026 hardware):

- **Pure FIRE quench** ($T = 0$, no refinement): 30–250 s depending
  on material.
- **Refinement + FIRE**: adds 5–60 s for the SO(3) search (longer
  for multi-species or many-grain regimes).  FIRE itself runs ~the
  same wall time but converges to a noticeably lower energy basin.

The visual effect is most dramatic on Si and SiO₂; see
[Refined Examples](../examples_refined/index.md) for the per-material
side-by-side comparison.

## Where to read the code

- `src/tricor/_resample.py` — `refine_initial_orientations`,
  `_pair_distance_cost`, `_so3_bounded_rotation`,
  `_retile_grain`.
- `src/tricor/supercell.py` — `Supercell.generate`'s integration
  block (the `if refine_orientations:` branch around the FIRE call).
- `src/tricor/_thermal_mc.py` — the numba kernel that runs the
  per-trial pair-distance evaluation.

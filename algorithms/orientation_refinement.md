# Orientation refinement

`Supercell.refine_initial_orientations(shell_target, ...)` walks each
grain through a sequence of progressively-finer SO(3) rotation
perturbations, accepting any rotation that lowers a fast topology-free
score against the grain's local environment.  It runs **between** the
Voronoi build and the final relaxation — whether that is the built-in
FIRE quench or a downstream MACE relaxation — so the relaxation starts
from a configuration where every grain's lattice is already aligned
with the neighbours it actually has, rather than the random
orientation the seed draw happened to produce.

The algorithm helps most for **directional-bond** materials (diamond,
silicon, graphite, …), where a small mis-rotation of a grain adds large
angle-spring strain across its boundary.  FCC metals like copper are
nearly invariant under SO(3) (high crystallographic symmetry → many
indistinguishable orientations), so orientation has little effect on
their energy; their crystalline character comes from grain size, not
alignment.

The integrated entry point is
`Supercell.generate(refine_orientations=True,
refine_orientations_kwargs=...)`; the standalone method is
`Supercell.refine_initial_orientations` (see
``src/atomode/_resample.py``).

## Why orient grains *before* FIRE

`shell_relax` (FIRE) has two failure modes when grain orientations
are bad at the start:

1. **Stuck across grain boundaries.**  When a grain is rotated wrong,
   its surface atoms sit far from the angles their cross-grain
   neighbours want.  FIRE pulls those atoms perpendicular to the
   gradient and they thrash without converging; angle-spring energy
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

The search re-runs the **full grain-assembly procedure** for every
trial — the same Voronoi fill + boundary-overlap removal + push-apart
pass that the initial build uses (see
[Supercell generation](supercell_generation.md)) — changing only the
per-grain SO(3) rotations.  A fixed RNG seed makes two assemblies with
identical rotations bit-identical, so a trial differs from the current
state only by the one rotation under test, and the trial geometry is
always as clean as a fresh build (no short boundary bonds).

For each rotation amplitude $a \in \{30°, 15°, 5°, 2°\}$ (the default
schedule) and each grain $g$:

1. **Propose.**  Draw $T$ random rotations
   $\mathbf R_t \in \mathrm{SO(3)}$ with axis uniform on $S^2$ and
   angle uniform in $[0, a]$.  Default $T = 50$.
2. **Re-assemble + score.**  For each candidate, set grain $g$'s
   rotation to $\mathbf R_t \cdot \mathbf R_g^{(0)}$, re-run the whole
   grain assembly with the fixed seed, and evaluate the **global**
   first-shell pair-distance cost (below) on the resulting cell.
3. **Accept if lower.**  Keep the candidate only if it strictly lowers
   the global cost; commit its rotation and the re-assembled cell.
   Because the baseline and every trial pass through the identical
   procedure, the cost decreases monotonically at every accept.
4. **Iterate within an amplitude.**  Repeat for
   `max_rounds_per_amplitude` rounds, so every grain gets another shot
   after its neighbours have moved.
5. **Step down the schedule.**  Move to the next (smaller) amplitude.

The full-reassembly approach is what keeps the trial geometry honest:
an earlier single-grain "retile" that skipped the boundary cleanup
left short overlapping bonds at grain faces, which made the cost
non-monotonic and could *raise* the energy of the accepted state.

## Pair-distance score

The cost quantifies how well every atom's first-shell neighbours sit
at the species-pair bond peak, *without* needing a bond list:

$$
S(\mathbf R) = \frac{1}{N}\!\!\sum_{(i,j)\,:\,d_{ij} < r_{\text{cut}}}
   \Big[\,\big(d_{ij} - r^\star_{s_i s_j}\big)^2
   + 50\,\big(\max(0,\, r^{\text{hard}}_{s_i s_j} - d_{ij})\big)^2\Big]
$$

summed over all min-image neighbour pairs within
$r_{\text{cut}} = 1.5\,\max(r^\star)$, where $r^\star_{s_i s_j}$ is the
species-pair peak and $r^{\text{hard}}_{s_i s_j}$ the hard-core
distance from `shell_target`.  The stiff hard-core penalty guarantees
any sub-hard-core pair is heavily penalised, so overlapping geometry is
never accepted.  It is evaluated globally via a single ``cKDTree``
neighbour query — $O(N)$ per trial.

- **Topology-free.**  No bond graph is built; only geometric neighbour
  pairs are summed.
- **Boundary-driven.**  Grain interiors are rigid under rotation and
  contribute a constant baseline; only boundary pairs change, so the
  accepted rotation is the one that best aligns each grain's surface
  against its neighbours.

## Multi-species grains

For grains drawn from a multi-species master (SiO₂'s SiO₄ tetrahedra,
SrTiO₃'s perovskite cube, …) the re-assembly carries the per-atom
species offsets through the rotation, so an O slot never lands at a Si
index and the species-pair shell-target lookups stay correct.

## What gets tuned

- `amplitudes_deg` (default `(30, 15, 5, 2)`): rotation schedule.
  The large first amplitude lets the search escape mis-oriented basins
  drawn by the seed RNG.
- `trials_per_amplitude_per_grain` (default 50): candidate rotations
  per (grain, amplitude).
- `max_rounds_per_amplitude` (default 2): full passes over all grains
  within one amplitude phase.
- `time_budget_sec` (default 120): wall-time guard rail; the search
  stops at the next grain boundary once this is exceeded.

## Cost of the search

Each trial re-runs the whole grain assembly, so the work scales as
**trials × amplitudes × rounds × (grains per assembly)** — effectively
*quadratic* in grain count, since one trial that rotates a single
grain still rebuilds all of them.  Regimes with large grains (few per
cell) finish quickly and converge; regimes with many small grains can
exhaust `time_budget_sec` after visiting only a handful of grains, so
the accept count is low.  A future optimisation that rebuilds only the
rotated grain and re-cleans just its boundary would make each trial
$O(1)$ in grain count.

The structural benefit is largest for directional-bond materials
(Si, SiO₂); see [Fast FIRE Refinement](../examples_refined/index.md)
for the per-material side-by-side comparison, and the
[MACE-MP0 Refinement Examples](../examples_mace/index.md), where the
same orientation step precedes a MACE relaxation.

## Where to read the code

- `src/atomode/_resample.py`: `refine_initial_orientations`,
  `_so3_bounded_rotation`.
- `src/atomode/_grain.py`: `_build_grain_atoms` (accepts a
  `rotations_override` so the refiner can re-assemble with trial
  rotations).
- `src/atomode/supercell.py`: `Supercell.generate` caches the build
  parameters and runs the refiner when `refine_orientations=True`.

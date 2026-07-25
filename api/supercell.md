# Supercell

The central class.  Constructs a periodic simulation cell from a
reference crystal and provides the full disorder-generation pipeline
(Voronoi grain build → optional orientation refinement → FIRE-style
relaxation), measurement, visualisation, and HTML-export helpers.

```python
class atomode.Supercell
```

### Construction

#### `from_atoms(atoms: 'Atoms', cell_dim_angstroms: 'float | Sequence[float]', *, r_max: 'float' = 10.0, r_step: 'float' = 0.2, phi_num_bins: 'int' = 90, relative_density: 'float' = 0.96, rng_seed: 'int | None' = None, label: 'str | None' = None, **kwargs: 'Any') -> "'Supercell'"`

Create a random supercell directly from a reference crystal.

This is a convenience constructor that measures the reference g3
distribution internally, avoiding the need to create a
:class:`G3Distribution` manually.  Use :meth:`generate` to build
the desired structure (amorphous, nanocrystalline, etc.).

**Parameters**
atoms
    Reference crystal structure (ASE Atoms object).
cell_dim_angstroms
    Physical supercell lengths in Angstrom.  A single scalar
    produces a cubic box.
r_max
    Maximum radius for the g3 measurement grid.
r_step
    Radial bin width for the g3 measurement grid.
phi_num_bins
    Number of angular bins for the g3 measurement grid.
relative_density
    Density relative to the crystalline reference.
rng_seed
    Random seed for reproducible initialization.
label
    Human-readable label.
**kwargs
    Forwarded to :meth:`Supercell.__init__`.

**Returns**
Supercell
    A new random supercell ready for :meth:`generate` or
    :meth:`shell_relax`.

### Generation

#### `generate(shell_target: "'CoordinationShellTarget'", num_steps: 'int' = 200, *, grain_size: 'float | None' = None, crystalline_fraction: 'float' = 1.0, bond_weight: 'float' = 1.0, angle_weight: 'float' = 1.0, repulsion_weight: 'float' = 3.0, hard_core_scale: 'float' = 1.0, nonbond_push_scale: 'float' = 1.0, displacement_sigma: 'float' = 0.0, atom_species_index: 'np.ndarray | None' = None, grain_sources: "'list[dict] | None'" = None, seeds: 'np.ndarray | None' = None, refine_orientations: 'bool' = False, refine_orientations_kwargs: "'dict | None'" = None, show_progress: 'bool' = True, **shell_relax_kwargs: 'Any') -> 'dict[str, Any]'`

Generate a disordered supercell from liquid to nanocrystalline.

Covers the full spectrum of disorder by combining Voronoi grain
construction with spring-network relaxation.  See
:attr:`PRESETS` for recommended parameter sets for Si.

**Parameters**
shell_target
    First-shell coordination targets from the reference crystal.
num_steps
    Number of relaxation sweeps.
grain_size
    Diameter of crystalline grains in Angstrom.  ``None`` means
    no grains - start from random positions (liquid/amorphous).
crystalline_fraction
    Volume fraction filled by crystalline grains (0–1).  Only
    used when *grain_size* is set.  The remaining volume is
    filled with random (amorphous) positions.
bond_weight
    Harmonic spring strength pulling bonded neighbours toward
    the target bond distance.  Larger = tighter distances.
angle_weight
    Spring strength pushing bond angles toward the target angle.
    Larger = tighter angles.  Near-zero = liquid-like freedom.
displacement_sigma
    Gaussian displacement (Angstrom) applied to atoms within
    crystalline grains as thermal broadening.  0 = no jitter.
show_progress
    Display a text progress bar.
**shell_relax_kwargs
    Additional keyword arguments forwarded to :meth:`shell_relax`
    (e.g. ``repulsion_weight``, ``hard_core_scale``, ``step_size``).

**Returns**
dict[str, Any]
    Summary dict with regime, construction parameters, and
    relaxation loss values.

### Orientation refinement

#### `refine_initial_orientations(shell_target: "'CoordinationShellTarget'", *, amplitudes_deg: 'tuple' = (30.0, 15.0, 5.0, 2.0), trials_per_amplitude_per_grain: 'int' = 50, max_rounds_per_amplitude: 'int' = 2, bond_weight: 'float' = 1.0, angle_weight: 'float' = 0.5, repulsion_weight: 'float' = 3.0, hard_core_scale: 'float' = 1.0, nonbond_push_scale: 'float' = 1.0, time_budget_sec: 'float' = 120.0, capture_trajectory: 'bool' = False, rng_seed: "'int | None'" = None, show_progress: 'bool' = True, **_ignored_kwargs) -> 'dict'`

Optimise per-grain rotations by re-running the full grain
assembly with trial rotations and keeping any rotation that
lowers a global pair-distance cost.  See the comment above for
the procedure.

Unrecognised keyword arguments are accepted and ignored for
backward compatibility.

#### `refine_grains(shell_target: "'CoordinationShellTarget'", *, time_budget_sec: 'float' = 300.0, max_passes: 'int' = 20, n_rot: 'int' = 8, n_trans: 'int' = 4, rotation_min_deg: 'float' = 10.0, rotation_max_deg: 'float' = 180.0, local_fire_steps: 'int' = 50, neighbor_shell_radius_factor: 'float' = 2.5, bond_weight: 'float' = 1.0, angle_weight: 'float' = 0.5, repulsion_weight: 'float' = 3.0, hard_core_scale: 'float' = 1.0, nonbond_push_scale: 'float' = 1.0, final_quench_steps: 'int' = 200, capture_trajectory: 'bool' = True, show_progress: 'bool' = True, rng_seed: "'int | None'" = None) -> 'dict'`

Iterative per-grain rotation refinement with local FIRE.

Walks the grain list round-robin; for each grain, tries
``n_rot * n_trans`` candidate (rotation, translation) pairs,
keeping the lowest-cost outcome.  A trial is judged by total
bond + angle + repulsion cost after a short
``local_fire_steps``-step FIRE pass on the grain plus its
neighbour shell.

Returns the history dict that gets stashed on
``self.refine_grains_history`` and used by
:meth:`Supercell.export_trajectory_html(history='refine_grains')`.

**Parameters**
time_budget_sec
    Stop after this many seconds of wall-clock have elapsed.
    For demo-quality results 60 - 300 s is plenty; for
    production runs raise to 1800 - 3600 s.
max_passes
    Stop after this many full round-robin passes regardless
    of time.  A pass with zero accepts triggers early
    convergence.
n_rot : int, optional
    Per-grain rotation trials.  Wall time scales linearly
    with ``n_rot * n_trans * num_grains``.
n_trans : int, optional
    Per-grain translation trials.  Combined with ``n_rot``
    sets the basin coverage per grain.
rotation_min_deg : float, optional
    Lower bound on trial rotation angle (degrees).  Lower
    values encourage fine local refinements late in the
    search.
rotation_max_deg : float, optional
    Upper bound on trial rotation angle (degrees).  Trial
    rotations sample uniformly in
    ``[rotation_min_deg, rotation_max_deg]`` about a
    uniformly-random axis.
neighbor_shell_radius_factor
    The local FIRE region around each grain extends
    ``radius_factor * pair_peak_max`` Å beyond the grain
    atoms.  ~2.5 covers the grain's own atoms plus the
    atoms in adjacent grains that share a Voronoi face,
    which is what bonds across grain boundaries actually
    depend on.
local_fire_steps
    Number of FIRE descent steps per trial.  50 is enough to
    absorb the boundary strain from a fresh rotation; raising
    past 100 wastes budget.
bond_weight : float, optional
    Spring weight for bond-distance terms.  Mirror the value
    used when the cell was originally generated.
angle_weight : float, optional
    Spring weight for bond-angle terms.
repulsion_weight : float, optional
    Spring weight for hard-core + nonbond-clearance terms.
hard_core_scale : float, optional
    Multiplier on ``shell_target.pair_inner`` setting the
    minimum allowed pair distance.
nonbond_push_scale : float, optional
    Multiplier on ``shell_target.pair_peak`` setting the
    non-bonded shell-clearance radius.
final_quench_steps
    After the round-robin loop finishes, run this many
    full-cell FIRE steps (no freezing, no restraint) to lock
    in the global minimum.  Set 0 to skip.
capture_trajectory
    When True, append a frame to the history each time a
    grain rotation is accepted.  Adds the initial state and
    the post-final-quench state too.

**Notes**
Wall-clock for the demo runs in this repo
(``cell_dim_angstroms = (40, 40, 40)``):

===========  =======  =============  ===========
regime       grains   ~accepts/run   wall time
===========  =======  =============  ===========
amorphous    ~600     ~50            5–7 min
MRO          ~50      ~10            2–3 min
nano (NC)    ~5       ~3             30–60 s
===========  =======  =============  ===========

For production-quality output (e.g. ML training datasets),
raise ``time_budget_sec`` to 1800 - 3600, raise ``n_rot`` to
16 - 32, and run multiple seeds in parallel.

#### `refine_grains_coarse_to_fine(shell_target: "'CoordinationShellTarget'", *, initial_uniform_trials: 'int' = 32, angle_schedule_deg: 'tuple' = (45.0, 22.0, 11.0, 5.0, 2.0, 1.0), trials_per_amplitude: 'int' = 12, max_rounds_per_amplitude: 'int' = 3, local_fire_steps: 'int' = 50, neighbor_shell_radius_factor: 'float' = 2.5, bond_weight: 'float' = 1.0, angle_weight: 'float' = 0.5, repulsion_weight: 'float' = 3.0, hard_core_scale: 'float' = 1.0, nonbond_push_scale: 'float' = 1.0, final_quench_steps: 'int' = 200, time_budget_sec: 'float' = 180.0, capture_trajectory: 'bool' = True, show_progress: 'bool' = True, rng_seed: "'int | None'" = None) -> 'dict'`

Coarse-to-fine basin hopping for per-grain rotations.

Walks an angle-amplitude schedule from coarse to fine.  For
each ``(amplitude, grain)`` pair, samples
``trials_per_amplitude`` candidate rotations bounded in angle
by ``amplitude`` and **composed** onto the grain's current
orientation, applies a short local FIRE on each, and accepts
the lowest-cost outcome.  The same amplitude is repeated up
to ``max_rounds_per_amplitude`` rounds while it keeps producing
accepts; then the schedule steps down.

This finds dozens of accepts where uniform-SO(3) sampling
finds only 1-2 because every trial is anchored to the current
orientation, so fine refinements within the chosen basin keep
yielding small improvements; translations are also bounded by
the amplitude (``trans_scale = amplitude / 180°``); and
multi-round at each amplitude exhausts the local search
before stepping to a smaller amplitude.

**Parameters**
shell_target : CoordinationShellTarget
    Target whose ``pair_peak`` defines the per-pair bond
    length the cost function targets.
initial_uniform_trials : int, optional
    Stage-1 uniform-SO(3) basin search per grain (rotations
    sampled independently of the current orientation, used
    only to escape the seed orientation).  Default ``32``.
    Set ``0`` to skip the basin search.
angle_schedule_deg : tuple of float, optional
    Stage-2 amplitude schedule (degrees), coarse → fine.
    Default ``(45, 22, 11, 5, 2, 1)``.
trials_per_amplitude : int, optional
    Candidate rotations per (amplitude, grain).  Default
    ``12``.
max_rounds_per_amplitude : int, optional
    Maximum round-robin passes over all grains within one
    amplitude phase.  Default ``3``.
local_fire_steps : int, optional
    FIRE steps applied to each trial's neighbour shell to
    evaluate its cost.  Default ``50``.
neighbor_shell_radius_factor : float, optional
    Local-FIRE neighbour shell extends to this multiple of
    ``shell_target.pair_peak`` around the perturbed grain.
    Default ``2.5``.
bond_weight, angle_weight, repulsion_weight : float, optional
    Spring weights forwarded to the per-trial FIRE + cost
    evaluation.
hard_core_scale, nonbond_push_scale : float, optional
    Repulsion thresholds for the per-trial FIRE.
final_quench_steps : int, optional
    Whole-cell FIRE quench steps applied after the SO(3)
    search completes.  Default ``200``; set ``0`` to skip.
time_budget_sec : float, optional
    Wall-time guard rail (seconds).  The search bails after
    this even if amplitudes remain.  Default ``180``.
capture_trajectory : bool, optional
    Record per-frame atom positions after each acceptance.
    Default ``True`` (needed for trajectory-replay HTML).
show_progress : bool, optional
    Display a tqdm progress bar.  Default ``True``.
rng_seed : int, optional
    Seed for the rotation sampler.  ``None`` (default) uses
    the cell's own RNG.

**Returns**
dict
    History captured under
    ``self.refine_grains_coarse_to_fine_history`` — same
    shape as :meth:`refine_grains`'s history (so the
    trajectory + cost plotters work unchanged), plus a
    ``rotation_amplitude_deg`` array marking which amplitude
    phase produced each accept.

### Relaxation

#### `shell_relax(shell_target: 'CoordinationShellTarget', num_steps: 'int' = 200, *, bond_weight: 'float' = 1.0, angle_weight: 'float' = 1.0, repulsion_weight: 'float' = 3.0, bond_potential: 'str' = 'auto', k_restraint: 'float' = 0.0, r_initial_override: "'np.ndarray | None'" = None, freeze_mask: "'np.ndarray | None'" = None, freeze_grain_interiors: 'bool' = False, hard_core_scale: 'float' = 1.0, nonbond_push_scale: 'float' = 1.0, step_size: 'float' = 0.1, step_decay: 'float' = 0.995, neighbor_update_interval: 'int' = 10, neighbor_cutoff_scale: 'float' = 1.5, max_force_clip: 'float' = 2.0, capture_trajectory: 'bool' = False, show_progress: 'bool' = True) -> 'dict[str, Any]'`

Relax random positions to match first-shell targets using spring forces.

Moves **all atoms simultaneously** each step via three vectorized force
terms: bond springs toward the target nearest-neighbor distance, angle
springs toward the target bond angle, and soft repulsion to eliminate
overlaps and close-packed background.  Bond topology (K-nearest
assignment) is rebuilt periodically using ASE's ``neighbor_list``.

**Parameters**
shell_target
    First-shell coordination targets extracted from the reference
    crystal via :meth:`CoordinationShellTarget.from_atoms`.
num_steps
    Number of relaxation sweeps.
bond_weight
    Strength of the harmonic spring pulling bonded neighbors toward
    ``pair_peak`` distance.
angle_weight
    Strength of the angular spring pushing bond angles toward
    ``angle_mode_deg``.
repulsion_weight
    Strength of the short-range repulsive force below ``pair_hard_min``.
bond_potential
    ``"auto"`` (default) uses Morse bond forces for species
    pairs whose shell target carries MACE-calibrated Morse
    parameters (:meth:`CoordinationShellTarget.calibrate_to_mace`)
    and harmonic springs otherwise.  ``"harmonic"`` forces
    harmonic everywhere; ``"morse"`` requires a calibrated
    target.  Calibrated per-pair / per-triplet stiffnesses are
    normalised to the mean bonded stiffness, so only the
    relative weights change and ``bond_weight`` /
    ``angle_weight`` still scale the overall terms.
k_restraint
    Spring constant (eV / Å²) for a global position-restraint
    energy ``½ k_restraint Σ ‖r_i - r_initial_i‖²`` that tethers
    every atom to its starting position.  ``0.0`` (default)
    disables the term and reproduces unrestrained relaxation.
    Small values (~0.1 - 1.0) preserve regime character (grain
    layout, amorphous topology) while still permitting local
    relaxation; large values (≫ 10) hold the structure rigid.
hard_core_scale
    Multiplier for the hard-core repulsion radius.  1.0 uses
    ``max(pair_hard_min, pair_inner)`` as the wall.  Values
    below 1.0 allow shorter bonds (softer wall for liquid).
    Values above 1.0 enforce a larger exclusion zone.
nonbond_push_scale
    Multiplier for the non-bonded shell clearance distance.
    1.0 pushes non-bonded atoms to ``1.5 * pair_peak``.
    Values below 1.0 allow non-bonded atoms closer (broader
    2nd shell for liquid).  0.0 disables non-bonded push.
step_size
    Initial maximum displacement per step (Angstrom).
step_decay
    Multiplicative decay applied to *step_size* each iteration.
neighbor_update_interval
    Rebuild the bond topology every this many steps.
neighbor_cutoff_scale
    Neighbor search cutoff as a multiple of ``max_pair_outer``.
max_force_clip
    Per-atom force magnitude is clipped to this value before
    integration to keep the dynamics stable.
freeze_grain_interiors
    If ``True``, atoms identified as deep grain interior (more
    than ``0.5 × max(pair_peak)`` away from the nearest
    grain-boundary plane) are held fixed during relaxation.
    ``False`` (the default) lets every atom relax, which is
    required for multi-species systems where the interior
    atoms must accommodate cross-species spring strain (SiO2,
    SrTiO3, sp²/sp³ carbon).  ``True`` is occasionally useful
    for single-species nanocrystalline cells where the
    interiors are already at their target geometry.  Has no
    effect on cells built without a ``grain_size``.
show_progress
    Display a text progress bar.

**Returns**
dict[str, Any]
    Summary with parameters and final/initial loss values.

#### `bond_relax(shell_target, n_iter: 'int' = 40, attract_frac: 'float' = 0.2, repel_frac: 'float' = 1.0, max_step: 'float' = 0.2) -> 'None'`

Combined attract-to-bond-peak + repel-from-hard-core sweep.

A fast O(N log N) alternative to a full FIRE relaxation for
cleaning up Voronoi-tiled or ML-predicted positions.  Each
iteration:

- Pulls bonded species pairs (those with non-zero
  ``shell_target.coordination_target``) toward
  ``shell_target.pair_peak``.
- Pushes any pair below ``shell_target.pair_hard_min`` apart.

Mutates ``self.atoms.positions`` in place.  Uses
:class:`scipy.spatial.cKDTree` so cost scales linearly with N
at constant density — at 200³ Å × 600 k atoms, ~1 s/iter on
CPU.  Drives Si-O to its 1.61 Å peak and non-bonded pairs
(Si-Si, O-O) onto their hard-core walls in 40-80 iterations.

**Parameters**
shell_target
    The :class:`CoordinationShellTarget` whose
    ``pair_peak`` / ``pair_hard_min`` / ``pair_outer`` /
    ``coordination_target`` matrices drive the forces.
n_iter
    Number of sweeps.  40 typically reaches the bond peak to
    within 0.01 Å.
attract_frac
    Per-sweep gap-closing fraction toward the bond peak.
repel_frac
    Per-sweep gap-closing fraction away from the hard-core
    wall.  ``1.0`` (default) closes the gap in one shot,
    with ``max_step`` providing the safety against overshoot
    in dense regions.
max_step
    Per-atom displacement cap (Å) per sweep.

#### `enforce_hard_core(shell_target, n_iter: 'int' = 40, push_fraction: 'float' = 0.5) -> 'None'`

Geometric projection step that clears hard-core overlaps.

Iteratively finds pairs below
``shell_target.pair_hard_min`` (via :class:`scipy.spatial.cKDTree`)
and pushes each violating pair apart along their bond vector
by ``push_fraction × deficit``.  Pure geometry - no force
springs - so it cannot pull a pair through its wall the way
the FIRE finisher's bond springs can.  Use this as a final
cleanup whenever you suspect FIRE's bond-spring forces have
compressed pairs below their hard-core distance in dense
regions (a real failure mode at 100+ Å cells).

Mutates ``self.atoms.positions`` in place.  Cost: ~1 s per
sweep at 200³ Å × 600 k atoms; converges in roughly
``O(log(initial_deficit / push_fraction))`` sweeps for
moderate overlaps, more for severe ones from a fresh Voronoi
tile.  Defaults are tuned to clear NB 01 / NB 02-scale
overlaps in a single call.

**Parameters**
shell_target
    The :class:`CoordinationShellTarget` whose
    ``pair_hard_min`` matrix sets the wall distances.
n_iter
    Number of projection sweeps.  Early-terminates if no
    violations remain.
push_fraction
    Per-iter fraction of the deficit to close.  ``0.5``
    (default) is the natural choice - both atoms move
    symmetrically and meet in the middle.  Larger values
    risk overshoot; smaller values just need more sweeps.

#### `thermal_relax(shell_target: "'CoordinationShellTarget'", *, num_sweeps: 'int' = 1000, T_schedule='anneal', T_start: 'float' = 0.05, T_end: 'float' = 0.001, hold_sweeps: 'int' = 200, step_sigma: 'float' = 0.05, smart_dt: 'float' = 0.02, adapt_step: 'bool' = True, target_accept: 'float' = 0.4, move_probs: "'dict | None'" = None, bond_weight: 'float' = 1.0, angle_weight: 'float' = 0.5, repulsion_weight: 'float' = 3.0, k_restraint: 'float' = 0.0, hard_core_scale: 'float' = 1.0, nonbond_push_scale: 'float' = 1.0, neighbor_update_interval: 'int' = 100, rep_neighbor_update_interval: 'int' = 20, capture_stride: 'int' = 10, capture_trajectory: 'bool' = True, restore_best: 'bool' = True, freeze_interior: 'bool | None' = None, freeze_mask: 'np.ndarray | None' = None, grain_moves: 'bool | None' = None, grain_move_interval: 'int' = 1, grain_sigma_rot: 'float' = 0.01, grain_sigma_trans: 'float' = 0.01, show_progress: 'bool' = True) -> 'dict'`

Temperature-dependent Metropolis Monte-Carlo relaxation.

Sits alongside :meth:`shell_relax` - same spring-network
energy (bond + angle + repulsion from ``shell_target``), but
moves atoms by Metropolis accept/reject with a temperature
schedule.  Good for escaping the local minima that gradient
descent settles into and for producing annealed amorphous
configurations.

A typical workflow is: run :meth:`shell_relax` or
:meth:`generate` once to bring the initial random / tile
configuration into a low-energy basin, then call
:meth:`thermal_relax` with a moderate-to-cold anneal schedule
to explore the basin and settle into the global minimum of
that basin.

**Parameters**
shell_target
    First-shell coordination targets, same object used by
    :meth:`shell_relax`.
num_sweeps
    Number of sweeps.  Each sweep performs ``len(atoms)``
    trial moves.
T_schedule
    ``"hold"`` (constant ``T_start``), ``"anneal"`` (hold at
    ``T_start`` for ``hold_sweeps`` then linearly drop to
    ``T_end``), or a ``callable(sweep_index) -> T``.
T_start, T_end, hold_sweeps
    Parameters for the ``"anneal"`` schedule.
step_sigma
    Initial Gaussian trial-move amplitude in Å.
adapt_step
    If ``True``, adapt ``step_sigma`` every 20 sweeps to
    target ``target_accept`` acceptance rate.
move_probs
    Dictionary with optional keys ``"displace"``, ``"swap"``,
    ``"smart"``.  Weights are normalised; default
    ``{"displace": 1.0}``.  ``"swap"`` exchanges virtual
    species between two atoms of different species; useful
    for multi-element + composite-shell-target systems.
    ``"smart"`` is a force-biased Langevin proposal with
    Metropolis correction (reserved for v2; currently treated
    as no-op).
bond_weight : float, optional
    Same as :meth:`shell_relax`.  Default ``1.0``.
angle_weight : float, optional
    Same as :meth:`shell_relax`.  Default ``0.5``.
repulsion_weight : float, optional
    Same as :meth:`shell_relax`.  Default ``3.0``.
k_restraint : float, optional
    Spring constant (eV / Å²) for a global position-restraint
    energy ``½ k_restraint Σ ‖r_i - r_initial_i‖²`` that tethers
    every atom to its starting position.  ``0.0`` (default)
    disables the term and reproduces unrestrained MC.  Small
    values (~0.1 - 1.0) preserve the input regime character
    (grain layout, amorphous topology) while still permitting
    local relaxation; large values (≫ 10) hold the structure
    essentially rigid.  Differentiable + globally defined, so
    unlike a hard ``freeze_interior`` the cost surface stays
    smooth and the relaxation can find consistent low-strain
    configurations across grain boundaries.
hard_core_scale : float, optional
    Same as :meth:`shell_relax`.  Default ``1.0``.
nonbond_push_scale : float, optional
    Same as :meth:`shell_relax`.  Default ``1.0``.
neighbor_update_interval
    Rebuild the bond topology every this many sweeps.
capture_stride
    Store a history frame every this many sweeps.  Smaller =
    finer trajectory movie, larger = less memory.
capture_trajectory
    Whether to store per-sweep positions.  Disable for very
    long runs where only cost / T / accept_rate matter.
freeze_interior
    Hard-freeze of crystalline grain interiors.  Only takes
    effect when explicitly set to ``True`` *and* the cell
    has populated ``_grain_ids`` / ``_grain_seeds`` (i.e. came
    from :meth:`generate` with ``grain_size``).  Default
    ``None`` leaves all atoms free; prefer ``k_restraint > 0``
    for a smooth, differentiable, regime-preserving alternative.
freeze_mask
    Explicit per-atom freeze mask of shape ``(num_atoms,)``.
    ``True`` entries are pinned for the entire run.  Overrides
    ``freeze_interior``.  Useful when the cell isn't grain-tiled
    but you still want to hold specific atoms (e.g. an
    interface) fixed.
grain_moves : bool, optional
    If ``True`` (or ``None`` and the cell has ≥2 grains),
    propose rigid rotation + translation of each grain every
    ``grain_move_interval`` sweeps.
grain_move_interval : int, optional
    Sweep cadence of the rigid-grain proposals.  Default ``1``
    (one set of grain moves per sweep when enabled).
grain_sigma_rot : float, optional
    Std-dev of the per-grain rotation angle (radians).
    Default ``0.01``.
grain_sigma_trans : float, optional
    Std-dev of the per-grain translation (Å).  Default
    ``0.01``.

**Returns**
dict
    History dictionary assigned to
    ``self.thermal_relax_history``.  Layout matches
    :meth:`shell_relax_history` where possible, so
    :meth:`export_trajectory_html` can visualise the
    trajectory unchanged.

### Measurement

#### `measure_g3(*, force: 'bool' = False, show_progress: 'bool' = True, backend: 'str' = 'auto', sample_fraction: 'float' = 1.0, sample_rng_seed: 'int | None' = None) -> 'G3Distribution'`

Measure the current random supercell on the target distribution grid.

**Parameters**
force
    If `True`, discard any cached measurement and recompute.
show_progress
    If `True`, display a text progress bar while the supercell
    histogram is accumulated.
backend
    Kernel selector forwarded to
    :meth:`G3Distribution.measure_g3`.  ``"auto"`` (default)
    picks the numba-parallel path when numba is installed.
sample_fraction, sample_rng_seed
    Monte-Carlo origin subsampling.  ``sample_fraction < 1.0``
    iterates only a uniform random subset of origin atoms
    (preserves PBC tile, full neighbour set).  At 200³ Å set
    this to ~``(40/200)**3`` so the histogram cost matches a
    40³ Å reference cell.

#### `sync_g3(*, show_progress: 'bool' = True) -> 'G3Distribution'`

Recompute the supercell's g2 + g3 from scratch and rebuild Monte-Carlo caches.

Forces a fresh :meth:`measure_g3` (bypassing any cached
result) and then re-initialises the per-atom contribution
tables that :meth:`monte_carlo` uses to compute incremental
ΔG3 / Δcost on each trial move.  Call after externally
modifying ``self.atoms.positions`` (e.g. injecting
a :func:`numpy.random.normal` thermal jitter) or after
chaining a :meth:`shell_relax` between MC rounds — otherwise
the MC caches refer to stale neighbour pairings and the
proposed-move statistics drift.

**Parameters**
show_progress : bool, optional
    Display a tqdm-style progress bar while the underlying
    :meth:`measure_g3` iterates.  Default ``True``.

**Returns**
G3Distribution
    The freshly measured distribution, also stored as
    ``self.current_distribution``.

### Inline visualisation (Jupyter)

#### `view_structure(shell_target: "'CoordinationShellTarget | None'" = None, *, polyhedra: "'dict | bool | None'" = True, **kwargs)`

Return an interactive 3D structure viewer widget.

Renders atoms as spheres (coloured by element).  Two overlay
modes, independently toggle-able in the widget:

* Bonds - cylinders between atoms within a radial cutoff.
* Polyhedra - translucent tetrahedra / octahedra /
  cuboctahedra around atoms that pass a distance + angle
  tolerance check (see
  :meth:`export_trajectory_html` / :func:`_detect_tetrahedra`
  for the underlying algorithm).  Enabled by default for
  materials whose coordination polyhedron we can auto-detect
  (Si / C tetrahedra at half-scale, Cu cuboctahedra, SiO2
  tetrahedra, SrTiO3 octahedra).

Sliders in the side panel let you tune the radial tolerance,
angular tolerance, centre-vertex bond length, and polyhedra
scale (0.5 places vertices at bond midpoints, 1.0 at atoms).

**Parameters**
shell_target
    Sets the default bond cutoff and bond_length from
    ``shell_target.max_pair_outer`` / ``pair_peak``.  If
    ``None``, uses the shell_target stored from the last
    :meth:`generate` call.
polyhedra
    Polyhedra config.  ``True`` / ``None`` (default) auto-pick
    kind + settings from species; ``False`` disables polyhedra;
    a ``dict`` overrides individual settings - e.g.
    ``{'kind': 'octahedra', 'center_symbol': 'Ti',
    'vertex_symbol': 'O', 'bond_length': 1.96}``.
**kwargs
    Forwarded to :class:`StructureWidget` (e.g. ``atom_scale``,
    ``bond_cutoff``, ``show_bonds``, ``slab_x``, etc.).

**Returns**
StructureWidget
    An anywidget instance for display in Jupyter.

#### `plot_structure(shell_target: "'CoordinationShellTarget | None'" = None, *, output: 'str | None' = None, width: 'int' = 1024, height: 'int' = 1024, fps: 'int' = 60, duration: 'float' = 6.0, elevation: 'float' = 15.0, atom_size: 'float' = 10.0, bond_cutoff: 'float | None' = None, show_cell: 'bool' = True, show_atoms: 'bool' = True, background: 'str' = 'white', colormap: 'str' = 'Reds', tetrahedral_thresh: 'float' = 0.4, show_progress: 'bool' = True)`

Render a bond-centric rotating 3D view of the atomic structure.

Bonds are the primary visual: crystalline (tetrahedral) bonds
are drawn thick and coloured by depth; boundary / amorphous
bonds are drawn faint.  Atoms are optional small dots.  The
animation performs a full periodic 360-degree rotation.

Classification follows the MATLAB ``plotAtoms02`` convention:
an atom is *crystalline* if it has exactly K nearest neighbours
within *bond_cutoff* **and** the mean displacement of those
neighbours is less than *tetrahedral_thresh* (i.e. the local
coordination is symmetric / tetrahedral).

**Parameters**
shell_target
    First-shell targets.  Used to set *bond_cutoff* and the
    coordination number K automatically.
output
    File path for a ``.mp4`` (recommended) or ``.gif``.
    ``None`` shows a static figure.
width, height
    Frame size in pixels.
fps
    Frames per second (GIF only).
duration
    Total GIF length in seconds.  Rotation is always exactly
    360 degrees so the loop is seamless.
elevation
    Camera elevation in degrees.
atom_size
    Matplotlib scatter marker size.  Set to 0 to hide atoms.
bond_cutoff
    NN bond length cutoff in Angstrom.
show_cell
    Draw the periodic cell outline.
show_atoms
    Draw atom dots.
background
    Figure background colour.
colormap
    Matplotlib colormap for crystalline bonds (coloured by
    depth / y-coordinate after rotation, like MATLAB ``bone``).
tetrahedral_thresh
    Maximum norm of mean NN displacement vector for an atom to
    be classified as crystalline.  Smaller = stricter.
show_progress
    Print frame counter during GIF rendering.

#### `plot_g2(*, r_max: 'float' = 10.0, r_step: 'float' = 0.05, title: 'str' = '', height: 'int' = 420, show_progress: 'bool' = False)`

Return an inline Jupyter display of the g(r) pair-correlation
viewer.

Convenience wrapper around :meth:`export_g2_html` that packages
the HTML as an :class:`IPython.display.HTML` object so you can
just do ``cells['MRO'].plot_g2()`` in a notebook cell.  The
viewer is embedded via a ``srcdoc`` iframe so it renders
isolated from the surrounding notebook CSS / JS.

**Parameters**
r_max, r_step, title, show_progress
    Forwarded to :meth:`export_g2_html`.
height
    Iframe height in pixels.

#### `plot_g3(pair: 'int | str' = 0, *, normalize: 'bool' = True)`

Return an interactive explorer for the supercell's measured g3.

Requires :meth:`measure_g3` to have been called first.

**Parameters**
pair
    Triplet index or label (e.g. ``0`` or ``"Si-Si-Si"``).
normalize
    If ``True``, display the reduced (density-normalised) g3.

#### `plot_g3_compare(pair: 'int | str' = 0, *, normalize: 'bool' = True)`

Interactive side-by-side comparison of the current supercell's g3 against its target g3.

Renders an anywidget-based two-panel viewer in Jupyter: left
panel is the supercell's measured g3 for the chosen
species-pair triplet channel, right panel is the corresponding
target g3 (set via ``Supercell.target_distribution``).  Drag
the radial-shell slider below either panel to inspect a g3
slice at fixed root-bond radius.

**Parameters**
pair : int or str, optional
    Which triplet channel to display.  Either an integer index
    into ``target_distribution.angle_index`` or a string label
    like ``"Si-Si-Si"`` resolved by
    :meth:`G3Distribution._resolve_pair_index`.  Default ``0``
    (first channel).
normalize : bool, optional
    If ``True`` (default), normalise both g3 values by the
    uniform-random reference so bins read as enhancements
    (>1) or depletions (<1).  If ``False``, raw counts.

**Returns**
G3CompareWidget
    Interactive anywidget instance.  Display it inline in
    Jupyter (returning the widget from a cell auto-renders).

#### `plot_shell_relax(*, log_y: 'bool' = False)`

Plot the FIRE relaxation loss history captured by the most recent :meth:`shell_relax` call.

Renders the per-step total loss alongside its best-so-far
envelope and the three component contributions (bond, angle,
repulsion).  When the run was launched with
``k_restraint > 0``, the position-restraint contribution is
added as a fifth curve in purple.

**Parameters**
log_y : bool, optional
    Display the loss axis on a log scale.  Useful for runs
    that span several orders of magnitude (e.g.
    ``num_steps`` > 200 with stiff springs).  Default
    ``False``.

**Returns**
matplotlib.figure.Figure
    The created figure.

**Raises**
ValueError
    If :meth:`shell_relax` has not been run yet
    (``self.shell_relax_history is None``).

#### `plot_thermal_relax(*, log_y: 'bool' = False, log_x: 'bool' = False)`

Plot thermal-MC history: cost + T on shared x-axis.

Two stacked panels with ``sharex=True`` so the hold-plateau /
anneal-ramp shape in temperature lines up visually with the
cost trajectory.

**Parameters**
log_y
    Log-scale the cost axis.  Recommended for convergence
    checking - a converged run shows a clear plateau when
    the cost curve flattens on a log scale.
log_x
    Log-scale the sweep axis.  Off by default because a
    typical hold+anneal schedule is linear in sweep index, so
    log-x distorts the temperature ramp visually.  Useful if
    your schedule spans many orders of magnitude in sweep
    number or you want to emphasize early-sweep dynamics.

#### `plot_thermal_before_after(*, r_max: 'float' = 8.0, title: 'str | None' = None)`

Compare g(r) before and after the most recent :meth:`thermal_relax` call.

Builds a g(r) overlay viewer with two curves: the cell state
cached at the start of :meth:`thermal_relax` ("before") and
the current state after the Monte-Carlo run completes
("after").  Useful for visualising how an anneal schedule
sharpened or broadened the radial distribution.

**Parameters**
r_max : float, optional
    Maximum radial distance (Å) plotted on the x-axis.
    Default ``8.0`` Å.
title : str, optional
    Title shown above the viewer.  Default uses the
    supercell's ``label``.

**Returns**
IPython.display.HTML
    The rendered comparison viewer (auto-displays inline in
    Jupyter when returned from a cell).

**Raises**
ValueError
    If :meth:`thermal_relax` has not been run yet (no cached
    pre-thermal snapshot or history).

#### `plot_monte_carlo(*, log_y: 'bool' = False, show_run_boundaries: 'bool' = True)`

Plot the Monte-Carlo cost history captured by the most recent :meth:`monte_carlo` call.

Two curves are drawn on a single matplotlib axis: instantaneous
cost (current MC state) and best-so-far cost (envelope).
Vertical dashed markers separate consecutive ``monte_carlo``
runs when ``show_run_boundaries=True``.

**Parameters**
log_y : bool, optional
    Display the cost on a logarithmic y-axis.  Useful for
    anneal schedules that span several orders of magnitude.
    Default ``False``.
show_run_boundaries : bool, optional
    If ``True``, draw vertical dashed lines at the start of
    each new MC run when ``mc_history["run_index"]`` increments
    (e.g. when chained calls extend the history).  Default
    ``True``.

**Returns**
matplotlib.figure.Figure
    The created figure.

**Raises**
ValueError
    If :meth:`monte_carlo` has not been run yet
    (``self.mc_history is None``).

### HTML export

#### `export_trajectory_html(output_path: 'str', *, bond_cutoff: 'float | None' = None, atom_scale: 'float' = 0.17, bond_radius: 'float' = 0.06, background_color: 'str' = '#f7f8f5', title: 'str' = '', tetrahedra: 'dict | None' = None, tetrahedra_color=(0.35, 0.45, 0.95), tetrahedra_opacity: 'float' = 0.45, octahedra: 'dict | None' = None, octahedra_color=(0.95, 0.55, 0.25), octahedra_opacity: 'float' = 0.4, cuboctahedra: 'dict | None' = None, cuboctahedra_color=(0.55, 0.35, 0.85), cuboctahedra_opacity: 'float' = 0.4, polyhedra_groups: "'list[dict] | None'" = None, show_bonds: 'bool | None' = None, history: "'dict | str | None'" = None) -> 'str'`

Export an interactive 3D trajectory viewer as a self-contained HTML file.

Requires :meth:`shell_relax` or :meth:`generate` to have been run
with ``capture_trajectory=True``.  The resulting HTML embeds the
full position trajectory, uses Three.js (from CDN) for rendering,
and provides play/pause/slider controls.

**Parameters**
output_path
    Path to write the HTML file.
bond_cutoff
    Maximum bond length in Angstrom.  If ``None`` and the
    supercell was generated with a shell_target, uses
    ``shell_target.max_pair_outer * 1.2``.  Otherwise 3.0.
atom_scale
    Radius scale for atom spheres (multiplied by covalent radii).
bond_radius
    Radius of bond cylinders in Angstrom.
background_color
    CSS colour for the viewer background.
title
    Optional title displayed above the viewer.
show_bonds
    Whether to emit bond cylinders.  ``None`` (default) auto-picks:
    ``True`` when no ``tetrahedra`` are requested, ``False`` when
    they are (tetrahedra supersede bonds).  Pass ``True`` / ``False``
    explicitly to override.
history
    Which trajectory history to render.  ``None`` (default) uses
    ``self.shell_relax_history``.  Pass ``"thermal_relax"`` to
    render ``self.thermal_relax_history``, or pass an explicit
    history dict.  Both shell-relax and thermal-relax dicts have
    a ``"trajectory"`` key when their parent call was run with
    ``capture_trajectory=True``.

**Returns**
str
    The output path.

#### `export_g3_html(output_path: 'str', *, r_max: 'float' = 10.0, r_step: 'float' = 0.1, phi_num_bins: 'int' = 45, background_color: 'str' = '#f7f8f5', title: 'str' = '', show_progress: 'bool' = False, show_all_triplets: 'bool' = False) -> 'str'`

Export a static 2D g3 viewer as a self-contained HTML file.

Renders one heatmap per species-triplet of the reduced three-body
distribution (density / uniform, where ``1.0`` = white).  The viewer
uses a diverging RdBu_r colormap centred at ``1.0`` and lets the user
pick the triplet and adjust the upper colour limit.

A fresh :class:`G3Distribution` is measured from the current atoms on
the coarse export grid (by default 50 x 45 bins per triplet) so the
embedded JSON stays small (~500 KB) without affecting anything the
supercell itself has cached.

**Parameters**
output_path
    Path to write the HTML file.
r_max, r_step, phi_num_bins
    Measurement grid for the exported distribution.
background_color, title
    Cosmetic.
show_progress
    Forwarded to the g3 measurement call.
show_all_triplets
    If True, the viewer renders a grid of all triplet heatmaps
    simultaneously (sharing one legend and colour scale) instead
    of the interactive single-panel view.  Useful for multi-
    species cases like SiO₂ where it's otherwise unclear which
    triplet channel is being displayed.

#### `export_g2_html(output_path: "'str | None'" = None, *, r_max: 'float' = 10.0, r_step: 'float' = 0.05, background_color: 'str' = '#f7f8f5', title: 'str' = '', show_progress: 'bool' = False) -> 'str'`

Export a standalone interactive 2D g(r) viewer.

Shows the per-species-pair pair-correlation function g_{AB}(r) as
a single g(r) plot with a dropdown to switch species pair, and
an "overlay all" checkbox to compare all pairs on one axis.
Essentially the bottom panel of :meth:`export_g3_html` lifted
out on its own with a species-pair selector - useful as a
quick 2-body PDF viewer without any angular content.

**Parameters**
output_path
    Path to write the HTML file.  When ``None`` the HTML is not
    written to disk; the raw HTML string is still returned so
    the caller can embed it directly (for example via
    :func:`IPython.display.HTML`) - see also :meth:`plot_g2`
    for a ready-made Jupyter wrapper.
r_max, r_step
    Radial grid for the measurement.  A finer ``r_step`` (default
    0.05 Å) gives smoother curves than the coarse 0.1 Å
    grid used by the g3 viewer.
background_color, title
    Cosmetic.
show_progress
    Forwarded to the underlying :meth:`measure_g3` call (this
    exporter reuses the g3 machinery because the g2 array is
    a by-product; ``phi_num_bins`` is set low for speed).

**Returns**
str
    The resolved output path when ``output_path`` was provided,
    otherwise the HTML source string.

### Class attributes

#### `PRESETS`

Keys: `liquid`, `amorphous`, `SRO`, `MRO`, `LRO`, `nanocrystalline`.

## Presets

Ready-to-use parameter dictionaries available as `Supercell.PRESETS`.
See the
[silicon preset summary](../examples/silicon/index.md#preset-summary)
for the per-regime values used in the static examples.

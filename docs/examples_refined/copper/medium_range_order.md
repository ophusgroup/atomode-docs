# Medium-range order (MRO)

Cu, 40 × 40 × 40 Å, regime preset `"MRO"` with build-time
orientation refinement enabled.

## Orientation-refinement movie

Each frame is one accepted grain rotation; the schedule walks
30° → 15° → 5° → 2° and accepts the best of 50 trials per (amplitude,
grain).  Discrete steps, no FIRE between accepts.

<iframe src="../../_static/refined/trajectories/copper_MRO_refine.html"
        width="100%" height="600"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

## FIRE quench movie

Continuous atomic relaxation after rotation refinement.  The starting
state is whatever the rotation search settled on; FIRE then converges
all atoms into the basin.

<iframe src="../../_static/refined/trajectories/copper_MRO_fire.html"
        width="100%" height="600"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

## Cost trace: refinement + FIRE

Total / bond / angle / repulsion components.  Left of the dashed
line: rotation refinement (one point per accepted rotation).  Right:
FIRE convergence (downsampled).

![Cost trace for Cu Medium-range order (MRO)](../../_static/refined/cost_history/copper_MRO.png)

## g3 distribution: initial · after refine · after FIRE

Three rooted three-body distributions captured at three points along
the pipeline so the algorithmic effect of each stage is visible.

**Initial** (post-build, post-retile): grain interiors are perfect
crystal slabs at random orientations.

<iframe src="../../_static/refined/g3/copper_MRO_initial.html"
        width="100%" height="520"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

**After refinement** (pre-FIRE): SO(3) coordinate descent has
walked each grain into a better-aligned basin against its
neighbours.  Differences from the initial g3 are concentrated at
grain boundaries.

<iframe src="../../_static/refined/g3/copper_MRO_after_refine.html"
        width="100%" height="520"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

**After FIRE** (final): all atoms relaxed.  A small post-FIRE
thermal jitter (σ scaled by regime grain density) is applied
before measurement so the peaks have realistic finite-T width
rather than the perfectly sharp 0K-FIRE-quench result.

<iframe src="../../_static/refined/g3/copper_MRO_after_fire.html"
        width="100%" height="520"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

## Code

```python
from ase.build import bulk
import tricor as tc

atoms = bulk("Si", "diamond", a=5.431)  # use the right reference for Cu
shell_target = tc.CoordinationShellTarget.from_atoms(atoms, phi_num_bins=90)

cell = tc.Supercell.from_atoms(
    atoms,
    cell_dim_angstroms=(40, 40, 40),
    r_max=10, r_step=0.1, phi_num_bins=90,
    rng_seed=42,
)
cell.generate(
    shell_target,
    **tc.Supercell.PRESETS["MRO"],
    refine_orientations=True,
    refine_orientations_kwargs=dict(
        amplitudes_deg=(30.0, 15.0, 5.0, 2.0),
        trials_per_amplitude_per_grain=50,
        max_rounds_per_amplitude=2,
        cost_function="pair_distance",
        score_cutoff_factor=1.5,
        time_budget_sec=180.0,
        capture_trajectory=True,
    ),
    capture_trajectory=True,
)
```

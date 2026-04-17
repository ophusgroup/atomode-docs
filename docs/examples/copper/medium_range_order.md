# Medium-range order

Copper in the medium-range order (MRO) regime. A longer relaxation with
stronger bond springs and a stiffer hard core produces multiple visible
maxima in g(r) while keeping the angular distribution broadly FCC-like.

## Parameters

```python
from ase.build import bulk
import tricor as tc

atoms = bulk("Cu", "fcc", a=3.615)
shell_target = tc.CoordinationShellTarget.from_atoms(atoms, phi_num_bins=90)

cell = tc.Supercell.from_atoms(
    atoms,
    cell_dim_angstroms=(20, 20, 20),
    r_max=10, r_step=0.1, phi_num_bins=90,
    rng_seed=42,
)
cell.generate(
    shell_target,
    num_steps=150,
    grain_size=None,
    bond_weight=1.6,
    angle_weight=0.15,
    repulsion_weight=1.8,
    hard_core_scale=0.92,
    nonbond_push_scale=0.65,
)
```

## Relaxation trajectory

Interactive 3D viewer of the shell-relaxation trajectory (650 atoms, 151
frames). Drag to rotate, scroll to zoom. Controls below the canvas play,
scrub, and change playback speed.

<iframe src="../../_static/trajectories/cu_mro.html"
        width="100%" height="600"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

## g3 distribution

Measured from the **final (post-relaxation) atoms**. The heatmap is the
reduced three-body density in units of the uniform random reference - white
= 1.0, blue = depleted, red = enhanced. The lower panel shows the pair
profile g(r); the shaded amber band marks the first-neighbour shell used as
the root-bond integration window for the g3 slice.

<iframe src="../../_static/g3/cu_mro.html"
        width="100%" height="520"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

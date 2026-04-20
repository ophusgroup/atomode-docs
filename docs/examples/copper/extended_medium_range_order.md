# Extended medium-range order

Copper in the extended medium-range order regime. 11 Å Voronoi grains
hold enough FCC coordination for second and third neighbour peaks in
g(r) to stand out from the background; the random-rotation grain
boundaries still dominate the visible structure.

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
    num_steps=40,
    grain_size=11.0,
    bond_weight=0.3,
    angle_weight=0.0,
    repulsion_weight=0.6,
    hard_core_scale=0.82,
    nonbond_push_scale=0.55,
    displacement_sigma=0.04,
)
```

## Relaxation trajectory

Interactive 3D viewer of the shell-relaxation trajectory (650 atoms, 251
frames). Drag to rotate, scroll to zoom. Controls below the canvas play,
scrub, and change playback speed.

<iframe src="../../_static/trajectories/cu_mro_more.html"
        width="100%" height="600"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

## g3 distribution

Measured from the **final (post-relaxation) atoms**. The heatmap is the
reduced three-body density in units of the uniform random reference - white
= 1.0, blue = depleted, red = enhanced. The lower panel shows the pair
profile g(r); the shaded amber band marks the first-neighbour shell used as
the root-bond integration window for the g3 slice.

<iframe src="../../_static/g3/cu_mro_more.html"
        width="100%" height="520"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

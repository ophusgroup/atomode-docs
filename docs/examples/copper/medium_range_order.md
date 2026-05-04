# Medium-range order

Copper in the medium-range order (MRO) regime.  This is the first
regime where Voronoi grain seeding is introduced: 9 Å grains hold a
handful of well-coordinated Cu atoms each, and the random-rotation
grain boundaries keep longer-range correlations well short of a
full nanocrystal.

## Parameters

```python
from ase.build import bulk
import tricor as tc

atoms = bulk("Cu", "fcc", a=3.615)
shell_target = tc.CoordinationShellTarget.from_atoms(atoms, phi_num_bins=90)

cell = tc.Supercell.from_atoms(
    atoms,
    cell_dim_angstroms=(40, 40, 40),
    r_max=10, r_step=0.1, phi_num_bins=90,
    rng_seed=42,
)
cell.generate(
    shell_target,
    num_steps=120,
    grain_size=9.0,
    bond_weight=0.85,
    angle_weight=0.0,
    repulsion_weight=1.3,
    hard_core_scale=0.89,
    nonbond_push_scale=0.72,
    displacement_sigma=0.045,
)
```

## Relaxation trajectory

Interactive 3D viewer of the shell-relaxation trajectory (40 × 40 × 40 Å cell). Drag to rotate, scroll to zoom. Controls below the canvas play,
scrub, and change playback speed.

<iframe src="../../_static/trajectories/cu_mro.html"
        width="100%" height="600"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

## g3 distribution

Measured from the **final (post-relaxation) atoms**. The heatmap is the
reduced three-body density in units of the uniform random reference, where white
= 1.0, blue = depleted, red = enhanced. The lower panel shows the pair
profile g(r); the shaded amber band marks the first-neighbour shell used as
the root-bond integration window for the g3 slice.

<iframe src="../../_static/g3/cu_mro.html"
        width="100%" height="520"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

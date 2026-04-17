# Liquid

Copper in the liquid regime: fully disordered positions, no grain
structure. Bond springs hold a well-defined first-neighbour distance while
angle springs stay weak, so the angular distribution broadens naturally.

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
    num_steps=30,
    grain_size=None,
    bond_weight=0.25,
    angle_weight=0.0,
    repulsion_weight=0.4,
    hard_core_scale=0.7,
    nonbond_push_scale=0.5,
)
```

Angle springs are turned off entirely. A short relaxation with weak bond
springs and a soft hard core keeps the structure genuinely liquid-like;
longer runs would drive it into a close-packed configuration.

## Relaxation trajectory

Interactive 3D viewer of the shell-relaxation trajectory (650 atoms, 31
frames). Drag to rotate, scroll to zoom. Controls below the canvas play,
scrub, and change playback speed.

<iframe src="../../_static/trajectories/cu_liquid.html"
        width="100%" height="600"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

## g3 distribution

Measured from the **final (post-relaxation) atoms**. The heatmap is the
reduced three-body density in units of the uniform random reference - white
= 1.0, blue = depleted, red = enhanced. The lower panel shows the pair
profile g(r); the shaded amber band marks the first-neighbour shell used as
the root-bond integration window for the g3 slice.

<iframe src="../../_static/g3/cu_liquid.html"
        width="100%" height="520"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

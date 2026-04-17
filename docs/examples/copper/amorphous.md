# Amorphous

Copper in the amorphous regime: no grains, but stronger bond springs and a
stiffer hard core produce a well-defined first-neighbour shell with
persistent medium-range correlations. Angle springs stay weak, so the
angular distribution settles into the broad multimodal shape typical of a
metallic glass.

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
    num_steps=80,
    grain_size=None,
    bond_weight=0.9,
    angle_weight=0.0,
    repulsion_weight=1.0,
    hard_core_scale=0.88,
    nonbond_push_scale=0.55,
)
```

Angle springs are turned off so the angular distribution is shaped entirely
by the competition between bond springs and repulsion. The result is a
well-defined first neighbour shell with no medium-range crystallinity -
characteristic of a metallic glass.

## Relaxation trajectory

Interactive 3D viewer of the shell-relaxation trajectory (650 atoms, 81
frames). Drag to rotate, scroll to zoom. Controls below the canvas play,
scrub, and change playback speed.

<iframe src="../../_static/trajectories/cu_amorphous.html"
        width="100%" height="600"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

## g3 distribution

Measured from the **final (post-relaxation) atoms**. The heatmap is the
reduced three-body density in units of the uniform random reference - white
= 1.0, blue = depleted, red = enhanced. The lower panel shows the pair
profile g(r); the shaded amber band marks the first-neighbour shell used as
the root-bond integration window for the g3 slice.

<iframe src="../../_static/g3/cu_amorphous.html"
        width="100%" height="520"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

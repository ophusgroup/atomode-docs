# Long-range order

Copper in the long-range order regime. 11 Å Voronoi grains hold enough
FCC coordination for second and third neighbour peaks in g(r) to stand
out from the background; the random-rotation grain boundaries still
dominate the visible structure.

## Parameters

```python
from ase.build import bulk
import atomode as am

atoms = bulk("Cu", "fcc", a=3.615)
shell_target = am.CoordinationShellTarget.from_atoms(atoms, phi_num_bins=90)

cell = am.Supercell.from_atoms(
    atoms,
    cell_dim_angstroms=(40, 40, 40),
    r_max=10, r_step=0.1, phi_num_bins=90,
    rng_seed=42,
)
cell.generate(
    shell_target,
    num_steps=140,
    grain_size=12.5,
    bond_weight=1.1,
    angle_weight=0.0,
    repulsion_weight=1.6,
    hard_core_scale=0.91,
    nonbond_push_scale=0.82,
    displacement_sigma=0.03,
)
```

## Relaxation trajectory

Interactive 3D viewer of the shell-relaxation trajectory (40 × 40 × 40 Å cell). Drag to rotate, scroll to zoom. Controls below the canvas play,
scrub, and change playback speed.

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/trajectories/cu_lro.html
:width: 100%
:::

## g3 distribution

Measured from the **final (post-relaxation) atoms**. The heatmap is the
reduced three-body density in units of the uniform random reference, where white
= 1.0, blue = depleted, red = enhanced. The lower panel shows the pair
profile g(r); the shaded amber band marks the first-neighbour shell used as
the root-bond integration window for the g3 slice.

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/g3/cu_lro.html
:width: 100%
:::

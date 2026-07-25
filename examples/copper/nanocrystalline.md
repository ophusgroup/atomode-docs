# Nanocrystalline

Copper in the nanocrystalline regime. 18 Å Voronoi grains tile the
40 × 40 × 40 Å box into 3 random-rotation FCC crystallites with
sharp boundaries between them.  Most Cu atoms sit at the centre of a
full 12-vertex cuboctahedron; boundary atoms carry the residual
disorder.

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
    num_steps=200,
    grain_size=18.0,
    bond_weight=1.5,
    angle_weight=0.0,
    repulsion_weight=2.0,
    hard_core_scale=0.94,
    nonbond_push_scale=0.95,
    displacement_sigma=0.01,
)
```

## Relaxation trajectory

Interactive 3D viewer of the shell-relaxation trajectory (40 × 40 × 40 Å cell). Drag to rotate, scroll to zoom. Controls below the canvas play,
scrub, and change playback speed.

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/trajectories/cu_nanocrystalline.html
:width: 100%
:::

## g3 distribution

Measured from the **final (post-relaxation) atoms**. The heatmap is the
reduced three-body density in units of the uniform random reference, where white
= 1.0, blue = depleted, red = enhanced. The lower panel shows the pair
profile g(r); the shaded amber band marks the first-neighbour shell used as
the root-bond integration window for the g3 slice.

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/g3/cu_nanocrystalline.html
:width: 100%
:::

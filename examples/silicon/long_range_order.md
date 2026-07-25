# Long-range order

Silicon with larger ~18 Å grains. The pair correlation function retains
sharper peaks out to longer distances than the MRO case, approaching the
nanocrystalline regime.

## Parameters

```python
from ase.build import bulk
import atomode as am

atoms = bulk("Si", "diamond", a=5.431)
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
    grain_size=15.0,
    bond_weight=2.4,
    angle_weight=1.0,
    repulsion_weight=2.3,
    hard_core_scale=0.93,
    nonbond_push_scale=0.85,
    displacement_sigma=0.035,
)
```

## Relaxation trajectory

Interactive 3D viewer of the shell-relaxation trajectory (40 × 40 × 40 Å cell).
Drag to rotate, scroll to zoom. Controls below the canvas play, scrub, and change
playback speed.

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/trajectories/si_lro.html
:width: 100%
:::

## g3 distribution

Measured from the **final (post-relaxation) atoms**. The heatmap is the
reduced three-body density in units of the uniform random reference, where white
= 1.0, blue = depleted, red = enhanced. The lower panel shows the pair
profile g(r); the shaded amber band marks the first-neighbour shell used as
the root-bond integration window for the g3 slice. For silicon there is a
single Si-Si-Si triplet channel.

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/g3/si_lro.html
:width: 100%
:::

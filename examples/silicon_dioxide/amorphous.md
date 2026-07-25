# Amorphous

SiO₂ in the amorphous regime: small Voronoi grains (4 Å diameter) seed
local tetrahedral motifs, then shell relaxation fills in the
connectivity. Coordination numbers trend toward the ideal (Si: 4, O: 2)
while orientations remain largely uncorrelated beyond first neighbours.

## Parameters

```python
cell.generate(
    shell_target,
    num_steps=250,
    grain_size=12.0,
    bond_weight=1.55,
    angle_weight=1.25,
    repulsion_weight=1.25,
    hard_core_scale=0.81,
    nonbond_push_scale=0.7,
    displacement_sigma=0.012,
)
```

## Relaxation trajectory

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/trajectories/sio2_amorphous.html
:width: 100%
:::

## g3 distribution

:::{iframe} https://ophusgroup.github.io/atomode-docs/viewers/g3/sio2_amorphous.html
:width: 100%
:::

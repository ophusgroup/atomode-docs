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

<iframe src="../../_static/trajectories/sio2_amorphous.html"
        width="100%" height="600"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

## g3 distribution

<iframe src="../../_static/g3/sio2_amorphous.html"
        width="100%" height="620"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

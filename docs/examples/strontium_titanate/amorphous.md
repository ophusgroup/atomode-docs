# Amorphous

SrTiO₃ with 8 Å α-perovskite grains: each Voronoi cell is barely large
enough to host one or two randomly-oriented TiO₆ motifs. Only a handful
of full octahedra survive the boundaries; everywhere else is disordered
oxygen connectivity.

## Parameters

```python
cell.generate(
    shell_target,
    num_steps=100,
    grain_size=8.0,
    bond_weight=0.3, angle_weight=0.6, repulsion_weight=0.4,
    hard_core_scale=1.0, nonbond_push_scale=0.5,
    displacement_sigma=0.005,
)
```

## Relaxation trajectory

<iframe src="../../_static/trajectories/srtio3_amorphous.html"
        width="100%" height="600"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

## g3 distribution

<iframe src="../../_static/g3/srtio3_amorphous.html"
        width="100%" height="720"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

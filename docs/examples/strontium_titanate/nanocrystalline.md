# Nanocrystalline

SrTiO₃ with 18 Å grains: 2 - 3 distinct perovskite grains fit in the
20 × 20 × 20 Å box, each rotated independently. The crystalline
interiors dominate the structure; only thin seams of disordered atoms
remain at the grain boundaries.

## Parameters

```python
cell.generate(
    shell_target,
    num_steps=50,
    grain_size=18.0,
    bond_weight=0.2, angle_weight=0.0, repulsion_weight=0.3,
    hard_core_scale=1.0, nonbond_push_scale=0.5,
    displacement_sigma=0.005,
)
```

## Relaxation trajectory

<iframe src="../../_static/trajectories/srtio3_nanocrystalline.html"
        width="100%" height="600"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

## g3 distribution

<iframe src="../../_static/g3/srtio3_nanocrystalline.html"
        width="100%" height="720"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

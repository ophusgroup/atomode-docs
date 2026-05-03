# Nanocrystalline

SiO₂ with 21 Å α-quartz grains: grains are now large enough that only
a couple fit in the 40 × 40 × 40 Å box. The crystalline tiles dominate
the structure; only thin seams of disordered atoms remain where rotated
grains meet.

## Parameters

```python
cell.generate(
    shell_target,
    num_steps=250,
    grain_size=27.0,
    bond_weight=1.5,
    angle_weight=1.2,
    repulsion_weight=1.2,
    hard_core_scale=0.8,
    nonbond_push_scale=0.7,
    displacement_sigma=0.01,
)
```

## Relaxation trajectory

<iframe src="../../_static/trajectories/sio2_nanocrystalline.html"
        width="100%" height="600"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

## g3 distribution

<iframe src="../../_static/g3/sio2_nanocrystalline.html"
        width="100%" height="620"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

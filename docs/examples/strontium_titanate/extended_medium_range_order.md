# Extended medium-range order

SrTiO₃ with 18 Å grains: each grain holds several shells of intact
TiO₆ octahedra and the crystalline patches cover most of the cell.
The remaining disorder sits at the narrow seams where rotated grains
meet.

## Parameters

```python
cell.generate(
    shell_target,
    num_steps=50,
    grain_size=15.0,
    bond_weight=0.2, angle_weight=0.0, repulsion_weight=0.3,
    hard_core_scale=1.0, nonbond_push_scale=0.5,
    displacement_sigma=0.005,
)
```

## Relaxation trajectory

<iframe src="../../_static/trajectories/srtio3_mro_more.html"
        width="100%" height="600"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

## g3 distribution

<iframe src="../../_static/g3/srtio3_mro_more.html"
        width="100%" height="720"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

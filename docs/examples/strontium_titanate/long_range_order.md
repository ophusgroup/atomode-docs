# Long-range order

SrTiO₃ with 18 Å grains: each grain holds several shells of intact
TiO₆ octahedra and the crystalline patches cover most of the cell.
The remaining disorder sits at the narrow seams where rotated grains
meet.

## Parameters

```python
cell.generate(
    shell_target,
    num_steps=350,
    grain_size=18.0,
    bond_weight=1.1,
    angle_weight=0.8,
    repulsion_weight=1.3,
    hard_core_scale=1.10,
    nonbond_push_scale=0.8,
    displacement_sigma=0.004,
)
```

## Relaxation trajectory

<iframe src="../../_static/trajectories/srtio3_lro.html"
        width="100%" height="600"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

## g3 distribution

<iframe src="../../_static/g3/srtio3_lro.html"
        width="100%" height="720"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

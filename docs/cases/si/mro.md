# MRO

Medium-range ordered silicon. Grains of ~13 A diameter produce 4-5 visible maxima in the radial profile, with broad peaks decreasing in amplitude.

## Parameters

```python
cell.generate(
    shell_target,
    num_steps=150,
    grain_size=13.0,
    bond_weight=1.9,
    angle_weight=0.9,
    repulsion_weight=2.5,
    hard_core_scale=0.95,
    nonbond_push_scale=0.7,
    displacement_sigma=0.04,
)
```

## Relaxation trajectory

*Trajectory viewer will be embedded here once `si_mro.html` is generated.*

```{raw} html
<!-- <iframe src="../../_static/trajectories/si_mro.html" width="100%" height="640" frameborder="0"></iframe> -->
```

## g3 distribution

*g3 plot will be embedded here once `si_mro_g3.html` is generated.*

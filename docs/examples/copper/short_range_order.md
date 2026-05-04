# Short-range order

Copper in the short-range order (SRO) regime. Random starting
positions (no grain seeding) relaxed with a slightly stiffer bond
spring over more steps than the amorphous regime: a well-defined
first neighbour shell at 2.55 Å forms, and a bump of second-shell
density starts to stand out from the background, but no crystalline
patches yet.

## Parameters

```python
from ase.build import bulk
import tricor as tc

atoms = bulk("Cu", "fcc", a=3.615)
shell_target = tc.CoordinationShellTarget.from_atoms(atoms, phi_num_bins=90)

cell = tc.Supercell.from_atoms(
    atoms,
    cell_dim_angstroms=(40, 40, 40),
    r_max=10, r_step=0.1, phi_num_bins=90,
    rng_seed=42,
)
cell.generate(
    shell_target,
    num_steps=100,
    grain_size=7.0,
    bond_weight=0.6,
    angle_weight=0.0,
    repulsion_weight=1.0,
    hard_core_scale=0.88,
    nonbond_push_scale=0.65,
    displacement_sigma=0.06,
)
```

The weak angle spring nudges local coordination toward FCC-like geometry
without enforcing any of the four first-shell angles strictly. A
`nonbond_push_scale` of 0.85 places the effective first-shell radius close
to, but still slightly inside, the reference `pair_peak`.

## Relaxation trajectory

Interactive 3D viewer of the shell-relaxation trajectory (40 × 40 × 40 Å cell). Drag to rotate, scroll to zoom. Controls below the canvas play,
scrub, and change playback speed.

<iframe src="../../_static/trajectories/cu_sro.html"
        width="100%" height="600"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

## g3 distribution

Measured from the **final (post-relaxation) atoms**. The heatmap is the
reduced three-body density in units of the uniform random reference, where white
= 1.0, blue = depleted, red = enhanced. The lower panel shows the pair
profile g(r); the shaded amber band marks the first-neighbour shell used as
the root-bond integration window for the g3 slice.

<iframe src="../../_static/g3/cu_sro.html"
        width="100%" height="520"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

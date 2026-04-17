# Short-range order

Copper in the short-range order (SRO) regime. A standard 100-step
relaxation with moderate bond and angle springs tightens the first
neighbour shell and starts to pick up local FCC-like packing, while
longer-range correlations remain washed out.

## Parameters

```python
from ase.build import bulk
import tricor as tc

atoms = bulk("Cu", "fcc", a=3.615)
shell_target = tc.CoordinationShellTarget.from_atoms(atoms, phi_num_bins=90)

cell = tc.Supercell.from_atoms(
    atoms,
    cell_dim_angstroms=(20, 20, 20),
    r_max=10, r_step=0.1, phi_num_bins=90,
    rng_seed=42,
)
cell.generate(
    shell_target,
    num_steps=120,
    grain_size=None,
    bond_weight=1.1,
    angle_weight=0.12,
    repulsion_weight=1.3,
    hard_core_scale=0.90,
    nonbond_push_scale=0.85,
)
```

The weak angle spring nudges local coordination toward FCC-like geometry
without enforcing any of the four first-shell angles strictly. A
`nonbond_push_scale` of 0.85 places the effective first-shell radius close
to, but still slightly inside, the reference `pair_peak`.

## Relaxation trajectory

Interactive 3D viewer of the shell-relaxation trajectory (650 atoms, 121
frames). Drag to rotate, scroll to zoom. Controls below the canvas play,
scrub, and change playback speed.

<iframe src="../../_static/trajectories/cu_sro.html"
        width="100%" height="600"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

## g3 distribution

Measured from the **final (post-relaxation) atoms**. The heatmap is the
reduced three-body density in units of the uniform random reference - white
= 1.0, blue = depleted, red = enhanced. The lower panel shows the pair
profile g(r); the shaded amber band marks the first-neighbour shell used as
the root-bond integration window for the g3 slice.

<iframe src="../../_static/g3/cu_sro.html"
        width="100%" height="520"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

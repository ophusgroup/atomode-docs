# 10 Å nanocrystalline

Silicon in the nanocrystalline regime: crystalline grains are seeded at
~15 Å initial diameter, their interiors are held close to the diamond-cubic
reference, and the spring network relaxes the grain boundaries.  The
relaxed grain size is typically a little smaller than the initial diameter,
so the preset-level labels (e.g. `nanocrystalline_10`) are best treated as
nominal tags for the regime rather than exact post-relaxation dimensions.
See the [preset summary](index.md#preset-summary) for the full parameter
set.

## Parameters

```python
from ase.build import bulk
import tricor as tc

atoms = bulk("Si", "diamond", a=5.431)
shell_target = tc.CoordinationShellTarget.from_atoms(atoms, phi_num_bins=90)

cell = tc.Supercell.from_atoms(
    atoms,
    cell_dim_angstroms=(20, 20, 20),
    r_max=10, r_step=0.1, phi_num_bins=90,
    rng_seed=42,
)
cell.generate(shell_target, **tc.Supercell.PRESETS["nanocrystalline_10"])
```

## Relaxation trajectory

Interactive 3D viewer of the shell-relaxation trajectory (384 atoms, 201 frames).
Drag to rotate, scroll to zoom. Controls below the canvas play, scrub, and
change playback speed.

<iframe src="../../_static/trajectories/si_nanocrystalline_10.html"
        width="100%" height="600"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

## g3 distribution

Measured from the **final (post-relaxation) atoms**. The heatmap is the
reduced three-body density in units of the uniform random reference - white
= 1.0, blue = depleted, red = enhanced. The lower panel shows the pair
profile g(r); the shaded amber band marks the first-neighbour shell used as
the root-bond integration window for the g3 slice. For silicon there is a
single Si-Si-Si triplet channel.

<iframe src="../../_static/g3/si_nanocrystalline_10.html"
        width="100%" height="520"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

# Nanocrystalline

Silicon in the nanocrystalline regime: a single ~20 Å grain spans the
20 × 20 × 20 Å supercell (`grain_size ≥ min(box_dim)` triggers the
identity-rotation single-grain path), so the cell reads as a coherent
diamond-cubic tile. With the bigger grain + stronger springs compared to
``MRO_more``, this panel is the most ordered of the six - sharper first
and second g(r) peaks and the clearest tetrahedral g3 signature.

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
cell.generate(shell_target, **tc.Supercell.PRESETS["nanocrystalline"])
```

## Relaxation trajectory

Interactive 3D viewer of the shell-relaxation trajectory (384 atoms, 201 frames).
Drag to rotate, scroll to zoom. Controls below the canvas play, scrub, and
change playback speed.

<iframe src="../../_static/trajectories/si_nanocrystalline.html"
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

<iframe src="../../_static/g3/si_nanocrystalline.html"
        width="100%" height="520"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

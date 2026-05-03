# Liquid

SrTiO₃ in the liquid regime: random Sr / Ti / O positions at the
correct 1 : 1 : 3 stoichiometry and density, followed by a short shell
relaxation that enforces only the hard-core exclusion. No TiO₆
octahedra survive.

## Parameters

See [Strontium titanate](index.md#supercell) for the reference crystal
and `with_bonded_species_pairs([('Ti', 'O')])` setup. Then:

```python
cell.generate(
    shell_target,
    num_steps=200,
    grain_size=None,
    bond_weight=0.10,
    angle_weight=0.0,
    repulsion_weight=1.0,
    hard_core_scale=1.10,
    nonbond_push_scale=0.6,
    displacement_sigma=0.02,
)
```

## Relaxation trajectory

<iframe src="../../_static/trajectories/srtio3_liquid.html"
        width="100%" height="600"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

## g3 distribution

<iframe src="../../_static/g3/srtio3_liquid.html"
        width="100%" height="720"
        style="border: 1px solid rgba(0,0,0,0.1); border-radius: 6px;"
        loading="lazy"></iframe>

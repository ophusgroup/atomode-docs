# Silicon dioxide

Silicon dioxide (α-quartz) is a two-species oxide built from corner-sharing
SiO₄ tetrahedra. The g3 distribution has distinct Si-O and O-O channels,
so the framework exercises all of tricor's per-species-pair machinery.

## Reference crystal

```python
from ase.io import read
atoms = read("SiO2.cif")   # α-quartz primitive or conventional cell
```

For binary systems the `CoordinationShellTarget` automatically picks up
per-pair first-shell distances and target angles from the reference:

```python
import tricor as tc
shell_target = tc.CoordinationShellTarget.from_atoms(atoms, phi_num_bins=90)
```

## Status

Planned. The workflow is identical to the silicon case
([Silicon](../silicon/index.md)) - the only change is loading an α-quartz
reference instead of diamond-cubic Si.

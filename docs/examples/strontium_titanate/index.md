# Strontium titanate

Strontium titanate (SrTiO₃) is a cubic perovskite (*a* = 3.905 Å) with three
distinct sublattices: Sr sits in the corners (12-coordinated by O), Ti in
the body centre (6-coordinated by O, octahedral), and each O bridges
between two Ti and is surrounded by four Sr. This makes the measured g3
distribution particularly rich - every possible triplet type (Sr-Sr-Sr,
Sr-Ti-O, O-Ti-O, …) is populated.

## Reference crystal

```python
from ase.io import read
atoms = read("SrTiO3.cif")   # cubic perovskite
```

## Status

Planned. The workflow is identical to the silicon case
([Silicon](../silicon/index.md)) - the added complexity is handled entirely
by `CoordinationShellTarget`, which auto-detects per-species-pair
coordination numbers and target angles from the reference crystal.

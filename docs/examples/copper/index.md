# Copper

Copper (face-centred cubic, *a* = 3.615 Å). Twelve-fold close-packed
coordination with a broad angular distribution; metallic bonding calls for
a different preset than the covalent silicon reference.

## Reference crystal

```python
from ase.build import bulk
atoms = bulk("Cu", "fcc", a=3.615)
```

## Status

A full six-regime walkthrough for copper is planned but not yet ready.
Until it lands, the silicon case (diamond cubic, fourfold coordination)
is the reference example - see [Silicon](../silicon/index.md).

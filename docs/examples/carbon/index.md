# Carbon

Carbon supports a wide range of structural regimes - graphitic sp²
networks, diamond-like sp³, and amorphous mixtures of the two. A full
walkthrough is planned but not yet ready.

## Reference crystal

```python
from ase.build import bulk

# Diamond cubic reference (sp³)
atoms_diamond = bulk("C", "diamond", a=3.567)

# Graphite reference (sp²)
atoms_graphite = bulk("C", "graphite", a=2.461, c=6.708)
```

## Status

Planned. In the meantime, see [Silicon](../silicon/index.md) for the
reference workflow - the diamond-cubic carbon case follows it directly.

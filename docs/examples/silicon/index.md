# Silicon

Silicon (diamond cubic, a = 5.431 A). 4-fold tetrahedral coordination with Si-Si-Si bond angle of 109.5 degrees. The reference case for the 7 disorder regimes.

## Reference crystal

```python
from ase.build import bulk
atoms = bulk('Si', 'diamond', a=5.431)
```

## Disorder regimes

Click any regime for the full interactive trajectory viewer and g3 distribution.

```{toctree}
:maxdepth: 1

liquid
amorphous
short_range_order
medium_range_order
extended_medium_range_order
nanocrystalline_10
nanocrystalline_20
```

## Overview grid

*Visual grid with thumbnails coming soon - will show g3 + structure snapshot for each regime.*

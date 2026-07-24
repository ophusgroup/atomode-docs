---
title: Installation
---

# Installation

atomode requires Python ≥ 3.10.

```bash
pip install atomode
```

Or from source:

```bash
git clone https://github.com/ophusgroup/atomode
cd atomode
pip install -e .
```

## Optional extras

Some workflows need extra dependencies:

```bash
# electron-microscopy training pairs (abTEM-backed potentials/exit waves)
pip install -e '.[training]'
```

<!-- TODO: document GPU / performance notes and supported platforms. -->

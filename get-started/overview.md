---
title: Overview
---

# Overview

atomode builds atomistic supercells anywhere on the order–disorder spectrum:

- **Amorphous** — no long-range order, a target radial distribution function.
- **SRO / MRO** — short- and medium-range order, tunable via grain size.
- **NC** — nanocrystalline, a mosaic of misoriented crystalline grains.
- **LRO** — long-range-ordered single crystals.

The degree of order is a continuous parameter, so graded cells (ordered at one
end, disordered at the other) are built in a single pass.

## How it works

1. **Seed** the cell with Voronoi sites whose density sets the local grain size.
2. **Assemble** grains from a reference motif (or as a disordered network).
3. **Relax** the structure so it matches the target correlation functions.

<!-- TODO: expand each stage; add a schematic figure. -->

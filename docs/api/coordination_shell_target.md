# CoordinationShellTarget

First-shell coordination targets extracted from a reference crystal via
[Gaussian-mixture decomposition](../algorithms/glossary.md) of each
species-pair g(r) and of each rooted-angle distribution.  The result
drives the bond-length, angle, and repulsion springs in
{meth}`Supercell.generate` / {meth}`Supercell.shell_relax`.

```{eval-rst}
.. autoclass:: tricor.CoordinationShellTarget
   :members:
      from_atoms,
      from_targets,
      with_cross_species_bonds_only,
      with_bonded_species_pairs,
      with_angle_triplets,
      without_angle_triplets
   :undoc-members:
```

## Restricting the bond graph

By default every species pair with a first-shell peak contributes bond
and angle springs.  In multi-element compounds where only a subset of
pairs represent *actual* chemical bonds (e.g. Si-O in silica;
Ti-O in perovskites), the `angle_mode_deg` values extracted for the
other pairs are geometric artefacts of the reference sampling rather
than physical targets - relaxing against them can destroy the
coordination geometry you're trying to preserve.  Two helpers
produce a modified target where the unwanted pairs are set to
zero coordination:

```python
# SiO2: only Si-O is a real bond (equivalent to the two-species helper)
st = tc.CoordinationShellTarget.from_atoms(atoms, phi_num_bins=90)
st = st.with_cross_species_bonds_only()

# SrTiO3: both Ti-O and Sr-O are real bonds.  The SrO12 cuboctahedron
# is multi-modal (60°/90°/120°/180°) so Sr-centered angle springs
# would strain the other modes — mask them out but keep the Ti-O
# distance springs intact.
st = (
    tc.CoordinationShellTarget.from_atoms(atoms, phi_num_bins=90)
    .with_bonded_species_pairs([('Ti', 'O'), ('Sr', 'O')])
    .with_angle_triplets([('Ti', 'O', 'O'), ('O', 'Ti', 'Ti')])
)
```

## Masking angle springs (multi-modal shells)

Some coordination shells are **multi-modal** — the single
`angle_mode_deg` peak that `from_atoms` extracts is just the tallest
bar of a distribution with several physically valid modes.  The
canonical example is the 12-coordinated cuboctahedron (Cu FCC, SrO₁₂
in SrTiO₃) whose angle distribution sits at 60° / 90° / 120° / 180°
simultaneously — enforcing any one mode distorts the others.

Two helpers operate on the `angle_enabled_mask` field:

- `with_angle_triplets(triplets)` — whitelist; enable angle springs
  only for the listed triplet types.
- `without_angle_triplets(triplets)` — blacklist; disable angle
  springs for the listed triplets, keep the rest.

Bond-distance springs are unaffected — masking only controls the
angle force term.  For copper, the whole thing is replaced with
`angle_weight=0.0` in the regime presets, but for mixed compounds
like SrTiO₃ you want 90° preserved on the TiO₆ octahedron while
silencing the Sr-centered cuboctahedron:

```python
st.with_angle_triplets([
    ('Ti', 'O', 'O'),    # O-Ti-O at 90° (octahedral)
    ('O',  'Ti', 'Ti'),  # Ti-O-Ti at 180° (linear backbone)
])
```

## Blending two reference crystals

For materials with a controllable phase mix (sp²/sp³ carbon; SiO₂ /
Si₃N₄ nitride-silica blends; etc.) extract one shell target per
chemistry and combine them with `from_targets`:

```python
shell_sp2 = tc.CoordinationShellTarget.from_atoms(atoms_graphite, phi_num_bins=90)
shell_sp3 = tc.CoordinationShellTarget.from_atoms(atoms_diamond,  phi_num_bins=90)
shell_target = tc.CoordinationShellTarget.from_targets(
    {"sp2": shell_sp2, "sp3": shell_sp3},
)
```

The composite target holds **virtual species** (e.g. ``sp2_C`` at
index 0, ``sp3_C`` at index 1) — both atomic number 6, but with
distinct ``coordination_target`` rows (3 vs 4), ``pair_peak`` (1.42
vs 1.54 Å), and ``angle_mode_deg`` (120° vs 109.5°).  Each atom's
virtual species is assigned at grain-build time via
``Supercell.generate(..., grain_sources=[...])`` (see
[Carbon example](../examples/carbon/index.md)); the relaxer then
pulls each atom toward the geometry of its source crystal.

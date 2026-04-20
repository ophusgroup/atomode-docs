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
      with_cross_species_bonds_only,
      with_bonded_species_pairs
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

# SrTiO3: only Ti-O is a real bond (Sr is a spectator)
st = tc.CoordinationShellTarget.from_atoms(atoms, phi_num_bins=90)
st = st.with_bonded_species_pairs([('Ti', 'O')])
```

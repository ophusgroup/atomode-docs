# CoordinationShellTarget

First-shell coordination targets extracted from a reference crystal via
[Gaussian-mixture decomposition](../algorithms/glossary.md) of each
species-pair g(r) and of each rooted-angle distribution.  The result
drives the bond-length, angle, and repulsion springs in
`atomode.Supercell.generate` /
`atomode.Supercell.shell_relax`.

```python
class atomode.CoordinationShellTarget
```

### Construction

#### `from_atoms(atoms: 'Atoms', *, phi_num_bins: 'int' = 72, shell_hist_step: 'float' = 0.05, shell_smooth_sigma_bins: 'float' = 1.2, extract_cutoff: 'float | None' = None, auto_filter_lattice_artifacts: 'bool' = True, label: 'str | None' = None) -> "'CoordinationShellTarget'"`

Extract first-shell coordination, distance, and angle targets from a reference crystal.

For every species pair in ``atoms`` the method fits the first
peak of the radial pair distribution g(r) — its inner edge,
peak position, Gaussian width, and outer edge — and counts the
average number of neighbours each centre atom has within that
window.  For every triplet (centre, neighbour-A, neighbour-B)
species combination it builds a histogram of bond angles
ranged 0–180° using ``phi_num_bins`` bins, identifying the
dominant angle mode.  All quantities are stored as 2-D /
3-D numpy arrays indexed by species index in ``species``.

**Parameters**
atoms : ase.Atoms
    Reference crystal whose g(r) and bond-angle distributions
    define the target geometry.  Must be a periodic cell with
    at least one neighbour pair within
    ``extract_cutoff`` (auto if ``None``).
phi_num_bins : int, optional
    Number of bins used to discretise the [0, 180°] bond-angle
    axis.  Default ``72`` (2.5° per bin).  Higher values
    sharpen the angle target but slow down the angle
    measurement loop in :meth:`Supercell.measure_g3`.
shell_hist_step : float, optional
    Bin width (Å) of the per-pair radial histogram used to
    locate the first peak.  Default ``0.05`` Å.
shell_smooth_sigma_bins : float, optional
    Gaussian smoothing width (in bins) applied to the radial
    histogram before peak detection.  Default ``1.2`` bins.
extract_cutoff : float, optional
    Maximum centre-neighbour distance (Å) considered when
    building the neighbour list.  If ``None`` the routine picks
    ``min(default, max(3.8 × NN, NN + 2))`` based on the
    inferred nearest-neighbour distance.
auto_filter_lattice_artifacts : bool, optional
    If ``True`` (default), zero out ``coordination_target`` for
    species pairs that represent lattice artefacts rather than
    real chemical bonds.  A pair ``(i, j)`` is kept only when
    ``pair_peak[i, j]`` is the smallest enabled peak in
    either row ``i`` or column ``j``.  This automatically
    silences the second-shell ``Si-Si`` / ``O-O`` springs in
    ``SiO2``, the ``Sr-Sr`` / ``Ti-Ti`` / ``O-O`` / ``Sr-Ti``
    springs in ``SrTiO3``, etc.  Set to ``False`` to keep every
    extracted pair; callers can also override the filter by
    chaining :meth:`with_bonded_species_pairs` after
    extraction.
label : str, optional
    Free-text identifier carried along on the returned target
    (used in plot legends and HTML viewer titles).  Default
    uses the chemical formula of ``atoms``.

**Returns**
CoordinationShellTarget
    Frozen dataclass populated with every per-species and
    per-triplet field listed in the class header
    (``coordination_target``, ``pair_peak``, ``pair_inner``,
    ``angle_target``, ``angle_mode_deg``, etc.).  All ndarray
    fields are pre-symmetrised over species pairs and the
    angle-enabled mask is initialised to ``True`` everywhere.

**Notes**
Single-element references (Si, Cu, …) produce a 1×1
coordination matrix and one self-self angle channel.
Multi-element references (SiO₂, SrTiO₃, …) populate every
cross-pair entry — see
:meth:`with_cross_species_bonds_only` and
:meth:`with_bonded_species_pairs` for masking helpers when
only a subset of pairs represents real chemical bonds.

**Examples**
>>> from ase.build import bulk
>>> import atomode as tc
>>> atoms = bulk("Si", "diamond", a=5.431)
>>> shell = tc.CoordinationShellTarget.from_atoms(atoms,
...                                                phi_num_bins=90)
>>> shell.coordination_target  # 4 NN per Si
array([[4.]])
>>> float(shell.pair_peak[0, 0])
2.352

#### `from_targets(targets: "'dict[str, CoordinationShellTarget]'", *, cross_pair_peak: "'dict[tuple[str, str], float] | None'" = None, cross_pair_outer_scale: 'float' = 1.15, label: 'str | None' = None) -> "'CoordinationShellTarget'"`

Stack multiple shell targets into one with a widened species axis.

Used for blended materials where atoms share an atomic number but
want different local coordination (e.g. graphite sp² + diamond
sp³ carbon).  Each input target contributes a *virtual species
slot* per element of its ``species`` array; the composite target's
``species`` is the concatenation of all inputs, with
``species_labels`` rewritten as ``f"{key}_{element}"``.

Cross-target pairs default to:

- ``coordination_target = 0`` (no bonds form across virtual
  species boundaries; the repulsion term still keeps them apart),
- ``pair_peak = mean(peak_a, peak_b)`` unless overridden by
  ``cross_pair_peak``,
- ``pair_outer = max(outer_a, outer_b) * cross_pair_outer_scale``,
- ``pair_hard_min`` / ``pair_inner`` pro-rated from the two
  source values.

Cross-target triplets (any of the three species drawn from a
different source than the other two) get
``coordination_target = 0`` and zero ``angle_mode_deg`` - the
relaxer will never enumerate these triplets because no such
bonds form.

**Parameters**
targets
    Mapping ``{key: CoordinationShellTarget}``.  Insertion order
    defines the virtual-species order.
cross_pair_peak
    Optional overrides for ``pair_peak`` between elements drawn
    from different source targets.  Keys are ``(key_a, key_b)``
    with symbol lookup done via ``atomic_numbers`` when pair
    contains non-tuple element labels.
cross_pair_outer_scale
    Multiplier applied to the larger of the two source
    ``pair_outer`` values when populating cross-target entries.
label
    Optional label; defaults to ``"composite(" + keys + ")"``.

### Modifiers

#### `with_cross_species_bonds_only() -> "'CoordinationShellTarget'"`

Return a copy where same-species ``coordination_target`` entries are zeroed.

Useful for network-former compounds such as SiO₂ where only
cross-species pairs (Si-O) are real chemical bonds; the same-species
"shell" peaks (Si-Si, O-O) come from the second coordination shell
through the bridging atom and should not be treated as bonds by
:meth:`Supercell.shell_relax` (which would otherwise install
spurious angle springs on triplets like Si-Si-Si or O-O-O whose
``angle_mode_deg`` is just a geometric artefact of the reference
sampling, not a physical target).

**Returns**
CoordinationShellTarget
    New target whose ``coordination_target`` diagonal is
    zeroed (off-diagonal cross-species entries preserved).
    The original target is unmodified.

#### `with_bonded_species_pairs(pairs: "'list[tuple[str, str]]'") -> "'CoordinationShellTarget'"`

Return a copy whose ``coordination_target`` is zero everywhere except for the listed species pairs.

Useful for materials with spectator ions: perovskites like
SrTiO₃ want only Ti-O bonds considered by
:meth:`Supercell.shell_relax`, since Sr-O, Sr-Ti, O-O, Ti-Ti, etc.
would either install spurious angle springs (``angle_mode_deg``
is a geometric artefact for non-bond triplets) or pin atoms via
bond springs to distances that are really second-shell
separations, not chemical bonds.

**Parameters**
pairs : list of tuple of str
    Each ``(symbol_a, symbol_b)`` pair is treated symmetrically
    — both directions in the ``coordination_target`` matrix
    are preserved.  Pairs whose symbols don't appear in
    ``self.species_labels`` are silently skipped.

**Returns**
CoordinationShellTarget
    A new ``CoordinationShellTarget`` (the original is left
    unmodified) whose ``coordination_target`` keeps only the
    listed species-pair entries; every other slot is zeroed
    so :meth:`Supercell.shell_relax` won't try to enforce
    bonds there.

**Examples**
.. code-block:: python

    # SrTiO3: preserve only TiO6 octahedra
    st.with_bonded_species_pairs([('Ti', 'O')])

    # SiO2: equivalent to ``with_cross_species_bonds_only`` for a
    # binary, but explicit about what a bond is
    st.with_bonded_species_pairs([('Si', 'O')])

#### `with_angle_triplets(triplets: "'list[tuple[str, str, str]]'") -> "'CoordinationShellTarget'"`

Return a copy whose angle-spring mask is enabled *only* for
the listed triplet types; all other angle springs are disabled.

Each triplet is ``(centre_symbol, neighbour_1_symbol,
neighbour_2_symbol)``; both (n1, n2) and (n2, n1) are enabled
automatically.  Bond-distance springs are untouched - only the
angle springs installed during ``shell_relax`` are filtered.

Useful for multi-modal shells where the extracted
``angle_mode_deg`` picks one peak of a bimodal / quadrimodal
distribution; enforcing it would strain the other modes.
SrTiO₃'s SrO₁₂ cuboctahedron (O-Sr-O angles at
60°/90°/120°/180°) is the canonical example.

**Parameters**
triplets : list of tuple of str
    Each ``(centre, n1, n2)`` triplet enables the angle-spring
    term for that combination of species.  Ordering of ``n1``
    and ``n2`` is symmetrised internally.

**Returns**
CoordinationShellTarget
    New target whose ``angle_enabled_mask`` is ``True`` only
    for the listed triplets; every other triplet's angle
    spring is silenced.

**Examples**
.. code-block:: python

    # Keep Ti-centered 90° and linear O-Ti-Ti 180° angle
    # springs; silence every Sr-centered or Sr-in-triplet
    # angle spring.
    st.with_angle_triplets([
        ('Ti', 'O', 'O'),
        ('O',  'Ti', 'Ti'),
    ])

#### `without_angle_triplets(triplets: "'list[tuple[str, str, str]]'") -> "'CoordinationShellTarget'"`

Return a copy with the angle mask disabled for the listed triplets.

Inverse of :meth:`with_angle_triplets`: starts from the
current ``angle_enabled_mask`` and turns OFF the listed
triplets, leaving every other triplet's angle spring intact.

**Parameters**
triplets : list of tuple of str
    Each ``(centre, n1, n2)`` triplet disables the angle
    spring for that species combination.

**Returns**
CoordinationShellTarget
    New target whose ``angle_enabled_mask`` matches the
    original except the listed triplets are now ``False``.

### Helpers

#### `pair_labels`

*(property)* Human-readable species-pair labels for every present pair.

**Returns**
list of str
    One ``"<centre>-<neighbour>"`` string per ``(centre,
    neighbour)`` slot in ``self.pair_mask`` that is ``True``.
    Order matches the row-major flatten of the species table
    (centre, neighbour) — useful for legend labels in
    multi-pair g(r) plots.

#### `angle_labels`

*(property)* Human-readable rooted-angle labels for every triplet channel.

**Returns**
list of str
    One ``"<n1>-<centre>-<n2>"`` string per row of
    ``self.angle_index``.  Useful for labelling angle-channel
    histograms or filtering the per-triplet output of
    :meth:`Supercell.measure_g3`.

## Restricting the bond graph

In multi-element compounds only a subset of species pairs represent
*actual* chemical bonds (e.g. Si-O in silica; Ti-O and Sr-O in
perovskites) — the other pairs' first-shell peaks are lattice
separations through a bridging atom, and relaxing against them can
destroy the coordination geometry.  `from_atoms` zeroes those
lattice-artefact pairs automatically
(`auto_filter_lattice_artifacts=True`): any pair whose `pair_peak`
is not the smallest in either its row or column is excluded.  Two
helpers set the bond graph explicitly when the automatic rule is not
what you want:

```python
# SiO2: only Si-O is a real bond (equivalent to the two-species helper)
st = am.CoordinationShellTarget.from_atoms(atoms, phi_num_bins=90)
st = st.with_cross_species_bonds_only()

# SrTiO3: both Ti-O and Sr-O are real bonds.  The SrO12 cuboctahedron
# is multi-modal (60°/90°/120°/180°) so Sr-centered angle springs
# would strain the other modes; mask them out but keep the Ti-O
# distance springs intact.
st = (
    am.CoordinationShellTarget.from_atoms(atoms, phi_num_bins=90)
    .with_bonded_species_pairs([('Ti', 'O'), ('Sr', 'O')])
    .with_angle_triplets([('Ti', 'O', 'O'), ('O', 'Ti', 'Ti')])
)
```

## Masking angle springs (multi-modal shells)

Some coordination shells are **multi-modal**: the single
`angle_mode_deg` peak that `from_atoms` extracts is just the tallest
bar of a distribution with several physically valid modes.  The
canonical example is the 12-coordinated cuboctahedron (Cu FCC, SrO₁₂
in SrTiO₃) whose angle distribution sits at 60° / 90° / 120° / 180°
simultaneously, so enforcing any one mode distorts the others.

Two helpers operate on the `angle_enabled_mask` field:

- `with_angle_triplets(triplets)`: whitelist; enable angle springs
  only for the listed triplet types.
- `without_angle_triplets(triplets)`: blacklist; disable angle
  springs for the listed triplets, keep the rest.

Bond-distance springs are unaffected; masking only controls the
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
shell_sp2 = am.CoordinationShellTarget.from_atoms(atoms_graphite, phi_num_bins=90)
shell_sp3 = am.CoordinationShellTarget.from_atoms(atoms_diamond,  phi_num_bins=90)
shell_target = am.CoordinationShellTarget.from_targets(
    {"sp2": shell_sp2, "sp3": shell_sp3},
)
```

The composite target holds **virtual species** (e.g. ``sp2_C`` at
index 0, ``sp3_C`` at index 1): both atomic number 6, but with
distinct ``coordination_target`` rows (3 vs 4), ``pair_peak`` (1.42
vs 1.54 Å), and ``angle_mode_deg`` (120° vs 109.5°).  Each atom's
virtual species is assigned at grain-build time via
``Supercell.generate(..., grain_sources=[...])`` (see
[Carbon example](../examples/carbon/index.md)); the relaxer then
pulls each atom toward the geometry of its source crystal.

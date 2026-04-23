# Glossary

## Disorder regimes

**Liquid**
: A structure with only nearest-neighbour correlations enforced. No grain construction; atoms are placed randomly and relaxed with weak angle springs.

**Amorphous**
: Short-range order limited to the first nearest-neighbour shell. Constructed from very small grains (~6 A) with heavy broadening.

**Short-range order (SRO)**
: Correlations extend out to ~3 visible maxima in the pair correlation function. Constructed from small grains (~10 A).

**Medium-range order (MRO)**
: Correlations extend to 4-5 visible maxima. Constructed from grains of ~13 A.

**Extended medium-range order**
: Larger grains (~18 A) extend correlations further (8-10 A range).

**Nanocrystalline**
: Grains filling the box with sharp crystalline peaks. Grain size determines the crystallite domain size (e.g. 10 A, 20 A nanocrystalline).

## Three-body distribution

**g3**
: Rooted three-body distribution. A 4D histogram `g3[type, r01, r02, phi]` counting triplets of atoms (centre and two neighbours) by their two radial distances and bond angle.

**Triplet type**
: Species combination of a rooted triplet, written as `centre | neigh1 neigh2`. For SiC: `Si | Si Si`, `Si | Si C`, `Si | C C`, `C | C C`, `C | C Si`, `C | Si Si`.

**g2**
: Pair distribution. A 2D histogram `g2[species_pair, r]` counting all atomic pairs by their interatomic distance.

**Reduced g3**
: Density-normalised g3, approaching 1.0 in the random limit. Computed as `g3 / (A * r01^2 * r02^2 * sin(phi))`.

## Coordination shell target

**pair_peak**
: Mean nearest-neighbour distance for each species pair, extracted from the reference crystal.

**pair_inner, pair_outer**
: Inner and outer radial boundaries of the first coordination shell.

**pair_hard_min**
: Absolute minimum distance (hard-core overlap prevention).

**coordination_target** (K)
: Expected number of neighbours of a given species around each centre species. For Si diamond: K_Si-Si = 4. For SiC zincblende: K_Si-C = K_C-Si = 4, K_Si-Si = K_C-C = 0.

**angle_mode_deg**
: Most probable bond angle for each triplet type in the reference crystal.

**angle_enabled_mask**
: Per-triplet bool array that controls whether `shell_relax` installs
  an angle spring for that triplet type.  Bond-distance springs are
  always installed (independent of this mask).  Used to silence
  multi-modal cases (cuboctahedral SrO₁₂ in SrTiO₃, whose O-Sr-O
  distribution is spread over 60°/90°/120°/180° so picking one mode
  distorts the others).  Toggled via
  {meth}`~tricor.CoordinationShellTarget.with_angle_triplets` /
  {meth}`~tricor.CoordinationShellTarget.without_angle_triplets`.

## Grain construction

**grain_size**
: Diameter of crystalline grains in Angstrom. Smaller grains give fewer visible shells in g3.

**crystalline_fraction**
: Volume fraction filled by crystalline grains. The rest is amorphous fill. 1.0 = all grains, 0.0 = all random.

**Voronoi cell**
: Region of space closer to one grain seed than any other. The supercell box is partitioned into one Voronoi cell per seed.

**Grain boundary**
: Region between adjacent grains where atoms belong to different rotations of the reference crystal. Overlaps occur here and are removed.

## Shell relaxation

**bond_weight**
: Spring strength for bond distances in the relaxation.

**angle_weight**
: Spring strength for bond angles.

**repulsion_weight**
: Strength of the short-range repulsive force.

**hard_core_scale**
: Multiplier for the minimum bond distance wall. Values below 1.0 allow shorter bonds (softer wall).

**nonbond_push_scale**
: Multiplier for the non-bonded clearance distance. Values below 1.0 give broader 2nd shells.

**displacement_sigma**
: Gaussian displacement applied to grain atoms before relaxation (Angstrom).

## Composite shell targets

**Composite shell target**
: A single `CoordinationShellTarget` produced by
  `CoordinationShellTarget.from_targets({key: target, ...})` that
  stacks two or more per-chemistry targets into one object with
  a widened species axis.  Used for phase blends (sp²/sp³ carbon,
  potential SiO₂/Si₃N₄ mixes) where atoms share an atomic number
  but want different local coordination.

**Virtual species**
: A species slot in a composite shell target.  Each virtual species
  carries its own row of `coordination_target`, `pair_peak`,
  `angle_mode_deg`, etc.  Multiple virtual species can share an
  atomic number (e.g. sp²_C and sp³_C both have Z=6).

**grain_sources**
: The `generate(..., grain_sources=[{atoms, species_offset,
  weight}, ...])` kwarg that assigns each Voronoi grain a reference
  crystal by weight.  `species_offset` is the virtual-species index
  each atom from that grain receives; the relaxer consults it via
  `Supercell._atom_shell_species_index`.

**atom_species_index**
: Optional `generate(atom_species_index=...)` override - a (num_atoms,)
  array of virtual-species indices.  Used when the caller wants to
  assign virtual species directly rather than letting
  `grain_sources` do it.

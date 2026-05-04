# Three-Body Distribution (g3)

## Definition

The rooted three-body distribution $g_3$ captures pairwise distance and
angular correlations between atomic triplets.  For a centre atom at
position $\mathbf r_0$ with neighbours at $\mathbf r_1$ and $\mathbf r_2$:

- $r_{01} = \lVert \mathbf r_1 - \mathbf r_0 \rVert$
- $r_{02} = \lVert \mathbf r_2 - \mathbf r_0 \rVert$
- $\phi = \arccos\!\left(\dfrac{(\mathbf r_1 - \mathbf r_0) \cdot
  (\mathbf r_2 - \mathbf r_0)}{r_{01} \, r_{02}}\right)$

`G3Distribution.measure_g3` replicates the supercell up to
$r_\text{max}$ and, for every site, accumulates counts into a 4D
histogram

$$\texttt{g3count}[\text{channel}, r_{01}, r_{02}, \phi]$$

over all neighbour pairs $(j, k)$ inside the radial cutoff (with
$j \ne k$ when the two are the same species).  Radial bins use width
$\Delta r = \texttt{r\_step}$; angular bins use
$\Delta \phi = \pi / \texttt{phi\_num\_bins}$.

### Channel indexing

Channels are labelled by **species** triplets
`(centre | neigh_1 neigh_2)` with
`species_idx(neigh_1) ≤ species_idx(neigh_2)`.  For a system with $S$
species the channel count is

$$N_\text{channels} = \frac{S^2 (S + 1)}{2}.$$

Examples: SiO₂ ($S = 2$) → 6 channels (`Si | Si Si`, `Si | Si O`,
`Si | O O`, `O | Si Si`, `O | Si O`, `O | O O`); SrTiO₃ ($S = 3$) →
18 channels.

`g3_index` stores the `(centre, neigh_1, neigh_2)` species indices for
each channel, and `g3_lookup[c, a, b]` maps any ordered species triple
to its channel; both orderings of the two neighbours land on the same
entry so the caller doesn't have to sort.  The atom-pair $(j, k)$ and
$(k, j)$ are added separately when the two neighbour species differ
(symmetrising the $(r_{01}, r_{02})$ plane); when they are the same
species the diagonal is masked so no atom pairs with itself.

## Reduced coordinates

The random-limit (ideal gas) g3 scales as $r_{01}^2 \, r_{02}^2 \,
\sin\phi$.  The **reduced** g3 divides this out:

$$\tilde g_3 = \frac{g_3}{A \, r_{01}^2 \, r_{02}^2 \, \sin\phi}$$

where $A$ is a per-channel amplitude estimated from the far-field
mean.  In reduced coordinates $\tilde g_3 \to 1$ in the random limit
and crystalline peaks sit as sharp islands above the background.  The
pairwise byproduct $g_2$ is normalised analogously with the $r^2$
factor divided out.

## Coordination shell target

`CoordinationShellTarget.from_atoms(atoms)` extracts first-shell
structural targets from a reference crystal using ASE's periodic
``neighbor_list`` at an adaptive cutoff (clamped between $2$ Å and
$3.8 \times$ the median nearest-neighbour distance).  The resulting
frozen dataclass exposes (per species pair $(a, b)$):

| Field | Meaning |
|---|---|
| `pair_peak[a, b]` | Mean first-shell radius |
| `pair_inner[a, b]` / `pair_outer[a, b]` | Radial boundaries of the first shell (derived from the histogram minimum) |
| `pair_hard_min[a, b]` | Hard-core overlap radius (`max(0, r_inner − 1.5 σ_r)`) |
| `pair_sigma[a, b]` | First-shell width |
| `pair_mask[a, b]` | `True` iff any first-shell neighbours of this pair exist |
| `coordination_target[a, b]` | Mean number of $b$-neighbours around an $a$-atom |
| `angle_mode_deg[t]` | Most probable bond angle for triplet channel $t$ |
| `angle_target[t, :]` | Full angular histogram (width `phi_num_bins`) |

Triplet channels on the shell target use the same
`(centre, neigh_1 ≤ neigh_2)` indexing (`angle_index`, `angle_lookup`)
as the g3 object, so downstream consumers can re-use the same channel
layout.

### Bond restrictions

Two helpers zero entries of `coordination_target` to enforce
species-pair selectivity during `shell_relax`:

```python
shell_target.with_cross_species_bonds_only()          # zero diagonal: only A–B bonds
shell_target.with_bonded_species_pairs([('Ti', 'O')]) # keep listed pairs, zero the rest
```

Both return a new `CoordinationShellTarget`; the original is unchanged.
This is the mechanism that keeps SiO₂ / SrTiO₃ from developing a
spurious Si-Si or Ti-Ti bond at the second-shell distance.

### Angle-spring masking (multi-modal shells)

For shells with multiple physically valid bond angles (the 12-coord
cuboctahedron at 60°/90°/120°/180°, Sr in SrTiO₃'s SrO₁₂ motif, …)
the single `angle_mode_deg` that gets extracted picks one of the
peaks and forcing it strains the others.  Two helpers flip entries of
`angle_enabled_mask` to silence specific triplet types without
touching their bond-distance springs:

```python
shell_target.with_angle_triplets([('Ti','O','O'), ('O','Ti','Ti')])  # whitelist
shell_target.without_angle_triplets([('Sr','O','O')])                # blacklist
```

For SrTiO₃ the whitelist form keeps Ti-centered 90° (octahedral) and
O | Ti Ti 180° (linear Ti-O-Ti backbone) while silencing every
Sr-centered triplet, consistent with Cu FCC's `angle_weight=0`
treatment of the cuboctahedron.

### Composite shell target

`CoordinationShellTarget.from_targets({key: target, ...})` stacks
several per-chemistry targets into one with a widened species axis.
Each input contributes its own virtual-species rows of
`coordination_target`, `pair_peak`, `angle_mode_deg`, etc.
Cross-target coordination defaults to zero (no bonds form across the
virtual boundary), but cross-target repulsion is preserved so
different phases don't overlap.  Used for the sp²/sp³ carbon ladder
where the two virtual species (`sp2_C`, `sp3_C`) share atomic number
6 but carry distinct coordination (3 vs 4) and angle targets (120°
vs 109.5°).  Per-atom virtual species is assigned at grain-build
time via `Supercell.generate(..., grain_sources=[...])`; see
[Supercell generation](supercell_generation.md) for the grain
mechanism.

# Supercell generation

Disordered supercells are built in two stages: **Voronoi-grain
construction** sets the initial atom positions, and **spring-network
relaxation** refines the local geometry against first-shell targets.
The whole flow lives in `src/tricor/_grain.py` + `_shell_relax.py`.

## Voronoi grain construction

`Supercell.generate(..., grain_size=d)` forwards to
`_build_grain_atoms`, which executes the steps below.  `grain_size=None`
skips steps 1-6 (the random-position initial cell from
`_build_random_atoms` is used directly).

1. **Seed placement.** Drop $N_\text{seeds}$ random points in the
   orthogonal supercell box at

   $$N_\text{seeds} = \left\lceil \frac{V_\text{box}}{V_\text{grain}} \right\rceil,
     \quad V_\text{grain} = \tfrac{4}{3}\pi \left(\tfrac{d_\text{grain}}{2}\right)^3.$$

2. **Periodic Voronoi tessellation.** Replicate the seeds into a 3×3×3
   array of periodic images, call `scipy.spatial.Voronoi`, and keep
   the finite central cell for each original seed.  Each cell is
   stored as a convex polyhedron: `ConvexHull` of its vertices,
   together with the hull's half-space inequalities `A x + b ≤ 0`.

3. **Grain radius.** The radius of the smallest sphere around the
   origin (in seed-local coordinates) that encloses every Voronoi cell:

   $$R_\text{grain} = \max_{\text{seed } s, \text{ vertex } v \in \text{cell}(s)} \lVert v - s \rVert.$$

4. **Master atom block.** Tile the reference basis through all
   integer lattice vectors $i\mathbf a + j\mathbf b + k\mathbf c$ with
   $|i|,|j|,|k| \le \lceil R_\text{grain} / \lambda_\text{min} \rceil + 1$,
   where $\lambda_\text{min}$ is the shortest non-zero Bravais
   translation; crop to atoms within $R_\text{grain}$.  The result is a
   single array of positions + species shared by every grain.

5. **Per-grain rotation + source choice.** Crystalline grains get a
   random rotation $Q \in SO(3)$ drawn via
   `scipy.spatial.transform.Rotation.random`.  A
   **single-box-grain special case** is detected when
   $\sum \mathbb 1[\text{crystalline}] \le 1$ and
   $d_\text{grain}/2 \ge \tfrac{1}{2} \min L_\text{box}$: every grain
   gets the identity rotation and a *shared* random seed offset, so
   the resulting box is one coherent tile of the reference crystal
   (used e.g. for Si / SrTiO₃ nanocrystalline at 20 Å).

   **Multi-source grain sampling.** When `generate(..., grain_sources=
   [{"atoms": ..., "species_offset": k, "weight": w}, ...])` supplies
   more than one reference crystal, each grain independently samples
   a source by the listed weights.  A separate master atom block
   (step 4) is tiled per source; the grain's atoms are cut from that
   source's master block and tagged with the source's
   `species_offset` as their virtual-species index.  This is the
   mechanism behind the carbon sp²/sp³ ladder - graphite grains get
   virtual species 0 (sp²), diamond grains get virtual species 1
   (sp³), and the density target is a weight-averaged blend so the
   denser phase (diamond) isn't trimmed to the sparse phase's
   density at exact-count enforcement (step 7).

6. **Cell filling.** For each grain $g$ with seed $s_g$ and Voronoi
   cell $C_g$:

   - Crystalline grain: keep master-block atoms whose seed-local
     position lies inside the convex hull of $C_g$ (exact face-test
     $A x + b \le \varepsilon$), then translate by $s_g$ and wrap.
   - Amorphous grain: sample $\mathrm{round}(\rho_\text{ref} \cdot V_g)$
     points uniformly inside $C_g$ (tetrahedra decomposition +
     Dirichlet sampling), assign species from the reference
     composition.

7. **Overlap removal + exact-count enforcement.**

   - Tight duplicate cutoff
     $d_\text{dup} = \max(0.5, 0.7 \, r_\text{hard-min})$ for
     crystalline builds, $0.9 \, r_\text{hard-min}$ otherwise.
     Pairs within that radius collapse to one atom (species of the
     surviving atom chosen to favour whichever species is most
     *under* its stoichiometric target).
   - Target per-species counts
     $N_\text{target}(z) = \rho_\text{ref}(z) \cdot V_\text{box} \cdot f_\text{rel}$
     computed via formula-unit rounding (so Si : O stays exactly 1 : 2
     for SiO₂, Sr : Ti : O exactly 1 : 1 : 3 for SrTiO₃).  Surplus
     atoms are randomly dropped; shortfalls are random-placed with a
     rejection filter at $d_\text{pad} = 0.8 \, r_\text{hard-min}$.
     The single-box-grain path skips this step to preserve the
     coherent FCC tile.

8. **Close-pair push.** A few iterations of pairwise geometric
   repulsion move any surviving pair below $d_\text{push}$ outward
   along the pair axis to exactly $d_\text{push}$; positions are
   re-wrapped after each iteration.  Cutoff defaults to the build-
   specific $d_\text{dup}$ for crystalline grains and to the full
   hard-min for amorphous / liquid paths.

9. **Optional thermal displacement.** 3D Gaussian jitter per atom:

   $$\mathbf r_i \leftarrow \mathbf r_i + \sigma \, \boldsymbol\xi_i,
     \qquad \boldsymbol\xi_i \sim \mathcal N(\mathbf 0, \mathbf I_3)$$

   (equivalent to ``positions += rng.normal(0.0, sigma,
   size=positions.shape)``), then re-wrap into the supercell.

## Shell relaxation

The spring-network relaxation simultaneously moves all atoms to match
first-shell targets.  Three force terms contribute at each step; the
per-atom *spring energy* is accumulated into `atom_cost` for the
trajectory viewer's colour scale.

### Bond springs

For each bonded pair $(i, j)$ with target distance $r_\text{target}$
(the `shell_target.pair_peak[z_i, z_j]` entry):

$$\mathbf F_{ij}^\text{bond}
  = k_\text{bond} \, (r_{ij} - r_\text{target}) \, \hat{\mathbf r}_{ij}
  \qquad
  U_{ij}^\text{bond}
  = \tfrac{1}{2} k_\text{bond} \, (r_{ij} - r_\text{target})^2.$$

### Angle springs

For each bonded triplet $(a, c, b)$ centred on atom $c$ with target
angle $\phi_\text{target}$ (the `shell_target.angle_mode_deg` entry
for the triplet's species):

$$\mathbf F_a^\text{angle}
  = \frac{k_\text{angle} \, (\phi - \phi_\text{target})}{r_a}
      \, \mathbf e_{\perp,a},
  \quad
  \mathbf e_{\perp,a}
  = \frac{\hat{\mathbf r}_b - \cos\phi \, \hat{\mathbf r}_a}{\sin\phi}$$

(symmetric expression for $\mathbf F_b$; $\mathbf F_c = -(\mathbf F_a + \mathbf F_b)$).

### Repulsion

Two repulsive terms prevent overlaps and create a clean shell gap.
Define $u = r_\text{wall} / r$ for each pair and let $h = u - 1$.

**Hard core** (acts on all pairs with $u > 1$; wall at
$r_\text{wall} = r_\text{hard-min}$ scaled by `hard_core_scale`):

$$F^\text{hard} = 4 \, k_\text{rep} \, (h + h^2)$$

**Non-bonded clearance** (acts on non-bonded pairs with $u > 1$; wall at
$r_\text{wall} = 1.5 \, r_\text{peak}$ scaled by `nonbond_push_scale`):

$$F^\text{push} = k_\text{rep} \, (h + h^2)$$

Both forces are directed along the pair axis.

### Bond topology

The bond graph is rebuilt every `neighbor_update_interval` steps
(default 10) using a greedy algorithm:

1. Sort all neighbour pairs within $1.5 \, r_\text{peak}$ by distance.
2. Accept a candidate bond $(i, j)$ only if:
   - Neither atom has reached its total coordination target $K_i$ or $K_j$,
   - Neither atom has exceeded the per-species-pair target
     $K_{ij}$ set by `shell_target.coordination_target`,
   - The new bond makes $\ge 60°$ with every existing bond at both
     endpoints (prevents near-colinear bond pairs for covalent
     networks).
3. Species-aware bond restrictions via
   {meth}`CoordinationShellTarget.with_cross_species_bonds_only` or
   {meth}`CoordinationShellTarget.with_bonded_species_pairs` zero the
   corresponding entries of $K_{ij}$, so those pairs cannot be bonded
   even if they pass the distance check (essential for SiO₂ / SrTiO₃ - the second-shell Si-Si / Ti-Ti peak is close enough to pass a
   naive distance test but is not a chemical bond).

### Integration

FIRE-like velocity-Verlet with fixed momentum coefficient and step
decay:

$$\mathbf v_{n+1} = \begin{cases}
0.8 \, \mathbf v_n + \Delta t \, \mathbf F_n & \text{if } \mathbf v_n \cdot \mathbf F_n > 0 \\
\mathbf 0 & \text{otherwise}
\end{cases}$$

Positions are updated, then wrapped via fractional coordinates.  The
step size decays multiplicatively each iteration
($\Delta t \leftarrow \Delta t \cdot 0.995$ by default).  Per-atom
forces are clipped in magnitude at `max_force_clip` before
integration.

### Per-atom cost (spring energy)

The `atom_cost` accumulated into the trajectory's per-frame colour
map is the actual harmonic spring energy:

$$U_i^\text{cost}
  = \tfrac{1}{2} k_\text{bond} \sum_{j \in \mathcal N(i)} (r_{ij} - r_\text{target})^2
  + \tfrac{1}{6} k_\text{angle} \sum_{\text{triplets } (i, c, b)} (\phi - \phi_\text{target})^2
  + (\text{repulsion contributions}).$$

The viewer's global colour scale uses the 99th percentile of
`atom_cost` in the **last quarter of frames** (steady state), not
across the whole trajectory - early frames of liquid-path runs can
have per-atom costs two orders of magnitude larger than the relaxed
state and would otherwise saturate the scale.

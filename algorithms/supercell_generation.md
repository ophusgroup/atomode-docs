# Supercell generation

Disordered supercells are built in two stages: **Voronoi-grain
construction** (this page) sets the initial atom positions, and
**spring-network relaxation** ([FIRE relaxation](fire_relaxation.md))
refines the local geometry against first-shell targets.  An
optional [orientation refinement](orientation_refinement.md) pass
between the two stages walks each grain through small SO(3)
perturbations to seat its lattice in the right basin before FIRE
runs.  The grain-construction flow lives in
`src/atomode/_grain.py`.

`Supercell.generate(..., grain_size=d)` forwards to
`_build_grain_atoms`, which executes the steps below.  `grain_size=None`
skips steps 1-6 (the random-position initial cell from
`_build_random_atoms` is used directly).

## Voronoi grain construction

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
   mechanism behind the carbon sp²/sp³ ladder: graphite grains get
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

After grain construction, the resulting initial atom block is handed
off to **shell relaxation** to refine bond lengths, bond angles, and
non-bonded distances against the first-shell targets:

- [Orientation refinement](orientation_refinement.md): optional
  per-grain SO(3) coordinate search that runs **before** the FIRE
  quench, picking rotations that align each grain's lattice with its
  local neighbourhood.  Enabled with `refine_orientations=True`.
- [FIRE relaxation](fire_relaxation.md): FIRE-style gradient
  descent on the spring-network energy.  Default for
  `Supercell.generate()`.

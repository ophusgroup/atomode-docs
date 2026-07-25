# MACE-MP0 potential

The [MACE refinement examples](../examples_mace/index.md) relax
atomode-generated cells on **MACE-MP0**, a machine-learning interatomic
potential.  This page summarises the energy model (the Hamiltonian
being minimised) and the update strategies atomode's pipeline uses on
it.  atomode does not implement MACE; it consumes the published
`medium-mpa-0` weights through the
[`mace-torch`](https://github.com/ACEsuit/mace) ASE calculator.

References:

> I. Batatia, D. P. Kovács, G. N. C. Simm, C. Ortner, and G. Csányi,
> *MACE: Higher Order Equivariant Message Passing Neural Networks for
> Fast and Accurate Force Fields*, NeurIPS 35 (2022).
> [arXiv:2206.07697](https://arxiv.org/abs/2206.07697)

> I. Batatia *et al.*, *A foundation model for atomistic materials
> chemistry*, [arXiv:2401.00096](https://arxiv.org/abs/2401.00096).

> R. Drautz, *Atomic cluster expansion for accurate and transferable
> interatomic potentials*,
> [Phys. Rev. B **99**, 014104 (2019)](https://doi.org/10.1103/PhysRevB.99.014104)
> — the body-ordered basis MACE builds on.

## Energy model

MACE is a graph neural network over atoms.  The total energy is a sum
of per-atom contributions read out after $T = 2$ rounds of message
passing:

$$
E \;=\; \sum_i E_i,
\qquad
E_i \;=\; \sum_{t=1}^{T} \mathcal R_t\!\big(\mathbf h_i^{(t)}\big),
$$

where $\mathbf h_i^{(t)}$ is the feature vector (node state) of atom
$i$ after layer $t$ and $\mathcal R_t$ is a learned readout.

Each layer first forms the **two-body atomic basis** by summing over
neighbours within the cutoff $r_\text{cut} = 6$ Å:

$$
A_i \;=\; \sum_{j \,:\, r_{ij} < r_\text{cut}}
   R\!\left(r_{ij}\right)\, Y\!\left(\hat{\mathbf r}_{ij}\right)
   \otimes W\,\mathbf h_j^{(t)},
$$

with learned radial functions $R$ (Bessel basis with a smooth
polynomial envelope that takes the interaction to zero at
$r_\text{cut}$) and spherical harmonics $Y$ carrying the angular
information.  The distinguishing MACE step is the **higher-order
product basis**: symmetrised tensor products of up to $\nu = 3$ copies
of $A_i$,

$$
B_i \;=\; \big(\underbrace{A_i \otimes A_i \otimes A_i}_{\nu
\text{ copies}}\big)_{\text{sym}},
$$

so a *single* layer builds messages of body order $\nu + 1 = 4$
(centre atom + three neighbours) — angular and dihedral-like
correlations enter directly rather than through deep stacks of
two-body messages.  Two layers compose these features, giving an
effective receptive field of $2\,r_\text{cut} = 12$ Å and effective
body order far beyond four.  All features are E(3)-equivariant, so
predicted energies are exactly invariant under rotation, translation,
and permutation.

Forces and stress come from exact differentiation of the network
(autograd), so they are consistent with the energy:

$$
\mathbf F_i = -\frac{\partial E}{\partial \mathbf r_i},
\qquad
\sigma = \frac{1}{V}\frac{\partial E}{\partial \varepsilon}.
$$

### The MP0 / MPA-0 training data

The `MACE-MP0` family are *foundation models*: one parameter set
covering the periodic table, trained on DFT relaxation trajectories
from the Materials Project (the **MPtrj** dataset, ~1.5 M
configurations at the PBE / PBE+U level).  The `medium-mpa-0`
checkpoint used in the examples additionally trains on the Alexandria
dataset.  Accuracy on bulk inorganic materials is near-DFT for
energies and forces; known limitations relevant here are short-range
artefacts on far-from-equilibrium geometries (next section).

## Soft-wall regularisation

Foundation models are trained near equilibrium, so strongly disordered
inputs can fall into spurious low-energy basins where atom pairs
approach unphysically closely.  atomode wraps the MACE calculator with
a one-sided per-pair wall (`scripts/_wall_calculator.py` in
atomode-docs):

$$
U_\text{wall}(r_{ij}) =
\begin{cases}
\dfrac{k}{n}\big(r^{\min}_{s_i s_j} - r_{ij}\big)^{n},
   & r_{ij} < r^{\min}_{s_i s_j},\\[6pt]
0, & \text{otherwise},
\end{cases}
$$

with $k = 1000$ eV/Å$^n$, $n = 4$, and the per-species-pair floors
$r^{\min}$ measured from the cleaned pre-MACE geometry
(`per_pair_min_from_atoms`).  The wall is exactly zero at and above
each floor, so it never perturbs valid physics; it only blocks descent
into the near-overlap basins.

## Update strategies

Two updates are used, chosen per regime:

**LBFGS minimisation** (all ordered + amorphous regimes).  The ASE
LBFGS optimiser performs quasi-Newton descent, building a
limited-memory approximation of the inverse Hessian from recent
$(\Delta\mathbf r, \Delta\mathbf F)$ pairs (D. C. Liu and J. Nocedal,
Math. Program. **45**, 503 (1989)).  Pipeline settings: `maxstep =
0.2 Å`, 50 steps, with the force threshold set far below reach so the
step cap is the deterministic stop — matching the fixed-sweep
behaviour of the [FIRE relaxation](fire_relaxation.md).

**Langevin molecular dynamics** (liquid regime).  A melt is a
thermal state, not an energy minimum, so the liquid regime runs NVT
Langevin dynamics at the material's melting point instead of a
minimisation:

$$
m_i \ddot{\mathbf r}_i = \mathbf F_i - \gamma m_i \dot{\mathbf r}_i
   + \sqrt{2 m_i \gamma k_B T}\, \boldsymbol\eta_i(t),
$$

with $T = T_\text{melt}$ (Cu 1358 K, Si 1687 K, SiO₂ 1986 K,
SrTiO₃ 2353 K), time step 2 fs, friction $\gamma = 0.02$ (ASE units),
80 steps, and Maxwell–Boltzmann initial velocities.  This is what
makes the liquid structurally distinct from the energy-minimised
amorphous regime built from the same grain-free start.

## Cost

One MACE evaluation is $\mathcal O(N)$ in atom count (fixed
neighbour cutoff).  Measured on the 40³ Å examples (8 CPU threads):
~4 s/step at ~3 k atoms (Si) and ~9–13 s/step at ~5 k atoms (Cu,
SiO₂, SrTiO₃); a GPU is roughly 10–50× faster.  Extrapolated by atom
count, a 200³ Å cell (~600 k atoms) costs on the order of a day per
relaxation on CPU — at those sizes the
[FIRE spring network](fire_relaxation.md#cost-and-convergence)
(minutes) is the working option.

## See also

- [FIRE vs MACE-MP0](fire_vs_mace.md) — term-by-term comparison of
  the two energy models and the spring-weight calibration strategy.
- [FIRE relaxation](fire_relaxation.md) — atomode's built-in
  spring-network relaxer.
- [MACE-MP0 Refinement Examples](../examples_mace/index.md) — the
  worked per-material pipelines, movies, and energy ladders.

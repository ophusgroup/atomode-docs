# DFTB+ Refinement Examples

These examples take a tricor-generated SiO₂ supercell and refine it
with **[DFTB+](https://dftbplus.org/)** — a semi-empirical
tight-binding electronic-structure code that is much faster than full
DFT but recovers most of the structural correction (Si–O bond ±0.02 Å
vs PBE, O–Si–O angle distribution narrows to within a few degrees of
DFT).  See the [DFTB+ home page](https://dftbplus.org/) for method
background, citations, and the full user manual.

The pipeline per regime is:

```
1. Voronoi tile          (tricor: cell.generate(num_steps=0))
2. Orientation refine    (tricor: cell.refine_initial_orientations)
3. FIRE shell-relax      (tricor: cell.shell_relax)
4. DFTB+ relax           (ASE FIRE + UnitCellFilter + ase.calculators.dftb.Dftb)
```

At each stage we capture positions, compute pairwise g(r) +
angular distributions, and record the DFTB+ total energy, so you
can see exactly where each step in the pipeline contributes.

## Install DFTB+

```bash
conda install -c conda-forge dftbplus
```

Drops a `dftb+` executable into `$CONDA_PREFIX/bin/`.  Source build is
at <https://github.com/dftbplus/dftbplus> if you need MPI / custom BLAS.

## Get a Slater-Koster parameter set

For SiO₂ we use **`matsci-0-3`** — covers Si, O, C, H, N.

```bash
git clone --depth 1 https://github.com/dftbparams/matsci.git ~/dftb_sk/matsci-src
mkdir -p ~/dftb_sk/matsci-0-3
cp ~/dftb_sk/matsci-src/skfiles/*.skf ~/dftb_sk/matsci-0-3/
```

(or download the tarball at <https://dftb.org/parameters/download> — same
content, free academic registration.  Licence is CC-BY-SA 4.0 either way.)

## Set the environment variables

ASE finds DFTB+ through two env vars:

```bash
export DFTB_COMMAND="dftb+"
export DFTB_PREFIX="$HOME/dftb_sk/matsci-0-3/"   # trailing slash required
```

Add them to your shell rc so they persist.  ASE concatenates filenames
onto `DFTB_PREFIX`, hence the trailing slash.

## Verify the setup

```bash
python -c "
from ase.build import bulk
from ase.calculators.dftb import Dftb
atoms = bulk('Si', 'diamond', a=5.43)
atoms.calc = Dftb(
    Hamiltonian_='DFTB',
    Hamiltonian_MaxAngularMomentum_Si='p',
    kpts=(2, 2, 2),
)
print('E =', atoms.get_potential_energy(), 'eV')
"
```

Prints around `-101 eV` for the 2-atom bulk Si cell with matsci SK.

## Run the examples

```bash
# All three regimes at the default 30 Å / 2052 atoms (~15 hr total)
python scripts/regen_dftb_examples.py --box 30.0

# Single regime (nano is fastest, ~4 hr; amorphous is slowest, ~5 hr)
python scripts/regen_dftb_examples.py --regime amorphous --box 30.0

# Smaller cell for a quick sanity-check (~55 min for all three, ~609 atoms)
python scripts/regen_dftb_examples.py --box 20.0

# Even smaller smoke test (~5 min total, ~258 atoms)
python scripts/regen_dftb_examples.py --box 15.0

# tricor stages only — DFTB+ skipped (seconds)
python scripts/regen_dftb_examples.py --skip-dftb
```

Output files per regime live in `docs/_static/dftb/`:

| file | content |
|---|---|
| `{regime}_traj.xyz` | 4-frame extxyz with positions + species at each stage |
| `{regime}_energies.json` | total DFTB+ energy at each stage (eV) |
| `{regime}_summary.json` | Si–O peak position, atom count, per-stage timings |
| `{regime}_gr.png` | pair g(r) for Si–O / O–O / Si–Si, line per stage |
| `{regime}_bond_hist.png` | Si–O bond length distribution per stage |
| `{regime}_angle_hist.png` | O–Si–O + Si–O–Si angle distributions per stage |
| `{regime}_dftb_relax.log` | ASE FIRE log for stage 4 |

## Parameter choices

| knob | value |
|---|---|
| cell side | 30 Å (≈ 2050 atoms) |
| regimes | amorphous, SRO, nanocrystalline |
| `grain_size` for nano | 22 Å (close to the standard 35 Å, with ~4 Å of amorphous boundary on each face) |
| `kpts` | (1, 1, 1) Γ-only |
| SK set | matsci-0-3 |
| SCC tolerance | 1e-2 |
| Fermi smearing | 1e-2 Ha (≈ 3000 K) |
| pre-DFTB cleanup | `bond_relax(20)` + `enforce_hard_core(40)` |
| charge restart | seed SP + `Hamiltonian_ReadInitialCharges="Yes"` |
| DFTB+ optimizer | ASE FIRE, `maxstep = 0.03 Å` |
| DFTB+ cell DOFs | volume only (`UnitCellFilter(hydrostatic_strain=True)`) |
| DFTB+ fmax target | 1.0 eV/Å |
| DFTB+ step cap | 60 |

The pre-DFTB cleanup (`bond_relax` + `enforce_hard_core`) gives DFTB+ a
geometry with no sub-hard-core pair overlaps and bonded pairs already
near their peak distances — both important for SCC stability on the
first step.  `hydrostatic_strain=True` restricts the cell relax to
isotropic volume changes (no shear).  The charge restart (one-shot seed
single-point that writes `charges.bin`, then a relax with
`Hamiltonian_ReadInitialCharges = "Yes"`) keeps each FIRE step starting
from converged charges instead of reconverging the SCC from scratch,
which keeps per-step cost at ~2.5 s.

## See also

- {doc}`amorphous` — short-range tetrahedral network
- {doc}`sro` — short-range-ordered SiO₂
- {doc}`nanocrystalline` — crystalline interior + amorphous boundary

```{toctree}
:hidden:

amorphous
sro
nanocrystalline
```

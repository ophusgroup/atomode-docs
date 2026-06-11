"""Per-pair minimum-distance wall calculator for MACE relaxations.

MACE foundation models (mace-mp-0, mace-mpa-0) have spurious low-energy
basins on disordered SiO₂: atoms can be pulled into near-overlap through
shared O, producing a ~50° Si-O-Si hump in the ADF and a too-short Si-Si
peak.  LBFGS descends straight into them, so low ``fmax`` is not enough
to guarantee a physical structure.

``MinDistanceWallCalculator`` wraps a base ASE calculator (typically the
MACE one) and adds a one-sided soft repulsion that activates ONLY when a
pair distance falls below the corresponding per-species-pair floor.
Silent at or above each floor, so it does not perturb in-distribution
physics.

Recreated from the API documented in the collaborator's MACE notebook
(``mace_relaxation_and_evaluation.ipynb``):

    rmin = per_pair_min_from_atoms(atoms, margin=0.0)
    atoms.calc = MinDistanceWallCalculator(
        mace_calc, rmin, k=1000.0, exponent=4,
    )
"""

from __future__ import annotations

import numpy as np
from ase.calculators.calculator import Calculator, all_changes
from ase.neighborlist import neighbor_list


def per_pair_min_from_atoms(atoms, margin: float = 0.0) -> dict:
    """Minimum observed pair distance per species-pair, minus margin.

    Returns a dict keyed by ``(Z_lo, Z_hi)`` (sorted, atomic-number
    integers) mapping to the smallest distance found between that
    species pair in ``atoms``, with ``margin`` subtracted so the wall
    sits slightly below the current minimum.
    """
    cutoff = 8.0
    i, j, d = neighbor_list("ijd", atoms, cutoff, self_interaction=False)
    z = atoms.numbers
    out = {}
    if len(d) == 0:
        return out
    zlo = np.minimum(z[i], z[j])
    zhi = np.maximum(z[i], z[j])
    pairs = np.stack([zlo, zhi], axis=1)
    unique = np.unique(pairs, axis=0)
    for za, zb in unique:
        m = (zlo == za) & (zhi == zb)
        if m.any():
            out[(int(za), int(zb))] = float(d[m].min()) - float(margin)
    return out


class MinDistanceWallCalculator(Calculator):
    """Base calculator + one-sided soft wall below per-pair r_min.

    Wall energy per active pair (only when ``r_ij < r_min[s_i, s_j]``)::

        U_pair = (k / n) * (r_min - r_ij)^n

    Force on atom ``i`` (push i away from j)::

        F_i = -k * (r_min - r_ij)^(n-1) * (r_j - r_i) / r_ij

    Parameters
    ----------
    base_calc
        Underlying ASE calculator (typically a MACE one).
    r_min_per_pair
        Mapping ``{(Z_a, Z_b): r_min_AA}``.  Keys may be in any order;
        they are normalised to ``(min(Z_a, Z_b), max(Z_a, Z_b))``.
    k
        Wall spring constant (eV / Å^n).  Default ``1000``.
    exponent
        Polynomial exponent ``n``.  Default ``4`` — stiff but
        differentiable, matches the notebook's parameter choice.
    """

    implemented_properties = ["energy", "free_energy", "forces", "stress"]

    def __init__(
        self,
        base_calc,
        r_min_per_pair: dict,
        k: float = 1000.0,
        exponent: int = 4,
    ):
        super().__init__()
        self.base_calc = base_calc
        self.r_min_per_pair = {
            (min(a, b), max(a, b)): float(r)
            for (a, b), r in r_min_per_pair.items()
        }
        self.k = float(k)
        self.exponent = int(exponent)
        self._max_rmin = (
            max(self.r_min_per_pair.values()) if self.r_min_per_pair else 0.0
        )

    def calculate(self, atoms=None, properties=("energy",), system_changes=all_changes):
        super().calculate(atoms, properties, system_changes)

        self.base_calc.calculate(atoms, properties, system_changes)
        E = float(self.base_calc.results["energy"])
        F = np.asarray(self.base_calc.results["forces"], dtype=np.float64).copy()
        stress = np.asarray(
            self.base_calc.results.get("stress", np.zeros(6)), dtype=np.float64,
        ).copy()

        if self._max_rmin > 0.0:
            # ``ijdD`` returns each pair in both orderings, so D[k] is the
            # min-image vector r_j - r_i and the same pair appears once
            # with each (i, j) → energy must be halved, but per-atom force
            # accumulation already gives the correct one-sided contribution.
            i, j, d, D = neighbor_list(
                "ijdD", atoms, self._max_rmin, self_interaction=False,
            )
            if len(d):
                z = atoms.numbers
                zlo = np.minimum(z[i], z[j])
                zhi = np.maximum(z[i], z[j])

                rmin_pair = np.zeros(len(d), dtype=np.float64)
                for (za, zb), rmin in self.r_min_per_pair.items():
                    m = (zlo == za) & (zhi == zb)
                    rmin_pair[m] = rmin

                active = (rmin_pair > 0.0) & (d < rmin_pair)
                if active.any():
                    gap = rmin_pair[active] - d[active]
                    # Energy: each pair contributes once → half the row sum.
                    E_wall = 0.5 * np.sum(
                        (self.k / self.exponent) * gap ** self.exponent
                    )
                    E += float(E_wall)

                    # Force on atom i: -k * gap^(n-1) * (D / d)
                    # (D points from i toward j; the wall pushes i away → -D)
                    fmag = self.k * gap ** (self.exponent - 1)
                    unit = D[active] / d[active, None]
                    f_contrib = -fmag[:, None] * unit
                    np.add.at(F, i[active], f_contrib)

        self.results["energy"] = E
        self.results["free_energy"] = E
        self.results["forces"] = F
        self.results["stress"] = stress

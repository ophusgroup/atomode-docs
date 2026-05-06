"""Regenerate STATIC examples (no orientation refinement) at
40 × 40 × 40 Å so they match the refined examples' cell size.

For each (material, regime) pair this writes:

  * trajectory HTML  — the FIRE-quench movie with material-
                        appropriate polyhedra (Cu cuboctahedra,
                        Si / sp³-C / SiO₂ tetrahedra, sp²-C
                        triangles, mixed sp²/sp³ groups, SrTiO₃
                        octahedra).  Bonds are off everywhere.
  * g3 HTML         — measured at the FIRE-final positions.

The per-regime parameters are pulled from the original 20³ markdown
pages (the ``cell.generate(...)`` snippet).  Cell construction is
forced to 40³ here regardless of what the snippet says.
"""
from __future__ import annotations
import sys, time
from pathlib import Path
sys.stdout.reconfigure(line_buffering=True)

# Path resolution: this script lives in tricor-docs/scripts/.
# tricor-docs/ is the parent.  ``tricor`` (the library) is expected to
# be a sibling repo (../tricor/src), or already importable from the
# active environment.  Try the env first; fall back to the sibling.
_REPO_ROOT = Path(__file__).resolve().parents[1]   # tricor-docs/
DOCS_DIR = _REPO_ROOT / "docs"
STATIC_DIR = DOCS_DIR / "_static"
STRUCTURES_DIR = DOCS_DIR / "structures"
try:
    import tricor  # noqa: F401
except ImportError:
    sys.path.insert(0, str(_REPO_ROOT.parent / "tricor" / "src"))

import numpy as np
from ase.build import bulk
from ase.io import read
import tricor as tc
from tricor.shells import CoordinationShellTarget
import tricor._plotting as _tp


# ── Polyhedron subsampler — same caps as the refined regen so
#    the static-vs-refined comparison stays visually consistent.
SEED = 42
POLY_CAPS = {
    "_detect_cuboctahedra": 1500,
    # Tetrahedra cap bumped from 900 → 2500 (2026-05): Si LRO / NC
    # naturally generate ~1500-2000 clean tetrahedra at 40³ once
    # the detector tolerances are tight enough to discriminate
    # actual crystalline atoms from liquid clusters; capping at 900
    # squashed the upper end of the order ladder.
    # Triangle cap bumped 900 → 3500 (2026-05): graphite at the
    # carbon detector tolerance 0.10/15° gives ~3500 well-formed
    # sp² triangles for a 40³ cell (5974 C atoms); the prior 900
    # cap rendered <30 % of the actual graphitic order.
    # Tetrahedra cap bumped to 5000 so pure diamond at the same
    # 0.10/15° tol (~4300 detected) renders fully.
    "_detect_tetrahedra":   5000,
    "_detect_octahedra":     280,
    "_detect_triangles":    3500,
}


def _subsample(polys, cap, seed_offset):
    if len(polys) <= cap:
        return polys
    rng = np.random.default_rng(SEED + seed_offset + len(polys))
    idx = sorted(rng.choice(len(polys), cap, replace=False))
    return [polys[i] for i in idx]


for _name, _cap in POLY_CAPS.items():
    _orig = getattr(_tp, _name)
    def _make(orig, cap, hash_seed):
        def _wrapped(*args, **kwargs):
            return _subsample(orig(*args, **kwargs), cap, hash_seed)
        return _wrapped
    setattr(_tp, _name, _make(_orig, _cap, hash(_name) & 0xFFFF))


OUT = STATIC_DIR
TRAJ_DIR = OUT / "trajectories"
G3_DIR = OUT / "g3"
SIDE = 40.0


# ── Per-regime catalogue — params copied verbatim from the 20³
#    markdown pages.  Cell sizing is overridden to 40³ here.
DISORDER_REGIMES = {
    # (material, page_filename) → (asset_stem, gen_kwargs_dict)
    # Cu disorder ladder — re-tuned 2026-05.  Liquid stays the most
    # disordered (no grains, very weak springs); amorphous bumps the
    # bond weight up so a coordination shell forms visibly; SRO now
    # has 5 Å seed grains that produce small ordered patches; MRO /
    # LRO grow the grain size and strengthen the springs so the
    # crystallinity is monotonically more visible at each step;
    # NC stays at 18 Å with strong springs.
    # Cu g(r) smoothing pass 3 (2026-05): the user wanted physically
    # realistic distributions, not visualization smoothing.  The
    # previous pass left a broad shoulder of bonded atoms at
    # ~2.30–2.40 Å (RMS bond mismatch ~0.27 Å) because the bond
    # springs were too weak to populate the natural 1NN peak.  This
    # pass:
    #   1. **Strong bond springs**: bw 2–6× higher across the
    #      ladder so bonded pairs are tightly held at 2.56 Å.
    #   2. **Larger nonbond_push_scale**: push non-bonded pairs
    #      well past the 1NN peak (≥ 1.4 × 1NN = 3.6 Å) — exactly
    #      where the FCC 2NN sits — so the gap between 1NN and 2NN
    #      shells is clean.
    #   3. **More num_steps**: heavier bond springs need more FIRE
    #      iterations to fully equilibrate without bond oscillations.
    #
    # The result: a sharp 1NN peak at 2.56 Å, an empty gap 2.65–3.5 Å,
    # then 2NN density past 3.6 Å — i.e. the real FCC/liquid Cu g(r).
    ("copper", "liquid"):              ("cu_liquid",           dict(num_steps=200, grain_size=None,  bond_weight=2.5,  angle_weight=0.0, repulsion_weight=1.5, hard_core_scale=0.95, nonbond_push_scale=1.00, displacement_sigma=0.05)),
    ("copper", "amorphous"):           ("cu_amorphous",        dict(num_steps=200, grain_size=None,  bond_weight=3.0,  angle_weight=0.0, repulsion_weight=1.5, hard_core_scale=0.95, nonbond_push_scale=1.00, displacement_sigma=0.03)),
    ("copper", "short_range_order"):   ("cu_sro",              dict(num_steps=200, grain_size=7.0,   bond_weight=3.5,  angle_weight=0.0, repulsion_weight=1.6, hard_core_scale=0.96, nonbond_push_scale=1.00, displacement_sigma=0.03)),
    ("copper", "medium_range_order"):  ("cu_mro",              dict(num_steps=220, grain_size=9.0,   bond_weight=4.0,  angle_weight=0.0, repulsion_weight=1.7, hard_core_scale=0.97, nonbond_push_scale=1.00, displacement_sigma=0.025)),
    ("copper", "long_range_order"):    ("cu_lro",              dict(num_steps=240, grain_size=12.5,  bond_weight=4.5,  angle_weight=0.0, repulsion_weight=1.9, hard_core_scale=0.99, nonbond_push_scale=1.00, displacement_sigma=0.02)),
    ("copper", "nanocrystalline"):     ("cu_nanocrystalline",  dict(num_steps=280, grain_size=18.0,  bond_weight=5.0,  angle_weight=0.0, repulsion_weight=2.0, hard_core_scale=1.00, nonbond_push_scale=1.00, displacement_sigma=0.01)),

    # Si tweaked pass 4 (2026-05): explicit order ladder targeting
    # ~100 / 200 / 400 / 800 / 1900 / 1000 polyhedra (detector
    # tols 0.10/18° set in get_polyhedra_kwargs).  Liquid and NC
    # keep the library presets; the in-between regimes are tuned
    # to show clear monotonic progression.
    ("silicon", "liquid"):             ("si_liquid",           "preset:liquid"),
    # Pass 5 (2026-05): SRO bumped above amorphous (was matching),
    # MRO + LRO bumped further toward the target ladder.  Cleaner
    # progression: 110 / 200 / 400 / 800 / 1500 / 1300.
    ("silicon", "amorphous"):          ("si_amorphous",        dict(num_steps=120, grain_size=None, bond_weight=0.6,  angle_weight=0.20, repulsion_weight=1.3, hard_core_scale=0.86, nonbond_push_scale=0.45, displacement_sigma=0.12)),
    ("silicon", "short_range_order"):  ("si_sro",              dict(num_steps=180, grain_size=8.0,  bond_weight=1.5,  angle_weight=0.5,  repulsion_weight=1.8, hard_core_scale=0.91, nonbond_push_scale=0.60, displacement_sigma=0.06)),
    ("silicon", "medium_range_order"): ("si_mro",              dict(num_steps=200, grain_size=12.0, bond_weight=2.0,  angle_weight=0.8,  repulsion_weight=2.2, hard_core_scale=0.93, nonbond_push_scale=0.75, displacement_sigma=0.04)),
    ("silicon", "long_range_order"):   ("si_lro",              dict(num_steps=200, grain_size=15.0, bond_weight=2.4,  angle_weight=1.0,  repulsion_weight=2.3, hard_core_scale=0.93, nonbond_push_scale=0.85, displacement_sigma=0.035)),
    ("silicon", "nanocrystalline"):    ("si_nanocrystalline",  "preset:nanocrystalline"),

    # SiO₂ disorder ladder — re-tuned 2026-05.  Every grain-bearing
    # regime gets a +6 Å bump in grain_size and num_steps grows from
    # 50 → 80 so the FIRE quench has more iterations to settle into
    # the bigger grains.  Liquid stays grain-free as the high-T
    # endpoint.
    # SiO2 ladder bumped 2026-05: SRO/MRO/LRO/NC each given a
    # larger grain than the prior pass to push the SiO4 tetrahedra
    # count clearly above MRO at the 0.10/18° detector.  Bond/angle
    # weights stay at the FIRE sweet spot (1.65 / 1.35) — bigger
    # weights hit a plateau at every grain size.  Grain sweep
    # benchmark (rng_seed=42, 40 Å cell): grain → tet fraction
    #   12 → 41%   14 → 47%   16 → 52%   20 → 55%
    #   22 → 61%   26 → 63%   30 → 64%   35 → 70%   38 → 70%
    # Picked grain = 15 / 20 / 26 / 35 to give a clean ~6-7
    # percentage-point step between regimes.
    ("silicon_dioxide", "liquid"):              ("sio2_liquid",          dict(num_steps=120, grain_size=None, bond_weight=0.5, angle_weight=0.0, repulsion_weight=1.5, hard_core_scale=1.05, nonbond_push_scale=0.6, displacement_sigma=0.01)),
    # Bump pass 4 (2026-05): num_steps tripled — multi-element FIRE
    # quenches need ~250 iterations to converge against the angle
    # springs; the previous 100 steps left atoms still oscillating.
    # Repulsion held at 1.25-1.3 (not bumped) so they don't bounce.
    ("silicon_dioxide", "amorphous"):           ("sio2_amorphous",       dict(num_steps=250, grain_size=12.0, bond_weight=1.55, angle_weight=1.25, repulsion_weight=1.25, hard_core_scale=0.81, nonbond_push_scale=0.7,  displacement_sigma=0.012)),
    ("silicon_dioxide", "short_range_order"):   ("sio2_sro",             dict(num_steps=250, grain_size=15.0, bond_weight=1.65, angle_weight=1.35, repulsion_weight=1.3,  hard_core_scale=0.82, nonbond_push_scale=0.72, displacement_sigma=0.010)),
    ("silicon_dioxide", "medium_range_order"):  ("sio2_mro",             dict(num_steps=300, grain_size=20.0, bond_weight=1.65, angle_weight=1.35, repulsion_weight=1.3,  hard_core_scale=0.82, nonbond_push_scale=0.72, displacement_sigma=0.008)),
    ("silicon_dioxide", "long_range_order"):    ("sio2_lro",             dict(num_steps=350, grain_size=26.0, bond_weight=1.65, angle_weight=1.35, repulsion_weight=1.3,  hard_core_scale=0.82, nonbond_push_scale=0.72, displacement_sigma=0.006)),
    ("silicon_dioxide", "nanocrystalline"):     ("sio2_nanocrystalline", dict(num_steps=400, grain_size=35.0, bond_weight=1.65, angle_weight=1.35, repulsion_weight=1.3,  hard_core_scale=0.82, nonbond_push_scale=0.72, displacement_sigma=0.003)),

    # SrTiO₃ overhaul pass 5 (2026-05):
    #   - apply ``with_angle_triplets([Ti-O-O 90°, O-Ti-Ti 180°])``
    #     in build_disorder so the multi-modal Sr-centred angles
    #     (cuboctahedral 60/90/120/180° distribution) don't fight a
    #     single-target spring.  This is what the docs example
    #     already prescribed; the regen script was the outlier.
    #   - keep hard_core_scale = 1.10 (sweep showed dropping it to
    #     1.0 cuts the octahedra count 5–10 ×; the 1.10 wall is
    #     what enforces the cuboctahedral O-O / Ti-Ti / Sr-Sr
    #     minimum distances that let the corner-sharing TiO6
    #     network re-form during FIRE).
    #   - keep weights at the FIRE sweet spot ``b=1.0, a=0.7``;
    #     bumping a → 1.2 cuts the count by ~⅓ (sweep data).
    #   - grow the grain (10 → 14 → 22 → 30 → 35 Å) and the
    #     relaxation budget (300 → 350 → 400 → 450 → 500 steps),
    #     tighten ``displacement_sigma`` (0.006 → 0.001).
    # Benchmark TiO6 octahedra count (rng_seed=42, 40 Å cell,
    # 0.18/18° detector, 1026 Ti atoms): old NC → ~26% (266); new
    # ladder walks 0% → 10% → 26% → 36% → 48%.
    ("strontium_titanate", "liquid"):              ("srtio3_liquid",          dict(num_steps=200, grain_size=None, bond_weight=0.10, angle_weight=0.0, repulsion_weight=1.0, hard_core_scale=1.10, nonbond_push_scale=0.6,  displacement_sigma=0.02)),
    ("strontium_titanate", "amorphous"):           ("srtio3_amorphous",       dict(num_steps=300, grain_size=None, bond_weight=0.50, angle_weight=0.4, repulsion_weight=1.1, hard_core_scale=1.10, nonbond_push_scale=0.65, displacement_sigma=0.008)),
    ("strontium_titanate", "short_range_order"):   ("srtio3_sro",             dict(num_steps=350, grain_size=14.0, bond_weight=1.0,  angle_weight=0.7, repulsion_weight=1.2,  hard_core_scale=1.10, nonbond_push_scale=0.75, displacement_sigma=0.005)),
    ("strontium_titanate", "medium_range_order"):  ("srtio3_mro",             dict(num_steps=400, grain_size=22.0, bond_weight=1.0,  angle_weight=0.7, repulsion_weight=1.2,  hard_core_scale=1.10, nonbond_push_scale=0.75, displacement_sigma=0.002)),
    ("strontium_titanate", "long_range_order"):    ("srtio3_lro",             dict(num_steps=450, grain_size=28.0, bond_weight=1.0,  angle_weight=0.7, repulsion_weight=1.2,  hard_core_scale=1.10, nonbond_push_scale=0.75, displacement_sigma=0.0015)),
    ("strontium_titanate", "nanocrystalline"):     ("srtio3_nanocrystalline", dict(num_steps=500, grain_size=35.0, bond_weight=1.0,  angle_weight=0.7, repulsion_weight=1.2,  hard_core_scale=1.10, nonbond_push_scale=0.75, displacement_sigma=0.001)),
}

CARBON_REGIMES = {
    # name → (asset_stem, w_graphite, w_diamond)
    "graphite":    ("carbon_graphite_nc",  1.00, 0.00),
    "sp2_rich":    ("carbon_sp2_rich",     0.80, 0.20),
    "sp2_leaning": ("carbon_sp2_leaning",  0.60, 0.40),
    "sp3_leaning": ("carbon_sp3_leaning",  0.40, 0.60),
    "sp3_rich":    ("carbon_sp3_rich",     0.20, 0.80),
    "diamond":     ("carbon_diamond_nc",   0.00, 1.00),
}


# ── Material-specific cell + shell target builders.
def _atoms(material: str):
    if material == "copper":
        return bulk("Cu", "fcc", a=3.615)
    if material == "silicon":
        return bulk("Si", "diamond", a=5.431)
    cif_map = {
        "silicon_dioxide":    "SiO2.cif",
        "strontium_titanate": "SrTiO3.cif",
    }
    return read(
        str(STRUCTURES_DIR / cif_map[material])
    )


def build_disorder(material: str, regime: str):
    atoms_ref = _atoms(material)
    shell = CoordinationShellTarget.from_atoms(atoms_ref, phi_num_bins=90)
    # SrTiO3: whitelist the only two single-mode angle triplets.
    # Sr sits at the centre of an SrO12 cuboctahedron whose
    # O-Sr-O distribution is multi-modal (60° / 90° / 120° /
    # 180°), so any single-target angle spring through Sr fights
    # the natural geometry and prevents FIRE convergence.  Keep
    # Ti-O-O at 90° (TiO6 octahedron) and O-Ti-Ti at 180° (linear
    # backbone) — both genuinely single-peaked.  The auto-filter in
    # ``from_atoms`` already disabled the lattice-artefact bond pairs
    # (Sr-Sr, Ti-Ti, O-O, Sr-Ti); this whitelist further removes
    # angle springs that would conflict with cuboctahedral order.
    if material == "strontium_titanate":
        shell = shell.with_angle_triplets([
            ("Ti", "O", "O"),
            ("O", "Ti", "Ti"),
        ])
    cell = tc.Supercell.from_atoms(
        atoms_ref, cell_dim_angstroms=(SIDE, SIDE, SIDE),
        r_max=10, r_step=0.1, phi_num_bins=90, rng_seed=SEED,
    )
    spec = DISORDER_REGIMES[(material, regime)][1]
    if isinstance(spec, str) and spec.startswith("preset:"):
        preset_name = spec.split(":", 1)[1]
        gen_kwargs = tc.Supercell.PRESETS[preset_name].copy()
    else:
        gen_kwargs = dict(spec)
    # Cu uses ``angle_weight = 0`` because its first-shell angle
    # distribution is multi-modal (60° / 90° / 120° / 180°
    # cuboctahedral).  Without angle springs, the bond springs
    # alone can't maintain crystalline order during FIRE — interior
    # atoms drift slightly and the cuboctahedra detector misses
    # them.  Pre-2026 the global default ``freeze_grain_interiors=
    # True`` masked this; the new default (False, multi-species
    # fix) exposed it.  Re-enable interior freezing for Cu only,
    # since Cu has no cross-species spring strain that the freeze
    # would prevent from settling.
    if material == "copper" and gen_kwargs.get("grain_size") is not None:
        gen_kwargs["freeze_grain_interiors"] = True
    return cell, shell, gen_kwargs


def build_carbon(regime: str):
    ag = read(str(STRUCTURES_DIR / "C_graphite.cif"))
    ad = read(str(STRUCTURES_DIR / "C_diamond.cif"))
    shell_sp2 = CoordinationShellTarget.from_atoms(ag, phi_num_bins=90)
    shell_sp3 = CoordinationShellTarget.from_atoms(ad, phi_num_bins=90)
    shell = CoordinationShellTarget.from_targets(
        {"sp2": shell_sp2, "sp3": shell_sp3}
    )
    _, w_g, w_d = CARBON_REGIMES[regime]
    cell = tc.Supercell.from_atoms(
        ag, cell_dim_angstroms=(SIDE, SIDE, SIDE),
        r_max=10, r_step=0.1, phi_num_bins=90, rng_seed=SEED,
    )
    # Bump pass 4 (2026-05): grow grain 14 → 18 Å + bump num_steps
    # 150 → 250 across all carbon regimes.  Sweep showed grain=18
    # gives ~15 % more polyhedra (843 / 775 vs 687 / 740 for the
    # mixed sp²/sp³ panels) and grain ≥ 16 risks "two-grain dip"
    # only with shorter relaxation; 250 steps fully converges.
    gen_kwargs = dict(
        grain_size=18.0,
        grain_sources=[
            {"atoms": ag, "species_offset": 0, "weight": w_g},
            {"atoms": ad, "species_offset": 1, "weight": w_d},
        ],
        num_steps=250,
        bond_weight=2.5, angle_weight=1.2, repulsion_weight=2.0,
        hard_core_scale=0.92, nonbond_push_scale=0.85,
        displacement_sigma=0.02,
    )
    return cell, shell, gen_kwargs


def get_polyhedra_kwargs(material: str, regime: str) -> dict:
    """Material-appropriate polyhedron config for the trajectory
    viewer.  Same colours / opacities used by the refined examples
    so the static-vs-refined comparison stays visually consistent."""
    if material == "copper":
        return dict(
            cuboctahedra=dict(center_symbol="Cu", vertex_symbol="Cu"),
            cuboctahedra_color=(0.85, 0.45, 0.20),
            cuboctahedra_opacity=0.22,
        )
    if material == "carbon":
        # Detector loosened 2026-05 from 0.06/5° to 0.10/15° to
        # match Si/SiO2 (which use 0.10/18°): the strict 5° angle
        # window rejected most boundary atoms of pure diamond /
        # graphite (only 16% / 32% of C passed), while FIRE
        # actually achieves ~10° avg angle deviation per the bond /
        # angle losses.  At 0.10/15° pure diamond shows ~40 % and
        # pure graphite ~60 % of C atoms as well-formed polyhedra,
        # which the user expects from a "nanocrystalline graphite"
        # / "nanocrystalline diamond" panel.
        if regime == "graphite":
            return dict(polyhedra_groups=[dict(
                kind="triangles",
                center_symbol="C", vertex_symbol="C",
                bond_length=1.42, bond_length_tol=0.10,
                angle_tol_deg=15.0,
                color=(0.20, 0.65, 0.30), opacity=0.55,
            )])
        if regime == "diamond":
            return dict(
                tetrahedra=dict(
                    center_symbol="C", vertex_symbol="C",
                    bond_length=1.54, bond_length_tol=0.06,
                    angle_tol_deg=5.0,
                ),
                tetrahedra_color=(0.25, 0.35, 0.85),
                tetrahedra_opacity=0.45,
            )
        # mixed (sp2_rich, sp2_leaning, sp3_leaning, sp3_rich)
        return dict(polyhedra_groups=[
            dict(
                kind="triangles",
                center_symbol="C", vertex_symbol="C",
                bond_length=1.42, bond_length_tol=0.10,
                angle_tol_deg=15.0,
                color=(0.20, 0.65, 0.30), opacity=0.55,
            ),
            dict(
                kind="tetrahedra",
                center_symbol="C", vertex_symbol="C",
                bond_length=1.54, bond_length_tol=0.10,
                angle_tol_deg=15.0,
                color=(0.25, 0.35, 0.85), opacity=0.45,
            ),
        ])
    if material == "silicon":
        # Detector tightened from default 0.15/25° to 0.10/18°
        # (window 2.12-2.59 Å, 91.5-127.5°): cleanly separates
        # liquid from crystalline — defaults accepted ~20% of
        # liquid Si atoms as "tetrahedra" because the windows
        # were wide enough that any 4-NN close-pack happened to
        # pass.  At 0.10/18° the liquid drops to a few percent
        # while NC stays > 50%.
        return dict(
            tetrahedra=dict(
                center_symbol="Si", vertex_symbol="Si",
                bond_length_tol=0.10,
                angle_tol_deg=18.0,
            ),
            tetrahedra_color=(0.35, 0.45, 0.95),
            tetrahedra_opacity=0.45,
        )
    if material == "silicon_dioxide":
        # Tightened tolerances (same rationale as Si): defaults
        # 0.15/25° accept too many distorted SiO4 motifs in the
        # liquid / amorphous panels.  0.10/18° (window 1.45-1.77 Å,
        # 91.5-127.5°) cleanly isolates well-formed corner-sharing
        # SiO4 tetrahedra from boundary / disordered Si atoms.
        return dict(
            tetrahedra=dict(
                center_symbol="Si", vertex_symbol="O",
                bond_length_tol=0.10,
                angle_tol_deg=18.0,
            ),
            tetrahedra_color=(0.28, 0.62, 0.95),
            tetrahedra_opacity=0.42,
        )
    if material == "strontium_titanate":
        return dict(
            octahedra=dict(center_symbol="Ti", vertex_symbol="O"),
            octahedra_color=(0.95, 0.55, 0.25),
            octahedra_opacity=0.42,
        )
    return {}


def regen_one(material: str, regime: str, asset_stem: str):
    print(f"  {material}/{regime} → {asset_stem}", flush=True)
    if material == "carbon":
        cell, shell, gen_kwargs = build_carbon(regime)
    else:
        cell, shell, gen_kwargs = build_disorder(material, regime)
    t0 = time.time()
    cell.generate(
        shell, capture_trajectory=True, show_progress=False, **gen_kwargs,
    )
    elapsed = time.time() - t0

    fire_hist = cell.shell_relax_history
    fire_traj = np.asarray(
        fire_hist.get("trajectory", []), dtype=np.float32,
    )
    n_atoms = len(cell.atoms)
    print(f"    {n_atoms} atoms, {len(fire_traj)} frames, {elapsed:.1f} s",
          flush=True)
    if len(fire_traj) == 0:
        print(f"    WARN: no trajectory; skipping HTML", flush=True)
        return

    # Cap frames at 32 — same downsample as the refined regen so
    # the HTML stays under ~12 MB (single shell_relax with
    # num_steps=200 on a 5000-atom cell produces 201 raw frames =
    # ~85 MB unembedded HTML).
    if len(fire_traj) > 32:
        idx = np.linspace(0, len(fire_traj) - 1, 32, dtype=int)
        fire_hist["trajectory"] = fire_traj[idx]
        for fld in ("atom_cost", "step", "loss", "best_loss",
                     "bond_loss", "angle_loss", "repulsion_loss",
                     "restraint_loss"):
            arr = fire_hist.get(fld)
            if arr is not None and len(arr) == len(fire_traj):
                fire_hist[fld] = np.asarray(arr)[idx]

    # Force cell.atoms.positions to fire_traj[-1] — shell_relax
    # restores to "best loss" frame which is often pre-FIRE for
    # clean cells; without this fix the polyhedra detector locks
    # in indices from a different geometry than what the viewer
    # shows.  See regen_refined_full.py for the long version.
    cell.atoms.positions = np.asarray(fire_traj[-1], dtype=np.float64)

    poly_kwargs = get_polyhedra_kwargs(material, regime)
    traj_path = TRAJ_DIR / f"{asset_stem}.html"
    cell.export_trajectory_html(
        str(traj_path),
        title=f"{material} — {regime}",
        **poly_kwargs,
    )
    poly_kind = list(poly_kwargs)[0] if poly_kwargs else "atoms-only"
    print(f"    traj HTML: {traj_path.stat().st_size / 1024:.0f} KB "
          f"(kind={poly_kind})", flush=True)

    cell.measure_g3(show_progress=False)
    g3_path = G3_DIR / f"{asset_stem}.html"
    cell.export_g3_html(str(g3_path))
    print(f"    g3 HTML: {g3_path.stat().st_size / 1024:.0f} KB",
          flush=True)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--material", default=None)
    parser.add_argument("--regime", default=None)
    args = parser.parse_args()

    print("=" * 60, flush=True)
    print("Disorder-axis materials (40 × 40 × 40 Å)", flush=True)
    print("=" * 60, flush=True)
    for (mat, reg), (stem, _) in DISORDER_REGIMES.items():
        if args.material and mat != args.material:
            continue
        if args.regime and reg != args.regime:
            continue
        try:
            regen_one(mat, reg, stem)
        except Exception as e:
            print(f"  !! FAILED {mat}/{reg}: {e!r}", flush=True)
            import traceback; traceback.print_exc()

    if args.material in (None, "carbon"):
        print("\n" + "=" * 60, flush=True)
        print("Carbon sp²/sp³ axis (40 × 40 × 40 Å)", flush=True)
        print("=" * 60, flush=True)
        for reg, (stem, _, _) in CARBON_REGIMES.items():
            if args.regime and reg != args.regime:
                continue
            try:
                regen_one("carbon", reg, stem)
            except Exception as e:
                print(f"  !! FAILED carbon/{reg}: {e!r}", flush=True)
                import traceback; traceback.print_exc()


if __name__ == "__main__":
    main()

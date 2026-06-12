"""Regenerate the Fast FIRE Refinement example artefacts for the
``docs/examples_refined/`` pages — all materials, all regimes.

Pipeline per (material, regime) at 40³ Å:

  1. Voronoi tile        (cell.generate(num_steps=0))
  2. Orientation refine  (grain regimes; capture_trajectory → movie)
  3. FIRE relaxation     (cell.shell_relax, 300 steps), or for the
     liquid regime a short quench + thermostatted Metropolis sampling
     (cell.thermal_relax) auto-tuned to the MACE liquid's bond width

Shell targets are MACE-calibrated when ``mace-torch`` is available
(:meth:`CoordinationShellTarget.calibrate_to_mace`) — optional, falls
back to the hand-tuned registry weights with a printed note.  The
calibration contributes the per-pair stiffnesses, the Morse
anharmonicity, and the MACE hard-core wall; the effective bond and
angle force scales stay at the registry values (validated on Si NC —
transplanting the literal MACE angle/bond stiffness ratio
over-constrains angles under a quench).

Final structures are scored with a MACE single point when available,
so the per-material energy ladder is directly comparable to the
MACE-MP0 refinement section.

Artefacts land in ``docs/_static/fire/<material>/``.

Usage:
  python scripts/regen_fire_examples.py                      # everything
  python scripts/regen_fire_examples.py --material silicon
  python scripts/regen_fire_examples.py --material silicon --regime nanocrystalline
  python scripts/regen_fire_examples.py --no-calibrate       # registry weights
  python scripts/regen_fire_examples.py --no-movies
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

# Sibling-module reuse: material registry, measurement + plot helpers.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import regen_mace_examples as _RM   # noqa: E402
from regen_mace_examples import (   # noqa: E402
    MATERIALS, REGIME_TITLES, _DISORDER, OUT_ROOT as _MACE_OUT,
    _setup_paths, _subsample, _measure_bond, _measure_angles,
    _plot_bond_hist, _plot_angle_hist, _plot_gr_stack,
    _export_movie_html, _viz_for, _OverviewCell,
)

# The shared plot helpers label stages by position; relabel the final
# stage for the FIRE pipeline.
_RM.STAGE_LABELS = ["Voronoi", "after orient", "after cleanup", "after FIRE"]

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_ROOT = REPO_ROOT / "docs" / "_static" / "fire"

FIRE_STEPS = 300
ORIENT_KW = dict(amplitudes_deg=(30.0, 12.0, 5.0),
                 trials_per_amplitude_per_grain=12,
                 max_rounds_per_amplitude=1,
                 time_budget_sec=400.0)

# Liquid thermostat: Metropolis sampling on the spring network after a
# short quench; T auto-tuned so the bond-length spread matches the
# MACE-MD liquid reference when available.
LIQUID_QUENCH_STEPS = 60
LIQUID_TUNE_SWEEPS = 150
LIQUID_FINAL_SWEEPS = 400
LIQUID_T0 = 0.04

_SHELL_CACHE: dict = {}
_MACE_CALC = None


def _load_mace_calc_or_none():
    global _MACE_CALC
    if _MACE_CALC is not None:
        return _MACE_CALC
    try:
        from mace.calculators import mace_mp
        _MACE_CALC = mace_mp(model="medium-mpa-0", device="cpu",
                             default_dtype="float32")
    except Exception as exc:  # noqa: BLE001
        print(f"  (MACE unavailable — {exc.__class__.__name__}; "
              f"skipping calibration + energy scoring)", flush=True)
        _MACE_CALC = None
    return _MACE_CALC


def _build_shell(material, mat, calibrate=True):
    """Shell target for the material; MACE-calibrated when possible."""
    key = (material, calibrate)
    if key in _SHELL_CACHE:
        return _SHELL_CACHE[key]
    import tricor as tc
    from tricor.shells import CoordinationShellTarget

    if mat["axis"] == "sp":
        ag = mat["sp_sources"]["graphite"]()
        ad = mat["sp_sources"]["diamond"]()
        sg = CoordinationShellTarget.from_atoms(ag, phi_num_bins=36)
        sd = CoordinationShellTarget.from_atoms(ad, phi_num_bins=36)
        # Composite calibration is not supported; carbon runs on the
        # registry weights (see docs note).
        shell = CoordinationShellTarget.from_targets({"sp2": sg, "sp3": sd})
        calibrated = False
    else:
        ref = mat["builder"]()
        shell = CoordinationShellTarget.from_atoms(ref, phi_num_bins=36)
        if mat.get("angle_triplets"):
            shell = shell.with_angle_triplets(mat["angle_triplets"])
        calibrated = False
        if calibrate:
            try:
                shell = shell.calibrate_to_mace(show_progress=False)
                calibrated = True
            except Exception as exc:  # noqa: BLE001
                print(f"  calibration unavailable for {material}: "
                      f"{exc.__class__.__name__}: {exc}", flush=True)
    _SHELL_CACHE[key] = (shell, calibrated)
    return shell, calibrated


def _weights(kw, shell, calibrated):
    """FIRE weights for a calibrated shell.

    Validated on Si NC vs the MACE reference: the winning
    configuration keeps the registry's *effective* force scale for
    both terms (the literal MACE angle/bond stiffness ratio
    over-constrains angles under a quench) while the calibration
    contributes the per-pair stiffnesses, the Morse anharmonicity,
    and the MACE hard-core wall.  ``angle_weight`` divides out the
    calibrated ratio so ``angle_weight x tri_k`` lands back on the
    registry value.
    """
    if calibrated:
        info = getattr(shell, "mace_calibration", None) or {}
        ratio = info.get("angle_over_bond")
        ang = kw["angle_weight"]
        if ratio and np.isfinite(ratio) and ratio > 0:
            ang = kw["angle_weight"] / float(ratio)
        return dict(bond_weight=kw["bond_weight"], angle_weight=ang,
                    repulsion_weight=kw["repulsion_weight"],
                    hard_core_scale=1.0,
                    nonbond_push_scale=kw["nonbond_push_scale"])
    return dict(bond_weight=kw["bond_weight"], angle_weight=kw["angle_weight"],
                repulsion_weight=kw["repulsion_weight"],
                hard_core_scale=kw["hard_core_scale"],
                nonbond_push_scale=kw["nonbond_push_scale"])


def _mace_liquid_sigma(material, mat):
    """Bond-width target from the MACE liquid artefact, if present."""
    traj = _MACE_OUT / material / "liquid_traj.xyz"
    if not traj.exists():
        return None
    from ase.io import read
    a = read(str(traj), index=-1)
    za, zb, r_lo, r_hi = mat["bond"]
    _, _, sigma, _ = _measure_bond(a, za, zb, r_lo, r_hi)
    return sigma if sigma > 0 else None


def _run_pipeline(material, regime, box, rng_seed, out_dir,
                  calibrate=True, want_movies=True):
    import tricor as tc
    from ase.io import write

    mat = MATERIALS[material]
    kw = dict(mat["regimes"][regime])
    kw.pop("mace_mode", None)
    has_grains = kw.get("grain_size") is not None
    is_liquid = (regime == "liquid")
    print(f"\n=== {material} / {regime}   box {box:.0f}³ Å ===", flush=True)

    shell, calibrated = _build_shell(material, mat, calibrate=calibrate)
    if calibrated:
        print("  shell: MACE-calibrated", flush=True)
    w = _weights(kw, shell, calibrated)

    cell = tc.Supercell.from_atoms(
        (mat["sp_sources"]["graphite"]() if mat["axis"] == "sp"
         else mat["builder"]()),
        cell_dim_angstroms=(float(box),) * 3,
        r_max=10.0, r_step=0.1, phi_num_bins=36, rng_seed=rng_seed)

    gen = {k: v for k, v in kw.items()
           if k in ("grain_size", "displacement_sigma")}
    if mat["axis"] == "sp":
        ag = mat["sp_sources"]["graphite"]()
        ad = mat["sp_sources"]["diamond"]()
        gen["grain_sources"] = [
            {"atoms": ag, "species_offset": 0, "weight": kw["w_graphite"]},
            {"atoms": ad, "species_offset": 1, "weight": kw["w_diamond"]},
        ]

    timings, stage_atoms = {}, {}
    t0 = time.time()
    cell.generate(shell, num_steps=0, show_progress=False, **gen, **w)
    timings["voronoi"] = time.time() - t0
    stage_atoms["voronoi"] = cell.atoms.copy()
    n_atoms = len(cell.atoms)
    print(f"  stage 1 (Voronoi):  {timings['voronoi']:5.1f}s  ({n_atoms} atoms)",
          flush=True)

    orient_history = None
    t0 = time.time()
    n_acc = 0
    if has_grains:
        cell.refine_initial_orientations(
            shell, capture_trajectory=True, show_progress=False,
            **ORIENT_KW,
            bond_weight=w["bond_weight"], angle_weight=w["angle_weight"],
            repulsion_weight=w["repulsion_weight"],
            hard_core_scale=w["hard_core_scale"],
            nonbond_push_scale=w["nonbond_push_scale"])
        orient_history = cell.refine_initial_orientations_history
        n_acc = max(0, len(orient_history.get("accepted_grain", [])) - 1)
    timings["orient"] = time.time() - t0
    stage_atoms["orient"] = cell.atoms.copy()
    print(f"  stage 2 (orient):   {timings['orient']:5.1f}s  ({n_acc} accepts)",
          flush=True)

    # Cleanup: correct bond topology before the springs act.  Stiff
    # calibrated angle ratios diverge on raw Voronoi overlaps (the
    # FIRE best-restore then returns the input unchanged); bond_relax
    # + enforce_hard_core give the relaxer a physical start.
    t0 = time.time()
    cell.bond_relax(shell, n_iter=80, max_step=0.1)
    cell.enforce_hard_core(shell, n_iter=40)
    timings["cleanup"] = time.time() - t0
    stage_atoms["cleanup"] = cell.atoms.copy()
    print(f"  stage 3 (cleanup):  {timings['cleanup']:5.1f}s", flush=True)

    # FIRE (or quench + thermostat for liquid)
    t0 = time.time()
    thermal_info = None
    if is_liquid:
        cell.shell_relax(shell, num_steps=LIQUID_QUENCH_STEPS,
                         show_progress=False, capture_trajectory=False, **w)

        def _thermal(T, sweeps, capture=False):
            cell.thermal_relax(shell, num_sweeps=sweeps,
                               T_schedule="hold", T_start=T,
                               restore_best=False, show_progress=False,
                               capture_trajectory=capture,
                               capture_stride=20,
                               bond_weight=w["bond_weight"],
                               angle_weight=w["angle_weight"],
                               repulsion_weight=w["repulsion_weight"],
                               hard_core_scale=w["hard_core_scale"],
                               nonbond_push_scale=w["nonbond_push_scale"])

        # Temperature tuning.  Preferred: secant on the MACE
        # single-point energy against the MACE-MD liquid reference
        # (two probes bracket dE/dT).  Fallback when MACE is absent:
        # match the bond-length spread of the MACE liquid artefact,
        # or run at the default temperature.
        T = LIQUID_T0
        calc_t = _load_mace_calc_or_none()
        e_target = None
        if calc_t is not None:
            ref_json = _MACE_OUT / material / "index_summary.json"
            if ref_json.exists():
                gg = json.loads(ref_json.read_text()).get("liquid", {})
                em = (gg.get("energies", {}) or {}).get("mace")
                if em and gg.get("n_atoms"):
                    e_target = em / gg["n_atoms"]
        pos_quench = cell.atoms.positions.copy()
        if e_target is not None:
            def _probe_E(Tp):
                cell.atoms.positions = pos_quench.copy()
                _thermal(Tp, LIQUID_TUNE_SWEEPS)
                probe = cell.atoms.copy()
                probe.calc = calc_t
                return float(probe.get_potential_energy()) / n_atoms
            T1, T2 = LIQUID_T0, LIQUID_T0 * 2.5
            e1, e2 = _probe_E(T1), _probe_E(T2)
            if abs(e2 - e1) > 1e-4:
                T = T1 + (e_target - e1) * (T2 - T1) / (e2 - e1)
            T = float(np.clip(T, 0.004, 0.4))
            cell.atoms.positions = pos_quench.copy()
            print(f"  liquid T tuned on energy: target={e_target:.3f}, "
                  f"probes E({T1:.3f})={e1:.3f} E({T2:.3f})={e2:.3f} "
                  f"-> T={T:.4f}", flush=True)
        else:
            sigma_target = _mace_liquid_sigma(material, mat)
            if sigma_target:
                _thermal(T, LIQUID_TUNE_SWEEPS)
                za, zb, r_lo, r_hi = mat["bond"]
                _, _, sig1, _ = _measure_bond(cell.atoms, za, zb, r_lo, r_hi)
                if sig1 > 1e-3:
                    T = float(np.clip(T * (sigma_target / sig1) ** 2,
                                      0.004, 0.4))
                cell.atoms.positions = pos_quench.copy()
                print(f"  liquid T tuned on sigma: target={sigma_target:.3f}, "
                      f"probe={sig1:.3f} -> T={T:.4f}", flush=True)
        _thermal(T, LIQUID_FINAL_SWEEPS, capture=True)
        fire_history = getattr(cell, "thermal_relax_history", None)
        thermal_info = dict(T=T, sweeps=LIQUID_FINAL_SWEEPS)
    else:
        cell.shell_relax(shell, num_steps=FIRE_STEPS, show_progress=False,
                         capture_trajectory=True, **w)
        fire_history = cell.shell_relax_history
    timings["fire"] = time.time() - t0
    stage_atoms["fire"] = cell.atoms.copy()
    print(f"  stage 4 (FIRE):     {timings['fire']:5.1f}s", flush=True)

    # MACE single-point score of the final structure (optional)
    e_mace_sp = None
    calc = _load_mace_calc_or_none()
    if calc is not None:
        probe = stage_atoms["fire"].copy()
        probe.calc = calc
        e_mace_sp = float(probe.get_potential_energy())
        print(f"  MACE SP: {e_mace_sp / n_atoms:.4f} eV/atom", flush=True)

    # ---- summary ----
    za, zb, r_lo, r_hi = mat["bond"]
    summary = dict(material=material, regime=regime,
                   box_angstrom=float(box), n_atoms=int(n_atoms),
                   timings_s=timings, calibrated=bool(calibrated),
                   n_orient_accepts=int(n_acc),
                   mace_sp_eV=e_mace_sp, thermal=thermal_info)
    for name, atoms in stage_atoms.items():
        peak, mean, std, n = _measure_bond(atoms, za, zb, r_lo, r_hi)
        summary[name] = dict(bond_peak=peak, bond_mean=mean,
                             bond_std=std, n_bonds=n)

    write(str(out_dir / f"{regime}_traj.xyz"),
          [stage_atoms[s] for s in ("voronoi", "orient", "cleanup", "fire")],
          format="extxyz")

    # ---- plots ----
    _stages = {k: stage_atoms[k]
               for k in ("voronoi", "orient", "cleanup", "fire")}
    _plot_bond_hist(_stages, mat, regime, out_dir / f"{regime}_bond_hist.png")
    _plot_angle_hist(_stages, mat, regime, out_dir / f"{regime}_angle_hist.png")
    _plot_gr_stack(_stages, mat, regime, out_dir / f"{regime}_gr.png")

    # ---- movies ----
    if want_movies:
        viz = _viz_for(mat, regime)
        rt = REGIME_TITLES.get(regime, regime)
        _traj_o = (orient_history or {}).get("trajectory")
        if _traj_o is not None and len(_traj_o):
            frames, _ = _subsample(list(_traj_o), 24)
            cell.atoms.positions = np.asarray(frames[0], dtype=np.float64)
            _export_movie_html(cell, frames,
                               out_dir / f"{regime}_orient_movie.html",
                               f"{mat['title']} {rt} — orientation refinement",
                               {})
        traj = (fire_history or {}).get("trajectory")
        if traj is not None and len(traj) > 1:
            frames, _ = _subsample(list(traj), 24)
            cell.atoms.positions = np.asarray(frames[0], dtype=np.float64)
            _export_movie_html(cell, frames,
                               out_dir / f"{regime}_fire_movie.html",
                               f"{mat['title']} {rt} — FIRE relaxation", viz)

    # ---- g3 of the final state ----
    cell.atoms.positions = stage_atoms["fire"].positions.copy()
    cell.measure_g3(show_progress=False)
    cell.export_g3_html(str(out_dir / f"{regime}_g3_fire.html"))

    with open(out_dir / f"{regime}_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    return summary


def _export_overview(material, mat, out_dir):
    import tricor as tc
    from ase.io import read
    from tricor.shells import CoordinationShellTarget
    if mat["axis"] == "sp":
        ref = mat["sp_sources"]["graphite"]()
    else:
        ref = mat["builder"]()
    shell = CoordinationShellTarget.from_atoms(ref, phi_num_bins=36)
    regime_order = (_DISORDER if mat["axis"] == "disorder"
                    else tuple(mat["regimes"]))
    pairs = []
    for r in regime_order:
        traj = out_dir / f"{r}_traj.xyz"
        if traj.exists():
            atoms = read(str(traj), index=-1)
            atoms.wrap()
            pairs.append((_OverviewCell(atoms, shell),
                          REGIME_TITLES.get(r, r)))
    if not pairs:
        return
    from regen_mace_examples import _carbon_viz
    viz = _carbon_viz("mixed_nc") if mat["axis"] == "sp" else mat["viz"]
    cols = 3 if len(pairs) > 3 else len(pairs)
    tc.export_overview_html(
        str(out_dir / "overview.html"), pairs, grid_cols=cols,
        title=f"{mat['title']} — final FIRE structures", **viz)
    print(f"  overview HTML: "
          f"{(out_dir / 'overview.html').stat().st_size / 1024:.0f} KB",
          flush=True)


def main() -> int:
    import warnings
    warnings.filterwarnings("ignore")
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--material", choices=list(MATERIALS) + ["all"],
                   default="all")
    p.add_argument("--regime", default="all")
    p.add_argument("--box", type=float, default=40.0)
    p.add_argument("--rng-seed", type=int, default=2026)
    p.add_argument("--no-calibrate", action="store_true")
    p.add_argument("--no-movies", action="store_true")
    args = p.parse_args()

    _setup_paths()

    materials = list(MATERIALS) if args.material == "all" else [args.material]
    for material in materials:
        mat = MATERIALS[material]
        out_dir = OUT_ROOT / material
        out_dir.mkdir(parents=True, exist_ok=True)
        regimes = (list(mat["regimes"]) if args.regime == "all"
                   else [args.regime])
        idx_path = out_dir / "index_summary.json"
        summaries = {}
        if idx_path.exists():
            try:
                summaries = json.loads(idx_path.read_text())
            except Exception:
                summaries = {}
        for regime in regimes:
            if regime not in mat["regimes"]:
                continue
            try:
                summaries[regime] = _run_pipeline(
                    material, regime, args.box, args.rng_seed, out_dir,
                    calibrate=not args.no_calibrate,
                    want_movies=not args.no_movies)
            except Exception as exc:  # noqa: BLE001
                print(f"\n!! {material}/{regime} failed: "
                      f"{exc.__class__.__name__}: {exc}")
                import traceback
                traceback.print_exc()
                summaries[regime] = {"error": str(exc)}
        try:
            _export_overview(material, mat, out_dir)
        except Exception as exc:  # noqa: BLE001
            print(f"  overview export failed: {exc}")
        with open(idx_path, "w") as f:
            json.dump(summaries, f, indent=2)
        print(f"\nWrote {material} roll-up to {idx_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

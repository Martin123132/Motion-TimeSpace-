from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "class-only-boundary-action-noangular-theorem"
STATUS = "class_only_boundary_action_conditional_noangular_kill_switch_written_not_parent_derived_boundary_coefficients_retained"
CLAIM_CEILING = "class_only_boundary_theorem_target_only_no_boundary_nohair_PPN_EH_WEP_fifth_force_or_local_GR_pass"
NEXT_TARGET = "380-bulk-X-mass-gap-source-normalized-force-law.md"


SOURCE_DOCS = [
    {
        "path": "352-boundary-nohair-and-PPN-residual-vector-gate.md",
        "role": "boundary residual decomposition into monopole, radial trace, trace-free shear, vector, and flux pieces",
    },
    {
        "path": "353-boundary-nohair-theorem-attempt-or-PPN-bound-runner.md",
        "role": "first boundary no-hair theorem contract and proxy residual fallback",
    },
    {
        "path": "354-official-local-bound-source-lock-or-nohair-proof-deepening.md",
        "role": "class-only boundary action, no marker fields, no radial scalar hair, and Ward/Bianchi proof debts",
    },
    {
        "path": "356-parent-action-ward-identity-and-projector-variation.md",
        "role": "boundary force channel in the parent Ward identity and no-hidden-force rule",
    },
    {
        "path": "376-preferred-frame-coefficient-map-or-vector-nohair-theorem.md",
        "role": "B_0i/vector, xi, alpha_i, and unowned flux coefficient maps",
    },
    {
        "path": "377-fifth-force-range-coupling-map.md",
        "role": "radial/fifth-force range-coupling contract and no one-number fifth-force rule",
    },
    {
        "path": "378-source-normalization-Geff-Meff-GM-absorption-theorem.md",
        "role": "GM absorption succeeds only for constant universal Ward-owned monopole; source normalization not parent-derived",
    },
    {
        "path": "375-EH-exterior-operator-or-residual-modified-gravity-ledger.md",
        "role": "boundary/topological residual operators must be theorem-zero or retained as modified-gravity coefficients",
    },
]


BOUNDARY_ACTION_CANDIDATES = [
    {
        "candidate": "class_only_boundary_action",
        "schematic_form": "S_boundary = S_boundary(Q_rel, M_eff, V_scalar, boundary_topological_class)",
        "allowed_data": "scalar total class, conserved monopole, scalar volume/topological class",
        "forbidden_data": "angular representatives, marked patches, local normals, vector frames, l>=1/l>=2 boundary fields",
        "verdict": "conditional_noangular_kill_switch",
    },
    {
        "candidate": "angular_representative_boundary_action",
        "schematic_form": "S_boundary = S_boundary(Q_rel, Y_lm, B_TF, B_0i)",
        "allowed_data": "physical angular boundary modes",
        "forbidden_data": "none",
        "verdict": "reject_for_local_GR_route_unless_coefficients_bounded",
    },
    {
        "candidate": "marker_patch_action",
        "schematic_form": "S_boundary = S_boundary(markers_A, normals_n, active_patch_labels)",
        "allowed_data": "material boundary markers or preferred normals",
        "forbidden_data": "gauge-only treatment",
        "verdict": "preferred_frame_hazard",
    },
    {
        "candidate": "radial_profile_boundary_action",
        "schematic_form": "S_boundary = S_boundary(M_eff(r), B_rad(r), G_eff(r))",
        "allowed_data": "radial source profile",
        "forbidden_data": "GM absorption without theorem",
        "verdict": "fifth_force_beta_deltaG_hazard",
    },
    {
        "candidate": "Ward_owned_flux_boundary_action",
        "schematic_form": "S_boundary with n_mu B^{mu nu} canceled by owned boundary charge/current",
        "allowed_data": "conserved monopole flux with total Ward identity",
        "forbidden_data": "unowned momentum/energy flux",
        "verdict": "conditional_support_not_parent_derived",
    },
]


NOANGULAR_THEOREM_STEPS = [
    {
        "step": 1,
        "statement": "Assume the boundary action depends only on scalar class data.",
        "equation": "S_boundary = S_boundary(Q_rel, M_eff, V_scalar, I_top)",
        "result": "no local angular representative is an argument",
        "status": "assumption_not_parent_derived",
    },
    {
        "step": 2,
        "statement": "Vary trace-free angular boundary data.",
        "equation": "delta S_boundary / delta B_TF,ij = 0",
        "result": "B_TF source absent; xi/gamma shear channel killed",
        "status": "conditional",
    },
    {
        "step": 3,
        "statement": "Vary vector/preferred-frame boundary data.",
        "equation": "delta S_boundary / delta B_0i = 0",
        "result": "boundary vector source absent; alpha1/alpha2 channel killed",
        "status": "conditional",
    },
    {
        "step": 4,
        "statement": "Vary marker/normals/patch labels.",
        "equation": "delta S_boundary / delta n_D^i = delta S_boundary / delta markers_A = 0",
        "result": "preferred normals and patch labels are not physical fields",
        "status": "conditional",
    },
    {
        "step": 5,
        "statement": "Separate scalar monopole from radial scalar hair.",
        "equation": "B_tr = B_tr^mono + B_tr^rad(r), with B_tr^rad=0 required",
        "result": "only constant universal monopole may be safe",
        "status": "radial_hair_not_killed_by_class_only_alone",
    },
    {
        "step": 6,
        "statement": "Require Ward-owned boundary flux.",
        "equation": "n_mu B^{mu nu} + F_boundary_owned^nu = 0",
        "result": "no alpha3/Gdot/fake-Bianchi leakage",
        "status": "mapped_not_proved",
    },
    {
        "step": 7,
        "statement": "Because class-only boundary dependence is not parent-derived, retain coefficients.",
        "equation": "eps_TF, eps_B0i, eps_rad, eps_flux remain active unless theorem-zero",
        "result": "no boundary no-hair pass",
        "status": "actual_current_branch",
    },
]


BOUNDARY_RESIDUAL_COEFFICIENTS = [
    {
        "coefficient": "eps_B_TF",
        "boundary_piece": "B_TF,ij trace-free angular shear",
        "observable_rows": "gamma_minus_1;xi_preferred_location_anisotropy;lensing_slip",
        "theorem_zero_condition": "class-only boundary action has no angular representative/l>=2 argument",
        "current_status": "not_parent_derived",
    },
    {
        "coefficient": "eps_B0i",
        "boundary_piece": "B_0i vector/preferred-frame component",
        "observable_rows": "preferred_frame_alpha1;preferred_frame_alpha2",
        "theorem_zero_condition": "no marker fields, normals, or vector boundary representatives are physical",
        "current_status": "not_parent_derived",
    },
    {
        "coefficient": "eps_B_rad",
        "boundary_piece": "B_tr^rad(r) radial trace hair",
        "observable_rows": "beta_minus_1;delta_G_or_fifth_force_yukawa;perihelion",
        "theorem_zero_condition": "radial hair absent; only constant universal M_eff monopole survives",
        "current_status": "not_parent_derived",
    },
    {
        "coefficient": "eps_B_flux",
        "boundary_piece": "n_mu B^{mu nu} unowned boundary flux",
        "observable_rows": "preferred_frame_alpha3;Gdot_over_G;beta_minus_1;secular_drift",
        "theorem_zero_condition": "boundary flux owned by total Ward/Bianchi identity",
        "current_status": "mapped_not_proved",
    },
    {
        "coefficient": "eps_B_clock_WEP",
        "boundary_piece": "boundary-local matter/clock coupling residue",
        "observable_rows": "alpha_clock_redshift;eta_WEP",
        "theorem_zero_condition": "single observed coframe and no direct boundary matter vertices",
        "current_status": "closure_axiom_required",
    },
    {
        "coefficient": "eps_B_mono",
        "boundary_piece": "B_tr^mono constant conserved monopole",
        "observable_rows": "absorbed_into_measured_GM_if_378_gates_pass",
        "theorem_zero_condition": "not zero; safe only if constant universal conserved calibrated monopole",
        "current_status": "conditional_safe_not_parent_absorbed",
    },
]


OBSERVABLE_JOIN = [
    {
        "observable": "gamma_minus_1",
        "boundary_source": "eps_B_TF + eps_B_rad",
        "source_lock_status": "ready_budget_only",
        "claim_policy": "no pass without theorem-zero or coefficients",
    },
    {
        "observable": "beta_minus_1",
        "boundary_source": "eps_B_rad + nonlinear boundary self-coupling + eps_B_flux",
        "source_lock_status": "ready_budget_only",
        "claim_policy": "no pass without radial/flux theorem or coefficients",
    },
    {
        "observable": "preferred_frame_alpha1_alpha2",
        "boundary_source": "eps_B0i + marker/normal leakage",
        "source_lock_status": "ready_budget_only_after_374_376",
        "claim_policy": "no pass without no-marker/vector theorem or coefficients",
    },
    {
        "observable": "preferred_frame_alpha3",
        "boundary_source": "eps_B_flux / unowned momentum flux",
        "source_lock_status": "contingent_budget_only",
        "claim_policy": "use only if channel exists; no Ward erasure",
    },
    {
        "observable": "xi_preferred_location_anisotropy",
        "boundary_source": "eps_B_TF_lge2 + external/domain anisotropy",
        "source_lock_status": "ready_budget_only_after_374_376",
        "claim_policy": "do not fold xi into gamma only",
    },
    {
        "observable": "delta_G_or_fifth_force_yukawa",
        "boundary_source": "eps_B_rad or finite-range/source-normalized boundary hair",
        "source_lock_status": "parameterized_unscored_after_377",
        "claim_policy": "needs alpha_Y(lambda_Y) or GM absorption theorem",
    },
    {
        "observable": "Gdot_over_G",
        "boundary_source": "time-dependent monopole/flux/source normalization",
        "source_lock_status": "contingent_budget_only",
        "claim_policy": "active if time independence not derived",
    },
]


RUNNER_UPDATE = [
    {
        "runner_row": "boundary_nohair",
        "before_379": "class-only boundary action was conditional template",
        "after_379": "noangular kill switch written but not parent-derived",
        "claim_status": "conditional_only_no_nohair_pass",
    },
    {
        "runner_row": "xi_and_gamma_shear",
        "before_379": "B_TF source not derived zero",
        "after_379": "B_TF killed only if boundary action has no angular arguments",
        "claim_status": "active_coefficients",
    },
    {
        "runner_row": "preferred_frame_alpha1_alpha2",
        "before_379": "B_0i coefficient map active",
        "after_379": "B_0i killed only if no marker/vector boundary data are parent-forbidden",
        "claim_status": "active_coefficients",
    },
    {
        "runner_row": "delta_G_beta_radial_hair",
        "before_379": "GM absorption/fifth-force range gates active",
        "after_379": "radial trace hair not killed by class-only scalar action alone unless monopole-only theorem holds",
        "claim_status": "active_coefficients",
    },
    {
        "runner_row": "alpha3_Gdot_flux",
        "before_379": "Ward-owned flux mapped not proved",
        "after_379": "boundary flux must be owned or retained",
        "claim_status": "contingent_budget_only",
    },
]


FAILURE_MODES = [
    {
        "failure": "class_only_assumed_not_derived",
        "meaning": "using scalar-only boundary dependence as a postulate while claiming no-hair theorem",
        "consequence": "false boundary no-hair pass",
    },
    {
        "failure": "monopole_confused_with_radial_hair",
        "meaning": "calling B_tr^rad(r) measured mass",
        "consequence": "delta_G/beta/fifth-force residual erased",
    },
    {
        "failure": "angular_modes_hidden_in_class",
        "meaning": "allowing Y_lm or trace-free representatives while calling the action class-only",
        "consequence": "xi/gamma/lensing slip hidden",
    },
    {
        "failure": "boundary_vector_called_gauge_without_symmetry",
        "meaning": "dropping B_0i or marker normals without parent gauge principle",
        "consequence": "preferred-frame alpha rows falsely passed",
    },
    {
        "failure": "boundary_flux_erased_without_Ward_owner",
        "meaning": "setting n_mu B^{mu nu}=0 by local-GR desire rather than total identity",
        "consequence": "fake Bianchi closure, alpha3/Gdot drift risk",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "A class-only boundary action would conditionally kill angular shear and vector boundary hair because B_TF and B_0i are not arguments of the action. The parent theory has not derived that class-only restriction, radial trace hair is not killed by it alone, and Ward-owned flux remains open; therefore boundary coefficients stay active.",
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "derive or reject a massive/source-free bulk-X equation with m_X and q_X sufficient to define alpha_X(lambda_X)",
        "pass_condition": "bulk scalar force is theorem-zero, Yukawa-scored, or explicitly retained unscored",
    },
    {
        "priority": 2,
        "target": "381-local-GR-debt-ledger-rollup-after-360-379.md",
        "task": "roll up local-GR debts after WEP/EH/preferred-frame/fifth-force/source/boundary gates",
        "pass_condition": "ready rows, conditional theorem rows, active coefficient rows, and unscored rows are separated",
    },
    {
        "priority": 3,
        "target": "382-boundary-action-parent-selector-or-effective-closure.md",
        "task": "look for a parent selector forcing class-only boundary action, or label it as effective closure",
        "pass_condition": "class-only boundary dependence is derived or closure-labelled",
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_doc in SOURCE_DOCS:
        source_path = ROOT / source_doc["path"]
        rows.append(
            {
                "source_file": source_doc["path"],
                "exists": source_path.exists(),
                "role": source_doc["role"],
            }
        )
    return rows


def gate_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": ";".join(missing_sources) if missing_sources else "all cited source paths exist",
        },
        {
            "gate": "class_only_noangular_theorem_shape_written",
            "status": "conditional_pass",
            "evidence": "if boundary action has no angular/vector arguments then B_TF and B_0i sources vanish",
        },
        {
            "gate": "parent_class_only_boundary_action_derived",
            "status": "fail",
            "evidence": "parent action has not forbidden angular representatives, markers, normals, or radial profiles",
        },
        {
            "gate": "boundary_residual_coefficients_retained",
            "status": "pass",
            "evidence": f"{len(BOUNDARY_RESIDUAL_COEFFICIENTS)} boundary residual coefficients retained/mapped",
        },
        {
            "gate": "radial_trace_hair_killed",
            "status": "fail",
            "evidence": "class-only scalar dependence allows monopole but does not by itself prove no B_tr^rad(r)",
        },
        {
            "gate": "Ward_owned_boundary_flux_derived",
            "status": "fail",
            "evidence": "boundary flux is mapped but not proved owned in total Ward identity",
        },
        {
            "gate": "boundary_nohair_or_PPN_pass_claimed",
            "status": "fail",
            "evidence": "conditional theorem only and no coefficients bounded",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "boundary hair, bulk X, WEP, EH, source-normalization gates remain open",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "boundary_action_candidates.csv", BOUNDARY_ACTION_CANDIDATES)
    write_csv(results_dir / "noangular_theorem_steps.csv", NOANGULAR_THEOREM_STEPS)
    write_csv(results_dir / "boundary_residual_coefficients.csv", BOUNDARY_RESIDUAL_COEFFICIENTS)
    write_csv(results_dir / "observable_join.csv", OBSERVABLE_JOIN)
    write_csv(results_dir / "runner_update.csv", RUNNER_UPDATE)
    write_csv(results_dir / "failure_modes.csv", FAILURE_MODES)
    write_csv(results_dir / "gate_results.csv", gate_rows(source_rows))
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)

    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "boundary_residual_coefficients_retained": len(BOUNDARY_RESIDUAL_COEFFICIENTS),
        "parent_class_only_boundary_action_derived": False,
        "boundary_nohair_pass_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 379 class-only boundary action no-angular theorem artifacts."
    )
    parser.add_argument(
        "--timestamp",
        default=datetime.now().strftime("%Y%m%d-%H%M%S"),
        help="Run timestamp prefix.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_dir = write_run(args.timestamp)
    print(json.dumps({"status": STATUS, "run_dir": str(run_dir)}, indent=2))


if __name__ == "__main__":
    main()

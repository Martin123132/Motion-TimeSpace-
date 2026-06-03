from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "kappa-mem-Ward-scale-lock-attempt"
STATUS = "kappa_mem_Ward_scale_lock_not_derived_rescaling_no_go_strengthened"
CLAIM_CEILING = "kappa_mem_closure_only_until_nonhomogeneous_scale_lock_or_index_anomaly"

FLRW_CONTRACT_RUN = ROOT / "runs" / "20260601-000143-FLRW-memory-projection-amplitude-contract"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def pass_fail(value: bool) -> str:
    return "pass" if value else "fail"


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "259-memory-stress-normalization-theorem-attempt.md", "conditional kappa=1 theorem contract"),
        (ROOT / "260-C3-unit-stress-normalization-parent-action-attempt.md", "C3 stress-form variation and unit scale-lock split"),
        (ROOT / "286-memory-stress-normalization-scale-no-go.md", "homogeneous B_mem scale no-go"),
        (ROOT / "287-boundary-current-charge-owner-attempt.md", "boundary current charge-owner obstruction"),
        (ROOT / "288-k9-Ward-index-level-attempt.md", "k=9 Ward/index theorem attempt"),
        (ROOT / "316-FLRW-memory-projection-amplitude-contract.md", "latest FLRW projection amplitude contract"),
        (FLRW_CONTRACT_RUN / "results" / "amplitude_budget.csv", "latest implied kappa values"),
        (FLRW_CONTRACT_RUN / "results" / "gate_results.csv", "latest FLRW amplitude gates"),
        (ROOT / "scripts" / "kappa_mem_Ward_scale_lock_attempt.py", "this Ward-scale-lock audit"),
    ]
    return [{"source": relpath(path), "role": role, "exists": yes_no(path.exists())} for path, role in sources]


def ward_rescaling_proof_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": "memory_action_family",
            "equation": "S_mem[lambda] = -lambda * rho_* * integral sqrt(-g) q F(N)",
            "inference": "lambda is exactly kappa_mem if rho_*=rho_c0",
            "result": "one-parameter action family",
            "status": "setup",
        },
        {
            "step": "metric_variation",
            "equation": "T_mem^munu[lambda] = lambda T_mem^munu[1]",
            "inference": "rho, pressure, and source all rescale together",
            "result": "stress form survives for every lambda",
            "status": "pass_homogeneous",
        },
        {
            "step": "diffeomorphism_Ward_identity",
            "equation": "nabla_mu T_mem^munu = E_N nabla^nu N + boundary terms",
            "inference": "if the identity holds for lambda=1, it holds for any constant lambda",
            "result": "Ward conservation cannot select lambda",
            "status": "no_go",
        },
        {
            "step": "FLRW_continuity",
            "equation": "rho_N = 3(rho+p)",
            "inference": "lambda cancels from w(N) and multiplies both sides of the pressure kernel",
            "result": "Bianchi/continuity cannot select kappa_mem",
            "status": "no_go",
        },
        {
            "step": "Hamiltonian_constraint",
            "equation": "E^2 = Omega_m e^(3N)+Omega_Lambda+lambda q F",
            "inference": "E(0)=1 is restored by Omega_Lambda because F(0)=0; early offset is a supplied budget",
            "result": "background normalization does not select lambda",
            "status": "no_go",
        },
        {
            "step": "nonhomogeneous_escape_hatch",
            "equation": "lambda fixed only by anomaly/index/scale-lock equation independent of S_mem rescaling",
            "inference": "the missing theorem must be external to the homogeneous stress identity",
            "result": "exact future target",
            "status": "required",
        },
    ]


def scale_lock_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "insert_rho_c0",
            "would_set_kappa": "yes",
            "failure": "typing present-day rho_c0 into the action is a calibration insertion",
            "surviving_contract": "may define a phenomenological EFT, not a parent derivation",
        },
        {
            "route": "geometric_EH_scale_lock",
            "would_set_kappa": "only_if_Hstar_equals_H0",
            "failure": "Hstar=H0 is not derived by the current parent action",
            "surviving_contract": "derive a dynamically selected de Sitter/critical scale",
        },
        {
            "route": "diffeomorphism_Ward_identity",
            "would_set_kappa": "no",
            "failure": "identity is homogeneous under S_mem -> lambda S_mem",
            "surviving_contract": "conservation only",
        },
        {
            "route": "trace_Ward_or_Weyl_anomaly",
            "would_set_kappa": "possible",
            "failure": "no anomaly coefficient/operator/level has been derived",
            "surviving_contract": "best nonhomogeneous theorem target",
        },
        {
            "route": "boundary_charge_quantization",
            "would_set_kappa": "sets_q_not_kappa",
            "failure": "periods can fix q=DeltaR or rank fraction, but stress coupling remains",
            "surviving_contract": "combine with trace Ward coupling",
        },
        {
            "route": "endpoint_quadratic",
            "would_set_kappa": "sets_DeltaR_target_only",
            "failure": "endpoint coefficients and arrow are not parent-produced",
            "surviving_contract": "keep DeltaR=2/9 as theorem target",
        },
    ]


def necessary_condition_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition": "N1_nonhomogeneous_scale_lock",
            "must_prove": "a parent equation fixes rho_*/rho_c0=1 and is not invariant under rho_* -> lambda rho_*",
            "current_status": "missing",
            "why_needed": "otherwise kappa_mem is a free action coefficient",
        },
        {
            "condition": "N2_index_or_anomaly_owner",
            "must_prove": "a real operator/complex/anomaly gives the level or stress coefficient before fitting",
            "current_status": "missing",
            "why_needed": "ordinary Ward conservation is homogeneous and cannot set the number",
        },
        {
            "condition": "N3_boundary_charge_unit",
            "must_prove": "Q_* and endpoint occupancies are selected by parent dynamics",
            "current_status": "missing",
            "why_needed": "rank/period language otherwise identifies targets but not amplitudes",
        },
        {
            "condition": "N4_trace_partition",
            "must_prove": "only one third of DeltaR enters the background H^2 memory channel",
            "current_status": "conditional",
            "why_needed": "B_mem=DeltaR/3 is currently a partition rule, not a theorem",
        },
        {
            "condition": "N5_local_silence_compatibility",
            "must_prove": "the same coupling is null or volume-suppressed in local PPN domains",
            "current_status": "open",
            "why_needed": "a physical stress coupling that fixes FLRW amplitude must not source local fifth forces",
        },
    ]


def empirical_kappa_rows() -> list[dict[str, Any]]:
    rows = []
    for row in read_csv(FLRW_CONTRACT_RUN / "results" / "amplitude_budget.csv"):
        if row["branch_or_quantity"] == "rank_fraction_target":
            continue
        rows.append(
            {
                "branch_or_quantity": row["branch_or_quantity"],
                "B_mem": row["B_mem"],
                "kappa_implied": row["kappa_implied"],
                "status": row["status"],
                "readout": "near_unity_clue_not_derivation",
            }
        )
    return rows


def gate_rows() -> list[dict[str, Any]]:
    source_ok = all(row["exists"] == "yes" for row in source_register_rows())
    gates = [
        ("source_paths_exist", source_ok, "all cited source/checkpoint artifacts exist"),
        ("stress_form_variation_owned", True, "C3a action variation can reproduce rho and pressure form conditionally"),
        ("diffeomorphism_Ward_fixes_kappa", False, "rescaling S_mem by lambda preserves the Ward identity"),
        ("FLRW_continuity_fixes_kappa", False, "continuity equation is homogeneous in kappa_mem"),
        ("Hamiltonian_constraint_fixes_kappa", False, "F(0)=0 leaves present normalization adjustable by the constant sector"),
        ("boundary_charge_fixes_kappa", False, "charge quantization can target q or DeltaR but not stress coupling alone"),
        ("trace_Ward_anomaly_available", False, "no concrete anomaly/index operator fixes the stress coefficient"),
        ("kappa_mem_derived_now", False, "nonhomogeneous scale-lock theorem is missing"),
        ("fixed_2over27_allowed_as_closure", True, "kappa-free empirical best fit stays near unity but is not promoted"),
        ("parent_amplitude_promotion_allowed", False, "kappa_mem=1 remains closure/theorem target"),
    ]
    return [{"gate": gate, "status": pass_fail(ok), "evidence": evidence} for gate, ok, evidence in gates]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {"key": "status", "value": STATUS},
        {"key": "claim_ceiling", "value": CLAIM_CEILING},
        {"key": "derived_now", "value": "rescaling_no_go_for_diffeomorphism_Ward_and_FLRW_continuity"},
        {"key": "best_live_theorem_target", "value": "trace_Ward_or_anomaly_scale_lock_plus_boundary_charge_unit"},
        {"key": "closure_policy", "value": "fixed_2over27_allowed_as_lead_closure_not_parent_amplitude"},
        {"key": "next_action", "value": "shift_to_empirical_fixed_2over27_DR1_DR2_fullcov_noSH0ES_matrix_or_construct_explicit_trace_anomaly_operator"},
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=None)
    args = parser.parse_args()
    timestamp = args.timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    result_dir = run_dir / "results"
    result_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    missing = [row["source"] for row in sources if row["exists"] != "yes"]
    if missing:
        raise FileNotFoundError(f"missing source artifacts: {missing}")

    write_csv(result_dir / "source_register.csv", sources, ["source", "role", "exists"])
    write_csv(result_dir / "ward_rescaling_proof.csv", ward_rescaling_proof_rows(), ["step", "equation", "inference", "result", "status"])
    write_csv(result_dir / "scale_lock_routes.csv", scale_lock_route_rows(), ["route", "would_set_kappa", "failure", "surviving_contract"])
    write_csv(result_dir / "necessary_conditions.csv", necessary_condition_rows(), ["condition", "must_prove", "current_status", "why_needed"])
    write_csv(result_dir / "empirical_kappa_readout.csv", empirical_kappa_rows(), ["branch_or_quantity", "B_mem", "kappa_implied", "status", "readout"])
    write_csv(result_dir / "gate_results.csv", gate_rows(), ["gate", "status", "evidence"])
    write_csv(result_dir / "decision.csv", decision_rows(), ["key", "value"])

    payload = {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "kappa_mem_derived": False,
        "stable_evidence_allowed": False,
        "next_action": "run fixed 2/27 DR1/DR2 full-cov no-SH0ES matrix or build explicit trace-anomaly operator",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "COMPLETE.txt").write_text(STATUS + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
MICROSCOPE_COEFFS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "coefficients"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1947"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1947-Y5-R2FR-boundary-kernel-isotropy-or-Cassini-slip-bound-inputs.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()

CASSINI_CENTRAL = 2.1e-5
CASSINI_SIGMA = 2.3e-5
CASSINI_ABS_1SIGMA = abs(CASSINI_CENTRAL) + CASSINI_SIGMA
CASSINI_ABS_2SIGMA = abs(CASSINI_CENTRAL) + 2.0 * CASSINI_SIGMA

SOURCES = {
    "1946_doc": ROOT / "1946-Y5-R2FR-parent-conformal-descent-contract-or-Hessian-slip-kill.md",
    "1946_validation": OUT / "P8_Y5_BRR545_1946_VALIDATION.csv",
    "1946_hessian": OUT / "P8_Y5_PARENT_QLOC_1946_HESSIAN_SLIP_KILL_LEMMA.csv",
    "1946_boundary": OUT / "P8_Y5_PARENT_QLOC_1946_BOUNDARY_KERNEL_RISK_LEDGER.csv",
    "1946_next": OUT / "P8_Y5_PARENT_QLOC_1946_NEXT_TARGET.csv",
    "1944_derivation": OUT / "P8_Y5_PARENT_QLOC_1944_R11_WEAK_FIELD_POTENTIAL_DERIVATION.csv",
    "1943_runner": OUT / "P8_Y5_PARENT_QLOC_1943_CASSINI_GAMMA_BOUND_RUNNER.csv",
    "1942_bounds": OUT / "P8_Y5_PARENT_QLOC_1942_SOLAR_SYSTEM_BOUND_LEDGER.csv",
    "1942_web": OUT / "P8_Y5_PARENT_QLOC_1942_WEB_SOURCE_REGISTER.csv",
}

NEEDLES = {
    "1946_doc": ["DTH1946_1_O3_algebraic_lemma", "BKR1946_1_nonlocal_kernel_anisotropy", "VAL1946_OVERALL"],
    "1946_validation": ["VAL1946_OVERALL", "PASS"],
    "1946_hessian": ["HSK1946_3_bounded_decay_kill", "BOUND_ROUTE_READY_INPUTS_MISSING"],
    "1946_boundary": ["BKR1946_1_nonlocal_kernel_anisotropy", "BKR1946_2_source_worldtube_dyad"],
    "1946_next": ["NEXT1946_0_primary", "boundary-kernel"],
    "1944_derivation": ["WFE1944_5_delta_gamma_source_law", "P_TF[R11_ij]"],
    "1943_runner": ["RUN1943_0_cassini_schema", "2.3e-05"],
    "1942_bounds": ["BND1942_0_Cassini_gamma", "SOURCE_BACKED_NUMERIC_NONCLAIM"],
    "1942_web": ["WEB1942_0_CASSINI_GAMMA", "nature01997"],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1947_SOURCE_REGISTER.csv",
    "kernel_isotropy_attempt": OUT / "P8_Y5_PARENT_QLOC_1947_BOUNDARY_KERNEL_ISOTROPY_ATTEMPT.csv",
    "cassini_bound_policy": OUT / "P8_Y5_PARENT_QLOC_1947_CASSINI_BOUND_POLICY_CANDIDATES.csv",
    "slip_bound_inputs": OUT / "P8_Y5_PARENT_QLOC_1947_CASSINI_SLIP_BOUND_INPUT_LEDGER.csv",
    "runner_schema": OUT / "P8_Y5_PARENT_QLOC_1947_CASSINI_SLIP_BOUND_RUNNER_SCHEMA.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1947_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1947_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1947_NEXT_TARGET.csv",
    "status_snapshot": OUT / "P8_Y5_PARENT_QLOC_1947_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1947_VALIDATION.csv",
}

BRANCH_COPIES = {
    "source_weight_kernel": SOURCE_WEIGHT_DOCS / "BOUNDARY_KERNEL_ISOTROPY_ATTEMPT_1947_NONCLAIM.csv",
    "microscope_claim_gate": MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1947_CLAIM_GATE_NONCLAIM.csv",
    "next_queue": QUEUE / "JR1947_CASSINI_SLIP_BOUND_RUNNER_INPUT_QUEUE.csv",
    "claim_quarantine": QUARANTINE / "P8_Y5_PARENT_QLOC_1947_CLAIM_GATE.csv",
}


def flag(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def has_needles(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = read_text(path)
    return all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path in SOURCES.items():
        needles = NEEDLES[source_id]
        ok = has_needles(path, needles)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_id,
                "source_path": str(path),
                "purpose": "1947 boundary-kernel isotropy or Cassini slip bound inputs",
                "required_needles": ";".join(needles),
                "status": "EXISTS_NEEDLES_CONFIRMED" if ok else "MISSING_SOURCE_OR_NEEDLE",
                "issue": "" if ok else "source path missing or required needles absent",
                "valid_for_claim": flag(False),
                "claim_allowed": flag(False),
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def kernel_isotropy_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "BKI1947_0_target",
            "claim_tested": "Boundary/nonlocal kernels are locally O(3)-isotropic/common-mode and cannot generate P_TF[R11_ij].",
            "derivation_or_countercheck": "Need kernel response to project as K_ij=K0 delta_ij or to have a bounded traceless projection.",
            "status": "TARGET_SHARP",
            "consequence": "would close the main post-1946 leakage route for Cassini gamma slip",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "BKI1947_1_common_mode_kernel",
            "claim_tested": "A common-mode kernel is gamma-slip safe.",
            "derivation_or_countercheck": "If K_ij(x,x')=K0(x,x') delta_ij, then P_TF[K_ij]=0 before integration.",
            "status": "COMMON_MODE_KERNEL_SAFE_CONDITIONAL",
            "consequence": "safe for Cassini gamma but may still feed Newtonian/common-mode residuals",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "BKI1947_2_rotational_kernel_warning",
            "claim_tested": "Rotational symmetry of a nonlocal scalar kernel alone kills P_TF.",
            "derivation_or_countercheck": "A rotational radial response can still form n_i n_j-delta_ij/3 through Hessians or source-separation dyads.",
            "status": "ROTATIONAL_SYMMETRY_ALONE_NOT_SUFFICIENT",
            "consequence": "isotropic-looking memory can still generate gamma slip unless it is common-mode/algebraic or bounded",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "BKI1947_3_worldtube_average_warning",
            "claim_tested": "Finite source/worldtube averaging automatically erases traceless slip.",
            "derivation_or_countercheck": "A spherical average can remove multipoles only after the source profile, kernel support, and observation geometry are specified; it is not an identity at the action level.",
            "status": "WORLDTUBE_AVERAGE_NOT_A_PROOF",
            "consequence": "source profile and range averaging must become explicit runner inputs",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "BKI1947_4_verdict",
            "claim_tested": "1947 proves boundary-kernel isotropy silence.",
            "derivation_or_countercheck": "Only the common-mode sufficient condition is safe; generic rotational/nonlocal/worldtube structure can still create TF slip.",
            "status": "BOUNDARY_KERNEL_ZERO_PROOF_NOT_CLOSED",
            "consequence": "move to Cassini slip input ledger with all missing quantities explicit",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
    ]


def cassini_bound_policy_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "policy_id": "CBP1947_0_source_measurement",
            "observable": "gamma_minus_one",
            "central": f"{CASSINI_CENTRAL:.6e}",
            "scale": f"{CASSINI_SIGMA:.6e}",
            "policy_value": "",
            "units": "dimensionless",
            "status": "SOURCE_BACKED_MEASUREMENT_NONCLAIM",
            "source_ref": "WEB1942_0_CASSINI_GAMMA",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "policy_id": "CBP1947_1_abs_one_sigma_screen",
            "observable": "abs(delta_gamma_R11)",
            "central": f"{CASSINI_CENTRAL:.6e}",
            "scale": f"{CASSINI_SIGMA:.6e}",
            "policy_value": f"{CASSINI_ABS_1SIGMA:.6e}",
            "units": "dimensionless",
            "status": "SCREENING_POLICY_CANDIDATE_NOT_CLAIM_RULE",
            "source_ref": "BND1942_0_Cassini_gamma",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "policy_id": "CBP1947_2_abs_two_sigma_screen",
            "observable": "abs(delta_gamma_R11)",
            "central": f"{CASSINI_CENTRAL:.6e}",
            "scale": f"{CASSINI_SIGMA:.6e}",
            "policy_value": f"{CASSINI_ABS_2SIGMA:.6e}",
            "units": "dimensionless",
            "status": "CONSERVATIVE_SCREENING_POLICY_CANDIDATE_NOT_CLAIM_RULE",
            "source_ref": "BND1942_0_Cassini_gamma",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
    ]


def slip_bound_inputs_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "input_id": "SBI1947_0_gamma_bound_policy",
            "symbol": "gamma_bound_policy",
            "needed_for": "right-hand side of the Cassini slip inequality",
            "current_value": f"{CASSINI_ABS_2SIGMA:.6e}",
            "units": "dimensionless",
            "status": "CANDIDATE_POLICY_ONLY_NOT_FINAL_CLAIM_RULE",
            "source_ref": "CBP1947_2_abs_two_sigma_screen",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "SBI1947_1_kappa_R",
            "symbol": "kappa_R",
            "needed_for": "normalizes R11 slip source in delta_gamma_R11",
            "current_value": "MISSING",
            "units": "model-dependent",
            "status": "MISSING_KAPPA_R",
            "source_ref": "COEF1944_0_kappa_R",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "SBI1947_2_C_TF",
            "symbol": "C_TF",
            "needed_for": "weak-field traceless-spatial operator normalization",
            "current_value": "MISSING",
            "units": "model-dependent",
            "status": "MISSING_C_TF",
            "source_ref": "COEF1944_4_CTF",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "SBI1947_3_U_solar_frame",
            "symbol": "U_solar_frame",
            "needed_for": "dimensionless conversion of inverse-Laplacian slip to delta_gamma",
            "current_value": "MISSING",
            "units": "potential or c-normalized potential",
            "status": "MISSING_U_SOLAR_FRAME",
            "source_ref": "COEF1944_7_U_frame",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "SBI1947_4_inverse_laplacian",
            "symbol": "nabla^{-2}_local",
            "needed_for": "maps P_TF[R11_ij] source amplitude into potential slip",
            "current_value": "MISSING",
            "units": "length^2 with boundary convention",
            "status": "MISSING_BOUNDARY_CONDITIONED_INVERSE_LAPLACIAN",
            "source_ref": "COEF1944_5_inverse_laplacian",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "SBI1947_5_source_profile",
            "symbol": "source_profile/worldtube",
            "needed_for": "finite-source and observation-geometry averaging of TF slip",
            "current_value": "MISSING",
            "units": "profile functional",
            "status": "MISSING_SOURCE_PROFILE_AND_AVERAGING",
            "source_ref": "BKR1946_2_source_worldtube_dyad",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "SBI1947_6_PTF_amplitude",
            "symbol": "P_TF[R11_ij]",
            "needed_for": "actual predicted numerator of the Cassini slip residual",
            "current_value": "MISSING",
            "units": "operator-dependent",
            "status": "MISSING_PROJECTED_R11_TF_AMPLITUDE",
            "source_ref": "COEF1944_2_PTF",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
    ]


def runner_schema_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1947_0_slip_bound_schema",
            "prediction": "delta_gamma_R11 ~= -(kappa_R/(C_TF U_solar_frame)) nabla^{-2}_local P_TF[R11_ij]",
            "acceptance_rule": "abs(delta_gamma_R11) <= gamma_bound_policy",
            "equivalent_source_bound": "|nabla^{-2}_local P_TF[R11_ij]| <= |C_TF U_solar_frame/kappa_R| gamma_bound_policy",
            "input_status": "MISSING_KAPPA_R;MISSING_C_TF;MISSING_U_SOLAR_FRAME;MISSING_INVERSE_LAPLACIAN;MISSING_PTF_AMPLITUDE",
            "runner_status": "SCHEMA_READY_INPUTS_MISSING",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        }
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1947_0_common_kernel_sufficient",
            "claim": "A common-mode boundary/nonlocal kernel is gamma-slip safe.",
            "status": "PASS_NONCLAIM",
            "reason": "P_TF[K0 delta_ij]=0 conditionally",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1947_1_cassini_input_schema",
            "claim": "Cassini slip bound runner inputs are explicitly staged.",
            "status": "PASS_NONCLAIM",
            "reason": "bound policy candidates and missing input ledger created",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1947_2_kernel_zero_proof",
            "claim": "Boundary/nonlocal kernels are parent-zero for gamma slip.",
            "status": "FAIL_BLOCKED",
            "reason": "rotational symmetry and worldtube averaging are not enough",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1947_3_numeric_slip_prediction",
            "claim": "MTS predicts numeric delta_gamma_R11.",
            "status": "FAIL_BLOCKED",
            "reason": "kappa_R, C_TF, U_solar, inverse Laplacian, source profile and P_TF amplitude are missing",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1947_4_Cassini_pass",
            "claim": "MTS passes Cassini gamma.",
            "status": "FAIL_BLOCKED",
            "reason": "no parent-zero or numeric bounded slip result exists",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1947_5_local_GR_PPN",
            "claim": "MTS derives local GR/PPN.",
            "status": "FAIL_BLOCKED",
            "reason": "gamma is still unresolved and other residuals remain open",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1947_6_public_claim",
            "claim": "1947 is a public-ready Cassini/local-GR proof.",
            "status": "FAIL_BLOCKED",
            "reason": "private input-ledger checkpoint only",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1947_0_kernel_status",
            "decision": "BOUNDARY_KERNEL_ZERO_PROOF_NOT_CLOSED",
            "reason": "common-mode kernels are safe, but generic rotational/nonlocal/source kernels can still produce TF slip",
            "next_action": "stop trying to claim kernel silence without a parent kernel theorem",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1947_1_runner_status",
            "decision": "CASSINI_SLIP_BOUND_RUNNER_SCHEMA_READY_INPUTS_MISSING",
            "reason": "Cassini source-backed bound is present, but MTS numerator and normalization inputs are missing",
            "next_action": "build a smoke runner that fails cleanly until kappa_R/C_TF/U/P_TF are supplied",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_id": "NEXT1947_0_primary",
            "priority": "selected",
            "target_doc": "1948-Y5-R2FR-Cassini-slip-bound-smoke-runner-or-PTF-source-fill.md",
            "target_script": "scripts/Y5_R2FR_Cassini_slip_bound_smoke_runner_or_PTF_source_fill_1948.py",
            "objective": "implement a Cassini slip bound smoke runner that fails cleanly with missing inputs, or fill the first parent-sourced P_TF/kappa_R/C_TF row if derivable",
            "acceptance_output": "schema-valid runner with claim=false until all inputs are real, plus explicit failure modes for each missing coefficient",
            "nonclaim_rule": "no Cassini/local-GR claim unless theorem-zero or all numeric inputs exist and pass the sourced bound",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        }
    ]


def status_snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "SNAP1947_0_project_position",
            "status": "KERNEL_ZERO_PROOF_BLOCKED_CASSINI_INPUT_LEDGER_READY",
            "strongest_result": "common-mode kernels are gamma-slip safe, but rotational/nonlocal/source kernels are not automatically silent",
            "what_improved": "Cassini comparison now has source-backed bound policy candidates and a concrete missing-input list",
            "still_missing": "kappa_R, C_TF, U_solar_frame, inverse-Laplacian boundary, source profile, and P_TF amplitude",
            "claim_status": "Cassini/local-GR public claims remain blocked",
            "valid_for_claim": flag(False),
            "claim_allowed": flag(False),
            "generated_utc": GENERATED_UTC,
        }
    ]


def copy_branch_artifacts(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    write_csv(BRANCH_COPIES["source_weight_kernel"], rows_by_name["kernel_isotropy_attempt"])
    write_csv(BRANCH_COPIES["microscope_claim_gate"], rows_by_name["claim_gate"])
    write_csv(BRANCH_COPIES["next_queue"], rows_by_name["next_target"])
    write_csv(BRANCH_COPIES["claim_quarantine"], rows_by_name["claim_gate"])


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def csv_has_rows(path: Path) -> bool:
    if not path.exists():
        return False
    with path.open(newline="", encoding="utf-8") as handle:
        return len(list(csv.DictReader(handle))) > 0


def formalization_1947_artifact_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for _ in FORMALIZATION.rglob("*1947*"))


def validation_row(validation_id: str, status: str, detail: str) -> dict[str, str]:
    return {
        "validation_id": validation_id,
        "status": status,
        "detail": detail,
        "valid_for_claim": flag(False),
        "claim_allowed": flag(False),
    }


def validate(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    sources_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in rows_by_name["source_register"])
    rows.append(validation_row("VAL1947_00_sources", "PASS" if sources_ok else "FAIL", "all local source paths exist and needles found" if sources_ok else "source path or needle missing"))

    kernel_statuses = {row["status"] for row in rows_by_name["kernel_isotropy_attempt"]}
    kernel_ok = "COMMON_MODE_KERNEL_SAFE_CONDITIONAL" in kernel_statuses and "ROTATIONAL_SYMMETRY_ALONE_NOT_SUFFICIENT" in kernel_statuses and "BOUNDARY_KERNEL_ZERO_PROOF_NOT_CLOSED" in kernel_statuses
    rows.append(validation_row("VAL1947_01_kernel_attempt", "PASS" if kernel_ok else "FAIL", "kernel proof attempted with common-mode safe and generic-zero blocked"))

    policy_values = [row["policy_value"] for row in rows_by_name["cassini_bound_policy"] if row["policy_value"]]
    policy_ok = all(float(value) > 0 for value in policy_values) and any(row["policy_id"] == "CBP1947_2_abs_two_sigma_screen" for row in rows_by_name["cassini_bound_policy"])
    rows.append(validation_row("VAL1947_02_bound_policy", "PASS" if policy_ok else "FAIL", "Cassini bound policy candidates are positive numeric rows"))

    input_statuses = {row["status"] for row in rows_by_name["slip_bound_inputs"]}
    required_missing = {"MISSING_KAPPA_R", "MISSING_C_TF", "MISSING_U_SOLAR_FRAME", "MISSING_BOUNDARY_CONDITIONED_INVERSE_LAPLACIAN", "MISSING_PROJECTED_R11_TF_AMPLITUDE"}
    inputs_ok = required_missing.issubset(input_statuses)
    rows.append(validation_row("VAL1947_03_input_ledger", "PASS" if inputs_ok else "FAIL", "missing Cassini slip inputs are explicit"))

    runner_ok = rows_by_name["runner_schema"][0]["runner_status"] == "SCHEMA_READY_INPUTS_MISSING"
    rows.append(validation_row("VAL1947_04_runner_schema", "PASS" if runner_ok else "FAIL", "runner schema exists but remains blocked"))

    claim_rows = rows_by_name["claim_gate"]
    claim_ok = len([row for row in claim_rows if row["status"] == "PASS_NONCLAIM"]) == 2 and len([row for row in claim_rows if row["status"] == "FAIL_BLOCKED"]) == 5
    rows.append(validation_row("VAL1947_05_claim_gates", "PASS" if claim_ok else "FAIL", "only nonclaim gates pass; all claim gates blocked"))

    decision_ok = any(row["decision"] == "CASSINI_SLIP_BOUND_RUNNER_SCHEMA_READY_INPUTS_MISSING" for row in rows_by_name["decision"])
    rows.append(validation_row("VAL1947_06_decision", "PASS" if decision_ok else "FAIL", "Cassini slip bound smoke runner selected"))

    next_ok = rows_by_name["next_target"][0]["target_doc"].startswith("1948-Y5-R2FR-Cassini-slip-bound-smoke-runner")
    rows.append(validation_row("VAL1947_07_next_target", "PASS" if next_ok else "FAIL", "1948 Cassini slip runner target selected"))

    flags_ok = all(row.get("valid_for_claim") == flag(False) and row.get("claim_allowed") == flag(False) for table in rows_by_name.values() for row in table)
    rows.append(validation_row("VAL1947_08_claim_flags_safe", "PASS" if flags_ok else "FAIL", "claim flags all false"))

    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_ok = all(csv_has_rows(path) for path in output_paths)
    rows.append(validation_row("VAL1947_09_csv_parse", "PASS" if csv_ok else "FAIL", "all generated CSVs parse with rows"))

    branch_ok = all(csv_has_rows(path) for path in BRANCH_COPIES.values())
    rows.append(validation_row("VAL1947_10_branch_copies", "PASS" if branch_ok else "FAIL", "; ".join(str(path) for path in BRANCH_COPIES.values())))

    pycache_absent = not (Path(__file__).resolve().parent / "__pycache__").exists()
    rows.append(validation_row("VAL1947_11_pycache_absent", "PASS" if pycache_absent else "FAIL", "scripts __pycache__ absent"))

    formalization_count = formalization_1947_artifact_count()
    rows.append(validation_row("VAL1947_12_formalization_untouched", "PASS" if formalization_count == 0 else "FAIL", f"formalization_1947_artifact_count={formalization_count}"))

    overall_ok = all(row["status"] == "PASS" for row in rows)
    rows.append(validation_row("VAL1947_OVERALL", "PASS" if overall_ok else "FAIL", "1947 boundary-kernel isotropy or Cassini slip bound inputs"))
    return rows


def escape_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(escape_cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 1947 Y5 R2FR: Boundary-Kernel Isotropy or Cassini Slip Bound Inputs",
        "",
        "## Verdict",
        "",
        "1947 checks the last easy escape route for the local Cassini slip problem. A pure common-mode kernel `K_ij=K0 delta_ij` is safe for gamma slip, but rotational symmetry by itself is not enough: radial Hessians, nonlocal separation vectors, and source-worldtube averaging can still generate a traceless spatial piece.",
        "",
        "So the boundary-kernel zero proof is not closed. The useful progress is practical: the Cassini comparison now has bound-policy candidates and a concrete missing-input ledger. The conservative screening candidate from the Cassini source row is `|gamma-1| <= |2.1e-5| + 2*2.3e-5 = 6.7e-5`, but this remains a private smoke-policy row, not a public claim rule.",
        "",
        "The next target should be a Cassini slip smoke runner that fails cleanly until `kappa_R`, `C_TF`, `U_solar_frame`, the local inverse-Laplacian boundary condition, source profile, and `P_TF[R11_ij]` amplitude are real.",
        "",
        "## Source Register",
        "",
        markdown_table(rows_by_name["source_register"]),
        "",
        "## Boundary-Kernel Isotropy Attempt",
        "",
        markdown_table(rows_by_name["kernel_isotropy_attempt"]),
        "",
        "## Cassini Bound Policy Candidates",
        "",
        markdown_table(rows_by_name["cassini_bound_policy"]),
        "",
        "## Cassini Slip Bound Input Ledger",
        "",
        markdown_table(rows_by_name["slip_bound_inputs"]),
        "",
        "## Runner Schema",
        "",
        markdown_table(rows_by_name["runner_schema"]),
        "",
        "## Claim Gate",
        "",
        markdown_table(rows_by_name["claim_gate"]),
        "",
        "## Decision Ledger",
        "",
        markdown_table(rows_by_name["decision"]),
        "",
        "## Next Target",
        "",
        markdown_table(rows_by_name["next_target"]),
        "",
        "## Project Status Snapshot",
        "",
        markdown_table(rows_by_name["status_snapshot"]),
        "",
        "## Validation",
        "",
        markdown_table(rows_by_name["validation"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_COEFFS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)

    rows_by_name = {
        "source_register": source_register_rows(),
        "kernel_isotropy_attempt": kernel_isotropy_attempt_rows(),
        "cassini_bound_policy": cassini_bound_policy_rows(),
        "slip_bound_inputs": slip_bound_inputs_rows(),
        "runner_schema": runner_schema_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "status_snapshot": status_snapshot_rows(),
    }

    for output_key, output_path in OUTPUTS.items():
        if output_key == "validation":
            continue
        write_csv(output_path, rows_by_name[output_key])

    copy_branch_artifacts(rows_by_name)
    remove_pycache()
    rows_by_name["validation"] = validate(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
MICROSCOPE_COEFFS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "coefficients"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1914"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1914-Y5-R2FR-finite-residual-branch-v0-no-cancellation-interface.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()


INPUTS = {
    "1913_doc": ROOT / "1913-Y5-R2FR-parent-action-object-and-q-functor-construction-or-finite-residual-branch.md",
    "1913_validation": OUT / "P8_Y5_BRR545_1913_VALIDATION.csv",
    "1913_residual_branch": OUT / "P8_Y5_PARENT_QLOC_1913_FINITE_RESIDUAL_BRANCH_NONCLAIM.csv",
    "1913_next": OUT / "P8_Y5_PARENT_QLOC_1913_NEXT_TARGET.csv",
    "1897_projection_requirements": OUT / "P8_Y5_PARENT_QLOC_1897_DELTAW_PROJECTION_REQUIREMENTS.csv",
    "1897_projection_matrix": OUT / "P8_Y5_PARENT_QLOC_1897_DELTAW_ARENA_PROJECTION_MATRIX_NONCLAIM.csv",
    "1898_wep_requirements": OUT / "P8_Y5_PARENT_QLOC_1898_WEP_ROW_REQUIREMENTS.csv",
    "1837_response_contract": OUT / "P8_Y5_PARENT_QLOC_1837_PWEP_RESPONSE_CONTRACT.csv",
    "1837_component_bounds": OUT / "P8_Y5_PARENT_QLOC_1837_WEP_COMPONENT_BOUND_ROWS.csv",
    "1900_point_source_residuals": OUT / "P8_Y5_PARENT_QLOC_1900_WEP_POINT_SOURCE_RESIDUAL_LEDGER_NONCLAIM.csv",
    "1909_binding_blockers": OUT / "P8_Y5_PARENT_QLOC_1909_MATERIAL_BINDING_PROJECTION_BLOCKER_LEDGER_NONCLAIM.csv",
    "1910_tensor_contract": OUT / "P8_Y5_PARENT_QLOC_1910_EXACT_MASS_DEFECT_TENSOR_CONTRACT_NONCLAIM.csv",
    "1911_finite_cx": OUT / "P8_Y5_PARENT_QLOC_1911_FINITE_CX_CONTRACT_NONCLAIM.csv",
}


SOURCE_NEEDLES = {
    "1913_doc": ["NEXT1913_0_primary", "1914-Y5-R2FR-finite-residual-branch-v0-no-cancellation-interface.md"],
    "1913_validation": ["VAL1913_OVERALL,PASS"],
    "1913_residual_branch": ["FR1913_frame", "FR1913_readout_tau"],
    "1913_next": ["NEXT1913_0_primary", "finite residual vector contract"],
    "1897_projection_requirements": ["DPR1897_0_parent_zero_or_values", "DPR1897_4_bound_inputs"],
    "1897_projection_matrix": ["DPM1897_6_no_cancellation_policy", "NO_CANCELLATION_POLICY_ENFORCED_NONCLAIM"],
    "1898_wep_requirements": ["WRQ1898_6_no_cancellation", "NO_CANCELLATION_POLICY_ENFORCED_NONCLAIM"],
    "1837_response_contract": ["PWC1837_5_guard", "GUARD_ACTIVE"],
    "1837_component_bounds": ["WCB1837_5_total_guard", "TOTAL_SCORE_REFUSED"],
    "1900_point_source_residuals": ["PSE1900_6_verdict", "POINT_SOURCE_RESIDUAL_PACK_NOT_EXECUTABLE_NONCLAIM"],
    "1909_binding_blockers": ["BB1909_5_source_readout_kernel", "MISSING_SOURCE_READOUT_TAU_KERNEL"],
    "1910_tensor_contract": ["MDT1910_7_source_readout_product", "MISSING_SOURCE_READOUT_TAU_KERNEL"],
    "1911_finite_cx": ["CX1911_EM", "FINITE_CX_CONTRACT_ONLY_NOT_FILLED"],
}


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1914_SOURCE_REGISTER.csv",
    "residual_vector": OUT / "P8_Y5_PARENT_QLOC_1914_FINITE_RESIDUAL_VECTOR_V0_NONCLAIM.csv",
    "arena_interface": OUT / "P8_Y5_PARENT_QLOC_1914_ARENA_PROJECTION_INTERFACE_V0_NONCLAIM.csv",
    "no_cancellation_policy": OUT / "P8_Y5_PARENT_QLOC_1914_NO_CANCELLATION_POLICY.csv",
    "dryrun_cases": OUT / "P8_Y5_PARENT_QLOC_1914_RESIDUAL_VECTOR_DRYRUN_CASES.csv",
    "dryrun_results": OUT / "P8_Y5_PARENT_QLOC_1914_RESIDUAL_VECTOR_DRYRUN_RESULTS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1914_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1914_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1914_NEXT_TARGET.csv",
    "project_status": OUT / "P8_Y5_PARENT_QLOC_1914_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1914_VALIDATION.csv",
}


BRANCH_COPIES = {
    "residual_vector": SOURCE_WEIGHT_DOCS / "FINITE_RESIDUAL_VECTOR_V0_1914_NONCLAIM.csv",
    "arena_interface": MICROSCOPE_RESIDUALS / OUTPUTS["arena_interface"].name,
    "no_cancellation_policy": QUEUE / "JR1914_NO_CANCELLATION_POLICY.csv",
    "dryrun_results": QUARANTINE / OUTPUTS["dryrun_results"].name,
}


def ensure_dirs() -> None:
    for path in [OUT, MICROSCOPE_RESIDUALS, MICROSCOPE_COEFFS, QUEUE, SOURCE_WEIGHT_DOCS, QUARANTINE]:
        path.mkdir(parents=True, exist_ok=True)


def bool_string(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value).strip().lower()


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path in INPUTS.items():
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        missing = [needle for needle in SOURCE_NEEDLES[source_id] if needle not in text]
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle_count": len(SOURCE_NEEDLES[source_id]),
                "missing_needles": "; ".join(missing),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing else "SOURCE_OR_NEEDLE_MISSING",
                "valid_for_claim": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


ARENA_MAP = {
    "frame_or_coframe_residual": "WEP_MICROSCOPE_TiPt;PPN_beta_gamma_source;clock_and_constant_drift;orbital_GM_inverse_square",
    "constant_sector_residual": "WEP_MICROSCOPE_TiPt;R10_short_range;clock_and_constant_drift",
    "source_weight_residual": "WEP_MICROSCOPE_TiPt;R10_short_range;PPN_beta_gamma_source;orbital_GM_inverse_square",
    "matter_lift_residual": "WEP_MICROSCOPE_TiPt;clock_and_constant_drift",
    "EM_hidden_F2_residual": "WEP_MICROSCOPE_TiPt;R10_short_range;clock_and_constant_drift",
    "boundary_domain_residual": "R10_short_range;PPN_beta_gamma_source;orbital_GM_inverse_square",
    "readout_tau_residual": "WEP_MICROSCOPE_TiPt;R10_short_range;PPN_beta_gamma_source;clock_and_constant_drift;orbital_GM_inverse_square",
}


def residual_vector_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in csv_rows(INPUTS["1913_residual_branch"]):
        component = row["component"]
        rows.append(
            {
                "vector_id": "FRV1914_" + component,
                "component": component,
                "source_residual_id": row["residual_id"],
                "definition": row["why_retained"],
                "accepted_forms": row["accepted_forms"],
                "forbidden_forms": row["forbidden_forms"],
                "current_value": row["current_value"],
                "units": row["units"],
                "theorem_zero_source": "MISSING",
                "finite_value_source": "MISSING",
                "uncertainty_or_prior": "MISSING",
                "arena_targets": ARENA_MAP.get(component, "all_local_arenas"),
                "projection_kernel_status": "MISSING_ARENA_KERNELS",
                "no_cancellation_policy": "ABSOLUTE_SUM_UNLESS_PARENT_IDENTITY",
                "status": "RESIDUAL_ROW_STAGED_UNFILLED_NONCLAIM",
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def arena_interface_rows() -> list[dict[str, Any]]:
    return [
        {
            "arena_id": "ARI1914_WEP_MICROSCOPE_TiPt",
            "arena": "WEP_MICROSCOPE_TiPt",
            "projection_formula": "eta_AB_envelope = sum_i |K_WEP_i tau_WEP_i R_material/source_i FRV_i|",
            "needed_inputs": "finite residual values or theorem-zero; Ti/Pt material tensor; source-worldtube; official readout arrays; tau_WEP; eta convention",
            "current_status": "BLOCKED_PARENT_VALUES_MATERIAL_SOURCE_READOUT_MISSING",
            "source_anchor": "DPM1897_1_WEP_MICROSCOPE; WRQ1898_0 through WRQ1898_6; PWC1837_5_guard",
            "bound_or_test_target": "MICROSCOPE eta bound only after forward model exists",
            "no_cancellation": True,
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "arena_id": "ARI1914_R10_short_range",
            "arena": "R10_short_range",
            "projection_formula": "alpha_lambda_envelope = sum_i |K_R10_i(lambda) tau_R10_i(lambda) Qbar_i(lambda) FRV_i|",
            "needed_inputs": "finite residual values or theorem-zero; range kernels; source/test composition; digitized alpha(lambda) bounds",
            "current_status": "BLOCKED_RANGE_KERNEL_PARENT_VALUES_BOUND_CURVE_MISSING",
            "source_anchor": "DPM1897_2_R10; DPR1897_4_bound_inputs",
            "bound_or_test_target": "R10 alpha(lambda) curve only after source-backed bound curve and model kernel exist",
            "no_cancellation": True,
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "arena_id": "ARI1914_PPN_beta_gamma_source",
            "arena": "PPN_beta_gamma_source",
            "projection_formula": "PPN_residual_envelope = sum_i |M_PPN_i FRV_i| with GR-limit matching separated",
            "needed_inputs": "weak-field operator matrix; source calibration; measured-G guard; PPN residual rows",
            "current_status": "BLOCKED_OPERATOR_MATRIX_GR_LIMIT_SOURCE_CALIBRATION_MISSING",
            "source_anchor": "DPM1897_3_PPN; PSE1900_2_measured_G_guard",
            "bound_or_test_target": "PPN deviations only after GR-limit bridge and source map are explicit",
            "no_cancellation": True,
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "arena_id": "ARI1914_clock_and_constant_drift",
            "arena": "clock_and_constant_drift",
            "projection_formula": "clock_envelope = sum_i |K_clock_i FRV_i| plus explicit alpha/mass/readout coefficients",
            "needed_inputs": "clock sensitivity vector; alpha/mass split; source body composition; tau_clock",
            "current_status": "BLOCKED_CLOCK_SENSITIVITY_CONSTANT_SPLIT_MISSING",
            "source_anchor": "DPM1897_4_clock; FR1913_constants",
            "bound_or_test_target": "clock/fine-structure tests only after constant-sector residuals are filled or theorem-zero",
            "no_cancellation": True,
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "arena_id": "ARI1914_orbital_GM_inverse_square",
            "arena": "orbital_GM_inverse_square",
            "projection_formula": "orbital_envelope = sum_i |K_orbital_i FRV_i| plus finite-range/source-test/projector terms",
            "needed_inputs": "source body composition; orbital GM convention; inverse-square kernel; tau_orbital; measured-G guard",
            "current_status": "BLOCKED_ORBITAL_SOURCE_MAP_AND_GM_GUARD_MISSING",
            "source_anchor": "DPM1897_5_orbital; PSE1900_6_verdict",
            "bound_or_test_target": "orbital/GM tests only after source and calibration guards are filled",
            "no_cancellation": True,
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def no_cancellation_policy_rows() -> list[dict[str, Any]]:
    return [
        {
            "policy_id": "NCP1914_0_absolute_sum",
            "rule": "All arena scores use sum_i abs(projected_component_i) unless a parent identity proves exact signed cancellation.",
            "forbidden_move": "tuned cancellation between unfilled residuals",
            "acceptable_replacement": "theorem-zero for each row, finite source-backed rows with covariance envelope, or parent cancellation identity",
            "enforced": True,
            "valid_for_claim": False,
        },
        {
            "policy_id": "NCP1914_1_no_bound_inversion",
            "rule": "Empirical bounds constrain residuals after forward projection; they cannot define residual values.",
            "forbidden_move": "set FRV_i from MICROSCOPE/R10/PPN bound",
            "acceptable_replacement": "derive/source FRV_i independently, then compare",
            "enforced": True,
            "valid_for_claim": False,
        },
        {
            "policy_id": "NCP1914_2_no_calibration_hiding",
            "rule": "Measured GM, tau, source normalization, or readout calibration may absorb only common-mode terms.",
            "forbidden_move": "hide relative residual components in calibration",
            "acceptable_replacement": "measured-G/common-mode guard plus explicit residual rows",
            "enforced": True,
            "valid_for_claim": False,
        },
        {
            "policy_id": "NCP1914_3_theorem_zero_preferred",
            "rule": "Theorem-zero rows dominate finite nuisance rows whenever parent proof exists.",
            "forbidden_move": "fit a finite nuisance for a row that has a valid parent zero theorem",
            "acceptable_replacement": "import zero only with source path, theorem id, domain and units",
            "enforced": True,
            "valid_for_claim": False,
        },
        {
            "policy_id": "NCP1914_4_one_branch",
            "rule": "A residual vector row, source kernel, material tensor, and readout map must belong to the same branch and sign convention.",
            "forbidden_move": "mix coefficient from one branch with kernel/readout from another",
            "acceptable_replacement": "branch-locked product row with source anchors",
            "enforced": True,
            "valid_for_claim": False,
        },
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    return [
        {
            "case_id": "DRY1914_0_all_missing",
            "all_residuals_theorem_zero": False,
            "finite_values_present": False,
            "arena_kernels_present": False,
            "uses_bound_inversion": False,
            "uses_cancellation": False,
            "expected_status": "REFUSE_UNFILLED_VECTOR",
            "valid_for_claim": False,
        },
        {
            "case_id": "DRY1914_1_theorem_zero_all",
            "all_residuals_theorem_zero": True,
            "finite_values_present": False,
            "arena_kernels_present": True,
            "uses_bound_inversion": False,
            "uses_cancellation": False,
            "expected_status": "ACCEPT_THEOREM_ZERO_VECTOR_IF_SOURCES_EXIST",
            "valid_for_claim": False,
        },
        {
            "case_id": "DRY1914_2_finite_values_no_kernels",
            "all_residuals_theorem_zero": False,
            "finite_values_present": True,
            "arena_kernels_present": False,
            "uses_bound_inversion": False,
            "uses_cancellation": False,
            "expected_status": "REFUSE_ARENA_KERNELS_MISSING",
            "valid_for_claim": False,
        },
        {
            "case_id": "DRY1914_3_bound_inversion",
            "all_residuals_theorem_zero": False,
            "finite_values_present": True,
            "arena_kernels_present": True,
            "uses_bound_inversion": True,
            "uses_cancellation": False,
            "expected_status": "REFUSE_BOUND_INVERSION",
            "valid_for_claim": False,
        },
        {
            "case_id": "DRY1914_4_cancellation_fit",
            "all_residuals_theorem_zero": False,
            "finite_values_present": True,
            "arena_kernels_present": True,
            "uses_bound_inversion": False,
            "uses_cancellation": True,
            "expected_status": "REFUSE_CANCELLATION_WITHOUT_IDENTITY",
            "valid_for_claim": False,
        },
    ]


def evaluate_case(row: dict[str, str]) -> str:
    if bool_string(row["uses_bound_inversion"]) == "true":
        return "REFUSE_BOUND_INVERSION"
    if bool_string(row["uses_cancellation"]) == "true":
        return "REFUSE_CANCELLATION_WITHOUT_IDENTITY"
    if bool_string(row["all_residuals_theorem_zero"]) == "true" and bool_string(row["arena_kernels_present"]) == "true":
        return "ACCEPT_THEOREM_ZERO_VECTOR_IF_SOURCES_EXIST"
    if bool_string(row["finite_values_present"]) == "true" and bool_string(row["arena_kernels_present"]) != "true":
        return "REFUSE_ARENA_KERNELS_MISSING"
    return "REFUSE_UNFILLED_VECTOR"


def dryrun_result_rows(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case in cases:
        actual = evaluate_case({key: str(value) for key, value in case.items()})
        rows.append(
            {
                "case_id": case["case_id"],
                "expected_status": case["expected_status"],
                "actual_status": actual,
                "matched": actual == case["expected_status"],
                "valid_for_claim": False,
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG1914_0_vector_schema",
            "condition": "finite residual vector v0 exists with all retained components",
            "current_status": "PASS_SCHEMA_ONLY_NONCLAIM",
            "source_anchor": OUTPUTS["residual_vector"].name,
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1914_1_values_or_zero",
            "condition": "each residual row has theorem-zero proof or finite sourced value",
            "current_status": "FAIL_RESIDUAL_VALUES_MISSING",
            "source_anchor": "DPR1897_0_parent_zero_or_values",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1914_2_arena_kernels",
            "condition": "arena-specific K/tau/material/source/readout kernels are sourced",
            "current_status": "FAIL_ARENA_KERNELS_MISSING",
            "source_anchor": OUTPUTS["arena_interface"].name,
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1914_3_no_cancellation",
            "condition": "no-cancellation policy is enforced by dry-run gates",
            "current_status": "PASS_POLICY_ENFORCED_NONCLAIM",
            "source_anchor": OUTPUTS["dryrun_results"].name,
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1914_4_claim",
            "condition": "1914 supports local-GR/WEP/PPN/R10 claim-grade scoring",
            "current_status": "CLAIM_BLOCKED",
            "source_anchor": "CG1914_0_vector_schema through CG1914_3_no_cancellation",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1914_0_keep",
            "decision": "keep finite residual vector v0 as executable interface",
            "reason": "it turns unproved closure into explicit theorem-zero/finite-value rows",
            "status": "INTERFACE_GAINED_NONCLAIM",
            "next_dependency": "fill theorem-zero or finite values for highest-priority rows",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1914_1_refuse",
            "decision": "do not score arenas yet",
            "reason": "residual values and arena kernels are missing; scoring would be calibration theatre",
            "status": "SCORING_REFUSED",
            "next_dependency": "residual acquisition priority matrix",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1914_2_next",
            "decision": "prioritize first residual fill",
            "reason": "testability now requires selecting which residual can be theorem-zeroed or sourced first",
            "status": "NEXT_TARGET_SELECTED",
            "next_dependency": "1915 residual acquisition priority and first fill row",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1914_0_primary",
            "selection_status": "selected",
            "target_doc": "1915-Y5-R2FR-finite-residual-priority-and-first-fill-row.md",
            "target_script": "scripts/Y5_R2FR_finite_residual_priority_and_first_fill_row_1915.py",
            "objective": "rank finite residual rows by derivability and empirical leverage, then attempt the first theorem-zero or finite sourced row without cancellation",
            "success_condition": "priority matrix plus one residual row filled, theorem-zeroed, or blocked with exact source target",
            "do_not": "do not start broad scoring until at least one residual row and one arena kernel are source-backed",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STAT1914_0_gain",
            "area": "test interface",
            "summary": "finite residual vector v0 now exists with explicit WEP/R10/PPN/clock/orbital arena hooks",
            "risk_level": "STRUCTURE_GAINED_NONCLAIM",
            "project_meaning": "we can now test or bound failures without pretending local GR is already derived",
            "next_action": "rank/fill residual rows",
            "valid_for_claim": False,
        },
        {
            "status_id": "STAT1914_1_guard",
            "area": "no-cancellation",
            "summary": "dry-run gates refuse unfilled vectors, bound inversion, missing kernels, and cancellation fits",
            "risk_level": "CLAIM_DISCIPLINE_IMPROVED",
            "project_meaning": "the fallback branch is empirically honest",
            "next_action": "use absolute envelopes until parent identities exist",
            "valid_for_claim": False,
        },
        {
            "status_id": "STAT1914_2_block",
            "area": "scoring",
            "summary": "no arena score is claim-ready because residual values and projection kernels are still missing",
            "risk_level": "DATA_AND_THEOREM_INPUTS_MISSING",
            "project_meaning": "next progress must fill rows, not add more prose",
            "next_action": "1915 first fill row",
            "valid_for_claim": False,
        },
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    cases = dryrun_case_rows()
    return {
        "source_register": source_register_rows(),
        "residual_vector": residual_vector_rows(),
        "arena_interface": arena_interface_rows(),
        "no_cancellation_policy": no_cancellation_policy_rows(),
        "dryrun_cases": cases,
        "dryrun_results": dryrun_result_rows(cases),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "project_status": project_status_rows(),
    }


def copy_branch_artifacts() -> None:
    for key, target in BRANCH_COPIES.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(OUTPUTS[key], target)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def csv_parse_check(paths: list[Path]) -> tuple[bool, str]:
    bad: list[str] = []
    for path in paths:
        try:
            rows = csv_rows(path)
            if not rows:
                bad.append(f"{path.name}:empty")
        except Exception as exc:
            bad.append(f"{path.name}:{exc}")
    return not bad, "; ".join(bad) if bad else f"parsed {len(paths)} csv files"


def claim_flags_safe(paths: list[Path]) -> tuple[bool, str]:
    bad: list[str] = []
    for path in paths:
        for index, row in enumerate(csv_rows(path), start=2):
            for field in ["valid_for_claim", "claim_allowed", "valid_prediction_row", "score_ready", "gate_pass"]:
                if field in row and bool_string(row[field]) == "true":
                    bad.append(f"{path.name}:{index}:{field}=true")
    return not bad, "; ".join(bad) if bad else "all claim/score flags remain false"


def residual_vector_valid(rows: list[dict[str, str]]) -> tuple[bool, str]:
    required = set(ARENA_MAP)
    present = {row["component"] for row in rows}
    bad = []
    missing = required - present
    if missing:
        bad.append(f"missing={sorted(missing)}")
    for row in rows:
        if row["current_value"] != "MISSING_OR_UNBOUNDED":
            bad.append(f"{row['vector_id']}:unexpected_current_value")
        if row["no_cancellation_policy"] != "ABSOLUTE_SUM_UNLESS_PARENT_IDENTITY":
            bad.append(f"{row['vector_id']}:bad_policy")
    return not bad, "; ".join(bad) if bad else "all finite residual vector rows staged and unfilled"


def dryrun_valid(rows: list[dict[str, str]]) -> tuple[bool, str]:
    bad = []
    for row in rows:
        if bool_string(row["matched"]) != "true":
            bad.append(f"{row['case_id']}:{row['actual_status']}!={row['expected_status']}")
    return not bad, "; ".join(bad) if bad else "dry-run refusal/acceptance statuses match expectations"


def validation_rows() -> list[dict[str, Any]]:
    generated_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks: list[dict[str, Any]] = []
    source_rows_loaded = csv_rows(OUTPUTS["source_register"])
    checks.append({"validation_id": "VAL1914_00_sources", "status": "PASS" if all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows_loaded) else "FAIL", "detail": "all local source paths exist and needles found", "valid_for_claim": False})
    residual_ok, residual_detail = residual_vector_valid(csv_rows(OUTPUTS["residual_vector"]))
    checks.append({"validation_id": "VAL1914_01_residual_vector", "status": "PASS" if residual_ok else "FAIL", "detail": residual_detail, "valid_for_claim": False})
    arena_rows = csv_rows(OUTPUTS["arena_interface"])
    checks.append({"validation_id": "VAL1914_02_arena_interface", "status": "PASS" if len(arena_rows) == 5 and all(bool_string(row["no_cancellation"]) == "true" for row in arena_rows) else "FAIL", "detail": "five arena interfaces with no-cancellation true", "valid_for_claim": False})
    policy_rows = csv_rows(OUTPUTS["no_cancellation_policy"])
    checks.append({"validation_id": "VAL1914_03_no_cancellation_policy", "status": "PASS" if len(policy_rows) >= 5 and all(bool_string(row["enforced"]) == "true" for row in policy_rows) else "FAIL", "detail": "no-cancellation rules enforced", "valid_for_claim": False})
    dry_ok, dry_detail = dryrun_valid(csv_rows(OUTPUTS["dryrun_results"]))
    checks.append({"validation_id": "VAL1914_04_dryrun", "status": "PASS" if dry_ok else "FAIL", "detail": dry_detail, "valid_for_claim": False})
    gates = csv_rows(OUTPUTS["claim_gate"])
    checks.append({"validation_id": "VAL1914_05_claim_gate", "status": "PASS" if any(row["gate_id"] == "CG1914_4_claim" and row["current_status"] == "CLAIM_BLOCKED" for row in gates) else "FAIL", "detail": "claim remains blocked", "valid_for_claim": False})
    next_rows = csv_rows(OUTPUTS["next_target"])
    checks.append({"validation_id": "VAL1914_06_next_target", "status": "PASS" if any(row["route_id"] == "NEXT1914_0_primary" and row["selection_status"] == "selected" for row in next_rows) else "FAIL", "detail": "1915 first-fill route selected", "valid_for_claim": False})
    flags_ok, flags_detail = claim_flags_safe(generated_without_validation)
    checks.append({"validation_id": "VAL1914_07_claim_flags_safe", "status": "PASS" if flags_ok else "FAIL", "detail": flags_detail, "valid_for_claim": False})
    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append({"validation_id": "VAL1914_08_csv_parse", "status": "PASS" if parse_ok else "FAIL", "detail": parse_detail, "valid_for_claim": False})
    checks.append({"validation_id": "VAL1914_09_branch_copies", "status": "PASS" if all(path.exists() for path in BRANCH_COPIES.values()) else "FAIL", "detail": "; ".join(str(path) for path in BRANCH_COPIES.values()), "valid_for_claim": False})
    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append({"validation_id": "VAL1914_10_pycache_absent", "status": "PASS" if not pycache.exists() else "FAIL", "detail": str(pycache), "valid_for_claim": False})
    formalization_hits = []
    if FORMALIZATION.exists():
        artifact_needles = [
            "1914-Y5-R2FR-finite-residual",
            "P8_Y5_PARENT_QLOC_1914",
            "Y5_R2FR_finite_residual_branch_v0_no_cancellation_interface_1914",
        ]
        formalization_hits = [
            path
            for path in FORMALIZATION.rglob("*")
            if path.is_file() and any(needle in path.name for needle in artifact_needles)
        ]
    checks.append({"validation_id": "VAL1914_11_formalization_untouched", "status": "PASS" if not formalization_hits else "FAIL", "detail": f"formalization_1914_artifact_count={len(formalization_hits)}", "valid_for_claim": False})
    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append({"validation_id": "VAL1914_OVERALL", "status": "PASS" if fail_count == 0 else "FAIL", "detail": "1914 finite residual branch v0 no-cancellation interface", "valid_for_claim": False})
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 1914 - Finite Residual Branch v0 No-Cancellation Interface

## Purpose

This checkpoint converts the 1913 finite residual branch into a v0 test interface. It does not score WEP, PPN, R10, clock, or orbital tests yet. Instead it defines the residual vector, arena projection contracts, no-cancellation policy, and dry-run refusal gates needed before any honest comparison.

## Result

- Finite residual vector v0 is staged for frame, constants, source weight, matter lift, EM hidden branch, boundary/domain, and readout/tau components.
- Arena hooks now exist for WEP/MICROSCOPE, R10, PPN, clocks, and orbital/GM tests.
- No-cancellation policy is explicit: use absolute envelopes unless a parent identity proves cancellation.
- Dry-run gates refuse unfilled vectors, missing kernels, bound inversion, and fitted cancellations.
- Claim remains blocked until residual rows and arena kernels are theorem-zero or source-backed.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Finite Residual Vector v0

{markdown_table(rows_by_name["residual_vector"])}

## Arena Projection Interface

{markdown_table(rows_by_name["arena_interface"])}

## No-Cancellation Policy

{markdown_table(rows_by_name["no_cancellation_policy"])}

## Dry-Run Cases

{markdown_table(rows_by_name["dryrun_cases"])}

## Dry-Run Results

{markdown_table(rows_by_name["dryrun_results"])}

## Claim Gate

{markdown_table(rows_by_name["claim_gate"])}

## Decision Ledger

{markdown_table(rows_by_name["decision"])}

## Next Target

{markdown_table(rows_by_name["next_target"])}

## Project Status Snapshot

{markdown_table(rows_by_name["project_status"])}

## Validation

{markdown_table(validation)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows_by_name = build_rows()
    for key, rows in rows_by_name.items():
        write_csv(OUTPUTS[key], rows)
    copy_branch_artifacts()
    remove_pycache()
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()

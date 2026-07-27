from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "2701"
BRANCH_ID = "Y5_R2FR_Q_LOC_PPN_KERNEL_OR_R10_ALPHA_RESPONSE_OPERATOR_FILL_2701"

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTAKE = ROOT / "source-intake"
RESIDUALS = SOURCE_INTAKE / "mts_residuals"
LOCAL_BOUNDS = SOURCE_INTAKE / "local_bounds"
WEP_RESIDUALS = SOURCE_INTAKE / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT = SOURCE_INTAKE / "source-weight"
RAB_QUEUE = SOURCE_INTAKE / "rab-sector" / "acquisition-queue"

DOC_PATH = ROOT / "2701-Y5-R2FR-q-loc-PPN-kernel-or-R10-alpha-response-operator-fill.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2701_SOURCE_REGISTER.csv",
    "ppn_kernel_audit": RESIDUALS / "P8_Y5_R2FR_2701_PPN_KERNEL_DERIVATION_AUDIT.csv",
    "r10_operator": RESIDUALS / "P8_Y5_R2FR_2701_R10_ALPHA_RESPONSE_OPERATOR_NONCLAIM.csv",
    "r10_smoke_rows": RESIDUALS / "P8_Y5_R2FR_2701_R10_ALPHA_QLOC_SMOKE_ROWS_NONCLAIM.csv",
    "missing_inputs": RESIDUALS / "P8_Y5_R2FR_2701_R10_ALPHA_MISSING_INPUTS.csv",
    "bound_asset_status": RESIDUALS / "P8_Y5_R2FR_2701_R10_BOUND_ASSET_STATUS.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2701_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2701_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2701_NEXT_TARGET.csv",
    "project_status": RESIDUALS / "P8_Y5_R2FR_2701_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2701_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_r10_operator": LOCAL_BOUNDS / "q_loc_R10_alpha_response_operator_2701_NONCLAIM.csv",
    "local_r10_smoke": LOCAL_BOUNDS / "q_loc_R10_alpha_smoke_rows_2701_NONCLAIM.csv",
    "wep_r10_operator": WEP_RESIDUALS / "q_loc_R10_alpha_response_operator_2701_NONCLAIM.csv",
    "source_weight_r10_operator": SOURCE_WEIGHT / "QLOC_R10_ALPHA_RESPONSE_OPERATOR_2701_NONCLAIM.csv",
    "rab_next": RAB_QUEUE / "JR2701_QLOC_R10_PROFILE_OR_BOUND_CURVE_NEXT.csv",
}

SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "source_id": "SRC2701_2700_NEXT",
        "relative_path": "2700-Y5-R2FR-Gamma-eff-candidate-metric-response-or-first-q-loc-response-row.md",
        "required_needles": ["QOP2700_0_PPN_GK_q_loc_response_operator", "MISS2700_0_K_PPN_kernel", "NEXT2700_0_selected", "VAL2700_OVERALL"],
        "purpose": "imports the staged PPN operator row and selected 2701 target",
    },
    {
        "source_id": "SRC2701_2206_APQ",
        "relative_path": "2206-Y5-R2FR-GammaKhat-q-loc-parent-action-signature-or-official-residual-demotion.md",
        "required_needles": ["APQ2206_0_PPN", "APQ2206_1_R10", "QDEM2206_9_total"],
        "purpose": "imports q_loc PPN/R10 projection queue and total residual",
    },
    {
        "source_id": "SRC2701_2581_TESTS",
        "relative_path": "2581-Y5-R2FR-GammaKhat-q_loc-coupling-double-zero-or-residual-lock.md",
        "required_needles": ["TEST2581_0_PPN_alpha", "TEST2581_1_R10", "QLOC2581_TOTAL"],
        "purpose": "imports official q_loc local-test residual interface",
    },
    {
        "source_id": "SRC2701_563_R10",
        "relative_path": "563-Y5-R10-real-bound-curve-acquisition-and-alpha-row-smoke-runner.md",
        "required_needles": ["E563_1_full_curve_missing", "E563_2_mts_parent_coefficients_missing", "V563_10_no_overclaim"],
        "purpose": "imports R10 bound/source-plumbing status and no-claim ceiling",
    },
    {
        "source_id": "SRC2701_BOUND_ANCHORS",
        "relative_path": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv",
        "required_needles": ["R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM", "R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM"],
        "purpose": "imports nonclaim Eot-Wash anchor rows for smoke checks only",
    },
    {
        "source_id": "SRC2701_LIVE_BOUND_PLACEHOLDER",
        "relative_path": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
        "required_needles": ["R10_BOUND_PLACEHOLDER_0", "MISSING_NUMERIC_LAMBDA"],
        "purpose": "imports live placeholder bound curve that remains invalid for claim scoring",
    },
    {
        "source_id": "SRC2701_R10_PREFACTOR",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_ZX_LAMBDA_PREFACtOR_FORMULA_REGISTER.csv",
        "required_needles": ["PR562_4_prefactor", "PR562_6_spectral_generalization"],
        "purpose": "imports earlier Yukawa alpha(lambda) prefactor grammar for comparison",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def as_bool(value: bool) -> str:
    return "true" if value else "false"


def path_for(relative_path: str) -> Path:
    return ROOT / relative_path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            if not reader.fieldnames:
                return False, 0, "missing_header"
            return True, len(rows), "parsed"
    except Exception as exc:  # pragma: no cover
        return False, 0, f"{type(exc).__name__}: {exc}"


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        cells = [str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = path_for(spec["relative_path"])
        text = read_text(path)
        needles = list(spec["required_needles"])
        found = [needle for needle in needles if needle in text]
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "source_id": spec["source_id"],
                "relative_path": spec["relative_path"],
                "absolute_path": str(path),
                "exists": as_bool(path.exists()),
                "required_needles": ";".join(needles),
                "found_needles": ";".join(found),
                "missing_needles": ";".join(missing),
                "purpose": spec["purpose"],
                "valid_for_claim": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def ppn_kernel_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("PPN2701_0_input", "PPN response target", "Delta_PPN_GK^a = integral K_PPN^a{}_nu q_loc^nu dV", "requires metric perturbation response, source normalization, q_loc profile and observed frame", "from 2700 operator row", "TOO_UNDERDETERMINED"),
        ("PPN2701_1_metric_response", "metric response matrix", "delta g_obs / delta q_loc or delta g_obs / delta T_GK", "required to know whether q_loc sources gamma,beta,alpha_i,zeta_i,xi", "QLOC2699_6_readout says metric response matrix missing", "MISSING"),
        ("PPN2701_2_source_frame", "source-normalized frame", "same M_eff/H_tau/Pi_M source map before PPN readout", "otherwise q_loc projection can hide source-measure residuals", "2700 missing inputs include source_normalization_map", "MISSING"),
        ("PPN2701_3_profile", "q_loc radial/source profile", "q_loc^nu(r,source,frame,lambda)", "PPN kernel cannot be evaluated without profile support and dimensions", "QLOC2581 rows have MISSING_NUMERIC_VALUE", "MISSING"),
        ("PPN2701_4_verdict", "PPN kernel derivation status", "K_PPN cannot be derived from current inputs", "fallback to R10 alpha(lambda) operator because the Yukawa acceleration-ratio form is explicit", "NEXT2700 allows R10 fallback", "PPN_KERNEL_REJECTED_FOR_NOW"),
    ]
    return [
        {
            "audit_id": audit_id,
            "object": obj,
            "mathematical_form": form,
            "requirement": req,
            "evidence": evidence,
            "status": status,
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for audit_id, obj, form, req, evidence, status in rows
    ]


def r10_operator_rows() -> list[dict[str, Any]]:
    source_paths = ";".join(
        str(path_for(path))
        for path in [
            "2700-Y5-R2FR-Gamma-eff-candidate-metric-response-or-first-q-loc-response-row.md",
            "563-Y5-R10-real-bound-curve-acquisition-and-alpha-row-smoke-runner.md",
            "2206-Y5-R2FR-GammaKhat-q-loc-parent-action-signature-or-official-residual-demotion.md",
            "2581-Y5-R2FR-GammaKhat-q_loc-coupling-double-zero-or-residual-lock.md",
        ]
    )
    return [
        {
            "operator_id": "R10OP2701_0_QLOC_YUKAWA_ALPHA_RESPONSE",
            "arena": "R10_short_range",
            "input_residual": "q_loc_radial_acceleration_profile",
            "operator_symbol": "R_R10_alpha[q_loc;lambda,r_window,source]",
            "force_law_reference": "a_Y/a_N = alpha(lambda)*(1+r/lambda)*exp(-r/lambda)",
            "response_formula": "alpha_q(lambda;r)=a_q(r,lambda)/a_N(r)*exp(r/lambda)/(1+r/lambda)",
            "conservative_envelope": "abs_alpha_q(lambda)=sup_{r in window}|a_q(r,lambda)/a_N(r)|*exp(r/lambda)/(1+r/lambda)",
            "input_units": "a_q in m s^-2 or dimensionless a_q/a_N after source normalization",
            "output_units": "dimensionless alpha(lambda)",
            "source_paths": source_paths,
            "claim_status": "SCHEMA_ONLY_NONCLAIM",
            "score_ready": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "notes": "This maps q_loc to the same alpha(lambda) language used by inverse-square-law tests, but it needs a source-backed q_loc profile, source mass and full bound curve before scoring.",
            "timestamp_utc": stamp(),
        },
        {
            "operator_id": "R10OP2701_1_QLOC_FORCE_DENSITY_CONVERSION",
            "arena": "R10_short_range",
            "input_residual": "q_loc_force_density_or_stress_divergence",
            "operator_symbol": "a_q=q_loc/rho_test or q_loc/m_test after matter-frame normalization",
            "force_law_reference": "convert residual force density to test-body acceleration before alpha projection",
            "response_formula": "alpha_q(lambda;r)=q_loc^r(r,lambda)/(rho_test*a_N(r))*exp(r/lambda)/(1+r/lambda)",
            "conservative_envelope": "use absolute component envelope with no cancellation between q_loc defects",
            "input_units": "force_density N m^-3 or acceleration m s^-2 after normalization",
            "output_units": "dimensionless alpha(lambda)",
            "source_paths": source_paths,
            "claim_status": "UNIT_CONVERSION_SCHEMA_ONLY",
            "score_ready": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "notes": "The rho_test/m_test normalization is the live missing source-frame input; this row prevents silently comparing incompatible units.",
            "timestamp_utc": stamp(),
        },
    ]


def r10_smoke_rows() -> list[dict[str, Any]]:
    rows = [
        ("R10SMOKE2701_0_2020_anchor", "3.86e-5", "m", "alpha_q(lambda;r)=MISSING_QLOC_PROFILE_TO_ALPHA", "1.0", "R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM", "anchor_only_non_curve", "false"),
        ("R10SMOKE2701_1_2007_anchor", "5.6e-5", "m", "alpha_q(lambda;r)=MISSING_QLOC_PROFILE_TO_ALPHA", "1.0", "R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM", "anchor_only_non_curve", "false"),
    ]
    return [
        {
            "row_id": row_id,
            "lambda_value": lambda_value,
            "lambda_units": units,
            "alpha_predicted": alpha_pred,
            "alpha_bound_anchor": bound,
            "bound_reference": reference,
            "bound_status": bound_status,
            "score_ready": "false",
            "valid_for_claim": valid,
            "claim_allowed": "false",
            "notes": "Smoke row only: alpha prediction is a formula slot, not a number; anchor bound is not a digitized curve.",
            "timestamp_utc": stamp(),
        }
        for row_id, lambda_value, units, alpha_pred, bound, reference, bound_status, valid in rows
    ]


def missing_input_rows() -> list[dict[str, Any]]:
    rows = [
        ("MISS2701_0_q_loc_profile", "q_loc^r(r,lambda,source,frame)", "radial acceleration or force-density profile", "required to calculate alpha_q(lambda)", "MISSING_PROFILE"),
        ("MISS2701_1_source_mass", "M_source or a_N(r)=G M_source/r^2", "source-normalized Newtonian acceleration", "required denominator for alpha ratio", "MISSING_SOURCE_MEASURE_LOCK"),
        ("MISS2701_2_test_body_normalization", "rho_test or m_test map", "convert force density/stress divergence to test acceleration", "required if q_loc is not already acceleration", "MISSING_MATTER_FRAME_NORMALIZATION"),
        ("MISS2701_3_range_kernel", "lambda dependence of q_loc", "project q_loc onto Yukawa range lambda", "required to sample alpha(lambda)", "MISSING_RANGE_KERNEL"),
        ("MISS2701_4_bound_curve", "full alpha_bound(lambda) curve", "dense or interpolable source-backed bound rows", "required for claim scoring", "MISSING_FULL_DIGITIZED_BOUND_CURVE"),
        ("MISS2701_5_anchor_policy", "anchor-only nonclaim policy", "do not treat alpha=1 threshold anchors as full curve", "prevents false R10 pass", "ANCHORS_NONCLAIM_ONLY"),
        ("MISS2701_6_no_cancellation", "absolute q_loc component envelope", "sum/bound residual components without cancellation credit", "required for conservative local tests", "MISSING_COMPONENT_VALUES"),
    ]
    return [
        {
            "missing_id": missing_id,
            "input": input_name,
            "purpose": purpose,
            "why_required": why,
            "status": status,
            "source_backed": "false",
            "score_ready": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
        for missing_id, input_name, purpose, why, status in rows
    ]


def bound_asset_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("BOUND2701_0_live_digitized", "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv", "placeholder_invalid", "MISSING_NUMERIC_LAMBDA and missing digitized alpha_bound rows", "false"),
        ("BOUND2701_1_anchor_smoke", "source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv", "anchor_only_non_curve", "two positive Eot-Wash threshold anchors useful for smoke plumbing only", "false"),
        ("BOUND2701_2_mts_smoke", "source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_SMOKE_NONCLAIM.csv", "symbolic_nonclaim", "alpha_predicted uses symbolic parent coefficients, not numeric q_loc/R10 projection", "false"),
        ("BOUND2701_3_required", "future_full_curve_or_table", "missing", "full digitized or machine-readable alpha(lambda) curve needed before claim scoring", "false"),
    ]
    return [
        {
            "asset_id": asset_id,
            "asset_path_or_name": path,
            "status": status,
            "detail": detail,
            "valid_for_claim": valid,
            "timestamp_utc": stamp(),
        }
        for asset_id, path, status, detail, valid in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2701_0_PPN_kernel", "PPN response kernel is derived", "BLOCKED_NONCLAIM", "false", "false", "metric response, source frame and q_loc profile are missing"),
        ("CG2701_1_R10_operator", "R10 alpha(lambda) response operator exists", "PASS_SCHEMA_ONLY", "true", "false", "operator formula is written but not score-ready"),
        ("CG2701_2_R10_profile", "q_loc alpha(lambda) prediction is numeric", "BLOCKED_NONCLAIM", "false", "false", "q_loc profile/range/source normalization missing"),
        ("CG2701_3_bound_curve", "R10 bound curve is claim-valid", "BLOCKED_NONCLAIM", "false", "false", "only placeholder plus anchor-only rows exist"),
        ("CG2701_4_R10_pass", "R10/fifth-force pass can be claimed", "BLOCKED_NONCLAIM", "false", "false", "prediction and bound are not valid_for_claim"),
        ("CG2701_5_local_GR", "local GR/Newton can be claimed", "BLOCKED_NONCLAIM", "false", "false", "q_loc remains finite residual and unbounded"),
        ("CG2701_6_public", "public/GitHub readiness", "BLOCKED_PRIVATE_WORK", "false", "false", "private derivation/test plumbing only"),
    ]
    return [
        {
            "claim_gate_id": gate_id,
            "gate": gate,
            "status": status,
            "gate_passed": passed,
            "claim_allowed": allowed,
            "reason": reason,
            "timestamp_utc": stamp(),
        }
        for gate_id, gate, status, passed, allowed, reason in rows
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2701_0_PPN", "PPN_KERNEL_REJECTED_FOR_NOW", "current data cannot derive K_PPN without metric response, source frame and q_loc profile", "do not pretend PPN can be scored"),
        ("DEC2701_1_R10", "R10_ALPHA_OPERATOR_WRITTEN", "Yukawa acceleration ratio gives a clean alpha(lambda) response operator for q_loc", "use this as the first executable local-bound projection grammar"),
        ("DEC2701_2_nonclaim", "R10_REMAINS_NONCLAIM", "operator has no profile and bound assets are placeholder/anchor-only", "keep all valid_for_claim=false"),
        ("DEC2701_3_next", "QLOC_PROFILE_OR_FULL_BOUND_CURVE_NEXT", "the next real move is either source a q_loc radial/range profile or digitize the full Eot-Wash curve", "run 2702"),
    ]
    return [
        {
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "next_action": next_action,
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
        for decision_id, decision, rationale, next_action in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2701_0_selected",
            "selection": "selected_primary",
            "target_doc": "2702-Y5-R2FR-q-loc-radial-profile-or-R10-bound-curve-digitization-input.md",
            "target_script": "scripts/Y5_R2FR_q_loc_radial_profile_or_R10_bound_curve_digitization_input_2702.py",
            "task": "try to source or derive the q_loc radial/range profile needed for alpha_q(lambda); if unavailable, stage the full R10 bound-curve digitization input contract without claiming a pass",
            "success_condition": "either q_loc profile/range/source-normalization inputs become source-backed nonclaim rows, or full-bound-curve digitization requirements are made executable with no placeholder scoring",
            "forbidden_shortcuts": "score anchor-only rows; invent q_loc profile; treat symbolic alpha as numeric; claim R10/local GR; GitHub action; formalization-workbench edits",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("STATUS2701_0_q_loc", "q_loc testing", "R10_OPERATOR_EXISTS_NONCLAIM", "q_loc can now be expressed in alpha(lambda) language if a profile exists", "derive/source profile next"),
        ("STATUS2701_1_PPN", "PPN kernel", "HELD_UNTIL_METRIC_RESPONSE", "PPN is too broad until metric response/source frame is signed", "do not score"),
        ("STATUS2701_2_R10", "short-range tests", "OPERATOR_READY_INPUTS_MISSING", "operator is cleaner than PPN but still lacks profile and full bound curve", "2702 profile or bound curve"),
        ("STATUS2701_3_local_GR", "local GR/Newton", "STILL_BLOCKED_BUT_MORE_TESTABLE", "we moved from abstract residual to a concrete local-bound projection grammar", "fill inputs"),
        ("STATUS2701_4_public", "public/GitHub", "NO_ACTION_PRIVATE", "private nonclaim checkpoint only", "keep private"),
    ]
    return [
        {
            "status_id": status_id,
            "topic": topic,
            "status": status,
            "meaning": meaning,
            "next_action": next_action,
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for status_id, topic, status, meaning, next_action in rows
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": "BC2701_0_local_operator",
            "source_csv": str(OUTPUTS["r10_operator"]),
            "branch_csv": str(BRANCH_OUTPUTS["local_r10_operator"]),
            "purpose": "local-bound branch receives R10 q_loc alpha response operator",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2701_1_local_smoke",
            "source_csv": str(OUTPUTS["r10_smoke_rows"]),
            "branch_csv": str(BRANCH_OUTPUTS["local_r10_smoke"]),
            "purpose": "local-bound branch receives nonclaim anchor-aligned smoke rows",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2701_2_wep",
            "source_csv": str(OUTPUTS["r10_operator"]),
            "branch_csv": str(BRANCH_OUTPUTS["wep_r10_operator"]),
            "purpose": "WEP residual branch receives q_loc alpha operator grammar",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2701_3_source_weight",
            "source_csv": str(OUTPUTS["r10_operator"]),
            "branch_csv": str(BRANCH_OUTPUTS["source_weight_r10_operator"]),
            "purpose": "source-weight branch receives q_loc alpha/source-normalization operator grammar",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2701_4_rab_next",
            "source_csv": str(OUTPUTS["next_target"]),
            "branch_csv": str(BRANCH_OUTPUTS["rab_next"]),
            "purpose": "RAB queue receives q_loc profile or R10 bound-curve input next target",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = rows_by_name["source_register"]
    all_sources_exist = all(row["exists"] == "true" for row in source_rows)
    all_needles_found = all(row["missing_needles"] == "" for row in source_rows)

    parse_targets = {key: path for key, path in OUTPUTS.items() if key != "validation"}
    parse_targets.update(BRANCH_OUTPUTS)
    parse_results = {key: parse_csv(path) for key, path in parse_targets.items()}
    all_csv_parse = all(ok and count > 0 for ok, count, _ in parse_results.values())

    ppn = rows_by_name["ppn_kernel_audit"]
    operator_rows = rows_by_name["r10_operator"]
    smoke_rows = rows_by_name["r10_smoke_rows"]
    missing_rows = rows_by_name["missing_inputs"]
    assets = rows_by_name["bound_asset_status"]
    claim_gates = rows_by_name["claim_gates"]
    next_targets = rows_by_name["next_target"]

    ppn_rejected = any(row["audit_id"] == "PPN2701_4_verdict" and row["status"] == "PPN_KERNEL_REJECTED_FOR_NOW" for row in ppn)
    r10_operator_present = any(
        row["operator_id"] == "R10OP2701_0_QLOC_YUKAWA_ALPHA_RESPONSE"
        and "alpha_q(lambda" in row["response_formula"]
        and row["output_units"] == "dimensionless alpha(lambda)"
        and row["valid_for_claim"] == "false"
        for row in operator_rows
    )
    smoke_nonclaim = all(row["valid_for_claim"] == "false" and row["score_ready"] == "false" for row in smoke_rows)
    missing_inputs_recorded = len(missing_rows) >= 6 and all(row["valid_for_claim"] == "false" for row in missing_rows)
    bound_assets_nonclaim = all(row["valid_for_claim"] == "false" for row in assets)
    no_claims = all(row["claim_allowed"] == "false" for row in claim_gates)
    next_2702 = any(row["next_id"] == "NEXT2701_0_selected" and "2702-" in row["target_doc"] for row in next_targets)
    no_formalization_outputs = all("formalization-workbench" not in str(path).lower() for path in parse_targets.values())
    no_github_outputs = all(".git" not in str(path).lower() and "github" not in path.name.lower() for path in parse_targets.values())

    checks = [
        ("VAL2701_0_sources_exist", all_sources_exist, "all cited source paths exist"),
        ("VAL2701_1_needles_found", all_needles_found, "all required source needles were found"),
        ("VAL2701_2_csv_parse", all_csv_parse, "all generated CSVs and branch copies parse with at least one row"),
        ("VAL2701_3_ppn_rejected", ppn_rejected, "PPN kernel derivation is explicitly rejected for current inputs"),
        ("VAL2701_4_r10_operator_present", r10_operator_present, "R10 alpha(lambda) response operator exists with units and nonclaim status"),
        ("VAL2701_5_smoke_nonclaim", smoke_nonclaim, "anchor-aligned smoke rows remain nonclaim and nonscoreable"),
        ("VAL2701_6_missing_inputs_recorded", missing_inputs_recorded, "q_loc profile/source/bound inputs are explicit"),
        ("VAL2701_7_bound_assets_nonclaim", bound_assets_nonclaim, "bound assets remain nonclaim"),
        ("VAL2701_8_no_claims", no_claims, "all claim gates keep claim_allowed=false"),
        ("VAL2701_9_next_2702", next_2702, "2702 q_loc profile or bound-curve target selected"),
        ("VAL2701_10_no_formalization_outputs", no_formalization_outputs, "no output path points into formalization-workbench"),
        ("VAL2701_11_no_github_outputs", no_github_outputs, "no GitHub/public-output path was written"),
    ]

    rows: list[dict[str, Any]] = []
    for check_id, passed, detail in checks:
        rows.append(
            {
                "check_id": check_id,
                "passed": as_bool(passed),
                "detail": detail,
                "timestamp_utc": stamp(),
            }
        )
    for key, (ok, count, message) in parse_results.items():
        rows.append(
            {
                "check_id": f"VAL2701_PARSE_{key}",
                "passed": as_bool(ok and count > 0),
                "detail": f"{message}; rows={count}",
                "timestamp_utc": stamp(),
            }
        )
    overall = all(row["passed"] == "true" for row in rows)
    rows.append(
        {
            "check_id": "VAL2701_OVERALL",
            "passed": as_bool(overall),
            "detail": "2701 rejects the underdetermined q_loc-to-PPN kernel, writes the R10 Yukawa alpha(lambda) response operator, keeps smoke rows nonclaim, and selects q_loc profile or full bound-curve input next",
            "timestamp_utc": stamp(),
        }
    )
    return rows


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    verdict = (
        "2701 does the useful testing move. The PPN kernel is too underdetermined because the metric response, source frame, "
        "and q_loc profile are all missing. The R10 route is cleaner: compare the q_loc radial acceleration to the Yukawa "
        "acceleration ratio alpha(1+r/lambda)exp(-r/lambda). This creates a real alpha(lambda) operator, but it remains "
        "strictly nonclaim until q_loc(r,lambda), source normalization, and a full alpha-bound curve exist."
    )
    text = f"""# 2701: q_loc PPN Kernel Or R10 alpha(lambda) Response Operator Fill

**Branch:** `{BRANCH_ID}`

## Private Verdict

{verdict}

## PPN Kernel Audit

{markdown_table(rows_by_name["ppn_kernel_audit"])}

## R10 alpha(lambda) Response Operator

{markdown_table(rows_by_name["r10_operator"])}

## R10 Smoke Rows

{markdown_table(rows_by_name["r10_smoke_rows"])}

## Missing Inputs

{markdown_table(rows_by_name["missing_inputs"])}

## Bound Asset Status

{markdown_table(rows_by_name["bound_asset_status"])}

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Claim Gates

{markdown_table(rows_by_name["claim_gates"])}

## Decisions

{markdown_table(rows_by_name["decision_ledger"])}

## Next Target

{markdown_table(rows_by_name["next_target"])}

## Project Status

{markdown_table(rows_by_name["project_status"])}

## Validation

{markdown_table(rows_by_name["validation"])}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    ppn_rows = ppn_kernel_audit_rows()
    operator_rows = r10_operator_rows()
    smoke_rows = r10_smoke_rows()
    missing_rows = missing_input_rows()
    bound_rows = bound_asset_status_rows()
    claim_rows = claim_gate_rows()
    decision_rows = decision_ledger_rows()
    next_rows = next_target_rows()
    status_rows = project_status_rows()
    branch_rows = branch_copy_rows()

    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_rows,
        "ppn_kernel_audit": ppn_rows,
        "r10_operator": operator_rows,
        "r10_smoke_rows": smoke_rows,
        "missing_inputs": missing_rows,
        "bound_asset_status": bound_rows,
        "claim_gates": claim_rows,
        "decision_ledger": decision_rows,
        "next_target": next_rows,
        "project_status": status_rows,
        "branch_copies": branch_rows,
    }

    for key, rows in rows_by_name.items():
        write_csv(OUTPUTS[key], rows)

    write_csv(BRANCH_OUTPUTS["local_r10_operator"], operator_rows)
    write_csv(BRANCH_OUTPUTS["local_r10_smoke"], smoke_rows)
    write_csv(BRANCH_OUTPUTS["wep_r10_operator"], operator_rows)
    write_csv(BRANCH_OUTPUTS["source_weight_r10_operator"], operator_rows)
    write_csv(BRANCH_OUTPUTS["rab_next"], next_rows)

    validation = validation_rows(rows_by_name)
    rows_by_name["validation"] = validation
    write_csv(OUTPUTS["validation"], validation)
    write_doc(rows_by_name)

    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

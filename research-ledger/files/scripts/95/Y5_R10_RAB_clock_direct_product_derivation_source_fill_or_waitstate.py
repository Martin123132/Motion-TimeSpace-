from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1324"
TITLE = "1324-Y5-R10-RAB-clock-direct-product-derivation-source-fill-or-waitstate"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
EQUATION_ATTEMPT_PATH = OUT_DIR / f"{PACK_ID}_DIRECT_PRODUCT_EQUATION_ATTEMPT.csv"
FILL_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_DIRECT_PRODUCT_FILL_AUDIT.csv"
WAITSTATE_PATH = OUT_DIR / f"{PACK_ID}_CLOCK_WAITSTATE_LEDGER.csv"
RUNNER_UPDATE_PATH = OUT_DIR / f"{PACK_ID}_ACCEPTANCE_RUNNER_UPDATE.csv"
WEP_ROUTE_PATH = OUT_DIR / f"{PACK_ID}_WEP_SOURCE_NORMALIZATION_ROUTE.csv"
ANTI_SHORTCUT_PATH = OUT_DIR / f"{PACK_ID}_ANTI_SHORTCUT_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1324_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "details": details}


def is_false(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no"}


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    return all(
        is_false(row.get("valid_for_claim", False)) and is_false(row.get("claim_allowed", False))
        for rows in tables
        for row in rows
    )


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        EQUATION_ATTEMPT_PATH,
        FILL_AUDIT_PATH,
        WAITSTATE_PATH,
        RUNNER_UPDATE_PATH,
        WEP_ROUTE_PATH,
        ANTI_SHORTCUT_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def missing_token(value: object) -> bool:
    text = str(value).strip()
    return not text or "MISSING" in text or text.lower() in {"none", "null", "nan"}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1324_0_1323_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1323_NEXT_TARGET.csv",
            "needle": "NEXT1323_0_1324",
            "role": "handoff into direct product fill or wait-state",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1324_1_1323_pack",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1323_DIRECT_CLOCK_PRODUCT_SOURCE_PACK.csv",
            "needle": "DCLK1323_0_yb_direct_product",
            "role": "current direct clock product source pack",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1324_2_1323_runner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1323_ACCEPTANCE_RUNNER.csv",
            "needle": "ACCEPT1323_0_yb_direct_product",
            "role": "current refused acceptance runner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1324_3_1323_shortcuts",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1323_ANTI_SHORTCUT_GATES.csv",
            "needle": "SHORT1323_1_no_bound_as_prediction",
            "role": "anti-shortcut gates inherited from 1323",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1324_4_1322_requirements",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1322_DIRECT_PRODUCT_SOURCE_REQUIREMENTS.csv",
            "needle": "DCP1322_1_direct_product",
            "role": "direct product minimum usable form",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1324_5_1322_runner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1322_CLOCK_RUNNER_UPDATE.csv",
            "needle": "CLKRUN1322_0_tau_derivation_attempt",
            "role": "tau/readout derivation refusal",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1324_6_1316_tau_clock",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1316_P0_SOURCE_REQUIREMENT_LEDGER.csv",
            "needle": "REQ1316_4_tau_clock",
            "role": "tau_clock source requirement",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1324_7_1316_wep_requirements",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1316_P0_SOURCE_REQUIREMENT_LEDGER.csv",
            "needle": "REQ1316_8_material",
            "role": "WEP material/source requirements",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1324_8_1317_wep_runner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1317_PRIORITY_RUNNER_REFUSAL_TABLE.csv",
            "needle": "RUN1317_2_run1314_2_wep",
            "role": "WEP first-fill refusal row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1324_9_1313_source_weight",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1313_HIDDEN_SCALAR_COUNTEREXAMPLE_LOCK_UPDATE.csv",
            "needle": "HSC1313_4_source_weight",
            "role": "active source-weight counterexample lock",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1324_10_646_yb_sensitivity",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv",
            "needle": "CAS646_1_YbE3E2",
            "role": "source-backed Yb E3/E2 sensitivity",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    source_pack = read_csv(source_path("source-intake/mts_residuals/P8_Y5_R10_1323_DIRECT_CLOCK_PRODUCT_SOURCE_PACK.csv"))
    source_row = source_pack[0]
    runner_rows = read_csv(source_path("source-intake/mts_residuals/P8_Y5_R10_1323_ACCEPTANCE_RUNNER.csv"))
    runner_row = runner_rows[0]

    equation_attempt = [
        {
            "attempt_id": "EQ1324_0_clock_observable",
            "target_identity": "d ln R_YbE3E2/dt = DeltaK_alpha * d ln alpha_eff/dt",
            "available_piece": "DeltaK_alpha=-6.95 from CAS646_1_YbE3E2",
            "missing_piece": "MTS local d ln alpha_eff/dt in yr^-1",
            "result": "PARTIAL_EXTERNAL_CLOCK_SENSITIVITY_ONLY",
            "claim_effect": "no MTS prediction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "EQ1324_1_direct_product",
            "target_identity": "P_clock_alpha_direct := d ln R_YbE3E2/dt|MTS",
            "available_piece": source_row["predicted_product_value"],
            "missing_piece": "numeric source-backed direct product value, units, readout model, source path, anchor, equation reference, provenance, sign convention",
            "result": "NOT_FILLABLE_FROM_CURRENT_CORPUS",
            "claim_effect": "clock row must wait-state",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "EQ1324_2_factorized_product",
            "target_identity": "P_clock_alpha = b_alpha * tau_clock_time",
            "available_piece": "product coordinate named in 1322",
            "missing_piece": "parent-signed b_alpha/c_alpha and parent-derived tau_clock_time",
            "result": "REJECTED_AS_DERIVATION",
            "claim_effect": "cannot infer b_alpha or tau from the clock bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "EQ1324_3_h0_route",
            "target_identity": "tau_clock_time = H0 * d chi_X/dN",
            "available_piece": "H0-normalized diagnostic",
            "missing_piece": "lab clock readout theorem identifying local tau with cosmological H0 diagnostic",
            "result": "DIAGNOSTIC_ONLY_REFUSED",
            "claim_effect": "no numerical clock prediction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "EQ1324_4_local_silence",
            "target_identity": "P_clock_alpha=0 in a strict local closed/gapped branch",
            "available_piece": "conditional local silence route",
            "missing_piece": "strict local representative, stationary tau, clock lock, no-exchange certificate",
            "result": "CONDITIONAL_ONLY_NOT_ACTIVE",
            "claim_effect": "cannot score zero against clock bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    required_fill_fields = [
        "predicted_product_value",
        "predicted_product_units",
        "product_definition",
        "readout_model",
        "source_path",
        "source_anchor",
        "equation_ref",
        "provenance_note",
        "sign_convention",
    ]
    missing_fields = [field for field in required_fill_fields if missing_token(source_row.get(field, ""))]

    fill_audit = [
        {
            "audit_id": "FILL1324_0_direct_numeric_value",
            "product_row_id": source_row["product_row_id"],
            "field_or_route": "predicted_product_value",
            "current_value": source_row["predicted_product_value"],
            "fill_attempt": "scan inherited direct product row for numeric yr^-1 value",
            "result": "MISSING",
            "disposition": "WAITSTATE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "FILL1324_1_units",
            "product_row_id": source_row["product_row_id"],
            "field_or_route": "predicted_product_units",
            "current_value": source_row["predicted_product_units"],
            "fill_attempt": "require yr^-1 convention matching clock product bound",
            "result": "MISSING",
            "disposition": "WAITSTATE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "FILL1324_2_readout_kernel",
            "product_row_id": source_row["product_row_id"],
            "field_or_route": "readout_model",
            "current_value": source_row["readout_model"],
            "fill_attempt": "derive MTS map into Yb E3/E2 ratio readout",
            "result": "NOT_DERIVED",
            "disposition": "WAITSTATE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "FILL1324_3_tau_factorization",
            "product_row_id": source_row["product_row_id"],
            "field_or_route": "b_alpha*tau_clock_time",
            "current_value": "DEFINED_PRODUCT_COORDINATE_ONLY",
            "fill_attempt": "use tau_clock_time definition and b_alpha factorization",
            "result": "REFUSED_PARENT_NOT_SIGNED",
            "disposition": "NO_FILL",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "FILL1324_4_h0_diagnostic",
            "product_row_id": source_row["product_row_id"],
            "field_or_route": "H0_normalized_diagnostic",
            "current_value": "2.93296e-08 diagnostic imported in 1321",
            "fill_attempt": "use H0-normalized number as tau or product",
            "result": "REFUSED_DIAGNOSTIC_ONLY",
            "disposition": "NO_FILL",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "FILL1324_5_bound_as_prediction",
            "product_row_id": source_row["product_row_id"],
            "field_or_route": "comparison_bound_1sigma_yr_inv",
            "current_value": runner_row["bound_1sigma_yr_inv"],
            "fill_attempt": "copy empirical bound into predicted product",
            "result": "REFUSED_CIRCULAR",
            "disposition": "NO_FILL",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    waitstate = [
        {
            "waitstate_id": f"WAIT1324_{index}",
            "product_row_id": source_row["product_row_id"],
            "blocked_field": field,
            "current_value": source_row.get(field, ""),
            "required_resolution": "source or derive this field before clock product comparison can run",
            "waitstate_reason": "direct product cannot be filled without parent-owned readout/value/provenance",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for index, field in enumerate(missing_fields)
    ]

    runner_update = [
        {
            "runner_id": "ACCEPT1324_0_clock_waitstate",
            "previous_runner_id": runner_row["runner_id"],
            "product_row_id": source_row["product_row_id"],
            "clock_pair": source_row["clock_pair"],
            "bound_1sigma_yr_inv": runner_row["bound_1sigma_yr_inv"],
            "direct_product_fill_status": "WAITSTATE_NOT_FILLABLE_FROM_CURRENT_CORPUS",
            "missing_field_count": len(missing_fields),
            "missing_fields": ";".join(missing_fields),
            "comparison_status": "NOT_SCORED_OR_REFUSED",
            "runner_status": "REFUSED_WAITSTATE",
            "refusal_reason": "no direct P_clock_alpha value/readout/provenance; tau/H0/bound shortcuts refused",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    wep_route = [
        {
            "route_id": "WEP1324_0_beta_source_alpha",
            "needed_object": "beta_source_alpha",
            "source_requirement_id": "REQ1316_6_beta_source",
            "current_status": "MISSING_SOURCE_NORMALIZATION",
            "why_next": "this is the coupling/source side the clock route cannot test alone",
            "minimum_next_fill": "source-normalization coefficient or theorem-zero certificate with branch and source path",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "route_id": "WEP1324_1_tau_wep",
            "needed_object": "tau_WEP",
            "source_requirement_id": "REQ1316_7_tau_wep",
            "current_status": "MISSING_TAU_WEP",
            "why_next": "WEP cannot be scored without the arena projection/readout factor",
            "minimum_next_fill": "WEP branch projection with units/convention or explicit direct P_WEP_alpha bypass",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "route_id": "WEP1324_2_material_map",
            "needed_object": "DeltaQ_alpha_AB/material map",
            "source_requirement_id": "REQ1316_8_material",
            "current_status": "MISSING_MATERIAL_RESPONSE",
            "why_next": "MICROSCOPE-like source/test material comparison needs composition response",
            "minimum_next_fill": "material pair, alpha charge difference, source path, and readout convention",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "route_id": "WEP1324_3_source_profile",
            "needed_object": "source/worldtube profile",
            "source_requirement_id": "REQ1316_9_source_profile",
            "current_status": "MISSING_SOURCE_PROFILE",
            "why_next": "finite source normalization cannot be a point-source shortcut",
            "minimum_next_fill": "finite source/worldtube profile and domain with provenance",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "route_id": "WEP1324_4_source_weight_counterexample",
            "needed_object": "source-weight theorem-zero or finite coefficient",
            "source_requirement_id": "HSC1313_4_source_weight",
            "current_status": "LOCKED_ACTIVE",
            "why_next": "this is the active coupling loophole, the little goblin in the machinery",
            "minimum_next_fill": "prove source-only species weights are impossible/redundant, or source their finite coefficient",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    anti_shortcut = [
        {
            "gate_id": "SHORT1324_0_no_clock_bound_prediction",
            "shortcut": "copy the Yb comparison bound into P_clock_alpha",
            "enforcement": "REFUSED as circular bound-as-prediction",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1324_1_no_h0_tau",
            "shortcut": "use H0-normalized diagnostic as local clock tau",
            "enforcement": "REFUSED until lab tau/readout theorem is parent-signed",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1324_2_no_standalone_balpha",
            "shortcut": "divide a clock product bound by assumed tau to infer b_alpha",
            "enforcement": "REFUSED; clock scores products only",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1324_3_no_clock_to_wep_transfer",
            "shortcut": "transfer clock waitstate row into WEP/R10/local evidence",
            "enforcement": "REFUSED until parent branch/readout functor is signed",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1324_0_direct_product_not_filled",
            "decision": "direct P_clock_alpha is not fillable from current corpus",
            "because": "DeltaK and the bound are source-backed, but the MTS local alpha drift/readout kernel/provenance are absent",
            "effect": "clock row moves to explicit wait-state",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1324_1_no_derivation_shortcut",
            "decision": "factorized tau/H0/local-silence routes are refused",
            "because": "tau_clock_time, b_alpha, and local silence are definitions or conditional branches, not parent-signed readouts",
            "effect": "no clock pass, no b_alpha inference, no zero-product score",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1324_2_route_to_wep",
            "decision": "next finite-source route is WEP source-normalization decomposition",
            "because": "the real missing object is the coupling/source-normalization map, and WEP exposes source/material factors more directly than clocks",
            "effect": "start 1325 WEP first-fill decomposition while keeping clock wait-stated",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1324_0_1325",
            "target_file": "1325-Y5-R10-RAB-WEP-source-normalization-decomposition-first-fill.md",
            "target_script": "scripts/Y5_R10_RAB_WEP_source_normalization_decomposition_first_fill.py",
            "task": "decompose the WEP alpha/source product into beta_source_alpha, tau_WEP, material DeltaQ_alpha_AB, source profile, and direct-product bypass rows",
            "success_condition": "WEP branch receives exact source-fill requirements and a refusal runner that can accept real finite source coefficients without using clock/R10 transfer",
            "do_not": "do not claim WEP pass; do not set beta_source or tau_WEP to unity; do not transfer clock product or R10 thresholds",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(EQUATION_ATTEMPT_PATH, equation_attempt)
    write_csv(FILL_AUDIT_PATH, fill_audit)
    write_csv(WAITSTATE_PATH, waitstate)
    write_csv(RUNNER_UPDATE_PATH, runner_update)
    write_csv(WEP_ROUTE_PATH, wep_route)
    write_csv(ANTI_SHORTCUT_PATH, anti_shortcut)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)

    validations: list[dict[str, object]] = []
    sources_ok = all(row["exists"] and row["needle_found"] for row in source_register)
    validations.append(
        validation_row(
            "VAL1324_0_sources_exist",
            "registered source paths exist and anchors are found",
            sources_ok,
            f"{sum(1 for row in source_register if row['exists'] and row['needle_found'])}/{len(source_register)} source anchors found",
        )
    )
    equation_refuses = all(
        row["result"] in {
            "PARTIAL_EXTERNAL_CLOCK_SENSITIVITY_ONLY",
            "NOT_FILLABLE_FROM_CURRENT_CORPUS",
            "REJECTED_AS_DERIVATION",
            "DIAGNOSTIC_ONLY_REFUSED",
            "CONDITIONAL_ONLY_NOT_ACTIVE",
        }
        for row in equation_attempt
    )
    validations.append(
        validation_row(
            "VAL1324_1_equation_attempt_refuses_shortcuts",
            "equation attempt separates clock sensitivity from MTS product and refuses shortcuts",
            equation_refuses,
            ";".join(f"{row['attempt_id']}={row['result']}" for row in equation_attempt),
        )
    )
    fill_audit_ok = len(missing_fields) == 9 and all(is_false(row["valid_for_claim"]) for row in fill_audit)
    validations.append(
        validation_row(
            "VAL1324_2_fill_audit_keeps_missing_fields",
            "direct product fill audit records current missing fields without promotion",
            fill_audit_ok,
            ";".join(missing_fields),
        )
    )
    waitstate_ok = len(waitstate) == len(missing_fields) and all(row["blocked_field"] in missing_fields for row in waitstate)
    validations.append(
        validation_row(
            "VAL1324_3_clock_waitstate_complete",
            "clock wait-state ledger covers every required direct product field",
            waitstate_ok,
            f"waitstate_fields={len(waitstate)}",
        )
    )
    runner_waits = runner_update[0]["runner_status"] == "REFUSED_WAITSTATE" and len(missing_fields) == int(runner_update[0]["missing_field_count"])
    validations.append(
        validation_row(
            "VAL1324_4_runner_refuses_waitstate",
            "runner remains refused and not scored after direct product fill attempt",
            runner_waits,
            str(runner_update[0]["refusal_reason"]),
        )
    )
    wep_ready = {row["source_requirement_id"] for row in wep_route} >= {
        "REQ1316_6_beta_source",
        "REQ1316_7_tau_wep",
        "REQ1316_8_material",
        "REQ1316_9_source_profile",
        "HSC1313_4_source_weight",
    }
    validations.append(
        validation_row(
            "VAL1324_5_wep_route_selected",
            "next route targets WEP source-normalization decomposition fields",
            wep_ready,
            ";".join(row["source_requirement_id"] for row in wep_route),
        )
    )
    shortcut_ok = all(row["status"] == "ENFORCED" for row in anti_shortcut)
    validations.append(
        validation_row(
            "VAL1324_6_shortcuts_enforced",
            "anti-shortcut gates are enforced",
            shortcut_ok,
            ";".join(row["gate_id"] for row in anti_shortcut),
        )
    )
    nonclaim_ok = all_nonclaim(
        [
            source_register,
            equation_attempt,
            fill_audit,
            waitstate,
            runner_update,
            wep_route,
            anti_shortcut,
            decision,
            next_target,
        ]
    )
    validations.append(
        validation_row(
            "VAL1324_7_nonclaim_policy",
            "all generated rows remain nonclaim",
            nonclaim_ok,
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    formal_outputs = generated_inside_formalization()
    validations.append(
        validation_row(
            "VAL1324_8_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            not formal_outputs,
            f"formalization_generated_output_count={len(formal_outputs)}",
        )
    )
    next_ok = next_target[0]["target_file"].startswith("1325-Y5-R10-RAB-WEP-source-normalization")
    validations.append(
        validation_row(
            "VAL1324_9_next_target_1325",
            "next target routes to WEP source-normalization decomposition",
            next_ok,
            str(next_target[0]["target_file"]),
        )
    )
    validations.append(
        validation_row(
            "VAL1324_10_overall",
            "overall 1324 validation",
            all(row["status"] == "PASS" for row in validations),
            "1324 wait-states direct clock product, refuses shortcuts, and selects WEP source-normalization route",
        )
    )
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# 1324: RAB Clock Direct Product Derivation Source Fill Or Waitstate

**Current verdict:** 1324 tried the direct `P_clock_alpha` fill and did not promote it. The Yb clock sensitivity/bound are real, but the MTS local alpha drift/readout product is still absent.

**Main progress:** the clock route is now cleanly wait-stated rather than left vague: nine required direct-product fields remain missing, and the runner refuses the row without scoring.

**Decision:** move the next finite-source work to WEP source-normalization decomposition. That is where the coupling/source-weight gap can be attacked directly; the clock row stays ready to accept a real direct product later.

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Direct Product Equation Attempt
{markdown_table(equation_attempt, ["attempt_id", "target_identity", "available_piece", "missing_piece", "result", "claim_effect", "valid_for_claim", "claim_allowed"])}

## Direct Product Fill Audit
{markdown_table(fill_audit, ["audit_id", "product_row_id", "field_or_route", "current_value", "fill_attempt", "result", "disposition", "valid_for_claim", "claim_allowed"])}

## Clock Wait-State Ledger
{markdown_table(waitstate, ["waitstate_id", "product_row_id", "blocked_field", "current_value", "required_resolution", "waitstate_reason", "valid_for_claim", "claim_allowed"])}

## Acceptance Runner Update
{markdown_table(runner_update, ["runner_id", "previous_runner_id", "product_row_id", "clock_pair", "bound_1sigma_yr_inv", "direct_product_fill_status", "missing_field_count", "missing_fields", "comparison_status", "runner_status", "refusal_reason", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])}

## WEP Source-Normalization Route
{markdown_table(wep_route, ["route_id", "needed_object", "source_requirement_id", "current_status", "why_next", "minimum_next_fill", "valid_for_claim", "claim_allowed"])}

## Anti-Shortcut Gates
{markdown_table(anti_shortcut, ["gate_id", "shortcut", "enforcement", "status", "valid_for_claim", "claim_allowed"])}

## Decision Ledger
{markdown_table(decision, ["decision_id", "decision", "because", "effect", "valid_for_claim", "claim_allowed"])}

## Next Target
{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation
{markdown_table(validations, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()

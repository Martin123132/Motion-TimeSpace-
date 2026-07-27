from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1281"
TITLE = "1281-Y5-R10-RAB-Gamma-Khat-metric-response-symbol-match-or-q_loc-profile-template"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
RAB_INTAKE_DIR = ROOT / "source-intake" / "rab-sector"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
SYMBOL_MATCH_PATH = OUT_DIR / f"{PACK_ID}_GAMMA_KHAT_SYMBOL_MATCH_AUDIT.csv"
TENSOR_CONTRACT_PATH = OUT_DIR / f"{PACK_ID}_METRIC_RESPONSE_TENSOR_CONTRACT.csv"
PROFILE_TEMPLATE_PATH = OUT_DIR / f"{PACK_ID}_EPSILON_GK_QLOC_PROFILE_TEMPLATE_NONCLAIM.csv"
PROFILE_RULES_PATH = OUT_DIR / f"{PACK_ID}_PROFILE_INTAKE_RULES.csv"
VALIDATOR_RESCAN_PATH = OUT_DIR / f"{PACK_ID}_ZR_VALIDATOR_RESCAN.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1281_VALIDATION.csv"


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
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
    }


def is_false(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no"}


def contains_missing_marker(row: dict[str, object]) -> bool:
    return any("MISSING_" in str(value) for value in row.values())


def validate_intake_row(path: Path, intake_class: str, row: dict[str, str]) -> dict[str, object]:
    row_id = row.get("row_id") or row.get("template_id") or row.get("coefficient_symbol") or "MISSING_ROW_ID"
    required_columns = [
        "coefficient_symbol",
        "coefficient_value",
        "coefficient_units",
        "normalization_convention",
        "parent_action_block",
        "source_path",
        "source_anchor",
        "arena_projection",
        "valid_for_claim",
        "claim_allowed",
    ]
    missing_columns = [column for column in required_columns if column not in row]
    source_raw = str(row.get("source_path", "")).strip()
    anchor = str(row.get("source_anchor", "")).strip()
    source = None if not source_raw or source_raw.startswith("MISSING_") else source_path(source_raw)
    source_exists = bool(source and source.exists())
    anchor_found = bool(source_exists and anchor and not anchor.startswith("MISSING_") and anchor in read_text(source))
    reasons: list[str] = []
    if intake_class == "docs":
        reasons.append("DOCS_TEMPLATE_NOT_LIVE_INTAKE")
    if missing_columns:
        reasons.append("MISSING_REQUIRED_COLUMNS:" + ";".join(missing_columns))
    if contains_missing_marker(row):
        reasons.append("MISSING_MARKER_PRESENT")
    if source is None:
        reasons.append("SOURCE_PATH_MISSING_OR_PLACEHOLDER")
    elif not source_exists:
        reasons.append("SOURCE_PATH_NOT_FOUND")
    if not anchor or anchor.startswith("MISSING_"):
        reasons.append("SOURCE_ANCHOR_MISSING_OR_PLACEHOLDER")
    elif source_exists and not anchor_found:
        reasons.append("SOURCE_ANCHOR_NOT_FOUND")
    if str(row.get("valid_for_claim", "")).strip().lower() == "true" or str(row.get("claim_allowed", "")).strip().lower() == "true":
        reasons.append("CLAIM_FLAG_TRUE_REJECTED_IN_PRIVATE_NONCLAIM_PHASE")
    return {
        "scan_id": f"SCAN1281_{intake_class}_{path.stem}_{row_id}",
        "intake_class": intake_class,
        "file_path": str(path),
        "row_id": row_id,
        "coefficient_symbol": row.get("coefficient_symbol", ""),
        "status": "REJECT" if reasons else "ACCEPT_NONCLAIM_SOURCE_READY",
        "reasons": "|".join(reasons) if reasons else "NO_PLACEHOLDERS_SOURCE_ANCHOR_FOUND_NONCLAIM",
        "source_exists": source_exists,
        "anchor_found": anchor_found,
        "intake_eligible": not reasons,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def scan_rab_intake() -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for intake_class in ["docs", "raw", "accepted"]:
        directory = RAB_INTAKE_DIR / intake_class
        directory.mkdir(parents=True, exist_ok=True)
        for path in sorted(directory.glob("*.csv")):
            for row in read_csv(path):
                results.append(validate_intake_row(path, intake_class, row))
    return results


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        SYMBOL_MATCH_PATH,
        TENSOR_CONTRACT_PATH,
        PROFILE_TEMPLATE_PATH,
        PROFILE_RULES_PATH,
        VALIDATOR_RESCAN_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1281_0_1280_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1280_NEXT_TARGET.csv",
            "needle": "NEXT1280_0_1281",
            "purpose": "handoff into Gamma/Khat symbol-match or q_loc profile template",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1281_1_1280_metric",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1280_METRIC_RESPONSE_SYMBOL_MATCH_AUDIT.csv",
            "needle": "MRM1280_3_verdict",
            "purpose": "metric-response route not matched in 1280",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1281_2_1280_bound",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1280_EPSILON_GK_QLOC_BOUND_CONTRACT.csv",
            "needle": "BND1280_0_definition",
            "purpose": "epsilon_GK_q_loc bound contract from 1280",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1281_3_contract",
            "local_path": "source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_CONTRACT.csv",
            "needle": "MR514_1_Khat_metric_response",
            "purpose": "metric-response pass condition",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1281_4_evidence",
            "local_path": "source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_SOURCE_EVIDENCE.csv",
            "needle": "E515_5_current_contract",
            "purpose": "evidence says contract defines pass condition but does not match symbols",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1281_5_gate_tests",
            "local_path": "source-intake/mts_residuals/P8_GK_STRESS_ACTION_GATE_TESTS.csv",
            "needle": "G514_2_current_MTS_match",
            "purpose": "current MTS match fails",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1281_6_response_contract",
            "local_path": "source-intake/mts_residuals/P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv",
            "needle": "RD516_2_metric_response",
            "purpose": "response doublet metric-response route remains unchecked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1281_7_1010_schema",
            "local_path": "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
            "needle": "HGS1010_4_residual_retention",
            "purpose": "q_loc residual retention schema",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1281_8_1279_vector",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1279_EXTRA_SECTOR_RESIDUAL_VECTOR.csv",
            "needle": "XRV1279_2_GK_q_loc",
            "purpose": "q_loc residual vector row retained",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1281_9_validator",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1269_ZR_INTAKE_VALIDATOR_SUMMARY.csv",
            "needle": "NO_ACCEPTED_SOURCE_READY_ROWS",
            "purpose": "finite residual source rows remain absent",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    symbol_match = [
        {
            "match_id": "GKM1281_0_Gamma_formula",
            "symbol": "Gamma_eff",
            "required_for_match": "explicit covariant scalar-density formula, units, parent fields, no data-fit selector",
            "current_evidence": "symbol exists but is not action-placed",
            "status": "MISSING_FORMULA",
            "next_input": "Gamma_eff_formula; Gamma_eff_units; parent_field_list; source_path",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "match_id": "GKM1281_1_Khat_formula",
            "symbol": "K_hat^{mu nu}",
            "required_for_match": "explicit tensor formula and derivative/boundary accounting",
            "current_evidence": "current MTS match fails in G514_2",
            "status": "MISSING_TENSOR_MATCH",
            "next_input": "K_hat_formula; tensor_index_convention; boundary_terms; source_path",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "match_id": "GKM1281_2_metric_variation",
            "symbol": "K_metric^{mu nu}",
            "required_for_match": "compute 2/sqrt(-g)delta[sqrt(-g)Gamma_eff]/delta g_mu_nu under fixed sign convention",
            "current_evidence": "contract exists but no concrete computation exists",
            "status": "MISSING_VARIATION_COMPUTATION",
            "next_input": "K_metric_formula; sign_convention; volume_term_convention; derivative_term_accounting",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "match_id": "GKM1281_3_difference_test",
            "symbol": "Delta_K^{mu nu}=K_hat^{mu nu}-K_metric^{mu nu}",
            "required_for_match": "prove Delta_K=0 or exact/topological/boundary-silent",
            "current_evidence": "not available",
            "status": "MISSING_DIFFERENCE_LEDGER",
            "next_input": "tensor_component_comparison; residual_terms; exact_term_certificate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "match_id": "GKM1281_4_verdict",
            "symbol": "Gamma_eff/K_hat metric-response identity",
            "required_for_match": "GKM1281_0..3 pass with source paths",
            "current_evidence": "missing formula/tensor/variation/difference inputs",
            "status": "SYMBOL_MATCH_NOT_CLOSED",
            "next_input": "use profile template or derive response-doublet component map",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    tensor_contract = [
        {
            "contract_id": "MRT1281_0_candidate_identity",
            "identity": "K_hat^{mu nu} ?= K_metric^{mu nu}",
            "definition": "K_metric^{mu nu}:=2/sqrt(-g) delta[sqrt(-g)Gamma_eff]/delta g_mu_nu minus declared volume/sign convention",
            "pass_condition": "Delta_K^{mu nu}=0 up to declared exact/topological/boundary-silent terms",
            "current_status": "UNEXECUTED_NO_FORMULAS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "MRT1281_1_Ward_consequence",
            "identity": "nabla_mu(Gamma_eff g^{mu nu}-K_hat^{mu nu}) is a parent Ward/Euler residual",
            "definition": "requires action existence, metric response, and field Euler equations",
            "pass_condition": "q_loc equals on-shell Ward residual and vanishes when E_A=0 plus boundary=0",
            "current_status": "BLOCKED_BY_METRIC_RESPONSE_AND_EULER",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "MRT1281_2_double_zero_consequence",
            "identity": "F_1=partial_A T_GK(Phi0)=0",
            "definition": "requires response-doublet or parent symmetry forbidding linear local source terms",
            "pass_condition": "linear PPN/source-normalization leakage vanishes",
            "current_status": "CONDITIONAL_NOT_COMPONENT_DERIVED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    profile_template = [
        {
            "template_id": "GKQ1281_TEMPLATE_DO_NOT_SCORE",
            "residual_component": "epsilon_GK_q_loc",
            "branch_id": "finite_residual_profile_template",
            "q_loc_profile_formula": "MISSING_Q_LOC_PROFILE_FORMULA",
            "q_loc_units": "MISSING_Q_LOC_UNITS",
            "norm_definition": "MISSING_LOCAL_NORM_DEFINITION",
            "normalization_reference": "MISSING_A_REF_OR_DIMENSIONLESS_GATE",
            "P_loc_definition": "MISSING_P_LOC_DEFINITION",
            "Gamma_eff_formula": "MISSING_GAMMA_EFF_FORMULA",
            "K_hat_formula": "MISSING_K_HAT_FORMULA",
            "K_metric_formula": "MISSING_K_METRIC_VARIATION_FORMULA",
            "Delta_K_formula": "MISSING_DELTA_K_COMPARISON",
            "source_path": "MISSING_SOURCE_PATH",
            "source_anchor": "MISSING_SOURCE_ANCHOR",
            "equation_ref": "MISSING_EQUATION_REF",
            "arena_projection": "PPN;clock;orbital;local_GR",
            "bound_threshold": "MISSING_ARENA_BOUND_THRESHOLD",
            "bound_units": "MISSING_BOUND_UNITS",
            "theorem_zero_certificate": "MISSING_PARENT_ZERO_CERTIFICATE",
            "no_cancellation_guard": "TRUE",
            "derivation_status": "template_invalid_missing_profile_and_metric_response",
            "valid_for_claim": False,
            "claim_allowed": False,
            "notes": "Replace every MISSING_* field and pass branch/refusal gates before this can become a live residual row.",
        }
    ]

    profile_rules = [
        {
            "rule_id": "GKR1281_0_template_invalid",
            "requirement": "template rows are not live finite rows",
            "refusal_if": "template_id contains DO_NOT_SCORE or any MISSING_* marker remains",
            "status": "ACTIVE_REFUSAL_RULE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "GKR1281_1_source_path_anchor",
            "requirement": "source path and source anchor must exist and contain the equation/definition",
            "refusal_if": "missing source path, missing anchor, or anchor not found",
            "status": "REQUIRED_FOR_LIVE_ROW",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "GKR1281_2_metric_response_or_bound",
            "requirement": "either metric-response identity closes or q_loc profile/bound is explicit",
            "refusal_if": "neither theorem_zero_certificate nor source-backed numeric/symbolic bound exists",
            "status": "REQUIRED_FOR_CLAIM_REOPEN",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "GKR1281_3_no_cancellation",
            "requirement": "epsilon_GK_q_loc is scored as an absolute component",
            "refusal_if": "cancellation with closure baseline or another residual is used",
            "status": "ACTIVE_REFUSAL_RULE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    validator_rescan = scan_rab_intake()
    docs_rows = [row for row in validator_rescan if row["intake_class"] == "docs"]
    raw_rows = [row for row in validator_rescan if row["intake_class"] == "raw"]
    accepted_rows = [row for row in validator_rescan if row["intake_class"] == "accepted"]
    accepted_ready = [row for row in validator_rescan if row["intake_eligible"] and row["intake_class"] in {"raw", "accepted"}]

    claim_gates = [
        {
            "gate_id": "GATE1281_0_metric_response_match",
            "claim": "Gamma_eff/K_hat metric-response identity is matched",
            "status": "BLOCKED",
            "reason": "Gamma_eff formula, K_hat formula, metric variation, and Delta_K ledger are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1281_1_q_loc_profile",
            "claim": "epsilon_GK_q_loc profile/bound row is live",
            "status": "BLOCKED",
            "reason": "only a DO_NOT_SCORE template exists and contains MISSING markers",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1281_2_q_loc_zero",
            "claim": "q_loc is parent-zero",
            "status": "BLOCKED",
            "reason": "metric-response match and double-zero/Euler/boundary certificates remain open",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1281_3_local_tests",
            "claim": "local GR/Newton/R10/PPN/clock/orbital pass",
            "status": "BLOCKED",
            "reason": "epsilon_GK_q_loc is neither parent-zero nor bounded",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1281_4_finite_rows",
            "claim": "finite residual rows can be scored",
            "status": "BLOCKED",
            "reason": f"docs={len(docs_rows)} raw={len(raw_rows)} accepted={len(accepted_rows)} accepted_ready={len(accepted_ready)}",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1281_0_symbol_match_result",
            "decision": "do not claim Gamma/Khat metric-response symbol match",
            "because": "current corpus lacks the concrete Gamma_eff and K_hat formulas and metric variation comparison",
            "status": "SYMBOL_MATCH_NOT_CLOSED",
            "next_action": "try response-doublet component map or fill q_loc profile template",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1281_1_profile_template",
            "decision": "create epsilon_GK_q_loc profile template as nonclaim only",
            "because": "a residual cannot be tested until profile, units, norm, normalization, source path, and arena bound exist",
            "status": "PROFILE_TEMPLATE_WRITTEN_INVALID_BY_DESIGN",
            "next_action": "replace MISSING fields only with source-backed equations/values",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1281_2_next_derivation",
            "decision": "try response-doublet component map for F1=0 next",
            "because": "the response doublet is the most plausible route to derive double-zero rather than just bound q_loc",
            "status": "RESPONSE_DOUBLET_ROUTE_SELECTED",
            "next_action": "map Z^A components to physical q_loc/PPN residual vector or demote to profile fill",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1281_0_1282",
            "target_file": "1282-Y5-R10-RAB-response-doublet-component-map-F1-zero-or-q_loc-profile-fill.md",
            "target_script": "scripts/Y5_R10_RAB_response_doublet_component_map_F1_zero_or_q_loc_profile_fill.py",
            "task": "try to map response-doublet variables Z^A to the physical q_loc/PPN residual vector and prove the F1=0 double-zero condition; if this fails, keep epsilon_GK_q_loc profile filling as the nonclaim empirical route",
            "success_condition": "response-doublet symmetry covers the real local residual components and forbids linear sources, or the q_loc profile template remains the only live nonclaim route",
            "do_not": "do not treat formal Z=0 double-zero as physical q_loc silence until the component map is signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_tables = [
        (SOURCE_REGISTER_PATH, source_register),
        (SYMBOL_MATCH_PATH, symbol_match),
        (TENSOR_CONTRACT_PATH, tensor_contract),
        (PROFILE_TEMPLATE_PATH, profile_template),
        (PROFILE_RULES_PATH, profile_rules),
        (VALIDATOR_RESCAN_PATH, validator_rescan),
        (CLAIM_GATES_PATH, claim_gates),
        (DECISION_PATH, decisions),
        (NEXT_PATH, next_target),
    ]
    for path, rows in generated_tables:
        write_csv(path, rows)

    source_checks = [exists_and_contains(row["local_path"], row["needle"]) for row in source_register]
    all_sources_exist = all(exists for exists, _ in source_checks)
    all_needles_found = all(found for _, found in source_checks)
    symbol_match_not_closed = any(
        row["match_id"] == "GKM1281_4_verdict" and row["status"] == "SYMBOL_MATCH_NOT_CLOSED"
        for row in symbol_match
    )
    template_written_invalid = len(profile_template) == 1 and contains_missing_marker(profile_template[0]) and is_false(profile_template[0]["valid_for_claim"])
    profile_rules_ready = {row["rule_id"] for row in profile_rules} >= {
        "GKR1281_0_template_invalid",
        "GKR1281_1_source_path_anchor",
        "GKR1281_2_metric_response_or_bound",
        "GKR1281_3_no_cancellation",
    }
    tensor_contract_blocks = any(
        row["contract_id"] == "MRT1281_1_Ward_consequence" and row["current_status"] == "BLOCKED_BY_METRIC_RESPONSE_AND_EULER"
        for row in tensor_contract
    )
    docs_rejected = len(docs_rows) > 0 and all(row["status"] == "REJECT" for row in docs_rows)
    no_live_rows = len(raw_rows) == 0 and len(accepted_rows) == 0 and len(accepted_ready) == 0
    claim_gates_blocked = all(row["status"] == "BLOCKED" for row in claim_gates)
    all_generated_rows = [
        *source_register,
        *symbol_match,
        *tensor_contract,
        *profile_template,
        *profile_rules,
        *validator_rescan,
        *claim_gates,
        *decisions,
        *next_target,
    ]
    nonclaim_policy = all(is_false(row.get("valid_for_claim")) and is_false(row.get("claim_allowed")) for row in all_generated_rows)
    formalization_generated = generated_inside_formalization()

    parsed_details = []
    csv_parse_ok = True
    for path, _rows in generated_tables:
        try:
            parsed_rows = read_csv(path)
            parsed_details.append(f"{path.name}:{len(parsed_rows)}")
        except Exception as exc:
            csv_parse_ok = False
            parsed_details.append(f"{path.name}:ERROR:{exc}")

    validation = [
        validation_row(
            "VAL1281_0_sources_exist",
            "all cited local sources exist",
            all_sources_exist,
            f"{sum(1 for exists, _ in source_checks if exists)}/{len(source_checks)} sources exist",
        ),
        validation_row(
            "VAL1281_1_needles_found",
            "all cited local needles found",
            all_needles_found,
            f"{sum(1 for _, found in source_checks if found)}/{len(source_checks)} needles found",
        ),
        validation_row(
            "VAL1281_2_symbol_match",
            "Gamma/Khat metric-response symbol match remains not closed",
            symbol_match_not_closed,
            "GKM1281_4_verdict=SYMBOL_MATCH_NOT_CLOSED",
        ),
        validation_row(
            "VAL1281_3_tensor_contract",
            "Ward consequence remains blocked by metric-response and Euler gaps",
            tensor_contract_blocks,
            "MRT1281_1_Ward_consequence=BLOCKED_BY_METRIC_RESPONSE_AND_EULER",
        ),
        validation_row(
            "VAL1281_4_profile_template",
            "epsilon_GK_q_loc profile template is written and invalid by design",
            template_written_invalid,
            "template contains MISSING markers and valid_for_claim=false",
        ),
        validation_row(
            "VAL1281_5_profile_rules",
            "profile intake rules block templates, missing sources, missing bounds, and cancellation",
            profile_rules_ready,
            f"profile_rule_rows={len(profile_rules)}",
        ),
        validation_row(
            "VAL1281_6_finite_fallback_locked",
            "finite branch has no source-backed accepted rows",
            docs_rejected and no_live_rows,
            f"docs_rows={len(docs_rows)}; raw_rows={len(raw_rows)}; accepted_rows={len(accepted_rows)}; accepted_ready={len(accepted_ready)}",
        ),
        validation_row(
            "VAL1281_7_claim_gates_blocked",
            "all claim gates remain blocked",
            claim_gates_blocked,
            f"claim_gate_rows={len(claim_gates)}",
        ),
        validation_row(
            "VAL1281_8_nonclaim_policy",
            "all generated rows remain nonclaim",
            nonclaim_policy,
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        ),
        validation_row(
            "VAL1281_9_next_target_1282",
            "next target routes to response-doublet component map or q_loc profile fill",
            next_target[0]["next_id"] == "NEXT1281_0_1282",
            str(next_target[0]["target_file"]),
        ),
        validation_row(
            "VAL1281_10_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(parsed_details),
        ),
        validation_row(
            "VAL1281_11_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            len(formalization_generated) == 0,
            f"formalization_generated_output_count={len(formalization_generated)}",
        ),
    ]
    overall_pass = all(row["status"] == "PASS" for row in validation)
    validation.append(
        validation_row(
            "VAL1281_12_overall",
            "overall 1281 validation",
            overall_pass,
            "1281 attempts Gamma/Khat metric-response symbol matching, blocks it for missing formulas/tensor variation, writes an invalid-by-design epsilon_GK_q_loc profile template, and routes to response-doublet component-map/F1-zero next",
        )
    )
    write_csv(VALIDATION_PATH, validation)

    doc = f"""# {TITLE}

**Current verdict:** 1281 does not match the actual `Gamma_eff` and `K_hat` symbols to the metric-response identity. The blocker is concrete: missing `Gamma_eff` formula, missing `K_hat` tensor formula, missing metric variation, and missing `Delta_K=K_hat-K_metric` ledger.

**Main progress:** `epsilon_GK_q_loc` now has a strict nonclaim profile template. It is invalid by design until every `MISSING_*` field is replaced by source-backed equations, units, normalization, projection, and bounds.

**Next derivation target:** response-doublet component mapping. The formal double-zero route only matters if the doublet components are proven to be the real physical `q_loc`/PPN residual components.

**No-claim guard:** no metric-response match, `q_loc=0`, A511_3 silence, local-GR/Newton, R10, PPN, clock, orbital, or finite residual branch is claim-valid.

Run timestamp UTC: `{RUN_STARTED_UTC.isoformat()}`

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "purpose", "valid_for_claim", "claim_allowed"])}

## Gamma/Khat Symbol Match Audit
{markdown_table(symbol_match, ["match_id", "symbol", "required_for_match", "current_evidence", "status", "next_input", "valid_for_claim", "claim_allowed"])}

## Metric-Response Tensor Contract
{markdown_table(tensor_contract, ["contract_id", "identity", "definition", "pass_condition", "current_status", "valid_for_claim", "claim_allowed"])}

## epsilon_GK_q_loc Profile Template
{markdown_table(profile_template, ["template_id", "residual_component", "branch_id", "q_loc_profile_formula", "q_loc_units", "norm_definition", "normalization_reference", "P_loc_definition", "Gamma_eff_formula", "K_hat_formula", "K_metric_formula", "Delta_K_formula", "source_path", "source_anchor", "equation_ref", "arena_projection", "bound_threshold", "bound_units", "theorem_zero_certificate", "no_cancellation_guard", "derivation_status", "valid_for_claim", "claim_allowed", "notes"])}

## Profile Intake Rules
{markdown_table(profile_rules, ["rule_id", "requirement", "refusal_if", "status", "valid_for_claim", "claim_allowed"])}

## Z_R Validator Rescan
{markdown_table(validator_rescan, ["scan_id", "intake_class", "row_id", "coefficient_symbol", "status", "reasons", "source_exists", "anchor_found", "intake_eligible", "valid_for_claim", "claim_allowed"])}

## Claim Gates
{markdown_table(claim_gates, ["gate_id", "claim", "status", "reason", "valid_for_claim", "claim_allowed"])}

## Decision Ledger
{markdown_table(decisions, ["decision_id", "decision", "because", "status", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target
{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation
{markdown_table(validation, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()

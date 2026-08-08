from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1280"
TITLE = "1280-Y5-R10-RAB-Gamma-Khat-qloc-action-existence-or-extra-residual-bound"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
RAB_INTAKE_DIR = ROOT / "source-intake" / "rab-sector"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
ACTION_GATE_PATH = OUT_DIR / f"{PACK_ID}_GK_ACTION_EXISTENCE_GATE.csv"
METRIC_RESPONSE_PATH = OUT_DIR / f"{PACK_ID}_METRIC_RESPONSE_SYMBOL_MATCH_AUDIT.csv"
HELMHOLTZ_PATH = OUT_DIR / f"{PACK_ID}_HELMHOLTZ_EULER_DOUBLE_ZERO_AUDIT.csv"
BOUND_CONTRACT_PATH = OUT_DIR / f"{PACK_ID}_EPSILON_GK_QLOC_BOUND_CONTRACT.csv"
A511_IMPACT_PATH = OUT_DIR / f"{PACK_ID}_A511_IMPACT.csv"
VALIDATOR_RESCAN_PATH = OUT_DIR / f"{PACK_ID}_ZR_VALIDATOR_RESCAN.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1280_VALIDATION.csv"


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
        "scan_id": f"SCAN1280_{intake_class}_{path.stem}_{row_id}",
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
        ACTION_GATE_PATH,
        METRIC_RESPONSE_PATH,
        HELMHOLTZ_PATH,
        BOUND_CONTRACT_PATH,
        A511_IMPACT_PATH,
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
            "source_id": "SRC1280_0_1279_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1279_NEXT_TARGET.csv",
            "needle": "NEXT1279_0_1280",
            "purpose": "handoff into Gamma/Khat/q_loc action-existence target",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1280_1_1279_residual",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1279_EXTRA_SECTOR_RESIDUAL_VECTOR.csv",
            "needle": "XRV1279_2_GK_q_loc",
            "purpose": "epsilon_GK_q_loc retained as extra-sector residual",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1280_2_1010_verdict",
            "local_path": "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
            "needle": "GKT1010_6_verdict",
            "purpose": "prior q_loc derivation route not closed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1280_3_GK_contract",
            "local_path": "source-intake/mts_residuals/P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv",
            "needle": "GK513_0_action_existence",
            "purpose": "first-variation clauses required for q_loc zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1280_4_GK_candidates",
            "local_path": "source-intake/mts_residuals/P8_GK_STRESS_ACTION_CANDIDATES.csv",
            "needle": "GK514_A_metric_response_scalar_density",
            "purpose": "candidate metric-response scalar density action",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1280_5_gate_tests",
            "local_path": "source-intake/mts_residuals/P8_GK_STRESS_ACTION_GATE_TESTS.csv",
            "needle": "G514_2_current_MTS_match",
            "purpose": "current MTS symbol match fails",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1280_6_decision",
            "local_path": "source-intake/mts_residuals/P8_GK_STRESS_ACTION_DECISION.csv",
            "needle": "D514_1,current_MTS_not_matched",
            "purpose": "prior decision: Gamma/Khat not matched",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1280_7_response_doublet",
            "local_path": "source-intake/mts_residuals/P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv",
            "needle": "RD516_2_metric_response",
            "purpose": "response-doublet route not checked/currently matched",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1280_8_metric_contract",
            "local_path": "source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_CONTRACT.csv",
            "needle": "MR514_1_Khat_metric_response",
            "purpose": "metric-response pass condition",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1280_9_validator",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1269_ZR_INTAKE_VALIDATOR_SUMMARY.csv",
            "needle": "NO_ACCEPTED_SOURCE_READY_ROWS",
            "purpose": "finite residual source rows remain absent",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    action_gate = [
        {
            "gate_id": "GKA1280_0_action_existence",
            "required_clause": "local diffeomorphism-invariant S_GK exists",
            "candidate_form": "S_GK = - integral sqrt(-g) Gamma_eff(g,Phi,nabla Phi,D,...)",
            "current_evidence": "candidate written in 1010 and GK514_A",
            "status": "CANDIDATE_CONTRACT_ONLY",
            "failure_mode": "Gamma_eff/K_hat remain bookkeeping if no action is parent-signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GKA1280_1_metric_response",
            "required_clause": "K_hat equals metric response of sqrt(-g) Gamma_eff",
            "candidate_form": "K_hat^{mu nu}=2/sqrt(-g) delta[sqrt(-g)Gamma_eff]/delta g_mu_nu minus volume/sign convention",
            "current_evidence": "P8_GK_STRESS_ACTION_GATE_TESTS says current MTS match fails",
            "status": "FAIL_CURRENT_SYMBOL_MATCH",
            "failure_mode": "Gamma and Khat remain independent knobs; q_loc cannot be Ward-zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GKA1280_2_Helmholtz",
            "required_clause": "stress tensor is variational under second-variation symmetry",
            "candidate_form": "delta(sqrt(-g)T_GK)/delta g has Helmholtz symmetry up to boundary",
            "current_evidence": "1010 marks not_checked_current_claim",
            "status": "NOT_CHECKED_FOR_CURRENT_SYMBOLS",
            "failure_mode": "no action exists for proposed stress",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GKA1280_3_Euler_closure",
            "required_clause": "fields building Gamma/Khat obey local compact vacuum Euler equations",
            "candidate_form": "nabla_mu T_GK^{mu nu}=sum_A E_A nabla^nu Phi^A + boundary",
            "current_evidence": "1010 marks not_derived",
            "status": "NOT_DERIVED",
            "failure_mode": "q_loc remains physical force/source-exchange residual",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GKA1280_4_double_zero",
            "required_clause": "T_GK(Phi0)=0 and partial_A T_GK(Phi0)=0",
            "candidate_form": "Gamma0 subtraction plus matched K_hat response removes F_1",
            "current_evidence": "response doublet has formal candidate but not MTS promotion",
            "status": "CONDITIONAL_NOT_MATCHED",
            "failure_mode": "linear PPN/source-normalization hair can remain",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GKA1280_5_projector_boundary",
            "required_clause": "P_loc ownership and boundary/symplectic no-flux",
            "candidate_form": "P_loc=P_parent(Phi0), partial_A P_loc=0, boundary Delta(theta_GK,Q_GK,tau)=0",
            "current_evidence": "1010 marks open",
            "status": "OPEN",
            "failure_mode": "projection or boundary terms can hide force/mass flux",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GKA1280_6_verdict",
            "required_clause": "all GKA1280_0..5 pass",
            "candidate_form": "q_loc^nu is parent-zero in local branch",
            "current_evidence": "multiple gates blocked",
            "status": "QLOC_ZERO_NOT_DERIVED",
            "failure_mode": "epsilon_GK_q_loc must be retained with strict bound contract",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    metric_response = [
        {
            "match_id": "MRM1280_0_scalar_density",
            "target": "Gamma_eff",
            "pass_condition": "declared covariant scalar density/function of parent fields, not data-fit readout function",
            "current_status": "UNSIGNED",
            "evidence": "MR514_0 requires declaration; symbol map says Gamma_eff not action-placed",
            "next_required_artifact": "Gamma_eff formula, units, parent field content, source path",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "match_id": "MRM1280_1_Khat_response",
            "target": "K_hat^{mu nu}",
            "pass_condition": "exact metric response of sqrt(-g)Gamma_eff including derivative and boundary terms",
            "current_status": "FAIL_CURRENT_MATCH",
            "evidence": "G514_2_current_MTS_match=fail_for_current_claim",
            "next_required_artifact": "K_metric formula and tensor-term comparison to existing K_hat",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "match_id": "MRM1280_2_response_doublet",
            "target": "Gamma_eff double-zero candidate",
            "pass_condition": "exchange doublets cover physical q_loc/PPN residual vector and forbid linear source terms",
            "current_status": "CONDITIONAL_NOT_COMPONENT_DERIVED",
            "evidence": "RD516 and AV517 are candidates, not matched to current symbols",
            "next_required_artifact": "component map Z^A -> physical local residuals and source-zero proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "match_id": "MRM1280_3_verdict",
            "target": "metric-response route",
            "pass_condition": "MRM1280_0..2 pass",
            "current_status": "NOT_MATCHED",
            "evidence": "current MTS not matched to metric-response identity",
            "next_required_artifact": "1281 symbol-match contract or residual profile row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    helmholtz = [
        {
            "audit_id": "HED1280_0_Helmholtz_symmetry",
            "condition": "second metric variation is symmetric up to boundary and gauge constraints",
            "current_status": "NOT_CHECKED_CURRENT_SYMBOLS",
            "blocks": "action existence",
            "residual_if_fail": "epsilon_GK_q_loc",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "HED1280_1_Euler_on_shell",
            "condition": "all parent fields inside Gamma/Khat have E_A=0 local compact vacuum equations",
            "current_status": "NOT_DERIVED",
            "blocks": "q_loc Ward/Euler zero",
            "residual_if_fail": "epsilon_GK_q_loc",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "HED1280_2_double_zero",
            "condition": "T_GK(Phi0)=0 and partial_A T_GK(Phi0)=0",
            "current_status": "CONDITIONAL_NOT_MTS_MATCHED",
            "blocks": "linear local PPN/source-normalization silence",
            "residual_if_fail": "epsilon_GK_F1",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "HED1280_3_projector_boundary",
            "condition": "P_loc is parent-owned and boundary/symplectic flux vanishes or is fixed",
            "current_status": "OPEN",
            "blocks": "local force/mass flux silence",
            "residual_if_fail": "epsilon_GK_boundary",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "HED1280_4_verdict",
            "condition": "Helmholtz+Euler+double-zero+boundary all pass",
            "current_status": "NOT_CLOSED",
            "blocks": "q_loc parent-zero claim",
            "residual_if_fail": "epsilon_GK_q_loc retained",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    bound_contract = [
        {
            "bound_id": "BND1280_0_definition",
            "residual_component": "epsilon_GK_q_loc",
            "formula": "||P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})||_local / a_ref_or_dimensionless_gate",
            "required_inputs": "q_loc_profile; units; local norm; P_loc definition; Gamma_eff formula; K_hat formula; normalization; source path",
            "current_status": "MISSING_PROFILE_AND_NORMALIZATION",
            "maps_to_tests": "PPN;clock;orbital;local_GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "BND1280_1_theorem_zero_switch",
            "residual_component": "epsilon_GK_q_loc",
            "formula": "theorem_zero=true iff action existence, metric response, Helmholtz, Euler, double-zero, projector, and boundary pass",
            "required_inputs": "GKA1280_0..5 PASS with source paths",
            "current_status": "THEOREM_ZERO_FALSE",
            "maps_to_tests": "all local tests",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "BND1280_2_source_bound_switch",
            "residual_component": "epsilon_GK_q_loc",
            "formula": "abs(epsilon_GK_q_loc) <= bound_GK(arena) after source-backed profile or conservative envelope",
            "required_inputs": "numeric or symbolic bound; observable projection; arena-specific threshold; source file; assumptions",
            "current_status": "BOUND_MISSING",
            "maps_to_tests": "PPN;clock;orbital;local_GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "BND1280_3_no_cancellation",
            "residual_component": "epsilon_GK_q_loc plus extra-sector vector",
            "formula": "score absolute components individually; no cancellation with closure baseline or other residuals",
            "required_inputs": "componentwise gates and no-cancellation guard",
            "current_status": "GUARD_WRITTEN",
            "maps_to_tests": "combined local residual vector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "BND1280_4_row_status",
            "residual_component": "epsilon_GK_q_loc",
            "formula": "retain row as nonclaim until theorem_zero or source_bound closes",
            "required_inputs": "real source-backed values or parent-zero certificates",
            "current_status": "RETAIN_NONCLAIM",
            "maps_to_tests": "all local tests remain blocked for claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    a511_impact = [
        {
            "impact_id": "A511I1280_0_extra_silence",
            "dependency": "A511_3_extra_field_silence",
            "current_status": "BLOCKED_BY_EPSILON_GK_QLOC",
            "effect": "EH inheritance remains blocked because one concrete extra-sector force residual is not zero/bounded",
            "next_action": "match Gamma_eff/K_hat symbols to metric-response action or retain q_loc profile row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "impact_id": "A511I1280_1_local_branch",
            "dependency": "1278 local branch firewall",
            "current_status": "PROTECTS_CLOSURE_BRANCH",
            "effect": "closure-only local tests cannot erase epsilon_GK_q_loc",
            "next_action": "keep epsilon_GK_q_loc in residual vector until parent-zero or source-bound",
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
            "gate_id": "GATE1280_0_q_loc_zero",
            "claim": "q_loc^nu is parent-zero",
            "status": "BLOCKED",
            "reason": "action existence, metric response match, Helmholtz, Euler, double-zero, projector, and boundary are not all signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1280_1_epsilon_bound",
            "claim": "epsilon_GK_q_loc is source-bounded",
            "status": "BLOCKED",
            "reason": "profile, normalization, source path, and arena thresholds are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1280_2_A511_3",
            "claim": "A511_3 extra-sector silence closes",
            "status": "BLOCKED",
            "reason": "epsilon_GK_q_loc remains active",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1280_3_local_tests",
            "claim": "local GR/Newton/R10/PPN/clock/orbital pass",
            "status": "BLOCKED",
            "reason": "q_loc residual is neither parent-zero nor source-bounded",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1280_4_finite_rows",
            "claim": "finite residual rows can be scored",
            "status": "BLOCKED",
            "reason": f"docs={len(docs_rows)} raw={len(raw_rows)} accepted={len(accepted_rows)} accepted_ready={len(accepted_ready)}",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1280_0_q_loc_result",
            "decision": "do not claim q_loc parent-zero",
            "because": "current MTS symbols do not match the metric-response action and Helmholtz/Euler/double-zero/boundary clauses are open",
            "status": "QLOC_ZERO_NOT_DERIVED",
            "next_action": "attempt direct Gamma_eff/K_hat symbol match to metric-response action",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1280_1_bound_contract",
            "decision": "retain epsilon_GK_q_loc with a strict bound contract",
            "because": "the residual can be made testable only after profile, units, normalization, and source paths exist",
            "status": "BOUND_CONTRACT_WRITTEN_NONCLAIM",
            "next_action": "make an executable symbol-match/profile template for epsilon_GK_q_loc",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1280_2_A511_impact",
            "decision": "keep A511_3 and EH inheritance blocked",
            "because": "one active q_loc force residual contaminates the local EH fixed point",
            "status": "EH_INHERITANCE_STILL_BLOCKED",
            "next_action": "continue derivation-first at the Gamma/Khat symbol-match level",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1280_0_1281",
            "target_file": "1281-Y5-R10-RAB-Gamma-Khat-metric-response-symbol-match-or-q_loc-profile-template.md",
            "target_script": "scripts/Y5_R10_RAB_Gamma_Khat_metric_response_symbol_match_or_q_loc_profile_template.py",
            "task": "try to match the actual Gamma_eff and K_hat symbols to the metric-response identity K_hat=2/sqrt(-g)delta[sqrt(-g)Gamma_eff]/delta g; if that fails, create a strict epsilon_GK_q_loc profile/bound template without claiming local GR",
            "success_condition": "metric-response identity is symbol-matched with source paths, or epsilon_GK_q_loc gets a complete nonclaim profile/bound intake template",
            "do_not": "do not treat the candidate S_GK or response doublet as a current-symbol proof without the tensor match",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_tables = [
        (SOURCE_REGISTER_PATH, source_register),
        (ACTION_GATE_PATH, action_gate),
        (METRIC_RESPONSE_PATH, metric_response),
        (HELMHOLTZ_PATH, helmholtz),
        (BOUND_CONTRACT_PATH, bound_contract),
        (A511_IMPACT_PATH, a511_impact),
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
    qloc_not_derived = any(row["gate_id"] == "GKA1280_6_verdict" and row["status"] == "QLOC_ZERO_NOT_DERIVED" for row in action_gate)
    metric_not_matched = any(row["match_id"] == "MRM1280_3_verdict" and row["current_status"] == "NOT_MATCHED" for row in metric_response)
    helmholtz_not_closed = any(row["audit_id"] == "HED1280_4_verdict" and row["current_status"] == "NOT_CLOSED" for row in helmholtz)
    bound_contract_ready = any(row["bound_id"] == "BND1280_4_row_status" and row["current_status"] == "RETAIN_NONCLAIM" for row in bound_contract)
    a511_blocked = any(row["impact_id"] == "A511I1280_0_extra_silence" and row["current_status"] == "BLOCKED_BY_EPSILON_GK_QLOC" for row in a511_impact)
    docs_rejected = len(docs_rows) > 0 and all(row["status"] == "REJECT" for row in docs_rows)
    no_live_rows = len(raw_rows) == 0 and len(accepted_rows) == 0 and len(accepted_ready) == 0
    claim_gates_blocked = all(row["status"] == "BLOCKED" for row in claim_gates)
    all_generated_rows = [
        *source_register,
        *action_gate,
        *metric_response,
        *helmholtz,
        *bound_contract,
        *a511_impact,
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
            "VAL1280_0_sources_exist",
            "all cited local sources exist",
            all_sources_exist,
            f"{sum(1 for exists, _ in source_checks if exists)}/{len(source_checks)} sources exist",
        ),
        validation_row(
            "VAL1280_1_needles_found",
            "all cited local needles found",
            all_needles_found,
            f"{sum(1 for _, found in source_checks if found)}/{len(source_checks)} needles found",
        ),
        validation_row(
            "VAL1280_2_q_loc_not_derived",
            "q_loc parent-zero is not promoted",
            qloc_not_derived,
            "GKA1280_6_verdict=QLOC_ZERO_NOT_DERIVED",
        ),
        validation_row(
            "VAL1280_3_metric_response",
            "metric-response symbol match remains open/failed",
            metric_not_matched,
            "MRM1280_3_verdict=NOT_MATCHED",
        ),
        validation_row(
            "VAL1280_4_helmholtz",
            "Helmholtz/Euler/double-zero route remains not closed",
            helmholtz_not_closed,
            "HED1280_4_verdict=NOT_CLOSED",
        ),
        validation_row(
            "VAL1280_5_bound_contract",
            "epsilon_GK_q_loc bound contract is retained as nonclaim",
            bound_contract_ready,
            "BND1280_4_row_status=RETAIN_NONCLAIM",
        ),
        validation_row(
            "VAL1280_6_A511_impact",
            "A511_3 remains blocked by epsilon_GK_q_loc",
            a511_blocked,
            "A511I1280_0_extra_silence=BLOCKED_BY_EPSILON_GK_QLOC",
        ),
        validation_row(
            "VAL1280_7_finite_fallback_locked",
            "finite branch has no source-backed accepted rows",
            docs_rejected and no_live_rows,
            f"docs_rows={len(docs_rows)}; raw_rows={len(raw_rows)}; accepted_rows={len(accepted_rows)}; accepted_ready={len(accepted_ready)}",
        ),
        validation_row(
            "VAL1280_8_claim_gates_blocked",
            "all claim gates remain blocked",
            claim_gates_blocked,
            f"claim_gate_rows={len(claim_gates)}",
        ),
        validation_row(
            "VAL1280_9_nonclaim_policy",
            "all generated rows remain nonclaim",
            nonclaim_policy,
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        ),
        validation_row(
            "VAL1280_10_next_target_1281",
            "next target routes to metric-response symbol match or q_loc profile template",
            next_target[0]["next_id"] == "NEXT1280_0_1281",
            str(next_target[0]["target_file"]),
        ),
        validation_row(
            "VAL1280_11_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(parsed_details),
        ),
        validation_row(
            "VAL1280_12_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            len(formalization_generated) == 0,
            f"formalization_generated_output_count={len(formalization_generated)}",
        ),
    ]
    overall_pass = all(row["status"] == "PASS" for row in validation)
    validation.append(
        validation_row(
            "VAL1280_13_overall",
            "overall 1280 validation",
            overall_pass,
            "1280 tests Gamma/Khat/q_loc action-existence and metric-response gates, blocks q_loc parent-zero, retains epsilon_GK_q_loc with a strict bound contract, and routes to symbol matching/profile template next",
        )
    )
    write_csv(VALIDATION_PATH, validation)

    doc = f"""# {TITLE}

**Current verdict:** 1280 does not derive `q_loc^nu=0`. The candidate `S_GK` route is still the best mathematical shape, but current MTS has not matched the actual `Gamma_eff` and `K_hat` symbols to a metric-response action, and the Helmholtz/Euler/double-zero/projector/boundary clauses remain unsigned.

**Main progress:** `epsilon_GK_q_loc` is now a strict nonclaim residual component, not a foggy objection. It needs either a parent-zero theorem or a source-backed profile/bound before local PPN, clock, orbital, or local-GR claims can reopen.

**No-claim guard:** no `q_loc=0`, A511_3 silence, EH inheritance, local-GR/Newton, R10, PPN, clock, orbital, or finite residual branch is claim-valid.

Run timestamp UTC: `{RUN_STARTED_UTC.isoformat()}`

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "purpose", "valid_for_claim", "claim_allowed"])}

## GK Action-Existence Gate
{markdown_table(action_gate, ["gate_id", "required_clause", "candidate_form", "current_evidence", "status", "failure_mode", "valid_for_claim", "claim_allowed"])}

## Metric-Response Symbol Match Audit
{markdown_table(metric_response, ["match_id", "target", "pass_condition", "current_status", "evidence", "next_required_artifact", "valid_for_claim", "claim_allowed"])}

## Helmholtz/Euler/Double-Zero Audit
{markdown_table(helmholtz, ["audit_id", "condition", "current_status", "blocks", "residual_if_fail", "valid_for_claim", "claim_allowed"])}

## epsilon_GK_q_loc Bound Contract
{markdown_table(bound_contract, ["bound_id", "residual_component", "formula", "required_inputs", "current_status", "maps_to_tests", "valid_for_claim", "claim_allowed"])}

## A511 Impact
{markdown_table(a511_impact, ["impact_id", "dependency", "current_status", "effect", "next_action", "valid_for_claim", "claim_allowed"])}

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

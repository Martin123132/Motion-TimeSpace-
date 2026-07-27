from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1308"
TITLE = "1308-Y5-R10-RAB-canonical-memory-source-test-charge-zero-or-bound"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
ZERO_ROUTE_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_ZERO_ROUTE_AUDIT.csv"
CANONICAL_ALPHA_INPUTS_PATH = OUT_DIR / f"{PACK_ID}_CANONICAL_ALPHA_INPUTS_NONCLAIM.csv"
SOURCE_TEST_DECISION_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_TEST_CHARGE_DECISION_MATRIX.csv"
LOCAL_RESIDUAL_UPDATE_PATH = OUT_DIR / f"{PACK_ID}_LOCAL_RESIDUAL_UPDATE.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1308_VALIDATION.csv"


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
        ZERO_ROUTE_AUDIT_PATH,
        CANONICAL_ALPHA_INPUTS_PATH,
        SOURCE_TEST_DECISION_PATH,
        LOCAL_RESIDUAL_UPDATE_PATH,
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
            "source_id": "SRC1308_0_1307_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1307_NEXT_TARGET.csv",
            "needle": "NEXT1307_0_1308",
            "role": "handoff into source/test charge zero-or-bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1308_1_1307_transfer",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1307_TRANSFER_RESIDUAL_LEDGER_NONCLAIM.csv",
            "needle": "TRL1307_2_Qc_source_charge",
            "role": "canonical transferred source/test/projection residuals",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1308_2_1307_alpha",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1307_ALPHA_TRANSFER_AUDIT.csv",
            "needle": "ZERO_ROUTE_UNCHANGED_BY_CANONICALIZATION",
            "role": "alpha zero route after Z_m canonicalization",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1308_3_alpha_inputs",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_ALPHA_LAW_PARENT_INPUTS.csv",
            "needle": "PI560_4_qtest",
            "role": "parent alpha inputs for J, Q, q, PiM, measured GM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1308_4_alpha_derivation",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_SOURCE_NORMALIZED_ALPHA_DERIVATION_ATTEMPT.csv",
            "needle": "alpha_X=0 if Pi_M^H Q_X^H=0 or q_X^T=0",
            "role": "exact alpha zero conditions",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1308_5_1042_source_zero",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1042_SOURCE_ZERO_CLAUSE_AUDIT.csv",
            "needle": "FAIL_CURRENT_CLAIM_JX_ZERO_NOT_SIGNED",
            "role": "source zero route is not parent signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1308_6_618_source_zero",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_618_SOURCE_ZERO_CERTIFICATE_AUDIT.csv",
            "needle": "SZ618_0_qbar_XT_chain_rule",
            "role": "conditional qbar_XT zero route and source zero certificate audit",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1308_7_670_no_pole",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_670_NO_POLE_QUOTIENT_PROOF_CHAIN.csv",
            "needle": "NQ670_5_matter_descent",
            "role": "matter descent route for qbar_XT=0 remains constants-open",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1308_8_670_effect",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_670_R10_R11_ZERO_OR_RESIDUAL_EFFECT.csv",
            "needle": "MISSING_MATTER_CONSTANT_OWNERSHIP",
            "role": "test charge zero is blocked by material/constant ownership",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1308_9_source_norm_stack",
            "local_path": "source-intake/mts_residuals/P8_SOURCE_NORMALIZATION_THEOREM_STACK.csv",
            "needle": "S5_Newton_gate",
            "role": "source-normalized Newton gate fails current corpus",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1308_10_source_norm_950",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_950_SOURCE_NORMALIZATION_LEMMA_ATTEMPT.csv",
            "needle": "species-weighted source current",
            "role": "countermodel blocks covariance-only source universality",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1308_11_newton_norm",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_868_NEWTON_SOURCE_NORMALIZATION_CONTRACT.csv",
            "needle": "NS868_2_source_charge_universality",
            "role": "Newton source charge universality remains open",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1308_12_boundary_gate",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_671_BOUNDARY_CHARGE_OWNER_GATE.csv",
            "needle": "BCG671_7_verdict",
            "role": "boundary source charge zero not passed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1308_13_projection_gate",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_672_PROJECTOR_ORTHOGONALITY_ATTEMPT.csv",
            "needle": "PO672_6_verdict",
            "role": "projector orthogonality route not passed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    zero_route_audit = [
        {
            "route_id": "ZRA1308_0_Jc_zero",
            "target": "J_c=0 in compact local exterior",
            "zero_condition": "ordinary matter, constants, boundary, projector, domain, and memory sources vanish by one parent identity or are bounded absolutely",
            "current_evidence": "1042 records the channel decomposition and verdict FAIL_CURRENT_CLAIM_JX_ZERO_NOT_SIGNED.",
            "current_status": "NOT_DERIVED_SOURCE_CHANNELS_OPEN",
            "blocks": "positive nohair; local profile silence; Q_c source charge",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1042_SOURCE_ZERO_CLAUSE_AUDIT.csv",
            "source_anchor": "SZ1042_5_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "route_id": "ZRA1308_1_Qc_zero",
            "target": "Pi_M^H Q_c^H(lambda)=0 or Q_c^H(lambda)=0",
            "zero_condition": "bulk/source, boundary, projector, memory, and finite-size source charges vanish or are orthogonal to measured mass projection",
            "current_evidence": "670/671/672 retain Qbar_XH, Qbar_edge_XH, boundary/projector/memory channels as live residuals.",
            "current_status": "NOT_DERIVED_SOURCE_PROJECTION_OPEN",
            "blocks": "R10 alpha numerator; source-normalization; R11 residual vector",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_670_R10_R11_ZERO_OR_RESIDUAL_EFFECT.csv;source-intake/mts_residuals/P8_Y5_R10_671_BOUNDARY_CHARGE_OWNER_GATE.csv;source-intake/mts_residuals/P8_Y5_R10_672_PROJECTOR_ORTHOGONALITY_ATTEMPT.csv",
            "source_anchor": "ZE670_2_Qbar_XH;BCG671_7_verdict;PO672_6_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "route_id": "ZRA1308_2_qc_zero",
            "target": "q_c^T=0 for ordinary test bodies",
            "zero_condition": "S_matter descends through observed quotient and all constants/material labels are inert under the vertical memory direction",
            "current_evidence": "618 and 670 give a valid conditional chain-rule theorem, but constants/material marker ownership and no-extension remain open.",
            "current_status": "CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "blocks": "R10 test charge; WEP source/test split; matter-coupling closure",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_618_SOURCE_ZERO_CERTIFICATE_AUDIT.csv;source-intake/mts_residuals/P8_Y5_R10_670_NO_POLE_QUOTIENT_PROOF_CHAIN.csv",
            "source_anchor": "SZ618_0_qbar_XT_chain_rule;NQ670_5_matter_descent",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "route_id": "ZRA1308_3_source_normalization",
            "target": "measured GM cannot hide Q_c/q_c",
            "zero_condition": "same-frame EH source, constant universal kappa, Gauss-law mass, no extra long-range charge, and no absorption cheat all pass",
            "current_evidence": "source normalization stack fails S5 and 950 gives a species-weighted countermodel.",
            "current_status": "NOT_DERIVED_ANTI_CHEAT_ACTIVE",
            "blocks": "R1 WEP source charge; R9 Gdot; R10; R11; PPN source normalization",
            "source_path": "source-intake/mts_residuals/P8_SOURCE_NORMALIZATION_THEOREM_STACK.csv;source-intake/mts_residuals/P8_Y5_R10_950_SOURCE_NORMALIZATION_LEMMA_ATTEMPT.csv",
            "source_anchor": "S5_Newton_gate;SNL950_4_countermodel;SNL950_5_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "route_id": "ZRA1308_4_verdict",
            "target": "canonical alpha zero or bound",
            "zero_condition": "alpha_c=0 only if Pi_M^H Q_c^H=0 or q_c^T=0, or the physical source spectrum is theorem-zero",
            "current_evidence": "no zero route is parent-signed; nonclaim alpha/source rows must be staged instead of claiming local-GR/R10 silence.",
            "current_status": "ZERO_NOT_CLOSED_STAGE_NONCLAIM_ALPHA_INPUTS",
            "blocks": "local-GR promotion; R10 pass; nohair promotion",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1307_ALPHA_TRANSFER_AUDIT.csv;source-intake/mts_residuals/P8_Y5_R10_SOURCE_NORMALIZED_ALPHA_DERIVATION_ATTEMPT.csv",
            "source_anchor": "ATA1307_1_zero_routes;AL560_8_zero_conditions",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    canonical_alpha_inputs = [
        {
            "input_id": "CAI1308_0_lambda_c",
            "symbol": "lambda_c",
            "definition": "canonical finite-range memory/source mode range, lambda_c=1/M_c after canonical normalization",
            "needed_for": "R10 alpha(lambda) row and nohair/range decision",
            "current_value": "MISSING_M_c_OR_MASS_GAP",
            "units": "length",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_ALPHA_LAW_PARENT_INPUTS.csv",
            "source_anchor": "PI560_1_mX",
            "derivation_status": "closure_assumed_input_missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "CAI1308_1_Qc",
            "symbol": "Q_c^H(lambda)",
            "definition": "canonical source monopole/form-factor charge including compact source, boundary, projector, and memory pieces",
            "needed_for": "alpha numerator and source-free nohair",
            "current_value": "MISSING_SOURCE_CHARGE_OR_ZERO_THEOREM",
            "units": "canonical_source_charge_units_required",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_ALPHA_LAW_PARENT_INPUTS.csv",
            "source_anchor": "PI560_3_QX",
            "derivation_status": "nonclaim_residual_input_missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "CAI1308_2_qc",
            "symbol": "q_c^T",
            "definition": "canonical test-body charge/coupling to the memory/source mode",
            "needed_for": "R10 force on matter; WEP/source-test status",
            "current_value": "MISSING_TEST_CHARGE_OR_MATTER_DESCENT_ZERO",
            "units": "canonical_test_charge_units_required",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_ALPHA_LAW_PARENT_INPUTS.csv;source-intake/mts_residuals/P8_Y5_R10_618_SOURCE_ZERO_CERTIFICATE_AUDIT.csv",
            "source_anchor": "PI560_4_qtest;SZ618_0_qbar_XT_chain_rule",
            "derivation_status": "conditional_zero_not_parent_signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "CAI1308_3_PiMQ",
            "symbol": "Pi_M^H[Q_c^H(lambda)]",
            "definition": "mass/Hamiltonian projection of canonical source charge into measured local force sector",
            "needed_for": "decide whether a nonzero canonical source is gravitationally silent",
            "current_value": "MISSING_PROJECTOR_ORTHOGONALITY_OR_NUMERIC_PROJECTION",
            "units": "mass_or_charge_projection_units_required",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_672_PROJECTOR_ORTHOGONALITY_ATTEMPT.csv",
            "source_anchor": "PO672_6_verdict",
            "derivation_status": "nonclaim_projection_input_missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "CAI1308_4_alpha_c",
            "symbol": "alpha_c(lambda)",
            "definition": "alpha_c(lambda)=s_c Pi_M^H[Q_c^H(lambda)] q_c^T/(4*pi*G_obs*M_H*m_T)",
            "needed_for": "R10 comparator row after canonical Z_m=1 bookkeeping",
            "current_value": "MISSING_ALPHA_NUMERATOR_AND_MEASURED_GM_SPLIT",
            "units": "dimensionless",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1307_ALPHA_TRANSFER_AUDIT.csv;source-intake/mts_residuals/P8_Y5_R10_SOURCE_NORMALIZED_ALPHA_DERIVATION_ATTEMPT.csv",
            "source_anchor": "ATA1307_0_formula;AL560_6_exact_alpha_law",
            "derivation_status": "formula_only_nonclaim_not_executable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    source_test_decision = [
        {
            "decision_id": "STD1308_0_qc_priority",
            "candidate_zero": "q_c^T=0",
            "why_best_next": "one matter-descent theorem would kill the R10 test force for all source charges without tuning an alpha curve",
            "current_blocker": "MISSING_MATTER_CONSTANT_OWNERSHIP;MISSING_NO_EXTENSION_THEOREM",
            "fallback_if_fail": "stage q_c^T material/species residual vector",
            "rank": 1,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "STD1308_1_PiMQ_second",
            "candidate_zero": "Pi_M^H Q_c^H=0",
            "why_best_next": "would make nonzero canonical source gravitationally silent in R10",
            "current_blocker": "MISSING_BOUNDARY_CHARGE_ZERO;MISSING_PROJECTOR_ORTHOGONALITY;MISSING_SOURCE_MEASURE_GLUE",
            "fallback_if_fail": "stage Q_c/Pi_M source-backed alpha numerator rows",
            "rank": 2,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "STD1308_2_Jc_nohair_third",
            "candidate_zero": "J_c=0",
            "why_best_next": "would support source-free positive nohair and local profile silence",
            "current_blocker": "ordinary matter, boundary, projector, domain, memory, and source-normalization channels all remain open",
            "fallback_if_fail": "bound source profile and run alpha envelope",
            "rank": 3,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    local_residual_update = [
        {
            "update_id": "LRU1308_0_R10",
            "row": "R10_fifth_force",
            "status": "LIVE_NONCLAIM_ALPHA_INPUTS_STAGED",
            "reason": "alpha_c zero not proved; alpha_c row is formula-only with missing Q_c/q_c/PiM/GM inputs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "update_id": "LRU1308_1_R1",
            "row": "R1_WEP_source_charge",
            "status": "LIVE_MATTER_DESCENT_NOT_PARENT_SIGNED",
            "reason": "q_c^T zero depends on matter quotient descent plus inert constants/material labels",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "update_id": "LRU1308_2_R9_R11",
            "row": "R9_Gdot;R11_EH_operator_ledger",
            "status": "LIVE_SOURCE_NORMALIZATION_ANTI_CHEAT",
            "reason": "measured GM cannot absorb range/time/species/radial dependent source charge",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "update_id": "LRU1308_3_local_GR",
            "row": "local_GR_Newton_PPN",
            "status": "NO_LOCAL_GR_CLAIM",
            "reason": "source/test/projection channels are explicit but not zeroed or bounded",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "CG1308_0_qc_zero",
            "claim": "q_c^T=0 for ordinary matter",
            "current_status": "BLOCKED_CONDITIONAL_MATTER_DESCENT_ONLY",
            "reason": "constant/material-marker ownership remains open",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1308_1_Qc_zero",
            "claim": "Pi_M^H Q_c^H=0 or Q_c^H=0",
            "current_status": "BLOCKED_BOUNDARY_PROJECTOR_SOURCE_OPEN",
            "reason": "boundary charge, projector orthogonality, and source-measure glue are not parent-derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1308_2_alpha_executable",
            "claim": "alpha_c(lambda) is executable",
            "current_status": "BLOCKED_NUMERIC_OR_THEOREM_INPUTS_MISSING",
            "reason": "lambda_c, Q_c, q_c, Pi_M, sign, and measured-GM split are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1308_3_source_normalization",
            "claim": "measured GM absorbs no hidden source charge",
            "current_status": "BLOCKED_SOURCE_NORMALIZATION_NOT_DERIVED",
            "reason": "source-normalization Newton gate fails current corpus and countermodel survives",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1308_4_local_GR",
            "claim": "local GR/Newton/PPN recovery follows",
            "current_status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "reason": "source/test charge channel remains live",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1308_0_no_zero_claim",
            "decision": "do not claim alpha/local source-test silence",
            "because": "all three zero routes are conditional or blocked by explicit source/matter/projection gaps",
            "next_action": "attack q_c^T=0 by matter descent and constant/material-marker ownership first",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1308_1_nonclaim_alpha_rows",
            "decision": "stage canonical alpha inputs as nonclaim rows",
            "because": "if q_c^T zero fails, the next honest path is a sourced alpha(lambda) row rather than hidden normalization",
            "next_action": "derive q_c^T zero or build q_c^T residual prior with material/species tags",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1308_0_1309",
            "target_file": "1309-Y5-R10-RAB-matter-descent-constant-marker-theorem-or-qc-residual.md",
            "target_script": "scripts/Y5_R10_RAB_matter_descent_constant_marker_theorem_or_qc_residual.py",
            "task": "try to prove q_c^T=0 from parent matter descent plus inert constants/material labels; if it fails, stage q_c^T material/species residual rows",
            "success_condition": "q_c^T theorem-zero is parent-signed, or an explicit nonclaim q_c^T residual vector is ready for R10/WEP source-charge testing",
            "do_not": "do not let direct coframe WEP or canonical Z_m=1 substitute for source/test charge zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(ZERO_ROUTE_AUDIT_PATH, zero_route_audit)
    write_csv(CANONICAL_ALPHA_INPUTS_PATH, canonical_alpha_inputs)
    write_csv(SOURCE_TEST_DECISION_PATH, source_test_decision)
    write_csv(LOCAL_RESIDUAL_UPDATE_PATH, local_residual_update)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)

    validations = []
    source_count = len(source_register)
    source_hits = sum(1 for row in source_register if row["exists"] and row["needle_found"])
    validations.append(
        validation_row(
            "VAL1308_0_sources_exist",
            "registered source paths exist and anchors are found",
            source_hits == source_count,
            f"{source_hits}/{source_count} source anchors found",
        )
    )
    validations.append(
        validation_row(
            "VAL1308_1_zero_routes_blocked",
            "zero-route audit blocks alpha/local silence claim",
            any(row["route_id"] == "ZRA1308_4_verdict" and row["current_status"] == "ZERO_NOT_CLOSED_STAGE_NONCLAIM_ALPHA_INPUTS" for row in zero_route_audit)
            and all(is_false(row["valid_for_claim"]) for row in zero_route_audit),
            ";".join(str(row["route_id"]) + "=" + str(row["current_status"]) for row in zero_route_audit),
        )
    )
    required_alpha_inputs = {"CAI1308_0_lambda_c", "CAI1308_1_Qc", "CAI1308_2_qc", "CAI1308_3_PiMQ", "CAI1308_4_alpha_c"}
    validations.append(
        validation_row(
            "VAL1308_2_alpha_inputs_staged",
            "canonical nonclaim alpha inputs include lambda, Q, q, PiM projection, and alpha formula",
            required_alpha_inputs.issubset({str(row["input_id"]) for row in canonical_alpha_inputs})
            and all("MISSING" in str(row["current_value"]) for row in canonical_alpha_inputs),
            ";".join(str(row["input_id"]) + "=" + str(row["current_value"]) for row in canonical_alpha_inputs),
        )
    )
    validations.append(
        validation_row(
            "VAL1308_3_qc_next_priority",
            "decision matrix chooses q_c test charge zero as next best route",
            any(row["decision_id"] == "STD1308_0_qc_priority" and int(row["rank"]) == 1 for row in source_test_decision),
            ";".join(str(row["decision_id"]) + "=rank" + str(row["rank"]) for row in source_test_decision),
        )
    )
    validations.append(
        validation_row(
            "VAL1308_4_local_rows_live",
            "local residual update keeps R10/WEP/source-normalization/local-GR rows live",
            len(local_residual_update) == 4 and all(is_false(row["valid_for_claim"]) for row in local_residual_update),
            ";".join(str(row["update_id"]) + "=" + str(row["status"]) for row in local_residual_update),
        )
    )
    validations.append(
        validation_row(
            "VAL1308_5_claim_gates_block",
            "claim gates remain blocked",
            len(claim_gates) == 5 and all(str(row["current_status"]).startswith("BLOCKED") for row in claim_gates),
            ";".join(str(row["gate_id"]) + "=" + str(row["current_status"]) for row in claim_gates),
        )
    )
    generated_tables = [
        SOURCE_REGISTER_PATH,
        ZERO_ROUTE_AUDIT_PATH,
        CANONICAL_ALPHA_INPUTS_PATH,
        SOURCE_TEST_DECISION_PATH,
        LOCAL_RESIDUAL_UPDATE_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
    ]
    parse_ok = True
    parse_details: list[str] = []
    for table_path in generated_tables:
        try:
            parse_details.append(f"{table_path.name}:{len(read_csv(table_path))}")
        except Exception as error:
            parse_ok = False
            parse_details.append(f"{table_path.name}:ERROR:{error}")
    validations.append(validation_row("VAL1308_6_csv_parse", "all generated CSVs parse cleanly", parse_ok, "; ".join(parse_details)))
    formalization_hits = generated_inside_formalization()
    validations.append(
        validation_row(
            "VAL1308_7_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            not formalization_hits,
            f"formalization_generated_output_count={len(formalization_hits)}",
        )
    )
    validations.append(
        validation_row(
            "VAL1308_8_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim([source_register, zero_route_audit, canonical_alpha_inputs, source_test_decision, local_residual_update, claim_gates, decision, next_target]),
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    validations.append(
        validation_row(
            "VAL1308_9_next_target_1309",
            "next target routes to matter descent constant-marker theorem or q_c residual",
            next_target[0]["next_id"] == "NEXT1308_0_1309" and "matter-descent" in str(next_target[0]["target_file"]),
            str(next_target[0]["target_file"]),
        )
    )
    overall_pass = all(row["status"] == "PASS" for row in validations)
    validations.append(
        validation_row(
            "VAL1308_10_overall",
            "overall 1308 validation",
            overall_pass,
            "1308 does not prove source/test charge zero; it stages nonclaim canonical alpha inputs, keeps local rows live, and routes to q_c^T matter-descent theorem/residual 1309",
        )
    )
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# 1308 Y5 R10 RAB canonical memory source test charge zero or bound

Generated: `{RUN_STARTED_UTC.isoformat()}`

**Current verdict:** the canonical source/test charge channel does **not** close. After `Z_m=1` bookkeeping, the exact alpha zero routes are still `Pi_M^H Q_c^H=0`, `q_c^T=0`, or a parent theorem killing the physical source spectrum. None is parent-signed in the current corpus.

**Main progress:** the surviving alpha inputs are now explicit nonclaim rows: `lambda_c`, `Q_c^H(lambda)`, `q_c^T`, `Pi_M^H[Q_c^H]`, and `alpha_c(lambda)`. This prevents the coupling from hiding inside measured `GM` or canonical normalization.

**Decision:** go after `q_c^T=0` first. If ordinary matter descends through the observed quotient and constants/material labels are inert, the test charge dies for all sources at once. That is the cleanest next theorem route; if it fails, we stage a material/species residual vector.

## Source Register

{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Zero Route Audit

{markdown_table(zero_route_audit, ["route_id", "target", "zero_condition", "current_evidence", "current_status", "blocks", "source_path", "source_anchor", "valid_for_claim", "claim_allowed"])}

## Canonical Alpha Inputs

{markdown_table(canonical_alpha_inputs, ["input_id", "symbol", "definition", "needed_for", "current_value", "units", "source_path", "source_anchor", "derivation_status", "valid_for_claim", "claim_allowed"])}

## Source/Test Charge Decision Matrix

{markdown_table(source_test_decision, ["decision_id", "candidate_zero", "why_best_next", "current_blocker", "fallback_if_fail", "rank", "valid_for_claim", "claim_allowed"])}

## Local Residual Update

{markdown_table(local_residual_update, ["update_id", "row", "status", "reason", "valid_for_claim", "claim_allowed"])}

## Claim Gates

{markdown_table(claim_gates, ["gate_id", "claim", "current_status", "reason", "valid_for_claim", "claim_allowed"])}

## Decision Ledger

{markdown_table(decision, ["decision_id", "decision", "because", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation

{markdown_table(validations, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()

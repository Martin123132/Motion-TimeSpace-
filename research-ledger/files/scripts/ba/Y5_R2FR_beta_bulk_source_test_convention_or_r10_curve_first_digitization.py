from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1690"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "1690-Y5-R2FR-beta-bulk-source-test-convention-or-r10-curve-first-digitization.md"

SOURCE_FILES = {
    "1689_doc": ROOT / "1689-Y5-R2FR-bulk-alpha-template-beta-kernel-tail-fill-or-r10-curve-digitization.md",
    "1689_validation": OUT / "P8_Y5_BRR545_1689_VALIDATION.csv",
    "1689_template": OUT / "R10_alpha_lambda_curve_MTS_1689_BULK_ALPHA_TEMPLATE_SOURCE.csv",
    "1689_qbar_result": OUT / "P8_Y5_PARENT_QLOC_1689_QBAR_VALIDATOR_RESULT.csv",
    "1573_doc": ROOT / "1573-Y5-RAB-internal-tauR10-source-kernel-or-manual-curve-acceptance.md",
    "1573_kernel": OUT / "P8_Y5_PARENT_QLOC_1573_TAU_R10_KERNEL_DERIVATION_CONTRACT.csv",
    "1573_required": OUT / "P8_Y5_PARENT_QLOC_1573_TAU_R10_REQUIRED_INPUTS.csv",
    "1574_doc": ROOT / "1574-Y5-RAB-R10-matter-charge-and-ZR-MR2-input-row-or-zero-theorem.md",
    "1574_beta_theorem": OUT / "P8_Y5_PARENT_QLOC_1574_RAB_MATTER_CHARGE_ZERO_THEOREM_ATTEMPT.csv",
    "1574_finite_inputs": OUT / "P8_Y5_PARENT_QLOC_1574_RAB_FINITE_INPUT_ROWS_NONCLAIM.csv",
    "1575_doc": ROOT / "1575-Y5-RAB-parent-RAB-vertical-generator-and-matter-descent-signature.md",
    "1575_descent": OUT / "P8_Y5_PARENT_QLOC_1575_RAB_MATTER_DESCENT_SIGNATURE.csv",
    "1576_doc": ROOT / "1576-Y5-RAB-constraint-no-pole-or-quotient-map-construction.md",
    "1576_no_pole": OUT / "P8_Y5_PARENT_QLOC_1576_RAB_CONSTRAINT_NO_POLE_TEST.csv",
    "1578_doc": ROOT / "1578-Y5-RAB-finite-component-bound-pack-and-runner.md",
    "1578_arena": OUT / "P8_Y5_PARENT_QLOC_1578_ARENA_BLOCK_MATRIX.csv",
    "1578_runner": OUT / "P8_Y5_PARENT_QLOC_1578_PLACEHOLDER_REFUSAL_RUNNER.csv",
    "1579_doc": ROOT / "1579-Y5-RAB-finite-component-source-acquisition-ledger-and-comparator-dry-run.md",
    "1579_external": OUT / "P8_Y5_PARENT_QLOC_1579_EXTERNAL_BOUND_AUDIT.csv",
    "1579_decision": OUT / "P8_Y5_PARENT_QLOC_1579_DECISION.csv",
    "1571_curve_candidate": OUT / "P8_Y5_PARENT_QLOC_1571_R10_ALPHA_LAMBDA_DIGITIZED_QA_CANDIDATE.csv",
    "1034_curve_candidate": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
}

NEEDLES = {
    "1689_doc": ["runner-shaped nonclaim template", "beta_bulk,S", "1690-Y5-R2FR-beta-bulk-source-test-convention-or-r10-curve-first-digitization.md"],
    "1689_validation": ["VAL1689_OVERALL", "PASS"],
    "1689_template": ["K_bulk_ST(lambda)*beta_bulk_S*beta_bulk_T+epsilon_tail(lambda)", "beta_bulk_S"],
    "1689_qbar_result": ["QVR1689_0", "PLACEHOLDER_OR_BLOCKED_FIELDS"],
    "1573_doc": ["alpha_MTS(lambda_R)=Xi_R10", "beta_S^R"],
    "1573_kernel": ["KDER1573_4_alpha_match", "FORMAL_TAU_KERNEL_LAW_DERIVED_CONDITIONAL"],
    "1573_required": ["REQ1573_2_beta_source", "MISSING_SOURCE_CHARGE"],
    "1574_doc": ["beta_i^R", "EXACT_CONDITIONAL_THEOREM_NOT_SIGNED"],
    "1574_beta_theorem": ["RMC1574_2_zero_if_signed", "EXACT_CONDITIONAL_THEOREM_NOT_SIGNED"],
    "1574_finite_inputs": ["FIN1574_0_beta_source", "MISSING_SOURCE_CHARGE_OR_ZERO_THEOREM"],
    "1575_doc": ["Closure-only verticality is refused", "Matter Descent Signature"],
    "1575_descent": ["MDS1575_5_verdict", "FAIL_CURRENT_CLAIM_DESCENT_NOT_SIGNED"],
    "1576_doc": ["CONSTRAINT_ROUTE_MOTIVATED_NOT_DERIVED", "QUOTIENT_MAP_CONFLICT_IDENTIFIED"],
    "1576_no_pole": ["CNP1576_5_verdict", "FAIL_CURRENT_CLAIM_CONSTRAINT_NO_POLE_NOT_DERIVED"],
    "1578_doc": ["PLACEHOLDER_REFUSAL_RUNNER_ACTIVE", "beta_S^R"],
    "1578_arena": ["ARENA1578_1_PPN", "BLOCKED_NO_CLAIM"],
    "1578_runner": ["RUN1578_4_linear_coupling_shortcut", "REFUSE_PLACEHOLDER"],
    "1579_doc": ["PPN_RESIDUAL_VECTOR_FIRST", "derive gamma_minus_1"],
    "1579_external": ["EXT1579_0_R10", "REVIEW_CANDIDATE_NONCLAIM_ROWS_PRESENT"],
    "1579_decision": ["DEC1579_2_next", "NEXT_1580_RAB_PPN_RESIDUAL_VECTOR_OR_QRHAT_SOURCE_ROW"],
    "1571_curve_candidate": ["QA1571_000", "QA_CLEANED_CANDIDATE_NONCLAIM"],
    "1034_curve_candidate": ["review_candidate_only_requires_official_supplement", "false"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1690_SOURCE_REGISTER.csv"
BETA_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1690_BETA_RECONCILIATION_AUDIT.csv"
BETA_CONVENTION = OUT / "P8_Y5_PARENT_QLOC_1690_BETA_CONVENTION_CANDIDATE_NONCLAIM.csv"
CURVE_STATUS = OUT / "P8_Y5_PARENT_QLOC_1690_R10_CURVE_STATUS_RECONCILIATION.csv"
IMPORT_GATE = OUT / "P8_Y5_PARENT_QLOC_1690_CURRENT_BRANCH_IMPORT_GATE.csv"
NEXT_ROUTE = OUT / "P8_Y5_PARENT_QLOC_1690_NEXT_ROUTE_SELECTION.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1690_CLAIM_GATE.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1690_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    BETA_AUDIT,
    BETA_CONVENTION,
    CURVE_STATUS,
    IMPORT_GATE,
    NEXT_ROUTE,
    CLAIM_GATE,
]

CLAIM_CHECKED = [
    BETA_AUDIT,
    BETA_CONVENTION,
    CURVE_STATUS,
    IMPORT_GATE,
    NEXT_ROUTE,
    CLAIM_GATE,
]

COPY_TARGETS = {
    BETA_AUDIT: [
        QUARANTINE / "BETA_RECONCILIATION_AUDIT.csv",
        BRANCH_RESIDUALS / "R2FR_beta_reconciliation_audit_1690.csv",
        QUEUE / "JR1690_BETA_RECONCILIATION_AUDIT.csv",
    ],
    BETA_CONVENTION: [
        QUARANTINE / "BETA_CONVENTION_CANDIDATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_beta_convention_candidate_1690.csv",
        QUEUE / "JR1690_BETA_CONVENTION_CANDIDATE_NONCLAIM.csv",
    ],
    CURVE_STATUS: [
        QUARANTINE / "R10_CURVE_STATUS_RECONCILIATION.csv",
        BRANCH_RESIDUALS / "R2FR_r10_curve_status_reconciliation_1690.csv",
        QUEUE / "JR1690_R10_CURVE_STATUS_RECONCILIATION.csv",
    ],
    NEXT_ROUTE: [
        QUARANTINE / "NEXT_ROUTE_SELECTION.csv",
        BRANCH_RESIDUALS / "R2FR_next_route_selection_1690.csv",
        QUEUE / "JR1690_NEXT_ROUTE_SELECTION.csv",
    ],
}


def ensure_dirs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def bool_cell(value: object) -> bool:
    return str(value).strip().lower() == "true"


def list_cell(values: list[object] | tuple[object, ...]) -> str:
    return ";".join(str(value) for value in values)


def markdown_table(rows: list[dict[str, object]], headers: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for key, path in SOURCE_FILES.items():
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles = NEEDLES[key]
        needles_present = exists and all(needle in text for needle in needles)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_key": key,
                "source_path": str(path),
                "exists": exists,
                "needles_present": needles_present,
                "required_needles": list_cell(needles),
                "use_in_1690": "current beta/R10/PPN route reconciliation",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def curve_candidate_count() -> int:
    candidate = SOURCE_FILES["1571_curve_candidate"]
    if not candidate.exists():
        return 0
    return len(read_csv(candidate))


def beta_audit_rows() -> list[dict[str, object]]:
    rows = [
        (
            "BRA1690_0_current_template",
            "1689 current branch",
            "alpha_bulk,ST(lambda)=K_bulk,ST(lambda)*beta_bulk,S*beta_bulk,T+epsilon_tail(lambda)",
            "RUNNER_SHAPED_NONCLAIM_TEMPLATE_READY",
            "beta legs are visible to the runner but remain symbolic",
        ),
        (
            "BRA1690_1_kernel_law",
            "1573 finite R_AB kernel",
            "alpha_MTS(lambda_R)=Xi_R10[beta_S^R beta_T^R/(4*pi*G*Z_R)+alpha_boundary_tail]",
            "FORMAL_CONDITIONAL_KERNEL_LAW_AVAILABLE",
            "Z_R, M_R^2, Xi_R10, beta legs and tail are not sourced",
        ),
        (
            "BRA1690_2_beta_definition",
            "1574 matter-charge definition",
            "beta_i^R := partial ln m_i^eff / partial R_AB = M_i^-1 delta_vR S_i",
            "BEST_CURRENT_BETA_CONVENTION_NONCLAIM",
            "definition is clean; parent signatures are unsigned",
        ),
        (
            "BRA1690_3_beta_zero_theorem",
            "conditional descent theorem",
            "beta_i^R=0 if v_R in ker(Dq), matter descends through q, constants are fixed, markers absent, and boundary terms silent",
            "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "do not import beta zero into current branch",
        ),
        (
            "BRA1690_4_verticality_conflict",
            "1575/1576 coframe visibility",
            "R_AB=ln(T^2 S)=2 ln(J_q) is coframe-visible unless a constraint/no-pole or explicit quotient map removes it",
            "CURRENT_BLOCKER_IDENTIFIED",
            "cheap verticality is refused",
        ),
        (
            "BRA1690_5_runner_policy",
            "1578 placeholder refusal",
            "single coupling shortcuts, unsigned zeroes, reviewed-only curves, and cross-arena transfers are refused",
            "SAFETY_POLICY_IMPORTED_AS_NONCLAIM",
            "keeps beta/coupling hunt disciplined",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "object": obj,
            "equation_or_contract": equation,
            "status": status,
            "current_effect": effect,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for audit_id, obj, equation, status, effect in rows
    ]


def beta_convention_rows() -> list[dict[str, object]]:
    rows = [
        (
            "BETAC1690_0_source_leg",
            "beta_bulk,S / beta_S^R",
            "partial ln m_source^eff / partial R_AB",
            "bulk-neutral source body charge in finite R_AB/R10 branch",
            "THEOREM_ZERO_IF_PARENT_DESCENT_SIGNED_OR_NUMERIC_FINITE_ROW",
            "NOT_PARENT_SIGNED",
            "MISSING_SOURCE_CHARGE_OR_ZERO_THEOREM",
        ),
        (
            "BETAC1690_1_test_leg",
            "beta_bulk,T / beta_T^R",
            "partial ln m_test^eff / partial R_AB",
            "bulk-neutral test body/readout charge in finite R_AB/R10 branch",
            "THEOREM_ZERO_IF_PARENT_DESCENT_SIGNED_OR_NUMERIC_FINITE_ROW",
            "NOT_PARENT_SIGNED",
            "MISSING_TEST_CHARGE_OR_ZERO_THEOREM",
        ),
        (
            "BETAC1690_2_product_law",
            "beta_bulk,S*beta_bulk,T",
            "source-test product; no single-coupling shortcut",
            "R10/WEP/composition exchange amplitude",
            "PRODUCT_FORM_REQUIRED",
            "FORMAL_NONCLAIM_READY",
            "MISSING_BOTH_LEGS_AND_NO_MARKER_THEOREM",
        ),
        (
            "BETAC1690_3_zero_condition",
            "beta_bulk,S=beta_bulk,T=0",
            "Dq[v_R]=0 plus matter descent plus fixed constants plus no-marker plus boundary silence",
            "bulk exchange removal condition",
            "EXACT_CONDITIONAL_THEOREM",
            "UNSIGNED_CURRENT_CORPUS",
            "MISSING_PARENT_Q_CONSTRAINT_NO_POLE_OR_QUOTIENT_SIGNATURE",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "candidate_id": candidate_id,
            "symbol": symbol,
            "definition": definition,
            "role": role,
            "accepted_convention": convention,
            "current_status": status,
            "blocking_gap": gap,
            "source_paths": "1574-Y5-RAB-R10-matter-charge-and-ZR-MR2-input-row-or-zero-theorem.md; 1575-Y5-RAB-parent-RAB-vertical-generator-and-matter-descent-signature.md; 1578-Y5-RAB-finite-component-bound-pack-and-runner.md",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for candidate_id, symbol, definition, role, convention, status, gap in rows
    ]


def curve_status_rows() -> list[dict[str, object]]:
    count = curve_candidate_count()
    rows = [
        (
            "R10CURVE1690_0_current_1689",
            "1689 current live curve state",
            "anchor/template only in current route",
            "CURVE_MISSING_IN_1689_CONTEXT",
            0,
            "not scoreable",
        ),
        (
            "R10CURVE1690_1_prior_candidate",
            "1571 reviewed candidate trace",
            "P8_Y5_PARENT_QLOC_1571_R10_ALPHA_LAMBDA_DIGITIZED_QA_CANDIDATE.csv",
            "REVIEWED_CANDIDATE_NONCLAIM_PRESENT",
            count,
            "useful for future QA but not accepted_for_scoring",
        ),
        (
            "R10CURVE1690_2_1034_local_candidate",
            "1034 local bound review candidate",
            "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "REVIEW_CANDIDATE_ONLY_REQUIRES_OFFICIAL_SUPPLEMENT",
            len(read_csv(SOURCE_FILES["1034_curve_candidate"])) if SOURCE_FILES["1034_curve_candidate"].exists() else 0,
            "secondary source for QA reconciliation, not a claim curve",
        ),
        (
            "R10CURVE1690_3_priority",
            "curve versus beta/PPN priority",
            "external curve is less limiting than missing internal MTS prediction",
            "DO_NOT_DIGITIZE_FIRST_UNLESS_INTERNAL_ALPHA_READY",
            count,
            "next serious work should attack PPN/q_Rhat or beta/no-pole, not chase R10 score",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "curve_id": curve_id,
            "object": obj,
            "source_or_contract": source,
            "status": status,
            "row_count": row_count,
            "effect": effect,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for curve_id, obj, source, status, row_count, effect in rows
    ]


def import_gate_rows() -> list[dict[str, object]]:
    rows = [
        (
            "IMPORT1690_0_kernel",
            "1573 kernel law into 1689 current branch",
            "ALLOW_AS_FORMAL_NONCLAIM",
            "formula may define the symbolic alpha bridge but cannot score",
        ),
        (
            "IMPORT1690_1_beta_convention",
            "1574 beta_i^R convention into beta_bulk,S/T labels",
            "ALLOW_AS_CONVENTION_NONCLAIM",
            "source/test legs now have an exact definition target",
        ),
        (
            "IMPORT1690_2_beta_zero",
            "beta_S^R=beta_T^R=0 import",
            "BLOCK_IMPORT",
            "verticality, matter descent, constants, no-marker and boundary clauses are unsigned",
        ),
        (
            "IMPORT1690_3_curve_candidate",
            "1571/1034 reviewed R10 curve candidates into current route",
            "ALLOW_AS_QA_REFERENCE_ONLY",
            "not accepted_for_scoring and internal alpha is not numeric",
        ),
        (
            "IMPORT1690_4_next_priority",
            "1579 PPN residual-vector priority into current route",
            "ALLOW_AS_NEXT_TARGET",
            "PPN/q_Rhat directly pressures local GR reduction",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "import_object": obj,
            "gate_status": status,
            "reason": reason,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, obj, status, reason in rows
    ]


def next_route_rows() -> list[dict[str, object]]:
    rows = [
        (
            "NEXT1690_0_primary",
            "1691-Y5-R2FR-PPN-residual-vector-or-qRhat-source-row.md",
            "scripts/Y5_R2FR_PPN_residual_vector_or_qRhat_source_row.py",
            "derive gamma_minus_1=C_QR*q_R_hat+source_tail+boundary_tail, or prove q_R_hat remains a missing closure/source row",
            "PPN is the least-dodgy pressure test because it attacks GR reduction rather than asking R10 to carry the whole theory",
            "selected",
        ),
        (
            "NEXT1690_1_secondary",
            "1691b-Y5-R2FR-RAB-no-pole-parent-action-signature.md",
            "scripts/Y5_R2FR_RAB_no_pole_parent_action_signature.py",
            "attempt parent-origin constraint/no-pole proof for R_AB before finite scoring",
            "if this closes, beta zero and local branch become much cleaner",
            "parallel_theory_route_not_selected_first",
        ),
        (
            "NEXT1690_2_held",
            "R10 curve manual acceptance / official table acquisition",
            "manual or source-backed QA workflow",
            "accept or reject reviewed R10 curve only after internal alpha prediction path is ready",
            "external data alone cannot rescue missing beta/Z/M/tail/projector inputs",
            "held",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": route_id,
            "next_target": target,
            "script": script,
            "objective": objective,
            "reason": reason,
            "selection_status": status,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for route_id, target, script, objective, reason, status in rows
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    rows = [
        ("CG1690_0_beta_convention", "beta convention exists", "PASS_FORMAL_NONCLAIM", "definition target imported but not scoreable"),
        ("CG1690_1_beta_zero", "beta_bulk,S=beta_bulk,T=0", "BLOCKED_NO_CLAIM", "parent verticality/descent/no-marker/boundary signatures unsigned"),
        ("CG1690_2_R10_curve", "R10 curve accepted", "BLOCKED_NO_CLAIM", "reviewed candidate exists but is not accepted_for_scoring"),
        ("CG1690_3_R10_score", "R10 comparator can score MTS", "BLOCKED_NO_CLAIM", "internal alpha prediction is symbolic and incomplete"),
        ("CG1690_4_local_GR", "derived local GR/Newton branch", "BLOCKED_NO_CLAIM", "PPN/q_Rhat/source denominator/boundary residual vector not derived"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": claim_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for claim_id, claim, status, reason in rows
    ]


def all_claim_flags_false(paths: list[Path]) -> bool:
    for path in paths:
        for row in read_csv(path):
            for field in ("accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if field in row and bool_cell(row[field]):
                    return False
    return True


def copy_outputs() -> None:
    for source_path, target_paths in COPY_TARGETS.items():
        for target_path in target_paths:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, target_path)


def cleanup_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validate(
    source_rows: list[dict[str, object]],
    beta_rows: list[dict[str, object]],
    convention_rows: list[dict[str, object]],
    curve_rows: list[dict[str, object]],
    import_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    sources_ok = all(bool_cell(row["exists"]) and bool_cell(row["needles_present"]) for row in source_rows)
    convention_present = any(row["symbol"] == "beta_bulk,S / beta_S^R" for row in convention_rows) and any(row["symbol"] == "beta_bulk,T / beta_T^R" for row in convention_rows)
    beta_zero_blocked = any(row["claim"] == "beta_bulk,S=beta_bulk,T=0" and row["status"] == "BLOCKED_NO_CLAIM" for row in claim_rows)
    curve_candidate_present = any(row["status"] == "REVIEWED_CANDIDATE_NONCLAIM_PRESENT" and int(row["row_count"]) > 0 for row in curve_rows)
    curve_not_claim = all(not bool_cell(row["accepted_for_scoring"]) for row in curve_rows)
    import_blocks_zero = any(row["gate_id"] == "IMPORT1690_2_beta_zero" and row["gate_status"] == "BLOCK_IMPORT" for row in import_rows)
    ppn_selected = any(row["route_id"] == "NEXT1690_0_primary" and "PPN-residual-vector" in row["next_target"] and row["selection_status"] == "selected" for row in next_rows)
    r10_held = any(row["route_id"] == "NEXT1690_2_held" and row["selection_status"] == "held" for row in next_rows)
    claims_closed = all(row["status"] in {"PASS_FORMAL_NONCLAIM", "BLOCKED_NO_CLAIM"} and not bool_cell(row["claim_allowed"]) for row in claim_rows)
    csv_parse = True
    for path in GENERATED:
        try:
            read_csv(path)
        except Exception:
            csv_parse = False
    branch_copies = all(target.exists() for targets in COPY_TARGETS.values() for target in targets)
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_untouched = len(list(FORMALIZATION.rglob("*1690*"))) == 0 if FORMALIZATION.exists() else True
    no_claim_flags = all_claim_flags_false(CLAIM_CHECKED)

    checks = [
        ("VAL1690_0_sources_exist", sources_ok, "all cited source paths exist and required needles are present"),
        ("VAL1690_1_convention_present", convention_present, "source and test beta convention rows are present"),
        ("VAL1690_2_beta_zero_blocked", beta_zero_blocked, "beta-zero theorem is not imported as a live claim"),
        ("VAL1690_3_curve_candidate_present", curve_candidate_present, "prior reviewed R10 curve candidate is detected"),
        ("VAL1690_4_curve_nonclaim", curve_not_claim, "R10 curve rows remain nonclaim references"),
        ("VAL1690_5_import_blocks_zero", import_blocks_zero, "current-branch import gate blocks beta-zero promotion"),
        ("VAL1690_6_ppn_selected", ppn_selected, "next primary route selects PPN residual vector/qRhat"),
        ("VAL1690_7_r10_held", r10_held, "R10 curve acceptance is held until internal alpha is ready"),
        ("VAL1690_8_claim_gates_closed", claims_closed, "claim gates remain closed except formal nonclaim convention"),
        ("VAL1690_9_no_claim_flags", no_claim_flags, "all generated rows keep claim/scoring flags false"),
        ("VAL1690_10_csv_parse", csv_parse, "all generated 1690 CSVs parse"),
        ("VAL1690_11_branch_copies", branch_copies, "branch/quarantine/queue copies exist"),
        ("VAL1690_12_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL1690_13_formalization_untouched", formalization_untouched, "no 1690 outputs found under formalization-workbench"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1690_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1690 beta convention and R10 curve reconciliation validation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def write_doc(
    source_rows: list[dict[str, object]],
    beta_rows: list[dict[str, object]],
    convention_rows: list[dict[str, object]],
    curve_rows: list[dict[str, object]],
    import_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    body = f"""# 1690 - Beta Bulk Source/Test Convention Or R10 Curve First Digitization

## Verdict

1690 reconciles the fresh `1689` current branch with the older `1573-1579` coupling work. The beta/coupling route is not empty: the clean convention is now `beta_i^R := partial ln m_i^eff / partial R_AB = M_i^-1 delta_vR S_i`, and the symbolic R10 bridge is `alpha_MTS(lambda_R)=Xi_R10[beta_S^R beta_T^R/(4*pi*G*Z_R)+alpha_boundary_tail]`.

That is still not a claim. `beta_S^R=beta_T^R=0` is exact only under unsigned parent conditions: `v_R in ker(Dq)`, matter descent through the quotient, fixed constants, no marker/source-weight channel, and boundary silence. The prior R10 curve work is also useful but not accepted: a reviewed candidate curve exists, but it remains nonclaim and cannot score symbolic MTS alpha rows.

The best next attack is therefore not more R10 curve chasing. It is the local-GR pressure route: derive the PPN residual vector `gamma_minus_1=C_QR*q_R_hat+source_tail+boundary_tail`, or admit `q_R_hat/Q_R` is a finite missing source row.

## Source Register

{markdown_table(source_rows, ["source_key", "source_path", "exists", "needles_present", "use_in_1690"])}

## Beta Reconciliation Audit

{markdown_table(beta_rows, ["audit_id", "object", "equation_or_contract", "status", "current_effect"])}

## Beta Convention Candidate

{markdown_table(convention_rows, ["candidate_id", "symbol", "definition", "accepted_convention", "current_status", "blocking_gap"])}

## R10 Curve Status

{markdown_table(curve_rows, ["curve_id", "object", "status", "row_count", "effect"])}

## Current Branch Import Gate

{markdown_table(import_rows, ["gate_id", "import_object", "gate_status", "reason"])}

## Next Route Selection

{markdown_table(next_rows, ["route_id", "next_target", "objective", "selection_status"])}

## Claim Gates

{markdown_table(claim_rows, ["claim_id", "claim", "status", "reason"])}

## Validation

{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Working Interpretation

The coupling suspicion was right: the local-test fork lives or dies on whether the `R_AB` source/test charge is a real finite coupling or killed by a parent quotient/no-pole structure. We now have a precise convention and a precise refusal rule. The next stage should attack PPN/q_Rhat because it is closer to derived GR than an R10-only score.
"""
    DOC.write_text(body, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    source_rows = source_register_rows()
    beta_rows = beta_audit_rows()
    convention_rows = beta_convention_rows()
    curve_rows = curve_status_rows()
    import_rows = import_gate_rows()
    next_rows = next_route_rows()
    claim_rows = claim_gate_rows()

    write_csv(SOURCE_REGISTER, source_rows, ["branch_id", "source_key", "source_path", "exists", "needles_present", "required_needles", "use_in_1690", "valid_for_claim", "claim_allowed"])
    write_csv(BETA_AUDIT, beta_rows, ["branch_id", "audit_id", "object", "equation_or_contract", "status", "current_effect", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(BETA_CONVENTION, convention_rows, ["branch_id", "candidate_id", "symbol", "definition", "role", "accepted_convention", "current_status", "blocking_gap", "source_paths", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(CURVE_STATUS, curve_rows, ["branch_id", "curve_id", "object", "source_or_contract", "status", "row_count", "effect", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(IMPORT_GATE, import_rows, ["branch_id", "gate_id", "import_object", "gate_status", "reason", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(NEXT_ROUTE, next_rows, ["branch_id", "route_id", "next_target", "script", "objective", "reason", "selection_status", "valid_for_claim", "claim_allowed"])
    write_csv(CLAIM_GATE, claim_rows, ["branch_id", "claim_id", "claim", "status", "reason", "valid_for_claim", "claim_allowed"])

    copy_outputs()
    cleanup_pycache()
    validation_rows = validate(source_rows, beta_rows, convention_rows, curve_rows, import_rows, next_rows, claim_rows)
    write_csv(VALIDATION, validation_rows, ["check_id", "result", "detail", "valid_for_claim", "claim_allowed"])
    write_doc(source_rows, beta_rows, convention_rows, curve_rows, import_rows, next_rows, claim_rows, validation_rows)

    failed_rows = [row for row in validation_rows if row["result"] != "PASS"]
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    if failed_rows:
        for row in failed_rows:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("1690 validation PASS")


if __name__ == "__main__":
    main()

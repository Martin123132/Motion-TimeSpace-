from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "2707"
BRANCH_ID = "Y5_R2FR_PARENT_ACTION_COEFFICIENT_OWNER_EXTRACTION_2707"

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTAKE = ROOT / "source-intake"
RESIDUALS = SOURCE_INTAKE / "mts_residuals"
LOCAL_BOUNDS = SOURCE_INTAKE / "local_bounds"
SOURCE_WEIGHT = SOURCE_INTAKE / "source-weight"
RAB_QUEUE = SOURCE_INTAKE / "rab-sector" / "acquisition-queue"

DOC_PATH = ROOT / "2707-Y5-R2FR-parent-action-coefficient-owner-extraction.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2707_SOURCE_REGISTER.csv",
    "owner_extraction": RESIDUALS / "P8_Y5_R2FR_2707_PARENT_OWNER_EXTRACTION_MATRIX.csv",
    "branch_trilemma": RESIDUALS / "P8_Y5_R2FR_2707_EXCLUSIVE_BRANCH_TRILEMMA.csv",
    "coefficient_audit": RESIDUALS / "P8_Y5_R2FR_2707_COEFFICIENT_PROMOTION_AUDIT.csv",
    "no_pole_requirements": RESIDUALS / "P8_Y5_R2FR_2707_NO_POLE_CERTIFICATE_REQUIREMENTS.csv",
    "closure_demotion": RESIDUALS / "P8_Y5_R2FR_2707_CLOSURE_DEMOTION_LEDGER.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2707_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2707_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2707_NEXT_TARGET.csv",
    "project_status": RESIDUALS / "P8_Y5_R2FR_2707_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2707_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_closure_demotion": LOCAL_BOUNDS / "finite_local_Xhat_branch_closure_demotion_2707_NONCLAIM.csv",
    "local_no_pole_requirements": LOCAL_BOUNDS / "parent_quotient_no_pole_certificate_requirements_2707_NONCLAIM.csv",
    "source_weight_owner_matrix": SOURCE_WEIGHT / "PARENT_ACTION_OWNER_EXTRACTION_MATRIX_2707_NONCLAIM.csv",
    "rab_next": RAB_QUEUE / "JR2707_PARENT_QUOTIENT_NO_POLE_CERTIFICATE_NEXT.csv",
}

SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "source_id": "SRC2707_2706_HANDOFF",
        "relative_path": "2706-Y5-R2FR-CX-zero-factor-proof-or-first-parent-coefficient-row.md",
        "required_needles": ["NEXT2706_0_selected", "FCC2706_0_selected_Qbar_XH", "CPG2706_0_exact_product"],
        "purpose": "imports the selected parent-action owner extraction task",
    },
    {
        "source_id": "SRC2707_2156_XHAT_CLAUSE",
        "relative_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2156_PARENT_XHAT_ACTION_CLAUSE.csv",
        "required_needles": ["PX2156_0_field_owner", "PX2156_1_same_variable_lock", "PARENT_XHAT_ACTION_CLAUSE_NOT_DERIVED"],
        "purpose": "tests whether Xhat is parent-owned and same-variable locked",
    },
    {
        "source_id": "SRC2707_2156_HESSIAN",
        "relative_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2156_PARENT_HESSIAN_AUDIT.csv",
        "required_needles": ["PHA2156_1_ZX_positive", "PHA2156_2_MX2_positive", "PHA2156_8_verdict"],
        "purpose": "tests finite pole Hessian ownership for Z_X and M_X^2",
    },
    {
        "source_id": "SRC2707_2156_VERDICTS",
        "relative_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2156_BRANCH_VERDICTS.csv",
        "required_needles": ["BV2156_0_Xhat_owner", "PARENT_ACTION_CLAUSE_NOT_DERIVED", "BV2156_4_next_target"],
        "purpose": "imports prior owner verdict and finite-route blocker",
    },
    {
        "source_id": "SRC2707_1026_PARENT_METRIC",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1026_PARENT_METRIC_ATTEMPT.csv",
        "required_needles": ["PM1026_0_metric_target", "PM1026_5_cross_block_guard", "PM1026_6_verdict"],
        "purpose": "tests whether parent field-space metric can normalize Xhat",
    },
    {
        "source_id": "SRC2707_2106_NO_POLE",
        "relative_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2106_NO_POLE_RETURN_LEDGER.csv",
        "required_needles": ["NPR2106_1_no_pole_route", "NPR2106_3_required_certificate", "NPR2106_4_fallback_if_fails"],
        "purpose": "imports no-pole route and required certificate",
    },
    {
        "source_id": "SRC2707_2158_SOURCE_ZERO",
        "relative_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2158_SOURCE_ZERO_IDENTITY.csv",
        "required_needles": ["SZI2158_2_zero_theorem", "SZI2158_3_not_enough", "SZI2158_4_verdict"],
        "purpose": "imports source-zero theorem and counterexample guard",
    },
    {
        "source_id": "SRC2707_1088_MOMS",
        "relative_path": "1088-Y5-R10-minimal-parent-ordinary-matter-signature-clause-or-finite-coefficient-intake.md",
        "required_needles": ["MOMS1088_7_verdict", "THM1088_5_conclusion", "CM1088_0_species_weight"],
        "purpose": "imports minimal ordinary-matter signature and surviving countermodels",
    },
    {
        "source_id": "SRC2707_991_THEOREM_ROUTE",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_991_THEOREM_ROUTE_AUDIT.csv",
        "required_needles": ["HPT991_5_representative_zero_not_enough", "HPT991_6_coupling_descent", "HPT991_7_verdict"],
        "purpose": "prevents representative zero from being reused as observed local-GR proof",
    },
    {
        "source_id": "SRC2707_991_REP_ZERO",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_991_REPRESENTATIVE_ZERO_CREDIT_LEDGER.csv",
        "required_needles": ["RZC991_0_representative_vertical_zero", "cannot kill observed boundary/source/readout flux"],
        "purpose": "imports narrow credit for representative/vertical zero",
    },
    {
        "source_id": "SRC2707_990_PARENT_CONTRACT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_990_PARENT_ACTION_CONTRACT.csv",
        "required_needles": ["PAC990_2_matter_functor", "PAC990_5_Ward_Bianchi", "PAC990_6_PPN_readout"],
        "purpose": "imports full GR/Newton parent-action contract pressure",
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
    except Exception as exc:
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


def owner_extraction_rows() -> list[dict[str, Any]]:
    return [
        {
            "owner_id": "OWN2707_0_Xhat_field_owner",
            "object": "Xhat as parent-action field",
            "required_for": "finite local pole branch; Z_X/M_X^2; K_X; Qbar_XH; no-pole alternative",
            "best_evidence": "PX2156_0_field_owner requires S_parent contains normalized scalar/vertical mode Xhat",
            "current_status": "NOT_SIGNED",
            "promotion_result": "NO_OWNER_EXTRACTED",
            "if_missing": "Xhat cannot be used as a physical pole or as a gauge/no-pole theorem without an explicit parent owner",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "owner_id": "OWN2707_1_same_variable_lock",
            "object": "same Xhat across Hessian, source, matter response and readout",
            "required_for": "prevents separate knobs for range, clocks, WEP, R10 source amplitude and alpha",
            "best_evidence": "PX2156_1_same_variable_lock states the required d ln(c_visible)=b_X dXhat and delta_X S_parent relation",
            "current_status": "NOT_DERIVED",
            "promotion_result": "NO_SAME_VARIABLE_LOCK",
            "if_missing": "finite rows are closure parameters, not one parent-derived local field",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "owner_id": "OWN2707_2_parent_Hessian",
            "object": "Z_X and M_X^2 from parent second variation",
            "required_for": "lambda_X=sqrt(Z_X/M_X^2), positive operator, finite R10/PPN range",
            "best_evidence": "PHA2156_8_verdict and PM1026_6_verdict both fail current claim",
            "current_status": "FAIL_CURRENT_CLAIM",
            "promotion_result": "NO_NUMERIC_ZX_MX2",
            "if_missing": "lambda_X and K_X stay relation-only and cannot be scored",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "owner_id": "OWN2707_3_source_current_owner",
            "object": "J_X / Qbar_XH source current",
            "required_for": "source-zero theorem or finite source charge",
            "best_evidence": "SZI2158_2 gives exact theorem under unsigned premises; Qbar_XH contract remains missing source-current/projection inputs",
            "current_status": "CONDITIONAL_ONLY",
            "promotion_result": "NO_SOURCE_ZERO_OR_NUMERIC_QBAR",
            "if_missing": "compact source can carry a Yukawa monopole or boundary charge",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "owner_id": "OWN2707_4_matter_functor_owner",
            "object": "ordinary matter quotient signature",
            "required_for": "qbar_XT=0, J_matter=0, WEP/local source silence",
            "best_evidence": "MOMS1088 and 1044/1045 prove conditional theorem only",
            "current_status": "MINIMAL_SIGNATURE_NOT_DERIVED",
            "promotion_result": "NO_QBARXT_ZERO_PROMOTION",
            "if_missing": "species weights, variable constants, shadow frames and boundary/domain markers remain live countermodels",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "owner_id": "OWN2707_5_representative_zero_credit",
            "object": "vertical/representative zero",
            "required_for": "possible no-pole branch",
            "best_evidence": "991 allows narrow pruning of representative-only ghost channels but forbids observed source/readout promotion",
            "current_status": "NARROW_CREDIT_ONLY",
            "promotion_result": "NO_OBSERVED_ZERO_FROM_REPRESENTATIVE_ZERO",
            "if_missing": "cannot claim local GR/Newton from vertical language alone",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "owner_id": "OWN2707_6_verdict",
            "object": "parent-action coefficient owner extraction",
            "required_for": "2707 success condition",
            "best_evidence": "all inspected owner clauses remain unsigned or conditional",
            "current_status": "NO_PARENT_OWNER_OR_COEFFICIENT_ROW_EXTRACTED",
            "promotion_result": "DEMOTE_FINITE_LOCAL_XHAT_BRANCH_TO_CLOSURE_INPUT",
            "if_missing": "route must pivot to no-pole/source-zero certificate or remain explicit closure",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def branch_trilemma_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": "TRI2707_A_physical_finite_pole",
            "branch_name": "physical finite Xhat pole",
            "requirements": "parent-owned Xhat; positive Z_X; positive M_X^2; same-variable lock; source/test/readout coefficients; boundary/domain projection",
            "allowed_if_closed": "finite R10/PPN/clock/orbital residual vector can be scored",
            "current_status": "BLOCKED_VALUES_AND_OWNER_MISSING",
            "forbidden_mixing": "cannot use physical-pole Hessian while also declaring Xhat pure gauge for local silence",
            "selected_now": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "branch_id": "TRI2707_B_quotient_no_pole",
            "branch_name": "quotient/gauge no-pole branch",
            "requirements": "v_X in ker(Dq); S_parent descends or is gauge-degenerate along v_X; no boundary charge; matter/source/readout descend; degree count removes physical pole",
            "allowed_if_closed": "C_X=0 without fitting tiny coefficients; strongest GR-like local route",
            "current_status": "BEST_ROUTE_BUT_CERTIFICATE_MISSING",
            "forbidden_mixing": "cannot borrow finite Xhat coefficients from an unphysical representative",
            "selected_now": "next_target",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "branch_id": "TRI2707_C_closure_ansatz",
            "branch_name": "closure/diagnostic finite Xhat ansatz",
            "requirements": "explicitly labelled closure input; no evidence claims; re-entry only by parent owner or source-backed coefficient row",
            "allowed_if_closed": "private algebra and runner plumbing can continue without pretending derivation",
            "current_status": "SELECTED_FOR_CURRENT_FINITE_LOCAL_BRANCH",
            "forbidden_mixing": "cannot present closure coefficients as derived local GR/Newton reduction",
            "selected_now": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "branch_id": "TRI2707_D_inconsistent_hybrid_guard",
            "branch_name": "forbidden hybrid",
            "requirements": "none; this is a guardrail",
            "allowed_if_closed": "not applicable",
            "current_status": "REJECTED",
            "forbidden_mixing": "do not combine physical-pole positivity, quotient-zero source silence and closure coefficients as if all came from one parent action",
            "selected_now": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def coefficient_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "coef_id": "CPA2707_0_ZX",
            "quantity": "Z_X",
            "promotion_question": "does corpus provide parent-owned positive kinetic residue with units?",
            "answer": "no",
            "evidence": "PHA2156_1_ZX_positive=MISSING_PARENT_HESSIAN_SIGN; EXM2106_0_ZX=MISSING_ZX",
            "status_after_2707": "CLOSURE_INPUT_ONLY",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "coef_id": "CPA2707_1_MX2",
            "quantity": "M_X^2",
            "promotion_question": "does corpus provide parent-owned positive mass/range Hessian?",
            "answer": "no",
            "evidence": "PHA2156_2_MX2_positive=MISSING_PARENT_MASS_GAP; EXM2106_1_MX2=MISSING_MX2",
            "status_after_2707": "CLOSURE_INPUT_ONLY",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "coef_id": "CPA2707_2_sX",
            "quantity": "s_X",
            "promotion_question": "does corpus prove the readout/force channel is zero or numeric?",
            "answer": "no",
            "evidence": "PX2156_3 observed frame lock not signed; KX2663 sign convention missing",
            "status_after_2707": "CLOSURE_INPUT_ONLY",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "coef_id": "CPA2707_3_Qbar_XH",
            "quantity": "Qbar_XH(lambda_X)",
            "promotion_question": "does corpus provide source-current zero or numeric source charge?",
            "answer": "no",
            "evidence": "2664 Qbar row is a contract; 2158 source-zero premises unsigned",
            "status_after_2707": "CLOSURE_INPUT_ONLY",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "coef_id": "CPA2707_4_qbar_XT",
            "quantity": "qbar_XT",
            "promotion_question": "does corpus derive ordinary test-body zero response?",
            "answer": "conditional only",
            "evidence": "MOMS1088 proves qbar_XT=0 only if minimal ordinary-matter signature is parent-derived; countermodels retained",
            "status_after_2707": "CONDITIONAL_ZERO_NOT_PROMOTED",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "coef_id": "CPA2707_5_CX",
            "quantity": "C_X product",
            "promotion_question": "does at least one zero factor or all finite factors become claim-grade?",
            "answer": "no",
            "evidence": "2706 product law exact; 2707 owner extraction fails promotion",
            "status_after_2707": "FINITE_LOCAL_BRANCH_DEMOTED_TO_EXPLICIT_CLOSURE",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def no_pole_requirement_rows() -> list[dict[str, Any]]:
    return [
        {
            "requirement_id": "NPC2707_0_qmap",
            "requirement": "parent quotient map q and observed variables are explicit",
            "needed_for": "v_X in ker(Dq) and observed-field silence",
            "current_status": "CONDITIONAL_ONLY",
            "source_hint": "MOMS1088_1; PAC990_0",
            "if_missing": "no-pole branch cannot identify the observed local geometry",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "requirement_id": "NPC2707_1_action_descent",
            "requirement": "S_parent is invariant/degenerate along v_X or descends through q",
            "needed_for": "no physical X pole",
            "current_status": "NOT_SIGNED",
            "source_hint": "NPR2106_1; HPT991_0",
            "if_missing": "v_X may be a physical residual mode",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "requirement_id": "NPC2707_2_degree_count",
            "requirement": "local Hilbert/constraint degree count removes Xhat pole",
            "needed_for": "no-active-pole theorem",
            "current_status": "MISSING_PARENT_DEGREE_SIGNATURE",
            "source_hint": "2706 ZPA2706_0",
            "if_missing": "finite pole branch remains possible",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "requirement_id": "NPC2707_3_boundary_silence",
            "requirement": "boundary, support, domain and projector flux vanish or are bounded",
            "needed_for": "representative zero becoming observed zero",
            "current_status": "MISSING_BOUNDARY_DOMAIN_SILENCE",
            "source_hint": "SZI2158_3; HPT991_4; RZC991_0",
            "if_missing": "observed source/readout flux can survive a vertical zero",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "requirement_id": "NPC2707_4_matter_signature",
            "requirement": "ordinary matter signature forbids species weights, variable constants and shadow frames",
            "needed_for": "qbar_XT=0 and J_matter=0",
            "current_status": "MOMS_CONDITIONAL_NOT_DERIVED",
            "source_hint": "MOMS1088_7; CM1088 rows",
            "if_missing": "source-zero cannot be promoted",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "requirement_id": "NPC2707_5_Bianchi_Ward",
            "requirement": "selectors, boundaries and hidden/projector variables obey Ward/Bianchi conservation or are retained",
            "needed_for": "GR/Newton reduction without silent Euler leaks",
            "current_status": "OPEN",
            "source_hint": "PAC990_5_Ward_Bianchi",
            "if_missing": "local GR theorem is structurally incomplete",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "requirement_id": "NPC2707_6_verdict",
            "requirement": "all no-pole certificate clauses close in one parent branch",
            "needed_for": "C_X=0 and local-GR route",
            "current_status": "CERTIFICATE_NOT_CLOSED",
            "source_hint": "NPR2106_3_required_certificate",
            "if_missing": "finite local Xhat branch remains closure-only, not evidence",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def closure_demotion_rows() -> list[dict[str, Any]]:
    return [
        {
            "demotion_id": "CD2707_0_object",
            "object": "finite local Xhat pole branch",
            "demoted_to": "explicit closure/diagnostic input",
            "reason": "no parent Xhat owner, same-variable lock, Hessian values, source current, or zero factor was extracted",
            "still_useful_for": "organizing algebra, source-row schema, future runners and no-cancellation guards",
            "not_allowed_for": "local GR/Newton claim; R10/PPN/clock/orbital evidence; public claim",
            "reentry_condition": "parent action signs no-pole/source-zero certificate or provides one real coefficient row with units",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "demotion_id": "CD2707_1_allowed_language",
            "object": "C_X formula",
            "demoted_to": "conditional contract",
            "reason": "product law is exact but factors are not owned",
            "still_useful_for": "checking any future parent row against correct normalization",
            "not_allowed_for": "numeric alpha(lambda) prediction",
            "reentry_condition": "Z_X, M_X^2, s_X, Qbar_XH, qbar_XT and tau/projection become sourced or one zero factor closes",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "demotion_id": "CD2707_2_primary_route_after_demotion",
            "object": "next local-GR attempt",
            "demoted_to": "not demoted; rerouted",
            "reason": "the stronger derivational route is quotient no-pole/source-zero, not fitted finite residuals",
            "still_useful_for": "attempting GR-like reduction without small-parameter tuning",
            "not_allowed_for": "declaring success before certificate clauses close",
            "reentry_condition": "2708 certificate closes or names the irreducible closure axiom precisely",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_gate_id": "CG2707_0_owner",
            "gate": "parent action owner extracted",
            "status": "FAIL_NO_OWNER_EXTRACTED",
            "gate_passed": "false",
            "claim_allowed": "false",
            "reason": "Xhat owner and same-variable lock remain unsigned",
            "timestamp_utc": stamp(),
        },
        {
            "claim_gate_id": "CG2707_1_coefficient",
            "gate": "one C_X coefficient is zero/numeric source-backed",
            "status": "FAIL_NO_COEFFICIENT_PROMOTED",
            "gate_passed": "false",
            "claim_allowed": "false",
            "reason": "all coefficient slots remain closure/conditional/nonclaim",
            "timestamp_utc": stamp(),
        },
        {
            "claim_gate_id": "CG2707_2_no_pole",
            "gate": "no physical X pole theorem",
            "status": "BLOCKED_CERTIFICATE_MISSING",
            "gate_passed": "false",
            "claim_allowed": "false",
            "reason": "q-map/action descent/degree count/boundary/matter clauses not closed together",
            "timestamp_utc": stamp(),
        },
        {
            "claim_gate_id": "CG2707_3_closure_demotion",
            "gate": "finite local branch demoted to closure-only",
            "status": "PASS_NONCLAIM_DISCIPLINE",
            "gate_passed": "true",
            "claim_allowed": "false",
            "reason": "demotion prevents branch mixing and overclaiming",
            "timestamp_utc": stamp(),
        },
        {
            "claim_gate_id": "CG2707_4_private",
            "gate": "GitHub/public action",
            "status": "PRIVATE_NO_ACTION",
            "gate_passed": "false",
            "claim_allowed": "false",
            "reason": "private checkpoint only",
            "timestamp_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2707_0_extraction",
            "decision": "NO_PARENT_OWNER_EXTRACTED",
            "rationale": "the current corpus contains exact contracts but no parent action signs Xhat as the field with one normalization across Hessian/source/readout",
            "next_action": "stop treating the finite Xhat pole branch as derivation-grade",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2707_1_demotion",
            "decision": "FINITE_LOCAL_XHAT_BRANCH_DEMOTED_TO_CLOSURE_INPUT",
            "rationale": "without parent owner or coefficient row, finite alpha/local residual rows are useful scaffolding only",
            "next_action": "only re-enter finite scoring after a parent-signed coefficient row or zero factor exists",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2707_2_primary_route",
            "decision": "QUOTIENT_NO_POLE_SOURCE_ZERO_ROUTE_SELECTED_NEXT",
            "rationale": "this is the route that would reduce to GR/Newton structurally rather than by small fitted couplings",
            "next_action": "build the no-pole certificate with q-map, action descent, degree count, matter descent and boundary silence",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2707_0_selected",
            "selection": "selected_primary",
            "target_doc": "2708-Y5-R2FR-parent-quotient-no-pole-certificate-or-closure-reentry.md",
            "target_script": "scripts/Y5_R2FR_parent_quotient_no_pole_certificate_or_closure_reentry_2708.py",
            "task": "try to assemble the parent quotient no-pole/source-zero certificate: q-map, v_X in ker(Dq), action descent/degeneracy, degree count, matter MOMS signature, boundary silence, and no hidden tails; if it fails, write the exact closure axiom needed for local GR re-entry",
            "success_condition": "C_X=0 becomes parent-signed through no-pole/source-zero, or the local finite branch remains closure-only with a precise re-entry axiom rather than hidden claim language",
            "forbidden_shortcuts": "borrow representative zero as observed zero; use finite Xhat closure coefficients as evidence; fit local bounds; GitHub action; formalization-workbench edits",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STATUS2707_0_parent_owner",
            "topic": "parent action owner",
            "status": "NOT_EXTRACTED",
            "meaning": "Xhat is not currently derivation-grade as either physical pole or gauge/no-pole theorem",
            "next_action": "no-pole certificate attempt",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "STATUS2707_1_finite_branch",
            "topic": "finite local branch",
            "status": "CLOSURE_ONLY",
            "meaning": "useful private scaffold, not local-GR evidence",
            "next_action": "re-enter only by parent coefficient or zero theorem",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "STATUS2707_2_GR_Newton_route",
            "topic": "GR/Newton reduction",
            "status": "QUOTIENT_NO_POLE_ROUTE_SELECTED",
            "meaning": "the best route is structural silence of the extra local pole, not tuning a tiny fifth force",
            "next_action": "2708 no-pole/source-zero certificate",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "STATUS2707_3_private",
            "topic": "public/GitHub",
            "status": "NO_ACTION_PRIVATE",
            "meaning": "all outputs remain private under post-checkpoint-work",
            "next_action": "keep private",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": key,
            "path": str(path),
            "relative_path": str(path.relative_to(ROOT)),
            "exists_after_run": as_bool(path.exists()),
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
        for key, path in BRANCH_OUTPUTS.items()
    ]


def validate(generated_paths: dict[str, Path], rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "passed": as_bool(passed), "detail": detail, "timestamp_utc": stamp()})

    sources = rows_by_name["source_register"]
    add("VAL2707_0_sources_exist", all(row["exists"] == "true" for row in sources), "all cited local source paths exist")
    add("VAL2707_1_needles_found", all(not row["missing_needles"] for row in sources), "all required source needles were found")

    owner = rows_by_name["owner_extraction"]
    add("VAL2707_2_owner_not_extracted_recorded", any(row["owner_id"] == "OWN2707_6_verdict" and row["promotion_result"] == "DEMOTE_FINITE_LOCAL_XHAT_BRANCH_TO_CLOSURE_INPUT" for row in owner), "owner extraction verdict records closure demotion")
    add("VAL2707_3_no_owner_claim", all(row["valid_for_claim"] == "false" for row in owner), "no owner row is claim-grade")

    trilemma = rows_by_name["branch_trilemma"]
    add("VAL2707_4_trilemma_has_closure", any(row["branch_id"] == "TRI2707_C_closure_ansatz" and row["selected_now"] == "true" for row in trilemma), "closure branch is explicitly selected for current finite local branch")
    add("VAL2707_5_no_forbidden_hybrid", any(row["branch_id"] == "TRI2707_D_inconsistent_hybrid_guard" and row["current_status"] == "REJECTED" for row in trilemma), "forbidden hybrid branch rejected")

    coeffs = rows_by_name["coefficient_audit"]
    add("VAL2707_6_no_coeff_promoted", all(row["valid_for_claim"] == "false" and row["answer"] in {"no", "conditional only"} for row in coeffs), "no coefficient is promoted")
    add("VAL2707_7_CX_demoted", any(row["quantity"] == "C_X product" and "DEMOTED" in row["status_after_2707"] for row in coeffs), "C_X finite branch demotion recorded")

    no_pole = rows_by_name["no_pole_requirements"]
    add("VAL2707_8_no_pole_requirements_complete", len(no_pole) >= 7 and any(row["requirement_id"] == "NPC2707_6_verdict" for row in no_pole), "no-pole certificate requirement list includes verdict row")
    add("VAL2707_9_no_pole_not_claimed", all(row["valid_for_claim"] == "false" for row in no_pole), "no-pole certificate remains nonclaim")

    closure = rows_by_name["closure_demotion"]
    add("VAL2707_10_closure_demotion_pass", any(row["demotion_id"] == "CD2707_0_object" and row["demoted_to"] == "explicit closure/diagnostic input" for row in closure), "finite local Xhat branch demoted to explicit closure")
    add("VAL2707_11_claims_blocked", all(row["claim_allowed"] == "false" for row in rows_by_name["claim_gates"]), "all claim gates keep claim_allowed=false")
    add("VAL2707_12_next_2708", any(row["next_id"] == "NEXT2707_0_selected" and "2708" in row["target_doc"] for row in rows_by_name["next_target"]), "2708 target selected")
    add("VAL2707_13_no_formalization_outputs", not any("formalization-workbench" in str(path).lower() for path in generated_paths.values()), "no output path points into formalization-workbench")
    add("VAL2707_14_no_github_outputs", not any(".git" in str(path).lower() or "github" in str(path).lower() for path in generated_paths.values()), "no GitHub/public-output path was written")

    for key, path in generated_paths.items():
        ok, count, detail = parse_csv(path)
        add(f"VAL2707_PARSE_{key}", ok and count > 0, f"{detail}; rows={count}")

    core = [row for row in rows if not row["check_id"].startswith("VAL2707_PARSE_validation")]
    add(
        "VAL2707_OVERALL",
        all(row["passed"] == "true" for row in core),
        "2707 fails to extract a parent coefficient owner, demotes the finite local Xhat branch to explicit closure-only status, and selects the quotient no-pole/source-zero certificate for 2708",
    )
    return rows


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        ("Parent Owner Extraction Matrix", rows_by_name["owner_extraction"]),
        ("Exclusive Branch Trilemma", rows_by_name["branch_trilemma"]),
        ("Coefficient Promotion Audit", rows_by_name["coefficient_audit"]),
        ("No-Pole Certificate Requirements", rows_by_name["no_pole_requirements"]),
        ("Closure Demotion Ledger", rows_by_name["closure_demotion"]),
        ("Source Register", rows_by_name["source_register"]),
        ("Claim Gates", rows_by_name["claim_gates"]),
        ("Decisions", rows_by_name["decision_ledger"]),
        ("Next Target", rows_by_name["next_target"]),
        ("Project Status", rows_by_name["project_status"]),
        ("Validation", rows_by_name["validation"]),
    ]
    lines = [
        "# 2707: Parent Action Coefficient Owner Extraction",
        "",
        f"**Branch:** `{BRANCH_ID}`",
        "",
        "## Private Verdict",
        "",
        "2707 tries the leap forward rather than circling the coupling wall. The result is strict: the current corpus does not extract a parent-action owner for `Xhat`, does not parent-sign `Z_X`, `M_X^2`, `s_X`, `Qbar_XH`, or `qbar_XT`, and does not prove a no-physical-pole theorem. Therefore the finite local `Xhat` pole branch is demoted to an explicit closure/diagnostic input. That is useful progress: it stops us mixing a physical-pole Hessian, a quotient-zero argument, and closure coefficients as if they were one parent derivation.",
        "",
        "## Bottom Line",
        "",
        "- `C_X` remains an exact conditional product, not a prediction.",
        "- The finite local `Xhat` pole branch is closure-only until a parent owner or real coefficient row appears.",
        "- The best GR/Newton route is now the quotient no-pole/source-zero certificate.",
        "- 2708 should try to prove that certificate, or write the exact closure axiom needed for re-entry.",
        "",
    ]
    for title, rows in sections:
        lines.extend([f"## {title}", "", markdown_table(rows), ""])
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "owner_extraction": owner_extraction_rows(),
        "branch_trilemma": branch_trilemma_rows(),
        "coefficient_audit": coefficient_audit_rows(),
        "no_pole_requirements": no_pole_requirement_rows(),
        "closure_demotion": closure_demotion_rows(),
        "claim_gates": claim_gate_rows(),
        "decision_ledger": decision_rows(),
        "next_target": next_target_rows(),
        "project_status": project_status_rows(),
    }

    for name, path in OUTPUTS.items():
        if name in {"validation", "branch_copies"}:
            continue
        write_csv(path, rows_by_name[name])

    write_csv(BRANCH_OUTPUTS["local_closure_demotion"], rows_by_name["closure_demotion"])
    write_csv(BRANCH_OUTPUTS["local_no_pole_requirements"], rows_by_name["no_pole_requirements"])
    write_csv(BRANCH_OUTPUTS["source_weight_owner_matrix"], rows_by_name["owner_extraction"])
    write_csv(BRANCH_OUTPUTS["rab_next"], rows_by_name["next_target"])

    branch_rows = branch_copy_rows()
    rows_by_name["branch_copies"] = branch_rows
    write_csv(OUTPUTS["branch_copies"], branch_rows)

    generated_paths = {name: path for name, path in OUTPUTS.items() if name != "validation"}
    generated_paths.update(BRANCH_OUTPUTS)
    validation = validate(generated_paths, rows_by_name)
    rows_by_name["validation"] = validation
    write_csv(OUTPUTS["validation"], validation)

    write_doc(rows_by_name)
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

BRANCH_ID = "MTS_R2FR_Q_SECTOR_PARENT_COEFFICIENT_EXTRACTION_OR_SELECTOR_FORK_2287"
START_TS = datetime.now(timezone.utc).timestamp()
DOC = ROOT / "2287-Y5-R2FR-q-sector-parent-coefficient-extraction-or-selector-fork.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2287_00_2286_doc",
        "source_key": "2286_handoff",
        "source_path": ROOT / "2286-Y5-R2FR-parent-weak-field-Mq-jq-delta-beta-source-or-zero-theorem.md",
        "needles": [
            "Q_SECTOR_COEFFICIENT_EXTRACTION_OR_SELECTOR_FORK_NEXT",
            "q_R=j_q/M_q^2",
            "FORK2286_0_constraint_zero",
        ],
        "role": "current handoff: q-sector route selection after weak-field normal form",
    },
    {
        "source_id": "SRC2287_01_2286_validation",
        "source_key": "2286_validation",
        "source_path": OUT / "P8_Y5_BRR545_2286_VALIDATION.csv",
        "needles": ["VAL2286_OVERALL", "PASS"],
        "role": "confirms 2286 passed before 2287",
    },
    {
        "source_id": "SRC2287_02_2286_normal_form",
        "source_key": "2286_normal_form",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2286_WEAK_FIELD_NORMAL_FORM.csv",
        "needles": ["NF2286_1_algebraic_q_sector", "NF2286_3_gradient_hair_sector", "NF2286_4_beta_completion"],
        "role": "defines algebraic, gradient/hair, and beta-completion lanes",
    },
    {
        "source_id": "SRC2287_03_2286_coefficients",
        "source_key": "2286_coefficient_slots",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2286_MQ_JQ_COEFFICIENT_DEFINITIONS.csv",
        "needles": ["COEF2286_0_Mq2", "COEF2286_1_jq", "COEF2286_3_Zq"],
        "role": "missing M_q^2, j_q, Z_q, boundary and beta slots",
    },
    {
        "source_id": "SRC2287_04_2286_forks",
        "source_key": "2286_zero_finite_forks",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2286_ZERO_OR_FINITE_FORK_LEDGER.csv",
        "needles": ["FORK2286_0_constraint_zero", "FORK2286_1_algebraic_finite", "FORK2286_2_massive_range"],
        "role": "formal fork ledger for selecting constraint, algebraic finite, or gradient/massive route",
    },
    {
        "source_id": "SRC2287_05_1257_selector",
        "source_key": "1257_selector_clauses",
        "source_path": OUT / "P8_Y5_R10_1257_ZR_LAMBDAR_SELECTOR_CLAUSES.csv",
        "needles": ["SEL1257_0_field_exclusion", "SEL1257_2_generic_field_rule", "SEL1257_3_mass_gap_silence"],
        "role": "older selector logic for Z_R=0 versus finite residual branch",
    },
    {
        "source_id": "SRC2287_06_1257_routes",
        "source_key": "1257_branch_routes",
        "source_path": OUT / "P8_Y5_R10_1257_BRANCH_ROUTING_LEDGER.csv",
        "needles": ["ROUTE1257_0_clean_zero", "ROUTE1257_2_massive_suppression", "KEPT_OPEN"],
        "role": "shows clean zero not selected and finite/massive routes kept open",
    },
    {
        "source_id": "SRC2287_07_2235_origin",
        "source_key": "2235_lambdaR_origin",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2235_LAMBDAR_ORIGIN_AUDIT.csv",
        "needles": ["ORG2235_3_second_class_auxiliary", "BEST_CONDITIONAL_ROUTE", "ORG2235_4_kinetic_RAB"],
        "role": "auxiliary compatibility is the best conditional zero route but not parent-signed",
    },
    {
        "source_id": "SRC2287_08_2235_stress",
        "source_key": "2235_zero_stress",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2235_ZERO_STRESS_VARIATION_GATE.csv",
        "needles": ["STR2235_1_multiplier_metric_stress", "FAIL_UNSIGNED", "STR2235_3_no_derivative"],
        "role": "zero-stress and no-derivative gates remain unsigned",
    },
    {
        "source_id": "SRC2287_09_2236_auxiliary",
        "source_key": "2236_auxiliary_grammar",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2236_NO_DERIVATIVE_GRAMMAR_GATE.csv",
        "needles": ["GRAM2236_0_no_DRAB", "GRAM2236_5_verdict", "FAIL_CURRENT_THEOREM"],
        "role": "no-derivative grammar exists as exact conditional but not as parent theorem",
    },
    {
        "source_id": "SRC2287_10_2236_validation",
        "source_key": "2236_validation",
        "source_path": OUT / "P8_Y5_BRR545_2236_VALIDATION.csv",
        "needles": ["VAL2236_OVERALL", "PASS"],
        "role": "confirms auxiliary grammar checkpoint passed as nonclaim",
    },
    {
        "source_id": "SRC2287_11_2237_null",
        "source_key": "2237_vertical_null",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2237_PRESYMPLECTIC_NULL_CHAIN.csv",
        "needles": ["NULL2237_0_parent_L_theta", "NULL2237_3_vR_generator", "CONDITIONAL_CONTRADICTION_WRITTEN_NOT_PARENT_PROVED"],
        "role": "vertical-null route can forbid Z_R only if parent theta/Omega/v_R are supplied",
    },
    {
        "source_id": "SRC2287_12_2237_kinetic",
        "source_key": "2237_kinetic_contradiction",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2237_KINETIC_TERM_CONTRADICTION.csv",
        "needles": ["KIN2237_1_null_contradiction", "KIN2237_2_escape_physical", "COUNTERMODEL_FORCES_FALLBACK"],
        "role": "exact conditional contradiction and finite-branch escape routes",
    },
    {
        "source_id": "SRC2287_13_2237_validation",
        "source_key": "2237_validation",
        "source_path": OUT / "P8_Y5_BRR545_2237_VALIDATION.csv",
        "needles": ["VAL2237_OVERALL", "PASS"],
        "role": "confirms vertical-null checkpoint passed as nonclaim",
    },
    {
        "source_id": "SRC2287_14_1256_coefficients",
        "source_key": "1256_coefficient_requirements",
        "source_path": OUT / "P8_Y5_R10_1256_COEFFICIENT_REQUIREMENTS.csv",
        "needles": ["COEF1256_0_ZR", "COEF1256_1_MR2", "COEF1256_3_JR"],
        "role": "legacy coefficient requirements for Z_R/M_R^2/J_R/B_R",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2287_SOURCE_REGISTER.csv",
    "selector_audit": OUT / "P8_Y5_PARENT_QLOC_2287_Q_SECTOR_SELECTOR_AUDIT.csv",
    "coefficient_attempt": OUT / "P8_Y5_PARENT_QLOC_2287_COEFFICIENT_EXTRACTION_ATTEMPT.csv",
    "route_scorecard": OUT / "P8_Y5_PARENT_QLOC_2287_ROUTE_SCORECARD_NONCLAIM.csv",
    "beta_backreaction": OUT / "P8_Y5_PARENT_QLOC_2287_DELTA_BETA_BACKREACTION_LEDGER.csv",
    "missing_primitives": OUT / "P8_Y5_PARENT_QLOC_2287_MISSING_PARENT_PRIMITIVES.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2287_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2287_REFUSAL_RUNNER.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2287_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2287_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2287_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2287_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_selector": (OUTPUTS["selector_audit"], QUEUE / "JR2287_Q_SECTOR_SELECTOR_AUDIT_NONCLAIM.csv"),
    "queue_coefficients": (OUTPUTS["coefficient_attempt"], QUEUE / "JR2287_COEFFICIENT_EXTRACTION_ATTEMPT_NONCLAIM.csv"),
    "branch_wep_refusal": (OUTPUTS["refusal"], MICROSCOPE / "RAB_q_sector_selector_refusal_2287.csv"),
    "beta_docs": (OUTPUTS["beta_backreaction"], BETA_DOCS / "RAB_Q_SECTOR_SELECTOR_2287_NONCLAIM.csv"),
}


def stringify(value: Any) -> str:
    if isinstance(value, bool):
        return "True" if value else "False"
    return str(value)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow({key: stringify(value) for key, value in row.items()})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def validation_pass(path: Path) -> bool:
    if not path.exists() or not csv_parses(path):
        return False
    rows = read_csv(path)
    if not rows:
        return False
    id_key = "check_id" if "check_id" in rows[0] else "validation_id"
    result_key = "result" if "result" in rows[0] else "status"
    overall_rows = [row for row in rows if "overall" in row.get(id_key, "").lower()]
    if overall_rows:
        return all(row.get(result_key, "").upper() == "PASS" for row in overall_rows)
    return all(row.get(result_key, "").upper() == "PASS" for row in rows)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def ignored_environment_path(path: Path) -> bool:
    ignored_parts = {".venv", ".venv-score", "__pycache__", "site-packages", ".git"}
    return any(part in ignored_parts for part in path.parts)


def formalization_has_2287_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    for candidate in FORMALIZATION.rglob("*2287*"):
        if candidate.is_file() and not ignored_environment_path(candidate.relative_to(FORMALIZATION)):
            return True
    return False


def formalization_touched_since_start() -> bool:
    if not FORMALIZATION.exists():
        return False
    for candidate in FORMALIZATION.rglob("*"):
        if candidate.is_file() and not ignored_environment_path(candidate.relative_to(FORMALIZATION)):
            if candidate.stat().st_mtime >= START_TS:
                return True
    return False


def table(headers: list[str], rows: list[dict[str, Any]]) -> str:
    def cell(value: Any) -> str:
        return stringify(value).replace("\n", " ").replace("|", "\\|")

    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        source_path = Path(source["source_path"])
        source_text = read_text(source_path)
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": source_path,
                "exists": source_path.exists(),
                "needles": "; ".join(needles),
                "needles_present": all(needle in source_text for needle in needles),
                "role": source["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def selector_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "selector_id": "SEL2287_0_constraint_zero",
            "route": "constraint_zero",
            "route_condition": "q=R_AB is parent-owned auxiliary/compatibility data and Lambda_R is a parent reaction variable",
            "needed_parent_clause": "typed parent sort; no independent q variation as physical scalar; parent-owned Lambda_R; zero stress; boundary silence; readout stability",
            "mathematical_result_if_signed": "delta_Lambda S=0 gives q=0, hence q_R=0 before PPN projection",
            "current_evidence": "2235/2236 make this the best zero route, but only conditionally",
            "current_status": "BEST_ZERO_ROUTE_UNSIGNED",
            "route_selected_for_claim": False,
            "valid_for_claim": False,
        },
        {
            "selector_id": "SEL2287_1_auxiliary_no_derivative",
            "route": "auxiliary_compatibility_no_derivative",
            "route_condition": "R_AB-C_AB[q(Phi),theta,top]=0 is algebraic compatibility data and D R_AB/D Lambda_R operators are forbidden",
            "needed_parent_clause": "object-language no-derivative grammar or vertical-null/no-vertical-metric theorem",
            "mathematical_result_if_signed": "Z_q=0 and no exterior Pi_q/Q_R hair",
            "current_evidence": "2236 no-derivative grammar and 2237 vertical-null contradiction are exact conditional, not parent-signed",
            "current_status": "BEST_CONDITIONAL_ROUTE_NOT_SELECTED",
            "route_selected_for_claim": False,
            "valid_for_claim": False,
        },
        {
            "selector_id": "SEL2287_2_algebraic_finite",
            "route": "algebraic_finite",
            "route_condition": "q is algebraic but not constrained to zero; no gradient/boundary hair survives",
            "needed_parent_clause": "M_q^2>0 and j_q sourced in the same weak-field normalization; no Dq or boundary charge",
            "mathematical_result_if_signed": "q_R=j_q/M_q^2 and q_R=0 iff j_q=0 with M_q^2>0",
            "current_evidence": "2286 derives the normal form but not the parent coefficients",
            "current_status": "FORMAL_NORMAL_FORM_INPUTS_MISSING",
            "route_selected_for_claim": False,
            "valid_for_claim": False,
        },
        {
            "selector_id": "SEL2287_3_gradient_massive",
            "route": "gradient_massive",
            "route_condition": "q/R_AB is an independent local strain/scalar with allowed kinetic term and positive local Hessian",
            "needed_parent_clause": "Z_q, M_q^2, J_q, boundary class, and lambda_q=sqrt(Z_q/M_q^2) in source-backed units",
            "mathematical_result_if_signed": "finite range or Yukawa-suppressed q profile becomes testable against R10/PPN/clock/orbital arenas",
            "current_evidence": "1257/2237 keep the finite branch open whenever physical or vertical-metric countermodels survive",
            "current_status": "FINITE_BRANCH_RETAINED_NOT_SCOREABLE",
            "route_selected_for_claim": False,
            "valid_for_claim": False,
        },
        {
            "selector_id": "SEL2287_4_boundary_nohair",
            "route": "boundary_nohair",
            "route_condition": "bulk q may exist but physical source worldtubes and corners carry no Pi_q/Q_R hair",
            "needed_parent_clause": "boundary variational class; Hamiltonian differentiability; source-worldtube no-flux theorem",
            "mathematical_result_if_signed": "local exterior q source can vanish even without global Z_q=0",
            "current_evidence": "boundary/no-hair appears repeatedly as required but not derived",
            "current_status": "BOUNDARY_CLASS_MISSING",
            "route_selected_for_claim": False,
            "valid_for_claim": False,
        },
    ]


def coefficient_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "coefficient_id": "COEF2287_0_Mq2",
            "symbol": "M_q^2",
            "extraction_target": "second q variation of the local parent weak-field density",
            "candidate_source": "2286 normal form plus 1256 M_R^2 requirement",
            "attempt_result": "NOT_EXTRACTED",
            "blocker": "no parent Hessian around local vacuum in current source chain",
            "numeric_value_present": False,
            "source_backed": False,
            "parent_prediction_ready": False,
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "COEF2287_1_jq",
            "symbol": "j_q",
            "extraction_target": "mixed q/source coefficient in J_q=j_q L+j_q2 L^2+O(L^3)",
            "candidate_source": "matter descent/source-current map",
            "attempt_result": "NOT_EXTRACTED",
            "blocker": "matter q-current and source normalization are not parent-signed",
            "numeric_value_present": False,
            "source_backed": False,
            "parent_prediction_ready": False,
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "COEF2287_2_qR",
            "symbol": "q_R",
            "extraction_target": "local first-order PPN residual coefficient q=q_R L+O(L^2)",
            "candidate_source": "q_R=j_q/M_q^2 or signed constraint/no-source theorem",
            "attempt_result": "NOT_EXTRACTED",
            "blocker": "neither coefficient ratio nor zero theorem is source-backed",
            "numeric_value_present": False,
            "source_backed": False,
            "parent_prediction_ready": False,
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "COEF2287_3_Zq",
            "symbol": "Z_q",
            "extraction_target": "gradient coefficient for q/R_AB if it propagates or has finite range",
            "candidate_source": "operator inventory of parent q sector or vertical-null theorem-zero",
            "attempt_result": "NOT_EXTRACTED",
            "blocker": "no derivative grammar is conditional; no finite coefficient row accepted",
            "numeric_value_present": False,
            "source_backed": False,
            "parent_prediction_ready": False,
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "COEF2287_4_MR2",
            "symbol": "M_R^2 or M_q^2",
            "extraction_target": "positive local Hessian/mass gap for finite-range suppression",
            "candidate_source": "1256/2286 coefficient requirement rows",
            "attempt_result": "NOT_EXTRACTED",
            "blocker": "no parent potential or second variation coefficient with units",
            "numeric_value_present": False,
            "source_backed": False,
            "parent_prediction_ready": False,
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "COEF2287_5_JR",
            "symbol": "J_R or J_q",
            "extraction_target": "matter/source coupling to reciprocal q sector",
            "candidate_source": "matter descent and source-current map",
            "attempt_result": "NOT_EXTRACTED",
            "blocker": "source current owner and matter descent remain unsigned",
            "numeric_value_present": False,
            "source_backed": False,
            "parent_prediction_ready": False,
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "COEF2287_6_BR",
            "symbol": "B_R, Pi_q, Q_R",
            "extraction_target": "boundary flux/hair coefficient for local exterior q profile",
            "candidate_source": "Hamiltonian boundary variation and source worldtube class",
            "attempt_result": "NOT_EXTRACTED",
            "blocker": "boundary/corner no-hair class is not sourced",
            "numeric_value_present": False,
            "source_backed": False,
            "parent_prediction_ready": False,
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "COEF2287_7_LambdaR",
            "symbol": "Lambda_R",
            "extraction_target": "parent-owned reaction/multiplier variable enforcing q=0 or compatibility",
            "candidate_source": "2235/2236 auxiliary route",
            "attempt_result": "CONDITIONAL_ONLY",
            "blocker": "parent sort and zero-stress theorem remain unsigned",
            "numeric_value_present": False,
            "source_backed": False,
            "parent_prediction_ready": False,
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def route_scorecard_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "ROUTE2287_0_constraint_zero",
            "route": "constraint_zero",
            "strength": "best route for exact local GR if signed",
            "weakness": "requires parent-owned Lambda_R, auxiliary sort, zero-stress, no boundary hair, and readout stability",
            "decision": "KEEP_AS_PRIMARY_DERIVATION_TARGET_UNSIGNED",
            "next_action": "try to prove R_AB auxiliary parent sort/no-derivative grammar from parent object language",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "route_id": "ROUTE2287_1_algebraic_finite",
            "route": "algebraic_finite",
            "strength": "gives clean q_R=j_q/M_q^2 prediction if coefficients can be sourced",
            "weakness": "M_q^2 and j_q are both missing and no-gradient/no-boundary conditions still required",
            "decision": "RETAIN_AS_SCOREABLE_FALLBACK_INPUTS_MISSING",
            "next_action": "stage coefficient intake only after parent Hessian and source-current map exist",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "route_id": "ROUTE2287_2_gradient_massive",
            "route": "gradient_massive",
            "strength": "least hand-wavy if q is genuinely physical; can be bounded by R10/PPN/clock/orbital arenas",
            "weakness": "would demote exact local-GR derivation to finite residual control unless mass/no-flux suppression is proven",
            "decision": "RETAIN_AS_NONCLAIM_BOUND_BRANCH",
            "next_action": "source Z_q, M_q^2, J_q, B_R and lambda_q before any scoring",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "route_id": "ROUTE2287_3_boundary_nohair",
            "route": "boundary_nohair",
            "strength": "could protect local exterior without needing global q elimination",
            "weakness": "boundary differentiability and physical source-worldtube class are unsourced",
            "decision": "RETAIN_AS_SUBGATE_NOT_ROUTE_SELECTION",
            "next_action": "tie no-hair to Hamiltonian boundary charge or source-worldtube theorem",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "route_id": "ROUTE2287_4_beta_completion",
            "route": "second_order_beta_backreaction",
            "strength": "keeps GR/Newton reduction honest by not confusing gamma/q_R with beta",
            "weakness": "requires O(L^2) parent variation and PPN gauge/source/readout map",
            "decision": "CARRY_FORWARD_NONCLAIM",
            "next_action": "after q-sector route selection, derive or bound beta backreaction terms",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def beta_backreaction_rows() -> list[dict[str, Any]]:
    return [
        {
            "beta_id": "BETA2287_0_definition_guard",
            "term_or_gate": "delta_beta",
            "source_in_q_sector": "beta_parent-1 only after declared PPN gauge, source normalization, and observed metric/coframe readout",
            "effect": "prevents beta=1 claim from closure Schwarzschild or from q_R=0 alone",
            "required_inputs": "O(L^2) parent equation; Ward/Bianchi identity; PPN coordinate/readout map",
            "current_status": "GUARD_ACTIVE_INPUTS_MISSING",
            "valid_for_claim": False,
        },
        {
            "beta_id": "BETA2287_1_jq2",
            "term_or_gate": "j_q2/M_q^2",
            "source_in_q_sector": "second source leg J_q=j_q L+j_q2 L^2+...",
            "effect": "can shift q at O(L^2) and feed beta-like readout",
            "required_inputs": "j_q2 and M_q^2 in same parent normalization",
            "current_status": "MISSING_PARENT_COEFFICIENTS",
            "valid_for_claim": False,
        },
        {
            "beta_id": "BETA2287_2_q2_self_interaction",
            "term_or_gate": "q^2 and qL operators",
            "source_in_q_sector": "quadratic/cubic q-sector parent density",
            "effect": "finite q_R can backreact into second-order metric/coframe coefficients",
            "required_inputs": "parent Hessian/cubic terms plus projection into observed PPN metric",
            "current_status": "MISSING_PARENT_OPERATOR_INVENTORY",
            "valid_for_claim": False,
        },
        {
            "beta_id": "BETA2287_3_source_normalization",
            "term_or_gate": "delta_GM or epsilon_mu_extra",
            "source_in_q_sector": "Pi_M/Hilbert/worldtube mismatch or reference-current residual",
            "effect": "can imitate beta/gamma shifts even if raw q equation is controlled",
            "required_inputs": "source normalization and mass-current equality theorem",
            "current_status": "RETAINED_UNFILLED_SOURCE_NORMALIZATION_VECTOR",
            "valid_for_claim": False,
        },
        {
            "beta_id": "BETA2287_4_constraint_route",
            "term_or_gate": "auxiliary q=0 route",
            "source_in_q_sector": "if q is eliminated algebraically before readout",
            "effect": "removes direct q_R contribution but does not by itself prove beta=1",
            "required_inputs": "EH/operator selection plus O(L^2) parent variation",
            "current_status": "ZERO_Q_NOT_ZERO_BETA",
            "valid_for_claim": False,
        },
    ]


def missing_parent_primitive_rows() -> list[dict[str, Any]]:
    return [
        {
            "missing_id": "MISS2287_0_parent_field_sort",
            "primitive": "typed parent field/sort list",
            "needed_for": "deciding whether R_AB/q is auxiliary compatibility data or physical local field",
            "status": "MISSING_PARENT_INPUT",
            "blocks": "constraint_zero; no-derivative grammar; finite branch selection",
            "valid_for_claim": False,
        },
        {
            "missing_id": "MISS2287_1_parent_object_language",
            "primitive": "operator grammar forbidding or allowing Dq/DLambda/vertical metrics",
            "needed_for": "Z_q=0 proof or finite Z_q intake",
            "status": "MISSING_PARENT_INPUT",
            "blocks": "auxiliary_no_derivative; gradient_massive route decision",
            "valid_for_claim": False,
        },
        {
            "missing_id": "MISS2287_2_parent_Hessian",
            "primitive": "local q-sector Hessian M_q^2",
            "needed_for": "algebraic q_R ratio or massive range lambda_q",
            "status": "MISSING_PARENT_INPUT",
            "blocks": "algebraic_finite; gradient_massive; R10/PPN scoring",
            "valid_for_claim": False,
        },
        {
            "missing_id": "MISS2287_3_matter_descent",
            "primitive": "matter/source q-current J_q and no-source theorem",
            "needed_for": "j_q extraction or q-source zero theorem",
            "status": "MISSING_PARENT_INPUT",
            "blocks": "q_R prediction; WEP/source consistency; local-GR claim",
            "valid_for_claim": False,
        },
        {
            "missing_id": "MISS2287_4_boundary_class",
            "primitive": "Pi_q/Q_R/B_R source-worldtube and corner class",
            "needed_for": "no exterior q hair or finite boundary flux normalization",
            "status": "MISSING_ARENA_PROJECTION",
            "blocks": "boundary_nohair; R10/local PPN profile",
            "valid_for_claim": False,
        },
        {
            "missing_id": "MISS2287_5_parent_theta_omega_vR",
            "primitive": "theta_MTS/Omega_parent and R_AB vertical generator v_R",
            "needed_for": "presymplectic-null proof that forbids kinetic q terms",
            "status": "MISSING_PARENT_INPUT",
            "blocks": "vertical-null Z_q=0 theorem",
            "valid_for_claim": False,
        },
        {
            "missing_id": "MISS2287_6_ppn_second_order",
            "primitive": "O(L^2) parent weak-field equation and PPN readout",
            "needed_for": "delta_beta prediction",
            "status": "MISSING_PARENT_INPUT",
            "blocks": "derived local GR/Newton claim",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "CG2287_0_sources",
            "claim": "source chain for selector audit is loaded",
            "gate_pass": True,
            "reason": "2286 plus auxiliary/vertical-null evidence are present",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2287_1_route_selected",
            "claim": "one q-sector route is selected as parent truth",
            "gate_pass": False,
            "reason": "auxiliary route is best but unsigned; finite routes retained",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2287_2_qR_prediction",
            "claim": "q_R is parent-predicted or theorem-zero",
            "gate_pass": False,
            "reason": "M_q^2/j_q ratio and constraint/no-source theorem are both missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2287_3_Zq_zero",
            "claim": "Z_q=0 by parent no-derivative/vertical-null theorem",
            "gate_pass": False,
            "reason": "no-derivative and vertical-null proofs are exact conditionals, not parent-signed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2287_4_delta_beta",
            "claim": "delta_beta is predicted or zero",
            "gate_pass": False,
            "reason": "second-order parent variation and PPN readout are missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2287_5_local_GR_Newton",
            "claim": "local GR/Newton recovery is derived",
            "gate_pass": False,
            "reason": "route selection, q_R, Z_q, boundary hair, and beta completion are incomplete",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "refusal_id": "REF2287_0_pick_zero_by_preference",
            "attempted_claim": "select constraint_zero because exact GR is desired",
            "runner_result": "REFUSED_ROUTE_PREFERENCE_NOT_DERIVATION",
            "blocked_by": "parent sort/no-derivative/zero-stress/boundary/readout premises unsigned",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2287_1_use_conditional_as_proof",
            "attempted_claim": "promote 2236/2237 exact conditional contradiction to Z_q=0",
            "runner_result": "REFUSED_CONDITIONAL_NOT_PARENT_SIGNED",
            "blocked_by": "theta/Omega/v_R and no-vertical-metric proof missing",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2287_2_score_placeholder_coefficients",
            "attempted_claim": "run R10/PPN scoring with placeholder M_q^2, j_q, Z_q, or B_R",
            "runner_result": "REFUSED_PLACEHOLDER_INPUTS",
            "blocked_by": "missing source-backed numeric rows and units",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2287_3_bounds_as_sources",
            "attempted_claim": "use experimental bounds as parent coefficient values",
            "runner_result": "REFUSED_BOUNDS_ARE_COMPARATORS",
            "blocked_by": "bounds can screen predictions but cannot define MTS parent coefficients",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2287_4_beta_shortcut",
            "attempted_claim": "claim beta=1 from q_R=0 or closure Schwarzschild lane",
            "runner_result": "REFUSED_BETA_NEEDS_SECOND_ORDER_PARENT_MAP",
            "blocked_by": "O(L^2) parent equation and source/readout map missing",
            "score_eligible": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2287_0_verdict",
            "decision": "NO_SINGLE_Q_ROUTE_SELECTED",
            "reason": "the auxiliary/no-derivative route is mathematically the cleanest local-GR route, but all parent-signing clauses remain unsigned",
            "next_action": "try to close the auxiliary parent sort/no-derivative proof before falling back to finite Z_q/M_q^2/j_q intake",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2287_1_best_route",
            "decision": "AUXILIARY_COMPATIBILITY_IS_BEST_ZERO_ROUTE_BUT_UNSIGNED",
            "reason": "it avoids smuggling a plateau axiom and would eliminate q before exterior PPN readout if parent-owned",
            "next_action": "build a stricter parent-sort/no-derivative-or-finite-Zq intake gate",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2287_2_fallback",
            "decision": "FINITE_BRANCH_RETAINED",
            "reason": "if R_AB/q is physical or vertically metrized, locality allows Z_q and the theory must predict or bound finite residuals",
            "next_action": "retain nonclaim coefficient rows for M_q^2, j_q, Z_q, J_q, B_R, lambda_q",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2287_3_claim_policy",
            "decision": "KEEP_PRIVATE_NONCLAIM",
            "reason": "2287 is a route-selection audit and blocker ledger, not a local-GR derivation",
            "next_action": "no GitHub action",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "NEXT2287_0_primary",
            "next_target": "2288-Y5-R2FR-RAB-auxiliary-parent-sort-no-derivative-or-finite-Zq-intake.md",
            "script": "scripts/Y5_R2FR_RAB_auxiliary_parent_sort_no_derivative_or_finite_Zq_intake_2288.py",
            "objective": "prove or reject R_AB/q as an auxiliary parent compatibility coordinate with no derivative operator; if the proof fails, create strict finite Z_q/M_q^2/j_q/J_q/B_R intake rows without scoring placeholders",
            "selection_status": "selected",
            "success_condition": "either parent sort/no-derivative clauses are signed strongly enough to set Z_q=0 non-ad-hoc, or finite residual coefficients are queued with all missing primitives explicit and nonclaim",
            "valid_for_claim": False,
        }
    ]


def generated_claim_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    guarded_keys = {
        "parent_prediction_ready",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "score_eligible",
        "route_selected_for_claim",
    }
    for path in paths:
        for row in read_csv(path):
            for key, value in row.items():
                if key in guarded_keys and value.strip().lower() not in false_values:
                    return False
    return True


def copy_branch_files() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for copy_id, (source_path, target_path) in COPY_TARGETS.items():
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)
        rows.append(
            {
                "copy_id": copy_id,
                "source_path": source_path,
                "target_path": target_path,
                "target_exists": target_path.exists(),
                "target_parses": csv_parses(target_path),
                "reason": "branch copy for 2287 q-sector selector and coefficient extraction checkpoint",
            }
        )
    return rows


def validation_rows(all_generated_before_validation: list[Path], branch_copy_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_rows = read_csv(OUTPUTS["source_register"])
    selector_rows = read_csv(OUTPUTS["selector_audit"])
    coefficient_rows = read_csv(OUTPUTS["coefficient_attempt"])
    scorecard_rows = read_csv(OUTPUTS["route_scorecard"])
    beta_rows = read_csv(OUTPUTS["beta_backreaction"])
    missing_rows = read_csv(OUTPUTS["missing_primitives"])
    claim_rows = read_csv(OUTPUTS["claim_gates"])
    refusal_runner_rows = read_csv(OUTPUTS["refusal"])
    decision_rows_local = read_csv(OUTPUTS["decision"])
    next_rows = read_csv(OUTPUTS["next_target"])

    routes = {row["route"] for row in selector_rows}
    coefficient_symbols = {row["symbol"] for row in coefficient_rows}
    missing_statuses = {row["status"] for row in missing_rows}
    checks = [
        ("VAL2287_0_sources_exist", all(row["exists"] == "True" for row in source_rows), "all cited source paths exist"),
        ("VAL2287_1_needles_present", all(row["needles_present"] == "True" for row in source_rows), "all cited source needles are present"),
        (
            "VAL2287_2_prior_validations",
            validation_pass(OUT / "P8_Y5_BRR545_2286_VALIDATION.csv")
            and validation_pass(OUT / "P8_Y5_BRR545_2236_VALIDATION.csv")
            and validation_pass(OUT / "P8_Y5_BRR545_2237_VALIDATION.csv"),
            "2286, 2236, and 2237 validation files pass overall",
        ),
        (
            "VAL2287_3_selector_routes_complete",
            {"constraint_zero", "auxiliary_compatibility_no_derivative", "algebraic_finite", "gradient_massive", "boundary_nohair"}.issubset(routes),
            "selector audit covers zero, auxiliary, algebraic finite, gradient/massive, and boundary no-hair routes",
        ),
        (
            "VAL2287_4_auxiliary_not_claimed",
            any(row["current_status"] == "BEST_CONDITIONAL_ROUTE_NOT_SELECTED" for row in selector_rows)
            and all(row["route_selected_for_claim"] == "False" for row in selector_rows),
            "auxiliary/no-derivative route is retained as best conditional but not selected for claim",
        ),
        (
            "VAL2287_5_coefficients_missing_nonclaim",
            {"M_q^2", "j_q", "q_R", "Z_q", "M_R^2 or M_q^2", "J_R or J_q", "B_R, Pi_q, Q_R", "Lambda_R"}.issubset(coefficient_symbols)
            and all(row["parent_prediction_ready"] == "False" and row["score_ready"] == "False" for row in coefficient_rows),
            "all q-sector coefficient slots remain explicit and nonclaim",
        ),
        (
            "VAL2287_6_finite_branch_retained",
            any(row["decision"] == "RETAIN_AS_NONCLAIM_BOUND_BRANCH" for row in scorecard_rows)
            and any(row["decision"] == "FINITE_BRANCH_RETAINED" for row in decision_rows_local),
            "finite residual branch remains retained without scoring",
        ),
        (
            "VAL2287_7_beta_backreaction_guard",
            any(row["beta_id"] == "BETA2287_4_constraint_route" and row["current_status"] == "ZERO_Q_NOT_ZERO_BETA" for row in beta_rows)
            and any(row["beta_id"] == "BETA2287_0_definition_guard" for row in beta_rows),
            "delta_beta cannot be shortcut from q_R or closure lane",
        ),
        (
            "VAL2287_8_missing_primitives_complete",
            {"MISSING_PARENT_INPUT", "MISSING_ARENA_PROJECTION"}.issubset(missing_statuses)
            and len(missing_rows) >= 7,
            "missing parent primitives and arena projections are explicitly queued",
        ),
        (
            "VAL2287_9_claim_gates_blocked",
            any(row["claim_id"] == "CG2287_5_local_GR_Newton" and row["gate_pass"] == "False" for row in claim_rows)
            and all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in claim_rows),
            "local GR/Newton and route-selection claims remain blocked",
        ),
        (
            "VAL2287_10_refusal_runner",
            {"REFUSED_ROUTE_PREFERENCE_NOT_DERIVATION", "REFUSED_CONDITIONAL_NOT_PARENT_SIGNED", "REFUSED_PLACEHOLDER_INPUTS", "REFUSED_BOUNDS_ARE_COMPARATORS"}.issubset(
                {row["runner_result"] for row in refusal_runner_rows}
            ),
            "refusal runner blocks route preference, conditional proof promotion, placeholders, and bounds-as-sources",
        ),
        (
            "VAL2287_11_next_selected",
            any(row["next_target"] == "2288-Y5-R2FR-RAB-auxiliary-parent-sort-no-derivative-or-finite-Zq-intake.md" for row in next_rows)
            and any(row["decision"] == "NO_SINGLE_Q_ROUTE_SELECTED" for row in decision_rows_local),
            "2288 auxiliary parent sort/no-derivative or finite Zq intake is selected next",
        ),
        ("VAL2287_12_csv_parse", all(csv_parses(path) for path in all_generated_before_validation), "all generated 2287 CSVs parse before validation file"),
        ("VAL2287_13_no_claim_flags", generated_claim_flags_false(all_generated_before_validation), "all generated claim/score flags remain false"),
        ("VAL2287_14_branch_copies", all(row["target_exists"] and row["target_parses"] for row in branch_copy_rows), "branch/queue copies exist and parse"),
        ("VAL2287_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL2287_16_formalization_no_2287", not formalization_has_2287_artifacts(), "formalization-workbench has no non-venv 2287 artifacts"),
        ("VAL2287_17_formalization_untouched", not formalization_touched_since_start(), "formalization-workbench untouched during 2287 run"),
    ]
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]
    overall_pass = all(row["result"] == "PASS" for row in rows)
    rows.append(
        {
            "check_id": "VAL2287_OVERALL",
            "result": "PASS" if overall_pass else "FAIL",
            "detail": "2287 refuses premature q-sector route selection, keeps auxiliary compatibility as the best unsigned zero route, retains finite residual branches, and selects 2288 no-derivative-or-finite-Zq intake next",
        }
    )
    return rows


def write_markdown(
    sources: list[dict[str, Any]],
    selector_audit: list[dict[str, Any]],
    coefficient_attempt: list[dict[str, Any]],
    route_scorecard: list[dict[str, Any]],
    beta_backreaction: list[dict[str, Any]],
    missing_primitives: list[dict[str, Any]],
    claim_gates: list[dict[str, Any]],
    refusal: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    branch_copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    content = f"""# 2287 - Y5/R2FR q-Sector Parent Coefficient Extraction or Selector Fork

## Verdict

2287 does not pick a winning q-sector route yet.

The cleanest local-GR route is still the auxiliary compatibility/no-derivative route: make `q=R_AB` parent-owned compatibility data, forbid derivative hair, and eliminate it before exterior PPN readout. If that could be parent-signed, it would give the non-ad-hoc local zero route we want.

But the parent signatures are still missing: typed field sort, no-derivative object language, zero-stress/matter descent, boundary silence, and readout stability. So this checkpoint refuses to claim `q_R=0`, `Z_q=0`, or local GR/Newton.

The finite route remains alive rather than embarrassing: if `q` is physical or vertically metrized, then the theory must source `M_q^2`, `j_q`, `Z_q`, `J_q`, and `B_R/Pi_q/Q_R`, then let R10/PPN/clock/orbital tests judge it. No placeholder coefficient is scoreable.

## Source Register
{table(["source_id", "source_key", "source_path", "exists", "needles_present", "role", "valid_for_claim"], sources)}

## q-Sector Selector Audit
{table(["selector_id", "route", "route_condition", "needed_parent_clause", "mathematical_result_if_signed", "current_evidence", "current_status", "route_selected_for_claim", "valid_for_claim"], selector_audit)}

## Coefficient Extraction Attempt
{table(["coefficient_id", "symbol", "extraction_target", "candidate_source", "attempt_result", "blocker", "numeric_value_present", "source_backed", "parent_prediction_ready", "score_ready", "valid_for_claim"], coefficient_attempt)}

## Route Scorecard
{table(["route_id", "route", "strength", "weakness", "decision", "next_action", "claim_allowed", "valid_for_claim"], route_scorecard)}

## Delta Beta Backreaction Ledger
{table(["beta_id", "term_or_gate", "source_in_q_sector", "effect", "required_inputs", "current_status", "valid_for_claim"], beta_backreaction)}

## Missing Parent Primitives
{table(["missing_id", "primitive", "needed_for", "status", "blocks", "valid_for_claim"], missing_primitives)}

## Claim Gates
{table(["claim_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"], claim_gates)}

## Refusal Runner
{table(["refusal_id", "attempted_claim", "runner_result", "blocked_by", "score_eligible", "valid_for_claim"], refusal)}

## Decision Ledger
{table(["decision_id", "decision", "reason", "next_action", "valid_for_claim"], decisions)}

## Next Target
{table(["route_id", "next_target", "script", "objective", "selection_status", "success_condition", "valid_for_claim"], next_target)}

## Branch Copies
{table(["copy_id", "source_path", "target_path", "target_exists", "target_parses", "reason"], branch_copies)}

## Validation
{table(["check_id", "result", "detail"], validation)}

## Working Interpretation

This is not circling; it is forcing the fork to confess. The theory wants the auxiliary/no-derivative route because that is how local GR becomes derivable rather than tuned. But if the parent action will not sign that, the honest fallback is finite residual physics with real coefficients and real bounds. The next checkpoint should attack exactly that hinge: either prove `R_AB/q` is auxiliary parent compatibility data, or stop asking it to vanish and build the finite `Z_q/M_q^2/j_q` intake cleanly.
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    remove_pycache()
    sources = source_register_rows()
    selector_audit = selector_audit_rows()
    coefficient_attempt = coefficient_attempt_rows()
    route_scorecard = route_scorecard_rows()
    beta_backreaction = beta_backreaction_rows()
    missing_primitives = missing_parent_primitive_rows()
    claim_gates = claim_gate_rows()
    refusal = refusal_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["selector_audit"], selector_audit)
    write_csv(OUTPUTS["coefficient_attempt"], coefficient_attempt)
    write_csv(OUTPUTS["route_scorecard"], route_scorecard)
    write_csv(OUTPUTS["beta_backreaction"], beta_backreaction)
    write_csv(OUTPUTS["missing_primitives"], missing_primitives)
    write_csv(OUTPUTS["claim_gates"], claim_gates)
    write_csv(OUTPUTS["refusal"], refusal)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next_target"], next_target)

    branch_copies = copy_branch_files()
    write_csv(OUTPUTS["branch_copies"], branch_copies)

    generated_before_validation = [
        OUTPUTS["source_register"],
        OUTPUTS["selector_audit"],
        OUTPUTS["coefficient_attempt"],
        OUTPUTS["route_scorecard"],
        OUTPUTS["beta_backreaction"],
        OUTPUTS["missing_primitives"],
        OUTPUTS["claim_gates"],
        OUTPUTS["refusal"],
        OUTPUTS["decision"],
        OUTPUTS["next_target"],
        OUTPUTS["branch_copies"],
    ]
    remove_pycache()
    validation = validation_rows(generated_before_validation, branch_copies)
    write_csv(OUTPUTS["validation"], validation)
    write_markdown(
        sources,
        selector_audit,
        coefficient_attempt,
        route_scorecard,
        beta_backreaction,
        missing_primitives,
        claim_gates,
        refusal,
        decisions,
        next_target,
        branch_copies,
        validation,
    )
    remove_pycache()

    failed = [row for row in validation if row["result"] != "PASS"]
    if failed:
        failed_ids = ", ".join(row["check_id"] for row in failed)
        raise SystemExit(f"2287 validation failed: {failed_ids}")
    print(f"Wrote {DOC}")
    print(f"Wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

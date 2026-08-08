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

BRANCH_ID = "MTS_R2FR_PARENT_WEAK_FIELD_MQ_JQ_DELTA_BETA_SOURCE_OR_ZERO_THEOREM_2286"
START_TS = datetime.now(timezone.utc).timestamp()
DOC = ROOT / "2286-Y5-R2FR-parent-weak-field-Mq-jq-delta-beta-source-or-zero-theorem.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2286_00_2285_doc",
        "source_key": "2285_projection_handoff",
        "source_path": ROOT / "2285-Y5-R2FR-finite-q-PPN-R10-projection-matrix-or-input-source-pack.md",
        "needles": ["ATTACK_PARENT_WEAK_FIELD_EXPANSION_NEXT", "q_R=j_q/M_q^2", "POBS_MATRIX_WRITTEN_NONCLAIM"],
        "role": "handoff selecting parent weak-field coefficient derivation",
    },
    {
        "source_id": "SRC2286_01_2285_validation",
        "source_key": "2285_validation",
        "source_path": OUT / "P8_Y5_BRR545_2285_VALIDATION.csv",
        "needles": ["VAL2285_OVERALL", "PASS"],
        "role": "confirms 2285 passed before 2286 starts",
    },
    {
        "source_id": "SRC2286_02_2284_finite_audit",
        "source_key": "2284_finite_q_audit",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2284_FINITE_Q_INPUT_SOURCE_AUDIT.csv",
        "needles": ["FQA2284_0_Mq2", "MISSING_PARENT_STIFFNESS_COEFFICIENT", "FQA2284_1_jq"],
        "role": "finite q missing coefficient intake",
    },
    {
        "source_id": "SRC2286_03_2233_weak_field",
        "source_key": "2233_weak_field_attempt",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2233_WEAK_FIELD_DERIVATION_ATTEMPT.csv",
        "needles": ["WF2233_5_beta_target", "MISSING_SECOND_ORDER_PARENT_COMPLETION", "WF2233_6_verdict"],
        "role": "weak-field zero-condition failure and beta target",
    },
    {
        "source_id": "SRC2286_04_2233_contract",
        "source_key": "2233_conditional_contract",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2233_CONDITIONAL_ZERO_THEOREM_CONTRACT.csv",
        "needles": ["COND2233_0_L_parent", "COND2233_4_second_order", "UNSIGNED_REQUIRED_PREMISE"],
        "role": "conditional theorem premises for local GR recovery",
    },
    {
        "source_id": "SRC2286_05_2234_ansatz",
        "source_key": "2234_minimal_action_ansatz",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2234_MINIMAL_ACTION_ANSATZ_REGISTER.csv",
        "needles": ["ANS2234_A_EH_lambdaR_silent", "BEST_CONDITIONAL_ANSATZ_NOT_ADOPTED", "ANS2234_D_kinetic_RAB"],
        "role": "minimal action ansatz and kinetic reciprocal branch",
    },
    {
        "source_id": "SRC2286_06_2234_euler",
        "source_key": "2234_euler_gate",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2234_EULER_VARIATION_GATE.csv",
        "needles": ["EUL2234_1_lambda_variation", "FAIL_UNSIGNED_STRESS_SILENCE", "EUL2234_3_EH_metric"],
        "role": "lambda variation, stress silence, and EH beta gate",
    },
    {
        "source_id": "SRC2286_07_1256_hcore",
        "source_key": "1256_minimal_Hcore",
        "source_path": OUT / "P8_Y5_R10_1256_MINIMAL_HCORE_SOURCE_EQUATION_CONTRACT.csv",
        "needles": ["HC1256_0_minimal_density", "M_R^2", "FORMAL_VARIATIONAL_CONTRACT_NOT_PARENT_SIGNED"],
        "role": "minimal reciprocal H_core normal-form contract",
    },
    {
        "source_id": "SRC2286_08_1256_coefficients",
        "source_key": "1256_coefficient_requirements",
        "source_path": OUT / "P8_Y5_R10_1256_COEFFICIENT_REQUIREMENTS.csv",
        "needles": ["COEF1256_1_MR2", "COEF1256_3_JR", "MISSING"],
        "role": "reciprocal coefficient requirements for Z_R, M_R^2, lambda_R, J_R, boundary",
    },
    {
        "source_id": "SRC2286_09_1251_blockers",
        "source_key": "1251_Hcore_blockers",
        "source_path": OUT / "P8_Y5_R10_1251_BLOCKER_LEDGER.csv",
        "needles": ["BLK1251_0_Hcore", "explicit weak-field H_core missing", "BLK1251_2_matter"],
        "role": "H_core and matter/source descent blockers",
    },
    {
        "source_id": "SRC2286_10_2232_model",
        "source_key": "2232_two_parameter_model",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2232_TWO_PARAMETER_MODEL.csv",
        "needles": ["MODEL2232_0_gamma", "MODEL2232_5_mercury_beta", "PPN_TRANSLATION_CONTROL_NOT_MTS_PREDICTION"],
        "role": "two-parameter q_R/delta_beta local PPN control plane",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2286_SOURCE_REGISTER.csv",
    "normal_form": OUT / "P8_Y5_PARENT_QLOC_2286_WEAK_FIELD_NORMAL_FORM.csv",
    "coefficient_definitions": OUT / "P8_Y5_PARENT_QLOC_2286_MQ_JQ_COEFFICIENT_DEFINITIONS.csv",
    "beta_completion": OUT / "P8_Y5_PARENT_QLOC_2286_DELTA_BETA_COMPLETION_LEDGER.csv",
    "derivation_runner": OUT / "P8_Y5_PARENT_QLOC_2286_DERIVATION_ATTEMPT_RUNNER.csv",
    "fork_ledger": OUT / "P8_Y5_PARENT_QLOC_2286_ZERO_OR_FINITE_FORK_LEDGER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2286_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2286_REFUSAL_RUNNER.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2286_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2286_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2286_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2286_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_normal_form": (OUTPUTS["normal_form"], QUEUE / "JR2286_WEAK_FIELD_NORMAL_FORM_NONCLAIM.csv"),
    "queue_coefficients": (OUTPUTS["coefficient_definitions"], QUEUE / "JR2286_MQ_JQ_COEFFICIENT_DEFINITIONS_NONCLAIM.csv"),
    "branch_wep_refusal": (OUTPUTS["refusal"], MICROSCOPE / "RAB_parent_weak_field_refusal_2286.csv"),
    "beta_completion": (OUTPUTS["beta_completion"], BETA_DOCS / "RAB_DELTA_BETA_COMPLETION_2286_NONCLAIM.csv"),
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


def formalization_has_2286_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    for candidate in FORMALIZATION.rglob("*2286*"):
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


def normal_form_rows() -> list[dict[str, Any]]:
    return [
        {
            "normal_id": "NF2286_0_variables",
            "object": "weak-field variables",
            "normal_form": "L=2U/c^2, q=R_AB=ln(T^2 S), J_q=j_q L+j_q2 L^2+O(L^3)",
            "variation_or_readout": "q_R is defined by q=q_R L+O(L^2) in the local exterior",
            "derived_relation": "q_R=j_q/M_q^2 only if the q sector is algebraic and M_q^2 is nonzero in the same normalization",
            "current_status": "NORMAL_FORM_WRITTEN_INPUTS_MISSING",
            "valid_for_claim": False,
        },
        {
            "normal_id": "NF2286_1_algebraic_q_sector",
            "object": "parent q sector",
            "normal_form": "L_q=-1/2 M_q^2 q^2 + (j_q L+j_q2 L^2+...) q + O(q^3)",
            "variation_or_readout": "delta_q L_q=0 gives M_q^2 q=j_q L+j_q2 L^2+...",
            "derived_relation": "q_R=j_q/M_q^2 and q_R=0 iff j_q=0 with M_q^2>0, before boundary and gradient channels",
            "current_status": "FORMAL_DERIVATION_PARENT_COEFFICIENTS_MISSING",
            "valid_for_claim": False,
        },
        {
            "normal_id": "NF2286_2_constraint_q_sector",
            "object": "nonpropagating reciprocal constraint",
            "normal_form": "L_constraint=lambda_R q plus parent origin and stress-silence certificates",
            "variation_or_readout": "delta_lambda_R L=0 gives q=0",
            "derived_relation": "would force q_R=0 only if lambda_R is parent-owned, first-class/auxiliary, stress-silent, and boundary-proper",
            "current_status": "CONDITIONAL_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "normal_id": "NF2286_3_gradient_hair_sector",
            "object": "gradient or boundary q branch",
            "normal_form": "L_q=-1/2 Z_q (nabla q)^2 -1/2 M_q^2 q^2 + J_q q + boundary",
            "variation_or_readout": "Z_q box q-M_q^2 q+J_q=0, with boundary momentum Pi_q",
            "derived_relation": "finite range lambda_q=sqrt(Z_q/M_q^2) or Q_R hair must be projected separately",
            "current_status": "OPERATOR_BOUNDARY_INVENTORY_MISSING",
            "valid_for_claim": False,
        },
        {
            "normal_id": "NF2286_4_beta_completion",
            "object": "second-order PPN beta lane",
            "normal_form": "delta_beta := beta_parent-1 after valid PPN gauge/readout/source normalization",
            "variation_or_readout": "delta_beta cannot be read from one raw T^2 coefficient without coordinate/source/readout map",
            "derived_relation": "delta_beta=0 only if the parent second-order metric/coframe equation, source normalization, and Ward/Bianchi identity reproduce the GR PPN lane",
            "current_status": "SECOND_ORDER_PARENT_COMPLETION_MISSING",
            "valid_for_claim": False,
        },
    ]


def coefficient_definition_rows() -> list[dict[str, Any]]:
    entries = [
        ("COEF2286_0_Mq2", "M_q^2", "minus the second q variation of the local parent weak-field density in the convention L_q=-1/2 M_q^2 q^2+J_q q", "parent Hessian around local vacuum", "MISSING_PARENT_STIFFNESS_COEFFICIENT"),
        ("COEF2286_1_jq", "j_q", "coefficient of the first source/readout leg J_q=j_q L+O(L^2)", "mixed parent variation in q and Newtonian load/source L", "MISSING_PARENT_SOURCE_COEFFICIENT"),
        ("COEF2286_2_qR", "q_R", "q_R=j_q/M_q^2 for algebraic q, or q_R=0 if a signed constraint/no-source theorem kills q", "COEF2286_0 and COEF2286_1 in compatible units or signed zero theorem", "MISSING_RATIO_OR_ZERO_THEOREM"),
        ("COEF2286_3_Zq", "Z_q", "gradient coefficient of q if reciprocal strain propagates or has finite range", "operator inventory of parent q sector", "MISSING_OPERATOR_INVENTORY"),
        ("COEF2286_4_boundary", "Pi_q or Q_R", "boundary momentum/charge that can source exterior q hair", "boundary variation and physical source worldtube class", "MISSING_BOUNDARY_CHARGE_CLASS"),
        ("COEF2286_5_beta2", "B_beta_parent", "second-order parent coefficient vector that maps to beta_parent in a valid PPN gauge", "O(L^2) parent field equation plus gauge/readout/source normalization", "MISSING_SECOND_ORDER_PARENT_COMPLETION"),
        ("COEF2286_6_source_norm", "delta_GM or epsilon_mu_extra", "source-normalization residual that can shift q_R/beta readout", "Pi_M/Hilbert/worldtube glue or explicit residual vector", "RETAINED_UNFILLED_SOURCE_NORMALIZATION_VECTOR"),
    ]
    return [
        {
            "coefficient_id": coefficient_id,
            "symbol": symbol,
            "definition": definition,
            "required_source": required_source,
            "current_status": status,
            "parent_prediction_ready": False,
            "score_ready": False,
            "valid_for_claim": False,
        }
        for coefficient_id, symbol, definition, required_source, status in entries
    ]


def beta_completion_rows() -> list[dict[str, Any]]:
    return [
        {
            "beta_id": "BETA2286_0_definition",
            "target": "delta_beta",
            "statement": "delta_beta=beta_parent-1 in a declared PPN gauge, not an arbitrary coordinate coefficient",
            "required_inputs": "second-order metric/coframe expansion; coordinate/gauge map; source normalization; matter readout",
            "current_status": "DEFINITION_READY_PARENT_COMPLETION_MISSING",
            "valid_for_claim": False,
        },
        {
            "beta_id": "BETA2286_1_EH_conditional",
            "target": "delta_beta=0",
            "statement": "EH plus universal matter/source readout gives beta=1 conditionally",
            "required_inputs": "MTS primitives matched to EH operator, Pi_M/Hilbert source equality, boundary reference, extra-sector silence",
            "current_status": "CONDITIONAL_EH_ROUTE_NOT_MTS_ADOPTED",
            "valid_for_claim": False,
        },
        {
            "beta_id": "BETA2286_2_q_backreaction",
            "target": "q-sector contribution to beta",
            "statement": "finite q can feed beta at O(L^2) through j_q2/M_q^2, q^2 terms, or source-normalization backreaction",
            "required_inputs": "q cubic/quadratic coefficients; j_q2; source-normalization vector; valid PPN gauge",
            "current_status": "MISSING_Q_BACKREACTION_COEFFICIENTS",
            "valid_for_claim": False,
        },
        {
            "beta_id": "BETA2286_3_no_shortcut",
            "target": "beta claim policy",
            "statement": "beta=1 cannot be inferred merely from q_R=0 or from closure Schwarzschild control values",
            "required_inputs": "parent second-order variation and Ward/Bianchi identity",
            "current_status": "GUARD_ACTIVE",
            "valid_for_claim": False,
        },
    ]


def derivation_runner_rows() -> list[dict[str, Any]]:
    entries = [
        ("RUN2286_0_normal_form", "write shared weak-field normal form", "PASS_NONCLAIM", "normal form for q_R and delta_beta is explicit"),
        ("RUN2286_1_Mq2", "derive M_q^2 from parent Hessian", "BLOCKED", "current corpus has formal H_core/Hessian requirements but no sourced coefficient"),
        ("RUN2286_2_jq", "derive j_q or theorem-zero source leg", "BLOCKED", "matter/readout q-source leg remains missing"),
        ("RUN2286_3_qR", "derive q_R=j_q/M_q^2 or q_R=0", "BLOCKED", "M_q^2 and j_q are missing; lambda_R/no-charge zero theorem remains unsigned"),
        ("RUN2286_4_delta_beta", "derive delta_beta=0 or finite value", "BLOCKED", "second-order parent completion, source normalization, and Ward/Bianchi identity are missing"),
        ("RUN2286_5_claim", "promote local GR/Newton", "REFUSED_NO_PARENT_PREDICTION", "normal form is not a parent derivation"),
    ]
    return [
        {
            "runner_id": runner_id,
            "test": test,
            "current_status": status,
            "detail": detail,
            "parent_prediction_ready": False,
            "score_ready": False,
            "valid_for_claim": False,
        }
        for runner_id, test, status, detail in entries
    ]


def fork_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "fork_id": "FORK2286_0_constraint_zero",
            "route": "parent-owned lambda_R or first-class reciprocal constraint",
            "condition_to_promote": "lambda_R/R_AB constraint has parent origin, stress silence, Dirac/degree-count closure, and proper boundary charge",
            "result_if_closed": "q_R=0 before PPN scoring",
            "current_status": "BEST_ZERO_ROUTE_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "fork_id": "FORK2286_1_algebraic_finite",
            "route": "algebraic finite q residual",
            "condition_to_promote": "M_q^2 and j_q are parent-sourced with compatible units; no gradient/boundary hair",
            "result_if_closed": "q_R=j_q/M_q^2 becomes a local prediction to feed 2285 P_obs",
            "current_status": "SOURCE_PACK_READY_INPUTS_MISSING",
            "valid_for_claim": False,
        },
        {
            "fork_id": "FORK2286_2_massive_range",
            "route": "gradient/massive suppressed q residual",
            "condition_to_promote": "Z_q, M_q^2, source coupling, boundary flux, and range map are sourced",
            "result_if_closed": "lambda_q=sqrt(Z_q/M_q^2) and alpha(lambda)/PPN projections become testable",
            "current_status": "OPERATOR_RANGE_INPUTS_MISSING",
            "valid_for_claim": False,
        },
        {
            "fork_id": "FORK2286_3_second_order_beta",
            "route": "second-order parent beta completion",
            "condition_to_promote": "parent weak-field equation to O(L^2), Ward/Bianchi identity, and source/readout map reproduce beta=1 or give finite delta_beta",
            "result_if_closed": "delta_beta becomes a parent prediction for 2285/2232 PPN runner",
            "current_status": "PARENT_COMPLETION_MISSING",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {"claim_id": "CG2286_0_normal_form", "claim": "shared weak-field normal form is written", "gate_pass": True, "reason": "M_q^2, j_q, q_R, gradient hair, and delta_beta lanes are defined", "valid_for_claim": False},
        {"claim_id": "CG2286_1_coefficients", "claim": "M_q^2 and j_q are parent-sourced", "gate_pass": False, "reason": "Hessian and q-source coefficients remain missing", "valid_for_claim": False},
        {"claim_id": "CG2286_2_qR_prediction", "claim": "q_R is parent-predicted or theorem-zero", "gate_pass": False, "reason": "ratio inputs and constraint/no-charge theorem are unsigned", "valid_for_claim": False},
        {"claim_id": "CG2286_3_delta_beta_prediction", "claim": "delta_beta is parent-predicted or theorem-zero", "gate_pass": False, "reason": "second-order completion and source/Ward identities are missing", "valid_for_claim": False},
        {"claim_id": "CG2286_4_local_GR_Newton", "claim": "local GR/Newton recovery is derived", "gate_pass": False, "reason": "normal form identifies missing parent coefficients but does not supply them", "valid_for_claim": False},
    ]


def refusal_rows() -> list[dict[str, Any]]:
    entries = [
        ("REF2286_0_infer_qR_zero", "infer q_R=0 because GR is desired", "REFUSED_MISSING_ZERO_THEOREM", "need j_q=0/no-charge/constraint theorem in parent action"),
        ("REF2286_1_use_bounds", "use Cassini/PPN bounds as q_R or M_q^2 source", "REFUSED_BOUNDS_ARE_COMPARATORS", "bounds screen predictions but cannot define parent coefficients"),
        ("REF2286_2_beta_from_closure", "claim beta=1 from closure control lane", "REFUSED_CLOSURE_NOT_PARENT_COMPLETION", "beta needs second-order parent variation and source normalization"),
        ("REF2286_3_lambda_shortcut", "accept lambda_R variation as derivation by itself", "REFUSED_LAMBDAR_ORIGIN_STRESS_MISSING", "parent origin, stress silence, and first-class/auxiliary status are unsigned"),
        ("REF2286_4_local_claim", "claim local GR/Newton from normal form", "REFUSED_NORMAL_FORM_NOT_VALUES", "normal form gives slots, not sourced values"),
    ]
    return [
        {
            "refusal_id": refusal_id,
            "attempted_claim": attempted_claim,
            "runner_result": result,
            "blocked_by": blocked_by,
            "score_eligible": False,
            "valid_for_claim": False,
        }
        for refusal_id, attempted_claim, result, blocked_by in entries
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2286_0_result",
            "decision": "NORMAL_FORM_DERIVED_COEFFICIENTS_NOT_SOURCED",
            "reason": "q_R=j_q/M_q^2 and delta_beta are now tied to one weak-field coefficient language, but parent values/theorem-zeros are absent",
            "next_action": "extract q-sector coefficients from actual parent primitives or select the constraint route",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2286_1_best_next",
            "decision": "Q_SECTOR_COEFFICIENT_EXTRACTION_OR_SELECTOR_FORK_NEXT",
            "reason": "the fastest route to local GR is deciding whether q is constrained away, algebraic finite, or gradient/massive",
            "next_action": "2287-Y5-R2FR-q-sector-parent-coefficient-extraction-or-selector-fork.md",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2286_2_claim_policy",
            "decision": "KEEP_PRIVATE_NONCLAIM",
            "reason": "normal-form progress is internal derivation infrastructure, not public evidence",
            "next_action": "no GitHub action",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "NEXT2286_0_primary",
            "next_target": "2287-Y5-R2FR-q-sector-parent-coefficient-extraction-or-selector-fork.md",
            "script": "scripts/Y5_R2FR_q_sector_parent_coefficient_extraction_or_selector_fork_2287.py",
            "objective": "extract or reject the q-sector parent coefficients and selector status: decide whether q is a parent-owned constraint, an algebraic finite residual with M_q^2 and j_q, or a gradient/massive branch with Z_q and boundary charge; carry delta_beta backreaction terms without claims",
            "selection_status": "selected",
            "success_condition": "one q-sector route is selected with source-backed coefficients or every missing parent primitive is queued while q_R/delta_beta remain nonclaim",
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
                "reason": "branch copy for 2286 parent weak-field normal-form checkpoint",
            }
        )
    return rows


def validation_rows(all_generated_before_validation: list[Path], branch_copy_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_rows = read_csv(OUTPUTS["source_register"])
    normal_rows = read_csv(OUTPUTS["normal_form"])
    coefficient_rows = read_csv(OUTPUTS["coefficient_definitions"])
    beta_rows = read_csv(OUTPUTS["beta_completion"])
    runner_rows = read_csv(OUTPUTS["derivation_runner"])
    fork_rows = read_csv(OUTPUTS["fork_ledger"])
    gate_rows = read_csv(OUTPUTS["claim_gates"])
    refusal_runner_rows = read_csv(OUTPUTS["refusal"])
    decision_rows_local = read_csv(OUTPUTS["decision"])
    next_rows = read_csv(OUTPUTS["next_target"])

    coefficient_symbols = {row["symbol"] for row in coefficient_rows}
    checks = [
        ("VAL2286_0_sources_exist", all(row["exists"] == "True" for row in source_rows), "all cited source paths exist"),
        ("VAL2286_1_needles_present", all(row["needles_present"] == "True" for row in source_rows), "all cited source needles are present"),
        ("VAL2286_2_prior_validation", validation_pass(OUT / "P8_Y5_BRR545_2285_VALIDATION.csv"), "2285 validation passes before 2286"),
        (
            "VAL2286_3_normal_form_contains_ratio",
            any("q_R=j_q/M_q^2" in row["derived_relation"] for row in normal_rows),
            "normal form derives q_R=j_q/M_q^2 relation conditionally",
        ),
        (
            "VAL2286_4_coefficients_complete",
            {"M_q^2", "j_q", "q_R", "Z_q", "Pi_q or Q_R", "B_beta_parent", "delta_GM or epsilon_mu_extra"}.issubset(coefficient_symbols),
            "coefficient definitions cover stiffness, source leg, ratio, gradient, boundary, beta, and source normalization",
        ),
        (
            "VAL2286_5_beta_guard",
            any(row["beta_id"] == "BETA2286_3_no_shortcut" and row["current_status"] == "GUARD_ACTIVE" for row in beta_rows),
            "beta=1 shortcut from closure is refused",
        ),
        (
            "VAL2286_6_runner_blocks_claims",
            any(row["runner_id"] == "RUN2286_5_claim" and row["current_status"] == "REFUSED_NO_PARENT_PREDICTION" for row in runner_rows),
            "runner refuses local GR/Newton claim",
        ),
        (
            "VAL2286_7_forks_complete",
            {row["route"] for row in fork_rows}
            >= {
                "parent-owned lambda_R or first-class reciprocal constraint",
                "algebraic finite q residual",
                "gradient/massive suppressed q residual",
                "second-order parent beta completion",
            },
            "zero/finite/range/beta fork ledger is complete",
        ),
        (
            "VAL2286_8_claim_gates_blocked",
            any(row["claim_id"] == "CG2286_4_local_GR_Newton" and row["gate_pass"] == "False" for row in gate_rows)
            and all(row["valid_for_claim"] == "False" for row in gate_rows),
            "local GR/Newton and coefficient claims remain blocked",
        ),
        (
            "VAL2286_9_refusals_include_bounds",
            any(row["runner_result"] == "REFUSED_BOUNDS_ARE_COMPARATORS" for row in refusal_runner_rows),
            "bounds-as-coefficients refusal is active",
        ),
        (
            "VAL2286_10_next_selected",
            any(row["next_target"] == "2287-Y5-R2FR-q-sector-parent-coefficient-extraction-or-selector-fork.md" for row in next_rows)
            and any(row["decision"] == "Q_SECTOR_COEFFICIENT_EXTRACTION_OR_SELECTOR_FORK_NEXT" for row in decision_rows_local),
            "2287 q-sector coefficient/selector fork selected",
        ),
        ("VAL2286_11_csv_parse", all(csv_parses(path) for path in all_generated_before_validation), "all generated 2286 CSVs parse before validation file"),
        ("VAL2286_12_no_claim_flags", generated_claim_flags_false(all_generated_before_validation), "all generated claim/score flags remain false"),
        ("VAL2286_13_branch_copies", all(row["target_exists"] and row["target_parses"] for row in branch_copy_rows), "branch/queue copies exist and parse"),
        ("VAL2286_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL2286_15_formalization_no_2286", not formalization_has_2286_artifacts(), "formalization-workbench has no non-venv 2286 artifacts"),
        ("VAL2286_16_formalization_untouched", not formalization_touched_since_start(), "formalization-workbench untouched during 2286 run"),
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
            "check_id": "VAL2286_OVERALL",
            "result": "PASS" if overall_pass else "FAIL",
            "detail": "2286 derives the shared weak-field normal form for q_R and delta_beta, keeps parent coefficients unsourced/nonclaim, and selects q-sector coefficient extraction or selector fork next",
        }
    )
    return rows


def write_markdown(
    sources: list[dict[str, Any]],
    normal_form: list[dict[str, Any]],
    coefficient_definitions: list[dict[str, Any]],
    beta_completion: list[dict[str, Any]],
    derivation_runner: list[dict[str, Any]],
    fork_ledger: list[dict[str, Any]],
    claim_gates: list[dict[str, Any]],
    refusal: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    branch_copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    content = f"""# 2286 - Y5/R2FR Parent Weak-Field Mq/jq/delta_beta Source Or Zero Theorem

## Verdict

This checkpoint gets one real derivation step: the finite local branch can be put in a shared weak-field normal form.

If the reciprocal sector is algebraic, then

`L_q=-1/2 M_q^2 q^2 + (j_q L+j_q2 L^2+...)q`

so the Euler equation gives

`q=q_R L+O(L^2)` with `q_R=j_q/M_q^2`.

That is useful because it tells us exactly what must be derived. But the current corpus still does not source `M_q^2`, `j_q`, the boundary/no-hair guard, or the second-order beta completion. Therefore 2286 does not claim local GR/Newton. It converts the gap into a coefficient/selector fork: either `q` is a parent-owned constraint, or it is a finite algebraic/range residual with sourceable coefficients.

## Source Register
{table(["source_id", "source_key", "source_path", "exists", "needles_present", "role", "valid_for_claim"], sources)}

## Weak-Field Normal Form
{table(["normal_id", "object", "normal_form", "variation_or_readout", "derived_relation", "current_status", "valid_for_claim"], normal_form)}

## Mq/jq Coefficient Definitions
{table(["coefficient_id", "symbol", "definition", "required_source", "current_status", "parent_prediction_ready", "score_ready", "valid_for_claim"], coefficient_definitions)}

## Delta Beta Completion Ledger
{table(["beta_id", "target", "statement", "required_inputs", "current_status", "valid_for_claim"], beta_completion)}

## Derivation Attempt Runner
{table(["runner_id", "test", "current_status", "detail", "parent_prediction_ready", "score_ready", "valid_for_claim"], derivation_runner)}

## Zero Or Finite Fork Ledger
{table(["fork_id", "route", "condition_to_promote", "result_if_closed", "current_status", "valid_for_claim"], fork_ledger)}

## Claim Gates
{table(["claim_id", "claim", "gate_pass", "reason", "valid_for_claim"], claim_gates)}

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

This is the useful kind of annoying: the shape of the answer is now simple, but the parent coefficients are not yet owned. The next move should be narrow and decisive: decide whether the reciprocal sector is constrained, algebraic finite, or gradient/massive. Once that is selected, `q_R` stops being a ghost variable and becomes either zero by theorem or a testable number.
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    remove_pycache()
    sources = source_register_rows()
    normal_form = normal_form_rows()
    coefficient_definitions = coefficient_definition_rows()
    beta_completion = beta_completion_rows()
    derivation_runner = derivation_runner_rows()
    fork_ledger = fork_ledger_rows()
    claim_gates = claim_gate_rows()
    refusal = refusal_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["normal_form"], normal_form)
    write_csv(OUTPUTS["coefficient_definitions"], coefficient_definitions)
    write_csv(OUTPUTS["beta_completion"], beta_completion)
    write_csv(OUTPUTS["derivation_runner"], derivation_runner)
    write_csv(OUTPUTS["fork_ledger"], fork_ledger)
    write_csv(OUTPUTS["claim_gates"], claim_gates)
    write_csv(OUTPUTS["refusal"], refusal)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next_target"], next_target)

    branch_copies = copy_branch_files()
    write_csv(OUTPUTS["branch_copies"], branch_copies)

    generated_before_validation = [
        OUTPUTS["source_register"],
        OUTPUTS["normal_form"],
        OUTPUTS["coefficient_definitions"],
        OUTPUTS["beta_completion"],
        OUTPUTS["derivation_runner"],
        OUTPUTS["fork_ledger"],
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
        normal_form,
        coefficient_definitions,
        beta_completion,
        derivation_runner,
        fork_ledger,
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
        raise SystemExit(f"2286 validation failed: {failed_ids}")
    print(f"Wrote {DOC}")
    print(f"Wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "1874"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / CHECKPOINT_ID
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1874-Y5-R2FR-parent-domain-verticality-for-RAB-or-explicit-residual-field.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1874_SOURCE_REGISTER.csv",
    "verticality_attempt": OUT / "P8_Y5_PARENT_QLOC_1874_RAB_VERTICALITY_CONSTRUCTION_ATTEMPT.csv",
    "trilemma": OUT / "P8_Y5_PARENT_QLOC_1874_RAB_DOMAIN_TRILEMMA_VERDICT.csv",
    "residual_classification": OUT / "P8_Y5_PARENT_QLOC_1874_RAB_EXPLICIT_RESIDUAL_FIELD_CLASSIFICATION.csv",
    "bound_requirements": OUT / "P8_Y5_PARENT_QLOC_1874_RAB_RESIDUAL_BOUND_REQUIREMENTS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1874_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1874_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1874_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_1874_VALIDATION.csv",
}

SOURCE_NEEDLES = {
    "1873_doc": {
        "path": ROOT / "1873-Y5-R2FR-boundary-silence-parent-contract-for-CR-zero-or-residual-closure.md",
        "needles": [
            "BOUNDARY_SILENCE_PARENT_CONTRACT_EXACTLY_STATED",
            "CURRENT_LOCAL_CR_ZERO_ROUTE_DEMOTED_TO_RESIDUAL_CLOSURE",
            "PARENT_DOMAIN_VERTICALITY_OR_EXPLICIT_RESIDUAL_FIELD_SELECTED_NEXT",
        ],
    },
    "1873_contract": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1873_BOUNDARY_SILENCE_PARENT_CONTRACT.csv",
        "needles": [
            "UNSIGNED_PARENT_DOMAIN",
            "A parent quotient q:Phi_parent->Q_obs exists before matter/readout",
            "R_AB remains a physical local/PPN residual channel",
        ],
    },
    "1575_doc": {
        "path": ROOT / "1575-Y5-RAB-parent-RAB-vertical-generator-and-matter-descent-signature.md",
        "needles": [
            "R_AB=ln(T^2 S)",
            "Closure-only verticality is refused",
            "RAB_VERTICALITY_NOT_SIGNED_TRILEMMA_EXPLICIT",
        ],
    },
    "1575_vertical": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1575_RAB_VERTICAL_GENERATOR_SIGNATURE_ATTEMPT.csv",
        "needles": [
            "CHART_CONTRACT_WRITTEN_NOT_PARENT_SIGNED",
            "NOT_PARENT_SIGNED",
            "FAIL_CURRENT_CLAIM_VERTICALITY_NOT_SIGNED",
        ],
    },
    "1575_trilemma": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1575_RAB_COFAME_VISIBILITY_TRILEMMA.csv",
        "needles": [
            "physical coframe residual",
            "quotient_representative",
            "constraint_no_pole",
            "closure_axiom",
        ],
    },
    "1576_doc": {
        "path": ROOT / "1576-Y5-RAB-constraint-no-pole-or-quotient-map-construction.md",
        "needles": [
            "R_AB=ln(T^2 S)=2 ln(J_q)",
            "QUOTIENT_MAP_CONFLICT_IDENTIFIED",
            "CONSTRAINT_ROUTE_MOTIVATED_NOT_DERIVED",
        ],
    },
    "1576_quotient": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1576_RAB_QUOTIENT_MAP_CONSTRUCTION_ATTEMPT.csv",
        "needles": [
            "observer_jacobian",
            "shape_only_quotient",
            "constraint_first",
            "REFUSED",
        ],
    },
    "1576_no_pole": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1576_RAB_NO_POLE_THEOREM_ATTEMPT.csv",
        "needles": [
            "first_class",
            "positive_sourcefree",
            "absent_nonprimitive",
            "FAIL_CURRENT_CLAIM_NO_POLE_NOT_DERIVED",
        ],
    },
    "10_observer": {
        "path": ROOT / "10-observer-map-symplectic-contract.md",
        "needles": [
            "R_AB = ln(T^2 S) = 2 ln(J_q).",
            "derive R_AB=0 from the parent theory",
            "explicit closure",
        ],
    },
    "07_constraint": {
        "path": ROOT / "07-nonpropagating-reciprocity-constraint.md",
        "needles": [
            "S_constraint = integral lambda_R R_AB.",
            "R_AB = 0.",
            "parent origin is still open",
        ],
    },
    "1486_neighbourhood": {
        "path": ROOT / "1486-Y5-R10-RAB-neighbourhood-quotient-descent-or-MOMS-parent-signature-source-map.md",
        "needles": [
            "TARGET_EXACT",
            "CONTRACT_AVAILABLE_NOT_PARENT_SIGNED",
            "NEIGHBOURHOOD_DESCENT_NOT_PARENT_SIGNED",
        ],
    },
}


def ensure_dirs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)


def bool_string(value: Any) -> str:
    return str(value).strip().lower()


def path_has_needles(path: Path, needles: list[str]) -> tuple[bool, str]:
    if not path.exists():
        return False, "MISSING_SOURCE_PATH"
    text = path.read_text(encoding="utf-8", errors="ignore")
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return False, "MISSING_NEEDLES=" + ";".join(missing)
    return True, "OK"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, payload in SOURCE_NEEDLES.items():
        path = payload["path"]
        ok, detail = path_has_needles(path, payload["needles"])
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source_id,
                "source_path": str(path),
                "required_needles": " ; ".join(payload["needles"]),
                "source_exists": path.exists(),
                "needle_check": detail,
                "usable_for_1874": ok,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def verticality_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "VAT1874_0_observer_cell_quotient",
            "candidate_q": "q_obs includes observer radial phase-cell/J_q data",
            "candidate_vR": "v_R changes R_AB=2 ln(J_q)",
            "test": "Dq[v_R] must vanish",
            "result": "Dq[v_R] != 0 unless J_q is removed or constrained",
            "status": "VERTICALITY_REJECTED_FOR_OBSERVER_CELL_MAP",
            "reason": "R_AB is coframe/observer-cell visible in the current observer map",
            "next_requirement": "do not call R_AB gauge/vertical under this q",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "VAT1874_1_shape_only_quotient",
            "candidate_q": "q_shape keeps physical shape/orientation but quotients reciprocal cell-volume R_AB",
            "candidate_vR": "v_R is cell-volume representative direction",
            "test": "matter rods/clocks and e_obs must be independent of R_AB on an open neighbourhood",
            "result": "possible contract, not constructed from MTS primitives",
            "status": "POSSIBLE_BUT_NOT_PARENT_CONSTRUCTED",
            "reason": "requires an independent cell normalization and observed coframe functor that the corpus does not supply",
            "next_requirement": "construct q_shape and Obs_e(q_shape) explicitly or reject",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "VAT1874_2_constraint_first",
            "candidate_q": "q after parent constraint lambda_R R_AB removes the R_AB fibre",
            "candidate_vR": "no physical v_R remains after constraint/no-pole elimination",
            "test": "lambda_R R_AB or first-class/no-pole owner must be parent-derived",
            "result": "clean route, parent origin unsigned",
            "status": "CONSTRAINT_FIRST_ROUTE_OPEN_NOT_DERIVED",
            "reason": "07/1576 motivate the constraint but do not derive lambda_R or no-pole from the parent action",
            "next_requirement": "derive lambda_R/current-chain/no-pole owner or keep residual field",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "VAT1874_3_absent_nonprimitive",
            "candidate_q": "R_AB is a readout artefact absent from the varied parent action",
            "candidate_vR": "no R_AB variation slot exists",
            "test": "S_parent, S_matter, and boundary terms must contain no R_AB primitive or derivative",
            "result": "not parent-proved; current 05/1581 branch gives a current equation when retained",
            "status": "ABSENT_FIELD_ROUTE_NOT_DERIVED",
            "reason": "the corpus has both closure/no-pole language and retained kinetic/current language; no parent selector decides",
            "next_requirement": "parent action must choose absent/constraint or explicit residual operator",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "VAT1874_4_posthoc_closure",
            "candidate_q": "delete R_AB after readout because local GR requires it",
            "candidate_vR": "closure-imposed v_R",
            "test": "must be parent-derived, not adopted after the fact",
            "result": "refused",
            "status": "POSTHOC_CLOSURE_REFUSED",
            "reason": "1575/1576 explicitly reject closure-only verticality",
            "next_requirement": "label closure if used; never promote as derivation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def trilemma_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "TRI1874_0_physical_residual",
            "route": "R_AB remains an explicit physical/local residual field",
            "evidence": "observer-cell q sees R_AB and no parent q_shape/constraint is constructed",
            "status": "DEFAULT_CURRENT_CLASSIFICATION",
            "claim_effect": "no beta-zero, C_R-zero, local-GR, PPN, or R10 claim",
            "required_to_escape": "derive q_shape verticality or constraint/no-pole",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "TRI1874_1_quotient_representative",
            "route": "R_AB is a quotient-representative fibre coordinate",
            "evidence": "1575/1873 give exact conditional theorem if q/v_R and matter descent are signed",
            "status": "BEST_THEOREM_ROUTE_UNSIGNED",
            "claim_effect": "would kill bulk matter charge only after parent signatures",
            "required_to_escape": "explicit q_shape, Obs_e(q), Dq[v_R]=0, no-marker and boundary clauses",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "TRI1874_2_constraint_no_pole",
            "route": "R_AB is removed by parent constraint/no-pole before matter variation",
            "evidence": "07/1576 show lambda_R R_AB is algebraically clean but parent origin is open",
            "status": "BEST_LOCAL_GR_ROUTE_UNSIGNED",
            "claim_effect": "would remove C_R tail and finite R10 pole if parent-signed",
            "required_to_escape": "lambda_R/current-chain/first-class/no-pole owner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "TRI1874_3_closure",
            "route": "R_AB=0 or vertical by explicit closure",
            "evidence": "allowed only as labelled benchmark",
            "status": "REFUSED_FOR_DERIVATION",
            "claim_effect": "may benchmark, cannot claim fundamental GR reduction",
            "required_to_escape": "rename as closure/local benchmark or derive parent origin",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def residual_classification_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "classification_id": "RFC1874_0_current_status",
            "field": "R_AB = ln(T^2 S)",
            "classification": "EXPLICIT_RESIDUAL_FIELD_UNTIL_PARENT_VERTICALITY_OR_CONSTRAINT_SIGNED",
            "operator_status": "retained residual channel",
            "test_routing": "PPN/orbital for massless C_R/r tail; R10/clock/orbital only for finite Z_R/M_R^2 Yukawa branch",
            "claim_status": "NONCLAIM",
            "reason": "Dq[v_R]=0 is not parent-signed and observer-cell visibility blocks cheap verticality",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "classification_id": "RFC1874_1_massless_tail",
            "field": "C_R/r reciprocal tail",
            "classification": "MASSLESS_PPN_ORBITAL_RESIDUAL",
            "operator_status": "requires C_R/Pi_R/kappa_W/M_* and no-cancellation",
            "test_routing": "PPN gamma, orbital/light propagation; not R10 alpha(lambda)",
            "claim_status": "BLOCKED_NONCLAIM",
            "reason": "1871/1872 give denominator and bound template, but no numeric/source C_R row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "classification_id": "RFC1874_2_finite_pole",
            "field": "finite R_AB operator",
            "classification": "FINITE_RESIDUAL_FIELD_IF_ZR_MR2_PARENT_SIGNED",
            "operator_status": "requires Z_R, M_R^2, lambda_R, source/test charges",
            "test_routing": "R10 alpha(lambda), clocks, WEP, orbital fifth-force only after finite range is real",
            "claim_status": "BLOCKED_NONCLAIM",
            "reason": "operator/range/source rows remain missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "classification_id": "RFC1874_3_constraint",
            "field": "constraint/no-pole R_AB",
            "classification": "DERIVATION_ROUTE_HELD_OPEN",
            "operator_status": "no physical pole only if lambda_R/no-pole owner is parent-derived",
            "test_routing": "local GR route only after source/boundary/no-cancellation followthrough",
            "claim_status": "BLOCKED_NONCLAIM",
            "reason": "constraint origin not derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def bound_requirement_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "requirement_id": "BR1874_0_vertical_response",
            "quantity": "Dq[v_R] or Lie_{v_R} e_obs",
            "needed_for": "prove quotient representative route or bound geometry leak",
            "current_status": "MISSING_VERTICALITY_CERTIFICATE_OR_BOUND",
            "fallback": "treat R_AB as physical residual",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "requirement_id": "BR1874_1_constraint_owner",
            "quantity": "lambda_R/current-chain/first-class no-pole owner",
            "needed_for": "remove R_AB before matter variation",
            "current_status": "MISSING_PARENT_CONSTRAINT_ORIGIN",
            "fallback": "finite residual operator or closure-labelled benchmark",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "requirement_id": "BR1874_2_operator",
            "quantity": "Z_R, M_R^2, lambda_range",
            "needed_for": "finite R10/clock/orbital branch",
            "current_status": "MISSING_OPERATOR_SIGNATURE",
            "fallback": "no R10 alpha(lambda) from massless C_R/r tail",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "requirement_id": "BR1874_3_source",
            "quantity": "J_R, beta_S^R, beta_T^R, C_R, Pi_R",
            "needed_for": "source/test amplitude and PPN/orbital residual",
            "current_status": "MISSING_SOURCE_CHARGE_RESOLUTION",
            "fallback": "nonclaim bound templates only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "requirement_id": "BR1874_4_boundary",
            "quantity": "worldtube orientation, boundary silence, Pi_R_abs",
            "needed_for": "C_R=0 theorem or absolute tail bound",
            "current_status": "MISSING_BOUNDARY_RESOLUTION",
            "fallback": "keep C_R/Pi_R branch blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "requirement_id": "BR1874_5_residual_vector",
            "quantity": "absolute local residual vector",
            "needed_for": "no-cancellation PPN/local-GR scoring",
            "current_status": "MISSING_NO_CANCELLATION_GUARD",
            "fallback": "no PPN/local-GR pass",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1874_0_verticality",
            "claim": "R_AB is parent-vertical with v_R in ker(Dq)",
            "status": "BLOCKED",
            "reason": "observer-cell map sees R_AB and shape-only quotient is not parent-constructed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1874_1_constraint",
            "claim": "R_AB is removed by parent constraint/no-pole",
            "status": "BLOCKED",
            "reason": "lambda_R/current-chain/no-pole owner missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1874_2_residual_classification",
            "claim": "R_AB must be handled as explicit residual field for now",
            "status": "ALLOW_INTERNAL_NONCLAIM_CLASSIFICATION",
            "reason": "this prevents false local-GR import and routes tests honestly",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1874_3_empirical_score",
            "claim": "R_AB residual passes PPN/R10/local tests",
            "status": "BLOCKED",
            "reason": "operator/source/boundary/no-cancellation inputs are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1874_0_result",
            "decision": "PARENT_DOMAIN_VERTICALITY_NOT_DERIVED",
            "reason": "R_AB=2 ln(J_q) is observer-cell visible under the available observer map, and no explicit shape-only quotient or constraint-first map is constructed",
            "consequence": "do not use v_R in ker(Dq), beta-zero, Pi_R-zero, C_R-zero, or local-GR language as a current claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1874_1_classification",
            "decision": "RAB_CLASSIFIED_AS_EXPLICIT_RESIDUAL_FIELD_CURRENTLY",
            "reason": "this is the only non-smuggling status consistent with 1575/1576/1873",
            "consequence": "route massless tail to PPN/orbital and finite pole to R10 only after operator/source inputs exist",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1874_2_next",
            "decision": "RAB_RESIDUAL_OPERATOR_SOURCE_VECTOR_SELECTED_NEXT",
            "reason": "once R_AB is explicit residual, the next disciplined move is to define its operator/source/tail coefficients and test routing",
            "consequence": "1875 should build the residual coefficient vector and block every score until values or zero theorems are sourced",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1874_0_primary",
            "target_doc": "1875-Y5-R2FR-RAB-residual-operator-source-vector-and-test-routing.md",
            "target_script": "scripts/Y5_R2FR_RAB_residual_operator_source_vector_and_test_routing_1875.py",
            "objective": "build the explicit residual-field coefficient vector for R_AB: vertical response, constraint owner, Z_R/M_R^2/lambda_range, C_R/Pi_R, source charges, boundary terms, and no-cancellation routing across PPN/orbital/R10/clock/WEP.",
            "selection_status": "selected",
            "success_condition": "single nonclaim residual vector that tells every future runner which missing zero theorem or numeric bound is needed before scoring.",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1874_1_derivation_parallel",
            "target_doc": "1875b-Y5-R2FR-shape-only-quotient-map-or-lambdaR-parent-origin-final-attempt.md",
            "target_script": "scripts/Y5_R2FR_shape_only_quotient_map_or_lambdaR_parent_origin_final_attempt_1875b.py",
            "objective": "if continuing derivation-first, make one final explicit construction attempt for q_shape or lambda_R parent origin; otherwise keep residual-field status.",
            "selection_status": "held_parallel",
            "success_condition": "parent-signed q_shape/constraint owner or permanent residual-field classification.",
            "valid_for_claim": False,
        },
    ]


def all_output_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "verticality_attempt": verticality_attempt_rows(),
        "trilemma": trilemma_rows(),
        "residual_classification": residual_classification_rows(),
        "bound_requirements": bound_requirement_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }


def all_claim_flags_false(paths: list[Path]) -> tuple[bool, str]:
    checked = 0
    for path in paths:
        for row_index, row in enumerate(csv_rows(path), start=2):
            for column in ["valid_for_claim", "claim_allowed", "score_ready", "valid_prediction_row", "parent_signed", "numeric_value_present"]:
                if column in row:
                    checked += 1
                    if bool_string(row[column]) == "true":
                        return False, f"{path.name}:{row_index}:{column}=true"
    return checked > 0, f"checked={checked}"


def csv_parse_check(paths: list[Path]) -> tuple[bool, str]:
    details: list[str] = []
    for path in paths:
        rows = csv_rows(path)
        if not rows:
            return False, f"EMPTY_CSV={path.name}"
        details.append(f"{path.name}:{len(rows)}")
    return True, ";".join(details)


def copy_branch_artifacts() -> None:
    for path in OUTPUTS.values():
        if path.name.endswith("_VALIDATION.csv"):
            continue
        shutil.copy2(path, MICROSCOPE_RESIDUALS / path.name)
        shutil.copy2(path, QUARANTINE / path.name)
    shutil.copy2(OUTPUTS["residual_classification"], QUEUE / "JR1874_RAB_EXPLICIT_RESIDUAL_FIELD_CLASSIFICATION_NONCLAIM.csv")
    shutil.copy2(OUTPUTS["bound_requirements"], QUEUE / "JR1874_RAB_RESIDUAL_BOUND_REQUIREMENTS_NONCLAIM.csv")
    shutil.copy2(OUTPUTS["next_target"], QUEUE / "JR1874_NEXT_TARGET_NONCLAIM.csv")


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows() -> list[dict[str, Any]]:
    generated_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    rows_by_name = {key: csv_rows(path) for key, path in OUTPUTS.items() if key != "validation"}
    checks: list[dict[str, Any]] = []

    sources = rows_by_name["source_register"]
    checks.append(
        {
            "validation_id": "VAL1874_0_sources",
            "status": "PASS" if all(bool_string(row["usable_for_1874"]) == "true" for row in sources) else "FAIL",
            "detail": "all verticality sources exist and contain required needles",
            "valid_for_claim": False,
        }
    )

    attempts = rows_by_name["verticality_attempt"]
    checks.append(
        {
            "validation_id": "VAL1874_1_verticality_attempt",
            "status": "PASS"
            if any(row["status"] == "VERTICALITY_REJECTED_FOR_OBSERVER_CELL_MAP" for row in attempts)
            and any(row["status"] == "POSSIBLE_BUT_NOT_PARENT_CONSTRUCTED" for row in attempts)
            and any(row["status"] == "CONSTRAINT_FIRST_ROUTE_OPEN_NOT_DERIVED" for row in attempts)
            else "FAIL",
            "detail": "observer-cell route rejected; quotient/constraint routes unsigned",
            "valid_for_claim": False,
        }
    )

    trilemma = rows_by_name["trilemma"]
    checks.append(
        {
            "validation_id": "VAL1874_2_trilemma",
            "status": "PASS"
            if any(row["status"] == "DEFAULT_CURRENT_CLASSIFICATION" for row in trilemma)
            and any(row["status"] == "REFUSED_FOR_DERIVATION" for row in trilemma)
            else "FAIL",
            "detail": "domain trilemma is resolved to current residual classification",
            "valid_for_claim": False,
        }
    )

    classification = rows_by_name["residual_classification"]
    checks.append(
        {
            "validation_id": "VAL1874_3_residual_classification",
            "status": "PASS"
            if any(row["classification"] == "EXPLICIT_RESIDUAL_FIELD_UNTIL_PARENT_VERTICALITY_OR_CONSTRAINT_SIGNED" for row in classification)
            and any(row["classification"] == "MASSLESS_PPN_ORBITAL_RESIDUAL" for row in classification)
            and any(row["classification"] == "FINITE_RESIDUAL_FIELD_IF_ZR_MR2_PARENT_SIGNED" for row in classification)
            else "FAIL",
            "detail": "R_AB explicit residual classification includes massless and finite routing",
            "valid_for_claim": False,
        }
    )

    requirements = rows_by_name["bound_requirements"]
    required_quantities = {"Dq[v_R] or Lie_{v_R} e_obs", "lambda_R/current-chain/first-class no-pole owner", "Z_R, M_R^2, lambda_range", "J_R, beta_S^R, beta_T^R, C_R, Pi_R"}
    checks.append(
        {
            "validation_id": "VAL1874_4_bound_requirements",
            "status": "PASS" if required_quantities.issubset({row["quantity"] for row in requirements}) else "FAIL",
            "detail": "bound requirement rows cover verticality, constraint, operator, and source",
            "valid_for_claim": False,
        }
    )

    claims = rows_by_name["claim_gate"]
    checks.append(
        {
            "validation_id": "VAL1874_5_claim_gates",
            "status": "PASS"
            if any(row["status"] == "ALLOW_INTERNAL_NONCLAIM_CLASSIFICATION" for row in claims)
            and all(bool_string(row["claim_allowed"]) == "false" for row in claims)
            else "FAIL",
            "detail": "only internal nonclaim residual classification is allowed",
            "valid_for_claim": False,
        }
    )

    decisions = rows_by_name["decision"]
    checks.append(
        {
            "validation_id": "VAL1874_6_decision",
            "status": "PASS"
            if any(row["decision"] == "PARENT_DOMAIN_VERTICALITY_NOT_DERIVED" for row in decisions)
            and any(row["decision"] == "RAB_CLASSIFIED_AS_EXPLICIT_RESIDUAL_FIELD_CURRENTLY" for row in decisions)
            else "FAIL",
            "detail": "decision ledger blocks verticality and classifies R_AB as residual",
            "valid_for_claim": False,
        }
    )

    next_targets = rows_by_name["next_target"]
    checks.append(
        {
            "validation_id": "VAL1874_7_next_target",
            "status": "PASS"
            if any(row["route_id"] == "NEXT1874_0_primary" and row["selection_status"] == "selected" for row in next_targets)
            else "FAIL",
            "detail": "1875 residual vector target selected",
            "valid_for_claim": False,
        }
    )

    flags_ok, flags_detail = all_claim_flags_false(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1874_8_claim_flags_false",
            "status": "PASS" if flags_ok else "FAIL",
            "detail": flags_detail,
            "valid_for_claim": False,
        }
    )

    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1874_9_csv_parse",
            "status": "PASS" if parse_ok else "FAIL",
            "detail": parse_detail,
            "valid_for_claim": False,
        }
    )

    copied_paths = [
        MICROSCOPE_RESIDUALS / OUTPUTS["residual_classification"].name,
        QUARANTINE / OUTPUTS["bound_requirements"].name,
        QUEUE / "JR1874_RAB_EXPLICIT_RESIDUAL_FIELD_CLASSIFICATION_NONCLAIM.csv",
        QUEUE / "JR1874_RAB_RESIDUAL_BOUND_REQUIREMENTS_NONCLAIM.csv",
    ]
    checks.append(
        {
            "validation_id": "VAL1874_10_branch_copies",
            "status": "PASS" if all(path.exists() for path in copied_paths) else "FAIL",
            "detail": ";".join(str(path) for path in copied_paths),
            "valid_for_claim": False,
        }
    )

    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append(
        {
            "validation_id": "VAL1874_11_pycache_absent",
            "status": "PASS" if not pycache.exists() else "FAIL",
            "detail": str(pycache),
            "valid_for_claim": False,
        }
    )

    formalization_hits = list(FORMALIZATION.rglob("*1874*")) if FORMALIZATION.exists() else []
    checks.append(
        {
            "validation_id": "VAL1874_12_formalization_untouched",
            "status": "PASS" if not formalization_hits else "FAIL",
            "detail": f"formalization_1874_count={len(formalization_hits)}",
            "valid_for_claim": False,
        }
    )

    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append(
        {
            "validation_id": "VAL1874_OVERALL",
            "status": "PASS" if fail_count == 0 else "FAIL",
            "detail": "1874 parent-domain verticality for R_AB or explicit residual-field checkpoint",
            "valid_for_claim": False,
        }
    )
    return checks


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", " ") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 1874 - Parent-Domain Verticality For R_AB Or Explicit Residual Field

**Private status:** nonclaim checkpoint. No derived local-GR, PPN, orbital, R10, WEP, clock, EM, or cosmology pass is claimed.

## Result

1874 tries the parent-domain route directly:

```text
Need: q:Phi_parent -> Q_obs and v_R in ker(Dq)
But: R_AB = ln(T^2 S) = 2 ln(J_q)
So: under the available observer-cell map, changing R_AB changes observed cell data.
Therefore: Dq[v_R] != 0 unless a new q_shape or parent constraint removes R_AB first.
```

The quotient-representative route remains mathematically attractive, but it is not constructed from MTS primitives. The constraint/no-pole route remains the best local-GR route, but `lambda_R`/no-pole is not parent-derived. So the non-smuggling current classification is:

```text
R_AB = explicit residual field until parent verticality or parent constraint is signed.
```

This does not kill the theory. It stops the theory from spending a theorem it has not earned. The next work is to build the residual-field coefficient vector so every future test knows exactly what has to be zero-derived or bounded.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Verticality Attempt

{markdown_table(rows_by_name["verticality_attempt"])}

## Domain Trilemma

{markdown_table(rows_by_name["trilemma"])}

## Residual Classification

{markdown_table(rows_by_name["residual_classification"])}

## Bound Requirements

{markdown_table(rows_by_name["bound_requirements"])}

## Claim Gate

{markdown_table(rows_by_name["claim_gate"])}

## Decision Ledger

{markdown_table(rows_by_name["decision"])}

## Next Target

{markdown_table(rows_by_name["next_target"])}

## Validation

{markdown_table(validation)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows_by_name = all_output_rows()
    for key, rows in rows_by_name.items():
        write_csv(OUTPUTS[key], rows)
    copy_branch_artifacts()
    remove_pycache()
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

BRANCH_ID = "MTS_R2FR_RAB_REDUCED_CONFIGURATION_OR_FINITE_STIFFNESS_2268"
DOC = ROOT / "2268-Y5-R2FR-RAB-reduced-configuration-parametrization-or-finite-stiffness-row.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2268_00_2267_doc",
        "source_key": "2267_doc",
        "source_path": ROOT / "2267-Y5-R2FR-RAB-lambdaR-origin-or-backreaction-elimination.md",
        "needles": ["RCS2267_0_local_parametrization", "LRR2267_0_reduced_configuration", "NEXT2267_0_primary"],
        "role": "handoff: reduced configuration selected after multiplier backreaction obstruction",
    },
    {
        "source_id": "SRC2268_01_2267_validation",
        "source_key": "2267_validation",
        "source_path": OUT / "P8_Y5_BRR545_2267_VALIDATION.csv",
        "needles": ["VAL2267_OVERALL", "PASS"],
        "role": "confirms 2267 passed before 2268 starts",
    },
    {
        "source_id": "SRC2268_02_08_phase_volume",
        "source_key": "phase_volume_08",
        "source_path": ROOT / "08-phase-volume-reciprocity-origin.md",
        "needles": ["phase_volume_reciprocity_motivated_not_parent_derived", "T sqrt(S) = 1.", "Generic volume preservation does not work."],
        "role": "early phase-volume result: right radial cell, not parent derived",
    },
    {
        "source_id": "SRC2268_03_10_observer",
        "source_key": "observer_10",
        "source_path": ROOT / "10-observer-map-symplectic-contract.md",
        "needles": ["J_q = T sqrt(S)", "R_AB = ln(T^2 S) = 2 ln(J_q).", "So the parent theory must do more than preserve canonical phase volume."],
        "role": "observer-cell Jacobian and exact missing theorem",
    },
    {
        "source_id": "SRC2268_04_2227_phase_import",
        "source_key": "phase_import_2227",
        "source_path": ROOT / "2227-Y5-R2FR-phase-volume-nonpropagating-qsector-origin-or-rejection.md",
        "needles": ["ORG2227_0_radial_cell_rule", "NO_ACCEPTED_ORIGIN", "VAL2227_OVERALL"],
        "role": "current R2FR phase-volume audit with no accepted origin",
    },
    {
        "source_id": "SRC2268_05_1554_phase_origin",
        "source_key": "phase_origin_1554",
        "source_path": ROOT / "1554-Y5-phase-volume-nonpropagating-qsector-origin-or-rejection.md",
        "needles": ["ORG1554_0_radial_cell_rule", "NO_ACCEPTED_ORIGIN", "VAL1554_14_overall"],
        "role": "older phase-volume origin audit imported by 2227",
    },
    {
        "source_id": "SRC2268_06_micro_action",
        "source_key": "micro_action",
        "source_path": PROJECT_ROOT / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md",
        "needles": ["A_MTS[ψ]", "g_{μν} = η_{μν}", "∂²_t ψ"],
        "role": "primitive psi action/covariance source checked for quotient derivation",
    },
    {
        "source_id": "SRC2268_07_vacuum_contract_04",
        "source_key": "vacuum_contract_04",
        "source_path": ROOT / "04-vacuum-reciprocity-action-contract.md",
        "needles": ["R_AB = ln(A B) = ln(T^2 S).", "T^2 S = 1", "d/dr [ W(r,L,fields) dR_AB/dr ] = J_R"],
        "role": "older reciprocal-strain action contract and finite current route",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2268_SOURCE_REGISTER.csv",
    "variable_split": OUT / "P8_Y5_PARENT_QLOC_2268_PHI_Q_VARIABLE_SPLIT.csv",
    "reduced_audit": OUT / "P8_Y5_PARENT_QLOC_2268_REDUCED_CONFIGURATION_AUDIT.csv",
    "origin_tests": OUT / "P8_Y5_PARENT_QLOC_2268_PHASE_VOLUME_PSI_ORIGIN_TESTS.csv",
    "finite_stiffness": OUT / "P8_Y5_PARENT_QLOC_2268_FINITE_STIFFNESS_QR_ROW.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2268_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2268_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2268_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2268_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2268_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2268_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_reduced": QUEUE / "JR2268_REDUCED_CONFIGURATION_AUDIT_NONCLAIM.csv",
    "queue_stiffness": QUEUE / "JR2268_FINITE_STIFFNESS_QR_ROW_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "RAB_reduced_configuration_or_finite_stiffness_refusal_2268.csv",
    "beta_docs": BETA_DOCS / "RAB_REDUCED_CONFIGURATION_OR_FINITE_STIFFNESS_2268_NONCLAIM.csv",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        try:
            return str(path.relative_to(PROJECT_ROOT)).replace("\\", "/")
        except ValueError:
            return str(path)


def validation_pass(path: Path) -> bool:
    if not path.exists():
        return False
    rows = read_csv(path)
    if not rows:
        return False
    id_key = next((key for key in ("check_id", "validation_id", "id") if key in rows[0]), "")
    result_key = next((key for key in ("result", "status") if key in rows[0]), "")
    if not result_key:
        return False
    overall = [row for row in rows if id_key and "overall" in row.get(id_key, "").lower()]
    return all(row.get(result_key, "").lower() == "pass" for row in (overall or rows))


def source_path(key: str) -> Path:
    return next(source["source_path"] for source in SOURCES if source["source_key"] == key)


def source_refs(*keys: str) -> str:
    return ";".join(rel(source_path(key)) for key in keys)


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCES:
        path = source["source_path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": rel(path),
                "exists": exists,
                "needles": ";".join(source["needles"]),
                "needles_present": exists and all(needle in text for needle in source["needles"]),
                "validation_overall_pass": validation_pass(path) if "validation" in source["source_key"] else "",
                "role": source["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def variable_split_rows() -> list[dict[str, Any]]:
    return [
        {
            "split_id": "PQS2268_0_definitions",
            "object": "local static radial metric block",
            "formula": "A=T^2, B=S, q:=R_AB=ln(AB), Phi:=1/4 ln(A/B)",
            "result": "A=exp(2Phi+q/2), B=exp(-2Phi+q/2)",
            "status": "EXACT_CHANGE_OF_VARIABLES",
            "valid_for_claim": False,
        },
        {
            "split_id": "PQS2268_1_observer_cell",
            "object": "radial observer configuration cell",
            "formula": "J_q=T sqrt(S)=sqrt(AB)=exp(q/2)",
            "result": "q=0 <=> J_q=1 <=> AB=T^2S=1",
            "status": "EXACT_IDENTITY",
            "valid_for_claim": False,
        },
        {
            "split_id": "PQS2268_2_reduced_branch",
            "object": "pre-variation reduced configuration seed",
            "formula": "q=0 before variation gives A=exp(2Phi), B=exp(-2Phi)",
            "result": "no lambda_R multiplier is required and no lambda_R D_A q backreaction is introduced",
            "status": "VALID_REDUCED_PARAMETRIZATION_SEED",
            "valid_for_claim": False,
        },
        {
            "split_id": "PQS2268_3_weak_field",
            "object": "first PPN scalar lane",
            "formula": "A=1-L+O(L^2) with q=0 gives B=A^-1=1+L+O(L^2)",
            "result": "gamma=1 at first order if the reduced branch is parent-derived",
            "status": "CONDITIONAL_LOCAL_LIMIT",
            "valid_for_claim": False,
        },
    ]


def reduced_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "RCA2268_0_reduced_parametrization",
            "candidate": "A=exp(2Phi), B=exp(-2Phi)",
            "what_closes": "R_AB=0 kinematically before variation; avoids post-hoc multiplier backreaction",
            "remaining_gap": "why q is absent/frozen in the parent local vacuum branch",
            "current_status": "VALID_SEED_NOT_PARENT_DERIVED",
            "source_paths": source_refs("2267_doc", "observer_10"),
            "valid_for_claim": False,
        },
        {
            "audit_id": "RCA2268_1_radial_cell_rule",
            "candidate": "J_q=T sqrt(S)=1",
            "what_closes": "selects p=1 exactly for S=(1-L)^(-p)",
            "remaining_gap": "separate radial cell preservation is exactly the missing parent theorem",
            "current_status": "MOTIVATED_NOT_PARENT_DERIVED",
            "source_paths": source_refs("phase_volume_08", "phase_import_2227"),
            "valid_for_claim": False,
        },
        {
            "audit_id": "RCA2268_2_generic_phase_volume",
            "candidate": "canonical/Liouville phase-volume preservation",
            "what_closes": "nothing specific to p=1 because J_q J_p=1 for every p",
            "remaining_gap": "generic phase volume does not select the GR scalar lane",
            "current_status": "REJECTED_TOO_WEAK",
            "source_paths": source_refs("observer_10", "phase_import_2227"),
            "valid_for_claim": False,
        },
        {
            "audit_id": "RCA2268_3_psi_quotient",
            "candidate": "psi covariance quotient removes q",
            "what_closes": "would be the cleanest fundamental derivation if q lies in ker(Dq_parent) or is absent from the reduced metric map",
            "remaining_gap": "current psi action gives emergent covariance metric but no determinant/radial-cell quotient theorem",
            "current_status": "ROOT_ROUTE_OPEN_MAP_MISSING",
            "source_paths": source_refs("micro_action"),
            "valid_for_claim": False,
        },
        {
            "audit_id": "RCA2268_4_finite_stiffness",
            "candidate": "algebraic finite stiffness q-sector",
            "what_closes": "keeps q nonpropagating without gradient hair and makes q_R testable",
            "remaining_gap": "M_R^2 stiffness and source coefficient j_R must be parent-derived",
            "current_status": "TESTABLE_FALLBACK_SCHEMA_READY_INPUTS_MISSING",
            "source_paths": source_refs("phase_import_2227", "vacuum_contract_04"),
            "valid_for_claim": False,
        },
        {
            "audit_id": "RCA2268_5_verdict",
            "candidate": "derived reduced local GR branch",
            "what_closes": "none at claim level",
            "remaining_gap": "no parent theorem yet for q=0/reduced configuration; finite q_R still lacks stiffness/source coefficients",
            "current_status": "REDUCED_CONFIGURATION_NOT_DERIVED_CURRENT_CORPUS",
            "source_paths": source_refs("2267_doc", "phase_volume_08", "observer_10", "phase_import_2227", "micro_action"),
            "valid_for_claim": False,
        },
    ]


def origin_test_rows() -> list[dict[str, Any]]:
    return [
        {
            "test_id": "OT2268_0_phase_cell_parent",
            "test": "Does the corpus derive separate radial configuration-cell conservation J_q=1?",
            "evidence": "08 and 2227 identify J_q=1 as the right condition but state it is motivated/not parent derived",
            "result": "FAIL_CURRENT_CLAIM",
            "next_required_input": "parent conservation/no-charge theorem for radial t-r observer cell",
            "valid_for_claim": False,
        },
        {
            "test_id": "OT2268_1_generic_liouville",
            "test": "Can generic Liouville/canonical volume preservation derive p=1?",
            "evidence": "10 and 2227 show J_q J_p=1 is true for every p",
            "result": "REJECTED_TOO_WEAK",
            "next_required_input": "a non-generic cell-specific conservation law",
            "valid_for_claim": False,
        },
        {
            "test_id": "OT2268_2_psi_covariance",
            "test": "Does psi covariance action derive q=0 or remove q from the metric map?",
            "evidence": "core action says g_munu emerges from smoothed psi covariance but supplies no q quotient/determinant theorem",
            "result": "OPEN_MAP_MISSING",
            "next_required_input": "explicit psi-to-(Phi,q) map showing q absent, gauge, or minimized",
            "valid_for_claim": False,
        },
        {
            "test_id": "OT2268_3_reduced_variation",
            "test": "If q=0 is imposed before variation, is lambda_R backreaction avoided?",
            "evidence": "2267 generic multiplier backreaction is avoided because no multiplier is introduced",
            "result": "PASS_CONDITIONAL_SEED",
            "next_required_input": "parent justification for imposing q=0 pre-variation",
            "valid_for_claim": False,
        },
    ]


def finite_stiffness_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "FSQ2268_0_algebraic_stiffness_template",
            "target": "q_R",
            "branch": "finite_nonpropagating_q",
            "parent_block": "L_q = -1/2 M_R^2 q^2 + J_R q, q=R_AB",
            "variation": "M_R^2 q = J_R under this sign convention",
            "weak_field_projection": "if J_R=j_R L+O(L^2), then q=R_AB=(j_R/M_R^2)L+O(L^2), so q_R=j_R/M_R^2",
            "required_parent_inputs": "M_R^2;j_R;normalization;units;matter/readout source path",
            "current_status": "SCHEMA_READY_PARENT_INPUTS_MISSING",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "FSQ2268_1_no_gradient_guard",
            "target": "reciprocal_charge_Q_R",
            "branch": "finite_nonpropagating_q",
            "parent_block": "no nabla q term in L_q",
            "variation": "no W q' exterior equation and no conserved Q_R hair from this block",
            "weak_field_projection": "finite q is algebraic/source-local rather than Q_R/r hair",
            "required_parent_inputs": "proof no derivative q operator is generated by parent/boundary terms",
            "current_status": "GUARD_READY_PARENT_PROOF_MISSING",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "FSQ2268_2_external_bounds_guard",
            "target": "external_local_bounds",
            "branch": "comparator_only",
            "parent_block": "none",
            "variation": "published bounds cannot set M_R^2 or j_R",
            "weak_field_projection": "bounds may screen q_R after q_R is parent-sourced",
            "required_parent_inputs": "parent q_R first, comparator second",
            "current_status": "GUARD_ONLY",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "refusal_id": "REF2268_0_reduced_config_claim",
            "attempted_claim": "A=exp(2Phi), B=exp(-2Phi) is parent-derived",
            "runner_result": "BLOCKED",
            "blocked_by": "RCA2268_5_verdict=REDUCED_CONFIGURATION_NOT_DERIVED_CURRENT_CORPUS",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2268_1_phase_volume_claim",
            "attempted_claim": "phase-volume derives local GR/Newton",
            "runner_result": "REJECTED_TOO_WEAK",
            "blocked_by": "generic phase volume does not select p=1 and radial cell rule is extra",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2268_2_psi_quotient_claim",
            "attempted_claim": "psi covariance removes q",
            "runner_result": "BLOCKED",
            "blocked_by": "explicit psi-to-(Phi,q) quotient map missing",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2268_3_finite_qR_score",
            "attempted_claim": "finite q_R stiffness row can be scored",
            "runner_result": "BLOCKED",
            "blocked_by": "M_R^2 and j_R parent inputs missing",
            "score_eligible": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "CG2268_0_exact_split",
            "claim": "Phi/q split is exact",
            "gate_pass": False,
            "reason": "exact math is recorded, but valid_for_claim remains false because it is not a physics derivation by itself",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2268_1_reduced_parent",
            "claim": "reduced configuration is parent-derived",
            "gate_pass": False,
            "reason": "radial cell or psi quotient theorem missing",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2268_2_local_GR",
            "claim": "derived local GR/Newton/PPN",
            "gate_pass": False,
            "reason": "q=0 branch is a conditional seed, not yet parent-derived",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2268_3_finite_qR",
            "claim": "finite q_R residual has source-backed value",
            "gate_pass": False,
            "reason": "M_R^2 and j_R are missing",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2268_0_exact_split",
            "decision": "PHI_Q_SPLIT_LOCKED",
            "reason": "A=exp(2Phi+q/2), B=exp(-2Phi+q/2), q=R_AB exactly separates Newton potential from reciprocal strain",
            "next_action": "use this split for all future local branch derivations",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2268_1_reduced_seed",
            "decision": "REDUCED_CONFIGURATION_SEED_VALID_BUT_NOT_DERIVED",
            "reason": "q=0 before variation avoids lambda backreaction and gives gamma=1, but parent theorem is absent",
            "next_action": "try to derive q absence from radial cell conservation or psi quotient",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2268_2_finite_fallback",
            "decision": "FINITE_STIFFNESS_QR_SCHEMA_OPENED",
            "reason": "if q=0 cannot be derived, algebraic stiffness gives a nonpropagating testable q_R row without Q_R/r hair",
            "next_action": "source M_R^2 and j_R from parent theory before scoring",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2268_3_next",
            "decision": "RADIAL_CELL_THEOREM_OR_STIFFNESS_COEFFICIENT_NEXT",
            "reason": "these are the two honest ways forward after the split",
            "next_action": "2269-Y5-R2FR-radial-cell-conservation-theorem-or-qR-stiffness-coefficient.md",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "NEXT2268_0_primary",
            "next_target": "2269-Y5-R2FR-radial-cell-conservation-theorem-or-qR-stiffness-coefficient.md",
            "script": "scripts/Y5_R2FR_radial_cell_conservation_theorem_or_qR_stiffness_coefficient_2269.py",
            "objective": "try to prove the radial observer configuration cell J_q=1 from MTS primitives/psi quotient; if it fails, source the finite algebraic stiffness coefficients M_R^2 and j_R for q_R",
            "selection_status": "selected",
            "success_condition": "J_q=1 is parent-derived before variation, or q_R=j_R/M_R^2 becomes a source-backed nonclaim coefficient row ready for comparator gates",
        }
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": "BC2268_reduced",
            "source_path": rel(OUTPUTS["reduced_audit"]),
            "target_path": rel(COPY_TARGETS["queue_reduced"]),
            "target_exists": COPY_TARGETS["queue_reduced"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["queue_reduced"]),
            "reason": "reduced configuration audit copied as nonclaim queue",
        },
        {
            "copy_id": "BC2268_stiffness",
            "source_path": rel(OUTPUTS["finite_stiffness"]),
            "target_path": rel(COPY_TARGETS["queue_stiffness"]),
            "target_exists": COPY_TARGETS["queue_stiffness"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["queue_stiffness"]),
            "reason": "finite stiffness q_R schema copied as nonclaim queue",
        },
        {
            "copy_id": "BC2268_branch_wep",
            "source_path": rel(OUTPUTS["claim_gates"]),
            "target_path": rel(COPY_TARGETS["branch_wep"]),
            "target_exists": COPY_TARGETS["branch_wep"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["branch_wep"]),
            "reason": "branch-locked WEP/local refusal gates",
        },
        {
            "copy_id": "BC2268_beta_docs",
            "source_path": rel(OUTPUTS["decision"]),
            "target_path": rel(COPY_TARGETS["beta_docs"]),
            "target_exists": COPY_TARGETS["beta_docs"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["beta_docs"]),
            "reason": "portable reduced-configuration decision ledger",
        },
    ]


def table(headers: list[str], rows: list[dict[str, Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", " ") for header in headers) + " |")
    return "\n".join(lines)


def validation_rows() -> list[dict[str, Any]]:
    source_rows = read_csv(OUTPUTS["source_register"])
    split = read_csv(OUTPUTS["variable_split"])
    reduced = read_csv(OUTPUTS["reduced_audit"])
    origin = read_csv(OUTPUTS["origin_tests"])
    stiffness = read_csv(OUTPUTS["finite_stiffness"])
    refusal = read_csv(OUTPUTS["refusal"])
    claims = read_csv(OUTPUTS["claim_gates"])
    next_rows = read_csv(OUTPUTS["next_target"])
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks = [
        ("VAL2268_0_sources_exist", all(row["exists"].lower() == "true" for row in source_rows), "all cited source paths exist"),
        ("VAL2268_1_needles_present", all(row["needles_present"].lower() == "true" for row in source_rows), "all cited source needles are present"),
        (
            "VAL2268_2_prior_validation",
            any(row["source_key"] == "2267_validation" and row["validation_overall_pass"].lower() == "true" for row in source_rows),
            "2267 validation passes",
        ),
        (
            "VAL2268_3_phi_q_split",
            any(row["split_id"] == "PQS2268_0_definitions" and row["status"] == "EXACT_CHANGE_OF_VARIABLES" for row in split)
            and any(row["split_id"] == "PQS2268_2_reduced_branch" for row in split),
            "Phi/q split and reduced branch seed are written",
        ),
        (
            "VAL2268_4_reduced_not_claimed",
            any(row["audit_id"] == "RCA2268_5_verdict" and row["current_status"] == "REDUCED_CONFIGURATION_NOT_DERIVED_CURRENT_CORPUS" for row in reduced)
            and all(row["valid_for_claim"].lower() == "false" for row in reduced),
            "reduced configuration is not falsely claimed",
        ),
        (
            "VAL2268_5_origin_tests",
            {row["test_id"] for row in origin}
            >= {"OT2268_0_phase_cell_parent", "OT2268_1_generic_liouville", "OT2268_2_psi_covariance", "OT2268_3_reduced_variation"},
            "phase-volume, Liouville, psi, and reduced-variation tests written",
        ),
        (
            "VAL2268_6_finite_stiffness_nonclaim",
            any(row["row_id"] == "FSQ2268_0_algebraic_stiffness_template" for row in stiffness)
            and all(row["score_ready"].lower() == "false" and row["valid_for_claim"].lower() == "false" for row in stiffness),
            "finite stiffness q_R row remains nonclaim",
        ),
        (
            "VAL2268_7_refusal_blocks",
            all(row["score_eligible"].lower() == "false" and row["valid_for_claim"].lower() == "false" for row in refusal),
            "refusal runner blocks local claims",
        ),
        (
            "VAL2268_8_claim_gates_blocked",
            all(row["gate_pass"].lower() == "false" and row["valid_for_claim"].lower() == "false" for row in claims),
            "claim gates are all blocked",
        ),
        (
            "VAL2268_9_next_selected",
            any(row["route_id"] == "NEXT2268_0_primary" and row["selection_status"] == "selected" for row in next_rows),
            "2269 target selected",
        ),
        ("VAL2268_10_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 2268 CSVs parse"),
        (
            "VAL2268_11_no_claim_flags",
            not any(
                row.get(key, "").lower() == "true"
                for path in generated_csvs
                for row in read_csv(path)
                for key in ("score_ready", "accepted_ready", "valid_for_claim", "claim_allowed", "gate_pass")
            ),
            "no generated score/claim/gate flags are true",
        ),
        (
            "VAL2268_12_branch_copies",
            all(row["target_exists"].lower() == "true" and row["target_parses"].lower() == "true" for row in read_csv(OUTPUTS["branch_copies"])),
            "branch/queue copies exist and parse",
        ),
        ("VAL2268_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        (
            "VAL2268_14_formalization_no_2268",
            not any(
                path.is_file()
                and (path.name.startswith("2268-") or (path.name.startswith("P8_Y5") and "2268" in path.name))
                for path in FORMALIZATION.rglob("*")
            ),
            "formalization-workbench has no 2268 output files",
        ),
    ]
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2268_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "2268 locks the Phi/q split, keeps reduced configuration nonclaim, opens finite stiffness q_R schema, and selects 2269",
        }
    )
    return rows


def write_doc() -> None:
    source_rows = read_csv(OUTPUTS["source_register"])
    split = read_csv(OUTPUTS["variable_split"])
    reduced = read_csv(OUTPUTS["reduced_audit"])
    origin = read_csv(OUTPUTS["origin_tests"])
    stiffness = read_csv(OUTPUTS["finite_stiffness"])
    refusal = read_csv(OUTPUTS["refusal"])
    claims = read_csv(OUTPUTS["claim_gates"])
    decisions = read_csv(OUTPUTS["decision"])
    next_rows = read_csv(OUTPUTS["next_target"])
    copies = read_csv(OUTPUTS["branch_copies"])
    validation = read_csv(OUTPUTS["validation"])
    sections = [
        "# 2268 - Y5/R2FR R_AB Reduced Configuration Parametrization Or Finite Stiffness Row",
        "",
        "## Verdict",
        "",
        "2268 locks a cleaner local variable split. For the static radial block, define `q=R_AB=ln(AB)` and `Phi=1/4 ln(A/B)`. Then exactly `A=exp(2Phi+q/2)` and `B=exp(-2Phi+q/2)`. The proposed local-GR branch is the pre-variation reduced configuration `q=0`, giving `A=exp(2Phi)`, `B=exp(-2Phi)`, `AB=1`, and no `lambda_R` backreaction.",
        "",
        "That is a strong parametrization result, but not yet the parent derivation. Existing phase-volume work already says the radial cell rule `J_q=T sqrt(S)=1` selects the GR lane, while generic Liouville/canonical phase volume is too weak. The core `psi` action gives an emergent covariance metric but no current source proves that `q` is absent, quotient-vertical, or minimized.",
        "",
        "So the branch is sharper: either derive `J_q=1` / `q=0` as a pre-variation MTS theorem, or use the finite algebraic stiffness fallback `q_R=j_R/M_R^2` as a testable nonclaim residual. No local-GR/Newton, PPN, R10, WEP, clock, orbital, `R_AB=0`, `Q_R=0`, or finite residual pass claim is made.",
        "",
        "## Source Register",
        table(["source_id", "source_key", "source_path", "exists", "needles_present", "validation_overall_pass", "role"], source_rows),
        "",
        "## Phi/q Variable Split",
        table(["split_id", "object", "formula", "result", "status", "valid_for_claim"], split),
        "",
        "## Reduced Configuration Audit",
        table(["audit_id", "candidate", "what_closes", "remaining_gap", "current_status", "source_paths", "valid_for_claim"], reduced),
        "",
        "## Phase-Volume / Psi Origin Tests",
        table(["test_id", "test", "evidence", "result", "next_required_input", "valid_for_claim"], origin),
        "",
        "## Finite Stiffness q_R Row",
        table(["row_id", "target", "branch", "parent_block", "variation", "weak_field_projection", "required_parent_inputs", "current_status", "score_ready", "valid_for_claim"], stiffness),
        "",
        "## Refusal Runner",
        table(["refusal_id", "attempted_claim", "runner_result", "blocked_by", "score_eligible", "valid_for_claim"], refusal),
        "",
        "## Claim Gates",
        table(["claim_id", "claim", "gate_pass", "reason", "valid_for_claim"], claims),
        "",
        "## Decision Ledger",
        table(["decision_id", "decision", "reason", "next_action", "valid_for_claim"], decisions),
        "",
        "## Next Target",
        table(["route_id", "next_target", "script", "objective", "selection_status", "success_condition"], next_rows),
        "",
        "## Branch Copies",
        table(["copy_id", "source_path", "target_path", "target_exists", "target_parses", "reason"], copies),
        "",
        "## Validation",
        table(["check_id", "result", "detail"], validation),
        "",
        "## Working Interpretation",
        "",
        "This is the best shape of the local problem so far. We should work in `(Phi,q)` from here. `Phi` is the Newton/Schwarzschild-like scalar lane; `q` is the reciprocal-strain debt. If MTS can derive `q=0` before variation, the local-GR route becomes much cleaner. If not, `q` becomes a finite algebraic residual with a stiffness/source coefficient to test instead of handwaving away.",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    for directory in (OUT, QUEUE, MICROSCOPE, BETA_DOCS):
        directory.mkdir(parents=True, exist_ok=True)

    write_csv(OUTPUTS["source_register"], source_register_rows())
    write_csv(OUTPUTS["variable_split"], variable_split_rows())
    write_csv(OUTPUTS["reduced_audit"], reduced_audit_rows())
    write_csv(OUTPUTS["origin_tests"], origin_test_rows())
    write_csv(OUTPUTS["finite_stiffness"], finite_stiffness_rows())
    write_csv(OUTPUTS["refusal"], refusal_rows())
    write_csv(OUTPUTS["claim_gates"], claim_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next_target"], next_target_rows())

    shutil.copyfile(OUTPUTS["reduced_audit"], COPY_TARGETS["queue_reduced"])
    shutil.copyfile(OUTPUTS["finite_stiffness"], COPY_TARGETS["queue_stiffness"])
    shutil.copyfile(OUTPUTS["claim_gates"], COPY_TARGETS["branch_wep"])
    shutil.copyfile(OUTPUTS["decision"], COPY_TARGETS["beta_docs"])
    write_csv(OUTPUTS["branch_copies"], branch_copy_rows())

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

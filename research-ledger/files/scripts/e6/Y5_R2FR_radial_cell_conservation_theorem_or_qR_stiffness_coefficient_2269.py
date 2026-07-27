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

BRANCH_ID = "MTS_R2FR_RADIAL_CELL_THEOREM_OR_QR_STIFFNESS_2269"
DOC = ROOT / "2269-Y5-R2FR-radial-cell-conservation-theorem-or-qR-stiffness-coefficient.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2269_00_2268_doc",
        "source_key": "2268_doc",
        "source_path": ROOT / "2268-Y5-R2FR-RAB-reduced-configuration-parametrization-or-finite-stiffness-row.md",
        "needles": ["PQS2268_0_definitions", "FSQ2268_0_algebraic_stiffness_template", "NEXT2268_0_primary"],
        "role": "handoff: Phi/q split locked and 2269 selected",
    },
    {
        "source_id": "SRC2269_01_2268_validation",
        "source_key": "2268_validation",
        "source_path": OUT / "P8_Y5_BRR545_2268_VALIDATION.csv",
        "needles": ["VAL2268_OVERALL", "PASS"],
        "role": "confirms 2268 passed before 2269 starts",
    },
    {
        "source_id": "SRC2269_02_2268_stiffness",
        "source_key": "2268_stiffness",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2268_FINITE_STIFFNESS_QR_ROW.csv",
        "needles": ["FSQ2268_0_algebraic_stiffness_template", "M_R^2", "j_R"],
        "role": "finite algebraic stiffness q_R template from 2268",
    },
    {
        "source_id": "SRC2269_03_09_radial_hamiltonian",
        "source_key": "radial_hamiltonian_09",
        "source_path": ROOT / "09-hamiltonian-radial-cell-derivation.md",
        "needles": ["hamiltonian_radial_cell_sharpened_not_parent_derived", "separate radial cell gives p=1 exactly", "not yet a parent derivation"],
        "role": "Hamiltonian/radial-cell attempt: sharpened but not parent-derived",
    },
    {
        "source_id": "SRC2269_04_10_observer",
        "source_key": "observer_10",
        "source_path": ROOT / "10-observer-map-symplectic-contract.md",
        "needles": ["J_q = T sqrt(S)", "J_q J_p", "J_q = 1."],
        "role": "observer-cell Jacobian and missing theorem",
    },
    {
        "source_id": "SRC2269_05_11_cell_current",
        "source_key": "cell_current_11",
        "source_path": ROOT / "11-cell-current-origin-attempt.md",
        "needles": ["cell_current_origin_no_charge_obstruction", "Q_R = constant.", "no-charge theorem"],
        "role": "cell-current route and no-charge obstruction",
    },
    {
        "source_id": "SRC2269_06_12_noether",
        "source_key": "noether_12",
        "source_path": ROOT / "12-gauge-noether-origin-audit.md",
        "needles": ["gauge_noether_origin_not_derived_closure_only", "first-class parent constraint", "Noether identity derives R_AB=0;"],
        "role": "gauge/Noether route remains closure-only",
    },
    {
        "source_id": "SRC2269_07_2228_gauge",
        "source_key": "gauge_2228",
        "source_path": ROOT / "2228-Y5-R2FR-gauge-noether-zero-charge-qsector-origin-audit.md",
        "needles": ["NO_ACCEPTED_ZERO_CHARGE_ORIGIN", "FIRST_CLASS_CONTRACT_ONLY", "VAL2228_OVERALL"],
        "role": "current R2FR gauge/Noether zero-charge audit",
    },
    {
        "source_id": "SRC2269_08_micro_action",
        "source_key": "micro_action",
        "source_path": PROJECT_ROOT / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md",
        "needles": ["A_MTS[ψ]", "g_{μν} = η_{μν}", "∂²_t ψ"],
        "role": "primitive psi action checked for radial-cell quotient/stiffness source",
    },
    {
        "source_id": "SRC2269_09_vacuum_contract_04",
        "source_key": "vacuum_contract_04",
        "source_path": ROOT / "04-vacuum-reciprocity-action-contract.md",
        "needles": ["R_AB = ln(A B) = ln(T^2 S).", "d/dr [ W(r,L,fields) dR_AB/dr ] = J_R", "R_AB(infinity) = 0."],
        "role": "older reciprocal-strain current/action contract",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2269_SOURCE_REGISTER.csv",
    "theorem_attempt": OUT / "P8_Y5_PARENT_QLOC_2269_RADIAL_CELL_THEOREM_ATTEMPT.csv",
    "route_audit": OUT / "P8_Y5_PARENT_QLOC_2269_RADIAL_CELL_ROUTE_AUDIT.csv",
    "stiffness_intake": OUT / "P8_Y5_PARENT_QLOC_2269_QR_STIFFNESS_COEFFICIENT_INTAKE.csv",
    "claim_requirements": OUT / "P8_Y5_PARENT_QLOC_2269_CLAIM_REQUIREMENTS.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2269_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2269_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2269_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2269_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2269_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2269_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_theorem": QUEUE / "JR2269_RADIAL_CELL_THEOREM_ATTEMPT_NONCLAIM.csv",
    "queue_stiffness": QUEUE / "JR2269_QR_STIFFNESS_COEFFICIENT_INTAKE_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "RAB_radial_cell_or_stiffness_refusal_2269.csv",
    "beta_docs": BETA_DOCS / "RAB_RADIAL_CELL_OR_STIFFNESS_2269_NONCLAIM.csv",
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


def theorem_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "RCT2269_0_identity",
            "target": "radial cell theorem",
            "statement": "J_q=T sqrt(S)=exp(q/2), q=R_AB=ln(T^2S). Therefore J_q=1 iff q=0 iff AB=1.",
            "proof_status": "EXACT_IDENTITY",
            "missing_for_claim": "identity is not a parent conservation theorem",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "RCT2269_1_conservation_to_zero",
            "target": "constant radial cell",
            "statement": "If a parent local-vacuum law gives partial_r ln(J_q)=0 and asymptotic flatness gives J_q(infinity)=1, then J_q=1 everywhere on the branch.",
            "proof_status": "EXACT_CONDITIONAL",
            "missing_for_claim": "parent law partial_r ln(J_q)=0 is not derived",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "RCT2269_2_current_route",
            "target": "cell-current no-charge theorem",
            "statement": "A derivative current law partial_r(W partial_r q)=0 gives W q'=Q_R and q=q_infinity+hair unless Q_R=0 is separately proved.",
            "proof_status": "REJECTED_AS_ZERO_PROOF",
            "missing_for_claim": "no-charge theorem/proper boundary charge proof",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "RCT2269_3_first_class_route",
            "target": "first-class radial-cell constraint",
            "statement": "A parent first-class constraint C_R=q with zero/proper boundary charge could make q=0 a physical quotient condition.",
            "proof_status": "CONTRACT_ONLY",
            "missing_for_claim": "parent symplectic potential, generator, Q_R boundary term, bracket closure, degree count, and matter map",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "RCT2269_4_psi_quotient_route",
            "target": "psi-to-(Phi,q) quotient",
            "statement": "If the psi covariance map lands only in Phi or places q in a quotient-vertical direction, the reduced configuration could be fundamental.",
            "proof_status": "OPEN_MAP_MISSING",
            "missing_for_claim": "explicit psi covariance determinant/radial-cell map",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "RCT2269_5_verdict",
            "target": "J_q=1 parent theorem",
            "statement": "No current route proves the parent radial-cell theorem; reduced q=0 remains a clean seed, not a derived local-GR branch.",
            "proof_status": "RADIAL_CELL_THEOREM_NOT_DERIVED_CURRENT_CORPUS",
            "missing_for_claim": "one of RCT2269_1, RCT2269_3, or RCT2269_4 must close with source paths",
            "valid_for_claim": False,
        },
    ]


def route_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RRA2269_0_radial_cell_conservation",
            "route": "parent conservation of J_q",
            "what_would_work": "partial_r ln(J_q)=0 plus flat boundary gives J_q=1",
            "current_blocker": "no parent conservation law for the separate configuration cell",
            "status": "BEST_THEOREM_ROUTE_NOT_DERIVED",
            "source_paths": source_refs("radial_hamiltonian_09", "observer_10"),
            "valid_for_claim": False,
        },
        {
            "route_id": "RRA2269_1_generic_liouville",
            "route": "canonical phase-volume preservation",
            "what_would_work": "would need to select J_q=1 rather than only J_q J_p=1",
            "current_blocker": "J_q J_p=1 is true for every p and does not select the GR lane",
            "status": "REJECTED_TOO_WEAK",
            "source_paths": source_refs("observer_10"),
            "valid_for_claim": False,
        },
        {
            "route_id": "RRA2269_2_cell_current",
            "route": "conserved reciprocal-cell current",
            "what_would_work": "current conservation plus parent no-charge theorem Q_R=0",
            "current_blocker": "ordinary current conservation gives Q_R constant, not zero",
            "status": "REJECTED_NO_CHARGE_OBSTRUCTION",
            "source_paths": source_refs("cell_current_11", "vacuum_contract_04"),
            "valid_for_claim": False,
        },
        {
            "route_id": "RRA2269_3_gauge_noether",
            "route": "gauge/Noether zero-charge origin",
            "what_would_work": "first-class parent constraint with differentiable generator and zero/proper boundary charge",
            "current_blocker": "coordinate/observer-gauge shortcuts and generic Noether identities fail; first-class structure missing",
            "status": "CONTRACT_ONLY_NOT_PRESENT",
            "source_paths": source_refs("noether_12", "gauge_2228"),
            "valid_for_claim": False,
        },
        {
            "route_id": "RRA2269_4_finite_stiffness",
            "route": "algebraic finite stiffness q-sector",
            "what_would_work": "parent supplies M_R^2 and j_R so q_R=j_R/M_R^2 can be tested",
            "current_blocker": "no parent stiffness/source coefficients found in current corpus",
            "status": "FALLBACK_SCHEMA_READY_INPUTS_MISSING",
            "source_paths": source_refs("2268_stiffness", "micro_action"),
            "valid_for_claim": False,
        },
    ]


def stiffness_intake_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "SCI2269_0_MR2",
            "coefficient": "M_R^2",
            "definition": "algebraic stiffness multiplying q^2/2 in L_q",
            "required_source": "parent action term or psi/quotient expansion coefficient",
            "units_or_normalization": "same density normalization as J_R/q source; must be declared",
            "current_value": "MISSING_PARENT_COEFFICIENT",
            "status": "NOT_SCORE_READY",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "SCI2269_1_jR",
            "coefficient": "j_R",
            "definition": "coefficient of J_R=j_R L+O(L^2) in local weak-field source expansion",
            "required_source": "matter/readout coupling variation in the q direction",
            "units_or_normalization": "same normalization as M_R^2 times dimensionless q",
            "current_value": "MISSING_PARENT_SOURCE_COEFFICIENT",
            "status": "NOT_SCORE_READY",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "SCI2269_2_qR",
            "coefficient": "q_R",
            "definition": "q_R=j_R/M_R^2 when L_q=-1/2 M_R^2 q^2+J_R q and J_R=j_R L",
            "required_source": "SCI2269_0_MR2 and SCI2269_1_jR with compatible units",
            "units_or_normalization": "dimensionless after matching L=2GM/(rc^2)",
            "current_value": "MISSING_RATIO",
            "status": "NOT_SCORE_READY",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "SCI2269_3_no_gradient",
            "coefficient": "Q_R_guard",
            "definition": "proof that no nabla q term or boundary term generates W q'=Q_R hair",
            "required_source": "parent operator inventory and boundary variation",
            "units_or_normalization": "boolean theorem-zero guard, not a numeric fit",
            "current_value": "MISSING_OPERATOR_INVENTORY",
            "status": "NOT_SCORE_READY",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "SCI2269_4_external_bounds",
            "coefficient": "comparator_bounds",
            "definition": "PPN/R10/clock/orbital gates may screen q_R after q_R is parent-sourced",
            "required_source": "external bounds plus parent q_R; bounds alone forbidden as theory value",
            "units_or_normalization": "arena-specific",
            "current_value": "COMPARATOR_ONLY",
            "status": "GUARD_ONLY",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def claim_requirement_rows() -> list[dict[str, Any]]:
    return [
        {
            "requirement_id": "REQ2269_0_Jq_theorem",
            "claim_path": "derived reduced local branch",
            "must_have": "parent theorem for J_q=1 or q absent before variation",
            "current_status": "MISSING",
            "valid_for_claim": False,
        },
        {
            "requirement_id": "REQ2269_1_no_charge",
            "claim_path": "derived reduced local branch",
            "must_have": "zero/proper Q_R boundary charge and no reciprocal hair",
            "current_status": "MISSING",
            "valid_for_claim": False,
        },
        {
            "requirement_id": "REQ2269_2_matter_map",
            "claim_path": "derived reduced local branch",
            "must_have": "matter/readout descent so q is not re-sourced by clocks/WEP/PPN",
            "current_status": "MISSING",
            "valid_for_claim": False,
        },
        {
            "requirement_id": "REQ2269_3_beta_second_order",
            "claim_path": "derived GR/Newton/PPN branch",
            "must_have": "second-order beta/conservation completion after q=0",
            "current_status": "MISSING",
            "valid_for_claim": False,
        },
        {
            "requirement_id": "REQ2269_4_finite_score",
            "claim_path": "finite q_R residual branch",
            "must_have": "M_R^2, j_R, units, normalization, no-gradient guard, and comparator gates",
            "current_status": "MISSING",
            "valid_for_claim": False,
        },
    ]


def refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "refusal_id": "REF2269_0_Jq_claim",
            "attempted_claim": "J_q=1 is parent-derived",
            "runner_result": "BLOCKED",
            "blocked_by": "RCT2269_5_verdict=RADIAL_CELL_THEOREM_NOT_DERIVED_CURRENT_CORPUS",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2269_1_current_claim",
            "attempted_claim": "cell current conservation kills Q_R",
            "runner_result": "REJECTED_NO_CHARGE_OBSTRUCTION",
            "blocked_by": "ordinary current conservation leaves Q_R constant",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2269_2_gauge_claim",
            "attempted_claim": "gauge/Noether shortcut derives R_AB=0",
            "runner_result": "REJECTED_OR_CONTRACT_ONLY",
            "blocked_by": "2228 rejects shortcuts; first-class contract not supplied",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2269_3_qR_score",
            "attempted_claim": "q_R stiffness row can be scored",
            "runner_result": "BLOCKED",
            "blocked_by": "M_R^2, j_R, and no-gradient guard missing",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2269_4_local_GR",
            "attempted_claim": "derived local GR/Newton/PPN",
            "runner_result": "BLOCKED",
            "blocked_by": "reduced theorem and finite residual branches both lack parent inputs",
            "score_eligible": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "CG2269_0_radial_cell",
            "claim": "radial-cell theorem J_q=1",
            "gate_pass": False,
            "reason": "only exact conditional identities are available; parent conservation theorem missing",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2269_1_first_class",
            "claim": "first-class q constraint/no-charge origin",
            "gate_pass": False,
            "reason": "contract exists but parent symplectic/generator/boundary package missing",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2269_2_stiffness",
            "claim": "finite stiffness q_R source row",
            "gate_pass": False,
            "reason": "M_R^2 and j_R not sourced",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2269_3_local_GR",
            "claim": "derived local GR/Newton/PPN",
            "gate_pass": False,
            "reason": "not achieved",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2269_0_theorem",
            "decision": "RADIAL_CELL_THEOREM_NOT_DERIVED",
            "reason": "J_q=1 is exact and powerful, but current sources do not derive its parent conservation/no-charge law",
            "next_action": "do not promote q=0 reduced branch to local-GR claim",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2269_1_route_priority",
            "decision": "FIRST_CLASS_OR_PSI_QUOTIENT_REMAINS_ONLY_CLEAN_PROMOTION",
            "reason": "generic phase volume, current conservation, and gauge/Noether shortcuts fail without parent structure",
            "next_action": "try psi-to-(Phi,q) quotient map or parent first-class generator if pursuing proof",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2269_2_fallback",
            "decision": "FINITE_STIFFNESS_INTAKE_OPENED_NOT_SCORED",
            "reason": "q_R=j_R/M_R^2 is the honest fallback, but M_R^2/j_R/no-gradient inputs are missing",
            "next_action": "source stiffness/source coefficients from parent action before comparator gates",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2269_3_next",
            "decision": "PSI_QUOTIENT_MAP_OR_STIFFNESS_SOURCE_NEXT",
            "reason": "2269 exhausts the direct radial-cell theorem using current evidence; the next root route is the psi-to-(Phi,q) map or finite coefficient sourcing",
            "next_action": "2270-Y5-R2FR-psi-to-Phiq-quotient-map-or-qR-stiffness-source.md",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "NEXT2269_0_primary",
            "next_target": "2270-Y5-R2FR-psi-to-Phiq-quotient-map-or-qR-stiffness-source.md",
            "script": "scripts/Y5_R2FR_psi_to_Phiq_quotient_map_or_qR_stiffness_source_2270.py",
            "objective": "try to construct an explicit psi covariance to (Phi,q) quotient map proving q is absent/vertical; if it fails, source finite stiffness inputs M_R^2 and j_R for q_R",
            "selection_status": "selected",
            "success_condition": "q is parent-absent/vertical in the psi metric map, or q_R=j_R/M_R^2 gains sourced nonclaim coefficient inputs",
        }
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": "BC2269_theorem",
            "source_path": rel(OUTPUTS["theorem_attempt"]),
            "target_path": rel(COPY_TARGETS["queue_theorem"]),
            "target_exists": COPY_TARGETS["queue_theorem"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["queue_theorem"]),
            "reason": "radial-cell theorem attempt copied as nonclaim queue",
        },
        {
            "copy_id": "BC2269_stiffness",
            "source_path": rel(OUTPUTS["stiffness_intake"]),
            "target_path": rel(COPY_TARGETS["queue_stiffness"]),
            "target_exists": COPY_TARGETS["queue_stiffness"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["queue_stiffness"]),
            "reason": "q_R stiffness coefficient intake copied as nonclaim queue",
        },
        {
            "copy_id": "BC2269_branch_wep",
            "source_path": rel(OUTPUTS["claim_gates"]),
            "target_path": rel(COPY_TARGETS["branch_wep"]),
            "target_exists": COPY_TARGETS["branch_wep"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["branch_wep"]),
            "reason": "branch-locked WEP/local refusal gates",
        },
        {
            "copy_id": "BC2269_beta_docs",
            "source_path": rel(OUTPUTS["decision"]),
            "target_path": rel(COPY_TARGETS["beta_docs"]),
            "target_exists": COPY_TARGETS["beta_docs"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["beta_docs"]),
            "reason": "portable radial-cell/stiffness decision ledger",
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
    theorem = read_csv(OUTPUTS["theorem_attempt"])
    routes = read_csv(OUTPUTS["route_audit"])
    stiffness = read_csv(OUTPUTS["stiffness_intake"])
    requirements = read_csv(OUTPUTS["claim_requirements"])
    refusal = read_csv(OUTPUTS["refusal"])
    claims = read_csv(OUTPUTS["claim_gates"])
    next_rows = read_csv(OUTPUTS["next_target"])
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks = [
        ("VAL2269_0_sources_exist", all(row["exists"].lower() == "true" for row in source_rows), "all cited source paths exist"),
        ("VAL2269_1_needles_present", all(row["needles_present"].lower() == "true" for row in source_rows), "all cited source needles are present"),
        (
            "VAL2269_2_prior_validation",
            any(row["source_key"] == "2268_validation" and row["validation_overall_pass"].lower() == "true" for row in source_rows),
            "2268 validation passes",
        ),
        (
            "VAL2269_3_theorem_not_claimed",
            any(row["attempt_id"] == "RCT2269_5_verdict" and row["proof_status"] == "RADIAL_CELL_THEOREM_NOT_DERIVED_CURRENT_CORPUS" for row in theorem)
            and all(row["valid_for_claim"].lower() == "false" for row in theorem),
            "radial-cell theorem is not falsely claimed",
        ),
        (
            "VAL2269_4_routes_audited",
            {row["route_id"] for row in routes}
            >= {"RRA2269_0_radial_cell_conservation", "RRA2269_1_generic_liouville", "RRA2269_2_cell_current", "RRA2269_3_gauge_noether", "RRA2269_4_finite_stiffness"},
            "radial-cell, Liouville, current, gauge, and stiffness routes audited",
        ),
        (
            "VAL2269_5_stiffness_nonclaim",
            {row["row_id"] for row in stiffness} >= {"SCI2269_0_MR2", "SCI2269_1_jR", "SCI2269_2_qR", "SCI2269_3_no_gradient"}
            and all(row["score_ready"].lower() == "false" and row["valid_for_claim"].lower() == "false" for row in stiffness),
            "q_R stiffness coefficient intake remains nonclaim",
        ),
        (
            "VAL2269_6_requirements_written",
            len(requirements) >= 5 and all(row["valid_for_claim"].lower() == "false" for row in requirements),
            "claim requirements written and blocked",
        ),
        (
            "VAL2269_7_refusal_blocks",
            all(row["score_eligible"].lower() == "false" and row["valid_for_claim"].lower() == "false" for row in refusal),
            "refusal runner blocks local claims",
        ),
        (
            "VAL2269_8_claim_gates_blocked",
            all(row["gate_pass"].lower() == "false" and row["valid_for_claim"].lower() == "false" for row in claims),
            "claim gates are all blocked",
        ),
        (
            "VAL2269_9_next_selected",
            any(row["route_id"] == "NEXT2269_0_primary" and row["selection_status"] == "selected" for row in next_rows),
            "2270 target selected",
        ),
        ("VAL2269_10_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 2269 CSVs parse"),
        (
            "VAL2269_11_no_claim_flags",
            not any(
                row.get(key, "").lower() == "true"
                for path in generated_csvs
                for row in read_csv(path)
                for key in ("score_ready", "accepted_ready", "valid_for_claim", "claim_allowed", "gate_pass")
            ),
            "no generated score/claim/gate flags are true",
        ),
        (
            "VAL2269_12_branch_copies",
            all(row["target_exists"].lower() == "true" and row["target_parses"].lower() == "true" for row in read_csv(OUTPUTS["branch_copies"])),
            "branch/queue copies exist and parse",
        ),
        ("VAL2269_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        (
            "VAL2269_14_formalization_no_2269",
            not any(
                path.is_file()
                and (path.name.startswith("2269-") or (path.name.startswith("P8_Y5") and "2269" in path.name))
                for path in FORMALIZATION.rglob("*")
            ),
            "formalization-workbench has no 2269 output files",
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
            "check_id": "VAL2269_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "2269 audits the radial-cell theorem, keeps J_q=1 nonclaim, opens q_R stiffness coefficient intake, and selects 2270",
        }
    )
    return rows


def write_doc() -> None:
    source_rows = read_csv(OUTPUTS["source_register"])
    theorem = read_csv(OUTPUTS["theorem_attempt"])
    routes = read_csv(OUTPUTS["route_audit"])
    stiffness = read_csv(OUTPUTS["stiffness_intake"])
    requirements = read_csv(OUTPUTS["claim_requirements"])
    refusal = read_csv(OUTPUTS["refusal"])
    claims = read_csv(OUTPUTS["claim_gates"])
    decisions = read_csv(OUTPUTS["decision"])
    next_rows = read_csv(OUTPUTS["next_target"])
    copies = read_csv(OUTPUTS["branch_copies"])
    validation = read_csv(OUTPUTS["validation"])
    sections = [
        "# 2269 - Y5/R2FR Radial-Cell Conservation Theorem Or q_R Stiffness Coefficient",
        "",
        "## Verdict",
        "",
        "2269 tries the direct theorem route for `J_q=1`. The algebra is exact: `J_q=T sqrt(S)=exp(q/2)`, so `J_q=1` is the same as `q=R_AB=0` and `AB=1`. Also exact: if a parent law gave `partial_r ln(J_q)=0` and flat boundary gave `J_q(infinity)=1`, then the reduced local branch would follow without a post-hoc multiplier.",
        "",
        "But the current corpus still does not supply that parent law. Generic Liouville phase-volume is too weak, cell-current conservation leaves `Q_R` hair unless a no-charge theorem is added, and gauge/Noether shortcuts remain rejected or contract-only. So `J_q=1` remains the sharp target, not a claim.",
        "",
        "The fallback is now explicit: an algebraic finite stiffness block gives `q_R=j_R/M_R^2`, but `M_R^2`, `j_R`, normalization, and the no-gradient guard are missing. No local-GR/Newton, PPN, R10, WEP, clock, orbital, `R_AB=0`, `Q_R=0`, or finite residual pass claim is made.",
        "",
        "## Source Register",
        table(["source_id", "source_key", "source_path", "exists", "needles_present", "validation_overall_pass", "role"], source_rows),
        "",
        "## Radial-Cell Theorem Attempt",
        table(["attempt_id", "target", "statement", "proof_status", "missing_for_claim", "valid_for_claim"], theorem),
        "",
        "## Radial-Cell Route Audit",
        table(["route_id", "route", "what_would_work", "current_blocker", "status", "source_paths", "valid_for_claim"], routes),
        "",
        "## q_R Stiffness Coefficient Intake",
        table(["row_id", "coefficient", "definition", "required_source", "units_or_normalization", "current_value", "status", "score_ready", "valid_for_claim"], stiffness),
        "",
        "## Claim Requirements",
        table(["requirement_id", "claim_path", "must_have", "current_status", "valid_for_claim"], requirements),
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
        "`J_q=1` is still the right target, but 2269 says it cannot be won by ordinary conservation language. The next clean attempt is deeper: inspect the primitive `psi -> g` map and see whether `q` is absent, vertical, or dynamically stiff. If that map cannot kill `q`, then the theory should stop calling the local branch derived and treat `q_R=j_R/M_R^2` as a finite residual to be sourced and tested.",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    for directory in (OUT, QUEUE, MICROSCOPE, BETA_DOCS):
        directory.mkdir(parents=True, exist_ok=True)

    write_csv(OUTPUTS["source_register"], source_register_rows())
    write_csv(OUTPUTS["theorem_attempt"], theorem_attempt_rows())
    write_csv(OUTPUTS["route_audit"], route_audit_rows())
    write_csv(OUTPUTS["stiffness_intake"], stiffness_intake_rows())
    write_csv(OUTPUTS["claim_requirements"], claim_requirement_rows())
    write_csv(OUTPUTS["refusal"], refusal_rows())
    write_csv(OUTPUTS["claim_gates"], claim_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next_target"], next_target_rows())

    shutil.copyfile(OUTPUTS["theorem_attempt"], COPY_TARGETS["queue_theorem"])
    shutil.copyfile(OUTPUTS["stiffness_intake"], COPY_TARGETS["queue_stiffness"])
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

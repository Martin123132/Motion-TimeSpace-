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

BRANCH_ID = "MTS_R2FR_RAB_PARENT_CONSTRAINT_ALGEBRA_OR_QR_SOURCE_2264"
DOC = ROOT / "2264-Y5-R2FR-RAB-parent-constraint-algebra-or-first-qR-value-source.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2264_00_2263_doc",
        "source_key": "2263_doc",
        "source_path": ROOT / "2263-Y5-R2FR-RAB-constrained-parent-action-lambda-origin-or-qR-envelope-runner.md",
        "needles": ["CPA2263_7_verdict", "CAG2263_6_verdict", "NEXT2263_0_primary"],
        "role": "handoff: constrained parent-action contract written but algebra not closed",
    },
    {
        "source_id": "SRC2264_01_2263_validation",
        "source_key": "2263_validation",
        "source_path": OUT / "P8_Y5_BRR545_2263_VALIDATION.csv",
        "needles": ["VAL2263_OVERALL", "PASS"],
        "role": "confirms 2263 passed before 2264 starts",
    },
    {
        "source_id": "SRC2264_02_2263_contract",
        "source_key": "2263_contract",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2263_CONSTRAINED_PARENT_ACTION_CONTRACT.csv",
        "needles": ["CPA2263_1_multiplier_origin", "CPA2263_7_verdict"],
        "role": "machine-readable constrained parent-action contract",
    },
    {
        "source_id": "SRC2264_03_2263_algebra",
        "source_key": "2263_algebra",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2263_CONSTRAINT_ALGEBRA_GATES.csv",
        "needles": ["CAG2263_0_primary_constraint", "CAG2263_6_verdict"],
        "role": "machine-readable constraint algebra gate list",
    },
    {
        "source_id": "SRC2264_04_2263_runner",
        "source_key": "2263_runner",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2263_QR_CANDIDATE_SCREENING_RUNNER.csv",
        "needles": ["RUN2263_2_MTS_unknown_qR", "not_scoreable_missing_parent_values"],
        "role": "q_R/Q_R runner refusing actual MTS unknown row",
    },
    {
        "source_id": "SRC2264_05_07_constraint",
        "source_key": "constraint_07",
        "source_path": ROOT / "07-nonpropagating-reciprocity-constraint.md",
        "needles": ["S_constraint = integral lambda_R R_AB", "no R_AB kinetic term", "parent origin is still open"],
        "role": "nonpropagating constraint candidate",
    },
    {
        "source_id": "SRC2264_06_10_observer",
        "source_key": "observer_10",
        "source_path": ROOT / "10-observer-map-symplectic-contract.md",
        "needles": ["R_AB = ln(T^2 S)", "J_q = 1", "contract not satisfied"],
        "role": "R_AB/J_q normalization and local-GR target",
    },
    {
        "source_id": "SRC2264_07_11_current",
        "source_key": "current_11",
        "source_path": ROOT / "11-cell-current-origin-attempt.md",
        "needles": ["W partial_r R_AB = Q_R", "Q_R = 0", "ordinary cell-current conservation does not close"],
        "role": "Q_R hair obstruction for kinetic/current route",
    },
    {
        "source_id": "SRC2264_08_12_noether",
        "source_key": "noether_12",
        "source_path": ROOT / "12-gauge-noether-origin-audit.md",
        "needles": ["Noether identity", "first-class parent constraint", "closure-only"],
        "role": "Noether/gauge warning",
    },
    {
        "source_id": "SRC2264_09_1038_omega",
        "source_key": "omega_1038",
        "source_path": ROOT / "1038-Y5-R10-parent-Omega-DCX-vertical-generator-closure-or-beta-bound-acquisition.md",
        "needles": ["MISSING_PARENT_OMEGA", "FIELD_MAP_INCOMPLETE", "MISSING_DEGREE_COUNT"],
        "role": "prior parent symplectic/degree-count obstruction",
    },
    {
        "source_id": "SRC2264_10_1040_boundary",
        "source_key": "boundary_1040",
        "source_path": ROOT / "1040-Y5-R10-parent-boundary-charge-formula-BX-or-alpha3-projection-bound.md",
        "needles": ["MISSING_THETA_X", "boundary cocycle", "Q_X differentiability"],
        "role": "prior boundary charge and symplectic potential obstruction",
    },
    {
        "source_id": "SRC2264_11_1041_theta",
        "source_key": "theta_1041",
        "source_path": ROOT / "1041-Y5-R10-parent-X-sector-ThetaX-PX-owner-or-boundary-coefficient-prior.md",
        "needles": ["first-class vertical constraint", "parent Omega", "ROUTE_OPEN_NOT_CLOSED"],
        "role": "prior Theta/Omega/constraint-owner audit",
    },
    {
        "source_id": "SRC2264_12_local_gates",
        "source_key": "gates_2263",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2263_LOCAL_SCREENING_GATES.csv",
        "needles": ["q_R", "Q_R", "screening_gate_not_fit_result"],
        "role": "local screening gates copied from 2263",
    },
    {
        "source_id": "SRC2264_13_translations",
        "source_key": "translations_2263",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2263_OBSERVABLE_TRANSLATIONS.csv",
        "needles": ["solar_shapiro", "mercury_perihelion_beta", "gps_gravitational_redshift"],
        "role": "observable translation coefficients copied from 2263",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2264_SOURCE_REGISTER.csv",
    "algebra_attempt": OUT / "P8_Y5_PARENT_QLOC_2264_CONSTRAINT_ALGEBRA_ATTEMPT.csv",
    "conditional_theorem": OUT / "P8_Y5_PARENT_QLOC_2264_CONDITIONAL_CONSTRAINT_THEOREM.csv",
    "failure_classification": OUT / "P8_Y5_PARENT_QLOC_2264_FAILURE_CLASSIFICATION.csv",
    "value_acquisition": OUT / "P8_Y5_PARENT_QLOC_2264_QR_VALUE_ACQUISITION_QUEUE.csv",
    "scoring_requirements": OUT / "P8_Y5_PARENT_QLOC_2264_QR_SCORING_REQUIREMENTS.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2264_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2264_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2264_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2264_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2264_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2264_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_value": QUEUE / "JR2264_QR_VALUE_ACQUISITION_QUEUE_NONCLAIM.csv",
    "queue_theorem": QUEUE / "JR2264_CONDITIONAL_CONSTRAINT_THEOREM_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "RAB_constraint_algebra_and_qR_value_refusal_2264.csv",
    "beta_docs": BETA_DOCS / "RAB_CONSTRAINT_ALGEBRA_OR_QR_SOURCE_2264_NONCLAIM.csv",
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
                "claim_allowed": False,
            }
        )
    return rows


def algebra_attempt_rows() -> list[dict[str, Any]]:
    rows = [
        ("ALG2264_0_phase_space", "parent phase space", "Y=(Q,Psi,theta,boundary; lambda_R,R_AB or J_q; conjugate momenta) with symplectic form Omega_Y", "MISSING_PARENT_PHASE_SPACE", "without Omega_Y and variables no Poisson brackets can be computed"),
        ("ALG2264_1_primary", "primary multiplier constraint", "if lambda_R has no velocity then pi_lambda approximately 0", "FORMAL_IF_ACTION_EXISTS", "requires the actual parent action and canonical one-form"),
        ("ALG2264_2_secondary", "secondary radial-cell constraint", "dot pi_lambda={pi_lambda,H_T}=-R_AB approximately 0", "FORMAL_IF_ACTION_EXISTS", "requires sign conventions and H_T from parent action"),
        ("ALG2264_3_preservation", "preserve R_AB", "dot R_AB={R_AB,H_0}+u_lambda{R_AB,pi_lambda}+... approximately 0", "NOT_COMPUTABLE", "H_0 and brackets are missing; cannot tell if this fixes a multiplier, creates a tertiary condition, or fails"),
        ("ALG2264_4_classification", "first/second-class classification", "rank of constraint bracket matrix C_ij={phi_i,phi_j}", "NOT_COMPUTABLE", "constraint matrix cannot be ranked without symplectic structure"),
        ("ALG2264_5_degree_count", "degree count", "R_AB/lambda_R removes no physical local mode and creates no hidden edge mode", "NOT_COMPUTABLE", "Dirac count and reduced Omega are missing"),
        ("ALG2264_6_boundary", "boundary differentiability", "delta H_T boundary terms vanish or are canceled by exact/proper charge with no Q_R hair", "MISSING_BOUNDARY_CHARGE_PROOF", "prior boundary audits still lack Theta/Omega and Q differentiation"),
        ("ALG2264_7_matter", "matter/source compatibility", "matter action cannot independently source R_AB after constraint elimination", "MISSING_MATTER_COMPATIBILITY", "same-coframe/readout order remains unsigned"),
        ("ALG2264_8_verdict", "parent constraint algebra", "ALG2264_0 through ALG2264_7 close jointly", "ALGEBRA_NOT_CLOSED_CURRENT_CORPUS", "move to value acquisition unless parent phase-space owner is supplied"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "algebra_id": algebra_id,
            "algebra_clause": clause,
            "required_statement": required,
            "current_status": status,
            "blocking_reason": blocker,
            "source_path": source_refs("2263_algebra", "omega_1038", "boundary_1040", "theta_1041"),
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for algebra_id, clause, required, status, blocker in rows
    ]


def conditional_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "THM2264_0_constraint_statement",
            "statement": "If the parent action contains a genuine nonpropagating lambda_R R_AB constraint, no D R_AB operator, differentiable boundary terms with no R_AB charge, and compatible matter/readout order, then R_AB=0 and Q_R=0 on the local branch.",
            "proof_status": "EXACT_CONDITIONAL",
            "proof_sketch": "delta_lambda S gives R_AB=0; no D R_AB term prevents W R_AB'=Q_R; boundary and matter clauses prevent edge/source reintroduction.",
            "missing_for_claim": "parent phase space, multiplier origin, constraint preservation, boundary proof, matter compatibility",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "THM2264_1_ppn_consequence",
            "statement": "If THM2264_0 is parent-signed and T^2=1-L is retained, then S=1/T^2, p=1, and the closure control lane has gamma=1.",
            "proof_status": "EXACT_CONDITIONAL",
            "proof_sketch": "R_AB=ln(T^2 S)=0 gives T^2 S=1; with T^2=1-L, S=(1-L)^-1.",
            "missing_for_claim": "same parent signature plus beta/conservation completion",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def failure_classification_rows() -> list[dict[str, Any]]:
    rows = [
        ("FAIL2264_0_not_coordinate", "not a coordinate failure", "areal gauge and Noether audit already reject coordinate AB=1", "do not revive coordinate-gauge route"),
        ("FAIL2264_1_not_numerical", "not a numerical/data failure", "local bounds can screen q_R but cannot supply parent q_R", "do not use Cassini/MICROSCOPE as MTS coefficients"),
        ("FAIL2264_2_structural", "structural missing object", "parent phase-space owner and constraint algebra are absent", "next derivation target is Theta/Omega/Hamiltonian owner"),
        ("FAIL2264_3_fallback", "finite residual fallback", "until algebra closes, q_R/Q_R rows remain live nonclaim acquisition rows", "source parent values or theorem-zero certificates"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "failure_id": failure_id,
            "failure_class": failure_class,
            "diagnosis": diagnosis,
            "instruction": instruction,
            "valid_for_claim": False,
        }
        for failure_id, failure_class, diagnosis, instruction in rows
    ]


def value_acquisition_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "ACQ2264_0_qR_parent_value",
            "target": "q_R",
            "definition": "R_AB=q_R L+O(L^2), L=2GM/(rc^2)",
            "needed_evidence": "parent-derived numeric q_R, theorem-zero q_R=0, or bounded q_R from an MTS parent coefficient calculation",
            "not_allowed_source": "Cassini/local-bound value used as theory value",
            "comparator_gate": "2.3e-5 from 2263 local screening gates",
            "units": "dimensionless",
            "arena_projection": "PPN;R10;clock;orbital",
            "current_status": "MISSING_PARENT_VALUE_OR_THEOREM_ZERO",
        },
        {
            "row_id": "ACQ2264_1_QR_zero_or_value",
            "target": "reciprocal_charge_Q_R",
            "definition": "boundary/current hair charge sourcing exterior R_AB",
            "needed_evidence": "parent boundary proof Q_R=0, or normalized Q_R value with map to q_R",
            "not_allowed_source": "assuming Q_R=0 from asymptotic flatness or current conservation alone",
            "comparator_gate": "0 by closure-definition theory gate",
            "units": "dimensionless_or_declared_boundary_normalization",
            "arena_projection": "PPN;R10;orbital",
            "current_status": "MISSING_BOUNDARY_ZERO_THEOREM_OR_NUMERIC_VALUE",
        },
        {
            "row_id": "ACQ2264_2_delta_beta_parent_value",
            "target": "delta_beta",
            "definition": "beta-1 nonlinear completion drift after R_AB branch choice",
            "needed_evidence": "weak-field second-order expansion of the parent local metric/readout",
            "not_allowed_source": "setting beta=1 because closure resembles Schwarzschild",
            "comparator_gate": "7.16e-5 from 2263 local screening gates",
            "units": "dimensionless",
            "arena_projection": "PPN;orbital",
            "current_status": "MISSING_SECOND_ORDER_PARENT_EXPANSION",
        },
        {
            "row_id": "ACQ2264_3_matter_clock_leak_values",
            "target": "alpha_clock;epsilon_matter",
            "definition": "clock/load redshift anomaly and matter-coupling spread under finite residual branch",
            "needed_evidence": "parent readout/matter functor expansion after R_AB decision",
            "not_allowed_source": "assuming universal coupling after introducing residual R_AB",
            "comparator_gate": "alpha_clock 2.48e-5; epsilon_matter 2.745906043549196e-15",
            "units": "dimensionless",
            "arena_projection": "clock;WEP;PPN",
            "current_status": "MISSING_READOUT_MATTER_EXPANSION",
        },
    ]
    return [
        {**{"branch_id": BRANCH_ID}, **row, "score_ready": False, "accepted_ready": False, "valid_for_claim": False, "claim_allowed": False}
        for row in rows
    ]


def scoring_requirement_rows() -> list[dict[str, Any]]:
    rows = [
        ("REQ2264_0_parent_source", "parent source path", "coefficient/theorem must come from an MTS parent derivation, not an external bound"),
        ("REQ2264_1_units", "units and normalization", "q_R and Q_R normalization must match R_AB=ln(T^2S) and L=2GM/(rc^2)"),
        ("REQ2264_2_projection", "arena projection", "PPN/R10/clock/orbital projection kernels must be declared"),
        ("REQ2264_3_no_cancellation", "no cancellation", "q_R, delta_beta, clock, matter, and Q_R gates are checked separately"),
        ("REQ2264_4_comparator", "external comparator", "published bounds are comparator gates only"),
        ("REQ2264_5_claim", "claim policy", "valid_for_claim remains false unless theorem-zero or all finite rows are sourced and pass gates"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "requirement_id": requirement_id,
            "requirement": requirement,
            "rule": rule,
            "valid_for_claim": False,
        }
        for requirement_id, requirement, rule in rows
    ]


def refusal_rows() -> list[dict[str, Any]]:
    rows = [
        ("REF2264_0_algebra", "parent constraint algebra closes", "BLOCKED", "ALG2264_8_verdict=ALGEBRA_NOT_CLOSED_CURRENT_CORPUS"),
        ("REF2264_1_theorem", "R_AB=0 and Q_R=0 theorem activates", "BLOCKED", "THM2264_0 is exact conditional only"),
        ("REF2264_2_qR_score", "actual q_R/Q_R finite row can be scored", "BLOCKED", "ACQ2264 rows lack parent values/theorem-zero certificates"),
        ("REF2264_3_bounds_as_values", "use local bounds as MTS q_R values", "REJECTED", "local bounds are comparator gates only"),
        ("REF2264_4_local_GR", "derived local GR/Newton/PPN safety", "BLOCKED", "no constraint algebra and no finite envelope pass"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "refusal_id": refusal_id,
            "attempted_claim": claim,
            "runner_result": result,
            "blocked_by": blocked_by,
            "score_eligible": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for refusal_id, claim, result, blocked_by in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2264_0_algebra", "parent constraint algebra", False, "parent phase space/Hamiltonian/Omega are missing"),
        ("CG2264_1_zero", "R_AB=0 and Q_R=0", False, "conditional theorem only"),
        ("CG2264_2_qR_value", "q_R/Q_R source-backed value", False, "all acquisition rows remain missing"),
        ("CG2264_3_screening", "finite residual screening pass", False, "no actual MTS values to screen"),
        ("CG2264_4_local_GR", "derived local GR/Newton/PPN", False, "not achieved"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": claim_id,
            "claim": claim,
            "gate_pass": gate_pass,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for claim_id, claim, gate_pass, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2264_0_algebra",
            "decision": "CONSTRAINT_ALGEBRA_NOT_CLOSED",
            "reason": "primary/secondary constraint form is formal, but preservation, classification, boundary differentiability, degree count, and matter compatibility cannot be computed without parent phase space and Hamiltonian",
            "next_action": "do not claim R_AB=0",
        },
        {
            "decision_id": "DEC2264_1_conditional",
            "decision": "CONDITIONAL_THEOREM_RETAINED",
            "reason": "if a real nonpropagating parent constraint is later supplied, the zero/no-hair theorem is exact",
            "next_action": "keep theorem as acceptance target",
        },
        {
            "decision_id": "DEC2264_2_acquisition",
            "decision": "FIRST_QR_VALUE_SOURCE_QUEUE_WRITTEN",
            "reason": "actual q_R/Q_R rows now specify required parent values, units, normalization, projections, and forbidden shortcuts",
            "next_action": "source a parent coefficient/theorem-zero before scoring",
        },
        {
            "decision_id": "DEC2264_3_next",
            "decision": "PARENT_PHASE_SPACE_OWNER_OR_QR_BOUND_ROW_NEXT",
            "reason": "the blocker is now the parent phase-space owner; if that cannot be supplied, the finite residual branch needs the first parent value row",
            "next_action": "2265-Y5-R2FR-RAB-parent-phase-space-owner-or-first-qR-bound-row.md",
        },
    ]
    return [{**{"branch_id": BRANCH_ID}, **row, "valid_for_claim": False, "claim_allowed": False} for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2264_0_primary",
            "next_target": "2265-Y5-R2FR-RAB-parent-phase-space-owner-or-first-qR-bound-row.md",
            "script": "scripts/Y5_R2FR_RAB_parent_phase_space_owner_or_first_qR_bound_row_2265.py",
            "objective": "try to identify the parent phase-space owner, symplectic potential, and Hamiltonian for the lambda_R/R_AB constraint; if it fails, fill the first parent-sourced q_R or Q_R bound/value row",
            "selection_status": "selected",
            "success_condition": "Omega/Hamiltonian owner makes ALG2264 computable, or one q_R/Q_R row gains a source-backed parent value/theorem-zero certificate while remaining nonclaim",
            "valid_for_claim": False,
        }
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "copy_id": "BC2264_value",
            "source_path": rel(OUTPUTS["value_acquisition"]),
            "target_path": rel(COPY_TARGETS["queue_value"]),
            "target_exists": COPY_TARGETS["queue_value"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["queue_value"]) if COPY_TARGETS["queue_value"].exists() else False,
            "reason": "q_R/Q_R parent value acquisition queue nonclaim copy",
        },
        {
            "branch_id": BRANCH_ID,
            "copy_id": "BC2264_theorem",
            "source_path": rel(OUTPUTS["conditional_theorem"]),
            "target_path": rel(COPY_TARGETS["queue_theorem"]),
            "target_exists": COPY_TARGETS["queue_theorem"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["queue_theorem"]) if COPY_TARGETS["queue_theorem"].exists() else False,
            "reason": "conditional zero/no-hair theorem nonclaim copy",
        },
        {
            "branch_id": BRANCH_ID,
            "copy_id": "BC2264_branch_wep",
            "source_path": rel(OUTPUTS["claim_gates"]),
            "target_path": rel(COPY_TARGETS["branch_wep"]),
            "target_exists": COPY_TARGETS["branch_wep"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["branch_wep"]) if COPY_TARGETS["branch_wep"].exists() else False,
            "reason": "branch-locked local/WEP refusal gates",
        },
        {
            "branch_id": BRANCH_ID,
            "copy_id": "BC2264_beta_docs",
            "source_path": rel(OUTPUTS["decision"]),
            "target_path": rel(COPY_TARGETS["beta_docs"]),
            "target_exists": COPY_TARGETS["beta_docs"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["beta_docs"]) if COPY_TARGETS["beta_docs"].exists() else False,
            "reason": "portable constraint algebra decision ledger",
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
    algebra_rows = read_csv(OUTPUTS["algebra_attempt"])
    theorem_rows = read_csv(OUTPUTS["conditional_theorem"])
    acquisition_rows = read_csv(OUTPUTS["value_acquisition"])
    requirement_rows = read_csv(OUTPUTS["scoring_requirements"])
    refusal = read_csv(OUTPUTS["refusal"])
    claims = read_csv(OUTPUTS["claim_gates"])
    next_rows = read_csv(OUTPUTS["next_target"])
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks = [
        ("VAL2264_0_sources_exist", all(row["exists"].lower() == "true" for row in source_rows), "all cited source paths exist"),
        ("VAL2264_1_needles_present", all(row["needles_present"].lower() == "true" for row in source_rows), "all cited source needles are present"),
        (
            "VAL2264_2_prior_validation",
            any(row["source_key"] == "2263_validation" and row["validation_overall_pass"].lower() == "true" for row in source_rows),
            "2263 validation passes",
        ),
        (
            "VAL2264_3_algebra_not_closed",
            any(row["algebra_id"] == "ALG2264_8_verdict" and row["current_status"] == "ALGEBRA_NOT_CLOSED_CURRENT_CORPUS" for row in algebra_rows),
            "constraint algebra is not falsely closed",
        ),
        (
            "VAL2264_4_conditional_theorem_retained",
            all(row["proof_status"] == "EXACT_CONDITIONAL" and row["valid_for_claim"].lower() == "false" for row in theorem_rows),
            "conditional theorem retained without claim",
        ),
        (
            "VAL2264_5_acquisition_rows",
            {row["row_id"] for row in acquisition_rows}
            >= {"ACQ2264_0_qR_parent_value", "ACQ2264_1_QR_zero_or_value", "ACQ2264_2_delta_beta_parent_value", "ACQ2264_3_matter_clock_leak_values"},
            "q_R/Q_R and companion acquisition rows written",
        ),
        (
            "VAL2264_6_acquisition_nonclaim",
            all(row["score_ready"].lower() == "false" and row["valid_for_claim"].lower() == "false" for row in acquisition_rows),
            "acquisition rows remain nonclaim and unscored",
        ),
        (
            "VAL2264_7_requirements_written",
            len(requirement_rows) >= 6 and any(row["requirement_id"] == "REQ2264_0_parent_source" for row in requirement_rows),
            "q_R scoring requirements written",
        ),
        (
            "VAL2264_8_refusal_blocks",
            all(row["claim_allowed"].lower() == "false" and row["score_eligible"].lower() == "false" for row in refusal),
            "refusal runner blocks claims",
        ),
        (
            "VAL2264_9_claim_gates_blocked",
            all(row["gate_pass"].lower() == "false" and row["valid_for_claim"].lower() == "false" for row in claims),
            "claim gates blocked",
        ),
        (
            "VAL2264_10_next_selected",
            any(row["route_id"] == "NEXT2264_0_primary" and row["selection_status"] == "selected" for row in next_rows),
            "2265 target selected",
        ),
        ("VAL2264_11_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 2264 CSVs parse"),
        (
            "VAL2264_12_no_claim_flags",
            not any(
                row.get(key, "").lower() == "true"
                for path in generated_csvs
                for row in read_csv(path)
                for key in ("score_ready", "accepted_ready", "valid_for_claim", "claim_allowed")
            ),
            "no generated score/claim flags are true",
        ),
        (
            "VAL2264_13_branch_copies",
            all(row["target_exists"].lower() == "true" and row["target_parses"].lower() == "true" for row in read_csv(OUTPUTS["branch_copies"])),
            "branch/queue copies exist and parse",
        ),
        ("VAL2264_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        (
            "VAL2264_15_formalization_no_2264",
            not any(
                path.is_file()
                and (path.name.startswith("2264-") or (path.name.startswith("P8_Y5") and "2264" in path.name))
                for path in FORMALIZATION.rglob("*")
            ),
            "formalization-workbench has no 2264 output files",
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
            "check_id": "VAL2264_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "2264 attempts the parent constraint algebra, keeps the zero theorem conditional, writes q_R/Q_R parent-value acquisition rows, and selects 2265",
        }
    )
    return rows


def write_doc() -> None:
    source_rows = read_csv(OUTPUTS["source_register"])
    algebra_rows = read_csv(OUTPUTS["algebra_attempt"])
    theorem_rows = read_csv(OUTPUTS["conditional_theorem"])
    failure_rows = read_csv(OUTPUTS["failure_classification"])
    acquisition_rows = read_csv(OUTPUTS["value_acquisition"])
    requirement_rows = read_csv(OUTPUTS["scoring_requirements"])
    refusal = read_csv(OUTPUTS["refusal"])
    claims = read_csv(OUTPUTS["claim_gates"])
    decisions = read_csv(OUTPUTS["decision"])
    next_rows = read_csv(OUTPUTS["next_target"])
    copies = read_csv(OUTPUTS["branch_copies"])
    validation = read_csv(OUTPUTS["validation"])
    sections = [
        "# 2264 - Y5/R2FR R_AB Parent Constraint Algebra Or First q_R Value Source",
        "",
        "## Verdict",
        "",
        "2264 tries to turn the `lambda_R R_AB` idea into an actual parent constraint algebra. The formal primary/secondary pattern is clear, but the algebra cannot be claimed because the parent phase space, symplectic form, Hamiltonian, boundary differentiability, degree count, and matter compatibility are not supplied.",
        "",
        "The zero/no-hair theorem is retained as an exact conditional. Since the algebra does not close, the finite branch now has explicit parent-value acquisition rows for `q_R`, `Q_R`, `delta_beta`, `alpha_clock`, and `epsilon_matter`. Published local bounds remain comparator gates only.",
        "",
        "No local-GR/Newton, PPN, R10, WEP, clock, orbital, `R_AB=0`, `Q_R=0`, or finite residual pass claim is made.",
        "",
        "## Source Register",
        table(["source_id", "source_key", "source_path", "exists", "needles_present", "validation_overall_pass", "role"], source_rows),
        "",
        "## Constraint Algebra Attempt",
        table(["algebra_id", "algebra_clause", "required_statement", "current_status", "blocking_reason", "valid_for_claim"], algebra_rows),
        "",
        "## Conditional Constraint Theorem",
        table(["theorem_id", "statement", "proof_status", "proof_sketch", "missing_for_claim", "valid_for_claim"], theorem_rows),
        "",
        "## Failure Classification",
        table(["failure_id", "failure_class", "diagnosis", "instruction", "valid_for_claim"], failure_rows),
        "",
        "## q_R/Q_R Value Acquisition Queue",
        table(["row_id", "target", "definition", "needed_evidence", "not_allowed_source", "comparator_gate", "units", "arena_projection", "current_status", "score_ready", "valid_for_claim"], acquisition_rows),
        "",
        "## q_R Scoring Requirements",
        table(["requirement_id", "requirement", "rule", "valid_for_claim"], requirement_rows),
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
        "This is a hard but clean result. The local-GR route is no longer floating around as a vibe: it needs a parent phase-space owner. Without that, the correct fallback is not to give up; it is to source `q_R/Q_R` as real finite residuals and let the local screening runner judge them.",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    for directory in (OUT, QUEUE, MICROSCOPE, BETA_DOCS):
        directory.mkdir(parents=True, exist_ok=True)

    write_csv(OUTPUTS["source_register"], source_register_rows())
    write_csv(OUTPUTS["algebra_attempt"], algebra_attempt_rows())
    write_csv(OUTPUTS["conditional_theorem"], conditional_theorem_rows())
    write_csv(OUTPUTS["failure_classification"], failure_classification_rows())
    write_csv(OUTPUTS["value_acquisition"], value_acquisition_rows())
    write_csv(OUTPUTS["scoring_requirements"], scoring_requirement_rows())
    write_csv(OUTPUTS["refusal"], refusal_rows())
    write_csv(OUTPUTS["claim_gates"], claim_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next_target"], next_target_rows())

    shutil.copyfile(OUTPUTS["value_acquisition"], COPY_TARGETS["queue_value"])
    shutil.copyfile(OUTPUTS["conditional_theorem"], COPY_TARGETS["queue_theorem"])
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

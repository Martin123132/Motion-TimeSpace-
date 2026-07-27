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

BRANCH_ID = "MTS_R2FR_RAB_PARENT_PHASE_SPACE_OWNER_OR_QR_BOUND_ROW_2265"
DOC = ROOT / "2265-Y5-R2FR-RAB-parent-phase-space-owner-or-first-qR-bound-row.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2265_00_2264_doc",
        "source_key": "2264_doc",
        "source_path": ROOT / "2264-Y5-R2FR-RAB-parent-constraint-algebra-or-first-qR-value-source.md",
        "needles": ["ALG2264_8_verdict", "THM2264_0_constraint_statement", "NEXT2264_0_primary"],
        "role": "handoff: constraint algebra not closed; phase-space owner selected next",
    },
    {
        "source_id": "SRC2265_01_2264_validation",
        "source_key": "2264_validation",
        "source_path": OUT / "P8_Y5_BRR545_2264_VALIDATION.csv",
        "needles": ["VAL2264_OVERALL", "PASS"],
        "role": "confirms 2264 passed before 2265 starts",
    },
    {
        "source_id": "SRC2265_02_2264_algebra",
        "source_key": "2264_algebra",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2264_CONSTRAINT_ALGEBRA_ATTEMPT.csv",
        "needles": ["ALG2264_0_phase_space", "ALG2264_8_verdict"],
        "role": "machine-readable phase-space/algebra obstruction",
    },
    {
        "source_id": "SRC2265_03_2264_acquisition",
        "source_key": "2264_acquisition",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2264_QR_VALUE_ACQUISITION_QUEUE.csv",
        "needles": ["ACQ2264_0_qR_parent_value", "ACQ2264_1_QR_zero_or_value"],
        "role": "parent q_R/Q_R value queue inherited from 2264",
    },
    {
        "source_id": "SRC2265_04_micro_action",
        "source_key": "micro_action",
        "source_path": PROJECT_ROOT / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md",
        "needles": ["A_MTS[ψ]", "g_{μν} = η_{μν}", "∂²_t ψ"],
        "role": "legacy microscopic psi action candidate",
    },
    {
        "source_id": "SRC2265_05_macro_action",
        "source_key": "macro_action",
        "source_path": PROJECT_ROOT / "core-mts-framework" / "action-principle" / "the-motion-timespace-action-principle.md",
        "needles": ["G_{μν} + Γ_G", "pure GR is recovered", "ψ : ℝ⁴ → ℝ"],
        "role": "legacy metric/EH plus Gamma_G action candidate",
    },
    {
        "source_id": "SRC2265_06_constraint_07",
        "source_key": "constraint_07",
        "source_path": ROOT / "07-nonpropagating-reciprocity-constraint.md",
        "needles": ["S_constraint = integral lambda_R R_AB", "no R_AB kinetic term", "parent origin is still open"],
        "role": "nonpropagating reciprocity constraint shape",
    },
    {
        "source_id": "SRC2265_07_observer_10",
        "source_key": "observer_10",
        "source_path": ROOT / "10-observer-map-symplectic-contract.md",
        "needles": ["R_AB = ln(T^2 S)", "J_q = 1", "contract not satisfied"],
        "role": "observer/radial-cell J_q target and missing symplectic contract",
    },
    {
        "source_id": "SRC2265_08_noether_12",
        "source_key": "noether_12",
        "source_path": ROOT / "12-gauge-noether-origin-audit.md",
        "needles": ["Noether identity", "first-class parent constraint", "closure-only"],
        "role": "gauge/Noether warning against smuggled AB=1",
    },
    {
        "source_id": "SRC2265_09_omega_1038",
        "source_key": "omega_1038",
        "source_path": ROOT / "1038-Y5-R10-parent-Omega-DCX-vertical-generator-closure-or-beta-bound-acquisition.md",
        "needles": ["MISSING_PARENT_OMEGA", "MISSING_DEGREE_COUNT", "no_pole_claim_rejected_current_corpus"],
        "role": "prior Omega/DCX/degree-count obstruction",
    },
    {
        "source_id": "SRC2265_10_boundary_1040",
        "source_key": "boundary_1040",
        "source_path": ROOT / "1040-Y5-R10-parent-boundary-charge-formula-BX-or-alpha3-projection-bound.md",
        "needles": ["MISSING_THETA_X", "Q_X differentiability", "boundary cocycle"],
        "role": "prior boundary charge formula missing parent Theta/P owner",
    },
    {
        "source_id": "SRC2265_11_theta_1041",
        "source_key": "theta_1041",
        "source_path": ROOT / "1041-Y5-R10-parent-X-sector-ThetaX-PX-owner-or-boundary-coefficient-prior.md",
        "needles": ["Theta_X/P_X owner", "ROUTE_OPEN_NOT_CLOSED", "parent Omega"],
        "role": "prior Theta/Omega owner menu, not parent-selected",
    },
    {
        "source_id": "SRC2265_12_local_gates",
        "source_key": "local_gates_2263",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2263_LOCAL_SCREENING_GATES.csv",
        "needles": ["q_R", "Q_R", "screening_gate_not_fit_result"],
        "role": "external/local comparator gates only",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2265_SOURCE_REGISTER.csv",
    "owner_audit": OUT / "P8_Y5_PARENT_QLOC_2265_PHASE_SPACE_OWNER_AUDIT.csv",
    "owner_contract": OUT / "P8_Y5_PARENT_QLOC_2265_MINIMUM_OWNER_CONTRACT.csv",
    "qr_rows": OUT / "P8_Y5_PARENT_QLOC_2265_FIRST_QR_BOUND_VALUE_ROWS.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2265_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2265_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2265_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2265_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2265_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2265_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_owner": QUEUE / "JR2265_RAB_PHASE_SPACE_OWNER_CONTRACT_NONCLAIM.csv",
    "queue_qr": QUEUE / "JR2265_FIRST_QR_BOUND_VALUE_ROWS_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "RAB_phase_space_owner_and_qR_refusal_2265.csv",
    "beta_docs": BETA_DOCS / "RAB_PHASE_SPACE_OWNER_OR_QR_BOUND_ROW_2265_NONCLAIM.csv",
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


def owner_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "POA2265_0_micro_psi_owner",
            "candidate_owner": "microscopic psi action",
            "owner_signal": "A_MTS[psi] gives a psi kinetic sector and a possible canonical pair (psi, pi_psi)",
            "phase_space_candidate": "Y_psi=(psi, pi_psi)",
            "blocking_reason": "no explicit map from (psi,pi_psi) or smoothing kernel to R_AB=ln(T^2S), J_q, lambda_R, or Q_R boundary silence",
            "current_status": "PSI_PHASE_SPACE_ONLY_NOT_RAB_OWNER",
            "needed_to_close": "derive R_AB=F[psi,pi_psi], lambda_R as a parent multiplier, and Theta_R/Omega_R from the psi parent action",
            "source_paths": source_refs("micro_action"),
            "valid_for_claim": False,
        },
        {
            "audit_id": "POA2265_1_metric_EH_owner",
            "candidate_owner": "macroscopic metric/EH plus Gamma_G action",
            "owner_signal": "A[g,psi] varies to G_munu + Gamma_G g_munu = kappa T_munu and has a GR limit",
            "phase_space_candidate": "ADM/covariant phase space of g_munu plus Gamma_G background/functional",
            "blocking_reason": "GR phase space cannot be used to import AB=1 as an MTS derivation; no lambda_R R_AB parent constraint is supplied",
            "current_status": "GR_LIMIT_ACTION_NOT_RAB_CONSTRAINT_OWNER",
            "needed_to_close": "show the metric action contains an independent nonpropagating R_AB multiplier or a first-class constraint removing R_AB before using the GR solution",
            "source_paths": source_refs("macro_action", "micro_action"),
            "valid_for_claim": False,
        },
        {
            "audit_id": "POA2265_2_observer_radial_cell_owner",
            "candidate_owner": "observer/radial-cell J_q scaffold",
            "owner_signal": "R_AB=ln(T^2S)=2ln(J_q), with local-GR target J_q=1",
            "phase_space_candidate": "radial cell variables (T,S,J_q) plus would-be conjugates",
            "blocking_reason": "generic phase-volume preservation is not enough and the symplectic contract is explicitly not satisfied",
            "current_status": "NORMALIZATION_TARGET_NOT_PHASE_SPACE_OWNER",
            "needed_to_close": "write the radial cell canonical one-form Theta_R and prove its constraint surface enforces J_q=1 without hidden edge modes",
            "source_paths": source_refs("observer_10"),
            "valid_for_claim": False,
        },
        {
            "audit_id": "POA2265_3_nonpropagating_constraint_owner",
            "candidate_owner": "lambda_R R_AB nonpropagating constraint",
            "owner_signal": "S_constraint=int lambda_R R_AB, no R_AB kinetic term, no Q_R hair if parent-signed",
            "phase_space_candidate": "(lambda_R,pi_lambda; R_AB,pi_R?) inside parent Y_R",
            "blocking_reason": "the constraint shape is ready but the parent origin, Hamiltonian, and boundary differentiability are open",
            "current_status": "CONTRACT_SHAPE_READY_PARENT_OWNER_MISSING",
            "needed_to_close": "supply H_T, pi_lambda≈0, R_AB≈0 preservation, constraint classification, degree count, and Q_R=0 boundary theorem",
            "source_paths": source_refs("constraint_07", "2264_algebra"),
            "valid_for_claim": False,
        },
        {
            "audit_id": "POA2265_4_noether_first_class_owner",
            "candidate_owner": "first-class Noether/vertical constraint",
            "owner_signal": "R_AB could be eliminated in a full constrained Hamiltonian parent theory",
            "phase_space_candidate": "momentum-map/constraint generator C_R on parent phase space",
            "blocking_reason": "a Noether identity relates equations but does not set R_AB=0 unless the parent constraint already exists",
            "current_status": "POSSIBLE_ROUTE_NOT_CONSTRUCTED",
            "needed_to_close": "construct C_R, show Omega_flat(v_R)=delta C_R, close brackets, and prove matter descent",
            "source_paths": source_refs("noether_12", "omega_1038", "theta_1041"),
            "valid_for_claim": False,
        },
        {
            "audit_id": "POA2265_5_prior_theta_omega_boundary_owner",
            "candidate_owner": "prior Theta/Omega/B_X/Q_X templates",
            "owner_signal": "Theta_X, Omega/DCX, B_X/Q_X formulas identify the right upstream objects",
            "phase_space_candidate": "generic finite-jet parent sector with Theta_X/P_X and boundary charge",
            "blocking_reason": "templates are not a selected parent R_AB sector; L_X/Theta_X/P_X, boundary class, and degree count remain missing",
            "current_status": "UPSTREAM_OBJECTS_NAMED_NOT_SIGNED",
            "needed_to_close": "specialize the X-template to R_AB, choose L_R or constraint C_R, and prove boundary/no-pole clauses",
            "source_paths": source_refs("omega_1038", "boundary_1040", "theta_1041"),
            "valid_for_claim": False,
        },
        {
            "audit_id": "POA2265_6_verdict",
            "candidate_owner": "claim-grade R_AB phase-space owner",
            "owner_signal": "all candidates audited jointly",
            "phase_space_candidate": "Theta_R/Omega_R/H_parent owner for lambda_R/R_AB",
            "blocking_reason": "no current source supplies the owner package without importing GR closure or inserting lambda_R by hand",
            "current_status": "PHASE_SPACE_OWNER_NOT_IDENTIFIED_CURRENT_CORPUS",
            "needed_to_close": "construct Theta_R/Omega_R from primitives or demote the local-GR transition route to closure-only while sourcing finite q_R",
            "source_paths": source_refs("2264_doc", "micro_action", "macro_action", "constraint_07", "observer_10", "noether_12", "theta_1041"),
            "valid_for_claim": False,
        },
    ]


def owner_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "MOC2265_0_parent_variables",
            "required_object": "parent field list and R_AB map",
            "acceptance_test": "declare Y_R and a covariant/local map R_AB[Y_R]=ln(T^2S)=2ln(J_q) before variation",
            "current_status": "MISSING_YR_AND_RAB_MAP",
            "why_it_matters": "without the map, R_AB can be a post-hoc diagnostic rather than a constrained parent variable",
            "valid_for_claim": False,
        },
        {
            "contract_id": "MOC2265_1_theta_R",
            "required_object": "symplectic potential Theta_R",
            "acceptance_test": "delta L_R = E_A delta Y_R^A + d Theta_R(delta Y_R) with finite-jet and boundary convention declared",
            "current_status": "MISSING_THETA_R",
            "why_it_matters": "Theta_R is the upstream object for Omega_R, boundary charges, and differentiability",
            "valid_for_claim": False,
        },
        {
            "contract_id": "MOC2265_2_omega_R",
            "required_object": "symplectic form Omega_R",
            "acceptance_test": "Omega_R=delta Theta_R is nondegenerate modulo declared gauge and contains the R_AB/lambda_R block",
            "current_status": "MISSING_OMEGA_R",
            "why_it_matters": "Poisson brackets and first/second-class tests cannot be computed without Omega_R",
            "valid_for_claim": False,
        },
        {
            "contract_id": "MOC2265_3_hamiltonian",
            "required_object": "parent Hamiltonian H_parent/H_T",
            "acceptance_test": "write H_T=H_0+u_lambda pi_lambda + lambda_R R_AB plus all allowed boundary terms, or the equivalent covariant constraint generator",
            "current_status": "MISSING_H_PARENT",
            "why_it_matters": "constraint preservation, tertiary conditions, and multipliers are Hamiltonian statements",
            "valid_for_claim": False,
        },
        {
            "contract_id": "MOC2265_4_constraint_pair",
            "required_object": "primary and secondary constraints",
            "acceptance_test": "derive pi_lambda≈0 and dot pi_lambda=-R_AB≈0 from the parent action, not as an imposed closure axiom",
            "current_status": "FORMAL_ONLY_PARENT_ACTION_MISSING",
            "why_it_matters": "this is the exact point where local GR would become derived rather than assumed",
            "valid_for_claim": False,
        },
        {
            "contract_id": "MOC2265_5_preservation_and_classification",
            "required_object": "constraint preservation and bracket rank",
            "acceptance_test": "compute dot R_AB, the constraint matrix rank, and whether a multiplier is fixed or a tertiary condition appears",
            "current_status": "NOT_COMPUTABLE_WITHOUT_OMEGA_H",
            "why_it_matters": "the local branch may otherwise hide a physical residual mode or inconsistency",
            "valid_for_claim": False,
        },
        {
            "contract_id": "MOC2265_6_degree_count",
            "required_object": "reduced phase-space degree count",
            "acceptance_test": "show the R_AB/lambda_R block removes no physical GR mode and creates no hidden edge mode",
            "current_status": "MISSING_DEGREE_COUNT",
            "why_it_matters": "derived GR requires the same propagating local content, not an extra fitted field",
            "valid_for_claim": False,
        },
        {
            "contract_id": "MOC2265_7_boundary_silence",
            "required_object": "differentiable boundary/no-hair theorem",
            "acceptance_test": "prove boundary terms are exact/proper/zero and Q_R=0 for the local branch under declared boundary class",
            "current_status": "MISSING_QR_ZERO_THEOREM",
            "why_it_matters": "otherwise the exterior solution carries Q_R hair and AB=1 is not forced",
            "valid_for_claim": False,
        },
        {
            "contract_id": "MOC2265_8_matter_readout",
            "required_object": "matter and clock/readout descent",
            "acceptance_test": "matter sees the quotient/constraint-reduced variables and cannot independently source R_AB at local order",
            "current_status": "MISSING_MATTER_READOUT_DESCENT",
            "why_it_matters": "WEP, clocks, and PPN all fail if matter reintroduces the removed direction",
            "valid_for_claim": False,
        },
        {
            "contract_id": "MOC2265_9_finite_residual_projection",
            "required_object": "q_R/Q_R finite branch projection",
            "acceptance_test": "if the zero theorem fails, compute parent q_R or Q_R with units and project to PPN/R10/clock/orbital gates",
            "current_status": "MISSING_PARENT_QR_VALUE",
            "why_it_matters": "finite residuals are testable only after MTS supplies the coefficient, not after borrowing bounds as values",
            "valid_for_claim": False,
        },
        {
            "contract_id": "MOC2265_10_verdict",
            "required_object": "minimum owner package",
            "acceptance_test": "MOC2265_0 through MOC2265_9 pass jointly",
            "current_status": "MINIMUM_OWNER_CONTRACT_UNSIGNED",
            "why_it_matters": "local GR/Newton cannot be claimed derived until this package closes",
            "valid_for_claim": False,
        },
    ]


def qr_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "QBV2265_0_qR_theorem_zero_candidate",
            "target": "q_R",
            "row_type": "theorem_zero_candidate",
            "definition": "R_AB=q_R L+O(L^2), L=2GM/(rc^2)",
            "parent_value": "MISSING_THEOREM_ZERO",
            "units": "dimensionless",
            "parent_source_path": rel(OUTPUTS["owner_contract"]),
            "extraction_method": "would follow only if MOC2265 owner contract closes",
            "comparator_gate": "2.3e-5 from local screening gates remains comparator only",
            "arena_projection": "PPN;R10;clock;orbital",
            "current_status": "MISSING_THETA_R_OMEGA_R_H_PARENT",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "QBV2265_1_reciprocal_charge_zero_candidate",
            "target": "reciprocal_charge_Q_R",
            "row_type": "boundary_zero_candidate",
            "definition": "boundary/current hair charge sourcing exterior R_AB",
            "parent_value": "MISSING_QR_ZERO_THEOREM",
            "units": "dimensionless_or_declared_boundary_normalization",
            "parent_source_path": rel(OUTPUTS["owner_contract"]),
            "extraction_method": "requires differentiable boundary generator and exact/proper/zero charge proof",
            "comparator_gate": "closure-definition Q_R=0 is a theory gate, not a measured value",
            "arena_projection": "PPN;R10;orbital",
            "current_status": "MISSING_BOUNDARY_SILENCE_AND_REFERENCE_CLASS",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "QBV2265_2_qR_finite_parent_value_candidate",
            "target": "q_R",
            "row_type": "finite_parent_value_candidate",
            "definition": "first nonzero local reciprocal residual coefficient after failed zero theorem",
            "parent_value": "MISSING_PARENT_NUMERIC_VALUE",
            "units": "dimensionless",
            "parent_source_path": rel(OUTPUTS["owner_contract"]),
            "extraction_method": "requires weak-field expansion of the parent R_AB sector and normalization to L",
            "comparator_gate": "compare to PPN/R10/clock/orbital bounds only after parent value exists",
            "arena_projection": "PPN;R10;clock;orbital",
            "current_status": "UNSCORED_PARENT_VALUE_ABSENT",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "QBV2265_3_external_bound_guard",
            "target": "external_local_bounds",
            "row_type": "comparator_guard",
            "definition": "published PPN/R10/WEP/clock/orbital bounds screen a parent coefficient but do not generate it",
            "parent_value": "NOT_A_PARENT_VALUE",
            "units": "mixed_by_arena",
            "parent_source_path": rel(source_path("local_gates_2263")),
            "extraction_method": "copied as comparator gate from prior local screening",
            "comparator_gate": "allowed for pass/fail after MTS supplies q_R/Q_R",
            "arena_projection": "PPN;R10;WEP;clock;orbital",
            "current_status": "GUARD_ONLY_VALID_FOR_CLAIM_FALSE",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "refusal_id": "REF2265_0_owner_claim",
            "attempted_claim": "R_AB phase-space owner identified",
            "runner_result": "BLOCKED",
            "blocked_by": "POA2265_6_verdict=PHASE_SPACE_OWNER_NOT_IDENTIFIED_CURRENT_CORPUS",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2265_1_local_gr_zero",
            "attempted_claim": "R_AB=0 and Q_R=0 derived local branch",
            "runner_result": "BLOCKED",
            "blocked_by": "MOC2265_10_verdict=MINIMUM_OWNER_CONTRACT_UNSIGNED",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2265_2_qR_score",
            "attempted_claim": "finite q_R/Q_R row can be scored",
            "runner_result": "BLOCKED",
            "blocked_by": "QBV2265 rows have no parent value/theorem-zero",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2265_3_bounds_as_values",
            "attempted_claim": "use local bounds as q_R/Q_R theory values",
            "runner_result": "REJECTED",
            "blocked_by": "external bounds are comparator gates only",
            "score_eligible": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF2265_4_github_public_claim",
            "attempted_claim": "public local-GR/Newton/R10/PPN pass",
            "runner_result": "BLOCKED",
            "blocked_by": "owner package and finite coefficient row both missing",
            "score_eligible": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "CG2265_0_phase_space_owner",
            "claim": "Theta_R/Omega_R/H_parent owner found",
            "gate_pass": False,
            "reason": "all current candidates are partial owners or contracts, not the R_AB parent owner",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2265_1_constraint_zero",
            "claim": "R_AB=0 and Q_R=0 are derived",
            "gate_pass": False,
            "reason": "zero theorem remains conditional on unsigned owner contract",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2265_2_finite_qR_value",
            "claim": "parent q_R/Q_R value is sourced",
            "gate_pass": False,
            "reason": "first q_R bound/value rows are source-ready placeholders only",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2265_3_local_screening",
            "claim": "local screening runner can score MTS finite residuals",
            "gate_pass": False,
            "reason": "no parent coefficient exists to compare against gates",
            "valid_for_claim": False,
        },
        {
            "claim_id": "CG2265_4_local_GR_Newton",
            "claim": "derived local GR/Newton limit",
            "gate_pass": False,
            "reason": "not achieved; route is sharpened but not closed",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2265_0_owner_audit",
            "decision": "PHASE_SPACE_OWNER_NOT_IDENTIFIED_CURRENT_CORPUS",
            "reason": "psi, EH/metric, observer-cell, nonpropagating, Noether, and prior Theta/Omega routes all lack the full R_AB owner package",
            "next_action": "do not claim derived local GR; construct Theta_R directly or demote route to closure-only",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2265_1_contract",
            "decision": "MINIMUM_OWNER_CONTRACT_WRITTEN",
            "reason": "the exact missing package is now a checklist: Y_R, Theta_R, Omega_R, H_parent, constraints, degree count, boundary, matter/readout, finite projection",
            "next_action": "attack the first missing object Theta_R/Omega_R rather than circling the same obstruction",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2265_2_qR_rows",
            "decision": "FIRST_QR_BOUND_VALUE_ROWS_REMAIN_NONCLAIM",
            "reason": "rows are source-ready but parent values/theorem-zero are absent; external local bounds are guards only",
            "next_action": "if Theta_R construction fails, source a parent prior width or numeric q_R from the primitive action",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2265_3_next",
            "decision": "THETAR_CONSTRUCTION_OR_QR_PRIOR_WIDTH_NEXT",
            "reason": "Theta_R is the upstream object needed by both the zero theorem and finite q_R branch",
            "next_action": "2266-Y5-R2FR-RAB-parent-ThetaR-construction-or-qR-prior-width-source.md",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "NEXT2265_0_primary",
            "next_target": "2266-Y5-R2FR-RAB-parent-ThetaR-construction-or-qR-prior-width-source.md",
            "script": "scripts/Y5_R2FR_RAB_parent_ThetaR_construction_or_qR_prior_width_source_2266.py",
            "objective": "try to construct the R_AB-sector symplectic potential Theta_R/Omega_R from MTS primitives; if that fails, source a nonclaim q_R prior width/value row from the parent action rather than external bounds",
            "selection_status": "selected",
            "success_condition": "either Theta_R/Omega_R makes the 2264 algebra computable, or one q_R/Q_R finite row gains a parent source/proven prior-width schema while remaining nonclaim",
        }
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": "BC2265_owner",
            "source_path": rel(OUTPUTS["owner_contract"]),
            "target_path": rel(COPY_TARGETS["queue_owner"]),
            "target_exists": COPY_TARGETS["queue_owner"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["queue_owner"]),
            "reason": "R_AB owner contract copied to acquisition queue",
        },
        {
            "copy_id": "BC2265_qr",
            "source_path": rel(OUTPUTS["qr_rows"]),
            "target_path": rel(COPY_TARGETS["queue_qr"]),
            "target_exists": COPY_TARGETS["queue_qr"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["queue_qr"]),
            "reason": "first q_R/Q_R bound-value rows copied as nonclaim queue",
        },
        {
            "copy_id": "BC2265_branch_wep",
            "source_path": rel(OUTPUTS["claim_gates"]),
            "target_path": rel(COPY_TARGETS["branch_wep"]),
            "target_exists": COPY_TARGETS["branch_wep"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["branch_wep"]),
            "reason": "branch-locked WEP/local refusal gates",
        },
        {
            "copy_id": "BC2265_beta_docs",
            "source_path": rel(OUTPUTS["decision"]),
            "target_path": rel(COPY_TARGETS["beta_docs"]),
            "target_exists": COPY_TARGETS["beta_docs"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["beta_docs"]),
            "reason": "portable phase-space-owner decision ledger",
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
    owners = read_csv(OUTPUTS["owner_audit"])
    contract = read_csv(OUTPUTS["owner_contract"])
    qr = read_csv(OUTPUTS["qr_rows"])
    refusal = read_csv(OUTPUTS["refusal"])
    claims = read_csv(OUTPUTS["claim_gates"])
    next_rows = read_csv(OUTPUTS["next_target"])
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks = [
        ("VAL2265_0_sources_exist", all(row["exists"].lower() == "true" for row in source_rows), "all cited source paths exist"),
        ("VAL2265_1_needles_present", all(row["needles_present"].lower() == "true" for row in source_rows), "all cited source needles are present"),
        (
            "VAL2265_2_prior_validation",
            any(row["source_key"] == "2264_validation" and row["validation_overall_pass"].lower() == "true" for row in source_rows),
            "2264 validation passes",
        ),
        (
            "VAL2265_3_owner_candidates_audited",
            {row["audit_id"] for row in owners}
            >= {
                "POA2265_0_micro_psi_owner",
                "POA2265_1_metric_EH_owner",
                "POA2265_2_observer_radial_cell_owner",
                "POA2265_3_nonpropagating_constraint_owner",
                "POA2265_4_noether_first_class_owner",
                "POA2265_5_prior_theta_omega_boundary_owner",
                "POA2265_6_verdict",
            },
            "psi/EH/observer/constraint/Noether/prior-owner candidates audited",
        ),
        (
            "VAL2265_4_owner_not_falsely_claimed",
            any(row["audit_id"] == "POA2265_6_verdict" and row["current_status"] == "PHASE_SPACE_OWNER_NOT_IDENTIFIED_CURRENT_CORPUS" for row in owners)
            and all(row["valid_for_claim"].lower() == "false" for row in owners),
            "phase-space owner is not falsely claimed",
        ),
        (
            "VAL2265_5_minimum_contract_unsigned",
            any(row["contract_id"] == "MOC2265_10_verdict" and row["current_status"] == "MINIMUM_OWNER_CONTRACT_UNSIGNED" for row in contract)
            and all(row["valid_for_claim"].lower() == "false" for row in contract),
            "minimum owner contract written and unsigned",
        ),
        (
            "VAL2265_6_qr_rows_nonclaim",
            {row["row_id"] for row in qr}
            >= {
                "QBV2265_0_qR_theorem_zero_candidate",
                "QBV2265_1_reciprocal_charge_zero_candidate",
                "QBV2265_2_qR_finite_parent_value_candidate",
                "QBV2265_3_external_bound_guard",
            }
            and all(row["score_ready"].lower() == "false" and row["valid_for_claim"].lower() == "false" for row in qr),
            "q_R/Q_R first bound-value rows remain nonclaim",
        ),
        (
            "VAL2265_7_refusal_blocks",
            all(row["score_eligible"].lower() == "false" and row["valid_for_claim"].lower() == "false" for row in refusal),
            "refusal runner blocks owner/zero/finite/local claims",
        ),
        (
            "VAL2265_8_claim_gates_blocked",
            all(row["gate_pass"].lower() == "false" and row["valid_for_claim"].lower() == "false" for row in claims),
            "claim gates are all blocked",
        ),
        (
            "VAL2265_9_next_selected",
            any(row["route_id"] == "NEXT2265_0_primary" and row["selection_status"] == "selected" for row in next_rows),
            "2266 target selected",
        ),
        ("VAL2265_10_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 2265 CSVs parse"),
        (
            "VAL2265_11_no_claim_flags",
            not any(
                row.get(key, "").lower() == "true"
                for path in generated_csvs
                for row in read_csv(path)
                for key in ("score_ready", "accepted_ready", "valid_for_claim", "claim_allowed", "gate_pass")
            ),
            "no generated score/claim/gate flags are true",
        ),
        (
            "VAL2265_12_branch_copies",
            all(row["target_exists"].lower() == "true" and row["target_parses"].lower() == "true" for row in read_csv(OUTPUTS["branch_copies"])),
            "branch/queue copies exist and parse",
        ),
        ("VAL2265_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        (
            "VAL2265_14_formalization_no_2265",
            not any(
                path.is_file()
                and (path.name.startswith("2265-") or (path.name.startswith("P8_Y5") and "2265" in path.name))
                for path in FORMALIZATION.rglob("*")
            ),
            "formalization-workbench has no 2265 output files",
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
            "check_id": "VAL2265_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "2265 audits parent phase-space owners, writes the minimum owner contract, keeps q_R/Q_R rows nonclaim, and selects 2266",
        }
    )
    return rows


def write_doc() -> None:
    source_rows = read_csv(OUTPUTS["source_register"])
    owners = read_csv(OUTPUTS["owner_audit"])
    contract = read_csv(OUTPUTS["owner_contract"])
    qr = read_csv(OUTPUTS["qr_rows"])
    refusal = read_csv(OUTPUTS["refusal"])
    claims = read_csv(OUTPUTS["claim_gates"])
    decisions = read_csv(OUTPUTS["decision"])
    next_rows = read_csv(OUTPUTS["next_target"])
    copies = read_csv(OUTPUTS["branch_copies"])
    validation = read_csv(OUTPUTS["validation"])
    sections = [
        "# 2265 - Y5/R2FR R_AB Parent Phase-Space Owner Or First q_R Bound Row",
        "",
        "## Verdict",
        "",
        "2265 takes the direct leap requested by 2264: look for the parent phase-space owner of the `lambda_R/R_AB` local-GR route. The result is useful but not claim-grade. The corpus contains candidate pieces — microscopic `psi`, macroscopic metric/EH, observer-cell `J_q`, nonpropagating `lambda_R R_AB`, Noether/first-class language, and prior `Theta/Omega` templates — but none supplies the full `Theta_R/Omega_R/H_parent` package.",
        "",
        "That means the local zero theorem remains exact only as a conditional: if the parent owner exists with no boundary/matter leakage, then `R_AB=0` and `Q_R=0`. It is not yet derived from the current corpus.",
        "",
        "The concrete improvement is that the missing object is now sharply localized: construct `Theta_R` first, or stop pretending the zero route is live and source a finite parent `q_R/Q_R` row. External local bounds remain comparator gates only.",
        "",
        "No local-GR/Newton, PPN, R10, WEP, clock, orbital, `R_AB=0`, `Q_R=0`, or finite residual pass claim is made.",
        "",
        "## Source Register",
        table(["source_id", "source_key", "source_path", "exists", "needles_present", "validation_overall_pass", "role"], source_rows),
        "",
        "## Phase-Space Owner Audit",
        table(["audit_id", "candidate_owner", "owner_signal", "phase_space_candidate", "blocking_reason", "current_status", "needed_to_close", "source_paths", "valid_for_claim"], owners),
        "",
        "## Minimum Owner Contract",
        table(["contract_id", "required_object", "acceptance_test", "current_status", "why_it_matters", "valid_for_claim"], contract),
        "",
        "## First q_R/Q_R Bound-Value Rows",
        table(["row_id", "target", "row_type", "definition", "parent_value", "units", "parent_source_path", "extraction_method", "comparator_gate", "arena_projection", "current_status", "score_ready", "valid_for_claim"], qr),
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
        "This is not circling for the sake of circling. It is a hard localization of the missing beam. The local-GR derivation lives or dies on `Theta_R/Omega_R/H_parent`. If we can construct that from MTS primitives, the `R_AB=0` theorem has a real parent. If we cannot, the intellectually clean move is to demote the zero route to closure-only and run the finite `q_R` branch as a testable residual with proper source provenance.",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    for directory in (OUT, QUEUE, MICROSCOPE, BETA_DOCS):
        directory.mkdir(parents=True, exist_ok=True)

    write_csv(OUTPUTS["source_register"], source_register_rows())
    write_csv(OUTPUTS["owner_audit"], owner_audit_rows())
    write_csv(OUTPUTS["owner_contract"], owner_contract_rows())
    write_csv(OUTPUTS["qr_rows"], qr_rows())
    write_csv(OUTPUTS["refusal"], refusal_rows())
    write_csv(OUTPUTS["claim_gates"], claim_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next_target"], next_target_rows())

    shutil.copyfile(OUTPUTS["owner_contract"], COPY_TARGETS["queue_owner"])
    shutil.copyfile(OUTPUTS["qr_rows"], COPY_TARGETS["queue_qr"])
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

from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1675"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1675-Y5-R2FR-constraint-first-Z-elimination-and-coframe-source-descent.md"

SOURCE_FILES = {
    "1674_doc": ROOT / "1674-Y5-R2FR-parent-q-Z-basis-minimal-ansatz-and-Dq-computation.md",
    "1674_validation": OUT / "P8_Y5_BRR545_1674_VALIDATION.csv",
    "1674_constraint": OUT / "P8_Y5_PARENT_QLOC_1674_CONSTRAINT_FIRST_ZERO_LEDGER.csv",
    "1674_dq_matrix": OUT / "P8_Y5_PARENT_QLOC_1674_DQZ_COMPONENT_DERIVATIVE_MATRIX.csv",
    "1666_theorem": OUT / "P8_Y5_PARENT_QLOC_1666_CONDITIONAL_THEOREM_ATTEMPT.csv",
    "1666_blockers": OUT / "P8_Y5_PARENT_QLOC_1666_BLOCKER_MATRIX.csv",
    "1620_chain_rule": OUT / "P8_Y5_PARENT_QLOC_1620_CHAIN_RULE_SOURCE_CURRENT_ZERO_ATTEMPT.csv",
    "1620_bridge": OUT / "P8_Y5_PARENT_QLOC_1620_PARENT_SIGNATURE_BRIDGE_CONTRACT.csv",
    "761_matter_contract": OUT / "P8_Y5_R10_761_PARENT_MATTER_VERTICAL_ACTION_CONTRACT.csv",
    "761_liev_audit": OUT / "P8_Y5_R10_761_LIEV_SMATTER_EVALUABILITY_AUDIT.csv",
    "1045_functor": OUT / "P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
    "1045_lift": OUT / "P8_Y5_R10_1045_VERTICAL_LIFT_DESCENT_GATE.csv",
    "1229_source_contract": OUT / "P8_Y5_R10_1229_LOCAL_GR_SOURCE_COUPLING_THEOREM_CONTRACT.csv",
    "1229_clause_audit": OUT / "P8_Y5_R10_1229_UNIVERSAL_SOURCE_COUPLING_CLAUSE_AUDIT.csv",
    "1023_descent": OUT / "P8_Y5_R10_1023_COUPLING_DESCENT_AUDIT.csv",
    "1023_demotion": OUT / "P8_Y5_R10_1023_DEMOTION_LEDGER.csv",
}

NEEDLES = {
    "1674_doc": ["constraint-first", "`Dq_Z_norm` remains `MISSING_NUMERIC_OR_THEOREM_ZERO`"],
    "1674_validation": ["VAL1674_OVERALL", "PASS"],
    "1674_constraint": ["CFZ1674_5_verdict", "CONSTRAINT_FIRST_ZERO_NOT_PROVED"],
    "1674_dq_matrix": ["DQM1674_1_source_current", "SOURCE_CURRENT_ZERO_NOT_DERIVED"],
    "1666_theorem": ["THM1666_5_verdict", "CONDITIONAL_THEOREM_ONLY_NO_CLAIM"],
    "1666_blockers": ["BLK1666_3_matter_descent", "MATTER_DESCENT_NOT_PARENT_SIGNED"],
    "1620_chain_rule": ["CR1620_1_zero_lemma", "EXACT_CONDITIONAL_SOURCE_CURRENT_ZERO_LEMMA"],
    "1620_bridge": ["BRC1620_6_verdict", "PARENT_SIGNATURE_BRIDGE_NOT_CLOSED"],
    "761_matter_contract": ["MVA761_5_evaluability_verdict", "parent_matter_vertical_action_not_signed"],
    "761_liev_audit": ["LEV761_3_current_corpus", "not_evaluable_as_parent_theorem"],
    "1045_functor": ["MFS1045_6_verdict", "FAIL_CURRENT_CLAIM_PARENT_MATTER_FUNCTOR_NOT_SIGNED"],
    "1045_lift": ["VLG1045_4_verdict", "FAIL_CURRENT_CLAIM_VERTICAL_LIFT_NOT_SIGNED"],
    "1229_source_contract": ["THM1229_2_countermodel", "OBSTRUCTION_ACTIVE"],
    "1229_clause_audit": ["CLC1229_8_verdict", "NOT_CLOSED"],
    "1023_descent": ["CDA1023_4_verdict", "coupling_not_theorem_zero"],
    "1023_demotion": ["DEM1023_3_claim_ceiling", "blocked"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1675_SOURCE_REGISTER.csv"
CONSTRAINT_DESCENT_THEOREM = OUT / "P8_Y5_PARENT_QLOC_1675_CONSTRAINT_FIRST_DESCENT_THEOREM_ATTEMPT.csv"
COFRAME_DESCENT_GATE = OUT / "P8_Y5_PARENT_QLOC_1675_COFRAME_DESCENT_GATE.csv"
SOURCE_READOUT_DESCENT_GATE = OUT / "P8_Y5_PARENT_QLOC_1675_SOURCE_READOUT_DESCENT_GATE.csv"
BOUNDARY_DESCENT_GATE = OUT / "P8_Y5_PARENT_QLOC_1675_BOUNDARY_PROJECTOR_DESCENT_GATE.csv"
SURVIVING_LEAK_VECTOR = OUT / "P8_Y5_PARENT_QLOC_1675_SURVIVING_DQZ_LEAK_VECTOR_NONCLAIM.csv"
DQZ_FACTOR_UPDATE = OUT / "P8_Y5_PARENT_QLOC_1675_DQZ_FACTOR_UPDATE_NONCLAIM.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1675_DECISION.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1675_CLAIM_GATE.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1675_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1675_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    CONSTRAINT_DESCENT_THEOREM,
    COFRAME_DESCENT_GATE,
    SOURCE_READOUT_DESCENT_GATE,
    BOUNDARY_DESCENT_GATE,
    SURVIVING_LEAK_VECTOR,
    DQZ_FACTOR_UPDATE,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    CONSTRAINT_DESCENT_THEOREM,
    COFRAME_DESCENT_GATE,
    SOURCE_READOUT_DESCENT_GATE,
    BOUNDARY_DESCENT_GATE,
    SURVIVING_LEAK_VECTOR,
    DQZ_FACTOR_UPDATE,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

COPY_TARGETS = {
    CONSTRAINT_DESCENT_THEOREM: [
        QUARANTINE / "CONSTRAINT_FIRST_DESCENT_THEOREM_ATTEMPT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_constraint_first_descent_theorem_attempt_nonclaim_1675.csv",
        QUEUE / "JR1675_CONSTRAINT_FIRST_DESCENT_THEOREM_ATTEMPT_NONCLAIM.csv",
    ],
    SURVIVING_LEAK_VECTOR: [
        QUARANTINE / "SURVIVING_DQZ_LEAK_VECTOR_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_surviving_DqZ_leak_vector_nonclaim_1675.csv",
        QUEUE / "JR1675_SURVIVING_DQZ_LEAK_VECTOR_NONCLAIM.csv",
    ],
    DQZ_FACTOR_UPDATE: [
        QUARANTINE / "DQZ_FACTOR_UPDATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_DqZ_factor_update_nonclaim_1675.csv",
        QUEUE / "JR1675_DQZ_FACTOR_UPDATE_NONCLAIM.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_nonclaim_1675.csv",
        QUEUE / "JR1675_NEXT_TARGET_NONCLAIM.csv",
    ],
}


def ensure_dirs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def bool_cell(value: str | bool) -> bool:
    if isinstance(value, bool):
        return value
    return value.strip().lower() == "true"


def missing_or_blocked(value: object) -> bool:
    value_text = str(value)
    blockers = ["MISSING_", "NOT_PARENT_SIGNED", "CONDITIONAL_ONLY", "NOT_CLOSED", "BLOCKED"]
    return any(blocker in value_text for blocker in blockers)


def source_register_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_key, source_path in SOURCE_FILES.items():
        exists = source_path.exists()
        body = read_text(source_path) if exists else ""
        needles_present = all(needle in body for needle in NEEDLES[source_key])
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_key": source_key,
                "source_path": str(source_path),
                "exists": exists,
                "needles_present": needles_present,
                "required_needles": "; ".join(NEEDLES[source_key]),
                "use_in_1675": "constraint-first Z elimination and coframe/source descent source input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def constraint_descent_theorem_rows() -> list[dict[str, object]]:
    common = {
        "branch_id": BRANCH_ID,
        "theorem_name": "constraint_first_DqZ_zero_descent_theorem",
        "formal_statement": "If C_Z(Phi)=0 eliminates Z before q, q(Phi)|C_Z=qbar(Q_vis), e_obs/source/readout/boundary descend through Q_vis, and q/Z norms are declared, then Dq_Z_norm=0 and Z is locally unobservable to first order.",
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    theorem_clauses = [
        (
            "CFD1675_0_parent_constraint",
            "C_Z(Phi)=0 or no-pole regularity is a parent Euler/constraint equation, not a post-hoc restriction.",
            "CFZ1674_0 and BLK1666_0/2 keep the parent origin missing.",
            "MISSING_PARENT_CONSTRAINT_ORIGIN",
            "construct the parent action term or regularity/no-pole condition that removes Z before q",
        ),
        (
            "CFD1675_1_tangent_space",
            "Allowed variations are tangent to C_Z=0 and do not contain hidden q/source/readout motion.",
            "CFZ1674_1 asks for tangent-space projection from parent equations.",
            "MISSING_TANGENT_SPACE_PROJECTION",
            "derive the projector onto the constraint surface and check Dq on projected tangents",
        ),
        (
            "CFD1675_2_q_factorization",
            "q(Phi)|C_Z=0=qbar(Q_vis) with no remaining Z argument.",
            "1674 only writes the ansatz; 1667 says q is not computable.",
            "MISSING_Q_FACTORISATION_PROOF",
            "show qbar components are exactly e_obs/g_obs/source/readout/theta/A_owned and exclude Z",
        ),
        (
            "CFD1675_3_coframe_functor",
            "e_obs=Obs_e(Q_vis), g_obs=e_obs^T eta e_obs, and connection/measure are functions of Q_vis only.",
            "MFS1045_1 is sufficient but not parent-signed.",
            "SUFFICIENT_SIGNATURE_NOT_PARENT_SIGNED",
            "derive observed coframe functor from the parent MTS field bundle",
        ),
        (
            "CFD1675_4_source_readout",
            "S_matter, source current, clocks, photons, EM, PPN, and orbital readouts descend through Q_vis.",
            "761/1045/1229 keep matter/source/readout descent unsigned and source weights live.",
            "MISSING_MATTER_SOURCE_READOUT_DESCENT",
            "derive quotient-invariant matter/readout action with no source-only species weights",
        ),
        (
            "CFD1675_5_boundary_projector",
            "Boundary/projector/source-measure terms vanish, are exact/proper, or are retained as finite factors before claiming Dq_Z=0.",
            "1023/1229/1666 keep boundary and local projection open.",
            "MISSING_BOUNDARY_PROJECTOR_NO_FLUX",
            "prove compact-local no-flux or retain boundary/source-measure leak rows",
        ),
        (
            "CFD1675_6_verdict",
            "Dq_Z_norm=0 by constraint-first descent.",
            "one or more required clauses above remains unsigned.",
            "DESCENT_THEOREM_NOT_CLOSED",
            "do not promote local GR/Newton; carry surviving leak vector forward",
        ),
    ]
    return [
        {
            **common,
            "clause_id": clause_id,
            "required_clause": required_clause,
            "current_evidence": current_evidence,
            "status": status,
            "next_action": next_action,
            "clause_met": False,
            "parent_signed": False,
            "theorem_zero_adopted": False,
            "accepted_for_scoring": False,
            "score_ready": False,
        }
        for clause_id, required_clause, current_evidence, status, next_action in theorem_clauses
    ]


def coframe_descent_rows() -> list[dict[str, object]]:
    gates = [
        (
            "CDG1675_0_obs_functor",
            "e_obs=Obs_e(Q_vis) with no Z or R_phys argument",
            "MFS1045_1 gives sufficient signature, not signed.",
            "CONDITIONAL_SUPPORT_NOT_PARENT_SIGNED",
            "would make Dq_Z[e_obs]=0",
        ),
        (
            "CDG1675_1_metric_connection",
            "g_obs and omega_obs are determined by e_obs or owned gauge fields only",
            "1045 warns hidden connection/frame re-entry remains legal.",
            "MISSING_CONNECTION_DESCENT",
            "would make Dq_Z[g_obs,omega_obs]=0",
        ),
        (
            "CDG1675_2_measure",
            "mu_m is species-blind and depends only on Q_vis",
            "1229 CLC1229_4 marks measure/coframe descent unsigned.",
            "UNSIGNED_MEASURE_COFRAME_DESCENT",
            "would block source-weight mimicry through Jacobians",
        ),
        (
            "CDG1675_3_verdict",
            "coframe/metric/measure contribution to Dq_Z is zero",
            "all coframe/measure clauses are conditional only.",
            "COFRAME_DESCENT_NOT_PARENT_SIGNED",
            "retain coframe leak component unless parent functor is derived",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "gate": gate,
            "current_evidence": evidence,
            "status": status,
            "effect_if_signed": effect,
            "gate_pass": False,
            "theorem_zero_adopted": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate, evidence, status, effect in gates
    ]


def source_readout_descent_rows() -> list[dict[str, object]]:
    gates = [
        (
            "SRD1675_0_matter_domain",
            "ordinary matter fields are sections over e_obs(Q_vis)",
            "MVA761_0 is admissible but not parent-constructed.",
            "MATTER_CATEGORY_NOT_PARENT_CONSTRUCTED",
            "without this, fixed/gauge lift is a convention",
        ),
        (
            "SRD1675_1_vertical_lift",
            "delta_Z Psi_A is fixed or an owned gauge/local-Lorentz/diffeomorphism lift for every species",
            "MVA761_1/2 and VLG1045_4 keep lift unsigned.",
            "VERTICAL_LIFT_NOT_PARENT_SIGNED",
            "without this, matter can carry physical Z charge",
        ),
        (
            "SRD1675_2_constants_markers",
            "Lie_Z theta_A=0 and no material marker/source-only scalar enters ordinary matter",
            "CDA1023_1 and MFS1045_5 keep constants/markers unsigned.",
            "CONSTANT_MARKER_SILENCE_NOT_DERIVED",
            "without this, WEP/clock/EM residual rows survive",
        ),
        (
            "SRD1675_3_source_weights",
            "one universal parent action/source scale or null projection for all source weights",
            "THM1229_2 gives active countermodel if source multipliers survive.",
            "SOURCE_WEIGHT_OBSTRUCTION_ACTIVE",
            "without this, Newton/GR source side is not derived",
        ),
        (
            "SRD1675_4_readouts",
            "clock/photon/EM/orbit/PPN readouts are functions of Q_vis and owned gauge data only",
            "1045/1674 keep readout descent missing.",
            "MISSING_READOUT_DESCENT",
            "without this, tests can see Z even if coframe is silent",
        ),
        (
            "SRD1675_5_verdict",
            "source/readout contribution to Dq_Z is zero",
            "source weights, constants, matter lift, and readouts are not parent-signed together.",
            "SOURCE_READOUT_DESCENT_NOT_CLOSED",
            "retain source/readout leak components",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "gate": gate,
            "current_evidence": evidence,
            "status": status,
            "risk_if_unsigned": risk,
            "gate_pass": False,
            "theorem_zero_adopted": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate, evidence, status, risk in gates
    ]


def boundary_descent_rows() -> list[dict[str, object]]:
    gates = [
        (
            "BDG1675_0_compact_support",
            "Z variation has compact support inside the local collar or exact/proper boundary primitive",
            "1666 and 1045 leave boundary action open.",
            "MISSING_COMPACT_SUPPORT_OR_EXACT_PRIMITIVE",
        ),
        (
            "BDG1675_1_projector",
            "P_loc, Q_X, and source-measure projection do not carry Z or are separately bounded",
            "1023 CDA1023_3 says projector/boundary coupling is open.",
            "BOUNDARY_PROJECTOR_OPEN",
        ),
        (
            "BDG1675_2_worldtube",
            "source worldtube and measured Hamiltonian mass have no Z-dependent edge term",
            "1229 CLC1229_5 keeps boundary local projection unsigned.",
            "UNSIGNED_BOUNDARY_LOCAL_PROJECTION",
        ),
        (
            "BDG1675_3_verdict",
            "boundary/projector contribution to Dq_Z is zero",
            "no-flux/proper-boundary theorem is not present.",
            "BOUNDARY_DESCENT_NOT_CLOSED",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "gate": gate,
            "current_evidence": evidence,
            "status": status,
            "gate_pass": False,
            "theorem_zero_adopted": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate, evidence, status in gates
    ]


def surviving_leak_vector_rows() -> list[dict[str, object]]:
    leaks = [
        (
            "LEAK1675_0_coframe",
            "Dq_Z[e_obs,g_obs,mu_m,D_m]",
            "MISSING_OBSERVED_COFRAME_FUNCTOR",
            "Pi_coframe*C_Obs_e*Dq_Z_norm*N_Z",
            "R0_WEP;R3_gamma;R4_beta;R11_operator",
        ),
        (
            "LEAK1675_1_source_weight",
            "Dq_Z[source normalization/J_H]",
            "SOURCE_WEIGHT_OBSTRUCTION_ACTIVE",
            "Pi_source*Delta_w_Z + Pi_Gauss*Dq_Z_norm",
            "Newton_limit;WEP;orbits;R10",
        ),
        (
            "LEAK1675_2_constants_markers",
            "Dq_Z[theta_A, material markers, clock/EM standards]",
            "CONSTANT_MARKER_SILENCE_NOT_DERIVED",
            "Pi_theta*Lie_Z(theta_A)+Pi_marker*qbar_marker_Z",
            "clocks;fine_structure;WEP;EM",
        ),
        (
            "LEAK1675_3_readout",
            "Dq_Z[clock/photon/orbit/EM/PPN readouts]",
            "MISSING_READOUT_DESCENT",
            "Pi_readout*Dq_Z[O_i]",
            "PPN;orbital;clock;EM",
        ),
        (
            "LEAK1675_4_boundary",
            "Dq_Z[B_edge,P_loc,Q_X]",
            "BOUNDARY_PROJECTOR_OPEN",
            "Pi_boundary*B_Z + Pi_QX*Dq_Z[Q_X]",
            "R10;WEP;compact_orbit;source_measure",
        ),
        (
            "LEAK1675_5_residual_lock",
            "Dq_Z[R_phys -> observed residuals]",
            "COMPONENT_MAP_NOT_CLOSED",
            "L^I_A Z^A with unproved rank/coercivity",
            "q_loc;PPN;R10;R11",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "leak_id": leak_id,
            "leak_component": component,
            "status": status,
            "symbolic_bound_form": bound_form,
            "priority_arenas": arenas,
            "candidate_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "upper_bound": "MISSING_SOURCE_BACKED_UPPER_BOUND",
            "source_paths": "1675 descent gates; 1674 Dq matrix; 1620 chain rule; 761/1045/1229/1023 audits",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for leak_id, component, status, bound_form, arenas in leaks
    ]


def dqz_factor_update_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQZ1675_0_factor_status",
            "symbol": "Dq_Z_norm",
            "previous_status": "STRUCTURE_CLARIFIED_VALUE_STILL_MISSING",
            "new_status": "DESCENT_ROUTE_FAILED_SURVIVING_LEAK_VECTOR_EMITTED",
            "candidate_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "upper_bound": "MISSING_SOURCE_BACKED_UPPER_BOUND",
            "conditional_zero_status": "NOT_ADOPTED",
            "reason": "constraint-first elimination and Q_vis descent are coherent but not parent-signed",
            "projection_formula": "C_qm_Z <= C_Obs_e * Dq_Z_norm * N_Z plus explicit source/readout/boundary leak terms",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def decision_rows() -> list[dict[str, object]]:
    decisions = [
        (
            "D1675_0_theorem",
            "CONSTRAINT_FIRST_DESCENT_THEOREM_CONDITIONAL_ONLY",
            "the theorem is mathematically coherent but all source-facing clauses are not parent-signed together",
            "do not call Dq_Z_norm zero",
        ),
        (
            "D1675_1_coupling",
            "COUPLING_SOURCE_DESCENT_IS_ACTIVE_BOTTLENECK",
            "source weights, markers, readouts, and boundary terms remain live after coframe logic",
            "attack parent object-language/action-scale/no-marker theorem next",
        ),
        (
            "D1675_2_leaks",
            "SURVIVING_LEAK_VECTOR_RETAINED",
            "every unclosed descent clause now has a named nonclaim leak row",
            "fill finite source-backed coefficients if derivation fails",
        ),
        (
            "D1675_3_safety",
            "NO_GR_NEWTON_CLAIM",
            "Dq_Z_norm zero is not adopted and source/readout descent is not closed",
            "keep local-GR/Newton/PPN/R10/WEP/clock/orbital gates false",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for decision_id, decision, reason, next_action in decisions
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    gates = [
        ("CG1675_0_constraint_origin", "C_Z parent constraint/no-pole origin is signed", False, "BLOCKED", "parent origin missing"),
        ("CG1675_1_coframe", "observed coframe/metric/measure descend through Q_vis", False, "BLOCKED", "coframe functor sufficient but not signed"),
        ("CG1675_2_source", "source current/action scale/source weights descend universally", False, "BLOCKED", "source-weight countermodel active"),
        ("CG1675_3_readout", "clock/photon/EM/orbit/PPN readouts descend through Q_vis", False, "BLOCKED", "readout descent missing"),
        ("CG1675_4_boundary", "boundary/projector/source-measure terms vanish or are bounded", False, "BLOCKED", "boundary/projector open"),
        ("CG1675_5_DqZ", "Dq_Z_norm=0 or finite source-backed value exists", False, "BLOCKED", "no zero theorem/value"),
        ("CG1675_6_local_GR", "local GR/Newton reduction follows", False, "BLOCKED", "coupling/source descent not closed"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "gate": gate,
            "gate_pass": gate_pass,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate, gate_pass, status, reason in gates
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1676-Y5-R2FR-parent-source-object-language-and-no-marker-theorem.md",
            "script": "scripts/Y5_R2FR_parent_source_object_language_and_no_marker_theorem.py",
            "objective": "try to derive the parent object-language theorem that forbids source-only weights, material markers, hidden frames, and readout-only constants in ordinary matter",
            "success_condition": "source/readout descent clauses close as parent-signed, or the surviving source/marker/readout leak coefficients are emitted as finite nonclaim acquisition rows",
            "why_next": "1675 shows coframe logic alone is not enough; source/coupling ownership is the bottleneck",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def copy_outputs() -> None:
    for source_path, target_paths in COPY_TARGETS.items():
        for target_path in target_paths:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_path, target_path)


def validate() -> list[dict[str, object]]:
    source_rows = read_csv(SOURCE_REGISTER)
    theorem_rows = read_csv(CONSTRAINT_DESCENT_THEOREM)
    coframe_rows = read_csv(COFRAME_DESCENT_GATE)
    source_readout_rows = read_csv(SOURCE_READOUT_DESCENT_GATE)
    boundary_rows = read_csv(BOUNDARY_DESCENT_GATE)
    leak_rows = read_csv(SURVIVING_LEAK_VECTOR)
    factor_rows = read_csv(DQZ_FACTOR_UPDATE)
    decision_rows_ = read_csv(DECISION)
    claim_rows = read_csv(CLAIM_GATE)
    next_rows = read_csv(NEXT_TARGET)

    sources_ok = all(bool_cell(row["exists"]) and bool_cell(row["needles_present"]) for row in source_rows)
    theorem_verdict = any(row["clause_id"] == "CFD1675_6_verdict" and row["status"] == "DESCENT_THEOREM_NOT_CLOSED" for row in theorem_rows)
    theorem_not_adopted = all(not bool_cell(row["theorem_zero_adopted"]) and not bool_cell(row["parent_signed"]) for row in theorem_rows)
    coframe_blocked = any(row["gate_id"] == "CDG1675_3_verdict" and row["status"] == "COFRAME_DESCENT_NOT_PARENT_SIGNED" for row in coframe_rows)
    source_blocked = any(row["gate_id"] == "SRD1675_5_verdict" and row["status"] == "SOURCE_READOUT_DESCENT_NOT_CLOSED" for row in source_readout_rows)
    boundary_blocked = any(row["gate_id"] == "BDG1675_3_verdict" and row["status"] == "BOUNDARY_DESCENT_NOT_CLOSED" for row in boundary_rows)
    leak_vector_complete = {
        "Dq_Z[e_obs,g_obs,mu_m,D_m]",
        "Dq_Z[source normalization/J_H]",
        "Dq_Z[theta_A, material markers, clock/EM standards]",
        "Dq_Z[clock/photon/orbit/EM/PPN readouts]",
        "Dq_Z[B_edge,P_loc,Q_X]",
        "Dq_Z[R_phys -> observed residuals]",
    } == {row["leak_component"] for row in leak_rows}
    factor_not_filled = (
        factor_rows[0]["candidate_value"] == "MISSING_NUMERIC_OR_THEOREM_ZERO"
        and factor_rows[0]["conditional_zero_status"] == "NOT_ADOPTED"
        and factor_rows[0]["new_status"] == "DESCENT_ROUTE_FAILED_SURVIVING_LEAK_VECTOR_EMITTED"
    )
    decision_next = any(row["decision"] == "COUPLING_SOURCE_DESCENT_IS_ACTIVE_BOTTLENECK" for row in decision_rows_)
    claim_gate_safe = all(not bool_cell(row["gate_pass"]) and not bool_cell(row["claim_allowed"]) for row in claim_rows)
    next_target_selected = next_rows[0]["next_target"] == "1676-Y5-R2FR-parent-source-object-language-and-no-marker-theorem.md"
    csv_parse = all(path.exists() and len(read_csv(path)) >= 1 for path in GENERATED)
    branch_copies = all(target_path.exists() for target_paths in COPY_TARGETS.values() for target_path in target_paths)
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_clean = not any(FORMALIZATION.rglob("*1675*")) if FORMALIZATION.exists() else True

    no_claim_flags = True
    missing_not_ready = True
    for generated_path in CLAIM_CHECKED:
        for generated_row in read_csv(generated_path):
            if generated_row.get("valid_for_claim", "False").lower() == "true" or generated_row.get("claim_allowed", "False").lower() == "true":
                no_claim_flags = False
            if any(missing_or_blocked(value) for value in generated_row.values()):
                for claim_key in ["valid_for_claim", "claim_allowed", "score_ready", "accepted_for_scoring", "prediction_source_backed", "valid_prediction_row"]:
                    if claim_key in generated_row and bool_cell(generated_row[claim_key]):
                        missing_not_ready = False

    checks = [
        ("VAL1675_0_sources_exist", sources_ok, "all cited 1675 source paths exist and needles are present"),
        ("VAL1675_1_theorem_verdict", theorem_verdict, "constraint-first descent theorem remains not closed"),
        ("VAL1675_2_theorem_not_adopted", theorem_not_adopted, "no theorem-zero clause is parent-signed/adopted"),
        ("VAL1675_3_coframe_blocked", coframe_blocked, "coframe descent remains unsigned"),
        ("VAL1675_4_source_blocked", source_blocked, "source/readout descent remains unsigned"),
        ("VAL1675_5_boundary_blocked", boundary_blocked, "boundary/projector descent remains unsigned"),
        ("VAL1675_6_leak_vector_complete", leak_vector_complete, "surviving Dq_Z leak vector covers coframe/source/constants/readout/boundary/residual lock"),
        ("VAL1675_7_factor_not_filled", factor_not_filled, "Dq_Z_norm zero/value remains unfilled"),
        ("VAL1675_8_decision_next", decision_next, "decision selects source/coupling object-language bottleneck"),
        ("VAL1675_9_claim_gate_safe", claim_gate_safe, "all claim gates keep local claims false"),
        ("VAL1675_10_no_claim_flags", no_claim_flags, "all generated rows keep claim flags false"),
        ("VAL1675_11_missing_not_ready", missing_not_ready, "no blocked/missing row is marked claim/scoring/source ready"),
        ("VAL1675_12_next_target_selected", next_target_selected, "next target selects parent source object-language/no-marker theorem"),
        ("VAL1675_13_csv_parse", csv_parse, "all generated 1675 CSVs parse"),
        ("VAL1675_14_branch_copies", branch_copies, "branch/quarantine/queue copies exist"),
        ("VAL1675_15_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL1675_16_formalization_untouched", formalization_clean, "no 1675 outputs found under formalization-workbench"),
    ]
    overall = all(result for _, result, _ in checks)
    validation_rows = [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, result, detail in checks
    ]
    validation_rows.append(
        {
            "check_id": "VAL1675_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1675 constraint-first Z elimination and coframe/source descent validation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return validation_rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    table_rows = []
    for row in rows:
        table_rows.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, separator, *table_rows])


def write_doc(
    source_rows: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    coframe_rows: list[dict[str, object]],
    source_readout_rows: list[dict[str, object]],
    boundary_rows: list[dict[str, object]],
    leak_rows: list[dict[str, object]],
    factor_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    body = f"""# 1675 - Constraint-First Z Elimination And Coframe/Source Descent

**Private status:** derivation attempt plus nonclaim leak-vector handoff. No `q_loc=0`, local-GR pass, Newton pass, PPN pass, R10 pass, WEP pass, clock pass, orbital pass, or public claim is made.

## Verdict

The constraint-first route is mathematically clean but **not parent-signed**:

```text
C_Z(Phi)=0 before q
q(Phi)|C_Z = qbar(Q_vis)
e_obs, source current, readouts, and boundary/projector terms descend through Q_vis
=> Dq_Z_norm = 0
```

Current evidence does not sign the parent constraint/no-pole origin, coframe functor, source/readout descent, source-weight/no-marker rule, or boundary/projector no-flux clause. So the zero is not adopted.

The useful progress is sharper: the surviving leak vector is now explicit. Coframe alone is not the boss fight; source/coupling ownership is.

## Source Register

{markdown_table(source_rows, ["source_key", "source_path", "exists", "needles_present", "use_in_1675"])}

## Constraint-First Descent Theorem Attempt

{markdown_table(theorem_rows, ["clause_id", "required_clause", "current_evidence", "status", "next_action"])}

## Coframe Descent Gate

{markdown_table(coframe_rows, ["gate_id", "gate", "current_evidence", "status", "effect_if_signed"])}

## Source/Readout Descent Gate

{markdown_table(source_readout_rows, ["gate_id", "gate", "current_evidence", "status", "risk_if_unsigned"])}

## Boundary/Projector Descent Gate

{markdown_table(boundary_rows, ["gate_id", "gate", "current_evidence", "status"])}

## Surviving DqZ Leak Vector

{markdown_table(leak_rows, ["leak_id", "leak_component", "status", "symbolic_bound_form", "priority_arenas"])}

## DqZ Factor Update

{markdown_table(factor_rows, ["row_id", "symbol", "new_status", "candidate_value", "projection_formula"])}

## Decisions

{markdown_table(decision_rows_, ["decision_id", "decision", "reason", "next_action"])}

## Claim Gates

{markdown_table(claim_rows, ["gate_id", "gate", "gate_pass", "status", "reason"])}

## Next Target

{markdown_table(next_rows, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Working Interpretation

This is a useful narrowing. The local branch is not dead, but the easy sentence “Z is invisible” is dead unless the parent action earns it. The next real fight is the source object-language theorem: forbid source-only weights, hidden frames, material markers, and readout-only constants. If that closes, the GR/Newton source side starts looking derivable; if it does not, those become finite testable leak coefficients.
"""
    DOC.write_text(body, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    source_rows = source_register_rows()
    theorem_rows = constraint_descent_theorem_rows()
    coframe_rows = coframe_descent_rows()
    source_readout_rows = source_readout_descent_rows()
    boundary_rows = boundary_descent_rows()
    leak_rows = surviving_leak_vector_rows()
    factor_rows = dqz_factor_update_rows()
    decision_rows_ = decision_rows()
    claim_rows = claim_gate_rows()
    next_rows = next_target_rows()

    write_csv(
        SOURCE_REGISTER,
        source_rows,
        ["branch_id", "source_key", "source_path", "exists", "needles_present", "required_needles", "use_in_1675", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        CONSTRAINT_DESCENT_THEOREM,
        theorem_rows,
        ["branch_id", "theorem_name", "formal_statement", "clause_id", "required_clause", "current_evidence", "status", "next_action", "clause_met", "parent_signed", "theorem_zero_adopted", "accepted_for_scoring", "score_ready", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        COFRAME_DESCENT_GATE,
        coframe_rows,
        ["branch_id", "gate_id", "gate", "current_evidence", "status", "effect_if_signed", "gate_pass", "theorem_zero_adopted", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        SOURCE_READOUT_DESCENT_GATE,
        source_readout_rows,
        ["branch_id", "gate_id", "gate", "current_evidence", "status", "risk_if_unsigned", "gate_pass", "theorem_zero_adopted", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        BOUNDARY_DESCENT_GATE,
        boundary_rows,
        ["branch_id", "gate_id", "gate", "current_evidence", "status", "gate_pass", "theorem_zero_adopted", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        SURVIVING_LEAK_VECTOR,
        leak_rows,
        ["branch_id", "leak_id", "leak_component", "status", "symbolic_bound_form", "priority_arenas", "candidate_value", "upper_bound", "source_paths", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        DQZ_FACTOR_UPDATE,
        factor_rows,
        ["branch_id", "row_id", "symbol", "previous_status", "new_status", "candidate_value", "upper_bound", "conditional_zero_status", "reason", "projection_formula", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        DECISION,
        decision_rows_,
        ["branch_id", "decision_id", "decision", "reason", "next_action", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        CLAIM_GATE,
        claim_rows,
        ["branch_id", "gate_id", "gate", "gate_pass", "status", "reason", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        NEXT_TARGET,
        next_rows,
        ["branch_id", "next_target", "script", "objective", "success_condition", "why_next", "valid_for_claim", "claim_allowed"],
    )

    copy_outputs()
    validation_rows = validate()
    write_csv(VALIDATION, validation_rows, ["check_id", "result", "detail", "valid_for_claim", "claim_allowed"])
    write_doc(source_rows, theorem_rows, coframe_rows, source_readout_rows, boundary_rows, leak_rows, factor_rows, decision_rows_, claim_rows, next_rows, validation_rows)

    failed_rows = [row for row in validation_rows if row["result"] != "PASS"]
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    if failed_rows:
        for failed_row in failed_rows:
            print(f"FAIL {failed_row['check_id']}: {failed_row['detail']}")
        raise SystemExit(1)
    print("1675 validation PASS")


if __name__ == "__main__":
    main()

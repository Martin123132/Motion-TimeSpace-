from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_Q_OBJECT_VERTICAL_GENERATOR_OPEN_BRANCH_2358"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2358-Y5-R2FR-q-object-vertical-generator-open-branch-proof-or-domain-bound.md"

PATHS = {
    "2357_doc": ROOT / "2357-Y5-R2FR-minimal-parent-matter-coupling-action-or-domain-motion-input.md",
    "2357_validation": OUT / "P8_Y5_BRR545_2357_VALIDATION.csv",
    "2357_signing": OUT / "P8_Y5_PARENT_QLOC_2357_ACTION_SIGNING_TESTS.csv",
    "2357_inputs": OUT / "P8_Y5_PARENT_QLOC_2357_DOMAIN_MOTION_INPUT_REQUIREMENTS.csv",
    "2357_next": OUT / "P8_Y5_PARENT_QLOC_2357_NEXT_TARGET.csv",
    "1157_qmap": OUT / "P8_Y5_R10_1157_QMAP_NULL_GENERATOR_PROOF_AUDIT.csv",
    "1157_cg": OUT / "P8_Y5_R10_1157_CG_BOUND_FIRST_FILL_ROWS.csv",
    "1737_q_contract": OUT / "P8_Y5_PARENT_QLOC_1737_Q_MAP_CONTRACT.csv",
    "1737_basis": OUT / "P8_Y5_PARENT_QLOC_1737_VERTICAL_BASIS_CONTRACT.csv",
    "1737_dq": OUT / "P8_Y5_PARENT_QLOC_1737_DQ_MATRIX_REQUIREMENTS.csv",
    "1737_finite": OUT / "P8_Y5_PARENT_QLOC_1737_FINITE_DQ_SOURCE_ROWS.csv",
    "1738_kernel": OUT / "P8_Y5_PARENT_QLOC_1738_COFRAME_KERNEL_CLAUSE_AUDIT.csv",
    "1738_theorem": OUT / "P8_Y5_PARENT_QLOC_1738_KERNEL_THEOREM_ATTEMPT.csv",
    "1738_directions": OUT / "P8_Y5_PARENT_QLOC_1738_DIRECTION_CLASSIFICATION.csv",
    "1738_rows": OUT / "P8_Y5_PARENT_QLOC_1738_FINITE_DOBS_E_SOURCE_ROWS.csv",
    "1739_ownership": OUT / "P8_Y5_PARENT_QLOC_1739_PARENT_COFRAME_OWNERSHIP_CLAUSE_GATE.csv",
    "1739_theorem": OUT / "P8_Y5_PARENT_QLOC_1739_PARENT_COFRAME_OWNERSHIP_THEOREM_ATTEMPT.csv",
    "1739_bg": OUT / "P8_Y5_PARENT_QLOC_1739_COMMON_FRAME_LOG_DERIVATIVE_ROWS.csv",
    "1575_vertical": OUT / "P8_Y5_PARENT_QLOC_1575_RAB_VERTICAL_GENERATOR_SIGNATURE_ATTEMPT.csv",
    "1575_trilemma": OUT / "P8_Y5_PARENT_QLOC_1575_RAB_COFAME_VISIBILITY_TRILEMMA.csv",
    "1575_matter": OUT / "P8_Y5_PARENT_QLOC_1575_RAB_MATTER_DESCENT_SIGNATURE.csv",
    "1621_constraint": OUT / "P8_Y5_PARENT_QLOC_1621_CONSTRAINT_FIRST_ZMAP_GATE.csv",
    "1621_nopole": OUT / "P8_Y5_PARENT_QLOC_1621_NO_POLE_THEOREM_AUDIT.csv",
    "1505_vertical": OUT / "P8_Y5_R10_1505_QUOTIENT_VERTICAL_THEOREM_LEDGER.csv",
    "1505_dq": OUT / "P8_Y5_R10_1505_DQ_VERTICALITY_TESTS.csv",
}

SOURCES = [
    ("SRC2358_00_2357_doc", "2357_doc", ["Result:", "least-handwavy coupling route"], "2357 handoff"),
    ("SRC2358_01_2357_validation", "2357_validation", ["VAL2357_OVERALL", "PASS"], "2357 validation"),
    ("SRC2358_02_2357_signing_q", "2357_signing", ["AST2357_0_PDC2356_0_q_object", "NOT_SIGNED_BY_ACTION_CANDIDATE"], "q object still upstream"),
    ("SRC2358_03_2357_inputs", "2357_inputs", ["DIR2357_1_q_vertical_open_branch", "MISSING_Q_VERTICALITY_PROOF"], "q vertical input requirement"),
    ("SRC2358_04_2357_next", "2357_next", ["NEXT2357_0", "2358-Y5-R2FR-q-object-vertical-generator-open-branch-proof-or-domain-bound.md"], "machine handoff"),
    ("SRC2358_05_1157_qmap", "1157_qmap", ["QMAP1157_8_verdict", "PARENT_Q_MAP_NULL_GENERATOR_NOT_DERIVED"], "q-map/null generator verdict"),
    ("SRC2358_06_1157_cg", "1157_cg", ["CG1157_1_zero_theorem_path", "ZERO_THEOREM_NOT_SIGNED"], "c_g first fill zero theorem block"),
    ("SRC2358_07_1737_q_contract", "1737_q_contract", ["QMAP1737_0_Q_vis", "CANDIDATE_CONTRACT_ONLY"], "q-map contract"),
    ("SRC2358_08_1737_basis", "1737_basis", ["VB1737_0_vZ", "Dq_zero_proved"], "vertical basis contract"),
    ("SRC2358_09_1737_dq", "1737_dq", ["DQM1737_5_Dq_total_kernel", "DQ_KERNEL_UNSIGNED_RETAIN_FINITE_ROWS"], "Dq matrix requirements"),
    ("SRC2358_10_1737_finite", "1737_finite", ["FDQ1737_vZ_e", "RETAINED_NONCLAIM_DQ_LEAK_INPUT"], "finite Dq source rows"),
    ("SRC2358_11_1738_kernel", "1738_kernel", ["OCK1738_6_verdict", "DOBS_E_KERNEL_ZERO_NOT_SIGNED"], "coframe kernel clause verdict"),
    ("SRC2358_12_1738_theorem", "1738_theorem", ["DOK1738_0_chain_rule_kernel", "EXACT_CONDITIONAL_THEOREM"], "coframe chain-rule theorem"),
    ("SRC2358_13_1738_directions", "1738_directions", ["DCL1738_0_vZ", "MISSING_PARENT_SELECTOR_AND_Z_BASIS"], "direction classification"),
    ("SRC2358_14_1738_rows", "1738_rows", ["DOE1738_4_total_coframe_kernel_envelope", "RETAINED_NONCLAIM_ENVELOPE"], "finite DObs_e rows"),
    ("SRC2358_15_1739_ownership", "1739_ownership", ["PCO1739_0_parent_q", "CONDITIONAL_SUPPORT_NOT_PARENT_COMPLETE"], "coframe ownership gate"),
    ("SRC2358_16_1739_theorem", "1739_theorem", ["PCO1739_THM0_chain_rule_bg_zero", "EXACT_CONDITIONAL_THEOREM"], "common-frame zero theorem"),
    ("SRC2358_17_1739_bg", "1739_bg", ["BG1739_5_total_abs", "MISSING_NUMERIC_OR_THEOREM_ZERO"], "common-frame derivative rows"),
    ("SRC2358_18_1575_vertical", "1575_vertical", ["VERT1575_5_verdict", "FAIL_CURRENT_CLAIM_VERTICALITY_NOT_SIGNED"], "RAB verticality verdict"),
    ("SRC2358_19_1575_trilemma", "1575_trilemma", ["TRI1575_1_quotient_representative", "BEST_ZERO_ROUTE_UNSIGNED"], "coframe visibility trilemma"),
    ("SRC2358_20_1575_matter", "1575_matter", ["MDS1575_5_verdict", "FAIL_CURRENT_CLAIM_DESCENT_NOT_SIGNED"], "matter descent still unsigned"),
    ("SRC2358_21_1621_constraint", "1621_constraint", ["CFG1621_7_verdict", "CONSTRAINT_FIRST_ZMAP_NOT_DERIVED"], "constraint-first alternative"),
    ("SRC2358_22_1621_nopole", "1621_nopole", ["NPA1621_5_verdict", "NO_POLE_NOT_DERIVED_CURRENT_MTS"], "no-pole alternative"),
    ("SRC2358_23_1505_vertical", "1505_vertical", ["THM1505_0_vertical_residual_safe", "EXACT_CONDITIONAL_THEOREM"], "quotient vertical theorem ledger"),
    ("SRC2358_24_1505_dq", "1505_dq", ["DQT1505_2_apply_Dq", "MISSING_COMPUTATION"], "Dq verticality tests"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2358_SOURCE_REGISTER.csv",
    "audit": OUT / "P8_Y5_PARENT_QLOC_2358_Q_VERTICAL_OPEN_BRANCH_AUDIT.csv",
    "dq_gate": OUT / "P8_Y5_PARENT_QLOC_2358_DQ_KERNEL_GATE_MATRIX.csv",
    "route": OUT / "P8_Y5_PARENT_QLOC_2358_QUOTIENT_OR_CONSTRAINT_ROUTE_LEDGER.csv",
    "bound": OUT / "P8_Y5_PARENT_QLOC_2358_DQ_DOMAIN_BOUND_ROWS.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2358_DECISION_LEDGER.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2358_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2358_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2358_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2358_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2358_VALIDATION.csv",
}


def b(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def has_needles(path: Path, needles: list[str]) -> bool:
    text = read_text(path)
    return path.exists() and all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8", errors="replace") as handle:
        return list(csv.DictReader(handle))


def source_rows() -> list[dict[str, Any]]:
    rows = []
    for row_id, source_key, needles, role in SOURCES:
        path = PATHS[source_key]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_key": source_key,
                "path": str(path),
                "exists": b(path.exists()),
                "required_needles": ";".join(needles),
                "needles_found": b(has_needles(path, needles)),
                "source_role": role,
                "valid_for_claim": "false",
            }
        )
    return rows


def open_branch_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "QVA2358_0_parent_chart",
            "gate": "parent local field chart",
            "mathematical_requirement": "Phi_parent=(Q_vis, r_aux, gauge, boundary) on an open neighbourhood with smooth admissible domain",
            "proof_status": "CHART_CONTRACT_ONLY",
            "failure_if_missing": "open-branch Dq(v)=0 cannot even be stated",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QVA2358_1_equivalence_relation",
            "gate": "parent equivalence relation",
            "mathematical_requirement": "Phi~Phi' iff ordinary-matter-visible observables and parent-owned constants/readouts agree",
            "proof_status": "EQUIVALENCE_RELATION_NOT_DERIVED",
            "failure_if_missing": "q can be chosen post-hoc to hide residuals",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QVA2358_2_q_map",
            "gate": "q object",
            "mathematical_requirement": "q: Phi_parent -> Q_vis is a parent map, not a closure label",
            "proof_status": "Q_OBJECT_NOT_PARENT_SIGNED",
            "failure_if_missing": "matter coupling action uses q without deriving it",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QVA2358_3_vertical_basis",
            "gate": "candidate vertical generator basis",
            "mathematical_requirement": "v_a are tangent to fibres of q on an open branch, with owned compensators if needed",
            "proof_status": "VERTICAL_BASIS_NOT_SIGNED",
            "failure_if_missing": "residual directions may be physical coframe/source modes",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QVA2358_4_Dq_matrix",
            "gate": "componentwise Dq kernel",
            "mathematical_requirement": "DObs_e[v]=Dsource_readout[v]=Dtheta_marker[v]=Dboundary_projector[v]=Dtau_pushforward[v]=0",
            "proof_status": "Dq_KERNEL_UNSIGNED_RETAIN_FINITE_ROWS",
            "failure_if_missing": "common-frame/source/readout leakage survives",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QVA2358_5_null_presymplectic_route",
            "gate": "null/presymplectic generator",
            "mathematical_requirement": "Omega(v_a,delta)=0 plus zero boundary charge on the same branch",
            "proof_status": "CONDITIONAL_ROUTE_NOT_CURRENTLY_SIGNED",
            "failure_if_missing": "verticality by missing kinetic term is not evidence",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QVA2358_6_constraint_no_pole_route",
            "gate": "constraint/no-pole elimination before matter",
            "mathematical_requirement": "residual is algebraic/second-class/absent before matter coupling, with no boundary/readout reentry",
            "proof_status": "BEST_ALTERNATIVE_NOT_DERIVED",
            "failure_if_missing": "finite source-current/Yukawa rows remain live",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QVA2358_7_open_branch_verdict",
            "gate": "q/v open-branch proof",
            "mathematical_requirement": "QVA2358_0 through QVA2358_6 all close in one parent branch",
            "proof_status": "OPEN_BRANCH_VERTICALITY_NOT_DERIVED",
            "failure_if_missing": "MCA2357 cannot fire as a local-GR/Newton proof",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
    ]


def dq_gate_rows() -> list[dict[str, Any]]:
    components = [
        ("DQM2358_0_DObs_e", "DObs_e[v]", "observed coframe/metric derivative", "QVA2358_2_q_map;QVA2358_4_Dq_matrix", "MISSING_THEOREM_OR_NUMERIC_DOBS_E"),
        ("DQM2358_1_Dsource_readout", "Dsource_readout[v]", "source/clock/orbit/photon/ruler/boundary readout derivative", "QVA2358_1_equivalence_relation;QVA2358_4_Dq_matrix", "MISSING_SOURCE_READOUT_DESCENT"),
        ("DQM2358_2_Dtheta_marker", "Dtheta_marker[v]", "ordinary constants/material marker derivative", "QVA2358_1_equivalence_relation;MCA2357 fixed-theta contract", "MISSING_CONSTANT_MARKER_DESCENT"),
        ("DQM2358_3_Dboundary_projector", "Dboundary_projector[v]", "boundary/projector/source-measure derivative", "QVA2358_4_Dq_matrix;QVA2358_6_constraint_no_pole_route", "MISSING_BOUNDARY_PROJECTOR_BASICNESS"),
        ("DQM2358_4_Dtau_pushforward", "Dq(L_tau Phi)-L_tau_red q(Phi)", "tau pushforward/source-clock-orbit lock", "tau parent selection;source/charge/clock/orbit branch lock", "MISSING_TAU_PROJECTABILITY"),
        ("DQM2358_5_kernel_total", "Dq[v_a]", "total Dq kernel over candidate vertical basis", "all DQM2358_0..4 zero on same open branch", "Dq_KERNEL_UNSIGNED_RETAIN_BOUND_ROWS"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "component": component,
            "meaning": meaning,
            "zero_requirement": zero_requirement,
            "current_status": status,
            "finite_fallback": f"{component}_finite_row",
            "parent_signed": "false",
            "valid_for_claim": "false",
        }
        for row_id, component, meaning, zero_requirement, status in components
    ]


def route_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "QCR2358_0_quotient_route",
            "route": "quotient representative route",
            "condition": "q object, equivalence relation, vertical basis and Dq matrix all parent-signed",
            "would_deliver": "v_a in ker(Dq); MCA2357 matter descent fires; support motion theorem-zero",
            "current_status": "BEST_ZERO_ROUTE_UNSIGNED",
            "rank": 1,
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QCR2358_1_constraint_route",
            "route": "constraint/no-pole route",
            "condition": "residual eliminated algebraically/second-class before matter coupling, no boundary/readout reentry",
            "would_deliver": "no local source-current pole without relying on vertical-by-label",
            "current_status": "BEST_LOCAL_GR_ROUTE_UNSIGNED",
            "rank": 2,
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QCR2358_2_finite_bound_route",
            "route": "finite Dq/domain bound route",
            "condition": "q/v proof fails but Dq, source/readout, common-frame, boundary and M_H_ref rows are numeric",
            "would_deliver": "testable residual vector instead of GR reduction theorem",
            "current_status": "MISSING_NUMERIC_INPUTS",
            "rank": 3,
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "QCR2358_3_closure_axiom",
            "route": "closure axiom",
            "condition": "declare residual vertical/zero without q, Dq or constraint proof",
            "would_deliver": "nothing claim-grade",
            "current_status": "REFUSED",
            "rank": 99,
            "valid_for_claim": "false",
        },
    ]


def bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQB2358_0_total",
            "quantity": "epsilon_Dq_open_branch_abs",
            "component": "absolute no-cancellation Dq/domain leakage envelope",
            "formula": "|DObs_e|+|Dsource_readout|+|Dtheta_marker|+|Dboundary_projector|+|Dtau_pushforward|+|boundary_charge|",
            "units": "dimensionless_or_declared_component_norm",
            "status": "MISSING_COMPONENT_VALUES",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQB2358_1_DObs_e",
            "quantity": "DObs_e_leak_abs",
            "component": "coframe/metric visibility of candidate vertical direction",
            "formula": "||e_obs^-1 DObs_e[v_a]||",
            "units": "dimensionless_per_declared_direction_unit",
            "status": "MISSING_DOBS_E_ZERO_OR_NUMERIC_ROW",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQB2358_2_Dsource_readout",
            "quantity": "Dsource_readout_leak_abs",
            "component": "source/clock/orbit/boundary readout visibility",
            "formula": "||Dsource_readout[Dq(v_a)]||",
            "units": "declared_readout_norm",
            "status": "MISSING_SOURCE_READOUT_ZERO_OR_NUMERIC_ROW",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQB2358_3_Dtheta_marker",
            "quantity": "Dtheta_marker_leak_abs",
            "component": "constant/material marker derivative",
            "formula": "sum_A ||L_v theta_A|| or material marker norm",
            "units": "dimensionless_or_declared_marker_norm",
            "status": "MISSING_THETA_MARKER_ZERO_OR_NUMERIC_ROW",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQB2358_4_Dboundary_projector",
            "quantity": "Dboundary_projector_leak_abs",
            "component": "boundary/projector/source-measure variation",
            "formula": "||Dboundary_projector[Dq(v_a)]||",
            "units": "boundary_projector_norm",
            "status": "MISSING_BOUNDARY_PROJECTOR_ZERO_OR_NUMERIC_ROW",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQB2358_5_Dtau_pushforward",
            "quantity": "Dtau_pushforward_leak_abs",
            "component": "tau projectability/source-clock-orbit mismatch",
            "formula": "||Dq(L_tau Phi)-L_tau_red q(Phi)||",
            "units": "tau_pushforward_norm",
            "status": "MISSING_TAU_PROJECTABILITY_ZERO_OR_NUMERIC_ROW",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQB2358_6_boundary_charge",
            "quantity": "Q_boundary_v_abs",
            "component": "boundary charge carried by the would-be vertical generator",
            "formula": "abs(int_boundary Q_v)/M_H_ref or declared boundary normalization",
            "units": "dimensionless_after_M_H_ref_or_declared_boundary_units",
            "status": "MISSING_BOUNDARY_CHARGE_ZERO_OR_NUMERIC_ROW",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQB2358_7_acceptance_rule",
            "quantity": "Dq_bound_acceptance",
            "component": "acceptance rule",
            "formula": "no Dq/domain row can score until every component has theorem-zero or numeric source path, units, direction basis and normalization",
            "units": "gate",
            "status": "NONCLAIM_ACCEPTANCE_RULE_INSTALLED",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2358_0_result",
            "decision": "do not claim q-object/open-branch verticality for current MTS",
            "reason": "parent chart, equivalence relation, Dq matrix, boundary/tau projectability, and null/constraint proof are unsigned",
            "effect": "MCA2357 cannot yet fire as a local-GR/Newton derivation",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2358_1_progress",
            "decision": "q/v gate is now precise",
            "reason": "the required proof has been reduced to open-branch chart + Dq matrix + no boundary charge, not a vague verticality claim",
            "effect": "future work can attack rows QVA2358/DQM2358 directly",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2358_2_best_route",
            "decision": "prefer parent q-object construction before numeric fallback",
            "reason": "if q and Dq close, the coupling theorem becomes clean; if not, the finite Dq vector is the honest empirical branch",
            "effect": "2359 should build the field chart/equivalence relation contract or select constraint/no-pole explicitly",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2358_0_q_object",
            "claim": "parent q object is constructed",
            "passes_public_claim": "false",
            "blocked_by": "QVA2358_0_parent_chart;QVA2358_1_equivalence_relation;QVA2358_2_q_map",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2358_1_vertical_generator",
            "claim": "v_a in ker(Dq) on an open local branch",
            "passes_public_claim": "false",
            "blocked_by": "QVA2358_3_vertical_basis;QVA2358_4_Dq_matrix;DQM2358_5_kernel_total",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2358_2_constraint_no_pole",
            "claim": "constraint/no-pole alternative removes residual before matter",
            "passes_public_claim": "false",
            "blocked_by": "QVA2358_6_constraint_no_pole_route;QCR2358_1_constraint_route",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2358_3_local_GR_Newton",
            "claim": "local GR/Newton source-current gate reopens",
            "passes_public_claim": "false",
            "blocked_by": "q/v not derived; constraint/no-pole not derived; finite Dq bound rows missing",
            "valid_for_claim": "false",
        },
    ]


def refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2358_0_q_by_declaration",
            "temptation": "define q to exclude every troublesome residual",
            "allowed": "false",
            "why_not": "q must be supplied by parent kinematics/action before readout, not chosen after the local tests",
            "blocking_rows": "QVA2358_1_equivalence_relation;QVA2358_2_q_map",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2358_1_vertical_by_label",
            "temptation": "call v vertical without computing the Dq matrix",
            "allowed": "false",
            "why_not": "DObs_e, source/readout, markers, boundary/projector and tau pushforward must all vanish or be bounded",
            "blocking_rows": "QVA2358_4_Dq_matrix;DQM2358_5_kernel_total",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2358_2_missing_kinetic_as_null",
            "temptation": "treat absent/missing kinetic terms as proof of null gauge direction",
            "allowed": "false",
            "why_not": "null direction needs presymplectic degeneracy and zero boundary/source charge, not absence of a written term",
            "blocking_rows": "QVA2358_5_null_presymplectic_route;DQB2358_6_boundary_charge",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2358_3_magic_constraint",
            "temptation": "insert a multiplier to remove the residual and call it derived",
            "allowed": "false",
            "why_not": "constraint/no-pole route needs parent origin, algebraic sort, no kinetic pole and boundary/readout stability",
            "blocking_rows": "QVA2358_6_constraint_no_pole_route;CG2358_2_constraint_no_pole",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2358_0",
            "next_target": "2359-Y5-R2FR-parent-q-field-chart-equivalence-relation-or-no-pole-selector.md",
            "why": "the missing proof starts at the parent field chart/equivalence relation; if that cannot be sourced, choose the constraint/no-pole route explicitly",
            "route_type": "derivation_first",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2358_1",
            "next_target": "2359b-Y5-R2FR-Dq-matrix-finite-bound-input-pack.md",
            "why": "fallback if q/v cannot close: source every Dq/domain component row with units and arena projection",
            "route_type": "fallback_nonclaim",
            "valid_for_claim": "false",
        },
    ]


def copy_branch_artifacts() -> list[dict[str, Any]]:
    copies = [
        (OUTPUTS["audit"], BETA_DOCS / "Q_VERTICAL_OPEN_BRANCH_AUDIT_2358_NONCLAIM.csv", "beta docs q vertical audit"),
        (OUTPUTS["bound"], MICRO_RESIDUALS / "DQ_DOMAIN_BOUND_ROWS_2358_NONCLAIM.csv", "microscope Dq/domain bound rows"),
        (OUTPUTS["decision"], RAB_QUEUE / "JR2358_Q_VERTICAL_DECISION_NONCLAIM.csv", "RAB queue decision ledger"),
    ]
    rows = []
    for src, dst, role in copies:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": f"COPY2358_{len(rows)}",
                "source": str(src),
                "destination": str(dst),
                "copy_role": role,
                "copy_exists": b(dst.exists() and dst.stat().st_size > 0),
                "valid_for_claim": "false",
            }
        )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body]) + "\n"


def write_markdown(
    sources: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    dq_gate: list[dict[str, Any]],
    route: list[dict[str, Any]],
    bound: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    refusals: list[dict[str, Any]],
    next_targets: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    created = datetime.now(timezone.utc).isoformat()
    text = f"""# 2358 — `q` Object / Vertical Generator Open-Branch Proof Or Domain Bound

Created UTC: `{created}`

Branch: `{BRANCH_ID}`

## Result

Result: the **`q` object / vertical-generator proof does not close for current MTS yet**.

The exact theorem route is now clear: build a parent local field chart and equivalence relation, define
`q: Phi_parent -> Q_vis`, prove the candidate generators are tangent to fibres on an open branch, and verify the full
`Dq` matrix: coframe, source/readout, constants/markers, boundary/projector and tau pushforward.

That does **not** happen in the current corpus. Therefore `MCA2357` remains a clean coupling candidate, not a local-GR/Newton
derivation. The finite fallback is the explicit no-cancellation envelope `epsilon_Dq_open_branch_abs`.

## Source Audit

{md_table(sources, ["row_id", "source_key", "exists", "needles_found", "source_role"])}

## Open-Branch Audit

{md_table(audit, ["row_id", "gate", "mathematical_requirement", "proof_status", "failure_if_missing", "parent_signed", "valid_for_claim"])}

## Dq Kernel Gate Matrix

{md_table(dq_gate, ["row_id", "component", "meaning", "zero_requirement", "current_status", "finite_fallback", "valid_for_claim"])}

## Quotient / Constraint Routes

{md_table(route, ["row_id", "route", "condition", "would_deliver", "current_status", "rank", "valid_for_claim"])}

## Dq / Domain Bound Rows

{md_table(bound, ["row_id", "quantity", "component", "formula", "status", "units", "score_ready", "valid_for_claim"])}

## Decision Ledger

{md_table(decisions, ["row_id", "decision", "reason", "effect", "valid_for_claim"])}

## Claim Gates

{md_table(claims, ["row_id", "claim", "passes_public_claim", "blocked_by", "valid_for_claim"])}

## Refusal Runner

{md_table(refusals, ["row_id", "temptation", "allowed", "why_not", "blocking_rows", "valid_for_claim"])}

## Next Targets

{md_table(next_targets, ["row_id", "next_target", "why", "route_type", "valid_for_claim"])}

## Validation

{md_table(validation, ["row_id", "status", "detail", "valid_for_claim"])}
"""
    DOC.write_text(text, encoding="utf-8")


def formalization_hits() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    hits: list[Path] = []
    for path in FORMALIZATION.rglob("*2358*"):
        if not path.is_file():
            continue
        parts = {part.lower() for part in path.parts}
        if ".venv" in parts or "site-packages" in parts or "__pycache__" in parts:
            continue
        if path.name.startswith(("2358-", "P8_Y5_PARENT_QLOC_2358", "P8_Y5_BRR545_2358")):
            hits.append(path)
    return hits


def no_true_claim_flags(paths: list[Path]) -> bool:
    guarded_columns = {
        "valid_for_claim",
        "passes_public_claim",
        "score_ready",
        "claim_allowed",
        "valid_prediction_row",
        "parent_signed",
    }
    for path in paths:
        if path.suffix.lower() != ".csv":
            continue
        for row in read_csv(path):
            for column in guarded_columns:
                if row.get(column, "").strip().lower() == "true":
                    return False
    return True


def validation_rows(sources: list[dict[str, Any]], copies: list[dict[str, Any]]) -> list[dict[str, Any]]:
    produced = [path for key, path in OUTPUTS.items() if key != "validation"]
    audit_text = read_text(OUTPUTS["audit"])
    dq_gate = read_csv(OUTPUTS["dq_gate"])
    bound = read_csv(OUTPUTS["bound"])
    claims = read_csv(OUTPUTS["claims"])
    next_text = read_text(OUTPUTS["next"])
    checks = [
        ("VAL2358_00_required_sources_exist", all(row["exists"] == "true" for row in sources), "every required source path exists"),
        ("VAL2358_01_required_needles_found", all(row["needles_found"] == "true" for row in sources), "all required source needles were found"),
        ("VAL2358_02_outputs_exist", all(path.exists() and path.stat().st_size > 0 for path in produced), "all 2358 outputs written"),
        ("VAL2358_03_open_branch_audit_written", "QVA2358_7_open_branch_verdict" in audit_text and "OPEN_BRANCH_VERTICALITY_NOT_DERIVED" in audit_text, "open-branch q/v audit written and blocked"),
        ("VAL2358_04_dq_gate_nonclaim", dq_gate and all(row.get("parent_signed") == "false" and row.get("valid_for_claim") == "false" for row in dq_gate), "Dq kernel gates remain nonclaim"),
        ("VAL2358_05_bound_rows_nonclaim", bound and all(row.get("score_ready") == "false" and row.get("valid_for_claim") == "false" for row in bound), "Dq/domain bound rows remain non-score-ready"),
        ("VAL2358_06_claim_gates_blocked", claims and all(row.get("passes_public_claim") == "false" and row.get("valid_for_claim") == "false" for row in claims), "all public claim gates blocked"),
        ("VAL2358_07_next_selected", "2359-Y5-R2FR-parent-q-field-chart-equivalence-relation-or-no-pole-selector.md" in next_text, "2359 field-chart/equivalence target selected"),
        ("VAL2358_08_branch_copies_parse", copies and all(row["copy_exists"] == "true" for row in copies), "branch copies exist"),
        ("VAL2358_09_formalization_untouched", not formalization_hits(), "no 2358 checkpoint output appears in formalization-workbench"),
        ("VAL2358_10_no_claim_flags", no_true_claim_flags(produced), "no generated row has claim/score-ready/parent-signed true flags"),
        ("VAL2358_11_no_github_policy", True, "public GitHub update not recommended from 2358"),
    ]
    rows = [
        {
            "row_id": row_id,
            "status": "PASS" if ok else "FAIL",
            "detail": detail,
            "valid_for_claim": "false",
        }
        for row_id, ok, detail in checks
    ]
    rows.append(
        {
            "row_id": "VAL2358_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "2358 audits the q-object/open-branch vertical-generator proof, refuses q-by-declaration and vertical-by-label, keeps Dq/domain bound rows nonclaim, and selects parent field-chart/equivalence construction as 2359.",
            "valid_for_claim": "false",
        }
    )
    return rows


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    audit = open_branch_audit_rows()
    dq_gate = dq_gate_rows()
    route = route_rows()
    bound = bound_rows()
    decisions = decision_rows()
    claims = claim_gate_rows()
    refusals = refusal_rows()
    next_targets = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["audit"], audit)
    write_csv(OUTPUTS["dq_gate"], dq_gate)
    write_csv(OUTPUTS["route"], route)
    write_csv(OUTPUTS["bound"], bound)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["claims"], claims)
    write_csv(OUTPUTS["refusal"], refusals)
    write_csv(OUTPUTS["next"], next_targets)

    copies = copy_branch_artifacts()
    write_csv(OUTPUTS["copies"], copies)

    validation = validation_rows(sources, copies)
    write_csv(OUTPUTS["validation"], validation)
    write_markdown(sources, audit, dq_gate, route, bound, decisions, claims, refusals, next_targets, validation)

    if validation[-1]["status"] != "PASS":
        failed = ", ".join(row["row_id"] for row in validation if row["status"] != "PASS")
        raise SystemExit(f"2358 validation failed: {failed}")
    print(f"2358 checkpoint written: {DOC}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

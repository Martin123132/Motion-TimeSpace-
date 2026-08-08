from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_PARENT_Q_FIELD_CHART_EQUIV_OR_NOPOLE_SELECTOR_2359"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2359-Y5-R2FR-parent-q-field-chart-equivalence-relation-or-no-pole-selector.md"

PATHS = {
    "2358_doc": ROOT / "2358-Y5-R2FR-q-object-vertical-generator-open-branch-proof-or-domain-bound.md",
    "2358_validation": OUT / "P8_Y5_BRR545_2358_VALIDATION.csv",
    "2358_audit": OUT / "P8_Y5_PARENT_QLOC_2358_Q_VERTICAL_OPEN_BRANCH_AUDIT.csv",
    "2358_route": OUT / "P8_Y5_PARENT_QLOC_2358_QUOTIENT_OR_CONSTRAINT_ROUTE_LEDGER.csv",
    "2358_next": OUT / "P8_Y5_PARENT_QLOC_2358_NEXT_TARGET.csv",
    "1667_chart": OUT / "P8_Y5_PARENT_QLOC_1667_PARENT_FIELD_CHART_CANDIDATE.csv",
    "1667_qmap": OUT / "P8_Y5_PARENT_QLOC_1667_QUOTIENT_MAP_AUDIT.csv",
    "1667_dq": OUT / "P8_Y5_PARENT_QLOC_1667_DQ_ON_ZPHI_TESTS.csv",
    "1667_constraint": OUT / "P8_Y5_PARENT_QLOC_1667_CONSTRAINT_FIRST_BRANCH_AUDIT.csv",
    "1675_theorem": OUT / "P8_Y5_PARENT_QLOC_1675_CONSTRAINT_FIRST_DESCENT_THEOREM_ATTEMPT.csv",
    "1675_coframe": OUT / "P8_Y5_PARENT_QLOC_1675_COFRAME_DESCENT_GATE.csv",
    "1675_readout": OUT / "P8_Y5_PARENT_QLOC_1675_SOURCE_READOUT_DESCENT_GATE.csv",
    "1675_leaks": OUT / "P8_Y5_PARENT_QLOC_1675_SURVIVING_DQZ_LEAK_VECTOR_NONCLAIM.csv",
    "1562_origin": OUT / "P8_Y5_PARENT_QLOC_1562_LAMBDAR_ORIGIN_AUDIT.csv",
    "1562_class": OUT / "P8_Y5_PARENT_QLOC_1562_CONSTRAINT_CLASS_GATE.csv",
    "1562_stress": OUT / "P8_Y5_PARENT_QLOC_1562_ZERO_STRESS_VARIATION_GATE.csv",
    "1562_route": OUT / "P8_Y5_PARENT_QLOC_1562_ROUTE_DECISION_LEDGER.csv",
    "1576_qmap": OUT / "P8_Y5_PARENT_QLOC_1576_RAB_QUOTIENT_MAP_CONSTRUCTION_ATTEMPT.csv",
    "1576_cnp": OUT / "P8_Y5_PARENT_QLOC_1576_RAB_CONSTRAINT_NO_POLE_TEST.csv",
    "1576_nopole": OUT / "P8_Y5_PARENT_QLOC_1576_RAB_NO_POLE_THEOREM_ATTEMPT.csv",
    "1576_fallback": OUT / "P8_Y5_PARENT_QLOC_1576_RAB_FINITE_FALLBACK_COMPONENT_ROWS.csv",
}

SOURCES = [
    ("SRC2359_00_2358_doc", "2358_doc", ["Result:", "`q` object / vertical-generator proof"], "2358 handoff"),
    ("SRC2359_01_2358_validation", "2358_validation", ["VAL2358_OVERALL", "PASS"], "2358 validation"),
    ("SRC2359_02_2358_audit", "2358_audit", ["QVA2358_7_open_branch_verdict", "OPEN_BRANCH_VERTICALITY_NOT_DERIVED"], "2358 q/v audit verdict"),
    ("SRC2359_03_2358_route", "2358_route", ["QCR2358_0_quotient_route", "BEST_ZERO_ROUTE_UNSIGNED"], "2358 route ledger"),
    ("SRC2359_04_2358_next", "2358_next", ["NEXT2358_0", "2359-Y5-R2FR-parent-q-field-chart-equivalence-relation-or-no-pole-selector.md"], "machine handoff"),
    ("SRC2359_05_1667_chart", "1667_chart", ["PFC1667_7_chart_verdict", "FIELD_CHART_CANDIDATE_NOT_PARENT_SIGNED"], "field chart candidate"),
    ("SRC2359_06_1667_qmap", "1667_qmap", ["QMA1667_6_verdict", "Q_NOT_COMPUTABLE_CURRENT_CORPUS"], "quotient map audit"),
    ("SRC2359_07_1667_dq", "1667_dq", ["DQT1667_6_verdict", "DQ_ZPHI_NOT_CLOSED_RETAIN_LEAK"], "Dq on Z/phi tests"),
    ("SRC2359_08_1667_constraint", "1667_constraint", ["CFB1667_5_verdict", "SELECT_NEXT_CONSTRAINT_OR_DQ_LEAK_BOUND"], "constraint-first branch audit"),
    ("SRC2359_09_1675_theorem", "1675_theorem", ["CFD1675_6_verdict", "DESCENT_THEOREM_NOT_CLOSED"], "constraint-first descent theorem"),
    ("SRC2359_10_1675_coframe", "1675_coframe", ["CDG1675_3_verdict", "COFRAME_DESCENT_NOT_PARENT_SIGNED"], "coframe descent gate"),
    ("SRC2359_11_1675_readout", "1675_readout", ["SRD1675_5_verdict", "SOURCE_READOUT_DESCENT_NOT_CLOSED"], "source/readout descent gate"),
    ("SRC2359_12_1675_leaks", "1675_leaks", ["LEAK1675_5_residual_lock", "MISSING_NUMERIC_OR_THEOREM_ZERO"], "surviving DqZ leak vector"),
    ("SRC2359_13_1562_origin", "1562_origin", ["ORG1562_3_second_class_auxiliary", "BEST_CONDITIONAL_ROUTE"], "lambda_R origin audit"),
    ("SRC2359_14_1562_class", "1562_class", ["CLASS1562_5_second_class", "BETTER_CONDITIONAL_THAN_FIRST_CLASS"], "constraint class gate"),
    ("SRC2359_15_1562_stress", "1562_stress", ["STR1562_5_current", "FAIL_CURRENT_CLAIM"], "zero stress variation gate"),
    ("SRC2359_16_1562_route", "1562_route", ["ROUTE1562_1_second_class_auxiliary", "BEST_DERIVATION_ROUTE_CONDITIONAL"], "route decision ledger"),
    ("SRC2359_17_1576_qmap", "1576_qmap", ["QMAP1576_2_constraint_first", "POSSIBLE_IF_CONSTRAINT_SIGNED"], "RAB q-map construction"),
    ("SRC2359_18_1576_cnp", "1576_cnp", ["CNP1576_5_verdict", "FAIL_CURRENT_CLAIM_CONSTRAINT_NO_POLE_NOT_DERIVED"], "constraint no-pole test"),
    ("SRC2359_19_1576_nopole", "1576_nopole", ["NPT1576_3_verdict", "FAIL_CURRENT_CLAIM_NO_POLE_NOT_DERIVED"], "no-pole theorem attempt"),
    ("SRC2359_20_1576_fallback", "1576_fallback", ["FF1576_0_constraint_origin", "MISSING_PARENT_CONSTRAINT_ORIGIN"], "finite fallback rows"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2359_SOURCE_REGISTER.csv",
    "chart": OUT / "P8_Y5_PARENT_QLOC_2359_FIELD_CHART_EQUIVALENCE_AUDIT.csv",
    "selector": OUT / "P8_Y5_PARENT_QLOC_2359_NOPOLE_SELECTOR_GATE.csv",
    "route": OUT / "P8_Y5_PARENT_QLOC_2359_ROUTE_SELECTION_LEDGER.csv",
    "inputs": OUT / "P8_Y5_PARENT_QLOC_2359_NEXT_INPUT_REQUIREMENTS.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2359_DECISION_LEDGER.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2359_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2359_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2359_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2359_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2359_VALIDATION.csv",
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


def chart_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "FCE2359_0_visible_quotient",
            "object": "Q_vis",
            "candidate": "Q_vis=(e_obs,g_obs,source/readout data,theta_owned)",
            "status": "CANDIDATE_CONTRACT_ONLY",
            "why_not_closed": "ordinary-matter visible data are listed, but no parent action/field bundle constructs them as quotient coordinates",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FCE2359_1_parent_chart",
            "object": "Phi_parent",
            "candidate": "Phi_parent=(Q_vis,R_phys,Z,phi,Psi_A,theta_A,B_edge,P_loc)",
            "status": "FIELD_CHART_CANDIDATE_NOT_PARENT_SIGNED",
            "why_not_closed": "chart is a useful testing grammar, not an adopted parent variable chart",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FCE2359_2_equivalence_relation",
            "object": "Phi~Phi'",
            "candidate": "same Q_vis, same fixed theta, same parent-owned readout/support class",
            "status": "EQUIVALENCE_RELATION_NOT_DERIVED",
            "why_not_closed": "the relation is not generated by constraints/gauge/orbits from the parent action",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FCE2359_3_computable_q",
            "object": "q: Phi_parent -> Q_vis",
            "candidate": "projection to visible quotient data",
            "status": "Q_NOT_COMPUTABLE_CURRENT_CORPUS",
            "why_not_closed": "Dq cannot be evaluated on live residual directions because q components and tangent basis are unsigned",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FCE2359_4_RAB_shape_only",
            "object": "shape-only quotient option",
            "candidate": "quotient reciprocal cell-volume while preserving physical shape/orientation",
            "status": "POSSIBLE_CONTRACT_NOT_CONSTRUCTED",
            "why_not_closed": "requires independent unit/cell normalization and observed coframe functor",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FCE2359_5_chart_verdict",
            "object": "parent q field-chart/equivalence route",
            "candidate": "FCE2359_0..4 close together",
            "status": "Q_FIELD_CHART_NOT_DERIVED",
            "why_not_closed": "current files do not construct the quotient as parent kinematics rather than testing grammar",
            "parent_signed": "false",
            "valid_for_claim": "false",
        },
    ]


def selector_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NPS2359_0_second_class_auxiliary",
            "route": "second-class/algebraic auxiliary compatibility",
            "test": "S_R=int mu_parent Lambda_R [R_AB-C_AB(q,theta,top)] with no derivative grammar",
            "status": "BEST_DERIVATION_ROUTE_CONDITIONAL",
            "missing": "parent origin; parent sort; no-derivative operator exclusion; matter descent; boundary/readout stability",
            "selected_next": "true",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NPS2359_1_first_class_route",
            "route": "first-class constraint/no-pole",
            "test": "Omega_flat(v_R)=delta C_R, closed brackets, proper boundary charge, degree-count certificate",
            "status": "POSSIBLE_BUT_BLOCKED",
            "missing": "H_core, brackets, degree count, differentiable generator, boundary charge",
            "selected_next": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NPS2359_2_positive_nohair",
            "route": "positive source-free no-hair fallback",
            "test": "Z_R>0, M_R^2>0, J_R=0, boundary flux=0, allowed topology",
            "status": "VALUES_AND_SOURCE_ZERO_MISSING",
            "missing": "operator values, source-zero, topology and boundary flux",
            "selected_next": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NPS2359_3_absent_nonprimitive",
            "route": "absent/nonprimitive parent field",
            "test": "R_AB is derived/readout artefact eliminated before variation and absent from S_matter",
            "status": "PROMISING_NOT_PARENT_PROVED",
            "missing": "parent field grammar and readout derivation",
            "selected_next": "parallel",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NPS2359_4_finite_leak",
            "route": "finite Dq/source-current leak vector",
            "test": "retain coframe, source-weight, constants, readout, boundary and residual-lock leak rows",
            "status": "FALLBACK_NONCLAIM",
            "missing": "numeric values, units, source paths and M_H_ref",
            "selected_next": "fallback",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NPS2359_5_selector_verdict",
            "route": "route selection",
            "test": "choose best next derivation target after q field-chart route fails current proof",
            "status": "SELECT_SECOND_CLASS_AUXILIARY_ORIGIN_NEXT",
            "missing": "not a claim; only next-target selection",
            "selected_next": "true",
            "valid_for_claim": "false",
        },
    ]


def route_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "RSL2359_0_q_route",
            "route": "parent q field-chart/equivalence",
            "rank_before": 1,
            "rank_after": 2,
            "verdict": "PARK_AS_REQUIRED_BUT_NOT_NEXT",
            "reason": "the chart/equivalence relation is still candidate-only and needs parent kinematics not present in corpus",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RSL2359_1_second_class_route",
            "route": "second-class auxiliary/no-pole origin",
            "rank_before": 2,
            "rank_after": 1,
            "verdict": "SELECT_NEXT_DERIVATION_ATTACK",
            "reason": "it avoids calling a visible residual gauge and attacks the residual before matter coupling",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RSL2359_2_finite_route",
            "route": "finite Dq/source-current coefficients",
            "rank_before": 3,
            "rank_after": 3,
            "verdict": "KEEP_FALLBACK",
            "reason": "needed if the second-class/no-pole origin also fails",
            "valid_for_claim": "false",
        },
    ]


def input_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "INP2359_0_parent_origin",
            "input_needed": "parent origin of Lambda_R/C_R",
            "required_fields": "action_term; MTS_core_derivation; C_R_definition; variation_class; source_path",
            "current_status": "MISSING_PARENT_CONSTRAINT_ORIGIN",
            "feeds": "NPS2359_0_second_class_auxiliary",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "INP2359_1_no_derivative_grammar",
            "input_needed": "operator grammar excluding derivatives/kinetic pole",
            "required_fields": "allowed_operators; forbidden_D_RAB_terms; Hessian_rank; no_Green_kernel_certificate",
            "current_status": "MISSING_OPERATOR_SIGNATURE",
            "feeds": "NPS2359_0_second_class_auxiliary;NPS2359_2_positive_nohair",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "INP2359_2_zero_stress_reaction",
            "input_needed": "E_R reaction stress theorem",
            "required_fields": "E_R equation; Lambda_R_solution; matter_source_zero; boundary_zero; readout_stability",
            "current_status": "MISSING_ZERO_STRESS_VARIATION_PROOF",
            "feeds": "NPS2359_0_second_class_auxiliary",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "INP2359_3_boundary_readout_stability",
            "input_needed": "boundary/readout reentry silence",
            "required_fields": "boundary_charge; edge_mode; source_readout_map; tau/frame lock; source_path",
            "current_status": "MISSING_BOUNDARY_READOUT_STABILITY",
            "feeds": "NPS2359_0_second_class_auxiliary;NPS2359_4_finite_leak",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2359_0_result",
            "decision": "do not claim parent q field-chart/equivalence construction",
            "reason": "the field chart and q map remain candidate contracts, not parent-derived kinematics",
            "effect": "q/v route remains required but not currently the fastest derivation attack",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2359_1_selector",
            "decision": "select second-class auxiliary/no-pole origin as next derivation route",
            "reason": "it removes the visible residual before matter coupling instead of quotienting it after the fact",
            "effect": "2360 targets parent origin/no-derivative grammar/zero-stress reaction",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2359_2_no_public_claim",
            "decision": "keep all local-GR/Newton gates blocked",
            "reason": "no route has parent-signed the required action/constraint/boundary package",
            "effect": "private derivation continues; no GitHub/public update",
            "valid_for_claim": "false",
        },
    ]


def claim_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2359_0_q_chart",
            "claim": "parent q field chart/equivalence relation constructed",
            "passes_public_claim": "false",
            "blocked_by": "FCE2359_1_parent_chart;FCE2359_2_equivalence_relation;FCE2359_3_computable_q",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2359_1_constraint_no_pole",
            "claim": "second-class/no-pole route derived",
            "passes_public_claim": "false",
            "blocked_by": "INP2359_0_parent_origin;INP2359_1_no_derivative_grammar;INP2359_2_zero_stress_reaction",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2359_2_local_GR_Newton",
            "claim": "local GR/Newton source-current branch derived",
            "passes_public_claim": "false",
            "blocked_by": "q chart not derived; no-pole route not derived; finite leak vector missing values",
            "valid_for_claim": "false",
        },
    ]


def refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2359_0_candidate_chart_as_parent",
            "temptation": "treat the 1667 field chart candidate as the parent chart",
            "allowed": "false",
            "why_not": "a chart used for testing is not a parent kinematic derivation",
            "blocking_rows": "FCE2359_1_parent_chart;CG2359_0_q_chart",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2359_1_shape_only_without_units",
            "temptation": "use shape-only quotient without constructing unit/cell normalization",
            "allowed": "false",
            "why_not": "R_AB/J_q may be visible to rods/clocks/source readout unless the normalization is parent-owned",
            "blocking_rows": "FCE2359_4_RAB_shape_only",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2359_2_magic_lambda",
            "temptation": "insert lambda_R R_AB and call the residual gone",
            "allowed": "false",
            "why_not": "the multiplier origin, operator grammar, reaction stress and boundary/readout stability are the theorem",
            "blocking_rows": "INP2359_0_parent_origin;INP2359_2_zero_stress_reaction",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2359_0",
            "next_target": "2360-Y5-R2FR-second-class-auxiliary-origin-no-derivative-grammar-or-finite-leak.md",
            "why": "best next derivation route is to prove the parent origin/no-derivative/zero-stress package for the second-class auxiliary/no-pole selector",
            "route_type": "derivation_first",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2359_1",
            "next_target": "2360b-Y5-R2FR-q-field-chart-adoption-certificate.md",
            "why": "parallel route if a source can derive the q chart/equivalence from MTS core",
            "route_type": "parallel_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2359_2",
            "next_target": "2360c-Y5-R2FR-finite-Dq-leak-vector-input-pack.md",
            "why": "fallback if neither q chart nor no-pole origin closes",
            "route_type": "fallback_nonclaim",
            "valid_for_claim": "false",
        },
    ]


def copy_branch_artifacts() -> list[dict[str, Any]]:
    copies = [
        (OUTPUTS["chart"], BETA_DOCS / "FIELD_CHART_EQUIVALENCE_AUDIT_2359_NONCLAIM.csv", "beta docs field chart audit"),
        (OUTPUTS["selector"], MICRO_RESIDUALS / "NOPOLE_SELECTOR_GATE_2359_NONCLAIM.csv", "microscope no-pole selector gate"),
        (OUTPUTS["decision"], RAB_QUEUE / "JR2359_ROUTE_DECISION_NONCLAIM.csv", "RAB queue route decision"),
    ]
    rows = []
    for src, dst, role in copies:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": f"COPY2359_{len(rows)}",
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
    chart: list[dict[str, Any]],
    selector: list[dict[str, Any]],
    route: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    refusals: list[dict[str, Any]],
    next_targets: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    created = datetime.now(timezone.utc).isoformat()
    text = f"""# 2359 — Parent `q` Field Chart / Equivalence Relation Or No-Pole Selector

Created UTC: `{created}`

Branch: `{BRANCH_ID}`

## Result

Result: the **parent `q` field-chart/equivalence route remains candidate-only**, not derived.

The chart `Phi_parent=(Q_vis,R_phys,Z,phi,Psi_A,theta_A,B_edge,P_loc)` is useful, but current files do not construct it
as parent kinematics or derive the equivalence relation from constraints/gauge orbits. So the `q` route stays required,
but it is not the sharpest next attack.

The selected next route is the **second-class auxiliary / no-pole origin**: derive the parent origin of the constraint,
exclude derivative/kinetic terms, prove zero reaction stress, and block boundary/readout reentry. This is the least post-hoc
route because it removes the visible residual before matter coupling instead of declaring it vertical after the fact.

## Source Audit

{md_table(sources, ["row_id", "source_key", "exists", "needles_found", "source_role"])}

## Field Chart / Equivalence Audit

{md_table(chart, ["row_id", "object", "candidate", "status", "why_not_closed", "parent_signed", "valid_for_claim"])}

## No-Pole Selector Gate

{md_table(selector, ["row_id", "route", "test", "status", "missing", "selected_next", "valid_for_claim"])}

## Route Selection Ledger

{md_table(route, ["row_id", "route", "rank_before", "rank_after", "verdict", "reason", "valid_for_claim"])}

## Next Input Requirements

{md_table(inputs, ["row_id", "input_needed", "required_fields", "current_status", "feeds", "valid_for_claim"])}

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
    for path in FORMALIZATION.rglob("*2359*"):
        if not path.is_file():
            continue
        parts = {part.lower() for part in path.parts}
        if ".venv" in parts or "site-packages" in parts or "__pycache__" in parts:
            continue
        if path.name.startswith(("2359-", "P8_Y5_PARENT_QLOC_2359", "P8_Y5_BRR545_2359")):
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
        "accepted_for_scoring",
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
    chart_text = read_text(OUTPUTS["chart"])
    selector_text = read_text(OUTPUTS["selector"])
    claims = read_csv(OUTPUTS["claims"])
    next_text = read_text(OUTPUTS["next"])
    checks = [
        ("VAL2359_00_required_sources_exist", all(row["exists"] == "true" for row in sources), "every required source path exists"),
        ("VAL2359_01_required_needles_found", all(row["needles_found"] == "true" for row in sources), "all required source needles were found"),
        ("VAL2359_02_outputs_exist", all(path.exists() and path.stat().st_size > 0 for path in produced), "all 2359 outputs written"),
        ("VAL2359_03_q_chart_not_promoted", "FCE2359_5_chart_verdict" in chart_text and "Q_FIELD_CHART_NOT_DERIVED" in chart_text, "q field-chart/equivalence route not promoted"),
        ("VAL2359_04_nopole_selected_nonclaim", "NPS2359_5_selector_verdict" in selector_text and "SELECT_SECOND_CLASS_AUXILIARY_ORIGIN_NEXT" in selector_text, "second-class/no-pole origin selected as nonclaim next route"),
        ("VAL2359_05_claim_gates_blocked", claims and all(row.get("passes_public_claim") == "false" and row.get("valid_for_claim") == "false" for row in claims), "all public claim gates blocked"),
        ("VAL2359_06_next_selected", "2360-Y5-R2FR-second-class-auxiliary-origin-no-derivative-grammar-or-finite-leak.md" in next_text, "2360 second-class auxiliary origin target selected"),
        ("VAL2359_07_branch_copies_parse", copies and all(row["copy_exists"] == "true" for row in copies), "branch copies exist"),
        ("VAL2359_08_formalization_untouched", not formalization_hits(), "no 2359 checkpoint output appears in formalization-workbench"),
        ("VAL2359_09_no_claim_flags", no_true_claim_flags(produced), "no generated row has claim/score-ready/parent-signed true flags"),
        ("VAL2359_10_no_github_policy", True, "public GitHub update not recommended from 2359"),
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
            "row_id": "VAL2359_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "2359 refuses to promote the candidate q field chart, selects the second-class auxiliary/no-pole origin route as the next derivation attack, and keeps all local-GR/Newton gates blocked.",
            "valid_for_claim": "false",
        }
    )
    return rows


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    chart = chart_rows()
    selector = selector_rows()
    route = route_rows()
    inputs = input_rows()
    decisions = decision_rows()
    claims = claim_rows()
    refusals = refusal_rows()
    next_targets = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["chart"], chart)
    write_csv(OUTPUTS["selector"], selector)
    write_csv(OUTPUTS["route"], route)
    write_csv(OUTPUTS["inputs"], inputs)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["claims"], claims)
    write_csv(OUTPUTS["refusal"], refusals)
    write_csv(OUTPUTS["next"], next_targets)

    copies = copy_branch_artifacts()
    write_csv(OUTPUTS["copies"], copies)

    validation = validation_rows(sources, copies)
    write_csv(OUTPUTS["validation"], validation)
    write_markdown(sources, chart, selector, route, inputs, decisions, claims, refusals, next_targets, validation)

    if validation[-1]["status"] != "PASS":
        failed = ", ".join(row["row_id"] for row in validation if row["status"] != "PASS")
        raise SystemExit(f"2359 validation failed: {failed}")
    print(f"2359 checkpoint written: {DOC}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

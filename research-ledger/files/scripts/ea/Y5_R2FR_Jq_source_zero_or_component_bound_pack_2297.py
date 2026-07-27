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

BRANCH_ID = "MTS_R2FR_Q_JQ_SOURCE_BOUND_2297"
DOC = ROOT / "2297-Y5-R2FR-Jq-source-zero-or-component-bound-pack.md"

PATHS = {
    "2296_doc": ROOT / "2296-Y5-R2FR-q-sourcefree-positive-nohair-or-firstclass-owner-gate.md",
    "2296_validation": OUT / "P8_Y5_BRR545_2296_VALIDATION.csv",
    "2296_next": OUT / "P8_Y5_PARENT_QLOC_2296_NEXT_TARGET.csv",
    "2296_jq_audit": OUT / "P8_Y5_PARENT_QLOC_2296_JQ_SOURCE_ZERO_AUDIT.csv",
    "2296_nohair": OUT / "P8_Y5_PARENT_QLOC_2296_Q_CONDITIONAL_NOHAIR_IDENTITY.csv",
    "2249_doc": ROOT / "2249-Y5-R2FR-RAB-JR-source-zero-or-component-bound-pack.md",
    "2249_validation": OUT / "P8_Y5_BRR545_2249_VALIDATION.csv",
    "2249_jr_components": OUT / "P8_Y5_PARENT_QLOC_2249_JR_COMPONENT_DECOMPOSITION.csv",
    "1043_doc": ROOT / "1043-Y5-R10-JX-zero-and-Phi-boundary-zero-premise-or-alpha3-prior-value.md",
    "1043_validation": OUT / "P8_Y5_BRR545_1043_VALIDATION.csv",
    "1044_doc": ROOT / "1044-Y5-R10-matter-pullback-JX-zero-or-qbarXT-bound-row.md",
    "1088_doc": ROOT / "1088-Y5-R10-minimal-parent-ordinary-matter-signature-clause-or-finite-coefficient-intake.md",
    "1344_doc": ROOT / "1344-Y5-R10-RAB-no-XR-vertex-theorem-or-retained-scalar-source-charge-row.md",
    "1720_functor": OUT / "P8_Y5_PARENT_QLOC_1720_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
    "1786_boundary": OUT / "P8_Y5_PARENT_QLOC_1786_BOUNDARY_MATTER_CLOSURE_GATE.csv",
    "2158_doc": ROOT / "2158-Y5-R2FR-JX-qbarXT-source-zero-or-bounded-coupling-component-pack.md",
    "2158_bounds": OUT / "P8_Y5_PARENT_QLOC_2158_BOUNDED_COUPLING_COMPONENT_PACK.csv",
    "2158_arenas": OUT / "P8_Y5_PARENT_QLOC_2158_ARENA_PROJECTION_ROWS.csv",
}

SOURCES = [
    ("SRC2297_00_2296_doc", "2296_q_nohair_handoff", PATHS["2296_doc"], ["conditional local q no-hair theorem", "J_q Source-Zero Audit", "JQ_SOURCE_ZERO_OR_COMPONENT_BOUND_PACK_NEXT"], "2296 identifies J_q as the next local-GR pressure point."),
    ("SRC2297_01_2296_validation", "2296_validation", PATHS["2296_validation"], ["VAL2296_OVERALL", "PASS"], "2296 validation passed."),
    ("SRC2297_02_2296_next", "2296_next_target", PATHS["2296_next"], ["2297-Y5-R2FR-Jq-source-zero-or-component-bound-pack.md", "prove J_q source silence"], "direct handoff to this checkpoint."),
    ("SRC2297_03_2296_jq_audit", "2296_jq_audit", PATHS["2296_jq_audit"], ["JQ2296_6_total_verdict", "JQ_TOTAL_ZERO_NOT_PROVED"], "J_q source-zero channels are open."),
    ("SRC2297_04_2296_nohair", "2296_q_nohair_identity", PATHS["2296_nohair"], ["NH2296_3_zero_theorem", "CONDITIONAL_THEOREM_PROVED_PREMISES_UNSIGNED"], "q no-hair identity needs J_q=0."),
    ("SRC2297_05_2249_doc", "2249_JR_precedent", PATHS["2249_doc"], ["ordinary-matter source-silence theorem", "body/source-worldtube charge", "concrete vector"], "R_AB source-zero/component-bound precedent."),
    ("SRC2297_06_2249_validation", "2249_validation", PATHS["2249_validation"], ["VAL2249_OVERALL", "PASS"], "2249 validation passed."),
    ("SRC2297_07_2249_components", "2249_component_shape", PATHS["2249_jr_components"], ["JRD2249_8_total_abs_guard", "ABS_ENVELOPE_SCHEMA_READY_VALUES_MISSING"], "source component no-cancellation shape."),
    ("SRC2297_08_1043_doc", "1043_JX_phi_precedent", PATHS["1043_doc"], ["J_X=0", "Phi_boundary_local"], "generic source-plus-boundary zero gate precedent."),
    ("SRC2297_09_1043_validation", "1043_validation", PATHS["1043_validation"], ["V1043_SUMMARY", "pass"], "1043 validation passed."),
    ("SRC2297_10_1044_doc", "1044_matter_pullback", PATHS["1044_doc"], ["ordinary-matter chain-rule route is now exact", "MPD1044_7_exact_theorem_if_signed"], "exact conditional ordinary-matter pullback theorem."),
    ("SRC2297_11_1088_doc", "1088_MOMS", PATHS["1088_doc"], ["MOMS1088_7_verdict", "THM1088_5_conclusion"], "minimal ordinary-matter signature contract."),
    ("SRC2297_12_1344_doc", "1344_body_charge", PATHS["1344_doc"], ["scalar source-charge law is now explicit", "Q_X[body]"], "body/source-worldtube charge warning and law."),
    ("SRC2297_13_1720_functor", "1720_matter_functor", PATHS["1720_functor"], ["MFS1720_0_parent_quotient_map", "MFS1720_8_verdict"], "matter functor signature remains unsigned."),
    ("SRC2297_14_1786_boundary", "1786_boundary_matter", PATHS["1786_boundary"], ["BMC1786_1_matter_interface", "BMC1786_5_verdict"], "boundary/matter closure remains open."),
    ("SRC2297_15_2158_doc", "2158_source_identity", PATHS["2158_doc"], ["JQD2158_7_total_abs_guard", "DEC2158_0_exact_identity"], "source-zero identity plus absolute component envelope."),
    ("SRC2297_16_2158_bounds", "2158_component_bounds", PATHS["2158_bounds"], ["BCP2158_10_total", "SCHEMA_READY_VALUES_MISSING"], "bounded coupling symbols for local arenas."),
    ("SRC2297_17_2158_arenas", "2158_arena_projection", PATHS["2158_arenas"], ["APR2158_5_local_GR", "BLOCKED_PENDING_SOURCE_SILENCE_OR_BOUNDS"], "arena projection contract if source silence fails."),
]

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2297_SOURCE_REGISTER.csv",
    "jq_zero_attempt": OUT / "P8_Y5_PARENT_QLOC_2297_JQ_ZERO_THEOREM_ATTEMPT.csv",
    "jq_component_decomposition": OUT / "P8_Y5_PARENT_QLOC_2297_JQ_COMPONENT_DECOMPOSITION.csv",
    "body_charge_law": OUT / "P8_Y5_PARENT_QLOC_2297_BODY_CHARGE_SOURCE_LAW.csv",
    "component_bound_template": OUT / "P8_Y5_PARENT_QLOC_2297_JQ_COMPONENT_BOUND_TEMPLATE.csv",
    "observable_projection": OUT / "P8_Y5_PARENT_QLOC_2297_OBSERVABLE_PROJECTION_LEDGER.csv",
    "acceptance_gate": OUT / "P8_Y5_PARENT_QLOC_2297_ACCEPTANCE_GATES.csv",
    "countermodels": OUT / "P8_Y5_PARENT_QLOC_2297_COUNTERMODEL_LEDGER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2297_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2297_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2297_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2297_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2297_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_jq_bounds": QUEUE / "JR2297_JQ_COMPONENT_BOUND_TEMPLATE_NONCLAIM.csv",
    "queue_body_charge": QUEUE / "JR2297_Q_BODY_CHARGE_SOURCE_LAW_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "q_Jq_source_bound_nonclaim_2297.csv",
    "beta_docs": BETA_DOCS / "Q_JQ_SOURCE_BOUND_2297_NONCLAIM.csv",
}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def contains_all(path: Path, needles: list[str]) -> bool:
    return path.exists() and all(needle in read_text(path) for needle in needles)


def validation_pass(path: Path) -> bool:
    if not path.exists():
        return False
    rows = read_csv(path)
    if not rows:
        return False
    id_key = "check_id" if "check_id" in rows[0] else "validation_id"
    result_key = "result" if "result" in rows[0] else "status"
    overall = [row for row in rows if "overall" in row.get(id_key, "").lower() or "summary" in row.get(id_key, "").lower()]
    check_rows = overall or rows
    return all(row.get(result_key, "").lower() == "pass" for row in check_rows)


def false_flags() -> dict[str, bool]:
    return {
        "theorem_zero": False,
        "numeric_value_present": False,
        "source_backed": False,
        "score_ready": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for source_id, source_key, path, needles, role in SOURCES:
        exists = path.exists()
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_id,
                "source_key": source_key,
                "source_path": rel(path),
                "exists": exists,
                "needles": ";".join(needles),
                "needles_present": contains_all(path, needles),
                "validation_overall_pass": validation_pass(path) if "validation" in source_key else "",
                "role": role,
                "valid_for_claim": False,
            }
        )
    return rows


def src(*keys: str) -> str:
    by_key = {source_key: path for _, source_key, path, _, _ in SOURCES}
    return ";".join(rel(by_key[key]) for key in keys)


def jq_zero_attempt_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "JZT2297_0_definition",
            "J_q total source in the candidate positive-q equation",
            "J_q := J_q^matter_bulk + J_q^curvature_vertex + J_q^body/worldtube + J_q^boundary + J_q^readout + J_q^history + J_q^projector + J_q^counterterm + J_q^constants",
            "A single vague coupling is replaced by a source vector that can be zero-proved componentwise or bounded in absolute value.",
            "DECOMPOSITION_WRITTEN_NOT_ZERO",
            "MISSING_COMPONENT_ZERO_OR_ABS_BOUNDS",
        ),
        (
            "JZT2297_1_ordinary_matter_chain_rule",
            "ordinary matter bulk source",
            "If S_matter depends on the parent fields only through quotient-owned observed geometry/gauge data, fixed representation constants, gauge/boundary matter lifts, and variation-before-readout, then delta_vq S_matter=0 and J_q^matter_bulk=0.",
            "This is an exact chain-rule theorem under the 1044/1088 MOMS contract, specialized to the q-sector vertical direction.",
            "EXACT_CONDITIONAL_THEOREM_PARENT_UNSIGNED",
            "MISSING_PARENT_MATTER_FUNCTOR_AND_NO_MARKER_SIGNATURE_FOR_Q",
        ),
        (
            "JZT2297_2_body_charge_warning",
            "body/interior source charge",
            "Even when J_q=0 in the exterior vacuum domain, a body/worldtube charge Q_q[body] can set exterior q boundary data through matching.",
            "Exterior source silence is not enough for local GR/Newton unless the body/source-worldtube charge is zero-proved or source-bounded.",
            "EXTERIOR_ZERO_INSUFFICIENT_BODY_CHARGE_OPEN",
            "MISSING_QQ_BODY_ZERO_OR_BOUND",
        ),
        (
            "JZT2297_3_nonbulk_tails",
            "boundary, history, readout, projector, constants and counterterm tails",
            "Each nonbulk channel must vanish in the same parent branch or enter an absolute no-cancellation envelope.",
            "No sign cancellation between source components can be used as evidence for local-GR reduction.",
            "TAIL_CHANNELS_OPEN",
            "MISSING_TAIL_ZERO_OR_BOUNDS",
        ),
        (
            "JZT2297_4_verdict",
            "J_q=0 theorem status",
            "J_q=0 is not proved by the current corpus; only the ordinary-matter conditional theorem and a q-sector component-bound pack are now assembled.",
            "The 2296 positive-q no-hair theorem remains conditional, and all local observables stay nonclaim.",
            "JQ_ZERO_NOT_PROVED_COMPONENT_BOUNDS_REQUIRED",
            "MISSING_PARENT_SIGNATURE_OR_SOURCE_BACKED_COMPONENTS",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": attempt_id,
            "target": target,
            "statement": statement,
            "result": result,
            "current_status": status,
            "missing_input": missing,
            "source_paths": src("2296_jq_audit", "1044_matter_pullback", "1088_MOMS", "1344_body_charge", "2158_source_identity"),
            **false_flags(),
        }
        for attempt_id, target, statement, result, status, missing in rows
    ]


def jq_component_decomposition_rows() -> list[dict[str, Any]]:
    components = [
        ("JQD2297_0_matter_bulk", "J_q_matter_bulk", "ordinary matter variation projected onto the q vertical direction", "zero if the MOMS ordinary-matter signature descends through quotient observables and q is vertical-trivial for observed matter", "MISSING_PARENT_MATTER_DESCENT_FOR_Q"),
        ("JQD2297_1_curvature_vertex", "J_q_curvature_vertex", "linear q-curvature or hidden-sector source vertex", "zero only if the parent object language forbids B_qR R_obs or equivalent q-curvature/source vertices", "MISSING_NO_Q_CURVATURE_VERTEX"),
        ("JQD2297_2_body_worldtube", "J_q_body_worldtube", "interior/source-worldtube charge that fixes exterior q boundary data", "zero if Q_q[body]=0 by source matching, symmetry, screening, compact support theorem, or parent charge law", "MISSING_QQ_BODY_ZERO_OR_BOUND"),
        ("JQD2297_3_boundary_edge", "J_q_boundary_edge", "edge, corner, reference, and boundary collar source term", "zero if no-flux/exact-boundary theorem covers the physical source boundary, not just compact proper transformations", "MISSING_PHYSICAL_Q_BOUNDARY_EDGE_RULE"),
        ("JQD2297_4_readout", "J_q_readout", "post-variation measured-G/source normalization or calibration re-entry", "zero if variation-before-readout and no-shadow-frame clauses are parent signed for source and test bodies", "MISSING_Q_READOUT_NO_REENTRY"),
        ("JQD2297_5_history", "J_q_history", "memory/history tail acting as an effective q source", "zero if compact-local stable kernel theorem excludes source-memory injection into the q sector", "MISSING_Q_HISTORY_KERNEL_ZERO_OR_BOUND"),
        ("JQD2297_6_projector_domain", "J_q_projector_domain", "projection/domain/constraint commutator leakage into q", "zero if source extraction, local projector, and q-reduced domain commute in the parent branch", "MISSING_Q_PROJECTOR_COMMUTATOR_ZERO"),
        ("JQD2297_7_counterterm_reference", "J_q_counterterm_reference", "reference/subtraction/counterterm source dependence", "zero if counterterms are fixed topological/reference constants before variation and carry no source support", "MISSING_Q_COUNTERTERM_SOURCE_RULE"),
        ("JQD2297_8_constants_labels", "J_q_constants_labels", "source/test material constants, clock standards, charges, or labels varying along q", "zero if constants are superselection data and no source/test marker lives in q", "MISSING_CONSTANT_SUPERSELECTION_FOR_Q"),
        ("JQD2297_9_total_abs_guard", "J_q_abs_total", "absolute no-cancellation envelope", "|J_q| <= sum_i |J_q_i| with every component theorem-zero or source-backed", "MISSING_COMPONENT_VALUES_AND_SOURCE_PATHS"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "component_id": component_id,
            "component": component,
            "meaning": meaning,
            "zero_or_bound_condition": condition,
            "current_status": "ABS_ENVELOPE_SCHEMA_READY_VALUES_MISSING" if component_id == "JQD2297_9_total_abs_guard" else "NOT_ZERO_PROVED",
            "missing_input": missing,
            "no_cancellation_policy": "component signs cannot be used to cancel; each source channel must be zero-proved or bounded in absolute value",
            "source_paths": src("2296_jq_audit", "2249_component_shape", "1044_matter_pullback", "1786_boundary_matter", "2158_component_bounds"),
            **false_flags(),
        }
        for component_id, component, meaning, condition, missing in components
    ]


def body_charge_law_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "law_id": "BCL2297_0_density",
            "object": "rho_q source density",
            "formula": "rho_q = B_qR R_obs + C_qT T + J_q_matter_bulk + J_q_readout + J_q_history + J_q_projector + J_q_counterterm + J_q_constants",
            "interpretation": "q local hair is sourced by body/interior and nonbulk channels unless every coefficient vanishes or is bounded.",
            "current_status": "SOURCE_DENSITY_TEMPLATE_NONCLAIM",
            "needed_inputs": "B_qR;C_qT;J_q_components;units;body measure;source paths",
            "source_paths": src("1344_body_charge", "2296_q_nohair_identity"),
            **false_flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "law_id": "BCL2297_1_body_charge",
            "object": "Q_q[body]",
            "formula": "Q_q[body] = int_body sqrt(gamma) W_q rho_q + Q_q_boundary",
            "interpretation": "The exterior q equation can be homogeneous while Q_q[body] fixes a nonzero exterior q profile.",
            "current_status": "BODY_CHARGE_TEMPLATE_NONCLAIM",
            "needed_inputs": "W_q;body model;screening/matching rule;Q_q_boundary;normalization",
            "source_paths": src("1344_body_charge", "2249_JR_precedent"),
            **false_flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "law_id": "BCL2297_2_exterior_profile",
            "object": "exterior q profile",
            "formula": "q(r) ~ Q_q[body] G_q(r;lambda_q,Z_q,domain) plus boundary/history/readout/projector tails",
            "interpretation": "A local-GR reduction needs Q_q[body]=0 or a sourced bound below the relevant arenas, not merely J_q=0 outside the body.",
            "current_status": "PROFILE_TEMPLATE_NONCLAIM",
            "needed_inputs": "lambda_q;Z_q;domain Green function;tail envelope;observable map",
            "source_paths": src("2296_q_nohair_identity", "2158_arena_projection"),
            **false_flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "law_id": "BCL2297_3_zero_switch",
            "object": "Q_q[body]=0 theorem",
            "formula": "Q_q[body]=0 iff B_qR=C_qT=J_q_components=Q_q_boundary=0 in the same parent branch, or the q direction is absent/constraint-only.",
            "interpretation": "This is the clean switch from the positive-q no-hair identity to derived local GR; it is not yet signed.",
            "current_status": "ZERO_SWITCH_REJECTED_UNTIL_PARENT_SIGNED",
            "needed_inputs": "parent no-source signature, first-class q removal, or body-charge bound rows",
            "source_paths": src("2296_q_nohair_identity", "1088_MOMS", "1344_body_charge"),
            **false_flags(),
        },
    ]


def component_bound_template_rows() -> list[dict[str, Any]]:
    bounds = [
        ("JBT2297_0_BqR", "B_qR", "q-curvature/source vertex", "|B_qR| <= theorem_zero_or_source_bound", "R10;PPN;local_GR"),
        ("JBT2297_1_CqT", "C_qT", "matter trace/source vertex into q", "|C_qT| <= theorem_zero_or_source_bound", "R10;WEP;PPN;orbital"),
        ("JBT2297_2_qbar_qT", "qbar_qT", "test/source matter response to q", "|qbar_qT| <= |qbar_geom|+|qbar_constants|+|qbar_marker|+|qbar_source_weight|+|qbar_nonH|", "R10;WEP;clock"),
        ("JBT2297_3_Qq_body", "Q_q_body", "body/worldtube source charge", "|Q_q_body| <= int_body abs(W_q rho_q)+|Q_q_boundary|", "R10;PPN;orbital;local_GR"),
        ("JBT2297_4_Qq_boundary", "Q_q_boundary", "boundary/edge/reference source charge", "|Q_q_boundary| <= |edge|+|corner|+|reference|+|support_tail|", "boundary;R10;orbital;alpha3"),
        ("JBT2297_5_Creadout_q", "C_readout_q", "post-variation readout/source-normalization tail", "|C_readout_q| <= theorem_zero_or_calibration_bound", "orbital;clock;PPN"),
        ("JBT2297_6_Khistory_q", "K_history_q", "history kernel source tail", "||K_history_q|| weighted by source support and decay envelope", "orbital;clock;local_GR;Gdot"),
        ("JBT2297_7_projector_q", "Delta_projector_q", "projector/constraint/domain commutator leakage", "||[Pi_source,P_q]|| or theorem-zero commutator", "PPN;local_GR;R10;alpha3"),
        ("JBT2297_8_Kct_q", "K_ct_q", "counterterm/reference source tail", "|K_ct_q| <= theorem_zero_or_reference_subtraction_bound", "R10;boundary;alpha3"),
        ("JBT2297_9_Cconstants_q", "C_constants_q", "constant/material-label q source", "|C_constants_q| <= theorem_zero_or_constant_sensitivity_bound", "clock;WEP;fine_structure;R10"),
        ("JBT2297_10_total_abs", "Jq_abs_envelope", "absolute no-cancellation total source/test coupling", "sum_abs_components in common q-source normalization", "all_local_arenas"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "symbol": symbol,
            "definition": definition,
            "formula_or_bound": formula,
            "current_status": "SCHEMA_READY_VALUES_MISSING" if row_id == "JBT2297_10_total_abs" else "MISSING_ZERO_THEOREM_OR_SOURCE_BOUND",
            "units": "declared_common_q_source_normalization_required",
            "source_path": src("2158_component_bounds", "1044_matter_pullback", "1344_body_charge"),
            "observable_link": observable,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for row_id, symbol, definition, formula, observable in bounds
    ]


def observable_projection_rows() -> list[dict[str, Any]]:
    rows = [
        ("OPL2297_0_R10", "R10 short-range", "alpha_q(lambda)=K_q(lambda) Qbar_qH(lambda) qbar_qT + body/boundary/history/readout/projector tails", "K_q;lambda_q;Qbar_qH;qbar_qT;Q_q_body;real alpha_bound(lambda);tail envelope", "MISSING_ARENA_PROJECTION"),
        ("OPL2297_1_PPN", "PPN/preferred-frame", "PPN_q_vec <= tau_PPN dot abs(B_qR,C_qT,Q_q_body,C_readout_q,Delta_projector_q,K_history_q)", "tau_PPN;source-normalized q coefficients;Solar-system profile;frame map", "MISSING_TAU_PPN_AND_COMPONENTS"),
        ("OPL2297_2_WEP", "WEP/source composition", "eta_AB <= tau_WEP dot abs(differential qbar_qT,C_constants_q,C_readout_q)", "material sensitivities;component bounds;same-frame source masses", "MISSING_WEP_COMPONENT_VECTOR"),
        ("OPL2297_3_clocks", "clocks/redshift/constants", "clock_q <= tau_clock dot abs(C_constants_q,C_readout_q,K_history_q)", "clock sensitivities;constant derivative bounds;readout rule", "MISSING_CLOCK_PROJECTION"),
        ("OPL2297_4_orbital", "orbital/source-support", "orbital_q <= tau_orbital dot abs(Q_q_body,Q_q_boundary,K_history_q,Creadout_q)", "worldtube support;source normalization;history kernel;screening rule", "MISSING_ORBITAL_PROJECTION"),
        ("OPL2297_5_alpha3", "preferred-frame alpha3/local anisotropy", "alpha3_q <= tau_alpha3 dot abs(Q_q_boundary,Delta_projector_q,Creadout_q,K_ct_q)", "alpha3 projection tensor;boundary/reference rule;domain map", "MISSING_ALPHA3_PROJECTION"),
        ("OPL2297_6_local_GR", "local GR/Newton", "derived only if 2296 no-hair activates, Q_q[body]=0, and observable projection tails vanish or are bounded below tests", "2296 nohair gates;2297 source gates;boundary/operator/first-class gates", "BLOCKED_PENDING_SOURCE_SILENCE_OR_BOUNDS"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "projection_id": projection_id,
            "arena": arena,
            "formula_or_contract": formula,
            "required_inputs": required,
            "current_status": status,
            "claim_effect": "no claim/no score",
            "source_paths": src("2158_arena_projection", "2296_q_nohair_identity", "1344_body_charge"),
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for projection_id, arena, formula, required, status in rows
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("AC2297_0_Jq_zero", "J_q=0 source theorem", "FAIL_PARENT_UNSIGNED_COMPONENTS", "ordinary matter chain-rule route is exact but unsigned; body/boundary/readout/history/projector/constants/counterterm components remain open"),
        ("AC2297_1_body_charge", "Q_q[body]=0 or bounded", "FAIL_BODY_CHARGE_INPUTS_MISSING", "exterior vacuum is insufficient without source-worldtube matching"),
        ("AC2297_2_component_bounds", "finite q component envelope", "SCHEMA_READY_VALUES_MISSING", "all symbolic component rows need source-backed values or theorem-zero certificates"),
        ("AC2297_3_no_cancellation", "no hidden cancellation credit", "POLICY_ACTIVE_NOT_SCORE", "absolute component envelope is required"),
        ("AC2297_4_local_GR_switch", "q source leg ready for no-hair/local-GR", "JQ_SOURCE_LEG_NOT_ZERO_AND_NOT_BOUNDED", "2297 improves the coupling contract but does not close the branch"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "gate": gate,
            "current_status": status,
            "reason": reason,
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate, status, reason in rows
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    rows = [
        ("CM2297_0_species_weight", "ordinary matter has source/species weight w_A(q)", "visible metric can descend while WEP/R10 qbar channels survive", "MOMS no-species-weight clause parent-signed"),
        ("CM2297_1_body_charge", "source body has Q_q[body] even with exterior J_q=0", "exterior q hair appears through boundary matching", "Q_q[body]=0 theorem or sourced body-charge bound"),
        ("CM2297_2_boundary_edge", "compact proper q transformations are silent but physical source boundary is not", "alpha3/R10 edge tails survive", "physical boundary/worldtube no-flux theorem"),
        ("CM2297_3_post_readout", "measured GM/source normalization re-enters after variation", "apparent fifth-force/PPN residual appears as readout tail", "variation-before-readout and no-shadow-source rule"),
        ("CM2297_4_history_memory", "memory/history kernel stores source support", "local exterior is not Markov/source-free in q", "compact-local kernel zero theorem or sourced kernel bound"),
        ("CM2297_5_projector_domain", "source projector and q local projector do not commute", "preferred-frame/domain residual survives", "projector commutator zero theorem or norm bound"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": countermodel_id,
            "countermodel": countermodel,
            "why_it_blocks_claim": why,
            "needed_to_kill": needed,
            "currently_killed": False,
            "valid_for_claim": False,
        }
        for countermodel_id, countermodel, why, needed in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CL2297_0_Jq_zero", "J_q=0 in local exterior and source matching", "BLOCKED", "JZT2297_4 verdict is JQ_ZERO_NOT_PROVED_COMPONENT_BOUNDS_REQUIRED"),
        ("CL2297_1_Qq_body", "Q_q[body]=0 or source-backed bound", "BLOCKED", "BCL2297 body charge rows are symbolic and nonclaim"),
        ("CL2297_2_abs_components", "all q source components zero or absolute-bound source-backed", "BLOCKED", "component values and theorem-zero certificates are missing"),
        ("CL2297_3_empirical_scores", "R10/PPN/WEP/clock/orbital/alpha3 score rows are runnable", "BLOCKED", "arena projections and component normalizations are missing"),
        ("CL2297_4_local_GR_Newton", "local GR/Newton reduction is derived", "BLOCKED", "source/body charge, operator sign/gap, boundary, first-class, and projection gates remain open"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": claim_id,
            "claim": claim,
            "current_status": status,
            "reason": reason,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for claim_id, claim, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2297_0_exact_contract", "JQ_SOURCE_ZERO_CONTRACT_SHARPENED", "ordinary matter source silence is an exact conditional chain-rule theorem, but q also needs body/worldtube, boundary, readout, history, projector, constants, and counterterm silence", "do not activate no-hair; fill or derive source components"),
        ("DEC2297_1_body_charge_repair", "EXTERIOR_VACUUM_NOT_ENOUGH", "Q_q[body] can source the exterior q profile even if J_q=0 away from the body", "promote body/source-worldtube charge to a first-class blocker"),
        ("DEC2297_2_no_cancellation", "ABSOLUTE_SOURCE_VECTOR_REQUIRED", "no hidden cancellation between source components, tails, or readout projections can be used to claim local GR", "every component must be theorem-zero or source-backed"),
        ("DEC2297_3_next", "PARENT_Q_MATTER_CURVATURE_SOURCE_SIGNATURE_OR_FIRST_BODY_CHARGE_ROW_NEXT", "the least-handwavy next route is either a parent no-source signature for q or a first sourced Q_q[body]/B_qR/C_qT row", "2298-Y5-R2FR-q-parent-matter-curvature-source-signature-or-first-body-charge-row.md"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "next_action": next_action,
            "valid_for_claim": False,
        }
        for decision_id, decision, rationale, next_action in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "NEXT2297_0_primary",
            "2298-Y5-R2FR-q-parent-matter-curvature-source-signature-or-first-body-charge-row.md",
            "scripts/Y5_R2FR_q_parent_matter_curvature_source_signature_or_first_body_charge_row_2298.py",
            "try to parent-sign the q ordinary-matter/curvature no-source signature; if unsigned, stage the first Q_q[body], B_qR, or C_qT source-charge row as nonclaim",
            "selected",
            "q source signature closes, or at least one body/source coefficient becomes theorem-zero/source-backed while all local claims remain blocked",
        ),
        (
            "NEXT2297_1_parallel_boundary",
            "2298b-Y5-R2FR-q-boundary-worldtube-charge-zero-or-tail-bound.md",
            "scripts/Y5_R2FR_q_boundary_worldtube_charge_zero_or_tail_bound_2298b.py",
            "prove q boundary/source-worldtube charge zero or emit Q_q_boundary/Phi_boundary tail bounds",
            "held_parallel",
            "boundary source charge theorem or nonclaim tail coefficient row",
        ),
        (
            "NEXT2297_2_parallel_firstclass",
            "2298c-Y5-R2FR-q-firstclass-source-marker-erasure-gate.md",
            "scripts/Y5_R2FR_q_firstclass_source_marker_erasure_gate_2298c.py",
            "test whether the first-class q route erases the same source/readout/material markers without finite source rows",
            "held_parallel",
            "first-class source marker erasure certificate or explicit failure ledger",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": route_id,
            "next_target": target,
            "script": script,
            "objective": objective,
            "priority": priority,
            "acceptance_output": acceptance,
            "valid_for_claim": False,
        }
        for route_id, target, script, objective, priority, acceptance in rows
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "copy_id": copy_id,
            "source_file": rel(source),
            "target_file": rel(target),
            "source_exists": source.exists(),
            "target_exists": target.exists(),
            "purpose": "q J_q source-bound nonclaim handoff",
        }
        for copy_id, source, target in [
            ("BC2297_queue_jq_bounds", OUTPUTS["component_bound_template"], COPY_TARGETS["queue_jq_bounds"]),
            ("BC2297_queue_body_charge", OUTPUTS["body_charge_law"], COPY_TARGETS["queue_body_charge"]),
            ("BC2297_branch_wep", OUTPUTS["component_bound_template"], COPY_TARGETS["branch_wep"]),
            ("BC2297_beta_docs", OUTPUTS["component_bound_template"], COPY_TARGETS["beta_docs"]),
        ]
    ]


def md_escape(value: Any) -> str:
    text = str(value)
    return text.replace("|", "\\|").replace("\n", " ")


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(sections: dict[str, list[dict[str, Any]]]) -> None:
    text = "\n\n".join(
        [
            "# 2297 - Y5/R2FR J_q Source-Zero or Component-Bound Pack",
            "## Summary\n\n2297 attacks the coupling/source leg directly. The ordinary-matter `J_q` silence route is a clean conditional chain-rule theorem, but it is not parent-signed for the current q branch. The body/worldtube charge repair is now explicit: exterior vacuum silence does not by itself prove local GR/Newton because `Q_q[body]` can set the exterior q profile through matching.\n\nThe result is a sharper fork, not a claim. Either the future parent action signs the q no-source signature, or the surviving coupling components must be filled as source-backed absolute bounds. No local-GR, Newton, R10, WEP, clock, orbital, PPN, alpha3, or public claim is allowed from this checkpoint.",
            "## Source Register\n\n" + md_table(sections["source_register"]),
            "## J_q Zero Theorem Attempt\n\n" + md_table(sections["jq_zero_attempt"]),
            "## J_q Component Decomposition\n\n" + md_table(sections["jq_component_decomposition"]),
            "## Body Charge Source Law\n\n" + md_table(sections["body_charge_law"]),
            "## Component Bound Template\n\n" + md_table(sections["component_bound_template"]),
            "## Observable Projection Ledger\n\n" + md_table(sections["observable_projection"]),
            "## Acceptance Gates\n\n" + md_table(sections["acceptance_gate"]),
            "## Countermodel Ledger\n\n" + md_table(sections["countermodels"]),
            "## Claim Gates\n\n" + md_table(sections["claim_gates"]),
            "## Decision Ledger\n\n" + md_table(sections["decision"]),
            "## Next Target\n\n" + md_table(sections["next_target"]),
            "## Branch Copies\n\n" + md_table(sections["branch_copies"]),
            "## Validation\n\n" + md_table(sections["validation"]),
            "## Plain-English Verdict\n\nThis is the coupling problem in its least slippery form so far. We have not proved `J_q=0`, but we have narrowed the hunt to an exact parent-action contract: ordinary matter must descend through quotient observables, constants must be q-trivial, source/readout/domain markers must be absent, and the body/worldtube charge must vanish or be bounded. That is the next hard strike, not another lap around the same tree.",
        ]
    )
    DOC.write_text(text + "\n", encoding="utf-8")


def parse_all_outputs(outputs: dict[str, Path]) -> bool:
    for path in outputs.values():
        if path.suffix.lower() == ".csv":
            rows = read_csv(path)
            if not rows:
                return False
    return True


def no_claims_true(rows_by_section: dict[str, list[dict[str, Any]]]) -> bool:
    for section, rows in rows_by_section.items():
        if section == "validation":
            continue
        for row in rows:
            for key, value in row.items():
                if key in {"valid_for_claim", "claim_allowed", "score_ready", "source_backed", "numeric_value_present", "theorem_zero"} and value is True:
                    return False
                if key in {"gate_pass", "currently_killed"} and value is True:
                    return False
    return True


def formalization_2297_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for path in FORMALIZATION.rglob("*2297*") if path.is_file())


def pycache_exists() -> bool:
    return any(path.name == "__pycache__" for path in (ROOT / "scripts").rglob("__pycache__"))


def build_validation_rows(sections: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = sections["source_register"]
    output_paths = {name: path for name, path in OUTPUTS.items() if name != "validation"}
    checks = [
        ("VAL2297_00_sources_exist", all(row["exists"] for row in source_rows), "all cited local source paths exist"),
        ("VAL2297_01_needles_present", all(row["needles_present"] for row in source_rows), "source register needles are present"),
        ("VAL2297_02_prior_validations_pass", all(row["validation_overall_pass"] in ("", True) for row in source_rows), "prior validation sources pass"),
        ("VAL2297_03_doc_written", DOC.exists() and "J_q Zero Theorem Attempt" in read_text(DOC), "checkpoint markdown written"),
        ("VAL2297_04_csv_parse", parse_all_outputs(output_paths), "all generated CSVs parse and contain rows"),
        ("VAL2297_05_no_claim_flags", no_claims_true(sections), "all generated theory rows remain nonclaim"),
        ("VAL2297_06_exact_conditional_theorem", any(row["current_status"] == "EXACT_CONDITIONAL_THEOREM_PARENT_UNSIGNED" for row in sections["jq_zero_attempt"]), "ordinary matter chain-rule theorem is present but unsigned"),
        ("VAL2297_07_Jq_zero_refused", any(row["current_status"] == "JQ_ZERO_NOT_PROVED_COMPONENT_BOUNDS_REQUIRED" for row in sections["jq_zero_attempt"]), "J_q=0 is not promoted"),
        ("VAL2297_08_body_charge_warning", any(row["object"] == "Q_q[body]" for row in sections["body_charge_law"]), "body/source-worldtube charge law is explicit"),
        ("VAL2297_09_abs_guard", any(row["component_id"] == "JQD2297_9_total_abs_guard" for row in sections["jq_component_decomposition"]), "absolute no-cancellation guard is present"),
        ("VAL2297_10_bounds_nonclaim", all(row["valid_for_claim"] is False for row in sections["component_bound_template"]), "component bound templates remain nonclaim"),
        ("VAL2297_11_projections_blocked", all(row["valid_for_claim"] is False and row["claim_allowed"] is False for row in sections["observable_projection"]), "observable projections remain blocked"),
        ("VAL2297_12_claim_gates_blocked", all(row["current_status"] == "BLOCKED" for row in sections["claim_gates"]), "claim gates remain blocked"),
        ("VAL2297_13_decision_next", any(row["decision"] == "PARENT_Q_MATTER_CURVATURE_SOURCE_SIGNATURE_OR_FIRST_BODY_CHARGE_ROW_NEXT" for row in sections["decision"]), "decision selects parent q source signature/body-charge row next"),
        ("VAL2297_14_branch_copies_exist", all(target.exists() for target in COPY_TARGETS.values()), "branch copy handoffs exist"),
        ("VAL2297_15_formalization_untouched", formalization_2297_count() == 0, "no 2297 files were written under formalization-workbench"),
        ("VAL2297_16_no_pycache", not pycache_exists(), "scripts __pycache__ removed"),
    ]
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2297_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "2297 sharpens J_q into source-zero/body-charge/component-bound contracts, refuses local claims, and selects parent q source signature or first body-charge row next",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def remove_pycache() -> None:
    for path in (ROOT / "scripts").rglob("__pycache__"):
        shutil.rmtree(path)


def main() -> None:
    for directory in (OUT, QUEUE, MICROSCOPE, BETA_DOCS):
        directory.mkdir(parents=True, exist_ok=True)

    sections = {
        "source_register": source_register_rows(),
        "jq_zero_attempt": jq_zero_attempt_rows(),
        "jq_component_decomposition": jq_component_decomposition_rows(),
        "body_charge_law": body_charge_law_rows(),
        "component_bound_template": component_bound_template_rows(),
        "observable_projection": observable_projection_rows(),
        "acceptance_gate": acceptance_gate_rows(),
        "countermodels": countermodel_rows(),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    for key, rows in sections.items():
        write_csv(OUTPUTS[key], rows)

    shutil.copyfile(OUTPUTS["component_bound_template"], COPY_TARGETS["queue_jq_bounds"])
    shutil.copyfile(OUTPUTS["body_charge_law"], COPY_TARGETS["queue_body_charge"])
    shutil.copyfile(OUTPUTS["component_bound_template"], COPY_TARGETS["branch_wep"])
    shutil.copyfile(OUTPUTS["component_bound_template"], COPY_TARGETS["beta_docs"])

    sections["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], sections["branch_copies"])

    sections["validation"] = [
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2297_PENDING",
            "result": "PENDING",
            "detail": "pre-validation document render",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]
    write_doc(sections)

    remove_pycache()
    sections["validation"] = build_validation_rows(sections)
    write_csv(OUTPUTS["validation"], sections["validation"])
    write_doc(sections)

    if sections["validation"][-1]["result"] != "PASS":
        raise SystemExit(f"2297 validation failed: {OUTPUTS['validation']}")
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

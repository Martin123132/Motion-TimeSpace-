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

BRANCH_ID = "MTS_R2FR_Q_SOURCE_SLOT_EXCLUSION_2299"
DOC = ROOT / "2299-Y5-R2FR-q-source-slot-exclusion-or-BqR-CqT-acquisition-ledger.md"

PATHS = {
    "2298_doc": ROOT / "2298-Y5-R2FR-q-parent-matter-curvature-source-signature-or-first-body-charge-row.md",
    "2298_validation": OUT / "P8_Y5_BRR545_2298_VALIDATION.csv",
    "2298_signature": OUT / "P8_Y5_PARENT_QLOC_2298_Q_SOURCE_SIGNATURE_ATTEMPT.csv",
    "2298_acquisition": OUT / "P8_Y5_PARENT_QLOC_2298_BQR_CQT_QQ_ACQUISITION_LEDGER.csv",
    "2298_next": OUT / "P8_Y5_PARENT_QLOC_2298_NEXT_TARGET.csv",
    "2297_bounds": OUT / "P8_Y5_PARENT_QLOC_2297_JQ_COMPONENT_BOUND_TEMPLATE.csv",
    "1761_doc": ROOT / "1761-Y5-R2FR-no-direct-matter-X-vertex-grammar-or-Amatter-coefficient-pack.md",
    "1761_csv": OUT / "P8_Y5_PARENT_QLOC_1761_NO_DIRECT_MATTER_X_VERTEX_GRAMMAR_ATTEMPT.csv",
    "1768_doc": ROOT / "1768-Y5-R2FR-parent-action-normal-form-and-source-map-identity-signature-or-shadow-coefficient-pack.md",
    "1720_functor": OUT / "P8_Y5_PARENT_QLOC_1720_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
    "1786_boundary": OUT / "P8_Y5_PARENT_QLOC_1786_BOUNDARY_MATTER_CLOSURE_GATE.csv",
    "1344_doc": ROOT / "1344-Y5-R10-RAB-no-XR-vertex-theorem-or-retained-scalar-source-charge-row.md",
    "2158_bounds": OUT / "P8_Y5_PARENT_QLOC_2158_BOUNDED_COUPLING_COMPONENT_PACK.csv",
    "2251_doc": ROOT / "2251-Y5-R2FR-RAB-source-slot-exclusion-or-BRR-CRT-acquisition-ledger.md",
    "2251_validation": OUT / "P8_Y5_BRR545_2251_VALIDATION.csv",
}

SOURCES = [
    ("SRC2299_00_2298_doc", "2298_handoff", PATHS["2298_doc"], ["DEC2298_2_next", "NEXT2298_0_primary"], "selects q source-slot exclusion or B_qR/C_qT acquisition as 2299 target"),
    ("SRC2299_01_2298_validation", "2298_validation", PATHS["2298_validation"], ["VAL2298_OVERALL", "PASS"], "confirms 2298 passed before 2299 starts"),
    ("SRC2299_02_2298_next", "2298_next", PATHS["2298_next"], ["2299-Y5-R2FR-q-source-slot-exclusion-or-BqR-CqT-acquisition-ledger.md", "B_qR/C_qT/Q_q/Pi_q"], "direct 2299 handoff"),
    ("SRC2299_03_2298_signature", "2298_signature", PATHS["2298_signature"], ["QSS2298_2_no_curvature_source_vertex", "MISSING_BQR_ZERO"], "records missing q curvature/source vertex theorem"),
    ("SRC2299_04_2298_acquisition", "2298_acquisition", PATHS["2298_acquisition"], ["ACQ2298_0_BqR", "ACQ2298_1_CqT", "ACQ2298_6_total"], "q source coefficient acquisition template to refine"),
    ("SRC2299_05_2297_bounds", "2297_bounds", PATHS["2297_bounds"], ["JBT2297_0_BqR", "JBT2297_10_total_abs"], "q component bound template and absolute envelope"),
    ("SRC2299_06_1761_doc", "1761_no_direct_vertex", PATHS["1761_doc"], ["NDV1761_4_current_verdict", "THEOREM_CONTRACT_READY_PARENT_UNSIGNED"], "no-direct-matter-vertex grammar attempt and source-prefactor countermodels"),
    ("SRC2299_07_1761_csv", "1761_no_vertex_csv", PATHS["1761_csv"], ["NDV1761_0_target", "NDV1761_4_current_verdict"], "machine-readable no-direct-vertex theorem status"),
    ("SRC2299_08_1768_doc", "1768_normal_form", PATHS["1768_doc"], ["ANF1768_6_current_verdict", "SCL1768_2_nonminimal_coupling"], "action normal-form owner rule and nonminimal-source classification"),
    ("SRC2299_09_1720_functor", "1720_functor", PATHS["1720_functor"], ["MFS1720_0_parent_quotient_map", "MFS1720_8_verdict"], "matter functor remains unsigned"),
    ("SRC2299_10_1786_boundary", "1786_boundary", PATHS["1786_boundary"], ["BMC1786_1_matter_interface", "BMC1786_5_verdict"], "boundary/matter closure remains open"),
    ("SRC2299_11_1344_doc", "1344_body_charge", PATHS["1344_doc"], ["VERT1344_3_body_charge", "QX1344_2_zero_switch"], "body charge warning and no-source/source-charge precedent"),
    ("SRC2299_12_2158_bounds", "2158_component_bounds", PATHS["2158_bounds"], ["BCP2158_10_total", "SCHEMA_READY_VALUES_MISSING"], "bounded coupling symbols for local arenas"),
    ("SRC2299_13_2251_doc", "2251_rab_precedent", PATHS["2251_doc"], ["RAB_SOURCE_SLOT_EXCLUSION_NOT_DERIVED", "MIXED_VERTEX_COUNTERMODEL_SURVIVES"], "R_AB source-slot exclusion precedent"),
    ("SRC2299_14_2251_validation", "2251_validation", PATHS["2251_validation"], ["VAL2251_OVERALL", "PASS"], "confirms 2251 passed"),
]

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2299_SOURCE_REGISTER.csv",
    "slot_exclusion": OUT / "P8_Y5_PARENT_QLOC_2299_Q_SOURCE_SLOT_EXCLUSION_ATTEMPT.csv",
    "countermodels": OUT / "P8_Y5_PARENT_QLOC_2299_COUNTERMODEL_LEDGER.csv",
    "acquisition": OUT / "P8_Y5_PARENT_QLOC_2299_BQR_CQT_QQ_ACQUISITION_LEDGER.csv",
    "runner_refusal": OUT / "P8_Y5_PARENT_QLOC_2299_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2299_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2299_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2299_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2299_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2299_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_coeffs": QUEUE / "JR2299_BQR_CQT_QQ_SOURCE_VECTOR_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "q_source_slot_BqR_CqT_Qq_nonclaim_2299.csv",
    "beta_docs": BETA_DOCS / "Q_SOURCE_SLOT_BQR_CQT_QQ_2299_NONCLAIM.csv",
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


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def validation_pass(path: Path) -> bool:
    if not path.exists():
        return False
    rows = read_csv(path)
    if not rows:
        return False
    id_key = "check_id" if "check_id" in rows[0] else "validation_id"
    result_key = "result" if "result" in rows[0] else "status"
    overall = [row for row in rows if "overall" in row.get(id_key, "").lower() or "summary" in row.get(id_key, "").lower()]
    return all(row.get(result_key, "").lower() == "pass" for row in (overall or rows))


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
        text = read_text(path) if exists else ""
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_id,
                "source_key": source_key,
                "source_path": rel(path),
                "exists": exists,
                "needles": ";".join(needles),
                "needles_present": exists and all(needle in text for needle in needles),
                "validation_overall_pass": validation_pass(path) if "validation" in source_key else "",
                "role": role,
                "valid_for_claim": False,
            }
        )
    return rows


def src(*keys: str) -> str:
    by_key = {source_key: path for _, source_key, path, _, _ in SOURCES}
    return ";".join(rel(by_key[key]) for key in keys)


def slot_exclusion_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "QSE2299_0_parent_object_language",
            "typed parent object language for q",
            "Allowed[S_parent] must decide before variation whether q is an LHS operator variable, a first-class/constrained auxiliary, or a legal matter/source argument.",
            "NEEDED_EXACTLY",
            "current corpus has contracts but no complete signed parent syntax",
            "MISSING_PARENT_OBJECT_LANGUAGE_SIGNATURE",
        ),
        (
            "QSE2299_1_no_direct_q_matter_slot",
            "ordinary matter has no independent q slot",
            "If S_matter = S_matter[Psi,e_obs(q_obs(Phi)),A_obs,theta] with no physical q argument, then delta S_matter/delta q=0 by chain rule.",
            "EXACT_CONDITIONAL_SUBTHEOREM",
            "works only after q is excluded from hidden frames, support functions, measured constants, material markers, and readout masks",
            "MISSING_NO_DIRECT_Q_SLOT_THEOREM",
        ),
        (
            "QSE2299_2_no_curvature_source_vertex",
            "curvature/source vertices vanish",
            "B_qR = delta^2 S_parent/(delta q delta R_obs)=0 and C_qT = delta^2 S_parent/(delta q delta T_H)=0 if no q R_obs, q T_H, or equivalent mixed source operator is legal.",
            "CONDITIONAL_VERTEX_ZERO",
            "normal-form owner rule classifies the term, but does not forbid it from the parent inventory",
            "MISSING_BQR_ZERO;MISSING_CQT_ZERO",
        ),
        (
            "QSE2299_3_no_source_only_scalar",
            "no inert q source scalar",
            "No sigma_source, w_A, W_source, domain marker, or active-source prefactor may multiply a q source channel while staying absent from nongravitational readout.",
            "CONTRACT_READY_UNSIGNED",
            "source-only Hom/action-scale owner remains unsigned",
            "MISSING_SOURCE_ONLY_SCALAR_EXCLUSION",
        ),
        (
            "QSE2299_4_action_scale_measure_owner",
            "action scale and measure are universal or observable-owned",
            "Any overall matter action multiplier is either a common calibrated constant or a measured matter-sector parameter, never an independent q source charge.",
            "NOT_PARENT_SIGNED",
            "classical field-normalization arguments do not remove action-scale/measure counterexamples",
            "MISSING_ACTION_SCALE_MEASURE_OWNER",
        ),
        (
            "QSE2299_5_boundary_worldtube_silence",
            "source-worldtube and boundary Pi_q slots are absent or bounded",
            "Q_q[body] and Pi_q vanish only if support, matching, boundary, and reference terms are all owned before variation or are separately bounded.",
            "NOT_PARENT_SIGNED",
            "exterior source-free proofs do not erase source-worldtube charge",
            "MISSING_QQ_BODY_ZERO;MISSING_PIQ_ZERO",
        ),
        (
            "QSE2299_6_firstclass_escape_clause",
            "first-class q removal could pre-empt source slots",
            "If q is proven pure gauge/constraint-only with matter descent and no boundary charge, all q source slots are absent from the reduced action.",
            "CONDITIONAL_ESCAPE_ROUTE_UNSIGNED",
            "first-class Omega/DCq/degree/matter package is not signed",
            "MISSING_Q_FIRSTCLASS_REMOVAL_CERTIFICATE",
        ),
        (
            "QSE2299_7_hidden_readout_projector_silence",
            "hidden/readout/history/projector/constant source tails are absent or bounded",
            "No post-variation readout, history kernel, projector commutator, counterterm, or variable-constant marker may reintroduce a q source component.",
            "NOT_PARENT_SIGNED",
            "2297/2298 keep these channels open",
            "MISSING_TAIL_ZERO_OR_BOUND",
        ),
        (
            "QSE2299_8_verdict",
            "q source-slot exclusion theorem",
            "QSE2299_0 through QSE2299_7 must close in the same parent branch before B_qR=C_qT=Q_q[body]=Pi_q=0 can be claimed.",
            "FAIL_CURRENT_CLAIM",
            "there is a simple covariant countermodel with B_qR, C_qT, or epsilon_q_source unless the object language forbids the slots",
            "Q_SOURCE_SLOT_EXCLUSION_NOT_DERIVED_CURRENT_CORPUS",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": attempt_id,
            "claim_piece": claim_piece,
            "mathematical_form": mathematical_form,
            "status": status,
            "current_evidence": evidence,
            "gap": gap,
            "source_paths": src("2298_handoff", "1761_no_direct_vertex", "1768_normal_form", "1720_functor", "1786_boundary", "2251_rab_precedent"),
            **false_flags(),
        }
        for attempt_id, claim_piece, mathematical_form, status, evidence, gap in rows
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CM2299_0_mixed_curvature_vertex",
            "Delta S = int sqrt(-g) (1/2 B_qR q R_obs)",
            "generally covariant mixed curvature/source operator can exist unless parent syntax forbids q R_obs",
            "B_qR remains a live acquisition coefficient",
            "parent no-mixed-curvature-vertex theorem or source-backed B_qR bound",
        ),
        (
            "CM2299_1_matter_trace_vertex",
            "Delta S = int sqrt(-g) C_qT q T_H",
            "Hilbert source ownership alone does not forbid a pre-action mixed q matter-trace vertex",
            "C_qT remains a live acquisition coefficient",
            "parent source-slot exclusion theorem or source-backed C_qT bound",
        ),
        (
            "CM2299_2_inert_source_scalar",
            "Delta S = int sqrt(-g) epsilon_q_source sigma_source q",
            "source-only scalar can produce a q channel without showing as a direct visible matter metric coupling",
            "epsilon_q_source remains live until source-only scalars are syntactically forbidden",
            "source-only scalar exclusion or numeric/source-backed prior width",
        ),
        (
            "CM2299_3_body_charge_matching",
            "q outside body = integral_body G_q rho_q dV + tails",
            "an exterior vacuum equation can still carry boundary data from Q_q[body]",
            "Q_q[body] remains a live local-GR/R10/PPN blocker",
            "body neutrality theorem or source-backed body-charge bound",
        ),
        (
            "CM2299_4_boundary_momentum",
            "Pi_q != 0 at source/support/boundary interface",
            "boundary/reference terms are not killed by ordinary-matter descent",
            "Pi_q remains a live boundary/acquisition coefficient",
            "Pi_q zero theorem or finite boundary momentum bound",
        ),
        (
            "CM2299_5_readout_history_projector_tail",
            "tail_q = C_readout_q + K_history_q + Delta_projector_q + C_constants_q",
            "post-variation readout/history/projector/constant channels can reintroduce q source dependence",
            "tail_q remains in the absolute source vector",
            "tail theorem-zero certificates or source-backed bounds",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": countermodel_id,
            "countermodel": countermodel,
            "why_it_survives": why,
            "residual_created": residual,
            "needed_to_kill": needed,
            "survives_current_corpus": True,
            "valid_for_claim": False,
        }
        for countermodel_id, countermodel, why, residual, needed in rows
    ]


def acquisition_rows() -> list[dict[str, Any]]:
    rows = [
        ("ACQ2299_0_BqR", "B_qR", "mixed q-observed-curvature vertex coefficient", "|B_qR| <= theorem_zero_or_source_backed_bound", "parent Hessian delta^2 S_parent/(delta q delta R_obs) and normalization to local arena basis", "MISSING_NO_VERTEX_THEOREM_OR_NUMERIC_BOUND", "R10;PPN;local_GR"),
        ("ACQ2299_1_CqT", "C_qT", "mixed q-Hilbert-source trace coefficient", "|C_qT| <= theorem_zero_or_source_backed_bound", "parent Hessian/source derivative delta^2 S_parent/(delta q delta T_H) in same matter frame", "MISSING_SOURCE_SLOT_EXCLUSION_OR_NUMERIC_BOUND", "R10;WEP;PPN;orbital"),
        ("ACQ2299_2_epsilon_q_source", "epsilon_q_source", "inert source-only q scalar/prior width", "|epsilon_q_source| <= theorem_zero_or_source_backed_prior_width", "source-only Hom/action-scale owner or explicit prior-width source", "MISSING_SOURCE_ONLY_SCALAR_ZERO_OR_WIDTH", "WEP;R10;PPN;clock"),
        ("ACQ2299_3_Qq_body", "Q_q_body", "body/source-worldtube reciprocal q charge", "|Q_q[body]| <= int_body abs(W_q rho_q) dV + |Q_q_boundary|", "body model, W_q, rho_q source density, Green function normalization, boundary term", "MISSING_BODY_NEUTRALITY_OR_NUMERIC_BODY_CHARGE", "R10;PPN;orbital;local_GR"),
        ("ACQ2299_4_Piq", "Pi_q", "boundary reciprocal momentum/source support term", "|Pi_q| <= theorem_zero_or_source_backed_boundary_bound", "boundary/support/reference variation and physical matching rule", "MISSING_PIQ_ZERO_OR_BOUND", "boundary;R10;PPN;orbital;alpha3"),
        ("ACQ2299_5_tail_source_vector", "tail_q", "readout/history/projector/counterterm/constant source-tail vector", "|tail_q| <= |C_readout_q| + ||K_history_q|| + ||Delta_projector_q|| + |C_counterterm_q| + |C_constants_q|", "variation-before-readout theorem or finite tail coefficient rows", "MISSING_TAIL_ZERO_OR_BOUNDS", "clock;orbital;PPN;local_GR;alpha3"),
        ("ACQ2299_6_total_abs", "q_source_vector_abs", "absolute no-cancellation source vector", "S_q_abs = |B_qR|+|C_qT|+|epsilon_q_source|+|Q_q_body|+|Pi_q|+|tail_q|", "all component theorem-zero certificates or numeric/source-backed bounds in common units", "SCHEMA_READY_VALUES_MISSING", "all_local_arenas"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "acquisition_id": acquisition_id,
            "symbol": symbol,
            "definition": definition,
            "formula_or_bound": formula,
            "required_source": required,
            "current_status": status,
            "observable_link": observable,
            "units_status": "MISSING_COMMON_Q_SOURCE_NORMALIZATION",
            "source_paths": src("2298_acquisition", "2297_bounds", "1768_normal_form", "1344_body_charge", "2158_component_bounds"),
            **false_flags(),
        }
        for acquisition_id, symbol, definition, formula, required, status, observable in rows
    ]


def runner_refusal_rows() -> list[dict[str, Any]]:
    rows = [
        ("REF2299_0_slot_exclusion", "q source-slot exclusion theorem", "BLOCKED", "QSE2299_8 verdict is FAIL_CURRENT_CLAIM"),
        ("REF2299_1_BqR_CqT_zero", "B_qR=C_qT=0 by theorem", "BLOCKED", "mixed curvature/source vertex countermodels survive"),
        ("REF2299_2_source_vector_values", "q source vector finite/source-backed", "BLOCKED", "acquisition rows are values-missing and common units missing"),
        ("REF2299_3_nohair_activation", "2296 q no-hair source side activates", "BLOCKED", "Q_q[body], Pi_q, and tails remain open"),
        ("REF2299_4_observable_scores", "R10/PPN/WEP/clock/orbital/alpha3 scoring", "BLOCKED", "B_qR/C_qT/Q_q/Pi_q/tail_q inputs remain symbolic"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "refusal_id": refusal_id,
            "attempted_claim": claim,
            "status": status,
            "reason": reason,
            "runner_allows_claim": False,
            "valid_for_claim": False,
        }
        for refusal_id, claim, status, reason in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2299_0_slot_exclusion", "q source-slot exclusion theorem", False, "QSE2299_8 fails"),
        ("CG2299_1_BqR_CqT", "B_qR and C_qT theorem-zero or source-backed", False, "mixed vertex coefficients remain missing"),
        ("CG2299_2_body_boundary", "Q_q[body] and Pi_q theorem-zero or source-backed", False, "body/boundary rows remain symbolic"),
        ("CG2299_3_tail_vector", "tail_q theorem-zero or source-backed", False, "readout/history/projector/constants remain open"),
        ("CG2299_4_common_units", "common q source normalization", False, "all acquisition rows need a shared normalization"),
        ("CG2299_5_local_GR_Newton", "derived local GR/Newton q reduction", False, "source slot exclusion and no-hair activation remain blocked"),
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
        ("DEC2299_0_theorem", "Q_SOURCE_SLOT_EXCLUSION_NOT_DERIVED", "A clean theorem exists if the parent object language forbids q source slots and mixed vertices, or proves q first-class/absent, but current corpus does not sign that object language.", "do not set B_qR=C_qT=Q_q[body]=Pi_q=0"),
        ("DEC2299_1_countermodel", "MIXED_Q_VERTEX_COUNTERMODEL_SURVIVES", "Delta S terms B_qR q R_obs and C_qT q T_H are not removed by covariance, Hilbert source ownership, or MOMS descent alone.", "force these terms into parent-action normal form with owner/forbid/bound labels"),
        ("DEC2299_2_acquisition", "BQR_CQT_QQ_PIQ_ACQUISITION_REFINED", "The source vector is now a concrete no-cancellation ledger with required Hessians, source normalization, body model, boundary momentum, and tail bounds.", "next classify each slot in a minimal parent action inventory"),
        ("DEC2299_3_next", "MINIMAL_PARENT_ACTION_Q_SOURCE_VECTOR_NORMAL_FORM_NEXT", "the least-handwavy next step is a parent action slot inventory for q: forbidden by syntax, LHS/operator-owned, boundary-owned, first-class removed, or finite residual", "2300-Y5-R2FR-minimal-parent-action-q-source-vector-normal-form-or-closure-declaration.md"),
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
            "NEXT2299_0_primary",
            "2300-Y5-R2FR-minimal-parent-action-q-source-vector-normal-form-or-closure-declaration.md",
            "scripts/Y5_R2FR_minimal_parent_action_q_source_vector_normal_form_or_closure_declaration_2300.py",
            "write the minimal parent action slot inventory for q and classify every source-looking term as forbidden by syntax, LHS operator-owned, boundary-owned, first-class removed, or finite residual; no zero claim unless the slot is actually absent in the same action",
            "selected",
            "each of B_qR, C_qT, epsilon_q_source, Q_q[body], Pi_q, and tail_q has a signed owner/forbid/bound status without cancellation credit",
        ),
        (
            "NEXT2299_1_fallback",
            "2300b-Y5-R2FR-BqR-CqT-source-vector-bound-runner.md",
            "scripts/Y5_R2FR_BqR_CqT_source_vector_bound_runner_2300b.py",
            "if the parent action slot inventory cannot be signed, build a refusal runner for numeric/source-backed bounds on B_qR, C_qT, epsilon_q_source, Q_q[body], Pi_q, and tail_q",
            "held_fallback",
            "runner refuses all rows with MISSING values and accepts only numeric, sourced, unit-matched residual bounds",
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
            "source_file": rel(OUTPUTS["acquisition"]),
            "target_file": rel(target),
            "source_exists": OUTPUTS["acquisition"].exists(),
            "target_exists": target.exists(),
            "purpose": purpose,
        }
        for copy_id, target, purpose in [
            ("BC2299_queue_coeffs", COPY_TARGETS["queue_coeffs"], "q B_qR/C_qT/Q_q/Pi_q source-vector nonclaim queue"),
            ("BC2299_branch_wep", COPY_TARGETS["branch_wep"], "q source-slot WEP/local residual nonclaim handoff"),
            ("BC2299_beta_docs", COPY_TARGETS["beta_docs"], "q source-slot beta-source nonclaim handoff"),
        ]
    ]


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def md_table(rows: list[dict[str, Any]]) -> str:
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
            "# 2299 - Y5/R2FR q Source-Slot Exclusion Or B_qR/C_qT Acquisition Ledger",
            "## Verdict\n\n2299 takes the derivation-first route and tries to prove that the parent object language forbids independent q source slots and mixed curvature/source vertices. The result is a useful rejection: the clean theorem is exact if the parent syntax is signed, or if q is first-class/absent in the reduced action, but the current corpus does not sign it. A covariant parent action can still contain `B_qR q R_obs`, `C_qT q T_H`, an inert source scalar, or body/boundary q source charge unless those slots are explicitly forbidden or bounded.\n\nSo no q source-zero/local-GR claim is allowed. The productive result is the refined acquisition ledger for `B_qR`, `C_qT`, `epsilon_q_source`, `Q_q[body]`, `Pi_q`, and `tail_q`, with absolute no-cancellation policy.",
            "## Source Register\n\n" + md_table(sections["source_register"]),
            "## q Source-Slot Exclusion Attempt\n\n" + md_table(sections["slot_exclusion"]),
            "## Countermodel Ledger\n\n" + md_table(sections["countermodels"]),
            "## B_qR/C_qT/Q_q Acquisition Ledger\n\n" + md_table(sections["acquisition"]),
            "## Refusal Runner\n\n" + md_table(sections["runner_refusal"]),
            "## Claim Gates\n\n" + md_table(sections["claim_gates"]),
            "## Decision Ledger\n\n" + md_table(sections["decision"]),
            "## Next Target\n\n" + md_table(sections["next_target"]),
            "## Branch Copies\n\n" + md_table(sections["branch_copies"]),
            "## Validation\n\n" + md_table(sections["validation"]),
            "## Working Interpretation\n\nThis is the coupling gap pinned to the wall. We do not get to say `q` decouples because ordinary matter descends; the parent action must either forbid every q source slot in one syntax, remove q as first-class, or carry a finite source vector into the tests. That is the right battlefield for the GR/Newton reduction.",
        ]
    )
    DOC.write_text(text + "\n", encoding="utf-8")


def read_all_outputs(outputs: dict[str, Path]) -> bool:
    for path in outputs.values():
        if path.suffix.lower() == ".csv" and path.exists():
            if not read_csv(path):
                return False
        elif not path.exists():
            return False
    return True


def no_claim_flags(sections: dict[str, list[dict[str, Any]]]) -> bool:
    for section, rows in sections.items():
        if section == "validation":
            continue
        for row in rows:
            for key, value in row.items():
                if key in {"valid_for_claim", "claim_allowed", "score_ready", "source_backed", "numeric_value_present", "theorem_zero", "runner_allows_claim"} and value is True:
                    return False
                if key == "gate_pass" and value is True:
                    return False
    return True


def formalization_2299_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for path in FORMALIZATION.rglob("*2299*") if path.is_file())


def pycache_exists() -> bool:
    return any(path.name == "__pycache__" for path in (ROOT / "scripts").rglob("__pycache__"))


def remove_pycache() -> None:
    for path in (ROOT / "scripts").rglob("__pycache__"):
        shutil.rmtree(path)


def validation_rows(sections: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = sections["source_register"]
    output_paths = {name: path for name, path in OUTPUTS.items() if name != "validation"}
    symbols = {row["symbol"] for row in sections["acquisition"]}
    checks = [
        ("VAL2299_00_sources_exist", all(row["exists"] for row in source_rows), "all cited local source paths exist"),
        ("VAL2299_01_needles_present", all(row["needles_present"] for row in source_rows), "source register needles are present"),
        ("VAL2299_02_prior_validations_pass", all(row["validation_overall_pass"] in ("", True) for row in source_rows), "prior validation sources pass"),
        ("VAL2299_03_doc_written", DOC.exists() and "q Source-Slot Exclusion Attempt" in read_text(DOC), "checkpoint markdown written"),
        ("VAL2299_04_csv_parse", read_all_outputs(output_paths), "all generated CSVs parse and contain rows"),
        ("VAL2299_05_no_claim_flags", no_claim_flags(sections), "all generated rows remain nonclaim"),
        ("VAL2299_06_slot_exclusion_refused", any(row["status"] == "FAIL_CURRENT_CLAIM" for row in sections["slot_exclusion"]), "q source-slot exclusion is not promoted"),
        ("VAL2299_07_countermodels_survive", all(row["survives_current_corpus"] is True for row in sections["countermodels"]), "mixed/source countermodels survive"),
        ("VAL2299_08_acquisition_symbols", all(symbol in symbols for symbol in ["B_qR", "C_qT", "epsilon_q_source", "Q_q_body", "Pi_q", "tail_q", "q_source_vector_abs"]), "all q source-vector symbols staged"),
        ("VAL2299_09_abs_guard", any(row["symbol"] == "q_source_vector_abs" and row["current_status"] == "SCHEMA_READY_VALUES_MISSING" for row in sections["acquisition"]), "absolute source-vector guard is present"),
        ("VAL2299_10_runner_refuses", all(row["status"] == "BLOCKED" for row in sections["runner_refusal"]), "refusal runner blocks all claims"),
        ("VAL2299_11_claim_gates_blocked", all(row["gate_pass"] is False for row in sections["claim_gates"]), "claim gates remain blocked"),
        ("VAL2299_12_next_target", any(row["next_target"] == "2300-Y5-R2FR-minimal-parent-action-q-source-vector-normal-form-or-closure-declaration.md" for row in sections["next_target"]), "next target selects minimal parent-action q source-vector normal form"),
        ("VAL2299_13_branch_copies_exist", all(target.exists() for target in COPY_TARGETS.values()), "branch copy handoffs exist"),
        ("VAL2299_14_formalization_untouched", formalization_2299_count() == 0, "no 2299 files were written under formalization-workbench"),
        ("VAL2299_15_no_pycache", not pycache_exists(), "scripts __pycache__ removed"),
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
            "check_id": "VAL2299_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "2299 rejects q source-slot exclusion from current premises, preserves mixed-vertex countermodels, stages B_qR/C_qT/Q_q/Pi_q acquisition, and selects minimal parent-action q source-vector normal form next",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def main() -> None:
    for directory in (OUT, QUEUE, MICROSCOPE, BETA_DOCS):
        directory.mkdir(parents=True, exist_ok=True)

    sections = {
        "source_register": source_register_rows(),
        "slot_exclusion": slot_exclusion_rows(),
        "countermodels": countermodel_rows(),
        "acquisition": acquisition_rows(),
        "runner_refusal": runner_refusal_rows(),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }
    for key, rows in sections.items():
        write_csv(OUTPUTS[key], rows)

    shutil.copyfile(OUTPUTS["acquisition"], COPY_TARGETS["queue_coeffs"])
    shutil.copyfile(OUTPUTS["acquisition"], COPY_TARGETS["branch_wep"])
    shutil.copyfile(OUTPUTS["acquisition"], COPY_TARGETS["beta_docs"])

    sections["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], sections["branch_copies"])

    sections["validation"] = [
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2299_PENDING",
            "result": "PENDING",
            "detail": "pre-validation document render",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]
    write_doc(sections)

    remove_pycache()
    sections["validation"] = validation_rows(sections)
    write_csv(OUTPUTS["validation"], sections["validation"])
    write_doc(sections)

    if sections["validation"][-1]["result"] != "PASS":
        raise SystemExit(f"2299 validation failed: {OUTPUTS['validation']}")
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

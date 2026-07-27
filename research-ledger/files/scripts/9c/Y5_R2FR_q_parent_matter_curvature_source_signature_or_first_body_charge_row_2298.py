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

BRANCH_ID = "MTS_R2FR_Q_SOURCE_SIGNATURE_2298"
DOC = ROOT / "2298-Y5-R2FR-q-parent-matter-curvature-source-signature-or-first-body-charge-row.md"

PATHS = {
    "2297_doc": ROOT / "2297-Y5-R2FR-Jq-source-zero-or-component-bound-pack.md",
    "2297_validation": OUT / "P8_Y5_BRR545_2297_VALIDATION.csv",
    "2297_body_law": OUT / "P8_Y5_PARENT_QLOC_2297_BODY_CHARGE_SOURCE_LAW.csv",
    "2297_bounds": OUT / "P8_Y5_PARENT_QLOC_2297_JQ_COMPONENT_BOUND_TEMPLATE.csv",
    "2297_next": OUT / "P8_Y5_PARENT_QLOC_2297_NEXT_TARGET.csv",
    "2296_nohair": OUT / "P8_Y5_PARENT_QLOC_2296_Q_CONDITIONAL_NOHAIR_IDENTITY.csv",
    "1088_doc": ROOT / "1088-Y5-R10-minimal-parent-ordinary-matter-signature-clause-or-finite-coefficient-intake.md",
    "1344_doc": ROOT / "1344-Y5-R10-RAB-no-XR-vertex-theorem-or-retained-scalar-source-charge-row.md",
    "1720_functor": OUT / "P8_Y5_PARENT_QLOC_1720_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
    "1786_boundary": OUT / "P8_Y5_PARENT_QLOC_1786_BOUNDARY_MATTER_CLOSURE_GATE.csv",
    "2158_doc": ROOT / "2158-Y5-R2FR-JX-qbarXT-source-zero-or-bounded-coupling-component-pack.md",
    "2158_bounds": OUT / "P8_Y5_PARENT_QLOC_2158_BOUNDED_COUPLING_COMPONENT_PACK.csv",
    "2250_doc": ROOT / "2250-Y5-R2FR-RAB-parent-matter-curvature-source-signature-or-first-body-charge-row.md",
    "2250_validation": OUT / "P8_Y5_BRR545_2250_VALIDATION.csv",
}

SOURCES = [
    ("SRC2298_00_2297_doc", "2297_handoff", PATHS["2297_doc"], ["DEC2297_3_next", "NEXT2297_0_primary"], "2297 selects parent q source signature or first body-charge row."),
    ("SRC2298_01_2297_validation", "2297_validation", PATHS["2297_validation"], ["VAL2297_OVERALL", "PASS"], "2297 validation passed."),
    ("SRC2298_02_2297_next", "2297_next", PATHS["2297_next"], ["2298-Y5-R2FR-q-parent-matter-curvature-source-signature-or-first-body-charge-row.md", "Q_q[body]"], "direct handoff to 2298."),
    ("SRC2298_03_2297_body_law", "2297_body_law", PATHS["2297_body_law"], ["BCL2297_3_zero_switch", "ZERO_SWITCH_REJECTED_UNTIL_PARENT_SIGNED"], "q body charge zero switch to be tested."),
    ("SRC2298_04_2297_bounds", "2297_bounds", PATHS["2297_bounds"], ["JBT2297_0_BqR", "JBT2297_1_CqT", "JBT2297_3_Qq_body"], "B_qR/C_qT/Q_q source coefficient templates."),
    ("SRC2298_05_2296_nohair", "2296_nohair", PATHS["2296_nohair"], ["NH2296_3_zero_theorem", "CONDITIONAL_THEOREM_PROVED_PREMISES_UNSIGNED"], "q no-hair theorem needing source closure."),
    ("SRC2298_06_1088_moms", "1088_moms", PATHS["1088_doc"], ["MOMS1088_7_verdict", "THM1088_5_conclusion"], "minimal ordinary-matter signature theorem contract."),
    ("SRC2298_07_1344_body_charge", "1344_body_charge", PATHS["1344_doc"], ["VERT1344_3_body_charge", "QX1344_2_zero_switch"], "body charge and no-source vertex warning."),
    ("SRC2298_08_1720_functor", "1720_functor", PATHS["1720_functor"], ["MFS1720_0_parent_quotient_map", "MFS1720_8_verdict"], "matter functor signature remains unsigned."),
    ("SRC2298_09_1786_boundary", "1786_boundary", PATHS["1786_boundary"], ["BMC1786_1_matter_interface", "BMC1786_5_verdict"], "boundary/matter closure remains open."),
    ("SRC2298_10_2158_doc", "2158_source_identity", PATHS["2158_doc"], ["JQD2158_7_total_abs_guard", "DEC2158_0_exact_identity"], "source-zero identity plus absolute component envelope."),
    ("SRC2298_11_2158_bounds", "2158_component_bounds", PATHS["2158_bounds"], ["BCP2158_10_total", "SCHEMA_READY_VALUES_MISSING"], "bounded coupling symbols for local arenas."),
    ("SRC2298_12_2250_doc", "2250_rab_precedent", PATHS["2250_doc"], ["FIRST_BODY_CHARGE_ROW_STAGED_NONCLAIM", "RAB_SOURCE_SLOT_EXCLUSION_OR_BRR_CRT_ACQUISITION_NEXT"], "R_AB source signature/body-charge precedent."),
    ("SRC2298_13_2250_validation", "2250_validation", PATHS["2250_validation"], ["VAL2250_OVERALL", "PASS"], "2250 validation passed."),
]

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2298_SOURCE_REGISTER.csv",
    "signature_attempt": OUT / "P8_Y5_PARENT_QLOC_2298_Q_SOURCE_SIGNATURE_ATTEMPT.csv",
    "no_source_theorem": OUT / "P8_Y5_PARENT_QLOC_2298_NO_SOURCE_THEOREM_GATE.csv",
    "first_body_charge_row": OUT / "P8_Y5_PARENT_QLOC_2298_FIRST_BODY_CHARGE_ROW.csv",
    "coefficient_acquisition": OUT / "P8_Y5_PARENT_QLOC_2298_BQR_CQT_QQ_ACQUISITION_LEDGER.csv",
    "runner_refusal": OUT / "P8_Y5_PARENT_QLOC_2298_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2298_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2298_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2298_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2298_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2298_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_body": QUEUE / "JR2298_Q_BODY_CHARGE_ROW_NONCLAIM.csv",
    "queue_coeffs": QUEUE / "JR2298_BQR_CQT_QQ_ACQUISITION_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "q_source_signature_body_charge_nonclaim_2298.csv",
    "beta_docs": BETA_DOCS / "Q_SOURCE_SIGNATURE_BODY_CHARGE_2298_NONCLAIM.csv",
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


def signature_attempt_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "QSS2298_0_parent_action_owner",
            "one parent action owns q, geometry, matter, boundary, and readout order before projection",
            "S_parent = S_geom[Phi,q,...] + S_matter[Psi,E(q_obs(Phi)),theta] + S_boundary, varied before empirical source/readout maps",
            "not supplied as a complete parent action in current corpus",
            "NOT_PARENT_SIGNED",
            "MISSING_PARENT_ACTION_OWNER",
        ),
        (
            "QSS2298_1_no_direct_q_matter_slot",
            "ordinary matter has no independent q argument",
            "partial S_matter / partial q = 0 because matter sees only quotient observed geometry/gauge data and fixed constants",
            "exact conditional MOMS route exists but direct q/source slots and source markers are not parent-excluded",
            "EXACT_CONDITIONAL_ROUTE_UNSIGNED",
            "MISSING_NO_DIRECT_Q_SOURCE_SLOT_THEOREM",
        ),
        (
            "QSS2298_2_no_curvature_source_vertex",
            "no q-curvature/source vertex",
            "B_qR := delta^2 S_parent/(delta q delta R_obs)=0 and C_qT := delta^2 S_parent/(delta q delta T)=0",
            "no-vertex theorem for q is not signed; nonminimal/source couplings remain legal countermodels",
            "NOT_PARENT_SIGNED",
            "MISSING_BQR_ZERO;MISSING_CQT_ZERO",
        ),
        (
            "QSS2298_3_source_worldtube_neutrality",
            "body/source-worldtube charge vanishes",
            "Q_q[body] = int_body sqrt(gamma) W_q rho_q + Q_q_boundary = 0",
            "exterior source silence does not prove this; Pi_q/boundary neutrality remains unsigned",
            "NOT_PARENT_SIGNED",
            "MISSING_QQ_BODY_ZERO;MISSING_PIQ_ZERO",
        ),
        (
            "QSS2298_4_boundary_reference_silence",
            "boundary/reference/counterterm source terms vanish or are bounded",
            "Q_q_boundary=0 and counterterm/reference variations are fixed before source extraction",
            "proper compact collar results do not cover physical source worldtubes",
            "NOT_PARENT_SIGNED",
            "MISSING_BOUNDARY_REFERENCE_SOURCE_RULE",
        ),
        (
            "QSS2298_5_projector_history_readout_silence",
            "projector, history, readout, and constant/source-label tails vanish",
            "Delta_projector_q=K_history_q=C_readout_q=C_constants_q=0 in the same parent branch",
            "2297 made these channels explicit but did not sign them",
            "NOT_PARENT_SIGNED",
            "MISSING_PROJECTOR_HISTORY_READOUT_CONSTANT_ZERO",
        ),
        (
            "QSS2298_6_verdict",
            "q parent matter/curvature no-source signature",
            "QSS2298_0 through QSS2298_5 pass in the same parent branch",
            "current corpus does not sign the source signature; retain body-charge and coefficient rows",
            "FAIL_CURRENT_CLAIM",
            "Q_SOURCE_SIGNATURE_NOT_PARENT_SIGNED",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "clause_id": clause_id,
            "clause": clause,
            "required_statement": required,
            "current_evidence": evidence,
            "current_status": status,
            "missing_for_claim": missing,
            "source_paths": src("2297_handoff", "1088_moms", "1344_body_charge", "1720_functor", "1786_boundary"),
            **false_flags(),
        }
        for clause_id, clause, required, evidence, status, missing in rows
    ]


def no_source_theorem_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "NST2298_0_conditional_theorem",
            "If the parent action has no direct q matter slot, B_qR=C_qT=0, Q_q[body]=0, Q_q_boundary=0, and readout/history/projector/constant tails vanish, then the source side of the 2296 q no-hair theorem closes.",
            "CONDITIONAL_THEOREM_WRITTEN_PREMISES_UNSIGNED",
            "NH2296_3 source premise and BCL2297_3 zero switch would pass, allowing positive q no-hair to be tested against operator/boundary/topology gates.",
            "QSS2298_6_verdict fails",
        ),
        (
            "NST2298_1_not_enough",
            "MOMS ordinary-matter pullback alone does not kill B_qR, C_qT, Q_q[body], Pi_q, boundary reference terms, q-constant markers, or a nonminimal q-curvature vertex.",
            "REPAIR_RULE_RECORDED",
            "prevents accidental promotion from ordinary-matter descent to full local-GR source neutrality",
            "body/curvature/readout/source terms remain live",
        ),
        (
            "NST2298_2_verdict",
            "No current q no-source theorem is claim-active.",
            "NO_SOURCE_THEOREM_NOT_ACTIVATED",
            "none yet; use finite body-charge/source-coefficient rows",
            "parent signature and source coefficients missing",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": theorem_id,
            "theorem": theorem,
            "status": status,
            "what_it_would_unlock": unlock,
            "current_blocker": blocker,
            **false_flags(),
        }
        for theorem_id, theorem, status, unlock, blocker in rows
    ]


def first_body_charge_rows() -> list[dict[str, Any]]:
    rows = [
        ("BCR2298_0_density", "rho_q", "rho_q = B_qR R_obs + C_qT T + J_q_matter_bulk + J_q_readout + J_q_history + J_q_projector + J_q_counterterm + J_q_constants", "source_density_units_required", "MISSING_BQR;MISSING_CQT;MISSING_COMPONENTS", "R10;PPN;WEP;clock;orbital;alpha3;local_GR"),
        ("BCR2298_1_body_charge", "Q_q_body", "Q_q[body] = int_body sqrt(gamma) W_q rho_q + Q_q_boundary", "q_charge_units_required", "MISSING_BODY_MODEL;MISSING_WQ;MISSING_QQ_BOUNDARY", "R10;PPN;orbital;local_GR"),
        ("BCR2298_2_exterior_profile", "q_profile", "q(x) = integral_body G_q(x,x') rho_q(x') dV' + boundary/history/readout/projector tails", "dimensionless_q_after_normalization", "MISSING_GREEN_FUNCTION;MISSING_ZQ;MISSING_MQ2;MISSING_DOMAIN", "R10;PPN;clock;orbital;alpha3"),
        ("BCR2298_3_zero_switch", "Q_q_body_zero", "Q_q[body]=0 iff B_qR=C_qT=J_q_components=Q_q_boundary=0 in the same signed parent branch, or q is first-class/absent", "theorem_zero_or_abs_bound", "MISSING_PARENT_SIGNATURE_OR_FIRSTCLASS_REMOVAL", "local_GR"),
        ("BCR2298_4_verdict", "first_q_body_charge_row", "first q body-charge row is staged as source-ready schema only; no numeric/source-backed value exists", "not_scoreable", "SOURCE_CHARGE_ROW_NONCLAIM_VALUES_MISSING", "all_local_arenas"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "symbol": symbol,
            "formula": formula,
            "units": units,
            "current_status": "ZERO_SWITCH_REJECTED_UNTIL_PARENT_SIGNED" if row_id == "BCR2298_3_zero_switch" else "NONCLAIM_SCHEMA_READY_VALUES_MISSING",
            "missing_inputs": missing,
            "observable_link": observable,
            "source_paths": src("2297_body_law", "1344_body_charge", "2297_bounds"),
            **false_flags(),
        }
        for row_id, symbol, formula, units, missing, observable in rows
    ]


def coefficient_acquisition_rows() -> list[dict[str, Any]]:
    rows = [
        ("ACQ2298_0_BqR", "B_qR", "q-curvature/source vertex coefficient", "MISSING_NO_VERTEX_THEOREM_OR_NUMERIC_BOUND", "R10;PPN;local_GR"),
        ("ACQ2298_1_CqT", "C_qT", "matter trace/source vertex into q", "MISSING_SOURCE_SLOT_EXCLUSION_OR_NUMERIC_BOUND", "R10;WEP;PPN;orbital"),
        ("ACQ2298_2_Qq_body", "Q_q_body", "source-worldtube/body reciprocal q charge", "MISSING_BODY_NEUTRALITY_OR_NUMERIC_BODY_CHARGE", "R10;PPN;orbital;local_GR"),
        ("ACQ2298_3_Pi_q", "Pi_q", "source/boundary momentum or normal-flux charge for q", "MISSING_BOUNDARY_NEUTRALITY_OR_FLUX_BOUND", "alpha3;R10;orbital"),
        ("ACQ2298_4_W_q", "W_q", "body/source weighting measure for q charge", "MISSING_BODY_MEASURE_AND_NORMALIZATION", "R10;PPN;orbital"),
        ("ACQ2298_5_Creadout_q", "C_readout_q", "post-variation source/readout calibration tail", "MISSING_READOUT_NO_REENTRY_OR_BOUND", "PPN;clock;orbital"),
        ("ACQ2298_6_total", "q_source_abs_vector", "absolute vector of B_qR,C_qT,Q_q_body,Pi_q,W_q,Creadout_q,history,projector,constants", "SCHEMA_READY_VALUES_MISSING", "all_local_arenas"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "acquisition_id": acquisition_id,
            "symbol": symbol,
            "definition": definition,
            "current_status": status,
            "units": "same_q_source_normalization_required",
            "observable_link": observable,
            "source_paths": src("2297_bounds", "2158_component_bounds", "2250_rab_precedent"),
            "priority": "first_row" if acquisition_id in {"ACQ2298_0_BqR", "ACQ2298_1_CqT", "ACQ2298_2_Qq_body"} else "supporting",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for acquisition_id, symbol, definition, status, observable in rows
    ]


def runner_refusal_rows() -> list[dict[str, Any]]:
    rows = [
        ("REF2298_0_q_no_source", "q no-source theorem", "BLOCKED", "QSS2298_6 source signature fails"),
        ("REF2298_1_Qq_body_zero", "Q_q[body]=0 theorem", "BLOCKED", "BCR2298_3 zero switch remains unsigned"),
        ("REF2298_2_first_row_numeric", "first q source row numeric/source-backed", "BLOCKED", "ACQ2298 first-row coefficients values missing"),
        ("REF2298_3_local_GR", "local GR/Newton from q branch", "BLOCKED", "source, operator, boundary, first-class, and projection gates are all not simultaneously signed"),
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
        ("CG2298_0_parent_signature", "q parent no-source signature", False, "QSS2298_6=FAIL_CURRENT_CLAIM"),
        ("CG2298_1_body_charge", "Q_q[body]=0 or source-backed finite value", False, "BCR2298 rows are symbolic/nonclaim"),
        ("CG2298_2_source_vector", "B_qR/C_qT/Q_q/Pi_q source vector score-ready", False, "ACQ2298_6 values missing"),
        ("CG2298_3_local_observables", "R10/PPN/WEP/clock/orbital/alpha3 runnable scores", False, "projection and normalization inputs missing"),
        ("CG2298_4_local_GR_Newton", "derived local GR/Newton q reduction", False, "source closure is not enough and is not closed"),
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
        ("DEC2298_0_derivation_attempt", "Q_NO_SOURCE_SIGNATURE_NOT_SIGNED", "MOMS kills only ordinary-matter pullback; it does not kill q-curvature vertices, body charge, boundary flux, readout, constants, history, or projector tails", "do not claim q source silence"),
        ("DEC2298_1_first_row", "FIRST_Q_BODY_CHARGE_ROW_STAGED_NONCLAIM", "Q_q[body], B_qR, C_qT, Pi_q, W_q and the absolute source vector are now explicit acquisition targets with units/arena links, but no values", "try source-slot exclusion before hunting arbitrary coefficients"),
        ("DEC2298_2_next", "Q_SOURCE_SLOT_EXCLUSION_OR_BQR_CQT_ACQUISITION_NEXT", "the least-scrutiny route is a parent grammar theorem forbidding direct q/source-only slots; fallback is source-backed B_qR/C_qT/Q_q/Pi_q acquisition", "2299-Y5-R2FR-q-source-slot-exclusion-or-BqR-CqT-acquisition-ledger.md"),
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
        ("NEXT2298_0_primary", "2299-Y5-R2FR-q-source-slot-exclusion-or-BqR-CqT-acquisition-ledger.md", "scripts/Y5_R2FR_q_source_slot_exclusion_or_BqR_CqT_acquisition_ledger_2299.py", "derive a parent grammar theorem forbidding direct q/source-only slots; if unsigned, stage source-backed B_qR/C_qT/Q_q/Pi_q acquisition rows", "selected", "q source-slot exclusion theorem or first coefficient acquisition row"),
        ("NEXT2298_1_parallel_boundary", "2299b-Y5-R2FR-q-Piq-boundary-neutrality-or-Qq-bound-row.md", "scripts/Y5_R2FR_q_Piq_boundary_neutrality_or_Qq_bound_row_2299b.py", "derive Pi_q=0 boundary/source neutrality or stage finite Q_q/Pi_q boundary-charge rows", "held_parallel", "Pi_q theorem-zero or source-backed finite boundary momentum row"),
        ("NEXT2298_2_parallel_firstclass", "2299c-Y5-R2FR-q-firstclass-removal-vs-source-row-decision.md", "scripts/Y5_R2FR_q_firstclass_removal_vs_source_row_decision_2299c.py", "decide whether first-class q removal can pre-empt finite source coefficient acquisition", "held_parallel", "first-class route prioritized or explicit source-row path retained"),
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
    pairs = [
        ("BC2298_queue_body", OUTPUTS["first_body_charge_row"], COPY_TARGETS["queue_body"], "q first body-charge nonclaim queue"),
        ("BC2298_queue_coeffs", OUTPUTS["coefficient_acquisition"], COPY_TARGETS["queue_coeffs"], "B_qR/C_qT/Q_q/Pi_q acquisition nonclaim queue"),
        ("BC2298_branch_wep", OUTPUTS["first_body_charge_row"], COPY_TARGETS["branch_wep"], "q source signature WEP/local residual nonclaim handoff"),
        ("BC2298_beta_docs", OUTPUTS["coefficient_acquisition"], COPY_TARGETS["beta_docs"], "q source signature beta-source nonclaim handoff"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "copy_id": copy_id,
            "source_file": rel(source),
            "target_file": rel(target),
            "source_exists": source.exists(),
            "target_exists": target.exists(),
            "purpose": purpose,
        }
        for copy_id, source, target, purpose in pairs
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
            "# 2298 - Y5/R2FR q Parent Matter/Curvature Source Signature Or First Body-Charge Row",
            "## Verdict\n\n2298 tries the clean derivation first. The result is negative but useful: the ordinary-matter MOMS pullback is not enough to sign the full q source side. A complete parent source signature would also need no direct q matter slot, no `B_qR q R_obs` or `C_qT q T` vertex, `Q_q[body]=0`, `Pi_q=0`, and boundary/reference/readout/history/projector/constant silence in the same parent branch.\n\nThose clauses are not signed, so the q source side remains nonclaim. The win is that the first body-charge/source-coefficient row is now explicit rather than fog: `rho_q`, `Q_q[body]`, `B_qR`, `C_qT`, `Pi_q`, `W_q`, and the absolute source vector are acquisition targets.",
            "## Source Register\n\n" + md_table(sections["source_register"]),
            "## q Source Signature Attempt\n\n" + md_table(sections["signature_attempt"]),
            "## No-Source Theorem Gate\n\n" + md_table(sections["no_source_theorem"]),
            "## First Body-Charge Row\n\n" + md_table(sections["first_body_charge_row"]),
            "## Coefficient Acquisition Ledger\n\n" + md_table(sections["coefficient_acquisition"]),
            "## Refusal Runner\n\n" + md_table(sections["runner_refusal"]),
            "## Claim Gates\n\n" + md_table(sections["claim_gates"]),
            "## Decision Ledger\n\n" + md_table(sections["decision"]),
            "## Next Target\n\n" + md_table(sections["next_target"]),
            "## Branch Copies\n\n" + md_table(sections["branch_copies"]),
            "## Validation\n\n" + md_table(sections["validation"]),
            "## Working Interpretation\n\nThis is not a retreat; it is the right kind of narrowing. The source side is no longer a mystical coupling. It is a grammar problem first: forbid direct q/source-only slots in the parent action, or admit finite source coefficients and make them face R10, PPN, WEP, clocks, orbital systems, alpha3, and local-GR residual gates.",
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


def formalization_2298_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for path in FORMALIZATION.rglob("*2298*") if path.is_file())


def pycache_exists() -> bool:
    return any(path.name == "__pycache__" for path in (ROOT / "scripts").rglob("__pycache__"))


def remove_pycache() -> None:
    for path in (ROOT / "scripts").rglob("__pycache__"):
        shutil.rmtree(path)


def validation_rows(sections: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = sections["source_register"]
    output_paths = {name: path for name, path in OUTPUTS.items() if name != "validation"}
    checks = [
        ("VAL2298_00_sources_exist", all(row["exists"] for row in source_rows), "all cited local source paths exist"),
        ("VAL2298_01_needles_present", all(row["needles_present"] for row in source_rows), "source register needles are present"),
        ("VAL2298_02_prior_validations_pass", all(row["validation_overall_pass"] in ("", True) for row in source_rows), "prior validation sources pass"),
        ("VAL2298_03_doc_written", DOC.exists() and "q Source Signature Attempt" in read_text(DOC), "checkpoint markdown written"),
        ("VAL2298_04_csv_parse", read_all_outputs(output_paths), "all generated CSVs parse and contain rows"),
        ("VAL2298_05_no_claim_flags", no_claim_flags(sections), "all generated rows remain nonclaim"),
        ("VAL2298_06_signature_refused", any(row["current_status"] == "FAIL_CURRENT_CLAIM" for row in sections["signature_attempt"]), "q no-source signature is not promoted"),
        ("VAL2298_07_moms_not_enough", any(row["theorem_id"] == "NST2298_1_not_enough" for row in sections["no_source_theorem"]), "MOMS-alone repair rule recorded"),
        ("VAL2298_08_body_charge_row", any(row["symbol"] == "Q_q_body" for row in sections["first_body_charge_row"]), "Q_q body-charge row is explicit"),
        ("VAL2298_09_first_coefficients", all(symbol in {row["symbol"] for row in sections["coefficient_acquisition"]} for symbol in ["B_qR", "C_qT", "Q_q_body", "Pi_q"]), "first source coefficients are acquisition targets"),
        ("VAL2298_10_runner_refuses", all(row["status"] == "BLOCKED" for row in sections["runner_refusal"]), "refusal runner blocks all claims"),
        ("VAL2298_11_claim_gates_blocked", all(row["gate_pass"] is False for row in sections["claim_gates"]), "claim gates remain blocked"),
        ("VAL2298_12_next_target", any(row["next_target"] == "2299-Y5-R2FR-q-source-slot-exclusion-or-BqR-CqT-acquisition-ledger.md" for row in sections["next_target"]), "next target selects source-slot exclusion or acquisition"),
        ("VAL2298_13_branch_copies_exist", all(target.exists() for target in COPY_TARGETS.values()), "branch copy handoffs exist"),
        ("VAL2298_14_formalization_untouched", formalization_2298_count() == 0, "no 2298 files were written under formalization-workbench"),
        ("VAL2298_15_no_pycache", not pycache_exists(), "scripts __pycache__ removed"),
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
            "check_id": "VAL2298_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "2298 refuses the q source signature, stages first body-charge/source-coefficient rows, and selects source-slot exclusion or acquisition next",
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
        "signature_attempt": signature_attempt_rows(),
        "no_source_theorem": no_source_theorem_rows(),
        "first_body_charge_row": first_body_charge_rows(),
        "coefficient_acquisition": coefficient_acquisition_rows(),
        "runner_refusal": runner_refusal_rows(),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }
    for key, rows in sections.items():
        write_csv(OUTPUTS[key], rows)

    shutil.copyfile(OUTPUTS["first_body_charge_row"], COPY_TARGETS["queue_body"])
    shutil.copyfile(OUTPUTS["coefficient_acquisition"], COPY_TARGETS["queue_coeffs"])
    shutil.copyfile(OUTPUTS["first_body_charge_row"], COPY_TARGETS["branch_wep"])
    shutil.copyfile(OUTPUTS["coefficient_acquisition"], COPY_TARGETS["beta_docs"])

    sections["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], sections["branch_copies"])

    sections["validation"] = [
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2298_PENDING",
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
        raise SystemExit(f"2298 validation failed: {OUTPUTS['validation']}")
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

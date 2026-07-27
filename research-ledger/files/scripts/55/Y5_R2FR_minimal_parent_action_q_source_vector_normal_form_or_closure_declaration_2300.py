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

BRANCH_ID = "MTS_R2FR_Q_MINIMAL_PARENT_SLOT_NORMAL_FORM_2300"
DOC = ROOT / "2300-Y5-R2FR-minimal-parent-action-q-source-vector-normal-form-or-closure-declaration.md"

PATHS = {
    "2299_doc": ROOT / "2299-Y5-R2FR-q-source-slot-exclusion-or-BqR-CqT-acquisition-ledger.md",
    "2299_validation": OUT / "P8_Y5_BRR545_2299_VALIDATION.csv",
    "2299_acquisition": OUT / "P8_Y5_PARENT_QLOC_2299_BQR_CQT_QQ_ACQUISITION_LEDGER.csv",
    "2299_countermodels": OUT / "P8_Y5_PARENT_QLOC_2299_COUNTERMODEL_LEDGER.csv",
    "2299_slot_exclusion": OUT / "P8_Y5_PARENT_QLOC_2299_Q_SOURCE_SLOT_EXCLUSION_ATTEMPT.csv",
    "2296_nohair": OUT / "P8_Y5_PARENT_QLOC_2296_Q_CONDITIONAL_NOHAIR_IDENTITY.csv",
    "2296_firstclass": OUT / "P8_Y5_PARENT_QLOC_2296_FIRSTCLASS_OWNER_GATE.csv",
    "2297_body": OUT / "P8_Y5_PARENT_QLOC_2297_BODY_CHARGE_SOURCE_LAW.csv",
    "2298_signature": OUT / "P8_Y5_PARENT_QLOC_2298_Q_SOURCE_SIGNATURE_ATTEMPT.csv",
    "1768_doc": ROOT / "1768-Y5-R2FR-parent-action-normal-form-and-source-map-identity-signature-or-shadow-coefficient-pack.md",
    "1786_boundary": OUT / "P8_Y5_PARENT_QLOC_1786_BOUNDARY_MATTER_CLOSURE_GATE.csv",
    "2158_bounds": OUT / "P8_Y5_PARENT_QLOC_2158_BOUNDED_COUPLING_COMPONENT_PACK.csv",
    "2252_doc": ROOT / "2252-Y5-R2FR-minimal-parent-action-RAB-source-vector-normal-form-or-closure-declaration.md",
    "2252_validation": OUT / "P8_Y5_BRR545_2252_VALIDATION.csv",
}

SOURCES = [
    ("SRC2300_00_2299_doc", "2299_handoff", PATHS["2299_doc"], ["DEC2299_3_next", "NEXT2299_0_primary"], "selects minimal parent-action q source-vector normal form"),
    ("SRC2300_01_2299_validation", "2299_validation", PATHS["2299_validation"], ["VAL2299_OVERALL", "PASS"], "confirms 2299 passed before 2300 starts"),
    ("SRC2300_02_2299_acquisition", "2299_acquisition", PATHS["2299_acquisition"], ["ACQ2299_0_BqR", "ACQ2299_6_total_abs"], "incoming q source-vector components for normal-form ownership"),
    ("SRC2300_03_2299_countermodels", "2299_countermodels", PATHS["2299_countermodels"], ["CM2299_0_mixed_curvature_vertex", "CM2299_1_matter_trace_vertex"], "mixed q-vertex countermodels that normal form must classify"),
    ("SRC2300_04_2299_slot_exclusion", "2299_slot_exclusion", PATHS["2299_slot_exclusion"], ["QSE2299_8_verdict", "Q_SOURCE_SLOT_EXCLUSION_NOT_DERIVED_CURRENT_CORPUS"], "q source-slot exclusion failure"),
    ("SRC2300_05_2296_nohair", "2296_nohair", PATHS["2296_nohair"], ["NH2296_3_zero_theorem", "NH2296_4_firstclass_alternative"], "conditional positive q no-hair and first-class alternative"),
    ("SRC2300_06_2296_firstclass", "2296_firstclass", PATHS["2296_firstclass"], ["FC2296_7_verdict", "FAIL_CURRENT_CLAIM_FIRSTCLASS_NOT_PROVED"], "q first-class removal package remains unsigned"),
    ("SRC2300_07_2297_body", "2297_body", PATHS["2297_body"], ["BCL2297_1_body_charge", "BCL2297_3_zero_switch"], "q body-charge and zero-switch precedent"),
    ("SRC2300_08_2298_signature", "2298_signature", PATHS["2298_signature"], ["QSS2298_6_verdict", "FAIL_CURRENT_CLAIM"], "q parent source-signature failure"),
    ("SRC2300_09_1768_doc", "1768_normal_form", PATHS["1768_doc"], ["ANF1768_1_geometry_left_hand_owner", "SCL1768_2_nonminimal_coupling"], "parent action owner rule and nonminimal-term classification precedent"),
    ("SRC2300_10_1786_boundary", "1786_boundary", PATHS["1786_boundary"], ["BMC1786_1_matter_interface", "BMC1786_5_verdict"], "boundary/source support closure remains open"),
    ("SRC2300_11_2158_bounds", "2158_component_bounds", PATHS["2158_bounds"], ["BCP2158_10_total", "SCHEMA_READY_VALUES_MISSING"], "bounded coupling symbols for local arenas"),
    ("SRC2300_12_2252_doc", "2252_rab_precedent", PATHS["2252_doc"], ["SOURCE_VECTOR_NORMAL_FORM_WRITTEN", "WEYL_MIXING_IS_THE_LOCAL_GR_DANGER"], "R_AB source-vector normal-form precedent"),
    ("SRC2300_13_2252_validation", "2252_validation", PATHS["2252_validation"], ["VAL2252_OVERALL", "PASS"], "confirms 2252 passed"),
]

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2300_SOURCE_REGISTER.csv",
    "slot_inventory": OUT / "P8_Y5_PARENT_QLOC_2300_PARENT_ACTION_Q_SLOT_INVENTORY.csv",
    "euler_map": OUT / "P8_Y5_PARENT_QLOC_2300_Q_EULER_SOURCE_VECTOR_NORMAL_FORM.csv",
    "closure_gate": OUT / "P8_Y5_PARENT_QLOC_2300_Q_CLOSURE_DECLARATION_GATE.csv",
    "firstclass_contract": OUT / "P8_Y5_PARENT_QLOC_2300_Q_FIRSTCLASS_REMOVAL_CONTRACT.csv",
    "residuals": OUT / "P8_Y5_PARENT_QLOC_2300_Q_RESIDUAL_ACQUISITION_ROWS.csv",
    "runner_refusal": OUT / "P8_Y5_PARENT_QLOC_2300_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2300_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2300_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2300_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2300_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2300_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_slots": QUEUE / "JR2300_Q_PARENT_ACTION_SLOT_INVENTORY_NONCLAIM.csv",
    "queue_residuals": QUEUE / "JR2300_Q_SOURCE_VECTOR_RESIDUALS_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "q_parent_slot_normal_form_nonclaim_2300.csv",
    "beta_docs": BETA_DOCS / "Q_PARENT_SLOT_NORMAL_FORM_2300_NONCLAIM.csv",
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


def slot_inventory_rows() -> list[dict[str, Any]]:
    rows = [
        ("QSLOT2300_0_EH_GR", "S_EH[e_obs]", "Einstein-Hilbert/GR left-hand geometry owner", "LHS_GEOMETRY_OWNER_REQUIRED", "allowed_required", "must reduce to Einstein operator and Newton/Poisson limit before local-GR claim", "MISSING_FULL_GR_LHS_DERIVATION"),
        ("QSLOT2300_1_q_diag", "1/2 <q, L_q q>", "diagonal q operator with Z_q, M_q^2, gauge/domain and boundary form", "LHS_Q_OPERATOR_OWNER", "allowed_conditional", "2296 no-hair can use this only if positivity, source-free domain, zero modes, and boundary conditions are signed", "MISSING_SIGNED_POSITIVE_Q_OPERATOR_AND_BOUNDARY"),
        ("QSLOT2300_2_q_constraint", "lambda_q C_q or first-class q generator", "constraint/first-class route that removes q from the reduced phase space", "FIRSTCLASS_REMOVAL_ROUTE", "allowed_conditional", "would delete q source slots after reduction, but Omega/DCq/brackets/degree count/matter descent are unsigned", "MISSING_Q_FIRSTCLASS_REMOVAL_CERTIFICATE"),
        ("QSLOT2300_3_BqRic_geometry_mix", "<q, B_qRic R_Ricci>", "q mixing with Ricci/Einstein curvature", "LHS_GEOMETRY_MIXING_OR_RESIDUAL", "must_diagonalize_or_bound", "Ricci mixing may be vacuum-silent outside matter only after curvature-basis split and coupled-operator positivity", "MISSING_Q_RICCI_SPLIT_AND_DIAGONALIZATION"),
        ("QSLOT2300_4_BqWeyl_geometry_mix", "<q, B_qW C_Weyl>", "q mixing with Weyl/tidal curvature", "DANGEROUS_GEOMETRY_RESIDUAL", "must_forbid_or_bound", "Weyl curvature is nonzero in Schwarzschild exterior, so this threatens local GR even when T_H=0", "MISSING_Q_WEYL_COUPLING_ZERO_OR_BOUND"),
        ("QSLOT2300_5_CqT_trace", "<q, C_qT T_H>", "mixed q-Hilbert matter trace/source term", "NONMINIMAL_MATTER_SOURCE_RESIDUAL", "must_forbid_or_bound", "Hilbert source ownership does not remove pre-action nonminimal q-matter coupling", "MISSING_CQT_ZERO_OR_BOUND"),
        ("QSLOT2300_6_epsilon_source_scalar", "epsilon_q_source sigma_source q", "inert/source-only q scalar", "FORBIDDEN_IF_PARENT_HOM_SIGNED_ELSE_RESIDUAL", "must_forbid_or_bound", "action-scale and no-source-only Hom remain unsigned", "MISSING_SOURCE_ONLY_Q_SCALAR_EXCLUSION"),
        ("QSLOT2300_7_body_worldtube", "Q_q[body] matching/source support term", "body/interior worldtube charge fixing exterior q data", "BODY_SOURCE_RESIDUAL", "must_zero_or_bound", "exterior vacuum equation is insufficient without source-worldtube neutrality", "MISSING_QQ_BODY_ZERO_OR_BOUND"),
        ("QSLOT2300_8_boundary_Piq", "Pi_q boundary/reference/support momentum", "boundary/source reciprocal q momentum", "BOUNDARY_OWNER_OR_RESIDUAL", "must_zero_or_bound", "physical boundary/reference terms are not signed silent", "MISSING_PIQ_ZERO_OR_BOUND"),
        ("QSLOT2300_9_tail_q", "C_readout_q + K_history_q + Delta_projector_q + C_counterterm_q + C_constants_q", "readout/history/projector/counterterm/constant source-tail vector", "TAIL_RESIDUAL", "must_zero_or_bound", "post-variation, kernel, projector, or material-label tails remain open", "MISSING_TAIL_Q_ZERO_OR_BOUND"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "slot_id": slot_id,
            "action_slot": action_slot,
            "meaning": meaning,
            "normal_form_owner": owner,
            "slot_status": slot_status,
            "classification_result": result,
            "missing_for_closure": missing,
            "source_paths": src("2299_handoff", "2296_nohair", "2296_firstclass", "1768_normal_form", "2252_rab_precedent"),
            **false_flags(),
        }
        for slot_id, action_slot, meaning, owner, slot_status, result, missing in rows
    ]


def euler_map_rows() -> list[dict[str, Any]]:
    rows = [
        ("QEUL2300_0_q_equation", "E_q := L_q q + B_qRic R_Ricci + B_qW C_Weyl + C_qT T_H + epsilon_q_source sigma_source + Q_q_body delta_body + Pi_q delta_boundary + tail_q = 0", "full q Euler normal form", "NORMAL_FORM_WRITTEN_NONCLAIM", "all source-looking q channels are explicit"),
        ("QEUL2300_1_firstclass_escape", "q absent from reduced action if Omega_flat(v_q)=delta C_q, brackets close, degree count removes q, and matter/boundary descend", "first-class removal owner", "CONDITIONAL_ESCAPE_ROUTE_UNSIGNED", "this would beat finite coupling rows, but the canonical package is not signed"),
        ("QEUL2300_2_lhs_operator_block", "[E_GR, E_q]^T = [[L_GR, B_qRic^T], [B_qRic, L_q]] [h, q]^T + B_qW C_Weyl + source_residuals", "coupled GR/q operator owner", "OPERATOR_OWNED_NOT_ZERO", "B_qRic can be LHS mixing only after curvature split, gauge fixing, and positivity/diagonalization"),
        ("QEUL2300_3_residual_source_vector", "J_q_res := B_qW C_Weyl + C_qT T_H + epsilon_q_source sigma_source + Q_q_body delta_body + Pi_q delta_boundary + tail_q", "absolute residual source vector", "RESIDUAL_VECTOR_NONCLAIM", "no cancellation allowed; every component must be zero-proved or bounded"),
        ("QEUL2300_4_local_vacuum_condition", "J_q_res=0 in the exterior requires B_qW=0/bounded, C_qT T_H=0 outside matter, epsilon=0, Q_q_body=0, Pi_q=0, tail_q=0", "local exterior source-free condition", "CONDITIONAL_REQUIREMENT", "Ricci-only mixing may vanish in GR vacuum, but Weyl/body/boundary/readout tails do not vanish automatically"),
        ("QEUL2300_5_nohair_activation", "2296 positive q identity activates only after L_eff positive and J_q_res plus boundary data vanish, or q is first-class absent", "no-hair bridge condition", "NOT_ACTIVATED", "operator positivity, residual-source closure, first-class removal, and projection gates are open"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "map_id": map_id,
            "formula": formula,
            "role": role,
            "current_status": status,
            "interpretation": interpretation,
            "source_paths": src("2296_nohair", "2299_acquisition", "1768_normal_form", "2252_rab_precedent"),
            **false_flags(),
        }
        for map_id, formula, role, status, interpretation in rows
    ]


def closure_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("QCLOSE2300_0_firstclass_removed", "q is first-class/constraint removed", "open", "Omega/DCq/bracket/degree/matter/boundary package is unsigned", False),
        ("QCLOSE2300_1_direct_source_slot", "ordinary/direct q source slot absent", "partly classified", "minimal visible matter excludes q only conditionally; source scalar, constants, readout, and nonminimal slots remain", False),
        ("QCLOSE2300_2_operator_positive", "L_q or L_eff is positive/coercive", "open", "Z_q/M_q^2/gauge/domain/zero-mode and mixed-operator positivity are not signed", False),
        ("QCLOSE2300_3_ricci_mix_owner", "B_qRic geometry mixing is LHS-owned", "conditional partial progress", "owner is plausible in normal form, but positivity/diagonalization and Ricci/Weyl split are unsigned", False),
        ("QCLOSE2300_4_weyl_mix_zero", "B_qW=0 or source-backed bound", "open", "Weyl/tidal curvature does not vanish in local vacuum and is not excluded", False),
        ("QCLOSE2300_5_matter_trace", "C_qT=0 or source-backed bound", "open", "pre-action nonminimal q matter-trace coupling remains legal", False),
        ("QCLOSE2300_6_body_boundary_tails", "Q_q[body]=Pi_q=tail_q=0 or bounded", "open", "body matching, physical boundary, and readout/history/projector/constant tails are not signed silent", False),
        ("QCLOSE2300_7_verdict", "local q source closure", "FAIL_CURRENT_CLAIM", "normal form clarifies ownership but does not close the full residual vector or first-class escape", False),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "closure_clause": clause,
            "status": status,
            "reason": reason,
            "gate_pass": gate_pass,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, clause, status, reason, gate_pass in rows
    ]


def firstclass_contract_rows() -> list[dict[str, Any]]:
    rows = [
        ("QFC2300_0_parent_Omega", "Omega_Y includes q, geometry, matter, boundary, and source/readout variables", "MISSING_PARENT_OMEGA", "without full phase-space form q cannot be declared gauge"),
        ("QFC2300_1_generator", "Omega_flat(v_q)=delta C_q plus differentiable boundary generator", "MISSING_MOMENTUM_MAP", "no first-class removal without a parent-owned generator"),
        ("QFC2300_2_brackets", "{G_q[epsilon],G_q[eta]} closes with zero/proper boundary term", "MISSING_BRACKET_CLOSURE", "an anomaly or second-class edge mode leaves q physical"),
        ("QFC2300_3_degree_count", "constraints remove the q canonical pair from reduced phase space", "MISSING_DEGREE_COUNT", "absence of a pole cannot be inferred without counting"),
        ("QFC2300_4_matter_descent", "matter/readout/constants descend to quotient with no q marker", "MISSING_MATTER_DESCENT", "source markers can survive even if bulk q is constrained"),
        ("QFC2300_5_boundary_charge", "Q_q[body], Pi_q, and boundary/reference q charges are zero/proper", "MISSING_BOUNDARY_SOURCE_NEUTRALITY", "physical source-worldtube can carry q boundary data"),
        ("QFC2300_6_verdict", "q first-class removal closes all q source slots", "FAIL_CURRENT_CLAIM_FIRSTCLASS_NOT_PROVED", "keep finite residual vector live until QFC2300_0 through QFC2300_5 close together"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "contract_id": contract_id,
            "needed_clause": clause,
            "current_status": status,
            "if_missing": if_missing,
            "source_paths": src("2296_nohair", "2296_firstclass", "2299_slot_exclusion"),
            **false_flags(),
        }
        for contract_id, clause, status, if_missing in rows
    ]


def residual_rows() -> list[dict[str, Any]]:
    rows = [
        ("QRES2300_0_BqWeyl", "B_qWeyl", "q-Weyl/tidal curvature mixing coefficient", "|B_qWeyl| <= zero_or_bound", "MISSING_Q_WEYL_COUPLING_ZERO_OR_BOUND", "PPN;orbital;local_GR;alpha3"),
        ("QRES2300_1_BqRic", "B_qRic", "q-Ricci/Einstein geometric mixing coefficient", "operator_owned_if_diagonalized_else |B_qRic| bound", "MISSING_Q_RICCI_DIAGONALIZATION_OR_BOUND", "local_GR;R10"),
        ("QRES2300_2_CqT", "C_qT", "q-Hilbert trace coupling", "|C_qT| <= zero_or_bound", "MISSING_CQT_ZERO_OR_BOUND", "WEP;PPN;R10;orbital"),
        ("QRES2300_3_epsilon", "epsilon_q_source", "inert source-only q scalar", "|epsilon_q_source| <= zero_or_prior_width", "MISSING_SOURCE_ONLY_Q_SCALAR_ZERO_OR_WIDTH", "WEP;R10;clock"),
        ("QRES2300_4_Qq_body", "Q_q_body", "body/source-worldtube q charge", "|Q_q_body| <= body integral plus boundary", "MISSING_BODY_CHARGE_ZERO_OR_BOUND", "R10;PPN;orbital;local_GR"),
        ("QRES2300_5_Piq", "Pi_q", "boundary reciprocal q momentum", "|Pi_q| <= boundary zero_or_bound", "MISSING_PIQ_ZERO_OR_BOUND", "R10;PPN;orbital;alpha3"),
        ("QRES2300_6_tail_q", "tail_q", "readout/history/projector/counterterm/constant source tail", "|tail_q| <= tail envelope", "MISSING_TAIL_Q_ZERO_OR_BOUND", "clock;orbital;PPN;alpha3"),
        ("QRES2300_7_firstclass_blocker", "q_firstclass_certificate", "certificate that q is absent from reduced action", "Omega/DCq/bracket/degree/matter/boundary all signed", "MISSING_Q_FIRSTCLASS_REMOVAL_CERTIFICATE", "all_local_arenas"),
        ("QRES2300_8_total", "q_residual_abs", "absolute residual vector after owner classification", "abs(B_qWeyl)+abs(C_qT)+abs(epsilon)+abs(Q_q_body)+abs(Pi_q)+abs(tail_q) plus B_qRic if not diagonalized; zero if first-class removed", "SCHEMA_READY_VALUES_MISSING", "all_local_arenas"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "residual_id": residual_id,
            "symbol": symbol,
            "meaning": meaning,
            "formula_or_bound": formula,
            "current_status": status,
            "observable_link": observable,
            "units_status": "MISSING_COMMON_Q_OPERATOR_NORMALIZATION",
            "source_paths": src("2299_acquisition", "2297_body", "2298_signature", "1786_boundary", "2158_component_bounds"),
            **false_flags(),
        }
        for residual_id, symbol, meaning, formula, status, observable in rows
    ]


def runner_refusal_rows() -> list[dict[str, Any]]:
    rows = [
        ("REF2300_0_closure", "q source vector closed", "BLOCKED", "QCLOSE2300_7_verdict=FAIL_CURRENT_CLAIM"),
        ("REF2300_1_firstclass", "q first-class removed", "BLOCKED", "QFC2300_6 verdict is not proved"),
        ("REF2300_2_BqRic_owner", "B_qRic safely moved to LHS", "BLOCKED", "diagonalization and Ricci/Weyl split unsigned"),
        ("REF2300_3_BqWeyl_zero", "Weyl/tidal q mixing absent", "BLOCKED", "B_qWeyl zero/bound missing"),
        ("REF2300_4_nohair", "2296 q no-hair activates", "BLOCKED", "L_eff positivity, first-class removal, and residual vector closure missing"),
        ("REF2300_5_local_GR", "derived local GR/Newton q branch", "BLOCKED", "GR LHS, q operator/source vector, boundary, projection, and empirical gates remain open"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "refusal_id": refusal_id,
            "attempted_claim": attempted_claim,
            "runner_result": result,
            "blocked_by": blocked_by,
            "score_eligible": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for refusal_id, attempted_claim, result, blocked_by in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2300_0_parent_slots", "complete parent-action q slot inventory is signed", "slot inventory is written but not parent-signed"),
        ("CG2300_1_firstclass", "q is removed as first-class/constraint", "canonical removal package is unsigned"),
        ("CG2300_2_operator_positive", "q or coupled GR/q operator is positive/coercive", "Z_q/M_q^2/gauge/domain/diagonalization are missing"),
        ("CG2300_3_geometric_diagonalization", "geometry mixing is safely LHS-owned", "Ricci/Weyl split and Schur/operator-norm diagonalization missing"),
        ("CG2300_4_residual_source", "non-geometric residual vector is zero or bounded", "B_qWeyl/C_qT/epsilon/Q_q/Pi_q/tail values missing"),
        ("CG2300_5_nohair", "positive q no-hair local branch activates", "source-free and boundary conditions not met"),
        ("CG2300_6_local_GR_Newton", "local GR/Newton reduction is derived", "operator/source/boundary/projection gates remain blocked"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": claim_id,
            "claim": claim,
            "gate_pass": False,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for claim_id, claim, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2300_0_gain",
            "decision": "Q_SOURCE_VECTOR_NORMAL_FORM_WRITTEN",
            "reason": "q coupling is no longer one vague coefficient: first-class removal, diagonal q operator, Ricci mixing, Weyl/tidal mixing, direct matter trace coupling, source scalar, body charge, boundary momentum, and tails are separated.",
            "next_action": "use the split to target either first-class removal or the dangerous Weyl/source residuals",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2300_1_firstclass",
            "decision": "FIRSTCLASS_ROUTE_IS_CLEANEST_IF_SIGNED",
            "reason": "If q is absent from the reduced action, source coefficients disappear without fitting; but the Omega/DCq/bracket/degree/matter/boundary package is not signed.",
            "next_action": "carry first-class clauses as a parallel zero route, not as a claim",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2300_2_guard",
            "decision": "Q_WEYL_MIXING_IS_THE_LOCAL_GR_DANGER",
            "reason": "Ricci terms can be vacuum-silent in a GR exterior, but Weyl/tidal curvature remains outside the source and would generate a q residual unless zeroed or bounded.",
            "next_action": "split B_qR into B_qRic and B_qWeyl from parent curvature basis",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2300_3_next",
            "decision": "Q_FIRSTCLASS_OR_RICCI_WEYL_SPLIT_NEXT",
            "reason": "The least-circular leap toward derived local GR is now binary: prove q is first-class absent, or prove the dangerous Weyl/source vector is zero/bounded and Ricci mixing is a positive LHS deformation.",
            "next_action": "2301-Y5-R2FR-q-firstclass-removal-or-Ricci-Weyl-source-vector-split.md",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2300_0_primary",
            "next_target": "2301-Y5-R2FR-q-firstclass-removal-or-Ricci-Weyl-source-vector-split.md",
            "script": "scripts/Y5_R2FR_q_firstclass_removal_or_Ricci_Weyl_source_vector_split_2301.py",
            "objective": "try first-class q removal first; if unsigned, derive the parent curvature basis split B_qR R_obs = B_qRic R_Ricci + B_qW C_Weyl, then prove B_qW=0/bounded and establish Schur/positive diagonalization for B_qRic before any no-hair activation",
            "selection_status": "selected",
            "success_condition": "q is first-class absent, or B_qWeyl is theorem-zero/source-backed bounded and Ricci mixing is diagonalized into a positive L_eff or retained as a finite residual",
            "forbidden_shortcuts": "calling q absent without Omega/DCq; calling all curvature Ricci; ignoring Weyl outside matter; moving B_qRic to LHS without positivity; local-GR/R10/PPN claim; GitHub action; formalization-workbench edit",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2300_1_fallback",
            "next_target": "2301b-Y5-R2FR-q-local-source-vector-bound-runner.md",
            "script": "scripts/Y5_R2FR_q_local_source_vector_bound_runner_2301b.py",
            "objective": "if first-class removal and Ricci/Weyl split cannot be derived, build numeric/source-backed bound rows for B_qRic, B_qWeyl, C_qT, epsilon_q_source, Q_q_body, Pi_q, and tail_q",
            "selection_status": "held_fallback",
            "success_condition": "runner refuses all rows with MISSING values and accepts only numeric, sourced, unit-matched local residual bounds",
            "forbidden_shortcuts": "zero priors by taste; tau=1; cancellation between residual components",
            "valid_for_claim": False,
        },
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
            "purpose": purpose,
        }
        for copy_id, source, target, purpose in [
            ("BC2300_queue_slots", OUTPUTS["slot_inventory"], COPY_TARGETS["queue_slots"], "q parent action slot inventory nonclaim queue"),
            ("BC2300_queue_residuals", OUTPUTS["residuals"], COPY_TARGETS["queue_residuals"], "q residual source vector acquisition queue"),
            ("BC2300_branch_wep", OUTPUTS["residuals"], COPY_TARGETS["branch_wep"], "WEP branch locked q residual copy"),
            ("BC2300_beta_docs", OUTPUTS["slot_inventory"], COPY_TARGETS["beta_docs"], "beta-source docs q parent slot normal form copy"),
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
            "# 2300 - Y5/R2FR Minimal Parent-Action q Source-Vector Normal Form Or Closure Declaration",
            "## Verdict\n\n2300 writes the minimal parent-action normal form for the q branch. This is the cleanest local-GR contract so far for this coupling leg: q must be either first-class/absent, a positive LHS operator with no residual source vector, or a finite residual field whose components are explicitly bounded. No slot is allowed to vanish by vibes.\n\nCurrent result: closure is not claimed. The normal form separates first-class removal, diagonal q dynamics, Ricci/Einstein mixing, Weyl/tidal mixing, matter trace coupling, source-only scalars, body charge, boundary momentum, and readout/history/projector/constant tails. The next leap is binary: prove q is first-class removed, or split `B_qR` into Ricci/Weyl pieces and handle the dangerous residuals.",
            "## Source Register\n\n" + md_table(sections["source_register"]),
            "## Parent Action q Slot Inventory\n\n" + md_table(sections["slot_inventory"]),
            "## q Euler Source-Vector Normal Form\n\n" + md_table(sections["euler_map"]),
            "## Closure Declaration Gate\n\n" + md_table(sections["closure_gate"]),
            "## q First-Class Removal Contract\n\n" + md_table(sections["firstclass_contract"]),
            "## q Residual Acquisition Rows\n\n" + md_table(sections["residuals"]),
            "## Refusal Runner\n\n" + md_table(sections["runner_refusal"]),
            "## Claim Gates\n\n" + md_table(sections["claim_gates"]),
            "## Decision Ledger\n\n" + md_table(sections["decision"]),
            "## Next Target\n\n" + md_table(sections["next_target"]),
            "## Branch Copies\n\n" + md_table(sections["branch_copies"]),
            "## Validation\n\n" + md_table(sections["validation"]),
            "## Working Interpretation\n\nThis is a good kind of grim: the coupling cannot hide anymore. Either q is gauge/constraint and disappears honestly, or it is physical and must carry an explicit residual source vector into local tests. That is exactly the right pressure point for making the GR/Newton reduction derivable instead of asserted.",
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
                if key in {"valid_for_claim", "claim_allowed", "score_ready", "source_backed", "numeric_value_present", "theorem_zero", "score_eligible"} and value is True:
                    return False
                if key == "gate_pass" and value is True:
                    return False
    return True


def formalization_2300_output_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    output_markers = (
        "Y5_R2FR_minimal_parent_action_q_source_vector_normal_form_or_closure_declaration_2300",
        "2300-Y5-R2FR-minimal-parent-action-q-source-vector-normal-form-or-closure-declaration",
        "P8_Y5_PARENT_QLOC_2300_",
        "P8_Y5_BRR545_2300_VALIDATION",
        "JR2300_",
        "Q_PARENT_SLOT_NORMAL_FORM_2300",
    )
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and any(marker in path.name for marker in output_markers)
    )


def pycache_exists() -> bool:
    return any(path.name == "__pycache__" for path in (ROOT / "scripts").rglob("__pycache__"))


def remove_pycache() -> None:
    for path in (ROOT / "scripts").rglob("__pycache__"):
        shutil.rmtree(path)


def validation_rows(sections: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = sections["source_register"]
    output_paths = {name: path for name, path in OUTPUTS.items() if name != "validation"}
    residual_symbols = {row["symbol"] for row in sections["residuals"]}
    required_residuals = {"B_qWeyl", "B_qRic", "C_qT", "epsilon_q_source", "Q_q_body", "Pi_q", "tail_q", "q_firstclass_certificate", "q_residual_abs"}
    slot_ids = {row["slot_id"] for row in sections["slot_inventory"]}
    required_slots = {"QSLOT2300_2_q_constraint", "QSLOT2300_4_BqWeyl_geometry_mix", "QSLOT2300_5_CqT_trace", "QSLOT2300_7_body_worldtube", "QSLOT2300_8_boundary_Piq"}
    checks = [
        ("VAL2300_00_sources_exist", all(row["exists"] for row in source_rows), "all cited local source paths exist"),
        ("VAL2300_01_needles_present", all(row["needles_present"] for row in source_rows), "source register needles are present"),
        ("VAL2300_02_prior_validations_pass", all(row["validation_overall_pass"] in ("", True) for row in source_rows), "prior validation sources pass"),
        ("VAL2300_03_doc_written", DOC.exists() and "Parent Action q Slot Inventory" in read_text(DOC), "checkpoint markdown written"),
        ("VAL2300_04_csv_parse", read_all_outputs(output_paths), "all generated CSVs parse and contain rows"),
        ("VAL2300_05_no_claim_flags", no_claim_flags(sections), "all generated rows remain nonclaim"),
        ("VAL2300_06_slot_inventory_covers_q", required_slots.issubset(slot_ids), "slot inventory covers q constraint, Weyl, matter, body, and boundary slots"),
        ("VAL2300_07_euler_normal_form", any(row["map_id"] == "QEUL2300_0_q_equation" and "B_qW C_Weyl" in row["formula"] for row in sections["euler_map"]), "q Euler/source-vector normal form includes Weyl split and residuals"),
        ("VAL2300_08_firstclass_contract", any(row["contract_id"] == "QFC2300_6_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM_FIRSTCLASS_NOT_PROVED" for row in sections["firstclass_contract"]), "first-class removal remains nonclaim"),
        ("VAL2300_09_closure_rejected", any(row["gate_id"] == "QCLOSE2300_7_verdict" and row["status"] == "FAIL_CURRENT_CLAIM" and row["gate_pass"] is False for row in sections["closure_gate"]), "closure declaration remains nonclaim"),
        ("VAL2300_10_residual_coverage", required_residuals.issubset(residual_symbols), "residual acquisition rows cover q source-vector components and first-class certificate"),
        ("VAL2300_11_runner_refuses", all(row["runner_result"] == "BLOCKED" for row in sections["runner_refusal"]), "refusal runner blocks all current claims"),
        ("VAL2300_12_claim_gates_blocked", all(row["gate_pass"] is False for row in sections["claim_gates"]), "claim gates remain blocked"),
        ("VAL2300_13_decision_next", any(row["decision"] == "Q_FIRSTCLASS_OR_RICCI_WEYL_SPLIT_NEXT" for row in sections["decision"]), "decision selects q first-class or Ricci/Weyl split next"),
        ("VAL2300_14_next_selected", any(row["route_id"] == "NEXT2300_0_primary" and row["selection_status"] == "selected" for row in sections["next_target"]), "next target selected"),
        ("VAL2300_15_branch_copies_exist", all(target.exists() for target in COPY_TARGETS.values()), "branch copy handoffs exist"),
        ("VAL2300_16_formalization_untouched", formalization_2300_output_count() == 0, "no 2300 checkpoint/output files were written under formalization-workbench"),
        ("VAL2300_17_no_pycache", not pycache_exists(), "scripts __pycache__ removed"),
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
            "check_id": "VAL2300_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "2300 writes the minimal q parent slot normal form, rejects closure, keeps first-class removal conditional, splits Ricci/Weyl geometry mixing, and selects q first-class or Ricci/Weyl source-vector split next",
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
        "slot_inventory": slot_inventory_rows(),
        "euler_map": euler_map_rows(),
        "closure_gate": closure_gate_rows(),
        "firstclass_contract": firstclass_contract_rows(),
        "residuals": residual_rows(),
        "runner_refusal": runner_refusal_rows(),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }
    for key, rows in sections.items():
        write_csv(OUTPUTS[key], rows)

    shutil.copyfile(OUTPUTS["slot_inventory"], COPY_TARGETS["queue_slots"])
    shutil.copyfile(OUTPUTS["residuals"], COPY_TARGETS["queue_residuals"])
    shutil.copyfile(OUTPUTS["residuals"], COPY_TARGETS["branch_wep"])
    shutil.copyfile(OUTPUTS["slot_inventory"], COPY_TARGETS["beta_docs"])

    sections["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], sections["branch_copies"])

    sections["validation"] = [
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2300_PENDING",
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
        raise SystemExit(f"2300 validation failed: {OUTPUTS['validation']}")
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

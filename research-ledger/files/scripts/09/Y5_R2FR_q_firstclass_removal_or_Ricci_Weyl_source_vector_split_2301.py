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

BRANCH_ID = "MTS_R2FR_Q_FIRSTCLASS_OR_RICCI_WEYL_SPLIT_2301"
DOC = ROOT / "2301-Y5-R2FR-q-firstclass-removal-or-Ricci-Weyl-source-vector-split.md"

PATHS = {
    "2300_doc": ROOT / "2300-Y5-R2FR-minimal-parent-action-q-source-vector-normal-form-or-closure-declaration.md",
    "2300_validation": OUT / "P8_Y5_BRR545_2300_VALIDATION.csv",
    "2300_next": OUT / "P8_Y5_PARENT_QLOC_2300_NEXT_TARGET.csv",
    "2300_firstclass": OUT / "P8_Y5_PARENT_QLOC_2300_Q_FIRSTCLASS_REMOVAL_CONTRACT.csv",
    "2300_residuals": OUT / "P8_Y5_PARENT_QLOC_2300_Q_RESIDUAL_ACQUISITION_ROWS.csv",
    "2300_slots": OUT / "P8_Y5_PARENT_QLOC_2300_PARENT_ACTION_Q_SLOT_INVENTORY.csv",
    "2296_nohair": OUT / "P8_Y5_PARENT_QLOC_2296_Q_CONDITIONAL_NOHAIR_IDENTITY.csv",
    "2296_firstclass": OUT / "P8_Y5_PARENT_QLOC_2296_FIRSTCLASS_OWNER_GATE.csv",
    "2299_countermodels": OUT / "P8_Y5_PARENT_QLOC_2299_COUNTERMODEL_LEDGER.csv",
    "1768_doc": ROOT / "1768-Y5-R2FR-parent-action-normal-form-and-source-map-identity-signature-or-shadow-coefficient-pack.md",
    "2253_doc": ROOT / "2253-Y5-R2FR-RAB-Ricci-Weyl-split-and-geometric-mixing-diagonalization.md",
    "2253_validation": OUT / "P8_Y5_BRR545_2253_VALIDATION.csv",
    "2253_split": OUT / "P8_Y5_PARENT_QLOC_2253_RICCI_WEYL_SPLIT_ATTEMPT.csv",
    "2253_diag": OUT / "P8_Y5_PARENT_QLOC_2253_GEOMETRIC_DIAGONALIZATION_ATTEMPT.csv",
}

SOURCES = [
    ("SRC2301_00_2300_doc", "2300_handoff", PATHS["2300_doc"], ["DEC2300_3_next", "NEXT2300_0_primary"], "selects q first-class removal or Ricci/Weyl source-vector split"),
    ("SRC2301_01_2300_validation", "2300_validation", PATHS["2300_validation"], ["VAL2300_OVERALL", "PASS"], "confirms 2300 passed"),
    ("SRC2301_02_2300_next", "2300_next", PATHS["2300_next"], ["2301-Y5-R2FR-q-firstclass-removal-or-Ricci-Weyl-source-vector-split.md", "B_qW C_Weyl"], "direct 2301 handoff"),
    ("SRC2301_03_2300_firstclass", "2300_firstclass", PATHS["2300_firstclass"], ["QFC2300_6_verdict", "FAIL_CURRENT_CLAIM_FIRSTCLASS_NOT_PROVED"], "q first-class removal remains unsigned"),
    ("SRC2301_04_2300_residuals", "2300_residuals", PATHS["2300_residuals"], ["QRES2300_0_BqWeyl", "QRES2300_8_total"], "incoming q curvature residual rows"),
    ("SRC2301_05_2300_slots", "2300_slots", PATHS["2300_slots"], ["QSLOT2300_2_q_constraint", "QSLOT2300_4_BqWeyl_geometry_mix"], "q slot inventory contains first-class and Weyl routes"),
    ("SRC2301_06_2296_nohair", "2296_nohair", PATHS["2296_nohair"], ["NH2296_4_firstclass_alternative", "NH2296_3_zero_theorem"], "conditional q no-hair and first-class alternatives"),
    ("SRC2301_07_2296_firstclass", "2296_firstclass", PATHS["2296_firstclass"], ["FC2296_7_verdict", "FAIL_CURRENT_CLAIM_FIRSTCLASS_NOT_PROVED"], "older first-class gate remains blocked"),
    ("SRC2301_08_2299_countermodels", "2299_countermodels", PATHS["2299_countermodels"], ["CM2299_0_mixed_curvature_vertex", "CM2299_1_matter_trace_vertex"], "q mixed vertex countermodels survive"),
    ("SRC2301_09_1768_doc", "1768_normal_form", PATHS["1768_doc"], ["ANF1768_1_geometry_left_hand_owner", "SCL1768_2_nonminimal_coupling"], "normal-form owner and nonminimal coupling classification"),
    ("SRC2301_10_2253_doc", "2253_rab_precedent", PATHS["2253_doc"], ["BWEYL_ZERO_IS_POSSIBLE_BUT_TYPE_GATED", "RAB_REPRESENTATION_CERTIFICATE_OR_BWEYL_BOUND_NEXT"], "R_AB Ricci/Weyl split precedent"),
    ("SRC2301_11_2253_validation", "2253_validation", PATHS["2253_validation"], ["VAL2253_OVERALL", "PASS"], "confirms 2253 passed"),
    ("SRC2301_12_2253_split", "2253_split", PATHS["2253_split"], ["RWS2253_3_representation_escape", "EXACT_CONDITIONAL_INDEX_THEOREM"], "conditional Weyl index theorem precedent"),
    ("SRC2301_13_2253_diag", "2253_diag", PATHS["2253_diag"], ["GDA2253_1_schur_condition", "GDA2253_4_verdict"], "Schur/positive diagonalization precedent"),
]

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2301_SOURCE_REGISTER.csv",
    "firstclass_attempt": OUT / "P8_Y5_PARENT_QLOC_2301_Q_FIRSTCLASS_REMOVAL_ATTEMPT.csv",
    "curvature_split": OUT / "P8_Y5_PARENT_QLOC_2301_Q_RICCI_WEYL_SPLIT_ATTEMPT.csv",
    "representation_gate": OUT / "P8_Y5_PARENT_QLOC_2301_Q_REPRESENTATION_TYPE_GATE.csv",
    "diagonalization": OUT / "P8_Y5_PARENT_QLOC_2301_Q_GEOMETRIC_DIAGONALIZATION_ATTEMPT.csv",
    "local_vacuum": OUT / "P8_Y5_PARENT_QLOC_2301_Q_LOCAL_VACUUM_SOURCE_SILENCE_GATE.csv",
    "residuals": OUT / "P8_Y5_PARENT_QLOC_2301_Q_CURVATURE_RESIDUAL_ACQUISITION_ROWS.csv",
    "runner_refusal": OUT / "P8_Y5_PARENT_QLOC_2301_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2301_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2301_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2301_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2301_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2301_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_firstclass": QUEUE / "JR2301_Q_FIRSTCLASS_REMOVAL_NONCLAIM.csv",
    "queue_split": QUEUE / "JR2301_Q_RICCI_WEYL_SPLIT_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "q_Ricci_Weyl_firstclass_nonclaim_2301.csv",
    "beta_docs": BETA_DOCS / "Q_RICCI_WEYL_FIRSTCLASS_2301_NONCLAIM.csv",
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


def firstclass_attempt_rows() -> list[dict[str, Any]]:
    rows = [
        ("QFC2301_0_parent_Omega", "Omega_Y includes q, geometry, matter, boundary, and source/readout variables", "i_vq Omega_Y can be evaluated on the full phase space", "MISSING_PARENT_OMEGA", "without full phase-space form q cannot be declared gauge"),
        ("QFC2301_1_generator", "Omega_flat(v_q)=delta C_q plus differentiable boundary generator", "C_q is parent-owned and its Hamiltonian flow is v_q", "MISSING_MOMENTUM_MAP", "no first-class removal without a parent-owned generator"),
        ("QFC2301_2_brackets", "{G_q[epsilon],G_q[eta]} closes with zero/proper boundary term", "first-class algebra has no anomalous source/worldtube term", "MISSING_BRACKET_CLOSURE", "an anomaly or second-class edge mode leaves q physical"),
        ("QFC2301_3_degree_count", "constraints remove the q canonical pair from reduced phase space", "degree count deletes the local q pole and no residual q source slot remains", "MISSING_DEGREE_COUNT", "absence of a pole cannot be inferred without counting"),
        ("QFC2301_4_matter_descent", "matter/readout/constants descend to quotient with no q marker", "ordinary matter, clocks, constants, source support, and readout maps carry no q charge", "MISSING_MATTER_DESCENT", "source markers can survive even if bulk q is constrained"),
        ("QFC2301_5_boundary_charge", "Q_q[body], Pi_q, and boundary/reference q charges are zero/proper", "physical source-worldtube matching carries no q edge data", "MISSING_BOUNDARY_SOURCE_NEUTRALITY", "source-worldtube can carry q boundary data"),
        ("QFC2301_6_verdict", "q first-class removal closes all q source slots", "QFC2301_0 through QFC2301_5 pass together in the same parent action", "FAIL_CURRENT_CLAIM_FIRSTCLASS_NOT_PROVED", "finite residual vector remains live"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": attempt_id,
            "needed_clause": clause,
            "test": test,
            "current_status": status,
            "if_missing": if_missing,
            "source_paths": src("2300_firstclass", "2296_firstclass", "2296_nohair"),
            **false_flags(),
        }
        for attempt_id, clause, test, status, if_missing in rows
    ]


def curvature_split_rows() -> list[dict[str, Any]]:
    rows = [
        ("QRWS2301_0_decomposition", "Riemann = Weyl + Ricci-tracefree + scalar-Ricci pieces", "any q-curvature mixing must declare whether it couples to vacuum-silent Ricci/Einstein components or Weyl/tidal components", "B_qR R_obs -> B_qRic R_Ricci + B_qW C_Weyl + B_q_extra higher_order", "SPLIT_CONTRACT_WRITTEN", "MISSING_PARENT_CURVATURE_BASIS"),
        ("QRWS2301_1_Ricci_vacuum_silence", "Ricci/Einstein-sector q mixing is vacuum-silent only after the GR/EH limit is already established", "in a GR exterior vacuum, R_munu=0 and T_H=0, but this cannot be used before the local GR limit is proven", "B_qRic may be LHS-owned, not automatically zero", "CONDITIONAL_ROUTE_UNSIGNED", "MISSING_GR_LHS_LIMIT_AND_Q_DIAGONALIZATION"),
        ("QRWS2301_2_Weyl_not_silent", "Weyl/tidal curvature generally survives in Schwarzschild/exterior vacuum", "a linear B_qW C_Weyl drive would source q outside matter and spoil the clean no-hair branch unless absent or bounded", "B_qWeyl is the dangerous local-GR residual", "DANGER_REGISTERED", "MISSING_BQWEYL_ZERO_OR_BOUND"),
        ("QRWS2301_3_representation_escape", "linear Weyl mixing is index-forbidden for scalar/quotient q without a background Weyl-type spurion", "a scalar/quotient coordinate q cannot contract linearly with C_munuab to a scalar action without an additional four-index field/tensor/projector", "B_qWeyl=0 conditional on q representation certificate and no spurion", "EXACT_CONDITIONAL_INDEX_THEOREM", "MISSING_Q_REPRESENTATION_CERTIFICATE"),
        ("QRWS2301_4_verdict", "q Ricci/Weyl split status", "the split is mathematically clean, but B_qWeyl cannot be set to zero until q representation/type and no-spurion clauses are signed", "retain B_qWeyl as residual until certificate exists", "SPLIT_READY_ZERO_NOT_CLAIMED", "MISSING_Q_TYPE_CERTIFICATE_OR_BQWEYL_BOUND"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "split_id": split_id,
            "claim_piece": claim_piece,
            "argument": argument,
            "normal_form_effect": effect,
            "status": status,
            "missing_for_claim": missing,
            "source_paths": src("2300_residuals", "2253_split", "1768_normal_form"),
            **false_flags(),
        }
        for split_id, claim_piece, argument, effect, status, missing in rows
    ]


def representation_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("QREP2301_0_scalar_quotient", "q is scalar/quotient coordinate", "linear Weyl coupling forbidden by index/representation mismatch without extra spurion", "would set B_qWeyl theorem-zero", "NOT_PARENT_CERTIFIED", "MISSING_Q_SCALAR_QUOTIENT_CERTIFICATE"),
        ("QREP2301_1_density_or_trace", "q is scalar density/trace-like scalar", "linear Weyl scalar still needs a spurion/projector; density weight must be absorbed by measure", "may set B_qWeyl zero if no-spurion and measure clauses are signed", "NOT_PARENT_CERTIFIED", "MISSING_Q_DENSITY_MEASURE_CERTIFICATE"),
        ("QREP2301_2_tensor_or_projector_q", "q carries hidden tensor/projector structure", "linear Weyl mixing can be legal through the hidden index carrier", "B_qWeyl must be bounded, not zero-assumed", "LIVE_COUNTERMODEL", "MISSING_BQWEYL_BOUND"),
        ("QREP2301_3_hidden_spurion", "background/projector/spurion supplies Weyl-type indices", "even scalar q can couple to Weyl through hidden tensor structure", "no-spurion clause required for zero theorem", "LIVE_COUNTERMODEL", "MISSING_NO_SPURION_CERTIFICATE"),
        ("QREP2301_4_firstclass_absent", "q is first-class absent", "Weyl coupling absent after reduction if q itself is removed and boundary/source charges vanish", "would pre-empt B_qWeyl rows", "NOT_PARENT_CERTIFIED", "MISSING_Q_FIRSTCLASS_REMOVAL_CERTIFICATE"),
        ("QREP2301_5_verdict", "q representation/removal certificate", "field type/removal is not sufficiently signed in this branch to claim B_qWeyl=0", "representation gate blocks Weyl-zero promotion", "FAIL_CURRENT_CLAIM", "MISSING_Q_REPRESENTATION_OR_FIRSTCLASS_CERTIFICATE"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "representation_case": case,
            "index_result": result,
            "effect_on_BqWeyl": effect,
            "current_status": status,
            "missing_for_claim": missing,
            "source_paths": src("2300_slots", "2300_firstclass", "2253_split"),
            **false_flags(),
        }
        for gate_id, case, result, effect, status, missing in rows
    ]


def diagonalization_rows() -> list[dict[str, Any]]:
    rows = [
        ("QGDA2301_0_block_form", "L_eff = [[L_GR, B_qRic^T], [B_qRic, L_q]]", "only Ricci/Einstein-sector q geometric mixing is eligible for LHS diagonalization", "BLOCK_FORM_READY", "MISSING_EXPLICIT_L_GR_L_Q_BQRIC_OPERATORS"),
        ("QGDA2301_1_schur_condition", "L_q - B_qRic L_GR^{-1} B_qRic^T > 0 after gauge/constraint quotient", "sufficient condition for positive coupled q/GR operator", "CONDITIONAL_THEOREM_NOT_EVALUATED", "MISSING_OPERATOR_DOMAIN_AND_NORM"),
        ("QGDA2301_2_norm_condition", "||L_q^{-1/2} B_qRic L_GR^{-1/2}|| < 1", "perturbative sufficient condition when direct Schur form is not available", "CONDITIONAL_THEOREM_NOT_EVALUATED", "MISSING_SOURCE_BACKED_OPERATOR_BOUND"),
        ("QGDA2301_3_source_shift_guard", "C_qT T_H cannot be diagonalized as pure geometry", "direct matter-trace coupling remains RHS/nonminimal residual unless parent action forbids or bounds it", "GUARD_ACTIVE", "MISSING_CQT_ZERO_OR_BOUND"),
        ("QGDA2301_4_firstclass_guard", "if q is first-class absent, no L_q/B_qRic diagonalization is needed", "prevents unnecessary finite-field work after a true constraint proof", "GUARD_ACTIVE", "MISSING_Q_FIRSTCLASS_CERTIFICATE"),
        ("QGDA2301_5_verdict", "q geometric diagonalization status", "diagonalization route is mathematically valid as a contract, but not activated because operators/norms and first-class status are missing", "NOT_ACTIVATED", "MISSING_OPERATOR_REALIZATION"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "diag_id": diag_id,
            "condition": condition,
            "purpose": purpose,
            "current_status": status,
            "missing_for_claim": missing,
            "source_paths": src("2253_diag", "2300_residuals", "2296_nohair"),
            **false_flags(),
        }
        for diag_id, condition, purpose, status, missing in rows
    ]


def local_vacuum_rows() -> list[dict[str, Any]]:
    rows = [
        ("QLVS2301_0_firstclass", "q absent from reduced action", "would silence local q exchange if boundary/source/readout descent also holds", "OPEN_BLOCKER", False),
        ("QLVS2301_1_Ricci", "R_Ricci=0 in GR vacuum exterior", "can silence B_qRic only after GR LHS limit and diagonalization are established", "ORDER_GUARD_ACTIVE", False),
        ("QLVS2301_2_Weyl", "C_Weyl generally nonzero outside gravitating bodies", "B_qWeyl must be zero/bounded for local no-hair; exterior vacuum does not help", "OPEN_BLOCKER", False),
        ("QLVS2301_3_body_boundary_tail", "Q_q_body, Pi_q, tail_q", "source-worldtube and readout/history tails are not removed by curvature split", "OPEN_BLOCKER", False),
        ("QLVS2301_4_verdict", "local-vacuum q source silence", "not closed until first-class or B_qWeyl/type gate, body/boundary, tail, and diagonalization clauses pass", "FAIL_CURRENT_CLAIM", False),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "condition": condition,
            "effect": effect,
            "status": status,
            "gate_pass": gate_pass,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, condition, effect, status, gate_pass in rows
    ]


def residual_rows() -> list[dict[str, Any]]:
    rows = [
        ("QCURV2301_0_BqWeyl", "B_qWeyl", "q-Weyl/tidal curvature mixing", "zero if QREP2301_0/1/4 and no-spurion/boundary certificates pass; otherwise numeric/source-backed bound required", "MISSING_REPRESENTATION_OR_FIRSTCLASS_CERTIFICATE_OR_BOUND", "PPN;orbital;local_GR;alpha3"),
        ("QCURV2301_1_BqRic", "B_qRic", "q-Ricci/Einstein geometry mixing", "LHS-owned only after Schur/norm positivity; otherwise finite operator residual", "MISSING_DIAGONALIZATION_OR_BOUND", "local_GR;R10"),
        ("QCURV2301_2_CqT", "C_qT", "q-Hilbert trace coupling", "not killed by curvature split; requires source-slot theorem or bound", "MISSING_CQT_ZERO_OR_BOUND", "WEP;PPN;R10;orbital"),
        ("QCURV2301_3_operator_norm", "N_qRic", "dimensionless q-Ricci mixing operator norm", "N_qRic = ||L_q^{-1/2} B_qRic L_GR^{-1/2}||", "MISSING_OPERATOR_NORM_BOUND", "local_GR"),
        ("QCURV2301_4_firstclass_certificate", "C_q_firstclass", "certificate that q is absent from reduced action", "Omega/DCq/bracket/degree/matter/boundary all signed", "MISSING_Q_FIRSTCLASS_REMOVAL_CERTIFICATE", "all_local_arenas"),
        ("QCURV2301_5_total", "q_curvature_source_residual_abs", "absolute curvature/firstclass residual after split", "|B_qWeyl| + residual(|B_qRic| if not diagonalized) + |C_qT| + |source/body/tail residuals| unless q first-class absent", "SCHEMA_READY_VALUES_MISSING", "local_GR;PPN;R10;orbital;alpha3"),
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
            "source_paths": src("2300_residuals", "2253_split", "2253_diag"),
            **false_flags(),
        }
        for residual_id, symbol, meaning, formula, status, observable in rows
    ]


def runner_refusal_rows() -> list[dict[str, Any]]:
    rows = [
        ("REF2301_0_firstclass", "q first-class absent", "BLOCKED", "QFC2301_6 verdict is not proved"),
        ("REF2301_1_BqWeyl_zero", "B_qWeyl=0 by representation theorem", "BLOCKED", "QREP2301_5 verdict=FAIL_CURRENT_CLAIM"),
        ("REF2301_2_BqRic_diagonalized", "B_qRic safely diagonalized into LHS", "BLOCKED", "QGDA2301_5 verdict=NOT_ACTIVATED"),
        ("REF2301_3_local_vacuum", "local q source silence", "BLOCKED", "QLVS2301_4 verdict=FAIL_CURRENT_CLAIM"),
        ("REF2301_4_nohair", "2296 q no-hair activated", "BLOCKED", "first-class, B_qWeyl/type, diagonalization, body/boundary, and tails remain open"),
        ("REF2301_5_local_GR", "derived local GR/Newton branch", "BLOCKED", "operator/source/boundary/projection gates remain open"),
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
        ("CG2301_0_firstclass", "q first-class/constraint removed", "Omega/DCq/bracket/degree/matter/boundary package missing"),
        ("CG2301_1_Ricci_Weyl_split", "parent q curvature basis split is signed", "split contract is written but q representation certificate missing"),
        ("CG2301_2_BqWeyl", "B_qWeyl theorem-zero or sourced bound", "q type/no-spurion/first-class certificate missing"),
        ("CG2301_3_BqRic", "B_qRic diagonalized into positive LHS operator", "Schur/norm operator data missing"),
        ("CG2301_4_local_vacuum", "local source silence for q", "Weyl/body/boundary/tail gates open"),
        ("CG2301_5_local_GR_Newton", "derived local GR/Newton reduction", "q removal/source/vector/projection gates remain blocked"),
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
        {"branch_id": BRANCH_ID, "decision_id": "DEC2301_0_firstclass", "decision": "Q_FIRSTCLASS_NOT_PROVED", "rationale": "The first-class route remains the cleanest kill for all q source slots, but Omega/DCq/brackets/degree count/matter descent/boundary neutrality are not signed.", "next_action": "do not claim q absent; keep finite residual vector live", "valid_for_claim": False},
        {"branch_id": BRANCH_ID, "decision_id": "DEC2301_1_split_gain", "decision": "Q_RICCI_WEYL_SPLIT_CONTRACT_ESTABLISHED", "rationale": "B_qR is now split into potentially LHS-owned Ricci/Einstein mixing and dangerous exterior Weyl/tidal mixing.", "next_action": "do not treat generic curvature coupling as vacuum-silent", "valid_for_claim": False},
        {"branch_id": BRANCH_ID, "decision_id": "DEC2301_2_index_theorem", "decision": "BQWEYL_ZERO_IS_POSSIBLE_BUT_TYPE_GATED", "rationale": "Linear Weyl coupling is index-forbidden for scalar/quotient q without hidden spurion, but the q representation/no-spurion/first-class certificate is not signed here.", "next_action": "hunt the corpus for q field representation/type/removal signature", "valid_for_claim": False},
        {"branch_id": BRANCH_ID, "decision_id": "DEC2301_3_diagonalization", "decision": "BQ_RIC_DIAGONALIZATION_REQUIRES_OPERATOR_DATA", "rationale": "Schur positivity or operator-norm condition would make Ricci mixing safe, but L_GR/L_q/B_qRic domains and norms are missing.", "next_action": "stage operator-domain/norm requirements after type certificate", "valid_for_claim": False},
        {"branch_id": BRANCH_ID, "decision_id": "DEC2301_4_next", "decision": "Q_REPRESENTATION_OR_FIRSTCLASS_CERTIFICATE_OR_BQWEYL_BOUND_NEXT", "rationale": "The fastest derivation win is to prove q is scalar/quotient or first-class with no Weyl spurion; if not, B_qWeyl must become a finite local bound row.", "next_action": "2302-Y5-R2FR-q-representation-or-firstclass-certificate-or-BqWeyl-bound-row.md", "valid_for_claim": False},
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2301_0_primary",
            "next_target": "2302-Y5-R2FR-q-representation-or-firstclass-certificate-or-BqWeyl-bound-row.md",
            "script": "scripts/Y5_R2FR_q_representation_or_firstclass_certificate_or_BqWeyl_bound_row_2302.py",
            "objective": "inspect/certify the q representation/removal status: scalar/quotient or first-class absent with no Weyl spurion gives a conditional B_qWeyl=0 theorem; tensor/projector/spurion cases require a finite B_qWeyl bound row",
            "selection_status": "selected",
            "success_condition": "q representation/first-class certificate closes B_qWeyl or a source-ready B_qWeyl residual row is staged without claiming local GR",
            "forbidden_shortcuts": "assuming scalar q; ignoring hidden spurions/projectors; declaring Weyl zero from covariance alone; declaring q first-class without Omega/DCq; local-GR/R10/PPN claim; GitHub action; formalization-workbench edit",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2301_1_parallel",
            "next_target": "2302b-Y5-R2FR-BqRic-operator-domain-and-Schur-bound.md",
            "script": "scripts/Y5_R2FR_BqRic_operator_domain_and_Schur_bound_2302b.py",
            "objective": "write L_GR/L_q/B_qRic domains and sufficient Schur/operator-norm positivity conditions for q-Ricci geometric mixing",
            "selection_status": "held_parallel",
            "success_condition": "B_qRic is either positive-diagonalized into LHS or retained as finite operator residual",
            "forbidden_shortcuts": "moving B_qRic to LHS without positivity/domain proof",
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
            ("BC2301_queue_firstclass", OUTPUTS["firstclass_attempt"], COPY_TARGETS["queue_firstclass"], "q first-class removal nonclaim queue"),
            ("BC2301_queue_split", OUTPUTS["curvature_split"], COPY_TARGETS["queue_split"], "q Ricci/Weyl split nonclaim queue"),
            ("BC2301_branch_wep", OUTPUTS["residuals"], COPY_TARGETS["branch_wep"], "WEP branch locked q curvature residual copy"),
            ("BC2301_beta_docs", OUTPUTS["curvature_split"], COPY_TARGETS["beta_docs"], "beta-source docs q Ricci/Weyl split copy"),
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
            "# 2301 - Y5/R2FR q First-Class Removal Or Ricci/Weyl Source-Vector Split",
            "## Verdict\n\n2301 tries the clean route first: remove q as a first-class/constraint variable. That would kill the source vector without fitting. Current result: not signed. The canonical package still lacks parent Omega, momentum map, bracket closure, degree count, matter descent, and boundary/source neutrality.\n\nThe fallback derivation step is now sharp: `B_qR curvature` splits into `B_qRic` and `B_qWeyl`. Ricci/Einstein-sector mixing might become LHS-owned after positivity/diagonalization. Weyl/tidal mixing is dangerous because it survives in local vacuum. There is a possible exact kill: if q is scalar/quotient or first-class absent with no Weyl spurion, linear Weyl mixing is forbidden. That certificate is the next target.",
            "## Source Register\n\n" + md_table(sections["source_register"]),
            "## q First-Class Removal Attempt\n\n" + md_table(sections["firstclass_attempt"]),
            "## q Ricci/Weyl Split Attempt\n\n" + md_table(sections["curvature_split"]),
            "## q Representation Type Gate\n\n" + md_table(sections["representation_gate"]),
            "## q Geometric Diagonalization Attempt\n\n" + md_table(sections["diagonalization"]),
            "## Local Vacuum Source Silence Gate\n\n" + md_table(sections["local_vacuum"]),
            "## q Curvature Residual Acquisition Rows\n\n" + md_table(sections["residuals"]),
            "## Refusal Runner\n\n" + md_table(sections["runner_refusal"]),
            "## Claim Gates\n\n" + md_table(sections["claim_gates"]),
            "## Decision Ledger\n\n" + md_table(sections["decision"]),
            "## Next Target\n\n" + md_table(sections["next_target"]),
            "## Branch Copies\n\n" + md_table(sections["branch_copies"]),
            "## Validation\n\n" + md_table(sections["validation"]),
            "## Working Interpretation\n\nThis is a genuine fork now, not circling: either q is removed by canonical structure, or q is physical and the Weyl piece becomes the local-GR danger. The next checkpoint should certify q's representation/removal status before we waste time fitting a coefficient that might be exactly forbidden.",
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


def formalization_2301_output_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    markers = ("2301-Y5-R2FR-q-firstclass-removal", "P8_Y5_PARENT_QLOC_2301_", "P8_Y5_BRR545_2301", "JR2301_", "Q_RICCI_WEYL_FIRSTCLASS_2301")
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and any(marker in path.name for marker in markers))


def pycache_exists() -> bool:
    return any(path.name == "__pycache__" for path in (ROOT / "scripts").rglob("__pycache__"))


def remove_pycache() -> None:
    for path in (ROOT / "scripts").rglob("__pycache__"):
        shutil.rmtree(path)


def validation_rows(sections: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = sections["source_register"]
    output_paths = {name: path for name, path in OUTPUTS.items() if name != "validation"}
    residual_symbols = {row["symbol"] for row in sections["residuals"]}
    required_residuals = {"B_qWeyl", "B_qRic", "C_qT", "N_qRic", "C_q_firstclass", "q_curvature_source_residual_abs"}
    checks = [
        ("VAL2301_00_sources_exist", all(row["exists"] for row in source_rows), "all cited local source paths exist"),
        ("VAL2301_01_needles_present", all(row["needles_present"] for row in source_rows), "source register needles are present"),
        ("VAL2301_02_prior_validations_pass", all(row["validation_overall_pass"] in ("", True) for row in source_rows), "prior validation sources pass"),
        ("VAL2301_03_doc_written", DOC.exists() and "q First-Class Removal Attempt" in read_text(DOC), "checkpoint markdown written"),
        ("VAL2301_04_csv_parse", read_all_outputs(output_paths), "all generated CSVs parse and contain rows"),
        ("VAL2301_05_no_claim_flags", no_claim_flags(sections), "all generated rows remain nonclaim"),
        ("VAL2301_06_firstclass_refused", any(row["attempt_id"] == "QFC2301_6_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM_FIRSTCLASS_NOT_PROVED" for row in sections["firstclass_attempt"]), "q first-class removal is not promoted"),
        ("VAL2301_07_split_written", any(row["split_id"] == "QRWS2301_0_decomposition" for row in sections["curvature_split"]), "Ricci/Weyl split contract written"),
        ("VAL2301_08_Weyl_danger", any(row["split_id"] == "QRWS2301_2_Weyl_not_silent" and row["status"] == "DANGER_REGISTERED" for row in sections["curvature_split"]), "Weyl/tidal danger registered"),
        ("VAL2301_09_representation_gate_blocks", any(row["gate_id"] == "QREP2301_5_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM" for row in sections["representation_gate"]), "q representation gate blocks B_qWeyl zero claim"),
        ("VAL2301_10_diagonalization_blocked", any(row["diag_id"] == "QGDA2301_5_verdict" and row["current_status"] == "NOT_ACTIVATED" for row in sections["diagonalization"]), "q geometric diagonalization is not activated"),
        ("VAL2301_11_local_vacuum_refused", any(row["gate_id"] == "QLVS2301_4_verdict" and row["status"] == "FAIL_CURRENT_CLAIM" for row in sections["local_vacuum"]), "local vacuum q source silence refused"),
        ("VAL2301_12_residuals_cover_curvature", required_residuals.issubset(residual_symbols), "curvature residual rows cover Weyl, Ricci, trace, operator norm, first-class certificate, and total"),
        ("VAL2301_13_runner_refuses", all(row["runner_result"] == "BLOCKED" for row in sections["runner_refusal"]), "refusal runner blocks all claims"),
        ("VAL2301_14_claim_gates_blocked", all(row["gate_pass"] is False for row in sections["claim_gates"]), "claim gates remain blocked"),
        ("VAL2301_15_decision_next", any(row["decision"] == "Q_REPRESENTATION_OR_FIRSTCLASS_CERTIFICATE_OR_BQWEYL_BOUND_NEXT" for row in sections["decision"]), "decision selects q representation/firstclass certificate or B_qWeyl bound next"),
        ("VAL2301_16_next_selected", any(row["route_id"] == "NEXT2301_0_primary" and row["selection_status"] == "selected" for row in sections["next_target"]), "next target selected"),
        ("VAL2301_17_branch_copies_exist", all(target.exists() for target in COPY_TARGETS.values()), "branch copy handoffs exist"),
        ("VAL2301_18_formalization_untouched", formalization_2301_output_count() == 0, "no 2301 checkpoint/output files were written under formalization-workbench"),
        ("VAL2301_19_no_pycache", not pycache_exists(), "scripts __pycache__ removed"),
    ]
    rows = [
        {"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail, "valid_for_claim": False, "claim_allowed": False}
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2301_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "2301 refuses q first-class removal, splits q Ricci/Weyl mixing, records conditional B_qWeyl index theorem, refuses diagonalization/local-vacuum claims, and selects q representation/firstclass certificate next",
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
        "firstclass_attempt": firstclass_attempt_rows(),
        "curvature_split": curvature_split_rows(),
        "representation_gate": representation_gate_rows(),
        "diagonalization": diagonalization_rows(),
        "local_vacuum": local_vacuum_rows(),
        "residuals": residual_rows(),
        "runner_refusal": runner_refusal_rows(),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }
    for key, rows in sections.items():
        write_csv(OUTPUTS[key], rows)

    shutil.copyfile(OUTPUTS["firstclass_attempt"], COPY_TARGETS["queue_firstclass"])
    shutil.copyfile(OUTPUTS["curvature_split"], COPY_TARGETS["queue_split"])
    shutil.copyfile(OUTPUTS["residuals"], COPY_TARGETS["branch_wep"])
    shutil.copyfile(OUTPUTS["curvature_split"], COPY_TARGETS["beta_docs"])

    sections["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], sections["branch_copies"])

    sections["validation"] = [{"branch_id": BRANCH_ID, "check_id": "VAL2301_PENDING", "result": "PENDING", "detail": "pre-validation document render", "valid_for_claim": False, "claim_allowed": False}]
    write_doc(sections)

    remove_pycache()
    sections["validation"] = validation_rows(sections)
    write_csv(OUTPUTS["validation"], sections["validation"])
    write_doc(sections)

    if sections["validation"][-1]["result"] != "PASS":
        raise SystemExit(f"2301 validation failed: {OUTPUTS['validation']}")
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

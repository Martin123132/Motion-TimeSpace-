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

BRANCH_ID = "MTS_R2FR_PARENT_QLOC_RAB_MINIMAL_PARENT_SLOT_NORMAL_FORM_2252"
DOC = ROOT / "2252-Y5-R2FR-minimal-parent-action-RAB-source-vector-normal-form-or-closure-declaration.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2252_00_2251_doc",
        "source_key": "2251_handoff",
        "source_path": ROOT / "2251-Y5-R2FR-RAB-source-slot-exclusion-or-BRR-CRT-acquisition-ledger.md",
        "needles": ["DEC2251_3_next", "NEXT2251_0_primary"],
        "role": "selects minimal parent-action R_AB source-vector normal form",
    },
    {
        "source_id": "SRC2252_01_2251_validation",
        "source_key": "2251_validation",
        "source_path": OUT / "P8_Y5_BRR545_2251_VALIDATION.csv",
        "needles": ["VAL2251_OVERALL", "PASS"],
        "role": "confirms 2251 passed before 2252 starts",
    },
    {
        "source_id": "SRC2252_02_2251_acquisition",
        "source_key": "2251_acquisition",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2251_BRR_CRT_QR_ACQUISITION_LEDGER.csv",
        "needles": ["ACQ2251_0_BRR", "ACQ2251_6_total_abs"],
        "role": "incoming source-vector components for normal-form ownership",
    },
    {
        "source_id": "SRC2252_03_2251_countermodels",
        "source_key": "2251_countermodels",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2251_COUNTERMODEL_LEDGER.csv",
        "needles": ["CM2251_0_mixed_curvature_vertex", "CM2251_1_matter_trace_vertex"],
        "role": "mixed-vertex countermodels that normal form must classify",
    },
    {
        "source_id": "SRC2252_04_1768_doc",
        "source_key": "1768_normal_form",
        "source_path": ROOT / "1768-Y5-R2FR-parent-action-normal-form-and-source-map-identity-signature-or-shadow-coefficient-pack.md",
        "needles": ["ANF1768_1_geometry_left_hand_owner", "SCL1768_2_nonminimal_coupling"],
        "role": "parent action owner rule and nonminimal-term classification precedent",
    },
    {
        "source_id": "SRC2252_05_2248_doc",
        "source_key": "2248_nohair",
        "source_path": ROOT / "2248-Y5-R2FR-RAB-sourcefree-positive-RAB-nohair-identity-or-alpha3-prior-first-fill.md",
        "needles": ["RNH2248_2_JR_zero", "DEC2248_2_next"],
        "role": "conditional positive source-free R_AB no-hair identity",
    },
    {
        "source_id": "SRC2252_06_2248_validation",
        "source_key": "2248_validation",
        "source_path": OUT / "P8_Y5_BRR545_2248_VALIDATION.csv",
        "needles": ["VAL2248_OVERALL", "PASS"],
        "role": "confirms no-hair checkpoint passed as conditional/nonclaim",
    },
    {
        "source_id": "SRC2252_07_2249_doc",
        "source_key": "2249_body",
        "source_path": ROOT / "2249-Y5-R2FR-RAB-JR-source-zero-or-component-bound-pack.md",
        "needles": ["BCL2249_1_body_charge", "JBT2249_0_BRR"],
        "role": "body-charge and component-bound precedent",
    },
    {
        "source_id": "SRC2252_08_2250_doc",
        "source_key": "2250_signature",
        "source_path": ROOT / "2250-Y5-R2FR-RAB-parent-matter-curvature-source-signature-or-first-body-charge-row.md",
        "needles": ["RSS2250_2_no_curvature_source_vertex", "BCR2250_1_body_charge"],
        "role": "previous source-signature failure and first body-charge row",
    },
    {
        "source_id": "SRC2252_09_1629_doc",
        "source_key": "1629_source_slot",
        "source_path": ROOT / "1629-Y5-R2FR-RAB-source-slot-exclusion-or-finite-JR-prior-width.md",
        "needles": ["RSE1629_7_verdict", "OBS1629_1_action_scale"],
        "role": "source-slot and action-scale obstruction precedent",
    },
    {
        "source_id": "SRC2252_10_1786_boundary",
        "source_key": "1786_boundary",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_1786_BOUNDARY_MATTER_CLOSURE_GATE.csv",
        "needles": ["BMC1786_1_matter_interface", "BMC1786_5_verdict"],
        "role": "boundary/source support closure remains open",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2252_SOURCE_REGISTER.csv",
    "slot_inventory": OUT / "P8_Y5_PARENT_QLOC_2252_PARENT_ACTION_SLOT_INVENTORY.csv",
    "euler_map": OUT / "P8_Y5_PARENT_QLOC_2252_EULER_SOURCE_VECTOR_NORMAL_FORM.csv",
    "closure_gate": OUT / "P8_Y5_PARENT_QLOC_2252_CLOSURE_DECLARATION_GATE.csv",
    "diagonalization": OUT / "P8_Y5_PARENT_QLOC_2252_GEOMETRIC_MIXING_DIAGONALIZATION_CONTRACT.csv",
    "residuals": OUT / "P8_Y5_PARENT_QLOC_2252_RESIDUAL_ACQUISITION_ROWS.csv",
    "runner_refusal": OUT / "P8_Y5_PARENT_QLOC_2252_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2252_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2252_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2252_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2252_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2252_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_slots": QUEUE / "JR2252_PARENT_ACTION_SLOT_INVENTORY_NONCLAIM.csv",
    "queue_residuals": QUEUE / "JR2252_RAB_SOURCE_VECTOR_RESIDUALS_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "RAB_parent_slot_normal_form_nonclaim_2252.csv",
    "beta_docs": BETA_DOCS / "RAB_PARENT_SLOT_NORMAL_FORM_2252_NONCLAIM.csv",
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
        return str(path)


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


def src(*keys: str) -> str:
    by_key = {source["source_key"]: source["source_path"] for source in SOURCES}
    return ";".join(rel(by_key[key]) for key in keys)


def slot_inventory_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "SLOT2252_0_EH_GR",
            "S_EH[e_obs]",
            "Einstein-Hilbert/GR left-hand geometry owner",
            "LHS_GEOMETRY_OWNER_REQUIRED",
            "allowed_required",
            "must reduce to Einstein operator and Newton/Poisson limit before local-GR claim",
            "MISSING_FULL_GR_LHS_DERIVATION",
        ),
        (
            "SLOT2252_1_RAB_diag",
            "1/2 <R_AB, L_R R_AB>",
            "diagonal R_AB operator with Z_R, M_R^2 and boundary form",
            "LHS_RAB_OPERATOR_OWNER",
            "allowed_conditional",
            "2248 no-hair can use this only if positivity, source-free domain, and boundary conditions are signed",
            "MISSING_SIGNED_POSITIVE_OPERATOR_AND_BOUNDARY",
        ),
        (
            "SLOT2252_2_BRR_geometry_mix",
            "<R_AB, B_RR R_Einstein/Ricci>",
            "pure geometry mixing with observed Ricci/Einstein operator",
            "LHS_GEOMETRY_MIXING_OWNER_NOT_ZERO",
            "allowed_as_operator_residual",
            "not a Hilbert matter source, but it can drive R_AB unless diagonalized or shown Ricci-only and vacuum-silent",
            "MISSING_RICCI_WEYL_SPLIT_AND_DIAGONALIZATION",
        ),
        (
            "SLOT2252_3_BRWeyl_geometry_mix",
            "<R_AB, B_RW C_Weyl>",
            "pure geometry mixing with Weyl/tidal curvature",
            "DANGEROUS_GEOMETRY_RESIDUAL",
            "must_forbid_or_bound",
            "Weyl does not vanish in Schwarzschild exterior, so this would threaten local GR even without local T_H",
            "MISSING_WEYL_COUPLING_ZERO_OR_BOUND",
        ),
        (
            "SLOT2252_4_CRT_trace",
            "<R_AB, C_RT T_H>",
            "mixed R_AB-Hilbert matter trace/source term",
            "NONMINIMAL_MATTER_SOURCE_RESIDUAL",
            "must_forbid_or_bound",
            "Hilbert source ownership does not remove pre-action nonminimal matter-geometry coupling",
            "MISSING_CRT_ZERO_OR_BOUND",
        ),
        (
            "SLOT2252_5_epsilon_source_scalar",
            "epsilon_RAB_source sigma_source R_AB",
            "inert/source-only reciprocal scalar",
            "FORBIDDEN_IF_PARENT_HOM_SIGNED_ELSE_RESIDUAL",
            "must_forbid_or_bound",
            "action-scale and no-source-only Hom remain unsigned",
            "MISSING_SOURCE_ONLY_SCALAR_EXCLUSION",
        ),
        (
            "SLOT2252_6_body_worldtube",
            "Q_R[body] matching/source support term",
            "body/interior worldtube charge fixing exterior R_AB data",
            "BODY_SOURCE_RESIDUAL",
            "must_zero_or_bound",
            "exterior vacuum equation is insufficient without source-worldtube neutrality",
            "MISSING_QR_BODY_ZERO_OR_BOUND",
        ),
        (
            "SLOT2252_7_boundary_PiR",
            "Pi_R boundary/reference/support momentum",
            "boundary/source reciprocal momentum",
            "BOUNDARY_OWNER_OR_RESIDUAL",
            "must_zero_or_bound",
            "physical boundary/reference terms are not signed silent",
            "MISSING_PIR_ZERO_OR_BOUND",
        ),
        (
            "SLOT2252_8_tail_R",
            "C_readout_R + K_history_R + Delta_projector_R + C_counterterm_R",
            "readout/history/projector/counterterm source-tail vector",
            "TAIL_RESIDUAL",
            "must_zero_or_bound",
            "post-variation or kernel tails remain open",
            "MISSING_TAIL_ZERO_OR_BOUND",
        ),
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
            "source_paths": src("2251_handoff", "1768_normal_form", "2248_nohair", "2250_signature"),
            **false_flags(),
        }
        for slot_id, action_slot, meaning, owner, slot_status, result, missing in rows
    ]


def euler_map_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "EUL2252_0_R_equation",
            "E_R := L_R R_AB + B_Ric R_Ricci + B_W C_Weyl + C_RT T_H + epsilon_RAB_source sigma_source + Q_R_body delta_body + Pi_R delta_boundary + tail_R = 0",
            "full R_AB Euler normal form",
            "NORMAL_FORM_WRITTEN_NONCLAIM",
            "all source-looking channels are explicit",
        ),
        (
            "EUL2252_1_lhs_geometry_block",
            "[E_GR, E_R]^T = [[L_GR, B_Ric^T], [B_Ric, L_R]] [h, R_AB]^T + B_W C_Weyl + source_residuals",
            "geometric block owner",
            "OPERATOR_OWNED_NOT_ZERO",
            "B_Ric can be LHS geometry mixing, but needs coupled positivity/diagonalization",
        ),
        (
            "EUL2252_2_residual_source_vector",
            "J_R_res := B_W C_Weyl + C_RT T_H + epsilon_RAB_source sigma_source + Q_R_body delta_body + Pi_R delta_boundary + tail_R",
            "absolute residual source vector",
            "RESIDUAL_VECTOR_NONCLAIM",
            "no cancellation allowed; every component must be zero-proved or bounded",
        ),
        (
            "EUL2252_3_local_vacuum_condition",
            "J_R_res=0 in the exterior requires B_W=0/bounded, C_RT T_H=0 outside matter, epsilon=0, Q_R_body=0, Pi_R=0, tail_R=0",
            "local exterior source-free condition",
            "CONDITIONAL_REQUIREMENT",
            "Ricci-only mixing may vanish in GR vacuum, but Weyl/body/boundary tails do not vanish automatically",
        ),
        (
            "EUL2252_4_nohair_activation",
            "2248 positive identity activates only after L_eff positive and J_R_res plus boundary data vanish",
            "no-hair bridge condition",
            "NOT_ACTIVATED",
            "operator positivity and residual-source closure are both open",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "map_id": map_id,
            "formula": formula,
            "role": role,
            "current_status": status,
            "interpretation": interpretation,
            "source_paths": src("2248_nohair", "2251_acquisition", "1768_normal_form"),
            **false_flags(),
        }
        for map_id, formula, role, status, interpretation in rows
    ]


def closure_gate_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CLOSE2252_0_direct_source_slot",
            "ordinary/direct source slot absent",
            "partly classified",
            "R_AB is excluded from minimal visible matter only conditionally; hidden/source scalar and nonminimal slots remain",
            False,
        ),
        (
            "CLOSE2252_1_geometry_mix_owner",
            "B_Ric geometry mixing is LHS-owned",
            "conditional partial progress",
            "owner is plausible in normal form, but positivity/diagonalization and Ricci/Weyl split are unsigned",
            False,
        ),
        (
            "CLOSE2252_2_weyl_mix_zero",
            "B_Weyl=0 or source-backed bound",
            "open",
            "Weyl/tidal curvature does not vanish in local vacuum and is not excluded",
            False,
        ),
        (
            "CLOSE2252_3_matter_trace",
            "C_RT=0 or source-backed bound",
            "open",
            "pre-action nonminimal matter trace coupling remains legal",
            False,
        ),
        (
            "CLOSE2252_4_body_boundary_tails",
            "Q_R[body]=Pi_R=tail_R=0 or bounded",
            "open",
            "body matching, physical boundary, and readout/history tails are not signed silent",
            False,
        ),
        (
            "CLOSE2252_5_verdict",
            "local R_AB source closure",
            "FAIL_CURRENT_CLAIM",
            "normal form clarifies ownership but does not close the full residual vector",
            False,
        ),
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


def diagonalization_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DIAG2252_0_block_operator",
            "L_eff = [[L_GR, B_Ric^T], [B_Ric, L_R]]",
            "write the coupled geometry operator before declaring a source-free R_AB equation",
            "CONTRACT_READY",
            "MISSING_EXPLICIT_OPERATOR_BASIS",
        ),
        (
            "DIAG2252_1_schur_positive",
            "L_R - B_Ric L_GR^{-1} B_Ric^T > 0",
            "sufficient Schur-complement condition for positive coupled operator after quotient/gauge fixing",
            "NOT_DERIVED",
            "MISSING_LGR_INVERSE_GAUGE_FIX_AND_BOUNDS",
        ),
        (
            "DIAG2252_2_small_mix_bound",
            "||L_R^{-1/2} B_Ric L_GR^{-1/2}|| < 1",
            "operator-norm route for perturbative diagonalization",
            "NOT_SOURCED",
            "MISSING_OPERATOR_NORM_BOUND",
        ),
        (
            "DIAG2252_3_Ricci_Weyl_split",
            "B_RR R_obs = B_Ric R_Ricci + B_W C_Weyl",
            "separate vacuum-silent Ricci mixing from exterior tidal/Weyl driving",
            "NEXT_DERIVATION_TARGET",
            "MISSING_PARENT_CURVATURE_BASIS",
        ),
        (
            "DIAG2252_4_vacuum_silence",
            "R_Ricci=0 in GR exterior vacuum, but C_Weyl generally !=0",
            "prevents false source-free claims from generic curvature words",
            "GUARD_RECORDED",
            "MISSING_BW_ZERO_OR_BOUND",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "diag_id": diag_id,
            "condition": condition,
            "purpose": purpose,
            "current_status": status,
            "missing_for_claim": missing,
            "source_paths": src("2248_nohair", "1768_normal_form", "2251_countermodels"),
            **false_flags(),
        }
        for diag_id, condition, purpose, status, missing in rows
    ]


def residual_rows() -> list[dict[str, Any]]:
    rows = [
        ("RES2252_0_BWeyl", "B_Weyl", "Weyl/tidal curvature mixing coefficient", "|B_Weyl| <= zero_or_bound", "MISSING_WEYL_COUPLING_ZERO_OR_BOUND", "PPN;orbital;local_GR"),
        ("RES2252_1_BRic", "B_Ric", "Ricci/Einstein geometric mixing coefficient", "operator_owned_if_diagonalized_else |B_Ric| bound", "MISSING_DIAGONALIZATION_OR_BOUND", "local_GR;R10"),
        ("RES2252_2_CRT", "C_RT", "R_AB-Hilbert trace coupling", "|C_RT| <= zero_or_bound", "MISSING_CRT_ZERO_OR_BOUND", "WEP;PPN;R10;orbital"),
        ("RES2252_3_epsilon", "epsilon_RAB_source", "inert source-only scalar", "|epsilon_RAB_source| <= zero_or_prior_width", "MISSING_SOURCE_ONLY_SCALAR_ZERO_OR_WIDTH", "WEP;R10;clock"),
        ("RES2252_4_QR_body", "Q_R_body", "body/source-worldtube charge", "|Q_R_body| <= body integral plus boundary", "MISSING_BODY_CHARGE_ZERO_OR_BOUND", "R10;PPN;orbital;local_GR"),
        ("RES2252_5_PiR", "Pi_R", "boundary reciprocal momentum", "|Pi_R| <= boundary zero_or_bound", "MISSING_PIR_ZERO_OR_BOUND", "R10;PPN;orbital"),
        ("RES2252_6_tail_R", "tail_R", "readout/history/projector/counterterm source tail", "|tail_R| <= tail envelope", "MISSING_TAIL_ZERO_OR_BOUND", "clock;orbital;PPN"),
        ("RES2252_7_total", "RAB_residual_abs", "absolute residual vector after owner classification", "abs(B_Weyl)+abs(C_RT)+abs(epsilon)+abs(Q_R_body)+abs(Pi_R)+abs(tail_R) plus BRic if not diagonalized", "SCHEMA_READY_VALUES_MISSING", "all_local_arenas"),
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
            "units_status": "MISSING_COMMON_OPERATOR_NORMALIZATION",
            "source_paths": src("2251_acquisition", "2249_body", "2250_signature", "1786_boundary"),
            **false_flags(),
        }
        for residual_id, symbol, meaning, formula, status, observable in rows
    ]


def runner_refusal_rows() -> list[dict[str, Any]]:
    rows = [
        ("REF2252_0_closure", "R_AB source vector closed", "BLOCKED", "CLOSE2252_5_verdict=FAIL_CURRENT_CLAIM"),
        ("REF2252_1_BRic_owner", "B_Ric safely moved to LHS", "BLOCKED", "diagonalization and Ricci/Weyl split unsigned"),
        ("REF2252_2_BWeyl_zero", "Weyl/tidal mixing absent", "BLOCKED", "B_Weyl zero/bound missing"),
        ("REF2252_3_nohair", "2248 no-hair activates", "BLOCKED", "L_eff positivity and residual vector closure missing"),
        ("REF2252_4_local_GR", "derived local GR/Newton branch", "BLOCKED", "GR LHS, source vector, boundary, and projection gates remain open"),
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
        ("CG2252_0_parent_slots", "complete parent-action R_AB slot inventory is signed", "slot inventory is written but not parent-signed"),
        ("CG2252_1_geometric_diagonalization", "geometry mixing is safely LHS-owned", "Schur/operator-norm and Ricci/Weyl split missing"),
        ("CG2252_2_residual_source", "non-geometric residual vector is zero or bounded", "B_Weyl/C_RT/epsilon/Q_R/Pi_R/tail values missing"),
        ("CG2252_3_nohair", "positive no-hair local branch activates", "L_eff positivity and source-free conditions not met"),
        ("CG2252_4_local_GR_Newton", "local GR/Newton reduction is derived", "operator/source/boundary/projection gates remain blocked"),
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
            "decision_id": "DEC2252_0_gain",
            "decision": "SOURCE_VECTOR_NORMAL_FORM_WRITTEN",
            "reason": "B_RR is no longer treated as one vague coupling: Ricci/Einstein geometry mixing, Weyl/tidal mixing, direct matter trace coupling, body charge, boundary momentum, and tails are separated.",
            "next_action": "use the split to target the most damaging local-GR blocker first",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2252_1_partial_owner",
            "decision": "BRIC_CAN_BE_LHS_GEOMETRY_ONLY_IF_DIAGONALIZED",
            "reason": "A Ricci/Einstein-sector B_Ric term is not automatically a matter source, but it still changes the coupled operator and cannot be ignored.",
            "next_action": "derive Schur/positivity or operator-norm diagonalization for the coupled geometry block",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2252_2_guard",
            "decision": "WEYL_MIXING_IS_THE_LOCAL_GR_DANGER",
            "reason": "Ricci terms can be vacuum-silent in a GR exterior, but Weyl/tidal curvature remains outside the source and would generate local residuals unless zeroed or bounded.",
            "next_action": "split B_RR into B_Ric and B_Weyl from parent curvature basis",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2252_3_next",
            "decision": "RICCI_WEYL_SPLIT_AND_GEOMETRIC_DIAGONALIZATION_NEXT",
            "reason": "This is now the least-circular leap toward derived local GR: prove the dangerous Weyl part absent/bounded and show Ricci mixing is a positive LHS operator deformation.",
            "next_action": "2253-Y5-R2FR-RAB-Ricci-Weyl-split-and-geometric-mixing-diagonalization.md",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2252_0_primary",
            "next_target": "2253-Y5-R2FR-RAB-Ricci-Weyl-split-and-geometric-mixing-diagonalization.md",
            "script": "scripts/Y5_R2FR_RAB_Ricci_Weyl_split_and_geometric_mixing_diagonalization_2253.py",
            "objective": "derive the parent curvature basis split B_RR R_obs = B_Ric R_Ricci + B_W C_Weyl, then prove B_W=0/bounded and establish Schur/positive diagonalization for B_Ric before any no-hair activation",
            "selection_status": "selected",
            "success_condition": "B_Weyl is theorem-zero or source-backed bounded, and Ricci mixing is either diagonalized into a positive L_eff or retained as a finite residual",
            "forbidden_shortcuts": "calling all curvature Ricci; ignoring Weyl outside matter; moving B_Ric to LHS without positivity; local-GR/R10/PPN claim; GitHub action; formalization-workbench edit",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2252_1_fallback",
            "next_target": "2253b-Y5-R2FR-RAB-local-source-vector-bound-runner.md",
            "script": "scripts/Y5_R2FR_RAB_local_source_vector_bound_runner_2253b.py",
            "objective": "if the Ricci/Weyl split cannot be derived, build numeric/source-backed bound rows for B_Ric, B_Weyl, C_RT, epsilon_RAB_source, Q_R_body, Pi_R, and tail_R",
            "selection_status": "held_fallback",
            "success_condition": "runner refuses all rows with MISSING values and accepts only numeric, sourced, unit-matched local residual bounds",
            "forbidden_shortcuts": "zero priors by taste; tau=1; cancellation between residual components",
            "valid_for_claim": False,
        },
    ]


def copy_branch_rows() -> list[dict[str, Any]]:
    plan = [
        ("queue_slots", OUTPUTS["slot_inventory"], COPY_TARGETS["queue_slots"], "R_AB parent action slot inventory nonclaim queue"),
        ("queue_residuals", OUTPUTS["residuals"], COPY_TARGETS["queue_residuals"], "R_AB residual source vector acquisition queue"),
        ("branch_wep", OUTPUTS["residuals"], COPY_TARGETS["branch_wep"], "WEP branch locked R_AB residual copy"),
        ("beta_docs", OUTPUTS["slot_inventory"], COPY_TARGETS["beta_docs"], "beta-source docs parent slot normal form copy"),
    ]
    rows = []
    for copy_id, source_path, target_path, reason in plan:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": f"BC2252_{copy_id}",
                "source_path": rel(source_path),
                "target_path": rel(target_path),
                "target_exists": target_path.exists(),
                "target_parses": parse_csv(target_path),
                "reason": reason,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def validation_rows(paths: list[Path]) -> list[dict[str, Any]]:
    source_rows = read_csv(OUTPUTS["source_register"])
    slots = read_csv(OUTPUTS["slot_inventory"])
    euler = read_csv(OUTPUTS["euler_map"])
    closure = read_csv(OUTPUTS["closure_gate"])
    diagonalization = read_csv(OUTPUTS["diagonalization"])
    residuals = read_csv(OUTPUTS["residuals"])
    refusals = read_csv(OUTPUTS["runner_refusal"])
    claims = read_csv(OUTPUTS["claim_gates"])
    decisions = read_csv(OUTPUTS["decision"])
    next_targets = read_csv(OUTPUTS["next_target"])
    copies = read_csv(OUTPUTS["branch_copies"])

    def check(check_id: str, passed: bool, detail: str) -> dict[str, Any]:
        return {"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail}

    csv_parse_ok = True
    for path in paths:
        try:
            parse_csv(path)
        except Exception:
            csv_parse_ok = False

    formalization_2252 = []
    if FORMALIZATION.exists():
        formalization_2252 = [path for path in FORMALIZATION.rglob("*2252*") if path.is_file()]

    all_rows = [row for path in paths for row in read_csv(path)]
    required_symbols = {"B_Weyl", "B_Ric", "C_RT", "epsilon_RAB_source", "Q_R_body", "Pi_R", "tail_R", "RAB_residual_abs"}
    residual_symbols = {row["symbol"] for row in residuals}

    rows = [
        check("VAL2252_0_sources_exist", all(row["exists"] == "True" for row in source_rows), "all cited source paths exist"),
        check("VAL2252_1_needles_present", all(row["needles_present"] == "True" for row in source_rows), "all cited source needles are present"),
        check("VAL2252_2_prior_validations", all(row["validation_overall_pass"] in ("", "True") for row in source_rows), "2251 and 2248 validations pass where checked"),
        check("VAL2252_3_slot_inventory_covers_components", len(slots) >= 9 and any(row["slot_id"] == "SLOT2252_3_BRWeyl_geometry_mix" for row in slots), "parent slot inventory covers EH, R_AB, Ricci, Weyl, matter, body, boundary, and tails"),
        check("VAL2252_4_euler_normal_form_written", any(row["map_id"] == "EUL2252_0_R_equation" and "B_W C_Weyl" in row["formula"] for row in euler), "Euler/source-vector normal form includes Weyl split and residuals"),
        check("VAL2252_5_closure_rejected", any(row["gate_id"] == "CLOSE2252_5_verdict" and row["status"] == "FAIL_CURRENT_CLAIM" and row["gate_pass"] == "False" for row in closure), "closure declaration remains nonclaim"),
        check("VAL2252_6_diagonalization_contract", any(row["diag_id"] == "DIAG2252_1_schur_positive" for row in diagonalization) and any(row["diag_id"] == "DIAG2252_3_Ricci_Weyl_split" for row in diagonalization), "Schur/positive and Ricci/Weyl split contracts are staged"),
        check("VAL2252_7_residual_coverage", required_symbols.issubset(residual_symbols), "residual acquisition rows cover all local source-vector components"),
        check("VAL2252_8_runner_refuses", all(row["runner_result"] == "BLOCKED" for row in refusals), "refusal runner blocks all current claims"),
        check("VAL2252_9_claim_gates_blocked", all(row["gate_pass"] == "False" for row in claims), "claim gates are blocked"),
        check("VAL2252_10_decision_next", any(row["decision_id"] == "DEC2252_3_next" and "RICCI_WEYL" in row["decision"] for row in decisions), "decision selects Ricci/Weyl split and diagonalization next"),
        check("VAL2252_11_next_selected", any(row["route_id"] == "NEXT2252_0_primary" and row["selection_status"] == "selected" for row in next_targets), "next target selected"),
        check("VAL2252_12_csv_parse", csv_parse_ok, "all generated 2252 CSVs parse"),
        check("VAL2252_13_no_claim_flags", all(row.get("valid_for_claim", "False") != "True" and row.get("claim_allowed", "False") != "True" and row.get("theorem_zero", "False") != "True" and row.get("score_ready", "False") != "True" and row.get("source_backed", "False") != "True" for row in all_rows), "no generated theorem/source/score/claim flags are true"),
        check("VAL2252_14_branch_copies", all(row["target_exists"] == "True" and row["target_parses"] == "True" for row in copies), "branch/queue copies exist and parse"),
        check("VAL2252_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        check("VAL2252_16_formalization_no_2252", not formalization_2252, "formalization-workbench has no 2252 outputs"),
    ]
    rows.append(
        check(
            "VAL2252_OVERALL",
            all(row["result"] == "PASS" for row in rows),
            "2252 writes the minimal R_AB parent slot normal form, rejects closure, splits Ricci/Weyl geometry mixing, and selects diagonalization next",
        )
    )
    return rows


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def build_doc(
    source_rows: list[dict[str, Any]],
    slots: list[dict[str, Any]],
    euler: list[dict[str, Any]],
    closure: list[dict[str, Any]],
    diagonalization: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    refusals: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_targets: list[dict[str, Any]],
    copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 2252 - Y5/R2FR Minimal Parent-Action R_AB Source-Vector Normal Form Or Closure Declaration",
            "## Verdict\n\n2252 is a genuine tightening step. It does not close local GR, but it stops the coupling branch from circling the same fog. The parent action must now classify every `R_AB` source-looking channel as one of four things: forbidden by syntax, owned by the left-hand geometric operator, boundary/source-support owned, or a finite residual.\n\nThe useful partial win is that a Ricci/Einstein-sector `B_Ric` term need not be called a matter source; it can be a coupled left-hand geometry operator. But that is not a free pass. It must be diagonalized with a positive coupled operator, and the dangerous Weyl/tidal piece must be absent or bounded because Weyl curvature does not vanish in a local exterior vacuum. Therefore closure is rejected for now, and the next derivation target is the Ricci/Weyl split plus geometric-mixing diagonalization.",
            "## Source Register\n" + markdown_table(source_rows, ["source_id", "source_key", "source_path", "exists", "needles_present", "validation_overall_pass", "role"]),
            "## Parent Action Slot Inventory\n" + markdown_table(slots, ["slot_id", "action_slot", "meaning", "normal_form_owner", "slot_status", "classification_result", "missing_for_closure", "valid_for_claim"]),
            "## Euler Source-Vector Normal Form\n" + markdown_table(euler, ["map_id", "formula", "role", "current_status", "interpretation", "valid_for_claim"]),
            "## Closure Declaration Gate\n" + markdown_table(closure, ["gate_id", "closure_clause", "status", "reason", "gate_pass", "valid_for_claim"]),
            "## Geometric Mixing Diagonalization Contract\n" + markdown_table(diagonalization, ["diag_id", "condition", "purpose", "current_status", "missing_for_claim", "valid_for_claim"]),
            "## Residual Acquisition Rows\n" + markdown_table(residuals, ["residual_id", "symbol", "meaning", "formula_or_bound", "current_status", "observable_link", "valid_for_claim"]),
            "## Refusal Runner\n" + markdown_table(refusals, ["refusal_id", "attempted_claim", "runner_result", "blocked_by", "score_eligible", "valid_for_claim"]),
            "## Claim Gates\n" + markdown_table(claims, ["claim_id", "claim", "gate_pass", "reason", "valid_for_claim"]),
            "## Decision Ledger\n" + markdown_table(decisions, ["decision_id", "decision", "reason", "next_action", "valid_for_claim"]),
            "## Next Target\n" + markdown_table(next_targets, ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "## Branch Copies\n" + markdown_table(copies, ["copy_id", "source_path", "target_path", "target_exists", "target_parses", "reason"]),
            "## Validation\n" + markdown_table(validation, ["check_id", "result", "detail"]),
            "## Working Interpretation\n\nThis is closer to a GR-style derivation path than the previous source-slot attempts. The path is no longer 'make every coupling vanish by assertion.' It is: split the curvature coupling, move only legitimate Ricci/Einstein mixing into a coupled positive LHS operator, prove the Weyl/tidal mixing absent or bounded, and keep direct matter/body/boundary/tail terms as explicit residuals. That is a serious route because it gives the theory a way to reduce to GR locally without pretending every intermediate object is zero by taste.",
        ]
    ) + "\n"


def main() -> None:
    remove_pycache()

    source_rows = source_register_rows()
    write_csv(OUTPUTS["source_register"], source_rows)

    slots = slot_inventory_rows()
    euler = euler_map_rows()
    closure = closure_gate_rows()
    diagonalization = diagonalization_rows()
    residuals = residual_rows()
    refusals = runner_refusal_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_targets = next_target_rows()

    write_csv(OUTPUTS["slot_inventory"], slots)
    write_csv(OUTPUTS["euler_map"], euler)
    write_csv(OUTPUTS["closure_gate"], closure)
    write_csv(OUTPUTS["diagonalization"], diagonalization)
    write_csv(OUTPUTS["residuals"], residuals)
    write_csv(OUTPUTS["runner_refusal"], refusals)
    write_csv(OUTPUTS["claim_gates"], claims)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next_target"], next_targets)

    copies = copy_branch_rows()
    write_csv(OUTPUTS["branch_copies"], copies)

    generated = [
        OUTPUTS["source_register"],
        OUTPUTS["slot_inventory"],
        OUTPUTS["euler_map"],
        OUTPUTS["closure_gate"],
        OUTPUTS["diagonalization"],
        OUTPUTS["residuals"],
        OUTPUTS["runner_refusal"],
        OUTPUTS["claim_gates"],
        OUTPUTS["decision"],
        OUTPUTS["next_target"],
        OUTPUTS["branch_copies"],
    ]
    validation = validation_rows(generated)
    write_csv(OUTPUTS["validation"], validation)
    remove_pycache()
    validation = validation_rows(generated)
    write_csv(OUTPUTS["validation"], validation)

    DOC.write_text(
        build_doc(source_rows, slots, euler, closure, diagonalization, residuals, refusals, claims, decisions, next_targets, copies, validation),
        encoding="utf-8",
    )

    if not all(row["result"] == "PASS" for row in validation):
        raise SystemExit("2252 validation failed")

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

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

BRANCH_ID = "MTS_R2FR_PARENT_QLOC_RAB_RICCI_WEYL_DIAGONALIZATION_2253"
DOC = ROOT / "2253-Y5-R2FR-RAB-Ricci-Weyl-split-and-geometric-mixing-diagonalization.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2253_00_2252_doc",
        "source_key": "2252_handoff",
        "source_path": ROOT / "2252-Y5-R2FR-minimal-parent-action-RAB-source-vector-normal-form-or-closure-declaration.md",
        "needles": ["DEC2252_3_next", "NEXT2252_0_primary"],
        "role": "selects Ricci/Weyl split and geometric diagonalization",
    },
    {
        "source_id": "SRC2253_01_2252_validation",
        "source_key": "2252_validation",
        "source_path": OUT / "P8_Y5_BRR545_2252_VALIDATION.csv",
        "needles": ["VAL2252_OVERALL", "PASS"],
        "role": "confirms 2252 passed before 2253 starts",
    },
    {
        "source_id": "SRC2253_02_2252_slots",
        "source_key": "2252_slots",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2252_PARENT_ACTION_SLOT_INVENTORY.csv",
        "needles": ["SLOT2252_2_BRR_geometry_mix", "SLOT2252_3_BRWeyl_geometry_mix"],
        "role": "incoming Ricci/Weyl slot split",
    },
    {
        "source_id": "SRC2253_03_2252_diag",
        "source_key": "2252_diag",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2252_GEOMETRIC_MIXING_DIAGONALIZATION_CONTRACT.csv",
        "needles": ["DIAG2252_1_schur_positive", "DIAG2252_3_Ricci_Weyl_split"],
        "role": "Schur/positive diagonalization contract",
    },
    {
        "source_id": "SRC2253_04_2252_residuals",
        "source_key": "2252_residuals",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2252_RESIDUAL_ACQUISITION_ROWS.csv",
        "needles": ["RES2252_0_BWeyl", "RES2252_1_BRic"],
        "role": "B_Weyl and B_Ric residual rows",
    },
    {
        "source_id": "SRC2253_05_2248_doc",
        "source_key": "2248_nohair",
        "source_path": ROOT / "2248-Y5-R2FR-RAB-sourcefree-positive-RAB-nohair-identity-or-alpha3-prior-first-fill.md",
        "needles": ["RNH2248_2_JR_zero", "VAL2248_OVERALL"],
        "role": "source-free positive identity requiring source closure",
    },
    {
        "source_id": "SRC2253_06_1768_doc",
        "source_key": "1768_normal_form",
        "source_path": ROOT / "1768-Y5-R2FR-parent-action-normal-form-and-source-map-identity-signature-or-shadow-coefficient-pack.md",
        "needles": ["ANF1768_1_geometry_left_hand_owner", "GRB1768_1_lhs_operator"],
        "role": "LHS geometry owner and GR operator limit remains open",
    },
    {
        "source_id": "SRC2253_07_1761_doc",
        "source_key": "1761_no_direct_vertex",
        "source_path": ROOT / "1761-Y5-R2FR-no-direct-matter-X-vertex-grammar-or-Amatter-coefficient-pack.md",
        "needles": ["DV1761_3_shadow_frame", "GATE1761_4_local_GR_Newton"],
        "role": "hidden frame/source slot warnings",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2253_SOURCE_REGISTER.csv",
    "curvature_split": OUT / "P8_Y5_PARENT_QLOC_2253_RICCI_WEYL_SPLIT_ATTEMPT.csv",
    "representation_gate": OUT / "P8_Y5_PARENT_QLOC_2253_RAB_REPRESENTATION_TYPE_GATE.csv",
    "diagonalization": OUT / "P8_Y5_PARENT_QLOC_2253_GEOMETRIC_DIAGONALIZATION_ATTEMPT.csv",
    "local_vacuum": OUT / "P8_Y5_PARENT_QLOC_2253_LOCAL_VACUUM_SOURCE_SILENCE_GATE.csv",
    "residuals": OUT / "P8_Y5_PARENT_QLOC_2253_CURVATURE_RESIDUAL_ACQUISITION_ROWS.csv",
    "runner_refusal": OUT / "P8_Y5_PARENT_QLOC_2253_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2253_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2253_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2253_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2253_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2253_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_split": QUEUE / "JR2253_RICCI_WEYL_SPLIT_NONCLAIM.csv",
    "queue_rep": QUEUE / "JR2253_RAB_REPRESENTATION_GATE_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "RAB_Ricci_Weyl_diagonalization_nonclaim_2253.csv",
    "beta_docs": BETA_DOCS / "RAB_RICCI_WEYL_DIAGONALIZATION_2253_NONCLAIM.csv",
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


def curvature_split_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "RWS2253_0_decomposition",
            "Riemann = Weyl + Ricci-tracefree + scalar-Ricci pieces",
            "any local curvature mixing must declare whether it couples to vacuum-silent Ricci/Einstein components or to Weyl/tidal components",
            "B_RR R_obs -> B_Ric R_Ricci + B_W C_Weyl + B_extra higher_order",
            "SPLIT_CONTRACT_WRITTEN",
            "MISSING_PARENT_CURVATURE_BASIS",
        ),
        (
            "RWS2253_1_Ricci_vacuum_silence",
            "Ricci/Einstein-sector mixing is vacuum-silent only after the GR/EH limit is already established",
            "in a GR exterior vacuum, R_munu=0 and T_H=0, but this cannot be used before the local GR limit is proven",
            "B_Ric may be LHS-owned, not automatically zero",
            "CONDITIONAL_ROUTE_UNSIGNED",
            "MISSING_GR_LHS_LIMIT_AND_DIAGONALIZATION",
        ),
        (
            "RWS2253_2_Weyl_not_silent",
            "Weyl/tidal curvature generally survives in Schwarzschild/exterior vacuum",
            "a linear B_W C_Weyl drive would source R_AB outside matter and spoil the clean no-hair branch unless absent or bounded",
            "B_Weyl is the dangerous local-GR residual",
            "DANGER_REGISTERED",
            "MISSING_BWEYL_ZERO_OR_BOUND",
        ),
        (
            "RWS2253_3_representation_escape",
            "linear Weyl mixing is index-forbidden for scalar/trace-only R_AB without a background Weyl-type spurion",
            "a scalar or trace/Ricci-type R_AB cannot contract linearly with C_munuab to a scalar action without an additional four-index field/tensor",
            "B_Weyl=0 conditional on R_AB representation certificate and no spurion",
            "EXACT_CONDITIONAL_INDEX_THEOREM",
            "MISSING_RAB_REPRESENTATION_CERTIFICATE",
        ),
        (
            "RWS2253_4_verdict",
            "Ricci/Weyl split status",
            "the split is mathematically clean, but B_Weyl cannot be set to zero until R_AB representation/type and no-spurion clauses are signed",
            "retain B_Weyl as residual until certificate exists",
            "SPLIT_READY_ZERO_NOT_CLAIMED",
            "MISSING_RAB_TYPE_CERTIFICATE_OR_BWEYL_BOUND",
        ),
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
            "source_paths": src("2252_handoff", "2252_slots", "2252_diag"),
            **false_flags(),
        }
        for split_id, claim_piece, argument, effect, status, missing in rows
    ]


def representation_gate_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "REP2253_0_scalar_trace",
            "R_AB is scalar/trace/Ricci-type",
            "linear Weyl coupling forbidden by index/representation mismatch without extra spurion",
            "would set B_Weyl theorem-zero",
            "NOT_PARENT_CERTIFIED",
            "MISSING_RAB_SCALAR_TRACE_CERTIFICATE",
        ),
        (
            "REP2253_1_symmetric_two_tensor",
            "R_AB is symmetric two-tensor",
            "direct linear Weyl scalar still requires extra contractions; Ricci-type mixing is natural, Weyl mixing requires derivative/projector structure",
            "may reduce B_Weyl to higher-derivative/projector residual",
            "NOT_PARENT_CERTIFIED",
            "MISSING_INDEX_AND_PROJECTOR_BASIS",
        ),
        (
            "REP2253_2_weyl_type_tensor",
            "R_AB carries Weyl/Riemann-type four-index representation",
            "linear Weyl mixing is legal and dangerous",
            "B_Weyl must be bounded, not zero-assumed",
            "LIVE_COUNTERMODEL",
            "MISSING_BWEYL_BOUND",
        ),
        (
            "REP2253_3_hidden_spurion",
            "background/projector/spurion supplies Weyl-type indices",
            "even scalar R_AB can couple to Weyl through hidden tensor structure",
            "no-spurion clause required for zero theorem",
            "LIVE_COUNTERMODEL",
            "MISSING_NO_SPURION_CERTIFICATE",
        ),
        (
            "REP2253_4_verdict",
            "R_AB representation certificate",
            "field type is not sufficiently signed in this branch to claim B_Weyl=0",
            "representation gate blocks Weyl-zero promotion",
            "FAIL_CURRENT_CLAIM",
            "MISSING_RAB_REPRESENTATION_CERTIFICATE",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "representation_case": case,
            "index_result": result,
            "effect_on_BWeyl": effect,
            "current_status": status,
            "missing_for_claim": missing,
            "source_paths": src("2252_slots", "1761_no_direct_vertex", "1768_normal_form"),
            **false_flags(),
        }
        for gate_id, case, result, effect, status, missing in rows
    ]


def diagonalization_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "GDA2253_0_block_form",
            "L_eff = [[L_GR, B_Ric^T], [B_Ric, L_R]]",
            "only Ricci/Einstein-sector geometric mixing is eligible for LHS diagonalization",
            "BLOCK_FORM_READY",
            "MISSING_EXPLICIT_L_GR_L_R_B_RIC_OPERATORS",
        ),
        (
            "GDA2253_1_schur_condition",
            "L_R - B_Ric L_GR^{-1} B_Ric^T > 0 after gauge/constraint quotient",
            "sufficient condition for positive coupled R_AB/GR operator",
            "CONDITIONAL_THEOREM_NOT_EVALUATED",
            "MISSING_OPERATOR_DOMAIN_AND_NORM",
        ),
        (
            "GDA2253_2_norm_condition",
            "||L_R^{-1/2} B_Ric L_GR^{-1/2}|| < 1",
            "perturbative sufficient condition when direct Schur form is not available",
            "CONDITIONAL_THEOREM_NOT_EVALUATED",
            "MISSING_SOURCE_BACKED_OPERATOR_BOUND",
        ),
        (
            "GDA2253_3_source_shift_guard",
            "C_RT T_H cannot be diagonalized as pure geometry",
            "direct matter-trace coupling remains RHS/nonminimal residual unless parent action forbids or bounds it",
            "GUARD_ACTIVE",
            "MISSING_CRT_ZERO_OR_BOUND",
        ),
        (
            "GDA2253_4_verdict",
            "geometric diagonalization status",
            "diagonalization route is mathematically valid as a contract, but not activated because operators/norms are missing",
            "NOT_ACTIVATED",
            "MISSING_OPERATOR_REALIZATION",
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
            "source_paths": src("2252_diag", "2248_nohair", "1768_normal_form"),
            **false_flags(),
        }
        for diag_id, condition, purpose, status, missing in rows
    ]


def local_vacuum_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "LVS2253_0_exterior_T",
            "T_H=0 outside compact source",
            "removes direct C_RT T_H only in exterior, not body charge or boundary data",
            "CONDITIONAL_EXTERIOR_ONLY",
            False,
        ),
        (
            "LVS2253_1_Ricci",
            "R_Ricci=0 in GR vacuum exterior",
            "can silence B_Ric only after GR LHS limit and diagonalization are established",
            "ORDER_GUARD_ACTIVE",
            False,
        ),
        (
            "LVS2253_2_Weyl",
            "C_Weyl generally nonzero outside gravitating bodies",
            "B_Weyl must be zero/bounded for local no-hair; exterior vacuum does not help",
            "OPEN_BLOCKER",
            False,
        ),
        (
            "LVS2253_3_body_boundary",
            "Q_R_body and Pi_R can set exterior boundary data",
            "source-free differential equation does not imply source-free solution",
            "OPEN_BLOCKER",
            False,
        ),
        (
            "LVS2253_4_verdict",
            "local-vacuum source silence",
            "not closed until B_Weyl/type gate, body/boundary, tail, and diagonalization clauses pass",
            "FAIL_CURRENT_CLAIM",
            False,
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "vacuum_id": vacuum_id,
            "condition": condition,
            "effect": effect,
            "current_status": status,
            "gate_pass": gate_pass,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for vacuum_id, condition, effect, status, gate_pass in rows
    ]


def residual_rows() -> list[dict[str, Any]]:
    rows = [
        ("CURV2253_0_BWeyl", "B_Weyl", "Weyl/tidal curvature mixing", "zero if REP2253_0/1 and no-spurion certificate pass; otherwise numeric/source-backed bound required", "MISSING_REPRESENTATION_CERTIFICATE_OR_BOUND", "PPN;orbital;local_GR"),
        ("CURV2253_1_BRic", "B_Ric", "Ricci/Einstein geometry mixing", "LHS-owned only after Schur/norm positivity; otherwise finite operator residual", "MISSING_DIAGONALIZATION_OR_BOUND", "local_GR;R10"),
        ("CURV2253_2_CRT", "C_RT", "matter trace coupling not included in geometry diagonalization", "zero theorem or bound required", "MISSING_CRT_ZERO_OR_BOUND", "WEP;PPN;R10"),
        ("CURV2253_3_operator_norm", "N_Ric", "dimensionless Ricci-mixing operator norm", "N_Ric = ||L_R^{-1/2} B_Ric L_GR^{-1/2}||", "MISSING_OPERATOR_NORM_BOUND", "local_GR"),
        ("CURV2253_4_total", "curvature_source_residual_abs", "absolute curvature residual after split", "|B_Weyl| + residual(|B_Ric| if not diagonalized) + |C_RT|", "SCHEMA_READY_VALUES_MISSING", "local_GR;PPN;R10;orbital"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "residual_id": residual_id,
            "symbol": symbol,
            "meaning": meaning,
            "formula_or_requirement": formula,
            "current_status": status,
            "observable_link": observable,
            "units_status": "MISSING_COMMON_OPERATOR_NORMALIZATION",
            "source_paths": src("2252_residuals", "2252_diag"),
            **false_flags(),
        }
        for residual_id, symbol, meaning, formula, status, observable in rows
    ]


def runner_refusal_rows() -> list[dict[str, Any]]:
    rows = [
        ("REF2253_0_BWeyl_zero", "B_Weyl=0 by representation theorem", "BLOCKED", "REP2253_4_verdict=FAIL_CURRENT_CLAIM"),
        ("REF2253_1_BRic_diagonalized", "B_Ric safely diagonalized into LHS", "BLOCKED", "GDA2253_4_verdict=NOT_ACTIVATED"),
        ("REF2253_2_local_vacuum", "local exterior R_AB source silence", "BLOCKED", "LVS2253_4_verdict=FAIL_CURRENT_CLAIM"),
        ("REF2253_3_nohair", "2248 no-hair activated", "BLOCKED", "B_Weyl/type, diagonalization, body/boundary and tails remain open"),
        ("REF2253_4_local_GR", "derived local GR/Newton branch", "BLOCKED", "no claim until representation and operator certificates exist"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "refusal_id": refusal_id,
            "attempted_claim": claim,
            "runner_result": result,
            "blocked_by": blocked_by,
            "score_eligible": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for refusal_id, claim, result, blocked_by in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2253_0_Ricci_Weyl_split", "parent curvature basis split is signed", "split contract is written but representation certificate missing"),
        ("CG2253_1_BWeyl", "B_Weyl theorem-zero or sourced bound", "R_AB type/no-spurion certificate missing"),
        ("CG2253_2_BRic", "B_Ric diagonalized into positive LHS operator", "Schur/norm operator data missing"),
        ("CG2253_3_local_vacuum", "local source silence for R_AB", "Weyl/body/boundary/tail gates open"),
        ("CG2253_4_local_GR_Newton", "derived local GR/Newton reduction", "operator/source/representation gates remain blocked"),
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
            "decision_id": "DEC2253_0_split_gain",
            "decision": "RICCI_WEYL_SPLIT_CONTRACT_ESTABLISHED",
            "reason": "B_RR is now split into a potentially LHS-owned Ricci/Einstein part and a dangerous exterior Weyl/tidal part.",
            "next_action": "do not treat generic curvature coupling as vacuum-silent",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2253_1_index_theorem",
            "decision": "BWEYL_ZERO_IS_POSSIBLE_BUT_TYPE_GATED",
            "reason": "Linear Weyl coupling is index-forbidden for scalar/trace-only R_AB without a hidden spurion, but the R_AB representation certificate is not signed here.",
            "next_action": "hunt the corpus for R_AB field representation/type signature",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2253_2_diagonalization",
            "decision": "BRIC_DIAGONALIZATION_REQUIRES_OPERATOR_DATA",
            "reason": "Schur positivity or the operator-norm condition would make Ricci mixing safe, but L_GR/L_R/B_Ric domains and norms are missing.",
            "next_action": "stage operator-domain/norm requirements after type certificate",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2253_3_next",
            "decision": "RAB_REPRESENTATION_CERTIFICATE_OR_BWEYL_BOUND_NEXT",
            "reason": "The fastest derivation win is to prove R_AB is scalar/trace/Ricci-type with no Weyl spurion; if not, B_Weyl must become a finite local bound row.",
            "next_action": "2254-Y5-R2FR-RAB-representation-certificate-or-BWeyl-bound-row.md",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2253_0_primary",
            "next_target": "2254-Y5-R2FR-RAB-representation-certificate-or-BWeyl-bound-row.md",
            "script": "scripts/Y5_R2FR_RAB_representation_certificate_or_BWeyl_bound_row_2254.py",
            "objective": "inspect/certify the index representation of R_AB: scalar/trace/Ricci-type with no Weyl spurion gives a conditional B_Weyl=0 theorem; Weyl-type or hidden-spurion cases require a finite B_Weyl bound row",
            "selection_status": "selected",
            "success_condition": "R_AB representation certificate closes B_Weyl or a source-ready B_Weyl residual row is staged without claiming local GR",
            "forbidden_shortcuts": "assuming scalar type; ignoring hidden spurions/projectors; declaring Weyl zero from covariance alone; local-GR/R10/PPN claim; GitHub action; formalization-workbench edit",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2253_1_parallel",
            "next_target": "2254b-Y5-R2FR-BRic-operator-domain-and-Schur-bound.md",
            "script": "scripts/Y5_R2FR_BRic_operator_domain_and_Schur_bound_2254b.py",
            "objective": "write L_GR/L_R/B_Ric domains and sufficient Schur/operator-norm positivity conditions for Ricci geometric mixing",
            "selection_status": "held_parallel",
            "success_condition": "B_Ric is either positive-diagonalized into LHS or retained as finite operator residual",
            "forbidden_shortcuts": "moving B_Ric to LHS without positivity/domain proof",
            "valid_for_claim": False,
        },
    ]


def copy_branch_rows() -> list[dict[str, Any]]:
    plan = [
        ("queue_split", OUTPUTS["curvature_split"], COPY_TARGETS["queue_split"], "Ricci/Weyl split nonclaim queue"),
        ("queue_rep", OUTPUTS["representation_gate"], COPY_TARGETS["queue_rep"], "R_AB representation gate nonclaim queue"),
        ("branch_wep", OUTPUTS["residuals"], COPY_TARGETS["branch_wep"], "WEP branch locked curvature residual copy"),
        ("beta_docs", OUTPUTS["curvature_split"], COPY_TARGETS["beta_docs"], "beta-source docs Ricci/Weyl split copy"),
    ]
    rows = []
    for copy_id, source_path, target_path, reason in plan:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": f"BC2253_{copy_id}",
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
    split = read_csv(OUTPUTS["curvature_split"])
    rep = read_csv(OUTPUTS["representation_gate"])
    diag = read_csv(OUTPUTS["diagonalization"])
    vacuum = read_csv(OUTPUTS["local_vacuum"])
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

    formalization_2253 = []
    if FORMALIZATION.exists():
        formalization_2253 = [path for path in FORMALIZATION.rglob("*2253*") if path.is_file()]

    all_rows = [row for path in paths for row in read_csv(path)]
    residual_symbols = {row["symbol"] for row in residuals}

    rows = [
        check("VAL2253_0_sources_exist", all(row["exists"] == "True" for row in source_rows), "all cited source paths exist"),
        check("VAL2253_1_needles_present", all(row["needles_present"] == "True" for row in source_rows), "all cited source needles are present"),
        check("VAL2253_2_prior_validation", all(row["validation_overall_pass"] in ("", "True") for row in source_rows), "2252 validation passes where checked"),
        check("VAL2253_3_split_written", any(row["split_id"] == "RWS2253_0_decomposition" and "B_W C_Weyl" in row["normal_form_effect"] for row in split), "Ricci/Weyl split contract written"),
        check("VAL2253_4_index_theorem_conditional", any(row["split_id"] == "RWS2253_3_representation_escape" and row["status"] == "EXACT_CONDITIONAL_INDEX_THEOREM" for row in split), "conditional index theorem recorded without promotion"),
        check("VAL2253_5_representation_gate_blocks", any(row["gate_id"] == "REP2253_4_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM" for row in rep), "R_AB representation gate blocks B_Weyl zero claim"),
        check("VAL2253_6_diagonalization_not_activated", any(row["diag_id"] == "GDA2253_4_verdict" and row["current_status"] == "NOT_ACTIVATED" for row in diag), "geometric diagonalization remains inactive"),
        check("VAL2253_7_local_vacuum_rejected", any(row["vacuum_id"] == "LVS2253_4_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM" for row in vacuum), "local-vacuum source silence is not claimed"),
        check("VAL2253_8_residuals_cover_curvature", {"B_Weyl", "B_Ric", "C_RT", "N_Ric", "curvature_source_residual_abs"}.issubset(residual_symbols), "curvature residual rows cover Weyl, Ricci, trace coupling and operator norm"),
        check("VAL2253_9_runner_refuses", all(row["runner_result"] == "BLOCKED" for row in refusals), "refusal runner blocks all current claims"),
        check("VAL2253_10_claim_gates_blocked", all(row["gate_pass"] == "False" for row in claims), "claim gates are blocked"),
        check("VAL2253_11_decision_next", any(row["decision_id"] == "DEC2253_3_next" and "REPRESENTATION" in row["decision"] for row in decisions), "decision selects representation certificate or B_Weyl bound next"),
        check("VAL2253_12_next_selected", any(row["route_id"] == "NEXT2253_0_primary" and row["selection_status"] == "selected" for row in next_targets), "next target selected"),
        check("VAL2253_13_csv_parse", csv_parse_ok, "all generated 2253 CSVs parse"),
        check("VAL2253_14_no_claim_flags", all(row.get("valid_for_claim", "False") != "True" and row.get("claim_allowed", "False") != "True" and row.get("theorem_zero", "False") != "True" and row.get("score_ready", "False") != "True" and row.get("source_backed", "False") != "True" for row in all_rows), "no generated theorem/source/score/claim flags are true"),
        check("VAL2253_15_branch_copies", all(row["target_exists"] == "True" and row["target_parses"] == "True" for row in copies), "branch/queue copies exist and parse"),
        check("VAL2253_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        check("VAL2253_17_formalization_no_2253", not formalization_2253, "formalization-workbench has no 2253 outputs"),
    ]
    rows.append(
        check(
            "VAL2253_OVERALL",
            all(row["result"] == "PASS" for row in rows),
            "2253 splits Ricci/Weyl geometry mixing, records conditional index theorem for B_Weyl, refuses diagonalization/local-vacuum claims, and selects R_AB representation certificate next",
        )
    )
    return rows


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def build_doc(
    source_rows: list[dict[str, Any]],
    split: list[dict[str, Any]],
    rep: list[dict[str, Any]],
    diag: list[dict[str, Any]],
    vacuum: list[dict[str, Any]],
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
            "# 2253 - Y5/R2FR R_AB Ricci/Weyl Split And Geometric Mixing Diagonalization",
            "## Verdict\n\n2253 makes the local-GR problem sharper. Generic `B_RR curvature` language is now split into `B_Ric` and `B_Weyl`. Ricci/Einstein-sector mixing might be left-hand geometry and may become safe after a positive Schur/diagonalization proof. Weyl/tidal mixing is different: it survives outside a compact source and would drive `R_AB` in local vacuum unless it is forbidden by representation/index type or bounded.\n\nThere is one real derivation opening: if `R_AB` is scalar/trace/Ricci-type and the parent action has no hidden Weyl-type spurion/projector, a linear Weyl coupling is index-forbidden. But the current branch has not certified the representation of `R_AB`, so `B_Weyl=0` is not claimed. Next target is the `R_AB` representation certificate; if it fails, `B_Weyl` becomes a finite local residual bound row.",
            "## Source Register\n" + markdown_table(source_rows, ["source_id", "source_key", "source_path", "exists", "needles_present", "validation_overall_pass", "role"]),
            "## Ricci/Weyl Split Attempt\n" + markdown_table(split, ["split_id", "claim_piece", "argument", "normal_form_effect", "status", "missing_for_claim", "valid_for_claim"]),
            "## R_AB Representation Type Gate\n" + markdown_table(rep, ["gate_id", "representation_case", "index_result", "effect_on_BWeyl", "current_status", "missing_for_claim", "valid_for_claim"]),
            "## Geometric Diagonalization Attempt\n" + markdown_table(diag, ["diag_id", "condition", "purpose", "current_status", "missing_for_claim", "valid_for_claim"]),
            "## Local Vacuum Source Silence Gate\n" + markdown_table(vacuum, ["vacuum_id", "condition", "effect", "current_status", "gate_pass", "valid_for_claim"]),
            "## Curvature Residual Acquisition Rows\n" + markdown_table(residuals, ["residual_id", "symbol", "meaning", "formula_or_requirement", "current_status", "observable_link", "valid_for_claim"]),
            "## Refusal Runner\n" + markdown_table(refusals, ["refusal_id", "attempted_claim", "runner_result", "blocked_by", "score_eligible", "valid_for_claim"]),
            "## Claim Gates\n" + markdown_table(claims, ["claim_id", "claim", "gate_pass", "reason", "valid_for_claim"]),
            "## Decision Ledger\n" + markdown_table(decisions, ["decision_id", "decision", "reason", "next_action", "valid_for_claim"]),
            "## Next Target\n" + markdown_table(next_targets, ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "## Branch Copies\n" + markdown_table(copies, ["copy_id", "source_path", "target_path", "target_exists", "target_parses", "reason"]),
            "## Validation\n" + markdown_table(validation, ["check_id", "result", "detail"]),
            "## Working Interpretation\n\nThis is the first checkpoint in this mini-chain that gives a possible clean kill for one nasty coupling: `B_Weyl` may be exactly zero by representation/index type, not by wishful thinking. The price is discipline: we need the `R_AB` type certificate. If the field is scalar/trace/Ricci-type with no hidden spurion, the Weyl branch can close. If it is Weyl-type or has hidden projectors, we stop trying to derive zero and bound it instead.",
        ]
    ) + "\n"


def main() -> None:
    remove_pycache()

    source_rows = source_register_rows()
    write_csv(OUTPUTS["source_register"], source_rows)

    split = curvature_split_rows()
    rep = representation_gate_rows()
    diag = diagonalization_rows()
    vacuum = local_vacuum_rows()
    residuals = residual_rows()
    refusals = runner_refusal_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_targets = next_target_rows()

    write_csv(OUTPUTS["curvature_split"], split)
    write_csv(OUTPUTS["representation_gate"], rep)
    write_csv(OUTPUTS["diagonalization"], diag)
    write_csv(OUTPUTS["local_vacuum"], vacuum)
    write_csv(OUTPUTS["residuals"], residuals)
    write_csv(OUTPUTS["runner_refusal"], refusals)
    write_csv(OUTPUTS["claim_gates"], claims)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next_target"], next_targets)

    copies = copy_branch_rows()
    write_csv(OUTPUTS["branch_copies"], copies)

    generated = [
        OUTPUTS["source_register"],
        OUTPUTS["curvature_split"],
        OUTPUTS["representation_gate"],
        OUTPUTS["diagonalization"],
        OUTPUTS["local_vacuum"],
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
        build_doc(source_rows, split, rep, diag, vacuum, residuals, refusals, claims, decisions, next_targets, copies, validation),
        encoding="utf-8",
    )

    if not all(row["result"] == "PASS" for row in validation):
        raise SystemExit("2253 validation failed")

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

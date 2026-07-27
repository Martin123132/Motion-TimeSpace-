from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv"
MICROSCOPE = ROOT / "source-intake" / "microscope"
COEFF = MICROSCOPE / "branch_locked_wep" / "coefficients"
QUARANTINE = MICROSCOPE / "quarantine" / "1480"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1480-Y5-R10-RAB-coefficient-domain-Hom-exclusion-or-same-branch-WEP-delta-w-smoke-runner.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
START_TS = datetime.now(timezone.utc).timestamp()

PREV_NEXT = OUT / "P8_Y5_R10_1479_NEXT_TARGET.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1479_VALIDATION.csv"
PREV_THEOREM = OUT / "P8_Y5_R10_1479_NO_SOURCE_ONLY_ACTION_PREFACTOR_TYPING_THEOREM_ATTEMPT.csv"
PREV_HOM = OUT / "P8_Y5_R10_1479_HOM_SPECIES_TO_SOURCE_PREFACTOR_AUDIT.csv"
PREV_BOUND_INPUTS = OUT / "P8_Y5_R10_1479_DELTA_W_BOUND_INPUT_REQUIREMENTS.csv"
PREV_BOUND_PACK = OUT / "P8_Y5_R10_1479_COMPONENT_DELTA_W_BOUND_PACK_NONCLAIM.csv"
PREV_ANCHORS = OUT / "P8_Y5_R10_1479_DELTA_W_BOUND_ANCHOR_PACK_NONCLAIM.csv"
PREV_FIREWALL = OUT / "P8_Y5_R10_1479_CLAIM_FIREWALL_AND_NO_BOUND_INVERSION.csv"

PFT_1050 = OUT / "P8_Y5_R10_1050_PRODUCT_FUNCTOR_THEOREM_ATTEMPT.csv"
NMM_1051 = OUT / "P8_Y5_R10_1051_NO_MIXED_MORPHISM_LEMMA_ATTEMPT.csv"
ISO_1051 = OUT / "P8_Y5_R10_1051_INVARIANT_SCALAR_OBSTRUCTION_AUDIT.csv"
VOE_1058 = OUT / "P8_Y5_R10_1058_VISIBLE_OPERATOR_DOMAIN_EXHAUSTION_ATTEMPT.csv"
NMF_980 = OUT / "P8_Y5_R10_980_NO_MARKER_FUNCTOR_THEOREM_ATTEMPT.csv"
ODR_1066 = OUT / "P8_Y5_R10_1066_OPERATOR_DOMAIN_RULE_AUDIT.csv"
OLT_1066 = OUT / "P8_Y5_R10_1066_OBJECT_LANGUAGE_TYPING_AUDIT.csv"
OG_1451 = OUT / "P8_Y5_R10_1451_NO_SOURCE_ONLY_SLOT_OPERATOR_GRAMMAR_THEOREM_ATTEMPT.csv"
REQ_1451 = OUT / "P8_Y5_R10_1451_EPSILON_A_BOUND_INPUT_REQUIREMENTS.csv"
ANCH_1451 = OUT / "P8_Y5_R10_1451_ARENA_BOUND_ANCHOR_MAP_NONCLAIM.csv"
PACK_1426 = OUT / "P8_Y5_R10_1426_FINITE_WEP_COEFFICIENT_INPUT_PACK.csv"
EB_1333 = OUT / "P8_Y5_R10_1333_ELECTRON_RESIDUAL_BOUND_CONTRACT.csv"
RSC_1416 = OUT / "P8_Y5_R10_1416_FIRST_RSOURCE_COEFFICIENT_ROW.csv"
CM_1416 = OUT / "P8_Y5_R10_1416_SOURCE_SLOT_COUNTERMODEL_LEDGER.csv"
MAT_983 = OUT / "P8_Y5_R10_983_MATERIAL_CONSTITUENTS.csv"
MAT_1080 = OUT / "P8_Y5_R10_1080_MATERIAL_COMPOSITION_AND_TENSOR_CANDIDATES.csv"
WCM_1053 = OUT / "P8_Y5_R10_1053_WEP_COMPOSITION_CHARGE_MATRIX.csv"
COMP_1232 = OUT / "P8_Y5_R10_1232_COMPONENT_FRACTION_FORMULA_LEDGER.csv"
FSP_1232 = OUT / "P8_Y5_R10_1232_TIPT_COMPONENT_FRACTION_SOURCE_PACK.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1480_SOURCE_REGISTER.csv"
HOM_THEOREM = OUT / "P8_Y5_R10_1480_COEFFICIENT_DOMAIN_HOM_EXCLUSION_ATTEMPT.csv"
HOM_OBSTRUCTIONS = OUT / "P8_Y5_R10_1480_HOM_OBSTRUCTION_LEDGER.csv"
WEP_INPUT_MATRIX = OUT / "P8_Y5_R10_1480_SAME_BRANCH_WEP_DELTA_W_INPUT_MATRIX.csv"
WEP_SMOKE_RESULTS = OUT / "P8_Y5_R10_1480_SAME_BRANCH_WEP_DELTA_W_SMOKE_RESULTS_NONCLAIM.csv"
PROXY_QUARANTINE = OUT / "P8_Y5_R10_1480_PROXY_SMOKE_QUARANTINE_RESULTS.csv"
RUNNER_REJECTION = OUT / "P8_Y5_R10_1480_RUNNER_REJECTION_LEDGER.csv"
REDUCTION_GATES = OUT / "P8_Y5_R10_1480_REDUCTION_GATES.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1480_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1480_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1480_VALIDATION.csv"

QUAR_HOM = QUARANTINE / "COEFFICIENT_DOMAIN_HOM_EXCLUSION_ATTEMPT_NONCLAIM.csv"
QUAR_WEP = QUARANTINE / "SAME_BRANCH_WEP_DELTA_W_SMOKE_RESULTS_NONCLAIM.csv"
BRANCH_HOM = COEFF / "coefficient_domain_Hom_exclusion_attempt_nonclaim_1480.csv"
BRANCH_WEP = COEFF / "same_branch_WEP_delta_w_smoke_results_nonclaim_1480.csv"
BRANCH_GATES = COEFF / "coefficient_domain_Hom_reduction_gates_1480.csv"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def find_row(path: Path, column: str, value: str) -> dict[str, str] | None:
    if not path.exists():
        return None
    for row in read_csv(path):
        if row.get(column) == value:
            return row
    return None


def as_float(value: str | None) -> float | None:
    if value is None:
        return None
    try:
        number = float(value)
    except ValueError:
        return None
    if not math.isfinite(number):
        return None
    return number


def fmt(value: float | None) -> str:
    if value is None:
        return "MISSING_NUMERIC_INPUT"
    return f"{value:.12e}"


def copy_nonclaim(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


def source_rows() -> list[dict[str, Any]]:
    sources = [
        ("SRC1480_0_prev_next", PREV_NEXT, "1479 handoff selecting coefficient-domain Hom exclusion or same-branch WEP smoke runner"),
        ("SRC1480_1_prev_validation", PREV_VALIDATION, "1479 validation baseline"),
        ("SRC1480_2_prev_theorem", PREV_THEOREM, "no-source-only prefactor theorem attempt"),
        ("SRC1480_3_prev_hom", PREV_HOM, "Hom species/source prefactor audit"),
        ("SRC1480_4_prev_bound_inputs", PREV_BOUND_INPUTS, "delta_w bound input requirements"),
        ("SRC1480_5_prev_bound_pack", PREV_BOUND_PACK, "component delta_w bound pack"),
        ("SRC1480_6_prev_anchors", PREV_ANCHORS, "delta_w bound anchor pack"),
        ("SRC1480_7_prev_firewall", PREV_FIREWALL, "claim firewall"),
        ("SRC1480_8_PFT1050", PFT_1050, "product functor theorem attempt"),
        ("SRC1480_9_NMM1051", NMM_1051, "no mixed morphism lemma attempt"),
        ("SRC1480_10_ISO1051", ISO_1051, "invariant scalar obstruction audit"),
        ("SRC1480_11_VOE1058", VOE_1058, "visible operator-domain exhaustion attempt"),
        ("SRC1480_12_NMF980", NMF_980, "no-marker functor theorem attempt"),
        ("SRC1480_13_ODR1066", ODR_1066, "operator-domain rule audit"),
        ("SRC1480_14_OLT1066", OLT_1066, "object-language typing audit"),
        ("SRC1480_15_OG1451", OG_1451, "operator grammar theorem attempt"),
        ("SRC1480_16_REQ1451", REQ_1451, "epsilon_A bound input requirements"),
        ("SRC1480_17_ANCH1451", ANCH_1451, "arena bound anchor map"),
        ("SRC1480_18_PACK1426", PACK_1426, "finite WEP coefficient input pack"),
        ("SRC1480_19_EB1333", EB_1333, "electron residual bound contract"),
        ("SRC1480_20_RSC1416", RSC_1416, "first R_source coefficient row"),
        ("SRC1480_21_CM1416", CM_1416, "source slot countermodel ledger"),
        ("SRC1480_22_local_bounds", LOCAL_BOUNDS, "local bound anchors"),
        ("SRC1480_23_MAT983", MAT_983, "MICROSCOPE material constituents"),
        ("SRC1480_24_MAT1080", MAT_1080, "material composition/tensor candidates"),
        ("SRC1480_25_WCM1053", WCM_1053, "WEP composition charge smoke matrix"),
        ("SRC1480_26_COMP1232", COMP_1232, "component fraction formula ledger"),
        ("SRC1480_27_FSP1232", FSP_1232, "Ti/Pt component fraction source pack"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "source_id": source_id,
            "path_or_url": rel(path),
            "exists": path.exists(),
            "usage": usage,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for source_id, path, usage in sources
    ]


def hom_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "CDH1480_0_target",
            "claim_piece": "coefficient-domain Hom exclusion",
            "formal_statement": "Hom(C_hid or species/source labels, Coeff_source) = Const or absent for active-source coefficients",
            "proof_move": "try to derive coefficient target exhaustion from parent product functor and operator-domain typing",
            "status": "TARGET_EXACT",
            "if_signed": "source-only delta_w coefficients cannot be generated by hidden/species/readout labels",
            "current_blocker": "operator-domain exhaustion is still a contract and scalar invariant obstruction survives",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "CDH1480_1_trivial_hidden_algebra",
            "claim_piece": "trivial hidden invariant algebra route",
            "formal_statement": "If O(C_hid)^inv = R, then any natural scalar coefficient C_hid -> R_+ is constant",
            "proof_move": "reuse NMM1051_1",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "if_signed": "hidden-to-source coefficient maps collapse to common constants",
            "current_blocker": "current corpus has not proved hidden invariant algebra triviality",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "CDH1480_2_target_forbidden",
            "claim_piece": "coefficient target exclusion route",
            "formal_statement": "Even if I_hid exists, source-only coefficient targets are not admissible parent coefficient objects",
            "proof_move": "reuse ODR1066_4 and OG1451_6 as a grammar condition",
            "status": "POWERFUL_CONDITIONAL_NOT_REDUCED",
            "if_signed": "I_hid cannot feed w_A, kappa_A, current rescaling, or source readout weights",
            "current_blocker": "forbidden-target rule is not derived from MTS primitives",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "CDH1480_3_scalar_counterexample",
            "claim_piece": "nonconstant invariant scalar obstruction",
            "formal_statement": "I_hid with dI != 0 permits c(I)=c0+epsilon I and DeltaS=c(I) O_source unless coefficient target is forbidden",
            "proof_move": "reuse NMF980_2, NMM1051_2, ISO1051_0, and VOE1058_3",
            "status": "COUNTEREXAMPLE_PROVED",
            "if_signed": "nothing; this is the live obstruction",
            "current_blocker": "must prove trivial invariant algebra or forbid source coefficient target",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "CDH1480_4_radiative_readout",
            "claim_piece": "bare Hom exclusion must survive EFT/readout",
            "formal_statement": "S_bare no mixed Hom is insufficient unless S_eff and readout maps preserve coefficient-domain exclusion",
            "proof_move": "reuse PFT1050_3 and NMM1051_4",
            "status": "UNSIGNED_CLOSURE",
            "if_signed": "tree-level zero would transfer to WEP/clock/source products",
            "current_blocker": "radiative/readout closure remains unsigned",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "CDH1480_5_verdict",
            "claim_piece": "Hom exclusion proof status",
            "formal_statement": "The coefficient-domain Hom theorem is exact conditional but not parent-derived in the current corpus",
            "proof_move": "refuse theorem-zero and run same-branch WEP smoke as nonclaim",
            "status": "PROOF_NOT_CLOSED_SMOKE_RUNNER_REQUIRED",
            "if_signed": "delta_w source coefficients could become theorem-zero/common-mode",
            "current_blocker": "trivial invariant algebra, forbidden coefficient targets, source label forgetting, and readout closure remain unsigned",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def hom_obstruction_rows() -> list[dict[str, Any]]:
    rows = [
        ("HOB1480_0_scalar_I", "hidden invariant scalar", "I_hid -> c0+epsilon I_hid", "COUNTEREXAMPLE_PROVED", "prove O(C_hid)^inv=R or forbid coefficient target", "NMM1051_2_scalar_counterexample"),
        ("HOB1480_1_species_label", "species/source label", "A -> w_A or kappa_A", "COUNTEREXAMPLE_SURVIVES", "source-label forgetting plus no source-only prefactor syntax", "HOM1479_1_species_to_prefactor"),
        ("HOB1480_2_marker_domain", "material/domain/boundary marker", "marker -> w(marker)", "COUNTEREXAMPLE_SURVIVES", "no-marker/no-extension theorem and readout no-reentry", "NMF980_4_co_moving_marker_extension"),
        ("HOB1480_3_current_label", "current/source normalization label", "J_A -> c_A J_A", "CURRENT_OWNER_UNSIGNED", "Noether/Hilbert current owner and non-Hilbert silence", "RSC1416_1_current_rescaling"),
        ("HOB1480_4_readout_kernel", "readout/source-worldtube label", "post-variation selector -> effective kappa_A", "READOUT_TRANSFER_UNSIGNED", "official source-worldtube/readout transfer closure", "REQ1451_1_WEP;PACK1426_5_K_CMSM"),
        ("HOB1480_5_effective_action", "EFT/radiative coefficient", "S_eff regenerates c(I) O_source", "UNSIGNED_CLOSURE", "radiative/readout closure theorem or finite residual priors", "PFT1050_3_radiative_readout_closure"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "obstruction_id": obstruction_id,
            "domain": domain,
            "map_shape": map_shape,
            "status": status,
            "required_to_close": required,
            "source_anchor": anchor,
            "retained": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for obstruction_id, domain, map_shape, status, required, anchor in rows
    ]


def wep_input_matrix_rows() -> list[dict[str, Any]]:
    rows = [
        ("WIN1480_0_eta_bound", "eta_bound", "R1_WEP_source_charge upper_bound", "2.8e-15", "dimensionless", rel(LOCAL_BOUNDS), "R1_WEP_source_charge", True, "bound anchor only"),
        ("WIN1480_1_C_parent", "C_parent delta_w coefficient vector", "parent coefficient vector in same branch", "MISSING_PARENT_COEFFICIENT", "dimensionless", rel(PACK_1426), "PACK1426_0_C_parent", False, "required for MTS prediction"),
        ("WIN1480_2_R_source", "R_source Earth/source vector", "source worldtube/composition/profile in same parent basis", "MISSING_SOURCE_VECTOR", "dimensionless or declared", rel(PACK_1426), "PACK1426_3_R_source", False, "required for source side"),
        ("WIN1480_3_R_material", "R_TA6V_minus_PtRh10 material tensor", "full parent material response tensor", "PARTIAL_SMOKE_ONLY", "dimensionless", rel(MAT_1080), "MAT1080_4_full_tensor_upgrade", False, "DD smoke rows not full tensor"),
        ("WIN1480_4_K_CMSM", "MICROSCOPE readout/orbit kernel", "official arrays/product convention/readout kernel", "MISSING_OFFICIAL_EXPORT_SURROGATE_ONLY", "dimensionless projection", rel(PACK_1426), "PACK1426_5_K_CMSM", False, "required for tau/readout"),
        ("WIN1480_5_no_cancellation", "component covariance/no-cancellation", "norm/covariance envelope for component vector", "MISSING_NO_CANCELLATION_ENVELOPE", "dimensionless covariance", rel(PREV_BOUND_INPUTS), "BIN1479_4_no_cancellation", False, "required for robustness"),
        ("WIN1480_6_same_branch_lock", "same branch convention", "C_parent, R_source, R_material, K_CMSM, eta bound all share units/sign/basis", "MISSING_SAME_BRANCH_PRODUCT_CONVENTION", "contract", rel(PREV_BOUND_INPUTS), "BIN1479_5_same_branch", False, "prevents unit-kernel claim"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "input_id": input_id,
            "object": obj,
            "definition": definition,
            "current_value": value,
            "units": units,
            "source_path": source,
            "source_anchor": anchor,
            "input_present": present,
            "claim_relevance": relevance,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for input_id, obj, definition, value, units, source, anchor, present, relevance in rows
    ]


def numeric_context() -> dict[str, float | None]:
    r1 = find_row(LOCAL_BOUNDS, "row_id", "R1_WEP_source_charge")
    eb = find_row(EB_1333, "bound_id", "EB1333_0_unit_kernel_electron_prefactor")
    alpha = find_row(WCM_1053, "matrix_id", "WCM1053_4")
    surface = find_row(WCM_1053, "matrix_id", "WCM1053_5")
    eta = as_float(r1.get("upper_bound") if r1 else None)
    delta_f_e = as_float(eb.get("delta_F_e_abs") if eb else None)
    eb_bound = as_float(eb.get("required_abs_coefficient_max") if eb else None)
    delta_alpha = as_float(alpha.get("delta_Q_abs_for_pair") if alpha else None)
    delta_surface = as_float(surface.get("delta_Q_abs_for_pair") if surface else None)
    return {
        "eta": eta,
        "delta_f_e": delta_f_e,
        "electron_bound": eb_bound,
        "delta_alpha": delta_alpha,
        "delta_surface": delta_surface,
        "alpha_bound": eta / delta_alpha if eta is not None and delta_alpha not in (None, 0.0) else None,
        "surface_bound": eta / delta_surface if eta is not None and delta_surface not in (None, 0.0) else None,
    }


def wep_smoke_rows(ctx: dict[str, float | None]) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "smoke_id": "WSR1480_0_same_branch_MTS_claim_grade",
            "row_type": "claim_grade_target",
            "formula": "eta_pred = abs(K_CMSM * R_source dot C_parent dot R_TA6V_minus_PtRh10) with declared covariance/no-cancellation",
            "eta_bound": fmt(ctx["eta"]),
            "available_numeric_inputs": "eta_bound only",
            "computed_value": "NOT_COMPUTED",
            "status": "BLOCKED_MISSING_C_PARENT_R_SOURCE_R_MATERIAL_K_CMSM_COVARIANCE",
            "why_nonclaim": "same-branch product inputs are missing",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "smoke_id": "WSR1480_1_electron_unit_kernel_quarantine",
            "row_type": "proxy_quarantine",
            "formula": "abs(delta_w_e) <= eta_bound / abs(DeltaF_e) under tau_eff=1 and single electron component",
            "eta_bound": fmt(ctx["eta"]),
            "available_numeric_inputs": f"DeltaF_e_abs={fmt(ctx['delta_f_e'])}",
            "computed_value": fmt(ctx["electron_bound"] if ctx["electron_bound"] is not None else (ctx["eta"] / ctx["delta_f_e"] if ctx["eta"] is not None and ctx["delta_f_e"] not in (None, 0.0) else None)),
            "status": "PROXY_COMPUTED_QUARANTINED",
            "why_nonclaim": "unit-kernel electron proxy lacks parent tau/source/readout/product convention",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "smoke_id": "WSR1480_2_DD_alpha_external_quarantine",
            "row_type": "external_smoke_quarantine",
            "formula": "abs(c_alpha_DD) <= eta_bound / abs(DeltaQ_alpha_Coulomb)",
            "eta_bound": fmt(ctx["eta"]),
            "available_numeric_inputs": f"DeltaQ_alpha_abs={fmt(ctx['delta_alpha'])}",
            "computed_value": fmt(ctx["alpha_bound"]),
            "status": "EXTERNAL_DD_SMOKE_COMPUTED_QUARANTINED",
            "why_nonclaim": "DD alpha/Coulomb smoke is not MTS parent basis",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "smoke_id": "WSR1480_3_DD_surface_external_quarantine",
            "row_type": "external_smoke_quarantine",
            "formula": "abs(c_surface_DD) <= eta_bound / abs(DeltaQ_surface_binding)",
            "eta_bound": fmt(ctx["eta"]),
            "available_numeric_inputs": f"DeltaQ_surface_abs={fmt(ctx['delta_surface'])}",
            "computed_value": fmt(ctx["surface_bound"]),
            "status": "EXTERNAL_DD_SMOKE_COMPUTED_QUARANTINED",
            "why_nonclaim": "DD surface/binding smoke is not full MTS material tensor",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "smoke_id": "WSR1480_4_no_cancellation_guard",
            "row_type": "guard",
            "formula": "do not accept any WEP pass unless component covariance or conservative norm is declared",
            "eta_bound": fmt(ctx["eta"]),
            "available_numeric_inputs": "none",
            "computed_value": "NOT_COMPUTED",
            "status": "PASS_GUARD_ACTIVE",
            "why_nonclaim": "prevents cherry-picking component cancellations",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def proxy_quarantine_rows(ctx: dict[str, float | None]) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "proxy_id": "PQ1480_0_electron_unit_kernel",
            "quantity": "epsilon_e_or_delta_w_e proxy",
            "source_path": rel(EB_1333),
            "source_anchor": "EB1333_0_unit_kernel_electron_prefactor",
            "value": fmt(ctx["electron_bound"]),
            "units": "dimensionless proxy coefficient",
            "quarantine_reason": "unit-kernel assumption; no tau_WEP/source/readout normalization",
            "may_seed_future_runner": True,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proxy_id": "PQ1480_1_DD_alpha_smoke",
            "quantity": "external DD alpha/Coulomb coefficient bound",
            "source_path": rel(WCM_1053),
            "source_anchor": "WCM1053_4",
            "value": fmt(ctx["alpha_bound"]),
            "units": "external DD smoke coefficient",
            "quarantine_reason": "external phenomenological basis; not MTS parent source basis",
            "may_seed_future_runner": True,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proxy_id": "PQ1480_2_DD_surface_smoke",
            "quantity": "external DD surface/binding coefficient bound",
            "source_path": rel(WCM_1053),
            "source_anchor": "WCM1053_5",
            "value": fmt(ctx["surface_bound"]),
            "units": "external DD smoke coefficient",
            "quarantine_reason": "external phenomenological basis; not full MTS material tensor",
            "may_seed_future_runner": True,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def rejection_rows() -> list[dict[str, Any]]:
    rows = [
        ("REJ1480_0_parent_basis", "MISSING_PARENT_COUPLING_BASIS", "cannot compare coefficients before delta_w vector basis is declared"),
        ("REJ1480_1_C_parent", "MISSING_PARENT_COEFFICIENT", "no parent coefficient vector or theorem-zero certificate"),
        ("REJ1480_2_R_source", "MISSING_SOURCE_VECTOR", "Earth/source worldtube and composition are not in parent basis"),
        ("REJ1480_3_R_material", "MISSING_FULL_PARENT_MATERIAL_TENSOR", "Ti/Pt material tensor is only composition context plus DD smoke rows"),
        ("REJ1480_4_K_CMSM", "MISSING_READOUT_KERNEL", "official MICROSCOPE/readout/orbit kernel is not imported"),
        ("REJ1480_5_covariance", "MISSING_NO_CANCELLATION_ENVELOPE", "no covariance/norm rule for component cancellations"),
        ("REJ1480_6_same_branch", "MISSING_SAME_BRANCH_PRODUCT_CONVENTION", "unit-kernel/external smoke rows cannot be promoted"),
        ("REJ1480_7_Hom", "HOM_EXCLUSION_NOT_PARENT_DERIVED", "source-only coefficients remain legal residuals"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "rejection_id": rejection_id,
            "blocking_marker": marker,
            "reason": reason,
            "blocks_claim": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for rejection_id, marker, reason in rows
    ]


def gate_rows(
    hom_rows: list[dict[str, Any]],
    obstruction_rows: list[dict[str, Any]],
    input_rows: list[dict[str, Any]],
    smoke_rows: list[dict[str, Any]],
    proxy_rows: list[dict[str, Any]],
    rejection: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    conditional = any(row["theorem_id"] == "CDH1480_1_trivial_hidden_algebra" and row["status"] == "EXACT_CONDITIONAL_THEOREM" for row in hom_rows)
    proof_refused = any(row["theorem_id"] == "CDH1480_5_verdict" and row["status"] == "PROOF_NOT_CLOSED_SMOKE_RUNNER_REQUIRED" for row in hom_rows)
    obstructions_retained = all(row["retained"] for row in obstruction_rows)
    same_branch_blocked = any(row["smoke_id"] == "WSR1480_0_same_branch_MTS_claim_grade" and row["status"].startswith("BLOCKED") for row in smoke_rows)
    proxies_quarantined = all(not row["score_ready"] and not row["valid_for_claim"] for row in proxy_rows)
    inputs_missing = any(not row["input_present"] for row in input_rows)
    rejection_complete = all(row["blocks_claim"] for row in rejection)
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1480_0_Hom_conditional",
            "gate": "coefficient-domain Hom exclusion has exact conditional routes",
            "gate_pass": conditional,
            "claim_effect": "contract support only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1480_1_Hom_refused",
            "gate": "Hom theorem-zero promotion refused",
            "gate_pass": proof_refused,
            "claim_effect": "source coefficients stay live",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1480_2_obstructions_retained",
            "gate": "scalar/species/marker/current/readout obstructions retained",
            "gate_pass": obstructions_retained,
            "claim_effect": "no local-GR/GR source universality claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1480_3_same_branch_runner_blocked",
            "gate": "same-branch WEP MTS row is blocked",
            "gate_pass": same_branch_blocked and inputs_missing,
            "claim_effect": "runner exists but refuses score",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1480_4_proxies_quarantined",
            "gate": "electron/DD proxy rows are quarantine only",
            "gate_pass": proxies_quarantined,
            "claim_effect": "no proxy promoted as MTS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1480_5_rejection_complete",
            "gate": "runner rejection ledger covers all missing claim inputs",
            "gate_pass": rejection_complete,
            "claim_effect": "claim firewall active",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1480_0_Hom_status",
            "decision": "coefficient-domain Hom exclusion remains exact conditional, not parent-derived",
            "reason": "scalar invariant obstruction and forbidden-target/radiative-readout rules remain unsigned",
            "consequence": "delta_w source coefficients remain live residuals",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1480_1_runner_status",
            "decision": "same-branch WEP runner is built but refuses the MTS score",
            "reason": "C_parent, R_source, full Ti/Pt material tensor, K_CMSM, covariance, and product convention are missing",
            "consequence": "only proxy/quarantine rows are computed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1480_2_next_step",
            "decision": "fill the same-branch WEP material/readout pack next",
            "reason": "it is now the shortest empirical path while Hom derivation remains unsigned",
            "consequence": "1481 should acquire/source Ti/Pt tensor, tau/readout, covariance, and source vector rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1480_0_1481",
            "next_target": "1481-Y5-R10-RAB-same-branch-WEP-material-tau-source-pack-or-Hom-parent-generator-proof.md",
            "script": "scripts/Y5_R10_RAB_same_branch_WEP_material_tau_source_pack_or_Hom_parent_generator_proof.py",
            "objective": "try to source/fill the same-branch WEP material tensor, source vector, tau/readout kernel, covariance/no-cancellation, and product convention; if blocked, sharpen the parent-generator proof needed for coefficient-domain Hom exclusion",
            "include": "MICROSCOPE Ti/Pt tensor; source worldtube; K_CMSM/readout; tau_WEP; eta bound; component vector placeholders; proxy quarantine checks",
            "exclude": "GitHub action; formalization-workbench edits; WEP/local-GR claim promotion; unit-kernel or DD-smoke promotion; bound inversion",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    hom_rows: list[dict[str, Any]],
    obstruction_rows: list[dict[str, Any]],
    input_rows: list[dict[str, Any]],
    smoke_rows: list[dict[str, Any]],
    proxy_rows: list[dict[str, Any]],
    rejection: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated_paths = [
        SOURCE_REGISTER,
        HOM_THEOREM,
        HOM_OBSTRUCTIONS,
        WEP_INPUT_MATRIX,
        WEP_SMOKE_RESULTS,
        PROXY_QUARANTINE,
        RUNNER_REJECTION,
        REDUCTION_GATES,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    csv_parse_ok = True
    for path in generated_paths:
        try:
            parse_csv(path)
        except Exception:
            csv_parse_ok = False

    branch_copies = all(path.exists() for path in [QUAR_HOM, QUAR_WEP, BRANCH_HOM, BRANCH_WEP, BRANCH_GATES])
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_untouched = not any(
        file.stat().st_mtime >= START_TS
        for file in FORMALIZATION.rglob("*")
        if file.is_file()
    ) if FORMALIZATION.exists() else True

    hom_conditional = any(row["theorem_id"] == "CDH1480_1_trivial_hidden_algebra" and row["status"] == "EXACT_CONDITIONAL_THEOREM" for row in hom_rows)
    hom_refused = any(row["theorem_id"] == "CDH1480_5_verdict" and row["status"] == "PROOF_NOT_CLOSED_SMOKE_RUNNER_REQUIRED" for row in hom_rows)
    obstructions_retained = all(row["retained"] for row in obstruction_rows)
    input_matrix_blocks = any(not row["input_present"] for row in input_rows)
    same_branch_blocked = any(row["smoke_id"] == "WSR1480_0_same_branch_MTS_claim_grade" and row["status"].startswith("BLOCKED") for row in smoke_rows)
    proxy_numeric = all(row["value"] != "MISSING_NUMERIC_INPUT" for row in proxy_rows)
    proxy_nonclaim = all(not row["score_ready"] and not row["valid_for_claim"] and not row["claim_allowed"] for row in proxy_rows)
    rejection_blocks = all(row["blocks_claim"] and not row["claim_allowed"] for row in rejection)
    gate_claim_false = all(not row["valid_for_claim"] and not row["claim_allowed"] for row in gates)

    checks = [
        ("VAL1480_0_sources", all(row["exists"] for row in sources), "all cited local source paths exist"),
        ("VAL1480_1_Hom_conditional", hom_conditional, "Hom exclusion conditional theorem route recorded"),
        ("VAL1480_2_Hom_refused", hom_refused, "Hom theorem-zero promotion refused"),
        ("VAL1480_3_obstructions_retained", obstructions_retained, "scalar/species/marker/current/readout obstructions retained"),
        ("VAL1480_4_input_matrix_blocks", input_matrix_blocks, "same-branch WEP input matrix contains missing blockers"),
        ("VAL1480_5_same_branch_blocked", same_branch_blocked, "claim-grade MTS WEP smoke row refuses score"),
        ("VAL1480_6_proxy_numeric", proxy_numeric, "quarantine proxy rows compute numeric smoke values"),
        ("VAL1480_7_proxy_nonclaim", proxy_nonclaim, "proxy rows remain nonclaim"),
        ("VAL1480_8_rejection_blocks", rejection_blocks, "runner rejection ledger blocks claim"),
        ("VAL1480_9_gate_claim_false", gate_claim_false, "all gates keep claim flags false"),
        ("VAL1480_10_generated_csv_parse", csv_parse_ok, "all generated 1480 CSVs parse cleanly"),
        ("VAL1480_11_branch_copies", branch_copies, "nonclaim branch/quarantine copies written"),
        ("VAL1480_12_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1480_13_formalization_untouched", formalization_untouched, "formalization modified-file count since start=0"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "generated_utc": now(),
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1480_14_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1480 refuses Hom theorem-zero and builds same-branch WEP smoke runner with quarantined proxy values",
            "generated_utc": now(),
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    hom_rows: list[dict[str, Any]],
    obstruction_rows: list[dict[str, Any]],
    input_rows: list[dict[str, Any]],
    smoke_rows: list[dict[str, Any]],
    proxy_rows: list[dict[str, Any]],
    rejection: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> None:
    lines: list[str] = []
    lines.append("# 1480 — R10/RAB Coefficient-Domain Hom Exclusion Or Same-Branch WEP Delta-w Smoke Runner")
    lines.append("")
    lines.append("## Verdict")
    lines.append("- Coefficient-domain `Hom(C_hid/species, Coeff_source)=Const/absent` is still exact conditional, not parent-derived.")
    lines.append("- The scalar invariant counterexample survives: one untrivialized hidden/local scalar can feed a source coefficient unless the target is forbidden.")
    lines.append("- The same-branch WEP runner is now explicit and refuses the claim-grade MTS score; only electron/DD proxy rows are computed, quarantined, and nonclaim.")
    lines.append("")
    lines.append("## Hom Exclusion Attempt")
    lines.append("| theorem_id | status | current_blocker |")
    lines.append("|---|---|---|")
    for row in hom_rows:
        lines.append(f"| {row['theorem_id']} | {row['status']} | {row['current_blocker']} |")
    lines.append("")
    lines.append("## Hom Obstructions")
    lines.append("| obstruction_id | status | required_to_close |")
    lines.append("|---|---|---|")
    for row in obstruction_rows:
        lines.append(f"| {row['obstruction_id']} | {row['status']} | {row['required_to_close']} |")
    lines.append("")
    lines.append("## Same-Branch WEP Inputs")
    lines.append("| input_id | object | current_value | input_present |")
    lines.append("|---|---|---|---:|")
    for row in input_rows:
        lines.append(f"| {row['input_id']} | {row['object']} | {row['current_value']} | {row['input_present']} |")
    lines.append("")
    lines.append("## WEP Smoke Results")
    lines.append("| smoke_id | status | computed_value | why_nonclaim |")
    lines.append("|---|---|---|---|")
    for row in smoke_rows:
        lines.append(f"| {row['smoke_id']} | {row['status']} | {row['computed_value']} | {row['why_nonclaim']} |")
    lines.append("")
    lines.append("## Proxy Quarantine")
    lines.append("| proxy_id | value | quarantine_reason |")
    lines.append("|---|---|---|")
    for row in proxy_rows:
        lines.append(f"| {row['proxy_id']} | {row['value']} | {row['quarantine_reason']} |")
    lines.append("")
    lines.append("## Rejection Ledger")
    lines.append("| rejection_id | blocking_marker | reason |")
    lines.append("|---|---|---|")
    for row in rejection:
        lines.append(f"| {row['rejection_id']} | {row['blocking_marker']} | {row['reason']} |")
    lines.append("")
    lines.append("## Gates")
    lines.append("| gate_id | gate_pass | claim_effect |")
    lines.append("|---|---:|---|")
    for row in gates:
        lines.append(f"| {row['gate_id']} | {row['gate_pass']} | {row['claim_effect']} |")
    lines.append("")
    lines.append("## Decision Ledger")
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} — {row['consequence']}.")
    lines.append("")
    lines.append("## Validation")
    lines.append("| check_id | result | detail |")
    lines.append("|---|---|---|")
    for row in validation:
        lines.append(f"| {row['check_id']} | {row['result']} | {row['detail']} |")
    lines.append("")
    lines.append("## Source Register")
    lines.append("| source_id | exists | path_or_url | usage |")
    lines.append("|---|---:|---|---|")
    for row in sources:
        lines.append(f"| {row['source_id']} | {row['exists']} | `{row['path_or_url']}` | {row['usage']} |")
    lines.append("")
    lines.append("## Next Target")
    for row in next_target:
        lines.append(f"- `{row['next_target']}` via `{row['script']}`: {row['objective']}")
    lines.append("")
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    sources = source_rows()
    hom_rows = hom_theorem_rows()
    obstruction_rows = hom_obstruction_rows()
    input_rows = wep_input_matrix_rows()
    ctx = numeric_context()
    smoke_rows = wep_smoke_rows(ctx)
    proxy_rows = proxy_quarantine_rows(ctx)
    rejection = rejection_rows()
    gates = gate_rows(hom_rows, obstruction_rows, input_rows, smoke_rows, proxy_rows, rejection)
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(HOM_THEOREM, hom_rows)
    write_csv(HOM_OBSTRUCTIONS, obstruction_rows)
    write_csv(WEP_INPUT_MATRIX, input_rows)
    write_csv(WEP_SMOKE_RESULTS, smoke_rows)
    write_csv(PROXY_QUARANTINE, proxy_rows)
    write_csv(RUNNER_REJECTION, rejection)
    write_csv(REDUCTION_GATES, gates)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_target)

    copy_nonclaim(HOM_THEOREM, QUAR_HOM)
    copy_nonclaim(WEP_SMOKE_RESULTS, QUAR_WEP)
    copy_nonclaim(HOM_THEOREM, BRANCH_HOM)
    copy_nonclaim(WEP_SMOKE_RESULTS, BRANCH_WEP)
    copy_nonclaim(REDUCTION_GATES, BRANCH_GATES)

    validation = validation_rows(sources, hom_rows, obstruction_rows, input_rows, smoke_rows, proxy_rows, rejection, gates)
    write_csv(VALIDATION, validation)
    write_doc(sources, hom_rows, obstruction_rows, input_rows, smoke_rows, proxy_rows, rejection, gates, decisions, validation, next_target)
    print("Y5_R10_1480_Hom_conditional_same_branch_WEP_smoke_nonclaim")


if __name__ == "__main__":
    main()

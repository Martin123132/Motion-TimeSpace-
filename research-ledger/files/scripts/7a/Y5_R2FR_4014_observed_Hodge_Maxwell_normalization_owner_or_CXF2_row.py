from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "4014"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "4014-Y5-R2FR-observed-Hodge-Maxwell-normalization-owner-or-CXF2-row.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_4014_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_4014_OBSERVED_HODGE_MAXWELL_OWNER_THEOREM.csv",
    "audit": SRC / "P8_Y5_R2FR_4014_EM_OWNER_AUDIT.csv",
    "finite": SRC / "P8_Y5_R2FR_4014_HODGE_F2_CURRENT_FINITE_ROWS.csv",
    "cases": SRC / "P8_Y5_R2FR_4014_EVALUATOR_CASES.csv",
    "results": SRC / "P8_Y5_R2FR_4014_EVALUATOR_RESULTS.csv",
    "decision": SRC / "P8_Y5_R2FR_4014_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_4014_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_4014_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_4014_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_4014_VALIDATION.csv",
}

NEXT_DOC = "4015-Y5-R2FR-Gauss-Poisson-Gref-source-normalization-or-Newton-row.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_4015_Gauss_Poisson_Gref_source_normalization_or_Newton_row.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC4014_00_handoff", SRC / "P8_Y5_R2FR_4013_NEXT_TARGET.csv", "NEXT4013_0", "4013 handoff"),
        ("SRC4014_01_4013_stress", SRC / "P8_Y5_R2FR_4013_MAXWELL_POYNTING_ONCE_ONLY_THEOREM.csv", "MPE4013_1_Maxwell_Hilbert_stress", "4013 Maxwell stress inclusion"),
        ("SRC4014_02_4013_vector", SRC / "P8_Y5_R2FR_4013_MAXWELL_POYNTING_ONCE_ONLY_THEOREM.csv", "MPE4013_6_finite_EM_vector", "4013 EM finite vector"),
        ("SRC4014_03_4013_hodge_audit", SRC / "P8_Y5_R2FR_4013_EM_STRESS_SOURCE_AUDIT.csv", "ESA4013_0_same_observed_coframe", "4013 observed Hodge audit"),
        ("SRC4014_04_4013_norm_audit", SRC / "P8_Y5_R2FR_4013_EM_STRESS_SOURCE_AUDIT.csv", "ESA4013_1_unique_Maxwell_normalization", "4013 normalization audit"),
        ("SRC4014_05_4013_Delta_Hodge", SRC / "P8_Y5_R2FR_4013_EM_ONCE_ONLY_FINITE_ROWS.csv", "EMO4013_3_Delta_Hodge_EM", "4013 Delta_Hodge row"),
        ("SRC4014_06_4013_wEM", SRC / "P8_Y5_R2FR_4013_EM_ONCE_ONLY_FINITE_ROWS.csv", "EMO4013_4_wEM_CJQ", "4013 wEM/CJQ row"),
        ("SRC4014_07_4013_CXF2", SRC / "P8_Y5_R2FR_4013_EM_ONCE_ONLY_FINITE_ROWS.csv", "EMO4013_5_CXF2", "4013 CXF2 row"),
        ("SRC4014_08_4013_decision", SRC / "P8_Y5_R2FR_4013_DECISION_GATE.csv", "DEC4013_3_next", "4013 next decision"),
        ("SRC4014_09_DHB_master", SRC / "P8_EM_Hodge_flow_rule_bound_or_zero.csv", "DHB3504_0_Delta_Hodge_EM", "Delta_Hodge master"),
        ("SRC4014_10_DHB_principal", SRC / "P8_EM_Hodge_flow_rule_bound_or_zero.csv", "DHB3504_1_principal_cone", "principal cone row"),
        ("SRC4014_11_DHB_skewon", SRC / "P8_EM_Hodge_flow_rule_bound_or_zero.csv", "DHB3504_2_skewon", "skewon row"),
        ("SRC4014_12_DHB_axion", SRC / "P8_EM_Hodge_flow_rule_bound_or_zero.csv", "DHB3504_3_axion_gradient", "axion gradient row"),
        ("SRC4014_13_DHB_hidden", SRC / "P8_EM_Hodge_flow_rule_bound_or_zero.csv", "DHB3504_4_hidden_disformal_hodge", "hidden Hodge row"),
        ("SRC4014_14_DHB_readout", SRC / "P8_EM_Hodge_flow_rule_bound_or_zero.csv", "DHB3504_5_readout_hodge", "readout Hodge row"),
        ("SRC4014_15_DHB_conformal", SRC / "P8_EM_Hodge_flow_rule_bound_or_zero.csv", "DHB3504_6_conformal_scale_residual", "conformal scale guard"),
        ("SRC4014_16_EMB_Hodge", SRC / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv", "EMB3503_0_Delta_Hodge_EM", "Hodge/current bound vector"),
        ("SRC4014_17_EMB_wEM", SRC / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv", "EMB3503_1_w_EM", "w_EM bound vector"),
        ("SRC4014_18_EMB_CXF2", SRC / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv", "EMB3503_2_C_XF2", "C_XF2 bound vector"),
        ("SRC4014_19_EMB_CJQ", SRC / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv", "EMB3503_3_C_JQ", "C_JQ bound vector"),
        ("SRC4014_20_VEB_domain", SRC / "P8_EM_visible_action_domain_exhaustion_no_chiEM_bound_vector.csv", "VEB3505_0_Delta_Hodge_EM", "visible EM domain master"),
        ("SRC4014_21_VEB_principal", SRC / "P8_EM_visible_action_domain_exhaustion_no_chiEM_bound_vector.csv", "VEB3505_1_Delta_chi_principal", "visible principal row"),
        ("SRC4014_22_VEB_CXF2", SRC / "P8_EM_visible_action_domain_exhaustion_no_chiEM_bound_vector.csv", "VEB3505_6_C_XF2", "visible C_XF2 row"),
        ("SRC4014_23_scalar_status", SRC / "P8_EM_scalar_gauge_coupling_owner_status.csv", "STAT3526_1_zero_theorem", "scalar gauge zero theorem status"),
        ("SRC4014_24_alpha_no_go", SRC / "P8_EM_alpha_level_current_owner_status.csv", "STAT3527_1_no_go", "compact U1 no-go"),
        ("SRC4014_25_visible_status", SRC / "P8_EM_visible_EM_first_owner_branch_status.csv", "STAT3525_1_reduction", "visible EM reduction status"),
        ("SRC4014_26_3960_hidden", SRC / "P8_Y5_R2FR_3960_EM_POYNTING_F2_GATE.csv", "EMG3960_2_hidden_F2", "hidden F2 gate"),
        ("SRC4014_27_3961_hidden_law", SRC / "P8_Y5_R2FR_3961_HIDDEN_EM_VARIATION_LAW.csv", "HEV3961_1_source_current", "hidden EM source current law"),
        ("SRC4014_28_3961_sigma", SRC / "P8_Y5_R2FR_3961_SIGMA_FACTOR_EM_EXCLUSION_GATE.csv", "SFE3961_2_no_hidden_visible_Hom", "no hidden visible Hom gate"),
        ("SRC4014_29_3962_Hodge_lock", SRC / "P8_Y5_R2FR_3962_HODGE_OWNER_LOCK_OR_BOUND.csv", "HOL3962_0_lock_condition", "Hodge owner lock"),
        ("SRC4014_30_3962_norm_owner", SRC / "P8_Y5_R2FR_3962_HODGE_OWNER_LOCK_OR_BOUND.csv", "HOL3962_3_normalization_owner", "normalization owner lock"),
        ("SRC4014_31_3962_vector", SRC / "P8_Y5_R2FR_3962_EM_RESIDUAL_VECTOR.csv", "EMV3962_2_hidden_F2", "3962 hidden F2 vector"),
        ("SRC4014_32_3994_no_extra", SRC / "P8_Y5_R2FR_3994_NO_EXTRA_F2_OPERATOR_DOMAIN_THEOREM.csv", "F2G3994_1_no_extra_F2_zero", "3994 no extra F2 theorem"),
        ("SRC4014_33_3994_identity", SRC / "P8_Y5_R2FR_3994_NO_EXTRA_F2_OPERATOR_DOMAIN_THEOREM.csv", "F2G3994_2_canonical_identity", "3994 F2/current identity"),
        ("SRC4014_34_3503_owner", SRC / "P8_Y5_R2FR_3503_OBSERVED_HODGE_MAXWELL_OWNER_THEOREM.csv", "OHM3503_0_same_observed_Hodge", "3503 same observed Hodge"),
        ("SRC4014_35_3503_current", SRC / "P8_Y5_R2FR_3503_OBSERVED_HODGE_MAXWELL_OWNER_THEOREM.csv", "OHM3503_2_charge_current_owner", "3503 charge/current owner"),
        ("SRC4014_36_3504_unique", SRC / "P8_Y5_R2FR_3504_HODGE_UNIQUENESS_THEOREM.csv", "HFR3504_1_hodge_uniqueness", "3504 Hodge uniqueness"),
        ("SRC4014_37_3504_conformal", SRC / "P8_Y5_R2FR_3504_HODGE_UNIQUENESS_THEOREM.csv", "HFR3504_4_conformal_caveat", "3504 conformal caveat"),
        ("SRC4014_38_3505_domain", SRC / "P8_Y5_R2FR_3505_VISIBLE_EM_ACTION_DOMAIN_THEOREM.csv", "VEM3505_1_exact_typed_exclusion", "3505 typed domain exclusion"),
        ("SRC4014_39_3506_signature", SRC / "P8_Y5_R2FR_3506_PARENT_VISIBLE_EM_GENERATOR_SIGNATURE.csv", "GEN3506_5_scalar_gauge_kinetic_owner", "3506 scalar gauge kinetic owner"),
        ("SRC4014_40_3507_identity", SRC / "P8_Y5_R2FR_3507_ALPHA_COUPLING_IDENTITY.csv", "ALPHA3507_1_vertical_residual_law", "3507 alpha identity"),
        ("SRC4014_41_3862_zero", SRC / "P8_Y5_R2FR_3862_EM_HODGE_ZERO_THEOREM.csv", "EHZ3862_1_observed_Hodge_zero", "3862 observed Hodge zero"),
        ("SRC4014_42_3862_scale", SRC / "P8_Y5_R2FR_3862_EM_HODGE_OBSERVABLE_BOUND.csv", "EHB3862_3_EM_scale_gate", "3862 EM scale gate"),
        ("SRC4014_43_3863_owner", SRC / "P8_Y5_R2FR_3863_MAXWELL_NORMALIZATION_OWNER_THEOREM.csv", "MNO3863_2_normalization_owner_theorem", "3863 normalization owner theorem"),
        ("SRC4014_44_3864_no_extra", SRC / "P8_Y5_R2FR_3864_NO_EXTRA_F2_THEOREM.csv", "NEF3864_1_no_extra_F2_theorem", "3864 no extra F2 theorem"),
        ("SRC4014_45_3864_identity", SRC / "P8_Y5_R2FR_3864_LAMBDAF2_BOUND.csv", "LFB3864_0_canonical_identity", "3864 lambda F2 identity"),
        ("SRC4014_46_3995_tri", SRC / "P8_Y5_R2FR_3995_CURRENT_NORMALIZATION_GAUGE_TRICHOTOMY.csv", "TRI3995_0_rescaling_covariance", "3995 current normalization trichotomy"),
        ("SRC4014_47_3995_bound", SRC / "P8_Y5_R2FR_3995_JOINT_ALPHA_F2_CURRENT_BOUND_ROWS.csv", "JAB3995_0_invariant_identity", "3995 alpha/F2/current bound identity"),
        ("SRC4014_48_3996_product", SRC / "P8_Y5_R2FR_3996_BALPHA_SOURCE_PRODUCT_VECTOR.csv", "BSP3996_0_invariant_source_product", "3996 b_alpha source product"),
        ("SRC4014_49_4008_label_forget", SRC / "P8_Y5_R2FR_4008_SOURCE_LABEL_FORGETTING_CONSTRUCTOR_PACKET.csv", "SLF4008_2_constants", "4008 fixed representation constants"),
        ("SRC4014_50_1057_subblock", SRC / "P8_Y5_R10_1057_UNIQUE_MAXWELL_SUBBLOCK_THEOREM_ATTEMPT.csv", "UMS1057_2_no_independent_F2", "1057 no independent F2"),
        ("SRC4014_51_1100_norm", SRC / "P8_Y5_R10_1100_ALPHA_NORMALIZATION_DECOMPOSITION.csv", "Z1100_4_total", "1100 alpha normalization ledger"),
        ("SRC4014_52_1235_typed", SRC / "P8_Y5_R10_1235_UNIQUE_F2_TYPED_COEFFICIENT_DOMAIN_PROOF_ATTEMPT.csv", "UF21235_1_typed_domain_route", "1235 typed domain route"),
        ("SRC4014_53_1467_owner", SRC / "P8_Y5_R10_1467_UNIQUE_EM_OWNER_NO_HIDDEN_F2_PROOF_ATTEMPT.csv", "UEO1467_1_F2_coefficient", "1467 unique EM owner F2 coefficient"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in source_specs():
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "needle": needle,
                "exists": path.exists(),
                "needle_found": needle in text,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "OHN4014_0_observed_Hodge_lock",
            "claim_piece": "observed Hodge owner",
            "mathematical_form": "Args(S_EM)={A_Q,F_Q=dA_Q,e_obs(q),orientation,fixed representation data,fixed constants} implies *_EM=*_obs[e_obs(q)] and Delta_Hodge_EM=0",
            "derived_result": "Hodge ownership follows from typed action-domain exhaustion plus metric/orientation uniqueness; it does not follow from gauge symmetry alone",
            "status": "EXACT_CONDITIONAL_TYPED_DOMAIN_THEOREM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "OHN4014_1_constitutive_residual_split",
            "claim_piece": "Hodge/constitutive mismatch vector",
            "mathematical_form": "Delta_Hodge_EM <= Delta_chi_principal + Delta_chi_skewon + L|d theta_EM| + C_Hodge_hidden + C_Hodge_readout + Delta_orientation_flux",
            "derived_result": "if the typed-domain theorem is not adopted, every allowed constitutive escape route is retained separately with no cancellation credit",
            "status": "FINITE_CONSTITUTIVE_SPLIT_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "OHN4014_2_parent_Maxwell_normalization",
            "claim_piece": "Maxwell kinetic normalization owner",
            "mathematical_form": "F_parent=F_Q T_Q+F_perp and <T_Q,T_Q>_P=N_Q fixed imply Z_Q=C_P N_Q; if C_P,N_Q and T_Q are q-basic/fixed then D_v ln Z_Q=0",
            "derived_result": "a parent curvature norm can silence local Maxwell-normalization drift, but it does not predict the absolute alpha value unless constants/units are also derived",
            "status": "EXACT_CONDITIONAL_SUBBLOCK_THEOREM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "OHN4014_3_no_extra_F2_operator_domain",
            "claim_piece": "no hidden or independent F2 coefficient",
            "mathematical_form": "Allowed[S_vis]=Image(ParentGenerate) contains Q-subblock only as C_P N_Q F_Q^2, with no Coeff(F_Q^2) object and no Hom(hidden,Coeff(F_Q^2)) except constants/q-basic data",
            "derived_result": "C_XF2=0 only if the parent object language has no visible-hidden coefficient slot; diffeomorphism plus U(1) gauge invariance alone explicitly fails",
            "status": "EXACT_CONDITIONAL_NO_EXTRA_F2_THEOREM_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "OHN4014_4_charge_current_normalization",
            "claim_piece": "current and charge normalization owner",
            "mathematical_form": "A_Q -> e^sigma A_Q gives z_g -> z_g-Dsigma and s_XF2 -> s_XF2-2Dsigma, while b_alpha=2z_g-s_XF2 is invariant; same-current owner permits z_g=0 gauge",
            "derived_result": "z_g and s_XF2 separately are convention-dependent until the current owner is fixed; b_alpha is the physical invariant source-coupling throat",
            "status": "EXACT_RESCALE_INVARIANT_IDENTITY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "OHN4014_5_conformal_scale_guard",
            "claim_piece": "4D conformal Hodge caveat",
            "mathematical_form": "g_EM=Omega^2 g_obs leaves the Hodge star on two-forms invariant in 4D, so light-cone/Hodge agreement does not fix clock/source normalization, alpha, impedance, or G_ref M_H",
            "derived_result": "matching EM cones is not enough for source coupling; the scale/normalization rows remain necessary",
            "status": "ANTI_OVERCLAIM_GUARD",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "OHN4014_6_full_EM_owner_branch",
            "claim_piece": "EM owner local-silence branch",
            "mathematical_form": "Delta_Hodge_EM=w_EM-1=C_JQ=C_XF2=C_EM_readout=0 if observed Hodge, parent curvature norm, no-extra-F2 domain, same-current owner, fixed representation constants and radiative/readout closure are all signed",
            "derived_result": "the local EM contribution can be parent-owned and locally silent as an extra coupling, but current corpus does not sign the whole package",
            "status": "EXACT_CONDITIONAL_FULL_GATE_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "OHN4014_7_finite_owner_vector",
            "claim_piece": "finite fallback if EM owner fails",
            "mathematical_form": "epsilon_EM_owner_4014 <= |Delta_Hodge_EM|+|Delta_chi_principal|+|Delta_chi_skewon|+L|dtheta_EM|+|C_Hodge_hidden|+|C_Hodge_readout|+|Delta_conformal_scale|+|w_EM-1|+|C_JQ|+|C_XF2|+|b_alpha|+|C_EM_readout|+|delta_lambda_rad|",
            "derived_result": "all live Hodge, F2, current and alpha-normalization escape routes become explicit residual rows with observable links",
            "status": "FINITE_EM_OWNER_VECTOR_DERIVED_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def audit_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "EOA4014_0_action_domain",
            "clause": "visible EM action arguments are exhausted by A_Q,F_Q,e_obs(q),orientation,fixed representation data and constants",
            "current_status": "EXACT_ROUTE_NOT_PARENT_SIGNED",
            "risk_if_open": "independent chi_EM, hidden Hodge maps or readout Hodge fields can enter",
            "next_action": "adopt parent visible action-domain certificate or retain Delta_Hodge_EM components",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "EOA4014_1_parent_curvature_norm",
            "clause": "Maxwell kinetic coefficient descends from one parent curvature norm with fixed generator norm",
            "current_status": "CONDITIONAL_SUBBLOCK_OWNER_UNSIGNED",
            "risk_if_open": "w_EM rescales Hilbert source stress and alpha/source normalization",
            "next_action": "derive C_P,N_Q,T_Q fixedness or keep w_EM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "EOA4014_2_no_extra_F2",
            "clause": "no independent Coeff(F_Q^2), no hidden-to-F2 Hom, no radiative/readout regenerated F2 slot",
            "current_status": "KEY_BLOCKER_SYMMETRY_ALONE_FAILS",
            "risk_if_open": "C_XF2 becomes direct alpha/clock/WEP/R10/source-coupling pressure",
            "next_action": "prove typed object-domain exclusion or retain C_XF2 and b_alpha rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "EOA4014_3_same_current_owner",
            "clause": "A_Q,J_Q,representation charges and matter current are fixed by one parent current owner before readout",
            "current_status": "PARTIAL_ROUTE_NOT_JOINTLY_SIGNED",
            "risk_if_open": "C_JQ and z_g become physical source-slot residuals rather than gauge choice",
            "next_action": "bind current owner to 4008 fixed representation constants or keep C_JQ/z_g",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "EOA4014_4_conformal_scale",
            "clause": "Hodge/cone agreement is supplemented by clock/source/impedance normalization",
            "current_status": "CONFORMAL_CAVEAT_ACTIVE",
            "risk_if_open": "EM light-cone success is overread as source normalization success",
            "next_action": "route source-scale/G_ref normalization to 4015",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "EOA4014_5_radiative_readout_closure",
            "clause": "loops, thresholds, spectroscopy/readout and radiative closure preserve visible EM domain",
            "current_status": "READOUT_RADIATIVE_CLOSURE_OPEN",
            "risk_if_open": "C_EM_readout or delta_lambda_rad regenerate alpha/source response after tree-level proof",
            "next_action": "keep readout/radiative terms in finite vector until closure is derived",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "EOA4014_6_absolute_alpha_guard",
            "clause": "local drift silence is separated from absolute alpha/mu0 prediction",
            "current_status": "GUARD_ACTIVE",
            "risk_if_open": "conditional local constancy is oversold as deriving the numerical fine-structure constant",
            "next_action": "label absolute constants as calibration debt unless parent units/constants are derived",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def finite_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "EMOWN4014_0_master",
            "coefficient": "epsilon_EM_owner_4014",
            "formula": "|Delta_Hodge_EM|+|Delta_chi_principal|+|Delta_chi_skewon|+L|dtheta_EM|+|C_Hodge_hidden|+|C_Hodge_readout|+|Delta_conformal_scale|+|w_EM-1|+|C_JQ|+|C_XF2|+|b_alpha|+|C_EM_readout|+|delta_lambda_rad|",
            "value": "MISSING_PARENT_SIGNED_OR_NUMERIC_COMPONENTS",
            "units": "dimensionless_or_tensor_owner_norm",
            "source_status": "FINITE_VECTOR_NONCLAIM",
            "observable_links": "Maxwell light cone; alpha; clocks; WEP; R10; PPN; Newton source normalization",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EMOWN4014_1_Delta_Hodge_EM",
            "coefficient": "Delta_Hodge_EM",
            "formula": "*_EM - *_obs[e_obs(q)] or chi_EM - chi_obs",
            "value": "ZERO_IF_VISIBLE_ACTION_DOMAIN_EXHAUSTED_ELSE_COMPONENT_BOUND_REQUIRED",
            "units": "dimensionless_or_tensor",
            "source_status": "OBSERVED_HODGE_OWNER_UNSIGNED",
            "observable_links": "Maxwell waves; Poynting flow; clock/PPN geometry",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EMOWN4014_2_constitutive_shape",
            "coefficient": "Delta_chi_principal_plus_skewon_plus_axion",
            "formula": "|Delta_chi_principal|+|Delta_chi_skewon|+L|dtheta_EM|",
            "value": "MISSING_CONSTITUTIVE_EXCLUSION_OR_OBSERVATIONAL_BOUND",
            "units": "tensor_dimensionless_or_inverse_length",
            "source_status": "CONSTITUTIVE_COUNTERBRANCH_RETAINED",
            "observable_links": "birefringence; dispersion; polarization rotation; EM cone",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EMOWN4014_3_hidden_readout_Hodge",
            "coefficient": "C_Hodge_hidden_plus_C_Hodge_readout",
            "formula": "|C_Hodge_hidden|+|C_Hodge_readout|",
            "value": "MISSING_NO_HIDDEN_HODGE_OR_READOUT_CLOSURE",
            "units": "dimensionless_or_model_dependent",
            "source_status": "HIDDEN_READOUT_HODGE_OPEN",
            "observable_links": "preferred-frame; light-speed anisotropy; clocks; spectroscopy",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EMOWN4014_4_conformal_scale",
            "coefficient": "Delta_conformal_scale",
            "formula": "4D Hodge/cone match but clock/source/impedance scale drift remains",
            "value": "MISSING_CLOCK_CHARGE_SOURCE_SCALE_OWNER",
            "units": "dimensionless_scale_drift",
            "source_status": "CONFORMAL_SCALE_GATE_RETAINED",
            "observable_links": "clock redshift; source normalization; alpha; Newton G",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EMOWN4014_5_wEM",
            "coefficient": "w_EM_minus_1",
            "formula": "D_v ln Z_Q or independent multiplier of Maxwell action/stress",
            "value": "ZERO_IF_PARENT_CURVATURE_NORM_FIXED_ELSE_MISSING_NORMALIZATION_BOUND",
            "units": "dimensionless_Maxwell_normalization",
            "source_status": "MAXWELL_KINETIC_OWNER_UNSIGNED",
            "observable_links": "alpha; EM binding; WEP; clocks; source mass",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EMOWN4014_6_CJQ_zg",
            "coefficient": "C_JQ_plus_z_g",
            "formula": "charge/current normalization ambiguity; z_g=D_v ln g_J after gauge choice",
            "value": "ZERO_IF_SAME_CURRENT_OWNER_GAUGE_FIXED_ELSE_SOURCE_SLOT_BOUND_REQUIRED",
            "units": "dimensionless_current_normalization",
            "source_status": "SAME_CURRENT_OWNER_PARTIAL",
            "observable_links": "alpha; WEP; R10; source current conservation",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EMOWN4014_7_CXF2",
            "coefficient": "C_XF2",
            "formula": "hidden/motion/time/readout coefficient multiplying F_Q^2 or F_Q*F_Q",
            "value": "ZERO_IF_NO_EXTRA_F2_OPERATOR_DOMAIN_SIGNED_ELSE_BOUND_REQUIRED",
            "units": "model_dependent",
            "source_status": "NO_EXTRA_F2_KEY_BLOCKER",
            "observable_links": "alpha drift; clocks; WEP; R10; PPN source scale",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EMOWN4014_8_balpha_invariant",
            "coefficient": "b_alpha",
            "formula": "b_alpha=2 z_g - s_XF2, invariant under A_Q rescaling",
            "value": "MISSING_PARENT_VERTICAL_COEFFICIENT_OR_BOUND",
            "units": "dimensionless_per_normalized_vertical_generator",
            "source_status": "INVARIANT_ALPHA_SOURCE_THROAT",
            "observable_links": "alpha; clock; WEP; R10; spectroscopy",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EMOWN4014_9_readout_radiative",
            "coefficient": "C_EM_readout_plus_delta_lambda_rad",
            "formula": "|C_EM_readout|+|delta_lambda_rad| from loop/readout/radiative regeneration of F2 coefficient",
            "value": "MISSING_READOUT_RADIATIVE_CLOSURE",
            "units": "model_dependent",
            "source_status": "EFFECTIVE_DOMAIN_CLOSURE_OPEN",
            "observable_links": "clock; spectroscopy; alpha; EM binding response",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EMOWN4014_10_arena_projection",
            "coefficient": "EM_owner_arena_projection",
            "formula": "map surviving EM owner residuals into clocks/WEP/R10/PPN/Newton-source kernels",
            "value": "MISSING_ARENA_PROJECTION_IF_ANY_COMPONENT_LIVE",
            "units": "arena_dependent",
            "source_status": "PROJECTION_REQUIRED_FOR_NUMERIC_CLAIM",
            "observable_links": "clocks; WEP; R10; PPN; Newton source",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def case_rows(timestamp: str) -> list[dict[str, Any]]:
    base = {
        "visible_domain": True,
        "parent_norm": True,
        "no_extra_F2": True,
        "same_current": True,
        "conformal_scale_owned": True,
        "readout_closed": True,
        "absolute_claim": False,
        "numeric_pack": False,
    }
    cases: list[dict[str, Any]] = []

    def add(case_id: str, **overrides: bool) -> None:
        row = dict(base)
        row.update(overrides)
        row.update({"case_id": case_id, "valid_for_claim": False, "timestamp_utc": timestamp})
        cases.append(row)

    add("CASE4014_0_full_EM_owner_signed")
    add("CASE4014_1_visible_domain_open", visible_domain=False)
    add("CASE4014_2_parent_norm_open", parent_norm=False)
    add("CASE4014_3_no_extra_F2_open", no_extra_F2=False)
    add("CASE4014_4_same_current_open", same_current=False)
    add("CASE4014_5_conformal_scale_open", conformal_scale_owned=False)
    add("CASE4014_6_readout_radiative_open", readout_closed=False)
    add("CASE4014_7_absolute_alpha_overclaim", absolute_claim=True)
    add(
        "CASE4014_8_numeric_pack",
        visible_domain=False,
        parent_norm=False,
        no_extra_F2=False,
        same_current=False,
        conformal_scale_owned=False,
        readout_closed=False,
        numeric_pack=True,
    )
    return cases


def result_for_case(row: dict[str, Any], timestamp: str) -> dict[str, Any]:
    if bool(row["numeric_pack"]):
        return {
            "case_id": row["case_id"],
            "owner_status": "FINITE_EM_OWNER_PACK_NONCLAIM",
            "residual_result": "DELTA_HODGE+wEM+CJQ+CXF2+BALPHA+READOUT_VECTOR_REQUIRED",
            "claim_result": "NO_MAXWELL_ALPHA_NEWTON_LOCAL_GR_PROMOTION",
            "next_action": "fill or zero source-backed EM owner residual rows before arena scoring",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }

    if bool(row["absolute_claim"]):
        return {
            "case_id": row["case_id"],
            "owner_status": "ABSOLUTE_ALPHA_OVERCLAIM_REJECTED",
            "residual_result": "LOCAL_DRIFT_SILENCE_DOES_NOT_PREDICT_ALPHA_VALUE",
            "claim_result": "NO_ABSOLUTE_ALPHA_OR_MU0_CLAIM",
            "next_action": "separate local vertical silence from absolute constant derivation/calibration debt",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }

    blockers: list[str] = []
    if not bool(row["visible_domain"]):
        blockers.extend(["Delta_Hodge_EM", "Delta_chi", "C_Hodge_hidden"])
    if not bool(row["parent_norm"]):
        blockers.append("w_EM")
    if not bool(row["no_extra_F2"]):
        blockers.extend(["C_XF2", "b_alpha"])
    if not bool(row["same_current"]):
        blockers.append("C_JQ+z_g")
    if not bool(row["conformal_scale_owned"]):
        blockers.append("Delta_conformal_scale")
    if not bool(row["readout_closed"]):
        blockers.append("C_EM_readout+delta_lambda_rad")

    if not blockers:
        return {
            "case_id": row["case_id"],
            "owner_status": "CONDITIONAL_OBSERVED_HODGE_MAXWELL_OWNER_LOCK",
            "residual_result": "DELTA_HODGE_wEM_CJQ_CXF2_ZERO_IF_PARENT_DOMAIN_SIGNED",
            "claim_result": "LOCAL_EM_SOURCE_COUPLING_SILENCE_NOT_ABSOLUTE_ALPHA_OR_FULL_GR",
            "next_action": "move to Gauss/Poisson/G_ref source-normalization bridge",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }

    return {
        "case_id": row["case_id"],
        "owner_status": "EM_OWNER_LOCK_BLOCKED",
        "residual_result": "+".join(blockers),
        "claim_result": "NO_MAXWELL_ALPHA_NEWTON_LOCAL_GR_PROMOTION",
        "next_action": "retain " + "+".join(blockers) + " as finite nonclaim rows",
        "valid_for_claim": False,
        "timestamp_utc": timestamp,
    }


def result_rows(cases: list[dict[str, Any]], timestamp: str) -> list[dict[str, Any]]:
    return [result_for_case(row, timestamp) for row in cases]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4014_0_conditional_derivation",
            "decision": "observed Hodge/Maxwell owner has a real conditional route",
            "reason": "typed EM action-domain exhaustion gives *_EM=*_obs; parent curvature norm fixes Z_Q; no-extra-F2 object language and same-current owner silence C_XF2/C_JQ",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4014_1_no_promotion",
            "decision": "do not promote Maxwell/alpha/Newton/local-GR claim",
            "reason": "the parent object-language certificate, parent curvature normalization, no-hidden-F2 slot, readout/radiative closure and source-scale/G_ref bridge are not jointly signed",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4014_2_finite_policy",
            "decision": "if EM owner fails, retain explicit Hodge/F2/current vector",
            "reason": "Hodge shape, conformal scale, Maxwell normalization, current normalization, hidden F2 and readout terms have different observables and cannot cancel by notation",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4014_3_next",
            "decision": "next target is Gauss/Poisson/G_ref source-normalization bridge",
            "reason": "EM owner is now theorem-or-vector; the local-GR route still needs the parent source charge to produce the Newtonian Poisson/Gauss limit with non-laundered G_ref",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CLAIM4014_0_Maxwell",
            "arena": "Maxwell_EM_stress",
            "allowed": False,
            "reason": "observed Hodge and normalization owner are conditional, not parent-adopted",
            "blocking_rows": "EMOWN4014_1_Delta_Hodge_EM;EMOWN4014_5_wEM;EMOWN4014_7_CXF2",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CLAIM4014_1_alpha",
            "arena": "alpha_clocks_spectroscopy",
            "allowed": False,
            "reason": "b_alpha/C_XF2/readout rows remain live and absolute alpha is not derived",
            "blocking_rows": "EMOWN4014_7_CXF2;EMOWN4014_8_balpha_invariant;EMOWN4014_9_readout_radiative",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CLAIM4014_2_WEP_R10",
            "arena": "WEP_R10_source_coupling",
            "allowed": False,
            "reason": "surviving EM owner residuals lack arena projection and source-backed coefficients",
            "blocking_rows": "EMOWN4014_7_CXF2;EMOWN4014_8_balpha_invariant;EMOWN4014_10_arena_projection",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CLAIM4014_3_Newton_local_GR",
            "arena": "Newton_local_GR",
            "allowed": False,
            "reason": "EM owner is not the Gauss/Poisson/G_ref source-normalization bridge",
            "blocking_rows": "EMOWN4014_4_conformal_scale;EMOWN4014_10_arena_projection",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT4014_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive the Gauss/Poisson/G_ref source-normalization bridge from the parent Hilbert/Hamiltonian charge to Newtonian mechanics, or retain epsilon_G_norm and Newton-source residual rows",
            "success_condition": "the same parent source charge M_H_ref controls the weak-field 1/r metric coefficient, Poisson equation, Gauss surface law and slow-particle acceleration with G_ref treated as calibrated constant rather than fitted orbital laundering",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "COMPLETE_NONCLAIM",
            "summary": "observed Hodge/Maxwell normalization/no-extra-F2 owner reduced to an exact conditional parent object-language theorem plus finite Hodge/F2/current residual vector",
            "current_best_next": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(timestamp: str, sources: list[dict[str, Any]], results: list[dict[str, Any]]) -> None:
    found = sum(1 for row in sources if row["exists"] and row["needle_found"])
    lines = [
        "# 4014 - Observed Hodge/Maxwell Normalization Owner Or C_XF2 Row",
        "",
        f"- Timestamp: `{timestamp}`",
        "- Status: `private_nonclaim_checkpoint`",
        "- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.",
        "",
        "## Result",
        "",
        "The EM owner route is now sharp:",
        "",
        "`Args(S_EM)={A_Q,F_Q=dA_Q,e_obs(q),orientation,fixed representation data,fixed constants}`",
        "",
        "If that parent object language is signed, then the EM Hodge star is the observed Hodge star, `*_EM=*_obs[e_obs(q)]`, and the independent Hodge/constitutive escape routes vanish.",
        "",
        "The Maxwell normalization route is separate: a parent curvature norm with fixed generator norm gives `Z_Q=C_P N_Q`. But gauge/diffeomorphism symmetry alone does not forbid hidden or independent `F_Q^2` terms. That needs a no-extra-F2 operator-domain theorem.",
        "",
        "## Coupling Throat",
        "",
        "`b_alpha = 2 z_g - s_XF2` is the invariant source-coupling throat. The split between current normalization `z_g` and kinetic coefficient `s_XF2` is convention-dependent until the same-current owner is fixed.",
        "",
        "## Finite Owner Vector",
        "",
        "`epsilon_EM_owner_4014 <= |Delta_Hodge_EM|+|Delta_chi_principal|+|Delta_chi_skewon|+L|dtheta_EM|+|C_Hodge_hidden|+|C_Hodge_readout|+|Delta_conformal_scale|+|w_EM-1|+|C_JQ|+|C_XF2|+|b_alpha|+|C_EM_readout|+|delta_lambda_rad|`.",
        "",
        "This can silence local EM drift conditionally, but it does not derive the absolute value of alpha or mu0.",
        "",
        "## Evaluator Results",
        "",
    ]
    for row in results:
        lines.append(
            f"- `{row['case_id']}`: owner=`{row['owner_status']}`, residual=`{row['residual_result']}`, claim=`{row['claim_result']}`, next=`{row['next_action']}`"
        )
    lines.extend(
        [
            "",
            "## Verdict",
            "",
            "This is the right kind of progress: the EM sector is no longer a blob. Hodge shape, Maxwell normalization, current normalization, hidden F2, conformal scale and readout/radiative terms are separated. The next local-GR move is the Newtonian Gauss/Poisson/G_ref bridge.",
            "",
            "## Next Target",
            "",
            f"- `{NEXT_DOC}`",
            f"- `{NEXT_SCRIPT}`",
            "",
            "## Source Count",
            "",
            f"- source needles found: `{found}/{len(sources)}`",
            "",
        ]
    )
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def append_spine(timestamp: str) -> None:
    marker = "## 4014 - Observed Hodge/Maxwell Owner"
    block = f"""

{marker}

- Timestamp: `{timestamp}`
- Result: typed visible EM domain `{{A_Q,F_Q,e_obs(q),orientation,fixed representation data,fixed constants}}` gives `*_EM=*_obs[e_obs(q)]` conditionally.
- Maxwell normalization: parent curvature norm with fixed generator norm gives `Z_Q=C_P N_Q`; no-extra-`F_Q^2` operator-domain theorem is required because gauge/diffeomorphism symmetry alone permits hidden `F_Q^2`.
- Coupling throat: `b_alpha=2 z_g-s_XF2` is invariant under EM field/current rescaling; `z_g` and `s_XF2` separately are not physical until the same-current owner is fixed.
- Finite fallback: `epsilon_EM_owner_4014 <= |Delta_Hodge_EM|+|Delta_chi_principal|+|Delta_chi_skewon|+L|dtheta_EM|+|C_Hodge_hidden|+|C_Hodge_readout|+|Delta_conformal_scale|+|w_EM-1|+|C_JQ|+|C_XF2|+|b_alpha|+|C_EM_readout|+|delta_lambda_rad|`.
- No claim: local EM drift silence is not an absolute alpha/mu0 prediction and not yet Newton/local-GR closure.
- Next: `{NEXT_DOC}`.
"""
    current = read_text(SPINE_PATH)
    if marker not in current:
        SPINE_PATH.write_text(current.rstrip() + block + "\n", encoding="utf-8")


def marker_in_spine() -> bool:
    return "## 4014 - Observed Hodge/Maxwell Owner" in read_text(SPINE_PATH)


def build_validation_rows(
    timestamp: str,
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    results: list[dict[str, Any]],
    compile_ok: bool,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail, "timestamp_utc": timestamp})

    add("VAL4014_00_sources_exist", all(bool(row["exists"]) for row in sources), "every cited source path exists")
    add("VAL4014_01_needles_found", all(bool(row["needle_found"]) for row in sources), "every cited source needle found")
    for idx, theorem_id in enumerate(
        [
            "OHN4014_0_observed_Hodge_lock",
            "OHN4014_1_constitutive_residual_split",
            "OHN4014_2_parent_Maxwell_normalization",
            "OHN4014_3_no_extra_F2_operator_domain",
            "OHN4014_4_charge_current_normalization",
            "OHN4014_5_conformal_scale_guard",
            "OHN4014_6_full_EM_owner_branch",
            "OHN4014_7_finite_owner_vector",
        ],
        start=2,
    ):
        add(f"VAL4014_{idx:02d}_theorem", any(row["theorem_id"] == theorem_id for row in theorem), f"{theorem_id} present")
    add("VAL4014_10_audit_domain", any(row["audit_id"] == "EOA4014_0_action_domain" for row in audit), "action-domain audit present")
    add("VAL4014_11_audit_norm", any(row["audit_id"] == "EOA4014_1_parent_curvature_norm" for row in audit), "normalization audit present")
    add("VAL4014_12_audit_F2", any(row["audit_id"] == "EOA4014_2_no_extra_F2" for row in audit), "no-extra-F2 audit present")
    add("VAL4014_13_audit_current", any(row["audit_id"] == "EOA4014_3_same_current_owner" for row in audit), "same-current audit present")
    add("VAL4014_14_audit_conformal", any(row["audit_id"] == "EOA4014_4_conformal_scale" for row in audit), "conformal caveat audit present")
    add("VAL4014_15_audit_alpha_guard", any(row["audit_id"] == "EOA4014_6_absolute_alpha_guard" for row in audit), "absolute alpha guard present")
    master = next(row for row in finite if row["row_id"] == "EMOWN4014_0_master")
    add("VAL4014_16_master_vector", "C_XF2" in master["formula"] and "Delta_conformal_scale" in master["formula"], "master vector contains F2 and conformal guards")
    for idx, row_id in enumerate(
        [
            "EMOWN4014_1_Delta_Hodge_EM",
            "EMOWN4014_2_constitutive_shape",
            "EMOWN4014_3_hidden_readout_Hodge",
            "EMOWN4014_4_conformal_scale",
            "EMOWN4014_5_wEM",
            "EMOWN4014_6_CJQ_zg",
            "EMOWN4014_7_CXF2",
            "EMOWN4014_8_balpha_invariant",
            "EMOWN4014_9_readout_radiative",
            "EMOWN4014_10_arena_projection",
        ],
        start=17,
    ):
        add(f"VAL4014_{idx:02d}_{row_id}", any(row["row_id"] == row_id for row in finite), f"{row_id} present")
    full = next(row for row in results if row["case_id"] == "CASE4014_0_full_EM_owner_signed")
    visible = next(row for row in results if row["case_id"] == "CASE4014_1_visible_domain_open")
    norm = next(row for row in results if row["case_id"] == "CASE4014_2_parent_norm_open")
    f2 = next(row for row in results if row["case_id"] == "CASE4014_3_no_extra_F2_open")
    current = next(row for row in results if row["case_id"] == "CASE4014_4_same_current_open")
    conformal = next(row for row in results if row["case_id"] == "CASE4014_5_conformal_scale_open")
    readout = next(row for row in results if row["case_id"] == "CASE4014_6_readout_radiative_open")
    overclaim = next(row for row in results if row["case_id"] == "CASE4014_7_absolute_alpha_overclaim")
    numeric = next(row for row in results if row["case_id"] == "CASE4014_8_numeric_pack")
    add("VAL4014_27_full_case", full["residual_result"] == "DELTA_HODGE_wEM_CJQ_CXF2_ZERO_IF_PARENT_DOMAIN_SIGNED", "full signed case conditionally zeros EM owner rows")
    add("VAL4014_28_visible_case", "Delta_Hodge_EM" in visible["residual_result"], "visible domain open routes to Hodge rows")
    add("VAL4014_29_norm_case", norm["residual_result"] == "w_EM", "normalization open routes to w_EM")
    add("VAL4014_30_f2_case", "C_XF2" in f2["residual_result"] and "b_alpha" in f2["residual_result"], "no-extra-F2 open routes to C_XF2/b_alpha")
    add("VAL4014_31_current_case", current["residual_result"] == "C_JQ+z_g", "same-current open routes to C_JQ/z_g")
    add("VAL4014_32_conformal_case", conformal["residual_result"] == "Delta_conformal_scale", "conformal scale open routed")
    add("VAL4014_33_readout_case", readout["residual_result"] == "C_EM_readout+delta_lambda_rad", "readout/radiative open routed")
    add("VAL4014_34_overclaim_case", overclaim["owner_status"] == "ABSOLUTE_ALPHA_OVERCLAIM_REJECTED", "absolute alpha overclaim rejected")
    add("VAL4014_35_numeric_case", numeric["owner_status"] == "FINITE_EM_OWNER_PACK_NONCLAIM", "numeric pack remains nonclaim")
    add("VAL4014_36_claim_gate_false", all(str(row.get("allowed", "")).lower() == "false" for row in read_csv(OUTPUTS["claim_gate"])), "all claim gates false")
    add("VAL4014_37_next_target", OUTPUTS["next"].exists() and NEXT_DOC in read_text(OUTPUTS["next"]), "next target written")
    add("VAL4014_38_doc_exists", DOC_PATH.exists() and "b_alpha = 2 z_g - s_XF2" in read_text(DOC_PATH), "document written with invariant coupling throat")
    add("VAL4014_39_spine_updated", SPINE_PATH.exists() and marker_in_spine(), "spine updated")
    add("VAL4014_40_no_fwb_outputs", not any(str(path).startswith(str(FWB)) for path in OUTPUTS.values()), "no outputs target formalization-workbench")
    add("VAL4014_41_compile", compile_ok, "script compiles")
    add("VAL4014_42_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "script __pycache__ removed")
    output_tables = [
        sources,
        theorem,
        audit,
        finite,
        results,
        read_csv(OUTPUTS["decision"]),
        read_csv(OUTPUTS["claim_gate"]),
        read_csv(OUTPUTS["next"]),
        read_csv(OUTPUTS["status"]),
    ]
    add("VAL4014_43_all_nonclaim", all(str(row.get("valid_for_claim", "")).lower() == "false" for table in output_tables for row in table), "all emitted rows remain nonclaim")
    add("VAL4014_44_no_nan", not any("nan" in str(row).lower() or "inf" in str(row).lower() for row in results), "no nan/inf evaluator outputs")
    add("VAL4014_45_private_scope", DOC_PATH.exists() and "private_nonclaim_checkpoint" in read_text(DOC_PATH), "private scope recorded")
    add("VAL4014_46_forward_target", "Gauss" in read_text(OUTPUTS["next"]) and "Poisson" in read_text(OUTPUTS["next"]) and "G_ref" in read_text(OUTPUTS["next"]), "forward target is Gauss/Poisson/G_ref bridge")
    return checks


def main() -> None:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    theorem = theorem_rows(timestamp)
    audit = audit_rows(timestamp)
    finite = finite_rows(timestamp)
    cases = case_rows(timestamp)
    results = result_rows(cases, timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["audit"], audit)
    write_csv(OUTPUTS["finite"], finite)
    write_csv(OUTPUTS["cases"], cases)
    write_csv(OUTPUTS["results"], results)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(timestamp, sources, results)
    append_spine(timestamp)

    compile_ok = True
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except py_compile.PyCompileError:
        compile_ok = False
    cache = SCRIPT_PATH.parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    validation = build_validation_rows(timestamp, sources, theorem, audit, finite, results, compile_ok)
    write_csv(OUTPUTS["validation"], validation)
    passed = sum(1 for row in validation if row["passed"])
    total = len(validation)
    print(f"4014 validation: {passed}/{total} passed")
    if passed != total:
        for row in validation:
            if not row["passed"]:
                print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()

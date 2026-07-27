from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from deltaktf_shell_profile_gate import read_csv, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4511"
CLAIM_ID = "L-353"
MARKER = "PPC4161_NO_SPURION_READOUT_GRAMMAR_OR_WFM_FINITE_ROW_4511"
PACKET_MARKER = "PPC4161_PACKET_NO_SPURION_READOUT_GRAMMAR_OR_WFM_FINITE_ROW_4511"
DECISION = "NO_SPURION_MONOPOLE_READOUT_THEOREM_DERIVED_CONDITIONALLY_WFM_ROW_STAGED_NONCLAIM"
NEXT_TARGET = "4512-Y5-R2FR-Khat-trace-match-or-RKtrace-finite-row.md"

FORMAL_PATH = FORMAL / "527-PPC4161-no-spurion-readout-grammar-or-WFm-finite-row.md"
DOC_PATH = POST / "4511-Y5-R2FR-no-spurion-readout-grammar-or-WFm-finite-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4511_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4511_SOURCE_REGISTER.csv"
NO_SPURION_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4511_NO_SPURION_READOUT_THEOREM.csv"
READOUT_CLASSIFIER = SOURCE_DIR / "P8_Y5_R2FR_4511_READOUT_SPURION_CLASSIFIER.csv"
WFM_INPUT_FILL = SOURCE_DIR / "P8_Y5_R2FR_4511_WFM_INPUT_FILL_ROWS.csv"
FINITE_WFM = SOURCE_DIR / "P8_Y5_R2FR_4511_WFM_FINITE_BOUND_ROWS.csv"
HIGHER_GUARD = SOURCE_DIR / "P8_Y5_R2FR_4511_HIGHER_CURVATURE_GUARD.csv"
PARENT_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4511_PARENT_SIGNATURE_AUDIT.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4511_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4511_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4511_NEXT_TARGET.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4511_DECISION.csv"

FORMAL_526 = FORMAL / "526-PPC4161-parent-source-root-lock-or-first-BWeyl-input-fill.md"
POST_4510 = POST / "4510-Y5-R2FR-parent-source-root-lock-or-first-BWeyl-input-fill.md"
BWEYL_FILL_4510 = SOURCE_DIR / "P8_Y5_R2FR_4510_BWEYL_INPUT_FILL_ROWS.csv"
NO_SPURION_4509 = SOURCE_DIR / "P8_Y5_R2FR_4509_NO_SPURION_GATE.csv"
NUMERIC_4509 = SOURCE_DIR / "P8_Y5_R2FR_4509_BWEYL_NUMERIC_ACQUISITION_ROW.csv"

WEYL_3606 = SOURCE_DIR / "P8_Y5_R2FR_3606_BQWEYL_NO_SPURION_THEOREM.csv"
WEYL_BOUND_3606 = SOURCE_DIR / "P8_Y5_R2FR_3606_BQWEYL_BOUND_ROWS.csv"
WEYL_ACQ_3607 = SOURCE_DIR / "P8_Y5_R2FR_3607_BQWEYL_FINITE_ACQUISITION_ROWS.csv"
OLI_2304 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2304_OBJECT_LANGUAGE_INDEX_LEMMA.csv"
PTG_2304 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2304_PARENT_SIGNATURE_GATE.csv"
BQI_2304 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2304_BQWEYL_FIRST_SOURCE_INPUT.csv"
BQB_2302 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2302_BQWEYL_BOUND_ROW_NONCLAIM.csv"
READOUT_EXCLUSION_2625 = SOURCE_DIR / "P8_Y5_PARENT_DOMAIN_CERT_2625_READOUT_EXCLUSION_CERTIFICATE.csv"
READOUT_POLICY_2625 = SOURCE_DIR / "P8_Y5_PARENT_DOMAIN_CERT_2625_READOUT_CLOSURE_POLICY.csv"
VBR_1816 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1816_VARIATION_BEFORE_READOUT_THEOREM.csv"
RTP_1919 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1919_READOUT_DESCENT_PROOF_ATTEMPT.csv"
RNE_2353 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2353_READOUT_NO_REENTRY_ZERO_AUDIT.csv"
RNG_2418 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2418_READOUT_NO_REENTRY_GATE.csv"
SRNG_2335 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2335_SOURCE_READOUT_ARGUMENT_CERTIFICATE.csv"
CBP_2419 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2419_CHAINMAP_READOUT_BOUND_PACK.csv"
BP_2354 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2354_READOUT_REENTRY_BOUND_PACK.csv"
PPN_2889 = SOURCE_DIR / "P8_Y5_R2FR_2889_COMMON_WEYL_PPN_KERNEL_ROW_NONCLAIM.csv"
DQWEYL2_2754 = SOURCE_DIR / "P8_Y5_R2FR_2754_DQWEYL2_INPUT_CONTRACT.csv"
BOUND_2530 = SOURCE_DIR / "P8_Y5_NO_SHADOW_2530_BQWEYL_BOUND_ROW_STATUS.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for line_number, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return line_number
    return 0


def md(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def table(rows: Sequence[Mapping[str, object]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    output = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        output.append("| " + " | ".join(md(row.get(header, "")) for header in headers) + " |")
    return "\n".join(output)


def source_rows() -> List[Dict[str, object]]:
    specs = [
        ("SRC4511_00_formal526", "4510 formal handoff", FORMAL_526, "Parent Source-Root Lock", "source-root previous leg"),
        ("SRC4511_01_post4510", "4510 post mirror", POST_4510, "PST4510_5_BWeyl_insertion", "B_Weyl insertion row"),
        ("SRC4511_02_bweyl4510", "4510 B_Weyl input fill", BWEYL_FILL_4510, "BWF4510_02_Lcg_chain", "Lcg chain conditionally filled"),
        ("SRC4511_03_ns4509", "4509 no-spurion gate", NO_SPURION_4509, "NSG4509_1_spurion_exclusion", "readout spurion gate"),
        ("SRC4511_04_numeric4509", "4509 numeric row", NUMERIC_4509, "BWN4509_05_WFm", "W_F,m numeric row"),
        ("SRC4511_05_weyl3606_spurion", "3606 spurion necessity", WEYL_3606, "BQW3606_3_spurion_necessity", "linear Weyl needs spurion"),
        ("SRC4511_06_weyl3606_bound", "3606 finite bound law", WEYL_3606, "BQW3606_5_finite_bound_law", "finite BqWeyl law"),
        ("SRC4511_07_weyl3606_verdict", "3606 current verdict", WEYL_3606, "BQW3606_7_current_MTS_verdict", "zero not live"),
        ("SRC4511_08_bound3606", "3606 bound rows", WEYL_BOUND_3606, "BQB3606_5_Pspurion", "P spurion finite row"),
        ("SRC4511_09_acq3607", "3607 acquisition rows", WEYL_ACQ_3607, "BACQ3607_11_acceptance_rule", "acceptance rule"),
        ("SRC4511_10_oli2304", "2304 object-language lemma", OLI_2304, "OLI2304_3_spurion_necessity", "index theorem"),
        ("SRC4511_11_oli2304_verdict", "2304 object-language verdict", OLI_2304, "OLI2304_6_verdict", "not parent signed"),
        ("SRC4511_12_ptg2304", "2304 parent signature gate", PTG_2304, "PTG2304_3_no_spurion_projector", "no-spurion missing gate"),
        ("SRC4511_13_bqi2304", "2304 first source input", BQI_2304, "BQI2304_1_BqWeyl_parent_coefficient", "finite coefficient row"),
        ("SRC4511_14_bqb2302", "2302 finite bound", BQB_2302, "BQB2302_2_profile_response", "profile response"),
        ("SRC4511_15_re2625", "2625 readout exclusion", READOUT_EXCLUSION_2625, "REC2625_1_solution_space_readout", "pure readout map"),
        ("SRC4511_16_policy2625", "2625 readout policy", READOUT_POLICY_2625, "POL2625_1_reduced_action_retention", "reduced action tax"),
        ("SRC4511_17_vbr1816", "1816 variation-before-readout", VBR_1816, "VBR1816_0_target", "post-current theorem"),
        ("SRC4511_18_rtp1919", "1919 readout descent attempt", RTP_1919, "RTP1919_5_verdict", "readout not derived"),
        ("SRC4511_19_rne2353", "2353 readout no-reentry", RNE_2353, "RNE2353_3_projector_worldtube", "projector countermodel"),
        ("SRC4511_20_rng2418", "2418 readout no-reentry gate", RNG_2418, "RNG2418_3_source_worldtube_projector", "worldtube projector"),
        ("SRC4511_21_srng2335", "2335 source-readout certificate", SRNG_2335, "SRNG2335_0_total_clause", "same coframe readout contract"),
        ("SRC4511_22_cbp2419", "2419 chainmap bound pack", CBP_2419, "CBP2419_4_projector_stress", "projector stress fallback"),
        ("SRC4511_23_bp2354", "2354 readout reentry bound", BP_2354, "BP2354_4_projector_stress", "readout finite fallback"),
        ("SRC4511_24_ppn2889", "2889 common Weyl PPN kernel", PPN_2889, "PPNK2889_0_common_weyl_gamma", "common Weyl kernel nonclaim"),
        ("SRC4511_25_dqweyl2754", "2754 quadratic Weyl guard", DQWEYL2_2754, "IN2754_0_DqWeyl2", "higher curvature guard"),
        ("SRC4511_26_bound2530", "2530 BqWeyl bound status", BOUND_2530, "BQB2530_5_acceptance", "zero or full finite rows"),
    ]
    rows: List[Dict[str, object]] = []
    for source_id, role, path, needle, note in specs:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text(path),
                "line": line_of(path, needle),
                "note": note,
                "valid_for_claim": False,
            }
        )
    return rows


def no_spurion_theorem_rows() -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "NST4511_0_object",
            "object": "W_F,m",
            "statement": "partial_m does not add Weyl indices; any linear Weyl term in W_F,m must already be a scalar linear in C_abcd with an available Weyl-type contraction object",
            "result": "reduces W_F,m zero to the same typed object-language problem as B_qWeyl",
            "status": "DERIVED_REDUCTION",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "NST4511_1_metric_epsilon",
            "object": "metric/orientation-only local scalar",
            "statement": "metric contractions and epsilon-only contractions of one Weyl tensor vanish by trace-free Weyl symmetries",
            "result": "no q C scalar exists with only g and epsilon",
            "status": "EXACT_INDEX_LEMMA_IMPORTED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "NST4511_2_monopole_worldline",
            "object": "isotropic worldline/worldtube readout",
            "statement": "with only u^a, h_ab=g_ab+u_a u_b and scalar monopole data, E_ab=C_acbd u^c u^d is spatial and trace-free, so h^ab E_ab=0 and u^a E_ab=0",
            "result": "an l=0 same-worldtube Hilbert monopole readout cannot supply a scalar linear Weyl spurion",
            "status": "NEW_MONOPOLE_READOUT_LEMMA",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "NST4511_3_spurion_necessity",
            "object": "nonzero linear Weyl readout",
            "statement": "a nonzero scalar must contain P^{abcd}C_abcd or equivalently a trace-free spatial multipole Q_TF^{ab}E_ab, anisotropic detector tensor, material marker, or field-dependent projector",
            "result": "the live danger is not generic Weyl; it is anisotropic/multipole/readout-kernel ownership",
            "status": "SPURION_CLASSIFIER_DERIVED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "NST4511_4_postreadout",
            "object": "pure post-solution readout",
            "statement": "R_post:Sol(S_parent)/G->Data absent from S_parent and S_eff cannot create an Euler-source Weyl spurion; if a reduced/readout action is varied, it is a retained EFT branch",
            "result": "pure readout is harmless, but pre-variation projector/reduced-action readout remains live",
            "status": "READOUT_ORDER_THEOREM_IMPORTED_AND_SHARPENED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "NST4511_5_combined_WFm_zero",
            "object": "W_F,m",
            "statement": "typed parent scalar/density q plus metric/epsilon/same-Hilbert-monopole readout plus no pre-variation projector/reduced action implies W_F,m=0",
            "result": "B_Weyl's linear Weyl/F-metric leg is conditionally theorem-zero, not numerically sourced",
            "status": "EXACT_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def readout_classifier_rows() -> List[Dict[str, object]]:
    return [
        {
            "class_id": "RSC4511_0_allowed_scalar",
            "readout_or_object": "q,m,F,V and scalar parent densities",
            "classification": "ALLOWED_UNDER_NO_SPURION_GRAMMAR",
            "reason": "scalar factors do not carry Weyl indices",
            "finite_fallback_if_unsigned": "B_qWeyl parent coefficient",
            "valid_for_claim": False,
        },
        {
            "class_id": "RSC4511_1_allowed_metric_epsilon",
            "readout_or_object": "g_ab, e^A_mu, epsilon_abcd, volume form",
            "classification": "ALLOWED_LINEAR_WEYL_ZERO",
            "reason": "single-Weyl metric/epsilon contractions vanish",
            "finite_fallback_if_unsigned": "P_Weyl_spurion if extra tensor exists",
            "valid_for_claim": False,
        },
        {
            "class_id": "RSC4511_2_allowed_monopole",
            "readout_or_object": "same-worldtube Hilbert monopole, isotropic clock/source mass, scalar tau",
            "classification": "ALLOWED_IF_POST_VARIATION_AND_ISOTROPIC",
            "reason": "monopole/timelike data cannot contract trace-free E_ab into a scalar",
            "finite_fallback_if_unsigned": "Q_TF_readout or projector-stress row",
            "valid_for_claim": False,
        },
        {
            "class_id": "RSC4511_3_forbidden_quadrupole",
            "readout_or_object": "trace-free source/detector quadrupole Q_TF^{ab}",
            "classification": "WEYL_SPURION",
            "reason": "Q_TF^{ab}E_ab is a nonzero scalar linear in Weyl",
            "finite_fallback_if_unsigned": "Q_TF_norm*C_Weyl*tau_arena",
            "valid_for_claim": False,
        },
        {
            "class_id": "RSC4511_4_forbidden_projector",
            "readout_or_object": "field-dependent projector, worldtube/domain selector, fitted mask",
            "classification": "READOUT_REENTRY_SPURION",
            "reason": "delta(Pi J)=Pi delta J+(delta Pi)J can create an effective P^{abcd}",
            "finite_fallback_if_unsigned": "epsilon_chainmap_readout_abs or E_projector_stress",
            "valid_for_claim": False,
        },
        {
            "class_id": "RSC4511_5_forbidden_reduced_action",
            "readout_or_object": "varied readout-reduced S_eff or radiative cutoff action",
            "classification": "RETAINED_EFT_BRANCH",
            "reason": "once varied, readout is no longer postprocessing and can carry real source coefficients",
            "finite_fallback_if_unsigned": "B_readout_m plus B_qWeyl coefficient row",
            "valid_for_claim": False,
        },
        {
            "class_id": "RSC4511_6_separate_tower",
            "readout_or_object": "q C_abcd C^abcd, q C*Cdual, nonlocal Weyl kernels",
            "classification": "NOT_KILLED_BY_LINEAR_THEOREM",
            "reason": "quadratic/higher-curvature terms are legal even when linear Weyl is absent",
            "finite_fallback_if_unsigned": "D_qWeyl2/no-tower row",
            "valid_for_claim": False,
        },
    ]


def wfm_input_fill_rows() -> List[Dict[str, object]]:
    return [
        {
            "input_id": "WFF4511_00_WFm",
            "source_4509_row": "BWN4509_05_WFm",
            "symbol": "W_F,m",
            "filled_value": "0",
            "fill_type": "CONDITIONAL_THEOREM_ZERO",
            "condition": "NST4511 no-spurion plus isotropic postreadout grammar is parent-signed in the active branch",
            "source_path": str(DOC_PATH),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "input_id": "WFF4511_01_Z_linear",
            "source_3606_row": "BQB3606_0_Z_linear",
            "symbol": "Z_BqWeyl_linear",
            "filled_value": "TRUE_CONDITIONAL",
            "fill_type": "ZERO_SWITCH_IF_PARENT_SIGNATURES_PASS",
            "condition": "typed parent object language, q scalar/density representation, no P^{abcd}, no quadrupole/readout reentry, no reduced action",
            "source_path": str(DOC_PATH),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "input_id": "WFF4511_02_Pspurion",
            "source_3606_row": "BQB3606_5_Pspurion",
            "symbol": "P_Weyl_spurion",
            "filled_value": "0",
            "fill_type": "CONDITIONAL_THEOREM_ZERO",
            "condition": "all allowed parent/readout objects are scalar, metric/epsilon, or isotropic monopole; no anisotropic/tidal source marker",
            "source_path": str(DOC_PATH),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def finite_wfm_rows() -> List[Dict[str, object]]:
    return [
        {
            "bound_id": "WFB4511_0_parent_spurion",
            "quantity": "W_F,m_parent",
            "formula": "|W_F,m_parent| <= |partial_m q| |P_parent| |C_Weyl| + |q| |partial_m P_parent| |C_Weyl|",
            "required_inputs": "partial_m q; q; P_parent; partial_m P_parent; C_Weyl; units; source path",
            "current_status": "MISSING_PARENT_SPURION_OR_ZERO_SIGNATURE",
            "valid_for_claim": False,
        },
        {
            "bound_id": "WFB4511_1_readout_quadrupole",
            "quantity": "W_F,m_readout",
            "formula": "|W_F,m_readout| <= |partial_m Q_TF| |E_Weyl| + |Q_TF| |partial_m E_Weyl| + commutator/readout tails",
            "required_inputs": "Q_TF norm; partial_m Q_TF; E_Weyl profile; readout commutator; source-worldtube certificate",
            "current_status": "MISSING_QUADRUPOLE_OR_READOUT_SILENCE",
            "valid_for_claim": False,
        },
        {
            "bound_id": "WFB4511_2_projector_reentry",
            "quantity": "W_F,m_projector",
            "formula": "|W_F,m_projector| <= E_projector_stress + E_worldtube + E_domain_motion + E_current_escape + E_exterior",
            "required_inputs": "chainmap/readout bound pack components and M_H_ref normalization",
            "current_status": "MISSING_CHAINMAP_COMPONENT_VALUES",
            "valid_for_claim": False,
        },
        {
            "bound_id": "WFB4511_3_arena_projection",
            "quantity": "E_WFm[arena]",
            "formula": "E_WFm[arena] <= tau_WFm_arena ||G_q|| |W_F,m_total| ||C_Weyl|| + boundary/source tails",
            "required_inputs": "tau_R10; tau_PPN; tau_clock; tau_orbital; G_q; C_Weyl profile; no-cancellation envelope",
            "current_status": "MISSING_ARENA_PROJECTION",
            "valid_for_claim": False,
        },
    ]


def higher_guard_rows() -> List[Dict[str, object]]:
    return [
        {
            "guard_id": "HCG4511_0_quadratic_Weyl",
            "object": "D_qWeyl2",
            "guard": "linear no-spurion theorem does not kill q C_abcd C^abcd or q C*Cdual",
            "required_followup": "no-higher-curvature/no-tower selector or finite D_qWeyl2 row",
            "valid_for_claim": False,
        },
        {
            "guard_id": "HCG4511_1_integrated_out_tower",
            "object": "nonlocal/higher-curvature effective action",
            "guard": "integrating out hidden fields can regenerate Weyl^2/Ricci^2/f(R)-like channels even if the bare linear term is absent",
            "required_followup": "no-tower theorem or retained finite rows",
            "valid_for_claim": False,
        },
        {
            "guard_id": "HCG4511_2_metric_GR_readout",
            "object": "ordinary GR Weyl curvature",
            "guard": "zeroing W_F,m means no extra MTS scalar source from linear Weyl; it does not erase physical GR tidal curvature/geodesic deviation",
            "required_followup": "keep GR Weyl as baseline geometry, not an anomalous source",
            "valid_for_claim": False,
        },
    ]


def parent_audit_rows() -> List[Dict[str, object]]:
    return [
        {
            "audit_id": "PA4511_0_theorem",
            "claim": "W_F,m has an exact no-spurion/readout zero theorem",
            "status": "DERIVED_CONDITIONALLY",
            "effect": "linear Weyl response is eliminated if the parent/readout inventory has no Weyl-type tensor beyond metric/epsilon/isotropic monopole",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4511_1_new_sharpening",
            "claim": "monopole readout is not a Weyl spurion",
            "status": "DERIVED_INDEX_LEMMA",
            "effect": "same-worldtube l=0 Hilbert mass/clock/source readout cannot make Q_TF^{ab}E_ab",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4511_2_live_gap",
            "claim": "active MTS branch signs no anisotropic/projector/readout reentry",
            "status": "NOT_PROVEN",
            "effect": "W_F,m zero remains conditional; finite rows are staged for quadrupole/projector/reduced-action tails",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4511_3_remaining_BWeyl",
            "claim": "full B_Weyl tail is zero",
            "status": "NOT_CLAIMED",
            "effect": "Khat trace match and boundary/domain/readout tails remain next gates",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> List[Dict[str, object]]:
    return [
        {"gate_id": "CG4511_0_WFm_zero", "gate": "W_F,m=0 live in active branch", "derived_now": False, "blocked_by": "no-spurion/readout inventory not parent-signed for active branch", "claim_allowed": False},
        {"gate_id": "CG4511_1_BqWeyl_zero", "gate": "linear B_qWeyl zero switch active", "derived_now": False, "blocked_by": "parent typed language, q representation, no-projector/readout and no-tower gates unsigned", "claim_allowed": False},
        {"gate_id": "CG4511_2_BWeyl_zero", "gate": "full B_Weyl=0", "derived_now": False, "blocked_by": "Khat trace and boundary/domain/readout tails remain open", "claim_allowed": False},
        {"gate_id": "CG4511_3_local_GR", "gate": "local GR/PPN/R10 promotion", "derived_now": False, "blocked_by": "source coupling/Khat/local projection gates remain open", "claim_allowed": False},
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "derived": "conditional no-spurion plus isotropic-monopole readout theorem for W_F,m, with finite W_F,m rows staged",
            "not_derived": "active parent signature excluding all Weyl-type projectors, anisotropic multipoles, reduced-action readout and higher-curvature towers",
            "claim_status": "PRIVATE_NONCLAIM",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated": STAMP,
        }
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4511_0",
            "decision": DECISION,
            "because": "a single Weyl tensor cannot form a scalar from metric/epsilon or isotropic monopole readout; nonzero linear Weyl needs an explicit anisotropic/projector/readout spurion",
            "effect": "W_F,m now has a clean conditional theorem-zero row and a concrete finite fallback; the next B_Weyl obstruction is Khat trace matching",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4511_0",
            "target_file": NEXT_TARGET,
            "task": "try to close K_hat=K_metric[Gamma_eff]+K_TF with zero trace derivative, or source R_K_trace,m as a finite B_Weyl component",
            "success_condition": "R_K_trace,m is theorem-zero in the parent branch or has a sourced finite row compatible with local arenas",
            "do_not": "claim B_Weyl zero until Khat trace and boundary/domain tails are also closed or bounded",
            "valid_for_claim": False,
        }
    ]


def validate(all_rows: Mapping[str, Sequence[Mapping[str, object]]]) -> List[Dict[str, object]]:
    csv_files = [
        SOURCE_REGISTER,
        NO_SPURION_THEOREM,
        READOUT_CLASSIFIER,
        WFM_INPUT_FILL,
        FINITE_WFM,
        HIGHER_GUARD,
        PARENT_AUDIT,
        CLAIM_GATES,
        STATUS_CSV,
        NEXT_CSV,
        DECISION_CSV,
    ]
    parsed = True
    details: List[str] = []
    for path in csv_files:
        try:
            rows = read_csv(path)
            parsed = parsed and bool(rows)
            details.append(f"{path.name}:{len(rows)}")
        except Exception as exc:
            parsed = False
            details.append(f"{path.name}:ERROR:{exc}")

    source_ok = all(bool(row["exists"]) and bool(row["needle_found"]) for row in all_rows["sources"])
    theorem_ok = any(row.get("theorem_id") == "NST4511_5_combined_WFm_zero" for row in all_rows["theorem"])
    monopole_ok = any(row.get("theorem_id") == "NST4511_2_monopole_worldline" for row in all_rows["theorem"])
    forbidden_ok = any(row.get("class_id") == "RSC4511_3_forbidden_quadrupole" for row in all_rows["classifier"])
    wfm_fill_ok = any(row.get("input_id") == "WFF4511_00_WFm" and row.get("filled_value") == "0" for row in all_rows["fill"])
    finite_ok = any(row.get("bound_id") == "WFB4511_3_arena_projection" for row in all_rows["finite"])
    guard_ok = any(row.get("guard_id") == "HCG4511_0_quadratic_Weyl" for row in all_rows["higher"])
    claim_gates_blocked = all(row.get("derived_now") is False and row.get("claim_allowed") is False for row in all_rows["gates"])
    nonclaim_ok = all(
        str(value).lower() != "true"
        for rows in all_rows.values()
        for row in rows
        for key, value in row.items()
        if key in {"valid_for_claim", "claim_allowed"}
    )
    next_ok = all_rows["next"][0]["target_file"] == NEXT_TARGET
    pycache_absent = not (SCRIPT_DIR / "__pycache__").exists()

    checks = [
        ("VAL4511_00_sources", source_ok, "all source paths exist and source needles are found"),
        ("VAL4511_01_theorem", theorem_ok, "combined W_F,m zero theorem row exists"),
        ("VAL4511_02_monopole", monopole_ok, "isotropic-monopole readout lemma recorded"),
        ("VAL4511_03_forbidden_spurion", forbidden_ok, "quadrupole/projector spurion classifier recorded"),
        ("VAL4511_04_WFm_fill", wfm_fill_ok, "W_F,m conditionally filled as theorem-zero row"),
        ("VAL4511_05_finite_bound", finite_ok, "finite W_F,m arena projection bound is staged"),
        ("VAL4511_06_higher_guard", guard_ok, "quadratic Weyl guard is retained"),
        ("VAL4511_07_claims_blocked", claim_gates_blocked, "all claim gates remain blocked"),
        ("VAL4511_08_nonclaim_flags", nonclaim_ok, "all generated valid_for_claim/claim_allowed flags remain false"),
        ("VAL4511_09_csv_parse", parsed, ";".join(details)),
        ("VAL4511_10_next_target", next_ok, NEXT_TARGET),
        ("VAL4511_11_pycache_absent", pycache_absent, "scripts __pycache__ absent after cleanup"),
    ]
    rows = [
        {
            "validation_id": check_id,
            "status": "PASS" if ok else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, ok, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL4511_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "4511 no-spurion readout grammar or W_F,m finite row",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def append_once(path: Path, marker: str, body: str) -> None:
    existing = text(path)
    if marker in existing:
        return
    path.write_text(existing.rstrip() + "\n\n" + body.strip() + "\n", encoding="utf-8")


def append_claim_once() -> None:
    existing = text(CLAIMS_PATH)
    if CLAIM_ID in existing or MARKER in existing:
        return
    row = ",".join(
        [
            CLAIM_ID,
            "local_gr_newton_r2fr_no_spurion_readout",
            '"4511 derives the conditional no-spurion/readout theorem for W_F,m: metric/epsilon contractions and same-worldtube isotropic monopole readouts cannot produce a scalar linear in Weyl; nonzero linear Weyl requires an explicit P^{abcd}, trace-free quadrupole, anisotropic/projector readout, or reduced-action reentry. W_F,m is conditionally filled as zero and finite fallback rows are staged."',
            '"4511 source register, no-spurion readout theorem, readout spurion classifier, W_F,m input fills, finite W_F,m rows, higher-curvature guard, parent audit, claim gates, status and validation."',
            "private_no_spurion_readout_WFm_conditional_nonclaim",
            NEXT_TARGET,
            "claiming full B_Weyl/local-GR from the linear Weyl index theorem, ignoring quadrupole/projector readout, or erasing Weyl^2 towers.",
            "local_gr_newton_r2fr_no_spurion_readout",
            str(FORMAL_PATH),
            NEXT_TARGET,
            '"close Khat trace match or source R_K_trace,m as the next B_Weyl component."',
        ]
    )
    CLAIMS_PATH.write_text(existing.rstrip() + "\n" + row + "\n", encoding="utf-8")


def build_doc(
    sources: Sequence[Mapping[str, object]],
    theorem: Sequence[Mapping[str, object]],
    classifier: Sequence[Mapping[str, object]],
    fill: Sequence[Mapping[str, object]],
    finite: Sequence[Mapping[str, object]],
    higher: Sequence[Mapping[str, object]],
    parent: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    status: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    next_target: Sequence[Mapping[str, object]],
    validation: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4511 - No-Spurion Readout Grammar Or W_F,m Finite Row

Marker: `{MARKER}`  
Claim: `{CLAIM_ID}`  
Decision: `{DECISION}`  
Generated: `{STAMP}`

## Verdict

4511 sharpens the no-spurion route instead of just saying "readout missing". The key result is:

`W_F,m=0`

if the active branch admits only scalar/density parent factors, metric/coframe/orientation contractions, and same-worldtube isotropic monopole readout after variation. Metric/epsilon contractions of one Weyl tensor vanish; a timelike monopole gives the electric Weyl tensor `E_ab=C_acbd u^c u^d`, but `E_ab` is spatial and trace-free, so scalar monopole readout cannot contract it into a nonzero source.

A nonzero linear Weyl term therefore requires a real spurion: `P^abcd C_abcd`, or equivalently a trace-free quadrupole/tidal readout `Q_TF^ab E_ab`, anisotropic material marker, field-dependent projector/worldtube selector, or readout-reduced action varied before the parent source is formed.

So `W_F,m` is now conditionally filled as a theorem-zero row, while the finite fallback is explicit if any anisotropic/projector/readout spurion survives. This is still private/nonclaim: no local-GR, PPN, R10, clock, orbital, or full `B_Weyl` claim fires.

## Source Register

{table(sources)}

## No-Spurion Readout Theorem

{table(theorem)}

## Readout Spurion Classifier

{table(classifier)}

## W_F,m Input Fill Rows

{table(fill)}

## W_F,m Finite Bound Rows

{table(finite)}

## Higher Curvature Guard

{table(higher)}

## Parent Signature Audit

{table(parent)}

## Claim Gates

{table(gates)}

## Status

{table(status)}

## Decision

{table(decisions)}

## Next Target

{table(next_target)}

## Validation

{table(validation)}
"""


def main() -> None:
    sources = source_rows()
    theorem = no_spurion_theorem_rows()
    classifier = readout_classifier_rows()
    fill = wfm_input_fill_rows()
    finite = finite_wfm_rows()
    higher = higher_guard_rows()
    parent = parent_audit_rows()
    gates = claim_gate_rows()
    status = status_rows()
    decisions = decision_rows()
    next_target = next_rows()

    all_rows = {
        "sources": sources,
        "theorem": theorem,
        "classifier": classifier,
        "fill": fill,
        "finite": finite,
        "higher": higher,
        "parent": parent,
        "gates": gates,
        "status": status,
        "decisions": decisions,
        "next": next_target,
    }

    write_csv(SOURCE_REGISTER, sources)
    write_csv(NO_SPURION_THEOREM, theorem)
    write_csv(READOUT_CLASSIFIER, classifier)
    write_csv(WFM_INPUT_FILL, fill)
    write_csv(FINITE_WFM, finite)
    write_csv(HIGHER_GUARD, higher)
    write_csv(PARENT_AUDIT, parent)
    write_csv(CLAIM_GATES, gates)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_CSV, next_target)
    write_csv(DECISION_CSV, decisions)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validate(all_rows)
    write_csv(VALIDATION_PATH, validation)

    doc = build_doc(
        sources,
        theorem,
        classifier,
        fill,
        finite,
        higher,
        parent,
        gates,
        status,
        decisions,
        next_target,
        validation,
    )
    write_text(FORMAL_PATH, doc)
    write_text(DOC_PATH, doc)
    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4511 No-Spurion Readout Grammar Or W_F,m Finite Row

Marker: `{MARKER}`  
4511 derives the conditional no-spurion/readout theorem for `W_F,m`. A scalar parent density with only metric/coframe/orientation and same-worldtube isotropic monopole readout cannot form a nonzero scalar linear in Weyl. Nonzero linear Weyl requires a real `P^abcd` spurion, trace-free quadrupole/tidal readout, anisotropic marker, field-dependent projector/worldtube selector, or readout-reduced action. `W_F,m` is conditionally filled as zero; finite spurion/readout rows are staged if that grammar fails.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4511 Packet Integration

Marker: `{PACKET_MARKER}`  
The private packet now has conditional theorem-zero rows for the Lcg-chain and `W_F,m` parts of `B_Weyl`. The next obstruction is not vague Weyl curvature; it is the remaining `Khat` trace-match residual plus boundary/domain/readout tails.
""",
    )
    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()

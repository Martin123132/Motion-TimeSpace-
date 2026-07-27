from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4093-Y5-R2FR-adopt-parent-normal-form-test-gamma-beta-zeta-or-reject-to-residuals.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
DECISION = "PARENT_NORMAL_FORM_FIXES_SOURCE_AND_PROJECTOR_BLOCK_BUT_GAMMA_BETA_ZETA_STILL_NEED_EH_R11_SOURCE_CLOSURE"

LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4093_00_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4092_NEXT_TARGET.csv",
        "4093-Y5-R2FR-adopt-parent-normal-form-test-gamma-beta-zeta-or-reject-to-residuals.md",
        "4092 selects normal-form test against gamma, beta, zeta and R11 families.",
    ),
    "SRC4093_01_normal_form": (
        SOURCE_DIR / "P8_Y5_R2FR_4092_PARENT_NORMAL_FORM.csv",
        "PNF4092_3_qbasic_projector",
        "4092 parent normal form clauses.",
    ),
    "SRC4093_02_sufficient_chain": (
        SOURCE_DIR / "P8_Y5_R2FR_4092_SUFFICIENT_THEOREM_CHAIN.csv",
        "SUFFICIENT_SOURCE_DENOMINATOR_ROUTE_CONSTRUCTED",
        "4092 sufficient theorem chain for q-basic selector and fixed source denominator.",
    ),
    "SRC4093_03_4085_ppn": (
        SOURCE_DIR / "P8_Y5_R2FR_4085_SOURCE_STABLE_PPN_THEOREM.csv",
        "PPN4085_4_conservation_zero",
        "4085 source-stable PPN theorem for gamma, beta, preferred-frame and zeta rows.",
    ),
    "SRC4093_04_4085_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_4085_PPN_BOUND_TABLE.csv",
        "BND4085_9_zeta3",
        "Sourced local PPN bounds used for fallback residual contracts.",
    ),
    "SRC4093_05_eh_signature": (
        SOURCE_DIR / "P8_Y5_R2FR_4086_EH_SIGNATURE_THEOREM.csv",
        "EH4086_4_4085_unlock",
        "4086 EH selector signature and PPN unlock condition.",
    ),
    "SRC4093_06_r11_families": (
        SOURCE_DIR / "P8_Y5_R2FR_4086_R11_FAMILY_TO_PPN_ROUTE.csv",
        "R11F4086_09",
        "R11 operator family to PPN projection map.",
    ),
    "SRC4093_07_r11_4087": (
        SOURCE_DIR / "P8_Y5_R2FR_4087_R11_VECTOR_UPDATE.csv",
        "R11UP4087_0",
        "4087 standard f(R)/R2 scalar gamma-beta template status.",
    ),
    "SRC4093_08_r11_4088": (
        SOURCE_DIR / "P8_Y5_R2FR_4088_R11_VECTOR_UPDATE.csv",
        "R11UP4088_1",
        "4088 Ricci/Weyl spin-2 slip template status.",
    ),
    "SRC4093_09_projector_4091": (
        SOURCE_DIR / "P8_Y5_R2FR_4091_PREFERRED_FRAME_RESIDUAL_VECTOR.csv",
        "PFR4091_0_alpha1",
        "4091 projector/domain preferred-frame block zero in private/candidate branch.",
    ),
    "SRC4093_10_4048_zero": (
        SOURCE_DIR / "P8_Y5_R2FR_4048_CONDITIONAL_PPN_ZERO_VECTOR.csv",
        "PPNZ4048_4_zeta",
        "Older conditional PPN zero vector including zeta rows.",
    ),
    "SRC4093_11_4063_readout": (
        SOURCE_DIR / "P8_Y5_R2FR_4063_PPN_READOUT_VECTOR.csv",
        "PPN4063_3_conservation_anisotropy",
        "PPN readout vector for gamma, beta, preferred-frame, xi and zeta.",
    ),
    "SRC4093_12_4063_fallback": (
        SOURCE_DIR / "P8_Y5_R2FR_4063_RESIDUAL_FALLBACK_VECTOR.csv",
        "RFB4063_4_master",
        "Fallback residual vector if weak-field assumptions fail.",
    ),
    "SRC4093_13_source_current": (
        SOURCE_DIR / "P8_Y5_SOURCE_CURRENT_CLOSURE_THEOREM_ATTEMPT.csv",
        "SC532_5_zero_extra_projection",
        "Source-current closure theorem attempt and extra-channel blockers.",
    ),
    "SRC4093_14_r11_minimum": (
        SOURCE_DIR / "P8_LOCAL_EH_R11_OPERATOR_AUDIT.csv",
        "R2_fR_scalar_mode",
        "Local EH/R11 operator audit listing unclosed operator families.",
    ),
}


def write_csv(path: Path, rows: List[dict]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> List[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def bool_string(value: bool) -> str:
    return "True" if value else "False"


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def source_register_rows() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        rows.append(
            {
                "source_id": source_id,
                "source_type": "local_checkpoint_csv",
                "path_or_url": str(path),
                "needle": needle,
                "role": role,
                "exists": bool_string(path.exists()),
                "valid_for_claim": "False",
                "timestamp_utc": TIMESTAMP,
            }
        )
    rows.append(
        {
            "source_id": "SRC4093_15_script",
            "source_type": "generator_script",
            "path_or_url": str(SCRIPT_PATH),
            "needle": SCRIPT_PATH.name,
            "role": "Reproducible generator for 4093 normal-form gamma/beta/zeta/R11 gate.",
            "exists": bool_string(SCRIPT_PATH.exists()),
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        }
    )
    return rows


def adoption_test_rows() -> List[dict]:
    return [
        {
            "test_id": "ADOPT4093_0_fixed_source",
            "normal_form_input": "PNF4092_1_Qvis + PNF4092_2_SourceQuotient + PNF4092_4_ReadoutAfterVariation",
            "tested_row": "fixed Newton/PPN source denominator",
            "result_if_adopted": "U=G_ref*M_H/r before PPN scoring",
            "surviving_gap": "observed time/Hamiltonian charge calibration and nonprojector extra mass channels",
            "verdict": "CANDIDATE_PASS_NOT_PUBLIC_SIGNED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "test_id": "ADOPT4093_1_projector_preferred_frame",
            "normal_form_input": "PNF4092_3_QBasicProjector + 4091 vector/flux/anisotropy zero",
            "tested_row": "alpha1 alpha2 alpha3 xi from projector/domain sector",
            "result_if_adopted": "alpha1_domain=alpha2_domain=alpha3_domain=xi_domain=0",
            "surviving_gap": "nonprojector vector/torsion/memory or frame channels, if present",
            "verdict": "CANDIDATE_PASS_FOR_PROJECTOR_DOMAIN_BLOCK_NOT_PUBLIC_SIGNED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "test_id": "ADOPT4093_2_gamma_beta",
            "normal_form_input": "PNF4092 fixed source plus 4086 EH selector",
            "tested_row": "gamma_minus_1 and beta_minus_1",
            "result_if_adopted": "gamma-1=0 and beta-1=0 only if EH-only through <=2PN and DeltaE_nonEH=0",
            "surviving_gap": "R2/fR, Ricci/Weyl, scalar-tensor, torsion/nonmetricity, bulk/range, nonlocal memory and source-normalization operators",
            "verdict": "NORMAL_FORM_ALONE_INSUFFICIENT",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "test_id": "ADOPT4093_3_zeta",
            "normal_form_input": "PNF4092 fixed source plus Bianchi/Hilbert source closure",
            "tested_row": "zeta1 zeta2 zeta3 conservation rows",
            "result_if_adopted": "zeta_i=0 only if the same Hilbert stress is covariantly conserved and no hidden source-current leak remains",
            "surviving_gap": "non-Hilbert current, boundary/reference source dependence, extra mass-channel projection, nonintegrable symplectic terms",
            "verdict": "NORMAL_FORM_HELPS_BUT_SOURCE_CURRENT_CLOSURE_STILL_OPEN",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def gamma_beta_zeta_rows() -> List[dict]:
    return [
        {
            "row_id": "GBZ4093_0_gamma",
            "observable": "gamma_minus_1",
            "theorem_formula": "EH same-branch spatial response and no tracefree non-EH/R11 stress => gamma-1=0",
            "normal_form_contribution": "fixes U denominator and same observed stack, so gamma is not laundered through GM_orb",
            "missing_for_public_zero": "parent EH selector and all tracefree R11/q_loc/nonprojector stresses zero or bounded",
            "candidate_value_if_all_premises": "0",
            "fallback_bound": "2.3e-5",
            "status": "CONDITIONAL_ZERO_NOT_PUBLIC",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "row_id": "GBZ4093_1_beta",
            "observable": "beta_minus_1",
            "theorem_formula": "same-source EH nonlinear completion gives B_source=A_source^2 => beta-1=0",
            "normal_form_contribution": "fixes source denominator before 2PN and blocks readout/source-mask reentry",
            "missing_for_public_zero": "EH-only O(U^2), no non-EH scalar/source-normalization hair, no boundary/reference beta source term",
            "candidate_value_if_all_premises": "0",
            "fallback_bound": "8.0e-5",
            "status": "CONDITIONAL_ZERO_NOT_PUBLIC",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "row_id": "GBZ4093_2_zeta1",
            "observable": "zeta1",
            "theorem_formula": "nabla_mu T_H^{mu nu}=0 and no hidden source leak => zeta1=0",
            "normal_form_contribution": "excludes source-label prefactors and readout source masks from ordinary Hilbert stress",
            "missing_for_public_zero": "non-Hilbert current silence, boundary/reference flux silence, extra Pi_M projection zero",
            "candidate_value_if_all_premises": "0",
            "fallback_bound": "2.0e-2",
            "status": "CONDITIONAL_ZERO_NOT_PUBLIC",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "row_id": "GBZ4093_3_zeta2",
            "observable": "zeta2",
            "theorem_formula": "nabla_mu T_H^{mu nu}=0 and no hidden source leak => zeta2=0",
            "normal_form_contribution": "same as zeta1",
            "missing_for_public_zero": "binary/self-acceleration source-current leaks remain to be zeroed or bounded",
            "candidate_value_if_all_premises": "0",
            "fallback_bound": "4.0e-5",
            "status": "CONDITIONAL_ZERO_NOT_PUBLIC",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "row_id": "GBZ4093_4_zeta3",
            "observable": "zeta3",
            "theorem_formula": "nabla_mu T_H^{mu nu}=0 and no hidden source leak => zeta3=0",
            "normal_form_contribution": "same as zeta1",
            "missing_for_public_zero": "Newton-third-law/source exchange leakage must be zero or below bound",
            "candidate_value_if_all_premises": "0",
            "fallback_bound": "1.0e-8",
            "status": "CONDITIONAL_ZERO_NOT_PUBLIC",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def r11_audit_rows() -> List[dict]:
    return [
        {
            "family_id": "R11A4093_0_projector_domain_stress",
            "operator_family": "projector_domain_stress",
            "normal_form_effect": "PNF4092_3 upgrades the 4090/4091 q-basic projector/domain zero into a candidate parent-normal-form consequence",
            "remaining_status": "CANDIDATE_ZERO_IF_PARENT_NORMAL_FORM_ADOPTED",
            "feeds": "alpha1; alpha2; alpha3; xi; projector part of zeta/source-normalization",
            "next_requirement": "public parent adoption of PNF4092_3",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "family_id": "R11A4093_1_vector_preferred_frame",
            "operator_family": "vector_preferred_frame",
            "normal_form_effect": "domain-selector vector channel zero inside q-basic projector/domain sector",
            "remaining_status": "PROJECTOR_DOMAIN_VECTOR_ZERO_CANDIDATE",
            "feeds": "alpha1; alpha2; alpha3; xi",
            "next_requirement": "prove no independent nonprojector vector/torsion/frame marker survives",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "family_id": "R11A4093_2_R2_fR_scalar",
            "operator_family": "R2_fR_scalar_mode",
            "normal_form_effect": "none beyond fixed source scoring denominator",
            "remaining_status": "LIVE_PARENT_COEFFICIENT_MAP_OR_DOUBLE_ZERO_REQUIRED",
            "feeds": "gamma_minus_1; beta_minus_1; alpha(lambda); R11",
            "next_requirement": "map MTS c_R2 to standard coefficient, prove absent/double-zero, or keep 4087 bound template",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "family_id": "R11A4093_3_Ricci_Weyl",
            "operator_family": "Ricci_Weyl_squared",
            "normal_form_effect": "none beyond fixed source scoring denominator",
            "remaining_status": "LIVE_PARENT_COEFFICIENT_MAP_OR_TOPOLOGICAL_DOUBLE_ZERO_REQUIRED",
            "feeds": "gamma_minus_1; xi; wave_sector; R11",
            "next_requirement": "separate Gauss-Bonnet/topological part from live Weyl/Ricci response and prove zero or bound",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "family_id": "R11A4093_4_scalar_tensor",
            "operator_family": "scalar_tensor_class_metric",
            "normal_form_effect": "source labels are removed, but scalar prefactor/hair is not automatically fixed",
            "remaining_status": "LIVE_IF_NONCONSTANT_SCALAR_HAIR_SURVIVES",
            "feeds": "gamma_minus_1; beta_minus_1; Gdot_over_G; alpha(lambda); R11",
            "next_requirement": "prove scalar fixed/source-free with double-zero/mass gap or compute coupling envelope",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "family_id": "R11A4093_5_torsion_nonmetricity",
            "operator_family": "torsion_nonmetricity",
            "normal_form_effect": "observed stack helps define the Levi-Civita target but does not prove connection reduction",
            "remaining_status": "LIVE_CONNECTION_SIGNATURE_RUNG",
            "feeds": "WEP; clocks; lightcone; spin/source; gamma; R11",
            "next_requirement": "derive no-independent-connection theorem or fill connection residual rows",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "family_id": "R11A4093_6_bulk_range",
            "operator_family": "bulk_X_force_law",
            "normal_form_effect": "ordinary source labels are removed but bulk X charge/range is not killed",
            "remaining_status": "LIVE_R10_RANGE_BRANCH_IF_NOT_ZERO",
            "feeds": "alpha(lambda); gamma_minus_1; beta_minus_1; source_eta; R11",
            "next_requirement": "derive X source charge zero/mass gap or compare to R10 alpha(lambda) bounds",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "family_id": "R11A4093_7_nonlocal_memory",
            "operator_family": "nonlocal_memory_kernel",
            "normal_form_effect": "readout firewall helps, but local-vacuum kernel silence is not automatic",
            "remaining_status": "LIVE_MEMORY_BRANCH_IF_LOCAL_SILENCE_NOT_PROVED",
            "feeds": "alpha3; Gdot_over_G; alpha(lambda); hysteresis; R11",
            "next_requirement": "prove compact-local kernel has zero monopole/vector/Gdot projection or bound kernel norm",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "family_id": "R11A4093_8_source_normalization",
            "operator_family": "source_normalization_operator",
            "normal_form_effect": "domain_projector_mass piece is zero in candidate branch; nonprojector source-normalization channels remain",
            "remaining_status": "PARTIAL_CANDIDATE_ZERO_REMAINDER_LIVE",
            "feeds": "beta_source; alpha_i; xi; zeta_i; Gdot; R11",
            "next_requirement": "zero or bound radial, boundary, bulk, nonEH, species, time-drift and calibration source-normalization channels",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "family_id": "R11A4093_9_boundary_topological",
            "operator_family": "boundary_topological_terms",
            "normal_form_effect": "fixed boundary reference helps only if source-blind no-flux/proper boundary class is parent-signed",
            "remaining_status": "LIVE_UNTIL_BOUNDARY_REFERENCE_NOFLUX_SIGNED_OR_BOUNDED",
            "feeds": "zeta_i; beta; alpha3; xi; Gdot; source calibration",
            "next_requirement": "derive source-blind boundary/reference theorem or supply boundary stress/source-normalization bounds",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def fallback_contract_rows() -> List[dict]:
    return [
        {
            "contract_id": "FB4093_0_gamma",
            "if_zero_rejected": "tracefree non-EH/R11/q_loc stress survives",
            "residual_formula": "delta_gamma_nonEH ~= -(kappa_ref/(C_TF*U)) nabla^-2 P_TF[DeltaE_nonEH_ij]",
            "bound": "abs(gamma-1) <= 2.3e-5",
            "required_inputs": "operator coefficient, weak-field projection, units, source path",
            "status": "SOURCE_READY_CONTRACT_NOT_FILLED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "contract_id": "FB4093_1_beta",
            "if_zero_rejected": "second-order EH-only/source-normalization completion fails",
            "residual_formula": "delta_beta_nonEH=Pi_beta[DeltaE_nonEH_00 plus source-normalization terms]",
            "bound": "abs(beta-1) <= 8.0e-5",
            "required_inputs": "2PN coefficient, fixed-U denominator, source-normalization residual, source path",
            "status": "SOURCE_READY_CONTRACT_NOT_FILLED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "contract_id": "FB4093_2_zeta",
            "if_zero_rejected": "hidden source-current leak or non-Bianchi residual survives",
            "residual_formula": "zeta_j=Pi_zeta_j[nabla_mu DeltaE_nonEH^{mu nu}-kappa_ref DeltaJ_source^nu]",
            "bound": "zeta1<=2.0e-2; zeta2<=4.0e-5; zeta3<=1.0e-8",
            "required_inputs": "DeltaJ_source projection, conservation anomaly, units, source path",
            "status": "SOURCE_READY_CONTRACT_NOT_FILLED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "contract_id": "FB4093_3_R11",
            "if_zero_rejected": "nonprojector R11 family remains live",
            "residual_formula": "DeltaE_nonEH=sum_i c_i E_i + E_q + E_boundary + E_readout",
            "bound": "componentwise 4085 PPN/R10/Gdot bounds; no cancellation",
            "required_inputs": "family coefficient, normalization, weak-field map, source path, pass/fail row",
            "status": "SOURCE_READY_CONTRACT_NOT_FILLED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def promotion_gate_rows() -> List[dict]:
    return [
        {
            "gate_id": "PROM4093_0_candidate_full_ppn_zero",
            "condition": "PNF4092 adopted and EH4086 selector signed and all R11/q_loc/source-current residuals zero or bounded below 4085 limits",
            "then_result": "gamma=beta=1; alpha_i=xi=zeta_i=0; fixed U=G_ref*M_H/r",
            "current_status": "NOT_MET",
            "why_not": "normal form adoption is candidate/unsigned and nonprojector R11/source-current gates remain live",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "gate_id": "PROM4093_1_projector_domain_subblock",
            "condition": "PNF4092 q-basic projector adopted",
            "then_result": "projector/domain preferred-frame block and domain_projector_mass channel are zero",
            "current_status": "CANDIDATE_SUBBLOCK_PASS_NOT_PUBLIC",
            "why_not": "parent adoption still unsigned; nonprojector families remain",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "gate_id": "PROM4093_2_public_local_GR",
            "condition": "all local GR residual rows prove zero or pass sourced bounds",
            "then_result": "public MTS local-GR reduction claim may be considered",
            "current_status": "FALSE",
            "why_not": "gamma/beta/zeta/R11 conditions not yet globally closed",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def decision_rows() -> List[dict]:
    return [
        {
            "decision_id": "DEC4093_0_normal_form_value",
            "decision": "keep parent normal form as the leading derivation route",
            "meaning": "It is the cleanest route because it turns source denominator and q-basic projector ownership into grammar consequences.",
            "result": "fixed-source and projector-domain gates are structurally advanced",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "decision_id": "DEC4093_1_gamma_beta_zeta",
            "decision": "do not promote gamma/beta/zeta yet",
            "meaning": "Those rows still require EH-only/no-R11 and source-current closure beyond the parent normal form.",
            "result": "conditional zero theorem plus fallback residual contracts",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "decision_id": "DEC4093_2_next_attack",
            "decision": "attack nonprojector R11 double-zero/absence next",
            "meaning": "This is now the largest remaining obstruction to gamma/beta and public local-GR promotion.",
            "result": "4094 target selected",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def claim_gate_rows() -> List[dict]:
    return [
        {
            "claim_id": "CLAIM4093_0_fixed_source_candidate",
            "claim": "candidate normal form fixes source denominator",
            "allowed": "True",
            "reason": "within candidate parent normal form, U=G_ref*M_H/r is derived before PPN scoring",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4093_1_projector_subblock_candidate",
            "claim": "candidate normal form kills projector/domain preferred-frame block",
            "allowed": "True",
            "reason": "PNF4092 q-basic projector imports 4090/4091 theorem-zero branch",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4093_2_gamma_beta_zeta_public",
            "claim": "public gamma=beta=1 and zeta_i=0",
            "allowed": "False",
            "reason": "EH selector, R11 silence and source-current closure remain unsigned",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4093_3_full_local_GR",
            "claim": "full public MTS to local GR",
            "allowed": "False",
            "reason": "normal form is necessary progress, not enough without nonprojector R11/source-current/boundary closure",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def next_target_rows() -> List[dict]:
    return [
        {
            "target_id": "NEXT4093_0",
            "next_target": "4094-Y5-R2FR-nonprojector-R11-double-zero-parent-selector-or-gamma-beta-bound.md",
            "script": "scripts/Y5_R2FR_4094_nonprojector_R11_double_zero_parent_selector_or_gamma_beta_bound.py",
            "why": "4093 shows parent normal form is not enough for gamma/beta/zeta while nonprojector R11 families remain live. Next attack R2/fR, Ricci/Weyl, scalar-tensor, torsion, bulk and memory families by double-zero/absence or source-backed bounds.",
            "priority": "P0",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "target_id": "NEXT4093_1",
            "next_target": "source_current_zeta_closure_after_R11",
            "script": "defer_until_R11_tracefree_and_source_normalization_reduced",
            "why": "Zeta/source-current closure is essential, but R11/source-normalization families first define the leaks that zeta must score.",
            "priority": "P1",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def status_rows() -> List[dict]:
    return [
        {
            "checkpoint": "4093",
            "decision": DECISION,
            "candidate_fixed_source_denominator": "yes_if_PNF4092_adopted",
            "candidate_projector_domain_block": "zero_if_PNF4092_adopted",
            "gamma_beta_zeta_public": "False",
            "largest_next_obstruction": "nonprojector_R11_and_source_current_closure",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        }
    ]


def write_doc() -> None:
    DOC_PATH.write_text(
        "\n".join(
            [
                "# 4093 - Adopt Parent Normal Form, Test Gamma/Beta/Zeta Or Reject To Residuals",
                "",
                "## Purpose",
                "",
                "4092 wrote a candidate parent normal form. 4093 tests what that normal form actually buys for the remaining local-GR rows.",
                "",
                f"- Decision: `{DECISION}`",
                "- Candidate fixed-source denominator: `yes, if PNF4092 is adopted`",
                "- Candidate projector/domain preferred-frame block: `zero, if PNF4092 is adopted`",
                "- Public `gamma=beta=1`, `zeta_i=0`, or local-GR claim: `false`",
                "",
                "## Result",
                "",
                "The parent normal form is useful but not sufficient by itself.",
                "",
                "It gives the clean route",
                "",
                "```text",
                "U = G_ref M_H / r",
                "GM_orb is output-only",
                "P_D = q_src^* Pbar_top",
                "epsilon_domain_vector = epsilon_domain_flux = epsilon_domain_anisotropy = 0",
                "```",
                "",
                "so it supports the 4090/4091 projector-domain result and prevents source-denominator laundering.",
                "",
                "But `gamma`, `beta`, and `zeta_i` still require more:",
                "",
                "```text",
                "gamma-1 = 0  needs EH-only tracefree spatial response plus no live R11/q_loc stress",
                "beta-1  = 0  needs EH 2PN nonlinear completion plus no source-normalization/boundary beta term",
                "zeta_i  = 0  needs same Hilbert stress conserved and no hidden source-current leak",
                "```",
                "",
                "## Nonprojector R11 Status",
                "",
                "The q-basic/projector-domain sector is the good news. The bad news, honestly stated, is that these families remain live unless separately zeroed or bounded:",
                "",
                "- `R2_fR_scalar_mode`",
                "- `Ricci_Weyl_squared`",
                "- `scalar_tensor_class_metric`",
                "- `torsion_nonmetricity`",
                "- `bulk_X_force_law`",
                "- `nonlocal_memory_kernel`",
                "- nonprojector pieces of `source_normalization_operator`",
                "- boundary/reference source terms unless source-blind no-flux is parent-signed",
                "",
                "That means 4093 does not circle the same missingness. It narrows the next fight: nonprojector R11 must be absent, double-zero, topological, massive/screened with a sourced bound, or kept as an explicit residual.",
                "",
                "## Decision",
                "",
                "Keep the parent normal form as the leading derivation route, but do not claim local GR from it yet. Next target is nonprojector R11 double-zero/absence or gamma/beta bounds.",
                "",
                "## Outputs",
                "",
                "- `P8_Y5_R2FR_4093_SOURCE_REGISTER.csv`",
                "- `P8_Y5_R2FR_4093_NORMAL_FORM_ADOPTION_TEST.csv`",
                "- `P8_Y5_R2FR_4093_GAMMA_BETA_ZETA_THEOREM.csv`",
                "- `P8_Y5_R2FR_4093_R11_RESIDUAL_FAMILY_AUDIT.csv`",
                "- `P8_Y5_R2FR_4093_FALLBACK_RESIDUAL_CONTRACT.csv`",
                "- `P8_Y5_R2FR_4093_PUBLIC_PROMOTION_GATE.csv`",
                "- `P8_Y5_R2FR_4093_DECISION_GATE.csv`",
                "- `P8_Y5_R2FR_4093_NEXT_TARGET.csv`",
                "- `P8_Y5_BRR545_4093_VALIDATION.csv`",
                "",
            ]
        ),
        encoding="utf-8",
    )


def generated_outputs() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4093_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4093_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4093_NORMAL_FORM_ADOPTION_TEST": SOURCE_DIR / "P8_Y5_R2FR_4093_NORMAL_FORM_ADOPTION_TEST.csv",
        "P8_Y5_R2FR_4093_GAMMA_BETA_ZETA_THEOREM": SOURCE_DIR / "P8_Y5_R2FR_4093_GAMMA_BETA_ZETA_THEOREM.csv",
        "P8_Y5_R2FR_4093_R11_RESIDUAL_FAMILY_AUDIT": SOURCE_DIR / "P8_Y5_R2FR_4093_R11_RESIDUAL_FAMILY_AUDIT.csv",
        "P8_Y5_R2FR_4093_FALLBACK_RESIDUAL_CONTRACT": SOURCE_DIR / "P8_Y5_R2FR_4093_FALLBACK_RESIDUAL_CONTRACT.csv",
        "P8_Y5_R2FR_4093_PUBLIC_PROMOTION_GATE": SOURCE_DIR / "P8_Y5_R2FR_4093_PUBLIC_PROMOTION_GATE.csv",
        "P8_Y5_R2FR_4093_DECISION_GATE": SOURCE_DIR / "P8_Y5_R2FR_4093_DECISION_GATE.csv",
        "P8_Y5_R2FR_4093_CLAIM_GATE": SOURCE_DIR / "P8_Y5_R2FR_4093_CLAIM_GATE.csv",
        "P8_Y5_R2FR_4093_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4093_NEXT_TARGET.csv",
        "P8_Y5_R2FR_4093_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4093_STATUS.csv",
    }


def write_outputs() -> Dict[str, Path]:
    outputs = generated_outputs()
    write_csv(outputs["P8_Y5_R2FR_4093_SOURCE_REGISTER"], source_register_rows())
    write_csv(outputs["P8_Y5_R2FR_4093_NORMAL_FORM_ADOPTION_TEST"], adoption_test_rows())
    write_csv(outputs["P8_Y5_R2FR_4093_GAMMA_BETA_ZETA_THEOREM"], gamma_beta_zeta_rows())
    write_csv(outputs["P8_Y5_R2FR_4093_R11_RESIDUAL_FAMILY_AUDIT"], r11_audit_rows())
    write_csv(outputs["P8_Y5_R2FR_4093_FALLBACK_RESIDUAL_CONTRACT"], fallback_contract_rows())
    write_csv(outputs["P8_Y5_R2FR_4093_PUBLIC_PROMOTION_GATE"], promotion_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4093_DECISION_GATE"], decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4093_CLAIM_GATE"], claim_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4093_NEXT_TARGET"], next_target_rows())
    write_csv(outputs["P8_Y5_R2FR_4093_STATUS"], status_rows())
    write_doc()
    return outputs


def validate(outputs: Dict[str, Path]) -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        exists = path.exists()
        contains = exists and needle in read_text(path)
        rows.append(
            {
                "check_id": f"VAL4093_SRC_{source_id}",
                "check": "local source exists and contains needle",
                "passed": bool_string(contains),
                "detail": f"{path} | needle={needle} | role={role}",
                "timestamp_utc": TIMESTAMP,
            }
        )

    for name, path in outputs.items():
        try:
            parsed = parse_csv(path)
            ok = len(parsed) > 0
            detail = f"{path} rows={len(parsed)}"
        except Exception as exc:
            ok = False
            detail = f"{path} parse_error={exc}"
        rows.append(
            {
                "check_id": f"VAL4093_CSV_{name}",
                "check": "generated CSV parses and is non-empty",
                "passed": bool_string(ok),
                "detail": detail,
                "timestamp_utc": TIMESTAMP,
            }
        )

    adoption = parse_csv(outputs["P8_Y5_R2FR_4093_NORMAL_FORM_ADOPTION_TEST"])
    adoption_text = "\n".join(str(row) for row in adoption)
    adoption_ok = all(
        needle in adoption_text
        for needle in [
            "CANDIDATE_PASS_NOT_PUBLIC_SIGNED",
            "CANDIDATE_PASS_FOR_PROJECTOR_DOMAIN_BLOCK_NOT_PUBLIC_SIGNED",
            "NORMAL_FORM_ALONE_INSUFFICIENT",
        ]
    )
    rows.append(
        {
            "check_id": "VAL4093_ADOPTION_TEST",
            "check": "normal form passes fixed-source/projector subblocks but not full gamma/beta/zeta",
            "passed": bool_string(adoption_ok),
            "detail": "checks candidate pass and insufficiency rows",
            "timestamp_utc": TIMESTAMP,
        }
    )

    gbz = parse_csv(outputs["P8_Y5_R2FR_4093_GAMMA_BETA_ZETA_THEOREM"])
    expected = {"gamma_minus_1", "beta_minus_1", "zeta1", "zeta2", "zeta3"}
    observed = {row.get("observable") for row in gbz}
    all_nonclaim = all(row.get("valid_for_claim") == "False" and row.get("status") == "CONDITIONAL_ZERO_NOT_PUBLIC" for row in gbz)
    rows.append(
        {
            "check_id": "VAL4093_GAMMA_BETA_ZETA_ROWS",
            "check": "gamma beta zeta rows are present and nonclaim conditional zeros",
            "passed": bool_string(expected == observed and all_nonclaim),
            "detail": f"observed={sorted(observed)}",
            "timestamp_utc": TIMESTAMP,
        }
    )

    r11 = parse_csv(outputs["P8_Y5_R2FR_4093_R11_RESIDUAL_FAMILY_AUDIT"])
    r11_text = "\n".join(str(row) for row in r11)
    r11_ok = all(
        needle in r11_text
        for needle in [
            "R2_fR_scalar_mode",
            "Ricci_Weyl_squared",
            "scalar_tensor_class_metric",
            "torsion_nonmetricity",
            "bulk_X_force_law",
            "nonlocal_memory_kernel",
            "source_normalization_operator",
            "projector_domain_stress",
        ]
    )
    rows.append(
        {
            "check_id": "VAL4093_R11_AUDIT_COVERAGE",
            "check": "R11 audit covers closed projector block and live nonprojector families",
            "passed": bool_string(r11_ok),
            "detail": f"r11_rows={len(r11)}",
            "timestamp_utc": TIMESTAMP,
        }
    )

    fallback = parse_csv(outputs["P8_Y5_R2FR_4093_FALLBACK_RESIDUAL_CONTRACT"])
    fallback_text = "\n".join(str(row) for row in fallback)
    fallback_ok = all(bound in fallback_text for bound in ["2.3e-5", "8.0e-5", "2.0e-2", "4.0e-5", "1.0e-8"])
    rows.append(
        {
            "check_id": "VAL4093_FALLBACK_CONTRACTS",
            "check": "fallback contracts carry sourced gamma beta zeta bounds",
            "passed": bool_string(fallback_ok),
            "detail": "requires gamma, beta, zeta1, zeta2, zeta3 bounds",
            "timestamp_utc": TIMESTAMP,
        }
    )

    claim_rows = parse_csv(outputs["P8_Y5_R2FR_4093_CLAIM_GATE"])
    no_public = all(row.get("public_claim") == "False" and row.get("valid_for_claim") == "False" for row in claim_rows)
    rows.append(
        {
            "check_id": "VAL4093_NO_PUBLIC_CLAIM",
            "check": "4093 does not promote public gamma/beta/zeta/local-GR claim",
            "passed": bool_string(no_public),
            "detail": "all public claims remain false",
            "timestamp_utc": TIMESTAMP,
        }
    )

    output_paths = list(outputs.values()) + [DOC_PATH, SCRIPT_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths)
    formalization_touched = any(is_under(path, FORMALIZATION) for path in output_paths)
    rows.append(
        {
            "check_id": "VAL4093_SCOPE",
            "check": "outputs stay in post-checkpoint-work and not formalization-workbench",
            "passed": bool_string(in_scope and not formalization_touched),
            "detail": f"doc={DOC_PATH}; csv_count={len(outputs)}",
            "timestamp_utc": TIMESTAMP,
        }
    )

    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
        compile_ok = True
        compile_detail = "py_compile passed"
    except Exception as exc:
        compile_ok = False
        compile_detail = f"py_compile failed: {exc}"
    rows.append(
        {
            "check_id": "VAL4093_SCRIPT_COMPILES",
            "check": "generator script compiles",
            "passed": bool_string(compile_ok),
            "detail": compile_detail,
            "timestamp_utc": TIMESTAMP,
        }
    )

    return rows


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4093_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['detail']}")
        raise SystemExit(1)

    print(f"4093 complete: {DECISION}")
    print(f"doc: {DOC_PATH}")
    print(f"csv_dir: {SOURCE_DIR}")
    print(f"validation: {validation_path}")


if __name__ == "__main__":
    main()

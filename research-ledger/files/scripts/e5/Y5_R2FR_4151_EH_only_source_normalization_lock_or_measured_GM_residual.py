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
DOC_PATH = ROOT / "4151-Y5-R2FR-EH-only-source-normalization-lock-or-measured-GM-residual.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_EH_ONLY_SOURCE_NORMALIZATION_4151"
CHECKPOINT_ID = "4151"
DECISION = "EH_ONLY_NEWTON_SOURCE_THEOREM_DERIVED_CONSTANT_KAPPA_PARENT_UNSIGNED_MEASURED_GM_RESIDUAL_ROWS_EMITTED"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4151_00_4150_doc": (
        ROOT / "4150-Y5-R2FR-response-doublet-Y5Y6-source-current-lock-or-Gamma-bound.md",
        "Go straight at the coupling/Newton problem",
        "4150 handoff naming Y5/Newton coupling as the next target.",
    ),
    "SRC4151_01_4150_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4150_NEXT_TARGET.csv",
        "attack the dominant Y5/Newton coupling blocker",
        "Machine-readable 4150 next-target row.",
    ),
    "SRC4151_02_source_stack": (
        SOURCE_DIR / "P8_SOURCE_NORMALIZATION_THEOREM_STACK.csv",
        "S5_Newton_gate",
        "Current Y5 source-normalization theorem stack.",
    ),
    "SRC4151_03_source_current_contract": (
        SOURCE_DIR / "P8_source_current_Ward_universality_CONTRACT.csv",
        "SC6_closed_calibrated_mass_projector",
        "Ward/source-current contract for calibrated mass projector.",
    ),
    "SRC4151_04_Ward_owner_contract": (
        SOURCE_DIR / "P8_Ward_source_owner_identity_CONTRACT.csv",
        "C4_constant_universal_coupling",
        "Ward owner contract naming constant universal coupling.",
    ),
    "SRC4151_05_4147_doc": (
        ROOT / "4147-Y5-R2FR-Jordan-frame-Geff-calibration-or-second-order-source-closure.md",
        "G_ref=1/(8 pi F_*)",
        "Jordan-frame constant-F coupling theorem.",
    ),
    "SRC4151_06_4147_Geff": (
        SOURCE_DIR / "P8_Y5_R2FR_4147_GEFF_CALIBRATION_THEOREM.csv",
        "GT4147_1_constant_F_calibration",
        "Machine-readable 4147 constant-F calibration theorem.",
    ),
    "SRC4151_07_constant_kappa": (
        SOURCE_DIR / "P8_constant_universal_Geff_kappa_CONTRACT.csv",
        "CU8_retained_residual_fallback",
        "Constant universal G_eff/kappa contract and fallback.",
    ),
    "SRC4151_08_superselection": (
        SOURCE_DIR / "P8_global_coupling_superselection_CONTRACT.csv",
        "GS7_scalar_branch_fallback",
        "Global coupling superselection contract and scalar fallback.",
    ),
    "SRC4151_09_runner_input": (
        SOURCE_DIR / "P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv",
        "P8_boundary_bulk_domain_mu_extra",
        "Existing measured-GM residual runner input.",
    ),
    "SRC4151_10_script": (
        SCRIPT_PATH,
        "EH_ONLY_NEWTON_SOURCE_THEOREM_DERIVED_CONSTANT_KAPPA",
        "This generator records the 4151 EH-only source-normalization attempt.",
    ),
}


def common() -> dict:
    return {
        "timestamp_utc": TIMESTAMP,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
    }


def write_csv(path: Path, rows: List[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def parse_csv(path: Path) -> List[dict]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def is_under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4151_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4151_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4151_EH_ONLY_NEWTON_THEOREM": SOURCE_DIR / "P8_Y5_R2FR_4151_EH_ONLY_NEWTON_THEOREM.csv",
        "P8_Y5_R2FR_4151_SOURCE_NORMALIZATION_PROOF": SOURCE_DIR / "P8_Y5_R2FR_4151_SOURCE_NORMALIZATION_PROOF.csv",
        "P8_Y5_R2FR_4151_CONSTANT_KAPPA_AUDIT": SOURCE_DIR / "P8_Y5_R2FR_4151_CONSTANT_KAPPA_AUDIT.csv",
        "P8_Y5_R2FR_4151_MEASURED_GM_RESIDUAL_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4151_MEASURED_GM_RESIDUAL_ROWS.csv",
        "P8_Y5_R2FR_4151_NEWTON_PPN_INTERFACE": SOURCE_DIR / "P8_Y5_R2FR_4151_NEWTON_PPN_INTERFACE.csv",
        "P8_Y5_R2FR_4151_DECISION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4151_DECISION_GATES.csv",
        "P8_Y5_R2FR_4151_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4151_STATUS.csv",
        "P8_Y5_R2FR_4151_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4151_NEXT_TARGET.csv",
    }


def source_rows() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        exists = path.exists()
        text = read_text(path) if exists and path.is_file() else ""
        rows.append(
            {
                **common(),
                "source_id": source_id,
                "path": str(path),
                "needle": needle,
                "role": role,
                "exists": str(exists),
                "needle_found": str(bool(exists and needle in text)),
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def theorem_rows() -> List[dict]:
    return [
        {
            **common(),
            "theorem_id": "EHN4151_0_action_branch",
            "statement": "same-frame EH-only source branch",
            "formula": "S_local=(1/(16 pi G_*)) int sqrt(-g_obs) R[g_obs] + S_matter[psi,g_obs] + S_extra",
            "derivation": "If S_extra has zero local monopole, zero PPN projection, or is absent/topological, the active Newton source is the Hilbert stress of S_matter in the same observed frame.",
            "status": "CONDITIONAL_BRANCH_DEFINED",
            "current_corpus_claim": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "EHN4151_1_poisson_reduction",
            "statement": "EH-only Poisson source normalization",
            "formula": "nabla^2 Phi=4 pi G_* rho_H + S_extra_00/2; mu_obs=lim_{r->infty} r^2 partial_r Phi=G_* M_H+mu_extra",
            "derivation": "The weak-field 00 equation and Gauss law fix the exterior monopole. With mu_extra=0, the measured Newtonian source is exactly G_* M_H.",
            "status": "NEWTON_SOURCE_THEOREM_DERIVED",
            "current_corpus_claim": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "EHN4151_2_Y5_lock",
            "statement": "Y5 source-current zero condition",
            "formula": "J_Y5=delta_Z mu_extra|_{Z=0}; if mu_extra=0 as a parent identity and G_* is global, then J_Y5=0",
            "derivation": "Y5 is not a separate response-doublet source current when the only active monopole is the same-frame EH/Hilbert source and all non-EH source normalization terms are parent-zero/topological.",
            "status": "Y5_LOCK_THEOREM_DERIVED_CONDITIONAL",
            "current_corpus_claim": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "EHN4151_3_constant_offset_policy",
            "statement": "Newton constant calibration is not a prediction of numerical G",
            "formula": "G_* constant may be measured once; only dG_*=0 and source universality are physics claims here",
            "derivation": "GR itself uses a measured constant G. The MTS local branch may inherit that role if the parent derives or explicitly declares G_* as a global/superselection coupling, but this checkpoint does not predict the numerical value of G.",
            "status": "NO_ABSOLUTE_G_CLAIM",
            "current_corpus_claim": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "EHN4151_4_failure_law",
            "statement": "measured-GM failure residual",
            "formula": "mu_obs=G_eff M_H (1+epsilon_mu); dln mu_obs=dln G_eff+dln M_H+dln(1+epsilon_mu)",
            "derivation": "Any time, radius, range, species, frame, boundary, memory, or domain dependence that survives cannot be absorbed into a one-time GM calibration; it becomes the retained residual branch.",
            "status": "RESIDUAL_LAW_DERIVED",
            "current_corpus_claim": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def proof_rows() -> List[dict]:
    return [
        {
            **common(),
            "proof_id": "P4151_0_same_frame",
            "step": "same observed frame",
            "mathematical_step": "all matter clocks and the EH operator vary g_obs/e_obs",
            "why_needed": "prevents a fake Newton coefficient caused by frame conversion",
            "status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "residual_if_failed": "delta_frame_source",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "proof_id": "P4151_1_constant_coupling",
            "step": "constant universal coupling",
            "mathematical_step": "partial_t G_*=partial_r G_*=partial_lambda G_*=partial_A G_*=partial_Z G_*=0",
            "why_needed": "makes G_* a one-time calibration rather than a local scalar/source-normalization field",
            "status": "NOT_PARENT_DERIVED",
            "residual_if_failed": "dln_Geff_dt; partial_r_ln_Geff; alpha(lambda); eta_source_AB; delta_kappa_source",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "proof_id": "P4151_2_Hilbert_mass",
            "step": "closed Hilbert mass flux",
            "mathematical_step": "M_H=int rho_H d^3x and dM_H/dt=0 for isolated compact source",
            "why_needed": "separates coupling drift from mass-flux drift in measured GM",
            "status": "CONDITIONAL_FLUX_CLOSURE_OPEN",
            "residual_if_failed": "dln_Meff_dt",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "proof_id": "P4151_3_no_extra_monopole",
            "step": "zero non-EH monopole",
            "mathematical_step": "mu_extra=sum_i mu_i^extra=0",
            "why_needed": "kills source-normalization operator c_domain_source_normalization_operator",
            "status": "NOT_PARENT_DERIVED",
            "residual_if_failed": "epsilon_mu; c_domain_source_normalization_operator",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "proof_id": "P4151_4_Gauss_law",
            "step": "Gauss monopole readout",
            "mathematical_step": "mu_obs=lim_{r->infty} r^2 partial_r Phi=G_* M_H+mu_extra",
            "why_needed": "turns field equation into operational measured GM",
            "status": "DERIVED",
            "residual_if_failed": "source readout ambiguous",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "proof_id": "P4151_5_second_order",
            "step": "PPN beta source closure",
            "mathematical_step": "S_beta^source=0 or |delta_beta_source| <= beta_gate after Newton normalization",
            "why_needed": "Newton calibration alone does not prove local GR through beta order",
            "status": "BOUND_ROW_ONLY",
            "residual_if_failed": "delta_beta_source",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def kappa_audit_rows() -> List[dict]:
    return [
        {
            **common(),
            "audit_id": "KA4151_0_GR_comparison",
            "gate": "GR uses a measured constant G, not a derived numerical value",
            "formula": "G_N is an empirical constant in local GR/Newton",
            "current_status": "CALIBRATION_ALLOWED",
            "decision": "MTS may inherit a measured constant if parent derives constancy/universality",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "audit_id": "KA4151_1_global_or_superselection",
            "gate": "G_* or kappa_* is not a local field",
            "formula": "delta_local kappa_*=0 and d kappa_*=0",
            "current_status": "NOT_PARENT_DERIVED",
            "decision": "constant-coupling parent signature still missing",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "audit_id": "KA4151_2_no_MTS_dependence",
            "gate": "coupling independent of MTS memory/domain/projector/class data",
            "formula": "partial_Z kappa_*=partial_IQ kappa_*=partial_D kappa_*=partial_boundary kappa_*=0",
            "current_status": "NOT_PARENT_DERIVED",
            "decision": "local memory/domain coupling drift remains possible",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "audit_id": "KA4151_3_no_source_label",
            "gate": "coupling independent of species/source/material labels",
            "formula": "partial_A kappa_*=partial_source kappa_*=0",
            "current_status": "NOT_PARENT_DERIVED",
            "decision": "source-charge row remains active",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "audit_id": "KA4151_4_Bianchi_limit",
            "gate": "Bianchi does not erase variable coupling unless matter is same-frame separately conserved for arbitrary sources",
            "formula": "q_kappa^nu=kappa_*^-1 P_loc[T_obs^{mu nu} nabla_mu kappa_*]",
            "current_status": "RESIDUAL_IF_VARIABLE",
            "decision": "retain delta_kappa_source unless constant-coupling theorem closes",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def residual_rows() -> List[dict]:
    return [
        {
            **common(),
            "component_id": "R4151_0_epsilon_mu",
            "symbol": "epsilon_mu",
            "definition": "epsilon_mu=mu_extra/(G_eff M_H)",
            "formula": "mu_obs=G_eff M_H (1+epsilon_mu)",
            "observable_link": "gamma; beta; alpha3; xi; operator_ledger",
            "current_status": "MISSING_NUMERIC_OR_PARENT_ZERO",
            "score_ready": "False",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            **common(),
            "component_id": "R4151_1_Gdot",
            "symbol": "dln_Geff_dt",
            "definition": "time drift of effective coupling",
            "formula": "dln mu_obs/dt=dln G_eff/dt+dln M_H/dt+dln(1+epsilon_mu)/dt",
            "observable_link": "Gdot_over_G; clocks; orbital timing",
            "current_status": "MISSING_NUMERIC_OR_PARENT_ZERO",
            "score_ready": "False",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            **common(),
            "component_id": "R4151_2_mass_flux",
            "symbol": "dln_MH_dt",
            "definition": "Hilbert mass-flux drift",
            "formula": "dln_M_H/dt=0 only after closed Pi_M/Hilbert flux theorem",
            "observable_link": "Gdot_over_G; beta source; orbital dynamics",
            "current_status": "CONDITIONAL_FLUX_CLOSURE_OPEN",
            "score_ready": "False",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            **common(),
            "component_id": "R4151_3_source_charge",
            "symbol": "eta_source_AB",
            "definition": "composition/source-label dependence of active gravitational source",
            "formula": "eta_source_AB ~= Delta_AB ln mu_obs",
            "observable_link": "source-charge WEP; eta_source_AB",
            "current_status": "MISSING_SOURCE_BLINDNESS_THEOREM_OR_NUMERIC_BOUND",
            "score_ready": "False",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            **common(),
            "component_id": "R4151_4_radial_hair",
            "symbol": "partial_r_ln_mu_obs",
            "definition": "radial dependence of measured source normalization",
            "formula": "partial_r ln mu_obs=partial_r ln G_eff+partial_r ln M_H+partial_r ln(1+epsilon_mu)",
            "observable_link": "PPN; fifth force; radial source hair",
            "current_status": "MISSING_RADIAL_ZERO_OR_PROFILE",
            "score_ready": "False",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            **common(),
            "component_id": "R4151_5_range_dependence",
            "symbol": "alpha(lambda)",
            "definition": "finite-range source/coupling hair",
            "formula": "G_eff(r,lambda)=G_*[1+alpha(lambda) exp(-r/lambda)] or theorem-zero",
            "observable_link": "R10 fifth-force curve",
            "current_status": "MISSING_EXECUTABLE_ALPHA_LAMBDA_CURVE_OR_ZERO_THEOREM",
            "score_ready": "False",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            **common(),
            "component_id": "R4151_6_frame_split",
            "symbol": "delta_frame_source",
            "definition": "source readout differs between matter/clock/EH frames",
            "formula": "Delta_frame ln mu_obs=0 required for same-frame source normalization",
            "observable_link": "WEP; clocks; operator ledger",
            "current_status": "MISSING_SAME_FRAME_PARENT_SIGNATURE",
            "score_ready": "False",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            **common(),
            "component_id": "R4151_7_beta_source",
            "symbol": "delta_beta_source",
            "definition": "second-order PPN source-normalization residue",
            "formula": "delta_beta_source=-1/(2N_U2)<L_00^-1 S_beta^source,U^2>",
            "observable_link": "PPN beta",
            "current_status": "MISSING_SECOND_ORDER_SOURCE_THEOREM_OR_NUMERIC_BOUND",
            "score_ready": "False",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def interface_rows() -> List[dict]:
    return [
        {
            **common(),
            "interface_id": "NPI4151_0_Newton",
            "claim": "Newtonian source normalization",
            "pass_condition": "same-frame EH source, constant G_*, closed M_H, mu_extra=0",
            "current_result": "CONDITIONAL_THEOREM_ONLY",
            "residual_if_failed": "epsilon_mu; dln_Geff_dt; dln_MH_dt",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "interface_id": "NPI4151_1_Y5",
            "claim": "response-doublet Y5 current silence",
            "pass_condition": "J_Y5=delta_Z mu_extra|_0=0 and kappa_* has no Z dependence",
            "current_result": "Y5_FORMULA_DERIVED_LOCK_UNSIGNED",
            "residual_if_failed": "J_Y5; c_domain_source_normalization_operator",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "interface_id": "NPI4151_2_PPN_beta",
            "claim": "local GR beta source closure",
            "pass_condition": "S_beta^source=0 through O(v^4) after Newton normalization",
            "current_result": "BOUND_ROW_ONLY",
            "residual_if_failed": "delta_beta_source",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "interface_id": "NPI4151_3_R10",
            "claim": "no finite-range source-coupling hair",
            "pass_condition": "alpha(lambda)=0 by theorem or real curve comparison passes",
            "current_result": "CURVE_OR_ZERO_THEOREM_REQUIRED",
            "residual_if_failed": "alpha(lambda)",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "interface_id": "NPI4151_4_local_GR",
            "claim": "local GR promotion",
            "pass_condition": "Newton, PPN beta, gamma, source-charge, clocks, R10, and Y6 stress all closed/scored",
            "current_result": "NOT_CLAIMED",
            "residual_if_failed": "full local residual vector",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[dict]:
    return [
        {
            **common(),
            "gate_id": "DG4151_0_EH_theorem",
            "question": "does same-frame EH-only plus constant coupling derive the Newton source normalization?",
            "answer": "yes, conditionally",
            "decision": "EH_ONLY_NEWTON_THEOREM_DERIVED",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            **common(),
            "gate_id": "DG4151_1_parent_signature",
            "question": "does the current parent corpus derive constant/global kappa and zero mu_extra?",
            "answer": "no",
            "decision": "CONSTANT_KAPPA_AND_MU_EXTRA_ZERO_UNSIGNED",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            **common(),
            "gate_id": "DG4151_2_residuals",
            "question": "are measured-GM residual rows explicit enough for future tests?",
            "answer": "yes, symbolically; numeric/source rows still missing",
            "decision": "MEASURED_GM_RESIDUAL_ROWS_EMITTED_NONCLAIM",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            **common(),
            "gate_id": "DG4151_3_next",
            "question": "best next derivation target",
            "answer": "try to derive constant coupling as a topological zero-form/superselection branch",
            "decision": "NEXT_TARGET_TOPOLOGICAL_KAPPA_ZERO_FORM_OR_DRIFT_RUNNER",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def status_rows() -> List[dict]:
    return [
        {
            **common(),
            "result": DECISION,
            "EH_only_Newton_source_theorem_derived": "True",
            "Y5_current_zero_condition_derived": "True",
            "measured_GM_residual_law_derived": "True",
            "constant_kappa_parent_signed": "False",
            "mu_extra_zero_parent_signed": "False",
            "mass_flux_closure_signed": "False",
            "second_order_beta_source_closed": "False",
            "measured_GM_residual_rows_emitted": "True",
            "Newton_claimed": "False",
            "local_gr_claimed": "False",
            "next_target": "4152-Y5-R2FR-topological-zero-form-kappa-superselection-or-coupling-drift-runner.md",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> List[dict]:
    return [
        {
            **common(),
            "next_id": "NEXT4151_0",
            "target_doc": "4152-Y5-R2FR-topological-zero-form-kappa-superselection-or-coupling-drift-runner.md",
            "target_script": "scripts/Y5_R2FR_4152_topological_zero_form_kappa_superselection_or_coupling_drift_runner.py",
            "objective": "try to derive constant universal kappa/G as a topological zero-form or parent superselection sector, rather than adopting it as a closure premise; if the derivation fails, turn coupling drift/source/range rows into the next executable residual runner",
            "success_gate": "d kappa_*=0, no local Euler equation, no MTS/domain/memory/source/range/frame dependence, no extra stress from the constancy mechanism, and no hidden Bianchi exchange; otherwise retain dln_Geff_dt, eta_source_AB, alpha(lambda), delta_kappa_source, and measured-GM residual rows",
            "reason": "4151 proves the EH-only Newton source theorem conditionally; the remaining root issue is whether constant kappa is derived or only assumed.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def write_doc(outputs: Dict[str, Path]) -> None:
    text = f"""# 4151 - EH-Only Source Normalization Lock Or Measured-GM Residual

Timestamp UTC: `{TIMESTAMP}`  
Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`

## Purpose
This checkpoint goes directly at the coupling/Newton problem isolated in 4150.

The target is not to predict the numerical value of Newton's constant. GR does not derive that number either. The target is sharper:

Can MTS derive a local branch where `G` is a single measured constant and the active mass source is the same-frame Hilbert source, with no hidden source-normalization current?

## EH-Only Newton Source Theorem
Assume a local branch

`S_local=(1/(16 pi G_*)) int sqrt(-g_obs) R[g_obs] + S_matter[psi,g_obs] + S_extra`.

If:

- matter, clocks, and the EH operator use the same observed frame `g_obs`;
- `G_*` or `kappa_*` is a global/superselection coupling with no local, range, species, memory, domain, boundary, or frame dependence;
- the Hilbert mass flux is closed for the isolated compact source;
- `S_extra` has zero monopole and zero relevant PPN projection;

then the weak-field Gauss law gives

`nabla^2 Phi=4 pi G_* rho_H + S_extra_00/2`,

and therefore

`mu_obs=lim_{{r->infty}} r^2 partial_r Phi=G_* M_H+mu_extra`.

If `mu_extra=0`, this becomes

`mu_obs=G_* M_H`.

So the Y5 source-normalization current vanishes:

`J_Y5=delta_Z mu_extra|_{{Z=0}}=0`.

That is the clean Newton/source theorem.

## What Is Still Unsigned
The theorem is derived as a conditional theorem, not promoted as a claim.

The current corpus still does not parent-sign:

- `G_*`/`kappa_*` as a derived global/superselection coupling;
- `partial_t G_*=partial_r G_*=partial_lambda G_*=partial_A G_*=partial_Z G_*=0`;
- `mu_extra=0` for boundary/domain/projector/source-normalization channels;
- closed Hilbert mass flux through the measured source projector;
- second-order PPN source closure.

Therefore this checkpoint does not claim Newton, PPN, or local GR.

## Residual Law When The Theorem Fails
The honest failure branch is now explicit:

`mu_obs=G_eff M_H (1+epsilon_mu)`.

Taking derivatives,

`dln mu_obs=dln G_eff+dln M_H+dln(1+epsilon_mu)`.

So no one is allowed to hide local physics inside a one-time measured `GM`. Any surviving dependence becomes one of:

- `dln_Geff_dt`;
- `dln_MH_dt`;
- `eta_source_AB`;
- `partial_r_ln_mu_obs`;
- `alpha(lambda)`;
- `delta_frame_source`;
- `delta_beta_source`;
- `c_domain_source_normalization_operator`.

## Coupling Interpretation
This is the useful answer to the "does GR derive Newton's constant?" issue:

GR uses `G` as an empirical constant. MTS does not need to predict its numerical value to reduce to GR/Newton. MTS does need to derive why the local branch has one constant universal coupling rather than a field/source/range/domain-dependent effective coupling.

So the root target is now:

`d kappa_*=0`

with no hidden local source current or exchange stress.

## Current Verdict
| Gate | Result | Meaning |
|---|---|---|
| EH-only Newton theorem | DERIVED CONDITIONALLY | proves `mu_obs=G_* M_H` if the source branch is parent-signed |
| Y5 current formula | DERIVED CONDITIONALLY | `J_Y5=delta_Z mu_extra|_0` |
| constant kappa/G | UNSIGNED | still the root parent-action target |
| extra source monopole | UNSIGNED | `mu_extra` remains active |
| measured-GM residual rows | EMITTED | branch is testable/nonclaim if theorem fails |
| Newton/local GR | NOT CLAIMED | source, beta, R10 and Y6 gates remain open |

## Outputs
- `{outputs["P8_Y5_R2FR_4151_SOURCE_REGISTER"]}`
- `{outputs["P8_Y5_R2FR_4151_EH_ONLY_NEWTON_THEOREM"]}`
- `{outputs["P8_Y5_R2FR_4151_SOURCE_NORMALIZATION_PROOF"]}`
- `{outputs["P8_Y5_R2FR_4151_CONSTANT_KAPPA_AUDIT"]}`
- `{outputs["P8_Y5_R2FR_4151_MEASURED_GM_RESIDUAL_ROWS"]}`
- `{outputs["P8_Y5_R2FR_4151_NEWTON_PPN_INTERFACE"]}`
- `{outputs["P8_Y5_R2FR_4151_DECISION_GATES"]}`
- `{outputs["P8_Y5_R2FR_4151_STATUS"]}`
- `{outputs["P8_Y5_R2FR_4151_NEXT_TARGET"]}`

## Next Target
- `4152-Y5-R2FR-topological-zero-form-kappa-superselection-or-coupling-drift-runner.md`
- Try to derive `d kappa_*=0` as a topological zero-form/integration-constant or parent superselection result. If that fails, build the executable coupling-drift/source/range residual runner.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    write_csv(outputs["P8_Y5_R2FR_4151_SOURCE_REGISTER"], source_rows())
    write_csv(outputs["P8_Y5_R2FR_4151_EH_ONLY_NEWTON_THEOREM"], theorem_rows())
    write_csv(outputs["P8_Y5_R2FR_4151_SOURCE_NORMALIZATION_PROOF"], proof_rows())
    write_csv(outputs["P8_Y5_R2FR_4151_CONSTANT_KAPPA_AUDIT"], kappa_audit_rows())
    write_csv(outputs["P8_Y5_R2FR_4151_MEASURED_GM_RESIDUAL_ROWS"], residual_rows())
    write_csv(outputs["P8_Y5_R2FR_4151_NEWTON_PPN_INTERFACE"], interface_rows())
    write_csv(outputs["P8_Y5_R2FR_4151_DECISION_GATES"], decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4151_STATUS"], status_rows())
    write_csv(outputs["P8_Y5_R2FR_4151_NEXT_TARGET"], next_rows())
    write_doc(outputs)
    return outputs


def validate(outputs: Dict[str, Path]) -> List[dict]:
    checks: List[dict] = []

    def add(check_id: str, requirement: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                **common(),
                "check_id": check_id,
                "requirement": requirement,
                "passed": str(bool(passed)),
                "detail": detail,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )

    sources = source_rows()
    add(
        "VAL4151_0_sources",
        "all cited source paths exist and contain required needles",
        all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources),
        "; ".join(f"{row['source_id']} exists={row['exists']} needle={row['needle_found']}" for row in sources),
    )

    csv_ok = True
    csv_detail: List[str] = []
    for name, path in outputs.items():
        try:
            rows = parse_csv(path)
            csv_detail.append(f"{name}:{len(rows)}")
            csv_ok = csv_ok and bool(rows)
        except Exception as exc:
            csv_ok = False
            csv_detail.append(f"{name}:ERR {exc!r}")
    add("VAL4151_1_csv_parse", "all generated CSV outputs parse and are nonempty", csv_ok, ", ".join(csv_detail))

    doc_text = read_text(DOC_PATH) if DOC_PATH.exists() else ""
    doc_tokens = [
        DECISION,
        "mu_obs=G_* M_H",
        "J_Y5=delta_Z mu_extra",
        "dln mu_obs=dln G_eff+dln M_H+dln(1+epsilon_mu)",
        "d kappa_*=0",
        "4152-Y5-R2FR-topological-zero-form-kappa-superselection-or-coupling-drift-runner.md",
    ]
    add("VAL4151_2_doc_tokens", "document records EH-only theorem, Y5 lock, residual law, kappa target and next target", all(token in doc_text for token in doc_tokens), "tokens checked")

    theorem_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4151_EH_ONLY_NEWTON_THEOREM"]))
    theorem_tokens = ["NEWTON_SOURCE_THEOREM_DERIVED", "Y5_LOCK_THEOREM_DERIVED_CONDITIONAL", "NO_ABSOLUTE_G_CLAIM", "RESIDUAL_LAW_DERIVED"]
    add("VAL4151_3_theorem", "EH-only Newton source theorem and residual law are recorded", all(token in theorem_text for token in theorem_tokens), "theorem tokens checked")

    proof_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4151_SOURCE_NORMALIZATION_PROOF"]))
    proof_tokens = ["CONDITIONAL_NOT_PARENT_SIGNED", "NOT_PARENT_DERIVED", "CONDITIONAL_FLUX_CLOSURE_OPEN", "BOUND_ROW_ONLY"]
    add("VAL4151_4_proof", "proof stack records same-frame, constant coupling, mass flux, mu_extra and beta requirements", all(token in proof_text for token in proof_tokens), "proof tokens checked")

    audit_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4151_CONSTANT_KAPPA_AUDIT"]))
    audit_tokens = ["CALIBRATION_ALLOWED", "NOT_PARENT_DERIVED", "q_kappa^nu=kappa_*^-1 P_loc", "delta_kappa_source"]
    add("VAL4151_5_kappa_audit", "kappa audit distinguishes measured constant calibration from derived constancy", all(token in audit_text for token in audit_tokens), "audit tokens checked")

    residual_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4151_MEASURED_GM_RESIDUAL_ROWS"]))
    residual_tokens = ["epsilon_mu", "dln_Geff_dt", "dln_MH_dt", "eta_source_AB", "partial_r_ln_mu_obs", "alpha(lambda)", "delta_frame_source", "delta_beta_source"]
    add("VAL4151_6_residuals", "measured-GM residual rows cover source, drift, mass flux, species, radial, range, frame and beta branches", all(token in residual_text for token in residual_tokens), "residual tokens checked")

    interface_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4151_NEWTON_PPN_INTERFACE"]))
    interface_tokens = ["CONDITIONAL_THEOREM_ONLY", "Y5_FORMULA_DERIVED_LOCK_UNSIGNED", "BOUND_ROW_ONLY", "CURVE_OR_ZERO_THEOREM_REQUIRED", "NOT_CLAIMED"]
    add("VAL4151_7_interface", "Newton/PPN/R10/local-GR interface remains nonclaim with explicit blockers", all(token in interface_text for token in interface_tokens), "interface tokens checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4151_STATUS"])
    status_ok = (
        len(status) == 1
        and status[0].get("result") == DECISION
        and status[0].get("EH_only_Newton_source_theorem_derived") == "True"
        and status[0].get("Y5_current_zero_condition_derived") == "True"
        and status[0].get("measured_GM_residual_law_derived") == "True"
        and status[0].get("constant_kappa_parent_signed") == "False"
        and status[0].get("mu_extra_zero_parent_signed") == "False"
        and status[0].get("measured_GM_residual_rows_emitted") == "True"
        and status[0].get("Newton_claimed") == "False"
        and status[0].get("local_gr_claimed") == "False"
    )
    add("VAL4151_8_status", "status records derived theorem, unsigned parent gates, residual rows and no Newton/local-GR claim", status_ok, str(status))

    next_target = parse_csv(outputs["P8_Y5_R2FR_4151_NEXT_TARGET"])
    next_ok = len(next_target) == 1 and next_target[0].get("target_doc") == "4152-Y5-R2FR-topological-zero-form-kappa-superselection-or-coupling-drift-runner.md"
    add("VAL4151_9_next", "next target attacks topological zero-form/superselection kappa or coupling-drift runner", next_ok, str(next_target))

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    no_score = all(row.get("score_ready", "False") in ("False", "") for row in all_rows)
    add("VAL4151_10_no_claim", "all outputs remain nonclaim and not score-ready", no_claim and no_score, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(
            ("4151-Y5-R2FR" in item.name or "R2FR_4151" in item.name)
            for item in FORMALIZATION.rglob("*")
        )
    add("VAL4151_11_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4151_12_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4151_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    print(f"wrote: {DOC_PATH}")
    for path in outputs.values():
        print(f"wrote: {path}")
    print(f"validation: {validation_path}")
    if failed:
        print("failed checks:")
        for row in failed:
            print(f"- {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("all validation checks passed")


if __name__ == "__main__":
    main()

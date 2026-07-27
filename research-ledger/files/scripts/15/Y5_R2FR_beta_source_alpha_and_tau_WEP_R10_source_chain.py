from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1810"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC_PATH = ROOT / "1810-Y5-R2FR-beta-source-alpha-and-tau-WEP-R10-source-chain.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1810_0_1809_doc",
        "source_key": "1809_doc",
        "source_path": ROOT / "1809-Y5-R2FR-tau-clock-Xhat-normalization-or-alpha-WEP-R10-projection-source.md",
        "needles": ["NEXT1809_0_primary", "TG1809_3_R10_transfer"],
        "role": "current handoff selecting beta-source-alpha and tau WEP/R10 source chain.",
    },
    {
        "source_id": "SRC1810_1_1809_validation",
        "source_key": "1809_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1809_VALIDATION.csv",
        "needles": ["VAL1809_OVERALL", "PASS"],
        "role": "confirms 1809 passed before 1810 starts.",
    },
    {
        "source_id": "SRC1810_2_1809_wep",
        "source_key": "1809_wep_projection",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1809_ALPHA_WEP_PROJECTION_LEDGER.csv",
        "needles": ["AWP1809_0_alpha_Coulomb", "4.797780522732e-05"],
        "role": "current WEP alpha pressure rows.",
    },
    {
        "source_id": "SRC1810_3_1809_r10",
        "source_key": "1809_r10_projection",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1809_ALPHA_R10_PROJECTION_LEDGER.csv",
        "needles": ["RAP1809_0_product_law", "RAP1809_2_clock_to_R10_transfer"],
        "role": "current R10 product-law refusal rows.",
    },
    {
        "source_id": "SRC1810_4_1054_doc",
        "source_key": "1054_zero_theorem",
        "source_path": ROOT / "1054-Y5-R10-beta-source-alpha-zero-theorem-or-first-numeric-prior-width.md",
        "needles": ["FP1054_6_verdict", "NPW1054_0_alpha_WEP_product", "DEC1054_2_best_next"],
        "role": "older beta-source-alpha zero theorem and first numeric product-width audit.",
    },
    {
        "source_id": "SRC1810_5_1054_validation",
        "source_key": "1054_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1054_VALIDATION.csv",
        "needles": ["V1054_SUMMARY", "pass"],
        "role": "confirms old zero theorem checkpoint passed as a nonclaim audit.",
    },
    {
        "source_id": "SRC1810_6_1593_doc",
        "source_key": "1593_canonical_coupling",
        "source_path": ROOT / "1593-Y5-R2FR-canonical-coupling-zero-theorem-or-finite-beta-source-rows.md",
        "needles": ["ZTH1593_8_verdict", "FBR1593_2_beta_product"],
        "role": "current R2FR canonical coupling zero theorem and finite beta row fallback.",
    },
    {
        "source_id": "SRC1810_7_1593_beta_rows",
        "source_key": "1593_finite_beta_rows",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1593_FINITE_BETA_SOURCE_ROWS.csv",
        "needles": ["FBR1593_11_verdict", "FINITE_BETA_SOURCE_ROWS_READY_NONCLAIM"],
        "role": "finite beta/source row schema retained after zero theorem fails.",
    },
    {
        "source_id": "SRC1810_8_1594_doc",
        "source_key": "1594_validator",
        "source_path": ROOT / "1594-Y5-R2FR-action-weight-exclusion-or-beta-source-acquisition-validator.md",
        "needles": ["AWT1594_7_verdict", "BVR1594_0_FBR1593_0_beta_source"],
        "role": "strict beta/source row validator and action-weight exclusion audit.",
    },
    {
        "source_id": "SRC1810_9_1594_validator_results",
        "source_key": "1594_validator_results",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1594_BETA_ROW_VALIDATOR_RESULTS.csv",
        "needles": ["BVR1594_0_FBR1593_0_beta_source", "REJECT"],
        "role": "confirms current beta source rows are rejected for claim scoring.",
    },
    {
        "source_id": "SRC1810_10_1694_doc",
        "source_key": "1694_source_backed_beta",
        "source_path": ROOT / "1694-Y5-R2FR-action-weight-exclusion-or-first-source-backed-beta-current-branch.md",
        "needles": ["BDW1694_0_MICROSCOPE_Delta_w_tau_bound_anchor", "NONCLAIM_ONLY"],
        "role": "current first source-backed WEP product anchor for Delta_w*tau_WEP.",
    },
    {
        "source_id": "SRC1810_11_1694_beta_delta_rows",
        "source_key": "1694_beta_delta_rows",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1694_SOURCE_BACKED_BETA_DELTAW_CURRENT_ROWS.csv",
        "needles": ["BDW1694_0_MICROSCOPE_Delta_w_tau_bound_anchor", "2.8e-15"],
        "role": "source-backed product anchor, not an MTS prediction row.",
    },
    {
        "source_id": "SRC1810_12_1695_doc",
        "source_key": "1695_tau_wep",
        "source_path": ROOT / "1695-Y5-R2FR-no-source-only-slot-theorem-or-tau-WEP-projection-current-branch.md",
        "needles": ["NST1695_7_verdict", "TAU1695_7_parser_status"],
        "role": "no-source-only theorem and tau_WEP projection/current branch status.",
    },
    {
        "source_id": "SRC1810_13_1695_tau_wep",
        "source_key": "1695_tau_wep_rows",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1695_TAU_WEP_PROJECTION_READINESS.csv",
        "needles": ["TAU1695_6_tau_min", "BLOCKED"],
        "role": "tau_WEP readiness and tau_min blocker rows.",
    },
    {
        "source_id": "SRC1810_14_1702_doc",
        "source_key": "1702_product_runner",
        "source_path": ROOT / "1702-Y5-R2FR-readout-commutator-ledger-and-first-arena-product-runner.md",
        "needles": ["WEP1702_4_refusal", "RUN1702_2_r10_score"],
        "role": "first arena product runner and refusal matrix.",
    },
    {
        "source_id": "SRC1810_15_1702_wep_product",
        "source_key": "1702_wep_product",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1702_WEP_SOURCE_WEIGHT_PRODUCT_ROW.csv",
        "needles": ["WEP1702_0_delta_w", "REFUSAL_ACTIVE"],
        "role": "WEP source-weight product row requirements.",
    },
    {
        "source_id": "SRC1810_16_1780_doc",
        "source_key": "1780_signature",
        "source_path": ROOT / "1780-Y5-R2FR-q-Dq-tau-source-functor-signature-or-Delta-frame-tau-first-row.md",
        "needles": ["QTS1780_7_verdict", "FTZ1780_4_current_verdict"],
        "role": "current q/Dq/tau/source-functor signature theorem attempt.",
    },
    {
        "source_id": "SRC1810_17_1780_signature_gate",
        "source_key": "1780_signature_gate",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1780_Q_DQ_TAU_SOURCE_FUNCTOR_SIGNATURE_GATE.csv",
        "needles": ["QTS1780_7_verdict", "SIGNATURE_NOT_SIGNED"],
        "role": "parent signature clauses needed before source/tau bridge can be promoted.",
    },
    {
        "source_id": "SRC1810_18_1780_delta_frame_tau",
        "source_key": "1780_delta_frame_tau",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1780_DELTA_FRAME_TAU_FIRST_ROW_SCHEMA.csv",
        "needles": ["DFT1780_6_total_abs", "MISSING_COMPONENT_VALUES_AND_COMMON_NORM"],
        "role": "residual fallback schema if q/Dq/tau/source functor signature remains unsigned.",
    },
]


OUTPUTS: dict[str, Path] = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1810_SOURCE_REGISTER.csv",
    "zero_theorem_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1810_BETA_SOURCE_ALPHA_ZERO_THEOREM_AUDIT.csv",
    "finite_product_widths": RESIDUALS / "P8_Y5_PARENT_QLOC_1810_FINITE_PRODUCT_WIDTH_CHAIN.csv",
    "tau_projection_chain": RESIDUALS / "P8_Y5_PARENT_QLOC_1810_TAU_WEP_R10_SOURCE_CHAIN.csv",
    "arena_projection_bridge": RESIDUALS / "P8_Y5_PARENT_QLOC_1810_ARENA_PROJECTION_BRIDGE.csv",
    "parent_signature_contract": RESIDUALS / "P8_Y5_PARENT_QLOC_1810_PARENT_SIGNATURE_CONTRACT.csv",
    "residual_component_schema": RESIDUALS / "P8_Y5_PARENT_QLOC_1810_DELTA_FRAME_TAU_RESIDUAL_SCHEMA.csv",
    "mts_r10_template": RESIDUALS / "R10_alpha_lambda_curve_MTS_1810_BETA_TAU_SOURCE_CHAIN_TEMPLATE_NONCLAIM.csv",
    "runner_refusal": RESIDUALS / "P8_Y5_PARENT_QLOC_1810_RUNNER_REFUSAL_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1810_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1810_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1810_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1810_VALIDATION.csv",
}


def ensure_dirs() -> None:
    for path in {RESIDUALS, MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE}:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def boolish(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "yes", "1", "pass", "passed"}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    headers = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["source_path"]
        text = read_text(path)
        exists = path.exists()
        needles = source["needles"]
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": exists,
                "needles": ";".join(needles),
                "needles_present": exists and not missing,
                "missing_needles": ";".join(missing),
                "role": source["role"],
            }
        )
    return rows


def zero_theorem_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "BZA1810_0_chain_rule_core",
            "claim_piece": "beta_source_alpha zero from vertical blindness",
            "mathematical_form": "beta_source_alpha := partial_Xhat ln m_source_eff or partial_Xhat ln alpha_EM; if S_matter and theta_A factor through q and v in ker(Dq), then delta_v S_matter=0 and beta_source_alpha=0",
            "proof_status": "EXACT_CONDITIONAL_CHAIN_RULE",
            "missing_for_current_claim": "parent q/Dq signature; matter functor; constant/alpha owner; source/readout ownership; boundary/radiative silence",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "BZA1810_1_q_Dq_signature",
            "claim_piece": "hidden generator is quotient-vertical",
            "mathematical_form": "Dq[v_X]=0 for the retained alpha/source/coupling direction",
            "proof_status": "NOT_PARENT_SIGNED",
            "missing_for_current_claim": "QTS1780_0..QTS1780_2 and explicit vertical basis with Dq kernel",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "BZA1810_2_matter_functor",
            "claim_piece": "ordinary matter descends through observed coframe",
            "mathematical_form": "S_ord=sum_A S_A[Psi_A,e_obs(q),omega[e_obs],theta_A] with no independent hidden-visible coefficient slot",
            "proof_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "missing_for_current_claim": "parent matter functor/action grammar and no-shadow-frame theorem",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "BZA1810_3_alpha_constant_owner",
            "claim_piece": "alpha_EM, masses, clocks and material labels are quotient-owned or constant",
            "mathematical_form": "Lie_v theta_A=0, including alpha_EM, charge unit, mass ratios, clock standards and material labels",
            "proof_status": "OWNER_NOT_DERIVED",
            "missing_for_current_claim": "constant superselection/alpha-owner parent clause plus radiative closure",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "BZA1810_4_no_source_only_slot",
            "claim_piece": "no independent source/action prefactor",
            "mathematical_form": "not exists w_A(X) S_A that changes source/test strength while keeping ordinary matter equations looking Hilbertian",
            "proof_status": "EXACT_TARGET_NOT_PARENT_DERIVED",
            "missing_for_current_claim": "object language, action-measure and current-owner theorem; no non-Hilbert bypass",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "BZA1810_5_tau_role_lock",
            "claim_piece": "one tau projects across clock, WEP, R10, orbit and boundary roles",
            "mathematical_form": "tau_source=tau_charge=tau_clock=tau_orbit=tau_boundary after q pushforward",
            "proof_status": "NOT_DERIVED",
            "missing_for_current_claim": "tau projectability, role-lock certificate, stationarity/admissibility and source/readout convention",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "BZA1810_6_boundary_readout_silence",
            "claim_piece": "boundary, local projector and readout do not reintroduce alpha/source markers",
            "mathematical_form": "Pi_local delta_v B_A=0 and Dreadout[Dq(v)]=0, or finite residual rows bound the leakage",
            "proof_status": "UNSIGNED",
            "missing_for_current_claim": "worldtube support, boundary silence and readout functor proof",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "BZA1810_7_countermodel_guard",
            "claim_piece": "same-frame/common-source wording is not enough",
            "mathematical_form": "e_obs=exp(b_g X)e0 or w_A(X)S_A gives a live countermodel unless b_g=0 and w_A' = 0 are parent-signed",
            "proof_status": "COUNTERMODEL_RETAINED",
            "missing_for_current_claim": "no-shadow and no-source-only-slot theorem or finite b_g/w_A rows",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "BZA1810_8_verdict",
            "claim_piece": "beta_source_alpha=0 is a theorem of current corpus",
            "mathematical_form": "BZA1810_0 through BZA1810_7 close simultaneously",
            "proof_status": "ZERO_THEOREM_NOT_CLOSED_CURRENT_CORPUS",
            "missing_for_current_claim": "the parent action has not signed the q/Dq, matter, alpha, source, tau and boundary package",
            "valid_for_claim": False,
        },
    ]


def finite_product_width_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "width_id": "FPW1810_0_clock_alpha_product",
            "arena": "clock",
            "quantity": "abs(b_alpha*tau_clock_time)",
            "bound_or_value": "2.1e-18",
            "units": "yr^-1",
            "source_anchor": "ACB1809_2 imported from 171Yb+ E3/E2 clock product row",
            "interpretation": "source-backed clock product only; not standalone b_alpha",
            "missing_for_claim": "tau_clock_time parent derivation and Xhat/chi_X normalization",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "width_id": "FPW1810_1_alpha_WEP_product",
            "arena": "MICROSCOPE_WEP",
            "quantity": "abs(beta_source_alpha*b_alpha*tau_WEP)",
            "bound_or_value": "4.797780522732e-05",
            "units": "dimensionless under 1809 smoke convention",
            "source_anchor": "AWP1809_0_alpha_Coulomb and NPW1054_0_alpha_WEP_product",
            "interpretation": "hard normalized product target if alpha/Coulomb marker survives",
            "missing_for_claim": "beta_source_alpha owner, b_alpha standalone or shared product convention, tau_WEP, full material tensor",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "width_id": "FPW1810_2_surface_WEP_product",
            "arena": "MICROSCOPE_WEP",
            "quantity": "abs(beta_source_or_binding*b_A*tau_WEP)",
            "bound_or_value": "2.887280314062e-05",
            "units": "dimensionless under 1809 smoke convention",
            "source_anchor": "AWP1809_1_surface_binding and NPW1054_1_surface_WEP_product",
            "interpretation": "more conservative binding/surface product target if surface channel survives",
            "missing_for_claim": "binding coefficient theorem/prior, tau_WEP, material response tensor",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "width_id": "FPW1810_3_source_weight_WEP_product",
            "arena": "MICROSCOPE_WEP",
            "quantity": "abs(Delta_w_TiPt*tau_WEP)",
            "bound_or_value": "2.8e-15",
            "units": "dimensionless eta-product anchor",
            "source_anchor": "BDW1694_0_MICROSCOPE_Delta_w_tau_bound_anchor and PBI1695_0_bound_anchor",
            "interpretation": "source-backed product anchor; no finite Delta_w bound without tau_min",
            "missing_for_claim": "Delta_w theorem/numeric row, tau_WEP lower bound or direct product derivation",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "width_id": "FPW1810_4_R10_alpha_product",
            "arena": "R10_short_range",
            "quantity": "alpha_X(lambda)=K_X^R10(lambda)*beta_s(lambda)*beta_t(lambda)+epsilon_tail(lambda)",
            "bound_or_value": "MISSING_PROMOTED_BOUND_AND_MTS_FACTORS",
            "units": "dimensionless alpha(lambda) once lambda convention is fixed",
            "source_anchor": "RAP1809_0_product_law and CAC1053_3_R10",
            "interpretation": "schema only; cannot be scored from clock/WEP products",
            "missing_for_claim": "lambda_X, Z_X, K_X(lambda), beta_s, beta_t, tau_R10 and claim-valid bound curve",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "width_id": "FPW1810_5_verdict",
            "arena": "cross_arena",
            "quantity": "finite coupling width status",
            "bound_or_value": "PRODUCT_WIDTHS_ONLY",
            "units": "mixed",
            "source_anchor": "1809/1054/1694/1695 chain",
            "interpretation": "we have useful pressure products, but no standalone coupling prediction yet",
            "missing_for_claim": "parent theorem-zero or source-backed beta/tau rows in one convention",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def tau_projection_chain_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "tau_id": "TPC1810_0_tau_clock",
            "arena": "clock",
            "current_status": "PRODUCT_BOUND_ONLY",
            "definition_or_formula": "d ln(alpha_EM)/dt = b_alpha*tau_clock_time",
            "missing_for_claim": "tau_clock_time parent derivation and Xhat/chi_X normalization",
            "unity_shortcut_status": "not_applicable",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "tau_id": "TPC1810_1_tau_WEP",
            "arena": "MICROSCOPE_WEP",
            "current_status": "BLOCKED",
            "definition_or_formula": "tau_WEP is the normalized local source/orbit/readout/material contraction mapping parent alpha/source variation to eta_AB",
            "missing_for_claim": "official readout matrix, Earth/source worldtube, material tensor, product convention, tau_min or direct product",
            "unity_shortcut_status": "rejected_tau_is_physical_contraction",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "tau_id": "TPC1810_2_tau_R10",
            "arena": "R10_short_range",
            "current_status": "BLOCKED",
            "definition_or_formula": "tau_R10 is the finite-source/readout/profile contraction under a chosen Yukawa kernel convention",
            "missing_for_claim": "lambda_X, Z_X, K_X, source/test charges, profile integral, readout trace and promoted bound curve",
            "unity_shortcut_status": "rejected_do_not_set_tau_R10_to_one",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "tau_id": "TPC1810_3_tau_PPN_orbit",
            "arena": "PPN_orbital",
            "current_status": "BLOCKED",
            "definition_or_formula": "tau_PPN/tau_orbit maps source-normalized parent residuals into gamma, beta, preferred-frame, perihelion and clock sectors",
            "missing_for_claim": "PPN response matrix, gauge/profile split, source-normalized Newton limit and no-cancellation tail envelope",
            "unity_shortcut_status": "rejected",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "tau_id": "TPC1810_4_shared_role_lock",
            "arena": "cross_arena",
            "current_status": "NOT_DERIVED",
            "definition_or_formula": "tau_source=tau_charge=tau_clock=tau_orbit=tau_boundary after q pushforward, or each arena gets its own signed zero theorem",
            "missing_for_claim": "QTS1780_3 tau projectability and DFT1780_2 tau role row",
            "unity_shortcut_status": "forbidden",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "tau_id": "TPC1810_5_verdict",
            "arena": "cross_arena",
            "current_status": "TRANSFER_BLOCKED",
            "definition_or_formula": "clock, WEP, R10 and PPN products cannot be transferred until tau roles and source/readout functors are parent-owned",
            "missing_for_claim": "q/Dq/tau/source-functor signature or source-backed residual components",
            "unity_shortcut_status": "all_unity_shortcuts_rejected",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def arena_projection_bridge_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "bridge_id": "APB1810_0_clock_to_WEP",
            "bridge": "clock alpha product to WEP alpha/source product",
            "status": "BLOCKED",
            "needed_map": "b_alpha*tau_clock_time -> beta_source_alpha*b_alpha*tau_WEP with same alpha domain and source convention",
            "blocking_gap": "standalone b_alpha, beta_source_alpha, tau_WEP and full material tensor missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "bridge_id": "APB1810_1_WEP_to_R10",
            "bridge": "WEP source/product pressure to R10 alpha(lambda)",
            "status": "BLOCKED",
            "needed_map": "DeltaQ or source-weight convention -> beta_s beta_t K_X^R10(lambda) tau_R10",
            "blocking_gap": "R10 source/test charge split, lambda/Z/K and promoted curve missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "bridge_id": "APB1810_2_source_to_Newton",
            "bridge": "source coupling branch to Newton/GR source term",
            "status": "BLOCKED",
            "needed_map": "single observed Hilbert/source current feeds Poisson/Gauss and weak-field Einstein equation",
            "blocking_gap": "source-measure/current owner and Delta_frame_tau remain unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "bridge_id": "APB1810_3_PPN",
            "bridge": "same coupling source branch to PPN residual vector",
            "status": "BLOCKED",
            "needed_map": "source-normalized residuals -> gamma,beta,preferred-frame,tails with no-cancellation envelope",
            "blocking_gap": "PPN response matrix and tau_PPN/profile split missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "bridge_id": "APB1810_4_verdict",
            "bridge": "cross-arena bridge",
            "status": "BRIDGE_NOT_CLOSED",
            "needed_map": "one parent q/Dq/tau/source-functor signature or explicit residual component rows per arena",
            "blocking_gap": "QTS1780_7 and BZA1810_8 fail current proof",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def parent_signature_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "contract_id": "PSC1810_0_parent_q",
            "required_clause": "parent quotient map q is defined before readout",
            "mathematical_contract": "q: Phi_parent -> Q_vis with Q_vis carrying e_obs, g_obs, source/readout data and owned constants",
            "current_evidence": "QTS1780_0 exists as a contract",
            "status": "CONTRACT_WRITTEN_NOT_SIGNED",
            "next_action": "construct q/Dq matrix row or Obs_e factorisation proof",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "PSC1810_1_Dq_kernel",
            "required_clause": "retained hidden/coupling directions are in ker(Dq) or are bounded components",
            "mathematical_contract": "Dq[v_a]=0 for zero theorem; otherwise store finite Dq[v_a] with units and source path",
            "current_evidence": "QTS1780_1 and DFT1780_0 staged",
            "status": "MISSING_MATRIX_OR_COMPONENT_VALUES",
            "next_action": "fill first Dq/DObs_e row rather than assuming verticality",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "PSC1810_2_matter_alpha_owner",
            "required_clause": "matter functor, alpha_EM, masses, clocks and material labels descend or are constant",
            "mathematical_contract": "S_matter=Sbar[Psi,e_obs(q),omega[e_obs],theta] and Lie_v theta_A=0",
            "current_evidence": "BZA1810_2/BZA1810_3 exact conditional; 1054 parent alpha-owner route",
            "status": "OWNER_NOT_SIGNED",
            "next_action": "write parent alpha-owner/matter-functor action clause",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "PSC1810_3_no_source_weight",
            "required_clause": "no source-only action prefactor or non-Hilbert bypass",
            "mathematical_contract": "Allowed[S_matter] excludes independent w_A(X)S_A and any zeta_A non-Hilbert current is zero/exact/projected silent",
            "current_evidence": "AWT1594_7 and NST1695_7 exact target but not parent-derived",
            "status": "THEOREM_NOT_DERIVED",
            "next_action": "derive object-language/action-measure owner or keep Delta_w rows",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "PSC1810_4_tau_role_lock",
            "required_clause": "source, charge, clock, orbit and boundary tau roles are projectable and role-locked",
            "mathematical_contract": "Dq(L_tau Phi)=L_tau_red q(Phi) and tau_source=tau_charge=tau_clock=tau_orbit=tau_boundary",
            "current_evidence": "QTS1780_3 and DFT1780_2 staged",
            "status": "NOT_SIGNED",
            "next_action": "derive tau role-lock or fill tau residual rows",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "PSC1810_5_boundary_worldtube_readout",
            "required_clause": "worldtube, boundary and detector/readout maps do not reopen source/alpha markers",
            "mathematical_contract": "Dsource_readout[Dq(v)]=0, delta_v W_source=0 and Pi_local delta_v B_A=0 or source-bounded rows",
            "current_evidence": "DFT1780_1, DFT1780_5, WEP1702 rows",
            "status": "MISSING_SOURCE_READOUT_WORLDLINE_DATA",
            "next_action": "stage component rows with source paths before scoring WEP/R10/PPN",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "PSC1810_6_verdict",
            "required_clause": "single parent signature package closes",
            "mathematical_contract": "PSC1810_0 through PSC1810_5 all pass simultaneously",
            "current_evidence": "QTS1780_7 remains SIGNATURE_NOT_SIGNED",
            "status": "PARENT_SIGNATURE_NOT_CLOSED",
            "next_action": "attack q/Dq/Obs_e/alpha-owner package directly next",
            "valid_for_claim": False,
        },
    ]


def residual_component_schema_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "component_id": "RCS1810_0_DObs_e",
            "quantity": "DObs_e_vertical_leak",
            "source_from": "DFT1780_0_DObs_e",
            "required_to_promote": "direction_id; Dq_component; DObs_e_value; coframe_norm; units; source_path",
            "current_status": "MISSING_PARENT_Q_DQ_OBS_E_OR_VALUE",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "RCS1810_1_Dreadout",
            "quantity": "Dsource_readout_leak",
            "source_from": "DFT1780_1_Dreadout",
            "required_to_promote": "system_id; readout_map; direction_id; component_value; norm; units; source_path",
            "current_status": "MISSING_SOURCE_READOUT_FUNCTOR_OR_VALUE",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "RCS1810_2_tau_roles",
            "quantity": "Delta_tau_role_lock",
            "source_from": "DFT1780_2_tau_roles",
            "required_to_promote": "tau_source; tau_charge; tau_clock; tau_orbit; tau_boundary; norm; units; source_path",
            "current_status": "MISSING_TAU_PROJECTABILITY_ROLE_LOCK",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "RCS1810_3_constant_marker",
            "quantity": "Dtheta_marker_leak",
            "source_from": "DFT1780_3_constants_marker",
            "required_to_promote": "constant_id; direction_id; Lie_v_theta; marker_component; units; source_path",
            "current_status": "MISSING_CONSTANT_SUPERSELECTION_OR_VALUE",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "RCS1810_4_shadow_source",
            "quantity": "Delta_shadow_frame_source",
            "source_from": "DFT1780_4_shadow_frame_source",
            "required_to_promote": "shadow_type; coefficient; operator_basis; arena_projection; units; source_path",
            "current_status": "MISSING_NO_SHADOW_THEOREM_OR_BOUND",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "RCS1810_5_total_abs",
            "quantity": "epsilon_Delta_frame_tau_abs",
            "source_from": "DFT1780_6_total_abs",
            "required_to_promote": "all component values; component source paths; common normalizer; units; no-cancellation flag",
            "current_status": "MISSING_COMPONENT_VALUES_AND_COMMON_NORM",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def mts_r10_template_rows() -> list[dict[str, Any]]:
    return [
        {
            "model_id": "MTS_1810_beta_tau_source_chain_template",
            "branch_id": BRANCH_ID,
            "lambda_value": "MISSING_LAMBDA_X",
            "alpha_predicted": "MISSING_KX_ZX_BETA_SOURCE_BETA_TEST_TAU_R10",
            "force_law_form": "alpha_X(lambda)=K_X^R10(lambda)*beta_s(lambda)*beta_t(lambda)+epsilon_tail(lambda)",
            "derivation_status": "template_invalid_until_parent_signature_or_source_rows_close",
            "valid_for_claim": False,
        }
    ]


def runner_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1810_0_beta_zero",
            "attempted_claim": "beta_source_alpha=0",
            "runner_status": "REJECT_CLAIM",
            "reason": "zero theorem exact conditional but parent signature package not signed",
            "score_ready": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1810_1_beta_numeric",
            "attempted_claim": "standalone beta_source_alpha numeric prior",
            "runner_status": "REJECT_CLAIM",
            "reason": "only product-width targets exist; strict validator rejects missing source/beta convention rows",
            "score_ready": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1810_2_WEP_score",
            "attempted_claim": "WEP alpha/source branch passes",
            "runner_status": "REJECT_SCORE",
            "reason": "tau_WEP, material tensor, source worldtube and parent source/alpha owner missing",
            "score_ready": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1810_3_R10_score",
            "attempted_claim": "R10 alpha(lambda) branch passes",
            "runner_status": "REJECT_SCORE",
            "reason": "lambda/Z/K/beta_s/beta_t/tau_R10 and claim-valid bound curve missing",
            "score_ready": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1810_4_GR_Newton",
            "attempted_claim": "local GR/Newton follows from coupling bridge",
            "runner_status": "BLOCKED_NO_CLAIM",
            "reason": "source-normalized Hilbert current and q/Dq/tau/source-functor signature remain upstream",
            "score_ready": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1810_5_unity_tau",
            "attempted_claim": "set tau_WEP or tau_R10 to one",
            "runner_status": "REJECT_SHORTCUT",
            "reason": "tau is a physical projection/readout contraction, not a convention",
            "score_ready": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1810_0_zero_theorem",
            "claim": "beta_source_alpha=0 is parent-proved",
            "status": "BLOCKED",
            "reason": "BZA1810_8 remains ZERO_THEOREM_NOT_CLOSED_CURRENT_CORPUS",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1810_1_product_prior",
            "claim": "standalone numeric beta/source prior exists",
            "status": "BLOCKED",
            "reason": "current rows are product-width anchors or templates rejected by validator",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1810_2_WEP",
            "claim": "WEP alpha/source branch passes",
            "status": "BLOCKED",
            "reason": "tau_WEP/source/material/readout/parent owner rows not closed",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1810_3_R10",
            "claim": "R10 alpha(lambda) branch passes",
            "status": "BLOCKED",
            "reason": "R10 projection factors and claim-valid bound curve missing",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1810_4_cross_arena",
            "claim": "clock/WEP/R10/PPN products share one parent normalization",
            "status": "BLOCKED",
            "reason": "tau role lock and q/Dq/source-functor signature not signed",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1810_5_local_GR_Newton",
            "claim": "local GR/Newton source limit is derived",
            "status": "REFUSED",
            "reason": "source-normalized current owner, Delta_frame_tau and PPN residual vector remain open",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1810_0_derivation_result",
            "decision": "BETA_SOURCE_ALPHA_ZERO_THEOREM_EXACT_CONDITIONAL_NOT_CLOSED",
            "reason": "chain-rule route is mathematically clean, but parent q/Dq, matter, alpha, source, tau and boundary clauses are unsigned",
            "next_action": "treat it as the contract a future parent action must satisfy, not as a current theorem",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1810_1_empirical_result",
            "decision": "FINITE_PRODUCT_WIDTHS_ARE_REAL_PRESSURE_ROWS_NOT_PREDICTIONS",
            "reason": "clock, WEP alpha, WEP surface and source-weight rows give hard product targets, but not standalone beta or tau values",
            "next_action": "keep them as no-cancellation pressure data until a source/tau projection is derived or sourced",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1810_2_bridge_result",
            "decision": "CROSS_ARENA_BRIDGE_BLOCKED_BY_PARENT_SIGNATURE",
            "reason": "same tau/source/readout functor is not yet signed across clock, WEP, R10, PPN and orbital arenas",
            "next_action": "attack q/Dq/Obs_e/alpha-owner/matter-functor package directly",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1810_3_best_next",
            "decision": "PARENT_SIGNATURE_ALPHA_OWNER_AND_QDQ_PACKAGE_NEXT",
            "reason": "this is the shortest derivation route toward local GR/Newton: if signed, it kills beta/source leakage; if not, it yields the correct residual rows",
            "next_action": "1811-Y5-R2FR-parent-alpha-owner-matter-functor-and-qDq-signature-contract.md",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1810_0_primary",
            "next_target": "1811-Y5-R2FR-parent-alpha-owner-matter-functor-and-qDq-signature-contract.md",
            "script": "scripts/Y5_R2FR_parent_alpha_owner_matter_functor_and_qDq_signature_contract.py",
            "objective": "try to sign the exact parent package needed for beta_source_alpha=0: q/Dq kernel, Obs_e(q), matter functor, alpha/constant owner, no source-only slot, tau role lock and boundary/readout silence; otherwise stage source-backed Delta_frame_tau residual rows",
            "selection_status": "selected",
            "success_condition": "all parent clauses theorem-zero/source-backed with no placeholders, or a nonclaim residual component schema that blocks local-GR/WEP/R10 promotion cleanly",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1810_1_parallel_data",
            "next_target": "1811b-Y5-R2FR-WEP-R10-tau-source-readout-acquisition-pack.md",
            "script": "scripts/Y5_R2FR_WEP_R10_tau_source_readout_acquisition_pack.py",
            "objective": "prepare source/readout/material/tau rows for WEP and R10 if the theorem package remains unsigned",
            "selection_status": "held_parallel",
            "success_condition": "official/source-backed tau_WEP and tau_R10 input rows with units, source paths and no unity shortcuts",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "zero_theorem_audit": zero_theorem_audit_rows(),
        "finite_product_widths": finite_product_width_rows(),
        "tau_projection_chain": tau_projection_chain_rows(),
        "arena_projection_bridge": arena_projection_bridge_rows(),
        "parent_signature_contract": parent_signature_contract_rows(),
        "residual_component_schema": residual_component_schema_rows(),
        "mts_r10_template": mts_r10_template_rows(),
        "runner_refusal": runner_refusal_rows(),
        "claim_gate": claim_gate_rows(),
        "decision_ledger": decision_ledger_rows(),
        "next_target": next_target_rows(),
    }


def generated_csvs() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def copy_outputs() -> None:
    for output in generated_csvs():
        for target_dir in (MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE):
            target_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(output, target_dir / output.name)


def branch_copies_exist() -> bool:
    for output in generated_csvs():
        for target_dir in (MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE):
            if not (target_dir / output.name).exists():
                return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    names = {DOC_PATH.name, OUTPUTS["validation"].name} | {path.name for path in generated_csvs()}
    return not any(path.name in names for path in FORMALIZATION.rglob("*") if path.is_file())


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for key, rows in rows_map.items():
        if key == "source_register":
            continue
        for row in rows:
            for field in ("valid_for_claim", "claim_allowed", "score_ready", "gate_pass"):
                if field in row and boolish(row[field]):
                    if row.get("selection_status") == "selected":
                        continue
                    return False
    return True


def missing_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for key, rows in rows_map.items():
        if key == "source_register":
            continue
        for row in rows:
            text = " ".join(str(value) for value in row.values())
            if "MISSING_" in text and (
                boolish(row.get("score_ready", False))
                or boolish(row.get("valid_for_claim", False))
                or boolish(row.get("claim_allowed", False))
                or boolish(row.get("gate_pass", False))
            ):
                return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = rows_map["source_register"]
    exists_ok = all(boolish(row["exists"]) for row in source_rows)
    needles_ok = all(boolish(row["needles_present"]) for row in source_rows)
    checks: list[tuple[str, bool, str]] = [
        ("VAL1810_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1810_1_needles_present", needles_ok, "all cited source needles are present"),
        (
            "VAL1810_2_zero_theorem_conditional_only",
            any(row["theorem_id"] == "BZA1810_8_verdict" and row["proof_status"] == "ZERO_THEOREM_NOT_CLOSED_CURRENT_CORPUS" for row in rows_map["zero_theorem_audit"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["zero_theorem_audit"]),
            "beta_source_alpha zero theorem is exact conditional and not promoted",
        ),
        (
            "VAL1810_3_product_widths_nonclaim",
            any(row["width_id"] == "FPW1810_1_alpha_WEP_product" and row["bound_or_value"] == "4.797780522732e-05" for row in rows_map["finite_product_widths"])
            and any(row["width_id"] == "FPW1810_3_source_weight_WEP_product" and row["bound_or_value"] == "2.8e-15" for row in rows_map["finite_product_widths"])
            and all(not boolish(row["valid_for_claim"]) and not boolish(row["score_ready"]) for row in rows_map["finite_product_widths"]),
            "finite rows are product-width pressure targets only",
        ),
        (
            "VAL1810_4_tau_projection_blocked",
            any(row["tau_id"] == "TPC1810_1_tau_WEP" and row["current_status"] == "BLOCKED" for row in rows_map["tau_projection_chain"])
            and any(row["tau_id"] == "TPC1810_2_tau_R10" and row["unity_shortcut_status"].startswith("rejected") for row in rows_map["tau_projection_chain"]),
            "tau_WEP/tau_R10 remain physical projection blockers, not unity conventions",
        ),
        (
            "VAL1810_5_bridge_blocks",
            all(row["status"] in {"BLOCKED", "BRIDGE_NOT_CLOSED"} and not boolish(row["claim_allowed"]) for row in rows_map["arena_projection_bridge"]),
            "cross-arena clock/WEP/R10/PPN bridge remains blocked",
        ),
        (
            "VAL1810_6_parent_contract_written",
            any(row["contract_id"] == "PSC1810_6_verdict" and row["status"] == "PARENT_SIGNATURE_NOT_CLOSED" for row in rows_map["parent_signature_contract"]),
            "parent signature contract is explicit and not falsely signed",
        ),
        (
            "VAL1810_7_residual_schema_nonclaim",
            any(row["component_id"] == "RCS1810_5_total_abs" for row in rows_map["residual_component_schema"])
            and all(not boolish(row["score_ready"]) and not boolish(row["valid_for_claim"]) for row in rows_map["residual_component_schema"]),
            "Delta_frame_tau residual fallback rows are staged as nonclaim",
        ),
        (
            "VAL1810_8_mts_template_nonclaim",
            len(rows_map["mts_r10_template"]) == 1 and all(not boolish(row["valid_for_claim"]) for row in rows_map["mts_r10_template"]),
            "MTS R10 template has runner schema and no claim-valid rows",
        ),
        (
            "VAL1810_9_runner_refuses_claims",
            all(not boolish(row["score_ready"]) and not boolish(row["claim_allowed"]) for row in rows_map["runner_refusal"]),
            "runner ledger refuses beta-zero, WEP, R10, GR/Newton and unity-tau shortcuts",
        ),
        (
            "VAL1810_10_claim_gates_blocked",
            all(row["status"] in {"BLOCKED", "REFUSED"} and not boolish(row["gate_pass"]) and not boolish(row["valid_for_claim"]) for row in rows_map["claim_gate"]),
            "all coupling/local claim gates remain blocked",
        ),
        ("VAL1810_11_no_claim_flags", no_claim_flags(rows_map), "no generated theorem/score/claim flags are true"),
        ("VAL1810_12_missing_not_ready", missing_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1810_13_decision_next",
            any(row["decision_id"] == "DEC1810_3_best_next" and row["decision"] == "PARENT_SIGNATURE_ALPHA_OWNER_AND_QDQ_PACKAGE_NEXT" for row in rows_map["decision_ledger"]),
            "decision selects parent signature/alpha-owner/qDq package next",
        ),
        (
            "VAL1810_14_next_selected",
            any(row["route_id"] == "NEXT1810_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1810_15_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1810 CSVs parse"),
        ("VAL1810_16_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1810_17_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1810_18_formalization_untouched", formalization_untouched(), "no 1810 outputs found under formalization-workbench"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1810_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1810 beta-source-alpha and tau WEP/R10 source-chain checkpoint",
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    return "\n".join(
        [
            "# 1810 Y5 R2FR beta source alpha and tau WEP R10 source chain",
            "",
            "**Progress:** the coupling problem is now a precise parent-action contract. The clean theorem route says `beta_source_alpha=0` if the visible matter/readout/constant package descends through `q` and the retained direction is in `ker(Dq)`. The corpus has the right conditional chain rule, but not the parent signature that lets us claim it.",
            "",
            "**Current verdict:** not a failure, not a pass. We have real product-pressure rows from clocks and WEP, and a strict R10 schema, but every public-facing coupling/local-GR claim remains blocked until the parent alpha-owner/qDq/tau/source package is signed or finite residual rows are sourced.",
            "",
            "**Best next move:** attack the parent signature package directly: `q`, `Dq`, `Obs_e(q)`, matter functor, alpha/constant owner, no source-only slot, tau role lock, and boundary/readout silence. That is the route most likely to make MTS reduce to GR/Newton instead of becoming just another fitted fifth-force model.",
            "",
            "**Claim ceiling:** no standalone `beta_source_alpha`, no theorem-zero coupling claim, no WEP/R10/PPN/clock/local-GR pass, no unity tau shortcut, no GitHub action, and no `formalization-workbench` edit is allowed from 1810.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "missing_needles", "role"]),
            "",
            "## Beta Source Alpha Zero Theorem Audit",
            markdown_table(rows_map["zero_theorem_audit"], ["theorem_id", "claim_piece", "mathematical_form", "proof_status", "missing_for_current_claim", "valid_for_claim"]),
            "",
            "## Finite Product Width Chain",
            markdown_table(rows_map["finite_product_widths"], ["width_id", "arena", "quantity", "bound_or_value", "units", "interpretation", "missing_for_claim", "score_ready", "valid_for_claim"]),
            "",
            "## Tau WEP/R10 Source Chain",
            markdown_table(rows_map["tau_projection_chain"], ["tau_id", "arena", "current_status", "definition_or_formula", "missing_for_claim", "unity_shortcut_status", "score_ready", "valid_for_claim"]),
            "",
            "## Arena Projection Bridge",
            markdown_table(rows_map["arena_projection_bridge"], ["bridge_id", "bridge", "status", "needed_map", "blocking_gap", "claim_allowed", "valid_for_claim"]),
            "",
            "## Parent Signature Contract",
            markdown_table(rows_map["parent_signature_contract"], ["contract_id", "required_clause", "mathematical_contract", "current_evidence", "status", "next_action", "valid_for_claim"]),
            "",
            "## Delta Frame Tau Residual Schema",
            markdown_table(rows_map["residual_component_schema"], ["component_id", "quantity", "source_from", "required_to_promote", "current_status", "score_ready", "valid_for_claim"]),
            "",
            "## MTS R10 Template",
            markdown_table(rows_map["mts_r10_template"], ["model_id", "branch_id", "lambda_value", "alpha_predicted", "derivation_status", "valid_for_claim"]),
            "",
            "## Runner Refusal Ledger",
            markdown_table(rows_map["runner_refusal"], ["runner_id", "attempted_claim", "runner_status", "reason", "score_ready", "claim_allowed"]),
            "",
            "## Claim Gates",
            markdown_table(rows_map["claim_gate"], ["claim_id", "claim", "status", "reason", "gate_pass", "valid_for_claim"]),
            "",
            "## Decision Ledger",
            markdown_table(rows_map["decision_ledger"], ["decision_id", "decision", "reason", "next_action"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This is the coupling throat, and it is finally named cleanly. The Mayweather route here is not to fake a knockout by setting `tau=1`; it is to force the parent action to either sign the zero theorem or hand us concrete residual components with units and source paths. That is exactly the kind of bridge that can become a GR/Newton reduction instead of a patchwork fit.",
            "",
        ]
    )


def main() -> None:
    ensure_dirs()
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1810 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()

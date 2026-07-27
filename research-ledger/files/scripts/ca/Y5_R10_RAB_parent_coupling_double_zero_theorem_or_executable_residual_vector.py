from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
COEFF = MICROSCOPE / "branch_locked_wep" / "coefficients"
QUARANTINE = MICROSCOPE / "quarantine" / "1473"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1473-Y5-R10-RAB-parent-coupling-double-zero-theorem-or-executable-residual-vector.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
START_TS = datetime.now(timezone.utc).timestamp()

PREV_NEXT = OUT / "P8_Y5_R10_1472_NEXT_TARGET.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1472_VALIDATION.csv"
PREV_DEBT = OUT / "P8_Y5_R10_1472_COUPLING_DEBT_ROLLUP.csv"
PREV_CONTRACT = OUT / "P8_Y5_R10_1472_PARENT_ACTION_COUPLING_CONTRACT_ATTEMPT.csv"
PREV_FEED = OUT / "P8_Y5_R10_1472_LOCAL_GR_FEED_LEDGER.csv"
PREV_SOURCE_PACK = OUT / "P8_Y5_R10_1472_ALPHA_PRODUCT_COMPONENT_SOURCE_PACK.csv"

LOCAL_ACTION_511 = OUT / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv"
LOCAL_FIXED_511 = OUT / "P8_MIN_PARENT_LOCAL_GR_FIXED_POINT_CONDITIONS.csv"
LOCAL_RESIDUAL_511 = OUT / "P8_MIN_PARENT_LOCAL_GR_RESIDUAL_VECTOR.csv"
LOCAL_GATES_511 = OUT / "P8_MIN_PARENT_LOCAL_GR_GATE_TESTS.csv"
LOCAL_VECTOR_482 = OUT / "P8_LOCAL_GR_RESIDUAL_VECTOR_FROM_DOMAIN_SOURCE.csv"
LOCAL_PROMOTION_482 = OUT / "P8_LOCAL_GR_RESIDUAL_PROMOTION_GATES.csv"

SOURCE_COUPLING_1229 = OUT / "P8_Y5_R10_1229_LOCAL_GR_SOURCE_COUPLING_THEOREM_CONTRACT.csv"
SOURCE_GATE_1230 = OUT / "P8_Y5_R10_1230_LOCAL_GR_SOURCE_COUPLING_GATE_UPDATE.csv"
WEP_OWNER_1077 = OUT / "P8_Y5_R10_1077_PARENT_WEP_COUPLING_OWNER_THEOREM_ATTEMPT.csv"
MATTER_COUPLING_716 = OUT / "P8_Y5_R10_716_MATTER_COUPLING_DERIVATION.csv"
FINITE_COUPLING_630 = OUT / "P8_Y5_R10_630_FINITE_COUPLING_DERIVATION.csv"
CPARENT_CONTRACT_1445 = OUT / "P8_Y5_R10_1445_C_PARENT_COUPLING_THEOREM_CONTRACT.csv"
UEM_1099 = OUT / "P8_Y5_R10_1099_EM_KINETIC_OWNER_THEOREM_ATTEMPT.csv"
OBSTRUCTION_1114 = OUT / "P8_Y5_R10_1114_COUPLING_OBSTRUCTION_LEDGER.csv"
SHARED_TAU_1402 = OUT / "P8_Y5_R10_1402_SHARED_TAU_TRANSFER_THEOREM_AUDIT.csv"
KX_ROWS_1035 = OUT / "P8_Y5_R10_1035_KX_FACTORIZATION_ROWS.csv"
R10_INPUT_1034 = OUT / "P8_Y5_R10_1034_PROJECTION_INPUT_PACK.csv"
NEWTON_SPINE_956 = OUT / "P8_Y5_R10_956_SOURCE_SIDE_GR_NEWTON_SPINE.csv"
NEWTON_LHS_956 = OUT / "P8_Y5_R10_956_LEFT_HAND_EH_NEWTON_GATE_MAP.csv"
NEWTON_LADDER_990 = OUT / "P8_Y5_R10_990_GR_NEWTON_REENTRY_LADDER.csv"
NEWTON_BLOCKERS_1339 = OUT / "P8_Y5_R10_1339_NEWTON_TRANSFER_BLOCKERS.csv"
PPN_GATE_1339 = OUT / "P8_Y5_R10_1339_PPN_COMPLETION_GATE.csv"

LIVE_CPARENT = COEFF / "C_parent_WEP_slot_import.csv"
LIVE_DOUBLE_ZERO = COEFF / "parent_coupling_double_zero_claim_rows.csv"
LIVE_ALPHA_PRODUCT = COEFF / "alpha_residual_product_claim_rows.csv"
LIVE_LOCAL_GR = COEFF / "local_GR_claim_promotion_rows.csv"
LIVE_PPN_VECTOR = COEFF / "PPN_residual_vector_claim_rows.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1473_SOURCE_REGISTER.csv"
DOUBLE_ZERO_THEOREM = OUT / "P8_Y5_R10_1473_PARENT_COUPLING_DOUBLE_ZERO_THEOREM_ATTEMPT.csv"
PREMISE_AUDIT = OUT / "P8_Y5_R10_1473_DOUBLE_ZERO_PREMISE_AUDIT.csv"
EXEC_RESIDUAL_VECTOR = OUT / "P8_Y5_R10_1473_EXECUTABLE_LOCAL_RESIDUAL_VECTOR.csv"
RESIDUAL_HOOK_MAP = OUT / "P8_Y5_R10_1473_RESIDUAL_HOOK_MAP.csv"
PPN_NEWTON_GATE = OUT / "P8_Y5_R10_1473_NEWTON_PPN_LOCAL_GR_GATE_UPDATE.csv"
COUNTERMODELS = OUT / "P8_Y5_R10_1473_COUNTERMODEL_LEDGER.csv"
LIVE_GUARD = OUT / "P8_Y5_R10_1473_LIVE_IMPORT_GUARD.csv"
REDUCTION_GATES = OUT / "P8_Y5_R10_1473_REDUCTION_GATES.csv"
SIGNING_DECISION = OUT / "P8_Y5_R10_1473_PARENT_SIGNING_DECISION.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1473_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1473_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1473_VALIDATION.csv"

QUAR_RESIDUAL_VECTOR = QUARANTINE / "EXECUTABLE_LOCAL_RESIDUAL_VECTOR.csv"
QUAR_THEOREM = QUARANTINE / "PARENT_COUPLING_DOUBLE_ZERO_THEOREM_ATTEMPT.csv"
BRANCH_RESIDUAL_VECTOR = COEFF / "executable_local_residual_vector_nonclaim_1473.csv"
BRANCH_THEOREM = COEFF / "parent_coupling_double_zero_theorem_attempt_nonclaim_1473.csv"
BRANCH_SIGNING = COEFF / "parent_coupling_double_zero_signing_decision_1473.csv"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def truth(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def copy_branch(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)


def formalization_modified_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= START_TS)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def source_rows() -> list[dict[str, Any]]:
    local_sources = [
        ("SRC1473_0_1472_next", PREV_NEXT, "1472 handoff to double-zero theorem or executable residual vector"),
        ("SRC1473_1_1472_validation", PREV_VALIDATION, "1472 validation baseline"),
        ("SRC1473_2_1472_debt", PREV_DEBT, "1472 coupling debt rollup"),
        ("SRC1473_3_1472_contract", PREV_CONTRACT, "1472 parent action coupling contract attempt"),
        ("SRC1473_4_1472_feed", PREV_FEED, "1472 local-GR feed ledger"),
        ("SRC1473_5_1472_source_pack", PREV_SOURCE_PACK, "1472 alpha component source pack"),
        ("SRC1473_6_action_blocks", LOCAL_ACTION_511, "minimum local-GR parent action blocks"),
        ("SRC1473_7_fixed_point", LOCAL_FIXED_511, "local fixed-point conditions"),
        ("SRC1473_8_residual_511", LOCAL_RESIDUAL_511, "minimum parent local-GR residual vector"),
        ("SRC1473_9_gates_511", LOCAL_GATES_511, "minimum parent local-GR gate tests"),
        ("SRC1473_10_vector_482", LOCAL_VECTOR_482, "existing local-GR residual vector"),
        ("SRC1473_11_promotion_482", LOCAL_PROMOTION_482, "local-GR residual promotion gates"),
        ("SRC1473_12_source_coupling", SOURCE_COUPLING_1229, "local-GR source coupling theorem contract"),
        ("SRC1473_13_source_gate", SOURCE_GATE_1230, "local-GR source coupling gate update"),
        ("SRC1473_14_wep_owner", WEP_OWNER_1077, "parent WEP coupling owner theorem attempt"),
        ("SRC1473_15_matter_coupling", MATTER_COUPLING_716, "matter coupling derivation"),
        ("SRC1473_16_finite_coupling", FINITE_COUPLING_630, "finite coupling derivation"),
        ("SRC1473_17_Cparent_contract", CPARENT_CONTRACT_1445, "C_parent coupling theorem contract"),
        ("SRC1473_18_UEM", UEM_1099, "EM kinetic owner theorem attempt"),
        ("SRC1473_19_obstruction", OBSTRUCTION_1114, "coupling obstruction ledger"),
        ("SRC1473_20_shared_tau", SHARED_TAU_1402, "shared tau/domain transfer audit"),
        ("SRC1473_21_KX", KX_ROWS_1035, "K_X factorization rows"),
        ("SRC1473_22_R10_input", R10_INPUT_1034, "R10 projection input pack"),
        ("SRC1473_23_newton_spine", NEWTON_SPINE_956, "source-side GR/Newton spine"),
        ("SRC1473_24_newton_lhs", NEWTON_LHS_956, "left-hand EH/Newton gate map"),
        ("SRC1473_25_newton_ladder", NEWTON_LADDER_990, "GR/Newton reentry ladder"),
        ("SRC1473_26_newton_blockers", NEWTON_BLOCKERS_1339, "Newton transfer blockers"),
        ("SRC1473_27_ppn_gate", PPN_GATE_1339, "PPN completion gate"),
    ]
    return [
        {
            "source_id": source_id,
            "source_type": "local_file",
            "path_or_url": rel(path),
            "exists": path.exists(),
            "usage": usage,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for source_id, path, usage in local_sources
    ]


def double_zero_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "DZ1473_0_taylor_lemma",
            "claim_piece": "double-zero kills first-order coupling leakage",
            "formal_statement": "Let C_i(Phi) be every non-EH coefficient entering observed matter, Maxwell, source, finite-range, Pi_M, or readout operators. If C_i(Phi0)=0 and partial_A C_i(Phi0)=0 for all A, then C_i(Phi0+deltaPhi)=O(deltaPhi^2), so no first-order local WEP/R10/clock/PPN residual is sourced by C_i.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "proof_sketch": "Taylor expand C_i around the compact local fixed point. The constant and linear terms vanish by premise, leaving quadratic terms only. First-order weak-field/source/readout residuals proportional to C_i or partial_A C_i therefore vanish.",
            "missing_for_parent_claim": "parent action must identify the complete list of C_i and prove the double-zero conditions, not just name them",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "DZ1473_1_fixed_point_not_enough",
            "claim_piece": "stationary local fixed point alone does not imply double zero",
            "formal_statement": "E_A(Phi0)=0 and L_tau Phi0=0 do not imply C_i(Phi0)=0 or partial_A C_i(Phi0)=0 unless C_i is dynamically tied to the same extremized functional with a symmetry/selection rule.",
            "proof_status": "NO_GO_GUARD",
            "proof_sketch": "A field can be at an extremum while a distinct coupling function has nonzero value or slope there; e.g. C(Phi)=c0+c1(Phi-Phi0)+... with c0 or c1 nonzero.",
            "missing_for_parent_claim": "selection symmetry, quotient grammar, or action variation tying every observed coupling to the fixed-point annihilator",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "DZ1473_2_positive_gap_supports_not_replaces",
            "claim_piece": "positive mass gap suppresses field profiles but does not set couplings to zero",
            "formal_statement": "A positive operator L_AB can suppress deltaPhi sourced by residual currents; it cannot by itself prove that source charges, alpha slopes, or readout derivatives vanish.",
            "proof_status": "EXACT_DISTINCTION",
            "proof_sketch": "The Green response scales like L^{-1}J. If J contains nonzero coupling derivatives, suppression is finite-range/bounded evidence, not theorem-zero.",
            "missing_for_parent_claim": "either J=0 by double-zero/source universality or a numeric finite-range residual bound",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "DZ1473_3_universal_matter_branch",
            "claim_piece": "universal matter/coframe branch is the clean route to source-side GR",
            "formal_statement": "If S_matter descends to one observed coframe with no species/source/readout multiplier, then source-label variations lie in the null kernel and WEP/source-current first derivatives vanish.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "proof_sketch": "All matter variations factor through delta S_matter/delta e_obs. Species decomposition is bookkeeping, so no independent source selector produces a coupling derivative.",
            "missing_for_parent_claim": "parent-signed connected ordinary matter category, action-density line owner, and same-readout-frame theorem",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "DZ1473_4_verdict",
            "claim_piece": "parent fixed-point double-zero law",
            "formal_statement": "DZ1473_0 plus parent-owned complete C_i list, source-current universality, same-frame readout, and finite-mode operator would close the first-order local coupling branch.",
            "proof_status": "NOT_PARENT_DERIVED_EMIT_EXECUTABLE_RESIDUAL_VECTOR",
            "proof_sketch": "The mathematical lemma is clean; the parent ownership premises are still open, so every surviving linear coupling is emitted as a residual row.",
            "missing_for_parent_claim": "complete parent action map and double-zero proof for alpha/source/readout/finite-mode/Pi_M/PPN couplings",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def premise_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "premise_id": "PREM1473_0_complete_Ci_list",
            "premise": "complete list of non-EH local couplings C_i is parent-owned",
            "current_evidence": "A511_3, A511_6, PAC1472_0, and CTC1445 identify the classes but not a complete parent coefficient list",
            "status": "INCOMPLETE_PARENT_MAP",
            "blocks": "double-zero theorem promotion; residual-vector completeness",
            "source_path": rel(LOCAL_ACTION_511),
            "source_anchor": "A511_3_extra_field_silence;A511_6_metric_readout",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "premise_id": "PREM1473_1_alpha_owner",
            "premise": "alpha_EM/F_Q^2 coefficient has no independent hidden or readout slope",
            "current_evidence": "UEM1099 gives an exact conditional chain rule but retains f_X(Xhat)F_Q^2 counterterm",
            "status": "UNSIGNED_THEOREM_TARGET",
            "blocks": "clock alpha, WEP alpha, R10 alpha(lambda), local EM leakage",
            "source_path": rel(UEM_1099),
            "source_anchor": "UEM1099_1_chain_rule;UEM1099_2_counterterm;UEM1099_3_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "premise_id": "PREM1473_2_source_current_universality",
            "premise": "ordinary source current has one owner and no species/source multiplier",
            "current_evidence": "THM1229/WCO1077 are exact conditional routes but not parent-signed",
            "status": "CONDITIONAL_ONLY",
            "blocks": "Newton source side, WEP source normalization, R10 source/test charges",
            "source_path": rel(SOURCE_COUPLING_1229),
            "source_anchor": "THM1229_1_iff;THM1229_3_residual_vector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "premise_id": "PREM1473_3_same_readout_frame",
            "premise": "clock/light/orbit/boundary/source readouts use one observed coframe through PPN order",
            "current_evidence": "coframe/tau lock is a contract; tau clock/WEP/R10 transfer remains blocked",
            "status": "CONTRACT_WRITTEN_NOT_DERIVED",
            "blocks": "clock-WEP-R10 transfer; measured-GM; PPN readout",
            "source_path": rel(SHARED_TAU_1402),
            "source_anchor": "DTT1402_5_no_arena_specific_screen;DTT1402_7_current_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "premise_id": "PREM1473_4_finite_mode_operator",
            "premise": "finite local response mode has parent-owned Z_X, lambda_X, charges, and boundary conditions",
            "current_evidence": "K_X has a symbolic shape contract but no numeric parent-signed value",
            "status": "SYMBOLIC_ONLY_PARENT_OPERATOR_MISSING",
            "blocks": "R10 alpha(lambda), finite-range Newton/PPN residuals",
            "source_path": rel(KX_ROWS_1035),
            "source_anchor": "KXF1035_4_total",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "premise_id": "PREM1473_5_EH_PiM_PPN",
            "premise": "EH operator, Pi_M lock, measured-GM calibration, and PPN completion are derived",
            "current_evidence": "Newton ladder says operator blocked, Newton not reached, PPN not ready",
            "status": "NOT_REACHED",
            "blocks": "Newtonian mechanics and local GR reduction",
            "source_path": rel(NEWTON_LADDER_990),
            "source_anchor": "LAD990_1_operator;LAD990_3_Newton;LAD990_4_PPN",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def executable_residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "component_id": "ERV1473_0_alpha_EM_slope",
            "sector": "EM_alpha",
            "source_channel": "hidden_or_readout_F2",
            "target_row": "clock/WEP/R10/PPN_alpha_branch",
            "observable": "dln_alpha; eta_alpha; alpha_R10(lambda); local_EM_PPN",
            "residual_symbol": "b_alpha_EM",
            "residual_expression": "b_alpha_EM := partial_A ln Z_EM_eff(Phi0) v_X^A; require b_alpha_EM=0 or product bounds for each arena",
            "predicted_value_or_certificate": "FILL_NUMERIC_OR_THEOREM_ZERO",
            "units": "dimensionless vertical derivative",
            "bound_or_gate": "clock product bound; WEP alpha target; R10 alpha(lambda) bound; local readout gate",
            "source_artifact": rel(UEM_1099),
            "theorem_zero_certificate": "MISSING_PARENT_ALPHA_OWNER_AND_RADIATIVE_CLOSURE",
            "numeric_source_file": "MISSING_NUMERIC_B_ALPHA_SOURCE",
            "current_status": "executable_residual_unfilled",
            "passes_required_gate": False,
            "valid_for_local_GR_claim": False,
            "blocks_Newton": False,
            "blocks_PPN": True,
            "blocks_local_GR": True,
            "next_action": "prove no hidden F2/effective readout coefficient or fill b_alpha products numerically",
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "component_id": "ERV1473_1_source_weight",
            "sector": "ordinary_matter_source",
            "source_channel": "species_or_source_multiplier",
            "target_row": "Newton_source/WEP/R10_source",
            "observable": "q_source^nu; eta_AB; measured GM; alpha_R10 source leg",
            "residual_symbol": "delta_w_A",
            "residual_expression": "q_source^nu = P_loc nabla_mu[sum_A delta_w_A T_A^{mu nu}] plus readout/boundary terms",
            "predicted_value_or_certificate": "FILL_NUMERIC_OR_THEOREM_ZERO",
            "units": "dimensionless source multiplier or declared current units",
            "bound_or_gate": "source-normalized Newton gate; WEP eta gate; R10 source charge gate",
            "source_artifact": rel(SOURCE_COUPLING_1229),
            "theorem_zero_certificate": "MISSING_UNIVERSAL_SOURCE_COUPLING_CERTIFICATE",
            "numeric_source_file": "MISSING_DELTA_W_A_VECTOR",
            "current_status": "executable_residual_unfilled",
            "passes_required_gate": False,
            "valid_for_local_GR_claim": False,
            "blocks_Newton": True,
            "blocks_PPN": True,
            "blocks_local_GR": True,
            "next_action": "prove connected ordinary matter/source-label forgetting or fill finite source residual vector",
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "component_id": "ERV1473_2_matter_frame_charge",
            "sector": "matter_frame",
            "source_channel": "species_dependent_frame_or_mass_charge",
            "target_row": "WEP/R10/clock/Gdot",
            "observable": "Q_Aa; eta_AB; alpha_R10(lambda); clock mass constants",
            "residual_symbol": "Q_Aa",
            "residual_expression": "Q_Aa = N_frame E_a^I[partial_I ln m_A^obs + f_frame partial_I ln A_EH]_{Phi0}",
            "predicted_value_or_certificate": "FILL_NUMERIC_OR_THEOREM_ZERO",
            "units": "dimensionless charge per canonical mode",
            "bound_or_gate": "WEP material contrast; R10 source/test charge; clock mass matrix; Gdot/PPN",
            "source_artifact": rel(MATTER_COUPLING_716),
            "theorem_zero_certificate": "MISSING_MATTER_BLINDNESS_SAME_FRAME_NO_MODE_CERTIFICATE",
            "numeric_source_file": "MISSING_Q_AA_COEFFICIENT_TABLE",
            "current_status": "executable_residual_unfilled",
            "passes_required_gate": False,
            "valid_for_local_GR_claim": False,
            "blocks_Newton": True,
            "blocks_PPN": True,
            "blocks_local_GR": True,
            "next_action": "derive universal observed coframe/matter blindness or fill Q_Aa coefficient basis",
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "component_id": "ERV1473_3_tau_domain_screen",
            "sector": "readout_domain",
            "source_channel": "arena_private_tau_or_screen",
            "target_row": "clock/WEP/R10/PPN_transfer",
            "observable": "tau_clock; tau_WEP; tau_R10; A_i[D_parent]",
            "residual_symbol": "Delta_tau_a",
            "residual_expression": "Delta_tau_a := tau_a - T_a[D_parent]; require Delta_tau_clock=Delta_tau_WEP=Delta_tau_R10=Delta_tau_PPN=0 or arena-specific residuals",
            "predicted_value_or_certificate": "FILL_NUMERIC_OR_THEOREM_ZERO",
            "units": "arena-dependent declared tau units",
            "bound_or_gate": "shared tau/domain gate; clock product; WEP source projection; R10 tau projection; PPN projection",
            "source_artifact": rel(SHARED_TAU_1402),
            "theorem_zero_certificate": "MISSING_SHARED_D_PARENT_TAU_CERTIFICATE",
            "numeric_source_file": "MISSING_ARENA_TAU_RESIDUAL_ROWS",
            "current_status": "executable_residual_unfilled",
            "passes_required_gate": False,
            "valid_for_local_GR_claim": False,
            "blocks_Newton": False,
            "blocks_PPN": True,
            "blocks_local_GR": True,
            "next_action": "derive common local domain/readout map or score arena-specific tau residuals separately",
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "component_id": "ERV1473_4_finite_range_operator",
            "sector": "finite_range_R10",
            "source_channel": "local_extra_mode",
            "target_row": "R10_alpha_lambda/Newton_finite_range/PPN_tail",
            "observable": "alpha_X(lambda); finite-range mu_extra; gamma/beta tails",
            "residual_symbol": "alpha_X(lambda)",
            "residual_expression": "alpha_X(lambda)=K_X(lambda) Qbar_source(lambda) Qbar_test(lambda)/(4*pi Z_X G_obs) plus no-cancellation tail envelope",
            "predicted_value_or_certificate": "FILL_NUMERIC_CURVE_OR_THEOREM_ZERO",
            "units": "dimensionless alpha(lambda)",
            "bound_or_gate": "R10 alpha(lambda) curve; finite-range Newton/PPN residual gate",
            "source_artifact": rel(R10_INPUT_1034),
            "theorem_zero_certificate": "MISSING_NO_MODE_OR_ZERO_CHARGE_CERTIFICATE",
            "numeric_source_file": "MISSING_KX_QBAR_ZX_LAMBDAX_CURVE",
            "current_status": "executable_residual_unfilled",
            "passes_required_gate": False,
            "valid_for_local_GR_claim": False,
            "blocks_Newton": True,
            "blocks_PPN": True,
            "blocks_local_GR": True,
            "next_action": "derive positive finite-mode operator and charges or fill alpha(lambda) prediction curve",
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "component_id": "ERV1473_5_PiM_measured_GM",
            "sector": "source_measure_calibration",
            "source_channel": "mass_projector_or_boundary_readout",
            "target_row": "Newton_measured_GM",
            "observable": "mu_obs; dln_mu_obs_dt; radial/source normalization",
            "residual_symbol": "delta_PiM",
            "residual_expression": "delta_PiM := Pi_M(Phi0)-Pi_EH plus partial_A Pi_M(Phi0) deltaPhi^A and boundary/reference flux terms",
            "predicted_value_or_certificate": "FILL_NUMERIC_OR_THEOREM_ZERO",
            "units": "dimensionless or declared mass-projector units",
            "bound_or_gate": "measured-GM calibration; Newton transfer blockers; source-normalized Newton gate",
            "source_artifact": rel(NEWTON_LHS_956),
            "theorem_zero_certificate": "MISSING_PIM_LOCK_AND_GAUSS_CALIBRATION_CERTIFICATE",
            "numeric_source_file": "MISSING_DELTA_PIM_SOURCE_ROW",
            "current_status": "executable_residual_unfilled",
            "passes_required_gate": False,
            "valid_for_local_GR_claim": False,
            "blocks_Newton": True,
            "blocks_PPN": True,
            "blocks_local_GR": True,
            "next_action": "prove Pi_M=Pi_EH with first variation zero or emit measured-GM residual coefficients",
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "component_id": "ERV1473_6_metric_PPN_readout",
            "sector": "metric_readout",
            "source_channel": "second_order_metric_or_frame_tail",
            "target_row": "PPN_gamma_beta_alpha_i_xi",
            "observable": "gamma-1; beta-1; alpha1; alpha2; alpha3; xi",
            "residual_symbol": "Delta_PPN_i",
            "residual_expression": "Delta_PPN_i := projection_i[g_readout - g_GR] through O(U^2), including frame/source/projector/domain terms",
            "predicted_value_or_certificate": "FILL_NUMERIC_VECTOR_OR_THEOREM_ZERO",
            "units": "dimensionless PPN residuals",
            "bound_or_gate": "PPN completion gate; local residual promotion gates",
            "source_artifact": rel(PPN_GATE_1339),
            "theorem_zero_certificate": "MISSING_WEAK_FIELD_METRIC_READOUT_CERTIFICATE",
            "numeric_source_file": "MISSING_PPN_VECTOR_SOURCE_ROW",
            "current_status": "executable_residual_unfilled",
            "passes_required_gate": False,
            "valid_for_local_GR_claim": False,
            "blocks_Newton": False,
            "blocks_PPN": True,
            "blocks_local_GR": True,
            "next_action": "derive weak-field metric readout or fill PPN residual vector against bounds",
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "component_id": "ERV1473_7_transition_activation",
            "sector": "local_cosmology_transition",
            "source_channel": "activation_scale_or_memory_switch",
            "target_row": "local_GR_vs_cosmology_galaxy_unification",
            "observable": "ell_tr/L_cg; local silence; cosmological activation",
            "residual_symbol": "Delta_activation",
            "residual_expression": "Delta_activation := activation functional not derived from parent operator spectrum/source scale/topological sector",
            "predicted_value_or_certificate": "FILL_PARENT_ACTIVATION_LAW_OR_THEOREM_ZERO",
            "units": "dimensionless or declared scale ratio",
            "bound_or_gate": "unified field theory gate; no hand plateau; local/cosmology coexistence",
            "source_artifact": rel(LOCAL_FIXED_511),
            "theorem_zero_certificate": "MISSING_ACTION_DERIVED_TRANSITION_LAW",
            "numeric_source_file": "MISSING_ELL_TR_LCG_DERIVATION_ROW",
            "current_status": "executable_residual_unfilled",
            "passes_required_gate": False,
            "valid_for_local_GR_claim": False,
            "blocks_Newton": False,
            "blocks_PPN": True,
            "blocks_local_GR": True,
            "next_action": "derive activation from operator spectrum/source scale or retain transition residual explicitly",
        },
    ]


def residual_hook_rows(residuals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "hook_id": "HOOK1473_0_alpha_to_1472",
            "new_residual_rows": "ERV1473_0_alpha_EM_slope",
            "prior_debt_rows": "DEBT1472_0_alpha_owner",
            "existing_gate_or_vector": rel(PREV_DEBT),
            "hook_effect": "turns alpha owner debt into executable clock/WEP/R10/PPN residual",
            "promotion_allowed": False,
            "valid_for_claim": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "hook_id": "HOOK1473_1_source_to_Newton",
            "new_residual_rows": "ERV1473_1_source_weight;ERV1473_2_matter_frame_charge",
            "prior_debt_rows": "DEBT1472_1_source_current_owner",
            "existing_gate_or_vector": rel(NEWTON_SPINE_956),
            "hook_effect": "connects finite source coupling debt to source-side GR/Newton closure",
            "promotion_allowed": False,
            "valid_for_claim": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "hook_id": "HOOK1473_2_tau_to_PPN",
            "new_residual_rows": "ERV1473_3_tau_domain_screen",
            "prior_debt_rows": "DEBT1472_2_tau_domain_map",
            "existing_gate_or_vector": rel(SHARED_TAU_1402),
            "hook_effect": "prevents clock bound from being exported to WEP/R10/PPN without a common parent domain map",
            "promotion_allowed": False,
            "valid_for_claim": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "hook_id": "HOOK1473_3_R10_to_finite_range",
            "new_residual_rows": "ERV1473_4_finite_range_operator",
            "prior_debt_rows": "DEBT1472_3_R10_operator",
            "existing_gate_or_vector": rel(KX_ROWS_1035),
            "hook_effect": "keeps finite-range alpha(lambda) as a curve/theorem-zero row, not a public pass",
            "promotion_allowed": False,
            "valid_for_claim": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "hook_id": "HOOK1473_4_Newton_PPN_to_local_GR",
            "new_residual_rows": "ERV1473_5_PiM_measured_GM;ERV1473_6_metric_PPN_readout;ERV1473_7_transition_activation",
            "prior_debt_rows": "DEBT1472_4_EH_Newton_PPN_left_side",
            "existing_gate_or_vector": rel(LOCAL_PROMOTION_482),
            "hook_effect": "keeps GR/Newton reduction honest: measured GM and PPN vector must be derived or scored",
            "promotion_allowed": False,
            "valid_for_claim": False,
        },
    ]


def ppn_newton_gate_rows(residuals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "NPLG1473_0_double_zero",
            "gate": "parent double-zero theorem closes every ERV1473 coupling row",
            "current_result": "FAIL_FOR_CLAIM",
            "evidence": "DZ1473_4 verdict is not parent-derived",
            "claim_effect": "no theorem-zero promotion",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "NPLG1473_1_Newton",
            "gate": "Newtonian limit follows with stable measured GM",
            "current_result": "FAIL_FOR_CLAIM",
            "evidence": "ERV1473_1, ERV1473_2, and ERV1473_5 block source/GM calibration",
            "claim_effect": "no source-normalized Newton promotion",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "NPLG1473_2_PPN",
            "gate": "PPN residual vector is zero or below bounds",
            "current_result": "FAIL_FOR_CLAIM",
            "evidence": "ERV1473_0, ERV1473_3, ERV1473_4, ERV1473_6, and ERV1473_7 remain unfilled",
            "claim_effect": "no PPN/local-GR promotion",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "NPLG1473_3_executable_residual_policy",
            "gate": "every failed premise emits a residual row with formula/source/gate",
            "current_result": "PASS_GUARD",
            "evidence": f"executable rows written={len(residuals)}",
            "claim_effect": "private workbench is stricter and more testable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CM1473_0_fixed_point_with_slope",
            "countermodel": "Phi0 solves E_A=0, but C(Phi)=c1(Phi-Phi0) has nonzero first derivative and sources a fifth force/readout slope.",
            "survives_why": "stationary fixed point alone does not imply double zero",
            "killed_by_1473": False,
            "needed_to_kill": "parent symmetry/selection rule forcing partial_A C_i(Phi0)=0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CM1473_1_universal_equations_nonuniversal_source",
            "countermodel": "matter equations look universal while Hilbert source weights differ by species/source label.",
            "survives_why": "single source-current owner is conditional only",
            "killed_by_1473": False,
            "needed_to_kill": "connected ordinary matter category and source-label forgetting",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CM1473_2_EH_left_side_bad_readout",
            "countermodel": "the left-side operator is EH-like but Pi_M/readout/boundary calibration shifts measured GM or PPN coefficients.",
            "survives_why": "Pi_M lock and metric readout double-zero are unsigned",
            "killed_by_1473": False,
            "needed_to_kill": "measured-GM calibration and weak-field PPN readout theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def live_guard_rows() -> list[dict[str, Any]]:
    guarded = [
        ("LG1473_0_Cparent", LIVE_CPARENT, "live C_parent WEP coefficient import"),
        ("LG1473_1_double_zero", LIVE_DOUBLE_ZERO, "live double-zero claim import"),
        ("LG1473_2_alpha_product", LIVE_ALPHA_PRODUCT, "live alpha residual product claim rows"),
        ("LG1473_3_local_GR", LIVE_LOCAL_GR, "live local-GR claim promotion rows"),
        ("LG1473_4_PPN_vector", LIVE_PPN_VECTOR, "live PPN residual vector claim rows"),
    ]
    return [
        {
            "guard_id": guard_id,
            "path": rel(path),
            "meaning": meaning,
            "exists_now": path.exists(),
            "would_write_in_1473": False,
            "status": "ABSENT_EXPECTED" if not path.exists() else "PRESENT_PREEXISTING_REVIEW_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for guard_id, path, meaning in guarded
    ]


def reduction_gate_rows(theorems: list[dict[str, Any]], premises: list[dict[str, Any]], residuals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    exact_theorem = any(row["proof_status"] == "EXACT_CONDITIONAL_THEOREM" for row in theorems)
    verdict_refuses = any(row["proof_status"] == "NOT_PARENT_DERIVED_EMIT_EXECUTABLE_RESIDUAL_VECTOR" for row in theorems)
    premises_unsigned = all(not truth(row["claim_allowed"]) for row in premises)
    residuals_executable = all(
        row["residual_expression"]
        and row["source_artifact"]
        and row["bound_or_gate"]
        and not truth(row["passes_required_gate"])
        and not truth(row["valid_for_local_GR_claim"])
        for row in residuals
    )
    blocks_core = any(truth(row["blocks_Newton"]) for row in residuals) and any(truth(row["blocks_PPN"]) for row in residuals) and any(truth(row["blocks_local_GR"]) for row in residuals)
    return [
        {
            "gate_id": "GATE1473_0_double_zero_math",
            "gate": "double-zero Taylor lemma is exact conditionally",
            "gate_pass": exact_theorem,
            "claim_effect": "conditional math only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1473_1_parent_double_zero_signed",
            "gate": "parent action proves all C_i(Phi0)=0 and partial_A C_i(Phi0)=0",
            "gate_pass": False,
            "claim_effect": "no local coupling theorem-zero promotion",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1473_2_fixed_point_no_smuggle",
            "gate": "fixed point is not treated as sufficient for double zero",
            "gate_pass": True,
            "claim_effect": "no plateau axiom smuggled",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1473_3_premise_audit_unsigned",
            "gate": "unsigned premises are explicitly listed",
            "gate_pass": premises_unsigned,
            "claim_effect": "blocks promotion",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1473_4_executable_residuals_written",
            "gate": "failed premises emit executable residual rows",
            "gate_pass": residuals_executable,
            "claim_effect": "testable nonclaim artifacts",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1473_5_core_claims_blocked",
            "gate": "Newton/PPN/local-GR blockers remain explicit",
            "gate_pass": blocks_core,
            "claim_effect": "no GR/Newton promotion",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1473_6_refusal_recorded",
            "gate": "double-zero promotion refusal is recorded",
            "gate_pass": verdict_refuses,
            "claim_effect": "prevents false closure",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1473_7_local_GR_claim",
            "gate": "local GR/Newton/PPN claim allowed",
            "gate_pass": False,
            "claim_effect": "explicitly forbidden in 1473",
            "valid_for_claim": False,
        },
    ]


def signing_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "SIGN1473_0_double_zero",
            "target": "parent coupling double-zero theorem and executable local residual vector",
            "double_zero_conditional_theorem_written": True,
            "parent_complete_Ci_list_signed": False,
            "parent_double_zero_signed": False,
            "universal_source_current_signed": False,
            "same_readout_frame_signed": False,
            "finite_mode_operator_signed": False,
            "executable_residual_vector_written": True,
            "double_zero_claim_allowed": False,
            "Newton_transfer_allowed": False,
            "PPN_claim_allowed": False,
            "local_GR_claim_allowed": False,
            "decision": "REFUSE_DOUBLE_ZERO_PROMOTION_EMIT_EXECUTABLE_RESIDUAL_VECTOR",
            "reason": "the Taylor lemma is exact, but the parent action has not signed the complete coupling list, double-zero premises, source current, readout frame, or finite-mode operator",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1473_0",
            "decision": "keep double-zero as the clean derivation route",
            "why": "it gives a real GR/Newton-style local reduction mechanism rather than a fitted local plateau",
            "consequence": "future work should prove parent ownership of every C_i and first derivative",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1473_1",
            "decision": "do not let fixed-point language smuggle the result",
            "why": "E_A(Phi0)=0 does not force C_i(Phi0)=0 or partial_A C_i(Phi0)=0",
            "consequence": "stationarity and mass gap support the route but do not replace coupling proofs",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1473_2",
            "decision": "use executable residual rows as the fallback",
            "why": "every missing theorem can now be tested, bounded, or killed by a later parent proof",
            "consequence": "local-GR/Newton/PPN branch becomes stricter and more empirical-ready without claiming success",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1473_0_1474",
            "next_target": "1474-Y5-R10-RAB-complete-Ci-parent-action-map-or-residual-vector-evaluator.md",
            "script": "scripts/Y5_R10_RAB_complete_Ci_parent_action_map_or_residual_vector_evaluator.py",
            "objective": "build the complete parent coupling list C_i from action blocks and map each C_i to either a double-zero proof obligation or an executable residual-vector evaluator row",
            "include": "alpha_EM; source weights; matter-frame charges; tau/readout screens; finite-range mode; Pi_M; metric PPN readout; transition activation",
            "exclude": "GitHub action; formalization-workbench edits; local-GR pass; WEP/R10/clock claim promotion; bound inversion",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def generated_csvs() -> list[Path]:
    return [
        SOURCE_REGISTER,
        DOUBLE_ZERO_THEOREM,
        PREMISE_AUDIT,
        EXEC_RESIDUAL_VECTOR,
        RESIDUAL_HOOK_MAP,
        PPN_NEWTON_GATE,
        COUNTERMODELS,
        QUAR_RESIDUAL_VECTOR,
        QUAR_THEOREM,
        LIVE_GUARD,
        REDUCTION_GATES,
        SIGNING_DECISION,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]


def csv_parse_clean(paths: list[Path]) -> bool:
    try:
        return all(read_csv_rows(path) for path in paths)
    except Exception:
        return False


def branch_copies_exist() -> bool:
    return BRANCH_RESIDUAL_VECTOR.exists() and BRANCH_THEOREM.exists() and BRANCH_SIGNING.exists()


def validation_rows(
    sources: list[dict[str, Any]],
    theorems: list[dict[str, Any]],
    premises: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    hooks: list[dict[str, Any]],
    gate_update: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    live_guard: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    signing: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    local_sources_exist = all(row["source_type"] != "local_file" or truth(row["exists"]) for row in sources)
    exact_theorem = any(row["proof_status"] == "EXACT_CONDITIONAL_THEOREM" for row in theorems)
    fixed_point_guard = any(row["proof_status"] == "NO_GO_GUARD" for row in theorems)
    refusal = any(row["proof_status"] == "NOT_PARENT_DERIVED_EMIT_EXECUTABLE_RESIDUAL_VECTOR" for row in theorems)
    premises_sources_exist = all((ROOT / row["source_path"]).exists() for row in premises)
    premises_unsigned = all(not truth(row["claim_allowed"]) and row["status"] != "SIGNED" for row in premises)
    residual_sources_exist = all((ROOT / row["source_artifact"]).exists() for row in residuals)
    residuals_executable = all(
        row["residual_expression"]
        and row["bound_or_gate"]
        and row["theorem_zero_certificate"].startswith("MISSING")
        and row["numeric_source_file"].startswith("MISSING")
        and not truth(row["passes_required_gate"])
        and not truth(row["valid_for_local_GR_claim"])
        for row in residuals
    )
    residuals_block_core = any(truth(row["blocks_Newton"]) for row in residuals) and any(truth(row["blocks_PPN"]) for row in residuals) and any(truth(row["blocks_local_GR"]) for row in residuals)
    hooks_nonclaim = all(not truth(row["promotion_allowed"]) and not truth(row["valid_for_claim"]) for row in hooks)
    gate_update_nonclaim = all(not truth(row["claim_allowed"]) for row in gate_update)
    countermodels_retained = all(not truth(row["killed_by_1473"]) for row in countermodels)
    live_paths_untouched = all(not truth(row["exists_now"]) and not truth(row["would_write_in_1473"]) for row in live_guard)
    safe_gate_pattern = truth(gates[0]["gate_pass"]) and not truth(gates[1]["gate_pass"]) and truth(gates[2]["gate_pass"]) and truth(gates[3]["gate_pass"]) and truth(gates[4]["gate_pass"]) and truth(gates[5]["gate_pass"]) and truth(gates[6]["gate_pass"]) and not truth(gates[7]["gate_pass"])
    signing_refuses = all(
        truth(row["double_zero_conditional_theorem_written"])
        and truth(row["executable_residual_vector_written"])
        and not truth(row["parent_complete_Ci_list_signed"])
        and not truth(row["parent_double_zero_signed"])
        and not truth(row["universal_source_current_signed"])
        and not truth(row["same_readout_frame_signed"])
        and not truth(row["finite_mode_operator_signed"])
        and not truth(row["double_zero_claim_allowed"])
        and not truth(row["Newton_transfer_allowed"])
        and not truth(row["PPN_claim_allowed"])
        and not truth(row["local_GR_claim_allowed"])
        for row in signing
    )
    generated_parse = csv_parse_clean(generated_csvs())
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_untouched = formalization_modified_count() == 0
    checks = [
        ("VAL1473_0_sources", local_sources_exist, "all cited local source paths exist"),
        ("VAL1473_1_exact_theorem", exact_theorem, "double-zero Taylor theorem written conditionally"),
        ("VAL1473_2_fixed_point_guard", fixed_point_guard, "fixed point alone is not treated as enough"),
        ("VAL1473_3_refusal", refusal, "double-zero promotion refused"),
        ("VAL1473_4_premise_sources", premises_sources_exist, "all premise audit source paths exist"),
        ("VAL1473_5_premises_unsigned", premises_unsigned, "premises remain unsigned/nonclaim"),
        ("VAL1473_6_residual_sources", residual_sources_exist, "all executable residual source paths exist"),
        ("VAL1473_7_residuals_executable", residuals_executable, "residual rows have formula/source/gate and missing theorem/numeric certificates"),
        ("VAL1473_8_residuals_block_core", residuals_block_core, "residuals block Newton/PPN/local-GR explicitly"),
        ("VAL1473_9_hooks_nonclaim", hooks_nonclaim, "hook map is routing only"),
        ("VAL1473_10_gate_update_nonclaim", gate_update_nonclaim, "Newton/PPN/local-GR gate update remains nonclaim"),
        ("VAL1473_11_countermodels", countermodels_retained, "all countermodels retained"),
        ("VAL1473_12_live_paths", live_paths_untouched, "critical live claim/import paths remain absent"),
        ("VAL1473_13_gate_pattern", safe_gate_pattern, "conditional/residual gates pass while claim gates fail"),
        ("VAL1473_14_signing_refuses", signing_refuses, "parent signing refuses double-zero/Newton/PPN/local-GR promotion"),
        ("VAL1473_15_generated_csv_parse", generated_parse, "all generated 1473 CSVs parse cleanly"),
        ("VAL1473_16_branch_copies", branch_copies_exist(), "nonclaim branch/quarantine copies written"),
        ("VAL1473_17_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1473_18_formalization_untouched", formalization_untouched, f"formalization modified-file count since start={formalization_modified_count()}"),
    ]
    overall = all(result for _, result, _ in checks)
    checks.append(("VAL1473_19_overall", overall, "1473 derives the conditional double-zero theorem and emits executable residual rows without promoting local GR"))
    generated = now()
    return [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "generated_utc": generated,
        }
        for check_id, result, detail in checks
    ]


def write_doc(
    sources: list[dict[str, Any]],
    theorems: list[dict[str, Any]],
    premises: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    hooks: list[dict[str, Any]],
    gate_update: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    signing: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> None:
    lines: list[str] = []
    lines.append("# 1473 - Y5 R10 RAB Parent Coupling Double-Zero Theorem Or Executable Residual Vector")
    lines.append("")
    lines.append("## Verdict")
    lines.append("- The double-zero law is mathematically clean: if every local non-EH coupling has `C_i(Phi0)=0` and `partial_A C_i(Phi0)=0`, first-order local leakage is killed.")
    lines.append("- It is not parent-derived yet: the corpus has not signed the complete `C_i` list, source-current owner, same-readout frame, finite-mode operator, or PPN readout.")
    lines.append("- The fallback is now executable: every surviving coupling leak is written as a residual-vector row with formula, source artifact, gate, and missing certificate.")
    lines.append("")
    lines.append("## Double-Zero Theorem Attempt")
    lines.append("| theorem_id | proof_status | missing_for_parent_claim |")
    lines.append("|---|---|---|")
    for row in theorems:
        lines.append(f"| {row['theorem_id']} | {row['proof_status']} | {row['missing_for_parent_claim']} |")
    lines.append("")
    lines.append("## Premise Audit")
    lines.append("| premise_id | status | blocks |")
    lines.append("|---|---|---|")
    for row in premises:
        lines.append(f"| {row['premise_id']} | {row['status']} | {row['blocks']} |")
    lines.append("")
    lines.append("## Executable Residual Vector")
    lines.append("| component_id | residual_symbol | bound_or_gate | current_status | blocks_local_GR |")
    lines.append("|---|---|---|---|---:|")
    for row in residuals:
        lines.append(f"| {row['component_id']} | {row['residual_symbol']} | {row['bound_or_gate']} | {row['current_status']} | {row['blocks_local_GR']} |")
    lines.append("")
    lines.append("## Hook Map")
    lines.append("| hook_id | new_residual_rows | hook_effect |")
    lines.append("|---|---|---|")
    for row in hooks:
        lines.append(f"| {row['hook_id']} | {row['new_residual_rows']} | {row['hook_effect']} |")
    lines.append("")
    lines.append("## Newton/PPN/Local-GR Gate Update")
    lines.append("| gate_id | current_result | claim_effect |")
    lines.append("|---|---|---|")
    for row in gate_update:
        lines.append(f"| {row['gate_id']} | {row['current_result']} | {row['claim_effect']} |")
    lines.append("")
    lines.append("## Gates")
    lines.append("| gate_id | gate_pass | claim_effect |")
    lines.append("|---|---:|---|")
    for row in gates:
        lines.append(f"| {row['gate_id']} | {row['gate_pass']} | {row['claim_effect']} |")
    lines.append("")
    lines.append("## Parent Signing Decision")
    for row in signing:
        lines.append(f"- `{row['decision_id']}`: `{row['decision']}` because {row['reason']}.")
    lines.append("")
    lines.append("## Decision Ledger")
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} - {row['consequence']}.")
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
    theorems = double_zero_theorem_rows()
    premises = premise_audit_rows()
    residuals = executable_residual_rows()
    hooks = residual_hook_rows(residuals)
    gate_update = ppn_newton_gate_rows(residuals)
    countermodels = countermodel_rows()
    live_guard = live_guard_rows()
    gates = reduction_gate_rows(theorems, premises, residuals)
    signing = signing_decision_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(DOUBLE_ZERO_THEOREM, theorems)
    write_csv(PREMISE_AUDIT, premises)
    write_csv(EXEC_RESIDUAL_VECTOR, residuals)
    write_csv(RESIDUAL_HOOK_MAP, hooks)
    write_csv(PPN_NEWTON_GATE, gate_update)
    write_csv(COUNTERMODELS, countermodels)
    write_csv(QUAR_RESIDUAL_VECTOR, residuals)
    write_csv(QUAR_THEOREM, theorems)
    write_csv(LIVE_GUARD, live_guard)
    write_csv(REDUCTION_GATES, gates)
    write_csv(SIGNING_DECISION, signing)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_target)

    copy_branch(EXEC_RESIDUAL_VECTOR, BRANCH_RESIDUAL_VECTOR)
    copy_branch(DOUBLE_ZERO_THEOREM, BRANCH_THEOREM)
    copy_branch(SIGNING_DECISION, BRANCH_SIGNING)

    validation = validation_rows(sources, theorems, premises, residuals, hooks, gate_update, countermodels, live_guard, gates, signing)
    write_csv(VALIDATION, validation)
    write_doc(sources, theorems, premises, residuals, hooks, gate_update, gates, signing, decisions, validation, next_target)
    print("Y5_R10_1473_parent_coupling_double_zero_executable_residual_vector_nonclaim")


if __name__ == "__main__":
    main()

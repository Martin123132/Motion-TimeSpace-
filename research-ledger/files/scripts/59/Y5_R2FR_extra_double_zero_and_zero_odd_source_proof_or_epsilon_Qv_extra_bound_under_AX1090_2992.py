from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_COEFF = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "coefficients"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2992"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2992-Y5-R2FR-extra-double-zero-and-zero-odd-source-proof-or-epsilon-Qv-extra-bound-under-AX1090.md"

SRC_2991_DOC = ROOT / "2991-Y5-R2FR-fixed-boundary-reference-theta-zero-proof-or-epsilon-Bv-source-bound-under-AX1090.md"
SRC_2991_NEXT = RESIDUALS / "P8_Y5_R2FR_2991_NEXT_TARGET.csv"
SRC_2990_NORMAL = RESIDUALS / "P8_Y5_R2FR_2990_SELECTED_PARENT_NORMAL_FORM_CONTRACT.csv"
SRC_2990_SECTOR = RESIDUALS / "P8_Y5_R2FR_2990_SECTOR_BY_SECTOR_THETA_NORMAL_FORM_CONTRACT.csv"
SRC_2989_SECTOR = RESIDUALS / "P8_Y5_R2FR_2989_PARENT_LAGRANGIAN_THETA_SECTOR_AUDIT.csv"
SRC_2903_LEAKS = RESIDUALS / "P8_Y5_R2FR_2903_VERTICAL_SECTOR_QV_PIECE_LEAK_ROWS.csv"
SRC_MIN_BLOCKS = RESIDUALS / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv"
SRC_RESPONSE_CONTRACT = RESIDUALS / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv"
SRC_RESPONSE_VARIATION = RESIDUALS / "P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv"
SRC_GK_CONTRACT = RESIDUALS / "P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv"
SRC_GAMMA_OWNER = RESIDUALS / "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv"
SRC_GK_CANDIDATES = RESIDUALS / "P8_GK_STRESS_ACTION_CANDIDATES.csv"
SRC_SYMBOL_MAP = RESIDUALS / "P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv"
SRC_ODD_THEOREM = RESIDUALS / "P8_ODD_RESIDUAL_EXCHANGE_THEOREM.csv"
SRC_ODD_CONTRACT = RESIDUALS / "P8_ODD_RESIDUAL_EXCHANGE_CONTRACT.csv"
SRC_EXTRA_ENERGY = RESIDUALS / "P8_EXTRA_SECTOR_SILENCE_ENERGY_IDENTITY.csv"
SRC_LOCAL_ZERO_REQ = RESIDUALS / "P8_LOCAL_ZERO_EXTRA_PREMISE_REQUIREMENTS.csv"
SRC_MEMORY_TEST = RESIDUALS / "P8_DOUBLE_ZERO_MEMORY_VARIATION_TEST.csv"
SRC_2028_DOC = ROOT / "2028-Y5-R2FR-vZ-local-vacuum-double-zero-or-finite-jZB-bound.md"
SRC_2188_DOC = ROOT / "2188-Y5-R2FR-extra-sector-double-zero-and-PiM-lock-signature-or-residual-fill.md"
SRC_2189_DOC = ROOT / "2189-Y5-R2FR-parent-extra-sector-inventory-and-coupling-map-or-leakage-bounds.md"

LIVE_C_PARENT = MICRO_COEFF / "C_parent_WEP_slot_import.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2992_SOURCE_REGISTER.csv",
    "proof_chain": RESIDUALS / "P8_Y5_R2FR_2992_EXTRA_DOUBLE_ZERO_PROOF_CHAIN.csv",
    "clause_audit": RESIDUALS / "P8_Y5_R2FR_2992_EXTRA_ZERO_ODD_SOURCE_CLAUSE_AUDIT.csv",
    "epsilon": RESIDUALS / "P8_Y5_R2FR_2992_EPSILON_QV_EXTRA_BOUND_ROWS_NONCLAIM.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2992_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2992_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2992_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2992_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2992_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "proof_copy": PARENT_ACTION / "extra_double_zero_zero_odd_source_attempt_2992_NOT_SIGNED.csv",
    "epsilon_copy": LOCAL_BOUNDS / "epsilon_Qv_extra_piece_bound_rows_2992_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2992_parent_extra_sector_source_pack_or_epsilon_Qv_extra_next_NONCLAIM.csv",
}

for directory in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def anchors(path: Path, needles: list[str]) -> bool:
    haystack = text(path)
    return path.exists() and all(needle in haystack for needle in needles)


def add(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "control_only": True,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "generated_utc": RUN_UTC,
    }


def write_csv(path: Path, out_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in out_rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(out_rows)


def csv_ok(path: Path) -> bool:
    try:
        rows(path)
        return True
    except Exception:
        return False


def under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2992_00_2991_doc", SRC_2991_DOC, ["NEXT2991_0_2992", "epsilon_Qv_extra_piece"], "2991 handoff"),
        ("SRC2992_01_2991_next", SRC_2991_NEXT, ["NEXT2991_0_2992", "zero odd source"], "selected 2992 target"),
        ("SRC2992_02_2990_normal", SRC_2990_NORMAL, ["NF2990_3_extra_double_zero", "CONDITIONAL_NOT_SIGNED"], "selected normal-form extra clause"),
        ("SRC2992_03_2990_sector", SRC_2990_SECTOR, ["SNF2990_2_extra", "epsilon_Qv_extra_piece"], "sector-by-sector extra theta row"),
        ("SRC2992_04_2989_sector", SRC_2989_SECTOR, ["TLS2989_3_extra", "MISSING_EXTRA_SECTOR_VARIATION"], "Theta sector audit extra gap"),
        ("SRC2992_05_2903_leaks", SRC_2903_LEAKS, ["VSP2903_2_extra", "MISSING_ZERO_ODD_SOURCE"], "vertical sector extra leakage row"),
        ("SRC2992_06_min_blocks", SRC_MIN_BLOCKS, ["A511_3_extra_field_silence", "Hessian(V)>0"], "minimum local-GR extra-field silence block"),
        ("SRC2992_07_response_contract", SRC_RESPONSE_CONTRACT, ["RD516_4_zero_odd_source", "not_derived_hard_block"], "response doublet contract"),
        ("SRC2992_08_response_variation", SRC_RESPONSE_VARIATION, ["AV517_3_double_zero", "conditional_pass_not_MTS_promotion"], "response doublet variation"),
        ("SRC2992_09_GK_contract", SRC_GK_CONTRACT, ["GK513_3_double_zero", "F_1 survives"], "Gamma/Khat/q_loc first-variation contract"),
        ("SRC2992_10_gamma_owner", SRC_GAMMA_OWNER, ["GO516_A_response_doublet_quadratic_density", "GO516_D_residual_bound_runner"], "Gamma owner candidate actions"),
        ("SRC2992_11_GK_candidates", SRC_GK_CANDIDATES, ["GK514_B_positive_auxiliary_fields", "GK514_D_residual_branch"], "GK stress action candidates"),
        ("SRC2992_12_symbol_map", SRC_SYMBOL_MAP, ["Gamma_eff", "memory / B_mem / U_mem / I_M"], "symbol-to-action map"),
        ("SRC2992_13_odd_theorem", SRC_ODD_THEOREM, ["E4_local_no_odd_boundary_charge", "E5_current_corpus"], "odd residual exchange theorem"),
        ("SRC2992_14_odd_contract", SRC_ODD_CONTRACT, ["O4_local_odd_charge_zero", "not_derived"], "odd residual exchange contract"),
        ("SRC2992_15_energy_identity", SRC_EXTRA_ENERGY, ["E506_scalar_positive_operator", "boundary_flux=0"], "extra-sector energy identity"),
        ("SRC2992_16_local_zero_req", SRC_LOCAL_ZERO_REQ, ["P3_stress_Bianchi", "P4_no_total_cancellation"], "local zero premise requirements"),
        ("SRC2992_17_memory_test", SRC_MEMORY_TEST, ["required_general_condition", "fail_hidden_selector_exchange"], "memory double-zero variation test"),
        ("SRC2992_18_2028_doc", SRC_2028_DOC, ["VDZ2028_7_verdict", "THEOREM_PROVED_CONDITIONAL_NOT_ACTIVATED"], "canonical local-vacuum double-zero theorem"),
        ("SRC2992_19_2188_doc", SRC_2188_DOC, ["DZ2188_7_verdict", "THEOREM_CONTRACT_PASS_CURRENT_CLAIM_FAILS"], "extra-sector double-zero/PiM signature precedent"),
        ("SRC2992_20_2189_doc", SRC_2189_DOC, ["EI2189_0_GK", "EI2189_1_response_memory"], "extra-sector inventory and coupling map"),
    ]
    return [
        add(
            {
                "source_id": source_id,
                "source_path": str(path),
                "role": role,
                "required_anchors": ";".join(needles),
                "exists": path.exists(),
                "anchors_found": anchors(path, needles),
            }
        )
        for source_id, path, needles, role in specs
    ]


def proof_chain_rows() -> list[dict[str, Any]]:
    data = [
        (
            "EDZ2992_0_target",
            "extra-sector local silence",
            "Show the retained non-EH extra sector has no zeroth-order stress/current and no first-order local source/readout/stress around the local branch.",
            "TARGET_SHARP",
            "requires parent S_extra, branch data, no direct source slot, metric/readout lock, boundary no-flux and M_ref",
            False,
        ),
        (
            "EDZ2992_1_canonical_bulk",
            "canonical bulk double-zero theorem",
            "For S_Z=int sqrt(-g)[-1/2 K_AB grad Z^A grad Z^B - V(Z)], if Z=Z0 constant, V(Z0)=0 and partial_A V(Z0)=0, then T_Z(Z0)=0 and delta T_Z|Z0 has no bulk linear term.",
            "EXACT_CONDITIONAL_THEOREM",
            "only covers canonical bulk fields after parent S_Z, K_AB, V, Z0 and vacuum subtraction are sourced",
            False,
        ),
        (
            "EDZ2992_2_coupling_double_zero",
            "coupling/readout double-zero",
            "Every non-EH coupling C_i(Z)O_i must satisfy C_i(Z0)=0 and partial_A C_i(Z0)=0, including metric response, readout, memory, projector/domain and source-normalization channels.",
            "REQUIRED_NOT_PARENT_SIGNED",
            "without a complete C_i/O_i inventory, F_1 can survive in a hidden channel",
            False,
        ),
        (
            "EDZ2992_3_positive_gap",
            "positive source-free operator",
            "If L_Z is self-adjoint positive on compact local collars and J_Z=B_Z=0, the energy identity forces Z-Z0=0 modulo declared pure gauge/topological modes.",
            "EXACT_CONDITIONAL_BOUND_FORM",
            "mass gap/operator spectrum, boundary flux and source work are missing for current MTS",
            False,
        ),
        (
            "EDZ2992_4_zero_odd_source",
            "zero exchange-odd source",
            "Exchange-even parent action with matter/readout depending only on even variables forbids linear odd-source terms J_Z and B_Z.",
            "CONDITIONAL_THEOREM_NOT_ACTIVATED",
            "component map, even matter/readout and local odd boundary/source charge zero are not parent-derived",
            False,
        ),
        (
            "EDZ2992_5_Gamma_Khat",
            "Gamma/Khat/q_loc residual channel",
            "Gamma_eff/K_hat must be metric-response matched, Helmholtz-compatible, Euler-closed and double-zero so q_loc becomes on-shell residual zero.",
            "HARD_BLOCK_NOT_CLOSED",
            "K_hat metric response, Helmholtz, Euler closure, projector ownership and boundary terms remain unsigned",
            False,
        ),
        (
            "EDZ2992_6_verdict",
            "current extra-sector double-zero result",
            "The double-zero mechanism is mathematically viable as a conditional normal form, but current MTS does not parent-sign the full extra-sector silence stack.",
            "EXTRA_DOUBLE_ZERO_NOT_ACTIVATED_RETAIN_EPSILON_QV_EXTRA",
            "stage explicit epsilon_Qv_extra_piece rows rather than claiming local GR/Newton/PPN",
            False,
        ),
    ]
    return [
        add(
            {
                "proof_id": proof_id,
                "step": step,
                "mathematical_statement": statement,
                "current_status": status,
                "blocking_gap": gap,
                "theorem_zero_claimed": theorem_zero,
            }
        )
        for proof_id, step, statement, status, gap, theorem_zero in data
    ]


def clause_audit_rows() -> list[dict[str, Any]]:
    data = [
        ("ECA2992_0_parent_SZ", "parent S_extra/S_Z action and field list", "MISSING_PARENT_SOURCE", "without it the theorem is a prototype, not MTS", "epsilon_extra_parent_action"),
        ("ECA2992_1_branch_data", "Z0, K_AB, V(Z0), partial V, Hessian/mass gap", "MISSING_BRANCH_DATA", "stationarity and positive gap cannot be activated", "epsilon_extra_bulk_C0;epsilon_extra_positive_gap_hair"),
        ("ECA2992_2_Ci_inventory", "complete C_i O_i coupling/readout/source inventory", "MISSING_COUPLING_INVENTORY", "hidden first-order F1 channel can survive", "epsilon_extra_bulk_F1"),
        ("ECA2992_3_metric_response", "Gamma_eff/K_hat metric-response and Helmholtz match", "MISSING_GK_METRIC_RESPONSE_HELMHOLTZ", "q_loc remains a live residual", "epsilon_GK_metric_response"),
        ("ECA2992_4_zero_odd_source", "no exchange-odd matter/source/boundary charge", "MISSING_ZERO_ODD_SOURCE", "J_Z or B_Z can source the local branch", "epsilon_extra_zero_odd_source"),
        ("ECA2992_5_readout_lock", "g_readout and physical q_loc/PPN residual equal the protected parent variable through first order", "MISSING_READOUT_PPN_LOCK", "auxiliary zero may not zero observed residuals", "epsilon_extra_readout_linear"),
        ("ECA2992_6_boundary", "extra theta/Q/boundary no-flux", "MISSING_EXTRA_BOUNDARY_ZERO_PROOF", "bulk double-zero can leak through Hamiltonian boundary", "epsilon_extra_boundary_flux"),
        ("ECA2992_7_Mref", "positive same-frame M_ref", "MISSING_POSITIVE_SAME_FRAME_MREF", "residual rows cannot be score-ready", "epsilon_extra_Mref"),
        ("ECA2992_8_total", "all extra-sector clauses close together", "EXTRA_TOTAL_NOT_SIGNED", "local GR cannot inherit EH at first order", "epsilon_Qv_extra_piece_total_abs"),
    ]
    return [
        add(
            {
                "clause_id": clause_id,
                "clause": clause,
                "current_status": status,
                "if_open": gap,
                "residual_symbol": residual,
                "clause_passed_now": False,
            }
        )
        for clause_id, clause, status, gap, residual in data
    ]


def epsilon_rows() -> list[dict[str, Any]]:
    data = [
        ("EQE2992_00_definition", "epsilon_Qv_extra_piece", "extra motion/time/domain/memory contribution to missing theta/current surface row", "epsilon_Qv_extra_piece <= sum_abs(EQE2992_01..09); no cancellation between components", "dimensionless_after_M_ref", "EXTRA_TOTAL_NOT_SIGNED", "VSP2903_2_extra"),
        ("EQE2992_01_parent_action", "epsilon_extra_parent_action", "parent S_extra/S_Z source and field-list gap", "action-source absence guard for all extra rows", "boolean_or_action_norm_guard", "MISSING_PARENT_SOURCE", "ECA2992_0_parent_SZ"),
        ("EQE2992_02_bulk_C0", "epsilon_extra_bulk_C0", "zeroth-order extra stress/current at local branch", "abs(T_extra(Z0) or Q_extra(Z0))/M_ref", "dimensionless_bulk_stress", "MISSING_V0_ZERO_SUBTRACTION_AND_BRANCH_DATA", "EDZ2992_1_canonical_bulk"),
        ("EQE2992_03_bulk_F1", "epsilon_extra_bulk_F1", "first-order extra-sector leakage F_1", "norm(partial_A T_extra|Z0, partial_A C_i|Z0, partial_A readout|Z0)", "dimensionless_operator_norm", "MISSING_COUPLING_DERIVATIVE_ZERO_PROOF", "EDZ2992_2_coupling_double_zero"),
        ("EQE2992_04_gap_hair", "epsilon_extra_positive_gap_hair", "failure of positive operator/gap to force Z=Z0", "A_Z^2 exp(-2r/ell_Z) or source-work/gap bound", "dimensionless_or_length_scale", "MISSING_MASS_GAP_PROFILE_AND_SOURCE_WORK", "EDZ2992_3_positive_gap"),
        ("EQE2992_05_zero_odd_source", "epsilon_extra_zero_odd_source", "exchange-odd source/boundary charge", "abs(int_A J_Z + int_boundary B_Z)/M_ref", "dimensionless_odd_source_charge", "MISSING_ZERO_ODD_SOURCE", "EDZ2992_4_zero_odd_source"),
        ("EQE2992_06_GK_metric", "epsilon_GK_metric_response", "Gamma/Khat/q_loc action/metric-response/Helmholtz residual", "norm(K_hat-K_metric)+Helmholtz_defect+Euler_closure_defect", "mixed_metric_response_norm", "MISSING_GK_METRIC_RESPONSE_HELMHOLTZ", "GK513_0_to_5"),
        ("EQE2992_07_memory", "epsilon_memory_response_doublet", "memory/response doublet component-map and source gap", "component-map defect plus zero-odd-source defect for memory channels", "dimensionless_memory_response", "MISSING_MEMORY_COMPONENT_MAP_AND_PPN_LOCK", "RD516_0_to_5"),
        ("EQE2992_08_readout", "epsilon_extra_readout_linear", "linear metric/readout/PPN residual from extra variables", "norm(D_A g_readout|Z0, D_A P_loc|Z0, D_A Pi_M|Z0)", "dimensionless_readout_operator_norm", "MISSING_READOUT_PPN_LOCK", "A511_6_metric_readout"),
        ("EQE2992_09_boundary", "epsilon_extra_boundary_flux", "extra-sector theta/Q/boundary leakage", "abs(int_S(Q_extra+C_extra-i_v Theta_extra))/M_ref boundary part", "dimensionless_boundary_flux", "MISSING_EXTRA_BOUNDARY_ZERO_PROOF", "FBZ2991_5_verdict"),
        ("EQE2992_10_Mref", "epsilon_extra_Mref", "positive same-frame denominator missing for extra-sector scoring", "normalization guard for epsilon_Qv_extra_piece", "dimensionless_normalization_guard", "MISSING_POSITIVE_SAME_FRAME_MREF", "TLS2989_7_Mref"),
        ("EQE2992_11_total", "epsilon_Qv_extra_piece_total_abs", "source-ready total extra-sector theta/current residual", "sum_abs(EQE2992_01..10)", "dimensionless_after_M_ref", "MISSING_SOURCE_BACKED_UPPER_BOUND", "EQE2992_00_definition"),
    ]
    return [
        add(
            {
                "epsilon_id": eps_id,
                "symbol": symbol,
                "definition": definition,
                "bound_interface": formula,
                "units": units,
                "current_status": status,
                "current_value": "MISSING_SOURCE_BACKED_UPPER_BOUND",
                "lower_bound": "0",
                "upper_bound": "MISSING_SOURCE_BACKED_UPPER_BOUND",
                "source_anchor": anchor,
                "source_ready_template": True,
                "finite_value_present": False,
                "theorem_zero_claimed": False,
                "no_cancellation_policy": True,
            }
        )
        for eps_id, symbol, definition, formula, units, status, anchor in data
    ]


def gate_rows() -> list[dict[str, Any]]:
    data = [
        ("GATE2992_0_conditional_theorem", "canonical extra-sector double-zero theorem exists as conditional prototype", True, "CONDITIONAL_THEOREM_ONLY"),
        ("GATE2992_1_parent_SZ", "parent S_extra/S_Z and field list sourced", False, "MISSING_PARENT_SOURCE"),
        ("GATE2992_2_branch_data", "Z0/K/V/Vprime/Hessian/mass gap sourced", False, "MISSING_BRANCH_DATA"),
        ("GATE2992_3_Ci_inventory", "all coupling/readout/source C_i and derivatives double-zero", False, "MISSING_COUPLING_INVENTORY"),
        ("GATE2992_4_zero_odd_source", "exchange-odd source and boundary charge zero", False, "MISSING_ZERO_ODD_SOURCE"),
        ("GATE2992_5_GK_metric", "Gamma/Khat metric-response Helmholtz/Euler closure", False, "MISSING_GK_METRIC_RESPONSE_HELMHOLTZ"),
        ("GATE2992_6_readout", "readout/PPN/projector lock through first order", False, "MISSING_READOUT_PPN_LOCK"),
        ("GATE2992_7_boundary", "extra theta/Q/boundary no-flux", False, "MISSING_EXTRA_BOUNDARY_ZERO_PROOF"),
        ("GATE2992_8_Mref", "positive same-frame M_ref exists", False, "MISSING_POSITIVE_SAME_FRAME_MREF"),
        ("GATE2992_9_promote_extra_zero", "promote epsilon_Qv_extra_piece=0", False, "all extra-sector gates must pass"),
        ("GATE2992_10_promote_local_GR", "promote Theta/Omega/local-GR branch", False, "not allowed from extra-only checkpoint"),
    ]
    return [
        add(
            {
                "gate_id": gate_id,
                "gate": gate,
                "condition_passed": passed,
                "status": status,
                "promotion_allowed_now": False,
            }
        )
        for gate_id, gate, passed, status in data
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        add(
            {
                "decision_id": "DEC2992_0_theorem_gain",
                "decision": "Keep the canonical double-zero theorem as a real conditional mechanism.",
                "because": "stationary vacuum subtraction plus zero first derivative and positive gap gives a mathematically clean way for extra bulk stress to start only at second order.",
                "next_action": "do not downgrade this to hand-waving; source the actual parent S_extra data next.",
            }
        ),
        add(
            {
                "decision_id": "DEC2992_1_no_activation",
                "decision": "Do not activate the theorem for current MTS.",
                "because": "the required parent S_Z, branch data, full C_i/O_i inventory, zero odd source, GK metric response, readout lock, boundary no-flux and M_ref are not signed together.",
                "next_action": "retain epsilon_Qv_extra_piece_total_abs as explicit nonclaim residual.",
            }
        ),
        add(
            {
                "decision_id": "DEC2992_2_next",
                "decision": "Next target should source the parent extra-sector normal-form package before moving to projector.",
                "because": "without S_Z/K/V/Z0/mass-gap/no-source inputs, the best theorem cannot become a branch certificate.",
                "next_action": "build 2993 around parent S_extra/S_Z source pack or first epsilon_Qv_extra numeric source row.",
            }
        ),
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add(
            {
                "next_id": "NEXT2992_0_2993",
                "priority": "selected_primary",
                "next_doc": "2993-Y5-R2FR-parent-extra-sector-source-normal-form-pack-or-first-epsilon-Qv-extra-numeric-row-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_parent_extra_sector_source_normal_form_pack_or_first_epsilon_Qv_extra_numeric_row_under_AX1090_2993.py",
                "objective": "Source or reject the actual parent extra-sector normal-form inputs S_Z, Z0, K_AB, V(Z0), partial V, Hessian/mass gap, C_i/O_i inventory, no-source slot and Q_Z boundary term; if missing, fill the first epsilon_Qv_extra source-bound row without claiming local GR.",
                "include": "S_extra source path;field list;Z0 branch;K_AB sign;V0/Vprime0/Hessian;m_Z^2;C_i and dC_i;J_Z/B_Z;readout derivative;boundary flux;M_ref dependency",
                "exclude": "C_parent import;Omega promotion;V_WEP promotion;local-GR claim;Newton claim;public/GitHub action;formalization-workbench edits",
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [add({"copy_id": key, "path": str(path), "exists": path.exists()}) for key, path in BRANCH_OUTPUTS.items()]


def validation(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    csv_paths = [*OUTPUTS.values(), *BRANCH_OUTPUTS.values()]
    generated = [*csv_paths, DOC]
    formal_count = sum(1 for path in FORMALIZATION.rglob("*2992*") if path.is_file()) if FORMALIZATION.exists() else 0
    theorem_retained = any(
        row["proof_id"] == "EDZ2992_1_canonical_bulk"
        and row["current_status"] == "EXACT_CONDITIONAL_THEOREM"
        and not row["theorem_zero_claimed"]
        for row in all_rows["proof_chain"]
    )
    total_not_activated = any(
        row["proof_id"] == "EDZ2992_6_verdict"
        and row["current_status"] == "EXTRA_DOUBLE_ZERO_NOT_ACTIVATED_RETAIN_EPSILON_QV_EXTRA"
        for row in all_rows["proof_chain"]
    )
    epsilon_nonclaim = all(
        row["source_ready_template"]
        and not row["valid_for_claim"]
        and not row["claim_allowed"]
        and not row["theorem_zero_claimed"]
        for row in all_rows["epsilon"]
    )
    checks = [
        ("VAL2992_0_sources_exist", all(row["exists"] for row in all_rows["sources"]), "all cited local source paths exist", True),
        ("VAL2992_1_anchors_found", all(row["anchors_found"] for row in all_rows["sources"]), "all cited source anchors found", True),
        ("VAL2992_2_conditional_theorem_retained", theorem_retained, "canonical double-zero theorem retained only conditionally", True),
        ("VAL2992_3_total_not_activated", total_not_activated, "full extra-sector silence not activated", True),
        ("VAL2992_4_eps_source_ready_nonclaim", epsilon_nonclaim, "epsilon_Qv_extra rows source-ready but nonclaim", True),
        ("VAL2992_5_no_promotion", all(not row["promotion_allowed_now"] for row in all_rows["gates"]), "no extra-sector or local-GR promotion allowed", True),
        ("VAL2992_6_no_live_cparent", not LIVE_C_PARENT.exists(), "C_parent_WEP_slot_import.csv not created or promoted", True),
        ("VAL2992_7_next_written", any(row["next_id"] == "NEXT2992_0_2993" for row in all_rows["next"]), "2993 next target written", True),
        ("VAL2992_8_branches_exist", all(row["exists"] for row in all_rows["branches"]), "branch copies exist", True),
        ("VAL2992_9_csvs_parse", all(csv_ok(path) for path in csv_paths), "all generated CSVs parse", True),
        ("VAL2992_10_outputs_under_post", all(under(path, ROOT) for path in generated), "all generated outputs under post-checkpoint-work", True),
        ("VAL2992_11_formalization_clean", formal_count == 0, f"no 2992 outputs in formalization-workbench (count={formal_count})", True),
        ("VAL2992_12_doc_written", DOC.exists(), "2992 markdown checkpoint exists", True),
    ]
    out_rows = [add({"validation_id": check_id, "passed": bool(passed), "check": check, "required": required}) for check_id, passed, check, required in checks]
    out_rows.append(add({"validation_id": "VAL2992_OVERALL", "passed": all(row["passed"] for row in out_rows), "check": "2992 validation overall", "required": True}))
    return out_rows


def esc(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def table(out_rows: list[dict[str, Any]], cols: list[str]) -> str:
    if not out_rows:
        return "_No rows._"
    return "\n".join(
        [
            "| " + " | ".join(cols) + " |",
            "| " + " | ".join("---" for _ in cols) + " |",
            *["| " + " | ".join(esc(row.get(col, "")) for col in cols) + " |" for row in out_rows],
        ]
    )


def write_markdown(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    outputs = [{"output": key, "path": str(path), "exists": path.exists()} for key, path in OUTPUTS.items() if key != "validation"]
    branches = [{"copy": key, "path": str(path), "exists": path.exists()} for key, path in BRANCH_OUTPUTS.items()]
    DOC.write_text(
        f"""# 2992 - Extra Double-Zero and Zero-Odd-Source Proof or epsilon_Qv_extra Bound

Status: `Y5_R2FR_2992_canonical_extra_double_zero_theorem_retained_conditionally_not_activated_epsilon_Qv_extra_rows_staged_nonclaim`

Claim ceiling: `no_extra_sector_silence_claim_no_Theta_parent_promotion_no_Omega_promotion_no_parent_generator_no_VWEP_promotion_no_Cparent_import_no_local_GR_no_Newton_no_WEP_no_R10_no_PPN_no_clock_no_orbital_no_public_claim`

## Summary

- The conditional mechanism is real: a canonical extra sector with vacuum subtraction, stationary branch, zero first derivative and positive gap can have no zeroth-order bulk stress and no first-order bulk leakage.
- That is not enough for current MTS. The actual parent `S_extra/S_Z`, branch data, full coupling inventory, zero odd source, Gamma/Khat metric response, readout lock, boundary no-flux and `M_ref` are not signed together.
- So the theorem is retained as a private derivation scaffold, not activated as local GR.
- `epsilon_Qv_extra_piece` is now split into source-ready nonclaim rows so the extra sector cannot hide inside the EH comparator.

## Generated Outputs

{table(outputs, ["output", "path", "exists"])}

## Branch Copies

{table(branches, ["copy", "path", "exists"])}

## Extra Double-Zero Proof Chain

{table(all_rows["proof_chain"], ["proof_id", "step", "current_status", "blocking_gap", "theorem_zero_claimed"])}

## Zero-Odd-Source Clause Audit

{table(all_rows["clause_audit"], ["clause_id", "clause", "current_status", "if_open", "residual_symbol"])}

## epsilon_Qv_extra Bound Rows

{table(all_rows["epsilon"], ["epsilon_id", "symbol", "definition", "bound_interface", "current_status", "current_value"])}

## Promotion Gates

{table(all_rows["gates"], ["gate_id", "gate", "condition_passed", "status", "promotion_allowed_now"])}

## Decision Ledger

{table(all_rows["decision"], ["decision_id", "decision", "because", "next_action"])}

## Next Target

{table(all_rows["next"], ["next_id", "priority", "next_doc", "next_script", "objective", "exclude"])}

## Validation

{table(all_rows["validation"], ["validation_id", "passed", "check", "required"])}

Validation overall: `{all_rows["validation"][-1]["passed"]}`.
""",
        encoding="utf-8",
    )


def main() -> None:
    all_rows: dict[str, list[dict[str, Any]]] = {
        "sources": source_rows(),
        "proof_chain": proof_chain_rows(),
        "clause_audit": clause_audit_rows(),
        "epsilon": epsilon_rows(),
        "gates": gate_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
    }
    for key, path in OUTPUTS.items():
        if key in {"branches", "validation"}:
            continue
        write_csv(path, all_rows[key])
    shutil.copyfile(OUTPUTS["proof_chain"], BRANCH_OUTPUTS["proof_copy"])
    shutil.copyfile(OUTPUTS["epsilon"], BRANCH_OUTPUTS["epsilon_copy"])
    shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])
    all_rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], all_rows["branches"])
    all_rows["validation"] = validation(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)
    all_rows["validation"] = validation(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)
    print(f"2992 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from action_scale_constant_gate import (  # noqa: E402
    evaluate_action_mode_rows,
    evaluate_action_owner_rows,
    evaluate_k_action_scale_rows,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4433"
CLAIM_ID = "L-274"
MARKER = "PPC4161_ACTION_SCALE_CONSTANT_SECTOR_UNIVERSALITY_OR_KMACTIONSCALE_FIRST_VALUE_4433"
PACKET_MARKER = "PPC4161_PACKET_ACTION_SCALE_CONSTANT_SECTOR_UNIVERSALITY_OR_KMACTIONSCALE_FIRST_VALUE_4433"
DECISION = "ACTION_SCALE_COMMON_MODE_CALIBRATION_ONLY_RELATIVE_MODE_REQUIRES_PARENT_HBAR_MEASURE_AND_CONNECTED_MATTER"
NEXT_TARGET = "4434-Y5-R2FR-parent-hbar-measure-owner-and-connected-matter-certificate-or-Kmactionscale-value.md"

FORMAL_PATH = FORMAL / "449-PPC4161-action-scale-constant-sector-universality-or-Kmactionscale-first-value.md"
DOC_PATH = POST / "4433-Y5-R2FR-action-scale-constant-sector-universality-or-Kmactionscale-first-value.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4433_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4433_SOURCE_REGISTER.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4433_DERIVATION_ROWS.csv"
OWNER_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4433_ACTION_SCALE_OWNER_INPUT.csv"
OWNER_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4433_ACTION_SCALE_OWNER_OUTPUT.csv"
MODE_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4433_ACTION_SCALE_MODE_SPLIT_INPUT.csv"
MODE_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4433_ACTION_SCALE_MODE_SPLIT_OUTPUT.csv"
K_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4433_K_ACTION_SCALE_INPUT.csv"
K_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4433_K_ACTION_SCALE_OUTPUT.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4433_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4433_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4433_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4433_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "action_scale_constant_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4433_action_scale_constant_sector_universality_or_Kmactionscale_first_value.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4432 = SOURCE_DIR / "P8_Y5_R2FR_4432_NEXT_TARGET.csv"
FORMAL_448 = FORMAL / "448-PPC4161-source-shadow-constructor-noHom-proof-or-KmshadowCshadow-first-value.md"
KMSHADOW4432 = SOURCE_DIR / "P8_Y5_R2FR_4432_KMSHADOW_VALUE_OUTPUT.csv"
HMO4422 = SOURCE_DIR / "P8_Y5_R2FR_4422_HBAR_MEASURE_OWNER_OUTPUT.csv"
ASO1888 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1888_ACTION_SCALE_OWNER_PROOF_ATTEMPT.csv"
NCR1815 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1815_NO_CURRENT_RESCALE_THEOREM.csv"
NSP1765 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1765_NO_SOURCE_PREFACTOR_PROOF_ATTEMPT.csv"
CMC1905 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1905_CONNECTED_MATTER_CATEGORY_ATTEMPT.csv"
CONSTANT_CONTRACT = SOURCE_DIR / "P8_constant_sector_universality_CONTRACT.csv"
CSU1927 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1927_CONSTANT_SECTOR_UNIVERSALITY_AUDIT.csv"
SOURCE_CHARGE = SOURCE_DIR / "P8_species_source_charge_residual_or_zero.csv"
SOURCE_WEIGHTS = SOURCE_DIR / "P8_Y5_NO_SHADOW_2508_SOURCE_WEIGHT_RESIDUAL_ROWS.csv"
COUNTERMODELS = SOURCE_DIR / "P8_Y5_NO_SHADOW_2508_SOURCE_ONLY_COUNTERMODELS.csv"
MTS_DD_STATUS = SOURCE_DIR / "P8_Y5_MTS_to_DD_source_map_status.csv"

DELTA_Q_MHAT = 3.330000e-03
ETA_BOUND = 2.8e-15
D_MHAT_ONE_CHANNEL_CEILING = ETA_BOUND / DELTA_Q_MHAT


def text(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ""


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for index, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return index
    return 0


def rows_from(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def md(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def table(rows: Sequence[Mapping[str, object]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(md(row.get(header, "")) for header in headers) + " |")
    return "\n".join(output)


def source_specs() -> List[Dict[str, object]]:
    return [
        {"source_id": "SRC4433_00_4432_next", "path": NEXT_4432, "needle": "action-scale/constant-sector", "role": "4432 handoff."},
        {"source_id": "SRC4433_01_448_formal", "path": FORMAL_448, "needle": "SPLIT4432_1_surviving_shadow_reassignment", "role": "source-shadow survivor reassigned to action scale."},
        {"source_id": "SRC4433_02_kmshadow4432", "path": KMSHADOW4432, "needle": "KM4432_1_action_scale_reassignment", "role": "action-scale product target."},
        {"source_id": "SRC4433_03_hmo4422", "path": HMO4422, "needle": "HMO4422_3_future_universal_hbar_measure_contract", "role": "future universal hbar/measure contract."},
        {"source_id": "SRC4433_04_aso1888", "path": ASO1888, "needle": "ASO1888_7_verdict", "role": "action-scale owner proof attempt."},
        {"source_id": "SRC4433_05_ncr1815", "path": NCR1815, "needle": "NCR1815_3_connected_naturality", "role": "connected naturality collapse."},
        {"source_id": "SRC4433_06_nsp1765", "path": NSP1765, "needle": "NSP1765_3_common_prefactor", "role": "common prefactor absorption."},
        {"source_id": "SRC4433_07_cmc1905", "path": CMC1905, "needle": "CMC1905_1_naturality", "role": "connected matter naturality."},
        {"source_id": "SRC4433_08_constant_contract", "path": CONSTANT_CONTRACT, "needle": "C1_superselection_independence", "role": "constant-sector universality contract."},
        {"source_id": "SRC4433_09_csu1927", "path": CSU1927, "needle": "CSU1927_6_verdict", "role": "constant-sector universality verdict."},
        {"source_id": "SRC4433_10_source_charge", "path": SOURCE_CHARGE, "needle": "SSC2675_3_no_bound_inversion_guard", "role": "no bound inversion guard."},
        {"source_id": "SRC4433_11_source_weights", "path": SOURCE_WEIGHTS, "needle": "RSW2508_3", "role": "action-scale residual row."},
        {"source_id": "SRC4433_12_countermodels", "path": COUNTERMODELS, "needle": "CM2508_5_action_scale", "role": "action-scale countermodel."},
        {"source_id": "SRC4433_13_mts_dd_status", "path": MTS_DD_STATUS, "needle": "STAT3544_0_map", "role": "MTS-to-DD status."},
        {"source_id": "SRC4433_14_gate", "path": GATE_PATH, "needle": "def evaluate_action_owner_row", "role": "4433 gate script."},
        {"source_id": "SRC4433_15_generator", "path": GENERATOR_PATH, "needle": "CHECKPOINT = \"4433\"", "role": "4433 generator script."},
    ]


def source_rows() -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for spec in source_specs():
        path = Path(spec["path"])
        needle = str(spec["needle"])
        content = text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": spec["source_id"],
                "path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": needle in content,
                "line_number": line_of(path, needle),
                "role": spec["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def derivation_rows() -> List[Dict[str, object]]:
    return [
        {
            "derivation_id": "ASU4433_0_connected_naturality_common_mode_theorem",
            "claim": "Connected ordinary-matter action weights collapse to one common mode.",
            "derivation": "Let w_A be a natural positive automorphism of the ordinary matter action-density/source functor. For every parent-owned nonzero morphism f:A->B, naturality gives w_B F(f)=F(f)w_A, so w_A=w_B. If the ordinary matter action-density category is connected, w_A=w_* for all ordinary sectors.",
            "consequence": "Relative action-scale WEP/source weights disappear once parent-owned connectedness and action-density functor ownership are signed.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "ASU4433_1_common_mode_calibration_theorem",
            "claim": "A derivative-silent common action-scale mode is calibration, not a local residual.",
            "derivation": "If S_matter -> w_* S_matter with w_* common to all ordinary sectors and d w_*=0 in the local arena, then T_total -> w_* T_total. The field equation can absorb this into kappa_eff or measured G. This does not predict G, but it produces no composition-dependent WEP/PPN/R10 residual.",
            "consequence": "The remaining physical action-scale debt is relative, marker-dependent, time/range-dependent, or hidden-sector leakage.",
            "status": "DERIVED_COMMON_MODE_ONLY",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "ASU4433_2_hbar_measure_owner_requirement",
            "claim": "The common-mode theorem is not enough without hbar/measure ownership.",
            "derivation": "Species-dependent hbar_A, path-integral weights, measure Jacobians or action-density normalizations are physical unless the parent action supplies one phase line, one hbar_parent and one species-blind measure. Classical equations alone cannot erase them because the Hilbert source and quantum/statistical measure still change.",
            "consequence": "The owner proof must sign hbar/measure/Jacobian ownership, not just matter EOM shape.",
            "status": "OWNER_REQUIREMENT_SHARPENED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "ASU4433_3_constant_sector_requirement",
            "claim": "Constant-sector universality is the other half of action-scale silence.",
            "derivation": "Even if action weights collapse, hidden dependence of alpha, masses, binding fractions, clock standards or kappa_eff on MTS selectors/invariants can reintroduce WEP, clock or fifth-force channels. The local theorem needs theta_A as fixed representation/superselection data or theta_A=theta_bar_A(q(Phi)) with vertical derivative zero.",
            "consequence": "Constant-sector universality is not optional bookkeeping; it is the route that prevents action-scale leakage from returning as particle/clock/source constants.",
            "status": "CONSTANT_SECTOR_REQUIRED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "KAS4433_0_first_action_scale_product_contract",
            "claim": "No parent-owned numeric K_m_action_scale*C_action_scale value exists yet.",
            "derivation": f"The finite branch keeps a nonclaim Ti/Pt target: abs(K_m_action_scale*C_action_scale)<={D_MHAT_ONE_CHANNEL_CEILING:.12e} in the one-channel D_mhat limit, or {DELTA_Q_MHAT:.5f}*abs(K_m_action_scale*C_action_scale)<={ETA_BOUND:.12e} inside the no-cancellation envelope. This is a bound target, not a fitted coefficient.",
            "consequence": "The next checkpoint should either sign the owner/connectedness route or fill a sourced action-scale coefficient row.",
            "status": "FINITE_VALUE_NOT_FOUND_BOUND_TARGET_ONLY",
            "valid_for_claim": False,
        },
    ]


def owner_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "ASO4433_0_exact_action_scale_owner_contract",
            "clause": "single action-scale/hbar/measure/current owner",
            "one_parent_action_object": True,
            "universal_hbar_parent": True,
            "common_measure_jacobian": True,
            "species_blind_action_density": True,
            "hilbert_current_owner": True,
            "ordinary_matter_connected": True,
            "variation_before_readout": True,
            "common_mode_calibrated": True,
            "source_path": str(HMO4422),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Exact future owner contract; nonclaim until parent action signs every clause.",
        },
        {
            "row_id": "ASO4433_1_current_hbar_measure_gap",
            "clause": "current phase seed with hbar/measure open",
            "one_parent_action_object": True,
            "universal_hbar_parent": False,
            "common_measure_jacobian": False,
            "species_blind_action_density": False,
            "hilbert_current_owner": True,
            "ordinary_matter_connected": False,
            "variation_before_readout": False,
            "common_mode_calibrated": True,
            "source_path": str(HMO4422),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Single phase line helps, but hbar/measure/Jacobian ownership remains open.",
        },
        {
            "row_id": "ASO4433_2_connected_naturality_route",
            "clause": "connected ordinary matter naturality collapse",
            "one_parent_action_object": True,
            "universal_hbar_parent": False,
            "common_measure_jacobian": False,
            "species_blind_action_density": True,
            "hilbert_current_owner": True,
            "ordinary_matter_connected": True,
            "variation_before_readout": True,
            "common_mode_calibrated": True,
            "source_path": str(CMC1905),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Naturality collapse is exact conditionally; parent-owned graph edges and hbar/measure are unsigned.",
        },
        {
            "row_id": "ASO4433_3_weighted_action_countermodel",
            "clause": "weighted pre-action countermodel",
            "one_parent_action_object": False,
            "universal_hbar_parent": False,
            "common_measure_jacobian": False,
            "species_blind_action_density": False,
            "hilbert_current_owner": True,
            "ordinary_matter_connected": False,
            "variation_before_readout": False,
            "common_mode_calibrated": False,
            "source_path": str(ASO1888),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "w_A S_A survives unless the parent object language has no action-scale slot.",
        },
        {
            "row_id": "ASO4433_4_constant_sector_countermodel",
            "clause": "constant-sector hidden dependence",
            "one_parent_action_object": True,
            "universal_hbar_parent": False,
            "common_measure_jacobian": False,
            "species_blind_action_density": False,
            "hilbert_current_owner": True,
            "ordinary_matter_connected": True,
            "variation_before_readout": True,
            "common_mode_calibrated": False,
            "source_path": str(CSU1927),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Hidden-dependent constants can reintroduce clock/WEP/source channels.",
        },
    ]


def mode_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "ASM4433_0_common_derivative_silent_mode",
            "mode": "w_common",
            "definition": "S_matter -> w_* S_matter with same w_* for all ordinary sectors and d w_*=0",
            "all_species_same": True,
            "derivative_silent": True,
            "relative_component_zero": True,
            "absorbed_in_G_calibration": True,
            "observable_residual": False,
            "source_path": str(NSP1765),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Common derivative-silent prefactor is calibration only, not a WEP/local residual.",
        },
        {
            "row_id": "ASM4433_1_relative_species_action_weight",
            "mode": "delta_w_A",
            "definition": "species/block-dependent action weight before variation",
            "all_species_same": False,
            "derivative_silent": True,
            "relative_component_zero": False,
            "absorbed_in_G_calibration": False,
            "observable_residual": True,
            "source_path": str(SOURCE_WEIGHTS),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Physical composition residual unless connected/natural owner theorem collapses it.",
        },
        {
            "row_id": "ASM4433_2_marker_dependent_common_scale",
            "mode": "w_common(Z)",
            "definition": "common-looking action scale that varies with time, range, marker, memory or domain",
            "all_species_same": True,
            "derivative_silent": False,
            "relative_component_zero": True,
            "absorbed_in_G_calibration": False,
            "observable_residual": True,
            "source_path": str(CONSTANT_CONTRACT),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Not a WEP composition split, but still a Gdot/range/fifth-force residual.",
        },
        {
            "row_id": "ASM4433_3_connected_naturality_common_mode",
            "mode": "w_connected",
            "definition": "relative weights collapsed to w_* by parent-owned connected ordinary matter category",
            "all_species_same": True,
            "derivative_silent": True,
            "relative_component_zero": True,
            "absorbed_in_G_calibration": True,
            "observable_residual": False,
            "source_path": str(CMC1905),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Exact conditional theorem; parent edge certificate is unsigned.",
        },
    ]


def k_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "KAS4433_0_common_mode_calibration_projection",
            "product": "K_m_action_scale*C_action_scale_common",
            "subcomponent": "C_action_scale_common",
            "value": "COMMON_CALIBRATION_ONLY",
            "units": "dimensionless",
            "parent_source": "NSP1765_common_prefactor_absorption",
            "source_leg": "not_applicable_common_G_calibration",
            "projection": "common derivative-silent action scale is absorbed into measured G and does not enter Ti/Pt differential channel",
            "bound_value": f"{D_MHAT_ONE_CHANNEL_CEILING:.12e}",
            "no_bound_inversion_guard": True,
            "source_path": str(NSP1765),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Calibration theorem is nonclaim because parent owner/connectedness remain unsigned.",
        },
        {
            "row_id": "KAS4433_1_relative_action_scale_contract",
            "product": "K_m_action_scale*C_action_scale_relative",
            "subcomponent": "delta_w_A",
            "value": "MISSING_PARENT_COEFFICIENT",
            "units": "dimensionless",
            "parent_source": "MISSING_ACTION_SCALE_PARENT_SOURCE",
            "source_leg": "MISSING_ACTION_SCALE_SOURCE_LEG",
            "projection": f"{DELTA_Q_MHAT:.5f}*abs(K_m_action_scale*C_action_scale_relative) <= {ETA_BOUND:.12e}",
            "bound_value": f"{D_MHAT_ONE_CHANNEL_CEILING:.12e}",
            "no_bound_inversion_guard": True,
            "source_path": str(SOURCE_WEIGHTS),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "First finite action-scale product if theorem route stays unsigned.",
        },
        {
            "row_id": "KAS4433_2_constant_sector_contract",
            "product": "K_m_constant*C_constant_sector",
            "subcomponent": "constant_sector_hidden_dependence",
            "value": "MISSING_PARENT_COEFFICIENT",
            "units": "dimensionless",
            "parent_source": "MISSING_CONSTANT_SECTOR_PARENT_SOURCE",
            "source_leg": "MISSING_CONSTANT_SECTOR_SOURCE_LEG",
            "projection": f"{DELTA_Q_MHAT:.5f}*abs(K_m_constant*C_constant_sector) <= {ETA_BOUND:.12e}",
            "bound_value": f"{D_MHAT_ONE_CHANNEL_CEILING:.12e}",
            "no_bound_inversion_guard": True,
            "source_path": str(CONSTANT_CONTRACT),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Constant-sector fallback if hidden dependence survives.",
        },
        {
            "row_id": "KAS4433_3_action_scale_bound_target",
            "product": "K_m_action_scale*C_action_scale_effective",
            "subcomponent": "effective_action_scale",
            "value": f"BOUND_ONLY_{D_MHAT_ONE_CHANNEL_CEILING:.12e}",
            "units": "dimensionless",
            "parent_source": "MISSING_PARENT_SOURCE",
            "source_leg": "MISSING_SOURCE_LEG",
            "projection": f"abs(K_m_action_scale*C_action_scale_effective) <= {D_MHAT_ONE_CHANNEL_CEILING:.12e} only as one-channel target",
            "bound_value": f"{D_MHAT_ONE_CHANNEL_CEILING:.12e}",
            "no_bound_inversion_guard": True,
            "source_path": str(KMSHADOW4432),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Bound target only; empirical bound cannot define parent coefficient.",
        },
    ]


def claim_gate_rows(owner: Sequence[Mapping[str, str]], modes: Sequence[Mapping[str, str]], kproducts: Sequence[Mapping[str, str]]) -> List[Dict[str, object]]:
    owner_rows = {row["row_id"]: row for row in owner}
    mode_rows = {row["row_id"]: row for row in modes}
    k_rows = {row["row_id"]: row for row in kproducts}
    no_claims = not any(row.get("valid_for_claim") == "True" for row in owner) and not any(row.get("valid_for_claim") == "True" for row in modes) and not any(row.get("valid_for_claim") == "True" for row in kproducts)
    return [
        {"gate_id": "CG4433_0_owner_contract", "claim": "single action-scale/hbar/measure owner contract staged", "passed": owner_rows["ASO4433_0_exact_action_scale_owner_contract"].get("current_status") == "ACTION_SCALE_OWNER_CONTRACT_READY_NONCLAIM", "valid_for_claim": False, "detail": "Exact but parent unsigned."},
        {"gate_id": "CG4433_1_hbar_measure_gap", "claim": "current phase seed leaves hbar/measure gap open", "passed": owner_rows["ASO4433_1_current_hbar_measure_gap"].get("current_status") == "ACTION_SCALE_OWNER_CURRENT_GAP_HBAR_MEASURE_OPEN", "valid_for_claim": False, "detail": "Do not promote phase seed to full action-scale owner."},
        {"gate_id": "CG4433_2_connected_route", "claim": "connected naturality reduces to common mode plus hbar/measure gap", "passed": owner_rows["ASO4433_2_connected_naturality_route"].get("current_status") == "ACTION_SCALE_OWNER_REDUCES_TO_COMMON_MODE_PLUS_HBAR_MEASURE_GAP", "valid_for_claim": False, "detail": "Naturality theorem is useful but parent graph/measure ownership unsigned."},
        {"gate_id": "CG4433_3_countermodel_retained", "claim": "weighted action countermodel remains live", "passed": owner_rows["ASO4433_3_weighted_action_countermodel"].get("current_status") == "ACTION_SCALE_OWNER_COUNTERMODEL_SURVIVES", "valid_for_claim": False, "detail": "w_A S_A cannot be erased by classical EOM."},
        {"gate_id": "CG4433_4_common_mode_calibration", "claim": "derivative-silent common mode is calibration only", "passed": mode_rows["ASM4433_0_common_derivative_silent_mode"].get("current_status") == "ACTION_SCALE_COMMON_MODE_CALIBRATION_ONLY_NONCLAIM", "valid_for_claim": False, "detail": "No WEP/PPN/R10 differential residual from common mode."},
        {"gate_id": "CG4433_5_relative_mode_retained", "claim": "relative action-scale mode remains finite", "passed": mode_rows["ASM4433_1_relative_species_action_weight"].get("current_status") == "ACTION_SCALE_RELATIVE_MODE_RETAINED", "valid_for_claim": False, "detail": "This is the first action-scale coefficient target."},
        {"gate_id": "CG4433_6_marker_common_scale_retained", "claim": "marker-dependent common scale remains a non-WEP residual", "passed": mode_rows["ASM4433_2_marker_dependent_common_scale"].get("current_status") == "ACTION_SCALE_MODE_DERIVATIVE_OPEN", "valid_for_claim": False, "detail": "Can become Gdot/range/fifth-force residual."},
        {"gate_id": "CG4433_7_K_common_nonclaim", "claim": "common-mode K row is calibration-only nonclaim", "passed": k_rows["KAS4433_0_common_mode_calibration_projection"].get("current_status") == "K_ACTION_SCALE_PRODUCT_INPUT_INVALID_NONCLAIM", "valid_for_claim": False, "detail": "Parent owner still unsigned."},
        {"gate_id": "CG4433_8_K_bound_only", "claim": "effective action-scale product remains bound target only", "passed": k_rows["KAS4433_3_action_scale_bound_target"].get("current_status") == "K_ACTION_SCALE_PRODUCT_BOUND_TARGET_ONLY", "valid_for_claim": False, "detail": "No bound inversion."},
        {"gate_id": "CG4433_9_no_claim_outputs", "claim": "4433 emits no local-GR/WEP/PPN/R10 claim", "passed": no_claims, "valid_for_claim": False, "detail": "All rows remain private nonclaim rows."},
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4433_0",
            "decision": DECISION,
            "summary": "4433 separates harmless calibration from physical coupling debt. If ordinary matter action weights are connected/natural, relative weights collapse to a derivative-silent common mode; that common mode is absorbed into measured G/kappa and is not a WEP/PPN/R10 residual. The dangerous pieces are relative action-scale weights, species hbar/measure/Jacobian factors, marker-dependent common scales, and hidden constant-sector dependence. No parent-owned numeric K_m_action_scale*C_action_scale value exists yet.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "public_claim": False,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {"status_id": "STAT4433_0_common", "status": "COMMON_ACTION_SCALE_MODE_CALIBRATION_ONLY", "detail": "Derivative-silent common action-scale prefactor can be absorbed into measured G and is not a differential local residual.", "valid_for_claim": False},
        {"status_id": "STAT4433_1_relative", "status": "RELATIVE_ACTION_SCALE_MODE_RETAINED", "detail": "Relative w_A/action-measure/hbar/Jacobian modes remain finite until parent hbar/measure owner and connected matter certificate close.", "valid_for_claim": False},
        {"status_id": "STAT4433_2_constant", "status": "CONSTANT_SECTOR_UNIVERSALITY_UNSIGNED", "detail": "Hidden MTS dependence of alpha/masses/binding/clock/kappa remains a separate source-coupling route.", "valid_for_claim": False},
        {"status_id": "STAT4433_3_k", "status": "NO_PARENT_NUMERIC_K_ACTION_SCALE_VALUE_FOUND", "detail": f"Only effective one-channel target exists: abs(K_m_action_scale*C_action_scale) <= {D_MHAT_ONE_CHANNEL_CEILING:.12e}.", "valid_for_claim": False},
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4433_0",
            "target": NEXT_TARGET,
            "objective": "Either sign parent hbar/measure ownership plus connected ordinary matter action-density certificate, or fill K_m_action_scale*C_action_scale with a sourced parent coefficient.",
            "derive_first": "derive one hbar_parent/path-measure/Jacobian owner and parent-owned ordinary matter graph edges so naturality collapses relative action weights to common calibration.",
            "fallback": "fill K_m_action_scale*C_action_scale_relative with numeric value, units, parent source, source leg, Ti/Pt projection, and no-bound-inversion guard.",
            "avoid": "using classical EOM scaling to erase Hilbert-source weights; treating common G calibration as a G prediction; using empirical bounds to define parent coefficients.",
            "valid_for_claim": False,
        }
    ]


def build_doc(sources: Sequence[Mapping[str, object]], owner: Sequence[Mapping[str, str]], modes: Sequence[Mapping[str, str]], kproducts: Sequence[Mapping[str, str]], gates: Sequence[Mapping[str, object]]) -> str:
    return f"""# 449 PPC4161 action-scale constant-sector universality or Kmactionscale first value

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4433 sharpens the weighted-action survivor:

- Connected/natural ordinary-matter action weights collapse to one common mode if parent-owned action-density graph edges exist.
- A derivative-silent common action-scale mode is only calibration: it rescales `T_total` and can be absorbed into measured `G/kappa`; it is not a WEP/PPN/R10 differential residual and does not predict `G`.
- The live physics is the relative part: `delta_w_A`, species hbar/measure/Jacobian factors, marker-dependent common scales, and hidden constant-sector dependence.
- Current MTS has useful conditional theorems and a single-phase seed, but not parent-signed hbar/measure ownership, species-blind Jacobian descent, parent-owned connected graph edges, or constant-sector universality.
- No numeric parent-owned `K_m_action_scale*C_action_scale` value exists; the Ti/Pt one-channel target remains `abs(K_m_action_scale*C_action_scale) <= {D_MHAT_ONE_CHANNEL_CEILING:.12e}`.

## Source Register

{table(sources)}

## Derivation Rows

{table(derivation_rows())}

## Action-Scale Owner Gate

{table(owner)}

## Action-Scale Mode Split Gate

{table(modes)}

## K Action-Scale Gate

{table(kproducts)}

## Claim Gates

{table(gates)}

## Decision

{table(decision_rows())}

## Next Target

{table(next_rows())}
"""


def post_doc() -> str:
    return f"""# 4433 - action-scale constant-sector universality or Kmactionscale first value

Marker: `{MARKER}`

Private checkpoint generated at `{STAMP}`.

## What changed

- Split action-scale leakage into harmless common calibration and dangerous relative/marker-dependent modes.
- Derived the conditional connected-naturality theorem: connected ordinary matter weights collapse to `w_*`.
- Kept hbar/measure/Jacobian and constant-sector universality unsigned.
- Kept `K_m_action_scale*C_action_scale` as a bound-only acquisition target, not a theory value.

## Decision

{table(decision_rows())}

## Next target

{table(next_rows())}
"""


def upsert_marked_section(path: Path, marker: str, section: str) -> None:
    existing = text(path)
    start = f"<!-- {marker}:START -->"
    end = f"<!-- {marker}:END -->"
    block = f"{start}\n{section.rstrip()}\n{end}\n"
    if start in existing and end in existing:
        before = existing.split(start)[0]
        after = existing.split(end, 1)[1].lstrip("\n")
        write_text(path, before + block + after)
    else:
        separator = "" if existing.endswith("\n") or not existing else "\n"
        write_text(path, existing + separator + block)


def update_claims_register() -> None:
    rows = rows_from(CLAIMS_PATH) if CLAIMS_PATH.exists() else []
    fieldnames = list(rows[0].keys()) if rows else ["claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk", "sector", "evidence", "next_action", "risk"]
    rows = [row for row in rows if row.get("claim_id") != CLAIM_ID]
    new_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": "4433 proves the useful conditional split for action-scale leakage: connected/natural ordinary matter weights collapse to a derivative-silent common mode, and that common mode is calibration only. Relative action-scale weights, species hbar/measure/Jacobian factors, marker-dependent common scales and constant-sector hidden dependence remain finite nonclaim routes until parent hbar/measure ownership and connected matter certification close.",
        "current_evidence": "4433 source register, derivation rows, action-scale owner output, action-scale mode split output, K action-scale output, claim gates, decision, status, next target and validation CSV.",
        "status": "action_scale_common_mode_calibration_only_relative_mode_requires_parent_hbar_measure_and_connected_matter",
        "next_test": "Sign parent hbar/measure ownership plus connected ordinary matter action-density certificate, or fill K_m_action_scale*C_action_scale with sourced parent provenance.",
        "key_risk": "Using classical EOM scaling to erase Hilbert-source weights; treating common G calibration as a G prediction; using empirical bounds to define parent coefficients.",
        "sector": "local_gr",
        "evidence": "4433 source register, derivation rows, action-scale owner output, action-scale mode split output, K action-scale output, claim gates, decision, status, next target and validation CSV.",
        "next_action": "Sign parent hbar/measure ownership plus connected ordinary matter action-density certificate, or fill K_m_action_scale*C_action_scale with sourced parent provenance.",
        "risk": "Using classical EOM scaling to erase Hilbert-source weights; treating common G calibration as a G prediction; using empirical bounds to define parent coefficients.",
    }
    rows.append({name: new_row.get(name, "") for name in fieldnames})
    with CLAIMS_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_spine_and_packet() -> None:
    spine_section = f"""## 4433 local spine update: action-scale common mode split

4433 shows that the weighted-action survivor is not all equally dangerous. If ordinary matter action weights are connected/natural, relative weights collapse to one `w_*`; if `w_*` is derivative-silent, it is absorbed into measured `G/kappa` and produces no differential WEP/PPN/R10 residual. The live local-GR coupling debt is therefore relative action-scale/hbar/measure/Jacobian leakage, marker-dependent common scale drift, and constant-sector hidden dependence.
"""
    packet_section = f"""## 4433 packet update: common mode is calibration, relative mode is physics

`{PACKET_MARKER}`

Private packet result: do not chase a single `K_m_action_scale*C_action_scale` number yet. First try to sign parent hbar/measure ownership and parent-owned connected ordinary matter graph edges; if that fails, fill the relative action-scale product with real source provenance and keep the no-bound-inversion guard.
"""
    upsert_marked_section(SPINE_PATH, MARKER, spine_section)
    upsert_marked_section(PACKET_PATH, PACKET_MARKER, packet_section)


def validation_rows(paths: Mapping[str, Path]) -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    owner = {row["row_id"]: row for row in rows_from(OWNER_OUTPUT)}
    modes = {row["row_id"]: row for row in rows_from(MODE_OUTPUT)}
    kproducts = {row["row_id"]: row for row in rows_from(K_OUTPUT)}
    gates = rows_from(CLAIM_GATES)
    no_claims = not any(row.get("valid_for_claim") == "True" for row in owner.values()) and not any(row.get("valid_for_claim") == "True" for row in modes.values()) and not any(row.get("valid_for_claim") == "True" for row in kproducts.values())
    checks = [
        ("VAL4433_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source path exists"),
        ("VAL4433_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited source needle is present"),
        ("VAL4433_2_owner_contract", owner["ASO4433_0_exact_action_scale_owner_contract"].get("current_status") == "ACTION_SCALE_OWNER_CONTRACT_READY_NONCLAIM", "action-scale owner contract staged"),
        ("VAL4433_3_hbar_measure_gap", owner["ASO4433_1_current_hbar_measure_gap"].get("current_status") == "ACTION_SCALE_OWNER_CURRENT_GAP_HBAR_MEASURE_OPEN", "hbar/measure gap remains open"),
        ("VAL4433_4_connected_route", owner["ASO4433_2_connected_naturality_route"].get("current_status") == "ACTION_SCALE_OWNER_REDUCES_TO_COMMON_MODE_PLUS_HBAR_MEASURE_GAP", "connected route reduces to common mode plus hbar/measure gap"),
        ("VAL4433_5_countermodel", owner["ASO4433_3_weighted_action_countermodel"].get("current_status") == "ACTION_SCALE_OWNER_COUNTERMODEL_SURVIVES", "weighted-action countermodel retained"),
        ("VAL4433_6_common_mode", modes["ASM4433_0_common_derivative_silent_mode"].get("current_status") == "ACTION_SCALE_COMMON_MODE_CALIBRATION_ONLY_NONCLAIM", "common derivative-silent mode is calibration only"),
        ("VAL4433_7_relative_mode", modes["ASM4433_1_relative_species_action_weight"].get("current_status") == "ACTION_SCALE_RELATIVE_MODE_RETAINED", "relative action-scale mode retained"),
        ("VAL4433_8_marker_mode", modes["ASM4433_2_marker_dependent_common_scale"].get("current_status") == "ACTION_SCALE_MODE_DERIVATIVE_OPEN", "marker-dependent common scale retained"),
        ("VAL4433_9_k_common", kproducts["KAS4433_0_common_mode_calibration_projection"].get("current_status") == "K_ACTION_SCALE_PRODUCT_INPUT_INVALID_NONCLAIM", "common mode K row is nonclaim"),
        ("VAL4433_10_k_relative_contract", kproducts["KAS4433_1_relative_action_scale_contract"].get("current_status") == "K_ACTION_SCALE_PRODUCT_CONTRACT_ONLY", "relative K action-scale contract staged"),
        ("VAL4433_11_k_bound_target", kproducts["KAS4433_3_action_scale_bound_target"].get("current_status") == "K_ACTION_SCALE_PRODUCT_BOUND_TARGET_ONLY", "action-scale bound target retained"),
        ("VAL4433_12_no_claim_outputs", no_claims, "no output row is claim-ready"),
        ("VAL4433_13_claim_gate_no_claim", any(row["gate_id"] == "CG4433_9_no_claim_outputs" and row["passed"] == "True" for row in gates), "claim gate explicitly blocks public claim"),
        ("VAL4433_14_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-274"),
        ("VAL4433_15_formal_doc", paths["formal"].exists() and MARKER in text(paths["formal"]), "formal doc exists with marker"),
        ("VAL4433_16_post_doc", paths["post"].exists() and "Private checkpoint" in text(paths["post"]), "post checkpoint doc exists"),
        ("VAL4433_17_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4433_18_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4433_19_next_target", paths["next"].exists() and NEXT_TARGET in text(paths["next"]), "next target file exists"),
        ("VAL4433_20_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": bool(passed), "detail": detail} for check_id, passed, detail in checks]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(DERIVATION_ROWS, derivation_rows())
    write_csv(OWNER_INPUT, owner_input_rows())
    write_csv(OWNER_OUTPUT, evaluate_action_owner_rows(OWNER_INPUT))
    write_csv(MODE_INPUT, mode_input_rows())
    write_csv(MODE_OUTPUT, evaluate_action_mode_rows(MODE_INPUT))
    write_csv(K_INPUT, k_input_rows())
    write_csv(K_OUTPUT, evaluate_k_action_scale_rows(K_INPUT))
    owner = rows_from(OWNER_OUTPUT)
    modes = rows_from(MODE_OUTPUT)
    kproducts = rows_from(K_OUTPUT)
    gates = claim_gate_rows(owner, modes, kproducts)
    write_csv(CLAIM_GATES, gates)
    write_csv(DECISION_CSV, decision_rows())
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    write_text(FORMAL_PATH, build_doc(rows_from(SOURCE_REGISTER), owner, modes, kproducts, gates))
    write_text(DOC_PATH, post_doc())
    update_claims_register()
    write_spine_and_packet()
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    write_csv(VALIDATION_PATH, validation_rows({"formal": FORMAL_PATH, "post": DOC_PATH, "next": NEXT_CSV}))


if __name__ == "__main__":
    main()

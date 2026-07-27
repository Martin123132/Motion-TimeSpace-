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

from source_owner_cspecies_dd_gate import (  # noqa: E402
    evaluate_dd_map_rows,
    evaluate_envelope_rows,
    evaluate_signature_rows,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4430"
CLAIM_ID = "L-271"
MARKER = "PPC4161_TOTAL_HILBERT_SOURCE_OWNER_NO_SOURCE_WEIGHT_SIGNATURE_OR_TIPT_DD_MAP_4430"
PACKET_MARKER = "PPC4161_PACKET_TOTAL_HILBERT_SOURCE_OWNER_NO_SOURCE_WEIGHT_SIGNATURE_OR_TIPT_DD_MAP_4430"
DECISION = "TOTAL_HILBERT_SOURCE_ZERO_SIGNATURE_EXACT_BUT_PARENT_GRAMMAR_UNSIGNED_DD_MAP_SYMBOLIC_ENVELOPE_READY_VALUES_MISSING"
NEXT_TARGET = "4431-Y5-R2FR-source-shadow-ban-and-nonHilbert-bypass-zero-or-first-DD-K-value.md"

FORMAL_PATH = FORMAL / "446-PPC4161-total-Hilbert-source-owner-no-source-weight-signature-or-TiPt-DD-map.md"
DOC_PATH = POST / "4430-Y5-R2FR-total-Hilbert-source-owner-no-source-weight-signature-or-TiPt-DD-map.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4430_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4430_SOURCE_REGISTER.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4430_DERIVATION_ROWS.csv"
SIGNATURE_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4430_SOURCE_OWNER_SIGNATURE_INPUT.csv"
SIGNATURE_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4430_SOURCE_OWNER_SIGNATURE_OUTPUT.csv"
DD_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4430_DD_SOURCE_MAP_INPUT.csv"
DD_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4430_DD_SOURCE_MAP_OUTPUT.csv"
ENVELOPE_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4430_DD_ENVELOPE_INPUT.csv"
ENVELOPE_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4430_DD_ENVELOPE_OUTPUT.csv"
COEFFICIENT_QUEUE = SOURCE_DIR / "P8_Y5_R2FR_4430_FIRST_DD_K_VALUE_QUEUE.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4430_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4430_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4430_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4430_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "source_owner_cspecies_dd_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4430_total_Hilbert_source_owner_no_source_weight_signature_or_TiPt_DD_map.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4429 = SOURCE_DIR / "P8_Y5_R2FR_4429_NEXT_TARGET.csv"
FORMAL_445 = FORMAL / "445-PPC4161-hidden-rho-internal-shift-from-parent-constraint-or-Cspecies-zero-theorem.md"
DOC_4429 = POST / "4429-Y5-R2FR-hidden-rho-internal-shift-from-parent-constraint-or-Cspecies-zero-theorem.md"
CSV_4429_CSPECIES = SOURCE_DIR / "P8_Y5_R2FR_4429_CSPECIES_ZERO_OUTPUT.csv"
CSV_4429_RESIDUAL = SOURCE_DIR / "P8_Y5_R2FR_4429_CSPECIES_RESIDUAL_DECOMPOSITION.csv"
CSV_4429_BOUND = SOURCE_DIR / "P8_Y5_R2FR_4429_TIPT_BOUND_MAP_OUTPUT.csv"

CSV_THO1765 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1765_TOTAL_HILBERT_SOURCE_OWNER_AUDIT.csv"
CSV_NSP1765 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1765_NO_SOURCE_PREFACTOR_PROOF_ATTEMPT.csv"
CSV_SF2613 = SOURCE_DIR / "P8_Y5_HOM_EXCLUSION_GATE_2613_LABEL_FORGETTING_SOURCE_FUNCTOR_AUDIT.csv"
CSV_SLF1603 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1603_SOURCE_LABEL_FORGETTING_THEOREM_ATTEMPT.csv"
CSV_NO_SPECIES = SOURCE_DIR / "P8_no_species_source_charge_CONTRACT.csv"
CSV_SPECIES_RESIDUAL = SOURCE_DIR / "P8_species_source_charge_residual_or_zero.csv"
CSV_NSS3542 = SOURCE_DIR / "P8_Y5_R2FR_3542_NO_SOURCE_ONLY_SLOT_PROOF_ATTEMPT.csv"
CSV_INTAKE3542 = SOURCE_DIR / "P8_Y5_R2FR_3542_COEFFICIENT_INTAKE_ROWS.csv"

DOC_3543 = POST / "3543-Y5-R2FR-constructor-exhaustion-or-first-species-source-coefficient-fill.md"
CSV_MATERIAL2440 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2440_WEP_MATERIAL_SENSITIVITY_BASIS.csv"
CSV_PROJ2440 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2440_WEP_K_VECTOR_PROJECTION.csv"
CSV_BLOCK2440 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2440_WEP_SOURCE_LEG_BLOCKERS.csv"
CSV_MTS_DD_STATUS = SOURCE_DIR / "P8_Y5_MTS_to_DD_source_map_status.csv"
CSV_FIRST_DD_STATUS = SOURCE_DIR / "P8_Y5_first_DD_K_value_or_source_leg_status.csv"


DELTA_Q_MHAT = 3.330000e-03
DELTA_Q_E = 2.040000e-03
ETA_BOUND = 2.8e-15
D_MHAT_ONE_CHANNEL_CEILING = ETA_BOUND / DELTA_Q_MHAT
D_E_ONE_CHANNEL_CEILING = ETA_BOUND / DELTA_Q_E


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
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        out.append("| " + " | ".join(md(row.get(header, "")) for header in headers) + " |")
    return "\n".join(out)


def source_specs() -> List[Dict[str, object]]:
    return [
        {"source_id": "SRC4430_00_4429_next", "path": NEXT_4429, "needle": "total Hilbert source owner", "role": "4429 handoff."},
        {"source_id": "SRC4430_01_445_formal", "path": FORMAL_445, "needle": "CSP4429_0_species_zero_theorem", "role": "4429 calibrated source theorem."},
        {"source_id": "SRC4430_02_4429_doc", "path": DOC_4429, "needle": "C_species=DERIVED_ZERO", "role": "4429 post checkpoint."},
        {"source_id": "SRC4430_03_4429_cspecies", "path": CSV_4429_CSPECIES, "needle": "CSZ4429_2_exchange_collapse", "role": "previous C_species zero gate."},
        {"source_id": "SRC4430_04_4429_residual", "path": CSV_4429_RESIDUAL, "needle": "C_nonHilbert", "role": "C_species residual vector."},
        {"source_id": "SRC4430_05_4429_bound", "path": CSV_4429_BOUND, "needle": "TBM4429_0_real_TiPt_interface", "role": "previous Ti/Pt bound interface."},
        {"source_id": "SRC4430_06_tho1765", "path": CSV_THO1765, "needle": "THO1765_4_owner_verdict", "role": "total Hilbert source owner audit."},
        {"source_id": "SRC4430_07_nsp1765", "path": CSV_NSP1765, "needle": "NSP1765_4_current_verdict", "role": "no-source-prefactor and exchange filter."},
        {"source_id": "SRC4430_08_sf2613", "path": CSV_SF2613, "needle": "SF2613_4_verdict", "role": "source functor label forgetting."},
        {"source_id": "SRC4430_09_slf1603", "path": CSV_SLF1603, "needle": "SLF1603_5_verdict", "role": "source label forgetting theorem attempt."},
        {"source_id": "SRC4430_10_no_species", "path": CSV_NO_SPECIES, "needle": "S4_source_normalization_species_blind", "role": "no species source charge contract."},
        {"source_id": "SRC4430_11_species_residual", "path": CSV_SPECIES_RESIDUAL, "needle": "SSC2675_0_definition", "role": "species source residual row."},
        {"source_id": "SRC4430_12_nss3542", "path": CSV_NSS3542, "needle": "NSS3542_6_verdict", "role": "no source-only slot proof attempt."},
        {"source_id": "SRC4430_13_intake3542", "path": CSV_INTAKE3542, "needle": "INT3542_0_species_source", "role": "coefficient intake row."},
        {"source_id": "SRC4430_14_doc3543", "path": DOC_3543, "needle": "SSF3543_0_DD_two_charge_constraint", "role": "first real Ti/Pt DD inequality."},
        {"source_id": "SRC4430_15_material2440", "path": CSV_MATERIAL2440, "needle": "WMS2440_2_Pt_minus_Ti", "role": "source-backed DD material contrast."},
        {"source_id": "SRC4430_16_proj2440", "path": CSV_PROJ2440, "needle": "WKP2440_1_MTS_expanded_formula", "role": "existing expanded MTS-to-DD formula shape."},
        {"source_id": "SRC4430_17_block2440", "path": CSV_BLOCK2440, "needle": "WB2440_0_MTS_to_DD_map", "role": "source-leg blockers."},
        {"source_id": "SRC4430_18_mts_dd_status", "path": CSV_MTS_DD_STATUS, "needle": "STAT3544_0_map", "role": "MTS-to-DD status."},
        {"source_id": "SRC4430_19_first_dd_status", "path": CSV_FIRST_DD_STATUS, "needle": "STATUS3545_0", "role": "first DD K/source-leg status."},
        {"source_id": "SRC4430_20_gate", "path": GATE_PATH, "needle": "def evaluate_signature_row", "role": "4430 gate script."},
        {"source_id": "SRC4430_21_generator", "path": GENERATOR_PATH, "needle": "CHECKPOINT = \"4430\"", "role": "4430 generator."},
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
                "needle_found": True if not needle else needle in content,
                "line_number": line_of(path, needle),
                "role": spec["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def derivation_rows() -> List[Dict[str, object]]:
    return [
        {
            "derivation_id": "THS4430_0_zero_signature",
            "claim": "Total-Hilbert source ownership plus no source-weight constructors implies C_species=DERIVED_ZERO.",
            "derivation": "If ordinary active source is only T_total=delta S_matter/delta e_obs, SourceFunctor has domain T_total rather than labelled pairs, Hom_parent(SpeciesLabel,Coeff_active_source)=empty, no source-shadow S_source=sum_A w_A S_A exists, hidden/readout/material markers cannot enter active source coefficients, non-Hilbert bypass J_NH vanishes, and common calibration is quotiented out, then no relative species coefficient can be written. Therefore C_species=0.",
            "consequence": "This is the cleanest calibrated-source zero theorem currently available.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "THS4430_1_exchange_filter",
            "claim": "Bianchi/Ward exchange collapses many source weights even before the full no-Hom theorem closes.",
            "derivation": "For interacting matter sectors with exchange currents C_i^nu, separate source weights require sum_i w_i C_i^nu=0. On a connected exchange graph, this forces all w_i to one common calibration. Only disconnected block weights, source-shadow slots, non-Hilbert bypasses and marker/readout returns remain.",
            "consequence": "The finite residual vector is smaller and has named components.",
            "status": "PARTIAL_DERIVATION_REDUCES_RESIDUAL_SPACE",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "THS4430_2_current_gap",
            "claim": "Current MTS does not parent-sign the zero signature.",
            "derivation": "1765/2613/3542 show the Hilbert owner, source-domain and no-source-slot routes as exact contracts, but source-shadow exclusion, no-Hom constructor exhaustion, non-Hilbert silence, hidden/readout no-return and ordinary exchange connectivity are not all parent-signed.",
            "consequence": "C_species remains nonclaim and must carry a finite DD envelope.",
            "status": "PARENT_GRAMMAR_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "DD4430_0_symbolic_map",
            "claim": "The Ti/Pt finite branch now has a symbolic MTS-to-DD map and absolute envelope.",
            "derivation": "Use D_mhat_source=sum_j K_m_j C_j and D_e_source=sum_j K_e_j C_j for C_j in {C_block,C_shadow,C_nonHilbert,C_marker_readout}. The source-backed contrast gives |DeltaQ_mhat D_mhat + DeltaQ_e D_e| <= eta_bound. With no cancellation, |DeltaQ_mhat| sum_j |K_m_j C_j| + |DeltaQ_e| sum_j |K_e_j C_j| <= eta_bound.",
            "consequence": "The next empirical task is one real K value/source-leg, not another abstract coupling audit.",
            "status": "SYMBOLIC_MAP_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "DD4430_1_single_channel_ceilings",
            "claim": "The one-channel Ti/Pt ceilings are numeric nonclaim targets.",
            "derivation": f"If only D_mhat is active, |D_mhat| <= {D_MHAT_ONE_CHANNEL_CEILING:.12e}. If only D_e is active, |D_e| <= {D_E_ONE_CHANNEL_CEILING:.12e}. These are empirical ceilings, not theory predictions.",
            "consequence": "Future K*C products can be checked immediately once a parent coefficient exists.",
            "status": "NUMERIC_TARGETS_READY_NONCLAIM",
            "valid_for_claim": False,
        },
    ]


def signature_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "SIG4430_0_full_zero_signature",
            "signature_piece": "full total-Hilbert/no-source-weight zero signature",
            "one_total_matter_action": True,
            "total_hilbert_derivative": True,
            "source_domain_total_current": True,
            "no_source_shadow": True,
            "no_species_hom": True,
            "no_hidden_marker_return": True,
            "nonhilbert_bypass_zero": True,
            "exchange_connected_or_common": True,
            "common_calibration_removed": True,
            "source_path": str(FORMAL_445),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Pure theorem target; nonclaim until parent grammar signs all pieces.",
        },
        {
            "row_id": "SIG4430_1_current_total_Hilbert_owner",
            "signature_piece": "current total Hilbert owner audit",
            "one_total_matter_action": True,
            "total_hilbert_derivative": True,
            "source_domain_total_current": True,
            "no_source_shadow": False,
            "no_species_hom": False,
            "no_hidden_marker_return": False,
            "nonhilbert_bypass_zero": False,
            "exchange_connected_or_common": True,
            "common_calibration_removed": True,
            "source_path": str(CSV_THO1765),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Clean owner contract, but source-shadow and non-Hilbert bypass remain live.",
        },
        {
            "row_id": "SIG4430_2_no_source_weight_core",
            "signature_piece": "same-action plus exchange filter",
            "one_total_matter_action": True,
            "total_hilbert_derivative": True,
            "source_domain_total_current": True,
            "no_source_shadow": True,
            "no_species_hom": False,
            "no_hidden_marker_return": False,
            "nonhilbert_bypass_zero": False,
            "exchange_connected_or_common": True,
            "common_calibration_removed": True,
            "source_path": str(CSV_NSP1765),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Partial derivation: source-only shadow weights are pressured, connected exchange weights collapse.",
        },
        {
            "row_id": "SIG4430_3_source_domain_label_forgetting",
            "signature_piece": "source functor uses total current not labelled family",
            "one_total_matter_action": True,
            "total_hilbert_derivative": True,
            "source_domain_total_current": True,
            "no_source_shadow": False,
            "no_species_hom": False,
            "no_hidden_marker_return": False,
            "nonhilbert_bypass_zero": False,
            "exchange_connected_or_common": False,
            "common_calibration_removed": True,
            "source_path": str(CSV_SF2613),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Domain shape is exact, parent functor and hidden return are unsigned.",
        },
        {
            "row_id": "SIG4430_4_no_source_only_constructor",
            "signature_piece": "no-Hom/no constructor from species to source coefficient",
            "one_total_matter_action": True,
            "total_hilbert_derivative": True,
            "source_domain_total_current": True,
            "no_source_shadow": False,
            "no_species_hom": False,
            "no_hidden_marker_return": False,
            "nonhilbert_bypass_zero": False,
            "exchange_connected_or_common": True,
            "common_calibration_removed": True,
            "source_path": str(CSV_NSS3542),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "No-source-only theorem is exact if parent sorts/constructor exhaustion are signed; current countermodel survives.",
        },
    ]


def dd_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "DD4430_0_D_mhat_symbolic",
            "dd_quantity": "D_mhat_source",
            "map_formula": "D_mhat_source = K_m_block*C_block + K_m_shadow*C_shadow + K_m_nonHilbert*C_nonHilbert + K_m_marker*C_marker_readout",
            "material_delta_Q": "DeltaQ_mhat(Pt-Ti)=3.330000e-03",
            "coefficient_values_present": False,
            "source_leg_present": False,
            "alloy_policy_present": False,
            "sign_policy_present": False,
            "source_path": str(CSV_PROJ2440),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Symbolic source map into DD mhat channel; K values/source leg missing.",
        },
        {
            "row_id": "DD4430_1_D_e_symbolic",
            "dd_quantity": "D_e_source",
            "map_formula": "D_e_source = K_e_block*C_block + K_e_shadow*C_shadow + K_e_nonHilbert*C_nonHilbert + K_e_marker*C_marker_readout",
            "material_delta_Q": "DeltaQ_e(Pt-Ti)=2.040000e-03",
            "coefficient_values_present": False,
            "source_leg_present": False,
            "alloy_policy_present": False,
            "sign_policy_present": False,
            "source_path": str(CSV_PROJ2440),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Symbolic source map into DD electromagnetic binding channel; K values/source leg missing.",
        },
        {
            "row_id": "DD4430_2_future_zero_projection",
            "dd_quantity": "D_mhat_source,D_e_source",
            "map_formula": "if C_block=C_shadow=C_nonHilbert=C_marker_readout=0 then D_mhat_source=D_e_source=0",
            "material_delta_Q": "DeltaQ_mhat=3.330000e-03;DeltaQ_e=2.040000e-03",
            "coefficient_values_present": True,
            "source_leg_present": True,
            "alloy_policy_present": True,
            "sign_policy_present": True,
            "source_path": str(CSV_4429_RESIDUAL),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Future zero projection; input-invalid until C_species zero theorem is parent-signed.",
        },
    ]


def envelope_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "ENV4430_0_two_charge_constraint",
            "envelope": "abs(3.330000e-03*D_mhat_source + 2.040000e-03*D_e_source) <= 2.8e-15",
            "bound_value": f"{ETA_BOUND:.12e}",
            "units": "dimensionless",
            "source_path": str(DOC_3543),
            "numeric_bound_present": True,
            "theory_values_present": False,
            "no_cancellation_policy": False,
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Source-backed two-charge line; cancellation-safe only after sign/model policy.",
        },
        {
            "row_id": "ENV4430_1_no_cancellation_envelope",
            "envelope": "0.00333*sum_j abs(K_m_j*C_j) + 0.00204*sum_j abs(K_e_j*C_j) <= 2.8e-15",
            "bound_value": f"{ETA_BOUND:.12e}",
            "units": "dimensionless",
            "source_path": str(CSV_PROJ2440),
            "numeric_bound_present": True,
            "theory_values_present": False,
            "no_cancellation_policy": True,
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Absolute envelope for C_block,C_shadow,C_nonHilbert,C_marker_readout; K*C values missing.",
        },
        {
            "row_id": "ENV4430_2_single_channel_D_mhat",
            "envelope": f"abs(D_mhat_source) <= {D_MHAT_ONE_CHANNEL_CEILING:.12e} if D_e_source=0",
            "bound_value": f"{D_MHAT_ONE_CHANNEL_CEILING:.12e}",
            "units": "dimensionless",
            "source_path": str(CSV_MTS_DD_STATUS),
            "numeric_bound_present": True,
            "theory_values_present": False,
            "no_cancellation_policy": True,
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "One-channel empirical target, not a theory prediction.",
        },
        {
            "row_id": "ENV4430_3_single_channel_D_e",
            "envelope": f"abs(D_e_source) <= {D_E_ONE_CHANNEL_CEILING:.12e} if D_mhat_source=0",
            "bound_value": f"{D_E_ONE_CHANNEL_CEILING:.12e}",
            "units": "dimensionless",
            "source_path": str(CSV_MTS_DD_STATUS),
            "numeric_bound_present": True,
            "theory_values_present": False,
            "no_cancellation_policy": True,
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "One-channel empirical target, not a theory prediction.",
        },
    ]


def coefficient_queue_rows() -> List[Dict[str, object]]:
    return [
        {"queue_id": "KQ4430_0_K_m_block", "target": "K_m_block*C_block", "why_first": "block residual is the only piece left after exchange connectivity fails", "needed_input": "ordinary matter exchange graph or parent block split", "source_path": str(CSV_NSP1765), "valid_for_claim": False},
        {"queue_id": "KQ4430_1_K_m_shadow", "target": "K_m_shadow*C_shadow", "why_first": "source-shadow is the cleanest remaining countermodel", "needed_input": "parent grammar ban or explicit source-shadow coefficient", "source_path": str(CSV_NSS3542), "valid_for_claim": False},
        {"queue_id": "KQ4430_2_K_m_nonHilbert", "target": "K_m_nonHilbert*C_nonHilbert", "why_first": "non-Hilbert bypass survives all Hilbert-owner arguments", "needed_input": "J_NH=0 theorem or finite current coefficient", "source_path": str(CSV_SLF1603), "valid_for_claim": False},
        {"queue_id": "KQ4430_3_K_e_marker", "target": "K_e_marker*C_marker_readout", "why_first": "hidden/readout return can reintroduce species dependence under another name", "needed_input": "no-hidden-return theorem or marker/readout coefficient", "source_path": str(CSV_SF2613), "valid_for_claim": False},
    ]


def claim_gate_rows(signature: Sequence[Mapping[str, str]], dd: Sequence[Mapping[str, str]], envelopes: Sequence[Mapping[str, str]]) -> List[Dict[str, object]]:
    sig = {row["row_id"]: row for row in signature}
    dd_rows = {row["row_id"]: row for row in dd}
    env = {row["row_id"]: row for row in envelopes}
    no_claims = not any(row.get("valid_for_claim") == "True" for row in signature) and not any(row.get("valid_for_claim") == "True" for row in dd) and not any(row.get("valid_for_claim") == "True" for row in envelopes)
    return [
        {"gate_id": "CG4430_0_zero_signature", "claim": "full C_species=0 signature staged", "passed": sig["SIG4430_0_full_zero_signature"].get("current_status") == "SOURCE_OWNER_SIGNATURE_CONTRACT_READY_NONCLAIM", "valid_for_claim": False, "detail": "exact but input-invalid until parent grammar signs it."},
        {"gate_id": "CG4430_1_current_owner_partial", "claim": "current total Hilbert owner remains partial", "passed": sig["SIG4430_1_current_total_Hilbert_owner"].get("current_status") == "TOTAL_HILBERT_OWNER_SOURCE_SHADOW_OPEN", "valid_for_claim": False, "detail": "source-shadow, no-Hom and non-Hilbert bypass remain live."},
        {"gate_id": "CG4430_2_no_weight_core", "claim": "same-action/exchange filter reduces residuals", "passed": sig["SIG4430_2_no_source_weight_core"].get("current_status") == "SOURCE_OWNER_SIGNATURE_REDUCES_TO_HIDDEN_NONHILBERT_RETURNS", "valid_for_claim": False, "detail": "arbitrary species weights collapse to hidden/non-Hilbert return channels."},
        {"gate_id": "CG4430_3_DD_symbolic_map", "claim": "MTS residual vector mapped symbolically into DD source channels", "passed": dd_rows["DD4430_0_D_mhat_symbolic"].get("current_status") == "DD_SYMBOLIC_MAP_READY_VALUES_MISSING" and dd_rows["DD4430_1_D_e_symbolic"].get("current_status") == "DD_SYMBOLIC_MAP_READY_VALUES_MISSING", "valid_for_claim": False, "detail": "K values and source leg are missing."},
        {"gate_id": "CG4430_4_envelope_target", "claim": "no-cancellation Ti/Pt envelope is ready as nonclaim target", "passed": env["ENV4430_1_no_cancellation_envelope"].get("current_status") == "DD_ENVELOPE_TARGET_READY_THEORY_VALUES_MISSING", "valid_for_claim": False, "detail": "real bound target, missing theory values."},
        {"gate_id": "CG4430_5_single_channel_targets", "claim": "single-channel numeric ceilings are ready", "passed": env["ENV4430_2_single_channel_D_mhat"].get("current_status") == "DD_ENVELOPE_TARGET_READY_THEORY_VALUES_MISSING" and env["ENV4430_3_single_channel_D_e"].get("current_status") == "DD_ENVELOPE_TARGET_READY_THEORY_VALUES_MISSING", "valid_for_claim": False, "detail": "empirical ceilings only, not predictions."},
        {"gate_id": "CG4430_6_no_claim_outputs", "claim": "4430 emits no local-GR/WEP/PPN/R10 claim", "passed": no_claims, "valid_for_claim": False, "detail": "all outputs remain private nonclaim rows."},
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4430_0",
            "decision": DECISION,
            "summary": "4430 sharpens calibrated source coupling. The exact zero signature is now explicit: one total matter action, total Hilbert/coframe source, source functor on T_total not labelled pairs, no source-shadow, no species/hidden Hom into active coefficients, no non-Hilbert bypass, exchange-connected or common calibration. Current MTS has not parent-signed those grammar clauses. The finite fallback is materially better: the retained C_species vector is mapped symbolically into D_mhat_source and D_e_source, with a no-cancellation Ti/Pt envelope and one-channel ceilings.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "public_claim": False,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {"status_id": "STAT4430_0_zero", "status": "TOTAL_HILBERT_SOURCE_ZERO_SIGNATURE_EXACT_UNSIGNED", "detail": "C_species=0 follows if all source owner/no-Hom/no-bypass clauses are parent-signed.", "valid_for_claim": False},
        {"status_id": "STAT4430_1_finite", "status": "DD_SYMBOLIC_MAP_AND_ENVELOPE_READY_VALUES_MISSING", "detail": "D_mhat/D_e now receive C_block,C_shadow,C_nonHilbert,C_marker_readout through K values.", "valid_for_claim": False},
        {"status_id": "STAT4430_2_targets", "status": "SINGLE_CHANNEL_NUMERIC_CEILINGS_READY_NONCLAIM", "detail": f"D_mhat ceiling {D_MHAT_ONE_CHANNEL_CEILING:.12e}; D_e ceiling {D_E_ONE_CHANNEL_CEILING:.12e}.", "valid_for_claim": False},
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4430_0",
            "target": NEXT_TARGET,
            "objective": "Close the source-shadow/non-Hilbert bypass clauses for C_species=0, or fill the first DD K*C value/source leg.",
            "derive_first": "prove no independent source-shadow functional S_source=sum_A w_A S_A exists and J_NH=0 for ordinary calibrated matter after total Hilbert variation.",
            "fallback": "fill one product row such as K_m_shadow*C_shadow or K_m_nonHilbert*C_nonHilbert with parent provenance, units, and Ti/Pt projection.",
            "avoid": "using Ward covariance alone to ban weighted actions; treating one-channel ceilings as predictions; hiding marker/readout returns inside common calibration.",
            "valid_for_claim": False,
        }
    ]


def build_doc(sources: Sequence[Mapping[str, object]], signature: Sequence[Mapping[str, str]], dd: Sequence[Mapping[str, str]], envelopes: Sequence[Mapping[str, str]], gates: Sequence[Mapping[str, object]]) -> str:
    return f"""# 446 PPC4161 total Hilbert source owner no-source-weight signature or TiPt DD map

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4430 pushes calibrated source coupling into a sharper form:

- `C_species=DERIVED_ZERO` follows if the active source is only `T_total=delta S_matter/delta e_obs`, the source functor forgets labels, and source-shadow/hidden/non-Hilbert returns are forbidden.
- Current MTS has the theorem shape, but not the parent grammar signature that forbids every return channel.
- The finite branch now has a symbolic DD map:
  `D_mhat_source=sum_j K_mj C_j`, `D_e_source=sum_j K_ej C_j` for `C_j in {{C_block,C_shadow,C_nonHilbert,C_marker_readout}}`.
- The no-cancellation Ti/Pt envelope is now explicit:
  `0.00333 sum_j |K_mj C_j| + 0.00204 sum_j |K_ej C_j| <= 2.8e-15`.

## Source Register

{table(sources)}

## Derivation Rows

{table(derivation_rows())}

## Source Owner Signature Gate

{table(signature)}

## DD Source Map Gate

{table(dd)}

## DD Envelope Gate

{table(envelopes)}

## First DD K Queue

{table(coefficient_queue_rows())}

## Claim Gates

{table(gates)}

## Decision

{table(decision_rows())}

## Next Target

{table(next_rows())}
"""


def post_doc() -> str:
    return f"""# 4430 - total Hilbert source owner no-source-weight signature or TiPt DD map

Marker: `{MARKER}`

Private checkpoint generated at `{STAMP}`.

## What changed

- Wrote the exact total-Hilbert/no-source-weight signature for `C_species=DERIVED_ZERO`.
- Kept it nonclaim because source-shadow, no-Hom constructor, hidden return and non-Hilbert bypass clauses are not parent-signed.
- Built the symbolic MTS-to-DD source map for `D_mhat_source` and `D_e_source`.
- Added the no-cancellation Ti/Pt envelope and single-channel numeric ceilings as nonclaim empirical targets.

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
        sep = "" if existing.endswith("\n") or not existing else "\n"
        write_text(path, existing + sep + block)


def update_claims_register() -> None:
    rows = rows_from(CLAIMS_PATH) if CLAIMS_PATH.exists() else []
    fieldnames = list(rows[0].keys()) if rows else ["claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk", "sector", "evidence", "next_action", "risk"]
    rows = [row for row in rows if row.get("claim_id") != CLAIM_ID]
    new_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": "4430 writes the exact total-Hilbert source owner/no-source-weight signature for C_species=DERIVED_ZERO, but current MTS has not parent-signed source-shadow exclusion, no-Hom constructor exhaustion, hidden/readout return silence, or non-Hilbert bypass zero. The finite fallback now has a symbolic MTS-to-DD map for D_mhat_source and D_e_source, a no-cancellation Ti/Pt envelope, and numeric single-channel ceilings, all nonclaim.",
        "current_evidence": "4430 source register, derivation rows, source owner signature output, DD source map output, DD envelope output, first DD K queue, claim gates, decision, status, next target and validation CSV.",
        "status": "total_hilbert_source_zero_signature_exact_unsigned_dd_symbolic_envelope_ready_values_missing",
        "next_test": "Prove source-shadow/non-Hilbert bypass zero, or fill the first DD K*C product/source-leg row.",
        "key_risk": "Using Ward covariance alone to ban weighted actions; treating one-channel ceilings as predictions; hiding marker/readout returns inside common calibration.",
        "sector": "local_gr",
        "evidence": "4430 source register, derivation rows, source owner signature output, DD source map output, DD envelope output, first DD K queue, claim gates, decision, status, next target and validation CSV.",
        "next_action": "Prove source-shadow/non-Hilbert bypass zero, or fill the first DD K*C product/source-leg row.",
        "risk": "Using Ward covariance alone to ban weighted actions; treating one-channel ceilings as predictions; hiding marker/readout returns inside common calibration.",
    }
    rows.append({name: new_row.get(name, "") for name in fieldnames})
    with CLAIMS_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_spine_and_packet() -> None:
    spine_section = f"""## 4430 local spine update: source zero signature and DD envelope

4430 pins calibrated source coupling to two exact routes. The zero route is the total-Hilbert/no-source-weight signature: source equals one total Hilbert/coframe derivative, source functor sees `T_total`, and species/hidden/readout/non-Hilbert return channels are forbidden. The finite route maps the retained vector `C_block,C_shadow,C_nonHilbert,C_marker_readout` into DD channels `D_mhat_source,D_e_source` and the Ti/Pt no-cancellation envelope. Current MTS still lacks parent-signed source-shadow and non-Hilbert exclusions, plus actual `K*C` values.
"""
    packet_section = f"""## 4430 packet update: DD map is symbolic-ready

`{PACKET_MARKER}`

Private packet result: `C_species` is now either zero by a precise source-owner signature or finite through a concrete DD envelope. The next practical target is one `K*C` product or a proof that the source-shadow/non-Hilbert channels are absent.
"""
    upsert_marked_section(SPINE_PATH, MARKER, spine_section)
    upsert_marked_section(PACKET_PATH, PACKET_MARKER, packet_section)


def validation_rows(paths: Mapping[str, Path]) -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    sig = {row["row_id"]: row for row in rows_from(SIGNATURE_OUTPUT)}
    dd = {row["row_id"]: row for row in rows_from(DD_OUTPUT)}
    env = {row["row_id"]: row for row in rows_from(ENVELOPE_OUTPUT)}
    gates = rows_from(CLAIM_GATES)
    no_claims = not any(row.get("valid_for_claim") == "True" for row in sig.values()) and not any(row.get("valid_for_claim") == "True" for row in dd.values()) and not any(row.get("valid_for_claim") == "True" for row in env.values())
    checks = [
        ("VAL4430_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source path exists"),
        ("VAL4430_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited source needle is present"),
        ("VAL4430_2_zero_signature_contract", sig["SIG4430_0_full_zero_signature"].get("current_status") == "SOURCE_OWNER_SIGNATURE_CONTRACT_READY_NONCLAIM", "full zero signature staged"),
        ("VAL4430_3_current_owner_partial", sig["SIG4430_1_current_total_Hilbert_owner"].get("current_status") == "TOTAL_HILBERT_OWNER_SOURCE_SHADOW_OPEN", "current owner remains partial"),
        ("VAL4430_4_no_weight_core", sig["SIG4430_2_no_source_weight_core"].get("current_status") == "SOURCE_OWNER_SIGNATURE_REDUCES_TO_HIDDEN_NONHILBERT_RETURNS", "no-weight core reduces residuals"),
        ("VAL4430_5_DD_symbolic_mhat", dd["DD4430_0_D_mhat_symbolic"].get("current_status") == "DD_SYMBOLIC_MAP_READY_VALUES_MISSING", "D_mhat symbolic map ready"),
        ("VAL4430_6_DD_symbolic_e", dd["DD4430_1_D_e_symbolic"].get("current_status") == "DD_SYMBOLIC_MAP_READY_VALUES_MISSING", "D_e symbolic map ready"),
        ("VAL4430_7_envelope_target", env["ENV4430_1_no_cancellation_envelope"].get("current_status") == "DD_ENVELOPE_TARGET_READY_THEORY_VALUES_MISSING", "no-cancellation envelope ready"),
        ("VAL4430_8_single_channel_ceilings", f"{D_MHAT_ONE_CHANNEL_CEILING:.12e}" in text(ENVELOPE_OUTPUT) and f"{D_E_ONE_CHANNEL_CEILING:.12e}" in text(ENVELOPE_OUTPUT), "single-channel ceilings written"),
        ("VAL4430_9_queue_written", len(rows_from(COEFFICIENT_QUEUE)) == 4 and "K_m_shadow" in text(COEFFICIENT_QUEUE), "first DD K queue written"),
        ("VAL4430_10_no_claim_outputs", no_claims, "no output row is claim-ready"),
        ("VAL4430_11_claim_gate_no_claim", any(row["gate_id"] == "CG4430_6_no_claim_outputs" and row["passed"] == "True" for row in gates), "claim gate explicitly blocks public claim"),
        ("VAL4430_12_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-271"),
        ("VAL4430_13_formal_doc", paths["formal"].exists() and MARKER in text(paths["formal"]), "formal doc exists with marker"),
        ("VAL4430_14_post_doc", paths["post"].exists() and "Private checkpoint" in text(paths["post"]), "post checkpoint doc exists"),
        ("VAL4430_15_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4430_16_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4430_17_next_target", paths["next"].exists() and NEXT_TARGET in text(paths["next"]), "next target file exists"),
        ("VAL4430_18_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": bool(passed), "detail": detail} for check_id, passed, detail in checks]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(DERIVATION_ROWS, derivation_rows())
    write_csv(SIGNATURE_INPUT, signature_input_rows())
    write_csv(SIGNATURE_OUTPUT, evaluate_signature_rows(SIGNATURE_INPUT))
    write_csv(DD_INPUT, dd_input_rows())
    write_csv(DD_OUTPUT, evaluate_dd_map_rows(DD_INPUT))
    write_csv(ENVELOPE_INPUT, envelope_input_rows())
    write_csv(ENVELOPE_OUTPUT, evaluate_envelope_rows(ENVELOPE_INPUT))
    write_csv(COEFFICIENT_QUEUE, coefficient_queue_rows())
    signature = rows_from(SIGNATURE_OUTPUT)
    dd = rows_from(DD_OUTPUT)
    envelopes = rows_from(ENVELOPE_OUTPUT)
    gates = claim_gate_rows(signature, dd, envelopes)
    write_csv(CLAIM_GATES, gates)
    write_csv(DECISION_CSV, decision_rows())
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    write_text(FORMAL_PATH, build_doc(rows_from(SOURCE_REGISTER), signature, dd, envelopes, gates))
    write_text(DOC_PATH, post_doc())
    update_claims_register()
    write_spine_and_packet()
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    write_csv(VALIDATION_PATH, validation_rows({"formal": FORMAL_PATH, "post": DOC_PATH, "next": NEXT_CSV}))


if __name__ == "__main__":
    main()

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

from source_shadow_nonhilbert_k_gate import (  # noqa: E402
    evaluate_kproduct_rows,
    evaluate_nonhilbert_rows,
    evaluate_shadow_rows,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4431"
CLAIM_ID = "L-272"
MARKER = "PPC4161_SOURCE_SHADOW_BAN_AND_NONHILBERT_BYPASS_ZERO_OR_FIRST_DD_K_VALUE_4431"
PACKET_MARKER = "PPC4161_PACKET_SOURCE_SHADOW_BAN_AND_NONHILBERT_BYPASS_ZERO_OR_FIRST_DD_K_VALUE_4431"
DECISION = "SOURCE_SHADOW_AND_NONHILBERT_ZERO_THEOREMS_EXACT_BUT_PARENT_SIGNATURES_UNSIGNED_FIRST_DD_K_PRODUCT_STAGED"
NEXT_TARGET = "4432-Y5-R2FR-source-shadow-constructor-noHom-proof-or-KmshadowCshadow-first-value.md"

FORMAL_PATH = FORMAL / "447-PPC4161-source-shadow-ban-and-nonHilbert-bypass-zero-or-first-DD-K-value.md"
DOC_PATH = POST / "4431-Y5-R2FR-source-shadow-ban-and-nonHilbert-bypass-zero-or-first-DD-K-value.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4431_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4431_SOURCE_REGISTER.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4431_DERIVATION_ROWS.csv"
SHADOW_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4431_SOURCE_SHADOW_INPUT.csv"
SHADOW_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4431_SOURCE_SHADOW_OUTPUT.csv"
NONHILBERT_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4431_NONHILBERT_BYPASS_INPUT.csv"
NONHILBERT_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4431_NONHILBERT_BYPASS_OUTPUT.csv"
KPRODUCT_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4431_DD_K_PRODUCT_INPUT.csv"
KPRODUCT_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4431_DD_K_PRODUCT_OUTPUT.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4431_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4431_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4431_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4431_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "source_shadow_nonhilbert_k_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4431_source_shadow_ban_and_nonHilbert_bypass_zero_or_first_DD_K_value.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4430 = SOURCE_DIR / "P8_Y5_R2FR_4430_NEXT_TARGET.csv"
FORMAL_446 = FORMAL / "446-PPC4161-total-Hilbert-source-owner-no-source-weight-signature-or-TiPt-DD-map.md"
SIG4430 = SOURCE_DIR / "P8_Y5_R2FR_4430_SOURCE_OWNER_SIGNATURE_OUTPUT.csv"
QUEUE4430 = SOURCE_DIR / "P8_Y5_R2FR_4430_FIRST_DD_K_VALUE_QUEUE.csv"
ENV4430 = SOURCE_DIR / "P8_Y5_R2FR_4430_DD_ENVELOPE_OUTPUT.csv"
CSV_SSB2616 = SOURCE_DIR / "P8_Y5_EXCHANGE_GRAPH_GATE_2616_SOURCE_SHADOW_BAN_ATTEMPT.csv"
CSV_NSP2508 = SOURCE_DIR / "P8_Y5_NO_SHADOW_2508_NO_SOURCE_ONLY_SLOT_PROOF_ATTEMPT.csv"
CSV_CM2508 = SOURCE_DIR / "P8_Y5_NO_SHADOW_2508_SOURCE_ONLY_COUNTERMODELS.csv"
CSV_RSW2508 = SOURCE_DIR / "P8_Y5_NO_SHADOW_2508_SOURCE_WEIGHT_RESIDUAL_ROWS.csv"
CSV_NSCI2538 = SOURCE_DIR / "P8_Y5_NO_SHADOW_2538_NOETHER_SOURCE_CHARGE_IDENTITY_ATTEMPT.csv"
CSV_NHR2538 = SOURCE_DIR / "P8_Y5_NO_SHADOW_2538_NONHILBERT_RESIDUAL_ROW.csv"
CSV_NH_STATUS = SOURCE_DIR / "P8_Y5_nonHilbert_bypass_official_fallback_status.csv"
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
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(md(row.get(header, "")) for header in headers) + " |")
    return "\n".join(output)


def source_specs() -> List[Dict[str, object]]:
    return [
        {"source_id": "SRC4431_00_4430_next", "path": NEXT_4430, "needle": "source-shadow/non-Hilbert", "role": "4430 handoff to 4431."},
        {"source_id": "SRC4431_01_446_formal", "path": FORMAL_446, "needle": "THS4430_0_zero_signature", "role": "formal source-owner zero signature."},
        {"source_id": "SRC4431_02_sig4430", "path": SIG4430, "needle": "SIG4430_2_no_source_weight_core", "role": "source-owner signature gate."},
        {"source_id": "SRC4431_03_queue4430", "path": QUEUE4430, "needle": "KQ4430_1_K_m_shadow", "role": "first DD K queue."},
        {"source_id": "SRC4431_04_env4430", "path": ENV4430, "needle": "ENV4430_1_no_cancellation_envelope", "role": "Ti/Pt envelope."},
        {"source_id": "SRC4431_05_ssb2616", "path": CSV_SSB2616, "needle": "SSB2616_5_current_verdict", "role": "source-shadow ban attempt."},
        {"source_id": "SRC4431_06_nsp2508", "path": CSV_NSP2508, "needle": "NSP2508_6_counterexample", "role": "no-source-only slot proof attempt."},
        {"source_id": "SRC4431_07_cm2508", "path": CSV_CM2508, "needle": "CM2508_0_wA_action", "role": "surviving source-weight countermodel."},
        {"source_id": "SRC4431_08_rsw2508", "path": CSV_RSW2508, "needle": "RSW2508_0", "role": "source-weight residual rows."},
        {"source_id": "SRC4431_09_nsci2538", "path": CSV_NSCI2538, "needle": "NSCI2538_5_nonhilbert_channels", "role": "Noether source charge identity attempt."},
        {"source_id": "SRC4431_10_nhr2538", "path": CSV_NHR2538, "needle": "NHR2538_0_total", "role": "non-Hilbert residual row."},
        {"source_id": "SRC4431_11_nh_status", "path": CSV_NH_STATUS, "needle": "NONHILBERT_TOTAL_ZERO_NOT_DERIVED", "role": "official non-Hilbert fallback status."},
        {"source_id": "SRC4431_12_mts_dd_status", "path": CSV_MTS_DD_STATUS, "needle": "STAT3544_0_map", "role": "MTS-to-DD source map status."},
        {"source_id": "SRC4431_13_first_dd_status", "path": CSV_FIRST_DD_STATUS, "needle": "STATUS3545_0", "role": "first DD K value/source-leg status."},
        {"source_id": "SRC4431_14_gate", "path": GATE_PATH, "needle": "def evaluate_shadow_row", "role": "4431 gate script."},
        {"source_id": "SRC4431_15_generator", "path": GENERATOR_PATH, "needle": "CHECKPOINT = \"4431\"", "role": "4431 generator script."},
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
            "derivation_id": "SH4431_0_shadow_ban_theorem",
            "claim": "A source-shadow functional is untypeable if active ordinary source has one parent owner.",
            "derivation": "If the only ordinary source object is T_total=delta S_matter/delta e_obs, if Coeff_active_source is generated only from q(Phi), theta_rep and universal constants, and if Hom_parent(SpeciesLabel,Coeff_active_source)=Hom_parent(HiddenMarker,Coeff_active_source)=empty before readout, then an independent S_source=sum_A w_A S_A cannot be formed as a parent term. Source-shadow is not small; it is absent.",
            "consequence": "This would kill C_shadow exactly rather than fitting or bounding it.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "SH4431_1_current_gap",
            "claim": "Current MTS has the shadow-ban theorem shape but not the parent no-Hom/constructor signature.",
            "derivation": "The single Hilbert owner and exchange filter pressure weighted source actions, but 2508 still has legal countermodels w_A S_A, kappa_A T_A, direct-sum constants, hidden markers, readout projectors and action-scale weights unless a parent grammar forbids them.",
            "consequence": "C_shadow remains a finite residual channel and the first DD product target is K_m_shadow*C_shadow.",
            "status": "PARENT_CONSTRUCTOR_NOHOM_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "NH4431_0_nonHilbert_zero_theorem",
            "claim": "A non-Hilbert source bypass vanishes if it is only an owned improvement with zero compact flux.",
            "derivation": "If the Noether source charge decomposes as J_active=J_Hilbert+dU+J_NH, if spin/torsion/hypermomentum, boundary/worldtube, readout/projector and improvement terms are all parent-owned, and if dU has zero compact projected flux, then P_source[J_NH]=0 or is a common calibration term. It cannot carry species-dependent active source weight.",
            "consequence": "This would kill C_nonHilbert exactly rather than treating it as a hidden coupling.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "NH4431_1_current_gap",
            "claim": "Current MTS retains the non-Hilbert residual row.",
            "derivation": "2538 derives Hilbert/Noether ownership conditionally, but explicitly leaves spin/torsion, boundary/worldtube, readout reentry, improvement flux and projected mass charge open. 3564 therefore selected the official non-Hilbert fallback.",
            "consequence": "C_nonHilbert remains in the DD residual vector until those channels are zeroed or bounded.",
            "status": "NONHILBERT_RESIDUAL_RETAINED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "K4431_0_first_product_contract",
            "claim": "The first finite coefficient target is K_m_shadow*C_shadow.",
            "derivation": f"With source-shadow still unsigned, the Ti/Pt one-channel target is abs(K_m_shadow*C_shadow) <= {D_MHAT_ONE_CHANNEL_CEILING:.12e} if all other D_mhat and D_e components are zero. In the no-cancellation envelope it appears as {DELTA_Q_MHAT:.5f}*abs(K_m_shadow*C_shadow) inside a total bound {ETA_BOUND:.12e}.",
            "consequence": "This is not a prediction; it is a concrete acquisition row for the next source-coupling pass.",
            "status": "DD_K_PRODUCT_CONTRACT_STAGED",
            "valid_for_claim": False,
        },
    ]


def shadow_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "SH4431_0_exact_shadow_zero_contract",
            "clause": "source-shadow zero theorem contract",
            "single_parent_action": True,
            "no_independent_source_functional": True,
            "no_weighted_duplicate_action": True,
            "constructor_no_hom": True,
            "exchange_graph_connected": True,
            "hidden_readout_no_return": True,
            "source_path": str(FORMAL_446),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Exact theorem target; nonclaim until parent grammar signs all clauses.",
        },
        {
            "row_id": "SH4431_1_current_no_weight_core",
            "clause": "current same-action/exchange source-shadow pressure",
            "single_parent_action": True,
            "no_independent_source_functional": True,
            "no_weighted_duplicate_action": True,
            "constructor_no_hom": False,
            "exchange_graph_connected": True,
            "hidden_readout_no_return": False,
            "source_path": str(SIG4430),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Reduces arbitrary source weights to constructor/no-Hom and hidden-return gaps.",
        },
        {
            "row_id": "SH4431_2_wA_countermodel_survives",
            "clause": "weighted duplicate action countermodel",
            "single_parent_action": True,
            "no_independent_source_functional": False,
            "no_weighted_duplicate_action": False,
            "constructor_no_hom": False,
            "exchange_graph_connected": False,
            "hidden_readout_no_return": False,
            "source_path": str(CSV_CM2508),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "S_matter=sum_A w_A S_A remains legal unless parent object language forbids the slot.",
        },
        {
            "row_id": "SH4431_3_source_shadow_current_verdict",
            "clause": "current source-shadow ban verdict",
            "single_parent_action": True,
            "no_independent_source_functional": True,
            "no_weighted_duplicate_action": False,
            "constructor_no_hom": False,
            "exchange_graph_connected": True,
            "hidden_readout_no_return": False,
            "source_path": str(CSV_SSB2616),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "2616 isolates the route but does not parent-sign it.",
        },
    ]


def nonhilbert_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "NH4431_0_exact_nonHilbert_zero_contract",
            "clause": "non-Hilbert bypass zero theorem contract",
            "total_noether_identity": True,
            "hilbert_current_owner": True,
            "spin_boundary_improvement_owned": True,
            "readout_projector_after_variation": True,
            "J_NH_decomposition_declared": True,
            "J_NH_zero_or_exact_divergence": True,
            "compact_flux_zero": True,
            "source_path": str(CSV_NSCI2538),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Exact theorem target; still nonclaim because component zeros are not parent-signed.",
        },
        {
            "row_id": "NH4431_1_current_residual_retained",
            "clause": "current non-Hilbert residual row",
            "total_noether_identity": True,
            "hilbert_current_owner": True,
            "spin_boundary_improvement_owned": False,
            "readout_projector_after_variation": False,
            "J_NH_decomposition_declared": True,
            "J_NH_zero_or_exact_divergence": False,
            "compact_flux_zero": False,
            "source_path": str(CSV_NHR2538),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "2538 keeps P_source[J_NH] as a residual envelope.",
        },
        {
            "row_id": "NH4431_2_improvement_exact_boundary_open",
            "clause": "exact improvement but compact flux open",
            "total_noether_identity": True,
            "hilbert_current_owner": True,
            "spin_boundary_improvement_owned": True,
            "readout_projector_after_variation": False,
            "J_NH_decomposition_declared": True,
            "J_NH_zero_or_exact_divergence": True,
            "compact_flux_zero": False,
            "source_path": str(CSV_NSCI2538),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "An exact divergence is safe only after projected compact flux is zero or bounded.",
        },
        {
            "row_id": "NH4431_3_official_fallback_status",
            "clause": "official fallback remains selected",
            "total_noether_identity": True,
            "hilbert_current_owner": True,
            "spin_boundary_improvement_owned": False,
            "readout_projector_after_variation": False,
            "J_NH_decomposition_declared": True,
            "J_NH_zero_or_exact_divergence": False,
            "compact_flux_zero": False,
            "source_path": str(CSV_NH_STATUS),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "3564 says non-Hilbert total zero is not derived and fallback is official.",
        },
    ]


def kproduct_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "K4431_0_K_m_shadow_contract",
            "product": "K_m_shadow*C_shadow",
            "dd_channel": "D_mhat_source",
            "value": "MISSING_PARENT_COEFFICIENT",
            "units": "dimensionless",
            "parent_coefficient_source": "MISSING_PARENT_COEFFICIENT_SOURCE",
            "K_source": "MISSING_K_m_shadow",
            "source_leg": "MISSING_SOURCE_LEG",
            "projection_formula": f"{DELTA_Q_MHAT:.5f}*abs(K_m_shadow*C_shadow) <= {ETA_BOUND:.12e}",
            "bound_value": f"{D_MHAT_ONE_CHANNEL_CEILING:.12e}",
            "source_path": str(QUEUE4430),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "First finite source-shadow product to fill if no-Hom proof stays unsigned.",
        },
        {
            "row_id": "K4431_1_K_m_shadow_bound_target",
            "product": "K_m_shadow*C_shadow",
            "dd_channel": "D_mhat_source",
            "value": f"BOUND_ONLY_{D_MHAT_ONE_CHANNEL_CEILING:.12e}",
            "units": "dimensionless",
            "parent_coefficient_source": "MISSING_PARENT_COEFFICIENT_SOURCE",
            "K_source": "MISSING_K_m_shadow",
            "source_leg": "MISSING_SOURCE_LEG",
            "projection_formula": f"abs(K_m_shadow*C_shadow) <= {D_MHAT_ONE_CHANNEL_CEILING:.12e} if all other DD source components vanish",
            "bound_value": f"{D_MHAT_ONE_CHANNEL_CEILING:.12e}",
            "source_path": str(CSV_FIRST_DD_STATUS),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Empirical target only; not a theory value.",
        },
        {
            "row_id": "K4431_2_K_m_nonHilbert_contract",
            "product": "K_m_nonHilbert*C_nonHilbert",
            "dd_channel": "D_mhat_source",
            "value": "MISSING_PARENT_COEFFICIENT",
            "units": "dimensionless",
            "parent_coefficient_source": "MISSING_PARENT_COEFFICIENT_SOURCE",
            "K_source": "MISSING_K_m_nonHilbert",
            "source_leg": "MISSING_SOURCE_LEG",
            "projection_formula": f"{DELTA_Q_MHAT:.5f}*abs(K_m_nonHilbert*C_nonHilbert) <= {ETA_BOUND:.12e}",
            "bound_value": f"{D_MHAT_ONE_CHANNEL_CEILING:.12e}",
            "source_path": str(CSV_NHR2538),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Second finite product if source-shadow closes before non-Hilbert bypass.",
        },
    ]


def claim_gate_rows(shadow: Sequence[Mapping[str, str]], nonhilbert: Sequence[Mapping[str, str]], kproducts: Sequence[Mapping[str, str]]) -> List[Dict[str, object]]:
    shadow_rows = {row["row_id"]: row for row in shadow}
    nh_rows = {row["row_id"]: row for row in nonhilbert}
    k_rows = {row["row_id"]: row for row in kproducts}
    no_claims = not any(row.get("valid_for_claim") == "True" for row in shadow) and not any(row.get("valid_for_claim") == "True" for row in nonhilbert) and not any(row.get("valid_for_claim") == "True" for row in kproducts)
    return [
        {"gate_id": "CG4431_0_shadow_contract", "claim": "source-shadow exact zero theorem staged", "passed": shadow_rows["SH4431_0_exact_shadow_zero_contract"].get("current_status") == "SOURCE_SHADOW_BAN_CONTRACT_READY_NONCLAIM", "valid_for_claim": False, "detail": "Exact but parent object language unsigned."},
        {"gate_id": "CG4431_1_shadow_current_gap", "claim": "current source-shadow ban reduces but does not close", "passed": shadow_rows["SH4431_1_current_no_weight_core"].get("current_status") == "SOURCE_SHADOW_REDUCES_TO_BLOCK_AND_HIDDEN_RETURN", "valid_for_claim": False, "detail": "No-Hom/constructor and hidden readout return remain open."},
        {"gate_id": "CG4431_2_shadow_countermodel", "claim": "weighted-action countermodel remains live", "passed": shadow_rows["SH4431_2_wA_countermodel_survives"].get("current_status") == "SOURCE_SHADOW_COUNTERMODEL_SURVIVES", "valid_for_claim": False, "detail": "The route cannot be declared zero by covariance alone."},
        {"gate_id": "CG4431_3_nonHilbert_contract", "claim": "non-Hilbert exact zero theorem staged", "passed": nh_rows["NH4431_0_exact_nonHilbert_zero_contract"].get("current_status") == "NONHILBERT_BYPASS_ZERO_CONTRACT_READY_NONCLAIM", "valid_for_claim": False, "detail": "Exact but spin/boundary/readout/flux clauses unsigned."},
        {"gate_id": "CG4431_4_nonHilbert_residual", "claim": "current non-Hilbert row remains retained", "passed": nh_rows["NH4431_1_current_residual_retained"].get("current_status") == "NONHILBERT_RESIDUAL_ROW_RETAINED", "valid_for_claim": False, "detail": "Residual envelope stays in the finite branch."},
        {"gate_id": "CG4431_5_first_K_contract", "claim": "first K_m_shadow*C_shadow product row staged", "passed": k_rows["K4431_0_K_m_shadow_contract"].get("current_status") == "DD_K_PRODUCT_CONTRACT_ONLY", "valid_for_claim": False, "detail": "Has units/projection/bound target but no parent coefficient/source leg."},
        {"gate_id": "CG4431_6_K_bound_target", "claim": "K_m_shadow*C_shadow one-channel bound target is explicit", "passed": k_rows["K4431_1_K_m_shadow_bound_target"].get("current_status") == "DD_K_PRODUCT_BOUND_TARGET_ONLY", "valid_for_claim": False, "detail": "Bound target only, not a prediction."},
        {"gate_id": "CG4431_7_no_claim_outputs", "claim": "4431 emits no local-GR/WEP/PPN/R10 claim", "passed": no_claims, "valid_for_claim": False, "detail": "All rows remain private nonclaim rows."},
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4431_0",
            "decision": DECISION,
            "summary": "4431 makes the coupling gap less foggy. Source-shadow has an exact zero theorem if the parent object language forbids independent source functionals and Hom into active source coefficients; current MTS does not sign that yet and 2508 countermodels survive. Non-Hilbert bypass has an exact zero theorem if all improvement/spin/boundary/readout flux pieces are owned and compact-silent; current MTS retains the official residual row. The finite fallback is now a concrete first product: K_m_shadow*C_shadow in the Ti/Pt D_mhat channel.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "public_claim": False,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {"status_id": "STAT4431_0_shadow", "status": "SOURCE_SHADOW_ZERO_THEOREM_EXACT_PARENT_NOHOM_UNSIGNED", "detail": "C_shadow=0 follows if single source owner plus no-Hom/constructor/no-readout-return is parent-signed.", "valid_for_claim": False},
        {"status_id": "STAT4431_1_nonHilbert", "status": "NONHILBERT_ZERO_THEOREM_EXACT_FLUX_COMPONENTS_UNSIGNED", "detail": "C_nonHilbert=0 follows if J_NH is only exact owned improvement with zero compact projected flux.", "valid_for_claim": False},
        {"status_id": "STAT4431_2_K_target", "status": "K_M_SHADOW_C_SHADOW_FIRST_PRODUCT_STAGED_NONCLAIM", "detail": f"First finite target is abs(K_m_shadow*C_shadow) <= {D_MHAT_ONE_CHANNEL_CEILING:.12e} in one-channel D_mhat limit.", "valid_for_claim": False},
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4431_0",
            "target": NEXT_TARGET,
            "objective": "Either prove parent constructor/no-Hom exclusion for source-shadow, or fill K_m_shadow*C_shadow with a real parent coefficient and source leg.",
            "derive_first": "prove Hom_parent(SpeciesLabel or HiddenMarker, Coeff_active_source)=empty and ParentGenerate[q(Phi),theta_rep,constants] exhausts active source coefficients.",
            "fallback": "fill K_m_shadow*C_shadow with value, units, parent coefficient source, K source, source leg, Ti/Pt projection and no-cancellation policy.",
            "avoid": "using covariance/Noether conservation alone to ban weighted source actions; treating the one-channel ceiling as a predicted value.",
            "valid_for_claim": False,
        }
    ]


def build_doc(sources: Sequence[Mapping[str, object]], shadow: Sequence[Mapping[str, str]], nonhilbert: Sequence[Mapping[str, str]], kproducts: Sequence[Mapping[str, str]], gates: Sequence[Mapping[str, object]]) -> str:
    return f"""# 447 PPC4161 source-shadow ban and nonHilbert bypass zero or first DD K value

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4431 attacks the coupling gap directly:

- `C_shadow=0` is derivable if the parent object language has one source owner and no constructor/Hom into active source coefficients from species labels, hidden markers or readout projectors.
- Current MTS does not yet sign that parent grammar, so the weighted-action source-shadow countermodels stay live.
- `C_nonHilbert=0` is derivable if every non-Hilbert source-current piece is an owned exact improvement with zero compact projected flux.
- Current MTS does not yet sign the spin/boundary/readout/flux pieces, so the non-Hilbert residual row stays live.
- The finite fallback is now concrete: first fill or kill `K_m_shadow*C_shadow`, with one-channel target `abs(K_m_shadow*C_shadow) <= {D_MHAT_ONE_CHANNEL_CEILING:.12e}`.

## Source Register

{table(sources)}

## Derivation Rows

{table(derivation_rows())}

## Source-Shadow Gate

{table(shadow)}

## Non-Hilbert Bypass Gate

{table(nonhilbert)}

## DD K Product Gate

{table(kproducts)}

## Claim Gates

{table(gates)}

## Decision

{table(decision_rows())}

## Next Target

{table(next_rows())}
"""


def post_doc() -> str:
    return f"""# 4431 - source-shadow ban and nonHilbert bypass zero or first DD K value

Marker: `{MARKER}`

Private checkpoint generated at `{STAMP}`.

## What changed

- Tried the derivation route first for `C_shadow=0` and `C_nonHilbert=0`.
- Kept both zero routes nonclaim because parent constructor/no-Hom and compact-flux signatures are unsigned.
- Promoted `K_m_shadow*C_shadow` to the first concrete finite coupling target instead of circling generic coupling words.
- Preserved the Ti/Pt DD target as a bound/acquisition row, not a prediction.

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
        "claim": "4431 derives exact conditional zero theorems for C_shadow and C_nonHilbert, but keeps both nonclaim because parent constructor/no-Hom, hidden/readout return, spin/boundary/readout ownership and compact-flux clauses are unsigned. The fallback finite branch now stages K_m_shadow*C_shadow as the first DD product target.",
        "current_evidence": "4431 source register, derivation rows, source-shadow output, non-Hilbert bypass output, DD K product output, claim gates, decision, status, next target and validation CSV.",
        "status": "source_shadow_and_nonhilbert_zero_theorems_exact_parent_signatures_unsigned_first_dd_k_product_staged",
        "next_test": "Prove source-shadow constructor/no-Hom exclusion or fill K_m_shadow*C_shadow with a sourced parent coefficient and source leg.",
        "key_risk": "Using covariance or Noether conservation alone to ban weighted source actions; treating a one-channel Ti/Pt ceiling as a predicted value.",
        "sector": "local_gr",
        "evidence": "4431 source register, derivation rows, source-shadow output, non-Hilbert bypass output, DD K product output, claim gates, decision, status, next target and validation CSV.",
        "next_action": "Prove source-shadow constructor/no-Hom exclusion or fill K_m_shadow*C_shadow with a sourced parent coefficient and source leg.",
        "risk": "Using covariance or Noether conservation alone to ban weighted source actions; treating a one-channel Ti/Pt ceiling as a predicted value.",
    }
    rows.append({name: new_row.get(name, "") for name in fieldnames})
    with CLAIMS_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_spine_and_packet() -> None:
    spine_section = f"""## 4431 local spine update: source-shadow and non-Hilbert fork

4431 narrows the source-coupling problem to two real locks. The first is source-shadow: `C_shadow=0` follows if the parent source grammar has one active source owner and no `SpeciesLabel`/`HiddenMarker`/readout Hom into `Coeff_active_source`. The second is non-Hilbert bypass: `C_nonHilbert=0` follows if non-Hilbert current is only an owned exact improvement with zero compact projected flux. Neither parent signature is currently closed, so the finite branch now targets `K_m_shadow*C_shadow` first.
"""
    packet_section = f"""## 4431 packet update: first finite coupling product selected

`{PACKET_MARKER}`

Private packet result: the coupling gap is no longer generic. Either the parent object language kills `C_shadow`, or the next source-coupling row to fill is `K_m_shadow*C_shadow` with real provenance, units and Ti/Pt source leg. Non-Hilbert remains second unless its compact-flux zero proof closes first.
"""
    upsert_marked_section(SPINE_PATH, MARKER, spine_section)
    upsert_marked_section(PACKET_PATH, PACKET_MARKER, packet_section)


def validation_rows(paths: Mapping[str, Path]) -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    shadow = {row["row_id"]: row for row in rows_from(SHADOW_OUTPUT)}
    nonhilbert = {row["row_id"]: row for row in rows_from(NONHILBERT_OUTPUT)}
    kproducts = {row["row_id"]: row for row in rows_from(KPRODUCT_OUTPUT)}
    gates = rows_from(CLAIM_GATES)
    no_claims = not any(row.get("valid_for_claim") == "True" for row in shadow.values()) and not any(row.get("valid_for_claim") == "True" for row in nonhilbert.values()) and not any(row.get("valid_for_claim") == "True" for row in kproducts.values())
    checks = [
        ("VAL4431_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source path exists"),
        ("VAL4431_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited source needle is present"),
        ("VAL4431_2_shadow_contract", shadow["SH4431_0_exact_shadow_zero_contract"].get("current_status") == "SOURCE_SHADOW_BAN_CONTRACT_READY_NONCLAIM", "source-shadow zero theorem staged"),
        ("VAL4431_3_shadow_current_gap", shadow["SH4431_1_current_no_weight_core"].get("current_status") == "SOURCE_SHADOW_REDUCES_TO_BLOCK_AND_HIDDEN_RETURN", "current source-shadow ban reduces to no-Hom/return gap"),
        ("VAL4431_4_shadow_countermodel", shadow["SH4431_2_wA_countermodel_survives"].get("current_status") == "SOURCE_SHADOW_COUNTERMODEL_SURVIVES", "weighted-action countermodel remains live"),
        ("VAL4431_5_nonhilbert_contract", nonhilbert["NH4431_0_exact_nonHilbert_zero_contract"].get("current_status") == "NONHILBERT_BYPASS_ZERO_CONTRACT_READY_NONCLAIM", "non-Hilbert zero theorem staged"),
        ("VAL4431_6_nonhilbert_residual", nonhilbert["NH4431_1_current_residual_retained"].get("current_status") == "NONHILBERT_RESIDUAL_ROW_RETAINED", "current non-Hilbert residual retained"),
        ("VAL4431_7_improvement_flux_open", nonhilbert["NH4431_2_improvement_exact_boundary_open"].get("current_status") == "NONHILBERT_EXACT_DIVERGENCE_BOUNDARY_OPEN", "exact improvement still needs compact flux zero"),
        ("VAL4431_8_k_contract", kproducts["K4431_0_K_m_shadow_contract"].get("current_status") == "DD_K_PRODUCT_CONTRACT_ONLY", "K_m_shadow*C_shadow contract staged"),
        ("VAL4431_9_k_bound_target", kproducts["K4431_1_K_m_shadow_bound_target"].get("current_status") == "DD_K_PRODUCT_BOUND_TARGET_ONLY", "K_m_shadow*C_shadow bound target staged"),
        ("VAL4431_10_no_claim_outputs", no_claims, "no output row is claim-ready"),
        ("VAL4431_11_claim_gate_no_claim", any(row["gate_id"] == "CG4431_7_no_claim_outputs" and row["passed"] == "True" for row in gates), "claim gate explicitly blocks public claim"),
        ("VAL4431_12_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-272"),
        ("VAL4431_13_formal_doc", paths["formal"].exists() and MARKER in text(paths["formal"]), "formal doc exists with marker"),
        ("VAL4431_14_post_doc", paths["post"].exists() and "Private checkpoint" in text(paths["post"]), "post checkpoint doc exists"),
        ("VAL4431_15_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4431_16_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4431_17_next_target", paths["next"].exists() and NEXT_TARGET in text(paths["next"]), "next target file exists"),
        ("VAL4431_18_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": bool(passed), "detail": detail} for check_id, passed, detail in checks]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(DERIVATION_ROWS, derivation_rows())
    write_csv(SHADOW_INPUT, shadow_input_rows())
    write_csv(SHADOW_OUTPUT, evaluate_shadow_rows(SHADOW_INPUT))
    write_csv(NONHILBERT_INPUT, nonhilbert_input_rows())
    write_csv(NONHILBERT_OUTPUT, evaluate_nonhilbert_rows(NONHILBERT_INPUT))
    write_csv(KPRODUCT_INPUT, kproduct_input_rows())
    write_csv(KPRODUCT_OUTPUT, evaluate_kproduct_rows(KPRODUCT_INPUT))
    shadow = rows_from(SHADOW_OUTPUT)
    nonhilbert = rows_from(NONHILBERT_OUTPUT)
    kproducts = rows_from(KPRODUCT_OUTPUT)
    gates = claim_gate_rows(shadow, nonhilbert, kproducts)
    write_csv(CLAIM_GATES, gates)
    write_csv(DECISION_CSV, decision_rows())
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    write_text(FORMAL_PATH, build_doc(rows_from(SOURCE_REGISTER), shadow, nonhilbert, kproducts, gates))
    write_text(DOC_PATH, post_doc())
    update_claims_register()
    write_spine_and_packet()
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    write_csv(VALIDATION_PATH, validation_rows({"formal": FORMAL_PATH, "post": DOC_PATH, "next": NEXT_CSV}))


if __name__ == "__main__":
    main()

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

from hbar_measure_graph_gate import (  # noqa: E402
    evaluate_connected_graph_rows,
    evaluate_hbar_owner_rows,
    evaluate_k_action_value_rows,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4434"
CLAIM_ID = "L-275"
MARKER = "PPC4161_PARENT_HBAR_MEASURE_OWNER_AND_CONNECTED_MATTER_CERTIFICATE_OR_KMACTIONSCALE_VALUE_4434"
PACKET_MARKER = "PPC4161_PACKET_PARENT_HBAR_MEASURE_OWNER_AND_CONNECTED_MATTER_CERTIFICATE_OR_KMACTIONSCALE_VALUE_4434"
DECISION = "TWO_LOCK_ACTION_SCALE_ZERO_THEOREM_EXACT_HBAR_MEASURE_AND_PARENT_GRAPH_CERTIFICATES_UNSIGNED"
NEXT_TARGET = "4435-Y5-R2FR-parent-owned-action-density-graph-edge-certificate-or-first-Kmactionscale-source-leg.md"

FORMAL_PATH = FORMAL / "450-PPC4161-parent-hbar-measure-owner-and-connected-matter-certificate-or-Kmactionscale-value.md"
DOC_PATH = POST / "4434-Y5-R2FR-parent-hbar-measure-owner-and-connected-matter-certificate-or-Kmactionscale-value.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4434_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4434_SOURCE_REGISTER.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4434_DERIVATION_ROWS.csv"
HBAR_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4434_HBAR_MEASURE_OWNER_INPUT.csv"
HBAR_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4434_HBAR_MEASURE_OWNER_OUTPUT.csv"
GRAPH_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4434_CONNECTED_GRAPH_INPUT.csv"
GRAPH_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4434_CONNECTED_GRAPH_OUTPUT.csv"
K_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4434_K_ACTION_SCALE_VALUE_INPUT.csv"
K_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4434_K_ACTION_SCALE_VALUE_OUTPUT.csv"
EDGE_QUEUE = SOURCE_DIR / "P8_Y5_R2FR_4434_EDGE_CERTIFICATE_QUEUE.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4434_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4434_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4434_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4434_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "hbar_measure_graph_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4434_parent_hbar_measure_owner_and_connected_matter_certificate_or_Kmactionscale_value.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4433 = SOURCE_DIR / "P8_Y5_R2FR_4433_NEXT_TARGET.csv"
FORMAL_449 = FORMAL / "449-PPC4161-action-scale-constant-sector-universality-or-Kmactionscale-first-value.md"
OWNER4433 = SOURCE_DIR / "P8_Y5_R2FR_4433_ACTION_SCALE_OWNER_OUTPUT.csv"
K4433 = SOURCE_DIR / "P8_Y5_R2FR_4433_K_ACTION_SCALE_OUTPUT.csv"
HMO4422 = SOURCE_DIR / "P8_Y5_R2FR_4422_HBAR_MEASURE_OWNER_OUTPUT.csv"
CMC1905 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1905_CONNECTED_MATTER_CATEGORY_ATTEMPT.csv"
OMC2616 = SOURCE_DIR / "P8_Y5_EXCHANGE_GRAPH_GATE_2616_ORDINARY_MATTER_EXCHANGE_CONNECTIVITY_THEOREM.csv"
SMG1907 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1907_STANDARD_MATTER_EXCHANGE_GRAPH_SOURCE_BACKED_ATTEMPT.csv"
GRC1477 = SOURCE_DIR / "P8_Y5_R10_1477_CONNECTED_MATTER_GRAPH_CERTIFICATE.csv"
EDGES1477 = SOURCE_DIR / "P8_Y5_R10_1477_CONNECTED_MATTER_GRAPH_EDGES.csv"
NODES1477 = SOURCE_DIR / "P8_Y5_R10_1477_CONNECTED_MATTER_GRAPH_NODES.csv"
CON1464 = SOURCE_DIR / "P8_Y5_R10_1464_CONNECTED_MATTER_CATEGORY_PROOF_ATTEMPT.csv"
SOURCE_WEIGHTS = SOURCE_DIR / "P8_Y5_NO_SHADOW_2508_SOURCE_WEIGHT_RESIDUAL_ROWS.csv"
COUNTERMODELS = SOURCE_DIR / "P8_Y5_NO_SHADOW_2508_SOURCE_ONLY_COUNTERMODELS.csv"

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
        {"source_id": "SRC4434_00_4433_next", "path": NEXT_4433, "needle": "hbar/measure ownership", "role": "4433 handoff."},
        {"source_id": "SRC4434_01_449_formal", "path": FORMAL_449, "needle": "ASU4433_0_connected_naturality_common_mode_theorem", "role": "4433 connected naturality theorem."},
        {"source_id": "SRC4434_02_owner4433", "path": OWNER4433, "needle": "ASO4433_1_current_hbar_measure_gap", "role": "current action-scale owner gap."},
        {"source_id": "SRC4434_03_k4433", "path": K4433, "needle": "KAS4433_1_relative_action_scale_contract", "role": "relative K action-scale target."},
        {"source_id": "SRC4434_04_hmo4422", "path": HMO4422, "needle": "HMO4422_3_future_universal_hbar_measure_contract", "role": "hbar/measure future contract."},
        {"source_id": "SRC4434_05_cmc1905", "path": CMC1905, "needle": "CMC1905_1_naturality", "role": "connected naturality collapse."},
        {"source_id": "SRC4434_06_omc2616", "path": OMC2616, "needle": "OMC2616_1_connected_graph_implication", "role": "connected graph implication."},
        {"source_id": "SRC4434_07_smg1907", "path": SMG1907, "needle": "SMG1907_6_verdict", "role": "source-backed graph attempt."},
        {"source_id": "SRC4434_08_grc1477", "path": GRC1477, "needle": "GRC1477_1_parent_owned_connectivity", "role": "parent-owned connectivity certificate."},
        {"source_id": "SRC4434_09_edges1477", "path": EDGES1477, "needle": "E1477_4_lepton_EM", "role": "template edge queue."},
        {"source_id": "SRC4434_10_nodes1477", "path": NODES1477, "needle": "N1477_0_L_parent", "role": "graph node inventory."},
        {"source_id": "SRC4434_11_con1464", "path": CON1464, "needle": "CON1464_1_naturality_lemma", "role": "category proof attempt."},
        {"source_id": "SRC4434_12_source_weights", "path": SOURCE_WEIGHTS, "needle": "RSW2508_3", "role": "action-scale residual row."},
        {"source_id": "SRC4434_13_countermodels", "path": COUNTERMODELS, "needle": "CM2508_5_action_scale", "role": "action-scale countermodel."},
        {"source_id": "SRC4434_14_gate", "path": GATE_PATH, "needle": "def evaluate_hbar_owner_row", "role": "4434 gate script."},
        {"source_id": "SRC4434_15_generator", "path": GENERATOR_PATH, "needle": "CHECKPOINT = \"4434\"", "role": "4434 generator script."},
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
            "derivation_id": "HMGC4434_0_two_lock_zero_theorem",
            "claim": "Relative action-scale weights vanish if hbar/measure ownership and parent-owned connected matter graph both close.",
            "derivation": "Lock 1: one parent action phase, hbar_parent, path/statistical measure, species-blind Jacobian, action-density owner, Hilbert/current owner and variation-before-readout fix the ordinary matter action-density functor. Lock 2: the parent-owned ordinary matter graph is connected by nonzero action-density/source morphisms. Then connected naturality propagates w_A=w_*; the derivative-silent common w_* is measured-G calibration, so delta_w_A=0 in local differential channels.",
            "consequence": "This is a clean route to kill the relative action-scale source-coupling channel without fitting it.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "HMGC4434_1_current_hbar_gap",
            "claim": "Current MTS has a phase-line seed but not hbar/measure/Jacobian ownership.",
            "derivation": "4422 supplies a useful single-phase seed and a future hbar/measure owner contract, but universal hbar_parent, common path measure, species-blind measure Jacobian and no hbar_A are not parent-signed in current evidence.",
            "consequence": "Classical EOM scaling remains disallowed as a proof shortcut.",
            "status": "HBAR_MEASURE_OWNER_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "HMGC4434_2_current_graph_gap",
            "claim": "Current matter graph is physically connected but not parent-owned.",
            "derivation": "1477/1905 give a connected physical template for ordinary lab matter and an exact naturality lemma. But graph edges are template edges, not parent-owned nonzero action-density/source morphisms; material projections and decoupled-sector inventory are not complete.",
            "consequence": "Connectedness is a sharp target, not a claim-grade certificate.",
            "status": "CONNECTED_GRAPH_PARENT_EDGES_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "HMGC4434_3_first_edge_queue",
            "claim": "The next proof step is one parent-owned action-density graph edge certificate.",
            "derivation": "A graph certificate can be built edge-by-edge. The queue starts with single L_matter parent line edges and the electron-photon minimal coupling edge because they are direct action-density morphism candidates; material/coarse-graining edges come later.",
            "consequence": "This turns the proof route into concrete parent-edge rows instead of another abstract connectedness appeal.",
            "status": "EDGE_CERTIFICATE_QUEUE_STAGED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "KAS4434_0_no_numeric_action_scale_value",
            "claim": "No parent-owned numeric K_m_action_scale*C_action_scale value exists yet.",
            "derivation": f"The existing target remains abs(K_m_action_scale*C_action_scale_relative)<={D_MHAT_ONE_CHANNEL_CEILING:.12e} or {DELTA_Q_MHAT:.5f}*abs(K_m_action_scale*C_action_scale_relative)<={ETA_BOUND:.12e}. It is a bound/acquisition target and cannot define the theory coefficient.",
            "consequence": "If the proof route fails, the first empirical row needs a source leg and parent coefficient provenance, not a fitted value.",
            "status": "BOUND_TARGET_ONLY_VALUE_MISSING",
            "valid_for_claim": False,
        },
    ]


def hbar_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "HMO4434_0_future_owner_contract",
            "clause": "future universal hbar/measure owner contract",
            "single_phase_line": True,
            "universal_hbar_parent": True,
            "common_path_measure": True,
            "species_blind_jacobian": True,
            "ordinary_same_phase_bundle": True,
            "no_species_hbar_A": True,
            "action_density_owner": True,
            "current_owner": True,
            "variation_before_readout": True,
            "source_path": str(HMO4422),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Exact owner contract only; parent action has not signed it.",
        },
        {
            "row_id": "HMO4434_1_current_phase_seed",
            "clause": "current MTS time-flow phase seed",
            "single_phase_line": True,
            "universal_hbar_parent": False,
            "common_path_measure": False,
            "species_blind_jacobian": False,
            "ordinary_same_phase_bundle": False,
            "no_species_hbar_A": False,
            "action_density_owner": False,
            "current_owner": False,
            "variation_before_readout": False,
            "source_path": str(HMO4422),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Phase seed is real but does not close hbar/measure ownership.",
        },
        {
            "row_id": "HMO4434_2_hbar_measure_gap",
            "clause": "prior hbar/measure owner gap",
            "single_phase_line": True,
            "universal_hbar_parent": False,
            "common_path_measure": False,
            "species_blind_jacobian": False,
            "ordinary_same_phase_bundle": True,
            "no_species_hbar_A": False,
            "action_density_owner": False,
            "current_owner": False,
            "variation_before_readout": False,
            "source_path": str(HMO4422),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Prior audit names this exact gap.",
        },
        {
            "row_id": "HMO4434_3_hypothetical_owner_graph_needed",
            "clause": "hypothetical owner still needs graph/local route",
            "single_phase_line": True,
            "universal_hbar_parent": True,
            "common_path_measure": True,
            "species_blind_jacobian": True,
            "ordinary_same_phase_bundle": True,
            "no_species_hbar_A": True,
            "action_density_owner": True,
            "current_owner": True,
            "variation_before_readout": True,
            "source_path": str(HMO4422),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Even if owner closes, connected graph and local tau/R_eq route still need signatures.",
        },
    ]


def graph_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "GRC4434_0_connected_graph_contract",
            "clause": "parent-owned connected ordinary matter graph contract",
            "nodes_declared": True,
            "template_connected": True,
            "parent_owned_edges": True,
            "nonzero_morphisms": True,
            "action_density_functor_owned": True,
            "source_label_forgetting": True,
            "material_projection_sourced": True,
            "decoupled_inventory_closed": True,
            "source_path": str(CMC1905),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Exact graph certificate target; nonclaim until edges/material/inventory are signed.",
        },
        {
            "row_id": "GRC4434_1_physical_template",
            "clause": "physical ordinary matter template",
            "nodes_declared": True,
            "template_connected": True,
            "parent_owned_edges": False,
            "nonzero_morphisms": False,
            "action_density_functor_owned": False,
            "source_label_forgetting": True,
            "material_projection_sourced": False,
            "decoupled_inventory_closed": False,
            "source_path": str(GRC1477),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Connected as physics template, not parent-owned proof.",
        },
        {
            "row_id": "GRC4434_2_edge_rows_not_parent_signed",
            "clause": "edge row inventory",
            "nodes_declared": True,
            "template_connected": True,
            "parent_owned_edges": False,
            "nonzero_morphisms": False,
            "action_density_functor_owned": False,
            "source_label_forgetting": True,
            "material_projection_sourced": False,
            "decoupled_inventory_closed": False,
            "source_path": str(EDGES1477),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "All candidate edges are physical templates with parent_owned=false.",
        },
        {
            "row_id": "GRC4434_3_source_backed_graph_gap",
            "clause": "source-backed graph extraction",
            "nodes_declared": True,
            "template_connected": True,
            "parent_owned_edges": False,
            "nonzero_morphisms": False,
            "action_density_functor_owned": False,
            "source_label_forgetting": True,
            "material_projection_sourced": False,
            "decoupled_inventory_closed": False,
            "source_path": str(SMG1907),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Source candidates exist but component rows/material projection are not extracted.",
        },
    ]


def k_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "KAS4434_0_common_calibration_nonclaim",
            "product": "K_m_action_scale*C_action_scale_common",
            "value": "COMMON_CALIBRATION_ONLY",
            "units": "dimensionless",
            "parent_coefficient_source": "NSP1765_common_prefactor_absorption",
            "source_leg": "not_applicable_common_G_calibration",
            "projection": "common derivative-silent action scale has zero Ti/Pt differential projection",
            "bound_value": f"{D_MHAT_ONE_CHANNEL_CEILING:.12e}",
            "no_bound_inversion_guard": True,
            "source_path": str(K4433),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Calibration-only row remains nonclaim until owner/graph are signed.",
        },
        {
            "row_id": "KAS4434_1_relative_action_scale_contract",
            "product": "K_m_action_scale*C_action_scale_relative",
            "value": "MISSING_PARENT_COEFFICIENT",
            "units": "dimensionless",
            "parent_coefficient_source": "MISSING_ACTION_SCALE_PARENT_SOURCE",
            "source_leg": "MISSING_ACTION_SCALE_SOURCE_LEG",
            "projection": f"{DELTA_Q_MHAT:.5f}*abs(K_m_action_scale*C_action_scale_relative) <= {ETA_BOUND:.12e}",
            "bound_value": f"{D_MHAT_ONE_CHANNEL_CEILING:.12e}",
            "no_bound_inversion_guard": True,
            "source_path": str(K4433),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "First finite action-scale product if proof route remains unsigned.",
        },
        {
            "row_id": "KAS4434_2_bound_target_only",
            "product": "K_m_action_scale*C_action_scale_effective",
            "value": f"BOUND_ONLY_{D_MHAT_ONE_CHANNEL_CEILING:.12e}",
            "units": "dimensionless",
            "parent_coefficient_source": "MISSING_PARENT_SOURCE",
            "source_leg": "MISSING_SOURCE_LEG",
            "projection": f"abs(K_m_action_scale*C_action_scale_effective) <= {D_MHAT_ONE_CHANNEL_CEILING:.12e} only as one-channel target",
            "bound_value": f"{D_MHAT_ONE_CHANNEL_CEILING:.12e}",
            "no_bound_inversion_guard": True,
            "source_path": str(K4433),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "No bound inversion; not a theory value.",
        },
    ]


def edge_queue_rows() -> List[Dict[str, object]]:
    return [
        {"queue_id": "EQ4434_0_single_L_to_EM", "edge": "L_parent -> photon/EM", "why_first": "direct parent action-density/gauge field edge; simpler than composite material projection", "needed_signature": "single parent L_matter/gauge action term and source-current morphism", "source_path": str(EDGES1477), "valid_for_claim": False},
        {"queue_id": "EQ4434_1_single_L_to_lepton", "edge": "L_parent -> electron/lepton", "why_first": "direct ordinary matter action-density line edge", "needed_signature": "single parent L_matter term with no species action prefactor", "source_path": str(EDGES1477), "valid_for_claim": False},
        {"queue_id": "EQ4434_2_lepton_EM", "edge": "electron/lepton -> photon/EM", "why_first": "minimal coupling is the cleanest physical interaction morphism candidate", "needed_signature": "parent-owned gauge-current morphism and nonzero coupling", "source_path": str(EDGES1477), "valid_for_claim": False},
        {"queue_id": "EQ4434_3_quark_gluon", "edge": "quark -> gluon/QCD", "why_first": "connects dominant hadronic mass/binding sector", "needed_signature": "parent-owned QCD current/action-density morphism", "source_path": str(EDGES1477), "valid_for_claim": False},
        {"queue_id": "EQ4434_4_material_projection", "edge": "atom -> macroscopic test body", "why_first": "needed before Ti/Pt source claim; not first because it requires material fractions", "needed_signature": "sourced isotope/alloy/binding/material projection tensor", "source_path": str(SMG1907), "valid_for_claim": False},
    ]


def claim_gate_rows(hbar: Sequence[Mapping[str, str]], graph: Sequence[Mapping[str, str]], kvalues: Sequence[Mapping[str, str]]) -> List[Dict[str, object]]:
    hbar_rows = {row["row_id"]: row for row in hbar}
    graph_rows = {row["row_id"]: row for row in graph}
    k_rows = {row["row_id"]: row for row in kvalues}
    no_claims = not any(row.get("valid_for_claim") == "True" for row in hbar) and not any(row.get("valid_for_claim") == "True" for row in graph) and not any(row.get("valid_for_claim") == "True" for row in kvalues)
    return [
        {"gate_id": "CG4434_0_hbar_contract", "claim": "hbar/measure owner contract staged", "passed": hbar_rows["HMO4434_0_future_owner_contract"].get("current_status") == "HBAR_MEASURE_OWNER_CONTRACT_READY_NONCLAIM", "valid_for_claim": False, "detail": "Exact but parent unsigned."},
        {"gate_id": "CG4434_1_phase_seed_only", "claim": "current phase seed does not close owner", "passed": hbar_rows["HMO4434_1_current_phase_seed"].get("current_status") == "HBAR_MEASURE_OWNER_PHASE_SEED_ONLY", "valid_for_claim": False, "detail": "Single phase line is useful but insufficient."},
        {"gate_id": "CG4434_2_hbar_gap", "claim": "hbar/measure/Jacobian gap remains open", "passed": hbar_rows["HMO4434_2_hbar_measure_gap"].get("current_status") == "HBAR_MEASURE_OWNER_HBAR_MEASURE_JACOBIAN_OPEN", "valid_for_claim": False, "detail": "Blocks action-scale zero claim."},
        {"gate_id": "CG4434_3_graph_contract", "claim": "connected graph certificate staged", "passed": graph_rows["GRC4434_0_connected_graph_contract"].get("current_status") == "CONNECTED_GRAPH_CERTIFICATE_CONTRACT_READY_NONCLAIM", "valid_for_claim": False, "detail": "Exact but edges/material/inventory unsigned."},
        {"gate_id": "CG4434_4_template_only", "claim": "physical template is not parent certificate", "passed": graph_rows["GRC4434_1_physical_template"].get("current_status") == "CONNECTED_GRAPH_CERTIFICATE_PARENT_EDGES_MISSING", "valid_for_claim": False, "detail": "Template connectedness is not enough."},
        {"gate_id": "CG4434_5_edge_gap", "claim": "edge rows remain parent-unsigned", "passed": graph_rows["GRC4434_2_edge_rows_not_parent_signed"].get("current_status") == "CONNECTED_GRAPH_CERTIFICATE_PARENT_EDGES_MISSING", "valid_for_claim": False, "detail": "Need parent-owned nonzero morphism certificate."},
        {"gate_id": "CG4434_6_k_common_nonclaim", "claim": "common action-scale row remains nonclaim", "passed": k_rows["KAS4434_0_common_calibration_nonclaim"].get("current_status") == "K_ACTION_VALUE_INPUT_INVALID_NONCLAIM", "valid_for_claim": False, "detail": "Owner/graph unsigned."},
        {"gate_id": "CG4434_7_k_relative_contract", "claim": "relative action-scale product contract staged", "passed": k_rows["KAS4434_1_relative_action_scale_contract"].get("current_status") == "K_ACTION_VALUE_CONTRACT_ONLY", "valid_for_claim": False, "detail": "Missing parent coefficient and source leg."},
        {"gate_id": "CG4434_8_k_bound_only", "claim": "effective action-scale target remains bound-only", "passed": k_rows["KAS4434_2_bound_target_only"].get("current_status") == "K_ACTION_VALUE_BOUND_TARGET_ONLY", "valid_for_claim": False, "detail": "No bound inversion."},
        {"gate_id": "CG4434_9_edge_queue", "claim": "edge certificate queue written", "passed": len(edge_queue_rows()) == 5, "valid_for_claim": False, "detail": "Next route has concrete graph edges."},
        {"gate_id": "CG4434_10_no_claim_outputs", "claim": "4434 emits no local-GR/WEP/PPN/R10 claim", "passed": no_claims, "valid_for_claim": False, "detail": "All rows remain private nonclaim rows."},
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4434_0",
            "decision": DECISION,
            "summary": "4434 establishes the exact two-lock theorem for relative action-scale zero: one universal hbar/measure/Jacobian/action-density/current owner plus a parent-owned connected ordinary matter graph. Current MTS has a phase-line seed and a connected physical graph template, but neither lock is parent-signed. The finite K_m_action_scale*C_action_scale route remains bound-only until a parent coefficient and source leg are supplied. The next proof task is one parent-owned graph edge certificate, starting with direct action-density/gauge edges.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "public_claim": False,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {"status_id": "STAT4434_0_theorem", "status": "TWO_LOCK_ACTION_SCALE_ZERO_THEOREM_EXACT_CONDITIONAL", "detail": "hbar/measure owner plus parent-owned connected graph collapses relative weights to common calibration.", "valid_for_claim": False},
        {"status_id": "STAT4434_1_hbar", "status": "HBAR_MEASURE_OWNER_UNSIGNED", "detail": "single phase seed exists, but hbar_parent/path measure/species-blind Jacobian/no hbar_A are not parent-signed.", "valid_for_claim": False},
        {"status_id": "STAT4434_2_graph", "status": "PHYSICAL_GRAPH_CONNECTED_PARENT_EDGES_UNSIGNED", "detail": "ordinary matter graph is a connected template, not a claim-grade parent-owned certificate.", "valid_for_claim": False},
        {"status_id": "STAT4434_3_k", "status": "NO_PARENT_NUMERIC_K_ACTION_SCALE_VALUE_FOUND", "detail": f"relative action-scale target remains abs(K_m_action_scale*C_action_scale)<={D_MHAT_ONE_CHANNEL_CEILING:.12e}.", "valid_for_claim": False},
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4434_0",
            "target": NEXT_TARGET,
            "objective": "Either certify one parent-owned nonzero action-density graph edge, or fill the first K_m_action_scale source leg.",
            "derive_first": "turn one physical template edge such as L_parent->EM or electron->EM into a parent-owned nonzero action-density/source morphism with source path and no species prefactor.",
            "fallback": "fill K_m_action_scale*C_action_scale_relative with numeric parent coefficient, source leg, units, Ti/Pt projection, and no-bound-inversion guard.",
            "avoid": "counting physical graph templates as parent-owned proof; using classical EOM scaling; using MICROSCOPE bound to define the theory coefficient.",
            "valid_for_claim": False,
        }
    ]


def build_doc(sources: Sequence[Mapping[str, object]], hbar: Sequence[Mapping[str, str]], graph: Sequence[Mapping[str, str]], kvalues: Sequence[Mapping[str, str]], gates: Sequence[Mapping[str, object]]) -> str:
    return f"""# 450 PPC4161 parent hbar-measure owner and connected matter certificate or Kmactionscale value

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4434 turns the action-scale survivor into a two-lock theorem:

- Lock 1: one parent phase, `hbar_parent`, path/statistical measure, species-blind Jacobian, action-density owner, current owner and variation-before-readout.
- Lock 2: a parent-owned connected ordinary matter graph with nonzero action-density/source morphisms.
- If both locks close, connected naturality gives `w_A=w_*`; derivative-silent `w_*` is measured-`G/kappa` calibration, so relative action-scale leakage vanishes.
- Current MTS has a single-phase seed and a physically connected ordinary-matter template, but hbar/measure ownership and parent-owned graph edges are unsigned.
- No numeric parent-owned `K_m_action_scale*C_action_scale` value exists; the target remains `abs(K_m_action_scale*C_action_scale)<={D_MHAT_ONE_CHANNEL_CEILING:.12e}`.

## Source Register

{table(sources)}

## Derivation Rows

{table(derivation_rows())}

## Hbar-Measure Owner Gate

{table(hbar)}

## Connected Graph Gate

{table(graph)}

## K Action-Scale Value Gate

{table(kvalues)}

## Edge Certificate Queue

{table(edge_queue_rows())}

## Claim Gates

{table(gates)}

## Decision

{table(decision_rows())}

## Next Target

{table(next_rows())}
"""


def post_doc() -> str:
    return f"""# 4434 - parent hbar-measure owner and connected matter certificate or Kmactionscale value

Marker: `{MARKER}`

Private checkpoint generated at `{STAMP}`.

## What changed

- Wrote the exact two-lock theorem for relative action-scale zero.
- Kept the theorem nonclaim because hbar/measure ownership and parent-owned graph edges are unsigned.
- Preserved the finite `K_m_action_scale*C_action_scale` branch as bound-only unless a parent coefficient/source leg is supplied.
- Added a concrete edge-certificate queue so the next derivation has real graph edges to attack.

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
        "claim": "4434 writes the exact two-lock theorem for relative action-scale zero: universal hbar/measure/Jacobian/action-density/current ownership plus a parent-owned connected ordinary matter graph. Current MTS has a phase-line seed and a physically connected template, but both parent signatures are unsigned. K_m_action_scale*C_action_scale remains a bound-only acquisition target.",
        "current_evidence": "4434 source register, derivation rows, hbar-measure owner output, connected graph output, K action-scale value output, edge queue, claim gates, decision, status, next target and validation CSV.",
        "status": "two_lock_action_scale_zero_theorem_exact_hbar_measure_and_parent_graph_certificates_unsigned",
        "next_test": "Certify one parent-owned nonzero action-density graph edge or fill the first K_m_action_scale source leg.",
        "key_risk": "Counting physical graph templates as parent-owned proof; using classical EOM scaling; using empirical bounds to define parent coefficients.",
        "sector": "local_gr",
        "evidence": "4434 source register, derivation rows, hbar-measure owner output, connected graph output, K action-scale value output, edge queue, claim gates, decision, status, next target and validation CSV.",
        "next_action": "Certify one parent-owned nonzero action-density graph edge or fill the first K_m_action_scale source leg.",
        "risk": "Counting physical graph templates as parent-owned proof; using classical EOM scaling; using empirical bounds to define parent coefficients.",
    }
    rows.append({name: new_row.get(name, "") for name in fieldnames})
    with CLAIMS_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_spine_and_packet() -> None:
    spine_section = f"""## 4434 local spine update: two-lock action-scale zero theorem

4434 makes the action-scale route precise. Relative action-scale leakage vanishes only when two locks close: a universal hbar/measure/Jacobian/action-density/current owner and a parent-owned connected ordinary matter graph. The current corpus has a single-phase seed and a physically connected graph template, but not claim-grade parent signatures. The next local-GR coupling proof is one parent-owned graph edge certificate, not a generic appeal to ordinary matter connectedness.
"""
    packet_section = f"""## 4434 packet update: parent graph edge queue

`{PACKET_MARKER}`

Private packet result: `K_m_action_scale*C_action_scale` remains bound-only. The best derivation route is now an edge certificate queue: start with direct parent action-density/gauge edges such as `L_parent -> EM` or electron-photon minimal coupling, then only later material projection edges.
"""
    upsert_marked_section(SPINE_PATH, MARKER, spine_section)
    upsert_marked_section(PACKET_PATH, PACKET_MARKER, packet_section)


def validation_rows(paths: Mapping[str, Path]) -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    hbar = {row["row_id"]: row for row in rows_from(HBAR_OUTPUT)}
    graph = {row["row_id"]: row for row in rows_from(GRAPH_OUTPUT)}
    kvalues = {row["row_id"]: row for row in rows_from(K_OUTPUT)}
    gates = rows_from(CLAIM_GATES)
    no_claims = not any(row.get("valid_for_claim") == "True" for row in hbar.values()) and not any(row.get("valid_for_claim") == "True" for row in graph.values()) and not any(row.get("valid_for_claim") == "True" for row in kvalues.values())
    checks = [
        ("VAL4434_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source path exists"),
        ("VAL4434_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited source needle is present"),
        ("VAL4434_2_hbar_contract", hbar["HMO4434_0_future_owner_contract"].get("current_status") == "HBAR_MEASURE_OWNER_CONTRACT_READY_NONCLAIM", "hbar/measure contract staged"),
        ("VAL4434_3_phase_seed_only", hbar["HMO4434_1_current_phase_seed"].get("current_status") == "HBAR_MEASURE_OWNER_PHASE_SEED_ONLY", "current phase seed does not close owner"),
        ("VAL4434_4_hbar_gap", hbar["HMO4434_2_hbar_measure_gap"].get("current_status") == "HBAR_MEASURE_OWNER_HBAR_MEASURE_JACOBIAN_OPEN", "hbar/measure/Jacobian gap open"),
        ("VAL4434_5_graph_contract", graph["GRC4434_0_connected_graph_contract"].get("current_status") == "CONNECTED_GRAPH_CERTIFICATE_CONTRACT_READY_NONCLAIM", "connected graph contract staged"),
        ("VAL4434_6_template_only", graph["GRC4434_1_physical_template"].get("current_status") == "CONNECTED_GRAPH_CERTIFICATE_PARENT_EDGES_MISSING", "physical template lacks parent edges"),
        ("VAL4434_7_edge_gap", graph["GRC4434_2_edge_rows_not_parent_signed"].get("current_status") == "CONNECTED_GRAPH_CERTIFICATE_PARENT_EDGES_MISSING", "edge rows parent unsigned"),
        ("VAL4434_8_k_common", kvalues["KAS4434_0_common_calibration_nonclaim"].get("current_status") == "K_ACTION_VALUE_INPUT_INVALID_NONCLAIM", "common K row nonclaim"),
        ("VAL4434_9_k_relative", kvalues["KAS4434_1_relative_action_scale_contract"].get("current_status") == "K_ACTION_VALUE_CONTRACT_ONLY", "relative K action-scale contract staged"),
        ("VAL4434_10_k_bound", kvalues["KAS4434_2_bound_target_only"].get("current_status") == "K_ACTION_VALUE_BOUND_TARGET_ONLY", "bound target retained"),
        ("VAL4434_11_edge_queue", len(rows_from(EDGE_QUEUE)) == 5 and "EQ4434_0_single_L_to_EM" in text(EDGE_QUEUE), "edge certificate queue written"),
        ("VAL4434_12_no_claim_outputs", no_claims, "no output row is claim-ready"),
        ("VAL4434_13_claim_gate_no_claim", any(row["gate_id"] == "CG4434_10_no_claim_outputs" and row["passed"] == "True" for row in gates), "claim gate explicitly blocks public claim"),
        ("VAL4434_14_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-275"),
        ("VAL4434_15_formal_doc", paths["formal"].exists() and MARKER in text(paths["formal"]), "formal doc exists with marker"),
        ("VAL4434_16_post_doc", paths["post"].exists() and "Private checkpoint" in text(paths["post"]), "post checkpoint doc exists"),
        ("VAL4434_17_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4434_18_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4434_19_next_target", paths["next"].exists() and NEXT_TARGET in text(paths["next"]), "next target file exists"),
        ("VAL4434_20_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": bool(passed), "detail": detail} for check_id, passed, detail in checks]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(DERIVATION_ROWS, derivation_rows())
    write_csv(HBAR_INPUT, hbar_input_rows())
    write_csv(HBAR_OUTPUT, evaluate_hbar_owner_rows(HBAR_INPUT))
    write_csv(GRAPH_INPUT, graph_input_rows())
    write_csv(GRAPH_OUTPUT, evaluate_connected_graph_rows(GRAPH_INPUT))
    write_csv(K_INPUT, k_input_rows())
    write_csv(K_OUTPUT, evaluate_k_action_value_rows(K_INPUT))
    write_csv(EDGE_QUEUE, edge_queue_rows())
    hbar = rows_from(HBAR_OUTPUT)
    graph = rows_from(GRAPH_OUTPUT)
    kvalues = rows_from(K_OUTPUT)
    gates = claim_gate_rows(hbar, graph, kvalues)
    write_csv(CLAIM_GATES, gates)
    write_csv(DECISION_CSV, decision_rows())
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    write_text(FORMAL_PATH, build_doc(rows_from(SOURCE_REGISTER), hbar, graph, kvalues, gates))
    write_text(DOC_PATH, post_doc())
    update_claims_register()
    write_spine_and_packet()
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    write_csv(VALIDATION_PATH, validation_rows({"formal": FORMAL_PATH, "post": DOC_PATH, "next": NEXT_CSV}))


if __name__ == "__main__":
    main()

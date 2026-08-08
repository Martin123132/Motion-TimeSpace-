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

from action_density_edge_gate import (  # noqa: E402
    evaluate_edge_rows,
    evaluate_k_source_leg_rows,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4435"
CLAIM_ID = "L-276"
MARKER = "PPC4161_PARENT_OWNED_ACTION_DENSITY_GRAPH_EDGE_CERTIFICATE_OR_FIRST_KMACTIONSCALE_SOURCE_LEG_4435"
PACKET_MARKER = "PPC4161_PACKET_PARENT_OWNED_ACTION_DENSITY_GRAPH_EDGE_CERTIFICATE_OR_FIRST_KMACTIONSCALE_SOURCE_LEG_4435"
DECISION = "FIRST_EDGE_CERTIFICATE_REDUCED_TO_VISIBLE_EM_ACTION_DOMAIN_PARENT_SIGNATURE_KMACTIONSCALE_SOURCE_LEG_STILL_MISSING"
NEXT_TARGET = "4436-Y5-R2FR-visible-EM-action-edge-parent-signature-or-Kmactionscale-source-leg.md"

FORMAL_PATH = FORMAL / "451-PPC4161-parent-owned-action-density-graph-edge-certificate-or-first-Kmactionscale-source-leg.md"
DOC_PATH = POST / "4435-Y5-R2FR-parent-owned-action-density-graph-edge-certificate-or-first-Kmactionscale-source-leg.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4435_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4435_SOURCE_REGISTER.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4435_DERIVATION_ROWS.csv"
EDGE_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4435_ACTION_DENSITY_EDGE_INPUT.csv"
EDGE_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4435_ACTION_DENSITY_EDGE_OUTPUT.csv"
KLEG_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4435_K_ACTION_SOURCE_LEG_INPUT.csv"
KLEG_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4435_K_ACTION_SOURCE_LEG_OUTPUT.csv"
EDGE_QUEUE_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4435_NEXT_EDGE_QUEUE.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4435_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4435_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4435_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4435_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "action_density_edge_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4435_parent_owned_action_density_graph_edge_certificate_or_first_Kmactionscale_source_leg.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4434 = SOURCE_DIR / "P8_Y5_R2FR_4434_NEXT_TARGET.csv"
FORMAL_450 = FORMAL / "450-PPC4161-parent-hbar-measure-owner-and-connected-matter-certificate-or-Kmactionscale-value.md"
EDGE_QUEUE4434 = SOURCE_DIR / "P8_Y5_R2FR_4434_EDGE_CERTIFICATE_QUEUE.csv"
GRAPH4434 = SOURCE_DIR / "P8_Y5_R2FR_4434_CONNECTED_GRAPH_OUTPUT.csv"
K4434 = SOURCE_DIR / "P8_Y5_R2FR_4434_K_ACTION_SCALE_VALUE_OUTPUT.csv"
EDGES1477 = SOURCE_DIR / "P8_Y5_R10_1477_CONNECTED_MATTER_GRAPH_EDGES.csv"
NODES1477 = SOURCE_DIR / "P8_Y5_R10_1477_CONNECTED_MATTER_GRAPH_NODES.csv"
VEM3505 = SOURCE_DIR / "P8_Y5_R2FR_3505_VISIBLE_EM_ACTION_DOMAIN_THEOREM.csv"
VEB3505 = SOURCE_DIR / "P8_EM_visible_action_domain_exhaustion_no_chiEM_bound_vector.csv"
UCSR3510 = SOURCE_DIR / "P8_EM_common_action_density_line_universal_source_scale.csv"
SOURCE_OWNER_ACTION = SOURCE_DIR / "P8_source_owner_parent_action_terms_CONTRACT.csv"
TNG1470 = SOURCE_DIR / "P8_Y5_R10_1470_TYPED_VISIBLE_ACTION_GRAMMAR_ATTEMPT.csv"
SMG1907 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1907_STANDARD_MATTER_EXCHANGE_GRAPH_SOURCE_BACKED_ATTEMPT.csv"
SOURCE_WEIGHTS = SOURCE_DIR / "P8_Y5_NO_SHADOW_2508_SOURCE_WEIGHT_RESIDUAL_ROWS.csv"

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
        {"source_id": "SRC4435_00_4434_next", "path": NEXT_4434, "needle": "action-density graph edge", "role": "4434 handoff."},
        {"source_id": "SRC4435_01_450_formal", "path": FORMAL_450, "needle": "HMGC4434_3_first_edge_queue", "role": "4434 edge queue derivation."},
        {"source_id": "SRC4435_02_edge_queue4434", "path": EDGE_QUEUE4434, "needle": "EQ4434_0_single_L_to_EM", "role": "first edge queue."},
        {"source_id": "SRC4435_03_graph4434", "path": GRAPH4434, "needle": "GRC4434_2_edge_rows_not_parent_signed", "role": "current graph edge gap."},
        {"source_id": "SRC4435_04_k4434", "path": K4434, "needle": "KAS4434_1_relative_action_scale_contract", "role": "fallback K source leg."},
        {"source_id": "SRC4435_05_edges1477", "path": EDGES1477, "needle": "E1477_1_L_to_EM", "role": "template L to EM edge."},
        {"source_id": "SRC4435_06_nodes1477", "path": NODES1477, "needle": "N1477_0_L_parent", "role": "node inventory."},
        {"source_id": "SRC4435_07_vem3505", "path": VEM3505, "needle": "VEM3505_0_target_domain", "role": "visible EM action-domain contract."},
        {"source_id": "SRC4435_08_veb3505", "path": VEB3505, "needle": "VEB3505_6_C_XF2", "role": "EM kinetic coefficient residual guard."},
        {"source_id": "SRC4435_09_ucsr3510", "path": UCSR3510, "needle": "UCSR3510_1_delta_w_species", "role": "EM common action-density scale status."},
        {"source_id": "SRC4435_10_source_owner_action", "path": SOURCE_OWNER_ACTION, "needle": "A6_selector_blind_source_action", "role": "source-owner parent action contract."},
        {"source_id": "SRC4435_11_tng1470", "path": TNG1470, "needle": "TNG1470_1_type_theorem", "role": "typed visible action grammar."},
        {"source_id": "SRC4435_12_smg1907", "path": SMG1907, "needle": "SMG1907_6_verdict", "role": "source-backed graph gap."},
        {"source_id": "SRC4435_13_source_weights", "path": SOURCE_WEIGHTS, "needle": "RSW2508_3", "role": "action-scale residual row."},
        {"source_id": "SRC4435_14_gate", "path": GATE_PATH, "needle": "def evaluate_edge_row", "role": "4435 gate script."},
        {"source_id": "SRC4435_15_generator", "path": GENERATOR_PATH, "needle": "CHECKPOINT = \"4435\"", "role": "4435 generator script."},
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
            "derivation_id": "EDGE4435_0_parent_edge_certificate_theorem",
            "claim": "One parent-owned action-density edge is certified by an action term plus a typed source/current morphism.",
            "derivation": "For an edge A->B in the ordinary matter graph, if a single parent action-density line contains a nonzero interaction or inclusion term coupling A and B, the action-density functor owns that term, the source/Hilbert current is varied before readout, and no species/action prefactor multiplies the edge, then the edge is a parent-owned nonzero morphism. Naturality can use that edge to propagate action-scale weights.",
            "consequence": "This is the atomic unit needed to turn the connected physical template into a parent graph certificate.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "EDGE4435_1_L_to_EM_reduction",
            "claim": "The first edge reduces to visible EM action-domain parent signature.",
            "derivation": "The visible EM action-domain theorem supplies the right conditional action term: S_EM=-1/4 int F_Q wedge *_obs F_Q + int A_Q J_Q. That supports the L_parent->EM edge only if this EM block is parent-owned, on the same action-density line, with fixed representation/current data and no hidden F^2/source prefactor.",
            "consequence": "The next proof lock is not generic connectedness; it is visible EM action-domain ownership/no-extra-F2.",
            "status": "REDUCED_TO_VISIBLE_EM_ACTION_DOMAIN_SIGNATURE",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "EDGE4435_2_template_not_certificate",
            "claim": "The existing edge rows are physical templates, not certificates.",
            "derivation": "1477 lists L_parent->EM and electron->EM candidate edges with template_edge_present=True, but parent_owned=False. They cannot be counted for the connected graph proof until parent ownership, nonzero morphism convention and action-density functor ownership are signed.",
            "consequence": "No local-GR/WEP/source-coupling claim is allowed from template connectedness.",
            "status": "PARENT_EDGE_SIGNATURE_MISSING",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "EDGE4435_3_source_backed_extraction_gap",
            "claim": "Source-backed graph extraction is still below claim grade.",
            "derivation": "1907 records source candidates for standard matter graph edges, but no extracted graph row defines the edge convention, material projection and arena inventory. That is useful sourcing groundwork, not a parent-owned graph proof.",
            "consequence": "The graph route needs edge extraction and parent action-domain signatures before scoring.",
            "status": "SOURCE_BACKED_EXTRACTION_MISSING",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "KLEG4435_0_source_leg_missing",
            "claim": "The first K_m_action_scale source leg is still missing.",
            "derivation": f"The finite fallback remains {DELTA_Q_MHAT:.5f}*abs(K_m_action_scale*C_action_scale_relative)<={ETA_BOUND:.12e}. Current rows give a bound target only; they do not provide a parent coefficient, source leg, or source-leg units. The empirical bound cannot define the coefficient.",
            "consequence": "If the EM edge signature route fails, the next empirical action is source-leg acquisition, not fitting from MICROSCOPE.",
            "status": "K_SOURCE_LEG_MISSING_BOUND_ONLY",
            "valid_for_claim": False,
        },
    ]


def edge_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "EDGE4435_0_exact_parent_edge_contract",
            "edge": "generic parent-owned A->B action-density edge",
            "source_node": "A",
            "target_node": "B",
            "template_edge_present": True,
            "visible_action_term_present": True,
            "same_parent_action_line": True,
            "parent_owned_morphism": True,
            "nonzero_coupling": True,
            "action_density_functor_owned": True,
            "source_current_owner": True,
            "no_species_prefactor": True,
            "source_path": str(FORMAL_450),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Exact future edge certificate; nonclaim until parent action signs it.",
        },
        {
            "row_id": "EDGE4435_1_L_parent_to_EM_visible_domain",
            "edge": "L_parent -> photon/EM",
            "source_node": "N1477_0_L_parent",
            "target_node": "N1477_2_photon_EM",
            "template_edge_present": True,
            "visible_action_term_present": True,
            "same_parent_action_line": False,
            "parent_owned_morphism": False,
            "nonzero_coupling": True,
            "action_density_functor_owned": False,
            "source_current_owner": True,
            "no_species_prefactor": True,
            "source_path": str(VEM3505),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Visible EM action has the right conditional grammar, but parent action-domain ownership is unsigned.",
        },
        {
            "row_id": "EDGE4435_2_L_parent_to_EM_template",
            "edge": "L_parent -> photon/EM",
            "source_node": "N1477_0_L_parent",
            "target_node": "N1477_2_photon_EM",
            "template_edge_present": True,
            "visible_action_term_present": False,
            "same_parent_action_line": False,
            "parent_owned_morphism": False,
            "nonzero_coupling": False,
            "action_density_functor_owned": False,
            "source_current_owner": False,
            "no_species_prefactor": False,
            "source_path": str(EDGES1477),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Physical template edge only.",
        },
        {
            "row_id": "EDGE4435_3_lepton_EM_template",
            "edge": "electron/lepton -> photon/EM",
            "source_node": "N1477_1_electron_lepton",
            "target_node": "N1477_2_photon_EM",
            "template_edge_present": True,
            "visible_action_term_present": False,
            "same_parent_action_line": False,
            "parent_owned_morphism": False,
            "nonzero_coupling": False,
            "action_density_functor_owned": False,
            "source_current_owner": False,
            "no_species_prefactor": False,
            "source_path": str(EDGES1477),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Minimal coupling is the right physical target, but no parent-owned morphism row exists.",
        },
        {
            "row_id": "EDGE4435_4_source_backed_extraction_gap",
            "edge": "standard matter source-backed graph",
            "source_node": "ordinary source components",
            "target_node": "Ti/Pt test-body graph",
            "template_edge_present": True,
            "visible_action_term_present": False,
            "same_parent_action_line": False,
            "parent_owned_morphism": False,
            "nonzero_coupling": False,
            "action_density_functor_owned": False,
            "source_current_owner": False,
            "no_species_prefactor": False,
            "source_path": str(SMG1907),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Source candidates exist; extracted component convention/material projection is missing.",
        },
    ]


def kleg_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "KLEG4435_0_relative_action_scale_source_leg_contract",
            "product": "K_m_action_scale*C_action_scale_relative",
            "coefficient_value": "MISSING_PARENT_COEFFICIENT",
            "units": "dimensionless",
            "parent_coefficient_source": "MISSING_ACTION_SCALE_PARENT_SOURCE",
            "source_leg": "MISSING_ACTION_SCALE_SOURCE_LEG",
            "source_leg_units": "dimensionless_or_declared_parent_units",
            "projection": f"{DELTA_Q_MHAT:.5f}*abs(K_m_action_scale*C_action_scale_relative) <= {ETA_BOUND:.12e}",
            "bound_value": f"{D_MHAT_ONE_CHANNEL_CEILING:.12e}",
            "no_bound_inversion_guard": True,
            "source_path": str(K4434),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Schema-ready finite fallback; missing coefficient and source leg.",
        },
        {
            "row_id": "KLEG4435_1_bound_target_only",
            "product": "K_m_action_scale*C_action_scale_effective",
            "coefficient_value": f"BOUND_ONLY_{D_MHAT_ONE_CHANNEL_CEILING:.12e}",
            "units": "dimensionless",
            "parent_coefficient_source": "MISSING_PARENT_SOURCE",
            "source_leg": "MISSING_SOURCE_LEG",
            "source_leg_units": "MISSING_SOURCE_LEG_UNITS",
            "projection": f"abs(K_m_action_scale*C_action_scale_effective) <= {D_MHAT_ONE_CHANNEL_CEILING:.12e} only as one-channel target",
            "bound_value": f"{D_MHAT_ONE_CHANNEL_CEILING:.12e}",
            "no_bound_inversion_guard": True,
            "source_path": str(K4434),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Bound target only; empirical bound cannot define theory coefficient.",
        },
        {
            "row_id": "KLEG4435_2_EM_action_scale_component",
            "product": "K_m_EM_action_scale*C_EM_action_scale",
            "coefficient_value": "MISSING_PARENT_COEFFICIENT",
            "units": "dimensionless",
            "parent_coefficient_source": "MISSING_VISIBLE_EM_ACTION_DOMAIN_PARENT_SIGNATURE",
            "source_leg": "MISSING_EM_BINDING_SOURCE_LEG",
            "source_leg_units": "dimensionless_or_binding_fraction",
            "projection": f"{DELTA_Q_MHAT:.5f}*abs(K_m_EM_action_scale*C_EM_action_scale) <= {ETA_BOUND:.12e}",
            "bound_value": f"{D_MHAT_ONE_CHANNEL_CEILING:.12e}",
            "no_bound_inversion_guard": True,
            "source_path": str(UCSR3510),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "EM-specific action-scale leg suggested by first edge route; still missing parent signature/source leg.",
        },
    ]


def next_edge_queue_rows() -> List[Dict[str, object]]:
    return [
        {"queue_id": "EQ4435_0_visible_EM_action_domain_signature", "target": "L_parent -> photon/EM", "needed_input": "parent-owned visible EM action domain: S_EM args only A_Q,F_Q,e_obs,rep/current constants; no independent F2/Hodge/source prefactor", "source_path": str(VEM3505), "valid_for_claim": False},
        {"queue_id": "EQ4435_1_no_extra_F2_prefactor", "target": "L_parent -> photon/EM", "needed_input": "unique F2/operator-domain theorem so EM kinetic action has no w_EM or hidden C_XF2 prefactor", "source_path": str(VEB3505), "valid_for_claim": False},
        {"queue_id": "EQ4435_2_source_current_owner", "target": "A_Q J_Q current", "needed_input": "Hilbert/Noether current owner and source-current descent before readout", "source_path": str(SOURCE_OWNER_ACTION), "valid_for_claim": False},
        {"queue_id": "EQ4435_3_lepton_EM_minimal_coupling", "target": "electron/lepton -> photon/EM", "needed_input": "parent-owned minimal coupling morphism with fixed representation charge and no species action prefactor", "source_path": str(EDGES1477), "valid_for_claim": False},
    ]


def claim_gate_rows(edges: Sequence[Mapping[str, str]], klegs: Sequence[Mapping[str, str]]) -> List[Dict[str, object]]:
    edge_rows = {row["row_id"]: row for row in edges}
    k_rows = {row["row_id"]: row for row in klegs}
    no_claims = not any(row.get("valid_for_claim") == "True" for row in edges) and not any(row.get("valid_for_claim") == "True" for row in klegs)
    return [
        {"gate_id": "CG4435_0_edge_contract", "claim": "generic parent-owned edge contract staged", "passed": edge_rows["EDGE4435_0_exact_parent_edge_contract"].get("current_status") == "ACTION_DENSITY_EDGE_CERTIFICATE_CONTRACT_READY_NONCLAIM", "valid_for_claim": False, "detail": "Exact but parent unsigned."},
        {"gate_id": "CG4435_1_visible_EM_reduction", "claim": "L_parent->EM reduces to visible EM action-domain signature", "passed": edge_rows["EDGE4435_1_L_parent_to_EM_visible_domain"].get("current_status") == "ACTION_DENSITY_EDGE_CONDITIONAL_ACTION_DOMAIN_PARENT_UNSIGNED", "valid_for_claim": False, "detail": "Right action grammar, but not parent-owned."},
        {"gate_id": "CG4435_2_template_not_certificate", "claim": "template edges remain non-certificates", "passed": edge_rows["EDGE4435_2_L_parent_to_EM_template"].get("current_status") == "ACTION_DENSITY_EDGE_PHYSICAL_TEMPLATE_PARENT_SIGNATURE_MISSING" and edge_rows["EDGE4435_3_lepton_EM_template"].get("current_status") == "ACTION_DENSITY_EDGE_PHYSICAL_TEMPLATE_PARENT_SIGNATURE_MISSING", "valid_for_claim": False, "detail": "Physical template rows cannot be counted as parent graph proof."},
        {"gate_id": "CG4435_3_source_backed_gap", "claim": "source-backed extraction remains missing", "passed": edge_rows["EDGE4435_4_source_backed_extraction_gap"].get("current_status") == "ACTION_DENSITY_EDGE_PHYSICAL_TEMPLATE_PARENT_SIGNATURE_MISSING", "valid_for_claim": False, "detail": "Source candidates not extracted into component/material rows."},
        {"gate_id": "CG4435_4_kleg_contract", "claim": "K_m_action_scale source-leg contract staged", "passed": k_rows["KLEG4435_0_relative_action_scale_source_leg_contract"].get("current_status") == "K_ACTION_SOURCE_LEG_CONTRACT_ONLY", "valid_for_claim": False, "detail": "Coefficient/source leg missing."},
        {"gate_id": "CG4435_5_kleg_bound_only", "claim": "bound-only row retained", "passed": k_rows["KLEG4435_1_bound_target_only"].get("current_status") == "K_ACTION_SOURCE_LEG_BOUND_TARGET_ONLY", "valid_for_claim": False, "detail": "No bound inversion."},
        {"gate_id": "CG4435_6_em_component_contract", "claim": "EM action-scale component row staged", "passed": k_rows["KLEG4435_2_EM_action_scale_component"].get("current_status") == "K_ACTION_SOURCE_LEG_CONTRACT_ONLY", "valid_for_claim": False, "detail": "EM source leg missing."},
        {"gate_id": "CG4435_7_next_queue", "claim": "next edge queue written", "passed": len(next_edge_queue_rows()) == 4, "valid_for_claim": False, "detail": "Next target has concrete EM signature locks."},
        {"gate_id": "CG4435_8_no_claim_outputs", "claim": "4435 emits no local-GR/WEP/PPN/R10 claim", "passed": no_claims, "valid_for_claim": False, "detail": "All rows remain private nonclaim rows."},
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4435_0",
            "decision": DECISION,
            "summary": "4435 attempts the first parent-owned ordinary-matter graph edge. The exact edge theorem is clean: a nonzero action-density/source morphism on one parent action line can count as a graph edge. The L_parent->EM edge has the right visible EM action-domain contract, but parent ownership, no-extra-F2/source-prefactor, action-density functor ownership and source-current descent are unsigned. Template edges remain non-certificates. The K_m_action_scale fallback is schema-ready but still lacks parent coefficient and source leg.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "public_claim": False,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {"status_id": "STAT4435_0_edge", "status": "FIRST_EDGE_REDUCED_TO_VISIBLE_EM_ACTION_DOMAIN_PARENT_SIGNATURE", "detail": "L_parent->EM can be the first edge if visible EM action domain is parent-owned and no extra F2/source prefactor exists.", "valid_for_claim": False},
        {"status_id": "STAT4435_1_template", "status": "PHYSICAL_TEMPLATE_EDGES_NOT_PARENT_CERTIFICATES", "detail": "1477 template edges stay nonclaim until parent_owned=true with source-current/action-density morphism.", "valid_for_claim": False},
        {"status_id": "STAT4435_2_kleg", "status": "K_ACTION_SCALE_SOURCE_LEG_MISSING", "detail": f"relative action-scale source leg remains bound-only with target {D_MHAT_ONE_CHANNEL_CEILING:.12e}.", "valid_for_claim": False},
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4435_0",
            "target": NEXT_TARGET,
            "objective": "Either parent-sign the visible EM action edge, or fill the first K_m_action_scale source leg.",
            "derive_first": "prove the visible EM action-domain is parent-owned on the same action-density line, with unique F2 coefficient, fixed current data, and no species/source prefactor.",
            "fallback": "fill K_m_action_scale*C_action_scale_relative or K_m_EM_action_scale*C_EM_action_scale with parent coefficient, source leg, units, projection, and no-bound-inversion guard.",
            "avoid": "counting EM template edges as parent-owned; ignoring independent F2/Hodge prefactors; using the Ti/Pt bound as coefficient source.",
            "valid_for_claim": False,
        }
    ]


def build_doc(sources: Sequence[Mapping[str, object]], edges: Sequence[Mapping[str, str]], klegs: Sequence[Mapping[str, str]], gates: Sequence[Mapping[str, object]]) -> str:
    return f"""# 451 PPC4161 parent-owned action-density graph edge certificate or first Kmactionscale source leg

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4435 attempts the first graph edge:

- A parent-owned graph edge is certified by a nonzero action-density/source morphism on one parent action line, with source current owned before readout and no species/action prefactor.
- The `L_parent -> photon/EM` edge has the right conditional action-domain shape from visible EM: `S_EM=-1/4 int F_Q wedge *_obs F_Q + int A_Q J_Q`.
- Current MTS does not yet parent-sign that EM action domain, nor does it close no-extra-`F^2`, Hodge/source-prefactor, current-owner and readout/radiative stability clauses.
- Existing EM/lepton graph edges are physical templates, not parent-owned certificates.
- The fallback `K_m_action_scale*C_action_scale` source leg remains missing and bound-only.

## Source Register

{table(sources)}

## Derivation Rows

{table(derivation_rows())}

## Action-Density Edge Gate

{table(edges)}

## K Action-Scale Source Leg Gate

{table(klegs)}

## Next Edge Queue

{table(next_edge_queue_rows())}

## Claim Gates

{table(gates)}

## Decision

{table(decision_rows())}

## Next Target

{table(next_rows())}
"""


def post_doc() -> str:
    return f"""# 4435 - parent-owned action-density graph edge certificate or first Kmactionscale source leg

Marker: `{MARKER}`

Private checkpoint generated at `{STAMP}`.

## What changed

- Tried to certify the first ordinary matter graph edge.
- Reduced `L_parent -> EM` to visible EM action-domain parent ownership plus no-extra-F2/source-prefactor.
- Kept template graph edges nonclaim.
- Kept `K_m_action_scale` fallback schema-ready but missing parent coefficient/source leg.

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
        "claim": "4435 reduces the first parent-owned graph-edge certificate to the visible EM action-domain parent signature. L_parent->EM has the right conditional action grammar, but parent ownership, unique F2/no-source-prefactor, current-owner and readout/radiative stability clauses are unsigned. Template edges remain non-certificates and K_m_action_scale*C_action_scale remains source-leg missing.",
        "current_evidence": "4435 source register, derivation rows, action-density edge output, K action-scale source-leg output, next edge queue, claim gates, decision, status, next target and validation CSV.",
        "status": "first_edge_certificate_reduced_to_visible_em_action_domain_parent_signature_kmactionscale_source_leg_still_missing",
        "next_test": "Parent-sign visible EM action edge or fill the first K_m_action_scale source leg.",
        "key_risk": "Counting template edges as parent-owned; ignoring independent F2/Hodge/source prefactors; using empirical bounds to define theory coefficients.",
        "sector": "local_gr",
        "evidence": "4435 source register, derivation rows, action-density edge output, K action-scale source-leg output, next edge queue, claim gates, decision, status, next target and validation CSV.",
        "next_action": "Parent-sign visible EM action edge or fill the first K_m_action_scale source leg.",
        "risk": "Counting template edges as parent-owned; ignoring independent F2/Hodge/source prefactors; using empirical bounds to define theory coefficients.",
    }
    rows.append({name: new_row.get(name, "") for name in fieldnames})
    with CLAIMS_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_spine_and_packet() -> None:
    spine_section = f"""## 4435 local spine update: first graph edge reduces to EM action ownership

4435 tries the first parent-owned matter graph edge. The `L_parent -> EM` edge is the best route because visible EM already has a precise conditional action-domain theorem. The missing parent signatures are now named: visible EM action ownership on the same action-density line, unique `F^2`/no source-prefactor, source-current owner, and readout/radiative stability. Template graph edges still do not count.
"""
    packet_section = f"""## 4435 packet update: visible EM edge is next

`{PACKET_MARKER}`

Private packet result: the connected graph proof now has a first edge target. Try to parent-sign `L_parent -> EM`; if that fails, fill `K_m_action_scale*C_action_scale` or the EM-specific source leg with real provenance rather than using the bound as a coefficient.
"""
    upsert_marked_section(SPINE_PATH, MARKER, spine_section)
    upsert_marked_section(PACKET_PATH, PACKET_MARKER, packet_section)


def validation_rows(paths: Mapping[str, Path]) -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    edges = {row["row_id"]: row for row in rows_from(EDGE_OUTPUT)}
    klegs = {row["row_id"]: row for row in rows_from(KLEG_OUTPUT)}
    gates = rows_from(CLAIM_GATES)
    no_claims = not any(row.get("valid_for_claim") == "True" for row in edges.values()) and not any(row.get("valid_for_claim") == "True" for row in klegs.values())
    checks = [
        ("VAL4435_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source path exists"),
        ("VAL4435_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited source needle is present"),
        ("VAL4435_2_edge_contract", edges["EDGE4435_0_exact_parent_edge_contract"].get("current_status") == "ACTION_DENSITY_EDGE_CERTIFICATE_CONTRACT_READY_NONCLAIM", "generic edge contract staged"),
        ("VAL4435_3_visible_EM_reduction", edges["EDGE4435_1_L_parent_to_EM_visible_domain"].get("current_status") == "ACTION_DENSITY_EDGE_CONDITIONAL_ACTION_DOMAIN_PARENT_UNSIGNED", "L_parent to EM reduced to visible action domain"),
        ("VAL4435_4_template_edges", edges["EDGE4435_2_L_parent_to_EM_template"].get("current_status") == "ACTION_DENSITY_EDGE_PHYSICAL_TEMPLATE_PARENT_SIGNATURE_MISSING" and edges["EDGE4435_3_lepton_EM_template"].get("current_status") == "ACTION_DENSITY_EDGE_PHYSICAL_TEMPLATE_PARENT_SIGNATURE_MISSING", "template edges remain non-certificates"),
        ("VAL4435_5_source_backed_gap", edges["EDGE4435_4_source_backed_extraction_gap"].get("current_status") == "ACTION_DENSITY_EDGE_PHYSICAL_TEMPLATE_PARENT_SIGNATURE_MISSING", "source-backed graph extraction still missing"),
        ("VAL4435_6_kleg_contract", klegs["KLEG4435_0_relative_action_scale_source_leg_contract"].get("current_status") == "K_ACTION_SOURCE_LEG_CONTRACT_ONLY", "K action-scale source leg contract staged"),
        ("VAL4435_7_kleg_bound", klegs["KLEG4435_1_bound_target_only"].get("current_status") == "K_ACTION_SOURCE_LEG_BOUND_TARGET_ONLY", "bound-only row retained"),
        ("VAL4435_8_em_component", klegs["KLEG4435_2_EM_action_scale_component"].get("current_status") == "K_ACTION_SOURCE_LEG_CONTRACT_ONLY", "EM component source leg staged"),
        ("VAL4435_9_next_edge_queue", len(rows_from(EDGE_QUEUE_NEXT)) == 4 and "EQ4435_0_visible_EM_action_domain_signature" in text(EDGE_QUEUE_NEXT), "next edge queue written"),
        ("VAL4435_10_no_claim_outputs", no_claims, "no output row is claim-ready"),
        ("VAL4435_11_claim_gate_no_claim", any(row["gate_id"] == "CG4435_8_no_claim_outputs" and row["passed"] == "True" for row in gates), "claim gate explicitly blocks public claim"),
        ("VAL4435_12_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-276"),
        ("VAL4435_13_formal_doc", paths["formal"].exists() and MARKER in text(paths["formal"]), "formal doc exists with marker"),
        ("VAL4435_14_post_doc", paths["post"].exists() and "Private checkpoint" in text(paths["post"]), "post checkpoint doc exists"),
        ("VAL4435_15_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4435_16_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4435_17_next_target", paths["next"].exists() and NEXT_TARGET in text(paths["next"]), "next target file exists"),
        ("VAL4435_18_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": bool(passed), "detail": detail} for check_id, passed, detail in checks]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(DERIVATION_ROWS, derivation_rows())
    write_csv(EDGE_INPUT, edge_input_rows())
    write_csv(EDGE_OUTPUT, evaluate_edge_rows(EDGE_INPUT))
    write_csv(KLEG_INPUT, kleg_input_rows())
    write_csv(KLEG_OUTPUT, evaluate_k_source_leg_rows(KLEG_INPUT))
    write_csv(EDGE_QUEUE_NEXT, next_edge_queue_rows())
    edges = rows_from(EDGE_OUTPUT)
    klegs = rows_from(KLEG_OUTPUT)
    gates = claim_gate_rows(edges, klegs)
    write_csv(CLAIM_GATES, gates)
    write_csv(DECISION_CSV, decision_rows())
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    write_text(FORMAL_PATH, build_doc(rows_from(SOURCE_REGISTER), edges, klegs, gates))
    write_text(DOC_PATH, post_doc())
    update_claims_register()
    write_spine_and_packet()
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    write_csv(VALIDATION_PATH, validation_rows({"formal": FORMAL_PATH, "post": DOC_PATH, "next": NEXT_CSV}))


if __name__ == "__main__":
    main()

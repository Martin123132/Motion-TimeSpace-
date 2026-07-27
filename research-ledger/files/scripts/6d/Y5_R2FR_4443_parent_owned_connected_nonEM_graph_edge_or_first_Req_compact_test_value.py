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

from nonem_graph_edge_gate import (  # noqa: E402
    evaluate_root_edge_rows,
    evaluate_species_edge_rows,
    evaluate_tail_rows,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4443"
CLAIM_ID = "L-284"
MARKER = "PPC4161_NONEM_HILBERT_STRESS_ROOT_EDGE_OR_REQ_COMPACT_TEST_4443"
PACKET_MARKER = "PPC4161_PACKET_NONEM_HILBERT_STRESS_ROOT_EDGE_4443"
DECISION = "NONEM_HILBERT_STRESS_ROOT_EDGE_SIGNED_STANDARD_LMATTER_BRANCH_SPECIES_GRAPH_AND_REQ_COMPACT_VALUE_REMAIN_NONCLAIM"
NEXT_TARGET = "4444-Y5-R2FR-standard-Lmatter-component-edge-expansion-or-Req-compact-test-value.md"

FORMAL_PATH = FORMAL / "459-PPC4161-parent-owned-connected-nonEM-graph-edge-or-first-Req-compact-test-value.md"
DOC_PATH = POST / "4443-Y5-R2FR-parent-owned-connected-nonEM-graph-edge-or-first-Req-compact-test-value.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4443_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4443_SOURCE_REGISTER.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4443_DERIVATION_ROWS.csv"
ROOT_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4443_NONEM_ROOT_EDGE_INPUT.csv"
ROOT_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4443_NONEM_ROOT_EDGE_OUTPUT.csv"
SPECIES_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4443_NONEM_SPECIES_EDGE_INPUT.csv"
SPECIES_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4443_NONEM_SPECIES_EDGE_OUTPUT.csv"
TAIL_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4443_REQ_COMPACT_TEST_TAIL_INPUT.csv"
TAIL_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4443_REQ_COMPACT_TEST_TAIL_OUTPUT.csv"
REDUCTION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4443_REDUCTION_ROWS.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4443_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4443_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4443_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4443_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "nonem_graph_edge_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4443_parent_owned_connected_nonEM_graph_edge_or_first_Req_compact_test_value.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4442 = SOURCE_DIR / "P8_Y5_R2FR_4442_NEXT_TARGET.csv"
FORMAL_458 = FORMAL / "458-PPC4161-nonEM-universal-hbar-measure-owner-proof-or-first-Req-Bzero-tail-value.md"
FORMAL_451 = FORMAL / "451-PPC4161-parent-owned-action-density-graph-edge-certificate-or-first-Kmactionscale-source-leg.md"
FORMAL_450 = FORMAL / "450-PPC4161-parent-hbar-measure-owner-and-connected-matter-certificate-or-Kmactionscale-value.md"
FORMAL_439 = FORMAL / "439-PPC4161-action-density-line-owner-or-first-source-backed-Pwep-Req-value.md"
FORMAL_436 = FORMAL / "436-PPC4161-parent-action-measure-current-owner-or-Req-moment-bound.md"
CORE_ACTION = ROOT / "core-mts-framework" / "action-principle" / "the-motion-timespace-action-principle.md"
FUND_ACTION = ROOT / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md"
EDGE_TEMPLATE = SOURCE_DIR / "P8_Y5_R10_1477_CONNECTED_MATTER_GRAPH_EDGES.csv"
NODE_TEMPLATE = SOURCE_DIR / "P8_Y5_R10_1477_CONNECTED_MATTER_GRAPH_NODES.csv"
SOURCE_GRAPH_ATTEMPT = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1907_STANDARD_MATTER_EXCHANGE_GRAPH_SOURCE_BACKED_ATTEMPT.csv"
SOURCE_OWNER_CONTRACT = SOURCE_DIR / "P8_source_owner_parent_action_terms_CONTRACT.csv"
POST_4378 = POST / "4378-Y5-R2FR-transition-topological-profile-moment-zero-or-first-multipole-bound-row.md"
OUTPUT_4442_ROUTE = SOURCE_DIR / "P8_Y5_R2FR_4442_NONEM_SOURCE_ROUTE_OUTPUT.csv"
OUTPUT_4442_TAIL = SOURCE_DIR / "P8_Y5_R2FR_4442_REQ_BZERO_FIRST_TAIL_OUTPUT.csv"

SMOKE_BOUND = 1.0e-5
SMOKE_PASS_VALUE = 3.0e-7
SMOKE_FAIL_VALUE = 4.0e-3


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
    for line_number, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return line_number
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
        {"source_id": "SRC4443_00_4442_next", "path": NEXT_4442, "needle": "4443-Y5-R2FR-parent-owned-connected-nonEM", "role": "4442 handoff."},
        {"source_id": "SRC4443_01_458_formal", "path": FORMAL_458, "needle": "NEM4442_1_scalar_naturality_reused", "role": "4442 graph/current route split."},
        {"source_id": "SRC4443_02_core_action", "path": CORE_ACTION, "needle": "L_matter the standard matter Lagrangian", "role": "core effective action standard matter block."},
        {"source_id": "SRC4443_03_core_variation", "path": CORE_ACTION, "needle": "δ(L_matter √(-g)) = T_{μν}", "role": "core variation maps matter action to Hilbert stress."},
        {"source_id": "SRC4443_04_fund_action", "path": FUND_ACTION, "needle": "L_matter] √(-g)", "role": "fundamental action has matter block under same measure."},
        {"source_id": "SRC4443_05_fund_variation", "path": FUND_ACTION, "needle": "δ [ L_matter √(-g) ]      →  T_{μν}", "role": "fundamental note maps matter block to stress."},
        {"source_id": "SRC4443_06_4423_schema", "path": FORMAL_439, "needle": "ADL4423_0_MTS_action_schema_seed", "role": "single L_matter schema seed precedent."},
        {"source_id": "SRC4443_07_4435_edge_theorem", "path": FORMAL_451, "needle": "EDGE4435_0_parent_edge_certificate_theorem", "role": "atomic parent edge certificate theorem."},
        {"source_id": "SRC4443_08_4434_graph", "path": FORMAL_450, "needle": "HMGC4434_2_current_graph_gap", "role": "connected graph gap remains."},
        {"source_id": "SRC4443_09_4420_req", "path": FORMAL_436, "needle": "AMR4420_0_joint_contract", "role": "joint source owner and R_eq route."},
        {"source_id": "SRC4443_10_edge_templates", "path": EDGE_TEMPLATE, "needle": "E1477_0_L_to_lepton", "role": "nonEM species/template edge inventory."},
        {"source_id": "SRC4443_11_node_templates", "path": NODE_TEMPLATE, "needle": "N1477_1_electron_lepton", "role": "nonEM graph node inventory."},
        {"source_id": "SRC4443_12_source_graph", "path": SOURCE_GRAPH_ATTEMPT, "needle": "SMG1907_6_verdict", "role": "source-backed exchange graph attempt."},
        {"source_id": "SRC4443_13_source_owner_contract", "path": SOURCE_OWNER_CONTRACT, "needle": "A6_selector_blind_source_action", "role": "selector-blind source action contract."},
        {"source_id": "SRC4443_14_req_source", "path": POST_4378, "needle": "HARMONIC_NULL_MOMENT_ZERO_THEOREM", "role": "R_eq compact/multipole moment route."},
        {"source_id": "SRC4443_15_gate", "path": GATE_PATH, "needle": "def evaluate_root_edge_row", "role": "4443 edge/tail gate."},
        {"source_id": "SRC4443_16_generator", "path": GENERATOR_PATH, "needle": 'CHECKPOINT = "4443"', "role": "4443 generator."},
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
            "derivation_id": "NEDGE4443_0_root_hilbert_stress_edge",
            "claim": "The standard classical nonEM matter block owns a Hilbert stress-current root edge inside the effective branch.",
            "derivation": "The core MTS action writes one L_matter under the same sqrt(-g) measure and explicitly maps delta(L_matter sqrt(-g)) to T_mu_nu. Therefore the edge L_matter -> T_H is signed as a branch-level action-density/current root edge before readout. This is the nonEM source-current owner for the total standard matter block, not yet a species graph certificate.",
            "consequence": "The total Hilbert source-current owner clause is no longer a foggy missing coupling on the standard branch; the remaining graph problem is component decomposition and no-prefactor/no-reentry.",
            "status": "NONEM_HILBERT_STRESS_ROOT_EDGE_BRANCH_SIGNED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "NEDGE4443_1_root_edge_not_component_graph",
            "claim": "The root Hilbert stress edge does not prove connected lepton/quark/QCD graph ownership.",
            "derivation": "A total L_matter block can vary to one total T_H while still hiding relative component weights inside L_matter = sum_A w_A L_A unless the parent expands the component terms and proves no species/source coefficient, species Jacobian or readout reentry. Thus L_matter->T_H closes a root-current edge but not Delta_w_A=0.",
            "consequence": "The next proof must expand standard L_matter into parent-owned component edges such as lepton, quark, QCD/gluon and composite material edges, or keep explicit Delta_w/C_src tails.",
            "status": "COMPONENT_GRAPH_NOT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "NEDGE4443_2_Req_definition_sharpened_after_root",
            "claim": "After the root edge, R_eq is the same-current mismatch rather than action-source ownership.",
            "derivation": "With L_matter->T_H signed on the standard branch, the remaining source-current obstruction is R_eq[varphi]=<Pi_M J_H-J_M^top-dB_zero,varphi> on the same worldtube. This object measures Hilbert/Hamiltonian/topological readout equality, not whether an ordinary Hilbert stress exists.",
            "consequence": "The first finite fallback is now an R_eq compact-test/multipole value or B_zero flux, with projection coefficient and arena bound.",
            "status": "REQ_COMPACT_TEST_TARGET_SHARPENED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "NEDGE4443_3_public_firewall",
            "claim": "No local-GR/Newton/PPN public claim follows from 4443.",
            "derivation": "The branch signs only the total standard-matter Hilbert stress root edge. It does not parent-sign component graph connectivity, constructor exhaustion, no hidden/readout reentry, R_eq=0, B_zero flux silence, or H_tau/MHref locks.",
            "consequence": NEXT_TARGET,
            "status": "PUBLIC_CLAIM_BLOCKED_NEXT_COMPONENT_EDGE_OR_REQ_VALUE",
            "valid_for_claim": False,
        },
    ]


def root_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "ROOT4443_0_core_Lmatter_to_T_H",
            "edge": "L_matter -> Hilbert stress T_H",
            "source_block": "standard classical L_matter block",
            "target_object": "T_mu_nu = Hilbert stress/current",
            "standard_lmatter_present": True,
            "metric_variation_to_hilbert_stress": True,
            "same_parent_measure": True,
            "nonEM_total_block": True,
            "current_before_readout": True,
            "no_species_prefactor_for_total_block": True,
            "component_decomposition_not_claimed": True,
            "source_path": str(CORE_ACTION),
            "public_authority": False,
            "input_valid_for_claim": False,
        },
        {
            "row_id": "ROOT4443_1_fundamental_action_confirming_row",
            "edge": "effective L_matter -> T_H in fundamental action note",
            "source_block": "MTS-Einstein action L_matter",
            "target_object": "T_mu_nu stress variation",
            "standard_lmatter_present": True,
            "metric_variation_to_hilbert_stress": True,
            "same_parent_measure": True,
            "nonEM_total_block": True,
            "current_before_readout": True,
            "no_species_prefactor_for_total_block": True,
            "component_decomposition_not_claimed": True,
            "source_path": str(FUND_ACTION),
            "public_authority": False,
            "input_valid_for_claim": False,
        },
    ]


def species_input_rows() -> List[Dict[str, object]]:
    base = {
        "template_edge_present": True,
        "standard_action_term_present": False,
        "same_parent_action_line": False,
        "parent_owned_morphism": False,
        "nonzero_morphism": False,
        "source_current_owner": False,
        "no_species_prefactor": False,
        "readout_no_reentry": False,
        "public_authority": False,
        "input_valid_for_claim": False,
    }
    return [
        {
            **base,
            "edge_id": "EDGE4443_0_L_to_lepton_template",
            "edge": "L_parent -> electron/lepton",
            "source_node": "N1477_0_L_parent",
            "target_node": "N1477_1_electron_lepton",
            "source_path": str(EDGE_TEMPLATE),
        },
        {
            **base,
            "edge_id": "EDGE4443_1_L_to_quark_template",
            "edge": "L_parent -> quark/flavour",
            "source_node": "N1477_0_L_parent",
            "target_node": "N1477_3_quark_flavour",
            "source_path": str(EDGE_TEMPLATE),
        },
        {
            **base,
            "edge_id": "EDGE4443_2_quark_gluon_template",
            "edge": "quark/flavour -> gluon/QCD",
            "source_node": "N1477_3_quark_flavour",
            "target_node": "N1477_4_gluon_QCD",
            "source_path": str(EDGE_TEMPLATE),
        },
        {
            "edge_id": "EDGE4443_3_future_component_edge_contract",
            "edge": "future parent-owned nonEM component edge",
            "source_node": "ordinary matter component A",
            "target_node": "ordinary matter component B",
            "template_edge_present": True,
            "standard_action_term_present": True,
            "same_parent_action_line": True,
            "parent_owned_morphism": True,
            "nonzero_morphism": True,
            "source_current_owner": True,
            "no_species_prefactor": True,
            "readout_no_reentry": True,
            "source_path": str(FORMAL_451),
            "public_authority": False,
            "input_valid_for_claim": False,
        },
    ]


def tail_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "tail_id": "REQ4443_0_compact_test_live",
            "quantity": "R_eq_compact_test",
            "arena": "Newton_PPN_orbital_same_current",
            "distributional_definition": "R_eq[varphi]=<Pi_M J_H-J_M_top-dB_zero,varphi> on W_H",
            "projection_coeff": "MISSING_P_REQ_COMPACT",
            "tail_value": "MISSING_REQ_COMPACT_TEST_VALUE",
            "arena_bound": "MISSING_ARENA_BOUND",
            "units": "source_current_distribution",
            "source_path": str(POST_4378),
            "public_authority": False,
            "input_valid_for_claim": False,
        },
        {
            "tail_id": "REQ4443_1_req_multipole_live",
            "quantity": "R_eq_l_multipole",
            "arena": "Newton_orbital_profile_moment",
            "distributional_definition": "M_l[R_eq]=int_W r^l Y_lm R_eq dV",
            "projection_coeff": "MISSING_P_REQ_L",
            "tail_value": "MISSING_REQ_MULTIPOLE_VALUE",
            "arena_bound": "MISSING_ARENA_BOUND",
            "units": "dimensionless_projected_moment",
            "source_path": str(POST_4378),
            "public_authority": False,
            "input_valid_for_claim": False,
        },
        {
            "tail_id": "REQ4443_2_zero_smoke",
            "quantity": "R_eq_compact_test",
            "arena": "schema_smoke",
            "distributional_definition": "P_tail*tail <= bound",
            "projection_coeff": "1",
            "tail_value": "0",
            "arena_bound": f"{SMOKE_BOUND:.12g}",
            "units": "dimensionless",
            "source_path": str(OUTPUT_4442_TAIL),
            "public_authority": False,
            "input_valid_for_claim": False,
        },
        {
            "tail_id": "REQ4443_3_small_smoke",
            "quantity": "R_eq_compact_test",
            "arena": "schema_smoke",
            "distributional_definition": "P_tail*tail <= bound",
            "projection_coeff": "1",
            "tail_value": f"{SMOKE_PASS_VALUE:.12g}",
            "arena_bound": f"{SMOKE_BOUND:.12g}",
            "units": "dimensionless",
            "source_path": str(OUTPUT_4442_TAIL),
            "public_authority": False,
            "input_valid_for_claim": False,
        },
        {
            "tail_id": "REQ4443_4_fail_control",
            "quantity": "R_eq_compact_test",
            "arena": "schema_smoke",
            "distributional_definition": "P_tail*tail <= bound",
            "projection_coeff": "1",
            "tail_value": f"{SMOKE_FAIL_VALUE:.12g}",
            "arena_bound": f"{SMOKE_BOUND:.12g}",
            "units": "dimensionless",
            "source_path": str(OUTPUT_4442_TAIL),
            "public_authority": False,
            "input_valid_for_claim": False,
        },
    ]


def reduction_rows() -> List[Dict[str, object]]:
    return [
        {"reduction_id": "RED4443_0_total_Hilbert_root_edge", "object": "L_matter -> T_H", "status": "BRANCH_SIGNED_NONCLAIM", "remaining": "component graph, no-prefactor, no-reentry, same-current R_eq", "source_path": str(CORE_ACTION), "valid_for_claim": False},
        {"reduction_id": "RED4443_1_component_graph", "object": "lepton/quark/gluon/QCD component graph", "status": "TEMPLATE_ONLY_PARENT_SIGNATURE_MISSING", "remaining": "expand standard L_matter into parent-owned component edges", "source_path": str(EDGE_TEMPLATE), "valid_for_claim": False},
        {"reduction_id": "RED4443_2_Req_tail", "object": "Pi_M J_H-J_top-dB_zero", "status": "LIVE_COMPACT_TEST_VALUES_MISSING", "remaining": "compact-test/multipole value, projection coefficient and arena bound", "source_path": str(POST_4378), "valid_for_claim": False},
        {"reduction_id": "RED4443_3_next", "object": "next least circular target", "status": "STANDARD_LMATTER_COMPONENT_EXPANSION_OR_REQ_VALUE", "remaining": NEXT_TARGET, "source_path": str(FORMAL_439), "valid_for_claim": False},
    ]


def claim_gate_rows(root_outputs: Sequence[Mapping[str, str]], species_outputs: Sequence[Mapping[str, str]], tail_outputs: Sequence[Mapping[str, str]]) -> List[Dict[str, object]]:
    root_by_id = {row["row_id"]: row for row in root_outputs}
    species_by_id = {row["edge_id"]: row for row in species_outputs}
    tail_by_id = {row["tail_id"]: row for row in tail_outputs}
    no_claims = not any(row.get("valid_for_claim") == "True" for row in root_outputs) and not any(row.get("valid_for_claim") == "True" for row in species_outputs) and not any(row.get("valid_for_claim") == "True" for row in tail_outputs)
    template_blocked = all(species_by_id[key].get("current_status") == "NONEM_SPECIES_GRAPH_EDGE_TEMPLATE_ONLY_PARENT_SIGNATURE_MISSING" for key in ("EDGE4443_0_L_to_lepton_template", "EDGE4443_1_L_to_quark_template", "EDGE4443_2_quark_gluon_template"))
    return [
        {"gate_id": "CG4443_0_sources_exist", "claim": "all cited source paths exist", "passed": all(row["path_exists"] == "True" for row in rows_from(SOURCE_REGISTER)), "valid_for_claim": False, "detail": "Source register path-backed."},
        {"gate_id": "CG4443_1_needles_found", "claim": "all cited source needles found", "passed": all(row["needle_found"] == "True" for row in rows_from(SOURCE_REGISTER)), "valid_for_claim": False, "detail": "No unsourced import."},
        {"gate_id": "CG4443_2_root_edge_signed", "claim": "standard L_matter Hilbert stress root edge is branch-signed", "passed": root_by_id["ROOT4443_0_core_Lmatter_to_T_H"].get("current_status") == "NONEM_HILBERT_STRESS_ROOT_EDGE_SIGNED_BRANCH_NONCLAIM", "valid_for_claim": False, "detail": "Total standard matter Hilbert current exists before readout on the effective branch."},
        {"gate_id": "CG4443_3_component_templates_blocked", "claim": "component graph template edges are not parent certificates", "passed": template_blocked, "valid_for_claim": False, "detail": "Lepton/quark/QCD rows remain templates only."},
        {"gate_id": "CG4443_4_future_component_contract", "claim": "future component edge contract is executable", "passed": species_by_id["EDGE4443_3_future_component_edge_contract"].get("current_status") == "NONEM_SPECIES_GRAPH_EDGE_CONTRACT_READY_NONCLAIM", "valid_for_claim": False, "detail": "Exact component edge row exists but is not parent/public signed."},
        {"gate_id": "CG4443_5_tail_controls", "claim": "R_eq tail gate has pass and fail controls", "passed": tail_by_id["REQ4443_3_small_smoke"].get("current_status") == "REQ_COMPACT_TEST_TAIL_SCHEMA_PASS_NONCLAIM" and tail_by_id["REQ4443_4_fail_control"].get("current_status") == "REQ_COMPACT_TEST_TAIL_FAILS_BOUND", "valid_for_claim": False, "detail": "Tail gate catches safe/failing controls."},
        {"gate_id": "CG4443_6_live_req_targets", "claim": "R_eq compact/multipole live targets written", "passed": all(key in text(TAIL_OUTPUT) for key in ("REQ4443_0_compact_test_live", "REQ4443_1_req_multipole_live")), "valid_for_claim": False, "detail": "Live rows require values/projections."},
        {"gate_id": "CG4443_7_no_public_claim", "claim": "4443 emits no local-GR/Newton/PPN public claim", "passed": no_claims, "valid_for_claim": False, "detail": "All outputs remain private nonclaim."},
        {"gate_id": "CG4443_8_next_target_written", "claim": "next target selected", "passed": NEXT_TARGET in text(NEXT_CSV), "valid_for_claim": False, "detail": NEXT_TARGET},
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4443_0",
            "decision": DECISION,
            "summary": "4443 signs a real root edge inside the standard effective branch: L_matter under the common metric measure varies to the Hilbert stress T_mu_nu, so the total nonEM standard-matter source current exists before readout. This advances the local source-coupling ladder, but it does not prove the component lepton/quark/QCD graph or Delta_w_A=0, because relative weights could still hide inside the L_matter decomposition unless component edges/no-Hom/no-reentry are parent-signed. The R_eq compact-test fallback is sharpened but still value-missing.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "public_claim": False,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {"status_id": "STAT4443_0_root_edge", "object": "L_matter -> T_H", "status": "BRANCH_SIGNED_NONCLAIM", "detail": "Standard effective matter block owns total Hilbert stress/current before readout.", "valid_for_claim": False},
        {"status_id": "STAT4443_1_component_graph", "object": "lepton/quark/QCD graph", "status": "TEMPLATE_ONLY", "detail": "Component edges need explicit parent action terms, no source prefactors and no readout reentry.", "valid_for_claim": False},
        {"status_id": "STAT4443_2_req", "object": "R_eq compact test", "status": "VALUE_MISSING", "detail": "Same-current compact/multipole value still needed.", "valid_for_claim": False},
        {"status_id": "STAT4443_3_next", "object": "next target", "status": "LMATTER_COMPONENT_EXPANSION_OR_REQ_VALUE", "detail": NEXT_TARGET, "valid_for_claim": False},
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4443_0",
            "target": NEXT_TARGET,
            "objective": "Either expand standard L_matter into claim-grade component graph edges, or fill the first same-current R_eq compact-test value.",
            "derive_first": "write the parent-owned component expansion of L_matter for lepton, quark and QCD/gluon sectors with no species/source prefactor, nonzero morphism and readout no-reentry",
            "fallback": "fill R_eq compact-test or first multipole value with units, projection coefficient, arena bound, source path and no-cancellation guard",
            "avoid": "treating total T_H as Delta_w_A=0; counting template graph rows as parent-owned; using observed GM as R_eq value",
            "valid_for_claim": False,
        }
    ]


def build_doc(sources: Sequence[Mapping[str, object]], root_outputs: Sequence[Mapping[str, object]], species_outputs: Sequence[Mapping[str, object]], tail_outputs: Sequence[Mapping[str, object]], gates: Sequence[Mapping[str, object]]) -> str:
    return f"""# 459 PPC4161 parent-owned connected nonEM graph edge or first Req compact test value

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4443 closes one real rung without overclaiming it:

```text
standard effective branch:
  S_matter = int L_matter sqrt(-g) d4x
  delta(L_matter sqrt(-g)) -> T_mu_nu
  therefore L_matter -> T_H is a signed total Hilbert source-current root edge

not yet closed:
  L_matter = sum_A L_A with no w_A/source prefactor
  parent-owned lepton/quark/QCD component graph edges
  readout/EFT no-reentry
  R_eq=0 and B_zero/H_tau locks
```

This is useful because the missing coupling is now narrower. The total standard matter Hilbert stress exists in the branch; the remaining fight is component graph ownership and same-current equality.

## Source Register

{table(sources)}

## Derivation Rows

{table(derivation_rows())}

## NonEM Hilbert Root Edge Gate

{table(root_outputs)}

## NonEM Component Edge Gate

{table(species_outputs)}

## R_eq Compact-Test Tail Gate

{table(tail_outputs)}

## Reduction Rows

{table(reduction_rows())}

## Claim Gates

{table(gates)}

## Decision

{table(decision_rows())}

## Status

{table(status_rows())}

## Next Target

{table(next_rows())}
"""


def post_doc() -> str:
    return f"""# 4443 Y5 R2FR parent-owned connected nonEM graph edge or first Req compact test value

Private checkpoint generated at `{STAMP}`.

Formal mirror: `{FORMAL_PATH}`

Decision: `{DECISION}`

Summary:
- `L_matter -> T_H` is branch-signed for the standard effective matter block.
- This does not prove lepton/quark/QCD component graph ownership or `Delta_w_A=0`.
- `R_eq` is now sharpened as same-current compact-test mismatch, but values remain missing.

Next target: `{NEXT_TARGET}`
"""


def update_claims_register() -> None:
    rows = rows_from(CLAIMS_PATH)
    fieldnames = list(rows[0].keys()) if rows else ["claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk", "sector", "evidence", "next_action", "risk"]
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    new_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_source_coupling",
        "claim": "4443 signs the standard-branch nonEM Hilbert stress root edge: L_matter under the common metric measure varies to T_mu_nu, so the total standard matter source current exists before readout. This is not a component graph or Delta_w_A zero claim; lepton/quark/QCD component edges, no-Hom/no-reentry and R_eq compact-test values remain open.",
        "current_evidence": "4443 source register, derivation rows, nonEM root edge gate, nonEM component edge gate, R_eq compact-test tail gate, reduction rows, claim gates, decision, status, next target and validation CSV.",
        "status": "nonEM_Hilbert_stress_root_edge_signed_standard_Lmatter_branch_species_graph_and_Req_value_open_nonclaim",
        "next_test": "Expand standard L_matter into parent-owned component graph edges or fill first R_eq compact-test value.",
        "key_risk": "Treating total T_H as component graph connectedness; hiding w_A inside L_matter; using observed GM as R_eq.",
        "sector": "local_gr_source_coupling",
        "evidence": "4443 source register, derivation rows, nonEM root edge gate, nonEM component edge gate, R_eq compact-test tail gate, reduction rows, claim gates, decision, status, next target and validation CSV.",
        "next_action": "Expand standard L_matter into parent-owned component graph edges or fill first R_eq compact-test value.",
        "risk": "Treating total T_H as component graph connectedness; hiding w_A inside L_matter; using observed GM as R_eq.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writerow(new_row)


def append_marker_section(path: Path, marker: str, section: str) -> None:
    existing = text(path)
    if marker in existing:
        return
    write_text(path, existing.rstrip() + "\n\n" + section.strip() + "\n")


def write_spine_and_packet() -> None:
    spine_section = f"""## Local GR Source Coupling Update - NonEM Hilbert Stress Root Edge

Marker: `{MARKER}`  
Source checkpoint: `4443-Y5-R2FR-parent-owned-connected-nonEM-graph-edge-or-first-Req-compact-test-value.md`  
Claim register row: `{CLAIM_ID}`

The standard effective branch now has a signed total matter source-current root edge: `L_matter` under the common metric measure varies to `T_H`. This narrows the coupling gap. It does not yet prove component graph connectedness or `Delta_w_A=0`; the next proof must expand `L_matter` into parent-owned lepton/quark/QCD component edges or fill a real `R_eq` compact-test value.
"""
    packet_section = f"""## PPC4161 Packet Addendum - NonEM Hilbert Stress Root Edge

Marker: `{PACKET_MARKER}`  
Source checkpoint: `4443-Y5-R2FR-parent-owned-connected-nonEM-graph-edge-or-first-Req-compact-test-value.md`

The packet may now treat the total standard `L_matter -> T_H` root edge as branch-signed. Component source weights remain live until `L_matter` is decomposed into parent-owned nonEM graph edges with no source prefactor and no readout re-entry. Same-current `R_eq` still needs proof-zero or a compact-test value.
"""
    append_marker_section(SPINE_PATH, MARKER, spine_section)
    append_marker_section(PACKET_PATH, PACKET_MARKER, packet_section)


def validation_rows(paths: Mapping[str, Path]) -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    roots = {row["row_id"]: row for row in rows_from(ROOT_OUTPUT)}
    species = {row["edge_id"]: row for row in rows_from(SPECIES_OUTPUT)}
    tails = {row["tail_id"]: row for row in rows_from(TAIL_OUTPUT)}
    gates = rows_from(CLAIM_GATES)
    no_claims = not any(row.get("valid_for_claim") == "True" for row in roots.values()) and not any(row.get("valid_for_claim") == "True" for row in species.values()) and not any(row.get("valid_for_claim") == "True" for row in tails.values())
    checks = [
        ("VAL4443_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source path exists"),
        ("VAL4443_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited source needle is present"),
        ("VAL4443_2_root_edge_signed", roots["ROOT4443_0_core_Lmatter_to_T_H"].get("current_status") == "NONEM_HILBERT_STRESS_ROOT_EDGE_SIGNED_BRANCH_NONCLAIM", "standard L_matter to T_H root edge signed nonclaim"),
        ("VAL4443_3_templates_blocked", all(species[key].get("current_status") == "NONEM_SPECIES_GRAPH_EDGE_TEMPLATE_ONLY_PARENT_SIGNATURE_MISSING" for key in ("EDGE4443_0_L_to_lepton_template", "EDGE4443_1_L_to_quark_template", "EDGE4443_2_quark_gluon_template")), "component templates remain blocked"),
        ("VAL4443_4_future_contract_nonclaim", species["EDGE4443_3_future_component_edge_contract"].get("current_status") == "NONEM_SPECIES_GRAPH_EDGE_CONTRACT_READY_NONCLAIM", "future component edge contract executable nonclaim"),
        ("VAL4443_5_tail_smoke_pass", tails["REQ4443_3_small_smoke"].get("current_status") == "REQ_COMPACT_TEST_TAIL_SCHEMA_PASS_NONCLAIM", "small R_eq tail smoke row passes schema nonclaim"),
        ("VAL4443_6_tail_fail_control", tails["REQ4443_4_fail_control"].get("current_status") == "REQ_COMPACT_TEST_TAIL_FAILS_BOUND", "fail-control R_eq tail row fails bound"),
        ("VAL4443_7_live_req_targets", all(key in text(TAIL_OUTPUT) for key in ("REQ4443_0_compact_test_live", "REQ4443_1_req_multipole_live")), "live R_eq compact/multipole rows written"),
        ("VAL4443_8_no_claim_outputs", no_claims, "no output row is claim-ready"),
        ("VAL4443_9_claim_gate_no_claim", any(row["gate_id"] == "CG4443_7_no_public_claim" and row["passed"] == "True" for row in gates), "claim gate explicitly blocks public claim"),
        ("VAL4443_10_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-284"),
        ("VAL4443_11_formal_doc", paths["formal"].exists() and MARKER in text(paths["formal"]), "formal doc exists with marker"),
        ("VAL4443_12_post_doc", paths["post"].exists() and "Private checkpoint" in text(paths["post"]), "post checkpoint doc exists"),
        ("VAL4443_13_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4443_14_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4443_15_next_gate", any(row["gate_id"] == "CG4443_8_next_target_written" and row["passed"] == "True" for row in gates), "next target claim gate is true"),
        ("VAL4443_16_next_target", paths["next"].exists() and NEXT_TARGET in text(paths["next"]), "next target file exists"),
        ("VAL4443_17_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": bool(passed), "detail": detail} for check_id, passed, detail in checks]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(DERIVATION_ROWS, derivation_rows())
    write_csv(ROOT_INPUT, root_input_rows())
    write_csv(ROOT_OUTPUT, evaluate_root_edge_rows(ROOT_INPUT))
    write_csv(SPECIES_INPUT, species_input_rows())
    write_csv(SPECIES_OUTPUT, evaluate_species_edge_rows(SPECIES_INPUT))
    write_csv(TAIL_INPUT, tail_input_rows())
    write_csv(TAIL_OUTPUT, evaluate_tail_rows(TAIL_INPUT))
    write_csv(REDUCTION_ROWS, reduction_rows())
    write_csv(DECISION_CSV, decision_rows())
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    root_outputs = rows_from(ROOT_OUTPUT)
    species_outputs = rows_from(SPECIES_OUTPUT)
    tail_outputs = rows_from(TAIL_OUTPUT)
    gates = claim_gate_rows(root_outputs, species_outputs, tail_outputs)
    write_csv(CLAIM_GATES, gates)
    write_text(FORMAL_PATH, build_doc(rows_from(SOURCE_REGISTER), root_outputs, species_outputs, tail_outputs, gates))
    write_text(DOC_PATH, post_doc())
    update_claims_register()
    write_spine_and_packet()
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    write_csv(VALIDATION_PATH, validation_rows({"formal": FORMAL_PATH, "post": DOC_PATH, "next": NEXT_CSV}))


if __name__ == "__main__":
    main()

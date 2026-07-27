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

from standard_lmatter_component_gate import (  # noqa: E402
    evaluate_parent_component_rows,
    evaluate_standard_component_rows,
    evaluate_tail_rows,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4444"
CLAIM_ID = "L-285"
MARKER = "PPC4161_STANDARD_LMATTER_COMPONENT_EDGE_EXPANSION_OR_REQ_COMPACT_TEST_4444"
PACKET_MARKER = "PPC4161_PACKET_STANDARD_LMATTER_COMPONENT_EDGE_EXPANSION_4444"
DECISION = "STANDARD_LMATTER_COMPONENT_IMPORT_GRAPH_CONTRACT_WRITTEN_PARENT_SM_ORIGIN_AND_REQ_VALUE_REMAIN_NONCLAIM"
NEXT_TARGET = "4445-Y5-R2FR-parent-SM-component-origin-no-source-prefactor-or-first-Req-value.md"

FORMAL_PATH = FORMAL / "460-PPC4161-standard-Lmatter-component-edge-expansion-or-Req-compact-test-value.md"
DOC_PATH = POST / "4444-Y5-R2FR-standard-Lmatter-component-edge-expansion-or-Req-compact-test-value.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4444_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4444_SOURCE_REGISTER.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4444_DERIVATION_ROWS.csv"
STANDARD_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4444_STANDARD_COMPONENT_EDGE_INPUT.csv"
STANDARD_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4444_STANDARD_COMPONENT_EDGE_OUTPUT.csv"
PARENT_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4444_PARENT_COMPONENT_CERT_INPUT.csv"
PARENT_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4444_PARENT_COMPONENT_CERT_OUTPUT.csv"
TAIL_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4444_REQ_COMPACT_TEST_TAIL_INPUT.csv"
TAIL_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4444_REQ_COMPACT_TEST_TAIL_OUTPUT.csv"
REDUCTION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4444_REDUCTION_ROWS.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4444_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4444_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4444_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4444_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "standard_lmatter_component_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4444_standard_Lmatter_component_edge_expansion_or_Req_compact_test_value.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4443 = SOURCE_DIR / "P8_Y5_R2FR_4443_NEXT_TARGET.csv"
FORMAL_459 = FORMAL / "459-PPC4161-parent-owned-connected-nonEM-graph-edge-or-first-Req-compact-test-value.md"
FORMAL_451 = FORMAL / "451-PPC4161-parent-owned-action-density-graph-edge-certificate-or-first-Kmactionscale-source-leg.md"
FORMAL_439 = FORMAL / "439-PPC4161-action-density-line-owner-or-first-source-backed-Pwep-Req-value.md"
CORE_ACTION = ROOT / "core-mts-framework" / "action-principle" / "the-motion-timespace-action-principle.md"
FUND_ACTION = ROOT / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md"
EDGE_TEMPLATE = SOURCE_DIR / "P8_Y5_R10_1477_CONNECTED_MATTER_GRAPH_EDGES.csv"
NODE_TEMPLATE = SOURCE_DIR / "P8_Y5_R10_1477_CONNECTED_MATTER_GRAPH_NODES.csv"
SOURCE_GRAPH_ATTEMPT = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1907_STANDARD_MATTER_EXCHANGE_GRAPH_SOURCE_BACKED_ATTEMPT.csv"
SOURCE_OWNER_CONTRACT = SOURCE_DIR / "P8_source_owner_parent_action_terms_CONTRACT.csv"
POST_4378 = POST / "4378-Y5-R2FR-transition-topological-profile-moment-zero-or-first-multipole-bound-row.md"

SMOKE_BOUND = 1.0e-5
SMOKE_PASS_VALUE = 2.5e-7
SMOKE_FAIL_VALUE = 3.0e-3


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
        {"source_id": "SRC4444_00_next4443", "path": NEXT_4443, "needle": "4444-Y5-R2FR-standard-Lmatter-component-edge-expansion-or-Req-compact-test-value.md", "role": "4443 handoff to component expansion target."},
        {"source_id": "SRC4444_01_459_formal", "path": FORMAL_459, "needle": "L_matter = sum_A L_A", "role": "4443 narrowed missing proof to component decomposition."},
        {"source_id": "SRC4444_02_core_standard", "path": CORE_ACTION, "needle": "L_matter the standard matter Lagrangian", "role": "core action imports standard matter block."},
        {"source_id": "SRC4444_03_core_variation", "path": CORE_ACTION, "needle": "δ(L_matter √(-g)) = T_{μν}", "role": "core variation maps matter block to Hilbert stress."},
        {"source_id": "SRC4444_04_fund_action", "path": FUND_ACTION, "needle": "L_matter] √(-g)", "role": "fundamental action has matter block under same measure."},
        {"source_id": "SRC4444_05_hom_theorem", "path": FORMAL_439, "needle": "ADL4423_1_typed_Hom_no_slot_theorem", "role": "no source-only species coefficient theorem contract."},
        {"source_id": "SRC4444_06_edge_theorem", "path": FORMAL_451, "needle": "EDGE4435_0_parent_edge_certificate_theorem", "role": "atomic parent component edge certificate theorem."},
        {"source_id": "SRC4444_07_template_edges", "path": EDGE_TEMPLATE, "needle": "E1477_0_L_to_lepton", "role": "component graph template inventory."},
        {"source_id": "SRC4444_08_template_nodes", "path": NODE_TEMPLATE, "needle": "N1477_4_gluon_QCD", "role": "component node inventory."},
        {"source_id": "SRC4444_09_source_graph_attempt", "path": SOURCE_GRAPH_ATTEMPT, "needle": "SMG1907_1_exchange_theorem", "role": "prior source-backed exchange graph attempt."},
        {"source_id": "SRC4444_10_source_owner_contract", "path": SOURCE_OWNER_CONTRACT, "needle": "A6_selector_blind_source_action", "role": "selector-blind source action contract."},
        {"source_id": "SRC4444_11_req_fallback", "path": POST_4378, "needle": "HARMONIC_NULL_MOMENT_ZERO_THEOREM", "role": "R_eq compact/multipole fallback theorem precedent."},
        {"source_id": "SRC4444_12_gate", "path": GATE_PATH, "needle": "def evaluate_standard_component_row", "role": "4444 gate script."},
        {"source_id": "SRC4444_13_generator", "path": GENERATOR_PATH, "needle": 'CHECKPOINT = "4444"', "role": "4444 generator script."},
    ]


def source_rows() -> List[Dict[str, object]]:
    rows = []
    for spec in source_specs():
        path = Path(spec["path"])
        needle = str(spec["needle"])
        line = line_of(path, needle)
        rows.append({
            "checkpoint": CHECKPOINT,
            "source_id": spec["source_id"],
            "path": str(path),
            "path_exists": path.exists(),
            "needle": needle,
            "needle_found": line > 0,
            "line_number": line,
            "role": spec["role"],
            "valid_for_claim": False,
        })
    return rows


def derivation_rows() -> List[Dict[str, object]]:
    return [
        {
            "derivation_id": "LMCE4444_0_standard_import_expansion",
            "claim": "The standard effective branch can expand L_matter into visible component sectors as an imported matter theory contract.",
            "derivation": "4443 signed the total L_matter -> T_H root edge. Because the core text names L_matter as the standard matter Lagrangian, the branch may write component slots for lepton, quark, EM/gauge and QCD/gluon sectors under the same metric measure. This is a standard-matter import expansion, not an MTS derivation of the Standard Model.",
            "consequence": "We can now test component-edge clauses explicitly instead of repeatedly saying 'coupling missing'.",
            "status": "STANDARD_IMPORT_COMPONENT_GRAPH_CONTRACT_WRITTEN",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "LMCE4444_1_component_naturality_contract",
            "claim": "If component edges are parent-owned and selector-blind, relative source weights collapse.",
            "derivation": "On a connected ordinary-matter component graph, nonzero same-action source morphisms plus empty Hom(SpeciesLabel,Coeff_active_source), no source-only prefactor, and readout no-reentry leave only one common calibration of the Hilbert source current. Therefore Delta_w_A=0 is exact only after those parent clauses are signed.",
            "consequence": "The mathematical target is sharper: prove parent ownership/no-prefactor for the component graph, not just total T_H.",
            "status": "EXACT_CONDITIONAL_COMPONENT_NATURALITY_THEOREM_READY",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "LMCE4444_2_parent_origin_gap",
            "claim": "MTS does not yet derive the component action content of ordinary matter.",
            "derivation": "The corpus imports standard L_matter, but it does not yet parent-derive the lepton/quark/gauge/QCD component terms, representation constants, Yukawa/mass terms, material projection, or constructor exhaustion that forbids hidden source prefactors.",
            "consequence": "The imported branch is useful and honest, but local-GR/source-universality remains nonclaim until the parent origin or a first R_eq value is supplied.",
            "status": "PARENT_SM_COMPONENT_ORIGIN_OPEN",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "LMCE4444_3_req_fallback",
            "claim": "If component origin cannot be signed, the first finite fallback is a same-current R_eq compact-test value.",
            "derivation": "A real compact-test residual needs a distributional definition, projection coefficient, value, arena bound and source path. Smoke rows can test schema only; live rows remain blocked until numeric/source-backed values exist.",
            "consequence": "The fallback is concrete: either derive source universality or score the exact residual it leaves.",
            "status": "REQ_COMPACT_TEST_VALUE_ROUTE_RETAINED_NONCLAIM",
            "valid_for_claim": False,
        },
    ]


def standard_component_input_rows() -> List[Dict[str, object]]:
    edge_path = str(EDGE_TEMPLATE)
    return [
        {
            "edge_id": "COMP4444_0_L_to_lepton_import",
            "edge": "L_matter -> lepton_component",
            "source_node": "standard L_matter",
            "target_node": "electron/lepton",
            "branch": "imported_standard_matter",
            "template_edge_present": True,
            "standard_lmatter_imported": True,
            "component_action_term_named": True,
            "same_metric_measure": True,
            "nonzero_standard_morphism": True,
            "source_current_before_readout": True,
            "no_species_prefactor_in_import": True,
            "readout_no_reentry": True,
            "parent_derived_by_MTS": False,
            "source_path": edge_path,
            "public_authority": False,
            "input_valid_for_claim": False,
            "notes": "Lepton component edge is ready only as standard-matter import; MTS parent origin remains open.",
        },
        {
            "edge_id": "COMP4444_1_L_to_quark_import",
            "edge": "L_matter -> quark_component",
            "source_node": "standard L_matter",
            "target_node": "light quark sector",
            "branch": "imported_standard_matter",
            "template_edge_present": True,
            "standard_lmatter_imported": True,
            "component_action_term_named": True,
            "same_metric_measure": True,
            "nonzero_standard_morphism": True,
            "source_current_before_readout": True,
            "no_species_prefactor_in_import": True,
            "readout_no_reentry": True,
            "parent_derived_by_MTS": False,
            "source_path": edge_path,
            "public_authority": False,
            "input_valid_for_claim": False,
            "notes": "Quark component edge is an imported standard-matter slot, not a parent-derived MTS source edge.",
        },
        {
            "edge_id": "COMP4444_2_L_to_gluon_QCD_import",
            "edge": "L_matter -> gluon_QCD_component",
            "source_node": "standard L_matter",
            "target_node": "gluon/QCD binding",
            "branch": "imported_standard_matter",
            "template_edge_present": True,
            "standard_lmatter_imported": True,
            "component_action_term_named": True,
            "same_metric_measure": True,
            "nonzero_standard_morphism": True,
            "source_current_before_readout": True,
            "no_species_prefactor_in_import": True,
            "readout_no_reentry": True,
            "parent_derived_by_MTS": False,
            "source_path": edge_path,
            "public_authority": False,
            "input_valid_for_claim": False,
            "notes": "QCD/gluon component edge is import-ready but MTS has not derived color/gauge action content.",
        },
        {
            "edge_id": "COMP4444_3_quark_gluon_import",
            "edge": "quark_component -> gluon_QCD_component",
            "source_node": "light quark sector",
            "target_node": "gluon/QCD binding",
            "branch": "imported_standard_matter_exchange",
            "template_edge_present": True,
            "standard_lmatter_imported": True,
            "component_action_term_named": True,
            "same_metric_measure": True,
            "nonzero_standard_morphism": True,
            "source_current_before_readout": True,
            "no_species_prefactor_in_import": True,
            "readout_no_reentry": True,
            "parent_derived_by_MTS": False,
            "source_path": edge_path,
            "public_authority": False,
            "input_valid_for_claim": False,
            "notes": "Imported QCD exchange gives connectedness shape, but source universality still waits on parent ownership.",
        },
        {
            "edge_id": "COMP4444_4_template_control",
            "edge": "template_only_control",
            "source_node": "template graph",
            "target_node": "component graph",
            "branch": "control",
            "template_edge_present": True,
            "standard_lmatter_imported": False,
            "component_action_term_named": False,
            "same_metric_measure": False,
            "nonzero_standard_morphism": False,
            "source_current_before_readout": False,
            "no_species_prefactor_in_import": False,
            "readout_no_reentry": False,
            "parent_derived_by_MTS": False,
            "source_path": edge_path,
            "public_authority": False,
            "input_valid_for_claim": False,
            "notes": "Control row proves templates alone are rejected.",
        },
    ]


def parent_component_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "cert_id": "PARENT4444_0_live_MTS_parent_origin",
            "branch": "live_MTS_parent_component_origin",
            "object": "MTS-derived standard matter component action and source graph",
            "mts_parent_derives_component_action": False,
            "representation_constants_derived_or_import_contract": False,
            "yukawa_mass_terms_derived_or_import_contract": False,
            "material_projection_sourced": False,
            "no_source_prefactor_parent_signed": False,
            "source_current_before_readout": True,
            "readout_no_reentry": False,
            "constructor_exhaustion_signed": False,
            "source_path": str(SOURCE_OWNER_CONTRACT),
            "public_authority": False,
            "input_valid_for_claim": False,
            "notes": "Live MTS corpus imports standard matter but has not derived its component origin or no-source-prefactor certificate.",
        },
        {
            "cert_id": "PARENT4444_1_imported_SM_branch_contract",
            "branch": "imported_standard_model_branch",
            "object": "standard matter accepted as imported branch with guarded no-source-prefactor contract",
            "mts_parent_derives_component_action": False,
            "representation_constants_derived_or_import_contract": True,
            "yukawa_mass_terms_derived_or_import_contract": True,
            "material_projection_sourced": False,
            "no_source_prefactor_parent_signed": False,
            "source_current_before_readout": True,
            "readout_no_reentry": True,
            "constructor_exhaustion_signed": False,
            "source_path": str(SOURCE_OWNER_CONTRACT),
            "public_authority": False,
            "input_valid_for_claim": False,
            "notes": "Import branch can be used internally, but it is not a parent derivation and lacks material/source-prefactor closure.",
        },
        {
            "cert_id": "PARENT4444_2_future_parent_contract",
            "branch": "future_parent_SM_component_contract",
            "object": "future MTS parent action derives or legally imports all ordinary matter component sectors",
            "mts_parent_derives_component_action": True,
            "representation_constants_derived_or_import_contract": True,
            "yukawa_mass_terms_derived_or_import_contract": True,
            "material_projection_sourced": True,
            "no_source_prefactor_parent_signed": True,
            "source_current_before_readout": True,
            "readout_no_reentry": True,
            "constructor_exhaustion_signed": True,
            "source_path": str(SOURCE_OWNER_CONTRACT),
            "public_authority": False,
            "input_valid_for_claim": False,
            "notes": "Exact future contract only; nonclaim until parent-signed by actual MTS construction.",
        },
    ]


def tail_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "tail_id": "REQ4444_0_compact_test_live",
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
            "notes": "Live fallback still value-missing; retained because parent component origin remains open.",
        },
        {
            "tail_id": "REQ4444_1_req_multipole_live",
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
            "notes": "First multipole fallback remains numeric/source-backed work, not a claim.",
        },
        {
            "tail_id": "REQ4444_2_zero_smoke",
            "quantity": "R_eq_compact_test",
            "arena": "schema_smoke",
            "distributional_definition": "P_tail*tail <= bound",
            "projection_coeff": "1",
            "tail_value": "0",
            "arena_bound": str(SMOKE_BOUND),
            "units": "dimensionless",
            "source_path": str(POST_4378),
            "public_authority": False,
            "input_valid_for_claim": False,
            "notes": "Zero smoke verifies schema only.",
        },
        {
            "tail_id": "REQ4444_3_small_smoke",
            "quantity": "R_eq_compact_test",
            "arena": "schema_smoke",
            "distributional_definition": "P_tail*tail <= bound",
            "projection_coeff": "1",
            "tail_value": str(SMOKE_PASS_VALUE),
            "arena_bound": str(SMOKE_BOUND),
            "units": "dimensionless",
            "source_path": str(POST_4378),
            "public_authority": False,
            "input_valid_for_claim": False,
            "notes": "Small smoke must pass as nonclaim.",
        },
        {
            "tail_id": "REQ4444_4_fail_control",
            "quantity": "R_eq_compact_test",
            "arena": "schema_smoke",
            "distributional_definition": "P_tail*tail <= bound",
            "projection_coeff": "1",
            "tail_value": str(SMOKE_FAIL_VALUE),
            "arena_bound": str(SMOKE_BOUND),
            "units": "dimensionless",
            "source_path": str(POST_4378),
            "public_authority": False,
            "input_valid_for_claim": False,
            "notes": "Fail control must fail the bound.",
        },
    ]


def reduction_rows() -> List[Dict[str, object]]:
    return [
        {
            "reduction_id": "RED4444_0_not_total_stress",
            "from_problem": "missing local GR/source coupling",
            "to_problem": "parent origin and no-source-prefactor for component ordinary matter graph",
            "status": "REDUCED_TO_COMPONENT_ORIGIN_NO_PREFAC",
            "reason": "Total L_matter -> T_H is already signed; the remaining loophole is relative component weights hidden inside the imported standard matter block.",
            "valid_for_claim": False,
        },
        {
            "reduction_id": "RED4444_1_import_branch_not_public_claim",
            "from_problem": "standard component expansion",
            "to_problem": "imported branch usable internally, parent derivation still open",
            "status": "IMPORT_BRANCH_USEFUL_PARENT_ORIGIN_OPEN",
            "reason": "This prevents both errors: rejecting useful standard matter structure and overclaiming it as MTS-derived.",
            "valid_for_claim": False,
        },
        {
            "reduction_id": "RED4444_2_fallback_value",
            "from_problem": "if component parent origin fails",
            "to_problem": "first R_eq compact-test or multipole value",
            "status": "REQ_VALUE_ROUTE_RETAINED",
            "reason": "A finite residual can still be bounded if derivation cannot close.",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(standard_outputs: Sequence[Mapping[str, str]], parent_outputs: Sequence[Mapping[str, str]], tail_outputs: Sequence[Mapping[str, str]]) -> List[Dict[str, object]]:
    standard_by_id = {row["edge_id"]: row for row in standard_outputs}
    parent_by_id = {row["cert_id"]: row for row in parent_outputs}
    tail_by_id = {row["tail_id"]: row for row in tail_outputs}
    no_claim = not any(row.get("valid_for_claim") == "True" for row in standard_outputs) and not any(row.get("valid_for_claim") == "True" for row in parent_outputs) and not any(row.get("valid_for_claim") == "True" for row in tail_outputs)
    import_ready = all(standard_by_id[key].get("current_status") == "STANDARD_COMPONENT_EDGE_IMPORT_READY_PARENT_DERIVATION_OPEN_NONCLAIM" for key in ("COMP4444_0_L_to_lepton_import", "COMP4444_1_L_to_quark_import", "COMP4444_2_L_to_gluon_QCD_import", "COMP4444_3_quark_gluon_import"))
    return [
        {"gate_id": "CG4444_0_sources_exist", "claim": "all cited source paths exist", "passed": all(row["path_exists"] == "True" for row in rows_from(SOURCE_REGISTER)), "valid_for_claim": False, "detail": "Source register path-backed."},
        {"gate_id": "CG4444_1_needles_found", "claim": "all cited source needles found", "passed": all(row["needle_found"] == "True" for row in rows_from(SOURCE_REGISTER)), "valid_for_claim": False, "detail": "No unsourced import."},
        {"gate_id": "CG4444_2_import_edges_ready", "claim": "standard component import edges are written", "passed": import_ready, "valid_for_claim": False, "detail": "Lepton/quark/QCD component rows are now explicit imported-branch contracts."},
        {"gate_id": "CG4444_3_template_control_rejected", "claim": "template-only control remains blocked", "passed": standard_by_id["COMP4444_4_template_control"].get("current_status") == "STANDARD_COMPONENT_EDGE_TEMPLATE_ONLY_IMPORT_MISSING", "valid_for_claim": False, "detail": "Templates alone still do not count."},
        {"gate_id": "CG4444_4_parent_origin_blocked", "claim": "live parent component origin remains open", "passed": parent_by_id["PARENT4444_0_live_MTS_parent_origin"].get("current_status") == "PARENT_COMPONENT_DERIVATION_OPEN", "valid_for_claim": False, "detail": "MTS has not yet derived SM component terms/no-source-prefactor/material projection."},
        {"gate_id": "CG4444_5_future_contract_nonclaim", "claim": "future parent component contract is executable", "passed": parent_by_id["PARENT4444_2_future_parent_contract"].get("current_status") == "PARENT_COMPONENT_DERIVATION_CONTRACT_READY_NONCLAIM", "valid_for_claim": False, "detail": "Exact contract exists but is not parent-signed."},
        {"gate_id": "CG4444_6_tail_controls", "claim": "R_eq tail gate has pass and fail controls", "passed": tail_by_id["REQ4444_3_small_smoke"].get("current_status") == "REQ_COMPACT_TEST_TAIL_SCHEMA_PASS_NONCLAIM" and tail_by_id["REQ4444_4_fail_control"].get("current_status") == "REQ_COMPACT_TEST_TAIL_FAILS_BOUND", "valid_for_claim": False, "detail": "Tail gate catches safe/failing controls."},
        {"gate_id": "CG4444_7_live_req_targets", "claim": "R_eq compact/multipole live targets written", "passed": all(key in tail_by_id for key in ("REQ4444_0_compact_test_live", "REQ4444_1_req_multipole_live")), "valid_for_claim": False, "detail": "Live rows still require values/projections."},
        {"gate_id": "CG4444_8_no_public_claim", "claim": "4444 emits no local-GR/Newton/PPN public claim", "passed": no_claim, "valid_for_claim": False, "detail": "All outputs remain private nonclaim."},
        {"gate_id": "CG4444_9_next_target_written", "claim": "next target selected", "passed": NEXT_CSV.exists() and NEXT_TARGET in text(NEXT_CSV), "valid_for_claim": False, "detail": NEXT_TARGET},
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4444_0",
            "decision": DECISION,
            "summary": "4444 moves the coupling problem forward by writing an explicit standard-L_matter component expansion gate. Lepton, quark, QCD/gluon and quark-gluon rows are import-ready inside the standard effective branch, so component structure is no longer just a vague missing item. But those rows are not MTS-parent-derived: representation constants, Yukawa/mass terms, material projection, constructor exhaustion and no source-only prefactor remain unsigned. Therefore Delta_w_A=0/local-GR source universality is still nonclaim, and the fallback is a real R_eq compact-test or multipole value.",
            "next_target": NEXT_TARGET,
            "public_claim": False,
            "valid_for_claim": False,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "root_result": "standard component import graph contract written",
            "still_missing": "MTS parent origin of component action; no-source-prefactor certificate; material projection; R_eq value",
            "next_target": NEXT_TARGET,
            "public_claim": False,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4444_0",
            "target": NEXT_TARGET,
            "objective": "Either derive the MTS parent origin/no-source-prefactor certificate for the imported standard-matter component graph, or fill the first same-current R_eq compact-test value.",
            "derive_first": "try to construct a parent action clause that legally owns or derives lepton/quark/gauge/QCD component terms while forbidding source-only species weights",
            "fallback": "fill R_eq compact-test or first multipole value with units, projection coefficient, arena bound, source path and no-cancellation guard",
            "risk": "mistaking imported standard matter for MTS-derived matter; hiding relative source weights inside representation constants or material projection",
            "valid_for_claim": False,
        }
    ]


def build_doc(sources: Sequence[Mapping[str, object]], standard_outputs: Sequence[Mapping[str, object]], parent_outputs: Sequence[Mapping[str, object]], tail_outputs: Sequence[Mapping[str, object]], gates: Sequence[Mapping[str, object]]) -> str:
    return f"""# 460 PPC4161 standard Lmatter component edge expansion or Req compact test value

Marker: `{MARKER}`

Decision: `{DECISION}`

Claim register: `{CLAIM_ID}`

## Result

4444 does not just circle the missing coupling. It separates the problem into two clean branches:

1. **Imported standard-matter branch:** `L_matter` may be expanded into lepton, quark, EM/gauge and QCD/gluon component slots under the same metric measure. Those rows are now explicit import-ready contracts.
2. **MTS parent-derived branch:** the corpus still has not derived the component action content, representation/Yukawa/mass structure, material projection, constructor exhaustion or no source-only-prefactor theorem. Therefore `Delta_w_A=0` and full local-GR source universality remain nonclaim.

The real next fork is therefore not "is coupling missing?" but:

```text
Can MTS parent-own/import the standard component graph without a source-only species prefactor?
If yes: push toward Delta_w_A=0.
If no: fill the first same-current R_eq compact-test or multipole value.
```

## Source Register

{table(sources)}

## Derivation Rows

{table(rows_from(DERIVATION_ROWS))}

## Standard Component Edge Gate

{table(standard_outputs)}

## Parent Component Certificate Gate

{table(parent_outputs)}

## R_eq Compact-Test Tail Gate

{table(tail_outputs)}

## Reduction Rows

{table(rows_from(REDUCTION_ROWS))}

## Claim Gates

{table(gates)}

## Decision

{table(rows_from(DECISION_CSV))}

## Status

{table(rows_from(STATUS_CSV))}

## Next Target

{table(rows_from(NEXT_CSV))}
"""


def post_doc() -> str:
    return f"""# 4444 Y5 R2FR standard Lmatter component edge expansion or Req compact test value

Private checkpoint generated at `{STAMP}`.

Summary:
- Standard `L_matter` component rows are now explicit for lepton, quark, QCD/gluon and quark-gluon exchange as **imported standard-matter branch contracts**.
- This is a real narrowing of the coupling gap, not a public claim: MTS has not yet parent-derived those sectors or proved no hidden source prefactor.
- The next target is parent-origin/no-prefactor for the component graph; if that fails, fill the first same-current `R_eq` value.

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
        "claim": "4444 writes the standard L_matter component expansion gate: lepton, quark, QCD/gluon and quark-gluon rows are import-ready inside the standard effective branch, but are not MTS-parent-derived. Delta_w_A=0/source universality remains nonclaim until parent origin/no-source-prefactor/material projection close or a same-current R_eq value is filled.",
        "current_evidence": "4444 source register, derivation rows, standard component edge gate, parent component certificate gate, R_eq compact-test tail gate, reduction rows, claim gates, decision, status, next target and validation CSV.",
        "status": "standard_Lmatter_component_import_graph_contract_written_parent_SM_origin_and_Req_value_open_nonclaim",
        "next_test": "Derive MTS parent SM component origin/no-source-prefactor, or fill first R_eq compact-test value.",
        "key_risk": "Mistaking imported standard matter for MTS-derived matter; hiding source weights inside component decomposition, representation constants or material projection.",
        "sector": "local_gr_source_coupling",
        "evidence": "4444 source register, derivation rows, standard component edge gate, parent component certificate gate, R_eq compact-test tail gate, reduction rows, claim gates, decision, status, next target and validation CSV.",
        "next_action": "Derive MTS parent SM component origin/no-source-prefactor, or fill first R_eq compact-test value.",
        "risk": "Mistaking imported standard matter for MTS-derived matter; hiding source weights inside component decomposition, representation constants or material projection.",
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
    spine_section = f"""## Local GR Source Coupling Update - Standard Lmatter Component Expansion

Marker: `{MARKER}`  
Source checkpoint: `4444-Y5-R2FR-standard-Lmatter-component-edge-expansion-or-Req-compact-test-value.md`  
Claim register row: `{CLAIM_ID}`

The standard effective branch now has explicit component-edge contracts for lepton, quark, QCD/gluon and quark-gluon sectors under imported `L_matter`. This is progress because the local source-coupling gap has been narrowed to parent origin/no-source-prefactor/material projection, not generic "missing coupling". The component graph is not yet MTS-derived, so source universality remains private nonclaim until the parent action owns/imports those sectors without a source-only species coefficient or a first same-current `R_eq` value is filled.
"""
    packet_section = f"""## PPC4161 Packet Addendum - Standard Lmatter Component Expansion

Marker: `{PACKET_MARKER}`  
Source checkpoint: `4444-Y5-R2FR-standard-Lmatter-component-edge-expansion-or-Req-compact-test-value.md`

The packet may use the standard `L_matter` component expansion as an imported-branch contract only. It must not count lepton/quark/QCD component connectedness as MTS-parent-derived until the parent action signs component origin, no source-only prefactor, material projection and readout no-reentry. If that route fails, score same-current `R_eq`.
"""
    append_marker_section(SPINE_PATH, MARKER, spine_section)
    append_marker_section(PACKET_PATH, PACKET_MARKER, packet_section)


def validation_rows(paths: Mapping[str, Path]) -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    standard = {row["edge_id"]: row for row in rows_from(STANDARD_OUTPUT)}
    parent = {row["cert_id"]: row for row in rows_from(PARENT_OUTPUT)}
    tails = {row["tail_id"]: row for row in rows_from(TAIL_OUTPUT)}
    gates = rows_from(CLAIM_GATES)
    no_claims = not any(row.get("valid_for_claim") == "True" for row in standard.values()) and not any(row.get("valid_for_claim") == "True" for row in parent.values()) and not any(row.get("valid_for_claim") == "True" for row in tails.values())
    checks = [
        ("VAL4444_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source path exists"),
        ("VAL4444_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited source needle is present"),
        ("VAL4444_2_import_edges_ready", all(standard[key].get("current_status") == "STANDARD_COMPONENT_EDGE_IMPORT_READY_PARENT_DERIVATION_OPEN_NONCLAIM" for key in ("COMP4444_0_L_to_lepton_import", "COMP4444_1_L_to_quark_import", "COMP4444_2_L_to_gluon_QCD_import", "COMP4444_3_quark_gluon_import")), "standard component import edges ready nonclaim"),
        ("VAL4444_3_template_control_rejected", standard["COMP4444_4_template_control"].get("current_status") == "STANDARD_COMPONENT_EDGE_TEMPLATE_ONLY_IMPORT_MISSING", "template-only control is rejected"),
        ("VAL4444_4_parent_origin_open", parent["PARENT4444_0_live_MTS_parent_origin"].get("current_status") == "PARENT_COMPONENT_DERIVATION_OPEN", "live parent SM origin remains open"),
        ("VAL4444_5_future_contract_nonclaim", parent["PARENT4444_2_future_parent_contract"].get("current_status") == "PARENT_COMPONENT_DERIVATION_CONTRACT_READY_NONCLAIM", "future parent component contract executable nonclaim"),
        ("VAL4444_6_tail_smoke_pass", tails["REQ4444_3_small_smoke"].get("current_status") == "REQ_COMPACT_TEST_TAIL_SCHEMA_PASS_NONCLAIM", "small R_eq tail smoke row passes schema nonclaim"),
        ("VAL4444_7_tail_fail_control", tails["REQ4444_4_fail_control"].get("current_status") == "REQ_COMPACT_TEST_TAIL_FAILS_BOUND", "fail-control R_eq tail row fails bound"),
        ("VAL4444_8_live_req_targets", all(key in text(TAIL_OUTPUT) for key in ("REQ4444_0_compact_test_live", "REQ4444_1_req_multipole_live")), "live R_eq compact/multipole rows written"),
        ("VAL4444_9_no_claim_outputs", no_claims, "no output row is claim-ready"),
        ("VAL4444_10_claim_gate_no_claim", any(row["gate_id"] == "CG4444_8_no_public_claim" and row["passed"] == "True" for row in gates), "claim gate explicitly blocks public claim"),
        ("VAL4444_11_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-285"),
        ("VAL4444_12_formal_doc", paths["formal"].exists() and MARKER in text(paths["formal"]), "formal doc exists with marker"),
        ("VAL4444_13_post_doc", paths["post"].exists() and "Private checkpoint" in text(paths["post"]), "post checkpoint doc exists"),
        ("VAL4444_14_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4444_15_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4444_16_next_gate", any(row["gate_id"] == "CG4444_9_next_target_written" and row["passed"] == "True" for row in gates), "next target claim gate is true"),
        ("VAL4444_17_next_target", paths["next"].exists() and NEXT_TARGET in text(paths["next"]), "next target file exists"),
        ("VAL4444_18_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": bool(passed), "detail": detail} for check_id, passed, detail in checks]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(DERIVATION_ROWS, derivation_rows())
    write_csv(STANDARD_INPUT, standard_component_input_rows())
    write_csv(STANDARD_OUTPUT, evaluate_standard_component_rows(STANDARD_INPUT))
    write_csv(PARENT_INPUT, parent_component_input_rows())
    write_csv(PARENT_OUTPUT, evaluate_parent_component_rows(PARENT_INPUT))
    write_csv(TAIL_INPUT, tail_input_rows())
    write_csv(TAIL_OUTPUT, evaluate_tail_rows(TAIL_INPUT))
    write_csv(REDUCTION_ROWS, reduction_rows())
    write_csv(DECISION_CSV, decision_rows())
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    standard_outputs = rows_from(STANDARD_OUTPUT)
    parent_outputs = rows_from(PARENT_OUTPUT)
    tail_outputs = rows_from(TAIL_OUTPUT)
    gates = claim_gate_rows(standard_outputs, parent_outputs, tail_outputs)
    write_csv(CLAIM_GATES, gates)
    write_text(FORMAL_PATH, build_doc(rows_from(SOURCE_REGISTER), standard_outputs, parent_outputs, tail_outputs, gates))
    write_text(DOC_PATH, post_doc())
    update_claims_register()
    write_spine_and_packet()
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    write_csv(VALIDATION_PATH, validation_rows({"formal": FORMAL_PATH, "post": DOC_PATH, "next": NEXT_CSV}))


if __name__ == "__main__":
    main()

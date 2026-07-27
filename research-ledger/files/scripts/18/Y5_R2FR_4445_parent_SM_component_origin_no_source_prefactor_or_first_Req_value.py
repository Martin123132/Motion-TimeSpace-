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

from parent_sm_import_no_prefactor_gate import (  # noqa: E402
    evaluate_import_rows,
    evaluate_no_prefac_rows,
    evaluate_tail_rows,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4445"
CLAIM_ID = "L-286"
MARKER = "PPC4161_PARENT_SM_COMPONENT_ORIGIN_NO_SOURCE_PREFAC_OR_REQ_VALUE_4445"
PACKET_MARKER = "PPC4161_PACKET_GR_PARITY_SM_IMPORT_NO_SOURCE_PREFAC_4445"
DECISION = "GR_PARITY_STANDARD_MATTER_IMPORT_NO_SOURCE_PREFAC_THEOREM_READY_PARENT_ADOPTION_AND_MATERIAL_PROJECTION_REMAIN_NONCLAIM"
NEXT_TARGET = "4446-Y5-R2FR-adopt-GR-parity-SM-import-or-source-backed-material-Req-value.md"

FORMAL_PATH = FORMAL / "461-PPC4161-parent-SM-component-origin-no-source-prefactor-or-first-Req-value.md"
DOC_PATH = POST / "4445-Y5-R2FR-parent-SM-component-origin-no-source-prefactor-or-first-Req-value.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4445_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4445_SOURCE_REGISTER.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4445_DERIVATION_ROWS.csv"
IMPORT_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4445_GR_PARITY_SM_IMPORT_INPUT.csv"
IMPORT_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4445_GR_PARITY_SM_IMPORT_OUTPUT.csv"
NO_PREFAC_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4445_NO_SOURCE_PREFAC_INPUT.csv"
NO_PREFAC_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4445_NO_SOURCE_PREFAC_OUTPUT.csv"
COUNTERMODEL_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4445_COUNTERMODEL_ROWS.csv"
TAIL_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4445_REQ_COMPACT_TEST_TAIL_INPUT.csv"
TAIL_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4445_REQ_COMPACT_TEST_TAIL_OUTPUT.csv"
REDUCTION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4445_REDUCTION_ROWS.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4445_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4445_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4445_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4445_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "parent_sm_import_no_prefactor_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4445_parent_SM_component_origin_no_source_prefactor_or_first_Req_value.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4444 = SOURCE_DIR / "P8_Y5_R2FR_4444_NEXT_TARGET.csv"
FORMAL_460 = FORMAL / "460-PPC4161-standard-Lmatter-component-edge-expansion-or-Req-compact-test-value.md"
FORMAL_459 = FORMAL / "459-PPC4161-parent-owned-connected-nonEM-graph-edge-or-first-Req-compact-test-value.md"
FORMAL_451 = FORMAL / "451-PPC4161-parent-owned-action-density-graph-edge-certificate-or-first-Kmactionscale-source-leg.md"
FORMAL_439 = FORMAL / "439-PPC4161-action-density-line-owner-or-first-source-backed-Pwep-Req-value.md"
CORE_ACTION = ROOT / "core-mts-framework" / "action-principle" / "the-motion-timespace-action-principle.md"
FUND_ACTION = ROOT / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md"
OBJECT_LANGUAGE = SOURCE_DIR / "P8_Y5_R10_1338_OBJECT_LANGUAGE_THEOREM_ATTEMPT.csv"
TYPED_CERT = SOURCE_DIR / "P8_Y5_R10_1236_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv"
SOURCE_OWNER_CONTRACT = SOURCE_DIR / "P8_source_owner_parent_action_terms_CONTRACT.csv"
STANDARD_GRAPH_ATTEMPT = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1907_STANDARD_MATTER_EXCHANGE_GRAPH_SOURCE_BACKED_ATTEMPT.csv"
COMPONENT_OUTPUT_4444 = SOURCE_DIR / "P8_Y5_R2FR_4444_STANDARD_COMPONENT_EDGE_OUTPUT.csv"
POST_4378 = POST / "4378-Y5-R2FR-transition-topological-profile-moment-zero-or-first-multipole-bound-row.md"

SMOKE_BOUND = 1.0e-5
SMOKE_PASS_VALUE = 2.0e-7
SMOKE_FAIL_VALUE = 2.5e-3


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
        {"source_id": "SRC4445_00_next4444", "path": NEXT_4444, "needle": "4445-Y5-R2FR-parent-SM-component-origin-no-source-prefactor-or-first-Req-value.md", "role": "4444 handoff."},
        {"source_id": "SRC4445_01_460_formal", "path": FORMAL_460, "needle": "Imported standard-matter branch", "role": "4444 branch split."},
        {"source_id": "SRC4445_02_core_standard", "path": CORE_ACTION, "needle": "L_matter the standard matter Lagrangian", "role": "standard matter import slot."},
        {"source_id": "SRC4445_03_core_variation", "path": CORE_ACTION, "needle": "δ(L_matter √(-g)) = T_{μν}", "role": "Hilbert source variation."},
        {"source_id": "SRC4445_04_fund_action", "path": FUND_ACTION, "needle": "L_matter] √(-g)", "role": "fundamental action matter block."},
        {"source_id": "SRC4445_05_hom", "path": FORMAL_439, "needle": "Hom(SpeciesLabel, Coeff_active_source)=empty", "role": "no source-only species coefficient theorem."},
        {"source_id": "SRC4445_06_action_density_theorem", "path": FORMAL_439, "needle": "ADL4423_3_action_density_owner_theorem", "role": "source-weight zero theorem contract."},
        {"source_id": "SRC4445_07_edge_theorem", "path": FORMAL_451, "needle": "EDGE4435_0_parent_edge_certificate_theorem", "role": "component edge certificate theorem."},
        {"source_id": "SRC4445_08_object_language", "path": OBJECT_LANGUAGE, "needle": "OLT1338_1_typed_domain", "role": "typed coefficient domain precedent."},
        {"source_id": "SRC4445_09_source_forgetting", "path": TYPED_CERT, "needle": "CERT1236_5_source_label_forgetting", "role": "source label forgetting conditional lemma."},
        {"source_id": "SRC4445_10_selector_blind", "path": SOURCE_OWNER_CONTRACT, "needle": "A6_selector_blind_source_action", "role": "selector-blind source action contract."},
        {"source_id": "SRC4445_11_exchange_graph", "path": STANDARD_GRAPH_ATTEMPT, "needle": "SMG1907_1_exchange_theorem", "role": "connected exchange collapse theorem."},
        {"source_id": "SRC4445_12_component_outputs", "path": COMPONENT_OUTPUT_4444, "needle": "COMP4444_0_L_to_lepton_import", "role": "4444 component import rows."},
        {"source_id": "SRC4445_13_req_fallback", "path": POST_4378, "needle": "HARMONIC_NULL_MOMENT_ZERO_THEOREM", "role": "R_eq fallback theorem precedent."},
        {"source_id": "SRC4445_14_gate", "path": GATE_PATH, "needle": "def evaluate_no_prefac_row", "role": "4445 gate script."},
        {"source_id": "SRC4445_15_generator", "path": GENERATOR_PATH, "needle": 'CHECKPOINT = "4445"', "role": "4445 generator script."},
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
            "derivation_id": "SMIMP4445_0_GR_parity_import_principle",
            "claim": "MTS need not derive the Standard Model to reduce to local GR; it must couple universally to the same imported matter action GR uses.",
            "derivation": "GR recovers local source coupling by varying a diffeomorphic matter action under the metric measure, not by deriving lepton, quark, gauge or Yukawa sectors. Therefore the fair MTS->GR requirement is a GR-parity import: a single parent-owned imported S_matter[g,psi;c_i] with fixed internal constants c_i and Hilbert variation before readout.",
            "consequence": "This avoids the impossible bar of deriving all microphysics while still forbidding cheating through source-only weights.",
            "status": "EXACT_REDUCTION_REQUIREMENT_REFRAMED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "SMIMP4445_1_no_source_prefactor_theorem",
            "claim": "A source-only component multiplier is illegal once the imported matter action is a single typed functor.",
            "derivation": "Let I_SM map geometry/coframe, matter fields, gauge fields, representation constants and universal constants to one scalar density. If Coeff_active_source has no SpeciesLabel or MaterialLabel argument and source labels are forgotten before Hilbert variation, then w_A L_A cannot be introduced except as one common calibration; it would require a forbidden morphism SpeciesLabel -> Coeff_active_source.",
            "consequence": "Delta_w_A=0 follows conditionally from typed import + no-Hom + connected component graph + no readout reentry.",
            "status": "CONDITIONAL_THEOREM_READY",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "SMIMP4445_2_countermodel_if_no_prefac_missing",
            "claim": "Without the no-source-prefactor clause, the local branch can fail even with total T_H.",
            "derivation": "A countermodel S_matter=sum_A w_A S_A uses the same metric variation and can still create a total Hilbert stress, but composition-dependent weights survive unless w_A are common. Therefore total T_H and component templates are insufficient.",
            "consequence": "The no-source-prefactor theorem is not bureaucracy; it is the exact place where WEP/PPN source universality can break.",
            "status": "COUNTERMODEL_RETAINED_AS_GUARD",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "SMIMP4445_3_material_projection_scope",
            "claim": "Material projections are empirical source inventory, not fundamental source weights.",
            "derivation": "Ti/Pt, clocks and orbital bodies need source-backed isotope/binding/material projection tensors for scoring, but those tensors live in the readout/inventory layer. They must not feed back into the active gravitational source coefficient.",
            "consequence": "The route splits cleanly: adopt the GR-parity import/no-prefactor theorem for source universality, then source material projections only for empirical residual tests.",
            "status": "READOUT_SCOPE_SEPARATED",
            "valid_for_claim": False,
        },
    ]


def import_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "IMP4445_0_live_core_GR_parity_import",
            "branch": "live_core_standard_matter_import",
            "object": "single imported S_matter action under MTS parent/effective action",
            "standard_lmatter_slot_present": True,
            "total_hilbert_variation_signed": True,
            "component_import_edges_ready": True,
            "single_metric_measure": True,
            "matter_internal_constants_quarantined": True,
            "parent_import_clause_written": True,
            "variation_before_readout": True,
            "no_component_source_weight_in_import": True,
            "adopted_by_parent": False,
            "source_path": str(CORE_ACTION),
            "public_authority": False,
            "input_valid_for_claim": False,
            "notes": "Theorem-ready as a GR-parity import route; nonclaim until formally adopted as parent/effective branch policy.",
        },
        {
            "row_id": "IMP4445_1_total_T_only_control",
            "branch": "control_total_stress_only",
            "object": "total T_H without component no-source-prefactor",
            "standard_lmatter_slot_present": True,
            "total_hilbert_variation_signed": True,
            "component_import_edges_ready": False,
            "single_metric_measure": True,
            "matter_internal_constants_quarantined": False,
            "parent_import_clause_written": False,
            "variation_before_readout": True,
            "no_component_source_weight_in_import": False,
            "adopted_by_parent": False,
            "source_path": str(FORMAL_459),
            "public_authority": False,
            "input_valid_for_claim": False,
            "notes": "Control row proves total Hilbert stress alone is not enough.",
        },
        {
            "row_id": "IMP4445_2_future_adopted_import_contract",
            "branch": "future_parent_adopted_GR_parity_import",
            "object": "adopted single imported standard matter functor with fixed internal constants",
            "standard_lmatter_slot_present": True,
            "total_hilbert_variation_signed": True,
            "component_import_edges_ready": True,
            "single_metric_measure": True,
            "matter_internal_constants_quarantined": True,
            "parent_import_clause_written": True,
            "variation_before_readout": True,
            "no_component_source_weight_in_import": True,
            "adopted_by_parent": True,
            "source_path": str(FORMAL_460),
            "public_authority": False,
            "input_valid_for_claim": False,
            "notes": "Exact future adoption contract; not public/claim-valid yet.",
        },
    ]


def no_prefac_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "NP4445_0_live_no_source_prefac_route",
            "branch": "live_GR_parity_no_source_prefac_route",
            "object": "forbid source-only species/material weights in active source coefficients",
            "typed_domain_declared": True,
            "hom_species_to_source_empty": True,
            "action_density_line_unique": True,
            "source_label_forgetting": True,
            "selector_blind_source_action": True,
            "component_graph_connected_import": True,
            "readout_no_reentry": True,
            "material_projection_scope_declared": True,
            "adopted_by_parent": False,
            "source_path": str(FORMAL_439),
            "public_authority": False,
            "input_valid_for_claim": False,
            "notes": "Conditional theorem is complete as a route, but parent adoption/public claim remains false.",
        },
        {
            "row_id": "NP4445_1_live_corpus_strict_parent_derivation",
            "branch": "strict_MTS_primitive_derivation",
            "object": "derive no-source-prefactor directly from motion/time/space primitives",
            "typed_domain_declared": True,
            "hom_species_to_source_empty": False,
            "action_density_line_unique": True,
            "source_label_forgetting": False,
            "selector_blind_source_action": False,
            "component_graph_connected_import": True,
            "readout_no_reentry": False,
            "material_projection_scope_declared": False,
            "adopted_by_parent": False,
            "source_path": str(OBJECT_LANGUAGE),
            "public_authority": False,
            "input_valid_for_claim": False,
            "notes": "Strict primitive derivation is still not present in the corpus.",
        },
        {
            "row_id": "NP4445_2_future_adopted_no_prefac_contract",
            "branch": "future_adopted_no_source_prefac_contract",
            "object": "parent-adopted empty Hom and source-label-forgetting theorem",
            "typed_domain_declared": True,
            "hom_species_to_source_empty": True,
            "action_density_line_unique": True,
            "source_label_forgetting": True,
            "selector_blind_source_action": True,
            "component_graph_connected_import": True,
            "readout_no_reentry": True,
            "material_projection_scope_declared": True,
            "adopted_by_parent": True,
            "source_path": str(SOURCE_OWNER_CONTRACT),
            "public_authority": False,
            "input_valid_for_claim": False,
            "notes": "Exact future adoption contract; nonclaim until promoted by a parent action decision and source audit.",
        },
    ]


def countermodel_rows() -> List[Dict[str, object]]:
    return [
        {
            "countermodel_id": "CM4445_0_weighted_components",
            "assumption_removed": "no_component_source_weight_in_import",
            "construction": "S_matter = sum_A w_A S_A with w_A not all equal",
            "survives_4443_total_T": True,
            "survives_4444_component_templates": True,
            "killed_by_4445_theorem": True,
            "lesson": "Total Hilbert stress plus component templates do not force WEP/source universality; the no-source-prefactor theorem is necessary.",
            "valid_for_claim": False,
        },
        {
            "countermodel_id": "CM4445_1_material_reentry",
            "assumption_removed": "readout_no_reentry",
            "construction": "material projection tensor feeds back into active source coefficient after readout",
            "survives_4443_total_T": True,
            "survives_4444_component_templates": True,
            "killed_by_4445_theorem": True,
            "lesson": "Empirical material projections must remain readout inventory, not source couplings.",
            "valid_for_claim": False,
        },
    ]


def tail_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "tail_id": "REQ4445_0_compact_test_live",
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
            "notes": "Fallback remains value-missing if import/no-prefactor adoption is rejected.",
        },
        {
            "tail_id": "REQ4445_1_material_projection_live",
            "quantity": "material_projection_Req",
            "arena": "WEP_clock_orbital_material_inventory",
            "distributional_definition": "R_material=Pi_material(T_H)-Pi_material(T_inventory)",
            "projection_coeff": "MISSING_MATERIAL_PROJECTION_COEFF",
            "tail_value": "MISSING_MATERIAL_RESIDUAL_VALUE",
            "arena_bound": "MISSING_ARENA_BOUND",
            "units": "dimensionless_or_source_fraction",
            "source_path": str(STANDARD_GRAPH_ATTEMPT),
            "public_authority": False,
            "input_valid_for_claim": False,
            "notes": "Material projection is now scoped as readout inventory and still needs source-backed rows.",
        },
        {
            "tail_id": "REQ4445_2_zero_smoke",
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
            "tail_id": "REQ4445_3_small_smoke",
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
            "tail_id": "REQ4445_4_fail_control",
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
            "reduction_id": "RED4445_0_not_SM_derivation",
            "from_problem": "derive every Standard Model component from MTS",
            "to_problem": "GR-parity import plus universal no-source-prefactor coupling",
            "status": "REDUCED_TO_FAIR_GR_PARITY_REQUIREMENT",
            "reason": "Local GR reduction does not require deriving microphysics; it requires universal coupling to a diffeomorphic matter action.",
            "valid_for_claim": False,
        },
        {
            "reduction_id": "RED4445_1_no_prefac_exact_lock",
            "from_problem": "component source universality",
            "to_problem": "empty Hom from source/species labels into active source coefficients",
            "status": "NO_SOURCE_PREFAC_LOCK_IDENTIFIED",
            "reason": "A hidden w_A source multiplier is the actual mathematical loophole.",
            "valid_for_claim": False,
        },
        {
            "reduction_id": "RED4445_2_material_scope",
            "from_problem": "material projection gap",
            "to_problem": "readout inventory/source-backed residual values",
            "status": "MATERIAL_PROJECTION_MOVED_TO_EMPIRICAL_SCORING",
            "reason": "Material fractions can be needed for WEP/clock/orbital tests without becoming fundamental source couplings.",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(import_outputs: Sequence[Mapping[str, str]], no_prefac_outputs: Sequence[Mapping[str, str]], tail_outputs: Sequence[Mapping[str, str]]) -> List[Dict[str, object]]:
    imports = {row["row_id"]: row for row in import_outputs}
    noprefac = {row["row_id"]: row for row in no_prefac_outputs}
    tails = {row["tail_id"]: row for row in tail_outputs}
    no_claim = not any(row.get("valid_for_claim") == "True" for row in import_outputs) and not any(row.get("valid_for_claim") == "True" for row in no_prefac_outputs) and not any(row.get("valid_for_claim") == "True" for row in tail_outputs)
    return [
        {"gate_id": "CG4445_0_sources_exist", "claim": "all cited source paths exist", "passed": all(row["path_exists"] == "True" for row in rows_from(SOURCE_REGISTER)), "valid_for_claim": False, "detail": "Source register path-backed."},
        {"gate_id": "CG4445_1_needles_found", "claim": "all cited source needles found", "passed": all(row["needle_found"] == "True" for row in rows_from(SOURCE_REGISTER)), "valid_for_claim": False, "detail": "No unsourced import."},
        {"gate_id": "CG4445_2_GR_parity_import_ready", "claim": "GR-parity standard matter import theorem is ready", "passed": imports["IMP4445_0_live_core_GR_parity_import"].get("current_status") == "GR_PARITY_SM_IMPORT_THEOREM_READY_ADOPTION_OPEN_NONCLAIM", "valid_for_claim": False, "detail": "MTS can fairly import ordinary matter like GR, if adopted."},
        {"gate_id": "CG4445_3_total_T_control_rejected", "claim": "total T_H alone remains insufficient", "passed": imports["IMP4445_1_total_T_only_control"].get("current_status") == "GR_PARITY_SM_IMPORT_SOURCE_PRESENT_CLAUSES_OPEN", "valid_for_claim": False, "detail": "Countermodel survives without component/no-prefactor clauses."},
        {"gate_id": "CG4445_4_no_prefac_theorem_ready", "claim": "no-source-prefactor theorem route is ready", "passed": noprefac["NP4445_0_live_no_source_prefac_route"].get("current_status") == "NO_SOURCE_PREFAC_THEOREM_READY_ADOPTION_OPEN_NONCLAIM", "valid_for_claim": False, "detail": "Empty-Hom/source-label-forgetting theorem can kill w_A if adopted."},
        {"gate_id": "CG4445_5_strict_primitive_derivation_blocked", "claim": "strict primitive derivation remains blocked", "passed": noprefac["NP4445_1_live_corpus_strict_parent_derivation"].get("current_status") == "NO_SOURCE_PREFAC_PARTIAL_TYPED_ACTION_READY", "valid_for_claim": False, "detail": "Motion/time/space primitive derivation is still not in corpus."},
        {"gate_id": "CG4445_6_countermodels_written", "claim": "countermodels are explicitly recorded", "passed": all(key in text(COUNTERMODEL_ROWS) for key in ("CM4445_0_weighted_components", "CM4445_1_material_reentry")), "valid_for_claim": False, "detail": "Guards prevent smuggling closure."},
        {"gate_id": "CG4445_7_tail_controls", "claim": "R_eq tail gate has pass and fail controls", "passed": tails["REQ4445_3_small_smoke"].get("current_status") == "REQ_COMPACT_TEST_TAIL_SCHEMA_PASS_NONCLAIM" and tails["REQ4445_4_fail_control"].get("current_status") == "REQ_COMPACT_TEST_TAIL_FAILS_BOUND", "valid_for_claim": False, "detail": "Tail gate catches safe/failing controls."},
        {"gate_id": "CG4445_8_live_req_targets", "claim": "live R_eq/material targets written", "passed": all(key in tails for key in ("REQ4445_0_compact_test_live", "REQ4445_1_material_projection_live")), "valid_for_claim": False, "detail": "Live rows still require values/projections."},
        {"gate_id": "CG4445_9_no_public_claim", "claim": "4445 emits no local-GR/Newton/PPN public claim", "passed": no_claim, "valid_for_claim": False, "detail": "All outputs remain private nonclaim."},
        {"gate_id": "CG4445_10_next_target_written", "claim": "next target selected", "passed": NEXT_CSV.exists() and NEXT_TARGET in text(NEXT_CSV), "valid_for_claim": False, "detail": NEXT_TARGET},
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4445_0",
            "decision": DECISION,
            "summary": "4445 derives the fair less-scrutiny route: MTS does not need to derive all Standard Model microphysics to reduce to GR, because GR itself imports S_matter. The required theorem is a GR-parity imported standard matter functor with fixed internal constants, Hilbert variation before readout, and an empty-Hom/no-source-prefactor/source-label-forgetting rule that forbids w_A component source weights. This kills the main component-weight loophole conditionally, but remains nonclaim until the import/no-prefactor clause is formally parent-adopted and material projections are sourced only as readout inventory. Strict primitive derivation from motion/time/space remains open.",
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
            "root_result": "GR-parity standard matter import and no-source-prefactor theorem route ready",
            "still_missing": "formal parent adoption; strict primitive derivation; source-backed material projection/R_eq values",
            "next_target": NEXT_TARGET,
            "public_claim": False,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4445_0",
            "target": NEXT_TARGET,
            "objective": "Either formally adopt the GR-parity SM import/no-source-prefactor theorem as the local branch, or fill source-backed material/R_eq residual values.",
            "derive_first": "write the adoption invariant: imported S_matter is one scalar density functor, internal constants are not source labels, Hom(SpeciesLabel,Coeff_active_source)=empty, and readout/material projections cannot re-enter the active source coefficient",
            "fallback": "fill material projection or R_eq compact-test value with units, projection coefficient, arena bound, source path and no-cancellation guard",
            "risk": "turning a fair GR-parity import into an overclaim that MTS derives the Standard Model; letting material readout re-enter as a source coefficient",
            "valid_for_claim": False,
        }
    ]


def build_doc(sources: Sequence[Mapping[str, object]], import_outputs: Sequence[Mapping[str, object]], no_prefac_outputs: Sequence[Mapping[str, object]], tail_outputs: Sequence[Mapping[str, object]], gates: Sequence[Mapping[str, object]]) -> str:
    return f"""# 461 PPC4161 parent SM component origin no-source-prefactor or first Req value

Marker: `{MARKER}`

Decision: `{DECISION}`

Claim register: `{CLAIM_ID}`

## Result

4445 takes the less-scrutiny route and derives a fair GR-parity theorem:

```text
MTS does not need to derive every Standard Model term to reduce to local GR.
It needs a single imported matter action S_matter[g,psi;c_i],
varied before readout, with fixed internal constants c_i,
and no morphism from SpeciesLabel/MaterialLabel into active source coefficients.
```

That is enough to kill hidden component weights `w_A` **if parent-adopted**. The strict primitive derivation from motion/time/space is still open, so this remains private nonclaim. But the target has moved forward: the next lock is formal adoption of this GR-parity import/no-source-prefactor invariant, not a demand to derive all particle physics in one step.

## Source Register

{table(sources)}

## Derivation Rows

{table(rows_from(DERIVATION_ROWS))}

## GR-Parity Standard Matter Import Gate

{table(import_outputs)}

## No-Source-Prefactor Gate

{table(no_prefac_outputs)}

## Countermodel Rows

{table(rows_from(COUNTERMODEL_ROWS))}

## R_eq / Material Tail Gate

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
    return f"""# 4445 Y5 R2FR parent SM component origin no-source-prefactor or first Req value

Private checkpoint generated at `{STAMP}`.

Summary:
- Derived the fair GR-parity route: MTS can reduce to local GR by importing one standard matter action, as GR does, rather than deriving all microphysics.
- The exact no-source-prefactor theorem is now stated: fixed internal matter constants are allowed, but species/material labels cannot map into active source coefficients.
- This kills hidden `w_A` component weights only if parent-adopted; strict primitive derivation and source-backed material/R_eq values remain open.

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
        "claim": "4445 derives the fair GR-parity route: MTS need not derive all SM microphysics to reduce to local GR; it needs one imported standard matter action with fixed internal constants, Hilbert variation before readout, and an empty-Hom/no-source-prefactor/source-label-forgetting theorem forbidding source-only component weights. This is theorem-ready but nonclaim until parent-adopted and material/R_eq values are sourced.",
        "current_evidence": "4445 source register, derivation rows, GR-parity import gate, no-source-prefactor gate, countermodels, R_eq/material tail gate, reduction rows, claim gates, decision, status, next target and validation CSV.",
        "status": "GR_parity_standard_matter_import_no_source_prefac_theorem_ready_parent_adoption_and_material_projection_open_nonclaim",
        "next_test": "Adopt GR-parity SM import/no-source-prefactor invariant or fill first source-backed material/R_eq residual value.",
        "key_risk": "Overclaiming MTS derives the Standard Model; letting material/readout labels re-enter as active source coefficients.",
        "sector": "local_gr_source_coupling",
        "evidence": "4445 source register, derivation rows, GR-parity import gate, no-source-prefactor gate, countermodels, R_eq/material tail gate, reduction rows, claim gates, decision, status, next target and validation CSV.",
        "next_action": "Adopt GR-parity SM import/no-source-prefactor invariant or fill first source-backed material/R_eq residual value.",
        "risk": "Overclaiming MTS derives the Standard Model; letting material/readout labels re-enter as active source coefficients.",
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
    spine_section = f"""## Local GR Source Coupling Update - GR-Parity SM Import No-Source-Prefactor Route

Marker: `{MARKER}`  
Source checkpoint: `4445-Y5-R2FR-parent-SM-component-origin-no-source-prefactor-or-first-Req-value.md`  
Claim register row: `{CLAIM_ID}`

4445 reframes the Standard Model origin blocker into a fair local-GR reduction requirement. MTS does not need to derive every matter microterm to match GR; it needs to parent-adopt a single imported standard matter action with fixed internal constants and no source-only species/material coefficient. The theorem route is now explicit: typed import + empty Hom from source labels to active source coefficients + source-label forgetting + connected component import + readout no-reentry implies no hidden `w_A` component weights. This remains private nonclaim until adopted and material/R_eq residual values are sourced.
"""
    packet_section = f"""## PPC4161 Packet Addendum - GR-Parity SM Import No-Source-Prefactor Route

Marker: `{PACKET_MARKER}`  
Source checkpoint: `4445-Y5-R2FR-parent-SM-component-origin-no-source-prefactor-or-first-Req-value.md`

The packet may use a GR-parity standard matter import route: one imported `S_matter[g,psi;c_i]` is acceptable for local-GR reduction if all internal constants are quarantined as matter data and no SpeciesLabel/MaterialLabel can map into active source coefficients. Do not claim strict MTS derivation of the Standard Model. If the adoption invariant is rejected, score source-backed material or same-current `R_eq` residuals.
"""
    append_marker_section(SPINE_PATH, MARKER, spine_section)
    append_marker_section(PACKET_PATH, PACKET_MARKER, packet_section)


def validation_rows(paths: Mapping[str, Path]) -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    imports = {row["row_id"]: row for row in rows_from(IMPORT_OUTPUT)}
    noprefac = {row["row_id"]: row for row in rows_from(NO_PREFAC_OUTPUT)}
    tails = {row["tail_id"]: row for row in rows_from(TAIL_OUTPUT)}
    gates = rows_from(CLAIM_GATES)
    no_claims = not any(row.get("valid_for_claim") == "True" for row in imports.values()) and not any(row.get("valid_for_claim") == "True" for row in noprefac.values()) and not any(row.get("valid_for_claim") == "True" for row in tails.values())
    checks = [
        ("VAL4445_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source path exists"),
        ("VAL4445_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited source needle is present"),
        ("VAL4445_2_GR_parity_import_ready", imports["IMP4445_0_live_core_GR_parity_import"].get("current_status") == "GR_PARITY_SM_IMPORT_THEOREM_READY_ADOPTION_OPEN_NONCLAIM", "GR-parity import route theorem-ready nonclaim"),
        ("VAL4445_3_total_T_control_rejected", imports["IMP4445_1_total_T_only_control"].get("current_status") == "GR_PARITY_SM_IMPORT_SOURCE_PRESENT_CLAUSES_OPEN", "total T_H alone rejected as insufficient"),
        ("VAL4445_4_no_prefac_ready", noprefac["NP4445_0_live_no_source_prefac_route"].get("current_status") == "NO_SOURCE_PREFAC_THEOREM_READY_ADOPTION_OPEN_NONCLAIM", "no-source-prefactor route theorem-ready nonclaim"),
        ("VAL4445_5_strict_derivation_blocked", noprefac["NP4445_1_live_corpus_strict_parent_derivation"].get("current_status") == "NO_SOURCE_PREFAC_PARTIAL_TYPED_ACTION_READY", "strict primitive derivation remains blocked"),
        ("VAL4445_6_countermodels_written", all(key in text(COUNTERMODEL_ROWS) for key in ("CM4445_0_weighted_components", "CM4445_1_material_reentry")), "countermodels written"),
        ("VAL4445_7_tail_smoke_pass", tails["REQ4445_3_small_smoke"].get("current_status") == "REQ_COMPACT_TEST_TAIL_SCHEMA_PASS_NONCLAIM", "small R_eq tail smoke row passes schema nonclaim"),
        ("VAL4445_8_tail_fail_control", tails["REQ4445_4_fail_control"].get("current_status") == "REQ_COMPACT_TEST_TAIL_FAILS_BOUND", "fail-control R_eq tail row fails bound"),
        ("VAL4445_9_live_req_targets", all(key in text(TAIL_OUTPUT) for key in ("REQ4445_0_compact_test_live", "REQ4445_1_material_projection_live")), "live R_eq/material rows written"),
        ("VAL4445_10_no_claim_outputs", no_claims, "no output row is claim-ready"),
        ("VAL4445_11_claim_gate_no_claim", any(row["gate_id"] == "CG4445_9_no_public_claim" and row["passed"] == "True" for row in gates), "claim gate explicitly blocks public claim"),
        ("VAL4445_12_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-286"),
        ("VAL4445_13_formal_doc", paths["formal"].exists() and MARKER in text(paths["formal"]), "formal doc exists with marker"),
        ("VAL4445_14_post_doc", paths["post"].exists() and "Private checkpoint" in text(paths["post"]), "post checkpoint doc exists"),
        ("VAL4445_15_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4445_16_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4445_17_next_gate", any(row["gate_id"] == "CG4445_10_next_target_written" and row["passed"] == "True" for row in gates), "next target claim gate is true"),
        ("VAL4445_18_next_target", paths["next"].exists() and NEXT_TARGET in text(paths["next"]), "next target file exists"),
        ("VAL4445_19_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": bool(passed), "detail": detail} for check_id, passed, detail in checks]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(DERIVATION_ROWS, derivation_rows())
    write_csv(IMPORT_INPUT, import_input_rows())
    write_csv(IMPORT_OUTPUT, evaluate_import_rows(IMPORT_INPUT))
    write_csv(NO_PREFAC_INPUT, no_prefac_input_rows())
    write_csv(NO_PREFAC_OUTPUT, evaluate_no_prefac_rows(NO_PREFAC_INPUT))
    write_csv(COUNTERMODEL_ROWS, countermodel_rows())
    write_csv(TAIL_INPUT, tail_input_rows())
    write_csv(TAIL_OUTPUT, evaluate_tail_rows(TAIL_INPUT))
    write_csv(REDUCTION_ROWS, reduction_rows())
    write_csv(DECISION_CSV, decision_rows())
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    import_outputs = rows_from(IMPORT_OUTPUT)
    no_prefac_outputs = rows_from(NO_PREFAC_OUTPUT)
    tail_outputs = rows_from(TAIL_OUTPUT)
    gates = claim_gate_rows(import_outputs, no_prefac_outputs, tail_outputs)
    write_csv(CLAIM_GATES, gates)
    write_text(FORMAL_PATH, build_doc(rows_from(SOURCE_REGISTER), import_outputs, no_prefac_outputs, tail_outputs, gates))
    write_text(DOC_PATH, post_doc())
    update_claims_register()
    write_spine_and_packet()
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    write_csv(VALIDATION_PATH, validation_rows({"formal": FORMAL_PATH, "post": DOC_PATH, "next": NEXT_CSV}))


if __name__ == "__main__":
    main()

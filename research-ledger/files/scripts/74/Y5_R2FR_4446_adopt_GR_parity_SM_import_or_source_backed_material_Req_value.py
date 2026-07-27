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

from gr_parity_import_adoption_gate import (  # noqa: E402
    evaluate_adoption_rows,
    evaluate_material_rows,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4446"
CLAIM_ID = "L-288"
MARKER = "PPC4161_ADOPT_GR_PARITY_SM_IMPORT_OR_SOURCE_BACKED_MATERIAL_REQ_4446"
PACKET_MARKER = "PPC4161_PACKET_ADOPTED_GR_PARITY_SM_IMPORT_4446"
DECISION = "GR_PARITY_STANDARD_MATTER_IMPORT_PRIVATE_BRANCH_ADOPTED_STRICT_PRIMITIVE_AND_MATERIAL_VALUES_REMAIN_NONCLAIM"
NEXT_TARGET = "4447-Y5-R2FR-GR-parity-source-universality-to-local-PPN-residual-vector-or-material-values.md"

FORMAL_PATH = FORMAL / "462-PPC4161-adopt-GR-parity-SM-import-or-source-backed-material-Req-value.md"
DOC_PATH = POST / "4446-Y5-R2FR-adopt-GR-parity-SM-import-or-source-backed-material-Req-value.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4446_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4446_SOURCE_REGISTER.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4446_DERIVATION_ROWS.csv"
ADOPTION_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4446_GR_PARITY_ADOPTION_INPUT.csv"
ADOPTION_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4446_GR_PARITY_ADOPTION_OUTPUT.csv"
MATERIAL_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4446_MATERIAL_REQ_INPUT.csv"
MATERIAL_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4446_MATERIAL_REQ_OUTPUT.csv"
RESIDUAL_VECTOR = SOURCE_DIR / "P8_Y5_R2FR_4446_SOURCE_UNIVERSALITY_RESIDUAL_VECTOR.csv"
COUNTERMODEL_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4446_COUNTERMODEL_STATUS.csv"
REDUCTION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4446_REDUCTION_ROWS.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4446_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4446_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4446_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4446_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "gr_parity_import_adoption_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4446_adopt_GR_parity_SM_import_or_source_backed_material_Req_value.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4445 = SOURCE_DIR / "P8_Y5_R2FR_4445_NEXT_TARGET.csv"
FORMAL_461 = FORMAL / "461-PPC4161-parent-SM-component-origin-no-source-prefactor-or-first-Req-value.md"
FORMAL_460 = FORMAL / "460-PPC4161-standard-Lmatter-component-edge-expansion-or-Req-compact-test-value.md"
FORMAL_459 = FORMAL / "459-PPC4161-parent-owned-connected-nonEM-graph-edge-or-first-Req-compact-test-value.md"
FORMAL_439 = FORMAL / "439-PPC4161-action-density-line-owner-or-first-source-backed-Pwep-Req-value.md"
CORE_ACTION = ROOT / "core-mts-framework" / "action-principle" / "the-motion-timespace-action-principle.md"
FUND_ACTION = ROOT / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md"
SOURCE_OWNER_CONTRACT = SOURCE_DIR / "P8_source_owner_parent_action_terms_CONTRACT.csv"
TYPED_CERT = SOURCE_DIR / "P8_Y5_R10_1236_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv"
OBJECT_LANGUAGE = SOURCE_DIR / "P8_Y5_R10_1338_OBJECT_LANGUAGE_THEOREM_ATTEMPT.csv"
STANDARD_GRAPH_ATTEMPT = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1907_STANDARD_MATTER_EXCHANGE_GRAPH_SOURCE_BACKED_ATTEMPT.csv"
COUNTERMODELS_4445 = SOURCE_DIR / "P8_Y5_R2FR_4445_COUNTERMODEL_ROWS.csv"
IMPORT_OUTPUT_4445 = SOURCE_DIR / "P8_Y5_R2FR_4445_GR_PARITY_SM_IMPORT_OUTPUT.csv"
NO_PREFAC_OUTPUT_4445 = SOURCE_DIR / "P8_Y5_R2FR_4445_NO_SOURCE_PREFAC_OUTPUT.csv"
POST_4378 = POST / "4378-Y5-R2FR-transition-topological-profile-moment-zero-or-first-multipole-bound-row.md"


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
        {"source_id": "SRC4446_00_next4445", "path": NEXT_4445, "needle": "4446-Y5-R2FR-adopt-GR-parity-SM-import-or-source-backed-material-Req-value.md", "role": "4445 handoff."},
        {"source_id": "SRC4446_01_461_formal", "path": FORMAL_461, "needle": "GR_PARITY_STANDARD_MATTER_IMPORT_NO_SOURCE_PREFAC_THEOREM_READY", "role": "4445 theorem-ready result."},
        {"source_id": "SRC4446_02_private_packet", "path": PACKET_PATH, "needle": "For the compact isolated local `<=2PN` same-source branch, adopt privately", "role": "PPC4161 private adoption precedent."},
        {"source_id": "SRC4446_03_core_standard", "path": CORE_ACTION, "needle": "L_matter the standard matter Lagrangian", "role": "standard matter import slot."},
        {"source_id": "SRC4446_04_core_variation", "path": CORE_ACTION, "needle": "δ(L_matter √(-g)) = T_{μν}", "role": "Hilbert variation before readout."},
        {"source_id": "SRC4446_05_fund_action", "path": FUND_ACTION, "needle": "L_matter] √(-g)", "role": "fundamental matter block."},
        {"source_id": "SRC4446_06_hom", "path": FORMAL_439, "needle": "Hom(SpeciesLabel, Coeff_active_source)=empty", "role": "empty-Hom no-source-slot theorem."},
        {"source_id": "SRC4446_07_component_import", "path": FORMAL_460, "needle": "standard component import graph contract written", "role": "component import graph already staged."},
        {"source_id": "SRC4446_08_total_edge", "path": FORMAL_459, "needle": "L_matter -> T_H", "role": "total Hilbert stress root edge."},
        {"source_id": "SRC4446_09_source_forgetting", "path": TYPED_CERT, "needle": "CERT1236_5_source_label_forgetting", "role": "source-label forgetting lemma."},
        {"source_id": "SRC4446_10_selector_blind", "path": SOURCE_OWNER_CONTRACT, "needle": "A6_selector_blind_source_action", "role": "selector-blind source action contract."},
        {"source_id": "SRC4446_11_object_language_verdict", "path": OBJECT_LANGUAGE, "needle": "NOT_DERIVED_CURRENT_CORPUS", "role": "strict primitive derivation remains open."},
        {"source_id": "SRC4446_12_material_graph", "path": STANDARD_GRAPH_ATTEMPT, "needle": "MATERIAL_PROJECTION_NOT_SOURCED", "role": "material projection fallback remains unsourced."},
        {"source_id": "SRC4446_13_countermodels", "path": COUNTERMODELS_4445, "needle": "CM4445_0_weighted_components", "role": "countermodel guard rows."},
        {"source_id": "SRC4446_14_import_output", "path": IMPORT_OUTPUT_4445, "needle": "IMP4445_0_live_core_GR_parity_import", "role": "4445 GR-parity import gate."},
        {"source_id": "SRC4446_15_no_prefac_output", "path": NO_PREFAC_OUTPUT_4445, "needle": "NP4445_0_live_no_source_prefac_route", "role": "4445 no-source-prefactor gate."},
        {"source_id": "SRC4446_16_req_fallback", "path": POST_4378, "needle": "HARMONIC_NULL_MOMENT_ZERO_THEOREM", "role": "R_eq fallback theorem."},
        {"source_id": "SRC4446_17_gate", "path": GATE_PATH, "needle": "def evaluate_adoption_row", "role": "4446 adoption gate script."},
        {"source_id": "SRC4446_18_generator", "path": GENERATOR_PATH, "needle": 'CHECKPOINT = "4446"', "role": "4446 generator script."},
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
            "derivation_id": "ADOPT4446_0_private_branch_adoption",
            "claim": "The GR-parity SM import/no-source-prefactor invariant can be adopted inside the private PPC4161 local branch.",
            "derivation": "PPC4161 already uses private scoped adoption for local packet clauses. 4445 provides the theorem-ready invariant: one imported S_matter, Hilbert variation before readout, component import graph, empty Hom from source labels into active source coefficients, source-label forgetting, readout no-reentry and public-claim false. Therefore the invariant is adoptable as a private local branch rule, not as global MTS or public local-GR proof.",
            "consequence": "Inside PPC4161, hidden component source weights w_A are no longer an active residual; the strict primitive derivation and empirical material/R_eq values remain live obligations.",
            "status": "PRIVATE_BRANCH_ADOPTION_DERIVED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "ADOPT4446_1_weight_countermodel_killed",
            "claim": "The weighted-component countermodel is killed inside the adopted private branch.",
            "derivation": "The countermodel S_matter=sum_A w_A S_A requires a morphism from component/source labels to an active source coefficient. The adopted invariant declares that morphism absent and quarantines representation/mass/charge constants as matter data rather than source labels.",
            "consequence": "Delta_w_A=0 becomes branch-internal, conditional on PPC4161-GR-parity adoption.",
            "status": "WEIGHTED_COMPONENT_COUNTERMODEL_KILLED_IN_PRIVATE_BRANCH",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "ADOPT4446_2_material_reentry_killed",
            "claim": "Material projection cannot re-enter the active source coefficient inside the adopted branch.",
            "derivation": "Material/isotope/binding tensors are readout inventory for WEP/clock/orbital scoring. They are explicitly barred from the active gravitational source coefficient by the selector-blind/source-label-forgetting invariant.",
            "consequence": "Material data are still needed for empirical residual tests, but not as fundamental source weights.",
            "status": "MATERIAL_REENTRY_COUNTERMODEL_KILLED_IN_PRIVATE_BRANCH",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "ADOPT4446_3_public_claim_guard",
            "claim": "Private adoption does not equal public local-GR completion.",
            "derivation": "The strict derivation from motion/time/space primitives remains explicitly false in 1338, and material/R_eq residual values are still missing. Therefore 4446 closes one private branch residual while preserving all public claim guards.",
            "consequence": "The next proof target can push the adopted source-universality invariant into the local PPN residual vector, or fill material/R_eq values if adoption is rejected.",
            "status": "PUBLIC_CLAIM_BLOCK_RETAINED",
            "valid_for_claim": False,
        },
    ]


def adoption_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "ADOPT4446_0_PPC4161_GR_parity_import",
            "branch": "PPC4161_private_local_branch",
            "invariant": "one imported S_matter scalar density functor with no SpeciesLabel/MaterialLabel -> Coeff_active_source morphism",
            "private_scope_declared": True,
            "standard_lmatter_slot_present": True,
            "hilbert_variation_before_readout": True,
            "component_import_graph_ready": True,
            "no_source_prefactor_theorem_ready": True,
            "source_label_forgetting_ready": True,
            "material_projection_readout_only": True,
            "countermodels_killed": True,
            "strict_primitive_derivation_not_claimed": True,
            "public_claim_false": True,
            "private_branch_adoption": True,
            "strict_primitive_derived": False,
            "source_path": str(FORMAL_461),
            "public_authority": False,
            "input_valid_for_claim": False,
            "notes": "Adopted only as a private PPC4161 local-branch invariant.",
        },
        {
            "row_id": "ADOPT4446_1_total_T_control",
            "branch": "control_total_T_only",
            "invariant": "total Hilbert stress without component/no-prefactor rule",
            "private_scope_declared": True,
            "standard_lmatter_slot_present": True,
            "hilbert_variation_before_readout": True,
            "component_import_graph_ready": False,
            "no_source_prefactor_theorem_ready": False,
            "source_label_forgetting_ready": False,
            "material_projection_readout_only": False,
            "countermodels_killed": False,
            "strict_primitive_derivation_not_claimed": True,
            "public_claim_false": True,
            "private_branch_adoption": False,
            "strict_primitive_derived": False,
            "source_path": str(FORMAL_459),
            "public_authority": False,
            "input_valid_for_claim": False,
            "notes": "Control row: total T_H alone still does not close source universality.",
        },
        {
            "row_id": "ADOPT4446_2_public_claim_control",
            "branch": "public_claim_control",
            "invariant": "same invariant but demanding public/strict primitive status",
            "private_scope_declared": True,
            "standard_lmatter_slot_present": True,
            "hilbert_variation_before_readout": True,
            "component_import_graph_ready": True,
            "no_source_prefactor_theorem_ready": True,
            "source_label_forgetting_ready": True,
            "material_projection_readout_only": True,
            "countermodels_killed": True,
            "strict_primitive_derivation_not_claimed": False,
            "public_claim_false": False,
            "private_branch_adoption": True,
            "strict_primitive_derived": False,
            "source_path": str(OBJECT_LANGUAGE),
            "public_authority": False,
            "input_valid_for_claim": False,
            "notes": "Control row: public/strict primitive claim remains blocked.",
        },
    ]


def material_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "MAT4446_0_material_projection_live",
            "arena": "WEP_clock_orbital_material_inventory",
            "quantity": "material_projection_Req",
            "material_inventory_named": True,
            "source_candidates_recorded": True,
            "component_convention_defined": False,
            "projection_coeff_numeric": False,
            "residual_value_numeric": False,
            "arena_bound_numeric": False,
            "readout_no_reentry": True,
            "projection_coeff": "MISSING_MATERIAL_PROJECTION_COEFF",
            "residual_value": "MISSING_MATERIAL_RESIDUAL_VALUE",
            "arena_bound": "MISSING_ARENA_BOUND",
            "source_path": str(STANDARD_GRAPH_ATTEMPT),
            "public_authority": False,
            "input_valid_for_claim": False,
            "notes": "Source candidates exist, but material projection rows are not yet numeric/source-backed.",
        },
        {
            "row_id": "MAT4446_1_Req_compact_live",
            "arena": "Newton_PPN_orbital_same_current",
            "quantity": "R_eq_compact_test",
            "material_inventory_named": True,
            "source_candidates_recorded": True,
            "component_convention_defined": False,
            "projection_coeff_numeric": False,
            "residual_value_numeric": False,
            "arena_bound_numeric": False,
            "readout_no_reentry": True,
            "projection_coeff": "MISSING_P_REQ_COMPACT",
            "residual_value": "MISSING_REQ_COMPACT_TEST_VALUE",
            "arena_bound": "MISSING_ARENA_BOUND",
            "source_path": str(POST_4378),
            "public_authority": False,
            "input_valid_for_claim": False,
            "notes": "Same-current R_eq fallback remains numeric/source-backed work.",
        },
        {
            "row_id": "MAT4446_2_smoke_pass",
            "arena": "schema_smoke",
            "quantity": "material_projection_Req",
            "material_inventory_named": True,
            "source_candidates_recorded": True,
            "component_convention_defined": True,
            "projection_coeff_numeric": True,
            "residual_value_numeric": True,
            "arena_bound_numeric": True,
            "readout_no_reentry": True,
            "projection_coeff": "1",
            "residual_value": "2e-7",
            "arena_bound": "1e-5",
            "source_path": str(STANDARD_GRAPH_ATTEMPT),
            "public_authority": False,
            "input_valid_for_claim": False,
            "notes": "Schema pass control, nonclaim.",
        },
        {
            "row_id": "MAT4446_3_fail_control",
            "arena": "schema_smoke",
            "quantity": "material_projection_Req",
            "material_inventory_named": True,
            "source_candidates_recorded": True,
            "component_convention_defined": True,
            "projection_coeff_numeric": True,
            "residual_value_numeric": True,
            "arena_bound_numeric": True,
            "readout_no_reentry": True,
            "projection_coeff": "1",
            "residual_value": "0.003",
            "arena_bound": "1e-5",
            "source_path": str(STANDARD_GRAPH_ATTEMPT),
            "public_authority": False,
            "input_valid_for_claim": False,
            "notes": "Fail control must exceed bound.",
        },
    ]


def residual_vector_rows() -> List[Dict[str, object]]:
    return [
        {
            "residual_id": "RU4446_0_Delta_w_A",
            "quantity": "relative_component_source_weight",
            "branch_value": "0",
            "status": "ZERO_INSIDE_PRIVATE_GR_PARITY_IMPORT_BRANCH",
            "proof_basis": "adopted empty-Hom/no-source-prefactor/source-label-forgetting invariant",
            "still_public_claim": False,
            "fallback_if_rejected": "material_projection_Req and P_WEP residual rows",
            "valid_for_claim": False,
        },
        {
            "residual_id": "RU4446_1_material_readout_reentry",
            "quantity": "material_label_to_active_source_reentry",
            "branch_value": "0",
            "status": "ZERO_INSIDE_PRIVATE_GR_PARITY_IMPORT_BRANCH",
            "proof_basis": "material projections are readout-only inventory",
            "still_public_claim": False,
            "fallback_if_rejected": "source-backed material projection tensor",
            "valid_for_claim": False,
        },
        {
            "residual_id": "RU4446_2_strict_primitive_origin",
            "quantity": "motion_time_space_primitive_derivation_of_no_source_prefac",
            "branch_value": "OPEN",
            "status": "STRICT_PRIMITIVE_DERIVATION_NOT_CLAIMED",
            "proof_basis": "1338 says primitive constructor route remains not derived",
            "still_public_claim": False,
            "fallback_if_rejected": "keep GR-parity import as explicit closure or fill empirical residual values",
            "valid_for_claim": False,
        },
        {
            "residual_id": "RU4446_3_R_eq_material_values",
            "quantity": "same_current_or_material_projection_numeric_residuals",
            "branch_value": "MISSING_NUMERIC_VALUES",
            "status": "EMPIRICAL_SCORING_VALUES_OPEN",
            "proof_basis": "material/R_eq live rows remain value-missing",
            "still_public_claim": False,
            "fallback_if_rejected": "source-backed material/R_eq acquisition",
            "valid_for_claim": False,
        },
    ]


def countermodel_status_rows() -> List[Dict[str, object]]:
    return [
        {
            "countermodel_id": "CM4446_0_weighted_components",
            "source_countermodel": "CM4445_0_weighted_components",
            "status_under_4446": "KILLED_INSIDE_PRIVATE_BRANCH",
            "killing_clause": "no SpeciesLabel/MaterialLabel -> Coeff_active_source morphism; imported S_matter is one scalar density functor",
            "public_claim": False,
            "valid_for_claim": False,
        },
        {
            "countermodel_id": "CM4446_1_material_reentry",
            "source_countermodel": "CM4445_1_material_reentry",
            "status_under_4446": "KILLED_INSIDE_PRIVATE_BRANCH",
            "killing_clause": "material projection is readout inventory only and cannot re-enter active source coefficient",
            "public_claim": False,
            "valid_for_claim": False,
        },
        {
            "countermodel_id": "CM4446_2_strict_derivation_challenge",
            "source_countermodel": "OLT1338_2_MTS_primitive_constructor",
            "status_under_4446": "SURVIVES_AS_PUBLIC_CLAIM_BLOCKER",
            "killing_clause": "not killed; strict primitive derivation remains open",
            "public_claim": False,
            "valid_for_claim": False,
        },
    ]


def reduction_rows() -> List[Dict[str, object]]:
    return [
        {
            "reduction_id": "RED4446_0_source_weight_to_zero",
            "from_problem": "component source-weight loophole",
            "to_problem": "zero inside adopted private GR-parity import branch",
            "status": "PRIVATE_BRANCH_RESIDUAL_ZERO",
            "reason": "The adopted invariant makes w_A ill-typed except as one common calibration.",
            "valid_for_claim": False,
        },
        {
            "reduction_id": "RED4446_1_public_claim_to_strict_origin",
            "from_problem": "public local-GR source-universality claim",
            "to_problem": "strict primitive derivation or empirical material/R_eq values",
            "status": "PUBLIC_CLAIM_STILL_BLOCKED",
            "reason": "Private adoption is not a primitive derivation from motion/time/space and not a public empirical pass.",
            "valid_for_claim": False,
        },
        {
            "reduction_id": "RED4446_2_next_ppn_vector",
            "from_problem": "adopted source universality",
            "to_problem": "propagate into local PPN residual vector",
            "status": "NEXT_DERIVATION_TARGET_SELECTED",
            "reason": "If Delta_w_A and material reentry are zero inside PPC4161, the next question is which PPN/Newton residual entries remain alive.",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(adoption_outputs: Sequence[Mapping[str, str]], material_outputs: Sequence[Mapping[str, str]]) -> List[Dict[str, object]]:
    adoption = {row["row_id"]: row for row in adoption_outputs}
    material = {row["row_id"]: row for row in material_outputs}
    no_claim = not any(row.get("valid_for_claim") == "True" for row in adoption_outputs) and not any(row.get("valid_for_claim") == "True" for row in material_outputs)
    return [
        {"gate_id": "CG4446_0_sources_exist", "claim": "all cited source paths exist", "passed": all(row["path_exists"] == "True" for row in rows_from(SOURCE_REGISTER)), "valid_for_claim": False, "detail": "Source register path-backed."},
        {"gate_id": "CG4446_1_needles_found", "claim": "all cited source needles found", "passed": all(row["needle_found"] == "True" for row in rows_from(SOURCE_REGISTER)), "valid_for_claim": False, "detail": "No unsourced adoption."},
        {"gate_id": "CG4446_2_private_adoption", "claim": "GR-parity import invariant adopted inside PPC4161", "passed": adoption["ADOPT4446_0_PPC4161_GR_parity_import"].get("current_status") == "GR_PARITY_SM_IMPORT_PRIVATE_BRANCH_ADOPTED_NONCLAIM", "valid_for_claim": False, "detail": "Private branch adoption succeeds without public claim."},
        {"gate_id": "CG4446_3_total_T_control_rejected", "claim": "total T_H control remains insufficient", "passed": adoption["ADOPT4446_1_total_T_control"].get("current_status") == "GR_PARITY_SM_IMPORT_ADOPTION_PARTIAL_CLAUSES_OPEN", "valid_for_claim": False, "detail": "Total Hilbert stress alone still fails."},
        {"gate_id": "CG4446_4_public_claim_control_blocked", "claim": "public/strict primitive control remains blocked", "passed": adoption["ADOPT4446_2_public_claim_control"].get("current_status") == "GR_PARITY_SM_IMPORT_ADOPTION_PARTIAL_CLAUSES_OPEN", "valid_for_claim": False, "detail": "Strict primitive derivation is not claimed."},
        {"gate_id": "CG4446_5_material_live_values_missing", "claim": "material live row remains source-candidate only", "passed": material["MAT4446_0_material_projection_live"].get("current_status") == "MATERIAL_REQ_SOURCE_CANDIDATES_READY_VALUES_MISSING", "valid_for_claim": False, "detail": "Source candidates exist, values missing."},
        {"gate_id": "CG4446_6_material_controls", "claim": "material gate has pass and fail controls", "passed": material["MAT4446_2_smoke_pass"].get("current_status") == "MATERIAL_REQ_VALUE_SCHEMA_PASS_NONCLAIM" and material["MAT4446_3_fail_control"].get("current_status") == "MATERIAL_REQ_VALUE_FAILS_BOUND", "valid_for_claim": False, "detail": "Schema pass and fail control are both active."},
        {"gate_id": "CG4446_7_residual_vector_written", "claim": "source-universality residual vector written", "passed": all(key in text(RESIDUAL_VECTOR) for key in ("RU4446_0_Delta_w_A", "RU4446_3_R_eq_material_values")), "valid_for_claim": False, "detail": "Branch zeros and open empirical values are separated."},
        {"gate_id": "CG4446_8_countermodels_statused", "claim": "countermodels are killed or retained explicitly", "passed": all(key in text(COUNTERMODEL_ROWS) for key in ("KILLED_INSIDE_PRIVATE_BRANCH", "SURVIVES_AS_PUBLIC_CLAIM_BLOCKER")), "valid_for_claim": False, "detail": "No smuggled closure."},
        {"gate_id": "CG4446_9_no_public_claim", "claim": "4446 emits no public local-GR/PPN claim", "passed": no_claim, "valid_for_claim": False, "detail": "All outputs remain private nonclaim."},
        {"gate_id": "CG4446_10_next_target_written", "claim": "next target selected", "passed": NEXT_CSV.exists() and NEXT_TARGET in text(NEXT_CSV), "valid_for_claim": False, "detail": NEXT_TARGET},
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4446_0",
            "decision": DECISION,
            "summary": "4446 formally adopts the GR-parity standard-matter import/no-source-prefactor invariant inside the private PPC4161 local branch. This is a real leap: the hidden component source-weight residual Delta_w_A and material readout re-entry countermodel are zero inside the private branch. It is not a public local-GR claim, not a strict derivation of the Standard Model or of the no-source-prefactor theorem from motion/time/space primitives, and it does not fill material/R_eq empirical values. The next target is to propagate this adopted source-universality invariant into the local PPN/Newton residual vector, or fill material values if adoption is rejected.",
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
            "root_result": "GR-parity standard-matter import/no-source-prefactor invariant privately adopted inside PPC4161",
            "closed_inside_private_branch": "Delta_w_A; material readout reentry",
            "still_missing": "strict primitive derivation; source-backed material/R_eq values; propagation through full local PPN residual vector",
            "next_target": NEXT_TARGET,
            "public_claim": False,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4446_0",
            "target": NEXT_TARGET,
            "objective": "Propagate the privately adopted GR-parity source-universality invariant into the local PPN/Newton residual vector, or fill source-backed material/R_eq values if the adoption branch is rejected.",
            "derive_first": "map Delta_w_A=0 and material-reentry=0 into gamma, beta, alpha_i, xi, zeta_i, Gdot/G, WEP, clock and orbital residual rows while preserving remaining non-source residuals",
            "fallback": "fill material projection or R_eq compact-test value with units, projection coefficient, arena bound, source path and no-cancellation guard",
            "risk": "mistaking private branch adoption for public proof; erasing non-source residuals that are not touched by the matter import invariant",
            "valid_for_claim": False,
        }
    ]


def build_doc(sources: Sequence[Mapping[str, object]], adoption_outputs: Sequence[Mapping[str, object]], material_outputs: Sequence[Mapping[str, object]], gates: Sequence[Mapping[str, object]]) -> str:
    return f"""# 462 PPC4161 adopt GR-parity SM import or source-backed material Req value

Marker: `{MARKER}`

Decision: `{DECISION}`

Claim register: `{CLAIM_ID}`

## Result

4446 makes the adoption move:

```text
Inside the private PPC4161 local branch, adopt the GR-parity standard-matter import invariant.
S_matter is one imported scalar density functor.
Internal matter constants are not source labels.
Hom(SpeciesLabel/MaterialLabel, Coeff_active_source)=empty.
Hilbert variation happens before readout.
Material projections are readout inventory only.
```

Consequently, the hidden component source-weight countermodel `S_matter=sum_A w_A S_A` is killed **inside the private branch**. The material readout re-entry countermodel is also killed inside the private branch. This is not public/local-GR completion: strict primitive derivation and source-backed material/`R_eq` values remain open.

## Source Register

{table(sources)}

## Derivation Rows

{table(rows_from(DERIVATION_ROWS))}

## Adoption Gate

{table(adoption_outputs)}

## Material / R_eq Value Gate

{table(material_outputs)}

## Source-Universality Residual Vector

{table(rows_from(RESIDUAL_VECTOR))}

## Countermodel Status

{table(rows_from(COUNTERMODEL_ROWS))}

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
    return f"""# 4446 Y5 R2FR adopt GR-parity SM import or source-backed material Req value

Private checkpoint generated at `{STAMP}`.

Summary:
- Adopted the GR-parity standard-matter import/no-source-prefactor invariant inside the private PPC4161 local branch.
- This closes `Delta_w_A` and material readout re-entry as private-branch source-coupling residuals.
- It is not a public local-GR claim: strict primitive derivation and source-backed material/`R_eq` values remain open.

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
        "claim": "4446 privately adopts the GR-parity standard-matter import/no-source-prefactor invariant inside PPC4161. Inside that private branch, hidden component source weights Delta_w_A and material readout re-entry are zero. This is not a public local-GR claim: strict primitive derivation and source-backed material/R_eq values remain open.",
        "current_evidence": "4446 source register, derivation rows, adoption gate, material/R_eq value gate, source-universality residual vector, countermodel status, reduction rows, claim gates, decision, status, next target and validation CSV.",
        "status": "GR_parity_standard_matter_import_private_branch_adopted_strict_primitive_and_material_values_open_nonclaim",
        "next_test": "Propagate private source-universality into the local PPN/Newton residual vector, or fill material/R_eq values.",
        "key_risk": "Mistaking private adoption for public proof; deleting non-source residuals untouched by the matter import invariant.",
        "sector": "local_gr_source_coupling",
        "evidence": "4446 source register, derivation rows, adoption gate, material/R_eq value gate, source-universality residual vector, countermodel status, reduction rows, claim gates, decision, status, next target and validation CSV.",
        "next_action": "Propagate private source-universality into the local PPN/Newton residual vector, or fill material/R_eq values.",
        "risk": "Mistaking private adoption for public proof; deleting non-source residuals untouched by the matter import invariant.",
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
    spine_section = f"""## Local GR Source Coupling Update - Adopted GR-Parity SM Import

Marker: `{MARKER}`  
Source checkpoint: `4446-Y5-R2FR-adopt-GR-parity-SM-import-or-source-backed-material-Req-value.md`  
Claim register row: `{CLAIM_ID}`

Inside the private PPC4161 local branch, the GR-parity standard-matter import/no-source-prefactor invariant is now adopted. This makes `Delta_w_A=0` and material readout re-entry zero inside the private branch, because source/species/material labels have no morphism into active source coefficients and `S_matter` is one imported scalar density functor varied before readout. Public claim guards remain: strict primitive derivation and source-backed material/`R_eq` values are still open.
"""
    packet_section = f"""## PPC4161 Packet Addendum - Adopted GR-Parity SM Import

Marker: `{PACKET_MARKER}`  
Source checkpoint: `4446-Y5-R2FR-adopt-GR-parity-SM-import-or-source-backed-material-Req-value.md`

The private PPC4161 packet now adopts the GR-parity imported standard matter invariant: one `S_matter[g,psi;c_i]`, fixed internal matter constants, Hilbert variation before readout, no source/species/material label to active source coefficient, and readout-only material projections. This closes the private source-weight loophole but remains nonpublic and non-global.
"""
    append_marker_section(SPINE_PATH, MARKER, spine_section)
    append_marker_section(PACKET_PATH, PACKET_MARKER, packet_section)


def validation_rows(paths: Mapping[str, Path]) -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    adoption = {row["row_id"]: row for row in rows_from(ADOPTION_OUTPUT)}
    material = {row["row_id"]: row for row in rows_from(MATERIAL_OUTPUT)}
    gates = rows_from(CLAIM_GATES)
    no_claims = not any(row.get("valid_for_claim") == "True" for row in adoption.values()) and not any(row.get("valid_for_claim") == "True" for row in material.values())
    checks = [
        ("VAL4446_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source path exists"),
        ("VAL4446_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited source needle is present"),
        ("VAL4446_2_private_adoption", adoption["ADOPT4446_0_PPC4161_GR_parity_import"].get("current_status") == "GR_PARITY_SM_IMPORT_PRIVATE_BRANCH_ADOPTED_NONCLAIM", "GR-parity import adopted privately"),
        ("VAL4446_3_total_T_control", adoption["ADOPT4446_1_total_T_control"].get("current_status") == "GR_PARITY_SM_IMPORT_ADOPTION_PARTIAL_CLAUSES_OPEN", "total T_H control rejected"),
        ("VAL4446_4_public_control", adoption["ADOPT4446_2_public_claim_control"].get("current_status") == "GR_PARITY_SM_IMPORT_ADOPTION_PARTIAL_CLAUSES_OPEN", "public/strict primitive control blocked"),
        ("VAL4446_5_material_live_missing", material["MAT4446_0_material_projection_live"].get("current_status") == "MATERIAL_REQ_SOURCE_CANDIDATES_READY_VALUES_MISSING", "material live row values missing"),
        ("VAL4446_6_req_live_missing", material["MAT4446_1_Req_compact_live"].get("current_status") in {"MATERIAL_REQ_SOURCE_CANDIDATES_READY_VALUES_MISSING", "MATERIAL_REQ_SOURCE_PRESENT_CLAUSES_OPEN"}, "R_eq live row values missing"),
        ("VAL4446_7_material_smoke_pass", material["MAT4446_2_smoke_pass"].get("current_status") == "MATERIAL_REQ_VALUE_SCHEMA_PASS_NONCLAIM", "material smoke pass works"),
        ("VAL4446_8_material_fail_control", material["MAT4446_3_fail_control"].get("current_status") == "MATERIAL_REQ_VALUE_FAILS_BOUND", "material fail control does not pass"),
        ("VAL4446_9_residual_vector", all(key in text(RESIDUAL_VECTOR) for key in ("RU4446_0_Delta_w_A", "RU4446_3_R_eq_material_values")), "residual vector written"),
        ("VAL4446_10_countermodels", all(key in text(COUNTERMODEL_ROWS) for key in ("KILLED_INSIDE_PRIVATE_BRANCH", "SURVIVES_AS_PUBLIC_CLAIM_BLOCKER")), "countermodel statuses written"),
        ("VAL4446_11_no_claim_outputs", no_claims, "no output row is public claim-ready"),
        ("VAL4446_12_claim_gate_no_claim", any(row["gate_id"] == "CG4446_9_no_public_claim" and row["passed"] == "True" for row in gates), "claim gate explicitly blocks public claim"),
        ("VAL4446_13_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-288"),
        ("VAL4446_14_formal_doc", paths["formal"].exists() and MARKER in text(paths["formal"]), "formal doc exists with marker"),
        ("VAL4446_15_post_doc", paths["post"].exists() and "Private checkpoint" in text(paths["post"]), "post checkpoint doc exists"),
        ("VAL4446_16_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4446_17_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4446_18_next_gate", any(row["gate_id"] == "CG4446_10_next_target_written" and row["passed"] == "True" for row in gates), "next target claim gate is true"),
        ("VAL4446_19_next_target", paths["next"].exists() and NEXT_TARGET in text(paths["next"]), "next target file exists"),
        ("VAL4446_20_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": bool(passed), "detail": detail} for check_id, passed, detail in checks]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(DERIVATION_ROWS, derivation_rows())
    write_csv(ADOPTION_INPUT, adoption_input_rows())
    write_csv(ADOPTION_OUTPUT, evaluate_adoption_rows(ADOPTION_INPUT))
    write_csv(MATERIAL_INPUT, material_input_rows())
    write_csv(MATERIAL_OUTPUT, evaluate_material_rows(MATERIAL_INPUT))
    write_csv(RESIDUAL_VECTOR, residual_vector_rows())
    write_csv(COUNTERMODEL_ROWS, countermodel_status_rows())
    write_csv(REDUCTION_ROWS, reduction_rows())
    write_csv(DECISION_CSV, decision_rows())
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    adoption_outputs = rows_from(ADOPTION_OUTPUT)
    material_outputs = rows_from(MATERIAL_OUTPUT)
    gates = claim_gate_rows(adoption_outputs, material_outputs)
    write_csv(CLAIM_GATES, gates)
    write_text(FORMAL_PATH, build_doc(rows_from(SOURCE_REGISTER), adoption_outputs, material_outputs, gates))
    write_text(DOC_PATH, post_doc())
    update_claims_register()
    write_spine_and_packet()
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    write_csv(VALIDATION_PATH, validation_rows({"formal": FORMAL_PATH, "post": DOC_PATH, "next": NEXT_CSV}))


if __name__ == "__main__":
    main()

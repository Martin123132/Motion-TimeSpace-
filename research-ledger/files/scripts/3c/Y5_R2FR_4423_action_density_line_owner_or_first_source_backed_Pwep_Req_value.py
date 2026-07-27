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

from action_density_owner_gate import evaluate_density_owner_rows, write_csv  # noqa: E402
from hbar_measure_value_gate import evaluate_value_rows  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
RAB_QUEUE = POST / "source-intake" / "rab-sector" / "acquisition-queue"
CORE = ROOT / "core-mts-framework"

CHECKPOINT = "4423"
CLAIM_ID = "L-264"
MARKER = "PPC4161_ACTION_DENSITY_LINE_OWNER_OR_FIRST_SOURCE_BACKED_PWEP_REQ_VALUE_4423"
PACKET_MARKER = "PPC4161_PACKET_ACTION_DENSITY_LINE_OWNER_OR_FIRST_SOURCE_BACKED_PWEP_REQ_VALUE_4423"
DECISION = "ACTION_DENSITY_OWNER_TYPED_HOM_THEOREM_CONDITIONAL_PWEP_PROVENANCE_STRENGTHENED_NONCLAIM"
NEXT_TARGET = "4424-Y5-R2FR-parent-constructor-exhaustion-or-first-numeric-Pwep-coefficient.md"

FORMAL_PATH = FORMAL / "439-PPC4161-action-density-line-owner-or-first-source-backed-Pwep-Req-value.md"
DOC_PATH = POST / "4423-Y5-R2FR-action-density-line-owner-or-first-source-backed-Pwep-Req-value.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4423_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4423_SOURCE_REGISTER.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4423_DERIVATION_ROWS.csv"
DENSITY_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4423_ACTION_DENSITY_OWNER_INPUT.csv"
DENSITY_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4423_ACTION_DENSITY_OWNER_OUTPUT.csv"
VALUE_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4423_FIRST_SOURCE_BACKED_VALUE_INPUT.csv"
VALUE_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4423_FIRST_SOURCE_BACKED_VALUE_OUTPUT.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4423_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4423_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4423_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4423_NEXT_TARGET.csv"

DENSITY_GATE_PATH = SCRIPT_DIR / "action_density_owner_gate.py"
VALUE_GATE_PATH = SCRIPT_DIR / "hbar_measure_value_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4423_action_density_line_owner_or_first_source_backed_Pwep_Req_value.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4422 = SOURCE_DIR / "P8_Y5_R2FR_4422_NEXT_TARGET.csv"
FORMAL_438 = FORMAL / "438-PPC4161-universal-hbar-measure-owner-or-first-source-backed-Pwep-Req-row.md"
CORE_ACTION = CORE / "action-principle" / "the-motion-timespace-action-principle.md"
CORE_FUNDAMENTAL = CORE / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md"
POST_1066 = POST / "1066-Y5-R10-parent-action-syntax-source-scalar-exclusion-or-WEP-Delta-w-prior-width.md"
POST_1389 = POST / "1389-Y5-R10-RAB-Delta-w-material-source-map-or-action-measure-owner-proof.md"
RAB_COMMON_OWNER = RAB_QUEUE / "JR1687_COMMON_ACTION_MEASURE_CURRENT_OWNER_PROOF_ATTEMPT.csv"
RAB_ACTION = RAB_QUEUE / "JR1694_ACTION_MEASURE_OWNER_PROOF_GATE.csv"
RAB_AXIOM = RAB_QUEUE / "JR1698_OWNER_AXIOM_DERIVATION_TEST.csv"
CSV_1066 = SOURCE_DIR / "P8_Y5_R10_1066_OBJECT_LANGUAGE_TYPING_AUDIT.csv"
CSV_1078 = SOURCE_DIR / "P8_Y5_R10_1078_OBJECT_LANGUAGE_PROOF_ATTEMPT.csv"
CSV_1107 = SOURCE_DIR / "P8_Y5_R10_1107_OBJECT_LANGUAGE_EXHAUSTION_ATTEMPT.csv"
CSV_1236 = SOURCE_DIR / "P8_Y5_R10_1236_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv"
CSV_1338 = SOURCE_DIR / "P8_Y5_R10_1338_OBJECT_LANGUAGE_THEOREM_ATTEMPT.csv"
CSV_2434 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2434_TYPED_OBJECT_LANGUAGE_CERTIFICATE.csv"
CSV_2982 = SOURCE_DIR / "P8_Y5_R2FR_2982_PARENT_HBAR_MEASURE_OWNER_SOURCE_SEARCH.csv"
SSC_SOURCE = SOURCE_DIR / "P8_species_source_charge_residual_or_zero.csv"
RADIAL_GAP = SOURCE_DIR / "P8_RADIAL_BOUND_INPUT_AUDIT_GAP_LEDGER.csv"
WEP_CLAUSE = POST / "source-intake" / "microscope" / "branch_locked_wep" / "coefficients" / "C_parent_WEP_minimal_parent_clause.csv"
WEP_PDF = POST / "source-intake" / "wep-sources" / "1899" / "MICROSCOPE_final_results_arxiv_2209_15487.pdf"


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
        {"source_id": "SRC4423_00_4422_next", "path": NEXT_4422, "needle": "4423-Y5-R2FR-action-density-line-owner-or-first-source-backed-Pwep-Req-value.md", "role": "4422 handoff."},
        {"source_id": "SRC4423_01_438_formal", "path": FORMAL_438, "needle": "UHM4422_1_exact_owner_contract", "role": "exact hbar/measure owner contract from 4422."},
        {"source_id": "SRC4423_02_core_action", "path": CORE_ACTION, "needle": "L_matter the standard matter Lagrangian", "role": "MTS action schema includes standard matter coupling."},
        {"source_id": "SRC4423_03_core_fundamental", "path": CORE_FUNDAMENTAL, "needle": "L_matter", "role": "fundamental action line carrying matter sector."},
        {"source_id": "SRC4423_04_1066_typing", "path": CSV_1066, "needle": "OLT1066_4_inert_source_scalar", "role": "object-language typing rejects inert source scalar conditionally."},
        {"source_id": "SRC4423_05_1078_object_language", "path": CSV_1078, "needle": "OL1078_4_verdict", "role": "object-language proof attempt verdict."},
        {"source_id": "SRC4423_06_1107_exhaustion", "path": CSV_1107, "needle": "EXH1107_6_verdict", "role": "parent constructor/domain exhaustion attempt."},
        {"source_id": "SRC4423_07_1236_certificate", "path": CSV_1236, "needle": "CERT1236_6_current_verdict", "role": "typed parent object-language certificate."},
        {"source_id": "SRC4423_08_1338_no_slot", "path": CSV_1338, "needle": "OLT1338_6_verdict", "role": "NoSourceOnlySpeciesSlot theorem attempt."},
        {"source_id": "SRC4423_09_2434_typed_q", "path": CSV_2434, "needle": "TOL2434_7_verdict", "role": "R2/f(R) typed object-language certificate."},
        {"source_id": "SRC4423_10_2982_hbar_search", "path": CSV_2982, "needle": "HMO2982_1_action_density_line", "role": "action-density line owner source search."},
        {"source_id": "SRC4423_11_common_owner", "path": RAB_COMMON_OWNER, "needle": "COM1687_5_object_language", "role": "common owner and object-language gap."},
        {"source_id": "SRC4423_12_action_measure", "path": RAB_ACTION, "needle": "OWG1694_1_no_source_only_slot", "role": "action-measure owner gate."},
        {"source_id": "SRC4423_13_axiom", "path": RAB_AXIOM, "needle": "DER1698_2_single_density_owner", "role": "owner axiom derivation test."},
        {"source_id": "SRC4423_14_species_charge", "path": SSC_SOURCE, "needle": "SSC2675_1_conditional_zero", "role": "source-backed WEP residual/provenance ledger."},
        {"source_id": "SRC4423_15_wep_clause", "path": WEP_CLAUSE, "needle": "MPC1439_1_formal_zero", "role": "compact parent WEP zero-shape clause."},
        {"source_id": "SRC4423_16_wep_pdf", "path": WEP_PDF, "needle": "", "role": "local MICROSCOPE official comparator PDF path."},
        {"source_id": "SRC4423_17_density_gate", "path": DENSITY_GATE_PATH, "needle": "def evaluate_density_owner_row", "role": "4423 action-density owner gate."},
        {"source_id": "SRC4423_18_value_gate", "path": VALUE_GATE_PATH, "needle": "def evaluate_value_row", "role": "finite source-backed value gate."},
        {"source_id": "SRC4423_19_generator", "path": GENERATOR_PATH, "needle": "ACTION_DENSITY_OWNER_TYPED_HOM_THEOREM", "role": "4423 generator."},
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
            "derivation_id": "ADL4423_0_MTS_action_schema_seed",
            "claim": "The current MTS action schema already points to a single ordinary matter action density.",
            "derivation": "The core action writes one standard L_matter under one spacetime measure. That is the right shape for local-GR coupling, but it is a schema seed unless the parent proves no additional source-only species coefficient can be attached.",
            "consequence": "The route is not random: MTS already has the local action slot, but the no-extra-slot theorem must be derived rather than assumed.",
            "status": "MTS_ACTION_SCHEMA_SEED_READY_OBJECT_LANGUAGE_OPEN",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "ADL4423_1_typed_Hom_no_slot_theorem",
            "claim": "Typed object language would forbid species source weights if Hom(SpeciesLabel,Coeff_active_source) is empty.",
            "derivation": "Let the parent action admit only observed geometry/coframe, matter fields, gauge/current data, representation constants and universal constants as ordinary matter arguments. If no morphism exists from a species/source bookkeeping label to an active source coefficient, then w_A S_A is ill-typed except for one common calibration.",
            "consequence": "This is stronger than taste: it turns no-source-only-prefactor into an object-language theorem when parent constructors are exhausted.",
            "status": "EXACT_IF_PARENT_CONSTRUCTOR_EXHAUSTION_SIGNED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "ADL4423_2_positive_list_not_exhaustion",
            "claim": "A positive list of allowed arguments is not yet a proof of exhaustion.",
            "derivation": "Hidden markers, disconnected species components, radiative/readout maps and source-worldtube selectors can reintroduce the same coefficient under a different name unless the parent proves constructor exhaustion and no-reentry.",
            "consequence": "The proof obligation moves from vague coupling to a concrete parent-constructor exhaustion theorem.",
            "status": "COUNTERMODEL_SURVIVES_WITHOUT_EXHAUSTION",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "ADL4423_3_action_density_owner_theorem",
            "claim": "The exact action-density owner theorem is now narrowed.",
            "derivation": "Typed domains + empty Hom to active source coefficients + no source-only prefactor + one action-density line + common hbar/measure + species-blind Jacobian + connected matter graph + readout/EFT no-reentry imply Delta_w_A=0 for ordinary matter source coupling.",
            "consequence": "This is a real derivation target for local GR/Newton coupling, not merely another checklist.",
            "status": "EXACT_CONDITIONAL_THEOREM_READY_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "ADL4423_4_PWEP_provenance_improved",
            "claim": "The finite P_WEP branch now has real local comparator/source provenance attached.",
            "derivation": "The MICROSCOPE comparator PDF and compact parent WEP clause exist locally. The row can now distinguish official bound provenance from missing MTS-side parent coefficients.",
            "consequence": "The finite fallback is less vague, but still not a prediction until Delta_w_TiPt*tau_WEP or C_parent_WEP is derived or filled.",
            "status": "PWEP_OFFICIAL_BOUND_PROVENANCE_READY_PREDICTION_MISSING",
            "valid_for_claim": False,
        },
    ]


def density_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "ADLO4423_0_core_MTS_action_schema",
            "branch": "core_standard_Lmatter_schema",
            "parent_sorts_declared": True,
            "primitive_constructor_list": False,
            "ordinary_domain_exhausted": False,
            "hom_species_to_source_empty": False,
            "no_source_only_prefactor": False,
            "action_density_line_unique": True,
            "common_hbar_measure_owner": False,
            "species_blind_measure_jacobian": False,
            "connected_matter_graph": False,
            "representation_constants_exempt": True,
            "hidden_marker_no_reentry": False,
            "readout_eft_closure": False,
            "variation_before_readout": True,
            "source_path": str(CORE_ACTION),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Core action gives a useful single L_matter schema seed, not constructor exhaustion.",
        },
        {
            "row_id": "ADLO4423_1_typed_domain_certificate",
            "branch": "typed_parent_object_language_certificate",
            "parent_sorts_declared": True,
            "primitive_constructor_list": False,
            "ordinary_domain_exhausted": True,
            "hom_species_to_source_empty": True,
            "no_source_only_prefactor": True,
            "action_density_line_unique": False,
            "common_hbar_measure_owner": False,
            "species_blind_measure_jacobian": False,
            "connected_matter_graph": False,
            "representation_constants_exempt": True,
            "hidden_marker_no_reentry": False,
            "readout_eft_closure": False,
            "variation_before_readout": True,
            "source_path": str(CSV_1236),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Typed-domain certificate writes the right grammar but says it is not parent-derived.",
        },
        {
            "row_id": "ADLO4423_2_hom_no_slot_contract",
            "branch": "hom_species_to_active_source_empty_contract",
            "parent_sorts_declared": True,
            "primitive_constructor_list": True,
            "ordinary_domain_exhausted": True,
            "hom_species_to_source_empty": True,
            "no_source_only_prefactor": True,
            "action_density_line_unique": False,
            "common_hbar_measure_owner": False,
            "species_blind_measure_jacobian": False,
            "connected_matter_graph": False,
            "representation_constants_exempt": True,
            "hidden_marker_no_reentry": False,
            "readout_eft_closure": False,
            "variation_before_readout": True,
            "source_path": str(CSV_1338),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "No-source-slot theorem is exact if the constructor list is parent-signed; action-scale/measure remains open.",
        },
        {
            "row_id": "ADLO4423_3_action_owner_after_no_slot",
            "branch": "action_density_measure_owner_dependency",
            "parent_sorts_declared": True,
            "primitive_constructor_list": True,
            "ordinary_domain_exhausted": True,
            "hom_species_to_source_empty": True,
            "no_source_only_prefactor": True,
            "action_density_line_unique": True,
            "common_hbar_measure_owner": True,
            "species_blind_measure_jacobian": True,
            "connected_matter_graph": False,
            "representation_constants_exempt": True,
            "hidden_marker_no_reentry": False,
            "readout_eft_closure": False,
            "variation_before_readout": True,
            "source_path": str(CSV_2982),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "If no-slot plus hbar/measure are granted, connectivity and readout no-reentry still matter.",
        },
        {
            "row_id": "ADLO4423_4_future_action_density_owner_contract",
            "branch": "future_parent_action_density_owner_contract",
            "parent_sorts_declared": True,
            "primitive_constructor_list": True,
            "ordinary_domain_exhausted": True,
            "hom_species_to_source_empty": True,
            "no_source_only_prefactor": True,
            "action_density_line_unique": True,
            "common_hbar_measure_owner": True,
            "species_blind_measure_jacobian": True,
            "connected_matter_graph": True,
            "representation_constants_exempt": True,
            "hidden_marker_no_reentry": True,
            "readout_eft_closure": True,
            "variation_before_readout": True,
            "source_path": str(RAB_AXIOM),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Exact future theorem contract only; nonclaim because it is not parent-signed.",
        },
    ]


def value_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "value_id": "PV4423_0_PWEP_official_bound_attached",
            "quantity": "P_WEP_relative_source_weight",
            "arena": "MICROSCOPE_WEP_TiPt",
            "normal_form": "P_WEP=abs(Delta_w_TiPt*tau_WEP)",
            "predicted_value": "MISSING_PARENT_ZERO_OR_NUMERIC_EPSILON_A",
            "prediction_source": str(SSC_SOURCE),
            "projection_source": str(WEP_CLAUSE),
            "comparator_value": "2.8e-15",
            "comparator_source": str(WEP_PDF),
            "units": "dimensionless",
            "parent_coefficient_source": str(WEP_CLAUSE),
            "official_numeric_source": str(WEP_PDF),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Official local MICROSCOPE bound and parent-clause path are attached; MTS prediction value remains missing.",
        },
        {
            "value_id": "PV4423_1_Cparent_WEP_zero_shape",
            "quantity": "C_parent_WEP_TiPt",
            "arena": "source_label_forgetting_WEP",
            "normal_form": "C_parent_WEP_TiPt=0 if parent descent/no-label/readout clauses close",
            "predicted_value": "MISSING_PARENT_CLAUSE_SIGNATURE_FOR_ZERO",
            "prediction_source": str(WEP_CLAUSE),
            "projection_source": str(WEP_CLAUSE),
            "comparator_value": "2.8e-15",
            "comparator_source": str(WEP_PDF),
            "units": "dimensionless",
            "parent_coefficient_source": str(WEP_CLAUSE),
            "official_numeric_source": str(WEP_PDF),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Zero shape is written, but the parent clause itself warns it is not adopted.",
        },
        {
            "value_id": "PV4423_2_Req_radial_gap_ledger",
            "quantity": "R_eq_integral_or_Bzero_flux",
            "arena": "Newton_PPN_radial_source_profile",
            "normal_form": "epsilon_radial_Meff from R_eq/B_zero/worldtube integral",
            "predicted_value": "MISSING_SOURCE_BACKED_REQ_OR_BZERO_VALUE",
            "prediction_source": str(RADIAL_GAP),
            "projection_source": str(RADIAL_GAP),
            "comparator_value": "SCHEMA_PPN_OR_ORBIT_BOUND_REQUIRED",
            "comparator_source": str(RADIAL_GAP),
            "units": "dimensionless",
            "parent_coefficient_source": "MISSING_PARENT_REQ_BZERO_COEFFICIENT_SOURCE_PATH",
            "official_numeric_source": "MISSING_OFFICIAL_PPN_OR_ORBIT_BOUND_SOURCE_PATH",
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "R_eq/B_zero fallback remains a gap ledger, not a value.",
        },
    ]


def claim_gate_rows(density_out: Sequence[Mapping[str, str]], value_out: Sequence[Mapping[str, str]]) -> List[Dict[str, object]]:
    density = {row["row_id"]: row for row in density_out}
    values = {row["value_id"]: row for row in value_out}
    no_claims = not any(row.get("valid_for_claim") == "True" for row in density_out) and not any(
        row.get("valid_for_claim") == "True" for row in value_out
    )
    return [
        {"gate_id": "CG4423_0_core_action_schema", "claim": "core MTS action supplies an action-density seed", "passed": density["ADLO4423_0_core_MTS_action_schema"].get("current_status") == "ACTION_DENSITY_OWNER_PARTIAL_PARENT_SYNTAX", "valid_for_claim": False, "detail": "one L_matter schema exists, but constructor exhaustion is not derived."},
        {"gate_id": "CG4423_1_hom_no_slot_contract", "claim": "Hom no-source-only slot contract is executable", "passed": density["ADLO4423_2_hom_no_slot_contract"].get("current_status") == "HOM_NO_SLOT_READY_ACTION_MEASURE_OPEN", "valid_for_claim": False, "detail": "typed no-slot route is sharpened; action measure remains open."},
        {"gate_id": "CG4423_2_future_contract", "claim": "full action-density owner theorem is executable", "passed": density["ADLO4423_4_future_action_density_owner_contract"].get("current_status") == "ACTION_DENSITY_OWNER_CONTRACT_READY_NONCLAIM", "valid_for_claim": False, "detail": "contract closes only with input_valid=false."},
        {"gate_id": "CG4423_3_action_density_claim", "claim": "current MTS parent-signs action-density owner", "passed": False, "valid_for_claim": False, "detail": "primitive constructor exhaustion, common measure, connectivity and no-reentry remain unsigned."},
        {"gate_id": "CG4423_4_PWEP_official_bound", "claim": "P_WEP row has official bound provenance", "passed": values["PV4423_0_PWEP_official_bound_attached"].get("official_numeric_source_exists") == "True", "valid_for_claim": False, "detail": "official local MICROSCOPE PDF path is now attached."},
        {"gate_id": "CG4423_5_PWEP_prediction", "claim": "P_WEP row has MTS prediction value", "passed": values["PV4423_0_PWEP_official_bound_attached"].get("current_status") == "COMPARATOR_ANCHOR_READY_PREDICTION_VALUE_MISSING_NONCLAIM", "valid_for_claim": False, "detail": "prediction remains missing, so no score claim."},
        {"gate_id": "CG4423_6_no_claim_outputs", "claim": "4423 generated no claim-ready row", "passed": no_claims, "valid_for_claim": False, "detail": "checkpoint advances theorem shape and provenance only."},
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4423_0",
            "decision": DECISION,
            "summary": "4423 does not magically close the coupling, but it moves the proof target forward. The parent action already has the right single L_matter schema seed. The sharpened theorem is: if parent constructors are exhausted and Hom(SpeciesLabel,Coeff_active_source) is empty, then source-only w_A is ill-typed; adding one action-density line, common hbar/measure, species-blind Jacobian, connected ordinary-matter graph and readout no-reentry kills Delta_w_A. Current MTS has this as an exact conditional theorem, not a signed result. The finite WEP branch is improved by attaching the local MICROSCOPE official comparator PDF and compact parent WEP clause, but the MTS prediction value remains missing.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "public_claim": False,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {"status_id": "STAT4423_0_best_result", "status": "TYPED_HOM_NO_SLOT_THEOREM_NARROWED", "detail": "No-source-only coupling is now a Hom/exhaustion theorem target, not vague missing coupling.", "valid_for_claim": False},
        {"status_id": "STAT4423_1_open_parent_proof", "status": "PARENT_CONSTRUCTOR_EXHAUSTION_NOT_DERIVED", "detail": "Need primitive constructor list and no-reentry proof from MTS, or finite coefficient values.", "valid_for_claim": False},
        {"status_id": "STAT4423_2_finite_branch", "status": "PWEP_OFFICIAL_PROVENANCE_ATTACHED_PREDICTION_MISSING", "detail": "MICROSCOPE PDF and WEP parent-clause paths are attached; no MTS Delta_w*tau value.", "valid_for_claim": False},
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4423_0",
            "target": NEXT_TARGET,
            "objective": "Try to derive parent constructor exhaustion from MTS primitives; if it fails, fill the first numeric/source-backed parent WEP coefficient rather than another comparator-only row.",
            "derive_first": "construct the allowed parent object constructors from motion/time/space/observed quotient data and prove no Hom from species/source labels to active source coefficients.",
            "fallback": "fill C_parent_WEP_TiPt, Delta_w_TiPt*tau_WEP, or an R_eq/B_zero value with numeric parent coefficient, projection source, official comparator source and no-cancellation guard.",
            "avoid": "calling a positive action ansatz a proof; treating the MICROSCOPE bound as an MTS prediction; hiding w_A in measured G; skipping readout/EFT no-reentry.",
            "valid_for_claim": False,
        }
    ]


def build_doc(sources: Sequence[Mapping[str, object]], density_out: Sequence[Mapping[str, str]], value_out: Sequence[Mapping[str, str]], gates: Sequence[Mapping[str, object]]) -> str:
    return f"""# 439 PPC4161 action-density line owner or first source-backed P_WEP/R_eq value

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4423 advances the coupling route in two concrete ways:

- The local action-density proof is no longer just "missing coupling"; it is now a typed parent-constructor/Hom theorem.
- The exact no-slot condition is: `Hom(SpeciesLabel, Coeff_active_source)=empty` after parent constructor exhaustion.
- The full source-weight zero theorem also needs one action-density line, common `hbar`/measure, species-blind Jacobian, connected ordinary-matter graph, and readout/EFT no-reentry.
- The current MTS corpus has the right `L_matter` action schema seed, but not the parent constructor-exhaustion proof.
- The finite WEP branch now carries real local MICROSCOPE comparator provenance and a compact parent WEP zero-shape clause, while still refusing to treat the bound as an MTS prediction.

## Source Register

{table(sources)}

## Derivation Rows

{table(derivation_rows())}

## Action-Density Owner Gate

{table(density_out)}

## First Source-Backed Value Gate

{table(value_out)}

## Claim Gates

{table(gates)}

## Decision

{table(decision_rows())}

## Next Target

{table(next_rows())}
"""


def post_doc() -> str:
    return f"""# 4423 - action-density line owner or first source-backed P_WEP/R_eq value

Marker: `{MARKER}`

Private checkpoint generated at `{STAMP}`.

## What changed

- Recast the action-density owner problem as a parent constructor-exhaustion / Hom no-slot theorem.
- Preserved the useful MTS `L_matter` schema seed without pretending it proves the no-slot rule.
- Added an executable action-density owner gate and source-backed finite-value gate.
- Attached local MICROSCOPE comparator PDF provenance and compact parent WEP clause provenance to the P_WEP fallback row.

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
        "claim": "4423 narrows the source-coupling/action-density owner route to a typed parent-constructor theorem: if parent constructors are exhausted and Hom(SpeciesLabel,Coeff_active_source) is empty, then source-only w_A is ill-typed; with one action-density line, common hbar/measure, species-blind Jacobian, connected matter graph and readout no-reentry, Delta_w_A would vanish. Current MTS has this only as a conditional theorem. The finite WEP branch now has local official MICROSCOPE comparator provenance but no MTS prediction value.",
        "current_evidence": "4423 source register, derivation rows, action-density owner output, source-backed value output, claim gates, decision, status, next target and validation CSV.",
        "status": "typed_hom_action_density_theorem_conditional_pwep_provenance_nonclaim",
        "next_test": "Derive parent constructor exhaustion from MTS primitives, or fill a numeric/source-backed parent WEP coefficient.",
        "key_risk": "Calling a positive matter-action ansatz a proof; treating comparator bounds as predictions; hiding source weights in measured G; skipping readout/EFT no-reentry.",
        "sector": "local_gr",
        "evidence": "4423 source register, derivation rows, action-density owner output, source-backed value output, claim gates, decision, status, next target and validation CSV.",
        "next_action": "Derive parent constructor exhaustion from MTS primitives, or fill a numeric/source-backed parent WEP coefficient.",
        "risk": "Calling a positive matter-action ansatz a proof; treating comparator bounds as predictions; hiding source weights in measured G; skipping readout/EFT no-reentry.",
    }
    rows.append({name: new_row.get(name, "") for name in fieldnames})
    with CLAIMS_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_spine_and_packet() -> None:
    spine_section = f"""## 4423 local spine update: coupling as a typed Hom/no-slot theorem

4423 moves the coupling proof target forward. The remaining `w_A/hbar_A` problem is now a parent constructor-exhaustion problem: prove `Hom(SpeciesLabel, Coeff_active_source)=empty` after constructing all admissible matter-action arguments from MTS motion/time/space/observed quotient data. The core `L_matter` action schema is a real seed, but not a proof of exhaustion. The WEP finite branch is also cleaner: local MICROSCOPE comparator provenance and the compact parent WEP clause are attached, but no MTS prediction value is claimed.
"""
    packet_section = f"""## 4423 packet update: action-density owner gate

`{PACKET_MARKER}`

Private packet result: source coupling is now pinned to a typed object-language theorem. If the parent action proves no species/source-label Hom into active source coefficients and owns one action-density/measure line, `w_A` is not an allowed object. If this does not close, the next honest move is a numeric/source-backed parent WEP coefficient.
"""
    upsert_marked_section(SPINE_PATH, MARKER, spine_section)
    upsert_marked_section(PACKET_PATH, PACKET_MARKER, packet_section)


def validation_rows(paths: Mapping[str, Path]) -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    density = {row["row_id"]: row for row in rows_from(DENSITY_OUTPUT)}
    values = {row["value_id"]: row for row in rows_from(VALUE_OUTPUT)}
    gates = rows_from(CLAIM_GATES)
    no_claims = not any(row.get("valid_for_claim") == "True" for row in density.values()) and not any(row.get("valid_for_claim") == "True" for row in values.values())
    checks = [
        ("VAL4423_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source path exists"),
        ("VAL4423_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited text source needle is present"),
        ("VAL4423_2_core_schema_status", density["ADLO4423_0_core_MTS_action_schema"].get("current_status") == "ACTION_DENSITY_OWNER_PARTIAL_PARENT_SYNTAX", "core L_matter is schema seed only"),
        ("VAL4423_3_hom_no_slot_status", density["ADLO4423_2_hom_no_slot_contract"].get("current_status") == "HOM_NO_SLOT_READY_ACTION_MEASURE_OPEN", "Hom no-slot theorem is executable but action-measure open"),
        ("VAL4423_4_action_owner_dependency", density["ADLO4423_3_action_owner_after_no_slot"].get("current_status") == "ACTION_OWNER_READY_CONNECTIVITY_READOUT_OPEN", "connectivity/readout no-reentry separated from action owner"),
        ("VAL4423_5_future_contract", density["ADLO4423_4_future_action_density_owner_contract"].get("current_status") == "ACTION_DENSITY_OWNER_CONTRACT_READY_NONCLAIM", "future action-density owner contract executable nonclaim"),
        ("VAL4423_6_PWEP_source_exists", values["PV4423_0_PWEP_official_bound_attached"].get("official_numeric_source_exists") == "True", "P_WEP official comparator source exists locally"),
        ("VAL4423_7_PWEP_prediction_missing", values["PV4423_0_PWEP_official_bound_attached"].get("current_status") == "COMPARATOR_ANCHOR_READY_PREDICTION_VALUE_MISSING_NONCLAIM", "P_WEP row remains prediction-missing"),
        ("VAL4423_8_Cparent_zero_shape", values["PV4423_1_Cparent_WEP_zero_shape"].get("current_status") == "COMPARATOR_ANCHOR_READY_PREDICTION_VALUE_MISSING_NONCLAIM", "C_parent WEP zero shape is nonclaim"),
        ("VAL4423_9_Req_gap_schema", values["PV4423_2_Req_radial_gap_ledger"].get("current_status") == "PREDICTION_SCHEMA_READY_VALUES_MISSING_NONCLAIM", "R_eq/B_zero gap row remains schema only"),
        ("VAL4423_10_no_claim_outputs", no_claims, "no generated row is claim-ready"),
        ("VAL4423_11_claim_gates", any(row["gate_id"] == "CG4423_6_no_claim_outputs" and row["passed"] == "True" for row in gates), "claim gates explicitly block public claim"),
        ("VAL4423_12_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-264"),
        ("VAL4423_13_formal_doc", paths["formal"].exists() and MARKER in text(paths["formal"]), "formal doc exists with marker"),
        ("VAL4423_14_post_doc", paths["post"].exists() and "Private checkpoint" in text(paths["post"]), "post checkpoint doc exists"),
        ("VAL4423_15_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4423_16_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4423_17_next_target", paths["next"].exists() and NEXT_TARGET in text(paths["next"]), "next target file exists"),
        ("VAL4423_18_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": bool(passed), "detail": detail} for check_id, passed, detail in checks]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(DERIVATION_ROWS, derivation_rows())
    write_csv(DENSITY_INPUT, density_input_rows())
    write_csv(VALUE_INPUT, value_input_rows())
    write_csv(DENSITY_OUTPUT, evaluate_density_owner_rows(DENSITY_INPUT))
    write_csv(VALUE_OUTPUT, evaluate_value_rows(VALUE_INPUT))
    density_output = rows_from(DENSITY_OUTPUT)
    value_output = rows_from(VALUE_OUTPUT)
    gates = claim_gate_rows(density_output, value_output)
    write_csv(CLAIM_GATES, gates)
    write_csv(DECISION_CSV, decision_rows())
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    write_text(FORMAL_PATH, build_doc(rows_from(SOURCE_REGISTER), density_output, value_output, gates))
    write_text(DOC_PATH, post_doc())
    update_claims_register()
    write_spine_and_packet()
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    write_csv(VALIDATION_PATH, validation_rows({"formal": FORMAL_PATH, "post": DOC_PATH, "next": NEXT_CSV}))


if __name__ == "__main__":
    main()

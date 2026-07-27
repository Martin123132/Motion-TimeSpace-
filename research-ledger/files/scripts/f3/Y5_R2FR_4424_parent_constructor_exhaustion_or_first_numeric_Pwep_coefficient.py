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

from constructor_exhaustion_wep_gate import evaluate_coefficient_rows, evaluate_constructor_rows, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
COEFF_DIR = POST / "source-intake" / "microscope" / "branch_locked_wep" / "coefficients"
CORE = ROOT / "core-mts-framework"

CHECKPOINT = "4424"
CLAIM_ID = "L-265"
MARKER = "PPC4161_PARENT_CONSTRUCTOR_EXHAUSTION_OR_FIRST_NUMERIC_PWEP_COEFFICIENT_4424"
PACKET_MARKER = "PPC4161_PACKET_PARENT_CONSTRUCTOR_EXHAUSTION_OR_FIRST_NUMERIC_PWEP_COEFFICIENT_4424"
DECISION = "PARENT_CONSTRUCTOR_ATLAS_READY_EXHAUSTION_BLOCKED_BY_HIDDEN_READOUT_REENTRY_NO_NUMERIC_PARENT_PWEP_COEFFICIENT"
NEXT_TARGET = "4425-Y5-R2FR-hidden-invariant-no-extension-or-live-Cparent-WEP-import-row.md"

FORMAL_PATH = FORMAL / "440-PPC4161-parent-constructor-exhaustion-or-first-numeric-Pwep-coefficient.md"
DOC_PATH = POST / "4424-Y5-R2FR-parent-constructor-exhaustion-or-first-numeric-Pwep-coefficient.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4424_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4424_SOURCE_REGISTER.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4424_DERIVATION_ROWS.csv"
CONSTRUCTOR_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4424_CONSTRUCTOR_EXHAUSTION_INPUT.csv"
CONSTRUCTOR_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4424_CONSTRUCTOR_EXHAUSTION_OUTPUT.csv"
COEFFICIENT_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4424_PWEP_COEFFICIENT_INPUT.csv"
COEFFICIENT_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4424_PWEP_COEFFICIENT_OUTPUT.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4424_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4424_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4424_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4424_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "constructor_exhaustion_wep_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4424_parent_constructor_exhaustion_or_first_numeric_Pwep_coefficient.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4423 = SOURCE_DIR / "P8_Y5_R2FR_4423_NEXT_TARGET.csv"
FORMAL_439 = FORMAL / "439-PPC4161-action-density-line-owner-or-first-source-backed-Pwep-Req-value.md"
CORE_ACTION = CORE / "action-principle" / "the-motion-timespace-action-principle.md"
CORE_FUNDAMENTAL = CORE / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md"
CORE_EFFECTIVE = CORE / "field-theory" / "the-effective-field-theory-of-motion-timespace.md"
CORE_TIME = CORE / "relativity" / "time-as-thermodynamic-exchange-in-motion-timespace-a-unified-framework-for-relativity-and-thermodynamics.md"
CSV_1107 = SOURCE_DIR / "P8_Y5_R10_1107_OBJECT_LANGUAGE_EXHAUSTION_ATTEMPT.csv"
CSV_1236 = SOURCE_DIR / "P8_Y5_R10_1236_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv"
CSV_1338 = SOURCE_DIR / "P8_Y5_R10_1338_OBJECT_LANGUAGE_THEOREM_ATTEMPT.csv"
CSV_2304 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2304_OBJECT_LANGUAGE_INDEX_LEMMA.csv"
CSV_2434 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2434_TYPED_OBJECT_LANGUAGE_CERTIFICATE.csv"
CSV_2681 = COEFF_DIR / "coefficient_target_inventory_nonclaim_2681.csv"
CSV_2682 = COEFF_DIR / "coefficient_target_classification_nonclaim_2682.csv"
CDH_1480 = COEFF_DIR / "coefficient_domain_Hom_exclusion_attempt_nonclaim_1480.csv"
C_PARENT = COEFF_DIR / "C_parent.csv"
C_SCHEMA = COEFF_DIR / "C_parent_import_schema.csv"
C_SLOT_TEMPLATE = COEFF_DIR / "C_parent_WEP_slot_import_TEMPLATE.csv"
C_SLOT_REFUSED = COEFF_DIR / "C_parent_WEP_slot_import_REFUSED_1447.csv"
CX_CONTRACT = COEFF_DIR / "C_parent_WEP_finite_CX_contract_1911_nonclaim.csv"
ALPHA_COMPONENTS = COEFF_DIR / "alpha_product_component_source_pack_nonclaim_1472.csv"
CI_SMOKE = COEFF_DIR / "Ci_smoke_evaluator_results_nonclaim_1475.csv"
ACTION_LINE_AUDIT = COEFF_DIR / "action_density_line_owner_audit_nonclaim_2679.csv"
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
        {"source_id": "SRC4424_00_4423_next", "path": NEXT_4423, "needle": "4424-Y5-R2FR-parent-constructor-exhaustion-or-first-numeric-Pwep-coefficient.md", "role": "4423 handoff."},
        {"source_id": "SRC4424_01_439_formal", "path": FORMAL_439, "needle": "ADL4423_1_typed_Hom_no_slot_theorem", "role": "typed Hom/no-slot theorem target."},
        {"source_id": "SRC4424_02_core_action", "path": CORE_ACTION, "needle": "The fundamental object is a scalar motion field", "role": "MTS primitive motion field."},
        {"source_id": "SRC4424_03_core_action_lmatter", "path": CORE_ACTION, "needle": "L_matter the standard matter Lagrangian", "role": "single matter action schema seed."},
        {"source_id": "SRC4424_04_core_fundamental", "path": CORE_FUNDAMENTAL, "needle": "A[g,ψ]", "role": "MTS-Einstein action and microscopic action."},
        {"source_id": "SRC4424_05_core_effective", "path": CORE_EFFECTIVE, "needle": "The effective action is the coarse-grained functional integral", "role": "coarse-grained functional-integral map."},
        {"source_id": "SRC4424_06_core_time", "path": CORE_TIME, "needle": "time is not an independent dimension", "role": "time/space exchange primitive."},
        {"source_id": "SRC4424_07_1107_exhaustion", "path": CSV_1107, "needle": "EXH1107_6_verdict", "role": "prior constructor exhaustion attempt."},
        {"source_id": "SRC4424_08_1236_certificate", "path": CSV_1236, "needle": "CERT1236_6_current_verdict", "role": "typed certificate not parent-derived."},
        {"source_id": "SRC4424_09_1338_no_slot", "path": CSV_1338, "needle": "OLT1338_2_MTS_primitive_constructor", "role": "MTS primitive constructor gap."},
        {"source_id": "SRC4424_10_2304_index", "path": CSV_2304, "needle": "OLI2304_3_spurion_necessity", "role": "example of constructor grammar becoming an index theorem."},
        {"source_id": "SRC4424_11_2434_typed", "path": CSV_2434, "needle": "TOL2434_7_verdict", "role": "R2/f(R) typed object-language verdict."},
        {"source_id": "SRC4424_12_2681_inventory", "path": CSV_2681, "needle": "TGT2681_4_active_source_prefactor", "role": "coefficient target inventory."},
        {"source_id": "SRC4424_13_2682_classification", "path": CSV_2682, "needle": "TC2682_4_source_prefactor", "role": "coefficient target classification."},
        {"source_id": "SRC4424_14_hom_1480", "path": CDH_1480, "needle": "CDH1480_5_verdict", "role": "Hom exclusion obstruction."},
        {"source_id": "SRC4424_15_Cparent", "path": C_PARENT, "needle": "CP1430_6_verdict", "role": "C_parent vector has no scoreable parent coefficient."},
        {"source_id": "SRC4424_16_import_schema", "path": C_SCHEMA, "needle": "value,float_or_DERIVED_ZERO", "role": "parent coefficient import schema."},
        {"source_id": "SRC4424_17_slot_template", "path": C_SLOT_TEMPLATE, "needle": "MISSING_DERIVED_ZERO_OR_NUMERIC_VALUE", "role": "live slot import template remains unfilled."},
        {"source_id": "SRC4424_18_slot_refused", "path": C_SLOT_REFUSED, "needle": "REFUSED_NO_SOURCE_SIGNED_FUNCTIONAL_DERIVATIVE", "role": "prior import refusal."},
        {"source_id": "SRC4424_19_CX_contract", "path": CX_CONTRACT, "needle": "FINITE_CX_CONTRACT_ONLY_NOT_FILLED", "role": "finite parent WEP component contracts."},
        {"source_id": "SRC4424_20_alpha_components", "path": ALPHA_COMPONENTS, "needle": "CSP1472_3_DeltaQ_WEP", "role": "numeric sensitivity component, not parent coefficient."},
        {"source_id": "SRC4424_21_Ci_smoke", "path": CI_SMOKE, "needle": "MISSING_THEOREM_ZERO_OR_NUMERIC_INPUT", "role": "same-branch coefficient smoke results."},
        {"source_id": "SRC4424_22_action_line_audit", "path": ACTION_LINE_AUDIT, "needle": "ADO2679_5_connected_morphisms", "role": "action-line connectivity audit."},
        {"source_id": "SRC4424_23_wep_pdf", "path": WEP_PDF, "needle": "", "role": "local MICROSCOPE comparator PDF."},
        {"source_id": "SRC4424_24_gate", "path": GATE_PATH, "needle": "def evaluate_constructor_row", "role": "4424 constructor/coefficient gate."},
        {"source_id": "SRC4424_25_generator", "path": GENERATOR_PATH, "needle": "PARENT_CONSTRUCTOR_ATLAS_READY", "role": "4424 generator."},
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
            "derivation_id": "CEX4424_0_parent_generate_normal_form",
            "claim": "Parent constructor exhaustion can be phrased as an image theorem.",
            "derivation": "Define ParentGenerate_MTS as the constructor closure generated by the microscopic motion field psi, time/space exchange, the observed metric/coframe from smoothed psi-gradients, standard matter representation data, gauge/current data and universal constants. Constructor exhaustion is the statement that every local ordinary-sector coefficient lies in Image(ParentGenerate_MTS).",
            "consequence": "This turns 'no source-only slot' into a finite theorem target rather than taste.",
            "status": "PARENT_GENERATE_NORMAL_FORM_WRITTEN",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "CEX4424_1_chain_rule_win",
            "claim": "If a coefficient is in Image(ParentGenerate_MTS), vertical source-label drift is killed.",
            "derivation": "For c_vis(Phi)=cbar(q(Phi),theta_rep) with Dq[v]=0 and theta_rep fixed, Lie_v c_vis=0. Therefore a species/source label can only make an active source coefficient if it is an admitted constructor or a hidden/readout re-entry.",
            "consequence": "The mathematical core is solid; the remaining fight is constructor membership and re-entry.",
            "status": "EXACT_CONDITIONAL_CHAIN_RULE",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "CEX4424_2_Hom_no_slot_result",
            "claim": "Hom(SpeciesLabel,Coeff_active_source)=empty follows if constructor exhaustion and no-reentry close.",
            "derivation": "Species labels may index representation fields and measured constants, but if Coeff_active_source is not a parent target and hidden markers/readout maps cannot extend that target, there is no morphism from SpeciesLabel to active source weights. Then w_A S_A is ill-typed except for one common calibration mode.",
            "consequence": "This is the cleanest local GR/Newton source-coupling theorem path currently available.",
            "status": "EXACT_IF_EXHAUSTION_AND_NO_REENTRY_SIGNED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "CEX4424_3_current_failure_witness",
            "claim": "Current MTS does not yet prove constructor exhaustion.",
            "derivation": "The core corpus gives psi, emergent geometry and one L_matter schema, but it does not prove that all effective/radiative/readout coefficient targets are generated by those primitives. Hidden invariant scalars, source-prefactor targets and readout tails remain legal countermodels unless no-extension is signed.",
            "consequence": "No local-GR source-coupling claim fires from constructor language alone.",
            "status": "EXHAUSTION_BLOCKED_BY_HIDDEN_READOUT_REENTRY",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "CEX4424_4_coefficient_scan_result",
            "claim": "No numeric/source-backed parent WEP coefficient is found in the active local coefficient set.",
            "derivation": "The coefficient directory contains comparator and sensitivity components, including numeric DeltaQ_alpha and clock sensitivities, but C_parent_WEP_TiPt and the finite C_i parent coefficients remain MISSING_* or import-refused. Those numeric components are not MTS parent coefficients because the parent basis, functional derivative and source-independent coefficient value are absent.",
            "consequence": "The finite branch is now audited: do not promote sensitivity/comparator numbers to MTS predictions.",
            "status": "NO_NUMERIC_PARENT_PWEP_COEFFICIENT_FOUND",
            "valid_for_claim": False,
        },
    ]


def constructor_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "CEX4424_0_core_MTS_primitives",
            "branch": "psi_metric_Lmatter_seed",
            "motion_primitive_declared": True,
            "time_space_exchange_declared": True,
            "observed_metric_constructed": True,
            "matter_action_constructor_declared": True,
            "parent_generate_map_defined": False,
            "constructor_image_exhaustive": False,
            "hom_species_source_empty": False,
            "hidden_invariant_algebra_trivial": False,
            "no_extension_marker": False,
            "radiative_readout_closure": False,
            "source_path": str(CORE_ACTION),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Core MTS gives psi, emergent metric and L_matter seed, not a full ParentGenerate map.",
        },
        {
            "row_id": "CEX4424_1_parent_generate_atlas",
            "branch": "parent_constructor_atlas_from_MTS_primitives",
            "motion_primitive_declared": True,
            "time_space_exchange_declared": True,
            "observed_metric_constructed": True,
            "matter_action_constructor_declared": True,
            "parent_generate_map_defined": True,
            "constructor_image_exhaustive": False,
            "hom_species_source_empty": False,
            "hidden_invariant_algebra_trivial": False,
            "no_extension_marker": False,
            "radiative_readout_closure": False,
            "source_path": str(CSV_1107),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Normal form is written: all local coefficients must be in Image(ParentGenerate_MTS), but membership is not proved.",
        },
        {
            "row_id": "CEX4424_2_Hom_no_slot_if_exhausted",
            "branch": "Hom_species_to_active_source_empty",
            "motion_primitive_declared": True,
            "time_space_exchange_declared": True,
            "observed_metric_constructed": True,
            "matter_action_constructor_declared": True,
            "parent_generate_map_defined": True,
            "constructor_image_exhaustive": True,
            "hom_species_source_empty": True,
            "hidden_invariant_algebra_trivial": False,
            "no_extension_marker": False,
            "radiative_readout_closure": False,
            "source_path": str(CSV_1338),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "If constructor exhaustion is granted, the Hom no-slot theorem works, but hidden/readout re-entry remains open.",
        },
        {
            "row_id": "CEX4424_3_hidden_scalar_readout_obstruction",
            "branch": "hidden_invariant_and_readout_tail_countermodel",
            "motion_primitive_declared": True,
            "time_space_exchange_declared": True,
            "observed_metric_constructed": True,
            "matter_action_constructor_declared": True,
            "parent_generate_map_defined": True,
            "constructor_image_exhaustive": True,
            "hom_species_source_empty": True,
            "hidden_invariant_algebra_trivial": False,
            "no_extension_marker": False,
            "radiative_readout_closure": False,
            "source_path": str(CDH_1480),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Scalar invariant and radiative/readout countermodels remain live unless no-extension is derived.",
        },
        {
            "row_id": "CEX4424_4_future_constructor_exhaustion_contract",
            "branch": "future_parent_constructor_exhaustion_contract",
            "motion_primitive_declared": True,
            "time_space_exchange_declared": True,
            "observed_metric_constructed": True,
            "matter_action_constructor_declared": True,
            "parent_generate_map_defined": True,
            "constructor_image_exhaustive": True,
            "hom_species_source_empty": True,
            "hidden_invariant_algebra_trivial": True,
            "no_extension_marker": True,
            "radiative_readout_closure": True,
            "source_path": str(CSV_1236),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Exact future contract only; nonclaim until parent-signed.",
        },
    ]


def coefficient_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "CPWEP4424_0_slot_import_template",
            "coefficient": "C_parent_WEP_TiPt",
            "coefficient_kind": "parent_coefficient",
            "value": "MISSING_DERIVED_ZERO_OR_NUMERIC_VALUE",
            "units": "MISSING_PARENT_BASIS_UNITS",
            "source_path": str(C_SLOT_TEMPLATE),
            "comparator_source": str(WEP_PDF),
            "independent_of_bound": False,
            "parent_basis_declared": False,
            "sign_convention_declared": False,
            "zero_certificate_source": "MISSING_PARENT_THEOREM_OR_NUMERIC_SOURCE_PATH",
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "The live import shape exists only as a template; no value is importable.",
        },
        {
            "row_id": "CPWEP4424_1_Cparent_vector_verdict",
            "coefficient": "C_parent_vector",
            "coefficient_kind": "parent_coefficient",
            "value": "NOT_SCOREABLE",
            "units": "NOT_CLAIM_UNITS",
            "source_path": str(C_PARENT),
            "comparator_source": str(WEP_PDF),
            "independent_of_bound": False,
            "parent_basis_declared": False,
            "sign_convention_declared": False,
            "zero_certificate_source": "MISSING_ZERO_CERTIFICATE",
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Existing C_parent vector explicitly says placeholder rows only.",
        },
        {
            "row_id": "CPWEP4424_2_finite_CX_electron_contract",
            "coefficient": "C_e",
            "coefficient_kind": "parent_coefficient",
            "value": "MISSING_PARENT_COEFFICIENT",
            "units": "dimensionless_parent_WEP_basis",
            "source_path": str(CX_CONTRACT),
            "comparator_source": str(WEP_PDF),
            "independent_of_bound": False,
            "parent_basis_declared": True,
            "sign_convention_declared": False,
            "zero_certificate_source": "MISSING_PARENT_ZERO_CERTIFICATE",
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Finite component contract is present, but no parent coefficient value is filled.",
        },
        {
            "row_id": "CPWEP4424_3_numeric_DeltaQ_alpha_component",
            "coefficient": "DeltaQ_alpha_AB",
            "coefficient_kind": "sensitivity_component",
            "value": "1.989808886825000e-03",
            "units": "dimensionless_smoke_material_contrast",
            "source_path": str(ALPHA_COMPONENTS),
            "comparator_source": str(WEP_PDF),
            "independent_of_bound": True,
            "parent_basis_declared": False,
            "sign_convention_declared": False,
            "zero_certificate_source": "MISSING_NOT_A_ZERO_CERTIFICATE",
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Numeric component exists, but it is not a parent MTS coefficient.",
        },
        {
            "row_id": "CPWEP4424_4_import_refused",
            "coefficient": "C_parent_WEP_TiPt",
            "coefficient_kind": "parent_coefficient",
            "value": "MISSING_REFUSED_NO_SOURCE_SIGNED_FUNCTIONAL_DERIVATIVE",
            "units": "MISSING_PARENT_BASIS_UNITS",
            "source_path": str(C_SLOT_REFUSED),
            "comparator_source": str(WEP_PDF),
            "independent_of_bound": False,
            "parent_basis_declared": False,
            "sign_convention_declared": False,
            "zero_certificate_source": "MISSING_PARENT_ZERO_CERTIFICATE",
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Prior import was explicitly refused because no source-signed functional derivative exists.",
        },
    ]


def claim_gate_rows(constructor_out: Sequence[Mapping[str, str]], coeff_out: Sequence[Mapping[str, str]]) -> List[Dict[str, object]]:
    constructors = {row["row_id"]: row for row in constructor_out}
    coeffs = {row["row_id"]: row for row in coeff_out}
    no_claims = not any(row.get("valid_for_claim") == "True" for row in constructor_out) and not any(
        row.get("valid_for_claim") == "True" for row in coeff_out
    )
    return [
        {"gate_id": "CG4424_0_primitive_atlas", "claim": "MTS primitive constructor atlas is ready", "passed": constructors["CEX4424_1_parent_generate_atlas"].get("current_status") == "PRIMITIVE_CONSTRUCTOR_ATLAS_READY_EXHAUSTION_OPEN", "valid_for_claim": False, "detail": "atlas normal form exists; exhaustion remains open."},
        {"gate_id": "CG4424_1_Hom_no_slot", "claim": "Hom no-slot theorem works if exhausted", "passed": constructors["CEX4424_2_Hom_no_slot_if_exhausted"].get("current_status") == "HOM_NO_SLOT_READY_HIDDEN_READOUT_REENTRY_OPEN", "valid_for_claim": False, "detail": "no-slot route is exact conditional."},
        {"gate_id": "CG4424_2_hidden_reentry", "claim": "hidden/readout re-entry is closed", "passed": False, "valid_for_claim": False, "detail": "hidden invariant algebra and readout/EFT closure are not parent-signed."},
        {"gate_id": "CG4424_3_future_contract", "claim": "constructor exhaustion contract is executable", "passed": constructors["CEX4424_4_future_constructor_exhaustion_contract"].get("current_status") == "PARENT_CONSTRUCTOR_EXHAUSTION_CONTRACT_READY_NONCLAIM", "valid_for_claim": False, "detail": "future contract closes only with input_valid=false."},
        {"gate_id": "CG4424_4_numeric_component_not_parent", "claim": "numeric WEP component is not a parent coefficient", "passed": coeffs["CPWEP4424_3_numeric_DeltaQ_alpha_component"].get("current_status") == "NUMERIC_COMPONENT_NOT_PARENT_COEFFICIENT", "valid_for_claim": False, "detail": "DeltaQ_alpha is useful but cannot be scored as C_parent."},
        {"gate_id": "CG4424_5_no_numeric_parent_coefficient", "claim": "active set contains a numeric/source-backed parent WEP coefficient", "passed": False, "valid_for_claim": False, "detail": "all parent coefficient rows are missing, refused, or contract-only."},
        {"gate_id": "CG4424_6_no_claim_outputs", "claim": "4424 generated no claim-ready row", "passed": no_claims, "valid_for_claim": False, "detail": "checkpoint advances proof target and coefficient audit only."},
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4424_0",
            "decision": DECISION,
            "summary": "4424 attempts the derivation route. It constructs a clean ParentGenerate_MTS normal form from psi, time/space exchange, observed geometry and one L_matter action schema. The chain-rule part is exact: coefficients in Image(ParentGenerate_MTS) are vertical-source-label silent. The current failure is not the theorem shape; it is proving constructor-image exhaustion and closing hidden invariant/readout re-entry. The WEP fallback scan finds numeric sensitivity/comparator components but no numeric/source-backed parent WEP coefficient or DERIVED_ZERO certificate.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "public_claim": False,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {"status_id": "STAT4424_0_best_result", "status": "PARENT_GENERATE_NORMAL_FORM_READY", "detail": "Constructor exhaustion has a concrete image-theorem shape.", "valid_for_claim": False},
        {"status_id": "STAT4424_1_open_proof", "status": "HIDDEN_INVARIANT_AND_READOUT_REENTRY_BLOCK_EXHAUSTION", "detail": "Need hidden invariant algebra triviality, no-extension marker theorem and radiative/readout closure.", "valid_for_claim": False},
        {"status_id": "STAT4424_2_finite_branch", "status": "NO_NUMERIC_PARENT_PWEP_COEFFICIENT_FOUND", "detail": "Numeric sensitivity components exist, but parent coefficient import remains missing/refused.", "valid_for_claim": False},
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4424_0",
            "target": NEXT_TARGET,
            "objective": "Try to derive hidden-invariant no-extension and radiative/readout closure for the constructor atlas; if it fails, create a live C_parent_WEP import row only with a real numeric or DERIVED_ZERO source.",
            "derive_first": "prove O(C_hid)^inv=R or otherwise forbid maps from hidden/material/readout markers into Coeff_active_source under MTS ParentGenerate.",
            "fallback": "fill C_parent_WEP_TiPt or one C_i with numeric value or DERIVED_ZERO certificate, units, sign, parent basis, source path and independence from MICROSCOPE bound.",
            "avoid": "using DeltaQ or clock sensitivity as a parent coefficient; importing template rows; treating no-slot grammar as parent-derived before no-reentry closes.",
            "valid_for_claim": False,
        }
    ]


def build_doc(sources: Sequence[Mapping[str, object]], constructor_out: Sequence[Mapping[str, str]], coeff_out: Sequence[Mapping[str, str]], gates: Sequence[Mapping[str, object]]) -> str:
    return f"""# 440 PPC4161 parent constructor exhaustion or first numeric P_WEP coefficient

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4424 takes the leap at the right place:

- The parent-constructor route is now an explicit image theorem: all ordinary-sector coefficients must lie in `Image(ParentGenerate_MTS)`.
- The exact chain-rule win is banked: if `c_vis(Phi)=cbar(q(Phi),theta_rep)` and `Dq[v]=0`, then source-label/vertical drift cannot create an active source coefficient.
- Therefore `Hom(SpeciesLabel, Coeff_active_source)=empty` follows if constructor exhaustion and no hidden/readout re-entry are parent-signed.
- Current MTS does **not** yet prove that exhaustion: hidden invariant scalars, no-extension markers, and radiative/readout tails remain live countermodels.
- The WEP fallback scan finds numeric sensitivity/comparator components, but no numeric/source-backed MTS parent WEP coefficient or `DERIVED_ZERO` certificate.

## Source Register

{table(sources)}

## Derivation Rows

{table(derivation_rows())}

## Constructor Exhaustion Gate

{table(constructor_out)}

## P_WEP Coefficient Gate

{table(coeff_out)}

## Claim Gates

{table(gates)}

## Decision

{table(decision_rows())}

## Next Target

{table(next_rows())}
"""


def post_doc() -> str:
    return f"""# 4424 - parent constructor exhaustion or first numeric P_WEP coefficient

Marker: `{MARKER}`

Private checkpoint generated at `{STAMP}`.

## What changed

- Wrote the constructor-exhaustion problem as `Image(ParentGenerate_MTS)`.
- Banked the exact chain-rule result for coefficients already in the parent-generated image.
- Identified the live obstruction: hidden invariant / marker / radiative-readout re-entry.
- Scanned WEP coefficient sources enough to separate numeric sensitivity components from actual parent coefficients.

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
        "claim": "4424 writes the parent constructor-exhaustion route as an Image(ParentGenerate_MTS) theorem and banks the exact chain-rule result for parent-generated coefficients. It remains nonclaim because hidden invariant algebra, no-extension markers and radiative/readout closure are not parent-signed. The WEP coefficient scan finds numeric sensitivity/comparator components but no numeric/source-backed MTS parent WEP coefficient or DERIVED_ZERO certificate.",
        "current_evidence": "4424 source register, derivation rows, constructor exhaustion output, P_WEP coefficient output, claim gates, decision, status, next target and validation CSV.",
        "status": "parent_generate_constructor_atlas_ready_exhaustion_hidden_reentry_open_no_numeric_parent_pwep_coefficient",
        "next_test": "Derive hidden-invariant no-extension/readout closure, or fill a real C_parent_WEP import row with numeric/DERIVED_ZERO source.",
        "key_risk": "Using sensitivity components as parent coefficients; importing templates; declaring constructor grammar exhausted without no-reentry proof.",
        "sector": "local_gr",
        "evidence": "4424 source register, derivation rows, constructor exhaustion output, P_WEP coefficient output, claim gates, decision, status, next target and validation CSV.",
        "next_action": "Derive hidden-invariant no-extension/readout closure, or fill a real C_parent_WEP import row with numeric/DERIVED_ZERO source.",
        "risk": "Using sensitivity components as parent coefficients; importing templates; declaring constructor grammar exhausted without no-reentry proof.",
    }
    rows.append({name: new_row.get(name, "") for name in fieldnames})
    with CLAIMS_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_spine_and_packet() -> None:
    spine_section = f"""## 4424 local spine update: constructor exhaustion as an image theorem

4424 turns the source-coupling syntax problem into a cleaner theorem: construct `ParentGenerate_MTS` from the MTS primitives and prove ordinary-sector coefficients lie in its image. The chain rule then kills source-label drift automatically. The remaining obstruction is precise: hidden invariant scalars, marker extensions, and radiative/readout tails can still map into active source coefficients unless no-extension is derived. The WEP coefficient scan also prevents a bad shortcut: numeric sensitivity components exist, but no numeric/source-backed parent WEP coefficient is available yet.
"""
    packet_section = f"""## 4424 packet update: ParentGenerate_MTS

`{PACKET_MARKER}`

Private packet result: the next proof is not "find the coupling" in the fog. It is: prove `Image(ParentGenerate_MTS)` exhausts visible source coefficient targets and no hidden/readout map extends it. If that fails, only a real `C_parent_WEP` numeric or `DERIVED_ZERO` import row can move the finite branch.
"""
    upsert_marked_section(SPINE_PATH, MARKER, spine_section)
    upsert_marked_section(PACKET_PATH, PACKET_MARKER, packet_section)


def validation_rows(paths: Mapping[str, Path]) -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    constructors = {row["row_id"]: row for row in rows_from(CONSTRUCTOR_OUTPUT)}
    coeffs = {row["row_id"]: row for row in rows_from(COEFFICIENT_OUTPUT)}
    gates = rows_from(CLAIM_GATES)
    no_claims = not any(row.get("valid_for_claim") == "True" for row in constructors.values()) and not any(row.get("valid_for_claim") == "True" for row in coeffs.values())
    checks = [
        ("VAL4424_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source path exists"),
        ("VAL4424_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited text source needle is present"),
        ("VAL4424_2_core_status", constructors["CEX4424_0_core_MTS_primitives"].get("current_status") == "CONSTRUCTOR_EXHAUSTION_PARTIAL", "core primitive seed is partial only"),
        ("VAL4424_3_atlas_status", constructors["CEX4424_1_parent_generate_atlas"].get("current_status") == "PRIMITIVE_CONSTRUCTOR_ATLAS_READY_EXHAUSTION_OPEN", "ParentGenerate atlas ready but exhaustion open"),
        ("VAL4424_4_Hom_status", constructors["CEX4424_2_Hom_no_slot_if_exhausted"].get("current_status") == "HOM_NO_SLOT_READY_HIDDEN_READOUT_REENTRY_OPEN", "Hom no-slot theorem blocked by re-entry"),
        ("VAL4424_5_future_contract", constructors["CEX4424_4_future_constructor_exhaustion_contract"].get("current_status") == "PARENT_CONSTRUCTOR_EXHAUSTION_CONTRACT_READY_NONCLAIM", "future constructor exhaustion contract executable nonclaim"),
        ("VAL4424_6_slot_missing", coeffs["CPWEP4424_0_slot_import_template"].get("current_status") == "PARENT_COEFFICIENT_VALUE_MISSING_NONCLAIM", "C_parent WEP slot import is missing value"),
        ("VAL4424_7_Cparent_vector_missing", coeffs["CPWEP4424_1_Cparent_vector_verdict"].get("current_status") == "PARENT_COEFFICIENT_VALUE_MISSING_NONCLAIM", "C_parent vector remains not scoreable"),
        ("VAL4424_8_CX_missing", coeffs["CPWEP4424_2_finite_CX_electron_contract"].get("current_status") == "PARENT_COEFFICIENT_VALUE_MISSING_NONCLAIM", "finite C_i contract remains missing"),
        ("VAL4424_9_numeric_component_not_parent", coeffs["CPWEP4424_3_numeric_DeltaQ_alpha_component"].get("current_status") == "NUMERIC_COMPONENT_NOT_PARENT_COEFFICIENT", "numeric DeltaQ component is not a parent coefficient"),
        ("VAL4424_10_no_claim_outputs", no_claims, "no generated row is claim-ready"),
        ("VAL4424_11_claim_gates", any(row["gate_id"] == "CG4424_6_no_claim_outputs" and row["passed"] == "True" for row in gates), "claim gates explicitly block public claim"),
        ("VAL4424_12_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-265"),
        ("VAL4424_13_formal_doc", paths["formal"].exists() and MARKER in text(paths["formal"]), "formal doc exists with marker"),
        ("VAL4424_14_post_doc", paths["post"].exists() and "Private checkpoint" in text(paths["post"]), "post checkpoint doc exists"),
        ("VAL4424_15_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4424_16_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4424_17_next_target", paths["next"].exists() and NEXT_TARGET in text(paths["next"]), "next target file exists"),
        ("VAL4424_18_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": bool(passed), "detail": detail} for check_id, passed, detail in checks]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(DERIVATION_ROWS, derivation_rows())
    write_csv(CONSTRUCTOR_INPUT, constructor_input_rows())
    write_csv(COEFFICIENT_INPUT, coefficient_input_rows())
    write_csv(CONSTRUCTOR_OUTPUT, evaluate_constructor_rows(CONSTRUCTOR_INPUT))
    write_csv(COEFFICIENT_OUTPUT, evaluate_coefficient_rows(COEFFICIENT_INPUT))
    constructor_output = rows_from(CONSTRUCTOR_OUTPUT)
    coefficient_output = rows_from(COEFFICIENT_OUTPUT)
    gates = claim_gate_rows(constructor_output, coefficient_output)
    write_csv(CLAIM_GATES, gates)
    write_csv(DECISION_CSV, decision_rows())
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    write_text(FORMAL_PATH, build_doc(rows_from(SOURCE_REGISTER), constructor_output, coefficient_output, gates))
    write_text(DOC_PATH, post_doc())
    update_claims_register()
    write_spine_and_packet()
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    write_csv(VALIDATION_PATH, validation_rows({"formal": FORMAL_PATH, "post": DOC_PATH, "next": NEXT_CSV}))


if __name__ == "__main__":
    main()

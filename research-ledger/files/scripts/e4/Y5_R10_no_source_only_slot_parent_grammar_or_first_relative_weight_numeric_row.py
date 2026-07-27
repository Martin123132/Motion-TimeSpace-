from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from Y5_R10_alpha_product_prediction_stub_runner_and_required_inputs import (
    BOUND_REQUIRED_COLUMNS,
    PRODUCT_REQUIRED_COLUMNS,
    run_product_runner,
)


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1065-Y5-R10-no-source-only-slot-parent-grammar-or-first-relative-weight-numeric-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1065-no-source-only-slot-parent-grammar" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_TEMPLATE = OUT / "P8_Y5_R10_1065_WEP_RELATIVE_WEIGHT_PRODUCT_CANDIDATE_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1065_WEP_RELATIVE_WEIGHT_BOUND_IMPORT.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |" for row in rows],
        ]
    ) + "\n"


def count_formalization_modified_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED
    )


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1065_0_1064_next", "source-intake/mts_residuals/P8_Y5_R10_1064_NEXT_TARGET.csv", "1065-Y5-R10-no-source-only-slot-parent-grammar", "1064 handoff."),
        ("SRC1065_1_1064_proof", "source-intake/mts_residuals/P8_Y5_R10_1064_LABEL_FORGETTING_PROOF_ATTEMPT.csv", "PLF1064_5_verdict", "1064 label-forgetting verdict."),
        ("SRC1065_2_1064_slot", "source-intake/mts_residuals/P8_Y5_R10_1064_NO_SOURCE_ONLY_SLOT_AUDIT.csv", "NSS1064_2_relative_weight", "live w_A slot."),
        ("SRC1065_3_1064_req", "source-intake/mts_residuals/P8_Y5_R10_1064_NUMERIC_SOURCE_REQUIREMENTS.csv", "REQ1064_0_WEP_species", "first WEP requirement."),
        ("SRC1065_4_1064_guard", "source-intake/mts_residuals/P8_Y5_R10_1064_COMMON_MODE_GUARD.csv", "CMG1064_0_common_absorption", "measured-G common-mode guard."),
        ("SRC1065_5_1064_template", "source-intake/mts_residuals/P8_Y5_R10_1064_RELATIVE_WEIGHT_PRODUCT_TEMPLATE_NONCLAIM.csv", "PRED1064_0_WEP_relative_source_weight", "relative-weight product template."),
        ("SRC1065_6_1064_bound", "source-intake/mts_residuals/P8_Y5_R10_1064_RELATIVE_WEIGHT_BOUND_IMPORT.csv", "BOUND1064_0_WEP_source_charge", "WEP source-charge bound anchor."),
        ("SRC1065_7_1063_theorem", "source-intake/mts_residuals/P8_Y5_R10_1063_SOURCE_FORGETTING_THEOREM_ATTEMPT.csv", "THM1063_5_verdict", "source-label forgetting theorem attempt."),
        ("SRC1065_8_1062_parent", "source-intake/mts_residuals/P8_Y5_R10_1062_PARENT_PRODUCT_THEOREM_ATTEMPT.csv", "THM1062_3_source_label_forgetting", "parent WEP product theorem attempt."),
        ("SRC1065_9_1062_counter", "source-intake/mts_residuals/P8_Y5_R10_1062_COUNTEREXAMPLE_SURVIVAL_LEDGER.csv", "CE1062_1_relative_source_weight", "relative source-weight counterexample."),
        ("SRC1065_10_954_clause", "source-intake/mts_residuals/P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv", "PAC954_1_no_source_prefactors", "parent action no-prefactor clause."),
        ("SRC1065_11_955_class", "source-intake/mts_residuals/P8_Y5_R10_955_SOURCE_PREFACTOR_CLASSIFICATION.csv", "SPC955_2_relative_species_weight", "source prefactor class."),
        ("SRC1065_12_956_spine", "source-intake/mts_residuals/P8_Y5_R10_956_SOURCE_SIDE_GR_NEWTON_SPINE.csv", "SSG956_3_minimal_matter_action", "source-side GR/Newton spine."),
        ("SRC1065_13_1061_input", "source-intake/mts_residuals/P8_Y5_R10_1061_INPUT_FILL_LEDGER.csv", "INF1061_4_tau_WEP", "tau_WEP missing row."),
        ("SRC1065_14_1061_material", "source-intake/mts_residuals/P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv", "MCON1061_2_eta_bound", "WEP material and eta convention."),
        ("SRC1065_15_local_bounds", "source-intake/local_bounds/local_bound_claims.csv", "R1_WEP_source_charge", "local WEP bound source."),
        ("SRC1065_16_393_common_mode", "393-source-normalized-Newtonian-limit-under-identity-closure.md", "Only a constant, universal, range-independent", "common-mode measured-G guard."),
    ]
    rows: list[dict[str, str]] = []
    for source_id, relative_path, needle, note in specs:
        path = source_path(relative_path)
        exists = path.exists()
        needle_found = exists and needle in read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "relative_path": relative_path,
                "absolute_path": str(path),
                "exists": str(exists).lower(),
                "needle": needle,
                "needle_found": str(needle_found).lower(),
                "note": note,
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def parent_grammar_audit_rows() -> list[dict[str, str]]:
    return [
        {
            "audit_id": "PGG1065_0_parent_language",
            "claim": "define the parent matter action language before source coupling",
            "formal_clause": "S_matter is a local functional of e_obs, Psi_A, connections, and measured matter parameters theta_A",
            "test": "all slots affect matter dynamics, observed currents, representation data, or universal geometry",
            "result": "CONDITIONAL_GRAMMAR_CANDIDATE",
            "gap": "the corpus has not yet made this object language a parent theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "PGG1065_1_no_inert_species_scalar",
            "claim": "forbid a dimensionless inert scalar w_A that only multiplies active source strength",
            "formal_clause": "w_A not in Obj(Language) if delta w_A changes T_source but no nongravitational observable or representation label",
            "test": "partial S_matter / partial w_A is undefined rather than set to zero by hand",
            "result": "EXACT_IF_PARENT_SYNTAX_ACCEPTED",
            "gap": "this is the desired grammar rule, not yet derived from deeper MTS quotient/category primitives",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "PGG1065_2_field_normalization_quotient",
            "claim": "classify apparent w_A as field normalization when possible",
            "formal_clause": "Psi_A -> Z_A^{1/2} Psi_A with canonical kinetic term and transformed measured couplings",
            "test": "after quotienting by field redefinition, no independent source-only coefficient remains",
            "result": "LOOPHOLE_AUDITED_NOT_CLOSED",
            "gap": "interaction terms, path-integral normalization, and composite matter conventions are not parent-owned",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "PGG1065_3_charge_interaction_owner",
            "claim": "source normalization cannot hide inside charge/current normalization",
            "formal_clause": "q_A, m_A, representation data, and J_A normalizations are measured matter-sector parameters",
            "test": "a coefficient that changes interactions is observable; a coefficient that only changes gravity is w_A and prohibited",
            "result": "OWNER_CONDITIONAL",
            "gap": "Noether/current owner remains candidate-missing in the 1063 chain",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "PGG1065_4_measure_coframe_descent",
            "claim": "prevent measure/coframe factors from reintroducing species labels",
            "formal_clause": "sqrt(-g_obs), e_obs, connection descent, and boundary terms are species blind through local limit",
            "test": "no species-dependent Jacobian, frame factor, or boundary selector multiplies only the Hilbert source",
            "result": "PARALLEL_PARENT_SIGNATURE_MISSING",
            "gap": "measure/coframe/hidden-spurion return was named earlier but not parent signed",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "PGG1065_5_verdict",
            "claim": "no-source-only-slot parent grammar theorem",
            "formal_clause": "Language(S_matter) excludes w_A; common w is calibration; all relative weights are either measured matter parameters or forbidden spurions",
            "test": "if accepted, Delta_w_AB=0 theorem-zero and WEP relative-source row closes without numeric prior",
            "result": "CONDITIONAL_GRAMMAR_NOT_PARENT_SIGNED",
            "gap": "still no derivation that the parent category object language must exclude inert species scalars",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def allowed_action_grammar_rows() -> list[dict[str, str]]:
    return [
        {
            "grammar_id": "AAG1065_0_observed_geometry",
            "slot": "observed coframe/metric",
            "allowed_status": "allowed",
            "grammar_rule": "one e_obs/g_obs supplies matter dynamics, Hilbert variation, clocks, photons, and readout",
            "source_effect": "species-blind source geometry",
            "signature_status": "conditional_from_956",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "grammar_id": "AAG1065_1_matter_fields",
            "slot": "ordinary matter fields Psi_A",
            "allowed_status": "allowed",
            "grammar_rule": "fields may carry representation labels and measured charges/masses",
            "source_effect": "Hilbert stress is varied from the same matter action",
            "signature_status": "ordinary_matter_language_allowed",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "grammar_id": "AAG1065_2_measured_parameters",
            "slot": "theta_A measured matter parameters",
            "allowed_status": "allowed_if_observable",
            "grammar_rule": "masses, charges, representation data, and interaction coefficients must be readout-measurable",
            "source_effect": "not a hidden gravitational source prefactor",
            "signature_status": "requires Noether/current owner for full closure",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "grammar_id": "AAG1065_3_common_normalization",
            "slot": "w_common",
            "allowed_status": "calibration_only",
            "grammar_rule": "single universal constant multiplier can be absorbed into kappa/G only if range/time/species/frame independent",
            "source_effect": "common-mode, not WEP-sensitive",
            "signature_status": "guarded_by_393_and_1064",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "grammar_id": "AAG1065_4_source_only_species_scalar",
            "slot": "w_A",
            "allowed_status": "prohibited_by_candidate_grammar",
            "grammar_rule": "no inert dimensionless species scalar may multiply S_A while remaining invisible to nongravitational readout",
            "source_effect": "would create T_source=sum_A w_A T_A",
            "signature_status": "not_parent_signed",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "grammar_id": "AAG1065_5_hidden_spurion",
            "slot": "w(m,D,boundary,A)",
            "allowed_status": "prohibited_or_retained_residual",
            "grammar_rule": "marker, domain, boundary, and post-readout masks cannot reweight source after variation",
            "source_effect": "reopens species labels after apparent source forgetting",
            "signature_status": "parallel_open_gate",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "grammar_id": "AAG1065_6_nonHilbert_current",
            "slot": "zeta_A J_NH,A",
            "allowed_status": "absent_exact_silent_or_residual",
            "grammar_rule": "spin/torsion/boundary/non-Hilbert current must be proved silent or bounded separately",
            "source_effect": "could bypass Hilbert source uniqueness",
            "signature_status": "parallel_open_gate",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def field_normalization_rows() -> list[dict[str, str]]:
    return [
        {
            "loophole_id": "FNL1065_0_free_field_rescaling",
            "possible_escape": "w_A is only a field normalization",
            "audit_result": "not enough by itself",
            "reason": "canonical kinetic normalization can remove one factor, but interactions and composite observables fix relative normalizations",
            "required_closure": "field-redefinition quotient plus all measured couplings transformed with no leftover source-only factor",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "loophole_id": "FNL1065_1_action_scale_quantum_weight",
            "possible_escape": "overall S_A multiplier is dynamically invisible classically",
            "audit_result": "dangerous_counterexample",
            "reason": "classical EOM may be unchanged while Hilbert stress and path-integral/statistical weight change",
            "required_closure": "parent quantum/statistical action normalization or theorem that such multipliers are gauge quotiented",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "loophole_id": "FNL1065_2_mass_unit_convention",
            "possible_escape": "w_A is mass renormalization or unit choice",
            "audit_result": "not source-only if observable",
            "reason": "if it changes inertial mass or spectra, it belongs to theta_A and is not a hidden gravitational prefactor",
            "required_closure": "same parameter must enter dynamics, source, and readout through one owner",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "loophole_id": "FNL1065_3_measure_jacobian",
            "possible_escape": "species-dependent measure/coframe Jacobian",
            "audit_result": "parallel_spurion_channel",
            "reason": "a Jacobian can multiply variation without appearing as explicit w_A",
            "required_closure": "species-blind measure/coframe descent and boundary silence",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "loophole_id": "FNL1065_4_verdict",
            "possible_escape": "all w_A are normalization artifacts",
            "audit_result": "NOT_PROVED",
            "reason": "some apparent weights may be quotiented, but an inert source-only scalar is still legal unless the parent grammar forbids it",
            "required_closure": "parent action syntax exclusion or numeric WEP prior row",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def charge_interaction_rows() -> list[dict[str, str]]:
    return [
        {
            "audit_id": "CIN1065_0_charge_is_observable",
            "object": "electric/gauge charge q_A",
            "result": "not a hidden source prefactor",
            "reason": "charge enters interactions and currents, so it is measured matter data rather than a pure gravitational source weight",
            "closure_needed": "current normalization and representation owner",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "CIN1065_1_neutral_rest_source",
            "object": "neutral/rest-mass source contribution",
            "result": "blocks charge-only escape",
            "reason": "source weight must apply to all stress-energy, not only EM charge channels",
            "closure_needed": "Hilbert source owner for total stress tensor",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "CIN1065_2_current_owner",
            "object": "Noether/current normalization",
            "result": "candidate_missing",
            "reason": "1063 still marks the owner as not derived, so current normalization cannot yet force w_A absent",
            "closure_needed": "single parent current owner for charge, matter, and source readout",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "CIN1065_3_interaction_renormalization",
            "object": "coupling and charge renormalization",
            "result": "loophole_not_closed",
            "reason": "renormalized interactions can hide normalization choices unless the parent identifies which constants are measured",
            "closure_needed": "operator-domain rule separating measured constants from source-only scalars",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "CIN1065_4_verdict",
            "object": "interaction/charge normalization route to no w_A",
            "result": "CONDITIONAL_NOT_PARENT_SIGNED",
            "reason": "it supplies a good classification but not a proof that inert source-only scalars cannot exist",
            "closure_needed": "parent current owner or explicit source-scalar exclusion theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def theorem_zero_rows() -> list[dict[str, str]]:
    return [
        {
            "zero_id": "WTZ1065_0_strict_no_slot",
            "target_quantity": "Delta_w_AB",
            "theorem_clause": "w_A is not a syntactic object in the parent matter action language",
            "would_imply": "Delta_w_AB = 0 for all material/source pairs",
            "current_status": "exact_clause_not_parent_signed",
            "blocks": "cannot score WEP relative-source row as theorem-zero",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "zero_id": "WTZ1065_1_common_mode_only",
            "target_quantity": "Delta_w_AB",
            "theorem_clause": "w_A = w_common for every species/source and w_common is constant/range/time/frame independent",
            "would_imply": "Delta_w_AB = 0 after common calibration",
            "current_status": "common_mode_guarded_not_proved",
            "blocks": "relative weights cannot be absorbed into measured G",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "zero_id": "WTZ1065_2_field_redefinition",
            "target_quantity": "Delta_w_AB",
            "theorem_clause": "all apparent w_A are field normalizations removed by canonical quotient with interactions preserved",
            "would_imply": "no residual source-only product",
            "current_status": "normalization_loophole_audited_not_closed",
            "blocks": "path-integral/action-scale counterexample survives",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "zero_id": "WTZ1065_3_current_owner",
            "target_quantity": "Delta_w_AB",
            "theorem_clause": "one parent current/source owner fixes matter dynamics, Noether currents, and Hilbert source normalization",
            "would_imply": "source label has no independent coupling selector",
            "current_status": "owner_candidate_missing",
            "blocks": "relative source weights remain finite-branch debts",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "zero_id": "WTZ1065_4_verdict",
            "target_quantity": "P_WEP_relative_source_weight",
            "theorem_clause": "Delta_w_AB=0 OR tau_WEP=0 from parent-signed grammar/projection",
            "would_imply": "P_WEP_relative_source_weight=0",
            "current_status": "THEOREM_ZERO_NOT_PARENT_SIGNED",
            "blocks": "first WEP numeric row must remain nonclaim/missing-input",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def first_wep_numeric_schema_rows() -> list[dict[str, str]]:
    return [
        {
            "row_id": "WEP1065_0_bound_anchor",
            "quantity": "eta_AB source-charge bound",
            "symbol": "eta_TiPt_bound",
            "value_or_status": "2.8e-15",
            "units": "dimensionless",
            "source_path": "source-intake/local_bounds/local_bound_claims.csv",
            "source_row": "R1_WEP_source_charge",
            "runner_role": "bound",
            "refusal_gate": "bound alone is not an MTS prediction",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "WEP1065_1_material_pair",
            "quantity": "MICROSCOPE Ti/Pt material convention",
            "symbol": "AB",
            "value_or_status": "TA6V_minus_PtRh10",
            "units": "dimensionless convention",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv",
            "source_row": "MCON1061_0_test_pair",
            "runner_role": "context",
            "refusal_gate": "material convention does not supply Delta_w_AB",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "WEP1065_2_delta_w",
            "quantity": "relative source-weight difference for Ti/Pt",
            "symbol": "Delta_w_TiPt",
            "value_or_status": "MISSING_PARENT_GRAMMAR_ZERO_OR_NUMERIC_PRIOR",
            "units": "dimensionless",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1065_WA_THEOREM_ZERO_CLAUSES.csv",
            "source_row": "WTZ1065_4_verdict",
            "runner_role": "required_prediction_input",
            "refusal_gate": "no unity shortcut and no absorption into measured G",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "WEP1065_3_tau_WEP",
            "quantity": "local lab/source/orbit/readout projection",
            "symbol": "tau_WEP",
            "value_or_status": "MISSING_LAB_SOURCE_ORBIT_PROJECTION",
            "units": "dimensionless",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1061_INPUT_FILL_LEDGER.csv",
            "source_row": "INF1061_4_tau_WEP",
            "runner_role": "required_prediction_input",
            "refusal_gate": "tau_WEP cannot be set to one",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "WEP1065_4_product",
            "quantity": "first scoreable WEP relative source product",
            "symbol": "P_WEP_relative_source_weight = abs(Delta_w_TiPt * tau_WEP)",
            "value_or_status": "MISSING_DELTA_W_TiPt_TIMES_TAU_WEP_PRODUCT",
            "units": "dimensionless",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1065_FIRST_WEP_NUMERIC_ROW_SCHEMA.csv",
            "source_row": "WEP1065_2_delta_w; WEP1065_3_tau_WEP",
            "runner_role": "prediction",
            "refusal_gate": "must be numeric, sourced, unit-matched, and <= 2.8e-15",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "WEP1065_5_no_cancellation",
            "quantity": "absolute-value no-cancellation guard",
            "symbol": "abs(Delta_w_TiPt * tau_WEP)",
            "value_or_status": "ENFORCED_AS_SCHEMA",
            "units": "dimensionless",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1065_FIRST_WEP_NUMERIC_ROW_SCHEMA.csv",
            "source_row": "WEP1065_4_product",
            "runner_role": "guard",
            "refusal_gate": "no signed-material cancellation accepted as evidence",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1065_0_WEP_relative_source_weight_first_row",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_DELTA_W_TiPt_TIMES_TAU_WEP_PRODUCT",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1065_FIRST_WEP_NUMERIC_ROW_SCHEMA.csv",
            "inputs_present": "eta_TiPt_bound=2.8e-15;material_pair=TA6V_minus_PtRh10",
            "required_inputs": "Delta_w_TiPt theorem-zero or numeric prior;tau_WEP local projection;absolute product;source paths",
            "derivation_status": "MISSING_NUMERIC_OR_THEOREM_ZERO_RELATIVE_WEIGHT",
            "valid_for_claim": "false",
            "notes": "The first WEP row is now structurally defined, but it is not a prediction until Delta_w_TiPt and tau_WEP are derived or sourced.",
        }
    ]


def bound_rows() -> list[dict[str, str]]:
    return [
        {
            "bound_id": "BOUND1065_0_WEP_source_charge",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "bound_value": "2.8e-15",
            "bound_units": "dimensionless",
            "bound_source": "source-intake/local_bounds/local_bound_claims.csv",
            "source_row": "R1_WEP_source_charge",
            "bound_type": "numeric_bound_anchor_nonclaim",
            "valid_for_claim": "true",
            "notes": "Source-backed WEP anchor; it does not create an MTS prediction without a numeric product row.",
        }
    ]


def product_status_rows(status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "runner_id": "APR1065_0_WEP_relative_weight_first_row",
            "prediction_rows": str(status.get("prediction_rows", "")),
            "bound_rows": str(status.get("bound_rows", "")),
            "valid_prediction_rows": str(status.get("valid_prediction_rows", "")),
            "valid_bound_rows": str(status.get("valid_bound_rows", "")),
            "comparison_rows": str(status.get("comparison_rows", "")),
            "passed_rows": str(status.get("passed_rows", "")),
            "blocked_or_failed_rows": str(status.get("blocked_or_failed_rows", "")),
            "claim_allowed": str(status.get("claim_allowed", "")).lower(),
            "generated_utc": stamp(),
        }
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1065_0_parent_grammar_theorem",
            "claim": "parent action grammar forbids source-only species scalar w_A",
            "gate_pass": "false",
            "reason": "candidate grammar is exact but not parent signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1065_1_theorem_zero_Delta_w",
            "claim": "Delta_w_TiPt=0 by theorem",
            "gate_pass": "false",
            "reason": "no-source-only-slot theorem zero clauses remain unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1065_2_first_WEP_numeric_row",
            "claim": "first WEP relative-weight row is scoreable",
            "gate_pass": "false",
            "reason": "Delta_w_TiPt and tau_WEP are missing; product runner has valid_prediction_rows=0",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1065_3_measured_G_absorption",
            "claim": "relative source weights can be absorbed into measured G",
            "gate_pass": "false",
            "reason": "only common universal range/time/species/frame independent factors are absorbable",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1065_4_local_GR_WEP_claim",
            "claim": "local GR/WEP source coupling branch is derived",
            "gate_pass": "false",
            "reason": "right source-side structure is isolated, but the grammar/current/projection signatures remain open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1065_0_grammar_status",
            "decision": "no-source-only-slot grammar is the right theorem target but not closed",
            "because": "the grammar cleanly kills w_A if accepted, but acceptance is still a parent syntax axiom/contract",
            "next_action": "derive the source-scalar exclusion from parent object language or operator-domain rules",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1065_1_first_WEP_row_status",
            "decision": "first WEP relative-source row is now schema-complete but numerically empty",
            "because": "eta bound and material convention exist, while Delta_w_TiPt and tau_WEP are missing",
            "next_action": "either prove Delta_w_TiPt=0 or source a numeric prior width plus tau_WEP projection",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1065_2_best_next",
            "decision": "next target is parent source-scalar exclusion or WEP Delta-w prior width",
            "because": "this is now the smallest remaining fork between a derivation win and a bounded finite branch",
            "next_action": "1066-Y5-R10-parent-action-syntax-source-scalar-exclusion-or-WEP-Delta-w-prior-width.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1066-Y5-R10-parent-action-syntax-source-scalar-exclusion-or-WEP-Delta-w-prior-width.md",
            "objective": "derive the parent action syntax/operator-domain rule that excludes inert source-only species scalars; if it fails, fill the WEP Delta_w_TiPt prior-width row and tau_WEP projection requirements without claiming a pass.",
            "include": "source-scalar exclusion lemma, object-language typing, field/measure normalization, quantum action-scale issue, WEP Delta_w_TiPt prior-width schema, tau_WEP projection contract",
            "exclude": "assuming minimality, setting Delta_w=0 by taste, setting tau_WEP=1, absorbing relative weights into measured G, public WEP/local-GR claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def validate_outputs(
    outputs: dict[str, Path],
    sources: list[dict[str, str]],
    grammar_audit: list[dict[str, str]],
    allowed_grammar: list[dict[str, str]],
    field_loopholes: list[dict[str, str]],
    charge_audit: list[dict[str, str]],
    theorem_zero: list[dict[str, str]],
    wep_schema: list[dict[str, str]],
    predictions: list[dict[str, str]],
    bounds: list[dict[str, str]],
    product_status: dict[str, Any],
    claims: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []

    def add(check_id: str, condition: bool, detail: str) -> None:
        checks.append(
            {
                "check_id": check_id,
                "result": "pass" if condition else "fail",
                "detail": detail,
                "generated_utc": stamp(),
            }
        )

    add(
        "V1065_1_sources_exist_and_needles",
        all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources),
        "every cited source path exists and every source needle was found",
    )
    add(
        "V1065_2_grammar_not_promoted",
        any(row["audit_id"] == "PGG1065_5_verdict" and row["result"] == "CONDITIONAL_GRAMMAR_NOT_PARENT_SIGNED" for row in grammar_audit),
        "parent grammar theorem remains conditional",
    )
    add(
        "V1065_3_allowed_slots_written",
        len(allowed_grammar) >= 7 and any(row["grammar_id"] == "AAG1065_4_source_only_species_scalar" and row["allowed_status"].startswith("prohibited") for row in allowed_grammar),
        "allowed/prohibited action grammar slots are recorded",
    )
    add(
        "V1065_4_loopholes_audited",
        len(field_loopholes) >= 5 and len(charge_audit) >= 5,
        "field normalization and charge/current loopholes are audited",
    )
    add(
        "V1065_5_theorem_zero_unsigned",
        any(row["zero_id"] == "WTZ1065_4_verdict" and row["current_status"] == "THEOREM_ZERO_NOT_PARENT_SIGNED" for row in theorem_zero),
        "w_A theorem-zero is not promoted",
    )
    add(
        "V1065_6_first_WEP_schema_written",
        len(wep_schema) >= 6
        and any(row["row_id"] == "WEP1065_2_delta_w" and "MISSING" in row["value_or_status"] for row in wep_schema)
        and any(row["row_id"] == "WEP1065_3_tau_WEP" and "MISSING" in row["value_or_status"] for row in wep_schema),
        "first WEP row has bound, material context, Delta_w, tau_WEP, product, and no-cancellation guard",
    )
    add(
        "V1065_7_prediction_template_nonclaim",
        len(predictions) == 1 and "MISSING" in predictions[0]["product_value"] and predictions[0]["valid_for_claim"] == "false",
        "first WEP prediction row remains missing-input/nonclaim",
    )
    bound_numeric = False
    try:
        bound_numeric = float(bounds[0]["bound_value"]) > 0
    except (IndexError, KeyError, ValueError):
        bound_numeric = False
    add(
        "V1065_8_bound_anchor_numeric",
        len(bounds) == 1 and bound_numeric and bounds[0]["valid_for_claim"] == "true",
        "WEP bound anchor is numeric and source-backed",
    )
    add(
        "V1065_9_runner_refuses_missing_prediction",
        product_status.get("valid_prediction_rows") == 0 and product_status.get("claim_allowed") is False,
        "strict product runner refuses the first WEP placeholder",
    )
    add(
        "V1065_10_claim_gates_blocked",
        bool(claims) and all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claims),
        "all grammar/WEP/local-GR claim gates remain blocked",
    )
    add(
        "V1065_11_next_target_written",
        bool(next_rows) and next_rows[0]["next_target"].startswith("1066-Y5-R10-parent-action-syntax-source-scalar-exclusion"),
        "next target selects source-scalar exclusion or WEP Delta-w prior-width",
    )
    generated_inside = all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in outputs.values())
    add(
        "V1065_12_generated_files_in_post_checkpoint",
        generated_inside,
        "all generated files are under post-checkpoint-work",
    )
    formalization_count = count_formalization_modified_since_start()
    add(
        "V1065_13_formalization_untouched",
        formalization_count == 0,
        f"formalization-workbench modified-file count since script start is {formalization_count}",
    )
    summary_pass = all(row["result"] == "pass" for row in checks)
    checks.insert(
        0,
        {
            "check_id": "V1065_SUMMARY",
            "result": "pass" if summary_pass else "fail",
            "detail": "1065 parent grammar / first WEP relative-weight row validation summary",
            "generated_utc": stamp(),
        },
    )
    return checks


def write_doc(
    sources: list[dict[str, str]],
    grammar_audit: list[dict[str, str]],
    allowed_grammar: list[dict[str, str]],
    field_loopholes: list[dict[str, str]],
    charge_audit: list[dict[str, str]],
    theorem_zero: list[dict[str, str]],
    wep_schema: list[dict[str, str]],
    predictions: list[dict[str, str]],
    bounds: list[dict[str, str]],
    product_status_rows_: list[dict[str, str]],
    product_comparisons: list[dict[str, Any]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1065 — No-Source-Only-Slot Parent Grammar Or First Relative-Weight Numeric Row",
            "",
            "**Current verdict:** the candidate grammar is sharp: if the parent matter language has no inert species scalar `w_A`, then `Delta_w_AB=0` follows. But that language rule is still not parent-derived, so no WEP/local-GR claim is allowed.",
            "",
            "**Runner result:** the first WEP relative-source row is schema-complete, but `Delta_w_TiPt` and `tau_WEP` are missing; the strict product runner therefore keeps `valid_prediction_rows=0`.",
            "",
            "**Coupling discipline:** measured `G` absorbs only a common universal range/time/species/frame independent normalization. A relative `w_A/w_B` is a physical WEP residual unless the parent grammar forbids it.",
            "",
            "## Parent Grammar Audit",
            md_table(grammar_audit, ["audit_id", "claim", "formal_clause", "result", "gap", "valid_for_claim"]),
            "",
            "## Allowed Action Grammar",
            md_table(allowed_grammar, ["grammar_id", "slot", "allowed_status", "grammar_rule", "signature_status", "valid_for_claim"]),
            "",
            "## Field Normalization Loopholes",
            md_table(field_loopholes, ["loophole_id", "possible_escape", "audit_result", "reason", "required_closure", "valid_for_claim"]),
            "",
            "## Charge And Interaction Normalization",
            md_table(charge_audit, ["audit_id", "object", "result", "reason", "closure_needed", "valid_for_claim"]),
            "",
            "## w_A Theorem-Zero Clauses",
            md_table(theorem_zero, ["zero_id", "target_quantity", "theorem_clause", "would_imply", "current_status", "blocks", "valid_for_claim"]),
            "",
            "## First WEP Numeric Row Schema",
            md_table(wep_schema, ["row_id", "quantity", "symbol", "value_or_status", "units", "source_row", "runner_role", "refusal_gate", "valid_for_claim"]),
            "",
            "## WEP Product Runner",
            md_table(predictions, PRODUCT_REQUIRED_COLUMNS),
            "",
            "## WEP Bound Import",
            md_table(bounds, BOUND_REQUIRED_COLUMNS),
            "",
            "## Runner Status",
            md_table(product_status_rows_, ["runner_id", "prediction_rows", "bound_rows", "valid_prediction_rows", "valid_bound_rows", "comparison_rows", "passed_rows", "blocked_or_failed_rows", "claim_allowed", "generated_utc"]),
            "",
            "## Runner Comparisons",
            md_table(product_comparisons, ["comparison_id", "arena", "product_symbol", "product_value", "bound_value", "comparison_status", "pass_for_claim", "issues"]),
            "",
            "## Claim Gates",
            md_table(claims, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "",
            "## Decisions",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "",
            "## Source Register",
            md_table(sources, ["source_id", "relative_path", "exists", "needle", "needle_found", "valid_for_claim"]),
            "",
            "## Validation",
            md_table(validation, ["check_id", "result", "detail", "generated_utc"]),
            "",
            "## Next Target",
            md_table(next_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    grammar_audit = parent_grammar_audit_rows()
    allowed_grammar = allowed_action_grammar_rows()
    field_loopholes = field_normalization_rows()
    charge_audit = charge_interaction_rows()
    theorem_zero = theorem_zero_rows()
    wep_schema = first_wep_numeric_schema_rows()
    predictions = prediction_rows()
    bounds = bound_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    outputs: dict[str, Path] = {
        "source_register": OUT / "P8_Y5_R10_1065_SOURCE_REGISTER.csv",
        "grammar_audit": OUT / "P8_Y5_R10_1065_PARENT_GRAMMAR_AUDIT.csv",
        "allowed_grammar": OUT / "P8_Y5_R10_1065_ALLOWED_ACTION_GRAMMAR.csv",
        "field_loopholes": OUT / "P8_Y5_R10_1065_FIELD_NORMALIZATION_LOOPHOLE_AUDIT.csv",
        "charge_audit": OUT / "P8_Y5_R10_1065_CHARGE_INTERACTION_NORMALIZATION_AUDIT.csv",
        "theorem_zero": OUT / "P8_Y5_R10_1065_WA_THEOREM_ZERO_CLAUSES.csv",
        "wep_schema": OUT / "P8_Y5_R10_1065_FIRST_WEP_NUMERIC_ROW_SCHEMA.csv",
        "predictions": PREDICTION_TEMPLATE,
        "bounds": BOUND_IMPORT,
        "product_status": OUT / "P8_Y5_R10_1065_PRODUCT_RUNNER_STATUS.csv",
        "product_comparison": OUT / "P8_Y5_R10_1065_PRODUCT_COMPARISON_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_R10_1065_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1065_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1065_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1065_VALIDATION.csv",
        "doc": DOC,
    }

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["grammar_audit"], grammar_audit)
    write_csv(outputs["allowed_grammar"], allowed_grammar)
    write_csv(outputs["field_loopholes"], field_loopholes)
    write_csv(outputs["charge_audit"], charge_audit)
    write_csv(outputs["theorem_zero"], theorem_zero)
    write_csv(outputs["wep_schema"], wep_schema)
    write_csv(outputs["predictions"], predictions, PRODUCT_REQUIRED_COLUMNS)
    write_csv(outputs["bounds"], bounds, BOUND_REQUIRED_COLUMNS)
    write_csv(outputs["claim_gates"], claims)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next_target"], next_rows)

    product_result = run_product_runner(PREDICTION_TEMPLATE, BOUND_IMPORT, PRODUCT_RUN_DIR)
    product_status = product_result["status"]
    product_status_rows_ = product_status_rows(product_status)
    write_csv(outputs["product_status"], product_status_rows_)
    write_csv(outputs["product_comparison"], product_result["comparisons"])

    validation = validate_outputs(
        outputs,
        sources,
        grammar_audit,
        allowed_grammar,
        field_loopholes,
        charge_audit,
        theorem_zero,
        wep_schema,
        predictions,
        bounds,
        product_status,
        claims,
        next_rows,
    )
    write_csv(outputs["validation"], validation)
    write_doc(
        sources,
        grammar_audit,
        allowed_grammar,
        field_loopholes,
        charge_audit,
        theorem_zero,
        wep_schema,
        predictions,
        bounds,
        product_status_rows_,
        product_result["comparisons"],
        claims,
        decisions,
        validation,
        next_rows,
    )

    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()

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
DOC = ROOT / "1066-Y5-R10-parent-action-syntax-source-scalar-exclusion-or-WEP-Delta-w-prior-width.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1066-parent-action-syntax-source-scalar-exclusion" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_TEMPLATE = OUT / "P8_Y5_R10_1066_WEP_DELTA_W_PRODUCT_CANDIDATE_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1066_WEP_DELTA_W_BOUND_IMPORT.csv"


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
        ("SRC1066_0_1065_next", "source-intake/mts_residuals/P8_Y5_R10_1065_NEXT_TARGET.csv", "1066-Y5-R10-parent-action-syntax-source-scalar-exclusion", "1065 handoff."),
        ("SRC1066_1_1065_grammar", "source-intake/mts_residuals/P8_Y5_R10_1065_PARENT_GRAMMAR_AUDIT.csv", "PGG1065_5_verdict", "1065 parent grammar verdict."),
        ("SRC1066_2_1065_allowed", "source-intake/mts_residuals/P8_Y5_R10_1065_ALLOWED_ACTION_GRAMMAR.csv", "AAG1065_4_source_only_species_scalar", "candidate prohibited w_A slot."),
        ("SRC1066_3_1065_field", "source-intake/mts_residuals/P8_Y5_R10_1065_FIELD_NORMALIZATION_LOOPHOLE_AUDIT.csv", "FNL1065_1_action_scale_quantum_weight", "action-scale loophole."),
        ("SRC1066_4_1065_charge", "source-intake/mts_residuals/P8_Y5_R10_1065_CHARGE_INTERACTION_NORMALIZATION_AUDIT.csv", "CIN1065_2_current_owner", "current owner still missing."),
        ("SRC1066_5_1065_zero", "source-intake/mts_residuals/P8_Y5_R10_1065_WA_THEOREM_ZERO_CLAUSES.csv", "WTZ1065_4_verdict", "w_A theorem-zero not signed."),
        ("SRC1066_6_1065_wep", "source-intake/mts_residuals/P8_Y5_R10_1065_FIRST_WEP_NUMERIC_ROW_SCHEMA.csv", "WEP1065_2_delta_w", "first WEP Delta_w schema."),
        ("SRC1066_7_1065_product", "source-intake/mts_residuals/P8_Y5_R10_1065_WEP_RELATIVE_WEIGHT_PRODUCT_CANDIDATE_NONCLAIM.csv", "PRED1065_0_WEP_relative_source_weight_first_row", "prior WEP product placeholder."),
        ("SRC1066_8_1055_parent", "source-intake/mts_residuals/P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv", "PAC1055_4_source_label_forgetting", "parent action source-label forgetting."),
        ("SRC1066_9_1055_counter", "source-intake/mts_residuals/P8_Y5_R10_1055_COUNTEREXAMPLE_LEDGER.csv", "CE1055_3_relative_source_weight", "relative source-weight counterexample."),
        ("SRC1066_10_980_theorem", "source-intake/mts_residuals/P8_Y5_R10_980_NO_MARKER_FUNCTOR_THEOREM_ATTEMPT.csv", "NMF980_2_scalar_obstruction_lemma", "continuous target obstruction."),
        ("SRC1066_11_980_counter", "source-intake/mts_residuals/P8_Y5_R10_980_COUNTEREXAMPLE_LEDGER.csv", "CEX980_2_species_kappa", "species kappa counterexample."),
        ("SRC1066_12_989_owner", "source-intake/mts_residuals/P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv", "ELA989_2_current_owner", "Noether/current owner audit."),
        ("SRC1066_13_1061_tau", "source-intake/mts_residuals/P8_Y5_R10_1061_INPUT_FILL_LEDGER.csv", "INF1061_4_tau_WEP", "tau_WEP missing input."),
        ("SRC1066_14_1061_material", "source-intake/mts_residuals/P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv", "MCON1061_0_test_pair", "MICROSCOPE material convention."),
        ("SRC1066_15_local_bounds", "source-intake/local_bounds/local_bound_claims.csv", "R1_WEP_source_charge", "WEP bound source."),
        ("SRC1066_16_393_common", "393-source-normalized-Newtonian-limit-under-identity-closure.md", "Only a constant, universal, range-independent", "measured-G common-mode guard."),
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


def source_scalar_exclusion_rows() -> list[dict[str, str]]:
    return [
        {
            "lemma_id": "SSE1066_0_target",
            "claim": "exclude inert source-only species scalars from the parent action syntax",
            "formal_statement": "If a scalar x_A changes only active gravitational source strength and has no observable/gauge/representation/geometry type, then x_A is not an admissible parent argument.",
            "attempt_result": "TARGET_SHARPENED",
            "gap": "typing principle must be parent-derived rather than adopted as minimality",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "lemma_id": "SSE1066_1_object_language_route",
            "claim": "typed parent arguments are geometry, matter fields, gauge/current data, representation constants, or universal constants",
            "formal_statement": "Arg(S_parent) subset Gamma(E_geom) union Gamma(E_matter) union Conn union Theta_meas union Theta_univ.",
            "attempt_result": "CONDITIONAL_TYPING_LEMMA",
            "gap": "the exact parent object language is not yet derived from deeper MTS primitives",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "lemma_id": "SSE1066_2_variation_before_readout",
            "claim": "post-variation source selectors cannot generate species weights",
            "formal_statement": "T_matter := delta S_matter/delta e_obs before readout/projector reduction; no F((T_A,A)) after variation.",
            "attempt_result": "CLEAN_IF_PARENT_VARIATION_ORDER_SIGNED",
            "gap": "readout/EFT backreaction closure remains unsigned in the 1055 chain",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "lemma_id": "SSE1066_3_naturality_route",
            "claim": "natural source scalar across ordinary matter coproduct should be common",
            "formal_statement": "Nat(Obj(C_matter), R_+) = constants if the ordinary matter category is connected by allowed morphisms.",
            "attempt_result": "HELPFUL_CONDITIONAL_ONLY",
            "gap": "species components can be disconnected; a family w_A is natural on disconnected/simple-object components",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "lemma_id": "SSE1066_4_quantum_action_scale_obstruction",
            "claim": "multiplying S_A by w_A is not guaranteed to be a harmless classical redundancy",
            "formal_statement": "S_A -> w_A S_A can leave classical EOM form invariant while changing Hilbert stress, path-integral weight, and source normalization.",
            "attempt_result": "OBSTRUCTION_SURVIVES",
            "gap": "needs parent quantum/statistical/action-scale normalization owner",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "lemma_id": "SSE1066_5_verdict",
            "claim": "parent source-scalar exclusion lemma",
            "formal_statement": "typed object language + variation-before-readout + common action-scale normalization => no inert species source scalar w_A",
            "attempt_result": "CONDITIONAL_SOURCE_SCALAR_EXCLUSION_NOT_PARENT_DERIVED",
            "gap": "action-scale/measure normalization and parent object-language typing remain unsigned",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def object_language_typing_rows() -> list[dict[str, str]]:
    return [
        {
            "type_id": "OLT1066_0_geometry",
            "candidate": "e_obs, g_obs, connection",
            "type_status": "admissible",
            "why": "observable geometry and its connection determine matter dynamics and Hilbert variation",
            "wA_effect": "species blind if one observed coframe is signed",
            "signature_status": "conditional",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "type_id": "OLT1066_1_matter_fields",
            "candidate": "Psi_A",
            "type_status": "admissible",
            "why": "ordinary species fields are dynamical variables",
            "wA_effect": "labels are bookkeeping unless source coupling can see them after variation",
            "signature_status": "allowed",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "type_id": "OLT1066_2_measured_parameters",
            "candidate": "m_A, q_A, representation data, interaction couplings",
            "type_status": "admissible_if_observable",
            "why": "they affect spectra, scattering, charge/current, or representation labels",
            "wA_effect": "not source-only if they are measured in nongravitational channels",
            "signature_status": "current_owner_unsigned",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "type_id": "OLT1066_3_universal_constant",
            "candidate": "single w_common or kappa_univ",
            "type_status": "calibration_only",
            "why": "a common multiplier can be absorbed into measured coupling only after universality guards",
            "wA_effect": "cannot absorb relative w_A/w_B",
            "signature_status": "guarded_by_common_mode_rule",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "type_id": "OLT1066_4_inert_source_scalar",
            "candidate": "w_A multiplying only S_A/source strength",
            "type_status": "rejected_by_candidate_typing",
            "why": "it has no independent observable, gauge, representation, or geometry role",
            "wA_effect": "would create WEP-sensitive T_source=sum_A w_A T_A",
            "signature_status": "not_parent_signed",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "type_id": "OLT1066_5_hidden_marker",
            "candidate": "w(m,D,boundary,A)",
            "type_status": "rejected_or_residual",
            "why": "marker/domain/boundary scalars can reintroduce labels under another name",
            "wA_effect": "must be theorem-forbidden or explicitly bounded",
            "signature_status": "obstruction_active_from_980",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "type_id": "OLT1066_6_verdict",
            "candidate": "object-language typing proof",
            "type_status": "conditional_not_parent_derived",
            "why": "typing kills w_A if accepted, but acceptance still rests on parent syntax/measure axioms",
            "wA_effect": "Delta_w_TiPt not theorem-zero yet",
            "signature_status": "open",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def operator_domain_rows() -> list[dict[str, str]]:
    return [
        {
            "rule_id": "ODR1066_0_allowed_coefficient_ring",
            "rule": "visible coefficients may depend only on q_loc and fixed representation/topological data",
            "formal_form": "Coeff(O_vis) in Alg[q_loc,Theta_rep,Level_EM]",
            "result": "POWERFUL_IF_SIGNED",
            "obstruction": "same rule was a contract in 1055, not a theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "rule_id": "ODR1066_1_continuous_target_obstruction",
            "rule": "source scalar target R_+ is continuous",
            "formal_form": "nonconstant invariant I gives w=w0+epsilon I unless invariant algebra/action target is forbidden",
            "result": "OBSTRUCTION_FROM_980",
            "obstruction": "one untrivialized invariant scalar can feed continuous source weights",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "rule_id": "ODR1066_2_species_component_obstruction",
            "rule": "species labels may form disconnected components",
            "formal_form": "Nat(C_disconnected,R_+) admits independent constants on components",
            "result": "OBSTRUCTION_SURVIVES",
            "obstruction": "need connected/rich morphism category or explicit no external source-label argument",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "rule_id": "ODR1066_3_action_scale_target",
            "rule": "action-scale coefficients are not ordinary measured couplings unless parent measure owns them",
            "formal_form": "w_A S_A is a coefficient of the variational weight, not simply a field redefinition",
            "result": "REQUIRES_PARENT_MEASURE_OWNER",
            "obstruction": "quantum/statistical normalization of each matter sector is not signed",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "rule_id": "ODR1066_4_verdict",
            "rule": "operator-domain source-scalar exclusion",
            "formal_form": "Hom(Arg_parent,R_+^species_source_only)=empty",
            "result": "EXACT_RULE_NOT_DERIVED",
            "obstruction": "requires invariant algebra triviality/no-extension plus parent action-scale ownership",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def field_measure_quantum_rows() -> list[dict[str, str]]:
    return [
        {
            "audit_id": "FMQ1066_0_classical_EOM_rescaling",
            "issue": "overall S_A multiplier may not change isolated classical equations",
            "effect": "tempts false dismissal of w_A",
            "required_closure": "show same multiplier is gauge/quotient redundancy for source and quantum measure too",
            "status": "not_closed",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "FMQ1066_1_Hilbert_source_rescaling",
            "issue": "overall S_A multiplier rescales Hilbert stress",
            "effect": "directly produces T_source=sum_A w_A T_A",
            "required_closure": "ban inert source scalars or prove universal common action normalization",
            "status": "active_obstruction",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "FMQ1066_2_path_integral_weight",
            "issue": "action scale controls phase/statistical weight",
            "effect": "species-dependent hbar/effective action scale would be physically meaningful",
            "required_closure": "single parent hbar/action measure owner for all ordinary matter",
            "status": "parent_owner_missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "FMQ1066_3_measure_jacobian",
            "issue": "species-dependent Jacobian can mimic w_A",
            "effect": "hidden measure/coframe descent can reopen source labels",
            "required_closure": "species-blind measure/coframe/boundary descent theorem",
            "status": "parallel_open_gate",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "FMQ1066_4_verdict",
            "issue": "field/measure/quantum normalization closure",
            "effect": "blocks promotion of Delta_w_TiPt=0",
            "required_closure": "derive a universal parent action-scale normalization or retain finite Delta_w prior",
            "status": "NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def delta_w_prior_rows() -> list[dict[str, str]]:
    return [
        {
            "prior_id": "DWP1066_0_WEP_bound",
            "quantity": "eta_TiPt_bound",
            "value_or_status": "2.8e-15",
            "units": "dimensionless",
            "formula_or_requirement": "abs(P_WEP_relative_source_weight) <= eta_TiPt_bound",
            "source": "source-intake/local_bounds/local_bound_claims.csv:R1_WEP_source_charge",
            "status": "bound_anchor_available",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "prior_id": "DWP1066_1_material_pair",
            "quantity": "AB",
            "value_or_status": "TA6V_minus_PtRh10",
            "units": "convention",
            "formula_or_requirement": "Delta_w_TiPt := w_Ti_source - w_Pt_source in the MICROSCOPE convention",
            "source": "source-intake/mts_residuals/P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv:MCON1061_0_test_pair",
            "status": "context_available",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "prior_id": "DWP1066_2_theorem_zero_option",
            "quantity": "Delta_w_TiPt",
            "value_or_status": "MISSING_PARENT_SOURCE_SCALAR_EXCLUSION",
            "units": "dimensionless",
            "formula_or_requirement": "Delta_w_TiPt=0 only if SSE1066_5 is parent signed",
            "source": "source-intake/mts_residuals/P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv:SSE1066_5_verdict",
            "status": "not_available",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "prior_id": "DWP1066_3_finite_prior_width",
            "quantity": "abs(Delta_w_TiPt)",
            "value_or_status": "MISSING_NUMERIC_PRIOR_WIDTH",
            "units": "dimensionless",
            "formula_or_requirement": "if tau_WEP is numeric and nonzero, require abs(Delta_w_TiPt) <= 2.8e-15/abs(tau_WEP)",
            "source": "source-intake/mts_residuals/P8_Y5_R10_1066_TAU_WEP_PROJECTION_CONTRACT.csv:TWP1066_7_verdict",
            "status": "blocked_by_tau_WEP",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "prior_id": "DWP1066_4_tau_WEP",
            "quantity": "tau_WEP",
            "value_or_status": "MISSING_LAB_SOURCE_ORBIT_PROJECTION",
            "units": "dimensionless",
            "formula_or_requirement": "derive from Earth/source worldtube, spacecraft orbit, observed coframe, and force readout",
            "source": "source-intake/mts_residuals/P8_Y5_R10_1061_INPUT_FILL_LEDGER.csv:INF1061_4_tau_WEP",
            "status": "not_available",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "prior_id": "DWP1066_5_product",
            "quantity": "P_WEP_relative_source_weight",
            "value_or_status": "MISSING_ABS_DELTA_W_TiPt_TIMES_TAU_WEP",
            "units": "dimensionless",
            "formula_or_requirement": "P = abs(Delta_w_TiPt * tau_WEP); no cancellation/sign trick accepted",
            "source": "DWP1066_2_theorem_zero_option;DWP1066_3_finite_prior_width;DWP1066_4_tau_WEP",
            "status": "not_scoreable",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def tau_wep_contract_rows() -> list[dict[str, str]]:
    return [
        {
            "contract_id": "TWP1066_0_source_worldtube",
            "input": "Earth/source worldtube and source stress profile",
            "required_form": "T_source^Earth(x) in observed local frame, with composition/source-weight convention",
            "current_status": "missing",
            "blocks": "tau_WEP normalization",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "TWP1066_1_orbit_average",
            "input": "MICROSCOPE orbit and averaging convention",
            "required_form": "time/orbit average of differential acceleration channel in the same convention as eta_AB",
            "current_status": "missing",
            "blocks": "projection from local source profile to observed eta_AB",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "TWP1066_2_observed_coframe",
            "input": "observed coframe/readout frame",
            "required_form": "same e_obs for force law, clocks, source variation, and readout",
            "current_status": "conditional_from_prior_spine",
            "blocks": "frame consistency of tau_WEP",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "TWP1066_3_material_response",
            "input": "test-body material/source tensor",
            "required_form": "Ti/Pt material response to relative source-weight channel, not just alpha/Coulomb charge",
            "current_status": "material_pair_only",
            "blocks": "full Delta_w_TiPt mapping",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "TWP1066_4_force_readout",
            "input": "differential acceleration readout map",
            "required_form": "map from parent source residual to eta_AB with units and sign/absolute convention",
            "current_status": "missing",
            "blocks": "scoreable WEP product",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "TWP1066_5_no_unity_shortcut",
            "input": "tau_WEP value",
            "required_form": "numeric sourced value, theorem-zero, or explicit retained nuisance with prior",
            "current_status": "unity_forbidden",
            "blocks": "cannot set tau_WEP=1",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "TWP1066_6_no_cancellation",
            "input": "sign/material cancellation",
            "required_form": "absolute product bound unless a signed material model is fully derived and sourced",
            "current_status": "absolute_guard_enforced",
            "blocks": "cannot hide product by cancellation",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "TWP1066_7_verdict",
            "input": "tau_WEP projection",
            "required_form": "tau_WEP = functional[source worldtube, orbit average, e_obs, material tensor, force readout]",
            "current_status": "PROJECTION_CONTRACT_WRITTEN_NOT_DERIVED",
            "blocks": "finite Delta_w prior width and WEP runner scoring",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1066_0_WEP_Delta_w_prior_width_product",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_ABS_DELTA_W_TiPt_TIMES_TAU_WEP",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1066_WEP_DELTA_W_PRIOR_WIDTH_SCHEMA.csv",
            "inputs_present": "eta_TiPt_bound=2.8e-15;material_pair=TA6V_minus_PtRh10",
            "required_inputs": "parent source-scalar theorem-zero OR numeric Delta_w_TiPt prior width;tau_WEP projection;absolute product source",
            "derivation_status": "MISSING_DELTA_W_TAUPROJECTION_PRODUCT",
            "valid_for_claim": "false",
            "notes": "The finite branch is now explicit: if the theorem fails, Delta_w_TiPt and tau_WEP must be sourced before scoring.",
        }
    ]


def bound_rows() -> list[dict[str, str]]:
    return [
        {
            "bound_id": "BOUND1066_0_WEP_source_charge",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "bound_value": "2.8e-15",
            "bound_units": "dimensionless",
            "bound_source": "source-intake/local_bounds/local_bound_claims.csv",
            "source_row": "R1_WEP_source_charge",
            "bound_type": "numeric_bound_anchor_nonclaim",
            "valid_for_claim": "true",
            "notes": "MICROSCOPE Ti/Pt source-charge proxy bound; only a bound anchor, not a prediction.",
        }
    ]


def product_status_rows(status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "runner_id": "APR1066_0_WEP_Delta_w_prior_width",
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
            "gate_id": "CG1066_0_source_scalar_exclusion",
            "claim": "inert source-only species scalars are parent-forbidden",
            "gate_pass": "false",
            "reason": "object-language typing and action-scale ownership are not parent-derived",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1066_1_Delta_w_theorem_zero",
            "claim": "Delta_w_TiPt=0",
            "gate_pass": "false",
            "reason": "source-scalar exclusion lemma remains conditional",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1066_2_finite_Delta_w_prior",
            "claim": "finite Delta_w_TiPt prior width is scoreable",
            "gate_pass": "false",
            "reason": "tau_WEP projection is missing and no numeric Delta_w prior is sourced",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1066_3_WEP_product_runner",
            "claim": "first WEP relative-weight product passes bound",
            "gate_pass": "false",
            "reason": "runner has valid_prediction_rows=0",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1066_4_local_GR_source_branch",
            "claim": "local GR/Newton source coupling is derived",
            "gate_pass": "false",
            "reason": "coupling source-side branch still needs parent action-scale/current/projection closure",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1066_0_lemma_status",
            "decision": "source-scalar exclusion is a strong conditional lemma, not a theorem",
            "because": "the proof needs parent object-language typing plus action-scale/measure ownership",
            "next_action": "attack the quantum/action-scale normalization owner",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1066_1_finite_branch_status",
            "decision": "WEP finite branch is now explicitly parameterized by Delta_w_TiPt and tau_WEP",
            "because": "bound and material convention exist, but both prediction inputs are missing",
            "next_action": "derive tau_WEP or source a numeric prior width only after tau is defined",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1066_2_best_next",
            "decision": "next target is parent action-scale normalization or tau_WEP local projection",
            "because": "action-scale closure kills w_A cleanly; tau_WEP is the finite-branch bottleneck if the theorem fails",
            "next_action": "1067-Y5-R10-parent-quantum-action-scale-normalization-or-WEP-tau-projection.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1067-Y5-R10-parent-quantum-action-scale-normalization-or-WEP-tau-projection.md",
            "objective": "derive the parent action-scale/measure normalization that forbids species-dependent S_A multipliers; if it fails, start filling tau_WEP as a real local source/orbit/readout projection instead of a unity shortcut.",
            "include": "single hbar/action-measure owner, classical EOM vs Hilbert stress distinction, path-integral/action-scale typing, species-blind measure descent, tau_WEP source-worldtube/orbit/readout functional",
            "exclude": "setting w_A=1 by convention, setting tau_WEP=1, absorbing relative weights into measured G, cancellation arguments, public WEP/local-GR claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def validate_outputs(
    outputs: dict[str, Path],
    sources: list[dict[str, str]],
    exclusion: list[dict[str, str]],
    typing: list[dict[str, str]],
    operator_domain: list[dict[str, str]],
    fmq: list[dict[str, str]],
    delta_w: list[dict[str, str]],
    tau_contract: list[dict[str, str]],
    predictions: list[dict[str, str]],
    bounds: list[dict[str, str]],
    product_status: dict[str, Any],
    claims: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []

    def add(check_id: str, condition: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "result": "pass" if condition else "fail", "detail": detail, "generated_utc": stamp()})

    add("V1066_1_sources_exist_and_needles", all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources), "every cited source path exists and every source needle was found")
    add("V1066_2_exclusion_not_promoted", any(row["lemma_id"] == "SSE1066_5_verdict" and row["attempt_result"] == "CONDITIONAL_SOURCE_SCALAR_EXCLUSION_NOT_PARENT_DERIVED" for row in exclusion), "source-scalar exclusion remains conditional")
    add("V1066_3_object_typing_blocks_wA", any(row["type_id"] == "OLT1066_4_inert_source_scalar" and row["type_status"] == "rejected_by_candidate_typing" and row["signature_status"] == "not_parent_signed" for row in typing), "object-language typing rejects w_A only as candidate grammar")
    add("V1066_4_operator_obstructions_written", len(operator_domain) >= 5 and any(row["rule_id"] == "ODR1066_1_continuous_target_obstruction" for row in operator_domain), "operator-domain continuous/species obstructions are written")
    add("V1066_5_action_scale_obstruction_written", any(row["audit_id"] == "FMQ1066_4_verdict" and row["status"] == "NOT_PARENT_SIGNED" for row in fmq), "field/measure/quantum action-scale obstruction is retained")
    add("V1066_6_delta_w_schema_missing_inputs", any(row["prior_id"] == "DWP1066_2_theorem_zero_option" and "MISSING" in row["value_or_status"] for row in delta_w) and any(row["prior_id"] == "DWP1066_4_tau_WEP" and "MISSING" in row["value_or_status"] for row in delta_w), "Delta_w theorem-zero and tau_WEP inputs remain missing")
    add("V1066_7_tau_contract_written", len(tau_contract) >= 8 and any(row["contract_id"] == "TWP1066_7_verdict" and row["current_status"] == "PROJECTION_CONTRACT_WRITTEN_NOT_DERIVED" for row in tau_contract), "tau_WEP projection contract is written but not derived")
    add("V1066_8_prediction_nonclaim", len(predictions) == 1 and "MISSING" in predictions[0]["product_value"] and predictions[0]["valid_for_claim"] == "false", "WEP Delta_w product prediction remains nonclaim")
    try:
        bound_numeric = len(bounds) == 1 and float(bounds[0]["bound_value"]) > 0
    except (ValueError, KeyError):
        bound_numeric = False
    add("V1066_9_bound_anchor_numeric", bound_numeric and bounds[0]["valid_for_claim"] == "true", "WEP bound anchor is numeric")
    add("V1066_10_runner_refuses_placeholder", product_status.get("valid_prediction_rows") == 0 and product_status.get("claim_allowed") is False, "strict runner refuses missing Delta_w/tau product")
    add("V1066_11_claim_gates_blocked", bool(claims) and all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claims), "all source-scalar/WEP/local-GR claim gates remain blocked")
    add("V1066_12_next_target_written", bool(next_rows) and next_rows[0]["next_target"].startswith("1067-Y5-R10-parent-quantum-action-scale-normalization"), "next target selects action-scale normalization or tau projection")
    generated_inside = all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in outputs.values())
    add("V1066_13_generated_files_in_post_checkpoint", generated_inside, "all generated files are under post-checkpoint-work")
    formalization_count = count_formalization_modified_since_start()
    add("V1066_14_formalization_untouched", formalization_count == 0, f"formalization-workbench modified-file count since script start is {formalization_count}")
    summary_pass = all(row["result"] == "pass" for row in checks)
    checks.insert(0, {"check_id": "V1066_SUMMARY", "result": "pass" if summary_pass else "fail", "detail": "1066 parent source-scalar exclusion / WEP Delta_w prior-width validation summary", "generated_utc": stamp()})
    return checks


def write_doc(
    sources: list[dict[str, str]],
    exclusion: list[dict[str, str]],
    typing: list[dict[str, str]],
    operator_domain: list[dict[str, str]],
    fmq: list[dict[str, str]],
    delta_w: list[dict[str, str]],
    tau_contract: list[dict[str, str]],
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
            "# 1066 — Parent Action Syntax Source-Scalar Exclusion Or WEP Delta-w Prior Width",
            "",
            "**Current verdict:** the source-scalar exclusion lemma is now exact as a conditional theorem, but not parent-derived. The block is action-scale/measure ownership: `w_A S_A` is not safely dismissible as a classical normalization.",
            "",
            "**Finite branch:** if the theorem fails, the WEP row needs both `Delta_w_TiPt` and `tau_WEP`; the MICROSCOPE bound and material convention alone are not a prediction.",
            "",
            "**No shortcut:** relative source weights cannot be absorbed into measured `G`, `tau_WEP` cannot be set to one, and signed cancellation is refused unless a full sourced material/readout model exists.",
            "",
            "## Source-Scalar Exclusion Lemma",
            md_table(exclusion, ["lemma_id", "claim", "formal_statement", "attempt_result", "gap", "valid_for_claim"]),
            "",
            "## Object-Language Typing",
            md_table(typing, ["type_id", "candidate", "type_status", "why", "wA_effect", "signature_status", "valid_for_claim"]),
            "",
            "## Operator-Domain Rule Audit",
            md_table(operator_domain, ["rule_id", "rule", "formal_form", "result", "obstruction", "valid_for_claim"]),
            "",
            "## Field / Measure / Quantum Normalization",
            md_table(fmq, ["audit_id", "issue", "effect", "required_closure", "status", "valid_for_claim"]),
            "",
            "## WEP Delta-w Prior Width Schema",
            md_table(delta_w, ["prior_id", "quantity", "value_or_status", "units", "formula_or_requirement", "status", "valid_for_claim"]),
            "",
            "## tau_WEP Projection Contract",
            md_table(tau_contract, ["contract_id", "input", "required_form", "current_status", "blocks", "valid_for_claim"]),
            "",
            "## WEP Product Candidate",
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
    exclusion = source_scalar_exclusion_rows()
    typing = object_language_typing_rows()
    operator_domain = operator_domain_rows()
    fmq = field_measure_quantum_rows()
    delta_w = delta_w_prior_rows()
    tau_contract = tau_wep_contract_rows()
    predictions = prediction_rows()
    bounds = bound_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    outputs: dict[str, Path] = {
        "source_register": OUT / "P8_Y5_R10_1066_SOURCE_REGISTER.csv",
        "exclusion": OUT / "P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv",
        "typing": OUT / "P8_Y5_R10_1066_OBJECT_LANGUAGE_TYPING_AUDIT.csv",
        "operator_domain": OUT / "P8_Y5_R10_1066_OPERATOR_DOMAIN_RULE_AUDIT.csv",
        "fmq": OUT / "P8_Y5_R10_1066_FIELD_MEASURE_QUANTUM_NORMALIZATION_AUDIT.csv",
        "delta_w": OUT / "P8_Y5_R10_1066_WEP_DELTA_W_PRIOR_WIDTH_SCHEMA.csv",
        "tau_contract": OUT / "P8_Y5_R10_1066_TAU_WEP_PROJECTION_CONTRACT.csv",
        "predictions": PREDICTION_TEMPLATE,
        "bounds": BOUND_IMPORT,
        "product_status": OUT / "P8_Y5_R10_1066_PRODUCT_RUNNER_STATUS.csv",
        "product_comparison": OUT / "P8_Y5_R10_1066_PRODUCT_COMPARISON_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_R10_1066_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1066_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1066_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1066_VALIDATION.csv",
        "doc": DOC,
    }

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["exclusion"], exclusion)
    write_csv(outputs["typing"], typing)
    write_csv(outputs["operator_domain"], operator_domain)
    write_csv(outputs["fmq"], fmq)
    write_csv(outputs["delta_w"], delta_w)
    write_csv(outputs["tau_contract"], tau_contract)
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
        exclusion,
        typing,
        operator_domain,
        fmq,
        delta_w,
        tau_contract,
        predictions,
        bounds,
        product_status,
        claims,
        next_rows,
    )
    write_csv(outputs["validation"], validation)
    write_doc(
        sources,
        exclusion,
        typing,
        operator_domain,
        fmq,
        delta_w,
        tau_contract,
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

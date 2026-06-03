from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "metric-compatibility-Levi-Civita-or-R11-connection-row"
CHECKPOINT_DOC = "443-metric-compatibility-Levi-Civita-or-R11-connection-row.md"
STATUS = "metric_compatibility_connection_row_written_connection_theorem_not_parent_derived_torsion_nonmetricity_demoted_to_R11_no_EH_Newton_PPN_or_local_GR_pass"
CLAIM_CEILING = "metric_compatibility_connection_row_only_no_WEP_EH_Newton_PPN_R11_or_local_GR_pass"
NEXT_TARGET = "444-source-normalization-residual-vector-refinement.md"
P4_TEMPLATE_PATH = Path("source-intake/mts_residuals/R11_P4_connection_rows_TEMPLATE.csv")


R11_VECTOR_COLUMNS = [
    "model_id",
    "branch_id",
    "vector_id",
    "operator_family",
    "coefficient_symbol",
    "coefficient_value",
    "coefficient_units",
    "normalization",
    "operator_form",
    "weak_field_map",
    "affected_rows",
    "induced_observable",
    "predicted_residual_or_bound_source",
    "derivation_status",
    "formula_reference",
    "source_file",
    "assumptions",
    "valid_for_claim",
    "notes",
]


SOURCE_DOCS = [
    {
        "path": "382-parent-local-action-minimal-contract.md",
        "role": "minimal parent action blocks and variation identities",
    },
    {
        "path": "392-EH-operator-selection-under-identity-closure.md",
        "role": "matter written with omega[e] and warning that identity closure does not derive EH",
    },
    {
        "path": "438-R11-nonEH-coefficient-vector-contract.md",
        "role": "R11 torsion/nonmetricity operator-family contract",
    },
    {
        "path": "439-EH-only-exterior-parent-premise-ladder.md",
        "role": "P4 metric-compatibility rung in the EH-only ladder",
    },
    {
        "path": "440-metric-only-second-order-sector-reduction-attempt.md",
        "role": "torsion/nonmetricity sector reduction matrix",
    },
    {
        "path": "441-extra-sector-nohair-priority-gate.md",
        "role": "torsion/nonmetricity selected as crisp follow-up after P6",
    },
    {
        "path": "442-P6-second-order-operator-restriction-or-R11-demotion.md",
        "role": "P6 demotion and next target for P4",
    },
    {
        "path": "runs/20260602-055500-quotient-matter-functor-theorem-attempt/results/matter_argument_audit.csv",
        "role": "omega[e_obs] matter-argument hazard and required control",
    },
    {
        "path": "runs/20260602-130000-R11-nonEH-coefficient-vector-contract/results/operator_families.csv",
        "role": "canonical R11 operator family row for torsion/nonmetricity",
    },
    {
        "path": "runs/20260602-133000-metric-only-second-order-sector-reduction-attempt/results/sector_reduction_matrix.csv",
        "role": "machine-readable connection-sector reduction row",
    },
    {
        "path": "runs/20260602-134500-extra-sector-nohair-priority-gate/results/sector_priority_matrix.csv",
        "role": "P4 priority score and fallback route",
    },
    {
        "path": "source-intake/mts_residuals/R11_nonEH_operator_vector_TEMPLATE.csv",
        "role": "general R11 vector template to match for P4-specific rows",
    },
]


P4_PROBLEM_STATEMENT = [
    {
        "item": "P4_target",
        "statement": "derive that the observed local connection is Levi-Civita and universally used by matter, light, clocks, and spin",
        "mathematical_form": "nabla_mu g_ab=0 and T^alpha_{mu nu}=0 with Gamma=Gamma_LC[g]",
        "current_status": "central_blocker_not_parent_derived",
    },
    {
        "item": "why_it_matters",
        "statement": "without P4, WEP, clock, spin, light-cone, and R11 operator channels remain open even if an EH-like metric block exists",
        "mathematical_form": "Gamma=Gamma_LC + C(T,Q,Delta_matter)",
        "current_status": "R11_retained",
    },
    {
        "item": "legal_success",
        "statement": "the parent action either has no independent connection or its connection variation forces zero torsion and zero nonmetricity with no matter hypermomentum residue",
        "mathematical_form": "delta_Gamma S_parent=0 implies C^alpha_{mu nu}=0",
        "current_status": "not_derived",
    },
    {
        "item": "legal_failure",
        "statement": "if any independent connection, torsion, nonmetricity, spin, hypermomentum, or source-connection coupling survives, P4 becomes explicit R11 data",
        "mathematical_form": "R11_P4_connection_rows_TEMPLATE.csv",
        "current_status": "template_written_by_this_checkpoint",
    },
]


COMPATIBILITY_THEOREM_ROUTES = [
    {
        "route_id": "P4_R0_metric_formalism_if_parent_selects_only_g",
        "route_claim": "connection is not an independent parent variable; Gamma is defined as Gamma_LC[g] and matter uses omega[e]",
        "required_parent_evidence": "configuration-space theorem selecting one observed metric/coframe and excluding independent Gamma, torsion, nonmetricity, and source connection charges",
        "result": "would_close_P4_kinematically",
        "status": "conditional_not_parent_derived",
        "why_not_enough": "current files use omega[e] in places, but do not derive the absence of all independent connection variables from the parent action",
    },
    {
        "route_id": "P4_R1_Palatini_EH_no_hypermomentum",
        "route_claim": "variation of an EH Palatini action with matter independent of Gamma gives Levi-Civita up to harmless projective freedom",
        "required_parent_evidence": "EH-only connection sector, no torsion/nonmetricity kinetic terms, no matter hypermomentum, projective mode fixed or unobservable",
        "result": "would_close_P4_after_P6_EH_and_matter_gate",
        "status": "blocked_by_open_premises",
        "why_not_enough": "P6/EH-only is not derived, and matter/light/spin independence from Gamma is not proven",
    },
    {
        "route_id": "P4_R2_first_order_coframe_zero_spin_torsion",
        "route_claim": "spin-connection variation of the first-order coframe action imposes vanishing torsion",
        "required_parent_evidence": "Palatini/tetrad EH action plus zero net spin/hypermomentum or a theorem that spin torsion is absent/undetectable in the branch",
        "result": "could_kill_torsion_conditionally",
        "status": "not_parent_derived",
        "why_not_enough": "ordinary spinor matter can source Einstein-Cartan torsion unless explicitly excluded or mapped",
    },
    {
        "route_id": "P4_R3_metric_affine_zero_Q_zero_T_theorem",
        "route_claim": "the parent metric-affine equations algebraically force both torsion and nonmetricity to zero",
        "required_parent_evidence": "positive algebraic connection operator with no source term, boundary residue, projective trace, or nonmetric light/clock coupling",
        "result": "would_derive_P4_dynamically",
        "status": "not_supplied",
        "why_not_enough": "no current action-level equation supplies the required zero-source algebraic connection theorem",
    },
    {
        "route_id": "P4_R4_projective_gauge_only",
        "route_claim": "a projective connection residue can be gauge-fixed or made unobservable",
        "required_parent_evidence": "proof that only the projective trace remains and all matter/light/clocks are projectively invariant",
        "result": "partial_not_full_P4",
        "status": "insufficient",
        "why_not_enough": "projective freedom does not remove generic axial torsion, tensor torsion, Weyl nonmetricity, shear nonmetricity, or hypermomentum",
    },
    {
        "route_id": "P4_R5_empirical_R11_connection_vector",
        "route_claim": "retain connection residues as coefficient rows and map them into WEP, clock, spin, light-cone, and operator-ledger residuals",
        "required_parent_evidence": "coefficient values or bounds, units, normalization, weak-field maps, affected rows, and source paths",
        "result": "modified_gravity_branch_only",
        "status": "R11_demotion",
        "why_not_enough": "empirical smallness can keep the model viable, but it is not a theorem-zero local-GR reduction",
    },
]


CONNECTION_OPERATOR_DEMOTIONS = [
    {
        "operator_family": "torsion_nonmetricity_combined",
        "operator_form": "c_T T^2 + c_Q Q^2 + matter connection couplings",
        "P4_status": "not_forbidden",
        "affected_rows": "R0;R1;R2;R11",
        "theorem_zero_condition": "T=0 and Q=0 from parent variation or no independent connection in the parent configuration",
        "demotion_action": "fill P4 R11 combined connection row and split into torsion/nonmetricity subrows if nonzero",
    },
    {
        "operator_family": "axial_torsion_spin_coupling",
        "operator_form": "S_mu psi_bar gamma^mu gamma5 psi or equivalent spin-torsion coupling",
        "P4_status": "not_forbidden",
        "affected_rows": "R0;R2;R11",
        "theorem_zero_condition": "spin connection is omega[e] only or spin-sourced torsion is algebraically zero/below mapped bound",
        "demotion_action": "fill spin/light/clock residual map before any local-GR claim",
    },
    {
        "operator_family": "torsion_trace_projective_mode",
        "operator_form": "T_mu trace/projective connection residue",
        "P4_status": "partly_gauge_possible_not_closed",
        "affected_rows": "R0;R1;R11",
        "theorem_zero_condition": "only projective trace remains and all sectors are projectively invariant, or trace fixed to zero",
        "demotion_action": "record projective gauge proof or retain source/WEP residual row",
    },
    {
        "operator_family": "nonmetricity_weyl_trace",
        "operator_form": "Q_mu g_ab length/clock nonmetricity",
        "P4_status": "not_forbidden",
        "affected_rows": "R0;R2;R11",
        "theorem_zero_condition": "Q_mu=0 or universal integrable calibration with no clock/rod species dependence",
        "demotion_action": "fill clock/redshift/rod residual map",
    },
    {
        "operator_family": "nonmetricity_shear_lightcone",
        "operator_form": "tilde_Q_{lambda mu nu} trace-free nonmetricity altering local light/metric compatibility",
        "P4_status": "not_forbidden",
        "affected_rows": "R0;R2;R11",
        "theorem_zero_condition": "trace-free Q is absent or algebraically zero in observed branch",
        "demotion_action": "fill light-cone/clock/WEP residual map",
    },
    {
        "operator_family": "independent_connection_hypermomentum",
        "operator_form": "Delta_lambda^{mu nu} delta Gamma^lambda_{mu nu} from matter/source/readout sectors",
        "P4_status": "not_forbidden",
        "affected_rows": "R0;R1;R2;R11",
        "theorem_zero_condition": "all matter, light, spin, source, and readout actions are independent of Gamma except through omega[e]",
        "demotion_action": "fill hypermomentum/source-charge row or derive no-Gamma matter theorem",
    },
]


P4_R11_TEMPLATE_ROWS = [
    {
        "model_id": "MTS_branch_name",
        "branch_id": "fill_branch_id",
        "vector_id": "R11_P4_connection_rows",
        "operator_family": "torsion_nonmetricity_combined",
        "coefficient_symbol": "c_T_or_c_Q",
        "coefficient_value": "fill_numeric_or_zero",
        "coefficient_units": "fill_length_power_or_dimensionless_after_normalization",
        "normalization": "fill_relative_to_EH_measured_G_or_connection_scale",
        "operator_form": "c_T T^2 + c_Q Q^2 + matter connection couplings",
        "weak_field_map": "fill_WEP_clock_lightcone_spin_source_map",
        "affected_rows": "R0;R1;R2;R11",
        "induced_observable": "eta_WEP;clock_residual;lightcone_residual;operator_ledger",
        "predicted_residual_or_bound_source": "fill_numeric_residual_bound_or_map_path",
        "derivation_status": "fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative",
        "formula_reference": "fill_formula_reference",
        "source_file": "fill_derivation_or_run_path",
        "assumptions": "fill_frame_matter_connection_projective_spin_clock_assumptions",
        "valid_for_claim": "false",
        "notes": "P4 template only; combined row must split if torsion or nonmetricity is nonzero",
    },
    {
        "model_id": "MTS_branch_name",
        "branch_id": "fill_branch_id",
        "vector_id": "R11_P4_connection_rows",
        "operator_family": "axial_torsion_spin_coupling",
        "coefficient_symbol": "c_A_or_S_mu",
        "coefficient_value": "fill_numeric_or_zero",
        "coefficient_units": "fill_torsion_units_or_normalized_spin_units",
        "normalization": "fill_relative_to_spin_connection_or_EH_scale",
        "operator_form": "S_mu psi_bar gamma^mu gamma5 psi",
        "weak_field_map": "fill_spin_clock_lightcone_WEP_map",
        "affected_rows": "R0;R2;R11",
        "induced_observable": "spin_torsion_residual;clock_residual;operator_ledger",
        "predicted_residual_or_bound_source": "fill_spin_torsion_bound_or_map_path",
        "derivation_status": "fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative",
        "formula_reference": "fill_formula_reference",
        "source_file": "fill_derivation_or_run_path",
        "assumptions": "fill_spinor_matter_Einstein_Cartan_or_no_spin_assumptions",
        "valid_for_claim": "false",
        "notes": "P4 template only; spinor matter prevents silent zero unless parent route excludes or maps torsion",
    },
    {
        "model_id": "MTS_branch_name",
        "branch_id": "fill_branch_id",
        "vector_id": "R11_P4_connection_rows",
        "operator_family": "torsion_trace_projective_mode",
        "coefficient_symbol": "c_Ttrace_or_T_mu",
        "coefficient_value": "fill_numeric_or_zero",
        "coefficient_units": "fill_inverse_length_or_normalized_units",
        "normalization": "fill_projective_gauge_or_source_normalization",
        "operator_form": "T_mu trace/projective connection residue",
        "weak_field_map": "fill_projective_invariance_or_WEP_source_map",
        "affected_rows": "R0;R1;R11",
        "induced_observable": "eta_WEP;source_charge_residual;operator_ledger",
        "predicted_residual_or_bound_source": "fill_projective_bound_or_gauge_proof_path",
        "derivation_status": "fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative",
        "formula_reference": "fill_formula_reference",
        "source_file": "fill_derivation_or_run_path",
        "assumptions": "fill_projective_gauge_matter_invariance_assumptions",
        "valid_for_claim": "false",
        "notes": "P4 template only; projective mode is safe only if all sectors are invariant or the mode is fixed",
    },
    {
        "model_id": "MTS_branch_name",
        "branch_id": "fill_branch_id",
        "vector_id": "R11_P4_connection_rows",
        "operator_family": "nonmetricity_weyl_trace",
        "coefficient_symbol": "c_Qtrace_or_Q_mu",
        "coefficient_value": "fill_numeric_or_zero",
        "coefficient_units": "fill_inverse_length_or_normalized_units",
        "normalization": "fill_clock_rod_or_EH_normalization",
        "operator_form": "Q_mu g_ab length/clock nonmetricity",
        "weak_field_map": "fill_clock_rod_redshift_WEP_map",
        "affected_rows": "R0;R2;R11",
        "induced_observable": "clock_residual;rod_residual;eta_WEP;operator_ledger",
        "predicted_residual_or_bound_source": "fill_clock_or_nonmetricity_bound_path",
        "derivation_status": "fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative",
        "formula_reference": "fill_formula_reference",
        "source_file": "fill_derivation_or_run_path",
        "assumptions": "fill_nonmetric_clock_universality_assumptions",
        "valid_for_claim": "false",
        "notes": "P4 template only; nonmetric clock/rod effects must be theorem-zero or mapped",
    },
    {
        "model_id": "MTS_branch_name",
        "branch_id": "fill_branch_id",
        "vector_id": "R11_P4_connection_rows",
        "operator_family": "nonmetricity_shear_lightcone",
        "coefficient_symbol": "c_Qshear_or_Q_tilde",
        "coefficient_value": "fill_numeric_or_zero",
        "coefficient_units": "fill_inverse_length_or_normalized_units",
        "normalization": "fill_lightcone_or_EH_normalization",
        "operator_form": "trace-free nonmetricity tilde_Q_{lambda mu nu}",
        "weak_field_map": "fill_lightcone_clock_WEP_map",
        "affected_rows": "R0;R2;R11",
        "induced_observable": "lightcone_residual;clock_residual;eta_WEP;operator_ledger",
        "predicted_residual_or_bound_source": "fill_lightcone_or_nonmetricity_bound_path",
        "derivation_status": "fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative",
        "formula_reference": "fill_formula_reference",
        "source_file": "fill_derivation_or_run_path",
        "assumptions": "fill_metric_lightcone_connection_assumptions",
        "valid_for_claim": "false",
        "notes": "P4 template only; metric light-cone cannot be assumed if shear nonmetricity survives",
    },
    {
        "model_id": "MTS_branch_name",
        "branch_id": "fill_branch_id",
        "vector_id": "R11_P4_connection_rows",
        "operator_family": "independent_connection_hypermomentum",
        "coefficient_symbol": "c_Delta_or_Delta_lambda_munu",
        "coefficient_value": "fill_numeric_or_zero",
        "coefficient_units": "fill_hypermomentum_or_normalized_units",
        "normalization": "fill_matter_source_readout_connection_normalization",
        "operator_form": "Delta_lambda^{mu nu} delta Gamma^lambda_{mu nu}",
        "weak_field_map": "fill_WEP_source_clock_spin_map",
        "affected_rows": "R0;R1;R2;R11",
        "induced_observable": "eta_WEP;source_charge_residual;clock_residual;operator_ledger",
        "predicted_residual_or_bound_source": "fill_hypermomentum_bound_or_no_Gamma_matter_proof_path",
        "derivation_status": "fill: derived_zero/derived_bound/fitted/phenomenological/closure_assumed/speculative",
        "formula_reference": "fill_formula_reference",
        "source_file": "fill_derivation_or_run_path",
        "assumptions": "fill_universal_matter_light_spin_source_connection_assumptions",
        "valid_for_claim": "false",
        "notes": "P4 template only; no local-GR claim while matter/source connection charges are placeholders",
    },
]


P4_GATE_TESTS = [
    {
        "gate": "observed_frame_gate",
        "pass_condition": "one observed metric/coframe is parent-selected for all matter, photons, clocks, rods, and spin",
        "current_result": "conditional_open",
        "evidence": "omega[e_obs] is used in the matter audit, but parent selection is not derived",
    },
    {
        "gate": "independent_connection_absence_gate",
        "pass_condition": "Gamma/omega is either absent as an independent variable or its Euler equation gives Gamma_LC[g]",
        "current_result": "fail_open",
        "evidence": "no source file derives the connection Euler equation killing all C(T,Q,Delta)",
    },
    {
        "gate": "hypermomentum_spin_gate",
        "pass_condition": "matter, light, spin, source, and readout sectors carry no independent connection charge",
        "current_result": "fail_open",
        "evidence": "spin/hypermomentum are known escape routes unless omega[e] use is parent-derived universally",
    },
    {
        "gate": "projective_residue_gate",
        "pass_condition": "any projective trace is fixed or unobservable to all sectors",
        "current_result": "conditional_open",
        "evidence": "projective freedom can be harmless only after a dedicated invariance proof",
    },
    {
        "gate": "WEP_clock_lightcone_map_gate",
        "pass_condition": "all surviving connection residues have executable residual maps or derived zeros",
        "current_result": "demote_to_R11",
        "evidence": "P4-specific R11 template rows are written but not filled with data",
    },
]


THEOREM_ATTEMPT_STATUS = [
    {
        "claim": "P4 theorem routes audited",
        "status": "pass",
        "evidence": "6 candidate routes recorded with required parent evidence",
    },
    {
        "claim": "metric-formalism route preserved",
        "status": "pass_conditional",
        "evidence": "if the parent action has only g/e and matter universally uses omega[e], P4 closes kinematically",
    },
    {
        "claim": "Palatini/EH connection route preserved",
        "status": "pass_conditional",
        "evidence": "if EH-only plus no hypermomentum/projective residue is derived, connection compatibility follows",
    },
    {
        "claim": "Levi-Civita compatibility parent-derived",
        "status": "fail",
        "evidence": "no current parent action equation derives T=0 and Q=0 for the observed branch",
    },
    {
        "claim": "torsion/nonmetricity theorem-zero",
        "status": "fail",
        "evidence": "spin, projective, hypermomentum, and nonmetric clock/light-cone channels remain legal",
    },
    {
        "claim": "P4 demoted to executable R11 fallback",
        "status": "pass",
        "evidence": str(P4_TEMPLATE_PATH),
    },
    {
        "claim": "WEP/EH/Newton/PPN/local-GR promoted",
        "status": "fail",
        "evidence": "P4 demotion only; no R11 data and no local-GR pass",
    },
]


GATE_RESULTS_TEMPLATE = [
    {
        "gate": "P4_problem_statement_written",
        "status": "pass",
        "evidence": "P4 target, success, and failure conditions recorded",
    },
    {
        "gate": "compatibility_theorem_routes_audited",
        "status": "pass",
        "evidence": "6 routes audited",
    },
    {
        "gate": "connection_operator_demotion_rows_written",
        "status": "pass",
        "evidence": "6 P4 operator demotion rows recorded",
    },
    {
        "gate": "P4_R11_template_written",
        "status": "pass",
        "evidence": str(P4_TEMPLATE_PATH),
    },
    {
        "gate": "Levi_Civita_parent_derived",
        "status": "fail",
        "evidence": "no current parent connection variation proves Gamma=Gamma_LC[g]",
    },
    {
        "gate": "torsion_zero_derived",
        "status": "fail",
        "evidence": "torsion is not killed if spin/projective/independent connection channels survive",
    },
    {
        "gate": "nonmetricity_zero_derived",
        "status": "fail",
        "evidence": "nonmetricity is not killed without a metric-affine zero-Q theorem or metric-only parent route",
    },
    {
        "gate": "hypermomentum_absence_derived",
        "status": "fail",
        "evidence": "universal matter/source independence from independent Gamma is not parent-derived",
    },
    {
        "gate": "P4_promoted",
        "status": "fail",
        "evidence": "P4 is demoted to R11 unless future theorem closes it",
    },
    {
        "gate": "R11_data_supplied",
        "status": "fail",
        "evidence": "template rows only; no numeric coefficients or weak-field maps supplied",
    },
    {
        "gate": "local_GR_promoted",
        "status": "fail",
        "evidence": "P4 audit only; no WEP/EH/Newton/PPN/local-GR pass",
    },
    {
        "gate": "claim_ceiling_enforced",
        "status": "pass",
        "evidence": CLAIM_CEILING,
    },
]


DECISION = [
    {
        "decision": "P4 is now a sharp theorem-or-vector fork. The clean winning route is not to assert a plateau or a readout convention; it is to show that the parent configuration has only the observed metric/coframe connection omega[e], or that an independent connection variation forces torsion, nonmetricity, projective residue, and matter hypermomentum to vanish. The current corpus does not yet derive that. Therefore Levi-Civita compatibility remains conditional, and torsion/nonmetricity are demoted into explicit R11 P4 connection rows. This protects the GR-reduction route without pretending the connection problem has been solved.",
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "rank": 1,
        "target": "444-source-normalization-residual-vector-refinement.md",
        "why_next": "the Newton lane is now the biggest parallel blocker: measured GM must be constant, universal, and range/time/species independent",
    },
    {
        "rank": 2,
        "target": "fill R11_P4_connection_rows_TEMPLATE.csv",
        "why_next": "if P4 remains demoted, torsion/nonmetricity coefficients need executable bounds and weak-field maps",
    },
    {
        "rank": 3,
        "target": "derive no-independent-connection parent configuration theorem",
        "why_next": "the clean P4 win is a parent action variable-selection theorem, not an empirical bound",
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
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
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCE_DOCS:
        source_path = ROOT / source["path"]
        rows.append(
            {
                "source_file": source["path"],
                "exists": source_path.exists(),
                "role": source["role"],
            }
        )
    return rows


def gate_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    source_gate = {
        "gate": "source_paths_exist",
        "status": "pass" if not missing_sources else "fail",
        "evidence": "all cited source paths exist" if not missing_sources else ";".join(missing_sources),
    }
    template_schema_gate = {
        "gate": "P4_template_schema_matches_R11",
        "status": "pass" if list(P4_R11_TEMPLATE_ROWS[0].keys()) == R11_VECTOR_COLUMNS else "fail",
        "evidence": "P4 template columns match canonical R11 vector schema"
        if list(P4_R11_TEMPLATE_ROWS[0].keys()) == R11_VECTOR_COLUMNS
        else "P4 template schema mismatch",
    }
    return [source_gate, template_schema_gate, *GATE_RESULTS_TEMPLATE]


def write_checkpoint_markdown(run_dir: Path, gate_result_rows: list[dict[str, Any]]) -> None:
    source_rows = source_register_rows()
    text = f"""# 443 - Metric Compatibility Levi-Civita Or R11 Connection Row

Private EH/connection checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, R11, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 442 left the metric operator route sharpened but not promoted. This checkpoint attacks P4 directly: can the current parent-action route derive that the observed local connection is Levi-Civita, or must torsion and nonmetricity be retained as explicit R11 connection rows?

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/metric_compatibility_Levi_Civita_or_R11_connection_row.py` |
| Run directory | `runs/{run_dir.name}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| P4 R11 template | `{P4_TEMPLATE_PATH}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(source_rows, ["source_file", "exists", "role"])}

## 4. P4 Problem Statement

{markdown_table(P4_PROBLEM_STATEMENT, ["item", "statement", "mathematical_form", "current_status"])}

## 5. Compatibility Theorem Routes

{markdown_table(COMPATIBILITY_THEOREM_ROUTES, ["route_id", "route_claim", "result", "status", "why_not_enough"])}

## 6. Connection Operator Demotions

{markdown_table(CONNECTION_OPERATOR_DEMOTIONS, ["operator_family", "P4_status", "affected_rows", "theorem_zero_condition", "demotion_action"])}

## 7. P4 R11 Template Rows

The P4-specific R11 template has been written to `{P4_TEMPLATE_PATH}`.

{markdown_table(P4_R11_TEMPLATE_ROWS, R11_VECTOR_COLUMNS)}

## 8. P4 Gate Tests

{markdown_table(P4_GATE_TESTS, ["gate", "pass_condition", "current_result", "evidence"])}

## 9. Theorem Attempt Status

{markdown_table(THEOREM_ATTEMPT_STATUS, ["claim", "status", "evidence"])}

## 10. Gate Results

{markdown_table(gate_result_rows, ["gate", "status", "evidence"])}

## 11. Decision

{DECISION[0]["decision"]}

Practical read: this is not grim, it is useful. The local-GR route now knows exactly where the connection has to be won. Either the parent action never allows an independent connection into the observed branch, or every surviving connection residue has to step into the R11 ring with coefficients, units, and residual maps.

## 12. Next Queue

{markdown_table(NEXT_QUEUE, ["rank", "target", "why_next"])}
"""
    (ROOT / CHECKPOINT_DOC).write_text(text, encoding="utf-8")


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()
    gate_result_rows = gate_rows(source_rows)

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "P4_problem_statement.csv", P4_PROBLEM_STATEMENT)
    write_csv(results_dir / "compatibility_theorem_routes.csv", COMPATIBILITY_THEOREM_ROUTES)
    write_csv(results_dir / "connection_operator_demotions.csv", CONNECTION_OPERATOR_DEMOTIONS)
    write_csv(results_dir / "P4_R11_template_rows.csv", P4_R11_TEMPLATE_ROWS, R11_VECTOR_COLUMNS)
    write_csv(results_dir / "P4_gate_tests.csv", P4_GATE_TESTS)
    write_csv(results_dir / "theorem_attempt_status.csv", THEOREM_ATTEMPT_STATUS)
    write_csv(results_dir / "gate_results.csv", gate_result_rows)
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)
    write_csv(ROOT / P4_TEMPLATE_PATH, P4_R11_TEMPLATE_ROWS, R11_VECTOR_COLUMNS)
    write_csv(results_dir / "R11_P4_connection_rows_TEMPLATE.csv", P4_R11_TEMPLATE_ROWS, R11_VECTOR_COLUMNS)

    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "compatibility_theorem_routes": len(COMPATIBILITY_THEOREM_ROUTES),
        "connection_operator_demotion_rows": len(CONNECTION_OPERATOR_DEMOTIONS),
        "P4_template_rows": len(P4_R11_TEMPLATE_ROWS),
        "Levi_Civita_parent_derived": False,
        "torsion_zero_derived": False,
        "nonmetricity_zero_derived": False,
        "hypermomentum_absence_derived": False,
        "P4_promoted": False,
        "R11_data_supplied": False,
        "WEP_promoted": False,
        "EH_promoted": False,
        "Newtonian_reduction_promoted": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "P4_template_path": str(ROOT / P4_TEMPLATE_PATH),
        "checkpoint_doc": CHECKPOINT_DOC,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    write_checkpoint_markdown(run_dir, gate_result_rows)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 443 metric compatibility Levi-Civita or R11 connection row artifacts."
    )
    parser.add_argument(
        "--timestamp",
        default=datetime.now().strftime("%Y%m%d-%H%M%S"),
        help="Run timestamp prefix.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_dir = write_run(args.timestamp)
    print(json.dumps({"status": STATUS, "run_dir": str(run_dir)}, indent=2))


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "620-Y5-R10-qbarXT-residual-envelope-after-no-marker-failure.md"
SCRIPT_REL = "scripts/Y5_R10_qbarXT_residual_envelope_after_no_marker_failure.py"
STATUS = "Y5_R10_qbarXT_residual_envelope_derived_as_on_shell_chain_rule_vector_no_local_GR_claim"
CLAIM_CEILING = "private_residual_decomposition_only_no_qbarXT_zero_R10_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "621-Y5-R10-matter-coupling-normal-form-theorem-or-residual-coefficient-priors.md"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = fieldnames or (list(rows[0].keys()) if rows else [])
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_bool(value: object) -> bool:
    return str(value).strip().lower() == "true"


def md_table(rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    fields = fieldnames or list(rows[0].keys())

    def cell(value: object) -> str:
        return str(value).replace("|", "\\|").replace("\n", " ")

    lines = [
        "| " + " | ".join(cell(field) for field in fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def build_source_register() -> list[dict[str, object]]:
    sources = [
        ("619-Y5-R10-no-marker-minimal-quotient-theorem-or-qbarXT-residual-fill.md", "immediate handoff: qbarXT residual fill selected"),
        ("source-intake/mts_residuals/P8_Y5_BRR545_619_VALIDATION.csv", "prior validation gate"),
        ("source-intake/mts_residuals/P8_Y5_R10_619_QBARXT_RESIDUAL_FILL_TEMPLATE.csv", "619 component template"),
        ("source-intake/mts_residuals/P8_Y5_R10_619_COUNTEREXAMPLE_ROUTER.csv", "619 counterexample to residual-channel map"),
        ("source-intake/mts_residuals/P8_Y5_R10_619_MINIMAL_QUOTIENT_GATE.csv", "619 minimal quotient gate"),
        ("613-Y5-R10-parent-matter-selector-theorem-or-finite-CX-envelope-lock.md", "selector theorem and qbarXT zero failure"),
        ("576-Y5-R10-constant-source-current-universality-or-qbar-envelope.md", "constant/source-current residual basis"),
        ("565-Y5-R10-coframe-pullback-zero-or-finite-alpha-coefficient.md", "metric/coframe pullback zero route"),
        ("410-quotient-matter-functor-theorem-attempt.md", "quotient matter functor theorem attempt"),
        ("423-parent-action-minimality-no-extension-theorem-attempt.md", "minimal/no-extension theorem attempt"),
        ("source-intake/mts_residuals/P8_Y5_R10_576_UNIVERSALITY_PREMISE_LEDGER.csv", "constant/source-current premise ledger"),
        (SCRIPT_REL, "this checkpoint generator"),
    ]
    return [
        {"source_file": source_file, "exists": (ROOT / source_file).exists(), "role": role}
        for source_file, role in sources
    ]


def build_residual_basis_rows() -> list[dict[str, object]]:
    return [
        {
            "component_id": "QXT620_0_metric_common",
            "channel": "common metric/coframe readout",
            "normalized_symbol": "b_g",
            "definition": "b_g := projected 0.5*T^ab*Lie_vX(hat_g_ab)/rho_ref, equivalently a common-frame log derivative when hat_g_ab=A_g(X)^2 g_ab",
            "dimension_status": "dimensionless_after_rho_ref_projection",
            "zero_condition": "Lie_vX(hat_g_ab)=0 because observed geometry factors through Q_MTS",
            "bound_condition": "bound b_g through inverse-square, local gravity, clocks, or PPN projections once K_X, Qbar_XH, and lambda_X are known",
            "observable_links": "R10 inverse-square; PPN if long range; universal clock/gravitational redshift checks",
            "parent_input_needed": "observed metric/coframe normal-form theorem or sourced Fprime_X coefficient",
            "current_status": "open_residual",
            "valid_for_claim": "false",
        },
        {
            "component_id": "QXT620_1_constants",
            "channel": "ordinary constants and representation data",
            "normalized_symbol": "b_theta",
            "definition": "b_theta := sum_A projected (partial L_m/partial theta_A)*Lie_vX(theta_A)/rho_ref",
            "dimension_status": "dimensionless_if_each_theta_derivative_is_log_normalized",
            "zero_condition": "Lie_vX(theta_A)=0 for all ordinary constants by parent superselection/representation theorem",
            "bound_condition": "bound each d ln theta_A/dX through clocks, alpha_EM, mass ratios, spectra, composition tests",
            "observable_links": "atomic clocks; fine-structure; WEP/composition; particle-mass sector",
            "parent_input_needed": "constant-triviality theorem or coefficient ledger for d ln theta_A/dX",
            "current_status": "open_residual",
            "valid_for_claim": "false",
        },
        {
            "component_id": "QXT620_2_marker",
            "channel": "material marker field",
            "normalized_symbol": "b_m",
            "definition": "b_m := projected (partial L_m/partial m)*Lie_vX(m)/rho_ref for any retained marker m",
            "dimension_status": "dimensionless_after_marker_coupling_normalization",
            "zero_condition": "marker is absent, pure gauge, or a unique source-independent auxiliary with Lie_vX effective m=0",
            "bound_condition": "bound marker coupling by composition dependence, fifth-force source charge, or set to zero only after classification",
            "observable_links": "WEP/composition; R10 source-test contrast; material-sector anomalies",
            "parent_input_needed": "marker classification theorem and coupling normalization",
            "current_status": "open_residual",
            "valid_for_claim": "false",
        },
        {
            "component_id": "QXT620_3_source_weight",
            "channel": "species or class weighted source current",
            "normalized_symbol": "b_kappa",
            "definition": "b_kappa := projected sum_A ((kappa_A-kappa)/kappa)*T_A/T_ref",
            "dimension_status": "dimensionless",
            "zero_condition": "one universal source current with one kappa for all ordinary matter",
            "bound_condition": "bound kappa_A splittings through Eotvos/composition tests and source-material swaps",
            "observable_links": "WEP; composition-dependent fifth force; R10 material contrast",
            "parent_input_needed": "universal Hilbert/coframe source-current theorem",
            "current_status": "open_residual",
            "valid_for_claim": "false",
        },
        {
            "component_id": "QXT620_4_nonHilbert",
            "channel": "non-Hilbert/coframe current",
            "normalized_symbol": "b_NH",
            "definition": "b_NH := projected J_XT_nonHilbert/J_ref after matter equations of motion",
            "dimension_status": "dimensionless_after_reference_current_choice",
            "zero_condition": "non-Hilbert current is exact, boundary-only with zero flux, absent, or separately varied and constrained",
            "bound_condition": "bound any spin, torsion, topological, or edge current coefficient in the relevant local environment",
            "observable_links": "spin-polarized tests; torsion searches; boundary/edge residual audits",
            "parent_input_needed": "current decomposition theorem and boundary/flux certificate",
            "current_status": "open_residual",
            "valid_for_claim": "false",
        },
        {
            "component_id": "QXT620_5_readout_counterterm",
            "channel": "post-readout EFT or phenomenological counterterm",
            "normalized_symbol": "b_EFT",
            "definition": "b_EFT := projected delta_X(L_EFT_after_readout)/rho_ref",
            "dimension_status": "dimensionless_after_EFT_operator_normalization",
            "zero_condition": "counterterm is absent from the parent-derived branch",
            "bound_condition": "if used, label nonfundamental and bound as phenomenology rather than theorem credit",
            "observable_links": "only the specific observable arena where the counterterm is introduced",
            "parent_input_needed": "parent derivation of the operator or explicit demotion to phenomenology",
            "current_status": "forbidden_for_theorem_credit_open_if_used",
            "valid_for_claim": "false",
        },
        {
            "component_id": "QXT620_6_total",
            "channel": "total qbar_XT source/test residual",
            "normalized_symbol": "qbar_XT_vec",
            "definition": "qbar_XT_vec := (b_g,b_theta,b_m,b_kappa,b_NH,b_EFT); qbar_XT_eff is an observable-dependent projection of this vector",
            "dimension_status": "dimensionless_vector",
            "zero_condition": "all six components theorem-zero, or the observable projection has a proven null vector",
            "bound_condition": "for each arena A, require abs(P_A qbar_XT_vec) <= epsilon_A or abs(K_X Qbar_XH P_A qbar_XT_vec) <= alpha_bound(lambda_X)",
            "observable_links": "R10; WEP; PPN; clocks; EM; orbital/local gravity",
            "parent_input_needed": "component zeros or numeric coefficient priors plus projection matrix",
            "current_status": "residual_envelope_derived_no_zero_promotion",
            "valid_for_claim": "false",
        },
    ]


def build_envelope_equation_rows() -> list[dict[str, object]]:
    return [
        {
            "equation_id": "EQ620_0_on_shell_chain_rule",
            "equation": "Lie_vX S_m,on-shell = int sqrt(-g)[0.5*T^ab*Lie_vX(hat_g_ab) + sum_A O_A*Lie_vX(theta_A) + O_m*Lie_vX(m) + J_XT_nonHilbert + delta_X L_EFT]",
            "assumptions": "matter equations of motion used; boundary terms either zero or routed to b_NH/edge residual; dependency basis inherited from 619",
            "meaning": "every qbar_XT failure mode is now a named component, not a hidden assumption",
            "claim_status": "identity_within_chosen_dependency_basis_nonclaim",
        },
        {
            "equation_id": "EQ620_1_dimensionless_projection",
            "equation": "qbar_XT_i := P_i[Lie_vX S_m,on-shell]/S_ref, with S_ref chosen from local Hilbert/coframe source normalization",
            "assumptions": "projection P_i and S_ref must be specified before numerical scoring",
            "meaning": "turns matter-sector residuals into dimensionless runner inputs",
            "claim_status": "template_only",
        },
        {
            "equation_id": "EQ620_2_total_vector",
            "equation": "qbar_XT_vec=(b_g,b_theta,b_m,b_kappa,b_NH,b_EFT), qbar_XT_eff(A)=P_A*qbar_XT_vec",
            "assumptions": "observable arena A supplies its projection vector P_A",
            "meaning": "local tests see projections, not necessarily the same scalar residual",
            "claim_status": "template_only",
        },
        {
            "equation_id": "EQ620_3_R10_bound_gate",
            "equation": "abs(alpha_X(lambda_X,A)) = abs(K_X(lambda_X)*Qbar_XH*P_R10(A)*qbar_XT_vec) <= alpha_bound(lambda_X)",
            "assumptions": "requires sourced K_X, Qbar_XH, lambda_X, bound curve, and projection coefficients",
            "meaning": "R10 cannot pass while K_X/Qbar_XH/qbar_XT inputs are placeholders",
            "claim_status": "blocked_until_numeric_parent_inputs",
        },
        {
            "equation_id": "EQ620_4_PPN_residual_vector",
            "equation": "r_PPN = M_PPN(lambda_X,L_system,environment)*qbar_XT_vec",
            "assumptions": "short-range Yukawa pieces may be exponentially suppressed, but constants or long-range components are not automatically suppressed",
            "meaning": "PPN pass requires either theorem zeros or an explicit range/projection suppression calculation",
            "claim_status": "blocked",
        },
        {
            "equation_id": "EQ620_5_local_GR_recovery_gate",
            "equation": "local_GR_recovery only if qbar_XT_vec=0 by theorem, or every observable projection is bounded below its arena threshold with baseline comparison",
            "assumptions": "must compare against GR/Newton/standard-model baselines where applicable",
            "meaning": "this is a scoring route, not a declaration route",
            "claim_status": "not_passed",
        },
    ]


def build_zero_or_bound_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "ZB620_0_metric_common",
            "component": "b_g",
            "derive_zero_route": "prove observed metric/coframe is a Q_MTS pullback with Lie_vX(hat_g)=0",
            "bound_route": "fit or bound common-frame coupling via R10/local gravity/PPN/clocks",
            "current_gate_status": "open",
            "failure_consequence": "universal fifth-force or PPN/local-gravity residual remains",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "ZB620_1_constants",
            "component": "b_theta",
            "derive_zero_route": "prove all ordinary constants are selector-trivial representation data",
            "bound_route": "use clock, spectra, alpha_EM, mass-ratio, and composition constraints",
            "current_gate_status": "open",
            "failure_consequence": "EM/time/particle sector residual remains",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "ZB620_2_marker",
            "component": "b_m",
            "derive_zero_route": "classify every marker as absent/gauge/source-independent auxiliary",
            "bound_route": "bound marker coupling with material-contrast source/test data",
            "current_gate_status": "open",
            "failure_consequence": "material-dependent fifth-force residual remains",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "ZB620_3_source_weight",
            "component": "b_kappa",
            "derive_zero_route": "derive one universal Hilbert/coframe source current and one kappa",
            "bound_route": "bound source weights by Eotvos and composition-dependent searches",
            "current_gate_status": "open",
            "failure_consequence": "WEP/composition branch remains exposed",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "ZB620_4_nonHilbert",
            "component": "b_NH",
            "derive_zero_route": "prove non-Hilbert currents absent/exact/zero-flux",
            "bound_route": "route to spin/torsion/topological/edge tests",
            "current_gate_status": "open",
            "failure_consequence": "non-Hilbert source residual remains",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "ZB620_5_readout_counterterm",
            "component": "b_EFT",
            "derive_zero_route": "ban post-readout counterterms from parent-derived theory",
            "bound_route": "if kept, demote to phenomenology and fit separately",
            "current_gate_status": "open_but_forbidden_for_theorem_credit",
            "failure_consequence": "public fundamental claim would be contaminated by post-hoc EFT",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "ZB620_6_total",
            "component": "qbar_XT_vec",
            "derive_zero_route": "all component derive-zero routes pass",
            "bound_route": "all arena projections pass with sourced coefficients",
            "current_gate_status": "not_passed",
            "failure_consequence": "local-GR reduction not claimed",
            "valid_for_claim": "false",
        },
    ]


def build_observable_projection_rows() -> list[dict[str, object]]:
    return [
        {
            "arena_id": "OBS620_0_R10_inverse_square",
            "test_arena": "short-range inverse-square/Yukawa tests",
            "projection": "P_R10*qbar_XT_vec enters alpha_X(lambda_X)",
            "sensitive_components": "b_g,b_m,b_kappa,b_NH depending on source/test materials and range",
            "baseline_comparator": "Newtonian/GR inverse-square baseline with experimental alpha_bound(lambda)",
            "required_data_or_derivation": "lambda_X; K_X(lambda); Qbar_XH; material projection P_R10; real bound curve",
            "current_status": "blocked_placeholders_only",
            "claim_allowed": "false",
        },
        {
            "arena_id": "OBS620_1_WEP_composition",
            "test_arena": "weak equivalence/composition tests",
            "projection": "composition differences project b_theta,b_m,b_kappa",
            "sensitive_components": "b_theta,b_m,b_kappa",
            "baseline_comparator": "universal free-fall GR baseline",
            "required_data_or_derivation": "composition charge model or theorem-zero for all nonuniversal components",
            "current_status": "open",
            "claim_allowed": "false",
        },
        {
            "arena_id": "OBS620_2_PPN_solar",
            "test_arena": "PPN/local solar-system gravity",
            "projection": "M_PPN(lambda_X,L_system)*qbar_XT_vec",
            "sensitive_components": "b_g and any long-range component; constants if environment-dependent",
            "baseline_comparator": "GR PPN gamma=beta=1 style baseline",
            "required_data_or_derivation": "range suppression calculation plus metric coupling normal form",
            "current_status": "open",
            "claim_allowed": "false",
        },
        {
            "arena_id": "OBS620_3_atomic_clocks",
            "test_arena": "clock/frequency/time-sector tests",
            "projection": "clock sensitivity coefficients dot b_theta plus possible b_g environment coupling",
            "sensitive_components": "b_theta,b_g",
            "baseline_comparator": "standard-model constants fixed in local GR",
            "required_data_or_derivation": "d ln alpha_EM/dX, d ln mass ratios/dX, environmental X profile",
            "current_status": "open",
            "claim_allowed": "false",
        },
        {
            "arena_id": "OBS620_4_EM_fine_structure",
            "test_arena": "EM/fine-structure sector",
            "projection": "alpha_EM and charge normalization derivatives inside b_theta",
            "sensitive_components": "b_theta",
            "baseline_comparator": "Maxwell/QED local fixed-coupling baseline",
            "required_data_or_derivation": "parent charge/EM coupling normal form or coefficient bound",
            "current_status": "open",
            "claim_allowed": "false",
        },
        {
            "arena_id": "OBS620_5_orbital_binary",
            "test_arena": "orbital systems and binary dynamics",
            "projection": "range- and source-dependent projection of b_g,b_kappa,b_NH",
            "sensitive_components": "b_g,b_kappa,b_NH",
            "baseline_comparator": "GR/Newtonian orbital baseline with residual precession/energy-loss checks",
            "required_data_or_derivation": "range, radiation channel, source charge, and environment profile",
            "current_status": "open",
            "claim_allowed": "false",
        },
    ]


def build_input_template_rows() -> list[dict[str, object]]:
    return [
        {
            "input_id": "IN620_0_b_g",
            "parameter": "b_g",
            "component": "QXT620_0_metric_common",
            "units": "dimensionless",
            "numeric_value": "MISSING_PARENT_INPUT",
            "source_path": "MISSING_PARENT_SOURCE",
            "derivation_status": "zero_or_bound_required",
            "valid_for_claim": "false",
            "failure_if_missing": "R10/PPN/common gravity residual cannot be scored",
        },
        {
            "input_id": "IN620_1_b_theta_alpha",
            "parameter": "d_ln_alpha_EM_dXhat",
            "component": "QXT620_1_constants",
            "units": "dimensionless",
            "numeric_value": "MISSING_PARENT_INPUT",
            "source_path": "MISSING_PARENT_SOURCE",
            "derivation_status": "zero_or_bound_required",
            "valid_for_claim": "false",
            "failure_if_missing": "EM/clock residual cannot be scored",
        },
        {
            "input_id": "IN620_2_b_theta_mass",
            "parameter": "d_ln_mass_ratio_dXhat",
            "component": "QXT620_1_constants",
            "units": "dimensionless",
            "numeric_value": "MISSING_PARENT_INPUT",
            "source_path": "MISSING_PARENT_SOURCE",
            "derivation_status": "zero_or_bound_required",
            "valid_for_claim": "false",
            "failure_if_missing": "mass/composition residual cannot be scored",
        },
        {
            "input_id": "IN620_3_b_m",
            "parameter": "marker_coupling_projection",
            "component": "QXT620_2_marker",
            "units": "dimensionless",
            "numeric_value": "MISSING_PARENT_INPUT",
            "source_path": "MISSING_PARENT_SOURCE",
            "derivation_status": "classify_or_bound_required",
            "valid_for_claim": "false",
            "failure_if_missing": "marker residual remains open",
        },
        {
            "input_id": "IN620_4_b_kappa",
            "parameter": "species_source_weight_splitting",
            "component": "QXT620_3_source_weight",
            "units": "dimensionless",
            "numeric_value": "MISSING_PARENT_INPUT",
            "source_path": "MISSING_PARENT_SOURCE",
            "derivation_status": "universal_source_theorem_or_bound_required",
            "valid_for_claim": "false",
            "failure_if_missing": "WEP/composition residual cannot be scored",
        },
        {
            "input_id": "IN620_5_b_NH",
            "parameter": "nonHilbert_current_projection",
            "component": "QXT620_4_nonHilbert",
            "units": "dimensionless",
            "numeric_value": "MISSING_PARENT_INPUT",
            "source_path": "MISSING_PARENT_SOURCE",
            "derivation_status": "current_decomposition_required",
            "valid_for_claim": "false",
            "failure_if_missing": "spin/torsion/edge residual remains open",
        },
        {
            "input_id": "IN620_6_b_EFT",
            "parameter": "post_readout_counterterm_projection",
            "component": "QXT620_5_readout_counterterm",
            "units": "dimensionless",
            "numeric_value": "FORBIDDEN_FOR_THEOREM_CREDIT",
            "source_path": "N/A",
            "derivation_status": "omit_or_demote_to_phenomenology",
            "valid_for_claim": "false",
            "failure_if_missing": "no failure; absence is preferred for field-theory claim",
        },
        {
            "input_id": "IN620_7_KQ_lambda",
            "parameter": "K_X_lambda_Qbar_XH_lambda_X",
            "component": "R10_alpha_gate",
            "units": "mixed_requires_schema",
            "numeric_value": "MISSING_PARENT_INPUT",
            "source_path": "MISSING_PARENT_SOURCE",
            "derivation_status": "required_before_R10_claim",
            "valid_for_claim": "false",
            "failure_if_missing": "alpha_X(lambda) cannot be compared to R10 bound",
        },
    ]


def build_decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D620_0_main_verdict",
            "status": STATUS,
            "decision": "derive qbar_XT residual envelope instead of zeroing qbar_XT",
            "meaning": "the on-shell chain rule turns the failed no-marker theorem into six explicit residual components",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D620_1_local_GR_status",
            "status": "local_GR_not_derived",
            "decision": "do not claim local GR recovery",
            "meaning": "local recovery now requires all six components zero-derived or bounded through observable projections",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D620_2_best_next_derivation",
            "status": "matter_coupling_normal_form_selected",
            "decision": "attack matter-coupling normal form before numerical priors",
            "meaning": "the cleanest route is to prove metric/coframe minimal coupling, constant triviality, and universal source current from the parent action",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D620_3_claim_ceiling",
            "status": CLAIM_CEILING,
            "decision": "no R10/WEP/PPN pass",
            "meaning": "input template intentionally contains MISSING_PARENT_INPUT markers and all claim flags are false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def build_route_rows() -> list[dict[str, object]]:
    return [
        {
            "route_id": "RU620_0_allowed",
            "allowed_after_620": "use qbar_XT_vec as the local source/test residual vector",
            "forbidden_after_620": "collapse the vector to zero without component proofs",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU620_1_allowed",
            "allowed_after_620": "score local tests using observable projections P_A once coefficients are sourced",
            "forbidden_after_620": "compare to R10/WEP/PPN while K_X, Qbar_XH, qbar components, or projections are placeholders",
            "next_action": "derive normal-form zeros first, then fill remaining priors",
        },
        {
            "route_id": "RU620_2_allowed",
            "allowed_after_620": "treat post-readout EFT as nonfundamental unless parent-derived",
            "forbidden_after_620": "use post-hoc counterterms as field-theory evidence",
            "next_action": "keep public/private claim ceiling explicit",
        },
    ]


def build_nonclaim_summary() -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "on_shell_residual_decomposition_derived": "true",
            "qbar_XT_zero_promoted": "false",
            "residual_components": "b_g,b_theta,b_m,b_kappa,b_NH,b_EFT",
            "numeric_coefficients_sourced": "false",
            "R10_pass": "false",
            "WEP_pass": "false",
            "PPN_pass": "false",
            "local_GR_pass": "false",
            "next_target": NEXT_TARGET,
        }
    ]


def build_validation_rows(
    source_register: list[dict[str, object]],
    residual_basis_rows: list[dict[str, object]],
    equation_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    observable_rows: list[dict[str, object]],
    input_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    nonclaim_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    missing_sources = [row["source_file"] for row in source_register if not parse_bool(row["exists"])]
    prior_path = OUT / "P8_Y5_BRR545_619_VALIDATION.csv"
    prior_rows = read_csv(prior_path) if prior_path.exists() else []
    prior_failures = [row for row in prior_rows if row.get("result") != "pass"]

    residual_components = {row["normalized_symbol"] for row in residual_basis_rows}
    required_components = {"b_g", "b_theta", "b_m", "b_kappa", "b_NH", "b_EFT", "qbar_XT_vec"}
    residual_basis_complete = required_components.issubset(residual_components)
    residual_rows_well_formed = all(row["zero_condition"] and row["bound_condition"] for row in residual_basis_rows)
    equation_ids = {row["equation_id"] for row in equation_rows}
    has_chain_rule = "EQ620_0_on_shell_chain_rule" in equation_ids
    total_gate = [row for row in gate_rows if row["gate_id"] == "ZB620_6_total"]
    arena_ids = {row["arena_id"] for row in observable_rows}
    required_arenas = {"OBS620_0_R10_inverse_square", "OBS620_1_WEP_composition", "OBS620_2_PPN_solar", "OBS620_3_atomic_clocks"}
    placeholders_safe = all(not parse_bool(row["valid_for_claim"]) for row in input_rows) and any(
        "MISSING_PARENT_INPUT" in str(row["numeric_value"]) for row in input_rows
    )
    all_nonclaim = all(not parse_bool(row.get("valid_for_claim", "false")) for row in residual_basis_rows + gate_rows + input_rows + decision_rows)
    nonclaim = nonclaim_rows[0]

    checks = [
        {
            "check_id": "V620_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": "missing=" + str(len(missing_sources)) + ("; " + json.dumps(missing_sources) if missing_sources else ""),
        },
        {
            "check_id": "V620_1_prior_619_clean",
            "result": "pass" if prior_path.exists() and not prior_failures else "fail",
            "detail": f"prior_exists={prior_path.exists()};prior_rows={len(prior_rows)};prior_failures={len(prior_failures)}",
        },
        {
            "check_id": "V620_2_residual_basis_complete",
            "result": "pass" if residual_basis_complete and residual_rows_well_formed else "fail",
            "detail": f"components={','.join(sorted(residual_components))};well_formed={residual_rows_well_formed}",
        },
        {
            "check_id": "V620_3_chain_rule_equation_present",
            "result": "pass" if has_chain_rule else "fail",
            "detail": "on-shell chain-rule decomposition included",
        },
        {
            "check_id": "V620_4_zero_or_bound_gate_total_blocks_claim",
            "result": "pass" if total_gate and total_gate[0]["current_gate_status"] == "not_passed" else "fail",
            "detail": f"total_gate_status={total_gate[0]['current_gate_status'] if total_gate else 'missing'}",
        },
        {
            "check_id": "V620_5_observable_matrix_core_arenas",
            "result": "pass" if required_arenas.issubset(arena_ids) else "fail",
            "detail": f"arenas={','.join(sorted(arena_ids))}",
        },
        {
            "check_id": "V620_6_input_placeholders_safe",
            "result": "pass" if placeholders_safe else "fail",
            "detail": "MISSING_PARENT_INPUT rows are nonclaim placeholders",
        },
        {
            "check_id": "V620_7_all_claim_flags_false",
            "result": "pass" if all_nonclaim else "fail",
            "detail": f"all_valid_for_claim_false={all_nonclaim}",
        },
        {
            "check_id": "V620_8_no_local_claim",
            "result": "pass"
            if nonclaim["R10_pass"] == "false"
            and nonclaim["WEP_pass"] == "false"
            and nonclaim["PPN_pass"] == "false"
            and nonclaim["local_GR_pass"] == "false"
            and nonclaim["qbar_XT_zero_promoted"] == "false"
            else "fail",
            "detail": "qbar_XT_zero=false;R10=false;WEP=false;PPN=false;local_GR=false",
        },
    ]
    return checks


def write_doc(
    source_register: list[dict[str, object]],
    residual_basis_rows: list[dict[str, object]],
    equation_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    observable_rows: list[dict[str, object]],
    input_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    route_rows: list[dict[str, object]],
    nonclaim_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    generated = utc_now()
    content = f"""# 620 Y5 R10 qbarXT residual envelope after no-marker failure

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`

## Verdict
- The 619 no-marker route did not close `qbar_XT=0`, but it gave us the right dependency basis.
- 620 derives the exact on-shell residual envelope: whatever ordinary matter can still source along the local `X` branch must enter through common metric/coframe readout, constants, material markers, source weights, non-Hilbert currents, or post-readout EFT.
- This is not a local-GR pass. It is better than that fake comfort: it is a pressure map. Every missing theorem is now a named coefficient that can be killed by derivation or bounded by data.
- The next best move is not immediate numerics. It is a matter-coupling normal-form theorem attempt, because killing `b_g`, `b_theta`, and `b_kappa` analytically would shrink the local problem the most.

## Derived Envelope
Start with an enlarged matter dependency basis after 619:

```text
S_m = S_m[Psi, hat_g(Q,X), theta(X), m(X), J_nonHilbert(X), L_EFT_after_readout(X)]
```

On shell for the matter fields, the chain rule gives:

```text
Lie_vX S_m =
int sqrt(-g) [
  0.5 T^ab Lie_vX(hat_g_ab)
  + sum_A O_A Lie_vX(theta_A)
  + O_m Lie_vX(m)
  + J_XT_nonHilbert
  + delta_X L_EFT_after_readout
]
```

Projecting and normalizing this identity defines:

```text
qbar_XT_vec = (b_g, b_theta, b_m, b_kappa, b_NH, b_EFT)
qbar_XT_eff(A) = P_A qbar_XT_vec
```

So the strict local-GR route is:

```text
qbar_XT_vec = 0 by theorem
```

and the empirical survival route is:

```text
abs(P_A qbar_XT_vec) <= epsilon_A
```

for every relevant local arena `A`, with R10 using:

```text
abs(K_X(lambda_X) Qbar_XH P_R10 qbar_XT_vec) <= alpha_bound(lambda_X)
```

No placeholders are allowed to masquerade as a pass.

## Source Register
{md_table(source_register)}

## Residual Basis
{md_table(residual_basis_rows)}

## Envelope Equations
{md_table(equation_rows)}

## Zero Or Bound Gate
{md_table(gate_rows)}

## Observable Projection Matrix
{md_table(observable_rows)}

## Input Template
{md_table(input_rows)}

## Decision
{md_table(decision_rows)}

## Route Update
{md_table(route_rows)}

## Nonclaim Summary
{md_table(nonclaim_rows)}

## Validation
{md_table(validation_rows)}

## Practical Read
This is a real improvement. We have not proven local GR, but we have stopped treating the missing matter coupling theorem as fog. The fog is now six boxes. If 621 can prove the normal-form clauses, several boxes disappear. If not, they become coefficient priors for fair R10/WEP/PPN/clock scoring.
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    source_register = build_source_register()
    residual_basis_rows = build_residual_basis_rows()
    equation_rows = build_envelope_equation_rows()
    gate_rows = build_zero_or_bound_gate_rows()
    observable_rows = build_observable_projection_rows()
    input_rows = build_input_template_rows()
    decision_rows = build_decision_rows()
    route_rows = build_route_rows()
    nonclaim_rows = build_nonclaim_summary()
    validation_rows = build_validation_rows(
        source_register,
        residual_basis_rows,
        equation_rows,
        gate_rows,
        observable_rows,
        input_rows,
        decision_rows,
        nonclaim_rows,
    )

    outputs = [
        ("P8_Y5_R10_620_SOURCE_REGISTER.csv", source_register),
        ("P8_Y5_R10_620_RESIDUAL_BASIS.csv", residual_basis_rows),
        ("P8_Y5_R10_620_ENVELOPE_EQUATIONS.csv", equation_rows),
        ("P8_Y5_R10_620_ZERO_OR_BOUND_GATE.csv", gate_rows),
        ("P8_Y5_R10_620_OBSERVABLE_PROJECTION_MATRIX.csv", observable_rows),
        ("P8_Y5_R10_620_INPUT_TEMPLATE.csv", input_rows),
        ("P8_Y5_BRR545_620_DECISION.csv", decision_rows),
        ("P8_Y5_BRR545_620_ROUTE_UPDATE.csv", route_rows),
        ("P8_Y5_R10_620_NONCLAIM_SUMMARY.csv", nonclaim_rows),
        ("P8_Y5_BRR545_620_VALIDATION.csv", validation_rows),
    ]
    for filename, rows in outputs:
        write_csv(OUT / filename, rows)

    write_doc(
        source_register,
        residual_basis_rows,
        equation_rows,
        gate_rows,
        observable_rows,
        input_rows,
        decision_rows,
        route_rows,
        nonclaim_rows,
        validation_rows,
    )

    failed = [row for row in validation_rows if row["result"] != "pass"]
    print(json.dumps({"status": STATUS, "doc": str(DOC), "failed_checks": failed}, indent=2))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

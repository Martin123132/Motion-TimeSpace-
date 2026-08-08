from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MTS_DIR = ROOT / "source-intake" / "mts_residuals"
EXTERNAL_DIR = ROOT / "source-intake" / "external_papers"

DOC = ROOT / "638-Y5-R10-constant-sector-zero-or-finite-beta-derivation.md"
SCRIPT = ROOT / "scripts" / "Y5_R10_constant_sector_zero_or_finite_beta_derivation.py"

STATUS = "Y5_R10_constant_sector_zero_derivation_partially_succeeds_dimensionless_channels_become_finite_beta_contract"
CLAIM_CEILING = "constant_sector_derivation_and_symbolic_beta_laws_only_no_cg_zero_R10_WEP_PPN_clock_or_local_GR_pass"
NEXT_TARGET = "639-Y5-R10-finite-constant-beta-local-bound-matrix-runner.md"

PRIOR_637_DOC = ROOT / "637-Y5-R10-parent-action-quotient-map-and-constant-ownership-derivation.md"
PRIOR_637_VALIDATION = MTS_DIR / "P8_Y5_BRR545_637_VALIDATION.csv"
PRIOR_637_CONSTANT_THEOREM = MTS_DIR / "P8_Y5_R10_637_CONSTANT_OWNERSHIP_THEOREM.csv"
PRIOR_637_CONSTANT_STATUS = MTS_DIR / "P8_Y5_R10_637_CONSTANT_STATUS_UPDATE.csv"
PRIOR_637_FINITE = MTS_DIR / "P8_Y5_R10_637_FINITE_BRANCH_UPDATE.csv"
PRIOR_637_SUMMARY = MTS_DIR / "P8_Y5_R10_637_NONCLAIM_SUMMARY.csv"
PRIOR_360_DOC = ROOT / "360-universal-matter-coupling-theorem-attempt.md"
PRIOR_410_DOC = ROOT / "410-quotient-matter-functor-theorem-attempt.md"
PRIOR_565_DOC = ROOT / "565-Y5-R10-coframe-pullback-zero-or-finite-alpha-coefficient.md"
PRIOR_566_DOC = ROOT / "566-Y5-R10-primitive-quotient-no-marker-parent-clause-or-alpha-coefficient-fill.md"
CHARGE_CONTRACT = EXTERNAL_DIR / "Andersen_2026_phase_current_CHARGE_CONTRACT.csv"

SOURCE_REGISTER = MTS_DIR / "P8_Y5_R10_638_SOURCE_REGISTER.csv"
ZERO_ROUTE_ATTEMPT = MTS_DIR / "P8_Y5_R10_638_CONSTANT_ZERO_ROUTE_ATTEMPT.csv"
DIMENSIONLESS_GATE = MTS_DIR / "P8_Y5_R10_638_DIMENSIONLESS_OBSERVABLE_GATE.csv"
FINITE_BETA_LAWS = MTS_DIR / "P8_Y5_R10_638_FINITE_BETA_LAWS.csv"
ARENA_PROJECTION = MTS_DIR / "P8_Y5_R10_638_ARENA_PROJECTION_MATRIX.csv"
CONSTANT_VERDICT = MTS_DIR / "P8_Y5_R10_638_CONSTANT_VERDICT.csv"
ADOPTION_GATE = MTS_DIR / "P8_Y5_R10_638_ADOPTION_GATE.csv"
DECISION = MTS_DIR / "P8_Y5_BRR545_638_DECISION.csv"
NEXT_CONTRACT = MTS_DIR / "P8_Y5_R10_638_NEXT_CONTRACT.csv"
NONCLAIM_SUMMARY = MTS_DIR / "P8_Y5_R10_638_NONCLAIM_SUMMARY.csv"
VALIDATION = MTS_DIR / "P8_Y5_BRR545_638_VALIDATION.csv"


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


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
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (PRIOR_637_DOC, "immediate 637 checkpoint"),
        (PRIOR_637_VALIDATION, "637 validation gate"),
        (PRIOR_637_CONSTANT_THEOREM, "637 constant descent theorem"),
        (PRIOR_637_CONSTANT_STATUS, "637 constant status update"),
        (PRIOR_637_FINITE, "637 finite branch update"),
        (PRIOR_637_SUMMARY, "637 nonclaim summary"),
        (PRIOR_360_DOC, "universal matter coupling constant hazards"),
        (PRIOR_410_DOC, "quotient matter functor constant blocker"),
        (PRIOR_565_DOC, "vertical observation constant premise"),
        (PRIOR_566_DOC, "primitive quotient no-marker blocker"),
        (CHARGE_CONTRACT, "charge/EM topological contract warning"),
        (SCRIPT, "this checkpoint generator"),
    ]
    return [
        {
            "source_id": f"SRC638_{index}",
            "source_path": rel(path),
            "exists": bool_text(path.exists()),
            "role": role,
            "valid_for_claim": "false",
        }
        for index, (path, role) in enumerate(sources)
    ]


def zero_route_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "constant_id": "ZR638_0_c_light",
            "object": "c",
            "zero_route": "owned by observed causal cone E_obs plus unit convention",
            "derivation_result": "conditional_repair",
            "reason": "a dimensionful speed can be fixed by the observed metric/coframe and units; no independent scalar c(Xhat) is needed",
            "what_still_blocks": "disformal shadow cone or non-E_obs clock map would reopen PPN/clock residuals",
            "finite_if_fail": "tau_clock;gamma_minus_1;disformal_residual",
            "valid_for_claim": "false",
        },
        {
            "constant_id": "ZR638_1_alpha_EM",
            "object": "alpha_EM, e, gauge coupling",
            "zero_route": "topological/representation ownership or quotient-descended gauge kinetic data",
            "derivation_result": "not_derived_open",
            "reason": "charge quantization/topological current would help, but the parent action has not derived Maxwell limit, gauge coupling normalization, or alpha_EM as vertical-silent",
            "what_still_blocks": "alpha_EM is dimensionless, so unit rescaling cannot hide d ln alpha_EM/dXhat",
            "finite_if_fail": "kappa_alpha=d_ln_alpha_EM_dXhat;tau_clock;tau_WEP;EM_spectra",
            "valid_for_claim": "false",
        },
        {
            "constant_id": "ZR638_2_particle_masses",
            "object": "m_A, mass ratios, Yukawa/binding data",
            "zero_route": "fixed matter representation data or quotient-owned mass spectrum",
            "derivation_result": "not_derived_open",
            "reason": "dimensionful masses alone can be unit-scaled, but mass ratios and composition-dependent binding fractions are observable",
            "what_still_blocks": "no parent derivation of mass spectrum, binding energy fractions, or universal unit-only variation",
            "finite_if_fail": "kappa_mA=d_ln_mA_dXhat;beta_A;composition_sensitivity",
            "valid_for_claim": "false",
        },
        {
            "constant_id": "ZR638_3_clock_transitions",
            "object": "nu_clock, Rydberg, hyperfine/nuclear transitions",
            "zero_route": "derived from quotient-owned alpha_EM and mass/nuclear ratios",
            "derivation_result": "not_independently_closed",
            "reason": "clock ratios inherit alpha_EM and mass-ratio sensitivities; they are not silenced by metric descent alone",
            "what_still_blocks": "clock comparisons measure dimensionless ratios and gradients",
            "finite_if_fail": "kappa_clock_i=d_ln_nu_i_dXhat;tau_clock",
            "valid_for_claim": "false",
        },
        {
            "constant_id": "ZR638_4_species_labels",
            "object": "species/isotope labels and preparation data",
            "zero_route": "discrete representation labels are locally vertical-silent",
            "derivation_result": "partial_only",
            "reason": "integer labels do not vary smoothly under local Xhat, but source density, isotope fractions, and preparation normalization can still carry Xhat",
            "what_still_blocks": "material preparation variables need a no-marker theorem",
            "finite_if_fail": "beta_source;beta_test;WEP_charge_vector",
            "valid_for_claim": "false",
        },
        {
            "constant_id": "ZR638_5_measured_GM",
            "object": "G_N, GM, source normalization",
            "zero_route": "not a matter constant; must be owned by EH/PPN/source-normalization branch",
            "derivation_result": "not_closed_here",
            "reason": "measured GM is a local gravity/operator observable, not fixed by constant descent",
            "what_still_blocks": "source normalization and EH-only exterior remain separate debts",
            "finite_if_fail": "delta_GM;source_normalization_residual;PPN_vector",
            "valid_for_claim": "false",
        },
    ]


def dimensionless_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "DG638_0_dimensionful_unit_warning",
            "statement": "A dimensionful constant can be made silent only as a unit/readout convention; this is not by itself an observable zero theorem.",
            "consequence": "do not score d c/dXhat or d m/dXhat alone without reducing to dimensionless ratios or beta charges",
            "result": "pass_guardrail",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "DG638_1_dimensionless_observable_rule",
            "statement": "Any nonzero vertical derivative of a dimensionless observable is physical unless it is quotient-descended or topological.",
            "consequence": "alpha_EM, mass ratios, clock ratios, and composition sensitivities must be zero-proven or carried as finite beta/tau inputs",
            "result": "core_rule",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "DG638_2_topological_discrete_escape",
            "statement": "Integer/winding/representation labels are locally silent under smooth vertical variation, but only after the parent action derives the relevant compact/topological sector.",
            "consequence": "charge/species discreteness can help, but cannot be used as a public EM or local-GR proof yet",
            "result": "conditional_escape",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "DG638_3_marker_failure_rule",
            "statement": "If a material marker theta_A(Xhat) changes a dimensionless observable, it is not hidden; it is a finite matter coupling.",
            "consequence": "failed zero proofs become beta/tau rows rather than rhetorical closures",
            "result": "finite_branch_trigger",
            "valid_for_claim": "false",
        },
    ]


def finite_beta_law_rows() -> list[dict[str, Any]]:
    return [
        {
            "law_id": "BL638_0_constant_vector",
            "symbol": "kappa_i",
            "definition": "kappa_i := d ln C_i / dXhat for each dimensionless constant C_i in {alpha_EM, mass ratios, binding fractions, clock ratios}",
            "units": "per_Xhat_unit",
            "source_status": "symbolic_not_numeric",
            "needed_source": "parent constant-sector variation or theorem-zero descent",
            "valid_for_claim": "false",
        },
        {
            "law_id": "BL638_1_body_charge",
            "symbol": "beta_A",
            "definition": "beta_A := d ln m_A / dXhat = sum_i S_Ai kappa_i plus any source/preparation marker derivative",
            "units": "dimensionless_per_Xhat_unit",
            "source_status": "symbolic_not_numeric",
            "needed_source": "composition sensitivities S_Ai and parent kappa_i values",
            "valid_for_claim": "false",
        },
        {
            "law_id": "BL638_2_R10_two_leg",
            "symbol": "alpha_X(lambda)",
            "definition": "alpha_X(lambda) = tau_R10(lambda) beta_source beta_test / Z_eff, or zero if either beta leg is theorem-zero",
            "units": "dimensionless",
            "source_status": "symbolic_not_numeric",
            "needed_source": "beta_source,beta_test,Z_eff,lambda_X,tau_R10 and validated alpha_bound(lambda)",
            "valid_for_claim": "false",
        },
        {
            "law_id": "BL638_3_clock_sensitivity",
            "symbol": "d ln nu_a/dXhat",
            "definition": "d ln nu_a/dXhat = sum_i K_ai kappa_i, and clock-ratio drift uses differences K_ai-K_bi",
            "units": "per_Xhat_unit",
            "source_status": "symbolic_not_numeric",
            "needed_source": "clock sensitivity coefficients and kappa_i values",
            "valid_for_claim": "false",
        },
        {
            "law_id": "BL638_4_WEP_vector",
            "symbol": "eta_AB",
            "definition": "eta_AB pressure scales with beta_source times (beta_A-beta_B), plus any arena-specific tau_WEP normalization",
            "units": "dimensionless",
            "source_status": "symbolic_not_numeric",
            "needed_source": "source composition, test-body beta vectors, tau_WEP and experimental bound map",
            "valid_for_claim": "false",
        },
        {
            "law_id": "BL638_5_source_normalization",
            "symbol": "delta_GM",
            "definition": "delta(GM)/GM is retained as an operator/source-normalization residual, not folded into c_g=0",
            "units": "dimensionless",
            "source_status": "symbolic_not_numeric",
            "needed_source": "EH/PPN/source-normalization derivation",
            "valid_for_claim": "false",
        },
    ]


def arena_projection_rows() -> list[dict[str, Any]]:
    return [
        {
            "arena_id": "AP638_0_R10",
            "arena": "short-range fifth force",
            "constant_failure_input": "beta_source,beta_test,Z_eff,lambda_X,tau_R10",
            "projection_law": "alpha_X(lambda)=tau_R10 beta_source beta_test/Z_eff",
            "current_status": "source_ready_not_scoreable",
            "valid_for_claim": "false",
        },
        {
            "arena_id": "AP638_1_WEP",
            "arena": "composition/free-fall",
            "constant_failure_input": "kappa_i,S_Ai,S_Bi,beta_source,tau_WEP",
            "projection_law": "eta_AB ~ tau_WEP beta_source sum_i(S_Ai-S_Bi)kappa_i",
            "current_status": "source_ready_not_scoreable",
            "valid_for_claim": "false",
        },
        {
            "arena_id": "AP638_2_clocks",
            "arena": "clock comparisons/redshift",
            "constant_failure_input": "kappa_i,K_ai,K_bi,tau_clock",
            "projection_law": "d ln(nu_a/nu_b)/dXhat=sum_i(K_ai-K_bi)kappa_i",
            "current_status": "source_ready_not_scoreable",
            "valid_for_claim": "false",
        },
        {
            "arena_id": "AP638_3_EM_spectra",
            "arena": "EM/fine-structure",
            "constant_failure_input": "kappa_alpha and gauge/charge parent normalization",
            "projection_law": "spectral shifts follow alpha_EM sensitivity; Maxwell/charge branch remains separate from local-GR gate",
            "current_status": "source_ready_not_scoreable",
            "valid_for_claim": "false",
        },
        {
            "arena_id": "AP638_4_PPN",
            "arena": "weak-field metric/PPN",
            "constant_failure_input": "delta_GM, universal scalar residue, disformal residue, non-EH operator vector",
            "projection_law": "gamma_minus_1,beta_minus_1 are operator-frame residuals, not closed by constant zero alone",
            "current_status": "separate_GR_debt",
            "valid_for_claim": "false",
        },
        {
            "arena_id": "AP638_5_orbital",
            "arena": "orbital/source normalization",
            "constant_failure_input": "delta_GM, beta_source, range/profile",
            "projection_law": "orbital residual = source-normalization residual plus any finite-range beta contribution",
            "current_status": "source_ready_not_scoreable",
            "valid_for_claim": "false",
        },
    ]


def constant_verdict_rows() -> list[dict[str, Any]]:
    return [
        {
            "verdict_id": "CV638_0_c_light",
            "object": "c",
            "status_after_638": "conditional_zero_route_available",
            "why": "causal cone/unit ownership can silence independent c variation if E_obs is parent-owned",
            "blocks_zero_clause": "true",
            "valid_for_claim": "false",
        },
        {
            "verdict_id": "CV638_1_alpha_EM",
            "object": "alpha_EM/e",
            "status_after_638": "finite_beta_required_unless_topological_parent_proof",
            "why": "dimensionless and not derived as quotient/topological",
            "blocks_zero_clause": "true",
            "valid_for_claim": "false",
        },
        {
            "verdict_id": "CV638_2_masses",
            "object": "mass ratios/composition",
            "status_after_638": "finite_beta_required_unless_mass_spectrum_parent_proof",
            "why": "mass ratios and binding fractions are observable and composition sensitive",
            "blocks_zero_clause": "true",
            "valid_for_claim": "false",
        },
        {
            "verdict_id": "CV638_3_clocks",
            "object": "clock ratios",
            "status_after_638": "finite_tau_required_if_underlying_constants_open",
            "why": "clock ratios inherit alpha/mass/nuclear sensitivities",
            "blocks_zero_clause": "true",
            "valid_for_claim": "false",
        },
        {
            "verdict_id": "CV638_4_species_labels",
            "object": "species labels/preparation",
            "status_after_638": "discrete_labels_partly_safe_preparation_open",
            "why": "integer labels are locally silent, but material/source preparation can still carry markers",
            "blocks_zero_clause": "true",
            "valid_for_claim": "false",
        },
        {
            "verdict_id": "CV638_5_measured_GM",
            "object": "G_N/GM",
            "status_after_638": "separate_operator_source_normalization_debt",
            "why": "not solved by matter constant descent",
            "blocks_zero_clause": "true",
            "valid_for_claim": "false",
        },
    ]


def adoption_gate_rows(verdict_rows: list[dict[str, Any]], beta_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    blockers = [row for row in verdict_rows if row.get("blocks_zero_clause") == "true"]
    numeric_beta_rows = [row for row in beta_rows if row.get("source_status") == "numeric_sourced"]
    return [
        {
            "gate_id": "AG638_0_constant_derivation_attempted",
            "requirement": "six constant families audited for zero or finite beta route",
            "result": "pass" if len(verdict_rows) == 6 else "fail",
            "detail": f"verdict_rows={len(verdict_rows)}",
            "adoption_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "AG638_1_constants_zero_closed",
            "requirement": "no constant family blocks zero clause",
            "result": "blocked",
            "detail": f"blocking_constant_families={len(blockers)}",
            "adoption_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "AG638_2_finite_beta_scoreable",
            "requirement": "finite beta laws have numeric parent-sourced kappa/beta/tau inputs",
            "result": "blocked",
            "detail": f"numeric_beta_rows={len(numeric_beta_rows)};all_beta_rows_symbolic=true",
            "adoption_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "AG638_3_claim_status",
            "requirement": "no local claim from symbolic constant beta laws",
            "result": "pass",
            "detail": "c_g_zero_claimed=false;finite_branch_scoreable=false;local_GR=false",
            "adoption_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D638_0_main_verdict",
            "decision": STATUS,
            "meaning": "constant-zero derivation partly works for unit/quotient/discrete cases, but dimensionless alpha/mass/clock channels remain finite beta contracts",
            "status": "partial_derivation_not_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D638_1_key_rule",
            "decision": "dimensionless_constants_cannot_hide",
            "meaning": "alpha_EM, mass ratios, and clock ratios must be zero-proven or explicitly bounded",
            "status": "core_rule",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D638_2_finite_route",
            "decision": "symbolic_beta_laws_written",
            "meaning": "failed zero channels now map to kappa_i, beta_A, tau_R10, tau_WEP, tau_clock, and source-normalization rows",
            "status": "source_ready_not_numeric",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D638_3_claim_ceiling",
            "decision": CLAIM_CEILING,
            "meaning": "no R10/WEP/clock/PPN/local-GR pass until constants are parent-zero or finite inputs are numeric and source-backed",
            "status": "hard_guardrail",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def next_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "NC638_0_numeric_beta_matrix",
            "required_output": "build a local bound matrix with symbolic-to-numeric slots for kappa_alpha,kappa_mass,beta_source,beta_test,tau_R10,tau_WEP,tau_clock",
            "success_condition": "every finite constant channel has units, owner equation, and local arena projection",
            "if_success": "private local bound scoring can begin",
            "if_fail": "finite branch remains source-ready but unscoreable",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "NC638_1_charge_topology_attempt",
            "required_output": "try deriving alpha_EM/e charge ownership from compact phase, Noether current, quantized charge unit, and Maxwell limit",
            "success_condition": "charge/gauge coupling becomes quotient/topological rather than empirical marker",
            "if_success": "alpha_EM blocker may close conditionally",
            "if_fail": "kappa_alpha remains finite beta input",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "NC638_2_mass_clock_attempt",
            "required_output": "try deriving mass ratios and clock ratios as quotient-owned representation data or convert to sensitivities",
            "success_condition": "no composition/clock spurion survives",
            "if_success": "WEP/clock blockers may close conditionally",
            "if_fail": "WEP/clock pressure matrix is mandatory",
            "valid_for_claim": "false",
        },
    ]


def nonclaim_summary_rows(verdict_rows: list[dict[str, Any]], beta_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    blockers = [row for row in verdict_rows if row.get("blocks_zero_clause") == "true"]
    symbolic_beta = [row for row in beta_rows if row.get("source_status") == "symbolic_not_numeric"]
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "constant_zero_families_closed_for_claim": 0,
            "conditional_or_partial_zero_routes": 2,
            "blocking_constant_families": len(blockers),
            "symbolic_beta_laws": len(symbolic_beta),
            "finite_branch_scoreable": "false",
            "zero_clause_adopted": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        }
    ]


def validation_rows(
    source_rows: list[dict[str, Any]],
    zero_rows: list[dict[str, Any]],
    dimensionless_rows: list[dict[str, Any]],
    beta_rows: list[dict[str, Any]],
    arena_rows: list[dict[str, Any]],
    verdict_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    contract_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = [row for row in source_rows if row.get("exists") != "true"]
    prior_rows = read_csv(PRIOR_637_VALIDATION)
    prior_fails = [row for row in prior_rows if row.get("result") != "pass"]
    claim_rows = [
        row
        for group in (zero_rows, dimensionless_rows, beta_rows, arena_rows, verdict_rows, gate_rows)
        for row in group
        if row.get("valid_for_claim") == "true"
    ]
    not_derived = [row for row in zero_rows if "not_derived" in row.get("derivation_result", "")]
    blockers = [row for row in verdict_rows if row.get("blocks_zero_clause") == "true"]
    symbolic_beta = [row for row in beta_rows if row.get("source_status") == "symbolic_not_numeric"]
    adoption_allowed = any(row.get("adoption_allowed") == "true" for row in gate_rows)
    return [
        {
            "check_id": "V638_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V638_1_prior_637_clean",
            "result": "pass" if prior_rows and not prior_fails else "fail",
            "detail": f"prior_rows={len(prior_rows)};prior_fails={len(prior_fails)}",
        },
        {
            "check_id": "V638_2_zero_route_audit_complete",
            "result": "pass" if len(zero_rows) == 6 and len(not_derived) >= 2 else "fail",
            "detail": f"zero_rows={len(zero_rows)};not_derived={len(not_derived)}",
        },
        {
            "check_id": "V638_3_dimensionless_gate_written",
            "result": "pass" if len(dimensionless_rows) == 4 else "fail",
            "detail": f"dimensionless_rows={len(dimensionless_rows)}",
        },
        {
            "check_id": "V638_4_beta_laws_symbolic_nonclaim",
            "result": "pass" if len(beta_rows) == 6 and len(symbolic_beta) >= 5 else "fail",
            "detail": f"beta_rows={len(beta_rows)};symbolic_beta={len(symbolic_beta)}",
        },
        {
            "check_id": "V638_5_arena_projection_complete",
            "result": "pass" if len(arena_rows) == 6 else "fail",
            "detail": f"arena_rows={len(arena_rows)}",
        },
        {
            "check_id": "V638_6_constant_verdict_blocks_claim",
            "result": "pass" if len(verdict_rows) == 6 and len(blockers) == 6 else "fail",
            "detail": f"verdict_rows={len(verdict_rows)};blockers={len(blockers)}",
        },
        {
            "check_id": "V638_7_adoption_blocked",
            "result": "pass" if len(gate_rows) == 4 and not adoption_allowed else "fail",
            "detail": f"gate_rows={len(gate_rows)};adoption_allowed={bool_text(adoption_allowed)}",
        },
        {
            "check_id": "V638_8_next_contract_written",
            "result": "pass" if len(contract_rows) == 3 else "fail",
            "detail": f"contract_rows={len(contract_rows)}",
        },
        {
            "check_id": "V638_9_no_claim_rows",
            "result": "pass" if not claim_rows else "fail",
            "detail": f"claim_rows={len(claim_rows)}",
        },
        {
            "check_id": "V638_10_no_local_claim",
            "result": "pass",
            "detail": "constant_zero_claimed=false;c_g_zero_claimed=false;finite_branch_scoreable=false;R10=false;WEP=false;PPN=false;clock=false;orbital=false;local_GR=false",
        },
    ]


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "\n"
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines) + "\n"


def write_doc(
    source_rows: list[dict[str, Any]],
    zero_rows: list[dict[str, Any]],
    dimensionless_rows: list[dict[str, Any]],
    beta_rows: list[dict[str, Any]],
    arena_rows: list[dict[str, Any]],
    verdict_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    contract_rows: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = "\n".join(
        [
            "# 638 Y5 R10 constant sector zero or finite beta derivation",
            "",
            f"Status: `{STATUS}`  ",
            f"Claim ceiling: `{CLAIM_CEILING}`  ",
            f"Next target: `{NEXT_TARGET}`",
            "",
            "## Verdict",
            "- The constant-zero route partly works for unit/readout and discrete-label cases, but it does not close the local branch.",
            "- The hard rule is now explicit: dimensionless constants cannot be hidden by unit convention.",
            "- `alpha_EM`, mass ratios, clock ratios, composition sensitivities, and measured `GM` must either be parent-zero/topological or become finite beta/tau inputs.",
            "- Therefore the zero branch remains blocked; the finite branch is now symbolically structured but not numerically scoreable.",
            "",
            "## Derivation Core",
            "From 637, the matter variation after quotient descent has the form",
            "",
            "`delta_v S_matter = (delta Sbar_m/dE_obs) DObs(Dq[v]) + (partial Sbar_m/partial theta_A) delta_v theta_A`.",
            "",
            "The first term is killed by vertical quotient descent. The second term is killed only if each `theta_A` is fixed representation data or descends to the quotient. If a dimensionless `theta_A` varies with `Xhat`, it is an observable finite coupling, not a harmless convention.",
            "",
            "The finite fallback is therefore not arbitrary:",
            "",
            "`kappa_i = d ln C_i / dXhat`,",
            "",
            "`beta_A = sum_i S_Ai kappa_i + marker_A`,",
            "",
            "`alpha_X(lambda) = tau_R10(lambda) beta_source beta_test / Z_eff`.",
            "",
            "That gives the correct source/test two-leg structure while keeping R10, WEP, clocks, EM, PPN, and orbital tests tied to the same constant-sector failure vector.",
            "",
            "## Source Register",
            markdown_table(source_rows),
            "## Constant Zero Route Attempt",
            markdown_table(zero_rows),
            "## Dimensionless Observable Gate",
            markdown_table(dimensionless_rows),
            "## Finite Beta Laws",
            markdown_table(beta_rows),
            "## Arena Projection Matrix",
            markdown_table(arena_rows),
            "## Constant Verdict",
            markdown_table(verdict_rows),
            "## Adoption Gate",
            markdown_table(gate_rows),
            "## Decision",
            markdown_table(decision),
            "## Next Contract",
            markdown_table(contract_rows),
            "## Nonclaim Summary",
            markdown_table(summary),
            "## Validation",
            markdown_table(validation),
            "## Interpretation",
            "This is a good tightening step. It prevents the local branch from cheating by calling dimensionless physics a unit choice. If charge and mass data are topological/quotient-owned, the zero branch gets much stronger. If not, we now have the right symbolic beta machinery to test the surviving coupling instead of guessing.",
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    zero_rows = zero_route_attempt_rows()
    dimensionless_rows = dimensionless_gate_rows()
    beta_rows = finite_beta_law_rows()
    arena_rows = arena_projection_rows()
    verdict_rows = constant_verdict_rows()
    gate_rows = adoption_gate_rows(verdict_rows, beta_rows)
    decision = decision_rows()
    contract_rows = next_contract_rows()
    summary = nonclaim_summary_rows(verdict_rows, beta_rows)
    validation = validation_rows(
        source_rows,
        zero_rows,
        dimensionless_rows,
        beta_rows,
        arena_rows,
        verdict_rows,
        gate_rows,
        contract_rows,
    )

    write_csv(SOURCE_REGISTER, source_rows)
    write_csv(ZERO_ROUTE_ATTEMPT, zero_rows)
    write_csv(DIMENSIONLESS_GATE, dimensionless_rows)
    write_csv(FINITE_BETA_LAWS, beta_rows)
    write_csv(ARENA_PROJECTION, arena_rows)
    write_csv(CONSTANT_VERDICT, verdict_rows)
    write_csv(ADOPTION_GATE, gate_rows)
    write_csv(DECISION, decision)
    write_csv(NEXT_CONTRACT, contract_rows)
    write_csv(NONCLAIM_SUMMARY, summary)
    write_csv(VALIDATION, validation)
    write_doc(
        source_rows,
        zero_rows,
        dimensionless_rows,
        beta_rows,
        arena_rows,
        verdict_rows,
        gate_rows,
        decision,
        contract_rows,
        summary,
        validation,
    )

    failed = [row for row in validation if row["result"] != "pass"]
    print(
        json.dumps(
            {
                "status": STATUS,
                "doc": str(DOC),
                "failed_checks": failed,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

STATUS = "Y5_R10_891_finite_trace_coefficient_source_rows_built_all_claims_blocked_zero_route_watch_retained_nonclaim"
CLAIM_CEILING = "finite_trace_source_row_builder_and_zero_route_watch_only_no_numeric_trace_branch_no_R10_PPN_or_local_GR_claim"
NEXT_TARGET = "892-Y5-R10-trace-Hessian-Ztr-lambdatr-source-row-or-no-pole-theorem.md"


SOURCE_SPECS = [
    {
        "source_id": "890_doc",
        "path": ROOT / "890-Y5-R10-boundary-quotient-no-tail-signature-or-finite-trace-coefficient-acquisition.md",
        "needle": "finite trace coefficient acquisition is staged",
        "role": "immediate acquisition-plan handoff",
    },
    {
        "source_id": "890_validation",
        "path": OUT / "P8_Y5_BRR545_890_VALIDATION.csv",
        "needle": "V890_12_validation_rows_ready",
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "890_acquisition_plan",
        "path": OUT / "P8_Y5_R10_890_FINITE_TRACE_COEFFICIENT_ACQUISITION_PLAN.csv",
        "needle": "FCA890_8_source_provenance",
        "role": "finite trace coefficient acquisition requirements",
    },
    {
        "source_id": "882_min_source_pack",
        "path": OUT / "P8_Y5_R10_882_RETAINED_CT_MINIMUM_SOURCE_PACK.csv",
        "needle": "MCP882_8_source_provenance",
        "role": "minimum retained c_T source pack",
    },
    {
        "source_id": "875_ct_schema",
        "path": OUT / "P8_Y5_R10_875_CT_INPUT_SCHEMA.csv",
        "needle": "IN875_5_full_R10_curve",
        "role": "minimal c_T runner input schema",
    },
    {
        "source_id": "875_doc",
        "path": ROOT / "875-Y5-R10-cT-coefficient-fill-minimal-runner-and-claim-gate.md",
        "needle": "the c_T testing gate exists and every local claim is blocked",
        "role": "prior c_T coefficient gate",
    },
    {
        "source_id": "872_projection_formulas",
        "path": ROOT / "872-Y5-R10-cT-parent-projection-coefficient-or-theorem-zero-return.md",
        "needle": "alpha_T_AB = Q_T^A Q_T^B/(4*pi*Z_T*G_obs*m_A*m_B)",
        "role": "finite trace alpha/force/PPN formulas",
    },
    {
        "source_id": "873_charge_zero",
        "path": ROOT / "873-Y5-R10-local-matter-trace-charge-zero-theorem-or-coefficient-fill.md",
        "needle": "Q_T^A=0 follows by chain rule",
        "role": "zero-route matter charge watch",
    },
    {
        "source_id": "886_zero_pole",
        "path": ROOT / "886-Y5-R10-Htr-zero-pole-rank-test-and-Jtr-source-cokernel-gate.md",
        "needle": "rank-zero/no-pole/source-cokernel",
        "role": "zero-route no-pole/source-cokernel watch",
    },
    {
        "source_id": "559_R10_runner",
        "path": ROOT / "559-Y5-R10-bound-curve-digitization-and-MTS-alpha-prediction-runner.md",
        "needle": "The R10 runner now exists and correctly rejects placeholders",
        "role": "R10 executable curve runner contract",
    },
    {
        "source_id": "437_R10_contract",
        "path": ROOT / "437-R10-alpha-lambda-executable-curve-contract.md",
        "needle": "Anything else remains symbolic and blocks R10 promotion.",
        "role": "R10 alpha(lambda) claim discipline",
    },
    {
        "source_id": "R10_mts_placeholder",
        "path": OUT / "R10_alpha_lambda_curve_MTS_source_normalization.csv",
        "needle": "MISSING_DIGITIZED_ALPHA_BOUND",
        "role": "current MTS-side R10 placeholder curve",
    },
    {
        "source_id": "R10_bound_placeholder",
        "path": BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv",
        "needle": "MISSING_DIGITIZED_ALPHA_BOUND",
        "role": "current bound-side R10 placeholder curve",
    },
]


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def stringify(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return "" if value is None else str(value)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: stringify(row.get(field, "")) for field in fields})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def has_needle(path: Path, needle: str) -> bool:
    return path.exists() and needle in read_text(path)


def md_table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return "_No rows._"
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
        lines.append("| " + " | ".join(stringify(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines)


def source_register_rows(generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in SOURCE_SPECS:
        path = Path(spec["path"])
        rows.append(
            {
                "source_id": spec["source_id"],
                "path": path,
                "exists": path.exists(),
                "needle_check": "pass" if has_needle(path, str(spec["needle"])) else "fail",
                "role": spec["role"],
                "valid_for_claim": False,
                "generated_utc": generated_utc,
            }
        )
    return rows


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "built a first finite trace coefficient source-row manifest that unifies the 872 formulas, 875 c_T gate, 882 minimum pack, 890 acquisition plan, and 559 R10 runner",
            "best_partial_result": "the finite branch is now executable in schema: Z_tr, lambda_tr, Q_tr/m, species charge, metric/source response, clock response, R10 curve, arena projections, and provenance each have a row with units, formula/source target, arena, and claim blocker",
            "hard_blockers": "every physical input is still missing or theorem-dependent; MTS alpha(lambda) and external bound curves are placeholders; zero-route no-tail/matter/zero-pole proofs remain unsigned",
            "what_is_not_claimed": "numeric trace coefficients, finite trace carrier, R10 pass, PPN pass, clock/WEP pass, orbital pass, local GR/Newton derivation",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def coefficient_source_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "TCSR891_0_Ztr",
            "coefficient": "Z_tr",
            "sector": "trace_hessian",
            "formula_or_definition": "H_tr principal symbol sigma_2(H_tr)=Z_tr g^{mu nu}k_mu k_nu",
            "units": "parent_defined_kinetic_normalization",
            "needed_for": "alpha amplitude, positivity, ghost/no-pole check",
            "source_target": "parent trace Hessian or no-pole theorem",
            "current_value": "MISSING_PARENT_HESSIAN",
            "status": "missing_blocks_claim",
            "zero_route": "prove no local H_tr pole from rank-zero/readout-only theorem",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "row_id": "TCSR891_1_lambda_tr",
            "coefficient": "lambda_tr_or_m_tr",
            "sector": "trace_hessian",
            "formula_or_definition": "lambda_tr=1/m_tr, m_tr^2=mu_tr^2/Z_tr in natural units; SI conversion only after parent units are fixed",
            "units": "length_or_mass_parent_defined",
            "needed_for": "R10 interpolation and orbital Yukawa profile",
            "source_target": "H_tr pole/mass gap or theorem no physical pole",
            "current_value": "MISSING_PARENT_HESSIAN_OR_NOPOLE",
            "status": "missing_blocks_claim",
            "zero_route": "prove H_tr has no source-coupled local pole",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "row_id": "TCSR891_2_Qtr_universal",
            "coefficient": "Q_tr_over_m_universal",
            "sector": "matter_source",
            "formula_or_definition": "Q_tr^A/m_A = partial_{v_tr}m_A/m_A or source-cokernel projection per inertial mass",
            "units": "parent_defined_charge_per_mass",
            "needed_for": "R10/orbital common force",
            "source_target": "matter descent/no-marker theorem or source projection calculation",
            "current_value": "MISSING_SOURCE_PROJECTION_OR_ZERO_THEOREM",
            "status": "missing_blocks_claim",
            "zero_route": "prove Q_tr^A=0 by q_loc verticality and matter descent",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "row_id": "TCSR891_3_Qtr_species",
            "coefficient": "Delta_Q_tr_over_m_AB",
            "sector": "matter_species",
            "formula_or_definition": "Delta(Q_tr/m)_AB for material/species/clock composition channels",
            "units": "differential_charge_per_mass",
            "needed_for": "WEP and clock/material tests",
            "source_target": "no-marker constants audit or species response row",
            "current_value": "MISSING_NO_MARKER_RESULT",
            "status": "missing_blocks_claim",
            "zero_route": "prove partial_{v_tr} theta_A=0 for all ordinary matter constants",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "row_id": "TCSR891_4_metric_response",
            "coefficient": "C_T_gamma,C_T_beta,C_T_source",
            "sector": "weak_field_metric_source",
            "formula_or_definition": "gamma-1=C_T_gamma c_T; beta-1=C_T_beta c_T; source response decides GM absorption/leakage",
            "units": "dimensionless_response",
            "needed_for": "PPN and Newtonian source-normalization gates",
            "source_target": "linearized observed metric/coframe/source-normalization response",
            "current_value": "MISSING_RESPONSE_OPERATOR",
            "status": "missing_blocks_claim",
            "zero_route": "prove trace mode is locally vertical or exact-gauge before metric response",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "row_id": "TCSR891_5_clock_response",
            "coefficient": "C_T_clock",
            "sector": "clock_EM_time",
            "formula_or_definition": "delta nu_i/nu_i=C_T_clock_i c_T or zero by clock/matter descent",
            "units": "fractional_clock_response",
            "needed_for": "clock/redshift/local constants tests",
            "source_target": "clock/EM/time sector descent or response coefficient",
            "current_value": "MISSING_CLOCK_RESPONSE",
            "status": "missing_blocks_claim",
            "zero_route": "prove clock constants factor through q_loc with no trace marker",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "row_id": "TCSR891_6_R10_bound_curve",
            "coefficient": "alpha_bound(lambda)_R10",
            "sector": "external_bound_curve",
            "formula_or_definition": "full digitized/source-backed alpha_bound(lambda) in same Yukawa convention as alpha_tr",
            "units": "dimensionless_alpha_vs_length",
            "needed_for": "R10 comparison only after MTS theory row exists",
            "source_target": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
            "current_value": "MISSING_FULL_CURVE_FOR_CLAIM",
            "status": "missing_blocks_claim",
            "zero_route": "not needed only if theorem-zero is fully signed",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "row_id": "TCSR891_7_arena_projection",
            "coefficient": "tau_R10,tau_PPN,tau_clock_WEP,tau_orbital",
            "sector": "arena_projection",
            "formula_or_definition": "maps c_T,Z_tr,lambda_tr,J_tr,Q_tr to arena observables with units and assumptions",
            "units": "arena_dependent",
            "needed_for": "turn coefficients into testable residual vector",
            "source_target": "arena-specific projection maps",
            "current_value": "MISSING_ARENA_PROJECTION",
            "status": "missing_blocks_claim",
            "zero_route": "not needed for arenas if trace branch theorem-zero is signed",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "row_id": "TCSR891_8_provenance",
            "coefficient": "source_path_and_units_for_every_numeric_input",
            "sector": "provenance",
            "formula_or_definition": "each numeric/theorem-zero row must cite local path/URL/DOI, extraction method, confidence, units, assumptions",
            "units": "metadata",
            "needed_for": "claim hygiene and reproducibility",
            "source_target": "source register and formula references",
            "current_value": "SCHEMA_READY_VALUES_MISSING",
            "status": "schema_ready_no_claim",
            "zero_route": "theorem-zero certificate must also have source path and parent-signature evidence",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def arena_projection_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "arena_id": "APR891_0_R10",
            "arena": "R10_short_range",
            "observable_formula": "alpha_tr_AB=(Q_tr^A/m_A)(Q_tr^B/m_B)/(4*pi*Z_tr*G_obs); compare at lambda_tr",
            "requires_rows": "TCSR891_0_Ztr;TCSR891_1_lambda_tr;TCSR891_2_Qtr_universal;TCSR891_6_R10_bound_curve",
            "current_status": "blocked_missing_theory_and_bound_rows",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "arena_id": "APR891_1_orbital",
            "arena": "orbital_GM_Newton",
            "observable_formula": "delta a/a_N=alpha_tr_AB(1+r/lambda_tr)exp(-r/lambda_tr) unless constant universal GM absorption is proved",
            "requires_rows": "TCSR891_1_lambda_tr;TCSR891_2_Qtr_universal;TCSR891_4_metric_response;TCSR891_7_arena_projection",
            "current_status": "blocked_missing_source_normalization_and_orbital_bound",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "arena_id": "APR891_2_PPN",
            "arena": "PPN_gamma_beta_preferred_frame",
            "observable_formula": "gamma-1=C_T_gamma c_T; beta-1=C_T_beta c_T; preferred-frame/vector terms require their own coefficients",
            "requires_rows": "TCSR891_4_metric_response;TCSR891_7_arena_projection",
            "current_status": "blocked_missing_metric_response_operator",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "arena_id": "APR891_3_clock_WEP",
            "arena": "clock_WEP_EM_species",
            "observable_formula": "delta nu_i/nu_i=C_T_clock_i c_T; eta_AB depends on Delta(Q_tr/m)_AB",
            "requires_rows": "TCSR891_3_Qtr_species;TCSR891_5_clock_response;TCSR891_7_arena_projection",
            "current_status": "blocked_missing_no_marker_or_response",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "arena_id": "APR891_4_local_GR",
            "arena": "local_GR_Newton",
            "observable_formula": "trace branch must be theorem-zero or bounded, plus EH/source-normalization/PPN/q_loc/projector channels must close separately",
            "requires_rows": "all trace rows plus broader local-GR stack",
            "current_status": "blocked_trace_branch_and_broader_stack_open",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def r10_runner_input_audit_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "audit_id": "R10A891_0_MTS_curve_file",
            "artifact": OUT / "R10_alpha_lambda_curve_MTS_source_normalization.csv",
            "required_for_claim": "numeric lambda_value, numeric alpha_predicted, formula/source path, valid_for_claim=true or theorem-zero certificate",
            "current_status": "placeholder_invalid",
            "runner_effect": "no valid MTS trace rows for comparison",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "R10A891_1_bound_curve_file",
            "artifact": BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv",
            "required_for_claim": "positive numeric lambda_value and alpha_bound with source/digitization method and valid_for_claim=true",
            "current_status": "placeholder_invalid",
            "runner_effect": "no valid bound rows for comparison",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "R10A891_2_formula_ready_not_numeric",
            "artifact": "872/890/891 formula rows",
            "required_for_claim": "alpha_tr(lambda_tr) from parent Z_tr/lambda_tr/Q_tr values",
            "current_status": "formula_schema_only",
            "runner_effect": "do not populate claim curve until parent values exist",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "R10A891_3_comparator_policy",
            "artifact": ROOT / "scripts" / "R10_alpha_lambda_bound_prediction_runner.py",
            "required_for_claim": "all MTS and bound rows valid, numeric, sourced; abs(alpha_predicted)<=alpha_bound over valid lambda range",
            "current_status": "runner_available_but_not_evidence_ready",
            "runner_effect": "next run remains dry/blocker only",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def zero_route_watch_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "watch_id": "ZRW891_0_no_tail",
            "zero_route": "boundary/no-tail P_loc J_trace=0",
            "current_status": "conditional_not_parent_signed",
            "would_replace_rows": "TCSR891_0_Ztr;TCSR891_1_lambda_tr;TCSR891_2_Qtr_universal for R10/orbital trace carrier",
            "required_next_evidence": "parent-owned J_trace support class and compact relative-zero/no-flux certificate",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "watch_id": "ZRW891_1_matter_charge_zero",
            "zero_route": "Q_tr^A=0 by q_loc verticality and matter descent",
            "current_status": "conditional_not_parent_signed",
            "would_replace_rows": "TCSR891_2_Qtr_universal;TCSR891_3_Qtr_species;TCSR891_5_clock_response",
            "required_next_evidence": "S_matter descends through q_loc and constants carry no trace marker",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "watch_id": "ZRW891_2_no_pole",
            "zero_route": "H_tr has no source-coupled local pole",
            "current_status": "conditional_not_parent_signed",
            "would_replace_rows": "TCSR891_0_Ztr;TCSR891_1_lambda_tr",
            "required_next_evidence": "rank(P_loc P_tr P_loc^dagger)=0 or parent constraint/gauge route",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "watch_id": "ZRW891_3_source_cokernel",
            "zero_route": "J_tr source-cokernel vanishes",
            "current_status": "conditional_not_parent_signed",
            "would_replace_rows": "TCSR891_2_Qtr_universal;TCSR891_3_Qtr_species",
            "required_next_evidence": "local matter source is compact-local and descends through q_loc",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "watch_id": "ZRW891_4_verdict",
            "zero_route": "full trace zero-return",
            "current_status": "watch_only_no_promotion",
            "would_replace_rows": "all finite trace coefficient rows for local arenas",
            "required_next_evidence": "ZRW891_0 through ZRW891_3 parent-signed together",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def claim_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "G891_0_coefficients_ready",
            "gate": "all finite trace coefficient rows have numeric/theorem-zero source-backed inputs",
            "current_result": "fail_for_claim",
            "reason": "every coefficient row is missing or schema-only",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "G891_1_R10_ready",
            "gate": "MTS alpha(lambda) row and bound alpha(lambda) row are both valid, numeric, sourced",
            "current_result": "fail_for_claim",
            "reason": "MTS and bound curves are placeholders",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "G891_2_local_arenas_ready",
            "gate": "PPN/clock/WEP/orbital projections are derived or sourced",
            "current_result": "fail_for_claim",
            "reason": "response operators and arena maps are missing",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "G891_3_zero_route_promoted",
            "gate": "zero-route certificate parent-signed and replaces finite rows",
            "current_result": "fail_for_claim",
            "reason": "zero-route watch is conditional only",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "G891_4_local_GR",
            "gate": "local GR/Newton follows",
            "current_result": "fail_for_claim",
            "reason": "trace branch is only one unresolved local-GR component",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def blocker_ledger_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "blocker_id": "BL891_0_first_physics_row",
            "blocker": "Z_tr and lambda_tr require parent trace Hessian or no-pole theorem",
            "why_it_is_first": "without kinetic normalization/range there is no finite carrier to score",
            "next_action": "attack H_tr principal symbol or prove no local pole",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "blocker_id": "BL891_1_source_charge",
            "blocker": "Q_tr/m or source-cokernel zero is missing",
            "why_it_is_first": "even with Z/lambda, no force exists without a source/test charge",
            "next_action": "derive Q_tr=0 by matter descent or fill source projection rows",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "blocker_id": "BL891_2_arena_maps",
            "blocker": "metric/source/clock/orbital response maps are missing",
            "why_it_is_first": "nonzero trace branch must map to actual observables, not symbolic c_T language",
            "next_action": "after Z/lambda/Q, derive arena response operators",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "blocker_id": "BL891_3_R10_bound_data",
            "blocker": "R10 bound curve is placeholder-only",
            "why_it_is_first": "needed only after an MTS alpha prediction row exists",
            "next_action": "do not digitize as evidence until MTS theory row exists; keep dry-run ready",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def promotion_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "PG891_0_finite_trace_branch",
            "promotion_target": "finite trace branch is executable as a physical prediction",
            "required_to_pass": "Z_tr/lambda_tr/Q_tr and arena maps source-backed or theorem-zero",
            "current_evidence": "source rows built but values missing",
            "gate_result": "fail_for_claim",
            "next_action": "start with trace Hessian Z_tr/lambda_tr or no-pole theorem",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG891_1_R10",
            "promotion_target": "R10 alpha(lambda) comparison can support claim",
            "required_to_pass": "valid MTS alpha row and valid bound curve row pass comparator",
            "current_evidence": "placeholder rows only",
            "gate_result": "fail_for_claim",
            "next_action": "no R10 evidence yet",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG891_2_zero_route",
            "promotion_target": "trace branch theorem-zero replaces finite coefficients",
            "required_to_pass": "no-tail, matter charge zero, no-pole, and source-cokernel jointly signed",
            "current_evidence": "watch only",
            "gate_result": "fail_for_claim",
            "next_action": "keep zero route alive while filling finite branch",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG891_3_local_GR",
            "promotion_target": "local GR/Newton derived",
            "required_to_pass": "trace branch plus all other local residual/source-normalization branches closed",
            "current_evidence": "trace coefficient rows only",
            "gate_result": "fail_for_claim",
            "next_action": "do not promote",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC891_0_selected",
            "route": "trace_Hessian_Ztr_lambdatr_source_row_or_no_pole_theorem",
            "status": "selected",
            "reason": "Z_tr and lambda_tr are upstream of every finite trace arena; if no-pole closes, they are unnecessary, otherwise they are the first real theory inputs",
            "include": "H_tr principal symbol, mass/range, no-pole theorem, source row validation",
            "exclude": "R10 scoring, public claim, formalization-workbench edits, GitHub action, fitted tiny coupling",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG891_0_no_numeric_trace_claim",
            "forbidden_claim": "trace coefficients are known",
            "status": "forbidden",
            "reason": "source rows are schema/manifest only and contain missing markers",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG891_1_no_R10_claim",
            "forbidden_claim": "R10/fifth-force comparison passes",
            "status": "forbidden",
            "reason": "MTS alpha and bound curves are placeholder-invalid",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG891_2_no_zero_route_claim",
            "forbidden_claim": "trace zero-return is proven",
            "status": "forbidden",
            "reason": "zero-route watch remains unsigned",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG891_3_no_local_GR",
            "forbidden_claim": "local GR/Newton follows",
            "status": "forbidden",
            "reason": "trace coefficient source rows are not a local-GR derivation",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG891_4_allowed_private_result",
            "forbidden_claim": "none",
            "status": "allowed_private_nonclaim",
            "reason": "891 turns the finite trace fallback into a disciplined source-row manifest",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D891_0",
            "finding": "source_rows_built",
            "reason": "finite trace branch now has explicit source rows for every required coefficient and arena projection",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D891_1",
            "finding": "all_claims_blocked",
            "reason": "every finite branch row is missing/theorem-dependent and every arena gate refuses claim",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D891_2",
            "finding": "Ztr_lambdatr_selected_next",
            "reason": "the trace Hessian/range is upstream of R10, orbital, and stability decisions",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def next_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "derive or source the trace Hessian principal symbol/range, or prove the no-pole theorem so Z_tr/lambda_tr are not physical local inputs",
            "include": "H_tr principal symbol, Z_tr sign, m_tr/lambda_tr, no-pole theorem, source row validation",
            "exclude": "R10 evidence claim, PPN/local-GR pass, fitted coefficient, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def prior_890_clean() -> bool:
    path = OUT / "P8_Y5_BRR545_890_VALIDATION.csv"
    return path.exists() and all(row.get("result") == "pass" for row in read_csv(path))


def formalization_changed_count() -> int:
    if not FORMALIZATION.exists():
        return -1
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime)
            if modified > CUTOFF:
                count += 1
    return count


def all_nonclaim(row_groups: Iterable[list[dict[str, object]]]) -> bool:
    for rows in row_groups:
        for row in rows:
            if stringify(row.get("valid_for_claim", False)) != "false":
                return False
    return True


def validation_rows(
    generated_utc: str,
    source_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    coefficient_rows: list[dict[str, object]],
    arena_rows: list[dict[str, object]],
    r10_rows: list[dict[str, object]],
    zero_rows: list[dict[str, object]],
    claim_gate_rows_: list[dict[str, object]],
    blocker_rows: list[dict[str, object]],
    promotion_rows: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_target_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    formalization_count = formalization_changed_count()
    coefficient_ids = {row["row_id"] for row in coefficient_rows}
    missing_values = [str(row["current_value"]) for row in coefficient_rows]
    r10_statuses = [str(row["current_status"]) for row in r10_rows]
    row_groups = [
        source_rows,
        summary_rows,
        coefficient_rows,
        arena_rows,
        r10_rows,
        zero_rows,
        claim_gate_rows_,
        blocker_rows,
        promotion_rows,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
    ]
    checks = [
        {
            "check_id": "V891_0_sources_exist_and_needles",
            "result": "pass" if all(row["exists"] and row["needle_check"] == "pass" for row in source_rows) else "fail",
            "detail": "all 891 source paths exist and needles are present",
        },
        {
            "check_id": "V891_1_prior_890_clean",
            "result": "pass" if prior_890_clean() else "fail",
            "detail": "P8_Y5_BRR545_890_VALIDATION.csv clean",
        },
        {
            "check_id": "V891_2_coefficient_rows_complete",
            "result": "pass" if {"TCSR891_0_Ztr", "TCSR891_1_lambda_tr", "TCSR891_2_Qtr_universal", "TCSR891_3_Qtr_species", "TCSR891_4_metric_response", "TCSR891_5_clock_response", "TCSR891_6_R10_bound_curve", "TCSR891_7_arena_projection", "TCSR891_8_provenance"}.issubset(coefficient_ids) else "fail",
            "detail": "all finite trace coefficient source rows present",
        },
        {
            "check_id": "V891_3_missing_markers_block_coefficients",
            "result": "pass" if all(("MISSING" in value or "SCHEMA_READY" in value) for value in missing_values) else "fail",
            "detail": "coefficient rows remain missing/schema-only",
        },
        {
            "check_id": "V891_4_arena_gates_blocked",
            "result": "pass" if arena_rows and all(row["claim_allowed"] is False for row in arena_rows) else "fail",
            "detail": "arena projection rows all block claims",
        },
        {
            "check_id": "V891_5_R10_placeholders_blocked",
            "result": "pass" if r10_rows and all(("placeholder" in status or "schema" in status or "runner_available" in status) for status in r10_statuses) else "fail",
            "detail": "R10 MTS and bound placeholder rows remain blocked",
        },
        {
            "check_id": "V891_6_zero_route_watch_nonclaim",
            "result": "pass" if zero_rows and all(row["valid_for_claim"] is False for row in zero_rows) and any(row["watch_id"] == "ZRW891_4_verdict" for row in zero_rows) else "fail",
            "detail": "zero-route watch remains nonclaim",
        },
        {
            "check_id": "V891_7_claim_gates_blocked",
            "result": "pass" if claim_gate_rows_ and all(row["claim_allowed"] is False for row in claim_gate_rows_) else "fail",
            "detail": "claim gates all false",
        },
        {
            "check_id": "V891_8_promotion_gates_blocked",
            "result": "pass" if promotion_rows and all(row["gate_result"] == "fail_for_claim" for row in promotion_rows) else "fail",
            "detail": "all promotion gates fail for claim",
        },
        {
            "check_id": "V891_9_claim_allowed_false",
            "result": "pass" if all(row["claim_allowed"] is False for row in decision_rows_) else "fail",
            "detail": "decision rows keep claim_allowed=false",
        },
        {
            "check_id": "V891_10_all_rows_nonclaim",
            "result": "pass" if all_nonclaim(row_groups) else "fail",
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "V891_11_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V891_12_route_selected",
            "result": "pass" if route_rows_ and next_target_rows_ and next_target_rows_[0]["next_target"] == NEXT_TARGET else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V891_13_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        },
    ]
    return [{**row, "generated_utc": generated_utc} for row in checks]


def write_markdown(
    path: Path,
    generated_utc: str,
    summary_rows: list[dict[str, object]],
    source_rows: list[dict[str, object]],
    coefficient_rows: list[dict[str, object]],
    arena_rows: list[dict[str, object]],
    r10_rows: list[dict[str, object]],
    zero_rows: list[dict[str, object]],
    claim_gate_rows_: list[dict[str, object]],
    blocker_rows: list[dict[str, object]],
    promotion_rows: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_target_rows_: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    lines = [
        "# 891 - Y5/R10 Finite Trace Coefficient Source-Row Builder With Zero-Route Watch",
        "",
        f"Status: `{STATUS}`  ",
        f"Claim ceiling: `{CLAIM_CEILING}`  ",
        f"Generated UTC: `{generated_utc}`",
        "",
        "Current result: **the finite trace fallback now has a disciplined source-row manifest, but still no physical claim**. The branch can no longer hide behind `c_T` as a symbol: `Z_tr`, `lambda_tr`, `Q_tr/m`, species charge, metric/source response, clock response, R10 bound data, arena projection, and provenance are separate gated rows. Every one is missing or theorem-dependent, the R10 runner still sees placeholder curves, and the zero-route watch remains conditional.",
        "",
        "## Nonclaim Summary",
        md_table(summary_rows),
        "",
        "## Source Register",
        md_table(source_rows),
        "",
        "## Trace Coefficient Source Rows",
        md_table(coefficient_rows),
        "",
        "## Arena Projection Rows",
        md_table(arena_rows),
        "",
        "## R10 Runner Input Audit",
        md_table(r10_rows),
        "",
        "## Zero Route Watch",
        md_table(zero_rows),
        "",
        "## Claim Gates",
        md_table(claim_gate_rows_),
        "",
        "## Blocker Ledger",
        md_table(blocker_rows),
        "",
        "## Promotion Gates",
        md_table(promotion_rows),
        "",
        "## Route Choice",
        md_table(route_rows_),
        "",
        "## Claim Guards",
        md_table(guard_rows),
        "",
        "## Decisions",
        md_table(decision_rows_),
        "",
        "## Next Target",
        md_table(next_target_rows_),
        "",
        "## Validation",
        md_table(validation_rows_),
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    generated_utc = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows(generated_utc)
    summary_rows = nonclaim_summary_rows(generated_utc)
    coefficient_rows = coefficient_source_rows(generated_utc)
    arena_rows = arena_projection_rows(generated_utc)
    r10_rows = r10_runner_input_audit_rows(generated_utc)
    zero_rows = zero_route_watch_rows(generated_utc)
    claim_gate_rows_ = claim_gate_rows(generated_utc)
    blocker_rows = blocker_ledger_rows(generated_utc)
    promotion_rows = promotion_gate_rows(generated_utc)
    route_rows_ = route_rows(generated_utc)
    guard_rows = claim_guard_rows(generated_utc)
    decision_rows_ = decision_rows(generated_utc)
    next_target_rows_ = next_target_rows(generated_utc)
    validation_rows_ = validation_rows(
        generated_utc,
        source_rows,
        summary_rows,
        coefficient_rows,
        arena_rows,
        r10_rows,
        zero_rows,
        claim_gate_rows_,
        blocker_rows,
        promotion_rows,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
    )

    outputs = {
        "P8_Y5_R10_891_SOURCE_REGISTER.csv": source_rows,
        "P8_Y5_R10_891_TRACE_COEFFICIENT_SOURCE_ROWS.csv": coefficient_rows,
        "P8_Y5_R10_891_ARENA_PROJECTION_ROWS.csv": arena_rows,
        "P8_Y5_R10_891_R10_RUNNER_INPUT_AUDIT.csv": r10_rows,
        "P8_Y5_R10_891_ZERO_ROUTE_WATCH.csv": zero_rows,
        "P8_Y5_R10_891_CLAIM_GATE.csv": claim_gate_rows_,
        "P8_Y5_R10_891_BLOCKER_LEDGER.csv": blocker_rows,
        "P8_Y5_R10_891_PROMOTION_GATE.csv": promotion_rows,
        "P8_Y5_R10_891_ROUTE_CHOICE.csv": route_rows_,
        "P8_Y5_R10_891_CLAIM_GUARD.csv": guard_rows,
        "P8_Y5_R10_891_DECISION.csv": decision_rows_,
        "P8_Y5_R10_891_NEXT_TARGET.csv": next_target_rows_,
        "P8_Y5_R10_891_NONCLAIM_SUMMARY.csv": summary_rows,
        "P8_Y5_BRR545_891_VALIDATION.csv": validation_rows_,
    }
    for filename, rows in outputs.items():
        write_csv(OUT / filename, rows)

    doc_path = ROOT / "891-Y5-R10-finite-trace-coefficient-source-row-builder-with-zero-route-watch.md"
    write_markdown(
        doc_path,
        generated_utc,
        summary_rows,
        source_rows,
        coefficient_rows,
        arena_rows,
        r10_rows,
        zero_rows,
        claim_gate_rows_,
        blocker_rows,
        promotion_rows,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
        validation_rows_,
    )

    failed = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"wrote {doc_path}")
    print(f"wrote {OUT / 'P8_Y5_BRR545_891_VALIDATION.csv'}")
    print(f"status={STATUS}")
    if failed:
        print("failed_validation=" + ",".join(row["check_id"] for row in failed))
        raise SystemExit(1)


if __name__ == "__main__":
    main()

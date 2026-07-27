from __future__ import annotations

import csv
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

STATUS = "Y5_R10_899_trace_residual_vector_source_pack_and_local_bound_interface_built_all_claims_blocked_nonclaim"
CLAIM_CEILING = "trace_residual_source_pack_interface_only_no_numeric_trace_prediction_no_R10_PPN_WEP_clock_orbital_or_local_GR_claim"
NEXT_TARGET = "900-Y5-R10-trace-residual-vector-priority-source-acquisition-or-theorem-zero-reopen.md"

R10_ALPHA_FORMULA = "alpha_tr_AB(lambda_tr)=(Q_tr^A/m_A)*(Q_tr^B/m_B)/(4*pi*Z_tr*G_obs), evaluated only after lambda_tr and Q_tr are sourced"

MTS_REQUIRED_COLUMNS = [
    "model_id",
    "branch_id",
    "curve_id",
    "lambda_value",
    "lambda_units",
    "alpha_predicted",
    "alpha_bound",
    "alpha_bound_source",
    "force_law_form",
    "derivation_status",
    "formula_reference",
    "source_file",
    "assumptions",
    "valid_for_claim",
    "notes",
]

SOURCE_SPECS = [
    {
        "source_id": "898_doc",
        "path": ROOT / "898-Y5-R10-trace-vertical-generator-matter-descent-signature-or-residual-vector.md",
        "needle": "residual vector is now staged explicitly",
        "role": "immediate residual-vector handoff",
    },
    {
        "source_id": "898_validation",
        "path": OUT / "P8_Y5_BRR545_898_VALIDATION.csv",
        "needle": "V898_12_validation_rows_ready",
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "898_residual_vector",
        "path": OUT / "P8_Y5_R10_898_TRACE_RESIDUAL_VECTOR.csv",
        "needle": "TRV898_0_Ztr",
        "role": "staged trace residual vector inputs",
    },
    {
        "source_id": "898_branch_decision",
        "path": OUT / "P8_Y5_R10_898_BRANCH_DECISION.csv",
        "needle": "BD898_2_residual_vector_route",
        "role": "residual vector route selection",
    },
    {
        "source_id": "875_doc",
        "path": ROOT / "875-Y5-R10-cT-coefficient-fill-minimal-runner-and-claim-gate.md",
        "needle": "c_T testing gate exists",
        "role": "previous local-bound coefficient interface pattern",
    },
    {
        "source_id": "875_validation",
        "path": OUT / "P8_Y5_BRR545_875_VALIDATION.csv",
        "needle": "V875_10_validation_rows_ready",
        "role": "prior local-bound gate validation",
    },
    {
        "source_id": "875_input_schema",
        "path": OUT / "P8_Y5_R10_875_CT_INPUT_SCHEMA.csv",
        "needle": "IN875_0_Z_T",
        "role": "minimal coefficient schema pattern",
    },
    {
        "source_id": "875_bound_links",
        "path": OUT / "P8_Y5_R10_875_BOUND_LINK_ROWS.csv",
        "needle": "CT871_R10_EOTWASH_2020_ALPHA1_38P6UM_ANCHOR",
        "role": "context-only bound link rows",
    },
    {
        "source_id": "875_symbolic_predictions",
        "path": OUT / "P8_Y5_R10_875_SYMBOLIC_PREDICTION_ROWS.csv",
        "needle": "PRED875_0_R10_alpha",
        "role": "symbolic prediction pattern",
    },
    {
        "source_id": "r10_runner",
        "path": ROOT / "scripts" / "R10_alpha_lambda_bound_prediction_runner.py",
        "needle": "MTS_REQUIRED_COLUMNS",
        "role": "existing R10 alpha(lambda) schema and dry-run comparator",
    },
    {
        "source_id": "r10_digitized_bound_placeholder",
        "path": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv",
        "needle": "R10_BOUND_PLACEHOLDER_0",
        "role": "current R10 bound file remains invalid placeholder data",
    },
    {
        "source_id": "local_bounds_template",
        "path": LOCAL_BOUNDS / "local_bound_claims_TEMPLATE.csv",
        "needle": "WEP_differential_acceleration",
        "role": "local PPN/WEP/clock template rows, not claim-grade inputs",
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
        values = [stringify(row.get(field, "")).replace("\n", " ").replace("|", "/") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
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
            "what_changed": "converted the 898 trace residual vector into an executable source-pack and local-bound interface",
            "best_partial_result": "every trace leakage quantity now has an arena map, a required parent source/theorem-zero route, and a bound interface without pretending the coefficients exist",
            "hard_blockers": "Z_tr, lambda_tr, Q_tr/m, species deltas, PPN response, clock/EM response, source normalization, and boundary tails remain missing or theorem-dependent",
            "what_is_not_claimed": "numeric alpha_tr, R10 pass, PPN pass, WEP/clock pass, orbital pass, local GR/Newton reduction, or J_tr/Q_tr zero",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def residual_requirements() -> dict[str, dict[str, str]]:
    return {
        "TRV898_0_Ztr": {
            "required_parent_source": "parent Hessian/principal symbol for H_tr, or parent-signed no-pole theorem",
            "required_units": "positive kinetic normalization in the parent local trace sector, or absent_by_theorem",
            "source_status": "MISSING_PARENT_HESSIAN_OR_NOPOLE",
            "theorem_zero_reopen": "prove local trace Hessian has no source-coupled pole or rank-zero compact-local image",
            "bound_interface": "R10/orbital alpha denominator and PPN response amplitude",
            "next_action": "derive Z_tr from parent action or reopen no-pole proof",
        },
        "TRV898_1_lambdatr": {
            "required_parent_source": "parent mass gap mu_tr^2 with Z_tr normalization, or no local pole",
            "required_units": "length in meters after lambda_tr=sqrt(Z_tr/mu_tr^2), or absent_by_theorem",
            "source_status": "MISSING_MASS_GAP_OR_NOPOLE",
            "theorem_zero_reopen": "prove no finite-range trace carrier couples to local matter",
            "bound_interface": "R10 alpha(lambda) and finite-range orbital residuals",
            "next_action": "derive mu_tr^2/Z_tr or prove lambda_tr does not exist locally",
        },
        "TRV898_2_Qtr_universal": {
            "required_parent_source": "source-cokernel pairing P_tr^dagger J_parent or matter charge derivative along v_tr",
            "required_units": "dimensionless or parent charge per inertial mass with G_obs normalization",
            "source_status": "MISSING_SOURCE_PROJECTION_OR_ZERO_THEOREM",
            "theorem_zero_reopen": "prove Dq_loc[v_tr]=0 and matter descends through q_loc, giving Q_tr^A=0",
            "bound_interface": "R10 common Yukawa force and orbital/source-normalization audit",
            "next_action": "prove source-cokernel zero or source Q_tr/m",
        },
        "TRV898_3_Qtr_species_delta": {
            "required_parent_source": "species/material dependence of trace charge, or no-marker theorem",
            "required_units": "dimensionless Eotvos/charge-per-mass difference",
            "source_status": "MISSING_NO_MARKER_OR_SPECIES_FUNCTIONAL",
            "theorem_zero_reopen": "prove no trace marker in species constants, alpha_EM, masses, or binding terms",
            "bound_interface": "WEP/MICROSCOPE and clock-material comparisons",
            "next_action": "derive species delta or parent-sign no-marker theorem",
        },
        "TRV898_4_Ctr_PPN": {
            "required_parent_source": "weak-field observed metric response operator for trace leakage",
            "required_units": "dimensionless PPN response coefficients",
            "source_status": "MISSING_WEAK_FIELD_RESPONSE_OPERATOR",
            "theorem_zero_reopen": "prove trace response is double-zero at the local GR fixed point",
            "bound_interface": "gamma, beta, alpha_i, xi, and related PPN bounds",
            "next_action": "derive observed metric map or parent-sign double-zero response",
        },
        "TRV898_5_clock_EM": {
            "required_parent_source": "clock transition and electromagnetic/fine-structure functional along v_tr",
            "required_units": "dimensionless frequency/alpha_EM response or per-time projection",
            "source_status": "MISSING_CLOCK_EM_FUNCTIONAL_OR_NO_ALPHA_THEOREM",
            "theorem_zero_reopen": "prove EM/clock constants are quotient-only or superselected, not trace markers",
            "bound_interface": "redshift clocks, alpha_EM drift, and clock-comparison residuals",
            "next_action": "derive clock/EM response or no-alpha marker theorem",
        },
        "TRV898_6_source_normalization": {
            "required_parent_source": "measured-GM/source-normalization split and Gdot/source response operator",
            "required_units": "dimensionless source normalization or inverse-time drift",
            "source_status": "MISSING_SOURCE_NORMALIZATION_OPERATOR",
            "theorem_zero_reopen": "prove trace leakage is absorbed into universal kappa without fifth-force residue",
            "bound_interface": "Newtonian limit, ephemerides, LLR/Gdot, and orbital acceleration residuals",
            "next_action": "derive source-normalization operator and choose a real orbital observable",
        },
        "TRV898_7_boundary_tail": {
            "required_parent_source": "boundary support/no-tail certificate and transverse tensor leakage bound",
            "required_units": "model-dependent boundary/tensor leakage norm",
            "source_status": "MISSING_BOUNDARY_SUPPORT_CERTIFICATE_OR_BOUND",
            "theorem_zero_reopen": "prove local projection silence and no boundary/EFT re-entry",
            "bound_interface": "local_GR, PPN, orbital residual contamination guard",
            "next_action": "prove no-tail or carry boundary leakage as explicit residual",
        },
    }


def residual_source_pack_rows(generated_utc: str) -> list[dict[str, object]]:
    residual_rows = read_csv(OUT / "P8_Y5_R10_898_TRACE_RESIDUAL_VECTOR.csv")
    requirements = residual_requirements()
    rows: list[dict[str, object]] = []
    for index, residual in enumerate(residual_rows):
        residual_id = residual["residual_id"]
        req = requirements[residual_id]
        rows.append(
            {
                "pack_id": f"RSP899_{index}",
                "residual_id": residual_id,
                "quantity": residual["quantity"],
                "arena": residual["arena"],
                "current_value": residual["current_value"],
                "inherited_units": residual["units"],
                "inherited_source_path": residual["source_path"],
                "required_parent_source": req["required_parent_source"],
                "required_units": req["required_units"],
                "source_status": req["source_status"],
                "theorem_zero_reopen": req["theorem_zero_reopen"],
                "bound_interface": req["bound_interface"],
                "next_action": req["next_action"],
                "valid_for_claim": False,
                "generated_utc": generated_utc,
            }
        )
    return rows


def local_bound_interface_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "interface_id": "LBI899_0_R10_alpha_lambda",
            "arena": "R10_short_range_inverse_square",
            "prediction_shape": R10_ALPHA_FORMULA,
            "requires_trace_inputs": "Z_tr;lambda_tr;Q_tr^A/m_A;Q_tr^B/m_B;source-normalization",
            "requires_bound_inputs": "claim-grade full alpha_bound(lambda) curve with positive numeric lambda and alpha rows",
            "current_status": "blocked_missing_trace_inputs_and_bound_curve",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "interface_id": "LBI899_1_PPN_metric",
            "arena": "PPN_solar_system",
            "prediction_shape": "gamma-1=C_tr_gamma*epsilon_tr, beta-1=C_tr_beta*epsilon_tr, alpha_i=C_tr_alpha_i*epsilon_tr after gauge/source-normalization split",
            "requires_trace_inputs": "C_tr_gamma;C_tr_beta;C_tr_alpha_i;epsilon_tr or theorem-zero",
            "requires_bound_inputs": "Cassini/VLBI/ephemeris/preferred-frame bounds with cited source rows",
            "current_status": "blocked_missing_weak_field_response_operator",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "interface_id": "LBI899_2_WEP_species",
            "arena": "WEP_composition",
            "prediction_shape": "eta_AB controlled by Delta_AB(Q_tr/m) after ordinary-matter no-marker audit",
            "requires_trace_inputs": "Delta_AB_Q_tr_over_m or parent-signed no-marker theorem",
            "requires_bound_inputs": "MICROSCOPE/Eotvos material-pair bound rows",
            "current_status": "blocked_missing_species_functional_or_no_marker_theorem",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "interface_id": "LBI899_3_clock_EM",
            "arena": "clock_redshift_EM",
            "prediction_shape": "delta nu_i/nu_i=C_tr_clock_i*epsilon_tr and delta alpha_EM/alpha_EM=C_tr_alphaEM*epsilon_tr unless no-alpha theorem closes",
            "requires_trace_inputs": "C_tr_clock_i;C_tr_alphaEM;clock/EM functional or no-alpha marker theorem",
            "requires_bound_inputs": "clock redshift, clock-comparison, and alpha_EM drift rows",
            "current_status": "blocked_missing_clock_EM_functional",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "interface_id": "LBI899_4_orbital_finite_range",
            "arena": "orbital_dynamics",
            "prediction_shape": "delta a/a_N=alpha_tr_AB*(1+r/lambda_tr)*exp(-r/lambda_tr) plus source-normalization split",
            "requires_trace_inputs": "alpha_tr_AB;lambda_tr;C_tr_source;delta_GM_tr;Gdot_tr",
            "requires_bound_inputs": "LLR/ephemeris/Gdot/anomalous-acceleration source-backed bound rows",
            "current_status": "blocked_missing_alpha_lambda_source_normalization_and_orbital_bound_selection",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "interface_id": "LBI899_5_boundary_local_projection",
            "arena": "boundary_tail_local_GR",
            "prediction_shape": "local residual norm includes B_tr_tail and K_perp_trace unless no-tail/local-projection silence is parent-signed",
            "requires_trace_inputs": "B_tr_tail;K_perp_trace or no-boundary-tail theorem",
            "requires_bound_inputs": "not a standalone empirical score; gates contamination of PPN/orbital/local-GR reductions",
            "current_status": "blocked_missing_boundary_support_certificate",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "interface_id": "LBI899_6_local_GR_aggregate",
            "arena": "local_GR_Newton_reduction",
            "prediction_shape": "q_loc residual vector must vanish structurally or be bounded below all local arenas while EH/Newton/source-normalization gates also close",
            "requires_trace_inputs": "all trace residual rows zero/sourced plus non-trace local-GR gates",
            "requires_bound_inputs": "R10;PPN;WEP;clock;orbital;Newton source-normalization evidence",
            "current_status": "blocked_trace_channel_only_one_unclosed_local_GR_gate",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def r10_runner_dry_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "model_id": "MTS_trace_residual_vector",
            "branch_id": "R10_trace_residual_symbolic",
            "curve_id": "TR899_R10_0_missing_alpha",
            "lambda_value": "MISSING_LAMBDA_TR",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_ALPHA_TR",
            "alpha_bound": "MISSING_BOUND_LOOKUP",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
            "force_law_form": "Yukawa-like alpha_tr_AB exp(-r/lambda_tr) nonclaim placeholder",
            "derivation_status": "MISSING_ZTR_LAMBDATR_QTR_PARENT_INPUTS",
            "formula_reference": R10_ALPHA_FORMULA,
            "source_file": "source-intake/mts_residuals/P8_Y5_R10_899_TRACE_RESIDUAL_SOURCE_PACK.csv",
            "assumptions": "no numeric trace prediction; row exists only to dry-check runner schema and failure modes",
            "valid_for_claim": False,
            "notes": "must fail runner validation until lambda_tr and alpha_tr are sourced or theorem-zero closes",
            "generated_utc": generated_utc,
        },
        {
            "model_id": "MTS_trace_residual_vector",
            "branch_id": "R10_trace_zero_theorem_unsigned",
            "curve_id": "TR899_R10_1_unsigned_zero",
            "lambda_value": "MISSING_NO_LOCAL_POLE_PROOF",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_ZERO_THEOREM_NOT_SIGNED",
            "alpha_bound": "MISSING_BOUND_LOOKUP",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
            "force_law_form": "zero only if source-cokernel/no-pole theorem is parent-signed",
            "derivation_status": "ZERO_ROUTE_UNSIGNED_NONCLAIM",
            "formula_reference": "alpha_tr=0 only if Q_tr^A=0 or no source-coupled pole",
            "source_file": "source-intake/mts_residuals/P8_Y5_R10_899_THEOREM_ZERO_REOPEN_GATE.csv",
            "assumptions": "theorem-zero branch is an audit target, not evidence",
            "valid_for_claim": False,
            "notes": "keeps the honest zero route visible without converting it into a pass",
            "generated_utc": generated_utc,
        },
    ]


def arena_projection_requirement_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "projection_id": "APR899_0_R10",
            "arena": "R10",
            "minimal_projection": "trace residual -> alpha_tr(lambda_tr)",
            "must_supply": "Z_tr, lambda_tr, Q_tr/m, G_obs normalization, full bound curve",
            "blocks_claim_because": "all trace inputs are MISSING and current bound file is placeholder",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "projection_id": "APR899_1_PPN",
            "arena": "PPN",
            "minimal_projection": "trace residual -> gamma,beta,alpha_i,xi residual vector in observed metric gauge",
            "must_supply": "weak-field response operator and source-normalization/gauge split",
            "blocks_claim_because": "C_tr_PPN is missing and local observed metric map is unsigned",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "projection_id": "APR899_2_WEP_clock_EM",
            "arena": "WEP_clock_EM",
            "minimal_projection": "trace residual -> species charge, clock transition, alpha_EM response",
            "must_supply": "no-marker theorem or numeric material/clock functional",
            "blocks_claim_because": "species/clock/EM trace markers are not parent-classified",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "projection_id": "APR899_3_orbital_Newton",
            "arena": "orbital_Newton_source",
            "minimal_projection": "trace residual -> finite-range acceleration plus GM/Gdot/source-normalization residue",
            "must_supply": "lambda_tr, alpha_tr, C_tr_source, delta_GM_tr, specific orbital observable",
            "blocks_claim_because": "finite-range profile and source-normalization operator are missing",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "projection_id": "APR899_4_boundary_tail",
            "arena": "boundary_local_projection",
            "minimal_projection": "trace residual -> local projection contamination/no-tail certificate",
            "must_supply": "B_tr_tail/K_perp_trace bound or parent no-tail theorem",
            "blocks_claim_because": "boundary/EFT re-entry is not ruled out",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def theorem_zero_reopen_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "TZR899_0_vertical_generator",
            "target_zero": "Dq_loc[v_tr]=0",
            "required_signature": "parent-owned ell_tr/K_parent/v_tr/P_tr plus local support or exact-gauge proof",
            "current_status": "unsigned",
            "if_closed": "Q_tr and J_tr source-cokernel proof can be reattempted",
            "if_open": "residual source pack remains mandatory",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "TZR899_1_matter_descent",
            "target_zero": "partial_vtr S_matter=0",
            "required_signature": "S_matter factors through q_loc and theta has no Lie_vtr marker",
            "current_status": "unsigned",
            "if_closed": "Q_tr^A=0 can become a theorem",
            "if_open": "species and universal Q_tr rows must be sourced/bounded",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "TZR899_2_no_pole_rank_zero",
            "target_zero": "no local source-coupled trace pole",
            "required_signature": "rank(P_loc P_tr P_loc^dagger)=0 or H_tr reduced inverse has no local source pole",
            "current_status": "unsigned",
            "if_closed": "Z_tr/lambda_tr finite-carrier rows become absent_by_theorem",
            "if_open": "Z_tr and lambda_tr must be derived from parent action",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "TZR899_3_double_zero_response",
            "target_zero": "C_tr(Phi0)=0 and partial_A C_tr(Phi0)=0",
            "required_signature": "response functional is quadratic or higher in a parent zero-mode norm, not a linear marker",
            "current_status": "unsigned",
            "if_closed": "PPN/clock/source first-order leakage can be structurally silent",
            "if_open": "response coefficients must be computed and bounded",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "TZR899_4_boundary_no_tail",
            "target_zero": "B_tr_tail=0 and K_perp_trace=0 locally",
            "required_signature": "compact local projection kills boundary/exact trace current and no post-readout EFT term re-enters",
            "current_status": "unsigned",
            "if_closed": "local projection silence becomes stable",
            "if_open": "boundary tail remains an explicit contamination guard",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def claim_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    gates = [
        ("CGATE899_0_R10", "R10_short_range", "Z_tr/lambda_tr/Q_tr and full R10 curve are missing"),
        ("CGATE899_1_PPN", "PPN", "weak-field response operator is missing"),
        ("CGATE899_2_WEP_clock_EM", "WEP_clock_EM", "species no-marker and clock/EM functionals are unsigned"),
        ("CGATE899_3_orbital_Newton", "orbital_Newton", "alpha/lambda/source-normalization and selected orbital bound are missing"),
        ("CGATE899_4_local_GR", "local_GR_Newton", "trace channel is unresolved and broader local-GR gates remain open"),
    ]
    return [
        {
            "gate_id": gate_id,
            "arena": arena,
            "trace_inputs_ready": False,
            "bound_inputs_claim_grade": False,
            "prediction_numeric": False,
            "claim_allowed": False,
            "blocker": blocker,
            "next_action": "source residual row or parent-sign theorem-zero route",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
        for gate_id, arena, blocker in gates
    ]


def promotion_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "promotion_id": "PG899_0_residual_pack_executable",
            "target": "trace residual vector can be sent to local-bound tests",
            "required_to_pass": "every residual row is either parent-zeroed or has numeric sourced value, units, source path, and arena projection",
            "current_result": "fail_for_claim",
            "reason": "all rows remain MISSING or theorem-dependent",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "promotion_id": "PG899_1_R10_runner_claim",
            "target": "R10 alpha(lambda) comparison",
            "required_to_pass": "MTS runner rows and bound rows have positive numeric values and valid_for_claim=true",
            "current_result": "fail_for_claim",
            "reason": "dry rows intentionally contain MISSING markers and valid_for_claim=false",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "promotion_id": "PG899_2_theorem_zero_reopen",
            "target": "structural trace silence",
            "required_to_pass": "vertical generator, matter descent, no-pole, double-zero, and no-tail clauses are parent-signed",
            "current_result": "fail_for_claim",
            "reason": "all theorem-zero reopen gates are unsigned",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "promotion_id": "PG899_3_local_GR",
            "target": "local GR/Newton reduction",
            "required_to_pass": "trace residual closed plus EH operator, projector stress, conservation/source normalization, and known limits closed",
            "current_result": "fail_for_claim",
            "reason": "899 is only the trace residual source interface, not a full local-GR proof",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def route_choice_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC899_0_selected",
            "route": "priority_source_acquisition_or_theorem_zero_reopen",
            "status": "selected",
            "reason": "the residual vector is now wired to bounds; the next useful move is to attack the highest-leverage missing inputs rather than add more closure prose",
            "include": "Z_tr/lambda_tr no-pole gate, Q_tr source-cokernel, PPN response, species/clock/EM markers, source normalization, boundary no-tail",
            "exclude": "claim scoring with placeholders, free fitted coupling, GitHub action, formalization-workbench edits",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "GUARD899_0_no_R10_claim",
            "forbidden_claim": "MTS trace branch passes R10",
            "status": "forbidden",
            "reason": "alpha_tr(lambda_tr) has no sourced numeric MTS rows and the bound curve is placeholder-only",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "GUARD899_1_no_PPN_WEP_clock_claim",
            "forbidden_claim": "trace branch passes PPN/WEP/clock/EM tests",
            "status": "forbidden",
            "reason": "arena response operators and species/clock/EM functionals are missing",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "GUARD899_2_no_zero_theorem_claim",
            "forbidden_claim": "J_tr=0 or Q_tr^A=0 is proven",
            "status": "forbidden",
            "reason": "vertical generator, matter descent, no-pole, double-zero, and no-tail routes remain unsigned",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "GUARD899_3_no_local_GR_claim",
            "forbidden_claim": "local GR/Newton reduction is derived",
            "status": "forbidden",
            "reason": "trace residual source pack is only one blocked branch of the local-GR proof",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "GUARD899_4_allowed_private_result",
            "forbidden_claim": "none",
            "status": "allowed_private_nonclaim",
            "reason": "899 safely converts the trace residual vector into a source/bound interface with all claims blocked",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D899_0",
            "finding": "trace_residual_source_pack_built",
            "reason": "all eight 898 residual quantities now map to source requirements, theorem-zero reopen routes, and local bound interfaces",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D899_1",
            "finding": "R10_runner_dry_interface_only",
            "reason": "dry rows match the runner schema but intentionally fail validation due MISSING markers and valid_for_claim=false",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D899_2",
            "finding": "next_best_move_is_priority_source_or_zero",
            "reason": "the interface shows the shortest path is either parent-sign no-pole/source-cokernel/double-zero, or source real residual coefficients and bounds",
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
            "objective": "choose the highest-leverage trace residual input and either parent-sign its theorem-zero route or source a claim-grade numeric row",
            "include": "first attack Z_tr/lambda_tr no-pole and Q_tr source-cokernel because they control R10/orbital amplitude and matter coupling",
            "exclude": "fitted tiny couplings, placeholder alpha rows, public claim, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def prior_898_clean() -> bool:
    path = OUT / "P8_Y5_BRR545_898_VALIDATION.csv"
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


def row_has_missing_marker(row: dict[str, object]) -> bool:
    return "MISSING" in json.dumps(row, sort_keys=True)


def generated_rows_nonclaim(row_groups: list[list[dict[str, object]]]) -> bool:
    for group in row_groups:
        for row in group:
            if "valid_for_claim" in row and stringify(row["valid_for_claim"]).lower() != "false":
                return False
            if "claim_allowed" in row and stringify(row["claim_allowed"]).lower() != "false":
                return False
    return True


def import_r10_runner() -> Any:
    runner_path = ROOT / "scripts" / "R10_alpha_lambda_bound_prediction_runner.py"
    spec = importlib.util.spec_from_file_location("r10_runner_899", runner_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {runner_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_r10_dry_runner() -> dict[str, Any]:
    module = import_r10_runner()
    result = module.run_runner(
        OUT / "P8_Y5_R10_899_R10_RUNNER_DRY_ROWS.csv",
        LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv",
        OUT / "P8_Y5_R10_899_R10_RUNNER_DRY_RESULTS",
    )
    return result["status"]


def validation_rows(
    generated_utc: str,
    source_rows_: list[dict[str, object]],
    summary_rows_: list[dict[str, object]],
    residual_pack_rows_: list[dict[str, object]],
    local_interface_rows_: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    arena_rows_: list[dict[str, object]],
    theorem_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    promotion_rows_: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    guard_rows_: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    runner_status: dict[str, Any],
) -> list[dict[str, object]]:
    formalization_count = formalization_changed_count()
    row_groups = [
        summary_rows_,
        residual_pack_rows_,
        local_interface_rows_,
        dry_rows_,
        arena_rows_,
        theorem_rows_,
        claim_rows_,
        promotion_rows_,
        route_rows_,
        guard_rows_,
        decision_rows_,
        next_rows_,
    ]
    dry_schema_ok = [key for key in MTS_REQUIRED_COLUMNS if key not in dry_rows_[0]]
    checks = [
        {
            "check_id": "V899_0_sources_exist_and_needles",
            "result": "pass"
            if all(row["exists"] is True and row["needle_check"] == "pass" for row in source_rows_)
            else "fail",
            "detail": "all source paths exist and needles are present",
        },
        {
            "check_id": "V899_1_prior_898_clean",
            "result": "pass" if prior_898_clean() else "fail",
            "detail": "P8_Y5_BRR545_898_VALIDATION.csv clean",
        },
        {
            "check_id": "V899_2_residual_pack_covers_898_vector",
            "result": "pass"
            if len(residual_pack_rows_) == 8
            and residual_pack_rows_[0]["residual_id"] == "TRV898_0_Ztr"
            and residual_pack_rows_[-1]["residual_id"] == "TRV898_7_boundary_tail"
            else "fail",
            "detail": f"residual_pack_rows={len(residual_pack_rows_)}",
        },
        {
            "check_id": "V899_3_residual_pack_missing_nonclaim",
            "result": "pass"
            if all(row_has_missing_marker(row) and row["valid_for_claim"] is False for row in residual_pack_rows_)
            else "fail",
            "detail": "all residual rows remain missing/theorem-dependent and nonclaim",
        },
        {
            "check_id": "V899_4_local_bound_interfaces_blocked",
            "result": "pass"
            if all(row["claim_allowed"] is False and row["valid_for_claim"] is False for row in local_interface_rows_)
            else "fail",
            "detail": f"local_interface_rows={len(local_interface_rows_)} blocked",
        },
        {
            "check_id": "V899_5_R10_dry_rows_match_runner_schema",
            "result": "pass" if not dry_schema_ok else "fail",
            "detail": "schema ok" if not dry_schema_ok else "missing=" + ",".join(dry_schema_ok),
        },
        {
            "check_id": "V899_6_R10_dry_runner_blocks_claim",
            "result": "pass"
            if runner_status.get("claim_allowed") is False
            and runner_status.get("valid_mts_rows") == 0
            and runner_status.get("blocked_or_failed_rows", 0) >= 1
            else "fail",
            "detail": json.dumps(
                {
                    "claim_allowed": runner_status.get("claim_allowed"),
                    "valid_mts_rows": runner_status.get("valid_mts_rows"),
                    "blocked_or_failed_rows": runner_status.get("blocked_or_failed_rows"),
                },
                sort_keys=True,
            ),
        },
        {
            "check_id": "V899_7_theorem_zero_reopen_unsigned",
            "result": "pass"
            if len(theorem_rows_) == 5
            and all(row["current_status"] == "unsigned" and row["claim_allowed"] is False for row in theorem_rows_)
            else "fail",
            "detail": "vertical, matter, no-pole, double-zero, and no-tail gates remain unsigned",
        },
        {
            "check_id": "V899_8_all_claim_gates_false",
            "result": "pass" if all(row["claim_allowed"] is False for row in claim_rows_) else "fail",
            "detail": "R10/PPN/WEP-clock/orbital/local-GR gates all false",
        },
        {
            "check_id": "V899_9_all_generated_rows_nonclaim",
            "result": "pass" if generated_rows_nonclaim(row_groups) else "fail",
            "detail": "all generated claim_allowed/valid_for_claim flags remain false",
        },
        {
            "check_id": "V899_10_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V899_11_route_selected",
            "result": "pass" if next_rows_ and next_rows_[0]["next_target"] == NEXT_TARGET else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V899_12_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        },
    ]
    for row in checks:
        row["generated_utc"] = generated_utc
    return checks


def write_markdown(
    path: Path,
    generated_utc: str,
    summary_rows_: list[dict[str, object]],
    source_rows_: list[dict[str, object]],
    residual_pack_rows_: list[dict[str, object]],
    local_interface_rows_: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    arena_rows_: list[dict[str, object]],
    theorem_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    promotion_rows_: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    guard_rows_: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    content = f"""# 899 - Y5/R10 Trace Residual Vector Source Pack And Local Bound Interface

Status: `{STATUS}`
Claim ceiling: `{CLAIM_CEILING}`
Generated UTC: `{generated_utc}`

Current result: **the 898 trace residual vector is now wired into a claim-safe source pack and local-bound interface**. This is not a pass and not a local-GR derivation. It is the plumbing that prevents us from smuggling a tiny trace coupling into the theory: every residual quantity must now either be parent-zeroed by theorem or sourced numerically before R10, PPN, WEP, clock, EM, orbital, Newtonian-source, or local-GR language is allowed.

## Exact 899 Finding
The coupling problem is now mechanically exposed. The shortest honest route is still theorem-zero if the parent action can sign the vertical generator, matter descent, no-pole, double-zero, and no-tail clauses. If that route does not close, the source-pack tells us exactly what must be measured/derived: `Z_tr`, `lambda_tr`, `Q_tr/m`, species deltas, PPN response, clock/EM response, source-normalization response, and boundary-tail leakage. Until then the R10 runner can only dry-run schemas and must return `claim_allowed=false`.

## Nonclaim Summary
{md_table(summary_rows_)}

## Source Register
{md_table(source_rows_)}

## Trace Residual Source Pack
{md_table(residual_pack_rows_)}

## Local Bound Interface
{md_table(local_interface_rows_)}

## R10 Runner Dry Rows
{md_table(dry_rows_)}

## Arena Projection Requirements
{md_table(arena_rows_)}

## Theorem-Zero Reopen Gate
{md_table(theorem_rows_)}

## Claim Gate
{md_table(claim_rows_)}

## Promotion Gate
{md_table(promotion_rows_)}

## Route Choice
{md_table(route_rows_)}

## Claim Guard
{md_table(guard_rows_)}

## Decision
{md_table(decision_rows_)}

## Next Target
{md_table(next_rows_)}

## Validation
{md_table(validation_rows_)}
"""
    path.write_text(content, encoding="utf-8")


def main() -> None:
    generated_utc = now_utc()
    source_rows_ = source_register_rows(generated_utc)
    summary_rows_ = nonclaim_summary_rows(generated_utc)
    residual_pack_rows_ = residual_source_pack_rows(generated_utc)
    local_interface_rows_ = local_bound_interface_rows(generated_utc)
    dry_rows_ = r10_runner_dry_rows(generated_utc)
    arena_rows_ = arena_projection_requirement_rows(generated_utc)
    theorem_rows_ = theorem_zero_reopen_gate_rows(generated_utc)
    claim_rows_ = claim_gate_rows(generated_utc)
    promotion_rows_ = promotion_gate_rows(generated_utc)
    route_rows_ = route_choice_rows(generated_utc)
    guard_rows_ = claim_guard_rows(generated_utc)
    decision_rows_ = decision_rows(generated_utc)
    next_rows_ = next_target_rows(generated_utc)

    first_outputs = {
        "P8_Y5_R10_899_SOURCE_REGISTER.csv": source_rows_,
        "P8_Y5_R10_899_TRACE_RESIDUAL_SOURCE_PACK.csv": residual_pack_rows_,
        "P8_Y5_R10_899_LOCAL_BOUND_INTERFACE.csv": local_interface_rows_,
        "P8_Y5_R10_899_R10_RUNNER_DRY_ROWS.csv": dry_rows_,
        "P8_Y5_R10_899_ARENA_PROJECTION_REQUIREMENTS.csv": arena_rows_,
        "P8_Y5_R10_899_THEOREM_ZERO_REOPEN_GATE.csv": theorem_rows_,
        "P8_Y5_R10_899_CLAIM_GATE.csv": claim_rows_,
        "P8_Y5_R10_899_PROMOTION_GATE.csv": promotion_rows_,
        "P8_Y5_R10_899_ROUTE_CHOICE.csv": route_rows_,
        "P8_Y5_R10_899_CLAIM_GUARD.csv": guard_rows_,
        "P8_Y5_R10_899_DECISION.csv": decision_rows_,
        "P8_Y5_R10_899_NEXT_TARGET.csv": next_rows_,
        "P8_Y5_R10_899_NONCLAIM_SUMMARY.csv": summary_rows_,
    }
    for filename, rows in first_outputs.items():
        write_csv(OUT / filename, rows)

    runner_status = run_r10_dry_runner()
    validation_rows_ = validation_rows(
        generated_utc,
        source_rows_,
        summary_rows_,
        residual_pack_rows_,
        local_interface_rows_,
        dry_rows_,
        arena_rows_,
        theorem_rows_,
        claim_rows_,
        promotion_rows_,
        route_rows_,
        guard_rows_,
        decision_rows_,
        next_rows_,
        runner_status,
    )
    write_csv(OUT / "P8_Y5_BRR545_899_VALIDATION.csv", validation_rows_)

    doc_path = ROOT / "899-Y5-R10-trace-residual-vector-source-pack-and-local-bound-interface.md"
    write_markdown(
        doc_path,
        generated_utc,
        summary_rows_,
        source_rows_,
        residual_pack_rows_,
        local_interface_rows_,
        dry_rows_,
        arena_rows_,
        theorem_rows_,
        claim_rows_,
        promotion_rows_,
        route_rows_,
        guard_rows_,
        decision_rows_,
        next_rows_,
        validation_rows_,
    )

    failed = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"wrote {doc_path}")
    print(f"wrote {OUT / 'P8_Y5_BRR545_899_VALIDATION.csv'}")
    print(f"status={STATUS}")
    if failed:
        print("failed_validation=" + ",".join(row["check_id"] for row in failed))
        raise SystemExit(1)


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

STATUS = "Y5_R10_882_relative_chain_action_shape_written_Qstar_endpoint_variation_obstruction_found_retained_cT_minimum_pack_staged_nonclaim"
CLAIM_CEILING = "relative_chain_action_shape_and_retained_source_pack_only_no_Qstar_unit_no_DeltaR_prediction_no_Ptr_Htr_no_R10_PPN_or_local_GR_claim"
NEXT_TARGET = "883-Y5-R10-Qstar-superselection-or-Ward-norm-sector-and-cT-source-pack-prioritization.md"


SOURCES = [
    {
        "source_id": "881_doc",
        "path": ROOT / "881-Y5-R10-Qstar-Ward-normalization-and-oriented-boundary-signature-or-retained-cT-bound-runner.md",
        "needle": "relative-chain boundary object",
        "role": "immediate relative-chain/Qstar handoff",
    },
    {
        "source_id": "881_validation",
        "path": OUT / "P8_Y5_BRR545_881_VALIDATION.csv",
        "needle": "V881_12_validation_rows_ready",
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "109_boundary_charge",
        "path": ROOT / "109-boundary-charge-two-ninth-theorem-attempt.md",
        "needle": "relative_boundary_language_exists",
        "role": "relative boundary language and Qstar failure",
    },
    {
        "source_id": "111_variational_owner",
        "path": ROOT / "111-endpoint-quadratic-variational-owner-attempt.md",
        "needle": "Qstar_charge_metric_derived",
        "role": "formal potential, Qstar metric, and endpoint arrow blockers",
    },
    {
        "source_id": "862_trace_lift",
        "path": ROOT / "862-Y5-R10-trace-lift-endpoint-equation-and-coframe-pullback-closure.md",
        "needle": "DeltaQ_trace/Q_*",
        "role": "trace-lift/Qstar bridge",
    },
    {
        "source_id": "863_Ward_trace",
        "path": ROOT / "863-Y5-R10-Ward-trace-lift-current-and-coframe-pullback-zero-theorem.md",
        "needle": "Q_* = unit(J_trace,parent)",
        "role": "Qstar unit theorem target",
    },
    {
        "source_id": "864_split",
        "path": ROOT / "864-Y5-R10-local-global-quotient-split-and-endpoint-stationarity-parent-clause.md",
        "needle": "Qstar Normalization Audit",
        "role": "local/global split and Qstar normalization blocker",
    },
    {
        "source_id": "875_schema",
        "path": OUT / "P8_Y5_R10_875_CT_INPUT_SCHEMA.csv",
        "needle": "IN875_0_Z_T",
        "role": "retained cT coefficient schema",
    },
    {
        "source_id": "880_queue",
        "path": OUT / "P8_Y5_R10_880_RETAINED_CT_BOUND_QUEUE.csv",
        "needle": "RCB880_0_cT",
        "role": "retained cT/Ztr/lambdatr/Jtr queue",
    },
    {
        "source_id": "97_canonical_R",
        "path": ROOT / "97-canonical-R-theorem-attempt.md",
        "needle": "Q_* fixes the unit boundary charge scale",
        "role": "canonical Qstar/R theorem blocker",
    },
    {
        "source_id": "337_exact_readout",
        "path": ROOT / "337-exact-parent-pullback-selection-rule-gate.md",
        "needle": "q_trace = 2/27",
        "role": "conditional trace readout",
    },
    {
        "source_id": "338_readout_gate",
        "path": ROOT / "338-action-level-exact-readout-gate.md",
        "needle": "source-at-zero",
        "role": "readout/spurion guard",
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
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: stringify(row.get(key, "")) for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def has_needle(path: Path, needle: str) -> bool:
    return needle in read_text(path)


def md_table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        cells = [stringify(row.get(header, "")).replace("\n", " ") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def source_register_rows(generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source in SOURCES:
        path = Path(source["path"])
        needle = str(source["needle"])
        rows.append(
            {
                "source_id": source["source_id"],
                "path": str(path),
                "exists": path.exists(),
                "needle_check": "pass" if has_needle(path, needle) else "fail",
                "role": source["role"],
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
            "what_changed": "wrote the relative-chain endpoint action owner shape, tested whether varying Q_* derives the unit, and staged the minimum retained c_T source pack",
            "best_partial_result": "the oriented relative-chain action cleanly owns the sign pattern, but direct Q_* variation gives dS/dQ_*=-8 Q_*/81 at the target roots, so the endpoint action cannot derive a nonzero charge unit by itself",
            "hard_blockers": "separate Q_* superselection/Ward norm sector, parent relative-chain action owner, physical endpoint arrow, full K_parent extension, local no-hair/source-cokernel, numeric retained c_T inputs",
            "what_is_not_claimed": "Q_* derivation, DeltaR prediction, P_tr/H_tr promotion, c_T zero/pass, R10/PPN/WEP/clock/orbital pass, local GR/Newton",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def relative_chain_owner_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "owner_id": "RCO882_0_relative_chain_domain",
            "required_object": "oriented relative chain C_rel=(M;Sigma_early,Sigma_today)",
            "formal_clause": "partial C_rel = Sigma_early - Sigma_today, up to the chosen parent orientation convention",
            "if_signed": "boundary evaluations enter with the sign needed by the 880 endpoint action",
            "current_status": "shape_available_parent_owner_missing",
            "blocker": "relative boundary language exists, but no parent action declares C_rel as the fundamental boundary object",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "owner_id": "RCO882_1_trace_charge_map",
            "required_object": "Q_trace[Sigma]",
            "formal_clause": "Q_trace[Sigma]=int_Sigma star J_trace, with R_Sigma=Q_trace[Sigma]/Q_*",
            "if_signed": "endpoint variables become boundary charges rather than free roots",
            "current_status": "conditional_current_not_parent_owned",
            "blocker": "J_trace and its local no-hair class are still theorem targets",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "owner_id": "RCO882_2_endpoint_action",
            "required_object": "S_rel endpoint term",
            "formal_clause": "S_rel=Q_*^2 int_{partial C_rel} U(Q_trace/Q_*) = Q_*^2[U(R_early)-U(R_today)]",
            "if_signed": "stationarity gives U'(R_early)=U'(R_today)=0 with the oriented sign pattern",
            "current_status": "formal_owner_shape_written",
            "blocker": "U coefficients and Q_* unit are not derived from the parent action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "owner_id": "RCO882_3_boundary_variation",
            "required_object": "endpoint Euler equations",
            "formal_clause": "delta_Q S_rel = Q_* U'(R_early) delta Q_early - Q_* U'(R_today) delta Q_today",
            "if_signed": "both endpoints solve 27R^2-12R+1=0 without flipping the Hessian sign",
            "current_status": "conditional_variation_ok_if_Qstar_fixed",
            "blocker": "requires Q_* to be fixed/superselected during endpoint variation",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "owner_id": "RCO882_4_arrow",
            "required_object": "physical endpoint arrow",
            "formal_clause": "R_early=1/3 and R_today=1/9 selected by relaxation/expansion/entropy orientation, not by post-fit choice",
            "if_signed": "DeltaR=+2/9 becomes an oriented prediction candidate",
            "current_status": "not_derived",
            "blocker": "orientation gives subtraction order but does not assign high root to early by itself",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "owner_id": "RCO882_5_verdict",
            "required_object": "relative-chain owner",
            "formal_clause": "parent action must own C_rel, J_trace, Q_*, U, and arrow jointly",
            "if_signed": "endpoint route could re-enter P_tr/H_tr construction",
            "current_status": "partial_shape_only_nonclaim",
            "blocker": "Q_* and arrow remain missing; no promotion to local GR",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def qstar_variation_obstruction_rows(generated_utc: str) -> list[dict[str, object]]:
    u_early = Fraction(0, 1)
    u_today = Fraction(4, 81)
    delta_u = u_early - u_today
    derivative_coeff = 2 * delta_u
    return [
        {
            "obstruction_id": "QVO882_0_action",
            "test": "vary Q_* inside the same endpoint action",
            "calculation": "S_rel=Q_*^2[U(R_early)-U(R_today)], R_i=Q_i/Q_*",
            "result": "dS/dQ_*=2Q_*[U_e-U_t]-Q_*[R_e U'_e-R_t U'_t]",
            "status": "formula_ready",
            "consequence": "Q_* variation adds an extra Euler equation unless Q_* is fixed by another sector",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "obstruction_id": "QVO882_1_at_stationary_roots",
            "test": "evaluate at R_early=1/3, R_today=1/9 and U'=0",
            "calculation": "U(1/3)=0, U(1/9)=4/81, so U_e-U_t=-4/81",
            "result": f"dS/dQ_*={derivative_coeff} Q_* = -8 Q_*/81",
            "status": "nonzero_for_Qstar_nonzero",
            "consequence": "the endpoint action alone would force Q_*=0 or require an extra counter-sector; neither is a valid charge unit derivation",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "obstruction_id": "QVO882_2_fixed_unit_rule",
            "test": "hold Q_* fixed during endpoint variation",
            "calculation": "delta Q_* = 0 removes the extra equation and leaves U'(R_early)=U'(R_today)=0",
            "result": "endpoint roots are consistent only if Q_* is a parent-fixed unit/superselection parameter",
            "status": "requires_external_Qstar_owner",
            "consequence": "Q_* must come from Ward norm, charge quantum, or superselection sector outside S_rel",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "obstruction_id": "QVO882_3_counterterm_warning",
            "test": "add W(Q_*) to repair dS/dQ_*",
            "calculation": "W'(Q_*)=+8Q_*/81 at the selected roots would cancel the obstruction",
            "result": "possible but would be a new parent sector requiring independent derivation",
            "status": "allowed_future_route_not_inserted",
            "consequence": "do not add a Q_* counterterm merely to save the endpoint route",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "obstruction_id": "QVO882_4_verdict",
            "test": "can S_rel derive Q_*?",
            "calculation": "direct endpoint-action variation fails for nonzero Q_*",
            "result": "Q_* is not derivable from the 880/882 endpoint action alone",
            "status": "reject_endpoint_only_Qstar_derivation",
            "consequence": "next derivation must be Q_* superselection/Ward norm sector or switch to retained c_T inputs",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def qstar_owner_options_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "option_id": "QOO882_0_Ward_norm",
            "candidate_owner": "Q_* from parent Ward-current norm",
            "required_formula": "Q_*^2=<J_trace,J_trace>_parent or equivalent charge metric fixed before endpoint variation",
            "status": "best_next_derivation_target",
            "risk": "requires a parent inner product/measure and no calibration leakage",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "option_id": "QOO882_1_charge_quantum",
            "candidate_owner": "Q_* as trace charge quantum/superselection unit",
            "required_formula": "allowed boundary charges are integer/rational multiples of Q_*; q_trace=2/27 is a normalized exact readout",
            "status": "plausible_but_unsigned",
            "risk": "needs quantization/topological class theorem rather than chosen units",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "option_id": "QOO882_2_fixed_cell_trace",
            "candidate_owner": "Q_* from full-cell trace normalization",
            "required_formula": "full trace average and active readout fix a unit cell current before endpoint charge is formed",
            "status": "conditional_on_exact_readout",
            "risk": "337/338 still leave exact readout versus EFT/spurion proof open",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "option_id": "QOO882_3_Qstar_countersector",
            "candidate_owner": "new W(Q_*) normalization sector",
            "required_formula": "W'(Q_*) cancels endpoint obstruction and has independent parent justification",
            "status": "last_resort",
            "risk": "looks like a target-fitted counterterm unless independently derived",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "option_id": "QOO882_4_no_owner",
            "candidate_owner": "no Q_* theorem found",
            "required_formula": "demote DeltaR amplitude route to closure/retained branch",
            "status": "fallback_if_883_fails",
            "risk": "cosmology amplitude remains useful but not derived",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def retained_ct_minimum_pack_rows(generated_utc: str) -> list[dict[str, object]]:
    source_path = OUT / "P8_Y5_R10_880_RETAINED_CT_BOUND_QUEUE.csv"
    return [
        {
            "pack_id": "MCP882_0_Ztr",
            "quantity": "Z_tr",
            "minimum_required_value": "numeric positive or zero-return certificate",
            "units": "parent_defined_kinetic_normalization",
            "needed_for": "R10 amplitude, orbital profile, ghost/no-pole decision",
            "current_value": "MISSING_PARENT_HESSIAN",
            "source_path": str(source_path),
            "status": "missing_blocks_claim",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "pack_id": "MCP882_1_lambdatr",
            "quantity": "lambda_tr_or_m_tr",
            "minimum_required_value": "numeric range/mass or proof of no physical pole",
            "units": "length_or_mass",
            "needed_for": "R10 alpha(lambda), orbital finite-range tests",
            "current_value": "MISSING_PARENT_HESSIAN_OR_NOPOLE",
            "source_path": str(source_path),
            "status": "missing_blocks_claim",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "pack_id": "MCP882_2_universal_charge",
            "quantity": "Q_tr_over_m_universal",
            "minimum_required_value": "numeric universal charge per inertial mass or theorem zero",
            "units": "charge_per_mass_parent_defined",
            "needed_for": "R10/orbital common-force score",
            "current_value": "MISSING_SOURCE_PROJECTION",
            "source_path": str(source_path),
            "status": "missing_blocks_claim",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "pack_id": "MCP882_3_species_charge",
            "quantity": "Delta_Q_tr_over_m_AB",
            "minimum_required_value": "numeric material/species differential charge or no-marker theorem",
            "units": "differential_charge_per_mass",
            "needed_for": "WEP and clock/material tests",
            "current_value": "MISSING_NO_MARKER_RESULT",
            "source_path": str(source_path),
            "status": "missing_blocks_claim",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "pack_id": "MCP882_4_metric_response",
            "quantity": "C_T_gamma,C_T_beta,C_T_source",
            "minimum_required_value": "numeric response operator or EH/same-frame absorption theorem",
            "units": "dimensionless_response",
            "needed_for": "PPN gamma/beta and Newtonian source normalization",
            "current_value": "MISSING_RESPONSE_OPERATOR",
            "source_path": str(source_path),
            "status": "missing_blocks_claim",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "pack_id": "MCP882_5_clock_response",
            "quantity": "C_T_clock",
            "minimum_required_value": "numeric clock response or proof matter constants factor through q_loc",
            "units": "fractional_clock_response",
            "needed_for": "clock/redshift/local constants tests",
            "current_value": "MISSING_CLOCK_RESPONSE",
            "source_path": str(source_path),
            "status": "missing_blocks_claim",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "pack_id": "MCP882_6_R10_bound_curve",
            "quantity": "alpha_bound(lambda)_R10",
            "minimum_required_value": "full source-backed curve or explicitly nonclaim anchor-only rows",
            "units": "dimensionless_alpha_vs_length",
            "needed_for": "R10 claim comparison",
            "current_value": "MISSING_FULL_CURVE_FOR_CLAIM",
            "source_path": str(source_path),
            "status": "missing_blocks_claim",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "pack_id": "MCP882_7_arena_projection",
            "quantity": "tau_R10,tau_PPN,tau_clock_WEP,tau_orbital",
            "minimum_required_value": "arena projection maps from c_T/Z_tr/lambda_tr/J_tr to observables",
            "units": "arena_dependent",
            "needed_for": "any retained c_T score",
            "current_value": "MISSING_ARENA_PROJECTION",
            "source_path": str(source_path),
            "status": "missing_blocks_claim",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "pack_id": "MCP882_8_source_provenance",
            "quantity": "source_path_and_units_for_every_numeric_input",
            "minimum_required_value": "local path/DOI/URL, extraction method, confidence, units, valid_for_claim flag",
            "units": "metadata",
            "needed_for": "claim hygiene",
            "current_value": "MISSING_NUMERIC_INPUTS",
            "source_path": str(source_path),
            "status": "schema_ready_no_claim",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC882_0_selected",
            "route": "Qstar_superselection_or_Ward_norm_sector_and_cT_source_pack_prioritization",
            "status": "selected",
            "reason": "direct Q_* variation inside the endpoint action fails, so the only derivation route is a separate parent-fixed Ward norm/superselection sector; retained c_T source pack is staged if that fails",
            "include": "Q_* Ward norm, charge quantum/superselection, exact readout unit, relative-chain owner, retained c_T source priority",
            "exclude": "DeltaR claim, local-GR/Newton pass, R10/PPN pass, fitted counterterm, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG882_0_no_Qstar_claim",
            "claim": "Q_* is derived by the endpoint action",
            "status": "forbidden",
            "reason": "Q_* variation gives -8 Q_*/81 at the selected roots and does not allow a nonzero unit",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG882_1_no_DeltaR_claim",
            "claim": "DeltaR=2/9 is parent predicted",
            "status": "forbidden",
            "reason": "Q_*, endpoint arrow, and parent relative-chain owner remain unsigned",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG882_2_no_Kparent_claim",
            "claim": "full K_parent/P_tr/H_tr are promoted",
            "status": "forbidden",
            "reason": "relative endpoint block does not supply full quotient tangent pairing or local no-hair",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG882_3_no_retained_cT_claim",
            "claim": "retained c_T is scored or passes bounds",
            "status": "forbidden",
            "reason": "minimum source pack has schema rows only and every numeric input is missing",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG882_4_no_local_GR_claim",
            "claim": "local GR/Newton follows",
            "status": "forbidden",
            "reason": "trace branch plus other local residual channels remain unclosed",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG882_5_allowed_private_result",
            "claim": "endpoint-only Q_* derivation is rejected and next route is sharper",
            "status": "allowed_private_nonclaim",
            "reason": "this prevents an invalid unit derivation and focuses 883 on superselection/Ward norm or retained source inputs",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D882_0",
            "finding": "relative_chain_action_shape_written",
            "reason": "oriented relative boundary action provides a coherent sign owner shape for U(R_early)-U(R_today)",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D882_1",
            "finding": "endpoint_only_Qstar_derivation_rejected",
            "reason": "varying Q_* gives a nonzero residual -8 Q_*/81 at the target roots",
            "status": STATUS,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D882_2",
            "finding": "retained_cT_minimum_pack_staged",
            "reason": "if Q_* superselection/Ward norm fails, the trace branch must be source-packed before any local bound scoring",
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
            "objective": "try to derive Q_* as a parent-fixed Ward norm or charge superselection sector; if not, prioritize the retained c_T source-pack inputs needed for real local-bound scoring",
            "include": "Q_* superselection, Ward-current inner product, exact readout unit, relative-chain owner, retained c_T source priority order",
            "exclude": "endpoint-only Q_* derivation, fitted Q_* counterterm, R10/local-GR pass, public claim, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def prior_881_clean() -> bool:
    path = OUT / "P8_Y5_BRR545_881_VALIDATION.csv"
    if not path.exists():
        return False
    return all(row.get("result") == "pass" for row in read_csv(path))


def formalization_changed_count() -> int:
    if not FORMALIZATION.exists():
        return -1
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > CUTOFF
    )


def all_nonclaim(row_sets: Iterable[list[dict[str, object]]]) -> bool:
    return all(row.get("valid_for_claim") is False for rows in row_sets for row in rows if "valid_for_claim" in row)


def validation_rows(
    source_rows: list[dict[str, object]],
    owner_rows: list[dict[str, object]],
    obstruction_rows: list[dict[str, object]],
    option_rows: list[dict[str, object]],
    pack_rows: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_target_rows_: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    generated_sets = [
        source_rows,
        owner_rows,
        obstruction_rows,
        option_rows,
        pack_rows,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
        summary_rows,
    ]
    source_ok = all(row["exists"] is True and row["needle_check"] == "pass" for row in source_rows)
    action_shape = any(row.get("owner_id") == "RCO882_2_endpoint_action" for row in owner_rows)
    qstar_obstruction = any(
        row.get("obstruction_id") == "QVO882_1_at_stationary_roots" and "-8 Q_*/81" in row.get("result", "")
        for row in obstruction_rows
    )
    endpoint_qstar_rejected = any(
        row.get("obstruction_id") == "QVO882_4_verdict" and row.get("status") == "reject_endpoint_only_Qstar_derivation"
        for row in obstruction_rows
    )
    external_owner_required = any(
        row.get("option_id") == "QOO882_0_Ward_norm" and row.get("status") == "best_next_derivation_target"
        for row in option_rows
    )
    retained_pack_ready = len(pack_rows) >= 9 and all(row.get("valid_for_claim") is False for row in pack_rows)
    retained_pack_missing = all("MISSING" in row.get("current_value", "") for row in pack_rows)
    claim_guards_closed = all(row.get("status") != "allowed_claim" for row in guard_rows) and all(
        row.get("claim_allowed") is False for row in decision_rows_
    )
    route_selected = route_rows_[0]["status"] == "selected" and next_target_rows_[0]["next_target"] == NEXT_TARGET
    fw_count = formalization_changed_count()
    checks = [
        ("V882_0_sources_exist_and_needles", source_ok, "all source paths exist and needles are present"),
        ("V882_1_prior_881_clean", prior_881_clean(), "P8_Y5_BRR545_881_VALIDATION.csv clean"),
        ("V882_2_relative_action_shape_written", action_shape, "relative-chain endpoint action shape recorded"),
        ("V882_3_Qstar_variation_obstruction_recorded", qstar_obstruction, "dS/dQ_*=-8 Q_*/81 at selected roots recorded"),
        ("V882_4_endpoint_only_Qstar_rejected", endpoint_qstar_rejected, "endpoint-only Q_* derivation rejected"),
        ("V882_5_external_Qstar_owner_required", external_owner_required, "Ward norm/superselection selected as next Q_* route"),
        ("V882_6_retained_pack_ready", retained_pack_ready, "minimum retained c_T source pack staged"),
        ("V882_7_retained_pack_missing_inputs", retained_pack_missing, "retained pack rows remain missing and nonclaim"),
        ("V882_8_claim_allowed_false", claim_guards_closed, "claim guards and decision rows keep claim_allowed=false"),
        ("V882_9_all_rows_nonclaim", all_nonclaim(generated_sets), "all generated rows valid_for_claim=false"),
        ("V882_10_formalization_workbench_untouched", fw_count == 0, f"formalization_changed_after_cutoff={fw_count}"),
        ("V882_11_route_selected", route_selected, NEXT_TARGET),
        ("V882_12_validation_rows_ready", True, "validation table constructed"),
    ]
    return [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]


def write_markdown(
    path: Path,
    generated_utc: str,
    summary_rows: list[dict[str, object]],
    source_rows: list[dict[str, object]],
    owner_rows: list[dict[str, object]],
    obstruction_rows: list[dict[str, object]],
    option_rows: list[dict[str, object]],
    pack_rows: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_target_rows_: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    sections = [
        "# 882 - Y5/R10 Relative-Chain Boundary Owner and Qstar Unit or Retained cT Minimum Source Pack",
        "",
        f"Status: `{STATUS}`  ",
        f"Claim ceiling: `{CLAIM_CEILING}`  ",
        f"Generated UTC: `{generated_utc}`",
        "",
        "Current result: **the relative-chain action shape is useful, but it rejects an endpoint-only `Q_*` derivation**. "
        "The clean formal owner is `S_rel=Q_*^2 int_{partial C_rel} U(Q_trace/Q_*)`, giving "
        "`Q_*^2[U(R_early)-U(R_today)]` when the oriented boundary is `Sigma_early-Sigma_today`. "
        "That owns the sign shape from 880, but varying `Q_*` in the same endpoint action gives "
        "`dS/dQ_*=-8 Q_*/81` at `R_early=1/3`, `R_today=1/9`. "
        "So the endpoint action cannot derive a nonzero `Q_*`; the unit must be fixed by a separate Ward norm, "
        "charge quantum, or superselection sector. Since the zero route remains unsigned, the minimum retained "
        "`c_T` source pack is staged, but every row remains nonclaim until real parent coefficients or source-backed inputs exist.",
        "",
        "## Nonclaim Summary",
        md_table(summary_rows),
        "",
        "## Source Register",
        md_table(source_rows),
        "",
        "## Relative Chain Owner",
        md_table(owner_rows),
        "",
        "## Qstar Variation Obstruction",
        md_table(obstruction_rows),
        "",
        "## Qstar Owner Options",
        md_table(option_rows),
        "",
        "## Retained cT Minimum Source Pack",
        md_table(pack_rows),
        "",
        "## Route Choice",
        md_table(route_rows_),
        "",
        "## Claim Guard",
        md_table(guard_rows),
        "",
        "## Decision",
        md_table(decision_rows_),
        "",
        "## Next Target",
        md_table(next_target_rows_),
        "",
        "## Validation",
        md_table(validation_rows_),
        "",
    ]
    path.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    generated_utc = now_utc()
    source_rows = source_register_rows(generated_utc)
    summary_rows = nonclaim_summary_rows(generated_utc)
    owner_rows = relative_chain_owner_rows(generated_utc)
    obstruction_rows = qstar_variation_obstruction_rows(generated_utc)
    option_rows = qstar_owner_options_rows(generated_utc)
    pack_rows = retained_ct_minimum_pack_rows(generated_utc)
    route_rows_ = route_rows(generated_utc)
    guard_rows = claim_guard_rows(generated_utc)
    decision_rows_ = decision_rows(generated_utc)
    next_target_rows_ = next_target_rows(generated_utc)
    validation_rows_ = validation_rows(
        source_rows,
        owner_rows,
        obstruction_rows,
        option_rows,
        pack_rows,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
        summary_rows,
    )

    outputs = {
        "P8_Y5_R10_882_SOURCE_REGISTER.csv": source_rows,
        "P8_Y5_R10_882_RELATIVE_CHAIN_OWNER.csv": owner_rows,
        "P8_Y5_R10_882_QSTAR_VARIATION_OBSTRUCTION.csv": obstruction_rows,
        "P8_Y5_R10_882_QSTAR_OWNER_OPTIONS.csv": option_rows,
        "P8_Y5_R10_882_RETAINED_CT_MINIMUM_SOURCE_PACK.csv": pack_rows,
        "P8_Y5_R10_882_ROUTE_CHOICE.csv": route_rows_,
        "P8_Y5_R10_882_CLAIM_GUARD.csv": guard_rows,
        "P8_Y5_R10_882_DECISION.csv": decision_rows_,
        "P8_Y5_R10_882_NEXT_TARGET.csv": next_target_rows_,
        "P8_Y5_R10_882_NONCLAIM_SUMMARY.csv": summary_rows,
        "P8_Y5_BRR545_882_VALIDATION.csv": validation_rows_,
    }
    for filename, rows in outputs.items():
        write_csv(OUT / filename, rows)

    doc_path = ROOT / "882-Y5-R10-relative-chain-boundary-owner-and-Qstar-unit-or-retained-cT-minimum-source-pack.md"
    write_markdown(
        doc_path,
        generated_utc,
        summary_rows,
        source_rows,
        owner_rows,
        obstruction_rows,
        option_rows,
        pack_rows,
        route_rows_,
        guard_rows,
        decision_rows_,
        next_target_rows_,
        validation_rows_,
    )

    failed = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"wrote {doc_path}")
    print(f"wrote {OUT / 'P8_Y5_BRR545_882_VALIDATION.csv'}")
    print(f"status={STATUS}")
    if failed:
        print("failed_validation=" + ",".join(row["check_id"] for row in failed))
        raise SystemExit(1)


if __name__ == "__main__":
    main()

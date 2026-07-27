from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "863-Y5-R10-Ward-trace-lift-current-and-coframe-pullback-zero-theorem.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_863_SOURCE_REGISTER.csv"
WARD_TRACE_CURRENT_PATH = RESIDUALS / "P8_Y5_R10_863_WARD_TRACE_CURRENT_DERIVATION.csv"
TRACE_ENDPOINT_PATH = RESIDUALS / "P8_Y5_R10_863_TRACE_LIFT_ENDPOINT_CONSTRAINT.csv"
COFRAME_ZERO_PATH = RESIDUALS / "P8_Y5_R10_863_COFRAME_ZERO_THEOREM.csv"
LOCAL_RESIDUAL_PATH = RESIDUALS / "P8_Y5_R10_863_LOCAL_RESIDUAL_FORK.csv"
GR_NEWTON_PATH = RESIDUALS / "P8_Y5_R10_863_GR_NEWTON_REQUIREMENT_LEDGER.csv"
ROUTE_CHOICE_PATH = RESIDUALS / "P8_Y5_R10_863_ROUTE_CHOICE.csv"
CLAIM_GUARD_PATH = RESIDUALS / "P8_Y5_R10_863_CLAIM_GUARD.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_863_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_863_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_863_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_863_VALIDATION.csv"

PRIOR_VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_862_VALIDATION.csv"

STATUS = "Y5_R10_863_conditional_local_global_quotient_trace_theorem_written_parent_action_unsigned_nonclaim"
CLAIM_CEILING = "conditional_current_and_coframe_zero_contract_only_no_2over27_prediction_no_local_GR_claim"
NEXT_TARGET = "864-Y5-R10-local-global-quotient-split-and-endpoint-stationarity-parent-clause.md"

SOURCE_SPECS = [
    {
        "source_id": "862_doc",
        "path": POST_CHECKPOINT / "862-Y5-R10-trace-lift-endpoint-equation-and-coframe-pullback-closure.md",
        "needles": [
            "the trace-lift route is sharper, but still not closed",
            "TL862_3_endpoint_identification",
            "863-Y5-R10-Ward-trace-lift-current-and-coframe-pullback-zero-theorem.md",
        ],
        "role": "immediate trace-current/coframe-zero handoff",
    },
    {
        "source_id": "862_validation",
        "path": PRIOR_VALIDATION_PATH,
        "needles": [
            "V862_7_route_selected,pass",
            "V862_9_all_rows_nonclaim,pass",
            "V862_11_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "337_exact_pullback",
        "path": POST_CHECKPOINT / "337-exact-parent-pullback-selection-rule-gate.md",
        "needles": [
            "full S27 cell equivalence",
            "q_trace = 2/27",
            "epsilon_H = 1",
        ],
        "role": "conditional exact readout for trace charge",
    },
    {
        "source_id": "356_Ward_identity",
        "path": POST_CHECKPOINT / "356-parent-action-ward-identity-and-projector-variation.md",
        "needles": [
            "Ward Identity Derivation",
            "F_boundary^nu",
            "F_matter_nonmetric^nu",
        ],
        "role": "parent Ward force-channel ledger",
    },
    {
        "source_id": "384_first_variation",
        "path": POST_CHECKPOINT / "384-parent-action-first-variation-obstruction-map.md",
        "needles": [
            "observed-coframe selector pullback",
            "Pi_I^matter",
            "first unowned term",
        ],
        "role": "coframe pullback obstruction source",
    },
    {
        "source_id": "385_pullback_cancellation",
        "path": POST_CHECKPOINT / "385-observed-coframe-selector-pullback-cancellation-theorem.md",
        "needles": [
            "Pi_I^matter not cancelled",
            "identity coframe",
            "Ward-owned counterstress",
        ],
        "role": "allowed coframe-pullback closure routes",
    },
    {
        "source_id": "565_vertical_observation",
        "path": POST_CHECKPOINT / "565-Y5-R10-coframe-pullback-zero-or-finite-alpha-coefficient.md",
        "needles": [
            "X is vertical to the observed quotient",
            "partial_X hat_g = DObs(Dq[X]) = 0",
            "vertical observation theorem is the clean proof shape",
        ],
        "role": "chain-rule theorem template for matter blindness",
    },
    {
        "source_id": "566_primitive_quotient",
        "path": POST_CHECKPOINT / "566-Y5-R10-primitive-quotient-no-marker-parent-clause-or-alpha-coefficient-fill.md",
        "needles": [
            "primitive quotient/no-marker clause is sufficient but not derived",
            "Dq[X]=0 and DObs(Dq[X])=0",
            "no material/readout marker extension",
        ],
        "role": "sufficient quotient/no-marker parent clause",
    },
    {
        "source_id": "627_cg_zero_proof",
        "path": POST_CHECKPOINT / "627-Y5-R10-cg-bound-source-acquisition-or-local-geometry-zero-proof.md",
        "needles": [
            "v_X in ker(Dq)",
            "matter action descent",
            "boundary projection silence",
        ],
        "role": "local geometry zero-proof audit and unsigned clauses",
    },
    {
        "source_id": "630_coupling_gate",
        "path": POST_CHECKPOINT / "630-Y5-R10-cg-projection-parent-input-derivation-or-source-prior-envelope.md",
        "needles": [
            "the coupling is now isolated as the local-theory bottleneck",
            "matter action descends to the quotient",
            "linear_vs_two_leg_coupling_must_be_resolved",
        ],
        "role": "coupling/source-test ambiguity guard",
    },
]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def check_needles(path: Path, needles: list[str]) -> str:
    text = read_text(path)
    if not text:
        return "missing_path"
    missing_needles = [needle for needle in needles if needle not in text]
    if missing_needles:
        return "missing_needles:" + ";".join(missing_needles)
    return "pass"


def validation_file_clean(path: Path) -> tuple[bool, str]:
    if not path.exists():
        return False, f"missing={path}"
    failures: list[str] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("result") != "pass":
                failures.append(f"{row.get('check_id')}={row.get('result')}")
    if failures:
        return False, ";".join(failures)
    return True, f"{path.name} clean"


def formalization_workbench_modified_count() -> int:
    command = (
        "$fw='"
        + str(FORMALIZATION).replace("'", "''")
        + "'; "
        + "$cutoff=[datetime]'2026-05-31T14:42:00'; "
        + "(Get-ChildItem -LiteralPath $fw -Recurse -File | "
        + "Where-Object { $_.LastWriteTime -gt $cutoff }).Count"
    )
    completed = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        check=True,
        capture_output=True,
        text=True,
        timeout=20,
    )
    return int(completed.stdout.strip() or "0")


def source_register_rows(generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in SOURCE_SPECS:
        path = spec["path"]
        rows.append(
            {
                "source_id": spec["source_id"],
                "path": str(path),
                "exists": str(path.exists()).lower(),
                "needle_check": check_needles(path, spec["needles"]),
                "role": spec["role"],
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def ward_trace_current_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "step_id": "WTC863_0_parent_Ward_identity",
            "object": "total parent Ward identity",
            "candidate_equation": "nabla_mu T_tot^{mu nu} + F_X^nu + F_P^nu + F_boundary^nu + F_domain^nu + F_matter_nonmetric^nu = 0",
            "derivation_status": "imported_force_channel_ledger",
            "what_it_gives": "any trace current must be one explicit boundary/Ward channel, not a hidden fitted memory term",
            "missing_for_claim": "separate J_trace^mu from F_boundary^nu and show all non-trace local channels vanish or are retained",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "step_id": "WTC863_1_trace_current_definition",
            "object": "J_trace^mu",
            "candidate_equation": "J_trace^mu := sum_{i=1}^3 J_i^mu where each J_i^mu is the parent exact-readout current for one FLRW spatial trace leg",
            "derivation_status": "conditional_definition",
            "what_it_gives": "a real current-level meaning for DeltaR=3 q_trace",
            "missing_for_claim": "derive J_i^mu from the parent action and prove the three legs are equal by exact FLRW isotropy/readout symmetry",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "step_id": "WTC863_2_divergence_endpoint_equation",
            "object": "endpoint charge balance",
            "candidate_equation": "nabla_mu J_trace^mu = delta_Sigma_early Q_early - delta_Sigma_today Q_today + div J_exact + J_local_leak",
            "derivation_status": "candidate_balance_law",
            "what_it_gives": "endpoint stationarity can become a Noether/Ward balance instead of a fitted value",
            "missing_for_claim": "prove J_local_leak=0 and derive endpoint boundary conditions from the action",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "step_id": "WTC863_3_charge_integral",
            "object": "DeltaQ_trace",
            "candidate_equation": "DeltaQ_trace/Q_* = integral_{Sigma_early-Sigma_today} J_trace/Q_* = 3 q_trace",
            "derivation_status": "conditional_if_WTC863_1_and_WTC863_2_close",
            "what_it_gives": "with q_trace=2/27, this gives DeltaR=2/9",
            "missing_for_claim": "Q_* normalization and equality between DeltaQ_trace/Q_* and cosmological DeltaR",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "step_id": "WTC863_4_local_projection_silence",
            "object": "P_loc J_trace^mu",
            "candidate_equation": "P_loc J_trace^mu = 0 while P_FLRW J_trace^mu may be nonzero",
            "derivation_status": "new_required_split",
            "what_it_gives": "the same trace charge can drive FLRW memory without becoming local PPN/WEP/clock hair",
            "missing_for_claim": "local/global quotient split theorem and boundary no-hair proof",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "step_id": "WTC863_5_failure_branch",
            "object": "retained local trace leakage",
            "candidate_equation": "P_loc J_trace^mu != 0 => q_loc^nu residual, PPN/WEP/clock/orbital rows",
            "derivation_status": "fallback_required",
            "what_it_gives": "prevents hiding a failed zero theorem",
            "missing_for_claim": "source-normalized residual coefficients if zero theorem stays unsigned",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def trace_endpoint_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "constraint_id": "TEC863_0_exact_readout_charge",
            "premise": "q_trace is the exact S27 parent readout",
            "mathematical_form": "q_trace = Tr(P_active H_parent)/27 = 2/27",
            "status": "conditional_import_from_337",
            "if_satisfied": "one trace leg has fixed charge 2/27",
            "if_missing": "the number remains a reduced-sector readout, not a parent prediction",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "constraint_id": "TEC863_1_FLRW_three_leg_lift",
            "premise": "FLRW endpoint sees exactly three equal spatial trace legs and no extra scalar/vector/tensor leakage",
            "mathematical_form": "DeltaQ_trace/Q_* = q_1+q_2+q_3 = 3 q_trace",
            "status": "conditional_new_theorem_shape",
            "if_satisfied": "DeltaR=2/9 follows from q_trace=2/27",
            "if_missing": "DeltaR=3q_trace is only an imposed projection rule",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "constraint_id": "TEC863_2_endpoint_stationarity",
            "premise": "Q_early and Q_today solve parent boundary Euler/Ward endpoint equations",
            "mathematical_form": "delta S_boundary/dQ_early=0 and delta S_boundary/dQ_today=0",
            "status": "not_parent_derived",
            "if_satisfied": "endpoint values are not fitted from cosmology",
            "if_missing": "the endpoint difference remains vulnerable to target inversion",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "constraint_id": "TEC863_3_Qstar_unit",
            "premise": "Q_* is the parent-normalized unit of trace charge",
            "mathematical_form": "Q_* = unit(J_trace,parent)",
            "status": "missing_normalization",
            "if_satisfied": "DeltaR becomes dimensionless and source-normalized",
            "if_missing": "the 2/9 ratio lacks an action-owned unit",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "constraint_id": "TEC863_4_no_target_inversion",
            "premise": "all above constraints are derived before data scoring",
            "mathematical_form": "b_P=2/27 independent of argmin_BIC(b_P)",
            "status": "future_promotion_gate",
            "if_satisfied": "2/27 can become a real prediction candidate",
            "if_missing": "keep b_P=2/27 as private conditional/theorem target only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def coframe_zero_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "theorem_id": "CZT863_0_chain_rule_zero",
            "claim_shape": "If q_loc:Phi->Q_loc, ehat=Obs_e(q_loc(Phi)), and v_I in ker(Dq_loc), then partial_I ehat=0.",
            "proof_line": "partial_I ehat = DObs_e(Dq_loc[v_I]) = DObs_e(0) = 0",
            "current_status": "conditional_proof_valid",
            "missing_parent_signature": "parent must identify the relevant endpoint/projector/memory variables as local-vertical directions",
            "local_GR_effect": "Pi_I^matter can vanish by chain rule for arbitrary matter stress",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "CZT863_1_matter_descent",
            "claim_shape": "S_matter = Sbar_matter[Obs(q_loc(Phi)), Psi, theta(q_loc)] with no representative marker extension.",
            "proof_line": "delta_v S_matter = (delta S/d ehat) partial_v ehat + (partial S/partial theta) partial_v theta = 0",
            "current_status": "sufficient_but_not_parent_derived",
            "missing_parent_signature": "quotient-only matter and no-marker/no-spurion constants remain a parent clause, not a theorem",
            "local_GR_effect": "kills direct WEP/clock/fifth-force matter pullback only if no hidden constants reintroduce v_I",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "CZT863_2_local_global_split",
            "claim_shape": "q_FLRW sees Q_trace, but q_loc does not: Dq_FLRW[v_Q] != 0 and Dq_loc[v_Q] = 0.",
            "proof_line": "the trace endpoint is a global/boundary observable, while local rods/clocks factor through q_loc only",
            "current_status": "best_new_clause_not_derived",
            "missing_parent_signature": "parent action must define two compatible quotient functors and an inclusion map showing no local hair",
            "local_GR_effect": "allows cosmological memory without local PPN/WEP/clock leakage",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "CZT863_3_endpoint_boundary_silence",
            "claim_shape": "boundary/exact terms from Q_trace have zero local projection",
            "proof_line": "P_loc(delta boundary exact current)=0 and no shear/vector/clock boundary components survive",
            "current_status": "not_parent_signed",
            "missing_parent_signature": "boundary no-hair theorem for trace endpoint current",
            "local_GR_effect": "blocks or allows q_loc^nu=0 depending on sign",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "CZT863_4_counterstress_fallback",
            "claim_shape": "If Pi_I^matter is not zero, include it in E_selector,I + Pi_I^matter = 0.",
            "proof_line": "Ward-owned counterstress is honest only if conserved and locally bounded/no-hair",
            "current_status": "fallback_modified_gravity_route",
            "missing_parent_signature": "counterstress coefficient and local residual vector",
            "local_GR_effect": "not a GR derivation unless the retained stress has zero local projection",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "CZT863_5_zero_verdict",
            "claim_shape": "Pi_I^matter=0 is derived for the trace endpoint/local projector branch.",
            "proof_line": "CZT863_0..CZT863_3 jointly parent-signed",
            "current_status": "not_proven",
            "missing_parent_signature": "local/global quotient split, matter descent, no-marker, boundary silence",
            "local_GR_effect": "local GR/Newton cannot be promoted from this branch yet",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def local_residual_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "fork_id": "LRF863_0_zero_branch",
            "condition": "P_loc J_trace=0, Pi_I^matter=0, F_P_bulk=0, boundary no-hair",
            "local_expression": "q_loc^nu=0 from trace/projector/coframe endpoint channels",
            "status": "conditional_not_parent_signed",
            "required_if_not": "none if fully signed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fork_id": "LRF863_1_trace_leak_branch",
            "condition": "P_loc J_trace != 0",
            "local_expression": "q_loc^nu includes trace endpoint flux",
            "status": "residual_required_if_zero_fails",
            "required_if_not": "PPN/clock/WEP/orbital source projection for trace leakage",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fork_id": "LRF863_2_coframe_pullback_branch",
            "condition": "Pi_I^matter != 0",
            "local_expression": "matter stress sources selector/projector equations",
            "status": "residual_required_if_zero_fails",
            "required_if_not": "c_g/source-test law or theorem-zero matter-frame descent",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fork_id": "LRF863_3_projector_stress_branch",
            "condition": "F_P_bulk or T_projector survives",
            "local_expression": "retained anisotropic/projector stress modifies exterior metric",
            "status": "residual_required_if_N5_fails",
            "required_if_not": "source-normalized PPN residual vector",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fork_id": "LRF863_4_coupling_ambiguity_branch",
            "condition": "finite common-frame coupling survives",
            "local_expression": "alpha/PPN/clock response depends on whether coupling is zero, one-leg, two-leg, or disformal",
            "status": "blocked_by_630_ambiguity",
            "required_if_not": "derive matter-frame variation and source/test current law",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def gr_newton_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "requirement_id": "GN863_0_one_observed_metric",
            "requirement": "ordinary matter, clocks, rulers, and photons see one local observed coframe/metric",
            "current_status": "conditional_via_quotient_descent",
            "needed_for": "WEP, redshift, Maxwell/light cone, PPN gamma",
            "blocking_clause": "matter-frame descent and no-marker theorem not parent-signed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "requirement_id": "GN863_1_Bianchi_safe_stress",
            "requirement": "all projector, boundary, domain, and memory stresses are zero locally or retained in conserved total stress",
            "current_status": "open",
            "needed_for": "GR reduction rather than fake dropped-stress GR",
            "blocking_clause": "N5/projector and boundary no-hair remain conditional",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "requirement_id": "GN863_2_Newtonian_source_lock",
            "requirement": "Poisson/Newton limit uses measured source mass and measured G without hidden memory source",
            "current_status": "not_checked_here",
            "needed_for": "Newtonian mechanics limit",
            "blocking_clause": "source normalization waits on q_loc and matter-frame closure",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "requirement_id": "GN863_3_trace_memory_cosmology",
            "requirement": "global trace endpoint can alter FLRW/cosmology while remaining locally silent",
            "current_status": "new_parent_clause_required",
            "needed_for": "unified field-theory route rather than patched cosmology-only model",
            "blocking_clause": "local/global quotient split not derived",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "requirement_id": "GN863_4_local_GR_verdict",
            "requirement": "local exterior reduces to GR/Newton",
            "current_status": "not_derived",
            "needed_for": "serious field-theory claim",
            "blocking_clause": "GN863_0..GN863_3 all need stronger parent signatures",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_choice_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC863_0_selected",
            "route": "local_global_quotient_split_and_endpoint_stationarity_parent_clause",
            "status": "selected",
            "reason": "the exact missing move is to make Q_trace globally observable for FLRW but locally vertical/invisible for rods, clocks, and PPN",
            "include": "q_FLRW/q_loc split, endpoint stationarity, Q_* unit, no-marker matter descent, boundary no-hair",
            "exclude": "new data scoring, fitted DeltaR, dropped projector stress, public claim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RC863_1_deferred",
            "route": "retained_residual_runner_for_failed_zero_theorem",
            "status": "deferred",
            "reason": "if local/global quotient split fails, local trace/coframe/projector residuals must be scored rather than ignored",
            "include": "PPN, clock, WEP, orbital and R10 coefficient rows",
            "exclude": "before the local/global split theorem is attempted once explicitly",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG863_0_no_Ward_current_claim",
            "claim": "J_trace^mu is derived from the parent action",
            "status": "forbidden",
            "reason": "863 writes the current contract but does not derive the action-level current",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG863_1_no_endpoint_prediction",
            "claim": "DeltaR=2/9 is predicted",
            "status": "forbidden",
            "reason": "endpoint stationarity and Q_* normalization remain unsigned",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG863_2_no_coframe_zero_claim",
            "claim": "Pi_I^matter=0 is proven",
            "status": "forbidden",
            "reason": "chain-rule zero is conditional on local quotient verticality and matter descent",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG863_3_no_local_GR_claim",
            "claim": "MTS reduces to GR/Newton locally",
            "status": "forbidden",
            "reason": "local/global split, source normalization, and projector/boundary stress closure remain open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG863_4_allowed_private_result",
            "claim": "local/global quotient split is the next exact parent-action target",
            "status": "allowed_private_nonclaim",
            "reason": "863 identifies the minimal clause that could reconcile cosmological memory with local GR silence",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D863_0",
            "finding": "Ward_trace_current_contract_written_not_derived",
            "reason": "DeltaR=3q_trace becomes a current theorem only if J_trace^mu is derived and its local leakage vanishes",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D863_1",
            "finding": "coframe_zero_has_clean_chain_rule_proof_shape",
            "reason": "Pi_I^matter vanishes if local observed geometry factors through a quotient that treats endpoint/projector variables as vertical",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D863_2",
            "finding": "new_core_clause_is_local_global_quotient_split",
            "reason": "MTS needs Q_trace visible to FLRW but invisible to local rods/clocks; that is now the exact parent-action contract",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def next_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "write or reject the parent action clause that makes trace memory globally visible to FLRW but locally quotient-vertical for matter/coframe variations",
            "include": "q_FLRW/q_loc functors, endpoint stationarity, Q_* normalization, matter descent, no-marker constants, boundary no-hair",
            "exclude": "new cosmology scoring, fitted endpoints, formalization-workbench edits, public claim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "generalized the vertical-observation proof shape to the trace-endpoint/local-GR branch and isolated the local/global quotient split as the exact missing clause",
            "best_partial_result": "if Q_trace is FLRW-visible but locally vertical, then P_loc J_trace=0 and Pi_I^matter=0 can both follow by quotient descent",
            "hard_blockers": "parent Ward trace current, endpoint stationarity, Q_* unit, local/global quotient split, no-marker matter descent, boundary no-hair",
            "what_is_not_claimed": "J_trace derivation, DeltaR=2/9 prediction, Pi_I^matter zero, q_loc zero, local GR/Newton",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_valid_for_claim_false(row_groups: list[list[dict[str, object]]]) -> bool:
    for rows in row_groups:
        for row in rows:
            if row.get("valid_for_claim") != "false":
                return False
    return True


def validation_rows(
    source_rows: list[dict[str, object]],
    ward_rows: list[dict[str, object]],
    endpoint_rows: list[dict[str, object]],
    coframe_rows: list[dict[str, object]],
    residual_rows: list[dict[str, object]],
    gr_rows: list[dict[str, object]],
    routes: list[dict[str, object]],
    guards: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
) -> list[dict[str, object]]:
    prior_clean, prior_detail = validation_file_clean(PRIOR_VALIDATION_PATH)
    formalization_count = formalization_workbench_modified_count()
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    ward_contract_ok = any(row["step_id"] == "WTC863_4_local_projection_silence" and row["derivation_status"] == "new_required_split" for row in ward_rows)
    endpoint_blocks_ok = any(row["constraint_id"] == "TEC863_2_endpoint_stationarity" and row["status"] == "not_parent_derived" for row in endpoint_rows)
    coframe_chain_ok = any(row["theorem_id"] == "CZT863_0_chain_rule_zero" and row["current_status"] == "conditional_proof_valid" for row in coframe_rows)
    coframe_not_claimed = any(row["theorem_id"] == "CZT863_5_zero_verdict" and row["current_status"] == "not_proven" for row in coframe_rows)
    residual_fallback_ok = len(residual_rows) == 5 and any(row["fork_id"] == "LRF863_4_coupling_ambiguity_branch" for row in residual_rows)
    gr_not_promoted = any(row["requirement_id"] == "GN863_4_local_GR_verdict" and row["current_status"] == "not_derived" for row in gr_rows)
    route_selected = any(row["route_id"] == "RC863_0_selected" for row in routes)
    no_claim = not any(row["claim_allowed"] == "true" for row in decisions)
    nonclaim_ok = all_valid_for_claim_false([source_rows, ward_rows, endpoint_rows, coframe_rows, residual_rows, gr_rows, routes, guards, decisions, next_targets, nonclaim])
    next_selected = bool(next_targets) and next_targets[0]["next_target"] == NEXT_TARGET
    return [
        {"check_id": "V863_0_sources_exist_and_needles", "result": "pass" if source_ok else "fail", "detail": "all source paths exist and needles are present" if source_ok else "source register has missing path or needle"},
        {"check_id": "V863_1_prior_862_clean", "result": "pass" if prior_clean else "fail", "detail": prior_detail},
        {"check_id": "V863_2_Ward_trace_contract_ready", "result": "pass" if ward_contract_ok else "fail", "detail": "local projection silence recorded as the new required split"},
        {"check_id": "V863_3_endpoint_blocks_claim", "result": "pass" if endpoint_blocks_ok else "fail", "detail": "endpoint stationarity remains not parent-derived"},
        {"check_id": "V863_4_coframe_chain_rule_zero_written", "result": "pass" if coframe_chain_ok else "fail", "detail": "conditional quotient chain-rule zero theorem recorded"},
        {"check_id": "V863_5_coframe_zero_not_promoted", "result": "pass" if coframe_not_claimed else "fail", "detail": "Pi_I^matter zero verdict remains not proven"},
        {"check_id": "V863_6_residual_fallbacks_ready", "result": "pass" if residual_fallback_ok else "fail", "detail": "trace, coframe, projector, and coupling residual forks recorded"},
        {"check_id": "V863_7_local_GR_not_promoted", "result": "pass" if gr_not_promoted else "fail", "detail": "local GR/Newton verdict remains not derived"},
        {"check_id": "V863_8_route_selected", "result": "pass" if route_selected else "fail", "detail": "local/global quotient split and endpoint stationarity selected"},
        {"check_id": "V863_9_claim_allowed_false", "result": "pass" if no_claim else "fail", "detail": "decision rows keep claim_allowed=false"},
        {"check_id": "V863_10_all_rows_nonclaim", "result": "pass" if nonclaim_ok else "fail", "detail": "all generated rows valid_for_claim=false"},
        {"check_id": "V863_11_next_target_selected", "result": "pass" if next_selected else "fail", "detail": NEXT_TARGET},
        {"check_id": "V863_12_formalization_workbench_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={formalization_count}"},
        {"check_id": "V863_13_validation_rows_ready", "result": "pass", "detail": "validation table constructed"},
    ]


def csv_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for row in rows:
        values = []
        for column in columns:
            text = str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            values.append(text)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_document(
    source_rows: list[dict[str, object]],
    ward_rows: list[dict[str, object]],
    endpoint_rows: list[dict[str, object]],
    coframe_rows: list[dict[str, object]],
    residual_rows: list[dict[str, object]],
    gr_rows: list[dict[str, object]],
    routes: list[dict[str, object]],
    guards: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 863 - Y5 R10 Ward Trace-Lift Current And Coframe Pullback Zero Theorem",
        "",
        "Current result: **the theorem shape is now explicit, but the parent action still has to sign it**. The only clean route is a local/global quotient split: the trace endpoint `Q_trace` must be visible to the FLRW quotient and endpoint Ward current, but vertical/invisible to the local quotient used by rods, clocks, matter stress, and PPN. If that split is parent-derived, then `P_loc J_trace=0` and `Pi_I^matter=0` can follow by the same chain-rule mechanism. If not, local residuals must be scored.",
        "",
        "## Non-Claim Summary",
        "",
        csv_table(nonclaim, ["status", "claim_ceiling", "what_changed", "best_partial_result", "hard_blockers", "what_is_not_claimed", "next_target", "valid_for_claim"]),
        "",
        "## Ward Trace Current Derivation",
        "",
        csv_table(ward_rows, ["step_id", "object", "candidate_equation", "derivation_status", "what_it_gives", "missing_for_claim", "valid_for_claim"]),
        "",
        "## Trace-Lift Endpoint Constraint",
        "",
        csv_table(endpoint_rows, ["constraint_id", "premise", "mathematical_form", "status", "if_satisfied", "if_missing", "valid_for_claim"]),
        "",
        "## Coframe Zero Theorem",
        "",
        csv_table(coframe_rows, ["theorem_id", "claim_shape", "proof_line", "current_status", "missing_parent_signature", "local_GR_effect", "valid_for_claim"]),
        "",
        "## Local Residual Fork",
        "",
        csv_table(residual_rows, ["fork_id", "condition", "local_expression", "status", "required_if_not", "valid_for_claim"]),
        "",
        "## GR/Newton Requirement Ledger",
        "",
        csv_table(gr_rows, ["requirement_id", "requirement", "current_status", "needed_for", "blocking_clause", "valid_for_claim"]),
        "",
        "## Route Choice",
        "",
        csv_table(routes, ["route_id", "route", "status", "reason", "include", "exclude", "valid_for_claim"]),
        "",
        "## Claim Guard",
        "",
        csv_table(guards, ["guard_id", "claim", "status", "reason", "valid_for_claim"]),
        "",
        "## Decision",
        "",
        csv_table(decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        csv_table(next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
        "",
        "## Source Register",
        "",
        csv_table(source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        csv_table(validation, ["check_id", "result", "detail"]),
        "",
    ]
    OUTPUT_DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    generated_utc = datetime.now(timezone.utc).isoformat(timespec="seconds")
    source_rows = source_register_rows(generated_utc)
    ward_rows = ward_trace_current_rows(generated_utc)
    endpoint_rows = trace_endpoint_rows(generated_utc)
    coframe_rows = coframe_zero_rows(generated_utc)
    residual_rows = local_residual_rows(generated_utc)
    gr_rows = gr_newton_rows(generated_utc)
    routes = route_choice_rows(generated_utc)
    guards = claim_guard_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    next_targets = next_target_rows(generated_utc)
    nonclaim = nonclaim_summary_rows(generated_utc)
    validation = validation_rows(
        source_rows,
        ward_rows,
        endpoint_rows,
        coframe_rows,
        residual_rows,
        gr_rows,
        routes,
        guards,
        decisions,
        next_targets,
        nonclaim,
    )

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(WARD_TRACE_CURRENT_PATH, ward_rows, ["step_id", "object", "candidate_equation", "derivation_status", "what_it_gives", "missing_for_claim", "valid_for_claim", "generated_utc"])
    write_csv(TRACE_ENDPOINT_PATH, endpoint_rows, ["constraint_id", "premise", "mathematical_form", "status", "if_satisfied", "if_missing", "valid_for_claim", "generated_utc"])
    write_csv(COFRAME_ZERO_PATH, coframe_rows, ["theorem_id", "claim_shape", "proof_line", "current_status", "missing_parent_signature", "local_GR_effect", "valid_for_claim", "generated_utc"])
    write_csv(LOCAL_RESIDUAL_PATH, residual_rows, ["fork_id", "condition", "local_expression", "status", "required_if_not", "valid_for_claim", "generated_utc"])
    write_csv(GR_NEWTON_PATH, gr_rows, ["requirement_id", "requirement", "current_status", "needed_for", "blocking_clause", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_CHOICE_PATH, routes, ["route_id", "route", "status", "reason", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_GUARD_PATH, guards, ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, nonclaim, ["status", "claim_ceiling", "what_changed", "best_partial_result", "hard_blockers", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_document(source_rows, ward_rows, endpoint_rows, coframe_rows, residual_rows, gr_rows, routes, guards, decisions, next_targets, nonclaim, validation)

    print(f"wrote={OUTPUT_DOC}")
    print(f"wrote={VALIDATION_PATH}")
    print(f"status={STATUS}")
    print("partial_theorem=Q_trace must be FLRW-visible but locally vertical; then P_loc J_trace=0 and Pi_I^matter=0 can follow conditionally")
    print(f"claim_ceiling={CLAIM_CEILING}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()

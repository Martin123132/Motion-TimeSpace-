from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "862-Y5-R10-trace-lift-endpoint-equation-and-coframe-pullback-closure.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_862_SOURCE_REGISTER.csv"
TRACE_LIFT_PATH = RESIDUALS / "P8_Y5_R10_862_TRACE_LIFT_THEOREM_ATTEMPT.csv"
ENDPOINT_CANDIDATES_PATH = RESIDUALS / "P8_Y5_R10_862_ENDPOINT_EQUATION_CANDIDATES.csv"
COFRAME_CLOSURE_PATH = RESIDUALS / "P8_Y5_R10_862_COFRAME_PULLBACK_CLOSURE_AUDIT.csv"
LOCAL_GR_IMPACT_PATH = RESIDUALS / "P8_Y5_R10_862_LOCAL_GR_IMPACT_LEDGER.csv"
ROUTE_CHOICE_PATH = RESIDUALS / "P8_Y5_R10_862_ROUTE_CHOICE.csv"
CLAIM_GUARD_PATH = RESIDUALS / "P8_Y5_R10_862_CLAIM_GUARD.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_862_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_862_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_862_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_862_VALIDATION.csv"

PRIOR_VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_861_VALIDATION.csv"

STATUS = "Y5_R10_862_trace_lift_bridge_conditional_endpoint_and_coframe_unsigned_nonclaim"
CLAIM_CEILING = "conditional_trace_lift_algebra_only_no_endpoint_equation_no_coframe_zero_no_local_GR_claim"
NEXT_TARGET = "863-Y5-R10-Ward-trace-lift-current-and-coframe-pullback-zero-theorem.md"

SOURCE_SPECS = [
    {
        "source_id": "861_doc",
        "path": POST_CHECKPOINT / "861-Y5-R10-Ward-owned-boundary-charge-endpoint-and-N5-projector-closure.md",
        "needles": [
            "DeltaR=3 q_trace",
            "observed-coframe pullback",
            "862-Y5-R10-trace-lift-endpoint-equation-and-coframe-pullback-closure.md",
        ],
        "role": "immediate trace-lift/coframe target handoff",
    },
    {
        "source_id": "861_validation",
        "path": PRIOR_VALIDATION_PATH,
        "needles": [
            "V861_8_route_selected,pass",
            "V861_10_all_rows_nonclaim,pass",
            "V861_12_formalization_workbench_untouched,pass",
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
        "role": "conditional exact-readout charge source",
    },
    {
        "source_id": "109_boundary_charge",
        "path": POST_CHECKPOINT / "109-boundary-charge-two-ninth-theorem-attempt.md",
        "needles": [
            "normalized boundary charge",
            "boundary_charge_unit_defined",
            "product_two_over_nine_derived",
        ],
        "role": "previous two-ninth endpoint theorem attempt",
    },
    {
        "source_id": "384_first_variation",
        "path": POST_CHECKPOINT / "384-parent-action-first-variation-obstruction-map.md",
        "needles": [
            "observed-coframe selector pullback",
            "Pi_I^matter",
            "first unowned term",
        ],
        "role": "total-variation coframe obstruction",
    },
    {
        "source_id": "385_pullback_cancellation",
        "path": POST_CHECKPOINT / "385-observed-coframe-selector-pullback-cancellation-theorem.md",
        "needles": [
            "Pi_I^matter not cancelled",
            "identity coframe",
            "Ward-owned selector counterstress",
        ],
        "role": "legal fates for the coframe pullback residual",
    },
    {
        "source_id": "356_Ward_projector",
        "path": POST_CHECKPOINT / "356-parent-action-ward-identity-and-projector-variation.md",
        "needles": [
            "Ward identity",
            "F_P^nu",
            "metric-dependent projector + dropped stress = fake GR",
        ],
        "role": "projector force must be Ward-owned or retained",
    },
    {
        "source_id": "347_local_GR",
        "path": POST_CHECKPOINT / "347-local-GR-parent-reduction-theorem-attempt.md",
        "needles": [
            "N5_projector_stress_Bianchi_safe",
            "T_projector",
            "conditional GR-reduction theorem",
        ],
        "role": "local GR reduction and N5 projector-stress blocker",
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


def trace_lift_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "theorem_step": "TL862_0_exact_readout_import",
            "object": "q_trace",
            "candidate_equation": "q_trace = Tr(P_active H_parent)/27 = 2/27",
            "result": "available only under exact parent readout from 337",
            "status": "conditional_import",
            "missing_for_claim": "parent action still has to prove exact readout rather than a Wilsonian chosen sector",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_step": "TL862_1_trace_current_definition",
            "object": "J_trace^mu",
            "candidate_equation": "J_trace^mu := sum_{i=1}^3 J_i^mu with isotropic FLRW trace projection",
            "result": "defines the only clean route to DeltaR=3 q_trace",
            "status": "definition_candidate_not_parent_owned",
            "missing_for_claim": "derive J_i^mu and the trace projection from the parent Ward current",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_step": "TL862_2_three_direction_lift",
            "object": "DeltaQ_trace",
            "candidate_equation": "DeltaQ_trace/Q_* = sum_{i=1}^3 q_trace = 3 q_trace",
            "result": "algebraically gives 2/9 if TL862_0 and TL862_1 are true",
            "status": "conditional_algebra_constructed",
            "missing_for_claim": "show the FLRW endpoint charge is exactly this trace-lifted current, not a fitted memory variable",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_step": "TL862_3_endpoint_identification",
            "object": "DeltaR",
            "candidate_equation": "DeltaR := (Q_early - Q_today)/Q_* = DeltaQ_trace/Q_*",
            "result": "this is the hard physical identification, not yet a theorem",
            "status": "central_unsigned_axiom",
            "missing_for_claim": "endpoint Euler/Ward equation selecting Q_early, Q_today, and Q_* before cosmology data",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_step": "TL862_4_amplitude_readout",
            "object": "b_P",
            "candidate_equation": "b_P = a_F DeltaR/(3 eta^2), with eta=1, a_F=1",
            "result": "if DeltaR=3 q_trace then b_P=q_trace=2/27",
            "status": "conditional_bridge_only",
            "missing_for_claim": "eta lock, trace current, and endpoint identification are all parent-action obligations",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_step": "TL862_5_local_nohair_requirement",
            "object": "boundary endpoint current",
            "candidate_equation": "P_loc J_trace^mu = 0 outside FLRW/monopole support",
            "result": "needed so the same boundary charge does not become local PPN/WEP/clock hair",
            "status": "open_nohair_condition",
            "missing_for_claim": "prove local projection silence or retain a sourced residual vector",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def endpoint_candidate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "candidate_id": "EC862_0_Ward_stationarity",
            "endpoint_object": "Q_early,Q_today",
            "candidate_equation": "delta S_boundary/dQ_early = 0 and delta S_boundary/dQ_today = 0",
            "test": "Can stationary endpoints differ by exactly 3 q_trace Q_*?",
            "outcome": "not_derived",
            "blocker": "no parent boundary potential/current action fixes both endpoint values",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "EC862_1_topological_jump",
            "endpoint_object": "DeltaQ",
            "candidate_equation": "DeltaQ = integral_boundary d star J_trace = 3 q_trace Q_*",
            "test": "Can the endpoint difference be a relative-chain/topological jump?",
            "outcome": "promising_form_not_theorem",
            "blocker": "existing 109 result says form-factor multiplication is bookkeeping until action-owned",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "EC862_2_normalization_unit",
            "endpoint_object": "Q_*",
            "candidate_equation": "Q_* = parent-normalized trace Ward charge unit",
            "test": "Can Q_* be fixed without SN/BAO calibration?",
            "outcome": "missing",
            "blocker": "boundary_charge_unit_defined is still failed in the earlier theorem attempt",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "EC862_3_no_target_inversion",
            "endpoint_object": "DeltaR",
            "candidate_equation": "DeltaR=2/9 follows before b_P fit or cosmology scoring",
            "test": "Does the route avoid reading the number back from the empirical optimum?",
            "outcome": "passes_only_if_TL862_1_to_TL862_3_are_proved",
            "blocker": "current route still requires the trace-lift identification as an extra premise",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "EC862_4_endpoint_local_silence",
            "endpoint_object": "P_loc DeltaQ",
            "candidate_equation": "P_loc(Q_early - Q_today)=0 for local non-cosmological experiments",
            "test": "Can the cosmological endpoint avoid WEP/clock/PPN hair?",
            "outcome": "open",
            "blocker": "needs boundary no-hair theorem or retained local residual budget",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def coframe_closure_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "closure_id": "CC862_0_variation_identity",
            "pullback_term": "Pi_I^matter = (delta S_matter/d ehat^a_mu)(partial ehat^a_mu/partial Z_I)",
            "closure_condition": "term vanishes or is included in a conserved selector equation",
            "status": "obstruction_reconfirmed",
            "reason": "fixed-ehat variation is insufficient when ehat depends on selector/projector fields",
            "local_GR_impact": "unowned term can source WEP, clocks, PPN, and fifth-force rows",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "closure_id": "CC862_1_strict_identity_coframe",
            "pullback_term": "partial ehat/partial Z_I",
            "closure_condition": "partial ehat/partial Z_I = 0 in the local exterior",
            "status": "cleanest_route_but_not_parent_derived",
            "reason": "would make Pi_I^matter zero for arbitrary local matter",
            "local_GR_impact": "supports local GR if paired with N5 and source-normalization closure",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "closure_id": "CC862_2_pure_gauge_pullback",
            "pullback_term": "delta ehat = Lie_xi ehat + local Lorentz rotation",
            "closure_condition": "all representative selector motion is gauge",
            "status": "insufficient_as_general_zero",
            "reason": "works only for gauge directions; physical endpoint/projector directions still need proof",
            "local_GR_impact": "cannot by itself clear WEP/PPN residuals",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "closure_id": "CC862_3_universal_absorbed_constant",
            "pullback_term": "common-mode conformal/coframe scaling",
            "closure_condition": "only a universal source-normalized constant survives",
            "status": "narrow_fallback",
            "reason": "gradients, anisotropy, species dependence, or time dependence still make observables",
            "local_GR_impact": "at best a measured-G renormalization; not a full local-GR proof",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "closure_id": "CC862_4_Ward_owned_counterstress",
            "pullback_term": "E_selector,I + Pi_I^matter = 0",
            "closure_condition": "counterstress is explicit, conserved, and no-hair/bounded",
            "status": "honest_modified_gravity_route",
            "reason": "owning the term is allowed, but it is not the same as proving it locally zero",
            "local_GR_impact": "requires retained residual runner unless counterstress has zero local projection",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "closure_id": "CC862_5_boundary_endpoint_silence",
            "pullback_term": "partial ehat/partial Q_endpoint",
            "closure_condition": "boundary endpoints couple only to FLRW trace/monopole charge",
            "status": "open_hard",
            "reason": "without this, the cosmological memory charge leaks into local clock/WEP/PPN tests",
            "local_GR_impact": "blocks q_loc=0 and local GR promotion",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def local_gr_impact_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "impact_id": "LG862_0_amplitude_if_closed",
            "branch": "cosmological parent memory",
            "conditional_result": "DeltaR=3 q_trace=2/9 and b_P=2/27",
            "required_stack": "exact readout, trace current, endpoint stationarity, eta=1, a_F=1",
            "current_status": "conditional_not_claimed",
            "next_action": "derive the Ward trace-lift current equation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "impact_id": "LG862_1_N5_if_coframe_closes",
            "branch": "local projector stress",
            "conditional_result": "exact-readout projector can avoid bulk F_P/T_projector",
            "required_stack": "metric-independent parent selector, identity coframe, no boundary hair",
            "current_status": "blocked_by_coframe_and_nohair",
            "next_action": "prove partial ehat/partial Z_I=0 or retain counterstress",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "impact_id": "LG862_2_qloc_zero_if_all_silent",
            "branch": "local GR/Newton limit",
            "conditional_result": "q_loc^nu=0 only if local projector, coframe, and endpoint projections vanish",
            "required_stack": "P_loc J_trace=0, Pi_I^matter=0, F_P_bulk=0, source normalization",
            "current_status": "not_derived",
            "next_action": "build zero theorem or residual vector",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "impact_id": "LG862_3_failure_branch",
            "branch": "retained residual modified-gravity route",
            "conditional_result": "if any local projection survives, score it as WEP/clock/PPN/orbital residual",
            "required_stack": "source coefficients, ranges, units, and comparison baselines",
            "current_status": "fallback_ready_not_run",
            "next_action": "only use after zero theorem fails or remains unsigned",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_choice_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC862_0_selected",
            "route": "Ward_trace_lift_current_and_coframe_pullback_zero_theorem",
            "status": "selected",
            "reason": "862 turned DeltaR=3q_trace into a sharp current/endpoint theorem and showed coframe zero is the shared local-GR blocker",
            "include": "derive J_trace^mu, endpoint stationarity, Q_* normalization, P_loc silence, partial ehat/partial Z_I zero",
            "exclude": "cosmology refit, fitted endpoint values, dropped projector stress, public claim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RC862_1_deferred",
            "route": "retained_residual_bound_runner",
            "status": "deferred",
            "reason": "bounds are needed only if the derivation route fails or leaves a nonzero projector/coframe/endpoint residual",
            "include": "PPN, WEP, clock, orbital coefficient rows",
            "exclude": "using bounds to pretend the exact GR limit is derived",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG862_0_no_trace_lift_claim",
            "claim": "DeltaR=3 q_trace is derived",
            "status": "forbidden",
            "reason": "J_trace^mu and endpoint identification are not parent-derived",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG862_1_no_2over27_prediction",
            "claim": "b_P=2/27 is a prediction",
            "status": "forbidden",
            "reason": "the amplitude follows only conditionally from unsigned trace-lift and endpoint equations",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG862_2_no_coframe_zero_claim",
            "claim": "Pi_I^matter is zero",
            "status": "forbidden",
            "reason": "identity coframe, pure gauge, constant, or counterstress routes remain unproved",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG862_3_no_local_GR_claim",
            "claim": "local GR/Newton follows",
            "status": "forbidden",
            "reason": "q_loc zero still needs N5, coframe, endpoint no-hair, and source normalization closure",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG862_4_allowed_private_result",
            "claim": "private theorem contract is sharper",
            "status": "allowed_private_nonclaim",
            "reason": "862 identifies the exact current equation and coframe zero theorem needed next",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D862_0",
            "finding": "trace_lift_bridge_constructed_but_not_proved",
            "reason": "DeltaR=3q_trace is algebraically clean once J_trace and endpoint identification are assumed, but those assumptions are the theorem target",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D862_1",
            "finding": "coframe_pullback_zero_is_shared_local_GR_gate",
            "reason": "Pi_I^matter remains active unless identity coframe, gauge, absorbed constant, or Ward-owned counterstress is parent-derived",
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
            "objective": "derive the Ward trace current and the local coframe-zero/no-hair theorem, or demote the route to retained residuals",
            "include": "J_trace^mu from parent Ward identity, endpoint Euler equations, Q_* unit, P_loc endpoint silence, partial ehat/partial Z_I zero theorem",
            "exclude": "new cosmology scoring, public claim, formalization-workbench edits, target-fitting DeltaR",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "converted DeltaR=3q_trace into an exact theorem contract and rechecked the coframe pullback as the shared local-GR blocker",
            "best_partial_result": "if J_trace is the FLRW three-direction lift of q_trace and endpoints identify with its charge, then DeltaR=2/9 and b_P=2/27",
            "hard_blockers": "parent Ward trace current, endpoint stationarity, Q_* normalization, coframe pullback zero, boundary/local no-hair",
            "what_is_not_claimed": "DeltaR=3q_trace, b_P=2/27 prediction, Pi_I^matter zero, q_loc zero, local GR/Newton",
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
    trace_rows: list[dict[str, object]],
    endpoint_rows: list[dict[str, object]],
    coframe_rows: list[dict[str, object]],
    local_rows: list[dict[str, object]],
    routes: list[dict[str, object]],
    guards: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
) -> list[dict[str, object]]:
    prior_clean, prior_detail = validation_file_clean(PRIOR_VALIDATION_PATH)
    formalization_count = formalization_workbench_modified_count()
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    trace_contract_ok = any(row["theorem_step"] == "TL862_3_endpoint_identification" and row["status"] == "central_unsigned_axiom" for row in trace_rows)
    conditional_algebra_ok = any(row["theorem_step"] == "TL862_4_amplitude_readout" and "b_P=q_trace=2/27" in row["result"] for row in trace_rows)
    endpoint_blocks_ok = any(row["candidate_id"] == "EC862_2_normalization_unit" and row["outcome"] == "missing" for row in endpoint_rows)
    coframe_blocks_ok = any(row["closure_id"] == "CC862_5_boundary_endpoint_silence" and row["status"] == "open_hard" for row in coframe_rows)
    local_claim_blocked = all(row["current_status"] != "derived" for row in local_rows)
    route_selected = any(row["route_id"] == "RC862_0_selected" for row in routes)
    no_claim = not any(row["claim_allowed"] == "true" for row in decisions)
    nonclaim_ok = all_valid_for_claim_false([source_rows, trace_rows, endpoint_rows, coframe_rows, local_rows, routes, guards, decisions, next_targets, nonclaim])
    next_selected = bool(next_targets) and next_targets[0]["next_target"] == NEXT_TARGET
    return [
        {"check_id": "V862_0_sources_exist_and_needles", "result": "pass" if source_ok else "fail", "detail": "all source paths exist and needles are present" if source_ok else "source register has missing path or needle"},
        {"check_id": "V862_1_prior_861_clean", "result": "pass" if prior_clean else "fail", "detail": prior_detail},
        {"check_id": "V862_2_trace_lift_contract_ready", "result": "pass" if trace_contract_ok else "fail", "detail": "DeltaR endpoint identification is recorded as the central unsigned axiom"},
        {"check_id": "V862_3_conditional_algebra_ready", "result": "pass" if conditional_algebra_ok else "fail", "detail": "if trace lift closes, b_P=q_trace=2/27 is recorded"},
        {"check_id": "V862_4_endpoint_candidates_block_claim", "result": "pass" if endpoint_blocks_ok else "fail", "detail": "Q_* and endpoint equations remain missing"},
        {"check_id": "V862_5_coframe_pullback_blocks_claim", "result": "pass" if coframe_blocks_ok else "fail", "detail": "boundary endpoint/coframe silence remains open"},
        {"check_id": "V862_6_local_GR_not_promoted", "result": "pass" if local_claim_blocked else "fail", "detail": "local GR impact rows remain conditional or blocked"},
        {"check_id": "V862_7_route_selected", "result": "pass" if route_selected else "fail", "detail": "Ward trace current plus coframe zero theorem selected"},
        {"check_id": "V862_8_claim_allowed_false", "result": "pass" if no_claim else "fail", "detail": "decision rows keep claim_allowed=false"},
        {"check_id": "V862_9_all_rows_nonclaim", "result": "pass" if nonclaim_ok else "fail", "detail": "all generated rows valid_for_claim=false"},
        {"check_id": "V862_10_next_target_selected", "result": "pass" if next_selected else "fail", "detail": NEXT_TARGET},
        {"check_id": "V862_11_formalization_workbench_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={formalization_count}"},
        {"check_id": "V862_12_validation_rows_ready", "result": "pass", "detail": "validation table constructed"},
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
    trace_rows: list[dict[str, object]],
    endpoint_rows: list[dict[str, object]],
    coframe_rows: list[dict[str, object]],
    local_rows: list[dict[str, object]],
    routes: list[dict[str, object]],
    guards: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 862 - Y5 R10 Trace-Lift Endpoint Equation And Coframe Pullback Closure",
        "",
        "Current result: **the trace-lift route is sharper, but still not closed**. The clean conditional theorem is: if `q_trace=2/27` is an exact parent readout, if the FLRW memory endpoint is the three-direction Ward trace lift of that readout, and if `eta=a_F=1`, then `DeltaR=3 q_trace=2/9` and `b_P=2/27`. The missing piece is not algebra now; it is the parent-owned current/endpoint equation plus the local coframe/no-hair zero theorem.",
        "",
        "## Non-Claim Summary",
        "",
        csv_table(nonclaim, ["status", "claim_ceiling", "what_changed", "best_partial_result", "hard_blockers", "what_is_not_claimed", "next_target", "valid_for_claim"]),
        "",
        "## Trace-Lift Theorem Attempt",
        "",
        csv_table(trace_rows, ["theorem_step", "object", "candidate_equation", "result", "status", "missing_for_claim", "valid_for_claim"]),
        "",
        "## Endpoint Equation Candidates",
        "",
        csv_table(endpoint_rows, ["candidate_id", "endpoint_object", "candidate_equation", "test", "outcome", "blocker", "valid_for_claim"]),
        "",
        "## Coframe Pullback Closure Audit",
        "",
        csv_table(coframe_rows, ["closure_id", "pullback_term", "closure_condition", "status", "reason", "local_GR_impact", "valid_for_claim"]),
        "",
        "## Local GR Impact Ledger",
        "",
        csv_table(local_rows, ["impact_id", "branch", "conditional_result", "required_stack", "current_status", "next_action", "valid_for_claim"]),
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
    trace_rows = trace_lift_rows(generated_utc)
    endpoint_rows = endpoint_candidate_rows(generated_utc)
    coframe_rows = coframe_closure_rows(generated_utc)
    local_rows = local_gr_impact_rows(generated_utc)
    routes = route_choice_rows(generated_utc)
    guards = claim_guard_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    next_targets = next_target_rows(generated_utc)
    nonclaim = nonclaim_summary_rows(generated_utc)
    validation = validation_rows(
        source_rows,
        trace_rows,
        endpoint_rows,
        coframe_rows,
        local_rows,
        routes,
        guards,
        decisions,
        next_targets,
        nonclaim,
    )

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(TRACE_LIFT_PATH, trace_rows, ["theorem_step", "object", "candidate_equation", "result", "status", "missing_for_claim", "valid_for_claim", "generated_utc"])
    write_csv(ENDPOINT_CANDIDATES_PATH, endpoint_rows, ["candidate_id", "endpoint_object", "candidate_equation", "test", "outcome", "blocker", "valid_for_claim", "generated_utc"])
    write_csv(COFRAME_CLOSURE_PATH, coframe_rows, ["closure_id", "pullback_term", "closure_condition", "status", "reason", "local_GR_impact", "valid_for_claim", "generated_utc"])
    write_csv(LOCAL_GR_IMPACT_PATH, local_rows, ["impact_id", "branch", "conditional_result", "required_stack", "current_status", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_CHOICE_PATH, routes, ["route_id", "route", "status", "reason", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_GUARD_PATH, guards, ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, nonclaim, ["status", "claim_ceiling", "what_changed", "best_partial_result", "hard_blockers", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_document(source_rows, trace_rows, endpoint_rows, coframe_rows, local_rows, routes, guards, decisions, next_targets, nonclaim, validation)

    print(f"wrote={OUTPUT_DOC}")
    print(f"wrote={VALIDATION_PATH}")
    print(f"status={STATUS}")
    print("partial_bridge=if J_trace is parent-owned and endpoints identify with it, DeltaR=3*q_trace=2/9 and b_P=2/27")
    print(f"claim_ceiling={CLAIM_CEILING}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()

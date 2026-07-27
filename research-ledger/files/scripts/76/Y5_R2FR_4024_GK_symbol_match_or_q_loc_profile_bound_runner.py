from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "4024"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "4024-Y5-R2FR-GK-symbol-match-or-q-loc-profile-bound-runner.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_4024_SOURCE_REGISTER.csv",
    "symbol_match": SRC / "P8_Y5_R2FR_4024_GK_SYMBOL_MATCH_MATRIX.csv",
    "response_template": SRC / "P8_Y5_R2FR_4024_RESPONSE_FIELD_TEMPLATE_ROUTE.csv",
    "bound_runner": SRC / "P8_Y5_R2FR_4024_QLOC_PROFILE_BOUND_RUNNER_ROWS.csv",
    "dry_run": SRC / "P8_Y5_R2FR_4024_QLOC_BOUND_DRY_RUN_RESULTS.csv",
    "cases": SRC / "P8_Y5_R2FR_4024_EVALUATOR_CASES.csv",
    "results": SRC / "P8_Y5_R2FR_4024_EVALUATOR_RESULTS.csv",
    "decision": SRC / "P8_Y5_R2FR_4024_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_4024_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_4024_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_4024_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_4024_VALIDATION.csv",
}

NEXT_DOC = "4025-Y5-R2FR-response-field-owner-construction-or-DGK-bound-fill.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_4025_response_field_owner_construction_or_DGK_bound_fill.py"
COMPACT_SHELL_PROXY = 7.432631961576971e-06


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
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
        writer.writerows(rows)


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC4024_00_handoff", SRC / "P8_Y5_R2FR_4023_NEXT_TARGET.csv", "NEXT4023_0", "4023 handoff"),
        ("SRC4024_01_action", SRC / "P8_Y5_R2FR_4023_CANONICAL_SGK_ACTION_ATTEMPT.csv", "SGK4023_4_match_condition", "canonical SGK match condition"),
        ("SRC4024_02_match", SRC / "P8_Y5_R2FR_4023_GK_MATCH_AND_HELMHOLTZ_GATES.csv", "MATCH4023_5_2PN_match", "4023 match gate"),
        ("SRC4024_03_bound", SRC / "P8_Y5_R2FR_4023_QLOC_BOUND_INTERFACE_ROWS.csv", "BND4023_0_DGK_norm", "4023 bound interface"),
        ("SRC4024_04_sym_audit", SRC / "P8_Y5_PARENT_QLOC_1526_SYMBOL_MATCH_AUDIT.csv", "SYM1526_5_verdict", "older symbol match audit"),
        ("SRC4024_05_response_contract", SRC / "P8_GK_METRIC_RESPONSE_CONTRACT.csv", "MR514_1_Khat_metric_response", "metric response contract"),
        ("SRC4024_06_response_audit", SRC / "P8_GK_METRIC_RESPONSE_MATCH_AUDIT.csv", "MA515_1_Khat_metric_response", "metric response audit"),
        ("SRC4024_07_pass_fail", SRC / "P8_GK_METRIC_RESPONSE_PASS_FAIL.csv", "PF515_2_Khat_response_found", "response pass/fail"),
        ("SRC4024_08_residual_branch", SRC / "P8_GK_RESIDUAL_BOUND_BRANCH.csv", "GB514_1_Khat_not_response", "residual bound branch"),
        ("SRC4024_09_bound_spec", SRC / "P8_QLOC_BOUND_RUNNER_SPEC.csv", "QB516_0_compact_shell_budget", "q_loc bound spec"),
        ("SRC4024_10_trigger", SRC / "P8_QLOC_BOUND_TRIGGER_LEDGER.csv", "BT517_0_owner_match_fails", "q_loc bound trigger"),
        ("SRC4024_11_evidence", SRC / "P8_GK_METRIC_RESPONSE_SOURCE_EVIDENCE.csv", "E515_4_source_current_audit", "response-field template evidence"),
        ("SRC4024_12_nohair", SRC / "P8_Y5_PARENT_QLOC_1534_LOCAL_LOCKING_NOHAIR_THEOREM.csv", "NH1534_3_exact_nohair", "nohair theorem"),
        ("SRC4024_13_leakage", SRC / "P8_Y5_PARENT_QLOC_1534_QUADRATIC_LEAKAGE_BOUND_CONTRACT.csv", "LEAK1534_6_verdict", "leakage bound"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in source_specs():
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "role": role,
                "needle": needle,
                "exists": path.exists(),
                "needle_found": needle in text,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def symbol_match_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "match_id": "SM4024_0_Gamma_owner",
            "object": "Gamma_eff",
            "required": "covariant scalar action density Gamma_eff(g,Y,nablaY,D,topological data) with units and fixed branch ownership",
            "current_evidence": "Gamma_eff exists as route/readout symbol, but old audit found no explicit scalar-density owner",
            "verdict": "fail_current_claim",
            "residual_if_fail": "D_GK scalar/source mismatch",
            "repair_or_bound": "define parent scalar density or bound Gamma contribution directly",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "match_id": "SM4024_1_Khat_response",
            "object": "Khat^{mu nu}",
            "required": "Khat equals metric response of sqrt|g| Gamma_eff including derivative and boundary terms under fixed sign",
            "current_evidence": "old audit found Khat in q_loc identities but no live derivation as delta[sqrt|g|Gamma_eff]/delta g",
            "verdict": "fail_current_claim",
            "residual_if_fail": "D_GK tensor mismatch",
            "repair_or_bound": "compute metric response from proposed Gamma_eff and compare to Khat tensor structure",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "match_id": "SM4024_2_response_template",
            "object": "conjugate parent response field",
            "required": "Gamma_eff and Khat are conjugate scalar/tensor projections of one parent response/displacement field",
            "current_evidence": "source-current Noether audit gives promising template, not a proof",
            "verdict": "open_promising_template",
            "residual_if_fail": "response-field construction unavailable",
            "repair_or_bound": "construct response field owner in 4025 or retain D_GK bound",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "match_id": "SM4024_3_Helmholtz",
            "object": "sqrt|g|T_GK inverse-variational symmetry",
            "required": "Helmholtz defect H_GK=0 for the actual Gamma/Khat tensor",
            "current_evidence": "canonical S_can has H=0, actual Gamma/Khat not checked",
            "verdict": "unverified",
            "residual_if_fail": "nonvariational part of D_GK",
            "repair_or_bound": "compute symbolic Helmholtz defect or bound nonvariational response",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "match_id": "SM4024_4_fixed_point",
            "object": "local fixed point",
            "required": "T_GK(Y0)=0 and partial_A T_GK(Y0)=0, with constant background subtracted",
            "current_evidence": "canonical action has double-zero; actual Gamma/Khat fixed-point expansion not found",
            "verdict": "unverified",
            "residual_if_fail": "linear F_1 leakage",
            "repair_or_bound": "expand actual Gamma/Khat around local fixed point or carry F_1 profile coefficient",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "match_id": "SM4024_5_boundary_projector",
            "object": "P_loc and boundary flux",
            "required": "P_loc parent-owned; boundary/symplectic flux zero or fixed topological subtraction",
            "current_evidence": "old audits keep boundary/projector gates open",
            "verdict": "open",
            "residual_if_fail": "boundary_flux_GK and projector residual",
            "repair_or_bound": "derive ownership/no-flux or use compact-shell proxy bound",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "match_id": "SM4024_6_current_verdict",
            "object": "D_GK through local 2PN",
            "required": "all SM4024_0..5 pass",
            "current_evidence": "SM4024_0 and SM4024_1 fail current claim; SM4024_2 is promising but unsigned",
            "verdict": "D_GK_not_zeroed_currently",
            "residual_if_fail": "q_loc profile/bound branch required",
            "repair_or_bound": "4025 response-field owner construction or D_GK bound fill",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def response_template_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "template_id": "RFT4024_0_parent_field",
            "piece": "response carrier",
            "candidate_form": "Introduce response field R_A[g,Y] with scalar projection Gamma_eff=Gamma(R_A,Y,g) and tensor response Khat^{mu nu}=(-2/sqrt|g|)delta int sqrt|g| Gamma_eff / delta g_{mu nu}",
            "what_it_would_close": "SM4024_0_Gamma_owner; SM4024_1_Khat_response",
            "current_status": "candidate_route_not_corpus_adopted",
            "next_test": "write explicit Gamma_eff density and compute metric response",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "template_id": "RFT4024_1_sign_units",
            "piece": "normalization",
            "candidate_form": "Fix sign convention so T_GK^{mu nu}=Gamma_eff g^{mu nu}-Khat^{mu nu}=T_can^{mu nu}+D_GK^{mu nu}; declare stress units relative to EH source normalization",
            "what_it_would_close": "units/readout and D_GK definition",
            "current_status": "required_before_score",
            "next_test": "map units to delta_beta_q_loc/R10 alpha(lambda)",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "template_id": "RFT4024_2_fixed_point",
            "piece": "double-zero response",
            "candidate_form": "Gamma_eff(Y0)=constant, nabla Gamma_eff(Y0)=0, Khat(Y0)=constant*g plus subtracted background, partial_A[T_GK]_{Y0}=0",
            "what_it_would_close": "F_1 local leakage",
            "current_status": "unverified_for_actual_symbols",
            "next_test": "Taylor-expand Gamma_eff and Khat around Y0",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "template_id": "RFT4024_3_fallback",
            "piece": "mismatch bound",
            "candidate_form": "If any response-field clause fails, keep D_GK and estimate |q_loc|<=||P_loc||(|nabla D_GK|+Euler+boundary)",
            "what_it_would_close": "testability despite failed symbol match",
            "current_status": "active_fallback",
            "next_test": "fill profile amplitudes A_DGK, A_Euler, A_boundary and projector coefficients",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def bound_runner_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "QRUN4024_0_profile_master",
            "quantity": "Q_loc_envelope",
            "formula": "Q_loc <= C_Ploc*(A_DGK/L_DGK + A_Euler/L_Euler + A_boundary/L_boundary)",
            "required_inputs": "C_Ploc,A_DGK,L_DGK,A_Euler,L_Euler,A_boundary,L_boundary",
            "current_value": "NOT_NUMERIC",
            "dry_run_value": "symbolic_only",
            "observable_map": "delta_beta_q_loc; R10 alpha(lambda); source-exchange",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "runner_id": "QRUN4024_1_DGK_profile",
            "quantity": "A_DGK/L_DGK",
            "formula": "norm of nabla_mu[Gamma_eff g^{mu nu}-Khat^{mu nu}-T_can^{mu nu}]",
            "required_inputs": "symbol match residual amplitude A_DGK and length scale L_DGK",
            "current_value": "MISSING_SYMBOL_MATCH_PROFILE",
            "dry_run_value": "not_available",
            "observable_map": "PPN beta/gamma q_loc tail",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "runner_id": "QRUN4024_2_Euler_forcing",
            "quantity": "A_Euler/L_Euler",
            "formula": "sum_A |E_A||nablaY^A|",
            "required_inputs": "carrier Euler residual and field-gradient scale",
            "current_value": "MISSING_EULER_SOURCE_SILENCE_OR_PROFILE",
            "dry_run_value": "not_available",
            "observable_map": "fifth-force/source-exchange",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "runner_id": "QRUN4024_3_boundary_proxy",
            "quantity": "A_boundary_proxy",
            "formula": "compact-shell leakage proxy from prior q_loc bound spec",
            "required_inputs": "map proxy to stress/PPN units",
            "current_value": COMPACT_SHELL_PROXY,
            "dry_run_value": COMPACT_SHELL_PROXY,
            "observable_map": "alpha3; measured-GM drift; beta/gamma tail after normalization",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "runner_id": "QRUN4024_4_delta_beta_map",
            "quantity": "delta_beta_q_loc",
            "formula": "delta_beta_q_loc = C_beta_qloc * Q_loc_envelope",
            "required_inputs": "C_beta_qloc from weak-field PPN projector",
            "current_value": "MISSING_C_BETA_QLOC",
            "dry_run_value": "not_available",
            "observable_map": "PPN beta",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "runner_id": "QRUN4024_5_R10_map",
            "quantity": "alpha_q(lambda)",
            "formula": "alpha_q(lambda)=C_R10_qloc(lambda)*Q_loc_envelope",
            "required_inputs": "C_R10_qloc(lambda), lambda profile, source normalization",
            "current_value": "MISSING_R10_PROFILE_MAP",
            "dry_run_value": "not_available",
            "observable_map": "R10 fifth-force alpha(lambda)",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def dry_run_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "dry_run_id": "DRY4024_0_proxy_parse",
            "input": "compact-shell leakage proxy",
            "value": COMPACT_SHELL_PROXY,
            "units": "dimensionless proxy; not PPN units",
            "result": "parsed_positive_numeric",
            "claim_use": "forbidden_until_mapping_exists",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "dry_run_id": "DRY4024_1_score_readiness",
            "input": "C_beta_qloc and C_R10_qloc",
            "value": "MISSING",
            "units": "PPN/R10 projector coefficients",
            "result": "not_score_ready",
            "claim_use": "blocked",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "dry_run_id": "DRY4024_2_bound_branch_trigger",
            "input": "SM4024_0/1 fail current claim",
            "value": "true",
            "units": "logic",
            "result": "bound_branch_active",
            "claim_use": "nonclaim_only",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def case_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "case_id": "CASE4024_0_exact_match",
            "assumption": "Gamma owner and Khat metric response are constructed and D_GK=0 through 2PN",
            "expected": "return to q_loc zero theorem route",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4024_1_current_state",
            "assumption": "current audits fail Gamma owner and Khat response for claim",
            "expected": "D_GK not zeroed; bound branch active",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4024_2_template_route",
            "assumption": "response-field template is built in 4025",
            "expected": "symbol match can be retried with explicit Gamma density",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4024_3_profile_bound",
            "assumption": "D_GK remains nonzero",
            "expected": "fill QRUN4024 amplitudes and PPN/R10 projector maps",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def result_rows(cases: list[dict[str, Any]], timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case in cases:
        case_id = str(case["case_id"])
        if case_id == "CASE4024_0_exact_match":
            verdict = "QLOC_ZERO_ROUTE_REOPENS_IF_MATCH_PROVED"
            next_action = "verify projector/boundary and Euler gates after D_GK=0"
        elif case_id == "CASE4024_1_current_state":
            verdict = "CURRENT_SYMBOL_MATCH_FAILS_FOR_CLAIM"
            next_action = "4025 must either construct response-field owner or fill D_GK bound"
        elif case_id == "CASE4024_2_template_route":
            verdict = "RESPONSE_TEMPLATE_IS_BEST_DERIVATION_ROUTE"
            next_action = "write explicit Gamma_eff density and metric response"
        else:
            verdict = "PROFILE_BOUND_RUNNER_REQUIRED"
            next_action = "source A_DGK/L_DGK, Euler forcing, boundary mapping and PPN/R10 projectors"
        rows.append(
            {
                "case_id": case_id,
                "verdict": verdict,
                "claim_result": "NO_PUBLIC_QLOC_OR_LOCAL_GR_CLAIM_FROM_4024",
                "next_action": next_action,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4024_0_symbol_match",
            "decision": "current Gamma/Khat symbol match fails for claim",
            "rationale": "Gamma scalar-density owner and Khat metric-response derivation are not live in the corpus",
            "effect": "D_GK cannot be set to zero yet",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4024_1_keep_template",
            "decision": "response-field template remains the best derivation route",
            "rationale": "old Noether/source-current evidence suggests a conjugate response field could own both Gamma and Khat",
            "effect": "4025 tries construction before fully demoting to numeric bounds",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4024_2_start_bound_runner",
            "decision": "q_loc bound runner interface started",
            "rationale": "if response-field construction fails, D_GK/Euler/boundary rows are ready to receive source-backed amplitudes",
            "effect": "q_loc becomes testable rather than rhetorical",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4024_3_next",
            "decision": f"move to {NEXT_DOC}",
            "rationale": "next step must either build the response-field owner or fill the D_GK profile inputs",
            "effect": "derive-first path stays alive with a bound fallback",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "CLAIM4024_0_q_loc_zero",
            "claim": "q_loc is theorem-zero in current corpus",
            "allowed": False,
            "reason": "Gamma owner and Khat metric-response match fail current claim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "claim_id": "CLAIM4024_1_DGK_zero",
            "claim": "D_GK=0 through local 2PN",
            "allowed": False,
            "reason": "response-field symbol match is only a template, not adopted/proved",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "claim_id": "CLAIM4024_2_bound_pass",
            "claim": "q_loc bound passes PPN/R10",
            "allowed": False,
            "reason": "bound runner lacks A_DGK/L_DGK, C_beta_qloc and C_R10_qloc",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "claim_id": "CLAIM4024_3_local_GR",
            "claim": "local-GR branch passes",
            "allowed": False,
            "reason": "q_loc, R11/source-normalization and boundary/projector gates remain nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT4024_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "objective": "construct an explicit response-field owner that makes Gamma_eff a scalar action density and Khat its metric response; if construction fails, fill D_GK profile amplitude and PPN/R10 map inputs",
            "success_condition": "either SM4024_0/1 become theorem-zero through a live owner, or QRUN4024_1/4/5 become source-ready bound rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "private_nonclaim_checkpoint",
            "summary": "Gamma/Khat current symbol match fails for claim; response-field route and q_loc bound runner prepared",
            "current_best_route": "try response-field owner construction, then D_GK profile bound fill",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(timestamp: str, sources: list[dict[str, Any]], results: list[dict[str, Any]]) -> None:
    source_hits = sum(1 for row in sources if row["exists"] and row["needle_found"])
    source_total = len(sources)
    current = next(row for row in results if row["case_id"] == "CASE4024_1_current_state")
    DOC_PATH.write_text(
        f"""# 4024 - GK Symbol Match Or q_loc Profile Bound Runner

- Timestamp: `{timestamp}`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.

## Result

The actual current-symbol match does **not** pass for claim.

The failure is specific, not vague:

- `Gamma_eff` is present as a framework symbol, but not yet as a parent-owned covariant scalar action density with units.
- `Khat` is present in q_loc identities, but not yet derived as the metric response of `sqrt|g| Gamma_eff`.
- A conjugate response-field template exists and is promising, but it is not adopted/proved.

Therefore `D_GK=Gamma_eff g-Khat-T_can` cannot be set to zero yet.

## Bound Runner Started

The active nonclaim bound interface is:

`Q_loc <= C_Ploc*(A_DGK/L_DGK + A_Euler/L_Euler + A_boundary/L_boundary)`.

Observable maps:

- `delta_beta_q_loc = C_beta_qloc * Q_loc`;
- `alpha_q(lambda)=C_R10_qloc(lambda)*Q_loc`;
- source-exchange and boundary terms enter through the same envelope.

The compact-shell proxy `{COMPACT_SHELL_PROXY}` parses as a positive number, but it is **not** a PPN score until the unit/projector maps are supplied.

## Current Verdict

- Current evaluator result: `{current["verdict"]}`.
- Claim result: `{current["claim_result"]}`.
- Source needles found: `{source_hits}/{source_total}`.

## Next Target

- `{NEXT_DOC}`
- `{NEXT_SCRIPT}`
""",
        encoding="utf-8",
    )


def append_spine(timestamp: str) -> None:
    marker = "## 4024 - Gamma/Khat Symbol Match And q_loc Bound Runner"
    block = f"""

{marker}

- Timestamp: `{timestamp}`
- Result: current `Gamma_eff/Khat -> T_can` symbol match fails for claim: `Gamma_eff` owner and `Khat` metric response are not live in the corpus.
- Kept derivation route: conjugate response-field template could own both scalar density and tensor response if constructed.
- Bound route started: `Q_loc <= C_Ploc*(A_DGK/L_DGK + A_Euler/L_Euler + A_boundary/L_boundary)`.
- Dry-run proxy: compact-shell leakage `{COMPACT_SHELL_PROXY}` is parseable but not a PPN/R10 score.
- No claim: `D_GK=0`, `q_loc=0`, and local GR remain blocked.
- Next: `{NEXT_DOC}`.
"""
    current = read_text(SPINE_PATH)
    if marker not in current:
        SPINE_PATH.write_text(current.rstrip() + block + "\n", encoding="utf-8")


def marker_in_spine() -> bool:
    return "## 4024 - Gamma/Khat Symbol Match And q_loc Bound Runner" in read_text(SPINE_PATH)


def build_validation_rows(
    timestamp: str,
    sources: list[dict[str, Any]],
    symbol_match: list[dict[str, Any]],
    response_template: list[dict[str, Any]],
    bound_runner: list[dict[str, Any]],
    dry_run: list[dict[str, Any]],
    results: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    compile_ok: bool,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail, "timestamp_utc": timestamp})

    add("VAL4024_00_sources_exist", all(bool(row["exists"]) for row in sources), "every cited source path exists")
    add("VAL4024_01_needles_found", all(bool(row["needle_found"]) for row in sources), "every cited source needle found")
    for idx, match_id in enumerate(
        ["SM4024_0_Gamma_owner", "SM4024_1_Khat_response", "SM4024_2_response_template", "SM4024_3_Helmholtz", "SM4024_4_fixed_point", "SM4024_5_boundary_projector", "SM4024_6_current_verdict"],
        start=2,
    ):
        add(f"VAL4024_{idx:02d}_symbol", any(row["match_id"] == match_id for row in symbol_match), f"{match_id} present")
    add("VAL4024_09_gamma_fail", any(row["match_id"] == "SM4024_0_Gamma_owner" and row["verdict"] == "fail_current_claim" for row in symbol_match), "Gamma owner fail recorded")
    add("VAL4024_10_khat_fail", any(row["match_id"] == "SM4024_1_Khat_response" and row["verdict"] == "fail_current_claim" for row in symbol_match), "Khat response fail recorded")
    add("VAL4024_11_template_open", any(row["match_id"] == "SM4024_2_response_template" and row["verdict"] == "open_promising_template" for row in symbol_match), "response template preserved")
    for idx, template_id in enumerate(["RFT4024_0_parent_field", "RFT4024_1_sign_units", "RFT4024_2_fixed_point", "RFT4024_3_fallback"], start=12):
        add(f"VAL4024_{idx:02d}_template", any(row["template_id"] == template_id for row in response_template), f"{template_id} present")
    for idx, runner_id in enumerate(["QRUN4024_0_profile_master", "QRUN4024_1_DGK_profile", "QRUN4024_2_Euler_forcing", "QRUN4024_3_boundary_proxy", "QRUN4024_4_delta_beta_map", "QRUN4024_5_R10_map"], start=16):
        add(f"VAL4024_{idx:02d}_runner", any(row["runner_id"] == runner_id for row in bound_runner), f"{runner_id} present")
    add("VAL4024_22_proxy_positive", any(row["dry_run_id"] == "DRY4024_0_proxy_parse" and float(row["value"]) > 0 for row in dry_run), "compact-shell proxy parsed positive")
    result_lookup = {row["case_id"]: row for row in results}
    add("VAL4024_23_current_case", result_lookup["CASE4024_1_current_state"]["verdict"] == "CURRENT_SYMBOL_MATCH_FAILS_FOR_CLAIM", "current case fails match for claim")
    add("VAL4024_24_template_case", result_lookup["CASE4024_2_template_route"]["verdict"] == "RESPONSE_TEMPLATE_IS_BEST_DERIVATION_ROUTE", "template case preserved")
    add("VAL4024_25_bound_case", result_lookup["CASE4024_3_profile_bound"]["verdict"] == "PROFILE_BOUND_RUNNER_REQUIRED", "profile bound case defined")
    add("VAL4024_26_decision_bound", any(row["decision_id"] == "DEC4024_2_start_bound_runner" for row in decisions), "bound runner decision recorded")
    add("VAL4024_27_claims_false", all(str(row.get("allowed", "")).lower() == "false" for row in claims), "all claim gates false")
    add("VAL4024_28_bound_not_ready", all(str(row.get("score_ready", "")).lower() == "false" for row in bound_runner), "bound runner rows not score-ready")
    add("VAL4024_29_next_target", OUTPUTS["next"].exists() and NEXT_SCRIPT in read_text(OUTPUTS["next"]), "next target written")
    output_tables = [
        sources,
        symbol_match,
        response_template,
        bound_runner,
        dry_run,
        results,
        decisions,
        claims,
        read_csv(OUTPUTS["next"]),
        read_csv(OUTPUTS["status"]),
    ]
    add("VAL4024_30_all_nonclaim", all(str(row.get("valid_for_claim", "")).lower() == "false" for table in output_tables for row in table), "all emitted rows remain nonclaim")
    add("VAL4024_31_doc_exists", DOC_PATH.exists() and "Bound Runner Started" in read_text(DOC_PATH), "document written with bound-runner section")
    add("VAL4024_32_spine_updated", SPINE_PATH.exists() and marker_in_spine(), "spine updated")
    add("VAL4024_33_no_fwb_outputs", not any(str(path).startswith(str(FWB)) for path in OUTPUTS.values()), "no outputs target formalization-workbench")
    add("VAL4024_34_compile", compile_ok, "script compiles")
    add("VAL4024_35_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "script __pycache__ removed")
    add("VAL4024_36_no_nan", not any("nan" in str(row).lower() or "inf" in str(row).lower() for row in results), "no nan/inf evaluator outputs")
    add("VAL4024_37_private_scope", DOC_PATH.exists() and "private_nonclaim_checkpoint" in read_text(DOC_PATH), "private scope recorded")
    add("VAL4024_38_overclaim_block", any(row["claim_id"] == "CLAIM4024_0_q_loc_zero" and str(row["allowed"]).lower() == "false" for row in claims), "q_loc zero overclaim blocked")
    return checks


def main() -> None:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    symbol_match = symbol_match_rows(timestamp)
    response_template = response_template_rows(timestamp)
    bound_runner = bound_runner_rows(timestamp)
    dry_run = dry_run_rows(timestamp)
    cases = case_rows(timestamp)
    results = result_rows(cases, timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["symbol_match"], symbol_match)
    write_csv(OUTPUTS["response_template"], response_template)
    write_csv(OUTPUTS["bound_runner"], bound_runner)
    write_csv(OUTPUTS["dry_run"], dry_run)
    write_csv(OUTPUTS["cases"], cases)
    write_csv(OUTPUTS["results"], results)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(timestamp, sources, results)
    append_spine(timestamp)

    compile_ok = True
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except py_compile.PyCompileError:
        compile_ok = False
    cache = SCRIPT_PATH.parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    validation = build_validation_rows(timestamp, sources, symbol_match, response_template, bound_runner, dry_run, results, decisions, claims, compile_ok)
    write_csv(OUTPUTS["validation"], validation)
    passed = sum(1 for row in validation if row["passed"])
    total = len(validation)
    print(f"4024 validation: {passed}/{total} passed")
    if passed != total:
        for row in validation:
            if not row["passed"]:
                print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()

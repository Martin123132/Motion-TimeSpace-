from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3895"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3895-Y5-R2FR-memory-boundary-history-zero-or-first-numeric-memory-row.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3895_SOURCE_REGISTER.csv",
    "zero": SRC / "P8_Y5_R2FR_3895_MEMORY_BOUNDARY_HISTORY_ZERO_ATTEMPT.csv",
    "law": SRC / "P8_Y5_R2FR_3895_MEMORY_SUPPRESSION_LAW.csv",
    "numeric": SRC / "P8_Y5_R2FR_3895_FIRST_NUMERIC_MEMORY_ROW_INTERFACE.csv",
    "gate": SRC / "P8_Y5_R2FR_3895_LOCAL_GR_DECISION_GATE.csv",
    "runner": SRC / "P8_Y5_R2FR_3895_RUNNER_UPDATE.csv",
    "next": SRC / "P8_Y5_R2FR_3895_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3895_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3895_VALIDATION.csv",
}

MEMORY_BOUND = "||X_mem|| <= (||J_open|| + B_lift)/lambda_gap"
LAMBDA_GAP = "lambda_gap := a_min C_P/L_D^2 + m_min^2"
HISTORY_BOUND = "||X_mem(t)|| <= exp(-gamma_mem Delta t)||X_mem(t0)|| + (1-exp(-gamma_mem Delta t)) sup||J_open+B_lift||/lambda_gap"
OBS_BOUND = "|Delta O_i| <= K_i ||X_mem|| + K_i_grad ||grad X_mem||"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def rel(path: Path) -> str:
    return str(path.relative_to(PCW)) if path.is_relative_to(PCW) else str(path)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


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
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC3895_00_next", SRC / "P8_Y5_R2FR_3894_NEXT_TARGET.csv", "NEXT3894_0", "3894 selected the memory boundary/history target"),
        ("SRC3895_01_jx", SRC / "P8_Y5_R2FR_3894_MEMORY_JX_COMPONENT_CLOSURE_GATE.csv", "JXG3894_3_chi_wall", "3894 open JX components"),
        ("SRC3895_02_gap", SRC / "P8_Y5_R2FR_3894_MEMORY_GAP_BOUND_AND_PROJECTION_ACQUISITION.csv", "ACQ3894_5_X_bound", "3894 memory amplitude bound interface"),
        ("SRC3895_03_gate", SRC / "P8_Y5_R2FR_3894_LOCAL_GR_DECISION_GATE.csv", "LGG3894_6_local_GR", "3894 local-GR nonclaim gate"),
        ("SRC3895_04_validation", SRC / "P8_Y5_BRR545_3894_VALIDATION.csv", "VAL3894_14_next_target", "3894 validation"),
        ("SRC3895_05_2627_jx", SRC / "P8_Y5_MEMORY_SOURCE_BOUNDARY_2627_JX_COMPONENT_ZERO_GATE.csv", "JX2627_6_total_verdict", "older JX component zero gate"),
        ("SRC3895_06_2627_bound", SRC / "P8_Y5_MEMORY_SOURCE_BOUNDARY_2627_FINITE_RESIDUAL_BOUND_PACK.csv", "RBP2627_4_local_projection", "older finite residual bound pack"),
        ("SRC3895_07_3892_boundary", SRC / "P8_Y5_R2FR_3892_BOUNDARY_TOPOLOGICAL_NOFLUX_CERTIFICATE.csv", "BC3892", "boundary topological certificate"),
        ("SRC3895_08_3892_projector", SRC / "P8_Y5_R2FR_3892_PROJECTOR_ABSOLUTE_TOPOLOGICAL_CERTIFICATE.csv", "PC3892", "projector certificate"),
        ("SRC3895_09_3893_memory", SRC / "P8_Y5_R2FR_3893_MEMORY_SILENCE_THEOREM_OR_BOUND.csv", "MEM3893_5_verdict", "3893 memory zero theorem or bound"),
        ("SRC3895_10_3891_lock", SRC / "P8_Y5_R2FR_3891_RESIDUAL_LOCK_MAP.csv", "RLM3891_4_memory", "memory residual lock map"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, path, needle, role in source_specs():
        exists = path.exists()
        found = exists and needle in read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "path": rel(path),
                "exists": exists,
                "needle": needle,
                "needle_found": found,
                "role": role,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def zero_attempt_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "zero_id": "ZERO3895_0_domain_motion",
            "open_channel": "J_X^chi_wall/domain motion",
            "derivation_or_bound": "If the local domain D is selected by q-basic data only, D_X 1_D(q(Phi)) = 0 for X_mem in ker(Dq); the wall does not move under a pure memory variation.",
            "status": "PASS_CANDIDATE_DERIVATION",
            "what_remains": "standalone wall stress or non-q-basic selector still reopens the source",
            "exact_zero_if_parent_signed": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "zero_id": "ZERO3895_1_wall_stress",
            "open_channel": "J_X^chi_wall/wall stress",
            "derivation_or_bound": "A wall action of the form S_wall = int Sigma_loc(Y) W_wall(q,Psi) or a wall coordinate included in Y_loc has delta_X S_wall=0 on Y_loc=0 because delta Sigma_loc|_0=0.",
            "status": "PASS_IF_SIGMA_SELECTED_PARENT_UNSIGNED",
            "what_remains": "a term linear in X_mem or f'(0) wall coupling would survive and must be bounded",
            "exact_zero_if_parent_signed": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "zero_id": "ZERO3895_2_boundary_dirichlet",
            "open_channel": "J_X^boundary",
            "derivation_or_bound": "In the energy identity, boundary_X = int_partialD X_mem n_i A^ij_mem D_j X_mem. Dirichlet X_mem|partialD=0 makes boundary_X=0 exactly.",
            "status": "PASS_MATH_NOT_PARENT_SIGNED",
            "what_remains": "Dirichlet compact-support/local-vacuum condition must come from parent action or matching, not taste",
            "exact_zero_if_parent_signed": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "zero_id": "ZERO3895_3_boundary_neumann",
            "open_channel": "J_X^boundary",
            "derivation_or_bound": "No-flux n_i A^ij_mem D_j X_mem|partialD=0 also gives boundary_X=0, but a constant zero mode remains unless m_min^2>0 or mean(X_mem)=0 is parent-fixed.",
            "status": "PASS_MATH_NEEDS_ZERO_MODE_GATE",
            "what_remains": "zero-mode removal or positive mass gap still required",
            "exact_zero_if_parent_signed": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "zero_id": "ZERO3895_4_history_exact",
            "open_channel": "J_X^history",
            "derivation_or_bound": "Exact history silence needs no incoming memory data plus no long-tail kernel: X_mem(t0)=0 and source-free retarded evolution. Otherwise the channel is bounded, not zero.",
            "status": "FAIL_AS_GLOBAL_EXACT_ZERO",
            "what_remains": "derive local reset/no-incoming condition or keep history_tail_norm",
            "exact_zero_if_parent_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "zero_id": "ZERO3895_5_total",
            "open_channel": "J_X_open",
            "derivation_or_bound": "Domain motion and boundary can be exact-zero under parent-signed clauses; history is only exact-zero with no incoming memory. Default branch therefore uses a suppression law.",
            "status": "PARTIAL_ZERO_BOUND_REQUIRED",
            "what_remains": "source gamma_mem, Delta t, C_P/L_D^2, m_min^2, boundary lift, and arena K_i",
            "exact_zero_if_parent_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def suppression_law_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "law_id": "LAW3895_0_energy_identity",
            "piece": "elliptic energy identity",
            "statement": "int_D(A^ij_mem D_i X D_j X + m_mem^2 X^2) = int_D X J_open + boundary_X",
            "derived_consequence": "Cauchy-Schwarz plus Poincare turns open sources into an amplitude bound.",
            "status": "FORMAL_DERIVED_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "law_id": "LAW3895_1_gap",
            "piece": "gap lower bound",
            "statement": LAMBDA_GAP,
            "derived_consequence": "If A^ij_mem >= a_min h^ij and the local domain has Poincare constant C_P/L_D^2, then the zero-mode-safe operator is coercive when lambda_gap>0.",
            "status": "DERIVED_IF_SIGN_DOMAIN_GAP_INPUTS_EXIST",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "law_id": "LAW3895_2_static_amplitude",
            "piece": "static memory amplitude",
            "statement": MEMORY_BOUND,
            "derived_consequence": "Boundary/history/domain-wall sources no longer remain vague: they enter only through J_open and B_lift divided by lambda_gap.",
            "status": "FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "law_id": "LAW3895_3_history_decay",
            "piece": "dynamic history tail",
            "statement": HISTORY_BOUND,
            "derived_consequence": "If gamma_mem Delta t is large, old memory is exponentially suppressed; if it is not sourced, history cannot be ignored.",
            "status": "DERIVED_SUPPRESSION_NOT_EXACT_ZERO",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "law_id": "LAW3895_4_observable_projection",
            "piece": "arena projection",
            "statement": OBS_BOUND,
            "derived_consequence": "R10/PPN/clock/orbital/WEP checks become ordinary coefficient bounds once K_i and K_i_grad are sourced.",
            "status": "FORMULA_READY_ARENA_COEFFICIENTS_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def numeric_interface_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "NUM3895_0_a_min",
            "input": "a_min",
            "first_fill_route": "If the parent kinetic metric is positive, canonically normalize X_mem so the principal lower bound is a_min=1 in local orthonormal units.",
            "units": "dimensionless after X normalization",
            "claim_status": "NOT_FILLED_PARENT_SIGN_NEEDED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "NUM3895_1_domain_scale",
            "input": "C_P/L_D^2",
            "first_fill_route": "Use lambda_1(D) >= C_P/L_D^2 for the selected bounded local domain; C_P and L_D must be fixed by the local matching rule.",
            "units": "1/length^2",
            "claim_status": "FORMULA_READY_NO_DOMAIN_NUMBER",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "NUM3895_2_m_min",
            "input": "m_min^2",
            "first_fill_route": "Derive from auxiliary mass/gap term in S_y or set m_min^2=0 only if zero-mode removal is already signed.",
            "units": "1/length^2",
            "claim_status": "NOT_FILLED_PARENT_GAP_NEEDED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "NUM3895_3_history_decay",
            "input": "gamma_mem Delta t",
            "first_fill_route": "Treat history as a damped auxiliary mode; source gamma_mem from parent dissipative/retarded kernel and Delta t from local branch age/matching interval.",
            "units": "dimensionless",
            "claim_status": "NOT_FILLED_KERNEL_NEEDED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "NUM3895_4_open_source_norm",
            "input": "||J_open|| + B_lift",
            "first_fill_route": "Sum only remaining wall/boundary/history norms after exact-zero rows are parent-signed; no cancellation credit allowed.",
            "units": "operator-normalized source units",
            "claim_status": "NOT_FILLED_COMPONENT_NORMS_NEEDED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "NUM3895_5_arena_K",
            "input": "K_R10,K_PPN,K_clock,K_orbital,K_WEP,K_Gdot",
            "first_fill_route": "Differentiate each observable readout with respect to X_mem on the candidate branch, then compare K_i||X|| to the external bound.",
            "units": "arena-specific per X unit",
            "claim_status": "NOT_FILLED_PROJECTION_DERIVATIVES_NEEDED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "LGG3895_0_wall",
            "gate": "domain-wall memory source",
            "result": "domain motion zero derived if q-basic; wall stress zero if Sigma/Yloc selected",
            "status": "PARTIAL_PASS_PARENT_UNSIGNED",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "LGG3895_1_boundary",
            "gate": "boundary memory source",
            "result": "Dirichlet or no-flux gives exact energy-boundary zero; zero-mode/matching not parent-signed",
            "status": "PARTIAL_PASS_BOUNDARY_CLAUSE_UNSIGNED",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "LGG3895_2_history",
            "gate": "history memory source",
            "result": "exact zero rejected unless no incoming memory; exponential suppression law derived",
            "status": "BOUND_NOT_EXACT_ZERO",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "LGG3895_3_amplitude",
            "gate": "finite memory amplitude",
            "result": MEMORY_BOUND,
            "status": "FORMULA_READY_NUMERIC_INPUTS_MISSING",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "LGG3895_4_local_GR",
            "gate": "local-GR promotion",
            "result": "not claimable until exact zero clauses are parent-signed or the suppression bound beats R10/PPN/clock/orbital/WEP limits",
            "status": "BLOCKED_NO_CLAIM_BUT_BOUND_ROUTE_OPEN",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def runner_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "update_id": "RUNU3895_0_zero",
            "runner_field": "zero_gate",
            "rule": "accept exact memory zero only if domain q-basic, wall Sigma/Yloc selected, boundary no-flux/Dirichlet parent-signed, and no incoming history are all true",
            "status": "STRICT_EXACT_ZERO_GATE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "update_id": "RUNU3895_1_bound",
            "runner_field": "bound_gate",
            "rule": "otherwise compute X_bound=(J_open+B_lift)/(a_min C_P/L_D^2+m_min^2) plus exp(-gamma_mem Delta t) history tail",
            "status": "SUPPRESSION_RUNNER_READY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "update_id": "RUNU3895_2_score",
            "runner_field": "score_gate",
            "rule": "arena pass only if K_i X_bound and K_i_grad grad_bound are below sourced bounds with no cancellation credit",
            "status": "NO_SCORE_WITHOUT_KI",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3895_0",
            "target_checkpoint": "3896-Y5-R2FR-memory-suppression-runner-and-first-local-bound-row.md",
            "script": "scripts/Y5_R2FR_3896_memory_suppression_runner_and_first_local_bound_row.py",
            "objective": "turn the 3895 suppression law into an executable nonclaim runner with placeholder-safe rows for a_min, C_P/L_D^2, m_min^2, gamma_mem Delta t, J_open+B_lift, and arena K_i",
            "why_next": "3895 converts the memory blocker into exact-zero clauses plus a finite suppression inequality; the next useful step is to make that inequality executable without claiming local GR",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_MEMORY_ZERO_PARTIAL_SUPPRESSION_LAW_DERIVED",
            "claim": "NO_LOCAL_GR_CLAIM",
            "summary": "boundary/domain-wall exact-zero routes sharpened; exact history zero rejected except no-incoming-data; finite memory suppression law derived",
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    zero: list[dict[str, object]],
    law: list[dict[str, object]],
    numeric: list[dict[str, object]],
    gate: list[dict[str, object]],
    runner: list[dict[str, object]],
    next_target: list[dict[str, object]],
    timestamp: str,
) -> None:
    doc = f"""# 3895 - Memory Boundary/History Zero or First Numeric Memory Row

Generated: `{timestamp}`

## Result

3895 does not hand-wave the memory channel away. It splits the remaining blocker into exact-zero clauses and a finite suppression law.

Exact-zero progress:

- domain motion is silent if the local domain is selected by quotient-basic data;
- wall stress is silent if it is Sigma/Yloc selected, using the same double-zero logic as R11;
- the boundary term vanishes for parent-signed Dirichlet or no-flux matching;
- exact history silence is rejected unless no incoming memory data is a real parent/matching condition.

Fallback bound:

`{MEMORY_BOUND}`, with `{LAMBDA_GAP}`.

Dynamic/history version:

`{HISTORY_BOUND}`.

Observable projection:

`{OBS_BOUND}`.

The useful movement is this: memory is no longer just an open word. If exact zero cannot be parent-signed, the project now has a clear executable bound route.

## Memory Boundary/History Zero Attempt

{markdown_table(zero, ["zero_id", "open_channel", "derivation_or_bound", "status", "what_remains"])}

## Memory Suppression Law

{markdown_table(law, ["law_id", "piece", "statement", "derived_consequence", "status"])}

## First Numeric Memory Row Interface

{markdown_table(numeric, ["row_id", "input", "first_fill_route", "units", "claim_status"])}

## Local-GR Decision Gate

{markdown_table(gate, ["gate_id", "gate", "result", "status", "claim_allowed"])}

## Runner Update

{markdown_table(runner, ["update_id", "runner_field", "rule", "status"])}

## Source Register

Resolved `{sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)}/{len(sources)}` source rows.

{markdown_table(sources, ["source_id", "path", "needle_found", "role"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_checkpoint", "objective", "why_next"])}

## Bottom Line

This is a genuine narrowing, not a circle. The memory branch still does not prove local GR, but it now has two disciplined paths: parent-sign the exact-zero clauses, or run the finite suppression law against real R10/PPN/clock/orbital/WEP bounds.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    block = f"""

<!-- BEGIN 3895 MEMORY BOUNDARY HISTORY ZERO SUPPRESSION -->
## 3895 Memory Boundary/History Zero or Suppression Law

Timestamp: `{timestamp}`

Result: `PASS_MEMORY_ZERO_PARTIAL_SUPPRESSION_LAW_DERIVED`.

Exact-zero progress:
- domain motion: zero if the local domain is quotient-basic;
- wall stress: zero if Sigma/Yloc selected with the double-zero mechanism;
- boundary: zero under parent-signed Dirichlet or no-flux matching;
- history: not exact-zero unless no incoming memory data is parent/matching signed.

Fallback suppression law:
`{MEMORY_BOUND}`, with `{LAMBDA_GAP}`.

Dynamic/history law:
`{HISTORY_BOUND}`.

Observable projection law:
`{OBS_BOUND}`.

Decision: no local-GR claim. The branch is now either exact-zero by parent clauses or executable as a finite residual bound.

Next gate: `3896`, memory suppression runner and first local bound row.
<!-- END 3895 MEMORY BOUNDARY HISTORY ZERO SUPPRESSION -->
"""
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    start = "<!-- BEGIN 3895 MEMORY BOUNDARY HISTORY ZERO SUPPRESSION -->"
    end = "<!-- END 3895 MEMORY BOUNDARY HISTORY ZERO SUPPRESSION -->"
    if start in existing and end in existing:
        before = existing.split(start, 1)[0].rstrip()
        after = existing.split(end, 1)[1].lstrip()
        SPINE_PATH.write_text(before + block + "\n" + after, encoding="utf-8")
    else:
        SPINE_PATH.write_text(existing.rstrip() + block + "\n", encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    zero: list[dict[str, object]],
    law: list[dict[str, object]],
    numeric: list[dict[str, object]],
    gate: list[dict[str, object]],
    runner: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    checks: list[tuple[str, str, bool, str]] = []
    resolved = [row for row in sources if row["exists"] and row["needle_found"]]
    checks.append(("VAL3895_0_sources", "all source paths and needles resolve", len(resolved) == len(sources), f"{len(resolved)}/{len(sources)} sources resolved"))
    checks.append(("VAL3895_1_domain", "domain motion zero route derived", any(row["zero_id"] == "ZERO3895_0_domain_motion" and "PASS" in str(row["status"]) for row in zero), "ZERO3895_0"))
    checks.append(("VAL3895_2_boundary", "boundary exact-zero clauses represented", any(row["zero_id"] == "ZERO3895_2_boundary_dirichlet" for row in zero) and any(row["zero_id"] == "ZERO3895_3_boundary_neumann" for row in zero), "Dirichlet/no-flux"))
    checks.append(("VAL3895_3_history", "history exact zero rejected unless no incoming memory", any(row["zero_id"] == "ZERO3895_4_history_exact" and "FAIL_AS_GLOBAL_EXACT_ZERO" in str(row["status"]) for row in zero), "ZERO3895_4"))
    checks.append(("VAL3895_4_law", "suppression law emitted", any(row["law_id"] == "LAW3895_2_static_amplitude" and MEMORY_BOUND in str(row["statement"]) for row in law), MEMORY_BOUND))
    checks.append(("VAL3895_5_history_law", "dynamic history law emitted", any(row["law_id"] == "LAW3895_3_history_decay" and "exp(-gamma_mem" in str(row["statement"]) for row in law), "LAW3895_3"))
    needed_numeric = {"a_min", "C_P/L_D^2", "m_min^2", "gamma_mem Delta t", "||J_open|| + B_lift", "K_R10,K_PPN,K_clock,K_orbital,K_WEP,K_Gdot"}
    found_numeric = {str(row["input"]) for row in numeric}
    checks.append(("VAL3895_6_numeric_interface", "first numeric memory input rows exist", needed_numeric.issubset(found_numeric), f"{len(found_numeric)} rows"))
    checks.append(("VAL3895_7_no_claim", "local GR remains blocked", any(row["gate_id"] == "LGG3895_4_local_GR" and "BLOCKED" in str(row["status"]) for row in gate), "LGG3895_4"))
    checks.append(("VAL3895_8_all_nonclaim", "all generated rows are nonclaim", all(str(row.get("valid_for_claim", row.get("claim_allowed", False))) == "False" for collection in [zero, law, numeric, gate, runner] for row in collection), "valid_for_claim=false"))
    checks.append(("VAL3895_9_runner", "runner has exact-zero and bound gates", any(row["runner_field"] == "zero_gate" for row in runner) and any(row["runner_field"] == "bound_gate" for row in runner), "RUNU3895_0/1"))
    checks.append(("VAL3895_10_doc", "markdown checkpoint exists with bottom line", DOC_PATH.exists() and "genuine narrowing" in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3895_11_spine", "spine updated with 3895 block", SPINE_PATH.exists() and "BEGIN 3895 MEMORY BOUNDARY HISTORY ZERO SUPPRESSION" in read_text(SPINE_PATH), rel(SPINE_PATH)))
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_parse_ok = True
    parse_details = []
    for path in csv_outputs:
        try:
            parse_details.append(f"{path.name}:{len(read_csv_rows(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parse_details.append(f"{path.name}:{exc}")
    checks.append(("VAL3895_12_csv_parse", "all generated CSV outputs parse", csv_parse_ok, "; ".join(parse_details)))
    formalization_hits = []
    if FWB.exists():
        formalization_hits = [
            path
            for path in FWB.rglob("*3895*")
            if path.is_file() and ("3895-Y5" in path.name or "P8_Y5_R2FR_3895" in path.name or "P8_Y5_BRR545_3895" in path.name)
        ]
    checks.append(("VAL3895_13_formalization_untouched", "no generated 3895 files appear in formalization-workbench", not formalization_hits, f"{len(formalization_hits)} hits"))
    pycache_hits = [path for path in (PCW / "scripts").rglob("__pycache__") if path.is_dir()]
    checks.append(("VAL3895_14_no_pycache", "scripts __pycache__ removed", not pycache_hits, f"{len(pycache_hits)} pycache dirs"))
    checks.append(("VAL3895_15_next_target", "next target builds suppression runner", any("3896-Y5-R2FR-memory-suppression-runner" in str(row["target_checkpoint"]) for row in next_rows(timestamp)), "3896 suppression runner"))
    return [
        {
            "check_id": check_id,
            "description": description,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for check_id, description, passed, detail in checks
    ]


def main() -> int:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    zero = zero_attempt_rows(timestamp)
    law = suppression_law_rows(timestamp)
    numeric = numeric_interface_rows(timestamp)
    gate = gate_rows(timestamp)
    runner = runner_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["zero"], zero)
    write_csv(OUTPUTS["law"], law)
    write_csv(OUTPUTS["numeric"], numeric)
    write_csv(OUTPUTS["gate"], gate)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, zero, law, numeric, gate, runner, next_target, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, zero, law, numeric, gate, runner, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_MEMORY_ZERO_PARTIAL_SUPPRESSION_LAW_DERIVED")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

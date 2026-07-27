from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "870-Y5-R10-P_loc-Jtrace-nohair-zero-theorem-or-bound.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_870_SOURCE_REGISTER.csv"
NOHAIR_PROOF_PATH = RESIDUALS / "P8_Y5_R10_870_JTRACE_NOHAIR_PROOF_ATTEMPT.csv"
PROJECTION_TEST_PATH = RESIDUALS / "P8_Y5_R10_870_LOCAL_PROJECTION_TESTS.csv"
CT_BOUND_PATH = RESIDUALS / "P8_Y5_R10_870_C_T_BOUND_INPUT_LEDGER.csv"
FAILURE_BRANCH_PATH = RESIDUALS / "P8_Y5_R10_870_FAILURE_BRANCH_LEDGER.csv"
ROUTE_CHOICE_PATH = RESIDUALS / "P8_Y5_R10_870_ROUTE_CHOICE.csv"
CLAIM_GUARD_PATH = RESIDUALS / "P8_Y5_R10_870_CLAIM_GUARD.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_870_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_870_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_870_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_870_VALIDATION.csv"

PRIOR_VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_869_VALIDATION.csv"

STATUS = "Y5_R10_870_Ploc_Jtrace_nohair_conditional_not_parent_signed_cT_retained_nonclaim"
CLAIM_CEILING = "conditional_trace_nohair_contract_only_cT_retained_no_q_loc_no_local_GR_claim"
NEXT_TARGET = "871-Y5-R10-cT-trace-leakage-bound-source-row-builder.md"

GENERATED_CSV_PATHS = [
    SOURCE_REGISTER_PATH,
    NOHAIR_PROOF_PATH,
    PROJECTION_TEST_PATH,
    CT_BOUND_PATH,
    FAILURE_BRANCH_PATH,
    ROUTE_CHOICE_PATH,
    CLAIM_GUARD_PATH,
    DECISION_PATH,
    NEXT_TARGET_PATH,
    NONCLAIM_SUMMARY_PATH,
]

SOURCE_SPECS = [
    {
        "source_id": "869_doc",
        "path": POST_CHECKPOINT / "869-Y5-R10-q_loc-residual-vector-decomposition-or-zero-theorem.md",
        "needles": [
            "P_loc_Jtrace_selected_first",
            "RR869_T",
            "870-Y5-R10-P_loc-Jtrace-nohair-zero-theorem-or-bound.md",
        ],
        "role": "immediate P_loc J_trace target handoff",
    },
    {
        "source_id": "869_validation",
        "path": PRIOR_VALIDATION_PATH,
        "needles": [
            "V869_6_ranked_target_ready,pass",
            "V869_9_all_rows_nonclaim,pass",
            "V869_10_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "861_boundary_nohair",
        "path": POST_CHECKPOINT / "861-Y5-R10-Ward-owned-boundary-charge-endpoint-and-N5-projector-closure.md",
        "needles": [
            "EP861_4_nohair",
            "boundary charge local no-hair",
            "QL861_0_definition",
        ],
        "role": "boundary charge no-hair debt",
    },
    {
        "source_id": "862_trace_lift_nohair",
        "path": POST_CHECKPOINT / "862-Y5-R10-trace-lift-endpoint-equation-and-coframe-pullback-closure.md",
        "needles": [
            "TL862_5_local_nohair_requirement",
            "EC862_4_endpoint_local_silence",
            "LG862_2_qloc_zero_if_all_silent",
        ],
        "role": "trace current local silence debt",
    },
    {
        "source_id": "863_trace_projection",
        "path": POST_CHECKPOINT / "863-Y5-R10-Ward-trace-lift-current-and-coframe-pullback-zero-theorem.md",
        "needles": [
            "WTC863_4_local_projection_silence",
            "CZT863_3_endpoint_boundary_silence",
            "LRF863_1_trace_leak_branch",
        ],
        "role": "P_loc J_trace conditional/failure branch",
    },
    {
        "source_id": "864_local_global_split",
        "path": POST_CHECKPOINT / "864-Y5-R10-local-global-quotient-split-and-endpoint-stationarity-parent-clause.md",
        "needles": [
            "Dq_FLRW[v_T] = delta Q_trace",
            "Dq_loc[U][v_T] = 0",
            "GN864_2_if_split_fails",
        ],
        "role": "q_FLRW/q_loc compatibility clause",
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
    return [
        {
            "source_id": spec["source_id"],
            "path": str(spec["path"]),
            "exists": str(spec["path"].exists()).lower(),
            "needle_check": check_needles(spec["path"], spec["needles"]),
            "role": spec["role"],
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for spec in SOURCE_SPECS
    ]


def nohair_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "proof_id": "NH870_0_current_owner",
            "required_clause": "J_trace^mu is a parent Ward/exact current with a defined support class",
            "candidate_argument": "if J_trace is a global FLRW/boundary current, local compact regions see it only through quotient-zero data",
            "what_would_follow": "P_loc J_trace can be a theorem rather than a screening assumption",
            "current_status": "definition_candidate_not_parent_owned",
            "blocker": "J_trace itself is still a contract, not a derived parent current",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "proof_id": "NH870_1_support_separation",
            "required_clause": "support(J_trace) is only FLRW zero-mode/global boundary support and not compact local exterior support",
            "candidate_argument": "for any local compact U not intersecting the cosmological boundary, P_loc J_trace|_U=0",
            "what_would_follow": "no local finite-range trace force from the endpoint branch",
            "current_status": "not_parent_derived",
            "blocker": "no support theorem forbids local tails or representative-dependent exact pieces",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "proof_id": "NH870_2_quotient_verticality",
            "required_clause": "Dq_loc[U][v_T]=0 while Dq_FLRW[v_T]!=0",
            "candidate_argument": "the trace direction is visible globally but vertical for local rods/clocks/matter",
            "what_would_follow": "trace memory can source FLRW without direct local matter/coframe variation",
            "current_status": "sufficient_clause_written_not_parent_derived",
            "blocker": "q_FLRW/q_loc compatibility is not action-level derived",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "proof_id": "NH870_3_multipole_silence",
            "required_clause": "boundary current has no local scalar gradient, vector B_0i, or traceless tensor B_TF multipoles",
            "candidate_argument": "pure monopole/FLRW endpoint support leaves no local PPN/clock/WEP projection",
            "what_would_follow": "gamma/beta/clock/orbital trace leakage is zero at the boundary-current level",
            "current_status": "open",
            "blocker": "no multipole/no-tail theorem is present",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "proof_id": "NH870_4_exact_current_local_gauge",
            "required_clause": "local exact representative is pure gauge or integrates to zero on local test domains",
            "candidate_argument": "P_loc(dB_trace)=0 when B_trace has no local gauge-invariant flux through local cycles",
            "what_would_follow": "exact-current wording becomes a real no-hair mechanism",
            "current_status": "plausible_but_unsigned",
            "blocker": "relative cohomology/current support not connected to parent variation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "proof_id": "NH870_5_nohair_verdict",
            "required_clause": "NH870_0 through NH870_4 all parent-signed",
            "candidate_argument": "then P_loc J_trace=0 and c_T=0",
            "what_would_follow": "first q_loc channel closes and local GR stack can move to matter descent/projector stress",
            "current_status": "not_proved",
            "blocker": "current owner, support separation, multipole silence, and local quotient derivation remain unsigned",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def projection_test_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "test_id": "PT870_0_compact_U_support",
            "local_test": "compact solar-system/lab domain U",
            "required_zero": "support(J_trace) cap U = empty or pure local gauge",
            "if_failed": "finite-range trace leakage",
            "observable_risk": "R10, orbital, clock",
            "status": "not_verified",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "test_id": "PT870_1_scalar_gradient",
            "local_test": "local scalar/monopole gradient",
            "required_zero": "P_loc grad Q_trace = 0 through tested order",
            "if_failed": "fifth force or GM drift",
            "observable_risk": "delta_G, Gdot/G, orbital residual",
            "status": "not_verified",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "test_id": "PT870_2_vector_tensor_hair",
            "local_test": "B_0i and B_TF boundary/projector components",
            "required_zero": "no local vector or traceless tensor trace-current projection",
            "if_failed": "preferred-frame/slip/projector residual",
            "observable_risk": "PPN gamma, alpha1/alpha2, lensing slip",
            "status": "not_verified",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "test_id": "PT870_3_clock_WEP_marker",
            "local_test": "species/clock marker dependence",
            "required_zero": "J_trace has no direct species or clock coupling",
            "if_failed": "composition or clock-channel trace leakage",
            "observable_risk": "WEP, atomic clocks",
            "status": "not_verified",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def ct_bound_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "bound_id": "CT870_0_alpha_lambda",
            "coefficient": "c_T_alpha_lambda",
            "needed_input": "map P_loc J_trace to finite-range alpha(lambda)",
            "units": "dimensionless alpha with lambda length",
            "source_status": "missing_parent_projection_and_bound_source",
            "claim_status": "valid_for_claim_false_until_numeric_sourced",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "bound_id": "CT870_1_PPN_gamma_beta",
            "coefficient": "c_T_PPN",
            "needed_input": "map trace leakage to gamma-1 and beta-1",
            "units": "dimensionless PPN residual",
            "source_status": "missing_projection_coefficient",
            "claim_status": "valid_for_claim_false_until_numeric_sourced",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "bound_id": "CT870_2_clock_WEP",
            "coefficient": "c_T_clock_WEP",
            "needed_input": "map trace leakage to clock drift and composition charge",
            "units": "fractional clock drift / Eotvos-like differential acceleration",
            "source_status": "missing_species_marker_projection",
            "claim_status": "valid_for_claim_false_until_numeric_sourced",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "bound_id": "CT870_3_orbital_GM",
            "coefficient": "c_T_orbital",
            "needed_input": "map trace leakage to GM drift or anomalous radial acceleration",
            "units": "fractional GM, Gdot/G, or acceleration",
            "source_status": "missing_source_normalization",
            "claim_status": "valid_for_claim_false_until_numeric_sourced",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def failure_branch_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "branch_id": "FB870_0_if_nohair_closes",
            "condition": "P_loc J_trace=0 parent-signed",
            "consequence": "set c_T=0 and move to matter descent/no-marker theorem for Pi_I^matter",
            "local_GR_impact": "one q_loc channel closed, not full local GR",
            "status": "conditional_not_current",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "branch_id": "FB870_1_if_nohair_fails",
            "condition": "P_loc J_trace not proved zero",
            "consequence": "retain c_T and source/bound it across R10, PPN, clocks, WEP, and orbital systems",
            "local_GR_impact": "no local GR claim until c_T is zeroed or safely bounded",
            "status": "current_fallback",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_choice_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC870_0_selected",
            "route": "cT_trace_leakage_bound_source_row_builder",
            "status": "selected",
            "reason": "P_loc J_trace no-hair remains unsigned; the honest next move is to source/bound c_T rather than claim local silence",
            "include": "alpha(lambda), PPN, clock/WEP, orbital GM rows with units and source-status flags",
            "exclude": "local GR claim, endpoint root algebra, unsourced numeric coefficients, formalization-workbench edits, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG870_0_no_Ploc_Jtrace_claim",
            "claim": "P_loc J_trace=0 is derived",
            "status": "forbidden",
            "reason": "no parent-signed support separation, multipole silence, exact-current local gauge, or q_loc quotient derivation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG870_1_no_cT_zero_claim",
            "claim": "c_T=0",
            "status": "forbidden",
            "reason": "c_T remains the retained trace leakage coefficient unless the no-hair theorem closes",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG870_2_no_local_GR_claim",
            "claim": "local GR/Newton follows",
            "status": "forbidden",
            "reason": "closing or bounding c_T is only the first q_loc channel",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG870_3_allowed_private_result",
            "claim": "trace no-hair proof obligations and c_T fallback rows are explicit",
            "status": "allowed_private_nonclaim",
            "reason": "870 converts the first q_loc channel into proof clauses plus bound inputs",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D870_0",
            "finding": "P_loc_Jtrace_zero_not_proved",
            "reason": "current owner, support separation, multipole silence, exact-current gauge, and local quotient derivation remain unsigned",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D870_1",
            "finding": "cT_retained",
            "reason": "trace endpoint leakage remains a boundable residual coefficient",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D870_2",
            "finding": "bound_source_rows_selected",
            "reason": "without no-hair proof, the next honest work is source-normalized c_T rows for R10/PPN/clock/WEP/orbital tests",
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
            "objective": "build source-ready c_T trace leakage bound rows for R10, PPN, clocks/WEP, and orbital tests without claiming local GR",
            "include": "units, observable map, missing parent projection flags, source URLs/paths if available, valid_for_claim=false unless fully numeric and sourced",
            "exclude": "unsourced numeric coefficients, local GR claim, endpoint root algebra, formalization-workbench edits, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "attempted P_loc J_trace no-hair theorem and identified exact unsigned clauses",
            "best_partial_result": "if current support, quotient verticality, multipole silence, and exact local gauge are signed, c_T=0 follows",
            "hard_blockers": "parent current owner, support separation, multipole/no-tail theorem, exact-current local gauge, q_loc quotient derivation",
            "what_is_not_claimed": "P_loc J_trace zero, c_T zero, q_loc zero, local GR/Newton",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_csv_rows_nonclaim(paths: list[Path]) -> tuple[bool, str]:
    offenders: list[str] = []
    for path in paths:
        if not path.exists():
            offenders.append(f"{path.name}:missing")
            continue
        with path.open("r", encoding="utf-8", newline="") as handle:
            for index, row in enumerate(csv.DictReader(handle), start=2):
                if row.get("valid_for_claim") != "false":
                    offenders.append(f"{path.name}:{index}")
    if offenders:
        return False, ";".join(offenders)
    return True, "all generated rows valid_for_claim=false"


def csv_table(rows: list[dict[str, object]], fieldnames: list[str]) -> str:
    lines = [
        "| " + " | ".join(fieldnames) + " |",
        "| " + " | ".join(["---"] * len(fieldnames)) + " |",
    ]
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ").replace("|", "/") for field in fieldnames]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_markdown(
    generated_utc: str,
    source_rows: list[dict[str, object]],
    nohair_rows_: list[dict[str, object]],
    projection_rows: list[dict[str, object]],
    ct_rows: list[dict[str, object]],
    failure_rows: list[dict[str, object]],
    route_rows: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    content = f"""# 870 - P_loc Jtrace Nohair Zero Theorem Or Bound

Generated: `{generated_utc}`

Current result: **the first local `q_loc` channel is conditionally clean but not derived**. If `J_trace` is a parent-owned global/FLRW boundary current, if it has no compact local support, if `Q_trace` is locally quotient-vertical, if all local multipoles/tails vanish, and if exact-current representatives are pure local gauge, then `P_loc J_trace=0` and `c_T=0`. The corpus does not yet sign those clauses. Therefore `c_T` remains retained and must be source/bound-ready across R10, PPN, clocks/WEP, and orbital systems.

## Nonclaim Summary

{csv_table(summary_rows, ["status", "claim_ceiling", "what_changed", "best_partial_result", "hard_blockers", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"])}

## Source Register

{csv_table(source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])}

## Jtrace Nohair Proof Attempt

{csv_table(nohair_rows_, ["proof_id", "required_clause", "candidate_argument", "what_would_follow", "current_status", "blocker", "valid_for_claim", "generated_utc"])}

## Local Projection Tests

{csv_table(projection_rows, ["test_id", "local_test", "required_zero", "if_failed", "observable_risk", "status", "valid_for_claim", "generated_utc"])}

## c_T Bound Input Ledger

{csv_table(ct_rows, ["bound_id", "coefficient", "needed_input", "units", "source_status", "claim_status", "valid_for_claim", "generated_utc"])}

## Failure Branch Ledger

{csv_table(failure_rows, ["branch_id", "condition", "consequence", "local_GR_impact", "status", "valid_for_claim", "generated_utc"])}

## Route Choice

{csv_table(route_rows, ["route_id", "route", "status", "reason", "include", "exclude", "valid_for_claim", "generated_utc"])}

## Claim Guard

{csv_table(claim_rows, ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"])}

## Decision

{csv_table(decision_rows_, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])}

## Next Target

{csv_table(next_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])}

## Validation

{csv_table(validation_rows, ["check_id", "result", "detail"])}
"""
    OUTPUT_DOC.write_text(content, encoding="utf-8")


def main() -> None:
    generated_utc = datetime.now(timezone.utc).isoformat()

    source_rows = source_register_rows(generated_utc)
    nohair_rows_ = nohair_rows(generated_utc)
    projection_rows = projection_test_rows(generated_utc)
    ct_rows = ct_bound_rows(generated_utc)
    failure_rows = failure_branch_rows(generated_utc)
    route_rows = route_choice_rows(generated_utc)
    claim_rows = claim_guard_rows(generated_utc)
    decision_rows_ = decision_rows(generated_utc)
    next_rows = next_target_rows(generated_utc)
    summary_rows = nonclaim_summary_rows(generated_utc)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(NOHAIR_PROOF_PATH, nohair_rows_, ["proof_id", "required_clause", "candidate_argument", "what_would_follow", "current_status", "blocker", "valid_for_claim", "generated_utc"])
    write_csv(PROJECTION_TEST_PATH, projection_rows, ["test_id", "local_test", "required_zero", "if_failed", "observable_risk", "status", "valid_for_claim", "generated_utc"])
    write_csv(CT_BOUND_PATH, ct_rows, ["bound_id", "coefficient", "needed_input", "units", "source_status", "claim_status", "valid_for_claim", "generated_utc"])
    write_csv(FAILURE_BRANCH_PATH, failure_rows, ["branch_id", "condition", "consequence", "local_GR_impact", "status", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_CHOICE_PATH, route_rows, ["route_id", "route", "status", "reason", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_GUARD_PATH, claim_rows, ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decision_rows_, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary_rows, ["status", "claim_ceiling", "what_changed", "best_partial_result", "hard_blockers", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"])

    prior_clean, prior_detail = validation_file_clean(PRIOR_VALIDATION_PATH)
    source_checks_pass = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    nohair_verdict_pass = any(row["proof_id"] == "NH870_5_nohair_verdict" and row["current_status"] == "not_proved" for row in nohair_rows_)
    projection_tests_pass = len(projection_rows) == 4 and all(row["status"] == "not_verified" for row in projection_rows)
    ct_rows_pass = len(ct_rows) == 4 and all(row["valid_for_claim"] == "false" for row in ct_rows)
    failure_branch_pass = any(row["branch_id"] == "FB870_1_if_nohair_fails" and row["status"] == "current_fallback" for row in failure_rows)
    route_selected_pass = route_rows[0]["route"] == "cT_trace_leakage_bound_source_row_builder"
    claim_allowed_false_pass = all(row["claim_allowed"] == "false" for row in decision_rows_)
    formalization_count = formalization_workbench_modified_count()

    validation_rows = [
        {"check_id": "V870_0_sources_exist_and_needles", "result": "pass" if source_checks_pass else "fail", "detail": "all source paths exist and needles are present" if source_checks_pass else "one or more source checks failed"},
        {"check_id": "V870_1_prior_869_clean", "result": "pass" if prior_clean else "fail", "detail": prior_detail},
        {"check_id": "V870_2_nohair_not_promoted", "result": "pass" if nohair_verdict_pass else "fail", "detail": "P_loc J_trace verdict remains not_proved"},
        {"check_id": "V870_3_projection_tests_ready", "result": "pass" if projection_tests_pass else "fail", "detail": "local projection tests recorded as not_verified"},
        {"check_id": "V870_4_cT_bound_rows_ready", "result": "pass" if ct_rows_pass else "fail", "detail": "c_T bound input rows remain nonclaim"},
        {"check_id": "V870_5_failure_branch_ready", "result": "pass" if failure_branch_pass else "fail", "detail": "c_T fallback branch selected if nohair fails"},
        {"check_id": "V870_6_route_selected", "result": "pass" if route_selected_pass else "fail", "detail": NEXT_TARGET},
        {"check_id": "V870_7_claim_allowed_false", "result": "pass" if claim_allowed_false_pass else "fail", "detail": "decision rows keep claim_allowed=false"},
        {"check_id": "V870_8_all_rows_nonclaim", "result": "pending", "detail": "filled after csv nonclaim scan"},
        {"check_id": "V870_9_formalization_workbench_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={formalization_count}"},
        {"check_id": "V870_10_validation_rows_ready", "result": "pass", "detail": "validation table constructed"},
    ]

    nonclaim_pass, nonclaim_detail = all_csv_rows_nonclaim(GENERATED_CSV_PATHS)
    for row in validation_rows:
        if row["check_id"] == "V870_8_all_rows_nonclaim":
            row["result"] = "pass" if nonclaim_pass else "fail"
            row["detail"] = nonclaim_detail

    write_csv(VALIDATION_PATH, validation_rows, ["check_id", "result", "detail"])
    write_markdown(
        generated_utc,
        source_rows,
        nohair_rows_,
        projection_rows,
        ct_rows,
        failure_rows,
        route_rows,
        claim_rows,
        decision_rows_,
        next_rows,
        summary_rows,
        validation_rows,
    )

    failed = [row for row in validation_rows if row["result"] != "pass"]
    print(f"status={STATUS}")
    print("partial_result=P_loc J_trace nohair theorem is conditional only; c_T trace leakage rows retained")
    print(f"claim_ceiling={CLAIM_CEILING}")
    print(f"next_target={NEXT_TARGET}")
    if failed:
        for row in failed:
            print(f"validation_failure={row['check_id']}:{row['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()

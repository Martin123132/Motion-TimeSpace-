from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "828-Y5-R10-XB-Lcg-local-constancy-or-Khat-owner-theorem.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_828_SOURCE_REGISTER.csv"
BASELINE_LOCK_PATH = RESIDUALS / "P8_Y5_R10_828_BASELINE_LOCK_THEOREM.csv"
KHAT_OWNER_PATH = RESIDUALS / "P8_Y5_R10_828_KHAT_OWNER_AUDIT.csv"
QUADRATIC_BOUND_PATH = RESIDUALS / "P8_Y5_R10_828_QUADRATIC_RESIDUAL_BOUND.csv"
PROMOTION_GATE_PATH = RESIDUALS / "P8_Y5_R10_828_PROMOTION_GATE.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_828_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_828_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_828_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_828_VALIDATION.csv"

STATUS = "Y5_R10_828_baseline_lock_reduces_q_loc_to_quadratic_memory_Khat_bound_still_open_nonclaim"
CLAIM_CEILING = "conditional_baseline_lock_theorem_only_no_numeric_residual_vector_no_local_GR_claim"
NEXT_TARGET = "829-Y5-R10-baseline-lock-source-support-residual-budget.md"

SOURCE_SPECS = [
    {
        "source_id": "827_doc",
        "path": POST_CHECKPOINT / "827-Y5-R10-XB-drift-and-Khat-bound-after-F1-zero.md",
        "needles": [
            "DI827_3_post_F1_residual_gradient",
            "G827_2_baseline_drift",
            "828-Y5-R10-XB-Lcg-local-constancy-or-Khat-owner-theorem.md",
        ],
        "role": "immediate post-F1 baseline-drift handoff",
    },
    {
        "source_id": "827_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_827_VALIDATION.csv",
        "needles": [
            "V827_2_moving_extremum_cancellation_recorded,pass",
            "V827_6_local_GR_still_blocked,pass",
            "V827_11_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "parent_equations_v1",
        "path": FORMALIZATION / "83-parent-equations-v1.md",
        "needles": [
            "Gamma_eff = Gamma_L = constant",
            "nabla_mu K_hat^{mu nu} = 0.",
            "Gamma_eff -> Lambda_loc",
            "nabla^nu Gamma_eff -> 0 or PPN-bounded",
        ],
        "role": "local GR/Newton limit target",
    },
    {
        "source_id": "826_doc",
        "path": POST_CHECKPOINT / "826-Y5-R10-parent-memory-action-coefficient-checklist.md",
        "needles": [
            "F826_1_F1_zero",
            "C826_5_Khat_response",
            "LC826_1_local_residual_vector",
        ],
        "role": "F1 zero and Khat response gap",
    },
    {
        "source_id": "equation_register",
        "path": FORMALIZATION / "05-equation-register.md",
        "needles": [
            "q^nu = nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu}",
            "K_hat has no independent divergence when delta m = 0",
            "Source-support / boundary-amplitude law",
        ],
        "role": "q/Khat identity and residual-bound obligations",
    },
    {
        "source_id": "XB_firewall",
        "path": FORMALIZATION / "85-coarse-graining-invariants-XB.md",
        "needles": [
            "If `X_B` is arbitrary",
            "transition shells remain local PPN obligations,",
            "source-power closure open.",
        ],
        "role": "X_B universality and transition-shell firewall",
    },
]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def check_needles(path: Path, needles: list[str]) -> str:
    if not path.exists():
        return "missing_path"
    text = path.read_text(encoding="utf-8", errors="replace")
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return "missing_needles:" + ";".join(missing)
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


def baseline_lock_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "theorem_id": "BL828_0_baseline_definition",
            "statement": "Define the local baseline trace as Gamma_L(X)=L_cg(X)^-2 F_L(X).",
            "derivation": "This is the delta_m=0 part of the 827 trace-lock expression.",
            "result": "definition",
            "blocker": "Gamma_L must descend from parent K_MTS trace projection",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "BL828_1_baseline_gradient",
            "statement": "nabla Gamma_L=L_cg^-2[partial_A F_L-2F_L partial_A ln L_cg]nabla X^A.",
            "derivation": "Differentiate Gamma_L=L_cg^-2 F_L with respect to the X_B invariant bundle.",
            "result": "derived_identity",
            "blocker": "this is the linear term left open by 827",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "BL828_2_local_baseline_lock",
            "statement": "If the parent local branch enforces Gamma_L(X)=Lambda_loc=constant, equivalently F_L(X)=Lambda_loc L_cg(X)^2 along the tested local branch, then nabla Gamma_L=0 even when nabla X is not zero.",
            "derivation": "Insert F_L=Lambda_loc L_cg^2 into BL828_1; the bracket partial_A F_L-2F_L partial_A ln L_cg vanishes.",
            "result": "baseline_drift_zero_conditional",
            "blocker": "must derive Lambda_loc and the branch relation from parent equations, not choose it for local tests",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "BL828_3_post_lock_q",
            "statement": "With F1=0, moving-extremum cancellation, and baseline lock, q_loc=P_loc[a_F L^-2 R_mm delta_m nabla delta_m + O(delta_m^2 nabla X, delta_m^2 nabla delta_m) - nabla_mu K_hat^{mu nu}].",
            "derivation": "Apply BL828_2 to the 827 q_loc residual contract.",
            "result": "linear_trace_terms_removed_conditionally",
            "blocker": "quadratic residual, Khat divergence, boundary data, and matter readout still need bounds",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "BL828_4_no_free_local_constant",
            "statement": "The baseline lock is not the same as assuming X_B is constant; it is a relation among parent coefficients that can tolerate local environmental gradients.",
            "derivation": "BL828_2 removes the contraction coefficient multiplying nabla X, rather than setting nabla X to zero.",
            "result": "least_cheaty_route_selected",
            "blocker": "relation must be produced by a parent local vacuum branch or it becomes a new closure axiom",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def khat_owner_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "owner_id": "KO828_0_scalar_memory_limit",
            "candidate_owner": "K_hat from scalar memory Hilbert stress after baseline lock",
            "status": "partially_compatible",
            "reason": "if delta_m=0 and boundary data are zero, scalar-gradient anisotropic stress has no independent linear divergence",
            "missing": "actual K_hat functional, boundary theorem, and response map to PPN/R10/clock/orbital observables",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "owner_id": "KO828_1_baseline_without_lock",
            "candidate_owner": "K_hat cancels nonzero baseline F_L/L_cg drift",
            "status": "not_accepted_without_parent_variation",
            "reason": "a scalar memory Khat is quadratic near local equilibrium and cannot be assumed to cancel arbitrary baseline X_B gradients",
            "missing": "variation of X_B/L_cg ancestors and bath/source stress",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "owner_id": "KO828_2_tensor_boundary",
            "candidate_owner": "tensor boundary condition K_hat divergence zero/decaying in local branch",
            "status": "open",
            "reason": "local GR requires no incoming tensor/boundary hair that reintroduces PPN residuals",
            "missing": "coercive/static or hyperbolic boundary theorem with source-backed boundary data",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "owner_id": "KO828_3_matter_descent",
            "candidate_owner": "ordinary matter couples only to the GR metric in the local locked branch",
            "status": "open",
            "reason": "even q_loc suppression is not enough if matter directly reads memory/X_B variables",
            "missing": "species-independent matter-frame descent or WEP/clock bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def quadratic_bound_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "bound_id": "QB828_0_symbolic_bound",
            "term": "a_F L^-2 R_mm delta_m nabla delta_m",
            "symbolic_bound": "|q_quad| <= |a_F| L^-2 |R_mm| |delta_m| |nabla delta_m|",
            "safe_condition": "source-backed delta_m and gradient bounds beat local residual budgets",
            "status": "symbolic_only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "bound_id": "QB828_1_support_power_bound",
            "term": "local screened memory perturbation",
            "symbolic_bound": "if delta_m=O(U_B^pS) and nabla delta_m=O(U_B^pS/L_tr), then |q_quad|=O(U_B^(2pS)/(L_cg^2 L_tr))",
            "safe_condition": "derive U_B profile, pS, transition width, and response conversion to PPN/R10/clock/orbit units",
            "status": "conditional_scaling",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "bound_id": "QB828_2_second_order_X",
            "term": "O(delta_m^2 nabla X)",
            "symbolic_bound": "|q_X2| <= C_X delta_m^2 |nabla X|/L_cg^2",
            "safe_condition": "moving-extremum cancellation holds and X_B gradients are bounded in tested systems",
            "status": "conditional_scaling",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "bound_id": "QB828_3_Khat_residual",
            "term": "nabla_mu K_hat^{mu nu}",
            "symbolic_bound": "|q_K| <= response_norm[K_hat source,boundary]",
            "safe_condition": "derive Khat owner or compute residual vector directly",
            "status": "open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def promotion_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "PG828_0_baseline_lock",
            "gate": "Does the baseline lock kill F_L/L_cg drift without setting nabla X_B=0?",
            "result": "pass_conditional",
            "consequence": "linear baseline trace source can vanish if Gamma_L is parent-constant on the local branch",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG828_1_parent_source",
            "gate": "Is Gamma_L=Lambda_loc derived from the parent action/coarse-graining theorem?",
            "result": "fail_open",
            "consequence": "baseline lock is not claimable yet",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG828_2_quadratic_residual_bound",
            "gate": "Are the remaining quadratic memory and second-order X_B terms below local budgets?",
            "result": "missing_numeric_bound",
            "consequence": "need residual budget before local-GR promotion",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "PG828_3_Khat_and_matter",
            "gate": "Are K_hat divergence, boundary data, and matter descent owned?",
            "result": "fail_open",
            "consequence": "no local-GR/Newton/PPN claim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D828_0",
            "decision": "select baseline lock as the least-cheaty local drift route",
            "reason": "it kills the F_L/L_cg linear drift by a parent coefficient relation, not by pretending local environmental gradients vanish",
            "claim_ceiling": CLAIM_CEILING,
            "runnable": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D828_1",
            "decision": "local GR remains unclaimed",
            "reason": "baseline lock is conditional and the remaining quadratic/Khat/matter residuals still lack source-backed numerical bounds",
            "claim_ceiling": CLAIM_CEILING,
            "runnable": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def next_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "turn the baseline-lock theorem into a source-support residual budget for q_loc and define the exact local residual vector needed for PPN/R10/clock/orbital/WEP gates",
            "allowed_work": "symbolic-to-numeric budget structure, U_B support powers, transition width, Khat residual contract, observable residual vector",
            "forbidden_work": "local-GR claim, data fitting, C2A closure promotion, unsourced numeric coefficients",
            "priority": "high",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_survived": "baseline lock can kill the remaining linear trace drift while allowing nonzero local X_B gradients",
            "what_failed": "parent derivation of the lock, numerical quadratic residual budget, Khat boundary theorem, and matter descent",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def validation_rows(
    source_rows: list[dict[str, object]],
    baseline_rows: list[dict[str, object]],
    khat_rows: list[dict[str, object]],
    bound_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail})

    add(
        "V828_0_sources_exist_and_needles",
        all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows),
        "all source paths exist and needles are present",
    )
    clean_827, clean_827_detail = validation_file_clean(RESIDUALS / "P8_Y5_BRR545_827_VALIDATION.csv")
    add("V828_1_prior_827_clean", clean_827, clean_827_detail)
    add(
        "V828_2_baseline_gradient_identity",
        any(row["theorem_id"] == "BL828_1_baseline_gradient" and row["result"] == "derived_identity" for row in baseline_rows),
        "baseline gradient identity recorded",
    )
    add(
        "V828_3_baseline_lock_condition",
        any(row["theorem_id"] == "BL828_2_local_baseline_lock" and row["result"] == "baseline_drift_zero_conditional" for row in baseline_rows),
        "baseline lock condition recorded",
    )
    add(
        "V828_4_post_lock_q_contract",
        any(row["theorem_id"] == "BL828_3_post_lock_q" for row in baseline_rows),
        "post-lock q_loc contract recorded",
    )
    add(
        "V828_5_Khat_matter_gaps_recorded",
        {"KO828_2_tensor_boundary", "KO828_3_matter_descent"}.issubset({row["owner_id"] for row in khat_rows}),
        "Khat boundary and matter descent gaps recorded",
    )
    add(
        "V828_6_quadratic_bounds_present",
        {"QB828_0_symbolic_bound", "QB828_1_support_power_bound", "QB828_3_Khat_residual"}.issubset({row["bound_id"] for row in bound_rows}),
        "symbolic, support-power, and Khat residual bounds present",
    )
    add(
        "V828_7_promotion_still_blocked",
        any(row["gate_id"] == "PG828_1_parent_source" and row["result"] == "fail_open" for row in gates)
        and any(row["gate_id"] == "PG828_3_Khat_and_matter" and row["result"] == "fail_open" for row in gates),
        "parent source and Khat/matter gates remain open",
    )
    add(
        "V828_8_decision_nonrunnable",
        all(row["runnable"] == "false" for row in decisions),
        "branch remains non-runnable",
    )
    add(
        "V828_9_next_target_selected",
        any(row["next_target"] == NEXT_TARGET for row in next_rows),
        NEXT_TARGET,
    )
    all_rows = source_rows + baseline_rows + khat_rows + bound_rows + gates + decisions + next_rows + summary
    add(
        "V828_10_all_rows_nonclaim",
        all(row.get("valid_for_claim") == "false" for row in all_rows),
        "all generated rows valid_for_claim=false",
    )
    add(
        "V828_11_no_data_or_local_GR_claim",
        all("data fitting" in row["forbidden_work"] and "local-GR claim" in row["forbidden_work"] for row in next_rows),
        "no data or local-GR claim selected",
    )
    changed = formalization_workbench_modified_count()
    add(
        "V828_12_formalization_workbench_untouched",
        changed == 0,
        f"formalization_changed_after_cutoff={changed}",
    )
    add("V828_13_validation_rows_ready", True, "validation table constructed")
    return rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def render_document(
    generated_utc: str,
    source_rows: list[dict[str, object]],
    baseline_rows: list[dict[str, object]],
    khat_rows: list[dict[str, object]],
    bound_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    summary: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> str:
    return "\n\n".join(
        [
            "# 828 - Y5 R10 X_B Lcg Local Constancy Or Khat Owner Theorem",
            (
                "Current result: **the best local drift route is a conditional baseline lock**. "
                "The parent local branch can kill the remaining linear trace drift by enforcing `Gamma_L(X_B)=L_cg^{-2}F_L(X_B)=Lambda_loc`, without pretending `nabla X_B=0`. "
                "After this lock, `q_loc` is reduced to quadratic memory terms plus owned/bounded `K_hat` response."
            ),
            f"Generated UTC: `{generated_utc}`",
            "## Nonclaim Summary\n\n" + markdown_table(summary, ["status", "claim_ceiling", "what_survived", "what_failed", "next_target", "valid_for_claim"]),
            "## Baseline Lock Theorem\n\n" + markdown_table(baseline_rows, ["theorem_id", "statement", "derivation", "result", "blocker", "valid_for_claim"]),
            "## Khat Owner Audit\n\n" + markdown_table(khat_rows, ["owner_id", "candidate_owner", "status", "reason", "missing", "valid_for_claim"]),
            "## Quadratic Residual Bound\n\n" + markdown_table(bound_rows, ["bound_id", "term", "symbolic_bound", "safe_condition", "status", "valid_for_claim"]),
            "## Promotion Gate\n\n" + markdown_table(gates, ["gate_id", "gate", "result", "consequence", "valid_for_claim"]),
            "## Decision\n\n" + markdown_table(decisions, ["decision_id", "decision", "reason", "claim_ceiling", "runnable", "next_target", "valid_for_claim"]),
            "## Next Target\n\n" + markdown_table(next_rows, ["next_target", "objective", "allowed_work", "forbidden_work", "valid_for_claim"]),
            "## Source Register\n\n" + markdown_table(source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"]),
            "## Validation\n\n" + markdown_table(validation, ["check_id", "result", "detail"]),
            "## Verdict\n\n"
            "This is the cleanest form of the local route so far: `F_1=0`, moving-extremum cancellation, and baseline lock together remove the linear trace-gradient channels. "
            "But the parent must still derive the lock and the remaining quadratic/Khat/matter residuals must be budgeted before any local-GR claim.",
        ]
    )


def main() -> None:
    generated_utc = datetime.now(timezone.utc).isoformat(timespec="seconds")

    source_rows = source_register_rows(generated_utc)
    baseline_rows = baseline_lock_rows(generated_utc)
    khat_rows = khat_owner_rows(generated_utc)
    bound_rows = quadratic_bound_rows(generated_utc)
    gates = promotion_gate_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    next_rows = next_target_rows(generated_utc)
    summary = nonclaim_summary_rows(generated_utc)
    validation = validation_rows(source_rows, baseline_rows, khat_rows, bound_rows, gates, decisions, next_rows, summary)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(BASELINE_LOCK_PATH, baseline_rows, ["theorem_id", "statement", "derivation", "result", "blocker", "valid_for_claim", "generated_utc"])
    write_csv(KHAT_OWNER_PATH, khat_rows, ["owner_id", "candidate_owner", "status", "reason", "missing", "valid_for_claim", "generated_utc"])
    write_csv(QUADRATIC_BOUND_PATH, bound_rows, ["bound_id", "term", "symbolic_bound", "safe_condition", "status", "valid_for_claim", "generated_utc"])
    write_csv(PROMOTION_GATE_PATH, gates, ["gate_id", "gate", "result", "consequence", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "reason", "claim_ceiling", "runnable", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_rows, ["next_target", "objective", "allowed_work", "forbidden_work", "priority", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "what_survived", "what_failed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])

    OUTPUT_DOC.write_text(
        render_document(generated_utc, source_rows, baseline_rows, khat_rows, bound_rows, gates, decisions, next_rows, summary, validation),
        encoding="utf-8",
    )

    failed = [row for row in validation if row["result"] != "pass"]
    if failed:
        details = "; ".join(f"{row['check_id']}={row['detail']}" for row in failed)
        raise SystemExit(f"828 validation failed: {details}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")


if __name__ == "__main__":
    main()

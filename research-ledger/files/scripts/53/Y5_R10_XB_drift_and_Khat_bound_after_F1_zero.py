from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "827-Y5-R10-XB-drift-and-Khat-bound-after-F1-zero.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_827_SOURCE_REGISTER.csv"
DRIFT_IDENTITY_PATH = RESIDUALS / "P8_Y5_R10_827_DRIFT_IDENTITY.csv"
KHAT_RESPONSE_PATH = RESIDUALS / "P8_Y5_R10_827_KHAT_RESPONSE_CONTRACT.csv"
RESIDUAL_CONTRACT_PATH = RESIDUALS / "P8_Y5_R10_827_QLOC_RESIDUAL_CONTRACT.csv"
GATE_PATH = RESIDUALS / "P8_Y5_R10_827_LOCAL_GR_GATE.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_827_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_827_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_827_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_827_VALIDATION.csv"

STATUS = "Y5_R10_827_F1_and_moving_extremum_cancel_memory_linear_drift_baseline_Khat_open_nonclaim"
CLAIM_CEILING = "conditional_gradient_identity_only_no_Khat_owner_no_local_GR_claim"
NEXT_TARGET = "828-Y5-R10-XB-Lcg-local-constancy-or-Khat-owner-theorem.md"

SOURCE_SPECS = [
    {
        "source_id": "826_doc",
        "path": POST_CHECKPOINT / "826-Y5-R10-parent-memory-action-coefficient-checklist.md",
        "needles": [
            "F826_1_F1_zero",
            "F826_3_drift_not_solved",
            "827-Y5-R10-XB-drift-and-Khat-bound-after-F1-zero.md",
        ],
        "role": "immediate F1-zero handoff",
    },
    {
        "source_id": "826_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_826_VALIDATION.csv",
        "needles": [
            "V826_4_F1_zero_conditional_lemma_recorded,pass",
            "V826_5_drift_and_Khat_open_recorded,pass",
            "V826_12_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "parent_equations_v1",
        "path": FORMALIZATION / "83-parent-equations-v1.md",
        "needles": [
            "q^nu = nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu}.",
            "partial_m Gamma_eff |_(m=m_L) = 0",
            "X_B cannot be selected differently for galaxies, cosmology, and local gravity after seeing the data.",
        ],
        "role": "parent q/Khat identity and trace lock",
    },
    {
        "source_id": "798_gamma_screening",
        "path": POST_CHECKPOINT / "798-Y5-R10-Gammaeff-local-screening-source-law-or-response-kernel-bound.md",
        "needles": [
            "GSE798_1_gradient_expansion",
            "GSE798_2_local_locked_expansion",
            "TCB798_5_Kperp_boundary",
        ],
        "role": "pre-827 gradient expansion and Kperp warning",
    },
    {
        "source_id": "equation_register",
        "path": FORMALIZATION / "05-equation-register.md",
        "needles": [
            "q^nu = nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu}",
            "The real Solar branch remains open until `F_1`, `M_tr`, `ell_tr`, `L_cg`, boundary data, and `K_perp,loc` are derived.",
            "K_hat has no independent divergence when delta m = 0",
        ],
        "role": "local branch obligations and Khat caveat",
    },
    {
        "source_id": "XB_firewall",
        "path": FORMALIZATION / "85-coarse-graining-invariants-XB.md",
        "needles": [
            "If `X_B` is arbitrary",
            "transition shells remain local PPN obligations,",
            "source-power closure open.",
        ],
        "role": "universal X_B firewall and transition-shell warning",
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


def drift_identity_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "identity_id": "DI827_0_trace_lock",
            "statement": "Gamma_eff=L(X)^-2 H(m,X), with H=F_L(X)+a_F[R(m,X)-R(m_L(X),X)] and R_m(m_L(X),X)=0.",
            "derivation": "Use the 826 trace-lock ansatz and treat X as the covariant X_B invariant bundle.",
            "result": "setup_conditional",
            "remaining_blocker": "H and L must descend from K_MTS/coarse-graining, not be chosen per sector",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "identity_id": "DI827_1_full_gradient",
            "statement": "nabla_n Gamma_eff=L^-2 nabla_n H - 2 L^-2 H nabla_n ln L.",
            "derivation": "Ordinary product rule for Gamma_eff=L^-2 H.",
            "result": "derived_identity",
            "remaining_blocker": "nabla H must be expanded into m, X_B, and moving-equilibrium pieces",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "identity_id": "DI827_2_moving_extremum_cancellation",
            "statement": "If m_L(X) is an extremum for every X, then d_X R_m(m_L(X),X)=R_mX+R_mm m_L,X=0, so the linear delta_m*nabla X term from the R sector cancels.",
            "derivation": "Differentiate the identity R_m(m_L(X),X)=0 with respect to X.",
            "result": "linear_memory_X_drift_cancels_conditionally",
            "remaining_blocker": "requires the same parent R to define both m_L and the trace projection",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "identity_id": "DI827_3_post_F1_residual_gradient",
            "statement": "Near m=m_L+delta_m, nabla Gamma_eff=L^-2[(partial_X F_L-2F_L partial_X ln L)nabla X + a_F R_mm delta_m nabla delta_m + O(delta_m^2 nabla X, delta_m^2 nabla delta_m)] plus higher baseline terms.",
            "derivation": "Taylor expand R about the moving extremum and apply DI827_2.",
            "result": "baseline_drift_plus_quadratic_memory_channel",
            "remaining_blocker": "baseline drift and K_hat response are not killed by F1=0",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "identity_id": "DI827_4_projected_q_loc",
            "statement": "q_loc^nu=P_loc[nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu}], so after F1=0 the local residual is baseline drift + quadratic memory channel - K_hat divergence.",
            "derivation": "Insert DI827_3 into the parent q/Khat identity.",
            "result": "q_loc_residual_contract",
            "remaining_blocker": "must derive baseline constancy or a K_hat owner/bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def khat_response_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "response_id": "KH827_0_no_hand_set_Khat",
            "candidate": "Set div K_hat equal to nabla Gamma_eff by definition.",
            "status": "rejected",
            "reason": "this would hide the local-GR problem in a tensor counterterm unless K_hat is varied from the parent action with boundary data",
            "needed_next": "derive K_hat^{mu nu}[m,X_B,psi] or compute an explicit residual bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "response_id": "KH827_1_scalar_memory_stress",
            "candidate": "K_hat from the Hilbert stress of a scalar memory sector L_m=-1/2 Z_m(X)nabla m^2-V_R(m,X).",
            "status": "insufficient_by_itself",
            "reason": "near the local extremum its anisotropic stress is gradient/quadratic and does not automatically cancel baseline X_B/L_cg drift",
            "needed_next": "include X_B ancestors, L_cg variation, and bath/source stress in the same Ward identity",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "response_id": "KH827_2_XB_spurion_source",
            "candidate": "Treat X_B and L_cg as external environmental profiles.",
            "status": "fails_parent_gate",
            "reason": "external gradients behave like spurion sources and can re-create q_loc even after F1=0",
            "needed_next": "derive X_B/L_cg from covariant fields or prove local gradients are below residual budgets",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "response_id": "KH827_3_Khat_owner_contract",
            "candidate": "Accept K_hat only if parent variation gives div K_hat = baseline drift + bounded higher-order memory terms in tested local systems.",
            "status": "open_contract",
            "reason": "this is the cleanest route to local q_loc suppression without a plateau axiom",
            "needed_next": "write Khat owner theorem or residual-vector bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def residual_contract_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "term_id": "Q827_0_baseline_F_L",
            "residual_term": "P_loc L^-2 partial_X F_L nabla X",
            "status": "open_linear_term",
            "safe_if": "partial_X F_L=0 locally, nabla X=0 locally, or K_hat/bath stress cancels it with Ward ownership",
            "claim_risk": "linear local source survives F1 zero",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "term_id": "Q827_1_Lcg_drift",
            "residual_term": "-2 P_loc L^-2 F_L nabla ln L",
            "status": "open_linear_term",
            "safe_if": "L_cg is locally constant/adiabatic below bounds or its variation is owned by K_hat/bath stress",
            "claim_risk": "trace-baseline gradient looks like local nonconservation/source",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "term_id": "Q827_2_quadratic_memory",
            "residual_term": "P_loc L^-2 a_F R_mm delta_m nabla delta_m",
            "status": "conditionally_suppressed",
            "safe_if": "delta_m and nabla delta_m are bounded by sourced local relaxation/support powers",
            "claim_risk": "can still fail in transition shells if delta_m gradients are not suppressed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "term_id": "Q827_3_second_order_X_drift",
            "residual_term": "O(delta_m^2 nabla X)",
            "status": "higher_order_conditional",
            "safe_if": "moving-extremum cancellation holds and delta_m is small enough",
            "claim_risk": "still needs a bound; not a zero theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "term_id": "Q827_4_Khat_divergence",
            "residual_term": "-P_loc nabla_mu K_hat^{mu nu}",
            "status": "owner_missing",
            "safe_if": "parent action derives the tensor response and boundary data or an explicit residual-vector bound passes",
            "claim_risk": "hand-setting K_hat is equivalent to smuggling in a cancellation axiom",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "G827_0_F1_zero_survives",
            "gate": "Does F1=0 survive the drift expansion?",
            "result": "pass_conditional",
            "consequence": "the direct linear m-channel remains killed if R owns both trace lock and local equilibrium",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "G827_1_moving_extremum_cancellation",
            "gate": "Does moving m_L(X_B) reintroduce a linear delta_m*nabla X_B term?",
            "result": "pass_conditional",
            "consequence": "the R-sector linear delta_m*nabla X term cancels by differentiating R_m(m_L(X),X)=0",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "G827_2_baseline_drift",
            "gate": "Are F_L and L_cg baseline gradients killed or bounded?",
            "result": "fail_open",
            "consequence": "local GR remains blocked unless X_B/L_cg constancy or K_hat ownership is derived",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "G827_3_Khat_owner",
            "gate": "Is K_hat response derived from parent variation and boundary data?",
            "result": "fail_open",
            "consequence": "cannot claim q_loc -> 0 from F1 zero alone",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "G827_4_local_residual_vector",
            "gate": "Does the branch produce a numeric/source-backed PPN/R10/clock/orbital/WEP residual vector?",
            "result": "missing",
            "consequence": "no local-GR/Newton claim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D827_0",
            "decision": "record the moving-extremum cancellation as a conditional mathematical win",
            "reason": "R_m(m_L(X),X)=0 implies R_mX+R_mm m_L,X=0, so the R-sector linear delta_m*nabla X drift cancels",
            "claim_ceiling": CLAIM_CEILING,
            "runnable": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D827_1",
            "decision": "do not promote local GR",
            "reason": "baseline F_L/L_cg drift and K_hat divergence remain unsourced and can be linear local residuals",
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
            "objective": "either derive local constancy/bounds for X_B and L_cg baseline drift, or derive a parent K_hat owner that cancels/bounds the remaining drift in q_loc",
            "allowed_work": "X_B ancestor theorem attempt, L_cg local constancy bound, K_hat Hilbert-stress response, residual-vector contract",
            "forbidden_work": "local-GR claim, data fitting, C2A closure promotion, hand-set K_hat cancellation",
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
            "what_survived": "F1 zero plus a conditional moving-extremum cancellation of R-sector linear delta_m*nabla X drift",
            "what_failed": "baseline F_L/L_cg drift and K_hat response remain open, so q_loc is not proven zero",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def validation_rows(
    source_rows: list[dict[str, object]],
    drift_rows: list[dict[str, object]],
    khat_rows: list[dict[str, object]],
    residual_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail})

    add(
        "V827_0_sources_exist_and_needles",
        all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows),
        "all source paths exist and needles are present",
    )
    clean_826, clean_826_detail = validation_file_clean(RESIDUALS / "P8_Y5_BRR545_826_VALIDATION.csv")
    add("V827_1_prior_826_clean", clean_826, clean_826_detail)
    add(
        "V827_2_moving_extremum_cancellation_recorded",
        any(row["identity_id"] == "DI827_2_moving_extremum_cancellation" and row["result"] == "linear_memory_X_drift_cancels_conditionally" for row in drift_rows),
        "moving-extremum cancellation recorded",
    )
    add(
        "V827_3_post_F1_residual_recorded",
        any(row["identity_id"] == "DI827_3_post_F1_residual_gradient" for row in drift_rows)
        and any(row["identity_id"] == "DI827_4_projected_q_loc" for row in drift_rows),
        "post-F1 gradient and q_loc residual recorded",
    )
    add(
        "V827_4_Khat_handset_rejected",
        any(row["response_id"] == "KH827_0_no_hand_set_Khat" and row["status"] == "rejected" for row in khat_rows),
        "hand-set Khat cancellation rejected",
    )
    add(
        "V827_5_residual_terms_complete",
        {"Q827_0_baseline_F_L", "Q827_1_Lcg_drift", "Q827_2_quadratic_memory", "Q827_4_Khat_divergence"}.issubset({row["term_id"] for row in residual_rows}),
        "baseline, Lcg, quadratic memory, and Khat terms listed",
    )
    add(
        "V827_6_local_GR_still_blocked",
        any(row["gate_id"] == "G827_2_baseline_drift" and row["result"] == "fail_open" for row in gates)
        and any(row["gate_id"] == "G827_3_Khat_owner" and row["result"] == "fail_open" for row in gates),
        "baseline drift and Khat owner gates fail open",
    )
    add(
        "V827_7_decision_nonrunnable",
        all(row["runnable"] == "false" for row in decisions),
        "branch remains non-runnable",
    )
    add(
        "V827_8_next_target_selected",
        any(row["next_target"] == NEXT_TARGET for row in next_rows),
        NEXT_TARGET,
    )
    all_rows = source_rows + drift_rows + khat_rows + residual_rows + gates + decisions + next_rows + summary
    add(
        "V827_9_all_rows_nonclaim",
        all(row.get("valid_for_claim") == "false" for row in all_rows),
        "all generated rows valid_for_claim=false",
    )
    add(
        "V827_10_no_data_or_local_GR_claim",
        all("data fitting" in row["forbidden_work"] and "local-GR claim" in row["forbidden_work"] for row in next_rows),
        "no data or local-GR claim selected",
    )
    changed = formalization_workbench_modified_count()
    add(
        "V827_11_formalization_workbench_untouched",
        changed == 0,
        f"formalization_changed_after_cutoff={changed}",
    )
    add("V827_12_validation_rows_ready", True, "validation table constructed")
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
    drift_rows: list[dict[str, object]],
    khat_rows: list[dict[str, object]],
    residual_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    summary: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> str:
    return "\n\n".join(
        [
            "# 827 - Y5 R10 X_B Drift And Khat Bound After F1 Zero",
            (
                "Current result: **one more linear channel cancels conditionally**. If the local state `m_L(X_B)` is the moving extremum of the same parent potential `R`, then differentiating `R_m(m_L(X_B),X_B)=0` cancels the `delta_m * grad X_B` drift from the `R` sector. "
                "But this does not prove local GR: baseline `F_L/L_cg` drift and the parent `K_hat` response remain unsolved."
            ),
            f"Generated UTC: `{generated_utc}`",
            "## Nonclaim Summary\n\n" + markdown_table(summary, ["status", "claim_ceiling", "what_survived", "what_failed", "next_target", "valid_for_claim"]),
            "## Drift Identity\n\n" + markdown_table(drift_rows, ["identity_id", "statement", "derivation", "result", "remaining_blocker", "valid_for_claim"]),
            "## Khat Response Contract\n\n" + markdown_table(khat_rows, ["response_id", "candidate", "status", "reason", "needed_next", "valid_for_claim"]),
            "## q_loc Residual Contract\n\n" + markdown_table(residual_rows, ["term_id", "residual_term", "status", "safe_if", "claim_risk", "valid_for_claim"]),
            "## Local GR Gate\n\n" + markdown_table(gates, ["gate_id", "gate", "result", "consequence", "valid_for_claim"]),
            "## Decision\n\n" + markdown_table(decisions, ["decision_id", "decision", "reason", "claim_ceiling", "runnable", "next_target", "valid_for_claim"]),
            "## Next Target\n\n" + markdown_table(next_rows, ["next_target", "objective", "allowed_work", "forbidden_work", "valid_for_claim"]),
            "## Source Register\n\n" + markdown_table(source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"]),
            "## Validation\n\n" + markdown_table(validation, ["check_id", "result", "detail"]),
            "## Verdict\n\n"
            "This is a proper derivation gain, not decoration: the moving-extremum condition kills a term that otherwise looked dangerous. "
            "The theory still has to beat the baseline drift/Khat problem. The next checkpoint should either prove local constancy for `X_B` and `L_cg`, or derive the parent `K_hat` owner that carries those gradients without creating a PPN residual.",
        ]
    )


def main() -> None:
    generated_utc = datetime.now(timezone.utc).isoformat(timespec="seconds")

    source_rows = source_register_rows(generated_utc)
    drift_rows = drift_identity_rows(generated_utc)
    khat_rows = khat_response_rows(generated_utc)
    residual_rows = residual_contract_rows(generated_utc)
    gates = gate_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    next_rows = next_target_rows(generated_utc)
    summary = nonclaim_summary_rows(generated_utc)
    validation = validation_rows(source_rows, drift_rows, khat_rows, residual_rows, gates, decisions, next_rows, summary)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(DRIFT_IDENTITY_PATH, drift_rows, ["identity_id", "statement", "derivation", "result", "remaining_blocker", "valid_for_claim", "generated_utc"])
    write_csv(KHAT_RESPONSE_PATH, khat_rows, ["response_id", "candidate", "status", "reason", "needed_next", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUAL_CONTRACT_PATH, residual_rows, ["term_id", "residual_term", "status", "safe_if", "claim_risk", "valid_for_claim", "generated_utc"])
    write_csv(GATE_PATH, gates, ["gate_id", "gate", "result", "consequence", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "reason", "claim_ceiling", "runnable", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_rows, ["next_target", "objective", "allowed_work", "forbidden_work", "priority", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "what_survived", "what_failed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])

    OUTPUT_DOC.write_text(
        render_document(generated_utc, source_rows, drift_rows, khat_rows, residual_rows, gates, decisions, next_rows, summary, validation),
        encoding="utf-8",
    )

    failed = [row for row in validation if row["result"] != "pass"]
    if failed:
        details = "; ".join(f"{row['check_id']}={row['detail']}" for row in failed)
        raise SystemExit(f"827 validation failed: {details}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")


if __name__ == "__main__":
    main()

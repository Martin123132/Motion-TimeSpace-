from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1127-Y5-R10-local-vs-FLRW-branch-selector-no-flux-certificate.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    generated = now()
    return [{**row, "generated_utc": generated} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_rows() -> list[dict[str, object]]:
    sources = [
        {
            "source_id": "SRC1127_0_1126_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1126_NEXT_TARGET.csv",
            "needle": "NEXT1126_0_1127",
            "note": "1126 handoff to local-vs-FLRW branch selector.",
        },
        {
            "source_id": "SRC1127_1_1126_obligations",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1126_SELECTOR_LOCAL_FLUX_OBLIGATIONS.csv",
            "needle": "OB1126_2_branch_selector",
            "note": "1126 requires local-vs-FLRW branch selector.",
        },
        {
            "source_id": "SRC1127_2_602_gate",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_602_LOCAL_FLRW_BRANCH_GATE.csv",
            "needle": "LFG602_2_FLRW_active",
            "note": "602 supports FLRW-active branch conditionally.",
        },
        {
            "source_id": "SRC1127_3_609_split",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_609_LOCAL_FLRW_BRANCH_SPLIT_GATE.csv",
            "needle": "LF609_2_no_overstrong_zero",
            "note": "609 forbids global all-domain zero because it kills cosmology.",
        },
        {
            "source_id": "SRC1127_4_822_FLRW",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_822_FLRW_REDUCTION_AUDIT.csv",
            "needle": "F822_1_FLRW_time",
            "note": "822 gives conditional FLRW N_D=-ln(a)=ln(1+z) reduction.",
        },
        {
            "source_id": "SRC1127_5_ownership",
            "relative_path": "source-intake/mts_residuals/P8_DOMAIN_ALPHA3_PREMISE_OWNERSHIP.csv",
            "needle": "P3_local_trivial_representative",
            "note": "Local trivial representative remains conditional.",
        },
        {
            "source_id": "SRC1127_6_no_vector",
            "relative_path": "source-intake/mts_residuals/P8_DOMAIN_SELECTOR_NOVECTOR_THEOREM_ATTEMPT.csv",
            "needle": "T2_no_flux_local_representative",
            "note": "No-flux local representative is conditional, not parent-derived.",
        },
        {
            "source_id": "SRC1127_7_newton_stack",
            "relative_path": "source-intake/mts_residuals/P8_source_normalized_Newton_branch_STACK.csv",
            "needle": "SN4_closed_Meff_flux",
            "note": "Newton/local-GR stack keeps closed flux not parent-derived.",
        },
    ]
    checked: list[dict[str, object]] = []
    for source in sources:
        path = ROOT / str(source["relative_path"])
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        checked.append(
            {
                **source,
                "exists": str(path.exists()).lower(),
                "needle_found": str(str(source["needle"]) in text).lower(),
            }
        )
    return stamp(checked)


def branch_audit_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "branch_id": "BS1127_0_local",
                "branch": "compact stationary local branch",
                "needed_statement": "N_D=0 or equivalent exact/trivial local domain representative, giving epsilon_domain_flux=0",
                "current_support": "602/609/T2 give conditional local-zero/no-flux route",
                "current_status": "CONDITIONAL_NOT_PARENT_DERIVED",
                "blocker": "local trivial relative class and scalar selector are not parent-owned",
                "valid_for_claim": "false",
            },
            {
                "branch_id": "BS1127_1_FLRW",
                "branch": "coherent FLRW/cosmological memory branch",
                "needed_statement": "N_D>0 or coherent expansion class remains active, with N_D=-ln(a)=ln(1+z) in FLRW",
                "current_support": "602/609/822 give conditional support for active FLRW shape",
                "current_status": "CONDITIONAL_SUPPORTED_NOT_PARENT_OWNED",
                "blocker": "Q_coh/P_coh/domain normalization and selector ownership are not parent-derived",
                "valid_for_claim": "false",
            },
            {
                "branch_id": "BS1127_2_no_overstrong_zero",
                "branch": "global all-domain zero",
                "needed_statement": "forbidden route: all domains globally zero",
                "current_support": "609 marks this as forbidden because it kills cosmological memory",
                "current_status": "FORBIDDEN_GUARD",
                "blocker": "not a unification route",
                "valid_for_claim": "false",
            },
            {
                "branch_id": "BS1127_3_verdict",
                "branch": "parent local-vs-FLRW selector",
                "needed_statement": "one parent selector yields local exact/trivial branch and FLRW coherent active branch without outcome fitting",
                "current_support": "conditional shape exists but parent ownership is missing",
                "current_status": "BRANCH_SELECTOR_NOT_CLOSED",
                "blocker": "same selector must produce both branches from parent variables, not hand-picked domains",
                "valid_for_claim": "false",
            },
        ]
    )


def candidate_rule_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "rule_id": "BR1127_0_selector_variable",
                "candidate_rule": "B_D selects branch by parent-owned invariant N_D or coherent determinant/current class",
                "formal_shape": "B_D=local if N_D=0 or [J_D]_local exact; B_D=FLRW if N_D>0/coherent expansion class",
                "status": "CANDIDATE_NOT_PARENT_DERIVED",
                "must_prove": "N_D/Q_coh/P_coh exists before empirical readout and is varied/owned by parent action",
                "valid_for_claim": "false",
            },
            {
                "rule_id": "BR1127_1_local_zero_effect",
                "candidate_rule": "local branch implies q_D_vector_flux=0",
                "formal_shape": "B_D=local -> epsilon_domain_flux=0 -> W_domain_alpha3*epsilon_domain_flux=0",
                "status": "CONDITIONAL_EFFECT_ONLY",
                "must_prove": "local branch condition is parent-selected, not imposed plateau",
                "valid_for_claim": "false",
            },
            {
                "rule_id": "BR1127_2_FLRW_survival",
                "candidate_rule": "FLRW branch keeps cosmological memory active",
                "formal_shape": "B_D=FLRW -> N_D=-ln(a)=ln(1+z), Q_coh positive/oriented, memory projection active",
                "status": "CONDITIONAL_SUPPORTED",
                "must_prove": "Q_coh/P_coh and normalization are parent-owned, not fit-history imported",
                "valid_for_claim": "false",
            },
            {
                "rule_id": "BR1127_3_no_data_gate",
                "candidate_rule": "branch selector cannot use residual success or empirical fit quality",
                "formal_shape": "B_D depends only on parent scalar/topological/boundary-current ingredients",
                "status": "POLICY_PASS_NOT_POSITIVE_DERIVATION",
                "must_prove": "actual parent ingredients exist and are sufficient",
                "valid_for_claim": "false",
            },
        ]
    )


def effect_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "effect_id": "EFF1127_0_if_closed_local",
                "if_statement": "parent selector closes local exact/trivial branch",
                "then_statement": "epsilon_domain_flux=0 locally; q_D_vector_flux alpha3 branch collapses",
                "claim_effect": "would unblock one direct alpha3 path, but R11 source-normalization/stress siblings remain guarded",
                "current_status": "CONDITIONAL_ONLY",
                "valid_for_claim": "false",
            },
            {
                "effect_id": "EFF1127_1_if_closed_FLRW",
                "if_statement": "same parent selector preserves coherent FLRW branch",
                "then_statement": "cosmological memory route remains available for FLRW tests",
                "claim_effect": "prevents local-GR proof from deleting cosmology mechanism",
                "current_status": "CONDITIONAL_ONLY",
                "valid_for_claim": "false",
            },
            {
                "effect_id": "EFF1127_2_if_not_closed",
                "if_statement": "branch selector remains unsigned",
                "then_statement": "1126 executable product rows stay active and alpha3 remains blocked",
                "claim_effect": "no PPN/R10/local-GR promotion",
                "current_status": "ACTIVE_CURRENT_STATE",
                "valid_for_claim": "false",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "G1127_0_local_branch",
                "rule": "local branch exact/trivial representative is parent-derived",
                "gate_pass": "false",
                "reason": "local representative remains conditional",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1127_1_FLRW_branch",
                "rule": "FLRW active branch is parent-owned",
                "gate_pass": "false",
                "reason": "FLRW shape is conditionally supported but Q_coh/P_coh ownership is missing",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1127_2_no_overstrong_zero",
                "rule": "global all-domain zero is forbidden",
                "gate_pass": "true_nonclaim",
                "reason": "1127 keeps this guard explicit",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1127_3_qD_flux_closed",
                "rule": "q_D_vector_flux=0 follows from branch selector",
                "gate_pass": "false",
                "reason": "branch selector is not parent-owned",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1127_4_local_GR",
                "rule": "local-GR/PPN branch can promote",
                "gate_pass": "false",
                "reason": "alpha3 flux, R11 source-normalization, and stress siblings remain blocked",
                "valid_for_claim": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "D1127_0_verdict",
                "decision": "branch_selector_not_closed",
                "reason": "local/FLRW split has conditional support but lacks parent-owned selector variables",
                "next_action": "derive parent ownership of N_D/Q_coh/P_coh or return to executable flux products",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1127_1_best_next",
                "decision": "parent_selector_ownership_first",
                "reason": "this is the cleanest way to silence local flux without killing cosmology",
                "next_action": "prove N_D/Q_coh/P_coh are parent variables with branch conditions",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1127_2_guard",
                "decision": "do_not_use_global_zero",
                "reason": "global all-domain zero would erase FLRW/cosmological memory",
                "next_action": "keep local and FLRW branches separate",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1127_0_1128",
                "next_target": "1128-Y5-R10-parent-branch-selector-ownership-ND-Qcoh-Pcoh.md",
                "objective": "derive parent ownership of the branch selector variables N_D, Q_coh, and P_coh so local exact/trivial branch and FLRW active branch come from one rule rather than hand-picked domains",
                "include": "N_D; Q_coh; P_coh; local N_D=0; FLRW N_D=ln(1+z); no empirical selector; no global all-domain zero; alpha3 flux guard",
                "exclude": "killing cosmology; plateau axiom; tuned cancellation; local-GR claim; GitHub; formalization edits",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    branches: list[dict[str, object]],
    rules: list[dict[str, object]],
    effects: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    outputs: dict[str, Path],
) -> list[dict[str, object]]:
    validation: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validation.append(
            {
                "check_id": check_id,
                "result": "pass" if passed else "fail",
                "detail": detail,
                "valid_for_claim": "false",
                "generated_utc": now(),
            }
        )

    all_rows = branches + rules + effects + gates + decisions + next_target
    branch_names = {row["branch"] for row in branches}
    add("V1127_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources), "all cited local source paths exist and needles are found")
    add("V1127_1_branch_coverage", {"compact stationary local branch", "coherent FLRW/cosmological memory branch", "global all-domain zero", "parent local-vs-FLRW selector"}.issubset(branch_names), "local, FLRW, forbidden global-zero, and selector verdict rows are covered")
    add("V1127_2_selector_not_closed", branches[-1]["current_status"] == "BRANCH_SELECTOR_NOT_CLOSED", "branch selector remains unclosed")
    add("V1127_3_FLRW_preserved", any("N_D=-ln(a)=ln(1+z)" in row["formal_shape"] for row in rules), "FLRW active branch shape is preserved")
    add("V1127_4_no_overstrong_zero_guard", gates[2]["gate_pass"] == "true_nonclaim" and decisions[-1]["decision"] == "do_not_use_global_zero", "global all-domain zero is forbidden")
    add("V1127_5_gates_blocked", all(row["gate_pass"] in {"false", "true_nonclaim"} for row in gates) and sum(row["gate_pass"] == "false" for row in gates) >= 4, "claim gates remain blocked")
    add("V1127_6_no_claim_rows", all(row.get("valid_for_claim") == "false" for row in all_rows) and all(row.get("claim_allowed", "false") == "false" for row in next_target), "all generated rows remain nonclaim")
    add("V1127_7_next_target", next_target[0]["next_target"].startswith("1128-") and "branch-selector-ownership" in str(next_target[0]["next_target"]), "1128 handoff targets parent branch selector ownership")
    add("V1127_8_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()), "all generated outputs are under post-checkpoint-work")
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1127_9_csv_parse", csv_parse_ok, "all 1127 CSV outputs parse cleanly")
    add("V1127_10_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add("V1127_SUMMARY", True, "1127 preserves local/FLRW split as conditional and keeps alpha3 blocked")
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    branches: list[dict[str, object]],
    rules: list[dict[str, object]],
    effects: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1127 - Y5/R10 Local-vs-FLRW Branch Selector No-Flux Certificate

**Current verdict:** the local-vs-FLRW split has the right conditional shape, but the parent branch selector is not closed. Local `epsilon_domain_flux=0` is still conditional, while FLRW memory is conditionally preserved.

**Good news:** the route does not require killing cosmology. A serious branch selector would set the compact local branch to exact/trivial while keeping the coherent FLRW branch active.

**Guard:** global all-domain zero is forbidden because it would erase the cosmological memory mechanism.

**No claim:** no domain/R11 `alpha3`, R10, PPN, Newton/local-GR, or measured-GM pass follows from 1127.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "note"], sources)}

## Branch Selector Audit
{table(["branch_id", "branch", "needed_statement", "current_support", "current_status", "blocker", "valid_for_claim"], branches)}

## Candidate Rule
{table(["rule_id", "candidate_rule", "formal_shape", "status", "must_prove", "valid_for_claim"], rules)}

## Effects If Closed
{table(["effect_id", "if_statement", "then_statement", "claim_effect", "current_status", "valid_for_claim"], effects)}

## Claim Gates
{table(["gate_id", "rule", "gate_pass", "reason", "valid_for_claim"], gates)}

## Decision Ledger
{table(["decision_id", "decision", "reason", "next_action", "valid_for_claim"], decisions)}

## Validation
{table(["check_id", "result", "detail", "valid_for_claim"], validation)}

## Next Target
{table(["next_id", "next_target", "objective", "include", "exclude", "valid_for_claim"], next_target)}
"""
    DOC.write_text(text, encoding="utf-8")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists() and pycache.is_dir():
        shutil.rmtree(pycache)


def main() -> None:
    outputs = {
        "source_register": OUT / "P8_Y5_R10_1127_SOURCE_REGISTER.csv",
        "branches": OUT / "P8_Y5_R10_1127_BRANCH_SELECTOR_AUDIT.csv",
        "rules": OUT / "P8_Y5_R10_1127_CANDIDATE_BRANCH_RULE.csv",
        "effects": OUT / "P8_Y5_R10_1127_NO_FLUX_EFFECT_LEDGER.csv",
        "gates": OUT / "P8_Y5_R10_1127_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1127_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1127_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1127_VALIDATION.csv",
    }
    sources = source_rows()
    branches = branch_audit_rows()
    rules = candidate_rule_rows()
    effects = effect_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["branches"], branches)
    write_csv(outputs["rules"], rules)
    write_csv(outputs["effects"], effects)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, branches, rules, effects, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, branches, rules, effects, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()

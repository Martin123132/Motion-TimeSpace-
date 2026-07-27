from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work"
)
OUT = ROOT / "source-intake" / "mts_residuals"
SCRIPT_PATH = ROOT / "scripts" / "Y5_R10_ultra_screened_alpha_branch_cross_arena_contract.py"
DOC_PATH = ROOT / "650-Y5-R10-ultra-screened-alpha-branch-cross-arena-contract.md"

STATUS = "Y5_R10_ultra_screened_alpha_branch_cross_arena_contract_formalized_nonclaim"
CLAIM_CEILING = "cross_arena_screening_contract_only_no_clock_WEP_R10_EM_or_PPN_claim"
NEXT_TARGET = "651-Y5-R10-WEP-alpha-sensitivity-source-fill-or-screening-stress-test.md"
NOMINAL_H0_YR_INV = 7.16e-11
YB_PRODUCT_BOUND_1SIGMA_YR_INV = 2.1e-18
SCREEN_BOUND_FOR_KAPPA_ONE = YB_PRODUCT_BOUND_1SIGMA_YR_INV / NOMINAL_H0_YR_INV


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def source_register_rows() -> list[dict[str, object]]:
    sources = [
        ("S650_0", "checkpoint_649_doc", ROOT / "649-Y5-R10-local-chiX-silence-theorem-or-ultra-screened-alpha-branch.md", "prior local silence / ultra-screen fork"),
        ("S650_1", "validation_649", OUT / "P8_Y5_BRR545_649_VALIDATION.csv", "prior validation"),
        ("S650_2", "ultra_screen_branch_649", OUT / "P8_Y5_R10_649_ULTRA_SCREENED_ALPHA_BRANCH.csv", "screening pressure imported from Yb clock product bound"),
        ("S650_3", "branch_policy_649", OUT / "P8_Y5_R10_649_BRANCH_POLICY.csv", "no clock-only special pleading warning"),
        ("S650_4", "silence_clause_audit_649", OUT / "P8_Y5_R10_649_SILENCE_CLAUSE_AUDIT.csv", "unsigned local silence clauses"),
        ("S650_5", "cross_arena_matrix_641", OUT / "P8_Y5_R10_641_CROSS_ARENA_REACTION_MATRIX.csv", "prior alpha reaction matrix"),
        ("S650_6", "bound_input_ledger_645", OUT / "P8_Y5_R10_645_BOUND_INPUT_LEDGER.csv", "local arena bound input ledger"),
        ("S650_7", "local_bound_matrix_639", OUT / "P8_Y5_R10_639_LOCAL_BOUND_MATRIX.csv", "WEP/R10/PPN/Gdot local bound matrix"),
        ("S650_8", "clock_alpha_source_646", OUT / "P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv", "source-backed clock alpha sensitivities"),
        ("S650_9", "clock_product_bound_647", OUT / "P8_Y5_R10_647_CLOCK_PRODUCT_BOUND.csv", "clock product bound owner"),
        ("S650_10", "generator_script_650", SCRIPT_PATH, "this checkpoint generator"),
    ]
    return [
        {
            "source_id": source_id,
            "label": label,
            "path": rel(path),
            "exists": bool_text(path.exists()),
            "role": role,
            "valid_for_claim": "false",
        }
        for source_id, label, path, role in sources
    ]


def ultra_screened_rule_rows() -> list[dict[str, object]]:
    return [
        {
            "rule_id": "USR650_0_shared_screen_variable",
            "screen_variable": "S_lab_alpha = |dchi_X/dN|_lab",
            "source_bound_owner": "Yb+ E3/E2 clock product row via 649 USB649_2",
            "formula": "|kappa_alpha| * S_lab_alpha <= 2.933e-08",
            "kappa_one_bound": f"{SCREEN_BOUND_FOR_KAPPA_ONE:.6e}",
            "scope": "all local alpha-sensitive arenas unless a parent-signed local silence theorem replaces it",
            "status": "cross_arena_contract_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "rule_id": "USR650_1_no_clock_only_screen",
            "screen_variable": "S_lab_alpha",
            "source_bound_owner": "branch policy BP649_3",
            "formula": "same S_lab_alpha must be used in clocks, WEP, R10, and local EM projections",
            "kappa_one_bound": f"{SCREEN_BOUND_FOR_KAPPA_ONE:.6e}",
            "scope": "forbids hiding alpha drift only in clock experiments",
            "status": "no_special_pleading_gate",
            "valid_for_claim": "false",
        },
        {
            "rule_id": "USR650_2_domain_classifier_required",
            "screen_variable": "D_parent(domain)",
            "source_bound_owner": "silence clause LCS649_0",
            "formula": "lab/bound screening and FLRW/galaxy unscreened behaviour require a parent-derived domain classifier",
            "kappa_one_bound": "not_a_numeric_bound",
            "scope": "prevents post-hoc lab-versus-cosmology toggles",
            "status": "missing_parent_derivation",
            "valid_for_claim": "false",
        },
    ]


def cross_arena_contract_rows() -> list[dict[str, object]]:
    return [
        {
            "arena_id": "R2_clocks",
            "arena": "atomic clocks and alpha drift",
            "bound_owner": "Yb+ E3/E2 product bound",
            "shared_screen_variable": "S_lab_alpha",
            "required_projection": "delta_nu_ab/nu_ab = (K_a_alpha-K_b_alpha) kappa_alpha H0 S_lab_alpha",
            "imported_bound_or_status": "|kappa_alpha*S_lab_alpha| <= 2.933e-08 H0-normalized",
            "cross_arena_rule": "sets the maximum local alpha screen used by every other local alpha arena",
            "current_status": "bounded_product_not_standalone_pass",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "arena_id": "R0_R1_WEP",
            "arena": "MICROSCOPE/Eotvos composition dependence",
            "bound_owner": "eta_AB <= 2.8e-15 ledger row",
            "shared_screen_variable": "S_lab_alpha",
            "required_projection": "eta_AB = beta_source tau_WEP sum_i[(S_Ai-S_Bi) kappa_i], with alpha channel tied to S_lab_alpha if it survives locally",
            "imported_bound_or_status": "numeric bound exists but alpha composition sensitivities and beta_source are missing",
            "cross_arena_rule": "WEP cannot use a weaker or different screening map than clocks",
            "current_status": "projection_missing_blocks_score",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "arena_id": "R10_short_range",
            "arena": "short-range fifth force / alpha(lambda)",
            "bound_owner": "R10 bound ledger / alpha(lambda) source slot",
            "shared_screen_variable": "S_lab_alpha",
            "required_projection": "alpha_R10(lambda)=tau_R10(lambda) beta_source beta_test c_eff(lambda), with any alpha-channel piece using the same lab screen",
            "imported_bound_or_status": "bound source path exists in ledger; local prediction coefficients remain symbolic",
            "cross_arena_rule": "R10 residuals cannot be declared silent by a separate lambda-only switch",
            "current_status": "prediction_missing_blocks_score",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "arena_id": "EM_spectra",
            "arena": "local and astrophysical EM spectra",
            "bound_owner": "source slot from 645, not yet filled",
            "shared_screen_variable": "S_lab_alpha plus parent domain classifier",
            "required_projection": "delta_alpha/alpha = kappa_alpha Delta chi_X, with lab Delta chi_X obeying S_lab_alpha and nonlocal rows requiring D_parent(domain)",
            "imported_bound_or_status": "no selected source-backed spectra dataset yet",
            "cross_arena_rule": "local spectra share the clock screen; astrophysical/cosmological spectra require parent domain separation",
            "current_status": "source_and_domain_missing_blocks_score",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "arena_id": "PPN_Gdot_orbital",
            "arena": "PPN, Gdot, orbital residuals",
            "bound_owner": "639 local bound matrix",
            "shared_screen_variable": "not_sufficient_by_itself",
            "required_projection": "metric/coframe/source-normalization operators must reduce to GR independently of the alpha screen",
            "imported_bound_or_status": "numeric bounds exist for PPN/Gdot rows but alpha screen does not close metric sector",
            "cross_arena_rule": "screening alpha cannot be used as a fake local-GR derivation",
            "current_status": "separate_GR_reduction_still_required",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def projection_requirement_rows() -> list[dict[str, object]]:
    return [
        {
            "requirement_id": "PR650_0_clocks",
            "arena_id": "R2_clocks",
            "needed_input": "source-backed K_alpha pair and tau_clock_time = H0 S_lab_alpha",
            "current_evidence": "K_alpha and product bound sourced in 646/647",
            "missing_piece": "parent derivation of S_lab_alpha or local silence",
            "acceptance_condition": "either prove tau_clock=0 from parent clauses or keep |kappa_alpha*S_lab_alpha| <= 2.933e-08",
            "status": "numeric_product_only",
            "valid_for_claim": "false",
        },
        {
            "requirement_id": "PR650_1_WEP",
            "arena_id": "R0_R1_WEP",
            "needed_input": "Delta composition sensitivities, source normalization beta_source, tau_WEP, and material map",
            "current_evidence": "MICROSCOPE bound row exists in 639/645",
            "missing_piece": "alpha-dependent body sensitivities and parent source normalization",
            "acceptance_condition": "WEP prediction uses same S_lab_alpha and does not invent a new arena-specific screen",
            "status": "blocked_missing_projection",
            "valid_for_claim": "false",
        },
        {
            "requirement_id": "PR650_2_R10",
            "arena_id": "R10_short_range",
            "needed_input": "alpha(lambda) curve, tau_R10(lambda), beta_source, beta_test, Z_eff, and c_eff(lambda)",
            "current_evidence": "R10 source slot exists; prior real-bound acquisition was nonclaim",
            "missing_piece": "numeric parent prediction and full sourced bound curve",
            "acceptance_condition": "R10 prediction obeys same lab screening if it contains the alpha channel",
            "status": "blocked_missing_projection",
            "valid_for_claim": "false",
        },
        {
            "requirement_id": "PR650_3_EM_spectra",
            "arena_id": "EM_spectra",
            "needed_input": "chosen spectra dataset, alpha sensitivity coefficients, Delta chi_X map, and domain labels",
            "current_evidence": "source slot only",
            "missing_piece": "source-backed EM spectra rows plus parent domain classifier",
            "acceptance_condition": "local spectra share S_lab_alpha; nonlocal spectra use a pre-declared D_parent(domain)",
            "status": "blocked_missing_source_and_domain",
            "valid_for_claim": "false",
        },
        {
            "requirement_id": "PR650_4_PPN",
            "arena_id": "PPN_Gdot_orbital",
            "needed_input": "metric-sector operator coefficients, coframe descent, source normalization, and observed-G map",
            "current_evidence": "numeric local bounds exist in 639",
            "missing_piece": "derived GR/local PPN branch",
            "acceptance_condition": "metric residuals are separately suppressed or derived; alpha screening alone is not accepted",
            "status": "blocked_separate_GR_reduction",
            "valid_for_claim": "false",
        },
    ]


def no_special_pleading_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "NG650_0_same_screen_variable",
            "gate": "same S_lab_alpha is used in clocks, WEP, R10, and local EM",
            "result": "pass_contract_written",
            "consequence": "future rows that use arena-specific alpha screens fail validation",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "NG650_1_no_clock_only_silence",
            "gate": "clock-only silence or screen is forbidden",
            "result": "pass_policy",
            "consequence": "the branch must survive cross-arena, not just clocks",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "NG650_2_parent_domain_classifier",
            "gate": "lab/bound versus FLRW/galaxy domain classifier is parent-derived before fitting data",
            "result": "fail_missing",
            "consequence": "screened lab plus unscreened cosmology remains a contract, not a claim",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "NG650_3_WEP_R10_EM_projection",
            "gate": "WEP, R10, and EM spectra have numeric projections using the shared screen",
            "result": "fail_missing",
            "consequence": "no local-alpha evidence score is allowed",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "NG650_4_PPN_not_fixed_by_alpha",
            "gate": "metric/PPN residuals are not repaired by alpha screening alone",
            "result": "pass_blocker",
            "consequence": "local GR reduction stays a separate derivation target",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "NG650_5_public_claim",
            "gate": "public local alpha or local GR pass claim",
            "result": "fail_policy",
            "consequence": "private robustness contract only",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D650_0",
            "route": "ultra_screened_alpha_branch",
            "decision": "retained_as_cross_arena_contract_only",
            "why": "it is the only finite-alpha survival path after clocks, but it must now face WEP/R10/EM with the same screen",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D650_1",
            "route": "local_chiX_silence_theorem",
            "decision": "kept_dormant_not_claimed",
            "why": "six local silence clauses are still parent-unsigned",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D650_2",
            "route": "next_arena",
            "decision": "select_WEP_stress_test_first",
            "why": "WEP is the next hardest local alpha-sensitive arena with a strong numeric bound and no range-curve ambiguity",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def next_contract_rows() -> list[dict[str, object]]:
    return [
        {
            "contract_id": "NC650_0",
            "next_target": NEXT_TARGET,
            "work_item": "Fill WEP alpha-sensitivity/source-normalization rows or prove the shared screen kills the WEP alpha channel.",
            "acceptance_condition": "eta_AB row uses S_lab_alpha and source-backed material sensitivities; otherwise remains blocked",
        },
        {
            "contract_id": "NC650_1",
            "next_target": NEXT_TARGET,
            "work_item": "Reject any arena-specific screening factor not derived from the parent domain classifier.",
            "acceptance_condition": "future runner fails rows with S_clock != S_WEP != S_R10 != S_EM unless parent-sourced",
        },
        {
            "contract_id": "NC650_2",
            "next_target": NEXT_TARGET,
            "work_item": "Keep PPN/local GR reduction separate from alpha screening.",
            "acceptance_condition": "metric/coframe residuals require their own zero or bound proof",
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "same_screen_variable_required": "true",
            "screen_variable": "S_lab_alpha=|dchi_X/dN|_lab",
            "kappa_one_screen_bound": f"{SCREEN_BOUND_FOR_KAPPA_ONE:.3e}",
            "clock_only_escape_allowed": "false",
            "WEP_ready": "false",
            "R10_ready": "false",
            "EM_spectra_ready": "false",
            "PPN_local_GR_ready": "false",
            "hardest_blocker": "parent domain classifier plus WEP/R10/EM projection coefficients are missing",
            "next_target": NEXT_TARGET,
        }
    ]


def validation_rows(
    source_rows: list[dict[str, object]],
    rule_rows: list[dict[str, object]],
    contract_rows: list[dict[str, object]],
    projection_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decision: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V650_0_source_paths_exist", all(row["exists"] == "true" for row in source_rows), "all cited local source paths exist"))
    prior = read_csv(OUT / "P8_Y5_BRR545_649_VALIDATION.csv")
    checks.append(("V650_1_prior_649_validation_clean", all(row.get("result") == "pass" for row in prior), "649 validation remains clean"))
    usb = read_csv(OUT / "P8_Y5_R10_649_ULTRA_SCREENED_ALPHA_BRANCH.csv")
    kappa_one = [row for row in usb if row.get("assumed_abs_kappa_alpha") == "1"]
    checks.append(("V650_2_kappa_one_screen_imported", len(kappa_one) == 1 and float(kappa_one[0]["required_abs_dchi_dN_over_H0_max"]) < 3e-8, "kappa=1 screen imported from 649 and remains below 3e-8"))
    checks.append(("V650_3_shared_screen_defined", any(row["screen_variable"] == "S_lab_alpha = |dchi_X/dN|_lab" for row in rule_rows), "shared lab alpha screen is explicit"))
    required_arenas = {"R2_clocks", "R0_R1_WEP", "R10_short_range", "EM_spectra", "PPN_Gdot_orbital"}
    contract_arenas = {row["arena_id"] for row in contract_rows}
    checks.append(("V650_4_required_arenas_covered", required_arenas.issubset(contract_arenas), "clock, WEP, R10, EM, and PPN/orbital arenas are covered"))
    checks.append(("V650_5_contract_rows_nonclaim", all(row["valid_for_claim"] == "false" and row["score_ready"] == "false" for row in contract_rows), "all cross-arena rows remain nonclaim and unscored"))
    blocked_statuses = {row["status"] for row in projection_rows}
    checks.append(("V650_6_projection_blocks_present", any("blocked" in status for status in blocked_statuses), "missing WEP/R10/EM/PPN projections are explicit blockers"))
    checks.append(("V650_7_no_special_pleading_gates_present", len(gate_rows) >= 5 and any(row["gate_id"] == "NG650_1_no_clock_only_silence" for row in gate_rows), "no-special-pleading gates are present"))
    checks.append(("V650_8_domain_classifier_still_missing", any(row["gate_id"] == "NG650_2_parent_domain_classifier" and row["result"] == "fail_missing" for row in gate_rows), "parent domain classifier remains missing"))
    checks.append(("V650_9_public_claim_blocked", any(row["gate_id"] == "NG650_5_public_claim" and row["result"] == "fail_policy" for row in gate_rows), "public claim gate is blocked"))
    checks.append(("V650_10_decisions_nonclaim", all(row["valid_for_claim"] == "false" for row in decision), "decision rows are nonclaim"))
    checks.append(("V650_11_next_target_WEP", all(row["next_target"] == NEXT_TARGET for row in next_rows) and "WEP" in NEXT_TARGET, "next target selects WEP screening stress test"))
    checks.append(("V650_12_summary_blocks_claim", summary[0]["clock_only_escape_allowed"] == "false" and summary[0]["WEP_ready"] == "false", "summary blocks clock-only escape and WEP claim"))

    fw = ROOT.parent / "formalization-workbench"
    cutoff = datetime(2026, 5, 31, 14, 42, 0).timestamp()
    changed_after_cutoff = 0
    if fw.exists():
        for path in fw.rglob("*"):
            if path.is_file() and path.stat().st_mtime > cutoff:
                changed_after_cutoff += 1
    checks.append(("V650_13_formalization_workbench_unchanged", changed_after_cutoff == 0, f"formalization files changed after cutoff: {changed_after_cutoff}"))

    return [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "generated_utc": now_iso(),
        }
        for check_id, passed, detail in checks
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            text = str(row.get(column, "")).replace("|", "\\|").replace("\n", " ")
            values.append(text)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    source_rows: list[dict[str, object]],
    rule_rows: list[dict[str, object]],
    contract_rows: list[dict[str, object]],
    projection_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decision: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    summary: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    lines = [
        "# 650 Y5/R10 Ultra-Screened Alpha Branch Cross-Arena Contract",
        "",
        "## Verdict",
        "",
        f"- Status: `{STATUS}`",
        f"- Claim ceiling: `{CLAIM_CEILING}`",
        "- The finite-alpha branch survives only if the same local screening variable is used across clocks, WEP, R10, and local EM.",
        "- This forbids a clock-only escape hatch: if `S_lab_alpha` is tiny for clocks, it must be tiny for every local alpha-sensitive arena unless the parent action derives a domain-specific exception.",
        f"- For `|kappa_alpha|=1`, the imported Yb clock product bound requires `S_lab_alpha <= {SCREEN_BOUND_FOR_KAPPA_ONE:.3e}`.",
        "- PPN/local-GR reduction is not solved by alpha screening and remains a separate derivation target.",
        "",
        "## Source Register",
        "",
        markdown_table(source_rows, ["source_id", "label", "path", "exists", "role"]),
        "",
        "## Ultra-Screened Rule",
        "",
        markdown_table(rule_rows, ["rule_id", "screen_variable", "source_bound_owner", "formula", "scope", "status"]),
        "",
        "## Cross-Arena Contract",
        "",
        markdown_table(contract_rows, ["arena_id", "arena", "bound_owner", "shared_screen_variable", "required_projection", "current_status", "score_ready"]),
        "",
        "## Projection Requirements",
        "",
        markdown_table(projection_rows, ["requirement_id", "arena_id", "needed_input", "missing_piece", "acceptance_condition", "status"]),
        "",
        "## No-Special-Pleading Gates",
        "",
        markdown_table(gate_rows, ["gate_id", "gate", "result", "consequence"]),
        "",
        "## Decision",
        "",
        markdown_table(decision, ["decision_id", "route", "decision", "why", "next_target"]),
        "",
        "## Next Contract",
        "",
        markdown_table(next_rows, ["contract_id", "work_item", "acceptance_condition"]),
        "",
        "## Validation",
        "",
        markdown_table(validation, ["check_id", "result", "detail"]),
        "",
        "## Interpretation",
        "",
        "- This is the right ruthless move: the alpha branch is allowed to live, but it must fight the whole local-card table, not just clocks.",
        "- The best next punch is WEP because it is local, numerically sharp, and does not need an R10 range-curve digitization before it can hurt us.",
        "- If WEP also accepts the same screen without special pleading, the branch looks disciplined; if it needs a different screen, the finite-alpha route likely collapses back to a closure-only theorem.",
        "",
        "## Nonclaim Summary",
        "",
        markdown_table(summary, ["status", "same_screen_variable_required", "screen_variable", "kappa_one_screen_bound", "clock_only_escape_allowed", "WEP_ready", "R10_ready", "EM_spectra_ready", "PPN_local_GR_ready", "hardest_blocker", "next_target"]),
        "",
    ]
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source_rows = source_register_rows()
    rule_rows = ultra_screened_rule_rows()
    contract_rows = cross_arena_contract_rows()
    projection_rows = projection_requirement_rows()
    gate_rows = no_special_pleading_gate_rows()
    decision = decision_rows()
    next_rows = next_contract_rows()
    summary = nonclaim_summary_rows()
    validation = validation_rows(source_rows, rule_rows, contract_rows, projection_rows, gate_rows, decision, next_rows, summary)

    write_csv(OUT / "P8_Y5_R10_650_SOURCE_REGISTER.csv", source_rows)
    write_csv(OUT / "P8_Y5_R10_650_ULTRA_SCREENED_RULE.csv", rule_rows)
    write_csv(OUT / "P8_Y5_R10_650_CROSS_ARENA_CONTRACT.csv", contract_rows)
    write_csv(OUT / "P8_Y5_R10_650_ARENA_PROJECTION_REQUIREMENTS.csv", projection_rows)
    write_csv(OUT / "P8_Y5_R10_650_NO_SPECIAL_PLEADING_GATES.csv", gate_rows)
    write_csv(OUT / "P8_Y5_BRR545_650_DECISION.csv", decision)
    write_csv(OUT / "P8_Y5_R10_650_NEXT_CONTRACT.csv", next_rows)
    write_csv(OUT / "P8_Y5_R10_650_NONCLAIM_SUMMARY.csv", summary)
    write_csv(OUT / "P8_Y5_BRR545_650_VALIDATION.csv", validation)
    write_doc(source_rows, rule_rows, contract_rows, projection_rows, gate_rows, decision, next_rows, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"wrote_doc={DOC_PATH}")
    print(f"wrote_csv_dir={OUT}")
    print(f"kappa_one_screen_bound={SCREEN_BOUND_FOR_KAPPA_ONE:.3e}")
    print(f"validation_rows={len(validation)}")
    print(f"validation_failures={len(failures)}")
    print(f"status={STATUS}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for row in failures:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()

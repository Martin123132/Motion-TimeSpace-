from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work"
)
OUT = ROOT / "source-intake" / "mts_residuals"
SCRIPT_PATH = ROOT / "scripts" / "Y5_R10_charge_unit_Maxwell_proof_extension_or_kappa_alpha_pressure_runner.py"
DOC_PATH = ROOT / "642-Y5-R10-charge-unit-Maxwell-proof-extension-or-kappa-alpha-pressure-runner.md"

STATUS = "Y5_R10_U1_charge_structure_partial_coupling_normalization_still_blocks_kappa_alpha_zero_pressure_runner_nonclaim"
CLAIM_CEILING = "compact_U1_and_Maxwell_form_partial_only_no_alpha_EM_value_no_kappa_alpha_zero_no_R10_WEP_clock_PPN_or_local_GR_pass"
NEXT_TARGET = "643-Y5-R10-alpha-normalization-owner-or-finite-coupling-bound-input-fill.md"


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
        ("S642_0", "checkpoint_641_doc", ROOT / "641-Y5-R10-kappa-alpha-pressure-envelope-and-charge-topology-next-proof.md", "immediate prior coupling-pressure checkpoint"),
        ("S642_1", "validation_641", OUT / "P8_Y5_BRR545_641_VALIDATION.csv", "prior checkpoint validation"),
        ("S642_2", "charge_next_proof_641", OUT / "P8_Y5_R10_641_CHARGE_UNIT_NEXT_PROOF.csv", "charge-unit blocker input"),
        ("S642_3", "maxwell_next_proof_641", OUT / "P8_Y5_R10_641_MAXWELL_NORMALIZATION_NEXT_PROOF.csv", "Maxwell normalization blocker input"),
        ("S642_4", "pressure_envelope_641", OUT / "P8_Y5_R10_641_KAPPA_ALPHA_PRESSURE_ENVELOPE.csv", "finite coupling pressure factors"),
        ("S642_5", "cross_arena_reaction_641", OUT / "P8_Y5_R10_641_CROSS_ARENA_REACTION_MATRIX.csv", "cross-arena symbolic reaction matrix"),
        ("S642_6", "boundary_current_charge_287", ROOT / "287-boundary-current-charge-owner-attempt.md", "relative current and charge-unit obstruction"),
        ("S642_7", "k9_ward_index_288", ROOT / "288-k9-Ward-index-level-attempt.md", "index/level theorem obstruction"),
        ("S642_8", "andersen_charge_contract", ROOT / "source-intake" / "external_papers" / "Andersen_2026_phase_current_CHARGE_CONTRACT.csv", "external clue audit: phase/current/Maxwell contract"),
        ("S642_9", "generator_script_642", SCRIPT_PATH, "this checkpoint generator"),
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


def theorem_attempt_rows() -> list[dict[str, object]]:
    return [
        {
            "step_id": "TA642_0_parent_U1_bundle",
            "candidate_statement": "Introduce a compact charge phase as a U(1) principal-bundle fibre with theta_Q ~ theta_Q + 2pi.",
            "derivation_status": "partial_structural_success",
            "what_it_derives": "charge sectors can be labelled by U(1) representations or winding classes rather than a free sign label",
            "what_it_does_not_derive": "the observed charge unit e or the fine-structure value alpha_EM",
            "effect_on_kappa_alpha_zero": "support_only",
            "valid_for_claim": "false",
        },
        {
            "step_id": "TA642_1_integer_charge_labels",
            "candidate_statement": "For compact U(1), single-valued matter wavefunctions transform as exp(i n theta_Q), so representation labels n are integers.",
            "derivation_status": "partial_structural_success_if_U1_is_parent_signed",
            "what_it_derives": "integer relative charge labels Q = n Q_star once a base normalization Q_star exists",
            "what_it_does_not_derive": "Q_star itself, its equality to electron charge e, or a level/index denominator k",
            "effect_on_kappa_alpha_zero": "does_not_close",
            "valid_for_claim": "false",
        },
        {
            "step_id": "TA642_2_connection_and_curvature",
            "candidate_statement": "A parent U(1) connection A has curvature F = dA, giving the Bianchi identity dF = 0.",
            "derivation_status": "conditional_Maxwell_form_success",
            "what_it_derives": "no-monopole/Faraday half of Maxwell in differential-form language if A is the observed EM connection",
            "what_it_does_not_derive": "Gauss/Ampere source normalization, epsilon0, c, hbar, or Lorentz readout",
            "effect_on_kappa_alpha_zero": "support_only",
            "valid_for_claim": "false",
        },
        {
            "step_id": "TA642_3_Maxwell_action_variation",
            "candidate_statement": "Vary S_EM = -1/(4 g_EM^2) int F wedge *F + int A wedge *J to obtain d*F = g_EM^2 *J.",
            "derivation_status": "closure_form_not_parent_derivation",
            "what_it_derives": "the shape of Gauss/Ampere equations after an EM action is assumed",
            "what_it_does_not_derive": "why MTS parent action contains this term, why g_EM is fixed, or why * is the observed coframe Hodge star",
            "effect_on_kappa_alpha_zero": "blocked_by_free_g_EM",
            "valid_for_claim": "false",
        },
        {
            "step_id": "TA642_4_coupling_normalization",
            "candidate_statement": "alpha_EM = g_EM^2/(4 pi hbar c) must be quotient/topological or parent-fixed to make D_v alpha_EM = 0.",
            "derivation_status": "failed_current_corpus",
            "what_it_derives": "nothing new; it names the exact missing owner of the coupling",
            "what_it_does_not_derive": "a parent level, anomaly cancellation, monopole quantization, or Ward/index theorem fixing g_EM",
            "effect_on_kappa_alpha_zero": "hard_blocker",
            "valid_for_claim": "false",
        },
        {
            "step_id": "TA642_5_vertical_silence",
            "candidate_statement": "If g_EM, hbar, c, and the charge lattice live on quotient/topological data, then vertical local Xhat motion gives D_v alpha_EM = 0.",
            "derivation_status": "conditional_theorem_only",
            "what_it_derives": "a clean sufficient condition for local alpha silence",
            "what_it_does_not_derive": "that the sufficient condition is actually satisfied by the MTS parent action",
            "effect_on_kappa_alpha_zero": "theorem_template_not_claim",
            "valid_for_claim": "false",
        },
    ]


def maxwell_descent_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "MD642_0_Bianchi",
            "equation": "dF = 0",
            "descent_attempt": "F=dA from a U(1) connection",
            "status": "conditional_success",
            "missing_owner": "parent proof that A is the observed EM connection rather than an added closure field",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "MD642_1_Gauss_Ampere",
            "equation": "d*F = g_EM^2 *J",
            "descent_attempt": "variation of assumed Maxwell action",
            "status": "closure_success_not_parent_success",
            "missing_owner": "g_EM, source current normalization, and observed-coframe Hodge star",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "MD642_2_current_conservation",
            "equation": "d*J = 0 or nabla_mu J^mu = 0",
            "descent_attempt": "Noether/Ward current from compact phase",
            "status": "conditional_support",
            "missing_owner": "identification of relative boundary current with EM source current",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "MD642_3_Lorentz_readout",
            "equation": "m a^mu = q F^mu_nu u^nu",
            "descent_attempt": "minimal coupling q int A_mu dx^mu",
            "status": "closure_form_not_parent_derivation",
            "missing_owner": "ordinary matter coupling derived from MTS coframe without hidden material marker",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "MD642_4_alpha_constant",
            "equation": "alpha_EM = g_EM^2/(4 pi hbar c)",
            "descent_attempt": "demand quotient-invariant or topological g_EM",
            "status": "blocked",
            "missing_owner": "no sourced level, index, anomaly, monopole, or Ward theorem fixes g_EM",
            "valid_for_claim": "false",
        },
    ]


def zero_verdict_rows() -> list[dict[str, object]]:
    return [
        {
            "verdict_id": "ZV642_0",
            "claim_tested": "kappa_alpha = D_local ln(alpha_EM)/D Xhat = 0",
            "sufficient_condition": "charge lattice, gauge kinetic coefficient, hbar, c, and observed coframe readout are quotient/topological and locally vertical-silent",
            "current_result": "not_proved",
            "reason": "compact U(1) gives integer labels but leaves the base coupling g_EM free; Maxwell form can be written but not parent-owned",
            "allowed_next_branch": "finite_coupling_pressure_runner_nonclaim",
            "valid_for_claim": "false",
        }
    ]


def load_pressure_inputs() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    envelope = read_csv(OUT / "P8_Y5_R10_641_KAPPA_ALPHA_PRESSURE_ENVELOPE.csv")
    reaction = read_csv(OUT / "P8_Y5_R10_641_CROSS_ARENA_REACTION_MATRIX.csv")
    return envelope, reaction


def pressure_runner_smoke_rows() -> list[dict[str, object]]:
    envelope, reaction = load_pressure_inputs()
    rows: list[dict[str, object]] = []
    for env in envelope:
        factor = env["normalized_abs_kappa_alpha_factor"]
        for arena in reaction:
            if factor == "0":
                expression = f"0 * ({arena['reaction_expression']})"
                interpretation = "theorem-zero sensitivity row only; not a claim because theorem-zero proof is blocked"
            elif factor.startswith("MISSING"):
                expression = f"{factor} * ({arena['reaction_expression']})"
                interpretation = "bound-saturating row blocked by missing normalization"
            else:
                expression = f"{factor} * sign(kappa_alpha) * ({arena['reaction_expression']})"
                interpretation = "symbolic pressure response only; no physical kappa_alpha unit or tau map"
            rows.append(
                {
                    "smoke_id": f"PRS642_{len(rows):02d}",
                    "branch_id": env["branch_id"],
                    "arena_id": arena["arena_id"],
                    "normalized_abs_kappa_alpha_factor": factor,
                    "symbolic_response": expression,
                    "missing_for_score": arena["missing_for_score"],
                    "numeric_ready": "false",
                    "valid_for_claim": "false",
                    "interpretation": interpretation,
                }
            )
    return rows


def runner_schema_rows() -> list[dict[str, object]]:
    return [
        {
            "input_id": "RS642_0",
            "needed_input": "physical Xhat unit",
            "status": "missing",
            "why_needed": "turns normalized pressure factors into a derivative with units",
            "blocks_numeric_score": "true",
        },
        {
            "input_id": "RS642_1",
            "needed_input": "tau_R10, tau_WEP, tau_clock, tau_EM",
            "status": "missing",
            "why_needed": "projects parent/local alpha response into each arena observable",
            "blocks_numeric_score": "true",
        },
        {
            "input_id": "RS642_2",
            "needed_input": "composition and clock alpha sensitivities",
            "status": "missing",
            "why_needed": "WEP and clocks cannot score alpha pressure without material/transition sensitivity coefficients",
            "blocks_numeric_score": "true",
        },
        {
            "input_id": "RS642_3",
            "needed_input": "source/test-body EM binding normalization for R10",
            "status": "missing",
            "why_needed": "short-range force limits constrain body-level residuals, not raw alpha_EM derivatives",
            "blocks_numeric_score": "true",
        },
        {
            "input_id": "RS642_4",
            "needed_input": "parent owner of g_EM or explicit finite prior",
            "status": "missing",
            "why_needed": "chooses theorem-zero route or honest finite-coupling route",
            "blocks_numeric_score": "true",
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D642_0",
            "route": "theorem_zero",
            "result": "blocked",
            "reason": "compact U(1) and connection geometry do not fix g_EM or alpha_EM",
            "next_action": "hunt owner of alpha normalization: level/index/anomaly/monopole/Ward or explicit finite prior",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D642_1",
            "route": "finite_coupling_pressure_runner",
            "result": "schema_ready_nonclaim",
            "reason": "pressure rows and cross-arena symbolic reactions can be combined, but all score-critical inputs are missing",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "theorem_zero_claim": "false",
            "maxwell_claim": "false",
            "pressure_runner_claim": "false",
            "numeric_score_allowed": "false",
            "strongest_positive_result": "compact U1 gives a mathematically respectable route to integer charge labels and dF=0 structure if parent-signed",
            "hardest_blocker": "the base EM coupling g_EM/alpha_EM is still free unless a parent level/index/anomaly/monopole/Ward owner is found",
            "next_target": NEXT_TARGET,
        }
    ]


def validation_rows(
    source_rows: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    maxwell_rows: list[dict[str, object]],
    zero_rows: list[dict[str, object]],
    pressure_rows: list[dict[str, object]],
    schema_rows: list[dict[str, object]],
    decision: list[dict[str, object]],
    summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V642_0_source_paths_exist", all(row["exists"] == "true" for row in source_rows), "all cited local source paths exist"))
    prior = read_csv(OUT / "P8_Y5_BRR545_641_VALIDATION.csv")
    checks.append(("V642_1_prior_641_validation_clean", all(row.get("result") == "pass" for row in prior), "641 validation remains clean"))
    checks.append(("V642_2_theorem_has_partial_success", any("success" in row["derivation_status"] for row in theorem_rows), "U1 route records real partial structural successes"))
    checks.append(("V642_3_theorem_still_blocks_claim", any(row["effect_on_kappa_alpha_zero"] in {"hard_blocker", "blocked_by_free_g_EM"} or "blocked" in row["derivation_status"] for row in theorem_rows), "coupling normalization blocker remains explicit"))
    checks.append(("V642_4_maxwell_alpha_blocked", any(row["gate_id"] == "MD642_4_alpha_constant" and row["status"] == "blocked" for row in maxwell_rows), "alpha constant gate remains blocked"))
    checks.append(("V642_5_zero_verdict_nonclaim", zero_rows[0]["current_result"] == "not_proved" and zero_rows[0]["valid_for_claim"] == "false", "zero verdict is not claim-valid"))
    envelope_count = len(read_csv(OUT / "P8_Y5_R10_641_KAPPA_ALPHA_PRESSURE_ENVELOPE.csv"))
    reaction_count = len(read_csv(OUT / "P8_Y5_R10_641_CROSS_ARENA_REACTION_MATRIX.csv"))
    checks.append(("V642_6_pressure_smoke_row_count", len(pressure_rows) == envelope_count * reaction_count, "pressure smoke covers every 641 envelope x arena pair"))
    checks.append(("V642_7_pressure_rows_nonclaim", all(row["numeric_ready"] == "false" and row["valid_for_claim"] == "false" for row in pressure_rows), "pressure smoke rows remain nonclaim"))
    checks.append(("V642_8_schema_blocks_numeric_score", all(row["blocks_numeric_score"] == "true" for row in schema_rows), "runner schema keeps numeric score blocked"))
    checks.append(("V642_9_decisions_nonclaim", all(row["valid_for_claim"] == "false" for row in decision), "decision rows do not claim a pass"))
    checks.append(("V642_10_summary_nonclaim", summary[0]["numeric_score_allowed"] == "false" and summary[0]["theorem_zero_claim"] == "false", "summary stays nonclaim"))

    fw = ROOT.parent / "formalization-workbench"
    cutoff = datetime(2026, 5, 31, 14, 42, 0).timestamp()
    changed_after_cutoff = 0
    if fw.exists():
        for path in fw.rglob("*"):
            if path.is_file() and path.stat().st_mtime > cutoff:
                changed_after_cutoff += 1
    checks.append(("V642_11_formalization_workbench_unchanged", changed_after_cutoff == 0, f"formalization files changed after cutoff: {changed_after_cutoff}"))

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
    theorem_rows: list[dict[str, object]],
    maxwell_rows: list[dict[str, object]],
    zero_rows: list[dict[str, object]],
    pressure_rows: list[dict[str, object]],
    schema_rows: list[dict[str, object]],
    decision: list[dict[str, object]],
    summary: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    pressure_preview = pressure_rows[:10]
    lines = [
        "# 642 Y5/R10 Charge-Unit Maxwell Proof Extension or Kappa-Alpha Pressure Runner",
        "",
        "## Verdict",
        "",
        f"- Status: `{STATUS}`",
        f"- Claim ceiling: `{CLAIM_CEILING}`",
        "- The theorem-zero attempt gets a real partial result: compact `U(1)` structure can give integer charge labels and the `dF = 0` half of Maxwell, if it is parent-signed.",
        "- The proof still blocks at the actual coupling: the base `g_EM` / `alpha_EM` normalization is not fixed by compactness alone.",
        "- Therefore `kappa_alpha = 0` is not claimable. The finite-coupling pressure runner is now schema-ready but remains nonclaim.",
        "",
        "## Source Register",
        "",
        markdown_table(source_rows, ["source_id", "label", "path", "exists", "role"]),
        "",
        "## Theorem-Zero Attempt",
        "",
        markdown_table(theorem_rows, ["step_id", "derivation_status", "candidate_statement", "what_it_derives", "what_it_does_not_derive", "effect_on_kappa_alpha_zero"]),
        "",
        "## Maxwell Descent Attempt",
        "",
        markdown_table(maxwell_rows, ["gate_id", "equation", "descent_attempt", "status", "missing_owner"]),
        "",
        "## Zero Verdict",
        "",
        markdown_table(zero_rows, ["verdict_id", "claim_tested", "current_result", "reason", "allowed_next_branch"]),
        "",
        "## Pressure Runner Smoke",
        "",
        "The runner now combines every 641 pressure-envelope row with every 641 cross-arena row. These are symbolic response rows only; none are numeric scores.",
        "",
        markdown_table(pressure_preview, ["smoke_id", "branch_id", "arena_id", "normalized_abs_kappa_alpha_factor", "numeric_ready", "valid_for_claim"]),
        "",
        f"- Full pressure-smoke rows: `{len(pressure_rows)}`",
        "",
        "## Runner Schema Blocks",
        "",
        markdown_table(schema_rows, ["input_id", "needed_input", "status", "why_needed", "blocks_numeric_score"]),
        "",
        "## Decision",
        "",
        markdown_table(decision, ["decision_id", "route", "result", "reason", "next_action"]),
        "",
        "## Validation",
        "",
        markdown_table(validation, ["check_id", "result", "detail"]),
        "",
        "## Interpretation",
        "",
        "- This is a useful narrowing, not a dead end: the EM branch is not missing everything; it is missing the owner of the coupling.",
        "- The cleanest possible route is now sharply defined: find a parent level/index/anomaly/monopole/Ward reason that fixes `g_EM` or makes it quotient-invariant.",
        "- If that owner cannot be found, the honest route is finite `kappa_alpha`, but it must be projected through real `Xhat` units, `tau` maps, and material sensitivities before any comparison score.",
        "",
        "## Nonclaim Summary",
        "",
        markdown_table(summary, ["status", "theorem_zero_claim", "maxwell_claim", "pressure_runner_claim", "numeric_score_allowed", "hardest_blocker", "next_target"]),
        "",
    ]
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source_rows = source_register_rows()
    theorem_rows = theorem_attempt_rows()
    maxwell_rows = maxwell_descent_rows()
    zero_rows = zero_verdict_rows()
    pressure_rows = pressure_runner_smoke_rows()
    schema_rows = runner_schema_rows()
    decision = decision_rows()
    summary = nonclaim_summary_rows()
    validation = validation_rows(source_rows, theorem_rows, maxwell_rows, zero_rows, pressure_rows, schema_rows, decision, summary)

    write_csv(OUT / "P8_Y5_R10_642_SOURCE_REGISTER.csv", source_rows)
    write_csv(OUT / "P8_Y5_R10_642_THEOREM_ZERO_ATTEMPT.csv", theorem_rows)
    write_csv(OUT / "P8_Y5_R10_642_MAXWELL_DESCENT_ATTEMPT.csv", maxwell_rows)
    write_csv(OUT / "P8_Y5_R10_642_ZERO_VERDICT.csv", zero_rows)
    write_csv(OUT / "P8_Y5_R10_642_PRESSURE_RUNNER_SMOKE.csv", pressure_rows)
    write_csv(OUT / "P8_Y5_R10_642_RUNNER_SCHEMA_BLOCKS.csv", schema_rows)
    write_csv(OUT / "P8_Y5_BRR545_642_DECISION.csv", decision)
    write_csv(OUT / "P8_Y5_R10_642_NONCLAIM_SUMMARY.csv", summary)
    write_csv(OUT / "P8_Y5_BRR545_642_VALIDATION.csv", validation)
    write_doc(source_rows, theorem_rows, maxwell_rows, zero_rows, pressure_rows, schema_rows, decision, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"wrote_doc={DOC_PATH}")
    print(f"wrote_csv_dir={OUT}")
    print(f"pressure_smoke_rows={len(pressure_rows)}")
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

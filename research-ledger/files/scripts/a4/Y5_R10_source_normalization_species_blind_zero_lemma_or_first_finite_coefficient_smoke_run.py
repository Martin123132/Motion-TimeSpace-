from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "950-Y5-R10-source-normalization-species-blind-zero-lemma-or-first-finite-coefficient-smoke-run.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _field in fields) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join([header, separator, *body])


def source_path(relative_path: str) -> Path:
    return ROOT / relative_path


def parse_float(value: str) -> float | None:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "949_doc",
            "path": "949-Y5-R10-parent-constant-sector-superselection-action-clause-or-finite-source-coefficient-input.md",
            "role": "handoff: theorem-or-number fork made explicit",
            "needle": "we now know exactly what number or theorem the next step must supply",
        },
        {
            "source_id": "949_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_949_VALIDATION.csv",
            "role": "previous checkpoint validation",
            "needle": "V949_12_validation_rows_ready",
        },
        {
            "source_id": "949_next_target",
            "path": "source-intake/mts_residuals/P8_Y5_R10_949_NEXT_TARGET.csv",
            "role": "950 target selection",
            "needle": "950-Y5-R10-source-normalization-species-blind-zero-lemma-or-first-finite-coefficient-smoke-run.md",
        },
        {
            "source_id": "949_input_schema",
            "path": "source-intake/mts_residuals/P8_Y5_R10_949_FINITE_COEFFICIENT_INPUT_SCHEMA.csv",
            "role": "finite coefficient input schema",
            "needle": "FCI949_2_WEP_surface_beta_source",
        },
        {
            "source_id": "949_parent_clause",
            "path": "source-intake/mts_residuals/P8_Y5_R10_949_PARENT_CLAUSE_ATTEMPT.csv",
            "role": "candidate parent clause, not adopted",
            "needle": "PCA949_2_source_universality",
        },
        {
            "source_id": "949_readiness",
            "path": "source-intake/mts_residuals/P8_Y5_R10_949_PRODUCT_RUNNER_READINESS.csv",
            "role": "product runner readiness",
            "needle": "PRR949_1_WEP",
        },
        {
            "source_id": "no_species_contract",
            "path": "source-intake/mts_residuals/P8_no_species_source_charge_CONTRACT.csv",
            "role": "species/source charge contract",
            "needle": "S4_source_normalization_species_blind",
        },
        {
            "source_id": "763_no_marker_spurion",
            "path": "source-intake/mts_residuals/P8_Y5_R10_763_NO_MARKER_SPURION_THEOREM_ATTEMPT.csv",
            "role": "no-marker and source-weight blockers",
            "needle": "NMS763_3_universal_source_weight",
        },
        {
            "source_id": "631_source_charge_law",
            "path": "source-intake/mts_residuals/P8_Y5_R10_631_SOURCE_TEST_CHARGE_LAW.csv",
            "role": "source/test charge branch law",
            "needle": "Q631_2_composition_channel",
        },
        {
            "source_id": "651_WEP_runner",
            "path": "source-intake/mts_residuals/P8_Y5_R10_948_WEP_PRODUCT_BOUND_RUNNER.csv",
            "role": "WEP source-product bound rows",
            "needle": "WEP948_1_WAS651_1_surface_binding",
        },
        {
            "source_id": "948_clock_runner",
            "path": "source-intake/mts_residuals/P8_Y5_R10_948_CLOCK_PRODUCT_BOUND_RUNNER.csv",
            "role": "clock product-bound rows",
            "needle": "CLK948_1_CAS646_1_YbE3E2",
        },
    ]
    rows = []
    for spec in specs:
        path = source_path(spec["path"])
        exists = path.exists()
        needle_found = exists and spec["needle"] in read_text(path)
        rows.append(
            {
                **spec,
                "absolute_path": str(path),
                "exists": flag(exists),
                "needle_found": flag(needle_found),
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def source_normalization_lemma_attempt() -> list[dict[str, str]]:
    return [
        {
            "lemma_id": "SNL950_0_target",
            "statement": "measured gravitational source normalization is species blind",
            "mathematical_form": "J_source = kappa_univ sum_A T_A[e_obs] with Lie_v kappa_univ=0 and no kappa_A(X)",
            "proof_status": "target_identified",
            "what_closes": "beta_source_normalized=0 for WEP source-normalization channel",
            "blocker": "current corpus lists S4 as not_parent_derived",
            "counterexample": "species-dependent kappa_A remains legal",
            "closes_zero": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "lemma_id": "SNL950_1_diffeomorphism_ward_identity",
            "statement": "diffeomorphism covariance gives conservation of total stress current",
            "mathematical_form": "nabla_mu T_total^{mu nu}=0 on shell",
            "proof_status": "valid_but_insufficient",
            "what_closes": "conservation bookkeeping only",
            "blocker": "conservation of the sum does not imply species-blind normalization or zero composition charge",
            "counterexample": "T_total conserved with kappa_A != kappa_B",
            "closes_zero": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "lemma_id": "SNL950_2_minimal_metric_coupling",
            "statement": "minimal universal coupling would make all ordinary species source the same observed metric",
            "mathematical_form": "S_m=sum_A S_A[Psi_A,e_obs,theta_univ] and delta theta_univ=0",
            "proof_status": "valid_conditional_lemma",
            "what_closes": "WEP source split vanishes if matter factorization and constant-sector clauses are parent-signed",
            "blocker": "matter factorization and constant universality are still candidate clauses",
            "counterexample": "marker-dependent theta_A or kappa_A survives if clauses are not parent-signed",
            "closes_zero": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "lemma_id": "SNL950_3_measured_GM_normalization",
            "statement": "measured source mass/GM cannot be assumed species independent while constants can vary",
            "mathematical_form": "mu_obs,A = G_eff(X,A) M_A(theta_A,X)",
            "proof_status": "hazard_identified",
            "what_closes": "nothing; this is the anti-cheat guard",
            "blocker": "measured GM can absorb composition dependence unless source-current universality is derived",
            "counterexample": "mu_obs,A = mu_A(1+epsilon_A X) creates WEP source split with same metric background",
            "closes_zero": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "lemma_id": "SNL950_4_countermodel",
            "statement": "quotient/metric descent alone does not force source normalization to be species blind",
            "mathematical_form": "q(Phi) fixed, e_obs fixed, but kappa_A=kappa(1+epsilon f_A m) gives Lie_v kappa_A != 0",
            "proof_status": "countermodel_blocks_unconditional_theorem",
            "what_closes": "blocks overclaim",
            "blocker": "must exclude matter-visible source weights at parent-action level",
            "counterexample": "species-weighted source current",
            "closes_zero": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "lemma_id": "SNL950_5_verdict",
            "statement": "species-blind source-normalization zero lemma closes WEP beta_source",
            "mathematical_form": "beta_source_normalized=0 follows only if SNL950_2 premises plus no source-weight marker are parent-signed",
            "proof_status": "not_closed_current_corpus",
            "what_closes": "would close WEP beta_source if parent-signed",
            "blocker": "S4 and NMS763_3 remain not_parent_signed",
            "counterexample": "retained species-weighted source current",
            "closes_zero": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def finite_smoke_input_template() -> list[dict[str, str]]:
    rows = []
    for source in read_csv(OUT / "P8_Y5_R10_949_FINITE_COEFFICIENT_INPUT_SCHEMA.csv"):
        rows.append(
            {
                "template_id": source["input_id"].replace("FCI949", "FST950"),
                "coefficient_symbol": source["coefficient_symbol"],
                "arena": source["arena"],
                "units": source["units"],
                "candidate_value": "MISSING_PARENT_INPUT",
                "candidate_source_path": "MISSING_PARENT_SOURCE",
                "branch_label": "finite_candidate_or_parent_zero_required",
                "comparison_bound": source["comparison_bound"],
                "comparison_rule": source["comparison_rule"],
                "input_ready": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def finite_coefficient_smoke_runner(template_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    for template in template_rows:
        value = parse_float(template["candidate_value"])
        bound = parse_float(template["comparison_bound"])
        is_boolean_zero = template["coefficient_symbol"] == "constant_source_zero_theorem"
        numeric_score_ready = value is not None and bound is not None
        theorem_score_ready = is_boolean_zero and template["candidate_value"] == "PARENT_SIGNED_TRUE"
        score_ready = numeric_score_ready or theorem_score_ready
        if numeric_score_ready:
            passes = abs(value) <= bound
            verdict = "PASS_NUMERIC_BOUND_NONCLAIM" if passes else "FAIL_NUMERIC_BOUND_NONCLAIM"
        elif theorem_score_ready:
            passes = True
            verdict = "PASS_PARENT_SIGNED_ZERO_THEOREM_NONCLAIM"
        else:
            passes = False
            verdict = "REFUSED_MISSING_PARENT_INPUT_OR_SOURCE"
        rows.append(
            {
                "run_id": template["template_id"].replace("FST950", "FSR950"),
                "coefficient_symbol": template["coefficient_symbol"],
                "arena": template["arena"],
                "candidate_value": template["candidate_value"],
                "candidate_source_path": template["candidate_source_path"],
                "comparison_bound": template["comparison_bound"],
                "comparison_rule": template["comparison_rule"],
                "score_ready": flag(score_ready),
                "passes_bound": flag(passes) if score_ready else "false",
                "verdict": verdict,
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def strict_refusal_ledger() -> list[dict[str, str]]:
    return [
        {
            "refusal_id": "REF950_0_no_invented_coefficients",
            "rule": "do not invent kappa_alpha_tau_clock_time or beta_source_normalized",
            "enforced_by": "finite smoke template has candidate_value=MISSING_PARENT_INPUT and score_ready=false",
            "status": "enforced",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "refusal_id": "REF950_1_no_silent_zero",
            "rule": "do not use zero unless parent-signed theorem is supplied",
            "enforced_by": "constant_source_zero_theorem requires PARENT_SIGNED_TRUE, not closure preference",
            "status": "enforced",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "refusal_id": "REF950_2_no_WEP_clock_claim",
            "rule": "source-side bounds are not MTS passes without an MTS coefficient or zero theorem",
            "enforced_by": "all smoke rows claim_allowed=false and valid_for_claim=false",
            "status": "enforced",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decisions() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC950_0_source_normalization",
            "topic": "species-blind source-normalization lemma",
            "result": "conditional_lemma_valid_unconditional_theorem_rejected",
            "reason": "diffeomorphism/metric descent gives conservation and conditional universality, but not species-blind source normalization unless S4/NMS763_3 are parent-signed",
            "next_action": "derive source-current universality from a parent Ward/source action, or retain beta_source as finite input",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC950_1_finite_smoke_runner",
            "topic": "finite coefficient smoke runner",
            "result": "strict_refusal_runner_written",
            "reason": "runner is ready to compare future numeric coefficients, but currently refuses to score missing parent inputs",
            "next_action": "build provenance gate for any proposed finite coefficient value",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gates() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE950_0_source_normalization_zero",
            "claim": "beta_source_normalized=0 by species-blind source normalization",
            "required_condition": "parent-signed source-current universality and no species source weight",
            "current_evidence": "conditional lemma plus countermodel",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE950_1_finite_smoke_score",
            "claim": "finite coefficient smoke runner can score current MTS inputs",
            "required_condition": "candidate_value numeric with source path, or PARENT_SIGNED_TRUE zero theorem",
            "current_evidence": "all candidate values are MISSING_PARENT_INPUT",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE950_2_local_GR",
            "claim": "local GR/WEP/clock pass",
            "required_condition": "R10/PPN plus WEP/clock coefficient routes closed together",
            "current_evidence": "950 only sharpens WEP/clock coefficient gate; no local-GR closure",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target() -> list[dict[str, str]]:
    return [
        {
            "next_target": "951-Y5-R10-source-current-Ward-action-or-finite-coefficient-provenance-gate.md",
            "objective": "derive source-current universality from a parent Ward/source action, or require provenance for any proposed finite kappa_alpha_tau_clock_time or beta_source_normalized coefficient before the smoke runner can score it",
            "include": "source action, Ward identity, measured-GM normalization, coefficient provenance fields, strict no-invention gate",
            "exclude": "invented coefficient values, zero-by-closure, WEP/clock/local-GR claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return -1
    changed = 0
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
        if modified > SCRIPT_START_UTC:
            changed += 1
    return changed


def validation(
    sources: list[dict[str, str]],
    lemma_rows: list[dict[str, str]],
    template_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
    refusal_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    def add(check_id: str, passes: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passes else "fail", "detail": detail, "generated_utc": stamp()})

    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    prior_clean = all(row.get("result") == "pass" for row in read_csv(OUT / "P8_Y5_BRR545_949_VALIDATION.csv"))
    lemma_not_closed = any(row["lemma_id"] == "SNL950_5_verdict" and row["closes_zero"] == "false" for row in lemma_rows)
    countermodel_retained = any(row["lemma_id"] == "SNL950_4_countermodel" for row in lemma_rows)
    template_ready = len(template_rows) == 5 and all(row["input_ready"] == "false" for row in template_rows)
    smoke_refuses = all(row["score_ready"] == "false" and row["verdict"] == "REFUSED_MISSING_PARENT_INPUT_OR_SOURCE" for row in smoke_rows)
    refusal_enforced = all(row["status"] == "enforced" for row in refusal_rows)
    decisions_nonclaim = all(row["claim_allowed"] == "false" for row in decision_rows)
    claim_gates_false = all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claim_rows)
    target_selected = target_rows and target_rows[0]["next_target"].startswith("951-")
    valid_for_claim_false = all(
        row.get("valid_for_claim") == "false"
        for table in [sources, lemma_rows, template_rows, smoke_rows, refusal_rows, decision_rows, claim_rows, target_rows]
        for row in table
    )
    formalization_changed = formalization_changed_after_start()

    add("V950_0_sources_exist_and_needles", sources_ok, "all 950 source paths exist and needles are present" if sources_ok else "missing source path or needle")
    add("V950_1_prior_949_clean", prior_clean, "P8_Y5_BRR545_949_VALIDATION.csv clean")
    add("V950_2_source_normalization_not_closed", lemma_not_closed, "source-normalization zero lemma remains unclosed")
    add("V950_3_countermodel_retained", countermodel_retained, "species-weighted source current countermodel recorded")
    add("V950_4_template_ready_missing_inputs", template_ready, "finite coefficient template rows present with missing inputs")
    add("V950_5_smoke_runner_refuses_missing_inputs", smoke_refuses, "smoke runner refuses every missing coefficient")
    add("V950_6_strict_refusal_enforced", refusal_enforced, "no invented coefficient, no silent zero, no WEP/clock claim rules enforced")
    add("V950_7_decisions_nonclaim", decisions_nonclaim, "decision ledger remains nonclaim")
    add("V950_8_claim_gates_false", claim_gates_false, "all claim gates remain false")
    add("V950_9_next_target_selected", target_selected, "951 source-current Ward action or coefficient provenance target selected")
    add("V950_10_no_claims_promoted", valid_for_claim_false, "all generated rows are valid_for_claim=false")
    add("V950_11_formalization_workbench_untouched", formalization_changed == 0, f"formalization_changed_after_start={formalization_changed}")
    add("V950_12_validation_rows_ready", True, "validation table constructed")
    return rows


def write_doc(
    sources: list[dict[str, str]],
    lemma_rows: list[dict[str, str]],
    template_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
    refusal_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    doc = f"""# 950 Y5 R10: Source-Normalization Species-Blind Zero Lemma Or First Finite-Coefficient Smoke Run

Status: `Y5_R10_950_source_normalization_zero_lemma_not_closed_strict_smoke_refusal_runner_written_nonclaim`

Claim ceiling: `conditional_source_universality_only_no_finite_score_no_WEP_no_clock_no_local_GR_claim`

## Result

This checkpoint tried the best route first: derive species-blind source normalization so the WEP source coefficient becomes theorem-zero.

The result is honest but not closed. Diffeomorphism covariance and minimal metric coupling give useful conditional structure, but they do not by themselves force `kappa_A=kappa_B` or remove species-dependent measured-GM/source weights. A species-weighted source-current countermodel remains legal unless the parent action signs the source-current universality/no-marker clause.

The finite route is now safer: a first smoke runner exists, but it refuses to score every row because all coefficient values are still `MISSING_PARENT_INPUT`. That is exactly the desired anti-cheat behavior.

```text
source-normalization zero: conditional, not derived;
finite coefficient smoke: runnable, but refuses missing values;
next required object: parent source-current Ward action or coefficient provenance.
```

## Source Register

{md_table(sources, ["source_id", "role", "exists", "needle_found", "path"])}

## Source-Normalization Lemma Attempt

{md_table(lemma_rows, ["lemma_id", "statement", "proof_status", "blocker", "counterexample", "closes_zero"])}

## Finite Smoke Input Template

{md_table(template_rows, ["template_id", "coefficient_symbol", "arena", "candidate_value", "comparison_bound", "input_ready"])}

## Finite Coefficient Smoke Runner

{md_table(smoke_rows, ["run_id", "coefficient_symbol", "arena", "candidate_value", "comparison_bound", "score_ready", "verdict"])}

## Strict Refusal Ledger

{md_table(refusal_rows, ["refusal_id", "rule", "enforced_by", "status"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "topic", "result", "reason", "next_action", "claim_allowed"])}

## Claim Gate

{md_table(claim_rows, ["gate_id", "claim", "current_evidence", "gate_pass", "claim_allowed"])}

## Validation

{md_table(validation_rows, ["check_id", "result", "detail", "generated_utc"])}

## Next Target

{md_table(target_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"])}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    sources = source_register()
    lemma_rows = source_normalization_lemma_attempt()
    template_rows = finite_smoke_input_template()
    smoke_rows = finite_coefficient_smoke_runner(template_rows)
    refusal_rows = strict_refusal_ledger()
    decision_rows = decisions()
    claim_rows = claim_gates()
    target_rows = next_target()
    validation_rows = validation(sources, lemma_rows, template_rows, smoke_rows, refusal_rows, decision_rows, claim_rows, target_rows)

    write_csv(
        OUT / "P8_Y5_R10_950_SOURCE_REGISTER.csv",
        sources,
        ["source_id", "path", "role", "needle", "absolute_path", "exists", "needle_found", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_950_SOURCE_NORMALIZATION_LEMMA_ATTEMPT.csv",
        lemma_rows,
        [
            "lemma_id",
            "statement",
            "mathematical_form",
            "proof_status",
            "what_closes",
            "blocker",
            "counterexample",
            "closes_zero",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_950_FINITE_SMOKE_INPUT_TEMPLATE.csv",
        template_rows,
        [
            "template_id",
            "coefficient_symbol",
            "arena",
            "units",
            "candidate_value",
            "candidate_source_path",
            "branch_label",
            "comparison_bound",
            "comparison_rule",
            "input_ready",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_950_FINITE_COEFFICIENT_SMOKE_RUNNER.csv",
        smoke_rows,
        [
            "run_id",
            "coefficient_symbol",
            "arena",
            "candidate_value",
            "candidate_source_path",
            "comparison_bound",
            "comparison_rule",
            "score_ready",
            "passes_bound",
            "verdict",
            "claim_allowed",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_950_STRICT_REFUSAL_LEDGER.csv",
        refusal_rows,
        ["refusal_id", "rule", "enforced_by", "status", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_950_DECISION_LEDGER.csv",
        decision_rows,
        ["decision_id", "topic", "result", "reason", "next_action", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_950_CLAIM_GATE.csv",
        claim_rows,
        ["gate_id", "claim", "required_condition", "current_evidence", "gate_pass", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_950_NEXT_TARGET.csv",
        target_rows,
        ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_BRR545_950_VALIDATION.csv",
        validation_rows,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_doc(sources, lemma_rows, template_rows, smoke_rows, refusal_rows, decision_rows, claim_rows, target_rows, validation_rows)


if __name__ == "__main__":
    main()

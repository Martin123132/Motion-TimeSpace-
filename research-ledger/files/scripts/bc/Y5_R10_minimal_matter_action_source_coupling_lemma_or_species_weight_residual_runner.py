from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "955-Y5-R10-minimal-matter-action-source-coupling-lemma-or-species-weight-residual-runner.md"
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
        return float(value)
    except ValueError:
        return None


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "954_doc",
            "path": "954-Y5-R10-parent-matter-category-no-species-label-clause-or-source-functor-countermodel-bound.md",
            "role": "handoff: PAC954 no-source-prefactor obstruction",
            "needle": "no independent species source prefactors",
        },
        {
            "source_id": "954_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_954_VALIDATION.csv",
            "role": "previous checkpoint validation",
            "needle": "V954_13_validation_rows_ready",
        },
        {
            "source_id": "954_parent_action_clause",
            "path": "source-intake/mts_residuals/P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv",
            "role": "minimal matter action clause inputs",
            "needle": "PAC954_1_no_source_prefactors",
        },
        {
            "source_id": "954_bound_targets",
            "path": "source-intake/mts_residuals/P8_Y5_R10_954_SOURCE_FUNCTOR_BOUND_TARGETS.csv",
            "role": "nonclaim residual bound targets",
            "needle": "SCB954_2_WEP_surface_beta_source",
        },
        {
            "source_id": "954_countermodel_map",
            "path": "source-intake/mts_residuals/P8_Y5_R10_954_COUNTERMODEL_TO_BOUND_MAP.csv",
            "role": "species-weight countermodel to observable map",
            "needle": "CBM954_3_verdict",
        },
        {
            "source_id": "953_theorem",
            "path": "source-intake/mts_residuals/P8_Y5_R10_953_SOURCE_FUNCTOR_THEOREM_ATTEMPT.csv",
            "role": "conditional no-species-label theorem",
            "needle": "NSF953_5_verdict",
        },
        {
            "source_id": "source_current_contract",
            "path": "source-intake/mts_residuals/P8_source_current_Ward_universality_CONTRACT.csv",
            "role": "universal kappa/source-current contract",
            "needle": "SC3_universal_kappa_coupling",
        },
        {
            "source_id": "r11_missing_ledger",
            "path": "source-intake/mts_residuals/P8_R11_SOURCE_NORMALIZATION_MISSING_LEDGER.csv",
            "role": "species source charge theorem or vector missing row",
            "needle": "MISSING_SELECTOR_BLIND_SOURCE_THEOREM_OR_SPECIES_CHARGE_VECTOR",
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


def minimal_matter_action_lemma() -> list[dict[str, str]]:
    return [
        {
            "lemma_id": "MMA955_0_target",
            "claim_shape": "minimal matter action forbids independent source-only species weights",
            "mathematical_form": "S_matter=sum_A S_A[Psi_A,e_obs,theta_A], no w_A slot",
            "status": "target_from_954",
            "would_prove": "PAC954_1_no_source_prefactors",
            "obstruction": "absence of a slot is a parent action schema condition unless derived from a deeper quotient",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "lemma_id": "MMA955_1_same_action_principle",
            "claim_shape": "matter dynamics and gravitational source are obtained from the same matter functional",
            "mathematical_form": "E_Psi=delta S_matter/delta Psi; T_munu=delta S_matter/delta g_obs^{munu}",
            "status": "strong_clean_principle",
            "would_prove": "rules out a separate source functional S_source[species labels]",
            "obstruction": "a constant prefactor inside S_A still scales T_A while preserving classical equations of motion",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "lemma_id": "MMA955_2_common_prefactor",
            "claim_shape": "one common prefactor on the whole matter action is harmless after G calibration",
            "mathematical_form": "S_matter -> w_common S_matter; kappa_univ w_common -> kappa_measured",
            "status": "common_mode_absorbable",
            "would_prove": "common source normalization is not a WEP residual",
            "obstruction": "only relative weights w_A/w_B are dangerous",
            "parent_signed": "conditional_common_mode_only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "lemma_id": "MMA955_3_relative_prefactor",
            "claim_shape": "relative species prefactors are not removed by Ward symmetry, covariance, or additivity",
            "mathematical_form": "S_matter=sum_A w_A S_A; T_source=sum_A w_A T_A",
            "status": "counterexample_survives",
            "would_prove": "nothing; this is the live residual if parent minimality is unsigned",
            "obstruction": "w_A can be constant and still pass Ward/additivity checks",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "lemma_id": "MMA955_4_field_rescaling_limit",
            "claim_shape": "field redefinitions do not give a universal proof that relative w_A are absent",
            "mathematical_form": "Psi_A -> sqrt(w_A) Psi_A may move w_A into interactions, charges, or quantum normalization",
            "status": "not_a_general_derivation",
            "would_prove": "at most model-by-model redundancy",
            "obstruction": "interactions and measured nongravitational constants can make relative normalization observable",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "lemma_id": "MMA955_5_minimal_schema",
            "claim_shape": "if the parent schema admits no source-only coefficients and fixes matter normalization by nongravitational standards, w_A is absent by construction",
            "mathematical_form": "Allowed[S_matter] excludes w_A; theta_A contains masses/charges, not active-source multipliers",
            "status": "conditional_parent_schema_lemma",
            "would_prove": "label-forgotten source side when combined with 953 and 954",
            "obstruction": "schema has not yet been signed as a parent theorem",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "lemma_id": "MMA955_6_verdict",
            "claim_shape": "minimal-matter-action source-coupling lemma",
            "mathematical_form": "same action + total Hilbert variation + no source-only slots => one source current",
            "status": "exact_lemma_contract_not_parent_derivation",
            "would_prove": "source-side GR/Newton coupling branch up to hidden-current and left-hand field-equation gates",
            "obstruction": "needs parent action schema acceptance or deeper quotient derivation",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def source_prefactor_classification() -> list[dict[str, str]]:
    return [
        {
            "class_id": "SPC955_0_absent_slot",
            "prefactor_type": "no w_A in parent action",
            "mathematical_form": "partial S_matter/partial w_A undefined because w_A is not an argument",
            "status": "desired_minimal_schema",
            "effect_on_source": "T_source=T_total",
            "test_policy": "zero_theorem_only_if_parent_signed",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "class_id": "SPC955_1_common_mode",
            "prefactor_type": "single common matter prefactor",
            "mathematical_form": "w_A=w_common for all A",
            "status": "calibration_mode",
            "effect_on_source": "absorbed into measured G_ref/kappa_univ",
            "test_policy": "not a WEP residual by itself",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "class_id": "SPC955_2_relative_species_weight",
            "prefactor_type": "relative source prefactor",
            "mathematical_form": "w_A=w_common(1+epsilon_A), epsilon_A != epsilon_B",
            "status": "live_countermodel",
            "effect_on_source": "composition/source-normalization residual",
            "test_policy": "must be bounded or parent-forbidden",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "class_id": "SPC955_3_hidden_marker_weight",
            "prefactor_type": "marker/domain/boundary/post-readout disguised prefactor",
            "mathematical_form": "w_A=w(m,D,boundary,A)",
            "status": "hidden_spurion_channel",
            "effect_on_source": "can reopen source charge after apparent label-forgetting",
            "test_policy": "must be killed by no-spurion theorem or retained in residual vector",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "class_id": "SPC955_4_nonHilbert_weight",
            "prefactor_type": "non-Hilbert current coefficient",
            "mathematical_form": "J_src=kappa T_Hilbert + zeta_A J_NH,A",
            "status": "parallel_open_gate",
            "effect_on_source": "bypasses Hilbert-current uniqueness theorem",
            "test_policy": "separate non-Hilbert current gate required",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def residual_input_schema() -> list[dict[str, str]]:
    return [
        {
            "input_id": "RIS955_0_epsilon_vector",
            "input_name": "epsilon_A vector or beta_source_normalized",
            "required_for": "species-weight residual prediction",
            "required_fields": "value;units;species_basis;source_path;source_row_id;derivation_status;valid_for_claim_policy",
            "current_value": "MISSING_PARENT_INPUT",
            "status": "missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "RIS955_1_composition_projection",
            "input_name": "composition sensitivity projection",
            "required_for": "map epsilon_A to WEP/source observable",
            "required_fields": "projection_formula;source_body;test_body_pair;sensitivity_weights;source_path",
            "current_value": "MISSING_ARENA_PROJECTION",
            "status": "missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "RIS955_2_clock_projection",
            "input_name": "alpha/time product projection",
            "required_for": "clock alpha drift residual",
            "required_fields": "kappa_alpha;tau_clock_or_time_residual;units;source_path;bound_link",
            "current_value": "MISSING_CLOCK_PROJECTION",
            "status": "missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "RIS955_3_zero_theorem_switch",
            "input_name": "parent-signed no-source-prefactor theorem",
            "required_for": "zero route instead of finite residual",
            "required_fields": "theorem_id;source_path;parent_signature_status;covered_hidden_channels",
            "current_value": "MISSING_PARENT_THEOREM",
            "status": "missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def species_weight_residual_runner() -> list[dict[str, str]]:
    rows = []
    for source in read_csv(OUT / "P8_Y5_R10_954_SOURCE_FUNCTOR_BOUND_TARGETS.csv"):
        prediction_raw = source["candidate_prediction"]
        bound_raw = source["comparison_bound"]
        units = source["units"]
        prediction = parse_float(prediction_raw)
        bound = parse_float(bound_raw)
        source_path_value = source["candidate_source_path"]
        has_source = bool(source_path_value) and not source_path_value.startswith("MISSING") and (ROOT / source_path_value).exists()
        if prediction is None:
            verdict = "REJECTED_MISSING_PARENT_INPUT"
            accepted = False
            pass_bound = False
        elif units == "boolean":
            verdict = "BOOLEAN_ZERO_ROUTE_REQUIRES_PARENT_THEOREM"
            accepted = False
            pass_bound = False
        elif bound is None or bound <= 0.0:
            verdict = "REJECTED_BAD_BOUND"
            accepted = False
            pass_bound = False
        elif not has_source:
            verdict = "REJECTED_MISSING_SOURCE_PATH"
            accepted = False
            pass_bound = False
        else:
            pass_bound = abs(prediction) <= bound
            accepted = True
            verdict = "PASS_BOUND_NONCLAIM" if pass_bound else "FAIL_BOUND"
        rows.append(
            {
                "run_id": source["bound_id"].replace("SCB954", "SWR955"),
                "coefficient_symbol": source["coefficient_symbol"],
                "arena": source["arena"],
                "countermodel_parameter": source["countermodel_parameter"],
                "prediction": prediction_raw,
                "prediction_abs": "" if prediction is None else f"{abs(prediction):.12e}",
                "comparison_bound": bound_raw,
                "units": units,
                "candidate_source_path": source_path_value,
                "source_path_exists": flag(has_source),
                "accepted_for_scoring": flag(accepted),
                "pass_bound": flag(pass_bound),
                "verdict": verdict,
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def decisions() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC955_0_lemma",
            "topic": "minimal matter action lemma",
            "result": "conditional_contract_not_parent_derivation",
            "reason": "same-action/total-variation logic is clean, but relative constant prefactors are not excluded by Ward symmetry alone",
            "next_action": "either sign the minimal parent action schema or derive it from a deeper quotient/no-extra-slot principle",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC955_1_common_mode",
            "topic": "common prefactor",
            "result": "harmless_after_calibration",
            "reason": "a single common matter prefactor rescales measured kappa/G and does not create relative WEP source charge",
            "next_action": "keep common mode separate from relative species residuals",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC955_2_relative_mode",
            "topic": "relative species prefactor",
            "result": "live_residual_if_parent_schema_unsigned",
            "reason": "w_A/w_B survives covariance/additivity and maps to source-normalization/WEP channels",
            "next_action": "do not claim local-GR source closure unless relative mode is parent-forbidden or bounded with sourced inputs",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC955_3_runner",
            "topic": "species-weight residual runner",
            "result": "strict_runner_written_all_rows_rejected_missing_inputs",
            "reason": "runner will score only numeric sourced predictions against positive bounds; current predictions remain MISSING_PARENT_INPUT",
            "next_action": "feed real parent coefficient rows or move to source-side spine consolidation",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gates() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE955_0_no_source_prefactors",
            "claim": "minimal parent matter action forbids relative species source prefactors",
            "required_condition": "parent-signed no-extra-source-slot/no-prefactor theorem",
            "current_evidence": "conditional schema lemma only",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE955_1_species_weight_bound",
            "claim": "relative species source weights are below empirical bounds",
            "required_condition": "numeric sourced epsilon/beta prediction and arena projection",
            "current_evidence": "strict runner rejects every row as missing input",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE955_2_source_side_GR_Newton",
            "claim": "source side of local GR/Newton limit is closed",
            "required_condition": "953 theorem plus 954/955 parent schema signed plus hidden-current gates closed",
            "current_evidence": "source-side theorem skeleton is sharp but unsigned",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target() -> list[dict[str, str]]:
    return [
        {
            "next_target": "956-Y5-R10-source-side-GR-reduction-spine-and-left-hand-EH-gate-map.md",
            "objective": "consolidate the conditional source-side GR/Newton reduction spine and map the remaining left-hand EH/Newton and hidden-current gates without promoting a claim",
            "include": "953 no-species theorem, 954 label-forgetting contract, 955 minimal matter lemma, common kappa calibration, hidden-current gates, EH/Newton left-hand gates",
            "exclude": "invented coefficients, local-GR claim, GitHub action, formalization-workbench edits",
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
    classification_rows: list[dict[str, str]],
    input_rows: list[dict[str, str]],
    runner_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    def add(check_id: str, passes: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passes else "fail", "detail": detail, "generated_utc": stamp()})

    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    prior_clean = all(row.get("result") == "pass" for row in read_csv(OUT / "P8_Y5_BRR545_954_VALIDATION.csv"))
    lemma_contract = any(row["lemma_id"] == "MMA955_6_verdict" and row["status"] == "exact_lemma_contract_not_parent_derivation" for row in lemma_rows)
    common_mode_classified = any(row["class_id"] == "SPC955_1_common_mode" and row["status"] == "calibration_mode" for row in classification_rows)
    relative_mode_live = any(row["class_id"] == "SPC955_2_relative_species_weight" and row["status"] == "live_countermodel" for row in classification_rows)
    input_schema_missing = len(input_rows) == 4 and all(row["status"] == "missing" for row in input_rows)
    runner_rejects_missing = len(runner_rows) == 5 and all(row["accepted_for_scoring"] == "false" and row["claim_allowed"] == "false" for row in runner_rows)
    runner_verdicts_strict = all(row["verdict"].startswith("REJECTED") or row["verdict"].startswith("BOOLEAN_ZERO_ROUTE") for row in runner_rows)
    decisions_nonclaim = all(row["claim_allowed"] == "false" for row in decision_rows)
    claim_gates_false = all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claim_rows)
    target_selected = bool(target_rows) and target_rows[0]["next_target"].startswith("956-")
    valid_for_claim_false = all(
        row.get("valid_for_claim") == "false"
        for table in [sources, lemma_rows, classification_rows, input_rows, runner_rows, decision_rows, claim_rows, target_rows]
        for row in table
    )
    formalization_changed = formalization_changed_after_start()

    add("V955_0_sources_exist_and_needles", sources_ok, "all 955 source paths exist and needles are present" if sources_ok else "missing source path or needle")
    add("V955_1_prior_954_clean", prior_clean, "P8_Y5_BRR545_954_VALIDATION.csv clean")
    add("V955_2_minimal_lemma_contract_written", lemma_contract, "minimal matter action lemma written as exact contract, not claim")
    add("V955_3_common_mode_classified", common_mode_classified, "common prefactor classified as calibration mode")
    add("V955_4_relative_mode_live", relative_mode_live, "relative species prefactor remains live residual")
    add("V955_5_input_schema_missing", input_schema_missing, "all residual inputs explicitly marked missing")
    add("V955_6_runner_rejects_missing_predictions", runner_rejects_missing, "strict runner rejects all rows without sourced predictions")
    add("V955_7_runner_verdicts_strict", runner_verdicts_strict, "runner emits only rejected/blocked verdicts")
    add("V955_8_decisions_nonclaim", decisions_nonclaim, "decision ledger remains nonclaim")
    add("V955_9_claim_gates_false", claim_gates_false, "all claim gates remain false")
    add("V955_10_next_target_selected", target_selected, "956 source-side spine and EH gate map selected")
    add("V955_11_no_claims_promoted", valid_for_claim_false, "all generated rows are valid_for_claim=false")
    add("V955_12_formalization_workbench_untouched", formalization_changed == 0, f"formalization_changed_after_start={formalization_changed}")
    add("V955_13_validation_rows_ready", True, "validation table constructed")
    return rows


def write_doc(
    sources: list[dict[str, str]],
    lemma_rows: list[dict[str, str]],
    classification_rows: list[dict[str, str]],
    input_rows: list[dict[str, str]],
    runner_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    doc = f"""# 955 Y5 R10: Minimal Matter Action Source-Coupling Lemma Or Species-Weight Residual Runner

Status: `Y5_R10_955_minimal_matter_action_lemma_contract_written_species_weight_runner_blocks_missing_inputs_nonclaim`

Claim ceiling: `conditional_source_side_contract_only_no_parent_signature_no_species_weight_bound_no_GR_Newton_claim`

## Result

This checkpoint sharpens the coupling problem again.

The best derivation path is now the minimal matter action lemma: matter equations and active source must come from the same total matter functional on one observed coframe, with no extra source-only species prefactor slots. Then total Hilbert variation gives the ordinary source `T_total`, and 953 supplies the one-`kappa_univ` uniqueness step.

But this is still not an unconditional theorem. A relative constant prefactor `w_A` multiplying a species action survives Ward symmetry, covariance, and additivity. A single common prefactor is harmless after measured-`G` calibration; relative prefactors are the live danger.

So 955 leaves us in a better position: the source-side GR/Newton path is now a precise conditional spine, and the fallback residual runner refuses to score anything until real parent coefficients and arena projections exist.

```text
good route: same action + no source-only slots + total Hilbert variation;
bad goblin: relative w_A/w_B;
runner verdict: all residual rows blocked until sourced predictions exist.
```

## Source Register

{md_table(sources, ["source_id", "role", "exists", "needle_found", "path"])}

## Minimal Matter Action Lemma

{md_table(lemma_rows, ["lemma_id", "claim_shape", "status", "would_prove", "obstruction", "parent_signed"])}

## Source Prefactor Classification

{md_table(classification_rows, ["class_id", "prefactor_type", "status", "effect_on_source", "test_policy"])}

## Residual Input Schema

{md_table(input_rows, ["input_id", "input_name", "required_for", "current_value", "status"])}

## Species-Weight Residual Runner

{md_table(runner_rows, ["run_id", "coefficient_symbol", "arena", "prediction", "comparison_bound", "accepted_for_scoring", "pass_bound", "verdict"])}

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
    lemma_rows = minimal_matter_action_lemma()
    classification_rows = source_prefactor_classification()
    input_rows = residual_input_schema()
    runner_rows = species_weight_residual_runner()
    decision_rows = decisions()
    claim_rows = claim_gates()
    target_rows = next_target()
    validation_rows = validation(sources, lemma_rows, classification_rows, input_rows, runner_rows, decision_rows, claim_rows, target_rows)

    write_csv(
        OUT / "P8_Y5_R10_955_SOURCE_REGISTER.csv",
        sources,
        ["source_id", "path", "role", "needle", "absolute_path", "exists", "needle_found", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv",
        lemma_rows,
        [
            "lemma_id",
            "claim_shape",
            "mathematical_form",
            "status",
            "would_prove",
            "obstruction",
            "parent_signed",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_955_SOURCE_PREFACTOR_CLASSIFICATION.csv",
        classification_rows,
        [
            "class_id",
            "prefactor_type",
            "mathematical_form",
            "status",
            "effect_on_source",
            "test_policy",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_955_RESIDUAL_INPUT_SCHEMA.csv",
        input_rows,
        [
            "input_id",
            "input_name",
            "required_for",
            "required_fields",
            "current_value",
            "status",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_955_SPECIES_WEIGHT_RESIDUAL_RUNNER.csv",
        runner_rows,
        [
            "run_id",
            "coefficient_symbol",
            "arena",
            "countermodel_parameter",
            "prediction",
            "prediction_abs",
            "comparison_bound",
            "units",
            "candidate_source_path",
            "source_path_exists",
            "accepted_for_scoring",
            "pass_bound",
            "verdict",
            "claim_allowed",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_955_DECISION_LEDGER.csv",
        decision_rows,
        ["decision_id", "topic", "result", "reason", "next_action", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_955_CLAIM_GATE.csv",
        claim_rows,
        ["gate_id", "claim", "required_condition", "current_evidence", "gate_pass", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_955_NEXT_TARGET.csv",
        target_rows,
        ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_BRR545_955_VALIDATION.csv",
        validation_rows,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_doc(sources, lemma_rows, classification_rows, input_rows, runner_rows, decision_rows, claim_rows, target_rows, validation_rows)


if __name__ == "__main__":
    main()

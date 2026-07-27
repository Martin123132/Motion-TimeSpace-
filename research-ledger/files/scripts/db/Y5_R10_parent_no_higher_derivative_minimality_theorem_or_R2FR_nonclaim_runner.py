from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "964-Y5-R10-parent-no-higher-derivative-minimality-theorem-or-R2FR-nonclaim-runner.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


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


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return -1
    since = SCRIPT_START_UTC.astimezone().strftime("%Y-%m-%dT%H:%M:%S")
    literal = str(FORMALIZATION).replace("'", "''")
    command = (
        "$since=[datetime]::Parse('"
        + since
        + "'); "
        + "$count=(Get-ChildItem -LiteralPath '"
        + literal
        + "' -Recurse -File | Where-Object { $_.LastWriteTime -gt $since } | Measure-Object).Count; "
        + "Write-Output $count"
    )
    completed = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )
    try:
        return int(completed.stdout.strip().splitlines()[-1])
    except (IndexError, ValueError):
        return -2


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "963_doc",
            "path": "963-Y5-R10-parent-second-order-signature-or-R2FR-bound-runner.md",
            "role": "handoff: parent second-order signature failed and runner spec written",
            "needle": "DO963_6_verdict",
        },
        {
            "source_id": "963_runner_spec",
            "path": "source-intake/mts_residuals/P8_Y5_R10_963_R2FR_BOUND_RUNNER_SPEC.csv",
            "role": "R2/fR runner spec with missing-input gates",
            "needle": "R2RUN963_4_decision_logic",
        },
        {
            "source_id": "962_proof",
            "path": "source-intake/mts_residuals/P8_Y5_R10_962_R2FR_ZERO_PROOF_ATTEMPT.csv",
            "role": "relative theorem that P6 activates",
            "needle": "RELATIVE_THEOREM_PROVEN_PARENT_PREMISE_UNSIGNED",
        },
        {
            "source_id": "440_second_order",
            "path": "440-metric-only-second-order-sector-reduction-attempt.md",
            "role": "metric-only second-order sector counterchecks",
            "needle": "integrating out a field can create f(R), R^2, Yukawa, or nonlocal terms",
        },
        {
            "source_id": "439_premise_ladder",
            "path": "439-EH-only-exterior-parent-premise-ladder.md",
            "role": "P6 second-order parent blocker",
            "needle": "V6_second_order_restriction",
        },
        {
            "source_id": "423_minimality",
            "path": "423-parent-action-minimality-no-extension-theorem-attempt.md",
            "role": "minimality/no-extension theorem failure source",
            "needle": "parent_universal_property_derived",
        },
        {
            "source_id": "413_no_marker",
            "path": "413-no-marker-parent-action-theorem-attempt.md",
            "role": "marker-extension counterexample source",
            "needle": "co_moving_material_marker",
        },
        {
            "source_id": "710_scalar_descent",
            "path": "710-Y5-R10-scalar-class-zero-premise-parent-action-clause-or-frame-transfer-guard.md",
            "role": "scalar no-prefactor/no-kinetic candidate clauses",
            "needle": "DPC710_4_no_local_kinetic_mode",
        },
        {
            "source_id": "R11_executable",
            "path": "source-intake/mts_residuals/R11_nonEH_operator_vector_executable.csv",
            "role": "R2/fR retained-row source",
            "needle": "R2_fR_scalar_mode",
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


def minimality_theorem_attempt() -> list[dict[str, str]]:
    return [
        {
            "attempt_id": "MIN964_0_target",
            "theorem_piece": "parent no-higher-derivative minimality theorem",
            "would_need_to_show": "the primitive MTS quotient admits no local curvature-squared, f(R), marker-scalar, or integrated-out higher-curvature tower in the ordinary compact exterior",
            "current_evidence": "963 identifies the exact activator; 439/440/423 show it is not parent-signed",
            "status": "target_defined_not_proven",
            "why_not_closed": "minimality/no-extension is not derived from a universal property of the parent object",
            "consequence": "does not activate the 962 R2/fR zero theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "MIN964_1_primitive_quotient",
            "theorem_piece": "Q_MTS is a primitive minimal quotient object",
            "would_need_to_show": "every parent-action argument is generated by motion, time, space, observed metric/coframe, and universal constants; no extra natural marker functor exists",
            "current_evidence": "423 says parent_universal_property_derived=fail and local_invariant_algebra_triviality_derived=fail",
            "status": "not_derived",
            "why_not_closed": "a legal extended quotient can still append covariant material/invariant marker variables",
            "consequence": "extra scalar generators can remain legal",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "MIN964_2_no_integrated_out_tower",
            "theorem_piece": "integrating out hidden sectors cannot generate f(R)/R^2",
            "would_need_to_show": "solved auxiliary, projector, memory, or scalar sectors contribute no Delta S_eff[g] with higher curvature, nonlocal kernel, or finite scalar pole",
            "current_evidence": "440 explicitly lists integrated-out f(R), R^2, Yukawa, and nonlocal terms as central-open hazards",
            "status": "not_derived",
            "why_not_closed": "E_A=0 or a large mass is not enough unless source/readout and metric variation vanish",
            "consequence": "R2/fR can re-enter after reduction even if not written in the primitive ansatz",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "MIN964_3_Ostrogradsky_regular",
            "theorem_piece": "regularity/stability forbids higher derivatives",
            "would_need_to_show": "parent variational principle rejects higher-derivative branches by a derived constraint, not by preference",
            "current_evidence": "current corpus has a stability intuition but no constraint algebra excluding R2/fR while allowing EH",
            "status": "insufficient_as_theorem",
            "why_not_closed": "R^2/f(R) can be recast as a scalar-tensor theory, so simple derivative-order distaste is not a mathematical exclusion",
            "consequence": "stability is a guide, not a zero certificate",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "MIN964_4_descent_signature",
            "theorem_piece": "scalar/class action descent",
            "would_need_to_show": "no scalar/class R-prefactor, no local kinetic scalar, matter functor blindness, and Ward ownership are parent-derived",
            "current_evidence": "710 provides candidate clauses DPC710_1..DPC710_8 but marks them not parent-signed",
            "status": "candidate_clause_only",
            "why_not_closed": "quotient geometry has not yet forced scalar/class labels to be readout-only and stressless",
            "consequence": "scalar-tensor/f(R)-like leakage remains retained",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "MIN964_5_verdict",
            "theorem_piece": "activate 962 c_R2=c_fR zero theorem",
            "would_need_to_show": "MIN964_1 through MIN964_4 all pass",
            "current_evidence": "all decisive pieces are not_derived/candidate/insufficient",
            "status": "THEOREM_NOT_PROVEN_CURRENT_CORPUS",
            "why_not_closed": "countermodels remain legal unless minimality/no-extension is strengthened",
            "consequence": "must either keep deriving minimality or use nonclaim runner for finite scalar branch",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def countermodel_ledger() -> list[dict[str, str]]:
    return [
        {
            "counter_id": "CM964_0_EH_plus_R2",
            "countermodel": "S = S_EH + epsilon int sqrt(-g) R^2",
            "why_legal_without_gate": "local, 4D, diffeo-invariant, metric-only, same observed frame, and Ward-compatible",
            "damage": "adds scalar trace pole/fourth-order metric equation unless epsilon=0 or decoupled",
            "gate_that_kills_it": "P6 no-higher-derivative/minimality theorem",
            "currently_killed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "counter_id": "CM964_1_auxiliary_scalar_integrated_out",
            "countermodel": "S = S_EH + int sqrt(-g)[-1/2 M^2 phi^2 + beta phi R]",
            "why_legal_without_gate": "auxiliary scalar can look nonpropagating before solving its equation",
            "damage": "solving phi ~ beta R/M^2 generates beta^2 R^2/(2M^2)",
            "gate_that_kills_it": "no integrated-out curvature tower certificate",
            "currently_killed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "counter_id": "CM964_2_marker_prefactor",
            "countermodel": "S = int sqrt(-g) F(sigma_marker) R + S_sigma",
            "why_legal_without_gate": "a covariant marker or quotient-invariant scalar can be appended unless no-extension is proven",
            "damage": "scalar-tensor/f(R)-like PPN, WEP, clock, and R10 leakage",
            "gate_that_kills_it": "primitive quotient no-natural-marker functor theorem",
            "currently_killed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "counter_id": "CM964_3_nonlocal_memory_kernel",
            "countermodel": "S = S_EH + int sqrt(-g) R Box^{-1} R or compact memory kernel",
            "why_legal_without_gate": "history/memory language can be covariant and source-owned if not explicitly forbidden",
            "damage": "nonlocal scalar response can mimic finite-range or time-varying source normalization",
            "gate_that_kills_it": "locality plus no integrated-out nonlocal kernel theorem",
            "currently_killed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "counter_id": "CM964_4_topological_safe_case",
            "countermodel": "4D Gauss-Bonnet exact topological/boundary combination",
            "why_legal_without_gate": "allowed as harmless only if exact combination and boundary flux are controlled",
            "damage": "safe case, but does not rescue generic R2/fR row",
            "gate_that_kills_it": "topological zero-local-variation certificate",
            "currently_killed": "conditional_safe_not_current_row",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def r2fr_input_template() -> list[dict[str, str]]:
    return [
        {
            "input_id": "R2IN964_0_mts_prediction_required",
            "row_type": "mts_prediction",
            "model_id": "MTS_R2FR_candidate",
            "coefficient_value": "MISSING_PARENT_INPUT",
            "coefficient_units": "MISSING_UNITS",
            "alpha_predicted": "MISSING_ALPHA",
            "lambda_predicted_um": "MISSING_LAMBDA",
            "mass_eV": "MISSING_MASS",
            "screening_flag": "MISSING_SCREENING_STATUS",
            "source_file": "MISSING_SOURCE_FILE",
            "extraction_method": "parent_or_closure_not_supplied",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "R2IN964_1_zero_theorem_switch",
            "row_type": "zero_theorem",
            "model_id": "MTS_R2FR_zero_route",
            "coefficient_value": "0_if_parent_signed_else_MISSING",
            "coefficient_units": "not_applicable_if_zero",
            "alpha_predicted": "0_if_parent_signed_else_MISSING",
            "lambda_predicted_um": "not_applicable_if_zero",
            "mass_eV": "infinite_if_parent_signed",
            "screening_flag": "not_applicable_if_zero",
            "source_file": "962_relative_theorem_plus_964_minimality_signature",
            "extraction_method": "theorem_zero_requires_parent_signature",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "R2IN964_2_Lee2020_anchor",
            "row_type": "bound_anchor",
            "model_id": "external_bound_anchor",
            "coefficient_value": "not_applicable",
            "coefficient_units": "not_applicable",
            "alpha_predicted": "not_applicable",
            "lambda_predicted_um": "38.6",
            "mass_eV": "0.0051121",
            "screening_flag": "not_applicable",
            "source_file": "https://arxiv.org/abs/2002.11761",
            "extraction_method": "anchor_only_non_curve",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "R2IN964_3_full_curve_required",
            "row_type": "bound_curve",
            "model_id": "external_full_curve_required",
            "coefficient_value": "not_applicable",
            "coefficient_units": "not_applicable",
            "alpha_predicted": "not_applicable",
            "lambda_predicted_um": "MISSING_DIGITIZED_CURVE",
            "mass_eV": "MISSING_DIGITIZED_CURVE",
            "screening_flag": "not_applicable",
            "source_file": "MISSING_FULL_CURVE_SOURCE_EXTRACTION",
            "extraction_method": "full_curve_required_for_claim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def has_missing(value: str) -> bool:
    return value == "" or "MISSING" in value or value.startswith("0_if_parent_signed_else")


def r2fr_nonclaim_runner_result(template_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    for row in template_rows:
        missing_fields = [
            field
            for field in [
                "coefficient_value",
                "coefficient_units",
                "alpha_predicted",
                "lambda_predicted_um",
                "mass_eV",
                "screening_flag",
                "source_file",
            ]
            if has_missing(row[field])
        ]
        anchor_only = row["extraction_method"] == "anchor_only_non_curve"
        zero_requires_signature = row["extraction_method"] == "theorem_zero_requires_parent_signature"
        accepted = not missing_fields and not anchor_only and not zero_requires_signature and row["valid_for_claim"] == "true"
        if zero_requires_signature:
            verdict = "REJECTED_ZERO_THEOREM_NOT_PARENT_SIGNED"
        elif anchor_only:
            verdict = "REJECTED_ANCHOR_ONLY_NON_CURVE"
        elif missing_fields:
            verdict = "REJECTED_MISSING_PARENT_OR_BOUND_INPUTS"
        elif row["valid_for_claim"] != "true":
            verdict = "REJECTED_VALID_FOR_CLAIM_FALSE"
        else:
            verdict = "ACCEPTED_FOR_SCORING"
        rows.append(
            {
                "run_id": row["input_id"].replace("R2IN", "R2RUN"),
                "input_id": row["input_id"],
                "row_type": row["row_type"],
                "accepted_for_scoring": flag(accepted),
                "claim_allowed": "false",
                "verdict": verdict,
                "missing_fields": ";".join(missing_fields) if missing_fields else "none",
                "reason": "strict nonclaim runner: no pass without parent-signed zero theorem or complete numeric prediction plus valid full bound curve",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    rows.append(
        {
            "run_id": "R2RUN964_VERDICT",
            "input_id": "all_rows",
            "row_type": "runner_verdict",
            "accepted_for_scoring": "false",
            "claim_allowed": "false",
            "verdict": "R2FR_BRANCH_BLOCKED_NONCLAIM",
            "missing_fields": "parent_zero_signature_or_numeric_prediction_and_full_curve",
            "reason": "no theorem-zero and no scoreable finite scalar branch currently exists",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    )
    return rows


def claim_gates() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE964_0_minimality_theorem",
            "claim": "parent no-higher-derivative/minimality theorem is proven",
            "required_condition": "primitive quotient minimality, no natural marker functor, no integrated-out curvature tower, and no scalar descent leakage all proven",
            "current_evidence": "theorem attempt fails at all decisive clauses",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE964_1_R2FR_zero",
            "claim": "c_R2=c_fR=0 in MTS",
            "required_condition": "964 minimality theorem activates 962 relative theorem",
            "current_evidence": "964 minimality theorem not proven",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE964_2_runner_scoring",
            "claim": "finite R2/fR branch can be scored",
            "required_condition": "complete MTS alpha/lambda prediction and valid full alpha(lambda) curve or PPN projection",
            "current_evidence": "runner rejects all rows as missing/anchor-only/nonclaim",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE964_3_local_GR",
            "claim": "local GR/Newton branch promotes",
            "required_condition": "R2/fR zero or bound plus connection/source/PPN gates",
            "current_evidence": "R2/fR remains blocked; connection/source gates remain outside this checkpoint",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decisions() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC964_0_theorem_result",
            "topic": "no-higher-derivative/minimality theorem",
            "result": "not_proven",
            "reason": "EH+R2, auxiliary scalar integrated-out, marker-prefactor, and nonlocal memory countermodels remain legal without stronger parent minimality",
            "next_action": "try the primitive quotient/no-natural-marker theorem directly or accept R2/fR as retained residual",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC964_1_runner_result",
            "topic": "R2/fR nonclaim runner",
            "result": "runner_shell_strictly_rejects_current_inputs",
            "reason": "all current rows are parent-missing, zero-theorem-unsigned, anchor-only, or full-curve-missing",
            "next_action": "only run scoring after either parent zero theorem or real finite scalar prediction plus full curve exists",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC964_2_best_next",
            "topic": "next hinge",
            "result": "decide_minimality_vs_connection",
            "reason": "R2/fR is boxed but blocked by primitive minimality; connection/torsion is the other big EH gate",
            "next_action": "best derivation route is now primitive quotient/no-natural-marker theorem; pragmatic route is R2/fR full-curve/nonclaim runner",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target() -> list[dict[str, str]]:
    return [
        {
            "next_target": "965-Y5-R10-primitive-quotient-no-natural-marker-theorem-or-R2FR-full-curve-intake.md",
            "objective": "try to prove the primitive quotient/no-natural-marker theorem that would forbid scalar/marker extensions; if it fails, start full-curve R10 intake for the retained R2/fR branch without making a claim",
            "include": "universal property; local invariant algebra triviality; marker countermodels; scalar extension kill condition; optional Lee2020 full-curve extraction manifest",
            "exclude": "EH/local-GR claim, torsion full proof unless selected next, invented coefficients, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def validation(
    sources: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
    counter_rows: list[dict[str, str]],
    template_rows: list[dict[str, str]],
    runner_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    theorem_not_proven = any(row["attempt_id"] == "MIN964_5_verdict" and row["status"] == "THEOREM_NOT_PROVEN_CURRENT_CORPUS" for row in theorem_rows)
    countermodels_live = all(row["currently_killed"] in {"false", "conditional_safe_not_current_row"} for row in counter_rows)
    template_nonclaim = all(row["valid_for_claim"] == "false" for row in template_rows)
    runner_rejects = all(row["accepted_for_scoring"] == "false" and row["claim_allowed"] == "false" for row in runner_rows)
    claim_gates_false = all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claim_rows)
    no_formalization_edits = formalization_changed_after_start() == 0
    outputs_inside_root = all(
        str(path.resolve()).startswith(str(ROOT.resolve()))
        for path in [
            DOC,
            OUT / "P8_Y5_R10_964_SOURCE_REGISTER.csv",
            OUT / "P8_Y5_R10_964_MINIMALITY_THEOREM_ATTEMPT.csv",
            OUT / "P8_Y5_R10_964_COUNTERMODEL_LEDGER.csv",
            OUT / "P8_Y5_R10_964_R2FR_NONCLAIM_INPUT_TEMPLATE.csv",
            OUT / "P8_Y5_R10_964_R2FR_NONCLAIM_RUNNER_RESULT.csv",
            OUT / "P8_Y5_R10_964_CLAIM_GATE.csv",
            OUT / "P8_Y5_R10_964_DECISION_LEDGER.csv",
            OUT / "P8_Y5_R10_964_NEXT_TARGET.csv",
            OUT / "P8_Y5_BRR545_964_VALIDATION.csv",
        ]
    )
    checks = [
        ("V964_0_sources_checked", sources_ok, "all cited local source paths exist and needles were found"),
        ("V964_1_theorem_not_proven", theorem_not_proven, "minimality/no-higher-derivative theorem remains unproven"),
        ("V964_2_countermodels_live", countermodels_live, "countermodels remain live or conditionally safe only"),
        ("V964_3_template_nonclaim", template_nonclaim, "all input template rows valid_for_claim=false"),
        ("V964_4_runner_rejects_all", runner_rejects, "strict runner rejects all current rows and permits no claim"),
        ("V964_5_claim_gates_false", claim_gates_false, "claim gates all false"),
        ("V964_6_decisions_ready", len(decision_rows) == 3, "decision ledger has three rows"),
        ("V964_7_next_target_ready", len(target_rows) == 1, "next target row written"),
        ("V964_8_formalization_untouched", no_formalization_edits, "formalization-workbench modified-file count since script start is zero"),
        ("V964_9_outputs_inside_post_checkpoint", outputs_inside_root, "all outputs resolve inside post-checkpoint-work"),
    ]
    rows = [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "generated_utc": stamp(),
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "V964_10_validation_rows_ready",
            "result": "pass" if all(row["result"] == "pass" for row in rows) else "fail",
            "detail": "964 validation pack assembled",
            "generated_utc": stamp(),
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
    counter_rows: list[dict[str, str]],
    template_rows: list[dict[str, str]],
    runner_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    doc = f"""# 964 Y5 R10: Parent No-Higher-Derivative Minimality Theorem Or R2/fR Nonclaim Runner

Status: `Y5_R10_964_minimality_theorem_not_proven_R2FR_nonclaim_runner_rejects_current_inputs`

Claim ceiling: no parent minimality theorem, R2/fR zero, R10 pass, PPN pass, EH, Newton, measured-GM, or local-GR claim is made.

## Readout

The best derivation shot was taken and it does not close yet. To activate the 962 theorem, MTS needs a parent no-higher-derivative/minimality theorem: no natural marker functor, no scalar/class extension, and no integrated-out sector that regenerates `R^2`, `f(R)`, or a scalaron.

Current corpus does not prove that. Countermodels like `EH + epsilon R^2`, an auxiliary scalar that integrates out to `R^2`, and marker-prefactor `F(sigma)R` remain legal unless the primitive quotient/minimality theorem is strengthened.

The practical gain is that the empirical fallback is now safer: the nonclaim runner rejects placeholders, unsigned zero theorems, anchor-only bounds, and missing full-curve data. No little gremlin can sneak a “pass” through the side door.

## Source Register

{md_table(sources, ["source_id", "role", "exists", "needle_found", "path"])}

## Minimality Theorem Attempt

{md_table(theorem_rows, ["attempt_id", "theorem_piece", "status", "why_not_closed", "consequence"])}

## Countermodel Ledger

{md_table(counter_rows, ["counter_id", "countermodel", "why_legal_without_gate", "damage", "currently_killed"])}

## R2/fR Nonclaim Input Template

{md_table(template_rows, ["input_id", "row_type", "coefficient_value", "alpha_predicted", "lambda_predicted_um", "source_file", "valid_for_claim"])}

## R2/fR Nonclaim Runner Result

{md_table(runner_rows, ["run_id", "row_type", "accepted_for_scoring", "claim_allowed", "verdict", "missing_fields"])}

## Claim Gate

{md_table(claim_rows, ["gate_id", "claim", "current_evidence", "gate_pass", "claim_allowed"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "topic", "result", "reason", "next_action"])}

## Validation

{md_table(validation_rows, ["check_id", "result", "detail", "generated_utc"])}

## Next Target

{md_table(target_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"])}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    sources = source_register()
    theorem_rows = minimality_theorem_attempt()
    counter_rows = countermodel_ledger()
    template_rows = r2fr_input_template()
    runner_rows = r2fr_nonclaim_runner_result(template_rows)
    claim_rows = claim_gates()
    decision_rows = decisions()
    target_rows = next_target()
    validation_rows = validation(
        sources,
        theorem_rows,
        counter_rows,
        template_rows,
        runner_rows,
        claim_rows,
        decision_rows,
        target_rows,
    )

    write_csv(
        OUT / "P8_Y5_R10_964_SOURCE_REGISTER.csv",
        sources,
        ["source_id", "path", "role", "needle", "absolute_path", "exists", "needle_found", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_964_MINIMALITY_THEOREM_ATTEMPT.csv",
        theorem_rows,
        ["attempt_id", "theorem_piece", "would_need_to_show", "current_evidence", "status", "why_not_closed", "consequence", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_964_COUNTERMODEL_LEDGER.csv",
        counter_rows,
        ["counter_id", "countermodel", "why_legal_without_gate", "damage", "gate_that_kills_it", "currently_killed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_964_R2FR_NONCLAIM_INPUT_TEMPLATE.csv",
        template_rows,
        [
            "input_id",
            "row_type",
            "model_id",
            "coefficient_value",
            "coefficient_units",
            "alpha_predicted",
            "lambda_predicted_um",
            "mass_eV",
            "screening_flag",
            "source_file",
            "extraction_method",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_964_R2FR_NONCLAIM_RUNNER_RESULT.csv",
        runner_rows,
        ["run_id", "input_id", "row_type", "accepted_for_scoring", "claim_allowed", "verdict", "missing_fields", "reason", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_964_CLAIM_GATE.csv",
        claim_rows,
        ["gate_id", "claim", "required_condition", "current_evidence", "gate_pass", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_964_DECISION_LEDGER.csv",
        decision_rows,
        ["decision_id", "topic", "result", "reason", "next_action", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_964_NEXT_TARGET.csv",
        target_rows,
        ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_BRR545_964_VALIDATION.csv",
        validation_rows,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_doc(sources, theorem_rows, counter_rows, template_rows, runner_rows, claim_rows, decision_rows, target_rows, validation_rows)


if __name__ == "__main__":
    main()

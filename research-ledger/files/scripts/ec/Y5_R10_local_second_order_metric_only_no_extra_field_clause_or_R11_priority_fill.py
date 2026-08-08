from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "959-Y5-R10-local-second-order-metric-only-no-extra-field-clause-or-R11-priority-fill.md"
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


def has_missing(value: str) -> bool:
    return value == "" or "MISSING" in value or value.startswith("fill_") or value.startswith("FILL_")


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "958_doc",
            "path": "958-Y5-R10-EH-core-operator-selection-or-executable-R11-nonEH-vector.md",
            "role": "handoff: EH route conditional and R11 vector rejected",
            "needle": "EH route: real but conditional",
        },
        {
            "source_id": "958_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_958_VALIDATION.csv",
            "role": "previous checkpoint validation",
            "needle": "V958_11_validation_rows_ready",
        },
        {
            "source_id": "958_priority",
            "path": "source-intake/mts_residuals/P8_Y5_R10_958_R11_OPERATOR_FAMILY_PRIORITY.csv",
            "role": "R11 priority rows selecting R2/fR and torsion/nonmetricity",
            "needle": "R11PRI958_5",
        },
        {
            "source_id": "958_R11_review",
            "path": "source-intake/mts_residuals/P8_Y5_R10_958_R11_NON_EH_VECTOR_REVIEW.csv",
            "role": "R11 review with non-executable rows",
            "needle": "R11REV958_1",
        },
        {
            "source_id": "506_doc",
            "path": "506-local-EH-reduction-and-extra-sector-silence-theorem.md",
            "role": "positive source-free silence mechanism",
            "needle": "positive source-free operator",
        },
        {
            "source_id": "506_theorem_attempt",
            "path": "source-intake/mts_residuals/P8_LOCAL_EH_REDUCTION_THEOREM_ATTEMPT.csv",
            "role": "EH plus silent reduction theorem attempt",
            "needle": "T506_EH_plus_silent_reduction",
        },
        {
            "source_id": "506_failure_ledger",
            "path": "source-intake/mts_residuals/P8_LOCAL_EH_REDUCTION_FAILURE_LEDGER.csv",
            "role": "local EH failure ledger",
            "needle": "F506_0_positive_operator_missing",
        },
        {
            "source_id": "507_queue",
            "path": "507-field-specific-silence-queue-kappa-domain-memory-motion.md",
            "role": "field-specific silence queue",
            "needle": "field-specific silence queue",
        },
        {
            "source_id": "655_EH_premises",
            "path": "source-intake/mts_residuals/P8_Y5_R10_655_EH_ONLY_PREMISE_AUDIT.csv",
            "role": "EH-only premise audit",
            "needle": "EHP655_P6_second_order",
        },
        {
            "source_id": "R11_executable",
            "path": "source-intake/mts_residuals/R11_nonEH_operator_vector_executable.csv",
            "role": "candidate R11 rows to fill",
            "needle": "R2_fR_scalar_mode",
        },
        {
            "source_id": "R11_missing",
            "path": "source-intake/mts_residuals/R11_MTS_VECTOR_MISSING_FIELD_LEDGER.csv",
            "role": "R11 missing field ledger",
            "needle": "torsion_nonmetricity",
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


def no_extra_field_clause_attempt() -> list[dict[str, str]]:
    return [
        {
            "clause_id": "NEF959_0_target",
            "clause": "local exterior parent branch is metric-only, second-order, and has no surviving extra field",
            "mathematical_form": "Fields_ext = {g_obs}; delta S_ext/delta g gives at most second derivatives; all other Euler sectors vanish/silent",
            "status": "target_from_958",
            "would_close": "EH/Lovelock route for the left-hand operator",
            "blocker": "this is the desired parent clause, not yet its derivation",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "NEF959_1_Lovelock_implication",
            "clause": "if the target clause is parent-signed, EH+Lambda follows as the local operator family",
            "mathematical_form": "local 4D diffeo metric-only second-order E_munu => a G_munu + b g_munu",
            "status": "conditional_mathematics_clean",
            "would_close": "operator side modulo normalization, boundary, and source-measure calibration",
            "blocker": "Lovelock implication cannot be applied until MTS earns the premises",
            "parent_signed": "conditional_only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "NEF959_2_extra_sector_filter",
            "clause": "each non-metric sector must be absent, pure gauge, topological zero-flux, positive source-free silent, or retained",
            "mathematical_form": "DeltaE_extra_i in {0, gauge, topological_no_flux, positive_source_free_silent, retained_R11_i}",
            "status": "exact_filter_from_506",
            "would_close": "prevents extra fields from bypassing EH while preserving bounded fallback route",
            "blocker": "field-specific operators, signs, source charges, and boundary data are not all supplied",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "NEF959_3_R2_fR_obstruction",
            "clause": "R2/f(R) terms violate the second-order metric-only premise unless theorem-zero/topological/redundant",
            "mathematical_form": "sqrt(-g)(c_R2 R^2 + c_fR f_extra(R)) -> extra scalar/fourth-order mode unless c=0 or bounded",
            "status": "priority_residual_family",
            "would_close": "R2/fR scalar-mode R11 family if zeroed or bounded",
            "blocker": "no sourced coefficient, units, weak-field map, or zero certificate",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "NEF959_4_torsion_nonmetricity_obstruction",
            "clause": "independent connection/torsion/nonmetricity violates metric-only Levi-Civita premise unless killed",
            "mathematical_form": "Gamma != LC(g_obs) gives T^2, Q^2, hypermomentum, light/spin/source couplings",
            "status": "priority_residual_family",
            "would_close": "torsion/nonmetricity R11 family if Levi-Civita theorem or bounds exist",
            "blocker": "no parent-derived no-independent-connection theorem or executable coefficient map",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "NEF959_5_verdict",
            "clause": "local second-order metric-only no-extra-field clause",
            "mathematical_form": "NEF959_0 + NEF959_2 => EH route; else fill prioritized R11 rows",
            "status": "not_parent_derived_current_corpus",
            "would_close": "EH operator selection if parent-signed",
            "blocker": "currently must proceed to R2/fR and torsion/nonmetricity zero-or-bound rows",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def silence_mechanism_requirements() -> list[dict[str, str]]:
    return [
        {
            "requirement_id": "SMR959_0_operator",
            "requirement": "field-specific Euler operator is explicitly written",
            "mathematical_form": "L_i phi_i = source_i",
            "needed_for": "decide whether sector is positive, gauge, topological, or retained",
            "current_status": "missing_for_priority_families",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "requirement_id": "SMR959_1_sign",
            "requirement": "operator has positive/self-adjoint source-free energy identity or topological zero-variation",
            "mathematical_form": "int <phi,L phi> = positive_norm + boundary_flux",
            "needed_for": "no-hair/silence theorem",
            "current_status": "not_supplied_for_R2_fR_or_torsion",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "requirement_id": "SMR959_2_source_charge",
            "requirement": "compact local exterior source/current charge vanishes",
            "mathematical_form": "source_i=0 outside W",
            "needed_for": "field cannot carry fifth-force/radial/source hair",
            "current_status": "not_supplied",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "requirement_id": "SMR959_3_boundary_flux",
            "requirement": "linking-sphere and boundary fluxes vanish or are fixed harmless reference terms",
            "mathematical_form": "boundary_flux_i=0 or background_constant",
            "needed_for": "divergence/topological terms do not become observable mass/PPN shifts",
            "current_status": "not_supplied",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "requirement_id": "SMR959_4_retained_vector",
            "requirement": "if any clause fails, retained R11 row has executable coefficient, units, map, source, and assumptions",
            "mathematical_form": "abs(predicted_residual_i)<=bound_i with source-backed row",
            "needed_for": "nonclaim empirical fallback",
            "current_status": "template_rows_only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def r11_priority_fill_template() -> list[dict[str, str]]:
    selected = {"R2_fR_scalar_mode", "torsion_nonmetricity"}
    rows = []
    for row in read_csv(OUT / "R11_nonEH_operator_vector_executable.csv"):
        if row["operator_family"] not in selected:
            continue
        if row["operator_family"] == "R2_fR_scalar_mode":
            required_zero = "derive c_R2=c_fR=0, topological/redundant certificate, or scalar mass/coupling bound"
            first_observable = "gamma/beta/R10 alpha(lambda)/finite-range scalar channel"
        else:
            required_zero = "derive Gamma=LC(g_obs), torsion/nonmetricity zero, or bounded connection coefficients"
            first_observable = "WEP/clocks/light-cone/spin/source-charge/PPN connection channel"
        rows.append(
            {
                "fill_id": f"R11FILL959_{len(rows)}",
                "operator_family": row["operator_family"],
                "coefficient_symbol": row["coefficient_symbol"],
                "required_zero_or_bound": required_zero,
                "candidate_value": row.get("coefficient_value", "MISSING_NUMERIC_OR_DERIVED_ZERO_COEFFICIENT"),
                "candidate_units": row.get("coefficient_units", "MISSING_COEFFICIENT_UNITS"),
                "normalization": row.get("normalization", "MISSING_NORMALIZATION"),
                "weak_field_map": row.get("weak_field_map", "MISSING_WEAK_FIELD_MAP"),
                "predicted_residual_or_bound_source": row.get("predicted_residual_or_bound_source", "MISSING_RESIDUAL_OR_BOUND_SOURCE"),
                "derivation_status": row.get("derivation_status", "MISSING_DERIVATION_STATUS"),
                "source_file": row.get("source_file", "MISSING_SOURCE_FILE"),
                "formula_reference": row.get("formula_reference", "MISSING_FORMULA_REFERENCE"),
                "assumptions": row.get("assumptions", "MISSING_ASSUMPTIONS"),
                "first_observable": first_observable,
                "ready_for_scoring": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def r11_priority_fill_dryrun(fill_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    required = [
        "candidate_value",
        "candidate_units",
        "normalization",
        "weak_field_map",
        "predicted_residual_or_bound_source",
        "derivation_status",
        "source_file",
        "formula_reference",
        "assumptions",
    ]
    rows = []
    for row in fill_rows:
        missing = [field for field in required if has_missing(row.get(field, ""))]
        rows.append(
            {
                "dryrun_id": row["fill_id"].replace("R11FILL959", "R11DRY959"),
                "operator_family": row["operator_family"],
                "missing_fields": ";".join(missing),
                "accepted_for_scoring": flag(not missing),
                "verdict": "READY_FOR_SCORING_NONCLAIM" if not missing else "REJECTED_PRIORITY_FILL_INCOMPLETE",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def decisions() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC959_0_parent_clause",
            "topic": "local second-order metric-only no-extra-field clause",
            "result": "conditional_clause_written_not_parent_signed",
            "reason": "the Lovelock route is clean only if all non-metric/extra sectors are absent, silent, topological, or retained",
            "next_action": "try priority zero/bound fills for R2/fR and torsion/nonmetricity rather than claiming EH",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC959_1_R2_fR",
            "topic": "R2/fR scalar mode",
            "result": "priority_fill_required",
            "reason": "R2/fR is the sharpest second-order blocker and can induce scalar/fourth-order finite-range channels",
            "next_action": "attempt derived-zero/topological/redundant certificate or alpha(lambda)/PPN bound map",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC959_2_torsion_nonmetricity",
            "topic": "torsion/nonmetricity",
            "result": "priority_fill_required",
            "reason": "connection compatibility is a separate EH premise affecting WEP, clocks, light cones, spin, and source charge",
            "next_action": "attempt Levi-Civita parent theorem or executable connection-residual coefficient row",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gates() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE959_0_EH_operator",
            "claim": "MTS local exterior operator is EH+Lambda",
            "required_condition": "local second-order metric-only no-extra-field clause is parent-signed",
            "current_evidence": "conditional clause only; R2/fR and torsion/nonmetricity remain unfilled",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE959_1_R11_priority_scoring",
            "claim": "priority R11 rows can be scored",
            "required_condition": "R2/fR and torsion/nonmetricity rows have real values/zero certificates, units, maps, sources, and assumptions",
            "current_evidence": "priority fill dryrun rejects both rows",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE959_2_Newton_local_GR",
            "claim": "Newton/local-GR bridge can promote",
            "required_condition": "EH/R11 operator gate passes before GM/worldtube and PPN gates",
            "current_evidence": "operator gate still open",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target() -> list[dict[str, str]]:
    return [
        {
            "next_target": "960-Y5-R10-R2-fR-scalar-mode-zero-or-bound-and-torsion-Levi-Civita-gate.md",
            "objective": "attempt derived-zero or bound rows for the first two R11 priority families: R2/fR scalar mode and torsion/nonmetricity/Levi-Civita connection",
            "include": "R2/fR scalar/fourth-order mode, alpha(lambda)/PPN mapping, Levi-Civita parent theorem, torsion/nonmetricity residual rows",
            "exclude": "EH claim, measured-GM claim, local-GR claim, invented coefficients, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return -1
    since = SCRIPT_START_UTC.astimezone().strftime("%Y-%m-%dT%H:%M:%S")
    command = (
        "$since=[datetime]::Parse('"
        + since
        + "'); "
        + "$count=(Get-ChildItem -LiteralPath '"
        + str(FORMALIZATION).replace("'", "''")
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


def validation(
    sources: list[dict[str, str]],
    clause_rows: list[dict[str, str]],
    silence_rows: list[dict[str, str]],
    fill_rows: list[dict[str, str]],
    dryrun_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    def add(check_id: str, passes: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passes else "fail", "detail": detail, "generated_utc": stamp()})

    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    prior_clean = all(row.get("result") == "pass" for row in read_csv(OUT / "P8_Y5_BRR545_958_VALIDATION.csv"))
    clause_not_signed = any(row["clause_id"] == "NEF959_5_verdict" and row["parent_signed"] == "false" for row in clause_rows)
    silence_requirements_ready = len(silence_rows) == 5
    fill_rows_selected = {row["operator_family"] for row in fill_rows} == {"R2_fR_scalar_mode", "torsion_nonmetricity"}
    dryrun_rejects = len(dryrun_rows) == 2 and all(row["accepted_for_scoring"] == "false" for row in dryrun_rows)
    decisions_nonclaim = all(row["claim_allowed"] == "false" for row in decision_rows)
    claim_gates_false = all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claim_rows)
    target_selected = bool(target_rows) and target_rows[0]["next_target"].startswith("960-")
    valid_for_claim_false = all(
        row.get("valid_for_claim") == "false"
        for table in [sources, clause_rows, silence_rows, fill_rows, dryrun_rows, decision_rows, claim_rows, target_rows]
        for row in table
    )
    formalization_changed = formalization_changed_after_start()

    add("V959_0_sources_exist_and_needles", sources_ok, "all 959 source paths exist and needles are present" if sources_ok else "missing source path or needle")
    add("V959_1_prior_958_clean", prior_clean, "P8_Y5_BRR545_958_VALIDATION.csv clean")
    add("V959_2_no_extra_field_clause_not_signed", clause_not_signed, "no-extra-field clause remains unsigned")
    add("V959_3_silence_requirements_ready", silence_requirements_ready, "positive-operator/no-source/zero-boundary requirements written")
    add("V959_4_priority_fill_rows_selected", fill_rows_selected, "R2/fR and torsion/nonmetricity priority rows selected")
    add("V959_5_priority_dryrun_rejects_placeholders", dryrun_rejects, "priority fill dryrun rejects incomplete rows")
    add("V959_6_decisions_nonclaim", decisions_nonclaim, "decision ledger remains nonclaim")
    add("V959_7_claim_gates_false", claim_gates_false, "all claim gates remain false")
    add("V959_8_next_target_selected", target_selected, "960 R2/fR and torsion/LC target selected")
    add("V959_9_no_claims_promoted", valid_for_claim_false, "all generated rows are valid_for_claim=false")
    add("V959_10_formalization_workbench_untouched", formalization_changed == 0, f"formalization_changed_after_start={formalization_changed}")
    add("V959_11_validation_rows_ready", True, "validation table constructed")
    return rows


def write_doc(
    sources: list[dict[str, str]],
    clause_rows: list[dict[str, str]],
    silence_rows: list[dict[str, str]],
    fill_rows: list[dict[str, str]],
    dryrun_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    doc = f"""# 959 Y5 R10: Local Second-Order Metric-Only No-Extra-Field Clause Or R11 Priority Fill

Status: `Y5_R10_959_no_extra_field_clause_unsigned_R11_priority_fill_templates_written_nonclaim`

Claim ceiling: `conditional_no_extra_field_clause_only_no_EH_claim_no_R11_score_no_Newton_or_local_GR_claim`

## Result

This checkpoint tries to make the EH route bite.

The Lovelock-style implication is clean: if the compact local exterior branch is genuinely 4D, local, diffeomorphism-invariant, metric-only, second-order, and has no surviving extra fields or harmful boundary flux, the operator side reduces to EH plus Lambda/background. That would be a serious left-hand bridge to GR.

But MTS has not yet parent-derived that no-extra-field clause. The current honest route is field-by-field: each extra sector must be absent, gauge/topological with zero flux, positive source-free silent, or retained as an R11 residual. The first two priority families are `R2_fR_scalar_mode` and `torsion_nonmetricity`.

```text
no-extra-field theorem: not signed.
R2/fR and torsion/nonmetricity: first priority rows.
R11 scoring: blocked until sourced zero/bound rows exist.
```

## Source Register

{md_table(sources, ["source_id", "role", "exists", "needle_found", "path"])}

## No-Extra-Field Clause Attempt

{md_table(clause_rows, ["clause_id", "clause", "status", "would_close", "blocker", "parent_signed"])}

## Silence Mechanism Requirements

{md_table(silence_rows, ["requirement_id", "requirement", "needed_for", "current_status"])}

## R11 Priority Fill Template

{md_table(fill_rows, ["fill_id", "operator_family", "coefficient_symbol", "required_zero_or_bound", "first_observable", "ready_for_scoring"])}

## R11 Priority Fill Dryrun

{md_table(dryrun_rows, ["dryrun_id", "operator_family", "missing_fields", "accepted_for_scoring", "verdict"])}

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
    clause_rows = no_extra_field_clause_attempt()
    silence_rows = silence_mechanism_requirements()
    fill_rows = r11_priority_fill_template()
    dryrun_rows = r11_priority_fill_dryrun(fill_rows)
    decision_rows = decisions()
    claim_rows = claim_gates()
    target_rows = next_target()
    validation_rows = validation(sources, clause_rows, silence_rows, fill_rows, dryrun_rows, decision_rows, claim_rows, target_rows)

    write_csv(
        OUT / "P8_Y5_R10_959_SOURCE_REGISTER.csv",
        sources,
        ["source_id", "path", "role", "needle", "absolute_path", "exists", "needle_found", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_959_NO_EXTRA_FIELD_CLAUSE_ATTEMPT.csv",
        clause_rows,
        ["clause_id", "clause", "mathematical_form", "status", "would_close", "blocker", "parent_signed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_959_SILENCE_MECHANISM_REQUIREMENTS.csv",
        silence_rows,
        ["requirement_id", "requirement", "mathematical_form", "needed_for", "current_status", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_959_R11_PRIORITY_FILL_TEMPLATE.csv",
        fill_rows,
        [
            "fill_id",
            "operator_family",
            "coefficient_symbol",
            "required_zero_or_bound",
            "candidate_value",
            "candidate_units",
            "normalization",
            "weak_field_map",
            "predicted_residual_or_bound_source",
            "derivation_status",
            "source_file",
            "formula_reference",
            "assumptions",
            "first_observable",
            "ready_for_scoring",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_959_R11_PRIORITY_FILL_DRYRUN.csv",
        dryrun_rows,
        ["dryrun_id", "operator_family", "missing_fields", "accepted_for_scoring", "verdict", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_959_DECISION_LEDGER.csv",
        decision_rows,
        ["decision_id", "topic", "result", "reason", "next_action", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_959_CLAIM_GATE.csv",
        claim_rows,
        ["gate_id", "claim", "required_condition", "current_evidence", "gate_pass", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_959_NEXT_TARGET.csv",
        target_rows,
        ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_BRR545_959_VALIDATION.csv",
        validation_rows,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_doc(sources, clause_rows, silence_rows, fill_rows, dryrun_rows, decision_rows, claim_rows, target_rows, validation_rows)


if __name__ == "__main__":
    main()

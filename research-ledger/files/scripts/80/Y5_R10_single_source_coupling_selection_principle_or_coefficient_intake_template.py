from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "952-Y5-R10-single-source-coupling-selection-principle-or-coefficient-intake-template.md"
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


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "951_doc",
            "path": "951-Y5-R10-source-current-Ward-action-or-finite-coefficient-provenance-gate.md",
            "role": "handoff: Ward bridge real but single coupling missing",
            "needle": "Ward bridge: real",
        },
        {
            "source_id": "951_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_951_VALIDATION.csv",
            "role": "previous checkpoint validation",
            "needle": "V951_11_validation_rows_ready",
        },
        {
            "source_id": "951_next_target",
            "path": "source-intake/mts_residuals/P8_Y5_R10_951_NEXT_TARGET.csv",
            "role": "952 target selection",
            "needle": "952-Y5-R10-single-source-coupling-selection-principle-or-coefficient-intake-template.md",
        },
        {
            "source_id": "951_Ward_action",
            "path": "source-intake/mts_residuals/P8_Y5_R10_951_SOURCE_CURRENT_WARD_ACTION_ATTEMPT.csv",
            "role": "Ward bridge and species-weight countermodel",
            "needle": "SWA951_3_species_weight_countermodel",
        },
        {
            "source_id": "951_provenance_schema",
            "path": "source-intake/mts_residuals/P8_Y5_R10_951_PROVENANCE_GATE_SCHEMA.csv",
            "role": "mandatory provenance fields",
            "needle": "PGS951_2_derivation_status",
        },
        {
            "source_id": "951_provenance_dryrun",
            "path": "source-intake/mts_residuals/P8_Y5_R10_951_PROVENANCE_GATE_DRYRUN.csv",
            "role": "current coefficient rows rejected for missing provenance",
            "needle": "PGD951_2_WEP_surface_beta_source",
        },
        {
            "source_id": "no_species_contract",
            "path": "source-intake/mts_residuals/P8_no_species_source_charge_CONTRACT.csv",
            "role": "constant/source no-marker contract",
            "needle": "S4_source_normalization_species_blind",
        },
        {
            "source_id": "763_no_marker_spurion",
            "path": "source-intake/mts_residuals/P8_Y5_R10_763_NO_MARKER_SPURION_THEOREM_ATTEMPT.csv",
            "role": "source-weight no-marker blocker",
            "needle": "NMS763_3_universal_source_weight",
        },
        {
            "source_id": "449_source_current",
            "path": "449-source-current-Ward-universality-theorem-attempt.md",
            "role": "older source-current Ward universality attempt",
            "needle": "source_current_Ward_universality_theorem_attempt_written",
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


def single_source_selection_attempt() -> list[dict[str, str]]:
    return [
        {
            "selection_id": "SSC952_0_target",
            "principle": "single universal source coupling",
            "mathematical_form": "S_source = kappa_univ int e_obs J_univ, J_univ=sum_A T_A",
            "status": "target_identified",
            "would_prove": "beta_source_normalized=0 for WEP source-normalization channel",
            "why_not_enough": "target statement is the desired result, not its derivation",
            "countermodel_excluded": "false",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "selection_id": "SSC952_1_Ward_symmetry",
            "principle": "diffeomorphism Ward symmetry",
            "mathematical_form": "delta_xi S=0 implies nabla_mu J_total^{mu}=0",
            "status": "valid_but_homogeneous",
            "would_prove": "conservation of whatever source current is in the action",
            "why_not_enough": "constant species weights kappa_A preserve Ward conservation",
            "countermodel_excluded": "false",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "selection_id": "SSC952_2_no_species_label_naturality",
            "principle": "source current is the unique natural additive Hilbert current of one observed coframe",
            "mathematical_form": "Source(T_A,T_B)=Source(T_A)+Source(T_B) and no A-label in Nat(T,J)",
            "status": "clean_candidate_principle_not_parent_derived",
            "would_prove": "only one overall kappa_univ remains; relative kappa_A are forbidden labels",
            "why_not_enough": "naturality/no-species-label rule must be derived or adopted by parent action",
            "countermodel_excluded": "conditional_only",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "selection_id": "SSC952_3_equivalence_principle_input",
            "principle": "empirical WEP/equivalence principle",
            "mathematical_form": "all ordinary species fall/source universally to current experimental precision",
            "status": "empirical_constraint_not_derivation",
            "would_prove": "can bound relative kappa_A",
            "why_not_enough": "using WEP to prove WEP silence is circular for the local-GR derivation branch",
            "countermodel_excluded": "bounded_not_derived",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "selection_id": "SSC952_4_unit_rescaling",
            "principle": "overall kappa can be absorbed into measured G units",
            "mathematical_form": "kappa_univ -> lambda kappa_univ can be calibrated by G_ref",
            "status": "valid_for_common_mode_only",
            "would_prove": "common source normalization can be a unit choice",
            "why_not_enough": "relative species weights kappa_A/kappa_B are invariant and WEP-visible",
            "countermodel_excluded": "false",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "selection_id": "SSC952_5_verdict",
            "principle": "single-source coupling selection theorem",
            "mathematical_form": "Ward + naturality/no-species-label + one observed coframe => one kappa_univ",
            "status": "not_closed_current_corpus",
            "would_prove": "the WEP source coefficient zero route",
            "why_not_enough": "the naturality/no-species-label premise is the new exact theorem target",
            "countermodel_excluded": "false",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def coefficient_intake_template() -> list[dict[str, str]]:
    rows = []
    for source in read_csv(OUT / "P8_Y5_R10_951_PROVENANCE_GATE_DRYRUN.csv"):
        rows.append(
            {
                "intake_id": source["dryrun_id"].replace("PGD951", "CIT952"),
                "coefficient_symbol": source["coefficient_symbol"],
                "arena": source["arena"],
                "branch_type": "finite_value_or_parent_zero",
                "candidate_value": "MISSING_PARENT_INPUT",
                "units": "yr^-1" if source["coefficient_symbol"] == "kappa_alpha_tau_clock_time" else ("boolean" if source["coefficient_symbol"] == "constant_source_zero_theorem" else "dimensionless"),
                "candidate_source_path": "MISSING_PARENT_SOURCE",
                "source_row_id": "MISSING_SOURCE_ROW_ID",
                "derivation_status": "MISSING_DERIVATION_STATUS",
                "comparison_bound": source["comparison_bound"],
                "comparison_bound_source": "inherited_from_951_provenance_dryrun",
                "claim_policy": "NONCLAIM_UNTIL_FULL_LOCAL_STACK_CLOSES",
                "ready_for_provenance_gate": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def intake_template_dryrun(template_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    for template in template_rows:
        missing = [
            field
            for field in ["candidate_value", "candidate_source_path", "source_row_id", "derivation_status"]
            if template[field].startswith("MISSING")
        ]
        rows.append(
            {
                "dryrun_id": template["intake_id"].replace("CIT952", "CID952"),
                "coefficient_symbol": template["coefficient_symbol"],
                "arena": template["arena"],
                "missing_fields": ";".join(missing),
                "accepted_by_intake": flag(not missing),
                "forward_to_951_gate": "false",
                "verdict": "REJECTED_TEMPLATE_PLACEHOLDER" if missing else "READY_FOR_951_PROVENANCE_GATE_NONCLAIM",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def decisions() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC952_0_single_coupling",
            "topic": "single-source coupling selection",
            "result": "candidate_naturality_principle_identified_not_derived",
            "reason": "Ward symmetry alone is homogeneous; the missing extra is a parent no-species-label/naturality rule for the source functor",
            "next_action": "try to derive the no-species-label naturality rule from the parent matter/source functor",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC952_1_coefficient_intake",
            "topic": "coefficient intake template",
            "result": "mandatory_provenance_template_written",
            "reason": "future finite values now need candidate value, source path, source row id, derivation status, units, bound link, and claim policy",
            "next_action": "only forward an intake row to the 951 provenance gate when all mandatory fields are filled",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gates() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE952_0_single_coupling",
            "claim": "parent action permits only one universal source coupling",
            "required_condition": "derive no-species-label/naturality source functor from parent action",
            "current_evidence": "clean candidate principle, not parent-signed",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE952_1_coefficient_intake",
            "claim": "finite coefficient can be forwarded to scoring",
            "required_condition": "all intake mandatory fields filled with existing source path",
            "current_evidence": "template rows intentionally contain missing markers",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target() -> list[dict[str, str]]:
    return [
        {
            "next_target": "953-Y5-R10-no-species-label-source-functor-theorem-or-filled-coefficient-intake-review.md",
            "objective": "try to derive the no-species-label naturality theorem for the source functor, or review any filled coefficient intake row against the 952/951 provenance gates",
            "include": "source functor naturality, additivity, one observed coframe, species-label exclusion, filled coefficient intake review",
            "exclude": "invented values, WEP/clock/local-GR claim, GitHub action, formalization-workbench edits",
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
    selection_rows: list[dict[str, str]],
    intake_rows: list[dict[str, str]],
    dryrun_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    def add(check_id: str, passes: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passes else "fail", "detail": detail, "generated_utc": stamp()})

    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    prior_clean = all(row.get("result") == "pass" for row in read_csv(OUT / "P8_Y5_BRR545_951_VALIDATION.csv"))
    selection_not_closed = any(row["selection_id"] == "SSC952_5_verdict" and row["parent_signed"] == "false" for row in selection_rows)
    naturality_identified = any(row["selection_id"] == "SSC952_2_no_species_label_naturality" for row in selection_rows)
    intake_rows_ready = len(intake_rows) == 5 and all(row["ready_for_provenance_gate"] == "false" for row in intake_rows)
    dryrun_rejected = all(row["accepted_by_intake"] == "false" and row["verdict"] == "REJECTED_TEMPLATE_PLACEHOLDER" for row in dryrun_rows)
    decisions_nonclaim = all(row["claim_allowed"] == "false" for row in decision_rows)
    claim_gates_false = all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claim_rows)
    target_selected = target_rows and target_rows[0]["next_target"].startswith("953-")
    valid_for_claim_false = all(
        row.get("valid_for_claim") == "false"
        for table in [sources, selection_rows, intake_rows, dryrun_rows, decision_rows, claim_rows, target_rows]
        for row in table
    )
    formalization_changed = formalization_changed_after_start()

    add("V952_0_sources_exist_and_needles", sources_ok, "all 952 source paths exist and needles are present" if sources_ok else "missing source path or needle")
    add("V952_1_prior_951_clean", prior_clean, "P8_Y5_BRR545_951_VALIDATION.csv clean")
    add("V952_2_single_coupling_not_closed", selection_not_closed, "single-source coupling theorem remains unclosed")
    add("V952_3_naturality_target_identified", naturality_identified, "no-species-label naturality target identified")
    add("V952_4_intake_template_written", intake_rows_ready, "coefficient intake template rows written with missing markers")
    add("V952_5_intake_dryrun_rejects_placeholders", dryrun_rejected, "intake dryrun rejects every placeholder row")
    add("V952_6_decisions_nonclaim", decisions_nonclaim, "decision ledger remains nonclaim")
    add("V952_7_claim_gates_false", claim_gates_false, "all claim gates remain false")
    add("V952_8_next_target_selected", target_selected, "953 no-species-label theorem or intake review target selected")
    add("V952_9_no_claims_promoted", valid_for_claim_false, "all generated rows are valid_for_claim=false")
    add("V952_10_formalization_workbench_untouched", formalization_changed == 0, f"formalization_changed_after_start={formalization_changed}")
    add("V952_11_validation_rows_ready", True, "validation table constructed")
    return rows


def write_doc(
    sources: list[dict[str, str]],
    selection_rows: list[dict[str, str]],
    intake_rows: list[dict[str, str]],
    dryrun_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    doc = f"""# 952 Y5 R10: Single-Source Coupling Selection Principle Or Coefficient Intake Template

Status: `Y5_R10_952_single_source_naturality_target_identified_intake_template_written_nonclaim`

Claim ceiling: `candidate_selection_principle_only_no_single_kappa_theorem_no_coefficient_score_no_local_GR_claim`

## Result

This checkpoint asks whether symmetry can force one universal source coupling.

The answer is still no from Ward symmetry alone. Ward conservation is homogeneous: it conserves whatever source current the action contains, including a species-weighted current if the parent action allows one. The clean new theorem target is narrower and sharper: a no-species-label naturality principle for the source functor. If the source functor is additive, built from one observed coframe, and cannot depend on species labels, then only one overall `kappa_univ` remains. That would close the WEP source-coupling branch, but it is not parent-signed yet.

The finite route now has an intake template. It deliberately rejects all placeholder rows until a future value arrives with source path, source row id, derivation status, units, bound link, and claim policy.

```text
Ward alone: not enough;
new exact target: no-species-label naturality of the source functor;
finite route: mandatory provenance intake before scoring.
```

## Source Register

{md_table(sources, ["source_id", "role", "exists", "needle_found", "path"])}

## Single-Source Coupling Selection Attempt

{md_table(selection_rows, ["selection_id", "principle", "status", "would_prove", "why_not_enough", "parent_signed"])}

## Coefficient Intake Template

{md_table(intake_rows, ["intake_id", "coefficient_symbol", "arena", "candidate_value", "candidate_source_path", "derivation_status", "ready_for_provenance_gate"])}

## Intake Template Dryrun

{md_table(dryrun_rows, ["dryrun_id", "coefficient_symbol", "arena", "missing_fields", "accepted_by_intake", "verdict"])}

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
    selection_rows = single_source_selection_attempt()
    intake_rows = coefficient_intake_template()
    dryrun_rows = intake_template_dryrun(intake_rows)
    decision_rows = decisions()
    claim_rows = claim_gates()
    target_rows = next_target()
    validation_rows = validation(sources, selection_rows, intake_rows, dryrun_rows, decision_rows, claim_rows, target_rows)

    write_csv(
        OUT / "P8_Y5_R10_952_SOURCE_REGISTER.csv",
        sources,
        ["source_id", "path", "role", "needle", "absolute_path", "exists", "needle_found", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_952_SINGLE_SOURCE_SELECTION_ATTEMPT.csv",
        selection_rows,
        [
            "selection_id",
            "principle",
            "mathematical_form",
            "status",
            "would_prove",
            "why_not_enough",
            "countermodel_excluded",
            "parent_signed",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_952_COEFFICIENT_INTAKE_TEMPLATE.csv",
        intake_rows,
        [
            "intake_id",
            "coefficient_symbol",
            "arena",
            "branch_type",
            "candidate_value",
            "units",
            "candidate_source_path",
            "source_row_id",
            "derivation_status",
            "comparison_bound",
            "comparison_bound_source",
            "claim_policy",
            "ready_for_provenance_gate",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_952_INTAKE_TEMPLATE_DRYRUN.csv",
        dryrun_rows,
        [
            "dryrun_id",
            "coefficient_symbol",
            "arena",
            "missing_fields",
            "accepted_by_intake",
            "forward_to_951_gate",
            "verdict",
            "claim_allowed",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_952_DECISION_LEDGER.csv",
        decision_rows,
        ["decision_id", "topic", "result", "reason", "next_action", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_952_CLAIM_GATE.csv",
        claim_rows,
        ["gate_id", "claim", "required_condition", "current_evidence", "gate_pass", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_952_NEXT_TARGET.csv",
        target_rows,
        ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_BRR545_952_VALIDATION.csv",
        validation_rows,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_doc(sources, selection_rows, intake_rows, dryrun_rows, decision_rows, claim_rows, target_rows, validation_rows)


if __name__ == "__main__":
    main()

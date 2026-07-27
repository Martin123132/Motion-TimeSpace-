from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "951-Y5-R10-source-current-Ward-action-or-finite-coefficient-provenance-gate.md"
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
            "source_id": "950_doc",
            "path": "950-Y5-R10-source-normalization-species-blind-zero-lemma-or-first-finite-coefficient-smoke-run.md",
            "role": "handoff: source-normalization not closed and smoke runner refuses missing values",
            "needle": "source-normalization zero: conditional, not derived",
        },
        {
            "source_id": "950_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_950_VALIDATION.csv",
            "role": "previous checkpoint validation",
            "needle": "V950_12_validation_rows_ready",
        },
        {
            "source_id": "950_next_target",
            "path": "source-intake/mts_residuals/P8_Y5_R10_950_NEXT_TARGET.csv",
            "role": "951 target selection",
            "needle": "951-Y5-R10-source-current-Ward-action-or-finite-coefficient-provenance-gate.md",
        },
        {
            "source_id": "950_smoke_runner",
            "path": "source-intake/mts_residuals/P8_Y5_R10_950_FINITE_COEFFICIENT_SMOKE_RUNNER.csv",
            "role": "strict finite-coefficient smoke runner",
            "needle": "REFUSED_MISSING_PARENT_INPUT_OR_SOURCE",
        },
        {
            "source_id": "949_input_schema",
            "path": "source-intake/mts_residuals/P8_Y5_R10_949_FINITE_COEFFICIENT_INPUT_SCHEMA.csv",
            "role": "finite coefficient comparison schema",
            "needle": "FCI949_2_WEP_surface_beta_source",
        },
        {
            "source_id": "449_source_current",
            "path": "449-source-current-Ward-universality-theorem-attempt.md",
            "role": "early source-current Ward universality attempt",
            "needle": "measured Newtonian `GM` still requires calibration",
        },
        {
            "source_id": "520_Ward_closure",
            "path": "520-Y5-source-current-Ward-closure-or-bound-row.md",
            "role": "Ward bridge and source-normalization insufficiency",
            "needle": "Ward conservation alone does not prove that",
        },
        {
            "source_id": "663_Euler_Ward",
            "path": "source-intake/mts_residuals/P8_Y5_R10_663_EULER_WARD_CHAIN_RESULT.csv",
            "role": "Euler/Ward chain result",
            "needle": "EW663_5_PiM_Hamiltonian_identification",
        },
        {
            "source_id": "737_Ward_flux",
            "path": "source-intake/mts_residuals/P8_Y5_R10_737_SOURCE_CURRENT_WARD_FLUX_ATTEMPT.csv",
            "role": "source-current Ward flux attempt",
            "needle": "WFA737_4_full_source_normalized_Newton",
        },
        {
            "source_id": "791_Ward_zero_gate",
            "path": "source-intake/mts_residuals/P8_Y5_R10_791_WARD_ZERO_THEOREM_GATE.csv",
            "role": "Ward zero theorem gate",
            "needle": "WZG791_1_matter_Q_zero",
        },
        {
            "source_id": "908_Bianchi_Ward",
            "path": "source-intake/mts_residuals/P8_Y5_R10_908_BIANCHI_WARD_GATE.csv",
            "role": "Bianchi/Ward no-silent-drop gate",
            "needle": "BWG908_1_no_silent_drop",
        },
        {
            "source_id": "no_species_contract",
            "path": "source-intake/mts_residuals/P8_no_species_source_charge_CONTRACT.csv",
            "role": "species/source current blocker contract",
            "needle": "S4_source_normalization_species_blind",
        },
        {
            "source_id": "763_no_marker_spurion",
            "path": "source-intake/mts_residuals/P8_Y5_R10_763_NO_MARKER_SPURION_THEOREM_ATTEMPT.csv",
            "role": "source-weight no-marker blocker",
            "needle": "NMS763_3_universal_source_weight",
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


def source_current_ward_action_attempt() -> list[dict[str, str]]:
    return [
        {
            "ward_id": "SWA951_0_matter_Ward",
            "target": "same-frame Hilbert stress conservation",
            "candidate_action_or_identity": "S_matter[Psi_A,e_obs,theta_univ] diffeomorphism invariant",
            "derivation_status": "valid_conditional",
            "what_it_proves": "nabla_mu T_matter^{mu nu}=0 on matter equations in observed geometry",
            "what_it_does_not_prove": "one universal source normalization or measured GM equality",
            "blocker": "same-frame and no-marker premises remain parent-signature requirements",
            "closes_source_zero": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "ward_id": "SWA951_1_Killing_current",
            "target": "unprojected stationary source current",
            "candidate_action_or_identity": "J_H[tau]=T_matter^{mu nu} tau_nu dSigma_mu, with tau Killing/stationary",
            "derivation_status": "valid_narrow_conditional",
            "what_it_proves": "nabla_mu(T_matter^{mu nu} tau_nu)=0 under Ward plus Killing conditions",
            "what_it_does_not_prove": "projected mass flux, Pi_M ownership, boundary/anomaly silence, or source calibration",
            "blocker": "projected measured source mass is stronger than Hilbert current conservation",
            "closes_source_zero": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "ward_id": "SWA951_2_single_coupling",
            "target": "one universal source coupling",
            "candidate_action_or_identity": "S_source = kappa_univ int e_obs J_univ, J_univ=sum_A T_A",
            "derivation_status": "candidate_contract_not_parent_derived",
            "what_it_proves": "would make beta_source_normalized=0 if parent-signed",
            "what_it_does_not_prove": "current corpus does not force kappa_A=kappa_B",
            "blocker": "Ward identities are homogeneous under constant species-weighted source couplings",
            "closes_source_zero": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "ward_id": "SWA951_3_species_weight_countermodel",
            "target": "unconditional Ward-to-universality proof",
            "candidate_action_or_identity": "S_source = sum_A kappa_A int e_obs T_A with constant kappa_A",
            "derivation_status": "countermodel_blocks_unconditional_theorem",
            "what_it_proves": "diffeomorphism Ward conservation can hold for a weighted total current",
            "what_it_does_not_prove": "species-blind WEP source normalization",
            "blocker": "kappa_A constants or marker-dependent kappa_A both evade pure Ward conservation unless excluded",
            "closes_source_zero": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "ward_id": "SWA951_4_measured_GM_calibration",
            "target": "measured source normalization",
            "candidate_action_or_identity": "mu_obs = G_ref M_H + Delta_mu(projector,boundary,exchange,calibration)",
            "derivation_status": "not_closed",
            "what_it_proves": "names the calibration residual that prevents Newton/PPN promotion",
            "what_it_does_not_prove": "Delta_mu=0 or source-normalized Newtonian limit",
            "blocker": "Pi_M, exchange current, boundary/anomaly flux, and Gauss/orbital calibration remain unsigned",
            "closes_source_zero": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "ward_id": "SWA951_5_verdict",
            "target": "source-current Ward action closes beta_source",
            "candidate_action_or_identity": "Ward + single source coupling + measured-GM calibration + no-marker source weight",
            "derivation_status": "not_closed_current_corpus",
            "what_it_proves": "Ward bridge is real but normalization is independent debt",
            "what_it_does_not_prove": "WEP, clock, R10, PPN, Newton, or local-GR pass",
            "blocker": "source-current universality must be parent-derived or finite coefficients must remain explicit",
            "closes_source_zero": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def provenance_gate_schema() -> list[dict[str, str]]:
    return [
        {
            "field_id": "PGS951_0_numeric_value",
            "field_name": "candidate_value",
            "requirement": "finite numeric value for finite branch, or PARENT_SIGNED_TRUE for zero-theorem branch",
            "failure_marker": "MISSING_PARENT_INPUT",
            "score_required": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "field_id": "PGS951_1_source_path",
            "field_name": "candidate_source_path",
            "requirement": "local source path exists and contains the coefficient or theorem",
            "failure_marker": "MISSING_PARENT_SOURCE",
            "score_required": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "field_id": "PGS951_2_derivation_status",
            "field_name": "derivation_status",
            "requirement": "one of parent_derived, parent_signed_zero_theorem, or explicit_closure_nonclaim",
            "failure_marker": "MISSING_DERIVATION_STATUS",
            "score_required": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "field_id": "PGS951_3_units",
            "field_name": "units",
            "requirement": "candidate units must match bound units",
            "failure_marker": "MISSING_OR_MISMATCHED_UNITS",
            "score_required": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "field_id": "PGS951_4_bound_link",
            "field_name": "comparison_bound_source",
            "requirement": "source-backed comparison bound row must be linked",
            "failure_marker": "MISSING_BOUND_LINK",
            "score_required": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "field_id": "PGS951_5_claim_policy",
            "field_name": "claim_policy",
            "requirement": "public/local-GR claim remains false unless full parent/local stack closes",
            "failure_marker": "CLAIM_POLICY_UNSET",
            "score_required": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def provenance_gate_dryrun() -> list[dict[str, str]]:
    rows = []
    for source in read_csv(OUT / "P8_Y5_R10_950_FINITE_COEFFICIENT_SMOKE_RUNNER.csv"):
        candidate_value = source["candidate_value"]
        candidate_source_path = source["candidate_source_path"]
        value_numeric = parse_float(candidate_value) is not None
        source_exists = candidate_source_path not in {"", "MISSING_PARENT_SOURCE"} and Path(candidate_source_path).exists()
        zero_theorem_ready = source["coefficient_symbol"] == "constant_source_zero_theorem" and candidate_value == "PARENT_SIGNED_TRUE" and source_exists
        finite_ready = value_numeric and source_exists
        score_eligible = finite_ready or zero_theorem_ready
        failure_reasons = []
        if not value_numeric and not zero_theorem_ready:
            failure_reasons.append("MISSING_NUMERIC_OR_PARENT_SIGNED_TRUE_VALUE")
        if not source_exists:
            failure_reasons.append("MISSING_EXISTING_SOURCE_PATH")
        failure_reasons.append("CLAIM_POLICY_FALSE")
        rows.append(
            {
                "dryrun_id": source["run_id"].replace("FSR950", "PGD951"),
                "coefficient_symbol": source["coefficient_symbol"],
                "arena": source["arena"],
                "candidate_value": candidate_value,
                "candidate_source_path": candidate_source_path,
                "comparison_bound": source["comparison_bound"],
                "provenance_status": "score_eligible_nonclaim" if score_eligible else "rejected_missing_provenance",
                "failure_reasons": ";".join(failure_reasons),
                "score_eligible": flag(score_eligible),
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def decisions() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC951_0_Ward_action",
            "topic": "source-current Ward action",
            "result": "Ward_bridge_real_normalization_unclosed",
            "reason": "Ward identities conserve same-frame currents under strong premises, but do not force one universal kappa or measured-GM calibration",
            "next_action": "derive a single-source coupling selection principle or keep finite source coefficients explicit",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC951_1_provenance_gate",
            "topic": "finite coefficient provenance",
            "result": "provenance_gate_written_all_current_candidates_rejected",
            "reason": "every current candidate still has MISSING_PARENT_INPUT and MISSING_PARENT_SOURCE",
            "next_action": "create a candidate coefficient intake file only if a real parent source path or labelled closure value is supplied",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gates() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE951_0_source_current_universality",
            "claim": "source-current Ward action proves species-blind normalization",
            "required_condition": "one universal kappa and measured-GM calibration derived from parent action",
            "current_evidence": "Ward bridge only; species-weighted source countermodel retained",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE951_1_finite_coefficient_score",
            "claim": "finite coefficients can be scored",
            "required_condition": "candidate value plus existing source path plus derivation status",
            "current_evidence": "provenance dryrun rejects every row",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE951_2_local_GR",
            "claim": "local GR/Newton/WEP/clock branch is closed",
            "required_condition": "source-current universality, coefficient gates, R10/PPN projections, and parent local stack close together",
            "current_evidence": "source normalization still unclosed; provenance gate only",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target() -> list[dict[str, str]]:
    return [
        {
            "next_target": "952-Y5-R10-single-source-coupling-selection-principle-or-coefficient-intake-template.md",
            "objective": "try to derive why the parent action permits only one universal source coupling kappa_univ, or create a coefficient intake template with mandatory provenance fields for future finite-value tests",
            "include": "single source-coupling selection, species-weighted countermodel exclusion, measured-GM calibration residual, provenance intake fields",
            "exclude": "invented coefficient values, zero-by-preference, WEP/clock/local-GR claim, GitHub action, formalization-workbench edits",
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
    ward_rows: list[dict[str, str]],
    schema_rows: list[dict[str, str]],
    dryrun_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    def add(check_id: str, passes: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passes else "fail", "detail": detail, "generated_utc": stamp()})

    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    prior_clean = all(row.get("result") == "pass" for row in read_csv(OUT / "P8_Y5_BRR545_950_VALIDATION.csv"))
    ward_not_closed = any(row["ward_id"] == "SWA951_5_verdict" and row["closes_source_zero"] == "false" for row in ward_rows)
    countermodel_retained = any(row["ward_id"] == "SWA951_3_species_weight_countermodel" for row in ward_rows)
    schema_complete = len(schema_rows) == 6 and all(row["score_required"] == "true" for row in schema_rows)
    dryrun_rejected = all(row["score_eligible"] == "false" and row["provenance_status"] == "rejected_missing_provenance" for row in dryrun_rows)
    decisions_nonclaim = all(row["claim_allowed"] == "false" for row in decision_rows)
    claim_gates_false = all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claim_rows)
    target_selected = target_rows and target_rows[0]["next_target"].startswith("952-")
    valid_for_claim_false = all(
        row.get("valid_for_claim") == "false"
        for table in [sources, ward_rows, schema_rows, dryrun_rows, decision_rows, claim_rows, target_rows]
        for row in table
    )
    formalization_changed = formalization_changed_after_start()

    add("V951_0_sources_exist_and_needles", sources_ok, "all 951 source paths exist and needles are present" if sources_ok else "missing source path or needle")
    add("V951_1_prior_950_clean", prior_clean, "P8_Y5_BRR545_950_VALIDATION.csv clean")
    add("V951_2_Ward_action_not_closed", ward_not_closed, "source-current Ward action does not close normalization")
    add("V951_3_species_weight_countermodel_retained", countermodel_retained, "species-weighted source-current countermodel recorded")
    add("V951_4_provenance_schema_complete", schema_complete, "provenance gate schema contains required fields")
    add("V951_5_provenance_dryrun_rejects_all", dryrun_rejected, "all current finite candidates rejected for missing provenance")
    add("V951_6_decisions_nonclaim", decisions_nonclaim, "decision ledger remains nonclaim")
    add("V951_7_claim_gates_false", claim_gates_false, "all claim gates remain false")
    add("V951_8_next_target_selected", target_selected, "952 single-source coupling or coefficient intake target selected")
    add("V951_9_no_claims_promoted", valid_for_claim_false, "all generated rows are valid_for_claim=false")
    add("V951_10_formalization_workbench_untouched", formalization_changed == 0, f"formalization_changed_after_start={formalization_changed}")
    add("V951_11_validation_rows_ready", True, "validation table constructed")
    return rows


def write_doc(
    sources: list[dict[str, str]],
    ward_rows: list[dict[str, str]],
    schema_rows: list[dict[str, str]],
    dryrun_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    doc = f"""# 951 Y5 R10: Source-Current Ward Action Or Finite-Coefficient Provenance Gate

Status: `Y5_R10_951_Ward_bridge_real_source_normalization_unclosed_provenance_gate_rejects_missing_inputs_nonclaim`

Claim ceiling: `Ward_conservation_and_provenance_gate_only_no_source_zero_no_finite_score_no_local_GR_claim`

## Result

This checkpoint attacks the 950 fork from both sides.

The Ward/source-action route is real but still not enough. A same-frame diffeomorphism Ward identity can conserve the Hilbert stress current, and a stationary generator can define a narrow conserved current. But pure Ward conservation does not force one universal coupling `kappa_univ`, nor does it close measured-GM/source calibration. A species-weighted source-current action remains a legal countermodel until the parent action selects a single source coupling.

The finite route now has a provenance gate. Every current coefficient row is rejected because it still has `MISSING_PARENT_INPUT` and `MISSING_PARENT_SOURCE`. That means the machinery is ready to score a future value, but it will not score a made-up one.

```text
Ward bridge: real;
source normalization: not closed;
finite coefficient gate: strict provenance required before scoring.
```

## Source Register

{md_table(sources, ["source_id", "role", "exists", "needle_found", "path"])}

## Source-Current Ward Action Attempt

{md_table(ward_rows, ["ward_id", "target", "derivation_status", "what_it_proves", "what_it_does_not_prove", "blocker", "closes_source_zero"])}

## Provenance Gate Schema

{md_table(schema_rows, ["field_id", "field_name", "requirement", "failure_marker", "score_required"])}

## Provenance Gate Dryrun

{md_table(dryrun_rows, ["dryrun_id", "coefficient_symbol", "arena", "candidate_value", "candidate_source_path", "provenance_status", "score_eligible"])}

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
    ward_rows = source_current_ward_action_attempt()
    schema_rows = provenance_gate_schema()
    dryrun_rows = provenance_gate_dryrun()
    decision_rows = decisions()
    claim_rows = claim_gates()
    target_rows = next_target()
    validation_rows = validation(sources, ward_rows, schema_rows, dryrun_rows, decision_rows, claim_rows, target_rows)

    write_csv(
        OUT / "P8_Y5_R10_951_SOURCE_REGISTER.csv",
        sources,
        ["source_id", "path", "role", "needle", "absolute_path", "exists", "needle_found", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_951_SOURCE_CURRENT_WARD_ACTION_ATTEMPT.csv",
        ward_rows,
        [
            "ward_id",
            "target",
            "candidate_action_or_identity",
            "derivation_status",
            "what_it_proves",
            "what_it_does_not_prove",
            "blocker",
            "closes_source_zero",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_951_PROVENANCE_GATE_SCHEMA.csv",
        schema_rows,
        ["field_id", "field_name", "requirement", "failure_marker", "score_required", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_951_PROVENANCE_GATE_DRYRUN.csv",
        dryrun_rows,
        [
            "dryrun_id",
            "coefficient_symbol",
            "arena",
            "candidate_value",
            "candidate_source_path",
            "comparison_bound",
            "provenance_status",
            "failure_reasons",
            "score_eligible",
            "claim_allowed",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_951_DECISION_LEDGER.csv",
        decision_rows,
        ["decision_id", "topic", "result", "reason", "next_action", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_951_CLAIM_GATE.csv",
        claim_rows,
        ["gate_id", "claim", "required_condition", "current_evidence", "gate_pass", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_951_NEXT_TARGET.csv",
        target_rows,
        ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_BRR545_951_VALIDATION.csv",
        validation_rows,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_doc(sources, ward_rows, schema_rows, dryrun_rows, decision_rows, claim_rows, target_rows, validation_rows)


if __name__ == "__main__":
    main()

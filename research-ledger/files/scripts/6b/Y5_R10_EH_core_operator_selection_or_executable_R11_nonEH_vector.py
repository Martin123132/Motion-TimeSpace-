from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "958-Y5-R10-EH-core-operator-selection-or-executable-R11-nonEH-vector.md"
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
    return "MISSING" in value or value.startswith("fill_") or value.startswith("FILL_") or value == ""


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "957_doc",
            "path": "957-Y5-R10-parent-local-GR-spine-ledger-and-EH-vs-GM-next-derivation-choice.md",
            "role": "handoff: EH/operator selected before GM",
            "needle": "EH-core operator selection",
        },
        {
            "source_id": "957_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_957_VALIDATION.csv",
            "role": "previous checkpoint validation",
            "needle": "V957_12_validation_rows_ready",
        },
        {
            "source_id": "957_next_contract",
            "path": "source-intake/mts_residuals/P8_Y5_R10_957_NEXT_BRANCH_CONTRACT.csv",
            "role": "958 EH/R11 branch contract",
            "needle": "NBC957_0_EH_core_target",
        },
        {
            "source_id": "655_premise_audit",
            "path": "source-intake/mts_residuals/P8_Y5_R10_655_EH_ONLY_PREMISE_AUDIT.csv",
            "role": "EH-only premise audit",
            "needle": "EHP655_P6_second_order",
        },
        {
            "source_id": "R11_gate",
            "path": "source-intake/mts_residuals/R11_EH_ONLY_OR_EXECUTABLE_VECTOR_GATE.csv",
            "role": "EH-only or executable R11 vector gate",
            "needle": "EHV5_R11_actual_vector_supplied",
        },
        {
            "source_id": "R11_executable",
            "path": "source-intake/mts_residuals/R11_nonEH_operator_vector_executable.csv",
            "role": "current R11/nonEH executable candidate rows",
            "needle": "R11_nonEH_operator_vector_executable",
        },
        {
            "source_id": "R11_missing_fields",
            "path": "source-intake/mts_residuals/R11_MTS_VECTOR_MISSING_FIELD_LEDGER.csv",
            "role": "R11 minimum missing-field ledger",
            "needle": "predicted_residual_or_bound_source",
        },
        {
            "source_id": "R11_status",
            "path": "source-intake/mts_residuals/R11_EXECUTABLE_VECTOR_STATUS.csv",
            "role": "R11 family status and blockers",
            "needle": "source_normalization_operator",
        },
        {
            "source_id": "699_EH_coefficient",
            "path": "source-intake/mts_residuals/P8_Y5_R10_699_EH_COEFFICIENT_PROOF_AUDIT.csv",
            "role": "EH-to-Poisson coefficient proof audit",
            "needle": "EH699_6_verdict",
        },
        {
            "source_id": "700_EH_algebra",
            "path": "source-intake/mts_residuals/P8_Y5_R10_700_EH_POISSON_ALGEBRA_CERTIFICATE.csv",
            "role": "EH weak-field Poisson algebra certificate",
            "needle": "ALG700_4_poisson_coefficient",
        },
        {
            "source_id": "704_EH_prefactor",
            "path": "source-intake/mts_residuals/P8_Y5_R10_704_EH_PREFACTOR_FORMALIZATION.csv",
            "role": "EH prefactor/coupling formalization",
            "needle": "EHPF704_2_epsilon_G",
        },
        {
            "source_id": "768_reentry",
            "path": "source-intake/mts_residuals/P8_Y5_R10_768_EH_R11_REENTRY_AUDIT.csv",
            "role": "EH/R11 reentry audit",
            "needle": "EHR768_2_R11_skeleton",
        },
        {
            "source_id": "912_EH_baseline",
            "path": "source-intake/mts_residuals/P8_Y5_R10_912_EH_CORE_BASELINE.csv",
            "role": "EH baseline and omega-extra warning",
            "needle": "EHB912_3_EH_does_not_silence_extras",
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


def eh_core_selection_attempt() -> list[dict[str, str]]:
    return [
        {
            "attempt_id": "EH958_0_target",
            "premise": "local exterior MTS operator selects EH core",
            "mathematical_form": "E_MTS = G_munu + Lambda g_munu + DeltaE_extra",
            "status": "target_selected_from_957",
            "if_passes": "left-hand local GR operator branch can use EH baseline and charge machinery",
            "why_not_closed": "DeltaE_extra terms are not yet theorem-zero or bounded",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "EH958_1_Lovelock_route",
            "premise": "local 4D diffeo-invariant metric-only second-order exterior action",
            "mathematical_form": "S_local[g_obs]=int sqrt(-g)(a R - 2 Lambda) + boundary",
            "status": "mathematical_route_known_conditional",
            "if_passes": "EH+Lambda operator selected up to normalization and boundary terms",
            "why_not_closed": "MTS has not parent-derived metric-only, second-order, no-extra-field, no-nonlocal premises",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "EH958_2_extra_field_obstruction",
            "premise": "no scalar, vector, bulk-X, domain, projector, memory, torsion/nonmetricity, or boundary operator survives",
            "mathematical_form": "DeltaE_extra = DeltaE_scalar + DeltaE_vector + DeltaE_X + DeltaE_D + DeltaE_conn + DeltaE_boundary + ... = 0",
            "status": "central_unclosed_obstruction",
            "if_passes": "R11/nonEH vector can be theorem-zero",
            "why_not_closed": "prior EH audits keep these families retained/template-only",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "EH958_3_EH_algebra_positive_result",
            "premise": "if EH source-frame premises pass, weak-field coefficient algebra is clean",
            "mathematical_form": "nabla^2 Phi=(kappa_eff c^4/2) rho_H = 4 pi G_eff rho_H",
            "status": "conditional_algebra_clean",
            "if_passes": "Poisson coefficient route is mathematically consistent",
            "why_not_closed": "coefficient algebra does not prove EH premise, constant G, source normalization, or measured GM",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "EH958_4_symplectic_warning",
            "premise": "EH baseline charge form does not silence omega_extra",
            "mathematical_form": "omega_total = omega_EH + omega_extra",
            "status": "baseline_not_full_MTS_proof",
            "if_passes": "Hamiltonian charge transfer can be attempted",
            "why_not_closed": "omega_extra must be zero/gauge/topological/no-flux or bounded",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "EH958_5_verdict",
            "premise": "EH-core operator selection theorem",
            "mathematical_form": "metric-only second-order + no-extra-sector + harmless boundary => EH+Lambda",
            "status": "not_parent_derived_current_corpus",
            "if_passes": "would unlock measured-GM transfer branch and PPN operator baseline",
            "why_not_closed": "the R11/nonEH residual vector remains required unless the parent signs all missing premises",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def premise_audit() -> list[dict[str, str]]:
    rows = []
    for row in read_csv(OUT / "P8_Y5_R10_655_EH_ONLY_PREMISE_AUDIT.csv"):
        rows.append(
            {
                "audit_id": row["premise_id"].replace("EHP655", "EHP958"),
                "premise": row["premise"],
                "required_for_EH": row["required_for_EH"],
                "current_status": row["current_status"],
                "result_for_EH": row["result_for_EH"],
                "residual_if_failed": row.get("residual_if_failed", ""),
                "passes_for_claim": flag(row["result_for_EH"] == "pass_for_claim"),
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def r11_vector_review() -> list[dict[str, str]]:
    rows = []
    fields_to_check = [
        "coefficient_value",
        "coefficient_units",
        "normalization",
        "weak_field_map",
        "predicted_residual_or_bound_source",
        "derivation_status",
        "formula_reference",
        "source_file",
        "assumptions",
    ]
    for row in read_csv(OUT / "R11_nonEH_operator_vector_executable.csv"):
        missing = [field for field in fields_to_check if has_missing(row.get(field, ""))]
        source_value = row.get("source_file", "")
        source_exists = bool(source_value) and not has_missing(source_value) and (ROOT / source_value).exists()
        if "source_file" not in missing and not source_exists:
            missing.append("source_file_exists")
        accepted = not missing
        rows.append(
            {
                "review_id": f"R11REV958_{len(rows)}",
                "operator_family": row["operator_family"],
                "coefficient_symbol": row["coefficient_symbol"],
                "affected_rows": row.get("affected_rows", ""),
                "coefficient_value": row.get("coefficient_value", ""),
                "coefficient_units": row.get("coefficient_units", ""),
                "weak_field_map": row.get("weak_field_map", ""),
                "predicted_residual_or_bound_source": row.get("predicted_residual_or_bound_source", ""),
                "derivation_status": row.get("derivation_status", ""),
                "missing_fields": ";".join(missing),
                "accepted_for_scoring": flag(accepted),
                "verdict": "READY_FOR_R11_SCORING_NONCLAIM" if accepted else "REJECTED_R11_NOT_EXECUTABLE",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def operator_family_priority() -> list[dict[str, str]]:
    priority_map = {
        "R2_fR_scalar_mode": ("highest_first", "central second-order blocker; finite-range/scalar PPN/R10 maps"),
        "torsion_nonmetricity": ("highest_first", "connection compatibility blocks WEP, clocks, light cones, spin, and source charge"),
        "bulk_X_force_law": ("high", "bulk/local fifth-force and source-normalization residuals"),
        "boundary_topological_terms": ("high", "boundary flux can shift gamma, beta, alpha3, xi, and mass charge"),
        "vector_preferred_frame": ("high", "preferred-frame alpha1/alpha2/alpha3/xi path"),
        "source_normalization_operator": ("high", "measured-GM and Newton promotion blocker"),
        "projector_domain_stress": ("high", "domain/projector backreaction into PPN/source rows"),
        "Ricci_Weyl_squared": ("medium", "quadratic tensor operators alter gamma/xi/wave-sector maps"),
        "scalar_tensor_class_metric": ("medium", "scalar class can change clocks/source/PPN/range"),
        "nonlocal_memory_kernel": ("medium", "local compact silence of memory kernel not imported from cosmology"),
    }
    rows = []
    for review in r11_vector_review():
        priority, reason = priority_map.get(review["operator_family"], ("unranked", "needs source-specific ranking"))
        rows.append(
            {
                "priority_id": review["review_id"].replace("R11REV958", "R11PRI958"),
                "operator_family": review["operator_family"],
                "priority": priority,
                "reason": reason,
                "current_verdict": review["verdict"],
                "minimum_next_fill": "derived_zero_certificate_or_numeric_bound_with_source_path",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def decisions() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC958_0_EH_theorem",
            "topic": "EH-core operator selection",
            "result": "conditional_route_known_not_parent_derived",
            "reason": "Lovelock-style EH route exists only after local 4D metric-only second-order no-extra-field premises are parent-derived",
            "next_action": "do not claim EH; attack the missing second-order/no-extra-field premises or fill R11 vector",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC958_1_R11_vector",
            "topic": "R11/nonEH fallback",
            "result": "vector_review_written_all_rows_rejected_not_executable",
            "reason": "current executable candidate rows still contain missing coefficients, units, maps, residual sources, derivation statuses, or source paths",
            "next_action": "prioritize R2/fR scalar-mode and torsion/nonmetricity zero-or-bound fills, then source-normalization/projector rows",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC958_2_next_route",
            "topic": "next derivation route",
            "result": "try_second_order_no_extra_field_parent_clause_before_numeric_fill",
            "reason": "a parent theorem would zero multiple R11 families at once; if it fails, the priority ledger now names the first coefficient families to fill",
            "next_action": "attempt local second-order metric-only/no-extra-field clause or produce R2/fR and torsion/nonmetricity residual fill rows",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gates() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE958_0_EH_selected",
            "claim": "local exterior operator is EH+Lambda",
            "required_condition": "all metric-only second-order no-extra-field premises parent-derived",
            "current_evidence": "conditional theorem route only; central premises fail for claim",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE958_1_R11_executable",
            "claim": "R11/nonEH vector can be scored",
            "required_condition": "every retained family has sourced coefficient, units, weak-field map, residual/bound source, derivation status, and assumptions",
            "current_evidence": "all current rows rejected as not executable",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE958_2_Newton_or_local_GR",
            "claim": "Newton/local-GR branch can promote",
            "required_condition": "EH/R11 gate plus measured-GM/source-normalization plus PPN vector pass",
            "current_evidence": "EH/R11 gate still fails",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target() -> list[dict[str, str]]:
    return [
        {
            "next_target": "959-Y5-R10-local-second-order-metric-only-no-extra-field-clause-or-R11-priority-fill.md",
            "objective": "try to derive the local second-order metric-only no-extra-field parent clause; if it fails, start the prioritized R11 fill with R2/fR scalar-mode and torsion/nonmetricity rows",
            "include": "Lovelock-style premise audit, no-extra-field theorem attempt, R2/fR scalar mode, torsion/nonmetricity, executable R11 fields",
            "exclude": "measured-GM claim, local-GR claim, invented coefficients, GitHub action, formalization-workbench edits",
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
    attempt_rows: list[dict[str, str]],
    premise_rows: list[dict[str, str]],
    r11_rows: list[dict[str, str]],
    priority_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    def add(check_id: str, passes: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passes else "fail", "detail": detail, "generated_utc": stamp()})

    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    prior_clean = all(row.get("result") == "pass" for row in read_csv(OUT / "P8_Y5_BRR545_957_VALIDATION.csv"))
    eh_not_claimed = any(row["attempt_id"] == "EH958_5_verdict" and row["status"] == "not_parent_derived_current_corpus" for row in attempt_rows)
    premise_failures_retained = any(row["audit_id"] == "EHP958_P6_second_order" and row["passes_for_claim"] == "false" for row in premise_rows)
    r11_review_complete = len(r11_rows) == 10 and all(row["accepted_for_scoring"] == "false" for row in r11_rows)
    priority_has_highest = any(row["priority"] == "highest_first" for row in priority_rows)
    decisions_nonclaim = all(row["claim_allowed"] == "false" for row in decision_rows)
    claim_gates_false = all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claim_rows)
    target_selected = bool(target_rows) and target_rows[0]["next_target"].startswith("959-")
    valid_for_claim_false = all(
        row.get("valid_for_claim") == "false"
        for table in [sources, attempt_rows, premise_rows, r11_rows, priority_rows, decision_rows, claim_rows, target_rows]
        for row in table
    )
    formalization_changed = formalization_changed_after_start()

    add("V958_0_sources_exist_and_needles", sources_ok, "all 958 source paths exist and needles are present" if sources_ok else "missing source path or needle")
    add("V958_1_prior_957_clean", prior_clean, "P8_Y5_BRR545_957_VALIDATION.csv clean")
    add("V958_2_EH_not_claimed", eh_not_claimed, "EH theorem route remains conditional/not parent-derived")
    add("V958_3_premise_failures_retained", premise_failures_retained, "central second-order premise still fails for claim")
    add("V958_4_R11_review_complete_rejected", r11_review_complete, "all 10 R11/nonEH rows reviewed and rejected as non-executable")
    add("V958_5_priority_rows_present", priority_has_highest, "R11 priority ledger identifies highest-first families")
    add("V958_6_decisions_nonclaim", decisions_nonclaim, "decision ledger remains nonclaim")
    add("V958_7_claim_gates_false", claim_gates_false, "all claim gates remain false")
    add("V958_8_next_target_selected", target_selected, "959 second-order/no-extra-field or R11 priority fill selected")
    add("V958_9_no_claims_promoted", valid_for_claim_false, "all generated rows are valid_for_claim=false")
    add("V958_10_formalization_workbench_untouched", formalization_changed == 0, f"formalization_changed_after_start={formalization_changed}")
    add("V958_11_validation_rows_ready", True, "validation table constructed")
    return rows


def write_doc(
    sources: list[dict[str, str]],
    attempt_rows: list[dict[str, str]],
    premise_rows: list[dict[str, str]],
    r11_rows: list[dict[str, str]],
    priority_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    doc = f"""# 958 Y5 R10: EH-Core Operator Selection Or Executable R11/NonEH Vector

Status: `Y5_R10_958_EH_core_route_conditional_R11_vector_review_rejects_missing_inputs_nonclaim`

Claim ceiling: `conditional_EH_route_only_no_EH_selection_no_R11_score_no_Newton_or_local_GR_claim`

## Result

This checkpoint attacks the EH/operator branch selected in 957.

The good part: the EH route is mathematically clean if MTS can earn the Lovelock-style premises — local 4D, diffeomorphism-invariant, metric-only, second-order, no extra local exterior fields, and harmless boundary terms. Under those conditions the left-hand operator reduces to EH plus Lambda/background, and prior algebra shows the Poisson coefficient route is clean.

The hard part: current MTS has not parent-derived those premises. Scalar/vector/bulk/domain/projector/memory/connection/boundary families remain legal unless killed. The fallback R11/nonEH vector exists, but current rows still contain missing coefficients, units, weak-field maps, residual/bound sources, derivation statuses, formula references, source files, or assumptions.

```text
EH route: real but conditional.
R11 route: scaffold exists but not executable.
next: try no-extra-field/second-order parent clause; if it fails, fill priority R11 rows.
```

## Source Register

{md_table(sources, ["source_id", "role", "exists", "needle_found", "path"])}

## EH-Core Selection Attempt

{md_table(attempt_rows, ["attempt_id", "premise", "status", "if_passes", "why_not_closed"])}

## EH Premise Audit

{md_table(premise_rows, ["audit_id", "premise", "current_status", "result_for_EH", "residual_if_failed"])}

## R11/NonEH Vector Review

{md_table(r11_rows, ["review_id", "operator_family", "coefficient_symbol", "missing_fields", "accepted_for_scoring", "verdict"])}

## R11 Operator Family Priority

{md_table(priority_rows, ["priority_id", "operator_family", "priority", "reason", "minimum_next_fill"])}

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
    attempt_rows = eh_core_selection_attempt()
    premise_rows = premise_audit()
    r11_rows = r11_vector_review()
    priority_rows = operator_family_priority()
    decision_rows = decisions()
    claim_rows = claim_gates()
    target_rows = next_target()
    validation_rows = validation(sources, attempt_rows, premise_rows, r11_rows, priority_rows, decision_rows, claim_rows, target_rows)

    write_csv(
        OUT / "P8_Y5_R10_958_SOURCE_REGISTER.csv",
        sources,
        ["source_id", "path", "role", "needle", "absolute_path", "exists", "needle_found", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_958_EH_CORE_SELECTION_ATTEMPT.csv",
        attempt_rows,
        ["attempt_id", "premise", "mathematical_form", "status", "if_passes", "why_not_closed", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_958_EH_PREMISE_AUDIT.csv",
        premise_rows,
        [
            "audit_id",
            "premise",
            "required_for_EH",
            "current_status",
            "result_for_EH",
            "residual_if_failed",
            "passes_for_claim",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_958_R11_NON_EH_VECTOR_REVIEW.csv",
        r11_rows,
        [
            "review_id",
            "operator_family",
            "coefficient_symbol",
            "affected_rows",
            "coefficient_value",
            "coefficient_units",
            "weak_field_map",
            "predicted_residual_or_bound_source",
            "derivation_status",
            "missing_fields",
            "accepted_for_scoring",
            "verdict",
            "claim_allowed",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_958_R11_OPERATOR_FAMILY_PRIORITY.csv",
        priority_rows,
        ["priority_id", "operator_family", "priority", "reason", "current_verdict", "minimum_next_fill", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_958_DECISION_LEDGER.csv",
        decision_rows,
        ["decision_id", "topic", "result", "reason", "next_action", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_958_CLAIM_GATE.csv",
        claim_rows,
        ["gate_id", "claim", "required_condition", "current_evidence", "gate_pass", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_958_NEXT_TARGET.csv",
        target_rows,
        ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_BRR545_958_VALIDATION.csv",
        validation_rows,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_doc(sources, attempt_rows, premise_rows, r11_rows, priority_rows, decision_rows, claim_rows, target_rows, validation_rows)


if __name__ == "__main__":
    main()

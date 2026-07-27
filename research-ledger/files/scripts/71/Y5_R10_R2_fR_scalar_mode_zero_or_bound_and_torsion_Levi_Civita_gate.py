from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "960-Y5-R10-R2-fR-scalar-mode-zero-or-bound-and-torsion-Levi-Civita-gate.md"
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


def has_missing(value: str) -> bool:
    return value == "" or "MISSING" in value or value.startswith("fill_") or value.startswith("FILL_")


def source_path(relative_path: str) -> Path:
    return ROOT / relative_path


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "959_doc",
            "path": "959-Y5-R10-local-second-order-metric-only-no-extra-field-clause-or-R11-priority-fill.md",
            "role": "handoff: R2/fR and torsion/nonmetricity first priority rows",
            "needle": "R2/fR and torsion/nonmetricity",
        },
        {
            "source_id": "959_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_959_VALIDATION.csv",
            "role": "previous checkpoint validation",
            "needle": "V959_11_validation_rows_ready",
        },
        {
            "source_id": "959_fill_template",
            "path": "source-intake/mts_residuals/P8_Y5_R10_959_R11_PRIORITY_FILL_TEMPLATE.csv",
            "role": "R2/fR and torsion fill templates",
            "needle": "R11FILL959_1",
        },
        {
            "source_id": "506_EH_silence",
            "path": "506-local-EH-reduction-and-extra-sector-silence-theorem.md",
            "role": "positive operator/source-free/zero-flux silence route",
            "needle": "positive source-free operator",
        },
        {
            "source_id": "443_connection",
            "path": "443-metric-compatibility-Levi-Civita-or-R11-connection-row.md",
            "role": "Levi-Civita vs R11 connection theorem audit",
            "needle": "Levi-Civita compatibility remains conditional",
        },
        {
            "source_id": "785_connection_stack",
            "path": "785-Y5-R10-psi-metric-coframe-connection-contract-or-bg-residual-lock.md",
            "role": "coframe/connection stack and torsion/nonmetricity lock",
            "needle": "torsion/nonmetricity gate blocks claim",
        },
        {
            "source_id": "784_connection_requirements",
            "path": "source-intake/mts_residuals/P8_Y5_R10_784_COFRAME_CONNECTION_REQUIREMENTS.csv",
            "role": "coframe/connection requirements",
            "needle": "CCR784_2_connection",
        },
        {
            "source_id": "R11_P4_connection_template",
            "path": "source-intake/mts_residuals/R11_P4_connection_rows_TEMPLATE.csv",
            "role": "P4 connection R11 rows",
            "needle": "torsion_nonmetricity_combined",
        },
        {
            "source_id": "R11_executable",
            "path": "source-intake/mts_residuals/R11_nonEH_operator_vector_executable.csv",
            "role": "general R11 executable candidate rows",
            "needle": "R2_fR_scalar_mode",
        },
        {
            "source_id": "700_EH_algebra",
            "path": "source-intake/mts_residuals/P8_Y5_R10_700_EH_POISSON_ALGEBRA_CERTIFICATE.csv",
            "role": "conditional EH-to-Poisson algebra certificate",
            "needle": "ALG700_4_poisson_coefficient",
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


def r2_fr_zero_or_bound_attempt() -> list[dict[str, str]]:
    return [
        {
            "attempt_id": "R2FR960_0_target",
            "route": "kill R2/fR scalar mode or retain it as bounded residual",
            "mathematical_form": "sqrt(-g)(c_R2 R^2 + c_fR f_extra(R))",
            "status": "target_from_959",
            "would_close": "second-order EH premise for this operator family",
            "why_not_closed": "c_R2/c_fR are not parent-derived zero and no scalar mass/coupling bound row is sourced",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "R2FR960_1_second_order_filter",
            "route": "second-order metric-only theorem filter",
            "mathematical_form": "R^2 or generic f(R) variation gives fourth-order/scalar mode unless coefficient zero/redundant",
            "status": "clean_filter_not_parent_zero",
            "would_close": "identifies why R2/fR is outside EH core",
            "why_not_closed": "filter says what must vanish; it does not prove the parent coefficient vanishes",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "R2FR960_2_topological_redundant_escape",
            "route": "topological/redundant escape",
            "mathematical_form": "Gauss-Bonnet in 4D may be topological; R^2/f(R) is not generically topological",
            "status": "escape_not_available_generically",
            "would_close": "only a true topological or field-redefinition proof would zero observables",
            "why_not_closed": "current row is R2/fR scalar mode, not a sourced Gauss-Bonnet topological certificate",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "R2FR960_3_bound_route",
            "route": "finite scalar-mode bound",
            "mathematical_form": "m_s^2 ~ 1/(6 c_R2) or model-specific scalar mass/coupling -> alpha(lambda), gamma, beta rows",
            "status": "schema_only_missing_inputs",
            "would_close": "R2/fR survives but becomes empirically scoreable",
            "why_not_closed": "needs coefficient, units, scalar mass/coupling, weak-field map, alpha(lambda)/PPN source path",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "R2FR960_4_verdict",
            "route": "R2/fR scalar-mode zero-or-bound",
            "mathematical_form": "c_R2=c_fR=0 theorem OR executable scalar-mode bound row",
            "status": "not_closed_current_corpus",
            "would_close": "R2/fR priority family",
            "why_not_closed": "neither zero theorem nor sourced bound inputs exist",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def torsion_lc_gate_attempt() -> list[dict[str, str]]:
    return [
        {
            "attempt_id": "LC960_0_target",
            "route": "derive observed connection is Levi-Civita or retain torsion/nonmetricity",
            "mathematical_form": "Gamma = Gamma_LC[g_obs], T^alpha_{mu nu}=0, Q_{lambda mu nu}=0",
            "status": "target_from_959_and_443",
            "would_close": "torsion/nonmetricity R11 family",
            "why_not_closed": "no parent action equation currently kills all independent connection residues",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "LC960_1_metric_formalism_route",
            "route": "connection absent as independent parent variable",
            "mathematical_form": "S_parent[g_obs,...] with Gamma defined as Gamma_LC[g_obs]",
            "status": "clean_if_parent_selects_metric_only",
            "would_close": "LC follows kinematically",
            "why_not_closed": "metric-only parent configuration remains unsigned and matter blindness to underlying fields is not fully derived",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "LC960_2_Palatini_route",
            "route": "Palatini/EH no-hypermomentum route",
            "mathematical_form": "delta_Gamma S_EH=0 and Delta_matter^lambda_{mu nu}=0 => LC up to projective gauge",
            "status": "conditional_but_premises_open",
            "would_close": "dynamic LC compatibility after EH and no-hypermomentum gates",
            "why_not_closed": "EH-only is not derived and matter/light/spin/source independence from Gamma is not proved",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "LC960_3_connection_residual_route",
            "route": "retain connection residues as R11 P4 rows",
            "mathematical_form": "c_T T^2 + c_Q Q^2 + matter connection couplings",
            "status": "fallback_schema_exists_not_filled",
            "would_close": "empirical nonclaim branch if every connection row gets coefficients and maps",
            "why_not_closed": "P4 template rows are placeholders and no WEP/clock/lightcone/spin/source maps are supplied",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "LC960_4_verdict",
            "route": "torsion/nonmetricity Levi-Civita gate",
            "mathematical_form": "metric-only parent OR Palatini no-hypermomentum OR executable P4 vector",
            "status": "not_closed_current_corpus",
            "would_close": "connection compatibility branch",
            "why_not_closed": "all theorem routes are conditional and executable R11 rows are unfilled",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def priority_bound_pack() -> list[dict[str, str]]:
    rows = []
    for row in read_csv(OUT / "P8_Y5_R10_959_R11_PRIORITY_FILL_TEMPLATE.csv"):
        if row["operator_family"] == "R2_fR_scalar_mode":
            needed = "c_R2_or_c_fR; units; scalar mass/coupling; gamma/beta map; alpha(lambda) map; source path"
            first_bound = "R10 alpha(lambda), PPN gamma/beta, finite-range scalar tests"
        else:
            needed = "c_T_or_c_Q; connection scale; WEP/clock/lightcone/spin/source map; source path"
            first_bound = "WEP/clock/lightcone/spin/source-charge/PPN connection tests"
        rows.append(
            {
                "pack_id": row["fill_id"].replace("R11FILL959", "BPACK960"),
                "operator_family": row["operator_family"],
                "coefficient_symbol": row["coefficient_symbol"],
                "needed_inputs": needed,
                "first_bound_family": first_bound,
                "candidate_value": row["candidate_value"],
                "candidate_units": row["candidate_units"],
                "weak_field_map": row["weak_field_map"],
                "source_file": row["source_file"],
                "ready_for_scoring": "false",
                "verdict": "BOUND_PACK_SCAFFOLD_ONLY",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def p4_connection_subrow_review() -> list[dict[str, str]]:
    rows = []
    required = [
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
    for row in read_csv(OUT / "R11_P4_connection_rows_TEMPLATE.csv"):
        missing = [field for field in required if has_missing(row.get(field, ""))]
        rows.append(
            {
                "review_id": f"P4REV960_{len(rows)}",
                "operator_family": row["operator_family"],
                "coefficient_symbol": row["coefficient_symbol"],
                "affected_rows": row["affected_rows"],
                "induced_observable": row["induced_observable"],
                "missing_fields": ";".join(missing),
                "accepted_for_scoring": flag(not missing),
                "verdict": "READY_FOR_SCORING_NONCLAIM" if not missing else "REJECTED_P4_CONNECTION_PLACEHOLDER",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def decisions() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC960_0_R2_fR",
            "topic": "R2/fR scalar mode",
            "result": "not_zeroed_not_bound",
            "reason": "second-order filter shows why the family is non-EH, but parent coefficient zero and scalar bound inputs are missing",
            "next_action": "try to derive c_R2=c_fR=0 from parent operator selection or source an alpha(lambda)/PPN scalar-mode map",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC960_1_torsion_nonmetricity",
            "topic": "Levi-Civita/torsion/nonmetricity",
            "result": "not_zeroed_not_bound",
            "reason": "metric-only and Palatini routes are conditional; P4 connection rows remain placeholders",
            "next_action": "attempt no-independent-connection/no-hypermomentum parent theorem or fill P4 connection subrows",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC960_2_next",
            "topic": "next route",
            "result": "split_next_into_parent_zero_vs_bound_pack",
            "reason": "both priority families need either theorem-zero certificates or executable bound rows before EH/R11 gate can progress",
            "next_action": "try parent zero clauses first; if they fail, build numeric/source acquisition ledgers",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gates() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE960_0_R2_fR_zero_or_bound",
            "claim": "R2/fR scalar mode is absent or below bounds",
            "required_condition": "derived zero/topological/redundant certificate or sourced scalar-mode bound row",
            "current_evidence": "filter and bound schema only",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE960_1_Levi_Civita",
            "claim": "observed connection is Levi-Civita and universally used",
            "required_condition": "metric-only parent or Palatini/no-hypermomentum theorem, or executable P4 vector below bounds",
            "current_evidence": "conditional theorem routes only; P4 rows unfilled",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE960_2_EH_R11",
            "claim": "EH/R11 operator gate progresses to Newton/GM branch",
            "required_condition": "priority families zeroed/bounded and remaining R11 families queued",
            "current_evidence": "priority families still blocked",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target() -> list[dict[str, str]]:
    return [
        {
            "next_target": "961-Y5-R10-priority-operator-parent-zero-clauses-or-bound-source-acquisition.md",
            "objective": "write exact parent-zero clauses for R2/fR and torsion/nonmetricity, or create source-acquisition ledgers for scalar-mode alpha(lambda)/PPN bounds and P4 connection residual bounds",
            "include": "c_R2/c_fR zero clause, Levi-Civita/no-hypermomentum clause, scalar-mode bound sources, torsion/nonmetricity bound sources",
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
    r2_rows: list[dict[str, str]],
    lc_rows: list[dict[str, str]],
    bound_rows: list[dict[str, str]],
    p4_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    def add(check_id: str, passes: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passes else "fail", "detail": detail, "generated_utc": stamp()})

    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    prior_clean = all(row.get("result") == "pass" for row in read_csv(OUT / "P8_Y5_BRR545_959_VALIDATION.csv"))
    r2_blocked = any(row["attempt_id"] == "R2FR960_4_verdict" and row["status"] == "not_closed_current_corpus" for row in r2_rows)
    lc_blocked = any(row["attempt_id"] == "LC960_4_verdict" and row["status"] == "not_closed_current_corpus" for row in lc_rows)
    bound_pack_ready = len(bound_rows) == 2 and all(row["ready_for_scoring"] == "false" for row in bound_rows)
    p4_rejected = len(p4_rows) == 6 and all(row["accepted_for_scoring"] == "false" for row in p4_rows)
    decisions_nonclaim = all(row["claim_allowed"] == "false" for row in decision_rows)
    claim_gates_false = all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claim_rows)
    target_selected = bool(target_rows) and target_rows[0]["next_target"].startswith("961-")
    valid_for_claim_false = all(
        row.get("valid_for_claim") == "false"
        for table in [sources, r2_rows, lc_rows, bound_rows, p4_rows, decision_rows, claim_rows, target_rows]
        for row in table
    )
    formalization_changed = formalization_changed_after_start()

    add("V960_0_sources_exist_and_needles", sources_ok, "all 960 source paths exist and needles are present" if sources_ok else "missing source path or needle")
    add("V960_1_prior_959_clean", prior_clean, "P8_Y5_BRR545_959_VALIDATION.csv clean")
    add("V960_2_R2_fR_not_closed", r2_blocked, "R2/fR row remains zero-or-bound blocked")
    add("V960_3_LC_not_closed", lc_blocked, "Levi-Civita/torsion row remains zero-or-bound blocked")
    add("V960_4_bound_pack_nonclaim", bound_pack_ready, "priority bound pack scaffolds written but not scoreable")
    add("V960_5_P4_rows_rejected", p4_rejected, "P4 connection subrows rejected as placeholders")
    add("V960_6_decisions_nonclaim", decisions_nonclaim, "decision ledger remains nonclaim")
    add("V960_7_claim_gates_false", claim_gates_false, "all claim gates remain false")
    add("V960_8_next_target_selected", target_selected, "961 parent-zero or bound-source acquisition selected")
    add("V960_9_no_claims_promoted", valid_for_claim_false, "all generated rows are valid_for_claim=false")
    add("V960_10_formalization_workbench_untouched", formalization_changed == 0, f"formalization_changed_after_start={formalization_changed}")
    add("V960_11_validation_rows_ready", True, "validation table constructed")
    return rows


def write_doc(
    sources: list[dict[str, str]],
    r2_rows: list[dict[str, str]],
    lc_rows: list[dict[str, str]],
    bound_rows: list[dict[str, str]],
    p4_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    doc = f"""# 960 Y5 R10: R2/fR Scalar Mode Zero-Or-Bound And Torsion Levi-Civita Gate

Status: `Y5_R10_960_R2_fR_and_torsion_LC_gates_not_closed_bound_scaffolds_written_nonclaim`

Claim ceiling: `priority_operator_gate_only_no_EH_claim_no_R11_score_no_Newton_or_local_GR_claim`

## Result

This checkpoint attacks the first two priority R11 families.

For `R2/fR`, the second-order filter is clean: generic `R^2` or `f(R)` terms are not EH-core terms because they introduce fourth-order/scalar dynamics unless their coefficients are zero, redundant, topological, or bounded. But the parent action has not supplied `c_R2=c_fR=0`, and no scalar-mode `alpha(lambda)`/PPN bound row is sourced.

For torsion/nonmetricity, the Levi-Civita route is also clean but conditional. It closes if the parent action has no independent connection, or if a Palatini/connection variation plus no hypermomentum forces `Gamma=Gamma_LC[g_obs]`. Current evidence does not prove that, and the P4 connection rows are still placeholders.

```text
R2/fR: filter works, zero/bound missing.
torsion/nonmetricity: LC routes known, parent proof/bounds missing.
EH/R11 gate: still blocked, but now with two precise next inputs.
```

## Source Register

{md_table(sources, ["source_id", "role", "exists", "needle_found", "path"])}

## R2/fR Zero-Or-Bound Attempt

{md_table(r2_rows, ["attempt_id", "route", "status", "would_close", "why_not_closed"])}

## Torsion / Levi-Civita Gate Attempt

{md_table(lc_rows, ["attempt_id", "route", "status", "would_close", "why_not_closed"])}

## Priority Bound Pack

{md_table(bound_rows, ["pack_id", "operator_family", "coefficient_symbol", "needed_inputs", "first_bound_family", "ready_for_scoring", "verdict"])}

## P4 Connection Subrow Review

{md_table(p4_rows, ["review_id", "operator_family", "coefficient_symbol", "induced_observable", "missing_fields", "accepted_for_scoring", "verdict"])}

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
    r2_rows = r2_fr_zero_or_bound_attempt()
    lc_rows = torsion_lc_gate_attempt()
    bound_rows = priority_bound_pack()
    p4_rows = p4_connection_subrow_review()
    decision_rows = decisions()
    claim_rows = claim_gates()
    target_rows = next_target()
    validation_rows = validation(sources, r2_rows, lc_rows, bound_rows, p4_rows, decision_rows, claim_rows, target_rows)

    write_csv(
        OUT / "P8_Y5_R10_960_SOURCE_REGISTER.csv",
        sources,
        ["source_id", "path", "role", "needle", "absolute_path", "exists", "needle_found", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_960_R2_FR_ZERO_OR_BOUND_ATTEMPT.csv",
        r2_rows,
        ["attempt_id", "route", "mathematical_form", "status", "would_close", "why_not_closed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_960_TORSION_LEVI_CIVITA_GATE_ATTEMPT.csv",
        lc_rows,
        ["attempt_id", "route", "mathematical_form", "status", "would_close", "why_not_closed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_960_PRIORITY_BOUND_PACK.csv",
        bound_rows,
        [
            "pack_id",
            "operator_family",
            "coefficient_symbol",
            "needed_inputs",
            "first_bound_family",
            "candidate_value",
            "candidate_units",
            "weak_field_map",
            "source_file",
            "ready_for_scoring",
            "verdict",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_960_P4_CONNECTION_SUBROW_REVIEW.csv",
        p4_rows,
        [
            "review_id",
            "operator_family",
            "coefficient_symbol",
            "affected_rows",
            "induced_observable",
            "missing_fields",
            "accepted_for_scoring",
            "verdict",
            "claim_allowed",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_960_DECISION_LEDGER.csv",
        decision_rows,
        ["decision_id", "topic", "result", "reason", "next_action", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_960_CLAIM_GATE.csv",
        claim_rows,
        ["gate_id", "claim", "required_condition", "current_evidence", "gate_pass", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_960_NEXT_TARGET.csv",
        target_rows,
        ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_BRR545_960_VALIDATION.csv",
        validation_rows,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_doc(sources, r2_rows, lc_rows, bound_rows, p4_rows, decision_rows, claim_rows, target_rows, validation_rows)


if __name__ == "__main__":
    main()

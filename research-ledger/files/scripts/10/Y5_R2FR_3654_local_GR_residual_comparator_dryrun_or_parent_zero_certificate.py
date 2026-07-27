from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3654"
BRANCH_ID = "MTS_R2FR_Y5_LOCAL_GR_RESIDUAL_COMPARATOR_DRYRUN_OR_PARENT_ZERO_CERTIFICATE_3654"
DOC = ROOT / "3654-Y5-R2FR-local-GR-residual-comparator-dryrun-or-parent-zero-certificate.md"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(ts: str) -> dict[str, object]:
    return {
        "timestamp_utc": ts,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_float(value: str | None) -> float | None:
    if value is None:
        return None
    value = str(value).strip()
    if not value or value.lower() in {"symbolic", "vector", "alpha(lambda)", "range-dependent"}:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def source_register(ts: str) -> list[dict[str, object]]:
    bounds = LOCAL_BOUNDS / "local_bound_claims.csv"
    specs = [
        ("next_3653", RESIDUALS / "P8_Y5_R2FR_3653_NEXT_TARGET.csv", "local-GR-residual-comparator", "3653 selected comparator dry-run"),
        ("doc_3653", ROOT / "3653-Y5-R2FR-Newton-Poisson-PPN-zero-vector-gate-or-local-GR-residual-fit.md", "GR/null baseline comparator", "3653 vector-gate caveat and baseline policy"),
        ("theorem_3653", RESIDUALS / "P8_Y5_R2FR_3653_NEWTON_PPN_ZERO_VECTOR_THEOREM_ATTEMPT.csv", "BASELINE_COMPARATOR_POLICY_DERIVED", "3653 baseline comparator policy"),
        ("bound_interface_3653", RESIDUALS / "P8_Y5_R2FR_3653_BOUND_INTERFACE_ROWS.csv", "BI3653_0_gamma", "3653 bound interface"),
        ("residual_rows_3653", RESIDUALS / "P8_Y5_R2FR_3653_LOCAL_GR_RESIDUAL_COMPONENT_ROWS.csv", "Delta_local_GR_abs", "3653 MTS residual symbols"),
        ("zero_contract_3653", RESIDUALS / "P8_Y5_R2FR_3653_ZERO_CONTRACT_ROWS.csv", "ZC3653_9_total", "3653 parent zero contract"),
        ("doc_425", ROOT / "425-EH-operator-retained-ledger-and-source-normalization-test-plan.md", "EH_plus_Lambda_baseline", "EH baseline comparator policy"),
        ("bounds_R3", bounds, "R3_gamma", "gamma bound anchor"),
        ("bounds_R4", bounds, "R4_beta", "beta bound anchor"),
        ("bounds_R5", bounds, "R5_alpha1", "alpha1 bound anchor"),
        ("bounds_R6", bounds, "R6_alpha2", "alpha2 bound anchor"),
        ("bounds_R7", bounds, "R7_alpha3", "alpha3 bound anchor"),
        ("bounds_R8", bounds, "R8_xi", "xi bound anchor"),
        ("bounds_R9", bounds, "R9_Gdot", "Gdot bound anchor"),
    ]
    rows = []
    for source_id, path, needle, role in specs:
        body = read_text(path)
        rows.append(
            {
                **base(ts),
                "source_id": source_id,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in body,
                "role": role,
            }
        )
    return rows


def bound_lookup() -> dict[str, dict[str, str]]:
    rows = load_csv(LOCAL_BOUNDS / "local_bound_claims.csv")
    return {row["row_id"]: row for row in rows if "row_id" in row}


def comparator_interface_rows(ts: str) -> list[dict[str, object]]:
    interface = load_csv(RESIDUALS / "P8_Y5_R2FR_3653_BOUND_INTERFACE_ROWS.csv")
    bounds = bound_lookup()
    rows = []
    for item in interface:
        bound_row = item["bound_row"]
        bound = bounds.get(bound_row, {})
        upper = bound.get("upper_bound") or item.get("upper_bound_or_status", "")
        units = bound.get("units") or item.get("units", "")
        numeric_bound = parse_float(upper)
        rows.append(
            {
                **base(ts),
                "interface_id": item["interface_id"].replace("BI3653", "CI3654"),
                "observable": item["observable"],
                "mts_symbol": item["mts_symbol"],
                "bound_row": bound_row,
                "upper_bound": upper,
                "numeric_bound": "" if numeric_bound is None else numeric_bound,
                "units": units,
                "baseline_symbol": f"GR_null_{item['mts_symbol']}",
                "mts_value_required": item["mts_symbol"],
                "comparison_status": "NUMERIC_BOUND_READY" if numeric_bound is not None else "SYMBOLIC_OR_VECTOR_GATE",
                "source_path_or_url": bound.get("reference_path_or_url", "internal_symbolic_gate"),
            }
        )
    return rows


def baseline_rows(ts: str, interface_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    for row in interface_rows:
        numeric_bound = row["numeric_bound"]
        is_numeric = numeric_bound != ""
        baseline_value = 0.0
        baseline_pass = bool(is_numeric and abs(baseline_value) <= float(numeric_bound))
        rows.append(
            {
                **base(ts),
                "score_ready": is_numeric,
                "baseline_id": row["interface_id"].replace("CI3654", "BL3654"),
                "baseline_model": "GR_null",
                "observable": row["observable"],
                "symbol": row["baseline_symbol"],
                "value": baseline_value if is_numeric else "STRUCTURAL_ZERO",
                "upper_bound": row["upper_bound"],
                "units": row["units"],
                "pass_same_interface": baseline_pass if is_numeric else False,
                "current_status": "BASELINE_NUMERIC_PASS" if baseline_pass else "BASELINE_STRUCTURAL_ONLY_NOT_NUMERIC",
                "claim_allowed": False,
            }
        )
    return rows


def mts_dryrun_rows(ts: str, interface_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    for row in interface_rows:
        numeric_bound = row["numeric_bound"]
        is_numeric = numeric_bound != ""
        rows.append(
            {
                **base(ts),
                "score_ready": False,
                "dryrun_id": row["interface_id"].replace("CI3654", "MTS3654"),
                "model": "MTS_local_GR_residual_vector",
                "observable": row["observable"],
                "symbol": row["mts_symbol"],
                "value": f"MISSING_{row['mts_symbol']}",
                "upper_bound": row["upper_bound"],
                "units": row["units"],
                "would_be_scoreable_if_numeric": is_numeric,
                "pass_same_interface": False,
                "current_status": "BLOCKED_PLACEHOLDER_REFUSED",
                "failure_reason": "MTS residual component is missing, parent-zero certificate absent, and placeholders are not evidence",
                "claim_allowed": False,
            }
        )
    return rows


def zero_certificate_audit(ts: str) -> list[dict[str, object]]:
    contracts = load_csv(RESIDUALS / "P8_Y5_R2FR_3653_ZERO_CONTRACT_ROWS.csv")
    rows = []
    for contract in contracts:
        status = contract["current_status"]
        rows.append(
            {
                **base(ts),
                "certificate_id": contract["contract_id"].replace("ZC3653", "PZC3654"),
                "symbol": contract["symbol"],
                "required_evidence": contract["required_evidence"],
                "input_status": status,
                "certificate_status": "MISSING_OR_UNSIGNED" if status != "SIGNED_PARENT_ZERO" else "SIGNED",
                "accepted_as_zero": False,
                "claim_allowed": False,
            }
        )
    return rows


def comparator_summary_rows(ts: str, baseline: list[dict[str, object]], mts: list[dict[str, object]], certs: list[dict[str, object]]) -> list[dict[str, object]]:
    numeric_baseline = [row for row in baseline if str(row["score_ready"]).lower() == "true"]
    baseline_passes = [row for row in numeric_baseline if str(row["pass_same_interface"]).lower() == "true"]
    mts_scoreable = [row for row in mts if str(row["score_ready"]).lower() == "true"]
    cert_accepted = [row for row in certs if str(row["accepted_as_zero"]).lower() == "true"]
    return [
        {
            **base(ts),
            "summary_id": "SUM3654_0_baseline",
            "object": "GR_null_baseline",
            "numeric_rows": len(numeric_baseline),
            "passes": len(baseline_passes),
            "blocked_rows": len(baseline) - len(numeric_baseline),
            "current_status": "BASELINE_NUMERIC_ROWS_PASS_SYMBOLIC_ROWS_STRUCTURAL",
            "claim_allowed": False,
        },
        {
            **base(ts),
            "summary_id": "SUM3654_1_MTS",
            "object": "MTS_local_GR_residual_vector",
            "numeric_rows": len(mts_scoreable),
            "passes": 0,
            "blocked_rows": len(mts) - len(mts_scoreable),
            "current_status": "MTS_DRYRUN_BLOCKED_VALUES_MISSING",
            "claim_allowed": False,
        },
        {
            **base(ts),
            "summary_id": "SUM3654_2_parent_zero_certificate",
            "object": "parent_zero_certificate",
            "numeric_rows": 0,
            "passes": len(cert_accepted),
            "blocked_rows": len(certs) - len(cert_accepted),
            "current_status": "PARENT_ZERO_CERTIFICATE_NOT_ACCEPTED",
            "claim_allowed": False,
        },
    ]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("CG3654_0_same_interface", "GR/null and MTS rows use the same observable/bound interface", "PASSED", "prevents one-sided MTS-only jackknife/bound interpretation"),
        ("CG3654_1_baseline_runs", "GR/null numeric rows pass their numeric bounds", "PASSED_FOR_NUMERIC_ROWS", "baseline sanity check works; symbolic Poisson/vector rows remain structural"),
        ("CG3654_2_placeholders_refused", "MTS placeholders cannot score or pass", "PASSED_REFUSAL", "prevents missing rows being silently treated as zero"),
        ("CG3654_3_parent_zero_certificate", "parent zero certificate can replace numeric rows only if every component is signed", "FAILED_UNSIGNED", "current corpus does not sign every component"),
        ("CG3654_4_no_public_claim", "local-GR/Newton/PPN pass is not claimed", "ACTIVE", "keeps dry-run private and nonclaim"),
        ("CG3654_5_next", "next step must fill residual values or parent zero certificates", "LOCAL_GR_COMPONENT_FILL_NEXT", "moves from interface to actual values/proofs"),
    ]
    return [
        {
            **base(ts),
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "reason": reason,
            "claim_allowed": False,
        }
        for gate_id, gate, status, reason in specs
    ]


def status_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "status": "LOCAL_GR_COMPARATOR_DRYRUN_WRITTEN_BASELINE_PASSES_MTS_PLACEHOLDERS_REFUSED",
            "summary": "3654 builds the local-GR comparator dry-run: GR/null baseline rows and MTS residual rows use the same bound interface, baseline numeric rows pass, and MTS placeholders are refused.",
            "claim_ceiling": "no Newtonian, PPN, local-GR, source-calibration, WEP, R10, clock, orbital, or EH-dominance pass is claimed",
            "useful_result": "The testing pipeline now implements the same-interface rule: MTS cannot be failed or passed without running the baseline through the same bounds, and missing MTS rows cannot masquerade as zero.",
        }
    ]


def next_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3654_0",
            "target_doc": "3655-Y5-R2FR-parent-local-GR-zero-certificate-or-first-residual-component-fill.md",
            "target_script": "scripts/Y5_R2FR_3655_parent_local_GR_zero_certificate_or_first_residual_component_fill.py",
            "objective": "try to sign the parent local-GR zero certificate component-by-component; if not possible, fill the first numeric/source-backed residual components for Delta_local_GR_abs",
            "success_gate": "at least one zero component is parent-signed or one residual component gains a real numeric/source-backed value, while the comparator keeps placeholder refusal active",
        }
    ]


def write_doc(sources, interface, baseline, mts, certs, summary, gates, status, next_target) -> None:
    lines = [
        "# 3654 - Local-GR residual comparator dry-run or parent zero certificate",
        "",
        f"**Status:** {status[0]['summary']}",
        "",
        f"**Claim ceiling:** {status[0]['claim_ceiling']}.",
        "",
        "## Main result",
        "",
        "The comparator now enforces the rule we wanted: `GR_null` and `MTS_local_GR_residual_vector` are evaluated against the same Newton/PPN interface. The GR/null numeric rows pass because their residuals are zero. MTS does **not** pass or fail physically yet, because every MTS residual row is still a missing component or unsigned parent-zero certificate.",
        "",
        "That is the clean result: no more one-sided tests, and no more accidentally treating placeholders as zeros.",
        "",
        "## Comparator interface",
    ]
    for row in interface:
        lines.append(f"- `{row['interface_id']}`: `{row['mts_symbol']}` vs `{row['bound_row']}` — {row['comparison_status']}")
    lines.extend(["", "## GR/null baseline rows"])
    for row in baseline:
        lines.append(f"- `{row['baseline_id']}`: `{row['observable']}` — {row['current_status']}")
    lines.extend(["", "## MTS dry-run rows"])
    for row in mts:
        lines.append(f"- `{row['dryrun_id']}`: `{row['symbol']}` — {row['current_status']}")
    lines.extend(["", "## Parent zero-certificate audit"])
    for row in certs:
        lines.append(f"- `{row['certificate_id']}`: `{row['symbol']}` — {row['certificate_status']}")
    lines.extend(["", "## Summary"])
    for row in summary:
        lines.append(f"- `{row['summary_id']}`: `{row['object']}` — {row['current_status']}")
    lines.extend(["", "## Claim gates"])
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: `{row['status']}` — {row['gate']}")
    lines.extend(["", "## Next checkpoint", ""])
    lines.append(f"`{next_target[0]['target_doc']}` via `{next_target[0]['target_script']}`.")
    lines.extend(["", "## Sources"])
    for row in sources:
        lines.append(f"- `{row['source_id']}`: `{row['path']}` exists={row['exists']} needle_found={row['needle_found']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_csv(path: Path) -> tuple[bool, int]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows)
    except Exception:
        return False, 0


def validate(ts, output_paths, sources, interface, baseline, mts, certs, summary, gates, status, next_target):
    rows = []

    def add(validation_id: str, ok: bool, detail: str) -> None:
        rows.append(
            {
                "timestamp_utc": ts,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "validation_id": validation_id,
                "result": "PASS" if ok else "FAIL",
                "detail": detail,
            }
        )

    add("VAL3654_0_sources_exist", all(row["exists"] for row in sources), "every cited local source path exists")
    add("VAL3654_1_needles_found", all(row["needle_found"] for row in sources), "every source needle found")
    add("VAL3654_2_outputs_exist", all(path.exists() for path in output_paths), "all expected 3654 outputs written")
    csv_status = [parse_csv(path) for path in output_paths if path.suffix.lower() == ".csv"]
    add("VAL3654_3_csv_parse", all(ok and count > 0 for ok, count in csv_status), "all generated CSVs parse with rows")
    add("VAL3654_4_same_interface", {row["observable"] for row in baseline} == {row["observable"] for row in mts}, "baseline and MTS share observable set")
    numeric_baseline = [row for row in baseline if str(row["score_ready"]).lower() == "true"]
    add("VAL3654_5_baseline_numeric_passes", len(numeric_baseline) >= 7 and all(str(row["pass_same_interface"]).lower() == "true" for row in numeric_baseline), "GR/null numeric rows pass same-interface bounds")
    add("VAL3654_6_mts_placeholders_refused", all(row["current_status"] == "BLOCKED_PLACEHOLDER_REFUSED" and str(row["score_ready"]).lower() == "false" for row in mts), "MTS placeholder rows refused")
    add("VAL3654_7_no_mts_pass", not any(str(row["pass_same_interface"]).lower() == "true" for row in mts), "no MTS row passes without numeric values")
    add("VAL3654_8_zero_certificate_refused", all(str(row["accepted_as_zero"]).lower() == "false" for row in certs), "parent zero certificate not accepted")
    add("VAL3654_9_claim_gates_present", {"CG3654_0_same_interface", "CG3654_2_placeholders_refused", "CG3654_3_parent_zero_certificate", "CG3654_4_no_public_claim"}.issubset({row["gate_id"] for row in gates}), "core claim gates present")
    add("VAL3654_10_summary_blocks_mts", any(row["summary_id"] == "SUM3654_1_MTS" and row["current_status"] == "MTS_DRYRUN_BLOCKED_VALUES_MISSING" for row in summary), "summary blocks MTS claim")
    generated = sources + interface + baseline + mts + certs + summary + gates + status + next_target
    add("VAL3654_11_all_nonclaim", not any(str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("claim_allowed", "")).lower() == "true" for row in generated), "all generated rows remain nonclaim")
    add("VAL3654_12_status_honest", status[0]["status"] == "LOCAL_GR_COMPARATOR_DRYRUN_WRITTEN_BASELINE_PASSES_MTS_PLACEHOLDERS_REFUSED", "status keeps dry-run nonclaim")
    doc_text = read_text(DOC)
    add("VAL3654_13_doc_written", "GR_null" in doc_text and "placeholders as zeros" in doc_text and "MTS does **not** pass" in doc_text, "doc records same-interface dry-run and refusal")
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ["*Y5_R2FR_3654*", "3654-Y5-R2FR-*", "Y5_R2FR_3654_*"]:
            leaks.extend(FORMALIZATION.rglob(pattern))
    add("VAL3654_14_no_formalization_leak", not leaks, "no 3654 checkpoint files in formalization-workbench")
    add("VAL3654_15_next_target", next_target[0]["target_doc"].startswith("3655-") and "residual-component-fill" in next_target[0]["target_doc"], "3655 residual fill target selected")
    return rows


def main() -> int:
    ts = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_register(ts)
    interface = comparator_interface_rows(ts)
    baseline = baseline_rows(ts, interface)
    mts = mts_dryrun_rows(ts, interface)
    certs = zero_certificate_audit(ts)
    summary = comparator_summary_rows(ts, baseline, mts, certs)
    gates = claim_gate_rows(ts)
    status = status_rows(ts)
    next_target = next_rows(ts)
    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3654_SOURCE_REGISTER.csv",
        "interface": RESIDUALS / "P8_Y5_R2FR_3654_COMPARATOR_INTERFACE_ROWS.csv",
        "baseline": RESIDUALS / "P8_Y5_R2FR_3654_GR_NULL_BASELINE_DRYRUN_ROWS.csv",
        "mts": RESIDUALS / "P8_Y5_R2FR_3654_MTS_RESIDUAL_DRYRUN_ROWS.csv",
        "certs": RESIDUALS / "P8_Y5_R2FR_3654_PARENT_ZERO_CERTIFICATE_AUDIT.csv",
        "summary": RESIDUALS / "P8_Y5_R2FR_3654_COMPARATOR_SUMMARY.csv",
        "gates": RESIDUALS / "P8_Y5_R2FR_3654_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3654_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3654_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3654_VALIDATION.csv",
    }
    write_csv(outputs["sources"], sources)
    write_csv(outputs["interface"], interface)
    write_csv(outputs["baseline"], baseline)
    write_csv(outputs["mts"], mts)
    write_csv(outputs["certs"], certs)
    write_csv(outputs["summary"], summary)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, interface, baseline, mts, certs, summary, gates, status, next_target)
    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(ts, generated_paths, sources, interface, baseline, mts, certs, summary, gates, status, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3654 validation failed: {failures}", file=sys.stderr)
        return 1
    print(f"wrote 3654 checkpoint with {len(validation)} validation checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3655"
BRANCH_ID = "MTS_R2FR_Y5_PARENT_LOCAL_GR_ZERO_CERTIFICATE_OR_FIRST_COMPONENT_FILL_3655"
DOC = ROOT / "3655-Y5-R2FR-parent-local-GR-zero-certificate-or-first-residual-component-fill.md"


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


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


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


def parse_float(value: object) -> float | None:
    text = str(value).strip()
    if not text or text.lower() in {"symbolic", "vector", "alpha(lambda)", "range-dependent", "operator family"}:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def source_register(ts: str) -> list[dict[str, object]]:
    bounds = LOCAL_BOUNDS / "local_bound_claims.csv"
    specs = [
        ("next_3654", RESIDUALS / "P8_Y5_R2FR_3654_NEXT_TARGET.csv", "3655-Y5-R2FR-parent-local-GR-zero-certificate", "3654 selected this target"),
        ("doc_3654", ROOT / "3654-Y5-R2FR-local-GR-residual-comparator-dryrun-or-parent-zero-certificate.md", "placeholders as zeros", "same-interface comparator and placeholder refusal"),
        ("baseline_3654", RESIDUALS / "P8_Y5_R2FR_3654_GR_NULL_BASELINE_DRYRUN_ROWS.csv", "BL3654_0_gamma", "baseline numeric comparator rows"),
        ("mts_dryrun_3654", RESIDUALS / "P8_Y5_R2FR_3654_MTS_RESIDUAL_DRYRUN_ROWS.csv", "BLOCKED_PLACEHOLDER_REFUSED", "MTS placeholder refusal rows"),
        ("parent_zero_3654", RESIDUALS / "P8_Y5_R2FR_3654_PARENT_ZERO_CERTIFICATE_AUDIT.csv", "PZC3654_0_EH_action", "parent zero certificate audit"),
        ("claim_gates_3654", RESIDUALS / "P8_Y5_R2FR_3654_CLAIM_GATES.csv", "FAILED_UNSIGNED", "zero certificate unsigned gate"),
        ("local_bounds", bounds, "R3_gamma", "numeric PPN and Gdot bound anchors"),
        ("motion_load_02", ROOT / "02-motion-load-local-GR-reduction.md", "motion_load_local_GR_reduction_conditional_not_promoted", "conditional local-GR reduction is not parent promotion"),
        ("EH_ledger_425", ROOT / "425-EH-operator-retained-ledger-and-source-normalization-test-plan.md", "EH-to-Poisson bridge is clean if the parent theory earns", "EH/source premises are explicit retained ledger"),
        ("source_current_3650", ROOT / "3650-Y5-R2FR-EM-source-current-normalization-or-beta-source-alpha-row.md", "WARD_CONSERVATION_NOT_ENOUGH", "source-current zero cannot be inferred from conservation alone"),
        ("matter_sensitivity_3651", ROOT / "3651-Y5-R2FR-matter-representation-source-sensitivity-or-composition-matrix-row.md", "Q_A^X = partial ln M_A^eff / partial Xhat", "composition/source sensitivity vector exists but is unsigned"),
        ("weak_field_3652", ROOT / "3652-Y5-R2FR-weak-field-source-Hamiltonian-GM-calibration-or-source-vector-bound.md", "delta ln mu_obs", "weak-field GM/source calibration law and unsigned local-GR zero contract"),
        ("local_GR_3653", ROOT / "3653-Y5-R2FR-Newton-Poisson-PPN-zero-vector-gate-or-local-GR-residual-fit.md", "Delta_local_GR_abs", "Newton/PPN zero vector gate"),
        ("alpha_mass_1048", ROOT / "1048-Y5-R10-no-extra-F2-no-mass-vertex-parent-action-signature-or-alpha-mass-bound-matrix.md", "LOCAL_GR_NOT_SCORE_READY", "PPN source/readout residuals remain unscored"),
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


def zero_certificate_component_audit(ts: str) -> list[dict[str, object]]:
    previous = load_csv(RESIDUALS / "P8_Y5_R2FR_3654_PARENT_ZERO_CERTIFICATE_AUDIT.csv")
    routes = {
        "q_EH_action": (
            "same-frame EH+Lambda action selection",
            "02 is conditional and 425 says the parent still has to earn the EH/source premises",
            "derive parent operator selection or bound non-EH operator vector",
        ),
        "q_GN_prefactor": (
            "EH prefactor equals measured local G_N after source calibration",
            "3652 derives the fitted-GM calibration law, but the prefactor/source owner is still unsigned",
            "derive source-calibrated EH prefactor or fit a residual vector",
        ),
        "q_Poisson_source": (
            "active source equals inertial/source Hamiltonian density",
            "3652 leaves active/inertial source identity unsigned",
            "derive weak-field source Hamiltonian owner",
        ),
        "q_metric_PPN": (
            "weak-field metric coefficients match GR through PPN order",
            "3653 supplies the vector gate but not the parent weak-field solution",
            "derive first metric coefficient, preferably gamma",
        ),
        "q_readout_PPN": (
            "clock/light/ruler readout descends to the same observed frame",
            "readout frame/no-shadow clause is not parent-signed",
            "derive readout descent or bound readout residuals",
        ),
        "q_boundary_PPN": (
            "boundary/domain terms are silent in local PPN limits",
            "boundary exactness/domain silence remains unsigned",
            "derive boundary silence or source domain projection bounds",
        ),
        "q_nonEH_PPN": (
            "all non-EH operators are absent, topological, or below local bounds",
            "425/1048 keep non-EH and PPN source rows retained rather than closed",
            "derive minimal operator selection or fill coefficient bounds",
        ),
        "q_source_coupling_PPN": (
            "matter/source coupling vector theorem-zero or source-backed bounded",
            "3650-3652 derive source-sensitivity laws but do not sign zero coefficients",
            "derive source-current owner or fill material/source coefficients",
        ),
        "q_time_drift": (
            "G/source/readout drift theorem-zero or below Gdot bound",
            "Gdot row has a real bound, but no MTS drift prediction or zero theorem",
            "derive time-drift zero law or fill Gdot_over_G_MTS",
        ),
        "Delta_local_GR_abs": (
            "all local-GR residual components vanish or are numeric/source-backed",
            "component clauses above are still unsigned",
            "do not promote total envelope until every component is filled or signed",
        ),
    }
    rows = []
    for item in previous:
        route, reason, next_action = routes.get(item["symbol"], ("component-specific theorem-zero", "no parent-owned evidence located", "fill or sign component"))
        can_sign = item.get("certificate_status") == "SIGNED" and item.get("accepted_as_zero") == "True"
        rows.append(
            {
                **base(ts),
                "audit_id": item["certificate_id"].replace("PZC3654", "ZPA3655"),
                "previous_certificate_id": item["certificate_id"],
                "symbol": item["symbol"],
                "attempted_zero_route": route,
                "required_evidence": item["required_evidence"],
                "previous_input_status": item["input_status"],
                "3655_zero_status": "SIGNED_PARENT_ZERO" if can_sign else "UNSIGNED_AFTER_COMPONENT_AUDIT",
                "accepted_as_zero": bool(can_sign),
                "blocker": "" if can_sign else reason,
                "next_action": "carry signed zero into comparator" if can_sign else next_action,
                "claim_allowed": False,
            }
        )
    return rows


def first_component_fill_rows(ts: str) -> list[dict[str, object]]:
    baseline = load_csv(RESIDUALS / "P8_Y5_R2FR_3654_GR_NULL_BASELINE_DRYRUN_ROWS.csv")
    mts = load_csv(RESIDUALS / "P8_Y5_R2FR_3654_MTS_RESIDUAL_DRYRUN_ROWS.csv")
    bounds = {row["row_id"]: row for row in load_csv(LOCAL_BOUNDS / "local_bound_claims.csv")}
    baseline_by_observable = {row["observable"]: row for row in baseline}
    mts_by_observable = {row["observable"]: row for row in mts}

    gamma_bound = bounds["R3_gamma"]
    gdot_bound = bounds["R9_Gdot"]
    gamma_baseline = baseline_by_observable["gamma_minus_1"]
    gdot_baseline = baseline_by_observable["Gdot_over_G"]
    gamma_mts = mts_by_observable["gamma_minus_1"]

    return [
        {
            **base(ts),
            "fill_id": "FCF3655_0_GRnull_gamma",
            "component": "delta_gamma_interface_component",
            "model": "GR_null",
            "observable": "gamma_minus_1",
            "symbol": gamma_baseline["symbol"],
            "value": parse_float(gamma_baseline["value"]),
            "upper_bound": parse_float(gamma_bound["upper_bound"]),
            "units": gamma_bound["units"],
            "bound_row": "R3_gamma",
            "numeric_source_status": "SOURCE_BACKED_NUMERIC_BASELINE",
            "applies_to_MTS": False,
            "score_ready": True,
            "pass_same_interface": True,
            "source_paths": f"{RESIDUALS / 'P8_Y5_R2FR_3654_GR_NULL_BASELINE_DRYRUN_ROWS.csv'}:BL3654_0_gamma;{LOCAL_BOUNDS / 'local_bound_claims.csv'}:R3_gamma",
            "bound_reference": gamma_bound["reference_path_or_url"],
            "current_status": "FIRST_DEFENSIBLE_COMPONENT_FILL_BASELINE_SIDE_ONLY",
            "claim_allowed": False,
        },
        {
            **base(ts),
            "fill_id": "FCF3655_1_GRnull_Gdot",
            "component": "Gdot_interface_component",
            "model": "GR_null",
            "observable": "Gdot_over_G",
            "symbol": gdot_baseline["symbol"],
            "value": parse_float(gdot_baseline["value"]),
            "upper_bound": parse_float(gdot_bound["upper_bound"]),
            "units": gdot_bound["units"],
            "bound_row": "R9_Gdot",
            "numeric_source_status": "SOURCE_BACKED_NUMERIC_BASELINE",
            "applies_to_MTS": False,
            "score_ready": True,
            "pass_same_interface": True,
            "source_paths": f"{RESIDUALS / 'P8_Y5_R2FR_3654_GR_NULL_BASELINE_DRYRUN_ROWS.csv'}:BL3654_6_Gdot;{LOCAL_BOUNDS / 'local_bound_claims.csv'}:R9_Gdot",
            "bound_reference": gdot_bound["reference_path_or_url"],
            "current_status": "SECOND_DEFENSIBLE_COMPONENT_FILL_BASELINE_SIDE_ONLY",
            "claim_allowed": False,
        },
        {
            **base(ts),
            "fill_id": "FCF3655_2_MTS_gamma_refusal",
            "component": "delta_gamma_interface_component",
            "model": "MTS_local_GR_residual_vector",
            "observable": "gamma_minus_1",
            "symbol": gamma_mts["symbol"],
            "value": gamma_mts["value"],
            "upper_bound": parse_float(gamma_bound["upper_bound"]),
            "units": gamma_bound["units"],
            "bound_row": "R3_gamma",
            "numeric_source_status": "MTS_VALUE_MISSING_PLACEHOLDER_REFUSED",
            "applies_to_MTS": True,
            "score_ready": False,
            "pass_same_interface": False,
            "source_paths": f"{RESIDUALS / 'P8_Y5_R2FR_3654_MTS_RESIDUAL_DRYRUN_ROWS.csv'}:MTS3654_0_gamma;{LOCAL_BOUNDS / 'local_bound_claims.csv'}:R3_gamma",
            "bound_reference": gamma_bound["reference_path_or_url"],
            "current_status": "MTS_COMPONENT_NOT_FILLED_PLACEHOLDER_REFUSED",
            "claim_allowed": False,
        },
    ]


def comparator_update_rows(ts: str, fills: list[dict[str, object]], zero_audit: list[dict[str, object]]) -> list[dict[str, object]]:
    signed = [row for row in zero_audit if str(row["accepted_as_zero"]).lower() == "true"]
    return [
        {
            **base(ts),
            "update_id": "CU3655_0_baseline_component_fill",
            "object": "GR_null_gamma_and_Gdot",
            "status": "BASELINE_COMPONENTS_SOURCE_BACKED",
            "meaning": "the comparator has real baseline-side numeric components for gamma and Gdot, not MTS evidence",
            "claim_allowed": False,
        },
        {
            **base(ts),
            "update_id": "CU3655_1_mts_component_status",
            "object": "delta_gamma_MTS",
            "status": "MTS_VALUE_STILL_MISSING_PLACEHOLDER_REFUSED",
            "meaning": "the first actual MTS component must be derived or source-backed next",
            "claim_allowed": False,
        },
        {
            **base(ts),
            "update_id": "CU3655_2_zero_certificate_status",
            "object": "parent_local_GR_zero_certificate",
            "status": "NO_COMPONENT_SIGNED" if not signed else "PARTIAL_COMPONENT_SIGNED",
            "meaning": f"{len(signed)} parent-zero components accepted; total local-GR certificate remains unavailable",
            "claim_allowed": False,
        },
    ]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("CG3655_0_zero_audit_done", "component-by-component zero proof attempted", "PASSED_AUDIT", "no parent-zero component was accepted without signed evidence"),
        ("CG3655_1_baseline_not_mts", "baseline numeric rows cannot be counted as MTS residual values", "ACTIVE_GUARD", "prevents the comparator from laundering GR/null zeros into MTS"),
        ("CG3655_2_placeholder_refusal", "MTS placeholders remain unscoreable", "PASSED_REFUSAL", "delta_gamma_MTS and siblings remain blocked until numeric/source-backed or theorem-zero"),
        ("CG3655_3_no_local_GR_claim", "no Newton/PPN/local-GR pass is claimed", "ACTIVE", "3655 is a comparator/certificate checkpoint only"),
        ("CG3655_4_next", "next step must fill one actual MTS local-GR residual component", "FIRST_MTS_COMPONENT_NEXT", "recommended first target is delta_gamma_MTS via weak-field metric coefficient derivation"),
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
            "status": "ZERO_CERTIFICATE_UNSIGNED_BASELINE_SIDE_COMPONENTS_FILLED_MTS_VALUE_STILL_MISSING",
            "summary": "3655 attempts the parent local-GR zero certificate component-by-component, accepts no unsigned zeros, and fills only baseline-side gamma/Gdot comparator components as real numeric rows.",
            "claim_ceiling": "no MTS local-GR, Newtonian, PPN, source-calibration, clock, orbital, R10, WEP, or EH-dominance pass is claimed",
            "useful_result": "The next leap is now pinned: derive or source one actual MTS residual component, preferably delta_gamma_MTS, rather than circling the whole local-GR vector.",
        }
    ]


def next_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3655_0",
            "target_doc": "3656-Y5-R2FR-first-MTS-local-GR-residual-component-acquisition.md",
            "target_script": "scripts/Y5_R2FR_3656_first_MTS_local_GR_residual_component_acquisition.py",
            "objective": "derive or source the first actual MTS local-GR residual component, with delta_gamma_MTS as the preferred target through the weak-field metric coefficient route",
            "success_gate": "one MTS component is numeric/source-backed or parent theorem-zero; GR/null baseline rows do not count toward this gate",
        }
    ]


def write_doc(sources, zero_audit, fills, updates, gates, status, next_target) -> None:
    lines = [
        "# 3655 - Parent local-GR zero certificate or first residual component fill",
        "",
        f"**Status:** {status[0]['summary']}",
        "",
        f"**Claim ceiling:** {status[0]['claim_ceiling']}.",
        "",
        "## Main result",
        "",
        "The zero-certificate route was tried component-by-component. Nothing is promoted: every MTS parent-zero clause remains unsigned after the audit.",
        "",
        "The first defensible numeric fill is therefore baseline-side only: `GR_null` gamma and `GR_null` Gdot stay as real comparator controls, while `delta_gamma_MTS` remains `MISSING_delta_gamma_MTS` and unscoreable. This is not a local-GR pass; it is the guardrail that stops us from counting GR/null zeros as MTS work.",
        "",
        "So the live target is now narrow and real: fill or derive one actual MTS component, preferably `delta_gamma_MTS`, from the weak-field metric coefficient route.",
        "",
        "## Zero-certificate component audit",
    ]
    for row in zero_audit:
        lines.append(f"- `{row['audit_id']}`: `{row['symbol']}` - {row['3655_zero_status']} - next: {row['next_action']}")
    lines.extend(["", "## Component fill rows"])
    for row in fills:
        lines.append(f"- `{row['fill_id']}`: `{row['model']}` `{row['symbol']}` - {row['current_status']}")
    lines.extend(["", "## Comparator updates"])
    for row in updates:
        lines.append(f"- `{row['update_id']}`: {row['status']} - {row['meaning']}")
    lines.extend(["", "## Claim gates"])
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: {row['status']} - {row['gate']}")
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


def validate(ts, output_paths, sources, zero_audit, fills, updates, gates, status, next_target) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

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

    add("VAL3655_0_sources_exist", all(row["exists"] for row in sources), "every cited local source path exists")
    add("VAL3655_1_needles_found", all(row["needle_found"] for row in sources), "every source needle found")
    add("VAL3655_2_outputs_exist", all(path.exists() for path in output_paths), "all expected 3655 outputs written")
    csv_status = [parse_csv(path) for path in output_paths if path.suffix.lower() == ".csv"]
    add("VAL3655_3_csv_parse", all(ok and count > 0 for ok, count in csv_status), "all generated CSVs parse with rows")
    zero_symbols = {row["symbol"] for row in zero_audit}
    add("VAL3655_4_zero_audit_complete", len(zero_audit) >= 10 and "q_EH_action" in zero_symbols and "Delta_local_GR_abs" in zero_symbols and "delta_gamma_MTS" not in zero_symbols, "all parent-zero certificate clauses audited without confusing residual symbols")
    add("VAL3655_5_no_unsigned_zero_accepted", not any(str(row["accepted_as_zero"]).lower() == "true" for row in zero_audit), "no zero component accepted from unsigned evidence")
    baseline_fills = [row for row in fills if str(row["applies_to_MTS"]).lower() == "false"]
    add("VAL3655_6_baseline_fill_numeric", len(baseline_fills) >= 2 and all(parse_float(row["value"]) is not None and parse_float(row["upper_bound"]) is not None for row in baseline_fills), "baseline-side filled components are numeric and source-backed")
    mts_fills = [row for row in fills if str(row["applies_to_MTS"]).lower() == "true"]
    add("VAL3655_7_mts_placeholder_refused", len(mts_fills) == 1 and mts_fills[0]["current_status"] == "MTS_COMPONENT_NOT_FILLED_PLACEHOLDER_REFUSED" and str(mts_fills[0]["score_ready"]).lower() == "false", "MTS component remains refused rather than silently zero")
    add("VAL3655_8_no_mts_claim", not any(str(row.get("applies_to_MTS", "")).lower() == "true" and str(row.get("score_ready", "")).lower() == "true" for row in fills), "no MTS row is made score-ready")
    add("VAL3655_9_updates_block_mts", any(row["status"] == "MTS_VALUE_STILL_MISSING_PLACEHOLDER_REFUSED" for row in updates), "comparator update keeps MTS value missing")
    add("VAL3655_10_claim_gates_present", {"CG3655_0_zero_audit_done", "CG3655_1_baseline_not_mts", "CG3655_2_placeholder_refusal", "CG3655_3_no_local_GR_claim", "CG3655_4_next"}.issubset({row["gate_id"] for row in gates}), "core claim gates present")
    generated = sources + zero_audit + fills + updates + gates + status + next_target
    add("VAL3655_11_all_nonclaim", not any(str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("claim_allowed", "")).lower() == "true" for row in generated), "all generated rows remain nonclaim")
    doc_text = read_text(DOC)
    add("VAL3655_12_doc_written", "baseline-side only" in doc_text and "not a local-GR pass" in doc_text and "delta_gamma_MTS" in doc_text, "doc records baseline-only fill and actual MTS next target")
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ["*Y5_R2FR_3655*", "3655-Y5-R2FR-*", "Y5_R2FR_3655_*"]:
            leaks.extend(FORMALIZATION.rglob(pattern))
    add("VAL3655_13_no_formalization_leak", not leaks, "no 3655 checkpoint files in formalization-workbench")
    add("VAL3655_14_next_target", next_target[0]["target_doc"].startswith("3656-") and "first-MTS" in next_target[0]["target_doc"], "3656 first actual MTS component target selected")
    return rows


def main() -> int:
    ts = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_register(ts)
    zero_audit = zero_certificate_component_audit(ts)
    fills = first_component_fill_rows(ts)
    updates = comparator_update_rows(ts, fills, zero_audit)
    gates = claim_gate_rows(ts)
    status = status_rows(ts)
    next_target = next_rows(ts)
    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3655_SOURCE_REGISTER.csv",
        "zero_audit": RESIDUALS / "P8_Y5_R2FR_3655_ZERO_CERTIFICATE_COMPONENT_AUDIT.csv",
        "fills": RESIDUALS / "P8_Y5_R2FR_3655_FIRST_COMPONENT_FILL_ROWS.csv",
        "updates": RESIDUALS / "P8_Y5_R2FR_3655_COMPARATOR_UPDATE_ROWS.csv",
        "gates": RESIDUALS / "P8_Y5_R2FR_3655_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3655_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3655_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3655_VALIDATION.csv",
    }
    write_csv(outputs["sources"], sources)
    write_csv(outputs["zero_audit"], zero_audit)
    write_csv(outputs["fills"], fills)
    write_csv(outputs["updates"], updates)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, zero_audit, fills, updates, gates, status, next_target)
    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(ts, generated_paths, sources, zero_audit, fills, updates, gates, status, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3655 validation failed: {failures}", file=sys.stderr)
        return 1
    print(f"wrote 3655 checkpoint with {len(validation)} validation checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

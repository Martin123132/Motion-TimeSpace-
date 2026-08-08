from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT_ID = "2549"
BRANCH_ID = "MTS_R2FR_FIRST_DELTA_REF_BOUND_VALUE_RUNNER_OR_SAME_FRAME_DENOMINATOR_SOURCE_2549"
POST_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = POST_ROOT.parent
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2549-Y5-R2FR-first-Delta-ref-bound-value-runner-or-same-frame-denominator-source.md"
FORMALIZATION_WORKBENCH = PROJECT_ROOT / "formalization-workbench"

OUTPUTS = {
    "source": RESIDUALS / "P8_Y5_NO_SHADOW_2549_SOURCE_REGISTER.csv",
    "denominator": RESIDUALS / "P8_Y5_NO_SHADOW_2549_DENOMINATOR_SOURCE_GATE.csv",
    "candidates": RESIDUALS / "P8_Y5_NO_SHADOW_2549_BOUND_VALUE_CANDIDATES.csv",
    "runner": RESIDUALS / "P8_Y5_NO_SHADOW_2549_NO_CANCELLATION_RUNNER_RESULTS.csv",
    "claims": RESIDUALS / "P8_Y5_NO_SHADOW_2549_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_NO_SHADOW_2549_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_NO_SHADOW_2549_NEXT_TARGET.csv",
    "copies": RESIDUALS / "P8_Y5_NO_SHADOW_2549_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2549_VALIDATION.csv",
}

BRANCH_COPIES = {
    "denominator": POST_ROOT / "source-intake" / "rab-sector" / "acquisition-queue" / "JR2549_DENOMINATOR_SOURCE_GATE_NONCLAIM.csv",
    "runner": POST_ROOT / "source-intake" / "rab-sector" / "acquisition-queue" / "JR2549_NO_CANCELLATION_RUNNER_RESULTS_NONCLAIM.csv",
    "hamiltonian": POST_ROOT / "source-intake" / "hamiltonian-source" / "Delta_ref_no_cancellation_runner_2549_NONCLAIM.csv",
    "local": POST_ROOT / "source-intake" / "local_bounds" / "Delta_ref_no_cancellation_runner_2549_NONCLAIM.csv",
}

SOURCE_SPECS = [
    (
        "SRC2549_00_2548_doc",
        "2548-Y5-R2FR-parent-action-signature-hunt-or-reference-route-demotion.md",
        ["REFERENCE_ZERO_ROUTE_DEMOTED_TO_EXPLICIT_CLOSURE_FOR_CURRENT_MTS", "BND2548_4_same_frame_denominator", "NEXT2548_0_selected", "VAL2548_OVERALL"],
        "handoff selecting finite Delta_ref bound path",
    ),
    (
        "SRC2549_01_2548_bound_ledger",
        "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2548_DELTA_REF_BOUND_ACQUISITION_LEDGER.csv",
        ["BND2548_4_same_frame_denominator", "MISSING_VALUE", "BND2548_5_no_cancellation_total"],
        "active finite bound targets",
    ),
    (
        "SRC2549_02_2547_bounds",
        "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2547_DELTA_REF_BOUND_ROWS.csv",
        ["DRB2547_4_total_absolute", "NOT_COMPUTED_COMPONENTS_MISSING"],
        "active Delta_ref bound schema",
    ),
    (
        "SRC2549_03_2459_doc",
        "2459-Y5-R2FR-first-Delta-ref-bound-value-runner-or-same-frame-denominator-source.md",
        ["RUN2459_live", "RUN2459_smoke", "VAL2459_OVERALL"],
        "older operational no-cancellation runner precedent",
    ),
    (
        "SRC2549_04_1006_denominator",
        "1006-Y5-R10-MHref-positive-same-frame-denominator-or-Htau-source-row.md",
        ["MHS1006_0_Htau_minus_Href", "CG1006_0_MHref_positive_same_frame", "ORBITAL_GM_SUBSTITUTION_REJECTED", "V1006_SUMMARY"],
        "H_tau-H_ref denominator schema and orbital-GM rejection",
    ),
    (
        "SRC2549_05_1017_reference_lock",
        "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md",
        ["HRL1017_5_MHref_denominator", "MHR1017_0_M_H_ref_denominator", "CG1017_4_MHref_claim"],
        "Hamiltonian/source charge denominator blocker",
    ),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rel(path: Path) -> str:
    try:
        return path.relative_to(POST_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def contains(path: Path, needle: str) -> bool:
    return path.exists() and needle in read_text(path)


def stamp(row: dict[str, object]) -> dict[str, object]:
    return {
        "timestamp_utc": utc_now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": "false",
        "claim_allowed": "false",
        **row,
    }


def no_claim(extra: dict[str, object] | None = None) -> dict[str, object]:
    row: dict[str, object] = {
        "parent_signed": "false",
        "theorem_zero": "false",
        "numeric_prediction_present": "false",
        "same_branch_locked": "false",
        "projection_ready": "false",
        "score_ready": "false",
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }
    if extra:
        row.update(extra)
    return row


def source_register() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, source_path, needles, role in SOURCE_SPECS:
        path = POST_ROOT / source_path
        rows.append(
            stamp(
                {
                    "row_id": source_id,
                    "source_path": str(path),
                    "exists": str(path.exists()).lower(),
                    "needles": "; ".join(needles),
                    "needles_found": str(all(contains(path, needle) for needle in needles)).lower(),
                    "source_role": role,
                }
            )
        )
    return rows


def denominator_rows() -> list[dict[str, object]]:
    rows = [
        {
            "row_id": "DEN2549_0_live_MHref_schema",
            "quantity": "M_H_ref",
            "method": "positive dressed same-frame Hamiltonian/Noether charge",
            "value": "MISSING_STABLE_MH_REF",
            "units": "MISSING_UNITS",
            "source_path": str(POST_ROOT / "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md"),
            "equation_ref": "MHR1017_0_M_H_ref_denominator",
            "same_frame": "false",
            "positive": "false",
            "orbital_gm_import": "false",
            "status": "BLOCKED_MISSING_STABLE_MH_REF",
        },
        {
            "row_id": "DEN2549_1_live_Htau_minus_Href_schema",
            "quantity": "M_H_ref",
            "method": "H_tau[S_link]-H_ref",
            "value": "MISSING_H_TAU_AND_H_REF",
            "units": "MISSING_UNITS",
            "source_path": str(POST_ROOT / "1006-Y5-R10-MHref-positive-same-frame-denominator-or-Htau-source-row.md"),
            "equation_ref": "MHS1006_0_Htau_minus_Href",
            "same_frame": "false",
            "positive": "false",
            "orbital_gm_import": "false",
            "status": "BLOCKED_MISSING_HAMILTONIAN_VALUES",
        },
        {
            "row_id": "DEN2549_2_rejected_orbital_GM",
            "quantity": "GM_orbit/G_ref",
            "method": "observed orbital readout substitution",
            "value": "REJECTED",
            "units": "mass",
            "source_path": str(POST_ROOT / "1006-Y5-R10-MHref-positive-same-frame-denominator-or-Htau-source-row.md"),
            "equation_ref": "MHR1006_3_orbital_GM_substitution",
            "same_frame": "false",
            "positive": "unknown",
            "orbital_gm_import": "true",
            "status": "REJECTED_CIRCULAR_DENOMINATOR",
        },
        {
            "row_id": "DEN2549_3_toy_smoke_denominator",
            "quantity": "N_E_smoke",
            "method": "internal smoke denominator only",
            "value": "1.0",
            "units": "arb",
            "source_path": "SELF_TEST_ONLY",
            "equation_ref": "SMOKE2549",
            "same_frame": "true",
            "positive": "true",
            "orbital_gm_import": "false",
            "status": "SCHEMA_SMOKE_ONLY",
        },
    ]
    return [stamp(no_claim(row)) for row in rows]


def bound_value_rows() -> list[dict[str, object]]:
    live_source = POST_ROOT / "source-intake" / "mts_residuals" / "P8_Y5_NO_SHADOW_2548_DELTA_REF_BOUND_ACQUISITION_LEDGER.csv"
    rows = [
        ("BVC2549_0_live_metric_leak", "C_sigma*max(||D_q sigma_AB||,||D_source sigma_AB||)", "live", "MISSING_VALUE", "MISSING_UNITS", "DEN2549_0_live_MHref_schema", str(live_source), "BND2548_0_metric_leak"),
        ("BVC2549_1_live_tau_leak", "C_tau*max(||D_q tau||,||D_source tau||)", "live", "MISSING_VALUE", "MISSING_UNITS", "DEN2549_0_live_MHref_schema", str(live_source), "BND2548_1_tau_leak"),
        ("BVC2549_2_live_counterterm_leak", "max(|D_q B_ct|,|D_source B_ct|)", "live", "MISSING_VALUE", "MISSING_UNITS", "DEN2549_0_live_MHref_schema", str(live_source), "BND2548_2_counterterm_leak"),
        ("BVC2549_3_live_topological_leak", "C_top*max(|D_q C_top|,|D_source C_top|)", "live", "MISSING_VALUE", "MISSING_UNITS", "DEN2549_0_live_MHref_schema", str(live_source), "BND2548_3_topological_leak"),
        ("BVC2549_4_smoke_metric_leak", "C_sigma*max(||D_q sigma_AB||,||D_source sigma_AB||)", "smoke", "1.0e-8", "arb", "DEN2549_3_toy_smoke_denominator", "SELF_TEST_ONLY", "SMOKE2549"),
        ("BVC2549_5_smoke_tau_leak", "C_tau*max(||D_q tau||,||D_source tau||)", "smoke", "2.0e-8", "arb", "DEN2549_3_toy_smoke_denominator", "SELF_TEST_ONLY", "SMOKE2549"),
        ("BVC2549_6_smoke_counterterm_leak", "max(|D_q B_ct|,|D_source B_ct|)", "smoke", "3.0e-9", "arb", "DEN2549_3_toy_smoke_denominator", "SELF_TEST_ONLY", "SMOKE2549"),
        ("BVC2549_7_smoke_topological_leak", "C_top*max(|D_q C_top|,|D_source C_top|)", "smoke", "0.0", "arb", "DEN2549_3_toy_smoke_denominator", "SELF_TEST_ONLY", "SMOKE2549"),
    ]
    return [
        stamp(
            no_claim(
                {
                    "row_id": row_id,
                    "quantity": quantity,
                    "component_group": group,
                    "value": value,
                    "units": units,
                    "denominator_id": denom,
                    "source_path": source,
                    "equation_ref": equation,
                }
            )
        )
        for row_id, quantity, group, value, units, denom, source, equation in rows
    ]


def parse_float(value: object) -> float | None:
    try:
        parsed = float(str(value))
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def runner_rows(denominators: list[dict[str, object]], candidates: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    denom_by_id = {str(row["row_id"]): row for row in denominators}
    for group, denom_id in [("live", "DEN2549_0_live_MHref_schema"), ("smoke", "DEN2549_3_toy_smoke_denominator")]:
        denom = denom_by_id[denom_id]
        components = [row for row in candidates if row["component_group"] == group]
        blockers: list[str] = []
        denom_value = parse_float(denom["value"])
        if denom.get("valid_for_claim") != "true":
            blockers.append("DENOMINATOR_VALID_FOR_CLAIM_FALSE")
        if denom.get("same_frame") != "true":
            blockers.append("DENOMINATOR_NOT_SAME_FRAME")
        if denom.get("positive") != "true":
            blockers.append("DENOMINATOR_NOT_POSITIVE")
        if denom.get("orbital_gm_import") == "true":
            blockers.append("ORBITAL_GM_IMPORT_REJECTED")
        if denom_value is None or denom_value <= 0:
            blockers.append("MISSING_OR_NONPOSITIVE_DENOMINATOR_VALUE")
        values: list[float] = []
        missing: list[str] = []
        for component in components:
            value = parse_float(component["value"])
            if value is None:
                missing.append(str(component["row_id"]))
            else:
                values.append(abs(value))
            if component.get("valid_for_claim") != "true":
                blockers.append("COMPONENT_VALID_FOR_CLAIM_FALSE")
        if missing:
            blockers.append("MISSING_COMPONENT_VALUES:" + ";".join(missing))
        if denom_value is not None and denom_value > 0 and not missing:
            component_sum = sum(values)
            bound = component_sum / denom_value
            status = "COMPUTED_NONCLAIM" if group == "smoke" else "COMPUTED_BUT_NONCLAIM"
        else:
            component_sum = "NOT_COMPUTED"
            bound = "NOT_COMPUTED"
            status = "BLOCKED_NOT_COMPUTED"
        rows.append(
            stamp(
                no_claim(
                    {
                        "row_id": f"RUN2549_{group}",
                        "component_group": group,
                        "denominator_id": denom_id,
                        "status": status,
                        "component_sum_abs": component_sum,
                        "denominator_value": denom_value if denom_value is not None else "NOT_NUMERIC",
                        "Delta_ref_bound_over_denominator": bound,
                        "blockers": ";".join(dict.fromkeys(blockers)),
                    }
                )
            )
        )
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    rows = [
        ("CG2549_0_runner_operational", "no-cancellation finite Delta_ref runner works on numeric schema rows", "PASS_NONCLAIM_SMOKE", "smoke group computes a nonclaim absolute-sum residual"),
        ("CG2549_1_live_denominator", "live same-frame N_E/M_H_ref denominator is available", "FAIL", "1006/1017 denominator candidates remain missing or blocked"),
        ("CG2549_2_orbital_GM", "orbital GM can fill denominator", "REFUSED", "orbital GM substitution is circular for GR/Newton reduction proof"),
        ("CG2549_3_live_bound_values", "live metric/tau/counterterm/topology leak values are sourced", "FAIL", "component values are missing and valid_for_claim=false"),
        ("CG2549_4_local_GR_Newton", "local GR/Newton/PPN branch passes from finite Delta_ref bound", "FAIL_NONCLAIM", "live runner result is blocked and smoke result is nonclaim"),
    ]
    return [
        stamp(no_claim({"row_id": row_id, "gate": gate, "gate_status": status, "claim_effect": effect}))
        for row_id, gate, status, effect in rows
    ]


def decision_rows() -> list[dict[str, object]]:
    rows = [
        {
            "row_id": "DEC2549_0_denominator_first",
            "decision": "finite Delta_ref path is denominator-first",
            "reason": "all residual bounds divide by M_H_ref/N_E; without same-frame positivity, component values are not claim-grade",
            "effect": "do not score live finite residuals until denominator is sourced",
        },
        {
            "row_id": "DEC2549_1_orbital_GM_refused",
            "decision": "reject orbital GM as denominator filler",
            "reason": "that imports Newton/GR readout into the theorem meant to derive it",
            "effect": "M_H_ref must come from parent Hamiltonian/source charge or remain blocked",
        },
        {
            "row_id": "DEC2549_2_smoke_nonclaim",
            "decision": "keep smoke row as schema validation only",
            "reason": "it verifies absolute-sum runner behavior without measuring MTS",
            "effect": "future sourced rows can reuse the runner",
        },
        {
            "row_id": "DEC2549_3_next_derivation",
            "decision": "attack same-frame Hamiltonian denominator next",
            "reason": "a sourced denominator unlocks finite residual testing and any future zero-route normalization",
            "effect": "2550 should derive or formally bound M_H_ref before component-value chasing",
        },
    ]
    return [stamp(no_claim(row)) for row in rows]


def next_rows() -> list[dict[str, object]]:
    rows = [
        {
            "row_id": "NEXT2549_0_selected",
            "priority": "selected",
            "next_file": "2550-Y5-R2FR-same-frame-Hamiltonian-denominator-derivation-or-retain-local-bound-block.md",
            "next_script": "scripts/Y5_R2FR_same_frame_Hamiltonian_denominator_derivation_or_retain_local_bound_block_2550.py",
            "success_condition": "derive a positive same-frame M_H_ref/N_E from parent Hamiltonian charge with fixed reference and tau/coframe lock",
            "fallback_condition": "prove why finite Delta_ref local scoring must remain blocked and retain nonclaim denominator ledger",
        },
        {
            "row_id": "NEXT2549_1_parallel",
            "priority": "parallel",
            "next_file": "2550b-Y5-R2FR-first-boundary-leak-source-values.md",
            "next_script": "scripts/Y5_R2FR_first_boundary_leak_source_values_2550b.py",
            "success_condition": "source at least one finite metric/tau/counterterm leak bound with units and equation path",
            "fallback_condition": "retain MISSING_VALUE rows and do not compute live Delta_ref",
        },
    ]
    return [stamp(no_claim(row)) for row in rows]


def branch_copy_rows() -> list[dict[str, object]]:
    copies = {
        BRANCH_COPIES["denominator"]: read_csv(OUTPUTS["denominator"]),
        BRANCH_COPIES["runner"]: read_csv(OUTPUTS["runner"]),
        BRANCH_COPIES["hamiltonian"]: read_csv(OUTPUTS["runner"]),
        BRANCH_COPIES["local"]: read_csv(OUTPUTS["runner"]),
    }
    rows: list[dict[str, object]] = []
    for path, payload in copies.items():
        write_csv(path, payload)
        rows.append(
            stamp(
                {
                    "row_id": f"COPY2549_{len(rows)}",
                    "copy_path": str(path),
                    "exists": str(path.exists()).lower(),
                    "purpose": "nonclaim branch handoff copy",
                }
            )
        )
    return rows


def csv_has(path: Path, needle: str) -> bool:
    return path.exists() and needle in read_text(path)


def all_flags_false(paths: list[Path]) -> bool:
    watched = {"valid_for_claim", "claim_allowed", "score_ready", "parent_signed", "theorem_zero", "numeric_prediction_present"}
    for path in paths:
        for row in read_csv(path):
            for key in watched.intersection(row):
                if str(row[key]).strip().lower() in {"true", "yes", "1", "pass_for_claim"}:
                    return False
    return True


def validation_rows(outputs: dict[str, Path], sources: list[dict[str, object]]) -> list[dict[str, object]]:
    generated = list(outputs.values())
    generated_before_validation = [path for key, path in outputs.items() if key != "validation"]
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2549_00_required_sources_exist", all(row["exists"] == "true" for row in sources), "all required source paths exist"))
    checks.append(("VAL2549_01_required_needles_found", all(row["needles_found"] == "true" for row in sources), "all source needles found"))
    checks.append(("VAL2549_02_outputs_exist", all(path.exists() for path in generated_before_validation), "all 2549 output files written before validation"))
    csv_parse_ok = True
    for path in generated_before_validation:
        try:
            csv_parse_ok = csv_parse_ok and len(read_csv(path)) > 0
        except Exception:
            csv_parse_ok = False
    checks.append(("VAL2549_03_csv_parse", csv_parse_ok, "all generated CSV files parse and contain rows"))
    checks.append(("VAL2549_04_denominator_gate_written", csv_has(outputs["denominator"], "DEN2549_2_rejected_orbital_GM") and csv_has(outputs["denominator"], "REJECTED_CIRCULAR_DENOMINATOR"), "denominator gate includes live blockers and orbital-GM rejection"))
    checks.append(("VAL2549_05_live_runner_blocked", csv_has(outputs["runner"], "RUN2549_live") and csv_has(outputs["runner"], "BLOCKED_NOT_COMPUTED"), "live residual is blocked rather than computed"))
    checks.append(("VAL2549_06_smoke_runner_computes", csv_has(outputs["runner"], "RUN2549_smoke") and csv_has(outputs["runner"], "COMPUTED_NONCLAIM") and csv_has(outputs["runner"], "3.3e-08"), "smoke residual computes no-cancellation absolute sum"))
    checks.append(("VAL2549_07_no_claim_flags", all_flags_false(generated_before_validation + list(BRANCH_COPIES.values())), "all generated claim/readiness flags remain negative"))
    checks.append(("VAL2549_08_claim_gates_safe", csv_has(outputs["claims"], "CG2549_4_local_GR_Newton") and csv_has(outputs["claims"], "FAIL_NONCLAIM"), "local-GR/PPN/Newton claims remain blocked"))
    checks.append(("VAL2549_09_next_selected", csv_has(outputs["next"], "NEXT2549_0_selected") and csv_has(outputs["next"], "2550-Y5-R2FR-same-frame-Hamiltonian-denominator-derivation-or-retain-local-bound-block.md"), "same-frame denominator target selected"))
    checks.append(("VAL2549_10_branch_copies", all(path.exists() for path in BRANCH_COPIES.values()), "all nonclaim branch copies exist"))
    checks.append(("VAL2549_11_formalization_untouched", FORMALIZATION_WORKBENCH.exists() and all(str(path).startswith(str(POST_ROOT)) for path in generated + list(BRANCH_COPIES.values()) + [DOC_PATH]), "generator writes only under post-checkpoint-work"))
    checks.append(("VAL2549_12_pycache_absent", not (POST_ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"))
    overall = all(ok for _, ok, _ in checks)
    rows = [stamp({"row_id": row_id, "status": "PASS" if ok else "FAIL", "detail": detail}) for row_id, ok, detail in checks]
    rows.append(
        stamp(
            {
                "row_id": "VAL2549_OVERALL",
                "status": "PASS" if overall else "FAIL",
                "detail": "2549 installs the active denominator-first no-cancellation Delta_ref runner; smoke computes, live claims remain blocked",
            }
        )
    )
    return rows


def table(columns: list[str], rows: list[dict[str, object]]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, sep]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(col, "")).replace("\n", " ") for col in columns) + " |")
    return "\n".join(lines)


def write_doc(outputs: dict[str, Path]) -> None:
    sources = read_csv(outputs["source"])
    denominators = read_csv(outputs["denominator"])
    candidates = read_csv(outputs["candidates"])
    runner = read_csv(outputs["runner"])
    claims = read_csv(outputs["claims"])
    decision = read_csv(outputs["decision"])
    next_target = read_csv(outputs["next"])
    validation = read_csv(outputs["validation"])

    md = f"""# 2549 - first Delta-ref bound value runner or same-frame denominator source

## Result

2549 installs the active finite `Delta_ref` no-cancellation runner.

The live branch is refused exactly where it should be refused: no positive same-frame `M_H_ref/N_E`, no live residual
score.  Orbital GM is explicitly rejected as a circular denominator.  A smoke group computes the absolute-sum residual,
so the machinery is ready for future sourced rows, but the smoke result is nonclaim.

No `Delta_ref`, local GR, Newton, PPN, clock, orbital, R10, or GitHub/public claim is made.

## Source Register

{table(["row_id", "source_path", "exists", "needles_found", "source_role"], sources)}

## Denominator Source Gate

{table(["row_id", "quantity", "method", "value", "units", "equation_ref", "same_frame", "positive", "orbital_gm_import", "status"], denominators)}

## Bound Value Candidates

{table(["row_id", "quantity", "component_group", "value", "units", "denominator_id", "equation_ref"], candidates)}

## No-cancellation Runner Results

{table(["row_id", "component_group", "denominator_id", "status", "component_sum_abs", "denominator_value", "Delta_ref_bound_over_denominator", "blockers"], runner)}

## Claim Gates

{table(["row_id", "gate", "gate_status", "claim_effect"], claims)}

## Decision Ledger

{table(["row_id", "decision", "reason", "effect"], decision)}

## Next Target

{table(["row_id", "priority", "next_file", "success_condition", "fallback_condition"], next_target)}

## Validation

{table(["row_id", "status", "detail"], validation)}

## Practical Status

This is denominator-first now.  The theory cannot honestly use finite local residual scoring until `M_H_ref/N_E` is
parent-owned, positive, same-frame, and non-circular.  The next useful strike is therefore not another `Delta_ref=0`
proof; it is the same-frame Hamiltonian denominator derivation or a hard block that says local finite scoring is still
unavailable.
"""
    DOC_PATH.write_text(md, encoding="utf-8")


def remove_pycache() -> None:
    pycache = POST_ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> int:
    remove_pycache()
    sources = source_register()
    write_csv(OUTPUTS["source"], sources)
    denominators = denominator_rows()
    candidates = bound_value_rows()
    write_csv(OUTPUTS["denominator"], denominators)
    write_csv(OUTPUTS["candidates"], candidates)
    write_csv(OUTPUTS["runner"], runner_rows(denominators, candidates))
    write_csv(OUTPUTS["claims"], claim_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_rows())
    write_csv(OUTPUTS["copies"], branch_copy_rows())
    validation = validation_rows(OUTPUTS, sources)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(OUTPUTS)
    remove_pycache()

    for row in validation:
        line = f"{row['row_id']},{row['status']},{row['detail']}"
        print(line.encode("ascii", errors="replace").decode("ascii"))
    return 0 if validation[-1]["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

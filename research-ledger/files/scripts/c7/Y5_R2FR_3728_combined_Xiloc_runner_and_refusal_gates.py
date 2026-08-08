from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3728"
BRANCH_ID = "MTS_R2FR_Y5_COMBINED_XILOC_RUNNER_AND_REFUSAL_GATES_3728"
DOC = ROOT / "3728-Y5-R2FR-combined-Xiloc-runner-and-refusal-gates.md"

DOC_3727 = ROOT / "3727-Y5-R2FR-UH-local-unit-map-schema-or-symbolic-operator-lock.md"
NEXT_3727 = RESIDUALS / "P8_Y5_R2FR_3727_NEXT_TARGET.csv"
RUNNER_3727 = RESIDUALS / "P8_Y5_R2FR_3727_UH_RUNNER_STATUS.csv"
RUNNER_3726 = RESIDUALS / "P8_Y5_R2FR_3726_GRAM_RUNNER_STATUS.csv"
LAW_3724 = RESIDUALS / "P8_Y5_R2FR_3724_MEAN_GAP_LAW_ROWS.csv"
PACK_3725 = RESIDUALS / "P8_Y5_R2FR_3725_FINITE_BOUND_PACK_ROWS.csv"


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
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def try_float(value: object) -> float | None:
    try:
        parsed = float(str(value))
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("doc_3727", DOC_3727, "UH_SCHEMA_READY_CURRENT_UNIT_MAP_SYMBOLIC", "3727 status"),
        ("next_3727", NEXT_3727, "combine Fisher window, U_H, Theta_min", "3728 handoff"),
        ("runner_3727", RUNNER_3727, "BLOCKED_SYMBOLIC_UH", "U_H runner status"),
        ("runner_3726", RUNNER_3726, "BLOCKED_SYMBOLIC_WINDOW", "score-Gram runner status"),
        ("law_3724", LAW_3724, "Theta_min/iota_max", "mean branch gap law"),
        ("pack_3725", PACK_3725, "Xi_loc", "finite input pack"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append({
            **base(ts),
            "source_id": source_id,
            "path": str(path),
            "exists": exists,
            "needle": needle,
            "needle_found": needle in text,
            "role": role,
        })
    return rows


def xiloc_input_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        ("XI3728_0_theta_min", "Theta_min", "MISSING_THETA_MIN", "positive", "KL/Legendre scale lower bound", "False"),
        ("XI3728_1_iota_min", "iota_min", "MISSING_IOTA_MIN", "positive", "Fisher invertibility floor", "False"),
        ("XI3728_2_iota_max", "iota_max", "MISSING_IOTA_MAX", "positive", "Fisher ceiling controlling mean-branch lower gap", "False"),
        ("XI3728_3_u_min", "u_min", "MISSING_U_MIN", "positive", "U_H coercivity/smallest singular value", "False"),
        ("XI3728_4_DeltaM_mean", "DeltaM_mean", "MISSING_DELTAM_MEAN", "nonnegative", "operator mismatch norm", "False"),
        ("XI3728_5_R_loss", "R_loss", "MISSING_R_LOSS", "nonnegative", "domain/source/boundary correction loss", "False"),
        ("XI3728_6_R_U", "R_U", "MISSING_R_U", "nonnegative", "unit-map/projection remainder", "False"),
    ]
    return [
        {
            **base(ts),
            "input_id": input_id,
            "quantity": quantity,
            "value": value,
            "required_sign": required_sign,
            "meaning": meaning,
            "source_owned": source_owned,
            "claim_allowed": False,
        }
        for input_id, quantity, value, required_sign, meaning, source_owned in rows
    ]


def runner_rows(ts: str, inputs: list[dict[str, object]]) -> list[dict[str, object]]:
    values: dict[str, float] = {}
    missing: list[str] = []
    sign_failures: list[str] = []
    for row in inputs:
        quantity = str(row["quantity"])
        parsed = try_float(row["value"])
        if parsed is None or str(row["source_owned"]) != "True":
            missing.append(quantity)
            continue
        if row["required_sign"] == "positive" and parsed <= 0:
            sign_failures.append(quantity)
        if row["required_sign"] == "nonnegative" and parsed < 0:
            sign_failures.append(quantity)
        values[quantity] = parsed
    executable = not missing and not sign_failures
    xi_core = ""
    xi_loc = ""
    positive = False
    if executable:
        xi_core_value = values["Theta_min"] / values["iota_max"] - values["DeltaM_mean"] - values["R_loss"]
        xi_loc_value = values["u_min"] ** 2 * xi_core_value - values["R_U"]
        xi_core = xi_core_value
        xi_loc = xi_loc_value
        positive = xi_loc_value > 0 and values["iota_min"] > 0
    status = "EXECUTABLE_POSITIVE_NONCLAIM" if positive else "BLOCKED_MISSING_OR_NONPOSITIVE_XILOC"
    return [{
        **base(ts),
        "runner_id": "RUN3728_0_Xiloc",
        "formula": "Xi_loc=u_min^2*(Theta_min/iota_max-DeltaM_mean-R_loss)-R_U; require iota_min>0",
        "executable": executable,
        "missing_inputs": ";".join(missing),
        "sign_failures": ";".join(sign_failures),
        "xi_core": xi_core,
        "xi_loc": xi_loc,
        "positive_gap": positive,
        "status": status,
        "claim_allowed": False,
    }]


def refusal_rows(ts: str, runner: list[dict[str, object]]) -> list[dict[str, object]]:
    row = runner[0]
    missing = [item for item in str(row["missing_inputs"]).split(";") if item]
    sign_failures = [item for item in str(row["sign_failures"]).split(";") if item]
    rows: list[dict[str, object]] = []
    for quantity in missing:
        rows.append({
            **base(ts),
            "refusal_id": f"REF3728_missing_{quantity}",
            "quantity": quantity,
            "reason": "missing numeric source-owned input",
            "required_fix": f"provide source-owned numeric {quantity} row with units and parent path",
            "claim_allowed": False,
        })
    for quantity in sign_failures:
        rows.append({
            **base(ts),
            "refusal_id": f"REF3728_sign_{quantity}",
            "quantity": quantity,
            "reason": "input sign violates positivity/nonnegativity gate",
            "required_fix": f"repair or reject {quantity} input before Xi_loc scoring",
            "claim_allowed": False,
        })
    if not rows:
        rows.append({
            **base(ts),
            "refusal_id": "REF3728_none",
            "quantity": "none",
            "reason": "all inputs present; claim still disallowed until external arena gates consume Xi_loc",
            "required_fix": "route positive nonclaim Xi_loc into R10/PPN/clock/orbit response gates",
            "claim_allowed": False,
        })
    return rows


def theorem_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        ("THM3728_0_combined_law", "Xi_loc=u_min^2*(Theta_min/iota_max-DeltaM_mean-R_loss)-R_U", "combines 3724 mean-branch gap with 3726 Fisher window and 3727 U_H map", "DERIVED_RUNNER_FORM"),
        ("THM3728_1_invertibility_gate", "iota_min>0 is required even though iota_max controls the lower mean gap", "separates inverse existence from gap floor", "DERIVED_GATE"),
        ("THM3728_2_positive_gate", "Xi_loc>0 is necessary but not sufficient for local-GR/Newton/PPN claim", "local response and source coupling gates still consume the gap", "ANTI_OVERCLAIM"),
        ("THM3728_3_refusal_gate", "Any missing/non-source-owned factor blocks scoring", "prevents symbolic product from becoming a hidden pass", "ANTI_SMUGGLING_GUARD"),
    ]
    return [
        {
            **base(ts),
            "theorem_id": theorem_id,
            "formula_or_clause": formula_or_clause,
            "meaning": meaning,
            "status": status,
            "claim_allowed": False,
        }
        for theorem_id, formula_or_clause, meaning, status in rows
    ]


def decision_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        ("DEC3728_0_runner_ready", "COMBINED_XILOC_RUNNER_READY", "The full mean-branch local gap product now has one executable/refusal-safe runner contract."),
        ("DEC3728_1_current_blocked", "CURRENT_XILOC_BLOCKED_BY_MISSING_FACTORS", "Current inputs are placeholders, so Xi_loc remains unscoreable and no local screening claim is allowed."),
        ("DEC3728_2_next", "ADVANCE_TO_RESPONSE_ARENA_MAP", "Next target should map a future positive Xi_loc into R10/PPN/clock/orbit residual gates without assuming local-GR recovery."),
    ]
    return [
        {
            **base(ts),
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "claim_allowed": False,
        }
        for decision_id, decision, rationale in rows
    ]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    gates = [
        ("CG3728_0_theta", "BLOCKED", "Theta_min numeric/source-owned"),
        ("CG3728_1_fisher", "BLOCKED", "iota_min and iota_max numeric/source-owned from score-Gram runner"),
        ("CG3728_2_UH", "BLOCKED", "u_min and R_U numeric/source-owned from U_H runner"),
        ("CG3728_3_losses", "BLOCKED", "DeltaM_mean and R_loss numeric/source-owned or theorem-zero"),
        ("CG3728_4_Xi", "BLOCKED", "Xi_loc computed positive"),
        ("CG3728_5_arena", "BLOCKED", "positive Xi_loc mapped into R10/PPN/clock/orbit/EM residual arenas"),
        ("CG3728_6_claim", "BLOCKED", "local-GR/Newton screening claim allowed"),
    ]
    return [
        {
            **base(ts),
            "gate_id": gate_id,
            "gate_status": gate_status,
            "required_before_claim": required_before_claim,
            "claim_allowed": False,
        }
        for gate_id, gate_status, required_before_claim in gates
    ]


def status_rows(ts: str) -> list[dict[str, object]]:
    return [{
        **base(ts),
        "status_id": "STATUS3728_0",
        "status": "COMBINED_XILOC_RUNNER_READY_CURRENTLY_BLOCKED",
        "summary": "3728 combines the mean-branch local gap factors into one runner. Current placeholder inputs block Xi_loc scoring; no local screening claim is allowed.",
        "claim_allowed": False,
    }]


def next_target_rows(ts: str) -> list[dict[str, object]]:
    return [{
        **base(ts),
        "next_id": "NEXT3728_0",
        "target_doc": "3729-Y5-R2FR-Xiloc-to-local-arena-response-map.md",
        "target_script": "scripts/Y5_R2FR_3729_Xiloc_to_local_arena_response_map.py",
        "objective": "write the response-map contract that would consume a future positive Xi_loc into R10, PPN, clock, orbital, EM/Poynting, and Newton residual bounds without claiming those arenas pass",
        "success_gate": "arena response rows are explicit and remain blocked unless Xi_loc and source/product inputs are numeric/source-owned",
        "claim_allowed": False,
    }]


def validation_rows(ts: str, paths: dict[str, Path]) -> list[dict[str, object]]:
    sources = parse_csv(paths["source_register"])
    csv_paths = [path for key, path in paths.items() if key not in {"doc", "validation"}]
    generated = [path for key, path in paths.items() if key != "validation"]
    formal_files = list(FORMALIZATION.rglob("*3728*")) if FORMALIZATION.exists() else []
    formal_files = [path for path in formal_files if path.is_file()]
    runner = parse_csv(paths["runner"])[0]
    checks = [
        ("sources_exist", "sources exist", all(row["exists"] == "True" for row in sources)),
        ("needles_found", "source needles found", all(row["needle_found"] == "True" for row in sources)),
        ("outputs_exist", "outputs exist", all(path.exists() for path in generated)),
        ("csv_parse", "CSVs parse", all(len(parse_csv(path)) > 0 for path in csv_paths if path.exists())),
        ("input_schema", "all Xi inputs present", len(parse_csv(paths["inputs"])) == 7),
        ("runner_blocks_placeholders", "runner blocks placeholders", runner["status"] == "BLOCKED_MISSING_OR_NONPOSITIVE_XILOC" and runner["claim_allowed"] == "False"),
        ("refusal_rows", "refusal rows exist for missing inputs", len(parse_csv(paths["refusals"])) >= 7),
        ("theorems", "combined law and invertibility gate present", all(token in read_text(paths["theorems"]) for token in ["Xi_loc=u_min^2", "iota_min>0"])),
        ("claim_gates_blocked", "all claim gates blocked", all(row["gate_status"] == "BLOCKED" and row["claim_allowed"] == "False" for row in parse_csv(paths["claim_gates"]))),
        ("next_target_3729", "next target is 3729", "3729" in read_text(paths["next_target"])),
        ("doc_core_terms", "doc contains combined runner status", all(token in read_text(paths["doc"]) for token in ["COMBINED_XILOC_RUNNER_READY", "BLOCKED_MISSING_OR_NONPOSITIVE_XILOC", "Xi_loc"])),
        ("no_formalization_leak", "no 3728 files in formalization-workbench", len(formal_files) == 0),
    ]
    return [
        {
            **base(ts),
            "validation_id": validation_id,
            "description": description,
            "result": "PASS" if result else "FAIL",
            "details": "",
        }
        for validation_id, description, result in checks
    ]


def write_doc(paths: dict[str, Path], grouped: dict[str, list[dict[str, object]]]) -> None:
    runner = grouped["runner"][0]
    lines = [
        "# 3728 — Combined Xi_loc Runner and Refusal Gates",
        "",
        "## Status",
        "- `COMBINED_XILOC_RUNNER_READY_CURRENTLY_BLOCKED`",
        "- Combined formula: `Xi_loc=u_min^2*(Theta_min/iota_max-DeltaM_mean-R_loss)-R_U`, with `iota_min>0` required for invertibility.",
        f"- Current runner status: `{runner['status']}`.",
        "- This is a runner contract, not a local-GR/Newton/R10 claim.",
        "",
        "## Main Result",
        "- The mean-branch local gap is now a single product/gate object.",
        "- Missing inputs generate refusal rows instead of silently passing.",
        "- A future positive `Xi_loc` must still be consumed by arena response maps before any empirical statement.",
        "",
        "## Runner",
    ]
    for row in grouped["runner"]:
        lines.append(f"- `{row['runner_id']}` `{row['status']}`: executable={row['executable']} positive_gap={row['positive_gap']} missing=`{row['missing_inputs']}`")
    lines.extend(["", "## Refusals"])
    for row in grouped["refusals"]:
        lines.append(f"- `{row['refusal_id']}` `{row['quantity']}`: {row['reason']} | fix: {row['required_fix']}")
    lines.extend(["", "## Theorem Rows"])
    for row in grouped["theorems"]:
        lines.append(f"- `{row['theorem_id']}` `{row['status']}`: {row['formula_or_clause']} | {row['meaning']}")
    lines.extend(["", "## Decisions"])
    for row in grouped["decisions"]:
        lines.append(f"- `{row['decision_id']}` `{row['decision']}` | {row['rationale']}")
    lines.extend(["", "## Claim Gates"])
    for row in grouped["claim_gates"]:
        lines.append(f"- `{row['gate_id']}` `{row['gate_status']}` | {row['required_before_claim']}")
    lines.extend(["", "## Next Target"])
    lines.append("- `3729-Y5-R2FR-Xiloc-to-local-arena-response-map.md`")
    lines.append("- Objective: write the response-map contract from future `Xi_loc` into R10/PPN/clock/orbit/EM/Newton residual arenas.")
    paths["doc"].write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ts = stamp()
    paths = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3728_SOURCE_REGISTER.csv",
        "inputs": RESIDUALS / "P8_Y5_R2FR_3728_XILOC_INPUT_ROWS.csv",
        "runner": RESIDUALS / "P8_Y5_R2FR_3728_XILOC_RUNNER_STATUS.csv",
        "refusals": RESIDUALS / "P8_Y5_R2FR_3728_REFUSAL_ROWS.csv",
        "theorems": RESIDUALS / "P8_Y5_R2FR_3728_THEOREM_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3728_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3728_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3728_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3728_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3728_VALIDATION.csv",
        "doc": DOC,
    }
    inputs = xiloc_input_rows(ts)
    runner = runner_rows(ts, inputs)
    grouped = {
        "source_register": source_register(ts),
        "inputs": inputs,
        "runner": runner,
        "refusals": refusal_rows(ts, runner),
        "theorems": theorem_rows(ts),
        "decisions": decision_rows(ts),
        "claim_gates": claim_gate_rows(ts),
        "status": status_rows(ts),
        "next_target": next_target_rows(ts),
    }
    for key, rows in grouped.items():
        write_csv(paths[key], rows)
    write_doc(paths, grouped)
    write_csv(paths["validation"], validation_rows(ts, paths))
    failures = [row for row in parse_csv(paths["validation"]) if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3728 validation failed: {failures}")
    print("wrote 3728 checkpoint: combined Xi_loc runner ready and blocked by missing factors")


if __name__ == "__main__":
    main()

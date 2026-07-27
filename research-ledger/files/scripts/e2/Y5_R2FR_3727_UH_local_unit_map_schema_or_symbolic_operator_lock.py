from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3727"
BRANCH_ID = "MTS_R2FR_Y5_UH_LOCAL_UNIT_MAP_SCHEMA_OR_SYMBOLIC_OPERATOR_LOCK_3727"
DOC = ROOT / "3727-Y5-R2FR-UH-local-unit-map-schema-or-symbolic-operator-lock.md"

DOC_3726 = ROOT / "3726-Y5-R2FR-score-Gram-coercivity-runner-or-symbolic-window-lock.md"
NEXT_3726 = RESIDUALS / "P8_Y5_R2FR_3726_NEXT_TARGET.csv"
RUNNER_3726 = RESIDUALS / "P8_Y5_R2FR_3726_GRAM_RUNNER_STATUS.csv"
LAW_3724 = RESIDUALS / "P8_Y5_R2FR_3724_MEAN_GAP_LAW_ROWS.csv"
INPUT_3724 = RESIDUALS / "P8_Y5_R2FR_3724_REQUIRED_INPUT_ROWS.csv"
DOC_1297 = ROOT / "1297-Y5-R10-RAB-MTS-source-normalization-bridge-to-linearized-GR-operator.md"
DOC_3253 = ROOT / "3253-Y5-R2FR-parent-ordinary-sector-action-signature-or-C_Tw-component-current-norm-intake-under-AX1090.md"


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


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("doc_3726", DOC_3726, "SCORE_GRAM_SCHEMA_READY_CURRENT_WINDOW_SYMBOLIC", "3726 status"),
        ("next_3726", NEXT_3726, "U_H map", "3727 handoff"),
        ("runner_3726", RUNNER_3726, "BLOCKED_SYMBOLIC_WINDOW", "Fisher window runner status"),
        ("law_3724", LAW_3724, "u_min^2", "local unit gap law"),
        ("input_3724", INPUT_3724, "MISSING_UNIT_MAP_COERCIVITY", "U_H input row"),
        ("doc_1297", DOC_1297, "Kbar_HAS_UNITS_L^-2", "local operator/source-unit bridge ancestor"),
        ("doc_3253", DOC_3253, "same-frame current norm", "same-basis norm/eigenvalue pattern"),
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


def basis_schema_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        ("domain", "F0", "Fisher/response Hessian basis vector", "MISSING_DOMAIN_BASIS", "MISSING_UNITS", "False"),
        ("domain", "F1", "Fisher/response Hessian basis vector", "MISSING_DOMAIN_BASIS", "MISSING_UNITS", "False"),
        ("codomain", "L0", "local operator m^-2 basis vector", "MISSING_LOCAL_OPERATOR_BASIS", "MISSING_UNITS", "False"),
        ("codomain", "L1", "local operator m^-2 basis vector", "MISSING_LOCAL_OPERATOR_BASIS", "MISSING_UNITS", "False"),
    ]
    return [
        {
            **base(ts),
            "basis_side": basis_side,
            "basis_id": basis_id,
            "meaning": meaning,
            "source_path": source_path,
            "units": units,
            "parent_owned": parent_owned,
        }
        for basis_side, basis_id, meaning, source_path, units, parent_owned in rows
    ]


def map_template_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        ("L0", "F0", "MISSING_U00", "False"),
        ("L0", "F1", "MISSING_U01", "False"),
        ("L1", "F0", "MISSING_U10", "False"),
        ("L1", "F1", "MISSING_U11", "False"),
    ]
    return [
        {
            **base(ts),
            "local_basis_id": local_basis_id,
            "fisher_basis_id": fisher_basis_id,
            "map_value": map_value,
            "numeric_parent_owned": numeric_parent_owned,
        }
        for local_basis_id, fisher_basis_id, map_value, numeric_parent_owned in rows
    ]


def try_float(value: str) -> float | None:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def jacobi_eigenvalues_symmetric(matrix: list[list[float]], max_iterations: int = 100) -> list[float]:
    n = len(matrix)
    work = [row[:] for row in matrix]
    if n == 1:
        return [work[0][0]]
    for _ in range(max_iterations):
        p, q, max_off = 0, 1, 0.0
        for i in range(n):
            for j in range(i + 1, n):
                if abs(work[i][j]) > max_off:
                    max_off = abs(work[i][j])
                    p, q = i, j
        if max_off < 1e-12:
            break
        angle = math.pi / 4 if work[p][p] == work[q][q] else 0.5 * math.atan2(2 * work[p][q], work[q][q] - work[p][p])
        c, s = math.cos(angle), math.sin(angle)
        app = c * c * work[p][p] - 2 * s * c * work[p][q] + s * s * work[q][q]
        aqq = s * s * work[p][p] + 2 * s * c * work[p][q] + c * c * work[q][q]
        work[p][q] = work[q][p] = 0.0
        work[p][p], work[q][q] = app, aqq
        for r in range(n):
            if r in {p, q}:
                continue
            arp = c * work[r][p] - s * work[r][q]
            arq = s * work[r][p] + c * work[r][q]
            work[r][p] = work[p][r] = arp
            work[r][q] = work[q][r] = arq
    return sorted(work[i][i] for i in range(n))


def unit_map_runner_rows(ts: str, map_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    local_ids = sorted({str(row["local_basis_id"]) for row in map_rows})
    fisher_ids = sorted({str(row["fisher_basis_id"]) for row in map_rows})
    missing: list[str] = []
    values: dict[tuple[str, str], float] = {}
    for row in map_rows:
        parsed = try_float(str(row["map_value"]))
        key = (str(row["local_basis_id"]), str(row["fisher_basis_id"]))
        if parsed is None or str(row["numeric_parent_owned"]) != "True":
            missing.append(f"{key[0]}:{key[1]}")
        else:
            values[key] = parsed
    executable = not missing and bool(local_ids) and bool(fisher_ids)
    singular_values: list[float] = []
    if executable:
        matrix = [[values[(local_id, fisher_id)] for fisher_id in fisher_ids] for local_id in local_ids]
        gram = []
        for i, _ in enumerate(fisher_ids):
            row_values = []
            for j, _ in enumerate(fisher_ids):
                row_values.append(sum(matrix[k][i] * matrix[k][j] for k in range(len(local_ids))))
            gram.append(row_values)
        eigenvalues = jacobi_eigenvalues_symmetric(gram)
        if all(value >= -1e-10 for value in eigenvalues):
            singular_values = [math.sqrt(max(0.0, value)) for value in eigenvalues]
    positive = bool(singular_values) and min(singular_values) > 0
    status = "EXECUTABLE_UH_COERCIVITY_NONCLAIM" if positive else "BLOCKED_SYMBOLIC_UH"
    return [{
        **base(ts),
        "runner_id": "RUN3727_0_UH",
        "executable": executable,
        "local_dim": len(local_ids),
        "fisher_dim": len(fisher_ids),
        "missing_entries": ";".join(missing),
        "u_min": min(singular_values) if positive else "",
        "u_max": max(singular_values) if positive else "",
        "status": status,
        "claim_allowed": False,
    }]


def theorem_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        ("THM3727_0_map_definition", "U_H: H_Fisher -> H_local maps abstract Hessian directions into local m^-2/operator units.", "defines the missing local-unit object", "SCHEMA"),
        ("THM3727_1_coercivity", "||U_H v||_local >= u_min ||v||_Fisher for all active v.", "gives the u_min^2 multiplier in Xi_loc", "COERCIVITY_REQUIREMENT"),
        ("THM3727_2_remainder", "R_U bounds projection, basis, non-isometry, and omitted-local-channel errors.", "keeps unit conversion losses explicit", "REMAINDER_REQUIREMENT"),
        ("THM3727_3_matrix_runner", "For finite U matrix, u_min=sqrt(lambda_min(U^T U)).", "makes U_H a singular-value problem", "DERIVED_SCHEMA"),
        ("THM3727_4_refusal", "If U entries, bases, units, or coercivity are missing, Xi_loc cannot be scored.", "prevents abstract gap from becoming local-GR claim", "ANTI_SMUGGLING_GUARD"),
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
        ("DEC3727_0_schema_ready", "UH_SCHEMA_READY", "U_H is now an explicit finite matrix/singular-value schema rather than a hidden unit conversion."),
        ("DEC3727_1_current_blocked", "CURRENT_UH_LOCKED_SYMBOLIC", "Template map rows are placeholders, so u_min/R_U remain missing and Xi_loc cannot be scored."),
        ("DEC3727_2_next", "ADVANCE_TO_COMBINED_XILOC_RUNNER", "With Fisher window and U_H schemas installed, next target can combine both and refuse scoring until all inputs are real."),
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
        ("CG3727_0_domain_basis", "BLOCKED", "Fisher/response Hessian basis parent-owned"),
        ("CG3727_1_local_basis", "BLOCKED", "local operator m^-2 basis parent-owned"),
        ("CG3727_2_units", "BLOCKED", "domain and codomain units matched"),
        ("CG3727_3_matrix", "BLOCKED", "U_H matrix entries numeric and parent-owned"),
        ("CG3727_4_coercivity", "BLOCKED", "u_min>0 and R_U finite"),
        ("CG3727_5_Xi", "BLOCKED", "Xi_loc score can use U_H"),
        ("CG3727_6_claim", "BLOCKED", "local operator/local-GR claim allowed"),
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
        "status_id": "STATUS3727_0",
        "status": "UH_SCHEMA_READY_CURRENT_UNIT_MAP_SYMBOLIC",
        "summary": "3727 installs U_H as an explicit finite matrix/singular-value schema with u_min=sqrt(lambda_min(U^T U)); current placeholder rows keep U_H and Xi_loc symbolic.",
        "claim_allowed": False,
    }]


def next_target_rows(ts: str) -> list[dict[str, object]]:
    return [{
        **base(ts),
        "next_id": "NEXT3727_0",
        "target_doc": "3728-Y5-R2FR-combined-Xiloc-runner-and-refusal-gates.md",
        "target_script": "scripts/Y5_R2FR_3728_combined_Xiloc_runner_and_refusal_gates.py",
        "objective": "combine Fisher window, U_H, Theta_min, DeltaM_mean, R_loss, and R_U into one Xi_loc runner that refuses local screening claims until every factor is source-owned",
        "success_gate": "Xi_loc runner produces either a positive nonclaim value from complete inputs or an explicit blocked ledger from missing factors",
        "claim_allowed": False,
    }]


def validation_rows(ts: str, paths: dict[str, Path]) -> list[dict[str, object]]:
    sources = parse_csv(paths["source_register"])
    csv_paths = [path for key, path in paths.items() if key not in {"doc", "validation"}]
    generated = [path for key, path in paths.items() if key != "validation"]
    formal_files = list(FORMALIZATION.rglob("*3727*")) if FORMALIZATION.exists() else []
    formal_files = [path for path in formal_files if path.is_file()]
    runner = parse_csv(paths["runner"])[0]
    checks = [
        ("sources_exist", "sources exist", all(row["exists"] == "True" for row in sources)),
        ("needles_found", "source needles found", all(row["needle_found"] == "True" for row in sources)),
        ("outputs_exist", "outputs exist", all(path.exists() for path in generated)),
        ("csv_parse", "CSVs parse", all(len(parse_csv(path)) > 0 for path in csv_paths if path.exists())),
        ("basis_rows", "basis schema rows exist", len(parse_csv(paths["basis"])) >= 4),
        ("runner_refuses_placeholders", "U_H runner refuses placeholders", runner["status"] == "BLOCKED_SYMBOLIC_UH" and runner["claim_allowed"] == "False"),
        ("theorems", "theorem rows include singular-value formula", "sqrt(lambda_min(U^T U))" in read_text(paths["theorems"])),
        ("claim_gates_blocked", "all claim gates blocked", all(row["gate_status"] == "BLOCKED" and row["claim_allowed"] == "False" for row in parse_csv(paths["claim_gates"]))),
        ("next_target_3728", "next target is 3728", "3728" in read_text(paths["next_target"])),
        ("doc_core_terms", "doc contains U_H symbolic lock", all(token in read_text(paths["doc"]) for token in ["U_H", "BLOCKED_SYMBOLIC_UH", "u_min"])),
        ("no_formalization_leak", "no 3727 files in formalization-workbench", len(formal_files) == 0),
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
        "# 3727 — U_H Local Unit Map Schema or Symbolic Operator Lock",
        "",
        "## Status",
        "- `UH_SCHEMA_READY_CURRENT_UNIT_MAP_SYMBOLIC`",
        "- `U_H` is now an explicit finite matrix/singular-value schema from Fisher/response Hessian units to local `m^-2` operator units.",
        f"- Current runner status: `{runner['status']}` because template map rows are placeholders.",
        "- `Xi_loc` remains unscoreable until `u_min` and `R_U` are source-owned.",
        "",
        "## Main Result",
        "- `U_H` must map the abstract mean-branch Hessian into the observed local operator basis.",
        "- Finite matrix law: `u_min=sqrt(lambda_min(U_H^T U_H))`.",
        "- The corrected local gap uses `u_min^2` and subtracts a unit-map remainder `R_U`.",
        "- Without `U_H`, a positive Fisher/response gap is not yet a local GR/Newton/R10 gap.",
        "",
        "## Theorem Rows",
    ]
    for row in grouped["theorems"]:
        lines.append(f"- `{row['theorem_id']}` `{row['status']}`: {row['formula_or_clause']} | {row['meaning']}")
    lines.extend(["", "## Runner Status"])
    for row in grouped["runner"]:
        lines.append(f"- `{row['runner_id']}` `{row['status']}`: executable={row['executable']} missing=`{row['missing_entries']}` u_min=`{row['u_min']}`")
    lines.extend(["", "## Decisions"])
    for row in grouped["decisions"]:
        lines.append(f"- `{row['decision_id']}` `{row['decision']}` | {row['rationale']}")
    lines.extend(["", "## Claim Gates"])
    for row in grouped["claim_gates"]:
        lines.append(f"- `{row['gate_id']}` `{row['gate_status']}` | {row['required_before_claim']}")
    lines.extend(["", "## Next Target"])
    lines.append("- `3728-Y5-R2FR-combined-Xiloc-runner-and-refusal-gates.md`")
    lines.append("- Objective: combine Fisher window, `U_H`, scale, mismatch, and losses into one refusal-safe `Xi_loc` runner.")
    paths["doc"].write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ts = stamp()
    paths = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3727_SOURCE_REGISTER.csv",
        "basis": RESIDUALS / "P8_Y5_R2FR_3727_UH_BASIS_SCHEMA.csv",
        "map": RESIDUALS / "P8_Y5_R2FR_3727_UH_MAP_TEMPLATE.csv",
        "runner": RESIDUALS / "P8_Y5_R2FR_3727_UH_RUNNER_STATUS.csv",
        "theorems": RESIDUALS / "P8_Y5_R2FR_3727_THEOREM_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3727_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3727_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3727_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3727_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3727_VALIDATION.csv",
        "doc": DOC,
    }
    basis = basis_schema_rows(ts)
    map_rows = map_template_rows(ts)
    runner = unit_map_runner_rows(ts, map_rows)
    grouped = {
        "source_register": source_register(ts),
        "basis": basis,
        "map": map_rows,
        "runner": runner,
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
        raise SystemExit(f"3727 validation failed: {failures}")
    print("wrote 3727 checkpoint: U_H schema ready; local unit map locked symbolic")


if __name__ == "__main__":
    main()

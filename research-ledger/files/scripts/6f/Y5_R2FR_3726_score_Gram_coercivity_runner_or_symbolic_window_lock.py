from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3726"
BRANCH_ID = "MTS_R2FR_Y5_SCORE_GRAM_COHERCIVITY_RUNNER_OR_SYMBOLIC_WINDOW_LOCK_3726"
DOC = ROOT / "3726-Y5-R2FR-score-Gram-coercivity-runner-or-symbolic-window-lock.md"

DOC_3725 = ROOT / "3725-Y5-R2FR-Fisher-window-UH-source-hunt-or-finite-bound-pack.md"
NEXT_3725 = RESIDUALS / "P8_Y5_R2FR_3725_NEXT_TARGET.csv"
GRAM_3725 = RESIDUALS / "P8_Y5_R2FR_3725_SCORE_GRAM_ROUTE_ROWS.csv"
PACK_3725 = RESIDUALS / "P8_Y5_R2FR_3725_FINITE_BOUND_PACK_ROWS.csv"
LAW_3724 = RESIDUALS / "P8_Y5_R2FR_3724_MEAN_GAP_LAW_ROWS.csv"
FISHER_3708 = RESIDUALS / "P8_Y5_R2FR_3708_FISHER_GAP_DERIVATION_ROWS.csv"


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
        ("doc_3725", DOC_3725, "SOURCE_HUNT_NO_CLAIM_FINITE_SCORE_GRAM_ROUTE_READY", "3725 status"),
        ("next_3725", NEXT_3725, "score basis and Gram matrix", "3726 handoff"),
        ("gram_3725", GRAM_3725, "I_AB=<Y_A,Y_B>_0", "score-Gram route"),
        ("pack_3725", PACK_3725, "lambda_max(G_Y)", "finite iota window pack"),
        ("law_3724", LAW_3724, "Theta_min/iota_max", "mean branch corrected gap"),
        ("fisher_3708", FISHER_3708, "p_z(xi|X_B,q)=p_0", "original Fisher bath construction"),
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


def score_basis_template_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        ("Y0", "placeholder_score_0", "MISSING_SCORE_FUNCTION", "MISSING_BATH_MEASURE", "MISSING_UNITS", "active_candidate", "False"),
        ("Y1", "placeholder_score_1", "MISSING_SCORE_FUNCTION", "MISSING_BATH_MEASURE", "MISSING_UNITS", "active_candidate", "False"),
    ]
    return [
        {
            **base(ts),
            "score_id": score_id,
            "score_name": score_name,
            "score_definition": score_definition,
            "inner_product_source": inner_product_source,
            "units": units,
            "active_status": active_status,
            "parent_owned": parent_owned,
        }
        for score_id, score_name, score_definition, inner_product_source, units, active_status, parent_owned in rows
    ]


def gram_matrix_template_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        ("Y0", "Y0", "MISSING_G00", "score_basis_template", "False"),
        ("Y0", "Y1", "MISSING_G01", "score_basis_template", "False"),
        ("Y1", "Y0", "MISSING_G10", "score_basis_template", "False"),
        ("Y1", "Y1", "MISSING_G11", "score_basis_template", "False"),
    ]
    return [
        {
            **base(ts),
            "row_score_id": row_score_id,
            "col_score_id": col_score_id,
            "gram_value": gram_value,
            "source_path": source_path,
            "numeric_parent_owned": numeric_parent_owned,
        }
        for row_score_id, col_score_id, gram_value, source_path, numeric_parent_owned in rows
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
    for _ in range(max_iterations):
        p, q = 0, 1 if n > 1 else 0
        max_off = 0.0
        for i in range(n):
            for j in range(i + 1, n):
                if abs(work[i][j]) > max_off:
                    max_off = abs(work[i][j])
                    p, q = i, j
        if max_off < 1e-12:
            break
        if work[p][p] == work[q][q]:
            angle = math.pi / 4
        else:
            angle = 0.5 * math.atan2(2 * work[p][q], work[q][q] - work[p][p])
        c = math.cos(angle)
        s = math.sin(angle)
        app = c * c * work[p][p] - 2 * s * c * work[p][q] + s * s * work[q][q]
        aqq = s * s * work[p][p] + 2 * s * c * work[p][q] + c * c * work[q][q]
        work[p][q] = 0.0
        work[q][p] = 0.0
        work[p][p] = app
        work[q][q] = aqq
        for r in range(n):
            if r in {p, q}:
                continue
            arp = c * work[r][p] - s * work[r][q]
            arq = s * work[r][p] + c * work[r][q]
            work[r][p] = arp
            work[p][r] = arp
            work[r][q] = arq
            work[q][r] = arq
    return sorted(work[i][i] for i in range(n))


def runner_status_rows(ts: str, matrix_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    score_ids = sorted({str(row["row_score_id"]) for row in matrix_rows} | {str(row["col_score_id"]) for row in matrix_rows})
    numeric_values: dict[tuple[str, str], float] = {}
    missing: list[str] = []
    for row in matrix_rows:
        row_id = str(row["row_score_id"])
        col_id = str(row["col_score_id"])
        parsed = try_float(str(row["gram_value"]))
        if parsed is None or str(row["numeric_parent_owned"]) != "True":
            missing.append(f"{row_id}:{col_id}")
        else:
            numeric_values[(row_id, col_id)] = parsed
    executable = not missing and bool(score_ids)
    symmetry_ok = False
    eigenvalues: list[float] = []
    if executable:
        matrix = []
        symmetry_ok = True
        for row_id in score_ids:
            row_values = []
            for col_id in score_ids:
                value = numeric_values[(row_id, col_id)]
                transpose = numeric_values[(col_id, row_id)]
                if abs(value - transpose) > 1e-10:
                    symmetry_ok = False
                row_values.append(0.5 * (value + transpose))
            matrix.append(row_values)
        if symmetry_ok:
            eigenvalues = jacobi_eigenvalues_symmetric(matrix)
    positive = bool(eigenvalues) and min(eigenvalues) > 0
    iota_min = min(eigenvalues) if positive else ""
    iota_max = max(eigenvalues) if positive else ""
    trace_bound = sum(eigenvalues) if eigenvalues else ""
    status = "EXECUTABLE_POSITIVE_NONCLAIM" if positive else "BLOCKED_SYMBOLIC_WINDOW"
    return [
        {
            **base(ts),
            "runner_id": "RUN3726_0_score_gram",
            "executable": executable,
            "symmetry_ok": symmetry_ok,
            "positive_definite": positive,
            "score_count": len(score_ids),
            "missing_entries": ";".join(missing),
            "iota_min": iota_min,
            "iota_max": iota_max,
            "trace_bound": trace_bound,
            "status": status,
            "claim_allowed": False,
        }
    ]


def theorem_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        ("THM3726_0_finite_gram", "Given finite active score basis Y_A and bath inner product <.,.>_0, define G_Y,AB=<Y_A,Y_B>_0.", "finite Fisher matrix is a Gram matrix", "DERIVED_SCHEMA"),
        ("THM3726_1_eigen_window", "If G_Y is symmetric positive definite, iota_min=lambda_min(G_Y), iota_max=lambda_max(G_Y).", "gives invertibility and mean-branch Fisher ceiling", "DERIVED_SCHEMA"),
        ("THM3726_2_trace_ceiling", "iota_max <= Tr(G_Y)=sum_A ||Y_A||_0^2.", "safe ceiling if exact eigenvalue runner is unavailable", "DERIVED_BOUND"),
        ("THM3726_3_mean_gap_feed", "Xi_loc <=/>= uses iota_max in denominator: Xi_loc >= u_min^2*(Theta_min/iota_max-DeltaM-R_loss)-R_U.", "Gram window feeds 3724 gap law", "DERIVED_LINK"),
        ("THM3726_4_refusal", "If any score, inner product, matrix value, symmetry, or positivity clause is missing, Fisher window stays symbolic.", "no local screening promotion from placeholders", "ANTI_SMUGGLING_GUARD"),
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
        ("DEC3726_0_runner_schema_ready", "SCORE_GRAM_RUNNER_SCHEMA_READY", "Future real score matrices can now produce iota_min/iota_max without changing the theory contract."),
        ("DEC3726_1_current_blocked", "CURRENT_WINDOW_LOCKED_SYMBOLIC", "The generated template contains placeholders, so no mean-branch gap value or screening claim is allowed."),
        ("DEC3726_2_next", "ADVANCE_TO_UH_UNIT_MAP_SCHEMA", "Once the Fisher window has a runner shell, the next orthogonal missing piece is U_H/local operator unit conversion."),
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
        ("CG3726_0_score_basis", "BLOCKED", "all active score functions Y_A parent-owned"),
        ("CG3726_1_inner_product", "BLOCKED", "bath measure/inner product <.,.>_0 source-owned"),
        ("CG3726_2_matrix", "BLOCKED", "G_Y matrix entries numeric and parent-owned"),
        ("CG3726_3_spd", "BLOCKED", "G_Y symmetric positive definite on active subspace"),
        ("CG3726_4_window", "BLOCKED", "iota_min/iota_max computed or theorem-bounded"),
        ("CG3726_5_local_gap", "BLOCKED", "Fisher window inserted into Xi_loc with U_H and losses"),
        ("CG3726_6_claim", "BLOCKED", "local screening claim allowed"),
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
        "status_id": "STATUS3726_0",
        "status": "SCORE_GRAM_SCHEMA_READY_CURRENT_WINDOW_SYMBOLIC",
        "summary": "3726 installs an executable finite score-Gram schema and eigenvalue runner logic, but the current placeholder score/matrix rows keep iota_min/iota_max symbolic and claims blocked.",
        "claim_allowed": False,
    }]


def next_target_rows(ts: str) -> list[dict[str, object]]:
    return [{
        **base(ts),
        "next_id": "NEXT3726_0",
        "target_doc": "3727-Y5-R2FR-UH-local-unit-map-schema-or-symbolic-operator-lock.md",
        "target_script": "scripts/Y5_R2FR_3727_UH_local_unit_map_schema_or_symbolic_operator_lock.py",
        "objective": "define the U_H map from Fisher/response Hessian units into local m^-2/operator units, including coercivity u_min and remainder R_U, or lock U_H as symbolic nonclaim",
        "success_gate": "U_H schema can accept future source rows and refuses local Xi_loc scoring until u_min/R_U are source-owned",
        "claim_allowed": False,
    }]


def validation_rows(ts: str, paths: dict[str, Path]) -> list[dict[str, object]]:
    sources = parse_csv(paths["source_register"])
    csv_paths = [path for key, path in paths.items() if key not in {"doc", "validation"}]
    generated = [path for key, path in paths.items() if key != "validation"]
    formal_files = list(FORMALIZATION.rglob("*3726*")) if FORMALIZATION.exists() else []
    formal_files = [path for path in formal_files if path.is_file()]
    runner = parse_csv(paths["runner"])[0]
    checks = [
        ("sources_exist", "sources exist", all(row["exists"] == "True" for row in sources)),
        ("needles_found", "source needles found", all(row["needle_found"] == "True" for row in sources)),
        ("outputs_exist", "outputs exist", all(path.exists() for path in generated)),
        ("csv_parse", "CSVs parse", all(len(parse_csv(path)) > 0 for path in csv_paths if path.exists())),
        ("schema_rows", "score basis and Gram templates exist", len(parse_csv(paths["basis"])) >= 2 and len(parse_csv(paths["matrix"])) >= 4),
        ("runner_refuses_placeholders", "runner refuses placeholder matrix", runner["status"] == "BLOCKED_SYMBOLIC_WINDOW" and runner["claim_allowed"] == "False"),
        ("theorem_rows", "theorem rows include eigen window and trace ceiling", all(token in read_text(paths["theorems"]) for token in ["iota_min=lambda_min", "iota_max <= Tr"])),
        ("claim_gates_blocked", "all claim gates blocked", all(row["gate_status"] == "BLOCKED" and row["claim_allowed"] == "False" for row in parse_csv(paths["claim_gates"]))),
        ("next_target_3727", "next target is 3727", "3727" in read_text(paths["next_target"])),
        ("doc_core_terms", "doc contains schema and symbolic lock", all(token in read_text(paths["doc"]) for token in ["score-Gram", "BLOCKED_SYMBOLIC_WINDOW", "iota_min/iota_max"])),
        ("no_formalization_leak", "no 3726 files in formalization-workbench", len(formal_files) == 0),
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
        "# 3726 — Score-Gram Coercivity Runner or Symbolic Window Lock",
        "",
        "## Status",
        "- `SCORE_GRAM_SCHEMA_READY_CURRENT_WINDOW_SYMBOLIC`",
        "- This checkpoint installs a finite score-Gram schema for `G_Y=<Y_A,Y_B>_0` and runner logic for `iota_min/iota_max`.",
        f"- Current runner status: `{runner['status']}` because placeholder score/matrix rows are not parent-owned.",
        "- No local screening claim is allowed from placeholder Gram rows.",
        "",
        "## Main Result",
        "- If a real finite active score basis is supplied, the runner computes the Fisher eigenvalue window.",
        "- `iota_min=lambda_min(G_Y)` gives invertibility for the mean branch.",
        "- `iota_max=lambda_max(G_Y)` supplies the Fisher ceiling required by the `Theta_min/iota_max` gap law.",
        "- If matrix rows are missing, nonsymmetric, or non-positive, the window remains symbolic.",
        "",
        "## Theorem Rows",
    ]
    for row in grouped["theorems"]:
        lines.append(f"- `{row['theorem_id']}` `{row['status']}`: {row['formula_or_clause']} | {row['meaning']}")
    lines.extend(["", "## Runner Status"])
    for row in grouped["runner"]:
        lines.append(f"- `{row['runner_id']}` `{row['status']}`: executable={row['executable']} symmetry_ok={row['symmetry_ok']} positive_definite={row['positive_definite']} missing=`{row['missing_entries']}`")
    lines.extend(["", "## Decisions"])
    for row in grouped["decisions"]:
        lines.append(f"- `{row['decision_id']}` `{row['decision']}` | {row['rationale']}")
    lines.extend(["", "## Claim Gates"])
    for row in grouped["claim_gates"]:
        lines.append(f"- `{row['gate_id']}` `{row['gate_status']}` | {row['required_before_claim']}")
    lines.extend(["", "## Output Files"])
    for key in ["basis", "matrix", "runner", "validation"]:
        lines.append(f"- `{paths[key]}`")
    lines.extend(["", "## Next Target"])
    lines.append("- `3727-Y5-R2FR-UH-local-unit-map-schema-or-symbolic-operator-lock.md`")
    lines.append("- Objective: define the local unit/operator map `U_H`, coercivity `u_min`, and unit remainder `R_U`.")
    paths["doc"].write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ts = stamp()
    paths = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3726_SOURCE_REGISTER.csv",
        "basis": RESIDUALS / "P8_Y5_R2FR_3726_SCORE_BASIS_TEMPLATE.csv",
        "matrix": RESIDUALS / "P8_Y5_R2FR_3726_GRAM_MATRIX_TEMPLATE.csv",
        "runner": RESIDUALS / "P8_Y5_R2FR_3726_GRAM_RUNNER_STATUS.csv",
        "theorems": RESIDUALS / "P8_Y5_R2FR_3726_THEOREM_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3726_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3726_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3726_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3726_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3726_VALIDATION.csv",
        "doc": DOC,
    }
    basis = score_basis_template_rows(ts)
    matrix = gram_matrix_template_rows(ts)
    runner = runner_status_rows(ts, matrix)
    grouped = {
        "source_register": source_register(ts),
        "basis": basis,
        "matrix": matrix,
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
        raise SystemExit(f"3726 validation failed: {failures}")
    print("wrote 3726 checkpoint: score-Gram schema ready; Fisher window locked symbolic")


if __name__ == "__main__":
    main()

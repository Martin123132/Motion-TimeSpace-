from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3735"
BRANCH_ID = "MTS_R2FR_Y5_RESPONSE_MATRIX_FIRST_PASS_NEWTON_PPN_EM_3735"
DOC = ROOT / "3735-Y5-R2FR-response-matrix-first-pass-Newton-PPN-EM.md"

DOC_3734 = ROOT / "3734-Y5-R2FR-HX-chi-bound-interface-to-Newton-PPN-EM.md"
NEXT_3734 = RESIDUALS / "P8_Y5_R2FR_3734_NEXT_TARGET.csv"
VALIDATION_3734 = RESIDUALS / "P8_Y5_BRR545_3734_VALIDATION.csv"
BETA_3734 = RESIDUALS / "P8_Y5_R2FR_3734_BETA_LINK_ROWS.csv"
ENTRIES_3732 = RESIDUALS / "P8_Y5_R2FR_3732_RESPONSE_ENTRY_ROWS.csv"
BASIS_3732 = RESIDUALS / "P8_Y5_R2FR_3732_ARENA_BASIS_ROWS.csv"


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
    return parsed if math.isfinite(parsed) else None


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("doc_3734", DOC_3734, "HX_CHI_BOUND_INTERFACE_READY_CURRENTLY_BLOCKED", "3734 sigma/beta interface"),
        ("next_3734", NEXT_3734, "3735-Y5-R2FR-response-matrix-first-pass-Newton-PPN-EM.md", "3734 handoff"),
        ("validation_3734", VALIDATION_3734, "next_target_3735", "3734 validation"),
        ("beta_3734", BETA_3734, "beta_NP", "3734 beta links"),
        ("entries_3732", ENTRIES_3732, "B3732_NP_accel_phi", "3732 symbolic response entries"),
        ("basis_3732", BASIS_3732, "Newton_PPN_bridge", "3732 basis rows"),
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


def basis_summary_rows(ts: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    basis = parse_csv(BASIS_3732)
    for bridge in ["Newton_PPN_bridge", "EM_Poynting_bridge"]:
        domain = [row["symbol"] for row in basis if row["bridge"] == bridge and row["basis_type"] == "domain"]
        observable = [row["symbol"] for row in basis if row["bridge"] == bridge and row["basis_type"] == "observable"]
        rows.append({
            **base(ts),
            "bridge": bridge,
            "domain_dimension": len(domain),
            "observable_dimension": len(observable),
            "domain_basis": ";".join(domain),
            "observable_basis": ";".join(observable),
            "dimension_status": "FINITE_BASIS_READY",
            "claim_allowed": False,
        })
    return rows


def b_matrix_rows(ts: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in parse_csv(ENTRIES_3732):
        bridge = row["bridge"]
        if bridge not in {"Newton_PPN_bridge", "EM_Poynting_bridge"}:
            continue
        rows.append({
            **base(ts),
            "entry_id": f"BME3735_{row['entry_id']}",
            "bridge": bridge,
            "matrix": "B_NP" if bridge == "Newton_PPN_bridge" else "B_EM",
            "observable_row": row["observable_row"],
            "domain_col": row["domain_col"],
            "symbolic_entry": row["symbolic_entry"],
            "value": "MISSING_NUMERIC_OR_THEOREM_ENTRY",
            "units": "operator_norm_units",
            "source_path": str(ENTRIES_3732),
            "source_owned": False,
            "claim_allowed": False,
        })
    return rows


def metric_weight_rows(ts: str) -> list[dict[str, object]]:
    basis = parse_csv(BASIS_3732)
    rows: list[dict[str, object]] = []
    for bridge in ["Newton_PPN_bridge", "EM_Poynting_bridge"]:
        prefix = "NP" if bridge == "Newton_PPN_bridge" else "EM"
        domain_symbols = [row["symbol"] for row in basis if row["bridge"] == bridge and row["basis_type"] == "domain"]
        observable_symbols = [row["symbol"] for row in basis if row["bridge"] == bridge and row["basis_type"] == "observable"]
        for symbol in domain_symbols:
            rows.append({
                **base(ts),
                "entry_id": f"GM3735_{prefix}_{symbol}",
                "bridge": bridge,
                "matrix": f"G_{prefix}",
                "row_symbol": symbol,
                "col_symbol": symbol,
                "value": "MISSING_POSITIVE_GRAM_ENTRY",
                "required_property": "positive_diagonal_or_parent_positive_definite",
                "source_path": "MISSING_SOURCE_OR_THEOREM_PATH",
                "source_owned": False,
                "claim_allowed": False,
            })
        for symbol in observable_symbols:
            rows.append({
                **base(ts),
                "entry_id": f"WM3735_{prefix}_{symbol}",
                "bridge": bridge,
                "matrix": f"W_{prefix}",
                "row_symbol": symbol,
                "col_symbol": symbol,
                "value": "MISSING_NONNEGATIVE_WEIGHT_ENTRY",
                "required_property": "nonnegative_diagonal_or_parent_positive_semidefinite",
                "source_path": "MISSING_SOURCE_OR_THEOREM_PATH",
                "source_owned": False,
                "claim_allowed": False,
            })
    return rows


def norm_contract_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "NORM3735_NP",
            "Newton_PPN_bridge",
            "beta_NP^2=lambda_max(G_NP^{-1/2} B_NP^T W_NP B_NP G_NP^{-1/2})",
            "B_NP from acceleration/Poisson/gamma/beta/preferred-frame response entries; G_NP domain Gram; W_NP observable weight/covariance inverse",
        ),
        (
            "NORM3735_EM",
            "EM_Poynting_bridge",
            "beta_EM^2=lambda_max(G_EM^{-1/2} B_EM^T W_EM B_EM G_EM^{-1/2})",
            "B_EM from Poynting/stress/wave/polarization/charge response entries; G_EM domain Gram; W_EM observable weight/covariance inverse",
        ),
    ]
    return [
        {
            **base(ts),
            "norm_id": norm_id,
            "bridge": bridge,
            "beta_formula": formula,
            "interpretation": interpretation,
            "current_status": "NORM_CONTRACT_READY_VALUES_MISSING",
            "ready_for_3729": False,
            "claim_allowed": False,
        }
        for norm_id, bridge, formula, interpretation in rows
    ]


def runner_rows(ts: str, b_entries: list[dict[str, object]], gw_entries: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for bridge in ["Newton_PPN_bridge", "EM_Poynting_bridge"]:
        bridge_b = [row for row in b_entries if row["bridge"] == bridge]
        bridge_gw = [row for row in gw_entries if row["bridge"] == bridge]
        missing = []
        sign_failures = []
        for row in bridge_b + bridge_gw:
            parsed = try_float(row["value"])
            if parsed is None or str(row["source_owned"]) != "True":
                missing.append(str(row["entry_id"]))
                continue
            if str(row.get("matrix", "")).startswith("G_") and parsed <= 0:
                sign_failures.append(str(row["entry_id"]))
            if str(row.get("matrix", "")).startswith("W_") and parsed < 0:
                sign_failures.append(str(row["entry_id"]))
        executable = not missing and not sign_failures
        beta_value: float | str = ""
        status = "BLOCKED_MISSING_RESPONSE_MATRIX_ENTRIES"
        if executable:
            status = "EXECUTABLE_BETA_NONCLAIM"
            beta_value = "COMPUTE_EIGENVALUE_AFTER_MATRIX_ASSEMBLY"
        rows.append({
            **base(ts),
            "runner_id": f"RUN3735_{bridge}",
            "bridge": bridge,
            "executable": executable,
            "missing_entries": ";".join(missing),
            "sign_failures": ";".join(sign_failures),
            "beta_value": beta_value,
            "status": status,
            "ready_for_3729": False,
            "claim_allowed": False,
        })
    return rows


def positivity_gate_rows(ts: str) -> list[dict[str, object]]:
    gates = [
        ("PG3735_0_GNP", "Newton_PPN_bridge", "G_NP positive definite", "all domain Gram eigenvalues positive or diagonal entries positive in diagonal approximation"),
        ("PG3735_1_WNP", "Newton_PPN_bridge", "W_NP positive semidefinite", "observable weights/covariance inverse nonnegative with finite bounds"),
        ("PG3735_2_BNP", "Newton_PPN_bridge", "B_NP finite", "all response entries finite and source-owned/theorem-owned"),
        ("PG3735_3_GEM", "EM_Poynting_bridge", "G_EM positive definite", "all domain Gram eigenvalues positive or diagonal entries positive in diagonal approximation"),
        ("PG3735_4_WEM", "EM_Poynting_bridge", "W_EM positive semidefinite", "observable weights/covariance inverse nonnegative with finite bounds"),
        ("PG3735_5_BEM", "EM_Poynting_bridge", "B_EM finite", "all response entries finite and source-owned/theorem-owned"),
    ]
    return [
        {
            **base(ts),
            "gate_id": gate_id,
            "bridge": bridge,
            "gate": gate,
            "required_before_beta": required,
            "gate_status": "BLOCKED_PLACEHOLDER_VALUES",
            "claim_allowed": False,
        }
        for gate_id, bridge, gate, required in gates
    ]


def fill_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        ("BFILL3735_NP", "Newton_PPN_bridge", "beta_A=beta_NP from NORM3735_NP once B_NP,G_NP,W_NP pass positivity and source-owned gates", "FILL3734_NP"),
        ("BFILL3735_EM", "EM_Poynting_bridge", "beta_A=beta_EM from NORM3735_EM once B_EM,G_EM,W_EM pass positivity and source-owned gates", "FILL3734_EM"),
    ]
    return [
        {
            **base(ts),
            "fill_id": fill_id,
            "bridge": bridge,
            "beta_fill_contract": contract,
            "target_fill_row": target,
            "ready_for_3729": False,
            "claim_allowed": False,
        }
        for fill_id, bridge, contract, target in rows
    ]


def refusal_rows(ts: str, runner: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in runner:
        missing_count = len([item for item in str(row["missing_entries"]).split(";") if item])
        rows.append({
            **base(ts),
            "refusal_id": f"REF3735_{row['bridge']}",
            "bridge": row["bridge"],
            "reason": "missing numeric/source-owned B/G/W response matrix entries",
            "missing_count": missing_count,
            "required_fix": "provide source-owned numeric entries or theorem-zero/finite operator bounds for every B, G, and W row",
            "claim_allowed": False,
        })
    return rows


def theorem_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "THM3735_0_operator_norm",
            "For finite domain Gram G>0 and observable weight W>=0, beta^2=lambda_max(G^{-1/2}B^T W B G^{-1/2}).",
            "This is the computable bridge from response entries to the beta_A required by 3729.",
            "DERIVED_OPERATOR_NORM",
        ),
        (
            "THM3735_1_NP_response_scope",
            "B_NP maps Newton/PPN domain coefficients to acceleration, Poisson, gamma, beta, and preferred-frame residuals.",
            "Local GR/Newton recovery becomes a finite residual matrix problem.",
            "DERIVED_MATRIX_SCOPE",
        ),
        (
            "THM3735_2_EM_response_scope",
            "B_EM maps Hodge/frame/current/marker/tail coefficients to Poynting, Maxwell-stress, wave, polarization, and charge residuals.",
            "Maxwell/EM stress recovery becomes a finite residual matrix problem.",
            "DERIVED_MATRIX_SCOPE",
        ),
        (
            "THM3735_3_separation",
            "beta_NP/beta_EM are response norms only; source uncertainty stays in sigma_NP/sigma_EM.",
            "Prevents source-coupling gaps from being hidden inside response matrices.",
            "ANTI_SMUGGLING",
        ),
    ]
    return [
        {
            **base(ts),
            "theorem_id": theorem_id,
            "clause": clause,
            "meaning": meaning,
            "status": status,
            "claim_allowed": False,
        }
        for theorem_id, clause, meaning, status in rows
    ]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    gates = [
        ("CG3735_0_contract", "PASS_NONCLAIM", "operator-norm contracts written"),
        ("CG3735_1_B", "BLOCKED", "B_NP and B_EM entries are placeholders"),
        ("CG3735_2_G", "BLOCKED", "G_NP and G_EM positivity entries are placeholders"),
        ("CG3735_3_W", "BLOCKED", "W_NP and W_EM weight/covariance entries are placeholders"),
        ("CG3735_4_beta", "BLOCKED", "beta_NP and beta_EM are not executable"),
        ("CG3735_5_3729", "BLOCKED", "3729 still lacks executable beta_A plus sigma/ell/epsilon/bound rows"),
        ("CG3735_6_claim", "BLOCKED", "no Newton/PPN/EM/local-GR claim allowed"),
    ]
    return [
        {
            **base(ts),
            "gate_id": gate_id,
            "gate_status": status,
            "required_before_claim": required,
            "claim_allowed": False,
        }
        for gate_id, status, required in gates
    ]


def decision_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "DEC3735_0_beta_contract_ready",
            "BETA_RESPONSE_MATRIX_CONTRACT_READY",
            "beta_NP and beta_EM now have finite-basis matrix contracts rather than loose symbols.",
        ),
        (
            "DEC3735_1_blocked_correctly",
            "RESPONSE_MATRICES_BLOCKED_BY_PLACEHOLDERS",
            "No beta score is allowed until B/G/W entries are source-owned or theorem-owned.",
        ),
        (
            "DEC3735_2_next",
            "NEXT_DERIVE_NEWTON_PPN_MATRIX_COEFFICIENTS",
            "The GR/Newton route should attack B_NP first because acceleration, Poisson, gamma, and beta are the cleanest local-reduction observables.",
        ),
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


def status_rows(ts: str) -> list[dict[str, object]]:
    return [{
        **base(ts),
        "status_id": "STATUS3735_0",
        "status": "RESPONSE_MATRIX_CONTRACT_READY_VALUES_MISSING",
        "summary": "3735 builds finite B/G/W response-matrix contracts for beta_NP and beta_EM. Current entries are placeholders, so beta scoring and local claims remain blocked.",
        "claim_allowed": False,
    }]


def next_target_rows(ts: str) -> list[dict[str, object]]:
    return [{
        **base(ts),
        "next_id": "NEXT3735_0",
        "target_doc": "3736-Y5-R2FR-Newton-PPN-response-coefficients-from-weak-field-limit.md",
        "target_script": "scripts/Y5_R2FR_3736_Newton_PPN_response_coefficients_from_weak_field_limit.py",
        "objective": "derive the Newton/PPN response coefficients in B_NP from weak-field metric and Poisson relations before attempting EM matrix coefficients",
        "success_gate": "B_NP symbolic entries are sharpened into theorem-owned coefficient formulas or explicit refusal rows with exact missing assumptions",
        "claim_allowed": False,
    }]


def validation_rows(ts: str, paths: dict[str, Path]) -> list[dict[str, object]]:
    sources = parse_csv(paths["source_register"])
    csv_paths = [path for key, path in paths.items() if key not in {"doc", "validation"}]
    generated = [path for key, path in paths.items() if key != "validation"]
    formal_files = list(FORMALIZATION.rglob("*3735*")) if FORMALIZATION.exists() else []
    formal_files = [path for path in formal_files if path.is_file()]
    basis = parse_csv(paths["basis"])
    b_entries = parse_csv(paths["b_entries"])
    gw_entries = parse_csv(paths["gw_entries"])
    runner = parse_csv(paths["runner"])
    doc_text = read_text(paths["doc"])
    checks = [
        ("sources_exist", "sources exist", all(row["exists"] == "True" for row in sources)),
        ("needles_found", "source needles found", all(row["needle_found"] == "True" for row in sources)),
        ("outputs_exist", "outputs exist", all(path.exists() for path in generated)),
        ("csv_parse", "CSVs parse", all(len(parse_csv(path)) > 0 for path in csv_paths if path.exists())),
        ("basis_summary", "two finite basis summaries present", len(basis) == 2 and all(row["dimension_status"] == "FINITE_BASIS_READY" for row in basis)),
        ("B_entries", "fourteen B entries carried forward", len(b_entries) == 14),
        ("GW_entries", "twenty Gram/weight entries present", len(gw_entries) == 20),
        ("norm_contracts", "beta_NP and beta_EM norm contracts present", all(token in read_text(paths["norms"]) for token in ["beta_NP", "beta_EM", "lambda_max"])),
        ("runner_blocks", "runners block placeholder entries", all(row["status"] == "BLOCKED_MISSING_RESPONSE_MATRIX_ENTRIES" for row in runner)),
        ("positivity_gates", "six positivity gates present", len(parse_csv(paths["positivity"])) == 6),
        ("fill_rows", "beta fill rows target 3734", all(token in read_text(paths["fills"]) for token in ["FILL3734_NP", "FILL3734_EM"])),
        ("claim_gates_blocked", "claim gates block promotion", all(row["claim_allowed"] == "False" for row in parse_csv(paths["claim_gates"]))),
        ("next_target_3736", "next target is Newton/PPN coefficients", all(token in read_text(paths["next_target"]) for token in ["3736", "Newton", "B_NP"])),
        ("doc_core_terms", "doc contains response matrix status", all(token in doc_text for token in ["B_NP", "B_EM", "beta_NP", "beta_EM"])),
        ("no_formalization_leak", "no 3735 files in formalization-workbench", len(formal_files) == 0),
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
    lines = [
        "# 3735 - Response Matrix First Pass: Newton/PPN and EM",
        "",
        "## Status",
        "- `RESPONSE_MATRIX_CONTRACT_READY_VALUES_MISSING`",
        "- `beta_NP` and `beta_EM` now have finite `B/G/W` matrix contracts.",
        "- All entries remain placeholders, so this is a computability scaffold, not evidence.",
        "",
        "## Norm Contracts",
    ]
    for row in grouped["norms"]:
        lines.append(f"- `{row['norm_id']}` `{row['bridge']}`: {row['beta_formula']}")
    lines.extend(["", "## Basis Summary"])
    for row in grouped["basis"]:
        lines.append(f"- `{row['bridge']}` domain_dim={row['domain_dimension']} obs_dim={row['observable_dimension']} domain=`{row['domain_basis']}` observable=`{row['observable_basis']}`")
    lines.extend(["", "## B Entries"])
    for row in grouped["b_entries"]:
        lines.append(f"- `{row['entry_id']}` `{row['matrix']}` `{row['observable_row']}` <- `{row['domain_col']}` via `{row['symbolic_entry']}`")
    lines.extend(["", "## Positivity Gates"])
    for row in grouped["positivity"]:
        lines.append(f"- `{row['gate_id']}` `{row['gate_status']}`: {row['gate']} | {row['required_before_beta']}")
    lines.extend(["", "## Runner Rows"])
    for row in grouped["runner"]:
        lines.append(f"- `{row['runner_id']}` `{row['status']}` missing_count={len([item for item in str(row['missing_entries']).split(';') if item])}")
    lines.extend(["", "## Decisions"])
    for row in grouped["decisions"]:
        lines.append(f"- `{row['decision_id']}` `{row['decision']}` | {row['rationale']}")
    lines.extend(["", "## Next Target"])
    lines.append("- `3736-Y5-R2FR-Newton-PPN-response-coefficients-from-weak-field-limit.md`")
    lines.append("- Objective: derive the Newton/PPN response coefficients in `B_NP` from weak-field metric and Poisson relations.")
    paths["doc"].write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ts = stamp()
    paths = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3735_SOURCE_REGISTER.csv",
        "basis": RESIDUALS / "P8_Y5_R2FR_3735_BASIS_SUMMARY_ROWS.csv",
        "b_entries": RESIDUALS / "P8_Y5_R2FR_3735_B_MATRIX_ENTRY_ROWS.csv",
        "gw_entries": RESIDUALS / "P8_Y5_R2FR_3735_GRAM_WEIGHT_ENTRY_ROWS.csv",
        "norms": RESIDUALS / "P8_Y5_R2FR_3735_NORM_CONTRACT_ROWS.csv",
        "runner": RESIDUALS / "P8_Y5_R2FR_3735_RUNNER_STATUS.csv",
        "positivity": RESIDUALS / "P8_Y5_R2FR_3735_POSITIVITY_GATE_ROWS.csv",
        "fills": RESIDUALS / "P8_Y5_R2FR_3735_BETA_FILL_ROWS.csv",
        "refusals": RESIDUALS / "P8_Y5_R2FR_3735_REFUSAL_ROWS.csv",
        "theorems": RESIDUALS / "P8_Y5_R2FR_3735_THEOREM_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3735_CLAIM_GATES.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3735_DECISION_ROWS.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3735_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3735_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3735_VALIDATION.csv",
        "doc": DOC,
    }
    b_entries = b_matrix_rows(ts)
    gw_entries = metric_weight_rows(ts)
    runner = runner_rows(ts, b_entries, gw_entries)
    grouped = {
        "source_register": source_register(ts),
        "basis": basis_summary_rows(ts),
        "b_entries": b_entries,
        "gw_entries": gw_entries,
        "norms": norm_contract_rows(ts),
        "runner": runner,
        "positivity": positivity_gate_rows(ts),
        "fills": fill_rows(ts),
        "refusals": refusal_rows(ts, runner),
        "theorems": theorem_rows(ts),
        "claim_gates": claim_gate_rows(ts),
        "decisions": decision_rows(ts),
        "status": status_rows(ts),
        "next_target": next_target_rows(ts),
    }
    for key, rows in grouped.items():
        write_csv(paths[key], rows)
    write_doc(paths, grouped)
    write_csv(paths["validation"], validation_rows(ts, paths))
    failures = [row for row in parse_csv(paths["validation"]) if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3735 validation failed: {failures}")
    print("wrote 3735 checkpoint: response-matrix contracts ready and blocked by placeholder entries")


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3736"
BRANCH_ID = "MTS_R2FR_Y5_NEWTON_PPN_RESPONSE_COEFFICIENTS_FROM_WEAK_FIELD_LIMIT_3736"
DOC = ROOT / "3736-Y5-R2FR-Newton-PPN-response-coefficients-from-weak-field-limit.md"

DOC_3735 = ROOT / "3735-Y5-R2FR-response-matrix-first-pass-Newton-PPN-EM.md"
NEXT_3735 = RESIDUALS / "P8_Y5_R2FR_3735_NEXT_TARGET.csv"
VALIDATION_3735 = RESIDUALS / "P8_Y5_BRR545_3735_VALIDATION.csv"
B_ENTRIES_3735 = RESIDUALS / "P8_Y5_R2FR_3735_B_MATRIX_ENTRY_ROWS.csv"
BASIS_3735 = RESIDUALS / "P8_Y5_R2FR_3735_BASIS_SUMMARY_ROWS.csv"
NORM_3735 = RESIDUALS / "P8_Y5_R2FR_3735_NORM_CONTRACT_ROWS.csv"


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
        ("doc_3735", DOC_3735, "RESPONSE_MATRIX_CONTRACT_READY_VALUES_MISSING", "3735 matrix contract"),
        ("next_3735", NEXT_3735, "3736-Y5-R2FR-Newton-PPN-response-coefficients-from-weak-field-limit.md", "3735 handoff"),
        ("validation_3735", VALIDATION_3735, "next_target_3736", "3735 validation"),
        ("b_entries_3735", B_ENTRIES_3735, "BME3735_B3732_NP_accel_phi", "3735 B_NP entries"),
        ("basis_3735", BASIS_3735, "Newton_PPN_bridge", "3735 finite basis"),
        ("norm_3735", NORM_3735, "beta_NP", "3735 beta_NP norm contract"),
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


def coefficient_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "BNP3736_0_accel_phi",
            "BME3735_B3732_NP_accel_phi",
            "y_accel",
            "h_phi",
            "delta a = -grad(delta Phi), so ||y_accel|| <= C_grad ||h_phi||",
            "C_grad",
            "DERIVED_SHAPE_COEFFICIENT_MISSING_NORM",
            "domain norm, boundary conditions, and local length scale",
        ),
        (
            "BNP3736_1_poisson_phi",
            "BME3735_B3732_NP_poisson_phi",
            "y_poisson",
            "h_phi",
            "delta R_Poisson = nabla^2(delta Phi), so ||y_poisson|| <= C_lap ||h_phi||",
            "C_lap",
            "DERIVED_SHAPE_COEFFICIENT_MISSING_NORM",
            "domain norm and boundary/regularity class",
        ),
        (
            "BNP3736_2_poisson_gm",
            "BME3735_B3732_NP_poisson_gm",
            "y_poisson",
            "h_GM",
            "measured-GM/source normalization contributes |4*pi*rho_eff| |h_GM| to the Poisson residual",
            "4*pi*rho_eff_norm",
            "DERIVED_SHAPE_COEFFICIENT_MISSING_SOURCE_NORM",
            "rho_eff norm and measured-G calibration convention",
        ),
        (
            "BNP3736_3_gamma_phipsi",
            "BME3735_B3732_NP_gamma_phipsi",
            "y_gamma",
            "h_phi;h_psi",
            "for weak fields gamma≈Psi/Phi, delta(gamma-1)≈(h_psi-h_phi)/Phi0 after gauge/background normalization",
            "Phi0_inv acting on h_psi-h_phi",
            "CONDITIONAL_WEAK_FIELD_FORMULA",
            "nonzero Phi0 floor, gauge convention, and background potential normalization",
        ),
        (
            "BNP3736_4_beta_phi",
            "BME3735_B3732_NP_beta_phi",
            "y_beta",
            "h_phi",
            "beta-1 is second-order weak-field response; coefficient needs the parent 2PN metric-potential map",
            "C_beta_2PN",
            "FORMULA_TARGET_SECOND_ORDER_NOT_DERIVED",
            "2PN expansion, gauge, nonlinear closure, and parent metric coefficient",
        ),
        (
            "BNP3736_5_pref_pref",
            "BME3735_B3732_NP_pref_pref",
            "y_pref",
            "h_pref",
            "preferred-frame residual is linear in the retained disformal/preferred-frame coordinate",
            "C_preferred_frame",
            "CONDITIONAL_LINEAR_RESPONSE",
            "preferred-frame observable convention and disformal normalization",
        ),
        (
            "BNP3736_6_boundary",
            "BME3735_B3732_NP_boundary",
            "y_accel;y_poisson",
            "h_bdy",
            "boundary/support perturbations project into acceleration and Poisson residuals through C_boundary_projection",
            "C_boundary_projection",
            "BOUND_SCHEMA_READY_VALUES_MISSING",
            "boundary condition, support deformation, and local domain projector",
        ),
    ]
    return [
        {
            **base(ts),
            "coefficient_id": coefficient_id,
            "target_b_entry": target,
            "observable_row": observable,
            "domain_col": domain,
            "weak_field_derivation": derivation,
            "coefficient_symbol": symbol,
            "current_status": status,
            "missing_for_numeric_or_theorem": missing,
            "ready_for_3735": False,
            "claim_allowed": False,
        }
        for coefficient_id, target, observable, domain, derivation, symbol, status, missing in rows
    ]


def coefficient_input_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("CIN3736_0_C_grad", "C_grad", "MISSING_GRAD_OPERATOR_NORM", "positive", "operator norm", "gradient norm from potential basis to acceleration residual"),
        ("CIN3736_1_C_lap", "C_lap", "MISSING_LAPLACIAN_OPERATOR_NORM", "positive", "operator norm", "Laplacian norm from potential basis to Poisson residual"),
        ("CIN3736_2_rho", "rho_eff_norm", "MISSING_RHO_EFF_NORM", "nonnegative", "source density norm", "effective source density norm for measured-GM calibration"),
        ("CIN3736_3_Phi0", "Phi0_inv", "MISSING_PHI0_INVERSE_OR_SAFE_NORMALIZATION", "positive", "inverse potential scale", "safe weak-field normalization for gamma response"),
        ("CIN3736_4_Cbeta", "C_beta_2PN", "MISSING_2PN_BETA_COEFFICIENT", "nonnegative", "2PN response norm", "second-order beta response coefficient"),
        ("CIN3736_5_Cpref", "C_preferred_frame", "MISSING_PREFERRED_FRAME_COEFFICIENT", "nonnegative", "response norm", "preferred-frame response coefficient"),
        ("CIN3736_6_Cbdy", "C_boundary_projection", "MISSING_BOUNDARY_PROJECTION_NORM", "nonnegative", "response norm", "boundary/support projection norm"),
    ]
    return [
        {
            **base(ts),
            "input_id": input_id,
            "quantity": quantity,
            "value": value,
            "required_sign": sign,
            "units": units,
            "meaning": meaning,
            "source_path": "MISSING_SOURCE_OR_THEOREM_PATH",
            "source_owned": False,
            "claim_allowed": False,
        }
        for input_id, quantity, value, sign, units, meaning in specs
    ]


def updated_b_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "target_b_entry": row["target_b_entry"],
            "bridge": "Newton_PPN_bridge",
            "matrix": "B_NP",
            "observable_row": row["observable_row"],
            "domain_col": row["domain_col"],
            "sharpened_entry": row["coefficient_symbol"],
            "derivation_status": row["current_status"],
            "value": "MISSING_NUMERIC_OR_THEOREM_ENTRY",
            "source_path": str(DOC),
            "source_owned": False,
            "claim_allowed": False,
        }
        for row in coefficient_rows(ts)
    ]


def runner_rows(ts: str) -> list[dict[str, object]]:
    coeffs = coefficient_rows(ts)
    ready_count = sum(1 for row in coeffs if row["current_status"] in {"DERIVED_NUMERIC", "THEOREM_OWNED"})
    return [{
        **base(ts),
        "runner_id": "RUN3736_0_BNP_WEAK_FIELD_COEFFICIENTS",
        "total_coefficients": len(coeffs),
        "ready_coefficients": ready_count,
        "shape_derived_coefficients": 5,
        "second_order_blocked": True,
        "numeric_executable": False,
        "status": "B_NP_SHAPES_SHARPENED_NUMERIC_VALUES_MISSING",
        "claim_allowed": False,
    }]


def refusal_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "refusal_id": f"REF3736_{row['coefficient_id']}",
            "target_b_entry": row["target_b_entry"],
            "reason": row["current_status"],
            "required_fix": row["missing_for_numeric_or_theorem"],
            "claim_allowed": False,
        }
        for row in coefficient_rows(ts)
    ]


def theorem_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "THM3736_0_Newton_accel",
            "Newtonian local acceleration residual is the gradient response of the potential perturbation: delta a=-grad delta Phi.",
            "This derives the y_accel<-h_phi B_NP entry shape.",
            "DERIVED_WEAK_FIELD_SHAPE",
        ),
        (
            "THM3736_1_Poisson",
            "Poisson residual is nabla^2 delta Phi minus measured-source normalization terms.",
            "This derives y_poisson<-h_phi and y_poisson<-h_GM entry shapes.",
            "DERIVED_WEAK_FIELD_SHAPE",
        ),
        (
            "THM3736_2_gamma",
            "In a fixed weak-field gauge with nonzero background potential scale, gamma response is controlled by h_psi-h_phi.",
            "This derives the gamma row conditionally and exposes the gauge/Phi0 dependency.",
            "CONDITIONAL_WEAK_FIELD_SHAPE",
        ),
        (
            "THM3736_3_beta",
            "PPN beta is 2PN/second-order and cannot be derived from the first-order Newtonian potential row alone.",
            "This prevents falsely promoting beta from a 1PN scaffold.",
            "ANTI_OVERCLAIM",
        ),
        (
            "THM3736_4_claim_gate",
            "B_NP shapes are sharper but not numeric/source-owned; beta_NP remains blocked in 3735.",
            "Shape derivation is progress, not an empirical or local-GR pass.",
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
        ("CG3736_0_shapes", "PASS_NONCLAIM", "Newton/Poisson/gamma/pref/boundary B_NP shapes are written"),
        ("CG3736_1_norms", "BLOCKED", "operator norms C_grad,C_lap,C_pref,C_boundary are missing"),
        ("CG3736_2_gamma", "BLOCKED", "Phi0/gauge normalization is missing"),
        ("CG3736_3_beta", "BLOCKED", "2PN beta coefficient is not derived"),
        ("CG3736_4_3735", "BLOCKED", "B_NP entries are not source-owned numeric/theorem rows for 3735"),
        ("CG3736_5_claim", "BLOCKED", "no local GR/Newton/PPN claim allowed"),
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
            "DEC3736_0_progress",
            "B_NP_WEAK_FIELD_SHAPES_SHARPENED",
            "The Newton/PPN response matrix is no longer anonymous: acceleration, Poisson, gamma, preferred-frame, and boundary rows have weak-field formulas.",
        ),
        (
            "DEC3736_1_beta_block",
            "BETA_REQUIRES_2PN_PARENT_MAP",
            "PPN beta is explicitly held back until the second-order parent weak-field expansion is derived.",
        ),
        (
            "DEC3736_2_next",
            "NEXT_DO_EM_MATRIX_OR_2PN_BETA",
            "The best continuation is either EM/Poynting B_EM coefficient derivation, or a focused 2PN beta parent expansion.",
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
        "status_id": "STATUS3736_0",
        "status": "B_NP_SHAPES_SHARPENED_NUMERIC_VALUES_MISSING",
        "summary": "3736 sharpens Newton/PPN response matrix entries from weak-field relations while blocking numeric beta_NP until operator norms, gauge normalization, and the 2PN beta coefficient are owned.",
        "claim_allowed": False,
    }]


def next_target_rows(ts: str) -> list[dict[str, object]]:
    return [{
        **base(ts),
        "next_id": "NEXT3736_0",
        "target_doc": "3737-Y5-R2FR-EM-Poynting-response-coefficients-from-Hodge-Maxwell.md",
        "target_script": "scripts/Y5_R2FR_3737_EM_Poynting_response_coefficients_from_Hodge_Maxwell.py",
        "objective": "derive the EM/Poynting response entries in B_EM from Hodge/constitutive Maxwell identities before returning to numeric beta assembly",
        "success_gate": "B_EM symbolic entries are sharpened into theorem-owned coefficient formulas or explicit refusal rows with exact missing assumptions",
        "claim_allowed": False,
    }]


def validation_rows(ts: str, paths: dict[str, Path]) -> list[dict[str, object]]:
    sources = parse_csv(paths["source_register"])
    csv_paths = [path for key, path in paths.items() if key not in {"doc", "validation"}]
    generated = [path for key, path in paths.items() if key != "validation"]
    formal_files = list(FORMALIZATION.rglob("*3736*")) if FORMALIZATION.exists() else []
    formal_files = [path for path in formal_files if path.is_file()]
    coeffs = parse_csv(paths["coefficients"])
    inputs = parse_csv(paths["inputs"])
    doc_text = read_text(paths["doc"])
    checks = [
        ("sources_exist", "sources exist", all(row["exists"] == "True" for row in sources)),
        ("needles_found", "source needles found", all(row["needle_found"] == "True" for row in sources)),
        ("outputs_exist", "outputs exist", all(path.exists() for path in generated)),
        ("csv_parse", "CSVs parse", all(len(parse_csv(path)) > 0 for path in csv_paths if path.exists())),
        ("coefficients", "seven Newton/PPN coefficient rows present", len(coeffs) == 7),
        ("weak_field_shapes", "Newton/Poisson/gamma shapes present", all(token in read_text(paths["coefficients"]) for token in ["delta a", "nabla^2", "gamma≈Psi/Phi"])),
        ("inputs", "seven coefficient input rows present", len(inputs) == 7),
        ("updated_b", "updated B_NP rows present", len(parse_csv(paths["updated_b"])) == 7),
        ("runner_blocks", "runner blocks numeric beta", parse_csv(paths["runner"])[0]["status"] == "B_NP_SHAPES_SHARPENED_NUMERIC_VALUES_MISSING"),
        ("beta_block", "2PN beta block is explicit", "2PN" in read_text(paths["theorems"]) and "beta" in read_text(paths["theorems"])),
        ("claim_gates_blocked", "claim gates block promotion", all(row["claim_allowed"] == "False" for row in parse_csv(paths["claim_gates"]))),
        ("next_target_3737", "next target is EM/Poynting matrix", all(token in read_text(paths["next_target"]) for token in ["3737", "EM", "B_EM"])),
        ("doc_core_terms", "doc contains weak-field coefficient status", all(token in doc_text for token in ["B_NP", "delta a", "Poisson", "gamma", "2PN"])),
        ("no_formalization_leak", "no 3736 files in formalization-workbench", len(formal_files) == 0),
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
        "# 3736 - Newton/PPN Response Coefficients from Weak-Field Limit",
        "",
        "## Status",
        "- `B_NP_SHAPES_SHARPENED_NUMERIC_VALUES_MISSING`",
        "- Newton/PPN `B_NP` entries now have weak-field coefficient formulas.",
        "- `beta_NP` remains blocked because operator norms, gauge normalization, and the 2PN beta map are not source-owned.",
        "",
        "## Coefficient Rows",
    ]
    for row in grouped["coefficients"]:
        lines.append(f"- `{row['coefficient_id']}` `{row['target_b_entry']}`: {row['weak_field_derivation']} -> `{row['coefficient_symbol']}` | status `{row['current_status']}`")
    lines.extend(["", "## Required Inputs"])
    for row in grouped["inputs"]:
        lines.append(f"- `{row['quantity']}` = `{row['value']}` | {row['meaning']}")
    lines.extend(["", "## Theorem Rows"])
    for row in grouped["theorems"]:
        lines.append(f"- `{row['theorem_id']}` `{row['status']}`: {row['clause']} | {row['meaning']}")
    lines.extend(["", "## Decisions"])
    for row in grouped["decisions"]:
        lines.append(f"- `{row['decision_id']}` `{row['decision']}` | {row['rationale']}")
    lines.extend(["", "## Next Target"])
    lines.append("- `3737-Y5-R2FR-EM-Poynting-response-coefficients-from-Hodge-Maxwell.md`")
    lines.append("- Objective: derive the EM/Poynting `B_EM` response entries from Hodge/constitutive Maxwell identities.")
    paths["doc"].write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ts = stamp()
    paths = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3736_SOURCE_REGISTER.csv",
        "coefficients": RESIDUALS / "P8_Y5_R2FR_3736_BNP_COEFFICIENT_ROWS.csv",
        "inputs": RESIDUALS / "P8_Y5_R2FR_3736_COEFFICIENT_INPUT_ROWS.csv",
        "updated_b": RESIDUALS / "P8_Y5_R2FR_3736_UPDATED_BNP_ROWS.csv",
        "runner": RESIDUALS / "P8_Y5_R2FR_3736_RUNNER_STATUS.csv",
        "refusals": RESIDUALS / "P8_Y5_R2FR_3736_REFUSAL_ROWS.csv",
        "theorems": RESIDUALS / "P8_Y5_R2FR_3736_THEOREM_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3736_CLAIM_GATES.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3736_DECISION_ROWS.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3736_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3736_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3736_VALIDATION.csv",
        "doc": DOC,
    }
    grouped = {
        "source_register": source_register(ts),
        "coefficients": coefficient_rows(ts),
        "inputs": coefficient_input_rows(ts),
        "updated_b": updated_b_rows(ts),
        "runner": runner_rows(ts),
        "refusals": refusal_rows(ts),
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
        raise SystemExit(f"3736 validation failed: {failures}")
    print("wrote 3736 checkpoint: Newton/PPN B_NP weak-field coefficient shapes sharpened, numeric values missing")


if __name__ == "__main__":
    main()

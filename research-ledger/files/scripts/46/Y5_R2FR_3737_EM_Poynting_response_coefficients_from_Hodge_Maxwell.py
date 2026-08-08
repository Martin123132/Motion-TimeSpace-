from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3737"
BRANCH_ID = "MTS_R2FR_Y5_EM_POYNTING_RESPONSE_COEFFICIENTS_FROM_HODGE_MAXWELL_3737"
DOC = ROOT / "3737-Y5-R2FR-EM-Poynting-response-coefficients-from-Hodge-Maxwell.md"

DOC_3736 = ROOT / "3736-Y5-R2FR-Newton-PPN-response-coefficients-from-weak-field-limit.md"
NEXT_3736 = RESIDUALS / "P8_Y5_R2FR_3736_NEXT_TARGET.csv"
VALIDATION_3736 = RESIDUALS / "P8_Y5_BRR545_3736_VALIDATION.csv"
B_ENTRIES_3735 = RESIDUALS / "P8_Y5_R2FR_3735_B_MATRIX_ENTRY_ROWS.csv"
BASIS_3735 = RESIDUALS / "P8_Y5_R2FR_3735_BASIS_SUMMARY_ROWS.csv"
NORM_3735 = RESIDUALS / "P8_Y5_R2FR_3735_NORM_CONTRACT_ROWS.csv"
DOC_3733 = ROOT / "3733-Y5-R2FR-HX-and-Hodge-variation-zero-or-bound.md"
HEURISTIC_00 = ROOT / "00-martin-fork-heuristics-private.md"


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
        ("doc_3736", DOC_3736, "EM/Poynting `B_EM` response entries", "3736 handoff to EM coefficients"),
        ("next_3736", NEXT_3736, "3737-Y5-R2FR-EM-Poynting-response-coefficients-from-Hodge-Maxwell.md", "3736 next target"),
        ("validation_3736", VALIDATION_3736, "next_target_3737", "3736 validation"),
        ("b_entries_3735", B_ENTRIES_3735, "BME3735_B3732_EM_poynting_chi", "3735 B_EM entries"),
        ("basis_3735", BASIS_3735, "EM_Poynting_bridge", "3735 finite EM basis"),
        ("norm_3735", NORM_3735, "beta_EM", "3735 beta_EM norm contract"),
        ("doc_3733", DOC_3733, "partial_X chi", "3733 Hodge variation bound/zero theorem"),
        ("heuristic_00", HEURISTIC_00, "Poynting", "private EM/Poynting fork heuristic"),
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
            "BEM3737_0_poynting_chi",
            "BME3735_B3732_EM_poynting_chi",
            "y_poynting",
            "h_chi",
            "Poynting theorem residual delta(partial_t u + div S) from constitutive/Hodge variation obeys ||y_poynting|| <= C_poynting_chi ||h_chi|| on fixed fields.",
            "C_poynting_chi",
            "DERIVED_SHAPE_COEFFICIENT_MISSING_FIELD_NORM",
            "background EM field norm, constitutive derivative, domain regularity, and time-slice convention",
        ),
        (
            "BEM3737_1_poynting_current",
            "BME3735_B3732_EM_poynting_current",
            "y_poynting",
            "h_Jem",
            "delta(J dot E) gives ||y_poynting|| <= C_JdotE ||h_Jem|| with C_JdotE controlled by local electric-field/readout norm.",
            "C_JdotE",
            "DERIVED_SHAPE_COEFFICIENT_MISSING_E_FIELD_NORM",
            "electric field norm, current normalization, and sign/readout convention",
        ),
        (
            "BEM3737_2_stress_frame",
            "BME3735_B3732_EM_stress_frame",
            "y_stress",
            "h_frame",
            "metric/frame variation changes Maxwell stress and its divergence, so ||y_stress|| <= C_TEM_frame ||h_frame||.",
            "C_TEM_frame",
            "DERIVED_SHAPE_COEFFICIENT_MISSING_STRESS_NORM",
            "EM stress norm, connection/frame variation, and boundary conditions",
        ),
        (
            "BEM3737_3_wave_chi",
            "BME3735_B3732_EM_wave_chi",
            "y_wave",
            "h_chi",
            "linearized Maxwell wave operator in a constitutive medium gives ||y_wave|| <= C_wave_chi ||h_chi||.",
            "C_wave_chi",
            "CONDITIONAL_MAXWELL_WAVE_FORMULA",
            "vacuum/material constitutive law, gauge choice, dispersion convention, and field regularity",
        ),
        (
            "BEM3737_4_pol_chi",
            "BME3735_B3732_EM_pol_chi",
            "y_pol",
            "h_chi",
            "anisotropic or parity-odd pieces of h_chi project into polarization/birefringence residuals through C_birefringence.",
            "C_birefringence",
            "CONDITIONAL_CONSTITUTIVE_POLARIZATION_FORMULA",
            "polarization basis, anisotropic Hodge decomposition, and observational norm",
        ),
        (
            "BEM3737_5_charge_marker",
            "BME3735_B3732_EM_charge_marker",
            "y_charge",
            "h_alpha",
            "charge/fine-structure marker variation perturbs continuity/readout as ||y_charge|| <= C_charge_marker ||h_alpha||.",
            "C_charge_marker",
            "BOUND_SCHEMA_READY_VALUES_MISSING",
            "charge marker descent theorem or finite b_alpha/source-current normalization",
        ),
        (
            "BEM3737_6_tail",
            "BME3735_B3732_EM_tail",
            "y_poynting;y_stress;y_wave;y_pol;y_charge",
            "h_EM_tail",
            "retained EM boundary/non-Hilbert/material tails project into all EM observables through C_EM_tail_projection.",
            "C_EM_tail_projection",
            "BOUND_SCHEMA_READY_VALUES_MISSING",
            "tail decomposition, boundary/source support, and no-cancellation envelope",
        ),
    ]
    return [
        {
            **base(ts),
            "coefficient_id": coefficient_id,
            "target_b_entry": target,
            "observable_row": observable,
            "domain_col": domain,
            "hodge_maxwell_derivation": derivation,
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
        ("CIN3737_0_Cpoynting", "C_poynting_chi", "MISSING_POYNTING_CHI_OPERATOR_NORM", "nonnegative", "response norm", "constitutive/Hodge perturbation to Poynting residual"),
        ("CIN3737_1_CJdotE", "C_JdotE", "MISSING_J_DOT_E_OPERATOR_NORM", "nonnegative", "response norm", "source-current perturbation to Poynting residual"),
        ("CIN3737_2_CTEM", "C_TEM_frame", "MISSING_TEM_FRAME_OPERATOR_NORM", "nonnegative", "response norm", "metric/frame perturbation to Maxwell stress residual"),
        ("CIN3737_3_Cwave", "C_wave_chi", "MISSING_WAVE_CHI_OPERATOR_NORM", "nonnegative", "response norm", "constitutive perturbation to wave residual"),
        ("CIN3737_4_Cpol", "C_birefringence", "MISSING_BIREFRINGENCE_OPERATOR_NORM", "nonnegative", "response norm", "anisotropic Hodge perturbation to polarization residual"),
        ("CIN3737_5_Ccharge", "C_charge_marker", "MISSING_CHARGE_MARKER_OPERATOR_NORM", "nonnegative", "response norm", "charge/fine-structure marker perturbation to continuity/readout residual"),
        ("CIN3737_6_Ctail", "C_EM_tail_projection", "MISSING_EM_TAIL_PROJECTION_NORM", "nonnegative", "response norm", "retained EM tail projection to observables"),
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
            "bridge": "EM_Poynting_bridge",
            "matrix": "B_EM",
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
        "runner_id": "RUN3737_0_BEM_HODGE_MAXWELL_COEFFICIENTS",
        "total_coefficients": len(coeffs),
        "ready_coefficients": ready_count,
        "shape_derived_coefficients": 5,
        "tail_or_marker_blocked": True,
        "numeric_executable": False,
        "status": "B_EM_SHAPES_SHARPENED_NUMERIC_VALUES_MISSING",
        "claim_allowed": False,
    }]


def refusal_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "refusal_id": f"REF3737_{row['coefficient_id']}",
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
            "THM3737_0_Poynting",
            "Poynting theorem residual responds to constitutive/Hodge variation and source-current variation through C_poynting_chi and C_JdotE.",
            "This derives the y_poynting rows from Hodge/Maxwell bookkeeping.",
            "DERIVED_HODGE_MAXWELL_SHAPE",
        ),
        (
            "THM3737_1_Maxwell_stress",
            "Maxwell stress residual responds to frame/metric perturbation through C_TEM_frame.",
            "This keeps EM stress tied to H^X rather than assumed Maxwell recovery.",
            "DERIVED_STRESS_SHAPE",
        ),
        (
            "THM3737_2_wave_polarization",
            "Wave and polarization residuals are controlled by constitutive/Hodge perturbations, with birefringence separated from scalar wave-speed response.",
            "This separates isotropic propagation shifts from anisotropic/polarization effects.",
            "CONDITIONAL_CONSTITUTIVE_SHAPE",
        ),
        (
            "THM3737_3_charge_marker",
            "Charge/fine-structure marker variation and EM tail terms are not killed by Maxwell identities; they need no-marker/no-tail theorems or finite bounds.",
            "Prevents hiding charge/readout coupling or retained tail coupling in the EM sector.",
            "ANTI_OVERCLAIM",
        ),
        (
            "THM3737_4_claim_gate",
            "B_EM shapes are sharper but not numeric/source-owned; beta_EM remains blocked in 3735.",
            "Shape derivation is progress, not an EM/Maxwell pass.",
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
        ("CG3737_0_shapes", "PASS_NONCLAIM", "Poynting/stress/wave/polarization/charge B_EM shapes are written"),
        ("CG3737_1_hodge", "BLOCKED", "constitutive/Hodge operator norms are missing"),
        ("CG3737_2_fields", "BLOCKED", "background EM field/stress/current norms are missing"),
        ("CG3737_3_marker", "BLOCKED", "charge/fine-structure marker theorem-zero or finite bound is missing"),
        ("CG3737_4_tail", "BLOCKED", "EM tail decomposition and projection norm are missing"),
        ("CG3737_5_3735", "BLOCKED", "B_EM entries are not source-owned numeric/theorem rows for 3735"),
        ("CG3737_6_claim", "BLOCKED", "no Maxwell/EM/Poynting claim allowed"),
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
            "DEC3737_0_progress",
            "B_EM_HODGE_MAXWELL_SHAPES_SHARPENED",
            "The EM/Poynting response matrix is no longer anonymous: Poynting, stress, wave, polarization, charge, and tail rows have Hodge/Maxwell formulas.",
        ),
        (
            "DEC3737_1_marker_tail_block",
            "CHARGE_MARKER_AND_EM_TAILS_REMAIN_EXPLICIT",
            "Maxwell identities do not prove away marker constants or hidden/tail terms.",
        ),
        (
            "DEC3737_2_next",
            "NEXT_ASSEMBLE_BETA_INTERFACE_OR_ATTACK_2PN",
            "Both B_NP and B_EM now have sharpened shapes; the next disciplined step is a beta assembly/interface ledger, then focused 2PN beta or numeric norm acquisition.",
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
        "status_id": "STATUS3737_0",
        "status": "B_EM_SHAPES_SHARPENED_NUMERIC_VALUES_MISSING",
        "summary": "3737 sharpens EM/Poynting response matrix entries from Hodge/Maxwell identities while blocking numeric beta_EM until constitutive, field, marker, and tail norms are owned.",
        "claim_allowed": False,
    }]


def next_target_rows(ts: str) -> list[dict[str, object]]:
    return [{
        **base(ts),
        "next_id": "NEXT3737_0",
        "target_doc": "3738-Y5-R2FR-beta-assembly-interface-and-open-coefficient-ledger.md",
        "target_script": "scripts/Y5_R2FR_3738_beta_assembly_interface_and_open_coefficient_ledger.py",
        "objective": "combine 3736 B_NP and 3737 B_EM sharpened coefficient rows with 3735 beta contracts, producing an explicit open-input ledger for beta_NP and beta_EM",
        "success_gate": "beta_NP/beta_EM readiness rows identify every remaining norm, gauge, field, marker, tail, Gram, and weight input before 3729 can score",
        "claim_allowed": False,
    }]


def validation_rows(ts: str, paths: dict[str, Path]) -> list[dict[str, object]]:
    sources = parse_csv(paths["source_register"])
    csv_paths = [path for key, path in paths.items() if key not in {"doc", "validation"}]
    generated = [path for key, path in paths.items() if key != "validation"]
    formal_files = list(FORMALIZATION.rglob("*3737*")) if FORMALIZATION.exists() else []
    formal_files = [path for path in formal_files if path.is_file()]
    coeffs = parse_csv(paths["coefficients"])
    inputs = parse_csv(paths["inputs"])
    doc_text = read_text(paths["doc"])
    checks = [
        ("sources_exist", "sources exist", all(row["exists"] == "True" for row in sources)),
        ("needles_found", "source needles found", all(row["needle_found"] == "True" for row in sources)),
        ("outputs_exist", "outputs exist", all(path.exists() for path in generated)),
        ("csv_parse", "CSVs parse", all(len(parse_csv(path)) > 0 for path in csv_paths if path.exists())),
        ("coefficients", "seven EM/Poynting coefficient rows present", len(coeffs) == 7),
        ("hodge_maxwell_shapes", "Poynting/stress/wave/polarization shapes present", all(token in read_text(paths["coefficients"]) for token in ["Poynting", "Maxwell stress", "wave", "birefringence"])),
        ("inputs", "seven coefficient input rows present", len(inputs) == 7),
        ("updated_b", "updated B_EM rows present", len(parse_csv(paths["updated_b"])) == 7),
        ("runner_blocks", "runner blocks numeric beta", parse_csv(paths["runner"])[0]["status"] == "B_EM_SHAPES_SHARPENED_NUMERIC_VALUES_MISSING"),
        ("marker_tail_block", "marker and tail blocks explicit", all(token in read_text(paths["theorems"]) for token in ["marker", "tail", "beta_EM"])),
        ("claim_gates_blocked", "claim gates block promotion", all(row["claim_allowed"] == "False" for row in parse_csv(paths["claim_gates"]))),
        ("next_target_3738", "next target is beta assembly ledger", all(token in read_text(paths["next_target"]) for token in ["3738", "beta_NP", "beta_EM"])),
        ("doc_core_terms", "doc contains EM coefficient status", all(token in doc_text for token in ["B_EM", "Poynting", "Maxwell", "beta_EM"])),
        ("no_formalization_leak", "no 3737 files in formalization-workbench", len(formal_files) == 0),
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
        "# 3737 - EM/Poynting Response Coefficients from Hodge/Maxwell",
        "",
        "## Status",
        "- `B_EM_SHAPES_SHARPENED_NUMERIC_VALUES_MISSING`",
        "- EM/Poynting `B_EM` entries now have Hodge/Maxwell coefficient formulas.",
        "- `beta_EM` remains blocked because constitutive, field, marker, and tail norms are not source-owned.",
        "",
        "## Coefficient Rows",
    ]
    for row in grouped["coefficients"]:
        lines.append(f"- `{row['coefficient_id']}` `{row['target_b_entry']}`: {row['hodge_maxwell_derivation']} -> `{row['coefficient_symbol']}` | status `{row['current_status']}`")
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
    lines.append("- `3738-Y5-R2FR-beta-assembly-interface-and-open-coefficient-ledger.md`")
    lines.append("- Objective: combine sharpened `B_NP` and `B_EM` coefficient rows with 3735 beta contracts and emit the open-input ledger for beta assembly.")
    paths["doc"].write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ts = stamp()
    paths = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3737_SOURCE_REGISTER.csv",
        "coefficients": RESIDUALS / "P8_Y5_R2FR_3737_BEM_COEFFICIENT_ROWS.csv",
        "inputs": RESIDUALS / "P8_Y5_R2FR_3737_COEFFICIENT_INPUT_ROWS.csv",
        "updated_b": RESIDUALS / "P8_Y5_R2FR_3737_UPDATED_BEM_ROWS.csv",
        "runner": RESIDUALS / "P8_Y5_R2FR_3737_RUNNER_STATUS.csv",
        "refusals": RESIDUALS / "P8_Y5_R2FR_3737_REFUSAL_ROWS.csv",
        "theorems": RESIDUALS / "P8_Y5_R2FR_3737_THEOREM_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3737_CLAIM_GATES.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3737_DECISION_ROWS.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3737_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3737_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3737_VALIDATION.csv",
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
        raise SystemExit(f"3737 validation failed: {failures}")
    print("wrote 3737 checkpoint: EM/Poynting B_EM Hodge/Maxwell coefficient shapes sharpened, numeric values missing")


if __name__ == "__main__":
    main()

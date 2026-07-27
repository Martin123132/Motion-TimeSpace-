from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3749"
BRANCH_ID = "MTS_R2FR_Y5_LOCAL_FERMI_DOMAIN_PROJECTOR_LEAK_NUMERIC_SMOKE_3749"
DOC = ROOT / "3749-Y5-R2FR-local-Fermi-domain-projector-leak-numeric-smoke.md"

DOC_3748 = ROOT / "3748-Y5-R2FR-parent-bundle-split-construction-or-projector-leak-bound.md"
BOUNDS_3748 = RESIDUALS / "P8_Y5_R2FR_3748_PROJECTOR_LEAK_BOUND_FORMULAS.csv"
GATES_3748 = RESIDUALS / "P8_Y5_R2FR_3748_CLAIM_GATES.csv"
NEXT_3748 = RESIDUALS / "P8_Y5_R2FR_3748_NEXT_TARGET.csv"
VALIDATION_3748 = RESIDUALS / "P8_Y5_BRR545_3748_VALIDATION.csv"
PPN_3742 = RESIDUALS / "P8_Y5_R2FR_3742_PPN_TOLERANCE_GATE_ROWS.csv"
CG_1029 = ROOT / "1029-Y5-R10-cg-no-shadow-frame-theorem-or-first-numeric-coupling-row.md"


G = 6.67430e-11
C = 299_792_458.0
M_SUN = 1.98847e30
M_EARTH = 5.9722e24
R_SUN = 6.957e8
R_EARTH = 6.371e6
AU = 1.495978707e11
TOL_GAMMA_SMOKE = 2.3e-5
TOL_BETA_SMOKE = 7.8e-5
TOL_NEWTON_SMOKE = 1.0e-5


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(timestamp: str) -> dict[str, object]:
    return {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def read_lines(path: Path) -> list[str]:
    return read_text(path).splitlines()


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


def find_line(path: Path, needle: str) -> tuple[int, str]:
    for line_number, line in enumerate(read_lines(path), start=1):
        if needle in line:
            return line_number, line.strip()
    return 0, ""


def source_register(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("doc_3748_status", DOC_3748, "BUNDLE_SPLIT_ANSATZ_AND_PROJECTOR_LEAK_BOUND_FORMULAS_READY_VALUES_MISSING", "3748 handoff status"),
        ("doc_3748_fermi", DOC_3748, "Fermi-domain drift", "Fermi-domain bound path"),
        ("bounds_3748_fermi", BOUNDS_3748, "epsilon_comm_Fermi", "machine-readable Fermi bound formula"),
        ("gates_3748_values_missing", GATES_3748, "CG3748_5_bound_values", "values missing gate"),
        ("next_3748", NEXT_3748, "3749-Y5-R2FR-local-Fermi-domain-projector-leak-numeric-smoke.md", "3748 next target"),
        ("validation_3748", VALIDATION_3748, "no_formalization_leak", "3748 clean validation"),
        ("ppn_3742", PPN_3742, "PT3742_3_combined", "symbolic PPN tolerance gate"),
        ("cg_1029_gamma", CG_1029, "2.3e-05", "older nonclaim gamma threshold placeholder"),
        ("cg_1029_beta", CG_1029, "7.8e-05", "older nonclaim beta threshold placeholder"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        line_number, line_text = find_line(path, needle) if exists else (0, "")
        rows.append({
            **base(timestamp),
            "source_id": source_id,
            "path": str(path),
            "exists": exists,
            "needle": needle,
            "needle_found": needle in text,
            "line_number": line_number,
            "line_text": line_text,
            "role": role,
            "claim_allowed": False,
        })
    return rows


def constants_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("CONST3749_0_G", "G", G, "m^3 kg^-1 s^-2", "standard SI nominal for smoke only"),
        ("CONST3749_1_c", "c", C, "m s^-1", "standard exact SI speed of light"),
        ("CONST3749_2_M_sun", "M_sun", M_SUN, "kg", "nominal solar mass parameter proxy via mass, smoke only"),
        ("CONST3749_3_M_earth", "M_earth", M_EARTH, "kg", "nominal Earth mass, smoke only"),
        ("CONST3749_4_R_sun", "R_sun", R_SUN, "m", "nominal solar radius, smoke only"),
        ("CONST3749_5_R_earth", "R_earth", R_EARTH, "m", "nominal Earth radius, smoke only"),
        ("CONST3749_6_AU", "AU", AU, "m", "astronomical unit, smoke only"),
        ("CONST3749_7_tol_gamma", "tol_gamma_smoke", TOL_GAMMA_SMOKE, "dimensionless", "prior nonclaim placeholder, not a claim source"),
        ("CONST3749_8_tol_beta", "tol_beta_smoke", TOL_BETA_SMOKE, "dimensionless", "prior nonclaim placeholder, not a claim source"),
        ("CONST3749_9_tol_newton", "tol_newton_smoke", TOL_NEWTON_SMOKE, "dimensionless", "rough smoke tolerance, not a claim source"),
    ]
    return [
        {
            **base(timestamp),
            "constant_id": constant_id,
            "symbol": symbol,
            "value": f"{value:.12e}",
            "units": units,
            "provenance_note": note,
            "claim_allowed": False,
        }
        for constant_id, symbol, value, units, note in specs
    ]


def curvature_scale(mass: float, radius: float) -> tuple[float, float]:
    riemann = math.sqrt(48.0) * G * mass / (C * C * radius**3)
    grad_riemann = 3.0 * riemann / radius
    return riemann, grad_riemann


def scenario_input_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("SC3749_0_earth_surface_1m", "Earth surface 1 m lab domain", M_EARTH, R_EARTH, 1.0, 1.0, 1.0, 1.0, 1.0),
        ("SC3749_1_earth_surface_1km", "Earth surface 1 km domain", M_EARTH, R_EARTH, 1.0e3, 1.0, 1.0, 1.0, 1.0),
        ("SC3749_2_solar_1AU_1m", "Solar field at 1 AU, 1 m domain", M_SUN, AU, 1.0, 1.0, 1.0, 1.0, 1.0),
        ("SC3749_3_solar_1AU_1km", "Solar field at 1 AU, 1 km domain", M_SUN, AU, 1.0e3, 1.0, 1.0, 1.0, 1.0),
        ("SC3749_4_solar_surface_1m", "Solar surface field, 1 m domain", M_SUN, R_SUN, 1.0, 1.0, 1.0, 1.0, 1.0),
        ("SC3749_5_solar_surface_1km", "Solar surface field, 1 km domain", M_SUN, R_SUN, 1.0e3, 1.0, 1.0, 1.0, 1.0),
        ("SC3749_6_solar_1AU_large_domain", "Solar field at 1 AU, AU-scale domain", M_SUN, AU, AU, 1.0, 1.0, 1.0, 1.0),
    ]
    rows: list[dict[str, object]] = []
    for scenario_id, label, mass, radius, domain_length, c_pair, c_fermi, c_fermi2, norm_product in specs:
        riemann, grad_riemann = curvature_scale(mass, radius)
        rows.append({
            **base(timestamp),
            "scenario_id": scenario_id,
            "label": label,
            "mass_kg": f"{mass:.12e}",
            "radius_m": f"{radius:.12e}",
            "domain_length_m": f"{domain_length:.12e}",
            "C_pair": f"{c_pair:.12e}",
            "C_Fermi": f"{c_fermi:.12e}",
            "C_Fermi2": f"{c_fermi2:.12e}",
            "operator_norm_product": f"{norm_product:.12e}",
            "riemann_norm_1_per_m2": f"{riemann:.12e}",
            "grad_riemann_norm_1_per_m3": f"{grad_riemann:.12e}",
            "claim_allowed": False,
        })
    return rows


def smoke_result_rows(timestamp: str, inputs: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in inputs:
        domain_length = float(row["domain_length_m"])
        c_pair = float(row["C_pair"])
        c_fermi = float(row["C_Fermi"])
        c_fermi2 = float(row["C_Fermi2"])
        norm_product = float(row["operator_norm_product"])
        riemann = float(row["riemann_norm_1_per_m2"])
        grad_riemann = float(row["grad_riemann_norm_1_per_m3"])
        drift = c_fermi * domain_length * riemann + c_fermi2 * domain_length**2 * grad_riemann
        epsilon_comm_fermi = c_pair * norm_product * drift
        gamma_bound = epsilon_comm_fermi
        beta_bound = epsilon_comm_fermi
        newton_bound = epsilon_comm_fermi
        pass_gamma = gamma_bound <= TOL_GAMMA_SMOKE
        pass_beta = beta_bound <= TOL_BETA_SMOKE
        pass_newton = newton_bound <= TOL_NEWTON_SMOKE
        smallest_tol = min(TOL_GAMMA_SMOKE, TOL_BETA_SMOKE, TOL_NEWTON_SMOKE)
        hidden_gain_to_fail = smallest_tol / epsilon_comm_fermi if epsilon_comm_fermi > 0 else math.inf
        rows.append({
            **base(timestamp),
            "result_id": row["scenario_id"].replace("SC", "RES"),
            "scenario_id": row["scenario_id"],
            "epsilon_comm_Fermi": f"{epsilon_comm_fermi:.12e}",
            "gamma_residual_smoke": f"{gamma_bound:.12e}",
            "beta_residual_smoke": f"{beta_bound:.12e}",
            "newton_residual_smoke": f"{newton_bound:.12e}",
            "pass_gamma_smoke": pass_gamma,
            "pass_beta_smoke": pass_beta,
            "pass_newton_smoke": pass_newton,
            "numeric_smoke_pass": pass_gamma and pass_beta and pass_newton,
            "hidden_operator_gain_to_fail_min_tol": f"{hidden_gain_to_fail:.12e}",
            "interpretation": "scale_not_obviously_fatal_nonclaim" if pass_gamma and pass_beta and pass_newton else "scale_fails_even_as_smoke",
            "claim_allowed": False,
        })
    return rows


def caveat_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("CAV3749_0_operator_norms", "operator constants and norm products are set to one", "real C_pair, C_gamma_S, C_beta_S, E_M norms could change the result", "must source/bound operator norms"),
        ("CAV3749_1_projector_origin", "parallel parent projector still unsigned", "small Fermi drift does not prove P_M is a valid parent object", "must derive parent bundle split or keep closure label"),
        ("CAV3749_2_curvature_model", "Schwarzschild curvature scale is a proxy", "real lab/Solar metric environment needs sourced domain and multipole profile", "replace smoke constants with source rows"),
        ("CAV3749_3_no_claim", "all numeric rows are nonclaim", "passing smoke only means not obviously impossible at scale", "do not promote local GR/PPN pass"),
    ]
    return [
        {
            **base(timestamp),
            "caveat_id": caveat_id,
            "caveat": caveat,
            "effect": effect,
            "required_next_action": next_action,
            "claim_allowed": False,
        }
        for caveat_id, caveat, effect, next_action in specs
    ]


def decision_rows(timestamp: str, results: list[dict[str, object]]) -> list[dict[str, object]]:
    all_pass = all(row["numeric_smoke_pass"] is True for row in results)
    min_gain = min(float(row["hidden_operator_gain_to_fail_min_tol"]) for row in results)
    specs = [
        ("DEC3749_0_scale_result", "FERMI_PROJECTOR_DRIFT_NOT_OBVIOUSLY_FATAL_IN_SMOKE", f"all scenarios pass smoke tolerances={all_pass}; smallest hidden-operator gain-to-fail is {min_gain:.3e}"),
        ("DEC3749_1_no_claim", "NO_LOCAL_GR_CLAIM", "the smoke uses proxy constants and unit operator norms, so it cannot prove PPN safety"),
        ("DEC3749_2_best_next", "SOURCE_OPERATOR_NORMS_OR_PARENT_PARALLEL_SPLIT", "the next real discriminator is either C/operator norm acquisition or parent proof of A_ML=0"),
    ]
    return [
        {
            **base(timestamp),
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "claim_allowed": False,
        }
        for decision_id, decision, rationale in specs
    ]


def claim_gate_rows(timestamp: str, results: list[dict[str, object]]) -> list[dict[str, object]]:
    all_pass = all(row["numeric_smoke_pass"] is True for row in results)
    specs = [
        ("CG3749_0_sources", "3749 source handoff complete", True, "local source handoff rows and anchors found"),
        ("CG3749_1_smoke_inputs", "smoke constants and scenarios emitted", True, "constants and curvature scenarios written"),
        ("CG3749_2_smoke_runner", "Fermi drift smoke runner executed", True, "epsilon_comm_Fermi computed for all scenarios"),
        ("CG3749_3_smoke_pass", "all nominal smoke scenarios pass placeholder tolerances", all_pass, "scale check is not obviously fatal under unit operator norms"),
        ("CG3749_4_source_values", "all constants/operators/tolerances are claim-source-backed", False, "operator norms and official claim tolerances are not sourced here"),
        ("CG3749_5_parent_projector", "parent parallel projector is derived", False, "3748 parent split remains ansatz only"),
        ("CG3749_6_local_claim", "local GR/Newton/PPN pass claim allowed", False, "nonclaim smoke only"),
    ]
    return [
        {
            **base(timestamp),
            "gate_id": gate_id,
            "gate": gate,
            "passed": passed,
            "rationale": rationale,
            "claim_allowed": False,
        }
        for gate_id, gate, passed, rationale in specs
    ]


def status_rows(timestamp: str, all_pass: bool) -> list[dict[str, object]]:
    return [{
        **base(timestamp),
        "status_id": "STATUS3749_0",
        "status": "FERMI_PROJECTOR_LEAK_NUMERIC_SMOKE_PASSES_NONCLAIM" if all_pass else "FERMI_PROJECTOR_LEAK_NUMERIC_SMOKE_FAILS_NONCLAIM",
        "summary": "3749 instantiates nonclaim Solar/Earth Fermi-domain projector leak scales. Under unit hidden operator norms, epsilon_comm_Fermi is far below placeholder local tolerances, but parent projector and operator constants remain unsourced.",
        "claim_allowed": False,
    }]


def next_target_rows(timestamp: str) -> list[dict[str, object]]:
    return [{
        **base(timestamp),
        "next_id": "NEXT3749_0",
        "target_doc": "3750-Y5-R2FR-operator-norm-source-or-parent-parallel-split-proof.md",
        "target_script": "scripts/Y5_R2FR_3750_operator_norm_source_or_parent_parallel_split_proof.py",
        "objective": "either source/bound the hidden operator norm product in epsilon_comm_Fermi, or attempt the stronger parent proof A_ML=0 for the structural parallel split",
        "success_gate": "the smoke margin becomes a real bound with sourced operator constants, or the projector leak is theorem-zero by parent geometry",
        "claim_allowed": False,
    }]


def write_doc(paths: dict[str, Path], grouped: dict[str, list[dict[str, object]]]) -> None:
    lines = [
        "# 3749 - Local Fermi-Domain Projector Leak Numeric Smoke",
        "",
        "## Status",
        f"- `{grouped['status'][0]['status']}`",
        "- This is a scale smoke test only: all rows stay nonclaim.",
        "- Under unit hidden operator norms, the Fermi-domain curvature projector drift is tiny in the tested Earth/Solar domains.",
        "",
        "## Formula",
        "- `epsilon_comm_Fermi = C_pair * ||E_M^nabla|| * (C_Fermi L_D ||Riemann|| + C_Fermi2 L_D^2 ||nabla Riemann||) * ||deltaPhi_L||`.",
        "- Curvature proxy: `||Riemann|| ~ sqrt(48) G M / (c^2 r^3)`, `||nabla Riemann|| ~ 3 ||Riemann|| / r`.",
        "",
        "## Smoke Results",
    ]
    for row in grouped["results"]:
        lines.append(f"- `{row['result_id']}` `{row['interpretation']}`: epsilon={row['epsilon_comm_Fermi']} gain_to_fail={row['hidden_operator_gain_to_fail_min_tol']} claim_allowed={row['claim_allowed']}")
    lines.extend(["", "## Caveats"])
    for row in grouped["caveats"]:
        lines.append(f"- `{row['caveat_id']}`: {row['caveat']} | {row['required_next_action']}")
    lines.extend(["", "## Decisions"])
    for row in grouped["decisions"]:
        lines.append(f"- `{row['decision_id']}` `{row['decision']}` | {row['rationale']}")
    lines.extend(["", "## Claim Gates"])
    for row in grouped["claim_gates"]:
        lines.append(f"- `{row['gate_id']}` passed={row['passed']} claim_allowed={row['claim_allowed']} | {row['gate']}: {row['rationale']}")
    lines.extend(["", "## Next Target"])
    next_row = grouped["next_target"][0]
    lines.append(f"- `{next_row['target_doc']}`")
    lines.append(f"- Objective: {next_row['objective']}")
    paths["doc"].write_text("\n".join(lines) + "\n", encoding="utf-8")


def validation_rows(timestamp: str, paths: dict[str, Path]) -> list[dict[str, object]]:
    sources = parse_csv(paths["source_register"])
    constants = parse_csv(paths["constants"])
    inputs = parse_csv(paths["inputs"])
    results = parse_csv(paths["results"])
    caveats = parse_csv(paths["caveats"])
    claim_gates = parse_csv(paths["claim_gates"])
    next_target = parse_csv(paths["next_target"])
    validation_paths = [path for key, path in paths.items() if key != "validation"]
    formalization_leaks = []
    if FORMALIZATION.exists():
        formalization_leaks = list(FORMALIZATION.rglob("*3749*"))
    checks = [
        ("sources_exist", "all source paths exist", all(row["exists"] == "True" for row in sources)),
        ("needles_found", "all source needles found", all(row["needle_found"] == "True" for row in sources)),
        ("outputs_exist", "all outputs exist", all(path.exists() for path in validation_paths)),
        ("csv_parse", "all generated CSVs parse", all(len(parse_csv(path)) > 0 for key, path in paths.items() if key not in {"doc", "validation"})),
        ("constants_complete", "smoke constants emitted", len(constants) == 10 and all(row["claim_allowed"] == "False" for row in constants)),
        ("inputs_complete", "seven Earth/Solar scenarios emitted", len(inputs) == 7 and all(row["claim_allowed"] == "False" for row in inputs)),
        ("results_complete", "seven smoke results emitted", len(results) == 7 and all(row["claim_allowed"] == "False" for row in results)),
        ("results_pass_smoke", "all scenarios pass smoke tolerance", all(row["numeric_smoke_pass"] == "True" for row in results)),
        ("caveats_nonclaim", "caveats block promotion", len(caveats) == 4 and "operator constants" in read_text(paths["caveats"])),
        ("claim_gates_block", "local claim gate remains blocked", any(row["gate_id"] == "CG3749_6_local_claim" and row["passed"] == "False" for row in claim_gates)),
        ("claim_allowed_false", "all gate rows keep claim_allowed false", all(row["claim_allowed"] == "False" for row in claim_gates)),
        ("doc_core_terms", "doc records smoke formula and caveats", all(token in read_text(paths["doc"]) for token in ["epsilon_comm_Fermi", "scale smoke test only", "operator constants"])),
        ("next_target_3750", "next target sources operator norms or parent split", next_target[0]["target_doc"] == "3750-Y5-R2FR-operator-norm-source-or-parent-parallel-split-proof.md"),
        ("no_formalization_leak", "no 3749 files in formalization-workbench", len(formalization_leaks) == 0),
    ]
    return [
        {
            **base(timestamp),
            "validation_id": validation_id,
            "description": description,
            "result": "PASS" if result else "FAIL",
            "details": "",
        }
        for validation_id, description, result in checks
    ]


def main() -> None:
    timestamp = stamp()
    paths = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3749_SOURCE_REGISTER.csv",
        "constants": RESIDUALS / "P8_Y5_R2FR_3749_SMOKE_CONSTANTS.csv",
        "inputs": RESIDUALS / "P8_Y5_R2FR_3749_FERMI_DOMAIN_INPUTS.csv",
        "results": RESIDUALS / "P8_Y5_R2FR_3749_FERMI_DOMAIN_RESULTS.csv",
        "caveats": RESIDUALS / "P8_Y5_R2FR_3749_NONCLAIM_CAVEATS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3749_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3749_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3749_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3749_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3749_VALIDATION.csv",
        "doc": DOC,
    }
    inputs = scenario_input_rows(timestamp)
    results = smoke_result_rows(timestamp, inputs)
    all_pass = all(row["numeric_smoke_pass"] is True for row in results)
    grouped = {
        "source_register": source_register(timestamp),
        "constants": constants_rows(timestamp),
        "inputs": inputs,
        "results": results,
        "caveats": caveat_rows(timestamp),
        "decisions": decision_rows(timestamp, results),
        "claim_gates": claim_gate_rows(timestamp, results),
        "status": status_rows(timestamp, all_pass),
        "next_target": next_target_rows(timestamp),
    }
    for key, rows in grouped.items():
        write_csv(paths[key], rows)
    write_doc(paths, grouped)
    write_csv(paths["validation"], validation_rows(timestamp, paths))
    failures = [row for row in parse_csv(paths["validation"]) if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3749 validation failed: {failures}")
    print("wrote 3749 checkpoint: Fermi-domain projector leak numeric smoke passed nonclaim")


if __name__ == "__main__":
    main()

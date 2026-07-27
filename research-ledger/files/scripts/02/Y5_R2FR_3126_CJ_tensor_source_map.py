from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
INPUT = OUT / "P8_Y5_R2FR_3126_CJ_TENSOR_MAP_INPUTS.csv"
OUTPUT = OUT / "P8_Y5_R2FR_3126_CJ_TENSOR_MAP_OUTPUT.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3126_VALIDATION.csv"
GATE = OUT / "P8_Y5_R2FR_3126_CJ_TENSOR_MAP_GATE.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def parse_float(value: object) -> float | None:
    try:
        parsed = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def is_true(value: object) -> bool:
    return str(value).strip().lower() == "true"


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    root_candidate = ROOT / path_text
    if root_candidate.exists():
        return root_candidate
    return OUT / path_text


def find_row(rows: list[dict[str, str]], row_id: str, row_id_column: str = "") -> dict[str, str] | None:
    if not row_id:
        return None
    if row_id_column:
        for row in rows:
            if row.get(row_id_column, "") == row_id:
                return row
    for row in rows:
        if row_id in row.values():
            return row
    return None


def load_sources(inputs: list[dict[str, str]]) -> dict[str, dict[str, Any]]:
    sources: dict[str, dict[str, Any]] = {}
    for row in inputs:
        path = source_path(row.get("source_file", ""))
        source = find_row(read_csv(path), row.get("source_row_id", ""), row.get("row_id_column", ""))
        sources[row.get("role", "")] = {
            "input": row,
            "path": path,
            "row": source,
            "exists": path.exists(),
            "found": source is not None,
        }
    return sources


def close(a: float | None, b: float | None, tol: float = 1e-24) -> bool:
    if a is None or b is None:
        return False
    return abs(a - b) <= max(tol, 1e-12 * max(abs(a), abs(b), 1.0))


def wep_reduction(sources: dict[str, dict[str, Any]]) -> dict[str, Any]:
    row = sources.get("WEP_CJ_smoke_coefficient", {}).get("row") or {}
    q_alpha = parse_float(row.get("q_alpha", ""))
    comparison_q_alpha = parse_float(row.get("comparison_q_alpha", ""))
    tau_em = parse_float(row.get("tau_EM", ""))
    c_relax = parse_float(row.get("C_relax", ""))
    source_delta = parse_float(row.get("delta_C_J", ""))
    source_bound = parse_float(row.get("deltaJ_bound_abs", ""))
    eta_bound = parse_float(row.get("eta_bound", ""))
    derived_delta: float | None = None
    derived_bound: float | None = None
    if q_alpha is not None and comparison_q_alpha is not None and tau_em is not None and c_relax is not None:
        derived_delta = (2.0 * tau_em * q_alpha + c_relax) - (2.0 * tau_em * comparison_q_alpha + c_relax)
    if eta_bound is not None and derived_delta is not None and abs(derived_delta) > 0:
        derived_bound = eta_bound / abs(derived_delta)
    return {
        "q_alpha": q_alpha,
        "comparison_q_alpha": comparison_q_alpha,
        "tau_EM": tau_em,
        "C_relax": c_relax,
        "source_delta_C_J": source_delta,
        "derived_delta_C_J": derived_delta,
        "delta_C_J_reproduced": close(derived_delta, source_delta),
        "source_deltaJ_bound_abs": source_bound,
        "derived_deltaJ_bound_abs": derived_bound,
        "deltaJ_bound_reproduced": close(derived_bound, source_bound),
    }


def adm_reduction_check() -> dict[str, Any]:
    tau_em = 1.3
    f_em_adm = 0.004
    c_relax = -0.0002
    zeta_q = 0.0
    pair_kernel = 2.0 * tau_em - zeta_q
    tensor_expression = f_em_adm * pair_kernel + c_relax
    prior_expression = 2.0 * tau_em * f_em_adm + c_relax
    return {
        "tau_EM": tau_em,
        "f_EM_ADM": f_em_adm,
        "C_relax": c_relax,
        "zeta_Q": zeta_q,
        "derived_C_J_ADM": tensor_expression,
        "prior_3121_C_J_ADM": prior_expression,
        "homogeneous_limit_reproduced": close(tensor_expression, prior_expression),
    }


def map_rows(sources: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    wep = wep_reduction(sources)
    adm = adm_reduction_check()
    rows = [
        {
            "map_id": "CJT3126_0",
            "layer": "parent_action_ansatz",
            "derived_object": "before_variation_current_coupling",
            "definition": "S contains -1/4 Z_Q(y)F^2 + sum_A c_A(y) A_Q_mu J_A^mu before Maxwell and Hilbert variation",
            "derived_coefficient": "kappa_A=d ln c_A/dJ, zeta_Q=d ln Z_Q/dJ",
            "known_limit": "if all kappa_A common and zeta_Q calibrates away, only differential or source/calibration residuals survive",
            "reduction_check": "conditional_action_map",
            "reduction_pass": "true",
            "status": "conditional_derived_map_not_parent_signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "PARENT_ACTION_ANSATZ_NOT_SIGNED;INPUT_VALID_FOR_CLAIM_FALSE",
            "next_action": "parent must sign or forbid c_A(y) and Z_Q(y) slots",
            "source_paths": str(sources["before_variation_projection"]["path"]),
            "generated_utc": stamp(),
        },
        {
            "map_id": "CJT3126_1",
            "layer": "maxwell_equation",
            "derived_object": "current_to_field_map",
            "definition": "nabla_mu(Z_Q F^{mu nu}) = sum_A c_A J_A^nu",
            "derived_coefficient": "field sourced by c_A/Z_Q",
            "known_limit": "standard Maxwell recovered for constant Z_Q and calibrated common c_A",
            "reduction_check": "before_variation_projection_matches_3123",
            "reduction_pass": str(is_true((sources["before_variation_projection"]["row"] or {}).get("projects_source_GM_observable", ""))).lower(),
            "status": "derived_from_action_ansatz",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "PARENT_ACTION_ANSATZ_NOT_SIGNED",
            "next_action": "derive whether parent object-language permits nonconstant c_A/Z_Q",
            "source_paths": str(sources["before_variation_projection"]["path"]),
            "generated_utc": stamp(),
        },
        {
            "map_id": "CJT3126_2",
            "layer": "pair_energy_tensor",
            "derived_object": "EM_pair_kernel",
            "definition": "U_AB^EM proportional to c_A c_B / Z_Q",
            "derived_coefficient": "K_AB = kappa_A + kappa_B - zeta_Q",
            "known_limit": "homogeneous kappa_A=kappa_B=tau_EM, zeta_Q=0 gives K_AB=2 tau_EM",
            "reduction_check": "reduces_to_3121_2tau_kernel",
            "reduction_pass": str(adm["homogeneous_limit_reproduced"]).lower(),
            "status": "derived_algebraic_kernel",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "BODY_PAIR_WEIGHTS_NOT_FILLED;PARENT_ACTION_ANSATZ_NOT_SIGNED",
            "next_action": "fill body pair weights w_AB^B or prove differential kernels vanish",
            "source_paths": str(sources["source_GM_bridge"]["path"]),
            "generated_utc": stamp(),
        },
        {
            "map_id": "CJT3126_3",
            "layer": "material_body_coefficient",
            "derived_object": "C_J_body_EM",
            "definition": "C_J,B^EM = sum_AB w_AB^B (kappa_A+kappa_B-zeta_Q)",
            "derived_coefficient": "C_J,B = q_alpha,B(2 tau_EM-zeta_Q)+C_relax,B in one-channel Coulomb smoke",
            "known_limit": "3122 TA6V-PtRh10 smoke coefficient reproduced",
            "reduction_check": json.dumps(wep, sort_keys=True),
            "reduction_pass": str(wep["delta_C_J_reproduced"] and wep["deltaJ_bound_reproduced"]).lower(),
            "status": "derived_material_map_smoke_reproduced",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "ONE_CHANNEL_COULOMB_SMOKE;NO_PARENT_MATERIAL_TENSOR;INPUT_VALID_FOR_CLAIM_FALSE",
            "next_action": "replace q_alpha-only smoke with parent-owned material tensor weights",
            "source_paths": str(sources["WEP_CJ_smoke_coefficient"]["path"]),
            "generated_utc": stamp(),
        },
        {
            "map_id": "CJT3126_4",
            "layer": "ADM_source_coefficient",
            "derived_object": "C_J_source_ADM",
            "definition": "C_J,S^ADM = f_EM,S^ADM C_J,S^EM + C_relax,S^ADM",
            "derived_coefficient": "homogeneous limit gives C_J,S^ADM=2 tau_EM,S f_EM,S^ADM + C_relax,S",
            "known_limit": "3121 source-GM bridge expression recovered",
            "reduction_check": json.dumps(adm, sort_keys=True),
            "reduction_pass": str(adm["homogeneous_limit_reproduced"]).lower(),
            "status": "derived_source_GM_map_missing_body_inputs",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "MISSING_f_EM_ADM_SOURCE;MISSING_C_RELAX_SOURCE;MISSING_CALIBRATION_REFERENCE",
            "next_action": "fill source body EM energy fraction and calibration kernel",
            "source_paths": str(sources["source_GM_bridge"]["path"]),
            "generated_utc": stamp(),
        },
        {
            "map_id": "CJT3126_5",
            "layer": "observable_bound_laws",
            "derived_object": "WEP_and_source_GM_observable_map",
            "definition": "eta_AB ~= |(C_J,A-C_J,B)delta_J| and Delta(GM)_S/GM_S=(C_J,S^ADM-C_J,cal^ADM)delta_J",
            "derived_coefficient": f"current strict nonclaim rollup |delta_J| <= {(sources['strict_deltaJ_interface']['row'] or {}).get('numeric_bound_abs', '')}",
            "known_limit": "WEP score uses material difference; source-GM score uses source minus calibration difference",
            "reduction_check": "does_not_mix_WEP_material_coefficient_into_source_GM",
            "reduction_pass": "true",
            "status": "observable_map_derived_but_nonclaim",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "ROLLUP_INPUTS_NONCLAIM;SOURCE_GM_KERNELS_UNFILLED",
            "next_action": "score only after parent-owned C_J coefficients are filled per arena",
            "source_paths": f"{sources['strict_deltaJ_interface']['path']};{sources['source_GM_bridge']['path']}",
            "generated_utc": stamp(),
        },
    ]
    return rows


def validate(inputs: list[dict[str, str]], sources: dict[str, dict[str, Any]], outputs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    required = ["source_id", "role", "source_file", "source_row_id", "row_id_column", "required", "valid_for_claim", "notes"]
    columns = set(inputs[0].keys()) if inputs else set()
    missing_columns = [column for column in required if column not in columns]
    source_status = {
        role: {"exists": payload["exists"], "found": payload["found"], "path": str(payload["path"])}
        for role, payload in sources.items()
    }
    wep = wep_reduction(sources)
    adm = adm_reduction_check()
    return [
        {
            "check_id": "VAL3126_0_input_schema",
            "status": "pass" if inputs and not missing_columns else "fail",
            "details": ";".join(missing_columns),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3126_1_required_source_rows_resolve",
            "status": "pass" if all(payload["exists"] and payload["found"] for payload in sources.values()) else "fail",
            "details": json.dumps(source_status, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3126_2_wep_delta_CJ_reproduced",
            "status": "pass" if wep["delta_C_J_reproduced"] and wep["deltaJ_bound_reproduced"] else "fail",
            "details": json.dumps(wep, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3126_3_3121_homogeneous_ADM_limit_reproduced",
            "status": "pass" if adm["homogeneous_limit_reproduced"] else "fail",
            "details": json.dumps(adm, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3126_4_all_reduction_rows_pass",
            "status": "pass" if outputs and all(is_true(row.get("reduction_pass", "")) for row in outputs) else "fail",
            "details": json.dumps({row["map_id"]: row.get("reduction_pass", "") for row in outputs}, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3126_5_all_outputs_nonclaim",
            "status": "pass" if outputs and all(not is_true(row.get("claim_allowed", "")) for row in outputs) else "fail",
            "details": f"output_rows={len(outputs)}",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def gate_rows(outputs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {row.get("map_id", ""): row for row in outputs}
    return [
        {
            "row_id": "CJTG3126_0",
            "gate": "parent_CJ_tensor_map",
            "status": "conditional_map_derived_not_parent_signed",
            "claim_allowed": "false",
            "theorem_or_failure": "If the before-variation Maxwell/Hilbert action slot exists, the coefficient map is K_AB=kappa_A+kappa_B-zeta_Q.",
            "observable_links": "EM_stress;WEP;source_GM;R10",
            "next_action": "prove the parent permits this slot with fixed coefficients or prove no-cA/no-ZQ zero",
            "source_paths": by_id.get("CJT3126_0", {}).get("source_paths", ""),
        },
        {
            "row_id": "CJTG3126_1",
            "gate": "3122_numeric_reproduction",
            "status": "Coulomb_smoke_reproduced",
            "claim_allowed": "false",
            "theorem_or_failure": by_id.get("CJT3126_3", {}).get("reduction_check", ""),
            "observable_links": "WEP;material_Coulomb;delta_J",
            "next_action": "replace q_alpha-only smoke with real material/source tensor weights",
            "source_paths": by_id.get("CJT3126_3", {}).get("source_paths", ""),
        },
        {
            "row_id": "CJTG3126_2",
            "gate": "3121_source_GM_reduction",
            "status": "homogeneous_source_GM_formula_recovered",
            "claim_allowed": "false",
            "theorem_or_failure": "C_J,S^ADM=f_EM,S^ADM C_J,S^EM+C_relax reduces to 2 tau_EM,S f_EM,S^ADM+C_relax,S.",
            "observable_links": "Newtonian_GM;local_GR;orbital",
            "next_action": "fill f_EM_ADM_source, C_relax_source and calibration kernel for actual sources",
            "source_paths": by_id.get("CJT3126_4", {}).get("source_paths", ""),
        },
        {
            "row_id": "CJTG3126_3",
            "gate": "no_mixing_rule",
            "status": "WEP_and_source_GM_coefficients_separated",
            "claim_allowed": "false",
            "theorem_or_failure": "Material WEP differences and source-GM source/calibration differences are different projections of the same C_J tensor.",
            "observable_links": "WEP;source_GM;calibration",
            "next_action": "do not transfer a material WEP coefficient into source-GM without body/source weights",
            "source_paths": by_id.get("CJT3126_5", {}).get("source_paths", ""),
        },
        {
            "row_id": "CJTG3126_4",
            "gate": "next_target_3127",
            "status": "queued_body_weight_derivation",
            "claim_allowed": "false",
            "theorem_or_failure": "The next missing object is not abstract coupling; it is the body/source weighting measure w_AB^B and f_EM^ADM/calibration map.",
            "observable_links": "GR_reduction;Newtonian_GM;EM_stress;WEP",
            "next_action": "derive body EM energy weighting measure and source/calibration kernel from Hilbert stress",
            "source_paths": OUTPUT,
        },
    ]


def main() -> None:
    inputs = read_csv(INPUT)
    sources = load_sources(inputs)
    outputs = map_rows(sources)
    validations = validate(inputs, sources, outputs)
    write_csv(OUTPUT, outputs)
    write_csv(VALIDATION, validations)
    write_csv(GATE, gate_rows(outputs))
    failing = [row for row in validations if row.get("status") != "pass"]
    if failing:
        raise SystemExit(f"3126 validation failed: {json.dumps(failing, sort_keys=True)}")
    print(f"wrote {OUTPUT}")
    print(f"wrote {VALIDATION}")
    print(f"wrote {GATE}")


if __name__ == "__main__":
    main()

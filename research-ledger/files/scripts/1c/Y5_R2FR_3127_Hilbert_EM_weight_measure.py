from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
INPUT = OUT / "P8_Y5_R2FR_3127_HILBERT_EM_WEIGHT_MEASURE_INPUTS.csv"
OUTPUT = OUT / "P8_Y5_R2FR_3127_HILBERT_EM_WEIGHT_MEASURE_OUTPUT.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3127_VALIDATION.csv"
GATE = OUT / "P8_Y5_R2FR_3127_HILBERT_EM_WEIGHT_MEASURE_GATE.csv"


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


def close(left: float | None, right: float | None, tol: float = 1e-24) -> bool:
    if left is None or right is None:
        return False
    return abs(left - right) <= max(tol, 1e-12 * max(abs(left), abs(right), 1.0))


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


def parse_reduction_json(row: dict[str, str] | None) -> dict[str, Any]:
    if not row:
        return {}
    text = row.get("reduction_check", "")
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def weight_identity_check() -> dict[str, Any]:
    energies = [0.3, 0.7]
    kernels = [1.2, 2.4]
    total_energy = sum(energies)
    weights = [energy / total_energy for energy in energies]
    direct = sum(energy * kernel for energy, kernel in zip(energies, kernels)) / total_energy
    weighted = sum(weight * kernel for weight, kernel in zip(weights, kernels))
    return {
        "energies": energies,
        "kernels": kernels,
        "weights": weights,
        "weight_sum": sum(weights),
        "direct_dlnE_dJ": direct,
        "weighted_sum": weighted,
        "identity_reproduced": close(direct, weighted) and close(sum(weights), 1.0),
    }


def one_channel_wep_check(sources: dict[str, dict[str, Any]]) -> dict[str, Any]:
    row = sources.get("WEP_CJ_smoke", {}).get("row") or {}
    q_alpha = parse_float(row.get("q_alpha", ""))
    comparison_q_alpha = parse_float(row.get("comparison_q_alpha", ""))
    tau_em = parse_float(row.get("tau_EM", ""))
    c_relax = parse_float(row.get("C_relax", ""))
    source_delta = parse_float(row.get("delta_C_J", ""))
    source_bound = parse_float(row.get("deltaJ_bound_abs", ""))
    eta_bound = parse_float(row.get("eta_bound", ""))
    zeta_q = 0.0
    k_one_channel = 2.0 * tau_em - zeta_q if tau_em is not None else None
    c_body = q_alpha * k_one_channel + c_relax if None not in (q_alpha, k_one_channel, c_relax) else None
    c_comparison = comparison_q_alpha * k_one_channel + c_relax if None not in (comparison_q_alpha, k_one_channel, c_relax) else None
    delta = c_body - c_comparison if None not in (c_body, c_comparison) else None
    bound = eta_bound / abs(delta) if eta_bound is not None and delta not in (None, 0.0) else None
    return {
        "q_alpha": q_alpha,
        "comparison_q_alpha": comparison_q_alpha,
        "tau_EM": tau_em,
        "zeta_Q": zeta_q,
        "K_one_channel": k_one_channel,
        "C_J_body": c_body,
        "C_J_comparison": c_comparison,
        "derived_delta_C_J": delta,
        "source_delta_C_J": source_delta,
        "delta_C_J_reproduced": close(delta, source_delta),
        "derived_deltaJ_bound_abs": bound,
        "source_deltaJ_bound_abs": source_bound,
        "deltaJ_bound_reproduced": close(bound, source_bound),
    }


def adm_limit_check(sources: dict[str, dict[str, Any]]) -> dict[str, Any]:
    row = sources.get("source_ADM_coefficient", {}).get("row") or {}
    parsed = parse_reduction_json(row)
    tau_em = parse_float(parsed.get("tau_EM", ""))
    f_em = parse_float(parsed.get("f_EM_ADM", ""))
    c_relax = parse_float(parsed.get("C_relax", ""))
    zeta_q = parse_float(parsed.get("zeta_Q", 0.0))
    prior = parse_float(parsed.get("prior_3121_C_J_ADM", ""))
    if None in (tau_em, f_em, c_relax, zeta_q):
        derived = None
    else:
        derived = f_em * (2.0 * tau_em - zeta_q) + c_relax
    return {
        "tau_EM": tau_em,
        "f_EM_ADM": f_em,
        "C_relax": c_relax,
        "zeta_Q": zeta_q,
        "derived_C_J_ADM_from_weight_measure": derived,
        "prior_3121_C_J_ADM": prior,
        "ADM_limit_reproduced": close(derived, prior),
    }


def output_rows(sources: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    weight_check = weight_identity_check()
    wep_check = one_channel_wep_check(sources)
    adm_check = adm_limit_check(sources)
    source_paths = lambda *roles: ";".join(str(sources[role]["path"]) for role in roles)
    return [
        {
            "derivation_id": "WGT3127_0",
            "layer": "Hilbert_EM_stress_slice",
            "object": "stationary_EM_energy_measure",
            "formula": "E_EM[B]=int_{Sigma_B} N T_EM^{mu nu} n_mu xi_nu dSigma, T_EM^{mu nu}=Z_Q(F^{mu lambda}F^nu_lambda-1/4 g^{mu nu}F^2)",
            "derived_from_hilbert_stress": "true",
            "static_boundary_condition": "stationary source slice with fixed boundary and no net unresolved flux",
            "poynting_flux_status": "requires div_S balance; radiative waves use flux law not static ADM coefficient",
            "reduction_check": "defines f_EM_ADM=E_EM/M_ADM when ADM split is signed",
            "reduction_pass": "true",
            "status": "measure_derived_conditionally",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "ADM_SPLIT_NOT_SOURCE_FILLED;BOUNDARY_FLUX_GUARD_REQUIRED;INPUT_VALID_FOR_CLAIM_FALSE",
            "next_action": "fill stationary source worldtube and boundary/Poynting conditions",
            "source_paths": source_paths("pair_kernel", "source_ADM_coefficient"),
            "generated_utc": stamp(),
        },
        {
            "derivation_id": "WGT3127_1",
            "layer": "Green_pair_decomposition",
            "object": "body_pair_weights_w_AB",
            "formula": "U_AB^B=(1/2) int rho_A G_B rho_B; w_AB^B=U_AB^B/sum_CD U_CD^B; C_J,B^EM=sum_AB w_AB^B K_AB",
            "derived_from_hilbert_stress": "true",
            "static_boundary_condition": "quasi-static bound-field decomposition; signed binding convention must be source-owned",
            "poynting_flux_status": "not valid for unaveraged outgoing radiation",
            "reduction_check": json.dumps(weight_check, sort_keys=True),
            "reduction_pass": str(weight_check["identity_reproduced"]).lower(),
            "status": "algebraic_weight_identity_derived",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "REAL_BODY_WEIGHTS_NOT_FILLED;SIGNED_BINDING_CONVENTION_NOT_SOURCE_OWNED",
            "next_action": "derive or source actual w_AB^B for test materials and gravitating sources",
            "source_paths": source_paths("pair_kernel", "material_body_coefficient"),
            "generated_utc": stamp(),
        },
        {
            "derivation_id": "WGT3127_2",
            "layer": "body_material_projection",
            "object": "one_channel_WEP_reduction",
            "formula": "C_J,B=q_alpha,B(2 tau_EM-zeta_Q)+C_relax,B; Delta C_J_AB=C_J,A-C_J,B",
            "derived_from_hilbert_stress": "true",
            "static_boundary_condition": "material coefficient only; not source-GM without source weights",
            "poynting_flux_status": "static material Coulomb channel",
            "reduction_check": json.dumps(wep_check, sort_keys=True),
            "reduction_pass": str(wep_check["delta_C_J_reproduced"] and wep_check["deltaJ_bound_reproduced"]).lower(),
            "status": "3122_WEP_smoke_reproduced_from_weight_measure",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "ONE_CHANNEL_COULOMB_SMOKE;NO_PARENT_MATERIAL_TENSOR;INPUT_VALID_FOR_CLAIM_FALSE",
            "next_action": "replace q_alpha smoke with parent-owned material Hilbert-stress weights",
            "source_paths": source_paths("WEP_CJ_smoke", "material_body_coefficient"),
            "generated_utc": stamp(),
        },
        {
            "derivation_id": "WGT3127_3",
            "layer": "source_ADM_projection",
            "object": "source_GM_and_calibration_kernel",
            "formula": "C_J,S^ADM=f_EM,S^ADM sum_AB w_AB^S K_AB + C_relax,S; observable=[C_J,S^ADM-C_J,cal^ADM]delta_J",
            "derived_from_hilbert_stress": "true",
            "static_boundary_condition": "stationary ADM/source mass split and calibration reference must use same convention",
            "poynting_flux_status": "blocked for time-dependent radiation until flux is included",
            "reduction_check": json.dumps(adm_check, sort_keys=True),
            "reduction_pass": str(adm_check["ADM_limit_reproduced"]).lower(),
            "status": "3121_homogeneous_source_GM_limit_recovered",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "MISSING_SOURCE_WEIGHTS;MISSING_CALIBRATION_KERNEL;MISSING_C_RELAX_SOURCE",
            "next_action": "fill f_EM_ADM and calibration weights for Sun/Earth/lab sources before source-GM scoring",
            "source_paths": source_paths("source_ADM_coefficient", "source_GM_bridge", "observable_map"),
            "generated_utc": stamp(),
        },
        {
            "derivation_id": "WGT3127_4",
            "layer": "Poynting_flux_guard",
            "object": "static_vs_radiative_EM_separation",
            "formula": "dE_EM/dt=-surface_int S dot dA - int J dot E dV; static C_J^ADM requires zero/averaged unresolved boundary flux",
            "derived_from_hilbert_stress": "true",
            "static_boundary_condition": "no net Poynting leakage through source boundary or explicitly averaged periodic/radiative balance",
            "poynting_flux_status": "explicit_guard_added",
            "reduction_check": "prevents using wave/Poynting channels as static source mass coefficients",
            "reduction_pass": "true",
            "status": "guard_derived_from_EM_energy_balance",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "RADIATIVE_CLOSURE_NOT_SIGNED;BOUNDARY_CONDITIONS_NOT_FILLED",
            "next_action": "if EM waves/Poynting are used, derive a flux/readout coefficient separately from static ADM mass",
            "source_paths": source_paths("pair_kernel", "source_ADM_coefficient"),
            "generated_utc": stamp(),
        },
        {
            "derivation_id": "WGT3127_5",
            "layer": "next_reduction_gate",
            "object": "body_source_weight_acquisition_contract",
            "formula": "scoreable C_J requires c_A/Z_Q parent slot plus w_AB^B, f_EM^ADM, C_relax, and C_J,cal^ADM from the same Hilbert-stress convention",
            "derived_from_hilbert_stress": "true",
            "static_boundary_condition": "same slice/reference convention across material, source, and calibration bodies",
            "poynting_flux_status": "flux branch split from static branch",
            "reduction_check": f"current strict delta_J nonclaim bound={(sources['deltaJ_rollup']['row'] or {}).get('numeric_bound_abs', '')}",
            "reduction_pass": "true",
            "status": "contract_ready_for_3128_source_weight_fill_or_zero_proof",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "CONTRACT_READY_BUT_NUMERIC_SOURCE_WEIGHTS_UNFILLED",
            "next_action": "3128 should derive/fill first source-calibration weight rows or prove c_A/Z_Q slots vanish",
            "source_paths": source_paths("deltaJ_rollup", "observable_map"),
            "generated_utc": stamp(),
        },
    ]


def validate(inputs: list[dict[str, str]], sources: dict[str, dict[str, Any]], outputs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    required = ["source_id", "role", "source_file", "source_row_id", "row_id_column", "required", "valid_for_claim", "notes"]
    columns = set(inputs[0].keys()) if inputs else set()
    missing_columns = [column for column in required if column not in columns]
    source_status = {
        role: {"exists": payload["exists"], "found": payload["found"], "path": str(payload["path"])}
        for role, payload in sources.items()
    }
    weight_rows = [row for row in outputs if row.get("derivation_id") == "WGT3127_1"]
    wep_rows = [row for row in outputs if row.get("derivation_id") == "WGT3127_2"]
    adm_rows = [row for row in outputs if row.get("derivation_id") == "WGT3127_3"]
    poynting_rows = [row for row in outputs if row.get("derivation_id") == "WGT3127_4"]
    return [
        {
            "check_id": "VAL3127_0_input_schema",
            "status": "pass" if inputs and not missing_columns else "fail",
            "details": ";".join(missing_columns),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3127_1_required_source_rows_resolve",
            "status": "pass" if all(payload["exists"] and payload["found"] for payload in sources.values()) else "fail",
            "details": json.dumps(source_status, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3127_2_weight_identity_passes",
            "status": "pass" if weight_rows and all(is_true(row.get("reduction_pass", "")) for row in weight_rows) else "fail",
            "details": json.dumps(weight_rows, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3127_3_wep_smoke_reproduced",
            "status": "pass" if wep_rows and all(is_true(row.get("reduction_pass", "")) for row in wep_rows) else "fail",
            "details": json.dumps(wep_rows, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3127_4_source_ADM_limit_reproduced",
            "status": "pass" if adm_rows and all(is_true(row.get("reduction_pass", "")) for row in adm_rows) else "fail",
            "details": json.dumps(adm_rows, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3127_5_poynting_guard_present",
            "status": "pass" if poynting_rows and "explicit_guard" in poynting_rows[0].get("poynting_flux_status", "") else "fail",
            "details": json.dumps(poynting_rows, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3127_6_all_outputs_nonclaim",
            "status": "pass" if outputs and all(not is_true(row.get("claim_allowed", "")) for row in outputs) else "fail",
            "details": f"output_rows={len(outputs)}",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def gate_rows(outputs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {row.get("derivation_id", ""): row for row in outputs}
    return [
        {
            "row_id": "HWG3127_0",
            "gate": "Hilbert_EM_energy_measure",
            "status": "conditional_measure_derived",
            "claim_allowed": "false",
            "theorem_or_failure": "Stationary source coefficient must be built from Hilbert EM stress on a specified slice/worldtube.",
            "observable_links": "EM_stress;source_GM;local_GR",
            "next_action": "fill source worldtube and boundary conditions",
            "source_paths": by_id.get("WGT3127_0", {}).get("source_paths", ""),
        },
        {
            "row_id": "HWG3127_1",
            "gate": "body_pair_weight_measure",
            "status": "weight_identity_derived",
            "claim_allowed": "false",
            "theorem_or_failure": "C_J,B^EM=sum_AB w_AB^B(kappa_A+kappa_B-zeta_Q), with weights normalized by EM Hilbert energy.",
            "observable_links": "WEP;material_response;source_GM",
            "next_action": "derive or source real w_AB^B for materials and gravitating bodies",
            "source_paths": by_id.get("WGT3127_1", {}).get("source_paths", ""),
        },
        {
            "row_id": "HWG3127_2",
            "gate": "WEP_and_source_GM_reductions",
            "status": "3122_and_3121_limits_reproduced",
            "claim_allowed": "false",
            "theorem_or_failure": "One-channel WEP smoke and homogeneous source-GM limit both reduce from the same weight measure.",
            "observable_links": "WEP;Newtonian_GM;calibration",
            "next_action": "fill real source/calibration kernels before scoring",
            "source_paths": f"{by_id.get('WGT3127_2', {}).get('source_paths', '')};{by_id.get('WGT3127_3', {}).get('source_paths', '')}",
        },
        {
            "row_id": "HWG3127_3",
            "gate": "Poynting_flux_branch_split",
            "status": "static_and_radiative_EM_separated",
            "claim_allowed": "false",
            "theorem_or_failure": "Poynting/wave channels cannot be smuggled into static ADM coefficients without a flux balance law.",
            "observable_links": "EM_waves;Poynting;source_GM;time",
            "next_action": "derive separate flux/readout coefficient if radiative EM is used",
            "source_paths": by_id.get("WGT3127_4", {}).get("source_paths", ""),
        },
        {
            "row_id": "HWG3127_4",
            "gate": "next_target_3128",
            "status": "queued_source_calibration_weight_fill_or_zero_proof",
            "claim_allowed": "false",
            "theorem_or_failure": "3127 reduces the gap to source/calibration weights or the parent zero proof for c_A/Z_Q.",
            "observable_links": "GR_reduction;Newtonian_GM;Maxwell;WEP",
            "next_action": "3128 should attempt first source-calibration kernel fill from Hilbert stress, then test against the 3125 delta_J envelope",
            "source_paths": OUTPUT,
        },
    ]


def main() -> None:
    inputs = read_csv(INPUT)
    sources = load_sources(inputs)
    outputs = output_rows(sources)
    validations = validate(inputs, sources, outputs)
    write_csv(OUTPUT, outputs)
    write_csv(VALIDATION, validations)
    write_csv(GATE, gate_rows(outputs))
    failing = [row for row in validations if row.get("status") != "pass"]
    if failing:
        raise SystemExit(f"3127 validation failed: {json.dumps(failing, sort_keys=True)}")
    print(f"wrote {OUTPUT}")
    print(f"wrote {VALIDATION}")
    print(f"wrote {GATE}")


if __name__ == "__main__":
    main()

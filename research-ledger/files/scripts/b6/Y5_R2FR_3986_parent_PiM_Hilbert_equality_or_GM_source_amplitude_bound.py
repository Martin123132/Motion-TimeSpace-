from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3986"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3986-Y5-R2FR-parent-PiM-Hilbert-equality-or-GM-source-amplitude-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3986_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_3986_PIM_HILBERT_EQUALITY_REDUCTION_THEOREM.csv",
    "certificate": SRC / "P8_Y5_R2FR_3986_PIM_HILBERT_CERTIFICATE_UPDATE.csv",
    "amplitude": SRC / "P8_Y5_R2FR_3986_GM_SOURCE_AMPLITUDE_BOUND_ROWS.csv",
    "runner_schema": SRC / "P8_Y5_R2FR_3986_GM_AMPLITUDE_RUNNER_SCHEMA.csv",
    "runner_smoke": SRC / "P8_Y5_R2FR_3986_GM_AMPLITUDE_SMOKE_RESULTS.csv",
    "projector": SRC / "P8_Y5_R2FR_3986_PROJECTOR_RESULTS.csv",
    "feed": SRC / "P8_Y5_R2FR_3986_FEED_UPDATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3986_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3986_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3986_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3986_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3986_VALIDATION.csv",
}

NEXT_DOC = "3987-Y5-R2FR-universal-coupling-normalization-or-extra-monopole-charge-bound.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3987_universal_coupling_normalization_or_extra_monopole_charge_bound.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
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
        writer.writerows(rows)


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC3986_00_3985_next", SRC / "P8_Y5_R2FR_3985_NEXT_TARGET.csv", "NEXT3985_0", "3985 handoff"),
        ("SRC3986_01_3985_parent_pim", SRC / "P8_Y5_R2FR_3985_CLOSED_SOURCE_CERTIFICATE_UPDATE.csv", "SC3985_5_parent_PiM", "3985 PiM open target"),
        ("SRC3986_02_3985_gm", SRC / "P8_Y5_R2FR_3985_RESIDUAL_REDUCTION_ROWS.csv", "RR3985_5_GM_amplitude", "3985 GM amplitude residual"),
        ("SRC3986_03_3985_master", SRC / "P8_Y5_R2FR_3985_RESIDUAL_REDUCTION_ROWS.csv", "RR3985_0_master_reduced", "3985 reduced master residual"),
        ("SRC3986_04_3985_runner", SRC / "P8_Y5_R2FR_3985_NEWTONIAN_GM_BOUND_SMOKE_RESULTS.csv", "SMOKE3985_2_real_parent_rows_missing", "3985 bound runner blocker"),
        ("SRC3986_05_3985_projector", SRC / "P8_Y5_R2FR_3985_PROJECTOR_RESULTS.csv", "REAL3985_0_controlled_EH_monopole_l2m0_reduced_source_residual", "3985 controlled projector"),
        ("SRC3986_06_3985_theorem_shape", SRC / "P8_Y5_R2FR_3985_SUBFACTOR_CLOSURE_THEOREM.csv", "SC3985_3_Newton_shape", "Newtonian shape open amplitude"),
        ("SRC3986_07_3969_unique", SRC / "P8_Y5_R2FR_3969_SINGLE_EXTERIOR_MASS_UNIQUENESS_THEOREM.csv", "UQ3969_1_conditional_uniqueness_theorem", "one exterior mass charge"),
        ("SRC3986_08_3969_square", SRC / "P8_Y5_R2FR_3969_SINGLE_EXTERIOR_MASS_UNIQUENESS_THEOREM.csv", "UQ3969_2_square_law_corollary", "one-charge PPN readout"),
        ("SRC3986_09_worldtube_transfer", SRC / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv", "T510_2_MTS_transfer_condition", "MTS charge transfer"),
        ("SRC3986_10_worldtube_source", SRC / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv", "T510_1_worldtube_source_measure", "dressed source measure"),
        ("SRC3986_11_source_identity", SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv", "T509_0_charge_identity_needed", "source/Hilbert identity needed"),
        ("SRC3986_12_no_extra", SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv", "T509_2_no_extra_mass_channel", "extra mass channel"),
        ("SRC3986_13_parent_JH", SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv", "SM509_1_source_current", "parent source current"),
        ("SRC3986_14_parent_PiM", SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv", "SM509_2_parent_mass_projector", "parent PiM projector"),
        ("SRC3986_15_worldtube_measure", SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv", "SM509_4_worldtube_source_measure", "worldtube source measure"),
        ("SRC3986_16_gauss", SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv", "SM509_6_Gauss_orbital_calibration", "Gauss calibration"),
        ("SRC3986_17_HC4", SRC / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv", "HC4_charge_equals_PiM_Hilbert_mass", "Hamiltonian/Hilbert equality"),
        ("SRC3986_18_HC5", SRC / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv", "HC5_no_extra_hidden_charge", "extra hidden charge"),
        ("SRC3986_19_HC7", SRC / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv", "HC7_constant_universal_Geff", "constant universal Geff"),
        ("SRC3986_20_HC8", SRC / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv", "HC8_Poisson_Gauss_orbital_calibration", "orbital calibration"),
        ("SRC3986_21_TC3", SRC / "P8_TOPOLOGICAL_PIM_CLOSURE_CONDITIONS.csv", "TC500_3_Hilbert_equality", "topological Hilbert equality fail-open"),
        ("SRC3986_22_TC7", SRC / "P8_TOPOLOGICAL_PIM_CLOSURE_CONDITIONS.csv", "TC500_7_calibration", "calibration fail-open"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in source_specs():
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "needle": needle,
                "exists": exists,
                "needle_found": needle in text,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "PH3986_0_rank_one_charge_space",
            "claim_piece": "controlled EH scalar mass-charge direction",
            "mathematical_form": "Exterior[g_obs] in controlled stationary EH monopole branch has one scalar charge mu after fixed background/reference subtraction; any closed scalar stationary source charge coupled to this exterior has Q_proj = lambda_PiM_EH * Q_EH + Q_extra",
            "derived_result": "PiM/Hilbert equality reduces to a one-dimensional normalization and extra-charge problem, not an arbitrary projector problem",
            "status": "RANK_ONE_CHARGE_DIRECTION_DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "PH3986_1_not_full_parent_equality",
            "claim_piece": "parent equality guard",
            "mathematical_form": "Pi_M J_H = J_EH^M requires lambda_PiM_EH=1, Q_extra=0, parent J_H origin, and no exact-boundary leakage; current sources do not sign those factors",
            "derived_result": "full parent PiM/Hilbert equality remains open; no local-GR claim follows",
            "status": "FULL_PIM_HILBERT_EQUALITY_REJECTED_FOR_NOW",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "PH3986_2_amplitude_reduction",
            "claim_piece": "GM amplitude residual split",
            "mathematical_form": "epsilon_GM_amplitude_calibration <= |lambda_PiM_EH-1| + |Q_extra|/|Q_ref| + epsilon_parent_JH_origin + epsilon_universal_G_normalization",
            "derived_result": "source amplitude is reduced to normalization, extra monopole charge, parent source-current origin, and universal coupling terms",
            "status": "GM_AMPLITUDE_BOUND_SPLIT_DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "PH3986_3_reduced_master",
            "claim_piece": "3986 master residual",
            "mathematical_form": "epsilon_closed_source_failure_3986 <= epsilon_charge_normalization + epsilon_extra_monopole_charge + epsilon_parent_JH_origin + epsilon_universal_G_normalization + epsilon_PPN_source_stability",
            "derived_result": "3985 PiM/Hilbert plus GM amplitude terms are consolidated into a smaller amplitude/source-ownership residual vector",
            "status": "MASTER_RESIDUAL_REDUCED_TO_AMPLITUDE_SOURCE_VECTOR",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "PH3986_4_runner_contract",
            "claim_piece": "GM amplitude runner contract",
            "mathematical_form": "given sourced numeric lambda_PiM_EH, Q_extra_over_Qref, epsilon_parent_JH_origin, epsilon_universal_G_normalization, and epsilon_PPN_source_stability, compute epsilon_closed_source_failure_3986",
            "derived_result": "future real source rows can bound the remaining local Newton/GR source coupling without pretending the equality is proven",
            "status": "GM_AMPLITUDE_RUNNER_READY_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def certificate_rows(timestamp: str) -> list[dict[str, Any]]:
    common = {"claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp}
    return [
        {
            "certificate_id": "PHC3986_0_rank_one",
            "factor": "Z_rank_one_EH_charge_direction",
            "3985_status": "OPEN_INSIDE_PARENT_PIM_HILBERT",
            "3986_status": "CLOSED_FOR_CONTROLLED_EH_MONOPOLE_CHARGE_SPACE",
            "mathematical_content": "Q_proj=lambda_PiM_EH*Q_EH+Q_extra",
            "remaining_gap": "lambda normalization, extra charge, and parent origin are not fixed by rank-one geometry alone",
            "source_path": str(SRC / "P8_Y5_R2FR_3969_SINGLE_EXTERIOR_MASS_UNIQUENESS_THEOREM.csv"),
            **common,
        },
        {
            "certificate_id": "PHC3986_1_parent_PiM_direction",
            "factor": "Z_parent_PiM_direction",
            "3985_status": "STILL_OPEN_NEXT_PRIMARY_TARGET",
            "3986_status": "REDUCED_TO_RANK_ONE_NORMALIZATION_AND_PARENT_ORIGIN",
            "mathematical_content": "Pi_M J_H cannot point to an independent local scalar charge in the controlled one-charge EH exterior",
            "remaining_gap": "prove Pi_M is parent-owned and not a fitted selector",
            "source_path": str(SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv"),
            **common,
        },
        {
            "certificate_id": "PHC3986_2_Hilbert_equality",
            "factor": "Z_PiM_Hilbert_equality",
            "3985_status": "BLOCKED_PARENT_PIM_HILBERT_EQUALITY_OPEN",
            "3986_status": "NOT_CLOSED_REDUCED_TO_LAMBDA_AND_EXTRA_CHARGE",
            "mathematical_content": "Pi_M J_H=J_EH^M iff lambda_PiM_EH=1, Q_extra=0, parent J_H origin holds, and exact-boundary leakage vanishes",
            "remaining_gap": "lambda_PiM_EH, Q_extra, parent_JH, and exact-boundary terms need derivation or numeric/source bounds",
            "source_path": str(SRC / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv"),
            **common,
        },
        {
            "certificate_id": "PHC3986_3_GM_amplitude",
            "factor": "Z_GM_source_amplitude",
            "3985_status": "BLOCKED_AMPLITUDE_SOURCE_EQUALITY_OPEN",
            "3986_status": "NOT_CLOSED_BUT_BOUNDABLE",
            "mathematical_content": "epsilon_GM_amplitude_calibration <= epsilon_charge_normalization + epsilon_extra_monopole_charge + epsilon_parent_JH_origin + epsilon_universal_G_normalization",
            "remaining_gap": "real parent/source rows are required before Newtonian promotion",
            "source_path": str(SRC / "P8_Y5_R2FR_3985_RESIDUAL_REDUCTION_ROWS.csv"),
            **common,
        },
        {
            "certificate_id": "PHC3986_4_universal_G",
            "factor": "Z_universal_G_normalization",
            "3985_status": "OPEN_INSIDE_AMPLITUDE",
            "3986_status": "STILL_OPEN_NEXT_PRIMARY_TARGET",
            "mathematical_content": "one constant G_ref/kappa_eff normalizes all controlled local source charges",
            "remaining_gap": "derive constant universal coupling from parent action or bound drift/source dependence",
            "source_path": str(SRC / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv"),
            **common,
        },
        {
            "certificate_id": "PHC3986_5_extra_monopole",
            "factor": "Z_extra_monopole_charge_zero",
            "3985_status": "STILL_OPEN_MONOPOLE_EXTRA_CHARGE_RETAINED",
            "3986_status": "STILL_OPEN_EXPLICIT_Q_EXTRA_BOUND_ROW",
            "mathematical_content": "Q_extra=Q_nonEH+Q_symp+Q_PiM_stress+Q_domain+Q_memory+Q_range+Q_delta_kappa+Q_frame",
            "remaining_gap": "l>=1 hair is not the same as monopole extra charge; monopole channel needs zero theorem or bound",
            "source_path": str(SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv"),
            **common,
        },
        {
            "certificate_id": "PHC3986_6_total",
            "factor": "Z_closed_total_source_monopole",
            "3985_status": "FALSE_BUT_RESIDUAL_VECTOR_REDUCED_FOR_CONTROLLED_BRANCH",
            "3986_status": "FALSE_BUT_REDUCED_TO_AMPLITUDE_SOURCE_VECTOR",
            "mathematical_content": "epsilon_closed_source_failure_3986 is the current live source-coupling residual",
            "remaining_gap": "normalization, extra monopole charge, parent source current, universal G, and PPN stability",
            "source_path": str(SRC / "P8_Y5_R2FR_3985_CLOSED_SOURCE_CERTIFICATE_UPDATE.csv"),
            **common,
        },
    ]


def amplitude_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "GMA3986_0_master",
            "symbol": "epsilon_closed_source_failure_3986",
            "definition": "current reduced local source-coupling residual after rank-one PiM/EH direction reduction",
            "formula": "epsilon_charge_normalization + epsilon_extra_monopole_charge + epsilon_parent_JH_origin + epsilon_universal_G_normalization + epsilon_PPN_source_stability",
            "units": "dimensionless",
            "status": "REDUCED_AMPLITUDE_SOURCE_VECTOR_NONCLAIM",
            "source_path": str(SRC / "P8_Y5_R2FR_3985_RESIDUAL_REDUCTION_ROWS.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GMA3986_1_lambda",
            "symbol": "epsilon_charge_normalization",
            "definition": "normalization mismatch between parent projected charge and EH/Hamiltonian mass charge",
            "formula": "|lambda_PiM_EH - 1|",
            "units": "dimensionless",
            "status": "OPEN_REQUIRES_PARENT_NORMALIZATION_OR_SOURCE_BOUND",
            "source_path": str(SRC / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GMA3986_2_extra",
            "symbol": "epsilon_extra_monopole_charge",
            "definition": "extra scalar monopole charge not absorbed into the one EH mass direction",
            "formula": "|Q_extra|/|Q_ref|",
            "units": "dimensionless",
            "status": "OPEN_REQUIRES_ZERO_THEOREM_OR_BOUND",
            "source_path": str(SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GMA3986_3_parent_JH",
            "symbol": "epsilon_parent_JH_origin",
            "definition": "failure of the source current to come from parent matter/coframe variation before readout",
            "formula": "norm(J_H - delta S_matter/delta e_obs contracted with tau)/norm(J_ref)",
            "units": "dimensionless",
            "status": "OPEN_PARENT_MATTER_ACTION_NEEDED",
            "source_path": str(SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GMA3986_4_universal_G",
            "symbol": "epsilon_universal_G_normalization",
            "definition": "failure of one constant universal coupling G_ref/kappa_eff to normalize all controlled local source charges",
            "formula": "|delta ln G_eff| + |partial_t ln G_eff|T + |partial_r ln G_eff|L + source-dependence residual",
            "units": "dimensionless",
            "status": "OPEN_COUPLING_SUPERSELECTION_OR_BOUND_NEEDED",
            "source_path": str(SRC / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GMA3986_5_PPN",
            "symbol": "epsilon_PPN_source_stability",
            "definition": "remaining second-order local GR source stability residual after Newton shape and amplitude selection",
            "formula": "|gamma-1| + |beta-1| + sum_i |alpha_i| + sum_i |zeta_i| + |xi_PPN|",
            "units": "dimensionless",
            "status": "OPEN_PPN_BRANCH_NEEDED",
            "source_path": str(SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def runner_schema_rows(timestamp: str) -> list[dict[str, Any]]:
    fields = [
        ("source_id", "text", "row identifier"),
        ("lambda_PiM_EH", "dimensionless", "normalization of parent projected charge relative to EH mass charge"),
        ("Q_extra_over_Qref", "dimensionless", "absolute extra monopole charge over reference charge"),
        ("epsilon_parent_JH_origin", "dimensionless", "parent matter/coframe source-current origin residual"),
        ("epsilon_universal_G_normalization", "dimensionless", "universal coupling normalization/drift/source-dependence residual"),
        ("epsilon_PPN_source_stability", "dimensionless", "PPN source stability residual"),
        ("epsilon_closed_source_failure_3986", "dimensionless", "computed reduced source coupling residual"),
    ]
    return [
        {
            "field": field,
            "required": field != "epsilon_closed_source_failure_3986",
            "units": units,
            "description": description,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for field, units, description in fields
    ]


def compute_amplitude(row: dict[str, Any]) -> tuple[str, str, str]:
    required = [
        "lambda_PiM_EH",
        "Q_extra_over_Qref",
        "epsilon_parent_JH_origin",
        "epsilon_universal_G_normalization",
        "epsilon_PPN_source_stability",
    ]
    missing = [field for field in required if row.get(field, "") in {"", None, "MISSING"}]
    if missing:
        return ("BLOCKED_MISSING_INPUTS", "|".join(f"MISSING_{field}" for field in missing), "")
    try:
        value = abs(float(row["lambda_PiM_EH"]) - 1.0)
        value += abs(float(row["Q_extra_over_Qref"]))
        value += abs(float(row["epsilon_parent_JH_origin"]))
        value += abs(float(row["epsilon_universal_G_normalization"]))
        value += abs(float(row["epsilon_PPN_source_stability"]))
    except ValueError as exc:
        return ("BLOCKED_NONNUMERIC_INPUT", str(exc), "")
    return ("COMPUTED_NONCLAIM", "numeric smoke computation only", f"{value:.12g}")


def runner_smoke_rows(timestamp: str) -> list[dict[str, Any]]:
    inputs = [
        {
            "source_id": "SMOKE3986_0_exact_normalized_no_extra",
            "lambda_PiM_EH": "1.0",
            "Q_extra_over_Qref": "0.0",
            "epsilon_parent_JH_origin": "0.0",
            "epsilon_universal_G_normalization": "0.0",
            "epsilon_PPN_source_stability": "0.0",
        },
        {
            "source_id": "SMOKE3986_1_small_amplitude_residuals",
            "lambda_PiM_EH": "0.99999",
            "Q_extra_over_Qref": "2e-6",
            "epsilon_parent_JH_origin": "3e-6",
            "epsilon_universal_G_normalization": "4e-6",
            "epsilon_PPN_source_stability": "5e-6",
        },
        {
            "source_id": "SMOKE3986_2_real_parent_rows_missing",
            "lambda_PiM_EH": "",
            "Q_extra_over_Qref": "",
            "epsilon_parent_JH_origin": "",
            "epsilon_universal_G_normalization": "",
            "epsilon_PPN_source_stability": "",
        },
    ]
    rows: list[dict[str, Any]] = []
    for row in inputs:
        status, blockers, value = compute_amplitude(row)
        rows.append(
            {
                **row,
                "epsilon_closed_source_failure_3986": value,
                "runner_status": status,
                "blockers": blockers,
                "claim_allowed": False,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def projector_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "source_id": "REAL3986_0_controlled_EH_monopole_l2m0_rank_one_reduced",
            "angular_projector_status": "PASS_LGE1_ANGULAR_ZERO",
            "Q_lm_residual": "0",
            "epsilon_extra_MTS_l_ge_1": "0",
            "source_charge_residual_before": "epsilon_closed_source_failure_3985",
            "source_charge_residual_after": "epsilon_closed_source_failure_3986",
            "closed_or_reduced_in_3986": "Z_rank_one_EH_charge_direction|PiM_direction_reduced_to_lambda_plus_extra",
            "still_open": "epsilon_charge_normalization|epsilon_extra_monopole_charge|epsilon_parent_JH_origin|epsilon_universal_G_normalization|epsilon_PPN_source_stability",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def feed_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "feed_id": "FEED3986_0",
            "target": "Z_parent_PiM_direction",
            "update": "rank-one controlled EH charge space removes arbitrary scalar projector direction; only normalization and extra charge remain",
            "status": "PIM_DIRECTION_REDUCED_BRANCH_SPECIFIC",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "feed_id": "FEED3986_1",
            "target": "Z_PiM_Hilbert_equality",
            "update": "not closed; equality iff lambda_PiM_EH=1, Q_extra=0, parent JH origin, and exact-boundary silence",
            "status": "PIM_HILBERT_EQUALITY_NOT_CLOSED_BUT_FACTORED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "feed_id": "FEED3986_2",
            "target": "epsilon_GM_amplitude_calibration",
            "update": "split into charge normalization, extra monopole charge, parent source origin, and universal G normalization",
            "status": "GM_AMPLITUDE_BOUND_SPLIT_READY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "feed_id": "FEED3986_3",
            "target": "epsilon_closed_source_failure_3985",
            "update": "reduced to epsilon_closed_source_failure_3986",
            "status": "MASTER_RESIDUAL_REDUCED_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3986_0",
            "question": "can PiM/Hilbert equality be fully proved now",
            "answer": "no",
            "reason": "the controlled EH charge direction is one-dimensional, but lambda normalization, Q_extra, parent source-current origin, and universal coupling remain unsigned",
            "status": "FULL_EQUALITY_REJECTED_FOR_NOW",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3986_1",
            "question": "did the target narrow",
            "answer": "yes",
            "reason": "arbitrary PiM direction is removed for the controlled branch; remaining problem is amplitude/source normalization",
            "status": "TARGET_NARROWED_TO_AMPLITUDE_SOURCE_VECTOR",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3986_2",
            "question": "next best target",
            "answer": "derive universal coupling normalization or bound extra monopole charge",
            "reason": "those are now the largest remaining pieces blocking Newtonian source-owned promotion",
            "status": "MOVE_TO_UNIVERSAL_COUPLING_OR_EXTRA_MONOPOLE_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CLG3986_0",
            "gate": "PiM/Hilbert equality",
            "requirement": "lambda_PiM_EH=1, Q_extra=0, parent JH origin, and exact-boundary silence",
            "status": "BLOCKED_NORMALIZATION_AND_PARENT_ORIGIN_OPEN",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3986_1",
            "gate": "Newtonian GM amplitude",
            "requirement": "epsilon_closed_source_failure_3986=0 or bounded by source-backed numeric rows",
            "status": "BLOCKED_REAL_AMPLITUDE_ROWS_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3986_2",
            "gate": "local GR/PPN",
            "requirement": "GM amplitude plus PPN source stability",
            "status": "BLOCKED_PPN_SOURCE_STABILITY_OPEN",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3986_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive universal coupling normalization or bound the extra monopole charge left after rank-one PiM/Hilbert reduction",
            "success_condition": "epsilon_charge_normalization or epsilon_extra_monopole_charge is closed/bounded with sourced parent inputs, reducing epsilon_closed_source_failure_3986 without a closure axiom",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PIM_HILBERT_DIRECTION_REDUCED_GM_AMPLITUDE_BOUND_READY",
            "strongest_result": "controlled EH one-charge geometry forces any closed scalar source projector into the same rank-one charge direction; full equality is reduced to normalization, extra charge, parent JH origin, universal coupling, and PPN stability",
            "claim_status": "NONCLAIM_AMPLITUDE_SOURCE_VECTOR_OPEN",
            "next_target": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def all_rows(timestamp: str) -> dict[str, list[dict[str, Any]]]:
    return {
        "sources": source_register_rows(timestamp),
        "theorem": theorem_rows(timestamp),
        "certificate": certificate_rows(timestamp),
        "amplitude": amplitude_rows(timestamp),
        "runner_schema": runner_schema_rows(timestamp),
        "runner_smoke": runner_smoke_rows(timestamp),
        "projector": projector_rows(timestamp),
        "feed": feed_rows(timestamp),
        "decision": decision_rows(timestamp),
        "claim_gate": claim_gate_rows(timestamp),
        "next": next_rows(timestamp),
        "status": status_rows(timestamp),
    }


def doc_text(timestamp: str, sources: list[dict[str, Any]]) -> str:
    source_lines = "\n".join(
        f"- `{row['source_id']}`: `{row['path']}` needle `{row['needle']}` found={row['needle_found']}"
        for row in sources
    )
    return f"""# 3986 — Parent PiM/Hilbert Equality Or GM Source-Amplitude Bound

Timestamp: `{timestamp}`

## Result

This checkpoint attacks the actual coupling knot.

For the controlled stationary EH/no-extra-hair monopole branch, the exterior scalar charge space is rank one: after fixed background/reference subtraction there is only one scalar mass charge, `mu`.

Therefore a closed scalar projected source charge cannot point in an arbitrary direction. It must take the form

`Q_proj = lambda_PiM_EH * Q_EH + Q_extra`.

That is progress: the `Pi_M/Hilbert` problem is no longer an open-ended projector fog. It is reduced to:

- normalization: `lambda_PiM_EH = 1`;
- extra scalar monopole charge: `Q_extra=0`;
- parent source-current origin;
- universal `G_ref/kappa_eff` normalization;
- PPN source stability.

## New Bound Form

The current live source residual becomes

`epsilon_closed_source_failure_3986 <= epsilon_charge_normalization + epsilon_extra_monopole_charge + epsilon_parent_JH_origin + epsilon_universal_G_normalization + epsilon_PPN_source_stability`.

where

`epsilon_charge_normalization = |lambda_PiM_EH - 1|`

and

`epsilon_extra_monopole_charge = |Q_extra|/|Q_ref|`.

## Nonclaim Guard

Full `Pi_M J_H = J_EH^M` is not claimed. The rank-one result proves the *directional reduction* only. It does not prove the parent projector owns the source, nor that the amplitude is universally normalized.

## Runner

`P8_Y5_R2FR_3986_GM_AMPLITUDE_SMOKE_RESULTS.csv` computes the new amplitude/source residual when numeric parent rows exist and blocks when they do not.

## Source Register

{source_lines}

## Next Target

`{NEXT_DOC}`

Either derive universal coupling normalization or bound/zero the extra monopole charge.
"""


def update_spine(timestamp: str) -> None:
    marker = "## 3986 - PiM/Hilbert Direction Reduced"
    entry = f"""

{marker}

- Timestamp: `{timestamp}`
- Status: `PIM_HILBERT_DIRECTION_REDUCED_GM_AMPLITUDE_BOUND_READY`
- Main derivation:
  controlled stationary EH monopole has rank-one scalar charge space, so any closed scalar source projector has `Q_proj=lambda_PiM_EH*Q_EH+Q_extra`.
- What closed:
  arbitrary `Pi_M` direction is removed for this controlled branch.
- What remains:
  `lambda_PiM_EH=1`, `Q_extra=0`, parent `J_H` origin, universal `G_ref/kappa_eff`, and PPN source stability.
- Current residual:
  `epsilon_closed_source_failure_3986 <= epsilon_charge_normalization + epsilon_extra_monopole_charge + epsilon_parent_JH_origin + epsilon_universal_G_normalization + epsilon_PPN_source_stability`.
- Next: `{NEXT_DOC}`.
"""
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else "# Local GR Coupling Spine Current State\n"
    if marker not in existing:
        SPINE_PATH.write_text(existing.rstrip() + entry + "\n", encoding="utf-8")


def validation_rows(timestamp: str, rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    sources = rows["sources"]
    theorem = rows["theorem"]
    certificate = rows["certificate"]
    amplitude = rows["amplitude"]
    runner_schema = rows["runner_schema"]
    runner_smoke = rows["runner_smoke"]
    projector = rows["projector"]
    feed = rows["feed"]
    decisions = rows["decision"]
    claims = rows["claim_gate"]
    next_target = rows["next"]

    def val(validation_id: str, passed: bool, detail: str) -> dict[str, Any]:
        return {
            "validation_id": validation_id,
            "passed": bool(passed),
            "detail": detail,
            "timestamp_utc": timestamp,
        }

    parsed = True
    parse_detail = "generated CSV files parse cleanly"
    for path in generated_csvs:
        try:
            read_csv(path)
        except Exception as exc:
            parsed = False
            parse_detail = f"{path} failed to parse: {exc}"
            break

    theorem_statuses = {str(row["status"]) for row in theorem}
    cert_statuses = {str(row["3986_status"]) for row in certificate}
    amplitude_symbols = {str(row["symbol"]) for row in amplitude}
    schema_fields = {str(row["field"]) for row in runner_schema}
    smoke_by_id = {str(row["source_id"]): row for row in runner_smoke}
    feed_statuses = {str(row["status"]) for row in feed}
    decision_statuses = {str(row["status"]) for row in decisions}
    claim_statuses = {str(row["status"]) for row in claims}
    required_amplitude = {
        "epsilon_closed_source_failure_3986",
        "epsilon_charge_normalization",
        "epsilon_extra_monopole_charge",
        "epsilon_parent_JH_origin",
        "epsilon_universal_G_normalization",
        "epsilon_PPN_source_stability",
    }
    required_schema = {
        "source_id",
        "lambda_PiM_EH",
        "Q_extra_over_Qref",
        "epsilon_parent_JH_origin",
        "epsilon_universal_G_normalization",
        "epsilon_PPN_source_stability",
        "epsilon_closed_source_failure_3986",
    }
    project = projector[0]

    return [
        val("VAL3986_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist"),
        val("VAL3986_01_needles_found", all(row["needle_found"] for row in sources), "all cited source needles found"),
        val("VAL3986_02_theorem_statuses", {"RANK_ONE_CHARGE_DIRECTION_DERIVED", "FULL_PIM_HILBERT_EQUALITY_REJECTED_FOR_NOW", "GM_AMPLITUDE_BOUND_SPLIT_DERIVED", "MASTER_RESIDUAL_REDUCED_TO_AMPLITUDE_SOURCE_VECTOR", "GM_AMPLITUDE_RUNNER_READY_NONCLAIM"} <= theorem_statuses, "rank-one reduction, equality guard, amplitude split, reduced master, and runner theorem rows present"),
        val("VAL3986_03_certificate_progress", {"CLOSED_FOR_CONTROLLED_EH_MONOPOLE_CHARGE_SPACE", "REDUCED_TO_RANK_ONE_NORMALIZATION_AND_PARENT_ORIGIN", "NOT_CLOSED_REDUCED_TO_LAMBDA_AND_EXTRA_CHARGE", "NOT_CLOSED_BUT_BOUNDABLE", "FALSE_BUT_REDUCED_TO_AMPLITUDE_SOURCE_VECTOR"} <= cert_statuses, "certificate records directional closure and remaining open equality"),
        val("VAL3986_04_amplitude_symbols", required_amplitude <= amplitude_symbols, "amplitude/source vector rows present"),
        val("VAL3986_05_runner_schema", required_schema <= schema_fields, "runner schema has required amplitude fields"),
        val("VAL3986_06_runner_zero", smoke_by_id["SMOKE3986_0_exact_normalized_no_extra"]["epsilon_closed_source_failure_3986"] == "0", "exact normalized smoke computes zero"),
        val("VAL3986_07_runner_small", smoke_by_id["SMOKE3986_1_small_amplitude_residuals"]["epsilon_closed_source_failure_3986"] == "2.4e-05", "small amplitude smoke computes expected residual"),
        val("VAL3986_08_runner_blocks_missing", smoke_by_id["SMOKE3986_2_real_parent_rows_missing"]["runner_status"] == "BLOCKED_MISSING_INPUTS", "runner blocks missing real parent rows"),
        val("VAL3986_09_projector_reduced", project["source_charge_residual_after"] == "epsilon_closed_source_failure_3986" and "epsilon_charge_normalization" in project["still_open"], "projector row points at 3986 reduced residual"),
        val("VAL3986_10_feed", {"PIM_DIRECTION_REDUCED_BRANCH_SPECIFIC", "PIM_HILBERT_EQUALITY_NOT_CLOSED_BUT_FACTORED", "GM_AMPLITUDE_BOUND_SPLIT_READY", "MASTER_RESIDUAL_REDUCED_NONCLAIM"} <= feed_statuses, "feed rows capture PiM reduction and amplitude split"),
        val("VAL3986_11_decision", {"FULL_EQUALITY_REJECTED_FOR_NOW", "TARGET_NARROWED_TO_AMPLITUDE_SOURCE_VECTOR", "MOVE_TO_UNIVERSAL_COUPLING_OR_EXTRA_MONOPOLE_BOUND"} <= decision_statuses, "decision gate records no overclaim and next target"),
        val("VAL3986_12_claim_gate", {"BLOCKED_NORMALIZATION_AND_PARENT_ORIGIN_OPEN", "BLOCKED_REAL_AMPLITUDE_ROWS_MISSING", "BLOCKED_PPN_SOURCE_STABILITY_OPEN"} <= claim_statuses, "claim gates preserve remaining blocks"),
        val("VAL3986_13_next_target", next_target[0]["next_doc"] == NEXT_DOC and next_target[0]["next_script"] == NEXT_SCRIPT, "next target points to universal coupling or extra monopole bound"),
        val("VAL3986_14_all_nonclaim", all(not row.get("valid_for_claim", True) for group in rows.values() for row in group), "all generated physics rows remain nonclaim"),
        val("VAL3986_15_outputs_outside_fwb", all(FWB not in path.parents for path in generated_csvs) and FWB not in DOC_PATH.parents, "no generated output is inside formalization-workbench"),
        val("VAL3986_16_doc_exists", DOC_PATH.exists(), "checkpoint doc exists"),
        val("VAL3986_17_spine_updated", SPINE_PATH.exists() and "3986 - PiM/Hilbert Direction Reduced" in read_text(SPINE_PATH), "spine updated"),
        val("VAL3986_18_csv_parse", parsed, parse_detail),
        val("VAL3986_19_script_compile", True, "script compiled before validation write"),
        val("VAL3986_20_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]


def run() -> None:
    timestamp = now_utc()
    rows = all_rows(timestamp)

    write_csv(OUTPUTS["sources"], rows["sources"])
    write_csv(OUTPUTS["theorem"], rows["theorem"])
    write_csv(OUTPUTS["certificate"], rows["certificate"])
    write_csv(OUTPUTS["amplitude"], rows["amplitude"])
    write_csv(OUTPUTS["runner_schema"], rows["runner_schema"])
    write_csv(OUTPUTS["runner_smoke"], rows["runner_smoke"])
    write_csv(OUTPUTS["projector"], rows["projector"])
    write_csv(OUTPUTS["feed"], rows["feed"])
    write_csv(OUTPUTS["decision"], rows["decision"])
    write_csv(OUTPUTS["claim_gate"], rows["claim_gate"])
    write_csv(OUTPUTS["next"], rows["next"])
    write_csv(OUTPUTS["status"], rows["status"])

    DOC_PATH.write_text(doc_text(timestamp, rows["sources"]), encoding="utf-8")
    update_spine(timestamp)

    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    validations = validation_rows(timestamp, rows)
    write_csv(OUTPUTS["validation"], validations)
    failed = [row for row in validations if not row["passed"]]
    if failed:
        for row in failed:
            print(f"FAILED {row['validation_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"3986 validation passed: {len(validations)}/{len(validations)} checks")
    print(f"source needles: {sum(1 for row in rows['sources'] if row['needle_found'])}/{len(rows['sources'])}")
    print(rows["status"][0]["status"])


if __name__ == "__main__":
    run()

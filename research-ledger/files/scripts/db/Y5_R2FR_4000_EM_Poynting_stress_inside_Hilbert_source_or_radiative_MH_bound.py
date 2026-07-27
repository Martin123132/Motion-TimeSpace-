from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "4000"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "4000-Y5-R2FR-EM-Poynting-stress-inside-Hilbert-source-or-radiative-MH-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_4000_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_4000_EM_STRESS_POYNTING_THEOREM.csv",
    "contract": SRC / "P8_Y5_R2FR_4000_ONCE_ONLY_SOURCE_CONTRACT.csv",
    "bounds": SRC / "P8_Y5_R2FR_4000_RADIATIVE_MH_BOUND_VECTOR.csv",
    "cases": SRC / "P8_Y5_R2FR_4000_EVALUATOR_CASES.csv",
    "results": SRC / "P8_Y5_R2FR_4000_EVALUATOR_RESULTS.csv",
    "decision": SRC / "P8_Y5_R2FR_4000_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_4000_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_4000_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_4000_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_4000_VALIDATION.csv",
}

NEXT_DOC = "4001-Y5-R2FR-parent-projector-constancy-or-PiM-commutator-bound.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_4001_parent_projector_constancy_or_PiM_commutator_bound.py"


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
        ("SRC4000_00_next", SRC / "P8_Y5_R2FR_3999_NEXT_TARGET.csv", "NEXT3999_0", "3999 handoff"),
        ("SRC4000_01_action", SRC / "P8_Y5_R2FR_3463_MAXWELL_POYNTING_STRESS_LEDGER.csv", "EM3463_0_action", "Maxwell action"),
        ("SRC4000_02_stress", SRC / "P8_Y5_R2FR_3463_MAXWELL_POYNTING_STRESS_LEDGER.csv", "EM3463_1_hilbert_stress", "EM Hilbert stress"),
        ("SRC4000_03_poynting", SRC / "P8_Y5_R2FR_3463_MAXWELL_POYNTING_STRESS_LEDGER.csv", "EM3463_2_poynting", "Poynting stress-current component"),
        ("SRC4000_04_exchange", SRC / "P8_Y5_R2FR_3463_MAXWELL_POYNTING_STRESS_LEDGER.csv", "EM3463_3_exchange", "matter-EM exchange"),
        ("SRC4000_05_multiplier", SRC / "P8_Y5_R2FR_3463_MAXWELL_POYNTING_STRESS_LEDGER.csv", "EM3463_4_multiplier_obstruction", "EM normalization obstruction"),
        ("SRC4000_06_vector_minimal", SRC / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv", "EMF3502_0_minimal_bound_field_stress", "minimal bound field stress"),
        ("SRC4000_07_vector_flux", SRC / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv", "EMF3502_1_radiative_poynting_flux", "radiative Poynting flux"),
        ("SRC4000_08_vector_exchange", SRC / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv", "EMF3502_5_matter_EM_internal_exchange", "internal exchange"),
        ("SRC4000_09_owner_bound", SRC / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv", "EMB3503_4_Phi_EM_rad", "Poynting owner bound"),
        ("SRC4000_10_3883", SRC / "P8_Y5_R2FR_3883_MAXWELL_STRESS_POYNTING_DERIVATION.csv", "MX3883_4_poynting", "once-only Poynting accounting"),
        ("SRC4000_11_3873", SRC / "P8_Y5_R2FR_3873_POYNTING_STATIONARY_BOUNDARY_ZERO_THEOREM.csv", "PZT3873_2_stationary_zero", "stationary boundary zero theorem"),
        ("SRC4000_12_3961", SRC / "P8_Y5_R2FR_3961_POYNTING_NO_FLUX_THEOREM_OR_BOUND.csv", "PNF3961_2_flux_bound", "Poynting flux bound"),
        ("SRC4000_13_3978", SRC / "P8_Y5_R2FR_3978_POYNTING_INCLUSION_CONTRACT.csv", "PIC3978_2_internal_flow_allowed", "internal Poynting guard"),
        ("SRC4000_14_3981", SRC / "P8_Y5_R2FR_3981_CONTROLLED_POYNTING_SILENCE_THEOREM.csv", "CPS3981_1_internal_guard", "controlled silence guard"),
        ("SRC4000_15_3993", SRC / "P8_Y5_R2FR_3993_EM_POYNTING_MAP_LEDGER.csv", "EMDD3993_0_minimal_bound_stress", "EM/Poynting source map"),
        ("SRC4000_16_3994", SRC / "P8_Y5_R2FR_3994_POYNTING_FLUX_ZERO_OR_BOUND_ROWS.csv", "PY3994_2_flux_bound", "latest Poynting bound rows"),
        ("SRC4000_17_3999", SRC / "P8_Y5_R2FR_3999_MH_FLUX_BOUND_VECTOR.csv", "MHF3999_5_radiation_Poynting", "3999 M_H radiation gate"),
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
            "theorem_id": "EMP4000_0_Maxwell_action_branch",
            "claim_piece": "minimal observed Maxwell action source branch",
            "mathematical_form": "S_EM = -(1/(4 mu0)) int sqrt(-g_obs) F_ab F^ab + int A_a J^a",
            "derived_result": "if the observed Hodge/coframe and normalization are parent-owned, EM stress is varied through the same Hilbert source slot as ordinary matter",
            "status": "STANDARD_CONDITIONAL_ACTION_FORM",
            "source_path": str(SRC / "P8_Y5_R2FR_3463_MAXWELL_POYNTING_STRESS_LEDGER.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "EMP4000_1_Hilbert_stress_inclusion",
            "claim_piece": "EM stress is inside total Hilbert source",
            "mathematical_form": "T_EM^{ab}=(1/mu0)(F^{a c}F^b_c - (1/4)g_obs^{ab}F_cd F^cd)",
            "derived_result": "bound EM energy, pressure, momentum density, and stress contribute to J_H_total once; they are not an extra fitted MTS force",
            "status": "EXACT_VARIATIONAL_IDENTITY_CONDITIONAL_ON_ACTION_BRANCH",
            "source_path": str(SRC / "P8_Y5_R2FR_3883_MAXWELL_STRESS_POYNTING_DERIVATION.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "EMP4000_2_Poynting_as_stress_flux",
            "claim_piece": "Poynting vector is the spatial stress-current flux",
            "mathematical_form": "local observed frame: T_EM^{0i}=S_Poynting^i/c^2, with S_Poynting=E x H",
            "derived_result": "the Poynting intuition is legitimate: it tests source-current flow, not a separate patch to be added after GR",
            "status": "EXACT_CONDITIONAL_LOCAL_FRAME_IDENTITY",
            "source_path": str(SRC / "P8_Y5_R2FR_3463_MAXWELL_POYNTING_STRESS_LEDGER.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "EMP4000_3_internal_exchange_cancellation",
            "claim_piece": "matter-EM Lorentz exchange cancels in total stress",
            "mathematical_form": "nabla_a T_EM^{ab}=-F^{b c}J_c and nabla_a T_matter^{ab}=+F^{b c}J_c, hence nabla_a(T_matter+T_EM)^{ab}=0 up to parent extra channels",
            "derived_result": "using matter-only source tubes is wrong; the conserved object is total matter+EM Hilbert stress",
            "status": "EXACT_SAME_ACTION_WARD_CANCELLATION",
            "source_path": str(SRC / "P8_Y5_R2FR_3760_MAXWELL_EM_STRESS_SOURCE_THEOREM.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "EMP4000_4_stationary_no_leakage",
            "claim_piece": "stationary isolated Poynting leakage zero",
            "mathematical_form": "dU_EM/dt + int_boundary S_Poynting.n dA = -int_W J.E dV; time averages with dU_EM=0 and int J.E=0 give <Phi_EM_rad>=0",
            "derived_result": "circulating internal Poynting can be nonzero while net boundary leakage vanishes in a closed stationary source worldtube",
            "status": "DERIVED_CONDITIONAL_STATIONARY_ZERO",
            "source_path": str(SRC / "P8_Y5_R2FR_3961_POYNTING_NO_FLUX_THEOREM_OR_BOUND.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "EMP4000_5_radiative_bound",
            "claim_piece": "open radiative branch becomes source-mass drift",
            "mathematical_form": "|Delta_rad_Poynting| <= (|Delta U_EM| + |W_matter| + |Phi_external| + |B_improvement|)/(M_H c^2)",
            "derived_result": "if EM radiation/background flux crosses the local source boundary, it is a bounded M_H leakage row, not a hidden constant or orbital backfill",
            "status": "EXECUTABLE_RADIATIVE_BOUND_TEMPLATE",
            "source_path": str(SRC / "P8_Y5_R2FR_3994_POYNTING_FLUX_ZERO_OR_BOUND_ROWS.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "EMP4000_6_nonminimal_guard",
            "claim_piece": "EM/Poynting inclusion does not derive EM itself",
            "mathematical_form": "epsilon_EM_source_4000 retains Delta_Hodge_EM, delta_w_EM, C_XF2, C_JQ, C_EM_readout, Delta_rad_Poynting, and Delta_internal_exchange",
            "derived_result": "Maxwell stress can be included in the source while charge normalization, alpha, no-extra-F2, and readout/radiative closure remain live gates",
            "status": "NO_EM_UNIFICATION_OVERCLAIM_GUARD",
            "source_path": str(SRC / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def contract_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "EMC4000_0_once_only",
            "rule": "bound/local EM field stress is included in J_H_total exactly once",
            "allowed_use": "T_EM contributes to M_H for bound fields inside the source worldtube",
            "forbidden_use": "add a second Poynting/source force after already including T_EM in Hilbert stress",
            "status": "ONCE_ONLY_ACCOUNTING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "contract_id": "EMC4000_1_no_matter_only_tube",
            "rule": "source worldtube must carry total matter+EM stress, not matter-only stress",
            "allowed_use": "matter-EM Lorentz exchange is internal to T_total",
            "forbidden_use": "delete EM binding/Poynting stress from the Newton/GR source denominator",
            "status": "TOTAL_SOURCE_TUBE_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "contract_id": "EMC4000_2_internal_flow_guard",
            "rule": "internal Poynting circulation may be nonzero even when net boundary flux is zero",
            "allowed_use": "zero only the net leakage integral through the selected source boundary",
            "forbidden_use": "set S_Poynting=0 pointwise to force a plateau",
            "status": "INTERNAL_FLOW_NOT_DELETED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "contract_id": "EMC4000_3_radiative_leakage",
            "rule": "net EM/wave/background flux crossing the source boundary is Delta_rad_Poynting",
            "allowed_use": "zero it for stationary isolated branches or bound it from energy/work/flux rows",
            "forbidden_use": "absorb it into orbital GM, G0, or a source mass definition",
            "status": "RADIATIVE_MH_LEAKAGE_GATE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "contract_id": "EMC4000_4_no_EM_origin_claim",
            "rule": "Poynting inclusion is not a derivation of charge, alpha, Coulomb law, or Maxwell emergence",
            "allowed_use": "local-GR/Newton source bookkeeping and source-drift bounds",
            "forbidden_use": "public unification claim from Poynting accounting alone",
            "status": "NO_OVERCLAIM_GUARD",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def bound_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "EMB4000_0_master",
            "target": "epsilon_EM_source_4000",
            "formula": "|Delta_Hodge_EM|+|delta_w_EM|+|C_XF2|+|C_JQ|+|C_EM_readout|+|Delta_rad_Poynting|+|Delta_internal_exchange|",
            "numeric_value": "MISSING_PARENT_SIGNED_COMPONENTS",
            "units": "dimensionless",
            "status": "EXECUTABLE_VECTOR_READY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "EMB4000_1_bound_stress_inside_MH",
            "target": "epsilon_EM_bound_stress_not_in_MH",
            "formula": "0 if minimal Maxwell stress is varied with the same observed coframe and included in J_H_total",
            "numeric_value": "ZERO_CONDITIONAL_INSIDE_MH",
            "units": "dimensionless",
            "status": "CONDITIONAL_ZERO_ROUTE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "EMB4000_2_radiative_flux",
            "target": "Delta_rad_Poynting",
            "formula": "(|Delta U_EM|+|W_matter|+|Phi_external|+|B_improvement|)/(M_H c^2)",
            "numeric_value": "MISSING_FLUX_WINDOW_AND_SOURCE_ROWS",
            "units": "dimensionless_per_window_or_time^-1_declared",
            "status": "FINITE_BOUND_TEMPLATE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "EMB4000_3_Hodge",
            "target": "Delta_Hodge_EM",
            "formula": "*_EM - *_obs[e_obs(q)] or chi_EM - chi_obs",
            "numeric_value": "MISSING_OBSERVED_HODGE_PARENT_SIGNATURE",
            "units": "dimensionless_or_tensor",
            "status": "OPEN_MAXWELL_GEOMETRY_OWNER",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "EMB4000_4_normalization",
            "target": "delta_w_EM",
            "formula": "D ln w_EM or w_EM-1 for Maxwell action/stress scale",
            "numeric_value": "MISSING_UNIQUE_F2_OR_ALPHA_OWNER",
            "units": "dimensionless",
            "status": "OPEN_NORMALIZATION_OWNER",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "EMB4000_5_nonminimal",
            "target": "C_XF2 + C_EM_readout",
            "formula": "hidden/motion/time field F^2 terms plus radiative/readout regeneration",
            "numeric_value": "MISSING_OPERATOR_EXCLUSION_OR_BOUND",
            "units": "model_dependent",
            "status": "OPEN_NONMINIMAL_EM_GUARD",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "EMB4000_6_internal_exchange",
            "target": "Delta_internal_exchange",
            "formula": "0 if matter and EM are varied in same parent action/current owner; otherwise source-current mismatch bound",
            "numeric_value": "ZERO_CONDITIONAL_IN_TOTAL_STRESS",
            "units": "dimensionless",
            "status": "CONDITIONAL_ZERO_ROUTE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def case_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "case_id": "CASE4000_0_static_bound_EM_inside_MH",
            "route": "minimal_static_total_Hilbert_source",
            "Delta_Hodge_EM": 0.0,
            "delta_w_EM": 0.0,
            "C_XF2": 0.0,
            "C_JQ": 0.0,
            "C_EM_readout": 0.0,
            "Delta_rad_Poynting": 0.0,
            "Delta_internal_exchange": 0.0,
            "uses_matter_only_source_tube": False,
            "double_counts_EM_stress": False,
            "input_status": "CONDITIONAL_STATIC_BOUND_BRANCH",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4000_1_internal_Poynting_circulation",
            "route": "internal_flow_no_boundary_leakage",
            "Delta_Hodge_EM": 0.0,
            "delta_w_EM": 0.0,
            "C_XF2": 0.0,
            "C_JQ": 0.0,
            "C_EM_readout": 0.0,
            "Delta_rad_Poynting": 0.0,
            "Delta_internal_exchange": 0.0,
            "uses_matter_only_source_tube": False,
            "double_counts_EM_stress": False,
            "internal_poynting_present": True,
            "input_status": "INTERNAL_FLOW_ALLOWED_ZERO_BOUNDARY_FLUX",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4000_2_radiative_boundary_flux",
            "route": "open_radiative_flux_bound",
            "Delta_Hodge_EM": 0.0,
            "delta_w_EM": 0.0,
            "C_XF2": 0.0,
            "C_JQ": 0.0,
            "C_EM_readout": 0.0,
            "Delta_rad_Poynting": 4.0e-5,
            "Delta_internal_exchange": 0.0,
            "uses_matter_only_source_tube": False,
            "double_counts_EM_stress": False,
            "input_status": "RADIATIVE_FLUX_RETAINED",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4000_3_nonminimal_EM_residuals",
            "route": "hidden_F2_or_normalization_open",
            "Delta_Hodge_EM": 1.0e-6,
            "delta_w_EM": 2.0e-6,
            "C_XF2": 3.0e-6,
            "C_JQ": 4.0e-6,
            "C_EM_readout": 5.0e-6,
            "Delta_rad_Poynting": 0.0,
            "Delta_internal_exchange": 0.0,
            "uses_matter_only_source_tube": False,
            "double_counts_EM_stress": False,
            "input_status": "NONMINIMAL_VECTOR_NONZERO",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4000_4_matter_only_tube_refused",
            "route": "forbidden_source_tube",
            "Delta_Hodge_EM": 0.0,
            "delta_w_EM": 0.0,
            "C_XF2": 0.0,
            "C_JQ": 0.0,
            "C_EM_readout": 0.0,
            "Delta_rad_Poynting": 0.0,
            "Delta_internal_exchange": 0.0,
            "uses_matter_only_source_tube": True,
            "double_counts_EM_stress": False,
            "input_status": "MATTER_ONLY_SOURCE_TUBE",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4000_5_double_count_refused",
            "route": "forbidden_second_source",
            "Delta_Hodge_EM": 0.0,
            "delta_w_EM": 0.0,
            "C_XF2": 0.0,
            "C_JQ": 0.0,
            "C_EM_readout": 0.0,
            "Delta_rad_Poynting": 0.0,
            "Delta_internal_exchange": 0.0,
            "uses_matter_only_source_tube": False,
            "double_counts_EM_stress": True,
            "input_status": "DOUBLE_COUNTS_EM_STRESS",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4000_6_missing_parent_rows",
            "route": "missing_EM_owner_components",
            "Delta_Hodge_EM": "",
            "delta_w_EM": "",
            "C_XF2": "",
            "C_JQ": "",
            "C_EM_readout": "",
            "Delta_rad_Poynting": "",
            "Delta_internal_exchange": "",
            "uses_matter_only_source_tube": False,
            "double_counts_EM_stress": False,
            "input_status": "MISSING_EM_SOURCE_COMPONENT_VECTOR",
            "timestamp_utc": timestamp,
        },
    ]


NUMERIC_FIELDS = [
    "Delta_Hodge_EM",
    "delta_w_EM",
    "C_XF2",
    "C_JQ",
    "C_EM_readout",
    "Delta_rad_Poynting",
    "Delta_internal_exchange",
]


def optional_float(value: Any) -> float | None:
    text = str(value).strip()
    if not text or text.upper().startswith("MISSING"):
        return None
    return float(text)


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def evaluate_case(row: dict[str, Any]) -> dict[str, Any]:
    values = {field: optional_float(row.get(field)) for field in NUMERIC_FIELDS}
    matter_only = as_bool(row.get("uses_matter_only_source_tube"))
    double_count = as_bool(row.get("double_counts_EM_stress"))
    result: dict[str, Any] = {
        "case_id": row["case_id"],
        "route": row["route"],
        "input_status": row["input_status"],
        "epsilon_EM_source_4000": "MISSING",
        "epsilon_geometry_normalization_abs": "MISSING",
        "epsilon_nonminimal_readout_abs": "MISSING",
        "epsilon_flux_exchange_abs": "MISSING",
        "uses_matter_only_source_tube": matter_only,
        "double_counts_EM_stress": double_count,
        "passes_schema": False,
        "passes_total_source_tube": not matter_only,
        "passes_once_only": not double_count,
        "static_bound_stress_inside_MH": False,
        "bound_ready": False,
        "claim_allowed": False,
        "valid_for_claim": False,
    }
    if any(value is None for value in values.values()):
        return result
    geometry_norm = abs(values["Delta_Hodge_EM"] or 0.0) + abs(values["delta_w_EM"] or 0.0) + abs(values["C_JQ"] or 0.0)
    nonminimal_readout = abs(values["C_XF2"] or 0.0) + abs(values["C_EM_readout"] or 0.0)
    flux_exchange = abs(values["Delta_rad_Poynting"] or 0.0) + abs(values["Delta_internal_exchange"] or 0.0)
    total = geometry_norm + nonminimal_readout + flux_exchange
    result.update(
        {
            "epsilon_EM_source_4000": f"{total:.12e}",
            "epsilon_geometry_normalization_abs": f"{geometry_norm:.12e}",
            "epsilon_nonminimal_readout_abs": f"{nonminimal_readout:.12e}",
            "epsilon_flux_exchange_abs": f"{flux_exchange:.12e}",
            "passes_schema": True,
            "passes_total_source_tube": not matter_only,
            "passes_once_only": not double_count,
            "static_bound_stress_inside_MH": total == 0.0 and not matter_only and not double_count,
            "bound_ready": not matter_only and not double_count,
        }
    )
    return result


def result_rows(cases: list[dict[str, Any]], timestamp: str) -> list[dict[str, Any]]:
    rows = [evaluate_case(row) for row in cases]
    for row in rows:
        row["timestamp_utc"] = timestamp
    return rows


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4000_0",
            "finding": "Static/bound EM field stress belongs inside the total Hilbert source, not outside it.",
            "evidence": "Maxwell metric variation gives T_EM; same-action Ward exchange makes matter+EM total stress the conserved source current.",
            "limitation": "observed Hodge/coframe, charge/current normalization, and no-extra-F2/readout guards remain unsigned for full Maxwell/local-GR claims.",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4000_1",
            "finding": "Poynting is handled as stress-current flux: internal circulation is allowed, net boundary leakage is bounded.",
            "evidence": "Poynting theorem gives stationary no-flux zero branch and radiative flux bound branch.",
            "limitation": "general radiative/background flux still needs numeric source rows over a declared window.",
            "next_action": "derive parent Pi_M constancy/commutator now that EM/Poynting accounting is placed",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CLAIM4000_0_EM_stress_source",
            "claim": "EM stress is safely included in local GR/Newton source",
            "allowed": False,
            "reason": "conditional inclusion theorem is built, but parent Hodge/coframe and normalization owner remain unsigned",
            "required_exit": "derive observed Maxwell/Hodge owner and unique normalization, or provide finite bounds",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CLAIM4000_1_Poynting_silence",
            "claim": "Poynting flux is universally zero",
            "allowed": False,
            "reason": "only stationary isolated/controlled branches zero net boundary leakage; radiative/open branches require bounds",
            "required_exit": "branch certificate or numeric Delta_rad_Poynting row",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CLAIM4000_2_EM_unification",
            "claim": "charge/alpha/Coulomb/Maxwell emergence is derived",
            "allowed": False,
            "reason": "4000 is source bookkeeping, not an EM-origin theorem",
            "required_exit": "separate charge/current/Hodge/F2 owner derivation",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT4000_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive parent constancy of Pi_M on the local stationary exterior annulus or retain an explicit Pi_M commutator bound",
            "success_condition": "D_A Pi_M=0 and [d,Pi_M]J_H=0 are parent-owned, or Delta_PiM is decomposed into source-backed commutator/domain/reference rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "EM_POYNTING_STRESS_INSIDE_HILBERT_SOURCE_OR_RADIATIVE_MH_BOUND",
            "headline": "Bound EM stress is included once in J_H_total; internal Poynting flow is allowed; net radiative/background flux is a retained Delta_rad_Poynting M_H leakage row.",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(timestamp: str, sources: list[dict[str, Any]], results: list[dict[str, Any]]) -> None:
    found = sum(bool(row["needle_found"]) for row in sources)
    lines = [
        "# 4000 - EM/Poynting Stress Inside Hilbert Source Or Radiative MH Bound",
        "",
        f"Timestamp: `{timestamp}`",
        "",
        "## Result",
        "",
        "The Poynting route is now placed correctly in the local source ladder:",
        "",
        "- static/bound EM field stress lives inside `J_H_total` once;",
        "- internal Poynting circulation is allowed and must not be erased;",
        "- only net boundary/radiative/background Poynting flux becomes `Delta_rad_Poynting` source-mass leakage.",
        "",
        "## Derivation",
        "",
        "Start with the observed Maxwell branch",
        "",
        "`S_EM = -(1/(4 mu0)) int sqrt(-g_obs) F_ab F^ab + int A_a J^a`.",
        "",
        "Metric variation gives",
        "",
        "`T_EM^{ab}=(1/mu0)(F^{a c}F^b_c - (1/4)g_obs^{ab}F_cd F^cd)`.",
        "",
        "In a local observed frame, `T_EM^{0i}=S_Poynting^i/c^2`. Therefore the Poynting vector is literally source-current flow. It is not a separate force to bolt on after the Hilbert source has already included EM stress.",
        "",
        "The same-action Ward exchange gives",
        "",
        "`nabla_a T_EM^{ab}=-F^{bc}J_c`, `nabla_a T_matter^{ab}=+F^{bc}J_c`.",
        "",
        "So matter-only source tubes are forbidden. The conserved object is total matter+EM stress.",
        "",
        "## Flux Split",
        "",
        "The Poynting theorem gives",
        "",
        "`dU_EM/dt + int_boundary S_Poynting.n dA = -int_W J.E dV`.",
        "",
        "Stationary isolated branch: `time_avg(dU_EM/dt)=0` and `time_avg(int J.E)=0` imply zero net boundary leakage, while internal circulation may remain nonzero.",
        "",
        "Radiative/open branch:",
        "",
        "`|Delta_rad_Poynting| <= (|Delta U_EM| + |W_matter| + |Phi_external| + |B_improvement|)/(M_H c^2)`.",
        "",
        "## Evaluator Results",
        "",
    ]
    for row in results:
        lines.append(
            f"- `{row['case_id']}`: status `{row['input_status']}`, epsilon `{row['epsilon_EM_source_4000']}`, total_tube={row['passes_total_source_tube']}, once={row['passes_once_only']}, claim={row['claim_allowed']}"
        )
    lines.extend(
        [
            "",
            "## Verdict",
            "",
            "This closes a real bookkeeping confusion: Poynting is not ignored and not double-counted. It either sits inside the total Hilbert source for bound/stationary fields, or it is an explicit radiative source-drift residual.",
            "",
            "No EM-origin claim follows from this rung. Charge normalization, alpha, unique Maxwell/Hodge owner, nonminimal `F^2`, and readout/radiative regeneration remain live gates.",
            "",
            "## Next Target",
            "",
            "With EM/Poynting placed, the sharpest remaining local source blocker is the mass projector itself: prove `D_A Pi_M=0` and `[d,Pi_M]J_H=0`, or make the commutator a source-backed residual.",
            "",
            f"- `{NEXT_DOC}`",
            f"- `{NEXT_SCRIPT}`",
            "",
            "## Source Count",
            "",
            f"- source needles found: `{found}/{len(sources)}`",
            "",
        ]
    )
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def append_spine(timestamp: str) -> None:
    marker = "## 4000 - EM/Poynting Hilbert Source Placement"
    block = f"""

{marker}

- Timestamp: `{timestamp}`
- Result: bound/static EM stress is included once in `J_H_total`; internal Poynting circulation is allowed; only net boundary/radiative/background flux is `Delta_rad_Poynting`.
- Derivation: Maxwell metric variation supplies `T_EM`; matter-EM Lorentz exchange cancels only in total stress, so matter-only source tubes are forbidden.
- Bound route: `|Delta_rad_Poynting| <= (|Delta U_EM|+|W_matter|+|Phi_external|+|B_improvement|)/(M_H c^2)`.
- Claim status: source bookkeeping improved, but no charge/alpha/Coulomb/Maxwell-emergence claim.
- Next: `{NEXT_DOC}`.
"""
    current = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    if marker not in current:
        SPINE_PATH.write_text(current.rstrip() + block + "\n", encoding="utf-8")


def build_validation_rows(
    timestamp: str,
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    results: list[dict[str, Any]],
    compile_ok: bool,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail, "timestamp_utc": timestamp})

    source_paths = [Path(row["path"]) for row in sources]
    add("VAL4000_00_sources_exist", all(path.exists() for path in source_paths), "every cited source path exists")
    add("VAL4000_01_needles_found", all(bool(row["needle_found"]) for row in sources), "every cited source needle found")
    add("VAL4000_02_action_branch", any(row["theorem_id"] == "EMP4000_0_Maxwell_action_branch" for row in theorem), "Maxwell action branch present")
    add("VAL4000_03_stress_inclusion", any(row["theorem_id"] == "EMP4000_1_Hilbert_stress_inclusion" for row in theorem), "Hilbert stress inclusion present")
    add("VAL4000_04_poynting_identity", any(row["theorem_id"] == "EMP4000_2_Poynting_as_stress_flux" for row in theorem), "Poynting stress identity present")
    add("VAL4000_05_exchange", any(row["theorem_id"] == "EMP4000_3_internal_exchange_cancellation" for row in theorem), "internal exchange cancellation present")
    add("VAL4000_06_stationary_zero", any(row["theorem_id"] == "EMP4000_4_stationary_no_leakage" for row in theorem), "stationary no-leakage theorem present")
    add("VAL4000_07_radiative_bound", any(row["theorem_id"] == "EMP4000_5_radiative_bound" for row in theorem), "radiative bound theorem present")
    add("VAL4000_08_nonminimal_guard", any(row["theorem_id"] == "EMP4000_6_nonminimal_guard" for row in theorem), "nonminimal guard present")
    add("VAL4000_09_once_contract", any(row["contract_id"] == "EMC4000_0_once_only" for row in contract), "once-only contract present")
    add("VAL4000_10_total_tube_contract", any(row["contract_id"] == "EMC4000_1_no_matter_only_tube" for row in contract), "total source tube contract present")
    add("VAL4000_11_internal_flow_guard", any(row["contract_id"] == "EMC4000_2_internal_flow_guard" for row in contract), "internal flow guard present")
    add("VAL4000_12_master_bound", any(row["bound_id"] == "EMB4000_0_master" for row in bounds), "master bound present")
    add("VAL4000_13_rad_bound", any(row["bound_id"] == "EMB4000_2_radiative_flux" for row in bounds), "radiative bound present")
    static = next(row for row in results if row["case_id"] == "CASE4000_0_static_bound_EM_inside_MH")
    internal = next(row for row in results if row["case_id"] == "CASE4000_1_internal_Poynting_circulation")
    radiative = next(row for row in results if row["case_id"] == "CASE4000_2_radiative_boundary_flux")
    nonminimal = next(row for row in results if row["case_id"] == "CASE4000_3_nonminimal_EM_residuals")
    matter_only = next(row for row in results if row["case_id"] == "CASE4000_4_matter_only_tube_refused")
    double_count = next(row for row in results if row["case_id"] == "CASE4000_5_double_count_refused")
    missing = next(row for row in results if row["case_id"] == "CASE4000_6_missing_parent_rows")
    add("VAL4000_14_static_case", float(static["epsilon_EM_source_4000"]) == 0.0 and str(static["static_bound_stress_inside_MH"]).lower() == "true", "static bound EM inside M_H case clean")
    add("VAL4000_15_internal_case", float(internal["epsilon_EM_source_4000"]) == 0.0 and str(internal["passes_once_only"]).lower() == "true", "internal Poynting circulation allowed")
    add("VAL4000_16_radiative_case", float(radiative["epsilon_flux_exchange_abs"]) > 0.0, "radiative boundary flux retained")
    add("VAL4000_17_nonminimal_case", float(nonminimal["epsilon_nonminimal_readout_abs"]) > 0.0 and float(nonminimal["epsilon_geometry_normalization_abs"]) > 0.0, "nonminimal residuals retained")
    add("VAL4000_18_matter_only_refused", str(matter_only["passes_schema"]).lower() == "true" and str(matter_only["passes_total_source_tube"]).lower() == "false", "matter-only source tube refused")
    add("VAL4000_19_double_count_refused", str(double_count["passes_schema"]).lower() == "true" and str(double_count["passes_once_only"]).lower() == "false", "double-count EM stress refused")
    add("VAL4000_20_missing_blocks", missing["epsilon_EM_source_4000"] == "MISSING" and str(missing["passes_schema"]).lower() == "false", "missing parent rows block")
    add("VAL4000_21_claim_gate_false", all(str(row.get("allowed", "")).lower() == "false" for row in read_csv(OUTPUTS["claim_gate"])), "all claim gates false")
    add("VAL4000_22_next_target", OUTPUTS["next"].exists() and NEXT_DOC in read_text(OUTPUTS["next"]), "next target written")
    add("VAL4000_23_doc_exists", DOC_PATH.exists() and "not ignored and not double-counted" in read_text(DOC_PATH), "document written")
    add("VAL4000_24_spine_updated", SPINE_PATH.exists() and "## 4000 - EM/Poynting Hilbert Source Placement" in read_text(SPINE_PATH), "spine updated")
    add("VAL4000_25_no_fwb_outputs", not any(str(path).startswith(str(FWB)) for path in OUTPUTS.values()), "no outputs target formalization-workbench")
    add("VAL4000_26_compile", compile_ok, "script compiles")
    add("VAL4000_27_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "script __pycache__ removed")
    add("VAL4000_28_status_exists", OUTPUTS["status"].exists(), "status file exists")
    add("VAL4000_29_results_nonclaim", all(str(row.get("valid_for_claim", "")).lower() == "false" for row in results), "all evaluator results remain nonclaim")
    add("VAL4000_30_no_nan", not any("nan" in str(row).lower() or "inf" in str(row).lower() for row in results), "no nan/inf evaluator outputs")
    add("VAL4000_31_no_em_origin_claim", DOC_PATH.exists() and "No EM-origin claim" in read_text(DOC_PATH), "no EM-origin overclaim recorded")
    return checks


def main() -> None:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    theorem = theorem_rows(timestamp)
    contract = contract_rows(timestamp)
    bounds = bound_rows(timestamp)
    cases = case_rows(timestamp)
    results = result_rows(cases, timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["contract"], contract)
    write_csv(OUTPUTS["bounds"], bounds)
    write_csv(OUTPUTS["cases"], cases)
    write_csv(OUTPUTS["results"], results)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(timestamp, sources, results)
    append_spine(timestamp)

    compile_ok = True
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except py_compile.PyCompileError:
        compile_ok = False
    cache = SCRIPT_PATH.parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    validation = build_validation_rows(timestamp, sources, theorem, contract, bounds, results, compile_ok)
    write_csv(OUTPUTS["validation"], validation)
    passed = sum(1 for row in validation if row["passed"])
    total = len(validation)
    print(f"4000 validation: {passed}/{total} passed")
    if passed != total:
        for row in validation:
            if not row["passed"]:
                print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()

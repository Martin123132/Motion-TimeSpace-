from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_BOUNDARY_CLOCK_TAU_OWNER_2599"
CHECKPOINT_ID = "2599"

DOC = ROOT / "2599-Y5-R2FR-boundary-clock-normalized-tau-owner-or-delta-tau-source-pack.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_BOUNDARY_CLOCK_TAU_2599_SOURCE_REGISTER.csv",
    "owner_attempt": OUT / "P8_Y5_BOUNDARY_CLOCK_TAU_2599_OWNER_ATTEMPT.csv",
    "clock_obstruction": OUT / "P8_Y5_BOUNDARY_CLOCK_TAU_2599_CLOCK_OBSTRUCTION_LEDGER.csv",
    "delta_tau_source_pack": OUT / "P8_Y5_BOUNDARY_CLOCK_TAU_2599_DELTA_TAU_SOURCE_PACK.csv",
    "bound_runner_contract": OUT / "P8_Y5_BOUNDARY_CLOCK_TAU_2599_BOUND_RUNNER_CONTRACT.csv",
    "runner_refusal": OUT / "P8_Y5_BOUNDARY_CLOCK_TAU_2599_RUNNER_REFUSAL.csv",
    "claim_gates": OUT / "P8_Y5_BOUNDARY_CLOCK_TAU_2599_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_BOUNDARY_CLOCK_TAU_2599_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_BOUNDARY_CLOCK_TAU_2599_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_BOUNDARY_CLOCK_TAU_2599_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2599_VALIDATION.csv",
}

COPY_TARGETS = {
    "owner_attempt": QUEUE / "JR2599_BOUNDARY_CLOCK_TAU_OWNER_ATTEMPT_NONCLAIM.csv",
    "delta_tau_source_pack": LOCAL_BOUNDS / "Boundary_clock_delta_tau_source_pack_2599_NONCLAIM.csv",
    "bound_runner_contract": LOCAL_BOUNDS / "Delta_tau_bound_runner_contract_2599_NONCLAIM.csv",
    "next_target": QUEUE / "JR2599_TOBS_DELTA_TAU_NORM_OR_CLOCK_ACTION_NEXT.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def with_stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": utc_now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        **row,
    }


def row_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (list, tuple, set)):
        return ";".join(str(item) for item in value)
    if value is None:
        return ""
    return str(value)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row_value(row.get(field, "")) for field in fields})


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), len(rows), ""
    except Exception as exc:  # pragma: no cover - validation reports the error.
        return False, 0, str(exc)


def path_has_needles(path: Path, needles: list[str]) -> list[str]:
    if not path.exists():
        return needles
    text = path.read_text(encoding="utf-8", errors="replace")
    return [needle for needle in needles if needle not in text]


def source_register_rows() -> list[dict[str, Any]]:
    source_specs = [
        {
            "source_id": "SRC2599_00_2598_handoff",
            "source_path": ROOT / "2598-Y5-R2FR-parent-stationary-tau-generator-or-first-tau-role-source-rows.md",
            "needles": ["NEXT2598_0_selected", "STA2598_0_tau_obs_object", "VAL2598_OVERALL"],
            "role": "active handoff selecting boundary-clock tau ownership or delta_tau source pack",
        },
        {
            "source_id": "SRC2599_01_2598_next_queue",
            "source_path": QUEUE / "JR2598_BOUNDARY_CLOCK_TAU_OR_DELTA_TAU_SOURCE_PACK_NEXT.csv",
            "needles": ["NEXT2598_0_selected", "2599-Y5-R2FR-boundary-clock-normalized-tau-owner-or-delta-tau-source-pack.md"],
            "role": "machine-readable 2599 target and guardrails",
        },
        {
            "source_id": "SRC2599_02_2598_bound_interface",
            "source_path": OUT / "P8_Y5_STATIONARY_TAU_2598_DELTA_TAU_BOUND_INTERFACE.csv",
            "needles": ["DTB2598_1_numerator", "DTB2598_3_dimensionless_bound"],
            "role": "delta_tau numerator/denominator interface",
        },
        {
            "source_id": "SRC2599_03_1727_boundary_clock_doc",
            "source_path": ROOT / "1727-Y5-R2FR-boundary-clock-superselection-or-delta-tau-residual-first-row.md",
            "needles": ["BCS1727_0_boundary_clock_data", "BCT1727_4_verdict", "VAL1727_OVERALL"],
            "role": "boundary-clock superselection theorem attempt",
        },
        {
            "source_id": "SRC2599_04_1727_clock_audit",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1727_BOUNDARY_CLOCK_SUPERSELECTION_AUDIT.csv",
            "needles": ["BCS1727_0_boundary_clock_data", "BCS1727_7_verdict"],
            "role": "machine boundary-clock/reference superselection clauses",
        },
        {
            "source_id": "SRC2599_05_1727_delta_rows",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1727_DELTA_TAU_FIRST_RESIDUAL_ROW.csv",
            "needles": ["DTAU1727_0_delta_tau_first_residual", "DTAU1727_3_clock_normalization_delta"],
            "role": "first delta_tau residual rows",
        },
        {
            "source_id": "SRC2599_06_1728_coefficients",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1728_DELTA_TAU_BOUND_COEFFICIENT_ROWS.csv",
            "needles": ["DTC1728_0_C_Tobs_tau_primary", "DTC1728_3_total_coefficient_stack"],
            "role": "delta_tau coefficient templates",
        },
        {
            "source_id": "SRC2599_07_1809_clock_norm",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1809_TAU_CLOCK_XHAT_NORMALIZATION_AUDIT.csv",
            "needles": ["TCN1809_0_product_definition", "TCN1809_4_verdict"],
            "role": "clock product is source-backed but not tau-owner theorem",
        },
        {
            "source_id": "SRC2599_08_2322_common_frame",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_2322_TAU_PPN_COMMON_FRAME_DERIVATION_AUDIT.csv",
            "needles": ["TPA2322_1_tau_standard_scalar_tensor", "TPA2322_4_verdict"],
            "role": "conditional tau_PPN normalization and common-frame guard",
        },
        {
            "source_id": "SRC2599_09_2557_clock_gate",
            "source_path": OUT / "P8_Y5_NO_SHADOW_2557_CLOCK_COMPATIBILITY_GATE.csv",
            "needles": ["CLK2557_4_parent_clock_origin", "CLK2557_5_clock_leak_bound"],
            "role": "clock origin and leakage bound gate",
        },
        {
            "source_id": "SRC2599_10_2558_stationary_hypotheses",
            "source_path": OUT / "P8_Y5_NO_SHADOW_2558_STATIONARY_THEOREM_HYPOTHESES.csv",
            "needles": ["HYP2558_4_stationary_clock", "HYP2558_8_stress_not_claimed"],
            "role": "stationary local source hypotheses remain assumptions",
        },
        {
            "source_id": "SRC2599_11_689_components",
            "source_path": OUT / "P8_Y5_R10_689_COMPONENT_ZERO_THEOREM_AUDIT.csv",
            "needles": ["ZTA689_1_shear", "ZTA689_6_stress_envelope"],
            "role": "symgrad_tau component zero-theorem audit",
        },
        {
            "source_id": "SRC2599_12_2597_mhref_rows",
            "source_path": OUT / "P8_Y5_TAU_IDENTITY_2597_MHREF_SOURCE_ACQUISITION_ROWS.csv",
            "needles": ["MHA2597_1_tau_obs", "MHA2597_10_acceptance"],
            "role": "tau/M_H_ref source acquisition fields",
        },
    ]

    rows: list[dict[str, Any]] = []
    for source in source_specs:
        source_path = source["source_path"]
        missing_needles = path_has_needles(source_path, source["needles"])
        rows.append(
            with_stamp(
                {
                    "source_id": source["source_id"],
                    "source_path": source_path,
                    "exists": source_path.exists(),
                    "missing_needles": missing_needles,
                    "source_pass": source_path.exists() and not missing_needles,
                    "role": source["role"],
                    "valid_for_claim": False,
                }
            )
        )
    return rows


def owner_attempt_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "attempt_id": "BCT2599_0_boundary_clock_class",
            "clause": "parent boundary clock class",
            "required_identity": "B_clock=(clock species, worldline/surface, e_obs|B, unit normalization) is selected by the parent branch before readout",
            "attempted_derivation": "boundary data fix tau_obs normalization at B",
            "current_status": "MISSING_PARENT_BOUNDARY_CLOCK_CLASS",
            "residual_if_missing": "Delta_clock_boundary_tau",
        },
        {
            "attempt_id": "BCT2599_1_reference_phase_space",
            "clause": "fixed reference and boundary phase space",
            "required_identity": "B_ref/H_ref, orientation and allowed variations are fixed independently of source, radius, clock residuals and fits",
            "attempted_derivation": "delta B_clock=delta B_ref=0 makes tau variation a fixed-boundary variation",
            "current_status": "REFERENCE_AND_PHASE_SPACE_NOT_PARENT_OWNED",
            "residual_if_missing": "Delta_ref_tau;Delta_symp",
        },
        {
            "attempt_id": "BCT2599_2_q_eobs_basic_clock",
            "clause": "q/e_obs-basic clock map",
            "required_identity": "clock normalization is a functor of q/e_obs and not an independent readout frame",
            "attempted_derivation": "Obs_tau(q,e_obs,B_clock) is invariant under vertical representative changes",
            "current_status": "MISSING_Q_OBS_E_CLOCK_BASICNESS",
            "residual_if_missing": "epsilon_tau_frame;epsilon_DObs_e",
        },
        {
            "attempt_id": "BCT2599_3_unique_bulk_extension",
            "clause": "unique extension from boundary to local exterior",
            "required_identity": "boundary-normalized tau extends uniquely into A_ext by stationary/Killing or quasilocal lapse-shift equations",
            "attempted_derivation": "tau_obs|B plus extension law fixes tau_obs in the source collar",
            "current_status": "GENERATOR_EXTENSION_NOT_SOURCED",
            "residual_if_missing": "epsilon_nonstationary_tau",
        },
        {
            "attempt_id": "BCT2599_4_clock_product_not_owner",
            "clause": "clock product versus parent time",
            "required_identity": "clock product bounds constrain drift but do not define Hamiltonian/source tau unless chi_X/Xhat dynamics are parent-owned",
            "attempted_derivation": "tau_clock_time=dchi_X/dt could become tau_obs only after parent Xhat/clock action is signed",
            "current_status": "CLOCK_PRODUCT_BOUND_ONLY",
            "residual_if_missing": "epsilon_clock_tau",
        },
        {
            "attempt_id": "BCT2599_5_same_tau_roles",
            "clause": "source/charge/clock/orbit/boundary same tau",
            "required_identity": "tau_source=tau_charge=tau_clock=tau_orbit=tau_boundary=tau_obs after boundary-clock selection",
            "attempted_derivation": "all role maps factor through the same Obs_tau object",
            "current_status": "MISSING_SAME_TAU_NORMALIZATION_THEOREM",
            "residual_if_missing": "Delta_tau_identity_total",
        },
        {
            "attempt_id": "BCT2599_6_mass_current_and_dynamic_exchange",
            "clause": "mass-current clock leakage",
            "required_identity": "either nabla_(mu tau_nu)=0 in the local collar or parent equations supply the dynamic exchange current that cancels clock leakage",
            "attempted_derivation": "stationary route sets L_tau=0; dynamic route requires parent I_GK=-L_tau",
            "current_status": "DYNAMIC_EXCHANGE_NOT_PARENT_SOURCED",
            "residual_if_missing": "N_delta_tau;B_exchange_mass_channel",
        },
        {
            "attempt_id": "BCT2599_7_mhref_denominator",
            "clause": "denominator lock",
            "required_identity": "M_H_ref=H_tau-H_ref is positive, same-frame and not orbital-GM-derived",
            "attempted_derivation": "delta_tau source pack can only score after denominator lock",
            "current_status": "MISSING_POSITIVE_SAME_FRAME_MHREF",
            "residual_if_missing": "M_H_ref;Delta_ref_tau",
        },
        {
            "attempt_id": "BCT2599_8_verdict",
            "clause": "boundary-clock tau owner verdict",
            "required_identity": "BCT2599_0 through BCT2599_7 close in the same q/e_obs/tau branch",
            "attempted_derivation": "boundary-clock normalized tau becomes the parent-owned source/charge/clock/orbit generator",
            "current_status": "BOUNDARY_CLOCK_TAU_OWNER_NOT_DERIVED_CURRENT_CORPUS",
            "residual_if_missing": "Delta_boundary_clock_tau_total",
        },
    ]
    return [
        with_stamp(
            {
                **row,
                "owner_signed": False,
                "score_ready": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        for row in rows
    ]


def clock_obstruction_rows() -> list[dict[str, Any]]:
    rows = [
        ("CLK2599_0_parent_clock", "parent boundary clock class", "MISSING_PARENT_BOUNDARY_CLOCK_CLASS", "BCS1727_0 says clock maps/bounds exist but no parent class selects Hamiltonian tau", "highest"),
        ("CLK2599_1_clock_product", "clock product bound", "PRODUCT_BOUND_ONLY", "TCN1809 keeps |b_alpha tau_clock_time| as usable nonclaim data, not tau ownership", "medium"),
        ("CLK2599_2_chiX", "chi_X/Xhat dynamics", "MISSING_PARENT_XHAT_CLOCK_DYNAMICS", "TCN1809_2 says chi_X is a closure coordinate only", "high"),
        ("CLK2599_3_common_frame", "common matter/clock frame", "COMMON_FRAME_SIGNATURE_NOT_DERIVED", "TPA2322 makes tau_PPN=1 exact only in a parent-signed branch", "high"),
        ("CLK2599_4_local_stationary", "stationary collar", "ASSUMED_NOT_PROVED", "HYP2558_4 remains an assumed stationary clock", "highest"),
        ("CLK2599_5_dynamic_exchange", "dynamic clock exchange", "MISSING_PARENT_CLOCK_ACTION", "CLK2557_2/4 require a parent clock equation or exchange current", "high"),
        ("CLK2599_6_reference", "reference class", "REFERENCE_SUPERSELECTION_NOT_PARENT_OWNED", "BCS1727_1/2 keep H_ref and phase space unsigned", "highest"),
        ("CLK2599_7_extension", "bulk tau extension", "GENERATOR_EXTENSION_NOT_SOURCED", "BCS1727_3 and LGA1728_1 keep extension/quasilocal data missing", "highest"),
        ("CLK2599_8_stress", "same-frame stress envelope", "MISSING_SAME_FRAME_STRESS_SOURCE_BOUND", "ZTA689_6 and HYP2558_8 leave metric stress/exchange open", "high"),
    ]
    return [
        with_stamp(
            {
                "clock_obstruction_id": obstruction_id,
                "object": obj,
                "status": status,
                "evidence": evidence,
                "priority": priority,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        for obstruction_id, obj, status, evidence, priority in rows
    ]


def delta_tau_source_pack_rows() -> list[dict[str, Any]]:
    rows = [
        ("DTS2599_0_tau_owner", "tau_obs_id", "parent-owned tau_obs identifier and branch q/e_obs/B_clock provenance", "MISSING_TAU_OBS", "identifier", OUT / "P8_Y5_PARENT_QLOC_1727_BOUNDARY_CLOCK_SUPERSELECTION_AUDIT.csv", "no anonymous tau"),
        ("DTS2599_1_boundary_clock", "B_clock", "boundary clock class and normalization rule for tau_obs", "MISSING_BOUNDARY_CLOCK_CLASS", "clock_class_metadata", OUT / "P8_Y5_PARENT_QLOC_1727_BOUNDARY_CLOCK_SUPERSELECTION_AUDIT.csv", "no clock residual backfill"),
        ("DTS2599_2_reference_phase_space", "B_ref_H_ref_phase_space", "reference subtraction, orientation and fixed boundary variation class", "MISSING_REFERENCE_PHASE_SPACE", "boundary_reference_metadata", OUT / "P8_Y5_PARENT_QLOC_1727_BOUNDARY_CLOCK_SUPERSELECTION_AUDIT.csv", "no fitted H_ref"),
        ("DTS2599_3_delta_tau_norm", "epsilon_delta_tau", "fractional moving-time-generator residual at the boundary and/or collar", "MISSING_DELTA_TAU_VALUE_OR_THEOREM_ZERO", "dimensionless", OUT / "P8_Y5_PARENT_QLOC_1727_DELTA_TAU_FIRST_RESIDUAL_ROW.csv", "no delta_tau zero without superselection"),
        ("DTS2599_4_trace", "B_trace", "trace/coherent volume component of symgrad_tau", "MISSING_TRACE_SOURCE_OR_ZERO", "1/time_or_normalized", OUT / "P8_Y5_R10_689_COMPONENT_ZERO_THEOREM_AUDIT.csv", "selector silence alone is not enough"),
        ("DTS2599_5_shear", "B_shear", "tracefree shear component of symgrad_tau", "MISSING_SHEAR_ZERO_THEOREM_OR_BOUND", "1/time_or_normalized", OUT / "P8_Y5_R10_689_COMPONENT_ZERO_THEOREM_AUDIT.csv", "zero trace is not zero shear"),
        ("DTS2599_6_lapse", "B_lapse_acceleration", "lapse/acceleration/clock-normalization contribution", "MISSING_LAPSE_ACCELERATION_GAUGE_SAFE_BOUND", "1/time_or_normalized", OUT / "P8_Y5_R10_688_SYMGRAD_TAU_DECOMPOSITION.csv", "no lapse gauge shortcut"),
        ("DTS2599_7_shift", "B_shift_extrinsic", "shift/extrinsic-curvature contribution to stationarity failure", "MISSING_SHIFT_EXTRINSIC_CURVATURE_BOUND", "1/time_or_normalized", OUT / "P8_Y5_R10_688_SYMGRAD_TAU_DECOMPOSITION.csv", "no ADM convention-only closure"),
        ("DTS2599_8_boundary", "B_boundary_reference", "boundary motion/reference jump contribution", "MISSING_BOUNDARY_MOTION_AND_REFERENCE_SHIFT_BOUND", "boundary_current_or_normalized", OUT / "P8_Y5_PARENT_QLOC_1727_DELTA_TAU_FIRST_RESIDUAL_ROW.csv", "no boundary jump hiding"),
        ("DTS2599_9_roles", "B_tau_role_mismatch", "source/charge/clock/orbit/boundary tau mismatch contribution", "MISSING_SAME_TAU_NORMALIZATION_THEOREM", "dimensionless", OUT / "P8_Y5_TAU_IDENTITY_2597_ROLE_RESIDUAL_ROWS.csv", "no scoring one tau against another"),
        ("DTS2599_10_stress", "T_H_same_frame_envelope", "same-frame stress envelope for contracting symgrad_tau", "MISSING_SAME_FRAME_STRESS_SOURCE_BOUND", "energy_density_or_mass_density", OUT / "P8_Y5_R10_689_COMPONENT_ZERO_THEOREM_AUDIT.csv", "no total-Ward to mass-channel shortcut"),
        ("DTS2599_11_exchange", "B_exchange_mass_channel", "hidden/projector/boundary/domain/coupling exchange leakage", "MISSING_PARENT_EXCHANGE_CURRENT_OR_BOUND", "current_or_mass_units", OUT / "P8_Y5_NO_SHADOW_2558_DYNAMIC_EXCHANGE_LEDGER.csv", "no dynamic closure patch"),
        ("DTS2599_12_C_Tobs_tau", "C_Tobs_tau", "operator norm mapping delta_tau into source-current leakage", "MISSING_TOBS_OPERATOR_NORM", "current_norm_per_tau_norm", OUT / "P8_Y5_PARENT_QLOC_1728_DELTA_TAU_BOUND_COEFFICIENT_ROWS.csv", "no unnormalized numerator"),
        ("DTS2599_13_C_Htau", "C_Htau", "Hamiltonian charge sensitivity to moving tau and reference class", "MISSING_C_HTAU", "dimensionless_per_tau_norm", OUT / "P8_Y5_PARENT_QLOC_1728_DELTA_TAU_BOUND_COEFFICIENT_ROWS.csv", "no EH-only charge"),
        ("DTS2599_14_C_clock_tau", "C_clock_tau", "clock readout sensitivity to delta_tau", "MISSING_C_CLOCK_TAU", "fractional_clock_shift_per_tau_norm", OUT / "P8_Y5_PARENT_QLOC_1728_DELTA_TAU_BOUND_COEFFICIENT_ROWS.csv", "no clock product as generator"),
        ("DTS2599_15_denominator", "M_H_ref", "positive same-frame H_tau-H_ref denominator", "MISSING_POSITIVE_SAME_FRAME_MHREF", "mass_or_energy", OUT / "P8_Y5_TAU_IDENTITY_2597_MHREF_SOURCE_ACQUISITION_ROWS.csv", "no orbital GM denominator"),
        ("DTS2599_16_total", "N_delta_tau_over_MHref", "absolute no-cancellation source pack for epsilon_stationary_tau", "COMPONENTS_MISSING", "dimensionless_after_MHref", OUT / "P8_Y5_STATIONARY_TAU_2598_DELTA_TAU_BOUND_INTERFACE.csv", "no local-GR claim from placeholders"),
    ]

    stamped_rows: list[dict[str, Any]] = []
    for row_id, symbol, definition, current_status, units, source_path, anti_shortcut in rows:
        stamped_rows.append(
            with_stamp(
                {
                    "row_id": row_id,
                    "symbol": symbol,
                    "definition": definition,
                    "current_status": current_status,
                    "numeric_value": f"MISSING_{symbol.upper()}",
                    "units": units,
                    "source_path": source_path,
                    "source_path_exists": source_path.exists(),
                    "anti_shortcut": anti_shortcut,
                    "score_ready": False,
                    "valid_prediction_row": False,
                    "valid_for_claim": False,
                    "claim_allowed": False,
                }
            )
        )
    return stamped_rows


def bound_runner_contract_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "contract_id": "BRC2599_0_identity",
            "object": "source-current identity",
            "formula": "Delta_J_tau <= C_Tobs_tau * epsilon_delta_tau + B_exchange_mass_channel + B_boundary_reference",
            "acceptance": "C_Tobs_tau, epsilon_delta_tau and exchange/boundary terms have units/source paths",
        },
        {
            "contract_id": "BRC2599_1_component_join",
            "object": "symgrad_tau component envelope",
            "formula": "N_delta_tau=sum_abs(B_trace,B_shear,B_lapse,B_shift,B_boundary,B_tau_role_mismatch,T_H_envelope,B_exchange)",
            "acceptance": "absolute no-cancellation join; every component theorem-zero or numeric",
        },
        {
            "contract_id": "BRC2599_2_clock_link",
            "object": "clock product quarantine",
            "formula": "|b_alpha*tau_clock_time| remains a bound row and cannot set tau_obs",
            "acceptance": "clock product only informs C_clock_tau after tau_obs/B_clock owner exists",
        },
        {
            "contract_id": "BRC2599_3_denominator",
            "object": "dimensionless denominator",
            "formula": "epsilon_stationary_tau <= N_delta_tau/M_H_ref",
            "acceptance": "M_H_ref is source-backed, positive, same-frame and not orbital GM",
        },
        {
            "contract_id": "BRC2599_4_score_rule",
            "object": "runner score rule",
            "formula": "accept iff every DTS2599 row is theorem-zero or numeric with units/source path and valid_for_claim=true",
            "acceptance": "current pass must remain false until placeholders are gone",
        },
    ]
    return [
        with_stamp(
            {
                **row,
                "current_status": "SCHEMA_ONLY_NONCLAIM",
                "score_ready": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        for row in rows
    ]


def runner_refusal_rows(owner_rows: list[dict[str, Any]], source_rows: list[dict[str, Any]], contract_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in owner_rows:
        rows.append(
            with_stamp(
                {
                    "runner_id": f"BCR2599_{row['attempt_id']}",
                    "target_id": row["attempt_id"],
                    "target": row["clause"],
                    "verdict": "REFUSED_UNSIGNED_BOUNDARY_CLOCK_TAU_OWNER",
                    "failure_reasons": "OWNER_SIGNED_FALSE;BOUNDARY_CLOCK_OR_EXTENSION_OR_DENOMINATOR_UNSIGNED",
                    "score_ready": False,
                    "claim_allowed": False,
                    "valid_for_claim": False,
                }
            )
        )
    for row in source_rows:
        rows.append(
            with_stamp(
                {
                    "runner_id": f"BCR2599_{row['row_id']}",
                    "target_id": row["row_id"],
                    "target": row["symbol"],
                    "verdict": "REFUSED_NONCLAIM_DELTA_TAU_SOURCE_ROW",
                    "failure_reasons": "VALID_FOR_CLAIM_FALSE;MISSING_NUMERIC_VALUE_OR_THEOREM_ZERO;SOURCE_PACK_NOT_SCORE_READY",
                    "score_ready": False,
                    "claim_allowed": False,
                    "valid_for_claim": False,
                }
            )
        )
    for row in contract_rows:
        rows.append(
            with_stamp(
                {
                    "runner_id": f"BCR2599_{row['contract_id']}",
                    "target_id": row["contract_id"],
                    "target": row["object"],
                    "verdict": "REFUSED_SCHEMA_ONLY_BOUND_CONTRACT",
                    "failure_reasons": "CONTRACT_HAS_MISSING_COMPONENTS_AND_DENOMINATOR",
                    "score_ready": False,
                    "claim_allowed": False,
                    "valid_for_claim": False,
                }
            )
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2599_0_boundary_clock_owner", "boundary-clock normalized tau_obs is parent-owned", "BLOCKED_NONCLAIM", "boundary clock class, reference phase space, q/e_obs basicness and extension are unsigned"),
        ("CG2599_1_clock_product_shortcut", "clock product bound defines tau_obs", "REJECTED_SHORTCUT", "clock data bound b_alpha*tau_clock_time only; it does not own Hamiltonian/source tau"),
        ("CG2599_2_lapse_shortcut", "choose lapse/time coordinate to normalize tau", "REJECTED_SHORTCUT", "lapse is gauge unless fixed by parent clock action and H_tau/H_ref"),
        ("CG2599_3_stationarity_axiom", "assume local stationary collar", "REJECTED_SHORTCUT", "stationary clock is an explicit hypothesis, not proved for current MTS"),
        ("CG2599_4_common_frame_shortcut", "use tau_PPN=1 to identify all tau roles", "REJECTED_SHORTCUT", "tau_PPN=1 is exact only inside a parent-signed common-frame branch"),
        ("CG2599_5_EH_only_or_orbital_GM", "borrow EH charge or fitted orbital GM as denominator", "REJECTED_SHORTCUT", "M_H_ref must be total MTS, positive, same-frame and noncircular"),
        ("CG2599_6_delta_tau_score", "epsilon_stationary_tau is numeric or theorem-zero", "BLOCKED_NONCLAIM", "delta_tau source pack rows carry MISSING values and no denominator"),
        ("CG2599_7_Newton_local_GR", "Newton/local-GR reduction is derived", "BLOCKED_NONCLAIM", "fixed tau, source-normalization denominator, stress/exchange and PPN residual vector remain open"),
    ]
    return [
        with_stamp(
            {
                "gate_id": gate_id,
                "claim": claim,
                "gate_status": status,
                "reason": reason,
                "gate_pass": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        for gate_id, claim, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2599_0_owner_attempt",
            "decision": "BOUNDARY_CLOCK_TAU_OWNER_CONDITIONAL_ONLY",
            "reason": "the superselection theorem shape is exact, but current sources do not parent-own B_clock, B_ref, phase space, or the bulk extension",
            "effect": "tau_obs remains a target object, not a promoted theorem",
        },
        {
            "decision_id": "DEC2599_1_clock_data",
            "decision": "CLOCK_PRODUCT_RETAINED_AS_CONSTRAINT_NOT_GENERATOR",
            "reason": "the atomic-clock product bound is useful evidence but does not define tau_obs or Xhat dynamics",
            "effect": "clock data can constrain C_clock_tau later without closing the local-GR route",
        },
        {
            "decision_id": "DEC2599_2_source_pack",
            "decision": "DELTA_TAU_SOURCE_PACK_STAGED",
            "reason": "if tau ownership fails, the exact current identity gives a boundable numerator with explicit component rows",
            "effect": "future scoring must fill C_Tobs_tau, stress envelope, components, exchange and M_H_ref",
        },
        {
            "decision_id": "DEC2599_3_next",
            "decision": "TOBS_DELTA_TAU_NORM_OR_CLOCK_ACTION_SELECTED_NEXT",
            "reason": "the immediate missing sourceable input is the operator norm C_Tobs_tau/common norm owner; alternatively a parent clock action could close tau ownership at the root",
            "effect": "2600 should derive/source C_Tobs_tau and norm owner, or write the parent boundary-clock action clause",
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False}) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2599_0_selected",
            "selection_status": "selected",
            "target_file": "2600-Y5-R2FR-Tobs-delta-tau-norm-owner-or-boundary-clock-action-clause.md",
            "target_script": "scripts/Y5_R2FR_Tobs_delta_tau_norm_owner_or_boundary_clock_action_clause_2600.py",
            "task": "derive or source the C_Tobs_tau operator norm and common norm owner for Delta_JH_delta_tau; in parallel, attempt the parent boundary-clock action clause that would own B_clock/tau_obs at the root",
            "success_condition": "Delta_JH_delta_tau numerator becomes theorem-zero or source-backed enough for the epsilon_stationary_tau runner to stop being purely schematic",
            "fallback_condition": "nonclaim source rows for T_obs envelope, delta_tau norm, A_ext, current norm, units, and M_H_ref denominator guard",
            "guardrails": "no clock-product shortcut; no lapse gauge cheat; no local stationarity axiom; no EH-only charge; no orbital GM denominator; no Newton/local-GR claim; no GitHub; no formalization-workbench edits",
            "valid_for_claim": False,
        }
    ]
    return [with_stamp(row) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for copy_id, target_path in COPY_TARGETS.items():
        source_path = OUTPUTS[copy_id]
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)
        rows.append(
            with_stamp(
                {
                    "copy_id": f"COPY2599_{copy_id}",
                    "source_path": source_path,
                    "target_path": target_path,
                    "source_exists": source_path.exists(),
                    "target_exists": target_path.exists(),
                    "valid_for_claim": False,
                }
            )
        )
    return rows


def generated_rows_have_no_claim_flags(data: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in data.values():
        for row in rows:
            if row.get("valid_for_claim") is True or row.get("claim_allowed") is True:
                return False
            if row.get("owner_signed") is True or row.get("score_ready") is True:
                return False
    return True


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, condition: bool, notes: str, detail: str = "") -> None:
        rows.append(
            with_stamp(
                {
                    "check_id": check_id,
                    "status": "PASS" if condition else "FAIL",
                    "notes": notes,
                    "detail": detail,
                    "valid_for_claim": False,
                }
            )
        )

    add("VAL2599_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and needles are present")
    required_attempts = {f"BCT2599_{idx}_{name}" for idx, name in [(0, "boundary_clock_class"), (1, "reference_phase_space"), (2, "q_eobs_basic_clock"), (3, "unique_bulk_extension"), (4, "clock_product_not_owner"), (5, "same_tau_roles"), (6, "mass_current_and_dynamic_exchange"), (7, "mhref_denominator"), (8, "verdict")]}
    add("VAL2599_01_owner_attempt_complete", required_attempts.issubset({row["attempt_id"] for row in data["owner_attempt"]}), "boundary-clock tau owner attempt covers all required clauses")
    add(
        "VAL2599_02_owner_not_promoted",
        any(row["attempt_id"] == "BCT2599_8_verdict" and row["current_status"] == "BOUNDARY_CLOCK_TAU_OWNER_NOT_DERIVED_CURRENT_CORPUS" for row in data["owner_attempt"])
        and all(row["owner_signed"] is False for row in data["owner_attempt"]),
        "boundary-clock tau owner remains conditional and nonclaim",
    )
    add("VAL2599_03_clock_obstructions_complete", len(data["clock_obstruction"]) >= 8 and all(row["claim_allowed"] is False for row in data["clock_obstruction"]), "clock obstruction ledger records active blockers")
    required_symbols = {"tau_obs_id", "B_clock", "B_ref_H_ref_phase_space", "epsilon_delta_tau", "B_trace", "B_shear", "B_lapse_acceleration", "B_shift_extrinsic", "B_boundary_reference", "B_tau_role_mismatch", "T_H_same_frame_envelope", "B_exchange_mass_channel", "C_Tobs_tau", "C_Htau", "C_clock_tau", "M_H_ref", "N_delta_tau_over_MHref"}
    add("VAL2599_04_delta_source_pack_complete", required_symbols.issubset({row["symbol"] for row in data["source_pack"]}), "delta_tau source pack covers owner, components, coefficients, stress, exchange and denominator")
    add("VAL2599_05_source_paths_exist", all(row["source_path_exists"] is True for row in data["source_pack"]), "delta_tau source pack rows point to existing local files")
    required_contracts = {"source-current identity", "symgrad_tau component envelope", "clock product quarantine", "dimensionless denominator", "runner score rule"}
    add("VAL2599_06_bound_runner_contract_complete", required_contracts.issubset({row["object"] for row in data["bound_contract"]}), "bound runner contract covers identity, component join, clock quarantine, denominator and score rule")
    add("VAL2599_07_rows_nonclaim", all(row["score_ready"] is False and row["valid_for_claim"] is False for row in data["source_pack"]) and all(row["score_ready"] is False for row in data["bound_contract"]), "all source-pack and bound-contract rows remain non-score-ready and nonclaim")
    add("VAL2599_08_runner_refuses", all(row["score_ready"] is False and row["claim_allowed"] is False for row in data["runner_refusal"]), "runner refuses unsigned owner/source/contract rows")
    add(
        "VAL2599_09_claim_gates_safe",
        all(row["claim_allowed"] is False for row in data["claim_gates"])
        and any(row["gate_id"] == "CG2599_1_clock_product_shortcut" and row["gate_status"] == "REJECTED_SHORTCUT" for row in data["claim_gates"])
        and any(row["gate_id"] == "CG2599_3_stationarity_axiom" and row["gate_status"] == "REJECTED_SHORTCUT" for row in data["claim_gates"]),
        "clock-product/lapse/stationarity/common-frame/EH-or-GM shortcuts and local-GR claims remain blocked",
    )
    add("VAL2599_10_no_claim_flags", generated_rows_have_no_claim_flags(data), "no generated row sets owner, scoring, or claim flags true")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in (
            "*2599-Y5-R2FR-boundary-clock*",
            "*Y5_R2FR_boundary_clock*2599*",
            "*P8_Y5_BOUNDARY_CLOCK_TAU_2599*",
            "*JR2599*",
        ):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add("VAL2599_11_no_formalization_artifacts", not formalization_artifacts, "no 2599 artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_artifacts))
    add("VAL2599_12_next_selected", any(row["route_id"] == "NEXT2599_0_selected" and "2600-Y5-R2FR-Tobs-delta-tau-norm-owner" in row["target_file"] for row in data["next"]), "2600 Tobs delta_tau norm/boundary-clock action target selected")
    add("VAL2599_13_branch_copies", all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]), "nonclaim branch copies exist")

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2599_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2599_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2599_OVERALL",
        overall,
        "2599 keeps boundary-clock tau ownership conditional, quarantines clock-product shortcuts, stages the delta_tau source pack, and selects C_Tobs_tau/norm owner or clock-action clause next",
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for row in rows:
        values = [row_value(row.get(column, "")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2599 Y5 R2FR boundary clock normalized tau owner or delta tau source pack",
        "",
        "**Status:** private nonclaim derivation checkpoint. The boundary-clock route gives the right theorem shape, but current MTS does not yet parent-own the boundary clock/reference phase space or the bulk extension that would make `tau_obs` a fixed generator.",
        "",
        "**Main result:** a clock product bound is useful evidence, not a time-generator theorem. `B_clock` can fix `tau_obs` only after the parent action supplies the boundary-clock class, fixed reference/phase space, q/e_obs-basic clock map, and a unique stationary/quasilocal extension. Since those clauses remain unsigned, 2599 stages the first full `delta_tau` source pack for `epsilon_stationary_tau <= N_delta_tau/M_H_ref`.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role", "valid_for_claim"]),
        "",
        "## Boundary Clock Tau Owner Attempt",
        markdown_table(data["owner_attempt"], ["attempt_id", "clause", "required_identity", "attempted_derivation", "current_status", "residual_if_missing", "owner_signed", "score_ready", "valid_for_claim", "claim_allowed"]),
        "",
        "## Clock Obstruction Ledger",
        markdown_table(data["clock_obstruction"], ["clock_obstruction_id", "object", "status", "evidence", "priority", "valid_for_claim", "claim_allowed"]),
        "",
        "## Delta Tau Source Pack",
        markdown_table(data["source_pack"], ["row_id", "symbol", "definition", "current_status", "numeric_value", "units", "source_path", "source_path_exists", "anti_shortcut", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Bound Runner Contract",
        markdown_table(data["bound_contract"], ["contract_id", "object", "formula", "acceptance", "current_status", "score_ready", "valid_for_claim", "claim_allowed"]),
        "",
        "## Runner Refusal",
        markdown_table(data["runner_refusal"], ["runner_id", "target_id", "target", "verdict", "failure_reasons", "score_ready", "claim_allowed", "valid_for_claim"]),
        "",
        "## Claim Gates",
        markdown_table(data["claim_gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "valid_for_claim", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect", "valid_for_claim"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "success_condition", "fallback_condition", "guardrails", "valid_for_claim"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists", "valid_for_claim"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail", "valid_for_claim"]),
        "",
        "## Practical Status",
        "",
        "This is the honest fork. Either the parent action gives a boundary-clock class that owns `tau_obs`, or the theory pays the moving-clock bill through `C_Tobs_tau`, stress, exchange, boundary, and denominator rows. That is not glamorous, but it is how this becomes derivable rather than hand-waved.",
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)

    owner_rows = owner_attempt_rows()
    source_pack = delta_tau_source_pack_rows()
    bound_contract = bound_runner_contract_rows()
    data = {
        "sources": source_register_rows(),
        "owner_attempt": owner_rows,
        "clock_obstruction": clock_obstruction_rows(),
        "source_pack": source_pack,
        "bound_contract": bound_contract,
        "runner_refusal": runner_refusal_rows(owner_rows, source_pack, bound_contract),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["owner_attempt"], data["owner_attempt"])
    write_csv(OUTPUTS["clock_obstruction"], data["clock_obstruction"])
    write_csv(OUTPUTS["delta_tau_source_pack"], data["source_pack"])
    write_csv(OUTPUTS["bound_runner_contract"], data["bound_contract"])
    write_csv(OUTPUTS["runner_refusal"], data["runner_refusal"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])

    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])

    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)

    overall = next(row for row in data["validations"] if row["check_id"] == "VAL2599_OVERALL")
    print(f"{overall['check_id']} {overall['status']}: {overall['notes']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

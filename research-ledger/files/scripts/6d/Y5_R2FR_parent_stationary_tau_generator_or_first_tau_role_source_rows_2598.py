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

BRANCH_ID = "MTS_R2FR_PARENT_STATIONARY_TAU_2598"
CHECKPOINT_ID = "2598"

DOC = ROOT / "2598-Y5-R2FR-parent-stationary-tau-generator-or-first-tau-role-source-rows.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_STATIONARY_TAU_2598_SOURCE_REGISTER.csv",
    "theorem_attempt": OUT / "P8_Y5_STATIONARY_TAU_2598_THEOREM_ATTEMPT.csv",
    "obstruction_matrix": OUT / "P8_Y5_STATIONARY_TAU_2598_OBSTRUCTION_MATRIX.csv",
    "source_rows": OUT / "P8_Y5_STATIONARY_TAU_2598_SOURCE_ROWS.csv",
    "bound_interface": OUT / "P8_Y5_STATIONARY_TAU_2598_DELTA_TAU_BOUND_INTERFACE.csv",
    "runner_refusal": OUT / "P8_Y5_STATIONARY_TAU_2598_RUNNER_REFUSAL.csv",
    "claim_gates": OUT / "P8_Y5_STATIONARY_TAU_2598_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_STATIONARY_TAU_2598_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_STATIONARY_TAU_2598_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_STATIONARY_TAU_2598_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2598_VALIDATION.csv",
}

COPY_TARGETS = {
    "theorem_attempt": QUEUE / "JR2598_PARENT_STATIONARY_TAU_THEOREM_ATTEMPT_NONCLAIM.csv",
    "source_rows": LOCAL_BOUNDS / "Parent_stationary_tau_source_rows_2598_NONCLAIM.csv",
    "bound_interface": LOCAL_BOUNDS / "Delta_tau_bound_interface_2598_NONCLAIM.csv",
    "next_target": QUEUE / "JR2598_BOUNDARY_CLOCK_TAU_OR_DELTA_TAU_SOURCE_PACK_NEXT.csv",
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
            "source_id": "SRC2598_00_2597_handoff",
            "source_path": ROOT / "2597-Y5-R2FR-tau-identity-source-charge-clock-orbit-or-MHref-source-acquisition.md",
            "needles": ["NEXT2597_0_selected", "TIA2597_1_stationary_generator", "VAL2597_OVERALL"],
            "role": "active handoff selecting parent stationary tau or first tau-role source rows",
        },
        {
            "source_id": "SRC2598_01_2597_next_queue",
            "source_path": QUEUE / "JR2597_PARENT_STATIONARY_TAU_OR_SOURCE_ROWS_NEXT.csv",
            "needles": ["NEXT2597_0_selected", "2598-Y5-R2FR-parent-stationary-tau-generator-or-first-tau-role-source-rows.md"],
            "role": "machine-readable 2598 target and guardrails",
        },
        {
            "source_id": "SRC2598_02_2597_theorem",
            "source_path": OUT / "P8_Y5_TAU_IDENTITY_2597_THEOREM_AUDIT.csv",
            "needles": ["TIA2597_0_parent_tau_definition", "TIA2597_8_verdict"],
            "role": "one-tau theorem audit feeding stationary tau definition",
        },
        {
            "source_id": "SRC2598_03_686_stationary_certificate",
            "source_path": OUT / "P8_Y5_R10_686_LOCAL_STATIONARY_CERTIFICATE.csv",
            "needles": ["LSC686_1_stationary_solution", "LSC686_7_verdict"],
            "role": "local stationary/Killing certificate attempt",
        },
        {
            "source_id": "SRC2598_04_687_selector_to_tau",
            "source_path": OUT / "P8_Y5_R10_687_SELECTOR_TO_TAU_THEOREM_ATTEMPT.csv",
            "needles": ["STT687_3_Killing_upgrade", "STT687_5_verdict"],
            "role": "selector-to-stationary-generator no-go/contract",
        },
        {
            "source_id": "SRC2598_05_688_symgrad",
            "source_path": OUT / "P8_Y5_R10_688_SYMGRAD_TAU_DECOMPOSITION.csv",
            "needles": ["SGT688_0_exact_congruence_identity", "SGT688_6_tau_role_mismatch"],
            "role": "kinematic decomposition of nonstationary tau obstruction",
        },
        {
            "source_id": "SRC2598_06_689_zero_audit",
            "source_path": OUT / "P8_Y5_R10_689_COMPONENT_ZERO_THEOREM_AUDIT.csv",
            "needles": ["ZTA689_0_theta", "ZTA689_5_tau_mismatch", "ZTA689_6_stress_envelope"],
            "role": "component zero-theorem audit and fallback rows",
        },
        {
            "source_id": "SRC2598_07_1728_quasilocal",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1728_STATIONARY_QUASILOCAL_CERTIFICATE_ATTEMPT.csv",
            "needles": ["LGA1728_0_exact_symmetry_route", "LGA1728_3_verdict"],
            "role": "quasilocal stationary generator certificate attempt",
        },
        {
            "source_id": "SRC2598_08_2067_tau_owner",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_2067_STATIONARY_TAU_OWNER_ATTEMPT.csv",
            "needles": ["STO2067_0_tau_obs_owner", "STO2067_7_verdict"],
            "role": "stationary tau owner attempt and cap bridge blocker",
        },
        {
            "source_id": "SRC2598_09_2468_stationary_source",
            "source_path": OUT / "P8_Y5_STATIONARY_SOURCE_2468_THEOREM_HYPOTHESES.csv",
            "needles": ["HYP2468_4_stationary_clock", "HYP2468_6_projector_owned"],
            "role": "stationary local source theorem hypotheses remain assumptions",
        },
        {
            "source_id": "SRC2598_10_2558_stationary_source",
            "source_path": OUT / "P8_Y5_NO_SHADOW_2558_STATIONARY_THEOREM_HYPOTHESES.csv",
            "needles": ["HYP2558_4_stationary_clock", "HYP2558_6_projector_owned"],
            "role": "later no-shadow stationary source theorem hypotheses remain assumptions",
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


def theorem_attempt_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "attempt_id": "STA2598_0_tau_obs_object",
            "premise": "parent tau object",
            "required_identity": "tau_obs=Obs_tau(q(Phi), e_obs, B_clock) is selected before source/readout fitting",
            "mathematical_form": "Obs_tau is q-basic and boundary-clock normalized on the local branch",
            "current_status": "MISSING_PARENT_TAU_OBS_OWNER",
            "if_closed": "all tau role rows can compare to one parent object",
            "residual_if_missing": "epsilon_tau_frame;epsilon_tau_selector",
        },
        {
            "attempt_id": "STA2598_1_stationary_exterior",
            "premise": "stationary exterior",
            "required_identity": "Lie_tau g_obs=0 through the local source plus exterior collar",
            "mathematical_form": "nabla_(mu tau_nu)=0 or all symgrad_tau components are theorem-zero/bounded",
            "current_status": "MISSING_LOCAL_STATIONARY_KILLING_CERTIFICATE",
            "if_closed": "Killing current route can conserve the mass/source current",
            "residual_if_missing": "epsilon_nonstationary_tau",
        },
        {
            "attempt_id": "STA2598_2_exact_current_identity",
            "premise": "Killing/source-current identity",
            "required_identity": "J_tau^mu=T_H^{mu nu}tau_nu has divergence controlled by stress exchange plus symgrad_tau",
            "mathematical_form": "div J_tau=(div T_H).tau + T_H^{mu nu} nabla_(mu tau_nu)",
            "current_status": "EXACT_IDENTITY_AVAILABLE_NOT_ZERO_THEOREM",
            "if_closed": "nonstationarity becomes an explicit numerator instead of a vague closure",
            "residual_if_missing": "N_delta_tau_source_current",
        },
        {
            "attempt_id": "STA2598_3_component_zero_stack",
            "premise": "symgrad_tau component silence",
            "required_identity": "trace, shear, lapse/acceleration, shift/extrinsic, boundary and tau-role mismatch are zero or source-bounded",
            "mathematical_form": "symgrad_tau decomposes into component envelope N_tau",
            "current_status": "COMPONENT_ZERO_THEOREMS_NOT_DERIVED",
            "if_closed": "epsilon_nonstationary_tau can be bounded in a denominator-safe way",
            "residual_if_missing": "B_trace;B_shear;B_lapse;B_shift;B_boundary;B_tau_mismatch",
        },
        {
            "attempt_id": "STA2598_4_same_tau_roles",
            "premise": "same tau role lock",
            "required_identity": "tau_source=tau_charge=tau_clock=tau_orbit=tau_boundary=tau_obs",
            "mathematical_form": "all role maps factor through Obs_tau(q,e_obs,B_clock)",
            "current_status": "MISSING_SAME_TAU_NORMALIZATION_THEOREM",
            "if_closed": "stationarity in one tau cannot be scored against another tau",
            "residual_if_missing": "Delta_tau_identity_total",
        },
        {
            "attempt_id": "STA2598_5_mass_channel_conservation",
            "premise": "same-frame mass-channel conservation",
            "required_identity": "div T_H=0 in the relevant projected mass channel, or every exchange term is retained",
            "mathematical_form": "Pi_M(exchange_hidden+projector+boundary+domain+coupling)=0 or bounded",
            "current_status": "MISSING_MASS_CHANNEL_EXCHANGE_SILENCE",
            "if_closed": "current divergence reduces to only the symgrad_tau term",
            "residual_if_missing": "B_exchange_mass_channel",
        },
        {
            "attempt_id": "STA2598_6_hamiltonian_reference",
            "premise": "Hamiltonian/reference lock",
            "required_identity": "theta_MTS, Q_tau, H_tau, H_ref and M_H_ref are integrable and fixed in the same tau branch",
            "mathematical_form": "delta H_tau=int_S(delta Q_tau-i_tau theta_MTS); M_H_ref=H_tau-H_ref",
            "current_status": "MISSING_THETA_QTAU_HREF_MHREF_LOCK",
            "if_closed": "epsilon_tau and source-current residuals receive a noncircular denominator",
            "residual_if_missing": "M_H_ref;delta_H_tau_curl;Delta_ref_tau",
        },
        {
            "attempt_id": "STA2598_7_verdict",
            "premise": "parent stationary tau theorem",
            "required_identity": "STA2598_0 through STA2598_6 close in one q/e_obs/boundary-clock branch",
            "mathematical_form": "parent stationary tau_obs theorem with denominator-safe source-current bridge",
            "current_status": "PARENT_STATIONARY_TAU_NOT_DERIVED_CURRENT_CORPUS",
            "if_closed": "local source-normalization/GR route can reopen downstream",
            "residual_if_missing": "Delta_stationary_tau_total",
        },
    ]
    return [
        with_stamp(
            {
                **row,
                "theorem_signed": False,
                "score_ready": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        for row in rows
    ]


def obstruction_rows() -> list[dict[str, Any]]:
    rows = [
        ("OBS2598_0_tau_owner", "tau_obs owner", "MISSING_PARENT_TAU_OBS_OWNER", "TGC685_0/STO2067_0 remain definition target only", "highest"),
        ("OBS2598_1_domain_owner", "parent domain/source owner", "MISSING_PARENT_DOMAIN_AND_SOURCE_OWNER", "LSC686_0 and STO2067_4 leave the branch/domain conditional", "high"),
        ("OBS2598_2_killing", "stationary/Killing exterior", "MISSING_LOCAL_STATIONARY_KILLING_CERTIFICATE", "LSC686_1/STO2067_1 explicitly block the theorem-zero route", "highest"),
        ("OBS2598_3_selector_gap", "selector silence to Killing upgrade", "COUNTEREXAMPLE_BLOCK", "STT687_3 says scalar/selector silence is not full stationarity", "high"),
        ("OBS2598_4_trace", "trace or coherent volume piece", "CONDITIONAL_ONLY", "ZTA689_0 is promising but not closed", "medium"),
        ("OBS2598_5_shear", "tracefree shear", "MISSING_SHEAR_ZERO_THEOREM_OR_BOUND", "SGT688_2/ZTA689_1 make shear the sharp counterexample", "highest"),
        ("OBS2598_6_lapse", "lapse/acceleration", "MISSING_LAPSE_ACCELERATION_GAUGE_SAFE_BOUND", "clock/lapse normalization is gauge-dangerous without parent coupling", "high"),
        ("OBS2598_7_boundary", "boundary/reference motion", "MISSING_BOUNDARY_MOTION_AND_REFERENCE_SHIFT_BOUND", "H_ref and boundary class are not fixed enough for a denominator", "high"),
        ("OBS2598_8_tau_roles", "same tau role lock", "MISSING_SAME_TAU_NORMALIZATION_THEOREM", "2597/TGC685_6 keep source/charge/clock/orbit/boundary unsigned", "highest"),
        ("OBS2598_9_stress", "same-frame stress envelope", "MISSING_MASS_CHANNEL_EXCHANGE_SILENCE", "Ward total conservation does not prove mass-channel silence", "high"),
        ("OBS2598_10_denominator", "same-frame denominator", "MISSING_POSITIVE_SAME_FRAME_MHREF", "M_H_ref remains nonclaim and source-acquisition only", "highest"),
    ]
    return [
        with_stamp(
            {
                "obstruction_id": obstruction_id,
                "object": obj,
                "current_status": status,
                "evidence": evidence,
                "priority": priority,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        for obstruction_id, obj, status, evidence, priority in rows
    ]


def source_rows() -> list[dict[str, Any]]:
    rows = [
        ("STS2598_0_tau_obs", "tau_obs_owner", "parent-selected tau_obs=Obs_tau(q,e_obs,B_clock)", "MISSING_PARENT_TAU_OBS_OWNER", OUT / "P8_Y5_PARENT_QLOC_2067_STATIONARY_TAU_OWNER_ATTEMPT.csv", "no post-readout tau label"),
        ("STS2598_1_boundary_clock", "boundary_clock_normalization", "boundary clock/lapse normalization fixes tau_obs before source/readout", "MISSING_BOUNDARY_CLOCK_NORMALIZATION", OUT / "P8_Y5_PARENT_QLOC_1728_STATIONARY_QUASILOCAL_CERTIFICATE_ATTEMPT.csv", "no homogeneous lapse shortcut"),
        ("STS2598_2_qbasic", "q_basic_tau", "tau_obs and e_obs are q-basic in the same parent branch", "MISSING_Q_OBS_E_TAU_BASICNESS", OUT / "P8_Y5_OBS_STACK_2588_OWNER_CERTIFICATE.csv", "no projection-by-declaration"),
        ("STS2598_3_stationary", "stationary_exterior", "Lie_tau g_obs=0 or symgrad_tau source envelope is supplied", "MISSING_LOCAL_STATIONARY_KILLING_CERTIFICATE", OUT / "P8_Y5_R10_686_LOCAL_STATIONARY_CERTIFICATE.csv", "no local stationarity axiom"),
        ("STS2598_4_trace", "B_trace", "trace/coherent volume component of symgrad_tau", "MISSING_PARENT_DOMAIN_SELECTION_AND_XD_ZERO_SOURCE", OUT / "P8_Y5_R10_689_COMPONENT_ZERO_THEOREM_AUDIT.csv", "selector silence alone is not enough"),
        ("STS2598_5_shear", "B_shear", "tracefree shear component of symgrad_tau", "MISSING_SHEAR_ZERO_THEOREM_OR_BOUND", OUT / "P8_Y5_R10_688_SYMGRAD_TAU_DECOMPOSITION.csv", "zero trace is not zero shear"),
        ("STS2598_6_lapse", "B_lapse_acceleration", "lapse/acceleration component with clock-safe normalization", "MISSING_LAPSE_ACCELERATION_GAUGE_SAFE_BOUND", OUT / "P8_Y5_R10_688_SYMGRAD_TAU_DECOMPOSITION.csv", "no clock/lapse gauge cheat"),
        ("STS2598_7_shift", "B_shift_extrinsic", "shift/extrinsic-curvature component of stationarity failure", "MISSING_SHIFT_EXTRINSIC_CURVATURE_BOUND", OUT / "P8_Y5_R10_688_SYMGRAD_TAU_DECOMPOSITION.csv", "no ADM convention without source"),
        ("STS2598_8_boundary", "B_boundary_reference", "boundary motion and fixed-reference drift component", "MISSING_BOUNDARY_MOTION_AND_REFERENCE_SHIFT_BOUND", OUT / "P8_Y5_R10_688_SYMGRAD_TAU_DECOMPOSITION.csv", "no fitted H_ref"),
        ("STS2598_9_roles", "B_tau_role_mismatch", "source/charge/clock/orbit/boundary tau mismatch component", "MISSING_SAME_TAU_NORMALIZATION_THEOREM", OUT / "P8_Y5_TAU_IDENTITY_2597_ROLE_RESIDUAL_ROWS.csv", "no scoring one tau against another"),
        ("STS2598_10_stress", "T_H_same_frame_envelope", "same-frame stress/current envelope for contracting symgrad_tau", "MISSING_SAME_FRAME_STRESS_SOURCE_BOUND", OUT / "P8_Y5_R10_689_COMPONENT_ZERO_THEOREM_AUDIT.csv", "no total-Ward-to-mass-channel shortcut"),
        ("STS2598_11_hamiltonian", "H_tau_integrability", "theta_MTS/Q_tau/H_tau integrability in same tau branch", "MISSING_THETA_QTAU_HREF_MHREF_LOCK", OUT / "P8_Y5_TAU_IDENTITY_2597_MHREF_SOURCE_ACQUISITION_ROWS.csv", "no EH-only charge"),
        ("STS2598_12_denominator", "M_H_ref_denominator", "positive same-frame M_H_ref=H_tau-H_ref", "MISSING_POSITIVE_SAME_FRAME_MHREF", OUT / "P8_Y5_TAU_IDENTITY_2597_MHREF_SOURCE_ACQUISITION_ROWS.csv", "no orbital GM denominator"),
        ("STS2598_13_acceptance", "stationary_tau_acceptance", "all rows source-backed, units-compatible and theorem-zero or numeric", "BLOCKED_NONCLAIM", OUT / "P8_Y5_TAU_IDENTITY_2597_THEOREM_AUDIT.csv", "no local-GR promotion from placeholders"),
    ]

    stamped_rows: list[dict[str, Any]] = []
    for row_id, field, required_input, current_status, source_path, anti_shortcut in rows:
        stamped_rows.append(
            with_stamp(
                {
                    "row_id": row_id,
                    "field": field,
                    "required_input": required_input,
                    "current_status": current_status,
                    "source_path": source_path,
                    "source_path_exists": source_path.exists(),
                    "units": "source_schema_or_bound",
                    "anti_shortcut": anti_shortcut,
                    "score_ready": False,
                    "valid_prediction_row": False,
                    "valid_for_claim": False,
                    "claim_allowed": False,
                }
            )
        )
    return stamped_rows


def bound_interface_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "interface_id": "DTB2598_0_current_identity",
            "quantity": "div_J_tau",
            "definition": "exact source-current leakage identity for a moving tau",
            "formula": "div_J_tau=(div_T_H).tau + T_H_contract_symgrad_tau",
            "needed_inputs": "same-frame T_H; tau_obs; exchange-current ledger; integration domain",
        },
        {
            "interface_id": "DTB2598_1_numerator",
            "quantity": "N_delta_tau",
            "definition": "absolute numerator from stress contraction, exchange leakage and boundary/reference terms",
            "formula": "abs_int(T_H_contract_symgrad_tau)+B_exchange+B_boundary+B_ref",
            "needed_inputs": "B_trace;B_shear;B_lapse;B_shift;B_boundary;B_tau_role_mismatch;T_H envelope",
        },
        {
            "interface_id": "DTB2598_2_denominator",
            "quantity": "M_H_ref",
            "definition": "same-frame positive Hamiltonian/reference denominator",
            "formula": "M_H_ref=H_tau-H_ref",
            "needed_inputs": "theta_MTS;Q_tau_MTS;H_tau;H_ref;fixed surfaces;integrability",
        },
        {
            "interface_id": "DTB2598_3_dimensionless_bound",
            "quantity": "epsilon_stationary_tau",
            "definition": "dimensionless bound replacing theorem-zero stationary tau if the proof fails",
            "formula": "epsilon_stationary_tau <= N_delta_tau / M_H_ref",
            "needed_inputs": "N_delta_tau and M_H_ref both source-backed with compatible units",
        },
        {
            "interface_id": "DTB2598_4_runner_acceptance",
            "quantity": "stationary_tau_score_rule",
            "definition": "runner only scores if every component is theorem-zero or numeric with source path and units",
            "formula": "accept iff no MISSING markers and no circular denominator",
            "needed_inputs": "all STS2598 rows pass in same q/e_obs/tau branch",
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


def runner_refusal_rows(theorem_rows: list[dict[str, Any]], source_data: list[dict[str, Any]], bound_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in theorem_rows:
        rows.append(
            with_stamp(
                {
                    "runner_id": f"STR2598_{row['attempt_id']}",
                    "target_id": row["attempt_id"],
                    "target": row["premise"],
                    "verdict": "REFUSED_UNSIGNED_STATIONARY_TAU_THEOREM",
                    "failure_reasons": "THEOREM_SIGNED_FALSE;MISSING_PARENT_TAU_OWNER_OR_COMPONENT_ZERO_STACK",
                    "score_ready": False,
                    "claim_allowed": False,
                    "valid_for_claim": False,
                }
            )
        )
    for row in source_data:
        rows.append(
            with_stamp(
                {
                    "runner_id": f"STR2598_{row['row_id']}",
                    "target_id": row["row_id"],
                    "target": row["field"],
                    "verdict": "REFUSED_NONCLAIM_SOURCE_ROW",
                    "failure_reasons": "VALID_FOR_CLAIM_FALSE;MISSING_SOURCE_BACKED_VALUE_OR_ZERO_THEOREM",
                    "score_ready": False,
                    "claim_allowed": False,
                    "valid_for_claim": False,
                }
            )
        )
    for row in bound_rows:
        rows.append(
            with_stamp(
                {
                    "runner_id": f"STR2598_{row['interface_id']}",
                    "target_id": row["interface_id"],
                    "target": row["quantity"],
                    "verdict": "REFUSED_SCHEMA_ONLY_BOUND_INTERFACE",
                    "failure_reasons": "BOUND_INTERFACE_HAS_MISSING_COMPONENTS_AND_DENOMINATOR",
                    "score_ready": False,
                    "claim_allowed": False,
                    "valid_for_claim": False,
                }
            )
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2598_0_stationary_tau_claim", "parent stationary tau_obs is derived", "BLOCKED_NONCLAIM", "tau owner, Killing exterior, same-tau roles, stress channel, Hamiltonian/reference lock are unsigned"),
        ("CG2598_1_local_stationarity_axiom", "assume local stationarity in the tested exterior", "REJECTED_SHORTCUT", "stationarity must be parent-selected or source-bounded, not inserted as a plateau axiom"),
        ("CG2598_2_selector_silence_to_Killing", "selector or trace silence implies Killing", "REJECTED_SHORTCUT", "trace/selector silence does not kill shear, lapse, shift, boundary motion or tau-role mismatch"),
        ("CG2598_3_lapse_clock_shortcut", "choose a lapse/time coordinate to normalize tau", "REJECTED_SHORTCUT", "clock/lapse normalization must couple to H_tau and H_ref from the parent action"),
        ("CG2598_4_EH_only_exterior", "borrow EH stationary exterior machinery as total MTS proof", "REJECTED_SHORTCUT", "retained MTS sectors and exchanges must be zeroed, bounded or explicitly included"),
        ("CG2598_5_orbital_GM_denominator", "use fitted orbital GM as M_H_ref denominator", "REJECTED_SHORTCUT", "orbital GM is an output of the source-transfer theorem, not an input"),
        ("CG2598_6_Newton_local_GR", "claim Newton/local-GR reduction", "BLOCKED_NONCLAIM", "stationary tau and M_H_ref denominator locks are upstream and unclosed"),
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
            "decision_id": "DEC2598_0_exact_route_retained",
            "decision": "KILLING_CURRENT_ROUTE_IS_REAL_BUT_CONDITIONAL",
            "reason": "div J_tau identity is exact and useful, but it requires parent tau owner plus same-frame stress and stationarity",
            "effect": "do not discard the route; keep it as the cleanest derivation spine",
        },
        {
            "decision_id": "DEC2598_1_no_theorem_zero",
            "decision": "PARENT_STATIONARY_TAU_NOT_DERIVED",
            "reason": "selector silence, clock normalization, and EH intuition do not prove full symgrad_tau=0",
            "effect": "epsilon_stationary_tau remains retained rather than theorem-zero",
        },
        {
            "decision_id": "DEC2598_2_bound_interface",
            "decision": "DELTA_TAU_BOUND_INTERFACE_WRITTEN",
            "reason": "if the theorem fails, the same identity gives a sourceable numerator and denominator interface",
            "effect": "future work can bound the damage instead of arguing qualitatively",
        },
        {
            "decision_id": "DEC2598_3_next",
            "decision": "BOUNDARY_CLOCK_TAU_OWNER_OR_DELTA_TAU_SOURCE_PACK_SELECTED_NEXT",
            "reason": "the first missing clause is the actual tau_obs owner; if that fails again, source the delta_tau numerator components directly",
            "effect": "2599 should attempt boundary-clock normalized tau ownership or fill the first source-backed delta_tau source pack",
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False}) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2598_0_selected",
            "selection_status": "selected",
            "target_file": "2599-Y5-R2FR-boundary-clock-normalized-tau-owner-or-delta-tau-source-pack.md",
            "target_script": "scripts/Y5_R2FR_boundary_clock_normalized_tau_owner_or_delta_tau_source_pack_2599.py",
            "task": "derive tau_obs as a q/e_obs-basic boundary-clock-normalized parent generator; if that fails, fill the first source-backed delta_tau numerator rows for trace, shear, lapse, shift, boundary, tau-role mismatch and same-frame stress",
            "success_condition": "tau_obs owner becomes source-backed enough for role residuals to be theorem-zero/bounded, or epsilon_stationary_tau has a nonclaim source-pack runner interface",
            "fallback_condition": "nonclaim component rows with units, source paths, numerator formula, M_H_ref denominator guard and no-cancellation acceptance",
            "guardrails": "no local stationarity axiom; no selector-to-Killing shortcut; no lapse gauge cheat; no EH-only exterior; no orbital GM denominator; no Newton/local-GR claim; no GitHub; no formalization-workbench edits",
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
                    "copy_id": f"COPY2598_{copy_id}",
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
            if row.get("theorem_signed") is True or row.get("score_ready") is True:
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

    add("VAL2598_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and needles are present")
    required_attempts = {f"STA2598_{idx}_{name}" for idx, name in [(0, "tau_obs_object"), (1, "stationary_exterior"), (2, "exact_current_identity"), (3, "component_zero_stack"), (4, "same_tau_roles"), (5, "mass_channel_conservation"), (6, "hamiltonian_reference"), (7, "verdict")]}
    add("VAL2598_01_theorem_attempt_complete", required_attempts.issubset({row["attempt_id"] for row in data["theorem_attempt"]}), "stationary tau theorem attempt covers owner, Killing, identity, components, roles, stress and denominator")
    add(
        "VAL2598_02_theorem_not_promoted",
        any(row["attempt_id"] == "STA2598_7_verdict" and row["current_status"] == "PARENT_STATIONARY_TAU_NOT_DERIVED_CURRENT_CORPUS" for row in data["theorem_attempt"])
        and all(row["theorem_signed"] is False for row in data["theorem_attempt"]),
        "stationary tau theorem remains unsigned",
    )
    add("VAL2598_03_obstruction_matrix_complete", len(data["obstructions"]) >= 10 and all(row["claim_allowed"] is False for row in data["obstructions"]), "obstruction matrix records the active blockers")
    required_source_fields = {"tau_obs_owner", "boundary_clock_normalization", "q_basic_tau", "stationary_exterior", "B_trace", "B_shear", "B_lapse_acceleration", "B_shift_extrinsic", "B_boundary_reference", "B_tau_role_mismatch", "T_H_same_frame_envelope", "H_tau_integrability", "M_H_ref_denominator", "stationary_tau_acceptance"}
    add("VAL2598_04_source_rows_complete", required_source_fields.issubset({row["field"] for row in data["source_rows"]}), "source rows cover tau owner, symgrad components, stress and denominator")
    add("VAL2598_05_source_paths_exist", all(row["source_path_exists"] is True for row in data["source_rows"]), "source rows point to existing local files")
    required_interfaces = {"div_J_tau", "N_delta_tau", "M_H_ref", "epsilon_stationary_tau", "stationary_tau_score_rule"}
    add("VAL2598_06_bound_interface_complete", required_interfaces.issubset({row["quantity"] for row in data["bound_interface"]}), "delta_tau bound interface covers identity, numerator, denominator, bound and score rule")
    add("VAL2598_07_rows_nonclaim", all(row["score_ready"] is False and row["valid_for_claim"] is False for row in data["source_rows"]) and all(row["score_ready"] is False for row in data["bound_interface"]), "source and bound rows remain non-score-ready and nonclaim")
    add("VAL2598_08_runner_refuses", all(row["score_ready"] is False and row["claim_allowed"] is False for row in data["runner_refusal"]), "runner refuses unsigned theorem/source/bound rows")
    add(
        "VAL2598_09_claim_gates_safe",
        all(row["claim_allowed"] is False for row in data["claim_gates"])
        and any(row["gate_id"] == "CG2598_1_local_stationarity_axiom" and row["gate_status"] == "REJECTED_SHORTCUT" for row in data["claim_gates"])
        and any(row["gate_id"] == "CG2598_2_selector_silence_to_Killing" and row["gate_status"] == "REJECTED_SHORTCUT" for row in data["claim_gates"]),
        "stationarity/selector/lapse/EH/orbital-GM shortcuts and local-GR claims remain blocked",
    )
    add("VAL2598_10_no_claim_flags", generated_rows_have_no_claim_flags(data), "no generated row sets claim, theorem, or scoring flags true")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in (
            "*2598-Y5-R2FR-parent-stationary-tau*",
            "*Y5_R2FR_parent_stationary_tau*",
            "*P8_Y5_STATIONARY_TAU_2598*",
            "*JR2598*",
        ):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add("VAL2598_11_no_formalization_artifacts", not formalization_artifacts, "no 2598 artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_artifacts))
    add("VAL2598_12_next_selected", any(row["route_id"] == "NEXT2598_0_selected" and "2599-Y5-R2FR-boundary-clock-normalized-tau-owner" in row["target_file"] for row in data["next"]), "2599 boundary-clock tau owner/delta_tau source-pack target selected")
    add("VAL2598_13_branch_copies", all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]), "nonclaim branch copies exist")

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2598_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2598_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2598_OVERALL",
        overall,
        "2598 keeps the stationary tau/Killing route conditional, converts the failure into a delta_tau bound interface, and selects boundary-clock tau ownership or source-pack fill next",
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
        "# 2598 Y5 R2FR parent stationary tau generator or first tau role source rows",
        "",
        "**Status:** private nonclaim derivation checkpoint. The stationary/Killing route remains the right mathematical spine, but current MTS does not parent-sign `tau_obs` as a q/e_obs-basic boundary-clock generator.",
        "",
        "**Main result:** the exact identity `div J_tau=(div T_H).tau + T_H^{mu nu} nabla_(mu tau_nu)` is retained. If `tau_obs` is parent-owned, stationary, same-role, and denominator-locked, it could close a serious mass-current route. Current sources do not prove that package, so 2598 converts the failure into a sourceable `delta_tau` bound interface rather than smuggling in local stationarity.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role", "valid_for_claim"]),
        "",
        "## Parent Stationary Tau Theorem Attempt",
        markdown_table(data["theorem_attempt"], ["attempt_id", "premise", "required_identity", "mathematical_form", "current_status", "if_closed", "residual_if_missing", "theorem_signed", "score_ready", "valid_for_claim", "claim_allowed"]),
        "",
        "## Obstruction Matrix",
        markdown_table(data["obstructions"], ["obstruction_id", "object", "current_status", "evidence", "priority", "valid_for_claim", "claim_allowed"]),
        "",
        "## Source Rows",
        markdown_table(data["source_rows"], ["row_id", "field", "required_input", "current_status", "source_path", "source_path_exists", "units", "anti_shortcut", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Delta Tau Bound Interface",
        markdown_table(data["bound_interface"], ["interface_id", "quantity", "definition", "formula", "needed_inputs", "current_status", "score_ready", "valid_for_claim", "claim_allowed"]),
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
        "This moves the coupling problem forward. The project no longer has a vague missing time choice; it has a named object: a parent-owned, q/e_obs-basic, boundary-clock-normalized `tau_obs`. If we cannot derive it, the exact same current identity gives a disciplined bound path through `N_delta_tau/M_H_ref`.",
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)

    theorem_rows = theorem_attempt_rows()
    source_data = source_rows()
    bound_rows = bound_interface_rows()
    data = {
        "sources": source_register_rows(),
        "theorem_attempt": theorem_rows,
        "obstructions": obstruction_rows(),
        "source_rows": source_data,
        "bound_interface": bound_rows,
        "runner_refusal": runner_refusal_rows(theorem_rows, source_data, bound_rows),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["theorem_attempt"], data["theorem_attempt"])
    write_csv(OUTPUTS["obstruction_matrix"], data["obstructions"])
    write_csv(OUTPUTS["source_rows"], data["source_rows"])
    write_csv(OUTPUTS["bound_interface"], data["bound_interface"])
    write_csv(OUTPUTS["runner_refusal"], data["runner_refusal"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])

    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])

    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)

    overall = next(row for row in data["validations"] if row["check_id"] == "VAL2598_OVERALL")
    print(f"{overall['check_id']} {overall['status']}: {overall['notes']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

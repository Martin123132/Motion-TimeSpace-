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

BRANCH_ID = "MTS_R2FR_TOBS_DTAU_NORM_OR_CLOCK_ACTION_2600"
CHECKPOINT_ID = "2600"

DOC = ROOT / "2600-Y5-R2FR-Tobs-delta-tau-norm-owner-or-boundary-clock-action-clause.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_TOBS_DTAU_2600_SOURCE_REGISTER.csv",
    "norm_owner_attempt": OUT / "P8_Y5_TOBS_DTAU_2600_NORM_OWNER_ATTEMPT.csv",
    "boundary_action_audit": OUT / "P8_Y5_TOBS_DTAU_2600_BOUNDARY_CLOCK_ACTION_CLAUSE_AUDIT.csv",
    "ctobs_rows": OUT / "P8_Y5_TOBS_DTAU_2600_CTOBS_SOURCE_ROWS.csv",
    "runner_refusal": OUT / "P8_Y5_TOBS_DTAU_2600_RUNNER_REFUSAL.csv",
    "claim_gates": OUT / "P8_Y5_TOBS_DTAU_2600_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_TOBS_DTAU_2600_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_TOBS_DTAU_2600_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_TOBS_DTAU_2600_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2600_VALIDATION.csv",
}

COPY_TARGETS = {
    "ctobs_rows": LOCAL_BOUNDS / "Tobs_delta_tau_norm_owner_rows_2600_NONCLAIM.csv",
    "boundary_action_audit": LOCAL_BOUNDS / "Boundary_clock_action_clause_audit_2600_NONCLAIM.csv",
    "next_target": QUEUE / "JR2600_TOBS_SUPPORT_ANNULUS_OR_NORM_SOURCE_NEXT.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def with_stamp(row_data: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": utc_now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        **row_data,
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
    for row_data in rows:
        for key in row_data:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row_data in rows:
            writer.writerow({field: row_value(row_data.get(field, "")) for field in fields})


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            parsed_rows = list(csv.DictReader(handle))
        return bool(parsed_rows), len(parsed_rows), ""
    except Exception as exc:
        return False, 0, str(exc)


def path_has_needles(path: Path, needles: list[str]) -> list[str]:
    if not path.exists():
        return needles
    text = path.read_text(encoding="utf-8", errors="replace")
    return [needle for needle in needles if needle not in text]


def source_register_rows() -> list[dict[str, Any]]:
    source_specs = [
        {
            "source_id": "SRC2600_00_2599_handoff_doc",
            "source_path": ROOT / "2599-Y5-R2FR-boundary-clock-normalized-tau-owner-or-delta-tau-source-pack.md",
            "needles": ["DTS2599_12_C_Tobs_tau", "BRC2599_3_denominator", "NEXT2599_0_selected", "VAL2599_OVERALL"],
            "role": "2599 handoff selecting C_Tobs_tau norm owner or boundary-clock action clause",
        },
        {
            "source_id": "SRC2600_01_2599_delta_tau_pack",
            "source_path": OUT / "P8_Y5_BOUNDARY_CLOCK_TAU_2599_DELTA_TAU_SOURCE_PACK.csv",
            "needles": ["DTS2599_12_C_Tobs_tau", "DTS2599_16_total"],
            "role": "2600 input rows for C_Tobs_tau and N_delta_tau numerator",
        },
        {
            "source_id": "SRC2600_02_1729_operator_law_doc",
            "source_path": ROOT / "1729-Y5-R2FR-Tobs-delta-tau-operator-norm-or-source-current-silence.md",
            "needles": ["TON1729_0_linear_map", "TON1729_1_operator_coefficient", "SCS1729_5_verdict", "VAL1729_OVERALL"],
            "role": "exact moving-tau source-current operator law and zero-route rejection",
        },
        {
            "source_id": "SRC2600_03_1729_operator_law_csv",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1729_TOBS_OPERATOR_NORM_LAW.csv",
            "needles": ["TON1729_0_linear_map", "TON1729_1_operator_coefficient", "TON1729_5_verdict"],
            "role": "machine-readable operator law",
        },
        {
            "source_id": "SRC2600_04_1729_ctobs_rows",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1729_C_TOBS_TAU_BOUND_ROWS.csv",
            "needles": ["CTT1729_0_C_Tobs_tau_primary", "CTT1729_3_vacuum_annulus_zero_candidate", "CTT1729_4_C_delta_tau_stack_update"],
            "role": "existing C_Tobs_tau source-row templates and support-annulus zero candidate",
        },
        {
            "source_id": "SRC2600_05_1729_silence_audit",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1729_SOURCE_CURRENT_SILENCE_AUDIT.csv",
            "needles": ["SCS1729_1_vacuum_support_silence", "SCS1729_5_verdict"],
            "role": "zero-proof routes and their active blockers",
        },
        {
            "source_id": "SRC2600_06_1720_jh_norm_source",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1720_JH_NORM_FIRST_SOURCE_ROW.csv",
            "needles": ["JHN1720_0_observed_Hilbert_current_norm_candidate", "MISSING_PARENT_SIGNED_TAU_OBS"],
            "role": "J_H norm owner prerequisites",
        },
        {
            "source_id": "SRC2600_07_1724_common_norm_schema",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1724_COMMON_NORM_SPACE_SCHEMA.csv",
            "needles": ["CNS1724_0_common_owner_schema", "CNS1724_1_minimal_candidate_definition"],
            "role": "common compact-exterior norm owner schema",
        },
        {
            "source_id": "SRC2600_08_1727_boundary_clock_audit",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1727_BOUNDARY_CLOCK_SUPERSELECTION_AUDIT.csv",
            "needles": ["BCS1727_0_boundary_clock_data", "BCS1727_7_verdict"],
            "role": "boundary-clock superselection conditions that would fix tau_obs",
        },
        {
            "source_id": "SRC2600_09_1727_delta_tau_rows",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1727_DELTA_TAU_FIRST_RESIDUAL_ROW.csv",
            "needles": ["DTAU1727_0_delta_tau_first_residual", "DTAU1727_1_source_current_delta_tau"],
            "role": "delta_tau residual first rows",
        },
        {
            "source_id": "SRC2600_10_1728_delta_tau_coefficients",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1728_DELTA_TAU_BOUND_COEFFICIENT_ROWS.csv",
            "needles": ["DTC1728_0_C_Tobs_tau_primary", "DTC1728_3_total_coefficient_stack"],
            "role": "delta_tau coefficient stack that 2600 must not over-promote",
        },
        {
            "source_id": "SRC2600_11_2558_exchange_attempt",
            "source_path": OUT / "P8_Y5_NO_SHADOW_2558_PARENT_EXCHANGE_ATTEMPT.csv",
            "needles": ["PEX2558_3_required_parent_signature", "PEX2558_4_current_corpus_result", "PEX2558_5_stationary_escape"],
            "role": "parent exchange-current obstruction and stationary escape",
        },
        {
            "source_id": "SRC2600_12_2557_clock_gate",
            "source_path": OUT / "P8_Y5_NO_SHADOW_2557_CLOCK_COMPATIBILITY_GATE.csv",
            "needles": ["CLK2557_4_parent_clock_origin", "CLK2557_5_clock_leak_bound"],
            "role": "clock-origin and finite clock-leakage bound gate",
        },
    ]
    rows: list[dict[str, Any]] = []
    for source_spec in source_specs:
        source_path = source_spec["source_path"]
        missing_needles = path_has_needles(source_path, source_spec["needles"])
        rows.append(
            with_stamp(
                {
                    "source_id": source_spec["source_id"],
                    "source_path": source_path,
                    "exists": source_path.exists(),
                    "missing_needles": missing_needles,
                    "source_pass": source_path.exists() and not missing_needles,
                    "role": source_spec["role"],
                    "valid_for_claim": False,
                }
            )
        )
    return rows


def norm_owner_attempt_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "attempt_id": "TON2600_0_exact_linear_map",
            "object": "moving-tau source-current map",
            "formula": "L_Tobs^A[delta tau] := star_A(T_obs(delta tau,.))",
            "derivation_status": "DERIVED_FROM_1729_FIXED_TOBS_VARIATION",
            "missing_inputs": "",
            "owner_signed": True,
            "score_ready": False,
        },
        {
            "attempt_id": "TON2600_1_common_domain",
            "object": "domain norm for delta_tau",
            "formula": "||delta tau_obs||_B and ||tau_obs||_B on the same boundary/collar class used by epsilon_delta_tau",
            "derivation_status": "NOT_PARENT_OWNED",
            "missing_inputs": "MISSING_B_CLOCK;MISSING_TAU_OBS_ID;MISSING_VARIATION_CLASS;MISSING_DELTA_TAU_VALUE_OR_ZERO",
            "owner_signed": False,
            "score_ready": False,
        },
        {
            "attempt_id": "TON2600_2_common_codomain",
            "object": "codomain current norm",
            "formula": "||star_A(T_obs(delta tau,.))||_{J_A}",
            "derivation_status": "NOT_PARENT_OWNED",
            "missing_inputs": "MISSING_A_EXT;MISSING_VOLUME_FORM;MISSING_HODGE_FACTOR;MISSING_CURRENT_NORM;MISSING_UNITS",
            "owner_signed": False,
            "score_ready": False,
        },
        {
            "attempt_id": "TON2600_3_stress_envelope",
            "object": "observed stress-energy operator envelope",
            "formula": "C_Tobs_tau <= C_star_measure(A_ext) sup_A ||T_obs||_op",
            "derivation_status": "BOUND_TEMPLATE_ONLY",
            "missing_inputs": "MISSING_TOBS_OPERATOR_BOUND;MISSING_OBSERVED_COFRAME;MISSING_SOURCE_WORLDTUBE;MISSING_A_EXT_SUPPORT_SPLIT",
            "owner_signed": False,
            "score_ready": False,
        },
        {
            "attempt_id": "TON2600_4_zero_route",
            "object": "theorem-zero route for C_Tobs_tau",
            "formula": "T_obs|A_ext=0 plus boundary flux accounting implies C_Tobs_tau=0 on A_ext only",
            "derivation_status": "CONDITIONAL_SUPPORT_SPLIT_MISSING",
            "missing_inputs": "MISSING_SOURCE_WORLDTUBE;MISSING_A_EXT_CAP_SUPPORT_EMPTY;MISSING_BOUNDARY_FLUX_ACCOUNTING;MISSING_CURRENT_MEASURE_OWNER",
            "owner_signed": False,
            "score_ready": False,
        },
        {
            "attempt_id": "TON2600_5_common_normalization",
            "object": "stack normalization",
            "formula": "N_delta_tau/M_H_ref contains Delta_JH_delta_tau, Delta_H_delta_tau, Delta_clock_boundary_tau and reference terms with shared units",
            "derivation_status": "STACK_TEMPLATE_ONLY",
            "missing_inputs": "MISSING_C_TOBS_TAU;MISSING_EPSILON_DELTA_TAU;MISSING_M_H_REF;MISSING_SECTOR_COEFFICIENTS;MISSING_COMMON_UNITS",
            "owner_signed": False,
            "score_ready": False,
        },
        {
            "attempt_id": "TON2600_6_verdict",
            "object": "C_Tobs_tau norm-owner verdict",
            "formula": "Delta_JH_delta_tau <= C_Tobs_tau ||delta tau_obs||_B is exact in form, but not numeric or claim-valid",
            "derivation_status": "LAW_SIGNED_COEFFICIENT_OWNER_UNSIGNED",
            "missing_inputs": "MISSING_COMMON_NORM_OWNER;MISSING_C_TOBS_TAU_VALUE_OR_ZERO;MISSING_DELTA_TAU_NORM;MISSING_UNITS",
            "owner_signed": False,
            "score_ready": False,
        },
    ]
    return [with_stamp({**row_data, "valid_for_claim": False, "claim_allowed": False}) for row_data in rows]


def boundary_action_audit_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "clause_id": "BCA2600_0_parent_clock_action",
            "clause": "parent boundary-clock action",
            "required_form": "S_clock_boundary[B_clock,e_obs,tau_obs,Psi_clock] is part of the parent action before local readout",
            "current_status": "MISSING_PARENT_BOUNDARY_CLOCK_ACTION",
            "blocking_gap": "clock maps and product bounds exist, but no parent action selects B_clock and tau_obs",
        },
        {
            "clause_id": "BCA2600_1_fixed_phase_space",
            "clause": "fixed boundary phase space",
            "required_form": "delta B_clock=delta B_ref=delta orientation=0 for allowed source/current variations",
            "current_status": "PHASE_SPACE_CLASS_NOT_DECLARED",
            "blocking_gap": "1727 records the theorem shape but not the parent tangent-space declaration",
        },
        {
            "clause_id": "BCA2600_2_unique_extension",
            "clause": "unique exterior time-flow extension",
            "required_form": "tau_obs|B plus stationary/quasilocal evolution fixes tau_obs throughout A_ext",
            "current_status": "GENERATOR_EXTENSION_UNSIGNED",
            "blocking_gap": "stationary collar is allowed conditionally, but not derived as a branch theorem",
        },
        {
            "clause_id": "BCA2600_3_tau_variation_equation",
            "clause": "tau/coframe variation equation",
            "required_form": "variation with respect to tau/coframe either fixes delta tau_obs=0 or produces the exact exchange current",
            "current_status": "MISSING_PARENT_CLOCK_EQUATION",
            "blocking_gap": "2558 rejects inserted I_GK=-L_tau without signed parent equations",
        },
        {
            "clause_id": "BCA2600_4_no_clock_product_shortcut",
            "clause": "clock-product quarantine",
            "required_form": "B_clock cannot be inferred from kappa_alpha tau_clock_time after readout",
            "current_status": "SHORTCUT_REJECTED",
            "blocking_gap": "clock product constrains a residual channel but does not own the generator",
        },
        {
            "clause_id": "BCA2600_5_verdict",
            "clause": "boundary-clock action clause verdict",
            "required_form": "B_clock parent action signs tau_obs, fixed variation, and the common norm owner",
            "current_status": "BOUNDARY_CLOCK_ACTION_NOT_DERIVED_CURRENT_CORPUS",
            "blocking_gap": "all antecedents remain unsigned, so C_Tobs_tau must stay as a nonclaim source row",
        },
    ]
    return [
        with_stamp({**row_data, "owner_signed": False, "score_ready": False, "valid_for_claim": False, "claim_allowed": False})
        for row_data in rows
    ]


def ctobs_source_rows() -> list[dict[str, Any]]:
    source_path_stack = [
        OUT / "P8_Y5_PARENT_QLOC_1729_TOBS_OPERATOR_NORM_LAW.csv",
        OUT / "P8_Y5_PARENT_QLOC_1729_C_TOBS_TAU_BOUND_ROWS.csv",
        OUT / "P8_Y5_PARENT_QLOC_1729_SOURCE_CURRENT_SILENCE_AUDIT.csv",
        OUT / "P8_Y5_PARENT_QLOC_1720_JH_NORM_FIRST_SOURCE_ROW.csv",
        OUT / "P8_Y5_PARENT_QLOC_1724_COMMON_NORM_SPACE_SCHEMA.csv",
        OUT / "P8_Y5_BOUNDARY_CLOCK_TAU_2599_DELTA_TAU_SOURCE_PACK.csv",
    ]
    rows = [
        {
            "row_id": "CNR2600_0_C_Tobs_tau_owner",
            "symbol": "C_Tobs_tau",
            "definition": "operator norm of delta tau_obs -> star_A(T_obs(delta tau_obs,.)) on the declared compact exterior",
            "bound_form": "Delta_JH_delta_tau <= C_Tobs_tau ||delta tau_obs||_B",
            "required_inputs": "system_id;A_ext;B_clock;tau_obs_id;norm_pair;volume_form;Hodge_star_factor;Tobs_operator_bound;delta_tau_norm;current_norm;units;source_paths",
            "current_status": "LAW_DERIVED_OWNER_INPUTS_MISSING",
            "missing_inputs": "MISSING_A_EXT;MISSING_B_CLOCK;MISSING_TAU_OBS_ID;MISSING_NORM_PAIR;MISSING_TOBS_OPERATOR_BOUND;MISSING_DELTA_TAU_NORM;MISSING_CURRENT_NORM;MISSING_UNITS",
            "numeric_value": "MISSING_C_TOBS_TAU",
            "units": "current_norm_per_tau_norm_MISSING",
        },
        {
            "row_id": "CNR2600_1_Delta_JH_delta_tau",
            "symbol": "Delta_JH_delta_tau",
            "definition": "moving observed-time source-current residual",
            "bound_form": "||star_A(T_obs(delta tau_obs,.))|| <= C_Tobs_tau ||delta tau_obs||_B",
            "required_inputs": "C_Tobs_tau;epsilon_delta_tau;tau_obs_norm;A_ext;current_norm;units",
            "current_status": "BOUND_FORM_READY_VALUES_MISSING",
            "missing_inputs": "MISSING_C_TOBS_TAU;MISSING_EPSILON_DELTA_TAU;MISSING_TAU_OBS_NORM;MISSING_A_EXT;MISSING_CURRENT_NORM;MISSING_UNITS",
            "numeric_value": "MISSING_DELTA_JH_DELTA_TAU",
            "units": "current_norm_units_MISSING",
        },
        {
            "row_id": "CNR2600_2_Tobs_envelope",
            "symbol": "sup_A_norm_Tobs_op",
            "definition": "conservative stress-energy operator envelope on A_ext",
            "bound_form": "C_Tobs_tau <= C_star_measure(A_ext) sup_A ||T_obs||_op",
            "required_inputs": "Tobs_components_or_energy_density_bound;observed_metric;A_ext;norm_type;Hodge_star_factor;units;source_path",
            "current_status": "SOURCE_ROW_TEMPLATE_ONLY",
            "missing_inputs": "MISSING_TOBS_COMPONENTS_OR_ENERGY_DENSITY_BOUND;MISSING_OBSERVED_METRIC;MISSING_A_EXT;MISSING_NORM_TYPE;MISSING_HODGE_FACTOR;MISSING_UNITS",
            "numeric_value": "MISSING_SUP_TOBS_OP",
            "units": "stress_energy_or_current_conversion_units_MISSING",
        },
        {
            "row_id": "CNR2600_3_vacuum_annulus_zero_candidate",
            "symbol": "Z_Tobs_Aext",
            "definition": "candidate theorem-zero flag for the source-current coefficient in a matter-free exterior annulus",
            "bound_form": "if supp(T_obs) cap A_ext is empty and boundary flux is accounted elsewhere, C_Tobs_tau=0 on A_ext",
            "required_inputs": "source_worldtube;A_ext_excludes_support;Tobs_support_proof;boundary_flux_accounting;current_measure_owner;source_path",
            "current_status": "ZERO_ROUTE_CONDITIONAL_SUPPORT_SPLIT_MISSING",
            "missing_inputs": "MISSING_SOURCE_WORLDTUBE;MISSING_A_EXT_SUPPORT_SPLIT;MISSING_TOBS_SUPPORT_PROOF;MISSING_BOUNDARY_FLUX_ACCOUNTING;MISSING_CURRENT_MEASURE_OWNER",
            "numeric_value": "MISSING_Z_TOBS_AEXT",
            "units": "boolean_theorem_zero_MISSING",
        },
        {
            "row_id": "CNR2600_4_delta_tau_stack_update",
            "symbol": "C_delta_tau_source_stack",
            "definition": "source-current piece of the full moving-time-generator residual stack",
            "bound_form": "source_piece <= C_Tobs_tau epsilon_delta_tau ||tau_obs||_B",
            "required_inputs": "C_Tobs_tau;epsilon_delta_tau;tau_obs_norm;common_normalization;source_paths;units",
            "current_status": "STACK_LINK_READY_VALUES_MISSING",
            "missing_inputs": "MISSING_C_TOBS_TAU;MISSING_EPSILON_DELTA_TAU;MISSING_TAU_OBS_NORM;MISSING_COMMON_NORMALIZATION;MISSING_UNITS",
            "numeric_value": "MISSING_SOURCE_STACK_VALUE",
            "units": "dimensionless_after_common_normalization_MISSING",
        },
        {
            "row_id": "CNR2600_5_MHref_denominator_guard",
            "symbol": "M_H_ref",
            "definition": "denominator for epsilon_stationary_tau and source-current stack comparison",
            "bound_form": "epsilon_stationary_tau <= N_delta_tau/M_H_ref",
            "required_inputs": "nonzero positive parent-owned M_H_ref;reference phase space;not orbital GM;units;source_path",
            "current_status": "DENOMINATOR_GUARD_OPEN",
            "missing_inputs": "MISSING_PARENT_SIGNED_M_H_REF;MISSING_REFERENCE_PHASE_SPACE;MISSING_NON_ORBITAL_DENOMINATOR_PROOF;MISSING_UNITS",
            "numeric_value": "MISSING_M_H_REF",
            "units": "mass_or_action_time_normalization_MISSING",
        },
    ]
    return [
        with_stamp(
            {
                **row_data,
                "source_paths": source_path_stack,
                "source_paths_exist": all(source_path.exists() for source_path in source_path_stack),
                "score_ready": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        for row_data in rows
    ]


def runner_refusal_rows(
    norm_rows: list[dict[str, Any]],
    action_rows: list[dict[str, Any]],
    source_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    any_norm_missing = any(row_data["owner_signed"] is False for row_data in norm_rows)
    any_action_missing = any(row_data["owner_signed"] is False for row_data in action_rows)
    any_source_missing = any("MISSING_" in row_value(row_data["missing_inputs"]) for row_data in source_rows)
    rows = [
        {
            "runner_id": "RUN2600_0_exact_law",
            "target": "Delta_JH_delta_tau <= C_Tobs_tau ||delta tau_obs||_B",
            "verdict": "ACCEPT_BOUND_FORM_ONLY",
            "failure_reasons": "COEFFICIENT_OWNER_UNSIGNED;NUMERIC_VALUE_MISSING;UNITS_MISSING",
            "accepted_for_scoring": False,
        },
        {
            "runner_id": "RUN2600_1_C_Tobs_tau_claim",
            "target": "C_Tobs_tau numeric/theorem-zero coefficient",
            "verdict": "REFUSE_SCORING",
            "failure_reasons": "MISSING_A_EXT;MISSING_NORM_PAIR;MISSING_TOBS_OPERATOR_BOUND;MISSING_SUPPORT_SPLIT_OR_STRESS_ROW",
            "accepted_for_scoring": False,
        },
        {
            "runner_id": "RUN2600_2_boundary_clock_action",
            "target": "parent action owns B_clock/tau_obs/fixed variation",
            "verdict": "REFUSE_CLAIM",
            "failure_reasons": "MISSING_PARENT_BOUNDARY_CLOCK_ACTION;MISSING_FIXED_PHASE_SPACE;MISSING_UNIQUE_EXTENSION;MISSING_TAU_VARIATION_EQUATION",
            "accepted_for_scoring": False,
        },
        {
            "runner_id": "RUN2600_3_local_GR_Newton",
            "target": "local GR/Newton recovery from this branch",
            "verdict": "BLOCKED_NO_CLAIM",
            "failure_reasons": "NO_C_TOBS_TAU_VALUE_OR_ZERO;NO_EPSILON_DELTA_TAU;NO_PARENT_M_H_REF;PPN_VECTOR_UNCLEARED",
            "accepted_for_scoring": False,
        },
    ]
    return [
        with_stamp(
            {
                **row_data,
                "norm_missing": any_norm_missing,
                "action_missing": any_action_missing,
                "source_missing": any_source_missing,
                "claim_allowed": False,
                "valid_for_claim": False,
            }
        )
        for row_data in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "CG2600_0_exact_operator_law",
            "claim": "moving-tau source-current law is exact in form",
            "gate_status": "PASS_FORM_ONLY",
            "reason": "1729 derives the linear map at fixed T_obs and observed volume form",
            "gate_pass": True,
        },
        {
            "gate_id": "CG2600_1_coefficient_value",
            "claim": "C_Tobs_tau is numeric or theorem-zero",
            "gate_status": "BLOCKED_NO_CLAIM",
            "reason": "no A_ext/norm_pair/Tobs envelope/support split/current units owner",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2600_2_boundary_clock_action",
            "claim": "parent boundary-clock action fixes tau_obs",
            "gate_status": "BLOCKED_NO_CLAIM",
            "reason": "B_clock action, fixed phase space, unique extension and tau equation are unsigned",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2600_3_clock_product_shortcut",
            "claim": "clock product bound owns tau_obs",
            "gate_status": "REJECTED_SHORTCUT",
            "reason": "a residual bound is not a parent generator-selection theorem",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2600_4_lapse_or_stationarity_shortcut",
            "claim": "choose lapse/stationary collar to kill delta_tau",
            "gate_status": "REJECTED_SHORTCUT",
            "reason": "stationary collars can be conditional hypotheses only until parent-signed",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2600_5_local_GR_claim",
            "claim": "local GR/Newton branch passes",
            "gate_status": "BLOCKED_NO_CLAIM",
            "reason": "source-current, denominator, clock/reference and PPN residual vector remain open",
            "gate_pass": False,
        },
    ]
    return [with_stamp({**row_data, "valid_for_claim": False, "claim_allowed": False}) for row_data in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2600_0_progress",
            "decision": "keep the exact operator-norm law",
            "reason": "Delta_JH_delta_tau is now a lawful linear response channel rather than a vague leak",
            "effect": "use C_Tobs_tau rows as the nonclaim interface",
        },
        {
            "decision_id": "DEC2600_1_no_owner",
            "decision": "do not promote C_Tobs_tau to evidence",
            "reason": "the common domain/codomain norm owner and stress envelope are missing",
            "effect": "runner stays blocked unless a theorem-zero or source-backed coefficient is supplied",
        },
        {
            "decision_id": "DEC2600_2_no_boundary_action",
            "decision": "boundary-clock action route remains open but unsigned",
            "reason": "current corpus has contracts and residual bounds, not a parent action clause",
            "effect": "do not use B_clock or clock product to freeze tau_obs",
        },
        {
            "decision_id": "DEC2600_3_next",
            "decision": "attack the support-annulus split first",
            "reason": "the cleanest low-scrutiny route is to prove C_Tobs_tau=0 on A_ext by excluding matter support while keeping boundary flux in the ledger",
            "effect": "2601 should decide vacuum annulus zero versus first Tobs norm source row",
        },
    ]
    return [with_stamp({**row_data, "valid_for_claim": False}) for row_data in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2600_0_selected",
            "selection_status": "selected",
            "target_file": "2601-Y5-R2FR-Tobs-support-annulus-split-or-first-norm-source-row.md",
            "target_script": "scripts/Y5_R2FR_Tobs_support_annulus_split_or_first_norm_source_row_2601.py",
            "task": "prove whether the chosen compact exterior A_ext is a vacuum annulus for T_obs with boundary flux retained, or fill the first source-backed Tobs operator-norm row",
            "success_condition": "C_Tobs_tau becomes theorem-zero on A_ext or receives a sourced nonclaim stress envelope with units",
            "fallback_condition": "keep C_Tobs_tau as a symbolic source row and move to numeric stress-envelope acquisition",
            "guardrails": "no integral cancellation; no hidden matter support; no orbital GM denominator; no clock-product shortcut; no local-GR claim; no GitHub; no formalization-workbench edits",
        }
    ]
    return [with_stamp({**row_data, "valid_for_claim": False}) for row_data in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for copy_id, target_path in COPY_TARGETS.items():
        source_path = OUTPUTS[copy_id]
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)
        rows.append(
            with_stamp(
                {
                    "copy_id": f"COPY2600_{copy_id}",
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
    for generated_rows in data.values():
        for row_data in generated_rows:
            if row_data.get("valid_for_claim") is True or row_data.get("claim_allowed") is True:
                return False
            if row_data.get("score_ready") is True and row_data.get("attempt_id") != "TON2600_0_exact_linear_map":
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

    add("VAL2600_00_sources_exist", all(row_data["source_pass"] is True for row_data in data["sources"]), "all cited local source paths exist and needles are present")
    required_norm_ids = {
        "TON2600_0_exact_linear_map",
        "TON2600_1_common_domain",
        "TON2600_2_common_codomain",
        "TON2600_3_stress_envelope",
        "TON2600_4_zero_route",
        "TON2600_5_common_normalization",
        "TON2600_6_verdict",
    }
    add("VAL2600_01_norm_owner_attempt_complete", required_norm_ids.issubset({row_data["attempt_id"] for row_data in data["norm_owner"]}), "norm-owner attempt covers map, domain, codomain, stress, zero route, stack and verdict")
    add(
        "VAL2600_02_exact_law_preserved",
        any(row_data["attempt_id"] == "TON2600_0_exact_linear_map" and row_data["owner_signed"] is True for row_data in data["norm_owner"])
        and any(row_data["attempt_id"] == "TON2600_6_verdict" and row_data["derivation_status"] == "LAW_SIGNED_COEFFICIENT_OWNER_UNSIGNED" for row_data in data["norm_owner"]),
        "exact linear law is kept, while coefficient owner remains unsigned",
    )
    required_action_ids = {
        "BCA2600_0_parent_clock_action",
        "BCA2600_1_fixed_phase_space",
        "BCA2600_2_unique_extension",
        "BCA2600_3_tau_variation_equation",
        "BCA2600_4_no_clock_product_shortcut",
        "BCA2600_5_verdict",
    }
    add("VAL2600_03_boundary_action_audit_complete", required_action_ids.issubset({row_data["clause_id"] for row_data in data["boundary_action"]}), "boundary-clock action audit covers parent action, phase space, extension, tau equation, shortcut and verdict")
    add("VAL2600_04_boundary_action_not_promoted", all(row_data["owner_signed"] is False and row_data["claim_allowed"] is False for row_data in data["boundary_action"]), "boundary-clock action route remains unsigned")
    required_symbols = {"C_Tobs_tau", "Delta_JH_delta_tau", "sup_A_norm_Tobs_op", "Z_Tobs_Aext", "C_delta_tau_source_stack", "M_H_ref"}
    add("VAL2600_05_ctobs_rows_complete", required_symbols.issubset({row_data["symbol"] for row_data in data["ctobs_rows"]}), "C_Tobs_tau rows cover coefficient, residual, stress envelope, vacuum zero, stack and denominator")
    add("VAL2600_06_ctobs_rows_nonclaim", all(row_data["score_ready"] is False and row_data["valid_for_claim"] is False and row_data["source_paths_exist"] is True for row_data in data["ctobs_rows"]), "all C_Tobs_tau source rows are nonclaim and cite existing inputs")
    add("VAL2600_07_runner_refuses", all(row_data["accepted_for_scoring"] is False and row_data["claim_allowed"] is False for row_data in data["runner_refusal"]), "runner refuses scoring for missing coefficient owner, action clause and local-GR claims")
    add(
        "VAL2600_08_claim_gates_safe",
        all(row_data["claim_allowed"] is False for row_data in data["claim_gates"])
        and any(row_data["gate_id"] == "CG2600_3_clock_product_shortcut" and row_data["gate_status"] == "REJECTED_SHORTCUT" for row_data in data["claim_gates"])
        and any(row_data["gate_id"] == "CG2600_5_local_GR_claim" and row_data["gate_status"] == "BLOCKED_NO_CLAIM" for row_data in data["claim_gates"]),
        "shortcuts and local-GR/Newton claims remain blocked",
    )
    add("VAL2600_09_no_claim_flags", generated_rows_have_no_claim_flags(data), "no generated row promotes score-ready evidence or claim flags")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in (
            "*2600-Y5-R2FR-Tobs*",
            "*Y5_R2FR_Tobs_delta_tau*2600*",
            "*P8_Y5_TOBS_DTAU_2600*",
            "*JR2600*",
        ):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add("VAL2600_10_no_formalization_artifacts", not formalization_artifacts, "no 2600 artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_artifacts))
    add("VAL2600_11_next_selected", any(row_data["route_id"] == "NEXT2600_0_selected" and "2601-Y5-R2FR-Tobs-support-annulus-split" in row_data["target_file"] for row_data in data["next"]), "2601 support-annulus or first norm source-row target selected")
    add("VAL2600_12_branch_copies", all(row_data["source_exists"] is True and row_data["target_exists"] is True for row_data in data["copies"]), "nonclaim branch copies exist")

    for output_key, output_path in OUTPUTS.items():
        if output_key == "validation":
            continue
        parsed, count, error = csv_parses(output_path)
        add(f"VAL2600_CSV_{output_path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for copy_key, copy_path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(copy_path)
        add(f"VAL2600_COPY_CSV_{copy_key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row_data["status"] == "PASS" for row_data in rows)
    add(
        "VAL2600_OVERALL",
        overall,
        "2600 preserves the exact Tobs/delta_tau operator law, refuses the unsigned norm owner and boundary-clock action shortcut, stages nonclaim C_Tobs_tau rows, and selects support-annulus split or first norm source row next",
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for row_data in rows:
        values = [row_value(row_data.get(column, "")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2600 Y5 R2FR Tobs delta tau norm owner or boundary clock action clause",
        "",
        "**Status:** private nonclaim derivation checkpoint. The exact source-current response to a moving observed time generator is retained, but the coefficient owner and boundary-clock action clause are not yet parent-signed.",
        "",
        "**Main result:** 2600 gives one real step forward and one hard stop. The real step is the exact law `Delta_JH_delta_tau <= C_Tobs_tau ||delta tau_obs||_B`, inherited from the 1729 linear map `L_Tobs^A[delta tau]=star_A(T_obs(delta tau,.))`. The hard stop is that current MTS still does not own the shared domain/codomain norm, stress envelope, support-annulus split, or boundary-clock action needed to turn `C_Tobs_tau` into evidence. No local-GR/Newton claim is made.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role", "valid_for_claim"]),
        "",
        "## C_Tobs Norm Owner Attempt",
        markdown_table(data["norm_owner"], ["attempt_id", "object", "formula", "derivation_status", "missing_inputs", "owner_signed", "score_ready", "valid_for_claim", "claim_allowed"]),
        "",
        "## Boundary Clock Action Clause Audit",
        markdown_table(data["boundary_action"], ["clause_id", "clause", "required_form", "current_status", "blocking_gap", "owner_signed", "score_ready", "valid_for_claim", "claim_allowed"]),
        "",
        "## C_Tobs Source Rows",
        markdown_table(data["ctobs_rows"], ["row_id", "symbol", "definition", "bound_form", "required_inputs", "current_status", "missing_inputs", "numeric_value", "units", "source_paths", "source_paths_exist", "score_ready", "valid_for_claim", "claim_allowed"]),
        "",
        "## Runner Refusal",
        markdown_table(data["runner_refusal"], ["runner_id", "target", "verdict", "failure_reasons", "norm_missing", "action_missing", "source_missing", "accepted_for_scoring", "claim_allowed", "valid_for_claim"]),
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
        "This is not circling. It is turning a vague local leak into a specific theorem-or-data gate. The clean route is now sharp: either prove the exterior annulus carries no ordinary `T_obs` support while boundary flux is retained elsewhere, or pay for `C_Tobs_tau` with a sourced stress-energy envelope and units.",
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)

    norm_owner = norm_owner_attempt_rows()
    boundary_action = boundary_action_audit_rows()
    ctobs_rows = ctobs_source_rows()
    data = {
        "sources": source_register_rows(),
        "norm_owner": norm_owner,
        "boundary_action": boundary_action,
        "ctobs_rows": ctobs_rows,
        "runner_refusal": runner_refusal_rows(norm_owner, boundary_action, ctobs_rows),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["norm_owner_attempt"], data["norm_owner"])
    write_csv(OUTPUTS["boundary_action_audit"], data["boundary_action"])
    write_csv(OUTPUTS["ctobs_rows"], data["ctobs_rows"])
    write_csv(OUTPUTS["runner_refusal"], data["runner_refusal"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])

    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])

    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)

    overall = next(row_data for row_data in data["validations"] if row_data["check_id"] == "VAL2600_OVERALL")
    print(f"{overall['check_id']} {overall['status']}: {overall['notes']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

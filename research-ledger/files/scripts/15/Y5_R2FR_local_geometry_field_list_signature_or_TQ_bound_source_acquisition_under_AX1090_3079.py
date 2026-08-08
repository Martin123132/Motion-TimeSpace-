from __future__ import annotations

import csv
import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
RUN_RESULTS = ROOT / "runs" / "20260602-141500-metric-compatibility-Levi-Civita-or-R11-connection-row" / "results"
FORMALIZATION = PROJECT / "formalization-workbench"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3079"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3079-Y5-R2FR-local-geometry-field-list-signature-or-TQ-bound-source-acquisition-under-AX1090.md"
DOTG_TARGET = RESIDUALS / "P8_time_drift_residual_or_zero.csv"

SOURCE_PATHS = {
    "SRC3079_00_3078_doc": ROOT / "3078-Y5-R2FR-P4-TQ-first-source-or-theorem-zero-under-AX1090.md",
    "SRC3079_01_3078_next": RESIDUALS / "P8_Y5_R2FR_3078_NEXT_TARGET.csv",
    "SRC3079_02_3078_geometry_gap": RESIDUALS / "P8_Y5_R2FR_3078_GEOMETRY_FIELD_LIST_GAP_LEDGER.csv",
    "SRC3079_03_3078_tq_theorem": RESIDUALS / "P8_Y5_R2FR_3078_P4_TQ_THEOREM_ZERO_AUDIT.csv",
    "SRC3079_04_3078_tq_numeric": RESIDUALS / "P8_Y5_R2FR_3078_P4_TQ_NUMERIC_SOURCE_AUDIT.csv",
    "SRC3079_05_3078_tq_bound": RESIDUALS / "P8_Y5_R2FR_3078_P4_TQ_BOUND_SCHEMA_NONCLAIM.csv",
    "SRC3079_06_3075_inventory": RESIDUALS / "P8_Y5_R2FR_3075_PARENT_FIELD_INVENTORY_AUDIT.csv",
    "SRC3079_07_3075_nogamma": RESIDUALS / "P8_Y5_R2FR_3075_NO_INDEPENDENT_GAMMA_AUDIT.csv",
    "SRC3079_08_3075_nohyper": RESIDUALS / "P8_Y5_R2FR_3075_NO_HYPERMOMENTUM_AUDIT.csv",
    "SRC3079_09_1831_inventory": RESIDUALS / "P8_Y5_PARENT_QLOC_1831_FIELD_INVENTORY_CERTIFICATE_ATTEMPT.csv",
    "SRC3079_10_1831_p4_first": RESIDUALS / "P8_Y5_PARENT_QLOC_1831_P4_FIRST_ROW_ACQUISITION_LEDGER.csv",
    "SRC3079_11_1831_weakmap": RESIDUALS / "P8_Y5_PARENT_QLOC_1831_P4_WEAK_FIELD_MAP_CONTRACT.csv",
    "SRC3079_12_1832_tq_zero": RESIDUALS / "P8_Y5_PARENT_QLOC_1832_TQ_ZERO_THEOREM_ATTEMPT.csv",
    "SRC3079_13_1832_coeff": RESIDUALS / "P8_Y5_PARENT_QLOC_1832_FIRST_COEFFICIENT_SOURCE_ROW.csv",
    "SRC3079_14_1832_routes": RESIDUALS / "P8_Y5_PARENT_QLOC_1832_PALATINI_METRIC_AFFINE_ROUTE_AUDIT.csv",
    "SRC3079_15_1833_decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1833_DECISION_LEDGER.csv",
    "SRC3079_16_1833_hyper": RESIDUALS / "P8_Y5_PARENT_QLOC_1833_HYPERMOMENTUM_SOURCE_ROW.csv",
    "SRC3079_17_1833_distortion": RESIDUALS / "P8_Y5_PARENT_QLOC_1833_DISTORTION_EQUATION_OWNER_AUDIT.csv",
    "SRC3079_18_run_p4_gates": RUN_RESULTS / "P4_gate_tests.csv",
    "SRC3079_19_run_demotions": RUN_RESULTS / "connection_operator_demotions.csv",
    "SRC3079_20_run_templates": RUN_RESULTS / "P4_R11_template_rows.csv",
    "SRC3079_21_dotg_target": DOTG_TARGET,
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3079_SOURCE_REGISTER.csv",
    "field_list": RESIDUALS / "P8_Y5_R2FR_3079_LOCAL_GEOMETRY_FIELD_LIST_SIGNATURE_AUDIT.csv",
    "connection": RESIDUALS / "P8_Y5_R2FR_3079_DERIVED_CONNECTION_DECLARATION_AUDIT.csv",
    "source_current": RESIDUALS / "P8_Y5_R2FR_3079_SOURCE_READOUT_CONNECTION_CURRENT_AUDIT.csv",
    "tq_acquisition": RESIDUALS / "P8_Y5_R2FR_3079_TQ_BOUND_SOURCE_ACQUISITION_NONCLAIM.csv",
    "historical": RESIDUALS / "P8_Y5_R2FR_3079_PRIOR_TRAIL_RECONCILIATION_LEDGER.csv",
    "local_consequence": RESIDUALS / "P8_Y5_R2FR_3079_LOCAL_GR_CONSEQUENCE_LEDGER.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3079_DECISION_LEDGER.csv",
    "claim_status": RESIDUALS / "P8_Y5_R2FR_3079_CLAIM_STATUS.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3079_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3079_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3079_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "field_list_copy": PARENT_ACTION / "local_geometry_field_list_signature_3079_NOT_SIGNED.csv",
    "connection_copy": PARENT_ACTION / "derived_connection_declaration_3079_NOT_SIGNED.csv",
    "source_current_copy": PARENT_ACTION / "source_readout_connection_current_3079_NOT_SIGNED.csv",
    "tq_acquisition_copy": LOCAL_BOUNDS / "TQ_bound_source_acquisition_3079_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3079_no_hypermomentum_source_readout_or_DeltaGamma_bound_NEXT_NONCLAIM.csv",
}

for output_path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    output_path.parent.mkdir(parents=True, exist_ok=True)


def remove_pycache() -> None:
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


def file_hash(path: Path) -> str:
    if not path.exists():
        return "MISSING"
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y", "pass", "passed"}


def csv_ok(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        with path.open("r", newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def source_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_ok(path) if path.suffix.lower() == ".csv" else True


def row_count(path: Path) -> int:
    if not path.exists():
        return 0
    if path.suffix.lower() == ".csv":
        return len(rows(path))
    return len(path.read_text(encoding="utf-8").splitlines())


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for output_row in output_rows:
        for key in output_row:
            if key not in fieldnames:
                fieldnames.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for output_row in output_rows:
            writer.writerow({key: output_row.get(key, "") for key in fieldnames})


def under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def has_claim_true(input_rows: list[dict[str, Any]]) -> bool:
    claim_fields = {
        "valid_for_claim",
        "claim_allowed",
        "valid_prediction_row",
        "score_ready",
        "claim_active",
        "signature_signed",
        "parent_signed",
        "inventory_signed",
        "connection_declared",
        "current_silence_signed",
        "numeric_ready",
        "bound_ready",
        "local_gr_claim",
        "tq_zero_claim",
        "theorem_zero_signed",
    }
    for input_row in input_rows:
        for field in claim_fields:
            if field in input_row and boolish(input_row[field]):
                return True
    return False


def base(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "timestamp_utc": RUN_UTC,
        "score_ready": "false",
        "valid_prediction_row": "false",
        "valid_for_claim": "false",
        "claim_allowed": "false",
        **row,
    }


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def md_table(table_rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not table_rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for table_row in table_rows:
        lines.append("| " + " | ".join(md_escape(table_row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def copy_csv(source_path: Path, destination_path: Path) -> None:
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source_path, destination_path)


remove_pycache()
dotg_hash_before = file_hash(DOTG_TARGET)

source_register = [
    base(
        {
            "source_id": source_id,
            "source_path": str(source_path),
            "exists": str(source_path.exists()),
            "parse_ok": str(source_parse_ok(source_path)),
            "row_count": row_count(source_path),
            "role": "local_geometry_field_list_signature_or_TQ_bound_evidence" if source_id != "SRC3079_21_dotg_target" else "append_guard_target",
            "status": "PRESENT" if source_path.exists() else "MISSING_SOURCE",
        }
    )
    for source_id, source_path in SOURCE_PATHS.items()
]

field_list_rows = [
    base(
        {
            "signature_id": "LGS3079_0_metric_coframe_parent",
            "required_signature": "parent local configuration variables are g_obs/e_obs plus matter; no independent Gamma/omega/C variable appears in the local branch",
            "current_evidence": "1831 and 3078 preserve the exact conditional theorem but do not sign the parent field list",
            "current_status": "CONDITIONAL_EXACT_NOT_PARENT_SIGNED",
            "signature_signed": "false",
            "parent_signed": "false",
            "inventory_signed": "false",
            "would_buy": "T=0,Q=0 kinematically; K_P4_TQ=0",
            "missing_for_claim": "MISSING_PARENT_ACTION_FIELD_LIST;MISSING_VARIATION_DOMAIN;MISSING_NO_INDEPENDENT_CONNECTION_SLOT",
            "source_ids": "SRC3079_02_3078_geometry_gap;SRC3079_09_1831_inventory",
        }
    ),
    base(
        {
            "signature_id": "LGS3079_1_visible_q_inventory",
            "required_signature": "q_loc owns visible e_obs,g_obs,omega_obs,theta_vis before tests and forbids post-hoc deletion of failed connection couplings",
            "current_evidence": "visible q inventory remains candidate-only",
            "current_status": "CANDIDATE_ONLY",
            "signature_signed": "false",
            "parent_signed": "false",
            "inventory_signed": "false",
            "would_buy": "prevents hiding local connection leakage after a failed test",
            "missing_for_claim": "MISSING_QLOC_PARENT_DEFINITION;MISSING_FIELD_BY_FIELD_DERIVATIVE;MISSING_NO_POSTHOC_DELETION_GUARD",
            "source_ids": "SRC3079_09_1831_inventory;SRC3079_06_3075_inventory",
        }
    ),
    base(
        {
            "signature_id": "LGS3079_2_single_geometry_stack",
            "required_signature": "measure, coframe, metric, connection and derivative stack descend together from the same observed geometry",
            "current_evidence": "single stack descent is not parent signed",
            "current_status": "NOT_PARENT_SIGNED",
            "signature_signed": "false",
            "parent_signed": "false",
            "inventory_signed": "false",
            "would_buy": "blocks connection force re-entry through source/readout stack mismatch",
            "missing_for_claim": "MISSING_MEASURE_COFIELD_CONNECTION_DESCENT;MISSING_BOUNDARY_DOMAIN_STACK",
            "source_ids": "SRC3079_09_1831_inventory;SRC3079_06_3075_inventory",
        }
    ),
    base(
        {
            "signature_id": "LGS3079_3_residual_reconciliation",
            "required_signature": "Gamma_eff, K_hat, q_loc and P4 are reconciled: either metric/coframe functionals or explicit residuals",
            "current_evidence": "Delta_K/P4 residual branch is retained",
            "current_status": "RESIDUAL_BRANCH_RETAINED",
            "signature_signed": "false",
            "parent_signed": "false",
            "inventory_signed": "false",
            "would_buy": "prevents double-counting or silently dropping Delta_K/P4 channels",
            "missing_for_claim": "MISSING_GAMMA_EFF_KHAT_OWNER;MISSING_DELTAK_ZERO_OR_BOUND;MISSING_P4_COMPLETION",
            "source_ids": "SRC3079_09_1831_inventory;SRC3079_10_3076_deltak",
        }
    ),
    base(
        {
            "signature_id": "LGS3079_4_verdict",
            "required_signature": "all local geometry field-list clauses close in one parent grammar",
            "current_evidence": "all current rows remain conditional or fail-open",
            "current_status": "LOCAL_GEOMETRY_FIELD_LIST_NOT_SIGNED",
            "signature_signed": "false",
            "parent_signed": "false",
            "inventory_signed": "false",
            "would_buy": "live GR-reduction route for the T/Q part of P4",
            "missing_for_claim": "MISSING_PARENT_FIELD_LIST;MISSING_NO_GAMMA_SLOT;MISSING_GEOMETRY_STACK_DESCENT;MISSING_SOURCE_READOUT_SILENCE",
            "source_ids": "SRC3079_02_3078_geometry_gap;SRC3079_09_1831_inventory",
        }
    ),
]

connection_rows = [
    base(
        {
            "connection_id": "DCD3079_0_derivative_only",
            "required_declaration": "omega_obs := omega[e_obs] or Gamma_obs := Gamma_LC[g_obs] in every ordinary local sector",
            "current_evidence": "omega[e] appears as a conditional route but is not globally parent-declared",
            "current_status": "DERIVATIVE_ONLY_NOT_GLOBAL",
            "connection_declared": "false",
            "theorem_zero_signed": "false",
            "missing_for_claim": "MISSING_GLOBAL_DERIVED_CONNECTION_DECLARATION;MISSING_SPINOR_TRANSPORT_CLAUSE",
            "source_ids": "SRC3079_07_3075_nogamma;SRC3079_09_1831_inventory",
        }
    ),
    base(
        {
            "connection_id": "DCD3079_1_independent_slot_absence",
            "required_declaration": "parent action and source/readout grammar never vary an independent connection",
            "current_evidence": "P4 gate remains fail-open for independent connection absence",
            "current_status": "NOT_CERTIFIED",
            "connection_declared": "false",
            "theorem_zero_signed": "false",
            "missing_for_claim": "MISSING_NO_INDEPENDENT_GAMMA_SLOT;MISSING_CONNECTION_EULER_EXCLUSION",
            "source_ids": "SRC3079_09_1831_inventory;SRC3079_18_run_p4_gates",
        }
    ),
    base(
        {
            "connection_id": "DCD3079_2_metric_affine_repair",
            "required_declaration": "if independent C exists, parent variation supplies M_C C = Delta_Gamma + boundary + projective with zero/invertible source-free solution",
            "current_evidence": "1832/1833 say distortion equation owner is not proven",
            "current_status": "DISTORTION_EQUATION_OWNER_NOT_PROVEN",
            "connection_declared": "false",
            "theorem_zero_signed": "false",
            "missing_for_claim": "MISSING_M_C;MISSING_POSITIVITY;MISSING_DELTA_GAMMA_ZERO_OR_BOUND;MISSING_PROJECTIVE_BOUNDARY_CONTROL",
            "source_ids": "SRC3079_12_1832_tq_zero;SRC3079_17_1833_distortion",
        }
    ),
    base(
        {
            "connection_id": "DCD3079_3_verdict",
            "required_declaration": "one derived-connection or metric-affine-repair route closes",
            "current_evidence": "all routes remain conditional, fail-open or template-only",
            "current_status": "DERIVED_CONNECTION_DECLARATION_NOT_SIGNED",
            "connection_declared": "false",
            "theorem_zero_signed": "false",
            "missing_for_claim": "MISSING_DERIVED_CONNECTION_OR_DYNAMICAL_ZERO_THEOREM",
            "source_ids": "SRC3079_07_3075_nogamma;SRC3079_12_1832_tq_zero;SRC3079_17_1833_distortion",
        }
    ),
]

source_current_rows = [
    base(
        {
            "current_id": "SRCUR3079_0_no_hypermomentum",
            "required_silence": "delta S_matter/delta Gamma_independent = 0 for matter, light, spin, source, clock, orbital and readout sectors",
            "current_evidence": "no-hypermomentum remains unsigned; spin/source/readout currents remain legal",
            "current_status": "NO_HYPERMOMENTUM_NOT_SIGNED",
            "current_silence_signed": "false",
            "missing_for_claim": "MISSING_MATTER_ACTION_DOMAIN;MISSING_SPIN_TORSION_EXCLUSION;MISSING_SOURCE_READOUT_CONNECTION_CURRENT_EXCLUSION",
            "source_ids": "SRC3079_08_3075_nohyper;SRC3079_16_1833_hyper",
        }
    ),
    base(
        {
            "current_id": "SRCUR3079_1_DeltaGamma_total",
            "required_silence": "Delta_Gamma_total := delta(S_matter+S_source+S_readout)/delta Gamma is zero or source-bounded",
            "current_evidence": "1833 staged Delta_Gamma_total as a nonclaim source row",
            "current_status": "MISSING_PARENT_ZERO_THEOREM_OR_NUMERIC_BOUND",
            "current_silence_signed": "false",
            "missing_for_claim": "MISSING_HYPERMOMENTUM_UNITS;MISSING_CONNECTION_VARIATION_NORMALIZATION;MISSING_WEAK_FIELD_MAP",
            "source_ids": "SRC3079_16_1833_hyper",
        }
    ),
    base(
        {
            "current_id": "SRCUR3079_2_projective_boundary",
            "required_silence": "projective trace and boundary-supported connection modes are fixed, gauged or projected silent",
            "current_evidence": "projective and boundary kernels remain open",
            "current_status": "KERNEL_NOT_FIXED",
            "current_silence_signed": "false",
            "missing_for_claim": "MISSING_PROJECTIVE_INVARIANCE;MISSING_BOUNDARY_NO_FLUX;MISSING_SOURCE_SUPPORT_MAP",
            "source_ids": "SRC3079_12_1832_tq_zero;SRC3079_18_run_p4_gates",
        }
    ),
    base(
        {
            "current_id": "SRCUR3079_3_verdict",
            "required_silence": "all source/current clauses close before the metric-affine zero route can kill C",
            "current_evidence": "source current is the right-hand side obstruction",
            "current_status": "SOURCE_CURRENT_SILENCE_NOT_SIGNED",
            "current_silence_signed": "false",
            "missing_for_claim": "MISSING_NO_HYPERMOMENTUM_OR_DELTAGAMMA_BOUND",
            "source_ids": "SRC3079_08_3075_nohyper;SRC3079_15_1833_decision;SRC3079_16_1833_hyper",
        }
    ),
]

tq_acquisition_rows = [
    base(
        {
            "acquisition_id": "TQAQ3079_0_c_T",
            "quantity": "c_T",
            "operator_or_norm": "torsion quadratic/linearized residual channel, including irreducible torsion decomposition",
            "required_source": "parent coefficient value or zero theorem, units, EH/connection scale normalization and torsion-to-observable map",
            "current_status": "TEMPLATE_ONLY_NONCLAIM",
            "numeric_ready": "false",
            "bound_ready": "false",
            "missing_for_claim": "MISSING_PARENT_VALUE_OR_ZERO_THEOREM;MISSING_UNITS;MISSING_NORMALIZATION;MISSING_TORSION_TO_PPN_WEP_CLOCK_MAP",
            "source_ids": "SRC3079_13_1832_coeff;SRC3079_20_run_templates",
        }
    ),
    base(
        {
            "acquisition_id": "TQAQ3079_1_T_bar",
            "quantity": "T_bar",
            "operator_or_norm": "arena-specific torsion amplitude/norm",
            "required_source": "local branch torsion amplitude or experimental bound translated into the same norm and length scale",
            "current_status": "MISSING_AMPLITUDE",
            "numeric_ready": "false",
            "bound_ready": "false",
            "missing_for_claim": "MISSING_T_BAR;MISSING_ARENA_DOMAIN;MISSING_SCALE_DEPENDENCE",
            "source_ids": "SRC3079_04_3078_tq_numeric;SRC3079_19_run_demotions",
        }
    ),
    base(
        {
            "acquisition_id": "TQAQ3079_2_c_Q",
            "quantity": "c_Q",
            "operator_or_norm": "nonmetricity quadratic/linearized residual channel, including Weyl/shear split",
            "required_source": "parent coefficient value or zero theorem, units, clock/rod/EH normalization and nonmetricity-to-observable map",
            "current_status": "TEMPLATE_ONLY_NONCLAIM",
            "numeric_ready": "false",
            "bound_ready": "false",
            "missing_for_claim": "MISSING_PARENT_VALUE_OR_ZERO_THEOREM;MISSING_UNITS;MISSING_CLOCK_ROD_OR_EH_NORMALIZATION;MISSING_NONMETRICITY_TO_CLOCK_LIGHTCONE_MAP",
            "source_ids": "SRC3079_13_1832_coeff;SRC3079_20_run_templates",
        }
    ),
    base(
        {
            "acquisition_id": "TQAQ3079_3_Q_bar",
            "quantity": "Q_bar",
            "operator_or_norm": "arena-specific nonmetricity amplitude/norm with trace and tracefree split",
            "required_source": "local branch nonmetricity amplitude or experimental bound translated into the same norm and length scale",
            "current_status": "MISSING_AMPLITUDE",
            "numeric_ready": "false",
            "bound_ready": "false",
            "missing_for_claim": "MISSING_Q_BAR;MISSING_ARENA_DOMAIN;MISSING_TRACE_AND_TRACEFREE_SPLIT",
            "source_ids": "SRC3079_04_3078_tq_numeric;SRC3079_19_run_demotions",
        }
    ),
    base(
        {
            "acquisition_id": "TQAQ3079_4_c_TQ",
            "quantity": "c_TQ",
            "operator_or_norm": "mixed torsion-nonmetricity contraction after symmetry decomposition",
            "required_source": "parent coefficient value or proof mixed contraction is forbidden, units and mixed-operator observable map",
            "current_status": "TEMPLATE_ONLY_NONCLAIM",
            "numeric_ready": "false",
            "bound_ready": "false",
            "missing_for_claim": "MISSING_PARENT_VALUE_OR_ZERO_THEOREM;MISSING_UNITS;MISSING_OPERATOR_BASIS;MISSING_MIXED_OPERATOR_MAP",
            "source_ids": "SRC3079_13_1832_coeff;SRC3079_20_run_templates",
        }
    ),
    base(
        {
            "acquisition_id": "TQAQ3079_5_projection_units",
            "quantity": "common_units_and_arena_projection",
            "operator_or_norm": "T/Q/TQ residual projection into R10, PPN, WEP, clock and orbital arenas",
            "required_source": "common unit ledger and weak-field map fixed before comparing against data",
            "current_status": "MISSING_WEAK_FIELD_MAP_AND_BOUND_PROJECTION",
            "numeric_ready": "false",
            "bound_ready": "false",
            "missing_for_claim": "MISSING_COMMON_UNITS;MISSING_PLOC_MAP;MISSING_OBSERVABLE_RESPONSE;MISSING_SOURCE_BACKED_BOUNDS",
            "source_ids": "SRC3079_11_1831_weakmap;SRC3079_20_run_templates",
        }
    ),
]

historical_rows = [
    base(
        {
            "trail_id": "HIST3079_0_1831",
            "prior_checkpoint": "1831",
            "prior_result": "parent field inventory certificate not proven",
            "current_use": "confirms 3079 field-list signature remains unsigned, not newly discovered",
            "status": "CONSISTENT_WITH_3079",
            "source_ids": "SRC3079_09_1831_inventory",
        }
    ),
    base(
        {
            "trail_id": "HIST3079_1_1832",
            "prior_checkpoint": "1832",
            "prior_result": "TQ zero theorem not proven; first coefficient rows template-only",
            "current_use": "adds distortion identity and c_T/c_Q/c_TQ source requirements",
            "status": "CONSISTENT_WITH_3079",
            "source_ids": "SRC3079_12_1832_tq_zero;SRC3079_13_1832_coeff",
        }
    ),
    base(
        {
            "trail_id": "HIST3079_2_1833",
            "prior_checkpoint": "1833",
            "prior_result": "distortion equation owner not proven; Delta_Gamma source row staged",
            "current_use": "prevents repeating the same failed distortion-owner target; points next to no-hypermomentum/DeltaGamma",
            "status": "CONSISTENT_WITH_3079_NEXT_TARGET",
            "source_ids": "SRC3079_15_1833_decision;SRC3079_16_1833_hyper;SRC3079_17_1833_distortion",
        }
    ),
]

local_consequence_rows = [
    base(
        {
            "impact_id": "LGC3079_0_GR_reduction",
            "question": "Did 3079 derive local GR via the metric/coframe field list?",
            "answer": "No. It preserved the exact conditional route but found no parent-signed field list, connection declaration or source-current silence.",
            "local_gr_claim": "false",
            "next_requirement": "no-hypermomentum/source-readout functor or Delta_Gamma bound",
        }
    ),
    base(
        {
            "impact_id": "LGC3079_1_TQ_residual",
            "question": "Can K_P4_TQ be zeroed or bounded?",
            "answer": "Not yet. Zero theorem is conditional; numeric source rows remain template-only.",
            "local_gr_claim": "false",
            "next_requirement": "either sign T=Q=0 branch or fill c_T,T_bar,c_Q,Q_bar,c_TQ and projection rows",
        }
    ),
    base(
        {
            "impact_id": "LGC3079_2_test_status",
            "question": "Can R10, PPN, WEP, clock or orbital tests claim pass?",
            "answer": "No. Delta_K, P4_TQ, other P4 components, source-current silence and arena maps remain open.",
            "local_gr_claim": "false",
            "next_requirement": "source-current and weak-field projection rows",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3079_0_field_list",
            "decision": "local geometry field-list signature not signed",
            "reason": "the metric/coframe-only theorem is exact but the parent action field list and variation domain are not signed",
            "consequence": "T=Q=0 remains conditional",
            "next_action": "do not claim K_P4_TQ=0 or local GR",
        }
    ),
    base(
        {
            "decision_id": "DEC3079_1_TQ_acquisition",
            "decision": "TQ bound-source acquisition rows staged",
            "reason": "c_T, T_bar, c_Q, Q_bar, c_TQ, units and projection maps remain missing",
            "consequence": "TQ residual can become empirical only after coefficient/source rows are real",
            "next_action": "keep all TQ rows nonclaim",
        }
    ),
    base(
        {
            "decision_id": "DEC3079_2_prior_trail",
            "decision": "do not repeat distortion-owner target blindly",
            "reason": "1833 already found distortion equation owner not proven and staged Delta_Gamma source current",
            "consequence": "the next useful target is source-current silence/bounds",
            "next_action": "3080-Y5-R2FR-no-hypermomentum-source-readout-functor-or-DeltaGamma-bound-under-AX1090.md",
        }
    ),
]

claim_rows = [
    base(
        {
            "claim_id": "CLAIM3079_0_field_list",
            "claim": "local parent field list is metric/coframe-only",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "field-list signature remains unsigned",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3079_1_TQ_zero",
            "claim": "T=Q=0 and K_P4_TQ=0",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "the zero theorem is conditional but not parent-signed",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3079_2_TQ_bound",
            "claim": "K_P4_TQ has a numeric source-backed bound",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "coefficient, amplitude, units and projection rows are template-only",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3079_3_local_tests",
            "claim": "local GR/Newton/PPN/R10/clock/WEP/orbital pass",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "Delta_K, P4, source-current and arena-map gates remain open",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3079_0_3080",
            "next_checkpoint": "3080-Y5-R2FR-no-hypermomentum-source-readout-functor-or-DeltaGamma-bound-under-AX1090.md",
            "script": "scripts/Y5_R2FR_no_hypermomentum_source_readout_functor_or_DeltaGamma_bound_under_AX1090_3080.py",
            "mission": "try to prove matter/source/readout sectors carry no independent connection current; if not, stage Delta_Gamma_total component bounds with units and weak-field maps",
            "starting_equation": "M_C C = Delta_Gamma + boundary + projective; T,Q are projections of C",
            "claim_policy": "no C=0, T=Q=0, K_P4_TQ=0 or local-GR claim unless Delta_Gamma and boundary/projective channels are zero or bounded",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["field_list"], field_list_rows)
write_csv(OUTPUTS["connection"], connection_rows)
write_csv(OUTPUTS["source_current"], source_current_rows)
write_csv(OUTPUTS["tq_acquisition"], tq_acquisition_rows)
write_csv(OUTPUTS["historical"], historical_rows)
write_csv(OUTPUTS["local_consequence"], local_consequence_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["claim_status"], claim_rows)
write_csv(OUTPUTS["next"], next_rows)

copy_csv(OUTPUTS["field_list"], BRANCH_OUTPUTS["field_list_copy"])
copy_csv(OUTPUTS["connection"], BRANCH_OUTPUTS["connection_copy"])
copy_csv(OUTPUTS["source_current"], BRANCH_OUTPUTS["source_current_copy"])
copy_csv(OUTPUTS["tq_acquisition"], BRANCH_OUTPUTS["tq_acquisition_copy"])
copy_csv(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

branch_rows = [
    base(
        {
            "copy_id": copy_id,
            "source_path": str(source_path),
            "copy_path": str(destination_path),
            "copy_exists": str(destination_path.exists()),
            "copy_parse_ok": str(csv_ok(destination_path)),
            "status": "COPIED_NONCLAIM",
        }
    )
    for copy_id, source_path, destination_path in [
        ("BC3079_0_field_list", OUTPUTS["field_list"], BRANCH_OUTPUTS["field_list_copy"]),
        ("BC3079_1_connection", OUTPUTS["connection"], BRANCH_OUTPUTS["connection_copy"]),
        ("BC3079_2_source_current", OUTPUTS["source_current"], BRANCH_OUTPUTS["source_current_copy"]),
        ("BC3079_3_tq_acquisition", OUTPUTS["tq_acquisition"], BRANCH_OUTPUTS["tq_acquisition_copy"]),
        ("BC3079_4_next", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
]
write_csv(OUTPUTS["branches"], branch_rows)
write_csv(
    OUTPUTS["validation"],
    [
        base(
            {
                "validation_id": "VAL3079_PRE",
                "passed": "False",
                "requirement": "placeholder overwritten by final validation",
                "evidence": "generator ordering guard",
            }
        )
    ],
)
DOC.write_text("# 3079 draft\n", encoding="utf-8")

remove_pycache()
dotg_hash_after = file_hash(DOTG_TARGET)
generated_csvs = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values())
generated_rows = (
    field_list_rows
    + connection_rows
    + source_current_rows
    + tq_acquisition_rows
    + historical_rows
    + local_consequence_rows
    + decision_rows
    + claim_rows
    + next_rows
)
formalization_output_count = sum(1 for output_path in generated_csvs + [DOC] if under(output_path, FORMALIZATION))
required_tq_quantities = {"c_T", "T_bar", "c_Q", "Q_bar", "c_TQ", "common_units_and_arena_projection"}

validation_rows = [
    base(
        {
            "validation_id": "VAL3079_00_sources_exist",
            "passed": str(all(row["exists"] == "True" for row in source_register)),
            "requirement": "all cited source paths exist",
            "evidence": OUTPUTS["sources"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3079_01_sources_parse",
            "passed": str(all(row["parse_ok"] == "True" for row in source_register)),
            "requirement": "all cited CSV sources parse and markdown sources exist",
            "evidence": OUTPUTS["sources"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3079_02_csv_parse",
            "passed": str(all(csv_ok(output_path) for output_path in generated_csvs)),
            "requirement": "all generated and branch-copy CSVs parse cleanly",
            "evidence": "csv.DictReader parse check",
        }
    ),
    base(
        {
            "validation_id": "VAL3079_03_field_list_not_signed",
            "passed": str(not any(boolish(row["signature_signed"]) or boolish(row["parent_signed"]) or boolish(row["inventory_signed"]) for row in field_list_rows)),
            "requirement": "local geometry field-list signature remains unsigned",
            "evidence": OUTPUTS["field_list"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3079_04_connection_not_declared",
            "passed": str(not any(boolish(row["connection_declared"]) or boolish(row["theorem_zero_signed"]) for row in connection_rows)),
            "requirement": "derived connection or metric-affine zero route remains unsigned",
            "evidence": OUTPUTS["connection"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3079_05_source_current_not_silent",
            "passed": str(not any(boolish(row["current_silence_signed"]) for row in source_current_rows)),
            "requirement": "source/readout independent connection current silence remains unsigned",
            "evidence": OUTPUTS["source_current"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3079_06_tq_acquisition_complete_nonclaim",
            "passed": str(required_tq_quantities.issubset({row["quantity"] for row in tq_acquisition_rows}) and not has_claim_true(tq_acquisition_rows)),
            "requirement": "TQ acquisition rows include c_T, T_bar, c_Q, Q_bar, c_TQ and projection units, all nonclaim",
            "evidence": OUTPUTS["tq_acquisition"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3079_07_prior_trail_reconciled",
            "passed": str({"1831", "1832", "1833"}.issubset({row["prior_checkpoint"] for row in historical_rows})),
            "requirement": "prior 1831/1832/1833 trail is reconciled rather than repeated blindly",
            "evidence": OUTPUTS["historical"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3079_08_no_local_claim",
            "passed": str(not has_claim_true(claim_rows + decision_rows + local_consequence_rows)),
            "requirement": "no K_P4_TQ zero, local-GR, PPN, R10, clock, WEP or orbital claim is promoted",
            "evidence": OUTPUTS["claim_status"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3079_09_next_target_selected",
            "passed": str(next_rows[0]["next_checkpoint"].startswith("3080-Y5-R2FR-no-hypermomentum-source-readout")),
            "requirement": "next target moves to no-hypermomentum/source-readout functor or DeltaGamma bound",
            "evidence": OUTPUTS["next"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3079_10_branch_copies_exist",
            "passed": str(all(row["copy_exists"] == "True" and row["copy_parse_ok"] == "True" for row in branch_rows)),
            "requirement": "branch copies exist and parse",
            "evidence": OUTPUTS["branches"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3079_11_dotg_unchanged",
            "passed": str(dotg_hash_before == dotg_hash_after),
            "requirement": "P8_time_drift_residual_or_zero.csv is not modified",
            "evidence": f"{dotg_hash_before}->{dotg_hash_after}",
        }
    ),
    base(
        {
            "validation_id": "VAL3079_12_outputs_under_post_checkpoint",
            "passed": str(all(under(output_path, ROOT) for output_path in generated_csvs + [DOC])),
            "requirement": "all outputs are under post-checkpoint-work",
            "evidence": "path containment check",
        }
    ),
    base(
        {
            "validation_id": "VAL3079_13_no_formalization_outputs",
            "passed": str(formalization_output_count == 0),
            "requirement": "formalization-workbench modified-file count for 3079 outputs remains zero",
            "evidence": f"formalization_3079_output_paths={formalization_output_count}",
        }
    ),
    base(
        {
            "validation_id": "VAL3079_14_pycache_absent",
            "passed": str(not PYCACHE.exists()),
            "requirement": "scripts __pycache__ is absent at generator completion",
            "evidence": str(PYCACHE),
        }
    ),
    base(
        {
            "validation_id": "VAL3079_15_doc_written",
            "passed": str(DOC.exists()),
            "requirement": "checkpoint markdown document is written",
            "evidence": str(DOC),
        }
    ),
    base(
        {
            "validation_id": "VAL3079_16_no_claim_fields_true",
            "passed": str(not has_claim_true(generated_rows)),
            "requirement": "no generated non-validation row contains a true claim/ready field",
            "evidence": "claim field scan",
        }
    ),
]

write_csv(OUTPUTS["validation"], validation_rows)

doc_text = f"""# 3079 - Local Geometry Field-List Signature or TQ Bound Source Acquisition

Status: `Y5_R2FR_3079_field_list_not_signed_DeltaGamma_next`

Generated: `{RUN_UTC}`

## Verdict

3079 tried the cleanest live GR-reduction move left after 3078: sign the local geometry field list so that the observed connection is derived from `g_obs/e_obs`, making torsion and nonmetricity vanish kinematically.

This still does **not** close. The conditional theorem is exact, but the current corpus does not parent-sign the local field list, the no-independent-`Gamma/omega/C` slot, the derived-connection declaration, or source/readout connection-current silence.

The useful correction is that 3079 now reconciles the fresh 3078 route with the older 1831/1832/1833 trail. We should not blindly repeat the distortion-equation-owner target: the older trail already found that `M_C C = Delta_Gamma + boundary + projective` is not owned. The next useful obstruction is therefore the right-hand side: no-hypermomentum/source-readout current silence or a real `Delta_Gamma` bound.

So 3079 does **not** claim a metric/coframe-only parent field list, `T=Q=0`, `K_P4_TQ=0`, local GR, Newtonian recovery, PPN, R10, clocks, WEP, or orbital success.

## Field-List Signature Audit

{md_table(field_list_rows, ["signature_id", "current_status", "signature_signed", "would_buy", "missing_for_claim"])}

## Derived Connection Declaration

{md_table(connection_rows, ["connection_id", "current_status", "connection_declared", "missing_for_claim"])}

## Source/Readout Connection Current

{md_table(source_current_rows, ["current_id", "current_status", "current_silence_signed", "missing_for_claim"])}

## TQ Bound Source Acquisition

{md_table(tq_acquisition_rows, ["acquisition_id", "quantity", "current_status", "numeric_ready", "missing_for_claim"])}

## Prior Trail Reconciliation

{md_table(historical_rows, ["trail_id", "prior_checkpoint", "prior_result", "current_use", "status"])}

## Local GR Consequence

{md_table(local_consequence_rows, ["impact_id", "question", "answer", "next_requirement"])}

## Decision

{md_table(decision_rows, ["decision_id", "decision", "reason", "next_action"])}

## Claim Status

{md_table(claim_rows, ["claim_id", "claim", "claim_active", "status", "reason"])}

## Next Target

{md_table(next_rows, ["next_id", "next_checkpoint", "mission", "starting_equation", "claim_policy"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}

## Files

- Source register: `{OUTPUTS["sources"]}`
- Field-list signature audit: `{OUTPUTS["field_list"]}`
- Derived connection audit: `{OUTPUTS["connection"]}`
- Source/readout current audit: `{OUTPUTS["source_current"]}`
- TQ acquisition rows: `{OUTPUTS["tq_acquisition"]}`
- Prior trail reconciliation: `{OUTPUTS["historical"]}`
- Local GR consequence ledger: `{OUTPUTS["local_consequence"]}`
- Claim status: `{OUTPUTS["claim_status"]}`
- Next target: `{OUTPUTS["next"]}`
- Validation: `{OUTPUTS["validation"]}`
- Branch copy: `{BRANCH_OUTPUTS["field_list_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["connection_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["source_current_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["tq_acquisition_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["next_copy"]}`
"""

DOC.write_text(doc_text, encoding="utf-8")
print(f"Wrote {DOC}")
print(f"Wrote {OUTPUTS['validation']}")
print(f"Validation passed {sum(1 for row in validation_rows if row['passed'] == 'True')}/{len(validation_rows)}")

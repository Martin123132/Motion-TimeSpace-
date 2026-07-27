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
FORMALIZATION = PROJECT / "formalization-workbench"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3078"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3078-Y5-R2FR-P4-TQ-first-source-or-theorem-zero-under-AX1090.md"
DOTG_TARGET = RESIDUALS / "P8_time_drift_residual_or_zero.csv"

SOURCE_PATHS = {
    "SRC3078_00_3077_doc": ROOT / "3077-Y5-R2FR-DeltaK-component-birth-certificate-or-P4-numeric-source-fill-under-AX1090.md",
    "SRC3078_01_3077_next": RESIDUALS / "P8_Y5_R2FR_3077_NEXT_TARGET.csv",
    "SRC3078_02_3077_p4": RESIDUALS / "P8_Y5_R2FR_3077_P4_SOURCE_FILL_QUEUE_NONCLAIM.csv",
    "SRC3078_03_3077_local": RESIDUALS / "P8_Y5_R2FR_3077_LOCAL_ARENA_BLOCKER_LEDGER.csv",
    "SRC3078_04_3075_p4": RESIDUALS / "P8_Y5_R2FR_3075_P4_CONNECTION_VECTOR_NONCLAIM.csv",
    "SRC3078_05_3074_p4": RESIDUALS / "P8_Y5_R2FR_3074_P4_CONNECTION_FALLBACK_VECTOR_NONCLAIM.csv",
    "SRC3078_06_3074_kconn": RESIDUALS / "P8_Y5_R2FR_3074_KCONN_BOUND_VECTOR_NONCLAIM.csv",
    "SRC3078_07_3075_nogamma": RESIDUALS / "P8_Y5_R2FR_3075_NO_INDEPENDENT_GAMMA_AUDIT.csv",
    "SRC3078_08_3075_inventory": RESIDUALS / "P8_Y5_R2FR_3075_PARENT_FIELD_INVENTORY_AUDIT.csv",
    "SRC3078_09_3075_nohyper": RESIDUALS / "P8_Y5_R2FR_3075_NO_HYPERMOMENTUM_AUDIT.csv",
    "SRC3078_10_3076_deltak": RESIDUALS / "P8_Y5_R2FR_3076_DELTAK_OBSTRUCTION_VECTOR_NONCLAIM.csv",
    "SRC3078_11_dotg_target": DOTG_TARGET,
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3078_SOURCE_REGISTER.csv",
    "theorem_zero": RESIDUALS / "P8_Y5_R2FR_3078_P4_TQ_THEOREM_ZERO_AUDIT.csv",
    "numeric_source": RESIDUALS / "P8_Y5_R2FR_3078_P4_TQ_NUMERIC_SOURCE_AUDIT.csv",
    "bound_schema": RESIDUALS / "P8_Y5_R2FR_3078_P4_TQ_BOUND_SCHEMA_NONCLAIM.csv",
    "arena_map": RESIDUALS / "P8_Y5_R2FR_3078_TQ_LOCAL_ARENA_MAP_NONCLAIM.csv",
    "geometry_gap": RESIDUALS / "P8_Y5_R2FR_3078_GEOMETRY_FIELD_LIST_GAP_LEDGER.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3078_DECISION_LEDGER.csv",
    "claim_status": RESIDUALS / "P8_Y5_R2FR_3078_CLAIM_STATUS.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3078_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3078_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3078_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "theorem_zero_copy": PARENT_ACTION / "P4_TQ_theorem_zero_audit_3078_NOT_SIGNED.csv",
    "geometry_gap_copy": PARENT_ACTION / "geometry_field_list_gap_3078_NOT_SIGNED.csv",
    "numeric_source_copy": LOCAL_BOUNDS / "P4_TQ_numeric_source_audit_3078_NONCLAIM.csv",
    "bound_schema_copy": LOCAL_BOUNDS / "P4_TQ_bound_schema_3078_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3078_local_geometry_field_list_signature_or_TQ_bound_source_NEXT_NONCLAIM.csv",
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
        "theorem_zero_signed",
        "parent_signed",
        "inventory_signed",
        "numeric_ready",
        "bound_ready",
        "arena_projection_ready",
        "local_gr_claim",
        "p4_tq_zero_claim",
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
            "role": "P4_TQ_theorem_zero_or_source_evidence" if source_id != "SRC3078_11_dotg_target" else "append_guard_target",
            "status": "PRESENT" if source_path.exists() else "MISSING_SOURCE",
        }
    )
    for source_id, source_path in SOURCE_PATHS.items()
]

theorem_zero_rows = [
    base(
        {
            "theorem_id": "TQZ3078_0_conditional_geometry_lemma",
            "clause": "metric/coframe-only local geometry",
            "statement": "If the parent local configuration space contains only g_obs/e_obs and the connection is the derived Levi-Civita/spin connection, then torsion T and nonmetricity Q are kinematically zero.",
            "math_conditional_ok": "true",
            "theorem_zero_signed": "false",
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "missing_for_claim": "MISSING_PARENT_ACTION_FIELD_LIST;MISSING_DERIVED_CONNECTION_DECLARATION",
            "source_ids": "SRC3078_07_3075_nogamma;SRC3078_08_3075_inventory",
        }
    ),
    base(
        {
            "theorem_id": "TQZ3078_1_parent_inventory_signature",
            "clause": "no independent Gamma/omega slot",
            "statement": "The parent action must explicitly exclude independent Gamma/omega or place it in a constrained algebraic sector.",
            "math_conditional_ok": "false",
            "theorem_zero_signed": "false",
            "current_status": "NOT_SIGNED",
            "missing_for_claim": "MISSING_NO_INDEPENDENT_GAMMA_SLOT;MISSING_VARIATION_DOMAIN;MISSING_NO_POSTHOC_DELETION_GUARD",
            "source_ids": "SRC3078_07_3075_nogamma;SRC3078_08_3075_inventory",
        }
    ),
    base(
        {
            "theorem_id": "TQZ3078_2_metric_affine_fork",
            "clause": "Palatini/metric-affine fallback",
            "statement": "If an independent connection is allowed, its field equation must force Levi-Civita/projective harmless form or the P4_TQ residual must be scored.",
            "math_conditional_ok": "true",
            "theorem_zero_signed": "false",
            "current_status": "FORK_RETAINED_NOT_CLOSED",
            "missing_for_claim": "MISSING_PALATINI_EH_PARENT;MISSING_ZERO_SOURCE_CONNECTION_EQUATION;MISSING_PROJECTIVE_SILENCE",
            "source_ids": "SRC3078_07_3075_nogamma;SRC3078_06_3074_kconn",
        }
    ),
    base(
        {
            "theorem_id": "TQZ3078_3_source_readout_silence",
            "clause": "no source/readout connection current",
            "statement": "Source/readout transfer must not reintroduce torsion/nonmetricity through a hidden connection current.",
            "math_conditional_ok": "false",
            "theorem_zero_signed": "false",
            "current_status": "NOT_PARENT_SIGNED",
            "missing_for_claim": "MISSING_SOURCE_CONNECTION_CURRENT_EXCLUSION;MISSING_READOUT_DOMAIN;MISSING_NO_SOURCE_LABEL_MORPHISM",
            "source_ids": "SRC3078_09_3075_nohyper",
        }
    ),
    base(
        {
            "theorem_id": "TQZ3078_4_verdict",
            "clause": "K_P4_TQ theorem-zero",
            "statement": "K_P4_TQ can be set to zero only if all geometry, connection and source/readout clauses close in one branch.",
            "math_conditional_ok": "false",
            "theorem_zero_signed": "false",
            "current_status": "THEOREM_ZERO_NOT_SIGNED",
            "missing_for_claim": "MISSING_PARENT_FIELD_INVENTORY;MISSING_NO_GAMMA;MISSING_NO_HYPERMOMENTUM_OR_SOURCE_CURRENT_SILENCE",
            "source_ids": "SRC3078_04_3075_p4;SRC3078_07_3075_nogamma;SRC3078_08_3075_inventory",
        }
    ),
]

numeric_source_rows = [
    base(
        {
            "source_id": "TQNS3078_0_c_T",
            "quantity": "c_T",
            "meaning": "torsion-to-local-residual coefficient",
            "required_source": "weak-field/operator derivation mapping torsion norm to q_loc/local observable residual",
            "current_status": "MISSING_NUMERIC_OR_THEOREM_SOURCE",
            "numeric_ready": "false",
            "missing_for_claim": "MISSING_C_T;MISSING_UNITS;MISSING_OPERATOR_NORM",
            "source_ids": "SRC3078_04_3075_p4;SRC3078_05_3074_p4",
        }
    ),
    base(
        {
            "source_id": "TQNS3078_1_T_bar",
            "quantity": "T_bar",
            "meaning": "arena-specific torsion amplitude/norm",
            "required_source": "local branch torsion norm or experimental upper bound translated into the same units",
            "current_status": "MISSING_AMPLITUDE",
            "numeric_ready": "false",
            "missing_for_claim": "MISSING_T_BAR;MISSING_ARENA_DOMAIN;MISSING_SCALE_DEPENDENCE",
            "source_ids": "SRC3078_04_3075_p4",
        }
    ),
    base(
        {
            "source_id": "TQNS3078_2_c_Q",
            "quantity": "c_Q",
            "meaning": "nonmetricity-to-local-residual coefficient",
            "required_source": "weak-field/operator derivation mapping nonmetricity norm to rods/clocks/lightcone/q_loc residual",
            "current_status": "MISSING_NUMERIC_OR_THEOREM_SOURCE",
            "numeric_ready": "false",
            "missing_for_claim": "MISSING_C_Q;MISSING_UNITS;MISSING_ROD_CLOCK_LIGHTCONE_MAP",
            "source_ids": "SRC3078_04_3075_p4;SRC3078_05_3074_p4",
        }
    ),
    base(
        {
            "source_id": "TQNS3078_3_Q_bar",
            "quantity": "Q_bar",
            "meaning": "arena-specific nonmetricity amplitude/norm",
            "required_source": "local branch nonmetricity norm or experimental upper bound translated into the same units",
            "current_status": "MISSING_AMPLITUDE",
            "numeric_ready": "false",
            "missing_for_claim": "MISSING_Q_BAR;MISSING_ARENA_DOMAIN;MISSING_TRACE_AND_TRACEFREE_SPLIT",
            "source_ids": "SRC3078_04_3075_p4",
        }
    ),
    base(
        {
            "source_id": "TQNS3078_4_units_projection",
            "quantity": "units_and_arena_projection",
            "meaning": "common units and local observable projection for K_P4_TQ",
            "required_source": "unit ledger and projection map into R10, PPN, clock/WEP/orbital arenas",
            "current_status": "MISSING_UNITS_AND_PROJECTION",
            "numeric_ready": "false",
            "missing_for_claim": "MISSING_COMMON_UNITS;MISSING_PLOC_MAP;MISSING_OBSERVABLE_RESPONSE",
            "source_ids": "SRC3078_03_3077_local;SRC3078_06_3074_kconn",
        }
    ),
]

bound_schema_rows = [
    base(
        {
            "bound_id": "TQB3078_0_symbolic",
            "quantity": "K_P4_TQ",
            "formula": "K_P4_TQ <= c_T T_bar + c_Q Q_bar",
            "status": "SCHEMA_ONLY_NONCLAIM",
            "bound_ready": "false",
            "numeric_ready": "false",
            "theorem_zero_signed": "false",
            "units": "MISSING_COMMON_UNITS",
            "missing_for_claim": "MISSING_C_T;MISSING_T_BAR;MISSING_C_Q;MISSING_Q_BAR;MISSING_UNITS",
            "source_ids": "SRC3078_04_3075_p4;SRC3078_05_3074_p4",
        }
    ),
    base(
        {
            "bound_id": "TQB3078_1_theorem_zero_limit",
            "quantity": "K_P4_TQ",
            "formula": "if T_bar=0 and Q_bar=0 by parent geometry theorem, then K_P4_TQ=0",
            "status": "CONDITIONAL_ONLY",
            "bound_ready": "false",
            "numeric_ready": "false",
            "theorem_zero_signed": "false",
            "units": "not_needed_if_parent_zero_theorem_signed",
            "missing_for_claim": "MISSING_PARENT_GEOMETRY_THEOREM_SIGNATURE",
            "source_ids": "SRC3078_07_3075_nogamma;SRC3078_08_3075_inventory",
        }
    ),
    base(
        {
            "bound_id": "TQB3078_2_total_interface",
            "quantity": "K_P4_bar",
            "formula": "K_P4_bar = K_P4_TQ + K_P4_spin + K_P4_proj + K_P4_QW + K_P4_QTF + K_P4_H",
            "status": "TOTAL_INTERFACE_RETAINED_NONCLAIM",
            "bound_ready": "false",
            "numeric_ready": "false",
            "theorem_zero_signed": "false",
            "units": "MISSING_COMMON_UNITS",
            "missing_for_claim": "MISSING_REMAINING_P4_COMPONENTS;MISSING_DELTAK_AND_PLOC_CLOSURE",
            "source_ids": "SRC3078_02_3077_p4;SRC3078_04_3075_p4",
        }
    ),
]

arena_map_rows = [
    base(
        {
            "arena_id": "TQA3078_0_R10",
            "arena": "R10 short-range",
            "needed_projection": "map torsion/nonmetricity residual to alpha(lambda) or force-gradient amplitude",
            "current_status": "NOT_PROJECTABLE",
            "arena_projection_ready": "false",
            "local_gr_claim": "false",
            "missing_for_claim": "MISSING_C_T;MISSING_T_BAR;MISSING_C_Q;MISSING_Q_BAR;MISSING_LENGTH_SCALE_MAP",
        }
    ),
    base(
        {
            "arena_id": "TQA3078_1_PPN_orbital",
            "arena": "PPN/orbital",
            "needed_projection": "map T/Q channels to preferred-frame, shear, trace and orbital residual coefficients",
            "current_status": "NOT_PROJECTABLE",
            "arena_projection_ready": "false",
            "local_gr_claim": "false",
            "missing_for_claim": "MISSING_WEAK_FIELD_MAP;MISSING_COMPONENT_SPLIT;MISSING_UNITS",
        }
    ),
    base(
        {
            "arena_id": "TQA3078_2_clock_WEP",
            "arena": "clock/WEP",
            "needed_projection": "map Weyl/shear/nonmetricity and torsion channels to rods, clocks and composition dependence",
            "current_status": "NOT_PROJECTABLE",
            "arena_projection_ready": "false",
            "local_gr_claim": "false",
            "missing_for_claim": "MISSING_CLOCK_ROD_MAP;MISSING_COMPOSITION_COUPLING;MISSING_SOURCE_CURRENT_SILENCE",
        }
    ),
]

geometry_gap_rows = [
    base(
        {
            "gap_id": "GFG3078_0_field_list",
            "required_signature": "parent action field list contains g_obs/e_obs and excludes independent Gamma/omega in the local branch",
            "current_status": "CONTRACT_WRITTEN_NOT_PARENT_SIGNED",
            "parent_signed": "false",
            "inventory_signed": "false",
            "why_it_matters": "without this signature, T=0 and Q=0 are conditional, not physical branch facts",
            "missing_for_claim": "MISSING_PARENT_ACTION_FIELD_LIST;MISSING_VARIATION_DOMAIN",
            "source_ids": "SRC3078_08_3075_inventory",
        }
    ),
    base(
        {
            "gap_id": "GFG3078_1_connection_declaration",
            "required_signature": "Gamma/omega is declared derived from g/e, or independent connection equations force harmless Levi-Civita/projective form",
            "current_status": "NO_GAMMA_THEOREM_NOT_CLOSED",
            "parent_signed": "false",
            "inventory_signed": "false",
            "why_it_matters": "this is the direct kill switch for K_P4_TQ",
            "missing_for_claim": "MISSING_DERIVED_CONNECTION_DECLARATION;MISSING_ALGEBRAIC_CONNECTION_EQUATION",
            "source_ids": "SRC3078_07_3075_nogamma",
        }
    ),
    base(
        {
            "gap_id": "GFG3078_2_source_readout",
            "required_signature": "matter/source/readout sectors do not couple to an independent connection current",
            "current_status": "NO_HYPERMOMENTUM_NOT_SIGNED",
            "parent_signed": "false",
            "inventory_signed": "false",
            "why_it_matters": "hidden currents can reintroduce torsion/nonmetricity even if the visible geometry looks metric",
            "missing_for_claim": "MISSING_NO_HYPERMOMENTUM_THEOREM;MISSING_SOURCE_READOUT_CONNECTION_CURRENT_EXCLUSION",
            "source_ids": "SRC3078_09_3075_nohyper",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3078_0_conditional_win",
            "decision": "conditional theorem is exact",
            "reason": "metric/coframe-only Levi-Civita geometry gives T=0 and Q=0",
            "consequence": "the derivation route is mathematically clean if the parent field list is signed",
            "next_action": "do not lose this route; turn it into a parent field-list signature target",
        }
    ),
    base(
        {
            "decision_id": "DEC3078_1_no_claim",
            "decision": "K_P4_TQ theorem-zero not signed",
            "reason": "parent action field list, derived connection declaration and source/readout silence are missing",
            "consequence": "K_P4_TQ cannot be set to zero",
            "next_action": "retain symbolic bound K_P4_TQ <= c_T T_bar + c_Q Q_bar",
        }
    ),
    base(
        {
            "decision_id": "DEC3078_2_no_numeric_bound",
            "decision": "numeric TQ bound not ready",
            "reason": "c_T, T_bar, c_Q, Q_bar, units and arena projections are missing",
            "consequence": "R10/PPN/clock/WEP/orbital arenas remain blocked",
            "next_action": "either sign geometry field list or source TQ coefficients",
        }
    ),
    base(
        {
            "decision_id": "DEC3078_3_next",
            "decision": "3079 local geometry field-list signature",
            "reason": "the theorem-zero path is less ugly than source-hunting every torsion/nonmetricity coefficient",
            "consequence": "try to close the direct GR-reduction route before accepting a numeric residual branch",
            "next_action": "3079-Y5-R2FR-local-geometry-field-list-signature-or-TQ-bound-source-acquisition-under-AX1090.md",
        }
    ),
]

claim_rows = [
    base(
        {
            "claim_id": "CLAIM3078_0_TQ_zero",
            "claim": "K_P4_TQ=0",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "the zero theorem is conditional but not parent-signed",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3078_1_TQ_bound",
            "claim": "K_P4_TQ has a numeric bound",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "c_T, T_bar, c_Q, Q_bar and projection units are missing",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3078_2_local_tests",
            "claim": "local GR/Newton/PPN/R10/clock/WEP/orbital pass",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "Delta_K, P4_TQ and other P4 components remain nonclaim",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3078_0_3079",
            "next_checkpoint": "3079-Y5-R2FR-local-geometry-field-list-signature-or-TQ-bound-source-acquisition-under-AX1090.md",
            "script": "scripts/Y5_R2FR_local_geometry_field_list_signature_or_TQ_bound_source_acquisition_under_AX1090_3079.py",
            "mission": "try to sign the local parent field list that makes Gamma/omega derived from g/e and kills torsion/nonmetricity; if not, create source acquisition rows for c_T,T_bar,c_Q,Q_bar",
            "starting_equation": "metric/coframe-only branch => T=0,Q=0 => K_P4_TQ=0, otherwise K_P4_TQ <= c_T T_bar + c_Q Q_bar",
            "claim_policy": "no K_P4_TQ zero, local-GR, PPN, R10, clock, WEP or orbital claim without parent signature or numeric bound rows",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["theorem_zero"], theorem_zero_rows)
write_csv(OUTPUTS["numeric_source"], numeric_source_rows)
write_csv(OUTPUTS["bound_schema"], bound_schema_rows)
write_csv(OUTPUTS["arena_map"], arena_map_rows)
write_csv(OUTPUTS["geometry_gap"], geometry_gap_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["claim_status"], claim_rows)
write_csv(OUTPUTS["next"], next_rows)

copy_csv(OUTPUTS["theorem_zero"], BRANCH_OUTPUTS["theorem_zero_copy"])
copy_csv(OUTPUTS["geometry_gap"], BRANCH_OUTPUTS["geometry_gap_copy"])
copy_csv(OUTPUTS["numeric_source"], BRANCH_OUTPUTS["numeric_source_copy"])
copy_csv(OUTPUTS["bound_schema"], BRANCH_OUTPUTS["bound_schema_copy"])
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
        ("BC3078_0_theorem_zero", OUTPUTS["theorem_zero"], BRANCH_OUTPUTS["theorem_zero_copy"]),
        ("BC3078_1_geometry_gap", OUTPUTS["geometry_gap"], BRANCH_OUTPUTS["geometry_gap_copy"]),
        ("BC3078_2_numeric_source", OUTPUTS["numeric_source"], BRANCH_OUTPUTS["numeric_source_copy"]),
        ("BC3078_3_bound_schema", OUTPUTS["bound_schema"], BRANCH_OUTPUTS["bound_schema_copy"]),
        ("BC3078_4_next", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
]
write_csv(OUTPUTS["branches"], branch_rows)
write_csv(
    OUTPUTS["validation"],
    [
        base(
            {
                "validation_id": "VAL3078_PRE",
                "passed": "False",
                "requirement": "placeholder overwritten by final validation",
                "evidence": "generator ordering guard",
            }
        )
    ],
)
DOC.write_text("# 3078 draft\n", encoding="utf-8")

remove_pycache()
dotg_hash_after = file_hash(DOTG_TARGET)
generated_csvs = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values())
generated_rows = (
    theorem_zero_rows
    + numeric_source_rows
    + bound_schema_rows
    + arena_map_rows
    + geometry_gap_rows
    + decision_rows
    + claim_rows
    + next_rows
)
formalization_output_count = sum(1 for output_path in generated_csvs + [DOC] if under(output_path, FORMALIZATION))

validation_rows = [
    base(
        {
            "validation_id": "VAL3078_00_sources_exist",
            "passed": str(all(row["exists"] == "True" for row in source_register)),
            "requirement": "all cited source paths exist",
            "evidence": OUTPUTS["sources"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3078_01_sources_parse",
            "passed": str(all(row["parse_ok"] == "True" for row in source_register)),
            "requirement": "all cited CSV sources parse and markdown sources exist",
            "evidence": OUTPUTS["sources"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3078_02_csv_parse",
            "passed": str(all(csv_ok(output_path) for output_path in generated_csvs)),
            "requirement": "all generated and branch-copy CSVs parse cleanly",
            "evidence": "csv.DictReader parse check",
        }
    ),
    base(
        {
            "validation_id": "VAL3078_03_conditional_lemma_recorded",
            "passed": str(any(row["theorem_id"] == "TQZ3078_0_conditional_geometry_lemma" and row["math_conditional_ok"] == "true" for row in theorem_zero_rows)),
            "requirement": "conditional metric/coframe T=Q=0 lemma is recorded",
            "evidence": OUTPUTS["theorem_zero"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3078_04_theorem_zero_not_signed",
            "passed": str(not any(boolish(row["theorem_zero_signed"]) for row in theorem_zero_rows)),
            "requirement": "K_P4_TQ zero theorem is not claimed",
            "evidence": OUTPUTS["theorem_zero"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3078_05_numeric_sources_missing",
            "passed": str(not any(boolish(row["numeric_ready"]) for row in numeric_source_rows)),
            "requirement": "c_T, T_bar, c_Q, Q_bar and projection sources remain missing",
            "evidence": OUTPUTS["numeric_source"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3078_06_bound_schema_nonclaim",
            "passed": str(any(row["quantity"] == "K_P4_TQ" for row in bound_schema_rows) and not has_claim_true(bound_schema_rows)),
            "requirement": "K_P4_TQ bound schema exists but is nonclaim",
            "evidence": OUTPUTS["bound_schema"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3078_07_arena_maps_blocked",
            "passed": str(not any(boolish(row["arena_projection_ready"]) or boolish(row["local_gr_claim"]) for row in arena_map_rows)),
            "requirement": "R10, PPN/orbital and clock/WEP projections remain blocked",
            "evidence": OUTPUTS["arena_map"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3078_08_geometry_gap_unsigned",
            "passed": str(not any(boolish(row["parent_signed"]) or boolish(row["inventory_signed"]) for row in geometry_gap_rows)),
            "requirement": "local geometry field-list gaps remain unsigned",
            "evidence": OUTPUTS["geometry_gap"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3078_09_no_local_claim",
            "passed": str(not has_claim_true(claim_rows + decision_rows + arena_map_rows)),
            "requirement": "no K_P4_TQ zero, local-GR, PPN, R10, clock, WEP or orbital claim is promoted",
            "evidence": OUTPUTS["claim_status"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3078_10_next_target_selected",
            "passed": str(next_rows[0]["next_checkpoint"].startswith("3079-Y5-R2FR-local-geometry-field-list")),
            "requirement": "next target moves to local geometry field-list signature or TQ bound source acquisition",
            "evidence": OUTPUTS["next"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3078_11_branch_copies_exist",
            "passed": str(all(row["copy_exists"] == "True" and row["copy_parse_ok"] == "True" for row in branch_rows)),
            "requirement": "branch copies exist and parse",
            "evidence": OUTPUTS["branches"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3078_12_dotg_unchanged",
            "passed": str(dotg_hash_before == dotg_hash_after),
            "requirement": "P8_time_drift_residual_or_zero.csv is not modified",
            "evidence": f"{dotg_hash_before}->{dotg_hash_after}",
        }
    ),
    base(
        {
            "validation_id": "VAL3078_13_outputs_under_post_checkpoint",
            "passed": str(all(under(output_path, ROOT) for output_path in generated_csvs + [DOC])),
            "requirement": "all outputs are under post-checkpoint-work",
            "evidence": "path containment check",
        }
    ),
    base(
        {
            "validation_id": "VAL3078_14_no_formalization_outputs",
            "passed": str(formalization_output_count == 0),
            "requirement": "formalization-workbench modified-file count for 3078 outputs remains zero",
            "evidence": f"formalization_3078_output_paths={formalization_output_count}",
        }
    ),
    base(
        {
            "validation_id": "VAL3078_15_pycache_absent",
            "passed": str(not PYCACHE.exists()),
            "requirement": "scripts __pycache__ is absent at generator completion",
            "evidence": str(PYCACHE),
        }
    ),
    base(
        {
            "validation_id": "VAL3078_16_doc_written",
            "passed": str(DOC.exists()),
            "requirement": "checkpoint markdown document is written",
            "evidence": str(DOC),
        }
    ),
    base(
        {
            "validation_id": "VAL3078_17_no_claim_fields_true",
            "passed": str(not has_claim_true(generated_rows)),
            "requirement": "no generated non-validation row contains a true claim/ready field",
            "evidence": "claim field scan",
        }
    ),
]

write_csv(OUTPUTS["validation"], validation_rows)

doc_text = f"""# 3078 - P4 TQ First Source or Theorem-Zero

Status: `Y5_R2FR_3078_conditional_TQ_zero_not_parent_signed`

Generated: `{RUN_UTC}`

## Verdict

3078 attacked the broadest P4 connection residue, `K_P4_TQ`, before touching narrower spin/projective/nonmetricity subchannels.

There is a clean conditional theorem: if the local parent branch is metric/coframe-only and `Gamma/omega` is derived as Levi-Civita/spin connection, then torsion and nonmetricity vanish, so `K_P4_TQ=0`.

But this is still **not** a claim. The parent action field list is not signed, the derived-connection declaration is missing, and source/readout connection-current silence is not parent-signed. The numeric fallback also cannot score because `c_T`, `T_bar`, `c_Q`, `Q_bar`, common units, and arena projections are missing.

So 3078 does **not** claim `K_P4_TQ=0`, a numeric `K_P4_TQ` bound, local GR, Newtonian recovery, PPN, R10, clocks, WEP, or orbital success.

The best next move is therefore not to scatter into every coefficient yet. The least-ugly route is to try to sign the local geometry field list that makes the conditional theorem live.

## TQ Theorem-Zero Audit

{md_table(theorem_zero_rows, ["theorem_id", "clause", "current_status", "math_conditional_ok", "theorem_zero_signed", "missing_for_claim"])}

## TQ Numeric Source Audit

{md_table(numeric_source_rows, ["source_id", "quantity", "current_status", "numeric_ready", "missing_for_claim"])}

## TQ Bound Schema

{md_table(bound_schema_rows, ["bound_id", "quantity", "formula", "status", "bound_ready"])}

## Local Arena Map

{md_table(arena_map_rows, ["arena_id", "arena", "current_status", "arena_projection_ready", "missing_for_claim"])}

## Geometry Field-List Gaps

{md_table(geometry_gap_rows, ["gap_id", "required_signature", "current_status", "parent_signed", "why_it_matters"])}

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
- TQ theorem-zero audit: `{OUTPUTS["theorem_zero"]}`
- TQ numeric source audit: `{OUTPUTS["numeric_source"]}`
- TQ bound schema: `{OUTPUTS["bound_schema"]}`
- Local arena map: `{OUTPUTS["arena_map"]}`
- Geometry field-list gaps: `{OUTPUTS["geometry_gap"]}`
- Claim status: `{OUTPUTS["claim_status"]}`
- Next target: `{OUTPUTS["next"]}`
- Validation: `{OUTPUTS["validation"]}`
- Branch copy: `{BRANCH_OUTPUTS["theorem_zero_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["geometry_gap_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["numeric_source_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["bound_schema_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["next_copy"]}`
"""

DOC.write_text(doc_text, encoding="utf-8")
print(f"Wrote {DOC}")
print(f"Wrote {OUTPUTS['validation']}")
print(f"Validation passed {sum(1 for row in validation_rows if row['passed'] == 'True')}/{len(validation_rows)}")

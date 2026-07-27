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
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = PROJECT / "formalization-workbench"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3075"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3075-Y5-R2FR-parent-field-inventory-no-independent-Gamma-or-P4-vector-under-AX1090.md"
DOTG_TARGET = RESIDUALS / "P8_time_drift_residual_or_zero.csv"

SOURCE_PATHS = {
    "SRC3075_00_3074_doc": ROOT / "3074-Y5-R2FR-connection-stack-grammar-or-Kconn-bound-fill-under-AX1090.md",
    "SRC3075_01_3074_next": RESIDUALS / "P8_Y5_R2FR_3074_NEXT_TARGET.csv",
    "SRC3075_02_3074_grammar": RESIDUALS / "P8_Y5_R2FR_3074_CONNECTION_STACK_GRAMMAR_AUDIT.csv",
    "SRC3075_03_3074_zero": RESIDUALS / "P8_Y5_R2FR_3074_KCONN_ZERO_ATTEMPT.csv",
    "SRC3075_04_3074_bound": RESIDUALS / "P8_Y5_R2FR_3074_KCONN_BOUND_VECTOR_NONCLAIM.csv",
    "SRC3075_05_3074_p4": RESIDUALS / "P8_Y5_R2FR_3074_P4_CONNECTION_FALLBACK_VECTOR_NONCLAIM.csv",
    "SRC3075_06_3074_symbol": RESIDUALS / "P8_Y5_R2FR_3074_GAMMA_KHAT_SYMBOL_MATCH_LEDGER.csv",
    "SRC3075_07_1830_no_independent": RAB_QUEUE / "P8_Y5_PARENT_QLOC_1830_NO_INDEPENDENT_CONNECTION_GRAMMAR_ATTEMPT.csv",
    "SRC3075_08_1829_metric_only": RAB_QUEUE / "P8_Y5_PARENT_QLOC_1829_METRIC_ONLY_CONNECTION_THEOREM_ATTEMPT.csv",
    "SRC3075_09_1828_connection": RAB_QUEUE / "P8_Y5_PARENT_QLOC_1828_CONNECTION_COMPATIBILITY_AUDIT.csv",
    "SRC3075_10_1829_p4_pack": RAB_QUEUE / "P8_Y5_PARENT_QLOC_1829_P4_CONNECTION_SOURCE_PACK.csv",
    "SRC3075_11_1814_visible_connection": RAB_QUEUE / "P8_Y5_PARENT_QLOC_1814_VISIBLE_CONNECTION_OWNER_AUDIT.csv",
    "SRC3075_12_1814_current_owner": RAB_QUEUE / "P8_Y5_PARENT_QLOC_1814_VISIBLE_CONNECTION_CURRENT_OWNER_THEOREM.csv",
    "SRC3075_13_2659_operator_domain": RESIDUALS / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv",
    "SRC3075_14_2539_connection_decision": RESIDUALS / "P8_Y5_NO_SHADOW_2539_CONNECTION_GATE_DECISION_LEDGER.csv",
    "SRC3075_15_dotg_target": DOTG_TARGET,
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3075_SOURCE_REGISTER.csv",
    "inventory": RESIDUALS / "P8_Y5_R2FR_3075_PARENT_FIELD_INVENTORY_AUDIT.csv",
    "nogamma": RESIDUALS / "P8_Y5_R2FR_3075_NO_INDEPENDENT_GAMMA_AUDIT.csv",
    "nohyper": RESIDUALS / "P8_Y5_R2FR_3075_NO_HYPERMOMENTUM_AUDIT.csv",
    "p4": RESIDUALS / "P8_Y5_R2FR_3075_P4_CONNECTION_VECTOR_NONCLAIM.csv",
    "gr": RESIDUALS / "P8_Y5_R2FR_3075_GR_REDUCTION_CONSEQUENCE_LEDGER.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3075_DECISION_LEDGER.csv",
    "claim_status": RESIDUALS / "P8_Y5_R2FR_3075_CLAIM_STATUS.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3075_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3075_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3075_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "inventory_copy": PARENT_ACTION / "parent_field_inventory_audit_3075_NOT_SIGNED.csv",
    "nogamma_copy": PARENT_ACTION / "no_independent_Gamma_audit_3075_NOT_SIGNED.csv",
    "nohyper_copy": PARENT_ACTION / "no_hypermomentum_audit_3075_NOT_SIGNED.csv",
    "p4_copy": LOCAL_BOUNDS / "P4_connection_vector_3075_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3075_Gamma_eff_Khat_symbol_match_or_P4_numeric_NEXT_NONCLAIM.csv",
}

for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    path.parent.mkdir(parents=True, exist_ok=True)


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
        "signed",
        "theorem_signed",
        "inventory_signed",
        "nogamma_signed",
        "nohyper_signed",
        "p4_ready",
        "numeric_ready",
        "bound_ready",
        "local_gr_claim",
        "khat_claim",
        "kconn_zero",
    }
    for row in input_rows:
        for field in claim_fields:
            if field in row and boolish(row[field]):
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
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, sep]
    for row in table_rows:
        lines.append("| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def copy_csv(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


dotg_hash_before = file_hash(DOTG_TARGET)

source_register = [
    base(
        {
            "source_id": source_id,
            "source_path": str(path),
            "exists": str(path.exists()),
            "parse_ok": str(source_parse_ok(path)),
            "row_count": row_count(path),
            "role": "parent_field_inventory_no_Gamma_or_P4_vector_evidence" if source_id != "SRC3075_15_dotg_target" else "append_guard_target",
            "status": "PRESENT" if path.exists() else "MISSING_SOURCE",
        }
    )
    for source_id, path in SOURCE_PATHS.items()
]

inventory_rows = [
    base(
        {
            "inventory_id": "PFI3075_0_allowed_geometry",
            "slot": "observed geometry",
            "required_contract": "Parent local geometry contains e_obs/g_obs as the public metric/coframe data; omega/Gamma appears only as omega[e_obs] or Gamma[g_obs].",
            "current_status": "CONTRACT_WRITTEN_NOT_PARENT_SIGNED",
            "inventory_signed": "false",
            "missing_for_claim": "MISSING_PARENT_ACTION_FIELD_LIST;MISSING_E_OBS_OWNER;MISSING_G_OBS_OWNER;MISSING_VARIATION_DOMAIN",
            "source_ids": "SRC3075_07_1830_no_independent;SRC3075_08_1829_metric_only;SRC3075_09_1828_connection",
        }
    ),
    base(
        {
            "inventory_id": "PFI3075_1_matter_domain",
            "slot": "ordinary matter and representation data",
            "required_contract": "Ordinary matter lives on the observed geometry stack with fixed representation data; no hidden/shadow frame or connection argument is admitted.",
            "current_status": "EXACT_TYPED_ROUTE_CONDITIONAL",
            "inventory_signed": "false",
            "missing_for_claim": "MISSING_ALLOWED_SORD_DOMAIN;MISSING_A_FIXED_REPRESENTATION_SECTOR;MISSING_NO_HIDDEN_VISIBLE_HOM_PARENT_PROOF",
            "source_ids": "SRC3075_13_2659_operator_domain;SRC3075_12_1814_current_owner",
        }
    ),
    base(
        {
            "inventory_id": "PFI3075_2_memory_motion_sector",
            "slot": "MTS memory/motion variables",
            "required_contract": "MTS-specific variables may exist, but any local-GR safe branch must either couple through the public geometry stack or appear as explicit residual terms, not as an unlisted connection slot.",
            "current_status": "RESIDUAL_OR_PUBLIC_STACK_SPLIT_REQUIRED",
            "inventory_signed": "false",
            "missing_for_claim": "MISSING_MTS_PARENT_FIELD_LIST;MISSING_PUBLIC_STACK_COUPLING_RULE;MISSING_RESIDUAL_DECLARATION_FOR_GAMMA_EFF",
            "source_ids": "SRC3075_06_3074_symbol;SRC3075_02_3074_grammar",
        }
    ),
    base(
        {
            "inventory_id": "PFI3075_3_forbidden_slot",
            "slot": "independent Gamma/omega",
            "required_contract": "No independent Gamma/omega variable is included in the local parent configuration unless its torsion, nonmetricity, projective and hypermomentum residues are carried by P4.",
            "current_status": "NOT_SIGNED_P4_FALLBACK_REQUIRED",
            "inventory_signed": "false",
            "missing_for_claim": "MISSING_NO_INDEPENDENT_GAMMA_SLOT;MISSING_P4_NUMERIC_OR_THEOREM_ZERO_VECTOR",
            "source_ids": "SRC3075_07_1830_no_independent;SRC3075_10_1829_p4_pack;SRC3075_14_2539_connection_decision",
        }
    ),
    base(
        {
            "inventory_id": "PFI3075_4_verdict",
            "slot": "parent field inventory",
            "required_contract": "All inventory clauses are signed in one parent action before local tests.",
            "current_status": "PARENT_FIELD_INVENTORY_NOT_SIGNED",
            "inventory_signed": "false",
            "missing_for_claim": "MISSING_PARENT_ACTION_FIELD_LIST;MISSING_NO_GAMMA_SLOT;MISSING_NO_HYPERMOMENTUM;MISSING_SYMBOL_MATCH",
            "source_ids": "SRC3075_01_3074_next;SRC3075_02_3074_grammar",
        }
    ),
]

nogamma_rows = [
    base(
        {
            "audit_id": "NIG3075_0_exact_kinematic_lemma",
            "target": "no independent Gamma",
            "statement": "On a metric/coframe-only configuration space, Gamma and omega are constructed from g/e, so torsion and nonmetricity are not independent fields.",
            "result": "EXACT_CONDITIONAL_LEMMA",
            "nogamma_signed": "false",
            "kconn_zero": "false",
            "missing_for_claim": "MISSING_PARENT_FIELD_INVENTORY;MISSING_DERIVED_CONNECTION_DECLARATION",
            "source_ids": "SRC3075_08_1829_metric_only;SRC3075_07_1830_no_independent",
        }
    ),
    base(
        {
            "audit_id": "NIG3075_1_q_visible",
            "target": "q_loc visible geometry ownership",
            "statement": "q_loc must own e_obs, g_obs and omega_obs before tests, not delete failed local couplings after the fact.",
            "result": "CANDIDATE_ONLY",
            "nogamma_signed": "false",
            "kconn_zero": "false",
            "missing_for_claim": "MISSING_QLOC_PARENT_DEFINITION;MISSING_NO_POSTHOC_DELETION_GUARD",
            "source_ids": "SRC3075_07_1830_no_independent;SRC3075_06_3074_symbol",
        }
    ),
    base(
        {
            "audit_id": "NIG3075_2_Palatini_metric_affine_fork",
            "target": "independent connection fork",
            "statement": "If Gamma is independent, Palatini/metric-affine equations must force harmless Levi-Civita/projective form or the P4 vector must be scored.",
            "result": "FORK_RETAINED",
            "nogamma_signed": "false",
            "kconn_zero": "false",
            "missing_for_claim": "MISSING_PALATINI_EH_PARENT;MISSING_ZERO_SOURCE_ALGEBRAIC_CONNECTION_EQUATION;MISSING_PROJECTIVE_SILENCE",
            "source_ids": "SRC3075_09_1828_connection;SRC3075_10_1829_p4_pack",
        }
    ),
    base(
        {
            "audit_id": "NIG3075_3_verdict",
            "target": "no-independent-Gamma theorem",
            "statement": "The no-Gamma theorem is still the best derivation route but is not parent-signed in current evidence.",
            "result": "NO_GAMMA_THEOREM_NOT_CLOSED",
            "nogamma_signed": "false",
            "kconn_zero": "false",
            "missing_for_claim": "MISSING_FIELD_INVENTORY_SIGNATURE;MISSING_GAMMA_EFF_RECONCILIATION;MISSING_NO_HYPERMOMENTUM",
            "source_ids": "SRC3075_07_1830_no_independent;SRC3075_02_3074_grammar",
        }
    ),
]

nohyper_rows = [
    base(
        {
            "audit_id": "NH3075_0_matter_hypermomentum",
            "sector": "ordinary matter",
            "required_zero": "delta S_matter/delta Gamma_independent = 0 beyond omega[e_obs]",
            "current_status": "NOT_PARENT_SIGNED",
            "nohyper_signed": "false",
            "missing_for_claim": "MISSING_MATTER_ACTION_DOMAIN;MISSING_SPIN_TORSION_EXCLUSION;MISSING_CONNECTION_CURRENT_EXCLUSION",
            "source_ids": "SRC3075_07_1830_no_independent;SRC3075_08_1829_metric_only;SRC3075_10_1829_p4_pack",
        }
    ),
    base(
        {
            "audit_id": "NH3075_1_source_readout_hypermomentum",
            "sector": "source/readout",
            "required_zero": "source/readout transfer has no independent Gamma current, source-label connection current, or non-Hilbert connection residue",
            "current_status": "COUNTERMODELS_RETAINED",
            "nohyper_signed": "false",
            "missing_for_claim": "MISSING_SOURCE_CONNECTION_CURRENT_EXCLUSION;MISSING_READOUT_TRANSFER_DOMAIN;MISSING_NO_SOURCE_LABEL_MORPHISM",
            "source_ids": "SRC3075_11_1814_visible_connection;SRC3075_12_1814_current_owner;SRC3075_13_2659_operator_domain",
        }
    ),
    base(
        {
            "audit_id": "NH3075_2_verdict",
            "sector": "all connection-current channels",
            "required_zero": "all hypermomentum and projective current channels vanish in the same branch",
            "current_status": "NO_HYPERMOMENTUM_NOT_SIGNED",
            "nohyper_signed": "false",
            "missing_for_claim": "MISSING_NO_HYPERMOMENTUM_THEOREM;MISSING_PROJECTIVE_INVARIANCE;MISSING_P4_VECTOR_BOUNDS",
            "source_ids": "SRC3075_10_1829_p4_pack;SRC3075_14_2539_connection_decision",
        }
    ),
]

p4_rows = [
    base(
        {
            "p4_id": "P4V3075_0_TQ_combined",
            "component": "torsion_nonmetricity_combined",
            "symbolic_bound": "K_P4_TQ <= c_T T_bar + c_Q Q_bar",
            "observable_links": "WEP;clock;lightcone;operator_ledger",
            "status": "SOURCE_PACK_REQUIRED_NONCLAIM",
            "p4_ready": "false",
            "numeric_ready": "false",
            "bound_ready": "false",
            "missing_for_claim": "MISSING_C_T;MISSING_T_BAR;MISSING_C_Q;MISSING_Q_BAR;MISSING_WEAK_FIELD_MAP",
            "source_ids": "SRC3075_10_1829_p4_pack",
        }
    ),
    base(
        {
            "p4_id": "P4V3075_1_axial_spin",
            "component": "axial_torsion_spin_coupling",
            "symbolic_bound": "K_P4_spin <= c_spin S_axial_bar",
            "observable_links": "clock;spin;operator_ledger",
            "status": "SOURCE_PACK_REQUIRED_NONCLAIM",
            "p4_ready": "false",
            "numeric_ready": "false",
            "bound_ready": "false",
            "missing_for_claim": "MISSING_C_SPIN;MISSING_SPINOR_ASSUMPTIONS;MISSING_S_AXIAL_BAR",
            "source_ids": "SRC3075_10_1829_p4_pack",
        }
    ),
    base(
        {
            "p4_id": "P4V3075_2_projective",
            "component": "torsion_trace_projective_mode",
            "symbolic_bound": "K_P4_proj <= c_proj P_projective_bar",
            "observable_links": "WEP;operator_ledger",
            "status": "SOURCE_PACK_REQUIRED_NONCLAIM",
            "p4_ready": "false",
            "numeric_ready": "false",
            "bound_ready": "false",
            "missing_for_claim": "MISSING_PROJECTIVE_INVARIANCE_OR_C_PROJ;MISSING_P_PROJECTIVE_BAR",
            "source_ids": "SRC3075_10_1829_p4_pack",
        }
    ),
    base(
        {
            "p4_id": "P4V3075_3_weyl_nonmetricity",
            "component": "nonmetricity_weyl_trace",
            "symbolic_bound": "K_P4_QW <= c_QW Q_W_bar",
            "observable_links": "WEP;clock;rod_calibration",
            "status": "SOURCE_PACK_REQUIRED_NONCLAIM",
            "p4_ready": "false",
            "numeric_ready": "false",
            "bound_ready": "false",
            "missing_for_claim": "MISSING_C_QW;MISSING_Q_W_BAR;MISSING_CLOCK_ROD_MAP",
            "source_ids": "SRC3075_10_1829_p4_pack",
        }
    ),
    base(
        {
            "p4_id": "P4V3075_4_shear_nonmetricity",
            "component": "nonmetricity_shear_lightcone",
            "symbolic_bound": "K_P4_QTF <= c_QTF Q_TF_bar",
            "observable_links": "lightcone;clock;WEP",
            "status": "SOURCE_PACK_REQUIRED_NONCLAIM",
            "p4_ready": "false",
            "numeric_ready": "false",
            "bound_ready": "false",
            "missing_for_claim": "MISSING_C_QTF;MISSING_Q_TF_BAR;MISSING_LIGHTCONE_MAP",
            "source_ids": "SRC3075_10_1829_p4_pack",
        }
    ),
    base(
        {
            "p4_id": "P4V3075_5_hypermomentum",
            "component": "independent_connection_hypermomentum",
            "symbolic_bound": "K_P4_H <= c_H H_bar",
            "observable_links": "WEP;clock;spin;lightcone;operator_ledger",
            "status": "MANDATORY_FALLBACK_IF_NO_HYPERMOMENTUM_THEOREM",
            "p4_ready": "false",
            "numeric_ready": "false",
            "bound_ready": "false",
            "missing_for_claim": "MISSING_NO_HYPERMOMENTUM_THEOREM;MISSING_C_H;MISSING_H_BAR",
            "source_ids": "SRC3075_10_1829_p4_pack;SRC3075_14_2539_connection_decision",
        }
    ),
    base(
        {
            "p4_id": "P4V3075_6_total",
            "component": "K_P4_bar",
            "symbolic_bound": "K_P4_bar := K_P4_TQ + K_P4_spin + K_P4_proj + K_P4_QW + K_P4_QTF + K_P4_H",
            "observable_links": "local_GR;PPN;R10;clock;WEP;operator_ledger",
            "status": "P4_VECTOR_SCHEMA_NONCLAIM",
            "p4_ready": "false",
            "numeric_ready": "false",
            "bound_ready": "false",
            "missing_for_claim": "MISSING_ALL_COMPONENT_BOUNDS;MISSING_COMMON_UNITS;MISSING_ARENA_PROJECTIONS",
            "source_ids": "SRC3075_05_3074_p4;SRC3075_10_1829_p4_pack",
        }
    ),
]

gr_rows = [
    base(
        {
            "impact_id": "GR3075_0_metric_GR_route",
            "question": "Did 3075 derive the metric-only local GR connection stack?",
            "answer": "No. It preserved the exact conditional route but found no parent-signed field inventory/no-Gamma/no-hypermomentum certificate.",
            "local_gr_claim": "false",
            "khat_claim": "false",
            "next_requirement": "either sign the parent field inventory from source text or keep scoring P4 components as residuals",
        }
    ),
    base(
        {
            "impact_id": "GR3075_1_useful_gain",
            "question": "What improved?",
            "answer": "The connection obstruction is now binary: either no independent Gamma is a parent grammar theorem, or K_P4_bar is the official fallback vector.",
            "local_gr_claim": "false",
            "khat_claim": "false",
            "next_requirement": "Gamma_eff/Khat symbol match and P4 numeric/theorem-zero inputs",
        }
    ),
    base(
        {
            "impact_id": "GR3075_2_next_best",
            "question": "Where to push next?",
            "answer": "Attack Gamma_eff/Khat symbol matching before P4 numerics, because a good symbol match may collapse part of K_conn into the already-known GR variation.",
            "local_gr_claim": "false",
            "khat_claim": "false",
            "next_requirement": "Gamma_eff owner and Khat action-match audit",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3075_0_result",
            "decision": "parent field inventory not signed",
            "reason": "sources contain conditional contracts and exact lemmas, not a live parent field list excluding independent Gamma",
            "consequence": "no K_conn zero or local-GR claim",
            "next_action": "Gamma_eff/Khat symbol match or P4 component sourcing",
        }
    ),
    base(
        {
            "decision_id": "DEC3075_1_p4",
            "decision": "P4 connection vector promoted to official nonclaim fallback",
            "reason": "without no-independent-Gamma and no-hypermomentum, torsion/nonmetricity/projective/hypermomentum channels remain legal",
            "consequence": "future local tests can demand these coefficients or theorem-zero rows",
            "next_action": "do not hide independent-connection residues inside K_conn",
        }
    ),
    base(
        {
            "decision_id": "DEC3075_2_next",
            "decision": "3076 Gamma_eff/Khat symbol match",
            "reason": "symbol matching is closer to derivation than immediately hunting six P4 numeric coefficients",
            "consequence": "P4 remains fallback while the GR-like action-response map is tested",
            "next_action": "3076-Y5-R2FR-Gamma-eff-Khat-symbol-match-or-P4-numeric-vector-under-AX1090.md",
        }
    ),
]

claim_rows = [
    base(
        {
            "claim_id": "CLAIM3075_0_field_inventory",
            "claim": "parent field inventory excludes independent Gamma",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "current evidence is a conditional contract, not a signed parent field list",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3075_1_no_hypermomentum",
            "claim": "matter/source/readout hypermomentum vanishes",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "spin, projective, source and readout connection-current counterbranches remain legal",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3075_2_local_gr",
            "claim": "local GR/Newton/PPN/R10 pass",
            "claim_active": "false",
            "status": "BLOCKED",
            "reason": "K_conn/P4, Gamma_eff/Khat, K_domain, K_boundary, units and observable projections remain open",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3075_0_3076",
            "next_checkpoint": "3076-Y5-R2FR-Gamma-eff-Khat-symbol-match-or-P4-numeric-vector-under-AX1090.md",
            "script": "scripts/Y5_R2FR_Gamma_eff_Khat_symbol_match_or_P4_numeric_vector_under_AX1090_3076.py",
            "mission": "try to match Gamma_eff and Khat to the same parent action/metric-response object; if not, start filling P4 numeric/theorem-zero component rows",
            "starting_equation": "K_conn_bar <= K_LC_stack_bar + K_P4_bar, K_P4_bar=sum(TQ,spin,projective,QW,QTF,H)",
            "claim_policy": "no K_conn zero, Khat, q_loc or local-GR claim unless Gamma_eff/Khat symbol match and P4/theorem-zero gates close",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["inventory"], inventory_rows)
write_csv(OUTPUTS["nogamma"], nogamma_rows)
write_csv(OUTPUTS["nohyper"], nohyper_rows)
write_csv(OUTPUTS["p4"], p4_rows)
write_csv(OUTPUTS["gr"], gr_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["claim_status"], claim_rows)
write_csv(OUTPUTS["next"], next_rows)

copy_csv(OUTPUTS["inventory"], BRANCH_OUTPUTS["inventory_copy"])
copy_csv(OUTPUTS["nogamma"], BRANCH_OUTPUTS["nogamma_copy"])
copy_csv(OUTPUTS["nohyper"], BRANCH_OUTPUTS["nohyper_copy"])
copy_csv(OUTPUTS["p4"], BRANCH_OUTPUTS["p4_copy"])
copy_csv(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

branch_rows = [
    base(
        {
            "copy_id": copy_id,
            "source_path": str(src),
            "copy_path": str(dst),
            "copy_exists": str(dst.exists()),
            "copy_parse_ok": str(csv_ok(dst)),
            "status": "COPIED_NONCLAIM",
        }
    )
    for copy_id, src, dst in [
        ("BC3075_0_inventory", OUTPUTS["inventory"], BRANCH_OUTPUTS["inventory_copy"]),
        ("BC3075_1_nogamma", OUTPUTS["nogamma"], BRANCH_OUTPUTS["nogamma_copy"]),
        ("BC3075_2_nohyper", OUTPUTS["nohyper"], BRANCH_OUTPUTS["nohyper_copy"]),
        ("BC3075_3_p4", OUTPUTS["p4"], BRANCH_OUTPUTS["p4_copy"]),
        ("BC3075_4_next", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
]
write_csv(OUTPUTS["branches"], branch_rows)
write_csv(
    OUTPUTS["validation"],
    [
        base(
            {
                "validation_id": "VAL3075_PRE",
                "passed": "False",
                "requirement": "placeholder overwritten by final validation",
                "evidence": "generator ordering guard",
            }
        )
    ],
)
DOC.write_text("# 3075 draft\n", encoding="utf-8")

dotg_hash_after = file_hash(DOTG_TARGET)
generated_csvs = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values())
formalization_3075 = list(FORMALIZATION.rglob("*3075*")) if FORMALIZATION.exists() else []

validation_rows = [
    base(
        {
            "validation_id": "VAL3075_00_sources_exist",
            "passed": str(all(row["exists"] == "True" for row in source_register)),
            "requirement": "all cited source paths exist",
            "evidence": OUTPUTS["sources"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3075_01_sources_parse",
            "passed": str(all(row["parse_ok"] == "True" for row in source_register)),
            "requirement": "all cited CSV sources parse and markdown sources exist",
            "evidence": OUTPUTS["sources"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3075_02_csv_parse",
            "passed": str(all(csv_ok(path) for path in generated_csvs)),
            "requirement": "all generated and branch-copy CSVs parse cleanly",
            "evidence": "csv.DictReader parse check",
        }
    ),
    base(
        {
            "validation_id": "VAL3075_03_inventory_not_signed",
            "passed": str(not any(boolish(row["inventory_signed"]) for row in inventory_rows)),
            "requirement": "parent field inventory remains unsigned",
            "evidence": OUTPUTS["inventory"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3075_04_noGamma_not_signed",
            "passed": str(not any(boolish(row["nogamma_signed"]) or boolish(row["kconn_zero"]) for row in nogamma_rows)),
            "requirement": "no-independent-Gamma theorem remains unclaimed",
            "evidence": OUTPUTS["nogamma"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3075_05_nohypermomentum_not_signed",
            "passed": str(not any(boolish(row["nohyper_signed"]) for row in nohyper_rows)),
            "requirement": "no-hypermomentum theorem remains unclaimed",
            "evidence": OUTPUTS["nohyper"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3075_06_P4_vector_nonclaim",
            "passed": str(not has_claim_true(p4_rows) and any(row["component"] == "K_P4_bar" for row in p4_rows)),
            "requirement": "P4 connection vector is explicit, totalled, and nonclaim",
            "evidence": OUTPUTS["p4"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3075_07_no_local_gr_claim",
            "passed": str(not has_claim_true(claim_rows + gr_rows)),
            "requirement": "no Khat, q_loc, local-GR, PPN, R10, clock or orbital claim is promoted",
            "evidence": OUTPUTS["claim_status"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3075_08_next_target_selected",
            "passed": str(next_rows[0]["next_checkpoint"].startswith("3076-Y5-R2FR-Gamma-eff-Khat")),
            "requirement": "next target moves to Gamma_eff/Khat symbol match or P4 numeric vector",
            "evidence": OUTPUTS["next"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3075_09_branch_copies_exist",
            "passed": str(all(row["copy_exists"] == "True" and row["copy_parse_ok"] == "True" for row in branch_rows)),
            "requirement": "branch copies exist and parse",
            "evidence": OUTPUTS["branches"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3075_10_dotg_unchanged",
            "passed": str(dotg_hash_before == dotg_hash_after),
            "requirement": "P8_time_drift_residual_or_zero.csv is not modified",
            "evidence": f"{dotg_hash_before}->{dotg_hash_after}",
        }
    ),
    base(
        {
            "validation_id": "VAL3075_11_outputs_under_post_checkpoint",
            "passed": str(all(under(path, ROOT) for path in generated_csvs + [DOC])),
            "requirement": "all outputs are under post-checkpoint-work",
            "evidence": "path containment check",
        }
    ),
    base(
        {
            "validation_id": "VAL3075_12_no_formalization_workbench_outputs",
            "passed": str(not formalization_3075 and all(not under(path, FORMALIZATION) for path in generated_csvs + [DOC])),
            "requirement": "formalization-workbench modified-file count for 3075 outputs remains zero",
            "evidence": f"formalization_3075_matches={len(formalization_3075)}",
        }
    ),
    base(
        {
            "validation_id": "VAL3075_13_pycache_absent",
            "passed": str(not PYCACHE.exists()),
            "requirement": "scripts __pycache__ is absent at generator completion",
            "evidence": str(PYCACHE),
        }
    ),
    base(
        {
            "validation_id": "VAL3075_14_doc_written",
            "passed": str(DOC.exists()),
            "requirement": "checkpoint markdown document is written",
            "evidence": str(DOC),
        }
    ),
    base(
        {
            "validation_id": "VAL3075_15_P4_components_complete",
            "passed": str({"torsion_nonmetricity_combined", "axial_torsion_spin_coupling", "torsion_trace_projective_mode", "nonmetricity_weyl_trace", "nonmetricity_shear_lightcone", "independent_connection_hypermomentum", "K_P4_bar"}.issubset({row["component"] for row in p4_rows})),
            "requirement": "P4 component set is complete",
            "evidence": OUTPUTS["p4"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3075_16_exact_lemma_retained",
            "passed": str(any(row["result"] == "EXACT_CONDITIONAL_LEMMA" for row in nogamma_rows)),
            "requirement": "exact no-independent-Gamma conditional lemma is retained",
            "evidence": OUTPUTS["nogamma"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3075_17_inventory_forbidden_slot_recorded",
            "passed": str(any(row["slot"] == "independent Gamma/omega" for row in inventory_rows)),
            "requirement": "independent Gamma forbidden/fallback slot is explicit",
            "evidence": OUTPUTS["inventory"].name,
        }
    ),
]

doc_text = f"""# 3075 - Parent Field Inventory, No Independent Gamma, or P4 Vector

Status: `Y5_R2FR_3075_parent_inventory_not_signed_P4_vector_written`

Generated: `{RUN_UTC}`

## Verdict

3075 tried the direct GR-native move: sign a parent field inventory in which the local geometry is metric/coframe-only and `Gamma/omega` is derived as `Gamma[g_obs]` or `omega[e_obs]`, not an independent field.

The useful theorem is exact as a conditional: on a metric/coframe-only configuration space, compatibility is kinematic and torsion/nonmetricity are not independent fields. But the current source set still does not parent-sign the field inventory, no-independent-`Gamma` slot, no-hypermomentum condition, source/readout connection-current exclusion, or `Gamma_eff/Khat/q_loc` symbol match.

So 3075 does **not** claim `K_conn=0`, `Khat`, `q_loc=0`, local GR, PPN, R10, clocks, WEP, or orbital success.

The gain is that the fork is now explicit:

- derivation lane: prove the parent field inventory/no-independent-`Gamma`/no-hypermomentum grammar;
- fallback lane: use `K_P4_bar := K_P4_TQ + K_P4_spin + K_P4_proj + K_P4_QW + K_P4_QTF + K_P4_H`.

## Parent Field Inventory Audit

{md_table(inventory_rows, ["inventory_id", "slot", "current_status", "inventory_signed", "missing_for_claim"])}

## No-Independent-Gamma Audit

{md_table(nogamma_rows, ["audit_id", "target", "result", "nogamma_signed", "missing_for_claim"])}

## No-Hypermomentum Audit

{md_table(nohyper_rows, ["audit_id", "sector", "current_status", "nohyper_signed", "missing_for_claim"])}

## P4 Connection Vector

{md_table(p4_rows, ["p4_id", "component", "status", "symbolic_bound", "missing_for_claim"])}

## GR Reduction Consequence

{md_table(gr_rows, ["impact_id", "answer", "next_requirement"])}

## Decision

{md_table(decision_rows, ["decision_id", "decision", "reason", "next_action"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}

## Files

- Source register: `{OUTPUTS["sources"]}`
- Parent field inventory audit: `{OUTPUTS["inventory"]}`
- No-independent-Gamma audit: `{OUTPUTS["nogamma"]}`
- No-hypermomentum audit: `{OUTPUTS["nohyper"]}`
- P4 connection vector: `{OUTPUTS["p4"]}`
- GR consequence ledger: `{OUTPUTS["gr"]}`
- Claim status: `{OUTPUTS["claim_status"]}`
- Next target: `{OUTPUTS["next"]}`
- Validation: `{OUTPUTS["validation"]}`
"""

write_csv(OUTPUTS["validation"], validation_rows)
DOC.write_text(doc_text, encoding="utf-8")
write_csv(OUTPUTS["validation"], validation_rows)

if PYCACHE.exists():
    shutil.rmtree(PYCACHE)

failed = [row for row in validation_rows if row["passed"] != "True"]
print(f"wrote {DOC}")
print(f"validation passed {len(validation_rows) - len(failed)}/{len(validation_rows)}")
if failed:
    for row in failed:
        print(f"FAILED {row['validation_id']}: {row['requirement']} :: {row['evidence']}")
    raise SystemExit(1)

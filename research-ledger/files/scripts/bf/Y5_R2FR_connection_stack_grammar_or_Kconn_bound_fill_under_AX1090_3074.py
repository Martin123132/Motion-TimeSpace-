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

CHECKPOINT = "3074"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3074-Y5-R2FR-connection-stack-grammar-or-Kconn-bound-fill-under-AX1090.md"
DOTG_TARGET = RESIDUALS / "P8_time_drift_residual_or_zero.csv"

SOURCE_PATHS = {
    "SRC3074_00_3073_doc": ROOT / "3073-Y5-R2FR-hidden-kernel-silence-or-bound-vector-fill-under-AX1090.md",
    "SRC3074_01_3073_next": RESIDUALS / "P8_Y5_R2FR_3073_NEXT_TARGET.csv",
    "SRC3074_02_3073_zero": RESIDUALS / "P8_Y5_R2FR_3073_HIDDEN_KERNEL_ZERO_AUDIT.csv",
    "SRC3074_03_3073_bound": RESIDUALS / "P8_Y5_R2FR_3073_HIDDEN_KERNEL_BOUND_VECTOR_NONCLAIM.csv",
    "SRC3074_04_3073_microlemma": RESIDUALS / "P8_Y5_R2FR_3073_SCALAR_DERIVATIVE_CONNECTION_MICROLEMMA.csv",
    "SRC3074_05_3073_lgr": RESIDUALS / "P8_Y5_R2FR_3073_LOCAL_GR_CONSEQUENCE_LEDGER.csv",
    "SRC3074_06_3070_kernel_audit": RESIDUALS / "P8_Y5_R2FR_3070_KMETRIC_KERNEL_NORM_AUDIT.csv",
    "SRC3074_07_776_kgamma": RESIDUALS / "P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
    "SRC3074_08_1289_derivative": RESIDUALS / "P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
    "SRC3074_09_1828_connection_audit": RAB_QUEUE / "P8_Y5_PARENT_QLOC_1828_CONNECTION_COMPATIBILITY_AUDIT.csv",
    "SRC3074_10_1829_metric_only": RAB_QUEUE / "P8_Y5_PARENT_QLOC_1829_METRIC_ONLY_CONNECTION_THEOREM_ATTEMPT.csv",
    "SRC3074_11_1829_p4_pack": RAB_QUEUE / "P8_Y5_PARENT_QLOC_1829_P4_CONNECTION_SOURCE_PACK.csv",
    "SRC3074_12_1830_no_independent_connection": RAB_QUEUE / "P8_Y5_PARENT_QLOC_1830_NO_INDEPENDENT_CONNECTION_GRAMMAR_ATTEMPT.csv",
    "SRC3074_13_1814_visible_connection": RAB_QUEUE / "P8_Y5_PARENT_QLOC_1814_VISIBLE_CONNECTION_OWNER_AUDIT.csv",
    "SRC3074_14_1814_current_owner": RAB_QUEUE / "P8_Y5_PARENT_QLOC_1814_VISIBLE_CONNECTION_CURRENT_OWNER_THEOREM.csv",
    "SRC3074_15_2539_connection_decision": RESIDUALS / "P8_Y5_NO_SHADOW_2539_CONNECTION_GATE_DECISION_LEDGER.csv",
    "SRC3074_16_dotg_target": DOTG_TARGET,
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3074_SOURCE_REGISTER.csv",
    "grammar": RESIDUALS / "P8_Y5_R2FR_3074_CONNECTION_STACK_GRAMMAR_AUDIT.csv",
    "zero": RESIDUALS / "P8_Y5_R2FR_3074_KCONN_ZERO_ATTEMPT.csv",
    "bound": RESIDUALS / "P8_Y5_R2FR_3074_KCONN_BOUND_VECTOR_NONCLAIM.csv",
    "p4": RESIDUALS / "P8_Y5_R2FR_3074_P4_CONNECTION_FALLBACK_VECTOR_NONCLAIM.csv",
    "symbol_match": RESIDUALS / "P8_Y5_R2FR_3074_GAMMA_KHAT_SYMBOL_MATCH_LEDGER.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3074_DECISION_LEDGER.csv",
    "claim_status": RESIDUALS / "P8_Y5_R2FR_3074_CLAIM_STATUS.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3074_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3074_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3074_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "grammar_copy": PARENT_ACTION / "connection_stack_grammar_audit_3074_NOT_SIGNED.csv",
    "zero_copy": PARENT_ACTION / "Kconn_zero_attempt_3074_NOT_SIGNED.csv",
    "bound_copy": LOCAL_BOUNDS / "Kconn_bound_vector_3074_NONCLAIM.csv",
    "p4_copy": RAB_QUEUE / "JR3074_P4_connection_fallback_vector_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3074_parent_field_inventory_no_independent_Gamma_NEXT_NONCLAIM.csv",
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
        "zero_proved",
        "theorem_signed",
        "grammar_signed",
        "bound_ready",
        "numeric_ready",
        "local_gr_claim",
        "khat_claim",
        "p4_ready",
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
            "role": "connection_stack_grammar_or_Kconn_bound_evidence" if source_id != "SRC3074_16_dotg_target" else "append_guard_target",
            "status": "PRESENT" if path.exists() else "MISSING_SOURCE",
        }
    )
    for source_id, path in SOURCE_PATHS.items()
]

grammar_rows = [
    base(
        {
            "grammar_id": "CSG3074_0_field_inventory",
            "clause": "parent field inventory",
            "required_statement": "The local parent configuration contains observed metric/coframe data e_obs,g_obs and ordinary matter fields, while omega/Gamma is a derived omega[e_obs] object rather than an independent field.",
            "current_result": "EXACT_GR_NATIVE_PREMISE_NOT_PARENT_SIGNED",
            "grammar_signed": "false",
            "missing_for_claim": "MISSING_PARENT_FIELD_INVENTORY;MISSING_NO_INDEPENDENT_GAMMA_SLOT;MISSING_E_OBS_OWNER",
            "source_ids": "SRC3074_09_1828_connection_audit;SRC3074_10_1829_metric_only;SRC3074_12_1830_no_independent_connection",
        }
    ),
    base(
        {
            "grammar_id": "CSG3074_1_omega_definition",
            "clause": "Levi-Civita/spin connection definition",
            "required_statement": "omega_obs := omega[e_obs] and Gamma_obs := Gamma[g_obs] before local tests; torsion/nonmetricity are not independent dynamical data.",
            "current_result": "KINEMATIC_LEMMA_CONDITIONAL_ONLY",
            "grammar_signed": "false",
            "missing_for_claim": "MISSING_DERIVED_CONNECTION_DECLARATION;MISSING_TORSION_NONMETRICITY_EXCLUSION;MISSING_VARIATION_ORDER",
            "source_ids": "SRC3074_10_1829_metric_only;SRC3074_12_1830_no_independent_connection",
        }
    ),
    base(
        {
            "grammar_id": "CSG3074_2_no_hypermomentum",
            "clause": "matter/source/readout connection independence",
            "required_statement": "S_matter and source/readout sectors have no independent delta-Gamma hypermomentum beyond omega[e_obs].",
            "current_result": "NOT_PARENT_SIGNED_COUNTERMODELS_RETAINED",
            "grammar_signed": "false",
            "missing_for_claim": "MISSING_MATTER_NO_HYPERMOMENTUM;MISSING_SPIN_TORSION_EXCLUSION;MISSING_SOURCE_CONNECTION_CURRENT_EXCLUSION",
            "source_ids": "SRC3074_09_1828_connection_audit;SRC3074_11_1829_p4_pack;SRC3074_15_2539_connection_decision",
        }
    ),
    base(
        {
            "grammar_id": "CSG3074_3_no_shadow_connection",
            "clause": "single geometry stack",
            "required_statement": "measure, coframe, connection, derivative, Hodge/domain operators and readouts descend through one observed q/e functor with no hidden/shadow connection slot.",
            "current_result": "CONDITIONAL_ONLY",
            "grammar_signed": "false",
            "missing_for_claim": "MISSING_SINGLE_GEOMETRY_STACK;MISSING_NO_SHADOW_CONNECTION;MISSING_OPERATOR_DOMAIN_THEOREM",
            "source_ids": "SRC3074_12_1830_no_independent_connection;SRC3074_13_1814_visible_connection;SRC3074_14_1814_current_owner",
        }
    ),
    base(
        {
            "grammar_id": "CSG3074_4_Gamma_eff_reconciliation",
            "clause": "Gamma_eff/Khat/q_loc symbol match",
            "required_statement": "Gamma_eff must reduce to metric/coframe-derived geometry or remain explicitly in the residual vector; Khat must match the same action/variation convention.",
            "current_result": "RETAINED_SYMBOLIC_GAP",
            "grammar_signed": "false",
            "missing_for_claim": "MISSING_GAMMA_EFF_GEOMETRY_MAP;MISSING_KHAT_ACTION_MATCH;MISSING_HELMHOLTZ_ACTION_EXISTENCE_CHECK",
            "source_ids": "SRC3074_07_776_kgamma;SRC3074_08_1289_derivative;SRC3074_09_1828_connection_audit",
        }
    ),
    base(
        {
            "grammar_id": "CSG3074_5_verdict",
            "clause": "connection stack grammar",
            "required_statement": "All prior clauses close in one same-branch parent action before local tests.",
            "current_result": "CONNECTION_STACK_GRAMMAR_NOT_SIGNED",
            "grammar_signed": "false",
            "missing_for_claim": "MISSING_PARENT_FIELD_INVENTORY;MISSING_NO_INDEPENDENT_CONNECTION;MISSING_NO_HYPERMOMENTUM;MISSING_SYMBOL_MATCH",
            "source_ids": "SRC3074_01_3073_next;SRC3074_09_1828_connection_audit;SRC3074_12_1830_no_independent_connection",
        }
    ),
]

zero_rows = [
    base(
        {
            "zero_id": "KCZ3074_0_lower_scalar_microzero",
            "target": "nabla_mu Gamma_eff",
            "statement": "For lower-index scalar derivative, nabla_mu Gamma_eff=partial_mu Gamma_eff.",
            "result": "TRUE_NARROW_MICROLEMMA",
            "zero_proved": "false",
            "theorem_signed": "false",
            "why_not_enough": "K_conn is a Hilbert/operator-stack metric-response term, including raised/projected indices and derivative/Hodge/domain operator responses.",
            "missing_for_claim": "MISSING_RAISED_INDEX_RESPONSE;MISSING_OPERATOR_STACK_REDUCTION;MISSING_HODGE_DOMAIN_RESPONSE",
            "source_ids": "SRC3074_04_3073_microlemma;SRC3074_07_776_kgamma",
        }
    ),
    base(
        {
            "zero_id": "KCZ3074_1_metric_only_zero",
            "target": "K_conn=0",
            "statement": "If all derivative/connection structures are purely metric/coframe-derived and their Hilbert response is already included in GR-side variation, no extra MTS K_conn residual remains.",
            "result": "EXACT_CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "zero_proved": "false",
            "theorem_signed": "false",
            "why_not_enough": "Requires parent field inventory, no independent Gamma, no hypermomentum, and Gamma_eff/Khat action matching.",
            "missing_for_claim": "MISSING_FIELD_INVENTORY;MISSING_NO_GAMMA_SLOT;MISSING_NO_HYPERMOMENTUM;MISSING_GAMMA_KHAT_MATCH",
            "source_ids": "SRC3074_09_1828_connection_audit;SRC3074_10_1829_metric_only;SRC3074_12_1830_no_independent_connection",
        }
    ),
    base(
        {
            "zero_id": "KCZ3074_2_Palatini_escape",
            "target": "independent connection residue",
            "statement": "Palatini/EH plus matter independent of Gamma could force Levi-Civita up to harmless projective freedom.",
            "result": "BLOCKED_BY_OPEN_EH_AND_MATTER_PREMISES",
            "zero_proved": "false",
            "theorem_signed": "false",
            "why_not_enough": "EH-only parent and matter/source/readout independence from Gamma are not derived; projective/torsion/nonmetricity rows remain legal.",
            "missing_for_claim": "MISSING_EH_PARENT;MISSING_MATTER_GAMMA_INDEPENDENCE;MISSING_PROJECTIVE_SILENCE",
            "source_ids": "SRC3074_09_1828_connection_audit;SRC3074_11_1829_p4_pack",
        }
    ),
    base(
        {
            "zero_id": "KCZ3074_3_verdict",
            "target": "K_conn local-GR contribution",
            "statement": "K_conn zero is the cleanest local-GR route but is not closed in the current corpus.",
            "result": "ZERO_NOT_CLAIMED_KCONN_BOUND_REQUIRED",
            "zero_proved": "false",
            "theorem_signed": "false",
            "why_not_enough": "The exact conditional lemma lacks parent-signed premises.",
            "missing_for_claim": "MISSING_CONNECTION_STACK_GRAMMAR;MISSING_KCONN_NUMERIC_BOUND;MISSING_ARENA_PROJECTION",
            "source_ids": "SRC3074_02_3073_zero;SRC3074_03_3073_bound;SRC3074_15_2539_connection_decision",
        }
    ),
]

bound_rows = [
    base(
        {
            "row_id": "KCB3074_0_metric_variation_template",
            "quantity": "delta Gamma_LC",
            "bound_formula": "||delta Gamma_LC||_D <= C_LC (||nabla h||_D + ||h||_D ||Gamma_LC||_D)",
            "status": "STANDARD_TEMPLATE_NONCLAIM",
            "numeric_ready": "false",
            "bound_ready": "false",
            "missing_for_claim": "MISSING_C_LC;MISSING_H_NORM;MISSING_NABLA_H_NORM;MISSING_DOMAIN_D;MISSING_WEAK_FIELD_GAUGE",
            "source_ids": "SRC3074_04_3073_microlemma;SRC3074_10_1829_metric_only",
        }
    ),
    base(
        {
            "row_id": "KCB3074_1_operator_stack",
            "quantity": "K_conn_bar",
            "bound_formula": "K_conn_bar <= C_conn(||delta Gamma_LC|| O1_bar + ||delta G_AB|| O2_bar + ||delta star|| O3_bar + ||delta D|| O4_bar)",
            "status": "SYMBOLIC_BOUND_NONCLAIM",
            "numeric_ready": "false",
            "bound_ready": "false",
            "missing_for_claim": "MISSING_C_CONN;MISSING_O1_BAR;MISSING_O2_BAR;MISSING_O3_BAR;MISSING_O4_BAR;MISSING_GAB_RESPONSE;MISSING_STAR_RESPONSE",
            "source_ids": "SRC3074_03_3073_bound;SRC3074_07_776_kgamma",
        }
    ),
    base(
        {
            "row_id": "KCB3074_2_P4_fallback",
            "quantity": "K_conn_P4_residual",
            "bound_formula": "K_conn_bar <= K_LC_stack_bar + K_P4_bar, with K_P4_bar collecting torsion, nonmetricity, projective and hypermomentum residues",
            "status": "P4_FALLBACK_REQUIRED_NONCLAIM",
            "numeric_ready": "false",
            "bound_ready": "false",
            "missing_for_claim": "MISSING_TORSION_COEFFICIENTS;MISSING_NONMETRICITY_COEFFICIENTS;MISSING_PROJECTIVE_BOUND;MISSING_HYPERMOMENTUM_BOUND",
            "source_ids": "SRC3074_11_1829_p4_pack;SRC3074_15_2539_connection_decision",
        }
    ),
    base(
        {
            "row_id": "KCB3074_3_E_SGamma_with_Kconn",
            "quantity": "E_SGamma_DZ_Kconn",
            "bound_formula": "E_SGamma_DZ <= (2/3)(L_min^-2 F2_bar Delta_m M_m_bar + L_min^-3 F2_bar Delta_m^2 M_L_bar + K_conn_bar + K_domain_bar + K_boundary_bar)",
            "status": "LOCAL_RESIDUAL_ENVELOPE_RETAINED_NONCLAIM",
            "numeric_ready": "false",
            "bound_ready": "false",
            "missing_for_claim": "MISSING_PARENT_DOUBLE_ZERO;MISSING_DELTA_m_AMPLITUDE;MISSING_KCONN_BAR;MISSING_KDOMAIN_BAR;MISSING_KBOUNDARY_BAR;MISSING_UNITS",
            "source_ids": "SRC3074_01_3073_next;SRC3074_03_3073_bound",
        }
    ),
]

p4_rows = [
    base(
        {
            "p4_id": "P4C3074_0_torsion_nonmetricity",
            "operator_family": "torsion_nonmetricity_combined",
            "required_input": "c_T, c_Q, units, normalization, weak-field map",
            "status": "RETAINED_NONCLAIM",
            "p4_ready": "false",
            "missing_for_claim": "MISSING_C_T;MISSING_C_Q;MISSING_WEAK_FIELD_MAP",
            "source_ids": "SRC3074_11_1829_p4_pack",
        }
    ),
    base(
        {
            "p4_id": "P4C3074_1_spin_projective",
            "operator_family": "axial_spin_and_projective_trace",
            "required_input": "spin-torsion coefficient, spinor assumptions, projective proof or coefficient",
            "status": "RETAINED_NONCLAIM",
            "p4_ready": "false",
            "missing_for_claim": "MISSING_SPIN_TORSION_COEFFICIENT;MISSING_SPINOR_MATTER_ASSUMPTION;MISSING_PROJECTIVE_INVARIANCE",
            "source_ids": "SRC3074_11_1829_p4_pack",
        }
    ),
    base(
        {
            "p4_id": "P4C3074_2_nonmetricity",
            "operator_family": "weyl_and_shear_nonmetricity",
            "required_input": "Q_mu coefficient, trace-free Q coefficient, clock/rod/lightcone maps",
            "status": "RETAINED_NONCLAIM",
            "p4_ready": "false",
            "missing_for_claim": "MISSING_Q_TRACE_COEFFICIENT;MISSING_Q_TF_COEFFICIENT;MISSING_CLOCK_LIGHTCONE_MAP",
            "source_ids": "SRC3074_11_1829_p4_pack",
        }
    ),
    base(
        {
            "p4_id": "P4C3074_3_hypermomentum",
            "operator_family": "independent_connection_hypermomentum",
            "required_input": "matter/source/readout Gamma-dependence theorem or finite hypermomentum residual coefficient",
            "status": "MANDATORY_FALLBACK_IF_NO_GRAMMAR",
            "p4_ready": "false",
            "missing_for_claim": "MISSING_NO_HYPERMOMENTUM_THEOREM;MISSING_HYPERMOMENTUM_BOUND",
            "source_ids": "SRC3074_11_1829_p4_pack;SRC3074_15_2539_connection_decision",
        }
    ),
]

symbol_rows = [
    base(
        {
            "symbol_id": "SYM3074_0_Gamma_eff",
            "object": "Gamma_eff",
            "required_match": "metric/coframe-derived source, parent memory scalar, or explicit residual sector",
            "current_status": "NOT_MATCHED_TO_GR_GEOMETRY",
            "consequence": "cannot identify K_conn with ordinary GR variation alone",
            "missing_for_claim": "MISSING_GAMMA_EFF_OWNER;MISSING_GEOMETRY_MAP_OR_RESIDUAL_DECLARATION",
            "source_ids": "SRC3074_07_776_kgamma;SRC3074_08_1289_derivative",
        }
    ),
    base(
        {
            "symbol_id": "SYM3074_1_Khat",
            "object": "K_hat",
            "required_match": "Hilbert metric response of the same parent action term as Gamma_eff",
            "current_status": "ACTION_MATCH_UNSIGNED",
            "consequence": "Khat adoption/local-GR remains blocked",
            "missing_for_claim": "MISSING_ACTION_EXISTENCE;MISSING_HELMHOLTZ_CHECK;MISSING_TENSOR_SLOT_COMPARISON",
            "source_ids": "SRC3074_07_776_kgamma;SRC3074_06_3070_kernel_audit",
        }
    ),
    base(
        {
            "symbol_id": "SYM3074_2_q_loc",
            "object": "q_loc",
            "required_match": "projected local residual must use same geometry stack and observable readout",
            "current_status": "LOCAL_PROJECTION_UNSIGNED",
            "consequence": "even K_conn progress would not by itself prove PPN/R10/clock/orbital success",
            "missing_for_claim": "MISSING_OBSERVABLE_PROJECTION;MISSING_UNITS;MISSING_ARENA_BASELINES",
            "source_ids": "SRC3074_05_3073_lgr;SRC3074_08_1289_derivative",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3074_0_proof_result",
            "decision": "connection stack grammar not signed",
            "reason": "the metric-only lemma is exact, but field inventory, no independent Gamma, no hypermomentum and Gamma/Khat symbol match are not jointly parent-derived",
            "consequence": "K_conn cannot be set to zero",
            "next_action": "target parent field inventory/no-independent-Gamma slot directly",
        }
    ),
    base(
        {
            "decision_id": "DEC3074_1_bound_result",
            "decision": "K_conn_bar bound row written",
            "reason": "operator-stack metric response must be bounded if zero theorem is unavailable",
            "consequence": "K_conn joins the local residual envelope as an explicit nonclaim coefficient",
            "next_action": "source C_conn, operator norms, or derive grammar zero",
        }
    ),
    base(
        {
            "decision_id": "DEC3074_2_next_target",
            "decision": "3075 parent field inventory/no-independent Gamma",
            "reason": "this is less ad hoc than filling torsion/nonmetricity coefficients first and is closest to GR reduction",
            "consequence": "P4 connection vector remains fallback only",
            "next_action": "3075-Y5-R2FR-parent-field-inventory-no-independent-Gamma-or-P4-vector-under-AX1090.md",
        }
    ),
]

claim_rows = [
    base(
        {
            "claim_id": "CLAIM3074_0_Kconn_zero",
            "claim": "K_conn=0",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "connection stack grammar is not parent-signed",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3074_1_metric_only_GR",
            "claim": "local metric-only GR/Newton branch",
            "claim_active": "false",
            "status": "BLOCKED",
            "reason": "field inventory, hypermomentum exclusion, symbol matching, domain/boundary kernels and observable projection remain open",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3074_2_Kconn_bound",
            "claim": "K_conn finite bound is score-ready",
            "claim_active": "false",
            "status": "SYMBOLIC_NONCLAIM",
            "reason": "bound constants and operator norms are missing",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3074_0_3075",
            "next_checkpoint": "3075-Y5-R2FR-parent-field-inventory-no-independent-Gamma-or-P4-vector-under-AX1090.md",
            "script": "scripts/Y5_R2FR_parent_field_inventory_no_independent_Gamma_or_P4_vector_under_AX1090_3075.py",
            "mission": "try to parent-sign the field inventory/no-independent-Gamma/no-hypermomentum grammar; if not, promote the P4 connection source pack into explicit nonclaim rows",
            "starting_equation": "K_conn_bar <= C_conn(deltaGamma_LC*O1 + deltaG_AB*O2 + deltastar*O3 + deltaD*O4) + K_P4_bar",
            "claim_policy": "no K_conn zero, Khat, q_loc or local-GR claim unless the parent geometry stack and residual symbol match are both signed",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["grammar"], grammar_rows)
write_csv(OUTPUTS["zero"], zero_rows)
write_csv(OUTPUTS["bound"], bound_rows)
write_csv(OUTPUTS["p4"], p4_rows)
write_csv(OUTPUTS["symbol_match"], symbol_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["claim_status"], claim_rows)
write_csv(OUTPUTS["next"], next_rows)

copy_csv(OUTPUTS["grammar"], BRANCH_OUTPUTS["grammar_copy"])
copy_csv(OUTPUTS["zero"], BRANCH_OUTPUTS["zero_copy"])
copy_csv(OUTPUTS["bound"], BRANCH_OUTPUTS["bound_copy"])
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
        ("BC3074_0_grammar", OUTPUTS["grammar"], BRANCH_OUTPUTS["grammar_copy"]),
        ("BC3074_1_zero", OUTPUTS["zero"], BRANCH_OUTPUTS["zero_copy"]),
        ("BC3074_2_bound", OUTPUTS["bound"], BRANCH_OUTPUTS["bound_copy"]),
        ("BC3074_3_p4", OUTPUTS["p4"], BRANCH_OUTPUTS["p4_copy"]),
        ("BC3074_4_next", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
]
write_csv(OUTPUTS["branches"], branch_rows)
write_csv(
    OUTPUTS["validation"],
    [
        base(
            {
                "validation_id": "VAL3074_PRE",
                "passed": "False",
                "requirement": "placeholder overwritten by final validation",
                "evidence": "generator ordering guard",
            }
        )
    ],
)
DOC.write_text("# 3074 draft\n", encoding="utf-8")

dotg_hash_after = file_hash(DOTG_TARGET)
generated_csvs = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values())
formalization_3074 = list(FORMALIZATION.rglob("*3074*")) if FORMALIZATION.exists() else []

validation_rows = [
    base(
        {
            "validation_id": "VAL3074_00_sources_exist",
            "passed": str(all(row["exists"] == "True" for row in source_register)),
            "requirement": "all cited source paths exist",
            "evidence": OUTPUTS["sources"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3074_01_sources_parse",
            "passed": str(all(row["parse_ok"] == "True" for row in source_register)),
            "requirement": "all cited CSV sources parse and markdown sources exist",
            "evidence": OUTPUTS["sources"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3074_02_csv_parse",
            "passed": str(all(csv_ok(path) for path in generated_csvs)),
            "requirement": "all generated and branch-copy CSVs parse cleanly",
            "evidence": "csv.DictReader parse check",
        }
    ),
    base(
        {
            "validation_id": "VAL3074_03_grammar_not_signed",
            "passed": str(not any(boolish(row["grammar_signed"]) for row in grammar_rows)),
            "requirement": "connection stack grammar remains unsigned",
            "evidence": OUTPUTS["grammar"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3074_04_Kconn_zero_not_claimed",
            "passed": str(not any(boolish(row["zero_proved"]) or boolish(row["theorem_signed"]) for row in zero_rows)),
            "requirement": "K_conn zero theorem remains unclaimed",
            "evidence": OUTPUTS["zero"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3074_05_Kconn_bound_nonclaim",
            "passed": str(not has_claim_true(bound_rows)),
            "requirement": "K_conn bound rows remain nonclaim and nonnumeric",
            "evidence": OUTPUTS["bound"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3074_06_P4_fallback_retained",
            "passed": str(any(row["status"] == "MANDATORY_FALLBACK_IF_NO_GRAMMAR" for row in p4_rows) and not has_claim_true(p4_rows)),
            "requirement": "P4 connection fallback vector is retained but not claim-ready",
            "evidence": OUTPUTS["p4"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3074_07_symbol_match_open",
            "passed": str(all("MISSING" in row["missing_for_claim"] for row in symbol_rows)),
            "requirement": "Gamma_eff/Khat/q_loc symbol matching remains open",
            "evidence": OUTPUTS["symbol_match"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3074_08_no_local_gr_claim",
            "passed": str(not has_claim_true(claim_rows)),
            "requirement": "no Khat, q_loc, local-GR, PPN, R10, clock or orbital claim is promoted",
            "evidence": OUTPUTS["claim_status"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3074_09_next_target_selected",
            "passed": str(next_rows[0]["next_checkpoint"].startswith("3075-Y5-R2FR-parent-field-inventory")),
            "requirement": "next target moves to parent field inventory/no-independent Gamma",
            "evidence": OUTPUTS["next"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3074_10_branch_copies_exist",
            "passed": str(all(row["copy_exists"] == "True" and row["copy_parse_ok"] == "True" for row in branch_rows)),
            "requirement": "branch copies exist and parse",
            "evidence": OUTPUTS["branches"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3074_11_dotg_unchanged",
            "passed": str(dotg_hash_before == dotg_hash_after),
            "requirement": "P8_time_drift_residual_or_zero.csv is not modified",
            "evidence": f"{dotg_hash_before}->{dotg_hash_after}",
        }
    ),
    base(
        {
            "validation_id": "VAL3074_12_outputs_under_post_checkpoint",
            "passed": str(all(under(path, ROOT) for path in generated_csvs + [DOC])),
            "requirement": "all outputs are under post-checkpoint-work",
            "evidence": "path containment check",
        }
    ),
    base(
        {
            "validation_id": "VAL3074_13_no_formalization_workbench_outputs",
            "passed": str(not formalization_3074 and all(not under(path, FORMALIZATION) for path in generated_csvs + [DOC])),
            "requirement": "formalization-workbench modified-file count for 3074 outputs remains zero",
            "evidence": f"formalization_3074_matches={len(formalization_3074)}",
        }
    ),
    base(
        {
            "validation_id": "VAL3074_14_pycache_absent",
            "passed": str(not PYCACHE.exists()),
            "requirement": "scripts __pycache__ is absent at generator completion",
            "evidence": str(PYCACHE),
        }
    ),
    base(
        {
            "validation_id": "VAL3074_15_doc_written",
            "passed": str(DOC.exists()),
            "requirement": "checkpoint markdown document is written",
            "evidence": str(DOC),
        }
    ),
    base(
        {
            "validation_id": "VAL3074_16_Kconn_envelope_contains_P4",
            "passed": str(any("K_P4_bar" in row["bound_formula"] for row in bound_rows)),
            "requirement": "K_conn bound includes P4 fallback residue",
            "evidence": OUTPUTS["bound"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3074_17_field_inventory_gap_recorded",
            "passed": str(any("MISSING_PARENT_FIELD_INVENTORY" in row["missing_for_claim"] for row in grammar_rows)),
            "requirement": "field inventory gap is explicit",
            "evidence": OUTPUTS["grammar"].name,
        }
    ),
]

doc_text = f"""# 3074 - Connection Stack Grammar or Kconn Bound Fill

Status: `Y5_R2FR_3074_connection_stack_not_signed_Kconn_bound_P4_fallback_written`

Generated: `{RUN_UTC}`

## Verdict

3074 attacked the most GR-native hidden kernel, `K_conn`. The attractive theorem is exact as a conditional statement:

if the parent configuration is metric/coframe-only, `omega_obs=omega[e_obs]`, ordinary matter/source/readout sectors carry no independent `delta Gamma` hypermomentum, and `Gamma_eff/Khat/q_loc` use that same action/variation convention, then no extra MTS connection residual should remain beyond ordinary GR metric variation.

But the current corpus does not parent-sign those premises. The field inventory, no-independent-`Gamma` slot, no-hypermomentum condition, no-shadow-connection rule, and `Gamma_eff/Khat/q_loc` symbol match remain unsigned. Therefore 3074 does **not** claim `K_conn=0`, `Khat`, `q_loc=0`, local GR, PPN, R10, clocks, WEP, or orbital success.

The useful gain is that `K_conn` is now split into two explicit lanes:

- clean derivation lane: parent-sign the metric/coframe-only no-independent-connection grammar;
- fallback lane: keep `K_conn_bar <= K_LC_stack_bar + K_P4_bar`, where `K_P4_bar` collects torsion, nonmetricity, projective and hypermomentum residues.

## Connection Grammar Audit

{md_table(grammar_rows, ["grammar_id", "clause", "current_result", "grammar_signed", "missing_for_claim"])}

## Kconn Zero Attempt

{md_table(zero_rows, ["zero_id", "target", "result", "zero_proved", "why_not_enough"])}

## Kconn Bound Vector

{md_table(bound_rows, ["row_id", "quantity", "status", "bound_formula", "missing_for_claim"])}

## P4 Fallback Vector

{md_table(p4_rows, ["p4_id", "operator_family", "status", "missing_for_claim"])}

## Symbol Match Ledger

{md_table(symbol_rows, ["symbol_id", "object", "current_status", "consequence", "missing_for_claim"])}

## Decision

{md_table(decision_rows, ["decision_id", "decision", "reason", "next_action"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}

## Files

- Source register: `{OUTPUTS["sources"]}`
- Connection grammar audit: `{OUTPUTS["grammar"]}`
- Kconn zero attempt: `{OUTPUTS["zero"]}`
- Kconn bound vector: `{OUTPUTS["bound"]}`
- P4 fallback vector: `{OUTPUTS["p4"]}`
- Symbol match ledger: `{OUTPUTS["symbol_match"]}`
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

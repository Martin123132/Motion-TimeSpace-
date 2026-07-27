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

CHECKPOINT = "3073"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3073-Y5-R2FR-hidden-kernel-silence-or-bound-vector-fill-under-AX1090.md"
DOTG_TARGET = RESIDUALS / "P8_time_drift_residual_or_zero.csv"

SOURCE_PATHS = {
    "SRC3073_00_3072_doc": ROOT / "3072-Y5-R2FR-source-root-double-zero-local-lock-or-Mm-ML-bound-fill-under-AX1090.md",
    "SRC3073_01_3072_next": RESIDUALS / "P8_Y5_R2FR_3072_NEXT_TARGET.csv",
    "SRC3073_02_3072_hidden": RESIDUALS / "P8_Y5_R2FR_3072_HIDDEN_KERNEL_CONSEQUENCE_LEDGER.csv",
    "SRC3073_03_3072_bounds": RESIDUALS / "P8_Y5_R2FR_3072_MM_ML_COEFFICIENT_BOUND_ROWS_NONCLAIM.csv",
    "SRC3073_04_3070_kernel_audit": RESIDUALS / "P8_Y5_R2FR_3070_KMETRIC_KERNEL_NORM_AUDIT.csv",
    "SRC3073_05_3070_bound_vector": RESIDUALS / "P8_Y5_R2FR_3070_DELTA_G_SGAMMA_BOUND_VECTOR_NONCLAIM.csv",
    "SRC3073_06_1289_derivative": RESIDUALS / "P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
    "SRC3073_07_776_kgamma": RESIDUALS / "P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
    "SRC3073_08_2539_connection_decision": RESIDUALS / "P8_Y5_NO_SHADOW_2539_CONNECTION_GATE_DECISION_LEDGER.csv",
    "SRC3073_09_2659_operator_domain": RESIDUALS / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv",
    "SRC3073_10_1828_connection_audit": RAB_QUEUE / "P8_Y5_PARENT_QLOC_1828_CONNECTION_COMPATIBILITY_AUDIT.csv",
    "SRC3073_11_1829_metric_only": RAB_QUEUE / "P8_Y5_PARENT_QLOC_1829_METRIC_ONLY_CONNECTION_THEOREM_ATTEMPT.csv",
    "SRC3073_12_1830_no_independent_connection": RAB_QUEUE / "P8_Y5_PARENT_QLOC_1830_NO_INDEPENDENT_CONNECTION_GRAMMAR_ATTEMPT.csv",
    "SRC3073_13_projector_silence": RESIDUALS / "P8_Y5_BRR545_PROJECTOR_SYMPLECTIC_SILENCE_THEOREM_ATTEMPT.csv",
    "SRC3073_14_projector_bound": RESIDUALS / "P8_Y5_BRR545_COMMUTATOR_PROJECTOR_BOUND_FILL_ROW.csv",
    "SRC3073_15_boundary_nohair": RESIDUALS / "P8_Y5_BRR545_BOUNDARY_COHOMOLOGY_NOHAIR_THEOREM_ATTEMPT.csv",
    "SRC3073_16_boundary_flux_bound": RESIDUALS / "P8_Y5_BRR545_BOUNDARY_FLUX_BOUND_FILL_ROW.csv",
    "SRC3073_17_2627_boundary_zero": RESIDUALS / "P8_Y5_MEMORY_SOURCE_BOUNDARY_2627_BOUNDARY_ZERO_GATE.csv",
    "SRC3073_18_2627_finite_pack": RESIDUALS / "P8_Y5_MEMORY_SOURCE_BOUNDARY_2627_FINITE_RESIDUAL_BOUND_PACK.csv",
    "SRC3073_19_1833_boundary_projective": RAB_QUEUE / "P8_Y5_PARENT_QLOC_1833_BOUNDARY_PROJECTIVE_LEDGER.csv",
    "SRC3073_20_1836_units_domain": RAB_QUEUE / "P8_Y5_PARENT_QLOC_1836_UNITS_AND_DOMAIN_LEDGER.csv",
    "SRC3073_21_dotg_target": DOTG_TARGET,
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3073_SOURCE_REGISTER.csv",
    "zero_audit": RESIDUALS / "P8_Y5_R2FR_3073_HIDDEN_KERNEL_ZERO_AUDIT.csv",
    "bounds": RESIDUALS / "P8_Y5_R2FR_3073_HIDDEN_KERNEL_BOUND_VECTOR_NONCLAIM.csv",
    "microlemma": RESIDUALS / "P8_Y5_R2FR_3073_SCALAR_DERIVATIVE_CONNECTION_MICROLEMMA.csv",
    "local_gr": RESIDUALS / "P8_Y5_R2FR_3073_LOCAL_GR_CONSEQUENCE_LEDGER.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3073_DECISION_LEDGER.csv",
    "claim_status": RESIDUALS / "P8_Y5_R2FR_3073_CLAIM_STATUS.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3073_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3073_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3073_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "zero_copy": PARENT_ACTION / "hidden_kernel_zero_audit_3073_NOT_SIGNED.csv",
    "microlemma_copy": PARENT_ACTION / "scalar_derivative_connection_microlemma_3073_CONDITIONAL.csv",
    "bound_copy": LOCAL_BOUNDS / "hidden_kernel_bound_vector_3073_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3073_connection_stack_grammar_or_Kconn_bound_NEXT_NONCLAIM.csv",
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
        "bound_ready",
        "numeric_ready",
        "local_gr_claim",
        "khat_claim",
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
            "role": "hidden_kernel_silence_or_bound_evidence" if source_id != "SRC3073_21_dotg_target" else "append_guard_target",
            "status": "PRESENT" if path.exists() else "MISSING_SOURCE",
        }
    )
    for source_id, path in SOURCE_PATHS.items()
]

zero_rows = [
    base(
        {
            "audit_id": "HKZ3073_0_K_conn_scalar_lower_microzero",
            "kernel": "K_conn",
            "attempted_zero": "For a scalar source with a lower derivative, nabla_mu Gamma_eff = partial_mu Gamma_eff, so there is no Christoffel term in that narrow object.",
            "result": "MICROLEMMA_TRUE_BUT_TOO_NARROW",
            "zero_proved": "false",
            "theorem_signed": "false",
            "missing_for_claim": "MISSING_RAISED_INDEX_RESPONSE;MISSING_HILBERT_VARIATION_OF_OPERATOR_STACK;MISSING_GAB_HODGE_DERIVATIVE_RESPONSE",
            "source_ids": "SRC3073_06_1289_derivative;SRC3073_07_776_kgamma",
        }
    ),
    base(
        {
            "audit_id": "HKZ3073_1_K_conn_metric_only_route",
            "kernel": "K_conn",
            "attempted_zero": "If the parent grammar is metric/coframe-only and omega=omega[e_obs] with no independent connection charge, the connection stack can be reduced to ordinary GR geometry plus explicit metric variation.",
            "result": "EXACT_CONDITIONAL_LEMMA_NOT_PARENT_SIGNED",
            "zero_proved": "false",
            "theorem_signed": "false",
            "missing_for_claim": "MISSING_PARENT_FIELD_INVENTORY;MISSING_NO_INDEPENDENT_GAMMA_SLOT;MISSING_NO_HYPERMOMENTUM;MISSING_GAMMA_KHAT_SYMBOL_MATCH",
            "source_ids": "SRC3073_10_1828_connection_audit;SRC3073_11_1829_metric_only;SRC3073_12_1830_no_independent_connection",
        }
    ),
    base(
        {
            "audit_id": "HKZ3073_2_K_domain_projector_route",
            "kernel": "K_domain",
            "attempted_zero": "A topological or parent-fixed projector/domain could commute with differentiation and carry no Hilbert stress.",
            "result": "CONDITIONAL_PROJECTOR_SILENCE_NOT_PARENT_OWNED",
            "zero_proved": "false",
            "theorem_signed": "false",
            "missing_for_claim": "MISSING_FIXED_DOMAIN;MISSING_PROJECTOR_METRIC_SILENCE;MISSING_COMMUTATOR_ZERO;MISSING_SOURCE_CHARGE_EQUALITY",
            "source_ids": "SRC3073_13_projector_silence;SRC3073_14_projector_bound;SRC3073_09_2659_operator_domain",
        }
    ),
    base(
        {
            "audit_id": "HKZ3073_3_K_boundary_nohair_route",
            "kernel": "K_boundary",
            "attempted_zero": "Boundary/cohomology no-hair can silence the boundary if exact improvement, no flux, fixed reference, and homogeneous scalar boundary data are parent-owned.",
            "result": "CONDITIONAL_BOUNDARY_NOHAIR_NOT_PARENT_OWNED",
            "zero_proved": "false",
            "theorem_signed": "false",
            "missing_for_claim": "MISSING_BOUNDARY_NO_FLUX;MISSING_RELATIVE_CLASS_SELECTION;MISSING_FIXED_REFERENCE;MISSING_NO_WALL_STRESS",
            "source_ids": "SRC3073_15_boundary_nohair;SRC3073_16_boundary_flux_bound;SRC3073_17_2627_boundary_zero",
        }
    ),
    base(
        {
            "audit_id": "HKZ3073_4_zero_verdict",
            "kernel": "all hidden kernels",
            "attempted_zero": "K_conn=K_domain=K_boundary=0 would close the algebraic double-zero residual into a local-GR candidate branch.",
            "result": "ZERO_ROUTE_NOT_CLOSED_BOUND_VECTOR_REQUIRED",
            "zero_proved": "false",
            "theorem_signed": "false",
            "missing_for_claim": "MISSING_CONNECTION_STACK_THEOREM;MISSING_DOMAIN_PROJECTOR_THEOREM;MISSING_BOUNDARY_NOHAIR_THEOREM;MISSING_OBSERVABLE_PROJECTION",
            "source_ids": "SRC3073_02_3072_hidden;SRC3073_04_3070_kernel_audit;SRC3073_05_3070_bound_vector",
        }
    ),
]

microlemma_rows = [
    base(
        {
            "lemma_id": "SCL3073_0_scalar_derivative",
            "statement": "For any scalar S, nabla_mu S = partial_mu S; therefore the lower-index first derivative of Gamma_eff has no Christoffel symbol.",
            "proof_status": "EXACT_DIFFERENTIAL_GEOMETRY_MICROLEMMA",
            "promotion_status": "NOT_ENOUGH_FOR_LOCAL_GR",
            "reason": "The local residual uses Hilbert metric response, raised/projected components, field-space operators, Hodge/domain maps, and boundary terms, not only a lower scalar derivative.",
            "missing_for_claim": "MISSING_OPERATOR_STACK_REDUCTION;MISSING_PROJECTOR_SILENCE;MISSING_BOUNDARY_SILENCE",
            "source_ids": "SRC3073_06_1289_derivative;SRC3073_07_776_kgamma",
        }
    ),
    base(
        {
            "lemma_id": "SCL3073_1_metric_variation",
            "statement": "For Levi-Civita geometry, delta Gamma^rho_{mu nu}=1/2 g^{rho sigma}(nabla_mu h_{nu sigma}+nabla_nu h_{mu sigma}-nabla_sigma h_{mu nu}) plus higher order terms.",
            "proof_status": "STANDARD_VARIATION_TEMPLATE_RECORDED",
            "promotion_status": "BOUND_TEMPLATE_ONLY",
            "reason": "This gives the shape of K_conn but not the source-backed norm constants needed for PPN/R10/clock scoring.",
            "missing_for_claim": "MISSING_H_NORM;MISSING_DERIVATIVE_NORM;MISSING_OPERATOR_COEFFICIENTS;MISSING_WEAK_FIELD_NORMALIZATION",
            "source_ids": "SRC3073_10_1828_connection_audit;SRC3073_11_1829_metric_only",
        }
    ),
]

bound_rows = [
    base(
        {
            "row_id": "HKB3073_0_K_conn_bound",
            "kernel": "K_conn",
            "bound_formula": "||K_conn|| <= C_conn(||delta Gamma_LC|| ||O_1[S_Gamma]|| + ||delta G_AB|| ||O_2[R]|| + ||delta star|| ||O_3[R]|| + ||delta D|| ||O_4[R]||)",
            "status": "SYMBOLIC_BOUND_NONCLAIM",
            "numeric_ready": "false",
            "bound_ready": "false",
            "zero_route": "metric/coframe-only no-independent-connection grammar",
            "missing_for_claim": "MISSING_C_CONN;MISSING_DELTA_GAMMA_LC_NORM;MISSING_G_AB_RESPONSE;MISSING_HODGE_RESPONSE;MISSING_OPERATOR_NORMS",
            "source_ids": "SRC3073_07_776_kgamma;SRC3073_10_1828_connection_audit;SRC3073_12_1830_no_independent_connection",
        }
    ),
    base(
        {
            "row_id": "HKB3073_1_K_domain_bound",
            "kernel": "K_domain",
            "bound_formula": "||K_domain|| <= C_dom(||delta P_loc|| ||nabla Gamma_eff|| + ||[d,P_loc]J|| + ||delta chi_D|| ||S_Gamma|| + ||delta n|| ||boundary data||)",
            "status": "SYMBOLIC_BOUND_NONCLAIM",
            "numeric_ready": "false",
            "bound_ready": "false",
            "zero_route": "fixed topological/projector domain with commutator zero",
            "missing_for_claim": "MISSING_C_DOM;MISSING_DELTA_PLOC;MISSING_COMMUTATOR_NUMERIC_OR_ZERO;MISSING_DOMAIN_SELECTOR_RESPONSE;MISSING_COLLAR_GEOMETRY",
            "source_ids": "SRC3073_13_projector_silence;SRC3073_14_projector_bound;SRC3073_20_1836_units_domain",
        }
    ),
    base(
        {
            "row_id": "HKB3073_2_K_boundary_bound",
            "kernel": "K_boundary",
            "bound_formula": "||K_boundary|| <= C_B(|B_zero_flux| + |B_corner| + |B_reference_drift| + |B_transition_support| + |T_wall|)",
            "status": "SYMBOLIC_BOUND_NONCLAIM",
            "numeric_ready": "false",
            "bound_ready": "false",
            "zero_route": "boundary cohomology/no-hair/fixed-reference/no-flux theorem",
            "missing_for_claim": "MISSING_C_B;MISSING_BOUNDARY_FLUX_NUMERIC_OR_ZERO;MISSING_CORNER_TERM_BOUND;MISSING_REFERENCE_DRIFT;MISSING_WALL_STRESS_BOUND",
            "source_ids": "SRC3073_15_boundary_nohair;SRC3073_16_boundary_flux_bound;SRC3073_17_2627_boundary_zero;SRC3073_19_1833_boundary_projective",
        }
    ),
    base(
        {
            "row_id": "HKB3073_3_combined_hidden_vector",
            "kernel": "K_hidden",
            "bound_formula": "K_hidden_bar := K_conn_bar + K_domain_bar + K_boundary_bar",
            "status": "COMBINED_HIDDEN_VECTOR_NONCLAIM",
            "numeric_ready": "false",
            "bound_ready": "false",
            "zero_route": "all three hidden kernels theorem-zero in same branch",
            "missing_for_claim": "MISSING_K_CONN_BAR;MISSING_K_DOMAIN_BAR;MISSING_K_BOUNDARY_BAR;MISSING_COMMON_UNITS;MISSING_OBSERVABLE_PROJECTION",
            "source_ids": "SRC3073_04_3070_kernel_audit;SRC3073_20_1836_units_domain",
        }
    ),
    base(
        {
            "row_id": "HKB3073_4_E_SGamma_DZ_with_hidden_vector",
            "kernel": "E_SGamma_DZ_hidden",
            "bound_formula": "E_SGamma_DZ <= (2/3)(L_min^-2 F2_bar Delta_m M_m_bar + L_min^-3 F2_bar Delta_m^2 M_L_bar + K_hidden_bar)",
            "status": "BEST_CURRENT_LOCAL_RESIDUAL_ENVELOPE_NONCLAIM",
            "numeric_ready": "false",
            "bound_ready": "false",
            "zero_route": "double-zero plus local lock plus hidden-kernel zero/bounds",
            "missing_for_claim": "MISSING_PARENT_DOUBLE_ZERO;MISSING_DELTA_m_AMPLITUDE_LAW;MISSING_K_HIDDEN_BAR;MISSING_UNITS;MISSING_ARENA_PROJECTIONS",
            "source_ids": "SRC3073_03_3072_bounds;SRC3073_04_3070_kernel_audit;SRC3073_05_3070_bound_vector",
        }
    ),
]

local_gr_rows = [
    base(
        {
            "impact_id": "LGR3073_0_GR_reduction_status",
            "question": "Does 3073 derive local GR/Newton?",
            "answer": "No. It identifies the conditional microlemma and writes a single hidden-kernel envelope, but the connection/domain/boundary theorems are not signed.",
            "local_gr_claim": "false",
            "khat_claim": "false",
            "next_requirement": "prove parent connection stack first, then domain/projector and boundary no-hair or finite bounds",
        }
    ),
    base(
        {
            "impact_id": "LGR3073_1_review_value",
            "question": "What is the real gain?",
            "answer": "The local branch now has one explicit residual vector instead of unnamed gremlins: algebraic double-zero leakage plus K_hidden_bar.",
            "local_gr_claim": "false",
            "khat_claim": "false",
            "next_requirement": "make K_hidden_bar theorem-zero or source-backed numeric",
        }
    ),
    base(
        {
            "impact_id": "LGR3073_2_best_next",
            "question": "Which hidden kernel should be attacked first?",
            "answer": "K_conn. A metric/coframe-only/no-independent-connection grammar is the most GR-native route and is less closure-looking than simply imposing boundary/projector silence.",
            "local_gr_claim": "false",
            "khat_claim": "false",
            "next_requirement": "connection stack grammar or K_conn finite bound",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3073_0_zero_result",
            "decision": "hidden-kernel zero proof not closed",
            "reason": "Every route has an exact conditional lemma, but none is parent-signed in the current corpus.",
            "consequence": "retain K_conn_bar, K_domain_bar, K_boundary_bar in the official local residual envelope",
            "next_action": "target K_conn first",
        }
    ),
    base(
        {
            "decision_id": "DEC3073_1_microlemma",
            "decision": "record scalar lower-derivative connection microzero",
            "reason": "It prevents us from overstating K_conn in the narrow scalar-gradient object while preserving the real operator-stack obstruction.",
            "consequence": "useful derivation note, not a local-GR pass",
            "next_action": "derive metric/coframe-only operator stack",
        }
    ),
    base(
        {
            "decision_id": "DEC3073_2_next_target",
            "decision": "3074 connection stack grammar",
            "reason": "K_conn is closest to the GR reduction theorem and controls whether MTS can look like metric-only GR locally.",
            "consequence": "domain and boundary remain queued after K_conn",
            "next_action": "3074-Y5-R2FR-connection-stack-grammar-or-Kconn-bound-fill-under-AX1090.md",
        }
    ),
]

claim_rows = [
    base(
        {
            "claim_id": "CLAIM3073_0_hidden_zero",
            "claim": "K_conn=K_domain=K_boundary=0",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "conditional routes exist but no same-branch parent theorem signs them",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3073_1_local_gr",
            "claim": "local GR/Newton/PPN/R10 pass",
            "claim_active": "false",
            "status": "BLOCKED",
            "reason": "hidden kernel envelope is symbolic and not projected into observables",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3073_2_scalar_microlemma",
            "claim": "lower scalar derivative has no Christoffel term",
            "claim_active": "false",
            "status": "TRUE_MICROLEMMA_NOT_PROMOTED",
            "reason": "true but too narrow for Khat/q_loc/local-GR",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3073_0_3074",
            "next_checkpoint": "3074-Y5-R2FR-connection-stack-grammar-or-Kconn-bound-fill-under-AX1090.md",
            "script": "scripts/Y5_R2FR_connection_stack_grammar_or_Kconn_bound_fill_under_AX1090_3074.py",
            "mission": "try to parent-sign metric/coframe-only no-independent-connection grammar and reduce K_conn; if not, fill K_conn_bar as an explicit nonclaim coefficient",
            "starting_equation": "E_SGamma_DZ <= (2/3)(L_min^-2 F2_bar Delta_m M_m_bar + L_min^-3 F2_bar Delta_m^2 M_L_bar + K_conn_bar + K_domain_bar + K_boundary_bar)",
            "claim_policy": "no local-GR claim unless K_conn is zero/bounded and K_domain/K_boundary plus observable projection are also handled",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["zero_audit"], zero_rows)
write_csv(OUTPUTS["bounds"], bound_rows)
write_csv(OUTPUTS["microlemma"], microlemma_rows)
write_csv(OUTPUTS["local_gr"], local_gr_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["claim_status"], claim_rows)
write_csv(OUTPUTS["next"], next_rows)

copy_csv(OUTPUTS["zero_audit"], BRANCH_OUTPUTS["zero_copy"])
copy_csv(OUTPUTS["microlemma"], BRANCH_OUTPUTS["microlemma_copy"])
copy_csv(OUTPUTS["bounds"], BRANCH_OUTPUTS["bound_copy"])
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
        ("BC3073_0_zero_audit", OUTPUTS["zero_audit"], BRANCH_OUTPUTS["zero_copy"]),
        ("BC3073_1_microlemma", OUTPUTS["microlemma"], BRANCH_OUTPUTS["microlemma_copy"]),
        ("BC3073_2_bounds", OUTPUTS["bounds"], BRANCH_OUTPUTS["bound_copy"]),
        ("BC3073_3_next", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
]
write_csv(OUTPUTS["branches"], branch_rows)
write_csv(
    OUTPUTS["validation"],
    [
        base(
            {
                "validation_id": "VAL3073_PRE",
                "passed": "False",
                "requirement": "placeholder overwritten by final validation",
                "evidence": "generator ordering guard",
            }
        )
    ],
)
DOC.write_text("# 3073 draft\n", encoding="utf-8")

dotg_hash_after = file_hash(DOTG_TARGET)
generated_csvs = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values())
formalization_3073 = list(FORMALIZATION.rglob("*3073*")) if FORMALIZATION.exists() else []

validation_rows = [
    base(
        {
            "validation_id": "VAL3073_00_sources_exist",
            "passed": str(all(row["exists"] == "True" for row in source_register)),
            "requirement": "all cited source paths exist",
            "evidence": OUTPUTS["sources"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3073_01_sources_parse",
            "passed": str(all(row["parse_ok"] == "True" for row in source_register)),
            "requirement": "all cited CSV sources parse and markdown sources exist",
            "evidence": OUTPUTS["sources"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3073_02_csv_parse",
            "passed": str(all(csv_ok(path) for path in generated_csvs)),
            "requirement": "all generated and branch-copy CSVs parse cleanly",
            "evidence": "csv.DictReader parse check",
        }
    ),
    base(
        {
            "validation_id": "VAL3073_03_hidden_zero_not_claimed",
            "passed": str(not any(boolish(row["zero_proved"]) or boolish(row["theorem_signed"]) for row in zero_rows)),
            "requirement": "hidden-kernel zero theorem remains unsigned",
            "evidence": OUTPUTS["zero_audit"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3073_04_microlemma_not_promoted",
            "passed": str(all(row["promotion_status"] != "LOCAL_GR_CLAIM" for row in microlemma_rows)),
            "requirement": "scalar derivative microlemma is recorded but not promoted",
            "evidence": OUTPUTS["microlemma"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3073_05_bound_rows_nonclaim",
            "passed": str(not has_claim_true(bound_rows)),
            "requirement": "hidden-kernel bound rows remain nonclaim and nonnumeric",
            "evidence": OUTPUTS["bounds"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3073_06_all_hidden_kernels_present",
            "passed": str({"K_conn", "K_domain", "K_boundary"}.issubset({row["kernel"] for row in bound_rows})),
            "requirement": "K_conn, K_domain and K_boundary rows are present",
            "evidence": OUTPUTS["bounds"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3073_07_combined_envelope_present",
            "passed": str(any("K_hidden_bar" in row["bound_formula"] and "E_SGamma_DZ" in row["kernel"] for row in bound_rows)),
            "requirement": "combined hidden vector enters E_SGamma_DZ envelope",
            "evidence": OUTPUTS["bounds"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3073_08_no_local_gr_claim",
            "passed": str(not has_claim_true(claim_rows + local_gr_rows)),
            "requirement": "no Khat, q_loc, local-GR, PPN, R10, clock or orbital claim is promoted",
            "evidence": OUTPUTS["claim_status"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3073_09_next_target_selected",
            "passed": str(next_rows[0]["next_checkpoint"].startswith("3074-Y5-R2FR-connection-stack")),
            "requirement": "next target moves to connection stack grammar or Kconn bound",
            "evidence": OUTPUTS["next"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3073_10_branch_copies_exist",
            "passed": str(all(row["copy_exists"] == "True" and row["copy_parse_ok"] == "True" for row in branch_rows)),
            "requirement": "branch copies exist and parse",
            "evidence": OUTPUTS["branches"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3073_11_dotg_unchanged",
            "passed": str(dotg_hash_before == dotg_hash_after),
            "requirement": "P8_time_drift_residual_or_zero.csv is not modified",
            "evidence": f"{dotg_hash_before}->{dotg_hash_after}",
        }
    ),
    base(
        {
            "validation_id": "VAL3073_12_outputs_under_post_checkpoint",
            "passed": str(all(under(path, ROOT) for path in generated_csvs + [DOC])),
            "requirement": "all outputs are under post-checkpoint-work",
            "evidence": "path containment check",
        }
    ),
    base(
        {
            "validation_id": "VAL3073_13_no_formalization_workbench_outputs",
            "passed": str(not formalization_3073 and all(not under(path, FORMALIZATION) for path in generated_csvs + [DOC])),
            "requirement": "formalization-workbench modified-file count for 3073 outputs remains zero",
            "evidence": f"formalization_3073_matches={len(formalization_3073)}",
        }
    ),
    base(
        {
            "validation_id": "VAL3073_14_pycache_absent",
            "passed": str(not PYCACHE.exists()),
            "requirement": "scripts __pycache__ is absent at generator completion",
            "evidence": str(PYCACHE),
        }
    ),
    base(
        {
            "validation_id": "VAL3073_15_doc_written",
            "passed": str(DOC.exists()),
            "requirement": "checkpoint markdown document is written",
            "evidence": str(DOC),
        }
    ),
    base(
        {
            "validation_id": "VAL3073_16_connection_priority_recorded",
            "passed": str(any("K_conn" in row["answer"] or "connection" in row["next_requirement"].lower() for row in local_gr_rows)),
            "requirement": "K_conn is selected as the next priority",
            "evidence": OUTPUTS["local_gr"].name,
        }
    ),
]

doc_text = f"""# 3073 - Hidden Kernel Silence or Bound Vector Fill

Status: `Y5_R2FR_3073_hidden_kernel_zero_not_signed_Khidden_bound_vector_written`

Generated: `{RUN_UTC}`

## Verdict

3073 attacked the three remaining hidden kernels after the double-zero/local-lock pass:

- `K_conn`: connection/operator/Hodge/field-space metric response.
- `K_domain`: projector/domain/collar response.
- `K_boundary`: boundary/reference/corner/transition response.

The honest result is mixed in the useful way. There is one real microlemma: for a scalar `S`, `nabla_mu S = partial_mu S`, so the lower-index first derivative of `Gamma_eff` carries no Christoffel symbol. But that does **not** close the local branch, because the residual being audited is a Hilbert metric-response/object-stack quantity with raised/projected components, operator response, domain/projector response, and boundary terms.

So 3073 does **not** claim `K_conn=K_domain=K_boundary=0`, `Khat`, `q_loc=0`, local GR, PPN, R10, clocks, WEP, or orbital success. It does replace the loose phrase "hidden kernels" with one official nonclaim envelope:

`E_SGamma_DZ <= (2/3)(L_min^-2 F2_bar Delta_m M_m_bar + L_min^-3 F2_bar Delta_m^2 M_L_bar + K_hidden_bar)`,

where `K_hidden_bar := K_conn_bar + K_domain_bar + K_boundary_bar`.

## Zero Audit

{md_table(zero_rows, ["audit_id", "kernel", "result", "zero_proved", "missing_for_claim"])}

## Scalar Connection Microlemma

{md_table(microlemma_rows, ["lemma_id", "proof_status", "promotion_status", "reason", "missing_for_claim"])}

## Hidden-Kernel Bound Vector

{md_table(bound_rows, ["row_id", "kernel", "status", "bound_formula", "missing_for_claim"])}

## Local-GR Consequence

{md_table(local_gr_rows, ["impact_id", "answer", "next_requirement"])}

## Decision

{md_table(decision_rows, ["decision_id", "decision", "reason", "next_action"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}

## Files

- Source register: `{OUTPUTS["sources"]}`
- Hidden zero audit: `{OUTPUTS["zero_audit"]}`
- Hidden bound vector: `{OUTPUTS["bounds"]}`
- Scalar derivative microlemma: `{OUTPUTS["microlemma"]}`
- Local-GR consequence ledger: `{OUTPUTS["local_gr"]}`
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

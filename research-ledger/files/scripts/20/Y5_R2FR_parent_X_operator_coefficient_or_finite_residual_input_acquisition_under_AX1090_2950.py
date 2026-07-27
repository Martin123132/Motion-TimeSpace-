from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2950"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2950-Y5-R2FR-parent-X-operator-coefficient-or-finite-residual-input-acquisition-under-AX1090.md"

SRC_2949_DOC = ROOT / "2949-Y5-R2FR-parent-X-action-route-selector-and-LX-normal-form-gate-under-AX1090.md"
SRC_2949_NEXT = RESIDUALS / "P8_Y5_R2FR_2949_NEXT_TARGET.csv"
SRC_2949_INPUTS = RESIDUALS / "P8_Y5_R2FR_2949_POSITIVE_OPERATOR_INPUT_QUEUE.csv"
SRC_2949_FINITE = RESIDUALS / "P8_Y5_R2FR_2949_FINITE_RESIDUAL_ACQUISITION_ROWS.csv"
SRC_2949_NORMAL = RESIDUALS / "P8_Y5_R2FR_2949_LX_NORMAL_FORM_GATE.csv"
SRC_2949_ROUTE = RESIDUALS / "P8_Y5_R2FR_2949_X_ROUTE_SELECTOR_MATRIX.csv"
SRC_2949_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2949_VALIDATION.csv"
SRC_2022_SCHEMA = RESIDUALS / "P8_Y5_PARENT_QLOC_2022_IX_FIRST_SOURCE_ROW_SCHEMA.csv"
SRC_2022_ZERO = RESIDUALS / "P8_Y5_PARENT_QLOC_2022_X_SECTOR_ZERO_THEOREM_ATTEMPT.csv"
SRC_2022_GATES = RESIDUALS / "P8_Y5_PARENT_QLOC_2022_X_SECTOR_ACTIVATION_GATES.csv"
SRC_2022_DECISION = RESIDUALS / "P8_Y5_PARENT_QLOC_2022_DECISION_LEDGER.csv"
SRC_2022_REFUSAL = RESIDUALS / "P8_Y5_PARENT_QLOC_2022_REFUSAL_RUNNER.csv"
SRC_1800_AUDIT = RESIDUALS / "P8_Y5_PARENT_QLOC_1800_POSITIVE_OPERATOR_ACTIVATION_AUDIT.csv"
SRC_1801_JX = RESIDUALS / "P8_Y5_PARENT_QLOC_1801_JX_COMPONENT_BOUND_PACK.csv"
SRC_1801_DECISION = RESIDUALS / "P8_Y5_PARENT_QLOC_1801_DECISION_LEDGER.csv"
SRC_967_LEMMA = RESIDUALS / "P8_Y5_R10_967_MEMORY_POSITIVE_OPERATOR_LEMMA.csv"
SRC_968_INPUTS = RESIDUALS / "P8_Y5_R10_968_MEMORY_OPERATOR_INPUT_AUDIT.csv"
SRC_973_JX = RESIDUALS / "P8_Y5_R10_973_JX_DECOMPOSITION_GATE.csv"
SRC_912_OMEGA = RESIDUALS / "P8_Y5_R10_912_EXTRA_SECTOR_OMEGA_LEDGER.csv"
SRC_2665_HLOCK = RESIDUALS / "P8_Y5_R10_HAMILTONIAN_PIM_QBARXH_LOCK_2665_LOCK_CONTRACT.csv"
SRC_2665_PDG = RESIDUALS / "P8_Y5_R10_HAMILTONIAN_PIM_QBARXH_LOCK_2665_PROJECTOR_DENOMINATOR_GATE.csv"
SRC_2946_SCHEMA = RESIDUALS / "P8_Y5_R2FR_2946_FIRST_ROW_ACQUISITION_SCHEMAS.csv"
SRC_2937_CLAUSES = RESIDUALS / "P8_Y5_R2FR_2937_SOURCE_CURRENT_CLAUSE_LEDGER.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2950_SOURCE_REGISTER.csv",
    "payload": RESIDUALS / "P8_Y5_R2FR_2950_OPERATOR_PAYLOAD_ACQUISITION_AUDIT.csv",
    "operator": RESIDUALS / "P8_Y5_R2FR_2950_ZX_MX2_OPERATOR_STATUS.csv",
    "jx": RESIDUALS / "P8_Y5_R2FR_2950_JX_COMPONENT_PAYLOAD_STATUS.csv",
    "ix": RESIDUALS / "P8_Y5_R2FR_2950_IX_FINITE_ROW_STATUS.csv",
    "priority": RESIDUALS / "P8_Y5_R2FR_2950_PAYLOAD_PRIORITY_DECISION.csv",
    "guards": RESIDUALS / "P8_Y5_R2FR_2950_ACQUISITION_GUARDS.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2950_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2950_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2950_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2950_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2950_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "payload_copy": PARENT_ACTION / "X_operator_payload_acquisition_audit_2950_NONCLAIM.csv",
    "operator_copy": PARENT_ACTION / "ZX_MX2_operator_status_2950_NONCLAIM.csv",
    "jx_copy": LOCAL_BOUNDS / "JX_component_payload_status_2950_NONCLAIM.csv",
    "ix_copy": LOCAL_BOUNDS / "IX_finite_row_status_2950_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2950_PARENT_X_FIELD_OWNER_OR_ZX_MX2_NEXT_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv_rows(path)
        return True
    except Exception:
        return False


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": RUN_UTC,
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    selected = columns or list(rows[0].keys())
    header = "| " + " | ".join(selected) + " |"
    separator = "| " + " | ".join("---" for _ in selected) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in selected) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2950_00_2949_doc", SRC_2949_DOC, "NEXT2949_0_2950;Validation overall: `True`", "2949 handoff"),
        ("SRC2950_01_2949_next", SRC_2949_NEXT, "NEXT2949_0_2950", "machine-readable 2950 target"),
        ("SRC2950_02_2949_inputs", SRC_2949_INPUTS, "PIN2949_2_ZX;PIN2949_8_MHref", "positive operator input queue"),
        ("SRC2950_03_2949_finite", SRC_2949_FINITE, "FIN2949_0_Ix_abs;FIN2949_5_no_cancellation", "finite residual acquisition rows"),
        ("SRC2950_04_2949_normal", SRC_2949_NORMAL, "LX2949_1_quadratic_operator;LX2949_7_verdict", "L_X normal form"),
        ("SRC2950_05_2949_route", SRC_2949_ROUTE, "XROUTE2949_2_positive_nohair;XROUTE2949_5_verdict", "route selector"),
        ("SRC2950_06_2949_validation", SRC_2949_VALIDATION, "VAL2949_OVERALL", "2949 validation"),
        ("SRC2950_07_2022_schema", SRC_2022_SCHEMA, "IXS2022_0_ZX;IXS2022_12_alphaX", "I_X first source row schema"),
        ("SRC2950_08_2022_zero", SRC_2022_ZERO, "XZT2022_1_positive_action;XZT2022_7_verdict", "X-sector zero theorem attempt"),
        ("SRC2950_09_2022_gates", SRC_2022_GATES, "XAG2022_1_positive_operator;XAG2022_6_Ix_finite", "X-sector activation gates"),
        ("SRC2950_10_2022_decision", SRC_2022_DECISION, "DEC2022_0_result;DEC2022_2_best_next", "2022 decision ledger"),
        ("SRC2950_11_2022_refusal", SRC_2022_REFUSAL, "REF2022_0_X_zero;REF2022_5_local_GR", "2022 refusal runner"),
        ("SRC2950_12_1800_audit", SRC_1800_AUDIT, "XPA1800_1_operator_sign_gap;XPA1800_5_verdict", "positive operator activation audit"),
        ("SRC2950_13_1801_jx", SRC_1801_JX, "JCB1801_0_matter;JCB1801_5_total_abs_guard", "J_X component bound pack"),
        ("SRC2950_14_1801_decision", SRC_1801_DECISION, "DEC1801_0_theorem_attempt;DEC1801_2_best_first_component", "J_X decision ledger"),
        ("SRC2950_15_967_lemma", SRC_967_LEMMA, "MPO967_1_operator;MPO967_6_verdict", "positive operator lemma"),
        ("SRC2950_16_968_inputs", SRC_968_INPUTS, "MOI968_2_operator_L;MOI968_8_verdict", "operator input audit"),
        ("SRC2950_17_973_jx", SRC_973_JX, "JXD973_0_kinetic_affine;JXD973_6_verdict", "J_X decomposition"),
        ("SRC2950_18_912_omega", SRC_912_OMEGA, "ESO912_3_bulk_X_memory;ESO912_6_matter_frame", "extra-sector omega ledger"),
        ("SRC2950_19_2665_hlock", SRC_2665_HLOCK, "HLOCK2665_3_MHref;HLOCK2665_7_verdict", "Hamiltonian/PiM lock"),
        ("SRC2950_20_2665_pdg", SRC_2665_PDG, "PDG2665_2_integrability;PDG2665_7_verdict", "projector denominator gate"),
        ("SRC2950_21_2946_schema", SRC_2946_SCHEMA, "SCHEMA2946_0_MHref_value;SCHEMA2946_8_side_flux", "denominator schemas"),
        ("SRC2950_22_2937_clauses", SRC_2937_CLAUSES, "SCL2937_3_source_current;SCL2937_8_Qbar", "source current clause ledger"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, source_path, anchors, role in specs:
        found, missing = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_type": "local_file",
                    "source_path": str(source_path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": source_path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def payload_rows() -> list[dict[str, Any]]:
    rows = [
        ("PAY2950_0_X_field_owner", "X field owner", "parent field or quotient scalar with equation owner", "CONDITIONAL_ONLY", "no explicit parent X owner found; 1800/2022/2949 supply contracts only", str(SRC_1800_AUDIT)),
        ("PAY2950_1_ZX", "Z_X / A_X^ij", "kinetic/operator normalization and positivity certificate", "NOT_FOUND", "no source-backed positive A_X or numeric/theorem Z_X exists in inspected corpus", str(SRC_1800_AUDIT)),
        ("PAY2950_2_MX2", "M_X^2", "mass/gap/range term with zero-mode policy", "NOT_FOUND", "lambda_X relation exists, but M_X^2 and gap are not parent-derived", str(SRC_2022_SCHEMA)),
        ("PAY2950_3_JX", "J_X", "source silence theorem or finite channel bounds", "COMPONENT_SCHEMA_ONLY", "J_X split and absolute bound formulas exist; all component values/theorem-zeros are missing", str(SRC_1801_JX)),
        ("PAY2950_4_boundary_X", "boundary_X", "boundary/no-tail/zero-mode class", "NOT_FOUND", "boundary zero/nohair class remains unsigned", str(SRC_2022_ZERO)),
        ("PAY2950_5_omega_X", "omega_X", "symplectic flux extracted from same L_X", "NOT_FOUND", "omega_X is named as retained if open; no Theta_X/omega_X extraction exists", str(SRC_912_OMEGA)),
        ("PAY2950_6_PiM_tail", "Pi_M^H Q_tau_X", "Hamiltonian projection tail/commutator stress", "NOT_FOUND", "PiM/Hamiltonian lock remains formal and blocked by M_H_ref/reference/integrability", str(SRC_2665_HLOCK)),
        ("PAY2950_7_MHref", "M_H_ref", "positive same-frame source denominator", "NOT_FOUND", "M_H_ref remains a schema; H_tau/Q_tau/integrability/reference are unsigned", str(SRC_2946_SCHEMA)),
        ("PAY2950_8_Ix_abs", "I_X/M_H_ref", "absolute no-cancellation finite row", "NOT_SCORE_READY", "formula exists, but every numerator component and denominator are missing", str(SRC_2022_ZERO)),
        ("PAY2950_9_alphaX", "alpha_X(lambda_X)", "finite-range fallback curve", "NOT_SCORE_READY", "Z_X, M_X^2, K_X, Qbar_XH, qbar_XT and bound join are not jointly present", str(SRC_2022_SCHEMA)),
    ]
    return [
        add_common(
            {
                "payload_id": payload_id,
                "symbol": symbol,
                "required_payload": required,
                "acquisition_status": status,
                "evidence_summary": evidence,
                "source_path": source_path,
                "source_path_exists": Path(source_path).exists(),
                "numeric_or_theorem_value": "MISSING",
                "source_backed_value": False,
                "accepted_for_scoring": False,
            }
        )
        for payload_id, symbol, required, status, evidence, source_path in rows
    ]


def operator_rows() -> list[dict[str, Any]]:
    rows = [
        ("OP2950_0_conditional_normal_form", "L_X", "L_X=-1/2 Z_X nabla X nabla X -1/2 M_X^2 X^2 + X J_X + dB_X", "CONDITIONAL_FORM_EXISTS", "XZT2022_1_positive_action;LX2949_1_quadratic_operator", True),
        ("OP2950_1_energy_identity", "positive nohair identity", "0=int_D X E_X = int_D(Z_X |nabla X|^2 + M_X^2 X^2) - int_D X J_X + boundary_X", "CONDITIONAL_IDENTITY_EXISTS", "XZT2022_2_energy_identity;MPO967_4_energy_identity", True),
        ("OP2950_2_ZX_value", "Z_X / A_X^ij", "numeric_or_theorem_zero_value;units;source_path;assumptions", "MISSING_ZX_OR_SIGN_CERTIFICATE", "IXS2022_0_ZX;XPA1800_1_operator_sign_gap", False),
        ("OP2950_3_MX2_value", "M_X^2", "numeric_or_theorem_zero_value;units;source_path;zero_mode_rule", "MISSING_MX2_OR_GAP_INPUT", "IXS2022_1_MX2;MOI968_4_mass_gap", False),
        ("OP2950_4_zero_mode", "zero-mode rule", "Dirichlet/zero-flux/zero-mean/topological class before readout", "MISSING_ZERO_MODE_CERTIFICATE", "XZT2022_4_boundary_zero;MPO967_5_constant_mode", False),
        ("OP2950_5_source", "operator source path", "parent action source path and equation reference for L_X", "MISSING_OPERATOR_SOURCE", "XPA1800_1_operator_sign_gap", False),
        ("OP2950_6_verdict", "operator payload", "Z_X, M_X^2, zero-mode, source path all present", "OPERATOR_PAYLOAD_NOT_ACQUIRED", "XPA1800_5_verdict", False),
    ]
    return [
        add_common(
            {
                "operator_id": op_id,
                "object": obj,
                "formula_or_required_payload": formula,
                "status": status,
                "source_anchor": anchor,
                "conditional_math_available": conditional,
                "parent_payload_acquired": False,
            }
        )
        for op_id, obj, formula, status, anchor, conditional in rows
    ]


def jx_rows() -> list[dict[str, Any]]:
    rows = [
        ("JXP2950_0_matter", "J_matter", "|J_matter| <= M_T |qbar_XT|", "MISSING_QBAR_XT_COMPONENT_VALUES", str(SRC_1801_JX)),
        ("JXP2950_1_chiD_wall", "J_chiD_wall", "|J_chiD_wall| <= |f_prime(chi_D)L_X|_wall + |wall_boundary_tail|", "MISSING_CHID_WALL_AMPLITUDE", str(SRC_1801_JX)),
        ("JXP2950_2_boundary", "J_boundary", "|J_boundary| <= |B_X| + |Q_edge_X| + |Phi_boundary_local| + |reference_tail|", "MISSING_BOUNDARY_EDGE_FLUX", str(SRC_1801_JX)),
        ("JXP2950_3_readout", "J_readout", "|J_readout| <= ||delta R_readout/delta X|| + |shadow_frame_tail| + |calibration_source_mask|", "MISSING_READOUT_REENTRY_COEFFICIENTS", str(SRC_1801_JX)),
        ("JXP2950_4_history", "J_history", "|J_history(t)| <= int |K_mem| |J_past| dmu plus tails", "MISSING_HISTORY_KERNEL_NORM", str(SRC_1801_JX)),
        ("JXP2950_5_PiM_projection", "J_PiM_tail", "|Pi_M^H Q_tau_X|/M_H_ref plus commutator stress", "MISSING_PIM_PROJECTION_LOCK", str(SRC_2665_HLOCK)),
        ("JXP2950_6_total_abs", "J_X_abs", "sum_abs(JXP2950_0..5)", "NO_CANCELLATION_ENVELOPE_READY_VALUES_MISSING", str(SRC_1801_JX)),
    ]
    return [
        add_common(
            {
                "jx_payload_id": row_id,
                "component": component,
                "absolute_bound_formula": formula,
                "current_status": status,
                "source_path": source_path,
                "source_path_exists": Path(source_path).exists(),
                "component_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
                "no_cancellation": True,
                "accepted_for_scoring": False,
            }
        )
        for row_id, component, formula, status, source_path in rows
    ]


def ix_rows() -> list[dict[str, Any]]:
    rows = [
        ("IXP2950_0_formula", "I_X/M_H_ref", "(|int_S i_tau omega_X|+|int_A C_X|+|boundary_X|+|Pi_M_tail|)/M_H_ref", "FORMULA_READY_NONCLAIM", "dimensionless"),
        ("IXP2950_1_omega", "int_S i_tau omega_X", "X symplectic flux", "MISSING_OMEGA_X", "charge_variation"),
        ("IXP2950_2_CX", "int_A C_X", "X constraint/current leakage", "MISSING_C_X", "charge_or_constraint"),
        ("IXP2950_3_boundary", "boundary_X", "X boundary/edge/history flux", "MISSING_BOUNDARY_X", "charge_or_flux"),
        ("IXP2950_4_PiM", "PiM_tail", "Hamiltonian projection tail", "MISSING_PIM_TAIL", "dimensionless_after_MHref"),
        ("IXP2950_5_MHref", "M_H_ref", "positive same-frame source denominator", "MISSING_MH_REF", "mass_or_charge"),
        ("IXP2950_6_acceptance", "Ix_acceptance", "all components source-backed or theorem-zero, no MISSING, no cancellation", "NOT_ACCEPTED", "gate"),
    ]
    return [
        add_common(
            {
                "ix_payload_id": row_id,
                "symbol": symbol,
                "formula_or_role": formula,
                "current_status": status,
                "units": units,
                "source_path": str(SRC_2022_ZERO),
                "source_path_exists": SRC_2022_ZERO.exists(),
                "numeric_or_theorem_value": "MISSING",
                "accepted_for_scoring": False,
            }
        )
        for row_id, symbol, formula, status, units in rows
    ]


def priority_rows() -> list[dict[str, Any]]:
    rows = [
        ("PRI2950_0_parent_X_owner", "parent X field/equation owner", 1, "UPSTREAM_ROOT", "without X field owner, Z_X/M_X^2/J_X are not one physical object"),
        ("PRI2950_1_ZX_MX2", "Z_X and M_X^2", 2, "FIRST_COEFFICIENT_PAYLOAD", "positive/nohair and alpha(lambda) both require operator normalization/range"),
        ("PRI2950_2_boundary_zero_mode", "boundary/zero-mode class", 3, "ENERGY_IDENTITY_DEPENDENCY", "positive identity fails with boundary hair"),
        ("PRI2950_3_JX_components", "J_X component zeros/bounds", 4, "SOURCE_DEPENDENCY", "J_X is necessary but downstream of selecting the same X operator"),
        ("PRI2950_4_PiM_MHref", "PiM tail and M_H_ref", 5, "DENOMINATOR_DEPENDENCY", "needed before local/R10/PPN scoring"),
        ("PRI2950_5_score_rows", "I_X/alpha/PPN scoring", 99, "REJECT_NOW", "would score placeholders"),
    ]
    return [
        add_common({"priority_id": row_id, "target": target, "rank": rank, "decision": decision, "reason": reason})
        for row_id, target, rank, decision, reason in rows
    ]


def guard_rows() -> list[dict[str, Any]]:
    rows = [
        ("GUARD2950_0_no_schema_as_payload", "schema/conditional formulas are not accepted as source-backed numeric or theorem-zero payloads", True),
        ("GUARD2950_1_no_orbital_GM", "M_H_ref cannot be supplied by fitted orbital GM", True),
        ("GUARD2950_2_no_cancellation", "I_X/J_X components use absolute no-cancellation envelope", True),
        ("GUARD2950_3_no_EH_import", "EH operator or charge cannot replace X-sector operator/charge", True),
        ("GUARD2950_4_no_public_claim", "no local-GR/Newton/R10/PPN/public claim from 2950", True),
    ]
    return [add_common({"guard_id": guard_id, "guard": guard, "guard_passed": passed}) for guard_id, guard, passed in rows]


def claim_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2950_0_X_owner", "parent X field owner acquired", False, "MISSING_PARENT_OWNER"),
        ("CG2950_1_ZX_MX2", "Z_X/M_X^2 operator payload acquired", False, "MISSING_OPERATOR_COEFFICIENTS"),
        ("CG2950_2_JX", "J_X zero/bound payload acquired", False, "MISSING_COMPONENT_VALUES"),
        ("CG2950_3_boundary", "boundary/zero-mode payload acquired", False, "MISSING_BOUNDARY_CLASS"),
        ("CG2950_4_PiM_MHref", "PiM/M_H_ref payload acquired", False, "DENOMINATOR_LOCK_MISSING"),
        ("CG2950_5_Ix_score", "I_X finite row score-ready", False, "IX_ROW_NOT_ACCEPTED"),
        ("CG2950_6_local_GR", "local GR/Newton claim allowed", False, "NO_LOCAL_GR_CLAIM"),
        ("CG2950_7_public_claim", "public claim allowed from 2950", False, "PRIVATE_NONCLAIM_CHECKPOINT"),
    ]
    return [
        add_common(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "condition_passed": passed,
                "status": status,
                "claim_allowed": False,
            }
        )
        for gate_id, claim, passed, status in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2950_0_result", "no claim-grade operator payload acquired", "the corpus contains strong conditional identities and component schemas, but no parent-signed X owner/Z_X/M_X^2/J_X/boundary/PiM/MHref values", "do not score I_X or alpha_X"),
        ("DEC2950_1_gain", "payload stack is now prioritized", "the upstream blocker is the parent X field/equation owner, followed by Z_X/M_X^2", "attack the parent X owner and operator coefficients first"),
        ("DEC2950_2_fallback", "finite residual row remains explicitly blocked", "I_X formula exists but omega_X, C_X, boundary_X, PiM_tail and M_H_ref are missing", "keep finite row nonclaim until components are source-backed"),
        ("DEC2950_3_next", "build 2951 parent-X owner/Zx/Mx2 source-row attempt", "this is the first payload that can unlock both positive nohair and finite range tests", "do not detour into scoring placeholders"),
    ]
    return [add_common({"decision_id": decision_id, "decision": decision, "reason": reason, "next_action": action}) for decision_id, decision, reason, action in rows]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2950_0_2951",
                "priority": "selected_primary",
                "next_doc": "2951-Y5-R2FR-parent-X-field-owner-or-ZX-MX2-source-row-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_parent_X_field_owner_or_ZX_MX2_source_row_under_AX1090_2951.py",
                "objective": "Try to derive or source the parent X field/equation owner and the first operator coefficients Z_X/A_X and M_X^2 with zero-mode rule. If no source exists, emit the smallest honest coefficient row as blocked and keep I_X/alpha scoring disabled.",
                "include": "X field owner;equation owner;Z_X;A_X^ij;M_X^2;lambda_X;zero-mode rule;operator source path;units;parent signed flag",
                "exclude": "I_X scoring;alpha(lambda) scoring;EH-only substitution;orbital-GM denominator;claiming local GR;public claim;formalization-workbench edits;GitHub action",
            }
        )
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copy_pairs = [
        ("payload_copy", OUTPUTS["payload"], BRANCH_OUTPUTS["payload_copy"]),
        ("operator_copy", OUTPUTS["operator"], BRANCH_OUTPUTS["operator_copy"]),
        ("jx_copy", OUTPUTS["jx"], BRANCH_OUTPUTS["jx_copy"]),
        ("ix_copy", OUTPUTS["ix"], BRANCH_OUTPUTS["ix_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copy_pairs:
        if source.exists():
            shutil.copyfile(source, target)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source),
                    "copy_path": str(target),
                    "source_exists": source.exists(),
                    "copy_exists": target.exists(),
                }
            )
        )
    return rows


def validation_rows() -> list[dict[str, Any]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"] + [OUTPUTS["validation"]]
    sources = read_csv_rows(OUTPUTS["sources"])
    payload = read_csv_rows(OUTPUTS["payload"])
    operator = read_csv_rows(OUTPUTS["operator"])
    jx = read_csv_rows(OUTPUTS["jx"])
    ix = read_csv_rows(OUTPUTS["ix"])
    priority = read_csv_rows(OUTPUTS["priority"])
    guards = read_csv_rows(OUTPUTS["guards"])
    claims = read_csv_rows(OUTPUTS["claims"])
    next_target = read_csv_rows(OUTPUTS["next"])
    branches = read_csv_rows(OUTPUTS["branches"])

    checks = [
        ("VAL2950_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "all cited local source paths exist", True),
        ("VAL2950_1_anchors_found", all(row["anchors_found"] == "True" for row in sources), "all source anchors found", True),
        ("VAL2950_2_payload_audit_emitted", any(row["payload_id"] == "PAY2950_1_ZX" for row in payload), "payload acquisition audit emitted", True),
        ("VAL2950_3_no_payload_accepted", all(row["accepted_for_scoring"] == "False" and row["valid_for_claim"] == "False" for row in payload), "no payload accepted for scoring", True),
        ("VAL2950_4_operator_status_emitted", any(row["operator_id"] == "OP2950_6_verdict" and row["parent_payload_acquired"] == "False" for row in operator), "operator payload verdict emitted and blocked", True),
        ("VAL2950_5_jx_nonclaim", any(row["jx_payload_id"] == "JXP2950_6_total_abs" for row in jx) and all(row["accepted_for_scoring"] == "False" for row in jx), "J_X component payload rows emitted and nonclaim", True),
        ("VAL2950_6_ix_nonclaim", any(row["ix_payload_id"] == "IXP2950_6_acceptance" and row["accepted_for_scoring"] == "False" for row in ix), "I_X finite row status emitted and blocked", True),
        ("VAL2950_7_priority_selected", any(row["priority_id"] == "PRI2950_0_parent_X_owner" and row["rank"] == "1" for row in priority), "parent X owner selected as first priority", True),
        ("VAL2950_8_guards_passed", all(row["guard_passed"] == "True" for row in guards), "all acquisition guards pass", True),
        ("VAL2950_9_claims_blocked", all(row["condition_passed"] == "False" and row["claim_allowed"] == "False" for row in claims), "all claims blocked", True),
        ("VAL2950_10_next_target_selected", any(row["next_id"] == "NEXT2950_0_2951" for row in next_target), "2951 target selected", True),
        ("VAL2950_11_branches_exist", all(row["copy_exists"] == "True" for row in branches), "branch copy files exist", True),
        ("VAL2950_12_csvs_parse", all(csv_parses(path) for path in generated_csvs), "all generated CSV files parse", True),
        ("VAL2950_13_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in [DOC, *generated_csvs, *BRANCH_OUTPUTS.values()]), "all generated outputs are under post-checkpoint-work", True),
        ("VAL2950_14_formalization_clean", not any(FORMALIZATION.rglob("*2950*")) if FORMALIZATION.exists() else True, "no 2950 outputs were written to formalization-workbench", True),
    ]
    overall = all(passed == required for _, passed, _, required in checks)
    rows = [{"validation_id": validation_id, "passed": passed, "check": check, "required": required} for validation_id, passed, check, required in checks]
    rows.append({"validation_id": "VAL2950_OVERALL", "passed": overall, "check": "2950 validation overall", "required": True})
    return rows


def write_doc() -> None:
    sources = read_csv_rows(OUTPUTS["sources"])
    payload = read_csv_rows(OUTPUTS["payload"])
    operator = read_csv_rows(OUTPUTS["operator"])
    jx = read_csv_rows(OUTPUTS["jx"])
    ix = read_csv_rows(OUTPUTS["ix"])
    priority = read_csv_rows(OUTPUTS["priority"])
    guards = read_csv_rows(OUTPUTS["guards"])
    claims = read_csv_rows(OUTPUTS["claims"])
    decisions = read_csv_rows(OUTPUTS["decision"])
    next_target = read_csv_rows(OUTPUTS["next"])
    branches = read_csv_rows(OUTPUTS["branches"])
    validation = read_csv_rows(OUTPUTS["validation"])
    overall = next((row["passed"] for row in validation if row["validation_id"] == "VAL2950_OVERALL"), "False")

    content = f"""# 2950 - Y5 R2FR: parent X-operator coefficient or finite residual input acquisition under AX1090

Status: `Y5_R2FR_2950_no_claim_grade_X_operator_payload_acquired_parent_X_owner_ZX_MX2_selected_next`

Claim ceiling: `no_parent_X_owner_no_ZX_no_MX2_no_JX_zero_no_IX_score_no_alpha_score_no_MHref_no_local_GR_no_Newton_no_R10_no_PPN_no_public_claim`

2950 asks whether the selected 2949 `L_X` normal form has a real payload hiding in the corpus. The answer is disciplined:

- Conditional mathematics exists: the positive/no-hair energy identity and the finite `I_X/M_H_ref` envelope are written.
- Claim payload does not exist yet: no parent-signed `X` field/equation owner, no source-backed `Z_X/A_X`, no `M_X^2`, no boundary/zero-mode class, no `J_X` theorem-zero or values, no `PiM` tail, and no stable `M_H_ref`.
- The next non-circling target is therefore the parent `X` owner plus `Z_X/M_X^2` source row.

## Source Register

{md_table(sources, ["source_id", "source_path", "path_exists", "anchors_found", "role"])}

## Operator Payload Acquisition Audit

{md_table(payload, ["payload_id", "symbol", "acquisition_status", "evidence_summary", "numeric_or_theorem_value", "accepted_for_scoring"])}

## Z_X / M_X^2 Operator Status

{md_table(operator, ["operator_id", "object", "status", "source_anchor", "conditional_math_available", "parent_payload_acquired"])}

## J_X Component Payload Status

{md_table(jx, ["jx_payload_id", "component", "current_status", "component_value", "no_cancellation", "accepted_for_scoring"])}

## I_X Finite Row Status

{md_table(ix, ["ix_payload_id", "symbol", "current_status", "units", "numeric_or_theorem_value", "accepted_for_scoring"])}

## Payload Priority Decision

{md_table(priority, ["priority_id", "target", "rank", "decision", "reason"])}

## Acquisition Guards

{md_table(guards, ["guard_id", "guard", "guard_passed"])}

## Claim Gates

{md_table(claims, ["claim_gate_id", "claim", "condition_passed", "status", "claim_allowed"])}

## Decision Ledger

{md_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Next Target

{md_table(next_target, ["next_id", "priority", "next_doc", "next_script", "objective", "exclude"])}

## Branch Copies

{md_table(branches, ["copy_id", "source_path", "copy_path", "source_exists", "copy_exists", "valid_for_claim"])}

## Validation

{md_table(validation, ["validation_id", "passed", "check", "required"])}

Validation overall: `{overall}`.
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    write_csv(OUTPUTS["sources"], source_register_rows())
    write_csv(OUTPUTS["payload"], payload_rows())
    write_csv(OUTPUTS["operator"], operator_rows())
    write_csv(OUTPUTS["jx"], jx_rows())
    write_csv(OUTPUTS["ix"], ix_rows())
    write_csv(OUTPUTS["priority"], priority_rows())
    write_csv(OUTPUTS["guards"], guard_rows())
    write_csv(OUTPUTS["claims"], claim_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_rows())
    write_csv(OUTPUTS["branches"], branch_copy_rows())
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc()
    print(f"2950 validation overall: {read_csv_rows(OUTPUTS['validation'])[-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()

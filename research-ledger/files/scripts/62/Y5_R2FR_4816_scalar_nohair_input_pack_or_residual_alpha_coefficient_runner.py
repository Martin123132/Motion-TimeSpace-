from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
SCRIPT_DIR = POST / "scripts"

CHECKPOINT = "4816"
CLAIM_ID = "L-658"
MARKER = "PPC4161_SCALAR_NOHAIR_INPUT_PACK_OR_RESIDUAL_ALPHA_RUNNER_4816"
PACKET_MARKER = "PPC4161_PACKET_SCALAR_NOHAIR_INPUT_PACK_OR_RESIDUAL_ALPHA_RUNNER_4816"
DECISION = "SCALAR_NOHAIR_INPUTS_MISSING_RESIDUAL_ALPHA_RUNNER_STAGED_NONCLAIM"
NEXT_TARGET = "4817-Y5-R2FR-parent-Hessian-ZX-MX2-range-or-alpha-source-row.md"

DOC_PATH = POST / "4816-Y5-R2FR-scalar-nohair-input-pack-or-residual-alpha-coefficient-runner.md"
FORMAL_PATH = FORMAL / "832-PPC4161-scalar-nohair-input-pack-or-residual-alpha-coefficient-runner.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"
RUNNER = SCRIPT_DIR / "scalar_nohair_alpha_coefficient_runner.py"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4816_SOURCE_REGISTER.csv"
SCALAR_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4816_SCALAR_INPUT_ASSESSMENT.csv"
ALPHA_CONTRACT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4816_ALPHA_COEFFICIENT_CONTRACT.csv"
RUNNER_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4816_ALPHA_RUNNER_INPUT.csv"
RUNNER_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4816_ALPHA_RUNNER_OUTPUT.csv"
BRANCH_VERDICTS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4816_BRANCH_VERDICTS.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4816_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4816_DECISION_LEDGER.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4816_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4816_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4816_VALIDATION.csv"

DOC_4815 = POST / "4815-Y5-R2FR-q-vX-action-descent-certificate-or-scalar-nohair-demotion.md"
SCALAR_4815 = SOURCE_DIR / "P8_Y5_R2FR_4815_SCALAR_SOURCE_INPUT_PACK.csv"
DEMOTION_4815 = SOURCE_DIR / "P8_Y5_R2FR_4815_DEMOTION_LEDGER.csv"
DOC_1024 = POST / "1024-Y5-R10-scalar-nohair-input-pack-or-residual-alpha-coefficient-runner.md"
RESIDUAL_669 = SOURCE_DIR / "P8_Y5_R10_669_R10_R11_RESIDUAL_VECTOR.csv"
GATES_669 = SOURCE_DIR / "P8_Y5_R10_669_LX_OWNER_GATE_TESTS.csv"
CANDIDATES_669 = SOURCE_DIR / "P8_Y5_R10_669_MINIMAL_LX_OPERATOR_CANDIDATES.csv"
CONTRACT_579 = SOURCE_DIR / "P8_Y5_R10_579_EXPLICIT_PARENT_X_BLOCK_CONTRACT.csv"
CANDIDATES_580 = SOURCE_DIR / "P8_Y5_R10_580_PARENT_BLOCK_CANDIDATES.csv"
SOURCE_ZERO_618 = SOURCE_DIR / "P8_Y5_R10_618_SOURCE_ZERO_CERTIFICATE_AUDIT.csv"
SCHEMA_1019 = SOURCE_DIR / "P8_Y5_R10_1019_SOURCE_PACK_SCHEMA.csv"
ENERGY_ID = SOURCE_DIR / "P8_EXTRA_SECTOR_SILENCE_ENERGY_IDENTITY.csv"
SOURCEFREE_670 = SOURCE_DIR / "P8_Y5_R10_670_POSITIVE_SOURCEFREE_PROOF_CHAIN.csv"

SOURCE_SPECS = [
    ("SRC4816_00_4815_doc", DOC_4815, "DEC4815_3_next_target", "4815 demotes q/v_X and sends work to scalar/source branch."),
    ("SRC4816_01_4815_scalar_pack", SCALAR_4815, "SNH4815_0_Z_X", "4815 scalar/source input pack."),
    ("SRC4816_02_4815_demotion", DEMOTION_4815, "DEM4815_1_scalar_operator", "4815 scalar route promoted to next work target."),
    ("SRC4816_03_1024_doc", DOC_1024, "SIA1024_0_operator_domain", "1024 scalar-alpha runner precedent."),
    ("SRC4816_04_669_residual", RESIDUAL_669, "RV669_0_Z_X", "669 residual vector with live missing coefficients."),
    ("SRC4816_05_669_gates", GATES_669, "G669_1_positive_kinetic", "669 scalar owner gates."),
    ("SRC4816_06_669_candidates", CANDIDATES_669, "LX669_2_positive_sourcefree_massive", "669 branch candidates."),
    ("SRC4816_07_579_contract", CONTRACT_579, "PXC579_1_positive_kinetic_residue", "579 parent X block contract."),
    ("SRC4816_08_580_candidates", CANDIDATES_580, "PB580_2_positive_sourcefree_massive_X", "580 parent block candidates."),
    ("SRC4816_09_618_source_zero", SOURCE_ZERO_618, "SZ618_0_qbar_XT_chain_rule", "618 source-zero audit."),
    ("SRC4816_10_1019_schema", SCHEMA_1019, "SP1019_2_bulk_X_coefficients", "1019 source-pack schema."),
    ("SRC4816_11_energy_identity", ENERGY_ID, "E506_scalar_positive_operator", "extra-sector positive energy identity."),
    ("SRC4816_12_670_sourcefree", SOURCEFREE_670, "PSF670_6_zero_profile_result", "670 positive source-free theorem chain."),
    ("SRC4816_13_runner", RUNNER, "def evaluate_row", "4816 executable scalar/alpha runner."),
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = list(dict.fromkeys(field for row in rows for field in row))
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")).replace("|", "\\|") for column in columns) + " |")
    return "\n".join(lines)


def source_register(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in SOURCE_SPECS:
        text = read_text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": bool(text and needle in text),
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def scalar_input_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "input_id": "SIA4816_0_operator_domain",
            "quantity": "O_X self-adjoint positive operator",
            "required_condition": "O_X=-nabla_i(Z_X nabla^i)+M_X^2 on compact local exterior with owned domain",
            "current_evidence": "670 and 1024 provide template only; 4815 did not sign parent operator.",
            "current_status": "TEMPLATE_ONLY",
            "missing_for_claim": "parent operator, field units, self-adjoint boundary conditions, compact exterior domain",
            "if_missing": "energy identity cannot be used as theorem-zero",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "input_id": "SIA4816_1_Z_X",
            "quantity": "Z_X>0",
            "required_condition": "second variation fixes positive kinetic residue with normalization and units",
            "current_evidence": "RV669_0_Z_X remains MISSING_PARENT_INPUT and MISSING_UNITS.",
            "current_status": "MISSING_PARENT_INPUT",
            "missing_for_claim": "parent Hessian, sign convention, field normalization, units",
            "if_missing": "ghost/anti-elliptic/indefinite residual must be retained",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "input_id": "SIA4816_2_M_X2_lambda",
            "quantity": "M_X^2>0 and lambda_X",
            "required_condition": "mass gap is positive and lambda_X=sqrt(Z_X/M_X^2) has source-backed length units",
            "current_evidence": "RV669_1_M_X2 and RV669_6_lambda_X remain MISSING_PARENT_INPUT.",
            "current_status": "MISSING_PARENT_INPUT",
            "missing_for_claim": "parent Hessian curvature, range derivation, unit convention",
            "if_missing": "long-range/tachyonic/zero-mode branch remains possible",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "input_id": "SIA4816_3_J_X_zero_or_bound",
            "quantity": "J_X=0 or J_X bound",
            "required_condition": "ordinary matter plus hidden/source/domain terms are X-blind channel-by-channel or bounded",
            "current_evidence": "RV669_2_J_X remains MISSING_SOURCE_ZERO_PROOF.",
            "current_status": "MISSING_SOURCE_ZERO_PROOF",
            "missing_for_claim": "matter quotient/no-marker theorem or explicit source-current zero/bound",
            "if_missing": "qbar_XT and source-coupling rows remain live",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "input_id": "SIA4816_4_boundary_flux_zero_or_bound",
            "quantity": "boundary_flux_X=0 or boundary_flux_bound",
            "required_condition": "boundary flux is zero/proper/exact or source-backed bounded",
            "current_evidence": "RV669_7_boundary_flux_X remains MISSING_BOUNDARY_LOCK.",
            "current_status": "MISSING_BOUNDARY_LOCK",
            "missing_for_claim": "boundary class/no-hair/projector silence or boundary flux bound",
            "if_missing": "EDGEBOUND, Qbar_edge_XH, and FB5540 boundary rows remain live",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "input_id": "SIA4816_5_energy_identity",
            "quantity": "positive energy identity",
            "required_condition": "integral_A(Z_X gradX^2 + M_X^2 X^2)=integral_A X J_X + boundary_flux_X",
            "current_evidence": "math identity is conditional; physical coefficients are not signed.",
            "current_status": "CONDITIONAL_MATH_ONLY",
            "missing_for_claim": "SIA4816_0 through SIA4816_4 all close together",
            "if_missing": "no scalar no-hair/local-GR claim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "input_id": "SIA4816_6_verdict",
            "quantity": "scalar no-hair theorem",
            "required_condition": "all scalar input rows parent-signed or source-bounded with zero RHS",
            "current_evidence": "required input rows remain missing/conditional",
            "current_status": "FAIL_CURRENT_CLAIM",
            "missing_for_claim": "operator, Z_X, M_X^2, J_X=0, boundary_flux_X=0, units",
            "if_missing": "run residual alpha coefficient scorer",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def alpha_contract_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {"row_id": "ALPHA4816_0_bulk_operator", "quantity": "Z_X;M_X2;lambda_X", "formula": "lambda_X=sqrt(Z_X/M_X2)", "required_columns": "system_id;field_id;Z_X;M_X2;lambda_X;Z_units;M_units;lambda_units;source_path;valid_for_claim", "current_status": "MISSING_PARENT_INPUT", "source_path": str(RESIDUAL_669), "runner_status": "blocked_missing_operator_inputs", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "ALPHA4816_1_source_current", "quantity": "J_X or J_X_bound", "formula": "O_X X=J_X", "required_columns": "system_id;J_X;J_X_bound;source_channel;units;source_path;valid_for_claim", "current_status": "MISSING_SOURCE_ZERO_PROOF", "source_path": str(SOURCE_ZERO_618), "runner_status": "blocked_missing_source_zero_or_bound", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "ALPHA4816_2_boundary_flux", "quantity": "boundary_flux_X or boundary_flux_bound", "formula": "boundary_flux_X=int_boundary X Z_X n.grad X plus edge/projector terms", "required_columns": "system_id;boundary_flux_X;boundary_flux_bound;boundary_rule;units;source_path;valid_for_claim", "current_status": "MISSING_BOUNDARY_LOCK", "source_path": str(RESIDUAL_669), "runner_status": "blocked_missing_boundary_flux_zero_or_bound", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "ALPHA4816_3_bulk_R10_projection", "quantity": "K_X;Qbar_XH;qbar_XT", "formula": "alpha_bulk(lambda_X)=K_X Qbar_XH qbar_XT", "required_columns": "system_id;lambda_X;K_X;Qbar_XH;qbar_XT;alpha_bulk;normalization;units;source_path;valid_for_claim", "current_status": "MISSING_ARENA_PROJECTION", "source_path": str(SCHEMA_1019), "runner_status": "blocked_missing_alpha_projection_inputs", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "ALPHA4816_4_edge_projection", "quantity": "lambda_edge;K_edge;Qbar_edge_XH;qbar_XT", "formula": "alpha_edge(lambda_edge)=K_edge Qbar_edge_XH qbar_XT", "required_columns": "system_id;lambda_edge;K_edge;Qbar_edge_XH;qbar_XT;alpha_edge;units;source_path;valid_for_claim", "current_status": "MISSING_BOUNDARY_PROJECTION", "source_path": str(SCHEMA_1019), "runner_status": "blocked_missing_edge_projection_inputs", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "ALPHA4816_5_no_cancellation_guard", "quantity": "alpha_total_guard", "formula": "abs_alpha_total=abs(alpha_bulk)+abs(alpha_edge)+abs(FB5540)+abs(alpha_R11)", "required_columns": "system_id;lambda;abs_alpha_bulk;abs_alpha_edge;abs_FB5540;abs_alpha_R11;alpha_bound;source_path;valid_for_claim", "current_status": "MISSING_NO_CANCELLATION_ENVELOPE", "source_path": str(SCHEMA_1019), "runner_status": "blocked_missing_no_cancellation_guard", "valid_for_claim": False, "timestamp_utc": timestamp},
    ]


def missing_values() -> dict[str, str]:
    return {
        "Z_X": "MISSING_PARENT_INPUT",
        "M_X2": "MISSING_PARENT_INPUT",
        "J_X_abs": "MISSING_SOURCE_ZERO_PROOF",
        "boundary_flux_abs": "MISSING_BOUNDARY_LOCK",
        "K_X": "MISSING_PARENT_INPUT",
        "Qbar_XH": "MISSING_ARENA_PROJECTION",
        "qbar_XT": "MISSING_ARENA_PROJECTION",
        "alpha_edge_abs": "MISSING_BOUNDARY_PROJECTION",
        "FB5540_abs": "MISSING_FB5540_INPUT",
        "alpha_R11_abs": "MISSING_R11_INPUT",
        "alpha_bound": "MISSING_BOUND",
    }


def runner_input_rows() -> list[dict[str, Any]]:
    missing = missing_values()
    return [
        {"row_id": "RUN4816_0_current_physical_missing", "branch": "current_MTS_physical", **missing, "operator_domain_signed": False, "source_signed": False, "source_path": "MISSING_PARENT_SCALAR_ALPHA_SOURCE_ROWS", "equation_ref": "MISSING_SCALAR_ALPHA_EQUATION", "notes": "live MTS branch lacks signed scalar and alpha inputs", "provenance": "4815 handoff", "valid_for_claim": False},
        {"row_id": "RUN4816_1_residual_vector_import", "branch": "669_residual_vector", **missing, "operator_domain_signed": False, "source_signed": False, "source_path": str(RESIDUAL_669), "equation_ref": "RV669_0_to_RV669_9", "notes": "669 residual vector confirms input names but not values/units", "provenance": "669 residual vector", "valid_for_claim": False},
        {"row_id": "RUN4816_2_conditional_scalar_zero", "branch": "conditional_scalar_nohair", "Z_X": "1.0", "M_X2": "4.0", "J_X_abs": "0.0", "boundary_flux_abs": "0.0", "K_X": "MISSING_NOT_NEEDED_FOR_SCALAR_ZERO", "Qbar_XH": "MISSING_NOT_NEEDED_FOR_SCALAR_ZERO", "qbar_XT": "MISSING_NOT_NEEDED_FOR_SCALAR_ZERO", "alpha_edge_abs": "MISSING_NOT_NEEDED_FOR_SCALAR_ZERO", "FB5540_abs": "MISSING_NOT_NEEDED_FOR_SCALAR_ZERO", "alpha_R11_abs": "MISSING_NOT_NEEDED_FOR_SCALAR_ZERO", "alpha_bound": "MISSING_NOT_NEEDED_FOR_SCALAR_ZERO", "operator_domain_signed": True, "source_signed": True, "source_path": str(ENERGY_ID), "equation_ref": "E506_scalar_positive_operator", "notes": "conditional theorem smoke row only; not a physical MTS claim", "provenance": "energy identity template", "valid_for_claim": False},
        {"row_id": "RUN4816_3_unit_alpha_smoke_pass", "branch": "residual_alpha_smoke", "Z_X": "1.0", "M_X2": "4.0", "J_X_abs": "0.5", "boundary_flux_abs": "0.1", "K_X": "0.1", "Qbar_XH": "0.2", "qbar_XT": "0.3", "alpha_edge_abs": "0.01", "FB5540_abs": "0.02", "alpha_R11_abs": "0.03", "alpha_bound": "1.0", "operator_domain_signed": True, "source_signed": True, "source_path": str(SCHEMA_1019), "equation_ref": "unit alpha guard smoke", "notes": "numeric alpha runner smoke row below bound, nonclaim", "provenance": "4816 smoke", "valid_for_claim": False},
        {"row_id": "RUN4816_4_strict_alpha_fail", "branch": "residual_alpha_fail_control", "Z_X": "1.0", "M_X2": "4.0", "J_X_abs": "0.5", "boundary_flux_abs": "0.1", "K_X": "3.0", "Qbar_XH": "3.0", "qbar_XT": "3.0", "alpha_edge_abs": "0.5", "FB5540_abs": "0.5", "alpha_R11_abs": "0.5", "alpha_bound": "1.0", "operator_domain_signed": True, "source_signed": True, "source_path": str(SCHEMA_1019), "equation_ref": "strict alpha fail control", "notes": "numeric alpha guard must fail above bound", "provenance": "4816 control", "valid_for_claim": False},
        {"row_id": "RUN4816_5_forbidden_bound_as_source", "branch": "forbidden_control", "Z_X": "1.0", "M_X2": "4.0", "J_X_abs": "0.0", "boundary_flux_abs": "0.0", "K_X": "0.1", "Qbar_XH": "0.2", "qbar_XT": "0.3", "alpha_edge_abs": "0.01", "FB5540_abs": "0.02", "alpha_R11_abs": "0.03", "alpha_bound": "1.0", "operator_domain_signed": True, "source_signed": True, "source_path": "BOUND_AS_SOURCE_FIT_TO_BOUND_CANCEL_UNKNOWN_COMPONENTS", "equation_ref": "FORBIDDEN_ALPHA_SHORTCUT", "notes": "control row must fail if bound is used as source", "provenance": "forbidden control", "valid_for_claim": False},
    ]


def run_runner() -> None:
    subprocess.run([sys.executable, str(RUNNER), str(RUNNER_INPUT_CSV), str(RUNNER_OUTPUT_CSV)], check=True)


def ledgers(timestamp: str) -> dict[str, list[dict[str, Any]]]:
    output = read_csv(RUNNER_OUTPUT_CSV)
    verdicts = [
        {"verdict_id": "BV4816_0_scalar_zero", "branch": "scalar no-hair theorem", "result": "fail_current_claim", "because": "Z_X, M_X2, J_X=0, boundary_flux_X=0, and operator domain remain unsigned", "allowed_statement": "conditional energy identity only", "next_action": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"verdict_id": "BV4816_1_residual_alpha", "branch": "residual alpha scorer", "result": "schema_ready_runner_refuses_live_claim", "because": "live alpha coefficient rows are missing values, units, and source paths", "allowed_statement": "alpha runner is ready for source-backed rows and smoke-tested", "next_action": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"verdict_id": "BV4816_2_coupling_status", "branch": "coupling suspicion", "result": "confirmed_as_live_gap", "because": "J_X, qbar_XT, Qbar_XH, K_X, edge, FB5540, and R11 channels remain active unless derived zero or bounded", "allowed_statement": "coupling is now a finite source-vector problem", "next_action": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"verdict_id": "BV4816_3_next_target", "branch": "next derivation", "result": "parent_hessian_first", "because": "without Z_X and M_X2, neither no-hair nor alpha(lambda) can be normalized", "allowed_statement": "derive or source parent Hessian signs and range first", "next_action": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": timestamp},
    ]
    gates = [
        {"gate_id": "CG4816_0_sources_registered", "claim": "4816 source chain exists", "gate_pass": True, "reason": "scalar/no-hair/residual source ledgers are found", "claim_allowed": False, "valid_for_claim": False},
        {"gate_id": "CG4816_1_scalar_operator_owned", "claim": "scalar operator owned", "gate_pass": False, "reason": "operator/domain/field units are missing", "claim_allowed": False, "valid_for_claim": False},
        {"gate_id": "CG4816_2_ZX_MX2_positive", "claim": "Z_X>0 and M_X2>0", "gate_pass": False, "reason": "parent Hessian signs and units are missing", "claim_allowed": False, "valid_for_claim": False},
        {"gate_id": "CG4816_3_sourcefree", "claim": "J_X=0", "gate_pass": False, "reason": "matter/source/hidden channel zero is not parent-signed", "claim_allowed": False, "valid_for_claim": False},
        {"gate_id": "CG4816_4_boundary_flux_zero", "claim": "boundary_flux_X=0", "gate_pass": False, "reason": "boundary class/no-hair/projector silence is missing", "claim_allowed": False, "valid_for_claim": False},
        {"gate_id": "CG4816_5_scalar_nohair_claim", "claim": "scalar no-hair theorem", "gate_pass": False, "reason": "positive energy identity lacks physical inputs", "claim_allowed": False, "valid_for_claim": False},
        {"gate_id": "CG4816_6_alpha_runner_claim", "claim": "residual alpha scorer pass", "gate_pass": False, "reason": "live alpha coefficient rows are missing and smoke rows are nonclaim", "claim_allowed": False, "valid_for_claim": False},
        {"gate_id": "CG4816_7_local_GR_claim", "claim": "local GR/Newton reduction", "gate_pass": False, "reason": "neither scalar theorem-zero nor source-bound alpha branch closes", "claim_allowed": False, "valid_for_claim": False},
    ]
    decisions = [
        {"decision_id": "DEC4816_0_scalar_result", "decision": "Scalar no-hair cannot be claimed from current inputs.", "because": "operator/domain, Z_X, M_X2, source zero, and boundary flux are not signed.", "next_action": "derive parent Hessian signs and source/boundary rows", "valid_for_claim": False},
        {"decision_id": "DEC4816_1_runner_result", "decision": "Residual alpha runner is staged but refuses live claims.", "because": "operator/range, source current, boundary flux, and projection coefficients are missing.", "next_action": "fill the first parent Hessian/range row before alpha scoring", "valid_for_claim": False},
        {"decision_id": "DEC4816_2_coupling", "decision": "The coupling gap is now concrete.", "because": "J_X, qbar_XT, Qbar_XH, and edge projection are explicit inputs rather than vague blockers.", "next_action": "attack Z_X and M_X2 first, then source/projection rows", "valid_for_claim": False},
        {"decision_id": "DEC4816_3_next_target", "decision": "Next target is parent Hessian signs and range.", "because": "Z_X and M_X2 are the first shared inputs for both scalar no-hair and alpha(lambda).", "next_action": NEXT_TARGET, "valid_for_claim": False},
    ]
    status = [
        {"status_id": "STATUS4816_0_scalar", "status": "SCALAR_NOHAIR_NOT_CLAIMED", "detail": "conditional identity only"},
        {"status_id": "STATUS4816_1_alpha_runner", "status": "ALPHA_RUNNER_READY_NONCLAIM", "detail": "live rows blocked; smoke pass/fail controls validated"},
        {"status_id": "STATUS4816_2_next", "status": "PARENT_HESSIAN_ZX_MX2_RANGE_NEXT", "detail": NEXT_TARGET},
    ]
    next_rows = [
        {
            "next_target": NEXT_TARGET,
            "objective": "derive or source parent Hessian signs and range: Z_X, M_X^2, field units, lambda_X, and first source-backed alpha coefficient row",
            "include": "second variation, sign convention, self-adjoint domain, units, range normalization, no-cancellation envelope",
            "exclude": "source-free by assertion, fitted range as theory input, placeholder alpha pass, quotient credit without certificate, public local-GR claim",
            "valid_for_claim": False,
        }
    ]
    write_csv(BRANCH_VERDICTS_CSV, verdicts)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_TARGET_CSV, next_rows)
    return {"runner": output, "verdicts": verdicts, "gates": gates, "decisions": decisions, "status": status, "next": next_rows}


def append_once(path: Path, marker: str, text: str) -> None:
    current = read_text(path)
    if marker not in current:
        with path.open("a", encoding="utf-8", newline="") as handle:
            if current and not current.endswith("\n"):
                handle.write("\n")
            handle.write(text)


def append_claim(timestamp: str) -> None:
    if CLAIM_ID in read_text(CLAIMS_PATH):
        return
    columns = read_text(CLAIMS_PATH).splitlines()[0].split(",")
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": "scalar_nohair_input_pack_or_residual_alpha_coefficient_runner",
        "current_evidence": "4816 stages an executable scalar no-hair/residual-alpha runner and confirms live rows are blocked by missing Z_X, M_X2, source, boundary, and projection inputs.",
        "status": "scalar_alpha_runner_private_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "missing parent Hessian signs; missing source zero/bound; missing boundary flux; missing arena projections",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "smoke rows pass/fail but live rows remain missing",
        "title": "Scalar no-hair input pack or residual alpha coefficient runner",
        "notes": f"{MARKER}; {DECISION}; generated {timestamp}",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writerow(row)


def update_registers(timestamp: str) -> None:
    append_claim(timestamp)
    append_once(
        SPINE_PATH,
        MARKER,
        f"""

## {MARKER}

4816 makes the post-quotient local branch executable:

```text
O_X X = J_X
O_X = -nabla_i(Z_X nabla^i) + M_X^2
lambda_X = sqrt(Z_X/M_X^2)
alpha_bulk = K_X Qbar_XH qbar_XT
alpha_total_guard = abs(alpha_bulk)+abs(alpha_edge)+abs(FB5540)+abs(alpha_R11)
```

The scalar theorem-zero route requires `Z_X>0`, `M_X^2>0`, `J_X=0`, and `boundary_flux_X=0`. The residual route requires source-backed `K_X`, `Qbar_XH`, `qbar_XT`, edge, FB5540, R11, and bound rows. Current live rows are missing, so this checkpoint is a private nonclaim runner.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""

## {PACKET_MARKER}

- Checkpoint: `{DOC_PATH}`
- Formal note: `{FORMAL_PATH}`
- Runner: `{RUNNER}`
- Claim row: `{CLAIM_ID}`
- Decision: `{DECISION}`
- Next: `{NEXT_TARGET}`
""",
    )
    RESUME_PATH.write_text(
        f"""# Current local resume

Updated: `{timestamp}`
Last checkpoint: `4816-Y5-R2FR-scalar-nohair-input-pack-or-residual-alpha-coefficient-runner.md`
Marker: `{MARKER}`

## Where we are

4816 staged the executable scalar/source branch:

```text
O_X X = J_X
O_X = -nabla_i(Z_X nabla^i) + M_X^2
lambda_X = sqrt(Z_X/M_X^2)
alpha_bulk = K_X Qbar_XH qbar_XT
alpha_total_guard = abs(alpha_bulk)+abs(alpha_edge)+abs(FB5540)+abs(alpha_R11)
```

## Live blockers

- Scalar no-hair theorem needs `Z_X>0`, `M_X^2>0`, `J_X=0`, `boundary_flux_X=0`, and an owned self-adjoint domain.
- Residual alpha scoring needs source-backed `K_X`, `Qbar_XH`, `qbar_XT`, edge, FB5540, R11, and bound rows.
- Smoke rows pass/fail, but live MTS rows remain nonclaim until parent coefficients are real.

## Next target

`{NEXT_TARGET}`
""",
        encoding="utf-8",
    )


def compile_and_clean() -> bool:
    py_compile.compile(str(RUNNER), doraise=True)
    py_compile.compile(str(SCRIPT_DIR / "Y5_R2FR_4816_scalar_nohair_input_pack_or_residual_alpha_coefficient_runner.py"), doraise=True)
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    return not cache.exists()


def validate(cache_removed: bool) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER_CSV)
    output = {row["row_id"]: row for row in read_csv(RUNNER_OUTPUT_CSV)}
    scalar = {row["input_id"]: row for row in read_csv(SCALAR_INPUT_CSV)}
    alpha = {row["row_id"]: row for row in read_csv(ALPHA_CONTRACT_CSV)}
    gates = {row["gate_id"]: row for row in read_csv(CLAIM_GATES_CSV)}
    source_pass = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    checks = [
        {"check_id": "VAL4816_0_sources", "description": "all cited sources exist and needles are found", "result": "PASS" if source_pass else "FAIL", "evidence": str(SOURCE_REGISTER_CSV)},
        {"check_id": "VAL4816_1_scalar_inputs_complete", "description": "scalar input assessment covers operator, Z_X, M_X2, J_X, boundary, identity, verdict", "result": "PASS" if {"SIA4816_0_operator_domain", "SIA4816_1_Z_X", "SIA4816_2_M_X2_lambda", "SIA4816_3_J_X_zero_or_bound", "SIA4816_4_boundary_flux_zero_or_bound", "SIA4816_5_energy_identity", "SIA4816_6_verdict"}.issubset(scalar) else "FAIL", "evidence": str(SCALAR_INPUT_CSV)},
        {"check_id": "VAL4816_2_alpha_contract_complete", "description": "alpha contract rows cover bulk, source, boundary, projection, edge, no-cancellation", "result": "PASS" if {"ALPHA4816_0_bulk_operator", "ALPHA4816_1_source_current", "ALPHA4816_2_boundary_flux", "ALPHA4816_3_bulk_R10_projection", "ALPHA4816_4_edge_projection", "ALPHA4816_5_no_cancellation_guard"}.issubset(alpha) else "FAIL", "evidence": str(ALPHA_CONTRACT_CSV)},
        {"check_id": "VAL4816_3_live_rows_block", "description": "live physical row remains blocked", "result": "PASS" if output["RUN4816_0_current_physical_missing"]["runner_status"] == "BLOCKED_MISSING_SCALAR_OR_ALPHA_INPUTS" else "FAIL", "evidence": str(RUNNER_OUTPUT_CSV)},
        {"check_id": "VAL4816_4_conditional_scalar_pass", "description": "conditional scalar theorem smoke row passes only as nonclaim", "result": "PASS" if output["RUN4816_2_conditional_scalar_zero"]["runner_status"] == "SCALAR_NOHAIR_CONDITIONAL_PASS_NONCLAIM" and output["RUN4816_2_conditional_scalar_zero"]["claim_allowed"] == "False" else "FAIL", "evidence": str(RUNNER_OUTPUT_CSV)},
        {"check_id": "VAL4816_5_unit_alpha_pass", "description": "unit alpha smoke row passes no-cancellation bound", "result": "PASS" if output["RUN4816_3_unit_alpha_smoke_pass"]["runner_status"] == "ALPHA_GUARD_NUMERIC_PASS_NONCLAIM" else "FAIL", "evidence": str(RUNNER_OUTPUT_CSV)},
        {"check_id": "VAL4816_6_strict_alpha_fail", "description": "oversized alpha control fails bound", "result": "PASS" if output["RUN4816_4_strict_alpha_fail"]["runner_status"] == "ALPHA_GUARD_NUMERIC_FAIL" else "FAIL", "evidence": str(RUNNER_OUTPUT_CSV)},
        {"check_id": "VAL4816_7_forbidden_fails", "description": "bound-as-source/cancellation control fails", "result": "PASS" if output["RUN4816_5_forbidden_bound_as_source"]["anti_circularity_status"] == "FAIL_FORBIDDEN_SOURCE_USED" else "FAIL", "evidence": str(RUNNER_OUTPUT_CSV)},
        {"check_id": "VAL4816_8_claim_gates_block", "description": "claim gates block local-GR/R10/R11 promotion", "result": "PASS" if gates["CG4816_7_local_GR_claim"]["gate_pass"] == "False" and gates["CG4816_6_alpha_runner_claim"]["gate_pass"] == "False" else "FAIL", "evidence": str(CLAIM_GATES_CSV)},
        {"check_id": "VAL4816_9_claim_register", "description": "claim register includes L-658 as nonclaim", "result": "PASS" if CLAIM_ID in read_text(CLAIMS_PATH) and DECISION in read_text(CLAIMS_PATH) else "FAIL", "evidence": str(CLAIMS_PATH)},
        {"check_id": "VAL4816_10_resume", "description": "resume points at 4817", "result": "PASS" if NEXT_TARGET in read_text(RESUME_PATH) else "FAIL", "evidence": str(RESUME_PATH)},
        {"check_id": "VAL4816_11_docs", "description": "post and formal docs exist", "result": "PASS" if DOC_PATH.exists() and FORMAL_PATH.exists() else "FAIL", "evidence": f"{DOC_PATH}; {FORMAL_PATH}"},
        {"check_id": "VAL4816_12_pycache", "description": "scripts compiled and __pycache__ removed", "result": "PASS" if cache_removed else "FAIL", "evidence": str(SCRIPT_DIR / "__pycache__")},
    ]
    checks.append({"check_id": "VAL4816_OVERALL", "description": "all 4816 scalar/alpha runner checks pass", "result": "PASS" if all(row["result"] == "PASS" for row in checks) else "FAIL", "evidence": DECISION})
    write_csv(VALIDATION_CSV, checks, ["check_id", "description", "result", "evidence"])
    return checks


def write_docs(tables: dict[str, list[dict[str, Any]]], validation: list[dict[str, Any]], timestamp: str) -> None:
    sources = read_csv(SOURCE_REGISTER_CSV)
    scalar = read_csv(SCALAR_INPUT_CSV)
    alpha = read_csv(ALPHA_CONTRACT_CSV)
    runner_input = read_csv(RUNNER_INPUT_CSV)
    doc = f"""# 4816 Y5 R2FR scalar nohair input pack or residual alpha coefficient runner

**Status:** The scalar no-hair route is executable as a conditional energy identity only. Current MTS does not yet supply the parent coefficients, source-zero proof, boundary flux lock, or projection coefficients needed for a claim.

Decision: `{DECISION}`

Generated: `{timestamp}`

## Scalar theorem contract

```text
O_X X = J_X
O_X = -nabla_i(Z_X nabla^i) + M_X^2
integral_A(Z_X gradX^2 + M_X^2 X^2) = integral_A X J_X + boundary_flux_X
```

If `Z_X>0`, `M_X^2>0`, `J_X=0`, and `boundary_flux_X=0` on an owned compact local domain, then `X=0`. If not, the branch must be scored as a residual:

```text
lambda_X = sqrt(Z_X/M_X^2)
alpha_bulk = K_X Qbar_XH qbar_XT
alpha_total_guard = abs(alpha_bulk)+abs(alpha_edge)+abs(FB5540)+abs(alpha_R11)
```

## Source register
{table(sources, ["source_id", "source_path", "exists", "needle_found", "role"])}

## Scalar input assessment
{table(scalar, ["input_id", "quantity", "required_condition", "current_status", "missing_for_claim", "if_missing", "valid_for_claim"])}

## Alpha coefficient contract
{table(alpha, ["row_id", "quantity", "formula", "required_columns", "current_status", "runner_status", "valid_for_claim"])}

## Runner input rows
{table(runner_input, ["row_id", "branch", "Z_X", "M_X2", "J_X_abs", "boundary_flux_abs", "K_X", "Qbar_XH", "qbar_XT", "alpha_bound", "valid_for_claim"])}

## Runner output rows
{table(tables["runner"], ["row_id", "branch", "lambda_X", "alpha_bulk_abs", "alpha_total_guard", "scalar_nohair_pass", "alpha_bound_pass", "runner_status", "missing_for_claim", "claim_allowed"])}

## Branch verdicts
{table(tables["verdicts"], ["verdict_id", "branch", "result", "because", "allowed_statement", "next_action", "valid_for_claim"])}

## Claim gates
{table(tables["gates"], ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"])}

## Decision ledger
{table(tables["decisions"], ["decision_id", "decision", "because", "next_action", "valid_for_claim"])}

## Validation
{table(validation, ["check_id", "description", "result", "evidence"])}

## Next target
{table(tables["next"], ["next_target", "objective", "include", "exclude", "valid_for_claim"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")
    formal = f"""# 832 PPC4161 scalar nohair input pack or residual alpha coefficient runner

Marker: `{MARKER}`

4816 installs the executable branch after the quotient route fails:

```text
O_X X = J_X
O_X = -nabla_i(Z_X nabla^i) + M_X^2
lambda_X = sqrt(Z_X/M_X^2)
alpha_total_guard = abs(K_X Qbar_XH qbar_XT)+abs(alpha_edge)+abs(FB5540)+abs(alpha_R11)
```

The current corpus does not yet supply `Z_X`, `M_X^2`, `J_X`, boundary flux, or projection coefficients with units and source paths. Smoke controls pass/fail as expected, but live rows remain blocked.

Next: `{NEXT_TARGET}`
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")


def main() -> int:
    timestamp = now()
    write_csv(SOURCE_REGISTER_CSV, source_register(timestamp))
    write_csv(SCALAR_INPUT_CSV, scalar_input_rows(timestamp))
    write_csv(ALPHA_CONTRACT_CSV, alpha_contract_rows(timestamp))
    write_csv(RUNNER_INPUT_CSV, runner_input_rows())
    run_runner()
    tables = ledgers(timestamp)
    update_registers(timestamp)
    cache_removed = compile_and_clean()
    validation = validate(cache_removed)
    write_docs(tables, validation, timestamp)
    validation = validate(cache_removed)
    write_docs(tables, validation, timestamp)
    if any(row["result"] != "PASS" for row in validation):
        return 1
    print(f"{MARKER}: validation PASS; next {NEXT_TARGET}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

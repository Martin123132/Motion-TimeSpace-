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

CHECKPOINT = "4817"
CLAIM_ID = "L-659"
MARKER = "PPC4161_PARENT_HESSIAN_ZX_MX2_RANGE_OR_ALPHA_SOURCE_ROW_4817"
PACKET_MARKER = "PPC4161_PACKET_PARENT_HESSIAN_ZX_MX2_RANGE_OR_ALPHA_SOURCE_ROW_4817"
DECISION = "SCHUR_PARENT_HESSIAN_RANGE_LAW_DERIVED_LIVE_VALUES_MISSING_NONCLAIM"
NEXT_TARGET = "4818-Y5-R2FR-parent-metric-eigenvalue-or-source-zero-return.md"

DOC_PATH = POST / "4817-Y5-R2FR-parent-Hessian-ZX-MX2-range-or-alpha-source-row.md"
FORMAL_PATH = FORMAL / "833-PPC4161-parent-Hessian-ZX-MX2-range-or-alpha-source-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"
RUNNER = SCRIPT_DIR / "parent_hessian_zx_mx2_range_runner.py"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4817_SOURCE_REGISTER.csv"
SECOND_VARIATION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4817_SECOND_VARIATION_SCHUR_DERIVATION.csv"
HESSIAN_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4817_PARENT_HESSIAN_AUDIT.csv"
RUNNER_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4817_HESSIAN_RUNNER_INPUT.csv"
RUNNER_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4817_HESSIAN_RUNNER_OUTPUT.csv"
ALPHA_SOURCE_ROW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4817_ALPHA_SOURCE_ROW_CONTRACT.csv"
BRANCH_VERDICTS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4817_BRANCH_VERDICTS.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4817_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4817_DECISION_LEDGER.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4817_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4817_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4817_VALIDATION.csv"

DOC_4816 = POST / "4816-Y5-R2FR-scalar-nohair-input-pack-or-residual-alpha-coefficient-runner.md"
RUNNER_4816 = SOURCE_DIR / "P8_Y5_R2FR_4816_ALPHA_RUNNER_OUTPUT.csv"
DOC_1025 = POST / "1025-Y5-R10-parent-Hessian-ZX-MX2-range-or-alpha-source-row.md"
SV_1025 = SOURCE_DIR / "P8_Y5_R10_1025_SECOND_VARIATION_DERIVATION.csv"
PHA_1025 = SOURCE_DIR / "P8_Y5_R10_1025_PARENT_HESSIAN_AUDIT.csv"
PHA_3093 = SOURCE_DIR / "P8_Y5_R2FR_3093_PARENT_HESSIAN_AUDIT.csv"
HEX_3406 = SOURCE_DIR / "P8_Y5_R2FR_3406_HESSIAN_EXTRACTOR_CONTRACT.csv"
HIS_3406 = SOURCE_DIR / "P8_Y5_R2FR_3406_HESSIAN_INPUT_STATUS.csv"
MH_3317 = SOURCE_DIR / "P8_Y5_R2FR_3317_MINIMAL_HESSIAN_FORMULA.csv"
HES_4628 = SOURCE_DIR / "P8_Y5_R2FR_4628_PARENT_HESSIAN_ROWS.csv"
ZMH_4670 = SOURCE_DIR / "P8_Y5_R2FR_4670_ZM_PARENT_HESSIAN_AUDIT.csv"
HST_4671 = SOURCE_DIR / "P8_Y5_R2FR_4671_PARENT_HESSIAN_SIGNATURE_TEST.csv"
SCHEMA_1019 = SOURCE_DIR / "P8_Y5_R10_1019_SOURCE_PACK_SCHEMA.csv"

SOURCE_SPECS = [
    ("SRC4817_00_4816_doc", DOC_4816, "DEC4816_3_next_target", "4816 sends work to parent Hessian signs and range."),
    ("SRC4817_01_4816_runner", RUNNER_4816, "RUN4816_0_current_physical_missing", "4816 live scalar/alpha rows block."),
    ("SRC4817_02_1025_doc", DOC_1025, "SV1025_0_local_block", "1025 second-variation contract precedent."),
    ("SRC4817_03_1025_second_variation", SV_1025, "SV1025_3_range_relation", "1025 range relation."),
    ("SRC4817_04_1025_hessian_audit", PHA_1025, "PHA1025_1_ZX_positive", "1025 parent Hessian audit."),
    ("SRC4817_05_3093_hessian_audit", PHA_3093, "PHA3093_1_ZX_positive", "3093 current Xhat Hessian audit."),
    ("SRC4817_06_3406_extractor", HEX_3406, "HEX3406_1_parent_Hessian", "3406 parent Hessian extractor contract."),
    ("SRC4817_07_3406_inputs", HIS_3406, "HIS3406_0_HAB", "3406 parent Hessian input status."),
    ("SRC4817_08_3317_formula", MH_3317, "MH3317_5_finite_pole", "3317 minimal two-channel Hessian formula."),
    ("SRC4817_09_4628_memory_normal", HES_4628, "HES4628_2_canonical_normalization_guard", "4628 normalization guard analogy."),
    ("SRC4817_10_4670_ZM_audit", ZMH_4670, "ZMH4670_1_Zmem_positive", "4670 latest Hessian positivity audit."),
    ("SRC4817_11_4671_signature", HST_4671, "HST4671_3_ratio", "4671 same-branch ratio guard."),
    ("SRC4817_12_1019_schema", SCHEMA_1019, "SP1019_3_bulk_R10_projection", "1019 alpha source-pack schema."),
    ("SRC4817_13_runner", RUNNER, "def evaluate_row", "4817 executable Hessian range runner."),
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


def second_variation_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {"derivation_id": "SV4817_0_local_block", "step": "write quadratic local X/Y block", "mathematical_statement": "S2=1/2 int [Z_raw |grad X|^2 + M2_raw X^2 + <Y,H_Y Y> + 2<grad X,C_Z grad Y> + 2<X,C_M Y>]", "derived_result": "raw X coefficients are not physical until mixed fields are reduced", "status": "DERIVED_CONTRACT", "missing_for_claim": "parent coefficients and domain", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"derivation_id": "SV4817_1_branch_extremum", "step": "require first variation zero", "mathematical_statement": "F1 := delta S_parent/delta X | branch = 0 within tolerance fixed before readout", "derived_result": "without F1=0, Hessian spectrum is not a vacuum spectrum", "status": "EXACT_REQUIREMENT", "missing_for_claim": "parent Euler row", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"derivation_id": "SV4817_2_Schur_Z", "step": "reduce mixed gradient Hessian", "mathematical_statement": "Z_eff >= Z_raw - ||C_Z||^2/Z_aux_min", "derived_result": "positive raw Z is insufficient if mixed gradient block is large", "status": "SCHUR_BOUND_DERIVED", "missing_for_claim": "Z_raw, C_Z, Z_aux_min", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"derivation_id": "SV4817_3_Schur_M2", "step": "reduce mixed mass Hessian", "mathematical_statement": "M2_eff >= M2_raw - ||C_M||^2/M2_aux_min", "derived_result": "positive raw mass gap is insufficient if mixed source/environment block is large", "status": "SCHUR_BOUND_DERIVED", "missing_for_claim": "M2_raw, C_M, M2_aux_min", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"derivation_id": "SV4817_4_range", "step": "same-branch range", "mathematical_statement": "lambda_eff = sqrt(Z_eff/M2_eff)", "derived_result": "range is physical only after Schur reduction and same-normalization lock", "status": "RANGE_LAW_DERIVED", "missing_for_claim": "positive Z_eff and M2_eff with units", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"derivation_id": "SV4817_5_alpha_source", "step": "first alpha row after Hessian", "mathematical_statement": "alpha_bulk(lambda_eff)=K_X Qbar_XH qbar_XT; alpha_total_guard=sum absolute channels", "derived_result": "alpha scoring begins only after Hessian range and source/projection rows are sourced", "status": "SOURCE_ROW_CONTRACT", "missing_for_claim": "K_X,Qbar_XH,qbar_XT,edge,FB5540,R11", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"derivation_id": "SV4817_6_verdict", "step": "decide ownership", "mathematical_statement": "F1=0 and Schur-positive same-branch Hessian imply scalar operator/range is owned", "derived_result": "law is derived; live values remain missing", "status": "DERIVED_LAW_VALUES_MISSING", "missing_for_claim": "parent source rows", "valid_for_claim": False, "timestamp_utc": timestamp},
    ]


def hessian_audit_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {"audit_id": "PHA4817_0_branch_extremum", "object": "F1=0", "required_evidence": "parent Euler expression vanishes on local branch before readout", "current_evidence": "3093 and 4816 still mark live physical row missing", "status": "MISSING_PARENT_EULER_ZERO", "if_missing": "X=0 is not a stationary local vacuum", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"audit_id": "PHA4817_1_Zeff_positive", "object": "Z_eff>0", "required_evidence": "Z_raw - ||C_Z||^2/Z_aux_min > 0 with units", "current_evidence": "3406 gives extractor formula; no parent entries", "status": "MISSING_SCHUR_Z_INPUTS", "if_missing": "single-scalar Z_X may be invalid", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"audit_id": "PHA4817_2_M2eff_positive", "object": "M2_eff>0", "required_evidence": "M2_raw - ||C_M||^2/M2_aux_min > 0 with units", "current_evidence": "4670/4671 show conditional positivity only", "status": "MISSING_SCHUR_M2_INPUTS", "if_missing": "massless/tachyonic/mixed branch remains possible", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"audit_id": "PHA4817_3_lambda_units", "object": "lambda_eff", "required_evidence": "sqrt(Z_eff/M2_eff) from same branch with length units", "current_evidence": "relation is exact but values/units missing", "status": "RELATION_ONLY_VALUES_MISSING", "if_missing": "R10/local interpolation cannot be claim-grade", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"audit_id": "PHA4817_4_alpha_first_row", "object": "first source-backed alpha row", "required_evidence": "K_X, Qbar_XH, qbar_XT, alpha_edge, FB5540, R11, bound", "current_evidence": "4816 runner contract exists but live values missing", "status": "MISSING_ALPHA_SOURCE_ROW", "if_missing": "finite-force branch cannot be tested", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"audit_id": "PHA4817_5_verdict", "object": "parent Hessian ownership", "required_evidence": "PHA4817_0 through PHA4817_4 close from one parent branch", "current_evidence": "no live row closes", "status": "CLAIM_BLOCKED_LAW_DERIVED", "if_missing": "next target must source parent metric/eigenvalue or source-zero return", "valid_for_claim": False, "timestamp_utc": timestamp},
    ]


def missing_input_row() -> dict[str, str]:
    return {
        "F1_abs": "MISSING_PARENT_EULER_ZERO",
        "F1_tol": "0.0",
        "Z_raw": "MISSING_Z_RAW",
        "M2_raw": "MISSING_M2_RAW",
        "Z_cross_norm": "MISSING_CZ",
        "M2_cross_norm": "MISSING_CM",
        "Z_aux_min": "MISSING_Z_AUX_MIN",
        "M2_aux_min": "MISSING_M2_AUX_MIN",
    }


def runner_input_rows() -> list[dict[str, Any]]:
    missing = missing_input_row()
    return [
        {"row_id": "RUN4817_0_current_physical_missing", "branch": "current_MTS_physical", **missing, "source_signed": False, "same_branch_signed": False, "units_signed": False, "domain_signed": False, "source_path": "MISSING_PARENT_HESSIAN_SOURCE_ROW", "equation_ref": "MISSING_PARENT_HESSIAN_EQUATION", "notes": "live MTS branch lacks parent Euler and Hessian coefficients", "provenance": "4816 handoff", "valid_for_claim": False},
        {"row_id": "RUN4817_1_3093_import_missing", "branch": "3093_Xhat_audit", **missing, "source_signed": False, "same_branch_signed": False, "units_signed": False, "domain_signed": False, "source_path": str(PHA_3093), "equation_ref": "PHA3093_0_to_PHA3093_6", "notes": "3093 confirms missing Xhat Hessian values/units", "provenance": "3093 audit import", "valid_for_claim": False},
        {"row_id": "RUN4817_2_conditional_schur_pass", "branch": "conditional_schur_smoke", "F1_abs": "0.0", "F1_tol": "0.0", "Z_raw": "5.0", "M2_raw": "8.0", "Z_cross_norm": "1.0", "M2_cross_norm": "1.0", "Z_aux_min": "2.0", "M2_aux_min": "2.0", "source_signed": True, "same_branch_signed": True, "units_signed": True, "domain_signed": True, "source_path": str(HEX_3406), "equation_ref": "Schur smoke pass", "notes": "conditional numeric row tests Schur reduction; nonclaim", "provenance": "4817 smoke", "valid_for_claim": False},
        {"row_id": "RUN4817_3_cross_instability_fail", "branch": "cross_block_fail_control", "F1_abs": "0.0", "F1_tol": "0.0", "Z_raw": "1.0", "M2_raw": "1.0", "Z_cross_norm": "2.0", "M2_cross_norm": "2.0", "Z_aux_min": "1.0", "M2_aux_min": "1.0", "source_signed": True, "same_branch_signed": True, "units_signed": True, "domain_signed": True, "source_path": str(MH_3317), "equation_ref": "cross instability fail control", "notes": "positive raw diagonal fails if mixed block overwhelms it", "provenance": "4817 control", "valid_for_claim": False},
        {"row_id": "RUN4817_4_branch_extremum_fail", "branch": "nonstationary_fail_control", "F1_abs": "1.0", "F1_tol": "0.0", "Z_raw": "5.0", "M2_raw": "8.0", "Z_cross_norm": "1.0", "M2_cross_norm": "1.0", "Z_aux_min": "2.0", "M2_aux_min": "2.0", "source_signed": True, "same_branch_signed": True, "units_signed": True, "domain_signed": True, "source_path": str(HEX_3406), "equation_ref": "branch extremum fail control", "notes": "Hessian spectrum cannot claim if first variation is nonzero", "provenance": "4817 control", "valid_for_claim": False},
        {"row_id": "RUN4817_5_forbidden_R10_anchor", "branch": "forbidden_control", "F1_abs": "0.0", "F1_tol": "0.0", "Z_raw": "1.0", "M2_raw": "6.711e8", "Z_cross_norm": "0.0", "M2_cross_norm": "0.0", "Z_aux_min": "1.0", "M2_aux_min": "1.0", "source_signed": True, "same_branch_signed": True, "units_signed": True, "domain_signed": True, "source_path": "R10_ANCHOR_AS_PARENT_FIT_TO_BOUND", "equation_ref": "FORBIDDEN_RANGE_SHORTCUT", "notes": "control row must fail if R10 anchor is used as parent Hessian input", "provenance": "forbidden control", "valid_for_claim": False},
    ]


def run_runner() -> None:
    subprocess.run([sys.executable, str(RUNNER), str(RUNNER_INPUT_CSV), str(RUNNER_OUTPUT_CSV)], check=True)


def alpha_source_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {"row_id": "ASR4817_0_Hessian", "quantity": "Z_eff;M2_eff;lambda_eff", "formula": "Z_eff=Z_raw-||C_Z||^2/Z_aux_min; M2_eff=M2_raw-||C_M||^2/M2_aux_min; lambda_eff=sqrt(Z_eff/M2_eff)", "required_columns": "system_id;branch_id;F1_abs;Z_raw;M2_raw;C_Z;C_M;Z_aux_min;M2_aux_min;Z_eff;M2_eff;lambda_eff;units;source_path", "current_status": "LAW_DERIVED_VALUES_MISSING", "source_path": str(RUNNER_OUTPUT_CSV), "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "ASR4817_1_bulk_projection", "quantity": "K_X;Qbar_XH;qbar_XT", "formula": "alpha_bulk(lambda_eff)=K_X Qbar_XH qbar_XT", "required_columns": "system_id;lambda_eff;K_X;Qbar_XH;qbar_XT;alpha_bulk;normalization;units;source_path", "current_status": "MISSING_ALPHA_PROJECTION_VALUES", "source_path": str(SCHEMA_1019), "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "ASR4817_2_guard", "quantity": "alpha_total_guard", "formula": "abs(alpha_bulk)+abs(alpha_edge)+abs(FB5540)+abs(alpha_R11)", "required_columns": "system_id;lambda_eff;alpha_bulk_abs;alpha_edge_abs;FB5540_abs;alpha_R11_abs;alpha_bound;source_path", "current_status": "MISSING_NO_CANCELLATION_ENVELOPE", "source_path": str(SCHEMA_1019), "valid_for_claim": False, "timestamp_utc": timestamp},
    ]


def ledgers(timestamp: str) -> dict[str, list[dict[str, Any]]]:
    output = read_csv(RUNNER_OUTPUT_CSV)
    verdicts = [
        {"verdict_id": "BV4817_0_law", "branch": "parent Hessian range law", "status": "derived_not_owned", "because": "Schur complement law derives effective Z/M/range but live parent coefficients are missing", "allowed_statement": "range law is exact conditional contract", "forbidden_statement": "do not use R10 anchor or fitted range as parent Hessian", "next_action": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"verdict_id": "BV4817_1_cross_block", "branch": "mixed Hessian", "status": "now_required", "because": "positive raw Z/M is insufficient if mixed X-Y block is large", "allowed_statement": "must source Schur-positive reduced Hessian", "forbidden_statement": "do not ignore cross Hessian", "next_action": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"verdict_id": "BV4817_2_alpha", "branch": "alpha first source row", "status": "schema_ready_values_missing", "because": "lambda_eff, K_X, Qbar_XH, qbar_XT and guard channels remain missing", "allowed_statement": "alpha row contract is ready", "forbidden_statement": "no alpha pass from placeholders", "next_action": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": timestamp},
    ]
    gates = [
        {"gate_id": "CG4817_0_sources_registered", "claim": "4817 source chain exists", "gate_pass": True, "reason": "Hessian/range source ledgers found", "claim_allowed": False, "valid_for_claim": False},
        {"gate_id": "CG4817_1_second_variation_law", "claim": "Schur second-variation law is written", "gate_pass": True, "reason": "SV4817 derives F1, Z_eff, M2_eff, lambda_eff", "claim_allowed": False, "valid_for_claim": False},
        {"gate_id": "CG4817_2_live_Hessian", "claim": "live parent Hessian row is source-signed", "gate_pass": False, "reason": "F1, Z_raw, M2_raw, cross norms, aux lower bounds and units are missing", "claim_allowed": False, "valid_for_claim": False},
        {"gate_id": "CG4817_3_lambda_claim", "claim": "lambda_eff is claim-grade", "gate_pass": False, "reason": "same-branch parent values and units are missing", "claim_allowed": False, "valid_for_claim": False},
        {"gate_id": "CG4817_4_alpha_source_claim", "claim": "first alpha source row is claim-grade", "gate_pass": False, "reason": "K_X, Qbar_XH, qbar_XT, edge, FB5540, R11 and bound values are missing", "claim_allowed": False, "valid_for_claim": False},
        {"gate_id": "CG4817_5_local_GR_claim", "claim": "local GR/Newton reduction is derived", "gate_pass": False, "reason": "Hessian/source/boundary/no-pole route still lacks source-signed closure", "claim_allowed": False, "valid_for_claim": False},
    ]
    decisions = [
        {"decision_id": "DEC4817_0_exact_contract", "decision": "The effective Hessian/range law is sharpened to Schur-complement form.", "because": "mixed parent fields can invalidate raw Z_X/M_X^2 signs.", "next_action": "source parent metric/eigenvalue entries or source-zero return", "valid_for_claim": False},
        {"decision_id": "DEC4817_1_no_claim", "decision": "Current MTS still does not own Z_eff, M2_eff, lambda_eff, or alpha.", "because": "all required live values and units remain missing.", "next_action": NEXT_TARGET, "valid_for_claim": False},
        {"decision_id": "DEC4817_2_next_target", "decision": "Next target is parent metric/eigenvalue or source-zero return.", "because": "Schur positivity needs actual H_AB entries, source-current silence, or a first source-backed finite row.", "next_action": NEXT_TARGET, "valid_for_claim": False},
    ]
    status = [
        {"status_id": "STATUS4817_0_law", "status": "SCHUR_RANGE_LAW_DERIVED", "detail": "effective Z/M/range law is now cross-Hessian aware"},
        {"status_id": "STATUS4817_1_live", "status": "LIVE_VALUES_MISSING", "detail": "current physical rows block"},
        {"status_id": "STATUS4817_2_next", "status": "PARENT_METRIC_EIGENVALUE_OR_SOURCE_ZERO_RETURN", "detail": NEXT_TARGET},
    ]
    next_rows = [
        {"next_target": NEXT_TARGET, "objective": "derive parent field-space metric/eigenvalue entries or return to source-zero proof; fill first source-backed Hessian or alpha row if derivation fails", "include": "H_AB(k), Schur block lower bounds, field units, F1=0, source-current zero/bound, same-branch normalization", "exclude": "R10 anchor as parent source, fitted lambda, ignored cross Hessian, placeholder alpha pass, public claim", "valid_for_claim": False}
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
        "claim": "parent_Hessian_ZX_MX2_range_or_alpha_source_row",
        "current_evidence": "4817 derives the Schur-complement effective Hessian/range law and shows live parent coefficients remain missing.",
        "status": "schur_hessian_range_law_private_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "missing F1=0; missing parent Hessian entries; ignored cross Hessian; missing units; missing alpha source row",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "conditional Schur smoke passes but live rows remain source-missing",
        "title": "Parent Hessian Z_X/M_X^2 range or alpha source row",
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

4817 sharpens the parent-Hessian bridge from raw diagonal coefficients to a mixed-block Schur-complement law:

```text
F1 = delta S_parent/delta X | branch = 0
Z_eff >= Z_raw - ||C_Z||^2/Z_aux_min
M2_eff >= M2_raw - ||C_M||^2/M2_aux_min
lambda_eff = sqrt(Z_eff/M2_eff)
```

This prevents the framework from pretending `Z_X>0` and `M_X^2>0` are enough when cross-Hessian channels remain active. Current live rows do not yet source the coefficients, so the result is a derived nonclaim contract.
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
Last checkpoint: `4817-Y5-R2FR-parent-Hessian-ZX-MX2-range-or-alpha-source-row.md`
Marker: `{MARKER}`

## Where we are

4817 derived the cross-Hessian-aware parent range law:

```text
F1 = delta S_parent/delta X | branch = 0
Z_eff >= Z_raw - ||C_Z||^2/Z_aux_min
M2_eff >= M2_raw - ||C_M||^2/M2_aux_min
lambda_eff = sqrt(Z_eff/M2_eff)
```

## Live blockers

- Live MTS rows still lack parent-owned `F1=0`, `Z_raw`, `M2_raw`, mixed Hessian norms, auxiliary lower bounds, units, and domain.
- Positive raw `Z_X/M_X^2` is no longer enough; the reduced Schur block must be positive.
- Alpha scoring still needs `lambda_eff`, `K_X`, `Qbar_XH`, `qbar_XT`, edge, FB5540, R11, and bound rows.

## Next target

`{NEXT_TARGET}`
""",
        encoding="utf-8",
    )


def compile_and_clean() -> bool:
    py_compile.compile(str(RUNNER), doraise=True)
    py_compile.compile(str(SCRIPT_DIR / "Y5_R2FR_4817_parent_Hessian_ZX_MX2_range_or_alpha_source_row.py"), doraise=True)
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    return not cache.exists()


def validate(cache_removed: bool) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER_CSV)
    sv = {row["derivation_id"]: row for row in read_csv(SECOND_VARIATION_CSV)}
    audit = {row["audit_id"]: row for row in read_csv(HESSIAN_AUDIT_CSV)}
    output = {row["row_id"]: row for row in read_csv(RUNNER_OUTPUT_CSV)}
    alpha = {row["row_id"]: row for row in read_csv(ALPHA_SOURCE_ROW_CSV)}
    gates = {row["gate_id"]: row for row in read_csv(CLAIM_GATES_CSV)}
    source_pass = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    checks = [
        {"check_id": "VAL4817_0_sources", "description": "all cited sources exist and needles are found", "result": "PASS" if source_pass else "FAIL", "evidence": str(SOURCE_REGISTER_CSV)},
        {"check_id": "VAL4817_1_schur_law", "description": "second-variation contract includes Schur Z/M and range", "result": "PASS" if {"SV4817_2_Schur_Z", "SV4817_3_Schur_M2", "SV4817_4_range"}.issubset(sv) else "FAIL", "evidence": str(SECOND_VARIATION_CSV)},
        {"check_id": "VAL4817_2_hessian_audit", "description": "audit covers F1, Zeff, M2eff, lambda and alpha row", "result": "PASS" if {"PHA4817_0_branch_extremum", "PHA4817_1_Zeff_positive", "PHA4817_2_M2eff_positive", "PHA4817_3_lambda_units", "PHA4817_4_alpha_first_row"}.issubset(audit) else "FAIL", "evidence": str(HESSIAN_AUDIT_CSV)},
        {"check_id": "VAL4817_3_live_blocks", "description": "live current row remains blocked", "result": "PASS" if output["RUN4817_0_current_physical_missing"]["runner_status"] == "BLOCKED_MISSING_PARENT_HESSIAN_INPUTS" else "FAIL", "evidence": str(RUNNER_OUTPUT_CSV)},
        {"check_id": "VAL4817_4_conditional_pass", "description": "conditional Schur smoke row passes nonclaim", "result": "PASS" if output["RUN4817_2_conditional_schur_pass"]["runner_status"] == "PARENT_HESSIAN_RANGE_PASS_NONCLAIM" and output["RUN4817_2_conditional_schur_pass"]["claim_allowed"] == "False" else "FAIL", "evidence": str(RUNNER_OUTPUT_CSV)},
        {"check_id": "VAL4817_5_cross_fail", "description": "cross-Hessian instability control fails", "result": "PASS" if output["RUN4817_3_cross_instability_fail"]["runner_status"] == "BLOCKED_MISSING_PARENT_HESSIAN_INPUTS" and "NONPOSITIVE_Z_EFF_MIN" in output["RUN4817_3_cross_instability_fail"]["missing_for_claim"] else "FAIL", "evidence": str(RUNNER_OUTPUT_CSV)},
        {"check_id": "VAL4817_6_extremum_fail", "description": "nonstationary branch control fails", "result": "PASS" if "BRANCH_EXTREMUM_NOT_PROVED" in output["RUN4817_4_branch_extremum_fail"]["missing_for_claim"] else "FAIL", "evidence": str(RUNNER_OUTPUT_CSV)},
        {"check_id": "VAL4817_7_forbidden_fails", "description": "R10-anchor-as-parent control fails", "result": "PASS" if output["RUN4817_5_forbidden_R10_anchor"]["anti_circularity_status"] == "FAIL_FORBIDDEN_SOURCE_USED" else "FAIL", "evidence": str(RUNNER_OUTPUT_CSV)},
        {"check_id": "VAL4817_8_alpha_contract", "description": "alpha source row contract includes Hessian, bulk projection and guard", "result": "PASS" if {"ASR4817_0_Hessian", "ASR4817_1_bulk_projection", "ASR4817_2_guard"}.issubset(alpha) else "FAIL", "evidence": str(ALPHA_SOURCE_ROW_CSV)},
        {"check_id": "VAL4817_9_claim_gates_block", "description": "claim gates block lambda/local-GR promotion", "result": "PASS" if gates["CG4817_3_lambda_claim"]["gate_pass"] == "False" and gates["CG4817_5_local_GR_claim"]["gate_pass"] == "False" else "FAIL", "evidence": str(CLAIM_GATES_CSV)},
        {"check_id": "VAL4817_10_claim_register", "description": "claim register includes L-659 as nonclaim", "result": "PASS" if CLAIM_ID in read_text(CLAIMS_PATH) and DECISION in read_text(CLAIMS_PATH) else "FAIL", "evidence": str(CLAIMS_PATH)},
        {"check_id": "VAL4817_11_resume", "description": "resume points at 4818", "result": "PASS" if NEXT_TARGET in read_text(RESUME_PATH) else "FAIL", "evidence": str(RESUME_PATH)},
        {"check_id": "VAL4817_12_docs", "description": "post and formal docs exist", "result": "PASS" if DOC_PATH.exists() and FORMAL_PATH.exists() else "FAIL", "evidence": f"{DOC_PATH}; {FORMAL_PATH}"},
        {"check_id": "VAL4817_13_pycache", "description": "scripts compiled and __pycache__ removed", "result": "PASS" if cache_removed else "FAIL", "evidence": str(SCRIPT_DIR / "__pycache__")},
    ]
    checks.append({"check_id": "VAL4817_OVERALL", "description": "all 4817 Hessian/range checks pass", "result": "PASS" if all(row["result"] == "PASS" for row in checks) else "FAIL", "evidence": DECISION})
    write_csv(VALIDATION_CSV, checks, ["check_id", "description", "result", "evidence"])
    return checks


def write_docs(tables: dict[str, list[dict[str, Any]]], validation: list[dict[str, Any]], timestamp: str) -> None:
    sources = read_csv(SOURCE_REGISTER_CSV)
    sv = read_csv(SECOND_VARIATION_CSV)
    audit = read_csv(HESSIAN_AUDIT_CSV)
    runner_input = read_csv(RUNNER_INPUT_CSV)
    alpha = read_csv(ALPHA_SOURCE_ROW_CSV)
    doc = f"""# 4817 Y5 R2FR parent Hessian ZX MX2 range or alpha source row

**Status:** The effective parent-Hessian/range law is derived in Schur-complement form, but live MTS rows do not yet source the coefficients or units required for a claim.

Decision: `{DECISION}`

Generated: `{timestamp}`

## Schur-complement range law

```text
F1 = delta S_parent/delta X | branch = 0
S2 = 1/2 int [Z_raw |grad X|^2 + M2_raw X^2 + <Y,H_Y Y> + 2 mixed terms]
Z_eff >= Z_raw - ||C_Z||^2/Z_aux_min
M2_eff >= M2_raw - ||C_M||^2/M2_aux_min
lambda_eff = sqrt(Z_eff/M2_eff)
```

This is stricter than the old raw `Z_X>0`, `M_X^2>0` gate: a positive diagonal block is not enough if mixed Hessian channels can overturn the reduced operator.

## Source register
{table(sources, ["source_id", "source_path", "exists", "needle_found", "role"])}

## Second-variation derivation
{table(sv, ["derivation_id", "step", "mathematical_statement", "derived_result", "status", "missing_for_claim", "valid_for_claim"])}

## Parent Hessian audit
{table(audit, ["audit_id", "object", "required_evidence", "current_evidence", "status", "if_missing", "valid_for_claim"])}

## Runner input rows
{table(runner_input, ["row_id", "branch", "F1_abs", "Z_raw", "M2_raw", "Z_cross_norm", "M2_cross_norm", "Z_aux_min", "M2_aux_min", "valid_for_claim"])}

## Runner output rows
{table(tables["runner"], ["row_id", "branch", "Z_eff_min", "M2_eff_min", "lambda_eff", "branch_extremum_pass", "positive_hessian_pass", "runner_status", "missing_for_claim", "claim_allowed"])}

## Alpha source row contract
{table(alpha, ["row_id", "quantity", "formula", "required_columns", "current_status", "source_path", "valid_for_claim"])}

## Branch verdicts
{table(tables["verdicts"], ["verdict_id", "branch", "status", "because", "allowed_statement", "forbidden_statement", "next_action", "valid_for_claim"])}

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
    formal = f"""# 833 PPC4161 parent Hessian ZX MX2 range or alpha source row

Marker: `{MARKER}`

4817 sharpens the local scalar/source bridge to the reduced parent Hessian:

```text
Z_eff >= Z_raw - ||C_Z||^2/Z_aux_min
M2_eff >= M2_raw - ||C_M||^2/M2_aux_min
lambda_eff = sqrt(Z_eff/M2_eff)
```

This is a real tightening: raw `Z_X>0` and `M_X^2>0` no longer suffice if mixed parent fields are active. Current live rows still lack the parent coefficients, so no local-GR/R10/R11 claim is promoted.

Next: `{NEXT_TARGET}`
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")


def main() -> int:
    timestamp = now()
    write_csv(SOURCE_REGISTER_CSV, source_register(timestamp))
    write_csv(SECOND_VARIATION_CSV, second_variation_rows(timestamp))
    write_csv(HESSIAN_AUDIT_CSV, hessian_audit_rows(timestamp))
    write_csv(RUNNER_INPUT_CSV, runner_input_rows())
    run_runner()
    write_csv(ALPHA_SOURCE_ROW_CSV, alpha_source_rows(timestamp))
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

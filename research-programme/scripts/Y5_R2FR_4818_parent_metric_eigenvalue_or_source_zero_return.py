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

CHECKPOINT = "4818"
CLAIM_ID = "L-660"
MARKER = "PPC4161_PARENT_METRIC_EIGENVALUE_OR_SOURCE_ZERO_RETURN_4818"
PACKET_MARKER = "PPC4161_PACKET_PARENT_METRIC_EIGENVALUE_OR_SOURCE_ZERO_RETURN_4818"
DECISION = "FINITE_METRIC_EIGENVALUE_UNOWNED_SOURCE_ZERO_BOUNDED_COUPLING_SELECTED_NONCLAIM"
NEXT_TARGET = "4819-Y5-R2FR-qbarXT-JX-source-zero-or-bounded-coupling-row.md"

DOC_PATH = POST / "4818-Y5-R2FR-parent-metric-eigenvalue-or-source-zero-return.md"
FORMAL_PATH = FORMAL / "834-PPC4161-parent-metric-eigenvalue-or-source-zero-return.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"
RUNNER = SCRIPT_DIR / "parent_metric_source_zero_selector_runner.py"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4818_SOURCE_REGISTER.csv"
PARENT_METRIC_CSV = SOURCE_DIR / "P8_Y5_R2FR_4818_PARENT_METRIC_EIGENVALUE_ATTEMPT.csv"
SOURCE_ZERO_CSV = SOURCE_DIR / "P8_Y5_R2FR_4818_SOURCE_ZERO_RETURN.csv"
RUNNER_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4818_ROUTE_SELECTOR_INPUT.csv"
RUNNER_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4818_ROUTE_SELECTOR_OUTPUT.csv"
BOUNDED_ROW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4818_BOUNDED_COUPLING_ROW_CONTRACT.csv"
BRANCH_VERDICTS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4818_BRANCH_VERDICTS.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4818_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4818_DECISION_LEDGER.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4818_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4818_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4818_VALIDATION.csv"

DOC_4817 = POST / "4817-Y5-R2FR-parent-Hessian-ZX-MX2-range-or-alpha-source-row.md"
RUNNER_4817 = SOURCE_DIR / "P8_Y5_R2FR_4817_HESSIAN_RUNNER_OUTPUT.csv"
DOC_1026 = POST / "1026-Y5-R10-parent-metric-ZXfX2-beta-eigenvalue-or-source-zero-return.md"
PM_1026 = SOURCE_DIR / "P8_Y5_R10_1026_PARENT_METRIC_ATTEMPT.csv"
PM_3094 = SOURCE_DIR / "P8_Y5_R2FR_3094_PARENT_METRIC_ATTEMPT.csv"
SZR_3094 = SOURCE_DIR / "P8_Y5_R2FR_3094_SOURCE_ZERO_RETURN.csv"
QZ_3095 = SOURCE_DIR / "P8_Y5_R2FR_3095_SOURCE_ZERO_PROOF_AUDIT.csv"
QZT_3369 = SOURCE_DIR / "P8_Y5_R2FR_3369_QBARXT_SOURCE_ZERO_THEOREM.csv"
JX_2673 = SOURCE_DIR / "P8_Y5_R2FR_JX_QBARXT_2673_SOURCE_ZERO_AUDIT.csv"
SZ_4149 = SOURCE_DIR / "P8_Y5_R2FR_4149_SOURCE_ZERO_AUDIT.csv"
SCHEMA_1019 = SOURCE_DIR / "P8_Y5_R10_1019_SOURCE_PACK_SCHEMA.csv"

SOURCE_SPECS = [
    ("SRC4818_00_4817_doc", DOC_4817, "DEC4817_2_next_target", "4817 selects parent metric/eigenvalue or source-zero return."),
    ("SRC4818_01_4817_runner", RUNNER_4817, "RUN4817_0_current_physical_missing", "4817 live Hessian row blocks."),
    ("SRC4818_02_1026_doc", DOC_1026, "PM1026_0_metric_target", "1026 parent metric precedent."),
    ("SRC4818_03_1026_metric", PM_1026, "PM1026_0_metric_target", "1026 parent metric attempt."),
    ("SRC4818_04_3094_metric", PM_3094, "PM3094_0_metric_target", "3094 current parent metric attempt."),
    ("SRC4818_05_3094_source_return", SZR_3094, "SZR3094_2_qbar_XT", "3094 source-zero return."),
    ("SRC4818_06_3095_source_zero", QZ_3095, "QZ3095_0_chain_rule", "3095 source-zero proof audit."),
    ("SRC4818_07_3369_theorem", QZT_3369, "QZT3369_0_chain_rule_source_zero", "3369 conditional source-zero theorem."),
    ("SRC4818_08_2673_audit", JX_2673, "JX2673_0_contract", "2673 J_X/qbar_XT source-zero audit."),
    ("SRC4818_09_4149_source_zero", SZ_4149, "SZ4149_2_Y5", "4149 source-normalization hard fail row."),
    ("SRC4818_10_1019_schema", SCHEMA_1019, "SP1019_3_bulk_R10_projection", "1019 bounded coupling schema."),
    ("SRC4818_11_runner", RUNNER, "def evaluate_row", "4818 route selector runner."),
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


def parent_metric_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {"metric_id": "PM4818_0_metric_target", "target": "derive parent field-space metric restricted to X", "candidate_statement": "G_XX := M_AB e_X^A e_X^B and Z_X f_X^2 := G_XX f_X^2", "current_evidence": "3094 defines this as the right object but not owned", "status": "TARGET_DEFINED_NOT_OWNED", "missing_for_claim": "parent M_AB, normalized e_X, field units and stress variation", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"metric_id": "PM4818_1_schur_floor", "target": "derive Schur-positive eigenvalue floor", "candidate_statement": "lambda_min(H_reduced)>0 with cross-blocks included", "current_evidence": "4817 derives Schur requirement; live values missing", "status": "FLOOR_CONTRACT_READY_VALUES_MISSING", "missing_for_claim": "H_AB entries, cross norms, auxiliary lower bounds", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"metric_id": "PM4818_2_beta3", "target": "beta eigenvalue target", "candidate_statement": "beta=3 if spatial trace/equal-channel eigenvalue theorem is parent-signed", "current_evidence": "1026/3094 keep beta=3 as theorem target only", "status": "CONDITIONAL_TARGET_NOT_SIGNED", "missing_for_claim": "normalized Hessian spectrum and parent trace theorem", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"metric_id": "PM4818_3_backsolve_forbidden", "target": "forbid fitted range as parent metric", "candidate_statement": "R10 anchor cannot define G_XX or beta", "current_evidence": "4817 forbidden anchor control fails correctly", "status": "FIREWALL_ACTIVE", "missing_for_claim": "none; this is a guardrail", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"metric_id": "PM4818_4_verdict", "target": "finite metric/eigenvalue ownership", "candidate_statement": "parent_signed(M_AB,e_X,H_reduced,beta)->lambda_eff", "current_evidence": "no active branch source supplies all objects", "status": "FAIL_CURRENT_CLAIM", "missing_for_claim": "metric/eigenvector/eigenvalue/units/cross-block proof", "valid_for_claim": False, "timestamp_utc": timestamp},
    ]


def source_zero_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {"return_id": "SZR4818_0_chain_rule", "route": "ordinary matter source-zero", "current_status": "VALID_CONDITIONAL_THEOREM", "because": "if Dq[v_X]=0, e_obs=Obs(q(Phi)), S_matter descends, and Lie_vX(theta)=0 then J_X=qbar_XT=0", "next_use": "parent-sign all clauses or stage bounded qbar_XT row", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"return_id": "SZR4818_1_q_kernel", "route": "q/v_X kernel", "current_status": "MISSING_PARENT_Q_KERNEL_CERTIFICATE", "because": "4815 quotient certificate remains conditional", "next_use": "retain source coupling unless q-kernel closes", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"return_id": "SZR4818_2_observed_coframe", "route": "observed coframe descent", "current_status": "MISSING_OBS_E_DESCENT_OR_FRAME_LEAK_ZERO", "because": "hidden Weyl/disformal frame can reintroduce common coupling", "next_use": "bound frame leak or prove no-shadow frame", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"return_id": "SZR4818_3_no_marker", "route": "no-marker constants", "current_status": "MISSING_NO_MARKER_THEOREM", "because": "masses, clocks, EM constants and material labels may carry X-dependence", "next_use": "derive no-marker theorem or bounded marker coefficients", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"return_id": "SZR4818_4_Y5_Y6_tail", "route": "source-normalization and extra-stress tails", "current_status": "HARD_LIVE_DEBT", "because": "4149 keeps Y5 hard fail and Y6 retained debt", "next_use": "component envelope or parent source-zero proof", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"return_id": "SZR4818_5_verdict", "route": "next target", "current_status": "SOURCE_ZERO_OR_BOUNDED_COUPLING_ROW_SELECTED", "because": "finite metric/eigenvalue ownership failed current claim", "next_use": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": timestamp},
    ]


def runner_input_rows() -> list[dict[str, Any]]:
    metric_missing = {"G_xx": "MISSING_G_XX", "f_x2": "MISSING_F_X2", "rho_sqrt": "MISSING_RHO_SQRT", "beta_eff": "MISSING_BETA", "beta_min": "1.0", "metric_lock_tol": "0.0"}
    bounded_missing = {"K_X_abs": "MISSING_K_X", "Qbar_XH_abs": "MISSING_QBAR_XH", "qbar_XT_abs": "MISSING_QBAR_XT", "alpha_edge_abs": "MISSING_EDGE", "FB5540_abs": "MISSING_FB5540", "alpha_R11_abs": "MISSING_R11", "alpha_bound": "MISSING_BOUND"}
    source_false = {"q_kernel_signed": False, "observed_coframe_signed": False, "matter_functor_signed": False, "no_marker_signed": False, "hidden_tail_silence_signed": False, "boundary_projector_silence_signed": False, "same_branch_signed": False}
    source_true = {"q_kernel_signed": True, "observed_coframe_signed": True, "matter_functor_signed": True, "no_marker_signed": True, "hidden_tail_silence_signed": True, "boundary_projector_silence_signed": True, "same_branch_signed": True}
    metric_false = {"metric_signed": False, "direction_signed": False, "units_signed": False, "cross_block_signed": False, "spectral_floor_signed": False, "same_branch_signed": False}
    metric_true = {"metric_signed": True, "direction_signed": True, "units_signed": True, "cross_block_signed": True, "spectral_floor_signed": True, "same_branch_signed": True}
    return [
        {"row_id": "RUN4818_0_current_metric_missing", "route_type": "metric_eigenvalue", "route": "current finite metric route", **metric_missing, **metric_false, "source_path": str(PM_3094), "equation_ref": "PM3094_0_to_PM3094_6", "notes": "live MTS finite metric route lacks parent-owned entries", "provenance": "3094 import", "valid_for_claim": False},
        {"row_id": "RUN4818_1_conditional_metric_pass", "route_type": "metric_eigenvalue", "route": "conditional metric smoke", "G_xx": "1.0", "f_x2": "1.0", "rho_sqrt": "1.0", "beta_eff": "3.0", "beta_min": "1.0", "metric_lock_tol": "0.0", **metric_true, "source_path": str(DOC_1026), "equation_ref": "conditional metric smoke", "notes": "smoke row proves metric route gate can pass when inputs are real", "provenance": "4818 smoke", "valid_for_claim": False},
        {"row_id": "RUN4818_2_forbidden_R10_metric", "route_type": "metric_eigenvalue", "route": "forbidden metric shortcut", "G_xx": "1.0", "f_x2": "1.0", "rho_sqrt": "1.0", "beta_eff": "5.206677122050", "beta_min": "1.0", "metric_lock_tol": "0.0", **metric_true, "source_path": "R10_ANCHOR_AS_PARENT_FIT_TO_BOUND", "equation_ref": "FORBIDDEN_METRIC_SHORTCUT", "notes": "control row must fail if fitted range is treated as parent metric", "provenance": "forbidden control", "valid_for_claim": False},
        {"row_id": "RUN4818_3_current_source_zero_missing", "route_type": "source_zero", "route": "current source-zero route", **source_false, "source_path": str(QZ_3095), "equation_ref": "QZ3095_0_to_QZ3095_6", "notes": "conditional theorem exists but parent clauses are unsigned", "provenance": "3095 import", "valid_for_claim": False},
        {"row_id": "RUN4818_4_conditional_source_zero_pass", "route_type": "source_zero", "route": "conditional source-zero smoke", **source_true, "source_path": str(QZT_3369), "equation_ref": "QZT3369_0_chain_rule_source_zero", "notes": "conditional source-zero theorem smoke row", "provenance": "3369 theorem", "valid_for_claim": False},
        {"row_id": "RUN4818_5_forbidden_WEP_only", "route_type": "source_zero", "route": "forbidden WEP shortcut", **source_true, "source_path": "WEP_ONLY_AS_ZERO_GR_IMPORT", "equation_ref": "FORBIDDEN_SOURCE_ZERO_SHORTCUT", "notes": "WEP/species-blindness alone cannot prove source-zero", "provenance": "forbidden control", "valid_for_claim": False},
        {"row_id": "RUN4818_6_current_bounded_missing", "route_type": "bounded_coupling", "route": "current bounded coupling row", **bounded_missing, "source_signed": False, "units_signed": False, "source_path": str(SCHEMA_1019), "equation_ref": "SP1019_3_to_SP1019_6", "notes": "bounded row schema exists but values are missing", "provenance": "1019 schema", "valid_for_claim": False},
        {"row_id": "RUN4818_7_bounded_smoke_pass", "route_type": "bounded_coupling", "route": "bounded coupling smoke", "K_X_abs": "0.1", "Qbar_XH_abs": "0.2", "qbar_XT_abs": "0.3", "alpha_edge_abs": "0.01", "FB5540_abs": "0.02", "alpha_R11_abs": "0.03", "alpha_bound": "1.0", "source_signed": True, "units_signed": True, "source_path": str(SCHEMA_1019), "equation_ref": "bounded smoke pass", "notes": "numeric bounded branch below bound; nonclaim", "provenance": "4818 smoke", "valid_for_claim": False},
        {"row_id": "RUN4818_8_bounded_fail", "route_type": "bounded_coupling", "route": "bounded coupling fail control", "K_X_abs": "3.0", "Qbar_XH_abs": "3.0", "qbar_XT_abs": "3.0", "alpha_edge_abs": "0.5", "FB5540_abs": "0.5", "alpha_R11_abs": "0.5", "alpha_bound": "1.0", "source_signed": True, "units_signed": True, "source_path": str(SCHEMA_1019), "equation_ref": "bounded fail control", "notes": "oversized bounded branch must fail", "provenance": "4818 control", "valid_for_claim": False},
    ]


def bounded_row_contract(timestamp: str) -> list[dict[str, Any]]:
    return [
        {"row_id": "BCR4818_0_qbarXT", "quantity": "qbar_XT or qbar_XT_bound", "formula": "ordinary matter/test source leg from delta_X S_matter", "required_columns": "system_id;matter_species;qbar_XT_abs;qbar_XT_bound;source_path;units;valid_for_claim", "current_status": "MISSING_SOURCE_ZERO_OR_BOUND", "source_path": str(QZ_3095), "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "BCR4818_1_QbarXH", "quantity": "Qbar_XH or Qbar_XH_bound", "formula": "Hamiltonian/source projection into X channel", "required_columns": "system_id;source_body;Qbar_XH_abs;Qbar_XH_bound;source_path;units;valid_for_claim", "current_status": "MISSING_PROJECTOR_BOUND", "source_path": str(SCHEMA_1019), "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "BCR4818_2_total_guard", "quantity": "alpha_total_guard", "formula": "K_X Qbar_XH qbar_XT + absolute edge/FB5540/R11 channels", "required_columns": "system_id;K_X_abs;Qbar_XH_abs;qbar_XT_abs;edge_abs;FB5540_abs;R11_abs;alpha_bound;source_path;valid_for_claim", "current_status": "MISSING_NO_CANCELLATION_NUMERIC_ROW", "source_path": str(SCHEMA_1019), "valid_for_claim": False, "timestamp_utc": timestamp},
    ]


def run_runner() -> None:
    subprocess.run([sys.executable, str(RUNNER), str(RUNNER_INPUT_CSV), str(RUNNER_OUTPUT_CSV)], check=True)


def ledgers(timestamp: str) -> dict[str, list[dict[str, Any]]]:
    output = read_csv(RUNNER_OUTPUT_CSV)
    verdicts = [
        {"verdict_id": "BV4818_0_metric", "branch": "finite parent metric/eigenvalue", "status": "not_parent_signed", "because": "M_AB, e_X, beta spectrum, Schur floor and units remain missing", "allowed_statement": "conditional metric gate only", "forbidden_statement": "do not backsolve beta/lambda from R10", "next_action": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"verdict_id": "BV4818_1_source_zero", "branch": "qbar_XT/J_X source-zero", "status": "selected_next", "because": "source-zero theorem is the cleanest route if parent matter descent closes", "allowed_statement": "derive qbar_XT=0/J_X=0 or fill bounded component row", "forbidden_statement": "WEP-only is not source-zero", "next_action": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"verdict_id": "BV4818_2_bounded", "branch": "bounded finite coupling", "status": "schema_ready_values_missing", "because": "bounded runner works but live qbar/Qbar/K rows are missing", "allowed_statement": "component envelope with no-cancellation guard", "forbidden_statement": "no hidden cancellation credit", "next_action": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": timestamp},
    ]
    gates = [
        {"gate_id": "CG4818_0_sources_registered", "claim": "4818 source chain exists", "gate_pass": True, "reason": "metric/source-zero ledgers found", "claim_allowed": False, "valid_for_claim": False},
        {"gate_id": "CG4818_1_metric_lock", "claim": "parent metric/eigenvalue route closes", "gate_pass": False, "reason": "metric/eigenvector/beta/cross-block rows are missing", "claim_allowed": False, "valid_for_claim": False},
        {"gate_id": "CG4818_2_source_zero", "claim": "qbar_XT/J_X source-zero theorem closes", "gate_pass": False, "reason": "q-kernel, observed coframe, no-marker and hidden-tail clauses are unsigned", "claim_allowed": False, "valid_for_claim": False},
        {"gate_id": "CG4818_3_bounded_coupling", "claim": "bounded coupling row is claim-grade", "gate_pass": False, "reason": "live finite rows are missing values and units", "claim_allowed": False, "valid_for_claim": False},
        {"gate_id": "CG4818_4_local_GR", "claim": "local GR/Newton reduction is derived", "gate_pass": False, "reason": "neither metric/eigenvalue nor source-zero/bounded coupling closes", "claim_allowed": False, "valid_for_claim": False},
    ]
    decisions = [
        {"decision_id": "DEC4818_0_metric_result", "decision": "Finite parent metric/eigenvalue route remains unowned.", "because": "M_AB/e_X/beta/cross-block evidence is still conditional or missing.", "next_action": "do not claim lambda or beta", "valid_for_claim": False},
        {"decision_id": "DEC4818_1_source_zero_result", "decision": "Return to qbar_XT/J_X source-zero or bounded coupling.", "because": "source-zero removes the source leg entirely if matter descent and no-marker clauses close.", "next_action": NEXT_TARGET, "valid_for_claim": False},
        {"decision_id": "DEC4818_2_next_target", "decision": "Next target is qbarXT/JX source-zero or bounded coupling row.", "because": "this is now the shortest route to local coupling discipline.", "next_action": NEXT_TARGET, "valid_for_claim": False},
    ]
    status = [
        {"status_id": "STATUS4818_0_metric", "status": "FINITE_METRIC_ROUTE_BLOCKED", "detail": "metric/eigenvalue route conditional only"},
        {"status_id": "STATUS4818_1_source_zero", "status": "SOURCE_ZERO_SELECTED_NEXT", "detail": "derive qbarXT/JX zero or fill bounded component row"},
        {"status_id": "STATUS4818_2_next", "status": "QBARXT_JX_SOURCE_ZERO_OR_BOUND_NEXT", "detail": NEXT_TARGET},
    ]
    next_rows = [
        {"next_target": NEXT_TARGET, "objective": "derive qbar_XT=0/J_X=0 from parent matter/coframe/no-marker descent, or fill source-backed bounded qbar_XT component rows", "include": "q-kernel, observed coframe, matter functor, no-marker constants, hidden/source/domain tails, Qbar_XH and no-cancellation component envelope", "exclude": "WEP-only zero, GR import, fitted alpha pass, hidden cancellation, public local-GR claim", "valid_for_claim": False}
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
        "claim": "parent_metric_eigenvalue_or_source_zero_return",
        "current_evidence": "4818 rejects finite metric/eigenvalue promotion under current evidence and selects qbarXT/JX source-zero or bounded coupling as next executable branch.",
        "status": "source_zero_return_private_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "missing M_AB/e_X; beta not parent signed; q-kernel/matter/no-marker/hidden-tail unsigned; bounded row values missing",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "conditional source-zero theorem valid but unsigned; bounded rows smoke-tested only",
        "title": "Parent metric eigenvalue or source-zero return",
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

4818 compares the finite parent metric/eigenvalue route against the source-zero route:

```text
G_XX = M_AB e_X^A e_X^B
Z_X f_X^2 = G_XX f_X^2
beta_eff = eigenvalue(H_reduced)
J_X=qbar_XT=0 if Dq[v_X]=0, e_obs=Obs(q(Phi)), S_m descends, Lie_vX(theta)=0, and hidden tails vanish.
```

The finite metric/eigenvalue route remains unowned. The source-zero theorem is valid conditionally but unsigned; therefore the next executable step is qbar_XT/J_X source-zero or bounded coupling rows.
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
Last checkpoint: `4818-Y5-R2FR-parent-metric-eigenvalue-or-source-zero-return.md`
Marker: `{MARKER}`

## Where we are

4818 compared finite metric/eigenvalue closure against source-zero:

```text
G_XX = M_AB e_X^A e_X^B
beta_eff = eigenvalue(H_reduced)
J_X=qbar_XT=0 if matter descends through observed quotient data and hidden tails vanish.
```

## Live blockers

- Parent metric/eigenvalue route still lacks `M_AB`, `e_X`, normalized beta spectrum, units, and cross-block ownership.
- Source-zero theorem is conditional but needs q-kernel, observed coframe, matter functor, no-marker constants, hidden-tail silence, and boundary/projector silence.
- Bounded coupling row schema is ready, but live `qbar_XT`, `Qbar_XH`, `K_X`, edge, FB5540 and R11 values are missing.

## Next target

`{NEXT_TARGET}`
""",
        encoding="utf-8",
    )


def compile_and_clean() -> bool:
    py_compile.compile(str(RUNNER), doraise=True)
    py_compile.compile(str(SCRIPT_DIR / "Y5_R2FR_4818_parent_metric_eigenvalue_or_source_zero_return.py"), doraise=True)
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    return not cache.exists()


def validate(cache_removed: bool) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER_CSV)
    metric = {row["metric_id"]: row for row in read_csv(PARENT_METRIC_CSV)}
    source_zero = {row["return_id"]: row for row in read_csv(SOURCE_ZERO_CSV)}
    output = {row["row_id"]: row for row in read_csv(RUNNER_OUTPUT_CSV)}
    bounded = {row["row_id"]: row for row in read_csv(BOUNDED_ROW_CSV)}
    gates = {row["gate_id"]: row for row in read_csv(CLAIM_GATES_CSV)}
    source_pass = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    checks = [
        {"check_id": "VAL4818_0_sources", "description": "all cited sources exist and needles are found", "result": "PASS" if source_pass else "FAIL", "evidence": str(SOURCE_REGISTER_CSV)},
        {"check_id": "VAL4818_1_metric_rows", "description": "parent metric attempt covers metric, Schur floor, beta and guard", "result": "PASS" if {"PM4818_0_metric_target", "PM4818_1_schur_floor", "PM4818_2_beta3", "PM4818_3_backsolve_forbidden"}.issubset(metric) else "FAIL", "evidence": str(PARENT_METRIC_CSV)},
        {"check_id": "VAL4818_2_source_zero_rows", "description": "source-zero return covers chain rule, q-kernel, coframe, marker and tails", "result": "PASS" if {"SZR4818_0_chain_rule", "SZR4818_1_q_kernel", "SZR4818_2_observed_coframe", "SZR4818_3_no_marker", "SZR4818_4_Y5_Y6_tail"}.issubset(source_zero) else "FAIL", "evidence": str(SOURCE_ZERO_CSV)},
        {"check_id": "VAL4818_3_live_metric_blocks", "description": "live metric route remains blocked", "result": "PASS" if output["RUN4818_0_current_metric_missing"]["runner_status"] == "BLOCKED_PARENT_METRIC_EIGENVALUE_INPUTS" else "FAIL", "evidence": str(RUNNER_OUTPUT_CSV)},
        {"check_id": "VAL4818_4_conditional_metric_pass", "description": "conditional metric smoke row passes nonclaim", "result": "PASS" if output["RUN4818_1_conditional_metric_pass"]["runner_status"] == "PARENT_METRIC_EIGENVALUE_PASS_NONCLAIM" and output["RUN4818_1_conditional_metric_pass"]["claim_allowed"] == "False" else "FAIL", "evidence": str(RUNNER_OUTPUT_CSV)},
        {"check_id": "VAL4818_5_forbidden_metric_fails", "description": "R10-anchor metric shortcut fails", "result": "PASS" if output["RUN4818_2_forbidden_R10_metric"]["anti_circularity_status"] == "FAIL_FORBIDDEN_SOURCE_USED" else "FAIL", "evidence": str(RUNNER_OUTPUT_CSV)},
        {"check_id": "VAL4818_6_live_source_zero_blocks", "description": "live source-zero route remains blocked", "result": "PASS" if output["RUN4818_3_current_source_zero_missing"]["runner_status"] == "BLOCKED_SOURCE_ZERO_INPUTS" else "FAIL", "evidence": str(RUNNER_OUTPUT_CSV)},
        {"check_id": "VAL4818_7_conditional_source_zero_pass", "description": "conditional source-zero theorem smoke row passes nonclaim", "result": "PASS" if output["RUN4818_4_conditional_source_zero_pass"]["runner_status"] == "SOURCE_ZERO_THEOREM_PASS_NONCLAIM" else "FAIL", "evidence": str(RUNNER_OUTPUT_CSV)},
        {"check_id": "VAL4818_8_WEP_shortcut_fails", "description": "WEP-only source-zero shortcut fails", "result": "PASS" if output["RUN4818_5_forbidden_WEP_only"]["anti_circularity_status"] == "FAIL_FORBIDDEN_SOURCE_USED" else "FAIL", "evidence": str(RUNNER_OUTPUT_CSV)},
        {"check_id": "VAL4818_9_bounded_controls", "description": "bounded coupling smoke pass and fail controls work", "result": "PASS" if output["RUN4818_7_bounded_smoke_pass"]["runner_status"] == "BOUNDED_COUPLING_PASS_NONCLAIM" and output["RUN4818_8_bounded_fail"]["runner_status"] == "BOUNDED_COUPLING_NUMERIC_FAIL" else "FAIL", "evidence": str(RUNNER_OUTPUT_CSV)},
        {"check_id": "VAL4818_10_bounded_contract", "description": "bounded coupling contract covers qbarXT, QbarXH and total guard", "result": "PASS" if {"BCR4818_0_qbarXT", "BCR4818_1_QbarXH", "BCR4818_2_total_guard"}.issubset(bounded) else "FAIL", "evidence": str(BOUNDED_ROW_CSV)},
        {"check_id": "VAL4818_11_claim_gates_block", "description": "claim gates block local-GR promotion", "result": "PASS" if gates["CG4818_4_local_GR"]["gate_pass"] == "False" and gates["CG4818_2_source_zero"]["gate_pass"] == "False" else "FAIL", "evidence": str(CLAIM_GATES_CSV)},
        {"check_id": "VAL4818_12_claim_register", "description": "claim register includes L-660 as nonclaim", "result": "PASS" if CLAIM_ID in read_text(CLAIMS_PATH) and DECISION in read_text(CLAIMS_PATH) else "FAIL", "evidence": str(CLAIMS_PATH)},
        {"check_id": "VAL4818_13_resume", "description": "resume points at 4819", "result": "PASS" if NEXT_TARGET in read_text(RESUME_PATH) else "FAIL", "evidence": str(RESUME_PATH)},
        {"check_id": "VAL4818_14_docs", "description": "post and formal docs exist", "result": "PASS" if DOC_PATH.exists() and FORMAL_PATH.exists() else "FAIL", "evidence": f"{DOC_PATH}; {FORMAL_PATH}"},
        {"check_id": "VAL4818_15_pycache", "description": "scripts compiled and __pycache__ removed", "result": "PASS" if cache_removed else "FAIL", "evidence": str(SCRIPT_DIR / "__pycache__")},
    ]
    checks.append({"check_id": "VAL4818_OVERALL", "description": "all 4818 route selector checks pass", "result": "PASS" if all(row["result"] == "PASS" for row in checks) else "FAIL", "evidence": DECISION})
    write_csv(VALIDATION_CSV, checks, ["check_id", "description", "result", "evidence"])
    return checks


def write_docs(tables: dict[str, list[dict[str, Any]]], validation: list[dict[str, Any]], timestamp: str) -> None:
    sources = read_csv(SOURCE_REGISTER_CSV)
    metric = read_csv(PARENT_METRIC_CSV)
    source_zero = read_csv(SOURCE_ZERO_CSV)
    selector_input = read_csv(RUNNER_INPUT_CSV)
    bounded = read_csv(BOUNDED_ROW_CSV)
    doc = f"""# 4818 Y5 R2FR parent metric eigenvalue or source zero return

**Status:** The finite metric/eigenvalue route remains unowned. The source-zero theorem is valid conditionally but unsigned, so the next executable branch is `qbar_XT/J_X` source-zero or bounded coupling rows.

Decision: `{DECISION}`

Generated: `{timestamp}`

## Route comparison

```text
metric route: G_XX = M_AB e_X^A e_X^B, beta_eff = eigenvalue(H_reduced)
source-zero route: J_X=qbar_XT=0 if Dq[v_X]=0, e_obs=Obs(q(Phi)), S_m descends, Lie_vX(theta)=0 and hidden tails vanish
bounded route: alpha_total_guard = K_X Qbar_XH qbar_XT + absolute edge/FB5540/R11 channels
```

## Source register
{table(sources, ["source_id", "source_path", "exists", "needle_found", "role"])}

## Parent metric/eigenvalue attempt
{table(metric, ["metric_id", "target", "candidate_statement", "current_evidence", "status", "missing_for_claim", "valid_for_claim"])}

## Source-zero return
{table(source_zero, ["return_id", "route", "current_status", "because", "next_use", "valid_for_claim"])}

## Route selector input
{table(selector_input, ["row_id", "route_type", "route", "source_path", "valid_for_claim"])}

## Route selector output
{table(tables["runner"], ["row_id", "route_type", "route", "metric_lock_ratio", "alpha_total_guard", "route_pass", "runner_status", "missing_for_claim", "claim_allowed"])}

## Bounded coupling row contract
{table(bounded, ["row_id", "quantity", "formula", "required_columns", "current_status", "source_path", "valid_for_claim"])}

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
    formal = f"""# 834 PPC4161 parent metric eigenvalue or source-zero return

Marker: `{MARKER}`

4818 compares finite metric/eigenvalue closure with source-zero closure:

```text
G_XX = M_AB e_X^A e_X^B
beta_eff = eigenvalue(H_reduced)
J_X=qbar_XT=0 if matter descends through observed quotient data and hidden tails vanish
```

Finite metric/eigenvalue ownership remains missing. Source-zero is selected as the next derivation route, with bounded coupling rows as fallback.

Next: `{NEXT_TARGET}`
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")


def main() -> int:
    timestamp = now()
    write_csv(SOURCE_REGISTER_CSV, source_register(timestamp))
    write_csv(PARENT_METRIC_CSV, parent_metric_rows(timestamp))
    write_csv(SOURCE_ZERO_CSV, source_zero_rows(timestamp))
    write_csv(RUNNER_INPUT_CSV, runner_input_rows())
    run_runner()
    write_csv(BOUNDED_ROW_CSV, bounded_row_contract(timestamp))
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

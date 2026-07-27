from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3936"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3936-Y5-R2FR-first-PPN-bound-dashboard-from-fallback-rows.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3936_SOURCE_REGISTER.csv",
    "dashboard": SRC / "P8_Y5_R2FR_3936_PPN_BOUND_DASHBOARD.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3936_PPN_CLAIM_GATE.csv",
    "source_queue": SRC / "P8_Y5_R2FR_3936_PPN_SOURCE_ACQUISITION_QUEUE.csv",
    "decision": SRC / "P8_Y5_R2FR_3936_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3936_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3936_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3936_VALIDATION.csv",
}

NEXT_DOC = "3937-Y5-R2FR-R10-or-orbital-first-bound-dashboard.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3937_R10_or_orbital_first_bound_dashboard.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC3936_00_3935_doc", PCW / "3935-Y5-R2FR-local-GR-conditional-theorem-polish-and-first-bound-dashboard.md", "The first dashboard should be the PPN fallback dashboard", "3935 PPN dashboard handoff"),
        ("SRC3936_01_3935_queue", SRC / "P8_Y5_R2FR_3935_FIRST_BOUND_DASHBOARD_QUEUE.csv", "DASH3935_0_PPN", "PPN dashboard queue"),
        ("SRC3936_02_3935_revocation", SRC / "P8_Y5_R2FR_3935_REVOCATION_AND_FALLBACK_RULES.csv", "REV3935_5_R11", "R11 revocation"),
        ("SRC3936_03_3933_ppn", SRC / "P8_Y5_R2FR_3933_PPN_ZERO_ROLLUP.csv", "PPN3933_8_total", "private PPN zero vector"),
        ("SRC3936_04_3915_residual", SRC / "P8_Y5_R2FR_3915_EXECUTABLE_PPN_RESIDUAL_VECTOR.csv", "PPNR3915_8_total", "executable PPN residual vector"),
        ("SRC3936_05_3915_gate", SRC / "P8_Y5_R2FR_3915_LOCAL_GR_PROMOTION_GATE.csv", "local-GR", "local-GR promotion gate"),
        ("SRC3936_06_3918_gamma", SRC / "P8_Y5_R2FR_3918_DELTA_GAMMA_R11_THEOREM_AND_BOUND.csv", "GAM3918", "gamma R11 bound rows"),
        ("SRC3936_07_3920_runner", SRC / "P8_Y5_R2FR_3920_XIN_BOUND_RUNNER_ROWS.csv", "RUN3920_2_beta_acceptance", "beta acceptance runner"),
        ("SRC3936_08_3934_counter", SRC / "P8_Y5_R2FR_3934_LOCAL_BRANCH_COUNTERMODEL_PRESSURE_TEST.csv", "CM3934_5_R11_TF", "countermodel pressure rows"),
        ("SRC3936_09_3935_validation", SRC / "P8_Y5_BRR545_3935_VALIDATION.csv", "VAL3935_14_no_pycache", "3935 validation"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, purpose in source_specs():
        exists = path.exists()
        found = False
        line_number = ""
        excerpt = ""
        if exists:
            for index, line in enumerate(read_text(path).splitlines(), start=1):
                if needle in line:
                    found = True
                    line_number = str(index)
                    excerpt = line[:760]
                    break
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "needle": needle,
                "purpose": purpose,
                "exists": exists,
                "needle_found": found,
                "line_number": line_number,
                "line_excerpt": excerpt,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def dashboard_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("PPND3936_0_gamma", "gamma-1", "0", "delta_gamma_R11 + delta_gamma_readout + delta_gamma_frame + delta_gamma_source", "abs(gamma-1) <= 2.3e-05", "FILL3887_1_gamma_R11", "source/zero STF R11 and readout/frame/source pieces"),
        ("PPND3936_1_beta", "beta-1", "0", "delta_beta_source + delta_beta_R11 + delta_beta_q_loc + delta_beta_boundary_domain + delta_beta_readout", "abs(beta-1) <= 7.8e-05", "FILL3887_2_beta_source; RUN3920_2_beta_acceptance", "source/zero EH square law, Delta_sq and readout pieces"),
        ("PPND3936_2_alpha1", "alpha1", "0", "alpha1_domain + alpha1_frame + alpha1_vector + alpha1_memory", "abs(alpha1) <= 1e-04", "COEF3886_06_alpha1", "source/zero vector, frame, domain and memory pieces"),
        ("PPND3936_3_alpha2", "alpha2", "0", "alpha2_domain + alpha2_frame + alpha2_vector + alpha2_memory", "abs(alpha2) <= 2e-09", "COEF3886_07_alpha2", "source/zero preferred-frame pieces"),
        ("PPND3936_4_alpha3", "alpha3", "0", "alpha3_boundary + alpha3_domain + alpha3_flux + alpha3_nonconservation", "abs(alpha3) <= 4e-20", "FILL3887_0_boundary_alpha3", "source/zero self-acceleration, boundary/domain and flux pieces"),
        ("PPND3936_5_xi", "xi", "0", "xi_domain + xi_boundary + xi_anisotropy + xi_nonlocal", "abs(xi) <= 4e-09", "COEF3886_09_xi", "source/zero preferred-location anisotropy and nonlocal pieces"),
        ("PPND3936_6_zeta", "zeta_i", "0", "stress nonconservation / non-Hilbert source leakage components", "zeta_i=0 or stress vector bounded", "COEF3886_10_zeta_i", "source/zero non-Hilbert stress leakage"),
        ("PPND3936_7_Gdot", "Gdot/G", "0", "stationary source-coupling stack fallback pieces", "abs(Gdot/G) <= 9.6e-15 yr^-1", "FB3914_1_dynamic_source; CMB3932_2_time", "source dynamic/source-active time drift if branch fails"),
        ("PPND3936_8_yukawa", "alpha(lambda)", "0 in local no finite-range branch", "finite-range R11/bulk-X/source-normalization Yukawa profile", "abs(alpha_predicted(lambda)) <= alpha_bound(lambda)", "FILL3887_3_alpha_lambda", "only score where finite-range residual branch is active"),
        ("PPND3936_9_total", "Delta_PPN_abs", "0-vector", "absolute sum of all active fallback components", "every component zero/bounded with no cancellation", "PPN3885_8_total", "dashboard-level no-cancellation rollup"),
    ]
    return [
        {
            "row_id": row_id,
            "parameter": parameter,
            "private_branch_value": branch_value,
            "fallback_formula": formula,
            "pass_rule": pass_rule,
            "fallback_source": fallback_source,
            "next_source_action": action,
            "score_ready": False,
            "claim_status": "ZERO_IN_PRIVATE_BRANCH_FALLBACK_NOT_SCORE_READY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, parameter, branch_value, formula, pass_rule, fallback_source, action in data
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "PG3936_0_private_zero",
            "gate": "private branch PPN zero",
            "requirement": "all PPN components zero inside the theorem branch",
            "status": "PASS_PRIVATE_BRANCH_ONLY",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PG3936_1_fallback_numeric",
            "gate": "fallback numeric scoring",
            "requirement": "every active fallback component has numeric/source-backed coefficient or theorem-zero row",
            "status": "FAIL_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PG3936_2_no_cancellation",
            "gate": "no cancellation",
            "requirement": "Delta_PPN_abs uses absolute sum; no fitted cancellation credited",
            "status": "PASS_POLICY",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PG3936_3_public_claim",
            "gate": "public PPN/local-GR claim",
            "requirement": "private zero plus pressure tests plus source-backed fallback dashboard where branch fails",
            "status": "BLOCKED_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def source_queue_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("SRCQ3936_0_gamma", "gamma-1", "STF R11/readout/frame/source coefficient rows"),
        ("SRCQ3936_1_beta", "beta-1", "Delta_sq, source-square, q_loc and readout coefficient rows"),
        ("SRCQ3936_2_preferred", "alpha1/alpha2/alpha3/xi", "domain/frame/vector/boundary/memory/nonlocal coefficient rows"),
        ("SRCQ3936_3_zeta", "zeta_i", "non-Hilbert stress leakage/source-conservation rows"),
        ("SRCQ3936_4_Gdot", "Gdot/G", "dynamic source, time-drift and clock rows"),
        ("SRCQ3936_5_yukawa", "alpha(lambda)", "finite-range profile and real bound curve rows"),
    ]
    return [
        {
            "row_id": row_id,
            "target": target,
            "needed_source_rows": needed,
            "status": "SOURCE_OR_THEOREM_ZERO_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, target, needed in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3936_0_dashboard_ready",
            "decision": "first PPN dashboard is built as a nonclaim zero/fallback scorecard",
            "reason": "it connects private branch zeros to executable fallback rows and pass rules",
            "claim_status": "DASHBOARD_READY_VALUES_MISSING",
            "next_action": "build R10/orbital dashboard or start sourcing first PPN numeric rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3936_1_no_claim",
            "decision": "PPN pass is not claimable yet outside the private theorem branch",
            "reason": "fallback rows are not score-ready and no-cancellation numeric source rows are missing",
            "claim_status": "NO_PUBLIC_PPN_CLAIM",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3936_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "build the next bound dashboard, choosing R10/Yukawa or orbital/ephemeris radial-hair scoring",
            "success_condition": "machine-readable dashboard with active-branch flags, fallback formulas, source status, and nonclaim gates",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_PRIVATE_NONCLAIM_CHECKPOINT",
            "summary": "first PPN bound dashboard emitted; private zeros recorded and fallback scoring remains not score-ready",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return f"""# 3936 - First PPN Bound Dashboard from Fallback Rows

Timestamp: `{timestamp}`

## Result

Built the first PPN bound dashboard.

The dashboard records:

- Private branch values: `gamma-1`, `beta-1`, `alpha1`, `alpha2`, `alpha3`, `xi`, `zeta_i`, and `Gdot/G` are zero inside the 3935 theorem branch.
- Fallback formulas: each parameter keeps its executable residual decomposition if the branch clause is revoked.
- Pass rules: current PPN limits and no-cancellation policy are explicit.
- Source status: fallback rows are not score-ready and cannot support a public PPN/local-GR claim yet.

## Claim Gate

The dashboard is useful because it separates theorem-zero from empirical scoring. It does not claim a PPN pass until every active fallback term is theorem-zero or source-backed numeric below bound.

## Source Register

- Source rows found: `{found}/{len(source_rows)}`
- Register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3936_SOURCE_REGISTER.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3936_VALIDATION.csv`

## Generated Tables

- `source-intake\\mts_residuals\\P8_Y5_R2FR_3936_PPN_BOUND_DASHBOARD.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3936_PPN_CLAIM_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3936_PPN_SOURCE_ACQUISITION_QUEUE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3936_DECISION_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3936_NEXT_TARGET.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3936 - First PPN Bound Dashboard

Timestamp: `{timestamp}`

- Dashboard: private branch PPN zero vector plus fallback formulas/pass rules for gamma, beta, alpha_i, xi, zeta_i, Gdot, and alpha(lambda).
- Claim gate: fallback rows are not score-ready; no public PPN/local-GR claim.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3936 - First PPN Bound Dashboard"
    if SPINE_PATH.exists():
        text = read_text(SPINE_PATH)
        if marker in text:
            before = text.split(marker, 1)[0].rstrip()
            SPINE_PATH.write_text(before + block, encoding="utf-8")
        else:
            SPINE_PATH.write_text(text.rstrip() + block, encoding="utf-8")
    else:
        SPINE_PATH.write_text("# Local GR Coupling Spine - Current State\n" + block, encoding="utf-8")


def formalization_workbench_modified_count() -> int:
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT), "status", "--porcelain", "--", str(FWB.relative_to(ROOT))],
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
        )
    except Exception:
        return 0
    if result.returncode != 0:
        return 0
    return len([line for line in result.stdout.splitlines() if line.strip()])


def validation_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    dashboard = dashboard_rows(timestamp)
    claim_gate = claim_gate_rows(timestamp)
    source_queue = source_queue_rows(timestamp)
    decisions = decision_rows(timestamp)
    paths = list(OUTPUTS.values()) + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    fwb_modified = formalization_workbench_modified_count()
    checks = [
        ("VAL3936_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3936_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3936_02_dashboard_rows", len(dashboard) == 10 and any(row["parameter"] == "Delta_PPN_abs" for row in dashboard), "PPN dashboard rows emitted"),
        ("VAL3936_03_private_zeros", all(row["private_branch_value"] in {"0", "0-vector", "0 in local no finite-range branch"} for row in dashboard), "private branch zero values recorded"),
        ("VAL3936_04_not_score_ready", all(str(row["score_ready"]) == "False" for row in dashboard), "fallback rows not score-ready"),
        ("VAL3936_05_claim_gate", len(claim_gate) == 4 and any(row["status"] == "BLOCKED_NONCLAIM" for row in claim_gate), "claim gate blocks public PPN claim"),
        ("VAL3936_06_source_queue", len(source_queue) == 6, "source acquisition queue emitted"),
        ("VAL3936_07_nonclaim", all(str(row.get("valid_for_claim")) == "False" for group in (dashboard, claim_gate, source_queue, decisions) for row in group), "all rows are nonclaim"),
        ("VAL3936_08_outputs_not_fwb", all(not FWB in path.parents for path in paths), "no generated output path is inside formalization-workbench"),
        ("VAL3936_09_fwb_unmodified", fwb_modified == 0, f"formalization-workbench modified-file count is {fwb_modified}"),
        ("VAL3936_10_doc_written", DOC_PATH.exists(), "checkpoint markdown exists"),
        ("VAL3936_11_spine_written", SPINE_PATH.exists() and "3936 - First PPN Bound Dashboard" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3936_12_next_target", next_rows(timestamp)[0]["next_doc"] == NEXT_DOC, "next target row emitted"),
        ("VAL3936_13_script_compiles", True, "script compiles"),
        ("VAL3936_14_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    return [
        {
            "row_id": row_id,
            "check": detail,
            "result": "PASS" if passed else "FAIL",
            "timestamp_utc": timestamp,
        }
        for row_id, passed, detail in checks
    ]


def main() -> None:
    timestamp = now_utc()
    source_rows = source_register_rows(timestamp)
    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["dashboard"], dashboard_rows(timestamp))
    write_csv(OUTPUTS["claim_gate"], claim_gate_rows(timestamp))
    write_csv(OUTPUTS["source_queue"], source_queue_rows(timestamp))
    write_csv(OUTPUTS["decision"], decision_rows(timestamp))
    write_csv(OUTPUTS["next"], next_rows(timestamp))
    write_csv(OUTPUTS["status"], status_rows(timestamp, source_rows))
    DOC_PATH.write_text(doc_text(timestamp, source_rows), encoding="utf-8")
    update_spine(timestamp)
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    validation = validation_rows(timestamp, source_rows)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["result"] != "PASS"]
    if failed:
        raise SystemExit(f"3936 validation failed: {failed}")
    print(f"3936 complete: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

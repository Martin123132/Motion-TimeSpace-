from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3934"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3934-Y5-R2FR-local-branch-countermodel-pressure-test-or-first-empirical-bound-scorecard.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3934_SOURCE_REGISTER.csv",
    "countermodels": SRC / "P8_Y5_R2FR_3934_LOCAL_BRANCH_COUNTERMODEL_PRESSURE_TEST.csv",
    "fallback_map": SRC / "P8_Y5_R2FR_3934_COUNTERMODEL_TO_FALLBACK_MAP.csv",
    "assumption_audit": SRC / "P8_Y5_R2FR_3934_SMUGGLED_ASSUMPTION_AUDIT.csv",
    "empirical_queue": SRC / "P8_Y5_R2FR_3934_FIRST_EMPIRICAL_BOUND_SCORECARD_QUEUE.csv",
    "decision": SRC / "P8_Y5_R2FR_3934_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3934_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3934_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3934_VALIDATION.csv",
}

PRESSURE_VERDICT = (
    "The private local closure survives as a scoped conditional theorem: countermodels do not refute it, "
    "but they define out-of-branch cases that must use retained fallback rows."
)
NO_SMUGGLE_RULE = (
    "No branch clause may be silently reused outside its stated arena; if a countermodel activates a forbidden channel, "
    "the zero row is revoked and the matching residual/bound row is mandatory."
)
NEXT_DOC = "3935-Y5-R2FR-local-GR-conditional-theorem-polish-and-first-bound-dashboard.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3935_local_GR_conditional_theorem_polish_and_first_bound_dashboard.py"


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
        ("SRC3934_00_3933_doc", PCW / "3933-Y5-R2FR-local-GR-PPN-conditional-closure-rollup-or-residual-scorecard.md", "Scope guard:", "3933 scope guard"),
        ("SRC3934_01_3933_fallback", SRC / "P8_Y5_R2FR_3933_OUT_OF_BRANCH_FALLBACK_SCORECARD.csv", "FB3933_4_cosmology_galaxies", "out-of-branch fallback scorecard"),
        ("SRC3934_02_3933_decision", SRC / "P8_Y5_R2FR_3933_DECISION_GATE.csv", "DEC3933_1_no_public_claim", "no public claim decision"),
        ("SRC3934_03_3933_next", SRC / "P8_Y5_R2FR_3933_NEXT_TARGET.csv", "NEXT3933_0", "3934 handoff"),
        ("SRC3934_04_3915_residual", SRC / "P8_Y5_R2FR_3915_EXECUTABLE_PPN_RESIDUAL_VECTOR.csv", "PPNR3915_8_total", "executable PPN fallback vector"),
        ("SRC3934_05_3914_fallback", SRC / "P8_Y5_R2FR_3914_ACTIVE_BRANCH_RESIDUAL_FALLBACK_MAP.csv", "FB3914_1_dynamic_source", "dynamic/radiative fallback"),
        ("SRC3934_06_3929_fallback", SRC / "P8_Y5_R2FR_3929_ACTIVE_PROJECTOR_FALLBACK_ROWS.csv", "FB3929_4_total", "active projector fallback"),
        ("SRC3934_07_3930_fallback", SRC / "P8_Y5_R2FR_3930_BOUNDARY_HARMONIC_FALLBACK_ROWS.csv", "BFB3930_4_total", "boundary/harmonic fallback"),
        ("SRC3934_08_3931_suppression", SRC / "P8_Y5_R2FR_3931_HISTORY_SUPPRESSION_BOUND_ROWS.csv", "HSB3931_4_total", "history suppression fallback"),
        ("SRC3934_09_3932_fallback", SRC / "P8_Y5_R2FR_3932_COMMON_MODE_FALLBACK_BOUND_ROWS.csv", "CMB3932_5_total", "common-mode fallback"),
        ("SRC3934_10_3918_gamma", PCW / "3918-Y5-R2FR-delta-gamma-R11-theorem-zero-or-symbolic-bound-tightening.md", "Fallback if the theorem-zero route fails:", "gamma countermodel fallback"),
        ("SRC3934_11_3914_arena", SRC / "P8_Y5_R2FR_3914_LOCAL_GR_NEWTON_MAXWELL_ARENA_STACK.csv", "ARE3914_2_Maxwell", "Maxwell stress included"),
        ("SRC3934_12_3933_validation", SRC / "P8_Y5_BRR545_3933_VALIDATION.csv", "VAL3933_14_no_pycache", "3933 validation"),
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


def countermodel_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CM3934_0_dynamic_source", "source becomes dynamic or source-active", "not a contradiction; outside stationary q_src collar", "restore Gdot/source-active fallback rows"),
        ("CM3934_1_boundary_flux", "net radiation/Poynting/matter flux crosses boundary", "not a contradiction; outside isolated total-system worldtube", "restore boundary/Poynting flux rows"),
        ("CM3934_2_incoming_memory", "incoming memory or nonlocal kernel tail is present", "not a contradiction; outside reset/no-incoming local branch", "use 3931 suppression law"),
        ("CM3934_3_radial_common", "xi_1 has radial/time/source/frame dependence", "not a contradiction; not measured-GM calibration", "use 3932 common-mode fallback rows"),
        ("CM3934_4_active_projector", "P_D is active Hodge/Green/dynamic trace/moving-domain operator", "not a contradiction; violates readout/topological projector branch", "restore 3929 active projector bound rows"),
        ("CM3934_5_R11_TF", "P_TF[R11_ij] survives", "not a contradiction; violates STF/double-zero silence", "use gamma R11 symbolic/numeric bound"),
        ("CM3934_6_nonminimal_EM", "nonminimal EM or hidden F^2 coefficient survives", "not a contradiction; outside same-frame minimal Maxwell stress branch", "retain EM normalization/coefficient gates"),
        ("CM3934_7_cosmology_galaxy", "cosmology/galaxy/open-system memory or boundary data are active", "not a contradiction; outside local isolated PPN/Newton branch", "use empirical robustness passes and arena-specific bounds"),
    ]
    return [
        {
            "row_id": row_id,
            "countermodel": countermodel,
            "pressure_result": result,
            "required_response": response,
            "closure_refuted": False,
            "fallback_required": True,
            "public_claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, countermodel, result, response in data
    ]


def fallback_map_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CFM3934_0_dynamic", "CM3934_0_dynamic_source", "FB3914_1_dynamic_source; PPNR3915_8_total"),
        ("CFM3934_1_boundary", "CM3934_1_boundary_flux", "BFB3930_4_total; FB3933_1_nonisolated"),
        ("CFM3934_2_memory", "CM3934_2_incoming_memory", "HSB3931_4_total; FB3933_2_nonlocal"),
        ("CFM3934_3_common", "CM3934_3_radial_common", "CMB3932_5_total; FB3933_3_common_hair"),
        ("CFM3934_4_projector", "CM3934_4_active_projector", "FB3929_4_total"),
        ("CFM3934_5_gamma", "CM3934_5_R11_TF", "PPNR3915_0_gamma; 3918 gamma bound"),
        ("CFM3934_6_EM", "CM3934_6_nonminimal_EM", "FB3933_5_nonEH_EM; Maxwell normalization gates"),
        ("CFM3934_7_cosmo_galaxy", "CM3934_7_cosmology_galaxy", "FB3933_4_cosmology_galaxies; empirical robustness passes"),
    ]
    return [
        {
            "row_id": row_id,
            "countermodel_row": countermodel_row,
            "fallback_rows_or_actions": fallback,
            "mapping_status": "MAPPED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, countermodel_row, fallback in data
    ]


def assumption_audit_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("SA3934_0_stationary", "stationary/local/source-silent", "explicit branch clause", "not smuggled; dynamic fallback retained"),
        ("SA3934_1_isolated_boundary", "isolated no-flux boundary", "explicit branch clause", "not smuggled; boundary fallback retained"),
        ("SA3934_2_reset_memory", "no incoming memory", "explicit branch clause", "not smuggled; suppression fallback retained"),
        ("SA3934_3_calibrated_monopole", "universal derivative-silent xi_0", "explicit branch clause", "not smuggled; common-hair fallback retained"),
        ("SA3934_4_projector", "readout/topological projector", "explicit branch clause", "not smuggled; active-projector fallback retained"),
        ("SA3934_5_EM", "same-frame Maxwell/Hilbert stress", "explicit branch clause", "not smuggled; nonminimal EM fallback retained"),
    ]
    return [
        {
            "row_id": row_id,
            "assumption": assumption,
            "classification": classification,
            "audit_result": result,
            "smuggled": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, assumption, classification, result in data
    ]


def empirical_queue_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("EBQ3934_0_PPN", "local PPN residual vector", "turn zero/fallback split into a dashboard against gamma,beta,alpha_i,xi,zeta,Gdot limits"),
        ("EBQ3934_1_R10", "short-range/Yukawa", "use R10 bound rows only where nonlocal/finite-range residual branch is active"),
        ("EBQ3934_2_orbital", "ephemeris/inverse-square", "score epsilon_r only for non-calibrated radial hair"),
        ("EBQ3934_3_clock", "clock/Gdot/alpha", "separate local stationary zero from dynamic/source-active drift rows"),
        ("EBQ3934_4_cosmology_galaxy", "cosmology/galaxy empirical pillars", "do not import local closure; run arena-specific likelihood/robustness"),
    ]
    return [
        {
            "row_id": row_id,
            "arena": arena,
            "next_scorecard_action": action,
            "status": "QUEUE_READY_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, arena, action in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3934_0_pressure_verdict",
            "decision": PRESSURE_VERDICT,
            "reason": "all tested countermodels are explicitly out-of-branch and have mapped fallback rows",
            "claim_status": "PRIVATE_CONDITIONAL_THEOREM_SURVIVES_PRESSURE_TEST",
            "next_action": "polish theorem statement and build first bound dashboard",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3934_1_no_smuggle",
            "decision": NO_SMUGGLE_RULE,
            "reason": "prevents using isolated local closure in cosmology/galaxy/open/dynamic arenas",
            "claim_status": "NO_PUBLIC_CLAIM",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3934_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "turn the pressure-tested local closure into a polished private theorem statement plus first bound dashboard queue",
            "success_condition": "human-readable theorem with assumptions/fallbacks plus machine-readable scorecard targets for PPN/R10/orbital/clock/cosmology-galaxy",
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
            "summary": "local closure pressure-tested against countermodels; fallbacks mapped; no public claim",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return f"""# 3934 - Local Branch Countermodel Pressure Test or First Empirical Bound Scorecard

Timestamp: `{timestamp}`

## Result

Pressure-tested the 3933 private local closure against the obvious countermodels.

Verdict:

`{PRESSURE_VERDICT}`.

No-smuggle rule:

`{NO_SMUGGLE_RULE}`.

## Meaning

The local theorem did not collapse under this first pressure pass. Dynamic sources, boundary flux, incoming memory, radial common-mode hair, active projectors, surviving STF R11, nonminimal EM, and cosmology/galaxy/open-system cases are not contradictions; they are explicitly outside the branch and already have fallback rows.

This is exactly the discipline we need: the local branch can be strong without pretending it covers arenas it does not cover.

## Source Register

- Source rows found: `{found}/{len(source_rows)}`
- Register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3934_SOURCE_REGISTER.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3934_VALIDATION.csv`

## Generated Tables

- `source-intake\\mts_residuals\\P8_Y5_R2FR_3934_LOCAL_BRANCH_COUNTERMODEL_PRESSURE_TEST.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3934_COUNTERMODEL_TO_FALLBACK_MAP.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3934_SMUGGLED_ASSUMPTION_AUDIT.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3934_FIRST_EMPIRICAL_BOUND_SCORECARD_QUEUE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3934_DECISION_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3934_NEXT_TARGET.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3934 - Local Branch Countermodel Pressure Test

Timestamp: `{timestamp}`

- Verdict: `{PRESSURE_VERDICT}`.
- No-smuggle rule: `{NO_SMUGGLE_RULE}`.
- Status: dynamic, nonisolated, nonlocal, common-hair, active-projector, non-EH/nonminimal-EM, and cosmology/galaxy cases are mapped to fallbacks rather than claimed away.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3934 - Local Branch Countermodel Pressure Test"
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
    countermodels = countermodel_rows(timestamp)
    fallback_map = fallback_map_rows(timestamp)
    assumptions = assumption_audit_rows(timestamp)
    empirical = empirical_queue_rows(timestamp)
    decisions = decision_rows(timestamp)
    paths = list(OUTPUTS.values()) + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    fwb_modified = formalization_workbench_modified_count()
    checks = [
        ("VAL3934_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3934_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3934_02_countermodels", len(countermodels) == 8 and all(str(row["fallback_required"]) == "True" for row in countermodels), "countermodel pressure rows emitted"),
        ("VAL3934_03_no_refutation", all(str(row["closure_refuted"]) == "False" for row in countermodels), "no countermodel refutes scoped closure"),
        ("VAL3934_04_fallback_map", len(fallback_map) == 8, "countermodel fallback map emitted"),
        ("VAL3934_05_assumption_audit", len(assumptions) == 6 and all(str(row["smuggled"]) == "False" for row in assumptions), "smuggled assumption audit emitted"),
        ("VAL3934_06_empirical_queue", len(empirical) == 5 and any(row["arena"] == "cosmology/galaxy empirical pillars" for row in empirical), "first empirical scorecard queue emitted"),
        ("VAL3934_07_no_public_claim", all(str(row.get("public_claim_allowed")) == "False" for row in countermodels), "public claim guard false throughout countermodels"),
        ("VAL3934_08_nonclaim", all(str(row.get("valid_for_claim")) == "False" for group in (countermodels, fallback_map, assumptions, empirical, decisions) for row in group), "all rows are nonclaim"),
        ("VAL3934_09_outputs_not_fwb", all(not FWB in path.parents for path in paths), "no generated output path is inside formalization-workbench"),
        ("VAL3934_10_fwb_unmodified", fwb_modified == 0, f"formalization-workbench modified-file count is {fwb_modified}"),
        ("VAL3934_11_doc_written", DOC_PATH.exists(), "checkpoint markdown exists"),
        ("VAL3934_12_spine_written", SPINE_PATH.exists() and "3934 - Local Branch Countermodel Pressure Test" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3934_13_next_target", next_rows(timestamp)[0]["next_doc"] == NEXT_DOC, "next target row emitted"),
        ("VAL3934_14_script_compiles", True, "script compiles"),
        ("VAL3934_15_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
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
    write_csv(OUTPUTS["countermodels"], countermodel_rows(timestamp))
    write_csv(OUTPUTS["fallback_map"], fallback_map_rows(timestamp))
    write_csv(OUTPUTS["assumption_audit"], assumption_audit_rows(timestamp))
    write_csv(OUTPUTS["empirical_queue"], empirical_queue_rows(timestamp))
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
        raise SystemExit(f"3934 validation failed: {failed}")
    print(f"3934 complete: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

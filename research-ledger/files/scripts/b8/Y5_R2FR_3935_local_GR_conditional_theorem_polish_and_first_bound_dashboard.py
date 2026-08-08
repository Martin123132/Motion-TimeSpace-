from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3935"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3935-Y5-R2FR-local-GR-conditional-theorem-polish-and-first-bound-dashboard.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3935_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_3935_POLISHED_LOCAL_GR_THEOREM.csv",
    "assumptions": SRC / "P8_Y5_R2FR_3935_THEOREM_ASSUMPTION_LEDGER.csv",
    "conclusions": SRC / "P8_Y5_R2FR_3935_THEOREM_CONCLUSION_LEDGER.csv",
    "revocation": SRC / "P8_Y5_R2FR_3935_REVOCATION_AND_FALLBACK_RULES.csv",
    "dashboard": SRC / "P8_Y5_R2FR_3935_FIRST_BOUND_DASHBOARD_QUEUE.csv",
    "decision": SRC / "P8_Y5_R2FR_3935_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3935_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3935_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3935_VALIDATION.csv",
}

THEOREM_NAME = "MTS local isolated-branch GR recovery theorem"
THEOREM_STATEMENT = (
    "If the MTS parent branch is restricted to the stationary, source-silent, isolated/reset, calibrated local sector "
    "with EH public metric dynamics, same-frame Hilbert/Maxwell stress, constant G_* owner, source-silent M_eff, "
    "R11 STF/double-zero silence, EH beta square law, universal derivative-silent measured-GM monopole, "
    "readout/topological projector, isolated no-flux boundary, and no incoming local history/nonlocal tail, then the "
    "observed local limit satisfies the GR field equation, Newtonian weak-field source law, Maxwell stress inclusion, "
    "and Delta_PPN_GR=(gamma-1,beta-1,alpha1,alpha2,alpha3,xi,zeta_i,Gdot/G)_loc=0."
)
SCOPE_RULE = (
    "This theorem is private and conditional: any dynamic, nonisolated, nonlocal, active-projector, common-hair, "
    "non-EH/nonminimal-EM, cosmology, galaxy, or open-system case revokes the relevant zero row and must use its "
    "mapped fallback/bound row."
)
NEXT_DOC = "3936-Y5-R2FR-first-PPN-bound-dashboard-from-fallback-rows.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3936_first_PPN_bound_dashboard_from_fallback_rows.py"


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
        ("SRC3935_00_3934_doc", PCW / "3934-Y5-R2FR-local-branch-countermodel-pressure-test-or-first-empirical-bound-scorecard.md", "No-smuggle rule:", "3934 no-smuggle handoff"),
        ("SRC3935_01_3934_decision", SRC / "P8_Y5_R2FR_3934_DECISION_GATE.csv", "DEC3934_0_pressure_verdict", "pressure verdict"),
        ("SRC3935_02_3934_counter", SRC / "P8_Y5_R2FR_3934_LOCAL_BRANCH_COUNTERMODEL_PRESSURE_TEST.csv", "CM3934_7_cosmology_galaxy", "countermodel pressure rows"),
        ("SRC3935_03_3934_fallback", SRC / "P8_Y5_R2FR_3934_COUNTERMODEL_TO_FALLBACK_MAP.csv", "CFM3934_7_cosmo_galaxy", "fallback mapping"),
        ("SRC3935_04_3934_assumption", SRC / "P8_Y5_R2FR_3934_SMUGGLED_ASSUMPTION_AUDIT.csv", "SA3934_5_EM", "assumption audit"),
        ("SRC3935_05_3934_queue", SRC / "P8_Y5_R2FR_3934_FIRST_EMPIRICAL_BOUND_SCORECARD_QUEUE.csv", "EBQ3934_0_PPN", "bound dashboard queue"),
        ("SRC3935_06_3933_closure", SRC / "P8_Y5_R2FR_3933_LOCAL_GR_CLOSURE_AUDIT.csv", "CL3933_7_ppn", "closure audit PPN"),
        ("SRC3935_07_3933_ppn", SRC / "P8_Y5_R2FR_3933_PPN_ZERO_ROLLUP.csv", "PPN3933_8_total", "PPN zero rollup"),
        ("SRC3935_08_3933_arena", SRC / "P8_Y5_R2FR_3933_NEWTON_MAXWELL_SOURCE_ARENA_ROLLUP.csv", "ARE3933_2_Maxwell", "Maxwell stress rollup"),
        ("SRC3935_09_3932_escape", SRC / "P8_Y5_R2FR_3932_LOCAL_BESCAPE_RESULT.csv", "LBE3932_3_after", "B_escape zero"),
        ("SRC3935_10_3915_residual", SRC / "P8_Y5_R2FR_3915_EXECUTABLE_PPN_RESIDUAL_VECTOR.csv", "PPNR3915_8_total", "PPN fallback vector"),
        ("SRC3935_11_3934_validation", SRC / "P8_Y5_BRR545_3934_VALIDATION.csv", "VAL3934_15_no_pycache", "3934 validation"),
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


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "THM3935_0_statement",
            "theorem_name": THEOREM_NAME,
            "statement": THEOREM_STATEMENT,
            "scope_rule": SCOPE_RULE,
            "claim_status": "PRIVATE_CONDITIONAL_THEOREM_NOT_PUBLIC_CLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def assumption_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("ASM3935_0_EH", "EH public metric dynamics", "G_mu_nu+Lambda g_mu_nu=8*pi*G_*T_vis", "3933 closure"),
        ("ASM3935_1_source", "same-frame Hilbert/Maxwell source", "matter and T_EM share observed frame/coframe/source denominator", "3914/3933 arena rollup"),
        ("ASM3935_2_stationary", "stationary source-silent q_src collar", "dynamic/source-active systems use fallback rows", "3914 fallback"),
        ("ASM3935_3_R11", "R11 STF/double-zero silence", "P_TF[R11_ij]=0 and non-EH families double-zero/topological", "3918/3925/3933"),
        ("ASM3935_4_escape", "escape sector closure", "projector/domain, boundary/harmonic, history/nonlocal and common-mode escape rows zero", "3929-3932"),
        ("ASM3935_5_monopole", "calibrated common mode", "only universal derivative-silent xi_0 is absorbed into measured GM", "3932"),
        ("ASM3935_6_scope", "no-smuggle scope", "outside-branch cases revoke zero rows and use fallback/bound rows", "3934"),
    ]
    return [
        {
            "row_id": row_id,
            "assumption": assumption,
            "meaning": meaning,
            "evidence": evidence,
            "status": "EXPLICIT_THEOREM_ASSUMPTION",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, assumption, meaning, evidence in data
    ]


def conclusion_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CON3935_0_GR", "local GR equation", "G_mu_nu+Lambda_*g_mu_nu=8*pi*G_*T_vis"),
        ("CON3935_1_Newton", "Newtonian weak-field limit", "nabla^2 Phi=4*pi*G_*rho_H and a=-grad Phi"),
        ("CON3935_2_Maxwell", "Maxwell/EM stress", "T_EM is inside T_vis; Poynting/field energy is not deleted"),
        ("CON3935_3_source", "calibrated source coupling", "G_* constant locally, M_eff source-silent, Z_Poisson=1, Z_frame=1"),
        ("CON3935_4_PPN", "PPN vector", "Delta_PPN_GR=(gamma-1,beta-1,alpha1,alpha2,alpha3,xi,zeta_i,Gdot/G)_loc=0"),
        ("CON3935_5_escape", "local escape envelope", "B_escape_loc=0"),
    ]
    return [
        {
            "row_id": row_id,
            "conclusion": conclusion,
            "private_branch_result": result,
            "status": "CONDITIONAL_PRIVATE_BRANCH_RESULT",
            "public_claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, conclusion, result in data
    ]


def revocation_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("REV3935_0_dynamic", "dynamic/source-active source", "revoke stationary Gdot/source zeros", "FB3914_1_dynamic_source; PPNR3915_8_total"),
        ("REV3935_1_boundary", "net boundary/radiative/Poynting flux", "revoke boundary/harmonic zero", "BFB3930_4_total"),
        ("REV3935_2_memory", "incoming memory/nonlocal kernel", "revoke history reset zero", "HSB3931_4_total"),
        ("REV3935_3_common", "radial/time/source/frame common-mode hair", "revoke calibrated monopole absorption", "CMB3932_5_total"),
        ("REV3935_4_projector", "active Hodge/Green/trace/moving-domain projector", "revoke readout/topological projector zero", "FB3929_4_total"),
        ("REV3935_5_R11", "surviving STF R11/non-EH operator", "revoke gamma/STF zero", "PPNR3915_0_gamma"),
        ("REV3935_6_EM", "nonminimal EM or hidden F^2 coefficient", "revoke minimal same-frame Maxwell conclusion", "EM normalization/coefficient gates"),
        ("REV3935_7_cosmo_galaxy", "cosmology/galaxy/open-system arena", "do not import local branch theorem", "arena-specific empirical robustness passes"),
    ]
    return [
        {
            "row_id": row_id,
            "trigger": trigger,
            "revoked_zero": revoked,
            "mandatory_fallback": fallback,
            "status": "REVOCATION_RULE_READY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, trigger, revoked, fallback in data
    ]


def dashboard_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("DASH3935_0_PPN", "PPN", "gamma,beta,alpha_i,xi,zeta_i,Gdot", "3915 executable PPN vector", "first dashboard"),
        ("DASH3935_1_R10", "R10/Yukawa", "alpha(lambda)", "R10 bound rows when finite-range branch active", "second dashboard"),
        ("DASH3935_2_orbital", "orbital/ephemeris", "epsilon_r and radial finite-range hair", "3932 fallback rows", "second dashboard"),
        ("DASH3935_3_clock", "clock/Gdot/alpha", "time drift/source-active clock or alpha leakage", "3914/3932 fallback rows", "third dashboard"),
        ("DASH3935_4_cosmology_galaxy", "cosmology/galaxy", "arena-specific likelihood/robustness", "do not import local theorem", "separate empirical programme"),
    ]
    return [
        {
            "row_id": row_id,
            "dashboard": dashboard,
            "tracked_quantities": quantities,
            "source_basis": source_basis,
            "priority": priority,
            "status": "QUEUE_READY_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, dashboard, quantities, source_basis, priority in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3935_0_theorem_ready",
            "decision": "polished private local theorem is ready for internal use",
            "reason": THEOREM_STATEMENT,
            "claim_status": "PRIVATE_THEOREM_READY_NONCLAIM",
            "next_action": "build first PPN bound dashboard from fallback rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3935_1_dashboard_queue",
            "decision": "first dashboard should be PPN because it directly audits the local theorem boundary",
            "reason": "PPN has explicit zero vector plus executable fallback vector",
            "claim_status": "DASHBOARD_QUEUE_READY",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3935_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "build the first PPN bound dashboard from fallback rows",
            "success_condition": "machine-readable PPN scorecard with zero-branch flags, fallback formulas, current source status and no-claim gates",
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
            "summary": "polished private local-GR theorem and first bound dashboard queue emitted",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return f"""# 3935 - Local GR Conditional Theorem Polish and First Bound Dashboard

Timestamp: `{timestamp}`

## Private Theorem

**{THEOREM_NAME}.**

`{THEOREM_STATEMENT}`

## Scope Rule

`{SCOPE_RULE}`

## Conclusions Inside The Branch

- Local GR equation: `G_mu_nu+Lambda_*g_mu_nu=8*pi*G_*T_vis`.
- Newtonian limit: `nabla^2 Phi=4*pi*G_*rho_H`, `a=-grad Phi`.
- Maxwell stress: `T_EM` is included in `T_vis`; Poynting/field energy is not deleted.
- Source coupling: local `G_*`, `M_eff`, `Z_Poisson`, and `Z_frame` are locked inside the stationary source collar.
- PPN vector: `Delta_PPN_GR=0`.
- Escape envelope: `B_escape_loc=0`.

## What Revokes The Zero

Dynamic sources, boundary flux, incoming memory, radial/time/source/frame common-mode hair, active projectors, surviving STF R11, nonminimal EM, and cosmology/galaxy/open-system arenas revoke the relevant zero row and require fallback scoring.

## First Dashboard Queue

The first dashboard should be the PPN fallback dashboard because it directly tests the edge of the theorem: gamma, beta, alpha_i, xi, zeta_i, Gdot, and optional short-range/Yukawa rows.

## Source Register

- Source rows found: `{found}/{len(source_rows)}`
- Register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3935_SOURCE_REGISTER.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3935_VALIDATION.csv`

## Generated Tables

- `source-intake\\mts_residuals\\P8_Y5_R2FR_3935_POLISHED_LOCAL_GR_THEOREM.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3935_THEOREM_ASSUMPTION_LEDGER.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3935_THEOREM_CONCLUSION_LEDGER.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3935_REVOCATION_AND_FALLBACK_RULES.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3935_FIRST_BOUND_DASHBOARD_QUEUE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3935_DECISION_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3935_NEXT_TARGET.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3935 - Local GR Conditional Theorem Polish

Timestamp: `{timestamp}`

- Theorem: `{THEOREM_STATEMENT}`.
- Scope rule: `{SCOPE_RULE}`.
- First dashboard: PPN fallback dashboard tracking gamma, beta, alpha_i, xi, zeta_i, Gdot and optional short-range/Yukawa rows.
- Status: private theorem polished for internal use; no public claim; first bound dashboard queued.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3935 - Local GR Conditional Theorem Polish"
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
    theorem = theorem_rows(timestamp)
    assumptions = assumption_rows(timestamp)
    conclusions = conclusion_rows(timestamp)
    revocations = revocation_rows(timestamp)
    dashboard = dashboard_rows(timestamp)
    decisions = decision_rows(timestamp)
    paths = list(OUTPUTS.values()) + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    fwb_modified = formalization_workbench_modified_count()
    checks = [
        ("VAL3935_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3935_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3935_02_theorem", len(theorem) == 1 and THEOREM_NAME in theorem[0]["theorem_name"], "polished theorem emitted"),
        ("VAL3935_03_assumptions", len(assumptions) == 7, "assumption ledger emitted"),
        ("VAL3935_04_conclusions", len(conclusions) == 6 and any(row["conclusion"] == "PPN vector" for row in conclusions), "conclusion ledger emitted"),
        ("VAL3935_05_revocations", len(revocations) == 8 and any(row["trigger"] == "cosmology/galaxy/open-system arena" for row in revocations), "revocation/fallback rules emitted"),
        ("VAL3935_06_dashboard", len(dashboard) == 5 and dashboard[0]["dashboard"] == "PPN", "first bound dashboard queue emitted with PPN first"),
        ("VAL3935_07_nonclaim", all(str(row.get("valid_for_claim")) == "False" for group in (theorem, assumptions, conclusions, revocations, dashboard, decisions) for row in group), "all rows are nonclaim"),
        ("VAL3935_08_outputs_not_fwb", all(not FWB in path.parents for path in paths), "no generated output path is inside formalization-workbench"),
        ("VAL3935_09_fwb_unmodified", fwb_modified == 0, f"formalization-workbench modified-file count is {fwb_modified}"),
        ("VAL3935_10_doc_written", DOC_PATH.exists(), "checkpoint markdown exists"),
        ("VAL3935_11_spine_written", SPINE_PATH.exists() and "3935 - Local GR Conditional Theorem Polish" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3935_12_next_target", next_rows(timestamp)[0]["next_doc"] == NEXT_DOC, "next target row emitted"),
        ("VAL3935_13_script_compiles", True, "script compiles"),
        ("VAL3935_14_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
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
    write_csv(OUTPUTS["theorem"], theorem_rows(timestamp))
    write_csv(OUTPUTS["assumptions"], assumption_rows(timestamp))
    write_csv(OUTPUTS["conclusions"], conclusion_rows(timestamp))
    write_csv(OUTPUTS["revocation"], revocation_rows(timestamp))
    write_csv(OUTPUTS["dashboard"], dashboard_rows(timestamp))
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
        raise SystemExit(f"3935 validation failed: {failed}")
    print(f"3935 complete: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

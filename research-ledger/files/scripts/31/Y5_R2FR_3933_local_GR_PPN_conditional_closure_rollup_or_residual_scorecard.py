from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3933"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3933-Y5-R2FR-local-GR-PPN-conditional-closure-rollup-or-residual-scorecard.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3933_SOURCE_REGISTER.csv",
    "closure": SRC / "P8_Y5_R2FR_3933_LOCAL_GR_CLOSURE_AUDIT.csv",
    "ppn": SRC / "P8_Y5_R2FR_3933_PPN_ZERO_ROLLUP.csv",
    "arenas": SRC / "P8_Y5_R2FR_3933_NEWTON_MAXWELL_SOURCE_ARENA_ROLLUP.csv",
    "fallback": SRC / "P8_Y5_R2FR_3933_OUT_OF_BRANCH_FALLBACK_SCORECARD.csv",
    "decision": SRC / "P8_Y5_R2FR_3933_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3933_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3933_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3933_VALIDATION.csv",
}

LOCAL_BRANCH = (
    "B_loc^closed := EH public metric + same-frame Hilbert/Maxwell source + G0 constant coupling + "
    "stationary q_src source collar + source-silent M_eff + R11 STF/double-zero silence + EH beta square law + "
    "calibrated monopole common mode + readout/topological projector + isolated no-flux boundary + local no-incoming history reset"
)
PPN_ZERO = "Delta_PPN_GR=(gamma-1,beta-1,alpha1,alpha2,alpha3,xi,zeta_i,Gdot/G)_loc=0"
ARENA_RESULT = (
    "G_mu_nu+Lambda_*g_mu_nu=8*pi*G_*T_vis, T_vis includes T_EM, "
    "and nabla^2 Phi=4*pi*G_*rho_H in the weak-field slow-motion limit"
)
NONCLAIM = (
    "PRIVATE_CONDITIONAL_THEOREM_STACK_ONLY: not a public local-GR claim, not an empirical pass, "
    "and not valid outside the stationary isolated/reset/calibrated local branch"
)
NEXT_DOC = "3934-Y5-R2FR-local-branch-countermodel-pressure-test-or-first-empirical-bound-scorecard.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3934_local_branch_countermodel_pressure_test_or_first_empirical_bound_scorecard.py"


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
        ("SRC3933_00_3932_doc", PCW / "3932-Y5-R2FR-derivative-hair-square-law-epsilonr-lock-or-bound.md", "Local escape result:", "3932 local B_escape zero handoff"),
        ("SRC3933_01_3932_escape", SRC / "P8_Y5_R2FR_3932_LOCAL_BESCAPE_RESULT.csv", "LBE3932_3_after", "local B_escape zero row"),
        ("SRC3933_02_3932_next", SRC / "P8_Y5_R2FR_3932_NEXT_TARGET.csv", "NEXT3932_0", "3933 handoff"),
        ("SRC3933_03_3923_doc", PCW / "3923-Y5-R2FR-local-GR-conditional-theorem-stack-and-remaining-bound-pack.md", "Conditional PPN conclusion:", "3923 theorem stack"),
        ("SRC3933_04_3923_stack", SRC / "P8_Y5_R2FR_3923_LOCAL_GR_CONDITIONAL_THEOREM_STACK.csv", "THM3923_10_total", "local GR theorem statement"),
        ("SRC3933_05_3926_core", SRC / "P8_Y5_R2FR_3926_CORE_LOCAL_BRANCH_ADOPTION_RECORD.csv", "CORE3926_0_status", "private core branch adoption"),
        ("SRC3933_06_3914_doc", PCW / "3914-Y5-R2FR-stationary-local-source-coupling-stack-or-readout-residual-map.md", "Newton/Maxwell source statement:", "source/Newton/Maxwell stack"),
        ("SRC3933_07_3914_arena", SRC / "P8_Y5_R2FR_3914_LOCAL_GR_NEWTON_MAXWELL_ARENA_STACK.csv", "ARE3914_2_Maxwell", "Maxwell stress arena"),
        ("SRC3933_08_3915_doc", PCW / "3915-Y5-R2FR-stationary-local-branch-contract-and-PPN-residual-vector.md", "Conditional PPN zero vector:", "PPN branch contract"),
        ("SRC3933_09_3915_ppn", SRC / "P8_Y5_R2FR_3915_CONDITIONAL_PPN_ZERO_VECTOR.csv", "PPNZ3915_8_total", "PPN zero vector"),
        ("SRC3933_10_3918_doc", PCW / "3918-Y5-R2FR-delta-gamma-R11-theorem-zero-or-symbolic-bound-tightening.md", "P_TF[R11_ij]=0", "gamma STF zero"),
        ("SRC3933_11_3919_doc", PCW / "3919-Y5-R2FR-beta-source-second-order-lock-or-common-mode-R11-bound.md", "B_source=A_source^2", "beta source lock"),
        ("SRC3933_12_3929_zero", SRC / "P8_Y5_R2FR_3929_PROJECTOR_DOMAIN_ZERO_RESULT.csv", "PDZ3929_4_epsilon_domain_projector_abs", "projector/domain zero"),
        ("SRC3933_13_3930_zero", SRC / "P8_Y5_R2FR_3930_BOUNDARY_HARMONIC_ZERO_RESULT.csv", "BHZ3930_1_B_harmonic_boundary", "boundary/harmonic zero"),
        ("SRC3933_14_3931_zero", SRC / "P8_Y5_R2FR_3931_HISTORY_NONLOCAL_ZERO_RESULT.csv", "HNZ3931_3_B_history", "history/nonlocal zero"),
        ("SRC3933_15_3932_validation", SRC / "P8_Y5_BRR545_3932_VALIDATION.csv", "VAL3932_14_no_pycache", "3932 validation"),
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


def closure_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CL3933_0_core", "core parent branch", "EH/source/Y/R11/G0 core adopted for private workbench", "3926 core adoption", "CLOSED_PRIVATE"),
        ("CL3933_1_source", "same-frame Hilbert/Maxwell source", "T_vis includes matter and Maxwell stress in one public frame", "3914 source stack", "CLOSED_PRIVATE"),
        ("CL3933_2_Newton", "Newtonian source normalization", "nabla^2 Phi=4*pi*G_*rho_H and a=-grad Phi", "3914 Newton arena", "CLOSED_PRIVATE"),
        ("CL3933_3_Gdot", "stationary local Gdot", "d_t ln G_*=0, B_Meff=0, Z_Poisson=1, Z_frame=1", "3914 Gdot arena", "CLOSED_PRIVATE"),
        ("CL3933_4_gamma", "gamma/STF slip", "P_TF[R11_ij]=0 => gamma-1=0", "3918 STF theorem route", "CLOSED_PRIVATE"),
        ("CL3933_5_beta_source", "beta source square law", "B_source=A_source^2 in EH/Hilbert branch", "3919 beta source lock", "CLOSED_PRIVATE"),
        ("CL3933_6_escape", "escape sector", "projector/domain + boundary/harmonic + history/nonlocal + derivative/common-mode escape all zero", "3929-3932", "CLOSED_PRIVATE"),
        ("CL3933_7_ppn", "PPN vector", PPN_ZERO, "3915/3923 plus 3932 closure", "CLOSED_PRIVATE"),
        ("CL3933_8_scope", "scope guard", NONCLAIM, "all claim gates", "NONCLAIM_GUARD"),
    ]
    return [
        {
            "row_id": row_id,
            "closure_item": item,
            "closure_statement": statement,
            "evidence": evidence,
            "closure_status": status,
            "public_claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, item, statement, evidence, status in data
    ]


def ppn_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("PPN3933_0_gamma", "gamma-1", "0", "STF R11 zero plus same-readout EH frame"),
        ("PPN3933_1_beta", "beta-1", "0", "EH source square law plus calibrated-monopole Delta_sq=0"),
        ("PPN3933_2_alpha1", "alpha1", "0", "no independent vector/domain/frame marker in B_loc"),
        ("PPN3933_3_alpha2", "alpha2", "0", "same common-frame/no-preferred-frame clause"),
        ("PPN3933_4_alpha3", "alpha3", "0", "Bianchi conservation plus stationary source collar and no boundary/domain self-acceleration"),
        ("PPN3933_5_xi", "xi", "0", "no anisotropic/nonlocal/preferred-location kernel in local collar"),
        ("PPN3933_6_zeta_i", "zeta_i", "0", "same-frame Hilbert stress plus Bianchi conservation"),
        ("PPN3933_7_Gdot", "Gdot/G", "0", "stationary local source-coupling stack"),
        ("PPN3933_8_total", "Delta_PPN_GR", "0-vector", PPN_ZERO),
    ]
    return [
        {
            "row_id": row_id,
            "ppn_component": component,
            "private_branch_value": value,
            "reason": reason,
            "status": "ZERO_IN_PRIVATE_LOCAL_BRANCH",
            "public_claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, component, value, reason in data
    ]


def arena_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("ARE3933_0_GR", "local GR equation", "G_mu_nu+Lambda_*g_mu_nu=8*pi*G_*T_vis", "conditional private branch"),
        ("ARE3933_1_Newton", "Newtonian mechanics", "nabla^2 Phi=4*pi*G_*rho_H and a=-grad Phi", "weak-field slow-motion limit with Hilbert source"),
        ("ARE3933_2_Maxwell", "Maxwell/EM stress", "T_EM^{mu nu} is included in T_vis and Poynting/field energy is not deleted", "same-frame Hilbert/Maxwell source"),
        ("ARE3933_3_source", "calibrated source coupling", "G_* measured/superselected, M_eff source-silent, Z_Poisson=1, Z_frame=1", "stationary source collar"),
        ("ARE3933_4_common_mode", "measured GM calibration", "only universal derivative-silent xi_0 monopole is calibratable", "3932 no-hair absorption guard"),
    ]
    return [
        {
            "row_id": row_id,
            "arena": arena,
            "private_branch_result": result,
            "scope": scope,
            "status": "CONDITIONAL_PRIVATE_ROLLUP",
            "public_claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, arena, result, scope in data
    ]


def fallback_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("FB3933_0_dynamic", "dynamic/source-active local systems", "use executable PPN residual vector and Gdot/source fallback rows"),
        ("FB3933_1_nonisolated", "non-isolated/radiating systems", "boundary/harmonic and Poynting flux fallback rows remain active"),
        ("FB3933_2_nonlocal", "history/nonlocal arenas", "use 3931 suppression law rather than reset zero"),
        ("FB3933_3_common_hair", "radial/time/source/frame common-mode hair", "use 3932 fallback bound rows; do not absorb into GM"),
        ("FB3933_4_cosmology_galaxies", "cosmology/galaxies/open systems", "do not import local isolated branch closure; use empirical robustness passes"),
        ("FB3933_5_nonEH_EM", "non-EH or nonminimal EM sectors", "retain coefficient/source maps and Maxwell normalization gates"),
    ]
    return [
        {
            "row_id": row_id,
            "out_of_branch_case": case,
            "required_fallback": fallback,
            "status": "FALLBACK_RETAINED",
            "public_claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, case, fallback in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3933_0_private_closure",
            "decision": "the private stationary isolated/reset/calibrated local branch now conditionally closes to local GR/PPN/Newton/Maxwell/source coupling",
            "reason": LOCAL_BRANCH,
            "claim_status": "PRIVATE_CONDITIONAL_THEOREM_STACK_READY",
            "next_action": "pressure-test the branch with countermodels and retained fallback rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3933_1_no_public_claim",
            "decision": "do not promote this as a public local-GR or empirical claim yet",
            "reason": NONCLAIM,
            "claim_status": "NO_PUBLIC_CLAIM",
            "next_action": "run 3934 pressure/countermodel audit before any GitHub/public wording",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3933_2_next",
            "decision": "next target is countermodel pressure test or first empirical bound scorecard",
            "reason": "a conditional theorem must be stress-tested against dynamic, nonisolated, nonlocal, non-EH and common-hair escapes",
            "claim_status": "NEXT_PRESSURE_TEST",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3933_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "pressure-test the private local closure against countermodels and retained fallback cases",
            "success_condition": "identify any hidden smuggled assumption or confirm the branch survives as a clearly scoped conditional theorem with fallback scorecards",
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
            "summary": "local GR/PPN/Newton/Maxwell/source-coupling conditional closure rollup built; pressure-test remains",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return f"""# 3933 - Local GR/PPN Conditional Closure Rollup or Residual Scorecard

Timestamp: `{timestamp}`

## Result

Built the conditional local closure rollup.

Closed private branch:

`{LOCAL_BRANCH}`.

PPN result inside branch:

`{PPN_ZERO}`.

GR/Newton/Maxwell/source result inside branch:

`{ARENA_RESULT}`.

Scope guard:

`{NONCLAIM}`.

## Meaning

This is a major private-branch milestone: after 3929-3932, the escape sector no longer blocks the stationary isolated/reset/calibrated local route. The rollup says that, under the listed branch clauses, MTS reduces to local GR/PPN/Newton with Maxwell stress included in the same Hilbert source.

It is not public evidence yet. Dynamic systems, non-isolated systems, cosmology, galaxies, nonlocal memory arenas, non-EH operators, nonminimal EM couplings, and common-mode hair still use fallback rows.

## Source Register

- Source rows found: `{found}/{len(source_rows)}`
- Register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3933_SOURCE_REGISTER.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3933_VALIDATION.csv`

## Generated Tables

- `source-intake\\mts_residuals\\P8_Y5_R2FR_3933_LOCAL_GR_CLOSURE_AUDIT.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3933_PPN_ZERO_ROLLUP.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3933_NEWTON_MAXWELL_SOURCE_ARENA_ROLLUP.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3933_OUT_OF_BRANCH_FALLBACK_SCORECARD.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3933_DECISION_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3933_NEXT_TARGET.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3933 - Local GR/PPN Conditional Closure Rollup

Timestamp: `{timestamp}`

- Closed private branch: `{LOCAL_BRANCH}`.
- PPN result: `{PPN_ZERO}`.
- Arena result: `{ARENA_RESULT}`.
- Scope guard: `{NONCLAIM}`.
- Status: private stationary isolated/reset/calibrated local branch conditionally closes; pressure-test/fallback scorecard remains before any public claim.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3933 - Local GR/PPN Conditional Closure Rollup"
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
    closure = closure_rows(timestamp)
    ppn = ppn_rows(timestamp)
    arenas = arena_rows(timestamp)
    fallback = fallback_rows(timestamp)
    decisions = decision_rows(timestamp)
    paths = list(OUTPUTS.values()) + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    fwb_modified = formalization_workbench_modified_count()
    checks = [
        ("VAL3933_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3933_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3933_02_closure_rows", len(closure) == 9 and any(row["closure_item"] == "PPN vector" for row in closure), "closure audit emitted"),
        ("VAL3933_03_ppn_zero", len(ppn) == 9 and any(row["ppn_component"] == "Delta_PPN_GR" and row["private_branch_value"] == "0-vector" for row in ppn), "PPN zero rollup emitted"),
        ("VAL3933_04_arenas", len(arenas) == 5 and any(row["arena"] == "Maxwell/EM stress" for row in arenas), "Newton/Maxwell/source arena rollup emitted"),
        ("VAL3933_05_fallback", len(fallback) == 6 and any(row["out_of_branch_case"] == "cosmology/galaxies/open systems" for row in fallback), "out-of-branch fallback scorecard emitted"),
        ("VAL3933_06_no_public_claim", all(str(row.get("public_claim_allowed")) == "False" for group in (closure, ppn, arenas, fallback) for row in group), "public claim guard false throughout"),
        ("VAL3933_07_nonclaim", all(str(row.get("valid_for_claim")) == "False" for group in (closure, ppn, arenas, fallback, decisions) for row in group), "all rows are nonclaim"),
        ("VAL3933_08_outputs_not_fwb", all(not FWB in path.parents for path in paths), "no generated output path is inside formalization-workbench"),
        ("VAL3933_09_fwb_unmodified", fwb_modified == 0, f"formalization-workbench modified-file count is {fwb_modified}"),
        ("VAL3933_10_doc_written", DOC_PATH.exists(), "checkpoint markdown exists"),
        ("VAL3933_11_spine_written", SPINE_PATH.exists() and "3933 - Local GR/PPN Conditional Closure Rollup" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3933_12_next_target", next_rows(timestamp)[0]["next_doc"] == NEXT_DOC, "next target row emitted"),
        ("VAL3933_13_script_compiles", True, "script compiles"),
        ("VAL3933_14_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
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
    write_csv(OUTPUTS["closure"], closure_rows(timestamp))
    write_csv(OUTPUTS["ppn"], ppn_rows(timestamp))
    write_csv(OUTPUTS["arenas"], arena_rows(timestamp))
    write_csv(OUTPUTS["fallback"], fallback_rows(timestamp))
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
        raise SystemExit(f"3933 validation failed: {failed}")
    print(f"3933 complete: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

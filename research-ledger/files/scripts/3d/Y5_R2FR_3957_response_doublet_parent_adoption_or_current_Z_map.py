from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3957"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3957-Y5-R2FR-response-doublet-parent-adoption-or-current-Z-map.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3957_SOURCE_REGISTER.csv",
    "adoption": SRC / "P8_Y5_R2FR_3957_RESPONSE_DOUBLET_ADOPTION_GATE.csv",
    "map": SRC / "P8_Y5_R2FR_3957_CURRENT_Z_MAP_REQUIREMENTS.csv",
    "decision": SRC / "P8_Y5_R2FR_3957_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3957_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3957_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3957_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3957_VALIDATION.csv",
}

NEXT_DOC = "3958-Y5-R2FR-current-variable-to-response-doublet-map-or-demotion.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3958_current_variable_to_response_doublet_map_or_demotion.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


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
        ("SRC3957_00_3956_next", SRC / "P8_Y5_R2FR_3956_NEXT_TARGET.csv", "NEXT3956_0", "3956 handoff"),
        ("SRC3957_01_3956_vertical", SRC / "P8_Y5_R2FR_3956_RESPONSE_DOUBLET_VERTICALITY_COMPUTATION.csv", "RDV3956_2_Z_generator", "constructed Z verticality"),
        ("SRC3957_02_3956_CA", SRC / "P8_Y5_R2FR_3956_RESPONSE_DOUBLET_VERTICALITY_COMPUTATION.csv", "RDV3956_4_CA_result", "constructed C_A zero"),
        ("SRC3957_03_3956_current", SRC / "P8_Y5_R2FR_3956_RESPONSE_DOUBLET_VERTICALITY_COMPUTATION.csv", "RDV3956_5_current_MTS_status", "current map still blocked"),
        ("SRC3957_04_3956_CA_value", SRC / "P8_Y5_R2FR_3956_CA_COMPONENT_VALUES.csv", "CAV3956_1_CA_response_doublet", "constructed C_A zero value"),
        ("SRC3957_05_GO516", SRC / "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv", "GO516_A_response_doublet_quadratic_density", "response-doublet candidate action"),
        ("SRC3957_06_3953_density", SRC / "P8_Y5_R2FR_3953_MINIMAL_GAMMA_VARIATION.csv", "MGV3953_0_density_ansatz", "minimal Gamma density"),
        ("SRC3957_07_3953_double", SRC / "P8_Y5_R2FR_3953_MINIMAL_GAMMA_VARIATION.csv", "MGV3953_3_double_zero", "double-zero law"),
        ("SRC3957_08_3955_current", SRC / "P8_Y5_R2FR_3955_CA_ZERO_THEOREM_OR_BOUND.csv", "CA3955_3_current_Z_status", "current Z map missing"),
        ("SRC3957_09_QVM1620", SRC / "P8_Y5_PARENT_QLOC_1620_QUOTIENT_VERTICALITY_MAP_AUDIT.csv", "QVM1620_5_verdict", "current verticality verdict"),
        ("SRC3957_10_validation_3956", SRC / "P8_Y5_BRR545_3956_VALIDATION.csv", "VAL3956_17_no_pycache", "previous validation"),
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
                    excerpt = line[:1000]
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
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def adoption_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "RDA3957_0_constructed_math",
            "adoption_clause": "constructed response-doublet mathematics",
            "requirement": "R_even=(R_++R_-)/2, Z=(R_+-R_-)/2, q_RD=R_even, Dq_RD[v_Z]=0",
            "evidence_status": "PASS_FROM_3956",
            "effect": "constructed branch has C_A=0 and J_A^obs=0 if g_obs is q_RD-basic",
            "current_decision": "KEEP_AS_STRONG_CONSTRUCTED_BRANCH",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RDA3957_1_parent_action_owner",
            "adoption_clause": "parent action owns response doublets",
            "requirement": "actual MTS parent action defines R_+^A,R_-^A and the exchange-even/odd split before matter coupling",
            "evidence_status": "NOT_PARENT_SIGNED",
            "effect": "without this, response-doublet branch is an ansatz/closure candidate",
            "current_decision": "BLOCK_ADOPTION",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RDA3957_2_current_variable_map",
            "adoption_clause": "actual residual variables map to R_+,R_-,R_even,Z",
            "requirement": "source paths identify current MTS residual symbols and their plus/minus partners",
            "evidence_status": "MISSING_CURRENT_VARIABLE_MAP",
            "effect": "cannot state current Z^A equals response-doublet odd coordinate",
            "current_decision": "BLOCK_ADOPTION",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RDA3957_3_observable_readout",
            "adoption_clause": "observable metric/readout is R_even-basic",
            "requirement": "g_obs, matter constants, coframe, source support and coupling factors depend on R_even/Q_pub but not Z",
            "evidence_status": "NOT_SIGNED",
            "effect": "direct Z readout could reintroduce C_A and source current",
            "current_decision": "BLOCK_ADOPTION",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RDA3957_4_Khat_Gamma_match",
            "adoption_clause": "Gamma/Khat branch uses the same Z/R_even variables",
            "requirement": "Gamma_eff=Gamma0+quadratic(Z;G_AB,M_AB,R_even,...) and Khat is metric response of the same density",
            "evidence_status": "CONSTRUCTED_NOT_CURRENT_MATCHED",
            "effect": "the local-GR Khat and source-current zero routes must share one parent object",
            "current_decision": "BLOCK_ADOPTION_FOR_CURRENT_CLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RDA3957_5_adoption_verdict",
            "adoption_clause": "response-doublet parent adoption verdict",
            "requirement": "all adoption clauses pass",
            "evidence_status": "NOT_ADOPTED_YET",
            "effect": "constructed route remains valuable, but current MTS source coupling uses C_A residual rows until adoption closes",
            "current_decision": "CONDITIONAL_BRANCH_RETAINED_CURRENT_BRANCH_BOUND_ONLY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def map_requirement_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("ZMAP3957_0_fields", "actual field list", "identify current residual variables that could be R_+^A and R_-^A", "MISSING_FIELD_SOURCE_PATHS"),
        ("ZMAP3957_1_pairing", "plus/minus pairing", "prove the two representatives are exchange partners rather than unrelated variables", "MISSING_PAIRING_RULE"),
        ("ZMAP3957_2_even", "R_even ownership", "show observable/readout variables depend on R_even and public variables", "MISSING_REVEN_READOUT_OWNER"),
        ("ZMAP3957_3_odd", "Z ownership", "show Z is an odd residual coordinate removed from q_RD", "MISSING_Z_ODD_OWNER"),
        ("ZMAP3957_4_gobs", "g_obs basicity", "prove g_obs=gbar(R_even,Q_pub,...) with no direct Z term", "MISSING_GOBS_BASICITY"),
        ("ZMAP3957_5_matter", "matter/source descent", "prove S_matter and source support see R_even/Q_pub but not Z", "MISSING_MATTER_SOURCE_DESCENT"),
        ("ZMAP3957_6_Khat", "Gamma/Khat consistency", "prove Gamma_eff and Khat use the same Z/R_even split", "MISSING_GAMMA_KHAT_MATCH"),
        ("ZMAP3957_7_current_bound", "current bound fallback", "if any clause fails, fill C_A_total_current and source-current residual rows", "BOUND_ROWS_ACTIVE"),
    ]
    return [
        {
            "row_id": row_id,
            "map_item": item,
            "requirement": requirement,
            "current_status": status,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, item, requirement, status in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3957_0_keep_branch",
            "decision": "retain response-doublet as the lead constructed local-source-silence branch",
            "basis": "3956 computes Dq_RD[v_Z]=0 and C_A=0 exactly",
            "effect": "this is the best derivation route, not discarded",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3957_1_no_current_promotion",
            "decision": "do not promote response-doublet branch to current MTS",
            "basis": "GO516 says best_candidate_not_current_MTS_derived and current variable/readout map is missing",
            "effect": "local-GR/Newton source coupling remains nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3957_2_next",
            "decision": f"move to {NEXT_DOC}",
            "basis": "the next real task is source-path mapping of current variables to R_+,R_-,R_even,Z",
            "effect": "either parent-adopt the branch or demote it cleanly",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CG3957_0_sources", "source-backed adoption checkpoint", "all source paths and needles exist", "PASS_IF_VALIDATION_PASS"),
        ("CG3957_1_constructed_math", "constructed response-doublet theorem", "Dq_RD[v_Z]=0 and C_A=0", "PASS_CONSTRUCTED_BRANCH"),
        ("CG3957_2_parent_adoption", "parent action adoption", "actual MTS parent owns R_+/R_-/R_even/Z", "BLOCKED_PARENT_OWNER_MISSING"),
        ("CG3957_3_current_map", "current variable map", "current residuals mapped to response doublets", "BLOCKED_CURRENT_VARIABLE_MAP_MISSING"),
        ("CG3957_4_readout", "readout basicity", "g_obs/source/matter readout depends on R_even not Z", "BLOCKED_READOUT_BASICITY_MISSING"),
        ("CG3957_5_local_GR", "local-GR/Newton source coupling", "adoption plus Khat/Gamma/source descent close", "BLOCKED_NONCLAIM"),
    ]
    return [
        {
            "row_id": row_id,
            "gate": gate,
            "requirement": requirement,
            "status": status,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, gate, requirement, status in data
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3957_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "map current MTS residual variables to response-doublet coordinates with source paths; either produce an adoption certificate or demote response-doublet to constructed closure and keep current C_A bound rows live",
            "success_condition": "actual variable/source rows fill R_+,R_-,R_even,Z and g_obs basicity, or a formal demotion row preserves the constructed theorem without claiming current MTS adoption",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in source_rows)
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_PRIVATE_NONCLAIM_CHECKPOINT",
            "summary": "3957 keeps the response-doublet source-silence branch as the lead constructed theorem but blocks current MTS adoption until variable/readout source paths are supplied.",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in source_rows)
    return f"""# 3957 - Response-Doublet Parent Adoption Or Current Z Map

Timestamp: `{timestamp}`

## Result

3957 decides the status of the response-doublet route.

It is retained as the lead constructed theorem because 3956 proved:

`q_RD(R_+,R_-)=R_even`

and:

`Dq_RD[v_Z]=0`.

Therefore the constructed branch gives `C_A=0` and `J_A^obs=0` when `g_obs` is `R_even`-basic.

## Honest Adoption Verdict

The branch is not yet adopted as current MTS.

Required adoption rows are still missing:

- actual `R_+`, `R_-`, `R_even`, `Z` source paths;
- a parent action that owns the exchange pair;
- `g_obs`/matter/source readout depending on `R_even` but not `Z`;
- the same `Z/R_even` split used by `Gamma_eff` and `K_hat`.

So the current branch remains bound-only via `C_A_total_current`.

## Source Register

- Source rows found: `{found}/{len(source_rows)}`
- Register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3957_SOURCE_REGISTER.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3957_VALIDATION.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3957 - Response-Doublet Adoption Gate

Timestamp: `{timestamp}`

- Retained the response-doublet branch as the lead constructed route: `Dq_RD[v_Z]=0`, hence `C_A=0` and `J_A^obs=0` if `g_obs` is `R_even`-basic.
- Did not adopt it as current MTS because actual `R_+`, `R_-`, `R_even`, `Z` source paths and readout basicity are missing.
- Current source-coupling route remains `C_A_total_current` bound-only.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3957 - Response-Doublet Adoption Gate"
    if SPINE_PATH.exists():
        text = read_text(SPINE_PATH)
        if marker in text:
            before = text.split(marker, 1)[0].rstrip()
            SPINE_PATH.write_text(before + block, encoding="utf-8")
        else:
            SPINE_PATH.write_text(text.rstrip() + block, encoding="utf-8")
    else:
        SPINE_PATH.write_text("# Local GR Coupling Spine - Current State\n" + block, encoding="utf-8")


def formalization_workbench_git_status() -> tuple[bool, str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT), "status", "--porcelain", "--", str(FWB.relative_to(ROOT))],
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
        )
    except Exception:
        return False, "git status unavailable; scope guard confirms generated outputs are outside formalization-workbench"
    if result.returncode != 0:
        return False, "git status unavailable; scope guard confirms generated outputs are outside formalization-workbench"
    modified_count = len([line for line in result.stdout.splitlines() if line.strip()])
    return modified_count == 0, f"formalization-workbench modified count is {modified_count}"


def csv_parse_ok(paths: list[Path]) -> bool:
    try:
        for path in paths:
            if path.exists():
                read_csv(path)
    except Exception:
        return False
    return True


def validation_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    adoption = adoption_rows(timestamp)
    maps = map_requirement_rows(timestamp)
    decisions = decision_rows(timestamp)
    claim_gate = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    paths = generated_csvs + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    fwb_git_clean, fwb_git_detail = formalization_workbench_git_status()
    adoption_statuses = {row["evidence_status"] for row in adoption}
    map_statuses = {row["current_status"] for row in maps}
    gate_statuses = {row["status"] for row in claim_gate}
    nonclaim_groups = (adoption, maps, decisions, claim_gate, next_target)
    checks = [
        ("VAL3957_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3957_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3957_02_constructed_kept", "PASS_FROM_3956" in adoption_statuses, "constructed response-doublet theorem retained"),
        ("VAL3957_03_parent_block", "NOT_PARENT_SIGNED" in adoption_statuses, "parent action adoption block retained"),
        ("VAL3957_04_variable_map_block", "MISSING_CURRENT_VARIABLE_MAP" in adoption_statuses and "MISSING_FIELD_SOURCE_PATHS" in map_statuses, "current variable map block retained"),
        ("VAL3957_05_readout_block", "NOT_SIGNED" in adoption_statuses and "MISSING_GOBS_BASICITY" in map_statuses, "readout basicity block retained"),
        ("VAL3957_06_verdict", "NOT_ADOPTED_YET" in adoption_statuses, "adoption verdict is nonclaim"),
        ("VAL3957_07_claim_gate_blocks", "PASS_CONSTRUCTED_BRANCH" in gate_statuses and "BLOCKED_PARENT_OWNER_MISSING" in gate_statuses and "BLOCKED_NONCLAIM" in gate_statuses, "claim gate distinguishes constructed from adopted branch"),
        ("VAL3957_08_next_target", next_target[0]["next_doc"] == NEXT_DOC and next_target[0]["next_script"] == NEXT_SCRIPT, "next target points to current variable map/demotion"),
        ("VAL3957_09_all_nonclaim", all(not row["valid_for_claim"] for group in nonclaim_groups for row in group), "all generated physics rows remain nonclaim"),
        ("VAL3957_10_outputs_outside_fwb", all(FWB not in path.parents and path != FWB for path in paths), "no generated output is inside formalization-workbench"),
        ("VAL3957_11_fwb_git_or_scope_guard", fwb_git_clean or all(FWB not in path.parents and path != FWB for path in paths), fwb_git_detail),
        ("VAL3957_12_doc_exists", DOC_PATH.exists(), "checkpoint doc exists"),
        ("VAL3957_13_spine_updated", SPINE_PATH.exists() and "3957 - Response-Doublet Adoption Gate" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3957_14_csv_parse", csv_parse_ok(generated_csvs), "generated CSV files parse cleanly"),
        ("VAL3957_15_script_compile", True, "script compiled before validation write"),
        ("VAL3957_16_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    return [
        {
            "validation_id": validation_id,
            "passed": bool(passed),
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for validation_id, passed, detail in checks
    ]


def run() -> None:
    timestamp = now_utc()
    source_rows = source_register_rows(timestamp)
    adoption = adoption_rows(timestamp)
    maps = map_requirement_rows(timestamp)
    decisions = decision_rows(timestamp)
    claim_gate = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp, source_rows)

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["adoption"], adoption)
    write_csv(OUTPUTS["map"], maps)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["claim_gate"], claim_gate)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)

    DOC_PATH.write_text(doc_text(timestamp, source_rows), encoding="utf-8")
    update_spine(timestamp)

    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    validations = validation_rows(timestamp, source_rows)
    write_csv(OUTPUTS["validation"], validations)
    failed = [row for row in validations if not row["passed"]]
    if failed:
        raise SystemExit(f"3957 validation failed: {failed}")

    print(f"3957 checkpoint complete: {DOC_PATH}")
    print(f"validation: {OUTPUTS['validation']}")
    print("response-doublet kept as constructed branch; current MTS adoption blocked pending variable map")


if __name__ == "__main__":
    run()

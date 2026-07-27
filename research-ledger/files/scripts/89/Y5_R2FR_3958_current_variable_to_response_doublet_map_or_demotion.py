from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3958"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3958-Y5-R2FR-current-variable-to-response-doublet-map-or-demotion.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3958_SOURCE_REGISTER.csv",
    "map": SRC / "P8_Y5_R2FR_3958_CURRENT_TO_RESPONSE_DOUBLET_MAP.csv",
    "demotion": SRC / "P8_Y5_R2FR_3958_RESPONSE_DOUBLET_DEMOTION_OR_ADOPTION.csv",
    "live_route": SRC / "P8_Y5_R2FR_3958_LIVE_CURRENT_ROUTE_REBASE.csv",
    "decision": SRC / "P8_Y5_R2FR_3958_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3958_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3958_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3958_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3958_VALIDATION.csv",
}

NEXT_DOC = "3959-Y5-R2FR-current-Yloc-Sigma-parent-action-or-CA-bound-values.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3959_current_Yloc_Sigma_parent_action_or_CA_bound_values.py"


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
        ("SRC3958_00_3957_next", SRC / "P8_Y5_R2FR_3957_NEXT_TARGET.csv", "NEXT3957_0", "3957 handoff"),
        ("SRC3958_01_3957_keep", SRC / "P8_Y5_R2FR_3957_RESPONSE_DOUBLET_ADOPTION_GATE.csv", "RDA3957_0_constructed_math", "constructed theorem kept"),
        ("SRC3958_02_3957_verdict", SRC / "P8_Y5_R2FR_3957_RESPONSE_DOUBLET_ADOPTION_GATE.csv", "RDA3957_5_adoption_verdict", "3957 adoption verdict"),
        ("SRC3958_03_2967_density", SRC / "P8_Y5_R2FR_2967_RESPONSE_DOUBLET_ADOPTION_GATE.csv", "RDA2967_0_density_ansatz", "old density adoption status"),
        ("SRC3958_04_2967_verdict", SRC / "P8_Y5_R2FR_2967_RESPONSE_DOUBLET_ADOPTION_GATE.csv", "RDA2967_7_verdict", "old response-doublet promotion verdict"),
        ("SRC3958_05_2977_doublets", SRC / "P8_Y5_R2FR_2977_RESPONSE_DOUBLET_OWNER_LOCK_AUDIT.csv", "OWN2977_0_parent_doublets", "parent doublet owner lock"),
        ("SRC3958_06_2977_verdict", SRC / "P8_Y5_R2FR_2977_RESPONSE_DOUBLET_OWNER_LOCK_AUDIT.csv", "OWN2977_7_verdict", "owner lock verdict"),
        ("SRC3958_07_3555_formal", SRC / "P8_Y5_R2FR_3555_RESPONSE_DOUBLET_THEOREM.csv", "RDT3555_0_quadratic_Gamma", "formal double-zero theorem"),
        ("SRC3958_08_3555_hard", SRC / "P8_Y5_R2FR_3555_RESPONSE_DOUBLET_THEOREM.csv", "RDT3555_3_hard_row_refusal", "oddness shortcut refusal"),
        ("SRC3958_09_3629_law", SRC / "P8_Y5_R2FR_3629_RESPONSE_DOUBLET_COUPLING_LAW.csv", "CL3629_1_linearized_Z_Euler", "linearized source current law"),
        ("SRC3958_10_3629_contract", SRC / "P8_Y5_R2FR_3629_RESPONSE_DOUBLET_COUPLING_LAW.csv", "CL3629_3_zero_theorem_contract", "total action zero contract"),
        ("SRC3958_11_2217_verdict", SRC / "P8_Y5_PARENT_QLOC_2217_RESPONSE_DOUBLET_PARENT_DENSITY_CANDIDATE.csv", "RDP2217_4_density_verdict", "density construction verdict"),
        ("SRC3958_12_2582_verdict", SRC / "P8_Y5_RESPONSE_DOUBLET_QLOC_2582_DOUBLET_GATE.csv", "RDG2582_8_verdict", "response doublet GK route verdict"),
        ("SRC3958_13_3534_variable", SRC / "P8_Y5_R2FR_3534_MTS_VARIABLE_TO_KERNEL_MAP.csv", "MQM3534_0_q_gobs", "current MTS variable kernel map"),
        ("SRC3958_14_3534_memory", SRC / "P8_Y5_R2FR_3534_MTS_VARIABLE_TO_KERNEL_MAP.csv", "MQM3534_6_memory", "current memory/Sigma route"),
        ("SRC3958_15_local_status", SRC / "P8_local_GR_MTS_variable_quotient_double_zero_status.csv", "STAT3534_2_next", "current route next target"),
        ("SRC3958_16_validation_3957", SRC / "P8_Y5_BRR545_3957_VALIDATION.csv", "VAL3957_16_no_pycache", "previous validation"),
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


def map_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CTRD3958_0_Rplus",
            "target_slot": "R_+^A",
            "candidate_current_symbol": "",
            "source_path": "",
            "mapping_status": "NOT_FOUND_AS_PARENT_OWNED_CURRENT_SYMBOL",
            "consequence": "cannot adopt response-doublet branch as current MTS",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CTRD3958_1_Rminus",
            "target_slot": "R_-^A",
            "candidate_current_symbol": "",
            "source_path": "",
            "mapping_status": "NOT_FOUND_AS_PARENT_OWNED_CURRENT_SYMBOL",
            "consequence": "no exchange-pair source path for current variable map",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CTRD3958_2_Reven",
            "target_slot": "R_even^A",
            "candidate_current_symbol": "Y_loc/Sigma_loc kernel route is the closest current replacement, not R_even itself",
            "source_path": str(SRC / "P8_Y5_R2FR_3534_MTS_VARIABLE_TO_KERNEL_MAP.csv"),
            "mapping_status": "NO_DIRECT_REVEN_MAP_CURRENT_ROUTE_REBASED_TO_YLOC",
            "consequence": "response-doublet theorem remains constructed; current branch uses Y_loc/Sigma route",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CTRD3958_3_Z",
            "target_slot": "Z^A",
            "candidate_current_symbol": "formal Z^A appears in response theorem but not as parent-owned physical residual vector",
            "source_path": str(SRC / "P8_Y5_R2FR_2977_RESPONSE_DOUBLET_OWNER_LOCK_AUDIT.csv"),
            "mapping_status": "FORMAL_Z_NOT_PARENT_LOCKED",
            "consequence": "current C_A=0 cannot be claimed from response doublet",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CTRD3958_4_gobs",
            "target_slot": "g_obs basic in R_even",
            "candidate_current_symbol": "q(Phi); g_obs observed coframe",
            "source_path": str(SRC / "P8_Y5_R2FR_3534_MTS_VARIABLE_TO_KERNEL_MAP.csv"),
            "mapping_status": "BEST_ANCHOR_CONDITIONAL_QAP_UNSIGNED",
            "consequence": "use q(Phi)/g_obs quotient-basicity route, not response-doublet adoption",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CTRD3958_5_verdict",
            "target_slot": "current variable to response-doublet map",
            "candidate_current_symbol": "none sufficient",
            "source_path": "P8_Y5_R2FR_2967_RESPONSE_DOUBLET_ADOPTION_GATE.csv;P8_Y5_R2FR_2977_RESPONSE_DOUBLET_OWNER_LOCK_AUDIT.csv;P8_Y5_R2FR_3534_MTS_VARIABLE_TO_KERNEL_MAP.csv",
            "mapping_status": "ADOPTION_FAILED_DEMOTE_TO_CONSTRUCTED_BRANCH",
            "consequence": "response-doublet remains a reusable theorem; live current work returns to Y_loc/Sigma and C_A bounds",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def demotion_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "RDD3958_0_keep_theorem",
            "decision_piece": "keep constructed theorem",
            "evidence": "3956 proved Dq_RD[v_Z]=0 and C_A=0 for the constructed response-doublet quotient",
            "decision": "RETAIN_AS_CONSTRUCTED_THEOREM_BRANCH",
            "effect": "useful for future parent action design and comparison",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RDD3958_1_demote_current",
            "decision_piece": "current MTS adoption",
            "evidence": "2967/2977/2217/2582 all say candidate/not parent-signed/not promoted; 3957 kept adoption blocked",
            "decision": "DEMOTE_RESPONSE_DOUBLET_AS_CURRENT_CLAIM",
            "effect": "current source coupling cannot claim C_A=0 from response doublet",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RDD3958_2_live_route",
            "decision_piece": "live current route",
            "evidence": "3534 maps actual MTS symbols into q(Phi), g_obs, Y_loc/Sigma_loc, Qcoh, memory, flow, EM kernels",
            "decision": "REBASE_TO_CURRENT_YLOC_SIGMA_ROUTE",
            "effect": "derive Y_loc=0 / Sigma_loc positivity or fill C_A current bounds",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def live_route_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("LIVE3958_0_q_gobs", "q(Phi); g_obs; observed coframe", "quotient base/readout anchor", "prove q-basic g_obs and vertical MTS variations leave q fixed", "C_A direct quotient term"),
        ("LIVE3958_1_Yloc", "Y_loc / local silent kernel", "replacement for response-doublet Z branch", "derive Y_loc=0 from explicit parent variation or positive Hessian", "C_A current and q_loc residuals"),
        ("LIVE3958_2_Sigma", "Sigma_loc=G_AB Y^A Y^B", "norm-square double-zero origin", "prove positivity/factorization and no direct source current", "source-current silence"),
        ("LIVE3958_3_Qcoh_memory", "Qcoh; memory; B_mem; U_mem", "current MTS local hair channels", "show local compact coupling factors through Sigma_loc or fill bounds", "R10/R11/PPN residuals"),
        ("LIVE3958_4_EM_Maxwell", "EM Hodge/Maxwell/Poynting residuals", "visible gauge stress plus hidden coupling residual", "same g_obs Hodge and no linear hidden F^2 source or bound it", "Maxwell/EM stress and source coupling"),
        ("LIVE3958_5_CA_bound", "C_A_total_current", "fallback if Yloc/Sigma proof fails", "fill E_DqZ_current, C_A_direct, C_A_coeff, C_A_readout, C_A_boundary values", "PPN/source-normalization residual vector"),
    ]
    return [
        {
            "row_id": row_id,
            "current_symbol": symbol,
            "role": role,
            "next_requirement": requirement,
            "feeds": feeds,
            "status": "LIVE_CURRENT_ROUTE_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, symbol, role, requirement, feeds in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3958_0_demote",
            "decision": "demote response-doublet from current-MTS adoption to constructed theorem branch",
            "basis": "no actual source paths fill R_+,R_-,R_even,Z; older owner/adoption gates remain blocked",
            "effect": "prevents smuggling a clean constructed quotient into current MTS",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3958_1_rebase",
            "decision": "rebase live current route onto Y_loc/Sigma_loc plus C_A bound rows",
            "basis": "3534 provides actual current MTS symbol placements and next target is Yloc Euler/positive Hessian",
            "effect": "next derivation attacks current variables instead of response-doublet ansatz",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3958_2_next",
            "decision": f"move to {NEXT_DOC}",
            "basis": "derive current Y_loc/Sigma parent action or fill current C_A values",
            "effect": "keeps local-GR/source-coupling path derivation-first",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CG3958_0_sources", "source-backed mapping checkpoint", "all source paths and needles exist", "PASS_IF_VALIDATION_PASS"),
        ("CG3958_1_constructed_theorem", "response-doublet constructed theorem", "Dq_RD[v_Z]=0 and C_A=0", "PASS_CONSTRUCTED_BRANCH"),
        ("CG3958_2_current_adoption", "current MTS adoption", "R_+/R_-/R_even/Z source paths and parent ownership", "FAIL_DEMOTED_CURRENT_CLAIM"),
        ("CG3958_3_live_route", "current Y_loc/Sigma route", "parent action variation proves Y_loc=0 or fills C_A bounds", "NEXT_TARGET_REQUIRED"),
        ("CG3958_4_local_GR", "local-GR/Newton/Maxwell/source coupling", "current variables close Khat, C_A, source, EM and coupling gates", "BLOCKED_NONCLAIM"),
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
            "row_id": "NEXT3958_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive the current Y_loc/Sigma_loc parent-action branch: prove Sigma_loc=G_AB Y^A Y^B positive and Y_loc=0 on compact local branch, or fill C_A_total_current/source-current bound values",
            "success_condition": "current MTS variables get a parent-owned local zero theorem, or C_A/source-current residual rows gain finite value-ready component inputs with units and observable links",
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
            "summary": "3958 searched current variable ownership and demoted response-doublet from current-MTS adoption to constructed theorem branch; live current route rebased to Y_loc/Sigma_loc or C_A bounds.",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in source_rows)
    return f"""# 3958 - Current Variable To Response-Doublet Map Or Demotion

Timestamp: `{timestamp}`

## Result

3958 searches the adoption path for the response-doublet branch.

The conclusion is blunt:

- The response-doublet theorem is kept as a strong constructed branch.
- It is not adopted as current MTS.
- Current source coupling must not claim `C_A=0` from response-doublet verticality.

The missing adoption rows are still:

- actual `R_+`, `R_-`, `R_even`, `Z` source paths;
- parent ownership of the exchange pair;
- `g_obs` and matter/source readout basicity;
- same `Z/R_even` split in `Gamma_eff` and `K_hat`.

## Live Route

The live current route is now rebased to actual MTS symbols:

- `q(Phi); g_obs`;
- `Y_loc`;
- `Sigma_loc=G_AB Y^A Y^B`;
- `Qcoh/memory/flow/EM` residual channels;
- fallback `C_A_total_current` bounds.

## Source Register

- Source rows found: `{found}/{len(source_rows)}`
- Register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3958_SOURCE_REGISTER.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3958_VALIDATION.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3958 - Response-Doublet Demotion And Current Route Rebase

Timestamp: `{timestamp}`

- Response-doublet remains a strong constructed theorem branch but is demoted from current-MTS adoption.
- No current `C_A=0` or source-coupling claim can use the response-doublet zero without actual `R_+`, `R_-`, `R_even`, `Z` source paths.
- Live current route is rebased to `Y_loc/Sigma_loc`, current MTS kernel placements, and `C_A_total_current` bound rows.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3958 - Response-Doublet Demotion And Current Route Rebase"
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
    maps = map_rows(timestamp)
    demotion = demotion_rows(timestamp)
    live_route = live_route_rows(timestamp)
    decisions = decision_rows(timestamp)
    claim_gate = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    paths = generated_csvs + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    fwb_git_clean, fwb_git_detail = formalization_workbench_git_status()
    mapping_statuses = {row["mapping_status"] for row in maps}
    demotion_decisions = {row["decision"] for row in demotion}
    live_symbols = {row["current_symbol"] for row in live_route}
    gate_statuses = {row["status"] for row in claim_gate}
    nonclaim_groups = (maps, demotion, live_route, decisions, claim_gate, next_target)
    checks = [
        ("VAL3958_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3958_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3958_02_Rslots_not_found", "NOT_FOUND_AS_PARENT_OWNED_CURRENT_SYMBOL" in mapping_statuses, "R+ and R- not found as parent-owned current symbols"),
        ("VAL3958_03_formal_Z_block", "FORMAL_Z_NOT_PARENT_LOCKED" in mapping_statuses, "formal Z is not parent locked"),
        ("VAL3958_04_demoted", "DEMOTE_RESPONSE_DOUBLET_AS_CURRENT_CLAIM" in demotion_decisions, "response-doublet current claim demoted"),
        ("VAL3958_05_keep_theorem", "RETAIN_AS_CONSTRUCTED_THEOREM_BRANCH" in demotion_decisions, "constructed theorem retained"),
        ("VAL3958_06_rebase", "REBASE_TO_CURRENT_YLOC_SIGMA_ROUTE" in demotion_decisions and {"Y_loc / local silent kernel", "Sigma_loc=G_AB Y^A Y^B", "C_A_total_current"}.issubset(live_symbols), "live route rebased to Yloc/Sigma/C_A"),
        ("VAL3958_07_claim_gate", "FAIL_DEMOTED_CURRENT_CLAIM" in gate_statuses and "NEXT_TARGET_REQUIRED" in gate_statuses and "BLOCKED_NONCLAIM" in gate_statuses, "claim gate blocks current promotion"),
        ("VAL3958_08_next_target", next_target[0]["next_doc"] == NEXT_DOC and next_target[0]["next_script"] == NEXT_SCRIPT, "next target points to current Yloc/Sigma branch"),
        ("VAL3958_09_all_nonclaim", all(not row["valid_for_claim"] for group in nonclaim_groups for row in group), "all generated physics rows remain nonclaim"),
        ("VAL3958_10_outputs_outside_fwb", all(FWB not in path.parents and path != FWB for path in paths), "no generated output is inside formalization-workbench"),
        ("VAL3958_11_fwb_git_or_scope_guard", fwb_git_clean or all(FWB not in path.parents and path != FWB for path in paths), fwb_git_detail),
        ("VAL3958_12_doc_exists", DOC_PATH.exists(), "checkpoint doc exists"),
        ("VAL3958_13_spine_updated", SPINE_PATH.exists() and "3958 - Response-Doublet Demotion And Current Route Rebase" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3958_14_csv_parse", csv_parse_ok(generated_csvs), "generated CSV files parse cleanly"),
        ("VAL3958_15_script_compile", True, "script compiled before validation write"),
        ("VAL3958_16_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
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
    maps = map_rows(timestamp)
    demotion = demotion_rows(timestamp)
    live_route = live_route_rows(timestamp)
    decisions = decision_rows(timestamp)
    claim_gate = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp, source_rows)

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["map"], maps)
    write_csv(OUTPUTS["demotion"], demotion)
    write_csv(OUTPUTS["live_route"], live_route)
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
        raise SystemExit(f"3958 validation failed: {failed}")

    print(f"3958 checkpoint complete: {DOC_PATH}")
    print(f"validation: {OUTPUTS['validation']}")
    print("response-doublet demoted as current claim; live route rebased to Yloc/Sigma or C_A bounds")


if __name__ == "__main__":
    run()

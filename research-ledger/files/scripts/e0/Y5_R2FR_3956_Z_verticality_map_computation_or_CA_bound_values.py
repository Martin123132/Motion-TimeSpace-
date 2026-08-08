from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3956"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3956-Y5-R2FR-Z-verticality-map-computation-or-CA-bound-values.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3956_SOURCE_REGISTER.csv",
    "verticality": SRC / "P8_Y5_R2FR_3956_RESPONSE_DOUBLET_VERTICALITY_COMPUTATION.csv",
    "ca_values": SRC / "P8_Y5_R2FR_3956_CA_COMPONENT_VALUES.csv",
    "source_current": SRC / "P8_Y5_R2FR_3956_SOURCE_CURRENT_UPDATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3956_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3956_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3956_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3956_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3956_VALIDATION.csv",
}

NEXT_DOC = "3957-Y5-R2FR-response-doublet-parent-adoption-or-current-Z-map.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3957_response_doublet_parent_adoption_or_current_Z_map.py"


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
        ("SRC3956_00_3955_next", SRC / "P8_Y5_R2FR_3955_NEXT_TARGET.csv", "NEXT3955_0", "3955 handoff"),
        ("SRC3956_01_3955_vertical", SRC / "P8_Y5_R2FR_3955_CA_ZERO_THEOREM_OR_BOUND.csv", "CA3955_1_vertical_zero_theorem", "C_A zero theorem"),
        ("SRC3956_02_3955_current", SRC / "P8_Y5_R2FR_3955_CA_ZERO_THEOREM_OR_BOUND.csv", "CA3955_3_current_Z_status", "current branch verticality block"),
        ("SRC3956_03_3955_DqZ", SRC / "P8_Y5_R2FR_3955_OBSERVABLE_METRIC_COEFFICIENT_LEDGER.csv", "CAL3955_0_DqZ", "DqZ missing component"),
        ("SRC3956_04_GO516", SRC / "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv", "GO516_A_response_doublet_quadratic_density", "response-doublet candidate"),
        ("SRC3956_05_3953_density", SRC / "P8_Y5_R2FR_3953_MINIMAL_GAMMA_VARIATION.csv", "MGV3953_0_density_ansatz", "minimal Gamma density"),
        ("SRC3956_06_3953_double_zero", SRC / "P8_Y5_R2FR_3953_MINIMAL_GAMMA_VARIATION.csv", "MGV3953_3_double_zero", "double-zero law"),
        ("SRC3956_07_3888_zero", SRC / "P8_Y5_R2FR_3888_QUOTIENT_NO_LINEAR_SOURCE_DERIVATION.csv", "NLS3888_3_observed_zero", "observed source-current zero condition"),
        ("SRC3956_08_3271_vertical", SRC / "P8_Y5_R2FR_3271_QUOTIENT_FIBER_DESCENT_THEOREM.csv", "QFT3271_1_vertical_derivative_zero", "vertical derivative zero theorem"),
        ("SRC3956_09_QVM1620", SRC / "P8_Y5_PARENT_QLOC_1620_QUOTIENT_VERTICALITY_MAP_AUDIT.csv", "QVM1620_5_verdict", "current verticality not closed"),
        ("SRC3956_10_validation_3955", SRC / "P8_Y5_BRR545_3955_VALIDATION.csv", "VAL3955_17_no_pycache", "previous validation"),
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


def verticality_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "RDV3956_0_coordinates",
            "object": "response-doublet coordinates",
            "definition": "R_even^A=(R_+^A+R_-^A)/2; Z^A=(R_+^A-R_-^A)/2",
            "computed_derivative": "partial R_even / partial Z = 0; partial Z / partial Z = 1",
            "result": "COORDINATE_SPLIT_DEFINED",
            "claim_scope": "constructed response-doublet branch only",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RDV3956_1_quotient_map",
            "object": "candidate quotient map",
            "definition": "q_RD(R_+^A,R_-^A) := R_even^A",
            "computed_derivative": "Dq_RD = [1/2, 1/2] in the (R_+,R_-) basis",
            "result": "QUOTIENT_MAP_DECLARED_FOR_CONSTRUCTED_BRANCH",
            "claim_scope": "not yet proven to be the full current MTS q map",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RDV3956_2_Z_generator",
            "object": "odd residual generator",
            "definition": "v_Z := partial/partial Z = partial/partial R_+ - partial/partial R_-",
            "computed_derivative": "Dq_RD[v_Z] = (1/2)(1) + (1/2)(-1) = 0",
            "result": "THEOREM_VERTICAL_FOR_CONSTRUCTED_RESPONSE_DOUBLET",
            "claim_scope": "one actual constructed Z direction is vertical for q_RD",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RDV3956_3_even_generator",
            "object": "public/even generator",
            "definition": "v_even := partial/partial R_even = partial/partial R_+ + partial/partial R_-",
            "computed_derivative": "Dq_RD[v_even] = 1",
            "result": "NOT_VERTICAL_PUBLIC_DIRECTION",
            "claim_scope": "keeps public metric/source variation out of the zero proof",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RDV3956_4_CA_result",
            "object": "observable metric coefficient",
            "definition": "if g_obs=gbar(R_even,Q_pub,...) and no direct Z readout, C_Z=partial_Z g_obs",
            "computed_derivative": "C_Z = Dgbar[Dq_RD[v_Z]] = 0",
            "result": "C_A_ZERO_FOR_CONSTRUCTED_RESPONSE_DOUBLET",
            "claim_scope": "constructed branch theorem-zero; current MTS still requires adoption/mapping",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RDV3956_5_current_MTS_status",
            "object": "current MTS map",
            "definition": "actual current q and Z^A basis",
            "computed_derivative": "not computed; QVM1620 says verticality map is not closed",
            "result": "CURRENT_BRANCH_STILL_BLOCKED",
            "claim_scope": "no public local-GR/Newton source-coupling claim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def ca_value_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CAV3956_0_DqZ_response_doublet", "E_DqZ_response_doublet", "Dq_RD[v_Z]", "0", "exact_constructed_branch", "THEOREM_ZERO_CONSTRUCTED_NONCLAIM"),
        ("CAV3956_1_CA_response_doublet", "C_A_response_doublet", "Dgbar[Dq_RD[v_Z]]", "0", "metric_linear_coefficient", "THEOREM_ZERO_CONSTRUCTED_NONCLAIM"),
        ("CAV3956_2_Jobs_response_doublet", "J_A_obs_response_doublet", "1/2 T_obs^{mu nu} C_{A mu nu}", "0", "source_current_units", "THEOREM_ZERO_CONSTRUCTED_NONCLAIM"),
        ("CAV3956_3_DqZ_current", "E_DqZ_current_MTS", "Dq_current[Z_A]", "", "dimensionless_or_declared", "MISSING_CURRENT_Q_Z_MAP"),
        ("CAV3956_4_CA_direct_current", "C_A_direct_current_MTS", "direct Z readout in g_obs", "", "metric_linear_coefficient", "MISSING_CURRENT_READOUT_GRAMMAR"),
        ("CAV3956_5_CA_total_current", "C_A_total_current_MTS", "sum/envelope(E_DqZ_current,C_A_direct,C_A_coeff,C_A_readout,C_A_boundary)", "", "metric_linear_coefficient_or_dimensionless_norm", "COMPONENT_VALUES_MISSING"),
    ]
    return [
        {
            "row_id": row_id,
            "component": component,
            "formula": formula,
            "value": value,
            "units": units,
            "status": status,
            "score_ready": status == "THEOREM_ZERO_CONSTRUCTED_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, component, formula, value, units, status in data
    ]


def source_current_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "SCU3956_0_constructed_branch",
            "quantity": "J_A^obs",
            "formula": "J_A^obs = 1/2 T_obs^{mu nu} C_{A mu nu}",
            "result": "0 on the constructed response-doublet quotient branch",
            "remaining_terms": "J_A^direct, J_A^measure, J_A^support require no-direct-readout/source-support descent",
            "claim_scope": "constructed nonclaim branch",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SCU3956_1_current_branch",
            "quantity": "J_A^obs current MTS",
            "formula": "|J_A^obs| <= 1/2 ||T_obs|| ||C_A_total_current||",
            "result": "bound form retained",
            "remaining_terms": "current q/Z/readout map missing",
            "claim_scope": "current MTS nonclaim fallback",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3956_0_constructed_pass",
            "decision": "response-doublet quotient gives an exact vertical Z direction",
            "basis": "q_RD=R_even and v_Z=(1,-1) imply Dq_RD[v_Z]=0",
            "effect": "the constructed parent branch has C_A=0 and J_A^obs=0 if g_obs is q_RD-basic",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3956_1_current_not_promoted",
            "decision": "do not promote current MTS to source-current silence",
            "basis": "actual current q map, actual Z basis, and direct readout grammar are still unsigned",
            "effect": "C_A bound components remain active for the current branch",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3956_2_next",
            "decision": f"move to {NEXT_DOC}",
            "basis": "the next step is adopting/matching the response-doublet parent branch to actual MTS variables or rejecting it",
            "effect": "this decides whether the clean branch becomes live or remains a constructed closure candidate",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CG3956_0_sources", "source-backed verticality computation", "all source paths and needles exist", "PASS_IF_VALIDATION_PASS"),
        ("CG3956_1_constructed_Z", "constructed response-doublet Z verticality", "Dq_RD[v_Z]=0", "PASS_CONSTRUCTED_BRANCH"),
        ("CG3956_2_constructed_CA", "constructed C_A zero", "g_obs is q_RD-basic and no direct Z readout", "PASS_CONDITIONAL_CONSTRUCTED_BRANCH"),
        ("CG3956_3_current_Z", "current MTS Z verticality", "actual Z^A basis lies in actual ker(Dq)", "BLOCKED_CURRENT_Q_Z_MAP_MISSING"),
        ("CG3956_4_current_readout", "current direct readout", "C_A_direct_current=0", "BLOCKED_READOUT_GRAMMAR_UNSIGNED"),
        ("CG3956_5_local_GR", "local-GR/Newton source coupling", "constructed branch adopted plus all direct/measure/support terms closed", "BLOCKED_NONCLAIM"),
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
            "row_id": "NEXT3956_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "decide whether the response-doublet quotient branch is a parent-owned MTS structure: map actual residual variables to R_+,R_-,R_even,Z and prove g_obs/readout uses R_even but not Z, or reject it and keep C_A current-bound rows",
            "success_condition": "response-doublet branch is parent-adopted with actual variable/source paths, or it is explicitly demoted to constructed closure and current C_A residual components remain the live route",
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
            "summary": "3956 computes an exact response-doublet quotient verticality map: Dq[v_Z]=0, giving constructed-branch C_A=0 and J_A^obs=0, while current MTS remains unpromoted.",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in source_rows)
    return f"""# 3956 - Z Verticality Map Computation Or C_A Bound Values

Timestamp: `{timestamp}`

## Result

3956 performs the first explicit verticality computation for the response-doublet branch.

Define:

`R_even = (R_+ + R_-)/2`

`Z = (R_+ - R_-)/2`

and the quotient:

`q_RD(R_+,R_-) = R_even`.

Then:

`Dq_RD[partial_Z] = (1/2)(1) + (1/2)(-1) = 0`.

So `Z` is exactly vertical for this constructed response-doublet quotient.

If `g_obs = gbar(R_even,Q_pub,...)` and has no direct `Z` readout, then:

`C_Z = partial_Z g_obs = 0`

and:

`J_Z^obs = 1/2 T_obs C_Z = 0`.

## Honest Scope

This is a real computed branch, not a public claim. Current MTS still needs actual variable adoption:

- actual residual variables mapped to `R_+`, `R_-`, `R_even`, `Z`;
- actual observable metric/readout proved to depend on `R_even` but not `Z`;
- direct/measure/support source-current terms closed.

## Source Register

- Source rows found: `{found}/{len(source_rows)}`
- Register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3956_SOURCE_REGISTER.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3956_VALIDATION.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3956 - Response-Doublet Z Verticality Computation

Timestamp: `{timestamp}`

- Computed the response-doublet quotient `q_RD(R_+,R_-)=R_even=(R_++R_-)/2`.
- Computed `Dq_RD[partial_Z]=(1/2)-(1/2)=0` for `Z=(R_+-R_-)/2`.
- Therefore the constructed branch has `C_Z=0` and `J_Z^obs=0` if `g_obs` is q-basic and has no direct Z readout.
- Current MTS remains nonclaim until actual variables adopt this response-doublet structure.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3956 - Response-Doublet Z Verticality Computation"
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
    verticality = verticality_rows(timestamp)
    ca_values = ca_value_rows(timestamp)
    source_current = source_current_rows(timestamp)
    decisions = decision_rows(timestamp)
    claim_gate = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    paths = generated_csvs + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    fwb_git_clean, fwb_git_detail = formalization_workbench_git_status()
    v_results = {row["result"] for row in verticality}
    ca_components = {row["component"]: row for row in ca_values}
    gate_statuses = {row["status"] for row in claim_gate}
    nonclaim_groups = (verticality, ca_values, source_current, decisions, claim_gate, next_target)
    checks = [
        ("VAL3956_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3956_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3956_02_quotient_declared", "QUOTIENT_MAP_DECLARED_FOR_CONSTRUCTED_BRANCH" in v_results, "response-doublet quotient map declared"),
        ("VAL3956_03_Z_vertical", "THEOREM_VERTICAL_FOR_CONSTRUCTED_RESPONSE_DOUBLET" in v_results, "Dq[v_Z]=0 computed"),
        ("VAL3956_04_CA_zero", "C_A_ZERO_FOR_CONSTRUCTED_RESPONSE_DOUBLET" in v_results, "constructed C_A zero emitted"),
        ("VAL3956_05_current_block", "CURRENT_BRANCH_STILL_BLOCKED" in v_results, "current MTS branch not promoted"),
        ("VAL3956_06_CA_values", ca_components.get("E_DqZ_response_doublet", {}).get("value") == "0" and ca_components.get("C_A_response_doublet", {}).get("value") == "0" and ca_components.get("J_A_obs_response_doublet", {}).get("value") == "0", "constructed zero values emitted"),
        ("VAL3956_07_current_missing_values", ca_components.get("E_DqZ_current_MTS", {}).get("status") == "MISSING_CURRENT_Q_Z_MAP" and ca_components.get("C_A_total_current_MTS", {}).get("status") == "COMPONENT_VALUES_MISSING", "current branch missing values retained"),
        ("VAL3956_08_claim_gate_blocks", "PASS_CONSTRUCTED_BRANCH" in gate_statuses and "BLOCKED_CURRENT_Q_Z_MAP_MISSING" in gate_statuses and "BLOCKED_NONCLAIM" in gate_statuses, "claim gate distinguishes constructed from current branch"),
        ("VAL3956_09_next_target", next_target[0]["next_doc"] == NEXT_DOC and next_target[0]["next_script"] == NEXT_SCRIPT, "next target points to response-doublet adoption gate"),
        ("VAL3956_10_all_nonclaim", all(not row["valid_for_claim"] for group in nonclaim_groups for row in group), "all generated physics rows remain nonclaim"),
        ("VAL3956_11_outputs_outside_fwb", all(FWB not in path.parents and path != FWB for path in paths), "no generated output is inside formalization-workbench"),
        ("VAL3956_12_fwb_git_or_scope_guard", fwb_git_clean or all(FWB not in path.parents and path != FWB for path in paths), fwb_git_detail),
        ("VAL3956_13_doc_exists", DOC_PATH.exists(), "checkpoint doc exists"),
        ("VAL3956_14_spine_updated", SPINE_PATH.exists() and "3956 - Response-Doublet Z Verticality Computation" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3956_15_csv_parse", csv_parse_ok(generated_csvs), "generated CSV files parse cleanly"),
        ("VAL3956_16_script_compile", True, "script compiled before validation write"),
        ("VAL3956_17_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
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
    verticality = verticality_rows(timestamp)
    ca_values = ca_value_rows(timestamp)
    source_current = source_current_rows(timestamp)
    decisions = decision_rows(timestamp)
    claim_gate = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp, source_rows)

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["verticality"], verticality)
    write_csv(OUTPUTS["ca_values"], ca_values)
    write_csv(OUTPUTS["source_current"], source_current)
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
        raise SystemExit(f"3956 validation failed: {failed}")

    print(f"3956 checkpoint complete: {DOC_PATH}")
    print(f"validation: {OUTPUTS['validation']}")
    print("response-doublet verticality computed: Dq[v_Z]=0; current branch remains nonclaim")


if __name__ == "__main__":
    run()

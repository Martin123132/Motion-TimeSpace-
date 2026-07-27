from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3909"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3909-Y5-R2FR-first-measured-Gstar-component-fill-Gdot-or-WEP.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3909_SOURCE_REGISTER.csv",
    "zeroform": SRC / "P8_Y5_R2FR_3909_GSTAR_ZEROFORM_ACTION_BLOCK.csv",
    "gdot_components": SRC / "P8_Y5_R2FR_3909_GDOT_COMPONENT_CLOSURE_MATRIX.csv",
    "fallback": SRC / "P8_Y5_R2FR_3909_GDOT_FALLBACK_COMPONENT_RUNNER.csv",
    "decision": SRC / "P8_Y5_R2FR_3909_BRANCH_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3909_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3909_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3909_VALIDATION.csv",
}

ZEROFORM_ACTION = "S_G0 = (1/(2*kappa_0)) int sqrt(-Q)(R[Q]-2 Lambda_*) + int_M C_G dA_3"
ZEROFORM_VARIATION = "delta_{A_3} S_G0 = - int_M dC_G wedge delta A_3 + boundary => dC_G=0 on connected local domains"
GSTAR_IDENTIFICATION = "C_G := 1/(2*kappa_0), kappa_0=8*pi*G_*/c^4, so dC_G=0 => d_t ln G_*=d_r ln G_*=0 for the G_* sector"
TOTAL_GDOT = "Gdot_total = |d_t ln G_*| + |d_t ln M_eff| + |d_t epsilon_mu/(1+epsilon_mu)| + |d_t ln Z_Poisson| + |d_t ln Z_frame|"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def rel(path: Path) -> str:
    return str(path.relative_to(PCW)) if path.is_relative_to(PCW) else str(path)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
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
        ("SRC3909_00_next", SRC / "P8_Y5_R2FR_3908_NEXT_TARGET.csv", "NEXT3908_0", "3908 selected first component fill target"),
        ("SRC3909_01_zroute", SRC / "P8_Y5_R2FR_3908_GSTAR_DERIVATIVE_ZERO_ROUTE_MATRIX.csv", "ZR3908_0_time", "3908 time derivative zero route"),
        ("SRC3909_02_runner", SRC / "P8_Y5_R2FR_3908_GSTAR_DERIVATIVE_BOUND_RUNNER.csv", "RUN3908_1_Gdot", "3908 Gdot runner"),
        ("SRC3909_03_3880", SRC / "P8_Y5_R2FR_3880_GEFF_DERIVATIVE_SILENCE_THEOREM.csv", "GST3880_1_topological_route", "Geff topological zero-form route"),
        ("SRC3909_04_3881", SRC / "P8_Y5_R2FR_3881_GDOT_FALLBACK_BOUND_ROWS.csv", "GDOT3881_2_Cstar_component", "Gdot fallback component rows"),
        ("SRC3909_05_3758", SRC / "P8_Y5_R2FR_3758_GDOT_BOUND_EVALUATION.csv", "GB3758_2_max_allowed_residual", "Gdot numeric budget"),
        ("SRC3909_06_kappa_theorem", SRC / "P8_CONSTANT_KAPPA_SUPERSELECTION_THEOREM.csv", "T508_1_topological_zeroform", "constant kappa topological zeroform theorem"),
        ("SRC3909_07_kappa_clause", SRC / "P8_CONSTANT_KAPPA_TOPOLOGICAL_ZEROFORM_CLAUSE.csv", "K508_1_variation_A3", "zeroform action clause"),
        ("SRC3909_08_kappa_tests", SRC / "P8_CONSTANT_KAPPA_GATE_TESTS.csv", "G508_1_parent_adoption", "kappa route claim gate"),
        ("SRC3909_09_gstar_owner", SRC / "P8_Y5_R2FR_3906_GSTAR_OWNER_MATRIX.csv", "G3906_2_constant_owner", "Gstar owner matrix"),
        ("SRC3909_10_policy", SRC / "P8_Y5_R2FR_3907_MEASURED_COUPLING_POLICY_RUNNER.csv", "POL3907_1_derivatives", "measured coupling derivative policy"),
        ("SRC3909_11_validation", SRC / "P8_Y5_BRR545_3908_VALIDATION.csv", "VAL3908_11_next_target", "3908 validation"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in source_specs():
        exists = path.exists()
        found = exists and needle in read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "path": rel(path),
                "exists": exists,
                "needle": needle,
                "needle_found": found,
                "role": role,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def zeroform_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "block_id": "ZF3909_0_action",
            "piece": "topological Gstar action block",
            "equation": ZEROFORM_ACTION,
            "result": "turns the measured GR coupling into an integration-constant sector rather than a local scalar field",
            "status": "CANDIDATE_PARENT_ACTION_BLOCK_READY",
            "remaining_failure": "not yet derived from deeper MTS action; adoption is a parent-branch choice",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "block_id": "ZF3909_1_variation_A3",
            "piece": "three-form variation",
            "equation": ZEROFORM_VARIATION,
            "result": "derives dC_G=0 without using observations or fitted GM",
            "status": "EXACT_VARIATIONAL_ZERO_IF_BLOCK_ADOPTED",
            "remaining_failure": "boundary variation of A_3 must be fixed/topological",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "block_id": "ZF3909_2_Gstar",
            "piece": "Gstar derivative consequence",
            "equation": GSTAR_IDENTIFICATION,
            "result": "d_t ln G_*=0 for the Gstar coupling sector",
            "status": "GSTAR_TIME_COMPONENT_ZERO_IF_BLOCK_ADOPTED",
            "remaining_failure": "does not by itself close M_eff/source/readout drift",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "block_id": "ZF3909_3_stress",
            "piece": "metric stress silence",
            "equation": "delta_Q int C_G dA_3 = 0 if A_3 sector is metric-independent and boundary class is fixed",
            "result": "topological coupling owner does not add local stress or preferred-frame force",
            "status": "STRESS_SILENT_IF_METRIC_INDEPENDENT",
            "remaining_failure": "must forbid hidden metric dependence in A_3 measure/boundary representative",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "block_id": "ZF3909_4_label_blindness",
            "piece": "source/range/species blindness",
            "equation": "partial_A C_G=partial_lambda C_G=partial_frame C_G=partial_domain C_G=0",
            "result": "same block can support WEP/range/frame zero routes for the coupling component only",
            "status": "LABEL_BLIND_IF_GLOBAL_SECTOR",
            "remaining_failure": "source mass and frame/readout product factors remain separate gates",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gdot_component_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "component_id": "GDC3909_0_CG",
            "component": "d_t ln G_*",
            "formula": "d_t ln G_* = - d_t ln C_G if constants are related by C_G=1/(2*kappa_0)",
            "zero_or_bound": "0 if ZF3909_1 variation is adopted",
            "status": "CONDITIONALLY_ZERO_COMPONENT_FILLED",
            "remaining_failure": "parent action has not globally adopted ZF3909 block",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "GDC3909_1_Meff",
            "component": "d_t ln M_eff",
            "formula": "Pi_M/J_H flux conservation component of measured GM drift",
            "zero_or_bound": "requires closed Hilbert worldtube mass current or numeric bound",
            "status": "OPEN_SEPARATE_COMPONENT",
            "remaining_failure": "Pi_M/H_tau/source-normalization still active",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "GDC3909_2_mu",
            "component": "d_t epsilon_mu/(1+epsilon_mu)",
            "formula": "time drift of mu_extra/(G_eff M_eff)",
            "zero_or_bound": "requires extra-sector/source residual silence or numeric bound",
            "status": "OPEN_SEPARATE_COMPONENT",
            "remaining_failure": "boundary/bulk/domain/memory/range source residuals remain active",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "GDC3909_3_Zpoisson",
            "component": "d_t ln Z_Poisson",
            "formula": "time drift in Poisson/source-normalization readout coefficient",
            "zero_or_bound": "requires same EH/Hilbert/Poisson calibration branch or numeric bound",
            "status": "OPEN_SEPARATE_COMPONENT",
            "remaining_failure": "source-measure calibration not globally closed",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "GDC3909_4_Zframe",
            "component": "d_t ln Z_frame",
            "formula": "time drift in source/orbit/clock/reference frame lock",
            "zero_or_bound": "requires same-frame/tau/source branch or numeric bound",
            "status": "OPEN_SEPARATE_COMPONENT",
            "remaining_failure": "frame/tau/readout residuals remain active",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def fallback_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "GDF3909_0_conditional_zero",
            "case": "adopt ZF3909 and close other drift components",
            "formula": TOTAL_GDOT,
            "value_or_status": "0 if every component is theorem-zero",
            "bound": "9.6e-15 yr^-1",
            "result": "CONDITIONAL_PASS_NOT_CLAIMED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "runner_id": "GDF3909_1_partial_zero",
            "case": "adopt ZF3909 only for Gstar",
            "formula": "Gdot_total = 0 + |d_t ln M_eff| + |d_t epsilon_mu/(1+epsilon_mu)| + |d_t ln Z_Poisson| + |d_t ln Z_frame|",
            "value_or_status": "GSTAR_COMPONENT_CLOSED_OTHER_INPUTS_MISSING",
            "bound": "9.6e-15 yr^-1",
            "result": "BLOCKED_COMPONENTS_REMAIN",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "runner_id": "GDF3909_2_live_fallback",
            "case": "no ZF3909 adoption",
            "formula": TOTAL_GDOT,
            "value_or_status": "MISSING_NUMERIC_COMPONENTS",
            "bound": "9.6e-15 yr^-1",
            "result": "BOUND_FORMULA_READY_NUMERIC_COMPONENTS_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "runner_id": "GDF3909_3_dry_pass",
            "case": "arithmetic check",
            "formula": "sum components = 2e-16 yr^-1",
            "value_or_status": "2e-16",
            "bound": "9.6e-15 yr^-1",
            "result": "PASS_DRYRUN_ARITHMETIC_ONLY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "runner_id": "GDF3909_4_dry_fail",
            "case": "arithmetic check",
            "formula": "sum components = 1e-12 yr^-1",
            "value_or_status": "1e-12",
            "bound": "9.6e-15 yr^-1",
            "result": "FAIL_DRYRUN_ARITHMETIC_ONLY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3909_0_component",
            "decision": "treat d_t ln G_* as conditionally closed by the zero-form mechanism",
            "reason": "ZF3909 supplies an actual variational equation dC_G=0, not a plateau axiom",
            "effect": "Gstar time drift can be set to zero only on the adopted topological-coupling branch",
            "status": "COMPONENT_FILLED_CONDITIONAL",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3909_1_total_Gdot",
            "decision": "do not claim total Gdot pass",
            "reason": "M_eff, epsilon_mu, Poisson calibration and frame drift are not closed by the Gstar zero-form block",
            "effect": "Gdot_total remains a component-sum bound until remaining terms are zeroed or sourced",
            "status": "TOTAL_GDOT_BLOCKED",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3909_2_next",
            "decision": "attack M_eff/source-normalization drift next",
            "reason": "after Gstar drift, d_t ln M_eff is the largest structural Gdot/GM obstruction",
            "effect": "next checkpoint should close Hilbert worldtube mass flux or produce numeric bound rows",
            "status": "NEXT_ROUTE_SELECTED",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3909_0",
            "target_checkpoint": "3910-Y5-R2FR-Meff-Hilbert-worldtube-drift-zero-or-Gdot-bound-fill.md",
            "script": "scripts/Y5_R2FR_3910_Meff_Hilbert_worldtube_drift_zero_or_Gdot_bound_fill.py",
            "objective": "derive or bound d_t ln M_eff through closed Hilbert worldtube mass flux, Pi_M/H_tau commutation, and source-frame support; otherwise fill numeric Gdot component rows",
            "why_next": "3909 conditionally closes d_t ln G_* but total Gdot still depends on measured source mass drift and source-normalization",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_GSTAR_TIME_COMPONENT_ZEROFORM_MECHANISM_FILLED",
            "claim": "NO_TOTAL_GDOT_OR_LOCAL_GR_CLAIM",
            "summary": "topological zero-form action block derives d_t ln G_*=0 if adopted; total measured Gdot remains blocked by M_eff, epsilon_mu, Poisson/readout and frame components",
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, Any]],
    zeroform: list[dict[str, Any]],
    gdot_components: list[dict[str, Any]],
    fallback: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    timestamp: str,
) -> None:
    doc = f"""# 3909 - First Measured-Gstar Component Fill: Gdot or WEP

Generated: `{timestamp}`

## Result

3909 attacks the first measured-`G_*` derivative component: `d_t ln G_*`.

Candidate parent action block:

`{ZEROFORM_ACTION}`

Variation:

`{ZEROFORM_VARIATION}`

Identification:

`{GSTAR_IDENTIFICATION}`

Verdict: this is a real mechanism, not a closure word. If the parent branch adopts the zero-form/three-form coupling block, the `G_*` time-drift component is zero. But total measured `Gdot` is **not** closed, because source mass drift, extra source drift, Poisson calibration and frame drift remain separate terms:

`{TOTAL_GDOT}`

## Gstar Zeroform Action Block

{markdown_table(zeroform, ["block_id", "piece", "equation", "status", "remaining_failure"])}

## Gdot Component Closure Matrix

{markdown_table(gdot_components, ["component_id", "component", "formula", "zero_or_bound", "status", "remaining_failure"])}

## Gdot Fallback Component Runner

{markdown_table(fallback, ["runner_id", "case", "formula", "value_or_status", "bound", "result"])}

## Branch Decision Gate

{markdown_table(decision, ["decision_id", "decision", "reason", "effect", "status"])}

## Source Register

Resolved `{sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)}/{len(sources)}` source rows.

{markdown_table(sources, ["source_id", "path", "needle_found", "role"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_checkpoint", "objective", "why_next"])}

## Bottom Line

We moved one real piece: `d_t ln G_*` now has an explicit topological parent mechanism. The local-GR branch still cannot claim a total `Gdot` pass until `M_eff`, `epsilon_mu`, `Z_Poisson`, and `Z_frame` are closed or bounded.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    block = f"""

<!-- BEGIN 3909 GSTAR ZEROFORM GDOT COMPONENT -->
## 3909 Gstar Zeroform Gdot Component

Timestamp: `{timestamp}`

Action block:
`{ZEROFORM_ACTION}`

Variation:
`{ZEROFORM_VARIATION}`

Gstar consequence:
`{GSTAR_IDENTIFICATION}`

Total measured Gdot still requires:
`{TOTAL_GDOT}`

Decision: `d_t ln G_*` is conditionally filled by a real zero-form mechanism; total Gdot remains blocked by measured-source/readout terms.
<!-- END 3909 GSTAR ZEROFORM GDOT COMPONENT -->
"""
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    start = "<!-- BEGIN 3909 GSTAR ZEROFORM GDOT COMPONENT -->"
    end = "<!-- END 3909 GSTAR ZEROFORM GDOT COMPONENT -->"
    if start in existing and end in existing:
        before = existing.split(start, 1)[0].rstrip()
        after = existing.split(end, 1)[1].lstrip()
        SPINE_PATH.write_text(before + block + "\n" + after, encoding="utf-8")
    else:
        SPINE_PATH.write_text(existing.rstrip() + block + "\n", encoding="utf-8")


def validation_rows(
    sources: list[dict[str, Any]],
    zeroform: list[dict[str, Any]],
    gdot_components: list[dict[str, Any]],
    fallback: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    resolved = [row for row in sources if row["exists"] and row["needle_found"]]
    checks.append(("VAL3909_0_sources", "all source paths and needles resolve", len(resolved) == len(sources), f"{len(resolved)}/{len(sources)} sources resolved"))
    checks.append(("VAL3909_1_zeroform", "zeroform action and variation emitted", any(row["block_id"] == "ZF3909_0_action" for row in zeroform) and any(row["block_id"] == "ZF3909_1_variation_A3" for row in zeroform), "ZF action+variation"))
    checks.append(("VAL3909_2_gstar_component", "d_t ln Gstar component conditionally filled", any(row["component_id"] == "GDC3909_0_CG" and "CONDITIONALLY_ZERO" in str(row["status"]) for row in gdot_components), "GDC3909_0"))
    required_components = {"d_t ln G_*", "d_t ln M_eff", "d_t epsilon_mu/(1+epsilon_mu)", "d_t ln Z_Poisson", "d_t ln Z_frame"}
    checks.append(("VAL3909_3_components", "total Gdot components listed", required_components.issubset({str(row["component"]) for row in gdot_components}), f"{len(gdot_components)} components"))
    checks.append(("VAL3909_4_runner", "fallback runner includes partial zero and dry checks", any(row["runner_id"] == "GDF3909_1_partial_zero" for row in fallback) and any(row["runner_id"] == "GDF3909_4_dry_fail" for row in fallback), "partial+dry"))
    checks.append(("VAL3909_5_no_total_claim", "total Gdot remains blocked", any(row["decision_id"] == "DEC3909_1_total_Gdot" and "BLOCKED" in str(row["status"]) for row in decision), "DEC3909_1"))
    checks.append(("VAL3909_6_all_nonclaim", "all generated rows are nonclaim", all(str(row.get("valid_for_claim", row.get("claim_allowed", False))) == "False" for collection in [zeroform, gdot_components, fallback, decision] for row in collection), "valid_for_claim=false"))
    checks.append(("VAL3909_7_doc", "markdown checkpoint exists with zeroform variation", DOC_PATH.exists() and ZEROFORM_VARIATION in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3909_8_spine", "spine updated with 3909 block", SPINE_PATH.exists() and "BEGIN 3909 GSTAR ZEROFORM GDOT COMPONENT" in read_text(SPINE_PATH), rel(SPINE_PATH)))
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_parse_ok = True
    parse_details = []
    for path in csv_outputs:
        try:
            parse_details.append(f"{path.name}:{len(read_csv_rows(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parse_details.append(f"{path.name}:{exc}")
    checks.append(("VAL3909_9_csv_parse", "all generated CSV outputs parse", csv_parse_ok, "; ".join(parse_details)))
    formalization_hits = []
    if FWB.exists():
        formalization_hits = [
            path
            for path in FWB.rglob("*3909*")
            if path.is_file() and ("3909-Y5" in path.name or "P8_Y5_R2FR_3909" in path.name or "P8_Y5_BRR545_3909" in path.name)
        ]
    checks.append(("VAL3909_10_formalization_untouched", "no generated 3909 files appear in formalization-workbench", not formalization_hits, f"{len(formalization_hits)} hits"))
    pycache_hits = [path for path in (PCW / "scripts").rglob("__pycache__") if path.is_dir()]
    checks.append(("VAL3909_11_no_pycache", "scripts __pycache__ removed", not pycache_hits, f"{len(pycache_hits)} pycache dirs"))
    checks.append(("VAL3909_12_next_target", "next target attacks Meff drift", any("Meff-Hilbert-worldtube" in str(row["target_checkpoint"]) for row in next_rows(timestamp)), "3910 Meff"))
    return [
        {
            "check_id": check_id,
            "description": description,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for check_id, description, passed, detail in checks
    ]


def main() -> int:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    zeroform = zeroform_rows(timestamp)
    gdot_components = gdot_component_rows(timestamp)
    fallback = fallback_rows(timestamp)
    decision = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["zeroform"], zeroform)
    write_csv(OUTPUTS["gdot_components"], gdot_components)
    write_csv(OUTPUTS["fallback"], fallback)
    write_csv(OUTPUTS["decision"], decision)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, zeroform, gdot_components, fallback, decision, next_target, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, zeroform, gdot_components, fallback, decision, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_GSTAR_TIME_COMPONENT_ZEROFORM_MECHANISM_FILLED")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

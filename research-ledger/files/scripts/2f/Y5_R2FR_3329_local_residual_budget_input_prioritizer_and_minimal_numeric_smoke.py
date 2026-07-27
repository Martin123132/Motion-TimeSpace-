from __future__ import annotations

import csv
import hashlib
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3329-Y5-R2FR-local-residual-budget-input-prioritizer-and-minimal-numeric-smoke-under-AX1090.md"

SOURCES = [
    {
        "source_id": "SRC3329_0_3328_doc",
        "path": ROOT / "3328-Y5-R2FR-local-GR-residual-budget-and-promotion-map-under-AX1090.md",
        "role": "local residual budget and next target",
    },
    {
        "source_id": "SRC3329_1_3328_budget",
        "path": OUT / "P8_Y5_R2FR_3328_RESIDUAL_BUDGET_FORMULAS.csv",
        "role": "master residual formulas",
    },
    {
        "source_id": "SRC3329_2_3328_arena",
        "path": OUT / "P8_Y5_R2FR_3328_ARENA_PROMOTION_MAP.csv",
        "role": "arena formulas and blocking inputs",
    },
    {
        "source_id": "SRC3329_3_3328_inputs",
        "path": OUT / "P8_Y5_R2FR_3328_REQUIRED_INPUT_LEDGER.csv",
        "role": "required input ledger",
    },
    {
        "source_id": "SRC3329_4_3328_claims",
        "path": OUT / "P8_Y5_R2FR_3328_CLAIM_STATUS_LEDGER.csv",
        "role": "no-public-claim constraints",
    },
    {
        "source_id": "SRC3329_5_3327_envelope",
        "path": OUT / "P8_Y5_R2FR_3327_COMPOSITE_ENVELOPE.csv",
        "role": "epsilon_composite envelope",
    },
    {
        "source_id": "SRC3329_6_3327_inputs",
        "path": OUT / "P8_Y5_R2FR_3327_REQUIRED_NUMERIC_INPUTS.csv",
        "role": "composite numeric inputs",
    },
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3329_SOURCE_REGISTER.csv",
    "arena_choice": OUT / "P8_Y5_R2FR_3329_ARENA_SELECTION.csv",
    "priors": OUT / "P8_Y5_R2FR_3329_SMOKE_PRIORS.csv",
    "smoke": OUT / "P8_Y5_R2FR_3329_PPN_NUMERIC_SMOKE.csv",
    "sensitivity": OUT / "P8_Y5_R2FR_3329_PPN_SENSITIVITY_TABLE.csv",
    "priority": OUT / "P8_Y5_R2FR_3329_INPUT_PRIORITY.csv",
    "decision": OUT / "P8_Y5_R2FR_3329_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3329_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3329_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()
SMOKE_THRESHOLD_PPN = 1.0e-5


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 1200) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: compact(row.get(key, "")) for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parse_ok(path: Path) -> bool:
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def text_parse_ok(path: Path) -> bool:
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_parse_ok(path) if path.suffix.lower() == ".csv" else text_parse_ok(path)


def sha256_prefix(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()[:16]


def snapshot_tree(path: Path) -> dict[str, tuple[int, int]]:
    if not path.exists():
        return {}
    result: dict[str, tuple[int, int]] = {}
    for item in path.rglob("*"):
        if item.is_file():
            try:
                stat = item.stat()
            except OSError:
                continue
            result[str(item.relative_to(path))] = (stat.st_size, stat.st_mtime_ns)
    return result


def changed_count(before: dict[str, tuple[int, int]], after: dict[str, tuple[int, int]]) -> int:
    keys = set(before) | set(after)
    return sum(1 for key in keys if before.get(key) != after.get(key))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["path"]
        rows.append(
            {
                "source_id": source["source_id"],
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "sha256_prefix": sha256_prefix(path),
                "role": source["role"],
                "valid_for_claim": "false",
            }
        )
    return rows


def arena_selection_rows() -> list[dict[str, Any]]:
    return [
        {
            "arena": "PPN_local_GR",
            "selected_for_3329": "true",
            "reason": "smallest dimensionless smoke route; no range-dependent bound curve or material-composition model required for algebra stress-test",
            "main_formula": "R_PPN <= |R_Gamma_PPN| + C_PPN epsilon_eff^2 + epsilon_composite_PPN + epsilon_direct_PPN",
            "claim_status": "NONCLAIM_SMOKE_ONLY",
            "valid_for_claim": "false",
        },
        {
            "arena": "R10_short_range",
            "selected_for_3329": "false",
            "reason": "needs claim-ready alpha_bound(lambda), contact/source-size routing, and C_R10(lambda)",
            "main_formula": "alpha_psi(lambda) <= |R_Gamma_R10| + C_R10 epsilon_eff(lambda)^2 + epsilon_composite_R10(lambda)",
            "claim_status": "DEFER_UNTIL_BOUND_CURVE_AND_CONTACT_RULE",
            "valid_for_claim": "false",
        },
        {
            "arena": "WEP",
            "selected_for_3329": "false",
            "reason": "needs material response Delta q_AB and direct-vertex exclusion or material-tail bounds",
            "main_formula": "eta_AB <= |R_Gamma_WEP| + C_WEP epsilon_eff^2 |Delta q_AB| + epsilon_composite_WEP + epsilon_direct_WEP",
            "claim_status": "DEFER",
            "valid_for_claim": "false",
        },
        {
            "arena": "clocks_EM_Poynting",
            "selected_for_3329": "false",
            "reason": "needs clock normalization and EM/Poynting projection; useful after PPN budget behavior is understood",
            "main_formula": "R_clock <= |R_Gamma_clock| + C_clock epsilon_eff^2 + epsilon_EM_tail + epsilon_direct_EM",
            "claim_status": "DEFER",
            "valid_for_claim": "false",
        },
        {
            "arena": "orbital_Newton",
            "selected_for_3329": "false",
            "reason": "needs orbital threshold table and compact-source projection; good follow-up after PPN response coefficient",
            "main_formula": "R_orb <= |R_Gamma_orb| + C_orb epsilon_eff^2 + epsilon_composite_orb",
            "claim_status": "DEFER",
            "valid_for_claim": "false",
        },
    ]


def smoke_priors_rows() -> list[dict[str, Any]]:
    return [
        {
            "prior_id": "PRI3329_0_threshold",
            "quantity": "B_PPN_smoke",
            "value": f"{SMOKE_THRESHOLD_PPN:.3e}",
            "meaning": "illustrative dimensionless PPN residual ceiling for smoke algebra only",
            "source_status": "PLACEHOLDER_NOT_EMPIRICAL_CLAIM",
            "valid_for_claim": "false",
        },
        {
            "prior_id": "PRI3329_1_G_closure",
            "quantity": "epsilon_G_closure",
            "value": "0",
            "meaning": "measured-G closure is declared for smoke; no derivation of G implied",
            "source_status": "CLOSURE_ASSUMPTION",
            "valid_for_claim": "false",
        },
        {
            "prior_id": "PRI3329_2_direct_vertex",
            "quantity": "epsilon_direct",
            "value": "0 unless scenario explicitly turns it on",
            "meaning": "clean local branch excludes direct psi-matter/EM vertices",
            "source_status": "BRANCH_SIGNATURE",
            "valid_for_claim": "false",
        },
        {
            "prior_id": "PRI3329_3_ppn_response",
            "quantity": "C_PPN",
            "value": "1 to 1e8 grid",
            "meaning": "response coefficient sensitivity sweep",
            "source_status": "PLACEHOLDER_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "prior_id": "PRI3329_4_residual_floors",
            "quantity": "R_Gamma_PPN and epsilon_composite_PPN",
            "value": "0 to 1e-4 scenario grid",
            "meaning": "tests whether floor terms dominate before epsilon_eff matters",
            "source_status": "PLACEHOLDER_NONCLAIM",
            "valid_for_claim": "false",
        },
    ]


def smoke_scenario_inputs() -> list[dict[str, float | str]]:
    return [
        {
            "scenario_id": "SMOKE3329_0_optimistic_clean",
            "C_PPN": 1.0,
            "epsilon_eff": 1.0e-10,
            "epsilon_composite": 1.0e-18,
            "R_Gamma": 0.0,
            "epsilon_direct": 0.0,
        },
        {
            "scenario_id": "SMOKE3329_1_large_C_tiny_leak",
            "C_PPN": 1.0e6,
            "epsilon_eff": 1.0e-6,
            "epsilon_composite": 1.0e-12,
            "R_Gamma": 0.0,
            "epsilon_direct": 0.0,
        },
        {
            "scenario_id": "SMOKE3329_2_large_C_danger",
            "C_PPN": 1.0e6,
            "epsilon_eff": 1.0e-5,
            "epsilon_composite": 1.0e-12,
            "R_Gamma": 0.0,
            "epsilon_direct": 0.0,
        },
        {
            "scenario_id": "SMOKE3329_3_composite_floor_fail",
            "C_PPN": 1.0,
            "epsilon_eff": 1.0e-8,
            "epsilon_composite": 1.0e-4,
            "R_Gamma": 0.0,
            "epsilon_direct": 0.0,
        },
        {
            "scenario_id": "SMOKE3329_4_Gamma_floor_fail",
            "C_PPN": 1.0,
            "epsilon_eff": 1.0e-8,
            "epsilon_composite": 1.0e-12,
            "R_Gamma": 1.0e-4,
            "epsilon_direct": 0.0,
        },
        {
            "scenario_id": "SMOKE3329_5_direct_vertex_warning",
            "C_PPN": 1.0e2,
            "epsilon_eff": 1.0e-7,
            "epsilon_composite": 1.0e-10,
            "R_Gamma": 0.0,
            "epsilon_direct": 1.0e-6,
        },
    ]


def ppn_smoke_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for scenario in smoke_scenario_inputs():
        C_ppn = float(scenario["C_PPN"])
        epsilon_eff = float(scenario["epsilon_eff"])
        epsilon_composite = float(scenario["epsilon_composite"])
        r_gamma = float(scenario["R_Gamma"])
        epsilon_direct = float(scenario["epsilon_direct"])
        tree = C_ppn * epsilon_eff * epsilon_eff
        total = abs(r_gamma) + tree + epsilon_composite + epsilon_direct
        smoke_pass = total <= SMOKE_THRESHOLD_PPN
        dominant = max(
            [
                ("R_Gamma", abs(r_gamma)),
                ("tree_C_epsilon2", tree),
                ("epsilon_composite", epsilon_composite),
                ("epsilon_direct", epsilon_direct),
            ],
            key=lambda item: item[1],
        )[0]
        rows.append(
            {
                "scenario_id": scenario["scenario_id"],
                "C_PPN": f"{C_ppn:.6e}",
                "epsilon_eff": f"{epsilon_eff:.6e}",
                "tree_C_epsilon2": f"{tree:.6e}",
                "epsilon_composite": f"{epsilon_composite:.6e}",
                "R_Gamma": f"{r_gamma:.6e}",
                "epsilon_direct": f"{epsilon_direct:.6e}",
                "R_total": f"{total:.6e}",
                "B_PPN_smoke": f"{SMOKE_THRESHOLD_PPN:.6e}",
                "smoke_pass": bool_str(smoke_pass),
                "dominant_term": dominant,
                "interpretation": "nonclaim pass-like smoke" if smoke_pass else "nonclaim fail-like smoke",
                "valid_for_claim": "false",
            }
        )
    return rows


def ppn_sensitivity_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for C_ppn in [1.0, 1.0e2, 1.0e4, 1.0e6, 1.0e8]:
        for floor in [0.0, 1.0e-12, 1.0e-8, 1.0e-6, 1.0e-5]:
            available = SMOKE_THRESHOLD_PPN - floor
            epsilon_max = math.sqrt(available / C_ppn) if available > 0 else float("nan")
            rows.append(
                {
                    "row_id": f"SENS3329_C{C_ppn:.0e}_F{floor:.0e}",
                    "C_PPN": f"{C_ppn:.6e}",
                    "fixed_floor": f"{floor:.6e}",
                    "B_PPN_smoke": f"{SMOKE_THRESHOLD_PPN:.6e}",
                    "epsilon_eff_max": "" if math.isnan(epsilon_max) else f"{epsilon_max:.6e}",
                    "status": "NO_ROOM_FOR_TREE_TERM" if math.isnan(epsilon_max) else "SMOKE_THRESHOLD_FORMULA",
                    "valid_for_claim": "false",
                }
            )
    return rows


def input_priority_rows() -> list[dict[str, Any]]:
    return [
        {
            "priority_rank": 1,
            "input": "C_PPN response coefficient",
            "why_first": "tree term scales as C_PPN epsilon_eff^2; without C_PPN every epsilon_eff result is floating",
            "next_action": "derive/bound PPN projection coefficient from C_i operator formula",
            "valid_for_claim": "false",
        },
        {
            "priority_rank": 2,
            "input": "epsilon_eff_PPN",
            "why_first": "even large C_PPN is harmless if epsilon_eff is tiny; this controls the main tree channel",
            "next_action": "turn ell_s/epsilon_bg/boundary/aniso into a local PPN bound",
            "valid_for_claim": "false",
        },
        {
            "priority_rank": 3,
            "input": "epsilon_composite_PPN floor",
            "why_first": "composite floor can fail the smoke even when tree leakage is tiny",
            "next_action": "instantiate 3327 composite envelope for PPN",
            "valid_for_claim": "false",
        },
        {
            "priority_rank": 4,
            "input": "R_Gamma_PPN floor",
            "why_first": "any unsuppressed local Gamma/saturation residual dominates immediately",
            "next_action": "derive local Gamma silence or a conservative PPN bound",
            "valid_for_claim": "false",
        },
        {
            "priority_rank": 5,
            "input": "claim-ready PPN threshold table",
            "why_first": "needed before converting smoke into a test, but algebra can be stress-tested first",
            "next_action": "source real PPN bounds only after coefficient side is less foggy",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3329_0",
            "question": "Which arena should be smoked first?",
            "answer": "PPN_local_GR",
            "reason": "it uses the master local residual budget with dimensionless coefficients and avoids R10 range/contact data for the first stress-test",
            "next_action": "derive C_PPN and epsilon_eff_PPN before using real PPN data",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3329_1",
            "question": "What did the smoke reveal?",
            "answer": "floors matter as much as tree leakage",
            "reason": "large C_PPN can be tolerated if epsilon_eff is sufficiently small, but composite/Gamma/direct floors can fail immediately",
            "next_action": "prioritize C_PPN, epsilon_eff, then composite/Gamma floors",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3329_2",
            "question": "Can any smoke pass be used as evidence?",
            "answer": "no",
            "reason": "threshold and coefficients are placeholders; every row is valid_for_claim=false",
            "next_action": "use this only as a coefficient prioritizer",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3330-Y5-R2FR-PPN-response-coefficient-and-local-floor-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3330_PPN_response_coefficient_and_local_floor_bound.py",
            "objective": "derive or bound C_PPN and the local PPN floor terms R_Gamma_PPN, epsilon_eff_PPN, and epsilon_composite_PPN so the 3329 smoke budget can stop using placeholders",
            "must_include": "C_i to C_PPN projection; epsilon_eff_PPN from smoothing/boundary/aniso; composite PPN envelope; Gamma local silence or floor; no real PPN claim yet",
            "fallback_if_failed": "keep PPN as symbolic sensitivity and move to R10 data-bound acquisition only after C_i behavior is clearer",
            "valid_for_claim": "false",
        }
    ]


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    arena = arena_selection_rows()
    priors = smoke_priors_rows()
    smoke = ppn_smoke_rows()
    sensitivity = ppn_sensitivity_rows()
    priority = input_priority_rows()
    decisions = decision_rows()
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    fw_changed = changed_count(formalization_before, snapshot_tree(FW))
    checks = [
        {
            "check_id": "VAL3329_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": all(row["exists"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3329_1_sources_parse",
            "check": "all cited source paths parse",
            "passed": all(row["parse_ok"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3329_2_outputs_parse",
            "check": "all 3329 non-validation outputs parse",
            "passed": all(path.exists() and parse_ok(path) for path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3329_3_arena_selected",
            "check": "PPN is selected and R10 is explicitly deferred",
            "passed": any(row["arena"] == "PPN_local_GR" and row["selected_for_3329"] == "true" for row in arena)
            and any(row["arena"] == "R10_short_range" and row["selected_for_3329"] == "false" for row in arena),
            "detail": "",
        },
        {
            "check_id": "VAL3329_4_priors_nonclaim",
            "check": "all smoke priors are nonclaim",
            "passed": all(row["valid_for_claim"] == "false" for row in priors)
            and any(row["quantity"] == "B_PPN_smoke" for row in priors),
            "detail": "",
        },
        {
            "check_id": "VAL3329_5_smoke_mixed_results",
            "check": "smoke has pass-like and fail-like rows and all are nonclaim",
            "passed": any(row["smoke_pass"] == "true" for row in smoke)
            and any(row["smoke_pass"] == "false" for row in smoke)
            and all(row["valid_for_claim"] == "false" for row in smoke),
            "detail": "",
        },
        {
            "check_id": "VAL3329_6_sensitivity_ready",
            "check": "sensitivity table includes C_PPN grid and epsilon_eff_max formulas",
            "passed": any(row["C_PPN"] == "1.000000e+06" for row in sensitivity)
            and any(row["status"] == "NO_ROOM_FOR_TREE_TERM" for row in sensitivity),
            "detail": "",
        },
        {
            "check_id": "VAL3329_7_priority",
            "check": "input priority starts with C_PPN and epsilon_eff",
            "passed": priority[0]["input"] == "C_PPN response coefficient"
            and priority[1]["input"] == "epsilon_eff_PPN",
            "detail": "",
        },
        {
            "check_id": "VAL3329_8_no_evidence_claim",
            "check": "decision ledger says smoke pass is not evidence",
            "passed": any(row["answer"] == "no" and "valid_for_claim=false" in row["reason"] for row in decisions),
            "detail": "",
        },
        {
            "check_id": "VAL3329_9_next_PPN_coefficients",
            "check": "next target is PPN response coefficient and local floors",
            "passed": any("C_PPN" in row["objective"] and "epsilon_eff_PPN" in row["must_include"] for row in next_target_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3329_10_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": fw_changed == 0,
            "detail": f"formalization_changed_count={fw_changed}",
        },
    ]
    overall = all(bool(check["passed"]) for check in checks)
    checks.append(
        {
            "check_id": "VAL3329_11_overall",
            "check": "3329 validation overall",
            "passed": overall,
            "detail": "all required checks passed" if overall else "one or more checks failed",
        }
    )
    for check in checks:
        check["passed"] = bool_str(bool(check["passed"]))
    return checks


def render_doc() -> str:
    smoke_passes = sum(1 for row in ppn_smoke_rows() if row["smoke_pass"] == "true")
    smoke_fails = sum(1 for row in ppn_smoke_rows() if row["smoke_pass"] == "false")
    lines: list[str] = [
        "# 3329 - Local residual budget input prioritizer and minimal numeric smoke under AX1090",
        "",
        f"Run UTC: `{RUN_UTC}`",
        "",
        "## Verdict",
        "",
        "3329 runs the first numeric smoke on the local residual budget, using `PPN_local_GR` because it is the smallest clean dimensionless arena.",
        "",
        "This is **not evidence** and not a PPN pass. The threshold is an illustrative placeholder:",
        "",
        f"`B_PPN_smoke = {SMOKE_THRESHOLD_PPN:.1e}`.",
        "",
        "The smoke equation is",
        "",
        "`R_PPN <= |R_Gamma_PPN| + C_PPN epsilon_eff_PPN^2 + epsilon_composite_PPN + epsilon_direct_PPN`.",
        "",
        f"The scenario grid gives {smoke_passes} pass-like and {smoke_fails} fail-like nonclaim rows. The useful result is qualitative: if residual floors are zero/tiny, even large `C_PPN` can be tolerable when `epsilon_eff` is small; if `epsilon_composite_PPN`, `R_Gamma_PPN`, or direct vertices have floors near the smoke threshold, the branch fails regardless of the tree term.",
        "",
        "So the next mathematical target is not broad wandering. It is `C_PPN` plus the three local floors: `epsilon_eff_PPN`, `epsilon_composite_PPN`, and `R_Gamma_PPN`.",
        "",
        "## Source Register",
        "",
    ]
    for row in source_register_rows():
        lines.append(
            f"- `{row['source_id']}`: `{row['path']}` exists={row['exists']} parse_ok={row['parse_ok']} role={row['role']}"
        )
    sections = [
        ("Arena Selection", arena_selection_rows(), "arena"),
        ("Smoke Priors", smoke_priors_rows(), "prior_id"),
        ("PPN Numeric Smoke", ppn_smoke_rows(), "scenario_id"),
        ("PPN Sensitivity Table", ppn_sensitivity_rows(), "row_id"),
        ("Input Priority", input_priority_rows(), "priority_rank"),
        ("Decision Ledger", decision_rows(), "decision_id"),
        ("Next Target", next_target_rows(), "target_doc"),
    ]
    for title, rows, key_name in sections:
        lines.extend(["", f"## {title}", ""])
        for row in rows:
            label = row.get(key_name, "")
            body = "; ".join(f"{key}={value}" for key, value in row.items() if key != key_name)
            lines.append(f"- `{label}`: {body}")
    lines.extend(
        [
            "",
            "## Test Notes",
            "",
            "- This checkpoint is private and nonclaim.",
            "- All thresholds and coefficients are smoke placeholders.",
            "- Pass-like rows are not evidence; fail-like rows are diagnostic only.",
            "- The purpose is input prioritization for the local residual budget.",
            "- `formalization-workbench` is not modified.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    formalization_before = snapshot_tree(FW)
    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUTS["sources"], source_register_rows())
    write_csv(OUTPUTS["arena_choice"], arena_selection_rows())
    write_csv(OUTPUTS["priors"], smoke_priors_rows())
    write_csv(OUTPUTS["smoke"], ppn_smoke_rows())
    write_csv(OUTPUTS["sensitivity"], ppn_sensitivity_rows())
    write_csv(OUTPUTS["priority"], input_priority_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before))
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()

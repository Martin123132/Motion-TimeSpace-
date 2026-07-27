from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_GK_STRESS_BOUND_LOCAL_ARENA_PROJECTION_RUNNER_2473"
CHECKPOINT_ID = "2473"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC = ROOT / "2473-Y5-R2FR-GK-stress-bound-local-arena-projection-runner.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_GK_STRESS_BOUND_2473_SOURCE_REGISTER.csv",
    "residual_parameters": OUT / "P8_Y5_GK_STRESS_BOUND_2473_RESIDUAL_PARAMETERS.csv",
    "arena_projection": OUT / "P8_Y5_GK_STRESS_BOUND_2473_ARENA_PROJECTION_ROWS.csv",
    "missing_coefficients": OUT / "P8_Y5_GK_STRESS_BOUND_2473_MISSING_COEFFICIENT_LEDGER.csv",
    "runner_schema": OUT / "P8_Y5_GK_STRESS_BOUND_2473_NONCLAIM_RUNNER_SCHEMA.csv",
    "smoke_cases": OUT / "P8_Y5_GK_STRESS_BOUND_2473_SMOKE_CASES.csv",
    "claim_gates": OUT / "P8_Y5_GK_STRESS_BOUND_2473_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_GK_STRESS_BOUND_2473_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_GK_STRESS_BOUND_2473_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_GK_STRESS_BOUND_2473_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2473_VALIDATION.csv",
}

COPY_TARGETS = {
    "local_projection_schema": LOCAL_BOUNDS / "GK_stress_bound_local_projection_schema_2473_NONCLAIM.csv",
    "missing_coefficients": LOCAL_BOUNDS / "GK_stress_bound_missing_coefficients_2473_NONCLAIM.csv",
    "runner_queue": QUEUE / "JR2473_GK_STRESS_BOUND_RUNNER_SCHEMA_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2473_00_2472_doc",
        "source_path": ROOT / "2472-Y5-R2FR-parent-sign-origin-and-boundary-topology-nohair-gate.md",
        "needles": ["DEM2472_0_demote_current_metric_branch", "NEXT2472_0_selected", "VAL2472_OVERALL"],
        "role": "handoff demoting local metric branch to stress-bound only",
    },
    {
        "source_id": "SRC2473_01_2472_demotion",
        "source_path": OUT / "P8_Y5_GK_PARENT_SIGN_2472_STRESS_BOUND_DEMOTION_ROUTE.csv",
        "needles": ["DEM2472_1_bound_quantity", "DEM2472_2_needed_coefficients", "MISSING_NUMERIC_INPUTS"],
        "role": "machine-readable stress-bound demotion route",
    },
    {
        "source_id": "SRC2473_02_2471_bound",
        "source_path": OUT / "P8_Y5_GK_OPERATOR_2471_STRESS_BOUND_BRANCH.csv",
        "needles": ["SBB2471_0_defect", "SBB2471_2_metric_bound", "SBB2471_3_data_gate"],
        "role": "stress bound formula handoff",
    },
    {
        "source_id": "SRC2473_03_2469_ppn",
        "source_path": OUT / "P8_Y5_GK_STRESS_2469_PPN_RESIDUAL_LEDGER.csv",
        "needles": ["PPN2469_0_residual_source", "PPN2469_2_hair_bound", "DEFER_NUMERIC_TEST"],
        "role": "PPN/local metric residual source ledger",
    },
    {
        "source_id": "SRC2473_04_2470_failures",
        "source_path": OUT / "P8_Y5_GK_NOHAIR_2470_FAILURE_MODES.csv",
        "needles": ["FAIL2470_3_boundary_hair", "FAIL2470_4_topological_hair", "FAIL2470_5_projector_hiding"],
        "role": "residual defect sources",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row() -> dict[str, Any]:
    return {"timestamp_utc": stamp(), "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID, "valid_for_claim": False, "claim_allowed": False}


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    columns: list[str] = []
    for row in rows:
        for key in row:
            if key not in columns:
                columns.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def source_register() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCES:
        path = Path(source["source_path"])
        exists = path.exists()
        missing: list[str] = []
        if exists:
            text = read_text(path)
            missing = [needle for needle in source["needles"] if needle not in text]
        else:
            missing = list(source["needles"])
        rows.append({**base_row(), "source_id": source["source_id"], "source_path": str(path), "exists": exists, "missing_needles": ";".join(missing), "source_pass": exists and not missing, "role": source["role"]})
    return rows


def residual_parameter_rows() -> list[dict[str, Any]]:
    rows = [
        ("RPAR2473_0_energy_norm", "E_GK_bound", "C_B*boundary_flux + C_S*source_tail + C_X*negative_mode_defect + C_H*topology_hair_amplitude + C_P*projector_leak", "dimensionless_or_energy_norm", "nonclaim aggregate stress-energy control norm", "MISSING_COEFFICIENTS"),
        ("RPAR2473_1_boundary_flux", "boundary_flux", "norm of A/Gamma/Khat boundary flux through local collar", "arena_norm", "captures unsilenced boundary hair", "MISSING_SOURCE"),
        ("RPAR2473_2_source_tail", "source_tail", "matter/GK support outside ideal worldtube", "arena_norm", "captures noncompact source leakage", "MISSING_SOURCE"),
        ("RPAR2473_3_negative_mode_defect", "negative_mode_defect", "max(0,c_AG^2-m_A2*Z_G) plus ghost/tachyon sign defects", "operator_defect", "captures failed coercivity", "MISSING_PARENT_SIGNS"),
        ("RPAR2473_4_topology_hair", "topology_hair_amplitude", "harmonic/topological GK mode amplitude", "arena_norm", "captures q_loc=0 but stressful hair", "MISSING_TOPOLOGY_LEDGER"),
        ("RPAR2473_5_projector_leak", "projector_leak", "nonprojected residual hidden by P_loc", "arena_norm", "captures projection mismatch", "MISSING_PROJECTOR_DESCENT"),
        ("RPAR2473_6_metric_response", "C_metric", "linearized metric Green/response coefficient", "arena_specific", "maps stress residual to observable metric deviation", "MISSING_ARENA_PROJECTION"),
    ]
    return [{**base_row(), "parameter_id": i, "symbol": s, "definition": d, "units": u, "role": r, "status": st} for i, s, d, u, r, st in rows]


def arena_projection_rows() -> list[dict[str, Any]]:
    rows = [
        ("ARENA2473_R10", "R10_short_range", "alpha_lambda_residual", "alpha_GK(lambda)=K_R10(lambda)*E_GK_bound", "needs R10 kernel, lambda mapping, source geometry", "valid_for_claim=false"),
        ("ARENA2473_PPN", "PPN_solar_system", "gamma_minus_1_beta_minus_1_precession", "delta_PPN <= K_PPN*C_metric*E_GK_bound", "needs metric response, solar-system boundary/topology assumptions", "valid_for_claim=false"),
        ("ARENA2473_CLOCK", "clock_redshift_time", "delta_clock_rate", "delta_clock <= K_clock*C_metric*E_GK_bound + K_tau*clock_exchange_leak", "needs tau-sector projection and clock data mapping", "valid_for_claim=false"),
        ("ARENA2473_ORBITAL", "orbital_dynamics", "delta_acceleration_or_precession", "delta_orbit <= K_orb*C_metric*E_GK_bound", "must not use fitted GM as source definition", "valid_for_claim=false"),
        ("ARENA2473_WEP", "WEP_composition", "eta_residual", "eta_GK <= K_WEP*species_leak*E_GK_bound", "needs composition coupling audit; Hilbert route should make species_leak zero", "valid_for_claim=false"),
    ]
    return [{**base_row(), "arena_id": i, "arena": a, "observable": obs, "projection_formula": formula, "missing_inputs": miss, "status": st} for i, a, obs, formula, miss, st in rows]


def missing_coefficient_rows() -> list[dict[str, Any]]:
    rows = [
        ("MISS2473_0_CB", "C_B", "boundary flux to energy coefficient", "needed for all arenas", "MISSING_PARENT_BOUNDARY_THEOREM"),
        ("MISS2473_1_CS", "C_S", "source tail to energy coefficient", "needed for source support leakage", "MISSING_SOURCE_SUPPORT_BOUND"),
        ("MISS2473_2_CX", "C_X", "negative mode defect to energy coefficient", "needed if coercivity fails", "MISSING_PARENT_SIGNS"),
        ("MISS2473_3_CH", "C_H", "topological hair to energy coefficient", "needed for harmonic/topology modes", "MISSING_TOPOLOGY_LEDGER"),
        ("MISS2473_4_CP", "C_P", "projector leak to stress coefficient", "needed because P_loc may hide residuals", "MISSING_PROJECTOR_DESCENT"),
        ("MISS2473_5_Cmetric", "C_metric", "stress to metric/observable response", "arena-specific local Green coefficient", "MISSING_ARENA_PROJECTION"),
        ("MISS2473_6_Karena", "K_R10,K_PPN,K_clock,K_orb,K_WEP", "observable kernels", "needed for comparisons to data", "MISSING_ARENA_KERNELS"),
        ("MISS2473_7_thresholds", "arena_bound", "external experimental/theory bounds", "needed for pass/fail comparisons", "MISSING_BOUND_DATA"),
    ]
    return [{**base_row(), "missing_id": i, "coefficient": c, "meaning": m, "why_needed": why, "status": st} for i, c, m, why, st in rows]


def runner_schema_rows() -> list[dict[str, Any]]:
    rows = [
        ("SCHEMA2473_0_input_parameters", "inputs", "arena_id,E_GK_bound,C_metric,K_arena,arena_bound,valid_for_claim,source_path", "all numeric rows must have source_path and units", "NONCLAIM_SCHEMA"),
        ("SCHEMA2473_1_prediction", "prediction", "residual_predicted=K_arena*C_metric*E_GK_bound plus arena-specific leak terms", "computed only when all numeric inputs present", "NONCLAIM_SCHEMA"),
        ("SCHEMA2473_2_pass_rule", "pass_rule", "abs(residual_predicted)<=arena_bound", "pass is compatibility only, not local-GR derivation", "NONCLAIM_SCHEMA"),
        ("SCHEMA2473_3_block_rule", "block_rule", "if any MISSING_* or valid_for_claim=false then claim_allowed=false", "default private guardrail", "PASS_GUARDRAIL"),
        ("SCHEMA2473_4_no_shortcuts", "forbidden", "no fitted GM, no M_H_ref reuse, no no-hair promotion, no plateau axiom", "prevents circular local claims", "PASS_GUARDRAIL"),
    ]
    return [{**base_row(), "schema_id": i, "field_group": g, "schema": schema, "acceptance_rule": rule, "status": st} for i, g, schema, rule, st in rows]


def smoke_case_rows() -> list[dict[str, Any]]:
    rows = [
        ("SMOKE2473_0_all_missing", "all arenas with placeholder coefficients", "BLOCKED", "runner must report missing inputs and claim_allowed=false"),
        ("SMOKE2473_1_numeric_nonclaim", "toy numeric coefficients with valid_for_claim=false", "COMPUTE_BUT_NONCLAIM", "schema arithmetic works but no evidence claim"),
        ("SMOKE2473_2_bad_units", "positive numeric values but unrecognized units", "BLOCKED", "unit parser must reject"),
        ("SMOKE2473_3_fitted_GM_flag", "orbital row uses fitted GM as source", "REJECTED", "anti-circularity guardrail"),
        ("SMOKE2473_4_future_claim", "all coefficients numeric, sourced, units valid, valid_for_claim=true", "FUTURE_ONLY", "not expected in 2473"),
    ]
    return [{**base_row(), "smoke_id": i, "case": c, "expected_status": st, "purpose": p} for i, c, st, p in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2473_0_schema", "stress-bound local arena schema exists.", "PASS_AS_SCHEMA", "projection rows and runner schema written", True, False),
        ("GATE2473_1_numeric_inputs", "all numeric coefficients are sourced.", "BLOCKED", "missing coefficient ledger is active", False, False),
        ("GATE2473_2_local_compatibility", "stress-bound branch passes local tests.", "BLOCKED", "no numeric sourced arena projections yet", False, False),
        ("GATE2473_3_local_GR", "local GR/PPN branch is derived.", "BLOCKED", "stress-bound compatibility cannot replace derivation", False, False),
        ("GATE2473_4_no_GitHub", "No public/GitHub update.", "PASS_GUARDRAIL", "private nonclaim scaffold only", True, False),
    ]
    return [{**base_row(), "gate_id": i, "claim": c, "gate_status": st, "reason": r, "gate_pass": gp, "claim_allowed": ca} for i, c, st, r, gp, ca in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2473_0_schema_first", "Build schema before numeric claims.", "coefficient sources are missing", "prevents false precision"),
        ("DEC2473_1_keep_nonclaim", "Keep all 2473 rows valid_for_claim=false.", "stress-bound branch is a compatibility scaffold only", "claim discipline"),
        ("DEC2473_2_next", "Next build the dry-run calculator and placeholder rejection tests.", "schema is ready; runner should enforce missing-input gates", "2474 selected"),
    ]
    return [{**base_row(), "decision_id": i, "decision": d, "reason": r, "effect": e} for i, d, r, e in rows]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            **base_row(),
            "route_id": "NEXT2473_0_selected",
            "selection_status": "selected",
            "target_file": "2474-Y5-R2FR-GK-stress-bound-runner-dry-run-and-placeholder-rejection.md",
            "target_script": "scripts/Y5_R2FR_GK_stress_bound_runner_dry_run_and_placeholder_rejection_2474.py",
            "task": "implement a small dry-run calculator over the 2473 schema that computes toy nonclaim rows but blocks all claim rows with missing coefficients, bad units, fitted GM, or valid_for_claim=false",
            "acceptance_target": "dry-run CSV, placeholder rejection ledger, toy arithmetic smoke, and claim gates",
            "guardrails": "no local-GR claim; no fitted GM; no M_H_ref reuse; no plateau axiom; no GitHub",
        }
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    for target in COPY_TARGETS.values():
        target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(OUTPUTS["arena_projection"], COPY_TARGETS["local_projection_schema"])
    shutil.copyfile(OUTPUTS["missing_coefficients"], COPY_TARGETS["missing_coefficients"])
    shutil.copyfile(OUTPUTS["runner_schema"], COPY_TARGETS["runner_queue"])
    source_map = {
        "local_projection_schema": OUTPUTS["arena_projection"],
        "missing_coefficients": OUTPUTS["missing_coefficients"],
        "runner_queue": OUTPUTS["runner_schema"],
    }
    return [{**base_row(), "copy_id": cid, "source_path": str(source_map[cid]), "target_path": str(target), "source_exists": source_map[cid].exists(), "target_exists": target.exists()} for cid, target in COPY_TARGETS.items()]


def csv_row_count(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as handle:
        return len(list(csv.DictReader(handle)))


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, status: bool, notes: str, detail: str = "") -> None:
        rows.append({**base_row(), "check_id": check_id, "status": "PASS" if status else "FAIL", "notes": notes, "detail": detail})

    add("VAL2473_00_sources_exist", all(row["source_pass"] is True or str(row["source_pass"]) == "True" for row in data["sources"]), "all cited source paths exist and needles are present")
    add("VAL2473_01_parameters_written", len(data["parameters"]) >= 7, "residual parameters written")
    add("VAL2473_02_arenas_written", len(data["arenas"]) >= 5 and all(row["status"] == "valid_for_claim=false" for row in data["arenas"]), "arena projections written as nonclaim")
    add("VAL2473_03_missing_ledger", len(data["missing"]) >= 8 and all(row["status"].startswith("MISSING") for row in data["missing"]), "missing coefficient ledger active")
    add("VAL2473_04_schema_guardrails", any(row["schema_id"] == "SCHEMA2473_3_block_rule" and row["status"] == "PASS_GUARDRAIL" for row in data["schema"]), "claim blocking schema written")
    add("VAL2473_05_smoke_cases", len(data["smoke"]) >= 5, "smoke cases written")
    add("VAL2473_06_claim_gates_safe", all(row["claim_allowed"] is False for row in data["gates"]), "no claim gate allows local-GR/PPN claim")
    add("VAL2473_07_next_target_written", bool(data["next"]) and data["next"][0]["route_id"] == "NEXT2473_0_selected", "2474 dry-run runner selected")
    add("VAL2473_08_branch_copies", all(row["source_exists"] and row["target_exists"] for row in data["copies"]), "nonclaim branch copies exist")
    markers = ("2473-Y5", "P8_Y5_GK_STRESS_BOUND_2473", "P8_Y5_BRR545_2473", "JR2473")
    formal_hits = [path for path in FORMALIZATION.rglob("*") if path.is_file() and any(marker in path.name for marker in markers)] if FORMALIZATION.exists() else []
    add("VAL2473_09_no_formalization_artifacts", not formal_hits, "no 2473 artifacts were written to formalization-workbench", ";".join(str(path) for path in formal_hits))
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        try:
            count = csv_row_count(path)
            add(f"VAL2473_CSV_{path.stem}", count > 0, f"CSV parses with {count} rows", str(path))
        except Exception as exc:
            add(f"VAL2473_CSV_{path.stem}", False, f"CSV parse failed: {exc}", str(path))
    for copy_id, path in COPY_TARGETS.items():
        try:
            count = csv_row_count(path)
            add(f"VAL2473_COPY_CSV_{copy_id}", count > 0, f"copy CSV parses with {count} rows", str(path))
        except Exception as exc:
            add(f"VAL2473_COPY_CSV_{copy_id}", False, f"copy CSV parse failed: {exc}", str(path))
    add("VAL2473_OVERALL", all(row["status"] == "PASS" for row in rows), "2473 builds nonclaim stress-bound local arena projection scaffold and selects dry-run rejection runner")
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2473 Y5 R2FR GK Stress-bound Local Arena Projection Runner",
        "",
        "**Status:** nonclaim projection scaffold written. Since parent sign/no-hair is not currently proved, the active local branch is a stress-bound compatibility scaffold for R10, PPN, clocks, orbital dynamics and WEP. Every row remains `valid_for_claim=false` until all coefficients, units, sources and arena kernels are real.",
        "",
        "**Meaning:** this does not derive local GR. It creates the disciplined test plumbing for the fallback route: if GK stress is not forced to zero, quantify how badly it can leak into each local arena.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Residual Parameters",
        markdown_table(data["parameters"], ["parameter_id", "symbol", "definition", "units", "role", "status"]),
        "",
        "## Arena Projection Rows",
        markdown_table(data["arenas"], ["arena_id", "arena", "observable", "projection_formula", "missing_inputs", "status"]),
        "",
        "## Missing Coefficient Ledger",
        markdown_table(data["missing"], ["missing_id", "coefficient", "meaning", "why_needed", "status"]),
        "",
        "## Nonclaim Runner Schema",
        markdown_table(data["schema"], ["schema_id", "field_group", "schema", "acceptance_rule", "status"]),
        "",
        "## Smoke Cases",
        markdown_table(data["smoke"], ["smoke_id", "case", "expected_status", "purpose"]),
        "",
        "## Claim Gates",
        markdown_table(data["gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    data = {
        "sources": source_register(),
        "parameters": residual_parameter_rows(),
        "arenas": arena_projection_rows(),
        "missing": missing_coefficient_rows(),
        "schema": runner_schema_rows(),
        "smoke": smoke_case_rows(),
        "gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }
    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["residual_parameters"], data["parameters"])
    write_csv(OUTPUTS["arena_projection"], data["arenas"])
    write_csv(OUTPUTS["missing_coefficients"], data["missing"])
    write_csv(OUTPUTS["runner_schema"], data["schema"])
    write_csv(OUTPUTS["smoke_cases"], data["smoke"])
    write_csv(OUTPUTS["claim_gates"], data["gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])
    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])
    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)
    print(f"wrote {DOC}")
    for key, path in OUTPUTS.items():
        print(f"wrote {key}: {path}")
    for key, path in COPY_TARGETS.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()

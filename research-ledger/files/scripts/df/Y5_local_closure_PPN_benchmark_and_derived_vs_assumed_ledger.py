from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1556-Y5-local-closure-PPN-benchmark-and-derived-vs-assumed-ledger.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1555_doc": ROOT / "1555-Y5-gauge-noether-zero-charge-qsector-origin-audit.md",
    "1555_validation": OUT / "P8_Y5_BRR545_1555_VALIDATION.csv",
    "1555_next": OUT / "P8_Y5_PARENT_QLOC_1555_NEXT_TARGET.csv",
    "1555_closure": OUT / "P8_Y5_PARENT_QLOC_1555_LOCAL_CLOSURE_LEDGER.csv",
    "1555_contract": OUT / "P8_Y5_PARENT_QLOC_1555_FIRST_CLASS_CONSTRAINT_CONTRACT.csv",
    "1555_audit": OUT / "P8_Y5_PARENT_QLOC_1555_GAUGE_NOETHER_ROUTE_AUDIT.csv",
    "13_doc": ROOT / "13-local-closure-PPN-benchmark.md",
    "10_doc": ROOT / "10-observer-map-symplectic-contract.md",
    "06_doc": ROOT / "06-reciprocal-charge-source-neutrality.md",
    "02_doc": ROOT / "02-motion-load-local-GR-reduction.md",
    "local_bound_claims": LOCAL_BOUNDS / "local_bound_claims.csv",
}

NEEDLES = {
    "13_doc": ["local_closure_ppn_benchmark_valid_control_not_derivation", "gamma = 1", "beta = 1"],
    "10_doc": ["gamma - 1 = 0 after R_AB=0", "beta - 1 = 0", "Bianchi-like consistency identity"],
    "1555_doc": ["closure benchmark", "not a derived GR/Newton limit"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1556_SOURCE_REGISTER.csv"
CLOSURE_ASSUMPTIONS = OUT / "P8_Y5_PARENT_QLOC_1556_CLOSURE_ASSUMPTION_LEDGER.csv"
DERIVED_VS_ASSUMED = OUT / "P8_Y5_PARENT_QLOC_1556_DERIVED_VS_ASSUMED_LEDGER.csv"
PPN_BENCHMARK = OUT / "P8_Y5_PARENT_QLOC_1556_PPN_BENCHMARK_REQUIREMENTS.csv"
OBSERVABLE_CONTROLS = OUT / "P8_Y5_PARENT_QLOC_1556_OBSERVABLE_CONTROL_VALUES_NONCLAIM.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1556_CLOSURE_BENCHMARK_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1556_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1556_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1556_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1556_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1556"
QUAR_ASSUMPTIONS = QUARANTINE / "CLOSURE_ASSUMPTION_LEDGER_NONCLAIM.csv"
QUAR_DERIVED = QUARANTINE / "DERIVED_VS_ASSUMED_LEDGER_NONCLAIM.csv"
QUAR_PPN = QUARANTINE / "PPN_BENCHMARK_REQUIREMENTS_NONCLAIM.csv"
QUAR_OBS = QUARANTINE / "OBSERVABLE_CONTROL_VALUES_NONCLAIM.csv"
QUAR_RUNNER = QUARANTINE / "CLOSURE_BENCHMARK_RUNNER_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "DECISION_NONCLAIM.csv"
BRANCH_ASSUMPTIONS = BRANCH_RESIDUALS / "closure_assumption_ledger_nonclaim_1556.csv"
BRANCH_DERIVED = BRANCH_RESIDUALS / "derived_vs_assumed_ledger_nonclaim_1556.csv"
BRANCH_PPN = BRANCH_RESIDUALS / "PPN_benchmark_requirements_nonclaim_1556.csv"
BRANCH_OBS = BRANCH_RESIDUALS / "observable_control_values_nonclaim_1556.csv"
BRANCH_RUNNER = BRANCH_RESIDUALS / "closure_benchmark_runner_nonclaim_1556.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "closure_benchmark_decision_nonclaim_1556.csv"


def flags() -> dict[str, bool]:
    return {
        "numeric_value_present": False,
        "source_backed": False,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def source_list(*keys: str) -> str:
    return "; ".join(rel(SOURCE_FILES[key]) for key in keys)


def file_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    return all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    claim_keys = [
        "numeric_value_present",
        "source_backed",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "accepted_for_scoring",
        "passes_for_claim",
    ]
    for path in paths:
        for row in read_csv(path):
            for key in claim_keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for index, (key, path) in enumerate(SOURCE_FILES.items()):
        needles = NEEDLES.get(key, [])
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1556_{index}_{key}",
                "source_path": rel(path),
                "exists": path.exists(),
                "needle_found": file_contains(path, needles) if needles else True,
                "needles": "; ".join(needles),
                "purpose": "evidence for local closure PPN benchmark and derived-vs-assumed ledger",
                **flags(),
            }
        )
    return rows


def closure_assumption_rows() -> list[dict[str, Any]]:
    rows = [
        ("ASM1556_0_clock_load", "T^2=1-L", "assumed_or_prior_local_clock_load", "Newtonian clock/load side is used as the weak-field scaffold", "source 13/02"),
        ("ASM1556_1_reciprocity", "R_AB=ln(T^2 S)=0", "explicit_closure_assumption", "not parent-derived after 1555", "source 1555 closure ledger"),
        ("ASM1556_2_spatial_routing", "S=1/T^2=1/(1-L)", "derived_inside_closure", "follows algebraically from ASM1556_0 and ASM1556_1", "closure algebra only"),
        ("ASM1556_3_reciprocal_charge", "Q_R=0", "explicit_closure_assumption", "zero-charge theorem failed; kept as closure", "source 1555 gauge/Noether audit"),
        ("ASM1556_4_areal_radius", "angular sector=r^2 dOmega^2", "benchmark_coordinate_condition", "defines the local control lane but must not be used to derive AB=1", "source 12/13"),
        ("ASM1556_5_matter_universality", "all matter uses same observer coframe", "test_required_not_derived_here", "needed for WEP/clocks/PPN interpretation", "source 10"),
        ("ASM1556_6_claim_policy", "closure is not derivation", "guard", "benchmark may test deviations but cannot prove parent theory", "source 1555"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "assumption_id": assumption_id,
            "statement": statement,
            "classification": classification,
            "reason": reason,
            "evidence_note": evidence_note,
            "source_paths": source_list("13_doc", "1555_closure", "10_doc"),
            **flags(),
        }
        for assumption_id, statement, classification, reason, evidence_note in rows
    ]


def derived_vs_assumed_rows() -> list[dict[str, Any]]:
    rows = [
        ("DVA1556_0_p_equals_1", "p=1", "DERIVED_WITHIN_CLOSURE", "from T^2=1-L and R_AB=0", "not parent-derived"),
        ("DVA1556_1_gamma", "gamma=1", "DERIVED_WITHIN_CLOSURE", "spatial curvature lane p=1 gives gamma=1", "only under closure"),
        ("DVA1556_2_beta", "beta=1", "BENCHMARK_CONTROL_VALUE", "accepted in the Schwarzschild-equivalent control lane", "not derived by MTS parent action"),
        ("DVA1556_3_Newton", "Newtonian acceleration", "TEST_REQUIRED", "T^2 weak-field term must produce correct slow-particle acceleration", "requires source normalization/Poisson bridge"),
        ("DVA1556_4_conservation", "Bianchi-like consistency", "TEST_REQUIRED", "field equations must imply conservation identity", "not supplied by closure"),
        ("DVA1556_5_matter", "universal matter coupling", "TEST_REQUIRED", "same coframe for clocks, matter, photons, and orbital readouts", "not supplied by closure"),
        ("DVA1556_6_source_norm", "measured GM/source normalization", "TEST_REQUIRED", "same source charge must feed Poisson/orbit/PPN", "not supplied by closure"),
        ("DVA1556_7_tracefree", "tracefree metric transfer", "BLOCKED_OUTSIDE_SCALAR_CLOSURE", "scalar reciprocity does not fix tracefree tensor map", "requires separate metric/coframe definition"),
        ("DVA1556_8_parent_origin", "R_AB=0 parent derivation", "BLOCKED_NOT_DERIVED", "gauge/Noether/phase-volume attempts failed", "future first-class constraint only"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "ledger_id": ledger_id,
            "quantity": quantity,
            "status": status,
            "basis": basis,
            "limitation": limitation,
            "source_paths": source_list("13_doc", "10_doc", "1555_audit", "1555_contract"),
            **flags(),
        }
        for ledger_id, quantity, status, basis, limitation in rows
    ]


def ppn_benchmark_rows() -> list[dict[str, Any]]:
    rows = [
        ("PPN1556_0_gamma", "gamma_minus_1", "0 under R_AB=0 closure", "dimensionless", "closure_control", "Cassini/local bound row can test deviations, not derivation"),
        ("PPN1556_1_beta", "beta_minus_1", "0 in exact Schwarzschild-equivalent control lane", "dimensionless", "benchmark_control_not_parent_derived", "second-order weak-field source closure still required"),
        ("PPN1556_2_alpha1", "alpha1", "0 only if no preferred-frame/shadow-frame residuals", "dimensionless", "test_required", "frame/coframe descent not proven by closure"),
        ("PPN1556_3_alpha2", "alpha2", "0 only if no spin/preferred-frame residuals", "dimensionless", "test_required", "not handled by scalar R_AB closure"),
        ("PPN1556_4_alpha3_xi", "alpha3,xi", "0 only if boundary/source fluxes vanish", "dimensionless", "test_required", "boundary/no-charge/source-normalization gates remain open"),
        ("PPN1556_5_Gdot", "Gdot/G", "0 only if source normalization is time-stationary", "yr^-1", "test_required", "measured-GM/source-normalization theorem missing"),
        ("PPN1556_6_R10", "alpha(lambda)", "0 only if no finite-range q/source hair survives", "dimensionless curve", "test_required", "closure says nothing about all retained residual sectors"),
        ("PPN1556_7_WEP_clock", "eta,delta ln nu", "0 only with universal matter/coframe coupling", "dimensionless", "test_required", "matter universality not derived by closure"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "ppn_id": ppn_id,
            "observable": observable,
            "closure_value_or_condition": closure_value_or_condition,
            "units": units,
            "benchmark_status": benchmark_status,
            "remaining_requirement": remaining_requirement,
            "source_paths": source_list("13_doc", "10_doc", "local_bound_claims"),
            **flags(),
        }
        for ppn_id, observable, closure_value_or_condition, units, benchmark_status, remaining_requirement in rows
    ]


def observable_control_rows() -> list[dict[str, Any]]:
    rows = [
        ("OBS1556_0_gps", "GPS satellite-minus-ground", "38.60879935757566", "microseconds/day", "GR_CONTROL_UNDER_CLOSURE"),
        ("OBS1556_1_light_bending", "solar limb light bending", "1.7512432813682448", "arcsec", "GR_CONTROL_UNDER_CLOSURE"),
        ("OBS1556_2_shapiro", "solar Shapiro scale", "119.4750358485562", "microseconds", "GR_CONTROL_UNDER_CLOSURE"),
        ("OBS1556_3_mercury", "Mercury perihelion", "42.98201260912118", "arcsec/century", "GR_CONTROL_UNDER_CLOSURE"),
        ("OBS1556_4_gamma", "gamma", "1", "dimensionless", "CLOSURE_CONTROL"),
        ("OBS1556_5_beta", "beta", "1", "dimensionless", "CLOSURE_CONTROL"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "observable_id": observable_id,
            "observable": observable,
            "control_value": control_value,
            "units": units,
            "status": status,
            "source_paths": source_list("13_doc"),
            **flags(),
        }
        for observable_id, observable, control_value, units, status in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN1556_0_assumptions", "closure assumptions explicit", "PASS_NONCLAIM", "R_AB=0 and Q_R=0 are labelled closure assumptions"),
        ("RUN1556_1_gamma", "gamma control", "PASS_CLOSURE_CONTROL", "gamma=1 follows inside closure"),
        ("RUN1556_2_beta", "beta control", "PASS_BENCHMARK_NOT_DERIVATION", "beta=1 is a GR-control value, not parent-derived"),
        ("RUN1556_3_conservation", "Bianchi/conservation", "REFUSED_MISSING_PARENT_IDENTITY", "closure does not supply field equations"),
        ("RUN1556_4_matter", "matter universality", "REFUSED_MISSING_MATTER_DESCENT", "closure does not prove universal coupling"),
        ("RUN1556_5_source", "Newton/source normalization", "REFUSED_MISSING_SOURCE_BRIDGE", "closure does not prove Poisson/Gauss/orbital GM bridge"),
        ("RUN1556_6_score_status", "derived local GR/Newton claim", "REFUSED_NOT_DERIVED", "closure benchmark is not derivation"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "check": check,
            "current_status": current_status,
            "reason": reason,
            "accepted_for_scoring": False,
            "passes_for_claim": False,
            **flags(),
        }
        for runner_id, check, current_status, reason in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1556_0_assumption_ledger", "closure assumption ledger", "PASS_NONCLAIM", "assumed vs derived is explicit"),
        ("GATE1556_1_ppn_benchmark", "PPN benchmark ledger", "PASS_NONCLAIM", "control values and remaining gates are written"),
        ("GATE1556_2_gamma_control", "gamma=1 under closure", "PASS_CLOSURE_CONTROL", "not a parent derivation"),
        ("GATE1556_3_beta_control", "beta=1 under closure", "PASS_BENCHMARK_NOT_DERIVATION", "second-order source closure remains required"),
        ("GATE1556_4_parent_origin", "R_AB=0 parent origin", "BLOCKED", "1555 rejected current derivation routes"),
        ("GATE1556_5_universality_conservation", "matter universality and conservation", "BLOCKED", "closure does not supply field equations or matter descent"),
        ("GATE1556_6_GR_Newton", "derived GR/Newton limit", "BLOCKED_NO_CLAIM", "benchmark is not derivation"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for gate_id, claim, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC1556_0_result", "The R_AB=0 closure benchmark is now cleanly separated from derivation.", "CLOSURE_CONTROL_LEDGER_WRITTEN", "gamma/beta controls are useful but nonclaim"),
        ("DEC1556_1_missing", "The missing gates are conservation, matter universality, source normalization, and deviation coefficients.", "TEST_REQUIRED_GATES_REMAIN", "these decide whether closure can become a testable local branch"),
        ("DEC1556_2_next", "Next target is closure-deviation PPN sensitivity.", "NEXT_1557_DEVIATION_SENSITIVITY", "quantify q_R, beta drift, matter drift, and source-normalization residuals against local bounds"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "result": result,
            "rationale": rationale,
            **flags(),
        }
        for decision_id, decision, result, rationale in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1556_0_1557",
            "next_target": "1557-Y5-closure-deviation-PPN-sensitivity-and-bound-budget.md",
            "script": "scripts/Y5_closure_deviation_PPN_sensitivity_and_bound_budget.py",
            "objective": "turn the closure benchmark into a deviation budget for q_R, beta drift, matter-universality drift, source-normalization drift, and residual R_AB hair against local bounds",
            "do_not": "do not call closure deviations predictions without sourced coefficients; do not claim local GR derivation; do not edit formalization-workbench",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (CLOSURE_ASSUMPTIONS, QUAR_ASSUMPTIONS),
        (DERIVED_VS_ASSUMED, QUAR_DERIVED),
        (PPN_BENCHMARK, QUAR_PPN),
        (OBSERVABLE_CONTROLS, QUAR_OBS),
        (RUNNER, QUAR_RUNNER),
        (DECISION, QUAR_DECISION),
        (CLOSURE_ASSUMPTIONS, BRANCH_ASSUMPTIONS),
        (DERIVED_VS_ASSUMED, BRANCH_DERIVED),
        (PPN_BENCHMARK, BRANCH_PPN),
        (OBSERVABLE_CONTROLS, BRANCH_OBS),
        (RUNNER, BRANCH_RUNNER),
        (DECISION, BRANCH_DECISION),
    ]
    for source, destination in copies:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_modified_count_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= START_TS)


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    assumptions = read_csv(CLOSURE_ASSUMPTIONS)
    derived = read_csv(DERIVED_VS_ASSUMED)
    ppn = read_csv(PPN_BENCHMARK)
    obs = read_csv(OBSERVABLE_CONTROLS)
    run_rows = read_csv(RUNNER)
    gate_rows = read_csv(CLAIM_GATE)
    decision_items = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    checks = [
        ("VAL1556_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1556 source paths exist"),
        ("VAL1556_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all registered evidence needles found"),
        ("VAL1556_2_assumptions", any(row["assumption_id"] == "ASM1556_1_reciprocity" and row["classification"] == "explicit_closure_assumption" for row in assumptions), "R_AB=0 is explicitly labelled as closure assumption"),
        ("VAL1556_3_derived_vs_assumed", any(row["ledger_id"] == "DVA1556_8_parent_origin" and row["status"] == "BLOCKED_NOT_DERIVED" for row in derived), "parent origin remains blocked in derived-vs-assumed ledger"),
        ("VAL1556_4_ppn_requirements", len(ppn) >= 8 and any(row["ppn_id"] == "PPN1556_1_beta" for row in ppn), "PPN/Newton/local requirements ledger written"),
        ("VAL1556_5_observable_controls", len(obs) >= 6 and any(row["observable_id"] == "OBS1556_1_light_bending" for row in obs), "observable control values recorded"),
        ("VAL1556_6_runner_refuses_derivation", any(row["runner_id"] == "RUN1556_6_score_status" and row["current_status"] == "REFUSED_NOT_DERIVED" for row in run_rows), "runner refuses derived local GR claim"),
        ("VAL1556_7_claim_gates_block", any(row["gate_id"] == "GATE1556_6_GR_Newton" and row["status"] == "BLOCKED_NO_CLAIM" for row in gate_rows), "GR/Newton claim remains blocked"),
        ("VAL1556_8_decision_next", any(row["result"] == "NEXT_1557_DEVIATION_SENSITIVITY" for row in decision_items), "decision selects closure-deviation sensitivity next"),
        ("VAL1556_9_next_target", any("1557-Y5-closure-deviation" in row["next_target"] for row in next_rows), "next target is closure-deviation PPN sensitivity and bound budget"),
        ("VAL1556_10_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1556 CSVs parse cleanly"),
        ("VAL1556_11_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1556_12_branch_copies", all(path.exists() for path in [QUAR_ASSUMPTIONS, QUAR_DERIVED, QUAR_PPN, QUAR_OBS, QUAR_RUNNER, QUAR_DECISION, BRANCH_ASSUMPTIONS, BRANCH_DERIVED, BRANCH_PPN, BRANCH_OBS, BRANCH_RUNNER, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1556_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1556_14_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1556_15_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1556 formalizes the R_AB=0 closure benchmark, separates derived/assumed/test-required local conditions, and selects closure-deviation sensitivity next"
            if overall
            else "1556 validation failed; inspect failed rows before continuing",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    output = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        output.append(
            "| "
            + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns)
            + " |"
        )
    return "\n".join(output)


def write_doc(
    sources: list[dict[str, Any]],
    assumptions: list[dict[str, Any]],
    derived: list[dict[str, Any]],
    ppn: list[dict[str, Any]],
    obs: list[dict[str, Any]],
    run_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    decision_items: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1556 - Local Closure PPN Benchmark and Derived vs Assumed Ledger",
                "",
                "## Verdict",
                "- The `R_AB=0` local closure benchmark is now formalized as a control lane, not a derivation.",
                "- Inside the closure, `p=1`, `gamma=1`, and the GR solar-system control values are available as benchmark checks.",
                "- `R_AB=0`, `Q_R=0`, beta completion, conservation, matter universality, source normalization, and tracefree transfer are not parent-derived here.",
                "- This lets future work test deviations honestly instead of pretending the local GR/Newton limit is already derived.",
                "- Next target is a closure-deviation PPN sensitivity/bound budget.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "",
                "## Closure Assumption Ledger",
                md_table(assumptions, ["assumption_id", "statement", "classification", "reason"]),
                "",
                "## Derived vs Assumed Ledger",
                md_table(derived, ["ledger_id", "quantity", "status", "basis", "limitation"]),
                "",
                "## PPN Benchmark Requirements",
                md_table(ppn, ["ppn_id", "observable", "closure_value_or_condition", "benchmark_status", "remaining_requirement"]),
                "",
                "## Observable Control Values",
                md_table(obs, ["observable_id", "observable", "control_value", "units", "status"]),
                "",
                "## Runner",
                md_table(run_rows, ["runner_id", "check", "current_status", "reason"]),
                "",
                "## Claim Gates",
                md_table(gate_rows, ["gate_id", "claim", "status", "reason"]),
                "",
                "## Decision",
                md_table(decision_items, ["decision_id", "decision", "result", "rationale"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_id", "next_target", "script", "objective", "do_not"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    sources = source_register_rows()
    assumptions = closure_assumption_rows()
    derived = derived_vs_assumed_rows()
    ppn = ppn_benchmark_rows()
    obs = observable_control_rows()
    run_rows = runner_rows()
    gate_rows = claim_gate_rows()
    decision_items = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(CLOSURE_ASSUMPTIONS, assumptions)
    write_csv(DERIVED_VS_ASSUMED, derived)
    write_csv(PPN_BENCHMARK, ppn)
    write_csv(OBSERVABLE_CONTROLS, obs)
    write_csv(RUNNER, run_rows)
    write_csv(CLAIM_GATE, gate_rows)
    write_csv(DECISION, decision_items)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        CLOSURE_ASSUMPTIONS,
        DERIVED_VS_ASSUMED,
        PPN_BENCHMARK,
        OBSERVABLE_CONTROLS,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, assumptions, derived, ppn, obs, run_rows, gate_rows, decision_items, validation, next_rows)


if __name__ == "__main__":
    main()

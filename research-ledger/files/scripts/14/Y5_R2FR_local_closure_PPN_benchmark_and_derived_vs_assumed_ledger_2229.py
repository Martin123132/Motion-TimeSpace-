from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "2229-Y5-R2FR-local-closure-PPN-benchmark-and-derived-vs-assumed-ledger.md"
BRANCH_ID = "MTS_R2FR_PARENT_QLOC_LOCAL_CLOSURE_PPN_BENCHMARK_2229"
START_TS = datetime.now(timezone.utc).timestamp()


SOURCE_FILES = {
    "2228_doc": ROOT / "2228-Y5-R2FR-gauge-noether-zero-charge-qsector-origin-audit.md",
    "2228_validation": OUT / "P8_Y5_BRR545_2228_VALIDATION.csv",
    "2228_next": OUT / "P8_Y5_PARENT_QLOC_2228_NEXT_TARGET.csv",
    "1556_doc": ROOT / "1556-Y5-local-closure-PPN-benchmark-and-derived-vs-assumed-ledger.md",
    "1556_validation": OUT / "P8_Y5_BRR545_1556_VALIDATION.csv",
    "1556_assumptions": OUT / "P8_Y5_PARENT_QLOC_1556_CLOSURE_ASSUMPTION_LEDGER.csv",
    "1556_derived": OUT / "P8_Y5_PARENT_QLOC_1556_DERIVED_VS_ASSUMED_LEDGER.csv",
    "1556_ppn": OUT / "P8_Y5_PARENT_QLOC_1556_PPN_BENCHMARK_REQUIREMENTS.csv",
    "1556_controls": OUT / "P8_Y5_PARENT_QLOC_1556_OBSERVABLE_CONTROL_VALUES_NONCLAIM.csv",
    "1556_runner": OUT / "P8_Y5_PARENT_QLOC_1556_CLOSURE_BENCHMARK_RUNNER_NONCLAIM.csv",
    "1556_decision": OUT / "P8_Y5_PARENT_QLOC_1556_DECISION.csv",
    "1556_next": OUT / "P8_Y5_PARENT_QLOC_1556_NEXT_TARGET.csv",
}


SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_2229_SOURCE_REGISTER.csv"
CLOSURE_ASSUMPTIONS = OUT / "P8_Y5_PARENT_QLOC_2229_CLOSURE_ASSUMPTION_LEDGER.csv"
DERIVED_ASSUMED = OUT / "P8_Y5_PARENT_QLOC_2229_DERIVED_VS_ASSUMED_LEDGER.csv"
PPN_REQUIREMENTS = OUT / "P8_Y5_PARENT_QLOC_2229_PPN_BENCHMARK_REQUIREMENTS.csv"
OBSERVABLE_CONTROLS = OUT / "P8_Y5_PARENT_QLOC_2229_OBSERVABLE_CONTROL_VALUES_NONCLAIM.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_2229_CLOSURE_BENCHMARK_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_2229_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_2229_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_2229_NEXT_TARGET.csv"
BRANCH_COPIES = OUT / "P8_Y5_PARENT_QLOC_2229_BRANCH_COPIES.csv"
VALIDATION = OUT / "P8_Y5_BRR545_2229_VALIDATION.csv"


COPY_TARGETS = {
    "queue": QUEUE / "JR2229_LOCAL_CLOSURE_PPN_BENCHMARK_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "local_closure_ppn_benchmark_nonclaim_2229.csv",
    "beta_docs": BETA_DOCS / "LOCAL_CLOSURE_PPN_BENCHMARK_2229_NONCLAIM.csv",
}


GENERATED = [
    SOURCE_REGISTER,
    CLOSURE_ASSUMPTIONS,
    DERIVED_ASSUMED,
    PPN_REQUIREMENTS,
    OBSERVABLE_CONTROLS,
    RUNNER,
    CLAIM_GATE,
    DECISION,
    NEXT_TARGET,
    BRANCH_COPIES,
    VALIDATION,
]


def flags() -> dict[str, bool]:
    return {
        "theorem_zero_adopted": False,
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


def validation_pass(path: Path) -> bool:
    if not path.exists():
        return False
    rows = read_csv(path)
    if not rows:
        return False
    id_key = "check_id" if "check_id" in rows[0] else "validation_id"
    result_key = "result" if "result" in rows[0] else "status"
    overall_rows = [row for row in rows if "overall" in row.get(id_key, "").lower()]
    if overall_rows:
        return all(row.get(result_key) == "PASS" for row in overall_rows)
    return all(row.get(result_key) == "PASS" for row in rows)


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    keys = [
        "theorem_zero_adopted",
        "numeric_value_present",
        "source_backed",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
    ]
    for path in paths:
        for row in read_csv(path):
            for key in keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_2229_artifacts_absent() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(
        path.is_file()
        and "2229" in path.name
        and ".venv" not in path.relative_to(FORMALIZATION).parts
        for path in FORMALIZATION.rglob("*")
    )


def formalization_untouched_since_start() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(path.is_file() and path.stat().st_mtime >= START_TS for path in FORMALIZATION.rglob("*"))


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (key, path) in enumerate(SOURCE_FILES.items()):
        role = "current zero-charge handoff" if key.startswith("2228") else "older local closure PPN benchmark evidence"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": f"SRC2229_{index}_{key}",
                "source_path": rel(path),
                "path_exists": path.exists(),
                "validation_overall_pass": validation_pass(path) if key.endswith("validation") else "",
                "role": role,
                **flags(),
            }
        )
    return rows


def assumption_rows() -> list[dict[str, Any]]:
    entries = [
        ("ASM2229_0_clock_load", "T^2=1-L", "assumed_or_prior_local_clock_load", "Newtonian clock/load side is used as the weak-field scaffold", "source 13/02"),
        ("ASM2229_1_reciprocity", "R_AB=ln(T^2 S)=0", "explicit_closure_assumption", "not parent-derived after 2228", "source 2228 closure ledger"),
        ("ASM2229_2_spatial_routing", "S=1/T^2=1/(1-L)", "derived_inside_closure", "follows algebraically from ASM2229_0 and ASM2229_1", "closure algebra only"),
        ("ASM2229_3_reciprocal_charge", "Q_R=0", "explicit_closure_assumption", "zero-charge theorem failed; kept as closure", "source 2228 gauge/Noether audit"),
        ("ASM2229_4_areal_radius", "angular sector=r^2 dOmega^2", "benchmark_coordinate_condition", "defines the local control lane but must not be used to derive AB=1", "source 12/13"),
        ("ASM2229_5_matter_universality", "all matter uses same observer coframe", "test_required_not_derived_here", "needed for WEP/clocks/PPN interpretation", "source 10"),
        ("ASM2229_6_claim_policy", "closure is not derivation", "guard", "benchmark may test deviations but cannot prove parent theory", "source 2228"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "assumption_id": assumption_id,
            "statement": statement,
            "classification": classification,
            "reason": reason,
            "evidence_note": evidence,
            **flags(),
        }
        for assumption_id, statement, classification, reason, evidence in entries
    ]


def derived_rows() -> list[dict[str, Any]]:
    entries = [
        ("DVA2229_0_p_equals_1", "p=1", "DERIVED_WITHIN_CLOSURE", "from T^2=1-L and R_AB=0", "not parent-derived"),
        ("DVA2229_1_gamma", "gamma=1", "DERIVED_WITHIN_CLOSURE", "spatial curvature lane p=1 gives gamma=1", "only under closure"),
        ("DVA2229_2_beta", "beta=1", "BENCHMARK_CONTROL_VALUE", "accepted in the Schwarzschild-equivalent control lane", "not derived by MTS parent action"),
        ("DVA2229_3_Newton", "Newtonian acceleration", "TEST_REQUIRED", "T^2 weak-field term must produce correct slow-particle acceleration", "requires source normalization/Poisson bridge"),
        ("DVA2229_4_conservation", "Bianchi-like consistency", "TEST_REQUIRED", "field equations must imply conservation identity", "not supplied by closure"),
        ("DVA2229_5_matter", "universal matter coupling", "TEST_REQUIRED", "same coframe for clocks, matter, photons, and orbital readouts", "not supplied by closure"),
        ("DVA2229_6_source_norm", "measured GM/source normalization", "TEST_REQUIRED", "same source charge must feed Poisson/orbit/PPN", "not supplied by closure"),
        ("DVA2229_7_tracefree", "tracefree metric transfer", "BLOCKED_OUTSIDE_SCALAR_CLOSURE", "scalar reciprocity does not fix tracefree tensor map", "requires separate metric/coframe definition"),
        ("DVA2229_8_parent_origin", "R_AB=0 parent derivation", "BLOCKED_NOT_DERIVED", "gauge/Noether/phase-volume attempts failed", "future first-class constraint only"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "ledger_id": ledger_id,
            "quantity": quantity,
            "status": status,
            "basis": basis,
            "limitation": limitation,
            **flags(),
        }
        for ledger_id, quantity, status, basis, limitation in entries
    ]


def ppn_rows() -> list[dict[str, Any]]:
    entries = [
        ("PPN2229_0_gamma", "gamma_minus_1", "0 under R_AB=0 closure", "dimensionless", "closure_control", "Cassini/local bound row can test deviations, not derivation"),
        ("PPN2229_1_beta", "beta_minus_1", "0 in exact Schwarzschild-equivalent control lane", "dimensionless", "benchmark_control_not_parent_derived", "second-order weak-field source closure still required"),
        ("PPN2229_2_alpha1", "alpha1", "0 only if no preferred-frame/shadow-frame residuals", "dimensionless", "test_required", "frame/coframe descent not proven by closure"),
        ("PPN2229_3_alpha2", "alpha2", "0 only if no spin/preferred-frame residuals", "dimensionless", "test_required", "not handled by scalar R_AB closure"),
        ("PPN2229_4_alpha3_xi", "alpha3,xi", "0 only if boundary/source fluxes vanish", "dimensionless", "test_required", "boundary/no-charge/source-normalization gates remain open"),
        ("PPN2229_5_Gdot", "Gdot/G", "0 only if source normalization is time-stationary", "yr^-1", "test_required", "measured-GM/source-normalization theorem missing"),
        ("PPN2229_6_R10", "alpha(lambda)", "0 only if no finite-range q/source hair survives", "dimensionless curve", "test_required", "closure says nothing about all retained residual sectors"),
        ("PPN2229_7_WEP_clock", "eta,delta ln nu", "0 only with universal matter/coframe coupling", "dimensionless", "test_required", "matter universality not derived by closure"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "ppn_id": ppn_id,
            "observable": observable,
            "closure_value_or_condition": condition,
            "units": units,
            "benchmark_status": status,
            "remaining_requirement": requirement,
            **flags(),
        }
        for ppn_id, observable, condition, units, status, requirement in entries
    ]


def control_rows() -> list[dict[str, Any]]:
    entries: list[tuple[str, str, str, str, str]] = [
        ("OBS2229_0_gps", "GPS satellite-minus-ground", "38.60879935757566", "microseconds/day", "GR_CONTROL_UNDER_CLOSURE"),
        ("OBS2229_1_light_bending", "solar limb light bending", "1.7512432813682448", "arcsec", "GR_CONTROL_UNDER_CLOSURE"),
        ("OBS2229_2_shapiro", "solar Shapiro scale", "119.4750358485562", "microseconds", "GR_CONTROL_UNDER_CLOSURE"),
        ("OBS2229_3_mercury", "Mercury perihelion", "42.98201260912118", "arcsec/century", "GR_CONTROL_UNDER_CLOSURE"),
        ("OBS2229_4_gamma", "gamma", "1", "dimensionless", "CLOSURE_CONTROL"),
        ("OBS2229_5_beta", "beta", "1", "dimensionless", "CLOSURE_CONTROL"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "observable_id": observable_id,
            "observable": observable,
            "control_value": value,
            "units": units,
            "status": status,
            **flags(),
        }
        for observable_id, observable, value, units, status in entries
    ]


def runner_rows() -> list[dict[str, Any]]:
    entries = [
        ("RUN2229_0_assumptions", "closure assumptions explicit", "PASS_NONCLAIM", "R_AB=0 and Q_R=0 are labelled closure assumptions"),
        ("RUN2229_1_gamma", "gamma control", "PASS_CLOSURE_CONTROL", "gamma=1 follows inside closure"),
        ("RUN2229_2_beta", "beta control", "PASS_BENCHMARK_NOT_DERIVATION", "beta=1 is a GR-control value, not parent-derived"),
        ("RUN2229_3_conservation", "Bianchi/conservation", "REFUSED_MISSING_PARENT_IDENTITY", "closure does not supply field equations"),
        ("RUN2229_4_matter", "matter universality", "REFUSED_MISSING_MATTER_DESCENT", "closure does not prove universal coupling"),
        ("RUN2229_5_source", "Newton/source normalization", "REFUSED_MISSING_SOURCE_BRIDGE", "closure does not prove Poisson/Gauss/orbital GM bridge"),
        ("RUN2229_6_score_status", "derived local GR/Newton claim", "REFUSED_NOT_DERIVED", "closure benchmark is not derivation"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "check": check,
            "current_status": status,
            "reason": reason,
            **flags(),
        }
        for runner_id, check, status, reason in entries
    ]


def claim_rows() -> list[dict[str, Any]]:
    entries = [
        ("CG2229_0_assumption_ledger", "closure assumption ledger", "PASS_NONCLAIM", "assumed vs derived is explicit"),
        ("CG2229_1_ppn_benchmark", "PPN benchmark ledger", "PASS_NONCLAIM", "control values and remaining gates are written"),
        ("CG2229_2_gamma_control", "gamma=1 under closure", "PASS_CLOSURE_CONTROL", "not a parent derivation"),
        ("CG2229_3_beta_control", "beta=1 under closure", "PASS_BENCHMARK_NOT_DERIVATION", "second-order source closure remains required"),
        ("CG2229_4_parent_origin", "R_AB=0 parent origin", "BLOCKED", "2228 rejected current derivation routes"),
        ("CG2229_5_universality_conservation", "matter universality and conservation", "BLOCKED", "closure does not supply field equations or matter descent"),
        ("CG2229_6_GR_Newton", "derived GR/Newton limit", "BLOCKED_NO_CLAIM", "benchmark is not derivation"),
        ("CG2229_7_GitHub", "public/GitHub update", "BLOCKED_NONCLAIM", "private proof line remains mid-derivation"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for gate_id, claim, status, reason in entries
    ]


def decision_rows() -> list[dict[str, Any]]:
    entries = [
        ("DEC2229_0_result", "The R_AB=0 closure benchmark is cleanly separated from derivation.", "CLOSURE_CONTROL_LEDGER_WRITTEN", "gamma/beta controls are useful but nonclaim"),
        ("DEC2229_1_missing", "The missing gates are conservation, matter universality, source normalization, and deviation coefficients.", "TEST_REQUIRED_GATES_REMAIN", "these decide whether closure can become a testable local branch"),
        ("DEC2229_2_next", "Next target is closure-deviation PPN sensitivity.", "NEXT_2230_DEVIATION_SENSITIVITY", "quantify q_R, beta drift, matter drift, source-normalization residuals, and R_AB hair against local bounds"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "result": result,
            "rationale": rationale,
            **flags(),
        }
        for decision_id, decision, result, rationale in entries
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_id": "NEXT2229_0_2230",
            "target_file": "2230-Y5-R2FR-closure-deviation-PPN-sensitivity-and-bound-budget.md",
            "target_script": "scripts/Y5_R2FR_closure_deviation_PPN_sensitivity_and_bound_budget_2230.py",
            "objective": "turn the closure benchmark into a deviation budget for q_R, beta drift, matter-universality drift, source-normalization drift, and residual R_AB hair against local bounds",
            "success_condition": "deviation channels and local-bound links are explicit while all unsourced coefficients remain nonclaim",
            "do_not": "do not call closure deviations predictions without sourced coefficients; do not claim local GR derivation; do not edit formalization-workbench",
            **flags(),
        }
    ]


def copy_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for copy_id, target in COPY_TARGETS.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(DERIVED_ASSUMED, target)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": copy_id,
                "source_path": rel(DERIVED_ASSUMED),
                "target_path": rel(target),
                "copied": target.exists(),
                "parse_ok": parse_csv(target),
                **flags(),
            }
        )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_doc(
    source: list[dict[str, Any]],
    assumptions: list[dict[str, Any]],
    derived: list[dict[str, Any]],
    ppn: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    claim: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 2229 - Y5/R2FR Local Closure PPN Benchmark And Derived-vs-Assumed Ledger",
            "## Verdict\n"
            "- 2229 imports the old `1556` local closure PPN benchmark into the current R2FR line.\n"
            "- Under explicit `R_AB=0` and `Q_R=0` closure, `p=1` and `gamma=1` follow inside the closure lane.\n"
            "- `beta=1` is retained only as a Schwarzschild-equivalent benchmark control, not as a parent-derived MTS result.\n"
            "- The closure still does not prove conservation, universal matter/coframe coupling, source normalization, tracefree transfer, or parent origin.\n"
            "- Next target is a deviation budget: how much `q_R`, beta drift, matter drift, source-normalization drift, or residual hair can survive local bounds.",
            "## Source Register\n"
            + md_table(source, ["source_id", "source_path", "path_exists", "validation_overall_pass", "role"]),
            "## Closure Assumption Ledger\n"
            + md_table(assumptions, ["assumption_id", "statement", "classification", "reason", "evidence_note"]),
            "## Derived vs Assumed Ledger\n"
            + md_table(derived, ["ledger_id", "quantity", "status", "basis", "limitation"]),
            "## PPN Benchmark Requirements\n"
            + md_table(ppn, ["ppn_id", "observable", "closure_value_or_condition", "units", "benchmark_status", "remaining_requirement"]),
            "## Observable Control Values\n"
            + md_table(controls, ["observable_id", "observable", "control_value", "units", "status"]),
            "## Closure Benchmark Runner\n"
            + md_table(runner, ["runner_id", "check", "current_status", "reason"]),
            "## Claim Gate\n"
            + md_table(claim, ["gate_id", "claim", "status", "reason"]),
            "## Decision Ledger\n"
            + md_table(decision, ["decision_id", "decision", "result", "rationale"]),
            "## Next Target\n"
            + md_table(next_target, ["next_id", "target_file", "target_script", "objective", "success_condition", "do_not"]),
            "## Branch Copies\n"
            + md_table(copies, ["copy_id", "source_path", "target_path", "copied", "parse_ok"]),
            "## Validation\n"
            + md_table(validation, ["check_id", "result", "detail"]),
            "## Working Interpretation\n\n"
            "This is the clean benchmark lane. It does not pretend that MTS has derived GR locally, but it lets the framework ask a serious question: if the unresolved reciprocal sector is closed explicitly, what local observables line up with the GR control values and which hidden residuals still have to be bounded? That is useful because the next pass can quantify deviations instead of arguing about labels.",
            "",
        ]
    )


def validation_rows(generated_paths: list[Path]) -> list[dict[str, Any]]:
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2229_00_sources_exist",
            "result": "PASS" if all(path.exists() for path in SOURCE_FILES.values()) else "FAIL",
            "detail": "all cited 2229 source paths exist",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2229_01_prior_validations",
            "result": "PASS" if validation_pass(SOURCE_FILES["2228_validation"]) and validation_pass(SOURCE_FILES["1556_validation"]) else "FAIL",
            "detail": "2228 and 1556 validations pass overall",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2229_02_assumptions",
            "result": "PASS" if any(row["classification"] == "explicit_closure_assumption" for row in read_csv(CLOSURE_ASSUMPTIONS)) else "FAIL",
            "detail": "R_AB=0 and Q_R=0 closure assumptions are explicit",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2229_03_derived_vs_assumed",
            "result": "PASS" if any(row["status"] == "BLOCKED_NOT_DERIVED" for row in read_csv(DERIVED_ASSUMED)) else "FAIL",
            "detail": "parent origin remains blocked in derived-vs-assumed ledger",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2229_04_ppn_requirements",
            "result": "PASS" if len(read_csv(PPN_REQUIREMENTS)) >= 8 else "FAIL",
            "detail": "PPN/Newton/local requirements ledger written",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2229_05_observable_controls",
            "result": "PASS" if len(read_csv(OBSERVABLE_CONTROLS)) >= 6 else "FAIL",
            "detail": "observable control values recorded",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2229_06_runner_refuses_derivation",
            "result": "PASS" if any(row["current_status"] == "REFUSED_NOT_DERIVED" for row in read_csv(RUNNER)) else "FAIL",
            "detail": "runner refuses derived local GR claim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2229_07_claim_gates_block",
            "result": "PASS" if all("BLOCKED" in row["status"] or row["status"].startswith("PASS") for row in read_csv(CLAIM_GATE)) else "FAIL",
            "detail": "GR/Newton and public claims remain blocked/nonclaim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2229_08_decision_next",
            "result": "PASS" if any(row["result"] == "NEXT_2230_DEVIATION_SENSITIVITY" for row in read_csv(DECISION)) else "FAIL",
            "detail": "decision selects closure-deviation sensitivity next",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2229_09_next_target",
            "result": "PASS" if read_csv(NEXT_TARGET)[0]["target_file"].startswith("2230-Y5-R2FR-closure-deviation") else "FAIL",
            "detail": "next target is current-numbered closure-deviation PPN sensitivity",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2229_10_csv_parse",
            "result": "PASS" if all(parse_csv(path) for path in generated_paths) else "FAIL",
            "detail": "all generated 2229 CSVs parse cleanly",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2229_11_claim_flags_false",
            "result": "PASS" if generated_flags_false(generated_paths) else "FAIL",
            "detail": "all generated flags remain nonclaim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2229_12_branch_copies",
            "result": "PASS" if all(row["copied"] == "True" and row["parse_ok"] == "True" for row in read_csv(BRANCH_COPIES)) else "FAIL",
            "detail": "branch copies written and parse",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2229_13_pycache_absent",
            "result": "PASS" if not (ROOT / "scripts" / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent after run",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2229_14_formalization_no_2229",
            "result": "PASS" if formalization_2229_artifacts_absent() else "FAIL",
            "detail": "formalization-workbench has no non-venv 2229 artifacts",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2229_15_formalization_untouched",
            "result": "PASS" if formalization_untouched_since_start() else "FAIL",
            "detail": "formalization-workbench untouched during 2229 run",
        },
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2229_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "2229 imports the local closure PPN benchmark, separates derived-vs-assumed pieces, keeps closure nonclaim, and selects closure-deviation sensitivity next",
        }
    )
    return rows


def main() -> None:
    source = source_rows()
    assumptions = assumption_rows()
    derived = derived_rows()
    ppn = ppn_rows()
    controls = control_rows()
    runner = runner_rows()
    claim = claim_rows()
    decision = decision_rows()
    next_target = next_rows()

    write_csv(SOURCE_REGISTER, source)
    write_csv(CLOSURE_ASSUMPTIONS, assumptions)
    write_csv(DERIVED_ASSUMED, derived)
    write_csv(PPN_REQUIREMENTS, ppn)
    write_csv(OBSERVABLE_CONTROLS, controls)
    write_csv(RUNNER, runner)
    write_csv(CLAIM_GATE, claim)
    write_csv(DECISION, decision)
    write_csv(NEXT_TARGET, next_target)
    copies = copy_rows()
    write_csv(BRANCH_COPIES, copies)

    remove_pycache()
    generated_before_validation = [path for path in GENERATED if path != VALIDATION]
    validation = validation_rows(generated_before_validation)
    write_csv(VALIDATION, validation)
    remove_pycache()

    DOC.write_text(
        build_doc(
            source,
            assumptions,
            derived,
            ppn,
            controls,
            runner,
            claim,
            decision,
            next_target,
            copies,
            validation,
        ),
        encoding="utf-8",
    )

    if not validation_pass(VALIDATION):
        raise SystemExit(f"2229 validation failed: {VALIDATION}")


if __name__ == "__main__":
    main()

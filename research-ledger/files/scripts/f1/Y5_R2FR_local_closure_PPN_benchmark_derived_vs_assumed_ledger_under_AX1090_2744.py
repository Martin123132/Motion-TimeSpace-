from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2744-Y5-R2FR-local-closure-PPN-benchmark-derived-vs-assumed-ledger-under-AX1090.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2744_SOURCE_REGISTER.csv",
    "assumptions": RESIDUALS / "P8_Y5_R2FR_2744_CLOSURE_ASSUMPTION_LEDGER.csv",
    "derived": RESIDUALS / "P8_Y5_R2FR_2744_DERIVED_VS_ASSUMED_LEDGER.csv",
    "ppn": RESIDUALS / "P8_Y5_R2FR_2744_PPN_BENCHMARK_REQUIREMENTS.csv",
    "controls": RESIDUALS / "P8_Y5_R2FR_2744_OBSERVABLE_CONTROL_VALUES_NONCLAIM.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2744_CLOSURE_BENCHMARK_RUNNER_NONCLAIM.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_2744_DECISION_LEDGER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2744_CLAIM_GATES.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2744_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2744_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2744_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "derived": SOURCE_WEIGHT / "local_closure_derived_vs_assumed_2744_NONCLAIM.csv",
    "ppn": LOCAL_BOUNDS / "local_closure_ppn_benchmark_2744_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2744_CLOSURE_DEVIATION_PPN_SENSITIVITY_NEXT.csv",
}

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()}:
        path.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def md(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], cols: list[str]) -> str:
    header = "| " + " | ".join(cols) + " |"
    sep = "| " + " | ".join("---" for _ in cols) + " |"
    body = ["| " + " | ".join(md(row.get(col, "")) for col in cols) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def local_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["score_ready"] = False
    row["valid_prediction_row"] = False
    row["valid_for_claim"] = False
    row["claim_allowed"] = False
    return row


def source_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "source_id": "SRC2744_0_2743_doc",
            "description": "2743 demotes zero-charge route to explicit closure benchmark and selects this PPN ledger.",
            "source_path": "2743-Y5-R2FR-gauge-noether-zero-charge-qsector-origin-or-closure-demotion-under-AX1090.md",
            "required_needles": "NEXT2743_0_2744;CL2743_0_closure_statement;VAL2743_OVERALL",
        },
        {
            "source_id": "SRC2744_1_2743_validation",
            "description": "2743 validation output.",
            "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2743_VALIDATION.csv",
            "required_needles": "VAL2743_OVERALL;True;local closure PPN benchmark next",
        },
        {
            "source_id": "SRC2744_2_1556_doc",
            "description": "prior local closure PPN benchmark and ledger.",
            "source_path": "1556-Y5-local-closure-PPN-benchmark-and-derived-vs-assumed-ledger.md",
            "required_needles": "DVA1556_1_gamma;PPN1556_0_gamma;NEXT1556_0_1557",
        },
        {
            "source_id": "SRC2744_3_13_local_closure",
            "description": "local closure PPN source text.",
            "source_path": "13-local-closure-PPN-benchmark.md",
            "required_needles": "local_closure_ppn_benchmark_valid_control_not_derivation;gamma = 1;beta = 1",
        },
        {
            "source_id": "SRC2744_4_10_observer_contract",
            "description": "observer-map contract for gamma/beta/conservation warning.",
            "source_path": "10-observer-map-symplectic-contract.md",
            "required_needles": "gamma - 1 = 0 after R_AB=0;beta - 1 = 0;Bianchi-like consistency identity",
        },
        {
            "source_id": "SRC2744_5_1556_derived_csv",
            "description": "machine-readable prior derived-vs-assumed ledger.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1556_DERIVED_VS_ASSUMED_LEDGER.csv",
            "required_needles": "DVA1556_1_gamma;DVA1556_5_matter;DVA1556_8_parent_origin",
        },
        {
            "source_id": "SRC2744_6_1556_ppn_csv",
            "description": "machine-readable prior PPN benchmark requirements.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1556_PPN_BENCHMARK_REQUIREMENTS.csv",
            "required_needles": "PPN1556_0_gamma;PPN1556_1_beta;PPN1556_7_WEP_clock",
        },
        {
            "source_id": "SRC2744_7_1556_controls_csv",
            "description": "machine-readable closure control values.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1556_OBSERVABLE_CONTROL_VALUES_NONCLAIM.csv",
            "required_needles": "OBS1556_0_gps;OBS1556_3_mercury;OBS1556_5_beta",
        },
        {
            "source_id": "SRC2744_8_2743_queue",
            "description": "live acquisition queue into this checkpoint.",
            "source_path": "source-intake/rab-sector/acquisition-queue/JR2743_LOCAL_CLOSURE_PPN_BENCHMARK_NEXT.csv",
            "required_needles": "NEXT2743_0_2744;build the honest R_AB=0 closure benchmark",
        },
    ]
    for row in rows:
        path = local_path(row["source_path"])
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        needles = [needle for needle in row["required_needles"].split(";") if needle]
        missing = [needle for needle in needles if needle not in text]
        row["exists"] = path.exists()
        row["needles_present"] = len(missing) == 0
        row["missing_needles"] = ";".join(missing)
        nonclaim(row)
    return rows


def assumption_rows() -> list[dict[str, Any]]:
    specs = [
        ("ASM2744_0_clock_load", "T^2=1-L", "assumed_or_prior_local_clock_load", "Newtonian clock/load side is used as weak-field scaffold"),
        ("ASM2744_1_reciprocity", "R_AB=ln(T^2 S)=0", "explicit_closure_assumption", "not parent-derived after phase-volume and zero-charge audits"),
        ("ASM2744_2_spatial_routing", "S=1/T^2=1/(1-L)", "derived_inside_closure", "follows algebraically from ASM2744_0 and ASM2744_1"),
        ("ASM2744_3_reciprocal_charge", "Q_R=0", "explicit_closure_assumption", "zero-charge theorem failed; kept as closure only"),
        ("ASM2744_4_areal_radius", "angular sector=r^2 dOmega^2", "benchmark_coordinate_condition", "defines the local control lane but must not be used to derive AB=1"),
        ("ASM2744_5_matter_universality", "all matter uses same observer coframe", "test_required_not_derived_here", "needed for WEP/clocks/PPN interpretation"),
        ("ASM2744_6_claim_policy", "closure is not derivation", "guard", "benchmark may test deviations but cannot prove parent theory"),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "assumption_id": aid,
                "statement": statement,
                "classification": classification,
                "reason": reason,
            }
        )
        for aid, statement, classification, reason in specs
    ]


def derived_rows() -> list[dict[str, Any]]:
    specs = [
        ("DVA2744_0_p_equals_1", "p=1", "DERIVED_WITHIN_CLOSURE", "from T^2=1-L and R_AB=0", "not parent-derived"),
        ("DVA2744_1_gamma", "gamma=1", "DERIVED_WITHIN_CLOSURE", "spatial curvature lane p=1 gives gamma=1", "only under closure"),
        ("DVA2744_2_beta", "beta=1", "BENCHMARK_CONTROL_VALUE", "accepted in the Schwarzschild-equivalent control lane", "not derived by MTS parent action"),
        ("DVA2744_3_Newton", "Newtonian acceleration", "TEST_REQUIRED", "T^2 weak-field term must produce correct slow-particle acceleration", "requires source normalization/Poisson bridge"),
        ("DVA2744_4_conservation", "Bianchi-like consistency", "TEST_REQUIRED", "field equations must imply conservation identity", "not supplied by closure"),
        ("DVA2744_5_matter", "universal matter coupling", "TEST_REQUIRED", "same coframe for clocks, matter, photons, and orbital readouts", "not supplied by closure"),
        ("DVA2744_6_source_norm", "measured GM/source normalization", "TEST_REQUIRED", "same source charge must feed Poisson/orbit/PPN", "not supplied by closure"),
        ("DVA2744_7_tracefree", "tracefree metric transfer", "BLOCKED_OUTSIDE_SCALAR_CLOSURE", "scalar reciprocity does not fix tracefree tensor map", "requires separate metric/coframe definition"),
        ("DVA2744_8_parent_origin", "R_AB=0 parent derivation", "BLOCKED_NOT_DERIVED", "gauge/Noether/phase-volume attempts failed", "future first-class constraint only"),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "ledger_id": lid,
                "quantity": quantity,
                "status": status,
                "basis": basis,
                "limitation": limitation,
                "source_paths": "2743-Y5-R2FR-gauge-noether-zero-charge-qsector-origin-or-closure-demotion-under-AX1090.md; 13-local-closure-PPN-benchmark.md; 10-observer-map-symplectic-contract.md",
            }
        )
        for lid, quantity, status, basis, limitation in specs
    ]


def ppn_rows() -> list[dict[str, Any]]:
    specs = [
        ("PPN2744_0_gamma", "gamma_minus_1", "0 under R_AB=0 closure", "closure_control", "Cassini/local bound can test deviations, not derivation"),
        ("PPN2744_1_beta", "beta_minus_1", "0 in exact Schwarzschild-equivalent control lane", "benchmark_control_not_parent_derived", "second-order weak-field source closure still required"),
        ("PPN2744_2_alpha1", "alpha1", "0 only if no preferred-frame/shadow-frame residuals", "test_required", "frame/coframe descent not proven by closure"),
        ("PPN2744_3_alpha2", "alpha2", "0 only if no spin/preferred-frame residuals", "test_required", "not handled by scalar R_AB closure"),
        ("PPN2744_4_alpha3_xi", "alpha3,xi", "0 only if boundary/source fluxes vanish", "test_required", "boundary/no-charge/source-normalization gates remain open"),
        ("PPN2744_5_Gdot", "Gdot/G", "0 only if source normalization is time-stationary", "test_required", "measured-GM/source-normalization theorem missing"),
        ("PPN2744_6_R10", "alpha(lambda)", "0 only if no finite-range q/source hair survives", "test_required", "closure says nothing about all retained residual sectors"),
        ("PPN2744_7_WEP_clock", "eta,delta ln nu", "0 only with universal matter/coframe coupling", "test_required", "matter universality not derived by closure"),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "ppn_id": pid,
                "observable": observable,
                "closure_value_or_condition": value,
                "benchmark_status": status,
                "remaining_requirement": requirement,
            }
        )
        for pid, observable, value, status, requirement in specs
    ]


def control_rows() -> list[dict[str, Any]]:
    specs = [
        ("OBS2744_0_gps", "GPS satellite-minus-ground", "38.60879935757566", "microseconds/day", "GR_CONTROL_UNDER_CLOSURE"),
        ("OBS2744_1_light_bending", "solar limb light bending", "1.7512432813682448", "arcsec", "GR_CONTROL_UNDER_CLOSURE"),
        ("OBS2744_2_shapiro", "solar Shapiro scale", "119.4750358485562", "microseconds", "GR_CONTROL_UNDER_CLOSURE"),
        ("OBS2744_3_mercury", "Mercury perihelion", "42.98201260912118", "arcsec/century", "GR_CONTROL_UNDER_CLOSURE"),
        ("OBS2744_4_gamma", "gamma", "1", "dimensionless", "CLOSURE_CONTROL"),
        ("OBS2744_5_beta", "beta", "1", "dimensionless", "CLOSURE_CONTROL"),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "observable_id": oid,
                "observable": observable,
                "control_value": value,
                "units": units,
                "status": status,
                "source_paths": "13-local-closure-PPN-benchmark.md; source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1556_OBSERVABLE_CONTROL_VALUES_NONCLAIM.csv",
            }
        )
        for oid, observable, value, units, status in specs
    ]


def runner_rows() -> list[dict[str, Any]]:
    specs = [
        ("RUN2744_0_assumptions", "closure assumptions explicit", "PASS_NONCLAIM", "R_AB=0 and Q_R=0 are labelled closure assumptions"),
        ("RUN2744_1_gamma", "gamma control", "PASS_CLOSURE_CONTROL", "gamma=1 follows inside closure"),
        ("RUN2744_2_beta", "beta control", "PASS_BENCHMARK_NOT_DERIVATION", "beta=1 is a GR-control value, not parent-derived"),
        ("RUN2744_3_conservation", "Bianchi/conservation", "REFUSED_MISSING_PARENT_IDENTITY", "closure does not supply field equations"),
        ("RUN2744_4_matter", "matter universality", "REFUSED_MISSING_MATTER_DESCENT", "closure does not prove universal coupling"),
        ("RUN2744_5_source", "Newton/source normalization", "REFUSED_MISSING_SOURCE_BRIDGE", "closure does not prove Poisson/Gauss/orbital GM bridge"),
        ("RUN2744_6_score_status", "derived local GR/Newton claim", "REFUSED_NOT_DERIVED", "closure benchmark is not derivation"),
    ]
    return [nonclaim({"same_parent_branch_id": BRANCH_ID, "runner_id": rid, "check": check, "current_status": status, "reason": reason}) for rid, check, status, reason in specs]


def gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATE2744_0_assumption_ledger", "closure assumption ledger", True, "PASS_NONCLAIM", "assumed vs derived is explicit"),
        ("GATE2744_1_ppn_benchmark", "PPN benchmark ledger", True, "PASS_NONCLAIM", "control values and remaining gates are written"),
        ("GATE2744_2_gamma_control", "gamma=1 under closure", True, "PASS_CLOSURE_CONTROL", "not a parent derivation"),
        ("GATE2744_3_beta_control", "beta=1 under closure", True, "PASS_BENCHMARK_NOT_DERIVATION", "second-order source closure remains required"),
        ("GATE2744_4_parent_origin", "R_AB=0 parent origin", False, "BLOCKED", "2743 rejected current derivation routes"),
        ("GATE2744_5_universality_conservation", "matter universality and conservation", False, "BLOCKED", "closure does not supply field equations or matter descent"),
        ("GATE2744_6_GR_Newton", "derived GR/Newton limit", False, "BLOCKED_NO_CLAIM", "benchmark is not derivation"),
    ]
    return [
        nonclaim(
            {
                "claim_gate_id": gid,
                "claim": claim,
                "gate_passed": passed,
                "status": status,
                "claim_allowed": False,
                "reason": reason,
            }
        )
        for gid, claim, passed, status, reason in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2744_0_result", "The R_AB=0 closure benchmark is cleanly separated from derivation.", "CLOSURE_CONTROL_LEDGER_WRITTEN", "gamma/beta controls are useful but nonclaim"),
        ("DEC2744_1_missing", "The missing gates are conservation, matter universality, source normalization, and deviation coefficients.", "TEST_REQUIRED_GATES_REMAIN", "these decide whether closure can become a credible local branch"),
        ("DEC2744_2_next", "Next target is closure-deviation PPN sensitivity.", "NEXT_2745_DEVIATION_SENSITIVITY", "quantify q_R, beta drift, matter drift, source-normalization residuals, and residual R_AB hair against local bounds"),
        ("DEC2744_3_strategy", "Stop trying to declare local GR derived before the residual budget exists.", "TEST_FIRST_DISCIPLINE", "this is the route that gets us toward real constraints instead of more verbal closure"),
    ]
    return [nonclaim({"decision_id": did, "decision": decision, "result": result, "rationale": rationale}) for did, decision, result, rationale in specs]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2744_0_2745",
                "status": "selected_primary",
                "target_doc": "2745-Y5-R2FR-closure-deviation-PPN-sensitivity-and-bound-budget-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_closure_deviation_PPN_sensitivity_and_bound_budget_under_AX1090_2745.py",
                "mission": "turn the closure benchmark into a deviation budget for q_R, beta drift, matter-universality drift, source-normalization drift, and residual R_AB hair against local bounds",
                "acceptance": "write nonclaim sensitivity rows and identify which coefficients need source-backed values before R10/PPN/clock/orbital testing",
                "forbidden": "do not call closure deviations predictions without sourced coefficients; do not claim local GR derivation; do not edit formalization-workbench",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"copy_id": "BR2744_0_derived", "source_table": rel(OUTPUTS["derived"]), "copy_path": rel(BRANCH_OUTPUTS["derived"]), "purpose": "source-weight derived-vs-assumed local closure ledger", "exists": BRANCH_OUTPUTS["derived"].exists()}),
        nonclaim({"copy_id": "BR2744_1_ppn", "source_table": rel(OUTPUTS["ppn"]), "copy_path": rel(BRANCH_OUTPUTS["ppn"]), "purpose": "local-bound PPN benchmark requirements", "exists": BRANCH_OUTPUTS["ppn"].exists()}),
        nonclaim({"copy_id": "BR2744_2_next_queue", "source_table": rel(OUTPUTS["next"]), "copy_path": rel(BRANCH_OUTPUTS["next_queue"]), "purpose": "RAB acquisition queue for closure-deviation PPN sensitivity", "exists": BRANCH_OUTPUTS["next_queue"].exists()}),
    ]


def formalization_recent_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    start = SCRIPT_START_UTC.timestamp()
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= start)


def pycache_path() -> Path:
    return Path(__file__).resolve().parent / "__pycache__"


def remove_pycache() -> None:
    pycache = pycache_path()
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(
    sources: list[dict[str, Any]],
    assumptions: list[dict[str, Any]],
    derived: list[dict[str, Any]],
    ppn: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_ok = all(row["exists"] is True and row["needles_present"] is True for row in sources)
    assumptions_ok = any(row["assumption_id"] == "ASM2744_1_reciprocity" and row["classification"] == "explicit_closure_assumption" for row in assumptions)
    derived_ok = any(row["ledger_id"] == "DVA2744_1_gamma" and row["status"] == "DERIVED_WITHIN_CLOSURE" for row in derived) and any(row["ledger_id"] == "DVA2744_8_parent_origin" and row["status"] == "BLOCKED_NOT_DERIVED" for row in derived)
    ppn_ok = any(row["ppn_id"] == "PPN2744_0_gamma" for row in ppn) and any(row["ppn_id"] == "PPN2744_7_WEP_clock" for row in ppn)
    controls_ok = any(row["observable_id"] == "OBS2744_0_gps" for row in controls) and any(row["observable_id"] == "OBS2744_5_beta" for row in controls)
    runner_ok = any(row["runner_id"] == "RUN2744_1_gamma" and row["current_status"] == "PASS_CLOSURE_CONTROL" for row in runner) and any(row["runner_id"] == "RUN2744_6_score_status" and "REFUSED" in row["current_status"] for row in runner)
    gates_ok = any(row["claim_gate_id"] == "GATE2744_2_gamma_control" and row["gate_passed"] is True for row in gates) and all(row["claim_allowed"] is False for row in gates)
    no_claim_flags_ok = all(row.get("valid_for_claim") is False and row.get("claim_allowed") is False for block in [assumptions, derived, ppn, controls, runner, gates] for row in block)
    next_ok = next_target[0]["selected"] is True and "2745" in next_target[0]["target_doc"] and "deviation" in next_target[0]["target_doc"]
    branch_ok = all(path.exists() for path in BRANCH_OUTPUTS.values())
    pycache_ok = not pycache_path().exists()
    formalization_count = formalization_recent_count()
    formalization_ok = formalization_count == 0
    csv_ok = True
    csv_bits: list[str] = []
    for key, path in {**OUTPUTS, **BRANCH_OUTPUTS}.items():
        if key == "validation":
            continue
        try:
            rows = read_csv(path)
            csv_bits.append(f"{path.name}:{len(rows)}:ok")
        except Exception as exc:
            csv_ok = False
            csv_bits.append(f"{path.name}:ERROR:{exc}")
    rows = [
        {"validation_id": "VAL2744_0_sources", "passed": source_ok, "detail": "all source paths exist and required anchors/needles are present", "timestamp_utc": ts()},
        {"validation_id": "VAL2744_1_assumptions", "passed": assumptions_ok, "detail": "R_AB=0 and Q_R=0 are explicitly labelled closure assumptions", "timestamp_utc": ts()},
        {"validation_id": "VAL2744_2_derived_vs_assumed", "passed": derived_ok, "detail": "gamma is closure-derived while parent origin remains blocked", "timestamp_utc": ts()},
        {"validation_id": "VAL2744_3_ppn_requirements", "passed": ppn_ok, "detail": "PPN/Newton/local requirements ledger written", "timestamp_utc": ts()},
        {"validation_id": "VAL2744_4_observable_controls", "passed": controls_ok, "detail": "observable control values recorded", "timestamp_utc": ts()},
        {"validation_id": "VAL2744_5_runner_refuses_derivation", "passed": runner_ok, "detail": "runner refuses derived local GR claim", "timestamp_utc": ts()},
        {"validation_id": "VAL2744_6_claim_gates", "passed": gates_ok and no_claim_flags_ok, "detail": "claim gates keep all prediction/claim flags false", "timestamp_utc": ts()},
        {"validation_id": "VAL2744_7_next_target", "passed": next_ok, "detail": "next target is closure-deviation PPN sensitivity and bound budget", "timestamp_utc": ts()},
        {"validation_id": "VAL2744_8_branch_outputs", "passed": branch_ok, "detail": "branch copies exist", "timestamp_utc": ts()},
        {"validation_id": "VAL2744_9_csv_parse", "passed": csv_ok, "detail": "; ".join(csv_bits), "timestamp_utc": ts()},
        {"validation_id": "VAL2744_10_pycache_absent", "passed": pycache_ok, "detail": f"scripts __pycache__ absent={pycache_ok}", "timestamp_utc": ts()},
        {"validation_id": "VAL2744_11_formalization_untouched", "passed": formalization_ok, "detail": f"formalization-workbench recent modified-file count since script start = {formalization_count}", "timestamp_utc": ts()},
    ]
    rows.append(
        {
            "validation_id": "VAL2744_OVERALL",
            "passed": all(row["passed"] is True for row in rows),
            "detail": "2744 formalizes the R_AB=0 closure benchmark, separates derived/assumed/test-required local conditions, and selects closure-deviation sensitivity next",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        f"""# 2744 - Y5 R2/f(R): Local Closure PPN Benchmark Derived-vs-Assumed Ledger Under AX1090

Status: `Y5_R2FR_2744_local_closure_ppn_benchmark_nonclaim_deviation_budget_next`

## Private Verdict

2744 stops the local branch from cheating and also keeps its strongest useful result.

Under the explicit closure

`T^2=1-L`, `R_AB=ln(T^2 S)=0`, `Q_R=0`,

we get

`S=1/T^2=1/(1-L)`, `p=1`, and `gamma=1`.

That is the clean local GR control lane. It is useful because it gives a benchmark against which deviations can be tested. It is not a parent derivation because `R_AB=0`, `Q_R=0`, beta completion, conservation, source normalization, and matter universality remain unproved by the parent theory.

So the next move is no longer verbal derivation. It is a sensitivity/bound budget: if residual reciprocal hair or coupling drift survives, how large can it be before R10/PPN/clocks/orbits kill it?

## Source Register

{markdown_table(data["sources"], ["source_id", "description", "source_path", "exists", "needles_present", "missing_needles", "valid_for_claim"])}

## Closure Assumption Ledger

{markdown_table(data["assumptions"], ["assumption_id", "statement", "classification", "reason", "valid_for_claim"])}

## Derived vs Assumed Ledger

{markdown_table(data["derived"], ["ledger_id", "quantity", "status", "basis", "limitation", "valid_for_claim"])}

## PPN Benchmark Requirements

{markdown_table(data["ppn"], ["ppn_id", "observable", "closure_value_or_condition", "benchmark_status", "remaining_requirement", "valid_for_claim"])}

## Observable Control Values

{markdown_table(data["controls"], ["observable_id", "observable", "control_value", "units", "status", "valid_for_claim"])}

## Closure Benchmark Runner

{markdown_table(data["runner"], ["runner_id", "check", "current_status", "reason", "valid_for_claim"])}

## Decision Ledger

{markdown_table(data["decisions"], ["decision_id", "decision", "result", "rationale", "valid_for_claim"])}

## Claim Gates

{markdown_table(data["gates"], ["claim_gate_id", "claim", "gate_passed", "status", "claim_allowed", "valid_for_claim", "reason"])}

## Next Target

{markdown_table(data["next"], ["next_id", "status", "target_doc", "target_script", "mission", "acceptance", "forbidden", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(data["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(data["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}

## Plain-English Read

This is a good place to be, because now the argument is honest enough to test. We have a closure lane that lands on the GR control values, but we are not pretending it is derived. The next round is where the gloves come back on: quantify the allowed deviation budget and see whether the remaining hair/coupling terms can survive real local bounds.
""",
        encoding="utf-8",
    )


def main() -> None:
    ensure_dirs()
    sources = source_rows()
    assumptions = assumption_rows()
    derived = derived_rows()
    ppn = ppn_rows()
    controls = control_rows()
    runner = runner_rows()
    decisions = decision_rows()
    gates = gate_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["assumptions"], assumptions)
    write_csv(OUTPUTS["derived"], derived)
    write_csv(OUTPUTS["ppn"], ppn)
    write_csv(OUTPUTS["controls"], controls)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["next"], next_target)

    write_csv(BRANCH_OUTPUTS["derived"], derived)
    write_csv(BRANCH_OUTPUTS["ppn"], ppn)
    write_csv(BRANCH_OUTPUTS["next_queue"], next_target)
    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)

    remove_pycache()
    validation = validation_rows(sources, assumptions, derived, ppn, controls, runner, gates, next_target)
    write_csv(OUTPUTS["validation"], validation)

    data = {
        "sources": sources,
        "assumptions": assumptions,
        "derived": derived,
        "ppn": ppn,
        "controls": controls,
        "runner": runner,
        "decisions": decisions,
        "gates": gates,
        "next": next_target,
        "branches": branches,
        "validation": validation,
    }
    write_doc(data)

    remove_pycache()

    if not all(row["passed"] is True for row in validation):
        failed = [row for row in validation if row["passed"] is not True]
        raise SystemExit(f"2744 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

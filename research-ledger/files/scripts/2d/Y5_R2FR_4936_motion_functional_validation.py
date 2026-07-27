from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "4936"
OUTPUT_DIR = POST / "source-intake" / "mts_residuals"
OUTPUT = OUTPUT_DIR / "P8_Y5_BRR545_4936_VALIDATION.csv"

CHECKPOINT = POST / "4936-Y5-R2FR-motion-1PI-mass-and-O4-functional-trace-projection-or-two-scale-predictivity-gate.md"
FORMAL_NOTE = FORMAL / "952-PPC4161-motion-functional-completion-and-predictivity-gate.md"
PROVENANCE = SOURCE / "PROVENANCE.md"
CLAIMS = FORMAL / "02-claims-register.csv"
VARIABLES = FORMAL / "04-variable-audit.csv"
EQUATIONS = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
SPINE = FORMAL / "07-unification-spine.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"

EXTRACTOR = POST / "scripts" / "Y5_R2FR_4936_scalar_notebook_box_extractor.py"
FRACTIONAL_SCRIPT = POST / "scripts" / "Y5_R2FR_4936_fractional_potential_LPA_closure.py"
SOURCE_SCRIPT = POST / "scripts" / "Y5_R2FR_4936_scalar_source_flow_evaluator.py"
O4_SCRIPT = POST / "scripts" / "Y5_R2FR_4936_O4_functional_trace_projection.py"
GATE_SCRIPT = POST / "scripts" / "Y5_R2FR_4936_motion_predictivity_gate.py"
NOTEBOOK = SOURCE / "flows.nb"
PAPER = POST / "source-intake" / "functional_rg" / "4929" / "src2204" / "R2scalarMES.tex"
MANIFEST = SOURCE / "flows_extraction_manifest.json"
FRACTIONAL_JSON = SOURCE / "fractional_potential_LPA_closure_results.json"
FRACTIONAL_SERIES = SOURCE / "fractional_potential_generated_operator_series.csv"
SOURCE_JSON = SOURCE / "scalar_source_flow_evaluation_results.json"
SOURCE_TABLE = SOURCE / "scalar_source_fixed_point_reproduction.csv"
O4_JSON = SOURCE / "O4_functional_trace_projection_results.json"
O4_TABLE = SOURCE / "O4_source_channel_projection.csv"
GATE_JSON = SOURCE / "motion_predictivity_gate_results.json"
ROUTE_TABLE = SOURCE / "motion_predictivity_route_gate.csv"

MARKER = "MTS_MOTION_FUNCTIONAL_COMPLETION_AND_PREDICTIVITY_GATE_4936"
FORMAL_MARKER = "PPC4161_MOTION_FUNCTIONAL_COMPLETION_AND_PREDICTIVITY_GATE_4936"
VALIDATION_MARKER = "MTS_MOTION_FUNCTIONAL_COMPLETION_AND_PREDICTIVITY_VALIDATION_4936"
NEXT_TARGET = "4937-Y5-R2FR-gravity-motion-functional-potential-Hessian-and-one-scale-fixed-function-gate.md"
CHECKED_DATE = "2026-07-12"

SCRIPTS = (
    EXTRACTOR,
    FRACTIONAL_SCRIPT,
    SOURCE_SCRIPT,
    O4_SCRIPT,
    GATE_SCRIPT,
    Path(__file__),
)
HASH_LOCKS = {
    NOTEBOOK: "841302a39fcf8e665c7dd6ded43a77bedb37dbdce4c2b2cf571b4a48da565bc6",
    PAPER: "56a906bdfef4af8c1e7a337263636bd0b2d5c863b5d5c52382385b655da4bdd7",
    EXTRACTOR: "a3008e6647fa992de593e8d0a900ae66ebc949e941ca6700766d3f97994d5128",
    FRACTIONAL_SCRIPT: "19fa49810c88c39b8bc47afc097b6cdfe18bbda483e280bcbbff0c43504965e9",
    SOURCE_SCRIPT: "d17d4c18cc1b348488c46dfb23ca83a2e320442b4eb3ecb45822e2457ca47eec",
    O4_SCRIPT: "4249bf7a6916a0aebf5e8f910a8104c55f45d1dd379e83ade03dabe9a4178d49",
    GATE_SCRIPT: "411470e8149d323bbee820dc5a9c16cff73b7a4f3e899993eb1fee7201f5165a",
    MANIFEST: "d4b8c06044a271ceaba8956e57870ffdf0ee8cecf04e1494559da8fa9424909c",
    FRACTIONAL_JSON: "8af1d8bf764372917991126c86de63847714f1a48ca4f5eb0925d1b91a4fdf96",
    FRACTIONAL_SERIES: "6d960c98d1b5011887463a3ab5f4da38abb2b62e750d0655a4a1495b51f28cae",
    SOURCE_JSON: "ab7394cf0ea455b40ec8678f5bb5cf34025657a51af499b5e92825b993dd6359",
    SOURCE_TABLE: "e3ac7ef71329d751cd618b61b9b8a3989e39c9e6b05d4c4d829b8edc5d13461f",
    O4_JSON: "06f6663105791669020729e21227db5007d696ea22d184081c9069d2d3d9bc99",
    O4_TABLE: "fdbf93ee1e705bcd9367d258b7b61b3b3f5dfddaf0287979bad58120032e056c",
    GATE_JSON: "e3e329b33c084fbe7e15f0f9e6c805cedb44581c4c7fffc165fef139f153fdd4",
    ROUTE_TABLE: "922c1ad3e0431a05b084289044dda584677ec88f7b0f57ea620b582f155a6230",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def add_check(
    checks: list[dict[str, Any]],
    check_id: str,
    requirement: str,
    expected: str,
    actual: str,
    passed: bool,
) -> None:
    checks.append(
        {
            "validation_id": check_id,
            "requirement": requirement,
            "expected": expected,
            "actual": actual,
            "passed": passed,
            "checkpoint_marker": VALIDATION_MARKER,
            "valid_for_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
    )


def main() -> int:
    checks: list[dict[str, Any]] = []
    required = [
        *SCRIPTS,
        *HASH_LOCKS,
        CHECKPOINT,
        FORMAL_NOTE,
        PROVENANCE,
        CLAIMS,
        VARIABLES,
        EQUATIONS,
        RED_TEAM,
        SPINE,
        RESUME,
    ]
    missing = sorted(str(path) for path in set(required) if not path.exists())
    add_check(
        checks,
        "VAL4936_00_paths",
        "all sources scripts results documents and registers exist",
        "0 missing paths",
        str(missing),
        not missing,
    )

    syntax_errors = []
    for path in SCRIPTS:
        try:
            compile(read_text(path), str(path), "exec")
        except SyntaxError as error:
            syntax_errors.append(f"{path.name}:{error}")
    add_check(
        checks,
        "VAL4936_01_compile",
        "all six checkpoint scripts compile without bytecode",
        "0 syntax errors",
        str(syntax_errors),
        not syntax_errors,
    )

    hash_failures = []
    for path, expected in HASH_LOCKS.items():
        actual = digest(path) if path.exists() else "MISSING"
        if actual != expected:
            hash_failures.append(f"{path.name}:{actual}")
    add_check(
        checks,
        "VAL4936_02_hashes",
        "primary sources generators and executed artifacts match locked hashes",
        f"{len(HASH_LOCKS)} matches",
        "OK" if not hash_failures else str(hash_failures),
        not hash_failures,
    )

    manifest = load_json(MANIFEST)
    input_failures = [
        failure
        for failure in manifest["parse_failures"]
        if failure["style"] == "Input"
    ]
    manifest_ok = (
        manifest["source_sha256"] == HASH_LOCKS[NOTEBOOK]
        and manifest["boxdata_cells_found"] == 27
        and manifest["input_cells"] == 25
        and manifest["output_cells"] == 2
        and not input_failures
        and manifest["raw_output_fallback_cells"] == [25]
    )
    add_check(
        checks,
        "VAL4936_03_notebook_extraction",
        "all input cells convert and the one parser-limited stored output remains raw",
        "27 cells; 25 input; 2 output; no input failure; raw output cell 25",
        str(manifest),
        manifest_ok,
    )

    fractional = load_json(FRACTIONAL_JSON)
    add_check(
        checks,
        "VAL4936_04_fractional_internal",
        "all exact fractional-flow closure and coordinate checks pass",
        "all true",
        str(fractional["checks"]),
        all(fractional["checks"].values()),
    )
    fractional_boundary = fractional["claim_boundary"]
    fractional_boundary_ok = (
        not fractional_boundary["fractional_one_coupling_LPA_closed"]
        and not fractional_boundary["scalar_only_fractional_fixed_point_derived"]
        and fractional_boundary["exact_escape_routes_derived"]
        and not fractional_boundary["mass_gap_coefficient_derived"]
        and not fractional_boundary["full_MTS_trajectory_calculated"]
        and not fractional_boundary["local_GR_Newton_Maxwell_promoted"]
    )
    add_check(
        checks,
        "VAL4936_05_fractional_boundary",
        "one-coupling closure and scalar fixed point are false while escape contracts are derived",
        "closure=false; fixed point=false; escape=true; full/local=false",
        str(fractional_boundary),
        fractional_boundary_ok,
    )

    fixed_test = fractional["fixed_point_test"]
    fixed_test_ok = (
        fixed_test["eta_for_classical_fractional_marginality"] == [4]
        and fixed_test["eta_for_optimized_scalar_trace_silence"] == [6]
        and fixed_test["common_eta"] == []
        and fixed_test["eta_four_leading_q_coefficient"]
        == "1/(32*pi**2*g_tilde)"
    )
    add_check(
        checks,
        "VAL4936_06_eta_fork",
        "marginality and optimized trace silence require incompatible eta values",
        "eta=4 versus eta=6; no intersection; eta4 q source nonzero",
        str(fixed_test),
        fixed_test_ok,
    )

    series_rows = read_csv(FRACTIONAL_SERIES)
    series_ok = (
        len(series_rows) == 6
        and series_rows[0]["varphi_power"] == "2/3"
        and series_rows[0]["inside_original_one_coupling_span"] == "False"
        and series_rows[1]["inside_original_one_coupling_span"] == "True"
        and all(row["valid_for_claim"] == "False" for row in series_rows)
        and all(
            row["checkpoint_marker"]
            == "MTS_4936_FRACTIONAL_POTENTIAL_LPA_CLOSURE"
            for row in series_rows
        )
    )
    add_check(
        checks,
        "VAL4936_07_generated_series",
        "six generated channels parse and the leading q operator lies outside the truncation",
        "6 private rows; q outside; q2 inside",
        str(series_rows),
        series_ok,
    )

    source_flow = load_json(SOURCE_JSON)
    add_check(
        checks,
        "VAL4936_08_source_internal",
        "all independent source-flow parsing root spectrum and series checks pass",
        "all true",
        str(source_flow["checks"]),
        all(source_flow["checks"].values()),
    )
    source_points = source_flow["fixed_points"]
    source_points_ok = (
        source_points["A"]["relevant_directions"] == 2
        and source_points["B"]["relevant_directions"] == 1
        and all(
            point["beta_residual_infinity_norm"] < 1.0e-10
            for point in source_points.values()
        )
        and source_flow["derived_source_channels"][
            "leading_additive_gravity_source"
        ]
        == "406/5"
    )
    add_check(
        checks,
        "VAL4936_09_source_reproduction",
        "source A and B spectra reproduce with tiny residual and the additive source is 406/5",
        "A relevant=2; B relevant=1; residual<1e-10; source=406/5",
        str(source_points),
        source_points_ok,
    )

    source_rows = read_csv(SOURCE_TABLE)
    source_table_ok = (
        len(source_rows) == 2
        and {row["fixed_point"] for row in source_rows} == {"A", "B"}
        and all(row["source_reproduced"] == "True" for row in source_rows)
        and all(
            row["valid_for_MTS_motion_claim"] == "False" for row in source_rows
        )
    )
    add_check(
        checks,
        "VAL4936_10_source_table",
        "the two source fixed-point rows are reproduced and firewalled from MTS claims",
        "A and B; reproduced=true; MTS claim=false",
        str(source_rows),
        source_table_ok,
    )

    o4 = load_json(O4_JSON)
    add_check(
        checks,
        "VAL4936_11_O4_internal",
        "all O4 projector source-channel and claim-boundary checks pass",
        "all true",
        str(o4["checks"]),
        all(o4["checks"].values()),
    )
    o4_boundary = o4["claim_boundary"]
    o4_boundary_ok = (
        o4_boundary["O4_projector_derived"]
        and o4_boundary["free_scalar_additive_O4_source_zero_proved"]
        and not o4_boundary["fractional_scalar_O4_vacuum_projection_finite"]
        and o4_boundary["gravity_motion_additive_channel_proved"]
        and not o4_boundary["numeric_O4_beta_coefficient_derived"]
    )
    add_check(
        checks,
        "VAL4936_12_O4_boundary",
        "projector and free zero are true while fractional finiteness and numeric mixed coefficient are false",
        "projector=true; free zero=true; finite=false; channel=true; coefficient=false",
        str(o4_boundary),
        o4_boundary_ok,
    )

    o4_rows = read_csv(O4_TABLE)
    o4_table_ok = (
        len(o4_rows) == 5
        and any(
            row["status"] == "ZERO_PROVED"
            and row["additive_O4_source"] == "0"
            for row in o4_rows
        )
        and any(
            row["status"]
            == "CHANNEL_NONZERO_PROVED_COEFFICIENT_REQUIRES_SIX_DERIVATIVE_TRACE"
            for row in o4_rows
        )
        and all(row["valid_for_claim"] == "False" for row in o4_rows)
    )
    add_check(
        checks,
        "VAL4936_13_O4_channels",
        "five private O4 channel rows distinguish exact zero singular and mixed-source cases",
        "5 rows; free zero; mixed coefficient required; private",
        str(o4_rows),
        o4_table_ok,
    )

    gate = load_json(GATE_JSON)
    add_check(
        checks,
        "VAL4936_14_gate_internal",
        "all route and logistic map checks pass",
        "all true",
        str(gate["checks"]),
        all(gate["checks"].values()),
    )
    gate_boundary = gate["claim_boundary"]
    gate_boundary_ok = (
        not gate_boundary["motion_sector_rejected"]
        and gate_boundary["one_coupling_fractional_realization_rejected"]
        and gate_boundary["functional_completion_selected"]
        and not gate_boundary["MTS_motion_fixed_function_derived"]
        and gate_boundary["galaxy_logistic_shape_kinematically_derived"]
        and not gate_boundary["galaxy_logistic_parent_amplitudes_identified"]
        and not gate_boundary["full_MTS_trajectory_calculated"]
        and not gate_boundary["local_GR_Newton_Maxwell_promoted"]
    )
    add_check(
        checks,
        "VAL4936_15_gate_boundary",
        "motion survives only through functional completion and all physical/full claims remain blocked",
        "motion rejected=false; one-coupling=true; functional=true; physical/full/local=false",
        str(gate_boundary),
        gate_boundary_ok,
    )

    route_rows = read_csv(ROUTE_TABLE)
    selected = [row for row in route_rows if row["selected_next"] == "True"]
    route_ok = (
        len(route_rows) == 5
        and len(selected) == 1
        and selected[0]["route_id"] == "MP4936_R4_functional_motion_potential"
        and selected[0]["result"] == "SELECTED"
        and all(row["valid_for_claim"] == "False" for row in route_rows)
    )
    add_check(
        checks,
        "VAL4936_16_routes",
        "exactly one of five private routes is selected and it is the full functional potential",
        "5 rows; selected=R4 only; private",
        str(route_rows),
        route_ok,
    )

    galaxy = gate["galaxy_phase_flow_interface"]
    galaxy_ok = (
        "dn/d ln R=q n(1-n)" in galaxy["derived_bounded_flow"]
        and "db/d ln R=-s b(1-b)" in galaxy["derived_bounded_flow"]
        and math.isclose(
            galaxy["conditional_source_B_example_not_MTS_prediction"]["q"],
            1.9673128628101106,
            rel_tol=1.0e-14,
        )
        and math.isclose(
            galaxy["conditional_source_B_example_not_MTS_prediction"]["s"],
            0.40887640805947983,
            rel_tol=1.0e-14,
        )
        and len(galaxy["ownership_requirements"]) == 4
    )
    add_check(
        checks,
        "VAL4936_17_galaxy_interface",
        "the logistic identities and conditional source example are explicit with four ownership requirements",
        "two equations; q/s source example; 4 pending ownership clauses",
        str(galaxy),
        galaxy_ok,
    )

    documents = {
        "checkpoint": read_text(CHECKPOINT),
        "formal": read_text(FORMAL_NOTE),
        "provenance": read_text(PROVENANCE),
        "claims": read_text(CLAIMS),
        "variables": read_text(VARIABLES),
        "equations": read_text(EQUATIONS),
        "red_team": read_text(RED_TEAM),
        "spine": read_text(SPINE),
        "resume": read_text(RESUME),
    }
    markers = {
        "checkpoint": MARKER,
        "formal": FORMAL_MARKER,
        "provenance": "MTS_MOTION_FUNCTIONAL_COMPLETION_AND_PREDICTIVITY_PROVENANCE_4936",
        "claims": "L-778",
        "variables": "PredictivityStatus4936_MTS",
        "equations": "## 1.229 Motion functional closure, O4 projection and phase-flow interface",
        "red_team": "## 180. A dimensionally attractive fractional potential is not an RG-closed theory",
        "spine": "## PPC4161 checkpoint 4936 - motion functional completion and predictivity gate",
        "resume": NEXT_TARGET,
    }
    missing_markers = [
        name for name, marker in markers.items() if marker not in documents[name]
    ]
    add_check(
        checks,
        "VAL4936_18_registers",
        "checkpoint provenance formal note registers and resume contain the 4936 markers",
        "0 missing markers",
        str(missing_markers),
        not missing_markers,
    )

    claim_rows = [
        row for row in read_csv(CLAIMS) if row.get("claim_id") == "L-778"
    ]
    claim_ok = (
        len(claim_rows) == 1
        and "full_MTS_fixed_function_false" in claim_rows[0]["status"]
        and "local GR" in claim_rows[0]["risk"]
        and NEXT_TARGET in claim_rows[0]["next_test"]
    )
    add_check(
        checks,
        "VAL4936_19_claim_policy",
        "the single L-778 row rejects only the one-coupling route and blocks full/local promotion",
        "one row; full=false; local prohibited; next=4937",
        str(claim_rows),
        claim_ok,
    )

    csv_register_errors = []
    for path in (CLAIMS, VARIABLES):
        rows = read_csv(path)
        malformed = [
            index
            for index, row in enumerate(rows, start=2)
            if None in row or any(value is None for value in row.values())
        ]
        if malformed:
            csv_register_errors.append(f"{path.name}:{malformed[:10]}")
    add_check(
        checks,
        "VAL4936_20_csv_registers",
        "claims and variable registers parse without malformed rows",
        "0 malformed rows",
        str(csv_register_errors),
        not csv_register_errors,
    )

    placeholders = [
        path.name
        for path in (CHECKPOINT, FORMAL_NOTE, PROVENANCE)
        if "MISSING_" in read_text(path)
    ]
    add_check(
        checks,
        "VAL4936_21_placeholders",
        "authored checkpoint documents contain no MISSING_ placeholders",
        "0 documents",
        str(placeholders),
        not placeholders,
    )

    cache_paths = sorted(str(path) for path in POST.rglob("__pycache__"))
    add_check(
        checks,
        "VAL4936_22_cache",
        "no Python bytecode cache directories remain under post-checkpoint-work",
        "0 __pycache__ directories",
        str(cache_paths),
        not cache_paths,
    )

    nonclaim_tables = (FRACTIONAL_SERIES, SOURCE_TABLE, O4_TABLE, ROUTE_TABLE)
    claim_leaks = []
    for path in nonclaim_tables:
        for index, row in enumerate(read_csv(path), start=2):
            relevant = [
                value
                for key, value in row.items()
                if key in {"valid_for_claim", "valid_for_MTS_motion_claim"}
            ]
            if not relevant or any(value != "False" for value in relevant):
                claim_leaks.append(f"{path.name}:{index}:{relevant}")
    add_check(
        checks,
        "VAL4936_23_nonclaim",
        "every generated evidence row remains private and invalid for an MTS claim",
        "0 claim leaks",
        str(claim_leaks),
        not claim_leaks,
    )

    all_prior_pass = all(bool(row["passed"]) for row in checks)
    add_check(
        checks,
        "VAL4936_24_gate",
        "all prior 4936 checks pass while full MTS fixed-function and local claims remain false",
        "all prior true; full/local=false",
        f"prior_passed={all_prior_pass}; prior_rows={len(checks)}",
        all_prior_pass
        and not gate_boundary["MTS_motion_fixed_function_derived"]
        and not gate_boundary["local_GR_Newton_Maxwell_promoted"],
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fields = [
        "validation_id",
        "requirement",
        "expected",
        "actual",
        "passed",
        "checkpoint_marker",
        "valid_for_claim",
        "source_checked_date",
    ]
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(checks)

    failed = [row["validation_id"] for row in checks if not row["passed"]]
    print(f"Wrote {OUTPUT}")
    print(f"Checks: {len(checks)}; failed: {failed}")
    print(
        "Selected route: "
        f"{gate['decision']['selected_route']}"
    )
    print(
        "Fractional one-coupling closure: "
        f"{fractional_boundary['fractional_one_coupling_LPA_closed']}"
    )
    print(
        "Full MTS fixed function: "
        f"{gate_boundary['MTS_motion_fixed_function_derived']}"
    )
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())

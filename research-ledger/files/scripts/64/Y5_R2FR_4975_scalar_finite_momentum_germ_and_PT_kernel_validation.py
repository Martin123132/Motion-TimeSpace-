from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

from scipy.integrate import quad


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "4975"
OUTPUT = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_4975_VALIDATION.csv"

RUNNER = POST / "scripts" / "Y5_R2FR_4975_scalar_finite_momentum_germ_and_PT_kernel.py"
CHECKPOINT = POST / "4975-Y5-R2FR-scalar-finite-momentum-germ-proper-time-kernel-and-dimension8-leakage-verdict.md"
FORMAL_NOTE = FORMAL / "991-PPC4161-scalar-finite-momentum-germ-and-dimension8-leakage.md"
RESULT = SOURCE / "C3_scalar_finite_momentum_germ_and_PT_kernel_results.json"
RESPONSES = SOURCE / "C3_scalar_q6_q8_Taylor_responses.csv"
PROJECTION = SOURCE / "C3_scalar_q6_q8_quotient_projection.csv"
LEAVE_ONE = SOURCE / "C3_scalar_q8_leave_one_geometry.csv"
MASS = SOURCE / "C3_scalar_mass_homogeneity.csv"
KERNEL = SOURCE / "C3_scalar_PT_m3_q6_q8_kernel.csv"
GATES = SOURCE / "C3_scalar_finite_momentum_germ_gate.csv"
PROVENANCE = SOURCE / "PROVENANCE.md"

RESUME = POST / "CURRENT_LOCAL_RESUME.md"
SPINE = POST / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"
VARIABLES = FORMAL / "04-variable-audit.csv"
CLAIMS = FORMAL / "02-claims-register.csv"
EQUATIONS = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
UNIFICATION = FORMAL / "07-unification-spine.md"

SCIENTIFIC_MARKER = "MTS_4975_SCALAR_FINITE_MOMENTUM_GERM_AND_PT_KERNEL"
FORMAL_MARKER = "PPC4161_SCALAR_FINITE_MOMENTUM_GERM_4975"
VALIDATION_MARKER = "MTS_4975_SCALAR_FINITE_MOMENTUM_GERM_VALIDATION"
TARGET = 1.0 / (30240.0 * (4.0 * math.pi) ** 2)

EXPECTED_HASHES = {
    RUNNER: "005dbcc850c8a617465d2c4c93e4207c258f5b91583533776ce05acc726a053d",
    CHECKPOINT: "935a777377bcbef94b286ce722a10791793a60ffb40afdd3830ef628eda1bcf5",
    FORMAL_NOTE: "a36e4f40032f2224ee33d999b43038eb064e444fe361a8aaa25a425e01bfdf6a",
    RESULT: "3f7b1fd80adf5d60f52948ac565813ac6f56149a2852cf195130597b943737af",
    RESPONSES: "6ba140d2f6ff6f85cf7da391eb946275eb7dc06d35c315d6bc92c3ae0e6f96a9",
    PROJECTION: "2b8bf4bbabe521e3fa8743dedb9b58a9c23237adfbe751cdca7a09bc42d4ec33",
    LEAVE_ONE: "fb8f359bdacc26620c56194e6a17a315dad9dd8efbb60d0281e86d4875ffc408",
    MASS: "d29ab527d9ed8c3b08d0b5c32a7417f24065d5753b1fbafd7c7b11f93598bdcc",
    KERNEL: "04198a79dc5ef31ad02cc446b503f06771b3ba8c48ccb2597b777a796c1df12e",
    GATES: "d46b8ac2ba046458c4d9585e421c99eeb87ebcd578d06607b01322496ddab0ca",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def widths(path: Path) -> set[int]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return {len(row) for row in csv.reader(handle)}


def check_row(
    index: int,
    name: str,
    observed: Any,
    required: Any,
    passed: bool,
) -> dict[str, Any]:
    return {
        "validation_id": f"VAL4975_{index:02d}",
        "check": name,
        "observed": observed,
        "required": required,
        "status": "PASS" if passed else "FAIL",
        "checkpoint_marker": VALIDATION_MARKER,
        "valid_for_full_MTS_claim": False,
        "source_checked_date": "2026-07-13",
    }


def main() -> int:
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    responses = read_csv(RESPONSES)
    projections = read_csv(PROJECTION)
    leave_one = read_csv(LEAVE_ONE)
    mass_rows = read_csv(MASS)
    kernel_rows = read_csv(KERNEL)
    gate_rows = read_csv(GATES)
    rows: list[dict[str, Any]] = []

    hash_pass = all(path.exists() and digest(path) == expected for path, expected in EXPECTED_HASHES.items())
    rows.append(check_row(len(rows), "runner checkpoint formal note and generated outputs are hash locked", hash_pass, True, hash_pass))

    expected_counts = {RESPONSES: 24, PROJECTION: 2, LEAVE_ONE: 12, MASS: 6, KERNEL: 13, GATES: 8}
    observed_counts = {path.name: len(read_csv(path)) for path in expected_counts}
    count_pass = all(observed_counts[path.name] == count for path, count in expected_counts.items())
    rows.append(check_row(len(rows), "generated CSV row counts", json.dumps(observed_counts, sort_keys=True), json.dumps({path.name: count for path, count in expected_counts.items()}, sort_keys=True), count_pass))

    width_pass = all(len(widths(path)) == 1 for path in expected_counts) and widths(VARIABLES) == {11} and widths(CLAIMS) == {13}
    rows.append(check_row(len(rows), "all generated and canonical CSV files have constant widths", width_pass, True, width_pass))

    scientific_rows = responses + projections + leave_one + mass_rows + kernel_rows + gate_rows
    nonclaim_pass = all(row["checkpoint_marker"] == SCIENTIFIC_MARKER and row["valid_for_full_MTS_claim"] == "False" for row in scientific_rows) and result["valid_for_full_MTS_claim"] is False
    rows.append(check_row(len(rows), "all scientific rows remain private nonclaim", nonclaim_pass, True, nonclaim_pass))

    selected = next(row for row in projections if row["config"] == "R24_A10_m1")
    q6_residual = float(selected["q6_relative_image_residual"])
    q6_target_residual = abs(float(selected["q6_zeta"]) / TARGET - 1.0)
    rows.append(check_row(len(rows), "q6 baseline quotient recovery", f"image={q6_residual:.17g};target={q6_target_residual:.17g}", "both <1e-8", q6_residual < 1.0e-8 and q6_target_residual < 1.0e-8))

    q8_leakages = [float(row["q8_relative_sigma1_image_residual"]) for row in projections]
    leakage_convergence = abs(q8_leakages[0] - q8_leakages[1])
    rows.append(check_row(len(rows), "q8 leakage is nonzero and quadrature converged", f"values={q8_leakages};difference={leakage_convergence:.17g}", "minimum >1e-6 and difference <1e-12", min(q8_leakages) > 1.0e-6 and leakage_convergence < 1.0e-12))

    vector_convergence = float(result["q8_vector_quadrature_convergence"])
    estimator_convergence = float(result["q8_estimator_quadrature_convergence"])
    rows.append(check_row(len(rows), "independent q8 convergence summaries", f"vector={vector_convergence:.17g};estimator={estimator_convergence:.17g}", "both <1e-8", vector_convergence < 1.0e-8 and estimator_convergence < 1.0e-8))

    zetas = [float(row["q8_projected_channel_estimator"]) for row in leave_one]
    rows.append(check_row(len(rows), "leave-one diagnostic estimator changes sign", f"minimum={min(zetas):.17g};maximum={max(zetas):.17g}", "minimum <0 and maximum >0", min(zetas) < 0.0 < max(zetas)))

    maximum_shift = max(float(row["relative_shift_from_full_estimator"]) for row in leave_one)
    rows.append(check_row(len(rows), "leave-one instability blocks coefficient promotion", maximum_shift, ">1 diagnostic rejection", maximum_shift > 1.0))

    mass_residual = max(float(row["absolute_scaling_residual"]) for row in mass_rows)
    powers = {(int(row["Taylor_order"]), int(row["dimension_power_of_mass"])) for row in mass_rows}
    rows.append(check_row(len(rows), "q6 and q8 mass homogeneity", f"max={mass_residual};powers={sorted(powers)}", "max <1e-12 and powers [(6,-2),(8,-4)]", mass_residual < 1.0e-12 and powers == {(6, -2), (8, -4)}))

    q6_integral = quad(lambda x: 3.0 * x**2 / (1.0 + x) ** 4, 0.0, math.inf, epsabs=1.0e-13, epsrel=1.0e-13)[0]
    q8_integral = quad(lambda x: 12.0 * x**2 / (1.0 + x) ** 5, 0.0, math.inf, epsabs=1.0e-13, epsrel=1.0e-13)[0]
    rows.append(check_row(len(rows), "independent proper-time kernel integrals", f"q6={q6_integral:.17g};q8={q8_integral:.17g}", "both equal one within 1e-12", abs(q6_integral - 1.0) < 1.0e-12 and abs(q8_integral - 1.0) < 1.0e-12))

    cumulative_values = [float(row["q8_cumulative_UV_to_IR_fraction"]) for row in kernel_rows]
    cumulative_pass = all(left <= right for left, right in zip(cumulative_values, cumulative_values[1:])) and cumulative_values[0] < 1.0e-20 and 1.0 - cumulative_values[-1] < 1.0e-7
    rows.append(check_row(len(rows), "q8 cumulative profile is monotone with correct endpoints", f"first={cumulative_values[0]:.17g};last={cumulative_values[-1]:.17g}", "monotone first~0 last~1", cumulative_pass))

    rank_pass = result["q6_rank"] == 8 and result["q8_sigma1_dressed_rank"] == 8 and float(result["q6_C3_null_map_residual"]) < 1.0e-10 and float(result["q8_C3_null_map_residual"]) < 1.0e-10
    rows.append(check_row(len(rows), "restricted quotient rank and C3 nullspace invariance", json.dumps({key: result[key] for key in ("q6_rank", "q8_sigma1_dressed_rank", "q6_C3_null_map_residual", "q8_C3_null_map_residual")}, sort_keys=True), "ranks 8 and residuals <1e-10", rank_pass))

    result_ceiling = result["pure_C3_form_factor_derivative_identified"] is False and result["massless_limit_status"] == "NONUNIFORM_NOT_TAKEN_FROM_LOCAL_TAYLOR_GERM" and result["all_internal_gates_pass"] is True
    rows.append(check_row(len(rows), "result enforces C3 and massless-limit claim ceilings", result_ceiling, True, result_ceiling))

    gate_pass = all(row["passed"] == "True" for row in gate_rows)
    rows.append(check_row(len(rows), "runner internal gates", f"{sum(row['passed'] == 'True' for row in gate_rows)}/{len(gate_rows)}", "8/8", gate_pass and len(gate_rows) == 8))

    sentinel_text = "\n".join(path.read_text(encoding="utf-8", errors="replace") for path in (CHECKPOINT, FORMAL_NOTE, RESULT, RESPONSES, PROJECTION, LEAVE_ONE, MASS, KERNEL, GATES, PROVENANCE))
    rows.append(check_row(len(rows), "generated checkpoint contains no placeholder sentinel", sentinel_text.count("MISSING_"), 0, "MISSING_" not in sentinel_text))

    handoff_paths = (CHECKPOINT, FORMAL_NOTE, RESUME, SPINE, EQUATIONS, RED_TEAM, UNIFICATION)
    handoff_pass = all(path.exists() and FORMAL_MARKER in path.read_text(encoding="utf-8", errors="replace") for path in handoff_paths)
    rows.append(check_row(len(rows), "checkpoint marker propagated through handoff documents", handoff_pass, True, handoff_pass))

    variable_rows = read_csv(VARIABLES)
    expected_symbols = {"ScalarTaylorQ6_4975_MTS", "ScalarTaylorQ8Vector_4975_MTS", "Sigma1_4975_MTS", "C3Q8Estimator4975_MTS", "PTQ8Kernel4975_MTS", "PredictivityStatus4975_MTS"}
    observed_symbols = {row["symbol"] for row in variable_rows if row["symbol"] in expected_symbols}
    rows.append(check_row(len(rows), "canonical variable audit contains six 4975 entries", sorted(observed_symbols), sorted(expected_symbols), observed_symbols == expected_symbols))

    claim_rows = read_csv(CLAIMS)
    matching_claims = [row for row in claim_rows if row["claim_id"] == "L-817"]
    claim_pass = len(matching_claims) == 1 and FORMAL_MARKER in matching_claims[0]["notes"] and "FULL_MTS_FALSE" in matching_claims[0]["notes"]
    rows.append(check_row(len(rows), "claims register contains bounded L-817 exactly once", len(matching_claims), 1, claim_pass))

    provenance_text = PROVENANCE.read_text(encoding="utf-8")
    provenance_pass = all(expected in provenance_text for path, expected in EXPECTED_HASHES.items() if path not in (RUNNER, CHECKPOINT, FORMAL_NOTE)) and "No GitHub action was performed" in provenance_text
    rows.append(check_row(len(rows), "provenance records generated hashes and no GitHub action", provenance_pass, True, provenance_pass))

    source_paths = [Path(row["source_files"].split(";")[0]) for row in variable_rows if row["symbol"] in expected_symbols and row["source_files"].startswith("D:\\")]
    relative_sources = [ROOT / row["source_files"].split(";")[0] for row in variable_rows if row["symbol"] in expected_symbols and not row["source_files"].startswith("D:\\")]
    path_pass = all(path.exists() for path in source_paths + relative_sources)
    rows.append(check_row(len(rows), "first cited source path for each new variable exists", path_pass, True, path_pass))

    all_pass = all(row["status"] == "PASS" for row in rows)
    rows.append(check_row(len(rows), "overall checkpoint 4975 validation", f"{sum(row['status'] == 'PASS' for row in rows)}/{len(rows)} pre-overall", f"{len(rows)}/{len(rows)} pre-overall", all_pass))

    fields = list(rows[0])
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"{VALIDATION_MARKER} {sum(row['status'] == 'PASS' for row in rows)}/{len(rows)}")
    return 0 if all(row["status"] == "PASS" for row in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())

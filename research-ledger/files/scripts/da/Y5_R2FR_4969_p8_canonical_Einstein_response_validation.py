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
SOURCE = POST / "source-intake" / "functional_rg" / "4969"
RESIDUAL = POST / "source-intake" / "mts_residuals"
OUTPUT = RESIDUAL / "P8_Y5_BRR545_4969_VALIDATION.csv"
MARKER = "MTS_4969_P8_CANONICAL_EINSTEIN_RESPONSE_VALIDATION"
CHECKPOINT_MARKER = "PPC4161_P8_CANONICAL_EINSTEIN_SPLIT_4969"
CHECKED_DATE = "2026-07-13"

SPLIT_SCRIPT = POST / "scripts" / "Y5_R2FR_4969_p8_canonical_Einstein_split.py"
TRAJECTORY_SCRIPT = (
    POST / "scripts" / "Y5_R2FR_4969_p8_corrected_trajectory_and_primitive_response.py"
)
VALIDATION_SCRIPT = (
    POST / "scripts" / "Y5_R2FR_4969_p8_canonical_Einstein_response_validation.py"
)
SPLIT_JSON = SOURCE / "p8_canonical_Einstein_split_results.json"
TRAJECTORY_JSON = SOURCE / "p8_corrected_trajectory_primitive_response_results.json"
SOURCE_AUDIT_CSV = SOURCE / "pure_Einstein_three_loop_source_audit.csv"
SCALING_CSV = SOURCE / "p8_canonical_scaling_repair.csv"
SPLIT_CSV = SOURCE / "pure_Einstein_iterated_primitive_split.csv"
MATCHING_CSV = SOURCE / "functional_to_onshell_C3_matching_diagnostic.csv"
FIXED_CSV = SOURCE / "p8_canonical_repaired_fixed_point.csv"
TRAJECTORY_CSV = SOURCE / "p8_canonical_repaired_GR_connected_trajectory.csv"
CONVERGENCE_CSV = SOURCE / "p8_canonical_repaired_endpoint_convergence.csv"
STATIC_CSV = SOURCE / "p8_canonical_repaired_static_compact_response.csv"
RESPONSE_CSV = SOURCE / "pure_Einstein_IR_matching_response.csv"
BUDGET_CSV = SOURCE / "primitive_and_matching_boundary_budget.csv"
PROVENANCE = SOURCE / "PROVENANCE.md"
CHECKPOINT = (
    POST
    / "4969-Y5-R2FR-p8-canonical-repair-pure-Einstein-iterated-source-and-primitive-response.md"
)
FORMAL_NOTE = FORMAL / "985-PPC4161-p8-canonical-repair-and-Einstein-three-loop-split.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"
SPINE = POST / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"
VARIABLES = FORMAL / "04-variable-audit.csv"
CLAIMS = FORMAL / "02-claims-register.csv"
EQUATIONS = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
UNIFICATION = FORMAL / "07-unification-spine.md"
OLD_CHECKPOINTS = (
    POST
    / "4967-Y5-R2FR-C3-O4-p8-trajectory-UV-boundary-and-static-bound-or-CFF-Einstein-source-boundary.md",
    POST
    / "4968-Y5-R2FR-CFF-squared-four-graviton-p8-helicity-source-GR-trajectory-and-static-bound-or-three-loop-Einstein-residual.md",
    FORMAL / "983-PPC4161-C3-O4-p8-trajectory-and-static-boundary.md",
    FORMAL / "984-PPC4161-CFF-p8-helicity-source-and-completed-trajectory.md",
)
EXTRANEOUS_SEARCH_DUMP = SOURCE / "inspire_three_loop_Einstein_search.json"

EXPECTED_HASHES = {
    SOURCE / "src-2009.01042" / "Paper-QuantumGravity-V3.tex": (
        "8240be2d3f61b3e2a6103c6996aab3dfedeb9b2d56d5250694dfd11b6f7a8223"
    ),
    SOURCE / "src-1711.05526" / "PLBpaperBv3.tex": (
        "b7768f6a1ba4a32f5718c455f3042e97ef1cbfe806b88c1daa71b64fe5a1b6a1"
    ),
    SOURCE / "src-1701.02422" / "gr_simp.tex": (
        "9448bff31da3e1e56e62e8fb6242a60c09afb90d1f7f25edaf3f23466ac0371e"
    ),
    POST / "source-intake" / "functional_rg" / "4967" / "src-2010.13809" / "draft.tex": (
        "d2892e4163b5a70ff3f660e2a48ba91f7e7be246dd53d21b3aa874a3a1b13230"
    ),
    POST / "source-intake" / "functional_rg" / "4965" / "src-2103.12728" / "GravScatt.tex": (
        "6812e00f073074e6c045d3241125dc5cf1c73891ad250754b82cd19bae5e7963"
    ),
    POST / "source-intake" / "functional_rg" / "4929" / "src2312" / "ess_cubic.tex": (
        "b23b0974509278be22c8917f531a2963d415184d9052e27860c65fad80943a1d"
    ),
    POST / "source-intake" / "functional_rg" / "4963" / "C3_Wilson_selection_and_running.csv": (
        "c130ad2c49cce89682726377d459d3af7119a330c82af10a6c18bed770f7dfa0"
    ),
    SPLIT_JSON: "7e45bf69deb9e61df28ef640eb0f075e2689849673d8199526e459bfd2e2d2d7",
    TRAJECTORY_JSON: "1589bf28b9429c7f90ff8284b3db093b09cc0db5352daaad3d395e5546b7e220",
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


def write_csv(rows: list[dict[str, Any]]) -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "check_id",
        "requirement",
        "observed",
        "detail",
        "passed",
        "checkpoint_marker",
        "valid_for_full_MTS_claim",
        "source_checked_date",
    ]
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def validation_row(
    index: int,
    requirement: str,
    observed: str,
    detail: object,
    passed: bool,
) -> dict[str, Any]:
    return {
        "check_id": f"VAL4969_{index:02d}",
        "requirement": requirement,
        "observed": observed,
        "detail": json.dumps(detail, sort_keys=True, default=str),
        "passed": bool(passed),
        "checkpoint_marker": MARKER,
        "valid_for_full_MTS_claim": False,
        "source_checked_date": CHECKED_DATE,
    }


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    required_paths = [
        SPLIT_SCRIPT,
        TRAJECTORY_SCRIPT,
        VALIDATION_SCRIPT,
        *EXPECTED_HASHES,
        SOURCE_AUDIT_CSV,
        SCALING_CSV,
        SPLIT_CSV,
        MATCHING_CSV,
        FIXED_CSV,
        TRAJECTORY_CSV,
        CONVERGENCE_CSV,
        STATIC_CSV,
        RESPONSE_CSV,
        BUDGET_CSV,
        PROVENANCE,
        CHECKPOINT,
        FORMAL_NOTE,
        RESUME,
        SPINE,
        VARIABLES,
        CLAIMS,
        EQUATIONS,
        RED_TEAM,
        UNIFICATION,
        *OLD_CHECKPOINTS,
    ]
    missing_paths = [str(path) for path in required_paths if not path.exists()]
    rows: list[dict[str, Any]] = []
    rows.append(
        validation_row(
            len(rows),
            "all checkpoint source result document and register paths exist",
            f"{len(missing_paths)} missing paths",
            missing_paths,
            not missing_paths,
        )
    )

    compile_failures: list[str] = []
    for script in (SPLIT_SCRIPT, TRAJECTORY_SCRIPT, VALIDATION_SCRIPT):
        try:
            compile(script.read_text(encoding="utf-8"), str(script), "exec")
        except Exception as error:
            compile_failures.append(f"{script}: {error}")
    rows.append(
        validation_row(
            len(rows),
            "all 4969 scripts compile without execution or bytecode",
            f"{len(compile_failures)} compile failures",
            compile_failures,
            not compile_failures,
        )
    )

    hash_failures: dict[str, dict[str, str]] = {}
    hash_results: dict[str, str] = {}
    for path, expected in EXPECTED_HASHES.items():
        if not path.exists():
            continue
        actual = digest(path)
        relative = str(path.relative_to(ROOT))
        hash_results[relative] = actual
        if actual != expected:
            hash_failures[relative] = {"expected": expected, "actual": actual}
    rows.append(
        validation_row(
            len(rows),
            "all primary-source and authoritative-result hashes match",
            f"{len(hash_failures)} hash mismatches",
            hash_results,
            not missing_paths and not hash_failures,
        )
    )

    split = json.loads(SPLIT_JSON.read_text(encoding="utf-8"))
    trajectory = json.loads(TRAJECTORY_JSON.read_text(encoding="utf-8"))
    rows.append(
        validation_row(
            len(rows),
            "both calculation stages pass every internal check",
            f"split={split['all_checks_pass']}; trajectory={trajectory['all_checks_pass']}",
            {"split": split["checks"], "trajectory": trajectory["checks"]},
            split["all_checks_pass"] and trajectory["all_checks_pass"],
        )
    )

    repair = split["canonical_repair"]
    rows.append(
        validation_row(
            len(rows),
            "B=v/g^3 gives the corrected p8 canonical block and fixed boundary",
            f"block={repair['correct_p8_subblock']}; boundary={repair['correct_fixed_boundary']}",
            repair,
            repair["correct_formula"] == "beta_B=[6-3 beta_g/g]B+source"
            and repair["correct_fixed_boundary"] == "B_star=-source_star/6"
            and repair["correct_p8_subblock"] == [6.0, 6.0],
        )
    )

    pure = split["pure_Einstein_split"]
    rows.append(
        validation_row(
            len(rows),
            "Bern-normalized additive R3 running and iterated p8 coefficients match exact formulas",
            f"betaA={pure['beta_A_C3_pure_GR']:.12g}; Bminus_L2={pure['Bminus_L2_coefficient']:.12g}",
            pure,
            math.isclose(
                pure["beta_C_R3_pure_GR"],
                1.0 / (20.0 * (4.0 * math.pi) ** 4),
                rel_tol=2e-15,
            )
            and math.isclose(
                pure["beta_A_C3_pure_GR"],
                1.0 / (3840.0 * math.pi**3),
                rel_tol=2e-15,
            )
            and math.isclose(
                pure["Bminus_L2_coefficient"],
                -1.0 / (640.0 * math.pi**3),
                rel_tol=2e-15,
            )
            and math.isclose(
                pure["primitive_B_helicity_source_per_unit_xi"],
                1.0 / (32.0 * math.pi**3),
                rel_tol=2e-15,
            )
            and math.isclose(pure["baratella_to_Bern_ratio"], 10.0)
            and math.isclose(pure["Bern_to_FRG_ratio"], 2.0)
            and pure["R3_running_type"] == "ADDITIVE_TWO_LOOP_SOURCE",
        )
    )

    primitive = split["primitive_three_loop"]
    rows.append(
        validation_row(
            len(rows),
            "the primitive three-loop vector remains rank two and is not set to zero",
            primitive["status"],
            primitive,
            primitive["same_helicity_parameter"] == "xi_minus"
            and primitive["mixed_helicity_parameter"] == "xi_plus"
            and primitive["set_to_zero"] is False,
        )
    )

    matching = split["functional_onshell_matching"]
    rows.append(
        validation_row(
            len(rows),
            "functional and on-shell C3 slopes remain explicitly unmatched",
            f"functional={matching['functional_dA_dlnk_min']:.12g}; onshell={matching['onshell_pure_GR_dA_dlnmu']:.12g}",
            matching,
            matching["functional_dA_dlnk_max"] < 0.0
            and matching["onshell_pure_GR_dA_dlnmu"] > 0.0
            and split["checks"]["functional_onshell_matching_not_claimed"],
        )
    )

    fixed_rows = read_csv(FIXED_CSV)
    trajectory_rows = read_csv(TRAJECTORY_CSV)
    convergence_rows = read_csv(CONVERGENCE_CSV)
    response_rows = read_csv(RESPONSE_CSV)
    budget_rows = read_csv(BUDGET_CSV)
    rows.append(
        validation_row(
            len(rows),
            "all generated p8 ledgers have their complete row counts",
            (
                f"fixed={len(fixed_rows)}; trajectory={len(trajectory_rows)}; "
                f"convergence={len(convergence_rows)}; response={len(response_rows)}; "
                f"budget={len(budget_rows)}"
            ),
            {
                "fixed": len(fixed_rows),
                "trajectory": len(trajectory_rows),
                "convergence": len(convergence_rows),
                "response": len(response_rows),
                "budget": len(budget_rows),
            },
            len(fixed_rows) == 4
            and len(trajectory_rows) == 4 * 121
            and len(convergence_rows) == 12
            and len(response_rows) == 20
            and len(budget_rows) == 80,
        )
    )

    fixed_max = max(
        max(abs(float(row["beta_B_C_fixed_residual"])), abs(float(row["beta_B_t_fixed_residual"])))
        for row in fixed_rows
    )
    rows.append(
        validation_row(
            len(rows),
            "all four corrected fixed points have block plus six and negligible residual",
            f"max residual={fixed_max:.12g}",
            [
                {
                    "scheme": row["scheme"],
                    "order": row["polynomial_order"],
                    "eigen_C": row["p8_subblock_eigenvalue_C"],
                    "eigen_t": row["p8_subblock_eigenvalue_t"],
                }
                for row in fixed_rows
            ],
            fixed_max <= 1.0e-15
            and all(float(row["p8_subblock_eigenvalue_C"]) == 6.0 for row in fixed_rows)
            and all(float(row["p8_subblock_eigenvalue_t"]) == 6.0 for row in fixed_rows)
            and all(int(row["new_relevant_directions"]) == 0 for row in fixed_rows),
        )
    )

    rows.append(
        validation_row(
            len(rows),
            "all corrected trajectories succeed and pass the N6/N8 gate",
            f"max={trajectory['maximum_N6_to_N8_relative_shift']:.12g}",
            trajectory["canonical_repaired_N8_endpoints"],
            len(trajectory["canonical_repaired_N8_endpoints"]) == 2
            and all(row["success"] for row in trajectory["canonical_repaired_N8_endpoints"])
            and trajectory["maximum_N6_to_N8_relative_shift"] <= 1.0e-3
            and all(row["status"] == "CANONICAL_REPAIRED_KNOWN_SOURCE_TRAJECTORY" for row in trajectory_rows),
        )
    )

    endpoints = trajectory["canonical_repaired_N8_endpoints"]
    b_c_values = [float(row["B_C_endpoint"]) for row in endpoints]
    b_t_values = [float(row["B_t_endpoint"]) for row in endpoints]
    rows.append(
        validation_row(
            len(rows),
            "the repaired N8 endpoints match the recorded canonical bracket",
            f"BC=[{min(b_c_values):.13g},{max(b_c_values):.13g}]; Bt=[{min(b_t_values):.13g},{max(b_t_values):.13g}]",
            endpoints,
            math.isclose(min(b_c_values), 0.013784331249138528, rel_tol=0.0, abs_tol=2e-15)
            and math.isclose(max(b_c_values), 0.013785187626140994, rel_tol=0.0, abs_tol=2e-15)
            and math.isclose(min(b_t_values), -0.012180655934044916, rel_tol=0.0, abs_tol=2e-15)
            and math.isclose(max(b_t_values), -0.012180337030564939, rel_tol=0.0, abs_tol=2e-15),
        )
    )

    response_failures = [
        row
        for row in response_rows
        if float(row["iterated_delta_B_plus"]) != 0.0
        or float(row["primitive_delta_B_minus_per_xi_minus"]) == 0.0
        or float(row["primitive_delta_B_plus_per_xi_plus"]) == 0.0
        or row["R3_running_type"] != "ADDITIVE_TWO_LOOP_SOURCE"
    ]
    rows.append(
        validation_row(
            len(rows),
            "the iterated response is same-helicity while the primitive response is rank two",
            f"failures={len(response_failures)}",
            response_failures,
            not response_failures
            and trajectory["checks"]["iterated_response_same_helicity_only"]
            and trajectory["checks"]["primitive_response_rank_two"],
        )
    )

    earliest_n8 = [
        row
        for row in response_rows
        if int(row["polynomial_order"]) == 8 and float(row["g_match"]) == 1.0e-2
    ]
    earliest_values = [float(row["iterated_delta_B_minus"]) for row in earliest_n8]
    rows.append(
        validation_row(
            len(rows),
            "the corrected g_match=1e-2 response carries the tenfold-smaller Bern source",
            f"range=[{min(earliest_values):.12g},{max(earliest_values):.12g}]",
            earliest_n8,
            len(earliest_n8) == 2
            and math.isclose(min(earliest_values), -0.004307473580014973, rel_tol=0.0, abs_tol=2e-14)
            and math.isclose(max(earliest_values), -0.004307473476387038, rel_tol=0.0, abs_tol=2e-14)
            and trajectory["pure_Einstein_R3_running_type"] == "ADDITIVE_TWO_LOOP_SOURCE",
        )
    )

    rows.append(
        validation_row(
            len(rows),
            "primitive and finite-boundary responses are retained but not added to the primary candidate",
            f"primitive={trajectory['primitive_source_status']}; boundary={trajectory['matching_boundary_status']}",
            {
                "primitive": trajectory["primitive_source_status"],
                "boundary": trajectory["matching_boundary_status"],
            },
            trajectory["primitive_source_status"] == "UNCOMPUTED_NOT_ADDED_TO_PRIMARY_CANDIDATE"
            and trajectory["matching_boundary_status"] == "EXPLICIT_LINEAR_RESPONSE_RETAINED",
        )
    )

    static_rows = read_csv(STATIC_CSV)
    static_max = max(float(row["max_abs_metric_residual"]) for row in static_rows)
    rows.append(
        validation_row(
            len(rows),
            "all corrected known-source compact rows remain below their gates",
            f"rows={len(static_rows)}; max={static_max:.12g}",
            {"recorded_max": trajectory["maximum_static_metric_residual"]},
            len(static_rows) == 22
            and all(
                float(row["max_abs_metric_residual"]) <= float(row["epsilon_gate"])
                for row in static_rows
            )
            and math.isclose(
                static_max,
                trajectory["maximum_static_metric_residual"],
                rel_tol=1.0e-14,
            ),
        )
    )

    marker_paths = [CHECKPOINT, FORMAL_NOTE, RESUME, SPINE, EQUATIONS, RED_TEAM, UNIFICATION]
    marker_missing = [
        str(path)
        for path in marker_paths
        if CHECKPOINT_MARKER not in path.read_text(encoding="utf-8")
    ]
    rows.append(
        validation_row(
            len(rows),
            "checkpoint formal handoff spine and registers contain the 4969 marker",
            f"{len(marker_missing)} missing markers",
            marker_missing,
            not marker_missing,
        )
    )

    banner_failures = [
        str(path)
        for path in OLD_CHECKPOINTS
        if "4969" not in path.read_text(encoding="utf-8")
        or "supersed" not in path.read_text(encoding="utf-8").lower()
    ]
    rows.append(
        validation_row(
            len(rows),
            "all 4967-4968 checkpoint and formal notes carry canonical supersession banners",
            f"{len(banner_failures)} banner failures",
            banner_failures,
            not banner_failures,
        )
    )

    variable_rows = read_csv(VARIABLES)
    required_variable_ids = (
        "beta_A_C3_EH4969",
        "xi_minus4969",
        "xi_plus4969",
        "B_C4969_MTS",
        "B_t4969_MTS",
        "PredictivityStatus4969_MTS",
    )
    variable_counts = {
        variable_id: sum(row["symbol"] == variable_id for row in variable_rows)
        for variable_id in required_variable_ids
    }
    rows.append(
        validation_row(
            len(rows),
            "all six canonical 4969 variable rows occur exactly once",
            str(variable_counts),
            variable_counts,
            all(count == 1 for count in variable_counts.values()),
        )
    )

    claim_rows = read_csv(CLAIMS)
    claim_4969 = [row for row in claim_rows if row["claim_id"] == "L-811"]
    numeric_claim_ids = [
        int(row["claim_id"].split("-", 1)[1])
        for row in claim_rows
        if row["claim_id"].startswith("L-") and row["claim_id"].split("-", 1)[1].isdigit()
    ]
    rows.append(
        validation_row(
            len(rows),
            "claim L-811 occurs once is latest and remains private nonclaim",
            f"count={len(claim_4969)}; max={max(numeric_claim_ids)}",
            claim_4969,
            len(claim_4969) == 1
            and max(numeric_claim_ids) == 811
            and "private_nonclaim" in claim_4969[0]["status"],
        )
    )

    generated_csvs = [
        SOURCE_AUDIT_CSV,
        SCALING_CSV,
        SPLIT_CSV,
        MATCHING_CSV,
        FIXED_CSV,
        TRAJECTORY_CSV,
        CONVERGENCE_CSV,
        STATIC_CSV,
        RESPONSE_CSV,
        BUDGET_CSV,
        VARIABLES,
        CLAIMS,
    ]
    malformed: list[str] = []
    placeholders: list[str] = []
    for path in generated_csvs:
        parsed = read_csv(path)
        if not parsed or any(None in row for row in parsed):
            malformed.append(str(path))
        if path.parent == SOURCE and "MISSING_" in path.read_text(encoding="utf-8-sig"):
            placeholders.append(str(path))
    rows.append(
        validation_row(
            len(rows),
            "all generated and canonical CSV files parse and 4969 outputs have no placeholder tokens",
            f"malformed={len(malformed)}; placeholders={len(placeholders)}",
            {"malformed": malformed, "placeholders": placeholders},
            not malformed and not placeholders,
        )
    )

    source_audit = read_csv(SOURCE_AUDIT_CSV)
    rows.append(
        validation_row(
            len(rows),
            "the source audit distinguishes locked results from search absence",
            f"rows={len(source_audit)}",
            [row["status"] for row in source_audit],
            len(source_audit) == 7
            and sum(row["status"] == "PRIMARY_SOURCE_LOCKED" for row in source_audit) >= 4
            and any("COEFFICIENT_QUARANTINED" in row["status"] for row in source_audit)
            and any("FACTOR_TWO" in row["result"].upper() or "ONE HALF" in row["result"].upper() for row in source_audit)
            and any("NOT_A_ZERO_THEOREM" in row["status"] for row in source_audit),
        )
    )

    authored_docs = [CHECKPOINT, FORMAL_NOTE, PROVENANCE]
    placeholder_docs = [
        str(path) for path in authored_docs if "MISSING_" in path.read_text(encoding="utf-8")
    ]
    rows.append(
        validation_row(
            len(rows),
            "new authored documents contain no MISSING placeholder tokens",
            f"{len(placeholder_docs)} placeholder documents",
            placeholder_docs,
            not placeholder_docs,
        )
    )

    rows.append(
        validation_row(
            len(rows),
            "the accidental broad-search dump is absent from the retained source pack",
            f"exists={EXTRANEOUS_SEARCH_DUMP.exists()}",
            str(EXTRANEOUS_SEARCH_DUMP),
            not EXTRANEOUS_SEARCH_DUMP.exists(),
        )
    )

    cache_paths = [str(path) for path in POST.rglob("__pycache__") if path.is_dir()]
    rows.append(
        validation_row(
            len(rows),
            "no Python bytecode cache directories remain under post-checkpoint-work",
            f"{len(cache_paths)} cache directories",
            cache_paths,
            not cache_paths,
        )
    )

    rows.append(
        validation_row(
            len(rows),
            "every prior validation row passes while claim promotion remains false",
            f"prior_passed={all(row['passed'] for row in rows)}; rows={len(rows)}",
            {"valid_for_full_MTS_claim": False, "github_action": "none"},
            all(row["passed"] for row in rows),
        )
    )

    write_csv(rows)
    failures = [row["check_id"] for row in rows if not row["passed"]]
    print(f"{MARKER}_CHECKS={len(rows)}", flush=True)
    print(f"{MARKER}_FAILURES={failures}", flush=True)
    print(f"{MARKER}_OUTPUT_SHA256={digest(OUTPUT)}", flush=True)
    if failures:
        raise RuntimeError(f"4969 validation failed: {failures}")
    print(f"{MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

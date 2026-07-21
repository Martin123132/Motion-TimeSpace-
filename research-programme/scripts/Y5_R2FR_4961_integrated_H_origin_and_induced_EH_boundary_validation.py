from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import sys
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "4961"
OUTPUT = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_4961_VALIDATION.csv"
)

MAIN_SCRIPT = (
    POST
    / "scripts"
    / "Y5_R2FR_4961_integrated_H_origin_and_induced_EH_boundary.py"
)
RESULT_JSON = SOURCE / "integrated_H_origin_and_induced_EH_results.json"
INVENTORY_CSV = SOURCE / "microscopic_tensor_density_candidate_inventory.csv"
MAP_CSV = SOURCE / "local_and_ensemble_metric_map_rank_gate.csv"
COLLECTIVE_CSV = SOURCE / "collective_field_transform_and_Diff_gate.csv"
BACKGROUND_CSV = SOURCE / "reference_background_split_Ward_gate.csv"
HESSIAN_CSV = SOURCE / "motion_Hessian_no_bootstrap_audit.csv"
RESIDUE_CSV = SOURCE / "induced_EH_residue_scale_gate.csv"
DECISION_CSV = SOURCE / "integrated_H_origin_boundary_decision.csv"
PROVENANCE = SOURCE / "PROVENANCE.md"
CHECKPOINT = POST / "4961-Y5-R2FR-integrated-H-origin-and-induced-EH-residue-from-motion-Hessian-or-explicit-fundamental-field-boundary.md"
FORMAL_NOTE = (
    FORMAL
    / "977-PPC4161-integrated-H-origin-induced-EH-and-explicit-parent-boundary.md"
)

CLAIMS = FORMAL / "02-claims-register.csv"
VARIABLES = FORMAL / "04-variable-audit.csv"
EQUATIONS = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
SPINE = FORMAL / "07-unification-spine.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"
LOCAL_SPINE = POST / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

MARKER = "MTS_4961_INTEGRATED_H_ORIGIN_AND_INDUCED_EH_BOUNDARY"
FORMAL_MARKER = "PPC4161_INTEGRATED_H_ORIGIN_AND_PARENT_BOUNDARY_4961"

HASH_LOCKS = {
    MAIN_SCRIPT: "ff0085dfbdf42520fbf08bb6e3a43d7380e805971667f614d484aecd93331864",
    RESULT_JSON: "2be33638d28a679878a17f1038543876b4df742d1a8769de9e8ead02bb665076",
    INVENTORY_CSV: "c0b4d92d1ea86168c9818e3b12721340f99f9fd459f645ae805b14de8821ccd9",
    MAP_CSV: "f3be4febe17177a046cc1ed4f00040874d069c35502d3222bcb069ff46b9fad7",
    COLLECTIVE_CSV: "4d6868f2b567454b0b695fef1d057bb9f9be4d66cf4a25fedcd7d696f82c3868",
    BACKGROUND_CSV: "e2de59f64476d463194407db3ff7057ee5e5ecf2042ca739a81ec04545f471ec",
    HESSIAN_CSV: "652c2551ea3b570d486f31174ec6ef270f69fbfe2dda473be1ea4073ddaffc74",
    RESIDUE_CSV: "1dd371cbdd7253c55ef1680a463d426211728fe7b9e469f75055680827c910c8",
    DECISION_CSV: "b576f3fbd382af96b874e26e503e47bbbaa8f6314e321ef682834ac9dbfe50bd",
    PROVENANCE: "0bc47ae6779c1638a52ed8873c925d56a2c14dabd958ed550d42ee1d2bc4cc3d",
    CHECKPOINT: "ec6c5ff4056ed13ad92cad5e70ce125d81183abd0d79c59345dd6393987e2de2",
    FORMAL_NOTE: "e79a2328b55e21c3fd27208f48b3f56056f3b53bde25c6532893fe24ce26a64f",
}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def truth(value: str) -> bool:
    return value.strip().lower() == "true"


def close(actual: float, expected: float, tolerance: float = 1.0e-11) -> bool:
    return math.isclose(actual, expected, rel_tol=tolerance, abs_tol=tolerance)


def add(
    rows: list[dict[str, Any]],
    check_id: str,
    test: str,
    expected: Any,
    actual: Any,
    passed: bool,
) -> None:
    rows.append(
        {
            "validation_id": check_id,
            "test": test,
            "expected": json.dumps(expected, sort_keys=True, default=str),
            "actual": json.dumps(actual, sort_keys=True, default=str),
            "passed": bool(passed),
            "checkpoint_marker": MARKER,
        }
    )


def main() -> int:
    checks: list[dict[str, Any]] = []

    missing_paths = [str(path) for path in HASH_LOCKS if not path.exists()]
    add(
        checks,
        "VAL4961_01_paths",
        "all hash-locked paths exist",
        [],
        missing_paths,
        not missing_paths,
    )

    bad_hashes = {
        str(path): {"expected": expected, "actual": digest(path)}
        for path, expected in HASH_LOCKS.items()
        if path.exists() and digest(path) != expected
    }
    add(
        checks,
        "VAL4961_02_hashes",
        "new research and documentation hashes match",
        {},
        bad_hashes,
        not bad_hashes,
    )

    compile_errors: list[str] = []
    for path in (MAIN_SCRIPT, Path(__file__).resolve()):
        try:
            compile(text(path), str(path), "exec")
        except Exception as error:
            compile_errors.append(f"{path.name}: {error}")
    add(
        checks,
        "VAL4961_03_compile",
        "research and validation scripts compile in memory",
        [],
        compile_errors,
        not compile_errors,
    )

    result = json.loads(text(RESULT_JSON))
    add(
        checks,
        "VAL4961_04_marker",
        "result marker",
        MARKER,
        result.get("marker"),
        result.get("marker") == MARKER,
    )
    failed_internal = [
        name for name, passed in result["checks"].items() if not passed
    ]
    add(
        checks,
        "VAL4961_05_internal",
        "all research checks pass",
        [],
        failed_internal,
        not failed_internal,
    )
    failed_clauses = [
        name
        for name, passed in result["source_clause_checks"].items()
        if not passed
    ]
    source_hashes = result["source_hashes"]
    add(
        checks,
        "VAL4961_06_sources",
        "15 source hashes and 14 source clauses pass",
        {"hash_count": 15, "clause_count": 14, "failed": []},
        {
            "hash_count": len(source_hashes),
            "clause_count": len(result["source_clause_checks"]),
            "failed": failed_clauses,
        },
        len(source_hashes) == 15
        and len(result["source_clause_checks"]) == 14
        and not failed_clauses
        and all(re.fullmatch(r"[0-9a-f]{64}", value) for value in source_hashes.values()),
    )

    tables = {
        "inventory": read_csv(INVENTORY_CSV),
        "map": read_csv(MAP_CSV),
        "collective": read_csv(COLLECTIVE_CSV),
        "background": read_csv(BACKGROUND_CSV),
        "hessian": read_csv(HESSIAN_CSV),
        "residue": read_csv(RESIDUE_CSV),
        "decision": read_csv(DECISION_CSV),
    }
    malformed = {
        f"{table_name}:{row_index}": row
        for table_name, rows in tables.items()
        for row_index, row in enumerate(rows)
        if None in row or any(value is None for value in row.values())
    }
    add(
        checks,
        "VAL4961_07_csv_shape",
        "all generated CSV rows parse without overflow",
        {},
        malformed,
        not malformed,
    )
    marker_errors = [
        f"{table_name}:{row_index}"
        for table_name, rows in tables.items()
        for row_index, row in enumerate(rows)
        if row.get("checkpoint_marker") != MARKER
        or truth(row.get("valid_for_full_MTS_claim", "False"))
    ]
    add(
        checks,
        "VAL4961_08_claim_flags",
        "all rows carry marker and full-MTS false",
        [],
        marker_errors,
        not marker_errors,
    )

    inventory = result["corpus_inventory"]
    inventory_candidates = [
        row
        for row in tables["inventory"]
        if truth(row["declares_independent_tensor_or_metric_parent"])
        and truth(row["declares_exact_Diff_BRST_parent"])
    ]
    add(
        checks,
        "VAL4961_09_inventory",
        "complete primitive corpus sweep and zero tensor-Diff parent candidates",
        {"files": 44, "md": 43, "pdf": 1, "candidates": 0},
        {
            "files": len(tables["inventory"]),
            "md": inventory["markdown_files"],
            "pdf": inventory["pdf_files"],
            "candidates": len(inventory_candidates),
        },
        len(tables["inventory"]) == 44
        and inventory["files_scanned"] == 44
        and inventory["markdown_files"] == 43
        and inventory["pdf_files"] == 1
        and not inventory_candidates,
    )

    map_rows = {row["gate_id"]: row for row in tables["map"]}
    map_result = result["metric_map_rank_gate"]
    expected_map_ids = {
        "MAP4961_00_single_gradient",
        "MAP4961_01_first_jet_bound",
        "MAP4961_02_connected_covariance",
        "MAP4961_03_interpretation",
    }
    add(
        checks,
        "VAL4961_10_map_ranks",
        "local scalar obstruction and full covariance tangent",
        {"ids": sorted(expected_map_ids), "gradient": 4, "jet_cap": 5, "covariance": 10},
        {
            "ids": sorted(map_rows),
            "gradient": map_result["single_gradient_generic_rank"],
            "jet_cap": map_result["first_jet_rank_upper_bound"],
            "covariance": map_result["covariance_tangent_rank_at_identity"],
        },
        set(map_rows) == expected_map_ids
        and map_result["single_gradient_generic_rank"] == 4
        and map_result["single_gradient_outer_product_rank"] == 1
        and map_result["first_jet_rank_upper_bound"] == 5
        and map_result["covariance_tangent_rank_at_identity"] == 10
        and all(truth(row["passed"]) for row in map_rows.values()),
    )

    collective_rows = {row["gate_id"]: row for row in tables["collective"]}
    collective = result["collective_field_gate"]
    expected_collective_ids = {
        f"COL4961_{index:02d}_{suffix}"
        for index, suffix in enumerate(
            (
                "HS_identity",
                "spin2_gauge_map",
                "regular_HS_Ward_failure",
                "Ward_Hessian",
                "singular_kernel_boundary",
                "accidental_pole_tuning",
                "composite_delta",
                "release_delta",
            )
        )
    }
    add(
        checks,
        "VAL4961_11_collective",
        "exact auxiliary transform and spin-two Ward-nullity mismatch",
        {
            "ids": sorted(expected_collective_ids),
            "sample_ranks": {"timelike_axis": 4, "spacelike_axis": 4, "Minkowski_null": 4, "generic": 4},
            "regular_nullity": 0,
            "Ward_nullity": 4,
        },
        {
            "ids": sorted(collective_rows),
            "sample_ranks": collective["sampled_gauge_map_ranks"],
            "regular_nullity": 10 - collective["regular_inverse_kernel_rank"],
            "Ward_nullity": collective["quotient_Hessian_nullity"],
        },
        set(collective_rows) == expected_collective_ids
        and all(rank == 4 for rank in collective["sampled_gauge_map_ranks"].values())
        and collective["regular_inverse_kernel_rank"] == 10
        and not collective["regular_inverse_kernel_Ward_zero"]
        and collective["quotient_Hessian_rank"] == 6
        and collective["quotient_Hessian_nullity"] == 4
        and collective["quotient_Hessian_Ward_zero"]
        and collective["quotient_Hessian_determinant"] == "0"
        and collective["gaussian_identity_residual"] == "0"
        and collective["accidental_pole_determinant"] == "epsilon"
        and all(truth(row["passed"]) for row in collective_rows.values()),
    )

    background_rows = {row["gate_id"]: row for row in tables["background"]}
    background = result["background_split_gate"]
    add(
        checks,
        "VAL4961_12_background",
        "nonzero reference-metric stress witness",
        {"rows": 4, "rank": 4, "norm2": "25"},
        {
            "rows": len(background_rows),
            "rank": background["stress_rank"],
            "norm2": background["stress_Frobenius_squared"],
        },
        len(background_rows) == 4
        and background["printed_scalar_action_has_nonzero_reference_variation"]
        and background["stress_rank"] == 4
        and background["stress_Frobenius_squared"] == "25"
        and all(truth(row["passed"]) for row in background_rows.values()),
    )

    hessian_rows = {row["gate_id"]: row for row in tables["hessian"]}
    hessian = result["motion_Hessian_audit"]
    add(
        checks,
        "VAL4961_13_hessian",
        "4956 motion Hessian is a correction around inherited gravity",
        {"rows": 4, "Hhh_g0": "I10", "Hhpsi_g0": "0", "bootstrap": False},
        {
            "rows": len(hessian_rows),
            "Hhh_g0": hessian["metric_block_at_g_zero"],
            "Hhpsi_g0": hessian["mixed_block_at_g_zero"],
            "bootstrap": hessian["motion_Hessian_bootstraps_gravity"],
        },
        len(hessian_rows) == 4
        and hessian["metric_block_at_g_zero"] == "I10"
        and hessian["mixed_block_at_g_zero"] == "0"
        and not hessian["motion_Hessian_bootstraps_gravity"]
        and close(hessian["inherited_g_fixed_point"], 0.1305603732179711)
        and all(truth(row["passed"]) for row in hessian_rows.values()),
    )

    residue_rows = {row["branch"]: row for row in tables["residue"]}
    residue = result["induced_EH_residue_gate"]
    add(
        checks,
        "VAL4961_14_residue",
        "induced Einstein scale and matching degeneracy",
        {
            "rows": 6,
            "W1_one_cutoff_over_mpl": 6.139960247678931,
            "rank": 1,
            "nullity": 2,
            "absolute_G": False,
        },
        {
            "rows": len(residue_rows),
            "W1_one_cutoff_over_mpl": residue["primitive_W1_1_Lambda_over_usual_mpl"],
            "rank": residue["one_Newton_measurement_Jacobian_rank"],
            "nullity": residue["matching_nullity"],
            "absolute_G": residue["absolute_G_predicted"],
        },
        len(residue_rows) == 6
        and close(residue["primitive_W1_1_Lambda_over_reduced_Mpl"], 30.781195923884734)
        and close(residue["primitive_W1_1_Lambda_over_usual_mpl"], 6.139960247678931)
        and close(residue["primitive_W1_1_ellstar_over_lPlanck"], 0.16286750396763996)
        and close(residue["W1_for_LambdaUV_equal_reduced_Mpl"], 96.0 * math.pi**2)
        and close(residue["W1_for_LambdaUV_equal_usual_mpl"], 12.0 * math.pi)
        and residue["one_Newton_measurement_Jacobian_rank"] == 1
        and residue["matching_nullity"] == 2
        and not residue["absolute_G_predicted"]
        and all(truth(row["passed"]) for row in residue_rows.values()),
    )

    decisions = {row["decision_id"]: row for row in tables["decision"]}
    expected_decision_ids = {f"DEC4961_{index:02d}_{suffix}" for index, suffix in enumerate((
        "primitive_content",
        "local_scalar_map",
        "covariance_span",
        "collective_transform",
        "background_independence",
        "motion_Hessian",
        "induced_EH",
        "absolute_G",
        "parent_boundary",
        "local_correspondence",
        "full_MTS",
        "next_target",
    ))}
    add(
        checks,
        "VAL4961_15_decisions",
        "twelve explicit origin and parent-boundary decisions",
        sorted(expected_decision_ids),
        sorted(decisions),
        set(decisions) == expected_decision_ids
        and decisions["DEC4961_08_parent_boundary"]["answer"]
        == "INTEGRATED_H_AND_EXACT_DIFF_ARE_EXPLICIT_FUNDAMENTAL_PARENT_FIELD_AND_SYMMETRY_DATA"
        and truth(decisions["DEC4961_08_parent_boundary"]["claim_granted"])
        and truth(decisions["DEC4961_09_local_correspondence"]["claim_granted"])
        and not truth(decisions["DEC4961_10_full_MTS"]["claim_granted"])
        and all(truth(row["passed"]) for row in decisions.values()),
    )

    decision = result["decision"]
    add(
        checks,
        "VAL4961_16_result_boundary",
        "result selects explicit parent and retains weak-local correspondence",
        {
            "H_Diff": "EXPLICIT_FUNDAMENTAL_PARENT_DATA",
            "local": "RETAINED",
            "strong": False,
            "full": False,
        },
        {
            "H_Diff": decision["integrated_H_and_Diff"],
            "local": decision["weak_local_GR_Newton_Maxwell_4960"],
            "strong": decision["strong_compact_GR"],
            "full": decision["full_MTS"],
        },
        decision["integrated_H_and_Diff"] == "EXPLICIT_FUNDAMENTAL_PARENT_DATA"
        and decision["weak_local_GR_Newton_Maxwell_4960"] == "RETAINED"
        and not decision["absolute_Newton_constant_prediction"]
        and not decision["strong_compact_GR"]
        and not decision["full_MTS"],
    )

    claims = read_csv(CLAIMS)
    claim_rows = [row for row in claims if row.get("claim_id") == "L-803"]
    add(
        checks,
        "VAL4961_17_claim_register",
        "one L-803 claim-register row with private nonclaim boundary",
        {"count": 1, "marker": FORMAL_MARKER},
        {
            "count": len(claim_rows),
            "marker_present": bool(claim_rows and FORMAL_MARKER in claim_rows[0]["notes"]),
        },
        len(claim_rows) == 1
        and "explicit_integrated_H_Diff_parent_selected" in claim_rows[0]["status"]
        and FORMAL_MARKER in claim_rows[0]["notes"]
        and "FULL_MTS_FALSE" in claim_rows[0]["notes"],
    )

    variable_rows = read_csv(VARIABLES)
    expected_symbols = {
        "SingleScalarMetricRank4961_MTS",
        "ConnectedCovarianceSpan4961_MTS",
        "CollectiveTransformDiffGate4961_MTS",
        "ReferenceBackgroundSplitWard4961_MTS",
        "MotionHessianNoBootstrap4961_MTS",
        "InducedEHMatching4961_MTS",
        "ParentFieldBoundary4961_MTS",
        "PredictivityStatus4961_MTS",
    }
    actual_symbols = {
        row["symbol"] for row in variable_rows if row["symbol"] in expected_symbols
    }
    add(
        checks,
        "VAL4961_18_variable_register",
        "eight canonical 4961 variables",
        sorted(expected_symbols),
        sorted(actual_symbols),
        actual_symbols == expected_symbols,
    )

    documentation = {
        "checkpoint": text(CHECKPOINT),
        "formal_note": text(FORMAL_NOTE),
        "equations": text(EQUATIONS),
        "red_team": text(RED_TEAM),
        "spine": text(SPINE),
        "resume": text(RESUME),
        "local_spine": text(LOCAL_SPINE),
        "provenance": text(PROVENANCE),
    }
    documentation_requirements = {
        "checkpoint_marker": MARKER in documentation["checkpoint"],
        "formal_marker": FORMAL_MARKER in documentation["formal_note"],
        "equation_section": "## 1.254 Integrated-H origin obstruction" in documentation["equations"],
        "red_team_section": "## 205. A full-rank covariance is not an independent gauge metric" in documentation["red_team"],
        "spine_marker": FORMAL_MARKER in documentation["spine"],
        "resume_latest": "Last checkpoint: `4961-" in documentation["resume"]
        and "Marker: `PPC4161_INTEGRATED_H_ORIGIN_AND_PARENT_BOUNDARY_4961`"
        in documentation["resume"],
        "local_spine_latest": "Current State Through 4961" in documentation["local_spine"]
        and FORMAL_MARKER in documentation["local_spine"],
        "provenance_marker": f"{MARKER}_PROVENANCE" in documentation["provenance"],
        "full_claim_false": all(
            phrase in documentation["checkpoint"]
            for phrase in (
                "full MTS",
                "Strong compact objects",
                "No GitHub action is authorized",
            )
        ),
    }
    add(
        checks,
        "VAL4961_19_documentation",
        "checkpoint, registers, resume and spine carry exact scoped boundary",
        {key: True for key in documentation_requirements},
        documentation_requirements,
        all(documentation_requirements.values()),
    )

    claims_malformed = [
        row_index
        for row_index, row in enumerate(claims)
        if None in row or any(value is None for value in row.values())
    ]
    variables_malformed = [
        row_index
        for row_index, row in enumerate(variable_rows)
        if None in row or any(value is None for value in row.values())
    ]
    add(
        checks,
        "VAL4961_20_register_shape",
        "claims and variable registers remain parseable",
        {"claims": [], "variables": []},
        {"claims": claims_malformed, "variables": variables_malformed},
        not claims_malformed and not variables_malformed,
    )

    pycache_paths = [
        str(path.relative_to(ROOT))
        for path in (POST / "scripts").rglob("__pycache__")
    ]
    add(
        checks,
        "VAL4961_21_pycache",
        "no scripts __pycache__ remains",
        [],
        pycache_paths,
        not pycache_paths,
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(checks[0]))
        writer.writeheader()
        writer.writerows(checks)

    failed_checks = [row["validation_id"] for row in checks if not row["passed"]]
    print(f"{MARKER}_VALIDATION_CHECKS={len(checks)}", flush=True)
    print(f"{MARKER}_VALIDATION_FAILED={len(failed_checks)}", flush=True)
    print(f"{MARKER}_VALIDATION_SHA256={digest(OUTPUT)}", flush=True)
    if failed_checks:
        print(
            f"{MARKER}_VALIDATION_FAILURES={','.join(failed_checks)}",
            flush=True,
        )
        return 1
    print(f"{MARKER}_VALIDATION_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

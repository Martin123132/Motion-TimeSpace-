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
SOURCE = POST / "source-intake" / "functional_rg" / "4970"
RESIDUAL = POST / "source-intake" / "mts_residuals"
OUTPUT = RESIDUAL / "P8_Y5_BRR545_4970_VALIDATION.csv"
MARKER = "MTS_4970_WEAK_SCALE_C3_P8_MATCHING_VALIDATION"
CHECKPOINT_MARKER = "PPC4161_WEAK_SCALE_C3_P8_MATCHING_4970"
CHECKED_DATE = "2026-07-13"

RUNNER = POST / "scripts" / "Y5_R2FR_4970_weak_scale_C3_p8_matching.py"
VALIDATOR = POST / "scripts" / "Y5_R2FR_4970_weak_scale_C3_p8_matching_validation.py"
CONTRACT = SOURCE / "C3_matching_contract.csv"
SCAN = SOURCE / "C3_weak_branch_splice_scan.csv"
TRANSFER = SOURCE / "C3_p8_matching_transfer_matrix.csv"
SENSITIVITY = SOURCE / "C3_matching_scale_sensitivity.csv"
TRANSPORT = SOURCE / "C3_matching_offset_RG_transport.csv"
RESULT = SOURCE / "C3_p8_finite_matching_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"
CHECKPOINT = (
    POST
    / "4970-Y5-R2FR-weak-scale-Wilsonian-to-onshell-C3-splice-and-p8-matching-transfer.md"
)
FORMAL_NOTE = FORMAL / "986-PPC4161-weak-scale-C3-p8-matching-transfer.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"
SPINE = POST / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"
CLAIMS = FORMAL / "02-claims-register.csv"
VARIABLES = FORMAL / "04-variable-audit.csv"
EQUATIONS = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
UNIFICATION = FORMAL / "07-unification-spine.md"

EXPECTED_HASHES = {
    POST
    / "source-intake"
    / "functional_rg"
    / "4957"
    / "functional_PX_O4_GR_trajectory.csv": (
        "c60eee38379dc8cf1bb16833b2b5a849ecc0b5d7da0f74d9f0c9bd1bf9b46166"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "4969"
    / "p8_canonical_repaired_GR_connected_trajectory.csv": (
        "b5984ba1c528aebd2099755561a8b578ec79751a3846be01032cc52e24e65957"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "4969"
    / "p8_canonical_Einstein_split_results.json": (
        "7e45bf69deb9e61df28ef640eb0f075e2689849673d8199526e459bfd2e2d2d7"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "4969"
    / "functional_to_onshell_C3_matching_diagnostic.csv": (
        "d8dc49be58f8eff511da14cae0d2fa9d803dc9fa1d227ba05957896b725dc243"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "4969"
    / "src-1701.02422"
    / "gr_simp.tex": (
        "9448bff31da3e1e56e62e8fb6242a60c09afb90d1f7f25edaf3f23466ac0371e"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "4965"
    / "src-2103.12728"
    / "GravScatt.tex": (
        "6812e00f073074e6c045d3241125dc5cf1c73891ad250754b82cd19bae5e7963"
    ),
    POST
    / "source-intake"
    / "functional_rg"
    / "4929"
    / "src2312"
    / "ess_cubic.tex": (
        "b23b0974509278be22c8917f531a2963d415184d9052e27860c65fad80943a1d"
    ),
    RUNNER: "fcd3ca282f1c5690de9ab173f8446f04dc83628fb2af5eee920bfe114c255cdb",
    CONTRACT: "08317c0db0cd93cef5020ac15eadd93689de086da6eec81e861716fbed79388b",
    SCAN: "43d28f9a3ac8afb1ab97d36e2112bba950afcfd593be501a2bceeb491a55971e",
    TRANSFER: "6349ddebd4db98f8ee2eee9ad1b2d95f589c3b78269db50d60e8fe5ed21c8de6",
    SENSITIVITY: "630688a987d714a73f9b9a474277a63897afe888f6a7a39ad5108160548bf26e",
    TRANSPORT: "5f0e0fb1ea159f22d15afbeb386a7f08ce2a7bf07910becdcd18541a387aeee0",
    RESULT: "9165acf171eb6e936f81e2ddc5fd2ca7f3be465d206e5cfd0d1704e12b371aa1",
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
        "check_id": f"VAL4970_{index:02d}",
        "requirement": requirement,
        "observed": observed,
        "detail": json.dumps(detail, sort_keys=True, default=str),
        "passed": bool(passed),
        "checkpoint_marker": MARKER,
        "valid_for_full_MTS_claim": False,
        "source_checked_date": CHECKED_DATE,
    }


def finite_rows(rows: list[dict[str, str]], columns: tuple[str, ...]) -> bool:
    try:
        return all(
            math.isfinite(float(row[column]))
            for row in rows
            for column in columns
        )
    except (KeyError, TypeError, ValueError):
        return False


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    required_paths = [
        RUNNER,
        VALIDATOR,
        CONTRACT,
        SCAN,
        TRANSFER,
        SENSITIVITY,
        TRANSPORT,
        RESULT,
        PROVENANCE,
        CHECKPOINT,
        FORMAL_NOTE,
        RESUME,
        SPINE,
        CLAIMS,
        VARIABLES,
        EQUATIONS,
        RED_TEAM,
        UNIFICATION,
        *EXPECTED_HASHES,
    ]
    missing = sorted(str(path) for path in set(required_paths) if not path.exists())
    rows: list[dict[str, Any]] = []
    rows.append(
        validation_row(
            len(rows),
            "all 4970 source result document and register paths exist",
            f"{len(missing)} missing",
            missing,
            not missing,
        )
    )

    compile_failures: list[str] = []
    for script in (RUNNER, VALIDATOR):
        try:
            compile(script.read_text(encoding="utf-8"), str(script), "exec")
        except Exception as error:
            compile_failures.append(f"{script}: {error}")
    rows.append(
        validation_row(
            len(rows),
            "runner and validator compile without execution or bytecode",
            f"{len(compile_failures)} failures",
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
        relative = path.relative_to(ROOT).as_posix()
        hash_results[relative] = actual
        if actual != expected:
            hash_failures[relative] = {"expected": expected, "actual": actual}
    rows.append(
        validation_row(
            len(rows),
            "all source runner and machine-output hashes match",
            f"{len(hash_failures)} mismatches",
            hash_results,
            not missing and not hash_failures,
        )
    )

    contract = read_csv(CONTRACT)
    scans = read_csv(SCAN)
    transfer = read_csv(TRANSFER)
    sensitivity = read_csv(SENSITIVITY)
    transport = read_csv(TRANSPORT)
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    rows.append(
        validation_row(
            len(rows),
            "4970 runner passes every internal check",
            f"all_checks_pass={result['all_checks_pass']}",
            result["checks"],
            result["all_checks_pass"] and not result["valid_for_full_MTS_claim"],
        )
    )

    expected_contract_ids = {
        f"MATCH4970_{index:02d}_{suffix}"
        for index, suffix in enumerate(
            (
                "constant_offset_no_go",
                "piecewise_branch",
                "p8_replacement",
                "finite_coordinates",
                "primitive_coordinates",
            )
        )
    }
    contract_ids = {row["contract_id"] for row in contract}
    rows.append(
        validation_row(
            len(rows),
            "five matching-contract clauses are present",
            f"{len(contract)} rows",
            sorted(contract_ids),
            len(contract) == 5 and contract_ids == expected_contract_ids,
        )
    )

    no_go = next(
        (row for row in contract if row["contract_id"].endswith("constant_offset_no_go")),
        {},
    )
    rows.append(
        validation_row(
            len(rows),
            "a finite constant alone is explicitly rejected when beta slopes differ",
            no_go.get("status", "missing"),
            no_go,
            no_go.get("derivation") == "dA_OS/dt=dA_F/dt"
            and no_go.get("status")
            == "FINITE_CONSTANT_ALONE_CANNOT_RECONCILE_THE_BETA_FUNCTIONS",
        )
    )

    functional_min, functional_max = result["functional_slope_range"]
    beta_a = result["physical_R3_beta_A"]
    rows.append(
        validation_row(
            len(rows),
            "functional and physical C3 slopes are numeric unequal and opposite sign",
            f"functional=[{functional_min:.12g},{functional_max:.12g}], physical={beta_a:.12g}",
            result["matching_theorem"],
            functional_max < 0.0 < beta_a
            and not math.isclose(functional_max, beta_a, rel_tol=1e-12, abs_tol=1e-15),
        )
    )

    branch = result["onshell_branch"]
    rows.append(
        validation_row(
            len(rows),
            "the on-shell beta is explicitly scoped to the pure-Einstein branch",
            f"branch={branch['name']}; N_b-N_f={branch['N_b_minus_N_f']}",
            branch,
            branch["name"] == "PURE_EINSTEIN_MASSLESS_GRAVITON_ONLY"
            and branch["N_b_minus_N_f"] == 2
            and math.isclose(beta_a, 2.0 / (7680.0 * math.pi**3), rel_tol=2e-15)
            and "thresholds require" in branch["scope"],
        )
    )

    expected_scan_keys = {
        (scheme, order, gravity)
        for scheme in ("dynamic_etaN", "reference_etaN0")
        for order in (6, 8)
        for gravity in (1e-2, 1e-3, 1e-4, 1e-5, 1e-6)
    }
    observed_scan_keys = {
        (row["scheme"], int(row["polynomial_order"]), float(row["g_match"]))
        for row in scans
    }
    rows.append(
        validation_row(
            len(rows),
            "all twenty scheme order and matching-scale splice scans exist",
            f"{len(scans)} rows",
            sorted(observed_scan_keys),
            len(scans) == 20 and observed_scan_keys == expected_scan_keys,
        )
    )

    expected_parameters = {
        "delta_A_match",
        "delta_Bminus_match",
        "delta_Bplus_match",
        "xi_minus",
        "xi_plus",
    }
    transfer_groups: dict[str, set[str]] = {}
    for row in transfer:
        transfer_groups.setdefault(row["scan_id"], set()).add(row["parameter"])
    rows.append(
        validation_row(
            len(rows),
            "each splice has the complete five-coordinate transfer vector",
            f"{len(transfer)} rows over {len(transfer_groups)} scans",
            {key: sorted(value) for key, value in transfer_groups.items()},
            len(transfer) == 100
            and len(transfer_groups) == 20
            and all(value == expected_parameters for value in transfer_groups.values()),
        )
    )

    rows.append(
        validation_row(
            len(rows),
            "all twenty-four raw match-scale sensitivity rows exist",
            f"{len(sensitivity)} rows",
            sorted({row["quantity"] for row in sensitivity}),
            len(sensitivity) == 24
            and len({row["quantity"] for row in sensitivity}) == 6,
        )
    )

    transport_keys = {
        (row["scheme"], int(row["polynomial_order"]), float(row["target_g_match"]))
        for row in transport
    }
    rows.append(
        validation_row(
            len(rows),
            "all twenty matching-offset RG transports exist",
            f"{len(transport)} rows",
            sorted(transport_keys),
            len(transport) == 20 and transport_keys == expected_scan_keys,
        )
    )

    numeric_ok = (
        finite_rows(
            scans,
            (
                "t_match",
                "A_functional_match",
                "A_onshell_endpoint_zero_offset",
                "B_minus_matched_endpoint_zero_offsets",
                "B_plus_matched_endpoint_zero_offsets",
            ),
        )
        and finite_rows(
            transfer,
            (
                "A_endpoint_per_unit",
                "B_minus_endpoint_per_unit",
                "B_plus_endpoint_per_unit",
            ),
        )
        and finite_rows(
            transport,
            (
                "delta_A_match_transported",
                "delta_Bminus_match_transported",
                "A_endpoint_transport_residual",
                "B_minus_endpoint_transport_residual",
                "B_plus_endpoint_transport_residual",
            ),
        )
    )
    rows.append(
        validation_row(
            len(rows),
            "all matching and transport numeric fields are finite",
            f"finite={numeric_ok}",
            {},
            numeric_ok,
        )
    )

    machine_text = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (CONTRACT, SCAN, TRANSFER, SENSITIVITY, TRANSPORT, RESULT)
    )
    placeholders = [
        token
        for token in ("MISSING_", "PLACEHOLDER", "TO_BE_CALCULATED")
        if token in machine_text
    ]
    rows.append(
        validation_row(
            len(rows),
            "new machine outputs contain no placeholder markers",
            f"{len(placeholders)} markers",
            placeholders,
            not placeholders,
        )
    )

    claim_flags = [
        row.get("valid_for_full_MTS_claim", "").strip().lower()
        for dataset in (contract, scans, transfer, sensitivity, transport)
        for row in dataset
    ]
    rows.append(
        validation_row(
            len(rows),
            "every generated CSV row remains nonclaim",
            f"{len(claim_flags)} flags",
            sorted(set(claim_flags)),
            claim_flags and all(value == "false" for value in claim_flags),
        )
    )

    rows.append(
        validation_row(
            len(rows),
            "functional C3 source is replaced below the splice and never added twice",
            sorted({row["source_status"] for row in scans}),
            {},
            all(
                row["source_status"]
                == "FUNCTIONAL_C3_SOURCE_REPLACED_BY_PURE_EINSTEIN_BELOW_MATCH_NOT_ADDED"
                for row in scans
            ),
        )
    )

    rows.append(
        validation_row(
            len(rows),
            "zero finite offsets are labelled a prescription rather than a theorem",
            sorted({row["zero_offset_status"] for row in scans}),
            {},
            all(
                row["zero_offset_status"]
                == "DECLARED_CONTINUITY_PRESCRIPTION_NOT_A_THEOREM"
                for row in scans
            ),
        )
    )

    ranks_ok = all(
        int(row["matching_matrix_rank_A_Bminus_Bplus"]) == 3
        and int(row["matching_matrix_nullity_at_one_endpoint"]) == 2
        and int(row["p8_boundary_primitive_matrix_rank"]) == 2
        and int(row["p8_boundary_primitive_parameter_count"]) == 4
        for row in scans
    )
    rows.append(
        validation_row(
            len(rows),
            "endpoint transfer has rank three nullity two and p8 rank two",
            f"ranks_ok={ranks_ok}",
            {
                "endpoint_rank": result["endpoint_matrix_rank"],
                "endpoint_nullity": result["endpoint_parameter_nullity"],
            },
            ranks_ok
            and result["endpoint_matrix_rank"] == 3
            and result["endpoint_parameter_nullity"] == 2,
        )
    )

    example = next(
        row
        for row in scans
        if row["scheme"] == "dynamic_etaN"
        and int(row["polynomial_order"]) == 8
        and math.isclose(float(row["g_match"]), 1e-2)
    )
    example_ok = (
        math.isclose(
            float(example["delta_Bminus_endpoint_per_delta_A_match"]),
            109.58139954161231,
            rel_tol=2e-12,
        )
        and math.isclose(
            float(example["delta_Bminus_endpoint_per_delta_Bminus_match"]),
            0.7782765647321441,
            rel_tol=2e-12,
        )
        and math.isclose(
            float(example["delta_Bminus_endpoint_per_xi_minus"]),
            -0.009203563230610664,
            rel_tol=2e-12,
        )
    )
    rows.append(
        validation_row(
            len(rows),
            "N8 dynamic anchor transfer coefficients reproduce the locked solution",
            f"example_ok={example_ok}",
            example,
            example_ok,
        )
    )

    maximum_raw_spread = max(float(row["relative_spread"]) for row in sensitivity)
    rows.append(
        validation_row(
            len(rows),
            "zero-offset continuity exposes rather than hides match-scale dependence",
            f"maximum_relative_spread={maximum_raw_spread:.12g}",
            {},
            maximum_raw_spread > 1.0
            and math.isclose(
                maximum_raw_spread,
                result["maximum_match_scale_relative_spread"],
                rel_tol=2e-14,
            ),
        )
    )

    residual_columns = (
        "A_endpoint_transport_residual",
        "B_minus_endpoint_transport_residual",
        "B_plus_endpoint_transport_residual",
    )
    maximum_transport_residual = max(
        abs(float(row[column])) for row in transport for column in residual_columns
    )
    rows.append(
        validation_row(
            len(rows),
            "derived offset RG transport restores endpoint match-scale invariance",
            f"max_residual={maximum_transport_residual:.12g}",
            result["matching_offset_running"],
            maximum_transport_residual <= 2e-11
            and math.isclose(
                maximum_transport_residual,
                result["maximum_RG_transport_endpoint_residual"],
                rel_tol=2e-14,
            ),
        )
    )

    anchor_rows = [row for row in transport if math.isclose(float(row["target_g_match"]), 1e-2)]
    transported_rows = [
        row for row in transport if not math.isclose(float(row["target_g_match"]), 1e-2)
    ]
    anchor_zero = all(
        float(row["delta_A_match_transported"]) == 0.0
        and float(row["delta_Bminus_match_transported"]) == 0.0
        for row in anchor_rows
    )
    transported_nonzero = all(
        abs(float(row["delta_A_match_transported"])) > 0.0
        and abs(float(row["delta_Bminus_match_transported"])) > 0.0
        for row in transported_rows
    )
    rows.append(
        validation_row(
            len(rows),
            "transport changes matching coordinates while preserving the endpoint",
            f"anchor_zero={anchor_zero}; nonanchor_nonzero={transported_nonzero}",
            {},
            len(anchor_rows) == 4
            and len(transported_rows) == 16
            and anchor_zero
            and transported_nonzero,
        )
    )

    equations = result["matching_offset_running"]
    rows.append(
        validation_row(
            len(rows),
            "all three matching-coordinate running equations are retained",
            equations["status"],
            equations,
            equations["delta_A_match"]
            == "d delta_A_m/dt_m=beta_A_physical-dA_F/dt_m"
            and equations["delta_Bminus_match"]
            == "d delta_Bminus_m/dt_m=H_B delta_Bminus_m-12delta_A_m"
            and equations["delta_Bplus_match"]
            == "d delta_Bplus_m/dt_m=H_B delta_Bplus_m",
        )
    )

    discrepancies = result["source_normalization_discrepancies"]
    rows.append(
        validation_row(
            len(rows),
            "source-normalization discrepancies remain explicit and unaveraged",
            discrepancies["status"],
            discrepancies,
            discrepancies["Baratella_to_Bern"] == 10.0
            and discrepancies["Bern_to_published_FRG"] == 2.0
            and discrepancies["status"] == "EXPLICIT_NOT_AVERAGED",
        )
    )

    document_paths = (
        PROVENANCE,
        CHECKPOINT,
        FORMAL_NOTE,
        RESUME,
        SPINE,
        EQUATIONS,
        RED_TEAM,
        UNIFICATION,
    )
    marker_failures = [
        str(path)
        for path in document_paths
        if CHECKPOINT_MARKER not in path.read_text(encoding="utf-8")
    ]
    rows.append(
        validation_row(
            len(rows),
            "checkpoint marker is propagated through all handoff documents",
            f"{len(marker_failures)} failures",
            marker_failures,
            not marker_failures,
        )
    )

    claim_rows = read_csv(CLAIMS)
    claim = next((row for row in claim_rows if row.get("claim_id") == "L-812"), None)
    rows.append(
        validation_row(
            len(rows),
            "claims register contains the private nonclaim 4970 row",
            "L-812 present" if claim else "L-812 missing",
            claim or {},
            claim is not None
            and CHECKPOINT_MARKER in claim.get("notes", "")
            and "full MTS" in claim.get("risk", ""),
        )
    )

    variable_rows = read_csv(VARIABLES)
    required_variables = {
        "deltaA_match4970_MTS",
        "deltaB_match4970_MTS",
        "RGMatchFlow4970_MTS",
        "MatchingStatus4970_MTS",
    }
    observed_variables = {
        row.get("symbol", "")
        for row in variable_rows
        if row.get("symbol", "") in required_variables
    }
    rows.append(
        validation_row(
            len(rows),
            "variable audit contains all four 4970 matching rows",
            f"{len(observed_variables)}/4 present",
            sorted(observed_variables),
            observed_variables == required_variables,
        )
    )

    bt_row = next(
        (row for row in variable_rows if row.get("symbol") == "B_t4969_MTS"),
        None,
    )
    rows.append(
        validation_row(
            len(rows),
            "B_t alias uses the convention B_t=(B_plus-B_minus)/2",
            bt_row.get("aliases", "missing") if bt_row else "missing",
            bt_row or {},
            bt_row is not None
            and "(B_plus-B_minus)/2" in bt_row.get("aliases", "")
            and "(B_minus-B_plus)/2" not in bt_row.get("aliases", ""),
        )
    )

    pycache = sorted(str(path) for path in (POST / "scripts").rglob("__pycache__"))
    rows.append(
        validation_row(
            len(rows),
            "post-checkpoint scripts contain no bytecode cache",
            f"{len(pycache)} directories",
            pycache,
            not pycache,
        )
    )

    rows.append(
        validation_row(
            len(rows),
            "absolute matching anchor primitive vector and full MTS remain unclaimed",
            f"valid_for_full_MTS_claim={result['valid_for_full_MTS_claim']}",
            result["interpretation"],
            result["valid_for_full_MTS_claim"] is False
            and result["matching_parameter_vector"]
            == [
                "delta_A_match",
                "delta_Bminus_match",
                "delta_Bplus_match",
                "xi_minus",
                "xi_plus",
            ],
        )
    )

    write_csv(rows)
    failed = [row["check_id"] for row in rows if not row["passed"]]
    print(f"{MARKER}_CHECKS={len(rows)}", flush=True)
    print(f"{MARKER}_PASSED={len(rows) - len(failed)}", flush=True)
    print(f"{MARKER}_FAILED={len(failed)}", flush=True)
    print(f"{MARKER}_OUTPUT_SHA256={digest(OUTPUT)}", flush=True)
    if failed:
        print(f"{MARKER}_FAILED_IDS={','.join(failed)}", flush=True)
        return 1
    print(f"{MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

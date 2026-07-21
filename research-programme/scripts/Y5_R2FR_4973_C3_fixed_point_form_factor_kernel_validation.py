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
SOURCE = POST / "source-intake" / "functional_rg" / "4973"
RUNNER = POST / "scripts" / "Y5_R2FR_4973_C3_fixed_point_form_factor_kernel.py"
CHARACTERISTICS = SOURCE / "C3_fixed_point_characteristics.csv"
NULL_DEFORMATION = SOURCE / "C3_kernel_null_deformation.csv"
ABREU_PROJECTION = SOURCE / "C3_Abreu_finite_remainder_projection.csv"
SOURCE_REQUIREMENTS = SOURCE / "C3_form_factor_source_requirements.csv"
RESULT = SOURCE / "C3_fixed_point_form_factor_kernel_results.json"
CHECKPOINT = (
    POST
    / "4973-Y5-R2FR-C3-fixed-point-form-factor-characteristics-kernel-null-family-and-finite-anchor-verdict.md"
)
PROVENANCE = SOURCE / "PROVENANCE.md"
FORMAL_NOTE = (
    FORMAL
    / "989-PPC4161-C3-form-factor-characteristics-kernel-null-family-and-finite-anchor-verdict.md"
)
RESUME = POST / "CURRENT_LOCAL_RESUME.md"
SPINE = POST / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"
CLAIMS = FORMAL / "02-claims-register.csv"
VARIABLES = FORMAL / "04-variable-audit.csv"
EQUATIONS = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
UNIFICATION = FORMAL / "07-unification-spine.md"
OUTPUT = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_4973_VALIDATION.csv"
)

MARKER = "MTS_4973_C3_FIXED_POINT_FORM_FACTOR_KERNEL_VALIDATION"
SCIENTIFIC_MARKER = "MTS_4973_C3_FIXED_POINT_FORM_FACTOR_KERNEL"
FORMAL_MARKER = "PPC4161_C3_FORM_FACTOR_KERNEL_NO_GO_4973"

EXPECTED_HASHES = {
    RUNNER: "a6993327ca976499ff241a5c1148552a41b74dba58f39d0968a807cf80f240ba",
    CHARACTERISTICS: "431b33fd669749b16266b5dd9f4b273132f46b83dbf8c14c57a5ea4da3d3b5d9",
    NULL_DEFORMATION: "9d9611698eb4b28b815cbd438c5ae42fb8498dc181a6af2ff8bfef00c5295197",
    ABREU_PROJECTION: "2c27587ec56c9dedb3dc54235cd19b47a9e3fdabe67df28ce3f5c96195d53272",
    SOURCE_REQUIREMENTS: "6a7a5ff0cde759bca498750bacf375b90ab808bcca1a2c398038a1d55c6e6545",
    RESULT: "1cd8cd9e789832da84039dda72af2d4deed72fc310fe18dcc9250a07345ceeb1",
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


def rectangular_csv(path: Path, expected_width: int) -> tuple[bool, int]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.reader(handle))
    return bool(rows) and all(len(row) == expected_width for row in rows), len(rows)


def validation_row(
    index: int,
    test: str,
    observed: Any,
    expected: Any,
    passed: bool,
) -> dict[str, Any]:
    return {
        "check_id": f"VAL4973_{index:02d}",
        "test": test,
        "observed": json.dumps(observed, sort_keys=True, default=str),
        "expected": json.dumps(expected, sort_keys=True, default=str),
        "passed": bool(passed),
        "checkpoint_marker": FORMAL_MARKER,
        "valid_for_full_MTS_claim": False,
    }


def write_csv(rows: list[dict[str, Any]]) -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    rows: list[dict[str, Any]] = []

    missing = [str(path) for path in EXPECTED_HASHES if not path.exists()]
    rows.append(
        validation_row(
            len(rows),
            "all executable 4973 products exist",
            missing,
            [],
            not missing,
        )
    )

    hash_mismatches = {
        str(path): {"observed": digest(path), "expected": expected}
        for path, expected in EXPECTED_HASHES.items()
        if path.exists() and digest(path) != expected
    }
    rows.append(
        validation_row(
            len(rows),
            "runner and generated product hashes are locked",
            hash_mismatches,
            {},
            not hash_mismatches,
        )
    )

    runner_source = RUNNER.read_text(encoding="utf-8")
    compile(runner_source, str(RUNNER), "exec")
    rows.append(
        validation_row(
            len(rows),
            "4973 runner compiles without writing bytecode",
            "compiled",
            "compiled",
            True,
        )
    )

    result = json.loads(RESULT.read_text(encoding="utf-8"))
    failed_internal = [
        check_id for check_id, passed in result["checks"].items() if not passed
    ]
    rows.append(
        validation_row(
            len(rows),
            "scientific runner passes all internal checks",
            {"checks": len(result["checks"]), "failed": failed_internal},
            {"checks": 23, "failed": []},
            result["all_checks_pass"]
            and len(result["checks"]) == 23
            and not failed_internal,
        )
    )

    rows.append(
        validation_row(
            len(rows),
            "result retains the strict finite-anchor decision",
            {
                "decision": result["decision"],
                "valid": result["valid_for_full_MTS_claim"],
            },
            {
                "decision": "FULL_MOMENTUM_KERNEL_REQUIRED_OR_ONE_EXPLICIT_MATCHED_LAMBDA",
                "valid": False,
            },
            result["decision"]
            == "FULL_MOMENTUM_KERNEL_REQUIRED_OR_ONE_EXPLICIT_MATCHED_LAMBDA"
            and result["valid_for_full_MTS_claim"] is False,
        )
    )

    characteristics = {row["derivation_id"]: row for row in read_csv(CHARACTERISTICS)}
    rows.append(
        validation_row(
            len(rows),
            "C3 characteristic table contains all six derivation stages",
            sorted(characteristics),
            [f"C3CHAR4973_{index:02d}_{suffix}" for index, suffix in enumerate(("DIMENSION", "FIXED_POINT", "CHARACTERISTIC", "HOMOGENEOUS", "QUASILOCAL", "SOURCE_LIMIT"))],
            len(characteristics) == 6
            and "partial_lnk F=2F" in characteristics["C3CHAR4973_00_DIMENSION"]["equation"]
            and "C(z)/rho" in characteristics["C3CHAR4973_02_CHARACTERISTIC"]["result"]
            and characteristics["C3CHAR4973_04_QUASILOCAL"]["equation"] == "C(z)=0",
        )
    )

    null_rows = read_csv(NULL_DEFORMATION)
    null_shifts = {int(row["a"]): row["finite_conversion_shift"] for row in null_rows}
    null_endpoints = all(
        float(row["Delta_K_at_x0"]) == 0.0
        and float(row["Delta_K_at_xinf"]) == 0.0
        and float(row["local_beta_shift"]) == 0.0
        and float(row["asymptotic_log_slope_shift"]) == 0.0
        for row in null_rows
    )
    rows.append(
        validation_row(
            len(rows),
            "five null-kernel rows preserve both endpoints",
            {"rows": len(null_rows), "endpoints_zero": null_endpoints},
            {"rows": 5, "endpoints_zero": True},
            len(null_rows) == 5 and null_endpoints,
        )
    )
    rows.append(
        validation_row(
            len(rows),
            "null-kernel finite shifts equal minus a over two",
            null_shifts,
            {-2: "1", -1: "1/2", 0: "0", 1: "-1/2", 2: "-1"},
            null_shifts == {-2: "1", -1: "1/2", 0: "0", 1: "-1/2", 2: "-1"},
        )
    )

    projections = {row["projection_id"]: row for row in read_csv(ABREU_PROJECTION)}
    all_plus = projections["ABREU4973_++++"]
    single_minus = projections["ABREU4973_-+++"]
    rows.append(
        validation_row(
            len(rows),
            "exact local C3 projectors retain the factor-ten identity",
            {"++++": all_plus["C3_projector"], "-+++": single_minus["C3_projector"]},
            {"++++": "-15", "-+++": "-3/2"},
            all_plus["C3_projector"] == "-15"
            and single_minus["C3_projector"] == "-3/2",
        )
    )
    rows.append(
        validation_row(
            len(rows),
            "direct finite remainders give unequal apparent C3 shifts",
            {
                "++++": float(all_plus["apparent_delta_c_real"]),
                "-+++": float(single_minus["apparent_delta_c_real"]),
            },
            "non-equal",
            not math.isclose(
                float(all_plus["apparent_delta_c_real"]),
                float(single_minus["apparent_delta_c_real"]),
                rel_tol=1e-12,
                abs_tol=1e-12,
            )
            and abs(float(all_plus["apparent_delta_c_imag"])) > 0.0
            and abs(float(single_minus["apparent_delta_c_imag"])) > 0.0,
        )
    )
    invariant = projections["ABREU4973_CROSS_HELICITY"]
    rows.append(
        validation_row(
            len(rows),
            "coupling-free cross-helicity loop invariant is nonzero",
            {
                "real": invariant["Einstein_loop_remainder_real"],
                "imag": invariant["Einstein_loop_remainder_imag"],
            },
            "both nonzero",
            abs(float(invariant["Einstein_loop_remainder_real"])) > 1e-6
            and abs(float(invariant["Einstein_loop_remainder_imag"])) > 1e-6,
        )
    )
    rows.append(
        validation_row(
            len(rows),
            "finite scheme orbit is retained as an exact one-match requirement",
            projections["ABREU4973_SCHEME_ORBIT"]["status"],
            "EXACT_FINITE_RENORMALIZATION_INVARIANCE_ONE_MATCH_REQUIRED",
            projections["ABREU4973_SCHEME_ORBIT"]["status"]
            == "EXACT_FINITE_RENORMALIZATION_INVARIANCE_ONE_MATCH_REQUIRED",
        )
    )

    requirements = read_csv(SOURCE_REQUIREMENTS)
    absent = {
        row["requirement_id"]
        for row in requirements
        if row["parent_status"] == "ABSENT"
    }
    rows.append(
        validation_row(
            len(rows),
            "source ledger distinguishes absent kernel and finite match",
            {"rows": len(requirements), "absent": sorted(absent)},
            {"rows": 8, "absent": ["C3SRC4973_00_KERNEL", "C3SRC4973_07_FINITE_MATCH"]},
            len(requirements) == 8
            and absent == {"C3SRC4973_00_KERNEL", "C3SRC4973_07_FINITE_MATCH"},
        )
    )

    missing_source_paths: list[str] = []
    for row in requirements:
        for source_path in row["source_path"].split(";"):
            if source_path and not (ROOT / source_path).exists():
                missing_source_paths.append(source_path)
    rows.append(
        validation_row(
            len(rows),
            "every local source-ledger path exists",
            missing_source_paths,
            [],
            not missing_source_paths,
        )
    )

    scientific_rows = (
        list(characteristics.values())
        + null_rows
        + list(projections.values())
        + requirements
    )
    rows.append(
        validation_row(
            len(rows),
            "all generated scientific rows remain private nonclaim",
            {"rows": len(scientific_rows)},
            {"all_valid_for_full_MTS_claim": False},
            all(
                row["checkpoint_marker"] == SCIENTIFIC_MARKER
                and row["valid_for_full_MTS_claim"] == "False"
                for row in scientific_rows
            ),
        )
    )

    scientific_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (
            CHARACTERISTICS,
            NULL_DEFORMATION,
            ABREU_PROJECTION,
            SOURCE_REQUIREMENTS,
            RESULT,
        )
    )
    rows.append(
        validation_row(
            len(rows),
            "generated products contain no missing-input sentinels",
            {"MISSING_": scientific_text.count("MISSING_")},
            {"MISSING_": 0},
            "MISSING_" not in scientific_text,
        )
    )

    handoff_paths = (
        CHECKPOINT,
        PROVENANCE,
        FORMAL_NOTE,
        RESUME,
        SPINE,
        EQUATIONS,
        RED_TEAM,
        UNIFICATION,
    )
    missing_markers = [
        str(path)
        for path in handoff_paths
        if not path.exists() or FORMAL_MARKER not in path.read_text(encoding="utf-8")
    ]
    rows.append(
        validation_row(
            len(rows),
            "formal marker propagates through every handoff document",
            missing_markers,
            [],
            not missing_markers,
        )
    )

    claims_rectangular, claims_count = rectangular_csv(CLAIMS, 13)
    claim_rows = read_csv(CLAIMS)
    claim_815 = [row for row in claim_rows if row["claim_id"] == "L-815"]
    rows.append(
        validation_row(
            len(rows),
            "claims register is rectangular and contains one L-815 row",
            {"rows": claims_count, "L-815": len(claim_815)},
            {"L-815": 1},
            claims_rectangular
            and len(claim_815) == 1
            and FORMAL_MARKER in claim_815[0]["notes"],
        )
    )

    variables_rectangular, variables_count = rectangular_csv(VARIABLES, 11)
    expected_symbols = {
        "F_C34973_MTS",
        "H_C34973_MTS",
        "C_z4973_MTS",
        "DeltaK_a4973_MTS",
        "FiniteSchemeOrbit4973_MTS",
        "PredictivityStatus4973_MTS",
    }
    variable_rows = read_csv(VARIABLES)
    observed_symbols = {
        row["symbol"] for row in variable_rows if row["symbol"] in expected_symbols
    }
    rows.append(
        validation_row(
            len(rows),
            "variable audit is rectangular and contains all six 4973 symbols",
            {"rows": variables_count, "symbols": sorted(observed_symbols)},
            sorted(expected_symbols),
            variables_rectangular and observed_symbols == expected_symbols,
        )
    )

    resume_text = RESUME.read_text(encoding="utf-8")
    spine_text = SPINE.read_text(encoding="utf-8")
    rows.append(
        validation_row(
            len(rows),
            "resume and coupling spine point to checkpoint 4973",
            {
                "resume_4973": "Last checkpoint: `4973-" in resume_text,
                "spine_4973": "Current State Through 4973" in spine_text,
            },
            {"resume_4973": True, "spine_4973": True},
            "Last checkpoint: `4973-" in resume_text
            and "Current State Through 4973" in spine_text,
        )
    )

    rows.append(
        validation_row(
            len(rows),
            "handoff selects kernel assembly rather than another local audit",
            "Gamma_k^(2)" in resume_text,
            True,
            "Gamma_k^(2)" in resume_text
            and "should not perform another source inventory" in CHECKPOINT.read_text(
                encoding="utf-8"
            ),
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

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
SOURCE = POST / "source-intake" / "functional_rg" / "4934"
OUTPUT = POST / "source-intake" / "mts_residuals"
CHECKPOINT = POST / "4934-Y5-R2FR-portal-a6-completion-and-direct-C3-photon-Hessian-gate.md"
FORMAL_NOTE = FORMAL / "950-PPC4161-source-complete-C3-CFF-F4-flow.md"
PROVENANCE = SOURCE / "PROVENANCE.md"
CLAIMS = FORMAL / "02-claims-register.csv"
VARIABLES = FORMAL / "04-variable-audit.csv"
EQUATIONS = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
SPINE = FORMAL / "07-unification-spine.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"
OUTPUT_CSV = OUTPUT / "P8_Y5_BRR545_4934_VALIDATION.csv"

MARKER = "MTS_SOURCE_COMPLETE_C3_CFF_F4_FLOW_4934"
FORMAL_MARKER = "PPC4161_SOURCE_COMPLETE_C3_CFF_F4_FLOW_4934"
VALIDATION_MARKER = "MTS_SOURCE_COMPLETE_C3_CFF_F4_FLOW_VALIDATION_4934"
NEXT_TARGET = "4935-Y5-R2FR-completed-fixed-point-GR-connected-trajectory-and-motion-sector-entry.md"
CHECKED_DATE = "2026-07-12"

SCRIPTS = (
    POST / "scripts" / "Y5_R2FR_4934_c3_photon_projection_selection.py",
    POST / "scripts" / "Y5_R2FR_4934_portal_linear_c3_zero.py",
    POST / "scripts" / "Y5_R2FR_4934_portal_quadratic_c3.py",
    POST / "scripts" / "Y5_R2FR_4934_direct_c3_cff_principal.py",
    POST / "scripts" / "Y5_R2FR_4934_completed_combined_flow.py",
    Path(__file__),
)

RESULTS = {
    "selection": SOURCE / "c3_photon_projection_selection_results.json",
    "linear": SOURCE / "portal_linear_c3_zero_results.json",
    "quadratic": SOURCE / "portal_quadratic_c3_results.json",
    "direct": SOURCE / "direct_c3_cff_principal_results.json",
    "completed": SOURCE / "completed_combined_flow_results.json",
}

HASH_LOCKS = {
    SOURCE / "hep-th-9708152-source.gz": "a6e7967d52207ebe3f7a8795b7fa052ecddf82ef942eb098995f8b62b2f38c94",
    SOURCE / "vandeven9708152" / "ncnotes12.tex": "b75bbee3d477afcd8bb3f916de6daa8ba78bf1853d79042ba7685c30d123f7d8",
    SOURCE / "hep-th-9704166-source.tar": "70582fbba17ccff37152ca195a292ff91870280ea3bae00b405335cca0e158f2",
    SOURCE / "avramidi9704166.tex": "647f6a15cf6736adabff1c9761b43859f71a7641b5dd0d35de18bb576a572902",
    RESULTS["selection"]: "ab925e077ca13913127105bf3619604e022dd57305f9b5cb4cbe053760eabc01",
    RESULTS["linear"]: "f0f30c1233d36d47a92655dd0023918f978d5a76056ffd196a378cdb3156c002",
    RESULTS["quadratic"]: "a939bf7f1464dc58cd61ea69f907d4d3bb29dd2b8aec36fa51c2ffbaa15ec574",
    RESULTS["direct"]: "00c2c4ed4a2ece0611a6b167e885a9811b8748cace0a456337ac03e426034a95",
    RESULTS["completed"]: "c70583d03ec773fb31aca0cb0ac73e662c66c6146ee8bfcdeb07598ddfe43978",
    POST / "source-intake" / "functional_rg" / "4933" / "combined_c3_photon_stability_results.json": "082c527e9ce2cfa722abcde9515606162bdb6fe55148ef41e316f78e82d52e0b",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


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
        *RESULTS.values(),
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
        "VAL4934_00_paths",
        "all source artifacts scripts results documents and registers exist",
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
        "VAL4934_01_compile",
        "all six checkpoint scripts compile without writing bytecode",
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
        "VAL4934_02_hashes",
        "all ten source and result artifacts match locked SHA-256 hashes",
        "10 matches",
        "OK" if not hash_failures else str(hash_failures),
        not hash_failures,
    )

    data = {name: load_json(path) for name, path in RESULTS.items()}
    selection = data["selection"]
    forbidden = set(selection["projection_theorem"]["forbidden_rows"])
    selection_ok = (
        forbidden == {"F2", "FDeltaF", "RFF", "SFF", "F2sq", "F4"}
        and selection["projection_theorem"]["allowed_rows"] == ["CFF"]
        and selection["projection_theorem"]["rows_eliminated"] == 6
        and selection["projection_theorem"]["rows_remaining"] == 1
    )
    add_check(
        checks,
        "VAL4934_03_selection",
        "the direct C3 Hessian selection theorem eliminates exactly six rows and leaves only CFF",
        "forbidden=6; allowed=CFF",
        f"forbidden={sorted(forbidden)}; allowed={selection['projection_theorem']['allowed_rows']}",
        selection_ok,
    )

    linear = data["linear"]
    linear_parts = linear["weyl_cubic_projections"]
    linear_ok = (
        linear["normalization_check"]["ratio_to_C_squared"] == "-1/4"
        and linear["normalization_check"]["passed"]
        and set(linear_parts.values()) == {"0"}
        and linear["theorem"]["formula"] == "Delta RHS_C3|linear in g_CFF = 0"
        and linear["theorem"]["passed"]
        and linear["all_checks_pass"]
    )
    add_check(
        checks,
        "VAL4934_04_linear_zero",
        "the lower normalization is -1/4 and every linear portal Weyl-cubic contribution vanishes exactly",
        "ratio=-1/4; four parts=0; theorem=true",
        f"ratio={linear['normalization_check']['ratio_to_C_squared']}; parts={linear_parts}",
        linear_ok,
    )

    records = set(linear["primary_records"])
    expected_records = {
        "https://arxiv.org/abs/hep-th/9708152",
        "https://arxiv.org/abs/hep-th/9704166",
        "https://arxiv.org/abs/2312.03831",
        "https://arxiv.org/abs/2405.08860",
    }
    provenance_text = read_text(PROVENANCE)
    provenance_ok = records == expected_records and all(record in provenance_text for record in records)
    add_check(
        checks,
        "VAL4934_05_provenance",
        "all four primary records are present in both the result and provenance ledger",
        str(sorted(expected_records)),
        str(sorted(records)),
        provenance_ok,
    )

    quadratic = data["quadratic"]
    quadratic_formula = "Delta RHS_C3|g_CFF^2 = g_CFF^2*(5 gamma_a - 3 gamma_DF + 20)/(80 pi^2)"
    quadratic_ok = (
        quadratic["symbolic_contractions"]["flat_ratio_to_C_squared"] == "6"
        and quadratic["symbolic_contractions"]["connection_ratio_to_C_cubed"] == "3/2"
        and quadratic["theorem"]["formula"] == quadratic_formula
        and quadratic["theorem"]["passed"]
        and not quadratic["remaining_portal_a6_terms"]
        and quadratic["all_checks_pass"]
    )
    add_check(
        checks,
        "VAL4934_06_quadratic",
        "the exact quadratic portal row reproduces the 6 and 3/2 contractions and leaves no a6 term open",
        "ratios=6,3/2; exact formula; remaining=0",
        f"ratios={quadratic['symbolic_contractions']['flat_ratio_to_C_squared']},{quadratic['symbolic_contractions']['connection_ratio_to_C_cubed']}; formula={quadratic['theorem']['formula']}",
        quadratic_ok,
    )

    direct = data["direct"]
    expected_ratios = {
        "diagonal_Maxwell": "7/32",
        "mixed_Maxwell": "7/32",
        "c3_cubic": "-27/64",
        "CFF_diagonal": "-7/8",
        "CFF_mixed_cross": "-7/8",
        "CFF_mixed_square": "7/8",
        "n2_trace": "0",
    }
    direct_ratios = direct["angular_ratios"]
    direct_ok = (
        all(direct_ratios[key] == value for key, value in expected_ratios.items())
        and direct["source_cubic_calibration"]["source_trace_polarization_calibration"] == "1/2"
        and all(direct["checks"].values())
        and direct["claim_boundary"]["full_direct_C3_to_CFF_coefficient_derived"]
        and not direct["claim_boundary"]["full_combined_fixed_point_claimed"]
        and math.isfinite(direct["direct_coefficient"]["coefficient_at_4933_partial_point"])
    )
    add_check(
        checks,
        "VAL4934_07_direct",
        "all exact direct angular ratios and the source 1/2 calibration pass and the full C3-to-CFF coefficient is derived",
        f"{expected_ratios}; calibration=1/2; full_direct=true",
        f"ratios={direct_ratios}; boundary={direct['claim_boundary']}",
        direct_ok,
    )

    completed = data["completed"]
    point = completed["source_complete_selected_row_fixed_point"]
    root_ok = (
        point["success"]
        and len(point["coordinates_g_gplus_gminus_gCFF_h"]) == 5
        and point["beta_residual_infinity_norm"] < 1.0e-9
        and all(math.isfinite(value) for value in point["coordinates_g_gplus_gminus_gCFF_h"])
    )
    add_check(
        checks,
        "VAL4934_08_root",
        "the completed five-coordinate root converges with finite coordinates and beta infinity norm below 1e-9",
        "success=true; five finite coordinates; residual<1e-9",
        f"success={point['success']}; x={point['coordinates_g_gplus_gminus_gCFF_h']}; residual={point['beta_residual_infinity_norm']}",
        root_ok,
    )

    index = point["signed_index"]
    stability_ok = (
        len(point["beta_eigenvalues"]) == 5
        and index == {"negative_real_parts": 1, "positive_real_parts": 4}
        and point["signed_imaginary_axis_gap"] > 0.24
        and all(math.isfinite(item["real"]) and math.isfinite(item["imag"]) for item in point["beta_eigenvalues"])
    )
    add_check(
        checks,
        "VAL4934_09_stability",
        "the completed beta matrix has one negative and four positive real parts with signed gap above 0.24",
        "index=1/4; gap>0.24",
        f"index={index}; gap={point['signed_imaginary_axis_gap']}; eigenvalues={point['beta_eigenvalues']}",
        stability_ok,
    )

    new_sources = completed["new_exact_sources"]
    source_rows_ok = (
        new_sources["linear_portal_C3_projection"] == 0.0
        and abs(new_sources["quadratic_portal_C3_projection"]) > 0.0
        and abs(new_sources["direct_C3_to_CFF_projection"]) > 0.0
        and completed["checks"]["portal_quadratic_included"]
        and completed["checks"]["direct_C3_CFF_included"]
    )
    add_check(
        checks,
        "VAL4934_10_source_rows",
        "the linear zero and both nonzero completed source rows are explicitly included in the rerun",
        "linear=0; quadratic!=0; direct!=0; included=true",
        str(new_sources),
        source_rows_ok,
    )

    contract = completed["canonical_projection_contract"]
    duplicate = completed["diagnostic_duplicate_lower_photon_residual"]
    contract_ok = (
        contract["equations"] == 20
        and contract["unknown_flow_coefficients"] == 20
        and "diagnostic only" in contract["duplicate_lower_photon_rows"]
        and duplicate["infinity_norm"] > 0.0
        and "diagnostic" in duplicate["claim_use"]
        and len(duplicate["values"]) == 5
    )
    add_check(
        checks,
        "VAL4934_11_contract",
        "the canonical 20-row contract is square and the five duplicate lower rows remain a nonzero diagnostic",
        "20=20; five diagnostic rows; residual>0",
        f"contract={contract}; duplicate={duplicate}",
        contract_ok,
    )

    boundary_ok = (
        point["is_source_complete_for_declared_minimal_truncation"]
        and not point["is_full_MTS_fixed_point"]
        and completed["remaining_exact_source_blocks_in_declared_minimal_C3_CFF_F4_system"] == []
        and completed["next_physics_boundary"] == [
            "trajectory integration from the completed fixed point",
            "larger operator-basis stability test",
            "connection to the parent MTS motion/time/source sector",
        ]
    )
    add_check(
        checks,
        "VAL4934_12_boundary",
        "the minimal source basis is complete while full MTS remains false and trajectory basis and motion extensions stay open",
        "minimal=true; full_MTS=false; remaining_exact=0",
        f"minimal={point['is_source_complete_for_declared_minimal_truncation']}; full={point['is_full_MTS_fixed_point']}; remaining={completed['remaining_exact_source_blocks_in_declared_minimal_C3_CFF_F4_system']}",
        boundary_ok,
    )

    documents = {
        "checkpoint": read_text(CHECKPOINT),
        "formal": read_text(FORMAL_NOTE),
        "claims": read_text(CLAIMS),
        "variables": read_text(VARIABLES),
        "equations": read_text(EQUATIONS),
        "red_team": read_text(RED_TEAM),
        "spine": read_text(SPINE),
        "resume": read_text(RESUME),
    }
    marker_requirements = {
        "checkpoint": MARKER,
        "formal": FORMAL_MARKER,
        "claims": "L-776",
        "variables": "SourceCompleteStatus4934_MTS",
        "equations": "## 1.227 Source-complete `C3-CFF-F4` flow",
        "red_team": "## 178. Source-complete minimal flow is not full-MTS trajectory closure",
        "spine": "## PPC4161 checkpoint 4934 - Source-complete `C3-CFF-F4` flow",
        "resume": NEXT_TARGET,
    }
    missing_markers = [name for name, marker in marker_requirements.items() if marker not in documents[name]]
    add_check(
        checks,
        "VAL4934_13_registers",
        "checkpoint formal note and all canonical registers contain their 4934 markers",
        "0 missing markers",
        str(missing_markers),
        not missing_markers,
    )

    claim_rows = []
    with CLAIMS.open("r", encoding="utf-8-sig", newline="") as handle:
        claim_rows = [row for row in csv.DictReader(handle) if row.get("claim_id") == "L-776"]
    claim_ok = (
        len(claim_rows) == 1
        and "full_MTS" in claim_rows[0]["status"]
        and "local GR" in claim_rows[0]["risk"]
        and NEXT_TARGET in claim_rows[0]["next_test"]
    )
    add_check(
        checks,
        "VAL4934_14_claim_policy",
        "the single L-776 row keeps full MTS and local-GR promotion explicitly blocked and selects trajectory integration",
        "one row; full_MTS blocked; local GR prohibited; next=4935",
        str(claim_rows),
        claim_ok,
    )

    cache_paths = sorted(str(path) for path in POST.rglob("__pycache__"))
    add_check(
        checks,
        "VAL4934_15_cache",
        "no Python bytecode cache directories remain under post-checkpoint-work",
        "0 __pycache__ directories",
        str(cache_paths),
        not cache_paths,
    )

    placeholder_hits = []
    for path in (CHECKPOINT, FORMAL_NOTE, PROVENANCE):
        if "MISSING_" in read_text(path):
            placeholder_hits.append(path.name)
    add_check(
        checks,
        "VAL4934_16_placeholders",
        "authored checkpoint documents contain no MISSING_ placeholder tokens",
        "0 documents",
        str(placeholder_hits),
        not placeholder_hits,
    )

    all_pass = all(bool(row["passed"]) for row in checks)
    add_check(
        checks,
        "VAL4934_17_gate",
        "every prior 4934 validation check passes while all rows remain private nonclaim evidence",
        "all prior passed; valid_for_claim=false",
        f"prior_passed={all_pass}; rows={len(checks)}",
        all_pass,
    )

    OUTPUT.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "validation_id",
        "requirement",
        "expected",
        "actual",
        "passed",
        "checkpoint_marker",
        "valid_for_claim",
        "source_checked_date",
    ]
    with OUTPUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(checks)

    failed = [row["validation_id"] for row in checks if not row["passed"]]
    print(f"Wrote {OUTPUT_CSV}")
    print(f"Checks: {len(checks)}; failed: {failed}")
    print(f"Source-complete point: {point['coordinates_g_gplus_gminus_gCFF_h']}")
    print(f"Signed index: {index}; gap={point['signed_imaginary_axis_gap']}")
    print(f"Full MTS fixed point: {point['is_full_MTS_fixed_point']}")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())


from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Any

from scipy.constants import G, alpha, c, hbar, m_e


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
SOURCE = POST / "source-intake" / "functional_rg" / "4932"
GENERATOR = POST / "scripts" / "Y5_R2FR_4932_photon_graviton_flow_MTS_projection.py"
CHECKPOINT = POST / "4932-Y5-R2FR-MTS-gauge-portal-functional-trace-projection-or-two-sided-polarization-likelihood.md"
FORMAL_NOTE = FORMAL / "948-PPC4161-photon-graviton-flow-MTS-portal-projection.md"
CLAIMS = FORMAL / "02-claims-register.csv"
VARIABLES = FORMAL / "04-variable-audit.csv"
EQUATIONS = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
SPINE = FORMAL / "07-unification-spine.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"

MARKER = "MTS_PHOTON_GRAVITON_FLOW_MTS_PROJECTION_4932"
VALIDATION_MARKER = "MTS_PHOTON_GRAVITON_FLOW_MTS_PROJECTION_VALIDATION_4932"
CHECKED_DATE = "2026-07-12"

TABLES = {
    "scheme": ("P8_Y5_R2FR_4932_SOURCE_SCHEME.csv", 7),
    "operators": ("P8_Y5_R2FR_4932_ESSENTIAL_OPERATOR_CLOSURE.csv", 6),
    "fixed": ("P8_Y5_R2FR_4932_PUBLISHED_FIXED_POINTS.csv", 4),
    "stability": ("P8_Y5_R2FR_4932_SIGNED_STABILITY.csv", 4),
    "maps": ("P8_Y5_R2FR_4932_MTS_NORMALIZATION_MAP.csv", 5),
    "wilson": ("P8_Y5_R2FR_4932_FP1_IR_WILSON.csv", 6),
    "si": ("P8_Y5_R2FR_4932_FP1_SI_PROJECTION.csv", 5),
    "hierarchy": ("P8_Y5_R2FR_4932_QED_VS_QG_HIERARCHY.csv", 3),
    "positivity": ("P8_Y5_R2FR_4932_POSITIVITY_COMBINATIONS.csv", 3),
    "inheritance": ("P8_Y5_R2FR_4932_MTS_INHERITANCE_GATE.csv", 8),
    "sources": ("P8_Y5_R2FR_4932_SOURCE_REGISTER.csv", 15),
    "gates": ("P8_Y5_R2FR_4932_GATE_DECISION.csv", 11),
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def is_true(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def is_false(value: Any) -> bool:
    return str(value).strip().lower() == "false"


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
    rows_by_name: dict[str, list[dict[str, str]]] = {}

    required_paths = [
        GENERATOR,
        CHECKPOINT,
        FORMAL_NOTE,
        CLAIMS,
        VARIABLES,
        EQUATIONS,
        RED_TEAM,
        SPINE,
        RESUME,
        SOURCE / "PROVENANCE.md",
        SOURCE / "2405.08860.pdf",
        SOURCE / "2405.08860-source.tar",
        SOURCE / "RHS_general_regulator.nb",
        SOURCE / "datacite-10.17632-tysd636dn4.1.json",
        SOURCE / "mendeley-files-metadata.json",
    ]
    missing_paths = [str(path) for path in required_paths if not path.exists()]
    add_check(
        checks,
        "VAL4932_00_paths",
        "all authored and source packet paths exist",
        "0 missing",
        f"missing={len(missing_paths)}; {missing_paths[:3]}",
        not missing_paths,
    )

    compile_failures: list[str] = []
    for path in (GENERATOR, Path(__file__)):
        try:
            compile(read_text(path), str(path), "exec")
        except SyntaxError as error:
            compile_failures.append(f"{path.name}:{error}")
    add_check(
        checks,
        "VAL4932_01_compile",
        "generator and validator compile without bytecode artifacts",
        "0 syntax errors",
        str(compile_failures),
        not compile_failures,
    )

    table_failures: list[str] = []
    for name, (filename, expected_rows) in TABLES.items():
        path = OUTPUT / filename
        if not path.exists():
            table_failures.append(f"{name}:missing")
            rows_by_name[name] = []
            continue
        rows = read_csv(path)
        rows_by_name[name] = rows
        if len(rows) != expected_rows:
            table_failures.append(f"{name}:{len(rows)}!={expected_rows}")
    add_check(
        checks,
        "VAL4932_02_tables",
        "all twelve evidence CSVs parse with declared row counts",
        ";".join(f"{name}:{count}" for name, (_, count) in TABLES.items()),
        "OK" if not table_failures else ";".join(table_failures),
        not table_failures,
    )

    all_rows = [row for rows in rows_by_name.values() for row in rows]
    marker_failures = sum(row.get("checkpoint_marker") != MARKER for row in all_rows)
    claim_failures = sum(not is_false(row.get("valid_for_claim")) for row in all_rows)
    passed_failures = sum(not is_true(row.get("passed", "True")) for row in all_rows)
    missing_tokens = sum("MISSING_" in str(value) for row in all_rows for value in row.values())
    add_check(
        checks,
        "VAL4932_03_row_policy",
        "all evidence rows carry marker, remain nonclaim, pass internal checks, and contain no missing placeholders",
        "marker_failures=0; claim_failures=0; passed_failures=0; MISSING=0",
        f"marker_failures={marker_failures}; claim_failures={claim_failures}; passed_failures={passed_failures}; MISSING={missing_tokens}",
        marker_failures == claim_failures == passed_failures == missing_tokens == 0,
    )

    fixed = {row["fixed_point"]: row for row in rows_by_name["fixed"]}
    fp1 = fixed.get("FP1", {})
    fp1_ok = (
        math.isclose(float(fp1.get("g_star", "nan")), 0.131)
        and math.isclose(float(fp1.get("g_plus_star", "nan")), 0.351)
        and math.isclose(float(fp1.get("g_minus_star", "nan")), 3.327)
        and math.isclose(float(fp1.get("g_CFF_star", "nan")), 0.00375)
        and fp1.get("relevant_directions") == "1"
        and is_true(fp1.get("GR_connected_IR"))
    )
    add_check(
        checks,
        "VAL4932_04_FP1",
        "published FP1 coordinates and relevance are reproduced",
        "0.131,0.351,3.327,0.00375; one relevant; GR connected",
        str(fp1),
        fp1_ok,
    )

    fp2 = fixed.get("FP2", {})
    mfp = fixed.get("MFP", {})
    branch_ok = fp2.get("relevant_directions") == "2" and is_true(fp2.get("gravity_active")) and is_false(mfp.get("gravity_active"))
    add_check(
        checks,
        "VAL4932_05_branch_count",
        "FP2 has two relevant directions and the MFP is gravity free",
        "FP2 relevant=2; MFP gravity_active=False",
        f"FP2={fp2.get('relevant_directions')}; MFP={mfp.get('gravity_active')}",
        branch_ok,
    )

    operator_rows = rows_by_name["operators"]
    required_dynamic = [row for row in operator_rows if is_true(row.get("essential_dynamic_coordinate")) and is_true(row.get("required_for_CFF_flow"))]
    f4_required = {row.get("coordinate") for row in required_dynamic if "g_plus" in row.get("coordinate", "") or "g_minus" in row.get("coordinate", "")}
    add_check(
        checks,
        "VAL4932_06_operator_closure",
        "the CFF flow contains four essential dynamic coordinates including both F4 directions",
        "4 dynamic required; g_plus and g_minus present",
        f"dynamic={len(required_dynamic)}; F4={sorted(f4_required)}",
        len(required_dynamic) == 4 and len(f4_required) == 2,
    )

    map_rows = {row["map_id"]: row for row in rows_by_name["maps"]}
    map_ok = map_rows.get("MAP4932_00_operator", {}).get("map") == "c_gamma=G_CFF" and map_rows.get("MAP4932_01_dimensionless", {}).get("map") == "u_gamma=g_CFF"
    add_check(
        checks,
        "VAL4932_07_map",
        "source portal maps exactly into the MTS operator and dimensionless coordinate",
        "c_gamma=G_CFF; u_gamma=g_CFF",
        f"{map_rows.get('MAP4932_00_operator', {}).get('map')}; {map_rows.get('MAP4932_01_dimensionless', {}).get('map')}",
        map_ok,
    )

    stability = {row["fixed_point"]: row for row in rows_by_name["stability"]}
    fp1_stability = stability.get("FP1", {})
    fp2_stability = stability.get("FP2", {})
    stability_ok = math.isclose(float(fp1_stability.get("distance_to_imaginary_axis", "nan")), 0.239) and math.isclose(float(fp2_stability.get("distance_to_imaginary_axis", "nan")), 0.141)
    add_check(
        checks,
        "VAL4932_08_stability",
        "signed beta-spectrum gaps are calculated from lambda=-theta",
        "FP1=0.239; FP2=0.141",
        f"FP1={fp1_stability.get('distance_to_imaginary_axis')}; FP2={fp2_stability.get('distance_to_imaginary_axis')}",
        stability_ok,
    )

    combined = stability.get("FP1_plus_4930_blocks", {})
    tighten = float(combined.get("tightening_factor_vs_1p88", "nan"))
    add_check(
        checks,
        "VAL4932_09_mixing_gate",
        "the combined sufficient gate is 0.239 and tightens the old 1.88 comparator",
        "norm(E_modal)_2<0.239; factor=7.8661087866",
        f"{combined.get('sufficient_modal_mixing_bound')}; factor={tighten}",
        combined.get("sufficient_modal_mixing_bound") == "norm(E_modal)_2<0.239" and math.isclose(tighten, 1.88 / 0.239),
    )

    wilson = {row["quantity"]: row for row in rows_by_name["wilson"]}
    wc = float(wilson.get("W_C", {}).get("value", "nan"))
    uv_ratio = float(wilson.get("g_CFF*/(16pi g*)", {}).get("value", "nan"))
    add_check(
        checks,
        "VAL4932_10_wilson",
        "published IR W_C is reproduced and kept distinct from the UV ratio",
        "W_C=0.000550; UV ratio=0.0005694952639; unequal",
        f"W_C={wc}; UV={uv_ratio}",
        math.isclose(wc, 0.000550) and math.isclose(uv_ratio, 0.00375 / (16.0 * math.pi * 0.131)) and not math.isclose(wc, uv_ratio, rel_tol=1.0e-3),
    )

    si_rows = {row["quantity"]: row for row in rows_by_name["si"]}
    planck_length = math.sqrt(hbar * G / c**3)
    expected_c_fp1 = 16.0 * math.pi * planck_length**2 * 0.000550
    actual_c_fp1 = float(si_rows.get("c_gamma^parent,FP1,IR", {}).get("value", "nan"))
    add_check(
        checks,
        "VAL4932_11_SI",
        "FP1 W_C converts to the conditional SI parent coefficient",
        f"{expected_c_fp1:.16e} m^2",
        f"{actual_c_fp1:.16e} m^2",
        math.isclose(actual_c_fp1, expected_c_fp1, rel_tol=1.0e-15),
    )

    expected_electron = -alpha * (hbar / (m_e * c)) ** 2 / (360.0 * math.pi)
    hierarchy_rows = {row["comparison_id"]: row for row in rows_by_name["hierarchy"]}
    ratio = float(hierarchy_rows.get("HIER4932_00_QED_vs_QG", {}).get("ratio", "nan"))
    add_check(
        checks,
        "VAL4932_12_hierarchy",
        "known electron threshold dominates the conditional FP1 parent portal",
        f"{abs(expected_electron) / expected_c_fp1:.16e}",
        f"{ratio:.16e}",
        math.isclose(ratio, abs(expected_electron) / expected_c_fp1, rel_tol=1.0e-15) and ratio > 1.0e40,
    )

    positivity = {row["bound_id"]: row for row in rows_by_name["positivity"]}
    p_first = positivity.get("POS4932_00_first", {})
    p_second = positivity.get("POS4932_01_second", {})
    positivity_ok = math.isclose(float(p_first.get("value", "nan")), -0.07284, abs_tol=1.0e-12) and math.isclose(float(p_second.get("value", "nan")), -0.08758, abs_tol=1.0e-12) and is_false(p_first.get("satisfied")) and is_false(p_second.get("satisfied"))
    add_check(
        checks,
        "VAL4932_13_positivity",
        "nominal FP1 positivity combinations are reconstructed without hiding their signs",
        "-0.07284 and -0.08758; both unsatisfied",
        f"{p_first.get('value')}; {p_second.get('value')}",
        positivity_ok,
    )

    inheritance_rows = rows_by_name["inheritance"]
    closed_count = sum(is_true(row.get("closed")) for row in inheritance_rows)
    open_blockers = sum(is_false(row.get("closed")) and is_true(row.get("blocking_if_open")) for row in inheritance_rows)
    add_check(
        checks,
        "VAL4932_14_inheritance",
        "only exact normalization is closed and all seven dynamic inheritance clauses remain blocking",
        "closed=1; open_blockers=7",
        f"closed={closed_count}; open_blockers={open_blockers}",
        closed_count == 1 and open_blockers == 7,
    )

    source_rows = rows_by_name["sources"]
    hash_rows = [row for row in source_rows if row.get("verification") == "SHA256"]
    source_failures: list[str] = []
    for row in source_rows:
        source_ref = row.get("source_path_or_url", "")
        if source_ref.startswith("http"):
            continue
        if not (ROOT / Path(source_ref)).exists():
            source_failures.append(source_ref)
    hashes_ok = len(hash_rows) == 5 and all(row.get("expected_sha256") == row.get("actual_sha256") for row in hash_rows)
    add_check(
        checks,
        "VAL4932_15_sources",
        "all local source references exist and five locked hashes match",
        "missing=0; hash_rows=5; mismatches=0",
        f"missing={len(source_failures)}; hash_rows={len(hash_rows)}; hashes_ok={hashes_ok}",
        not source_failures and hashes_ok,
    )

    scheme = {row["scheme_id"]: row for row in rows_by_name["scheme"]}
    notebook_row = scheme.get("SCHEME4932_05_notebook", {})
    execution_firewall = is_false(notebook_row.get("independently_executed")) and "18 BoxData input cells and 0 stored Output cells" in notebook_row.get("source_statement", "")
    add_check(
        checks,
        "VAL4932_16_execution_firewall",
        "official notebook acquisition is not mislabeled as independent execution",
        "independently_executed=False; 18 inputs; 0 outputs",
        str(notebook_row),
        execution_firewall,
    )

    gate_rows = {row["gate"]: row for row in rows_by_name["gates"]}
    gate_ok = gate_rows.get("MTS_fixed_point_inheritance", {}).get("status") == "OPEN_BUT_NOW_QUANTIFIED" and is_false(gate_rows.get("MTS_fixed_point_inheritance", {}).get("claim_promoted")) and gate_rows.get("next_target", {}).get("decision", "").startswith("4933-")
    add_check(
        checks,
        "VAL4932_17_gate",
        "MTS inheritance remains unpromoted and the next target is the combined flow",
        "OPEN; claim=False; target=4933",
        f"{gate_rows.get('MTS_fixed_point_inheritance', {}).get('status')}; {gate_rows.get('MTS_fixed_point_inheritance', {}).get('claim_promoted')}; {gate_rows.get('next_target', {}).get('decision')}",
        gate_ok,
    )

    checkpoint_text = read_text(CHECKPOINT)
    formal_text = read_text(FORMAL_NOTE)
    docs_ok = all(
        token in checkpoint_text
        for token in (
            MARKER,
            "7.221914138634598e-72",
            "||E_modal||_2<0.239",
            "not re-executed",
            "full MTS enlarged fixed point",
        )
    ) and all(token in formal_text for token in ("PPC4161_PHOTON_GRAVITON_FLOW_MTS_PROJECTION_4932", "W_C=lim G_CFF/(16pi G_N)=0.000550", "full MTS fixed point"))
    add_check(
        checks,
        "VAL4932_18_docs",
        "checkpoint and formal note contain numeric result and claim firewalls",
        "all required markers present",
        f"checkpoint_chars={len(checkpoint_text)}; formal_chars={len(formal_text)}",
        docs_ok,
    )

    claims_rows = read_csv(CLAIMS)
    variable_rows = read_csv(VARIABLES)
    claim_count = sum(row.get("claim_id") == "L-774" for row in claims_rows)
    variable_count = sum("4932_MTS" in row.get("symbol", "") for row in variable_rows)
    add_check(
        checks,
        "VAL4932_19_register_csv",
        "claims and variable registers parse with unique checkpoint identifiers",
        "L-774=1; 4932 variables=16",
        f"L-774={claim_count}; variables={variable_count}",
        claim_count == 1 and variable_count == 16,
    )

    register_requirements = {
        EQUATIONS: "## 1.225 Photon-graviton flow and MTS portal projection",
        RED_TEAM: "## 176. A real external portal fixed point is not automatic MTS inheritance",
        SPINE: "PPC4161_PHOTON_GRAVITON_FLOW_MTS_PROJECTION_4932",
        RESUME: "Last checkpoint: `4932-Y5-R2FR-MTS-gauge-portal-functional-trace-projection-or-two-sided-polarization-likelihood.md`",
    }
    register_missing = [f"{path.name}:{marker}" for path, marker in register_requirements.items() if marker not in read_text(path)]
    add_check(
        checks,
        "VAL4932_20_register_md",
        "equation, red-team, spine and resume registers are synchronized",
        "0 missing markers",
        str(register_missing),
        not register_missing,
    )

    next_target = "4933-Y5-R2FR-C3-CFF-F4-minimal-combined-natural-flow-and-0p239-stability-gate.md"
    next_target_ok = next_target in checkpoint_text and next_target in read_text(RESUME) and next_target in gate_rows.get("next_target", {}).get("decision", "")
    add_check(
        checks,
        "VAL4932_21_next_target",
        "checkpoint, resume and executable gate agree on the next target",
        next_target,
        f"checkpoint={next_target in checkpoint_text}; resume={next_target in read_text(RESUME)}; gate={gate_rows.get('next_target', {}).get('decision')}",
        next_target_ok,
    )

    pycache_paths = list((POST / "scripts").glob("__pycache__")) + list(SOURCE.rglob("__pycache__"))
    add_check(
        checks,
        "VAL4932_22_pycache",
        "checkpoint execution leaves no Python bytecode cache",
        "0 __pycache__ directories",
        str([str(path) for path in pycache_paths[:5]]),
        not pycache_paths,
    )

    output_path = OUTPUT / "P8_Y5_BRR545_4932_VALIDATION.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(checks[0]))
        writer.writeheader()
        writer.writerows(checks)

    passed_count = sum(bool(row["passed"]) for row in checks)
    print(f"P8_Y5_BRR545_4932_VALIDATION_{'PASS' if passed_count == len(checks) else 'FAIL'}")
    print(f"checks={passed_count}/{len(checks)}")
    for row in checks:
        if not row["passed"]:
            print(f"FAILED {row['validation_id']}: {row['actual']}")
    return 0 if passed_count == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())

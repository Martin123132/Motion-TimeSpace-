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
SOURCE = POST / "source-intake" / "functional_rg" / "4972"
RUNNER = POST / "scripts" / "Y5_R2FR_4972_C3_EAA_to_amplitude_matching.py"
NORMALIZATION = SOURCE / "C3_EAA_to_amplitude_normalization.csv"
ANCHORS = SOURCE / "C3_local_anchor_estimates.csv"
NONLOCAL = SOURCE / "C3_nonlocal_log_completion.csv"
IDENTIFIABILITY = SOURCE / "C3_finite_conversion_identifiability.csv"
HELICITIES = SOURCE / "C3_helicity_matching_predictions.csv"
RESULT = SOURCE / "C3_EAA_to_amplitude_matching_results.json"
CHECKPOINT = (
    POST
    / "4972-Y5-R2FR-C3-EAA-to-amplitude-tree-map-nonlocal-log-completion-and-finite-constant-isolation.md"
)
PROVENANCE = SOURCE / "PROVENANCE.md"
FORMAL_NOTE = FORMAL / "988-PPC4161-C3-EAA-amplitude-conversion-and-nonlocal-log-completion.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"
SPINE = POST / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"
CLAIMS = FORMAL / "02-claims-register.csv"
VARIABLES = FORMAL / "04-variable-audit.csv"
EQUATIONS = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
UNIFICATION = FORMAL / "07-unification-spine.md"
OUTPUT = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_4972_VALIDATION.csv"

MARKER = "MTS_4972_C3_EAA_TO_AMPLITUDE_MATCHING_VALIDATION"
FORMAL_MARKER = "PPC4161_C3_EAA_AMPLITUDE_CONVERSION_4972"
CHECKED_DATE = "2026-07-13"

EXPECTED_HASHES = {
    RUNNER: "ea624062862ef6b810318e6dc3edb79de893236346a323546f0cc9283c0dfee5",
    NORMALIZATION: "2d1d2b63795f89cb92847f2e76f7d076e9f6156ef6a6592ac687783947d61179",
    ANCHORS: "d260eaead4d2ebdab2d7fc9a9d6b75cc4fe395b42b364ab3916854f733e4ac61",
    NONLOCAL: "a044b3e12494b10ab24903f19ab5e40f412f06253fa4aefec020bc4faa2d9385",
    IDENTIFIABILITY: "5e2a9bbd25ee139e03a6792943cf69fd24f68915313c145a5b9b82372c56d7bf",
    HELICITIES: "eb96ac3f5a6fc9864355c655159513a13fcfd703a89bd4a15b554dfc074b072e",
    RESULT: "e150ec2b9424804ea50ad8a0258086e41436c8653e6214262160e1e2c593d4a1",
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
    return all(len(row) == expected_width for row in rows), len(rows) - 1


def validation_row(
    index: int,
    requirement: str,
    observed: str,
    detail: object,
    passed: bool,
) -> dict[str, Any]:
    return {
        "check_id": f"VAL4972_{index:02d}",
        "requirement": requirement,
        "observed": observed,
        "detail": json.dumps(detail, sort_keys=True, default=str),
        "passed": bool(passed),
        "checkpoint_marker": MARKER,
        "valid_for_full_MTS_claim": False,
        "source_checked_date": CHECKED_DATE,
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

    required_paths = [
        *EXPECTED_HASHES,
        CHECKPOINT,
        PROVENANCE,
        FORMAL_NOTE,
        RESUME,
        SPINE,
        CLAIMS,
        VARIABLES,
        EQUATIONS,
        RED_TEAM,
        UNIFICATION,
    ]
    missing = [str(path) for path in required_paths if not path.exists()]
    rows.append(
        validation_row(
            len(rows),
            "every 4972 executable, output, handoff and register exists",
            f"missing={len(missing)}",
            missing,
            not missing,
        )
    )

    hash_mismatches = {
        str(path): {"expected": expected, "actual": digest(path)}
        for path, expected in EXPECTED_HASHES.items()
        if path.exists() and digest(path) != expected
    }
    rows.append(
        validation_row(
            len(rows),
            "runner and all generated scientific outputs are hash locked",
            f"mismatches={len(hash_mismatches)}",
            hash_mismatches,
            not hash_mismatches,
        )
    )

    result = json.loads(RESULT.read_text(encoding="utf-8"))
    rows.append(
        validation_row(
            len(rows),
            "4972 runner passes every internal derivation check",
            f"all_checks_pass={result['all_checks_pass']}",
            result["checks"],
            result["all_checks_pass"] and not result["valid_for_full_MTS_claim"],
        )
    )

    normalization = read_csv(NORMALIZATION)
    normalization_results = {row["map_id"]: row["result"] for row in normalization}
    rows.append(
        validation_row(
            len(rows),
            "exact action chain contains the c and A tree maps",
            f"rows={len(normalization)}",
            normalization_results,
            len(normalization) == 5
            and normalization_results["MAP4972_02_TREE"]
            == "c_tree=c_R3=32*pi^3*r_C3"
            and normalization_results["MAP4972_03_BERN"]
            == "A_Bern_tree=-r_C3",
        )
    )

    anchors = read_csv(ANCHORS)
    current_anchors = [row for row in anchors if row["branch"].startswith("MTS_")]
    rows.append(
        validation_row(
            len(rows),
            "four MTS parent endpoints and two external comparators are emitted",
            f"total={len(anchors)}; mts={len(current_anchors)}",
            [row["branch"] for row in anchors],
            len(anchors) == 6 and len(current_anchors) == 4,
        )
    )

    current_c = [float(row["c_tree"]) for row in current_anchors]
    current_a = [float(row["A_Bern_tree"]) for row in current_anchors]
    rows.append(
        validation_row(
            len(rows),
            "current parent tree amplitude interval is finite and sign consistent",
            f"c=[{min(current_c)},{max(current_c)}]; A=[{min(current_a)},{max(current_a)}]",
            {},
            min(current_c) < max(current_c) < 0.0
            and 0.0 < min(current_a) < max(current_a),
        )
    )

    sm45_lambda = [
        float(row["lambda_over_mu_matching"])
        for row in anchors
        if row["branch"].startswith("MTS_SM45_")
        and not row["branch"].startswith("MTS_SM45_PLUS_MOTION")
    ]
    motion_lambda = [
        float(row["lambda_over_mu_matching"])
        for row in anchors
        if row["branch"].startswith("MTS_SM45_PLUS_MOTION")
    ]
    rows.append(
        validation_row(
            len(rows),
            "conditional local-EFT lambda intervals match the state-count branches",
            f"SM45={sm45_lambda}; motion={motion_lambda}",
            {},
            len(sm45_lambda) == 2
            and len(motion_lambda) == 2
            and 1.0906 < min(sm45_lambda) < max(sm45_lambda) < 1.0915
            and 1.0922 < min(motion_lambda) < max(motion_lambda) < 1.0931,
        )
    )

    rows.append(
        validation_row(
            len(rows),
            "every anchor row labels delta_c_fin zero as a prescription",
            f"rows={len(anchors)}",
            sorted({row["status"] for row in anchors}),
            all(
                float(row["delta_c_fin"]) == 0.0
                and "PRESCRIPTION" in row["status"]
                for row in anchors
            ),
        )
    )

    helicities = read_csv(HELICITIES)
    grouped: dict[str, dict[str, dict[str, str]]] = {}
    for row in helicities:
        grouped.setdefault(row["branch"], {})[row["helicity"]] = row
    ratio_ok = all(
        math.isclose(
            float(pair["++++"]["delta_remainder"]),
            10.0 * float(pair["-+++"]["delta_remainder"]),
            rel_tol=2e-15,
        )
        for pair in grouped.values()
    )
    rows.append(
        validation_row(
            len(rows),
            "all six branches pass the exact factor-ten helicity identity",
            f"branches={len(grouped)}; rows={len(helicities)}",
            {},
            len(grouped) == 6 and len(helicities) == 12 and ratio_ok,
        )
    )

    projected_ok = all(
        math.isclose(
            float(row["projected_A_Bern"]),
            -float(row["c_tree"]) / (32.0 * math.pi**3),
            rel_tol=2e-15,
            abs_tol=1e-18,
        )
        for row in helicities
    )
    rows.append(
        validation_row(
            len(rows),
            "both helicities independently recover A_Bern=-c/(32pi^3)",
            f"projected_ok={projected_ok}",
            {},
            projected_ok,
        )
    )

    nonlocal_rows = read_csv(NONLOCAL)
    closure_ok = all(
        math.isclose(
            float(row["d_c_local_d_ln_k"])
            + float(row["d_delta_c_nonlocal_d_ln_mu"]),
            float(row["d_c_physical_d_ln_mu"]),
            rel_tol=2e-15,
            abs_tol=1e-15,
        )
        for row in nonlocal_rows
    )
    rows.append(
        validation_row(
            len(rows),
            "derived nonlocal logarithm closes physical running in every endpoint row",
            f"rows={len(nonlocal_rows)}; closure={closure_ok}",
            {},
            len(nonlocal_rows) == 4 and closure_ok,
        )
    )

    sm45_q = [
        float(row["d_delta_c_nonlocal_d_ln_mu"])
        for row in nonlocal_rows
        if row["branch"] == "SM45"
    ]
    motion_q = [
        float(row["d_delta_c_nonlocal_d_ln_mu"])
        for row in nonlocal_rows
        if row["branch"] == "SM45_PLUS_MOTION"
    ]
    rows.append(
        validation_row(
            len(rows),
            "nonlocal slopes occupy the derived SM45 and motion intervals",
            f"SM45={sm45_q}; motion={motion_q}",
            {},
            len(sm45_q) == 2
            and len(motion_q) == 2
            and all(0.28649 < value < 0.28650 for value in sm45_q)
            and all(0.28232 < value < 0.28234 for value in motion_q),
        )
    )

    identifiability = {row["test_id"]: row for row in read_csv(IDENTIFIABILITY)}
    finite_test = identifiability["ID4972_00_TWO_HELICITY"]
    rows.append(
        validation_row(
            len(rows),
            "finite conversion no-go has rank one, nullity one and explicit null direction",
            f"rank={finite_test['matrix_rank']}; nullity={finite_test['nullity']}",
            finite_test["null_direction"],
            int(finite_test["matrix_rank"]) == 1
            and int(finite_test["nullity"]) == 1
            and "-32*pi^3" in finite_test["null_direction"],
        )
    )

    local_source_paths = {
        row["source"] for row in anchors if not row["source"].startswith("http")
    }
    absent_sources = [
        source for source in local_source_paths if not (ROOT / source).exists()
    ]
    rows.append(
        validation_row(
            len(rows),
            "every anchor source path exists locally",
            f"sources={len(local_source_paths)}; absent={len(absent_sources)}",
            absent_sources,
            not absent_sources,
        )
    )

    output_rows = normalization + anchors + nonlocal_rows + list(identifiability.values()) + helicities
    rows.append(
        validation_row(
            len(rows),
            "every scientific output remains private nonclaim",
            f"rows={len(output_rows)}",
            {},
            all(row["valid_for_full_MTS_claim"] == "False" for row in output_rows),
        )
    )

    missing_markers = [
        str(path)
        for path in (CHECKPOINT, PROVENANCE, FORMAL_NOTE, RESUME, SPINE, EQUATIONS, RED_TEAM, UNIFICATION)
        if FORMAL_MARKER not in path.read_text(encoding="utf-8")
    ]
    rows.append(
        validation_row(
            len(rows),
            "4972 formal marker propagates through all handoff documents",
            f"missing={len(missing_markers)}",
            missing_markers,
            not missing_markers,
        )
    )

    claims_rectangular, claims_count = rectangular_csv(CLAIMS, 13)
    claim_rows = read_csv(CLAIMS)
    claim_814 = [row for row in claim_rows if row["claim_id"] == "L-814"]
    rows.append(
        validation_row(
            len(rows),
            "claims register is rectangular and contains one L-814 row",
            f"rows={claims_count}; L-814={len(claim_814)}",
            {},
            claims_rectangular
            and len(claim_814) == 1
            and FORMAL_MARKER in claim_814[0]["notes"],
        )
    )

    variables_rectangular, variables_count = rectangular_csv(VARIABLES, 11)
    variable_rows = read_csv(VARIABLES)
    expected_symbols = {
        "r_C34972_MTS",
        "c_tree4972_MTS",
        "delta_c_fin4972",
        "q_NL4972_MTS",
        "lambda_local4972_MTS",
        "PredictivityStatus4972_MTS",
    }
    observed_symbols = {
        row["symbol"] for row in variable_rows if row["symbol"] in expected_symbols
    }
    rows.append(
        validation_row(
            len(rows),
            "variable audit is rectangular and contains all six 4972 symbols",
            f"rows={variables_count}; symbols={len(observed_symbols)}",
            sorted(observed_symbols),
            variables_rectangular and observed_symbols == expected_symbols,
        )
    )

    combined_outputs = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (NORMALIZATION, ANCHORS, NONLOCAL, IDENTIFIABILITY, HELICITIES, RESULT)
    )
    rows.append(
        validation_row(
            len(rows),
            "generated scientific outputs contain no missing-input sentinels",
            f"MISSING_ count={combined_outputs.count('MISSING_')}",
            {},
            "MISSING_" not in combined_outputs,
        )
    )

    resume_text = RESUME.read_text(encoding="utf-8")
    rows.append(
        validation_row(
            len(rows),
            "resume points to 4972 and prohibits another local-flow rerun",
            "4972 handoff present",
            {},
            "Last checkpoint: `4972-" in resume_text
            and "Do not repeat the local Wilson fit" in resume_text,
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

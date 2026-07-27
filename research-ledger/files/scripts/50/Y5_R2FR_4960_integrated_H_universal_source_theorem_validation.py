from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "4960"
OUTPUT = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_4960_VALIDATION.csv"

MAIN_SCRIPT = POST / "scripts" / "Y5_R2FR_4960_integrated_H_universal_source_theorem.py"
RESULT_JSON = SOURCE / "integrated_H_universal_source_results.json"
CONTRACT_CSV = SOURCE / "parent_definition_vs_derived_source_contract.csv"
H_SOURCE_CSV = SOURCE / "H_Hilbert_source_invertibility.csv"
UNIVERSALITY_CSV = SOURCE / "soft_Bianchi_species_coupling_nullspace.csv"
LOCAL_CHAIN_CSV = SOURCE / "local_limit_chain_and_calibrations.csv"
RESIDUAL_CSV = SOURCE / "local_residual_quarantine.csv"
DECISION_CSV = SOURCE / "universal_source_decision.csv"
PROVENANCE = SOURCE / "PROVENANCE.md"
CHECKPOINT = POST / "4960-Y5-R2FR-integrated-H-soft-BRST-universal-source-theorem-and-local-GR-Newton-Maxwell-promotion-or-parent-field-content-boundary.md"
FORMAL_NOTE = FORMAL / "976-PPC4161-integrated-H-universal-source-theorem-and-local-GR-boundary.md"

CLAIMS = FORMAL / "02-claims-register.csv"
VARIABLES = FORMAL / "04-variable-audit.csv"
EQUATIONS = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
SPINE = FORMAL / "07-unification-spine.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"
LOCAL_SPINE = POST / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

MARKER = "MTS_4960_INTEGRATED_H_UNIVERSAL_SOURCE_THEOREM"
FORMAL_MARKER = "PPC4161_INTEGRATED_H_UNIVERSAL_SOURCE_THEOREM_4960"

HASH_LOCKS = {
    MAIN_SCRIPT: "e08702bc5f10a58593d764b75fbdb91dfab052c8c6037339708cf3c23dc03e95",
    RESULT_JSON: "6fe2d8335cb1a4902c07c986e597e2f748050aa31f6137c5b52f9ced94542477",
    CONTRACT_CSV: "93937d1ed9b13eab2c9e13fdf45a98c2236d037759abbdbec77e8da96ec9ddaf",
    H_SOURCE_CSV: "7466bf1ac8e7c18d2a9957f15490307f4e78d926e786744c1d2e8e7910e073af",
    UNIVERSALITY_CSV: "ad714332cf51eccb8b271394715b8de27affe3baee21889223da74aeeee1ac51",
    LOCAL_CHAIN_CSV: "e4a7d3de99b2543b2e59b4fb47368e2357b179ca472b372822bfa3a2ca17a1ce",
    RESIDUAL_CSV: "db04d7caa6c17036e18eabcfa592648b95b451c97acfb411b41440bb539b1045",
    DECISION_CSV: "cbfb4a1a2d77450744e3275ed4ccea66b028f7d67502958f21c823e01f23d4bf",
    PROVENANCE: "513a29b7f5fd79bd8df8801215283c743a382fc1052036af4596b13e57abd711",
    CHECKPOINT: "6cd343d022dde751f86ad82eaf0f61fb5e3616753c228f631c44a45da278a69d",
    FORMAL_NOTE: "d8cac0e661fa60212f58a2525b86d6f2ea183c740e44376f21dfd1908365e7c1",
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
    add(checks, "VAL4960_01_paths", "all hash-locked paths exist", [], missing_paths, not missing_paths)

    bad_hashes = {
        str(path): {"expected": expected, "actual": digest(path)}
        for path, expected in HASH_LOCKS.items()
        if path.exists() and digest(path) != expected
    }
    add(checks, "VAL4960_02_hashes", "new research and documentation hashes match", {}, bad_hashes, not bad_hashes)

    compile_errors: list[str] = []
    for path in (MAIN_SCRIPT, Path(__file__).resolve()):
        try:
            compile(text(path), str(path), "exec")
        except Exception as error:
            compile_errors.append(f"{path.name}: {error}")
    add(checks, "VAL4960_03_compile", "research and validation scripts compile in memory", [], compile_errors, not compile_errors)

    result = json.loads(text(RESULT_JSON))
    add(checks, "VAL4960_04_marker", "result marker", MARKER, result.get("marker"), result.get("marker") == MARKER)
    failed_internal = [name for name, passed in result["checks"].items() if not passed]
    add(checks, "VAL4960_05_internal", "all research checks pass", [], failed_internal, not failed_internal)
    add(
        checks,
        "VAL4960_06_sources",
        "17 source hashes and all source clauses are present",
        {"hash_count": 17, "failed_clauses": []},
        {
            "hash_count": len(result["source_hashes"]),
            "failed_clauses": [
                name for name, passed in result["source_clause_checks"].items() if not passed
            ],
        },
        len(result["source_hashes"]) == 17
        and all(result["source_clause_checks"].values())
        and all(re.fullmatch(r"[0-9a-f]{64}", value) for value in result["source_hashes"].values()),
    )

    tables = {
        "contract": read_csv(CONTRACT_CSV),
        "H_source": read_csv(H_SOURCE_CSV),
        "universality": read_csv(UNIVERSALITY_CSV),
        "local_chain": read_csv(LOCAL_CHAIN_CSV),
        "residual": read_csv(RESIDUAL_CSV),
        "decision": read_csv(DECISION_CSV),
    }
    malformed = {
        f"{table_name}:{row_index}": row
        for table_name, rows in tables.items()
        for row_index, row in enumerate(rows)
        if None in row or any(value is None for value in row.values())
    }
    add(checks, "VAL4960_07_csv_shape", "all generated CSV rows parse without overflow", {}, malformed, not malformed)

    marker_errors = [
        f"{table_name}:{row_index}"
        for table_name, rows in tables.items()
        for row_index, row in enumerate(rows)
        if row.get("checkpoint_marker") != MARKER
        or truth(row.get("valid_for_full_MTS_claim", "False"))
    ]
    add(checks, "VAL4960_08_claim_flags", "all rows carry marker and full-MTS false", [], marker_errors, not marker_errors)

    contract_ids = {row["object_id"] for row in tables["contract"]}
    expected_contract_ids = {f"OWN4960_{index:02d}_{suffix}" for index, suffix in enumerate((
        "H", "Diff", "metric_map", "pole", "soft", "nonlinear", "matter_content", "matter_coefficient", "GN", "EM"
    ))}
    contract_parent_boundary = {
        row["object_id"]: row["ownership"] for row in tables["contract"]
    }
    add(
        checks,
        "VAL4960_09_contract",
        "ten exact parent-versus-derived ownership rows",
        sorted(expected_contract_ids),
        sorted(contract_ids),
        contract_ids == expected_contract_ids
        and contract_parent_boundary["OWN4960_00_H"] == "PARENT_FIELD_DEFINITION"
        and contract_parent_boundary["OWN4960_04_soft"] == "DERIVED_UNIVERSAL_COUPLING"
        and contract_parent_boundary["OWN4960_07_matter_coefficient"] == "NOT_AN_INDEPENDENT_PRIMITIVE_COEFFICIENT",
    )

    h_rows = {row["check_id"]: row for row in tables["H_source"]}
    expected_h_ids = {f"H4960_{index:02d}_{suffix}" for index, suffix in enumerate((
        "determinant", "inverse", "Jacobian", "source", "trace_reverse", "normalization", "Poynting"
    ))}
    add(
        checks,
        "VAL4960_10_H_map",
        "H map, source, trace reversal, normalization and Poynting checks",
        {"ids": sorted(expected_h_ids), "all_pass": True},
        {"ids": sorted(h_rows), "all_pass": all(truth(row["passed"]) for row in h_rows.values())},
        set(h_rows) == expected_h_ids
        and all(truth(row["passed"]) for row in h_rows.values())
        and h_rows["H4960_04_trace_reverse"]["matrix_rank"] == "10"
        and h_rows["H4960_04_trace_reverse"]["matrix_determinant"] == "-1",
    )

    universality_rows = {row["row_id"]: row for row in tables["universality"]}
    species_rows = [row for row in tables["universality"] if row.get("species") != "ALL"]
    common_row = universality_rows["UNI4960_07_common"]
    add(
        checks,
        "VAL4960_11_universality",
        "five source classes and one-dimensional common coupling kernel",
        {"species": 5, "rank": 4, "nullity": 1, "vector": "[[1, 1, 1, 1, 1]]"},
        {
            "species": len(species_rows),
            "rank": int(common_row["rank"]),
            "nullity": int(common_row["nullity"]),
            "vector": common_row["null_vector"],
        },
        len(species_rows) == 5
        and len(universality_rows) == 8
        and all(truth(row["passed"]) for row in tables["universality"])
        and common_row["rank"] == "4"
        and common_row["nullity"] == "1"
        and common_row["null_vector"] == "[[1, 1, 1, 1, 1]]",
    )

    local_counts = Counter(row["row_type"] for row in tables["local_chain"])
    expected_local_counts = {
        "source_chain": 14,
        "limit_gate": 10,
        "calibration": 9,
        "arena_transfer": 5,
    }
    arena_rows = [row for row in tables["local_chain"] if row["row_type"] == "arena_transfer"]
    token_columns = ("same_GN_token", "same_alphaEM_token", "same_Jgap_token", "same_cIR_token")
    token_sets = {column: {row[column] for row in arena_rows} for column in token_columns}
    add(
        checks,
        "VAL4960_12_local_chain",
        "complete 4947 chain and universal arena tokens",
        {"counts": expected_local_counts, "token_set_sizes": {column: 1 for column in token_columns}},
        {"counts": dict(local_counts), "token_set_sizes": {column: len(values) for column, values in token_sets.items()}},
        dict(local_counts) == expected_local_counts
        and all(truth(row["passed"]) for row in tables["local_chain"])
        and all(len(values) == 1 for values in token_sets.values())
        and all(row["arena_retuning_allowed"].lower() == "false" for row in arena_rows),
    )

    diagnostics = result["local_chain_diagnostics"]
    expected_support_counts = {
        "matter_rule_count": 10,
        "fifth_force_gate_count": 7,
        "Maxwell_certificate_count": 9,
        "local_residual_vector_count": 5,
    }
    actual_support_counts = {key: diagnostics[key] for key in expected_support_counts}
    add(
        checks,
        "VAL4960_13_supporting_gates",
        "PPN, scalar-source and Maxwell support tables remain passed",
        {**expected_support_counts, "supporting_pass": True},
        {**actual_support_counts, "supporting_pass": diagnostics["supporting_PPN_scalar_Maxwell_gates_pass"]},
        actual_support_counts == expected_support_counts
        and diagnostics["supporting_PPN_scalar_Maxwell_gates_pass"],
    )

    residual_rows = {row["residual_id"]: row for row in tables["residual"]}
    expected_residual_ids = {f"RES4960_{index:02d}_{suffix}" for index, suffix in enumerate((
        "scalar_source", "curvature_Higgs", "R2_C2", "C3", "CFF", "preferred_flow", "hidden_visible_reentry", "strong_EP", "matter_ontology", "scalar_only_graviton"
    ))}
    add(
        checks,
        "VAL4960_14_residuals",
        "ten residual classes retain zero, bound, conditional or open status",
        sorted(expected_residual_ids),
        sorted(residual_rows),
        set(residual_rows) == expected_residual_ids
        and residual_rows["RES4960_00_scalar_source"]["declared_local_status"].startswith("EXACT_ZERO")
        and residual_rows["RES4960_03_C3"]["declared_local_status"].startswith("NONZERO_RETAINED")
        and residual_rows["RES4960_04_CFF"]["declared_local_status"].endswith("OPEN")
        and not truth(residual_rows["RES4960_07_strong_EP"]["leading_weak_local_controlled"])
        and residual_rows["RES4960_08_matter_ontology"]["declared_local_status"] == "EXPLICIT_PARENT_CONTENT_NOT_MOTION_DERIVED",
    )

    decision_rows = {row["decision_id"]: row for row in tables["decision"]}
    local_promotion = decision_rows["DEC4960_04_local_promotion"]
    motion_origin = decision_rows["DEC4960_05_motion_origin"]
    strong_field = decision_rows["DEC4960_06_strong_field"]
    full_mts = decision_rows["DEC4960_07_full_MTS"]
    add(
        checks,
        "VAL4960_15_decision",
        "local theorem promoted while parent-origin, strong-field and full-MTS claims remain false",
        {"local": True, "motion_origin": False, "strong": False, "full_MTS": False},
        {
            "local": truth(local_promotion["claim_granted"]),
            "motion_origin": truth(motion_origin["claim_granted"]),
            "strong": truth(strong_field["claim_granted"]),
            "full_MTS": truth(full_mts["claim_granted"]),
        },
        len(decision_rows) == 8
        and all(truth(row["passed"]) for row in decision_rows.values())
        and truth(local_promotion["claim_granted"])
        and not truth(motion_origin["claim_granted"])
        and not truth(strong_field["claim_granted"])
        and not truth(full_mts["claim_granted"]),
    )

    provenance = text(PROVENANCE)
    primary_urls = (
        "10.1103/PhysRev.135.B1049",
        "10.1103/PhysRev.138.B988",
        "10.1007/BF00759198",
        "gr-qc/0411023",
        "0370-2693(80)90212-9",
    )
    add(
        checks,
        "VAL4960_16_provenance",
        "all primary theorem sources and nonclaim boundary recorded",
        list(primary_urls),
        [url for url in primary_urls if url in provenance],
        all(url in provenance for url in primary_urls)
        and "valid_for_full_MTS_claim=false" in provenance,
    )

    checkpoint_text = text(CHECKPOINT)
    checkpoint_clauses = (
        MARKER,
        "the soft theorem is the universality proof",
        "visible matter ontology",
        "strong compact-body GR",
        "full MTS                                          = false",
        "No GitHub action is authorized",
    )
    add(
        checks,
        "VAL4960_17_checkpoint",
        "checkpoint states theorem and all claim boundaries",
        list(checkpoint_clauses),
        [clause for clause in checkpoint_clauses if clause in checkpoint_text],
        all(clause in checkpoint_text for clause in checkpoint_clauses),
    )

    claims_rows = read_csv(CLAIMS)
    variable_rows = read_csv(VARIABLES)
    malformed_register_rows = [
        f"{table_name}:{row_index}"
        for table_name, rows in (("claims", claims_rows), ("variables", variable_rows))
        for row_index, row in enumerate(rows)
        if None in row or any(value is None for value in row.values())
    ]
    claim_matches = [row for row in claims_rows if row.get("claim_id") == "L-802"]
    expected_variables = {
        "IntegratedHSourceMap4960_MTS",
        "TraceReversalInvolution4960_MTS",
        "SoftSpeciesCouplingKernel4960_MTS",
        "BianchiExchangeKernel4960_MTS",
        "NormalizationInvariantMetricResidue4960_MTS",
        "LocalUniversalSourcePromotion4960_MTS",
        "ParentFieldContentBoundary4960_MTS",
        "PredictivityStatus4960_MTS",
    }
    actual_variables = {row.get("symbol") for row in variable_rows} & expected_variables
    add(
        checks,
        "VAL4960_18_registers",
        "claim L-802 and eight variable rows parse exactly once",
        {"claim_count": 1, "variables": sorted(expected_variables)},
        {
            "claim_count": len(claim_matches),
            "variables": sorted(actual_variables),
            "malformed": malformed_register_rows,
        },
        len(claim_matches) == 1
        and actual_variables == expected_variables
        and not malformed_register_rows,
    )

    register_markers = {
        "formal_note": FORMAL_MARKER in text(FORMAL_NOTE),
        "equation": "## 1.253 Integrated-H universal source theorem" in text(EQUATIONS),
        "red_team": "## 204. A derived universal coefficient is not a derived ontology" in text(RED_TEAM),
        "spine": FORMAL_MARKER in text(SPINE),
        "resume": FORMAL_MARKER in text(RESUME),
        "local_spine": "Current State Through 4960" in text(LOCAL_SPINE),
    }
    add(checks, "VAL4960_19_formal_sync", "formal notes and current handoffs are synchronized", {key: True for key in register_markers}, register_markers, all(register_markers.values()))

    pycache_paths = [str(path) for path in (POST / "scripts").rglob("__pycache__")]
    add(checks, "VAL4960_20_pycache", "no scripts __pycache__ remains", [], pycache_paths, not pycache_paths)

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
        print(f"{MARKER}_VALIDATION_FAILURES={','.join(failed_checks)}", flush=True)
        return 1
    print(f"{MARKER}_VALIDATION_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import shutil
import sys
import time
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5250"
RESIDUALS = POST / "source-intake" / "mts_residuals"

MANIFEST_5241 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5241"
    / "decay_angle_order9_manifest.json"
)
RESULT_5241 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5241"
    / "decay_angle_order9_result.json"
)
NODE_ROWS_5241 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5241"
    / "decay_angle_order9_node_summary.csv"
)
RESULT_5247 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5247"
    / "Q03_corrected_inner_slice_result.json"
)
EXTRAPOLATION_5247 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5247"
    / "Q03_corrected_regulator_extrapolation.csv"
)
VALIDATION_5247 = (
    RESIDUALS / "P8_Y5_BRR545_5247_VALIDATION.csv"
)
RESULT_5249 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5249"
    / "Q05_corrected_inner_slice_result.json"
)
EXTRAPOLATION_5249 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5249"
    / "Q05_corrected_regulator_extrapolation.csv"
)
VALIDATION_5249 = (
    RESIDUALS / "P8_Y5_BRR545_5249_VALIDATION.csv"
)

MANIFEST = SOURCE / "partial_outer_impact_manifest.json"
DRY_RUN = SOURCE / "partial_outer_impact_dry_run.json"
RESULT = SOURCE / "partial_outer_impact_result.json"
NODE_IMPACT_ROWS = SOURCE / "Q03_Q05_weighted_outer_impact.csv"
SUMMARY_ROWS = SOURCE / "partial_outer_impact_summary.csv"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5250_VALIDATION.csv"
DOCUMENT = (
    POST
    / "5250-Y5-R2FR-Q03-Q05-partial-outer-impact-and-remaining-node-gate.md"
)

MARKER = "MTS_5250_Q03_Q05_PARTIAL_OUTER_IMPACT_REMAINING_NODE_GATE"
REVISION = "Q03-Q05-partial-outer-impact-remaining-node-gate-v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
CORRECTED_NODE_IDS = ("Q03", "Q05")
ORDER5_BACKBONE_IDS = ("Q00", "Q02", "Q04", "Q06", "Q08")
REMAINING_ORDER9_IDS = ("Q01", "Q07")
MAXIMUM_RECONSTRUCTION_RESIDUAL = 2.0e-12
MAXIMUM_RUNTIME_SECONDS = 30.0 * 60.0


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for item in sorted(
        candidate for candidate in path.rglob("*")
        if candidate.is_file()
    ):
        value.update(
            str(item.relative_to(path)).replace("\\", "/").encode()
        )
        value.update(digest(item).encode())
    return value.hexdigest()


def serialized_hash(value: Any) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    temporary.replace(path)


def atomic_json(path: Path, value: Any) -> None:
    atomic_text(path, json.dumps(value, indent=2, sort_keys=True) + "\n")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        atomic_text(path, "")
        return
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def source_rows() -> list[dict[str, str]]:
    paths = (
        MANIFEST_5241,
        RESULT_5241,
        NODE_ROWS_5241,
        RESULT_5247,
        EXTRAPOLATION_5247,
        VALIDATION_5247,
        RESULT_5249,
        EXTRAPOLATION_5249,
        VALIDATION_5249,
    )
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in paths
    ]


def physical_values(path: Path) -> dict[int, complex]:
    rows = [
        row
        for row in read_csv(path)
        if row["row_type"] == "PHYSICAL_RICHARDSON_SLICE"
    ]
    return {
        int(row["quadrature_order"]): complex(
            float(row["subtracted_integral_real"]),
            float(row["subtracted_integral_imaginary"]),
        )
        for row in rows
    }


def fixed_node_values() -> dict[str, dict[int, complex]]:
    result: dict[str, dict[int, complex]] = {}
    for row in read_csv(NODE_ROWS_5241):
        result[row["order9_node_id"]] = {
            order: complex(
                float(row[f"order{order}_subtracted_real"]),
                float(row[f"order{order}_subtracted_imaginary"]),
            )
            for order in (128, 512)
        }
    return result


def prepare() -> tuple[dict[str, Any], dict[str, Any]]:
    result_5247 = read_json(RESULT_5247)
    result_5249 = read_json(RESULT_5249)
    manifest_5241 = read_json(MANIFEST_5241)
    rules = [
        row
        for row in manifest_5241["outer_rule_rows"]
        if int(row["outer_rule_order"]) == 9
    ]
    manifest = {
        "marker": MARKER,
        "revision": REVISION,
        "parent_checkpoints": [5247, 5249],
        "corrected_node_ids": list(CORRECTED_NODE_IDS),
        "order5_backbone_ids": list(ORDER5_BACKBONE_IDS),
        "remaining_order9_ids": list(REMAINING_ORDER9_IDS),
        "outer_rule_order": 9,
        "outer_rule_rows": rules,
        "source_files": source_rows(),
        "claim_boundary": {
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "The reported hybrid changes only Q03 and Q05. Seven "
                "outer nodes still use inherited topology."
            ),
        },
    }
    manifest["manifest_hash"] = serialized_hash(manifest)
    checks = {
        "source_paths_exist_and_match": all(
            Path(row["path"]).exists()
            and digest(Path(row["path"])) == row["sha256"]
            for row in manifest["source_files"]
        ),
        "Q03_parent_passed": (
            result_5247["integrity_passed"]
            and result_5247["acceptance_passed"]
        ),
        "Q05_parent_passed": (
            result_5249["integrity_passed"]
            and result_5249["acceptance_passed"]
        ),
        "order9_rule_has_nine_nodes": (
            len(rules) == 9
            and {row["order9_node_id"] for row in rules}
            == {f"Q{index:02d}" for index in range(9)}
        ),
        "corrected_nodes_are_order9_only_additions": all(
            node_id
            not in {
                row["order9_node_id"]
                for row in manifest_5241["outer_rule_rows"]
                if int(row["outer_rule_order"]) == 5
            }
            for node_id in CORRECTED_NODE_IDS
        ),
        "formal_digest_unchanged": (
            tree_digest(FORMAL) == FORMAL_BASELINE
        ),
        "claims_locked_false": all(
            not bool(manifest["claim_boundary"][field])
            for field in (
                "valid_for_numeric_UV_claim",
                "valid_for_local_GR_claim",
                "valid_for_full_MTS_claim",
            )
        ),
    }
    dry_run = {
        "marker": MARKER,
        "revision": REVISION,
        "dry_run_passed": all(checks.values()),
        "checks": checks,
        "manifest_hash": manifest["manifest_hash"],
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    return manifest, dry_run


def validation_rows(
    manifest: dict[str, Any],
    summary: dict[str, Any],
    formal_digest: str,
    elapsed: float,
) -> list[dict[str, Any]]:
    definitions = [
        (
            "integrity",
            "SOURCE_PATHS_EXIST_AND_MATCH",
            all(
                Path(row["path"]).exists()
                and digest(Path(row["path"])) == row["sha256"]
                for row in manifest["source_files"]
            ),
            len(manifest["source_files"]),
            "all source paths and hashes",
        ),
        (
            "acceptance",
            "FIXED_ORDER9_RECONSTRUCTED",
            summary["fixed_reconstruction_residual"]
            <= MAXIMUM_RECONSTRUCTION_RESIDUAL,
            summary["fixed_reconstruction_residual"],
            MAXIMUM_RECONSTRUCTION_RESIDUAL,
        ),
        (
            "acceptance",
            "HYBRID_ORDER9_ALGEBRA_CLOSES",
            summary["hybrid_algebra_residual"]
            <= MAXIMUM_RECONSTRUCTION_RESIDUAL,
            summary["hybrid_algebra_residual"],
            MAXIMUM_RECONSTRUCTION_RESIDUAL,
        ),
        (
            "acceptance",
            "HYBRID_INNER_128_TO_512_FINITE",
            math.isfinite(
                summary[
                    "hybrid_inner128_to512_relative_difference"
                ]
            ),
            summary[
                "hybrid_inner128_to512_relative_difference"
            ],
            "finite diagnostic",
        ),
        (
            "acceptance",
            "SEVEN_REMAINING_NODES_EXPLICIT",
            len(ORDER5_BACKBONE_IDS)
            + len(REMAINING_ORDER9_IDS)
            == 7,
            "|".join(
                [*ORDER5_BACKBONE_IDS, *REMAINING_ORDER9_IDS]
            ),
            "seven inherited nodes",
        ),
        (
            "integrity",
            "FORMALIZATION_WORKBENCH_UNCHANGED",
            formal_digest == FORMAL_BASELINE,
            formal_digest,
            FORMAL_BASELINE,
        ),
        (
            "integrity",
            "RUNTIME_BOUNDED",
            elapsed <= MAXIMUM_RUNTIME_SECONDS,
            elapsed,
            MAXIMUM_RUNTIME_SECONDS,
        ),
        (
            "integrity",
            "CLAIMS_REMAIN_FALSE",
            all(
                not bool(manifest["claim_boundary"][field])
                for field in (
                    "valid_for_numeric_UV_claim",
                    "valid_for_local_GR_claim",
                    "valid_for_full_MTS_claim",
                )
            ),
            "false,false,false",
            "false,false,false",
        ),
    ]
    return [
        {
            "checkpoint": 5250,
            "gate_kind": kind,
            "gate": gate,
            "passed": passed,
            "observed": observed,
            "required": required,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
        for kind, gate, passed, observed, required in definitions
    ]


def render_document(
    summary: dict[str, Any],
    validations: list[dict[str, Any]],
    elapsed: float,
) -> str:
    integrity_passed = all(
        bool(row["passed"])
        for row in validations
        if row["gate_kind"] == "integrity"
    )
    acceptance_passed = all(
        bool(row["passed"])
        for row in validations
        if row["gate_kind"] == "acceptance"
    )
    decision = (
        "INVALID_Q03_Q05_PARTIAL_OUTER_IMPACT"
        if not integrity_passed
        else (
            "HOLD_HYBRID_OUTER_VALUE__"
            "REBUILD_ORDER5_BACKBONE_WITH_PAIRED_TRANSPORT"
            if acceptance_passed
            else "HOLD_PARTIAL_OUTER_IMPACT_PENDING_FAILED_GATE"
        )
    )
    return "\n".join(
        [
            "# 5250 — Q03/Q05 partial outer impact and remaining-node gate",
            "",
            "## Exact partial update",
            "",
            (
                "The locked order-9 rule is reconstructed from all nine "
                "5241 node values. Only Q03 and Q05 are then replaced by "
                "their accepted 5247/5249 values. This hybrid is an impact "
                "diagnostic, not a corrected cubature."
            ),
            "",
            "## Results",
            "",
            (
                "- Fixed order-9 value: "
                f"`{summary['fixed_order9_value']}`."
            ),
            (
                "- Q03 weighted correction: "
                f"`{summary['Q03_weighted_correction']}`."
            ),
            (
                "- Q05 weighted correction: "
                f"`{summary['Q05_weighted_correction']}`."
            ),
            (
                "- Two-node weighted correction: "
                f"`{summary['combined_weighted_correction']}`."
            ),
            (
                "- Hybrid order-9 value: "
                f"`{summary['hybrid_order9_value']}`."
            ),
            (
                "- Relative hybrid shift: "
                f"`{summary['relative_hybrid_shift']:.12g}`."
            ),
            (
                "- Fixed versus hybrid order5/order9 differences: "
                f"`{summary['fixed_order5_to_order9_relative_difference']:.12g}`, "
                f"`{summary['hybrid_order5_to_order9_relative_difference']:.12g}`."
            ),
            f"- Runtime: `{elapsed:.3f} s`.",
            "",
            "## Decision",
            "",
            f"`{decision}`",
            "",
            "## Interpretation",
            "",
            (
                "The two corrected order-9-only nodes move the weighted "
                "sum by about twenty percent and make the comparison with "
                "the inherited order-5 value worse. That is not a failure "
                "of the paired correction: the order-5 baseline itself "
                "still contains five independently transported legacy "
                "maps, so mixing corrected and uncorrected nodes is not a "
                "valid convergence test."
            ),
            "",
            "## Claim boundary",
            "",
            (
                "The hybrid value must not be quoted as the corrected "
                "coefficient. Q00, Q02, Q04, Q06, Q08, Q01, and Q07 remain "
                "on inherited topology."
            ),
            "",
            "## Next exact target",
            "",
            (
                "Rebuild the nested order-5 backbone Q00/Q02/Q04/Q06/Q08 "
                "with the reciprocal-projective tracker first. This gives "
                "a like-for-like corrected order-5 baseline before Q01 "
                "and Q07 complete the corrected order-9 rule."
            ),
            "",
        ]
    )


def remove_project_pycache() -> None:
    target = POST / "scripts" / "__pycache__"
    if target.exists():
        shutil.rmtree(target)


def execute() -> dict[str, Any]:
    started = time.perf_counter()
    manifest, dry_run = prepare()
    atomic_json(MANIFEST, manifest)
    atomic_json(DRY_RUN, dry_run)
    if not dry_run["dry_run_passed"]:
        failed = [
            key
            for key, passed in dry_run["checks"].items()
            if not passed
        ]
        raise RuntimeError(f"5250 dry run failed: {failed}")

    fixed_nodes = fixed_node_values()
    corrected_nodes = {
        "Q03": physical_values(EXTRAPOLATION_5247),
        "Q05": physical_values(EXTRAPOLATION_5249),
    }
    rules = manifest["outer_rule_rows"]
    weights = {
        row["order9_node_id"]: float(
            row["weight_d_decay_cosine"]
        )
        for row in rules
    }
    fixed_outer: dict[int, complex] = {}
    hybrid_outer: dict[int, complex] = {}
    impact_rows: list[dict[str, Any]] = []
    for order in (128, 512):
        fixed_outer[order] = 0.25 * sum(
            (
                weights[node_id] * fixed_nodes[node_id][order]
                for node_id in weights
            ),
            0.0j,
        )
        hybrid_outer[order] = 0.25 * sum(
            (
                weights[node_id]
                * (
                    corrected_nodes[node_id][order]
                    if node_id in corrected_nodes
                    else fixed_nodes[node_id][order]
                )
                for node_id in weights
            ),
            0.0j,
        )
    for node_id in sorted(weights):
        fixed = fixed_nodes[node_id][512]
        corrected = (
            corrected_nodes[node_id][512]
            if node_id in corrected_nodes
            else fixed
        )
        delta = corrected - fixed
        weighted = 0.25 * weights[node_id] * delta
        impact_rows.append(
            {
                "order9_node_id": node_id,
                "weight_d_decay_cosine": weights[node_id],
                "angular_unit_cube_jacobian": 0.25,
                "correction_applied": node_id in corrected_nodes,
                "fixed_real": fixed.real,
                "fixed_imaginary": fixed.imag,
                "replacement_real": corrected.real,
                "replacement_imaginary": corrected.imag,
                "node_delta_real": delta.real,
                "node_delta_imaginary": delta.imag,
                "weighted_delta_real": weighted.real,
                "weighted_delta_imaginary": weighted.imag,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    result_5241 = read_json(RESULT_5241)
    reported_fixed = complex(
        float(result_5241["cubature_values"]["9"]["real"]),
        float(result_5241["cubature_values"]["9"]["imaginary"]),
    )
    order5 = complex(
        float(result_5241["cubature_values"]["5"]["real"]),
        float(result_5241["cubature_values"]["5"]["imaginary"]),
    )
    combined = hybrid_outer[512] - fixed_outer[512]
    weighted_by_node = {
        row["order9_node_id"]: complex(
            float(row["weighted_delta_real"]),
            float(row["weighted_delta_imaginary"]),
        )
        for row in impact_rows
    }
    summary = {
        "fixed_order9_value": str(fixed_outer[512]),
        "hybrid_order9_value": str(hybrid_outer[512]),
        "Q03_weighted_correction": str(weighted_by_node["Q03"]),
        "Q05_weighted_correction": str(weighted_by_node["Q05"]),
        "combined_weighted_correction": str(combined),
        "relative_hybrid_shift": abs(combined)
        / max(abs(fixed_outer[512]), 1.0),
        "fixed_order5_to_order9_relative_difference": (
            abs(order5 - fixed_outer[512])
            / max(abs(fixed_outer[512]), 1.0)
        ),
        "hybrid_order5_to_order9_relative_difference": (
            abs(order5 - hybrid_outer[512])
            / max(abs(hybrid_outer[512]), 1.0)
        ),
        "hybrid_inner128_to512_relative_difference": (
            abs(hybrid_outer[128] - hybrid_outer[512])
            / max(abs(hybrid_outer[512]), 1.0)
        ),
        "fixed_reconstruction_residual": abs(
            fixed_outer[512] - reported_fixed
        ),
        "hybrid_algebra_residual": abs(
            hybrid_outer[512]
            - fixed_outer[512]
            - weighted_by_node["Q03"]
            - weighted_by_node["Q05"]
        ),
        "remaining_node_ids": "|".join(
            [*ORDER5_BACKBONE_IDS, *REMAINING_ORDER9_IDS]
        ),
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    formal_digest = tree_digest(FORMAL)
    elapsed = time.perf_counter() - started
    validations = validation_rows(
        manifest, summary, formal_digest, elapsed
    )
    write_csv(NODE_IMPACT_ROWS, impact_rows)
    write_csv(SUMMARY_ROWS, [summary])
    write_csv(VALIDATION, validations)
    atomic_text(
        DOCUMENT,
        render_document(summary, validations, elapsed),
    )
    integrity_passed = all(
        bool(row["passed"])
        for row in validations
        if row["gate_kind"] == "integrity"
    )
    acceptance_passed = all(
        bool(row["passed"])
        for row in validations
        if row["gate_kind"] == "acceptance"
    )
    decision = (
        "INVALID_Q03_Q05_PARTIAL_OUTER_IMPACT"
        if not integrity_passed
        else (
            "HOLD_HYBRID_OUTER_VALUE__"
            "REBUILD_ORDER5_BACKBONE_WITH_PAIRED_TRANSPORT"
            if acceptance_passed
            else "HOLD_PARTIAL_OUTER_IMPACT_PENDING_FAILED_GATE"
        )
    )
    result = {
        "marker": MARKER,
        "revision": REVISION,
        "dry_run": dry_run,
        "manifest_hash": manifest["manifest_hash"],
        "decision": decision,
        "integrity_passed": integrity_passed,
        "acceptance_passed": acceptance_passed,
        "summary": summary,
        "formalization_workbench_digest": formal_digest,
        "elapsed_seconds": elapsed,
        "outputs": [
            str(path)
            for path in (
                MANIFEST,
                DRY_RUN,
                NODE_IMPACT_ROWS,
                SUMMARY_ROWS,
                VALIDATION,
                DOCUMENT,
            )
        ],
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT, result)
    remove_project_pycache()
    if not integrity_passed:
        failed = [
            row["gate"]
            for row in validations
            if row["gate_kind"] == "integrity"
            and not row["passed"]
        ]
        raise RuntimeError(f"5250 integrity validation failed: {failed}")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="validate the partial outer-impact manifest only",
    )
    arguments = parser.parse_args()
    if arguments.dry_run:
        manifest, dry_run = prepare()
        atomic_json(MANIFEST, manifest)
        atomic_json(DRY_RUN, dry_run)
        print(json.dumps(dry_run, indent=2, sort_keys=True))
        return
    print(json.dumps(execute(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

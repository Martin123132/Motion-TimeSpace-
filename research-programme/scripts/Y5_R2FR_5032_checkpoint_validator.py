from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5032"
RESIDUALS = POST / "source-intake" / "mts_residuals"
DOCUMENT = (
    POST
    / "5032-Y5-R2FR-projective-causal-topology-grid-and-corrected-event-kernel.md"
)
PROVENANCE = SOURCE / "PROVENANCE.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"
GRID = SOURCE / "multi_event_causal_topology_grid.json"
RESULT = SOURCE / "causal_topology_grid_validation.json"
GATE_CSV = SOURCE / "causal_topology_grid_gate.csv"
INTEGRALS = (
    SOURCE / "corrected_baseline_integral_global24_orders128_192.json",
    SOURCE / "corrected_baseline_integral_global32_orders128_192.json",
)
SCRIPTS = (
    POST / "scripts" / "Y5_R2FR_5030_causal_relative_collision_homotopy_gate.py",
    POST / "scripts" / "Y5_R2FR_5032_multi_event_causal_topology_grid.py",
    POST / "scripts" / "Y5_R2FR_5032_multi_event_causal_topology_validation.py",
    Path(__file__).resolve(),
)
OUTPUT = RESIDUALS / "P8_Y5_BRR545_5032_VALIDATION.csv"
MARKER = "MTS_5032_PROJECTIVE_CAUSAL_TOPOLOGY_GRID_GATE"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        value.update(item.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(item).encode("ascii"))
    return value.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def check_rows() -> list[tuple[str, bool, str]]:
    grid = load_json(GRID)
    result = load_json(RESULT)
    integral_documents = [load_json(path) for path in INTEGRALS]
    provenance_text = PROVENANCE.read_text(encoding="utf-8")
    cited_paths = [
        ROOT / value
        for value in re.findall(r"`(post-checkpoint-work/[^`]+)`", provenance_text)
    ]
    event_names = {
        row["output_file"] for row in grid["grid_rows"]
    } | {
        row["output_file"] for row in grid["refinement_rows"]
    }
    event_documents = [
        load_json(SOURCE / "events" / name) for name in sorted(event_names)
    ]
    with GATE_CSV.open(newline="", encoding="utf-8") as handle:
        gate_rows = list(csv.DictReader(handle))
    formal_digest = tree_digest(FORMAL)
    resume_text = RESUME.read_text(encoding="utf-8")
    document_text = DOCUMENT.read_text(encoding="utf-8")
    authoritative_paths = (
        DOCUMENT,
        PROVENANCE,
        RESUME,
        GRID,
        RESULT,
        GATE_CSV,
        *INTEGRALS,
        *SCRIPTS,
    )
    return [
        (
            "scripts_ast_parse",
            all(ast.parse(path.read_text(encoding="utf-8")) is not None for path in SCRIPTS),
            "all four 5030/5032 scripts parse cleanly",
        ),
        (
            "provenance_paths_exist",
            bool(cited_paths) and all(path.exists() for path in cited_paths),
            f"all {len(cited_paths)} cited local provenance paths exist",
        ),
        (
            "authoritative_json_parse",
            len(event_documents) == len(event_names),
            f"grid, validation, integrals, and {len(event_documents)} event outputs parse",
        ),
        (
            "nine_event_grid",
            grid["grid_event_count"] == 9 and len(grid["grid_rows"]) == 9,
            "nine deterministic finite-x events present",
        ),
        (
            "eight_topology_classes",
            grid["topology_class_count"] == 8,
            "eight net-winding classes with E01/E02 shared",
        ),
        (
            "projective_tracking",
            result["topology_gate_passed"]
            and result["maximum_grid_projective_step"] < 0.1
            and result["maximum_required_refinement_projective_step"] < 0.1,
            (
                f"max base={result['maximum_grid_projective_step']}; "
                f"refinement={result['maximum_required_refinement_projective_step']}"
            ),
        ),
        (
            "regulator_and_step_refinement",
            result["regulator_limit_refinement_passed"]
            and result["step_refinement_passed"],
            "all eight representatives pass epsilon/10 and step doubling",
        ),
        (
            "canonical_path_nontrivial",
            result["canonical_path_prescription_nontrivial"],
            (
                f"alternative paths match {result['path_diagnostic_match_count']}/"
                f"{result['path_diagnostic_total']} diagnostics"
            ),
        ),
        (
            "corrected_baseline_integral",
            result["corrected_fixed_event_integral_gate_passed"],
            result["reported_corrected_fixed_event_value"],
        ),
        (
            "integral_convergence",
            result["maximum_relative_order_residual"] < 2.0e-4
            and result["global_relative_difference"] < 1.0e-3
            and all(
                document["fixed_event_crossed_integral_converged"]
                for document in integral_documents
            ),
            (
                f"relative={result['maximum_relative_order_residual']}; "
                f"global={result['global_relative_difference']}"
            ),
        ),
        (
            "5031_superseded",
            result["checkpoint_5031_superseded"]
            and "superseded" in document_text.lower(),
            (
                f"crossings {result['superseded_5031_crossing_counts']} -> "
                f"{result['corrected_crossing_counts_by_chamber']}"
            ),
        ),
        (
            "claim_boundary",
            result["claim_boundary_passed"]
            and not result["outer_phase_space_integration_complete"]
            and not result["full_coupled_cut_bridge_complete"]
            and not result["valid_for_full_MTS_claim"],
            "outer integral, full cut, and full MTS remain false",
        ),
        (
            "gate_csv_semantics",
            len(gate_rows) == 8
            and all(row["passed"] == "True" for row in gate_rows[:6])
            and all(row["passed"] == "False" for row in gate_rows[6:]),
            "six completed gates pass and two explicit claim boundaries remain false",
        ),
        (
            "resume_marker",
            MARKER in resume_text and "four wall-clock hours" in resume_text,
            "5032 marker and four-hour runtime boundary present",
        ),
        (
            "no_missing_markers",
            all(
                "MISSING_" not in path.read_text(encoding="utf-8", errors="ignore")
                for path in (
                    DOCUMENT,
                    PROVENANCE,
                    RESUME,
                    GRID,
                    RESULT,
                    GATE_CSV,
                    *INTEGRALS,
                )
            ),
            "no placeholder marker in authoritative checkpoint files",
        ),
        (
            "formalization_unchanged",
            formal_digest == FORMAL_BASELINE,
            formal_digest,
        ),
        (
            "pycache_removed",
            not any(path.is_dir() for path in POST.rglob("__pycache__")),
            "no __pycache__ directory under post-checkpoint-work",
        ),
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    rows = check_rows()
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    with arguments.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("check_id", "passed", "detail", "checkpoint_marker"),
        )
        writer.writeheader()
        for index, (name, passed, detail) in enumerate(rows, start=1):
            writer.writerow(
                {
                    "check_id": f"V5032_{index:02d}_{name}",
                    "passed": passed,
                    "detail": detail,
                    "checkpoint_marker": MARKER,
                }
            )
    failed = [name for name, passed, _ in rows if not passed]
    print(
        json.dumps(
            {
                "checkpoint_marker": MARKER,
                "check_count": len(rows),
                "failed": failed,
                "passed": not failed,
                "output": str(arguments.output),
            },
            indent=2,
        )
    )
    if failed:
        raise RuntimeError(f"checkpoint 5032 validation failed: {failed}")


if __name__ == "__main__":
    main()

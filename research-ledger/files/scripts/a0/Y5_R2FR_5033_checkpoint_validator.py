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
SOURCE = POST / "source-intake" / "functional_rg" / "5033"
RESIDUALS = POST / "source-intake" / "mts_residuals"
DOCUMENT = POST / "5033-Y5-R2FR-representative-topology-class-kernel-matrix.md"
PROVENANCE = SOURCE / "PROVENANCE.md"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"
MATRIX = SOURCE / "representative_class_kernel_matrix.json"
GATE_CSV = SOURCE / "representative_class_kernel_gate.csv"
KERNEL_DIRECTORY = SOURCE / "kernels"
SCRIPTS = (
    POST / "scripts" / "Y5_R2FR_5026_finite_x_global_pole_transport_smoke.py",
    POST / "scripts" / "Y5_R2FR_5028_finite_x_relative_chamber_transport_event.py",
    POST / "scripts" / "Y5_R2FR_5030_causal_relative_collision_homotopy_gate.py",
    POST / "scripts" / "Y5_R2FR_5032_multi_event_causal_topology_grid.py",
    POST / "scripts" / "Y5_R2FR_5033_representative_class_kernel_matrix.py",
    Path(__file__).resolve(),
)
OUTPUT = RESIDUALS / "P8_Y5_BRR545_5033_VALIDATION.csv"
MARKER = "MTS_5033_REPRESENTATIVE_CLASS_KERNEL_MATRIX_GATE"
GLOBAL_REVISION = "conditioned-subminimum-annulus-v5"
RESIDUE_REVISION = "pair-local-double-residue-adaptive-v3"
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


def kernel_path(value: str) -> Path:
    candidate = Path(value)
    if candidate.exists():
        return candidate
    return KERNEL_DIRECTORY / candidate.name


def check_rows() -> list[tuple[str, bool, str]]:
    matrix = load_json(MATRIX)
    class_rows = matrix["class_rows"]
    kernel_paths = [
        kernel_path(row[key])
        for row in class_rows
        for key in ("global24_output", "global32_output")
    ]
    kernel_documents = [load_json(path) for path in kernel_paths]
    high_documents = kernel_documents[1::2]
    high_catalog = [
        residue
        for document in high_documents
        for chamber in document["fixed_event_integral_gate"]["chambers"]
        for residue in chamber["residue_catalog"]
    ]
    order_rows = [
        document["fixed_event_integral_gate"]["order_rows"][-1]
        for document in kernel_documents
    ]
    with GATE_CSV.open(newline="", encoding="utf-8") as handle:
        gate_rows = list(csv.DictReader(handle))
    provenance_text = PROVENANCE.read_text(encoding="utf-8")
    cited_paths = [
        ROOT / value
        for value in re.findall(r"`(post-checkpoint-work/[^`]+)`", provenance_text)
    ]
    document_text = DOCUMENT.read_text(encoding="utf-8")
    resume_text = RESUME.read_text(encoding="utf-8")
    formal_digest = tree_digest(FORMAL)
    c4 = next(row for row in class_rows if row["class_id"] == "C4")
    c6_documents = [
        document
        for document in kernel_documents
        if document["topology_class_id"] == "C6"
    ]
    checkpoint_outputs = (
        DOCUMENT,
        PROVENANCE,
        MATRIX,
        GATE_CSV,
        *kernel_paths,
    )
    return [
        (
            "scripts_ast_parse",
            all(ast.parse(path.read_text(encoding="utf-8")) is not None for path in SCRIPTS),
            "all six causal-kernel scripts parse cleanly",
        ),
        (
            "provenance_paths_exist",
            bool(cited_paths)
            and all(
                path.exists() or path.resolve() == OUTPUT.resolve()
                for path in cited_paths
            ),
            f"all {len(cited_paths)} cited local paths exist",
        ),
        (
            "authoritative_outputs_parse",
            len(kernel_documents) == 16 and all(path.exists() for path in kernel_paths),
            "matrix, gate CSV, and sixteen kernel documents parse",
        ),
        (
            "eight_class_matrix",
            matrix["representative_class_count"] == 8
            and len(class_rows) == 8
            and not matrix["failed_class_ids"]
            and matrix["all_representative_class_kernels_passed"]
            and matrix["representative_class_kernel_matrix_complete"],
            "all eight topology-class representatives pass",
        ),
        (
            "numerical_revisions",
            all(
                document["fixed_event_integral_gate"]["global_cycle_revision"]
                == GLOBAL_REVISION
                and document["fixed_event_integral_gate"]["relative_residue_revision"]
                == RESIDUE_REVISION
                for document in kernel_documents
            ),
            f"{GLOBAL_REVISION}; {RESIDUE_REVISION}",
        ),
        (
            "pair_local_residues",
            len(high_catalog) == 190
            and all(row["stable"] for row in high_catalog)
            and all(row["residue_method"] == RESIDUE_REVISION for row in high_catalog),
            f"{len(high_catalog)} high-tier residues, all stable",
        ),
        (
            "adaptive_contour_retry",
            all(row["residue_contour_fraction"] in (0.1, 0.2) for row in high_catalog)
            and sum(row["residue_contour_fraction"] == 0.2 for row in high_catalog) == 1,
            "one of 190 residues requires the bounded wider contour",
        ),
        (
            "adaptive_quadrature",
            all(row["adaptive_quadrature_converged"] for row in order_rows)
            and all(document["fixed_event_crossed_integral_converged"] for document in kernel_documents),
            "all sixteen tier calculations converge",
        ),
        (
            "class_convergence",
            max(row["global_relative_difference"] for row in class_rows) < 1.0e-3
            and max(row["maximum_relative_order_residual"] for row in class_rows) < 2.0e-4
            and max(row["correction_relative_scale"] for row in class_rows) < 1.0e-6,
            (
                f"global={max(row['global_relative_difference'] for row in class_rows)}; "
                f"relative={max(row['maximum_relative_order_residual'] for row in class_rows)}"
            ),
        ),
        (
            "c4_double_residue_regression",
            c4["class_kernel_gate_passed"]
            and c4["correction_relative_scale"] < 1.0e-10
            and c4["all_residues_stable"],
            f"C4 correction tier scale={c4['correction_relative_scale']}",
        ),
        (
            "c6_adaptive_regression",
            all(
                document["fixed_event_integral_gate"]["order_rows"][-1][
                    "composite_interval_count"
                ]
                < 128
                for document in c6_documents
            ),
            "C6 no longer reaches the 1024-interval cap",
        ),
        (
            "5032_numerical_supersession",
            "superseded" in document_text.lower() and "topology remains authoritative" in document_text,
            "5032 topology retained and baseline numerical value superseded",
        ),
        (
            "gate_csv_semantics",
            len(gate_rows) == 10
            and all(row["passed"] == "True" for row in gate_rows[:8])
            and all(row["passed"] == "False" for row in gate_rows[8:]),
            "eight class gates pass; outer and full-MTS boundaries remain false",
        ),
        (
            "claim_boundary",
            not matrix["outer_phase_space_integration_complete"]
            and not matrix["full_coupled_cut_bridge_complete"]
            and not matrix["valid_for_full_MTS_claim"]
            and all(not document["valid_for_full_MTS_claim"] for document in kernel_documents),
            "outer integral, complete cut, and full MTS are not claimed",
        ),
        (
            "resume_marker",
            MARKER in resume_text and "four wall-clock hours" in resume_text,
            "5033 handoff and runtime boundary present",
        ),
        (
            "no_missing_markers",
            all(
                "MISSING_" not in path.read_text(encoding="utf-8", errors="ignore")
                for path in checkpoint_outputs
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
                    "check_id": f"V5033_{index:02d}_{name}",
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
        raise RuntimeError(f"checkpoint 5033 validation failed: {failed}")


if __name__ == "__main__":
    main()

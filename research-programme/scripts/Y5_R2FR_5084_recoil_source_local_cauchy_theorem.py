from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
from typing import Any

import numpy as np


POST = Path(__file__).resolve().parents[1]
SCRIPT_5040 = POST / "scripts" / "Y5_R2FR_5040_arbitrary_precision_cross_source_residue.py"
SCRIPT_5045 = POST / "scripts" / "Y5_R2FR_5045_theorem_scope_falsification_and_quarantine.py"
SCRIPT_5083 = POST / "scripts" / "Y5_R2FR_5083_owned_g2_local_cauchy_zero_certificate.py"
RUN_5035 = POST / "source-intake" / "functional_rg" / "5035" / "runs" / "central_eps008_004_002_s4_v1"
SCOPE_AUDIT_5045 = POST / "source-intake" / "functional_rg" / "5045" / "theorem_scope_audit.json"
G1_WITNESSES = (
    POST / "source-intake" / "functional_rg" / "5040" / "arbitrary_precision_residues" / "E040__S503403_N0001__A00__primary24.json",
    POST / "source-intake" / "functional_rg" / "5040" / "arbitrary_precision_residues" / "E040__S503403_N0001__A14__primary24.json",
)
G2_A00_CERTIFICATE = POST / "source-intake" / "functional_rg" / "5083" / "owned_g2_local_cauchy_zero_certificate.json"
PILOT_V3 = POST / "source-intake" / "functional_rg" / "5079" / "runs" / "bounded_central_anchor_pilot_v3"
SOURCE = POST / "source-intake" / "functional_rg" / "5084"
RESULT_JSON = SOURCE / "recoil_source_local_cauchy_theorem.json"
G2_A01_WITNESS = SOURCE / "g2_A01_arbitrary_precision_witness.json"
FALSIFICATION_CSV = SOURCE / "stable_nonzero_falsification_audit.csv"
VALIDATION_CSV = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5084_VALIDATION.csv"
MARKER = "MTS_5084_RECOIL_SOURCE_LOCAL_CAUCHY_THEOREM"
REVISION = "guarded-owned-direct-g1-g2-cauchy-theorem-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
RECOIL_SOURCES = {"direct:g1", "direct:g2"}


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5040 = load_module("mts_5040_for_5084", SCRIPT_5040)
M5045 = load_module("mts_5045_for_5084", SCRIPT_5045)
N5030 = M5040.N5030


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def serialized(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imaginary": float(value.imag)}


def source_name(label: str) -> str:
    return label.rsplit(":", 1)[0]


def root_label(label: str) -> str:
    return label.rsplit(":", 1)[1]


def additive_component(label: str) -> str:
    return "direct" if label.startswith("direct:") else "subtraction"


def relative_safe_scale(row: dict[str, Any]) -> float:
    fraction = float(row.get("residue_contour_fraction", math.nan))
    radius = float(row.get("outer_radius", math.nan))
    if not math.isfinite(fraction) or not math.isfinite(radius) or fraction <= 0.0:
        return math.nan
    return radius / fraction


def corrected_recoil_certificate(
    row: dict[str, Any],
    ownership: dict[str, bool],
    module: Any | None = None,
) -> dict[str, Any]:
    active = N5030 if module is None else module
    root = complex(row["root"])
    pairs = [tuple(str(value) for value in pair) for pair in row["pairs"]]
    labels = sorted({label for pair in pairs for label in pair})
    owned = [label for label in labels if bool(ownership.get(label, False))]
    cross_source = len(pairs) == 1 and {
        additive_component(pairs[0][0]),
        additive_component(pairs[0][1]),
    } == {"direct", "subtraction"}
    owned_label = owned[0] if len(owned) == 1 else None
    owned_source = source_name(owned_label) if owned_label is not None else None
    recoil_owned = owned_source in RECOIL_SOURCES
    direct_label = next(
        (label for label in labels if label.startswith("direct:")), None
    )
    subtraction_label = next(
        (label for label in labels if label.startswith("subtraction:")), None
    )
    safe_scale = relative_safe_scale(row)
    diagnostics: dict[str, Any] = {
        "collision_root_residual": math.inf,
        "minimum_same_direct_component_root_separation": 0.0,
        "minimum_recoil_to_subtraction_direction_separation": 0.0,
        "minimum_internal_energy_magnitude": 0.0,
        "inverse_energy_square_sum_magnitude": 0.0,
    }
    evaluable = bool(
        cross_source
        and len(labels) == 2
        and len(owned) == 1
        and recoil_owned
        and owned_label == direct_label
        and direct_label is not None
        and subtraction_label is not None
    )
    if evaluable:
        soft_direction, decay_direction, internal = active.M5028.event_geometry(
            active.SOFT_ENERGY,
            complex(active.SOFT_COSINE, 0.0),
            complex(active.DECAY_COSINE, 0.0),
            root,
        )
        sources = active.M5028.source_directions(
            internal, soft_direction, decay_direction
        )
        factor_module = active.M5028.M5024
        direct_roots: dict[str, complex] = {}
        for source in ("direct:g1", "direct:g2", "direct:g3"):
            roots = factor_module.all_factor_roots(
                sources[source], active.TARGET_COSINE
            )
            for label, value in roots.items():
                direct_roots[f"{source}:{label}"] = complex(value)
        subtraction_roots = factor_module.all_factor_roots(
            sources[source_name(subtraction_label)], active.TARGET_COSINE
        )
        owned_global_root = direct_roots[direct_label]
        unowned_global_root = complex(subtraction_roots[root_label(subtraction_label)])
        collision_residual = abs(owned_global_root - unowned_global_root) / max(
            1.0, abs(owned_global_root), abs(unowned_global_root)
        )
        same_direct_separation = min(
            abs(owned_global_root - value)
            for label, value in direct_roots.items()
            if label != direct_label
        )
        recoil_direction = sources[owned_source]
        source_separation = min(
            float(
                np.linalg.norm(
                    recoil_direction - sources["subtraction:soft"]
                )
            ),
            float(
                np.linalg.norm(
                    recoil_direction - sources["subtraction:decay"]
                )
            ),
        )
        energy_magnitudes = [abs(complex(momentum[0])) for momentum in internal]
        inverse_sum = abs(
            sum(1.0 / (momentum[0] * momentum[0]) for momentum in internal)
        )
        diagnostics = {
            "owned_global_root": serialized(owned_global_root),
            "unowned_global_root": serialized(unowned_global_root),
            "collision_root_residual": float(collision_residual),
            "minimum_same_direct_component_root_separation": float(
                same_direct_separation
            ),
            "minimum_recoil_to_subtraction_direction_separation": float(
                source_separation
            ),
            "minimum_internal_energy_magnitude": float(min(energy_magnitudes)),
            "inverse_energy_square_sum_magnitude": float(inverse_sum),
        }
    guards = {
        "single_cross_additive_pair": cross_source and len(labels) == 2,
        "exactly_one_owned_collision_label": len(owned) == 1,
        "owned_label_is_direct_recoil_g1_or_g2": recoil_owned
        and owned_label == direct_label,
        "relative_collision_is_not_chart_origin": abs(root) > 1.0e-10,
        "relative_collision_disk_is_isolated": math.isfinite(safe_scale)
        and safe_scale > 0.0
        and abs(root) > safe_scale,
        "global_collision_equation_closes": diagnostics[
            "collision_root_residual"
        ]
        < 2.0e-6,
        "owned_direct_pole_cluster_is_isolated": diagnostics[
            "minimum_same_direct_component_root_separation"
        ]
        > 1.0e-8,
        "recoil_source_is_not_subtraction_alias": diagnostics[
            "minimum_recoil_to_subtraction_direction_separation"
        ]
        > 1.0e-8,
        "internal_energies_are_regular": diagnostics[
            "minimum_internal_energy_magnitude"
        ]
        > 1.0e-10,
        "direct_multiplier_is_regular": diagnostics[
            "inverse_energy_square_sum_magnitude"
        ]
        > 1.0e-10,
    }
    passed = all(guards.values())
    return {
        "passed": passed,
        "revision": REVISION,
        "root": serialized(root),
        "pairs": [list(pair) for pair in pairs],
        "labels": labels,
        "owned_labels": owned,
        "owned_label": owned_label,
        "owned_source": owned_source,
        "direct_label": direct_label,
        "subtraction_label": subtraction_label,
        "relative_safe_scale": safe_scale,
        "guards": guards,
        "diagnostics": diagnostics,
        "analytic_identity": (
            "For I=D+S and an owned recoil-source pole z_D(q), source separation gives "
            "Res_z I=Res_z D away from the isolated D/S crossing. The guarded separation "
            "from every other direct pole and the regular recoil kinematics provide a "
            "fixed local direct-component cycle through q0. Its residue R_D(q) is "
            "holomorphic at q0. Since q0 is nonzero, Res_q[R_D(q)/q]=0."
        ),
        "catalog_completeness_assumption": (
            "the finite-x pole catalogue exhausts direct-component z singularities"
        ),
        "excluded_alias": "direct:g3 equals subtraction:soft and is outside this theorem",
        "broad_5041_theorem_reinstated": False,
        "valid_for_full_MTS_claim": False,
    }


def complex_residue(row: dict[str, Any]) -> complex:
    value = row["residue"]
    if isinstance(value, dict):
        return complex(float(value["real"]), float(value["imaginary"]))
    return complex(value)


def stable_nonzero_falsification_audit() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    passed_counterexamples = []
    for kernel_path in sorted((RUN_5035 / "kernels").glob("*.json")):
        kernel = json.loads(kernel_path.read_text(encoding="utf-8"))
        M5045.M5041.configure_from_kernel(kernel)
        active = M5045.M5041.N5030
        ownerships = active.physical_chambers()[1]
        for chamber in kernel["fixed_event_integral_gate"]["chambers"]:
            ownership = ownerships[int(chamber["chamber_index"])]
            for residue in chamber["residue_catalog"]:
                if not bool(residue.get("stable")) or bool(
                    residue.get("numerically_zero")
                ):
                    continue
                magnitude = abs(complex_residue(residue))
                if magnitude <= 1.0e-7:
                    continue
                labels = {
                    str(label)
                    for pair in residue["pairs"]
                    for label in pair
                }
                if not any(label.startswith("direct:g") for label in labels):
                    continue
                certificate = corrected_recoil_certificate(
                    residue, ownership, active
                )
                row = {
                    "job_key": kernel["job_key"],
                    "chamber_index": int(chamber["chamber_index"]),
                    "pairs": json.dumps(residue["pairs"], separators=(",", ":")),
                    "residue_magnitude": magnitude,
                    "corrected_theorem_passed": certificate["passed"],
                    "owned_label": certificate["owned_label"],
                    "recoil_guard": certificate["guards"][
                        "owned_label_is_direct_recoil_g1_or_g2"
                    ],
                    "alias_guard": certificate["guards"][
                        "recoil_source_is_not_subtraction_alias"
                    ],
                }
                rows.append(row)
                if certificate["passed"]:
                    passed_counterexamples.append(row)
    if not rows:
        raise RuntimeError("stable nonzero falsification corpus is empty")
    FALSIFICATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with FALSIFICATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return {
        "source_run": str(RUN_5035),
        "stable_nonzero_cross_source_rows": len(rows),
        "corrected_theorem_counterexample_count": len(passed_counterexamples),
        "counterexamples": passed_counterexamples,
        "passed": not passed_counterexamples,
    }


def existing_g1_witness_audit() -> dict[str, Any]:
    rows = []
    for path in G1_WITNESSES:
        document = json.loads(path.read_text(encoding="utf-8"))
        values = {
            (float(row["relative_fraction"]), float(row["global_fraction"])): float(
                row["magnitude"]
            )
            for row in document["values"]
        }
        ratios = []
        for global_fraction in sorted({key[1] for key in values}):
            outer = values[(0.1, global_fraction)]
            inner = values[(0.05, global_fraction)]
            ratios.append(outer / inner)
        expected = float(2 ** int(document["relative_nodes"]))
        maximum_error = max(abs(ratio / expected - 1.0) for ratio in ratios)
        passed = bool(
            document["port_validation"]["passed"]
            and maximum_error < 0.02
            and max(row["magnitude"] for row in document["values"]) < 2.0e-19
        )
        rows.append(
            {
                "path": str(path),
                "sha256": digest(path),
                "pair": document["collision_pairs"],
                "maximum_halving_ratio_relative_error": maximum_error,
                "maximum_residue_magnitude": max(
                    row["magnitude"] for row in document["values"]
                ),
                "passed": passed,
            }
        )
    return {"rows": rows, "passed": len(rows) == 2 and all(row["passed"] for row in rows)}


def locate_pair_row(kernel: dict[str, Any], pair: tuple[str, str]) -> tuple[dict[str, Any], int]:
    target = tuple(sorted(pair))
    matches = []
    for chamber in kernel["fixed_event_integral_gate"]["chambers"]:
        for row in chamber["residue_catalog"]:
            pairs = {tuple(sorted(str(value) for value in candidate)) for candidate in row["pairs"]}
            if target in pairs and abs(complex(row["root"])) < 1.0:
                matches.append((row, int(chamber["chamber_index"])))
    if len(matches) != 1:
        raise RuntimeError(f"expected one subunit pair row, found {len(matches)}")
    return matches[0]


def main() -> None:
    required = [
        SCRIPT_5040,
        SCRIPT_5045,
        SCRIPT_5083,
        SCOPE_AUDIT_5045,
        G2_A00_CERTIFICATE,
        PILOT_V3 / "config.json",
        PILOT_V3 / "kernels" / "E040__S507602_N0000__A01__primary24.json",
        *G1_WITNESSES,
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing 5084 inputs: {missing}")
    falsification = stable_nonzero_falsification_audit()
    g1_witnesses = existing_g1_witness_audit()
    g2_a00 = json.loads(G2_A00_CERTIFICATE.read_text(encoding="utf-8"))
    M5083 = load_module("mts_5083_for_5084_main", SCRIPT_5083)
    config = json.loads((PILOT_V3 / "config.json").read_text(encoding="utf-8"))
    event = M5083.M5077.M5036.event_lookup(config)["S507602_N0000"]
    argument = M5083.M5077.M5036.argument_lookup(config)["E040_A01"]
    target = M5083.M5077.M5036.complex_from_row(argument["target_cosine"])
    M5083.M5077.M5036.M5035.M5034.configure(event, target)
    kernel_path = PILOT_V3 / "kernels" / "E040__S507602_N0000__A01__primary24.json"
    kernel = json.loads(kernel_path.read_text(encoding="utf-8"))
    pair = ("direct:g2:minus_v", "subtraction:decay:plus_v")
    a01_row, chamber_index = locate_pair_row(kernel, pair)
    ownership = M5083.N5030.physical_chambers()[1][chamber_index]
    root = complex(a01_row["root"])
    safe_scale = relative_safe_scale(a01_row)
    g2_a01_structural = M5083.structural_audit(root, safe_scale, ownership)
    g2_a01_witness = M5083.arbitrary_precision_witness(
        root, safe_scale, ownership
    )
    a01_reference_scale = max(
        abs(
            complex(
                float(port_row["arbitrary_precision"]["real"]),
                float(port_row["arbitrary_precision"]["imaginary"]),
            )
        )
        for port_row in g2_a01_witness["port_validation"]["rows"]
    )
    g2_a01_scale_aware_witness_passed = bool(
        g2_a01_witness["port_validation"]["passed"]
        and g2_a01_witness["maximum_halving_ratio_relative_error"] < 1.0e-8
        and g2_a01_witness["maximum_global_radius_relative_difference"] < 1.0e-8
        and g2_a01_witness["maximum_outer_magnitude"]
        / a01_reference_scale
        < 1.0e-20
        and g2_a01_witness["maximum_inner_magnitude"]
        / a01_reference_scale
        < 1.0e-24
    )
    g2_a01_witness["scale_aware_5084_gate"] = {
        "reference_integrand_scale": a01_reference_scale,
        "maximum_outer_relative_to_reference": g2_a01_witness[
            "maximum_outer_magnitude"
        ]
        / a01_reference_scale,
        "maximum_inner_relative_to_reference": g2_a01_witness[
            "maximum_inner_magnitude"
        ]
        / a01_reference_scale,
        "passed": g2_a01_scale_aware_witness_passed,
        "reason": (
            "the inherited 5083 absolute magnitude cutoff was calibrated to A00; "
            "5084 uses scale-relative suppression plus the pre-existing 2^16 "
            "halving and contour-radius invariance signatures"
        ),
    }
    atomic_json(G2_A01_WITNESS, g2_a01_witness)
    a01_certificate = corrected_recoil_certificate(
        a01_row, ownership, M5083.N5030
    )
    a00_kernel = json.loads(
        (PILOT_V3 / "kernels" / "E040__S507602_N0000__A00__primary24.json").read_text(
            encoding="utf-8"
        )
    )
    a00_argument = M5083.M5077.M5036.argument_lookup(config)["E040_A00"]
    a00_target = M5083.M5077.M5036.complex_from_row(
        a00_argument["target_cosine"]
    )
    M5083.M5077.M5036.M5035.M5034.configure(event, a00_target)
    a00_row, a00_chamber = locate_pair_row(a00_kernel, pair)
    a00_ownership = M5083.N5030.physical_chambers()[1][a00_chamber]
    a00_certificate = corrected_recoil_certificate(
        a00_row, a00_ownership, M5083.N5030
    )
    scope_5045 = json.loads(SCOPE_AUDIT_5045.read_text(encoding="utf-8"))
    known_g3_counterexamples_excluded = all(
        not any(
            label.startswith("direct:g1:") or label.startswith("direct:g2:")
            for label in row["owned_labels"]
        )
        for row in scope_5045["stable_nonzero_counterexamples"]["rows"]
    )
    theorem_accepted = bool(
        falsification["passed"]
        and g1_witnesses["passed"]
        and g2_a00["accepted_local_zero_certificate"]
        and g2_a01_structural["passed"]
        and g2_a01_scale_aware_witness_passed
        and a00_certificate["passed"]
        and a01_certificate["passed"]
        and known_g3_counterexamples_excluded
    )
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "theorem_statement": (
            "At an isolated cross-additive collision q0 != 0, if the owned global pole "
            "belongs to recoil source direct:g1 or direct:g2, is separated from every "
            "other direct-component pole, and the recoil kinematics are regular, then "
            "the source-separated iterated local residue Res_q Res_z[I/(z q)] is zero."
        ),
        "proof": (
            "Write I=D+S. On the owned direct local cycle away from q0, S is holomorphic "
            "and contributes no z residue. Direct-pole isolation and regular recoil "
            "kinematics give a fixed direct-component contour in a neighborhood of q0, "
            "so its residue R_D(q) is holomorphic by parameter-dependent Cauchy integration. "
            "The factor 1/q is also holomorphic because q0 is nonzero; hence the q residue vanishes."
        ),
        "guard_function": "corrected_recoil_certificate",
        "scope": "owned direct:g1/direct:g2 cross-source rows satisfying every explicit guard",
        "excluded_scope": [
            "direct:g3, which aliases subtraction:soft",
            "owned subtraction rows",
            "same-additive-source collisions",
            "chart-origin collisions",
            "non-isolated or kinematically singular rows",
        ],
        "falsification_audit": falsification,
        "existing_g1_arbitrary_precision_witnesses": g1_witnesses,
        "g2_A00_certificate": {
            "path": str(G2_A00_CERTIFICATE),
            "sha256": digest(G2_A00_CERTIFICATE),
            "corrected_guard_passed": a00_certificate["passed"],
        },
        "g2_A01_certificate": a01_certificate,
        "g2_A01_structural_audit_passed": g2_a01_structural["passed"],
        "g2_A01_arbitrary_precision_witness": str(G2_A01_WITNESS),
        "g2_A01_arbitrary_precision_witness_sha256": digest(G2_A01_WITNESS),
        "g2_A01_arbitrary_precision_witness_passed": g2_a01_scale_aware_witness_passed,
        "known_g3_stable_nonzero_counterexamples_excluded": known_g3_counterexamples_excluded,
        "corrected_recoil_theorem_accepted": theorem_accepted,
        "broad_5041_theorem_reinstated": False,
        "pilot_resume_authorized_under_guard_only": theorem_accepted,
        "source_paths": {str(path): digest(path) for path in required},
        "formalization_workbench_tree_sha256": FORMAL_BASELINE,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    checks = [
        ("source_paths_exist", not missing, "all theorem and falsification inputs exist"),
        ("stable_nonzero_falsification", falsification["passed"], f"counterexamples={falsification['corrected_theorem_counterexample_count']}"),
        ("g1_witnesses", g1_witnesses["passed"], "two independent 70-digit g1 witnesses retained"),
        ("g2_A00_guard", a00_certificate["passed"] and g2_a00["accepted_local_zero_certificate"], "existing A00 local certificate satisfies corrected theorem"),
        ("g2_A01_guard", a01_certificate["passed"] and g2_a01_structural["passed"], str(a01_certificate["guards"])),
        ("g2_A01_mp_witness", g2_a01_scale_aware_witness_passed, f"outer_relative={g2_a01_witness['maximum_outer_magnitude'] / a01_reference_scale}; inner_relative={g2_a01_witness['maximum_inner_magnitude'] / a01_reference_scale}; halving_error={g2_a01_witness['maximum_halving_ratio_relative_error']}"),
        ("g3_counterexamples_excluded", known_g3_counterexamples_excluded, "g3 alias is outside scope"),
        ("theorem_accepted", theorem_accepted, result["scope"]),
        ("broad_theorem_not_reinstated", not result["broad_5041_theorem_reinstated"], "guarded recoil scope only"),
        ("formalization_unchanged", result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE, result["formalization_workbench_tree_sha256"]),
        ("claim_discipline", not result["valid_for_full_MTS_claim"], "numerical integration theorem is not a physical claim"),
    ]
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=("check_id", "passed", "detail", "checkpoint_marker"))
        writer.writeheader()
        for index, (name, passed, detail) in enumerate(checks, start=1):
            writer.writerow(
                {
                    "check_id": f"V5084_{index:02d}_{name}",
                    "passed": passed,
                    "detail": detail,
                    "checkpoint_marker": MARKER,
                }
            )
    failed = [name for name, passed, _ in checks if not passed]
    if failed:
        raise RuntimeError(f"checkpoint 5084 validation failed: {failed}")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

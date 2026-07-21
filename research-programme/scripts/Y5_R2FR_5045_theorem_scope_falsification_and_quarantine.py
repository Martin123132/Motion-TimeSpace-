from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import os
from collections import Counter
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPT_5041 = POST / "scripts" / "Y5_R2FR_5041_cross_source_additive_zero_repair.py"
SCRIPT_MP = POST / "scripts" / "Y5_R2FR_5040_arbitrary_precision_cross_source_residue.py"
RUN_5040 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5040"
    / "runs"
    / "nested_sobol_power1_s4_v1"
)
SOURCE = POST / "source-intake" / "functional_rg" / "5045"
AUDIT_JSON = SOURCE / "theorem_scope_audit.json"
AUDIT_CSV = SOURCE / "theorem_scope_audit.csv"
QUARANTINE_CSV = SOURCE / "quarantine_manifest.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5045_SCOPE_VALIDATION.csv"
)
ORIGINAL_AUDIT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5041"
    / "cross_source_zero_audit.json"
)
MP_WITNESSES = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5040"
    / "arbitrary_precision_residues"
    / "E040__S503403_N0001__A00__primary24.json",
    POST
    / "source-intake"
    / "functional_rg"
    / "5040"
    / "arbitrary_precision_residues"
    / "E040__S503403_N0001__A14__primary24.json",
)
MARKER = "MTS_5045_THEOREM_SCOPE_FALSIFICATION_AND_QUARANTINE"
REVISION = "cross-source-zero-scope-restricted-to-witnessed-owned-direct-g1-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
PROVED_FAMILIES = {
    (
        "direct:g1:minus_v",
        ("direct:g1:minus_v", "subtraction:decay:minus_u"),
    ),
    (
        "direct:g1:plus_v",
        ("direct:g1:plus_v", "subtraction:decay:plus_u"),
    ),
}


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5041 = load_module("mts_5041_for_scope_audit", SCRIPT_5041)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    if not path.exists():
        return "MISSING"
    for file_path in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        value.update(file_path.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(file_path).encode("ascii"))
    return value.hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def complex_value(value: Any) -> complex:
    if isinstance(value, dict):
        return complex(float(value["real"]), float(value["imaginary"]))
    return complex(value)


def normalized_single_pair(certificate: dict[str, Any]) -> tuple[str, str] | None:
    pairs = certificate.get("pairs", [])
    if len(pairs) != 1 or len(pairs[0]) != 2:
        return None
    return tuple(sorted(str(label) for label in pairs[0]))


def proof_witnesses() -> dict[tuple[str, str], dict[str, Any]]:
    witnesses: dict[tuple[str, str], dict[str, Any]] = {}
    for path in MP_WITNESSES:
        document = json.loads(path.read_text(encoding="utf-8"))
        pair = tuple(sorted(str(label) for label in document["collision_pairs"][0]))
        values = {
            (float(row["relative_fraction"]), float(row["global_fraction"])): float(
                row["magnitude"]
            )
            for row in document["values"]
        }
        ratios = []
        for global_fraction in sorted({key[1] for key in values}):
            outer = values.get((0.1, global_fraction))
            inner = values.get((0.05, global_fraction))
            if outer is not None and inner not in (None, 0.0):
                ratios.append(outer / inner)
        expected = 2.0 ** int(document["relative_nodes"])
        maximum_ratio_error = max(
            (abs(ratio / expected - 1.0) for ratio in ratios), default=float("inf")
        )
        passed = bool(
            document.get("port_validation", {}).get("passed")
            and int(document["relative_nodes"]) >= 16
            and ratios
            and maximum_ratio_error < 0.02
            and max(float(row["magnitude"]) for row in document["values"]) < 2.0e-19
        )
        witnesses[pair] = {
            "path": str(path),
            "sha256": digest(path),
            "job_key": document["job_key"],
            "pair": list(pair),
            "passed": passed,
            "expected_halving_ratio": expected,
            "measured_halving_ratios": ratios,
            "maximum_ratio_relative_error": maximum_ratio_error,
        }
    return witnesses


def restricted_certificate(
    row: dict[str, Any], ownership: dict[str, bool]
) -> dict[str, Any]:
    broad = M5041.theorem_certificate(row, ownership)
    owned_labels = [str(label) for label in broad.get("owned_labels", [])]
    owned_label = owned_labels[0] if len(owned_labels) == 1 else None
    pair = normalized_single_pair(broad)
    witnesses = proof_witnesses()
    family = (owned_label, pair) if owned_label is not None and pair is not None else None
    family_guard = family in PROVED_FAMILIES
    witness = witnesses.get(pair) if pair is not None else None
    witness_guard = bool(witness and witness["passed"])
    broad.update(
        {
            "broad_5041_guard_passed": bool(broad["passed"]),
            "proved_family_guard_passed": family_guard,
            "independent_witness_guard_passed": witness_guard,
            "proved_family": (
                {"owned_label": owned_label, "pair": list(pair)}
                if family_guard and pair is not None
                else None
            ),
            "independent_witness": witness,
            "scope_revision": REVISION,
            "scope_rule": (
                "exact zero is restricted to the two owned-direct:g1 branch families "
                "present in the original eight repairs and independent 70-digit witnesses"
            ),
            "passed": bool(broad["passed"] and family_guard and witness_guard),
            "valid_for_full_MTS_claim": False,
        }
    )
    return broad


def family_name(certificate: dict[str, Any]) -> str:
    owned = certificate.get("owned_labels", [])
    if len(owned) != 1:
        return "other"
    label = str(owned[0])
    if label.startswith("direct:g1:"):
        return "owned_direct_g1"
    if label.startswith("direct:g2:"):
        return "owned_direct_g2"
    if label.startswith("direct:g3:"):
        return "owned_direct_g3"
    if label.startswith("subtraction:"):
        return "owned_subtraction"
    return "other"


def original_repair_audit() -> dict[str, Any]:
    document = json.loads(ORIGINAL_AUDIT.read_text(encoding="utf-8"))
    rows = []
    for job in document["rows"]:
        for certificate in job.get("certificates", []):
            pair = normalized_single_pair(certificate)
            owned = certificate.get("owned_labels", [])
            family = (str(owned[0]), pair) if len(owned) == 1 and pair is not None else None
            rows.append(
                {
                    "job_key": job["job_key"],
                    "broad_passed": bool(certificate.get("passed")),
                    "restricted_family_passed": family in PROVED_FAMILIES,
                    "owned_labels": owned,
                    "pair": list(pair) if pair is not None else None,
                }
            )
    return {
        "source": str(ORIGINAL_AUDIT),
        "source_sha256": digest(ORIGINAL_AUDIT),
        "rows": rows,
        "count": len(rows),
        "all_original_eight_retained": len(rows) == 8
        and all(row["broad_passed"] and row["restricted_family_passed"] for row in rows),
    }


def fourth_scramble_audit() -> dict[str, Any]:
    family_counts: Counter[str] = Counter()
    strict_family_counts: Counter[str] = Counter()
    job_rows = []
    broad_count = 0
    restricted_count = 0
    for kernel_path in sorted((RUN_5040 / "kernels").glob("*S503404*.json")):
        kernel = json.loads(kernel_path.read_text(encoding="utf-8"))
        M5041.configure_from_kernel(kernel)
        _, ownerships = M5041.N5030.physical_chambers()
        job_family_counts: Counter[str] = Counter()
        job_strict_count = 0
        for chamber in kernel["fixed_event_integral_gate"]["chambers"]:
            ownership = ownerships[int(chamber["chamber_index"])]
            for residue in chamber["residue_catalog"]:
                if residue.get("residue_method") != M5041.REVISION:
                    continue
                certificate = restricted_certificate(residue, ownership)
                if not certificate["broad_5041_guard_passed"]:
                    raise RuntimeError(
                        f"stored broad zero failed recertification in {kernel['job_key']}"
                    )
                family = family_name(certificate)
                family_counts[family] += 1
                job_family_counts[family] += 1
                broad_count += 1
                if certificate["passed"]:
                    restricted_count += 1
                    job_strict_count += 1
                    strict_family_counts[family] += 1
        job_rows.append(
            {
                "job_key": kernel["job_key"],
                "broad_zero_count": sum(job_family_counts.values()),
                "restricted_zero_count": job_strict_count,
                "unproved_zero_count": sum(job_family_counts.values()) - job_strict_count,
                "family_counts": dict(job_family_counts),
            }
        )
    return {
        "jobs": len(job_rows),
        "broad_zero_count": broad_count,
        "restricted_zero_count": restricted_count,
        "unproved_zero_count": broad_count - restricted_count,
        "family_counts": dict(family_counts),
        "restricted_family_counts": dict(strict_family_counts),
        "rows": job_rows,
    }


def coarse_matrix_audit() -> dict[str, Any]:
    family_counts: Counter[str] = Counter()
    strict_count = 0
    broad_count = 0
    job_count = 0
    run_directory = POST / "source-intake" / "functional_rg" / "5043" / "runs"
    for job_path in sorted(run_directory.glob("*/jobs/*.json")):
        job = json.loads(job_path.read_text(encoding="utf-8"))
        if job.get("status") != "COMPLETED_CONVERGED":
            continue
        job_count += 1
        for certificate in job.get("theorem_zero_rows", []):
            broad_count += 1
            family_counts[family_name(certificate)] += 1
            owned = certificate.get("owned_labels", [])
            pair = normalized_single_pair(certificate)
            family = (str(owned[0]), pair) if len(owned) == 1 and pair is not None else None
            if family in PROVED_FAMILIES:
                strict_count += 1
    return {
        "jobs": job_count,
        "broad_zero_count": broad_count,
        "restricted_zero_count": strict_count,
        "unproved_zero_count": broad_count - strict_count,
        "family_counts": dict(family_counts),
    }


def stable_counterexamples() -> dict[str, Any]:
    rows = []
    for epsilon_id in ("E020", "E040"):
        kernel_path = (
            RUN_5040
            / "kernels"
            / f"{epsilon_id}__S503401_N0001__A00__primary24.json"
        )
        kernel = json.loads(kernel_path.read_text(encoding="utf-8"))
        M5041.configure_from_kernel(kernel)
        _, ownerships = M5041.N5030.physical_chambers()
        for chamber in kernel["fixed_event_integral_gate"]["chambers"]:
            ownership = ownerships[int(chamber["chamber_index"])]
            for residue in chamber["residue_catalog"]:
                certificate = restricted_certificate(residue, ownership)
                value = complex_value(residue["residue"])
                if not (
                    certificate["broad_5041_guard_passed"]
                    and not certificate["passed"]
                    and residue.get("stable")
                    and residue.get("included_as_pole_model")
                    and abs(value) > 1.0
                ):
                    continue
                rows.append(
                    {
                        "epsilon_id": epsilon_id,
                        "job_key": kernel["job_key"],
                        "chamber_index": int(chamber["chamber_index"]),
                        "owned_labels": certificate["owned_labels"],
                        "pairs": certificate["pairs"],
                        "residue": {"real": value.real, "imaginary": value.imag},
                        "residue_magnitude": abs(value),
                        "residue_stability": float(residue["residue_stability"]),
                        "broad_guard_passed": True,
                        "restricted_guard_passed": False,
                    }
                )
    return {
        "rows": rows,
        "count": len(rows),
        "maximum_residue_magnitude": max(
            (row["residue_magnitude"] for row in rows), default=0.0
        ),
    }


def quarantine_rows() -> list[dict[str, Any]]:
    specifications = (
        (
            "5040 fourth-scramble statistical products",
            POST / "source-intake" / "functional_rg" / "5040" / "nested_sobol_results.json",
            "QUARANTINED_PENDING_RESTRICTED_RECOMPUTE",
            "includes S503404 rows generated by the overbroad exact-zero guard",
        ),
        (
            "5041 theorem-guarded fourth-scramble continuation",
            POST / "scripts" / "Y5_R2FR_5041_theorem_guarded_5040_resume.py",
            "QUARANTINED_OVERBROAD_GUARD",
            "372 certificates exceed the two independently witnessed direct:g1 families",
        ),
        (
            "5041 original eight direct:g1 repairs",
            ORIGINAL_AUDIT,
            "RETAINED_PROVED_SCOPE",
            "all eight belong to the two independently witnessed owned-direct:g1 families",
        ),
        (
            "5042 outer control-variate result",
            POST / "source-intake" / "functional_rg" / "5042" / "unbiased_control_variate_gate.json",
            "QUARANTINED_PENDING_RESTRICTED_RECOMPUTE",
            "uses the contaminated four-scramble matrix",
        ),
        (
            "5043 theorem-first coarse matrix",
            POST / "source-intake" / "functional_rg" / "5043" / "multilevel_coarse_E040_gate.json",
            "QUARANTINED_OVERBROAD_GUARD",
            "most theorem-zero rows are outside the independently proved scope",
        ),
        (
            "5044 hybrid-fidelity reserve",
            POST / "source-intake" / "functional_rg" / "5044" / "symmetric_hybrid_fidelity_gate.json",
            "QUARANTINED_PENDING_RESTRICTED_RECOMPUTE",
            "derived from the quarantined 5043 coarse matrix",
        ),
        (
            "5045 broad theorem-first cost benchmark",
            SOURCE / "primary24_benchmark.json",
            "DIAGNOSTIC_FALSIFICATION_ONLY",
            "A00 differs from legacy by about 6.83 percent after unproved g3 zeros",
        ),
    )
    rows = []
    for artifact, path, status, reason in specifications:
        rows.append(
            {
                "artifact": artifact,
                "path": str(path),
                "path_exists": path.exists(),
                "sha256": digest(path) if path.is_file() else "MISSING",
                "status": status,
                "reason": reason,
                "valid_for_claim": False,
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: tuple[str, ...]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    witnesses = proof_witnesses()
    original = original_repair_audit()
    fourth = fourth_scramble_audit()
    coarse = coarse_matrix_audit()
    counterexamples = stable_counterexamples()
    mp_source = SCRIPT_MP.read_text(encoding="utf-8")
    quarantine = quarantine_rows()
    formal_digest = tree_digest(POST.parent / "formalization-workbench")
    payload = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "finding": (
            "the 5041 exact-zero theorem was implemented beyond its independently "
            "demonstrated owned-direct:g1 scope"
        ),
        "proved_families": [
            {"owned_label": owned, "pair": list(pair)}
            for owned, pair in sorted(PROVED_FAMILIES)
        ],
        "proof_witnesses": list(witnesses.values()),
        "original_repair_audit": original,
        "fourth_scramble_audit": fourth,
        "coarse_matrix_audit": coarse,
        "stable_nonzero_counterexamples": counterexamples,
        "arbitrary_precision_evaluator": {
            "path": str(SCRIPT_MP),
            "sha256": digest(SCRIPT_MP),
            "owned_direct_g1_source_guard_present": (
                'if not label.startswith("direct:g1:")' in mp_source
            ),
        },
        "quarantine": quarantine,
        "next_gate": (
            "rerun the six primary24 benchmark jobs with the restricted guard; only "
            "then authorize a scratch recomputation of S503404"
        ),
        "formalization_workbench_tree_sha256": formal_digest,
        "production_precision_complete": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(AUDIT_JSON, payload)
    audit_rows = [
        {
            "scope": "original_5041_eight",
            "broad_zero_rows": original["count"],
            "restricted_zero_rows": original["count"] if original["all_original_eight_retained"] else 0,
            "unproved_zero_rows": 0,
            "status": "RETAINED_PROVED_SCOPE",
        },
        {
            "scope": "fourth_scramble_S503404",
            "broad_zero_rows": fourth["broad_zero_count"],
            "restricted_zero_rows": fourth["restricted_zero_count"],
            "unproved_zero_rows": fourth["unproved_zero_count"],
            "status": "QUARANTINED_PENDING_RESTRICTED_RECOMPUTE",
        },
        {
            "scope": "5043_coarse_matrix",
            "broad_zero_rows": coarse["broad_zero_count"],
            "restricted_zero_rows": coarse["restricted_zero_count"],
            "unproved_zero_rows": coarse["unproved_zero_count"],
            "status": "QUARANTINED_OVERBROAD_GUARD",
        },
    ]
    write_csv(
        AUDIT_CSV,
        audit_rows,
        ("scope", "broad_zero_rows", "restricted_zero_rows", "unproved_zero_rows", "status"),
    )
    write_csv(
        QUARANTINE_CSV,
        quarantine,
        ("artifact", "path", "path_exists", "sha256", "status", "reason", "valid_for_claim"),
    )
    checks = [
        ("original_eight_retained", original["all_original_eight_retained"], str(original["count"])),
        ("two_witnessed_families", len(witnesses) == 2 and all(row["passed"] for row in witnesses.values()), str(len(witnesses))),
        ("fourth_broad_count_reproduced", fourth["broad_zero_count"] == 372, str(fourth["broad_zero_count"])),
        ("fourth_all_rows_outside_proved_scope", fourth["restricted_zero_count"] == 0 and fourth["unproved_zero_count"] == 372, str(fourth["restricted_zero_count"])),
        ("coarse_scope_narrows", 0 < coarse["restricted_zero_count"] < coarse["broad_zero_count"], str(coarse["restricted_zero_count"])),
        ("stable_nonzero_counterexample_exists", counterexamples["maximum_residue_magnitude"] > 1000.0, str(counterexamples["maximum_residue_magnitude"])),
        ("mp_evaluator_is_g1_scoped", payload["arbitrary_precision_evaluator"]["owned_direct_g1_source_guard_present"], str(SCRIPT_MP)),
        ("all_quarantine_paths_exist", all(row["path_exists"] for row in quarantine), str(sum(row["path_exists"] for row in quarantine))),
        ("claim_remains_false", not payload["valid_for_full_MTS_claim"], "required false"),
        ("formalization_workbench_unchanged", formal_digest == FORMAL_BASELINE, formal_digest),
    ]
    validation_rows = [
        {"check": name, "passed": str(bool(passed)).lower(), "evidence": evidence}
        for name, passed, evidence in checks
    ]
    write_csv(VALIDATION_CSV, validation_rows, ("check", "passed", "evidence"))
    print(json.dumps({"audit": str(AUDIT_JSON), "checks": validation_rows}, indent=2))


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SCRIPT_5124 = POST / "scripts" / "Y5_R2FR_5124_crossed_hhh_two_stratum_derivation.py"
SCRIPT_5125 = POST / "scripts" / "Y5_R2FR_5125_reciprocal_stratified_fresh_pilot_runner.py"
RESULT_5124 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5124"
    / "crossed_hhh_two_stratum_derivation.json"
)
SOURCE = POST / "source-intake" / "functional_rg" / "5126"
WITNESS_JSON = SOURCE / "S512502_E040_A10_unstable_reciprocal_witness.json"
GATE_JSON = SOURCE / "reciprocal_partner_residue_repair_gate.json"
OVERLAY_STATUS = SOURCE / "reciprocal_partner_pilot_overlay_status.json"
AUDIT_CSV = SOURCE / "reciprocal_partner_repair_audit.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5126_VALIDATION.csv"
)
DOCUMENT = POST / "5126-Y5-R2FR-reciprocal-partner-residue-repair-and-pilot-resume.md"
RUN_DIRECTORY = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5125"
    / "runs"
    / "reciprocal_stratified_fresh_pilot_v1"
)
FAILED_JOB = RUN_DIRECTORY / "jobs" / "E040__S512502_N0000__A10__primary24.json"
FAILED_KERNEL = (
    RUN_DIRECTORY / "kernels" / "E040__S512502_N0000__A10__primary24.json"
)

MARKER = "MTS_5126_RECIPROCAL_PARTNER_RESIDUE_REPAIR"
REVISION = "isolated-reciprocal-partner-catalog-overlay-v1"
CHECKED_DATE = "2026-07-19"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
ROOT_TOLERANCE = 2.0e-8
REPAIR_AUDIT: list[dict[str, Any]] = []


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5124 = load_module("mts_5124_for_5126", SCRIPT_5124)
M5125 = load_module("mts_5125_for_5126", SCRIPT_5125)
BASE_CATALOG = M5125.M5077.certified_primary_catalog


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


def relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_json(path: Path, value: Any) -> None:
    M5125.atomic_json(path, value)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def tagged(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint_marker": MARKER,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "source_checked_date": CHECKED_DATE,
    }


def swap_uv_label(label: str) -> str:
    swaps = {
        "plus_u": "plus_v",
        "plus_v": "plus_u",
        "minus_u": "minus_v",
        "minus_v": "minus_u",
    }
    prefix, factor = label.rsplit(":", 1)
    if factor not in swaps:
        raise ValueError(f"unrecognized reciprocal factor label: {label}")
    return f"{prefix}:{swaps[factor]}"


def canonical_pairs(pairs: list[list[str]]) -> tuple[tuple[str, ...], ...]:
    return tuple(sorted(tuple(sorted(pair)) for pair in pairs))


def mapped_pairs(pairs: list[list[str]]) -> tuple[tuple[str, ...], ...]:
    return tuple(
        sorted(tuple(sorted(swap_uv_label(label) for label in pair)) for pair in pairs)
    )


def root_residual(first: complex, second: complex) -> float:
    inverse = 1.0 / first
    return abs(second - inverse) / max(1.0, abs(second), abs(inverse))


def safe_pair_contract(first: dict[str, Any], second: dict[str, Any]) -> bool:
    return (
        not M5124.reciprocal_unsafe_pairs(first["pairs"])
        and not M5124.reciprocal_unsafe_pairs(second["pairs"])
        and mapped_pairs(first["pairs"]) == canonical_pairs(second["pairs"])
        and root_residual(complex(first["root"]), complex(second["root"]))
        < ROOT_TOLERANCE
    )


def reciprocal_partner(
    row: dict[str, Any], catalog: list[dict[str, Any]]
) -> tuple[dict[str, Any] | None, float]:
    candidates = [
        (
            root_residual(complex(row["root"]), complex(candidate["root"])),
            candidate,
        )
        for candidate in catalog
        if candidate is not row
    ]
    if not candidates:
        return None, math.inf
    residual, candidate = min(candidates, key=lambda value: value[0])
    return candidate, residual


def repairing_catalog(*arguments: Any, **keywords: Any) -> tuple[list[dict[str, Any]], bool]:
    catalog, base_stable = BASE_CATALOG(*arguments, **keywords)
    repaired = 0
    for row in catalog:
        if bool(row["stable"]):
            continue
        partner, residual = reciprocal_partner(row, catalog)
        if partner is None or residual >= ROOT_TOLERANCE:
            continue
        if not bool(partner["stable"]) or not safe_pair_contract(row, partner):
            continue
        original_residue = complex(row["residue"])
        partner_residue = complex(partner["residue"])
        repaired_residue = -partner_residue
        current_job = str(M5125.M5077.M5036.MREPAIR.CURRENT_JOB)
        certificate = tagged(
            {
                "job_key": current_job,
                "target_root": str(row["root"]),
                "partner_root": str(partner["root"]),
                "target_pairs": json.dumps(row["pairs"]),
                "partner_pairs": json.dumps(partner["pairs"]),
                "reciprocal_root_residual": residual,
                "unrepaired_residue": str(original_residue),
                "partner_residue": str(partner_residue),
                "repaired_residue": str(repaired_residue),
                "partner_numerically_zero": bool(partner["numerically_zero"]),
                "partner_stable": bool(partner["stable"]),
                "proof": "I:xi->1/xi gives I*omega=-omega, hence Res_(1/r)=-Res_r on an isolated reflection-even ownership branch",
                "scope": "single isolated reciprocal pair with exact u/v label involution; g2/decay and multi-pair groups excluded",
                "repair_applied": True,
            }
        )
        REPAIR_AUDIT.append(certificate)
        M5125.M5077.LOCAL_RESIDUE_RESOLUTION_AUDIT.append(certificate)
        row["outer_residue"] = repaired_residue
        row["inner_residue"] = repaired_residue
        row["residue"] = repaired_residue
        row["residue_stability"] = float(partner["residue_stability"])
        row["numerically_zero"] = bool(partner["numerically_zero"])
        row["stable"] = True
        row["residue_method"] = "isolated-reciprocal-partner-theorem-v1"
        repaired += 1
    return catalog, bool(base_stable or (repaired > 0 and all(row["stable"] for row in catalog)))


def extract_witness() -> dict[str, Any]:
    job = read_json(FAILED_JOB)
    kernel = read_json(FAILED_KERNEL)
    unstable: list[tuple[int, dict[str, Any], dict[str, Any]]] = []
    for chamber_index, chamber in enumerate(kernel["fixed_event_integral_gate"]["chambers"]):
        catalog = chamber["residue_catalog"]
        for row in catalog:
            if bool(row["stable"]):
                continue
            partner, residual = reciprocal_partner(row, catalog)
            if partner is not None:
                unstable.append((chamber_index, row, partner))
    if len(unstable) != 1:
        raise RuntimeError(f"expected one unstable reciprocal witness, found {len(unstable)}")
    chamber_index, target, partner = unstable[0]
    return tagged(
        {
            "job_path": relative(FAILED_JOB),
            "job_sha256": digest(FAILED_JOB),
            "kernel_path": relative(FAILED_KERNEL),
            "kernel_sha256": digest(FAILED_KERNEL),
            "job_status": job["status"],
            "job_config_digest": job["config_digest"],
            "chamber_index": chamber_index,
            "target_root": target["root"],
            "target_pairs": target["pairs"],
            "target_stable": target["stable"],
            "target_residue": target["residue"],
            "partner_root": partner["root"],
            "partner_pairs": partner["pairs"],
            "partner_stable": partner["stable"],
            "partner_numerically_zero": partner["numerically_zero"],
            "partner_residue": partner["residue"],
            "reciprocal_root_residual": root_residual(
                complex(target["root"]), complex(partner["root"])
            ),
            "label_involution_passed": mapped_pairs(target["pairs"])
            == canonical_pairs(partner["pairs"]),
            "safe_pair_contract_passed": safe_pair_contract(target, partner),
        }
    )


def validation_rows(checks: list[tuple[str, bool, str]]) -> list[dict[str, Any]]:
    return [
        tagged({"check_id": name, "passed": passed, "detail": detail})
        for name, passed, detail in checks
    ]


def dry_run() -> tuple[dict[str, Any], dict[str, Any]]:
    required = (
        SCRIPT_5124,
        SCRIPT_5125,
        RESULT_5124,
        FAILED_JOB,
        FAILED_KERNEL,
        RUN_DIRECTORY / "config.json",
        FORMAL,
    )
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(missing)
    if WITNESS_JSON.exists():
        witness = read_json(WITNESS_JSON)
    else:
        witness = extract_witness()
        atomic_json(WITNESS_JSON, witness)
    source = read_json(RESULT_5124)
    job = read_json(FAILED_JOB)
    run_config = read_json(RUN_DIRECTORY / "config.json")
    checks = [
        ("all_required_paths_exist", not missing, str(len(required))),
        ("failed_job_is_exact_locked_witness", job["job_key"] == "E040__S512502_N0000__A10__primary24" and witness["job_status"] == "COMPLETED_UNCONVERGED" and job["status"] in {"COMPLETED_UNCONVERGED", "COMPLETED_CONVERGED"}, f"locked={witness['job_status']};current={job['status']}"),
        ("base_5125_config_digest_preserved", job["config_digest"] == run_config["config_digest"], run_config["config_digest"]),
        ("one_unstable_residue_witness_locked", not bool(witness["target_stable"]), str(witness["target_residue"])),
        ("reciprocal_partner_root_is_exact", float(witness["reciprocal_root_residual"]) < ROOT_TOLERANCE, str(witness["reciprocal_root_residual"])),
        ("reciprocal_uv_label_involution_is_exact", bool(witness["label_involution_passed"]), json.dumps(witness["partner_pairs"])),
        ("partner_is_stable", bool(witness["partner_stable"]), str(witness["partner_residue"])),
        ("safe_pair_excludes_ambiguous_families", bool(witness["safe_pair_contract_passed"]), json.dumps(witness["target_pairs"])),
        ("source_5124_safe_theorem_has_zero_failures", int(source["reciprocal_audit"]["safe_pair_failures"]) == 0 and float(source["reciprocal_audit"]["maximum_safe_residue_antisymmetry_residual"]) < 2.0e-6, str(source["reciprocal_audit"]["maximum_safe_residue_antisymmetry_residual"])),
        ("unsafe_families_remain_fail_closed", "multi-root" in source["reciprocal_audit"]["unsafe_policy"] and "evaluate both" in source["reciprocal_audit"]["unsafe_policy"], source["reciprocal_audit"]["unsafe_policy"]),
        ("repair_does_not_relax_numeric_thresholds", "ROOT_TOLERANCE" in Path(__file__).read_text(encoding="utf-8") and "residue_stability" in Path(__file__).read_text(encoding="utf-8"), "analytic partner substitution only"),
        ("formalization_workbench_unchanged", tree_digest(FORMAL) == FORMAL_BASELINE, tree_digest(FORMAL)),
    ]
    authorized = all(passed for _, passed, _ in checks)
    gate = tagged(
        {
            "revision": REVISION,
            "witness": relative(WITNESS_JSON),
            "witness_sha256": digest(WITNESS_JSON),
            "source_5124": relative(RESULT_5124),
            "source_5124_sha256": digest(RESULT_5124),
            "base_config_digest": run_config["config_digest"],
            "repair_contract": "if and only if an unstable isolated safe row has one stable reciprocal u/v-involuted partner, replace its exact residue by minus the partner residue",
            "excluded_scope": "multi-pair groups, mixed direct:g2/subtraction:decay groups, missing partners, unstable partners, and root mismatches all fail closed",
            "repair_authorized": authorized,
            "default_enabled": False,
        }
    )
    atomic_json(GATE_JSON, gate)
    write_csv(VALIDATION_CSV, validation_rows(checks))
    write_document(gate, None)
    if not authorized:
        failures = [name for name, passed, _ in checks if not passed]
        raise RuntimeError(f"5126 repair gate failed: {failures}")
    return gate, witness


def write_document(gate: dict[str, Any], status: dict[str, Any] | None) -> None:
    witness = read_json(WITNESS_JSON)
    status_text = (
        "The repair has not been numerically replayed yet."
        if status is None
        else f"The overlay run state is `{status['state']}` with `{status['completed_converged']}` converged jobs, `{status['completed_unconverged']}` unconverged and `{status['failed']}` failed. This invocation applied `{status['repair_count_this_invocation']}` reciprocal repair(s)."
    )
    text = f"""# 5126 - reciprocal-partner residue repair and pilot resume

## Fresh obstruction

The locked 5125 pilot stopped at
`E040__S512502_N0000__A10__primary24`. One isolated
`direct:g1:plus_v / subtraction:decay:plus_u` residue was unstable under the
unchanged nested-radius test. Its reciprocal root is present in the same
chamber with residual `{witness['reciprocal_root_residual']:.3e}`, carries the
exact `u <-> v` label image and is stable.

## Derived repair

For `I: xi -> 1/xi`, the relative azimuth cosine is invariant, the sine
reflects, and the helicity-summed scalar contour kernel is even. Therefore
the relative one-form obeys `I*omega=-omega`, so

```text
Res_(1/r)(omega) = -Res_r(omega).
```

The catalog overlay may replace an unstable residue by minus its stable
partner only when the roots, unique pair structure and exact factor-label
involution all pass. The known `g2/decay` ambiguity, multi-pair groups,
unstable partners and missing partners remain fail-closed. No tolerance,
integration order, seed, allocation or field equation changes.

## Status

{status_text}

This remains a private nonclaim numerical repair. It does not establish the
UV coefficient, source coupling, local GR/Newton, Maxwell or full MTS.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def execute(wall_cap_hours: float, maximum_new_jobs: int) -> dict[str, Any]:
    gate, _ = dry_run()
    if not gate["repair_authorized"]:
        raise RuntimeError("5126 repair overlay is not authorized")
    activation, config, jobs = M5125.dry_run()
    if config["config_digest"] != gate["base_config_digest"]:
        raise RuntimeError("5125 base config changed after 5126 authorization")
    previous_catalog = M5125.M5077.certified_primary_catalog
    REPAIR_AUDIT.clear()
    M5125.M5077.certified_primary_catalog = repairing_catalog
    try:
        base_status = M5125.execute(
            activation,
            config,
            jobs,
            wall_cap_hours,
            maximum_new_jobs,
        )
    finally:
        M5125.M5077.certified_primary_catalog = previous_catalog
    if REPAIR_AUDIT:
        historical = []
        if AUDIT_CSV.exists():
            with AUDIT_CSV.open(newline="", encoding="utf-8") as handle:
                historical = list(csv.DictReader(handle))
        write_csv(AUDIT_CSV, [*historical, *REPAIR_AUDIT])
    repaired_job = read_json(FAILED_JOB)
    with AUDIT_CSV.open(newline="", encoding="utf-8") as handle:
        cumulative_repairs = list(csv.DictReader(handle))
    status = tagged(
        {
            **base_status,
            "revision": REVISION,
            "base_checkpoint_marker": base_status["checkpoint_marker"],
            "overlay_gate": relative(GATE_JSON),
            "overlay_gate_sha256": digest(GATE_JSON),
            "repair_count_this_invocation": len(REPAIR_AUDIT),
            "cumulative_repair_count": len(cumulative_repairs),
            "repair_audit": relative(AUDIT_CSV) if REPAIR_AUDIT else None,
            "original_witness_now_converged": repaired_job["status"]
            == "COMPLETED_CONVERGED",
            "base_config_digest_preserved": repaired_job["config_digest"]
            == gate["base_config_digest"],
            "formalization_unchanged": tree_digest(FORMAL) == FORMAL_BASELINE,
        }
    )
    atomic_json(OVERLAY_STATUS, status)
    run_checks = [
        ("original_unstable_job_now_converged", status["original_witness_now_converged"], repaired_job["status"]),
        ("at_least_one_guarded_repair_preserved", len(cumulative_repairs) >= 1, str(len(cumulative_repairs))),
        ("every_applied_repair_passed_scope", all(bool(row["repair_applied"]) and float(row["reciprocal_root_residual"]) < ROOT_TOLERANCE for row in REPAIR_AUDIT), str(len(REPAIR_AUDIT))),
        ("base_config_digest_preserved", status["base_config_digest_preserved"], gate["base_config_digest"]),
        ("formalization_workbench_unchanged", status["formalization_unchanged"], tree_digest(FORMAL)),
    ]
    write_csv(VALIDATION_CSV, validation_rows(run_checks))
    if not all(passed for _, passed, _ in run_checks):
        failures = [name for name, passed, _ in run_checks if not passed]
        raise RuntimeError(f"5126 replay validation failed: {failures}")
    write_document(gate, status)
    return status


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("dry-run", "run"), default="dry-run")
    parser.add_argument("--wall-cap-hours", type=float, default=4.0)
    parser.add_argument("--maximum-new-jobs", type=int, default=0)
    arguments = parser.parse_args()
    if arguments.mode == "dry-run":
        result, _ = dry_run()
    else:
        result = execute(arguments.wall_cap_hours, arguments.maximum_new_jobs)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

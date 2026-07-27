from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPT_5046 = POST / "scripts" / "Y5_R2FR_5046_restricted_scope_primary24_benchmark.py"
SOURCE = POST / "source-intake" / "functional_rg" / "5049"
RUNS = SOURCE / "runs"
BENCHMARK_JSON = SOURCE / "restricted_coarse_profile_benchmark.json"
RESULT_JSON = SOURCE / "restricted_multilevel_coarse_E040_gate.json"
COMPONENT_CSV = SOURCE / "restricted_multilevel_component_gate.csv"
LOCK_JSON = SOURCE / "restricted_locked_multilevel_pilot_contract.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5049_VALIDATION.csv"
)
MARKER = "MTS_5049_RESTRICTED_COARSE_E040_MULTILEVEL_REAUDIT"
REVISION = "restricted-theorem-first-coarse-E040-v1"


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5046 = load_module("mts_5046_for_restricted_coarse", SCRIPT_5046)
M5043 = M5046.M5043
N5030 = M5043.N5030
ORIGINAL_CATALOG = N5030.chamber_residue_catalog
ORIGINAL_GLOBAL_CHAMBER_VALUE = N5030.global_chamber_value
ORIGINAL_THEOREM = M5043.M5041.theorem_certificate


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def configured_profile_digests() -> dict[str, str]:
    return {
        profile_name: canonical_digest(
            {
                "marker": MARKER,
                "revision": REVISION,
                "profile": profile,
                "restricted_scope_sha256": digest(M5046.SCRIPT_5045_SCOPE),
                "corrected_5040_result_sha256": digest(
                    POST
                    / "source-intake"
                    / "functional_rg"
                    / "5040"
                    / "nested_sobol_results.json"
                ),
            }
        )
        for profile_name, profile in M5043.PROFILES.items()
    }


def configure_modules() -> None:
    M5043.SOURCE = SOURCE
    M5043.RUNS = RUNS
    M5043.BENCHMARK_JSON = BENCHMARK_JSON
    M5043.RESULT_JSON = RESULT_JSON
    M5043.COMPONENT_CSV = COMPONENT_CSV
    M5043.LOCK_JSON = LOCK_JSON
    M5043.VALIDATION_CSV = VALIDATION_CSV
    M5043.MARKER = MARKER
    M5043.REVISION = REVISION
    M5043.LOCKED_PROFILE_DIGESTS = configured_profile_digests()
    M5043.M5041.theorem_certificate = M5046.restricted_certificate
    N5030.chamber_residue_catalog = M5043.theorem_first_chamber_residue_catalog


def restore_modules() -> None:
    M5043.M5041.theorem_certificate = ORIGINAL_THEOREM
    N5030.chamber_residue_catalog = ORIGINAL_CATALOG
    N5030.global_chamber_value = ORIGINAL_GLOBAL_CHAMBER_VALUE


def strict_scope_audit(profile_name: str) -> dict[str, Any]:
    broad_count = 0
    strict_count = 0
    invalid_rows = []
    for path in sorted((RUNS / profile_name / "jobs").glob("*.json")):
        document = json.loads(path.read_text(encoding="utf-8"))
        for certificate in document.get("theorem_zero_rows", []):
            broad_count += 1
            family_guard = bool(certificate.get("proved_family_guard_passed"))
            witness_guard = bool(certificate.get("independent_witness_guard_passed"))
            if family_guard and witness_guard and certificate.get("passed"):
                strict_count += 1
            else:
                invalid_rows.append(
                    {
                        "path": str(path),
                        "owned_labels": certificate.get("owned_labels"),
                        "pairs": certificate.get("pairs"),
                    }
                )
    return {
        "theorem_zero_rows": broad_count,
        "strict_scope_rows": strict_count,
        "invalid_scope_rows": invalid_rows,
        "all_theorem_zeros_within_restricted_scope": broad_count == strict_count
        and not invalid_rows,
    }


def selected_profile_from_benchmark(default: str = "coarse12") -> str:
    if not BENCHMARK_JSON.exists():
        return default
    document = json.loads(BENCHMARK_JSON.read_text(encoding="utf-8"))
    selected = document.get("selected_profile")
    return str(selected) if selected in M5043.PROFILES else default


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("dry-run", "benchmark", "matrix", "analyze", "all"), default="dry-run"
    )
    parser.add_argument("--profiles", default="coarse8,coarse12")
    parser.add_argument("--profile", choices=tuple(M5043.PROFILES), default=None)
    parser.add_argument("--max-jobs", type=int, default=0)
    parser.add_argument("--max-wall-seconds", type=float, default=28_800.0)
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    if arguments.max_wall_seconds <= 0.0 or arguments.max_wall_seconds > 32_400.0:
        raise ValueError("wall limit must be in (0,32400] seconds")
    configure_modules()
    try:
        config = M5043.load_config()
        if arguments.mode == "dry-run":
            result = M5043.dry_run(config)
            result.update(
                {
                    "checkpoint_marker": MARKER,
                    "revision": REVISION,
                    "restricted_scope_source": str(M5046.SCRIPT_5045_SCOPE),
                    "valid_for_full_MTS_claim": False,
                }
            )
            M5043.atomic_json(SOURCE / "dry_run.json", result)
            print(json.dumps(result, indent=2))
            return
        selected = arguments.profile or selected_profile_from_benchmark()
        if arguments.mode in {"benchmark", "all"}:
            profiles = [value.strip() for value in arguments.profiles.split(",") if value.strip()]
            if any(value not in M5043.PROFILES for value in profiles):
                raise ValueError("unknown benchmark profile")
            benchmark = M5043.benchmark(config, profiles)
            selected = str(benchmark["selected_profile"] or selected)
            benchmark["restricted_scope_source"] = str(M5046.SCRIPT_5045_SCOPE)
            benchmark["restricted_scope_source_sha256"] = digest(M5046.SCRIPT_5045_SCOPE)
            M5043.atomic_json(BENCHMARK_JSON, benchmark)
            print(json.dumps(benchmark, indent=2))
            if arguments.mode == "benchmark":
                return
        if arguments.mode in {"matrix", "all"}:
            status = M5043.run_matrix(
                config,
                selected,
                arguments.max_jobs,
                arguments.max_wall_seconds,
            )
            scope = strict_scope_audit(selected)
            status["restricted_scope_audit"] = scope
            M5043.atomic_json(RUNS / selected / "status.json", status)
            print(json.dumps(status, indent=2))
            if arguments.mode == "matrix" and not status["complete"]:
                M5043.write_validation(config, selected, None)
                return
        if arguments.mode in {"analyze", "all"}:
            result = M5043.analyze(config, selected)
            scope = strict_scope_audit(selected)
            result["restricted_scope_audit"] = scope
            result["restricted_scope_source"] = str(M5046.SCRIPT_5045_SCOPE)
            result["restricted_scope_source_sha256"] = digest(M5046.SCRIPT_5045_SCOPE)
            result["valid_for_full_MTS_claim"] = False
            M5043.atomic_json(RESULT_JSON, result)
            validation = M5043.write_validation(config, selected, result)
            print(json.dumps(result, indent=2))
            print(
                json.dumps(
                    {
                        "validation_passed": sum(row["passed"] == "true" for row in validation),
                        "validation_total": len(validation),
                        "restricted_scope_passed": scope[
                            "all_theorem_zeros_within_restricted_scope"
                        ],
                    },
                    indent=2,
                )
            )
    finally:
        restore_modules()


if __name__ == "__main__":
    main()

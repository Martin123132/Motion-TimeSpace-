from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import math
import os
import re
import sys
import traceback
from pathlib import Path
from typing import Any, Callable


os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
sys.dont_write_bytecode = True

import numpy as np


CHECKPOINT = 5337
MARKER = "MTS_5337_D4_REGULATOR_FOLD_DOUBLE_SCALING_CONTRAST_GATE"
POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMAL = ROOT / "formalization-workbench"
OUT = POST / "source-intake" / "functional_rg" / str(CHECKPOINT)
RESIDUALS = POST / "source-intake" / "mts_residuals"
VALIDATION = RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv"
RESULT = OUT / "D4_regulator_fold_double_scaling_contrast_result.json"
SCAN_STATUS = OUT / "scan_status.json"
RUNG_CACHE = OUT / "rung-cache"
SOURCE_LOCK_NOTE = (
    POST
    / "source-intake"
    / "maths_exploration"
    / str(CHECKPOINT)
    / "new-bundles-source-lock.md"
)
SCRIPT_5334 = POST / "scripts" / "Y5_R2FR_5334_D4_outer_regulator_ladder_controller.py"
FORMAL_DIGEST = "0ec1bc6012136ffc6b28a1512aca6ce712b6decd2ff793310a9bd61775f3db1f"
EPSILON_REFERENCE = 0.01
CONTACT_RESIDUAL_LIMIT = 1.0e-7
TRANSVERSE_SLOPE_FLOOR = 1.0e-3
SLOPE_WINDOW_RELATIVE_CHANGE_LIMIT = 0.5
EVENT_ROOT_WIDTH = 2.0e-11
EXPECTED_EVENT_COUNT = 8

EPSILON_VALUES = {
    "E000625": 0.000625,
    "E00125": 0.00125,
    "E0025": 0.0025,
    "E005": 0.005,
    "E010": 0.01,
    "E020": 0.02,
    "E040": 0.04,
}

LOCAL_SOURCE_LOCKS = {
    "5328-Y5-R2FR-D2-midpoint-regulator-zero-normal-form-gate.md": "cc4e79b592442328391c55a3fbf28ef89513d0794ec42e3e12076b59da1f71b9",
    "5334-Y5-R2FR-D4-outer-regulator-ladder-controller.md": "df162cb4ac3033e55a79423577f4c02879aec1f34a79aa1e4bcc2352132916fa",
    "5336-Y5-R2FR-fold-pair-equivalence-and-incremental-ownership-gate.md": "8da71824604c71cbe84b549b29c5128e0bdbb31795497fce2de43c2db6128cc2",
    "scripts/Y5_R2FR_5334_D4_outer_regulator_ladder_controller.py": "8da808982fdfc61c45af9f349467ea4c38a62e9d470569714cf739d07fb6f2c8",
    "source-intake/functional_rg/5327/D2_midpoint_finite_regulator_ladder.csv": "0b18c3427dc49b25f9b56359857369688b35dd597b2fa95a899a6490be6df9ae",
    "source-intake/functional_rg/5328/D2_midpoint_event_normal_form_certificate.csv": "6b74f84214b072ffd379e0d8942e1c0e86eef9bc25d7e03e769b108bdd2da8a5",
    "source-intake/functional_rg/5328/D2_midpoint_regulator_zero_normal_form_contract.csv": "2f88620a6e6b7e8ccf55aa3aa65949252f300cc441c3f3e5666307490ada4a98",
    "source-intake/functional_rg/5328/D2_midpoint_regulator_zero_normal_form_result.json": "da044602498e914b118c1c9a851175ccc6d6ca0bf95c9cc81cfd170fec683e23",
    "source-intake/functional_rg/5334/E0025/D4_outer_reduced_MC04_cubature_contract.csv": "0f691d1fa568d930a2d362e3f6aafdad1aee2746f43dcba4709590b3ead96cc2",
    "source-intake/functional_rg/5334/E0025/D4_outer_refined_support_events.csv": "c50085b936f4d6f7aad04f3d5f875b7804945b88ffcc0d8249c603c96bd9b158",
    "source-intake/functional_rg/5334/E0025/D4_outer_support_event_state_scan.csv": "f9ea47a161c8ce44f4840d7b114881341d3daf80794939372f023cd0ffb1a7b9",
    "source-intake/functional_rg/5334/E0025/D4_outer_event_aligned_initial_plan.csv": "34ac0685dcaef29298d44b0344f7d5efe0ffde3949366d37bbab2101e259181c",
    "source-intake/functional_rg/5334/E0025/D4_outer_event_aligned_E0025_result.json": "ba8d5d38578e8d380ec244d248ae8b29fa036753b47046f925a68fe8a19fc3c4",
    "source-intake/maths_exploration/5337/new-bundles-source-lock.md": "ba081bb773dcae36290ed0fc2314b882d7b04c75c6ad0f82ce5612b45971d851",
}

BUNDLE_LOCKS = (
    (
        "one_motion_massive_multihistory_bundle.zip",
        "2f78289a607174e669a2e3459e2e7cdc8bc94d5e",
        "c521f83730479320f805a43d3468afbb7ac8b7d7",
        "36cbe47d2e82bff91f25c9ccad312fd4c5c2aa087867757a9612445d05a760b1",
        973482,
    ),
    (
        "one_motion_massive_fold_bandwidth_bundle.zip",
        "874bf845b32f06ca4767482cf8e5805cc9a07bd6",
        "96246f7f33c3d792db951f1313d781f8f24847c2",
        "85378a423b4e5165cbe2afc45b736ad5339c31a97f3050444cd91a04a51672b9",
        759108,
    ),
    (
        "one_motion_fold_resolution_universality_bundle.zip",
        "646a325d0de5432538de2b32a167976d4a83d61e",
        "28838be8247559db2320ab44acf2db6832385de6",
        "712fc1f6187784b59329c1ea395c0e6247bf097806269797fc2ecc96f4502b2d",
        806605,
    ),
    (
        "one_motion_mixed_history_reconstruction_bundle.zip",
        "974e65ecbfa1b5c34c27061a2451f5ff15404df8",
        "c1fdd919ebe682e08e476c9c7f518f889d908fbf",
        "7864096620f6d077ea9ced972191e3a3572ed040449d2a508e3f82a7ce397bda",
        1230102,
    ),
    (
        "one_motion_worldline_inverse_bundle.zip",
        "1948cd75dbf09c5a97a91906b582d985931b716e",
        "d6729dcd6791d7bfcc94acffda338708052f8e56",
        "4a9d5a72485ef5866f961287462d3240f8852f197c0c37703f268d7f19c01050",
        1445124,
    ),
    (
        "causal_inference_workbench_bundle.zip",
        "797d8e992215c2877e744e0f766874fd4a9ae3f0",
        "f5bab928d7aeeaf9609ec5d34fe14d0b34319208",
        "9f014957ed1bfd6f7eb4ced836291d83a4776f46ff68d244469e03042ccd0869",
        612759,
    ),
)

CLAIM_FIELDS = (
    "valid_for_D4_regulator_zero_limit",
    "valid_for_decay_angle_integral",
    "valid_for_full_angular_convergence",
    "valid_for_full_phase_space_coefficient",
    "valid_for_numeric_UV_claim",
    "valid_for_local_GR_claim",
    "valid_for_full_MTS_claim",
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def serialized_hash(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def formal_inventory_digest() -> str:
    rows = [
        {
            "relative_path": str(path.relative_to(FORMAL)),
            "size": str(path.stat().st_size),
            "sha256": digest(path),
        }
        for path in sorted(
            (item for item in FORMAL.rglob("*") if item.is_file()),
            key=lambda item: str(item).lower(),
        )
    ]
    return serialized_hash(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"empty CSV payload: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    temporary.replace(path)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def safe_token(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("._")


def cached_event_row(
    path: Path,
    epsilon_id: str,
    event_id: str,
    cache_signature: str,
) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    row = payload.get("row")
    if (
        payload.get("marker") != MARKER
        or payload.get("epsilon_id") != epsilon_id
        or payload.get("event_id") != event_id
        or payload.get("cache_signature") != cache_signature
        or not isinstance(row, dict)
        or row.get("epsilon_id") != epsilon_id
        or row.get("event_id") != event_id
    ):
        return None
    return row


def cached_rung_rows(
    path: Path,
    epsilon_id: str,
    cache_signature: str,
) -> list[dict[str, Any]] | None:
    if not path.is_file():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    rows = payload.get("rows")
    if (
        payload.get("marker") != MARKER
        or payload.get("epsilon_id") != epsilon_id
        or payload.get("cache_signature") != cache_signature
        or not isinstance(rows, list)
        or len(rows) != EXPECTED_EVENT_COUNT
        or any(
            not isinstance(row, dict) or row.get("epsilon_id") != epsilon_id
            for row in rows
        )
    ):
        return None
    return rows


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def no_claims() -> dict[str, bool]:
    return {field: False for field in CLAIM_FIELDS}


def validation_row(gate: str, passed: bool, detail: str) -> dict[str, Any]:
    return {
        "gate": gate,
        "passed": passed,
        "detail": detail,
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
    }


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def source_rows() -> tuple[list[dict[str, Any]], bool]:
    rows: list[dict[str, Any]] = []
    all_locked = True
    for relative, expected in LOCAL_SOURCE_LOCKS.items():
        path = POST / relative
        actual = digest(path) if path.is_file() else "MISSING"
        locked = actual == expected
        all_locked = all_locked and locked
        rows.append(
            {
                "source_kind": "LOCAL_PARENT_OR_INTAKE",
                "source_id": relative,
                "commit": "LOCAL_LOCK",
                "git_blob": "NOT_APPLICABLE",
                "sha256": actual,
                "expected_sha256": expected,
                "bytes": path.stat().st_size if path.is_file() else "MISSING",
                "locked": locked,
                "source_path_or_url": str(path),
                "valid_for_parent_ownership": relative.startswith("source-intake/functional_rg/532"),
                **no_claims(),
            }
        )
    for filename, commit, blob, sha256, size in BUNDLE_LOCKS:
        complete = (
            len(commit) == 40
            and len(blob) == 40
            and len(sha256) == 64
            and size > 0
        )
        all_locked = all_locked and complete
        rows.append(
            {
                "source_kind": "PRIVATE_GITHUB_BUNDLE",
                "source_id": filename,
                "commit": commit,
                "git_blob": blob,
                "sha256": sha256,
                "expected_sha256": sha256,
                "bytes": size,
                "locked": complete,
                "source_path_or_url": (
                    "https://github.com/Martin123132/maths-exploration-/commit/"
                    + commit
                ),
                "valid_for_parent_ownership": False,
                **no_claims(),
            }
        )
    return rows, all_locked


def fold_double_scaling_rows() -> tuple[list[dict[str, Any]], dict[str, float]]:
    coefficient = 0.5625
    fixed_mass = 12.0
    fixed_xi = 4.0
    deltas = np.logspace(-5.0, -2.0, 13)
    rows: list[dict[str, Any]] = []
    fixed_mass_values: list[float] = []
    fixed_xi_values: list[float] = []
    maximum_asymptotic_error = 0.0
    for delta in deltas:
        xi_mass = fixed_mass * float(delta)
        argument_mass = 0.5 * math.sqrt(coefficient) * xi_mass
        ratio_mass = 2.0 * math.sin(argument_mass / 2.0) ** 2
        asymptotic = coefficient * fixed_mass**2 * float(delta) ** 2 / 8.0
        relative_error = abs(ratio_mass - asymptotic) / asymptotic
        maximum_asymptotic_error = max(maximum_asymptotic_error, relative_error)
        argument_xi = 0.5 * math.sqrt(coefficient) * fixed_xi
        ratio_xi = 2.0 * math.sin(argument_xi / 2.0) ** 2
        fixed_mass_values.append(ratio_mass)
        fixed_xi_values.append(ratio_xi)
        rows.extend(
            (
                {
                    "path": "FIXED_MASS",
                    "delta": float(delta),
                    "mass": fixed_mass,
                    "xi_mass_delta": xi_mass,
                    "tail_over_root": ratio_mass,
                    "small_delta_asymptotic": asymptotic,
                    "relative_asymptotic_error": relative_error,
                    "physical_interpretation": "xi tends to zero",
                    **no_claims(),
                },
                {
                    "path": "FIXED_XI_COSCALING",
                    "delta": float(delta),
                    "mass": fixed_xi / float(delta),
                    "xi_mass_delta": fixed_xi,
                    "tail_over_root": ratio_xi,
                    "small_delta_asymptotic": "NOT_FIXED_MASS",
                    "relative_asymptotic_error": "NOT_FIXED_MASS",
                    "physical_interpretation": "mass diverges as inverse delta",
                    **no_claims(),
                },
            )
        )
    fixed_mass_exponent = float(
        np.polyfit(np.log(deltas), np.log(fixed_mass_values), 1)[0]
    )
    fixed_xi_exponent = float(
        np.polyfit(np.log(deltas), np.log(fixed_xi_values), 1)[0]
    )
    return rows, {
        "fixed_mass_exponent": fixed_mass_exponent,
        "fixed_xi_exponent": fixed_xi_exponent,
        "maximum_asymptotic_error": maximum_asymptotic_error,
    }


def through_origin_slope(points: list[tuple[float, float]]) -> float:
    denominator = sum(delta * delta for delta, _ in points)
    if denominator <= 0.0:
        return math.nan
    return sum(delta * value for delta, value in points) / denominator


def d4_targeted_event_scan() -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    module = load_module("mts_5334_for_5337", SCRIPT_5334)
    module.configure_smoke()
    contract_path = (
        POST
        / "source-intake"
        / "functional_rg"
        / "5334"
        / "E0025"
        / "D4_outer_reduced_MC04_cubature_contract.csv"
    )
    source_event_path = (
        POST
        / "source-intake"
        / "functional_rg"
        / "5334"
        / "E0025"
        / "D4_outer_refined_support_events.csv"
    )
    contract = read_csv(contract_path)
    source_events = read_csv(source_event_path)
    cache_signature = serialized_hash(
        {
            "algorithm": "D4_TARGETED_EVENT_SCAN_RESUMABLE_V1",
            "contract_sha256": digest(contract_path),
            "source_events_sha256": digest(source_event_path),
            "parent_runner_sha256": digest(SCRIPT_5334),
            "event_root_width": EVENT_ROOT_WIDTH,
            "contact_residual_limit": CONTACT_RESIDUAL_LIMIT,
            "transverse_slope_floor": TRANSVERSE_SLOPE_FLOOR,
            "slope_window_relative_change_limit": SLOPE_WINDOW_RELATIVE_CHANGE_LIMIT,
        }
    )
    panel_bounds: dict[int, tuple[float, float]] = {}
    for row in contract:
        panel_index = int(row["x_panel_index"])
        lower = float(row["lower_absolute_soft_cosine"])
        upper = float(row["upper_absolute_soft_cosine"])
        if panel_index not in panel_bounds:
            panel_bounds[panel_index] = (lower, upper)
        else:
            old_lower, old_upper = panel_bounds[panel_index]
            panel_bounds[panel_index] = (min(old_lower, lower), max(old_upper, upper))

    original_epsilon_id = module.M5325.EPSILON_ID
    original_epsilon = module.M5325.EPSILON
    rows: list[dict[str, Any]] = []

    for epsilon_id, epsilon in EPSILON_VALUES.items():
        rung_directory = RUNG_CACHE / epsilon_id
        rung_path = rung_directory / "rung_result.json"
        cached_rows = cached_rung_rows(rung_path, epsilon_id, cache_signature)
        if cached_rows is not None:
            rows.extend(cached_rows)
            print(
                f"[{utc_now()}] resumed complete {epsilon_id}: "
                f"{len(cached_rows)}/{EXPECTED_EVENT_COUNT} events",
                flush=True,
            )
            continue

        rung_directory.mkdir(parents=True, exist_ok=True)
        module.M5325.EPSILON_ID = epsilon_id
        module.M5325.EPSILON = epsilon
        old_kernel = module.M5325.configure_kernel()
        state_cache: dict[tuple[int, str, str, float], dict[str, Any]] = {}

        def state(
            panel_index: int,
            term_id: str,
            surface_id: str,
            coordinate: float,
        ) -> dict[str, Any]:
            key = (panel_index, term_id, surface_id, round(coordinate, 15))
            if key in state_cache:
                return dict(state_cache[key])
            cells = [
                module.M5312.cell_geometry(row, coordinate)
                for row in contract
                if int(row["x_panel_index"]) == panel_index
                and int(row["reduced_MC04_term_count"]) > 0
            ]
            supports = module.M5312.merged_term_supports(cells).get(term_id, [])
            node = {
                "node_id": f"CP5337_{epsilon_id}_{len(state_cache) + 1:04d}",
                "x_panel_index": panel_index,
                "outer_order": 0,
                "absolute_soft_cosine": coordinate,
            }
            poles = module.M5312.scan_term_poles(node, term_id, supports)
            selected = [
                pole for pole in poles if pole["primary_surface_id"] == surface_id
            ]
            if len(selected) > 1:
                raise RuntimeError(
                    f"multiple {term_id} {surface_id} branches at {coordinate}"
                )
            if not selected:
                result = {
                    "branch_exists": False,
                    "coordinate": coordinate,
                    "signed_support_margin": math.nan,
                    "pole_real": math.nan,
                    "pole_imaginary": math.nan,
                    "support_lower": math.nan,
                    "support_upper": math.nan,
                }
            else:
                pole = selected[0]
                margin, support = module.M5326.support_margin(
                    float(pole["pole_real"]), supports
                )
                result = {
                    "branch_exists": True,
                    "coordinate": coordinate,
                    "signed_support_margin": float(margin),
                    "pole_real": float(pole["pole_real"]),
                    "pole_imaginary": float(pole["pole_imaginary"]),
                    "support_lower": float(support["lower"]),
                    "support_upper": float(support["upper"]),
                }
            state_cache[key] = result
            return dict(result)

        try:
            for event_index, source in enumerate(source_events, start=1):
                panel_index = int(source["x_panel_index"])
                term_id = source["term_id"]
                surface_id = source["primary_surface_id"]
                event_type = source["event_type"]
                event_id = source["event_id"]
                event_path = rung_directory / (
                    f"{event_index:02d}-{safe_token(event_id)}.json"
                )
                cached_row = cached_event_row(
                    event_path,
                    epsilon_id,
                    event_id,
                    cache_signature,
                )
                if cached_row is not None:
                    rows.append(cached_row)
                    print(
                        f"[{utc_now()}] resumed {epsilon_id} event "
                        f"{event_index}/{EXPECTED_EVENT_COUNT}: {event_id}",
                        flush=True,
                    )
                    continue

                atomic_json(
                    SCAN_STATUS,
                    {
                        "checkpoint": CHECKPOINT,
                        "marker": MARKER,
                        "state": "RUNNING",
                        "epsilon_id": epsilon_id,
                        "epsilon": epsilon,
                        "event_index": event_index,
                        "event_count": EXPECTED_EVENT_COUNT,
                        "event_id": event_id,
                        "completed_event_artifact_count": len(
                            list(RUNG_CACHE.glob("*/*.json"))
                        ),
                        "cache_signature": cache_signature,
                        "updated_utc": utc_now(),
                    },
                )
                print(
                    f"[{utc_now()}] scanning {epsilon_id} event "
                    f"{event_index}/{EXPECTED_EVENT_COUNT}: {event_id}",
                    flush=True,
                )
                left = float(source["source_bracket_left"])
                right = float(source["source_bracket_right"])
                lower_panel, upper_panel = panel_bounds[panel_index]

                def bracketed(
                    left_state: dict[str, Any], right_state: dict[str, Any]
                ) -> bool:
                    if event_type == "BRANCH_DEATH":
                        return bool(left_state["branch_exists"]) != bool(
                            right_state["branch_exists"]
                        )
                    return (
                        bool(left_state["branch_exists"])
                        and bool(right_state["branch_exists"])
                        and math.isfinite(left_state["signed_support_margin"])
                        and math.isfinite(right_state["signed_support_margin"])
                        and left_state["signed_support_margin"]
                        * right_state["signed_support_margin"]
                        <= 0.0
                    )

                left_state = state(panel_index, term_id, surface_id, left)
                right_state = state(panel_index, term_id, surface_id, right)
                expansion = 0
                while not bracketed(left_state, right_state) and expansion < 8:
                    width = right - left
                    left = max(lower_panel, left - width)
                    right = min(upper_panel, right + width)
                    left_state = state(panel_index, term_id, surface_id, left)
                    right_state = state(panel_index, term_id, surface_id, right)
                    expansion += 1
                if not bracketed(left_state, right_state):
                    raise RuntimeError(
                        f"unbracketed {epsilon_id} {source['event_id']} {event_type}"
                    )

                iteration_count = 0
                while right - left > EVENT_ROOT_WIDTH and iteration_count < 80:
                    iteration_count += 1
                    middle = 0.5 * (left + right)
                    middle_state = state(panel_index, term_id, surface_id, middle)
                    if event_type == "BRANCH_DEATH":
                        if bool(middle_state["branch_exists"]) == bool(
                            left_state["branch_exists"]
                        ):
                            left = middle
                            left_state = middle_state
                        else:
                            right = middle
                            right_state = middle_state
                    else:
                        if (
                            left_state["signed_support_margin"]
                            * middle_state["signed_support_margin"]
                            <= 0.0
                        ):
                            right = middle
                            right_state = middle_state
                        else:
                            left = middle
                            left_state = middle_state

                event_coordinate = 0.5 * (left + right)
                if event_type == "BRANCH_DEATH":
                    root_state = (
                        left_state if left_state["branch_exists"] else right_state
                    )
                else:
                    candidates = [left_state, right_state]
                    root_state = min(
                        candidates,
                        key=lambda item: abs(item["signed_support_margin"]),
                    )
                lower_contact = abs(root_state["pole_real"] - root_state["support_lower"])
                upper_contact = abs(root_state["pole_real"] - root_state["support_upper"])
                contact_residual = min(lower_contact, upper_contact)
                contact_boundary = "LOWER" if lower_contact <= upper_contact else "UPPER"

                sample_deltas = (
                    1.0e-6,
                    2.0e-6,
                    5.0e-6,
                    1.0e-5,
                    2.0e-5,
                    5.0e-5,
                    1.0e-4,
                    2.0e-4,
                    5.0e-4,
                )
                points: list[tuple[float, float]] = []
                left_absent = False
                right_absent = False
                for delta in sample_deltas:
                    for direction in (-1.0, 1.0):
                        coordinate = event_coordinate + direction * delta
                        if coordinate <= lower_panel or coordinate >= upper_panel:
                            continue
                        sampled = state(
                            panel_index, term_id, surface_id, coordinate
                        )
                        if not sampled["branch_exists"]:
                            if direction < 0.0:
                                left_absent = True
                            else:
                                right_absent = True
                            continue
                        margin = sampled["signed_support_margin"]
                        if event_type != "BRANCH_DEATH" or margin > 0.0:
                            points.append((delta, abs(float(margin))))
                near_points = [point for point in points if point[0] <= 1.0e-4]
                broad_slope = through_origin_slope(points)
                near_slope = through_origin_slope(near_points)
                slope_change = (
                    abs(broad_slope - near_slope)
                    / max(abs(broad_slope), abs(near_slope), 1.0e-300)
                    if math.isfinite(broad_slope) and math.isfinite(near_slope)
                    else math.inf
                )
                opposite_absence = left_absent or right_absent
                normal_form_class = (
                    "ONE_SIDED_TRANSVERSE_SUPPORT_CONTACT"
                    if event_type == "BRANCH_DEATH"
                    else "TWO_SIDED_TRANSVERSE_SUPPORT_CONTACT"
                )
                passes = (
                    contact_residual <= CONTACT_RESIDUAL_LIMIT
                    and len(points) >= 3
                    and len(near_points) >= 2
                    and math.isfinite(broad_slope)
                    and math.isfinite(near_slope)
                    and broad_slope >= TRANSVERSE_SLOPE_FLOOR
                    and near_slope >= TRANSVERSE_SLOPE_FLOOR
                    and slope_change <= SLOPE_WINDOW_RELATIVE_CHANGE_LIMIT
                    and (event_type != "BRANCH_DEATH" or opposite_absence)
                    and (event_type != "BRANCH_DEATH" or contact_boundary == "UPPER")
                )
                event_row = {
                        "epsilon_id": epsilon_id,
                        "epsilon": epsilon,
                        "event_id": event_id,
                        "event_type": event_type,
                        "x_panel_index": panel_index,
                        "term_id": term_id,
                        "primary_surface_id": surface_id,
                        "event_coordinate": event_coordinate,
                        "source_E0025_event_coordinate": float(source["event_coordinate"]),
                        "coordinate_shift_from_E0025": event_coordinate
                        - float(source["event_coordinate"]),
                        "contact_boundary": contact_boundary,
                        "contact_residual": contact_residual,
                        "pole_real": root_state["pole_real"],
                        "pole_imaginary": root_state["pole_imaginary"],
                        "imaginary_displacement_coefficient_abs": abs(
                            root_state["pole_imaginary"]
                        )
                        / epsilon,
                        "broad_transverse_slope_magnitude": broad_slope,
                        "near_transverse_slope_magnitude": near_slope,
                        "slope_window_relative_change": slope_change,
                        "broad_slope_point_count": len(points),
                        "near_slope_point_count": len(near_points),
                        "opposite_side_branch_absence_witness": opposite_absence,
                        "normal_form_class": normal_form_class,
                        "targeted_event_contract_passes": passes,
                        "root_iteration_count": iteration_count,
                        "source_event_path": str(source_event_path),
                        **no_claims(),
                    }
                rows.append(event_row)
                atomic_json(
                    event_path,
                    {
                        "checkpoint": CHECKPOINT,
                        "marker": MARKER,
                        "state": "EVENT_COMPLETE",
                        "epsilon_id": epsilon_id,
                        "epsilon": epsilon,
                        "event_id": event_id,
                        "event_index": event_index,
                        "cache_signature": cache_signature,
                        "completed_utc": utc_now(),
                        "row": event_row,
                    },
                )
                print(
                    f"[{utc_now()}] saved {epsilon_id} event "
                    f"{event_index}/{EXPECTED_EVENT_COUNT}: {event_id}",
                    flush=True,
                )

            rung_rows = [row for row in rows if row["epsilon_id"] == epsilon_id]
            if len(rung_rows) != EXPECTED_EVENT_COUNT:
                raise RuntimeError(
                    f"incomplete {epsilon_id} rung: "
                    f"{len(rung_rows)}/{EXPECTED_EVENT_COUNT} events"
                )
            atomic_json(
                rung_path,
                {
                    "checkpoint": CHECKPOINT,
                    "marker": MARKER,
                    "state": "RUNG_COMPLETE",
                    "epsilon_id": epsilon_id,
                    "epsilon": epsilon,
                    "cache_signature": cache_signature,
                    "completed_utc": utc_now(),
                    "rows": rung_rows,
                },
            )
            print(
                f"[{utc_now()}] saved complete {epsilon_id}: "
                f"{len(rung_rows)}/{EXPECTED_EVENT_COUNT} events",
                flush=True,
            )
        finally:
            module.M5325.restore_kernel(old_kernel)

    module.M5325.EPSILON_ID = original_epsilon_id
    module.M5325.EPSILON = original_epsilon

    summaries: list[dict[str, Any]] = []
    order_signatures: list[str] = []
    for epsilon_id, epsilon in EPSILON_VALUES.items():
        selected = sorted(
            (row for row in rows if row["epsilon_id"] == epsilon_id),
            key=lambda row: float(row["event_coordinate"]),
        )
        order_signature = "|".join(str(row["event_id"]) for row in selected)
        order_signatures.append(order_signature)
        coordinates = np.asarray(
            [float(row["event_coordinate"]) for row in selected], dtype=float
        )
        gaps = np.diff(coordinates)
        for index, row in enumerate(selected):
            adjacent: list[float] = []
            if index > 0:
                adjacent.append(coordinates[index] - coordinates[index - 1])
            if index + 1 < len(coordinates):
                adjacent.append(coordinates[index + 1] - coordinates[index])
            local_half_gap = 0.5 * min(adjacent)
            regulator_width = (
                float(row["imaginary_displacement_coefficient_abs"])
                * epsilon
                / float(row["near_transverse_slope_magnitude"])
            )
            eta = regulator_width / local_half_gap
            row["local_half_nearest_event_gap"] = local_half_gap
            row["regulator_contact_width"] = regulator_width
            row["eta_regulator_width_over_half_gap"] = eta
            row["zeta_half_gap_over_regulator_width"] = 1.0 / eta
        summaries.append(
            {
                "epsilon_id": epsilon_id,
                "epsilon": epsilon,
                "event_count": len(selected),
                "event_order_signature": order_signature,
                "minimum_event_gap": float(np.min(gaps)),
                "minimum_event_gap_over_epsilon": float(np.min(gaps)) / epsilon,
                "maximum_eta_regulator_width_over_half_gap": max(
                    float(row["eta_regulator_width_over_half_gap"])
                    for row in selected
                ),
                "minimum_zeta_half_gap_over_regulator_width": min(
                    float(row["zeta_half_gap_over_regulator_width"])
                    for row in selected
                ),
                "all_targeted_event_contracts_pass": all(
                    bool(row["targeted_event_contract_passes"])
                    for row in selected
                ),
                **no_claims(),
            }
        )

    epsilons = np.asarray([float(row["epsilon"]) for row in summaries])
    minimum_gaps = np.asarray(
        [float(row["minimum_event_gap"]) for row in summaries]
    )
    maximum_etas = np.asarray(
        [float(row["maximum_eta_regulator_width_over_half_gap"]) for row in summaries]
    )
    gap_exponent = float(np.polyfit(np.log(epsilons), np.log(minimum_gaps), 1)[0])
    eta_exponent = float(np.polyfit(np.log(epsilons), np.log(maximum_etas), 1)[0])
    coordinate_shifts = [
        abs(float(row["coordinate_shift_from_E0025"])) for row in rows
    ]
    all_contracts_pass = all(
        bool(row["targeted_event_contract_passes"]) for row in rows
    )
    order_stable = len(set(order_signatures)) == 1
    event_count_complete = all(
        int(row["event_count"]) == EXPECTED_EVENT_COUNT for row in summaries
    )
    co_scaling_rejected = (
        all_contracts_pass
        and order_stable
        and event_count_complete
        and abs(gap_exponent) <= 0.15
        and eta_exponent >= 0.75
    )
    checks = {
        "all_targeted_event_contracts_pass": all_contracts_pass,
        "event_order_stable": order_stable,
        "event_count_complete": event_count_complete,
        "minimum_gap_scaling_exponent": gap_exponent,
        "maximum_eta_scaling_exponent": eta_exponent,
        "maximum_event_coordinate_shift": max(coordinate_shifts),
        "event_merger_coscaling_rejected": co_scaling_rejected,
        "state_evaluation_count": sum(
            int(row["root_iteration_count"]) for row in rows
        ),
    }
    atomic_json(
        SCAN_STATUS,
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "state": "EVENT_SCAN_COMPLETE",
            "completed_rung_count": len(EPSILON_VALUES),
            "completed_event_count": len(rows),
            "cache_signature": cache_signature,
            "checks": checks,
            "updated_utc": utc_now(),
        },
    )
    return rows, summaries, checks


def helmert_contrast(count: int) -> np.ndarray:
    matrix = np.zeros((count - 1, count), dtype=float)
    for row in range(count - 1):
        scale = math.sqrt((row + 1) * (row + 2))
        matrix[row, : row + 1] = 1.0 / scale
        matrix[row, row + 1] = -(row + 1) / scale
    return matrix


def contrast_basis(model_id: str, epsilon: np.ndarray) -> np.ndarray:
    logarithm = np.log(epsilon / EPSILON_REFERENCE)
    columns: dict[str, tuple[np.ndarray, ...]] = {
        "R1_ANALYTIC_LINEAR": (epsilon,),
        "R2_ANALYTIC_QUADRATIC": (epsilon, epsilon**2),
        "R3_TRANSVERSE_ENDPOINT_LOG": (epsilon, epsilon * logarithm),
        "R4_ENDPOINT_LOG_PLUS_E2": (
            epsilon,
            epsilon * logarithm,
            epsilon**2,
        ),
        "R5_FOLD_SQRT_STRESS": (np.sqrt(epsilon), epsilon),
    }
    return np.column_stack(columns[model_id])


def d2_contrast_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    ladder_path = (
        POST
        / "source-intake"
        / "functional_rg"
        / "5327"
        / "D2_midpoint_finite_regulator_ladder.csv"
    )
    ladder = sorted(read_csv(ladder_path), key=lambda row: float(row["epsilon"]))
    epsilon = np.asarray([float(row["epsilon"]) for row in ladder], dtype=float)
    values = np.asarray(
        [
            complex(
                float(row["fixed_decay_integral_real"]),
                float(row["fixed_decay_integral_imaginary"]),
            )
            for row in ladder
        ]
    )
    bounds = np.asarray(
        [float(row["fixed_decay_error_absolute_conservative"]) for row in ladder]
    )
    contrast = helmert_contrast(len(ladder))
    common_annihilation = float(np.max(np.abs(contrast @ np.ones(len(ladder)))))
    orthonormality_error = float(
        np.max(np.abs(contrast @ contrast.T - np.eye(len(ladder) - 1)))
    )
    contrast_values = contrast @ values
    contrast_bound_rows = np.abs(contrast) @ bounds
    conservative_contrast_bound = float(np.linalg.norm(contrast_bound_rows))
    rows: list[dict[str, Any]] = []
    for model_id in (
        "R1_ANALYTIC_LINEAR",
        "R2_ANALYTIC_QUADRATIC",
        "R3_TRANSVERSE_ENDPOINT_LOG",
        "R4_ENDPOINT_LOG_PLUS_E2",
        "R5_FOLD_SQRT_STRESS",
    ):
        basis = contrast_basis(model_id, epsilon)
        design = contrast @ basis
        coefficients, _, rank, singular_values = np.linalg.lstsq(
            design, contrast_values, rcond=None
        )
        residual = contrast_values - design @ coefficients
        residual_norm = float(np.linalg.norm(residual))
        condition = float(singular_values[0] / singular_values[-1])
        point_intercepts = values - basis @ coefficients
        intercept = complex(np.mean(point_intercepts))
        intercept_spread = float(np.max(np.abs(point_intercepts - intercept)))
        rows.append(
            {
                "model_id": model_id,
                "basis_column_count": basis.shape[1],
                "contrast_row_count": contrast.shape[0],
                "contrast_design_rank": int(rank),
                "contrast_design_condition_number": condition,
                "contrast_design_singular_values": "|".join(
                    f"{value:.17g}" for value in singular_values
                ),
                "contrast_residual_norm": residual_norm,
                "conservative_contrast_bound": conservative_contrast_bound,
                "residual_over_conservative_bound": residual_norm
                / conservative_contrast_bound,
                "compatible_with_conservative_D2_errors": residual_norm
                <= conservative_contrast_bound,
                "zero_intercept_real": intercept.real,
                "zero_intercept_imaginary": intercept.imag,
                "zero_intercept_magnitude": abs(intercept),
                "maximum_point_intercept_spread": intercept_spread,
                "constant_channel_annihilation_error": common_annihilation,
                "contrast_orthonormality_error": orthonormality_error,
                "role": (
                    "DERIVED_D2_NORMAL_FORM_DIAGNOSTIC"
                    if model_id == "R3_TRANSVERSE_ENDPOINT_LOG"
                    else "COMPARISON_ONLY"
                ),
                "source_path": str(ladder_path),
                **no_claims(),
            }
        )
    compatible_count = sum(
        bool(row["compatible_with_conservative_D2_errors"]) for row in rows
    )
    reference = next(
        row for row in rows if row["model_id"] == "R3_TRANSVERSE_ENDPOINT_LOG"
    )
    checks = {
        "constant_channel_annihilation_error": common_annihilation,
        "contrast_orthonormality_error": orthonormality_error,
        "compatible_model_count": compatible_count,
        "reference_model_residual_over_bound": reference[
            "residual_over_conservative_bound"
        ],
        "reference_model_full_rank": reference["contrast_design_rank"]
        == reference["basis_column_count"],
        "data_select_unique_remainder_family": compatible_count == 1,
    }
    return rows, checks


def readiness_rows() -> list[dict[str, Any]]:
    d4_result_path = (
        POST
        / "source-intake"
        / "functional_rg"
        / "5334"
        / "E0025"
        / "D4_outer_event_aligned_E0025_result.json"
    )
    d4_result = json.loads(d4_result_path.read_text(encoding="utf-8"))
    d4_accepted = int(
        bool(d4_result.get("finite_regulator_fixed_decay_integral_accepted", False))
    )
    return [
        {
            "arena": "D2_MID",
            "accepted_regulator_rung_count": 7,
            "minimum_rungs_for_overdetermined_two_mode_contrast": 4,
            "contrast_executed": True,
            "status": "READY_AND_EXECUTED_AS_METHOD_CHECK",
            "physical_mass_interpretation_allowed": False,
            **no_claims(),
        },
        {
            "arena": "D4_OUTER",
            "accepted_regulator_rung_count": d4_accepted,
            "minimum_rungs_for_overdetermined_two_mode_contrast": 4,
            "contrast_executed": False,
            "status": "BLOCKED_UNTIL_AT_LEAST_FOUR_D4_RUNGS_ARE_ACCEPTED",
            "physical_mass_interpretation_allowed": False,
            **no_claims(),
        },
    ]


def incremental_value_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_feature": "fold double scaling",
            "incremental_use": "defines eta=regulator contact width/local event gap and distinguishes a fixed-topology limit from an event-merger co-scaling path",
            "parent_claim_added": False,
            "q_derived": False,
            **no_claims(),
        },
        {
            "source_feature": "orthogonal mass contrasts",
            "incremental_use": "becomes a computational regulator contrast that removes the common intercept and audits remainder rank",
            "parent_claim_added": False,
            "q_derived": False,
            **no_claims(),
        },
        {
            "source_feature": "clock gradient plus cycle residual",
            "incremental_use": "future finite benchmark for the existing exact/coexact local flux gate; it does not prove no swirl",
            "parent_claim_added": False,
            "q_derived": False,
            **no_claims(),
        },
        {
            "source_feature": "worldline and mixed-history inverse",
            "incremental_use": "future observability design for sharp events, continuous memory and boundary equivalence classes",
            "parent_claim_added": False,
            "q_derived": False,
            **no_claims(),
        },
        {
            "source_feature": "acquisition bandwidth exponents",
            "incremental_use": "retained only as measurement-resource laws and explicitly barred from identification with q_target",
            "parent_claim_added": False,
            "q_derived": False,
            **no_claims(),
        },
    ]


def route_rows(double_scaling_passes: bool) -> list[dict[str, Any]]:
    return [
        {
            "question": "Does adaptive panel motion itself change the physical regulator limit?",
            "answer": "NO_IF_THE_COMPLETE_FIXED_DOMAIN_IS_RETAINED",
            "reason": "partition boundaries are numerical; the source-owned plan covers the complete angular domain",
            "claim_promoted": False,
        },
        {
            "question": "Does the sampled D4 event geometry follow an event-merger co-scaling path?",
            "answer": "NO" if double_scaling_passes else "NOT_YET_EXCLUDED",
            "reason": "targeted seven-regulator event scan and eta scaling gate",
            "claim_promoted": False,
        },
        {
            "question": "Does the D2 contrast select a unique zero-limit remainder family?",
            "answer": "NO__TOPOLOGY_REMAINS_THE_SELECTOR",
            "reason": "the conservative numerical disks admit multiple contrast bases",
            "claim_promoted": False,
        },
        {
            "question": "What is the next executable action?",
            "answer": (
                "RESUME_5334_D4_E0025_SAVED_SHARDS"
                if double_scaling_passes
                else "HOLD_5334__REFINE_D4_EVENT_LIMIT_EVIDENCE"
            ),
            "reason": "only resume the expensive integral after the limit-geometry preflight passes",
            "claim_promoted": False,
        },
    ]


def run() -> dict[str, Any]:
    formal_start = formal_inventory_digest()
    sources, sources_locked = source_rows()
    parent_hashes_before = {
        relative: digest(POST / relative) for relative in LOCAL_SOURCE_LOCKS
    }
    fold_rows, fold_checks = fold_double_scaling_rows()
    d4_rows, d4_summaries, d4_checks = d4_targeted_event_scan()
    d2_rows, d2_checks = d2_contrast_rows()
    readiness = readiness_rows()
    incremental = incremental_value_rows()
    routes = route_rows(bool(d4_checks["event_merger_coscaling_rejected"]))
    parent_hashes_after = {
        relative: digest(POST / relative) for relative in LOCAL_SOURCE_LOCKS
    }

    outputs = {
        "source_register": OUT / "source_register.csv",
        "fold_reference": OUT / "fold_double_scaling_reference.csv",
        "d4_event_scan": OUT / "D4_targeted_event_regulator_scan.csv",
        "d4_summary": OUT / "D4_regulator_double_scaling_summary.csv",
        "d2_contrast": OUT / "D2_regulator_contrast_svd.csv",
        "readiness": OUT / "regulator_contrast_readiness.csv",
        "incremental_value": OUT / "maths_exploration_incremental_value.csv",
        "route": OUT / "route_decision.csv",
    }
    payloads = {
        "source_register": sources,
        "fold_reference": fold_rows,
        "d4_event_scan": d4_rows,
        "d4_summary": d4_summaries,
        "d2_contrast": d2_rows,
        "readiness": readiness,
        "incremental_value": incremental,
        "route": routes,
    }
    for key, path in outputs.items():
        write_csv(path, payloads[key])

    formal_end = formal_inventory_digest()
    parent_unchanged = parent_hashes_before == parent_hashes_after
    d4_contrast_row = next(row for row in readiness if row["arena"] == "D4_OUTER")
    checks = [
        validation_row("all_source_locks_pass", sources_locked, f"rows={len(sources)}"),
        validation_row(
            "formalization_workbench_unchanged",
            formal_start == formal_end == FORMAL_DIGEST,
            f"start={formal_start}; end={formal_end}",
        ),
        validation_row(
            "parent_checkpoint_inputs_unchanged_by_targeted_scan",
            parent_unchanged,
            f"locked_files={len(parent_hashes_before)}",
        ),
        validation_row(
            "source_fold_fixed_mass_and_coscaling_limits_reproduced",
            abs(fold_checks["fixed_mass_exponent"] - 2.0) <= 2.0e-4
            and abs(fold_checks["fixed_xi_exponent"]) <= 1.0e-10,
            json.dumps(fold_checks, sort_keys=True),
        ),
        validation_row(
            "D4_targeted_scan_covers_seven_regulators_and_eight_events",
            len(d4_rows) == len(EPSILON_VALUES) * EXPECTED_EVENT_COUNT,
            f"rows={len(d4_rows)}",
        ),
        validation_row(
            "all_D4_targeted_contacts_are_transverse",
            bool(d4_checks["all_targeted_event_contracts_pass"]),
            json.dumps(d4_checks, sort_keys=True),
        ),
        validation_row(
            "D4_event_order_and_count_are_stable",
            bool(d4_checks["event_order_stable"])
            and bool(d4_checks["event_count_complete"]),
            json.dumps(d4_checks, sort_keys=True),
        ),
        validation_row(
            "D4_event_merger_coscaling_path_rejected_on_sampled_ladder",
            bool(d4_checks["event_merger_coscaling_rejected"]),
            json.dumps(d4_checks, sort_keys=True),
        ),
        validation_row(
            "D2_contrast_is_orthonormal_and_removes_common_channel",
            d2_checks["constant_channel_annihilation_error"] <= 1.0e-14
            and d2_checks["contrast_orthonormality_error"] <= 1.0e-14,
            json.dumps(d2_checks, sort_keys=True),
        ),
        validation_row(
            "D2_derived_endpoint_log_family_survives_contrast_gate",
            bool(d2_checks["reference_model_full_rank"])
            and float(d2_checks["reference_model_residual_over_bound"]) <= 1.0,
            json.dumps(d2_checks, sort_keys=True),
        ),
        validation_row(
            "contrast_does_not_overclaim_unique_remainder_selection",
            not bool(d2_checks["data_select_unique_remainder_family"]),
            f"compatible_models={d2_checks['compatible_model_count']}",
        ),
        validation_row(
            "D4_contrast_remains_blocked_without_four_accepted_rungs",
            not bool(d4_contrast_row["contrast_executed"])
            and int(d4_contrast_row["accepted_regulator_rung_count"]) < 4,
            str(d4_contrast_row),
        ),
        validation_row(
            "no_source_feature_is_mistaken_for_q_or_parent_ownership",
            all(
                not bool(row["q_derived"])
                and not bool(row["parent_claim_added"])
                for row in incremental
            ),
            f"rows={len(incremental)}",
        ),
        validation_row(
            "no_claim_promoted",
            all(not bool(row["claim_promoted"]) for row in routes)
            and all(not any(bool(row[field]) for field in CLAIM_FIELDS) for row in d4_rows),
            f"route_rows={len(routes)}",
        ),
        validation_row(
            "route_resumes_saved_5334_shards_only_after_preflight",
            routes[-1]["answer"] == "RESUME_5334_D4_E0025_SAVED_SHARDS",
            routes[-1]["reason"],
        ),
    ]
    write_csv(VALIDATION, checks)
    validation = read_csv(VALIDATION)
    passed = bool(validation) and all(parse_bool(row["passed"]) for row in validation)
    result = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "decision": (
            "D4_EVENT_GEOMETRY_FIXED_TOPOLOGY_LIMIT_SUPPORTED__"
            "EVENT_MERGER_COSCALING_REJECTED_ON_SEVEN_TARGETED_REGULATORS__"
            "D2_CONTRAST_METHOD_VALID_BUT_NONSELECTIVE__"
            "RESUME_5334_SAVED_SHARDS"
            if passed
            else "CHECKPOINT_5337_VALIDATION_BLOCKED"
        ),
        "fold_checks": fold_checks,
        "D4_double_scaling_checks": d4_checks,
        "D2_contrast_checks": d2_checks,
        "output_row_counts": {
            key: len(read_csv(path)) for key, path in outputs.items()
        },
        "validation_rows": len(validation),
        "validation_passed": passed,
        "formalization_workbench_reference_digest": FORMAL_DIGEST,
        "formalization_workbench_start_digest": formal_start,
        "formalization_workbench_end_digest": formal_end,
        "formalization_workbench_modified_file_count": (
            0 if formal_start == formal_end == FORMAL_DIGEST else -1
        ),
        "parent_checkpoint_inputs_unchanged": parent_unchanged,
        "claim_flags": {field: False for field in CLAIM_FIELDS},
        "valid_for_new_parent_ownership": False,
        "valid_for_derived_q": False,
        "valid_for_state_preparation": False,
        "valid_for_galaxy_claim": False,
        "next_action": (
            ".\\.venv-score\\Scripts\\python.exe "
            ".\\scripts\\Y5_R2FR_5334_D4_outer_regulator_ladder_controller.py "
            "--mode refinement-run --max-runtime-hours 2"
            if passed
            else "REFINE_CHECKPOINT_5337_D4_EVENT_LIMIT_EVIDENCE"
        ),
    }
    atomic_json(RESULT, result)
    atomic_json(
        SCAN_STATUS,
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "state": "CHECKPOINT_COMPLETE" if passed else "VALIDATION_BLOCKED",
            "validation_passed": passed,
            "decision": result["decision"],
            "updated_utc": utc_now(),
        },
    )
    if not passed:
        raise RuntimeError("checkpoint 5337 validation failed")
    return result


def validate_existing() -> dict[str, Any]:
    required = [
        RESULT,
        VALIDATION,
        OUT / "source_register.csv",
        OUT / "fold_double_scaling_reference.csv",
        OUT / "D4_targeted_event_regulator_scan.csv",
        OUT / "D4_regulator_double_scaling_summary.csv",
        OUT / "D2_regulator_contrast_svd.csv",
        OUT / "regulator_contrast_readiness.csv",
        OUT / "maths_exploration_incremental_value.csv",
        OUT / "route_decision.csv",
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError("; ".join(missing))
    validation = read_csv(VALIDATION)
    if not validation or not all(parse_bool(row["passed"]) for row in validation):
        raise RuntimeError("stored validation has a failed gate")
    if formal_inventory_digest() != FORMAL_DIGEST:
        raise RuntimeError("formalization-workbench digest changed")
    for relative, expected in LOCAL_SOURCE_LOCKS.items():
        if digest(POST / relative) != expected:
            raise RuntimeError(f"source lock changed: {relative}")
    return json.loads(RESULT.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("run", "validate"), default="run")
    arguments = parser.parse_args()
    try:
        result = run() if arguments.mode == "run" else validate_existing()
    except Exception as error:
        atomic_json(
            SCAN_STATUS,
            {
                "checkpoint": CHECKPOINT,
                "marker": MARKER,
                "state": "FAILED",
                "error_type": type(error).__name__,
                "error": str(error),
                "traceback": traceback.format_exc(),
                "updated_utc": utc_now(),
            },
        )
        raise
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()

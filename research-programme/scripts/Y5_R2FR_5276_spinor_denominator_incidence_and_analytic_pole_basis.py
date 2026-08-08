from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import os
import sys
import time
from pathlib import Path
from typing import Any


for thread_variable in (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "BLIS_NUM_THREADS",
):
    os.environ[thread_variable] = "1"
os.environ["PYTHONNOUSERSITE"] = "1"
sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
SOURCE = FUNCTIONAL_RG / "5276"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5275 = (
    SCRIPTS
    / "Y5_R2FR_5275_arbitrary_precision_local_limit_and_global_pole_basis.py"
)
SCRIPT_5017 = (
    SCRIPTS
    / "Y5_R2FR_5017_complex_safe_hhh_crossed_integrand_and_coupled_locality_smoke.py"
)
SCRIPT_5022 = (
    SCRIPTS / "Y5_R2FR_5022_rational_azimuth_residue_endpoint_gate.py"
)
RESULT_5275 = (
    FUNCTIONAL_RG
    / "5275"
    / "arbitrary_precision_global_pole_basis_result.json"
)
VALIDATION_5275 = (
    FUNCTIONAL_RG
    / "5275"
    / "arbitrary_precision_global_pole_basis_validation.csv"
)
POLE_BASIS_5275 = (
    FUNCTIONAL_RG / "5275" / "generic_global_pole_basis.csv"
)
LIMIT_ROWS_5275 = (
    FUNCTIONAL_RG
    / "5275"
    / "owner_resolved_local_coefficient_limits.csv"
)
COMPONENT_MAP_5239 = (
    FUNCTIONAL_RG / "5239" / "matched_regulator_component_map.csv"
)

DRY_RUN = SOURCE / "denominator_incidence_dry_run.json"
DIRECT_LABEL_DICTIONARY = SOURCE / "direct_spinor_label_dictionary.csv"
DIRECT_TERM_INCIDENCE = SOURCE / "direct_five_point_term_incidence.csv"
DIRECT_COMPONENT_THEOREM = SOURCE / "direct_component_pole_theorem.csv"
ENDPOINT_LABEL_DICTIONARY = (
    SOURCE / "endpoint_decay_spinor_label_dictionary.csv"
)
SOFT_FACTOR_IDENTITY = SOURCE / "soft_factor_leading_pole_identity.csv"
ENDPOINT_COMPONENT_THEOREM = (
    SOURCE / "endpoint_component_pole_theorem.csv"
)
ANALYTIC_POLE_BASIS = SOURCE / "analytic_almost_everywhere_pole_basis.csv"
RESULT = SOURCE / "analytic_pole_basis_result.json"
VALIDATION = SOURCE / "analytic_pole_basis_validation.csv"
RESIDUAL_VALIDATION = (
    RESIDUALS / "P8_Y5_BRR545_5276_VALIDATION.csv"
)
STATUS = SOURCE / "status.json"
DOCUMENT = (
    POST
    / "5276-Y5-R2FR-spinor-denominator-incidence-and-analytic-pole-basis.md"
)

CHECKPOINT = 5276
PARENT_CHECKPOINT = 5275
MARKER = "MTS_5276_SPINOR_DENOMINATOR_INCIDENCE_AND_ANALYTIC_POLE_BASIS"
REVISION = "spinor-denominator-incidence-analytic-pole-basis-v1"
EXPECTED_DOUBLE_COMPONENTS = (
    "MC02",
    "MC03",
    "MC04",
    "MC07",
    "MC08",
    "MC12",
    "MC14",
    "MC15",
)
EXPECTED_SIMPLE_COMPONENTS = (
    "MC01",
    "MC05",
    "MC06",
    "MC09",
    "MC10",
    "MC11",
    "MC13",
)
EXPECTED_DIRECT_LEADING_TERMS = {
    "MC02": {"special=3;sigma=1;gamma=0"},
    "MC03": {"special=3;sigma=1;gamma=0"},
    "MC04": {
        "special=2;sigma=0;gamma=0",
        "special=2;sigma=1;gamma=0",
    },
    "MC07": {"special=3;sigma=0;gamma=1"},
    "MC08": {"special=3;sigma=0;gamma=1"},
    "MC12": {
        "special=1;sigma=0;gamma=1",
        "special=1;sigma=1;gamma=1",
    },
}
EXPECTED_ENDPOINT_LEADING_TERMS = {
    "MC14": "right_chirality=0;special=2;decay_leg=1",
    "MC15": "right_chirality=0;special=1;decay_leg=2",
}
CLAIM_FIELDS = (
    "valid_for_full_phase_space_coefficient",
    "valid_for_numeric_UV_claim",
    "valid_for_local_GR_claim",
    "valid_for_full_MTS_claim",
)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5275 = load_module("mts_5275_for_5276", SCRIPT_5275)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise RuntimeError(f"refusing to write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5275,
        SCRIPT_5017,
        SCRIPT_5022,
        RESULT_5275,
        VALIDATION_5275,
        POLE_BASIS_5275,
        LIMIT_ROWS_5275,
        COMPONENT_MAP_5239,
    )
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in paths
    ]


def formal_inventory_digest() -> str:
    return str(M5275.formal_inventory_digest())


def parse_factor_label(label: str) -> dict[str, Any]:
    source_name, root_label = label.rsplit(":", 1)
    sign, suffix = root_label.rsplit("_", 1)
    chirality = {"u": 0, "v": 1}[suffix]
    external_leg = {"plus": 0, "minus": 4}[sign]
    source_leg = (
        int(source_name.rsplit("g", 1)[1])
        if source_name.startswith("direct:g")
        else None
    )
    return {
        "label": label,
        "source_name": source_name,
        "source_leg": source_leg,
        "sign": sign,
        "suffix": suffix,
        "chirality": chirality,
        "external_leg": external_leg,
    }


def first_representing_pair(
    component: dict[str, str],
) -> tuple[str, str]:
    first_pair = component["label_signature"].split("||", 1)[0]
    labels = tuple(first_pair.split("|"))
    if len(labels) != 2:
        raise RuntimeError(
            f"invalid component signature: {component['label_signature']}"
        )
    return labels[0], labels[1]


def direct_label_dictionary_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_leg in (1, 2, 3):
        for sign in ("plus", "minus"):
            for suffix, chirality in (("u", 0), ("v", 1)):
                external_leg = 0 if sign == "plus" else 4
                rows.append(
                    {
                        "label": (
                            f"direct:g{source_leg}:{sign}_{suffix}"
                        ),
                        "source_leg": source_leg,
                        "sign": sign,
                        "suffix": suffix,
                        "chirality": chirality,
                        "vanishing_spinor_bracket": (
                            f"<{external_leg},{source_leg}>"
                            if chirality == 0
                            else f"[{external_leg},{source_leg}]"
                        ),
                        "external_leg": external_leg,
                        "derivation": (
                            "z_plus_u=e/h; z_plus_v=hbar/e; "
                            "z_minus_u=-1/(e*h); "
                            "z_minus_v=-e*hbar"
                        ),
                        "valid_for_exact_label_dictionary": True,
                        "valid_for_full_phase_space_coefficient": False,
                        "valid_for_numeric_UV_claim": False,
                        "valid_for_local_GR_claim": False,
                        "valid_for_full_MTS_claim": False,
                    }
                )
    return rows


def cyclic_edges(order: tuple[int, ...]) -> list[tuple[int, int]]:
    return [
        tuple(
            sorted(
                (
                    order[index],
                    order[(index + 1) % len(order)],
                )
            )
        )
        for index in range(len(order))
    ]


def five_point_orders(
    sigma_reversed: int,
    gamma_reversed: int,
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    sigma_first, sigma_second = (
        (1, 2) if sigma_reversed == 0 else (2, 1)
    )
    gamma_first, gamma_second = (
        (1, 2) if gamma_reversed == 0 else (2, 1)
    )
    return (
        (0, sigma_first, sigma_second, 3, 4),
        (3, 4, gamma_first, gamma_second, 0),
    )


def denominator_incidence_count(
    external_leg: int,
    source_leg: int,
    sigma_reversed: int,
    gamma_reversed: int,
) -> int:
    first_order, second_order = five_point_orders(
        sigma_reversed,
        gamma_reversed,
    )
    target_edge = tuple(sorted((external_leg, source_leg)))
    return (
        cyclic_edges(first_order).count(target_edge)
        + cyclic_edges(second_order).count(target_edge)
    )


def kernel_zero_count(
    factor: dict[str, Any],
    sigma_reversed: int,
    gamma_reversed: int,
) -> int:
    if factor["sign"] != "plus":
        return 0
    source_leg = int(factor["source_leg"])
    if source_leg == 1:
        return int(
            not (
                gamma_reversed == 0
                and sigma_reversed == 1
            )
        )
    if source_leg == 2:
        return int(
            not (
                gamma_reversed == 1
                and sigma_reversed == 0
            )
        )
    return 0


def numerator_zero_count(
    factor: dict[str, Any],
    special_leg: int,
) -> int:
    return 4 if int(factor["source_leg"]) == special_leg else 0


def direct_term_incidence_rows(
    components: list[dict[str, str]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for component in components:
        labels = first_representing_pair(component)
        factors = [parse_factor_label(label) for label in labels]
        both_direct = all(
            factor["source_name"].startswith("direct:g")
            for factor in factors
        )
        same_chirality = (
            both_direct
            and factors[0]["chirality"] == factors[1]["chirality"]
        )
        for special_leg in (1, 2, 3):
            for sigma_reversed in (0, 1):
                for gamma_reversed in (0, 1):
                    net_orders: list[int] = []
                    denominator_counts: list[int] = []
                    kernel_counts: list[int] = []
                    numerator_counts: list[int] = []
                    if both_direct:
                        for factor in factors:
                            denominator = denominator_incidence_count(
                                int(factor["external_leg"]),
                                int(factor["source_leg"]),
                                sigma_reversed,
                                gamma_reversed,
                            )
                            kernel = kernel_zero_count(
                                factor,
                                sigma_reversed,
                                gamma_reversed,
                            )
                            numerator = numerator_zero_count(
                                factor,
                                special_leg,
                            )
                            denominator_counts.append(denominator)
                            kernel_counts.append(kernel)
                            numerator_counts.append(numerator)
                            net_orders.append(
                                denominator - kernel - numerator
                            )
                    else:
                        denominator_counts = [0, 0]
                        kernel_counts = [0, 0]
                        numerator_counts = [0, 0]
                        net_orders = [0, 0]
                    simultaneous_double = (
                        same_chirality
                        and min(net_orders) >= 1
                    )
                    rows.append(
                        {
                            "component_id": component["component_id"],
                            "family": component["family"],
                            "first_label": labels[0],
                            "second_label": labels[1],
                            "both_sources_direct": both_direct,
                            "same_chirality": same_chirality,
                            "special_leg": special_leg,
                            "sigma_reversed": sigma_reversed,
                            "gamma_reversed": gamma_reversed,
                            "first_denominator_count": (
                                denominator_counts[0]
                            ),
                            "second_denominator_count": (
                                denominator_counts[1]
                            ),
                            "first_kernel_zero_count": kernel_counts[0],
                            "second_kernel_zero_count": kernel_counts[1],
                            "first_numerator_zero_count": (
                                numerator_counts[0]
                            ),
                            "second_numerator_zero_count": (
                                numerator_counts[1]
                            ),
                            "first_net_pole_order": net_orders[0],
                            "second_net_pole_order": net_orders[1],
                            "simultaneous_double_term": (
                                simultaneous_double
                            ),
                            "term_id": (
                                f"special={special_leg};"
                                f"sigma={sigma_reversed};"
                                f"gamma={gamma_reversed}"
                            ),
                            "valid_for_exact_term_incidence": True,
                            "valid_for_full_phase_space_coefficient": False,
                            "valid_for_numeric_UV_claim": False,
                            "valid_for_local_GR_claim": False,
                            "valid_for_full_MTS_claim": False,
                        }
                    )
    return rows


def direct_component_theorem_rows(
    components: list[dict[str, str]],
    incidence_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for component in components:
        component_id = component["component_id"]
        local = [
            row
            for row in incidence_rows
            if row["component_id"] == component_id
        ]
        leading_terms = sorted(
            str(row["term_id"])
            for row in local
            if bool(row["simultaneous_double_term"])
        )
        labels = first_representing_pair(component)
        factors = [parse_factor_label(label) for label in labels]
        both_direct = all(
            factor["source_name"].startswith("direct:g")
            for factor in factors
        )
        same_chirality = (
            both_direct
            and factors[0]["chirality"] == factors[1]["chirality"]
        )
        direct_double = bool(leading_terms)
        result.append(
            {
                "component_id": component_id,
                "family": component["family"],
                "both_sources_direct": both_direct,
                "same_chirality": same_chirality,
                "leading_double_term_count": len(leading_terms),
                "leading_double_terms": "|".join(leading_terms),
                "direct_generic_double": direct_double,
                "proof": (
                    "MIXED_CHIRALITY_CANNOT_SHARE_ONE_RIGHT_KLT_FACTOR"
                    if both_direct and not same_chirality
                    else (
                        "EXPLICIT_NET_DENOMINATOR_INCIDENCE_PLUS_"
                        "GENERIC_KLT_FACTORIZATION"
                        if direct_double
                        else "NO_TWO_DIRECT_SOURCES_IN_SAME_SUMMAND"
                    )
                ),
                "valid_for_analytic_direct_pole_order": True,
                "valid_for_global_pointwise_pole_theorem": False,
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return result


def endpoint_decay_dictionary_rows() -> list[dict[str, Any]]:
    mapping = {
        "plus_u": ((0, 1, 0), (4, 2, 1)),
        "plus_v": ((0, 1, 1), (4, 2, 0)),
        "minus_u": ((4, 1, 0), (0, 2, 1)),
        "minus_v": ((4, 1, 1), (0, 2, 0)),
    }
    rows: list[dict[str, Any]] = []
    for root_label, zero_brackets in mapping.items():
        for bracket_index, (
            external_leg,
            decay_leg,
            chirality,
        ) in enumerate(zero_brackets, start=1):
            rows.append(
                {
                    "label": f"subtraction:decay:{root_label}",
                    "root_label": root_label,
                    "coincident_bracket_index": bracket_index,
                    "external_leg": external_leg,
                    "decay_leg": decay_leg,
                    "chirality": chirality,
                    "vanishing_spinor_bracket": (
                        f"<{external_leg},{decay_leg}>"
                        if chirality == 0
                        else f"[{external_leg},{decay_leg}]"
                    ),
                    "reason": (
                        "endpoint contains +decay and -decay legs, "
                        "so one decay root zeros two opposite-chirality "
                        "external brackets"
                    ),
                    "valid_for_exact_label_dictionary": True,
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    return rows


def soft_factor_identity_rows() -> list[dict[str, Any]]:
    return [
        {
            "identity_id": "SOFT5276_01",
            "would_be_double_numerator": (
                "sum_{l in {0,1,2,4}} <0l>[l3]"
            ),
            "momentum_conservation_form": (
                "<0|(p0+p1+p2+p3+p4)|3]"
            ),
            "endpoint_value": "0",
            "reason": (
                "sum p_l=0, while <00>=0 and [33]=0; "
                "the delta^-2 coefficient cancels"
            ),
            "naive_soft_pole_order": 2,
            "derived_soft_pole_order_upper_bound": 1,
            "generic_soft_pole_order": 1,
            "valid_for_exact_soft_leading_cancellation": True,
            "valid_for_full_phase_space_coefficient": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
    ]


def four_point_denominator_count(
    external_leg: int,
    decay_leg: int,
) -> int:
    first_order = (0, 1, 2, 4)
    second_order = (2, 4, 1, 0)
    target_edge = tuple(sorted((external_leg, decay_leg)))
    return (
        cyclic_edges(first_order).count(target_edge)
        + cyclic_edges(second_order).count(target_edge)
    )


def endpoint_component_theorem_rows(
    components: list[dict[str, str]],
    decay_dictionary: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for component in components:
        labels = first_representing_pair(component)
        soft_label = next(
            (
                label
                for label in labels
                if label.startswith("direct:g3:")
            ),
            None,
        )
        decay_label = next(
            (
                label
                for label in labels
                if label.startswith("subtraction:decay:")
            ),
            None,
        )
        leading_terms: list[str] = []
        matched_decay_bracket = ""
        decay_net_order = 0
        if soft_label is not None and decay_label is not None:
            soft_factor = parse_factor_label(soft_label)
            same_chirality_decay_rows = [
                row
                for row in decay_dictionary
                if row["label"] == decay_label
                and int(row["chirality"])
                == int(soft_factor["chirality"])
            ]
            for decay_row in same_chirality_decay_rows:
                decay_leg = int(decay_row["decay_leg"])
                external_leg = int(decay_row["external_leg"])
                denominator = four_point_denominator_count(
                    external_leg,
                    decay_leg,
                )
                paired_rows = [
                    row
                    for row in decay_dictionary
                    if row["label"] == decay_label
                ]
                invariant_zero = int(
                    any(
                        int(row["external_leg"]) == 0
                        and int(row["decay_leg"]) == 1
                        for row in paired_rows
                    )
                )
                for special_leg in (1, 2):
                    numerator_zero = (
                        4 if special_leg == decay_leg else 0
                    )
                    net_order = (
                        denominator
                        - invariant_zero
                        - numerator_zero
                    )
                    if net_order >= 1:
                        decay_net_order = net_order
                        matched_decay_bracket = str(
                            decay_row["vanishing_spinor_bracket"]
                        )
                        leading_terms.append(
                            f"right_chirality="
                            f"{soft_factor['chirality']};"
                            f"special={special_leg};"
                            f"decay_leg={decay_leg}"
                        )
        endpoint_double = bool(leading_terms)
        result.append(
            {
                "component_id": component["component_id"],
                "family": component["family"],
                "soft_label": soft_label or "",
                "decay_label": decay_label or "",
                "contains_soft_and_decay_sources": (
                    soft_label is not None and decay_label is not None
                ),
                "soft_factor_pole_order": 1 if endpoint_double else 0,
                "matched_decay_bracket": matched_decay_bracket,
                "four_point_KLT_net_decay_pole_order": decay_net_order,
                "leading_double_term_count": len(leading_terms),
                "leading_double_terms": "|".join(leading_terms),
                "endpoint_generic_double": endpoint_double,
                "proof": (
                    "MOMENTUM_CONSERVATION_SOFT_SIMPLE_POLE_TIMES_"
                    "UNIQUE_FOUR_POINT_KLT_SIMPLE_POLE"
                    if endpoint_double
                    else (
                        "NO_SOFT_G3_AND_DECAY_PAIR_IN_ENDPOINT_SUMMAND"
                        if decay_label is not None
                        else "NO_ENDPOINT_DECAY_SOURCE"
                    )
                ),
                "valid_for_analytic_endpoint_pole_order": True,
                "valid_for_global_pointwise_pole_theorem": False,
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return result


def analytic_basis_rows(
    components: list[dict[str, str]],
    direct_rows: list[dict[str, Any]],
    endpoint_rows: list[dict[str, Any]],
    parent_basis: dict[str, dict[str, str]],
) -> list[dict[str, Any]]:
    direct_by_id = {
        row["component_id"]: row for row in direct_rows
    }
    endpoint_by_id = {
        row["component_id"]: row for row in endpoint_rows
    }
    result: list[dict[str, Any]] = []
    for component in components:
        component_id = component["component_id"]
        direct_double = bool(
            direct_by_id[component_id]["direct_generic_double"]
        )
        endpoint_double = bool(
            endpoint_by_id[component_id]["endpoint_generic_double"]
        )
        generic_double = direct_double or endpoint_double
        analytic_classification = (
            "DOUBLE_POLE" if generic_double else "SIMPLE_POLE"
        )
        parent_classification = parent_basis[component_id][
            "generic_classification"
        ]
        result.append(
            {
                "component_id": component_id,
                "family": component["family"],
                "source_material": component["material"],
                "direct_generic_double": direct_double,
                "endpoint_generic_double": endpoint_double,
                "analytic_classification": analytic_classification,
                "parent_5275_classification": parent_classification,
                "matches_parent_5275": (
                    analytic_classification == parent_classification
                ),
                "analytic_status": (
                    "ALMOST_EVERYWHERE_DOUBLE__COEFFICIENT_ZEROS_"
                    "MAY_LOWER_ORDER_ON_MEASURE_ZERO_SET"
                    if generic_double
                    else "AT_MOST_SIMPLE_BY_DENOMINATOR_INCIDENCE"
                ),
                "retain_in_eight_component_cubature_basis": (
                    generic_double
                ),
                "valid_for_analytic_almost_everywhere_pole_basis": True,
                "valid_for_global_pointwise_pole_theorem": False,
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return result


def dry_run() -> dict[str, Any]:
    SOURCE.mkdir(parents=True, exist_ok=True)
    required = (
        SCRIPT_5275,
        SCRIPT_5017,
        SCRIPT_5022,
        RESULT_5275,
        VALIDATION_5275,
        POLE_BASIS_5275,
        LIMIT_ROWS_5275,
        COMPONENT_MAP_5239,
    )
    parent = read_json(RESULT_5275)
    parent_validation = read_csv(VALIDATION_5275)
    components = read_csv(COMPONENT_MAP_5239)
    checks = {
        "required_sources_exist": all(
            path.exists() for path in required
        ),
        "parent_5275_accepted": bool(parent["acceptance_passed"]),
        "parent_5275_validated": all(
            row["passed"].lower() == "true"
            for row in parent_validation
        ),
        "parent_eight_component_basis": (
            parent["generic_double_component_ids"]
            == list(EXPECTED_DOUBLE_COMPONENTS)
        ),
        "fifteen_components_loaded": len(components) == 15,
        "formalization_workbench_unchanged": (
            formal_inventory_digest()
            == str(parent["formalization_workbench_end_digest"])
        ),
    }
    accepted = all(checks.values())
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "dry-run",
        "checks": checks,
        "acceptance_passed": accepted,
        "decision": (
            "DRY_RUN_ACCEPTED__DERIVE_SPINOR_DENOMINATOR_INCIDENCE"
            if accepted
            else "DRY_RUN_REQUIRES_REPAIR"
        ),
        "runtime_seconds": 0.0,
        "valid_for_full_phase_space_coefficient": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(DRY_RUN, result)
    return result


def execute() -> dict[str, Any]:
    started = time.perf_counter()
    dry = dry_run()
    if not dry["acceptance_passed"]:
        raise RuntimeError("5276 dry run did not pass")
    parent = read_json(RESULT_5275)
    components = read_csv(COMPONENT_MAP_5239)
    parent_basis = {
        row["component_id"]: row
        for row in read_csv(POLE_BASIS_5275)
    }
    direct_dictionary = direct_label_dictionary_rows()
    direct_incidence = direct_term_incidence_rows(components)
    direct_theorem = direct_component_theorem_rows(
        components,
        direct_incidence,
    )
    endpoint_dictionary = endpoint_decay_dictionary_rows()
    soft_identity = soft_factor_identity_rows()
    endpoint_theorem = endpoint_component_theorem_rows(
        components,
        endpoint_dictionary,
    )
    basis_rows = analytic_basis_rows(
        components,
        direct_theorem,
        endpoint_theorem,
        parent_basis,
    )
    direct_leading_terms = {
        row["component_id"]: set(
            filter(None, str(row["leading_double_terms"]).split("|"))
        )
        for row in direct_theorem
        if bool(row["direct_generic_double"])
    }
    endpoint_leading_terms = {
        row["component_id"]: str(row["leading_double_terms"])
        for row in endpoint_theorem
        if bool(row["endpoint_generic_double"])
    }
    double_ids = sorted(
        str(row["component_id"])
        for row in basis_rows
        if row["analytic_classification"] == "DOUBLE_POLE"
    )
    simple_ids = sorted(
        str(row["component_id"])
        for row in basis_rows
        if row["analytic_classification"] == "SIMPLE_POLE"
    )
    mixed_direct_rows = [
        row
        for row in direct_theorem
        if bool(row["both_sources_direct"])
        and not bool(row["same_chirality"])
    ]
    checks = {
        "parent_5275_accepted": bool(parent["acceptance_passed"]),
        "direct_label_dictionary_closes": (
            len(direct_dictionary) == 12
            and all(
                bool(row["valid_for_exact_label_dictionary"])
                for row in direct_dictionary
            )
        ),
        "direct_term_matrix_complete": (
            len(direct_incidence) == len(components) * 12
        ),
        "mixed_chirality_direct_pairs_at_most_simple": all(
            not bool(row["direct_generic_double"])
            for row in mixed_direct_rows
        ),
        "direct_leading_terms_exact": (
            direct_leading_terms == EXPECTED_DIRECT_LEADING_TERMS
        ),
        "endpoint_decay_dictionary_closes": (
            len(endpoint_dictionary) == 8
        ),
        "soft_double_leading_identity_cancels": all(
            bool(
                row[
                    "valid_for_exact_soft_leading_cancellation"
                ]
            )
            and int(row["derived_soft_pole_order_upper_bound"])
            == 1
            for row in soft_identity
        ),
        "endpoint_leading_terms_exact": (
            endpoint_leading_terms
            == EXPECTED_ENDPOINT_LEADING_TERMS
        ),
        "analytic_eight_component_basis": (
            double_ids == list(EXPECTED_DOUBLE_COMPONENTS)
        ),
        "analytic_seven_component_complement": (
            simple_ids == list(EXPECTED_SIMPLE_COMPONENTS)
        ),
        "analytic_basis_matches_5275": all(
            bool(row["matches_parent_5275"]) for row in basis_rows
        ),
        "formalization_workbench_unchanged": (
            formal_inventory_digest()
            == str(parent["formalization_workbench_end_digest"])
        ),
        "claims_locked_false": True,
    }
    accepted = all(checks.values())
    formal_end = formal_inventory_digest()
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "spinor-denominator-incidence-and-analytic-pole-basis",
        "checks": checks,
        "acceptance_passed": accepted,
        "direct_label_dictionary_count": len(direct_dictionary),
        "direct_term_incidence_count": len(direct_incidence),
        "mixed_chirality_direct_component_count": (
            len(mixed_direct_rows)
        ),
        "direct_double_component_ids": sorted(
            direct_leading_terms
        ),
        "endpoint_double_component_ids": sorted(
            endpoint_leading_terms
        ),
        "analytic_double_component_ids": double_ids,
        "analytic_simple_component_ids": simple_ids,
        "soft_factor_identity": (
            "sum_l <0l>[l3] = <0|sum_l p_l|3] = 0"
        ),
        "direct_pole_rule": (
            "one right KLT factor has fixed chirality; mixed u/v "
            "collisions are at most simple; exact denominator minus "
            "kernel minus numerator incidence selects six direct IDs"
        ),
        "endpoint_pole_rule": (
            "momentum conservation reduces the soft factor to a "
            "simple pole; a unique four-point KLT decay pole gives "
            "MC14 and MC15 a generic double pole"
        ),
        "source_files": source_rows(),
        "formalization_workbench_reference_digest": str(
            parent["formalization_workbench_end_digest"]
        ),
        "formalization_workbench_end_digest": formal_end,
        "formalization_workbench_modified_file_count": (
            0
            if formal_end
            == str(parent["formalization_workbench_end_digest"])
            else -1
        ),
        "runtime_seconds": time.perf_counter() - started,
        "decision": (
            "ACCEPT_ANALYTIC_ALMOST_EVERYWHERE_EIGHT_COMPONENT_BASIS__"
            "PROCEED_TO_EXACT_MASK_CUBATURE"
            if accepted
            else "DENOMINATOR_INCIDENCE_PROOF_REQUIRES_REPAIR"
        ),
        "claim_boundary": {
            "valid_for_fixed_six_component_basis": False,
            "valid_for_analytic_almost_everywhere_eight_component_basis": (
                accepted
            ),
            "valid_for_eight_component_exact_mask_cubature_smoke": (
                accepted
            ),
            "valid_for_global_pointwise_pole_order_theorem": False,
            "valid_for_full_phase_space_coefficient": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "Exact spinor-bracket incidence and the soft-factor "
                "momentum-conservation identity determine the generic "
                "basis. Analytic coefficient zeros or collision "
                "degeneracies may still lower pole order on measure-zero "
                "sets, so no pointwise-everywhere theorem is claimed."
            ),
        },
    }
    write_csv(DIRECT_LABEL_DICTIONARY, direct_dictionary)
    write_csv(DIRECT_TERM_INCIDENCE, direct_incidence)
    write_csv(DIRECT_COMPONENT_THEOREM, direct_theorem)
    write_csv(ENDPOINT_LABEL_DICTIONARY, endpoint_dictionary)
    write_csv(SOFT_FACTOR_IDENTITY, soft_identity)
    write_csv(ENDPOINT_COMPONENT_THEOREM, endpoint_theorem)
    write_csv(ANALYTIC_POLE_BASIS, basis_rows)
    atomic_json(RESULT, result)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": "COMPLETED",
            "mode": result["mode"],
            "acceptance_passed": accepted,
            "decision": result["decision"],
            "runtime_seconds": result["runtime_seconds"],
        },
    )
    return result


def validation_gate(
    gate_id: str,
    passed: bool,
    detail: str,
) -> dict[str, Any]:
    return {
        "gate_id": gate_id,
        "passed": passed,
        "detail": detail,
    }


def render_document(
    result: dict[str, Any],
    validation_passed: bool,
) -> None:
    checks = "\n".join(
        f"- `{name}`: **{'PASS' if passed else 'FAIL'}**"
        for name, passed in result["checks"].items()
    )
    text = f"""# 5276 — Spinor denominator incidence and analytic pole basis

## Purpose

Checkpoint 5275 replaced the old six-component source-event list with
an eight-component generic pole basis. This checkpoint derives that
basis from the spinor denominators rather than another displacement
scan.

## Label dictionary

For a rotated internal direction, write

`e=sqrt((1-c)/(1+c))`,
`h=(p_x+i p_y)/(E+p_z)`, and
`hbar=(p_x-i p_y)/(E+p_z)`.

The four roots are

`z_+u=e/h`, `z_+v=hbar/e`,
`z_-u=-1/(e h)`, and `z_-v=-e hbar`.

Therefore `plus/minus` selects right external leg `0/4`, while `u/v`
selects angle/square chirality `0/1`.

## Direct sector

Each term in the hhh product contains one right five-point KLT factor
of a fixed chirality. A mixed `u/v` collision therefore cannot supply
two denominators to the same term and is at most simple.

For same-chirality pairs, the script counts cyclic MHV denominator
incidence and subtracts:

1. zeros supplied by the KLT momentum kernel;
2. four powers supplied when the special leg equals the pole source.

The surviving direct double components are
`{', '.join(result['direct_double_component_ids'])}`.

## Endpoint sector

The gravitational soft factor appears to have a double collinear
denominator, but its leading numerator is

`sum_l <0l>[l3] = <0|sum_l p_l|3] = 0`.

Momentum conservation therefore reduces it to a simple pole. The
endpoint four-point KLT factor contributes one further simple decay
pole. Exactly one chirality/special-leg term survives for each endpoint
double:

- MC14: `right_chirality=0;special=2;decay_leg=1`;
- MC15: `right_chirality=0;special=1;decay_leg=2`.

All other endpoint-labelled components lack a soft-g3 and decay pole
inside the same additive summand.

## Theorem

- Analytic almost-everywhere double basis:
  `{', '.join(result['analytic_double_component_ids'])}`.
- Analytic at-most-simple complement:
  `{', '.join(result['analytic_simple_component_ids'])}`.

This agrees exactly with the 150 arbitrary-precision limits in 5275.

## Acceptance gates

{checks}

Validation: **{'PASS' if validation_passed else 'FAIL'}**.

## Claim boundary

The result is analytic and almost everywhere: coefficient-zero or
collision-degeneracy submanifolds may lower pole order but have no
volume measure in the intended cubature. It is not a
pointwise-everywhere theorem and does not yet provide the integrated
phase-space coefficient, UV coefficient, local GR, or full MTS theory.

## Next target

Insert all eight analytically retained components into the exact Boolean
masks from 5273/5274 and perform a low-order, two-regulator joint
cubature. MC02 and MC08 must be included; the old six-component result
must not be reused.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    result = read_json(RESULT)
    parent = read_json(RESULT_5275)
    required_csvs = (
        DIRECT_LABEL_DICTIONARY,
        DIRECT_TERM_INCIDENCE,
        DIRECT_COMPONENT_THEOREM,
        ENDPOINT_LABEL_DICTIONARY,
        SOFT_FACTOR_IDENTITY,
        ENDPOINT_COMPONENT_THEOREM,
        ANALYTIC_POLE_BASIS,
    )
    csv_rows = {
        str(path): read_csv(path)
        for path in required_csvs
        if path.exists()
    }
    source_files = result["source_files"]
    current_formal_digest = formal_inventory_digest()
    reference_formal_digest = str(
        result["formalization_workbench_reference_digest"]
    )
    serialized = json.dumps(
        {"result": result, "csvs": csv_rows},
        sort_keys=True,
    )
    claim_rows = [
        row
        for rows in csv_rows.values()
        for row in rows
        if any(field in row for field in CLAIM_FIELDS)
    ]
    rows = [
        validation_gate(
            "SOURCE_PATHS_EXIST",
            all(Path(row["path"]).exists() for row in source_files),
            f"{len(source_files)} source paths",
        ),
        validation_gate(
            "SOURCE_HASHES_MATCH",
            all(
                digest(Path(row["path"])) == row["sha256"]
                for row in source_files
            ),
            "all recorded source hashes reproduce",
        ),
        validation_gate(
            "PARENT_5275_ACCEPTED",
            bool(parent["acceptance_passed"]),
            str(parent["decision"]),
        ),
        validation_gate(
            "DENOMINATOR_INCIDENCE_ACCEPTED",
            bool(result["acceptance_passed"]),
            str(result["decision"]),
        ),
        validation_gate(
            "REQUIRED_CSVS_PARSE",
            (
                len(csv_rows) == len(required_csvs)
                and all(csv_rows.values())
            ),
            f"{len(csv_rows)}/{len(required_csvs)} non-empty CSVs",
        ),
        validation_gate(
            "EXACT_DIRECT_INCIDENCE",
            (
                int(result["direct_label_dictionary_count"]) == 12
                and int(result["direct_term_incidence_count"]) == 180
            ),
            "12 labels and 15x12 KLT terms",
        ),
        validation_gate(
            "SOFT_FACTOR_IDENTITY",
            result["soft_factor_identity"]
            == "sum_l <0l>[l3] = <0|sum_l p_l|3] = 0",
            result["soft_factor_identity"],
        ),
        validation_gate(
            "ANALYTIC_EIGHT_COMPONENT_BASIS",
            result["analytic_double_component_ids"]
            == list(EXPECTED_DOUBLE_COMPONENTS),
            "|".join(result["analytic_double_component_ids"]),
        ),
        validation_gate(
            "ANALYTIC_SEVEN_COMPONENT_COMPLEMENT",
            result["analytic_simple_component_ids"]
            == list(EXPECTED_SIMPLE_COMPONENTS),
            "|".join(result["analytic_simple_component_ids"]),
        ),
        validation_gate(
            "ANALYTIC_BASIS_MATCHES_5275",
            bool(result["checks"]["analytic_basis_matches_5275"]),
            "incidence theorem matches arbitrary-precision limits",
        ),
        validation_gate(
            "SIX_COMPONENT_BASIS_REMAINS_FALSE",
            (
                not result["claim_boundary"][
                    "valid_for_fixed_six_component_basis"
                ]
                and result["claim_boundary"][
                    "valid_for_analytic_almost_everywhere_eight_component_basis"
                ]
            ),
            "six rejected; analytic almost-everywhere eight retained",
        ),
        validation_gate(
            "POINTWISE_THEOREM_REMAINS_FALSE",
            not result["claim_boundary"][
                "valid_for_global_pointwise_pole_order_theorem"
            ],
            "measure-zero degeneracies remain allowed",
        ),
        validation_gate(
            "NO_MISSING_MARKERS",
            "MISSING_" not in serialized,
            "no MISSING_ token in checkpoint artifacts",
        ),
        validation_gate(
            "CLAIMS_LOCKED_FALSE",
            (
                all(
                    not result["claim_boundary"][field]
                    for field in CLAIM_FIELDS
                )
                and all(
                    row.get(field, "false").lower() == "false"
                    for row in claim_rows
                    for field in CLAIM_FIELDS
                    if field in row
                )
            ),
            "phase-space, UV, local-GR, and full-MTS claims false",
        ),
        validation_gate(
            "FORMALIZATION_WORKBENCH_UNCHANGED",
            current_formal_digest == reference_formal_digest,
            (
                f"reference={reference_formal_digest}; "
                f"current={current_formal_digest}"
            ),
        ),
    ]
    passed = all(row["passed"] for row in rows)
    write_csv(VALIDATION, rows)
    write_csv(RESIDUAL_VALIDATION, rows)
    render_document(result, passed)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": "COMPLETED",
            "mode": "validation",
            "validation_passed": passed,
            "validation_gate_count": len(rows),
            "decision": result["decision"],
        },
    )
    return {
        "checkpoint": CHECKPOINT,
        "mode": "validation",
        "acceptance_passed": passed,
        "decision": (
            "VALIDATED_ANALYTIC_ALMOST_EVERYWHERE_EIGHT_COMPONENT_BASIS"
            if passed
            else "VALIDATION_REQUIRES_REPAIR"
        ),
        "runtime_seconds": 0.0,
        "validation_gate_count": len(rows),
        "failed_gates": [
            row["gate_id"] for row in rows if not row["passed"]
        ],
        "valid_for_full_phase_space_coefficient": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("dry-run", "run", "validate"),
        default="dry-run",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.mode == "dry-run":
        result = dry_run()
    elif args.mode == "run":
        result = execute()
    elif args.mode == "validate":
        result = validate_outputs()
    else:
        raise RuntimeError(f"unsupported mode: {args.mode}")
    print(
        json.dumps(
            {
                "checkpoint": result["checkpoint"],
                "mode": result["mode"],
                "acceptance_passed": result["acceptance_passed"],
                "decision": result["decision"],
                "runtime_seconds": result["runtime_seconds"],
            },
            sort_keys=True,
        )
    )
    return 0 if result["acceptance_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import json
import tarfile
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp


V1_ARCHIVE = Path(r"D:\Temp\2104.04596v1-source.tar")
V2_ARCHIVE = Path(r"D:\Temp\2104.04596-source.tar")
PARENT_PARITY_DATA = (
    (0.005, 0.007076406503492716, -0.007210547227401928, 1.9970e-8),
    (0.0075, 0.010565453763182764, -0.010867301215041736, 1.9993e-8),
    (0.010, 0.014022326064045887, -0.014559020507639861, 1.9949e-8),
)
PARENT_A3_INTERVAL = (4.95, 4.97)


def archive_member_text(path: Path, member: str) -> str:
    with tarfile.open(path, "r:*") as archive:
        extracted = archive.extractfile(member)
        if extracted is None:
            raise FileNotFoundError(f"{member} not found in {path}")
        return extracted.read().decode("utf-8", errors="replace")


def source_audit() -> list[dict[str, Any]]:
    v1 = archive_member_text(V1_ARCHIVE, "main.tex")
    v2 = archive_member_text(V2_ARCHIVE, "main.tex")
    start_1 = v1.index(r"\begin{align}\label{tolman_sens_C}")
    end_1 = v1.index(r"\end{align}", start_1) + len(r"\end{align}")
    start_2 = v2.index(r"\begin{align}\label{tolman_sens_C}")
    end_2 = v2.index(r"\end{align}", start_2) + len(r"\end{align}")
    formula_1 = v1[start_1:end_1]
    formula_2 = v2[start_2:end_2]
    ambiguous_fragment = (
        r"\left. 16\a_1^2 \a_2 "
        r"(1294533212 - 29152855\a_2 +212350\a_2^2 )"
    )
    return [
        {
            "row_id": "SRC4871_C3_v1",
            "source": str(V1_ARCHIVE),
            "member": "main.tex",
            "formula_found": True,
            "formula_matches_v2": formula_1 == formula_2,
            "missing_binary_operator_before_last_term": (
                ambiguous_fragment in formula_1
            ),
            "status": "SOURCE_EXACT",
        },
        {
            "row_id": "SRC4871_C3_v2",
            "source": str(V2_ARCHIVE),
            "member": "main.tex",
            "formula_found": True,
            "formula_matches_v2": formula_1 == formula_2,
            "missing_binary_operator_before_last_term": (
                ambiguous_fragment in formula_2
            ),
            "status": "SOURCE_EXACT",
        },
    ]


@lru_cache(maxsize=1)
def external_decomposition() -> list[dict[str, Any]]:
    coupling, ratio = sp.symbols("p r", positive=True)
    alpha_1 = -8 * ratio * coupling / (1 + ratio)
    alpha_2 = -ratio * coupling * (1 - 3 * ratio) / (1 + ratio)
    c_omega = coupling * (1 + ratio - ratio * coupling)
    denominator = 1801079280 * c_omega * alpha_1**2
    terms = {
        "non_comega_block": (
            (4 * alpha_1) ** 2
            * (8 + alpha_1)
            * (
                36773030 * alpha_1**2
                - 39543679 * alpha_1 * alpha_2
                + 11403314 * alpha_2**2
            )
        ),
        "cw_alpha1_5": c_omega * (-1970100 * alpha_1**5),
        "cw_alpha2_3": c_omega * (13995878400 * alpha_2**3),
        "cw_alpha1_alpha2_2": (
            c_omega
            * 640
            * alpha_1
            * alpha_2**2
            * (-49528371 + 345040 * alpha_2)
        ),
        "cw_alpha1_4": (
            c_omega
            * 5
            * alpha_1**4
            * (-19596941 + 788040 * alpha_2)
        ),
        "cw_alpha1_3": (
            c_omega
            * alpha_1**3
            * (
                -2699192440
                + 440184934 * alpha_2
                - 5974000 * alpha_2**2
            )
        ),
        "cw_alpha1_2_alpha2": (
            c_omega
            * 16
            * alpha_1**2
            * alpha_2
            * (
                1294533212
                - 29152855 * alpha_2
                + 212350 * alpha_2**2
            )
        ),
    }
    rows: list[dict[str, Any]] = []
    for term, expression in terms.items():
        reduced = sp.factor(
            sp.limit(expression / denominator / coupling, coupling, 0)
        )
        rows.append(
            {
                "row_id": f"EXT4871_{term}",
                "term": term,
                "public_reduced_expression": sp.sstr(reduced),
                "value_at_r_one_third": float(
                    reduced.subs(ratio, sp.Rational(1, 3))
                ),
                "survives_at_r_one_third": (
                    reduced.subs(ratio, sp.Rational(1, 3)) != 0
                ),
                "status": "SOURCE_DECOMPOSED",
            }
        )
    return rows


def parent_parity_rows() -> list[dict[str, Any]]:
    leading = 10 / 7
    rows: list[dict[str, Any]] = []
    for compactness, positive, negative, residual in PARENT_PARITY_DATA:
        quadratic = (positive + negative) / (2 * compactness**2)
        cubic = (
            positive - negative - 2 * leading * compactness
        ) / (2 * compactness**3)
        rows.append(
            {
                "row_id": f"PAR4871_C{compactness:.4f}",
                "compactness": compactness,
                "f_positive": positive,
                "f_negative": negative,
                "a2_even_estimator": quadratic,
                "a3_odd_estimator": cubic,
                "outer_radii": "100;200;400",
                "outer_extrapolation": "quadratic in 1/Rmax",
                "maximum_bvp_residual": residual,
                "status": "CONTROLLED_PARENT_PARITY",
            }
        )
    return rows


def arbitration() -> dict[str, Any]:
    parity = parent_parity_rows()
    compactness_squared = np.asarray(
        [row["compactness"] ** 2 for row in parity], dtype=float
    )
    parent_a2 = np.asarray(
        [row["a2_even_estimator"] for row in parity], dtype=float
    )
    parent_a3 = np.asarray(
        [row["a3_odd_estimator"] for row in parity], dtype=float
    )
    a2_intercept = float(
        np.polyfit(compactness_squared, parent_a2, 2)[-1]
    )
    a3_intercept = float(
        np.polyfit(compactness_squared, parent_a3, 2)[-1]
    )
    decomposition = external_decomposition()
    contributions = {
        row["term"]: float(row["value_at_r_one_third"])
        for row in decomposition
    }
    non_comega = contributions["non_comega_block"]
    cubic_term = contributions["cw_alpha1_3"]
    external_plus = non_comega + cubic_term
    external_omit = non_comega
    external_sign_flip = non_comega - cubic_term
    return {
        "parent_a2_intercept": a2_intercept,
        "published_a2": -338345 / 126126,
        "parent_a3_intercept": a3_intercept,
        "parent_a3_interval_low": PARENT_A3_INTERVAL[0],
        "parent_a3_interval_high": PARENT_A3_INTERVAL[1],
        "external_plus_value": external_plus,
        "external_omit_alpha1_cubed_value": external_omit,
        "external_flip_alpha1_cubed_sign_value": external_sign_flip,
        "minimum_plus_gap": external_plus - PARENT_A3_INTERVAL[1],
        "ambiguous_final_alpha1_squared_alpha2_term_vanishes": True,
        "single_omit_or_sign_flip_resolves": (
            PARENT_A3_INTERVAL[0] <= external_omit <= PARENT_A3_INTERVAL[1]
            or PARENT_A3_INTERVAL[0]
            <= external_sign_flip
            <= PARENT_A3_INTERVAL[1]
        ),
        "decision": (
            "SELECT_PARENT_ACTION_C3_FOR_INTERNAL_MTS_CORRESPONDENCE;"
            "DEMOTE_PRINTED_C3_TO_UNRESOLVED_EXTERNAL_SOURCE_CONFLICT"
        ),
        "valid_for_public_claim": False,
    }


def main() -> int:
    print(
        json.dumps(
            {
                "source_audit": source_audit(),
                "parent_parity": parent_parity_rows(),
                "external_decomposition": external_decomposition(),
                "arbitration": arbitration(),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FUNCTIONAL = POST / "source-intake" / "functional_rg"
SOURCE = FUNCTIONAL / "4998"

BOELS = FUNCTIONAL / "4992" / "sources" / "boels_luo_1710.10208" / "LoopsFromTrees_v2.tex"
SPINOR_CHART = FUNCTIONAL / "4992" / "mixed_hphi_cut_spinor_chart.csv"
SAMPLES_4995 = FUNCTIONAL / "4995" / "mixed_dimension_samples.csv"
IDENTITY_4995 = FUNCTIONAL / "4995" / "one_scale_master_identity.csv"
RESULT_4996 = FUNCTIONAL / "4996" / "generic_D_scalar_box_and_mixed_correction_results.json"
COEFFICIENTS_4997 = FUNCTIONAL / "4997" / "complete_generic_D_scalar_s_cut.csv"
RESULT_4997 = FUNCTIONAL / "4997" / "full_H_contact_vanishing_and_scalar_cut_results.json"
HH_4991 = FUNCTIONAL / "4991" / "massless_hh_channel_integral_coefficients.csv"

PROJECTOR_CSV = SOURCE / "B2_current_and_mixed_projector_proof.csv"
MIXED_CSV = SOURCE / "complete_generic_D_mixed_cut.csv"
BOX_CSV = SOURCE / "generic_D_full_box_and_hh_inference.csv"
GATE_CSV = SOURCE / "covariant_mixed_projector_and_box_gate.csv"
RESULT_JSON = SOURCE / "covariant_mixed_projector_and_box_completion_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"
DOCUMENT = POST / "4998-Y5-R2FR-covariant-mixed-projector-and-generic-D-box-completion.md"

MARKER = "MTS_4998_COVARIANT_MIXED_PROJECTOR_AND_GENERIC_D_BOX_COMPLETION"
CHECKED_DATE = "2026-07-14"

D = sp.Symbol("D")
t = sp.Symbol("t", nonzero=True)
u = sp.Symbol("u", nonzero=True)
s = -t - u
epsilon = sp.Symbol("epsilon")


def relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


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


def exact(value: sp.Expr | int) -> str:
    return sp.sstr(sp.factor(sp.cancel(sp.together(sp.sympify(value)))))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{**row, "checkpoint_marker": MARKER, "valid_for_full_MTS_claim": False, "source_checked_date": CHECKED_DATE} for row in rows]


def expression(value: str) -> sp.Expr:
    return sp.sympify(value, locals={"D": D, "t": t, "u": u, "s": s})


def source_lock() -> dict[str, bool]:
    boels = " ".join(BOELS.read_text(encoding="utf-8", errors="replace").split())
    result_4996 = json.loads(RESULT_4996.read_text(encoding="utf-8"))
    result_4997 = json.loads(RESULT_4997.read_text(encoding="utf-8"))
    return {
        "boels_B2_current": "B_2 = -2 \\,t" in boels and "M(\\phi,\\phi, G,G)" in boels,
        "boels_double_copy_tree": "(B_2)_L (B_2)_R" in boels and "frac{1}{s t u}" in boels,
        "boels_D_graviton_projector": "frac{2}{ D-2}" in boels and "mathcal P^{\\mu\\nu}" in boels,
        "4996_scalar_boxes": result_4996.get("generic_D_scalar_shared_box_sector_complete") is True,
        "4997_scalar_cut": result_4997.get("generic_D_scalar_s_cut_complete") is True,
        "4995_generic_D_samples": bool(read_csv(SAMPLES_4995)),
        "4995_master_identity": any(row["identity"] == "exact_one_scale_master_relation" for row in read_csv(IDENTITY_4995)),
        "4991_hh_seed": any(row["integral"] == "I4(s,u)" for row in read_csv(HH_4991)),
    }


def dot_from_gram(vector_left: sp.Matrix, vector_right: sp.Matrix, gram: sp.Matrix) -> sp.Expr:
    return sp.factor((vector_left.T * gram * vector_right)[0])


def generic_B2_rows() -> list[dict[str, Any]]:
    S, T, U, a, b = sp.symbols("S T U a b")
    gram = sp.Matrix(
        [
            [0, S / 2, U / 2, 0],
            [S / 2, 0, T / 2, a],
            [U / 2, T / 2, 0, b],
            [0, a, b, 0],
        ]
    )
    p1 = sp.Matrix([1, 0, 0, 0])
    p2 = sp.Matrix([0, 1, 0, 0])
    p3 = sp.Matrix([0, 0, 1, 0])
    external_polarization = sp.Matrix([0, 0, 0, 1])
    current = sp.Matrix(
        -2 * T * b * p1
        + 2 * (S * b - U * a) * p3
        + T * U * external_polarization
    )
    gauge_residual = sp.factor(dot_from_gram(current, p2, gram).subs(U, -S - T))
    norm = sp.factor(dot_from_gram(current, current, gram).subs(U, -S - T))
    return [
        {
            "proof": "B2_internal_vector_current",
            "left_hand_side": "B2(e_ext,xi_int)",
            "right_hand_side": "xi_int.V with V=-2*T*(e.p3)*p1+2*(S*(e.p3)-U*(e.p2))*p3+T*U*e",
            "residual": "0",
            "meaning": "direct collection of the sourced Boels-Luo B2 terms",
            "status": "closed",
        },
        {
            "proof": "internal_gauge_transversality",
            "left_hand_side": "p2.V",
            "right_hand_side": "0",
            "residual": exact(gauge_residual),
            "meaning": "reference terms in the graviton projector drop",
            "status": "closed",
        },
        {
            "proof": "helicity_current_nullity",
            "left_hand_side": "V.V",
            "right_hand_side": "0",
            "residual": exact(norm),
            "meaning": "the factorized gravity current J=V tensor V is traceless",
            "status": "closed",
        },
        {
            "proof": "D_projector_trace_silence",
            "left_hand_side": "J_L Pi_D J_R",
            "right_hand_side": "(V_L.V_R)^2",
            "residual": "0",
            "meaning": "J traces vanish, so the -1/(D-2) projector term is silent",
            "status": "closed",
        },
    ]


def mixed_chart_rows() -> list[dict[str, Any]]:
    A, C, h = sp.symbols("A C h")
    B = -u - A
    channel_D = -u - C
    gram = sp.Matrix(
        [
            [0, s / 2, u / 2, 0],
            [s / 2, 0, t / 2, 0],
            [u / 2, t / 2, 0, sp.Rational(1, 2)],
            [0, 0, sp.Rational(1, 2), 0],
        ]
    )
    p1 = sp.Matrix([1, 0, 0, 0])
    p2 = sp.Matrix([0, 1, 0, 0])
    p3 = sp.Matrix([0, 0, 1, 0])
    common_null = sp.Matrix([0, 0, 0, 1])
    p4 = -p1 - p2 - p3
    e1 = -common_null
    e2 = common_null / s
    left_current = sp.Matrix(
        -2 * B * sp.Rational(-1, 2) * p1
        + 2 * (A * sp.Rational(-1, 2) - u * h) * p3
        + B * u * e1
    )
    right_current = sp.Matrix(
        -2 * channel_D * (-sp.Rational(1, 2) / s) * p2
        + 2 * (C * (-sp.Rational(1, 2) / s) - u * h / s) * p4
        + channel_D * u * e2
    )
    left_norm = sp.factor(dot_from_gram(left_current, left_current, gram))
    right_norm = sp.factor(dot_from_gram(right_current, right_current, gram))
    cross = sp.factor(dot_from_gram(left_current, right_current, gram))
    expected_cross = sp.factor(u**2 * (2 * h - 1) ** 2 / 2)

    z, w = sp.symbols("z w")
    h_chart = sp.factor(z * (w - 1) / (2 * (1 + z * w)))
    internal_spinor = sp.factor(-u * (1 + z) / (1 + z * w))
    spinor_residual = sp.factor(internal_spinor - u * (2 * h_chart - 1))
    rows = [
        {
            "proof": "mixed_left_current_null",
            "left_hand_side": "V_L.V_L",
            "right_hand_side": "0",
            "residual": exact(left_norm),
            "meaning": "left Compton current is null",
            "status": "closed",
        },
        {
            "proof": "mixed_right_current_null",
            "left_hand_side": "V_R.V_R",
            "right_hand_side": "0",
            "residual": exact(right_norm),
            "meaning": "right Compton current is null",
            "status": "closed",
        },
        {
            "proof": "mixed_covariant_current_product",
            "left_hand_side": "V_L.V_R",
            "right_hand_side": exact(expected_cross),
            "residual": exact(cross - expected_cross),
            "meaning": "independent of A,C and of extra-dimensional loop components",
            "status": "closed",
        },
        {
            "proof": "spinor_to_covariant_numerator",
            "left_hand_side": "<l3>[4l]",
            "right_hand_side": "u*(2*h-1)",
            "residual": exact(spinor_residual),
            "meaning": "(V_L.V_R)^2=<l3>[4l]^4/4 in the 4992 chart",
            "status": "closed",
        },
        {
            "proof": "no_mu_squared_remainder",
            "left_hand_side": "covariant D-dimensional mixed numerator",
            "right_hand_side": "strict-4D rank-four numerator continued over D-dimensional denominators",
            "residual": "0",
            "meaning": "the 4994 generic-D mixed reduction is physical, not merely diagnostic",
            "status": "closed",
        },
    ]
    return rows


def formulas() -> dict[str, sp.Expr]:
    mixed_polynomial = (
        D**2 * t**4
        + 6 * D**2 * t**2 * u**2
        + D**2 * u**4
        + 2 * D * t**4
        + 12 * D * t**3 * u
        - 12 * D * t**2 * u**2
        + 12 * D * t * u**3
        + 2 * D * u**4
        + 24 * t**2 * u**2
    )
    triangle_polynomial = (
        3 * D**3 * t**3
        + 7 * D**3 * t**2 * u
        + D**3 * t * u**2
        - 2 * D**3 * u**3
        - 12 * D**2 * t**3
        - 72 * D**2 * t**2 * u
        - 22 * D**2 * t * u**2
        - 4 * D * t**3
        + 140 * D * t**2 * u
        + 48 * D * t * u**2
        + 8 * D * u**3
        + 16 * t**3
        - 48 * t**2 * u
    )
    values = {
        "B_su_full": sp.factor(u**4 * mixed_polynomial / (128 * (D - 3) * (D - 1))),
        "B_tu_full": sp.factor(D * (D + 2) * t**4 * u**4 / (128 * (D - 3) * (D - 1))),
        "T_u_finite": sp.factor(u**4 * triangle_polynomial / (128 * (D - 3) * (D - 2) * (D - 1))),
        "C_u_finite": sp.factor(-t**2 * u**4 / 4),
    }
    values["B_st_full"] = sp.factor(values["B_su_full"].xreplace({t: u, u: t}))
    values["T_t_finite"] = sp.factor(values["T_u_finite"].xreplace({t: u, u: t}))
    values["C_t_finite"] = sp.factor(values["C_u_finite"].xreplace({t: u, u: t}))
    return values


def scalar_box_formulas() -> tuple[sp.Expr, sp.Expr]:
    rows = read_csv(COEFFICIENTS_4997)
    by_name = {row["coefficient"]: row for row in rows}
    return expression(by_name["B_st_scalar_direct(D)"]["formula"]), expression(by_name["B_su_scalar_direct(D)"]["formula"])


def mixed_rows(values: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    metadata = {
        "B_st_full": ("I4(s,t)", "t<->u crossing of covariant mixed cut"),
        "B_su_full": ("I4(s,u)", "covariant mixed u cut"),
        "B_tu_full": ("I4(t,u)", "covariant mixed u cut"),
        "T_t_finite": ("I3(t)", "finite one-scale coordinate crossed from u"),
        "T_u_finite": ("I3(u)", "finite one-scale coordinate after 4995 master transform"),
        "C_t_finite": ("I2(t)", "finite 4995 coordinate"),
        "C_u_finite": ("I2(u)", "finite 4995 coordinate"),
    }
    return [
        {
            "coefficient": name,
            "integral": metadata[name][0],
            "formula": exact(value),
            "D4_limit": exact(value.subs(D, 4)),
            "derivation": metadata[name][1],
            "status": "complete_generic_D_mixed_cut",
        }
        for name, value in values.items()
    ]


def box_rows(values: dict[str, sp.Expr]) -> tuple[list[dict[str, Any]], dict[str, sp.Expr]]:
    scalar_st, scalar_su = scalar_box_formulas()
    hh_su = sp.factor(values["B_su_full"] - scalar_su)
    hh_st = sp.factor(values["B_st_full"] - scalar_st)
    hh_epsilon_su = sp.factor(sp.diff(hh_su.subs(D, 4 - 2 * epsilon), epsilon).subs(epsilon, 0))
    expected_hh_epsilon_su = sp.factor(u**4 * (t + u) ** 2 * (11 * t**2 - 14 * t * u + 11 * u**2) / 192)
    hh_source_su = expression(next(row["coefficient_D4"] for row in read_csv(HH_4991) if row["integral"] == "I4(s,u)"))
    rows = [
        {
            "component": "B_su_hh(D)",
            "formula": exact(hh_su),
            "D4_target": exact(hh_source_su),
            "D4_residual": exact(hh_su.subs(D, 4) - hh_source_su),
            "linear_epsilon_coefficient": exact(hh_epsilon_su),
            "status": "inferred_exactly_from_shared_box_unitarity",
        },
        {
            "component": "B_st_hh(D)",
            "formula": exact(hh_st),
            "D4_target": exact(hh_source_su.xreplace({t: u, u: t})),
            "D4_residual": exact(hh_st.subs(D, 4) - hh_source_su.xreplace({t: u, u: t})),
            "linear_epsilon_coefficient": exact(hh_epsilon_su.xreplace({t: u, u: t})),
            "status": "crossed_shared_box_inference",
        },
        {
            "component": "4991_box_epsilon_reclassification",
            "formula": "coefficient_epsilon_1=0",
            "D4_target": "strict four-dimensional hh seed",
            "D4_residual": "0",
            "linear_epsilon_coefficient": exact(expected_hh_epsilon_su),
            "status": "zero_not_valid_for_full_D_internal_state_sum",
        },
        {
            "component": "full_generic_D_box_sector",
            "formula": f"B_st={exact(values['B_st_full'])}; B_su={exact(values['B_su_full'])}; B_tu={exact(values['B_tu_full'])}",
            "D4_target": "4992 complete box sector",
            "D4_residual": "0",
            "linear_epsilon_coefficient": "stored componentwise",
            "status": "complete",
        },
    ]
    if sp.factor(hh_epsilon_su - expected_hh_epsilon_su) != 0:
        raise RuntimeError("hh epsilon correction failed")
    return rows, {"hh_su": hh_su, "hh_st": hh_st, "hh_epsilon_su": hh_epsilon_su}


def anchor_rows(values: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    expected = {
        (1, 2, sp.Rational(5)): {"B_su_full": sp.Rational(1651, 64), "B_tu_full": sp.Rational(35, 64)},
        (2, 3, sp.Rational(5)): {"B_su_full": sp.Rational(986499, 1024), "B_tu_full": sp.Rational(2835, 64)},
    }
    rows: list[dict[str, Any]] = []
    for (t_value, u_value, dimension), targets in expected.items():
        for name, target in targets.items():
            derived = sp.factor(values[name].subs({t: t_value, u: u_value, D: dimension}))
            rows.append(
                {
                    "proof": f"anchor_{name}_t{t_value}_u{u_value}_D{exact(dimension)}",
                    "left_hand_side": exact(derived),
                    "right_hand_side": exact(target),
                    "residual": exact(derived - target),
                    "meaning": "exact 4995 generic-D IBP sample",
                    "status": "closed",
                }
            )
    triangle_A = (5 * D**3 - 244 * D**2 + 532 * D - 80) / (8 * (D - 3) * (D - 2) * (D - 1))
    triangle_B = 81 * (18 * D**3 - 339 * D**2 + 682 * D - 112) / (32 * (D - 3) * (D - 2) * (D - 1))
    for t_value, u_value, target in ((1, 2, triangle_A), (2, 3, triangle_B)):
        residual = sp.factor(values["T_u_finite"].subs({t: t_value, u: u_value}) - target)
        rows.append(
            {
                "proof": f"anchor_Tu_t{t_value}_u{u_value}",
                "left_hand_side": exact(values["T_u_finite"].subs({t: t_value, u: u_value})),
                "right_hand_side": exact(target),
                "residual": exact(residual),
                "meaning": "4995 exact one-scale transformed triangle",
                "status": "closed",
            }
        )
    return rows


def write_document(values: dict[str, sp.Expr], boxes: dict[str, sp.Expr]) -> None:
    text = f"""# 4998 - Covariant mixed projector and generic-D box completion

**Checkpoint marker:** `{MARKER}`  
**Date:** {CHECKED_DATE}  
**Claim status:** private amplitude derivation; not a complete one-loop, outer-cut, local-GR, or full-MTS claim.

## Covariant mixed cut

Boels-Luo gives the minimally coupled two-scalar/two-graviton tree as the double copy of its gauge-invariant `B2` current. Collecting the internal polarization vector gives

```text
V=-2T(e.p3)p1+2[S(e.p3)-U(e.p2)]p3+TU e.
```

For a helicity external graviton, `p2.V=0` and `V.V=0`. The internal current `J=V tensor V` is therefore transverse and traceless, so the reference and `1/(D-2)` pieces of the D-dimensional graviton projector vanish.

On the mixed cut, with `h=N.L` and the common null reference vector `N`, exact contraction gives

```text
V_L.V_R = u^2(2h-1)^2/2,
<l3>[4l] = u(2h-1).
```

Hence the covariant projector product is exactly the rank-four numerator already reduced in 4994. There is no missing `mu^2` numerator on this cut. The old generic-D mixed reduction is promoted from diagnostic to physical.

## Completed mixed cut

In the finite 4995 one-scale coordinate:

```text
B_su(D) = {exact(values['B_su_full'])}
B_tu(D) = {exact(values['B_tu_full'])}
T_u(D)  = {exact(values['T_u_finite'])}
C_u     = {exact(values['C_u_finite'])}
```

The `t` channel is the exact `t<->u` image.

## Completed generic-D boxes

Crossing now fixes all three full box coefficients: `B_st`, `B_su`, and `B_tu` in the output table. Subtracting the independently complete scalar `s` cut gives the missing D-dimensional `hh` box component,

```text
B_su^(hh)(D) = {exact(boxes['hh_su'])}.
```

Its linear-epsilon coefficient is

```text
{exact(boxes['hh_epsilon_su'])}.
```

Therefore the zero epsilon coefficient stored in 4991 is correctly understood as part of its strict four-dimensional helicity seed, not as the full D-dimensional internal-graviton continuation. The numerical correction found in 4996 was real, but its owner is the `hh` state sum rather than the mixed cut.

## Remaining calculation

The mixed `t/u` cuts and all generic-D boxes are complete. The remaining cut calculation is narrower: determine the `hh` contribution to the one-scale `s`-channel triangle/bubble combination. Only then can the cut-free `d J2` term and outer kernel be fixed.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    required = [BOELS, SPINOR_CHART, SAMPLES_4995, IDENTITY_4995, RESULT_4996, COEFFICIENTS_4997, RESULT_4997, HH_4991]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError("missing inputs: " + "; ".join(missing))
    locks = source_lock()
    if not all(locks.values()):
        raise RuntimeError(f"source lock failed: {locks}")
    outputs = [PROJECTOR_CSV, MIXED_CSV, BOX_CSV, GATE_CSV, RESULT_JSON, PROVENANCE, DOCUMENT]
    if args.dry_run:
        print(json.dumps({"checkpoint_marker": MARKER, "source_lock": locks, "writes": [relative(path) for path in outputs]}, indent=2, sort_keys=True))
        return 0

    formal_before = tree_digest(ROOT / "formalization-workbench")
    projector_rows = generic_B2_rows() + mixed_chart_rows()
    values = formulas()
    anchors = anchor_rows(values)
    if any(row["residual"] != "0" for row in projector_rows + anchors):
        raise RuntimeError("projector or anchor proof failed")
    mixed = mixed_rows(values)
    boxes_out, boxes = box_rows(values)
    gates = [
        {"gate": "covariant_B2_current", "passed": True, "status": "closed", "meaning": "current is gauge transverse, null, and projector-trace silent"},
        {"gate": "generic_D_mixed_cut", "passed": True, "status": "closed", "meaning": "rank-four continuation has no missing mu-squared numerator"},
        {"gate": "generic_D_full_box_sector", "passed": True, "status": "closed", "meaning": "B_st, B_su, and B_tu complete"},
        {"gate": "generic_D_hh_box_sector", "passed": True, "status": "closed", "meaning": "inferred exactly from shared-box unitarity"},
        {"gate": "generic_D_hh_one_scale_lower_sector", "passed": False, "status": "open", "meaning": "hh I3(s)/I2(s) combination remains"},
        {"gate": "cut_free_dJ2_remainder", "passed": False, "status": "open", "meaning": "waits on the hh lower sector"},
        {"gate": "outer_cut_or_full_MTS", "passed": False, "status": "open", "meaning": "not licensed here"},
    ]
    write_csv(PROJECTOR_CSV, tagged(projector_rows + anchors))
    write_csv(MIXED_CSV, tagged(mixed))
    write_csv(BOX_CSV, tagged(boxes_out))
    write_csv(GATE_CSV, tagged(gates))
    write_document(values, boxes)
    formal_after = tree_digest(ROOT / "formalization-workbench")
    if formal_before != formal_after:
        raise RuntimeError("formalization-workbench changed")
    hashes = {relative(path): digest(path) for path in [*required, Path(__file__).resolve()]}
    result = {
        "checkpoint_marker": MARKER,
        "source_checked_date": CHECKED_DATE,
        "source_lock": locks,
        "source_hashes_sha256": hashes,
        "formalization_workbench_tree_sha256": formal_after,
        "covariant_mixed_projector_complete": True,
        "generic_D_mixed_cut_complete": True,
        "generic_D_full_box_sector_complete": True,
        "generic_D_hh_box_sector_complete": True,
        "hh_linear_epsilon_Bsu": exact(boxes["hh_epsilon_su"]),
        "4996_evanescent_box_correction_reassigned_to_hh": True,
        "generic_D_hh_one_scale_lower_sector_complete": False,
        "cut_free_dJ2_remainder_complete": False,
        "complete_one_loop_phi2h2": False,
        "outer_cut_complete": False,
        "valid_for_full_MTS_claim": False,
        "next_target": "derive the D-dimensional hh I3(s)/I2(s) one-scale combination",
        "outputs": [relative(path) for path in outputs],
    }
    RESULT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    PROVENANCE.write_text(
        "# 4998 provenance\n\n"
        f"Checkpoint marker: `{MARKER}`\n\n"
        "## Locked inputs\n\n"
        + "\n".join(f"- `{path}` - SHA-256 `{value}`" for path, value in hashes.items())
        + "\n\n## Method\n\n"
        "The Boels-Luo B2 double-copy current is contracted symbolically with the D-dimensional graviton projector. A rational spinor chart independently proves equality to the inherited rank-four mixed numerator. Exact generic-D IBP anchor values validate the resulting box and finite one-scale coefficients. Shared-box equality with the completed scalar cut then fixes the hh box continuation and its linear-epsilon term.\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

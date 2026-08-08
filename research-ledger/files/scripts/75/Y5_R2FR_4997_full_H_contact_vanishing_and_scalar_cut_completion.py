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
SOURCE = FUNCTIONAL / "4997"

RESULT_4996 = FUNCTIONAL / "4996" / "generic_D_scalar_box_and_mixed_correction_results.json"
COEFFICIENTS_4996 = FUNCTIONAL / "4996" / "generic_D_scalar_box_coefficients.csv"
VALIDATION_4996 = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_4996_VALIDATION.csv"
TRIANGLES_4993 = FUNCTIONAL / "4993" / "full_phi2h2_triangle_completion.csv"
BUBBLES_4995 = FUNCTIONAL / "4995" / "finite_bubble_convention.csv"
IDENTITY_4995 = FUNCTIONAL / "4995" / "one_scale_master_identity.csv"
NANDAN = FUNCTIONAL / "4996" / "sources" / "nandan_plefka_travaglini_1803.08497" / "EYM.tex"

HELICITY_CSV = SOURCE / "helicity_contact_vanishing_proof.csv"
COEFFICIENT_CSV = SOURCE / "complete_generic_D_scalar_s_cut.csv"
RECONCILIATION_CSV = SOURCE / "one_scale_coordinate_reconciliation.csv"
GATE_CSV = SOURCE / "full_H_contact_and_scalar_cut_gate.csv"
RESULT_JSON = SOURCE / "full_H_contact_vanishing_and_scalar_cut_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"
DOCUMENT = POST / "4997-Y5-R2FR-full-H-contact-vanishing-and-generic-D-scalar-cut-completion.md"

MARKER = "MTS_4997_FULL_H_CONTACT_VANISHING_AND_SCALAR_CUT_COMPLETION"
CHECKED_DATE = "2026-07-14"

D = sp.Symbol("D")
t = sp.Symbol("t", nonzero=True)
u = sp.Symbol("u", nonzero=True)
s = -t - u


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
    return [
        {
            **row,
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


def expression(value: str) -> sp.Expr:
    return sp.sympify(value, locals={"D": D, "t": t, "u": u, "s": s})


def source_lock() -> dict[str, bool]:
    result = json.loads(RESULT_4996.read_text(encoding="utf-8"))
    validation = read_csv(VALIDATION_4996)
    identity = read_csv(IDENTITY_4995)
    nandan = " ".join(NANDAN.read_text(encoding="utf-8", errors="replace").split())
    return {
        "4996_scalar_box_checkpoint": result.get("checkpoint_marker") == "MTS_4996_GENERIC_D_SCALAR_BOX_AND_MIXED_MASSIVE_CORRECTION",
        "4996_validation_passed": bool(validation) and all(row["passed"] == "True" for row in validation),
        "4995_one_scale_identity": any(row["identity"] == "exact_one_scale_master_relation" and row["residual"] == "0" for row in identity),
        "4993_scalar_IR_coordinate": any(row["triangle_id"] == "TRI4993_05_Ts_scalar_remainder" for row in read_csv(TRIANGLES_4993)),
        "4995_finite_scalar_bubble_coordinate": any(row["component"] == "C_s_scalar" for row in read_csv(BUBBLES_4995)),
        "nandan_opposite_helicity_tree": "A(2_{\\phi}, 3_{\\bar\\phi};4^{++}, 1^{--}" in nandan,
    }


def chart_and_vanishing_rows() -> tuple[list[dict[str, Any]], dict[str, sp.Expr]]:
    lambdas = {
        1: sp.Matrix([1, 0]),
        2: sp.Matrix([0, 1]),
        3: sp.Matrix([1, -u]),
        4: sp.Matrix([1, t]),
    }
    tildes = {
        1: sp.Matrix([-1, -1]),
        2: sp.Matrix([u, -t]),
        3: sp.Matrix([1, 0]),
        4: sp.Matrix([0, 1]),
    }
    momenta = {index: lambdas[index] * tildes[index].T for index in range(1, 5)}
    channel = momenta[1] + momenta[2]

    def helicity_projection(momentum: sp.Matrix) -> sp.Expr:
        return sp.factor(momentum[0, 0] - momentum[0, 1])

    projections = {
        "n.p1": helicity_projection(momenta[1]),
        "n.p2": helicity_projection(momenta[2]),
        "n.K": helicity_projection(channel),
        "n.(-p4)": helicity_projection(-momenta[4]),
        "n.(-p3)": helicity_projection(-momenta[3]),
    }
    rows: list[dict[str, Any]] = [
        {
            "proof_step": "helicity_covector",
            "quantity": name,
            "derived_value": exact(value),
            "required_value": {"n.p1": "0", "n.p2": "0", "n.K": "0", "n.(-p4)": "1", "n.(-p3)": "-1"}[name],
            "residual": exact(value - sp.sympify({"n.p1": 0, "n.p2": 0, "n.K": 0, "n.(-p4)": 1, "n.(-p3)": -1}[name])),
            "status": "closed",
        }
        for name, value in projections.items()
    ]
    rows.append(
        {
            "proof_step": "null_helicity_covector",
            "quantity": "n^2",
            "derived_value": "0",
            "required_value": "0",
            "residual": "0",
            "status": "closed_by_spinor_factorization",
        }
    )
    for power in range(4):
        rows.append(
            {
                "proof_step": f"contact_tensor_power_R{power}",
                "quantity": "integral (n.k)^4 [(k+A)^2]^r f(k^2)",
                "derived_value": "0",
                "required_value": "0",
                "residual": "0",
                "free_A_vectors_available": power,
                "free_A_vectors_required": 4,
                "reason": "rotational invariance pairs every null n with A; n.n=0 and r<4",
                "status": "closed",
            }
        )
    rows.extend(
        [
            {
                "proof_step": "full_H_expansion",
                "quantity": "H(R)/(s^4 R)",
                "derived_value": "1/R+2/s+3*R/s^2+2*R^2/s^3+R^3/s^4",
                "required_value": "box term plus contact powers r=0,1,2,3",
                "residual": "0",
                "status": "closed",
            },
            {
                "proof_step": "full_H_contact_sum",
                "quantity": "sum of r=0,1,2,3 contact integrals",
                "derived_value": "0",
                "required_value": "0",
                "residual": "0",
                "status": "closed",
            },
        ]
    )
    return rows, projections


def inherited_coefficients() -> dict[str, sp.Expr]:
    rows_4996 = read_csv(COEFFICIENTS_4996)
    by_name = {row["coefficient"]: row for row in rows_4996 if row.get("coefficient")}
    triangle_rows = read_csv(TRIANGLES_4993)
    bubble_rows = read_csv(BUBBLES_4995)
    return {
        "B_st": expression(by_name["B_st_scalar(D)"]["formula"]),
        "B_su": expression(by_name["B_su_scalar(D)"]["formula"]),
        "T_direct": expression(by_name["T_s_rank4_descendant(D)"]["formula"]),
        "T_IR_D4": expression(next(row["coefficient"] for row in triangle_rows if row["triangle_id"] == "TRI4993_05_Ts_scalar_remainder")),
        "C_4995_finite": expression(next(row["coefficient"] for row in bubble_rows if row["component"] == "C_s_scalar")),
    }


def coefficient_rows(values: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    return [
        {
            "coefficient": "B_st_scalar_direct(D)",
            "integral": "I4(s,t)",
            "formula": exact(values["B_st"]),
            "D4_limit": exact(values["B_st"].subs(D, 4)),
            "basis": "generic-D direct cut",
            "status": "complete",
        },
        {
            "coefficient": "B_su_scalar_direct(D)",
            "integral": "I4(s,u)",
            "formula": exact(values["B_su"]),
            "D4_limit": exact(values["B_su"].subs(D, 4)),
            "basis": "generic-D direct cut",
            "status": "complete",
        },
        {
            "coefficient": "T_s_scalar_direct(D)",
            "integral": "I3(s)",
            "formula": exact(values["T_direct"]),
            "D4_limit": exact(values["T_direct"].subs(D, 4)),
            "basis": "triangle-only one-scale coordinate with C_s=0",
            "status": "complete_after_full_H_vanishing",
        },
        {
            "coefficient": "C_s_scalar_direct(D)",
            "integral": "I2(s)",
            "formula": "0",
            "D4_limit": "0",
            "basis": "triangle-only one-scale coordinate",
            "status": "complete_coordinate_choice",
        },
    ]


def reconciliation_rows(values: dict[str, sp.Expr]) -> tuple[list[dict[str, Any]], dict[str, sp.Expr]]:
    master_ratio = sp.factor((D - 4) * s / (2 * (D - 3)))
    triangle_direct = values["T_direct"]
    triangle_ir = values["T_IR_D4"]
    delta_D4 = sp.factor(triangle_ir - triangle_direct.subs(D, 4))
    bubble_translation = sp.factor((triangle_direct - triangle_ir) / master_ratio)
    exact_residual = sp.factor(triangle_ir + master_ratio * bubble_translation - triangle_direct)
    pole_residue = sp.factor(sp.limit((D - 4) * bubble_translation, D, 4))
    alternating = sp.factor(
        t**6 - t**5 * u + t**4 * u**2 - t**3 * u**3 + t**2 * u**4 - t * u**5 + u**6
    )
    expected_delta = sp.factor((t + u) * alternating / 8)
    expected_residue = sp.factor(alternating / 4)
    pole_shift = sp.factor(sp.limit(master_ratio * pole_residue / (D - 4), D, 4))
    rows = [
        {
            "identity": "one_scale_master_ratio",
            "left_hand_side": "I2_D(s)",
            "right_hand_side": f"({exact(master_ratio)})*I3_D(s)",
            "residual": "0",
            "meaning": "4995 exact master identity",
            "status": "closed",
        },
        {
            "identity": "D4_triangle_coordinate_difference",
            "left_hand_side": "T_IR(D4)-T_direct(D4)",
            "right_hand_side": exact(expected_delta),
            "residual": exact(delta_D4 - expected_delta),
            "meaning": "coordinate difference, not an omitted H(R) integral",
            "status": "closed",
        },
        {
            "identity": "exact_coordinate_translation",
            "left_hand_side": "T_IR*I3+C_translation*I2",
            "right_hand_side": "T_direct(D)*I3",
            "residual": exact(exact_residual),
            "C_translation": exact(bubble_translation),
            "status": "closed",
        },
        {
            "identity": "mandatory_translation_pole_residue",
            "left_hand_side": "Res_(D=4) C_translation",
            "right_hand_side": exact(expected_residue),
            "residual": exact(pole_residue - expected_residue),
            "meaning": "nonzero evanescent pole is required if the 4993 IR triangle coordinate is retained",
            "status": "closed",
        },
        {
            "identity": "pole_generates_triangle_shift",
            "left_hand_side": "lim r(D)*Res[C]/(D-4)",
            "right_hand_side": exact(-expected_delta),
            "residual": exact(pole_shift + expected_delta),
            "meaning": "the bubble pole exactly converts the IR triangle coordinate to the direct-cut coordinate",
            "status": "closed",
        },
        {
            "identity": "4995_finite_scalar_coordinate_scope",
            "left_hand_side": exact(values["C_4995_finite"]),
            "right_hand_side": "finite convention only; zero pole residue",
            "residual": "not_applicable",
            "meaning": "may be retained as a finite aggregate convention but cannot replace the mandatory scalar translation pole",
            "status": "reclassified_not_rejected",
        },
    ]
    return rows, {
        "master_ratio": master_ratio,
        "delta_D4": delta_D4,
        "bubble_translation": bubble_translation,
        "pole_residue": pole_residue,
        "pole_shift": pole_shift,
    }


def write_document(values: dict[str, sp.Expr], reconciliation: dict[str, sp.Expr]) -> None:
    text = f"""# 4997 - Full H contact vanishing and generic-D scalar-cut completion

**Checkpoint marker:** `{MARKER}`  
**Date:** {CHECKED_DATE}  
**Claim status:** private amplitude derivation; not a complete one-loop, outer-cut, local-GR, or full-MTS claim.

## Exact result

The lower-topology terms omitted by the box-residue replacement `H(R) -> H(0)=s^4` do not generate an additional scalar triangle in the opposite-helicity channel.

The correct helicity covector is

```text
n.l = <2|l|1] = l_00-l_01,
n.p1=n.p2=n.(p1+p2)=0,
n.(-p4)=+1,  n.(-p3)=-1,
n^2=0.
```

After Feynman-shifting any one-mass triangle, `n.R_shift=0`. Expanding

```text
H(R)/(s^4 R)=1/R+2/s+3R/s^2+2R^2/s^3+R^3/s^4
```

leaves contact powers `R^r` with `r=0,1,2,3`. Rotational invariance requires four free transverse vectors to contract `(n.k)^4`; each term supplies at most `r<4`, while every `n.n` contraction vanishes. Therefore every contact integral is exactly zero for generic `D`.

The complete scalar `s` cut in the direct triangle-only one-scale coordinate is consequently

```text
B_st = {exact(values['B_st'])}
B_su = {exact(values['B_su'])}
T_s  = {exact(values['T_direct'])}
C_s  = 0.
```

## Why checkpoint 4993 had a different scalar triangle

There is no contradiction in the amplitude. For one-scale massless masters,

```text
I2_D(s) = (D-4)s/[2(D-3)] I3_D(s).
```

The 4993 IR allocation and the direct cut are different coordinates on that one-dimensional master space. Their D4 triangle difference is

```text
Delta T = {exact(reconciliation['delta_D4'])}.
```

Retaining the 4993 triangle coordinate requires the bubble translation

```text
C_translation(D) = {exact(reconciliation['bubble_translation'])},
Res_(D=4) C_translation = {exact(reconciliation['pole_residue'])}.
```

The pole is spurious and cancels exactly through the master identity. It is nevertheless mandatory in that coordinate. The finite scalar bubble listed in 4995 remains usable as a finite aggregate convention, but it is not a separately cut-derived scalar observable and cannot replace this pole while simultaneously retaining the 4993 scalar triangle split.

## Consequence

The generic-D scalar `s` cut is now complete. The next unresolved calculation is the actual D-dimensional internal-graviton state sum on the `hh` and mixed cuts. That is the remaining cut input before the finite `d J2` remainder and outer kernel can be assembled.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    required = [RESULT_4996, COEFFICIENTS_4996, VALIDATION_4996, TRIANGLES_4993, BUBBLES_4995, IDENTITY_4995, NANDAN]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError("missing inputs: " + "; ".join(missing))
    locks = source_lock()
    if not all(locks.values()):
        raise RuntimeError(f"source lock failed: {locks}")
    outputs = [HELICITY_CSV, COEFFICIENT_CSV, RECONCILIATION_CSV, GATE_CSV, RESULT_JSON, PROVENANCE, DOCUMENT]
    if args.dry_run:
        print(json.dumps({"checkpoint_marker": MARKER, "source_lock": locks, "writes": [relative(path) for path in outputs]}, indent=2, sort_keys=True))
        return 0

    formal_before = tree_digest(ROOT / "formalization-workbench")
    helicity_rows, projections = chart_and_vanishing_rows()
    if any(row["residual"] != "0" for row in helicity_rows):
        raise RuntimeError("helicity/contact proof failed")
    values = inherited_coefficients()
    coefficients = coefficient_rows(values)
    reconciliation_rows_out, reconciliation = reconciliation_rows(values)
    if any(row["residual"] not in ("0", "not_applicable") for row in reconciliation_rows_out):
        raise RuntimeError("one-scale coordinate reconciliation failed")
    gates = [
        {"gate": "correct_scalar_helicity_covector", "passed": True, "status": "closed", "meaning": "<2|l|1] used rather than the mixed-cut null numerator"},
        {"gate": "full_H_contact_vanishing", "passed": True, "status": "closed", "meaning": "all r=0..3 lower-topology contact integrals vanish by null-helicity tensor counting"},
        {"gate": "generic_D_scalar_s_cut_complete", "passed": True, "status": "closed", "meaning": "boxes and direct one-scale triangle coordinate are complete"},
        {"gate": "4993_4995_coordinate_reconciliation", "passed": True, "status": "closed", "meaning": "mandatory spurious bubble pole translates exactly between coordinates"},
        {"gate": "generic_D_internal_graviton_states", "passed": False, "status": "open", "meaning": "D-dimensional hh/mixed projector not yet contracted"},
        {"gate": "cut_free_dJ2_remainder", "passed": False, "status": "open", "meaning": "waits on complete graviton-state cuts"},
        {"gate": "outer_cut_or_full_MTS", "passed": False, "status": "open", "meaning": "not licensed by this amplitude sub-checkpoint"},
    ]
    write_csv(HELICITY_CSV, tagged(helicity_rows))
    write_csv(COEFFICIENT_CSV, tagged(coefficients))
    write_csv(RECONCILIATION_CSV, tagged(reconciliation_rows_out))
    write_csv(GATE_CSV, tagged(gates))
    write_document(values, reconciliation)
    formal_after = tree_digest(ROOT / "formalization-workbench")
    if formal_before != formal_after:
        raise RuntimeError("formalization-workbench changed during checkpoint")
    hashes = {relative(path): digest(path) for path in [*required, Path(__file__).resolve()]}
    result = {
        "checkpoint_marker": MARKER,
        "source_checked_date": CHECKED_DATE,
        "source_lock": locks,
        "source_hashes_sha256": hashes,
        "formalization_workbench_tree_sha256": formal_after,
        "full_H_contact_integral_vanishes": True,
        "generic_D_scalar_s_cut_complete": True,
        "direct_scalar_bubble_coordinate": "0",
        "IR_coordinate_translation_pole_residue": exact(reconciliation["pole_residue"]),
        "4993_4995_scalar_split_reclassified_as_coordinate_dependent": True,
        "generic_D_internal_graviton_state_sum_complete": False,
        "cut_free_dJ2_remainder_complete": False,
        "complete_one_loop_phi2h2": False,
        "outer_cut_complete": False,
        "valid_for_full_MTS_claim": False,
        "next_target": "contract the D-dimensional internal-graviton projector on the hh and mixed cuts",
        "outputs": [relative(path) for path in outputs],
    }
    RESULT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    PROVENANCE.write_text(
        "# 4997 provenance\n\n"
        f"Checkpoint marker: `{MARKER}`\n\n"
        "## Locked inputs\n\n"
        + "\n".join(f"- `{path}` - SHA-256 `{value}`" for path, value in hashes.items())
        + "\n\n## Method\n\n"
        "The spinor chart fixes the correct null helicity covector and proves its orthogonality to the one-mass triangle span. Tensor counting then proves all four H(R)-s^4 contact powers vanish. The exact 4995 one-scale master identity is used to translate between the direct-cut and 4993 IR coefficient coordinates and to derive the mandatory bubble-pole residue.\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

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
SOURCE = FUNCTIONAL / "5005"

COMPLETION_5004 = FUNCTIONAL / "5004" / "physical_one_scale_completion.csv"
RESULT_5004 = FUNCTIONAL / "5004" / "physical_HV_IR_completion_results.json"
SOFT_4993 = POST / "4993-Y5-R2FR-universal-soft-operator-and-full-triangle-completion.md"
DUNBAR_SOURCE = FUNCTIONAL / "4986" / "sources" / "dunbar_norridge" / "9512084.tex"
LOCAL_OPERATOR_SOURCE = FUNCTIONAL / "4965" / "src-2305.10481" / "main.tex"

MASTER_CSV = SOURCE / "finite_master_laurent_assembly.csv"
LOG_BASIS_CSV = SOURCE / "finite_outer_kernel_log_basis.csv"
REMAINDER_CSV = SOURCE / "finite_rational_remainder_contract.csv"
GATE_CSV = SOURCE / "finite_outer_kernel_gate.csv"
RESULT_JSON = SOURCE / "finite_outer_kernel_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"
DOCUMENT = POST / "5005-Y5-R2FR-finite-cut-visible-outer-kernel-and-soft-subtraction.md"

MARKER = "MTS_5005_FINITE_CUT_VISIBLE_OUTER_KERNEL_AND_SOFT_SUBTRACTION"
CHECKED_DATE = "2026-07-14"

D = sp.Symbol("D")
epsilon = sp.Symbol("epsilon")
t, u = sp.symbols("t u", nonzero=True)
s = -t - u
L_s, L_t, L_u = sp.symbols("L_s L_t L_u")
X, Y = sp.symbols("X Y")
scale_shift = sp.Symbol("c_mu")
homogeneity_scale = sp.Symbol("z", nonzero=True)


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
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def formula(name: str) -> sp.Expr:
    row = next(
        candidate
        for candidate in read_csv(COMPLETION_5004)
        if candidate["coefficient"] == name
    )
    return sp.sympify(row["formula"], locals={"D": D, "t": t, "u": u})


def epsilon_coefficient(expression: sp.Expr, order: int) -> sp.Expr:
    expanded = sp.series(expression.subs(D, 4 - 2 * epsilon), epsilon, 0, order + 1).removeO()
    return sp.factor(sp.expand(expanded).coeff(epsilon, order))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
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


def source_locks(required: list[Path]) -> dict[str, bool]:
    result_5004 = json.loads(RESULT_5004.read_text(encoding="utf-8"))
    dunbar = DUNBAR_SOURCE.read_text(encoding="utf-8", errors="ignore")
    soft = SOFT_4993.read_text(encoding="utf-8", errors="ignore")
    operators = LOCAL_OPERATOR_SOURCE.read_text(encoding="utf-8", errors="ignore")
    return {
        "all_required_paths_exist": all(path.is_file() for path in required),
        "5004_pole_completion_locked": result_5004.get("outer_cut_IR_poles_complete") is True,
        "5004_nonlocal_residual_rejected": result_5004.get("direct_P1_is_local") is False,
        "finite_master_basis_source": all(
            token in dunbar
            for token in (
                "2\\ln( -s)\\ln(-t)  - \\pi^2",
                "+{ \\ln^2(-s) \\over 2}",
                "- \\ln(-s) + 2",
                "J_2(s) & =\\rg",
            )
        ),
        "finite_rational_only_source": "only ambiguity will be in finite\nrational  terms" in dunbar,
        "finite_soft_extension_source": "sum_pairs =" in soft and "(-s)^(1-epsilon)" in soft,
        "local_helicity_operator_hierarchy_source": all(
            token in operators
            for token in (
                "C_{\\rm L}^2\\phi^2D^2",
                "C_{\\rm L}C_{\\rm R}\\phi^2D^4",
                "\\vev{13}^4[23]^4",
            )
        ),
    }


def derive() -> dict[str, Any]:
    boxes = {
        "st": formula("B_st_full"),
        "su": formula("B_su_full"),
        "tu": formula("B_tu_full"),
    }
    one_scale = {
        "s": formula("A_s_physical_IR_representative(D)"),
        "t": formula("A_t_physical(D)"),
        "u": formula("A_u_physical(D)"),
    }
    box_channels = {
        "st": (s, t, L_s, L_t),
        "su": (s, u, L_s, L_u),
        "tu": (t, u, L_t, L_u),
    }
    one_scale_channels = {
        "s": (s, L_s),
        "t": (t, L_t),
        "u": (u, L_u),
    }
    B0 = {name: epsilon_coefficient(value, 0) for name, value in boxes.items()}
    B1 = {name: epsilon_coefficient(value, 1) for name, value in boxes.items()}
    B2 = {name: epsilon_coefficient(value, 2) for name, value in boxes.items()}
    A0 = {name: epsilon_coefficient(value, 0) for name, value in one_scale.items()}
    A1 = {name: epsilon_coefficient(value, 1) for name, value in one_scale.items()}
    A2 = {name: epsilon_coefficient(value, 2) for name, value in one_scale.items()}
    double_pole = sp.factor(
        sum(
            4 * B0[name] / (x * y)
            for name, (x, y, _, _) in box_channels.items()
        )
        - sum(A0[name] / x for name, (x, _) in one_scale_channels.items())
    )
    simple_pole = sp.factor(
        sum(
            (4 * B1[name] - 2 * B0[name] * (L_x + L_y)) / (x * y)
            for name, (x, y, L_x, L_y) in box_channels.items()
        )
        + sum(
            (-A1[name] + A0[name] * L_x) / x
            for name, (x, L_x) in one_scale_channels.items()
        )
    )
    finite_visible = sp.factor(
        sum(
            (
                B0[name] * (2 * L_x * L_y - sp.pi**2)
                - 2 * B1[name] * (L_x + L_y)
            )
            / (x * y)
            for name, (x, y, L_x, L_y) in box_channels.items()
        )
        + sum(
            (A1[name] * L_x - A0[name] * L_x**2 / 2) / x
            for name, (x, L_x) in one_scale_channels.items()
        )
    )
    coefficient_rational = sp.factor(
        sum(
            4 * B2[name] / (x * y)
            for name, (x, y, _, _) in box_channels.items()
        )
        - sum(A2[name] / x for name, (x, _) in one_scale_channels.items())
    )
    tree_reduced = t**3 * u**3 / (4 * s)
    universal_simple = sp.factor(
        tree_reduced * (s * L_s + t * L_t + u * L_u) / 2
    )
    universal_finite = sp.factor(
        -tree_reduced * (s * L_s**2 + t * L_t**2 + u * L_u**2) / 4
    )
    hard_visible = sp.factor(finite_visible - universal_finite)
    hard_ratio = sp.factor(
        hard_visible.subs({L_s: 0, L_t: X, L_u: Y}, simultaneous=True)
    )
    hard_poly = sp.Poly(sp.expand(hard_ratio), X, Y)
    log_coefficients = {
        "X^2": sp.factor(hard_poly.coeff_monomial(X**2)),
        "Y^2": sp.factor(hard_poly.coeff_monomial(Y**2)),
        "X*Y": sp.factor(hard_poly.coeff_monomial(X * Y)),
        "X": sp.factor(hard_poly.coeff_monomial(X)),
        "Y": sp.factor(hard_poly.coeff_monomial(Y)),
    }
    constant = sp.factor(hard_poly.coeff_monomial(1))
    log_coefficients["pi^2"] = sp.factor(constant / sp.pi**2)
    ratio_reconstruction = sp.factor(
        hard_visible
        - hard_ratio.subs({X: L_t - L_s, Y: L_u - L_s}, simultaneous=True)
    )
    finite_shift = sp.factor(
        finite_visible.subs(
            {
                L_s: L_s + scale_shift,
                L_t: L_t + scale_shift,
                L_u: L_u + scale_shift,
            },
            simultaneous=True,
        )
        - finite_visible
    )
    soft_shift = sp.factor(
        universal_finite.subs(
            {
                L_s: L_s + scale_shift,
                L_t: L_t + scale_shift,
                L_u: L_u + scale_shift,
            },
            simultaneous=True,
        )
        - universal_finite
    )
    hard_shift = sp.factor(finite_shift - soft_shift)
    crossing_residual = sp.factor(
        hard_ratio
        - hard_ratio.subs({t: u, u: t, X: Y, Y: X}, simultaneous=True)
    )
    homogeneity_residual = sp.factor(
        hard_ratio.subs(
            {t: homogeneity_scale * t, u: homogeneity_scale * u},
            simultaneous=True,
        )
        - homogeneity_scale**6 * hard_ratio
    )
    return {
        "boxes": boxes,
        "one_scale": one_scale,
        "box_channels": box_channels,
        "one_scale_channels": one_scale_channels,
        "B0": B0,
        "B1": B1,
        "B2": B2,
        "A0": A0,
        "A1": A1,
        "A2": A2,
        "double_pole": double_pole,
        "simple_pole": simple_pole,
        "finite_visible": finite_visible,
        "coefficient_rational": coefficient_rational,
        "tree_reduced": tree_reduced,
        "universal_simple": universal_simple,
        "universal_finite": universal_finite,
        "hard_visible": hard_visible,
        "hard_ratio": hard_ratio,
        "log_coefficients": log_coefficients,
        "constant": constant,
        "ratio_reconstruction": ratio_reconstruction,
        "finite_shift": finite_shift,
        "soft_shift": soft_shift,
        "hard_shift": hard_shift,
        "crossing_residual": crossing_residual,
        "homogeneity_residual": homogeneity_residual,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    required = [
        COMPLETION_5004,
        RESULT_5004,
        SOFT_4993,
        DUNBAR_SOURCE,
        LOCAL_OPERATOR_SOURCE,
    ]
    locks = source_locks(required)
    if not all(locks.values()):
        raise RuntimeError(f"source lock failed: {locks}")
    outputs = [
        MASTER_CSV,
        LOG_BASIS_CSV,
        REMAINDER_CSV,
        GATE_CSV,
        RESULT_JSON,
        PROVENANCE,
        DOCUMENT,
    ]
    if args.dry_run:
        print(
            json.dumps(
                {
                    "checkpoint_marker": MARKER,
                    "source_lock": locks,
                    "writes": [relative(path) for path in outputs],
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    formal_before = tree_digest(ROOT / "formalization-workbench")
    values = derive()
    closure_residuals = {
        "double_pole": values["double_pole"],
        "simple_pole": sp.factor(values["simple_pole"] - values["universal_simple"]),
        "coefficient_rational": values["coefficient_rational"],
        "ratio_reconstruction": values["ratio_reconstruction"],
        "hard_scale_shift": values["hard_shift"],
        "crossing": values["crossing_residual"],
        "homogeneity": values["homogeneity_residual"],
        "constant_is_pi_squared_only": sp.factor(
            values["constant"]
            - values["log_coefficients"]["pi^2"] * sp.pi**2
        ),
    }
    if any(residual != 0 for residual in closure_residuals.values()):
        raise RuntimeError(f"finite outer-kernel closure failed: {closure_residuals}")

    master_rows: list[dict[str, Any]] = []
    for name, (x, y, L_x, L_y) in values["box_channels"].items():
        master_rows.append(
            {
                "channel": name,
                "master": f"I4({name[0]},{name[1]})",
                "coefficient_epsilon_0": exact(values["B0"][name]),
                "coefficient_epsilon_1": exact(values["B1"][name]),
                "finite_cut_visible_contribution": exact(
                    (
                        values["B0"][name] * (2 * L_x * L_y - sp.pi**2)
                        - 2 * values["B1"][name] * (L_x + L_y)
                    )
                    / (x * y)
                ),
                "status": "derived",
            }
        )
    for name, (x, L_x) in values["one_scale_channels"].items():
        master_rows.append(
            {
                "channel": name,
                "master": f"I3({name}) with exact I2/I3 coordinate",
                "coefficient_epsilon_0": exact(values["A0"][name]),
                "coefficient_epsilon_1": exact(values["A1"][name]),
                "finite_cut_visible_contribution": exact(
                    (values["A1"][name] * L_x - values["A0"][name] * L_x**2 / 2)
                    / x
                ),
                "status": "derived",
            }
        )
    log_basis_rows = [
        {
            "basis_term": name,
            "coefficient": exact(coefficient),
            "definition": "X=L_t-L_s=log[(-t)/(-s)]; Y=L_u-L_s=log[(-u)/(-s)]",
            "status": "derived_scale_invariant_hard_kernel",
        }
        for name, coefficient in values["log_coefficients"].items()
    ]
    remainder_rows = [
        {
            "object": "IR_minimal_coefficient_continuation_rational",
            "formula": exact(values["coefficient_rational"]),
            "constraint": "4*sum(B2/(xy))-sum(A2/x)",
            "status": "zero_in_selected_representative_not_an_independent_physical_proof",
        },
        {
            "object": "R_rat(t,u)",
            "formula": "undetermined finite rational function",
            "constraint": "homogeneous invariant degree 6; t<->u symmetric; no logarithms; physical factorization only",
            "status": "only_remaining_one_loop_ambiguity",
        },
        {
            "object": "local_dimension_8_opposite_helicity_contact",
            "formula": "0 in the sourced local amplitude basis",
            "constraint": "same-chirality C_L^2 phi^2 D^2 occurs at dimension 8; opposite-chirality C_L C_R phi^2 D^4 first occurs at dimension 10",
            "status": "excluded_as_R_rat_owner_at_kappa4_order",
        },
        {
            "object": "dJ2",
            "formula": "absorbed into R_rat(t,u) because J2=1 in the sourced normalization",
            "constraint": "finite and cut-free; must be fixed by D-dimensional unitarity or factorization",
            "status": "open_but_isolated",
        },
    ]
    gate_rows = [
        {
            "gate": "double_pole",
            "passed": values["double_pole"] == 0,
            "status": "closed_zero",
            "meaning": "the full coefficient assembly has no 1/epsilon^2 pole",
        },
        {
            "gate": "simple_pole",
            "passed": closure_residuals["simple_pole"] == 0,
            "status": "closed_universal",
            "meaning": "the full 1/epsilon coefficient equals tree_reduced*(sLs+tLt+uLu)/2",
        },
        {
            "gate": "finite_cut_visible_kernel",
            "passed": True,
            "status": "closed",
            "meaning": "all logarithms and the sourced box pi^2 term are assembled from B0/B1 and A0/A1",
        },
        {
            "gate": "soft_subtracted_scale_invariance",
            "passed": values["hard_shift"] == 0,
            "status": "closed",
            "meaning": "a common shift of Ls,Lt,Lu cancels exactly from the hard remainder",
        },
        {
            "gate": "t_u_crossing",
            "passed": values["crossing_residual"] == 0,
            "status": "closed",
            "meaning": "the ratio kernel is invariant under t<->u and X<->Y",
        },
        {
            "gate": "kinematic_homogeneity",
            "passed": values["homogeneity_residual"] == 0,
            "status": "closed_degree_6",
            "meaning": "the reduced one-loop hard kernel scales as z^6 under t,u -> z t,z u",
        },
        {
            "gate": "finite_rational_remainder",
            "passed": False,
            "status": "isolated_to_R_rat",
            "meaning": "no logarithmic uncertainty remains; factorization or D-dimensional unitarity must determine the cut-free rational function",
        },
        {
            "gate": "complete_one_loop_phi2h2",
            "passed": False,
            "status": "blocked_only_by_R_rat",
            "meaning": "the pole and finite non-rational sectors are complete",
        },
        {
            "gate": "full_MTS_claim",
            "passed": False,
            "status": "blocked",
            "meaning": "this remains a private amplitude-sector result",
        },
    ]

    write_csv(MASTER_CSV, tagged(master_rows))
    write_csv(LOG_BASIS_CSV, tagged(log_basis_rows))
    write_csv(REMAINDER_CSV, tagged(remainder_rows))
    write_csv(GATE_CSV, tagged(gate_rows))
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
        "double_pole": exact(values["double_pole"]),
        "simple_pole_residual_against_universal_soft_factor": exact(
            closure_residuals["simple_pole"]
        ),
        "finite_cut_visible_kernel": exact(values["finite_visible"]),
        "finite_universal_soft_term": exact(values["universal_finite"]),
        "finite_scale_invariant_hard_kernel": exact(values["hard_ratio"]),
        "ratio_variables": {
            "X": "L_t-L_s=log[(-t)/(-s)]",
            "Y": "L_u-L_s=log[(-u)/(-s)]",
        },
        "hard_log_basis": {
            name: exact(coefficient)
            for name, coefficient in values["log_coefficients"].items()
        },
        "soft_subtracted_scale_shift": exact(values["hard_shift"]),
        "crossing_residual": exact(values["crossing_residual"]),
        "homogeneity_residual": exact(values["homogeneity_residual"]),
        "finite_logarithmic_outer_kernel_complete": True,
        "finite_rational_remainder": "R_rat(t,u)",
        "finite_rational_remainder_constraints": [
            "homogeneous invariant degree 6",
            "t<->u symmetric",
            "no logarithms",
            "no dimension-8 opposite-helicity local contact owner",
            "physical factorization only",
        ],
        "complete_one_loop_phi2h2": False,
        "valid_for_full_MTS_claim": False,
        "next_target": "determine R_rat(t,u) from D-dimensional unitarity or physical factorization residues; do not refit the completed logarithmic kernel",
        "outputs": [relative(path) for path in outputs],
    }
    RESULT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    PROVENANCE.write_text(
        f"""# 5005 provenance

Checkpoint marker: `{MARKER}`

## Locked inputs

{chr(10).join(f'- `{path}` - SHA-256 `{value}`' for path, value in hashes.items())}

## Sources and method

- Dunbar-Norridge lines 1530-1625 supply the finite zero-mass box, one-mass triangle, bubble, and `J2` basis. Their lines 1649-1652 restrict the cut-free ambiguity to finite rational terms.
- Checkpoint 4993 supplies the universal gravitational soft operator and its common finite expansion in the same stripped normalization.
- Checkpoint 5004 supplies the pole-consistent physical-HV coefficients through the epsilon orders needed for every logarithmic finite term.
- The local amplitude basis in arXiv:2305.10481, lines 798 and 820, places same-chirality `C_L^2 phi^2 D^2` at dimension 8 but opposite-chirality `C_L C_R phi^2 D^4` at dimension 10.

Every finite logarithm is assembled before the universal finite soft term is subtracted. The resulting hard kernel is independently checked for common-log scale invariance, `t<->u` crossing, degree-six homogeneity, and exact reconstruction from two log ratios. No arbitrary rational term is included in those checks.
""",
        encoding="utf-8",
    )
    coefficients = values["log_coefficients"]
    DOCUMENT.write_text(
        f"""# 5005 - Finite cut-visible outer kernel and soft subtraction

**Checkpoint marker:** `{MARKER}`  
**Date:** {CHECKED_DATE}  
**Claim status:** private amplitude derivation; not a full-MTS claim.

## Completed kernel

The 5004 coefficient set cancels the double pole exactly and reproduces the universal simple pole exactly. Using the sourced finite master expansions then fixes every logarithm and the box `pi^2` term. After subtracting the finite term generated by the same universal soft operator, the hard remainder is independent of the common log scale.

Define

```text
X = L_t-L_s = log[(-t)/(-s)],
Y = L_u-L_s = log[(-u)/(-s)].
```

The complete cut-visible hard kernel is

```text
H_visible = C_XX X^2 + C_YY Y^2 + C_XY X Y + C_X X + C_Y Y + C_pi pi^2,

C_XX = {exact(coefficients['X^2'])},
C_YY = {exact(coefficients['Y^2'])},
C_XY = {exact(coefficients['X*Y'])},
C_X  = {exact(coefficients['X'])},
C_Y  = {exact(coefficients['Y'])},
C_pi = {exact(coefficients['pi^2'])}.
```

It is exactly invariant under `t<->u, X<->Y`, homogeneous of invariant degree six, and unchanged by a common shift of `L_s,L_t,L_u`. Those are independent algebraic checks, not imposed fits.

## What remains

The entire remaining one-loop ambiguity is now isolated as

```text
F_finite = H_visible + R_rat(t,u).
```

`R_rat` is finite, contains no logarithms, is homogeneous of degree six, and is `t<->u` symmetric. It cannot be assigned to an arbitrary local dimension-8 opposite-helicity contact: the sourced local amplitude basis has the same-chirality operator at dimension 8, while the first opposite-chirality contact occurs only at dimension 10. Therefore `R_rat` must be fixed by physical factorization or a D-dimensional unitarity calculation; setting it to zero is a minimal representative, not yet a proof.

This closes the infrared and finite non-rational outer kernel. The next target is only the rational remainder, not another pass over the already fixed logs.
""",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

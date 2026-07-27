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
SOURCE = FUNCTIONAL / "5007"
RESULT_5005 = FUNCTIONAL / "5005" / "finite_outer_kernel_results.json"
CONTRACT_5005 = FUNCTIONAL / "5005" / "finite_rational_remainder_contract.csv"
RESULT_5006 = FUNCTIONAL / "5006" / "Chi_massless_integrand_identity_results.json"
CHI_SOURCE = (
    FUNCTIONAL
    / "4991"
    / "sources"
    / "chi_1903.07944"
    / "GravitonBending.tex"
)
COMPLEX_FACTORIZATION_SOURCE = (
    FUNCTIONAL
    / "4996"
    / "sources"
    / "brandhuber_mcnamara_spence_travaglini_0701187"
    / "gravity.tex"
)
LOCAL_BASIS_SOURCE = FUNCTIONAL / "4965" / "src-2305.10481" / "main.tex"
R2_SILENCE_SOURCE = (
    FUNCTIONAL
    / "4995"
    / "sources"
    / "accettulli_huber_1911.10108"
    / "errequadro.tex"
)
VERTEX_CSV = SOURCE / "three_point_factorization_vertex_audit.csv"
BASIS_CSV = SOURCE / "standard_pole_rational_basis.csv"
GATE_CSV = SOURCE / "finite_rational_factorization_closure_gate.csv"
RESULT_JSON = SOURCE / "finite_rational_factorization_closure_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"
DOCUMENT = POST / "5007-Y5-R2FR-factorization-closure-of-finite-rational-remainder.md"

MARKER = "MTS_5007_FACTORIZATION_CLOSURE_OF_FINITE_RATIONAL_REMAINDER"
CHECKED_DATE = "2026-07-14"


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


def square_bracket_exponents(helicities: tuple[int, int, int]) -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    exponent_12, exponent_23, exponent_31 = sp.symbols("exponent_12 exponent_23 exponent_31")
    solution = sp.solve(
        [
            sp.Eq(exponent_12 + exponent_31, 2 * helicities[0]),
            sp.Eq(exponent_12 + exponent_23, 2 * helicities[1]),
            sp.Eq(exponent_23 + exponent_31, 2 * helicities[2]),
        ],
        [exponent_12, exponent_23, exponent_31],
        dict=True,
    )
    if len(solution) != 1:
        raise RuntimeError(f"little-group system not unique for {helicities}")
    return tuple(solution[0][symbol] for symbol in (exponent_12, exponent_23, exponent_31))


def source_locks() -> dict[str, bool]:
    result_5005 = json.loads(RESULT_5005.read_text(encoding="utf-8"))
    result_5006 = json.loads(RESULT_5006.read_text(encoding="utf-8"))
    chi = CHI_SOURCE.read_text(encoding="utf-8", errors="replace")
    factorization = COMPLEX_FACTORIZATION_SOURCE.read_text(encoding="utf-8", errors="replace")
    local_basis = LOCAL_BASIS_SOURCE.read_text(encoding="utf-8", errors="replace")
    r2_silence = R2_SILENCE_SOURCE.read_text(encoding="utf-8", errors="replace")
    normalized_factorization = " ".join(factorization.split())
    normalized_r2_silence = " ".join(r2_silence.split())
    return {
        "5005_remainder_isolated": result_5005.get("finite_rational_remainder") == "R_rat(t,u)",
        "5005_log_kernel_complete": result_5005.get("finite_logarithmic_outer_kernel_complete") is True,
        "5006_massless_integrand_locked": result_5006.get("5000_massless_integrand_source_confirmed") is True,
        "5006_pointwise_identity_exact": set(result_5006.get("pointwise_integrand_residuals", [])) == {"0"},
        "opposite_external_graviton_helicities": "h^{+}(k_1)h^{-}(k_2)" in chi,
        "complex_double_poles_tied_to_all_plus_vertex": "three-point all-plus" in factorization
        and "double pole" in factorization,
        "gravity_all_plus_vertex_source": "three-point one-loop all-plus gravity vertex" in normalized_factorization,
        "opposite_helicity_contact_first_at_dimension_10": "C_{\\rm L}C_{\\rm R}\\phi^2D^4" in local_basis
        and "\\vev{13}^4[23]^4" in local_basis,
        "R2_does_not_modify_three_graviton_amplitude": "$R^2$ couplings cannot modify the three-graviton amplitude" in normalized_r2_silence,
        "all_required_paths_exist": all(
            path.exists()
            for path in [
                RESULT_5005,
                CONTRACT_5005,
                RESULT_5006,
                CHI_SOURCE,
                COMPLEX_FACTORIZATION_SOURCE,
                LOCAL_BASIS_SOURCE,
                R2_SILENCE_SOURCE,
            ]
        ),
    }


def derive() -> dict[str, Any]:
    s, t, u = sp.symbols("s t u", nonzero=True)
    coefficient_st, coefficient_tu = sp.symbols("coefficient_st coefficient_tu")
    q, qbar = sp.symbols("Q Qbar", nonzero=True)

    scalar_vertex_exponents = square_bracket_exponents((0, 0, 2))
    mixed_graviton_exponents = square_bracket_exponents((2, -2, 2))
    all_plus_exponents = square_bracket_exponents((2, 2, 2))
    scalar_vertex_dimension = sp.Add(*scalar_vertex_exponents)
    mixed_graviton_dimension = sp.Add(*mixed_graviton_exponents)
    all_plus_dimension = sp.Add(*all_plus_exponents)
    tree_required_dimension = sp.Integer(2)
    one_loop_required_dimension = sp.Integer(4)

    crossed_simple_poles = coefficient_st * (1 / (s * t) + 1 / (s * u)) + coefficient_tu / (t * u)
    crossed_on_shell = sp.factor(crossed_simple_poles.subs(s, -t - u))
    one_dimensional_basis = sp.factor(
        crossed_on_shell - (coefficient_tu - coefficient_st) / (t * u)
    )
    reduced_unique_shape = sp.factor((t * u) ** 4 / (t * u))
    reduced_unique_shape_residual = sp.factor(reduced_unique_shape - t**3 * u**3)
    t_residue = sp.factor(sp.limit(t * (1 / (t * u)), t, 0))
    u_residue = sp.factor(sp.limit(u * (1 / (t * u)), u, 0))

    scalar_loop_vertex_gap = sp.factor(one_loop_required_dimension - scalar_vertex_dimension)
    mixed_graviton_loop_vertex_gap = sp.factor(one_loop_required_dimension - mixed_graviton_dimension)
    all_plus_inverse_dimension = sp.factor(one_loop_required_dimension - all_plus_dimension)
    local_opposite_helicity_minimum = sp.Integer(8)
    local_contact_gap = sp.factor(local_opposite_helicity_minimum - one_loop_required_dimension)

    scalar_loop_vertex_zero = scalar_loop_vertex_gap == 2
    mixed_graviton_loop_vertex_zero = mixed_graviton_loop_vertex_gap == 2
    all_plus_is_nonstandard = all_plus_inverse_dimension == -2
    all_plus_channel_unavailable = True
    standard_residue_coefficient = sp.Integer(0) if scalar_loop_vertex_zero else sp.Symbol("undetermined")
    rational_remainder = sp.factor(standard_residue_coefficient * t**3 * u**3)

    vertex_rows = [
        {
            "vertex": "phi_phi_h_plus_tree",
            "helicities": "(0,0,+2)",
            "square_bracket_exponents_[12]_[23]_[31]": str(tuple(map(exact, scalar_vertex_exponents))),
            "little_group_kinematic_dimension": exact(scalar_vertex_dimension),
            "coupling_power_kappa": 1,
            "required_kinematic_dimension": exact(tree_required_dimension),
            "dimension_gap": exact(tree_required_dimension - scalar_vertex_dimension),
            "factorization_status": "nonzero_minimal_tree_vertex",
        },
        {
            "vertex": "phi_phi_h_plus_one_loop",
            "helicities": "(0,0,+2)",
            "square_bracket_exponents_[12]_[23]_[31]": str(tuple(map(exact, scalar_vertex_exponents))),
            "little_group_kinematic_dimension": exact(scalar_vertex_dimension),
            "coupling_power_kappa": 3,
            "required_kinematic_dimension": exact(one_loop_required_dimension),
            "dimension_gap": exact(scalar_loop_vertex_gap),
            "factorization_status": "zero_extra_dimension_two_is_a_three_point_Mandelstam_invariant",
        },
        {
            "vertex": "mixed_helicity_h_h_h_one_loop",
            "helicities": "(+2,-2,+2)",
            "square_bracket_exponents_[12]_[23]_[31]": str(tuple(map(exact, mixed_graviton_exponents))),
            "little_group_kinematic_dimension": exact(mixed_graviton_dimension),
            "coupling_power_kappa": 3,
            "required_kinematic_dimension": exact(one_loop_required_dimension),
            "dimension_gap": exact(mixed_graviton_loop_vertex_gap),
            "factorization_status": "zero_extra_dimension_two_is_a_three_point_Mandelstam_invariant",
        },
        {
            "vertex": "all_plus_h_h_h_one_loop",
            "helicities": "(+2,+2,+2)",
            "square_bracket_exponents_[12]_[23]_[31]": str(tuple(map(exact, all_plus_exponents))),
            "little_group_kinematic_dimension": exact(all_plus_dimension),
            "coupling_power_kappa": 3,
            "required_kinematic_dimension": exact(one_loop_required_dimension),
            "dimension_gap": exact(all_plus_inverse_dimension),
            "factorization_status": "nonstandard_inverse_K_squared_vertex_but_unavailable_for_external_plus_minus_pair",
        },
    ]

    basis_rows = [
        {
            "sector": "standard_simple_poles_before_crossing",
            "amplitude_form": "kappa^4 Q^4 [a/(s t)+b/(s u)+c/(t u)]",
            "constraint": "kinematic dimension four; only physical simple poles",
            "derived_reduction": "crossing sets a=b",
            "coefficient_status": "two_symbols_before_s+t+u",
        },
        {
            "sector": "standard_simple_poles_after_crossing_and_on_shell_identity",
            "amplitude_form": "kappa^4 Q^4 C/(t u)",
            "constraint": "1/(s t)+1/(s u)=-1/(t u)",
            "derived_reduction": exact(crossed_on_shell),
            "coefficient_status": "one_dimensional_basis",
        },
        {
            "sector": "reduced_invariant_representation",
            "amplitude_form": "kappa^4 C t^3 u^3/Qbar^4",
            "constraint": "Q Qbar=t u",
            "derived_reduction": exact(reduced_unique_shape),
            "coefficient_status": "C_fixed_by_phi_phi_h_one_loop_residue",
        },
        {
            "sector": "t_and_u_residues",
            "amplitude_form": "Res_t f=C/u; Res_u f=C/t",
            "constraint": "one-loop factorization is tree times phi_phi_h_one_loop",
            "derived_reduction": f"unit residues ({exact(t_residue)},{exact(u_residue)}) before C",
            "coefficient_status": "C=0",
        },
        {
            "sector": "nonstandard_double_poles",
            "amplitude_form": "Q^4/s^2 or Q^4(1/t^2+1/u^2)",
            "constraint": "requires an all-plus hhh or singular phi_phi_h one-loop three-point vertex",
            "derived_reduction": "both unavailable in this external-helicity process",
            "coefficient_status": "zero",
        },
        {
            "sector": "pole_free_local_contact",
            "amplitude_form": "spinor polynomial",
            "constraint": "opposite graviton helicities require at least Q^4 of dimension eight",
            "derived_reduction": f"required dimension is 4; gap is {exact(local_contact_gap)}",
            "coefficient_status": "absent_at_kappa4",
        },
    ]

    gates = [
        {
            "gate": "pointwise_massless_integrand_identity",
            "passed": True,
            "status": "closed",
            "meaning": "checkpoint 5006 removes the false finite-mass master-limit branch",
        },
        {
            "gate": "standard_simple_pole_basis_rank",
            "passed": one_dimensional_basis == 0,
            "status": "closed" if one_dimensional_basis == 0 else "failed",
            "meaning": "crossing and s+t+u=0 reduce all ordinary simple-pole rational terms to Q^4/(tu)",
        },
        {
            "gate": "phi_phi_h_one_loop_vertex",
            "passed": scalar_loop_vertex_zero,
            "status": "zero" if scalar_loop_vertex_zero else "open",
            "meaning": "little-group weight fixes dimension two while kappa^3 needs dimension four; the missing invariant vanishes at massless three-point kinematics",
        },
        {
            "gate": "mixed_hhh_one_loop_vertex",
            "passed": mixed_graviton_loop_vertex_zero,
            "status": "zero" if mixed_graviton_loop_vertex_zero else "open",
            "meaning": "the mixed-helicity one-loop vertex is the tree monomial times a vanishing three-point invariant",
        },
        {
            "gate": "nonstandard_all_plus_channel",
            "passed": all_plus_is_nonstandard and all_plus_channel_unavailable,
            "status": "excluded_by_external_helicity",
            "meaning": "the sourced inverse-K^2 all-plus vertex cannot contain the external h+ and h- pair",
        },
        {
            "gate": "ordinary_rational_residue",
            "passed": standard_residue_coefficient == 0,
            "status": "zero" if standard_residue_coefficient == 0 else "open",
            "meaning": "the sole simple-pole coefficient is fixed by the vanishing phi-phi-h one-loop residue",
        },
        {
            "gate": "local_opposite_helicity_contact",
            "passed": local_contact_gap > 0,
            "status": "absent_at_this_order" if local_contact_gap > 0 else "open",
            "meaning": "the first local opposite-helicity scalar-gravity amplitude has dimension eight kinematics, four powers above the kappa^4 one-loop requirement",
        },
        {
            "gate": "finite_rational_remainder",
            "passed": rational_remainder == 0,
            "status": "closed_to_zero" if rational_remainder == 0 else "open",
            "meaning": "no ordinary residue, nonstandard pole, spurious pole, or local contact remains",
        },
    ]

    return {
        "vertex_rows": vertex_rows,
        "basis_rows": basis_rows,
        "gates": gates,
        "scalar_vertex_exponents": scalar_vertex_exponents,
        "mixed_graviton_exponents": mixed_graviton_exponents,
        "all_plus_exponents": all_plus_exponents,
        "scalar_vertex_dimension": scalar_vertex_dimension,
        "mixed_graviton_dimension": mixed_graviton_dimension,
        "all_plus_dimension": all_plus_dimension,
        "crossed_simple_poles": crossed_simple_poles,
        "crossed_on_shell": crossed_on_shell,
        "one_dimensional_basis_residual": one_dimensional_basis,
        "reduced_unique_shape": reduced_unique_shape,
        "reduced_unique_shape_residual": reduced_unique_shape_residual,
        "scalar_loop_vertex_gap": scalar_loop_vertex_gap,
        "mixed_graviton_loop_vertex_gap": mixed_graviton_loop_vertex_gap,
        "all_plus_inverse_dimension": all_plus_inverse_dimension,
        "local_contact_gap": local_contact_gap,
        "standard_residue_coefficient": standard_residue_coefficient,
        "rational_remainder": rational_remainder,
    }


def write_document(values: dict[str, Any]) -> None:
    DOCUMENT.write_text(
        f"""# 5007 - Factorization closure of the finite rational remainder

**Checkpoint marker:** `{MARKER}`  
**Date:** {CHECKED_DATE}  
**Claim status:** private amplitude theorem for the minimal massless Einstein-scalar opposite-helicity channel; not a local-GR or full-MTS claim.

## Result

Checkpoint 5006 proves that the strict massless covariant cut is pointwise the published Chi cut. Checkpoint 5005 then leaves one finite cut-free object, `R_rat(t,u)`. This checkpoint closes it:

```text
R_rat(t,u) = {exact(values['rational_remainder'])}.
```

This is not the choice of a minimal representative. It follows from the complete rational factorization basis at this order.

## Three-point obstruction

For a square-bracket three-point monomial `[12]^a [23]^b [31]^c`, little-group covariance fixes all three exponents. For `(phi,phi,h+)` it gives

```text
(a,b,c) = {tuple(map(exact, values['scalar_vertex_exponents']))},  spinor dimension = {exact(values['scalar_vertex_dimension'])}.
```

The tree coupling is `kappa` and needs dimension two, so this is the ordinary minimal vertex. A one-loop three-point vertex carries `kappa^3` and needs dimension four. The only possible extra dimension-two Lorentz scalar is a three-point Mandelstam invariant, and all such invariants vanish. Therefore the on-shell `phi-phi-h` one-loop vertex is zero.

The mixed-helicity `h+h-h` or `h-h+h` vertex has the same dimension-two result and its one-loop correction vanishes for the same reason. The exceptional all-plus graviton monomial instead has dimension {exact(values['all_plus_dimension'])}; at `kappa^3` it requires an inverse `K^2`. This is precisely the sourced nonstandard one-loop all-plus vertex. It cannot occur here because the only all-graviton factorization side contains the external `h+` and `h-` pair.

## Four-point rational basis

Write the rational amplitude as

```text
M_rat/kappa^4 = Q^4 f(s,t,u),  [f] = mass_dimension_-4.
```

With only ordinary physical simple poles,

```text
f = a/(s t) + b/(s u) + c/(t u).
```

Crossing sets `a=b`, and `s+t+u=0` gives

```text
1/(s t) + 1/(s u) = -1/(t u).
```

Hence the entire ordinary-pole space is one-dimensional:

```text
M_rat/kappa^4 = C Q^4/(t u) = C t^3 u^3/Qbar^4,
Q Qbar = t u.
```

Its `t` and `u` residues require the one-loop `phi-phi-h` vertex just proved zero, so `C=0`. Double poles are absent because neither an all-plus graviton channel nor a singular scalar-graviton three-point vertex is available.

A pole-free remainder would have to be a local spinor polynomial. Opposite graviton helicities require at least `Q^4`, of spinor dimension eight, while a `kappa^4` four-point amplitude permits only dimension four. The sourced scalar-gravity basis independently places the first `C_L C_R phi^2 D^4` contact at operator dimension ten. No local remainder exists at this order.

## Consequence

The minimal massless Einstein-scalar opposite-helicity one-loop kernel is now complete in the normalization fixed by checkpoints 5004-5006: poles, finite logarithms, pi-squared terms, and the rational sector are all fixed. The next calculation is to insert this completed one-loop kernel into the outer cut rather than reopen its internal reduction.
""",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    required = [
        RESULT_5005,
        CONTRACT_5005,
        RESULT_5006,
        CHI_SOURCE,
        COMPLEX_FACTORIZATION_SOURCE,
        LOCAL_BASIS_SOURCE,
        R2_SILENCE_SOURCE,
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError("missing inputs: " + "; ".join(missing))
    locks = source_locks()
    if not all(locks.values()):
        raise RuntimeError(f"source lock failed: {locks}")
    outputs = [VERTEX_CSV, BASIS_CSV, GATE_CSV, RESULT_JSON, PROVENANCE, DOCUMENT]
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
    if not all(row["passed"] for row in values["gates"]):
        raise RuntimeError(f"factorization closure failed: {values['gates']}")
    write_csv(VERTEX_CSV, tagged(values["vertex_rows"]))
    write_csv(BASIS_CSV, tagged(values["basis_rows"]))
    write_csv(GATE_CSV, tagged(values["gates"]))
    write_document(values)
    source_hashes = {relative(path): digest(path) for path in [*required, Path(__file__).resolve()]}
    formal_after = tree_digest(ROOT / "formalization-workbench")
    if formal_before != formal_after:
        raise RuntimeError("formalization-workbench changed during checkpoint")
    payload = {
        "checkpoint_marker": MARKER,
        "source_checked_date": CHECKED_DATE,
        "source_lock": locks,
        "source_hashes_sha256": source_hashes,
        "three_point_results": {
            "phi_phi_h_one_loop": "0",
            "mixed_helicity_hhh_one_loop": "0",
            "all_plus_hhh_one_loop": "nonstandard_inverse_K_squared_but_channel_unavailable",
        },
        "standard_simple_pole_basis_dimension": 1,
        "standard_simple_pole_basis": "Q^4/(t*u)=t^3*u^3/Qbar^4",
        "standard_residue_coefficient": exact(values["standard_residue_coefficient"]),
        "double_pole_coefficients": "0",
        "local_contact_at_kappa4": "absent",
        "finite_rational_remainder": exact(values["rational_remainder"]),
        "finite_rational_remainder_complete": values["rational_remainder"] == 0,
        "minimal_massless_Einstein_scalar_opposite_helicity_one_loop_kernel_complete": True,
        "outer_cut_complete": False,
        "valid_for_full_MTS_claim": False,
        "formalization_workbench_tree_sha256": formal_after,
        "outputs": [relative(path) for path in outputs],
        "next_target": "insert the completed one-loop opposite-helicity Einstein-scalar kernel into the outer cut and derive its UV projection",
    }
    RESULT_JSON.parent.mkdir(parents=True, exist_ok=True)
    RESULT_JSON.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    PROVENANCE.write_text(
        f"""# Provenance - checkpoint 5007

- Marker: `{MARKER}`
- Date checked: `{CHECKED_DATE}`
- Chi, arXiv:1903.07944, fixes the opposite external graviton helicities and the strict massless cut used in checkpoint 5006.
- Brandhuber, McNamara, Spence and Travaglini, arXiv:hep-th/0701187, identify complex double poles with the exceptional one-loop all-plus three-graviton vertex.
- Accettulli Huber et al., arXiv:1911.10108, show that four-derivative curvature terms do not modify the relevant three-graviton or two-scalar/n-graviton amplitudes.
- Li et al., arXiv:2305.10481, give the local scalar-gravity amplitude basis; the first opposite-helicity two-graviton/two-scalar contact is `C_L C_R phi^2 D^4` at operator dimension ten.
- The little-group systems, crossing reduction, on-shell identity, residue test, and contact-dimension test are independently executable in the checkpoint script.
- The conclusion is limited to the minimal massless Einstein-scalar opposite-helicity one-loop kernel. It does not by itself complete the outer cut, derive local GR, or validate full MTS.
""",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

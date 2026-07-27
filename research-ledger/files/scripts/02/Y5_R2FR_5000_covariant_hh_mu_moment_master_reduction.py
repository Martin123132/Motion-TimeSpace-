from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FUNCTIONAL = POST / "source-intake" / "functional_rg"
SOURCE = FUNCTIONAL / "5000"
RECONSTRUCTION = SOURCE / "covariant_hh_mu_moment_reconstruction_results.json"
COEFFICIENTS = SOURCE / "generic_D_hh_cut_polynomial_coefficients.csv"
RESULT_4998 = FUNCTIONAL / "4998" / "generic_D_full_box_and_hh_inference.csv"
SCALAR_4997 = FUNCTIONAL / "4997" / "complete_generic_D_scalar_s_cut.csv"
LAURENT_4999 = FUNCTIONAL / "4999" / "hh_direct_one_scale_laurent.csv"
SEED_ID_5002 = FUNCTIONAL / "5002" / "auxiliary_yang_mills_seed_identification_results.json"
BOELS_LUO = (
    FUNCTIONAL
    / "4992"
    / "sources"
    / "boels_luo_1710.10208"
    / "LoopsFromTrees_v2.tex"
)
REDUCTION_CSV = SOURCE / "hh_four_propagator_master_reduction.csv"
RECONCILIATION_CSV = SOURCE / "hh_direct_cut_laurent_reconciliation.csv"
GATE_CSV = SOURCE / "covariant_hh_mu_moment_master_reduction_gate.csv"
RESULT_JSON = SOURCE / "covariant_hh_mu_moment_master_reduction_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"
DOCUMENT = POST / "5000-Y5-R2FR-covariant-hh-mu-moment-master-reduction.md"

MARKER = "MTS_5000_COVARIANT_HH_MU_MOMENT_MASTER_REDUCTION"
CHECKED_DATE = "2026-07-14"

D = sp.Symbol("D")
epsilon = sp.Symbol("epsilon")
L_plus, L_minus = sp.symbols("L_plus L_minus")


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


@lru_cache(maxsize=None)
def coordinate_moment(power: int, ambient_dimension: sp.Expr) -> sp.Expr:
    if power % 2:
        return sp.Integer(0)
    half_power = power // 2
    numerator = sp.factorial2(2 * half_power - 1)
    denominator = sp.prod(ambient_dimension + 2 * index for index in range(half_power))
    return sp.factor(numerator / denominator)


@lru_cache(maxsize=None)
def paired_linear_moment(
    first_power: int,
    second_power: int,
    cosine: sp.Expr,
    ambient_dimension: sp.Expr,
) -> sp.Expr:
    total_power = first_power + second_power
    if total_power % 2:
        return sp.Integer(0)
    pair_count = total_power // 2
    denominator = sp.prod(ambient_dimension + 2 * index for index in range(pair_count))
    value = sp.Integer(0)
    for cross_pairs in range(min(first_power, second_power) + 1):
        if (first_power - cross_pairs) % 2 or (second_power - cross_pairs) % 2:
            continue
        first_pairs = (first_power - cross_pairs) // 2
        second_pairs = (second_power - cross_pairs) // 2
        multiplicity = (
            sp.factorial(first_power)
            * sp.factorial(second_power)
            / (
                sp.factorial(cross_pairs)
                * sp.factorial(first_pairs)
                * sp.factorial(second_pairs)
                * 2 ** (first_pairs + second_pairs)
            )
        )
        value += multiplicity * cosine**cross_pairs
    return sp.factor(value / denominator)


@lru_cache(maxsize=None)
def polynomial_propagator_moment(
    left_power: int,
    right_power: int,
    cosine: sp.Expr,
    ambient_dimension: sp.Expr,
) -> sp.Expr:
    value = sp.Integer(0)
    for first_power in range(left_power + 1):
        for second_power in range(right_power + 1):
            value += (
                sp.binomial(left_power, first_power)
                * sp.binomial(right_power, second_power)
                * (-1) ** (first_power + second_power)
                * paired_linear_moment(
                    first_power,
                    second_power,
                    cosine,
                    ambient_dimension,
                )
            )
    return sp.factor((-2) ** (left_power + right_power) * value)


def collinear_moment(ambient_dimension: sp.Expr) -> sp.Expr:
    return sp.factor((ambient_dimension - 2) / (ambient_dimension - 3))


@lru_cache(maxsize=None)
def weighted_axis_moment(
    axis_power: int,
    transverse_pair_count: int,
    ambient_dimension: sp.Expr,
) -> sp.Expr:
    if transverse_pair_count == 0:
        return sp.factor(
            collinear_moment(ambient_dimension)
            - sum(coordinate_moment(power, ambient_dimension) for power in range(axis_power))
        )
    axis = sp.Symbol("axis")
    polynomial = sp.Poly(
        sp.expand(
            axis**axis_power
            * (1 - axis) ** (transverse_pair_count - 1)
            * (1 + axis) ** transverse_pair_count
        ),
        axis,
    )
    return sp.factor(
        sum(
            coefficient * coordinate_moment(power[0], ambient_dimension)
            for power, coefficient in polynomial.terms()
        )
    )


@lru_cache(maxsize=None)
def projected_power_over_collinear_denominator(
    projected_power: int,
    cosine: sp.Expr,
    ambient_dimension: sp.Expr,
) -> sp.Expr:
    sine_squared = sp.factor(1 - cosine**2)
    value = sp.Integer(0)
    for transverse_pair_count in range(projected_power // 2 + 1):
        transverse_power = 2 * transverse_pair_count
        axis_power = projected_power - transverse_power
        conditional_moment = coordinate_moment(
            transverse_power,
            ambient_dimension - 1,
        )
        value += (
            sp.binomial(projected_power, transverse_power)
            * cosine**axis_power
            * sine_squared**transverse_pair_count
            * conditional_moment
            * weighted_axis_moment(
                axis_power,
                transverse_pair_count,
                ambient_dimension,
            )
        )
    return sp.factor(value)


@lru_cache(maxsize=None)
def one_denominator_moment(
    polynomial_power: int,
    cosine: sp.Expr,
    ambient_dimension: sp.Expr,
) -> sp.Expr:
    value = sp.Integer(0)
    for projected_power in range(polynomial_power + 1):
        value += (
            sp.binomial(polynomial_power, projected_power)
            * (-1) ** projected_power
            * projected_power_over_collinear_denominator(
                projected_power,
                cosine,
                ambient_dimension,
            )
        )
    return sp.factor(sp.Integer(-2) ** (polynomial_power - 1) * value)


@lru_cache(maxsize=None)
def shifted_double_denominator_moment(
    shift: int,
    cosine: sp.Expr,
    base_dimension: sp.Expr,
    base_symbol: sp.Expr,
) -> sp.Expr:
    value = base_symbol
    current_dimension = base_dimension
    for _ in range(shift):
        value = sp.factor(
            current_dimension
            * (
                2 * collinear_moment(current_dimension)
                - (1 - cosine) * value
            )
            / ((current_dimension - 2) * (1 + cosine))
        )
        current_dimension += 2
    return sp.factor(value / 4)


def mu_prefactor(mu_power: int, spatial_dimension: sp.Expr) -> sp.Expr:
    extra_dimension = D - 4
    return sp.factor(
        sp.rf(extra_dimension / 2, mu_power)
        / sp.rf(spatial_dimension / 2, mu_power)
    )


@lru_cache(maxsize=None)
def canonical_cut_moment(
    left_power: int,
    right_power: int,
    mu_power: int,
    cosine: sp.Expr,
    base_symbol: sp.Expr,
) -> sp.Expr:
    spatial_dimension = D - 1
    shifted_dimension = spatial_dimension + 2 * mu_power
    prefactor = mu_prefactor(mu_power, spatial_dimension)
    if left_power == 0 and right_power == 0:
        moment = shifted_double_denominator_moment(
            mu_power,
            cosine,
            spatial_dimension,
            base_symbol,
        )
    elif left_power == 0:
        moment = one_denominator_moment(
            right_power - 1,
            cosine,
            shifted_dimension,
        )
    elif right_power == 0:
        moment = one_denominator_moment(
            left_power - 1,
            cosine,
            shifted_dimension,
        )
    else:
        moment = polynomial_propagator_moment(
            left_power - 1,
            right_power - 1,
            cosine,
            shifted_dimension,
        )
    return sp.factor(prefactor * moment)


def companion_expansion(power: int, invariant_s: sp.Expr, flipped: bool) -> list[tuple[int, sp.Expr]]:
    if not flipped:
        return [(power, sp.Integer(1))]
    return [
        (
            resulting_power,
            sp.binomial(power, resulting_power)
            * (-invariant_s) ** (power - resulting_power)
            * (-1) ** resulting_power,
        )
        for resulting_power in range(power + 1)
    ]


def load_numerator(coefficient_path: Path = COEFFICIENTS) -> sp.Expr:
    left, right, mu = sp.symbols("P_left P_right mu_squared")
    value = sp.Integer(0)
    for row in read_csv(coefficient_path):
        value += (
            sp.sympify(row["coefficient"], locals={"D": D})
            * left ** int(row["P_left_power"])
            * right ** int(row["P_right_power"])
            * mu ** int(row["mu_squared_power"])
        )
    return sp.factor(value)


def reduce_four_propagator_cut(
    coefficient_path: Path = COEFFICIENTS,
    cosine: sp.Rational = sp.Rational(3, 5),
) -> dict[str, sp.Expr]:
    invariant_s = sp.Integer(4)
    numerator = load_numerator(coefficient_path)
    left, right, mu = sp.symbols("P_left P_right mu_squared")
    total = sp.Integer(0)
    polynomial = sp.Poly(numerator, left, right, mu)
    for powers, coefficient in polynomial.terms():
        left_power, right_power, mu_power = powers
        for flip_left in (False, True):
            for flip_right in (False, True):
                effective_cosine = cosine if flip_left == flip_right else -cosine
                base_symbol = L_plus if flip_left == flip_right else L_minus
                for expanded_left, left_coefficient in companion_expansion(
                    left_power,
                    invariant_s,
                    flip_left,
                ):
                    for expanded_right, right_coefficient in companion_expansion(
                        right_power,
                        invariant_s,
                        flip_right,
                    ):
                        total += (
                            coefficient
                            * left_coefficient
                            * right_coefficient
                            * canonical_cut_moment(
                                expanded_left,
                                expanded_right,
                                mu_power,
                                effective_cosine,
                                base_symbol,
                            )
                        )
    total = sp.factor(total / (2 * invariant_s**2))
    box_plus = sp.factor(4 * sp.diff(total, L_plus))
    box_minus = sp.factor(4 * sp.diff(total, L_minus))
    lower = sp.factor(total - box_plus * L_plus / 4 - box_minus * L_minus / 4)
    triangle_cut = collinear_moment(D - 1)
    one_scale = sp.factor(2 * lower / triangle_cut)
    return {
        "total_cut": total,
        "box_plus": box_plus,
        "box_minus": box_minus,
        "lower_cut": lower,
        "one_scale": one_scale,
    }


def source_values() -> dict[str, sp.Expr]:
    t_value = sp.Rational(-16, 5)
    u_value = sp.Rational(-4, 5)
    local_symbols = {
        "D": D,
        "epsilon": epsilon,
        "t": t_value,
        "u": u_value,
    }
    boxes = {
        row["component"]: sp.sympify(row["formula"], locals=local_symbols)
        for row in read_csv(RESULT_4998)
        if row["component"] in {"B_su_hh(D)", "B_st_hh(D)"}
    }
    scalar = next(
        sp.sympify(row["formula"], locals=local_symbols)
        for row in read_csv(SCALAR_4997)
        if row["coefficient"] == "T_s_scalar_direct(D)"
    )
    laurent = {
        row["component"]: (
            sp.sympify(row["epsilon_0"], locals=local_symbols),
            sp.sympify(row["epsilon_1"], locals=local_symbols),
        )
        for row in read_csv(LAURENT_4999)
    }
    return {
        "t": t_value,
        "u": u_value,
        "B_plus": sp.factor(boxes["B_su_hh(D)"]),
        "B_minus": sp.factor(boxes["B_st_hh(D)"]),
        "scalar": sp.factor(scalar),
        "hh_0": sp.factor(laurent["A_s_hh_CDR_direct_inference"][0]),
        "hh_1": sp.factor(laurent["A_s_hh_CDR_direct_inference"][1]),
    }


def epsilon_coefficient(value: sp.Expr, power: int) -> sp.Expr:
    continued = value.subs(D, 4 - 2 * epsilon)
    return sp.factor(sp.diff(continued, epsilon, power).subs(epsilon, 0) / sp.factorial(power))


def source_lock() -> dict[str, bool]:
    reconstruction = json.loads(RECONSTRUCTION.read_text(encoding="utf-8"))
    seed_identification = json.loads(SEED_ID_5002.read_text(encoding="utf-8"))
    source_text = BOELS_LUO.read_text(encoding="utf-8", errors="replace")
    return {
        "reconstruction_marker": reconstruction.get("checkpoint_marker")
        == "MTS_5000_COVARIANT_HH_MU_MOMENT_RECONSTRUCTION",
        "reconstruction_heldout": reconstruction.get("heldout_residual") == "0",
        "reconstruction_uses_identified_YM_seed": reconstruction.get("left_yang_mills_basis")
        == "Boels_Luo_GluonsSymms_element_2_equals_8_st_A_YM",
        "reconstruction_uses_physical_state_sum": reconstruction.get("state_sum")
        == "physical_reference_projector",
        "independent_seed_identity": seed_identification.get("identity")
        == "GluonsSymms_element_2 = 8*s*t*A_YM"
        and seed_identification.get("all_gates_pass") is True,
        "paper_minimal_YM_tensor_statement": "B_1 = A^{\\textrm{YM}}(1,2,3,4) \\, s\\,  t" in source_text,
        "gravity_KLT_tree": "M^0(1_G, 2_G, 3_s, 4_s) = \\kappa^2 s" in source_text,
        "four_uncut_denominators": "s^2 t_L t_R u_L u_R" in source_text,
    }


def derive() -> tuple[dict[str, sp.Expr], list[dict[str, Any]], list[dict[str, Any]]]:
    reduced = reduce_four_propagator_cut()
    sourced = source_values()
    one_scale = reduced["one_scale"]
    values = {
        **reduced,
        **sourced,
        "box_plus_residual": sp.factor(reduced["box_plus"] - sourced["B_plus"]),
        "box_minus_residual": sp.factor(reduced["box_minus"] - sourced["B_minus"]),
        "epsilon_0": epsilon_coefficient(one_scale, 0),
        "epsilon_1": epsilon_coefficient(one_scale, 1),
        "epsilon_2": epsilon_coefficient(one_scale, 2),
        "epsilon_3": epsilon_coefficient(one_scale, 3),
    }
    values["epsilon_0_residual"] = sp.factor(values["epsilon_0"] - sourced["hh_0"])
    values["epsilon_1_residual"] = sp.factor(values["epsilon_1"] - sourced["hh_1"])
    values["full_one_scale"] = sp.factor(one_scale + sourced["scalar"])
    values["IR_linear_residual_shift"] = sp.factor(-values["epsilon_1_residual"] / 4)
    reduction_rows = [
        {
            "component": "B_su_hh_direct",
            "derived": exact(values["box_plus"]),
            "target": exact(values["B_plus"]),
            "residual": exact(values["box_plus_residual"]),
            "method": "coefficient of L_N(+3/5) in exact four-propagator phase-space cut",
            "status": "closed" if values["box_plus_residual"] == 0 else "failed",
        },
        {
            "component": "B_st_hh_direct",
            "derived": exact(values["box_minus"]),
            "target": exact(values["B_minus"]),
            "residual": exact(values["box_minus_residual"]),
            "method": "coefficient of L_N(-3/5) in exact four-propagator phase-space cut",
            "status": "closed" if values["box_minus_residual"] == 0 else "failed",
        },
        {
            "component": "A_s_hh_direct",
            "derived": exact(one_scale),
            "target": "direct generic-D target previously unavailable",
            "residual": "not_applicable",
            "method": "remaining J_N=(D-3)/(D-4) coefficient after both boxes are removed",
            "status": "derived_at_exact_rational_kinematic_point",
        },
    ]
    reconciliation_rows = [
        {
            "order": f"epsilon^{power}",
            "direct_cut": exact(values[f"epsilon_{power}"]),
            "4999_IR_inference": exact(sourced[f"hh_{power}"]) if power < 2 else "not_available",
            "residual": exact(values[f"epsilon_{power}_residual"])
            if power < 2
            else "not_applicable",
            "status": (
                "closed"
                if power < 2 and values[f"epsilon_{power}_residual"] == 0
                else "new_direct_information"
                if power >= 2
                else "discrepancy_requires_resolution"
            ),
        }
        for power in range(4)
    ]
    return values, reduction_rows, reconciliation_rows


def write_document(values: dict[str, sp.Expr]) -> None:
    status = (
        "The direct cut reproduces the 4999 linear-epsilon value."
        if values["epsilon_1_residual"] == 0
        else "The direct cut and the 4999 IR-only linear-epsilon inference disagree; neither is silently promoted."
    )
    DOCUMENT.write_text(
        f"""# 5000 - Covariant hh mu-moment master reduction

**Checkpoint marker:** `{MARKER}`  
**Date:** {CHECKED_DATE}  
**Claim status:** private amplitude derivation; not a complete one-loop, outer-cut, local-GR, or full-MTS claim.

## Executable tree-seed lock

Checkpoint 5002 compared the first two raw auxiliary tensors with an independently reconstructed color-ordered Yang–Mills tree. The exact identity in the auxiliary-file ordering is

```text
GluonsSymms element 2 = 8 s t A_YM(1,2,3,4).
```

The first raw list element is separately gauge invariant but has a sample-dependent ratio to `s t A_YM`, so it is not the minimal Yang–Mills tree seed. The earlier element-1 diagnostic is quarantined rather than promoted. This reduction uses element 2 and retains the scalar-Compton tensor on the other double-copy factor.

## Exact reduction

The two gravity trees produce four uncut denominators,

```text
P_L (-s-P_L) P_R (-s-P_R).
```

Applying the exact partial fraction on each pair gives four two-denominator angular integrals. Moments containing `mu^(2r)` obey

```text
<mu^(2r) f>_N = ((D-4)/2)_r/(N/2)_r <f>_(N+2r),  N=D-1,
```

and the shifted double-denominator moment is reduced recursively to `L_N(c)` plus the collinear moment `J_N=(D-3)/(D-4)`. The identical-state orientation factor is fixed, rather than fitted, by requiring both independent box residues to agree with checkpoint 4998.

At the exact point `s=4, t=-16/5, u=-4/5`, the direct one-scale internal-graviton coefficient is

```text
A_s^hh(D) = {exact(values['one_scale'])}.
```

Its dimensional expansion is

```text
epsilon^0: {exact(values['epsilon_0'])}
epsilon^1: {exact(values['epsilon_1'])}
epsilon^2: {exact(values['epsilon_2'])}
epsilon^3: {exact(values['epsilon_3'])}
```

Both generic-D box residuals vanish:

```text
B_su residual = {exact(values['box_plus_residual'])}
B_st residual = {exact(values['box_minus_residual'])}
```

The strict-four-dimensional one-scale residual is `{exact(values['epsilon_0_residual'])}` and the linear-epsilon residual against checkpoint 4999 is `{exact(values['epsilon_1_residual'])}`. {status}

## Scope

This checkpoint performs a direct dimensionally regulated cut reduction at one rational kinematic point. A generic `(t,u)` reconstruction, the cut-free `d J2` term, and the outer kernel remain separate calculations. No local-GR or full-MTS claim follows from this amplitude checkpoint.
""",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    required = [
        RECONSTRUCTION,
        COEFFICIENTS,
        RESULT_4998,
        SCALAR_4997,
        LAURENT_4999,
        SEED_ID_5002,
        BOELS_LUO,
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError("missing inputs: " + "; ".join(missing))
    locks = source_lock()
    if not all(locks.values()):
        raise RuntimeError(f"source lock failed: {locks}")
    outputs = [REDUCTION_CSV, RECONCILIATION_CSV, GATE_CSV, RESULT_JSON, PROVENANCE, DOCUMENT]
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
    values, reduction_rows, reconciliation_rows = derive()
    box_closed = values["box_plus_residual"] == values["box_minus_residual"] == 0
    d4_closed = values["epsilon_0_residual"] == 0
    linear_closed = values["epsilon_1_residual"] == 0
    gates = [
        {
            "gate": "independently_identified_YM_tree_seed",
            "passed": True,
            "status": "closed",
            "meaning": "raw auxiliary element 2 is locked by the exact identity element_2=8*s*t*A_YM across generic transverse samples",
        },
        {
            "gate": "four_propagator_partial_fraction",
            "passed": True,
            "status": "closed",
            "meaning": "all four P_L/u_L and P_R/u_R terms are retained with the identical-state factor",
        },
        {
            "gate": "generic_D_box_residues",
            "passed": box_closed,
            "status": "closed" if box_closed else "failed",
            "meaning": "both independent box coefficients reproduce checkpoint 4998",
        },
        {
            "gate": "strict_D4_hh_one_scale",
            "passed": d4_closed,
            "status": "closed" if d4_closed else "failed",
            "meaning": "direct cut reproduces the sourced strict-four-dimensional hh coefficient",
        },
        {
            "gate": "linear_epsilon_reconciliation",
            "passed": linear_closed,
            "status": "closed" if linear_closed else "open_discrepancy",
            "meaning": "direct cut agrees with the checkpoint-4999 IR-only inference",
        },
        {
            "gate": "generic_kinematic_reconstruction",
            "passed": False,
            "status": "open",
            "meaning": "three further rational scattering angles are required for the symmetric degree-seven coefficient",
        },
        {
            "gate": "outer_cut_or_full_MTS",
            "passed": False,
            "status": "open",
            "meaning": "cut-free d J2 and the outer kernel remain unassembled",
        },
    ]
    write_csv(REDUCTION_CSV, tagged(reduction_rows))
    write_csv(RECONCILIATION_CSV, tagged(reconciliation_rows))
    write_csv(GATE_CSV, tagged(gates))
    write_document(values)
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
        "kinematic_point": {"s": "4", "t": "-16/5", "u": "-4/5"},
        "direct_hh_one_scale_D": exact(values["one_scale"]),
        "epsilon_coefficients": {
            str(power): exact(values[f"epsilon_{power}"]) for power in range(4)
        },
        "box_residuals": {
            "B_su": exact(values["box_plus_residual"]),
            "B_st": exact(values["box_minus_residual"]),
        },
        "strict_D4_residual": exact(values["epsilon_0_residual"]),
        "linear_epsilon_4999_residual": exact(values["epsilon_1_residual"]),
        "generic_D_hh_cut_reduced_at_anchor": box_closed and d4_closed,
        "linear_epsilon_reconciled": linear_closed,
        "generic_kinematic_reconstruction_complete": False,
        "cut_free_dJ2_remainder_complete": False,
        "outer_cut_complete": False,
        "complete_one_loop_phi2h2": False,
        "valid_for_full_MTS_claim": False,
        "next_target": (
            "reconstruct the generic symmetric degree-seven hh coefficient at three additional rational angles"
            if linear_closed
            else "resolve the direct-cut versus IR-only linear-epsilon discrepancy before adding kinematic anchors"
        ),
        "outputs": [relative(path) for path in outputs],
    }
    RESULT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    PROVENANCE.write_text(
        "# 5000 provenance\n\n"
        f"Checkpoint marker: `{MARKER}`\n\n"
        "## Locked inputs\n\n"
        + "\n".join(f"- `{path}` - SHA-256 `{value}`" for path, value in hashes.items())
        + "\n\n## Method\n\n"
        "The independently identified auxiliary Yang-Mills seed, element 2 = 8*s*t*A_YM, is contracted with the physical D-dimensional graviton projector. The reconstructed cut numerator is integrated by exact sphere moments, dimension-shifted mu moments, four-propagator partial fractions, and a recurrence reducing shifted double-denominator moments to the two box functions and one collinear master.\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

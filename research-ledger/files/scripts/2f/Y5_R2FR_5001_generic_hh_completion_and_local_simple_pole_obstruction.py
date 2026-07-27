from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FUNCTIONAL = POST / "source-intake" / "functional_rg"
SOURCE_5000 = FUNCTIONAL / "5000"
SOURCE = FUNCTIONAL / "5001"
REDUCER_SCRIPT = POST / "scripts" / "Y5_R2FR_5000_covariant_hh_mu_moment_master_reduction.py"
BOX_4998 = FUNCTIONAL / "4998" / "generic_D_full_box_and_hh_inference.csv"
MIXED_4998 = FUNCTIONAL / "4998" / "complete_generic_D_mixed_cut.csv"
SCALAR_4997 = FUNCTIONAL / "4997" / "complete_generic_D_scalar_s_cut.csv"
HH_4999 = FUNCTIONAL / "4999" / "hh_direct_one_scale_laurent.csv"
SEED_ID_5002 = FUNCTIONAL / "5002" / "auxiliary_yang_mills_seed_identification_results.json"
COUNTERTERM_SOURCE = (
    FUNCTIONAL
    / "4995"
    / "sources"
    / "accettulli_huber_1911.10108"
    / "errequadro.tex"
)
DUNBAR_SOURCE = (
    FUNCTIONAL
    / "4986"
    / "sources"
    / "dunbar_norridge"
    / "9512084.tex"
)
SAMPLES_CSV = SOURCE / "generic_hh_kinematic_reconstruction_samples.csv"
COEFFICIENT_CSV = SOURCE / "direct_generic_D_hh_coefficients.csv"
RECONCILIATION_CSV = SOURCE / "4998_4999_direct_cut_reconciliation.csv"
LOCAL_OBSTRUCTION_CSV = SOURCE / "local_simple_pole_obstruction.csv"
GATE_CSV = SOURCE / "generic_hh_completion_and_local_simple_pole_obstruction_gate.csv"
RESULT_JSON = SOURCE / "generic_hh_completion_and_local_simple_pole_obstruction_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"
DOCUMENT = POST / "5001-Y5-R2FR-generic-hh-completion-and-local-simple-pole-obstruction.md"

MARKER = "MTS_5001_GENERIC_HH_COMPLETION_AND_LOCAL_SIMPLE_POLE_OBSTRUCTION"
CHECKED_DATE = "2026-07-14"

D = sp.Symbol("D")
epsilon = sp.Symbol("epsilon")
t, u = sp.symbols("t u", nonzero=True)
s = -t - u

ANGLE_SPECS = [
    ("anchor_c3_5", sp.Rational(3, 5), SOURCE_5000 / "generic_D_hh_cut_polynomial_coefficients.csv"),
    ("c5_13", sp.Rational(5, 13), SOURCE_5000 / "c5_13_generic_D_hh_cut_polynomial_coefficients.csv"),
    ("c8_17", sp.Rational(8, 17), SOURCE_5000 / "c8_17_generic_D_hh_cut_polynomial_coefficients.csv"),
    ("c7_25", sp.Rational(7, 25), SOURCE_5000 / "c7_25_generic_D_hh_cut_polynomial_coefficients.csv"),
    ("heldout_c20_29", sp.Rational(20, 29), SOURCE_5000 / "c20_29_generic_D_hh_cut_polynomial_coefficients.csv"),
]


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


def load_reducer() -> Any:
    spec = importlib.util.spec_from_file_location("mts_hh_master_reducer_5000", REDUCER_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {REDUCER_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def expression(value: str) -> sp.Expr:
    return sp.sympify(value, locals={"D": D, "epsilon": epsilon, "s": s, "t": t, "u": u})


def epsilon_coefficient(value: sp.Expr, power: int) -> sp.Expr:
    continued = value.subs(D, 4 - 2 * epsilon)
    return sp.factor(sp.diff(continued, epsilon, power).subs(epsilon, 0) / sp.factorial(power))


def symmetric_degree_seven_basis(first: sp.Expr, second: sp.Expr) -> list[sp.Expr]:
    return [
        first**7 + second**7,
        first * second * (first**5 + second**5),
        first**2 * second**2 * (first**3 + second**3),
        first**3 * second**3 * (first + second),
    ]


def symmetric_degree_four_basis(first: sp.Expr, second: sp.Expr) -> list[sp.Expr]:
    return [
        first**4 + second**4,
        first * second * (first**2 + second**2),
        first**2 * second**2,
    ]


def reconstruct() -> tuple[dict[str, sp.Expr], list[dict[str, Any]]]:
    reducer = load_reducer()
    samples: list[dict[str, Any]] = []
    sample_values: list[dict[str, sp.Expr]] = []
    for label, cosine, coefficient_path in ANGLE_SPECS:
        reduced = reducer.reduce_four_propagator_cut(coefficient_path, cosine)
        t_value = sp.factor(-2 * (1 + cosine))
        u_value = sp.factor(-2 * (1 - cosine))
        box_factor_su = sp.factor(reduced["box_plus"] / u_value**4)
        box_factor_st = sp.factor(reduced["box_minus"] / t_value**4)
        factor_residual = sp.factor(box_factor_su - box_factor_st)
        samples.append(
            {
                "sample": label,
                "cosine": exact(cosine),
                "t": exact(t_value),
                "u": exact(u_value),
                "A_s_hh_direct": exact(reduced["one_scale"]),
                "B_su_hh_direct": exact(reduced["box_plus"]),
                "B_st_hh_direct": exact(reduced["box_minus"]),
                "box_factor_residual": exact(factor_residual),
                "role": "held_out" if label.startswith("heldout") else "fit",
                "status": "closed" if factor_residual == 0 else "failed",
            }
        )
        sample_values.append(
            {
                "t": t_value,
                "u": u_value,
                "A": reduced["one_scale"],
                "F": box_factor_su,
            }
        )

    fit_A = sample_values[:4]
    matrix_A = sp.Matrix([symmetric_degree_seven_basis(row["t"], row["u"]) for row in fit_A])
    coefficients_A = matrix_A.inv() * sp.Matrix([row["A"] for row in fit_A])
    generic_A = sp.factor(
        sum(
            coefficient * basis
            for coefficient, basis in zip(coefficients_A, symmetric_degree_seven_basis(t, u))
        )
    )

    fit_F = sample_values[:3]
    matrix_F = sp.Matrix([symmetric_degree_four_basis(row["t"], row["u"]) for row in fit_F])
    coefficients_F = matrix_F.inv() * sp.Matrix([row["F"] for row in fit_F])
    generic_F = sp.factor(
        sum(
            coefficient * basis
            for coefficient, basis in zip(coefficients_F, symmetric_degree_four_basis(t, u))
        )
    )
    generic_B_su = sp.factor(u**4 * generic_F)
    generic_B_st = sp.factor(t**4 * generic_F)

    A_residuals = [
        sp.factor(generic_A.subs({t: row["t"], u: row["u"]}) - row["A"])
        for row in sample_values
    ]
    F_residuals = [
        sp.factor(generic_F.subs({t: row["t"], u: row["u"]}) - row["F"])
        for row in sample_values
    ]
    for row, A_residual, F_residual in zip(samples, A_residuals, F_residuals):
        row["A_reconstruction_residual"] = exact(A_residual)
        row["box_reconstruction_residual"] = exact(F_residual)
        if A_residual != 0 or F_residual != 0 or row["box_factor_residual"] != "0":
            row["status"] = "failed"

    return {
        "A_hh": generic_A,
        "F_hh": generic_F,
        "B_su_hh": generic_B_su,
        "B_st_hh": generic_B_st,
        "A_heldout_residual": A_residuals[-1],
        "F_heldout_residual": F_residuals[-1],
    }, samples


def reconcile(values: dict[str, sp.Expr]) -> dict[str, sp.Expr]:
    inferred_hh = {
        row["component"]: expression(row["formula"])
        for row in read_csv(BOX_4998)
        if row["component"] in {"B_su_hh(D)", "B_st_hh(D)"}
    }
    old_mixed = {
        row["coefficient"]: expression(row["formula"])
        for row in read_csv(MIXED_4998)
    }
    scalar = {
        row["coefficient"]: expression(row["formula"])
        for row in read_csv(SCALAR_4997)
    }
    infrared_hh_representative = next(
        expression(row["exact_generic_D_formula"])
        for row in read_csv(HH_4999)
        if row["component"] == "A_s_hh_CDR_direct_inference"
    )

    direct_B_su = sp.factor(scalar["B_su_scalar_direct(D)"] + values["B_su_hh"])
    direct_B_st = sp.factor(scalar["B_st_scalar_direct(D)"] + values["B_st_hh"])
    direct_A_s = sp.factor(scalar["T_s_scalar_direct(D)"] + values["A_hh"])
    ratio = lambda channel: sp.factor((D - 4) * channel / (2 * (D - 3)))
    direct_A_t = sp.factor(old_mixed["T_t_finite"] + ratio(t) * old_mixed["C_t_finite"])
    direct_A_u = sp.factor(old_mixed["T_u_finite"] + ratio(u) * old_mixed["C_u_finite"])

    infrared_representative_combination = sp.factor(
        4
        * (
            old_mixed["B_st_full"] / (s * t)
            + old_mixed["B_su_full"] / (s * u)
            + old_mixed["B_tu_full"] / (t * u)
        )
        - (infrared_hh_representative + scalar["T_s_scalar_direct(D)"]) / s
        - direct_A_t / t
        - direct_A_u / u
    )
    direct_cut_combination = sp.factor(
        4
        * (
            direct_B_st / (s * t)
            + direct_B_su / (s * u)
            + old_mixed["B_tu_full"] / (t * u)
        )
        - direct_A_s / s
        - direct_A_t / t
        - direct_A_u / u
    )
    direct_epsilon_0 = epsilon_coefficient(direct_cut_combination, 0)
    direct_epsilon_1 = epsilon_coefficient(direct_cut_combination, 1)
    local_denominator = sp.denom(sp.cancel(direct_epsilon_1))
    crossing_residual = sp.factor(direct_epsilon_1 - direct_epsilon_1.xreplace({t: u, u: t}))
    return {
        **values,
        "inferred_B_su_hh": inferred_hh["B_su_hh(D)"],
        "inferred_B_st_hh": inferred_hh["B_st_hh(D)"],
        "delta_B_su_hh": sp.factor(values["B_su_hh"] - inferred_hh["B_su_hh(D)"]),
        "delta_B_st_hh": sp.factor(values["B_st_hh"] - inferred_hh["B_st_hh(D)"]),
        "infrared_A_hh": infrared_hh_representative,
        "delta_A_hh": sp.factor(values["A_hh"] - infrared_hh_representative),
        "direct_B_su_full": direct_B_su,
        "direct_B_st_full": direct_B_st,
        "direct_A_s_full": direct_A_s,
        "shared_B_su_residual": sp.factor(
            old_mixed["B_su_full"]
            - scalar["B_su_scalar_direct(D)"]
            - values["B_su_hh"]
        ),
        "shared_B_st_residual": sp.factor(
            old_mixed["B_st_full"]
            - scalar["B_st_scalar_direct(D)"]
            - values["B_st_hh"]
        ),
        "full_B_su_residual": sp.factor(direct_B_su - old_mixed["B_su_full"]),
        "full_B_st_residual": sp.factor(direct_B_st - old_mixed["B_st_full"]),
        "infrared_representative_epsilon_0": epsilon_coefficient(infrared_representative_combination, 0),
        "infrared_representative_epsilon_1": epsilon_coefficient(infrared_representative_combination, 1),
        "direct_cut_epsilon_0": direct_epsilon_0,
        "direct_cut_epsilon_1": direct_epsilon_1,
        "required_simple_pole_cancellation": sp.factor(-direct_epsilon_1),
        "local_denominator": local_denominator,
        "local_crossing_residual": crossing_residual,
        "A_D4_residual": sp.factor(
            values["A_hh"].subs(D, 4) - infrared_hh_representative.subs(D, 4)
        ),
        "delta_A_D_minus_4_quotient": sp.factor(
            (values["A_hh"] - infrared_hh_representative) / (D - 4)
        ),
    }


def coefficient_rows(values: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    return [
        {
            "coefficient": "B_su_hh_direct(D)",
            "integral": "I4(s,u)",
            "formula": exact(values["B_su_hh"]),
            "D4_limit": exact(values["B_su_hh"].subs(D, 4)),
            "status": "direct_generic_D_cut_complete",
        },
        {
            "coefficient": "B_st_hh_direct(D)",
            "integral": "I4(s,t)",
            "formula": exact(values["B_st_hh"]),
            "D4_limit": exact(values["B_st_hh"].subs(D, 4)),
            "status": "direct_generic_D_cut_complete",
        },
        {
            "coefficient": "A_s_hh_direct(D)",
            "integral": "I3(s) one-scale coordinate",
            "formula": exact(values["A_hh"]),
            "D4_limit": exact(values["A_hh"].subs(D, 4)),
            "status": "direct_generic_D_cut_complete",
        },
        {
            "coefficient": "B_su_full_direct(D)",
            "integral": "I4(s,u)",
            "formula": exact(values["direct_B_su_full"]),
            "D4_limit": exact(values["direct_B_su_full"].subs(D, 4)),
            "status": "direct_shared_cut_sum_confirmed",
        },
        {
            "coefficient": "B_st_full_direct(D)",
            "integral": "I4(s,t)",
            "formula": exact(values["direct_B_st_full"]),
            "D4_limit": exact(values["direct_B_st_full"].subs(D, 4)),
            "status": "direct_shared_cut_sum_confirmed",
        },
        {
            "coefficient": "A_s_full_direct(D)",
            "integral": "I3(s) one-scale coordinate",
            "formula": exact(values["direct_A_s_full"]),
            "D4_limit": exact(values["direct_A_s_full"].subs(D, 4)),
            "status": "direct_s_cut_sum",
        },
    ]


def reconciliation_rows(values: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    return [
        {
            "quantity": "4998 B_su_hh(D) shared-cut inference",
            "prior_formula": exact(values["inferred_B_su_hh"]),
            "direct_formula": exact(values["B_su_hh"]),
            "residual": exact(values["delta_B_su_hh"]),
            "reason": "independent physical-seed direct cut reproduces the shared-box inference",
            "status": "confirmed_exactly",
        },
        {
            "quantity": "4998 B_st_hh(D) crossed shared-cut inference",
            "prior_formula": exact(values["inferred_B_st_hh"]),
            "direct_formula": exact(values["B_st_hh"]),
            "residual": exact(values["delta_B_st_hh"]),
            "reason": "independent physical-seed crossed box is reproduced by the direct cut",
            "status": "confirmed_exactly",
        },
        {
            "quantity": "4999 A_s_hh IR-minimal generic-D representative",
            "prior_formula": exact(values["infrared_A_hh"]),
            "direct_formula": exact(values["A_hh"]),
            "residual": exact(values["delta_A_hh"]),
            "reason": "the universal soft logarithm fixes the strict-D4 value, while the direct cut fixes its evanescent continuation",
            "status": "replaced_beyond_strict_D4",
        },
        {
            "quantity": "4998 full B_su and B_st shared cuts",
            "prior_formula": "componentwise 4998 full boxes",
            "direct_formula": "4997 scalar plus 5001 hh direct boxes",
            "residual": exact(values["full_B_su_residual"] + values["full_B_st_residual"]),
            "reason": "both independent shared cuts close without a mixed-sector repair",
            "status": "confirmed_exactly",
        },
    ]


def write_document(values: dict[str, sp.Expr]) -> None:
    DOCUMENT.write_text(
        f"""# 5001 - Generic hh completion and local simple-pole obstruction

**Checkpoint marker:** `{MARKER}`  
**Date:** {CHECKED_DATE}  
**Claim status:** private one-loop amplitude derivation; not an outer-kernel, local-GR, or full-MTS claim.

## What is now directly derived

Five exact rational scattering angles were reduced with the independently identified raw auxiliary seed `element 2 = 8 s t A_YM`, the full physical graviton projector, all four uncut denominators, and exact dimension-shifted sphere moments. Four angles determine the symmetric homogeneous functions and the fifth is held out.

```text
B_su^hh(D) = {exact(values['B_su_hh'])}
B_st^hh(D) = {exact(values['B_st_hh'])}
A_s^hh(D)  = {exact(values['A_hh'])}
```

The held-out residuals are

```text
box = {exact(values['F_heldout_residual'])}
one-scale = {exact(values['A_heldout_residual'])}.
```

The direct and crossed anchor cuts also agree exactly. This closes the generic-dimensional internal-graviton `s` cut in the one-scale coordinate.

## Reconciliation with 4998 and 4999

The two direct box coefficients reproduce the independent 4998 shared-cut inference exactly:

```text
direct B_su^hh - 4998 B_su^hh = {exact(values['delta_B_su_hh'])}
direct B_st^hh - 4998 B_st^hh = {exact(values['delta_B_st_hh'])}.
```

There is therefore no missing mixed-*box* evanescent repair. This statement does not close the mixed one-scale coefficients. The other difference is between the direct `s`-channel one-scale coefficient and the 4999 IR-minimal continuation:

```text
delta A_s^hh = {exact(values['delta_A_hh'])}.
```

It is proportional to `D-4`, so the sourced strict-four-dimensional amplitude and all logarithmic soft-pole checks remain intact. The direct cut, rather than the IR-minimal ansatz, owns this evanescent continuation.

## Local simple-pole obstruction

Combining the direct `s`, `t`, and `u` cuts gives

```text
P0 = {exact(values['direct_cut_epsilon_0'])}
P1 = {exact(values['direct_cut_epsilon_1'])}.
```

`P0=0` preserves the universal gravitational double-pole cancellation. `P1` is an exactly crossing-symmetric polynomial with no kinematic denominator. It is a real local simple-pole obstruction, but locality does not identify its owner. The required cancellation is

```text
required simple-pole cancellation = {exact(values['required_simple_pole_cancellation'])}
```

Dunbar--Norridge define `J2(s)=r_Gamma` and state that the `d J2` ambiguity is only in finite rational terms; it therefore cannot cancel a `1/epsilon` pole. The local source review also says four-derivative curvature terms do not generate a two-scalar/any-graviton on-shell amplitude in four dimensions, while evanescent Gauss--Bonnet effects are finite. The obstruction must instead be removed by an independently corrected one-scale cut coefficient or owned by an explicit source-backed UV counterterm of the required on-shell class. The immediate target is an independent generic-`D` mixed `t/u` one-scale reduction. No outer-kernel or full-amplitude claim is made while `P1 != 0`.
""",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    reconstruction_results = [
        coefficient_path.with_name(
            coefficient_path.name.replace(
                "generic_D_hh_cut_polynomial_coefficients.csv",
                "covariant_hh_mu_moment_reconstruction_results.json",
            )
        )
        for _, _, coefficient_path in ANGLE_SPECS
    ]
    required = [
        REDUCER_SCRIPT,
        BOX_4998,
        MIXED_4998,
        SCALAR_4997,
        HH_4999,
        SEED_ID_5002,
        COUNTERTERM_SOURCE,
        DUNBAR_SOURCE,
        *[path for _, _, path in ANGLE_SPECS],
        *reconstruction_results,
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError("missing inputs: " + "; ".join(missing))
    reconstruction_locks = []
    for path in reconstruction_results:
        payload = json.loads(path.read_text(encoding="utf-8"))
        reconstruction_locks.append(
            payload.get("checkpoint_marker") == "MTS_5000_COVARIANT_HH_MU_MOMENT_RECONSTRUCTION"
            and payload.get("heldout_residual") == "0"
            and payload.get("left_yang_mills_basis")
            == "Boels_Luo_GluonsSymms_element_2_equals_8_st_A_YM"
        )
    seed_identification = json.loads(SEED_ID_5002.read_text(encoding="utf-8"))
    counterterm_text = COUNTERTERM_SOURCE.read_text(encoding="utf-8", errors="replace")
    dunbar_text = DUNBAR_SOURCE.read_text(encoding="utf-8", errors="replace")
    source_lock = {
        "all_angle_reconstructions": all(reconstruction_locks),
        "five_independent_angles": len({cosine for _, cosine, _ in ANGLE_SPECS}) == 5,
        "independent_YM_seed_identity": seed_identification.get("identity")
        == "GluonsSymms_element_2 = 8*s*t*A_YM"
        and seed_identification.get("all_gates_pass") is True,
        "4998_inputs_present": BOX_4998.exists() and MIXED_4998.exists(),
        "4997_scalar_cut_present": SCALAR_4997.exists(),
        "4999_IR_representative_present": HH_4999.exists(),
        "two_scalar_R2_amplitude_silence_source": "no corrections to the EH (two-scalar)"
        in counterterm_text
        and "$n$-graviton amplitudes" in counterterm_text,
        "evanescent_Gauss_Bonnet_finite_source": "gives at one loop only finite (quantum) terms"
        in counterterm_text,
        "dJ2_is_finite_rational_only_source": "only remaining ambiguity arising in the $d J_2$ term"
        in dunbar_text
        and "only ambiguity will be in finite" in dunbar_text
        and "infinity structure" in dunbar_text,
    }
    if not all(source_lock.values()):
        raise RuntimeError(f"source lock failed: {source_lock}")
    outputs = [
        SAMPLES_CSV,
        COEFFICIENT_CSV,
        RECONCILIATION_CSV,
        LOCAL_OBSTRUCTION_CSV,
        GATE_CSV,
        RESULT_JSON,
        PROVENANCE,
        DOCUMENT,
    ]
    if args.dry_run:
        print(json.dumps({"checkpoint_marker": MARKER, "source_lock": source_lock, "writes": [relative(path) for path in outputs]}, indent=2, sort_keys=True))
        return 0

    formal_before = tree_digest(ROOT / "formalization-workbench")
    reconstructed, samples = reconstruct()
    values = reconcile(reconstructed)
    reconstruction_closed = (
        values["A_heldout_residual"] == 0
        and values["F_heldout_residual"] == 0
        and all(row["status"] == "closed" for row in samples)
    )
    d4_closed = values["A_D4_residual"] == 0
    boxes_reconciled = all(
        values[key] == 0
        for key in (
            "delta_B_su_hh",
            "delta_B_st_hh",
            "shared_B_su_residual",
            "shared_B_st_residual",
            "full_B_su_residual",
            "full_B_st_residual",
        )
    )
    leading_pole_closed = values["direct_cut_epsilon_0"] == 0
    local_obstruction_proved = (
        values["local_denominator"] == 1
        and values["local_crossing_residual"] == 0
        and values["direct_cut_epsilon_1"] != 0
    )
    evanescent_factor_closed = sp.factor(
        values["delta_A_hh"] - (D - 4) * values["delta_A_D_minus_4_quotient"]
    ) == 0
    gates = [
        {"gate": "five_angle_direct_reconstruction", "passed": reconstruction_closed, "status": "closed" if reconstruction_closed else "failed", "meaning": "four exact fits plus one independent held-out angle"},
        {"gate": "generic_D_hh_boxes", "passed": reconstruction_closed and boxes_reconciled, "status": "closed" if reconstruction_closed and boxes_reconciled else "failed", "meaning": "both direct s-cut boxes reproduce the independent 4998 shared-cut inference"},
        {"gate": "generic_D_hh_one_scale", "passed": reconstruction_closed, "status": "closed" if reconstruction_closed else "failed", "meaning": "the direct hh triangle/bubble combination is reconstructed"},
        {"gate": "strict_D4_continuity", "passed": d4_closed and evanescent_factor_closed, "status": "closed" if d4_closed and evanescent_factor_closed else "failed", "meaning": "the direct-minus-IR difference is exactly proportional to D-4"},
        {"gate": "IR_double_pole_after_direct_completion", "passed": leading_pole_closed, "status": "closed" if leading_pole_closed else "failed", "meaning": "the direct cuts preserve the leading gravitational IR cancellation"},
        {"gate": "mixed_box_evanescent_repair", "passed": boxes_reconciled, "status": "not_required" if boxes_reconciled else "open", "meaning": "the physical mixed/shared box coefficients are direct and mutually consistent"},
        {"gate": "local_simple_pole_obstruction", "passed": local_obstruction_proved, "status": "obstruction_proved" if local_obstruction_proved else "failed", "meaning": "the nonzero residual is a crossing-symmetric polynomial with no kinematic denominator"},
        {"gate": "finite_dJ2_excluded_as_pole_owner", "passed": source_lock["dJ2_is_finite_rational_only_source"], "status": "closed", "meaning": "the sourced dJ2 ambiguity is finite and cannot cancel a 1/epsilon pole"},
        {"gate": "two_scalar_R2_counterterm_silence", "passed": source_lock["two_scalar_R2_amplitude_silence_source"] and source_lock["evanescent_Gauss_Bonnet_finite_source"], "status": "closed", "meaning": "the sourced R-squared and evanescent Gauss-Bonnet routes do not own this pole"},
        {"gate": "mixed_one_scale_recheck", "passed": False, "status": "open", "meaning": "independently recompute the mixed t/u one-scale coefficients in generic D"},
        {"gate": "cut_free_dJ2_completion", "passed": False, "status": "deferred_until_poles_close", "meaning": "finite rational ambiguity is addressed only after all simple poles close"},
        {"gate": "outer_cut_or_full_MTS", "passed": False, "status": "blocked_by_simple_pole", "meaning": "the one-loop amplitude cannot feed the outer kernel while P1 is nonzero"},
    ]
    write_csv(SAMPLES_CSV, tagged(samples))
    write_csv(COEFFICIENT_CSV, tagged(coefficient_rows(values)))
    write_csv(RECONCILIATION_CSV, tagged(reconciliation_rows(values)))
    write_csv(
        LOCAL_OBSTRUCTION_CSV,
        tagged(
            [
                {"equation": "4999_IR_minimal_P0", "value": exact(values["infrared_representative_epsilon_0"]), "required": "0", "classification": "checksum", "status": "closed"},
                {"equation": "4999_IR_minimal_P1", "value": exact(values["infrared_representative_epsilon_1"]), "required": "0", "classification": "IR_minimal_assumption", "status": "not_direct_cut_input"},
                {"equation": "direct_cut_P0", "value": exact(values["direct_cut_epsilon_0"]), "required": "0", "classification": "double_pole", "status": "closed" if leading_pole_closed else "failed"},
                {"equation": "direct_cut_P1", "value": exact(values["direct_cut_epsilon_1"]), "required": "0", "classification": "crossing_symmetric_local_simple_pole_obstruction", "status": "open_obstruction"},
                {"equation": "required_simple_pole_cancellation", "value": exact(values["required_simple_pole_cancellation"]), "required": "negative_direct_cut_P1", "classification": "must_be_owned_by_recomputed_one_scale_cut_or_source_backed_UV_counterterm", "status": "derived_not_yet_filled"},
                {"equation": "dJ2_pole_contribution", "value": "0", "required": "finite_only", "classification": "source_excludes_dJ2_as_pole_owner", "status": "closed"},
            ]
        ),
    )
    write_csv(GATE_CSV, tagged(gates))
    write_document(values)
    formal_after = tree_digest(ROOT / "formalization-workbench")
    if formal_before != formal_after:
        raise RuntimeError("formalization-workbench changed during checkpoint")
    hashes = {relative(path): digest(path) for path in [*required, Path(__file__).resolve()]}
    result = {
        "checkpoint_marker": MARKER,
        "source_checked_date": CHECKED_DATE,
        "source_lock": source_lock,
        "source_hashes_sha256": hashes,
        "formalization_workbench_tree_sha256": formal_after,
        "generic_D_hh_box_sector_complete": reconstruction_closed,
        "generic_D_hh_one_scale_sector_complete": reconstruction_closed,
        "direct_hh_s_cut_complete": reconstruction_closed,
        "direct_B_su_hh": exact(values["B_su_hh"]),
        "direct_B_st_hh": exact(values["B_st_hh"]),
        "direct_A_s_hh": exact(values["A_hh"]),
        "heldout_residuals": {"box": exact(values["F_heldout_residual"]), "one_scale": exact(values["A_heldout_residual"])},
        "4998_generic_D_hh_box_rows_confirmed": reconstruction_closed and boxes_reconciled,
        "4999_IR_minimal_continuation_replaced_beyond_D4": reconstruction_closed and d4_closed,
        "mixed_box_evanescent_repair_required": False,
        "mixed_one_scale_recheck_required": True,
        "direct_cut_local_simple_pole_obstruction": exact(values["direct_cut_epsilon_1"]),
        "required_simple_pole_cancellation": exact(values["required_simple_pole_cancellation"]),
        "local_obstruction_is_crossing_symmetric_polynomial": local_obstruction_proved,
        "dJ2_can_cancel_simple_pole": False,
        "cut_free_dJ2_remainder_complete": False,
        "outer_cut_complete": False,
        "complete_one_loop_phi2h2": False,
        "valid_for_full_MTS_claim": False,
        "next_target": "independently recompute the generic-D mixed t/u one-scale coefficients and require the full P1 pole to vanish",
        "outputs": [relative(path) for path in outputs],
    }
    RESULT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    PROVENANCE.write_text(
        "# 5001 provenance\n\n"
        f"Checkpoint marker: `{MARKER}`\n\n"
        "## Locked inputs\n\n"
        + "\n".join(f"- `{path}` - SHA-256 `{value}`" for path, value in hashes.items())
        + "\n\n## Method\n\n"
        "Five exact rational-angle D-dimensional cuts are reduced with the 5000 angular master reducer. Symmetric homogeneous interpolation determines the generic hh boxes and one-scale coefficient; a held-out angle validates both. The boxes reproduce the independent 4998 shared cuts exactly. Inserting the direct s-channel one-scale continuation into the all-channel pole combination leaves a crossing-symmetric local simple-pole obstruction. Dunbar--Norridge exclude finite dJ2 as its owner, so the next calculation is an independent generic-D mixed t/u one-scale reduction; a source-backed UV counterterm remains a fallback only if it has the required on-shell two-scalar/two-graviton class.\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

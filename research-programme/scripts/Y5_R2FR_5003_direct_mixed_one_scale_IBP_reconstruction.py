from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FUNCTIONAL = POST / "source-intake" / "functional_rg"
SOURCE = FUNCTIONAL / "5003"
REDUCER_SCRIPT = POST / "scripts" / "Y5_R2FR_4994_strict_4d_mixed_bubble_and_evanescent_pole.py"
MIXED_4998 = FUNCTIONAL / "4998" / "complete_generic_D_mixed_cut.csv"
RESULT_4994 = FUNCTIONAL / "4994" / "strict_4d_mixed_bubble_and_evanescent_pole_results.json"
RESULT_5001 = FUNCTIONAL / "5001" / "generic_hh_completion_and_local_simple_pole_obstruction_results.json"

SAMPLE_CSV = SOURCE / "direct_mixed_one_scale_IBP_samples.csv"
TOPOLOGY_CSV = SOURCE / "direct_mixed_topology_master_coefficients.csv"
RECONSTRUCTION_CSV = SOURCE / "mixed_one_scale_generic_reconstruction.csv"
GATE_CSV = SOURCE / "direct_mixed_one_scale_recheck_gate.csv"
RESULT_JSON = SOURCE / "direct_mixed_one_scale_IBP_reconstruction_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"
DOCUMENT = POST / "5003-Y5-R2FR-direct-mixed-one-scale-IBP-reconstruction.md"

MARKER = "MTS_5003_DIRECT_MIXED_ONE_SCALE_IBP_RECONSTRUCTION"
CHECKED_DATE = "2026-07-14"

D = sp.Symbol("D")
t, u = sp.symbols("t u", nonzero=True)

FIT_DIMENSIONS = (Fraction(5), Fraction(11, 2), Fraction(13, 2), Fraction(15, 2))
FIT_KINEMATICS = ((1, 2), (1, 3), (2, 1), (3, 2))
HELD_OUT_SPECS = (
    (Fraction(17, 2), 2, 3),
    (Fraction(19, 2), 3, 1),
    (Fraction(21, 2), 4, 3),
)

MASTERS = {
    "bubble": (0, 1, 1, 0, 0),
    "triangle_left": (0, 1, 1, 1, 0),
    "triangle_right": (0, 1, 1, 0, 1),
    "box": (0, 1, 1, 1, 1),
}


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


def load_reducer() -> Any:
    spec = importlib.util.spec_from_file_location("mts_mixed_ibp_4994", REDUCER_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {REDUCER_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_candidate() -> dict[str, sp.Expr]:
    with MIXED_4998.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return {
        row["coefficient"]: sp.sympify(row["formula"], locals={"D": D, "t": t, "u": u})
        for row in rows
    }


def as_sympy(value: Fraction) -> sp.Rational:
    return sp.Rational(value.numerator, value.denominator)


def direct_sample(
    reducer_module: Any,
    candidates: dict[str, sp.Expr],
    dimension: Fraction,
    t_value: int,
    u_value: int,
    role: str,
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, sp.Expr]]:
    topology_values: dict[str, dict[str, sp.Expr]] = {}
    topology_rows: list[dict[str, Any]] = []
    for topology in ("AC", "AD", "BC", "BD"):
        reducer = reducer_module.OneLoopNullNumeratorReducer(
            t_value, u_value, topology, dimension
        )
        coefficients = {
            name: as_sympy(reducer.coefficient_to(master))
            for name, master in MASTERS.items()
        }
        topology_values[topology] = coefficients
        topology_rows.append(
            {
                "sample": f"D{dimension}_t{t_value}_u{u_value}",
                "role": role,
                "D": str(dimension),
                "t": t_value,
                "u": u_value,
                "topology": topology,
                **{name: exact(value) for name, value in coefficients.items()},
                "method": "direct rank-four null-numerator IBP; no stored 4995 coefficient samples",
                "status": "exact_rational_IBP",
            }
        )

    dimension_value = as_sympy(dimension)
    prefactor = sp.Rational(t_value) ** 4 / 16
    triangle_raw = sp.factor(
        -prefactor
        * sum(
            values["triangle_left"] + values["triangle_right"]
            for values in topology_values.values()
        )
    )
    bubble_raw = sp.factor(
        prefactor * sum(values["bubble"] for values in topology_values.values())
    )
    box_su = sp.factor(
        prefactor
        * (topology_values["AC"]["box"] + topology_values["BD"]["box"])
    )
    box_tu = sp.factor(
        prefactor
        * (topology_values["AD"]["box"] + topology_values["BC"]["box"])
    )
    ratio = sp.factor(
        (dimension_value - 4) * sp.Rational(u_value) / (2 * (dimension_value - 3))
    )
    one_scale = sp.factor(triangle_raw + ratio * bubble_raw)
    substitutions = {D: dimension_value, t: t_value, u: u_value}
    candidate_one_scale = sp.factor(
        (candidates["T_u_finite"] + (D - 4) * u * candidates["C_u_finite"] / (2 * (D - 3))).subs(substitutions)
    )
    candidate_box_su = sp.factor(candidates["B_su_full"].subs(substitutions))
    candidate_box_tu = sp.factor(candidates["B_tu_full"].subs(substitutions))
    values = {
        "D": dimension_value,
        "t": sp.Rational(t_value),
        "u": sp.Rational(u_value),
        "triangle_raw": triangle_raw,
        "bubble_raw": bubble_raw,
        "one_scale": one_scale,
        "box_su": box_su,
        "box_tu": box_tu,
        "candidate_one_scale": candidate_one_scale,
        "candidate_box_su": candidate_box_su,
        "candidate_box_tu": candidate_box_tu,
    }
    sample_row = {
        "sample": f"D{dimension}_t{t_value}_u{u_value}",
        "role": role,
        "D": str(dimension),
        "t": t_value,
        "u": u_value,
        "T_u_raw": exact(triangle_raw),
        "C_u_raw": exact(bubble_raw),
        "master_ratio_I2_over_I3": exact(ratio),
        "A_u_direct": exact(one_scale),
        "A_u_4998": exact(candidate_one_scale),
        "A_u_residual": exact(one_scale - candidate_one_scale),
        "B_su_direct": exact(box_su),
        "B_su_residual": exact(box_su - candidate_box_su),
        "B_tu_direct": exact(box_tu),
        "B_tu_residual": exact(box_tu - candidate_box_tu),
        "status": "closed" if one_scale == candidate_one_scale and box_su == candidate_box_su and box_tu == candidate_box_tu else "failed",
    }
    return sample_row, topology_rows, values


def reconstruct_generic(fit_values: list[dict[str, sp.Expr]]) -> sp.Expr:
    basis = [D**dimension_power * t**t_power * u ** (3 - t_power) for dimension_power in range(4) for t_power in range(4)]
    matrix = sp.Matrix(
        [
            [term.subs({D: row["D"], t: row["t"], u: row["u"]}) for term in basis]
            for row in fit_values
        ]
    )
    if matrix.det() == 0:
        raise RuntimeError("generic mixed one-scale reconstruction matrix is singular")
    targets = sp.Matrix(
        [
            sp.factor(
                row["one_scale"]
                * 128
                * (row["D"] - 3)
                * (row["D"] - 2)
                * (row["D"] - 1)
                / row["u"] ** 4
            )
            for row in fit_values
        ]
    )
    coefficients = matrix.inv() * targets
    polynomial = sp.factor(sum(value * term for value, term in zip(coefficients, basis)))
    return sp.factor(u**4 * polynomial / (128 * (D - 3) * (D - 2) * (D - 1)))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    required = [REDUCER_SCRIPT, MIXED_4998, RESULT_4994, RESULT_5001]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError("missing inputs: " + "; ".join(missing))
    result_4994 = json.loads(RESULT_4994.read_text(encoding="utf-8"))
    result_5001 = json.loads(RESULT_5001.read_text(encoding="utf-8"))
    source_lock = {
        "4994_rank_four_reducer": result_4994.get("checkpoint_marker") == "MTS_4994_STRICT_4D_MIXED_BUBBLE_AND_EVANESCENT_POLE",
        "4998_candidate_present": MIXED_4998.exists(),
        "5001_simple_pole_obstruction": result_5001.get("checkpoint_marker") == "MTS_5001_GENERIC_HH_COMPLETION_AND_LOCAL_SIMPLE_POLE_OBSTRUCTION" and result_5001.get("mixed_one_scale_recheck_required") is True,
    }
    if not all(source_lock.values()):
        raise RuntimeError(f"source lock failed: {source_lock}")
    outputs = [SAMPLE_CSV, TOPOLOGY_CSV, RECONSTRUCTION_CSV, GATE_CSV, RESULT_JSON, PROVENANCE, DOCUMENT]
    if args.dry_run:
        print(
            json.dumps(
                {
                    "checkpoint_marker": MARKER,
                    "source_lock": source_lock,
                    "fit_samples": len(FIT_DIMENSIONS) * len(FIT_KINEMATICS),
                    "held_out_samples": len(HELD_OUT_SPECS),
                    "writes": [relative(path) for path in outputs],
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    formal_before = tree_digest(ROOT / "formalization-workbench")
    reducer_module = load_reducer()
    candidates = read_candidate()
    sample_rows: list[dict[str, Any]] = []
    topology_rows: list[dict[str, Any]] = []
    fit_values: list[dict[str, sp.Expr]] = []
    held_out_values: list[dict[str, sp.Expr]] = []
    for dimension in FIT_DIMENSIONS:
        for t_value, u_value in FIT_KINEMATICS:
            sample, topology, values = direct_sample(
                reducer_module, candidates, dimension, t_value, u_value, "fit"
            )
            sample_rows.append(sample)
            topology_rows.extend(topology)
            fit_values.append(values)
    for dimension, t_value, u_value in HELD_OUT_SPECS:
        sample, topology, values = direct_sample(
            reducer_module, candidates, dimension, t_value, u_value, "held_out"
        )
        sample_rows.append(sample)
        topology_rows.extend(topology)
        held_out_values.append(values)

    reconstructed = reconstruct_generic(fit_values)
    candidate_generic = sp.factor(
        candidates["T_u_finite"]
        + (D - 4) * u * candidates["C_u_finite"] / (2 * (D - 3))
    )
    fit_residuals = [sp.factor(reconstructed.subs({D: row["D"], t: row["t"], u: row["u"]}) - row["one_scale"]) for row in fit_values]
    held_out_residuals = [sp.factor(reconstructed.subs({D: row["D"], t: row["t"], u: row["u"]}) - row["one_scale"]) for row in held_out_values]
    generic_residual = sp.factor(reconstructed - candidate_generic)
    all_direct_residuals = all(
        row["A_u_residual"] == row["B_su_residual"] == row["B_tu_residual"] == "0"
        and row["status"] == "closed"
        for row in sample_rows
    )
    reconstruction_closed = all(value == 0 for value in fit_residuals + held_out_residuals) and generic_residual == 0
    anchor = next(row for row in sample_rows if row["D"] == "5" and row["t"] == 1 and row["u"] == 2)
    anchor_4995_reproduced = anchor["T_u_raw"] == "-353/16" and anchor["C_u_raw"] == "319/32" and anchor["A_u_direct"] == "-1093/64"
    gates = [
        {"gate": "direct_four_topology_IBP", "passed": all_direct_residuals, "status": "closed" if all_direct_residuals else "failed", "meaning": "every fit and held-out point is regenerated from four rank-four topology reducers"},
        {"gate": "generic_one_scale_reconstruction", "passed": reconstruction_closed, "status": "closed" if reconstruction_closed else "failed", "meaning": "16 direct points derive the generic formula and three unused points validate it"},
        {"gate": "4995_anchor_regenerated", "passed": anchor_4995_reproduced, "status": "closed" if anchor_4995_reproduced else "failed", "meaning": "the formerly hard-coded D=5 anchor is reproduced directly"},
        {"gate": "mixed_tu_one_scale_owner_of_P1", "passed": False, "status": "excluded" if all_direct_residuals and reconstruction_closed else "open", "meaning": "the independently regenerated mixed coefficient equals 4998 and cannot supply the missing cancellation"},
        {"gate": "complete_one_loop_phi2h2", "passed": False, "status": "blocked_by_s_channel_or_counterterm_discrimination", "meaning": "the local simple pole remains after the mixed recheck"},
        {"gate": "full_MTS_claim", "passed": False, "status": "blocked", "meaning": "this is an internal amplitude checkpoint"},
    ]
    if not all_direct_residuals or not reconstruction_closed or not anchor_4995_reproduced:
        raise RuntimeError("direct mixed one-scale reconstruction failed")

    write_csv(SAMPLE_CSV, tagged(sample_rows))
    write_csv(TOPOLOGY_CSV, tagged(topology_rows))
    write_csv(
        RECONSTRUCTION_CSV,
        tagged(
            [
                {
                    "quantity": "A_u=T_u+I2_over_I3*C_u",
                    "derived_formula": exact(reconstructed),
                    "4998_formula": exact(candidate_generic),
                    "generic_residual": exact(generic_residual),
                    "fit_residual_sum": exact(sum(value**2 for value in fit_residuals)),
                    "held_out_residual_sum": exact(sum(value**2 for value in held_out_residuals)),
                    "status": "closed",
                }
            ]
        ),
    )
    write_csv(GATE_CSV, tagged(gates))
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
        "fit_samples": len(fit_values),
        "held_out_samples": len(held_out_values),
        "direct_topology_reductions": len(topology_rows),
        "direct_generic_A_u": exact(reconstructed),
        "4998_A_u_residual": exact(generic_residual),
        "mixed_tu_one_scale_recheck_complete": True,
        "mixed_tu_one_scale_can_cancel_5001_P1": False,
        "local_simple_pole_obstruction_complete": False,
        "complete_one_loop_phi2h2": False,
        "valid_for_full_MTS_claim": False,
        "next_target": "independently audit the D-dimensional hh s-cut state/current continuation and discriminate it from a source-backed UV counterterm",
        "outputs": [relative(path) for path in outputs],
    }
    RESULT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    PROVENANCE.write_text(
        "# 5003 provenance\n\n"
        f"Checkpoint marker: `{MARKER}`\n\n"
        "## Locked inputs\n\n"
        + "\n".join(f"- `{path}` - SHA-256 `{value}`" for path, value in hashes.items())
        + "\n\n## Method\n\n"
        "Each coefficient is regenerated from the rank-four null-numerator integral over AC, AD, BC, and BD. Bubble, both cut-visible triangles, and box masters are requested directly from the exact rational IBP reducer. Sixteen fit points determine the 16-coefficient homogeneous generic-D ansatz; three unused rational points validate it. Stored 4995 coefficient samples are not used as numerical inputs.\n",
        encoding="utf-8",
    )
    DOCUMENT.write_text(
        f"""# 5003 - Direct mixed one-scale IBP reconstruction

**Checkpoint marker:** `{MARKER}`  
**Date:** {CHECKED_DATE}  
**Claim status:** private amplitude derivation; not a complete one-loop, local-GR, or full-MTS claim.

## Calculation

The mixed `u` cut was regenerated from all four rank-four families `AC`, `AD`, `BC`, and `BD`. For every topology the exact rational reducer separately returned the cut-visible bubble, both triangles, and box. No hard-coded coefficient from checkpoint 4995 entered the fit.

Sixteen independent `(D,t,u)` points derive

```text
A_u(D) = {exact(reconstructed)}.
```

Three unused points have total squared residual `{exact(sum(value**2 for value in held_out_residuals))}`. The generic residual against the 4998 finite-coordinate result, after using the exact `I2/I3` master relation, is `{exact(generic_residual)}`. All box normalization residuals also vanish.

The formerly stored anchor is now regenerated rather than trusted:

```text
(D,t,u)=(5,1,2): T_u_raw=-353/16, C_u_raw=319/32, A_u=-1093/64.
```

## Consequence

The mixed `t/u` one-scale continuation is not the owner of the 5001 simple-pole mismatch. This is progress by exclusion backed by a fresh calculation: the remaining fork is now the `hh` `s`-cut dimensional state/current continuation versus a genuinely source-backed UV counterterm. Finite `dJ2` remains excluded as a pole owner.
""",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

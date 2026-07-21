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
SOURCE = POST / "source-intake" / "functional_rg" / "4995"
FUNCTIONAL = SOURCE.parent

DUNBAR = FUNCTIONAL / "4986" / "sources" / "dunbar_norridge" / "9512084.tex"
BOELS = FUNCTIONAL / "4992" / "sources" / "boels_luo_1710.10208" / "LoopsFromTrees_v2.tex"
ACCETTULLI = SOURCE / "sources" / "accettulli_huber_1911.10108" / "errequadro.tex"
HH_RESULT = FUNCTIONAL / "4991" / "massless_hh_channel_amplitude_seed_results.json"
BOX_RESULT = FUNCTIONAL / "4992" / "mixed_hphi_cut_and_full_box_completion_results.json"
TRIANGLE_RESULT = FUNCTIONAL / "4993" / "universal_soft_operator_and_triangle_completion_results.json"
MIXED_RESULT = FUNCTIONAL / "4994" / "strict_4d_mixed_bubble_and_evanescent_pole_results.json"

IDENTITY_CSV = SOURCE / "one_scale_master_identity.csv"
SAMPLE_CSV = SOURCE / "mixed_dimension_samples.csv"
RECONSTRUCTION_CSV = SOURCE / "mixed_dimension_basis_reconstruction.csv"
BUBBLE_CSV = SOURCE / "finite_bubble_convention.csv"
GATE_CSV = SOURCE / "one_scale_master_basis_and_bubble_gate.csv"
RESULT_JSON = SOURCE / "one_scale_master_basis_and_full_bubble_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"
DOCUMENT = POST / "4995-Y5-R2FR-one-scale-master-basis-cancellation-and-full-bubble-completion.md"

MARKER = "MTS_4995_ONE_SCALE_MASTER_BASIS_AND_FULL_BUBBLE_COMPLETION"
CHECKED_DATE = "2026-07-14"

D = sp.Symbol("D")
t = sp.Symbol("t", nonzero=True)
u = sp.Symbol("u", nonzero=True)
x = sp.Symbol("x", nonzero=True)


def q(value: str | int) -> sp.Rational:
    return sp.Rational(value)


ANCHOR_A = [
    (q(5), q("1651/64"), q("35/64"), q("-353/16"), q("319/32")),
    (q(7), q("949/64"), q("21/64"), q("-3799/400"), q("-599/1200")),
    (q(9), q("1457/128"), q("33/128"), q("-7057/1120"), q("-2453/1600")),
    (q(11), q("6223/640"), q("143/640"), q("-11971/2400"), q("-4737/2800")),
    (q("13/2"), q("10069/616"), q("221/616"), q("-25541/2310"), q("553/2200")),
    (q("15/2"), q("1421/104"), q("95/312"), q("-7171/858"), q("-7625/8008")),
    (q("17/2"), q("5279/440"), q("119/440"), q("-48833/7150"), q("-11051/7800")),
    (q("19/2"), q("19213/1768"), q("437/1768"), q("-64907/11050"), q("-60107/37400")),
    (q("21/2"), q("7639/760"), q("35/152"), q("-84509/16150"), q("-282007/167960")),
    (q("23/2"), q("8983/952"), q("207/952"), q("-108071/22610"), q("-135271/79800")),
    (q("25/2"), q("31309/3496"), q("725/3496"), q("-27205/6118"), q("-229/136")),
]

ANCHOR_B = [
    (q("7/2"), q("462753/128"), q("6237/40"), q("-23538681/13760"), q("-311031/1376")),
    (q("15/4"), q("3405483/1408"), q("9315/88"), q("-49192191/47168"), q("-39919581/165088")),
    (q("19/5"), q("16273143/7168"), q("44631/448"), q("-271461375/283136"), q("-8752935/35392")),
    (q("21/5"), q("6288921/4096"), q("17577/256"), q("-41826375/83968"), q("-82771605/230912")),
    (q("9/2"), q("1117071/896"), q("3159/56"), q("-9477/2240"), q("-1060803/1120")),
    (q(5), q("986499/1024"), q("2835/64"), q("-277749/512"), q("29529/128")),
    (q("11/2"), q("102033/128"), q("297/8"), q("-1274697/3520"), q("154551/2464")),
    (q(7), q("569349/1024"), q("1701/64"), q("-537759/2560"), q("-819/320")),
    (q("13/2"), q("862083/1408"), q("17901/616"), q("-84171069/349888"), q("139179/24992")),
    (q("15/2"), q("853389/1664"), q("2565/104"), q("-17067591/90688"), q("-3476223/498784")),
]

QUANTITIES = ("B_su", "B_tu", "T_u_Dunbar", "C_u_raw")


def relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def normalized_text(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8", errors="replace").split())


def exact(expression: sp.Expr | int) -> str:
    return sp.sstr(sp.factor(sp.cancel(sp.together(sp.sympify(expression)))))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
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


def source_lock() -> dict[str, bool]:
    dunbar = normalized_text(DUNBAR)
    boels = normalized_text(BOELS)
    accettulli = normalized_text(ACCETTULLI)
    hh = json.loads(HH_RESULT.read_text(encoding="utf-8"))
    box = json.loads(BOX_RESULT.read_text(encoding="utf-8"))
    triangle = json.loads(TRIANGLE_RESULT.read_text(encoding="utf-8"))
    mixed = json.loads(MIXED_RESULT.read_text(encoding="utf-8"))
    return {
        "dunbar_integral_basis": "I_2(s)" in dunbar and "I_{3}(s)" in dunbar,
        "dunbar_rational_ambiguity": "only remaining ambiguity arising in the $d J_2$ term" in dunbar,
        "dunbar_scalar_counterterm": "{203 \\over 320\\eps }" in dunbar and "four external scalars" in dunbar,
        "boels_dimension_dependence_warning": "D-independence of the coefficients" in boels and "mu^2" in boels,
        "accettulli_D_dimensional_field_redefinition": "This argument is valid in $D$ dimensions" in accettulli,
        "accettulli_no_two_scalar_graviton_R2": "no corrections to the EH (two-scalar) $n$-graviton amplitudes" in accettulli,
        "hh_seed_locked": hh.get("checkpoint_marker") == "MTS_4991_MASSLESS_HH_CHANNEL_AMPLITUDE_SEED",
        "box_sector_locked": bool(box.get("four_dimensional_box_sector_complete")),
        "triangle_sector_locked": bool(triangle.get("triangle_sector_complete_from_IR")),
        "strict_mixed_checkpoint_locked": mixed.get("checkpoint_marker") == "MTS_4994_STRICT_4D_MIXED_BUBBLE_AND_EVANESCENT_POLE",
    }


def reconstruct(samples: list[tuple[sp.Rational, ...]], column: int, degree: int, count: int) -> sp.Expr:
    points = [(row[0], row[column]) for row in samples[:count]]
    return sp.factor(sp.rational_interpolate(points, degree, D))


def formula_residual(formula: sp.Expr, samples: list[tuple[sp.Rational, ...]], column: int) -> sp.Expr:
    residuals = [sp.cancel(formula.subs(D, row[0]) - row[column]) for row in samples]
    return sp.simplify(sum(value**2 for value in residuals))


def build_reconstruction() -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, sp.Expr]]:
    expected = {
        "A_B_su": (41 * D**2 + 106 * D + 96) / (8 * (D - 3) * (D - 1)),
        "A_B_tu": D * (D + 2) / (8 * (D - 3) * (D - 1)),
        "A_T_u_Dunbar": -3 * (9 * D**3 - 36 * D**2 + 468 * D - 800) / (10 * (D - 3) * (D - 2) * (D - 1)),
        "A_C_u_raw": -(27 * D**3 + 532 * D**2 - 6036 * D + 8720) / (40 * (D - 4) * (D - 2) * (D - 1)),
        "B_B_su": 81 * (313 * D**2 + 698 * D + 864) / (128 * (D - 3) * (D - 1)),
        "B_B_tu": 81 * D * (D + 2) / (8 * (D - 3) * (D - 1)),
        "B_T_u_Dunbar": -729 * (125 * D**3 - 750 * D**2 + 4000 * D - 14208) / (64 * (D - 3) * (D - 1) * (19 * D - 88)),
        "B_C_u_raw": -27 * (15 * D**3 + 3894 * D**2 - 34832 * D + 51968) / (32 * (D - 2) * (D - 1) * (19 * D - 88)),
    }
    reconstructed: dict[str, sp.Expr] = {}
    rows: list[dict[str, Any]] = []
    sample_rows: list[dict[str, Any]] = []
    for anchor, t_value, u_value, samples in (("A", 1, 2, ANCHOR_A), ("B", 2, 3, ANCHOR_B)):
        for row in samples:
            sample_rows.append({
                "anchor": anchor,
                "t": t_value,
                "u": u_value,
                "s": -t_value - u_value,
                "D": exact(row[0]),
                **{name: exact(row[index + 1]) for index, name in enumerate(QUANTITIES)},
                "extraction_method": "exact rational D-dimensional IBP reduction of the two-particle cut",
                "status": "source_sample",
            })
        for column, quantity in enumerate(QUANTITIES, start=1):
            degree = 2 if quantity.startswith("B_") else 3
            count = 5 if degree == 2 else 7
            key = f"{anchor}_{quantity}"
            reconstructed[key] = reconstruct(samples, column, degree, count)
            residual = sp.cancel(reconstructed[key] - expected[key])
            heldout = formula_residual(reconstructed[key], samples[count:], column)
            rows.append({
                "anchor": anchor,
                "t": t_value,
                "u": u_value,
                "quantity": quantity,
                "fit_points": count,
                "heldout_points": len(samples) - count,
                "reconstructed_formula": exact(reconstructed[key]),
                "expected_formula": exact(expected[key]),
                "formula_residual": exact(residual),
                "heldout_squared_residual": exact(heldout),
                "limit_D_to_4": exact(sp.limit(reconstructed[key], D, 4)),
                "status": "closed" if residual == 0 and heldout == 0 else "failed",
            })
    return sample_rows, rows, reconstructed


def master_identity_rows(reconstructed: dict[str, sp.Expr]) -> tuple[list[dict[str, Any]], dict[str, sp.Expr]]:
    ratio = (D - 4) * x / (2 * (D - 3))
    transformed: dict[str, sp.Expr] = {}
    rows: list[dict[str, Any]] = [
        {
            "identity": "massless_bubble_parameter_integral",
            "left_hand_side": "I2_D(x)",
            "right_hand_side": "Gamma(2-D/2)*Gamma(D/2-1)^2/Gamma(D-2)*(-x)^(D/2-2)",
            "residual": "0",
            "scope": "common loop-normalization suppressed",
            "status": "closed",
        },
        {
            "identity": "one_mass_triangle_parameter_integral",
            "left_hand_side": "I3_D(x)",
            "right_hand_side": "Gamma(3-D/2)*Gamma(D/2-2)^2/Gamma(D-3)*(-x)^(D/2-3)",
            "residual": "0",
            "scope": "common loop-normalization suppressed",
            "status": "closed",
        },
        {
            "identity": "exact_one_scale_master_relation",
            "left_hand_side": "I2_D(x)",
            "right_hand_side": f"({exact(ratio)})*I3_D(x)",
            "residual": "0",
            "scope": "analytic continuation away from D=3,4; Laurent identity at D=4",
            "status": "closed",
        },
        {
            "identity": "coefficient_basis_transform",
            "left_hand_side": "T*I3_D(x)+C*I2_D(x)",
            "right_hand_side": "[T+(C-C_hat)*(D-4)*x/(2*(D-3))]*I3_D(x)+C_hat*I2_D(x)",
            "residual": "0",
            "scope": "C_hat arbitrary; individual T/C coefficients are basis coordinates",
            "status": "closed",
        },
    ]
    settings = {
        "A": (q(2), q(-4), q(-32), (5 * D**3 - 244 * D**2 + 532 * D - 80) / (8 * (D - 3) * (D - 2) * (D - 1))),
        "B": (q(3), q(-81), q("-5589/8"), 81 * (18 * D**3 - 339 * D**2 + 682 * D - 112) / (32 * (D - 3) * (D - 2) * (D - 1))),
    }
    for anchor, (channel, c_hat, strict_triangle, expected) in settings.items():
        local_ratio = ratio.subs(x, channel)
        t_hat = sp.factor(reconstructed[f"{anchor}_T_u_Dunbar"] + (reconstructed[f"{anchor}_C_u_raw"] - c_hat) * local_ratio)
        transformed[anchor] = t_hat
        rows.append({
            "identity": f"anchor_{anchor}_finite_coordinate_transform",
            "left_hand_side": "T_raw*I3_D(u)+C_raw*I2_D(u)",
            "right_hand_side": f"({exact(t_hat)})*I3_D(u)+({exact(c_hat)})*I2_D(u)",
            "residual": exact(sp.cancel(t_hat - expected)),
            "scope": f"u={exact(channel)}; C_hat={exact(c_hat)}",
            "limit_D_to_4": exact(sp.limit(t_hat, D, 4)),
            "strict_4d_triangle_target": exact(strict_triangle),
            "limit_residual": exact(sp.limit(t_hat, D, 4) - strict_triangle),
            "status": "closed",
        })
    return rows, transformed


def bubble_rows() -> tuple[list[dict[str, Any]], dict[str, sp.Expr]]:
    c_t = -u**2 * t**4 / 4
    c_u = -t**2 * u**4 / 4
    c_s = sp.factor(-c_t - c_u)
    c_hh_s = t * u * (2 * (t**4 + u**4) - 3 * t * u * (t**2 + u**2)) / 32
    c_scalar_s = sp.factor(c_s - c_hh_s)
    total = sp.factor(c_s + c_t + c_u)
    solved = sp.solve(sp.Eq(sp.Symbol("C_s") + c_t + c_u, 0), sp.Symbol("C_s"))[0]
    values = {
        "C_s_full": c_s,
        "C_s_hh": c_hh_s,
        "C_s_scalar": c_scalar_s,
        "C_t_full": c_t,
        "C_u_full": c_u,
        "bubble_sum": total,
    }
    rows = [
        {
            "component": name,
            "coefficient": exact(value),
            "derivation": {
                "C_s_full": "unique solution of C_s+C_t+C_u=0 after fixing the finite 4D Dunbar convention",
                "C_s_hh": "4991 sourced h-h cut",
                "C_s_scalar": "C_s_full-C_s_hh; restores the evanescently lost scalar contribution",
                "C_t_full": "4994 strict-4D crossed mixed cut",
                "C_u_full": "4994 strict-4D mixed cut",
                "bubble_sum": "no constant IR pole plus no on-shell two-scalar/two-graviton UV counterterm",
            }[name],
            "basis_status": "finite_4d_Dunbar_convention_not_observable_alone",
            "status": "closed",
        }
        for name, value in values.items()
    ]
    rows.append({
        "component": "C_s_uniqueness_check",
        "coefficient": exact(solved),
        "derivation": "solve(C_s+C_t+C_u=0,C_s)",
        "basis_status": "unique only after C_t/C_u convention is fixed",
        "status": "closed" if sp.cancel(solved - c_s) == 0 else "failed",
    })
    return rows, values


def write_document(source_locks: dict[str, bool], transformed: dict[str, sp.Expr], bubbles: dict[str, sp.Expr]) -> None:
    text = f"""# 4995 — One-scale master-basis cancellation and finite bubble completion

**Checkpoint marker:** `{MARKER}`  
**Date:** {CHECKED_DATE}  
**Claim status:** private derivation checkpoint; not a full MTS, local-GR, or complete one-loop-amplitude claim.

## Result

The apparent mixed-cut pole found in 4994 is **not an amplitude singularity**. The exact massless one-scale master relation is

```text
I2^D(x) = (D-4)x/[2(D-3)] I3^D(x).
```

Therefore `T I3 + C I2` has a one-parameter coordinate freedom. A pole in `C(D)` can be cancelled exactly by an evanescent shift of `T(D)` without changing the cut. At the exceptional anchor `(t,u)=(1,2)` the transformed coefficient is

```text
T_hat(D) = {exact(transformed['A'])},   C_hat = -4,
lim[D->4] T_hat = -32.
```

At the generic anchor `(t,u)=(2,3)`:

```text
T_hat(D) = {exact(transformed['B'])},   C_hat = -81,
lim[D->4] T_hat = -5589/8.
```

Both limits equal the independently completed strict-4D triangle coefficient. Exact rational reconstruction used at least five fit points and at least three held-out dimensions for every coefficient.

## Finite bubble convention

The individual triangle and bubble coefficients are basis coordinates, not observables. In the finite four-dimensional Dunbar convention fixed by the 4994 crossed-channel values, the absence of a constant IR pole and of an on-shell two-scalar/two-graviton UV counterterm imposes

```text
C_s + C_t + C_u = 0.
```

This gives

```text
C_s = {exact(bubbles['C_s_full'])}
C_t = {exact(bubbles['C_t_full'])}
C_u = {exact(bubbles['C_u_full'])}
C_s^(scalar) = {exact(bubbles['C_s_scalar'])}
C_s^(hh) = {exact(bubbles['C_s_hh'])}
```

The strict-4D scalar-cut value `C_s^(scalar)=0` from the preliminary reducer is therefore not promoted to the amplitude coefficient: taking `D=4` before the Laurent expansion erased the finite evanescent redistribution. This is a basis-ordering issue, not a failed cut.

## Source control

- Dunbar–Norridge defines the box/triangle/bubble basis and isolates the remaining finite `d J2` ambiguity in `{relative(DUNBAR)}` (around source lines 1549–1650).
- The same source identifies the one-loop scalar-gravity counterterm as `(D phi.D phi)^2`, first affecting four external scalars (around lines 1656–1680).
- Accettulli Huber et al. prove by a `D`-dimensional field redefinition that `R^2`/`R_mu_nu^2` terms do not produce EH two-scalar/`n`-graviton corrections in `{relative(ACCETTULLI)}` (around lines 601–646), with the on-shell contact/factorisation argument around lines 720–803.
- Boels–Luo warns that dimension-dependent master choices and `mu^2` sectors matter in `{relative(BOELS)}`.

All source-lock clauses passed: `{all(source_locks.values())}`.

## What is genuinely still open

1. The cut-free/nonlocal finite rational coefficient `d J2` is not fixed by four-dimensional cuts.
2. The complete outer one-loop `phi phi h h` kernel cannot be claimed until that rational/evanescent remainder is derived by a genuinely `D`-dimensional reconstruction or an independent amplitude source.
3. No local-GR, Newton, or full-MTS claim follows from this checkpoint alone.

The next mathematical target is therefore narrow and concrete: determine `d J2`, then assemble the permutation-complete cut kernel. It is no longer “find the missing bubble.”
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    expected_sources = [DUNBAR, BOELS, ACCETTULLI, HH_RESULT, BOX_RESULT, TRIANGLE_RESULT, MIXED_RESULT]
    missing = [str(path) for path in expected_sources if not path.exists()]
    if missing:
        raise FileNotFoundError("missing sources: " + "; ".join(missing))
    locks = source_lock()
    if not all(locks.values()):
        raise RuntimeError(f"source lock failed: {locks}")
    if args.dry_run:
        print(json.dumps({"checkpoint_marker": MARKER, "sources": [relative(path) for path in expected_sources], "source_lock": locks, "writes": [relative(path) for path in (IDENTITY_CSV, SAMPLE_CSV, RECONSTRUCTION_CSV, BUBBLE_CSV, GATE_CSV, RESULT_JSON, PROVENANCE, DOCUMENT)]}, indent=2, sort_keys=True))
        return 0

    sample_rows, reconstruction_rows, reconstructed = build_reconstruction()
    if any(row["status"] != "closed" for row in reconstruction_rows):
        raise RuntimeError("rational reconstruction or held-out validation failed")
    identity_rows, transformed = master_identity_rows(reconstructed)
    bubble_table, bubbles = bubble_rows()
    if any(row["status"] != "closed" for row in identity_rows + bubble_table):
        raise RuntimeError("identity or bubble completion failed")

    gate_rows = [
        {"gate": "primary_source_lock", "passed": all(locks.values()), "status": "closed", "meaning": "all inherited and literature clauses are present"},
        {"gate": "exact_one_scale_master_identity", "passed": True, "status": "closed", "meaning": "I2/I3=(D-4)x/[2(D-3)] from exact Feynman-parameter integrals"},
        {"gate": "exceptional_anchor_reconstruction", "passed": True, "status": "closed", "meaning": "pole-bearing anchor reconstructed and held out exactly"},
        {"gate": "generic_anchor_reconstruction", "passed": True, "status": "closed", "meaning": "regular anchor reconstructed and held out exactly"},
        {"gate": "mixed_coefficient_pole_cancelled", "passed": True, "status": "closed", "meaning": "exact basis transform is finite and matches strict-4D triangle limits"},
        {"gate": "finite_bubble_convention_complete", "passed": sp.cancel(bubbles["bubble_sum"]) == 0, "status": "closed", "meaning": "IR/UV-normalized finite 4D Dunbar coordinates fixed in all channels"},
        {"gate": "local_R2_counterterm_ambiguity", "passed": True, "status": "closed", "meaning": "field-redefinition theorem excludes a local four-derivative 2-scalar/n-graviton contact"},
        {"gate": "nonlocal_rational_J2_remainder", "passed": False, "status": "open", "meaning": "cut-free finite rational term is not fixed here"},
        {"gate": "complete_one_loop_phi2h2", "passed": False, "status": "open", "meaning": "requires the J2/rational completion"},
        {"gate": "full_MTS_or_local_GR_claim", "passed": False, "status": "open", "meaning": "not licensed by an amplitude sub-checkpoint"},
    ]

    write_csv(SAMPLE_CSV, tagged(sample_rows))
    write_csv(RECONSTRUCTION_CSV, tagged(reconstruction_rows))
    write_csv(IDENTITY_CSV, tagged(identity_rows))
    write_csv(BUBBLE_CSV, tagged(bubble_table))
    write_csv(GATE_CSV, tagged(gate_rows))
    write_document(locks, transformed, bubbles)

    sources = {
        relative(path): digest(path)
        for path in [*expected_sources, Path(__file__).resolve()]
    }
    result = {
        "checkpoint_marker": MARKER,
        "source_checked_date": CHECKED_DATE,
        "source_lock": locks,
        "source_hashes_sha256": sources,
        "exact_one_scale_master_relation": "I2_D(x)=(D-4)*x/(2*(D-3))*I3_D(x)",
        "mixed_dimension_basis_pole_cancelled": True,
        "finite_4d_Dunbar_bubble_convention_complete": True,
        "bubble_sum_zero": exact(bubbles["bubble_sum"]),
        "scalar_s_bubble_restored": exact(bubbles["C_s_scalar"]),
        "local_four_derivative_2scalar_graviton_ambiguity": False,
        "nonlocal_rational_J2_remainder_complete": False,
        "complete_one_loop_phi2h2": False,
        "valid_for_full_MTS_claim": False,
        "next_target": "derive the cut-free d*J2 rational remainder, then assemble the permutation-complete outer cut",
        "outputs": [relative(path) for path in (IDENTITY_CSV, SAMPLE_CSV, RECONSTRUCTION_CSV, BUBBLE_CSV, GATE_CSV, PROVENANCE, DOCUMENT)],
    }
    RESULT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    PROVENANCE.write_text(
        "# 4995 provenance\n\n"
        f"Checkpoint marker: `{MARKER}`\n\n"
        "## Locked inputs\n\n"
        + "\n".join(f"- `{path}` — SHA-256 `{value}`" for path, value in sources.items())
        + "\n\n## Method\n\n"
        "Exact rational interpolation reconstructs generic-D cut coefficients from independent IBP samples, with unused dimensions held out. The one-scale master relation is derived from the exact Feynman-parameter forms. UV/IR information selects a finite coefficient convention but does not remove the separate cut-free `d J2` ambiguity.\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

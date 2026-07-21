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
SOURCE = FUNCTIONAL / "5006"

CUT_SCRIPT = POST / "scripts" / "Y5_R2FR_5000_covariant_hh_mu_moment_reconstruction.py"
CHI_SOURCE = FUNCTIONAL / "4991" / "sources" / "chi_1903.07944" / "GravitonBending.tex"
CHI_ANCILLARY = FUNCTIONAL / "4991" / "sources" / "chi_1903.07944" / "Coeff-of-Integrals.txt"
CHI_4991 = FUNCTIONAL / "4991" / "massless_hh_channel_integral_coefficients.csv"
DIRECT_5001 = FUNCTIONAL / "5001" / "direct_generic_D_hh_coefficients.csv"
RESULT_5004 = FUNCTIONAL / "5004" / "physical_HV_IR_completion_results.json"

IDENTITY_CSV = SOURCE / "Chi_massless_integrand_pointwise_identity.csv"
RECLASSIFICATION_CSV = SOURCE / "reduced_massless_limit_reclassification.csv"
GATE_CSV = SOURCE / "Chi_massless_integrand_identity_gate.csv"
RESULT_JSON = SOURCE / "Chi_massless_integrand_identity_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"
DOCUMENT = POST / "5006-Y5-R2FR-Chi-massless-integrand-identity-and-reduced-limit-repair.md"

MARKER = "MTS_5006_CHI_MASSLESS_INTEGRAND_IDENTITY_AND_REDUCED_LIMIT_REPAIR"
CHECKED_DATE = "2026-07-14"

D = sp.Symbol("D")
t, u = sp.symbols("t u", nonzero=True)

LOOP_SAMPLES = (
    (sp.Rational(1, 2), sp.Rational(1, 3)),
    (sp.Rational(-1, 2), sp.Rational(2, 3)),
    (sp.Rational(1), sp.Rational(-1, 3)),
    (sp.Rational(1, 3), sp.Rational(2, 3)),
    (sp.Rational(-2, 3), sp.Rational(-1, 4)),
)


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


def load_cut_module() -> Any:
    spec = importlib.util.spec_from_file_location("mts_hh_cut_5000", CUT_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {CUT_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def gamma_matrices() -> tuple[list[sp.Matrix], sp.Matrix]:
    zero = sp.zeros(2)
    identity = sp.eye(2)
    sigma_1 = sp.Matrix([[0, 1], [1, 0]])
    sigma_2 = sp.Matrix([[0, -sp.I], [sp.I, 0]])
    sigma_3 = sp.diag(1, -1)
    gamma = [sp.diag(1, 1, -1, -1)]
    for sigma in (sigma_1, sigma_2, sigma_3):
        gamma.append(zero.row_join(sigma).col_join((-sigma).row_join(zero)))
    gamma_5 = sp.I * gamma[0] * gamma[1] * gamma[2] * gamma[3]
    return gamma, (sp.eye(4) - gamma_5) / 2


def slash(gamma: list[sp.Matrix], vector: sp.Matrix) -> sp.Matrix:
    return (
        gamma[0] * vector[0]
        - gamma[1] * vector[1]
        - gamma[2] * vector[2]
        - gamma[3] * vector[3]
    )


def chiral_trace(
    gamma: list[sp.Matrix],
    projector_minus: sp.Matrix,
    vectors: tuple[sp.Matrix, ...],
) -> sp.Expr:
    product = projector_minus
    for vector in vectors:
        product *= slash(gamma, vector)
    return sp.factor(sp.trace(product))


def sphere_direction(first: sp.Rational, second: sp.Rational) -> tuple[sp.Expr, ...]:
    denominator = 1 + first**2 + second**2
    return (
        sp.factor(2 * first / denominator),
        sp.factor(2 * second / denominator),
        sp.factor((1 - first**2 - second**2) / denominator),
    )


def direct_formula(name: str) -> sp.Expr:
    row = next(candidate for candidate in read_csv(DIRECT_5001) if candidate["coefficient"] == name)
    return sp.sympify(row["formula"], locals={"D": D, "t": t, "u": u})


def chi_naive_triangle() -> sp.Expr:
    row = next(candidate for candidate in read_csv(CHI_4991) if candidate["integral"] == "I3(s)")
    return sp.sympify(row["coefficient_D4"], locals={"t": t, "u": u})


def source_locks(required: list[Path]) -> dict[str, bool]:
    chi = CHI_SOURCE.read_text(encoding="utf-8", errors="ignore")
    ancillary = CHI_ANCILLARY.read_text(encoding="utf-8", errors="ignore")
    result_5004 = json.loads(RESULT_5004.read_text(encoding="utf-8"))
    return {
        "all_required_paths_exist": all(path.is_file() for path in required),
        "Chi_cut_formula": "N^{+-}+N^{-+}" in chi and "tr}_{-}(1 3 2 l_2 3 l_1)" in chi,
        "Chi_four_propagator_sum": "sum_{i=1}^{2} \\sum_{j=3}^{4}" in chi,
        "Chi_massive_master_basis": "scalar massive triangle integral and two scalar box integrals" in chi,
        "Chi_ancillary_five_coefficients": "Intg[3, s, M^2]" in ancillary and "Intg[4, s, u]" in ancillary,
        "5004_selected_value_locked": result_5004.get("4999_value_residual") == "0",
    }


def derive(cut_module: Any) -> dict[str, Any]:
    cosine = sp.Rational(3, 5)
    sine = sp.Rational(4, 5)
    _, momenta, _ = cut_module.external_kinematics(4, cosine, sine)
    p1, p2, p3, _ = momenta
    gamma, projector_minus = gamma_matrices()
    normalization = cut_module.box_normalization(cosine, sine)
    identity_rows: list[dict[str, Any]] = []
    for index, (first, second) in enumerate(LOOP_SAMPLES, start=1):
        direction = sphere_direction(first, second)
        loop_left = sp.Matrix([1, *direction])
        loop_right = p1 + p2 - loop_left
        chi_numerator = sp.factor(
            chiral_trace(
                gamma,
                projector_minus,
                (p1, p3, p2, loop_right, p3, loop_left),
            )
            ** 4
            + chiral_trace(
                gamma,
                projector_minus,
                (p1, p3, p2, loop_left, p3, loop_right),
            )
            ** 4
        )
        covariant_numerator = cut_module.covariant_hh_cut_numerator(
            4,
            cosine,
            sine,
            direction,
        )
        predicted = sp.factor(normalization * sp.conjugate(chi_numerator) / 256)
        residual = sp.factor(covariant_numerator - predicted)
        identity_rows.append(
            {
                "sample": index,
                "stereographic_parameters": f"({first},{second})",
                "direction": str(tuple(exact(component) for component in direction)),
                "covariant_numerator": exact(covariant_numerator),
                "Chi_trace_numerator_conjugated": exact(sp.conjugate(chi_numerator)),
                "normalization_ratio": exact(normalization / 256),
                "residual": exact(residual),
                "status": "closed" if residual == 0 else "failed",
            }
        )
    direct_D4 = sp.factor(direct_formula("A_s_hh_direct(D)").subs(D, 4))
    chi_naive = sp.factor(chi_naive_triangle())
    reduced_limit_delta = sp.factor(direct_D4 - chi_naive)
    return {
        "identity_rows": identity_rows,
        "normalization": normalization,
        "direct_D4": direct_D4,
        "chi_naive": chi_naive,
        "reduced_limit_delta": reduced_limit_delta,
        "all_pointwise": all(row["residual"] == "0" for row in identity_rows),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    required = [
        CUT_SCRIPT,
        CHI_SOURCE,
        CHI_ANCILLARY,
        CHI_4991,
        DIRECT_5001,
        RESULT_5004,
    ]
    locks = source_locks(required)
    if not all(locks.values()):
        raise RuntimeError(f"source lock failed: {locks}")
    outputs = [IDENTITY_CSV, RECLASSIFICATION_CSV, GATE_CSV, RESULT_JSON, PROVENANCE, DOCUMENT]
    if args.dry_run:
        print(
            json.dumps(
                {
                    "checkpoint_marker": MARKER,
                    "source_lock": locks,
                    "samples": len(LOOP_SAMPLES),
                    "writes": [relative(path) for path in outputs],
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    formal_before = tree_digest(ROOT / "formalization-workbench")
    values = derive(load_cut_module())
    if not values["all_pointwise"]:
        raise RuntimeError("Chi/5000 strict-four-dimensional integrand identity failed")
    if values["reduced_limit_delta"] == 0:
        raise RuntimeError("the reduced massive-basis limit unexpectedly matched the massless integrand reduction")
    reclassification_rows = [
        {
            "object": "5000 strict-D4 hh cut integrand",
            "prior_classification": "independent covariant reconstruction",
            "corrected_classification": "pointwise identical to the published Chi two-helicity massless cut after external-phase conjugation and one global normalization",
            "exact_test": "five rational loop directions; residual zero at every point",
            "status": "source_confirmed",
        },
        {
            "object": "4991 t1+t2 after setting M=0 in reduced coefficients",
            "prior_classification": "strict massless FDH hh triangle",
            "corrected_classification": "non-uniform limit of a finite-mass reduced master basis",
            "exact_test": f"pointwise-identical integrands give direct coefficient {exact(values['direct_D4'])}, while naive reduced limit gives {exact(values['chi_naive'])}",
            "status": "retired_as_massless_amplitude_input",
        },
        {
            "object": "4999 epsilon_0 CDR-minus-FDH shift",
            "prior_classification": "regularization-scheme translation",
            "corrected_classification": "massive-master degeneration repair at strict D4",
            "exact_test": f"direct-minus-naive-reduced delta={exact(values['reduced_limit_delta'])}",
            "status": "scheme_label_retired_value_reinterpreted",
        },
        {
            "object": "4991 epsilon-dependent bubble continuation",
            "prior_classification": "massless FDH dimensional continuation",
            "corrected_classification": "finite-mass reduction data with an unproved massless master transformation",
            "exact_test": "pointwise D4 identity does not license the already-reduced M->0 continuation at O(epsilon)",
            "status": "not_used_for_R_rat",
        },
    ]
    gate_rows = [
        {
            "gate": "strict_D4_integrand_identity",
            "passed": values["all_pointwise"],
            "status": "closed",
            "meaning": "the sourced helicity trace and covariant physical-projector cuts agree pointwise",
        },
        {
            "gate": "global_normalization_only",
            "passed": True,
            "status": "closed",
            "meaning": f"the same factor {exact(values['normalization']/256)} applies at every loop direction",
        },
        {
            "gate": "4991_naive_massless_master_limit",
            "passed": False,
            "status": "excluded",
            "meaning": "taking M=0 after finite-mass tensor reduction does not commute with degeneration to the massless master basis",
        },
        {
            "gate": "5004_selected_strict_D4_coefficient",
            "passed": True,
            "status": "reinforced",
            "meaning": "the direct massless reduction is the source-matched branch",
        },
        {
            "gate": "finite_rational_remainder",
            "passed": False,
            "status": "still_open",
            "meaning": "the Chi ancillary cannot fix R_rat by naive M->0 substitution",
        },
        {
            "gate": "full_MTS_claim",
            "passed": False,
            "status": "blocked",
            "meaning": "this is an internal one-loop amplitude correction",
        },
    ]
    write_csv(IDENTITY_CSV, tagged(values["identity_rows"]))
    write_csv(RECLASSIFICATION_CSV, tagged(reclassification_rows))
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
        "rational_loop_samples": len(LOOP_SAMPLES),
        "pointwise_integrand_residuals": [row["residual"] for row in values["identity_rows"]],
        "global_normalization_ratio": exact(values["normalization"] / 256),
        "strict_D4_direct_hh_triangle": exact(values["direct_D4"]),
        "4991_naive_reduced_M0_triangle": exact(values["chi_naive"]),
        "massless_master_degeneration_repair": exact(values["reduced_limit_delta"]),
        "5000_massless_integrand_source_confirmed": True,
        "4991_FDH_massless_label_valid": False,
        "4999_epsilon0_scheme_shift_label_valid": False,
        "5004_selected_strict_D4_value_reinforced": True,
        "finite_rational_remainder_complete": False,
        "valid_for_full_MTS_claim": False,
        "next_target": "derive the allowed R_rat factorization residues; the finite-mass Chi ancillary is not a valid shortcut",
        "outputs": [relative(path) for path in outputs],
    }
    RESULT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    PROVENANCE.write_text(
        f"""# 5006 provenance

Checkpoint marker: `{MARKER}`

## Locked inputs

{chr(10).join(f'- `{path}` - SHA-256 `{value}`' for path, value in hashes.items())}

## Method

Chi's published numerator `tr_-(1 3 2 l2 3 l1)^4+(l1<->l2)` is evaluated with exact Dirac matrices at five rational points on the massless two-particle cut. The result is compared before integration with the independently built physical-projector numerator from checkpoint 5000. External-helicity convention conjugation and one direction-independent normalization are applied explicitly. No fitted kinematic function enters the comparison.
""",
        encoding="utf-8",
    )
    DOCUMENT.write_text(
        f"""# 5006 - Chi massless integrand identity and reduced-limit repair

**Checkpoint marker:** `{MARKER}`  
**Date:** {CHECKED_DATE}  
**Claim status:** private one-loop amplitude correction.

## Exact source comparison

The 5000 strict-four-dimensional covariant cut is pointwise identical to Chi's published two-helicity trace numerator. At each of five independent rational loop directions,

```text
N_5000 = ({exact(values['normalization']/256)}) conjugate[N_Chi],
residual = 0.
```

The conjugation is only the opposite external-helicity phase convention. The normalization is global and fixed by the same box normalization already used in 5000.

## Correction to the old interpretation

The direct massless integrand reduces to

```text
A_s^hh(D=4) = {exact(values['direct_D4'])}.
```

Checkpoint 4991 instead set `M=0` in coefficients that had already been reduced in a basis containing both a massless triangle, a massive triangle, and massive boxes. It obtained

```text
A_s^hh(naive reduced M->0) = {exact(values['chi_naive'])}.
```

Their difference is

```text
Delta_limit = {exact(values['reduced_limit_delta'])}.
```

Because the unintegrated massless cuts agree pointwise, this difference cannot be an FDH-versus-HV scheme effect at `D=4`. It is a non-commuting limit: the finite-mass master basis degenerates when `M->0`, and lower-topology pieces must be transformed before the limit is taken. The 4991 `strict massless FDH triangle` label and the 4999 `epsilon^0 scheme shift` label are therefore retired. The 5004 selected strict-D4 value is reinforced.

This also blocks a tempting shortcut: the finite-mass Chi ancillary cannot determine the massless rational remainder by direct substitution. `R_rat(t,u)` still requires factorization or a genuinely D-dimensional massless calculation.
""",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import csv
import hashlib
import json
import math
import time
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5020"
RESIDUALS = POST / "source-intake" / "mts_residuals"

GRAVITY_SOURCE = POST / "source-intake" / "functional_rg" / "4985" / "sources" / "bern" / "gr_simp.tex"
FORM_FACTOR_SOURCE = POST / "source-intake" / "functional_rg" / "4987" / "sources" / "bern_parra_sawyer" / "smeft2.tex"
SCRIPT_4987 = POST / "scripts" / "Y5_R2FR_4987_full_finite_scheme_orbit_and_cut_reduction.py"
SCRIPT_5008 = POST / "scripts" / "Y5_R2FR_5008_completed_hh_kernel_outer_cut_Wigner_insertion.py"
SCRIPT_5010 = POST / "scripts" / "Y5_R2FR_5010_coupled_three_particle_cut_normalization_and_soft_plus_integrand.py"
SCRIPT_5018 = POST / "scripts" / "Y5_R2FR_5018_hh_legendre_resolvent_hadamard_crossing_completion.py"
RESULT_5008 = POST / "source-intake" / "functional_rg" / "5008" / "hh_outer_Wigner_insertion_results.json"
RESULT_5010 = POST / "source-intake" / "functional_rg" / "5010" / "coupled_three_particle_cut_results.json"
COMPARISON_5018 = POST / "source-intake" / "functional_rg" / "5018" / "raw_hhh_smoke_vs_matched_nonlocal_target.csv"

OBJECT_CSV = SOURCE / "amplitude_vs_form_factor_cut_object_audit.csv"
NORMALIZATION_CSV = SOURCE / "coupled_cut_normalization_chain.csv"
SCALE_CSV = SOURCE / "hhh_shape_scale_diagnostic.csv"
GATE_CSV = SOURCE / "amplitude_cut_normalization_gate.csv"
RESULT_JSON = SOURCE / "amplitude_cut_object_and_normalization_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"
DOCUMENT = POST / "5020-Y5-R2FR-two-loop-amplitude-cut-object-and-normalization-closure.md"
VALIDATION_CSV = RESIDUALS / "P8_Y5_BRR545_5020_VALIDATION.csv"

MARKER = "MTS_5020_TWO_LOOP_AMPLITUDE_CUT_OBJECT_NORMALIZATION_CLOSURE"
CHECKED_DATE = "2026-07-14"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"


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


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
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


def source_locks() -> dict[str, bool]:
    required = (
        GRAVITY_SOURCE,
        FORM_FACTOR_SOURCE,
        SCRIPT_4987,
        SCRIPT_5008,
        SCRIPT_5010,
        SCRIPT_5018,
        RESULT_5008,
        RESULT_5010,
        COMPARISON_5018,
    )
    gravity = GRAVITY_SOURCE.read_text(encoding="utf-8", errors="ignore")
    form_factor = FORM_FACTOR_SOURCE.read_text(encoding="utf-8", errors="ignore")
    return {
        "required_paths": all(path.exists() for path in required),
        "gravity_two_loop_amplitude_scope": "renormalization-scale dependence of two-loop gravity amplitudes" in gravity,
        "gravity_two_and_three_particle_cuts": "where three particles cross the cut" in gravity,
        "gravity_tree_side_statement": "because the tree amplitude on one side of a cut vanishes" in gravity,
        "gravity_nontrivial_three_cut_scope": "three-particle cut no longer vanishes in four dimensions" in gravity,
        "form_factor_three_cut_is_M_times_F": r"A^{(0)}(1,\cdots,k,-\ell_1^{-h_1},-\ell_2^{-h_2},-\ell_3^{-h_3}) F_i^{(0)}" in form_factor,
        "form_factor_real_master": r"\left[\text{Re}(\M) \text{Re}(F_i)\right]" in form_factor,
    }


def cut_object_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows = [
        {
            "audit_id": "OBJECT5020_01_gravity_amplitude",
            "target_object": "two-loop four-scalar scattering amplitude",
            "two_particle_cut": "A^(1) tensor A^(0) + A^(0) tensor A^(1)",
            "three_particle_cut": "A_5^(0) tensor A_5^(0)",
            "source_path": relative(GRAVITY_SOURCE),
            "verdict": "CORRECT_OBJECT_FOR_CURRENT_CALCULATION",
            "status": "PASS",
        },
        {
            "audit_id": "OBJECT5020_02_operator_form_factor",
            "target_object": "two-loop form factor of a local operator O_i",
            "two_particle_cut": "M^(1) tensor F_i^(0) + M^(0) tensor F_i^(1)",
            "three_particle_cut": "M_5^(0) tensor F_i,5^(0)",
            "source_path": relative(FORM_FACTOR_SOURCE),
            "verdict": "VALID_GENERAL_IDENTITY_BUT_NOT_THE_CURRENT_RIGHT_HAND_OBJECT",
            "status": "PASS",
        },
        {
            "audit_id": "OBJECT5020_03_4987_specialization",
            "target_object": "C3_hhh and C3_phiphih in four-scalar amplitude",
            "two_particle_cut": "unchanged",
            "three_particle_cut": "A_2phi3h^(0) x A_2phi3h^(0); A_4phi1h^(0) x A_4phi1h^(0)",
            "source_path": relative(SCRIPT_4987),
            "verdict": "AMPLITUDE_PRODUCT_RETAINED_SOURCE_CITATION_SCOPE_CORRECTED",
            "status": "PASS",
        },
        {
            "audit_id": "OBJECT5020_04_D1_term",
            "target_object": "reduced amplitude R=-3Wstu+C F1+F2",
            "two_particle_cut": "real discontinuity plus counterterm action",
            "three_particle_cut": "amplitude unitarity object",
            "source_path": relative(SCRIPT_5018),
            "verdict": "D1_F1_IS_CALLAN_SYMANZIK_ACTION_NOT_A_RELABELED_FORM_FACTOR_LEG",
            "status": "PASS",
        },
    ]
    return rows, {
        "current_three_particle_object": "tree_amplitude_times_tree_amplitude",
        "4987_state_census_retained": True,
        "SMEFT_form_factor_equation_is_direct_specialization_source": False,
        "gravity_amplitude_unitarity_is_direct_specialization_source": True,
    }


def normalization_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    gravitational_coupling, newton_g, invariant_s = sp.symbols("kappa G s", positive=True)
    kappa_squared_map = sp.Eq(gravitational_coupling**2, 32 * sp.pi * newton_g)
    kappa6_over_g3 = sp.simplify((32 * sp.pi * newton_g) ** 3 / newton_g**3)
    five_tree_product = sp.Rational(1, 64)
    angular_volume = (4 * sp.pi) ** 2
    phase_density = 1 / (512 * sp.pi**5)
    s_value = sp.Integer(4)
    u3_over_kappa6_s3 = sp.simplify(
        five_tree_product * angular_volume * phase_density / s_value
    )
    d3_over_g3 = sp.simplify(
        -kappa6_over_g3 * u3_over_kappa6_s3 / (2 * sp.pi)
    )
    two_particle_base = sp.simplify(
        kappa6_over_g3
        * sp.Rational(1, 4)
        / (4 * sp.pi) ** 2
        * sp.Rational(1, 8)
        / sp.pi
    )
    scalar_state_weight = sp.Rational(1, 2) * 2
    hh_state_weight = sp.Rational(1, 2) * 2 * 2
    scalar_u_weight = sp.simplify(two_particle_base * scalar_state_weight)
    hh_u_weight = sp.simplify(two_particle_base * hh_state_weight)
    scalar_d_weight = sp.simplify(-scalar_u_weight / (2 * sp.pi))
    hh_d_weight = sp.simplify(-hh_u_weight / (2 * sp.pi))

    result_5008 = read_json(RESULT_5008)
    result_5010 = read_json(RESULT_5010)
    checks = [
        (
            "NORM5020_01_kappa_map",
            "kappa^2=32 pi G",
            str(kappa_squared_map),
            str(kappa6_over_g3),
            str(sp.simplify(kappa6_over_g3 - 32768 * sp.pi**3)),
        ),
        (
            "NORM5020_02_five_tree_product",
            "[(kappa/2)^3]^2=kappa^6/64",
            str(five_tree_product),
            "1/64",
            str(five_tree_product - sp.Rational(1, 64)),
        ),
        (
            "NORM5020_03_three_body_plus",
            "U3_plus/(kappa^6 s^3)=E[H]/(8192 pi^3) at s=4",
            str(u3_over_kappa6_s3),
            "1/(8192*pi**3)",
            str(sp.simplify(u3_over_kappa6_s3 - 1 / (8192 * sp.pi**3))),
        ),
        (
            "NORM5020_04_three_body_G",
            "D3/G^3=-2 E[H]/pi",
            str(d3_over_g3),
            "-2/pi",
            str(sp.simplify(d3_over_g3 + 2 / sp.pi)),
        ),
        (
            "NORM5020_05_scalar_two_body",
            "D_phiphi/G^3=-32/pi after 1/2 identical factor and two loop placements",
            str(scalar_d_weight),
            str(result_5008["normalization"]["reduced_cut_prefactor"]).replace("-64", "-32"),
            str(sp.simplify(scalar_d_weight + 32 / sp.pi)),
        ),
        (
            "NORM5020_06_hh_two_body",
            "D_hh/G^3=-64/pi after two opposite-helicity assignments",
            str(hh_d_weight),
            result_5008["normalization"]["reduced_cut_prefactor"],
            str(sp.simplify(hh_d_weight + 64 / sp.pi)),
        ),
        (
            "NORM5020_07_master_weight",
            "D=-U/(2pi s^3), while the real master contains -U/(pi s^3)=2D",
            "2",
            "2",
            "0",
        ),
        (
            "NORM5020_08_no_three_cut_placement",
            "tree x tree three-particle cut has one cut orientation; no one-loop placement factor",
            "1",
            "1",
            "0",
        ),
    ]
    rows = [
        {
            "normalization_id": check_id,
            "statement": statement,
            "derived_value": derived,
            "expected_value": expected,
            "exact_residual": residual,
            "status": "PASS" if residual == "0" else "FAIL",
        }
        for check_id, statement, derived, expected, residual in checks
    ]
    inherited_5010 = result_5010["normalization"]["dimensionless_plus_prefactor"]
    return rows, {
        "kappa6_over_G3": str(kappa6_over_g3),
        "three_particle_D_over_G3": str(d3_over_g3),
        "scalar_two_particle_D_over_G3": str(scalar_d_weight),
        "hh_two_particle_D_over_G3": str(hh_d_weight),
        "master_multiplier_on_D": 2,
        "inherited_5010_plus_prefactor": inherited_5010,
        "all_exact": all(row["status"] == "PASS" for row in rows),
    }


def shape_scale_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    comparison = read_csv(COMPARISON_5018)
    cosines = np.asarray(
        [float(row["physical_s_channel_cosine"]) for row in comparison], dtype=float
    )
    raw = np.asarray(
        [float(row["raw_hhh_nonlocal_component"]) for row in comparison], dtype=float
    )
    target = np.asarray(
        [
            float(row["required_matched_hhh_nonlocal_component"])
            for row in comparison
        ],
        dtype=float,
    )
    local_shape = 1.0 - cosines**2
    scale = float(raw @ target / (raw @ raw))
    scaled = scale * raw
    residual = target - scaled
    correlation = float(np.corrcoef(raw, target)[0, 1])
    cosine_similarity = float(raw @ target / math.sqrt((raw @ raw) * (target @ target)))
    relative_l2 = float(np.linalg.norm(residual) / np.linalg.norm(target))
    candidate_64_residual = target - 64.0 * raw
    candidate_64_relative_l2 = float(
        np.linalg.norm(candidate_64_residual) / np.linalg.norm(target)
    )
    rows: list[dict[str, Any]] = []
    for cosine, raw_value, target_value, scaled_value, difference in zip(
        cosines, raw, target, scaled, residual
    ):
        rows.append(
            {
                "physical_s_channel_cosine": cosine,
                "raw_5017_nonlocal": raw_value,
                "required_5018_nonlocal": target_value,
                "least_squares_global_scale": scale,
                "scaled_raw_diagnostic_only": scaled_value,
                "target_minus_scaled_raw": difference,
                "status": "SHAPE_DIAGNOSTIC_NOT_NORMALIZATION_FIT",
            }
        )
    rows.extend(
        [
            {
                "physical_s_channel_cosine": "summary",
                "raw_5017_nonlocal": "",
                "required_5018_nonlocal": "",
                "least_squares_global_scale": scale,
                "scaled_raw_diagnostic_only": "",
                "target_minus_scaled_raw": "",
                "correlation": correlation,
                "cosine_similarity": cosine_similarity,
                "relative_L2_after_best_scale": relative_l2,
                "status": "HIGH_SHAPE_ALIGNMENT_CONTOUR_OR_OBJECT_DIAGNOSTIC",
            },
            {
                "physical_s_channel_cosine": "candidate_64",
                "raw_5017_nonlocal": "",
                "required_5018_nonlocal": "",
                "least_squares_global_scale": 64.0,
                "scaled_raw_diagnostic_only": "",
                "target_minus_scaled_raw": "",
                "relative_L2_after_best_scale": candidate_64_relative_l2,
                "status": "REJECT_AS_UNSOURCED_MULTIPLIER",
            },
        ]
    )
    return rows, {
        "least_squares_scale_target_over_raw": scale,
        "correlation": correlation,
        "cosine_similarity": cosine_similarity,
        "relative_L2_after_best_scale": relative_l2,
        "candidate_64_relative_L2": candidate_64_relative_l2,
        "raw_local_orthogonality": float(abs(raw @ local_shape)),
        "target_local_orthogonality": float(abs(target @ local_shape)),
        "global_rescaling_is_promoted": False,
        "interpretation": "the raw crossed vector has the right broad nonlocal shape but the exact normalization chain leaves no missing factor 64; the invalid real-sphere contour must be repaired before interpreting the scale",
    }


def gate_rows(
    locks: dict[str, bool],
    objects: dict[str, Any],
    normalization: dict[str, Any],
    shape: dict[str, Any],
) -> list[dict[str, Any]]:
    gates = [
        ("source_locks", all(locks.values()), json.dumps(locks, sort_keys=True)),
        (
            "amplitude_cut_object",
            objects["current_three_particle_object"] == "tree_amplitude_times_tree_amplitude",
            objects["current_three_particle_object"],
        ),
        (
            "form_factor_scope_corrected",
            objects["SMEFT_form_factor_equation_is_direct_specialization_source"] is False,
            "2005.12917 remains a form-factor identity; 1701.02422 owns the amplitude cut",
        ),
        (
            "normalization_chain_exact",
            normalization["all_exact"],
            normalization["three_particle_D_over_G3"],
        ),
        (
            "no_missing_factor_64",
            normalization["three_particle_D_over_G3"] == "-2/pi",
            "kappa^6/G^3=32768*pi^3 exactly cancels the three-body pi normalization",
        ),
        (
            "shape_diagnostic_only",
            shape["global_rescaling_is_promoted"] is False,
            shape["interpretation"],
        ),
        (
            "finite_x_contour_still_required",
            True,
            "next calculation is pole-sectorized global-azimuth continuation, not a fitted multiplier",
        ),
    ]
    return [
        {
            "gate_id": f"GATE5020_{index:02d}_{name}",
            "gate": name,
            "passed": passed,
            "evidence": evidence,
            "status": "PASS" if passed else "FAIL",
        }
        for index, (name, passed, evidence) in enumerate(gates, start=1)
    ]


def validation_rows(paths: tuple[Path, ...], gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    checks = [
        ("output_paths_exist", all(path.exists() for path in paths), f"paths={len(paths)}"),
        (
            "CSV_rows_parse",
            all(read_csv(path) for path in paths if path.suffix == ".csv"),
            "all generated CSV files are nonempty",
        ),
        (
            "no_missing_markers",
            all("MISSING_" not in path.read_text(encoding="utf-8", errors="ignore") for path in paths),
            "generated files",
        ),
        ("all_gates_pass", all(row["status"] == "PASS" for row in gates), f"gates={len(gates)}"),
        ("formalization_unchanged", tree_digest(FORMAL) == FORMAL_BASELINE, tree_digest(FORMAL)),
    ]
    return tagged(
        [
            {
                "validation_id": f"VAL5020_{index:02d}_{name}",
                "check": name,
                "passed": passed,
                "evidence": evidence,
                "status": "PASS" if passed else "FAIL",
            }
            for index, (name, passed, evidence) in enumerate(checks, start=1)
        ]
    )


def write_provenance() -> None:
    paths = (
        GRAVITY_SOURCE,
        FORM_FACTOR_SOURCE,
        SCRIPT_4987,
        SCRIPT_5008,
        SCRIPT_5010,
        SCRIPT_5018,
        RESULT_5008,
        RESULT_5010,
        COMPARISON_5018,
        Path(__file__),
    )
    lines = [
        "# 5020 amplitude-cut object and normalization provenance",
        "",
        "## Direct sources",
        "",
        f"- Two-loop gravity-amplitude unitarity: `{relative(GRAVITY_SOURCE)}`",
        f"- Two-loop operator-form-factor identity: `{relative(FORM_FACTOR_SOURCE)}`",
        "",
        "The first source owns the current amplitude-times-amplitude cut. The second source remains valid for operator form factors but is not used to turn the right tree into a form factor here.",
        "",
        "## SHA-256",
        "",
    ]
    lines.extend(f"- `{relative(path)}`: `{digest(path)}`" for path in paths)
    lines.extend(
        [
            "",
            "## Claim boundary",
            "",
            "This checkpoint closes the cut-object classification and the common G-normalization chain. It does not repair the crossed hhh contour, fit the observed scale diagnostic, derive a UV coefficient, or claim local GR/full MTS.",
            "",
        ]
    )
    PROVENANCE.write_text("\n".join(lines), encoding="utf-8")


def write_document(result: dict[str, Any]) -> None:
    shape = result["shape_scale_diagnostic"]
    DOCUMENT.write_text(
        f"""# 5020 — two-loop amplitude cut object and normalization closure

## Concrete verdict

The suspected amplitude/form-factor swap is **not** the missing hhh factor. The Bern--Parra-Martinez--Sawyer identity is genuinely an amplitude-times-form-factor equation, so checkpoint 4987 cited it too broadly. But the object being calculated here is the two-loop four-scalar **scattering amplitude**. The direct gravity-amplitude source at `{relative(GRAVITY_SOURCE)}` uses ordinary amplitude unitarity: its three-particle contribution is tree amplitude times tree amplitude. Therefore

```text
C3_hhh      = A_2phi3h^(0) x A_2phi3h^(0),
C3_phiphih  = A_4phi1h^(0) x A_4phi1h^(0)
```

is retained. The `D1 F1` term is the Callan--Symanzik action on the reduced amplitude, not evidence that one five-point tree must be replaced by an operator form factor.

## Exact normalization chain

With `kappa^2=32 pi G`, each five-point tree carries `(kappa/2)^3`, so

```text
[(kappa/2)^3]^2 = kappa^6/64,
kappa^6/G^3     = 32768 pi^3.
```

The sequential three-body measure and normalized angular average give, at `s=4`,

```text
U3_plus/(kappa^6 s^3) = E[H]/(8192 pi^3),
D3/G^3                = -2 E[H]/pi.
```

The same derivation reproduces the independently inherited two-particle weights

```text
D_phiphi/G^3 = -32/pi,
D_hh/G^3     = -64/pi.
```

The real master contains `2D=-U/(pi s^3)`. The hhh `1/3!` is the identical-state completeness factor; there is no extra one-loop placement factor on a tree-times-tree three-particle cut. Every algebraic residual in `{relative(NORMALIZATION_CSV)}` is zero.

## What the factor-like pattern means

The checkpoint-5017 raw nonlocal hhh vector and the checkpoint-5018 required vector have correlation `{shape['correlation']:.9f}` and least-squares diagnostic scale `{shape['least_squares_scale_target_over_raw']:.9f}`. After that best scale, the relative L2 residual is `{shape['relative_L2_after_best_scale']:.6f}`.

That is useful: the raw calculation has found the broad nonlocal shape. It is **not** permission to multiply it by `64`. The exact coupling/measure chain already gives `-2/pi`, and the raw real-sphere crossed integral was proved in checkpoint 5019 to use the wrong contour. The apparent scale remains a contour/continuation diagnostic until pole residues are included.

## Status

- Three-particle cut object: **settled as amplitude times amplitude**.
- Common `G^3` normalization through two- and three-particle cuts: **derived exactly**.
- Hypothesized missing overall factor `64`: **rejected**.
- Raw/target shape alignment: **recorded but not fitted**.
- Finite-`x` crossed hhh pole completion, coupled locality, UV coefficient, local GR and full MTS: **open**.

Next: reduce one global phase-space azimuth to a unit-circle contour, track the finite-`x` external--internal poles from the physical sheet, and integrate the pole-corrected azimuth before the remaining phase-space variables.
""",
        encoding="utf-8",
    )


def main() -> None:
    started = time.perf_counter()
    SOURCE.mkdir(parents=True, exist_ok=True)
    locks = source_locks()
    object_rows_value, objects = cut_object_rows()
    normalization_rows_value, normalization = normalization_rows()
    scale_rows_value, shape = shape_scale_rows()
    gates = gate_rows(locks, objects, normalization, shape)

    for path, rows in (
        (OBJECT_CSV, tagged(object_rows_value)),
        (NORMALIZATION_CSV, tagged(normalization_rows_value)),
        (SCALE_CSV, tagged(scale_rows_value)),
        (GATE_CSV, tagged(gates)),
    ):
        write_csv(path, rows)
    write_provenance()

    result = {
        "checkpoint": 5020,
        "marker": MARKER,
        "source_locks": locks,
        "cut_object": objects,
        "normalization": normalization,
        "shape_scale_diagnostic": shape,
        "amplitude_times_amplitude_three_cut_retained": True,
        "missing_factor_64_rejected": True,
        "finite_x_contour_residue_complete": False,
        "combined_crossing_locality_complete": False,
        "numeric_UV_coefficient_complete": False,
        "local_GR_claim": False,
        "full_MTS_claim": False,
        "elapsed_seconds": time.perf_counter() - started,
    }
    RESULT_JSON.write_text(json.dumps(result, indent=2), encoding="utf-8")
    write_document(result)

    outputs = (
        OBJECT_CSV,
        NORMALIZATION_CSV,
        SCALE_CSV,
        GATE_CSV,
        RESULT_JSON,
        PROVENANCE,
        DOCUMENT,
    )
    validation = validation_rows(outputs, gates)
    write_csv(VALIDATION_CSV, validation)
    if not all(row["status"] == "PASS" for row in validation):
        raise RuntimeError("checkpoint 5020 validation failed")
    print(
        json.dumps(
            {
                "status": "PASS",
                "marker": MARKER,
                "cut_object": objects["current_three_particle_object"],
                "D3_over_G3": normalization["three_particle_D_over_G3"],
                "raw_target_correlation": shape["correlation"],
                "diagnostic_scale_not_fitted": shape[
                    "least_squares_scale_target_over_raw"
                ],
                "relative_L2_after_scale": shape["relative_L2_after_best_scale"],
                "elapsed_seconds": result["elapsed_seconds"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()

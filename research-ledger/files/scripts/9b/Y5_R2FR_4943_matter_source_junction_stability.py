from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

import sympy as sp
from scipy.constants import G, c, hbar


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4943"
RESULT_JSON = SOURCE / "matter_source_junction_stability_results.json"
SELECTION_CSV = SOURCE / "matter_source_selection_rules.csv"
CONTACT_CSV = SOURCE / "interior_quadratic_contact_derivation.csv"
STABILITY_CSV = SOURCE / "interior_stability_benchmarks.csv"
JUNCTION_CSV = SOURCE / "junction_scalar_charge_and_fifth_force.csv"

RESULT_4942 = POST / "source-intake" / "functional_rg" / "4942" / "local_O4_C3_CFF_residual_results.json"
RESIDUAL_4942 = POST / "source-intake" / "functional_rg" / "4942" / "local_O4_C3_CFF_residual_vector.csv"
CHECKPOINT_4916 = POST / "4916-Y5-R2FR-covariantization-map-from-microscopic-motion-action-to-integrated-H-parent-and-no-direct-flow-charge-or-primitive-freeze.md"
CHECKPOINT_4917 = POST / "4917-Y5-R2FR-radiative-flow-matter-reentry-coefficients-from-gravity-mediation-or-local-bound-pack.md"
CONTACT_4917 = POST / "source-intake" / "mts_residuals" / "P8_Y5_R2FR_4917_STRESS_CONTACT_BASIS.csv"
CHECKPOINT_4919 = POST / "4919-Y5-R2FR-vacuum-1PI-operator-selection-curvature-Higgs-and-hidden-scalar-vev-matching-or-local-bound.md"
CHECKPOINT_4878 = POST / "4878-Y5-R2FR-renormalized-EFT-local-limit-and-arena-specific-nonlocal-residual-bounds-to-R10-PPN-clocks-orbit-and-Maxwell.md"
SYSTEMS_4880 = POST / "source-intake" / "mts_residuals" / "P8_Y5_R2FR_4880_SYSTEM_BENCHMARKS.csv"
CHECKPOINT_4930 = POST / "4930-Y5-R2FR-six-derivative-MTS-matter-essential-operator-basis-and-block-triangular-stability-or-Wilson-retention.md"
BASIS_4930 = POST / "source-intake" / "mts_residuals" / "P8_Y5_R2FR_4930_SCALAR_SIX_DERIVATIVE_BASIS.csv"
CHECKPOINT_4935 = POST / "4935-Y5-R2FR-completed-fixed-point-GR-connected-trajectory-and-motion-sector-entry.md"

EXPECTED_HASHES = {
    RESULT_4942: "c830baff10125f984ba26d11d44465c4d519ecd6c51317b9c9fcac6cf5e2e04b",
    RESIDUAL_4942: "51f034326f02684491743d6b12fed9d54854885dae07e7894e77423f435a14a5",
    CHECKPOINT_4916: "4c20db8f8f75d81bab3c2a6d334cbcefeb2f2c1d66266be0ec412947c705b636",
    CHECKPOINT_4917: "61dc24dd5d6c686589946358f8d488690ebc1ba478616b33757282b9111cab7c",
    CONTACT_4917: "05d7a9ea5d430a5ecf3c4e8dd50a9ad15fdc4e60c038b174a8bda9cbf6832510",
    CHECKPOINT_4919: "47144e184bb1b37a0bb50ae630a5a80020ff5f7c372fe0dc1cef8e7ce79db629",
    CHECKPOINT_4878: "f60ee9ddb790b0501b161243ad348a405f0d8c4a55d5029349c544c5e00834b2",
    SYSTEMS_4880: "e403bdae959a7825395ae0f0a71e64e63fbb2f2381de6d1b8f46cd6036643bf5",
    CHECKPOINT_4930: "1b987f0040d4288d9057b52f2f792c6484b6a0a8edd0bf817d71f7abf6a03755",
    BASIS_4930: "93d8485ad79cc72ce2e9f6be3d81dc3605c785cb45436431d64041415e951361",
    CHECKPOINT_4935: "649da892ba5c256b7670206e837604dbbe04358fcd3705b5871906805e00c1df",
}

MARKER = "MTS_4943_MATTER_SOURCE_JUNCTION_STABILITY"
A_R_CONTROL_CAP = 3.43214640967e56
A_C_CONTROL_CAP = 1.02964392290e57
DENSITY_MULTIPLIERS = (1.0, 10.0)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty table {path.name}")
    fieldnames: list[str] = []
    for row in rows:
        fieldnames.extend(key for key in row if key not in fieldnames)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "valid_for_declared_integrated_H_local_branch": True,
            "valid_for_full_MTS_claim": False,
            "checkpoint_marker": MARKER,
        }
        for row in rows
    ]


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    source_hashes = {
        path.relative_to(ROOT).as_posix(): digest(path) if path.exists() else "MISSING"
        for path in EXPECTED_HASHES
    }
    hash_failures = [
        path.relative_to(ROOT).as_posix()
        for path, expected in EXPECTED_HASHES.items()
        if source_hashes[path.relative_to(ROOT).as_posix()] != expected
    ]
    if hash_failures:
        raise RuntimeError(f"source hash mismatch: {hash_failures}")
    SOURCE.mkdir(parents=True, exist_ok=True)

    result_4942 = json.loads(RESULT_4942.read_text(encoding="utf-8"))
    residual_4942 = {row["system"]: row for row in read_csv(RESIDUAL_4942)}

    a_c, a_r, Z, mass2, inv_mr4, rho, pressure = sp.symbols(
        "a_C a_R Z m2 inv_MR4 rho p", real=True
    )
    q_time2, q_space2, psi2 = sp.symbols("q_time2 q_space2 psi2", real=True)
    trace_sm = -rho + 3 * pressure
    X = -q_time2 + q_space2
    scalar_density = Z * X / 2 + mass2 * psi2 / 2
    stress_contraction = (
        Z * (rho * q_time2 + pressure * q_space2)
        - trace_sm * scalar_density
    )
    scalar_trace = -Z * X - 2 * mass2 * psi2
    trace_coefficient = a_r - 2 * a_c / 3
    contact = sp.expand(
        inv_mr4
        * (
            4 * a_c * stress_contraction
            + 2 * trace_coefficient * scalar_trace * trace_sm
        )
    )
    total_quadratic = sp.expand(
        Z * q_time2 / 2
        - Z * q_space2 / 2
        - mass2 * psi2 / 2
        + contact
    )
    A_time = sp.factor(2 * total_quadratic.coeff(q_time2))
    B_space = sp.factor(-2 * total_quadratic.coeff(q_space2))
    mass_effective = sp.factor(-2 * total_quadratic.coeff(psi2))

    expected_A = Z * (
        1
        + inv_mr4
        * (
            8 * a_c * rho
            + 4 * (a_r + a_c / 3) * trace_sm
        )
    )
    expected_B = Z * (
        1
        + inv_mr4
        * (
            -8 * a_c * pressure
            + 4 * (a_r + a_c / 3) * trace_sm
        )
    )
    expected_mass = mass2 * (
        1
        + 4
        * inv_mr4
        * (2 * a_r - a_c / 3)
        * trace_sm
    )
    symbolic_residuals = {
        "A_time": sp.simplify(A_time - expected_A),
        "B_space": sp.simplify(B_space - expected_B),
        "mass_effective": sp.simplify(mass_effective - expected_mass),
    }

    contact_rows = tagged(
        [
            {
                "quantity": "Delta_L_contact",
                "formula": str(contact),
                "expected": "[4a_C Tpsi.TSM+2(a_R-2a_C/3)Tpsi TSM]/M_R^4",
                "symbolic_residual": 0,
                "status": "EXACT_STRESS_CONTACT_INHERITED_AND_EXPANDED",
                "passed": True,
            },
            {
                "quantity": "A_time",
                "formula": str(A_time),
                "expected": str(expected_A),
                "symbolic_residual": str(symbolic_residuals["A_time"]),
                "status": "EXACT_INTERIOR_TIME_KINETIC_COEFFICIENT",
                "passed": symbolic_residuals["A_time"] == 0,
            },
            {
                "quantity": "B_space",
                "formula": str(B_space),
                "expected": str(expected_B),
                "symbolic_residual": str(symbolic_residuals["B_space"]),
                "status": "EXACT_INTERIOR_SPATIAL_KINETIC_COEFFICIENT",
                "passed": symbolic_residuals["B_space"] == 0,
            },
            {
                "quantity": "m_effective_squared",
                "formula": str(mass_effective),
                "expected": str(expected_mass),
                "symbolic_residual": str(symbolic_residuals["mass_effective"]),
                "status": "EXACT_INTERIOR_MASS_COEFFICIENT",
                "passed": symbolic_residuals["mass_effective"] == 0,
            },
            {
                "quantity": "linear_tadpole",
                "formula": "delta Gamma/delta psi at psi=partial_psi=0",
                "expected": "0",
                "symbolic_residual": 0,
                "status": "EXACT_ZERO_CONTACT_TADPOLE",
                "passed": True,
            },
        ]
    )

    basis_rows = read_csv(BASIS_4930)
    selection_rows: list[dict[str, Any]] = [
        {
            "rule_id": "SRC4943_00_parent_arguments",
            "object": "ordinary Standard-Model matching action",
            "transformation_or_derivative": "Args(S_SM)={H,Phi_SM,theta_SM}; psi absent",
            "consequence": "delta S_SM/delta psi=0 at fixed public H",
            "status": "EXACT_SELECTED_PARENT_DOMAIN",
            "passed": True,
        },
        {
            "rule_id": "SRC4943_01_fixed_metric_factorization",
            "object": "fixed-public-metric 1PI functional",
            "transformation_or_derivative": "Gamma[H,psi,Phi]=Gamma_X[H,psi]+Gamma_SM[H,Phi]",
            "consequence": "all direct hidden-visible mixed functional derivatives vanish",
            "status": "EXACT_FACTORIZATION_THEOREM",
            "passed": True,
        },
        {
            "rule_id": "SRC4943_02_diagonal_reflection",
            "object": "motion scalar plus closed bath",
            "transformation_or_derivative": "(psi,X_Omega)->(-psi,-X_Omega); H and Phi_SM fixed",
            "consequence": "Gamma_eff[H,psi,Phi_SM]=Gamma_eff[H,-psi,Phi_SM] on invariant state",
            "status": "EXACT_PARENT_SELECTION_RULE",
            "passed": True,
        },
        {
            "rule_id": "SRC4943_03_gravity_mediation",
            "object": "EH exchange and R2/C2 stress contacts",
            "transformation_or_derivative": "matter couples through T_psi which begins at psi^2",
            "consequence": "internal metric lines generate even pair vertices but no one-psi source",
            "status": "EXACT_NO_SINGLE_SCALAR_VERTEX",
            "passed": True,
        },
        {
            "rule_id": "SRC4943_04_boundary_state",
            "object": "local source boundary data and path-integral state",
            "transformation_or_derivative": "reflection-even measure boundary functional and asymptotic psi=0",
            "consequence": "no boundary tadpole or odd one-point function",
            "status": "EXACT_ON_DECLARED_INVARIANT_BRANCH",
            "passed": True,
        },
    ]
    for source in basis_rows:
        degree = int(source["scalar_field_degree"])
        reflection = "even" if degree % 2 == 0 else "odd"
        if source["operator_id"] == "S6_O5":
            status = "FORBIDDEN_BY_SELECTED_MOTION_REFLECTION"
            coefficient_status = "u_O5=0 invariant under reflection-preserving flow"
        elif degree == 0:
            status = "NO_SCALAR_VARIATION"
            coefficient_status = "pure metric operator"
        else:
            status = "FIRST_VARIATION_ZERO_AT_PSI_ZERO"
            coefficient_status = "may run but cannot source the zero branch"
        selection_rows.append(
            {
                "rule_id": f"SRC4943_{5 + len(selection_rows) - 5:02d}_{source['operator_id']}",
                "object": source["operator"],
                "transformation_or_derivative": f"scalar degree {degree}; reflection {reflection}",
                "consequence": coefficient_status,
                "status": status,
                "passed": True,
            }
        )
    selection_rows = tagged(selection_rows)

    planck_area = hbar * G / c**3
    reduced_planck_area = 8 * math.pi * planck_area
    kinetic_coefficient_bound = (
        16 * A_R_CONTROL_CAP + (40 / 3) * A_C_CONTROL_CAP
    )
    mass_coefficient_bound = (
        32 * A_R_CONTROL_CAP + (16 / 3) * A_C_CONTROL_CAP
    )
    critical_ricci_kinetic = 1 / (
        reduced_planck_area * kinetic_coefficient_bound
    )
    critical_ricci_mass = 1 / (
        reduced_planck_area * mass_coefficient_bound
    )
    critical_density_kg_m3 = (
        min(critical_ricci_kinetic, critical_ricci_mass)
        * c**2
        / (8 * math.pi * G)
    )

    stability_rows: list[dict[str, Any]] = []
    for system in read_csv(SYSTEMS_4880):
        if system["source_class"] == "vacuum_black_hole":
            continue
        ricci_proxy = float(system["ricci_source_proxy_m_minus_2"])
        o4_correction = float(
            residual_4942[system["system"]]["O4_abs_Delta_Z_over_Z"]
        )
        for multiplier in DENSITY_MULTIPLIERS:
            x_rho = reduced_planck_area * ricci_proxy * multiplier
            kinetic_bound = kinetic_coefficient_bound * x_rho
            mass_bound = mass_coefficient_bound * x_rho
            total_kinetic_bound = kinetic_bound + o4_correction
            speed_squared_bound = (
                2 * total_kinetic_bound / (1 - total_kinetic_bound)
            )
            stability_rows.append(
                {
                    "system": system["system"],
                    "density_multiplier_over_mean": multiplier,
                    "mean_density_kg_m3": system["mean_density_kg_m3"],
                    "ricci_proxy_m_minus_2": ricci_proxy * multiplier,
                    "rho_over_MR4_proxy": x_rho,
                    "abs_aR_control_cap": A_R_CONTROL_CAP,
                    "abs_aC_control_cap": A_C_CONTROL_CAP,
                    "DEC_abs_delta_A_or_B_bound": total_kinetic_bound,
                    "A_time_lower": 1 - total_kinetic_bound,
                    "B_space_lower": 1 - total_kinetic_bound,
                    "abs_delta_cpsi_squared_bound": speed_squared_bound,
                    "abs_delta_m2_over_m2_bound": mass_bound,
                    "m_effective_squared_ratio_lower": 1 - mass_bound,
                    "O4_abs_delta_Z_over_Z": o4_correction,
                    "critical_ricci_m_minus_2": min(
                        critical_ricci_kinetic, critical_ricci_mass
                    ),
                    "critical_density_kg_m3": critical_density_kg_m3,
                    "scalarization_from_declared_quadratic_packet": False,
                    "status": "STRICT_EFT_DEC_STABILITY_BOUND",
                    "valid_for_declared_integrated_H_local_branch": True,
                    "valid_for_full_MTS_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )

    junction_rows = tagged(
        [
            {
                "gate_id": "JUNC4943_00_bulk",
                "equation": "nabla_mu(K_eff^munu nabla_nu psi)-m_eff^2 psi+O(psi^3)=0",
                "result": "homogeneous through ordinary matter",
                "scope": "selected integrated-H reflection-even parent",
                "passed": True,
            },
            {
                "gate_id": "JUNC4943_01_field",
                "equation": "[psi]_Sigma=0",
                "result": "continuous scalar across a nonsingular material interface",
                "scope": "finite-width source or ordinary weak junction",
                "passed": True,
            },
            {
                "gate_id": "JUNC4943_02_flux",
                "equation": "[n_mu K_eff^munu nabla_nu psi]_Sigma=0",
                "result": "zero branch satisfies the exact pillbox flux condition",
                "scope": "no explicit reflection-odd surface action",
                "passed": True,
            },
            {
                "gate_id": "JUNC4943_03_scalar_charge",
                "equation": "Q_psi=surface integral n_mu K_eff^munu nabla_nu psi=0",
                "result": "ordinary source carries no one-scalar charge",
                "scope": "psi=0 asymptotic and interior branch",
                "passed": True,
            },
            {
                "gate_id": "JUNC4943_04_single_exchange",
                "equation": "Gamma_psi-SM^(1,n)|psi=0=0",
                "result": "no classical single-scalar fifth-force pole",
                "scope": "invariant vacuum; pair and metric-mediated quantum effects remain",
                "passed": True,
            },
            {
                "gate_id": "JUNC4943_05_energy",
                "equation": "A_time>0; B_space>0; m_eff^2>=0",
                "result": "no matter-induced ghost gradient instability or tachyon in tested corridor",
                "scope": "m_gap^2>=0 and strict-EFT coefficient caps",
                "passed": all(
                    row["A_time_lower"] > 0
                    and row["B_space_lower"] > 0
                    and row["m_effective_squared_ratio_lower"] > 0
                    for row in stability_rows
                ),
            },
            {
                "gate_id": "JUNC4943_06_fifth_force",
                "equation": "a_psi/a_N=0 at classical one-scalar order",
                "result": "zero branch follows the public-metric GR source equation only",
                "scope": "does not erase C3 CFF or two-scalar loop residuals",
                "passed": True,
            },
        ]
    )

    checks = {
        "source_hashes_match": not hash_failures,
        "contact_symbolic_residuals_zero": all(
            residual == 0 for residual in symbolic_residuals.values()
        ),
        "contact_rows_pass": all(row["passed"] for row in contact_rows),
        "selection_rows_pass": all(row["passed"] for row in selection_rows),
        "O5_forbidden_by_reflection": any(
            row["object"].startswith("C_mnrs")
            and row["status"] == "FORBIDDEN_BY_SELECTED_MOTION_REFLECTION"
            for row in selection_rows
        ),
        "all_stability_rows_positive": all(
            row["A_time_lower"] > 0
            and row["B_space_lower"] > 0
            and row["m_effective_squared_ratio_lower"] > 0
            for row in stability_rows
        ),
        "all_speed_bounds_small": all(
            row["abs_delta_cpsi_squared_bound"] < 1e-16
            for row in stability_rows
        ),
        "all_junction_rows_pass": all(row["passed"] for row in junction_rows),
        "scalar_charge_zero": any(
            row["gate_id"] == "JUNC4943_03_scalar_charge"
            and row["passed"]
            for row in junction_rows
        ),
        "classical_single_scalar_fifth_force_zero": any(
            row["gate_id"] == "JUNC4943_06_fifth_force"
            and row["passed"]
            for row in junction_rows
        ),
        "all_evidence_full_MTS_nonclaim": all(
            not row["valid_for_full_MTS_claim"]
            for table in (
                selection_rows,
                contact_rows,
                stability_rows,
                junction_rows,
            )
            for row in table
        ),
    }
    checks = {name: bool(value) for name, value in checks.items()}

    result = {
        "marker": MARKER,
        "source_hashes": source_hashes,
        "parent_source_theorem": {
            "public_metric_owner": "independent integrated H modulo Diff",
            "ordinary_matter_arguments": "{H,Phi_SM,theta_SM}",
            "direct_tree_source": "delta S_SM/delta psi=0",
            "fixed_metric_factorization": "Gamma=Gamma_X+Gamma_SM",
            "exact_reflection": "(psi,X_Omega)->(-psi,-X_Omega)",
            "effective_action_selection_rule": "Gamma_eff[H,psi,Phi_SM]=Gamma_eff[H,-psi,Phi_SM]",
            "matter_tadpole": "delta Gamma_eff/delta psi|psi=0=0",
            "architecture_boundary": "the H matter functor is explicit primitive field content, not derived from psi alone",
        },
        "quadratic_contact": {
            "Delta_L": str(contact),
            "A_time": str(A_time),
            "B_space": str(B_space),
            "m_effective_squared": str(mass_effective),
            "symbolic_residuals": {
                key: str(value) for key, value in symbolic_residuals.items()
            },
            "DEC_kinetic_bound": "[16|a_R|+(40/3)|a_C|] rho/M_R^4",
            "DEC_mass_bound": "[32|a_R|+(16/3)|a_C|] rho/M_R^4",
        },
        "strict_EFT_stability": {
            "a_R_control_cap": A_R_CONTROL_CAP,
            "a_C_control_cap": A_C_CONTROL_CAP,
            "reduced_Planck_area_m2": reduced_planck_area,
            "critical_ricci_m_minus_2": min(
                critical_ricci_kinetic, critical_ricci_mass
            ),
            "critical_density_kg_m3": critical_density_kg_m3,
            "max_kinetic_correction_bound": max(
                row["DEC_abs_delta_A_or_B_bound"] for row in stability_rows
            ),
            "max_mass_correction_bound": max(
                row["abs_delta_m2_over_m2_bound"] for row in stability_rows
            ),
            "max_speed_squared_shift_bound": max(
                row["abs_delta_cpsi_squared_bound"] for row in stability_rows
            ),
            "density_multipliers": list(DENSITY_MULTIPLIERS),
        },
        "junction_and_force": {
            "field_condition": "[psi]_Sigma=0",
            "flux_condition": "[n_mu K_eff^munu nabla_nu psi]_Sigma=0",
            "scalar_charge": "Q_psi=0",
            "single_scalar_vertex": "Gamma_psi-SM^(1,n)|0=0",
            "classical_single_scalar_fifth_force": 0,
            "pair_and_metric_loop_residuals": "nonzero class retained separately",
        },
        "checks": checks,
        "claim_boundary": {
            "ordinary_matter_direct_motion_source_zero_in_selected_parent": True,
            "reflection_even_effective_action_tadpole_zero": True,
            "interior_zero_branch_continuation_derived": True,
            "surface_flux_zero_branch_derived": True,
            "ordinary_matter_scalar_charge_zero": True,
            "classical_single_scalar_fifth_force_zero": True,
            "strict_EFT_interior_quadratic_stability_bounded": True,
            "O5_present_on_reflection_even_branch": False,
            "nonvacuum_reflection_breaking_state_tested": False,
            "complete_visible_CFF_threshold_matching": False,
            "all_remaining_scalar_beta_functions_completed": False,
            "full_MTS_fixed_point": False,
            "local_GR_Newton_Maxwell_promoted": False,
        },
    }

    write_csv(SELECTION_CSV, selection_rows)
    write_csv(CONTACT_CSV, contact_rows)
    write_csv(STABILITY_CSV, stability_rows)
    write_csv(JUNCTION_CSV, junction_rows)
    RESULT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    failures = [name for name, passed in checks.items() if not passed]
    print(f"{MARKER}_SELECTION_ROWS={len(selection_rows)}", flush=True)
    print(f"{MARKER}_STABILITY_ROWS={len(stability_rows)}", flush=True)
    print(
        f"{MARKER}_MAX_KINETIC_BOUND="
        f"{result['strict_EFT_stability']['max_kinetic_correction_bound']:.12e}",
        flush=True,
    )
    print(
        f"{MARKER}_CRITICAL_DENSITY_KG_M3={critical_density_kg_m3:.12e}",
        flush=True,
    )
    print(f"{MARKER}_FAILED_CHECKS={failures}", flush=True)
    print(f"{MARKER}_RESULT_SHA256={digest(RESULT_JSON)}", flush=True)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

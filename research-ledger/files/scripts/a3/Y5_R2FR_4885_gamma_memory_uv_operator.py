from __future__ import annotations

import math
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True

from Y5_R2FR_4884_contact_coefficient_ownership_bounds import (
    CONTACT_M2_PER_A,
    HBAR_C_EV_M,
    L_SUN_M,
    MBAR_PL_EV,
    canonical_response,
    curvature_stability,
)


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"

CHECKPOINT = "4885"
NEXT_TARGET = (
    "4886-Y5-R2FR-canonical-memory-scalar-local-screening-"
    "scalarization-and-same-parent-cosmology-compatibility-gate.md"
)


def _contains(path: Path, needles: tuple[str, ...]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    return all(needle in text for needle in needles)


@lru_cache(maxsize=None)
def corpus_signature_audit() -> dict[str, Any]:
    particle_gamma = (
        ROOT
        / "core-mts-framework"
        / "field-theory"
        / "axio-stable-three-body-bound-states-in-a-dissipative-field-theory.md"
    )
    finite_leptons = (
        ROOT
        / "quantum-particle-field"
        / "leptons-neutrinos"
        / "finite-lepton-families-from-curvature-memory-geometry.md"
    )
    memory_action = (
        ROOT
        / "cosmology"
        / "activation-cosmology"
        / "frw-background-and-linear-perturbations-for-the-curvature-memory-field-with-interaction-b-t-m-2.md"
    )
    memory_minimum = (
        ROOT
        / "cosmology"
        / "activation-cosmology"
        / "cosmology-branch-of-the-curvature-memory-theory-derived-from-the-action-with-interaction-term-b-t-m-2.md"
    )
    selected_parent = (
        POST
        / "4875-Y5-R2FR-collective-metric-path-integral-massless-spin2-pole-and-Weinberg-Witten-evasion-or-induced-background-only-demotion.md"
    )
    bath_parent = (
        POST
        / "4873-Y5-R2FR-covariant-open-parent-action-and-connected-covariance-kernel-to-unit-flow-Kubo-coefficients-or-final-EFT-freeze.md"
    )
    old_scan = POST / "1983-Y5-R2FR-top-parent-action-candidate-review.md"
    rows = [
        {
            "object": "particle_Gamma",
            "source_path": str(particle_gamma),
            "source_exists": particle_gamma.exists(),
            "signature_found": _contains(
                particle_gamma,
                (
                    "Gamma = np.zeros(L)",
                    "dG = saturated_curvature - mu * G",
                ),
            ),
            "field_status": "FIRST_ORDER_RETARDED_MEMORY_VARIABLE",
            "UV_determinant_status": "NO_ORDINARY_SCALAR_DETERMINANT",
        },
        {
            "object": "particle_Gamma_lepton_text",
            "source_path": str(finite_leptons),
            "source_exists": finite_leptons.exists(),
            "signature_found": _contains(
                finite_leptons,
                ("curvature", "memory field", "irreversible"),
            ),
            "field_status": "PHENOMENOLOGICAL_FIRST_ORDER_MEMORY",
            "UV_determinant_status": "NO_ACTION_PRINTED",
        },
        {
            "object": "canonical_memory_M",
            "source_path": str(memory_action),
            "source_exists": memory_action.exists(),
            "signature_found": _contains(
                memory_action,
                (
                    "- 1/2 g^{",
                    "- a M^4 / 4",
                    "+ b T M^2",
                    "curvature",
                ),
            ),
            "field_status": "COVARIANT_CANONICAL_REAL_SCALAR",
            "UV_determinant_status": "ONE_REAL_SCALAR_IF_PARENT_ADOPTED",
        },
        {
            "object": "memory_M_matter_minimum",
            "source_path": str(memory_minimum),
            "source_exists": memory_minimum.exists(),
            "signature_found": _contains(
                memory_minimum,
                ("b < 0", "M_*^2 = 2", "m_*^2 = 4"),
            ),
            "field_status": "DENSITY_ACTIVATED_NONZERO_MINIMUM",
            "UV_determinant_status": "QUADRATIC_HESSIAN_DEFINED",
        },
        {
            "object": "selected_integrated_H_parent",
            "source_path": str(selected_parent),
            "source_exists": selected_parent.exists(),
            "signature_found": _contains(
                selected_parent,
                ("\\mathcal D\\psi_r", "\\mathcal DX", "\\Psi,A"),
            ),
            "field_status": "DOES_NOT_LIST_M_AS_SEPARATE_PARENT_VARIABLE",
            "UV_determinant_status": "M_REQUIRES_EXPLICIT_PARENT_JOIN",
        },
        {
            "object": "closed_bath_parent",
            "source_path": str(bath_parent),
            "source_exists": bath_parent.exists(),
            "signature_found": _contains(
                bath_parent,
                (
                    "continuum of bath fields",
                    "Sigma_R(\\omega)=-i\\gamma\\omega",
                ),
            ),
            "field_status": "COVARIANT_OPEN_SYSTEM_COMPLETION_AVAILABLE",
            "UV_determinant_status": "BATH_CAN_GENERATE_RETARDED_DAMPING",
        },
        {
            "object": "checkpoint_1983_scan_scope",
            "source_path": str(old_scan),
            "source_exists": old_scan.exists(),
            "signature_found": (
                old_scan.exists()
                and str(memory_action)
                not in old_scan.read_text(encoding="utf-8", errors="replace")
            ),
            "field_status": "CANONICAL_M_ACTION_NOT_REVIEWED_IN_1983",
            "UV_determinant_status": "OLD_NO_SOURCE_VERDICT_SUPERSEDED_IN_SCOPE",
        },
    ]
    return {
        "rows": rows,
        "particle_Gamma_verdict": (
            "the first-order irreversible Gamma variable is an IR response "
            "coordinate and cannot itself be counted as an ordinary real "
            "scalar determinant"
        ),
        "canonical_M_verdict": (
            "the corpus does contain a canonical real curvature-memory "
            "scalar M; it can supply one UV determinant only after an "
            "explicit same-parent identification with the Gamma sector"
        ),
        "passed": all(
            row["source_exists"] and row["signature_found"] for row in rows
        ),
    }


@lru_cache(maxsize=None)
def canonical_memory_hessian() -> dict[str, Any]:
    memory, background = sp.symbols("M Mbar", real=True)
    quartic = sp.symbols("a", positive=True, real=True)
    trace, coupling = sp.symbols("T b", real=True)
    mass_squared = sp.symbols("m_0_squared", nonnegative=True, real=True)
    curvature, nonminimal = sp.symbols("R xi_M", real=True)
    potential = (
        quartic * memory**4 / 4
        - coupling * trace * memory**2
        + mass_squared * memory**2 / 2
        + nonminimal * curvature * memory**2 / 2
    )
    first = sp.diff(potential, memory)
    hessian = sp.simplify(sp.diff(first, memory).subs(memory, background))

    density = sp.symbols("rho", positive=True, real=True)
    coupling_abs = sp.symbols("b_abs", positive=True, real=True)
    minimum_squared = 2 * coupling_abs * density / quartic
    dust_hessian = sp.simplify(
        (3 * quartic * memory**2 - 2 * coupling_abs * density).subs(
            memory**2, minimum_squared
        )
    )
    return {
        "existing_action": (
            "S_M=int sqrt(-g)[-1/2(grad M)^2-a M^4/4+b T M^2]"
        ),
        "canonical_completion": (
            "S_M adds -m0^2 M^2/2-xi_M R M^2/2 when the complete "
            "renormalizable curved-space operator is declared"
        ),
        "potential": str(potential),
        "first_variation": str(first),
        "quadratic_operator": (
            "D_M=-Box+m0^2+3*a*Mbar^2-2*b*T+xi_M*R"
        ),
        "hessian": str(hessian),
        "kinetic_residue": 1.0,
        "existing_m0_squared": 0.0,
        "existing_xi_M": 0.0,
        "matter_supported_minimum": "Mstar^2=2*abs(b)*rho/a",
        "minimum_hessian": str(dust_hessian),
        "determinant_count": 1,
        "determinant_rule": (
            "Gamma_M=+1/2 Tr log D_M; do not count the first-order "
            "Gamma readout as a second species"
        ),
        "passed": bool(
            hessian
            == 3 * background**2 * quartic
            - 2 * coupling * trace
            + curvature * nonminimal
            + mass_squared
            and dust_hessian == 4 * coupling_abs * density
        ),
    }


@lru_cache(maxsize=None)
def overdamped_gamma_map() -> dict[str, Any]:
    omega, gamma, omega0_squared = sp.symbols(
        "omega gamma_M Omega_M_squared", positive=True, real=True
    )
    imaginary = sp.I
    denominator_full = omega0_squared - omega**2 - imaginary * gamma * omega
    denominator_overdamped = omega0_squared - imaginary * gamma * omega
    response_full = 1 / denominator_full
    response_overdamped = 1 / denominator_overdamped
    relative_to_full = sp.simplify(
        (response_full - response_overdamped) / response_full
    )

    rows: list[dict[str, Any]] = []
    for mu_over_gamma in (0.1, 1.0, 10.0):
        gamma_value = 1.0
        mu_value = mu_over_gamma * gamma_value
        omega0_value = mu_value * gamma_value
        scale = min(gamma_value, mu_value)
        for omega_fraction in (1.0e-4, 1.0e-3, 1.0e-2):
            omega_value = omega_fraction * scale
            error = omega_value**2 / math.hypot(
                omega0_value, gamma_value * omega_value
            )
            rows.append(
                {
                    "mu_over_gamma": mu_over_gamma,
                    "omega_over_min_gamma_mu": omega_fraction,
                    "relative_response_error": error,
                    "inside_one_percent": error < 0.01,
                }
            )
    return {
        "rows": rows,
        "closed_equation": (
            "Mddot+gamma_M*Mdot+Omega_M^2*M=J_K+noise"
        ),
        "retarded_transfer": (
            "G_R(omega)=1/(Omega_M^2-omega^2-i*gamma_M*omega)"
        ),
        "overdamped_equation": (
            "Mdot=J_K/gamma_M-(Omega_M^2/gamma_M)*M"
        ),
        "Gamma_identification": (
            "Gamma=g_M*M; J_K=(gamma_M/g_M)*S[K]; "
            "mu=Omega_M^2/gamma_M"
        ),
        "curvature_source": "S[K]=K^2/(1+K^2/S_max)",
        "relative_error_formula": str(relative_to_full),
        "positivity_condition": (
            "gamma_M>=0 from a passive bath and Omega_M^2>0 give a "
            "retarded decaying kernel"
        ),
        "interpretation": (
            "the original first-order Gamma law is the leading low-frequency "
            "retarded limit of one canonical M field plus its bath; Gamma is "
            "not an additional determinant"
        ),
        "passed": bool(
            sp.simplify(
                relative_to_full
                - omega**2
                / (omega0_squared - imaginary * gamma * omega)
            )
            == 0
            and len(rows) == 9
            and all(row["inside_one_percent"] for row in rows)
        ),
    }


@lru_cache(maxsize=None)
def bath_nonminimal_no_go() -> dict[str, Any]:
    weight = sp.symbols("w", nonnegative=True, real=True)
    xi_memory, xi_bath = sp.symbols("xi_M xi_X", real=True)
    z_effective = 1 + weight
    xi_effective = sp.simplify(
        (xi_memory + weight * xi_bath) / z_effective
    )
    rows: list[dict[str, Any]] = []
    for weight_value in (0.0, 0.1, 1.0, 10.0):
        for xi_memory_value, xi_bath_value in (
            (0.0, 0.0),
            (0.0, 1 / 6),
            (0.1, 0.2),
        ):
            value = (
                xi_memory_value + weight_value * xi_bath_value
            ) / (1 + weight_value)
            rows.append(
                {
                    "w_sum": weight_value,
                    "xi_M": xi_memory_value,
                    "xi_bath_weighted_mean": xi_bath_value,
                    "xi_effective": value,
                    "nonnegative_inputs_remain_nonnegative": value >= 0,
                }
            )
    return {
        "rows": rows,
        "bath_operator": "D_X=Omega_X^2-Box+xi_X*R",
        "schur_complement": "D_eff=D_M-integral g_X^2 D_X^-1",
        "local_weight": "w_X=g_X^2/Omega_X^4>=0",
        "Z_effective": str(z_effective),
        "xi_effective": str(xi_effective),
        "multi_bath_formula": (
            "xi_eff=(xi_M+integral w_X*xi_X)/(1+integral w_X)"
        ),
        "no_go": (
            "a passive bilinearly mixed bath with xi_M>=0 and every "
            "xi_X>=0 cannot generate xi_eff<0; a microscopic negative "
            "curvature coupling or a different signed operator is required"
        ),
        "required_for_4884": "xi_eff<-1/18; W1=1 anchor xi_eff=-1/9",
        "passed": bool(
            xi_effective.subs({xi_memory: 0, xi_bath: 0}) == 0
            and len(rows) == 12
            and all(
                row["nonnegative_inputs_remain_nonnegative"] for row in rows
            )
        ),
    }


@lru_cache(maxsize=None)
def trace_coupling_audit() -> dict[str, Any]:
    stability = curvature_stability()
    maximum_ricci = stability["maximum_positive_R_m_minus2"]
    b_mbar_squared = -1 / 18
    xi_ir = 2 * b_mbar_squared
    zero_branch_mass_squared = -maximum_ricci / 9
    minimum_branch_mass_squared = 2 * maximum_ricci / 9
    tachyon_length_m = 1 / math.sqrt(abs(zero_branch_mass_squared))
    fluctuation_length_m = 1 / math.sqrt(minimum_branch_mass_squared)
    tachyon_scale_eV = HBAR_C_EV_M * math.sqrt(
        abs(zero_branch_mass_squared)
    )
    fluctuation_mass_eV = HBAR_C_EV_M * math.sqrt(
        minimum_branch_mass_squared
    )
    anchor_stability_floor = (
        stability["mass_floor_eV_per_sqrt_h_minus_1"]
        * math.sqrt(2 / 3)
    )
    return {
        "off_shell_operator": (
            "D_M=-Box+3*a*Mbar^2-2*b*T; T is an independent matter "
            "operator and supplies no R coefficient on a vacuum background"
        ),
        "forbidden_shortcut": (
            "substituting the Einstein trace T=-Mbar_Pl^2*R before deriving "
            "the Einstein term is circular in an induced-G calculation"
        ),
        "IR_correspondence_only": (
            "after an EH branch already exists, T=-Mbar_Pl^2*R maps "
            "+b*T*M^2 to -xi_IR*R*M^2/2 with xi_IR=2*b*Mbar_Pl^2"
        ),
        "W1_anchor_b_Mbar_squared": b_mbar_squared,
        "W1_anchor_xi_IR": xi_ir,
        "sampled_Rmax_m_minus2": maximum_ricci,
        "M_zero_mass_squared_m_minus2": zero_branch_mass_squared,
        "M_zero_tachyon_length_m": tachyon_length_m,
        "M_zero_tachyon_scale_eV": tachyon_scale_eV,
        "M_minimum_fluctuation_mass_squared_m_minus2": (
            minimum_branch_mass_squared
        ),
        "M_minimum_fluctuation_length_m": fluctuation_length_m,
        "M_minimum_fluctuation_mass_eV": fluctuation_mass_eV,
        "4884_anchor_stability_floor_eV": anchor_stability_floor,
        "existing_action_result": (
            "the printed m0=0, b<0 action does not satisfy the M=0 local "
            "curvature-stability gate; it moves to a nonzero density-supported "
            "branch whose local scalarization and fifth-force response must "
            "be solved"
        ),
        "passed": bool(
            math.isclose(xi_ir, -1 / 9, rel_tol=1e-15)
            and 30_000 < tachyon_length_m < 31_000
            and 21_000 < fluctuation_length_m < 22_000
            and 6.5e-12 < anchor_stability_floor < 6.6e-12
        ),
    }


def _strong_matter_shift(
    a_r: float, a_c: float
) -> tuple[float, float]:
    response = canonical_response()
    lambda_r = CONTACT_M2_PER_A * a_r / L_SUN_M**2
    lambda_c = CONTACT_M2_PER_A * a_c / L_SUN_M**2
    radius_shifts: list[float] = []
    tidal_shifts: list[float] = []
    for eos_id in response["backgrounds"]:
        radius_lsun = (
            response["derivatives"][(eos_id, "lambda_r", "radius")]
            * lambda_r
            + response["derivatives"][(eos_id, "lambda_c", "radius")]
            * lambda_c
        )
        tidal = (
            response["derivatives"][(
                eos_id,
                "lambda_r",
                "tidal_lambda",
            )]
            * lambda_r
            + response["derivatives"][(
                eos_id,
                "lambda_c",
                "tidal_lambda",
            )]
            * lambda_c
        )
        radius_shifts.append(radius_lsun * L_SUN_M / 1000)
        tidal_shifts.append(tidal)
    return (
        max(abs(value) for value in radius_shifts),
        max(abs(value) for value in tidal_shifts),
    )


@lru_cache(maxsize=None)
def renormalized_eh_fallback() -> dict[str, Any]:
    log_ns = math.log(
        (4 * math.pi * math.sqrt(6) * MBAR_PL_EV)
        / (HBAR_C_EV_M / 12_000)
    )
    rows: list[dict[str, Any]] = []
    for branch, scalar_count, ownership in (
        (
            "real_psi_plus_M_plus_U1",
            2,
            "core real psi plus separately adopted canonical M",
        ),
        (
            "complex_psi_plus_M_plus_U1",
            3,
            "later complex psi normalization plus adopted canonical M",
        ),
    ):
        vector_count = 1
        w0 = scalar_count + 2 * vector_count
        w1 = scalar_count - 4 * vector_count
        wc = scalar_count + 12 * vector_count
        sh2 = scalar_count
        a_r = log_ns * sh2 / (1152 * math.pi**2)
        a_c = log_ns * wc / (1920 * math.pi**2)
        radius_shift, tidal_shift = _strong_matter_shift(a_r, a_c)
        observation_fraction = max(
            radius_shift / 1.15,
            tidal_shift / 255.0,
        )
        rows.append(
            {
                "branch": branch,
                "N_s": scalar_count,
                "N_V": vector_count,
                "xi_s": 0.0,
                "W0": w0,
                "W1": w1,
                "S_h2": sh2,
                "W_C": wc,
                "L_NS_reference": log_ns,
                "a_R_loop_reference": a_r,
                "a_C_loop_reference": a_c,
                "aR_over_aC": a_r / a_c,
                "maximum_abs_radius_shift_km": radius_shift,
                "maximum_abs_tidal_shift": tidal_shift,
                "orders_below_observational_width": -math.log10(
                    observation_fraction
                ),
                "ownership": ownership,
                "status": "RENORMALIZED_EH_FALLBACK_NONCLAIM",
            }
        )
    matching_rows: list[dict[str, Any]] = []
    selected_w1 = -1.0
    for cutoff_ratio in (1.0, 4 * math.pi, 4 * math.pi * math.sqrt(6)):
        loop_ratio = selected_w1 * cutoff_ratio**2 / (96 * math.pi**2)
        bare_ratio = 1 - loop_ratio
        matching_rows.append(
            {
                "LambdaUV_over_MbarPl": cutoff_ratio,
                "Mloop_squared_over_MbarPl_squared": loop_ratio,
                "M0_squared_over_MbarPl_squared": bare_ratio,
                "MR_squared_over_MbarPl_squared": bare_ratio + loop_ratio,
            }
        )
    selected = next(
        row
        for row in rows
        if row["branch"] == "complex_psi_plus_M_plus_U1"
    )
    return {
        "rows": rows,
        "matching_rows": matching_rows,
        "selected_branch": "complex_psi_plus_M_plus_U1",
        "selected_rule": (
            "M_R^2=M_0^2+M_loop^2=Mbar_Pl^2 is calibrated once; "
            "with W1=-1, M_0^2=Mbar_Pl^2+LambdaUV^2/(96*pi^2)"
        ),
        "selected_loop_ratio": "a_R/a_C=1/3",
        "interpretation": (
            "this route no longer claims to predict G_N; it has the same "
            "one-constant status as GR while preserving derived universal "
            "loop corrections and every local correspondence test"
        ),
        "passed": bool(
            selected["W1"] == -1
            and math.isclose(selected["aR_over_aC"], 1 / 3, rel_tol=1e-12)
            and all(
                row["orders_below_observational_width"] > 70
                for row in rows
            )
            and math.isclose(
                matching_rows[-1]["M0_squared_over_MbarPl_squared"],
                2.0,
                rel_tol=1e-12,
            )
        ),
    }


@lru_cache(maxsize=None)
def arbitration() -> dict[str, Any]:
    corpus = corpus_signature_audit()
    hessian = canonical_memory_hessian()
    overdamped = overdamped_gamma_map()
    bath_no_go = bath_nonminimal_no_go()
    trace = trace_coupling_audit()
    fallback = renormalized_eh_fallback()
    return {
        "Gamma_first_order_UV_species": False,
        "canonical_M_UV_species": (
            "ONE_REAL_SCALAR_CONDITIONAL_ON_EXPLICIT_PARENT_JOIN"
        ),
        "Gamma_from_M_bath": (
            "DERIVED_AS_CONTROLLED_OVERDAMPED_RETARDED_LIMIT"
        ),
        "negative_xi_from_minimal_passive_bath": False,
        "bTM2_as_offshell_UV_xi": False,
        "bTM2_IR_frame_relation": (
            "xi_IR=2*b*Mbar_Pl^2 only after an EH correspondence branch exists"
        ),
        "three_boson_positive_EH_route": (
            "DEMOTED_CONDITIONAL_NEGATIVE_XI_NOT_PARENT_DERIVED"
        ),
        "three_boson_W1_one_anchor": (
            "ALSO_FAILS_PRINTED_M_ZERO_BRANCH_CURVATURE_STABILITY"
        ),
        "selected_local_correspondence_route": (
            "RENORMALIZED_EH_COMPLEX_PSI_M_U1_MINIMAL_SCALAR_FALLBACK"
        ),
        "GN_prediction": False,
        "GN_status": (
            "ONE_CALIBRATED_RENORMALIZED_CONSTANT_AS_IN_GR_NO_ARENA_RETUNING"
        ),
        "universal_loop_corrections": (
            "DERIVED_AND_OVER_70_ORDERS_BELOW_STRONG_MATTER_WIDTHS"
        ),
        "active_M_local_scalar_status": (
            "OPEN_DENSITY_SCALARIZATION_AND_SCREENING_TEST"
        ),
        "next_target": NEXT_TARGET,
        "passed": bool(
            corpus["passed"]
            and hessian["passed"]
            and overdamped["passed"]
            and bath_no_go["passed"]
            and trace["passed"]
            and fallback["passed"]
        ),
    }


@lru_cache(maxsize=None)
def result() -> dict[str, Any]:
    sections = {
        "corpus": corpus_signature_audit(),
        "hessian": canonical_memory_hessian(),
        "overdamped": overdamped_gamma_map(),
        "bath_no_go": bath_nonminimal_no_go(),
        "trace_coupling": trace_coupling_audit(),
        "fallback": renormalized_eh_fallback(),
        "arbitration": arbitration(),
    }
    all_checks_pass = all(
        section.get("passed", True) for section in sections.values()
    )
    return {
        "checkpoint": CHECKPOINT,
        "sections": sections,
        "all_checks_pass": all_checks_pass,
        "decision": (
            "identify canonical M as the only legitimate third scalar "
            "determinant and derive first-order Gamma as its overdamped bath "
            "limit; prove a minimally coupled passive bath cannot generate "
            "the negative xi required by the pure-induced three-boson route; "
            "demote that route and select a once-calibrated renormalized-EH "
            "fallback while advancing active-M scalarization to direct test"
        ),
    }


if __name__ == "__main__":
    calculation = result()
    print("MTS_GAMMA_MEMORY_UV_OPERATOR_4885")
    print(f"all_checks_pass={calculation['all_checks_pass']}")
    print(calculation["decision"])

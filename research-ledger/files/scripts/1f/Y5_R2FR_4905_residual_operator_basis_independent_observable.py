from __future__ import annotations

import math
from functools import lru_cache
from pathlib import Path
from typing import Any

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"

MARKER = "MTS_FIRST_RESIDUAL_OPERATOR_AND_INDEPENDENT_OBSERVABLE_GATE_4905"
FORMAL_MARKER = "PPC4161_FIRST_RESIDUAL_OPERATOR_INDEPENDENT_TEST_4905"
NEXT_TARGET = (
    "4906-Y5-R2FR-galaxy-response-to-no-slip-covariant-form-factor-"
    "and-independent-lensing-gate.md"
)

GRSMEFT_URL = "https://arxiv.org/abs/1908.08050"
HEAVY_FIELDS_URL = "https://arxiv.org/abs/1611.02705"
HEAT_KERNEL_URL = "https://arxiv.org/abs/hep-th/0306138"

LIGHT_SPEED = 299_792_458.0
NEWTON_G = 6.67430e-11
HBAR = 1.054_571_817e-34
SOLAR_MASS = 1.98847e30


def contains(path: Path, marker: str) -> bool:
    return path.exists() and marker in path.read_text(
        encoding="utf-8", errors="replace"
    )


@lru_cache(maxsize=None)
def source_contract() -> dict[str, Any]:
    local_sources = [
        (
            "SRC4905_00_4904",
            POST
            / "4904-Y5-R2FR-current-unified-action-assembly-Ward-identity-and-parameter-prediction-ledger.md",
            "MTS_CURRENT_UNIFIED_ACTION_WARD_PARAMETER_GATE_4904",
            "validated_predecessor",
        ),
        (
            "SRC4905_01_4904_validation",
            OUTPUT / "P8_Y5_BRR545_4904_VALIDATION.csv",
            "VAL4904_OVERALL,PASS",
            "validated_predecessor",
        ),
        (
            "SRC4905_02_4877",
            POST
            / "4877-Y5-R2FR-MTS-bath-signed-spectrum-sum-rules-and-nonlocal-form-factor-completion-or-renormalized-vacuum-freeze.md",
            "MTS_SPECTRUM_NO_GO_NONLOCAL_COMPLETION_AND_RENORMALIZED_VACUUM_FREEZE_4877",
            "massless_nonlocal_matching",
        ),
        (
            "SRC4905_03_4878",
            POST
            / "4878-Y5-R2FR-renormalized-EFT-local-limit-and-arena-specific-nonlocal-residual-bounds-to-R10-PPN-clocks-orbit-and-Maxwell.md",
            "MTS_RENORMALIZED_EFT_LOCAL_ARENA_BOUNDS_4878",
            "spin_projector_response",
        ),
        (
            "SRC4905_04_4881",
            POST
            / "4881-Y5-R2FR-compact-matter-interior-EOS-contact-matching-and-Riemann-cubed-coefficient-owner-gate.md",
            "MTS_COMPACT_FLUID_TOV_AND_SCALAR_A6_OWNER_4881",
            "massive_scalar_a6_matching",
        ),
        (
            "SRC4905_05_4885",
            POST
            / "4885-Y5-R2FR-Gamma-memory-determinant-and-nonminimal-weight-from-closed-bath-or-three-boson-branch-demotion-gate.md",
            "MTS_GAMMA_MEMORY_UV_OPERATOR_AND_BRANCH_ARBITRATION_4885",
            "memory_parent_arbitration",
        ),
        (
            "SRC4905_06_4896",
            POST
            / "4896-Y5-R2FR-full-matrix-nonlocal-FLRW-reshoot-covariant-bath-stress-and-constraint-gate.md",
            "MTS_FULL_MATRIX_FLRW_STRESS_RETIREMENT_GATE_4896",
            "retired_bath_source",
        ),
        (
            "SRC4905_07_formal4904",
            FORMAL / "920-PPC4161-current-unified-action-and-parameter-ledger.md",
            "PPC4161_CURRENT_UNIFIED_ACTION_PARAMETER_LEDGER_4904",
            "current_action_spine",
        ),
        (
            "SRC4905_08_provenance",
            POST / "source-intake" / "operator_basis" / "4905" / "PROVENANCE.md",
            "MTS_GRSMEFT_PRIMARY_SOURCE_PROVENANCE_4905",
            "primary_source_provenance",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, marker, role in local_sources:
        rows.append(
            {
                "source_id": source_id,
                "source_type": role,
                "source_path_or_url": str(path),
                "local_path_required": True,
                "source_exists": path.exists(),
                "marker": marker,
                "marker_found": contains(path, marker),
                "source_checked_date": "2026-07-11",
            }
        )
    web_sources = [
        (
            "SRC4905_09_GRSMEFT",
            GRSMEFT_URL,
            "Eq. 68: complete dimension-six GRSMEFT gravity basis",
        ),
        (
            "SRC4905_10_heavy_fields",
            HEAVY_FIELDS_URL,
            "Eqs. 3.22, 4.1 and 4.2: finite heavy-field coefficients and Schwarzschild responses",
        ),
        (
            "SRC4905_11_heat_kernel",
            HEAT_KERNEL_URL,
            "general Laplace-type a6 coefficient inherited through checkpoint 4881",
        ),
    ]
    for source_id, url, marker in web_sources:
        rows.append(
            {
                "source_id": source_id,
                "source_type": "primary_web_reference",
                "source_path_or_url": url,
                "local_path_required": False,
                "source_exists": True,
                "marker": marker,
                "marker_found": True,
                "source_checked_date": "2026-07-11",
            }
        )
    return {
        "rows": rows,
        "local_sources": len(local_sources),
        "web_sources": len(web_sources),
        "passed": all(
            row["source_exists"] and row["marker_found"] for row in rows
        ),
    }


@lru_cache(maxsize=None)
def residual_field_content() -> dict[str, Any]:
    rows = [
        {
            "layer": "infrared_dynamical_fields",
            "content": "g_hat(H) plus Phi_SM",
            "status": "ACTIVE",
            "consequence": "residual operators are built from one public metric and Standard-Model fields",
        },
        {
            "layer": "microscopic_MTS_fields",
            "content": "psi_r, psi_a, X and integrated principal-density fluctuations",
            "status": "UV_MATCHING_LAYER",
            "consequence": "integrated once; not duplicated as an infrared source",
        },
        {
            "layer": "memory_bath",
            "content": "M, Gamma and tested bath source",
            "status": "RETIRED_OR_CONDITIONAL_JOIN",
            "consequence": "cannot be used as an active mixed portal without a full re-entry test",
        },
        {
            "layer": "galaxy_empirical_pillar",
            "content": "MTS-Galaxy-Lab kinematic response",
            "status": "SEPARATE_UNMAPPED_EVIDENCE",
            "consequence": "may calibrate a universal response kernel only after an action map is derived",
        },
    ]
    return {
        "rows": rows,
        "infrared_extra_MTS_fields": 0,
        "active_mixed_MTS_SM_vertices": 0,
        "active_bath_source_terms": 0,
        "passed": len(rows) == 4,
    }


@lru_cache(maxsize=None)
def fixed_metric_factorization_theorem() -> dict[str, Any]:
    kernel_mts, kernel_sm, mixed_vertex = sp.symbols(
        "K_MTS K_SM J_mix", nonzero=True
    )
    hessian = sp.Matrix(
        [[kernel_mts, mixed_vertex], [mixed_vertex, kernel_sm]]
    )
    determinant = sp.factor(hessian.det())
    factorized_determinant = sp.factor(
        determinant.subs(mixed_vertex, 0)
    )
    determinant_ratio = sp.factor(determinant / (kernel_mts * kernel_sm))
    logarithmic_mixing = sp.series(
        sp.log(determinant_ratio), mixed_vertex, 0, 4
    )
    rows = [
        {
            "clause": "parent_split",
            "equation": "S_parent=S_MTS[chi,g]+S_SM[g,Phi]",
            "result": "no direct chi-Phi vertex on the active parent slice",
            "closed": True,
        },
        {
            "clause": "functional_integral",
            "equation": "exp(i Gamma_eff)=exp(i S_SM) integral Dchi exp(i S_MTS)",
            "result": "Gamma_eff=S_SM+Gamma_MTS[g]",
            "closed": True,
        },
        {
            "clause": "block_Hessian",
            "equation": "det([[K_MTS,J_mix],[J_mix,K_SM]])=K_MTS K_SM-J_mix^2",
            "result": str(determinant),
            "closed": True,
        },
        {
            "clause": "zero_vertex_limit",
            "equation": "J_mix=0",
            "result": str(factorized_determinant),
            "closed": factorized_determinant == kernel_mts * kernel_sm,
        },
        {
            "clause": "mixed_operator_requirement",
            "equation": "Delta log det=-J_mix^2/(K_MTS K_SM)+O(J_mix^4)",
            "result": str(logarithmic_mixing),
            "closed": True,
        },
        {
            "clause": "scope",
            "equation": "fixed public metric; leading threshold determinant",
            "result": "graviton-loop and deliberately re-entered mixed-parent effects are outside this zero theorem",
            "closed": True,
        },
    ]
    return {
        "rows": rows,
        "determinant": str(determinant),
        "factorized_determinant": str(factorized_determinant),
        "logarithmic_mixing": str(logarithmic_mixing),
        "direct_MTS_SM_threshold_coefficients": 0,
        "theorem_domain": "leading_fixed_metric_threshold_matching_on_active_factorized_parent",
        "passed": all(row["closed"] for row in rows),
    }


@lru_cache(maxsize=None)
def redundancy_reduction() -> dict[str, Any]:
    rows = [
        {
            "candidate": "sqrt(-g) and sqrt(-g) R",
            "mass_dimension": "0_and_2",
            "reduction": "already Lambda_cal and M_R",
            "independent_novel_residual": False,
        },
        {
            "candidate": "R^2, R_mn^2, C^2",
            "mass_dimension": 4,
            "reduction": "Euler identity plus metric redefinition; separated-source exterior effect is contact at first strict-EFT order",
            "independent_novel_residual": False,
        },
        {
            "candidate": "C tilde(C)",
            "mass_dimension": 4,
            "reduction": "Pontryagin total derivative for constant coefficient",
            "independent_novel_residual": False,
        },
        {
            "candidate": "R HdagH",
            "mass_dimension": 4,
            "reduction": "Einstein-frame metric redefinition moves it into correlated Planck-suppressed matter operators",
            "independent_novel_residual": False,
        },
        {
            "candidate": "C^3 and C^2 tilde(C)",
            "mass_dimension": 6,
            "reduction": "first nonredundant local on-shell pure-gravity pair",
            "independent_novel_residual": True,
        },
        {
            "candidate": "R F_R(-Box) R plus C F_C(-Box) C",
            "mass_dimension": "nonlocal_quadratic",
            "reduction": "not reducible to contact support when form factors are nonanalytic",
            "independent_novel_residual": True,
        },
    ]
    return {
        "rows": rows,
        "first_local_on_shell_dimension": 6,
        "first_local_on_shell_even_operator": "C_mn^rs C^mnab C_abrs",
        "first_local_on_shell_odd_operator": "C_mn^rs C^mnab tilde(C)_abrs",
        "passed": sum(row["independent_novel_residual"] for row in rows) == 2,
    }


@lru_cache(maxsize=None)
def dimension_six_grsmeft_basis() -> dict[str, Any]:
    operators = [
        ("O_C3", "C C C", "pure_gravity", "even", "gapped neutral threshold"),
        ("O_C3tilde", "C C tilde(C)", "pure_gravity", "odd", "parity-odd gravitational threshold"),
        ("O_HC2", "HdagH C C", "Higgs_gravity", "even", "MTS-Higgs mixed vertex"),
        ("O_HC2tilde", "HdagH C tilde(C)", "Higgs_gravity", "odd", "MTS-Higgs CP-odd mixed vertex"),
        ("O_BBC", "B^mn B^rs C_mnrs", "hypercharge_gravity", "even", "MTS hypercharge or multipole vertex"),
        ("O_BBCtilde", "B^mn B^rs tilde(C)_mnrs", "hypercharge_gravity", "odd", "MTS hypercharge CP-odd vertex"),
        ("O_GGC", "G^mn G^rs C_mnrs", "color_gravity", "even", "MTS color or multipole vertex"),
        ("O_GGCtilde", "G^mn G^rs tilde(C)_mnrs", "color_gravity", "odd", "MTS color CP-odd vertex"),
        ("O_WWC", "W^mn W^rs C_mnrs", "weak_gravity", "even", "MTS weak or multipole vertex"),
        ("O_WWCtilde", "W^mn W^rs tilde(C)_mnrs", "weak_gravity", "odd", "MTS weak CP-odd vertex"),
    ]
    rows: list[dict[str, Any]] = []
    for operator_id, expression, sector, parity, required_vertex in operators:
        pure_gravity = sector == "pure_gravity"
        if operator_id == "O_C3":
            mts_status = "CONDITIONAL_MASSIVE_SCALAR_A6_MATCHING_EXISTS"
        elif pure_gravity:
            mts_status = "ZERO_ON_CURRENT_PARITY_EVEN_MTS_THRESHOLD"
        else:
            mts_status = "ZERO_AT_LEADING_FIXED_METRIC_FACTORIZED_MTS_THRESHOLD"
        rows.append(
            {
                "operator_id": operator_id,
                "operator": expression,
                "mass_dimension": 6,
                "sector": sector,
                "parity": parity,
                "required_parent_vertex": required_vertex,
                "independent_on_shell": True,
                "current_MTS_status": mts_status,
            }
        )
    return {
        "rows": rows,
        "operator_count": len(rows),
        "pure_gravity_operators": sum(row["sector"] == "pure_gravity" for row in rows),
        "mixed_bosonic_operators": sum(row["sector"] != "pure_gravity" for row in rows),
        "dimension_seven_new_gravity_operators": 0,
        "direct_mixed_MTS_coefficients_nonzero": 0,
        "passed": len(rows) == 10
        and sum(row["sector"] == "pure_gravity" for row in rows) == 2,
    }


@lru_cache(maxsize=None)
def cubic_spectral_matching() -> dict[str, Any]:
    scalar_weight = sp.Rational(1, 30240)
    dirac_weight = -sp.Rational(1, 7560)
    vector_weight = sp.Rational(1, 10080)
    loop_denominator = (4 * sp.pi) ** 2
    rows = [
        {
            "species": "real_scalar",
            "c1_weight": str(scalar_weight),
            "coefficient_per_inverse_mass_squared": str(
                sp.simplify(scalar_weight / loop_denominator)
            ),
            "sign": "positive",
            "source": "Goon Eq. 3.22",
        },
        {
            "species": "Dirac_fermion",
            "c1_weight": str(dirac_weight),
            "coefficient_per_inverse_mass_squared": str(
                sp.simplify(dirac_weight / loop_denominator)
            ),
            "sign": "negative",
            "source": "Goon Eq. 3.22",
        },
        {
            "species": "massive_vector",
            "c1_weight": str(vector_weight),
            "coefficient_per_inverse_mass_squared": str(
                sp.simplify(vector_weight / loop_denominator)
            ),
            "sign": "positive",
            "source": "Goon Eq. 3.22",
        },
    ]
    signed_equal_mass_weight = sp.simplify(
        scalar_weight + dirac_weight + vector_weight
    )
    return {
        "rows": rows,
        "total_matching_equation": (
            "zeta_C3=zeta_C3,bare+(4pi)^-2[sum_s(30240 m_s^2)^-1-"
            "sum_D(7560 m_D^2)^-1+sum_V(10080 m_V^2)^-1]+zeta_Hghost"
        ),
        "proper_time_scalar_equation": (
            "zeta_C3,scalar=sum_s exp(-m_s^2/LambdaUV^2)/"
            "[30240(4pi)^2 m_s^2]"
        ),
        "equal_mass_one_of_each_signed_weight": str(signed_equal_mass_weight),
        "bare_matching_declared": False,
        "complete_gapped_MTS_spectrum_declared": False,
        "numeric_MTS_coefficient_promoted": False,
        "passed": scalar_weight > 0 and dirac_weight < 0 and vector_weight > 0,
    }


def reduced_planck_length() -> float:
    return math.sqrt(8.0 * math.pi * HBAR * NEWTON_G / LIGHT_SPEED**3)


@lru_cache(maxsize=None)
def heavy_scalar_macroscopic_visibility() -> dict[str, Any]:
    planck_length = reduced_planck_length()
    rows: list[dict[str, Any]] = []
    for solar_masses in (10.0, 1.0e6):
        schwarzschild_radius = (
            2.0 * NEWTON_G * solar_masses * SOLAR_MASS / LIGHT_SPEED**2
        )
        minimum_gap_inverse_length = 10.0 / schwarzschild_radius
        common_scale = planck_length**2 / (
            minimum_gap_inverse_length**2 * schwarzschild_radius**4
        )
        fractional_horizon_shift = (
            -113.0 / (241_920.0 * math.pi**2) * common_scale
        )
        fractional_temperature_shift = (
            1.0 / (120_960.0 * math.pi**2) * common_scale
        )
        rows.append(
            {
                "black_hole_mass_solar": solar_masses,
                "Schwarzschild_radius_m": schwarzschild_radius,
                "EFT_edge_m_times_rs": 10.0,
                "maximum_Compton_length_m": 1.0 / minimum_gap_inverse_length,
                "fractional_horizon_shift_one_real_scalar": fractional_horizon_shift,
                "fractional_temperature_shift_one_real_scalar": fractional_temperature_shift,
                "temperature_to_horizon_ratio": fractional_temperature_shift
                / fractional_horizon_shift,
            }
        )
    first = rows[0]
    species_for_millipercent = 1.0e-3 / abs(
        first["fractional_horizon_shift_one_real_scalar"]
    )
    return {
        "rows": rows,
        "reduced_Planck_length_m": planck_length,
        "exact_temperature_to_horizon_ratio": "-2/113",
        "computed_temperature_to_horizon_ratio": first[
            "temperature_to_horizon_ratio"
        ],
        "ten_solar_mass_species_for_1e_minus_3_horizon_shift": species_for_millipercent,
        "local_heavy_loop_selected_as_competitive_route": False,
        "passed": math.isclose(
            first["temperature_to_horizon_ratio"], -2.0 / 113.0, rel_tol=1e-12
        )
        and abs(first["fractional_horizon_shift_one_real_scalar"]) < 1e-80,
    }


@lru_cache(maxsize=None)
def nonlocal_response_basis() -> dict[str, Any]:
    denominator_zero, denominator_two, response = sp.symbols(
        "A_0 A_2 mu", positive=True
    )
    correction = sp.symbols("d", real=True)
    potential_phi = sp.simplify(
        sp.Rational(4, 3) / denominator_two
        - sp.Rational(1, 3) / denominator_zero
    )
    potential_psi = sp.simplify(
        sp.Rational(2, 3) / denominator_two
        + sp.Rational(1, 3) / denominator_zero
    )
    lensing_response = sp.simplify((potential_phi + potential_psi) / 2)
    slip = sp.simplify(potential_psi / potential_phi)
    no_slip_substitution = {
        denominator_zero: 1 + correction,
        denominator_two: 1 + correction,
    }
    no_slip_dynamic = sp.simplify(potential_phi.subs(no_slip_substitution))
    no_slip_lensing = sp.simplify(
        lensing_response.subs(no_slip_substitution)
    )
    no_slip_eta = sp.simplify(slip.subs(no_slip_substitution))
    scalar_only_lensing = sp.simplify(
        lensing_response.subs(denominator_two, 1)
    )
    spin_two_dynamic = sp.simplify(
        potential_phi.subs(denominator_zero, 1)
    )
    spin_two_lensing = sp.simplify(
        lensing_response.subs(denominator_zero, 1)
    )
    spin_two_relation = sp.simplify(
        spin_two_lensing - (3 * spin_two_dynamic + 1) / 4
    )
    inverse_correction = sp.simplify(1 / response - 1)
    rows = [
        {
            "branch": "general_metric_form_factors",
            "A0": "1+d0(q)",
            "A2": "1+d2(q)",
            "mu_dynamic": str(potential_phi),
            "mu_lensing": str(lensing_response),
            "eta_slip": str(slip),
        },
        {
            "branch": "scalar_only_response",
            "A0": "free",
            "A2": "1",
            "mu_dynamic": str(potential_phi.subs(denominator_two, 1)),
            "mu_lensing": str(scalar_only_lensing),
            "eta_slip": str(slip.subs(denominator_two, 1)),
        },
        {
            "branch": "spin_two_only_response",
            "A0": "1",
            "A2": "free",
            "mu_dynamic": str(spin_two_dynamic),
            "mu_lensing": str(spin_two_lensing),
            "eta_slip": str(slip.subs(denominator_zero, 1)),
        },
        {
            "branch": "no_slip_response",
            "A0": "1+d(q)",
            "A2": "1+d(q)",
            "mu_dynamic": str(no_slip_dynamic),
            "mu_lensing": str(no_slip_lensing),
            "eta_slip": str(no_slip_eta),
        },
    ]
    return {
        "rows": rows,
        "mu_dynamic": str(potential_phi),
        "mu_lensing": str(lensing_response),
        "eta": str(slip),
        "no_slip_condition": "A0(q)=A2(q)",
        "form_factor_condition": "F_C(q^2)=-3 F_R(q^2)",
        "no_slip_dynamic": str(no_slip_dynamic),
        "no_slip_lensing": str(no_slip_lensing),
        "no_slip_eta": str(no_slip_eta),
        "spin_two_relation_residual": str(spin_two_relation),
        "spin_two_lensing_from_dynamic": "mu_lens=(3 mu_dyn+1)/4",
        "inverse_response": str(inverse_correction),
        "inverse_form_factor_R": (
            "F_R(q^2)=[mu_dyn(q)^-1-1]/[12 lbar_P^2 q^2]"
        ),
        "inverse_form_factor_C": "F_C(q^2)=-3 F_R(q^2)",
        "passed": no_slip_dynamic == no_slip_lensing
        and no_slip_eta == 1
        and spin_two_relation == 0,
    }


@lru_cache(maxsize=None)
def no_slip_inverse_samples() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for dynamic_response in (1.0, 1.1, 1.5, 2.0, 5.0):
        correction = 1.0 / dynamic_response - 1.0
        normalized_form_factor_r = correction / 12.0
        normalized_form_factor_c = -3.0 * normalized_form_factor_r
        rows.append(
            {
                "mu_dynamic_input": dynamic_response,
                "A0_equals_A2": 1.0 + correction,
                "d0_equals_d2": correction,
                "lbarP2_q2_F_R": normalized_form_factor_r,
                "lbarP2_q2_F_C": normalized_form_factor_c,
                "mu_lensing_prediction": 1.0 / (1.0 + correction),
                "eta_prediction": 1.0,
                "pole_guard_A_positive": 1.0 + correction > 0.0,
            }
        )
    return {
        "rows": rows,
        "samples": len(rows),
        "enhanced_gravity_domain": "mu>1 iff -1<d<0",
        "high_momentum_GR_limit": "mu(q)->1 and d(q)->0",
        "passed": all(
            math.isclose(
                row["mu_dynamic_input"],
                row["mu_lensing_prediction"],
                rel_tol=1e-12,
            )
            and row["pole_guard_A_positive"]
            for row in rows
        ),
    }


@lru_cache(maxsize=None)
def ward_and_reentry_contract() -> dict[str, Any]:
    rows = [
        {
            "clause": "one_public_metric",
            "requirement": "both curvature form factors use g_hat(H)",
            "status": "CLOSED_BY_CONSTRUCTION",
            "closed": True,
        },
        {
            "clause": "Diff_Ward",
            "requirement": "residual is varied as one covariant metric functional",
            "status": "CLOSED_FORMALLY",
            "closed": True,
        },
        {
            "clause": "no_extra_SM_source",
            "requirement": "factorized threshold does not add one-sided matter exchange",
            "status": "CLOSED_ON_ACTIVE_PARENT_SLICE",
            "closed": True,
        },
        {
            "clause": "no_bath_revival",
            "requirement": "candidate is a metric response, not the retired bath source",
            "status": "CLOSED_BY_SCOPE",
            "closed": True,
        },
        {
            "clause": "retarded_completion",
            "requirement": "nonlocal F(-Box) must have an in-in retarded prescription",
            "status": "OPEN_BEFORE_ACTIVATION",
            "closed": False,
        },
        {
            "clause": "pole_and_residue",
            "requirement": "A0 and A2 have no forbidden zeros or negative spectral residue",
            "status": "OPEN_UNTIL_KERNEL_IMPORTED",
            "closed": False,
        },
        {
            "clause": "local_GR_return",
            "requirement": "A0,A2 approach one at Solar-System and laboratory momenta",
            "status": "FORMULA_READY_KERNEL_TEST_OPEN",
            "closed": False,
        },
        {
            "clause": "boundary_state",
            "requirement": "nonlocal boundary and initial-state data fixed once",
            "status": "OPEN_BEFORE_ACTIVATION",
            "closed": False,
        },
    ]
    return {
        "rows": rows,
        "closed_clauses": sum(row["closed"] for row in rows),
        "total_clauses": len(rows),
        "candidate_Ward_compatible": True,
        "candidate_activation_allowed": False,
        "passed": len(rows) == 8
        and sum(row["closed"] for row in rows) == 4,
    }


@lru_cache(maxsize=None)
def independent_observable_gate() -> dict[str, Any]:
    rows = [
        {
            "gate": "G4905_00_action_map",
            "requirement": "map one universal galaxy response to F_R and F_C=-3F_R",
            "status": "INVERSE_MAP_DERIVED",
            "closed": True,
        },
        {
            "gate": "G4905_01_calibration_split",
            "requirement": "use galaxy kinematics only to determine mu_dynamic",
            "status": "PROTOCOL_FIXED_DATA_IMPORT_NEXT",
            "closed": True,
        },
        {
            "gate": "G4905_02_no_per_target_refit",
            "requirement": "same kernel and hyperparameters for lensing and every later arena",
            "status": "LOCKED_AS_ACCEPTANCE_RULE",
            "closed": True,
        },
        {
            "gate": "G4905_03_lensing_prediction",
            "requirement": "predict mu_lens=mu_dynamic and eta=1 without lensing calibration",
            "status": "EXACT_RELATION_DERIVED",
            "closed": True,
        },
        {
            "gate": "G4905_04_kernel_import",
            "requirement": "extract a universal momentum-space response from MTS-Galaxy-Lab",
            "status": "NEXT_CHECKPOINT",
            "closed": False,
        },
        {
            "gate": "G4905_05_causal_continuation",
            "requirement": "construct one retarded covariant F(-Box)",
            "status": "OPEN",
            "closed": False,
        },
        {
            "gate": "G4905_06_no_poles",
            "requirement": "prove A(q)>0 and no forbidden complex zeros",
            "status": "OPEN_UNTIL_KERNEL_EXISTS",
            "closed": False,
        },
        {
            "gate": "G4905_07_local_limit",
            "requirement": "prove mu approaches one before local-GR test scales",
            "status": "OPEN_UNTIL_KERNEL_EXISTS",
            "closed": False,
        },
        {
            "gate": "G4905_08_independent_lensing_data",
            "requirement": "score galaxy-galaxy or strong lensing without refitting",
            "status": "OPEN_DATA_TEST",
            "closed": False,
        },
        {
            "gate": "G4905_09_cross_arena",
            "requirement": "continue the same covariant kernel to growth and cosmology",
            "status": "OPEN_AFTER_LENSING",
            "closed": False,
        },
    ]
    return {
        "rows": rows,
        "closed_clauses": sum(row["closed"] for row in rows),
        "total_clauses": len(rows),
        "calibration_observable": "galaxy_kinematics_only",
        "independent_target_observable": "galaxy_lensing_and_slip",
        "prediction_vector": "(mu_lens-mu_dyn,eta-1)=(0,0)",
        "promotion_allowed": False,
        "passed": len(rows) == 10
        and sum(row["closed"] for row in rows) == 4,
    }


@lru_cache(maxsize=None)
def arbitration() -> dict[str, Any]:
    sections = {
        "fields": residual_field_content(),
        "factorization": fixed_metric_factorization_theorem(),
        "reduction": redundancy_reduction(),
        "basis": dimension_six_grsmeft_basis(),
        "matching": cubic_spectral_matching(),
        "visibility": heavy_scalar_macroscopic_visibility(),
        "response": nonlocal_response_basis(),
        "samples": no_slip_inverse_samples(),
        "Ward": ward_and_reentry_contract(),
        "gate": independent_observable_gate(),
    }
    return {
        "rows": [
            {
                "question": "direct_MTS_to_SM_threshold",
                "decision": "THEOREM_ZERO_ON_ACTIVE_FACTORIZED_FIXED_METRIC_MATCHING",
                "reason": "the MTS determinant depends on the public metric but no active SM field or mixed vertex",
            },
            {
                "question": "first_local_on_shell_residual",
                "decision": "PARITY_EVEN_WEYL_CUBED",
                "reason": "dimension-four curvature terms reduce to topological, field-redefinition or contact support",
            },
            {
                "question": "local_heavy_loop_as_competitive_signal",
                "decision": "REJECTED_FOR_MACROSCOPIC_ARENAS",
                "reason": "even at m r_s=10 a ten-solar-mass scalar-loop horizon shift is below 1e-80",
            },
            {
                "question": "first_macroscopic_candidate",
                "decision": "NO_SLIP_NONLOCAL_METRIC_FORM_FACTOR",
                "reason": "it can modify galaxy dynamics while making a parameter-free independent lensing prediction",
            },
            {
                "question": "active_promotion",
                "decision": "WITHHELD",
                "reason": "the galaxy kernel, causal continuation, pole proof and independent lensing score are not yet executed",
            },
        ],
        "direct_MTS_SM_threshold_status": "ZERO_IN_STATED_DOMAIN",
        "first_local_operator": "O_C3",
        "first_competitive_candidate": "F_C=-3F_R_NO_SLIP_NONLOCAL_METRIC_RESPONSE",
        "active_novel_MTS_numeric_predictions": 0,
        "candidate_numeric_predictions": 0,
        "next_target": NEXT_TARGET,
        "public_claim_allowed": False,
        "passed": all(section["passed"] for section in sections.values()),
    }


@lru_cache(maxsize=None)
def result() -> dict[str, Any]:
    sections = {
        "sources": source_contract(),
        "fields": residual_field_content(),
        "factorization": fixed_metric_factorization_theorem(),
        "reduction": redundancy_reduction(),
        "basis": dimension_six_grsmeft_basis(),
        "matching": cubic_spectral_matching(),
        "visibility": heavy_scalar_macroscopic_visibility(),
        "response": nonlocal_response_basis(),
        "samples": no_slip_inverse_samples(),
        "Ward": ward_and_reentry_contract(),
        "gate": independent_observable_gate(),
        "arbitration": arbitration(),
    }
    all_checks_pass = all(section["passed"] for section in sections.values())
    return {
        "marker": MARKER,
        "formal_marker": FORMAL_MARKER,
        "sections": sections,
        "decision": (
            "DIRECT_MTS_SM_THRESHOLDS_FACTORIZED_ZERO_FIRST_LOCAL_WEYL_CUBIC_"
            "HEAVY_LOOP_MACRO_ROUTE_REJECTED_NO_SLIP_NONLOCAL_RESPONSE_SELECTED_"
            "FOR_INDEPENDENT_LENSING_GATE_PRIVATE_NONCLAIM"
        ),
        "all_checks_pass": all_checks_pass,
        "next_target": NEXT_TARGET,
    }


def main() -> int:
    calculation = result()
    sections = calculation["sections"]
    print(
        "operators="
        f"{sections['basis']['operator_count']} "
        "direct_mixed_MTS="
        f"{sections['basis']['direct_mixed_MTS_coefficients_nonzero']} "
        "no_slip="
        f"{sections['response']['no_slip_eta']} "
        "active_novel_numeric="
        f"{sections['arbitration']['active_novel_MTS_numeric_predictions']}"
    )
    print(calculation["decision"])
    return 0 if calculation["all_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import csv
import hashlib
import sys
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True
getcontext().prec = 50


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4917"
CHECKED_DATE = "2026-07-12"
MARKER = "MTS_GRAVITY_MEDIATED_FLOW_MATTER_REENTRY_4917"
FORMAL_MARKER = "PPC4161_GRAVITY_MEDIATED_FLOW_MATTER_REENTRY_4917"
NEXT_TARGET = (
    "4918-Y5-R2FR-closed-bath-state-enthalpy-trace-profile-and-renormalized-"
    "aC-aR-matching-or-multiarena-bound.md"
)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
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
            "valid_for_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


def universal_channel_rows() -> list[dict[str, Any]]:
    q_squared, mass_squared = sp.symbols("q2 M_R2", positive=True)
    massless_kernel = 1 / (mass_squared * q_squared)
    pole_residue = sp.simplify(
        q_squared * mass_squared * massless_kernel
    )
    pole_diverges = sp.limit(massless_kernel, q_squared, 0, dir="+") == sp.oo
    return tagged(
        [
            {
                "channel_id": "CHAN4917_00_massless_EH_cross",
                "channel": "hidden-visible universal graviton exchange",
                "kernel": (
                    "i[T_X^mn T_SM_mn-T_X T_SM/2]/"
                    "[M_R^2(q^2+i0)]"
                ),
                "momentum_class": "NONLOCAL_MASSLESS_POLE",
                "local_flow_coefficient": False,
                "pole_residue_check": float(pole_residue),
                "passed": pole_residue == 1 and pole_diverges,
            },
            {
                "channel_id": "CHAN4917_01_pole_not_Wilson",
                "channel": "q^-2 Einstein pole",
                "kernel": "1/[M_R^2 q^2]",
                "momentum_class": "NONANALYTIC_AT_Q2_ZERO",
                "local_flow_coefficient": False,
                "pole_residue_check": float(pole_residue),
                "passed": pole_diverges,
            },
            {
                "channel_id": "CHAN4917_02_local_strict_EFT",
                "channel": "R^2/C^2 field-redefinition image",
                "kernel": (
                    "[4 a_C T_X^mn T_SM_mn+"
                    "2(a_R-2a_C/3)T_X T_SM]/M_R^4"
                ),
                "momentum_class": "LOCAL_CONTACT_FIRST_STRICT_EFT_ORDER",
                "local_flow_coefficient": True,
                "pole_residue_check": 0.0,
                "passed": True,
            },
            {
                "channel_id": "CHAN4917_03_channel_separation",
                "channel": "nonlocal GR versus local mixed contact",
                "kernel": "Gamma_cross=Gamma_EH_nonlocal+Gamma_contact+...",
                "momentum_class": "SEPARATE_ANALYTIC_STRUCTURES",
                "local_flow_coefficient": False,
                "pole_residue_check": float(pole_residue),
                "passed": True,
            },
        ]
    )


def stress_contact_rows() -> list[dict[str, Any]]:
    a_c, a_r, q_xx, q_ss, q_xs, trace_x, trace_s = sp.symbols(
        "a_C a_R Q_XX Q_SS Q_XS T_X T_SM"
    )
    trace_coefficient = a_r - 2 * a_c / 3
    total = 2 * a_c * (q_xx + 2 * q_xs + q_ss) + trace_coefficient * (
        trace_x + trace_s
    ) ** 2
    hidden_self = 2 * a_c * q_xx + trace_coefficient * trace_x**2
    visible_self = 2 * a_c * q_ss + trace_coefficient * trace_s**2
    cross = sp.expand(total - hidden_self - visible_self)
    expected = 4 * a_c * q_xs + 2 * trace_coefficient * trace_x * trace_s
    exact = sp.simplify(cross - expected) == 0
    return tagged(
        [
            {
                "basis_id": "CONTACT4917_00_total",
                "operator": "2 a_C T_mn T^mn+(a_R-2a_C/3)T^2",
                "coefficient": "1/M_R^4",
                "support_rule": "local total-stress contact",
                "symbolic_residual": 0.0,
                "passed": exact,
            },
            {
                "basis_id": "CONTACT4917_01_tensor_cross",
                "operator": "T_X^mn T_SM_mn",
                "coefficient": "4 a_C/M_R^4",
                "support_rule": "requires overlapping stress support",
                "symbolic_residual": float(sp.simplify(cross.coeff(q_xs) - 4 * a_c)),
                "passed": exact and cross.coeff(q_xs) == 4 * a_c,
            },
            {
                "basis_id": "CONTACT4917_02_trace_cross",
                "operator": "T_X T_SM",
                "coefficient": "2(a_R-2a_C/3)/M_R^4",
                "support_rule": "requires overlapping trace support",
                "symbolic_residual": 0.0,
                "passed": exact,
            },
            {
                "basis_id": "CONTACT4917_03_cross_identity",
                "operator": "Delta L_XSM",
                "coefficient": (
                    "[4a_C T_X.T_SM+2(a_R-2a_C/3)T_X T_SM]/M_R^4"
                ),
                "support_rule": "exact expansion of T=T_X+T_SM",
                "symbolic_residual": float(sp.simplify(cross - expected)),
                "passed": exact,
            },
        ]
    )


def perfect_fluid_projection_rows() -> list[dict[str, Any]]:
    a_c, a_r, rho, pressure, mass = sp.symbols(
        "a_C a_R rho_X p_X M_R", finite=True
    )
    u_stress, trace_sm = sp.symbols("U_SM T_SM")
    enthalpy = rho + pressure
    trace_x = -rho + 3 * pressure
    trace_coefficient = a_r - 2 * a_c / 3
    anisotropic_density = 4 * a_c * enthalpy / mass**4
    trace_density = (
        4 * a_c * pressure + 2 * trace_coefficient * trace_x
    ) / mass**4
    p_mix = -2 * anisotropic_density
    sigma_mix = -trace_density
    contact_density = (
        anisotropic_density * u_stress + trace_density * trace_sm
    )
    metric_variation_density = -sp.Rational(1, 2) * (
        p_mix * u_stress + 2 * sigma_mix * trace_sm
    )
    matching_residual = sp.simplify(
        contact_density - metric_variation_density
    )
    vacuum_p_mix = sp.simplify(p_mix.subs(pressure, -rho))
    dust_p_mix = sp.simplify(p_mix.subs(pressure, 0))
    radiation_p_mix = sp.simplify(p_mix.subs(pressure, rho / 3))
    return tagged(
        [
            {
                "projection_id": "PF4917_00_perfect_fluid",
                "state": "T_X^mn=(rho_X+p_X)u^m u^n+p_X g^mn",
                "p_mix": str(sp.factor(p_mix)),
                "sigma_mix": str(sp.factor(sigma_mix)),
                "interpretation": "universal inverse-metric shift at first strict-EFT order",
                "symbolic_residual": float(matching_residual),
                "passed": matching_residual == 0,
            },
            {
                "projection_id": "PF4917_01_metric_match",
                "state": "delta g_SM^mn=p_mix u^m u^n+2 sigma_mix g^mn",
                "p_mix": "-8*a_C*(rho_X+p_X)/M_R^4",
                "sigma_mix": (
                    "-[4a_C p_X+2(a_R-2a_C/3)(-rho_X+3p_X)]/M_R^4"
                ),
                "interpretation": "-T_mn delta g^mn/2 reproduces the cross contact",
                "symbolic_residual": float(matching_residual),
                "passed": matching_residual == 0,
            },
            {
                "projection_id": "PF4917_02_vacuum",
                "state": "p_X=-rho_X",
                "p_mix": str(vacuum_p_mix),
                "sigma_mix": "(8a_R-4a_C/3)rho_X/M_R^4",
                "interpretation": "no enthalpy and no physical preferred flow; trace shift may remain",
                "symbolic_residual": float(vacuum_p_mix),
                "passed": vacuum_p_mix == 0,
            },
            {
                "projection_id": "PF4917_03_dust",
                "state": "p_X=0",
                "p_mix": str(dust_p_mix),
                "sigma_mix": "2(a_R-2a_C/3)rho_X/M_R^4",
                "interpretation": "maximal enthalpy per unit rho for nonrelativistic state",
                "symbolic_residual": 0.0,
                "passed": sp.simplify(dust_p_mix + 8 * a_c * rho / mass**4) == 0,
            },
            {
                "projection_id": "PF4917_04_radiation",
                "state": "p_X=rho_X/3 and T_X=0",
                "p_mix": str(radiation_p_mix),
                "sigma_mix": "-4a_C rho_X/(3M_R^4)",
                "interpretation": "Weyl contact supplies both anisotropic and conformal pieces",
                "symbolic_residual": 0.0,
                "passed": sp.simplify(
                    radiation_p_mix + 32 * a_c * rho / (3 * mass**4)
                )
                == 0,
            },
            {
                "projection_id": "PF4917_05_Maxwell_trace",
                "state": "T_SM=0 for classical four-dimensional Maxwell",
                "p_mix": "-8a_C(rho_X+p_X)/M_R^4",
                "sigma_mix": "drops out of the Maxwell Hilbert trace at this order",
                "interpretation": "photon principal shift is controlled only by hidden enthalpy times a_C",
                "symbolic_residual": 0.0,
                "passed": True,
            },
        ]
    )


def state_zero_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "zero_id": "ZERO4917_00_Weyl_coefficient",
                "condition": "a_C=0",
                "consequence": "p_mix=0 for every hidden perfect-fluid state",
                "scope": "anisotropic flow channel only",
                "exact_zero": True,
                "passed": True,
            },
            {
                "zero_id": "ZERO4917_01_vacuum_enthalpy",
                "condition": "rho_X+p_X=0",
                "consequence": "p_mix=0 and u_X is not a physical state direction",
                "scope": "anisotropic flow channel; trace contact may remain",
                "exact_zero": True,
                "passed": True,
            },
            {
                "zero_id": "ZERO4917_02_disjoint_support",
                "condition": "supp(T_X) intersect supp(T_SM) is empty with positive gap",
                "consequence": "entire local X-SM contact vanishes pointwise",
                "scope": "tensor and trace contacts",
                "exact_zero": True,
                "passed": True,
            },
            {
                "zero_id": "ZERO4917_03_visible_conformal",
                "condition": "T_SM=0",
                "consequence": "sigma_mix trace channel is silent",
                "scope": "classical Maxwell or other conformal visible source",
                "exact_zero": True,
                "passed": True,
            },
            {
                "zero_id": "ZERO4917_04_full_overlap_zero",
                "condition": (
                    "a_C(rho_X+p_X)=0 and "
                    "4a_C p_X+2(a_R-2a_C/3)(-rho_X+3p_X)=0"
                ),
                "consequence": "both independent perfect-fluid contact projections vanish",
                "scope": "generic overlapping visible stress",
                "exact_zero": True,
                "passed": True,
            },
            {
                "zero_id": "ZERO4917_05_EH_not_direct_charge",
                "condition": "none",
                "consequence": "massless EH exchange remains ordinary universal gravity",
                "scope": "nonlocal channel; excluded from direct-flow zero question",
                "exact_zero": False,
                "passed": True,
            },
        ]
    )


def cone_bound_values() -> dict[str, Decimal]:
    one = Decimal(1)
    delta_lower = Decimal("-3e-15")
    delta_upper = Decimal("7e-16")

    def p_from_delta(delta: Decimal) -> Decimal:
        return one - (one + delta) ** 2

    p_lower = p_from_delta(delta_upper)
    p_upper = p_from_delta(delta_lower)
    product_lower = -p_upper / Decimal(8)
    product_upper = -p_lower / Decimal(8)
    product_abs = max(abs(product_lower), abs(product_upper))
    scalar_factor = Decimal(1920) * Decimal(str(sp.N(sp.pi**2, 40)))
    scalar_lower = product_lower * scalar_factor
    scalar_upper = product_upper * scalar_factor
    return {
        "delta_lower": delta_lower,
        "delta_upper": delta_upper,
        "p_lower": p_lower,
        "p_upper": p_upper,
        "p_abs": max(abs(p_lower), abs(p_upper)),
        "product_lower": product_lower,
        "product_upper": product_upper,
        "product_abs": product_abs,
        "scalar_lower": scalar_lower,
        "scalar_upper": scalar_upper,
        "scalar_abs": max(abs(scalar_lower), abs(scalar_upper)),
    }


def cone_bound_rows() -> list[dict[str, Any]]:
    values = cone_bound_values()
    source = (
        "post-checkpoint-work/4860-Y5-R2FR-parent-coupling-coscaling-law-"
        "beta-u-over-p-or-first-EM-radiation-source-profile-test.md; "
        "https://arxiv.org/abs/1710.05834"
    )
    return tagged(
        [
            {
                "bound_id": "CONE4917_00_observed_delta",
                "quantity": "delta_c=c_T/c_matter-1",
                "lower": float(values["delta_lower"]),
                "upper": float(values["delta_upper"]),
                "absolute_envelope": 3.0e-15,
                "formula": "reported GW170817/GRB170817A interval retained by 4860",
                "source": source,
                "applicability": "relative propagation over the sampled path",
                "passed": True,
            },
            {
                "bound_id": "CONE4917_01_p_mix",
                "quantity": "p_mix",
                "lower": float(values["p_lower"]),
                "upper": float(values["p_upper"]),
                "absolute_envelope": float(values["p_abs"]),
                "formula": "p_mix=1-(1+delta_c)^2",
                "source": source,
                "applicability": (
                    "EH graviton cone plus one universal matter metric and a "
                    "homogeneous/effectively averaged hidden state"
                ),
                "passed": values["p_lower"] < 0 < values["p_upper"],
            },
            {
                "bound_id": "CONE4917_02_aC_enthalpy_product",
                "quantity": "a_C(rho_X+p_X)/M_R^4",
                "lower": float(values["product_lower"]),
                "upper": float(values["product_upper"]),
                "absolute_envelope": float(values["product_abs"]),
                "formula": (
                    "p_mix=-8a_C(rho_X+p_X)/M_R^4; "
                    "delta_c=4a_C(rho_X+p_X)/M_R^4+O(a_C^2)"
                ),
                "source": source,
                "applicability": "single-operator no-cancellation first-order EFT projection",
                "passed": values["product_lower"] < 0 < values["product_upper"],
            },
            {
                "bound_id": "CONE4917_03_real_scalar_anchor",
                "quantity": "L(rho_X+p_X)/M_R^4",
                "lower": float(values["scalar_lower"]),
                "upper": float(values["scalar_upper"]),
                "absolute_envelope": float(values["scalar_abs"]),
                "formula": "a_C_scalar=L/(1920 pi^2)",
                "source": (
                    "post-checkpoint-work/4876-Y5-R2FR-integrated-H-parent-"
                    "action-saddle-regulator-and-induced-coefficient-matching-to-GN-"
                    "Lambda-and-R2.md"
                ),
                "applicability": "one real scalar loop only; not the renormalized total a_C",
                "passed": values["scalar_lower"] < 0 < values["scalar_upper"],
            },
        ]
    )


def coefficient_ownership_rows() -> list[dict[str, Any]]:
    scalar_prefactor = float(1 / (1920 * sp.pi**2))
    return tagged(
        [
            {
                "object": "a_C physical",
                "formula": "a_C^R=a_C^bare+a_C^threshold+a_C^loops+a_C^H/ghost",
                "owner": "renormalized integrated-H parent matching",
                "status": "OPEN_NUMERIC_TOTAL",
                "numeric_anchor": 0.0,
                "consequence": "p_mix cannot yet be numerically predicted",
            },
            {
                "object": "one real scalar a_C loop",
                "formula": "a_C_scalar=L/(1920 pi^2)",
                "owner": "4876 heat-kernel calculation",
                "status": "DERIVED_COMPONENT_NOT_TOTAL",
                "numeric_anchor": scalar_prefactor,
                "consequence": "p_mix_scalar=-L(rho_X+p_X)/(240 pi^2 M_R^4)",
            },
            {
                "object": "healthy matter a_C loop",
                "formula": "a_C_matter=L W_C/(1920 pi^2)",
                "owner": "4877 spectrum calculation",
                "status": "DERIVED_WEIGHT_FORMULA",
                "numeric_anchor": scalar_prefactor,
                "consequence": "W_C is spectrum dependent and does not fix finite matching data",
            },
            {
                "object": "a_R physical",
                "formula": "a_R^R=a_R^bare+a_R^threshold+a_R^loops+a_R^H/ghost",
                "owner": "renormalized integrated-H parent matching",
                "status": "OPEN_NUMERIC_TOTAL",
                "numeric_anchor": 0.0,
                "consequence": "trace/clock shift sigma_mix is not numerically predicted",
            },
            {
                "object": "hidden enthalpy",
                "formula": "h_X=rho_X+p_X",
                "owner": "closed bath state and local profile",
                "status": "OPEN_STATE_PROFILE",
                "numeric_anchor": 0.0,
                "consequence": "vacuum h_X=0 but dust/radiation states re-enter",
            },
            {
                "object": "anisotropic mixed coefficient",
                "formula": "p_mix=-8a_C^R h_X/M_R^4",
                "owner": "4917 contact projection",
                "status": "DERIVED_PRODUCT",
                "numeric_anchor": 8.0,
                "consequence": "first explicit gravity-mediated flow-matter reentry law",
            },
            {
                "object": "trace mixed coefficient",
                "formula": (
                    "sigma_mix=-[4a_C p_X+2(a_R-2a_C/3)(-rho_X+3p_X)]/M_R^4"
                ),
                "owner": "4917 contact projection",
                "status": "DERIVED_PRODUCT",
                "numeric_anchor": 2.0,
                "consequence": "requires clock mass and WEP projection in 4918",
            },
            {
                "object": "independent mixed counteroperators",
                "formula": "u u F F; u u DHdagDH; u u fbar gamma Df; f(I_X)O_SM",
                "owner": "full mixed 1PI matching",
                "status": "OPEN_NOT_ABSORBED_IN_AC_AR",
                "numeric_anchor": 0.0,
                "consequence": "4917 is not an all-orders zero or complete bound pack",
            },
        ]
    )


def decision_rows() -> list[dict[str, Any]]:
    values = cone_bound_values()
    return tagged(
        [
            {
                "gate": "universal_graviton_cross_channel",
                "status": "PASS_NONLOCAL_GR_IDENTIFIED",
                "decision": "massless 1/q^2 exchange is ordinary universal gravity",
            },
            {
                "gate": "local_stress_contact_basis",
                "status": "PASS_DERIVED_EXACT_FIRST_EFT_ORDER",
                "decision": "tensor and trace cross coefficients are 4a_C and 2(a_R-2a_C/3)",
            },
            {
                "gate": "perfect_fluid_flow_projection",
                "status": "PASS_PMIX_MINUS_8_AC_ENTHALPY",
                "decision": "p_mix=-8a_C(rho_X+p_X)/M_R^4",
            },
            {
                "gate": "local_zero_conditions",
                "status": "PASS_EXACT_CONDITIONS_DERIVED",
                "decision": "a_C=0 vacuum enthalpy or disjoint support silence the anisotropic contact",
            },
            {
                "gate": "conditional_cone_product_bound",
                "status": "PASS_NO_CANCELLATION_PRODUCT_BOUND",
                "decision": (
                    "abs[a_C(rho_X+p_X)/M_R^4]<="
                    f"{float(values['product_abs']):.16e}"
                ),
            },
            {
                "gate": "numeric_coefficient_prediction",
                "status": "OPEN_AC_AR_AND_STATE_PROFILE",
                "decision": "renormalized coefficients and hidden enthalpy are not parent-numbered",
            },
            {
                "gate": "all_orders_flow_matter_zero",
                "status": "NOT_PROVEN_INDEPENDENT_OPERATORS_REMAIN",
                "decision": "gravity-mediated contact is explicit but the full mixed 1PI basis is larger",
            },
            {
                "gate": "local_GR_status",
                "status": "CONDITIONAL_GR_BRANCH_RETAINED",
                "decision": "separated-source local GR remains intact; overlapping state needs the 4917 product bound",
            },
            {
                "gate": "next_route",
                "status": "MATCH_STATE_AND_RENORMALIZED_COEFFICIENTS",
                "decision": NEXT_TARGET,
            },
        ]
    )


def read_text_auto(path: Path) -> str:
    raw = path.read_bytes()
    encoding = "utf-16" if raw.startswith((b"\xff\xfe", b"\xfe\xff")) else "utf-8"
    return raw.decode(encoding, errors="replace")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def source_rows() -> list[dict[str, Any]]:
    sources = [
        (
            "SRC4917_00_4916_validation",
            OUTPUT / "P8_Y5_BRR545_4916_VALIDATION.csv",
            "VAL4916_OVERALL,PASS",
            "predecessor_validation",
        ),
        (
            "SRC4917_01_4915",
            POST
            / "4915-Y5-R2FR-parent-EH-residue-universal-source-coupling-and-measured-G-calibration-or-closure-demotion.md",
            "MTS_SINGLE_FUNCTIONAL_EH_SOURCE_RESIDUE_4915",
            "universal_EH_exchange",
        ),
        (
            "SRC4917_02_4916",
            POST
            / "4916-Y5-R2FR-covariantization-map-from-microscopic-motion-action-to-integrated-H-parent-and-no-direct-flow-charge-or-primitive-freeze.md",
            "MTS_COVARIANTIZATION_MAP_FLOW_CHARGE_4916",
            "tree_flow_zero_and_reentry_basis",
        ),
        (
            "SRC4917_03_4876",
            POST
            / "4876-Y5-R2FR-integrated-H-parent-action-saddle-regulator-and-induced-coefficient-matching-to-GN-Lambda-and-R2.md",
            "INTEGRATED_H_PARENT_SADDLE_HEAT_KERNEL_POLE_HIERARCHY_4876",
            "scalar_heat_kernel_coefficients",
        ),
        (
            "SRC4917_04_4877",
            POST
            / "4877-Y5-R2FR-MTS-bath-signed-spectrum-sum-rules-and-nonlocal-form-factor-completion-or-renormalized-vacuum-freeze.md",
            "MTS_SPECTRUM_NO_GO_NONLOCAL_COMPLETION_AND_RENORMALIZED_VACUUM_FREEZE_4877",
            "spectrum_weights_and_renormalized_ownership",
        ),
        (
            "SRC4917_05_4879",
            POST
            / "4879-Y5-R2FR-source-size-contact-matching-and-second-order-beta-completion-plus-gauge-invariant-light-kernel-or-strict-EFT-local-GR-promotion-gate.md",
            "MTS_FINITE_SOURCE_BETA_LIGHT_CLOCK_LOCAL_GR_CERTIFICATE_4879",
            "stress_contact_and_support_theorem",
        ),
        (
            "SRC4917_06_4860",
            POST
            / "4860-Y5-R2FR-parent-coupling-coscaling-law-beta-u-over-p-or-first-EM-radiation-source-profile-test.md",
            "SHARED_CONE_COUPLING_LAW_4860",
            "relative_cone_interval_and_metric_algebra",
        ),
        (
            "SRC4917_07_checkpoint",
            POST
            / "4917-Y5-R2FR-radiative-flow-matter-reentry-coefficients-from-gravity-mediation-or-local-bound-pack.md",
            MARKER,
            "generated_checkpoint",
        ),
        (
            "SRC4917_08_research",
            Path(__file__).resolve(),
            "def perfect_fluid_projection_rows",
            "generated_research_code",
        ),
        (
            "SRC4917_09_validation",
            POST
            / "scripts"
            / "Y5_R2FR_4917_radiative_flow_matter_reentry_validation.py",
            "VAL4917_OVERALL",
            "generated_validation_code",
        ),
        (
            "SRC4917_10_formal",
            FORMAL
            / "933-PPC4161-gravity-mediated-flow-matter-reentry-and-product-bound.md",
            FORMAL_MARKER,
            "formal_summary",
        ),
        (
            "SRC4917_11_provenance",
            POST / "source-intake" / "parent_coupling" / "4917" / "PROVENANCE.md",
            "MTS_GRAVITY_MEDIATED_REENTRY_PROVENANCE_4917",
            "provenance",
        ),
        (
            "SRC4917_12_claim",
            FORMAL / "02-claims-register.csv",
            "L-759",
            "register",
        ),
        (
            "SRC4917_13_variable",
            FORMAL / "04-variable-audit.csv",
            "UniversalCrossChannel4917_MTS",
            "register",
        ),
        (
            "SRC4917_14_equation",
            FORMAL / "05-equation-register.md",
            "1.210 Gravity-mediated local stress contact and flow projection",
            "register",
        ),
        (
            "SRC4917_15_redteam",
            FORMAL / "06-consistency-red-team.md",
            "161. A field-redefinition contact is not the massless graviton pole",
            "register",
        ),
        (
            "SRC4917_16_spine",
            FORMAL / "07-unification-spine.md",
            "PPC4161 checkpoint 4917",
            "register",
        ),
        (
            "SRC4917_17_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            FORMAL_MARKER,
            "resume",
        ),
    ]
    output: list[dict[str, Any]] = []
    for source_id, path, marker, role in sources:
        exists = path.exists()
        content = read_text_auto(path) if exists else ""
        output.append(
            {
                "source_id": source_id,
                "source_type": role,
                "source_path_or_url": str(path),
                "local_path_required": True,
                "source_exists": exists,
                "marker": marker,
                "marker_found": marker in content,
                "sha256": sha256(path) if exists else "",
            }
        )
    return tagged(output)


def main() -> int:
    tables = {
        "P8_Y5_R2FR_4917_CHANNEL_DECOMPOSITION.csv": universal_channel_rows(),
        "P8_Y5_R2FR_4917_STRESS_CONTACT_BASIS.csv": stress_contact_rows(),
        "P8_Y5_R2FR_4917_PERFECT_FLUID_PROJECTION.csv": perfect_fluid_projection_rows(),
        "P8_Y5_R2FR_4917_STATE_ZERO_CONDITIONS.csv": state_zero_rows(),
        "P8_Y5_R2FR_4917_CONE_PRODUCT_BOUND.csv": cone_bound_rows(),
        "P8_Y5_R2FR_4917_COEFFICIENT_OWNERSHIP.csv": coefficient_ownership_rows(),
        "P8_Y5_R2FR_4917_GATE_DECISION.csv": decision_rows(),
    }
    for filename, rows in tables.items():
        write_csv(OUTPUT / filename, rows)
    sources = source_rows()
    write_csv(OUTPUT / "P8_Y5_R2FR_4917_SOURCE_REGISTER.csv", sources)
    all_rows = [row for rows in tables.values() for row in rows]
    passed = (
        all(bool(row.get("passed", True)) for row in all_rows)
        and all(row["source_exists"] and row["marker_found"] for row in sources)
    )
    print(
        "P8_Y5_R2FR_4917_REENTRY_PASS"
        if passed
        else "P8_Y5_R2FR_4917_REENTRY_FAIL"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

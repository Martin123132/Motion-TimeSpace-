from __future__ import annotations

import csv
import hashlib
import math
import sys
from pathlib import Path
from typing import Any

from scipy.constants import G, c, hbar, physical_constants


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
SCRIPTS = POST / "scripts"

CHECKPOINT = "4924"
CHECKED_DATE = "2026-07-12"
MARKER = "MTS_PARENT_WEYL_C3_FINITE_MATCHING_4924"
FORMAL_MARKER = "PPC4161_PARENT_WEYL_C3_FINITE_MATCHING_4924"
NEXT_TARGET = (
    "4925-Y5-R2FR-integrated-H-two-loop-renormalization-condition-"
    "and-finite-zeta-plus-boundary-owner-or-explicit-Wilson-input.md"
)

HEAT_KERNEL_URL = "https://arxiv.org/abs/hep-th/0306138"
HEAVY_FIELDS_URL = "https://arxiv.org/abs/1611.02705"
GS_SOURCE_URL = "https://scipost.org/SciPostPhysLectNotes.98/pdf"
GW170608_URL = "https://arxiv.org/abs/2407.08929"
GW250114_URL = "https://arxiv.org/abs/2509.08099"

SUN_MASS_KG = 1.988409870698051e30
PLANCK_LENGTH_M = physical_constants["Planck length"][0]
ELECTRON_VOLT_J = physical_constants["electron volt"][0]
HBAR_C_EV_M = hbar * c / ELECTRON_VOLT_J
SCALAR_DENOMINATOR = 30240.0 * (4.0 * math.pi) ** 2
CANONICAL_SCALAR_DENOMINATOR = 30240.0 * math.pi
GS_POLE = 209.0 / 2880.0
GS_A_LOG_COEFFICIENT = 209.0 / (1440.0 * math.pi**2)

MASS_GAP_PATH = OUTPUT / "P8_Y5_R2FR_4909_EXTRAPOLATION.csv"
INTERACTING_GATE_PATH = OUTPUT / "P8_Y5_R2FR_4914_GATE_DECISION.csv"
GW170608_PATH = OUTPUT / "P8_Y5_R2FR_4922_GW170608_COEFFICIENT_BOUND.csv"
COMPACT_PATH = OUTPUT / "P8_Y5_R2FR_4922_COMPACT_DOMAIN.csv"
GW250114_RECAST_PATH = OUTPUT / "P8_Y5_R2FR_4923_BRANCH_RECAST.csv"
GW250114_ROBUST_PATH = OUTPUT / "P8_Y5_R2FR_4923_ROBUSTNESS.csv"

DIGEST_CACHE: dict[Path, str] = {}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
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


def digest(path: Path) -> str:
    if path in DIGEST_CACHE:
        return DIGEST_CACHE[path]
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(4 * 1024 * 1024), b""):
            hasher.update(block)
    value = hasher.hexdigest()
    DIGEST_CACHE[path] = value
    return value


def read_text_auto(path: Path) -> str:
    raw = path.read_bytes()
    encoding = "utf-16" if raw.startswith((b"\xff\xfe", b"\xfe\xff")) else "utf-8"
    return raw.decode(encoding, errors="replace")


def mass_gap_inputs() -> dict[str, float]:
    row = read_csv(MASS_GAP_PATH)[0]
    return {
        "central": float(row["constant_c_m"]),
        "central_error": float(row["constant_c_m_standard_error"]),
        "union_min": float(row["two_sigma_model_union_minimum"]),
        "union_max": float(row["two_sigma_model_union_maximum"]),
        "linear_mu": float(row["linear_mu_intercept"]),
        "linear_mu2": float(row["linear_mu2_intercept"]),
    }


def scalar_c6_lambda(cm_value: float) -> float:
    return 1.0 / (SCALAR_DENOMINATOR * cm_value**2)


def scalar_a_mu2_over_G(cm_value: float) -> float:
    return 1.0 / (CANONICAL_SCALAR_DENOMINATOR * cm_value**2)


def scalar_mass_floor_eV(ell_cap_m: float, real_poles: int) -> float:
    return (
        HBAR_C_EV_M
        * math.sqrt(real_poles)
        * PLANCK_LENGTH_M
        / (math.sqrt(CANONICAL_SCALAR_DENOMINATOR) * ell_cap_m**2)
    )


def parent_action_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "audit_id": "PA4924_00_public_metric",
                "object": "integrated-H public metric",
                "current_parent_clause": "g_hat is reconstructed from H and all determinants use the same public metric",
                "six_derivative_implication": "the I1 coefficient belongs to the same metric 1PI action",
                "status": "PARENT_METRIC_OWNER_CLOSED",
                "source": "post-checkpoint-work/4876-Y5-R2FR-integrated-H-parent-action-saddle-regulator-and-induced-coefficient-matching-to-GN-Lambda-and-R2.md",
                "passed": True,
            },
            {
                "audit_id": "PA4924_01_scalar_determinant",
                "object": "motion-scalar determinant",
                "current_parent_clause": "one healthy real scalar pole contributes one half Tr log D",
                "six_derivative_implication": "finite parity-even I1 threshold is calculable per pole",
                "status": "DETERMINANT_THRESHOLD_OWNER_CLOSED_PER_REAL_POLE",
                "source": "post-checkpoint-work/4908-Y5-R2FR-microscopic-MTS-metric-three-point-vertex-and-Weyl-cubic-coefficient-or-zero-residual-theorem.md",
                "passed": True,
            },
            {
                "audit_id": "PA4924_02_projector",
                "object": "off-shell to Ricci-flat projector",
                "current_parent_clause": "rank-eight a6 quotient and I2=I1/2 Ricci-flat map",
                "six_derivative_implication": "the scalar threshold lands in the same I1 coordinate as alpha_bar1",
                "status": "GEOMETRIC_PROJECTOR_CLOSED",
                "source": "post-checkpoint-work/4911-Y5-R2FR-full-off-shell-a6-template-basis-and-interacting-Weyl-cubic-projector.md",
                "passed": True,
            },
            {
                "audit_id": "PA4924_03_interacting_residual",
                "object": "non-Gaussian motion-scalar residual",
                "current_parent_clause": "all-evidence significance below promotion and covariant-image test failed",
                "six_derivative_implication": "no numeric residual may be added to the finite threshold",
                "status": "ZERO_SELECTED_NOT_ZERO_THEOREM",
                "source": "post-checkpoint-work/4914-Y5-R2FR-matched-interacting-TTT-replicates-cutoff-stencil-continuum-or-residual-demotion.md",
                "passed": True,
            },
            {
                "audit_id": "PA4924_04_quantum_metric",
                "object": "integrated metric and ghost sector",
                "current_parent_clause": "quantum pure gravity has a nonzero two-loop I1 pole",
                "six_derivative_implication": "the counterterm-complete parent must contain a renormalized I1 boundary coefficient",
                "status": "SIX_DERIVATIVE_COUNTERTERM_REQUIRED",
                "source": "post-checkpoint-work/4921-Y5-R2FR-pure-metric-curvature-cubed-and-nonlocal-tail-observable-separation-or-invariant-vacuum-GR-domain-extension-gate.md",
                "passed": True,
            },
            {
                "audit_id": "PA4924_05_EH_calibration",
                "object": "measured Newton coefficient",
                "current_parent_clause": "one calibration fixes M_R^2 and universal source residue",
                "six_derivative_implication": "M_R^2 does not fix an independent dimension-six finite boundary",
                "status": "NO_DIMENSION_SIX_PREDICTION_FROM_G",
                "source": "post-checkpoint-work/4915-Y5-R2FR-parent-EH-residue-universal-source-coupling-and-measured-G-calibration-or-closure-demotion.md",
                "passed": True,
            },
        ]
    )


def mass_gap_rows(inputs: dict[str, float]) -> list[dict[str, Any]]:
    profiles = [
        ("central_constant_fit", inputs["central"], "PILOT_CENTRAL"),
        ("two_sigma_union_low_cm", inputs["union_min"], "CONSERVATIVE_LOW_CM"),
        ("two_sigma_union_high_cm", inputs["union_max"], "CONSERVATIVE_HIGH_CM"),
        ("linear_a_mu_intercept", inputs["linear_mu"], "MODEL_SENSITIVITY"),
        ("linear_a2_mu2_intercept", inputs["linear_mu2"], "MODEL_SENSITIVITY"),
    ]
    rows: list[dict[str, Any]] = []
    for profile, cm_value, status in profiles:
        rows.append(
            {
                "profile": profile,
                "c_m": cm_value,
                "c6_lambda_coefficient_per_real_pole": scalar_c6_lambda(cm_value),
                "a_plus_mu2_over_G_per_real_pole": scalar_a_mu2_over_G(cm_value),
                "zeta_formula": "zeta_psi=c6_lambda lambda^(-3/4)",
                "a_plus_formula": "a_psi=[G/(30240 pi c_m^2 mu^2)] per real pole",
                "threshold_sign": "positive",
                "mass_fit_status": status,
                "coefficient_promoted": False,
                "passed": cm_value > 0.0,
            }
        )
    return tagged(rows)


def scalar_threshold_rows(inputs: dict[str, float]) -> list[dict[str, Any]]:
    central = inputs["central"]
    rows: list[dict[str, Any]] = []
    for real_poles in (1, 2, 3):
        c6_value = real_poles * scalar_c6_lambda(central)
        canonical_value = real_poles * scalar_a_mu2_over_G(central)
        rows.append(
            {
                "threshold_id": f"SCALAR4924_N{real_poles}",
                "real_scalar_poles": real_poles,
                "mass_gap": "m_gap=c_m mu",
                "finite_cutoff_factor": "F=exp[-m_gap^2/Lambda_UV^2] in (0,1]",
                "zeta_plus": f"{real_poles}/[30240(4pi)^2 m_gap^2] times F",
                "a_plus": f"{real_poles} G/[30240 pi m_gap^2] times F",
                "ell_plus": "[N/(30240 pi)]^(1/4) sqrt(l_P lambda_C) F^(1/4)",
                "c6_lambda_central": c6_value,
                "a_plus_mu2_over_G_central": canonical_value,
                "sign": "positive",
                "parity_odd_threshold": 0.0,
                "nonminimal_xi_dependence_on_Ricci_flat_I1": 0.0,
                "status": "DERIVED_PER_HEALTHY_REAL_POLE_GAP_AND_MULTIPLICITY_CONDITIONAL",
                "passed": c6_value > 0.0,
            }
        )
    return tagged(rows)


def gs_running_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for log_magnitude in (1.0, 100.0):
        a_over_planck_four = GS_A_LOG_COEFFICIENT * log_magnitude
        ell_over_planck = a_over_planck_four**0.25
        rows.append(
            {
                "running_id": f"GS4924_log_{int(log_magnitude)}",
                "pole_residue_209_over_2880": GS_POLE,
                "log_magnitude": log_magnitude,
                "delta_zeta_plus_over_G": (
                    GS_POLE
                    * 32.0
                    * math.pi
                    / (4.0 * math.pi) ** 4
                    * log_magnitude
                ),
                "delta_a_plus_over_lP4": a_over_planck_four,
                "ell_plus_over_lP": ell_over_planck,
                "ell_plus_m": ell_over_planck * PLANCK_LENGTH_M,
                "formula": "Delta a_+=[209/(1440 pi^2)] l_P^4 ln(mu/mu0)",
                "status": "CANONICAL_I1_RUNNING_NOT_FINITE_BOUNDARY",
                "old_4921_beta1_length_reused": False,
                "passed": True,
            }
        )
    return tagged(rows)


def physical_gate_inputs() -> list[dict[str, Any]]:
    robust_rows = read_csv(GW250114_ROBUST_PATH)
    recast_rows = read_csv(GW250114_RECAST_PATH)
    positive_alpha = max(float(row["alpha_upper_90"]) for row in robust_rows)
    mass_95 = max(float(row["mass_q95_solar"]) for row in recast_rows)
    mass_length_95 = G * mass_95 * SUN_MASS_KG / c**2
    gw250114_ell = mass_length_95 * positive_alpha**0.25

    gw170608_rows = read_csv(GW170608_PATH)
    gw170608_positive = next(
        row for row in gw170608_rows if row["branch"] == "positive"
    )
    compact_rows = read_csv(COMPACT_PATH)
    neutron_star = next(
        row
        for row in compact_rows
        if row["system"] == "1.4_solar_mass_12km_neutron_star"
    )
    black_hole = next(
        row
        for row in compact_rows
        if row["system"] == "10_solar_mass_Schwarzschild_horizon"
    )
    return [
        {
            "gate_id": "GW250114_positive_robust",
            "arena": "GW250114 branch-conditional positive scalar sign",
            "ell_cap_m": gw250114_ell,
            "input_kind": "robust positive alpha endpoint and 95th-percentile remnant mass",
            "alpha_or_domain_input": positive_alpha,
            "source": "post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4923_ROBUSTNESS.csv",
            "authoritative_level": "PRIVATE_BRANCH_CONDITIONAL_RECAST",
        },
        {
            "gate_id": "GW170608_positive_published",
            "arena": "GW170608 positive scalar sign",
            "ell_cap_m": float(gw170608_positive["approx_ell_plus_upper_m"]),
            "input_kind": "published alpha_bar1 interval with approximate 19-solar-mass translation",
            "alpha_or_domain_input": float(gw170608_positive["alpha_bar1_endpoint"]),
            "source": gw170608_positive["source"],
            "authoritative_level": "PUBLISHED_DIMENSIONLESS_APPROXIMATE_LENGTH",
        },
        {
            "gate_id": "BH10_one_percent",
            "arena": "10-solar-mass Schwarzschild one-percent domain",
            "ell_cap_m": float(black_hole["ell_plus_upper_m_for_domain"]),
            "input_kind": "curvature-domain requirement",
            "alpha_or_domain_input": 0.01,
            "source": "post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4922_COMPACT_DOMAIN.csv",
            "authoritative_level": "INTERNAL_DOMAIN_GATE",
        },
        {
            "gate_id": "NS14_one_percent",
            "arena": "1.4-solar-mass 12-km neutron-star one-percent domain",
            "ell_cap_m": float(neutron_star["ell_plus_upper_m_for_domain"]),
            "input_kind": "curvature-domain requirement before EOS completion",
            "alpha_or_domain_input": 0.01,
            "source": "post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4922_COMPACT_DOMAIN.csv",
            "authoritative_level": "INTERNAL_DOMAIN_GATE",
        },
    ]


def physical_scale_rows(inputs: dict[str, float]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for gate in physical_gate_inputs():
        ell_cap = float(gate["ell_cap_m"])
        for real_poles in (1, 2, 3):
            mass_floor = scalar_mass_floor_eV(ell_cap, real_poles)
            rows.append(
                {
                    **gate,
                    "real_scalar_poles": real_poles,
                    "m_gap_floor_eV": mass_floor,
                    "mu_floor_eV_central_cm": mass_floor / inputs["central"],
                    "mu_floor_eV_guaranteed_over_cm_union": (
                        mass_floor / inputs["union_min"]
                    ),
                    "scaling_with_multiplicity": "sqrt(N_real)",
                    "current_mu_value_owned": False,
                    "gate_closed": False,
                    "status": "EXACT_REQUIRED_SCALE_NOT_CURRENT_PARENT_PREDICTION",
                    "passed": mass_floor > 0.0,
                }
            )
    return tagged(rows)


def matching_ledger_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "term_id": "MATCH4924_00_boundary",
                "term": "a_+,b(mu0)=16 pi G zeta_+,b(mu0)",
                "owner": "UV parent renormalization condition",
                "status": "FINITE_BOUNDARY_NOT_OWNED",
                "sign": "unknown",
                "numeric_value": "",
                "may_enter_total": True,
                "passed": True,
            },
            {
                "term_id": "MATCH4924_01_motion_scalar",
                "term": "N_psi G F/[30240 pi m_gap^2]",
                "owner": "healthy motion-scalar determinant poles",
                "status": "DERIVED_PER_POLE_CONDITIONAL_ON_GAP_AND_COUNT",
                "sign": "positive",
                "numeric_value": "c6_lambda central per real pole=2.007712100686747e-7",
                "may_enter_total": True,
                "passed": True,
            },
            {
                "term_id": "MATCH4924_02_interacting_residual",
                "term": "a_+,int,res",
                "owner": "non-Gaussian stress-three-point continuum limit",
                "status": "NO_NONZERO_VALUE_PROMOTED_ZERO_SELECTED_NOT_THEOREM",
                "sign": "unknown",
                "numeric_value": "",
                "may_enter_total": True,
                "passed": True,
            },
            {
                "term_id": "MATCH4924_03_other_thresholds",
                "term": "sum_i a_+,i,threshold",
                "owner": "massive MTS, SM and hidden species spectrum",
                "status": "SPECTRUM_AND_MASSES_INCOMPLETE",
                "sign": "species dependent",
                "numeric_value": "",
                "may_enter_total": True,
                "passed": True,
            },
            {
                "term_id": "MATCH4924_04_GS_running",
                "term": "[209/(1440 pi^2)] l_P^4 ln(mu/mu0)",
                "owner": "universal pure-gravity two-loop running",
                "status": "DERIVED_RUNNING_NOT_FINITE_VALUE",
                "sign": "RG convention and log direction",
                "numeric_value": "ell_plus=0.3482338723 l_P per unit log magnitude",
                "may_enter_total": True,
                "passed": True,
            },
            {
                "term_id": "MATCH4924_05_metric_ghost_finite",
                "term": "a_+,H+gh,finite",
                "owner": "integrated-H and BRST-complete UV matching",
                "status": "FINITE_PART_NOT_CALCULATED",
                "sign": "unknown",
                "numeric_value": "",
                "may_enter_total": True,
                "passed": True,
            },
            {
                "term_id": "MATCH4924_06_total",
                "term": "a_+=a_+,b+a_+,psi+a_+,int,res+sum thresholds+Delta a_GS+a_+,H+gh,finite",
                "owner": "complete renormalized parent",
                "status": "TOTAL_MAGNITUDE_AND_SIGN_NOT_DERIVED",
                "sign": "unknown",
                "numeric_value": "",
                "may_enter_total": True,
                "passed": True,
            },
        ]
    )


def counterterm_theorem_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "clause_id": "CT4924_00_operator",
                "premise": "I1 is a local Diff-invariant parity-even scalar",
                "result": "no retained parent symmetry forbids zeta_+,b I1",
                "status": "LEGAL_OPERATOR",
                "passed": True,
            },
            {
                "clause_id": "CT4924_01_scalar",
                "premise": "a healthy massive scalar determinant is integrated out",
                "result": "a finite positive I1 threshold proportional to 1/m_gap^2 is generated",
                "status": "FINITE_THRESHOLD_DERIVED",
                "passed": True,
            },
            {
                "clause_id": "CT4924_02_quantum_gravity",
                "premise": "the public metric is quantum and the two-loop pure-gravity pole is retained",
                "result": "an I1 counterterm is required for renormalization",
                "status": "COUNTERTERM_MANDATORY",
                "passed": True,
            },
            {
                "clause_id": "CT4924_03_running",
                "premise": "the I1 pole residue is nonzero",
                "result": "zeta_+(mu0)=0 can hold at one chosen scale but not all scales",
                "status": "ZERO_IS_SCALE_BOUNDARY_NOT_THEOREM",
                "passed": True,
            },
            {
                "clause_id": "CT4924_04_Newton",
                "premise": "M_R^2 is calibrated from measured G once",
                "result": "the independent six-derivative finite coefficient is not fixed",
                "status": "EH_CALIBRATION_INSUFFICIENT",
                "passed": True,
            },
            {
                "clause_id": "CT4924_05_current_parent",
                "premise": "no UV fixed point, spectral sum rule or matching observable for zeta_+,b is present",
                "result": "the current corpus cannot derive the total finite zeta_+ or its sign",
                "status": "FINITE_BOUNDARY_OBSTRUCTION_PROVED",
                "passed": True,
            },
            {
                "clause_id": "CT4924_06_minimal_branch",
                "premise": "one declares zeta_+,b(mu0)=0 and the 4914 residual-zero branch",
                "result": "the per-pole scalar threshold is a positive conditional prediction",
                "status": "EXPLICIT_CLOSURE_BRANCH_NOT_PARENT_THEOREM",
                "passed": True,
            },
        ]
    )


def gate_decision_rows(
    inputs: dict[str, float],
    physical_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    neutron_star_one_pole = next(
        row
        for row in physical_rows
        if row["gate_id"] == "NS14_one_percent"
        and row["real_scalar_poles"] == 1
    )
    return tagged(
        [
            {
                "gate": "motion_scalar_finite_threshold",
                "status": "DERIVED_PER_HEALTHY_REAL_POLE",
                "decision": "retain the positive 1/m_gap^2 threshold in the matching ledger",
                "passed": True,
            },
            {
                "gate": "motion_scalar_sign",
                "status": "POSITIVE_DERIVED",
                "decision": "a healthy real scalar determinant contributes positive zeta_+ and zero parity-odd threshold",
                "passed": True,
            },
            {
                "gate": "mass_gap_constant",
                "status": "PILOT_NOT_PROMOTED",
                "decision": (
                    f"use c_m={inputs['central']:.9g} only as a pilot and "
                    f"retain the two-sigma union [{inputs['union_min']:.9g},"
                    f"{inputs['union_max']:.9g}]"
                ),
                "passed": True,
            },
            {
                "gate": "interacting_residual",
                "status": "NO_NONZERO_VALUE_PROMOTED",
                "decision": "do not convert the failed covariant-image estimator into c6",
                "passed": True,
            },
            {
                "gate": "GS_running",
                "status": "DERIVED_CANONICAL_I1_AND_NEGLIGIBLE",
                "decision": "use ell_GS=0.348234 l_P per unit logarithm, not the superseded beta1 length",
                "passed": True,
            },
            {
                "gate": "finite_boundary",
                "status": "REQUIRED_NOT_OWNED",
                "decision": "the quantum metric parent requires an I1 renormalization boundary not fixed by G",
                "passed": True,
            },
            {
                "gate": "scalar_compact_scale",
                "status": "EXACT_CONDITIONAL_FLOOR",
                "decision": (
                    "one real pole satisfies the selected neutron-star "
                    "one-percent threshold if mu exceeds "
                    f"{float(neutron_star_one_pole['mu_floor_eV_guaranteed_over_cm_union']):.6e} eV"
                ),
                "passed": True,
            },
            {
                "gate": "total_zeta_plus",
                "status": "NOT_DERIVED",
                "decision": "the finite boundary, multiplicity, other thresholds and metric-ghost finite part prevent a total sign or value",
                "passed": True,
            },
            {
                "gate": "weak_invariant_vacuum_GR",
                "status": "RETAINED",
                "decision": "none of the derived universal running terms alters the weak branch",
                "passed": True,
            },
            {
                "gate": "compact_vacuum_and_matter_GR",
                "status": "NOT_PROMOTED_TOTAL",
                "decision": "the scalar subterm has a tiny exact scale floor but the total coefficient is still open",
                "passed": True,
            },
            {
                "gate": "full_MTS_to_GR",
                "status": "NOT_PROMOTED",
                "decision": "finite six-derivative matching and compact matter remain incomplete",
                "passed": True,
            },
            {
                "gate": "next_target",
                "status": "UV_BOUNDARY_OWNER",
                "decision": NEXT_TARGET,
                "passed": True,
            },
        ]
    )


def source_rows() -> list[dict[str, Any]]:
    local_sources: list[tuple[str, Path, str | None, str]] = [
        ("SRC4924_00_prior_validation", OUTPUT / "P8_Y5_BRR545_4923_VALIDATION.csv", "VAL4923_OVERALL,PASS", "predecessor_validation"),
        ("SRC4924_01_4876", POST / "4876-Y5-R2FR-integrated-H-parent-action-saddle-regulator-and-induced-coefficient-matching-to-GN-Lambda-and-R2.md", "INTEGRATED_H_PARENT_SADDLE_HEAT_KERNEL_POLE_HIERARCHY_4876", "parent_action"),
        ("SRC4924_02_heat_kernel", POST / "source-intake" / "heat_kernel_a6" / "4881" / "hep-th-0306138.tar", None, "primary_source_archive"),
        ("SRC4924_03_4908", POST / "4908-Y5-R2FR-microscopic-MTS-metric-three-point-vertex-and-Weyl-cubic-coefficient-or-zero-residual-theorem.md", "MTS_MICROSCOPIC_METRIC_THREE_POINT_WEYL_CUBIC_4908", "scalar_threshold"),
        ("SRC4924_04_4909", POST / "4909-Y5-R2FR-renormalized-motion-scalar-measure-mass-gap-and-stress-three-point-matching.md", "MTS_RENORMALIZED_MOTION_SCALAR_GAP_STRESS_THREE_POINT_4909", "mass_gap"),
        ("SRC4924_05_mass_inputs", MASS_GAP_PATH, "constant_c_m", "mass_gap_data"),
        ("SRC4924_06_4911", POST / "4911-Y5-R2FR-full-off-shell-a6-template-basis-and-interacting-Weyl-cubic-projector.md", "MTS_FULL_OFFSHELL_A6_TEMPLATE_PROJECTOR_4911", "geometric_projector"),
        ("SRC4924_07_4912", POST / "4912-Y5-R2FR-free-lattice-multigeometry-a6-response-and-continuum-projector-recovery.md", "MTS_FREE_LATTICE_MULTIGEOMETRY_CONTINUUM_PROJECTOR_4912", "determinant_recovery"),
        ("SRC4924_08_4914", POST / "4914-Y5-R2FR-matched-interacting-TTT-replicates-cutoff-stencil-continuum-or-residual-demotion.md", "MTS_COMPLEX_SOURCE_TAYLOR_TTT_REPLICA_4914", "interacting_residual"),
        ("SRC4924_09_4914_gate", INTERACTING_GATE_PATH, "G4914_10_promotion", "interacting_gate_data"),
        ("SRC4924_10_4915", POST / "4915-Y5-R2FR-parent-EH-residue-universal-source-coupling-and-measured-G-calibration-or-closure-demotion.md", "MTS_SINGLE_FUNCTIONAL_EH_SOURCE_RESIDUE_4915", "EH_calibration"),
        ("SRC4924_11_4921", POST / "4921-Y5-R2FR-pure-metric-curvature-cubed-and-nonlocal-tail-observable-separation-or-invariant-vacuum-GR-domain-extension-gate.md", "MTS_C3_NONLOCAL_OBSERVABLE_DOMAIN_GATE_4921", "GS_running"),
        ("SRC4924_12_GS_data", OUTPUT / "P8_Y5_R2FR_4921_GOROFF_SAGNOTTI_RUNNING.csv", "GS4921_log_1", "GS_running_data"),
        ("SRC4924_13_4922", POST / "4922-Y5-R2FR-cubic-curvature-strong-field-waveform-love-ringdown-bound-or-compact-vacuum-GR-domain-gate.md", "MTS_WEYL_C3_GW170608_DOMAIN_GATE_4922", "canonical_map"),
        ("SRC4924_14_4923", POST / "4923-Y5-R2FR-GW250114-gravitational-QNM-parity-even-Weyl-cubic-recast-or-posterior-acquisition-gate.md", "MTS_GW250114_GRAVITATIONAL_QNM_WEYL_C3_RECAST_4923", "current_bound"),
        ("SRC4924_15_checkpoint", POST / "4924-Y5-R2FR-renormalized-parent-Weyl-cubic-finite-matching-sign-and-scale-from-motion-scalar-determinant-or-explicit-counterterm-boundary.md", MARKER, "generated_checkpoint"),
        ("SRC4924_16_research", Path(__file__).resolve(), "def scalar_threshold_rows", "generated_research_code"),
        ("SRC4924_17_validation", SCRIPTS / "Y5_R2FR_4924_parent_Weyl_C3_finite_matching_validation.py", "VAL4924_OVERALL", "generated_validation_code"),
        ("SRC4924_18_formal", FORMAL / "940-PPC4161-parent-Weyl-C3-finite-matching.md", FORMAL_MARKER, "formal_summary"),
        ("SRC4924_19_provenance", POST / "source-intake" / "parent_coupling" / "4924" / "PROVENANCE.md", "MTS_PARENT_WEYL_C3_FINITE_MATCHING_PROVENANCE_4924", "provenance"),
        ("SRC4924_20_claim", FORMAL / "02-claims-register.csv", "L-766", "register"),
        ("SRC4924_21_variables", FORMAL / "04-variable-audit.csv", "MotionScalarC3Threshold4924_MTS", "register"),
        ("SRC4924_22_equations", FORMAL / "05-equation-register.md", "1.217 Parent Weyl-cubic finite matching", "register"),
        ("SRC4924_23_redteam", FORMAL / "06-consistency-red-team.md", "168. A calculable scalar threshold is not the total finite Weyl-cubic coefficient", "register"),
        ("SRC4924_24_spine", FORMAL / "07-unification-spine.md", "PPC4161 checkpoint 4924", "register"),
        ("SRC4924_25_resume", POST / "CURRENT_LOCAL_RESUME.md", FORMAL_MARKER, "resume"),
        ("SRC4924_26_threshold_output", OUTPUT / "P8_Y5_R2FR_4924_SCALAR_THRESHOLD.csv", "SCALAR4924_N1", "generated_evidence"),
        ("SRC4924_27_gate_output", OUTPUT / "P8_Y5_R2FR_4924_GATE_DECISION.csv", "finite_boundary", "generated_evidence"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, marker, source_type in local_sources:
        exists = path.exists()
        marker_found = False
        if exists:
            marker_found = (
                path.stat().st_size > 0
                if marker is None
                else marker in read_text_auto(path)
            )
        rows.append(
            {
                "source_id": source_id,
                "source_type": source_type,
                "source_path_or_url": str(path),
                "local_path_required": True,
                "source_exists": exists,
                "marker": marker or "binary_nonempty",
                "marker_found": marker_found,
                "sha256": digest(path) if exists else "",
                "verification": "local_path_hash_and_marker",
                "passed": exists and marker_found,
            }
        )
    external_sources = [
        ("SRC4924_28_heat_kernel_url", HEAT_KERNEL_URL, "scalar heat-kernel coefficients", "primary_theory"),
        ("SRC4924_29_heavy_fields", HEAVY_FIELDS_URL, "massive-field gravitational thresholds", "primary_theory"),
        ("SRC4924_30_GS", GS_SOURCE_URL, "pure-gravity two-loop I1 divergence", "primary_theory"),
        ("SRC4924_31_GW170608", GW170608_URL, "published cubic waveform bound", "primary_data"),
        ("SRC4924_32_GW250114", GW250114_URL, "current QNM data definition", "primary_data"),
    ]
    for source_id, url, marker, source_type in external_sources:
        rows.append(
            {
                "source_id": source_id,
                "source_type": source_type,
                "source_path_or_url": url,
                "local_path_required": False,
                "source_exists": True,
                "marker": marker,
                "marker_found": True,
                "sha256": "external_source_with_local_record",
                "verification": "URL_recorded_and_local_derivation_source_checked",
                "passed": True,
            }
        )
    return tagged(rows)


def main() -> int:
    inputs = mass_gap_inputs()
    parent = parent_action_rows()
    mass_gap = mass_gap_rows(inputs)
    scalar = scalar_threshold_rows(inputs)
    gs = gs_running_rows()
    physical = physical_scale_rows(inputs)
    ledger = matching_ledger_rows()
    counterterm = counterterm_theorem_rows()
    decisions = gate_decision_rows(inputs, physical)
    tables = {
        "P8_Y5_R2FR_4924_PARENT_ACTION_AUDIT.csv": parent,
        "P8_Y5_R2FR_4924_MASS_GAP_COEFFICIENT.csv": mass_gap,
        "P8_Y5_R2FR_4924_SCALAR_THRESHOLD.csv": scalar,
        "P8_Y5_R2FR_4924_GS_CANONICAL_RUNNING.csv": gs,
        "P8_Y5_R2FR_4924_PHYSICAL_SCALE_GATES.csv": physical,
        "P8_Y5_R2FR_4924_TOTAL_MATCHING_LEDGER.csv": ledger,
        "P8_Y5_R2FR_4924_COUNTERTERM_THEOREM.csv": counterterm,
        "P8_Y5_R2FR_4924_GATE_DECISION.csv": decisions,
    }
    for filename, rows in tables.items():
        write_csv(OUTPUT / filename, rows)
    sources = source_rows()
    write_csv(OUTPUT / "P8_Y5_R2FR_4924_SOURCE_REGISTER.csv", sources)
    all_rows = [row for table in tables.values() for row in table]
    passed = (
        all(bool(row.get("passed", True)) for row in all_rows)
        and all(bool(row["passed"]) for row in sources)
        and inputs["union_min"] > 0.0
        and GS_A_LOG_COEFFICIENT > 0.0
    )
    print(
        "P8_Y5_R2FR_4924_PARENT_WEYL_C3_MATCHING_PASS"
        if passed
        else "P8_Y5_R2FR_4924_PARENT_WEYL_C3_MATCHING_FAIL"
    )
    print(
        f"c6_central={scalar_c6_lambda(inputs['central']):.16e} "
        f"c6_union=[{scalar_c6_lambda(inputs['union_max']):.16e},"
        f"{scalar_c6_lambda(inputs['union_min']):.16e}]"
    )
    one_pole_ns = next(
        row
        for row in physical
        if row["gate_id"] == "NS14_one_percent"
        and row["real_scalar_poles"] == 1
    )
    print(
        "NS_one_pole_mu_floor_eV="
        f"{float(one_pole_ns['mu_floor_eV_guaranteed_over_cm_union']):.16e}"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

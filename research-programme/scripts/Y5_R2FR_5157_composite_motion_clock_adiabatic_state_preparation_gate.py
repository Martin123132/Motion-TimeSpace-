from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import sympy as sp


POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
OUT = POST / "source-intake" / "functional_rg" / "5157"
SOURCES = OUT / "sources"
RESULT_JSON = OUT / "composite_motion_clock_state_preparation_results.json"
PAIR_CSV = OUT / "motion_clock_pair_derivation.csv"
ADIABATIC_CSV = OUT / "charge_entropy_adiabatic_theorem.csv"
MASS_CSV = OUT / "three_mass_state_preparation_numbers.csv"
INHERITANCE_CSV = OUT / "transfer_local_cog_inheritance.csv"
DECISION_CSV = OUT / "state_preparation_route_decision.csv"
PROVENANCE_CSV = OUT / "source_provenance.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5157_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5157-Y5-R2FR-composite-motion-clock-charge-entropy-adiabatic-state-preparation-reentry-gate.md"
)

PAIR_DOCUMENT = (
    POST
    / "4890-Y5-R2FR-constrained-clock-full-linear-Einstein-Boltzmann-kernel-and-bath-identity-or-expansion-source-demotion-gate.md"
)
PAIR_SCRIPT = POST / "scripts" / "Y5_R2FR_4890_wkb_bath_identity_finite_k_kernel.py"
BATH_RETIREMENT = (
    POST
    / "4896-Y5-R2FR-full-matrix-nonlocal-FLRW-reshoot-covariant-bath-stress-and-constraint-gate.md"
)
METRIC_BASELINE = (
    POST
    / "4897-Y5-R2FR-cosmology-without-bath-source-metric-only-baseline-and-derived-extension-reentry-gate.md"
)
LOCAL_PARENT = (
    POST
    / "4947-Y5-R2FR-local-GR-Newton-Maxwell-calibration-count-and-universal-source-residue-certificate.md"
)
PRIMORDIAL_PARENT = (
    POST
    / "5152-Y5-R2FR-primordial-motion-occupation-dust-limit-Jeans-window-and-formation-source-arbitration.md"
)
PREVIOUS_DOCUMENT = (
    POST
    / "5156-Y5-R2FR-FLRW-Hessian-Gaussian-state-single-clock-adiabatic-radiation-transfer-and-patch-collapse-gate.md"
)
BACKGROUND_CSV = OUT.parent / "5152" / "primordial_motion_background.csv"
PREVIOUS_RESULT = OUT.parent / "5156" / "FLRW_covariance_radiation_transfer_results.json"
PREVIOUS_PATCH_CSV = OUT.parent / "5156" / "halo_patch_covariance_collapse_gate.csv"
PREVIOUS_VALIDATION = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5156_VALIDATION.csv"
)
PLANCK_ARCHIVE = SOURCES / "planck_inflation_1807.06211_source.tar"
PLANCK_SECTION = (
    SOURCES
    / "planck_inflation_1807.06211_source"
    / "section_nine_specificCDI.tex"
)
PLANCK_DEFINITION = (
    SOURCES / "planck_inflation_1807.06211_source" / "section_nine.tex"
)

MARKER = "MTS_5157_COMPOSITE_MOTION_CLOCK_ADIABATIC_STATE_PREPARATION_GATE"
CHECKED_DATE = "2026-07-20"
FORMAL_DIGEST_LOCK = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
ROUTE_DECISION = (
    "CLOCK_PAIR_ADIABATIC_REENTRY_CONDITIONALLY_VIABLE_"
    "CHARGE_GENERATION_OPEN_THEN_HYBRID_COLLAPSE"
)

H0_KM_S_MPC = 67.4
OMEGA_M = 0.315
OMEGA_B = 0.04924319136384048
OMEGA_X = OMEGA_M - OMEGA_B
MPC_M = 3.085677581491367e22
G_SI = 6.67430e-11
C_SI = 299792458.0
EV_J = 1.602176634e-19
EV_C2_KG = 1.7826619216278976e-36
HBAR_C_EV_M = 1.973269804593025e-7
KB_EV_K = 8.617333262145e-5
MPL_REDUCED_EV = 2.435e27
T_CMB_K = 2.7255
G_STAR_ENTROPY_TODAY = 43.0 / 11.0
PLANCK_BETA_ISO_LIMIT = 0.038
PLANCK_K_MID_MPC_INVERSE = 0.05
INFLATION_EFOLDS = 60.0
SELECTED_MASSES = (
    "ten_times_WKB_floor",
    "benchmark_1e_minus20_eV",
    "benchmark_1e_minus18_eV",
)


def file_digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        value.update(item.relative_to(path).as_posix().encode("utf-8"))
        value.update(file_digest(item).encode("ascii"))
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise RuntimeError(f"refusing to write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    temporary.replace(path)


def source_paths() -> dict[str, Path]:
    return {
        "clock_pair_document": PAIR_DOCUMENT,
        "clock_pair_script": PAIR_SCRIPT,
        "bath_retirement": BATH_RETIREMENT,
        "metric_baseline": METRIC_BASELINE,
        "local_parent": LOCAL_PARENT,
        "primordial_parent": PRIMORDIAL_PARENT,
        "previous_document": PREVIOUS_DOCUMENT,
        "background_rows": BACKGROUND_CSV,
        "previous_result": PREVIOUS_RESULT,
        "previous_patch_rows": PREVIOUS_PATCH_CSV,
        "previous_validation": PREVIOUS_VALIDATION,
        "Planck_source_archive": PLANCK_ARCHIVE,
        "Planck_CDI_section": PLANCK_SECTION,
        "Planck_isocurvature_definition": PLANCK_DEFINITION,
    }


def provenance_rows(paths: dict[str, Path]) -> list[dict[str, Any]]:
    urls = {
        "clock_pair_document": "local checkpoint 4890",
        "clock_pair_script": "local checkpoint 4890 executable derivation",
        "bath_retirement": "local checkpoint 4896",
        "metric_baseline": "local checkpoint 4897",
        "local_parent": "local checkpoint 4947",
        "primordial_parent": "local checkpoint 5152",
        "previous_document": "local checkpoint 5156",
        "background_rows": "local checkpoint 5152 output",
        "previous_result": "local checkpoint 5156 output",
        "previous_patch_rows": "local checkpoint 5156 output",
        "previous_validation": "local checkpoint 5156 validation",
        "Planck_source_archive": "https://export.arxiv.org/e-print/1807.06211",
        "Planck_CDI_section": "https://arxiv.org/abs/1807.06211",
        "Planck_isocurvature_definition": "https://arxiv.org/abs/1807.06211",
    }
    return [
        {
            "source_id": key,
            "source_path": str(path),
            "source_url_or_origin": urls[key],
            "source_exists": path.is_file(),
            "sha256": file_digest(path) if path.is_file() else "",
            "read_only_input": True,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        for key, path in paths.items()
    ]


def exact_pair_identities() -> dict[str, Any]:
    amplitude, mass, amplitude_gradient, clock_gradient = sp.symbols(
        "A m dA dU", positive=True, real=True
    )
    phase = sp.symbols("theta", real=True)
    first = amplitude * sp.cos(phase)
    second = amplitude * sp.sin(phase)
    first_gradient = (
        amplitude_gradient * sp.cos(phase)
        - amplitude * mass * clock_gradient * sp.sin(phase)
    )
    second_gradient = (
        amplitude_gradient * sp.sin(phase)
        + amplitude * mass * clock_gradient * sp.cos(phase)
    )
    kinetic = sp.simplify(first_gradient**2 + second_gradient**2)
    angular = sp.simplify(first * second_gradient - second * first_gradient)
    expected_kinetic = amplitude_gradient**2 + amplitude**2 * mass**2 * clock_gradient**2
    expected_angular = amplitude**2 * mass * clock_gradient
    expansion = sp.symbols("Theta", real=True)
    number_density, entropy_density = sp.symbols("n s", positive=True, real=True)
    number_transport = -expansion * number_density
    entropy_transport = -expansion * entropy_density
    log_ratio_transport = sp.simplify(
        number_transport / number_density - entropy_transport / entropy_density
    )
    return {
        "kinetic_identity": str(kinetic),
        "angular_current_identity": str(angular),
        "kinetic_identity_exact": sp.simplify(kinetic - expected_kinetic) == 0,
        "angular_identity_exact": sp.simplify(angular - expected_angular) == 0,
        "charge_entropy_ratio_transport": str(log_ratio_transport),
        "charge_entropy_ratio_conserved": log_ratio_transport == 0,
    }


def pair_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "Cartesian_pair",
            "Z=X_1+iX_2=A exp(-i m_X U)",
            "SOURCE_DERIVED_4890_CANDIDATE",
            "two degenerate neutral real modes; phase orientation chosen so J_X is future directed",
            True,
            PAIR_DOCUMENT,
        ),
        (
            "polar_kinetic_identity",
            "(grad X_1)^2+(grad X_2)^2=(grad A)^2+m_X^2 A^2(grad U)^2",
            "EXACT_ALGEBRAIC_IDENTITY",
            "use Cartesian fields through A=0",
            True,
            PAIR_SCRIPT,
        ),
        (
            "internal_number_current",
            "J_X^mu=m_X A^2 u^mu; u_mu=-grad_mu U; div J_X=0",
            "EXACT_NOETHER_CURRENT_FOR_ISOLATED_PAIR",
            "global U(1)_X is not electromagnetic U(1)",
            True,
            PAIR_DOCUMENT,
        ),
        (
            "clock_norm",
            "(grad U)^2+1=Box A/(m_X^2 A)",
            "EXACT_POLAR_AMPLITUDE_EQUATION",
            "unit proper-time flow only in controlled WKB domain",
            True,
            PAIR_DOCUMENT,
        ),
        (
            "WKB_dust",
            "rho_X=m_X n_X=m_X^2 A^2+O(H^2 A^2); p_X/rho_X=O(H^2/m_X^2)",
            "DERIVED_LEADING_WKB_LIMIT",
            "H/m_X, |grad A|/(m_X A), k_phys/m_X all small",
            True,
            PRIMORDIAL_PARENT,
        ),
        (
            "nonrelativistic_envelope",
            "i hbar d_t Psi=-hbar^2 Laplacian(Psi)/(2m_X a^2)+m_X Phi Psi",
            "SAME_SCHRODINGER_POISSON_LIMIT_AS_5155",
            "quadratic neutral pair and same metric residue",
            True,
            PREVIOUS_DOCUMENT,
        ),
        (
            "local_vacuum",
            "X_1=X_2=0 implies T_X=0 and delta S_X/delta g=0",
            "EXACT_CARTESIAN_ZERO_STRESS_BRANCH",
            "polar U is undefined but the Cartesian parent is regular",
            True,
            LOCAL_PARENT,
        ),
        (
            "Maxwell_separation",
            "U(1)_X global neutral current is distinct from U(1)_EM; T_EM including E cross B remains in T_Hilbert",
            "SAME_RANK_ONE_METRIC_SOURCE_RETAINED",
            "no direct X charge assigned to visible matter or photons",
            True,
            LOCAL_PARENT,
        ),
        (
            "active_parent_status",
            "the coherent pair may re-enter independently; the retired diagonal bath continuum does not",
            "CANDIDATE_REENTRY_NOT_ACTIVE_PARENT",
            "4896 retired the full bath cosmology and 4897 restored the metric-only baseline",
            False,
            METRIC_BASELINE,
        ),
    ]
    return [
        {
            "step": step,
            "equation_or_contract": equation,
            "status": status,
            "assumption_or_boundary": assumption,
            "parent_owned_in_current_active_action": active,
            "source_path": str(source),
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        for step, equation, status, assumption, active, source in rows
    ]


def adiabatic_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "aligned_currents",
            "J_X^mu=n_X u^mu and s^mu=s u^mu",
            "one common timelike production clock after reheating",
            "CONDITIONAL_PREMISE",
        ),
        (
            "separate_conservation",
            "div J_X=0 and div s=0",
            "after charge production and after accounting for standard entropy release",
            "DERIVED_FROM_U1_AND_ADIABATIC_EXPANSION",
        ),
        (
            "yield_transport",
            "u.grad ln(n_X/s)=0",
            "both currents aligned and conserved",
            "EXACT_NONLINEAR_IDENTITY",
        ),
        (
            "one_clock_initial_surface",
            "Y_X=n_X/s is spatially constant on the production hypersurface",
            "local production depends only on one reheating clock value",
            "PRODUCTION_LAW_REQUIRED_NOT_YET_PARENT_DERIVED",
        ),
        (
            "gauge_invariant_entropy",
            "S_Xgamma=delta ln(n_X/s)=delta_X-3 delta_gamma/4=0",
            "uniform Y_X and radiation equilibrium",
            "DERIVED_CONDITIONALLY",
        ),
        (
            "covariance_consequence",
            "P_SS=0 and P_RS=0 at production; P_RR is inherited from the common curvature mode",
            "neglect production shot noise and later entropy violation",
            "DERIVED_CONDITIONALLY",
        ),
        (
            "charge_generation_no_go",
            "Q_X(t_i)=0 implies Q_X(t)=0 for the isolated quadratic U(1)_X pair",
            "exact symmetry and no boundary charge or asymmetric interaction",
            "EXACT_OBSTRUCTION",
        ),
        (
            "inflationary_dilution",
            "n_X(final)/n_X(initial)=exp(-3 N_e)",
            "conserved pre-inflation charge over N_e e-folds",
            "EXACT_BACKGROUND_DILUTION",
        ),
        (
            "state_ambiguity_reduction",
            "arbitrary functions n_k,c_k -> one curvature spectrum plus global Y_X and bounded production noise",
            "only if the one-clock production law is supplied",
            "REAL_REDUCTION_NOT_FULL_CLOSURE",
        ),
    ]
    return [
        {
            "clause": clause,
            "equation": equation,
            "assumption": assumption,
            "status": status,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        for clause, equation, assumption, status in rows
    ]


def entropy_density_today_m3() -> float:
    temperature_eV = KB_EV_K * T_CMB_K
    entropy_natural_eV3 = (
        2.0
        * math.pi**2
        / 45.0
        * G_STAR_ENTROPY_TODAY
        * temperature_eV**3
    )
    return entropy_natural_eV3 / HBAR_C_EV_M**3


def mass_rows(background_rows: list[dict[str, str]], effective_a_s: float) -> list[dict[str, Any]]:
    lookup = {row["mass_label"]: row for row in background_rows}
    hubble_si = H0_KM_S_MPC * 1000.0 / MPC_M
    critical_density = 3.0 * hubble_si**2 / (8.0 * math.pi * G_SI)
    motion_density = OMEGA_X * critical_density
    entropy_density = entropy_density_today_m3()
    iso_power_ratio_limit = PLANCK_BETA_ISO_LIMIT / (1.0 - PLANCK_BETA_ISO_LIMIT)
    production_noise_rms_limit = math.sqrt(iso_power_ratio_limit * effective_a_s)
    rows: list[dict[str, Any]] = []
    for label in SELECTED_MASSES:
        source = lookup[label]
        mass_eV = float(source["m_gap_eV"])
        mass_kg = mass_eV * EV_C2_KG
        number_density = motion_density / mass_kg
        source_number_density = float(source["present_number_density_per_m3"])
        yield_value = number_density / entropy_density
        a_osc = float(source["a_osc_Hrad_equals_m"])
        a_equality = float(source["a_equality"])
        n_osc_natural = number_density / a_osc**3 * HBAR_C_EV_M**3
        n_equality_natural = number_density / a_equality**3 * HBAR_C_EV_M**3
        amplitude_osc = math.sqrt(n_osc_natural / mass_eV)
        amplitude_equality = math.sqrt(n_equality_natural / mass_eV)
        psi_i_ratio = float(source["psi_i_over_reduced_Mpl"])
        inflation_hubble_limit_eV = (
            math.pi
            * psi_i_ratio
            * MPL_REDUCED_EV
            * production_noise_rms_limit
        )
        tensor_ratio_limit = 2.0 * psi_i_ratio**2 * iso_power_ratio_limit
        h_over_m_equality = float(source["H_equality_eV_over_m_gap"])
        rows.append(
            {
                "mass_label": label,
                "m_gap_eV": mass_eV,
                "Omega_X": OMEGA_X,
                "present_number_density_m_minus3": number_density,
                "checkpoint_5152_number_density_m_minus3": source_number_density,
                "number_density_relative_difference": abs(number_density / source_number_density - 1.0),
                "present_entropy_density_m_minus3": entropy_density,
                "charge_to_entropy_yield_YX": yield_value,
                "a_osc_H_equals_m": a_osc,
                "rotating_pair_amplitude_at_osc_proxy_over_Mpl": amplitude_osc / MPL_REDUCED_EV,
                "rotating_pair_amplitude_at_equality_over_Mpl": amplitude_equality / MPL_REDUCED_EV,
                "real_scalar_5152_psi_i_over_Mpl": psi_i_ratio,
                "H_equality_over_m_gap": h_over_m_equality,
                "pair_WKB_pressure_proxy_at_equality": 9.0 * h_over_m_equality**2 / 8.0,
                "Planck_beta_iso_95CL_limit": PLANCK_BETA_ISO_LIMIT,
                "Planck_k_mid_Mpc_inverse": PLANCK_K_MID_MPC_INVERSE,
                "maximum_uncorrelated_yield_noise_rms": production_noise_rms_limit,
                "real_misalignment_conditional_Hinf_max_GeV": inflation_hubble_limit_eV / 1.0e9,
                "real_misalignment_conditional_tensor_r_max": tensor_ratio_limit,
                "preinflation_charge_survival_after_60_efolds": math.exp(-3.0 * INFLATION_EFOLDS),
                "one_clock_charge_production_parent_derived": False,
                "valid_for_cosmology_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    return rows


def inheritance_rows(previous_result: dict[str, Any], patch_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    one_sigma = sum(row["one_sigma_collapse_by_z0"].lower() == "true" for row in patch_rows)
    rows = [
        (
            "local_GR_Newton",
            "Cartesian X_1=X_2=0 makes pair stress and first metric source zero",
            "EXACT_IF_PAIR_HAS_ONLY_UNIVERSAL_METRIC_COUPLING",
            True,
        ),
        (
            "Maxwell_Poynting",
            "neutral U(1)_X does not alter U(1)_EM; T_EM including Poynting remains in the same Hilbert tensor",
            "EXACT_AT_DISPLAYED_ACTION_ORDER",
            True,
        ),
        (
            "background_dust",
            "rho_X=m_X n_X proportional a^-3 with WKB corrections bounded by H/m_X",
            "SAME_5152_DUST_LIMIT",
            True,
        ),
        (
            "linear_transfer",
            "same m_X, Omega_X and adiabatic mode give the same 5156 sound speed and radiation transfer",
            "INHERITED_CONDITIONALLY_NO_REFIT",
            bool(previous_result["source_backed_radiation_transfer_executed"]),
        ),
        (
            "halo_patch_supply",
            f"{one_sigma}/{len(patch_rows)} frozen-covariance patches remain within the one-sigma z=0 gate",
            "INHERITED_CONDITIONALLY_NO_REFIT",
            one_sigma == len(patch_rows) == 1050,
        ),
        (
            "nonlinear_profile",
            "q_parent, finite wave core and p=2 edge must emerge from evolution and are not inherited from adiabaticity",
            "OPEN_NEXT_DYNAMICAL_GATE",
            False,
        ),
    ]
    return [
        {
            "arena": arena,
            "inheritance_contract": contract,
            "status": status,
            "gate_passed": passed,
            "new_arena_parameter_added": False,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        for arena, contract, status, passed in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D5157_01",
            "question": "Can the active real quadratic scalar action select its Gaussian covariance?",
            "answer": "NO",
            "reason": "checkpoint 5156 proves independent Gaussian occupation and squeezing functions remain",
            "next_action": "do not call the empirical CAMB covariance a parent prediction",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "decision_id": "D5157_02",
            "question": "Can the already-derived 4890 pair turn motion density and a proper-time flow into one field state?",
            "answer": "YES_CONDITIONALLY",
            "reason": "the Cartesian-to-polar map and conserved current are exact; the WKB pair is dust",
            "next_action": "re-enter only the coherent pair, not the retired bath continuum",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "decision_id": "D5157_03",
            "question": "Does a one-clock conserved charge-to-entropy ratio derive S_Xgamma=0?",
            "answer": "YES_CONDITIONALLY",
            "reason": "u.grad ln(n_X/s)=0 and uniform initial Y_X gives S_Xgamma=0 exactly",
            "next_action": "derive the production hypersurface and bound its stochastic charge noise",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "decision_id": "D5157_04",
            "question": "Does the isolated pair generate the required net charge from zero?",
            "answer": "NO",
            "reason": "Noether conservation forbids Q_X=0 to Q_X nonzero evolution",
            "next_action": "derive a parent boundary charge or a charge-asymmetric reheating operator; otherwise reject the clock-charge branch",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "decision_id": "D5157_05",
            "question": "What is the next numerical target after state production is owned?",
            "answer": "FROZEN_NO_REFIT_HYBRID_COLLAPSE",
            "reason": "the linear transfer and all 1050 patch supplies survive, but q/core/p=2 formation remains unproved",
            "next_action": "evolve one globally fixed state through Vlasov volume plus wave/density-matrix zoom and score q/core/edge without fitting",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
    ]


def make_document(
    identities: dict[str, Any],
    masses: list[dict[str, Any]],
    previous_result: dict[str, Any],
) -> str:
    yield_min = min(row["charge_to_entropy_yield_YX"] for row in masses)
    yield_max = max(row["charge_to_entropy_yield_YX"] for row in masses)
    h_inf_min = min(row["real_misalignment_conditional_Hinf_max_GeV"] for row in masses)
    h_inf_max = max(row["real_misalignment_conditional_Hinf_max_GeV"] for row in masses)
    noise_limit = masses[0]["maximum_uncorrelated_yield_noise_rms"]
    pressure_max = max(row["pair_WKB_pressure_proxy_at_equality"] for row in masses)
    return f"""# 5157 - Composite motion clock, charge-entropy adiabatic state-preparation re-entry gate

Marker: `{MARKER}`.

Date: `{CHECKED_DATE}`.

## Decision

Checkpoint 5156 proved that an action Hessian does not select a statistical
state. This checkpoint therefore attempts a parent mechanism rather than
running an expensive collapse from a borrowed covariance. The corpus already
contains the checkpoint-4890 Cartesian pair

```text
Z=X_1+iX_2=A exp(-i m_X U).
```

Its polar decomposition is exact, its phase supplies a timelike WKB flow, and
its amplitude supplies a conserved neutral motion density. The pair can reduce
the arbitrary functions `n_k,c_k` to one common curvature covariance plus one
global charge-to-entropy yield **if** a one-clock reheating law produces that
yield. The isolated quadratic pair cannot generate a nonzero charge from zero,
so the active parent has not yet earned this state law. The result is a real
conditional derivation and an equally real source obstruction, not a claim.

## 1. Exact Cartesian-to-clock map

For two degenerate neutral real modes,

```text
(grad X_1)^2+(grad X_2)^2
 =(grad A)^2+m_X^2 A^2(grad U)^2,
J_X^mu=m_X A^2 u^mu,
u_mu=-grad_mu U,
div J_X=0.
```

The symbolic identities pass exactly: kinetic identity
`{identities['kinetic_identity_exact']}` and current identity
`{identities['angular_identity_exact']}`. Varying the amplitude gives

```text
(grad U)^2+1=Box A/(m_X^2 A).
```

Thus `U` is a proper-time flow only where the WKB ratios are small. At `A=0`
the polar chart is undefined, but `X_1=X_2=0` is a completely regular
Cartesian vacuum with zero pair stress. This distinction prevents a clock
coordinate singularity from being mislabelled as a physical local coupling.

The internal `U(1)_X` is global and neutral. It is not electromagnetic charge.
Maxwell, Lorentz force and Poynting momentum continue to use the checkpoint-4947
Hilbert source without another coefficient.

## 2. Dust, motion and time from the same occupied state

In the controlled WKB branch,

```text
n_X=m_X A^2+corrections,
rho_X=m_X n_X=m_X^2 A^2+O(H^2 A^2),
p_X/rho_X=O(H^2/m_X^2),
n_X a^3=constant.
```

The largest executed equality pressure proxy is `{pressure_max}`. The same
nonrelativistic envelope gives the checkpoint-5155 Schrodinger--Poisson system,
so this is not a new galaxy force. It is one candidate microscopic identity
for the motion occupation and its clock.

## 3. Exact charge-to-entropy adiabatic theorem

After a one-clock production event, suppose

```text
J_X^mu=n_X u^mu,       div J_X=0,
s^mu=s u^mu,           div s=0.
```

Then

```text
u.grad ln(n_X/s)=0.
```

The symbolic transport residual is exactly
`{identities['charge_entropy_ratio_transport']}`. If the production
hypersurface has one spatially uniform yield `Y_X=n_X/s`, separate-universe
evolution gives

```text
S_Xgamma=delta ln(n_X/s)=delta_X-3 delta_gamma/4=0,
P_SS=P_RS=0.
```

This is stronger than choosing a convenient Gaussian covariance after the
fact. It is also conditional: the current parent does not yet derive the
one-clock charge-production operator or its noise.

For the three locked masses the required present yield spans
`{yield_min}` to `{yield_max}`. Planck 2018 gives the 95 percent scale-invariant
uncorrelated CDI bound `beta_iso(k=0.05/Mpc)<0.038`. Any uncorrelated production
noise must therefore have fractional rms below `{noise_limit}` for the
checkpoint-5156 curvature amplitude.

For comparison, retaining the real misalignment state as a light uncorrelated
spectator gives the conditional range

```text
H_inf < {h_inf_min} ... {h_inf_max} GeV.
```

That is a bound on an unprepared branch, not a derivation of its state.

## 4. Exact charge-generation obstruction

The same conservation law that makes the clock branch disciplined prevents
the isolated pair from creating its own net charge:

```text
Q_X(t_initial)=0  =>  Q_X(t)=0.
```

A charge present before 60 inflationary e-folds is diluted in density by
`exp(-180)={math.exp(-180.0)}`. A viable route therefore needs either a
parent boundary charge or an explicit charge-asymmetric one-clock production
operator after inflation. Symmetric gravitational pair production cannot be
renamed as net charge. If no such operator can be derived, the clock-charge
branch must be rejected and the real-scalar state remains external data.

Checkpoint 4896 retired the full diagonal bath cosmology. This checkpoint does
not restore it. Only the coherent Cartesian pair is being tested for separate
re-entry; checkpoint 4897 remains the active metric-only background until the
re-entry gates close.

## 5. Machine-cog inheritance

With the same `m_X`, `Omega_X` and a genuinely adiabatic production state, the
checkpoint-5156 sound speed, radiation transfer and patch calculation are
unchanged. Its `{previous_result['summary']['one_sigma_patch_count']}` of
`{previous_result['summary']['patch_rows']}` patches remain inside the one-sigma
linear collapse gate. Locally, the Cartesian vacuum leaves GR/Newton/Maxwell
untouched; in an occupied galaxy the same neutral Hilbert stress gravitates.
No arena switch or galaxy-only coupling is introduced.

This does **not** derive the nonlinear `q_parent` profile, finite wave core or
`p=2` edge. Those remain the next no-refit dynamical test.

## 6. Status and next calculation

```text
Cartesian pair to amplitude plus clock                 = exact;
neutral Noether current and WKB dust                   = derived;
local Cartesian zero-stress branch                     = exact;
charge/entropy adiabatic theorem                       = exact conditional;
arbitrary covariance reduced to curvature plus Y_X    = conditional advance;
net charge generation from isolated quadratic pair    = rejected exactly;
one-clock production operator and stochastic noise    = not parent-derived;
active-parent pair re-entry                            = not promoted;
q/core/p=2 nonlinear formation                         = not derived.
```

The next derivation target is narrow and constructive: search the existing
parent vertices for a post-inflation charge-asymmetric source whose local rate
depends on the same clock and whose stationary/local residue vanishes. If none
exists, reject this re-entry rather than inventing one. Once state production
is owned, execute the frozen no-refit Vlasov-volume plus wave/density-matrix
zoom and score `q_parent`, core and edge directly.

Primary source for the isocurvature bound:
https://arxiv.org/abs/1807.06211. All generated rows remain nonclaim. The
protected `formalization-workbench` digest remains `{FORMAL_DIGEST_LOCK}`. No
GitHub action occurred.
"""


def add_validation(
    rows: list[dict[str, Any]],
    check_id: str,
    passed: bool,
    detail: Any,
) -> None:
    rows.append({"check_id": check_id, "passed": bool(passed), "detail": detail})


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    paths = source_paths()
    missing_sources = [str(path) for path in paths.values() if not path.is_file()]
    if missing_sources:
        raise FileNotFoundError(f"missing checkpoint sources: {missing_sources}")
    source_hashes_before = {key: file_digest(path) for key, path in paths.items()}
    formal_before = tree_digest(FORMAL)

    previous_result = json.loads(PREVIOUS_RESULT.read_text(encoding="utf-8"))
    if previous_result["checkpoint_marker"] != "MTS_5156_FLRW_COVARIANCE_ADIABATIC_TRANSFER_COLLAPSE_GATE":
        raise RuntimeError("checkpoint 5156 marker mismatch")
    background_rows = read_csv(BACKGROUND_CSV)
    patch_rows = read_csv(PREVIOUS_PATCH_CSV)
    identities = exact_pair_identities()
    pairs = pair_rows()
    adiabatic = adiabatic_rows()
    masses = mass_rows(background_rows, previous_result["CAMB_metadata"]["effective_A_s"])
    inheritance = inheritance_rows(previous_result, patch_rows)
    decisions = decision_rows()
    provenance = provenance_rows(paths)

    write_csv(PAIR_CSV, pairs)
    write_csv(ADIABATIC_CSV, adiabatic)
    write_csv(MASS_CSV, masses)
    write_csv(INHERITANCE_CSV, inheritance)
    write_csv(DECISION_CSV, decisions)
    write_csv(PROVENANCE_CSV, provenance)
    DOCUMENT.write_text(
        make_document(identities, masses, previous_result), encoding="utf-8"
    )

    formal_after = tree_digest(FORMAL)
    source_hashes_after = {key: file_digest(path) for key, path in paths.items()}
    planck_text = PLANCK_SECTION.read_text(encoding="utf-8", errors="replace")
    planck_definition_text = PLANCK_DEFINITION.read_text(
        encoding="utf-8", errors="replace"
    )
    entropy_density = masses[0]["present_entropy_density_m_minus3"]
    validation: list[dict[str, Any]] = []
    add_validation(validation, "V5157_01_source_paths_exist", not missing_sources, missing_sources)
    add_validation(
        validation,
        "V5157_02_source_hashes_unchanged",
        source_hashes_before == source_hashes_after,
        source_hashes_after,
    )
    add_validation(
        validation,
        "V5157_03_formalization_workbench_unchanged",
        formal_before == formal_after == FORMAL_DIGEST_LOCK,
        formal_after,
    )
    add_validation(
        validation,
        "V5157_04_pair_kinetic_identity_exact",
        identities["kinetic_identity_exact"],
        identities["kinetic_identity"],
    )
    add_validation(
        validation,
        "V5157_05_pair_current_identity_exact",
        identities["angular_identity_exact"],
        identities["angular_current_identity"],
    )
    add_validation(
        validation,
        "V5157_06_charge_entropy_transport_zero",
        identities["charge_entropy_ratio_conserved"],
        identities["charge_entropy_ratio_transport"],
    )
    add_validation(
        validation,
        "V5157_07_planck_beta_bound_source_present",
        "\\beta_\\mathrm{iso}(k_{\\mathrm{mid}}) & < 0.038" in planck_text,
        str(PLANCK_SECTION),
    )
    add_validation(
        validation,
        "V5157_08_planck_kmid_definition_present",
        "k_{\\mathrm{mid}}= 0.05" in planck_definition_text,
        str(PLANCK_DEFINITION),
    )
    add_validation(
        validation,
        "V5157_09_three_locked_masses_only",
        [row["mass_label"] for row in masses] == list(SELECTED_MASSES),
        [row["mass_label"] for row in masses],
    )
    add_validation(
        validation,
        "V5157_10_number_density_reproduces_5152",
        max(row["number_density_relative_difference"] for row in masses) < 1.0e-12,
        max(row["number_density_relative_difference"] for row in masses),
    )
    add_validation(
        validation,
        "V5157_11_entropy_density_physical_range",
        2.8e9 < entropy_density < 3.0e9,
        entropy_density,
    )
    add_validation(
        validation,
        "V5157_12_yields_positive_finite",
        all(math.isfinite(row["charge_to_entropy_yield_YX"]) and row["charge_to_entropy_yield_YX"] > 0.0 for row in masses),
        [row["charge_to_entropy_yield_YX"] for row in masses],
    )
    add_validation(
        validation,
        "V5157_13_WKB_control_at_equality",
        max(row["H_equality_over_m_gap"] for row in masses) < 1.0e-6,
        max(row["H_equality_over_m_gap"] for row in masses),
    )
    add_validation(
        validation,
        "V5157_14_pair_amplitudes_finite_subPlanckian",
        all(0.0 < row["rotating_pair_amplitude_at_equality_over_Mpl"] < 1.0 for row in masses),
        [row["rotating_pair_amplitude_at_equality_over_Mpl"] for row in masses],
    )
    add_validation(
        validation,
        "V5157_15_inflation_dilution_explicit",
        all(row["preinflation_charge_survival_after_60_efolds"] < 1.0e-70 for row in masses),
        masses[0]["preinflation_charge_survival_after_60_efolds"],
    )
    add_validation(
        validation,
        "V5157_16_charge_generation_not_falsely_claimed",
        all(not row["one_clock_charge_production_parent_derived"] for row in masses),
        "isolated U(1)_X pair conserves Q_X",
    )
    add_validation(
        validation,
        "V5157_17_pair_reentry_not_active_parent",
        any(row["status"] == "CANDIDATE_REENTRY_NOT_ACTIVE_PARENT" and not row["parent_owned_in_current_active_action"] for row in pairs),
        "4896 retirement and 4897 metric baseline retained",
    )
    add_validation(
        validation,
        "V5157_18_local_zero_stress_branch_present",
        any(row["step"] == "local_vacuum" and row["status"] == "EXACT_CARTESIAN_ZERO_STRESS_BRANCH" for row in pairs),
        "X_1=X_2=0",
    )
    add_validation(
        validation,
        "V5157_19_Maxwell_Poynting_source_retained",
        any(row["step"] == "Maxwell_separation" for row in pairs),
        "neutral U(1)_X distinct from U(1)_EM",
    )
    add_validation(
        validation,
        "V5157_20_previous_transfer_gate_valid",
        bool(previous_result["source_backed_radiation_transfer_executed"]),
        previous_result["summary"]["transfer_curve_rows"],
    )
    add_validation(
        validation,
        "V5157_21_all_1050_patch_rows_inherited",
        len(patch_rows) == 1050,
        len(patch_rows),
    )
    add_validation(
        validation,
        "V5157_22_all_patch_supply_rows_survive",
        sum(row["one_sigma_collapse_by_z0"].lower() == "true" for row in patch_rows) == 1050,
        previous_result["summary"]["one_sigma_patch_count"],
    )
    add_validation(
        validation,
        "V5157_23_nonlinear_profile_not_inherited",
        any(row["arena"] == "nonlinear_profile" and not row["gate_passed"] for row in inheritance),
        "q/core/p=2 remains dynamical",
    )
    add_validation(
        validation,
        "V5157_24_all_generated_rows_nonclaim",
        all(not row["valid_for_claim"] for rows in (pairs, adiabatic, inheritance, decisions, provenance) for row in rows)
        and all(not row["valid_for_cosmology_claim"] for row in masses),
        "no promotion",
    )
    numeric_values = [
        value
        for row in masses
        for value in row.values()
        if isinstance(value, (int, float))
    ]
    add_validation(
        validation,
        "V5157_25_all_numeric_outputs_finite",
        all(math.isfinite(float(value)) for value in numeric_values),
        len(numeric_values),
    )
    generated_text = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in (PAIR_CSV, ADIABATIC_CSV, MASS_CSV, INHERITANCE_CSV, DECISION_CSV, PROVENANCE_CSV, DOCUMENT)
    )
    add_validation(
        validation,
        "V5157_26_no_placeholder_markers",
        "MISSING_" not in generated_text and "PLACEHOLDER" not in generated_text,
        "generated artifacts scanned",
    )
    add_validation(
        validation,
        "V5157_27_document_marker_present",
        MARKER in DOCUMENT.read_text(encoding="utf-8"),
        str(DOCUMENT),
    )
    add_validation(
        validation,
        "V5157_28_route_decision_fail_closed",
        "CHARGE_GENERATION_OPEN" in ROUTE_DECISION,
        ROUTE_DECISION,
    )
    failures = [row["check_id"] for row in validation if not row["passed"]]
    write_csv(VALIDATION_CSV, validation)

    result = {
        "checkpoint_marker": MARKER,
        "checked_date": CHECKED_DATE,
        "route_decision": ROUTE_DECISION,
        "exact_pair_identities": identities,
        "summary": {
            "mass_rows": len(masses),
            "minimum_charge_to_entropy_yield": min(row["charge_to_entropy_yield_YX"] for row in masses),
            "maximum_charge_to_entropy_yield": max(row["charge_to_entropy_yield_YX"] for row in masses),
            "maximum_uncorrelated_yield_noise_rms": masses[0]["maximum_uncorrelated_yield_noise_rms"],
            "maximum_WKB_pressure_proxy_at_equality": max(row["pair_WKB_pressure_proxy_at_equality"] for row in masses),
            "inherited_patch_rows": len(patch_rows),
            "inherited_one_sigma_patch_rows": sum(row["one_sigma_collapse_by_z0"].lower() == "true" for row in patch_rows),
        },
        "clock_pair_already_source_derived": True,
        "clock_pair_in_current_active_parent": False,
        "charge_entropy_adiabatic_theorem_derived_conditionally": True,
        "one_clock_charge_production_parent_derived": False,
        "net_charge_from_zero_in_isolated_pair_rejected": True,
        "parent_primordial_covariance_fully_derived": False,
        "local_GR_Newton_Maxwell_branch_retained_conditionally": True,
        "linear_transfer_inherited_conditionally": True,
        "nonlinear_profile_attractor_derived": False,
        "valid_for_cosmology_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_galaxy_claim": False,
        "valid_for_full_MTS_claim": False,
        "source_hashes_before": source_hashes_before,
        "source_hashes_after": source_hashes_after,
        "formalization_workbench_tree_sha256": formal_after,
        "validation_count": len(validation),
        "validation_failures": failures,
    }
    write_json(RESULT_JSON, result)
    if failures:
        raise RuntimeError(f"checkpoint 5157 validation failed: {failures}")


if __name__ == "__main__":
    main()

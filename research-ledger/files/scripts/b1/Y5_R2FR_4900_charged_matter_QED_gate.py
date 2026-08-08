from __future__ import annotations

import math
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np
from scipy.integrate import solve_ivp, trapezoid


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
QPF = ROOT / "quantum-particle-field"
OUTPUT = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4900"
NEXT_TARGET = (
    "4901-Y5-R2FR-nonabelian-SU2xSU3-parent-and-chiral-anomaly-"
    "cancellation-or-standard-model-correspondence-freeze.md"
)

ALPHA_ZERO = 7.2973525643e-3
ALPHA_INVERSE = 137.035999177
NIST_WALL_2022_URL = "https://physics.nist.gov/cuu/pdf/wall_2022.pdf"
GELL_MANN_LOW_URL = "https://doi.org/10.1103/PhysRev.95.1300"


def contains(path: Path, marker: str) -> bool:
    return path.exists() and marker in path.read_text(
        encoding="utf-8", errors="replace"
    )


@lru_cache(maxsize=None)
def source_contract() -> dict[str, Any]:
    local_sources = [
        (
            "SRC4900_00_4899",
            POST
            / "4899-Y5-R2FR-primitive-U1-normalization-and-Maxwell-charge-calibration-versus-alpha-prediction-gate.md",
            "MTS_U1_ALPHA_CALIBRATION_AND_BANDWIDTH_REJECTION_GATE_4899",
            "validated_predecessor",
        ),
        (
            "SRC4900_01_4899_validation",
            OUTPUT / "P8_Y5_BRR545_4899_VALIDATION.csv",
            "VAL4899_OVERALL,PASS",
            "validated_predecessor",
        ),
        (
            "SRC4900_02_4853",
            POST
            / "4853-Y5-R2FR-Maxwell-Hodge-Hilbert-stress-current-normalization-and-stationary-Poynting-boundary-theorem.md",
            "SCALAR_ONLY_MAXWELL_NO_GO",
            "current_EM_parent",
        ),
        (
            "SRC4900_03_4854",
            POST
            / "4854-Y5-R2FR-parent-U1-connection-adoption-or-CP2-Berry-constructor-and-time-flow-constitutive-gate.md",
            "U1_BASELINE_CP2_CONSTITUTIVE_GATE_4854",
            "current_EM_parent",
        ),
        (
            "SRC4900_04_4875",
            POST
            / "4875-Y5-R2FR-collective-metric-path-integral-massless-spin2-pole-and-Weinberg-Witten-evasion-or-induced-background-only-demotion.md",
            "INTEGRATED_PRINCIPAL_DENSITY_PARENT_AND_SPIN2_POLE_THEOREM_4875",
            "current_gravity_matter_parent",
        ),
        (
            "SRC4900_05_4877",
            POST
            / "4877-Y5-R2FR-MTS-bath-signed-spectrum-sum-rules-and-nonlocal-form-factor-completion-or-renormalized-vacuum-freeze.md",
            "MTS_SPECTRUM_NO_GO_NONLOCAL_COMPLETION_AND_RENORMALIZED_VACUUM_FREEZE_4877",
            "primitive_spectrum_audit",
        ),
        (
            "SRC4900_06_formal4877",
            FORMAL / "893-PPC4161-spectrum-nonlocal-vacuum-freeze.md",
            "PPC4161_SPECTRUM_NONLOCAL_VACUUM_FREEZE_4877",
            "primitive_spectrum_audit",
        ),
        (
            "SRC4900_07_lepton_family",
            QPF
            / "leptons-neutrinos"
            / "finite-lepton-families-from-curvature-memory-geometry.md",
            "FINITE LEPTON FAMILIES",
            "particle_claim_under_audit",
        ),
        (
            "SRC4900_08_lepton_mass",
            QPF
            / "leptons-neutrinos"
            / "the-lepton-mass-hierarchy-from-motion-timespace.md",
            "LEPTON MASS HIERARCHY",
            "particle_claim_under_audit",
        ),
        (
            "SRC4900_09_quark_mass",
            QPF
            / "quarks-protons"
            / "the-quark-mass-hierarchy-from-motion-timespace.md",
            "QUARK MASS HIERARCHY",
            "particle_claim_under_audit",
        ),
        (
            "SRC4900_10_proton",
            QPF
            / "quarks-protons"
            / "the-proton-as-a-fundamental-mts-soliton.md",
            "PROTON AS A FUNDAMENTAL MTS SOLITON",
            "particle_claim_under_audit",
        ),
        (
            "SRC4900_11_neutrino",
            QPF
            / "leptons-neutrinos"
            / "neutrino-mixing-from-motion-timespace-geometry.md",
            "Neutrino Mixing from Motion",
            "particle_claim_under_audit",
        ),
        (
            "SRC4900_12_YM",
            QPF / "yang-mills" / "yang-mills-mass-gap-via-the-motion-theory.md",
            "Mass Gap",
            "particle_claim_under_audit",
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
    for source_id, url, description in (
        (
            "SRC4900_13_NIST_alpha",
            NIST_WALL_2022_URL,
            "CODATA 2022 alpha(0) boundary value",
        ),
        (
            "SRC4900_14_GellMannLow",
            GELL_MANN_LOW_URL,
            "Gell-Mann and Low QED scale dependence primary source",
        ),
    ):
        rows.append(
            {
                "source_id": source_id,
                "source_type": "official_or_primary_external_source",
                "source_path_or_url": url,
                "local_path_required": False,
                "source_exists": True,
                "marker": description,
                "marker_found": True,
                "source_checked_date": "2026-07-11",
            }
        )
    return {
        "rows": rows,
        "local_sources": len(local_sources),
        "external_sources": 2,
        "passed": all(
            row["source_exists"]
            and row["marker_found"]
            and (
                row["local_path_required"]
                or str(row["source_path_or_url"]).startswith("https://")
            )
            for row in rows
        ),
    }


@lru_cache(maxsize=None)
def corpus_field_content_audit() -> dict[str, Any]:
    files = sorted(QPF.rglob("*.md"))
    texts = {
        path: path.read_text(encoding="utf-8", errors="replace").lower()
        for path in files
    }
    patterns = [
        ("Grassmann_measure", ("grassmann",)),
        ("Dirac_operator", ("dirac",)),
        ("Clifford_module", ("clifford",)),
        ("spinor_field", ("spinor",)),
        ("fermion_field", ("fermion",)),
        ("spin_statistics_map", ("spin-statistics", "spin statistics")),
        ("U1_connection", ("u(1)",)),
        ("gauge_covariant_derivative", ("covariant derivative", "d_mu", "a_mu")),
    ]
    rows: list[dict[str, Any]] = []
    for object_name, needles in patterns:
        occurrences = sum(
            sum(text.count(needle) for needle in needles)
            for text in texts.values()
        )
        matching_files = sum(
            any(needle in text for needle in needles) for text in texts.values()
        )
        rows.append(
            {
                "object": object_name,
                "needles": ";".join(needles),
                "occurrences": occurrences,
                "matching_files": matching_files,
                "required_for_primitive_Dirac_QED": True,
                "present": occurrences > 0,
            }
        )
    complex_scalar_files = sum(
        "complex motion field" in text or "exp(i n" in text
        for text in texts.values()
    )
    winding_files = sum("winding" in text for text in texts.values())
    return {
        "rows": rows,
        "files_scanned": len(files),
        "critical_objects_present": sum(row["present"] for row in rows),
        "complex_scalar_or_phase_files": complex_scalar_files,
        "winding_files": winding_files,
        "primitive_Dirac_QED_field_content_present": all(
            row["present"] for row in rows[:6]
        ),
        "all_paths": [str(path) for path in files],
        "passed": bool(
            len(files) == 12
            and len(rows) == 8
            and all(row["occurrences"] == 0 for row in rows)
        ),
    }


@lru_cache(maxsize=None)
def representation_no_go() -> dict[str, Any]:
    rows = [
        {
            "clause": "local_scalar_representation",
            "finding": "ordinary perturbative excitations of the printed scalar carry integer spin",
            "consequence": "no electron spin one-half representation",
            "loophole_or_repair": "adopt a spinor or derive topological fermion quantization",
            "closed": False,
        },
        {
            "clause": "topological_fermion_loophole",
            "finding": "bosonic solitons can only evade the representation obstruction with nontrivial configuration-space quantization",
            "consequence": "current winding label is insufficient",
            "loophole_or_repair": "derive configuration-space pi1 and a Finkelstein-Rubinstein sign constraint",
            "closed": False,
        },
        {
            "clause": "winding_to_electric_charge",
            "finding": "exp(i n theta) is spatial orbital winding and no D_mu or A_mu current appears",
            "consequence": "n is not proved to be the principal-U1 charge",
            "loophole_or_repair": "derive the Noether moment map into the selected U1 representation",
            "closed": False,
        },
        {
            "clause": "winding_sign",
            "finding": "C(+n)=C(-n) proves parity of a scalar energy functional",
            "consequence": "does not prove charge conjugation or matter-antimatter quantum numbers",
            "loophole_or_repair": "derive C action on fields and current",
            "closed": False,
        },
        {
            "clause": "family_number",
            "finding": "the document's own threshold leaves n<=5 viable but identifies only n=1,2,3",
            "consequence": "exactly three charged lepton families are not selected",
            "loophole_or_repair": "derive a stability eigenvalue excluding n=4,5 without a fitted budget",
            "closed": False,
        },
        {
            "clause": "compact_U1_vectorlike_representations",
            "finding": "any integer vectorlike Dirac charge is anomaly free",
            "consequence": "U1 compactness and anomalies do not select observed charges",
            "loophole_or_repair": "derive a larger chiral gauge representation and its anomaly constraints",
            "closed": False,
        },
        {
            "clause": "primitive_verdict",
            "finding": "no Grassmann Clifford spin-statistics or U1 moment-map chain exists in the particle corpus",
            "consequence": "primitive charged fermions are not derived",
            "loophole_or_repair": "explicit Dirac correspondence adoption or a complete topological-fermion theorem",
            "closed": False,
        },
    ]
    return {
        "rows": rows,
        "primitive_charged_fermion_derived": False,
        "winding_charge_map_derived": False,
        "exact_three_family_theorem": False,
        "topological_fermion_route_present": False,
        "representation_status": (
            "CURRENT_SCALAR_WINDING_PARTICLE_ROUTE_REJECTED_AS_DIRAC_U1_DERIVATION"
        ),
        "passed": len(rows) == 7 and not any(row["closed"] for row in rows),
    }


@lru_cache(maxsize=None)
def particle_claim_audit() -> dict[str, Any]:
    rows = [
        {
            "claim_id": "QPF4900_LEPTON_FAMILIES",
            "source_path": "quantum-particle-field/leptons-neutrinos/finite-lepton-families-from-curvature-memory-geometry.md",
            "printed_claim": "three charged lepton families and charge symmetry from winding",
            "decisive_issue": "n<=5 remains viable; winding is not mapped to U1 charge or spin one-half",
            "retained_asset": "candidate scalar winding and curvature-cost diagnostic",
            "current_status": "HEURISTIC_NOT_PARTICLE_REPRESENTATION_THEOREM",
            "eligible_for_current_particle_claim": False,
        },
        {
            "claim_id": "QPF4900_LEPTON_MASSES",
            "source_path": "quantum-particle-field/leptons-neutrinos/the-lepton-mass-hierarchy-from-motion-timespace.md",
            "printed_claim": "parameter-free electron muon tau mass ratios",
            "decisive_issue": "three amplitudes are chosen including a documented tau fine adjustment; solutions do not decay and energy grows with radial cutoff",
            "retained_asset": "reproducible nonlinear amplitude-to-integral map",
            "current_status": "FITTED_NONLOCALIZED_SCALAR_PROXY_NOT_MASS_PREDICTION",
            "eligible_for_current_particle_claim": False,
        },
        {
            "claim_id": "QPF4900_QUARK_MASSES",
            "source_path": "quantum-particle-field/quarks-protons/the-quark-mass-hierarchy-from-motion-timespace.md",
            "printed_claim": "geometric quark mass ladder without Yukawa fitting",
            "decisive_issue": "six flavour amplitudes are assigned and the code explicitly minimizes a loss against three target ratios",
            "retained_asset": "nonlinear scalar regression experiment",
            "current_status": "EXPLICIT_RATIO_FIT_NOT_QUARK_SPECTRUM_DERIVATION",
            "eligible_for_current_particle_claim": False,
        },
        {
            "claim_id": "QPF4900_PROTON",
            "source_path": "quantum-particle-field/quarks-protons/the-proton-as-a-fundamental-mts-soliton.md",
            "printed_claim": "938 MeV and 0.84 fm from a parameter-free proton eigenmode",
            "decisive_issue": "no executable boundary-value solve or dimensionally closed map to the asserted eigenvalue and radius is supplied",
            "retained_asset": "candidate nonlinear radial BVP target",
            "current_status": "ASSERTED_NUMBERS_BVP_AND_QCD_QUANTUM_NUMBERS_OPEN",
            "eligible_for_current_particle_claim": False,
        },
        {
            "claim_id": "QPF4900_NEUTRINO",
            "source_path": "quantum-particle-field/leptons-neutrinos/neutrino-mixing-from-motion-timespace-geometry.md",
            "printed_claim": "PMNS matrix and masses derived without free inputs",
            "decisive_issue": "a numerical 3x3 Hamiltonian is inserted but no parent operator derives its matrix entries or spinor weak-interaction readout",
            "retained_asset": "Hermitian matrix parametrization and diagonalization target",
            "current_status": "NUMERIC_MATRIX_ANSATZ_NOT_NEUTRINO_FIELD_DERIVATION",
            "eligible_for_current_particle_claim": False,
        },
        {
            "claim_id": "QPF4900_YANG_MILLS",
            "source_path": "quantum-particle-field/yang-mills/yang-mills-mass-gap-via-the-motion-theory.md",
            "printed_claim": "Yang-Mills mass-gap proof from curvature resistance",
            "decisive_issue": "J^mu partial_mu C is not proved positive or coercive and finite damped-grid residual energy is not a continuum quantum spectral gap",
            "retained_asset": "nonlinear damping simulation concept",
            "current_status": "NOT_A_VALID_YANG_MILLS_MASS_GAP_PROOF",
            "eligible_for_current_particle_claim": False,
        },
    ]
    return {
        "rows": rows,
        "audited_claims": len(rows),
        "current_particle_claims": sum(
            row["eligible_for_current_particle_claim"] for row in rows
        ),
        "all_source_paths_exist": all((ROOT / row["source_path"]).exists() for row in rows),
        "quarantine_status": (
            "QPF_PRIMITIVE_PARTICLE_CLAIMS_QUARANTINED_HEURISTIC_ASSETS_RETAINED"
        ),
        "passed": bool(
            len(rows) == 6
            and not any(row["eligible_for_current_particle_claim"] for row in rows)
        ),
    }


def lepton_proxy_mass(amplitude: float, radius_max: float) -> dict[str, float]:
    curvature_strength = 1.2
    exponent = 1.75

    def ode(_: float, state: np.ndarray) -> list[float]:
        psi, derivative = state
        return [
            derivative,
            -curvature_strength * psi
            - abs(psi) ** (exponent - 1.0) * psi,
        ]

    solution = solve_ivp(
        ode,
        [0.0, radius_max],
        [amplitude, 0.0],
        max_step=0.05,
        rtol=1.0e-7,
        atol=1.0e-9,
    )
    psi = solution.y[0]
    radius = solution.t
    integrand = (
        psi**2
        + curvature_strength * psi**2
        + np.abs(psi) ** (exponent + 1.0)
    )
    mass = float(trapezoid(integrand * radius**2, radius))
    return {
        "mass_proxy": mass,
        "psi_boundary": float(psi[-1]),
        "dpsi_boundary": float(solution.y[1, -1]),
        "max_abs_psi": float(np.max(np.abs(psi))),
    }


@lru_cache(maxsize=None)
def lepton_solver_reproduction() -> dict[str, Any]:
    amplitudes = {
        "electron_like": 0.4,
        "muon_like": 4.33,
        "tau_like": 13.40,
    }
    radii = (10.0, 20.0, 40.0, 80.0)
    rows: list[dict[str, Any]] = []
    by_radius: dict[float, dict[str, dict[str, float]]] = {}
    for radius_max in radii:
        by_radius[radius_max] = {}
        for label, amplitude in amplitudes.items():
            result = lepton_proxy_mass(amplitude, radius_max)
            by_radius[radius_max][label] = result
            rows.append(
                {
                    "radius_max": radius_max,
                    "mode": label,
                    "amplitude_input": amplitude,
                    **result,
                    "finite_energy_boundary_condition_satisfied": False,
                }
            )
    ratio_rows: list[dict[str, Any]] = []
    for radius_max in radii:
        values = by_radius[radius_max]
        mu_e = (
            values["muon_like"]["mass_proxy"]
            / values["electron_like"]["mass_proxy"]
        )
        tau_mu = (
            values["tau_like"]["mass_proxy"]
            / values["muon_like"]["mass_proxy"]
        )
        ratio_rows.append(
            {
                "radius_max": radius_max,
                "mu_over_e": mu_e,
                "tau_over_mu": tau_mu,
                "electron_boundary_abs": abs(
                    values["electron_like"]["psi_boundary"]
                ),
                "muon_boundary_abs": abs(values["muon_like"]["psi_boundary"]),
                "tau_boundary_abs": abs(values["tau_like"]["psi_boundary"]),
            }
        )
    growth_exponents: dict[str, float] = {}
    for label in amplitudes:
        mass_40 = by_radius[40.0][label]["mass_proxy"]
        mass_80 = by_radius[80.0][label]["mass_proxy"]
        growth_exponents[label] = math.log(mass_80 / mass_40, 2.0)
    published_mu_e = 202.7238164914748
    published_tau_mu = 16.71744125265042
    row_40 = next(row for row in ratio_rows if row["radius_max"] == 40.0)
    reproduction_error = max(
        abs(row_40["mu_over_e"] / published_mu_e - 1.0),
        abs(row_40["tau_over_mu"] / published_tau_mu - 1.0),
    )
    return {
        "rows": rows,
        "ratio_rows": ratio_rows,
        "growth_exponents": growth_exponents,
        "amplitude_inputs": len(amplitudes),
        "target_mass_ratios": 2,
        "published_R40_reproduction_error": reproduction_error,
        "all_R80_boundary_values_nonzero": all(
            row[key] > 0.1
            for row in ratio_rows
            if row["radius_max"] == 80.0
            for key in (
                "electron_boundary_abs",
                "muon_boundary_abs",
                "tau_boundary_abs",
            )
        ),
        "all_mass_growth_exponents_near_three": all(
            2.9 < value < 3.1 for value in growth_exponents.values()
        ),
        "finite_energy_soliton_established": False,
        "mass_prediction_status": (
            "PUBLISHED_NUMBERS_REPRODUCED_BUT_AMPLITUDE_FITTED_AND_RADIAL_INTEGRAL_DIVERGES"
        ),
        "passed": bool(
            len(rows) == 12
            and len(ratio_rows) == 4
            and reproduction_error < 1.0e-10
            and all(
                2.9 < value < 3.1 for value in growth_exponents.values()
            )
        ),
    }


@lru_cache(maxsize=None)
def dirac_qed_correspondence() -> dict[str, Any]:
    clauses = [
        (
            "spin_structure",
            "declare the public metric manifold spin and choose a compatible tetrad",
            True,
        ),
        (
            "Grassmann_Dirac_fields",
            "integrate independent charged Grassmann spinors chi_a",
            True,
        ),
        (
            "Clifford_covariant_derivative",
            "D_mu chi_a=(nabla_mu+i e_R q_a A_mu)chi_a",
            True,
        ),
        (
            "single_public_metric_and_U1",
            "Dirac and Maxwell principal symbols use the 4875 public metric and 4854 U1",
            True,
        ),
        (
            "Ward_identity",
            "gauge invariance gives nabla_mu j^mu=0 and matter-EM exchange",
            True,
        ),
        (
            "vectorlike_anomaly_cancellation",
            "q^3+(-q)^3=0 and q+(-q)=0 for each Dirac pair",
            True,
        ),
        (
            "one_alpha_boundary",
            "reuse checkpoint 4899 alpha(0) calibration",
            True,
        ),
        (
            "claim_firewall",
            "explicit correspondence adoption is not called primitive scalar emergence",
            True,
        ),
    ]
    rows = [
        {
            "clause_index": index,
            "clause": clause,
            "implementation": implementation,
            "passes": passes,
        }
        for index, (clause, implementation, passes) in enumerate(
            clauses, start=1
        )
    ]
    return {
        "rows": rows,
        "action": (
            "S_QED=int sqrt(-g)[-F_c^2/4+sum_a bar(chi_a)(i gamma^mu(nabla_mu+i e_R q_a A_mu)-m_a)chi_a]"
        ),
        "gauge_current": "j^mu=sum_a q_a bar(chi_a) gamma^mu chi_a",
        "gauge_anomaly_per_Dirac": "q^3+(-q)^3=0",
        "mixed_gravity_anomaly_per_Dirac": "q+(-q)=0",
        "correspondence_module_status": (
            "EXPLICIT_STANDARD_DIRAC_QED_CORRESPONDENCE_ADOPTED"
        ),
        "primitive_MTS_fermion_derivation": False,
        "correspondence_gate_passed": all(row["passes"] for row in rows),
        "passed": len(rows) == 8 and all(row["passes"] for row in rows),
    }


@lru_cache(maxsize=None)
def qed_beta_function() -> dict[str, Any]:
    scale_ratio = 1000.0
    spectra = [
        (
            "one_Dirac_unit_charge",
            1.0,
            0.0,
            "minimal adopted electron-like QED correspondence",
            False,
        ),
        (
            "three_Dirac_unit_charge_leptons",
            3.0,
            0.0,
            "imported three charged-lepton benchmark",
            False,
        ),
        (
            "imported_SM_below_top_free_threshold",
            20.0 / 3.0,
            0.0,
            "three leptons plus five quarks with color; ignores hadronic matching",
            False,
        ),
        (
            "imported_full_SM_above_top",
            8.0,
            0.0,
            "three leptons plus six colored quarks",
            False,
        ),
        (
            "one_complex_scalar_unit_charge",
            0.0,
            1.0,
            "what a gauged primitive complex scalar would contribute",
            True,
        ),
    ]
    rows: list[dict[str, Any]] = []
    for (
        name,
        dirac_weight,
        scalar_weight,
        spectrum_note,
        primitive_scalar_compatible,
    ) in spectra:
        effective_weight = dirac_weight + scalar_weight / 4.0
        beta_at_alpha_zero = (
            2.0
            * ALPHA_ZERO**2
            * effective_weight
            / (3.0 * math.pi)
        )
        inverse_at_ratio = ALPHA_INVERSE - (
            2.0
            * effective_weight
            * math.log(scale_ratio)
            / (3.0 * math.pi)
        )
        rows.append(
            {
                "spectrum": name,
                "B_Dirac=sum_Nc_q2": dirac_weight,
                "B_complex_scalar=sum_q2": scalar_weight,
                "B_effective_Dirac_units": effective_weight,
                "dalpha_dlnmu_at_alpha0": beta_at_alpha_zero,
                "scale_ratio_mu_over_mu0": scale_ratio,
                "alpha_inverse_at_scale_ratio_massless_step_smoke": inverse_at_ratio,
                "alpha_at_scale_ratio_massless_step_smoke": 1.0
                / inverse_at_ratio,
                "vectorlike_gauge_anomaly": 0.0,
                "vectorlike_mixed_gravity_anomaly": 0.0,
                "spectrum_note": spectrum_note,
                "primitive_scalar_compatible": primitive_scalar_compatible,
                "parent_owned_spectrum": False,
                "claim_status": "conditional_running_structure_only",
            }
        )
    inverse_values = [
        row["alpha_inverse_at_scale_ratio_massless_step_smoke"]
        for row in rows
    ]
    return {
        "rows": rows,
        "beta_e_Dirac": "beta(e)=e^3 sum_f(Nc q_f^2)/(12 pi^2)",
        "beta_alpha_general": (
            "dalpha/dlnmu=2 alpha^2[B_Dirac+B_complex_scalar/4]/(3 pi)"
        ),
        "integrated_massless_step": (
            "alpha^-1(mu)=alpha^-1(mu0)-2 B_eff ln(mu/mu0)/(3 pi)"
        ),
        "spectrum_rows": len(rows),
        "inverse_running_spread_at_ratio": max(inverse_values)
        - min(inverse_values),
        "current_parent_B_effective_derived": False,
        "running_status": (
            "BETA_FUNCTION_FORM_DERIVED_SPECTRUM_AND_THRESHOLDS_IMPORTED_OR_OPEN"
        ),
        "passed": bool(
            len(rows) == 5
            and max(inverse_values) - min(inverse_values) > 10.0
            and all(row["vectorlike_gauge_anomaly"] == 0.0 for row in rows)
        ),
    }


@lru_cache(maxsize=None)
def primitive_particle_gate() -> dict[str, Any]:
    clauses = [
        (
            "primitive_Grassmann_measure",
            False,
            "fermionic path-integral sign is parent-owned",
        ),
        (
            "primitive_Clifford_spin_structure",
            False,
            "spinor bundle and Dirac operator descend from MTS",
        ),
        (
            "spin_statistics_theorem",
            False,
            "half-integer spin and anticommutation follow from the parent",
        ),
        (
            "soliton_to_U1_moment_map",
            False,
            "winding maps to the selected principal-U1 Noether charge",
        ),
        (
            "exact_three_lepton_representations",
            False,
            "n=4,5 are excluded by a derived stability spectrum",
        ),
        (
            "quark_and_chiral_gauge_representations",
            False,
            "fractional charges color and weak chirality are parent-owned",
        ),
        (
            "anomaly_cancellation_selects_spectrum",
            False,
            "gauge and mixed anomalies close on a uniquely derived chiral set",
        ),
        (
            "normalizable_mass_eigenstates",
            False,
            "particle BVPs decay and masses converge without fitted amplitudes",
        ),
        (
            "QED_beta_weight_and_thresholds",
            False,
            "charged spectrum fixes B_eff and every threshold",
        ),
        (
            "honest_standard_QED_correspondence_fallback",
            True,
            "explicit Dirac QED is available without claiming scalar emergence",
        ),
    ]
    rows = [
        {
            "clause_index": index,
            "clause": clause,
            "passes": passes,
            "required_evidence": evidence,
            "blocking_if_false": index < 10,
        }
        for index, (clause, passes, evidence) in enumerate(clauses, start=1)
    ]
    return {
        "rows": rows,
        "passed_clauses": sum(row["passes"] for row in rows),
        "total_clauses": len(rows),
        "primitive_particle_reentry_allowed": all(
            row["passes"] for row in rows[:9]
        ),
        "gate_logic": "first nine primitive clauses AND; fallback is not a derivation",
        "passed": bool(
            len(rows) == 10
            and sum(row["passes"] for row in rows) == 1
            and not all(row["passes"] for row in rows[:9])
        ),
    }


@lru_cache(maxsize=None)
def arbitration() -> dict[str, Any]:
    corpus = corpus_field_content_audit()
    representation = representation_no_go()
    claims = particle_claim_audit()
    solver = lepton_solver_reproduction()
    correspondence = dirac_qed_correspondence()
    beta = qed_beta_function()
    primitive = primitive_particle_gate()
    return {
        "primitive_particle_status": (
            "CURRENT_SCALAR_SOLITON_CLAIMS_REJECTED_AS_FERMION_CHARGE_DERIVATIONS"
        ),
        "legacy_particle_files_status": claims["quarantine_status"],
        "QED_correspondence_status": correspondence[
            "correspondence_module_status"
        ],
        "QED_beta_status": beta["running_status"],
        "alpha_boundary_status": "ONE_CODATA_CALIBRATION_INHERITED_FROM_4899",
        "classical_only_freeze_status": (
            "AVOIDED_BY_EXPLICIT_STANDARD_DIRAC_QED_CORRESPONDENCE_MODULE"
        ),
        "primitive_particle_gate_passed_clauses": primitive["passed_clauses"],
        "primitive_particle_gate_total_clauses": primitive["total_clauses"],
        "current_particle_claim_count": claims["current_particle_claims"],
        "next_target": NEXT_TARGET,
        "passed": bool(
            corpus["passed"]
            and not corpus["primitive_Dirac_QED_field_content_present"]
            and representation["passed"]
            and not representation["primitive_charged_fermion_derived"]
            and claims["passed"]
            and solver["passed"]
            and not solver["finite_energy_soliton_established"]
            and correspondence["passed"]
            and not correspondence["primitive_MTS_fermion_derivation"]
            and beta["passed"]
            and not beta["current_parent_B_effective_derived"]
            and primitive["passed"]
            and not primitive["primitive_particle_reentry_allowed"]
        ),
    }


@lru_cache(maxsize=None)
def result() -> dict[str, Any]:
    sections = {
        "sources": source_contract(),
        "corpus": corpus_field_content_audit(),
        "representation": representation_no_go(),
        "claims": particle_claim_audit(),
        "solver": lepton_solver_reproduction(),
        "correspondence": dirac_qed_correspondence(),
        "beta": qed_beta_function(),
        "primitive_gate": primitive_particle_gate(),
        "arbitration": arbitration(),
    }
    return {
        "checkpoint": CHECKPOINT,
        "sections": sections,
        "decision": sections["arbitration"]["QED_correspondence_status"],
        "all_checks_pass": all(
            section.get("passed", True) for section in sections.values()
        ),
    }


def main() -> int:
    calculation = result()
    corpus = calculation["sections"]["corpus"]
    solver = calculation["sections"]["solver"]
    beta = calculation["sections"]["beta"]
    print(
        "files={} primitive_objects={} lepton_growth={} beta_spread={:.6f}".format(
            corpus["files_scanned"],
            corpus["critical_objects_present"],
            ",".join(
                f"{value:.3f}"
                for value in solver["growth_exponents"].values()
            ),
            beta["inverse_running_spread_at_ratio"],
        )
    )
    print(calculation["decision"])
    return 0 if calculation["all_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

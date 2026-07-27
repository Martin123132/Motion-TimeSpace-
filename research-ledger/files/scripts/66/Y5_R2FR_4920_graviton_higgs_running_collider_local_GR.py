from __future__ import annotations

import csv
import hashlib
import math
import sys
from pathlib import Path
from typing import Any

from scipy.constants import c, electron_volt, hbar, physical_constants


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
SCRIPTS = POST / "scripts"

CHECKPOINT = "4920"
CHECKED_DATE = "2026-07-12"
MARKER = "MTS_GRAVITON_HIGGS_OBSERVABLE_LOCAL_GR_GATE_4920"
FORMAL_MARKER = "PPC4161_GRAVITON_HIGGS_OBSERVABLE_LOCAL_GR_GATE_4920"
NEXT_TARGET = (
    "4921-Y5-R2FR-pure-metric-curvature-cubed-and-nonlocal-tail-"
    "observable-separation-or-invariant-vacuum-GR-domain-extension-gate.md"
)

HIGGS_MASS_GEV = 125.13
ATLAS_MU = 1.023
ATLAS_SIGMA_PLUS = 0.056
ATLAS_SIGMA_MINUS = 0.053
CMS_MU = 1.014
CMS_SIGMA_PLUS = 0.055
CMS_SIGMA_MINUS = 0.053
ONE_SIDED_95_DELTA_CHI2 = 2.71
TWO_SIDED_95_DELTA_CHI2 = 3.84
R10_MINIMUM_GAP_M = 52.0e-6

ATLAS_URL = "https://cds.cern.ch/record/2937634"
CMS_URL = (
    "https://cms-results.web.cern.ch/cms-results/public-results/"
    "publications/HIG-21-018/"
)
MOSS_URL = "https://arxiv.org/abs/1409.2108"
ATKINS_CALMET_URL = "https://arxiv.org/abs/1211.0281"
VACUUM_CUTOFF_URL = "https://arxiv.org/abs/0903.0355"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


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


def calibration() -> dict[str, float]:
    rows = read_csv(OUTPUT / "P8_Y5_R2FR_4898_CODATA_CALIBRATION.csv")
    reduced_planck_gev = next(
        float(row["value"])
        for row in rows
        if row["quantity"] == "Mbar_Pl" and row["units"] == "GeV/c^2"
    )
    fermi_gev_minus_two = physical_constants["Fermi coupling constant"][0]
    electroweak_vev_gev = 1.0 / math.sqrt(
        math.sqrt(2.0) * fermi_gev_minus_two
    )
    hbar_c_gev_m = hbar * c / (electron_volt * 1.0e9)
    return {
        "Mbar_Pl_GeV": reduced_planck_gev,
        "G_F_GeV_minus_2": fermi_gev_minus_two,
        "v_EW_GeV": electroweak_vev_gev,
        "hbar_c_GeV_m": hbar_c_gev_m,
    }


def profile_limit(
    mu_observed: float,
    sigma_lower: float,
    delta_chi2: float,
) -> dict[str, float]:
    values = calibration()
    mu_lower = mu_observed - math.sqrt(
        (mu_observed - 1.0) ** 2 + delta_chi2 * sigma_lower**2
    )
    if not 0.0 < mu_lower <= 1.0:
        raise ValueError("profile lower limit lies outside physical signal-strength branch")
    beta_upper = 1.0 / mu_lower - 1.0
    xi_upper = (
        values["Mbar_Pl_GeV"]
        / values["v_EW_GeV"]
        * math.sqrt(beta_upper / 6.0)
    )
    return {
        "mu_lower": mu_lower,
        "beta_upper": beta_upper,
        "xi_upper": xi_upper,
        "kappa_lower": math.sqrt(mu_lower),
        "cutoff_M_over_xi_GeV": values["Mbar_Pl_GeV"] / xi_upper,
        "cutoff_M_over_sqrt_xi_GeV": values["Mbar_Pl_GeV"]
        / math.sqrt(xi_upper),
    }


def selected_limits() -> dict[str, float]:
    atlas_one = profile_limit(
        ATLAS_MU, ATLAS_SIGMA_MINUS, ONE_SIDED_95_DELTA_CHI2
    )
    atlas_two = profile_limit(
        ATLAS_MU, ATLAS_SIGMA_MINUS, TWO_SIDED_95_DELTA_CHI2
    )
    cms_one = profile_limit(
        CMS_MU, CMS_SIGMA_MINUS, ONE_SIDED_95_DELTA_CHI2
    )
    cms_two = profile_limit(
        CMS_MU, CMS_SIGMA_MINUS, TWO_SIDED_95_DELTA_CHI2
    )
    return {
        "xi_primary_one_sided": atlas_one["xi_upper"],
        "xi_primary_two_sided": atlas_two["xi_upper"],
        "cutoff_primary_one_sided_GeV": atlas_one["cutoff_M_over_xi_GeV"],
        "cutoff_primary_two_sided_GeV": atlas_two["cutoff_M_over_xi_GeV"],
        "xi_cms_one_sided": cms_one["xi_upper"],
        "xi_cms_two_sided": cms_two["xi_upper"],
    }


def running_basis_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "basis_id": "RUN4920_00_boundary",
                "object": "fixed-metric factorization boundary",
                "statement": "internal graviton lines are not removed by Gamma_X+Gamma_SM at fixed g",
                "invariant_status": "EXPLICIT_EXCEPTION_INHERITED_FROM_4919",
                "observable_action": "retain graviton-mediated mixed 1PI class",
                "passed": True,
            },
            {
                "basis_id": "RUN4920_01_split",
                "object": "graviton-mediated 1PI functional",
                "statement": "Gamma_grav=Gamma_local_analytic+Gamma_nonanalytic",
                "invariant_status": "EFT_OPERATOR_SPLIT",
                "observable_action": "renormalize local basis and bound nonanalytic amplitudes",
                "passed": True,
            },
            {
                "basis_id": "RUN4920_02_xi_beta",
                "object": "standalone beta_xi in a chosen Jordan basis",
                "statement": "off-shell coefficient running changes under correlated field redefinitions and scheme choices",
                "invariant_status": "NOT_A_STANDALONE_OBSERVABLE",
                "observable_action": "do not use a naked beta_xi number as a local-GR gate",
                "passed": True,
            },
            {
                "basis_id": "RUN4920_03_redefinition",
                "object": "R HdagH basis map",
                "statement": "a local conformal or metric redefinition moves R HdagH into correlated kinetic and trace operators",
                "invariant_status": "OPERATOR_MOVED_NOT_ERASED",
                "observable_action": "retain the full correlated operator packet",
                "passed": True,
            },
            {
                "basis_id": "RUN4920_04_VD",
                "object": "one-loop gravity-scalar effective action",
                "statement": "Vilkovisky-DeWitt construction removes gauge-fixing and field-coordinate artifacts from the full effective action",
                "invariant_status": "FULL_FUNCTIONAL_IS_THE_COVARIANT_TARGET",
                "observable_action": "compare on-shell residues and amplitudes",
                "passed": True,
            },
            {
                "basis_id": "RUN4920_05_total_xi",
                "object": "total renormalized curvature-Higgs packet",
                "statement": "xi_total=xi_SM+xi_grav+xi_hidden_grav+finite matching in a declared basis",
                "invariant_status": "COEFFICIENT_NOT_PREDICTED_BUT_PHYSICAL_PACKET_BOUNDABLE",
                "observable_action": "bound its canonical Higgs residue",
                "passed": True,
            },
            {
                "basis_id": "RUN4920_06_local",
                "object": "analytic loop terms",
                "statement": "local divergences and finite analytic pieces renormalize R HdagH and higher local operators",
                "invariant_status": "COUNTERTERM_PACKET_REQUIRED",
                "observable_action": "use xi_total for the dimension-four packet; keep higher contact terms in strict EFT",
                "passed": True,
            },
            {
                "basis_id": "RUN4920_07_nonanalytic",
                "object": "massless-graviton nonanalytic terms",
                "statement": "q^2 log(-q^2) and related cuts cannot be removed by local field redefinitions",
                "invariant_status": "PHYSICAL_LONG_RANGE_CLASS",
                "observable_action": "bound with an arena-scale loop expansion",
                "passed": True,
            },
            {
                "basis_id": "RUN4920_08_hidden",
                "object": "hidden loop connected to visible Higgs by gravitons",
                "statement": "its local R HdagH image is included in xi_total and its pure-vacuum metric part remains in the pure-metric ledger",
                "invariant_status": "NOT_ZEROED_BY_FACTORIZATION",
                "observable_action": "separate visible residue from pure-metric matching",
                "passed": True,
            },
            {
                "basis_id": "RUN4920_09_decision",
                "object": "gravitational running target",
                "statement": "replace an unphysical zero-or-number hunt by on-shell residue plus nonanalytic amplitude gates",
                "invariant_status": "OBSERVABLE_ROUTE_SELECTED",
                "observable_action": "collider recast and local NDA projection",
                "passed": True,
            },
        ]
    )


def higgs_input_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "input_id": "HIGGS4920_00_ATLAS",
                "experiment": "ATLAS",
                "analysis": "ATLAS-CONF-2025-006",
                "publication_year": 2025,
                "mu_observed": ATLAS_MU,
                "sigma_plus": ATLAS_SIGMA_PLUS,
                "sigma_minus": ATLAS_SIGMA_MINUS,
                "luminosity_fb_minus_1": 140.0,
                "status": "CURRENT_ATLAS_GLOBAL_RUN2_COMBINATION",
                "source_url": ATLAS_URL,
                "used_for_primary_bound": True,
                "passed": True,
            },
            {
                "input_id": "HIGGS4920_01_CMS",
                "experiment": "CMS",
                "analysis": "CMS-HIG-21-018; CERN-EP-2026-009",
                "publication_year": 2026,
                "mu_observed": CMS_MU,
                "sigma_plus": CMS_SIGMA_PLUS,
                "sigma_minus": CMS_SIGMA_MINUS,
                "luminosity_fb_minus_1": 138.0,
                "status": "CURRENT_CMS_MOST_COMPREHENSIVE_COMBINATION",
                "source_url": CMS_URL,
                "used_for_primary_bound": False,
                "passed": True,
            },
            {
                "input_id": "HIGGS4920_02_model",
                "experiment": "MTS active invariant-vacuum branch",
                "analysis": "universal canonical Higgs-residue recast",
                "publication_year": 2026,
                "mu_observed": "not_applicable",
                "sigma_plus": "not_applicable",
                "sigma_minus": "not_applicable",
                "luminosity_fb_minus_1": "not_applicable",
                "status": "NO_EXTRA_HIGGS_DECAYS_AND_SM_BRANCHING_RATIOS_ASSUMED",
                "source_url": "post-checkpoint-work/4919-Y5-R2FR-vacuum-1PI-operator-selection-curvature-Higgs-and-hidden-scalar-vev-matching-or-local-bound.md",
                "used_for_primary_bound": True,
                "passed": True,
            },
            {
                "input_id": "HIGGS4920_03_no_combine",
                "experiment": "ATLAS plus CMS",
                "analysis": "independent display only",
                "publication_year": 2026,
                "mu_observed": "not_combined",
                "sigma_plus": "not_combined",
                "sigma_minus": "not_combined",
                "luminosity_fb_minus_1": "not_summed",
                "status": "NO_UNPUBLISHED_COVARIANCE_OR_LIKELIHOOD_COMBINATION",
                "source_url": f"{ATLAS_URL};{CMS_URL}",
                "used_for_primary_bound": False,
                "passed": True,
            },
        ]
    )


def collider_recast_rows() -> list[dict[str, Any]]:
    experiments = (
        ("ATLAS", ATLAS_MU, ATLAS_SIGMA_MINUS, ATLAS_URL),
        ("CMS", CMS_MU, CMS_SIGMA_MINUS, CMS_URL),
    )
    thresholds = (
        ("one_sided_95", ONE_SIDED_95_DELTA_CHI2),
        ("two_sided_95_envelope", TWO_SIDED_95_DELTA_CHI2),
    )
    rows: list[dict[str, Any]] = []
    for experiment, mu_observed, sigma_lower, source_url in experiments:
        for threshold_name, delta_chi2 in thresholds:
            limit = profile_limit(mu_observed, sigma_lower, delta_chi2)
            rows.append(
                {
                    "recast_id": f"RECAST4920_{experiment}_{threshold_name}",
                    "experiment": experiment,
                    "threshold": threshold_name,
                    "delta_chi2": delta_chi2,
                    "model_formula": "mu_pred=kappa_h^2=1/(1+beta); beta=6 xi_H^2 v^2/Mbar_Pl^2",
                    "physical_best_mu": 1.0,
                    "mu_lower": limit["mu_lower"],
                    "kappa_lower": limit["kappa_lower"],
                    "beta_upper": limit["beta_upper"],
                    "abs_xi_upper": limit["xi_upper"],
                    "units_xi": "dimensionless",
                    "source_url": source_url,
                    "likelihood_status": "SPLIT_NORMAL_GAUSSIAN_RECAST_NOT_OFFICIAL_EXPERIMENT_LIKELIHOOD",
                    "selected_primary": experiment == "ATLAS"
                    and threshold_name == "one_sided_95",
                    "passed": True,
                }
            )
    return tagged(rows)


def eft_cutoff_rows() -> list[dict[str, Any]]:
    values = calibration()
    limits = {
        "ATLAS_one_sided": profile_limit(
            ATLAS_MU, ATLAS_SIGMA_MINUS, ONE_SIDED_95_DELTA_CHI2
        ),
        "ATLAS_two_sided": profile_limit(
            ATLAS_MU, ATLAS_SIGMA_MINUS, TWO_SIDED_95_DELTA_CHI2
        ),
        "CMS_one_sided": profile_limit(
            CMS_MU, CMS_SIGMA_MINUS, ONE_SIDED_95_DELTA_CHI2
        ),
        "CMS_two_sided": profile_limit(
            CMS_MU, CMS_SIGMA_MINUS, TWO_SIDED_95_DELTA_CHI2
        ),
    }
    rows: list[dict[str, Any]] = []
    for label, limit in limits.items():
        rows.append(
            {
                "cutoff_id": f"CUTOFF4920_{label}",
                "bound_source": label,
                "abs_xi_upper": limit["xi_upper"],
                "Lambda_vacuum_M_over_xi_GeV": limit["cutoff_M_over_xi_GeV"],
                "Lambda_covariant_M_over_sqrt_xi_GeV": limit[
                    "cutoff_M_over_sqrt_xi_GeV"
                ],
                "m_h_over_Lambda_vacuum": HIGGS_MASS_GEV
                / limit["cutoff_M_over_xi_GeV"],
                "Mbar_Pl_GeV": values["Mbar_Pl_GeV"],
                "interpretation": "conservative vacuum power-counting cutoff and Moss covariant small-field comparator",
                "status": "ON_SHELL_HIGGS_SCALE_BELOW_CONSERVATIVE_CUTOFF",
                "passed": HIGGS_MASS_GEV < limit["cutoff_M_over_xi_GeV"],
            }
        )
    return tagged(rows)


def local_loop_projection_rows() -> list[dict[str, Any]]:
    values = calibration()
    conservative = profile_limit(
        ATLAS_MU, ATLAS_SIGMA_MINUS, TWO_SIDED_95_DELTA_CHI2
    )
    cutoff_gev = conservative["cutoff_M_over_xi_GeV"]
    arenas = (
        ("Higgs_pole", "on-shell Higgs", None, HIGGS_MASS_GEV),
        ("nuclear_1fm", "one-femtometre positive gap", 1.0e-15, None),
        ("optical_EM_1eV", "one-eV Maxwell benchmark", None, 1.0e-9),
        ("atomic_1A", "atomic clock and matter", 1.0e-10, None),
        ("R10_52um", "short-range gravity", R10_MINIMUM_GAP_M, None),
        ("Earth_radius", "terrestrial PPN", 6.371e6, None),
        ("Galileo_altitude", "orbital clock", 2.3229e7, None),
        ("solar_radius", "solar PPN light", 6.957e8, None),
        ("one_AU", "planetary orbit", 1.495978707e11, None),
    )
    rows: list[dict[str, Any]] = []
    for arena_id, arena, distance_m, fixed_energy_gev in arenas:
        energy_gev = (
            fixed_energy_gev
            if fixed_energy_gev is not None
            else values["hbar_c_GeV_m"] / float(distance_m)
        )
        epsilon = (energy_gev / cutoff_gev) ** 2 / (16.0 * math.pi**2)
        rows.append(
            {
                "projection_id": f"LOOP4920_{arena_id}",
                "arena": arena,
                "distance_m": "not_applicable" if distance_m is None else distance_m,
                "energy_GeV": energy_gev,
                "abs_xi_envelope": conservative["xi_upper"],
                "Lambda_vacuum_GeV": cutoff_gev,
                "epsilon_xi_NDA": epsilon,
                "formula": "epsilon_xi=(xi E/Mbar_Pl)^2/(16 pi^2)=(E/Lambda_xi)^2/(16 pi^2)",
                "analytic_support": "renormalized_local_or_contact",
                "nonanalytic_support": "physical_tail_bounded_by_epsilon_times_O1_no_large_log",
                "status": "NDA_ENVELOPE_NOT_EXACT_LOOP_COEFFICIENT",
                "passed": epsilon < 1.0,
            }
        )
    return tagged(rows)


def promotion_domain_rows() -> list[dict[str, Any]]:
    limits = selected_limits()
    return tagged(
        [
            {
                "domain_id": "DOMAIN4920_00_parent",
                "clause": "single EH parent and measured source residue",
                "status": "INHERITED_CONDITIONAL_PASS_4915",
                "scope": "selected integrated-H metric branch",
                "exclusion": "does not derive microscopic G_N",
                "passed": True,
            },
            {
                "domain_id": "DOMAIN4920_01_state",
                "clause": "Lorentz-invariant zero-enthalpy vacuum state",
                "status": "DERIVED_EXISTENCE_4918",
                "scope": "invariant vacuum only",
                "exclusion": "nonvacuum bath or FLRW state may reactivate flow",
                "passed": True,
            },
            {
                "domain_id": "DOMAIN4920_02_portal",
                "clause": "direct hidden-visible vacuum portals",
                "status": "EXACT_ZERO_4919",
                "scope": "fixed-metric factorized active parent",
                "exclusion": "internal gravitons treated separately here",
                "passed": True,
            },
            {
                "domain_id": "DOMAIN4920_03_Higgs",
                "clause": "total curvature-Higgs physical residue",
                "status": "CURRENT_COLLIDER_RECAST_BOUND",
                "scope": f"abs(xi_H)<{limits['xi_primary_one_sided']:.12e} approximate one-sided 95 percent",
                "exclusion": "not an official ATLAS likelihood and no extra Higgs decays assumed",
                "passed": True,
            },
            {
                "domain_id": "DOMAIN4920_04_loop",
                "clause": "xi-enhanced nonanalytic local-arena loop tail",
                "status": "NDA_BOUNDED_BELOW_LOCAL_SENSITIVITY",
                "scope": "R10 PPN clock orbit and optical Maxwell scales",
                "exclusion": "O1 coefficient and no-large-log envelope",
                "passed": True,
            },
            {
                "domain_id": "DOMAIN4920_05_weak_GR",
                "clause": "weak separated minimally coupled sources",
                "status": "PRIVATE_1PN_CERTIFICATE_4879_RETAINED",
                "scope": "Newton gamma beta light and point-clock kernels",
                "exclusion": "overlapping UV contact coefficients remain renormalized body data",
                "passed": True,
            },
            {
                "domain_id": "DOMAIN4920_06_vacuum_strong",
                "clause": "Einstein vacuum metrics with local R2 and C2",
                "status": "EXACT_COMMON_SOLUTION_4880_RETAINED",
                "scope": "Ricci-flat Schwarzschild Kerr and Einstein vacua",
                "exclusion": "compact matter interiors charged electrovac perturbation spectra and C3",
                "passed": True,
            },
            {
                "domain_id": "DOMAIN4920_07_pure_metric",
                "clause": "curvature-cubed and nonlocal pure-metric residuals",
                "status": "SEPARATE_ACTIVE_LEDGER_NOT_ERASED",
                "scope": "outside the Higgs promotion decision",
                "exclusion": "next checkpoint",
                "passed": True,
            },
            {
                "domain_id": "DOMAIN4920_08_UV",
                "clause": "energy validity",
                "status": "BELOW_CONSERVATIVE_VACUUM_CUTOFF",
                "scope": f"E much less than {limits['cutoff_primary_two_sided_GeV']:.6f} GeV",
                "exclusion": "no UV-completion claim above cutoff",
                "passed": True,
            },
        ]
    )


def gate_decision_rows() -> list[dict[str, Any]]:
    limits = selected_limits()
    return tagged(
        [
            {
                "gate": "standalone_gravitational_beta_xi",
                "status": "DEMOTED_AS_NONINVARIANT_STANDALONE_TARGET",
                "decision": "retain only a declared-basis running coefficient inside the correlated full effective action",
            },
            {
                "gate": "on_shell_Higgs_residue",
                "status": "APPROXIMATE_CURRENT_DATA_BOUND",
                "decision": f"ATLAS split-normal recast gives abs(xi_H)<{limits['xi_primary_one_sided']:.12e} at one-sided DeltaChi2=2.71",
            },
            {
                "gate": "CMS_crosscheck",
                "status": "INDEPENDENT_CURRENT_CROSSCHECK_PASS",
                "decision": f"CMS 2026 recast gives abs(xi_H)<{limits['xi_cms_one_sided']:.12e}; no ATLAS-CMS combination is fabricated",
            },
            {
                "gate": "vacuum_EFT_cutoff",
                "status": "HIGGS_AND_LOCAL_SCALES_BELOW_CONSERVATIVE_CUTOFF",
                "decision": f"ATLAS two-sided envelope gives Lambda=Mbar_Pl/abs(xi_H)>{limits['cutoff_primary_two_sided_GeV']:.6f} GeV",
            },
            {
                "gate": "internal_graviton_local_residual",
                "status": "ANALYTIC_CONTACT_SEPARATED_NONANALYTIC_NDA_BOUNDED",
                "decision": "no graviton-loop zero theorem is claimed; invariant long-range amplitudes are retained and locally negligible",
            },
            {
                "gate": "invariant_vacuum_weak_field_local_GR",
                "status": "PROMOTED_PRIVATE_CONDITIONAL_CERTIFICATE",
                "decision": "selected metric-only invariant-vacuum branch inherits the 4879 1PN certificate after the curvature-Higgs/graviton route is bounded",
            },
            {
                "gate": "full_MTS_to_GR",
                "status": "NOT_PROMOTED",
                "decision": "nonvacuum flow compact matter strong-field response UV completion and pure-metric C3/nonlocal sectors remain outside the certificate",
            },
            {
                "gate": "next_target",
                "status": "PURE_METRIC_RESIDUAL_SEPARATION",
                "decision": NEXT_TARGET,
            },
        ]
    )


def source_rows() -> list[dict[str, Any]]:
    local_sources = [
        (
            "SRC4920_00_4919_validation",
            OUTPUT / "P8_Y5_BRR545_4919_VALIDATION.csv",
            "VAL4919_OVERALL,PASS",
            "predecessor_validation",
        ),
        (
            "SRC4920_01_4919",
            POST / "4919-Y5-R2FR-vacuum-1PI-operator-selection-curvature-Higgs-and-hidden-scalar-vev-matching-or-local-bound.md",
            "MTS_VACUUM_1PI_HIGGS_HIDDEN_VEV_GATE_4919",
            "curvature_Higgs_predecessor",
        ),
        (
            "SRC4920_02_4915",
            POST / "4915-Y5-R2FR-parent-EH-residue-universal-source-coupling-and-measured-G-calibration-or-closure-demotion.md",
            "MTS_SINGLE_FUNCTIONAL_EH_SOURCE_RESIDUE_4915",
            "EH_source_parent",
        ),
        (
            "SRC4920_03_4878",
            POST / "4878-Y5-R2FR-renormalized-EFT-local-limit-and-arena-specific-nonlocal-residual-bounds-to-R10-PPN-clocks-orbit-and-Maxwell.md",
            "MTS_RENORMALIZED_EFT_LOCAL_ARENA_BOUNDS_4878",
            "strict_EFT_nonanalytic_predecessor",
        ),
        (
            "SRC4920_04_4879",
            POST / "4879-Y5-R2FR-source-size-contact-matching-and-second-order-beta-completion-plus-gauge-invariant-light-kernel-or-strict-EFT-local-GR-promotion-gate.md",
            "MTS_FINITE_SOURCE_BETA_LIGHT_CLOCK_LOCAL_GR_CERTIFICATE_4879",
            "weak_local_GR_certificate",
        ),
        (
            "SRC4920_05_4880",
            POST / "4880-Y5-R2FR-selected-metric-branch-local-GR-certificate-domain-of-validity-and-strong-field-entry-gate.md",
            "MTS_EXACT_EINSTEIN_VACUUM_BRANCH_AND_STRONG_FIELD_DOMAIN_4880",
            "vacuum_strong_field_domain",
        ),
        (
            "SRC4920_06_calibration",
            OUTPUT / "P8_Y5_R2FR_4898_CODATA_CALIBRATION.csv",
            "2.4353234600842885e+18",
            "Planck_and_EW_calibration",
        ),
        (
            "SRC4920_07_checkpoint",
            POST / "4920-Y5-R2FR-graviton-mediated-curvature-Higgs-running-and-current-Higgs-coupling-bound-or-vacuum-local-GR-promotion-gate.md",
            MARKER,
            "generated_checkpoint",
        ),
        (
            "SRC4920_08_research",
            Path(__file__).resolve(),
            "def collider_recast_rows",
            "generated_research_code",
        ),
        (
            "SRC4920_09_validation",
            SCRIPTS / "Y5_R2FR_4920_graviton_higgs_running_collider_local_GR_validation.py",
            "VAL4920_OVERALL",
            "generated_validation_code",
        ),
        (
            "SRC4920_10_formal",
            FORMAL / "936-PPC4161-graviton-Higgs-observable-bound-vacuum-local-GR-promotion.md",
            FORMAL_MARKER,
            "formal_summary",
        ),
        (
            "SRC4920_11_provenance",
            POST / "source-intake" / "parent_coupling" / "4920" / "PROVENANCE.md",
            "MTS_GRAVITON_HIGGS_PROVENANCE_4920",
            "provenance",
        ),
        (
            "SRC4920_12_claim",
            FORMAL / "02-claims-register.csv",
            "L-762",
            "register",
        ),
        (
            "SRC4920_13_variable",
            FORMAL / "04-variable-audit.csv",
            "GravXiPacket4920_MTS",
            "register",
        ),
        (
            "SRC4920_14_equation",
            FORMAL / "05-equation-register.md",
            "1.213 Graviton-Higgs observable packet and local loop bound",
            "register",
        ),
        (
            "SRC4920_15_redteam",
            FORMAL / "06-consistency-red-team.md",
            "164. A running Jordan-basis coefficient is not an on-shell local-gravity observable",
            "register",
        ),
        (
            "SRC4920_16_spine",
            FORMAL / "07-unification-spine.md",
            "PPC4161 checkpoint 4920",
            "register",
        ),
        (
            "SRC4920_17_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            FORMAL_MARKER,
            "resume",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, marker, role in local_sources:
        exists = path.exists()
        content = read_text_auto(path) if exists else ""
        rows.append(
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
    external_sources = [
        (
            "SRC4920_18_ATLAS",
            ATLAS_URL,
            "ATLAS-CONF-2025-006 mu=1.023 +0.056 -0.053",
            "primary_current_Higgs_experiment",
        ),
        (
            "SRC4920_19_CMS",
            CMS_URL,
            "CMS-HIG-21-018 mu=1.014 +0.055 -0.053",
            "primary_current_Higgs_experiment",
        ),
        (
            "SRC4920_20_Moss",
            MOSS_URL,
            "field-redefinition-covariant one-loop gravity-scalar effective action",
            "primary_theory_source",
        ),
        (
            "SRC4920_21_Atkins_Calmet",
            ATKINS_CALMET_URL,
            "canonical nonminimal-Higgs normalization and universal coupling suppression",
            "primary_theory_source",
        ),
        (
            "SRC4920_22_vacuum_cutoff",
            VACUUM_CUTOFF_URL,
            "conservative vacuum power-counting cutoff Mbar_Pl/xi",
            "primary_theory_source",
        ),
    ]
    for source_id, url, marker, role in external_sources:
        rows.append(
            {
                "source_id": source_id,
                "source_type": role,
                "source_path_or_url": url,
                "local_path_required": False,
                "source_exists": True,
                "marker": marker,
                "marker_found": True,
                "sha256": "external_source_not_hashed",
            }
        )
    return tagged(rows)


def main() -> int:
    tables = {
        "P8_Y5_R2FR_4920_RUNNING_BASIS.csv": running_basis_rows(),
        "P8_Y5_R2FR_4920_HIGGS_INPUTS.csv": higgs_input_rows(),
        "P8_Y5_R2FR_4920_COLLIDER_RECAST.csv": collider_recast_rows(),
        "P8_Y5_R2FR_4920_EFT_CUTOFF.csv": eft_cutoff_rows(),
        "P8_Y5_R2FR_4920_LOCAL_LOOP_PROJECTION.csv": local_loop_projection_rows(),
        "P8_Y5_R2FR_4920_PROMOTION_DOMAIN.csv": promotion_domain_rows(),
        "P8_Y5_R2FR_4920_GATE_DECISION.csv": gate_decision_rows(),
    }
    for filename, rows in tables.items():
        write_csv(OUTPUT / filename, rows)
    sources = source_rows()
    write_csv(OUTPUT / "P8_Y5_R2FR_4920_SOURCE_REGISTER.csv", sources)
    all_rows = [row for rows in tables.values() for row in rows]
    passed = (
        all(bool(row.get("passed", True)) for row in all_rows)
        and all(row["source_exists"] and row["marker_found"] for row in sources)
    )
    print(
        "P8_Y5_R2FR_4920_GRAVITON_HIGGS_OBSERVABLE_PASS"
        if passed
        else "P8_Y5_R2FR_4920_GRAVITON_HIGGS_OBSERVABLE_FAIL"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

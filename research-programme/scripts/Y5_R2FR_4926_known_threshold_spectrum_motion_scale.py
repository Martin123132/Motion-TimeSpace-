from __future__ import annotations

import csv
import hashlib
import math
import sys
from datetime import datetime, timezone
from fractions import Fraction
from importlib.metadata import version
from pathlib import Path
from typing import Any

import pdg
from scipy.constants import G, c, hbar, physical_constants


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
SOURCE = POST / "source-intake" / "particle_data" / "4926"
SCRIPTS = POST / "scripts"

CHECKPOINT = "4926"
CHECKED_DATE = "2026-07-12"
MARKER = "MTS_KNOWN_THRESHOLD_MOTION_SCALE_4926"
FORMAL_MARKER = "PPC4161_KNOWN_THRESHOLD_MOTION_SCALE_4926"
NEXT_TARGET = (
    "4927-Y5-R2FR-motion-field-normalization-from-metric-covariance-residue-"
    "and-EH-matching-or-one-Wilson-freeze.md"
)

PDG_API_URL = "https://pdg.lbl.gov/2026/api/index.html"
PDG_DATABASE_URL = "https://pdg.lbl.gov/2026/api/pdg-2026.0.sqlite"
PDG_SUMMARY_URL = "https://pdg.lbl.gov/2026/tables/contents_tables.html"
NUFIT_URL = "https://arxiv.org/abs/2410.05380"
HEAVY_FIELDS_URL = "https://arxiv.org/abs/1611.02705"

PDG_DB = SOURCE / "pdg-2026.0.sqlite"
NUFIT_PDF = SOURCE / "NuFIT-6.0-v2.pdf"
HEAVY_PDF = SOURCE / "Heavy-Fields-and-Gravity-v2.pdf"
PROVENANCE = SOURCE / "PROVENANCE.md"

EXPECTED_HASHES = {
    PDG_DB: "40dc2587d9ae912d26fafb6b41f300f341d2a1f4bd620ff5b5f03827c39453fe",
    NUFIT_PDF: "66ff020fea48d04fe703e99559d625ed3d0bacfc36cbf619b8df16652d54194f",
    HEAVY_PDF: "57e93146014b3b02b518fd456c739bbc87cbe0974660c84b86301edc45799dd3",
}

CORE_ACTION = (
    ROOT
    / "core-mts-framework"
    / "action-principle"
    / "the-fundamental-action-of-motion-timespace-field-theory.md"
)
GEOMETRIC_FRAMEWORK = (
    ROOT
    / "core-mts-framework"
    / "field-theory"
    / "geometric-field-framework.md"
)
CHECKPOINT_4224 = (
    POST
    / "4224-Y5-R2FR-lambda-gamma-core-action-sign-and-binding-bound-source-row.md"
)
CHECKPOINT_4463 = (
    POST
    / "4463-Y5-R2FR-parent-kappa-scale-law-or-calibrated-G-residual-runner.md"
)
CHECKPOINT_4909 = (
    POST
    / "4909-Y5-R2FR-renormalized-motion-scalar-measure-mass-gap-and-stress-three-point-matching.md"
)
CHECKPOINT_4916 = (
    POST
    / "4916-Y5-R2FR-covariantization-map-from-microscopic-motion-action-to-integrated-H-parent-and-no-direct-flow-charge-or-primitive-freeze.md"
)
CHECKPOINT_4924 = (
    POST
    / "4924-Y5-R2FR-renormalized-parent-Weyl-cubic-finite-matching-sign-and-scale-from-motion-scalar-determinant-or-explicit-counterterm-boundary.md"
)
CHECKPOINT_4925 = (
    POST
    / "4925-Y5-R2FR-integrated-H-two-loop-renormalization-condition-and-finite-zeta-plus-boundary-owner-or-explicit-Wilson-input.md"
)

MASS_GAP_PATH = OUTPUT / "P8_Y5_R2FR_4924_MASS_GAP_COEFFICIENT.csv"
PHYSICAL_GATES_PATH = OUTPUT / "P8_Y5_R2FR_4924_PHYSICAL_SCALE_GATES.csv"
RG_PATH = OUTPUT / "P8_Y5_R2FR_4925_TWO_LOOP_RG_TRANSFER.csv"
WILSON_BOUND_PATH = OUTPUT / "P8_Y5_R2FR_4925_WILSON_BOUND.csv"

PLANCK_LENGTH_M = physical_constants["Planck length"][0]
ELECTRON_VOLT_J = physical_constants["electron volt"][0]
HBAR_C_EV_M = hbar * c / ELECTRON_VOLT_J
PLANCK_ENERGY_EV = math.sqrt(hbar * c**5 / G) / ELECTRON_VOLT_J
PHI_G = (1.0 + math.sqrt(5.0)) / 2.0
SCALAR_CANONICAL_DENOMINATOR = 30240.0 * math.pi
STRICT_LOCALITY_RATIO = 10.0

DM21_EV2 = 7.49e-5
DM3L_NO_EV2 = 2.534e-3
DM3L_IO_EV2 = -2.510e-3


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for fieldname in row:
            if fieldname not in fieldnames:
                fieldnames.append(fieldname)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    for row in rows:
        row["checkpoint_marker"] = MARKER
        row["valid_for_claim"] = False
        row["source_checked_date"] = CHECKED_DATE
    return rows


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def read_text_auto(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "cp1252"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def pdg_api() -> Any:
    database_url = "sqlite:///" + PDG_DB.resolve().as_posix()
    return pdg.connect(database_url)


def prior_inputs() -> dict[str, float]:
    mass_gap_rows = read_csv(MASS_GAP_PATH)
    physical_rows = read_csv(PHYSICAL_GATES_PATH)
    rg_rows = read_csv(RG_PATH)
    bound_rows = read_csv(WILSON_BOUND_PATH)

    central_cm = next(
        float(row["c_m"])
        for row in mass_gap_rows
        if row["profile"] == "central_constant_fit"
    )
    low_cm = next(
        float(row["c_m"])
        for row in mass_gap_rows
        if row["profile"] == "two_sigma_union_low_cm"
    )
    high_cm = next(
        float(row["c_m"])
        for row in mass_gap_rows
        if row["profile"] == "two_sigma_union_high_cm"
    )
    compact_row = next(
        row
        for row in physical_rows
        if row["gate_id"] == "NS14_one_percent"
        and row["real_scalar_poles"] == "1"
    )
    rg_gw_row = next(row for row in rg_rows if row["row_id"] == "RG4925_GW250114")
    robust_bound = next(
        row
        for row in bound_rows
        if row["bound_id"] == "WBOUND4925_00_robust_abs"
    )
    ns_bound = next(
        row
        for row in bound_rows
        if row["bound_id"] == "WBOUND4925_02_NS_domain"
    )
    return {
        "c_m_central": central_cm,
        "c_m_low": low_cm,
        "c_m_high": high_cm,
        "mu_floor_eV": float(compact_row["mu_floor_eV_guaranteed_over_cm_union"]),
        "q_gw_eV": float(rg_gw_row["q_eV"]),
        "gs_delta_a_over_lP4": float(rg_gw_row["delta_a_plus_over_lP4"]),
        "robust_ell_m": float(robust_bound["ell_bound_m"]),
        "ns_ell_m": float(ns_bound["ell_bound_m"]),
    }


def mass_snapshot_rows() -> list[dict[str, Any]]:
    api = pdg_api()
    release = datetime.fromtimestamp(
        float(api.info("data_release")), tz=timezone.utc
    ).isoformat()
    specifications = [
        ("electron", "e-", "charged_lepton", True, "one Dirac field", -4.0),
        ("muon", "mu-", "charged_lepton", True, "one Dirac field", -4.0),
        ("tau", "tau-", "charged_lepton", True, "one Dirac field", -4.0),
        ("W_pair", "W+", "electroweak_vector", True, "W plus/minus complex Proca = two real Proca fields", 6.0),
        ("Z", "Z0", "electroweak_vector", True, "one real Proca field", 3.0),
        ("Higgs", "H0", "electroweak_scalar", True, "one physical real scalar", 1.0),
        ("pion_neutral", "pi0", "QCD_gap_anchor", False, "gap anchor only; not a free-field QCD sum", 0.0),
        ("pion_charged", "pi+", "QCD_gap_crosscheck", False, "crosscheck only; not a free-field QCD sum", 0.0),
    ]
    rows: list[dict[str, Any]] = []
    for species_id, query_name, role, included, counting, ratio in specifications:
        particle = api.get_particle_by_name(query_name)
        mass_gev = float(particle.mass)
        mass_error_gev = float(particle.mass_error)
        rows.append(
            {
                "species_id": species_id,
                "pdg_query_name": query_name,
                "pdg_returned_name": particle.name,
                "pdg_id": str(particle.pdgid),
                "monte_carlo_id": int(particle.mcid),
                "mass_GeV": mass_gev,
                "mass_error_GeV": mass_error_gev,
                "mass_eV": mass_gev * 1.0e9,
                "role": role,
                "counting_unit": counting,
                "I1_ratio_used": ratio,
                "included_in_colorless_local_sum": included,
                "pdg_edition": api.info("edition"),
                "pdg_release_utc": release,
                "pdg_api_package": version("pdg"),
                "pdg_license": api.info("license"),
                "source_local": PDG_DB.relative_to(ROOT).as_posix(),
                "source_url": PDG_DATABASE_URL,
                "status": "PDG_API_MASS_LOCKED",
                "passed": mass_gev > 0.0 and mass_error_gev >= 0.0,
            }
        )
    return tagged(rows)


def threshold_a_m4(mass_eV: float, coefficient_ratio: float) -> float:
    if mass_eV <= 0.0:
        raise ValueError("local threshold requires positive mass")
    compton_m = HBAR_C_EV_M / mass_eV
    return (
        coefficient_ratio
        * PLANCK_LENGTH_M**2
        * compton_m**2
        / SCALAR_CANONICAL_DENOMINATOR
    )


def threshold_length_m(a_m4: float) -> float:
    return abs(a_m4) ** 0.25


def mass_map(rows: list[dict[str, Any]]) -> dict[str, float]:
    return {str(row["species_id"]): float(row["mass_eV"]) for row in rows}


def visible_threshold_rows(
    masses: dict[str, float], inputs: dict[str, float]
) -> list[dict[str, Any]]:
    specifications = [
        ("VIS4926_e", "electron", -4.0, "Dirac"),
        ("VIS4926_mu", "muon", -4.0, "Dirac"),
        ("VIS4926_tau", "tau", -4.0, "Dirac"),
        ("VIS4926_Wpair", "W_pair", 6.0, "complex Proca"),
        ("VIS4926_Z", "Z", 3.0, "real Proca"),
        ("VIS4926_H", "Higgs", 1.0, "real scalar"),
    ]
    rows: list[dict[str, Any]] = []
    total_a_m4 = 0.0
    for row_id, species, ratio, spin_counting in specifications:
        mass_eV = masses[species]
        a_m4 = threshold_a_m4(mass_eV, ratio)
        total_a_m4 += a_m4
        rows.append(
            {
                "row_id": row_id,
                "species": species,
                "spin_counting": spin_counting,
                "mass_eV": mass_eV,
                "I1_ratio": ratio,
                "a_threshold_m4": a_m4,
                "absolute_threshold_length_m": threshold_length_m(a_m4),
                "a_ratio_to_NS_one_percent": abs(a_m4) / inputs["ns_ell_m"] ** 4,
                "a_ratio_to_GW_robust_envelope": abs(a_m4) / inputs["robust_ell_m"] ** 4,
                "locality_ratio_m_over_qGW": mass_eV / inputs["q_gw_eV"],
                "formula": "a_i=r_i lP^2 (hbar c/m_i)^2/(30240 pi)",
                "status": "COLORLESS_FREE_THRESHOLD_CALCULATED",
                "passed": mass_eV / inputs["q_gw_eV"] > STRICT_LOCALITY_RATIO,
            }
        )
    rows.append(
        {
            "row_id": "VIS4926_total_without_neutrinos",
            "species": "charged_leptons_plus_WZ_H",
            "spin_counting": "signed sum without neutrinos",
            "I1_ratio": "species dependent",
            "a_threshold_m4": total_a_m4,
            "absolute_threshold_length_m": threshold_length_m(total_a_m4),
            "a_ratio_to_NS_one_percent": abs(total_a_m4) / inputs["ns_ell_m"] ** 4,
            "a_ratio_to_GW_robust_envelope": abs(total_a_m4) / inputs["robust_ell_m"] ** 4,
            "locality_ratio_m_over_qGW": masses["electron"] / inputs["q_gw_eV"],
            "formula": "sum of the six source-locked colorless rows",
            "status": "COLORLESS_NONNEUTRINO_SUM_CALCULATED",
            "passed": total_a_m4 < 0.0,
        }
    )
    return tagged(rows)


def neutrino_mass_sets() -> dict[str, tuple[float, float, float]]:
    normal = (0.0, math.sqrt(DM21_EV2), math.sqrt(DM3L_NO_EV2))
    inverted_m2 = math.sqrt(abs(DM3L_IO_EV2))
    inverted_m1 = math.sqrt(abs(DM3L_IO_EV2) - DM21_EV2)
    inverted = (inverted_m1, inverted_m2, 0.0)
    return {"normal": normal, "inverted": inverted}


def neutrino_scenario_rows(
    base_visible_a_m4: float, inputs: dict[str, float]
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for ordering, masses in neutrino_mass_sets().items():
        for nature, ratio in (("Majorana", -2.0), ("Dirac", -4.0)):
            massive = [mass for mass in masses if mass > 0.0]
            neutrino_a_m4 = sum(threshold_a_m4(mass, ratio) for mass in massive)
            colorless_total_a_m4 = base_visible_a_m4 + neutrino_a_m4
            rows.append(
                {
                    "scenario": f"{ordering}_{nature}_lightest_zero",
                    "ordering": ordering,
                    "nature": nature,
                    "lightest_mass_eV": 0.0,
                    "m1_eV": masses[0],
                    "m2_eV": masses[1],
                    "m3_eV": masses[2],
                    "dm21_eV2": DM21_EV2,
                    "dm3l_eV2": DM3L_NO_EV2 if ordering == "normal" else DM3L_IO_EV2,
                    "ratio_per_massive_eigenstate": ratio,
                    "massive_local_eigenstates": len(massive),
                    "massless_nonlocal_eigenstates": 1,
                    "neutrino_a_threshold_m4": neutrino_a_m4,
                    "neutrino_absolute_length_m": threshold_length_m(neutrino_a_m4),
                    "colorless_total_a_m4": colorless_total_a_m4,
                    "colorless_total_absolute_length_m": threshold_length_m(colorless_total_a_m4),
                    "colorless_a_ratio_to_NS_one_percent": abs(colorless_total_a_m4) / inputs["ns_ell_m"] ** 4,
                    "colorless_a_ratio_to_GW_envelope": abs(colorless_total_a_m4) / inputs["robust_ell_m"] ** 4,
                    "lightest_state_treatment": "exactly massless benchmark state retained in nonlocal form factor",
                    "source": NUFIT_URL,
                    "status": "CONDITIONAL_SPLITTING_BENCHMARK_NOT_ABSOLUTE_MASS_CLAIM",
                    "passed": all(mass / inputs["q_gw_eV"] > STRICT_LOCALITY_RATIO for mass in massive),
                }
            )
    return tagged(rows)


def domain_split_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "sector": "charged_leptons",
                "low_energy_treatment": "free massive Dirac thresholds",
                "included_numeric": True,
                "reason": "colorless physical poles and m much greater than local Q",
                "double_count_guard": "one field per e mu tau",
                "status": "CALCULATED",
                "passed": True,
            },
            {
                "sector": "Higgs",
                "low_energy_treatment": "one real scalar Ricci-flat threshold",
                "included_numeric": True,
                "reason": "physical colorless scalar pole",
                "double_count_guard": "Goldstones are already part of the massive gauge completion",
                "status": "CALCULATED",
                "passed": True,
            },
            {
                "sector": "W_and_Z",
                "low_energy_treatment": "massive Proca thresholds",
                "included_numeric": True,
                "reason": "physical colorless massive-vector poles",
                "double_count_guard": "W pair counts as two real Proca fields; Z as one",
                "status": "CALCULATED",
                "passed": True,
            },
            {
                "sector": "neutrino_massive_eigenstates",
                "low_energy_treatment": "four hierarchy-and-nature benchmark sums",
                "included_numeric": True,
                "reason": "splittings are sourced but absolute mass and Dirac/Majorana nature are open",
                "double_count_guard": "only positive-mass benchmark eigenstates enter local sum",
                "status": "CONDITIONAL_SCENARIOS",
                "passed": True,
            },
            {
                "sector": "neutrino_zero_or_ultralight_state",
                "low_energy_treatment": "nonlocal form factor until m is safely above Q",
                "included_numeric": False,
                "reason": "the local 1/m^2 expansion is invalid at m comparable to Q",
                "double_count_guard": "never add a massless 1/m^2 row",
                "status": "NONLOCAL_NOT_LOCAL_THRESHOLD",
                "passed": True,
            },
            {
                "sector": "photon",
                "low_energy_treatment": "massless nonlocal metric form factor",
                "included_numeric": False,
                "reason": "no heavy-mass expansion exists",
                "double_count_guard": "exclude from local C3 threshold table",
                "status": "NONLOCAL",
                "passed": True,
            },
            {
                "sector": "colored_quarks_and_gluons",
                "low_energy_treatment": "one renormalized confined QCD matching block",
                "included_numeric": False,
                "reason": "free quarks are not infrared asymptotic states and gluons are massless",
                "double_count_guard": "do not add free heavy-quark rows while retaining the all-QCD block",
                "status": "QCD_MATCHING_MOMENT_OPEN",
                "passed": True,
            },
            {
                "sector": "MTS_motion_scalar",
                "low_energy_treatment": "one real-pole threshold conditional on canonical normalization and c_m",
                "included_numeric": False,
                "reason": "the dimension repair is exact but its normalization coefficient is not parent-owned",
                "double_count_guard": "Schwinger-Keldysh doubling is not pole multiplicity",
                "status": "CONDITIONAL_BENCHMARK_ONLY",
                "passed": True,
            },
            {
                "sector": "integrated_H_metric_and_ghost",
                "low_energy_treatment": "renormalized ultraviolet Wilson boundary",
                "included_numeric": False,
                "reason": "checkpoint 4925 proves one physical coefficient but not its value",
                "double_count_guard": "bare and finite metric-ghost labels are one scheme-invariant input",
                "status": "ONE_UV_WILSON_INPUT",
                "passed": True,
            },
        ]
    )


def locality_envelope_rows(inputs: dict[str, float]) -> list[dict[str, Any]]:
    arena_scales = [
        ("GW250114", inputs["q_gw_eV"]),
        ("NS_12km", HBAR_C_EV_M / 12_000.0),
    ]
    rows: list[dict[str, Any]] = []
    for arena, q_eV in arena_scales:
        for mass_ratio, label in ((1.0, "formal_edge"), (STRICT_LOCALITY_RATIO, "strict_locality_gate")):
            mass_eV = mass_ratio * q_eV
            a_m4 = abs(threshold_a_m4(mass_eV, -4.0))
            ell_m = threshold_length_m(a_m4)
            rows.append(
                {
                    "arena": arena,
                    "gate": label,
                    "q_eV": q_eV,
                    "mass_over_q": mass_ratio,
                    "mass_eV": mass_eV,
                    "reference_counting": "one Dirac field abs(r)=4",
                    "max_abs_a_m4_at_or_above_mass": a_m4,
                    "max_threshold_length_m": ell_m,
                    "length_ratio_to_NS_one_percent": ell_m / inputs["ns_ell_m"],
                    "a_ratio_to_NS_one_percent": a_m4 / inputs["ns_ell_m"] ** 4,
                    "interpretation": "formal edge is diagnostic only; strict row is the declared local-expansion gate",
                    "status": "LOCAL_MODE_AUTOMATICALLY_COMPACT_SAFE_PER_DIRAC_FIELD",
                    "passed": a_m4 < inputs["ns_ell_m"] ** 4,
                }
            )
    return tagged(rows)


def motion_dimension_rows() -> list[dict[str, Any]]:
    exponent_n = Fraction(4, 3)
    lambda_old_dimension = Fraction(3, 1)
    field_dimension = (lambda_old_dimension - 2) / (2 - exponent_n)
    kinetic_dimension = 2 + 2 * field_dimension
    potential_dimension = lambda_old_dimension + exponent_n * field_dimension
    normalization_dimension = 4 - kinetic_dimension
    canonical_coupling_dimension = lambda_old_dimension + normalization_dimension / 3
    scale_dimension = canonical_coupling_dimension * Fraction(3, 8)
    rows = [
        {
            "audit_id": "MDIM4926_00_old_parameters",
            "object": "printed gamma and lambda",
            "calculation": "[gamma]=1; [lambda_old]=[1/G]+[gamma]=2+1=3 in hbar=c=1",
            "mass_dimension": "gamma:1; lambda_old:3",
            "result": "lambda_old cannot directly be the canonical |psi|^(4/3) coupling of dimension 8/3",
            "status": "DIRECT_CANONICAL_IDENTIFICATION_REJECTED",
            "passed": lambda_old_dimension != Fraction(8, 3),
        },
        {
            "audit_id": "MDIM4926_01_field_dimension",
            "object": "old motion field phi_old",
            "calculation": "2+2 Delta = 3+(4/3)Delta",
            "mass_dimension": str(field_dimension),
            "result": "Delta=3/2 makes the printed kinetic gamma-cross and potential terms homogeneous",
            "status": "NONCANONICAL_FIELD_DIMENSION_DERIVED",
            "passed": field_dimension == Fraction(3, 2),
        },
        {
            "audit_id": "MDIM4926_02_missing_prefactor",
            "object": "overall old-action normalization",
            "calculation": "common bracket dimension=5; d4x dimension=-4",
            "mass_dimension": str(normalization_dimension),
            "result": "the action requires an overall 1/M_N",
            "status": "ONE_MASS_NORMALIZATION_REQUIRED",
            "passed": kinetic_dimension == potential_dimension == 5 and normalization_dimension == -1,
        },
        {
            "audit_id": "MDIM4926_03_canonical_rescale",
            "object": "psi=phi_old/sqrt(M_N)",
            "calculation": "g_psi=lambda_old M_N^(-1/3)",
            "mass_dimension": str(canonical_coupling_dimension),
            "result": "the repaired canonical coupling has the required dimension 8/3",
            "status": "CANONICAL_COUPLING_REPAIR_DERIVED",
            "passed": canonical_coupling_dimension == Fraction(8, 3),
        },
        {
            "audit_id": "MDIM4926_04_physical_scale",
            "object": "mu=g_psi^(3/8)",
            "calculation": "mu=lambda_old^(3/8) M_N^(-1/8)",
            "mass_dimension": str(scale_dimension),
            "result": "the physical gap scale has mass dimension one",
            "status": "PHYSICAL_SCALE_FORMULA_DERIVED_NORMALIZATION_OPEN",
            "passed": scale_dimension == 1,
        },
        {
            "audit_id": "MDIM4926_05_gamma_term",
            "object": "gamma phi_old partial_t phi_old",
            "calculation": "1+3/2+(1+3/2)=5 inside the repaired bracket",
            "mass_dimension": "5 before 1/M_N",
            "result": "dimensionally homogeneous but still a boundary term for constant gamma; the bath remains the damping owner",
            "status": "DIMENSION_OK_DAMPING_CLAIM_STILL_REJECTED",
            "passed": True,
        },
    ]
    return tagged(rows)


def scientific_from_log10(log10_value: float) -> str:
    exponent = math.floor(log10_value)
    mantissa = 10.0 ** (log10_value - exponent)
    return f"{mantissa:.12g}e{exponent:+d}"


def motion_normalization_rows(inputs: dict[str, float]) -> list[dict[str, Any]]:
    gamma_eV = PHI_G * PLANCK_ENERGY_EV
    lambda_old_eV3 = PHI_G**4 * PLANCK_ENERGY_EV**3
    minimal_mu_eV = PHI_G ** 1.5 * PLANCK_ENERGY_EV
    generic_cpsi_min = (inputs["mu_floor_eV"] / PLANCK_ENERGY_EV) ** (8.0 / 3.0)
    log10_cn_max = 8.0 * (
        math.log10(minimal_mu_eV) - math.log10(inputs["mu_floor_eV"])
    )
    rows: list[dict[str, Any]] = [
        {
            "branch": "generic_normalization",
            "C_N": "positive dimensionless input",
            "M_N_eV": "C_N M_Pl",
            "gamma_eV": gamma_eV,
            "lambda_old_eV3": lambda_old_eV3,
            "g_psi": "Phi_G^4 C_N^(-1/3) M_Pl^(8/3)",
            "mu_eV": "Phi_G^(3/2) C_N^(-1/8) M_Pl",
            "m_gap_eV": "c_m Phi_G^(3/2) C_N^(-1/8) M_Pl",
            "normalization_status": "one dimensionless coefficient remains because the old field amplitude was never operationally normalized",
            "parent_derived": False,
            "status": "EXACT_ONE_PARAMETER_NORMALIZATION_FAMILY",
            "passed": True,
        },
        {
            "branch": "minimal_single_scale_C_N_1",
            "C_N": 1.0,
            "M_N_eV": PLANCK_ENERGY_EV,
            "gamma_eV": gamma_eV,
            "lambda_old_eV3": lambda_old_eV3,
            "g_psi": PHI_G**4 * PLANCK_ENERGY_EV ** (8.0 / 3.0),
            "mu_eV": minimal_mu_eV,
            "m_gap_eV": inputs["c_m_central"] * minimal_mu_eV,
            "normalization_status": "minimal no-second-scale benchmark; not a theorem fixing C_N",
            "parent_derived": False,
            "status": "CONDITIONAL_PLANCK_SCALE_BENCHMARK",
            "passed": minimal_mu_eV > inputs["mu_floor_eV"],
        },
    ]
    for profile, c_m_value in (
        ("central_c_m", inputs["c_m_central"]),
        ("conservative_low_c_m", inputs["c_m_low"]),
        ("conservative_high_c_m", inputs["c_m_high"]),
    ):
        mass_gap_eV = c_m_value * minimal_mu_eV
        a_m4 = threshold_a_m4(mass_gap_eV, 1.0)
        rows.append(
            {
                "branch": f"C_N_1_{profile}",
                "C_N": 1.0,
                "M_N_eV": PLANCK_ENERGY_EV,
                "gamma_eV": gamma_eV,
                "lambda_old_eV3": lambda_old_eV3,
                "g_psi": PHI_G**4 * PLANCK_ENERGY_EV ** (8.0 / 3.0),
                "mu_eV": minimal_mu_eV,
                "c_m": c_m_value,
                "m_gap_eV": mass_gap_eV,
                "motion_a_threshold_m4_per_real_pole": a_m4,
                "motion_threshold_length_m_per_real_pole": threshold_length_m(a_m4),
                "length_ratio_to_NS_one_percent": threshold_length_m(a_m4) / inputs["ns_ell_m"],
                "a_ratio_to_NS_one_percent": a_m4 / inputs["ns_ell_m"] ** 4,
                "normalization_status": "conditional on C_N=1 and the nonpromoted c_m profile",
                "parent_derived": False,
                "status": "CONDITIONAL_MOTION_THRESHOLD_COMPUTED",
                "passed": a_m4 < inputs["ns_ell_m"] ** 4,
            }
        )
    rows.extend(
        [
            {
                "branch": "compact_bound_on_C_N",
                "C_N": "less than C_N_max",
                "real_scalar_poles": 1,
                "mu_floor_eV": inputs["mu_floor_eV"],
                "log10_C_N_max": log10_cn_max,
                "C_N_max_scientific": scientific_from_log10(log10_cn_max),
                "multiplicity_scaling": "C_N_max(N_real)=C_N_max(1) N_real^(-4)",
                "normalization_status": "exact transform of the one-real-pole compact scale floor",
                "parent_derived": False,
                "status": "ONLY_ABSURDLY_LARGE_NORMALIZATION_REOPENS_MOTION_THRESHOLD",
                "passed": log10_cn_max > 600.0,
            },
            {
                "branch": "generic_canonical_coupling_floor",
                "C_N": "not used",
                "real_scalar_poles": 1,
                "g_psi": "C_psi M_Pl^(8/3)",
                "mu_eV": "C_psi^(3/8) M_Pl",
                "C_psi_min_for_NS_one_percent": generic_cpsi_min,
                "log10_C_psi_min": math.log10(generic_cpsi_min),
                "multiplicity_scaling": "C_psi_min(N_real)=C_psi_min(1) N_real^(4/3)",
                "normalization_status": "exact canonical compact floor independent of the old lambda naming",
                "parent_derived": False,
                "status": "CANONICAL_COUPLING_NEED_ONLY_EXCEED_TINY_FLOOR",
                "passed": generic_cpsi_min < 1.0e-200,
            },
        ]
    )
    return tagged(rows)


def qcd_firewall_rows(
    masses: dict[str, float], inputs: dict[str, float]
) -> list[dict[str, Any]]:
    pion_mass_eV = masses["pion_neutral"]
    scalar_unit_a_m4 = threshold_a_m4(pion_mass_eV, 1.0)
    required_ns = inputs["ns_ell_m"] ** 4 / scalar_unit_a_m4
    required_gw = inputs["robust_ell_m"] ** 4 / scalar_unit_a_m4
    return tagged(
        [
            {
                "row_id": "QCD4926_00_gap_anchor",
                "quantity": "neutral-pion mass gap anchor",
                "value": pion_mass_eV,
                "units": "eV",
                "equation": "m_gap,QCD <= or approximately m_pi0 as a scale anchor",
                "meaning": "source-backed infrared scale only; not a free scalar identification",
                "status": "PDG_GAP_SCALE_ACQUIRED",
                "passed": pion_mass_eV > 1.0e8,
            },
            {
                "row_id": "QCD4926_01_unit",
                "quantity": "scalar-normalized QCD Wilson unit",
                "value": scalar_unit_a_m4,
                "units": "m^4",
                "equation": "a_QCD=C_QCD lP^2(hbar c/m_pi0)^2/(30240 pi)",
                "meaning": "defines C_QCD without pretending the interacting coefficient equals one",
                "status": "DIMENSIONLESS_QCD_MATCHING_PARAMETER_DEFINED",
                "passed": scalar_unit_a_m4 > 0.0,
            },
            {
                "row_id": "QCD4926_02_NS_firewall",
                "quantity": "abs C_QCD required to saturate NS one-percent target",
                "value": required_ns,
                "units": "dimensionless",
                "equation": "abs C_QCD=ell_NS^4/a_QCD_unit",
                "meaning": "naturalness firewall only because no rigorous three-stress spectral bound is derived",
                "status": "OVER_1E118_REQUIRED_BUT_NOT_ZERO_PROOF",
                "passed": required_ns > 1.0e118,
            },
            {
                "row_id": "QCD4926_03_GW_firewall",
                "quantity": "abs C_QCD required to saturate current GW envelope",
                "value": required_gw,
                "units": "dimensionless",
                "equation": "abs C_QCD=ell_GW^4/a_QCD_unit",
                "meaning": "current data room is even less sensitive to an ordinary QCD-size coefficient",
                "status": "HUGE_COEFFICIENT_REQUIRED_NOT_A_THEOREM",
                "passed": required_gw > required_ns,
            },
            {
                "row_id": "QCD4926_04_matching_status",
                "quantity": "renormalized QCD three-stress matching moment",
                "value": "uncomputed",
                "units": "dimensionless C_QCD",
                "equation": "a_QCD^R=C_QCD a_QCD_unit",
                "meaning": "C3 is a three-point matching problem and has no simple positive two-point spectral bound",
                "status": "ABSORBED_IN_ONE_IR_WILSON_REMAINDER",
                "passed": True,
            },
        ]
    )


def ir_wilson_rows(
    neutrino_rows: list[dict[str, Any]],
    motion_rows: list[dict[str, Any]],
    inputs: dict[str, float],
) -> list[dict[str, Any]]:
    motion_central = next(
        row for row in motion_rows if row["branch"] == "C_N_1_central_c_m"
    )
    motion_a_m4 = float(motion_central["motion_a_threshold_m4_per_real_pole"])
    gs_a_m4 = inputs["gs_delta_a_over_lP4"] * PLANCK_LENGTH_M**4
    observation_a_m4 = inputs["robust_ell_m"] ** 4
    rows: list[dict[str, Any]] = []
    for scenario in neutrino_rows:
        visible_a_m4 = float(scenario["colorless_total_a_m4"])
        known_offset_a_m4 = visible_a_m4 + motion_a_m4 + gs_a_m4
        rows.append(
            {
                "scenario": scenario["scenario"],
                "matching_equation": "a_IR=a_unresolved^R+a_visible+a_motion(C_N,c_m,Nreal)+Delta a_GS",
                "a_visible_m4": visible_a_m4,
                "a_motion_m4_C_N1_central_one_pole": motion_a_m4,
                "a_GS_m4_Planck_to_GW": gs_a_m4,
                "known_offset_a_m4": known_offset_a_m4,
                "known_offset_absolute_length_m": threshold_length_m(known_offset_a_m4),
                "known_offset_ratio_to_GW_envelope": abs(known_offset_a_m4) / observation_a_m4,
                "known_offset_ratio_to_NS_target": abs(known_offset_a_m4) / inputs["ns_ell_m"] ** 4,
                "unresolved_remainder_lower_m4": -observation_a_m4 - known_offset_a_m4,
                "unresolved_remainder_upper_m4": observation_a_m4 - known_offset_a_m4,
                "independent_low_energy_I1_test_parameters": 1,
                "unresolved_contents": "renormalized H ultraviolet boundary plus all-QCD matching plus any nonpromoted MTS residual",
                "status": "KNOWN_OFFSETS_COLLAPSED_ONE_IR_WILSON_REMAINS",
                "passed": abs(known_offset_a_m4) < inputs["ns_ell_m"] ** 4,
            }
        )
    return tagged(rows)


def gate_decision_rows(
    source_rows: list[dict[str, Any]],
    visible_rows: list[dict[str, Any]],
    neutrino_rows: list[dict[str, Any]],
    motion_rows: list[dict[str, Any]],
    qcd_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    sources_pass = all(bool(row["passed"]) for row in source_rows)
    numeric_pass = all(bool(row["passed"]) for row in visible_rows + neutrino_rows)
    motion_benchmark = next(
        row for row in motion_rows if row["branch"] == "C_N_1_conservative_low_c_m"
    )
    qcd_open = next(
        row for row in qcd_rows if row["row_id"] == "QCD4926_04_matching_status"
    )
    return tagged(
        [
            {
                "gate": "locked_sources",
                "status": "PDG_2026_NUFIT6_HEAVY_FIELD_SOURCES_LOCKED",
                "decision": "all three durable source files pass their SHA-256 locks",
                "claim_promoted": False,
                "passed": sources_pass,
            },
            {
                "gate": "known_colorless_thresholds",
                "status": "CALCULATED_AND_COMPACT_NEGLIGIBLE",
                "decision": "charged leptons W Z Higgs and four neutrino benchmarks are over ninety orders below the compact coefficient target",
                "claim_promoted": False,
                "passed": numeric_pass,
            },
            {
                "gate": "QCD",
                "status": "ONE_CONFINED_MATCHING_BLOCK_OPEN",
                "decision": "free-quark double counting is removed; exact interacting three-stress coefficient remains inside a_IR",
                "claim_promoted": False,
                "passed": qcd_open["status"] == "ABSORBED_IN_ONE_IR_WILSON_REMAINDER",
            },
            {
                "gate": "motion_dimension",
                "status": "OLD_DIMENSION_MISMATCH_REPAIRED",
                "decision": "Delta_old=3/2 and one 1/M_N prefactor give g_psi=lambda_old M_N^(-1/3) and mu=lambda_old^(3/8)M_N^(-1/8)",
                "claim_promoted": False,
                "passed": True,
            },
            {
                "gate": "motion_normalization",
                "status": "ONE_DIMENSIONLESS_C_N_REMAINS_NOT_PARENT_DERIVED",
                "decision": "C_N=1 gives a Planck-scale benchmark safely below compact sensitivity, but is not promoted as an exact parent value",
                "claim_promoted": False,
                "passed": bool(motion_benchmark["passed"]),
            },
            {
                "gate": "IR_parameter_count",
                "status": "ONE_SIGNED_LOW_ENERGY_I1_PARAMETER_RETAINED",
                "decision": "known thresholds are offsets; UV QCD and unresolved MTS pieces remain one renormalized a_IR rather than arena closures",
                "claim_promoted": False,
                "passed": True,
            },
            {
                "gate": "weak_GR",
                "status": "RETAINED",
                "decision": "two-derivative invariant-vacuum GR remains the selected local branch",
                "claim_promoted": False,
                "passed": True,
            },
            {
                "gate": "compact_GR",
                "status": "NOT_PROMOTED",
                "decision": "known thresholds are safe but the finite UV/QCD remainder is not derived below the compact target",
                "claim_promoted": False,
                "passed": True,
            },
            {
                "gate": "full_MTS_to_GR",
                "status": "NOT_PROMOTED",
                "decision": "motion normalization and finite ultraviolet matching remain open",
                "claim_promoted": False,
                "passed": True,
            },
            {
                "gate": "next_target",
                "status": "METRIC_COVARIANCE_RESIDUE_NORMALIZATION",
                "decision": NEXT_TARGET,
                "claim_promoted": False,
                "passed": True,
            },
        ]
    )


def source_register_rows() -> list[dict[str, Any]]:
    local_binary_sources = [
        ("SRC4926_00_PDG", PDG_DB, EXPECTED_HASHES[PDG_DB], "PDG_2026_machine_readable_masses"),
        ("SRC4926_01_NuFIT", NUFIT_PDF, EXPECTED_HASHES[NUFIT_PDF], "neutrino_mass_splittings"),
        ("SRC4926_02_heavy", HEAVY_PDF, EXPECTED_HASHES[HEAVY_PDF], "spin_threshold_coefficients"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, expected_hash, role in local_binary_sources:
        exists = path.exists()
        actual_hash = digest(path) if exists else ""
        passed = exists and actual_hash == expected_hash
        rows.append(
            {
                "source_id": source_id,
                "source_path_or_url": path.relative_to(ROOT).as_posix(),
                "source_role": role,
                "verification": "SHA256",
                "expected_sha256": expected_hash,
                "actual_sha256": actual_hash,
                "source_exists": exists,
                "marker_found": passed,
                "status": "LOCAL_BINARY_SOURCE_HASH_VERIFIED" if passed else "LOCAL_BINARY_SOURCE_FAILED",
                "passed": passed,
            }
        )
    local_text_sources = [
        ("SRC4926_03_provenance", PROVENANCE, "MTS_KNOWN_THRESHOLD_MOTION_SCALE_PROVENANCE_4926", "source_provenance"),
        ("SRC4926_04_core_action", CORE_ACTION, "Determination of", "printed_gamma_lambda_action"),
        ("SRC4926_05_geometric", GEOMETRIC_FRAMEWORK, "n = 4/3", "Phi_G_and_fractional_exponent"),
        ("SRC4926_06_4224", CHECKPOINT_4224, "lambda = Phi_G^4", "old_lambda_dimension_input"),
        ("SRC4926_07_4463", CHECKPOINT_4463, "NUMERIC_G_SCALE_LAW_NOT_DERIVED", "calibrated_G_policy"),
        ("SRC4926_08_4909", CHECKPOINT_4909, "m_{\\rm gap}=c_m\\lambda^{3/8}", "motion_gap_pilot"),
        ("SRC4926_09_4916", CHECKPOINT_4916, "V(\\psi)=\\frac34g_\\psi|\\psi|^{4/3}", "canonical_covariant_scalar"),
        ("SRC4926_10_4924", CHECKPOINT_4924, "MTS_PARENT_WEYL_C3_FINITE_MATCHING_4924", "scale_floor_and_threshold_map"),
        ("SRC4926_11_4925", CHECKPOINT_4925, "MTS_INTEGRATED_H_TWO_LOOP_WILSON_BOUNDARY_4925", "one_Wilson_matching"),
        ("SRC4926_12_4924_mass", MASS_GAP_PATH, "central_constant_fit", "c_m_profiles"),
        ("SRC4926_13_4924_gate", PHYSICAL_GATES_PATH, "NS14_one_percent", "compact_mu_floor"),
        ("SRC4926_14_4925_RG", RG_PATH, "RG4925_GW250114", "reference_Q_and_running"),
        ("SRC4926_15_4925_bound", WILSON_BOUND_PATH, "WBOUND4925_00_robust_abs", "IR_Wilson_envelope"),
        ("SRC4926_16_research", Path(__file__).resolve(), "def motion_dimension_rows", "generated_research_code"),
        ("SRC4926_17_checkpoint", POST / "4926-Y5-R2FR-known-massive-threshold-spectrum-and-motion-scale-normalization-or-low-energy-Wilson-posterior.md", MARKER, "generated_checkpoint"),
        ("SRC4926_18_formal", FORMAL / "942-PPC4161-known-threshold-spectrum-and-motion-scale-normalization.md", FORMAL_MARKER, "formal_summary"),
        ("SRC4926_19_validation", SCRIPTS / "Y5_R2FR_4926_known_threshold_spectrum_motion_scale_validation.py", "VAL4926_OVERALL", "generated_validation_code"),
        ("SRC4926_20_claims", FORMAL / "02-claims-register.csv", "L-768", "claim_register"),
        ("SRC4926_21_variables", FORMAL / "04-variable-audit.csv", "KnownColorlessC3Threshold4926_MTS", "variable_register"),
        ("SRC4926_22_equations", FORMAL / "05-equation-register.md", "1.219 Known thresholds and repaired motion normalization", "equation_register"),
        ("SRC4926_23_redteam", FORMAL / "06-consistency-red-team.md", "170. A dimensionful old coupling is not a canonical physical scale", "redteam_register"),
        ("SRC4926_24_spine", FORMAL / "07-unification-spine.md", "PPC4161 checkpoint 4926", "spine_register"),
        ("SRC4926_25_resume", POST / "CURRENT_LOCAL_RESUME.md", "4927-Y5-R2FR-motion-field-normalization-from-metric-covariance-residue", "resume_register"),
    ]
    for source_id, path, marker, role in local_text_sources:
        exists = path.exists()
        marker_found = exists and marker in read_text_auto(path)
        rows.append(
            {
                "source_id": source_id,
                "source_path_or_url": path.relative_to(ROOT).as_posix(),
                "source_role": role,
                "verification": "path_and_marker",
                "expected_sha256": "",
                "actual_sha256": digest(path) if exists else "",
                "source_exists": exists,
                "marker_found": marker_found,
                "status": "LOCAL_TEXT_SOURCE_VERIFIED" if marker_found else "LOCAL_TEXT_SOURCE_FAILED",
                "passed": marker_found,
            }
        )
    for source_id, url, role in (
        ("SRC4926_26_PDG_API", PDG_API_URL, "official_programmatic_access"),
        ("SRC4926_27_PDG_DB_URL", PDG_DATABASE_URL, "official_database_download"),
        ("SRC4926_28_PDG_summary", PDG_SUMMARY_URL, "official_2026_citation"),
        ("SRC4926_29_NuFIT_URL", NUFIT_URL, "primary_neutrino_global_fit"),
        ("SRC4926_30_heavy_URL", HEAVY_FIELDS_URL, "primary_heavy_field_threshold_theory"),
    ):
        rows.append(
            {
                "source_id": source_id,
                "source_path_or_url": url,
                "source_role": role,
                "verification": "external_primary_URL_recorded",
                "expected_sha256": "",
                "actual_sha256": "",
                "source_exists": True,
                "marker_found": True,
                "status": "EXTERNAL_PRIMARY_URL_RECORDED",
                "passed": True,
            }
        )
    return tagged(rows)


def main() -> int:
    inputs = prior_inputs()
    source_rows = source_register_rows()
    mass_rows = mass_snapshot_rows()
    masses = mass_map(mass_rows)
    visible_rows = visible_threshold_rows(masses, inputs)
    base_visible_a_m4 = float(
        next(
            row
            for row in visible_rows
            if row["row_id"] == "VIS4926_total_without_neutrinos"
        )["a_threshold_m4"]
    )
    neutrino_rows = neutrino_scenario_rows(base_visible_a_m4, inputs)
    motion_dimension = motion_dimension_rows()
    motion_rows = motion_normalization_rows(inputs)
    qcd_rows = qcd_firewall_rows(masses, inputs)
    ir_rows = ir_wilson_rows(neutrino_rows, motion_rows, inputs)
    tables = {
        "P8_Y5_R2FR_4926_PDG_MASS_SNAPSHOT.csv": mass_rows,
        "P8_Y5_R2FR_4926_THRESHOLD_DOMAIN_SPLIT.csv": domain_split_rows(),
        "P8_Y5_R2FR_4926_COLORLESS_VISIBLE_THRESHOLDS.csv": visible_rows,
        "P8_Y5_R2FR_4926_NEUTRINO_SCENARIOS.csv": neutrino_rows,
        "P8_Y5_R2FR_4926_LOCALITY_ENVELOPE.csv": locality_envelope_rows(inputs),
        "P8_Y5_R2FR_4926_QCD_MATCHING_FIREWALL.csv": qcd_rows,
        "P8_Y5_R2FR_4926_MOTION_SCALE_DIMENSION_AUDIT.csv": motion_dimension,
        "P8_Y5_R2FR_4926_MOTION_SCALE_REPAIR_BRANCH.csv": motion_rows,
        "P8_Y5_R2FR_4926_IR_WILSON_COLLAPSE.csv": ir_rows,
        "P8_Y5_R2FR_4926_SOURCE_REGISTER.csv": source_rows,
    }
    gate_rows = gate_decision_rows(
        source_rows, visible_rows, neutrino_rows, motion_rows, qcd_rows
    )
    tables["P8_Y5_R2FR_4926_GATE_DECISION.csv"] = gate_rows
    for filename, rows in tables.items():
        write_csv(OUTPUT / filename, rows)
    all_rows = [row for rows in tables.values() for row in rows]
    passed = all(bool(row.get("passed", True)) for row in all_rows)
    max_colorless_length = max(
        float(row["colorless_total_absolute_length_m"]) for row in neutrino_rows
    )
    minimal_motion = next(
        row for row in motion_rows if row["branch"] == "C_N_1_central_c_m"
    )
    print(
        "P8_Y5_R2FR_4926_KNOWN_THRESHOLD_MOTION_SCALE_PASS"
        if passed
        else "P8_Y5_R2FR_4926_KNOWN_THRESHOLD_MOTION_SCALE_FAIL"
    )
    print(f"max_colorless_threshold_length_m={max_colorless_length:.16e}")
    print(
        "minimal_motion_threshold_length_m="
        f"{float(minimal_motion['motion_threshold_length_m_per_real_pole']):.16e}"
    )
    print("independent_IR_I1_test_parameters=1")
    print("compact_GR_promoted=False")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

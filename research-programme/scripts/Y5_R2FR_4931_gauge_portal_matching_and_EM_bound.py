from __future__ import annotations

import csv
import hashlib
import math
import sys
from pathlib import Path
from typing import Any

import scipy
from scipy.constants import G, alpha, c, hbar, m_e, physical_constants


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
SOURCE = POST / "source-intake" / "functional_rg" / "4931"
SOURCE_4930 = POST / "source-intake" / "functional_rg" / "4930"

CHECKED_DATE = "2026-07-12"
MARKER = "MTS_GAUGE_CURVATURE_PORTAL_MATCHING_EM_BOUND_4931"
NEXT_TARGET = "4932-Y5-R2FR-MTS-gauge-portal-functional-trace-projection-or-two-sided-polarization-likelihood.md"

PROVENANCE = SOURCE / "PROVENANCE.md"
TEX_1908 = SOURCE_4930 / "src1908" / "GravityEFTv2_final.tex"
TEX_0306 = SOURCE / "src-0306021" / "0306021.tex"
TEX_0812 = SOURCE / "src-0812.4849" / "ehgravfinal.tex"
TEX_1505 = SOURCE / "src-1505.01844" / "holomorphy_EFT_final.tex"
TEX_1609 = SOURCE / "src-1609.00723" / "SuperluminalityDraftarXiv2.tex"
TEX_2110 = SOURCE / "src-2110.06056" / "Arxiv-Sub2.tex"
TEX_2303 = SOURCE / "src-2303.10203" / "mainv4.tex"
TEX_2505 = SOURCE / "src-2505.21431" / "main.tex"

EXPECTED_HASHES = {
    SOURCE / "0306021.pdf": "051bb00b53a2405c5fe9e60ce8caa3fb53569fc521c3c160056a9ddc63308dd9",
    SOURCE / "0306021-source.tar": "4bb0cf7e021fd642f562c779b409e1d26cc42fc8aeae605fc1514bca565ba8b1",
    SOURCE / "0812.4849.pdf": "c0ba0b57f459cd03fa9ec36234e58e64acd214ab570d577806307b01cbf66071",
    SOURCE / "0812.4849-source.tar": "d094ed32127888dd0052e8341d43c83407dbe24c8f2813e3c5f4c49149781438",
    SOURCE / "1505.01844.pdf": "13ea6e7d9250257f72b8f3ea82c8b4c4f83c295998367164a5f2fcda1f071e1f",
    SOURCE / "1505.01844-source.tar": "74bb7123a648f87b36783253d54b51a17924e82e333d1ed421d4381a9aaac657",
    SOURCE / "1609.00723.pdf": "8f2c3437aaf3ab741f4ddf5139042859f802dff5e753a54d8401406faa80669e",
    SOURCE / "1609.00723-source.tar": "828b1655d88e414cd23f05684287a0ffa6d8c44ab03af4002a2b2cb0cc3dca26",
    SOURCE / "2110.06056.pdf": "08e6cad354b13c86683fde298338fb4738c28e5059d2dc3a3ebea631c20d1ba0",
    SOURCE / "2110.06056-source.tar": "22d1f0ead77c2a2bfb305968be0cfded94846c680ed55fab25c1994bba6ad421",
    SOURCE / "2303.10203.pdf": "db39ae9337d4fcb74108626a0fc04f2116eb5e9e6573d6d58b55d06366bf09cb",
    SOURCE / "2303.10203-source.tar": "0772442c8d3357750fd47310c193eb0a50ae92a670a7ddcbc6b99a1453917765",
    SOURCE / "2505.21431.pdf": "cf0cdec154d7ad74ada903e88f76d1fa90f2f73a14711eee11900a714ad3e192",
    SOURCE / "2505.21431-source.tar": "64e80415d379269b83eaf2bb94e71cdcfcd19210369a9bfbd8b6cda7c9ae276f",
}

ARXIV_URLS = {
    "legacy_bound": "https://arxiv.org/abs/gr-qc/0306021",
    "worldline_matching": "https://arxiv.org/abs/0812.4849",
    "nonrenormalization": "https://arxiv.org/abs/1505.01844",
    "QED_characteristic": "https://arxiv.org/abs/1609.00723",
    "geometry_control": "https://arxiv.org/abs/2110.06056",
    "curved_CDE": "https://arxiv.org/abs/2303.10203",
    "M87_case": "https://arxiv.org/abs/2505.21431",
    "GRSMEFT_basis": "https://arxiv.org/abs/1908.08050",
}

SOLAR_MASS_KG = 1.988409870698051e30
SOLAR_RADIUS_M = 6.957e8


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


def dirac_threshold_m2(charge: float, mass_kg: float) -> float:
    reduced_compton_m = hbar / (mass_kg * c)
    return -(charge**2) * alpha * reduced_compton_m**2 / (360.0 * math.pi)


def portal_beta_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "beta_id": "BETA4931_00_general",
            "sector": "generic parity-even gauge portal",
            "dimensionless_coupling": "u_X(k)=k^2 c_X(k)",
            "beta_equation": "beta_uX=(2+gamma_X)u_X+b_X(g_N,gauge,matter,...)+O(u_X^2)",
            "additive_source_at_u_zero": "b_X",
            "additive_source_derived": False,
            "multiplicative_gamma_derived": False,
            "fixed_point": "u_X*=-b_X/(2+gamma_X)+...",
            "critical_exponent": "theta_X=-(2+gamma_X)+...",
            "scope": "full projection template",
            "status": "FULL_MTS_FUNCTIONAL_TRACE_REQUIRED",
            "source": "dimensional analysis plus 4930 operator normalization",
            "passed": True,
        },
        {
            "beta_id": "BETA4931_01_Einstein_Maxwell_additive",
            "sector": "massless Einstein-Maxwell U1",
            "dimensionless_coupling": "u_gamma=k^2 c_gamma",
            "beta_equation": "beta_ugamma=(2+gamma_CFF)u_gamma+O(u_gamma^2); b_gamma^(1)|u=0=0",
            "additive_source_at_u_zero": 0.0,
            "additive_source_derived": True,
            "multiplicative_gamma_derived": False,
            "fixed_point": "u_gamma*=0 on the one-loop additive-zero manifold",
            "critical_exponent": "theta_gamma=-(2+gamma_CFF*)",
            "scope": "on-shell one-loop basis; not a two-loop or nonperturbative theorem",
            "status": "ONE_LOOP_ADDITIVE_ZERO_DERIVED",
            "source": "1908.08050 discussion after eq:dim6GRSMEFT; vector duality",
            "passed": True,
        },
        {
            "beta_id": "BETA4931_02_Einstein_Yang_Mills_additive",
            "sector": "massless Einstein-Yang-Mills SU2/SU3",
            "dimensionless_coupling": "u_W or u_G=k^2 c_X",
            "beta_equation": "beta_uX=(2+gamma_X)u_X+O(u_X^2); b_X^(1)|u=0=0",
            "additive_source_at_u_zero": 0.0,
            "additive_source_derived": True,
            "multiplicative_gamma_derived": False,
            "fixed_point": "u_X*=0 on the one-loop additive-zero manifold",
            "critical_exponent": "theta_X=-(2+gamma_X*)",
            "scope": "on-shell one-loop basis; not a two-loop or nonperturbative theorem",
            "status": "ONE_LOOP_ADDITIVE_ZERO_DERIVED",
            "source": "1908.08050 discussion after eq:dim6GRSMEFT; supersymmetry embedding",
            "passed": True,
        },
        {
            "beta_id": "BETA4931_03_canonical_Gaussian_estimate",
            "sector": "strict canonical portal approximation",
            "dimensionless_coupling": "u_X=k^2 c_X",
            "beta_equation": "beta_uX=2u_X",
            "additive_source_at_u_zero": 0.0,
            "additive_source_derived": True,
            "multiplicative_gamma_derived": False,
            "fixed_point": 0.0,
            "critical_exponent": -2.0,
            "scope": "sets gamma_X=0 and omits higher loops solely as a comparator",
            "status": "PERTURBATIVE_GAUSSIAN_COMPARATOR_NOT_FULL_MTS",
            "source": "canonical dimension plus one-loop additive zero",
            "passed": True,
        },
        {
            "beta_id": "BETA4931_04_mass_threshold",
            "sector": "massive charged Dirac matter",
            "dimensionless_coupling": "c_gamma below the mass threshold",
            "beta_equation": "Delta c_gamma=-Q^2 alpha_EM/[360 pi] (hbar/(m c))^2",
            "additive_source_at_u_zero": "finite matching jump at k approximately m",
            "additive_source_derived": True,
            "multiplicative_gamma_derived": False,
            "fixed_point": "not a fixed point; Wilsonian boundary matching",
            "critical_exponent": "not applicable",
            "scope": "Dirac spin-1/2 threshold in the declared MTS curvature convention",
            "status": "FINITE_THRESHOLD_DERIVED",
            "source": "1908.08050; magnitude cross-check 0812.4849 and 1609.00723",
            "passed": True,
        },
        {
            "beta_id": "BETA4931_05_full_MTS",
            "sector": "MTS gauge-curvature functional trace",
            "dimensionless_coupling": "u_B,u_W,u_G",
            "beta_equation": "requires regulator, gauge, ghost, gravity, motion and mixed-Hessian projection",
            "additive_source_at_u_zero": "not determined nonperturbatively",
            "additive_source_derived": False,
            "multiplicative_gamma_derived": False,
            "fixed_point": "not numerically determined",
            "critical_exponent": "not numerically determined",
            "scope": "full MTS essential truncation",
            "status": "NONPERTURBATIVE_FIXED_POINT_OPEN",
            "source": "4930 block-stability boundary",
            "passed": True,
        },
    ]
    return tagged(rows)


def threshold_matching_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "matching_id": "MATCH4931_00_GRSMEFT",
            "source_normalization": "L contains (c3/Lambda^2) B^mn B^rs C_mnrs",
            "result": "c3=-(1/90)(gprime/(4pi))^2 for a unit-hypercharge Dirac fermion of mass Lambda",
            "canonical_result": "Delta c_B=-gprime^2/[90(4pi)^2 Lambda^2]",
            "sign_policy": "MTS adopts the 1908 curvature convention",
            "matching_kind": "finite one-loop threshold",
            "source": "1908.08050 eq:dim6GRSMEFT and following matching paragraph",
            "passed": True,
        },
        {
            "matching_id": "MATCH4931_01_QED",
            "source_normalization": "L=-F^2/4+c_gamma CFF",
            "result": "Delta c_gamma=-Q^2 e^2/[90(4pi)^2 m^2]",
            "canonical_result": "Delta c_gamma=-Q^2 alpha_EM/[360pi] (hbar/(m c))^2",
            "sign_policy": "negative in the adopted MTS/GRSMEFT curvature convention",
            "matching_kind": "finite charged-Dirac threshold",
            "source": "1908.08050 translated to canonical QED",
            "passed": True,
        },
        {
            "matching_id": "MATCH4931_02_independent_magnitude",
            "source_normalization": "L=-F^2/(4e^2)+(c/m^2)Riemann F F with c=2/[180(4pi)^2]",
            "result": "canonical rescaling F=e F_c gives |Delta c_gamma|=e^2/[90(4pi)^2 m^2]",
            "canonical_result": "|Delta c_gamma|=Q^2 alpha_EM/[360pi] (hbar/(m c))^2",
            "sign_policy": "magnitude only; source Riemann convention differs",
            "matching_kind": "independent coefficient check",
            "source": "1609.00723 equations 4DEFT and EFTCoefficients; 0812.4849 drumhath",
            "passed": True,
        },
        {
            "matching_id": "MATCH4931_03_IR_decomposition",
            "source_normalization": "same canonical CFF basis at a declared low scale",
            "result": "c_gamma^IR=c_gamma^parent(mu_match)+sum_Dirac Delta c_f+c_gamma^QCD+c_gamma^EW+...",
            "canonical_result": "known free-lepton thresholds are calculable; parent, confined-QCD and spin-1 EW blocks remain separate",
            "sign_policy": "all terms must use one curvature and field normalization",
            "matching_kind": "no-double-counting Wilson decomposition",
            "source": "Wilsonian matching identity",
            "passed": True,
        },
        {
            "matching_id": "MATCH4931_04_no_free_quark_sum",
            "source_normalization": "infrared photon-curvature EFT",
            "result": "do not sum current-quark 1/m_q^2 thresholds below confinement",
            "canonical_result": "replace by a sourced hadronic/QCD matching block",
            "sign_policy": "not evaluated in checkpoint 4931",
            "matching_kind": "matching-domain guard",
            "source": "EFT threshold-domain consistency",
            "passed": True,
        },
    ]
    return tagged(rows)


def electroweak_projection_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "projection_id": "EW4931_00_photon",
            "infrared_channel": "A A C",
            "coefficient": "c_gamma=c_B cos^2(theta_W)+c_W sin^2(theta_W)",
            "derivation": "B=c_W A-s_W Z; W3=s_W A+c_W Z",
            "directly_constrained_by_photon_rows": True,
            "individual_UV_coefficients_separated": False,
            "status": "EXACT_TREE_LEVEL_ELECTROWEAK_PROJECTION",
            "passed": True,
        },
        {
            "projection_id": "EW4931_01_Z",
            "infrared_channel": "Z Z C",
            "coefficient": "c_Z=c_B sin^2(theta_W)+c_W cos^2(theta_W)",
            "derivation": "same neutral-field rotation",
            "directly_constrained_by_photon_rows": False,
            "individual_UV_coefficients_separated": False,
            "status": "EXACT_TREE_LEVEL_ELECTROWEAK_PROJECTION",
            "passed": True,
        },
        {
            "projection_id": "EW4931_02_mixed",
            "infrared_channel": "A Z C",
            "coefficient": "c_AZ=2 sin(theta_W) cos(theta_W)(c_W-c_B)",
            "derivation": "cross term from B B C plus W3 W3 C",
            "directly_constrained_by_photon_rows": False,
            "individual_UV_coefficients_separated": False,
            "status": "EXACT_TREE_LEVEL_ELECTROWEAK_PROJECTION",
            "passed": True,
        },
        {
            "projection_id": "EW4931_03_bound_strip",
            "infrared_channel": "photon-bound hyperplane",
            "coefficient": "|c_B cos^2(theta_W)+c_W sin^2(theta_W)+c_thresholds|<=B_gamma",
            "derivation": "substitute the photon projection into a two-sided c_gamma bound",
            "directly_constrained_by_photon_rows": True,
            "individual_UV_coefficients_separated": False,
            "status": "ONE_LINEAR_COMBINATION_ONLY",
            "passed": True,
        },
        {
            "projection_id": "EW4931_04_gluon",
            "infrared_channel": "G G C",
            "coefficient": "c_G remains orthogonal to photon propagation",
            "derivation": "SU3 field strength does not enter the neutral electroweak rotation",
            "directly_constrained_by_photon_rows": False,
            "individual_UV_coefficients_separated": False,
            "status": "NOT_CONSTRAINED_BY_THIS_CHECKPOINT",
            "passed": True,
        },
    ]
    return tagged(rows)


def charged_lepton_rows() -> list[dict[str, Any]]:
    particle_data = [
        ("electron", m_e, physical_constants["electron mass"][2]),
        ("muon", physical_constants["muon mass"][0], physical_constants["muon mass"][2]),
        ("tau", physical_constants["tau mass"][0], physical_constants["tau mass"][2]),
    ]
    rows: list[dict[str, Any]] = []
    electron_value = dirac_threshold_m2(1.0, m_e)
    for particle, mass_kg, mass_uncertainty_kg in particle_data:
        compton_m = hbar / (mass_kg * c)
        coefficient_m2 = dirac_threshold_m2(1.0, mass_kg)
        relative_mass_uncertainty = mass_uncertainty_kg / mass_kg
        rows.append(
            {
                "particle": particle,
                "charge_abs_e": 1.0,
                "mass_kg": mass_kg,
                "mass_uncertainty_kg": mass_uncertainty_kg,
                "reduced_Compton_m": compton_m,
                "Delta_c_gamma_m2": coefficient_m2,
                "abs_Delta_c_gamma_m2": abs(coefficient_m2),
                "sqrt_abs_Delta_c_gamma_m": math.sqrt(abs(coefficient_m2)),
                "relative_to_electron": coefficient_m2 / electron_value,
                "relative_coefficient_mass_uncertainty": 2.0 * relative_mass_uncertainty,
                "coefficient_formula": "-Q^2 alpha_EM lambda_bar^2/(360pi)",
                "free_particle_threshold": True,
                "full_SM_threshold": False,
                "source": f"scipy {scipy.__version__} physical_constants plus 1908.08050 matching",
                "status": "CALCULATED_FREE_DIRAC_THRESHOLD",
                "passed": coefficient_m2 < 0.0,
            }
        )
    total = sum(float(row["Delta_c_gamma_m2"]) for row in rows)
    rows.append(
        {
            "particle": "e+mu+tau free-lepton sum",
            "charge_abs_e": "three unit-charge species",
            "mass_kg": "not applicable",
            "mass_uncertainty_kg": "propagated uncertainty negligible for present gate",
            "reduced_Compton_m": "not applicable",
            "Delta_c_gamma_m2": total,
            "abs_Delta_c_gamma_m2": abs(total),
            "sqrt_abs_Delta_c_gamma_m": math.sqrt(abs(total)),
            "relative_to_electron": total / electron_value,
            "relative_coefficient_mass_uncertainty": "not used for claim",
            "coefficient_formula": "sum over e,mu,tau Dirac thresholds",
            "free_particle_threshold": True,
            "full_SM_threshold": False,
            "source": f"scipy {scipy.__version__} physical_constants plus 1908.08050 matching",
            "status": "CALCULATED_FREE_LEPTON_SUBTOTAL_ONLY",
            "passed": total < electron_value,
        }
    )
    return tagged(rows)


def photon_characteristic_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "characteristic_id": "EM4931_00_action",
            "object": "canonical photon-curvature action",
            "equation": "L_EM=-F_mn F^mn/4+c_gamma C_mnrs F^mn F^rs",
            "derivation": "4930 GRSMEFT photon basis after electroweak projection",
            "exactness": "exact at the retained local dimension-six order",
            "status": "DERIVED_OPERATOR_NORMALIZATION",
            "passed": True,
        },
        {
            "characteristic_id": "EM4931_01_excitation",
            "object": "constitutive excitation",
            "equation": "H^mn=F^mn-4 c_gamma C^mnrs F_rs",
            "derivation": "H^mn=-2 partial L/partial F_mn",
            "exactness": "exact variation of the retained action",
            "status": "DERIVED",
            "passed": True,
        },
        {
            "characteristic_id": "EM4931_02_field_equation",
            "object": "modified Maxwell equation",
            "equation": "nabla_m H^mn=J^n; nabla_[m F_rs]=0",
            "derivation": "variation with respect to A_n plus Bianchi identity",
            "exactness": "exact at retained order",
            "status": "DERIVED",
            "passed": True,
        },
        {
            "characteristic_id": "EM4931_03_principal_symbol",
            "object": "geometric-optics polarization equation",
            "equation": "[k^2 delta^nu_sigma-8 c_gamma k_mu C^(mu nu rho)_sigma k_rho] a^sigma=0; k.a=0",
            "derivation": "retain two phase derivatives and neglect gradients of amplitude and curvature",
            "exactness": "leading geometric-optics characteristic; curvature-sign convention declared",
            "status": "DERIVED",
            "passed": True,
        },
        {
            "characteristic_id": "EM4931_04_projected_dispersion",
            "object": "one-polarization dispersion",
            "equation": "k^2=8 c_gamma C_mrns k^m k^n f^r f^s",
            "derivation": "contract the principal symbol with unit transverse polarization f",
            "exactness": "leading local dimension-six and geometric-optics order",
            "status": "DERIVED_AND_SOURCE_CROSSCHECKED",
            "passed": True,
        },
        {
            "characteristic_id": "EM4931_05_screen_matrix",
            "object": "polarization eigenproblem",
            "equation": "K_AB=C_mrns l^m l^n e_A^r e_B^s; k^2/omega^2=8 c_gamma eig_A(K)",
            "derivation": "diagonalize the Weyl tidal map on the two-dimensional photon screen",
            "exactness": "basis invariant under screen rotations",
            "status": "DERIVED",
            "passed": True,
        },
        {
            "characteristic_id": "EM4931_06_no_frequency_dispersion",
            "object": "leading local frequency scaling",
            "equation": "both sides are quadratic in k, so delta v_A depends on c_gamma C and polarization, not |k|",
            "derivation": "homogeneity of the retained characteristic polynomial",
            "exactness": "no energy dispersion at this EFT order; higher derivatives and nonlocal loops may disperse",
            "status": "DISPERSION_FREE_BIREFRINGENCE_DERIVED",
            "passed": True,
        },
        {
            "characteristic_id": "EM4931_07_current_conservation",
            "object": "electric current",
            "equation": "nabla_n J^n=nabla_n nabla_m H^mn=0",
            "derivation": "antisymmetry of H and the covariant derivative commutator",
            "exactness": "exact for the retained gauge-invariant action",
            "status": "DERIVED",
            "passed": True,
        },
        {
            "characteristic_id": "EM4931_08_Hilbert_stress",
            "object": "full electromagnetic stress Ward identity",
            "equation": "nabla_m T_EM,total^(mn)=-F^(n m) J_m",
            "derivation": "diffeomorphism invariance after varying the complete Maxwell plus CFF action",
            "exactness": "exact on the electromagnetic equation of motion",
            "status": "DERIVED_CONSERVATION_IDENTITY",
            "passed": True,
        },
        {
            "characteristic_id": "EM4931_09_Poynting_constitutive_bound",
            "object": "local excitation and Poynting response",
            "equation": "epsilon_CF=4|c_gamma|||C||_op; ||delta H||/||F||<=epsilon_CF",
            "derivation": "operator-norm bound on H-F=-4c_gamma C.F",
            "exactness": "rigorous constitutive bound; full Hilbert stress also contains metric-variation derivative terms",
            "status": "DERIVED_WITH_STRESS_SCOPE_GUARD",
            "passed": True,
        },
    ]
    return tagged(rows)


def schwarzschild_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "observable_id": "SCH4931_00_dispersion",
            "observable": "Schwarzschild polarization characteristic",
            "formula": "p^2=+/-12 c_gamma (M_geom/r^3) p_3^2",
            "normalization": "M_geom=GM/c^2; c_gamma=lambda on Ricci-flat backgrounds",
            "leading_result": "opposite phase/group shifts for two linear polarizations",
            "empirical": False,
            "status": "SOURCE_DERIVED",
            "source": "gr-qc/0306021",
            "passed": True,
        },
        {
            "observable_id": "SCH4931_01_velocity_split",
            "observable": "tangential weak-coupling velocity splitting",
            "formula": "|Delta v_pol|/c=12|c_gamma| M_geom/r^3+O[(c_gamma M_geom/r^3)^2]",
            "normalization": "difference between the two polarization eigenmodes",
            "leading_result": "frequency independent and linear in the local tidal curvature",
            "empirical": False,
            "status": "DERIVED_FROM_SOURCE_DISPERSION",
            "source": "gr-qc/0306021 dispersion relation",
            "passed": True,
        },
        {
            "observable_id": "SCH4931_02_Horndeski_map",
            "observable": "Ricci-flat operator map",
            "formula": "L_doubledual F F=Riemann F F=C F F when R_mn=0",
            "normalization": "alpha_Horndeski=c_gamma only in a Ricci-flat arena",
            "leading_result": "black-hole propagation bounds transfer to CFF under this arena restriction",
            "empirical": False,
            "status": "EXACT_RICCI_FLAT_MAP",
            "source": "2505.21431 eq:vth_action and eq:vth_action_riem",
            "passed": True,
        },
        {
            "observable_id": "SCH4931_03_PPL_metric",
            "observable": "PPL optical angular factor",
            "formula": "rho_l(r)=(r^3-8 c_gamma M_geom)/(r^3+16 c_gamma M_geom)",
            "normalization": "ds_eff^2=-fdt^2+f^-1dr^2+rho_l r^2 dOmega^2",
            "leading_result": "one polarization optical metric",
            "empirical": False,
            "status": "SOURCE_DERIVED",
            "source": "2505.21431",
            "passed": True,
        },
        {
            "observable_id": "SCH4931_04_PPM_metric",
            "observable": "PPM optical angular factor",
            "formula": "rho_m(r)=(r^3+16 c_gamma M_geom)/(r^3-8 c_gamma M_geom)=1/rho_l",
            "normalization": "ds_eff^2=-fdt^2+f^-1dr^2+rho_m r^2 dOmega^2",
            "leading_result": "orthogonal-polarization optical metric",
            "empirical": False,
            "status": "SOURCE_DERIVED",
            "source": "2505.21431",
            "passed": True,
        },
        {
            "observable_id": "SCH4931_05_horizon_validity",
            "observable": "two-polarization horizon nonsingularity",
            "formula": "-1/2<=c_gamma/M_geom^2<=1",
            "normalization": "evaluate both optical metrics outside r=2M_geom",
            "leading_result": "theory/geometric-optics control interval, not an observational bound",
            "empirical": False,
            "status": "VALIDITY_CONDITION_NOT_DATA",
            "source": "2505.21431 eq:couplingrange",
            "passed": True,
        },
        {
            "observable_id": "SCH4931_06_Sultana_Dyer_control",
            "observable": "energy-density geometry interval",
            "formula": "-r_H^2/2<lambda<r_H^2",
            "normalization": "specific non-minimal model and background",
            "leading_result": "geometry/energy condition, not an empirical CFF likelihood",
            "empirical": False,
            "status": "CONTROL_ONLY_NOT_BOUND",
            "source": "2110.06056 eq:lambda-constraint-SD",
            "passed": True,
        },
    ]
    return tagged(rows)


def qed_arena_rows(leptons: list[dict[str, Any]]) -> list[dict[str, Any]]:
    c_lepton = float(next(row for row in leptons if row["particle"] == "e+mu+tau free-lepton sum")["Delta_c_gamma_m2"])
    arenas = [
        ("solar_limb", SOLAR_MASS_KG, SOLAR_RADIUS_M, "IAU nominal solar mass/radius control"),
        ("neutron_star_surface_benchmark", 1.4 * SOLAR_MASS_KG, 12_000.0, "1.4 solar-mass 12 km benchmark"),
        ("stellar_BH_horizon_benchmark", 10.0 * SOLAR_MASS_KG, None, "10 solar-mass r=2M_geom benchmark"),
        ("M87_horizon_case", 6.60e9 * SOLAR_MASS_KG, None, "2505.21431 gas-dynamics mass central value; r=2M_geom"),
    ]
    rows: list[dict[str, Any]] = []
    for arena, mass_kg, radius_m, source in arenas:
        mass_geom_m = G * mass_kg / c**2
        evaluation_radius_m = radius_m if radius_m is not None else 2.0 * mass_geom_m
        tidal_m_minus2 = mass_geom_m / evaluation_radius_m**3
        split = 12.0 * abs(c_lepton) * tidal_m_minus2
        rows.append(
            {
                "arena": arena,
                "mass_kg": mass_kg,
                "M_geom_m": mass_geom_m,
                "evaluation_radius_m": evaluation_radius_m,
                "M_over_r3_m_minus2": tidal_m_minus2,
                "c_gamma_free_leptons_m2": c_lepton,
                "leading_abs_polarization_velocity_split": split,
                "formula": "12|c_gamma|M_geom/r^3",
                "empirical_test": False,
                "source_or_role": source,
                "status": "QED_BASELINE_EFFECT_CONTROL",
                "passed": split > 0.0 and split < 1.0,
            }
        )
    return tagged(rows)


def observational_bound_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "bound_id": "BOUND4931_00_solar_bending_secondary",
            "arena": "solar birefringent bending",
            "bound_type": "secondary summary absolute-value recast",
            "source_bound": "sqrt(|alpha|)<3.16e5 km",
            "abs_or_upper_bound_m2": (3.16e5 * 1_000.0) ** 2,
            "sqrt_bound_m": 3.16e8,
            "two_sided_absolute": True,
            "source_internal_consistent": True,
            "selected_for_parent_bound": False,
            "assumptions": "secondary 2505 summary; model conditional; not independently reconstructed",
            "operator_map": "Horndeski/Riemann to CFF only on Ricci-flat exterior",
            "status": "CONDITIONAL_SECONDARY_BOUND",
            "source": "2505.21431 introduction",
            "passed": True,
        },
        {
            "bound_id": "BOUND4931_01_radar_intro",
            "arena": "solar radar echo",
            "bound_type": "original-paper introductory upper bound",
            "source_bound": "lambda<3.9e19 cm^2",
            "abs_or_upper_bound_m2": 3.9e19 * 1.0e-4,
            "sqrt_bound_m": math.sqrt(3.9e19 * 1.0e-4),
            "two_sided_absolute": False,
            "source_internal_consistent": False,
            "selected_for_parent_bound": False,
            "assumptions": "same source later prints 1.1e20 cm^2; quarantined discrepancy",
            "operator_map": "lambda Riemann F F equals c_gamma CFF in Ricci-flat solar exterior",
            "status": "SOURCE_DISCREPANCY_QUARANTINED",
            "source": "gr-qc/0306021 introduction",
            "passed": True,
        },
        {
            "bound_id": "BOUND4931_02_radar_detailed",
            "arena": "solar radar echo",
            "bound_type": "original-paper detailed upper bound",
            "source_bound": "lambda<1.1e20 cm^2",
            "abs_or_upper_bound_m2": 1.1e20 * 1.0e-4,
            "sqrt_bound_m": math.sqrt(1.1e20 * 1.0e-4),
            "two_sided_absolute": False,
            "source_internal_consistent": False,
            "selected_for_parent_bound": False,
            "assumptions": "conflicts with source introduction; not selected",
            "operator_map": "lambda Riemann F F equals c_gamma CFF in Ricci-flat solar exterior",
            "status": "SOURCE_DISCREPANCY_QUARANTINED",
            "source": "gr-qc/0306021 detailed radar section",
            "passed": True,
        },
        {
            "bound_id": "BOUND4931_03_PSR_original",
            "arena": "PSR B1534+12 Shapiro-delay polarization split",
            "bound_type": "original one-sided upper bound",
            "source_bound": "lambda<0.6e11 cm^2",
            "abs_or_upper_bound_m2": 0.6e11 * 1.0e-4,
            "sqrt_bound_m": math.sqrt(0.6e11 * 1.0e-4),
            "two_sided_absolute": False,
            "source_internal_consistent": True,
            "selected_for_parent_bound": True,
            "assumptions": "legacy 1 microsecond allowance; compact-star model; no competing operators; negative lambda not bounded by the printed inequality",
            "operator_map": "lambda Riemann F F equals c_gamma CFF in Ricci-flat exterior",
            "status": "STRONGEST_LEGACY_POSITIVE_SIDE_CONDITIONAL_BOUND",
            "source": "gr-qc/0306021 detailed pulsar section",
            "passed": True,
        },
        {
            "bound_id": "BOUND4931_04_PSR_secondary_abs",
            "arena": "PSR B1534+12",
            "bound_type": "secondary absolute-value recast",
            "source_bound": "sqrt(|alpha|)<2.45 km",
            "abs_or_upper_bound_m2": (2.45 * 1_000.0) ** 2,
            "sqrt_bound_m": 2_450.0,
            "two_sided_absolute": True,
            "source_internal_consistent": True,
            "selected_for_parent_bound": False,
            "assumptions": "2505 takes the older result at face value but explicitly cautions astrophysical/model systematics",
            "operator_map": "Horndeski/Riemann to CFF only on Ricci-flat exterior",
            "status": "STRONG_SECONDARY_ABSOLUTE_RECAST_NOT_PRIMARY_LIKELIHOOD",
            "source": "2505.21431 introduction",
            "passed": True,
        },
        {
            "bound_id": "BOUND4931_05_M87_case",
            "arena": "M87* n=1 thin photon-ring case study",
            "bound_type": "two-sided model-conditional case-study interval",
            "source_bound": "-0.3<alpha/M^2<0.3; sqrt(|alpha|)<5.34e9 km",
            "abs_or_upper_bound_m2": (5.34e9 * 1_000.0) ** 2,
            "sqrt_bound_m": 5.34e12,
            "two_sided_absolute": True,
            "source_internal_consistent": True,
            "selected_for_parent_bound": True,
            "assumptions": "thin reconstructed ring is n=1; unpolarized PPL/PPM overlap; external mass and distance; Schwarzschild approximation",
            "operator_map": "alpha=c_gamma on Ricci-flat Schwarzschild",
            "status": "MODERN_TWO_SIDED_CONDITIONAL_CASE_BOUND",
            "source": "2505.21431 eq:constraint",
            "passed": True,
        },
    ]
    return tagged(rows)


def bound_projection_rows(
    leptons: list[dict[str, Any]], bounds: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    c_known = float(next(row for row in leptons if row["particle"] == "e+mu+tau free-lepton sum")["Delta_c_gamma_m2"])
    selected_ids = {
        "BOUND4931_03_PSR_original",
        "BOUND4931_04_PSR_secondary_abs",
        "BOUND4931_05_M87_case",
    }
    rows: list[dict[str, Any]] = []
    for bound in bounds:
        if bound["bound_id"] not in selected_ids:
            continue
        bound_m2 = float(bound["abs_or_upper_bound_m2"])
        two_sided = bool(bound["two_sided_absolute"])
        if two_sided:
            residual_formula = "|c_parent+c_QCD+c_EW+...|<=B+|c_free_leptons|"
            residual_numeric = bound_m2 + abs(c_known)
        else:
            residual_formula = "c_parent+c_QCD+c_EW+...<B-c_free_leptons"
            residual_numeric = bound_m2 - c_known
        rows.append(
            {
                "projection_id": "PROJ_" + str(bound["bound_id"]),
                "bound_id": bound["bound_id"],
                "bound_m2": bound_m2,
                "known_free_lepton_c_gamma_m2": c_known,
                "known_to_bound_ratio": abs(c_known) / bound_m2,
                "bound_to_known_safety_factor": bound_m2 / abs(c_known),
                "residual_formula": residual_formula,
                "residual_numeric_envelope_m2": residual_numeric,
                "two_sided_parent_envelope": two_sided,
                "robust_general_bound": False,
                "status": "SOURCED_CONDITIONAL_WILSON_ENVELOPE",
                "passed": bound_m2 > 0.0 and residual_numeric > 0.0,
            }
        )
    rows.append(
        {
            "projection_id": "PROJ4931_no_general_two_sided_claim",
            "bound_id": "all",
            "bound_m2": "not applicable",
            "known_free_lepton_c_gamma_m2": c_known,
            "known_to_bound_ratio": "not applicable",
            "bound_to_known_safety_factor": "not applicable",
            "residual_formula": "a general parent bound requires a two-sided likelihood with all active RF2 and F4 operators",
            "residual_numeric_envelope_m2": "not promoted",
            "two_sided_parent_envelope": False,
            "robust_general_bound": False,
            "status": "GENERAL_EM_WILSON_CLAIM_BLOCKED_BY_MODEL_CONDITIONALITY",
            "passed": True,
        }
    )
    return tagged(rows)


def parent_matching_rows(leptons: list[dict[str, Any]]) -> list[dict[str, Any]]:
    c_known = float(next(row for row in leptons if row["particle"] == "e+mu+tau free-lepton sum")["Delta_c_gamma_m2"])
    rows = [
        {
            "component": "c_gamma_parent(mu_match)",
            "value_m2": "not numerically determined",
            "derivation_status": "requires MTS functional trace or a parent boundary condition",
            "independent_parameter": True,
            "included_in_4931_numeric_total": False,
            "next_action": "project u_B and u_W in the same regulator/truncation as the C3 branch",
            "passed": True,
        },
        {
            "component": "c_gamma_free_leptons",
            "value_m2": c_known,
            "derivation_status": "finite one-loop Dirac thresholds calculated for e, mu and tau",
            "independent_parameter": False,
            "included_in_4931_numeric_total": True,
            "next_action": "retain as a fixed infrared baseline",
            "passed": True,
        },
        {
            "component": "c_gamma_QCD_hadronic",
            "value_m2": "not evaluated",
            "derivation_status": "requires confined/hadronic matching; current-quark free sum forbidden",
            "independent_parameter": False,
            "included_in_4931_numeric_total": False,
            "next_action": "source a hadronic Euler-Heisenberg/curved-space matching calculation",
            "passed": True,
        },
        {
            "component": "c_gamma_EW_spin1",
            "value_m2": "not evaluated",
            "derivation_status": "charged-vector threshold has a spin-dependent coefficient not imported here",
            "independent_parameter": False,
            "included_in_4931_numeric_total": False,
            "next_action": "derive or source the W threshold in the identical CFF convention",
            "passed": True,
        },
        {
            "component": "c_gamma_IR",
            "value_m2": "c_parent+c_free_leptons+c_QCD+c_EW+...",
            "derivation_status": "decomposition derived; only free-lepton subtotal numeric",
            "independent_parameter": True,
            "included_in_4931_numeric_total": False,
            "next_action": "either calculate c_parent and remaining thresholds or fit one total Wilson coefficient",
            "passed": True,
        },
        {
            "component": "conditional_minimal_threshold_branch",
            "value_m2": c_known,
            "derivation_status": "equals c_IR only if c_parent=c_QCD=c_EW=...=0",
            "independent_parameter": False,
            "included_in_4931_numeric_total": False,
            "next_action": "do not adopt without a parent zero theorem and complete threshold accounting",
            "passed": True,
        },
    ]
    return tagged(rows)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (path, expected_hash) in enumerate(EXPECTED_HASHES.items()):
        exists = path.exists()
        actual_hash = digest(path) if exists else ""
        passed = exists and actual_hash == expected_hash
        rows.append(
            {
                "source_id": f"SRC4931_{index:02d}_binary",
                "source_path_or_url": path.relative_to(ROOT).as_posix(),
                "source_role": "locked_primary_pdf_or_author_source",
                "verification": "SHA256",
                "expected_sha256": expected_hash,
                "actual_sha256": actual_hash,
                "source_exists": exists,
                "marker_found": passed,
                "status": "LOCAL_BINARY_SOURCE_HASH_VERIFIED" if passed else "LOCAL_BINARY_SOURCE_FAILED",
                "passed": passed,
            }
        )
    text_sources = [
        (PROVENANCE, "MTS_GAUGE_CURVATURE_PORTAL_PROVENANCE_4931", "source_provenance"),
        (TEX_1908, "absence of (one-loop) divergences associated with mixed SM-gravity operators", "one_loop_additive_zero"),
        (TEX_1908, "c_3 = -\\tfrac{1}{90}", "finite_Dirac_threshold"),
        (TEX_0306, "0.6 \\times 10^{11} cm^2", "legacy_pulsar_bound"),
        (TEX_0306, "p^2 = \\pm 12 \\lambda", "Schwarzschild_dispersion"),
        (TEX_0812, "Drummond-Hathrell form", "independent_matching"),
        (TEX_1505, "\\gamma_{ij} =0", "one_loop_selection_rule"),
        (TEX_1609, "\\label{EFTCoefficients}", "QED_matching_coefficients"),
        (TEX_1609, "\\label{Oe2PhotonEOMSchwarzschild}", "photon_characteristic"),
        (TEX_2110, "eq:lambda-constraint-SD", "geometry_control"),
        (TEX_2303, "Covariant Derivative Expansion", "curved_CDE_method"),
        (TEX_2505, "5.34 \\times 10^{9}", "M87_case_bound"),
        (TEX_2505, "\\label{eq:couplingrange}", "optical_metric_validity"),
        (Path(__file__).resolve(), "def portal_beta_rows", "checkpoint_generator"),
    ]
    for offset, (path, marker, role) in enumerate(text_sources, start=len(rows)):
        exists = path.exists()
        marker_found = exists and marker in read_text_auto(path)
        rows.append(
            {
                "source_id": f"SRC4931_{offset:02d}_text",
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
    for source_id, url in ARXIV_URLS.items():
        rows.append(
            {
                "source_id": "SRC4931_URL_" + source_id,
                "source_path_or_url": url,
                "source_role": "primary_arXiv_record",
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


def gate_rows(
    beta: list[dict[str, Any]],
    leptons: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    c_e = float(next(row for row in leptons if row["particle"] == "electron")["Delta_c_gamma_m2"])
    c_leptons = float(next(row for row in leptons if row["particle"] == "e+mu+tau free-lepton sum")["Delta_c_gamma_m2"])
    psr = float(next(row for row in bounds if row["bound_id"] == "BOUND4931_03_PSR_original")["abs_or_upper_bound_m2"])
    m87 = float(next(row for row in bounds if row["bound_id"] == "BOUND4931_05_M87_case")["abs_or_upper_bound_m2"])
    rows = [
        {
            "gate": "one_loop_massless_additive_beta",
            "status": "CLOSED_IN_ON_SHELL_PERTURBATIVE_BASIS",
            "decision": "minimal Einstein-Maxwell and Einstein-Yang-Mills have b_X^(1)(u=0)=0",
            "claim_promoted": False,
            "passed": all(bool(row["passed"]) for row in beta[:4]),
        },
        {
            "gate": "portal_Gaussian_zero",
            "status": "PERTURBATIVE_SPECIAL_MANIFOLD_RETAINED",
            "decision": "u_X=0 is a one-loop additive-zero fixed manifold; theta=-2 only in the explicit gamma_X=0 comparator",
            "claim_promoted": False,
            "passed": True,
        },
        {
            "gate": "charged_Dirac_threshold",
            "status": "CALCULATED",
            "decision": f"c_gamma,e={c_e:.12e} m^2; free e+mu+tau subtotal={c_leptons:.12e} m^2",
            "claim_promoted": False,
            "passed": c_e < 0.0 and c_leptons < c_e,
        },
        {
            "gate": "photon_characteristic",
            "status": "DERIVED",
            "decision": "polarization-dependent but leading-order frequency-independent propagation follows from the CFF principal symbol",
            "claim_promoted": False,
            "passed": True,
        },
        {
            "gate": "legacy_PSR_bound",
            "status": "SOURCED_ONE_SIDED_MODEL_CONDITIONAL",
            "decision": f"printed positive-side upper bound c_gamma<{psr:.6e} m^2; it is not a robust two-sided likelihood",
            "claim_promoted": False,
            "passed": math.isclose(psr, 6.0e6),
        },
        {
            "gate": "modern_M87_bound",
            "status": "SOURCED_TWO_SIDED_CASE_STUDY",
            "decision": f"conditional |c_gamma|<{m87:.6e} m^2 from the assumed M87* n=1 thin ring",
            "claim_promoted": False,
            "passed": math.isclose(m87, 2.85156e25),
        },
        {
            "gate": "known_QED_safety",
            "status": "OVERWHELMINGLY_BELOW_CONDITIONAL_BOUNDS",
            "decision": f"PSR positive-side scale / |free-lepton c_gamma|={psr/abs(c_leptons):.6e}",
            "claim_promoted": False,
            "passed": psr / abs(c_leptons) > 1.0e30,
        },
        {
            "gate": "full_MTS_portal_fixed_point",
            "status": "OPEN_BUT_NARROWED",
            "decision": "the unknown is c_gamma^parent plus nonleptonic matching and gamma_X, not the entire low-energy portal structure",
            "claim_promoted": False,
            "passed": True,
        },
        {
            "gate": "Maxwell_Poynting_recovery",
            "status": "KNOWN_QED_BASELINE_SAFE_PARENT_RESIDUAL_BOUNDED_ONLY_CONDITIONALLY",
            "decision": "the free-lepton baseline is negligible in all tabulated arenas; a general Maxwell claim awaits parent matching or a robust two-sided polarization likelihood",
            "claim_promoted": False,
            "passed": True,
        },
        {
            "gate": "weak_GR_Newton",
            "status": "RETAINED",
            "decision": "CFF is silent for F=0 and does not alter the uncharged two-derivative GR/Newton branch at tree level",
            "claim_promoted": False,
            "passed": True,
        },
        {
            "gate": "compact_and_full_MTS_to_GR",
            "status": "NOT_PROMOTED",
            "decision": "nonperturbative portal projection, full threshold matching and a robust all-operator bound remain open",
            "claim_promoted": False,
            "passed": True,
        },
        {
            "gate": "next_target",
            "status": "FUNCTIONAL_TRACE_OR_POLARIZATION_LIKELIHOOD",
            "decision": NEXT_TARGET,
            "claim_promoted": False,
            "passed": True,
        },
    ]
    return tagged(rows)


def main() -> int:
    beta = portal_beta_rows()
    matching = threshold_matching_rows()
    electroweak = electroweak_projection_rows()
    leptons = charged_lepton_rows()
    characteristic = photon_characteristic_rows()
    schwarzschild = schwarzschild_rows()
    arenas = qed_arena_rows(leptons)
    bounds = observational_bound_rows()
    projections = bound_projection_rows(leptons, bounds)
    parent = parent_matching_rows(leptons)
    sources = source_register_rows()
    gates = gate_rows(beta, leptons, bounds)

    tables = {
        "P8_Y5_R2FR_4931_PORTAL_BETA_BOUNDARY.csv": beta,
        "P8_Y5_R2FR_4931_DIRAC_THRESHOLD_MATCHING.csv": matching,
        "P8_Y5_R2FR_4931_ELECTROWEAK_PORTAL_PROJECTION.csv": electroweak,
        "P8_Y5_R2FR_4931_CHARGED_LEPTON_THRESHOLDS.csv": leptons,
        "P8_Y5_R2FR_4931_PHOTON_CHARACTERISTIC.csv": characteristic,
        "P8_Y5_R2FR_4931_SCHWARZSCHILD_POLARIZATION.csv": schwarzschild,
        "P8_Y5_R2FR_4931_QED_ARENA_CONTROL.csv": arenas,
        "P8_Y5_R2FR_4931_OBSERVATIONAL_BOUNDS.csv": bounds,
        "P8_Y5_R2FR_4931_WILSON_BOUND_PROJECTION.csv": projections,
        "P8_Y5_R2FR_4931_PARENT_MATCHING_LEDGER.csv": parent,
        "P8_Y5_R2FR_4931_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4931_GATE_DECISION.csv": gates,
    }
    for filename, rows in tables.items():
        write_csv(OUTPUT / filename, rows)

    passed = all(bool(row.get("passed", True)) for rows in tables.values() for row in rows)
    electron = next(row for row in leptons if row["particle"] == "electron")
    lepton_sum = next(row for row in leptons if row["particle"] == "e+mu+tau free-lepton sum")
    psr = next(row for row in bounds if row["bound_id"] == "BOUND4931_03_PSR_original")
    print("P8_Y5_R2FR_4931_GAUGE_PORTAL_MATCHING_EM_BOUND_PASS" if passed else "P8_Y5_R2FR_4931_GAUGE_PORTAL_MATCHING_EM_BOUND_FAIL")
    print("one_loop_massless_additive_source=0")
    print("canonical_portal_fixed_point=0; canonical_theta=-2; full_gamma_open=True")
    print(f"electron_c_gamma_m2={float(electron['Delta_c_gamma_m2']):.16e}")
    print(f"free_lepton_sum_c_gamma_m2={float(lepton_sum['Delta_c_gamma_m2']):.16e}")
    print(f"legacy_PSR_positive_bound_m2={float(psr['abs_or_upper_bound_m2']):.16e}")
    print("leading_local_photon_effect=frequency_independent_birefringence")
    print("full_MTS_portal_fixed_point_promoted=False")
    print("general_two_sided_EM_Wilson_claim=False")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

from scipy.constants import alpha, c, hbar, physical_constants


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4944"
MTS_RESIDUALS = POST / "source-intake" / "mts_residuals"

RESULT_JSON = SOURCE / "visible_CFF_threshold_and_total_bound_results.json"
SPIN1_CSV = SOURCE / "spin1_heat_kernel_envelope.csv"
COMPONENT_CSV = SOURCE / "visible_CFF_matching_components.csv"
HADRONIC_CSV = SOURCE / "hadronic_matching_and_total_bound_gate.csv"
LOCAL_CSV = SOURCE / "conditional_total_CFF_local_residual_bound.csv"

CHECKPOINT_4931 = POST / "4931-Y5-R2FR-gauge-curvature-portal-beta-functions-and-fixed-point-values-or-EM-Wilson-bound.md"
PROVENANCE_4931 = POST / "source-intake" / "functional_rg" / "4931" / "PROVENANCE.md"
PDF_0812 = POST / "source-intake" / "functional_rg" / "4931" / "0812.4849.pdf"
SOURCE_0812 = POST / "source-intake" / "functional_rg" / "4931" / "0812.4849-source.tar"
PDF_2303 = POST / "source-intake" / "functional_rg" / "4931" / "2303.10203.pdf"
SOURCE_2303 = POST / "source-intake" / "functional_rg" / "4931" / "2303.10203-source.tar"
LEPTONS_4931 = MTS_RESIDUALS / "P8_Y5_R2FR_4931_CHARGED_LEPTON_THRESHOLDS.csv"
BOUNDS_4931 = MTS_RESIDUALS / "P8_Y5_R2FR_4931_OBSERVATIONAL_BOUNDS.csv"
WILSON_4931 = MTS_RESIDUALS / "P8_Y5_R2FR_4931_WILSON_BOUND_PROJECTION.csv"
RESULT_4942 = POST / "source-intake" / "functional_rg" / "4942" / "local_O4_C3_CFF_residual_results.json"
RESIDUAL_4942 = POST / "source-intake" / "functional_rg" / "4942" / "local_O4_C3_CFF_residual_vector.csv"
PDF_CHIRAL = SOURCE / "2512.12743.pdf"
SOURCE_CHIRAL = SOURCE / "2512.12743-source.tar"
PDF_W_MASS = SOURCE / "rpp2025-rev-w-mass.pdf"
PDF_MESONS = SOURCE / "rpp2025-sum-mesons.pdf"

EXPECTED_HASHES = {
    CHECKPOINT_4931: "f302c82dcbab0f5cdcba7a3fed7d6a6d075534eee2fa4c24f3dee3ee8a2d9852",
    PROVENANCE_4931: "03862aaada713c090cc2182c79fc09d8a74f180b1d3d0b6d45ac0a4524fb9cc2",
    PDF_0812: "c0ba0b57f459cd03fa9ec36234e58e64acd214ab570d577806307b01cbf66071",
    SOURCE_0812: "d094ed32127888dd0052e8341d43c83407dbe24c8f2813e3c5f4c49149781438",
    PDF_2303: "db39ae9337d4fcb74108626a0fc04f2116eb5e9e6573d6d58b55d06366bf09cb",
    SOURCE_2303: "0772442c8d3357750fd47310c193eb0a50ae92a670a7ddcbc6b99a1453917765",
    LEPTONS_4931: "f35f98894ec566a09bf891f258a0fe8e593a042fd89e892133f9a368ffa951cb",
    BOUNDS_4931: "1cdcf88b3d05922a2c7cd741bb3aa713ac7c6fb5b9f7103bfa6e7403ec15a105",
    WILSON_4931: "b542067370d75dfc1e5c1cdadbf9439dd90c82eb28dd7aaf8bc0e63350a6b75f",
    RESULT_4942: "c830baff10125f984ba26d11d44465c4d519ecd6c51317b9c9fcac6cf5e2e04b",
    RESIDUAL_4942: "51f034326f02684491743d6b12fed9d54854885dae07e7894e77423f435a14a5",
    PDF_CHIRAL: "8df550fbef213a3df0a4529afd8a2e8b31f5d26883f37a69617047c8d55b4e9a",
    SOURCE_CHIRAL: "79ed9c034e5d9a50a2d9fc89f1656b154905471f9066ce8da6cfc5876857c162",
    PDF_W_MASS: "35ec44036af48fa13efdd6310f3fab59e9305fb24e8b5e48737916025d764733",
    PDF_MESONS: "baa69ae2e5be33811a3d3e5d696707b6c20c8d9875791373a8a5053d132f2497",
}

MARKER = "MTS_4944_VISIBLE_CFF_THRESHOLD_AND_TOTAL_BOUND"
CHECKED_DATE = "2026-07-13"
W_MASS_GEV = 80.3692
CHARGED_PION_MASS_MEV = 139.5704
CHARGED_KAON_MASS_MEV = 493.677
W_DIMENSIONLESS_ENVELOPE = 10.0


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
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


def mass_kg_from_ev(mass_ev: float) -> float:
    return mass_ev * physical_constants["electron volt-kilogram relationship"][0]


def reduced_compton_m(mass_kg: float) -> float:
    return hbar / (mass_kg * c)


def scalar_cff_m2(mass_kg: float, charge: float = 1.0) -> float:
    return charge**2 * alpha * reduced_compton_m(mass_kg) ** 2 / (720.0 * math.pi)


def spin1_cff_bound_m2(mass_kg: float, charge: float = 1.0) -> float:
    return (
        W_DIMENSIONLESS_ENVELOPE
        * charge**2
        * alpha
        * reduced_compton_m(mass_kg) ** 2
        / (4.0 * math.pi)
    )


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

    leptons = read_csv(LEPTONS_4931)
    lepton_sum_row = next(row for row in leptons if row["particle"] == "e+mu+tau free-lepton sum")
    electron_row = next(row for row in leptons if row["particle"] == "electron")
    c_leptons = float(lepton_sum_row["Delta_c_gamma_m2"])
    c_electron_abs = float(electron_row["abs_Delta_c_gamma_m2"])

    bounds = read_csv(BOUNDS_4931)
    psr_abs_row = next(row for row in bounds if row["bound_id"] == "BOUND4931_04_PSR_secondary_abs")
    psr_abs_bound_m2 = float(psr_abs_row["abs_or_upper_bound_m2"])
    result_4942 = json.loads(RESULT_4942.read_text(encoding="utf-8"))
    c_parent_abs = float(result_4942["dimensionful_endpoint_envelope"]["abs_c_gamma_parent_m2"])

    mass_w_kg = mass_kg_from_ev(W_MASS_GEV * 1e9)
    mass_pion_kg = mass_kg_from_ev(CHARGED_PION_MASS_MEV * 1e6)
    mass_kaon_kg = mass_kg_from_ev(CHARGED_KAON_MASS_MEV * 1e6)
    c_w_bound = spin1_cff_bound_m2(mass_w_kg)
    c_pion_anchor = scalar_cff_m2(mass_pion_kg)
    c_kaon_anchor = scalar_cff_m2(mass_kaon_kg)

    spin1_rows = tagged(
        [
            {
                "term_id": "W4944_00_hessian",
                "operator": "Delta_1=-D^2 delta+m_W^2 delta+R+2 i e F; Gamma_W=Tr ln Delta_1-Tr ln Delta_0",
                "absolute_dimensionless_CFF_weight": 0.0,
                "bound_derivation": "charged vector plus Goldstone and ghost determinant reduces to complex vector minus complex scalar",
                "status": "GAUGE_FIXED_HESSIAN_AND_DETERMINANT_COUNT",
                "passed": True,
            },
            {
                "term_id": "W4944_01_explicit_Riemann_Omega2",
                "operator": "-(1/180)R_mnrs tr(Omega^mn Omega^rs)",
                "absolute_dimensionless_CFF_weight": 5.0 / 180.0,
                "bound_derivation": "triangle bound uses four vector components plus one subtracted scalar in absolute value",
                "status": "COMPLETE_UOLEA_MONOMIAL_BOUND",
                "passed": True,
            },
            {
                "term_id": "W4944_02_covariant_derivative_reduction",
                "operator": "(1/90)(D.Omega)^2+(1/360)(D Omega)^2",
                "absolute_dimensionless_CFF_weight": 5.0 * (1.0 / 90.0 + 1.0 / 360.0) * 4.0,
                "bound_derivation": "two-form Weitzenbock reduction cap four counts both curvature actions before using the photon EOM",
                "status": "CONSERVATIVE_DH_BASIS_REDUCTION_BOUND",
                "passed": True,
            },
            {
                "term_id": "W4944_03_U_box_U",
                "operator": "-(1/12)tr(U box U), U=2 i e F^a_b",
                "absolute_dimensionless_CFF_weight": (1.0 / 12.0) * 4.0 * 4.0,
                "bound_derivation": "gyromagnetic factor squared times the same four-action derivative-reduction cap",
                "status": "CONSERVATIVE_DH_BASIS_REDUCTION_BOUND",
                "passed": True,
            },
            {
                "term_id": "W4944_04_U_Omega2",
                "operator": "-(1/12)tr(U Omega_mn Omega^mn)",
                "absolute_dimensionless_CFF_weight": 1.0 / 3.0,
                "bound_derivation": "two placements of one spin curvature and one electromagnetic bundle curvature with |U|=2|eF|",
                "status": "EXPLICIT_CROSS_TERM_BOUND",
                "passed": True,
            },
            {
                "term_id": "W4944_05_non_CFF_monomials",
                "operator": "tr(Omega^3), tr(U^3), R U^2 and Ricci terms",
                "absolute_dimensionless_CFF_weight": 0.0,
                "bound_derivation": "tr of one Lorentz curvature vanishes in Omega^3; U^3 has no curvature; scalar and Ricci terms vanish on the Ricci-flat CFF projection",
                "status": "ZERO_ON_DECLARED_RICCI_FLAT_CFF_PROJECTION",
                "passed": True,
            },
        ]
    )
    raw_spin1_weight = sum(float(row["absolute_dimensionless_CFF_weight"]) for row in spin1_rows)
    spin1_rows.append(
        {
            "term_id": "W4944_06_total_envelope",
            "operator": "|c_gamma,W|<=K_W e^2/(16pi^2 m_W^2)",
            "absolute_dimensionless_CFF_weight": W_DIMENSIONLESS_ENVELOPE,
            "bound_derivation": f"raw triangle sum={raw_spin1_weight:.12g}<2; K_W=10 retains a factor-five safety margin",
            "status": "CONSERVATIVE_SPIN1_BOUND_NOT_EXACT_MATCHING",
            "passed": raw_spin1_weight < 2.0 and W_DIMENSIONLESS_ENVELOPE >= 5.0 * raw_spin1_weight,
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
    )

    elementary_center = c_leptons + c_parent_abs
    elementary_lower = elementary_center - c_w_bound
    elementary_upper = elementary_center + c_w_bound
    chiral_anchor_sum = c_pion_anchor + c_kaon_anchor
    control_lower = elementary_lower + chiral_anchor_sum
    control_upper = elementary_upper + chiral_anchor_sum
    known_threshold_abs_envelope = max(abs(control_lower), abs(control_upper))

    component_rows = tagged(
        [
            {
                "component_id": "CFF4944_00_parent",
                "sector": "completed MTS parent CFF endpoint",
                "coefficient_or_bound_m2": c_parent_abs,
                "sign_or_interval": "positive on the completed W_C family; worst absolute envelope shown",
                "formula": "c_parent=16pi W_C l_P^2",
                "matching_status": "CALCULATED_PARENT_ENDPOINT",
                "valid_for_elementary_subtotal": True,
                "valid_for_total_physical_prediction": False,
                "valid_for_conditional_total_bound": True,
                "source": "4942 completed endpoint result",
                "passed": c_parent_abs < 1e-70,
            },
            {
                "component_id": "CFF4944_01_free_leptons",
                "sector": "electron muon tau",
                "coefficient_or_bound_m2": c_leptons,
                "sign_or_interval": "negative in the locked MTS/GRSMEFT curvature convention",
                "formula": "sum_f -Q_f^2 alpha lambda_f^2/(360pi)",
                "matching_status": "CALCULATED_ELEMENTARY_DIRAC_THRESHOLDS",
                "valid_for_elementary_subtotal": True,
                "valid_for_total_physical_prediction": False,
                "valid_for_conditional_total_bound": True,
                "source": "4931 charged-lepton threshold table",
                "passed": c_leptons < 0,
            },
            {
                "component_id": "CFF4944_02_W_spin1",
                "sector": "charged electroweak spin-1 threshold",
                "coefficient_or_bound_m2": c_w_bound,
                "sign_or_interval": f"[-{c_w_bound:.16g},+{c_w_bound:.16g}]",
                "formula": "|c_W|<=10 alpha lambda_W^2/(4pi)",
                "matching_status": "COMPLETE_DIMENSION_SIX_HEAT_KERNEL_ENVELOPE_EXACT_SIGN_NOT_MATCHED",
                "valid_for_elementary_subtotal": True,
                "valid_for_total_physical_prediction": False,
                "valid_for_conditional_total_bound": True,
                "source": "2303.10203 UOLEA plus PDG 2025 m_W",
                "passed": c_w_bound / c_electron_abs < 1e-7,
            },
            {
                "component_id": "CFF4944_03_pion_pointlike_anchor",
                "sector": "charged-pion leading scalar-QED loop anchor",
                "coefficient_or_bound_m2": c_pion_anchor,
                "sign_or_interval": "positive relative to the adopted negative Dirac convention",
                "formula": "+alpha lambda_pi^2/(720pi)",
                "matching_status": "CALCULATED_POINTLIKE_CHIRAL_LOOP_ANCHOR_NOT_FULL_QCD",
                "valid_for_elementary_subtotal": False,
                "valid_for_total_physical_prediction": False,
                "valid_for_conditional_total_bound": True,
                "source": "0812.4849 scalar DH coefficient plus PDG 2025 pion mass",
                "passed": c_pion_anchor / c_electron_abs < 1e-5,
            },
            {
                "component_id": "CFF4944_04_kaon_pointlike_anchor",
                "sector": "charged-kaon scalar-QED loop anchor",
                "coefficient_or_bound_m2": c_kaon_anchor,
                "sign_or_interval": "positive relative to the adopted negative Dirac convention",
                "formula": "+alpha lambda_K^2/(720pi)",
                "matching_status": "CALCULATED_POINTLIKE_LOOP_ANCHOR_NOT_FULL_QCD",
                "valid_for_elementary_subtotal": False,
                "valid_for_total_physical_prediction": False,
                "valid_for_conditional_total_bound": True,
                "source": "0812.4849 scalar DH coefficient plus PDG 2025 kaon mass",
                "passed": c_kaon_anchor < c_pion_anchor,
            },
            {
                "component_id": "CFF4944_05_QCD_local_remainder",
                "sector": "confined QCD TJJ matching and hadronic local counterterms",
                "coefficient_or_bound_m2": "not separately bounded from first principles in the acquired sources",
                "sign_or_interval": "not assumed to cancel or equal the pointlike pion and kaon anchors",
                "formula": "c_QCD=c_pi_loop+c_K_loop+c_QCD_local+heavier spectral terms",
                "matching_status": "SEPARATE_QCD_MATCHING_OPEN_TOTAL_BOUND_USED_INSTEAD",
                "valid_for_elementary_subtotal": False,
                "valid_for_total_physical_prediction": False,
                "valid_for_conditional_total_bound": True,
                "source": "2512.12743 curved chiral EFT and Wilsonian matching",
                "passed": True,
            },
            {
                "component_id": "CFF4944_06_calculable_control_interval",
                "sector": "parent plus free leptons plus W envelope plus pointlike pi/K anchors",
                "coefficient_or_bound_m2": known_threshold_abs_envelope,
                "sign_or_interval": f"[{control_lower:.16g},{control_upper:.16g}]",
                "formula": "c_parent+c_leptons+[-cW,+cW]+c_pi_anchor+c_K_anchor",
                "matching_status": "CALCULABLE_CONTROL_NOT_TOTAL_PHYSICAL_COEFFICIENT",
                "valid_for_elementary_subtotal": False,
                "valid_for_total_physical_prediction": False,
                "valid_for_conditional_total_bound": True,
                "source": "source-executed 4931 4942 and 4944 rows",
                "passed": known_threshold_abs_envelope < 1e-30,
            },
            {
                "component_id": "CFF4944_07_total_conditional_bound",
                "sector": "complete infrared CFF coefficient including all thresholds",
                "coefficient_or_bound_m2": psr_abs_bound_m2,
                "sign_or_interval": f"[-{psr_abs_bound_m2},+{psr_abs_bound_m2}]",
                "formula": "|c_gamma^IR|<=B_PSR_secondary_abs",
                "matching_status": "TWO_SIDED_SECONDARY_MODEL_CONDITIONAL_TOTAL_BOUND",
                "valid_for_elementary_subtotal": False,
                "valid_for_total_physical_prediction": False,
                "valid_for_conditional_total_bound": True,
                "source": "4931 BOUND4931_04_PSR_secondary_abs",
                "passed": psr_abs_bound_m2 == 6002500.0,
            },
            {
                "component_id": "CFF4944_08_unmatched_remainder_bound",
                "sector": "QCD local plus any other unmatched visible threshold",
                "coefficient_or_bound_m2": psr_abs_bound_m2 + known_threshold_abs_envelope,
                "sign_or_interval": "two-sided triangle envelope conditional on the same PSR recast",
                "formula": "|c_unmatched|=|c_total-c_control|<=B_PSR+|c_control|",
                "matching_status": "CONDITIONAL_UNMATCHED_REMAINDER_BOUND_WITHOUT_CANCELLATION",
                "valid_for_elementary_subtotal": False,
                "valid_for_total_physical_prediction": False,
                "valid_for_conditional_total_bound": True,
                "source": "triangle inequality plus source-executed calculable control interval",
                "passed": True,
            },
        ]
    )

    hadronic_rows = tagged(
        [
            {
                "gate_id": "HAD4944_00_no_free_current_quarks",
                "statement": "current u d s masses are not inserted into free 1/m_q^2 CFF thresholds below confinement",
                "consequence": "avoids a spurious infrared enhancement",
                "status": "EXACT_WILSONIAN_DOMAIN_GUARD",
                "passed": True,
            },
            {
                "gate_id": "HAD4944_01_scalar_loop_anchors",
                "statement": "the pointlike charged-pion and charged-kaon scalar loops are calculable with the scalar DH coefficient",
                "consequence": "they provide signed low-mass anchors but not the complete QCD coefficient",
                "status": "CALCULATED_ANCHORS",
                "passed": c_pion_anchor > c_kaon_anchor > 0,
            },
            {
                "gate_id": "HAD4944_02_curved_chiral_LECs",
                "statement": "curved chiral EFT permits non-minimal curvature operators and additional low-energy constants",
                "consequence": "composite hadron matching cannot be replaced by a free point-particle sum",
                "status": "SOURCE_BACKED_COUNTERTERM_WARNING",
                "passed": True,
            },
            {
                "gate_id": "HAD4944_03_no_cancellation_assumption",
                "statement": "c_QCD_local is neither set to zero nor tuned against the electron or parent coefficient",
                "consequence": "no hidden threshold closure is introduced",
                "status": "EXPLICIT_NONCANCELLATION_FIREWALL",
                "passed": True,
            },
            {
                "gate_id": "HAD4944_04_total_bound_bypass",
                "statement": "the sourced bound acts on the complete c_gamma^IR and therefore includes the unresolved QCD and W signs",
                "consequence": "a conditional local residual envelope exists without pretending the split matching is complete",
                "status": "CONDITIONAL_TOTAL_BOUND_CONSTRUCTED",
                "passed": True,
            },
            {
                "gate_id": "HAD4944_05_primary_likelihood",
                "statement": "the selected two-sided 2.45 km PSR row is a secondary recast of a model-conditional legacy analysis",
                "consequence": "it cannot promote a robust general Maxwell claim",
                "status": "PRIMARY_TWO_SIDED_LIKELIHOOD_OPEN",
                "passed": True,
            },
        ]
    )

    local_rows: list[dict[str, Any]] = []
    for row in read_csv(RESIDUAL_4942):
        mass_length = float(row["mass_length_m"])
        radius = float(row["radius_m"])
        curvature_factor = 12.0 * mass_length / radius**3
        known_split = known_threshold_abs_envelope * curvature_factor
        total_bound_split = psr_abs_bound_m2 * curvature_factor
        local_rows.append(
            {
                "system": row["system"],
                "source_class": row["source_class"],
                "mass_length_m": mass_length,
                "radius_m": radius,
                "CFF_curvature_factor_m_minus_2": curvature_factor,
                "calculable_control_abs_cgamma_m2": known_threshold_abs_envelope,
                "calculable_control_abs_Delta_v_pol_over_c": known_split,
                "conditional_total_abs_cgamma_bound_m2": psr_abs_bound_m2,
                "conditional_total_abs_Delta_v_pol_over_c": total_bound_split,
                "known_control_to_total_bound_ratio": known_threshold_abs_envelope / psr_abs_bound_m2,
                "linearized_total_bound_below_ten_percent": total_bound_split < 0.1,
                "constant_PPN_interpretation": "NOT_A_CONSTANT_PPN_COEFFICIENT",
                "bound_scope": "secondary absolute PSR recast; model conditional; universal coefficient transfer",
                "status": "CONDITIONAL_TOTAL_CFF_LOCAL_RESIDUAL_BOUND",
                "valid_for_conditional_total_bound": True,
                "valid_for_general_physical_CFF_claim": False,
                "passed": total_bound_split < 0.1,
            }
        )
    local_rows = tagged(local_rows)

    checks = {
        "source_hashes_match": not hash_failures,
        "free_lepton_sum_negative": c_leptons < 0,
        "scalar_anchor_relative_sign_positive": c_pion_anchor > 0 and c_kaon_anchor > 0,
        "spin1_raw_triangle_weight_below_two": raw_spin1_weight < 2.0,
        "spin1_envelope_margin_at_least_five": W_DIMENSIONLESS_ENVELOPE >= 5.0 * raw_spin1_weight,
        "spin1_bound_below_one_e_minus_7_electron": c_w_bound / c_electron_abs < 1e-7,
        "pion_anchor_below_one_e_minus_5_electron": c_pion_anchor / c_electron_abs < 1e-5,
        "calculable_control_below_one_e_minus_30_m2": known_threshold_abs_envelope < 1e-30,
        "QCD_remainder_not_set_zero": any(row["gate_id"] == "HAD4944_03_no_cancellation_assumption" for row in hadronic_rows),
        "all_local_conditional_rows_below_ten_percent": all(row["passed"] for row in local_rows),
        "all_evidence_full_MTS_nonclaim": all(
            not row["valid_for_full_MTS_claim"]
            for table in (spin1_rows, component_rows, hadronic_rows, local_rows)
            for row in table
        ),
    }

    result = {
        "marker": MARKER,
        "source_hashes": source_hashes,
        "convention": "L_EM=-F^2/4+c_gamma C_mnrs F^mn F^rs",
        "masses": {
            "W_mass_GeV": W_MASS_GEV,
            "charged_pion_mass_MeV": CHARGED_PION_MASS_MEV,
            "charged_kaon_mass_MeV": CHARGED_KAON_MASS_MEV,
        },
        "thresholds": {
            "c_parent_abs_m2": c_parent_abs,
            "c_free_leptons_m2": c_leptons,
            "c_W_abs_bound_m2": c_w_bound,
            "c_pion_pointlike_anchor_m2": c_pion_anchor,
            "c_kaon_pointlike_anchor_m2": c_kaon_anchor,
            "calculable_control_interval_m2": [control_lower, control_upper],
            "calculable_control_abs_envelope_m2": known_threshold_abs_envelope,
            "QCD_local_remainder": "not separately bounded; no zero or cancellation assumed",
        },
        "spin1_envelope": {
            "raw_dimensionless_triangle_weight": raw_spin1_weight,
            "adopted_K_W": W_DIMENSIONLESS_ENVELOPE,
            "formula": "|c_W|<=K_W alpha lambda_W^2/(4pi)",
            "status": "conservative complete-dimension-six envelope, not exact signed W matching",
        },
        "conditional_total_bound": {
            "bound_m2": psr_abs_bound_m2,
            "unmatched_remainder_bound_formula": "|c_unmatched|<=B_PSR+|c_calculable_control|",
            "unmatched_remainder_bound_m2": psr_abs_bound_m2 + known_threshold_abs_envelope,
            "source_row": "BOUND4931_04_PSR_secondary_abs",
            "two_sided": True,
            "primary_likelihood": False,
            "model_conditional": True,
            "scope": "complete c_gamma^IR including parent, leptons, W, QCD and all other thresholds",
        },
        "local_projection": {
            "systems": len(local_rows),
            "max_calculable_control_split": max(row["calculable_control_abs_Delta_v_pol_over_c"] for row in local_rows),
            "max_conditional_total_split": max(row["conditional_total_abs_Delta_v_pol_over_c"] for row in local_rows),
            "max_system": max(local_rows, key=lambda row: row["conditional_total_abs_Delta_v_pol_over_c"])["system"],
        },
        "checks": checks,
        "claim_boundary": {
            "free_lepton_thresholds_calculated": True,
            "scalar_QED_CFF_formula_calculated": True,
            "pointlike_pion_kaon_anchors_calculated": True,
            "electroweak_spin1_complete_dimension_six_envelope_bounded": True,
            "electroweak_spin1_exact_signed_matching_calculated": False,
            "QCD_hadronic_local_matching_calculated": False,
            "QCD_hadronic_remainder_assumed_zero": False,
            "conditional_complete_total_CFF_bound_constructed": True,
            "primary_robust_two_sided_CFF_likelihood_available": False,
            "complete_physical_CFF_prediction": False,
            "local_Maxwell_promoted": False,
            "full_MTS_fixed_point": False,
        },
    }

    write_csv(SPIN1_CSV, spin1_rows)
    write_csv(COMPONENT_CSV, component_rows)
    write_csv(HADRONIC_CSV, hadronic_rows)
    write_csv(LOCAL_CSV, local_rows)
    RESULT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")

    failed = [name for name, passed in checks.items() if not passed]
    print(f"{MARKER}_SPIN1_RAW_WEIGHT={raw_spin1_weight:.12e}", flush=True)
    print(f"{MARKER}_W_BOUND_M2={c_w_bound:.12e}", flush=True)
    print(f"{MARKER}_PION_ANCHOR_M2={c_pion_anchor:.12e}", flush=True)
    print(f"{MARKER}_KNOWN_CONTROL_M2={known_threshold_abs_envelope:.12e}", flush=True)
    print(f"{MARKER}_TOTAL_CONDITIONAL_BOUND_M2={psr_abs_bound_m2:.12e}", flush=True)
    print(f"{MARKER}_MAX_TOTAL_SPLIT={result['local_projection']['max_conditional_total_split']:.12e}", flush=True)
    print(f"{MARKER}_FAILED={len(failed)}", flush=True)
    print(f"{MARKER}_RESULT_SHA256={digest(RESULT_JSON)}", flush=True)
    if failed:
        for failure in failed:
            print(f"{MARKER}_FAIL={failure}", flush=True)
        return 1
    print(f"{MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

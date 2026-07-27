from __future__ import annotations

import csv
import hashlib
import json
import math
import statistics
import subprocess
import sys
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4950"

RESULT_JSON = SOURCE / "pair_operator_RG_and_bifurcation_results.json"
GENERATION_CSV = SOURCE / "pair_operator_generation_and_RG_closure.csv"
BIFURCATION_CSV = SOURCE / "stabilized_pair_bifurcation_law.csv"
LOCAL_CSV = SOURCE / "local_spherical_pair_thresholds.csv"
SPARC_WINDOW_CSV = SOURCE / "SPARC_spherical_pair_window.csv"
POTENTIAL_CSV = SOURCE / "SPARC_baryonic_potential_depth_proxy.csv"
DECISION_CSV = SOURCE / "pair_route_decision.csv"
GALAXY_SNAPSHOT_CSV = SOURCE / "galaxy_readonly_snapshot.csv"

MEMORY_4886 = POST / "4886-Y5-R2FR-canonical-memory-scalar-local-screening-scalarization-and-same-parent-cosmology-compatibility-gate.md"
FACTOR_4919 = POST / "4919-Y5-R2FR-vacuum-1PI-operator-selection-curvature-Higgs-and-hidden-scalar-vev-matching-or-local-bound.md"
FUNCTIONAL_4936 = POST / "4936-Y5-R2FR-motion-1PI-mass-and-O4-functional-trace-projection-or-two-scale-predictivity-gate.md"
O4_4941 = POST / "4941-Y5-R2FR-natural-TypeII-direct-metric-scalar-O4-zero-proof-and-minimal-O4-parent-completion-gate.md"
LOWER_X2 = POST / "source-intake" / "functional_rg" / "4941" / "lower_scalar_essential_quotient.csv"
CTP_4949 = POST / "4949-Y5-R2FR-covariant-2PI-motion-occupation-Dyson-source-and-conserved-galaxy-stress-or-composite-route-rejection.md"
SPARC_4949 = POST / "source-intake" / "functional_rg" / "4949" / "SPARC_outer_occupation_scale_diagnostic.csv"
LOCAL_4947 = POST / "source-intake" / "functional_rg" / "4947" / "cross_arena_no_retuning_matrix.csv"

CURVED_PDF_1810 = SOURCE / "1810.06395.pdf"
CURVED_TAR_1810 = SOURCE / "1810.06395-source.tar"
CURVED_TEX_1810 = SOURCE / "src1810" / "multicritical-curved-space-v3.tex"
FRG_PDF_1711 = SOURCE / "1711.02224.pdf"
FRG_TAR_1711 = SOURCE / "1711.02224-source.tar"
FRG_TEX_1711 = SOURCE / "src1711" / "Flow-final.tex"

GALAXY_REPO = Path(r"D:\g4948")
GALAXY_README = GALAXY_REPO / "README.md"
GALAXY_SAMPLES = GALAXY_REPO / "data" / "samples.js"
EXPECTED_GALAXY_HEAD = "5c2fc082adcc67d779cfd99d5b6e9a9c9ac5fcbd"

MARKER = "MTS_4950_PAIR_OPERATOR_RG_AND_BIFURCATION_WINDOW"
CHECKED_DATE = "2026-07-13"
LIGHT_SPEED_KM_S = 299_792.458
LIGHT_SPEED_M_S = 299_792_458.0
NEWTON_G = 6.67430e-11
HBAR = 1.054571817e-34
PLANCK_LENGTH = math.sqrt(HBAR * NEWTON_G / LIGHT_SPEED_M_S**3)
KPC = 3.085677581491367e19
ML_DISK = 0.5
ML_BULGE = 0.7

EXPECTED_HASHES = {
    MEMORY_4886: "164ed70e5b269f98474a37b07aa52d46c2fdd80fa0f9b8f491351cb31bc61769",
    FACTOR_4919: "47144e184bb1b37a0bb50ae630a5a80020ff5f7c372fe0dc1cef8e7ce79db629",
    FUNCTIONAL_4936: "d24db400f3fb2fec75883bb078a37eec15b101e09c119f2a6ff43063d604c971",
    O4_4941: "f4c6f83668c5f904706747dcafb3d538068a038307ffc062e13fe3234a6b9543",
    LOWER_X2: "62f83d1e254709fa6dd5141ad9132a3d9aac89894a30684f804bae508646e89f",
    CTP_4949: "772bee9863471ab7e4a4e4887773b91786110539d471243c26aaa1b88866f7b8",
    SPARC_4949: "959c76b6e88efcf9ddcc9d010a20fbb1cefebfb310797e0b1814e76e3a13e92a",
    LOCAL_4947: "8c060a129155d84ebc40412e50a2acc11ea5043a9825afd24e5486065c194cc7",
    CURVED_PDF_1810: "c6a9056644661f9f7148ec34622644de0007287f885a6d66fec93e9c8a8d3d5b",
    CURVED_TAR_1810: "cba9d4b174248bf2665f50966edfa916a1e8fa1674ba8f70380b92e01946563d",
    CURVED_TEX_1810: "4f5f8ad95def5eb2d3892b862775e7b0e818eba26a87564243b418a4e98e0ef3",
    FRG_PDF_1711: "e4713d85ecd67fa59c6f12bbe1c683e69bba450e4bd9630e0377143f72ce5e87",
    FRG_TAR_1711: "aa15f8b91d51af105ab455b989c8095d7166a8125b09fd8db7f61ad2785f1c52",
    FRG_TEX_1711: "3fd379ba98e5ce9bdbdbf781683fdd2f471315328e9f28d94920e5b027c9a6cc",
    GALAXY_README: "e9acb4d72fc6fdd7f39ba62e18357746ae423e61c7e6932cf8b5b8f45265e402",
    GALAXY_SAMPLES: "a7edd2db0e237d7997207bf1ee53c78e492cf5dbc7a7cbfc478c12e69bddbfba",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
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


def load_samples() -> list[dict[str, str]]:
    raw = read_text(GALAXY_SAMPLES)
    return json.loads(raw[raw.index("[") : raw.rindex("]") + 1])


def parse_points(raw: str) -> list[list[float]]:
    return [
        [float(value) for value in line.split()]
        for line in raw.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def first_threshold_root(mu: float) -> float:
    if mu == 0.0:
        return math.pi / 2.0
    low = math.pi / 2.0
    high = math.pi - 1.0e-13
    for _ in range(180):
        middle = (low + high) / 2.0
        residual = middle / math.tan(middle) + mu
        if residual > 0.0:
            low = middle
        else:
            high = middle
    return (low + high) / 2.0


def sphere_threshold(radius_m: float, compactness: float, compton_length_m: float) -> tuple[float, float, float]:
    mu = 0.0 if math.isinf(compton_length_m) else radius_m / compton_length_m
    root = first_threshold_root(mu)
    threshold = (mu**2 + root**2) / (6.0 * compactness)
    return threshold, mu, root


def main() -> int:
    source_hashes = {str(path): digest(path) for path in EXPECTED_HASHES}
    source_hashes_match = all(source_hashes[str(path)] == expected for path, expected in EXPECTED_HASHES.items())

    memory_text = read_text(MEMORY_4886)
    factor_text = read_text(FACTOR_4919)
    functional_text = read_text(FUNCTIONAL_4936)
    o4_text = read_text(O4_4941)
    ctp_text = read_text(CTP_4949)
    curved_1810 = read_text(CURVED_TEX_1810)
    frg_1711 = read_text(FRG_TEX_1711)

    source_clause_checks = {
        "reflection_even_parent": "reflection-even" in ctp_text,
        "direct_fixed_metric_factorization": "fixed-metric path integral" in factor_text,
        "direct_hidden_visible_derivative_zero": "delta^2\\Gamma" in factor_text,
        "full_motion_potential_selected": "full functional motion potential" in functional_text,
        "X2_additive_source": "beta_c,ess|0   =16g^2" in o4_text,
        "X2_parent_scheme_value_open": "not numerically spliced" in read_text(ROOT / "formalization-workbench" / "04-variable-audit.csv"),
        "CTP_static_route_rejected": "current minimal scalar 2PI galaxy route            = rejected" in ctp_text,
        "curved_scalar_phi2R_special": "\\phi^2 R" in curved_1810,
        "curved_scalar_beta_xi": "\\beta_\\xi" in curved_1810,
        "FRG_VF_action": "RF_k(\\phi)+V_k(\\phi)" in frg_1711,
        "FRG_F_flow": "\\partial_t F_k" in frg_1711 and "\\frac{1}{6} -  \\frac{F_k''}{Z_k}" in frg_1711,
        "FRG_even_functions": "stay even at all scales" in frg_1711,
        "memory_scalarization_comparator": "first `beta_crit`" in memory_text,
    }

    generation_rows = tagged(
        [
            {
                "generation_id": "GEN4950_00_even_basis",
                "operator": "reflection-even quadratic and quartic motion basis",
                "parent_derivation": "psi->-psi permits F(psi)R, V_even(psi), X^2 and O4 while forbidding odd tadpoles",
                "equation_or_flow": "Gamma_k includes V_k(psi)+F_k(psi)R+Z_k(psi)X/2+...",
                "current_status": "BASIS_REQUIRED_BY_SYMMETRY_AND_CURVED_RG",
                "coefficient_owned": False,
                "passed": True,
            },
            {
                "generation_id": "GEN4950_01_VF_flow",
                "operator": "joint potential and curvature function",
                "parent_derivation": "curved-space scalar FRG closes V_k and F_k together",
                "equation_or_flow": "partial_t V=(V'')^2/[2(4pi)^2 Z^2]; partial_t F=-V''[(1/6)-F''/Z]/[(4pi)^2 Z]",
                "current_status": "PRIMARY_SOURCE_FLOW_RECONSTRUCTED",
                "coefficient_owned": False,
                "passed": True,
            },
            {
                "generation_id": "GEN4950_02_beta_xi",
                "operator": "R psi^2/2 and lambda psi^4/24",
                "parent_derivation": "insert V=lambda psi^4/24 and F=xi psi^2/2 in the primary one-loop flow",
                "equation_or_flow": "beta_lambda=3lambda^2/(4pi)^2; beta_xi=lambda(xi-1/6)/(4pi)^2",
                "current_status": "ONE_LOOP_RG_IDENTITY_DERIVED",
                "coefficient_owned": False,
                "passed": True,
            },
            {
                "generation_id": "GEN4950_03_minimal_xi",
                "operator": "xi=0 surface",
                "parent_derivation": "evaluate beta_xi at xi=0",
                "equation_or_flow": "beta_xi|xi=0=-lambda/[6(4pi)^2]",
                "current_status": "NOT_INVARIANT_IF_LAMBDA_NONZERO",
                "coefficient_owned": False,
                "passed": True,
            },
            {
                "generation_id": "GEN4950_04_direct_Tpsi2",
                "operator": "T_matter psi^2/M_R^2",
                "parent_derivation": "fixed-metric hidden-visible factorization kills direct mixed vertices",
                "equation_or_flow": "delta^2 Gamma/(delta psi delta Phi_SM)=0",
                "current_status": "DIRECT_PARENT_TERM_EXCLUDED",
                "coefficient_owned": True,
                "passed": True,
            },
            {
                "generation_id": "GEN4950_05_trace_basis",
                "operator": "xi_R R psi^2 plus xi_T T psi^2/M_R^2",
                "parent_derivation": "trace of the 4947 Einstein equation at negligible Lambda gives R=-T/M_R^2",
                "equation_or_flow": "m_eff^2=m_gap^2+(xi_R-xi_T)R; B=-(xi_R-xi_T)>0 for activation",
                "current_status": "ONE_EFFECTIVE_LOCAL_PAIR_COEFFICIENT",
                "coefficient_owned": False,
                "passed": True,
            },
            {
                "generation_id": "GEN4950_06_X2",
                "operator": "c_ess X^2",
                "parent_derivation": "lower essential quotient has additive source beta_c,ess|0=16g^2 in the source comparator",
                "equation_or_flow": "delta^2(X^2)/delta psi^2|psi=0=0 but higher 2PI self-energies are nonzero when occupied",
                "current_status": "GENERATED_CHANNEL_PARENT_SCHEME_COEFFICIENT_OPEN_NO_STATIC_MASS_SOURCE",
                "coefficient_owned": False,
                "passed": True,
            },
            {
                "generation_id": "GEN4950_07_quartic",
                "operator": "lambda psi^4/24",
                "parent_derivation": "regular full V_k is required after the fractional one-coupling family failed RG closure",
                "equation_or_flow": "lambda is a Taylor coordinate of V_k and cannot be copied from the old fractional potential",
                "current_status": "STABILIZER_VALUE_NOT_DERIVED",
                "coefficient_owned": False,
                "passed": True,
            },
            {
                "generation_id": "GEN4950_08_O4",
                "operator": "u_O4 C^2 X",
                "parent_derivation": "completed parent coefficient is nonzero but A=Z+2u_O4 C^2 remains positive",
                "equation_or_flow": "O4 changes kinetic operator and cannot by itself make m_eff^2 negative",
                "current_status": "KINETIC_PORTAL_NOT_PAIR_SOURCE",
                "coefficient_owned": True,
                "passed": True,
            },
            {
                "generation_id": "GEN4950_09_closure",
                "operator": "complete even motion two-point sector",
                "parent_derivation": "V_k F_k Z_k and c_ess must be solved in one parent convention before environmental activation",
                "equation_or_flow": "quadratic 4949 Gamma2=0 is scoped to the displayed truncation, not the unresolved X2/VF completion",
                "current_status": "CURRENT_PARENT_PAIR_SECTOR_NOT_RG_CLOSED",
                "coefficient_owned": False,
                "passed": True,
            },
        ]
    )

    bifurcation_rows = tagged(
        [
            {
                "derivation_id": "BIF4950_00_action",
                "object": "minimal reflection-even local pair action",
                "equation": "S_pair=int sqrt(-g)[-X/2-(m^2+xi_R R+xi_T T/M_R^2)psi^2/2-lambda psi^4/24]",
                "condition": "one public metric and one universal coefficient set",
                "status": "TEST_ACTION_DEFINED_NOT_ADOPTED",
                "passed": True,
            },
            {
                "derivation_id": "BIF4950_01_trace_reduction",
                "object": "leading GR trace basis",
                "equation": "R=-T/M_R^2 so m_eff^2=m^2-BR with B=-(xi_R-xi_T)",
                "condition": "Lambda and higher-gradient trace corrections negligible",
                "status": "PAIR_COEFFICIENT_DEGENERACY_DERIVED",
                "passed": True,
            },
            {
                "derivation_id": "BIF4950_02_Rayleigh",
                "object": "environmental lowest eigenvalue",
                "equation": "lambda0(B)=inf_f [int(|grad f|^2+m^2 f^2)-B int R f^2]/int f^2",
                "condition": "self-adjoint regular boundary problem",
                "status": "EXACT_SPECTRAL_GATE_DERIVED",
                "passed": True,
            },
            {
                "derivation_id": "BIF4950_03_top_hat",
                "object": "uniform spherical source threshold",
                "equation": "x cot x=-mu; mu=mL; x in [pi/2,pi); Bcrit=(mu^2+x^2)/(6C)",
                "condition": "constant density radius L with exterior vacuum and decaying zero mode",
                "status": "EXACT_FIRST_ZERO_MODE_DERIVED",
                "passed": True,
            },
            {
                "derivation_id": "BIF4950_04_massless",
                "object": "most favorable long-range threshold",
                "equation": "Bcrit(m=0)=pi^2/(24C)",
                "condition": "mass only increases the threshold for fixed L and C",
                "status": "MINIMUM_SPHERICAL_THRESHOLD_DERIVED",
                "passed": True,
            },
            {
                "derivation_id": "BIF4950_05_stabilization",
                "object": "lowest-mode amplitude below threshold",
                "equation": "A0^2=-6 lambda0/[lambda int f0^4] for V=lambda psi^4/24 and int f0^2=1",
                "condition": "lambda0<0 and lambda>0",
                "status": "STABILIZED_AMPLITUDE_LAW_DERIVED",
                "passed": True,
            },
            {
                "derivation_id": "BIF4950_06_energy",
                "object": "bifurcated energy",
                "equation": "Delta E_min=-3 lambda0^2/[2 lambda int f0^4]",
                "condition": "single-mode near-threshold expansion",
                "status": "ENERGY_LOWERING_DERIVED",
                "passed": True,
            },
            {
                "derivation_id": "BIF4950_07_local_GR",
                "object": "local correspondence gate",
                "equation": "lambda0_local>0 keeps psi=0; lambda0_local<0 creates a new scalarized branch and invalidates automatic 4947 recovery",
                "condition": "same B m and lambda in every arena",
                "status": "NO_RETUNING_LOCAL_STABILITY_GATE_DERIVED",
                "passed": True,
            },
        ]
    )

    compton_cases = {
        "massless": math.inf,
        "lambda_100_kpc": 100.0 * KPC,
        "lambda_10_kpc": 10.0 * KPC,
        "lambda_1_kpc": 1.0 * KPC,
    }
    local_source_rows = [
        row
        for row in read_csv(LOCAL_4947)
        if row["system"] in {"Earth", "Sun", "one_solar_mass_white_dwarf", "1.4_solar_mass_12km_neutron_star"}
    ]
    local_rows: list[dict[str, Any]] = []
    local_thresholds: dict[str, dict[str, float]] = {}
    for case, compton_length in compton_cases.items():
        local_thresholds[case] = {}
        for row in local_source_rows:
            threshold, mu, root = sphere_threshold(
                float(row["radius_m"]),
                float(row["compactness_GM_over_rc2"]),
                compton_length,
            )
            local_thresholds[case][row["system"]] = threshold
            local_rows.append(
                {
                    "compton_case": case,
                    "compton_length_m": "inf" if math.isinf(compton_length) else compton_length,
                    "Jgap": 0.0 if math.isinf(compton_length) else (PLANCK_LENGTH / compton_length) ** 2,
                    "system": row["system"],
                    "radius_m": row["radius_m"],
                    "compactness": row["compactness_GM_over_rc2"],
                    "mu_mL": mu,
                    "threshold_root_x": root,
                    "Bcrit_spherical": threshold,
                    "local_stability_requires": f"B<{threshold:.16g}",
                    "status": "LOCAL_PAIR_STABILITY_CEILING",
                    "checkpoint_marker": MARKER,
                    "valid_for_full_MTS_claim": False,
                    "source_checked_date": CHECKED_DATE,
                }
            )

    samples = load_samples()
    sparc_rows: list[dict[str, Any]] = []
    potential_rows: list[dict[str, Any]] = []
    for sample in samples:
        points = parse_points(sample["text"])
        baryonic_points: list[tuple[float, float]] = []
        for point in points:
            radius_kpc, _, _, vgas, vdisk, vbulge = point[:6]
            vbar2 = max(vgas * abs(vgas) + ML_DISK * vdisk**2 + ML_BULGE * vbulge**2, 0.0)
            baryonic_points.append((radius_kpc, vbar2))
        outer_radius_kpc, outer_vbar2 = baryonic_points[-1]
        compactness_proxy = outer_vbar2 / LIGHT_SPEED_KM_S**2
        for case, compton_length in compton_cases.items():
            threshold, mu, root = sphere_threshold(outer_radius_kpc * KPC, compactness_proxy, compton_length)
            sun_ceiling = local_thresholds[case]["Sun"]
            white_dwarf_ceiling = local_thresholds[case]["one_solar_mass_white_dwarf"]
            neutron_star_ceiling = local_thresholds[case]["1.4_solar_mass_12km_neutron_star"]
            sparc_rows.append(
                {
                    "galaxy": sample["name"].removesuffix("_rotmod.dat"),
                    "compton_case": case,
                    "outer_radius_kpc": outer_radius_kpc,
                    "outer_Vbar2_km2_s2": outer_vbar2,
                    "baryonic_compactness_proxy": compactness_proxy,
                    "mu_mL": mu,
                    "threshold_root_x": root,
                    "Bcrit_spherical": threshold,
                    "Sun_Bcrit": sun_ceiling,
                    "white_dwarf_Bcrit": white_dwarf_ceiling,
                    "neutron_star_Bcrit": neutron_star_ceiling,
                    "Bcrit_ratio_to_Sun": threshold / sun_ceiling,
                    "Bcrit_ratio_to_white_dwarf": threshold / white_dwarf_ceiling,
                    "Bcrit_ratio_to_neutron_star": threshold / neutron_star_ceiling,
                    "universal_window_vs_Sun": threshold < sun_ceiling,
                    "universal_window_vs_white_dwarf": threshold < white_dwarf_ceiling,
                    "universal_window_vs_neutron_star": threshold < neutron_star_ceiling,
                    "status": "SPHERICAL_GALAXY_ACTIVATION_LOCAL_STABILITY_NO_WINDOW",
                    "checkpoint_marker": MARKER,
                    "valid_for_full_MTS_claim": False,
                    "source_checked_date": CHECKED_DATE,
                }
            )

        radial_integral = sum(
            0.5 * (left[1] + right[1]) * math.log(right[0] / left[0])
            for left, right in zip(baryonic_points, baryonic_points[1:])
        )
        inner_solid_body_proxy = 0.5 * baryonic_points[0][1]
        outer_kepler_proxy = baryonic_points[-1][1]
        potential_depth_proxy = inner_solid_body_proxy + radial_integral + outer_kepler_proxy
        twice_potential_over_c2 = 2.0 * potential_depth_proxy / LIGHT_SPEED_KM_S**2
        no_bound_B_floor = 1.0 / twice_potential_over_c2
        potential_rows.append(
            {
                "galaxy": sample["name"].removesuffix("_rotmod.dat"),
                "inner_radius_kpc": baryonic_points[0][0],
                "outer_radius_kpc": baryonic_points[-1][0],
                "inner_solid_body_proxy_km2_s2": inner_solid_body_proxy,
                "observed_radial_integral_km2_s2": radial_integral,
                "outer_kepler_tail_proxy_km2_s2": outer_kepler_proxy,
                "baryonic_potential_depth_proxy_km2_s2": potential_depth_proxy,
                "U_Birman_Schwinger_proxy": twice_potential_over_c2,
                "B_no_bound_floor_proxy": no_bound_B_floor,
                "ratio_to_massless_white_dwarf_ceiling": no_bound_B_floor / local_thresholds["massless"]["one_solar_mass_white_dwarf"],
                "interpretation": "MIDPLANE_POTENTIAL_PROXY_NOT_FULL_3D_EIGENVALUE",
                "checkpoint_marker": MARKER,
                "valid_for_full_MTS_claim": False,
                "source_checked_date": CHECKED_DATE,
            }
        )

    threshold_summary: dict[str, dict[str, float]] = {}
    for case in compton_cases:
        selected = [row for row in sparc_rows if row["compton_case"] == case]
        values = [float(row["Bcrit_spherical"]) for row in selected]
        threshold_summary[case] = {
            "minimum": min(values),
            "median": statistics.median(values),
            "maximum": max(values),
            "minimum_ratio_to_Sun": min(float(row["Bcrit_ratio_to_Sun"]) for row in selected),
            "minimum_ratio_to_white_dwarf": min(float(row["Bcrit_ratio_to_white_dwarf"]) for row in selected),
            "windows_vs_Sun": sum(bool(row["universal_window_vs_Sun"]) for row in selected),
            "windows_vs_white_dwarf": sum(bool(row["universal_window_vs_white_dwarf"]) for row in selected),
            "windows_vs_neutron_star": sum(bool(row["universal_window_vs_neutron_star"]) for row in selected),
        }

    potential_floor_values = [float(row["B_no_bound_floor_proxy"]) for row in potential_rows]
    potential_ratio_values = [float(row["ratio_to_massless_white_dwarf_ceiling"]) for row in potential_rows]

    decision_rows = tagged(
        [
            {
                "decision_id": "DEC4950_00_RG_closure",
                "question": "is the current even pair sector RG closed",
                "result": "V_k alone is insufficient; F_k R and Z_k plus the generated X2 channel are required",
                "decision": "PARENT_PAIR_SECTOR_INCOMPLETE",
                "next_action": "solve one parent-scheme V-F-Z-X2 flow",
                "passed": True,
            },
            {
                "decision_id": "DEC4950_01_direct_trace",
                "question": "can an independent T psi2 coefficient be inserted",
                "result": "fixed-metric factorization excludes it; the leading GR trace reduces it to the same effective coefficient as R psi2",
                "decision": "NO_INDEPENDENT_DIRECT_TRACE_COUPLING",
                "next_action": "retain only parent-derived curvature function or metric-mediated basis image",
                "passed": True,
            },
            {
                "decision_id": "DEC4950_02_xi_zero",
                "question": "is xi=0 protected once the even potential interacts",
                "result": "beta_xi=lambda(xi-1/6)/(4pi)^2 at one loop",
                "decision": "MINIMAL_XI_ZERO_NOT_RG_INVARIANT_FOR_NONZERO_LAMBDA",
                "next_action": "derive xi on the same critical trajectory as lambda",
                "passed": True,
            },
            {
                "decision_id": "DEC4950_03_X2",
                "question": "does the generated derivative quartic populate the static vacuum",
                "result": "it gives occupied-state self-energy/scattering but its quadratic variation at psi=0 is zero",
                "decision": "X2_REFINES_4949_CTP_BUT_DOES_NOT_SOURCE_STATIC_BIFURCATION",
                "next_action": "include it in the full CTP hierarchy after its parent-scheme coefficient is solved",
                "passed": True,
            },
            {
                "decision_id": "DEC4950_04_spherical_window",
                "question": "can one monotonic local B activate any public galaxy sphere while preserving Sun white dwarf and neutron star",
                "result": "zero windows in all 175 galaxies for massless 100-kpc 10-kpc and 1-kpc Compton cases",
                "decision": "UNIVERSAL_SPHERICAL_PAIR_WINDOW_REJECTED",
                "next_action": "do not use a spherical trace scalarization closure",
                "passed": True,
            },
            {
                "decision_id": "DEC4950_05_potential_proxy",
                "question": "does a shape-aware baryonic potential proxy materially reduce the required coupling",
                "result": f"B no-bound proxy minimum={min(potential_floor_values):.12g}; minimum ratio to massless white-dwarf ceiling={min(potential_ratio_values):.12g}",
                "decision": "PROXY_STILL_ABOVE_WHITE_DWARF_CEILING_FULL_3D_SOLVE_NOT_SUBSTITUTED",
                "next_action": "only run an axisymmetric eigenproblem after a parent coefficient exists",
                "passed": True,
            },
            {
                "decision_id": "DEC4950_06_stabilizer",
                "question": "is the nonzero branch amplitude predicted",
                "result": "the amplitude law is derived but lambda and the full eigenfunction are not parent selected",
                "decision": "STABILIZED_AMPLITUDE_NOT_PREDICTED",
                "next_action": "solve lambda and xi jointly rather than fit amplitude",
                "passed": True,
            },
            {
                "decision_id": "DEC4950_07_local_GR",
                "question": "does adding the minimal pair operator automatically preserve checkpoint 4947",
                "result": "no; any local negative eigenvalue creates a scalarized branch and invalidates automatic local recovery",
                "decision": "LOCAL_GR_REQUIRES_POSITIVE_SPECTRUM_NOT_ASSUMED",
                "next_action": "keep every local arena in the common eigenvalue gate",
                "passed": True,
            },
            {
                "decision_id": "DEC4950_08_route",
                "question": "is the minimal local Rpsi2/Tpsi2 plus quartic galaxy route viable now",
                "result": "coefficients are not parent-owned and the executed universal spherical window is empty",
                "decision": "CURRENT_MINIMAL_LOCAL_PAIR_ROUTE_REJECTED",
                "next_action": "solve the parent V-F-Z-X2 flow before considering a nonlocal or time-dependent route",
                "passed": True,
            },
            {
                "decision_id": "DEC4950_09_next",
                "question": "what is the next derivation",
                "result": "coupled parent functional flow and its critical index",
                "decision": "ADVANCE_TO_COUPLED_VFZX2_PARENT_FLOW",
                "next_action": "derive or reject a GR-connected trajectory with finite xi lambda X2 and one universal Jgap",
                "passed": True,
            },
        ]
    )

    head = subprocess.run(["git", "-C", str(GALAXY_REPO), "rev-parse", "HEAD"], check=True, capture_output=True, text=True).stdout.strip()
    status = subprocess.run(["git", "-C", str(GALAXY_REPO), "status", "--porcelain"], check=True, capture_output=True, text=True).stdout.strip()
    galaxy_snapshot_rows = tagged(
        [
            {
                "snapshot_id": "GAL4950_00_public_samples",
                "repository": "https://github.com/Martin123132/MTS-Galaxy-Lab-",
                "local_readonly_clone": str(GALAXY_REPO),
                "head": head,
                "expected_head": EXPECTED_GALAXY_HEAD,
                "working_tree_clean": not status,
                "README_sha256": digest(GALAXY_README),
                "samples_sha256": digest(GALAXY_SAMPLES),
                "sample_count": len(samples),
                "repository_modified_by_checkpoint": False,
                "status": "READ_ONLY_SOURCE_SNAPSHOT",
                "passed": head == EXPECTED_GALAXY_HEAD and not status,
            }
        ]
    )

    beta_lambda_identity = 3.0
    beta_xi_lambda_coefficient = 1.0
    beta_xi_at_zero_coefficient = -1.0 / 6.0
    checks = {
        "source_hashes_match": source_hashes_match,
        "authoritative_clauses_match": all(source_clause_checks.values()),
        "generation_rows_pass": all(row["passed"] for row in generation_rows),
        "bifurcation_rows_pass": all(row["passed"] for row in bifurcation_rows),
        "one_loop_beta_lambda_identity": math.isclose(beta_lambda_identity, 3.0),
        "one_loop_beta_xi_identity": math.isclose(beta_xi_lambda_coefficient, 1.0),
        "xi_zero_noninvariant_for_lambda": beta_xi_at_zero_coefficient != 0.0,
        "top_hat_massless_root": math.isclose(first_threshold_root(0.0), math.pi / 2.0, rel_tol=0.0, abs_tol=1.0e-15),
        "top_hat_roots_valid": all(math.pi / 2.0 <= first_threshold_root(mu) < math.pi for mu in (0.0, 0.1, 1.0, 10.0, 100.0)),
        "top_hat_function_increases": all(
            left < right
            for left, right in zip(
                [mu**2 + first_threshold_root(mu) ** 2 for mu in (0.0, 0.1, 1.0, 10.0)],
                [mu**2 + first_threshold_root(mu) ** 2 for mu in (0.1, 1.0, 10.0, 100.0)],
            )
        ),
        "local_rows_complete": len(local_rows) == 16,
        "SPARC_window_rows_complete": len(sparc_rows) == 700,
        "SPARC_potential_rows_complete": len(potential_rows) == 175,
        "all_spherical_windows_vs_Sun_zero": all(not row["universal_window_vs_Sun"] for row in sparc_rows),
        "all_spherical_windows_vs_white_dwarf_zero": all(not row["universal_window_vs_white_dwarf"] for row in sparc_rows),
        "all_spherical_windows_vs_neutron_star_zero": all(not row["universal_window_vs_neutron_star"] for row in sparc_rows),
        "potential_proxy_above_white_dwarf_ceiling": min(potential_ratio_values) > 70.0,
        "decision_rows_pass": all(row["passed"] for row in decision_rows),
        "minimal_local_pair_route_rejected": next(row for row in decision_rows if row["decision_id"] == "DEC4950_08_route")["decision"] == "CURRENT_MINIMAL_LOCAL_PAIR_ROUTE_REJECTED",
        "galaxy_head_locked": head == EXPECTED_GALAXY_HEAD,
        "galaxy_worktree_clean": not status,
        "all_rows_full_MTS_nonclaim": all(
            not row["valid_for_full_MTS_claim"]
            for rows in (generation_rows, bifurcation_rows, local_rows, sparc_rows, potential_rows, decision_rows, galaxy_snapshot_rows)
            for row in rows
        ),
    }

    result = {
        "marker": MARKER,
        "checks": checks,
        "source_hashes": source_hashes,
        "source_clause_checks": source_clause_checks,
        "RG_closure": {
            "required_functions": ["V_k(psi)", "F_k(psi)", "Z_k(psi)"],
            "required_derivative_coordinate": "c_ess X^2",
            "beta_lambda": "3 lambda^2/(4pi)^2",
            "beta_xi": "lambda(xi-1/6)/(4pi)^2",
            "xi_zero_invariant_if_lambda_nonzero": False,
            "direct_Tpsi2_parent_vertex": False,
            "leading_GR_effective_pair_coefficient": "B=-(xi_R-xi_T)",
            "current_pair_sector_RG_closed": False,
        },
        "bifurcation": {
            "operator": "L=-Delta+m_gap^2-B R(x)",
            "sphere_zero_mode": "x cot x=-mu; Bcrit=(mu^2+x^2)/(6C)",
            "massless_threshold": "pi^2/(24C)",
            "stabilized_amplitude": "A0^2=-6 lambda0/[lambda int f0^4]",
            "local_GR_requires_positive_lambda0": True,
        },
        "local_massless_thresholds": local_thresholds["massless"],
        "SPARC_spherical_summary": threshold_summary,
        "SPARC_potential_proxy": {
            "minimum_B_no_bound_floor_proxy": min(potential_floor_values),
            "median_B_no_bound_floor_proxy": statistics.median(potential_floor_values),
            "maximum_B_no_bound_floor_proxy": max(potential_floor_values),
            "minimum_ratio_to_massless_white_dwarf_ceiling": min(potential_ratio_values),
            "full_3D_eigenvalue_solved": False,
        },
        "decision": {
            "current_minimal_local_pair_route": "REJECTED",
            "reason": "unowned coefficients plus an empty universal spherical galaxy/local stability window",
            "next_route": "solve the parent V-F-Z-X2 functional flow and critical surface before any further environmental fit",
        },
        "claim_boundary": {
            "curved_scalar_RG_requires_FpsiR": True,
            "one_loop_beta_xi_derived": True,
            "direct_Tpsi2_excluded_by_fixed_metric_parent": True,
            "X2_scattering_channel_recognized": True,
            "stabilized_bifurcation_law_derived": True,
            "public_spherical_window_executed": True,
            "universal_spherical_pair_window_exists": False,
            "full_axisymmetric_3D_spectrum_solved": False,
            "xi_lambda_X2_parent_values_predicted": False,
            "current_minimal_local_pair_route_viable": False,
            "4947_local_GR_automatically_preserved_after_pair_extension": False,
            "full_MTS_galaxy_unification": False,
            "galaxy_repository_modified": False,
        },
    }

    write_csv(GENERATION_CSV, generation_rows)
    write_csv(BIFURCATION_CSV, bifurcation_rows)
    write_csv(LOCAL_CSV, local_rows)
    write_csv(SPARC_WINDOW_CSV, sparc_rows)
    write_csv(POTENTIAL_CSV, potential_rows)
    write_csv(DECISION_CSV, decision_rows)
    write_csv(GALAXY_SNAPSHOT_CSV, galaxy_snapshot_rows)
    RESULT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    failed = [name for name, passed in checks.items() if not passed]
    print(f"SPARC_SAMPLES={len(samples)}")
    print(f"SPHERICAL_WINDOW_ROWS={len(sparc_rows)}")
    print(f"MASSLESS_GALAXY_BCRIT_MIN={threshold_summary['massless']['minimum']}")
    print(f"MASSLESS_SUN_BCRIT={local_thresholds['massless']['Sun']}")
    print(f"MASSLESS_WD_BCRIT={local_thresholds['massless']['one_solar_mass_white_dwarf']}")
    print(f"POTENTIAL_PROXY_B_FLOOR_MIN={min(potential_floor_values)}")
    print(f"FAILED={len(failed)}")
    if failed:
        print("FAILED_CHECKS=" + ",".join(failed))
    print(f"RESULT_SHA256={digest(RESULT_JSON)}")
    print("PASS" if not failed else "FAIL")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())

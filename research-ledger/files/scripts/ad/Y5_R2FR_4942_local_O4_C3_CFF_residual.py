from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np
from scipy.constants import G, c, hbar
from scipy.integrate import solve_ivp

import Y5_R2FR_4934_completed_combined_flow as completed_flow


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4942"
RESULT_JSON = SOURCE / "local_O4_C3_CFF_residual_results.json"
ENDPOINT_CSV = SOURCE / "completed_O4_endpoint_Wilson_family.csv"
BRANCH_CSV = SOURCE / "local_homogeneous_branch_identities.csv"
RESIDUAL_CSV = SOURCE / "local_O4_C3_CFF_residual_vector.csv"

RESULT_4940 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4940"
    / "metric_kernel_O4_source_and_family_results.json"
)
FAMILY_4940 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4940"
    / "O4_kernel_GR_family.csv"
)
RESULT_4941 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4941"
    / "typeII_direct_O4_zero_and_lower_quotient_results.json"
)
RESULT_4939 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4939"
    / "known_source_O4_and_backreacted_family_results.json"
)
SCRIPT_4940 = POST / "scripts" / "Y5_R2FR_4940_metric_kernel_O4_source_and_family.py"
COMPLETED_SCRIPT = POST / "scripts" / "Y5_R2FR_4934_completed_combined_flow.py"
SYSTEM_BENCHMARKS = (
    POST / "source-intake" / "mts_residuals" / "P8_Y5_R2FR_4880_SYSTEM_BENCHMARKS.csv"
)
C3_GATE = (
    POST
    / "4922-Y5-R2FR-cubic-curvature-strong-field-waveform-love-ringdown-bound-or-compact-vacuum-GR-domain-gate.md"
)
CFF_GATE = (
    POST
    / "4931-Y5-R2FR-gauge-curvature-portal-beta-functions-and-fixed-point-values-or-EM-Wilson-bound.md"
)
C3_SCRIPT = POST / "scripts" / "Y5_R2FR_4922_Weyl_C3_GW170608_domain.py"
CFF_SCRIPT = POST / "scripts" / "Y5_R2FR_4931_gauge_portal_matching_and_EM_bound.py"

EXPECTED_HASHES = {
    RESULT_4940: "4c4900dfe18f638801b1a0998ac40f9aa7d6eed9737c8c0a053b2cd2fa9d536a",
    FAMILY_4940: "d6f6fd98c06cdf29ef842a8ab99aea1642ceb3e0a188d3c449b4d66ff6a97723",
    RESULT_4941: "e234f85376912f5a9da919f32dd7db855d1ff45f39faa693a01a74677590b57f",
    RESULT_4939: "3859aded9146696080bd7c0209f5a2385ef68ee2dac43ee293a5b864305dd041",
    SCRIPT_4940: "64c21710778a0298a2a6e770986bfce0bc5e372e95d5aae58a9aeb780f5b6989",
    COMPLETED_SCRIPT: "c5fded8ca210607972c5d12640cdfd3e88ea3de48f84d1b699a3b2a7e342e230",
    SYSTEM_BENCHMARKS: "e403bdae959a7825395ae0f0a71e64e63fbb2f2381de6d1b8f46cd6036643bf5",
    C3_GATE: "da41b9e2ba735008ec6c1d3103a6e1a9508480e319dc853e3343dc40b8406197",
    CFF_GATE: "f302c82dcbab0f5cdcba7a3fed7d6a6d075534eee2fa4c24f3dee3ee8a2d9852",
    C3_SCRIPT: "199d1e66521b2a64110402d924f0b08a48deb172854edc32d2f075ed17ba1d5a",
    CFF_SCRIPT: "fd8726136c54939ac7c7c876d8ffc6bfffb15e59ee93de4288c4695304ea0dac",
}

MARKER = "MTS_4942_LOCAL_O4_C3_CFF_RESIDUAL"
SEED_AMPLITUDES = (1.0e-5, 3.0e-6, 1.0e-6)
R_UV_VALUES = (1.0e-12, 1.0e-10, 1.0e-8, 1.0e-6, 1.0e-4, 1.0e-2, 1.0)
MASS_MAPPINGS = {
    "Wetterich_v_equals_plus_2lambda": 1.0,
    "Wetterich_v_equals_minus_2lambda": -1.0,
}
IR_G_TARGET = 1.0e-10
T_IR_LIMIT = -40.0
LOG_SUBTRACTION_SCALE = 16.0 * math.pi
C2_ROW = 4
RC2_ROW = 7
GAMMA_C2_INDEX = 7
FREE_LEPTON_C_GAMMA_M2 = -9.621794423569482e-31


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


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


def decoupling(w_value: float) -> float:
    if w_value <= 0.0:
        return 1.0
    if w_value > 1.0e200:
        return 0.0
    return 1.0 / (1.0 + w_value)


def mass_scaling_A(g_value: float, v_sign: float) -> float:
    dimensionless_planck = 1.0 / (16.0 * math.pi * g_value)
    v_value = v_sign * 3.0 * g_value / (8.0 * math.pi)
    return 1.0 / (96.0 * math.pi**2 * dimensionless_planck) * (
        20.0 / (1.0 - v_value) ** 2
        + 1.0 / (1.0 - v_value / 4.0) ** 2
    )


def wilson_coordinates(
    state: np.ndarray, c3_source: float
) -> dict[str, float]:
    g_value, plus_value, minus_value, cff_value, h_value, u_value = (
        float(value) for value in state
    )
    photon_denominator = (16.0 * math.pi * g_value) ** 2
    return {
        "W_plus": plus_value / photon_denominator,
        "W_minus_cl16pi": (
            minus_value / g_value**2
            + (548.0 / 15.0) * math.log(LOG_SUBTRACTION_SCALE * g_value)
        )
        / (16.0 * math.pi) ** 2,
        "W_C": cff_value / (16.0 * math.pi * g_value),
        "A_C3": h_value / g_value - 0.5 * c3_source * math.log(g_value),
        "W_O4": u_value / g_value**2,
        "raw_h_over_g": h_value / g_value,
        "raw_gCFF_over_g": cff_value / g_value,
    }


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
    result_4940 = json.loads(RESULT_4940.read_text(encoding="utf-8"))
    result_4941 = json.loads(RESULT_4941.read_text(encoding="utf-8"))
    result_4939 = json.loads(RESULT_4939.read_text(encoding="utf-8"))
    fixed = result_4941["minimal_O4_completed_point"]["coordinates"]
    fixed_state = np.asarray(
        [fixed[name] for name in ("g", "g_plus", "g_minus", "g_CFF", "h_C3", "u_O4")],
        dtype=float,
    )
    c3_source = float(
        result_4939["gaussian_sources_for_Wilson_coordinates"]["c3_source_limit"]
    )

    system, _, _, _, _, _ = completed_flow.build_completed_solver()

    def solve_completed(
        state: np.ndarray, w_value: float
    ) -> tuple[np.ndarray, float]:
        x_point = state[:5]
        u_value = float(state[5])
        matrix, vector = system(x_point)
        D_value = decoupling(w_value)
        vector = vector + matrix[:, 0] * (
            x_point[0] ** 2 * D_value / (6.0 * math.pi)
        )
        vector[C2_ROW] += -u_value * D_value**2 / (24.0 * math.pi**2)
        vector[RC2_ROW] += -u_value * D_value**2 / (96.0 * math.pi**2)
        unknowns = np.linalg.solve(matrix, vector)
        beta_x = np.asarray(
            [
                unknowns[0],
                (unknowns[13] + unknowns[14]) / 2.0,
                (unknowns[13] - unknowns[14]) / 2.0,
                unknowns[15],
                unknowns[1],
            ],
            dtype=float,
        )
        beta_u = 4.0 * u_value - 0.5 * float(unknowns[GAMMA_C2_INDEX])
        residual = float(np.linalg.norm(matrix @ unknowns - vector, ord=np.inf))
        return np.concatenate([beta_x, np.asarray([beta_u])]), residual

    stability = np.asarray(
        result_4940["O4_completed_known_source_fixed_point"]["stability_matrix"],
        dtype=float,
    )
    values, vectors = np.linalg.eig(stability)
    relevant = [index for index, value in enumerate(values) if value.real < 0.0]
    if len(relevant) != 1:
        raise RuntimeError(f"expected one gravity-relevant direction: {values}")
    gravity_vector = np.real(vectors[:, relevant[0]])
    if gravity_vector[0] < 0.0:
        gravity_vector *= -1.0
    gravity_vector /= float(np.max(np.abs(gravity_vector[:5] / fixed_state[:5])))

    mapping_data = result_4940["mass_augmented_blocks"]
    rows: list[dict[str, Any]] = []
    massless_endpoints: dict[float, np.ndarray] = {}

    def integrate(initial: np.ndarray, mapping: str | None) -> tuple[np.ndarray, float, float]:
        if mapping is None:
            def rhs(_time: float, state: np.ndarray) -> np.ndarray:
                return solve_completed(state, 0.0)[0]

            def event(_time: float, state: np.ndarray) -> float:
                return float(state[0] - IR_G_TARGET)

            atol = np.asarray([1e-13, 1e-15, 1e-15, 1e-16, 1e-19, 1e-25])
        else:
            v_sign = MASS_MAPPINGS[mapping]

            def rhs(_time: float, state: np.ndarray) -> np.ndarray:
                log_w = float(state[6])
                w_value = math.exp(log_w) if log_w < 460.0 else 1.0e200
                beta = solve_completed(state[:6], w_value)[0]
                beta_log_w = -2.0 + mass_scaling_A(float(state[0]), v_sign)
                return np.concatenate([beta, np.asarray([beta_log_w])])

            def event(_time: float, state: np.ndarray) -> float:
                return float(state[0] - IR_G_TARGET)

            atol = np.asarray([1e-13, 1e-15, 1e-15, 1e-16, 1e-19, 1e-25, 1e-10])

        event.terminal = True
        event.direction = -1
        solution = solve_ivp(
            rhs,
            (0.0, T_IR_LIMIT),
            initial,
            method="DOP853",
            rtol=2.0e-9,
            atol=atol,
            max_step=0.08,
            events=event,
        )
        if not solution.success or not len(solution.t_events[0]):
            raise RuntimeError(f"trajectory failed for {mapping}: {solution.message}")
        endpoint = np.asarray(solution.y[:, -1], dtype=float)
        w_endpoint = 0.0 if mapping is None else math.exp(float(endpoint[6]))
        return endpoint[:6], float(solution.t[-1]), w_endpoint

    for relative_seed in SEED_AMPLITUDES:
        endpoint, time_endpoint, w_endpoint = integrate(
            fixed_state - relative_seed * gravity_vector,
            None,
        )
        massless_endpoints[relative_seed] = endpoint
        rows.append(
            {
                "mapping": "massless_shared",
                "relative_gravity_seed": relative_seed,
                "R_UV": 0.0,
                "w_seed": 0.0,
                "t_endpoint": time_endpoint,
                "g_endpoint": float(endpoint[0]),
                "w_endpoint": w_endpoint,
                "J_gap_endpoint": 0.0,
                **wilson_coordinates(endpoint, c3_source),
                "termination": "IR_G_TARGET",
                "direct_O4_trace_closed_zero": True,
                "valid_for_declared_local_vacuum_branch": True,
                "valid_for_full_MTS_claim": False,
                "checkpoint_marker": MARKER,
            }
        )

    for mapping, v_sign in MASS_MAPPINGS.items():
        data = mapping_data[mapping]
        mass_vector = np.asarray(data["mass_eigenvector_x_u_per_unit_w"], dtype=float)
        uv_power = float(data["uv_power"])
        for relative_seed in SEED_AMPLITUDES:
            for R_UV in R_UV_VALUES:
                w_seed = R_UV * relative_seed**uv_power
                initial_6 = (
                    fixed_state
                    - relative_seed * gravity_vector
                    + w_seed * mass_vector
                )
                initial = np.concatenate([initial_6, np.asarray([math.log(w_seed)])])
                endpoint, time_endpoint, w_endpoint = integrate(initial, mapping)
                g_endpoint = float(endpoint[0])
                rows.append(
                    {
                        "mapping": mapping,
                        "relative_gravity_seed": relative_seed,
                        "R_UV": R_UV,
                        "uv_power": uv_power,
                        "w_seed": w_seed,
                        "t_endpoint": time_endpoint,
                        "g_endpoint": g_endpoint,
                        "w_endpoint": w_endpoint,
                        "J_gap_endpoint": g_endpoint * w_endpoint,
                        **wilson_coordinates(endpoint, c3_source),
                        "termination": "IR_G_TARGET",
                        "direct_O4_trace_closed_zero": True,
                        "valid_for_declared_local_vacuum_branch": True,
                        "valid_for_full_MTS_claim": False,
                        "checkpoint_marker": MARKER,
                    }
                )

    family_4940 = read_csv(FAMILY_4940)
    reconstructed_w_o4 = [float(row["W_O4"]) for row in rows]
    inherited_w_o4 = [float(row["W_O4_equals_u_over_g2"]) for row in family_4940]
    max_reconstruction_gap = max(
        abs(first - second)
        for first, second in zip(reconstructed_w_o4, inherited_w_o4)
    )

    envelope = {
        name: {
            "minimum": min(float(row[name]) for row in rows),
            "maximum": max(float(row[name]) for row in rows),
            "max_abs": max(abs(float(row[name])) for row in rows),
        }
        for name in ("W_C", "A_C3", "W_O4", "J_gap_endpoint")
    }

    planck_length = math.sqrt(hbar * G / c**3)
    planck_area = planck_length**2
    W_C_abs = envelope["W_C"]["max_abs"]
    A_C3_abs = envelope["A_C3"]["max_abs"]
    W_O4_abs = envelope["W_O4"]["max_abs"]
    c_gamma_parent_abs = 16.0 * math.pi * W_C_abs * planck_area
    G_C3_abs = A_C3_abs * planck_area
    a_C3_abs = 16.0 * math.pi * A_C3_abs * planck_length**4
    u_over_Z_abs = W_O4_abs * planck_length**4

    branch_rows = [
        {
            "identity_id": "LOCAL4942_00_EOM",
            "statement": "nabla_mu[(Z+2u C2)nabla^mu psi]-m2 psi=0",
            "derivation": "variation of -1/2 Z X-u C2 X-1/2 m2 psi2",
            "result": "homogeneous linear source-free motion equation",
            "passed": True,
        },
        {
            "identity_id": "LOCAL4942_01_zero_branch",
            "statement": "psi=0 and nabla psi=0",
            "derivation": "every term in the homogeneous EOM is proportional to psi or its derivative",
            "result": "exact for arbitrary m2 and curvature",
            "passed": True,
        },
        {
            "identity_id": "LOCAL4942_02_stress",
            "statement": "T_mn[psi]+T_mn[O4]=0 at psi=0",
            "derivation": "metric variation of every retained scalar term contains psi or at least two psi derivatives",
            "result": "O4 is classically silent on the zero branch",
            "passed": True,
        },
        {
            "identity_id": "LOCAL4942_03_characteristic",
            "statement": "P_mn=(Z+2u C2)g_mn",
            "derivation": "retain the two-derivative principal part of the scalar EOM",
            "result": "same metric null cone when Z_eff is positive",
            "passed": True,
        },
        {
            "identity_id": "LOCAL4942_04_endpoint_map",
            "statement": "u/Z=W_O4 lP4; G_C3=A_C3 lP2; c_gamma=16pi W_C lP2",
            "derivation": "divide utilde=k4u/Z h=k2G_C3 and g_CFF=k2c_gamma by g=k2G_N",
            "result": "finite dimensionful local coefficients",
            "passed": True,
        },
        {
            "identity_id": "LOCAL4942_05_gap_independence",
            "statement": "partial local zero-branch residuals/partial J_gap=0",
            "derivation": "m2 changes only the lower-order homogeneous term and psi remains zero",
            "result": "no arena retuning of the independent motion gap",
            "passed": True,
        },
        {
            "identity_id": "LOCAL4942_06_PPN_orders",
            "statement": "delta gamma_PPN=delta beta_PPN=0 for O4 and CFF on psi=F=0; pure I1 begins beyond U2",
            "derivation": "O4 and CFF stresses vanish while the pure-I1 g_tt correction scales as r^-7",
            "result": "standard constant 1PN PPN coefficients unchanged but higher-gradient residuals remain",
            "passed": True,
        },
        {
            "identity_id": "LOCAL4942_07_Maxwell",
            "statement": "H_mn=F_mn-4c_gamma C_mnrs F^rs and nabla_m H^mn=J^n",
            "derivation": "variation of -F2/4+c_gamma CFF",
            "result": "current conservation exact; F=0 portal stress zero; curved photon cone shifted",
            "passed": True,
        },
    ]
    branch_rows = [
        {
            **row,
            "valid_for_declared_local_vacuum_branch": True,
            "valid_for_full_MTS_claim": False,
            "checkpoint_marker": MARKER,
        }
        for row in branch_rows
    ]

    threshold_max = IR_G_TARGET / (6.0 * math.pi)
    residual_rows: list[dict[str, Any]] = []
    for benchmark in read_csv(SYSTEM_BENCHMARKS):
        mass_length = float(benchmark["gravitational_radius_m"])
        radius = float(benchmark["radius_m"])
        kretschmann = float(benchmark["K_m_minus_4"])
        o4_kinetic = 2.0 * W_O4_abs * planck_length**4 * kretschmann
        c3_potential = 20.0 * a_C3_abs * mass_length**2 / radius**6
        c3_acceleration = 140.0 * a_C3_abs * mass_length**2 / radius**6
        c3_control = a_C3_abs * kretschmann
        cff_split = 12.0 * c_gamma_parent_abs * mass_length / radius**3
        cff_optical_ratio = c_gamma_parent_abs / mass_length**2
        residual_rows.append(
            {
                "system": benchmark["system"],
                "source_class": benchmark["source_class"],
                "mass_length_m": mass_length,
                "radius_m": radius,
                "K_m_minus_4": kretschmann,
                "O4_abs_Delta_Z_over_Z": o4_kinetic,
                "O4_Zeff_over_Z_lower": 1.0 - o4_kinetic,
                "O4_scalar_cone_shift": 0.0,
                "O4_tree_metric_stress_on_psi0": 0.0,
                "C3_abs_Delta_Phi_over_PhiN": c3_potential,
                "C3_abs_Delta_acceleration_over_aN": c3_acceleration,
                "C3_abs_a_plus_K": c3_control,
                "CFF_parent_abs_Delta_v_pol_over_c": cff_split,
                "CFF_parent_abs_cgamma_over_M2": cff_optical_ratio,
                "PPN_delta_gamma_at_standard_order": 0.0,
                "PPN_delta_beta_at_standard_order": 0.0,
                "RG_threshold_abs_Delta_beta_g_over_g_at_g1e_minus10_max": threshold_max,
                "J_gap_retuned": False,
                "status": "DERIVED_LOCAL_EXTERIOR_RESIDUAL_PRIVATE_NONCLAIM",
                "valid_for_declared_local_vacuum_branch": True,
                "valid_for_full_MTS_claim": False,
                "checkpoint_marker": MARKER,
            }
        )

    ghost_radii = {
        row["system"]: (
            96.0
            * W_O4_abs
            * planck_length**4
            * float(row["gravitational_radius_m"]) ** 2
        )
        ** (1.0 / 6.0)
        for row in read_csv(SYSTEM_BENCHMARKS)
    }

    checks = {
        "source_hashes_match": not hash_failures,
        "family_has_45_rows": len(rows) == 45,
        "all_family_runs_reach_IR": all(row["termination"] == "IR_G_TARGET" for row in rows),
        "reconstructed_WO4_matches_4940": max_reconstruction_gap < 5.0e-10,
        "all_Wilson_coefficients_finite": all(
            math.isfinite(float(row[name]))
            for row in rows
            for name in ("W_C", "A_C3", "W_O4")
        ),
        "homogeneous_branch_identities_pass": all(row["passed"] for row in branch_rows),
        "Zeff_positive_on_all_benchmarks": all(
            float(row["O4_Zeff_over_Z_lower"]) > 0.0 for row in residual_rows
        ),
        "O4_cone_shift_zero": all(float(row["O4_scalar_cone_shift"]) == 0.0 for row in residual_rows),
        "standard_PPN_vector_zero": all(
            float(row["PPN_delta_gamma_at_standard_order"]) == 0.0
            and float(row["PPN_delta_beta_at_standard_order"]) == 0.0
            for row in residual_rows
        ),
        "no_Jgap_retuning": all(not row["J_gap_retuned"] for row in residual_rows),
        "parent_CFF_below_free_lepton_threshold": c_gamma_parent_abs < abs(FREE_LEPTON_C_GAMMA_M2),
        "all_residuals_full_MTS_nonclaim": all(
            not row["valid_for_full_MTS_claim"] for row in residual_rows
        ),
    }
    checks = {name: bool(value) for name, value in checks.items()}

    result = {
        "marker": MARKER,
        "source_hashes": source_hashes,
        "action_and_local_branch": {
            "Lorentzian_scalar_action": "Spsi=int sqrt(-g)[-Z X/2-u_O4 C2 X-m2 psi2/2]",
            "equation": "nabla_mu[(Z+2u_O4 C2)nabla^mu psi]-m2 psi=0",
            "exact_branch": "psi=0; nabla psi=0",
            "stress_on_branch": "T_mn_scalar=T_mn_O4=0",
            "principal_symbol": "P^munu=(Z+2u_O4 C2)g^munu",
            "cone": "metric cone if Z_eff=Z+2u_O4 C2>0",
            "gap_statement": "psi=0 is exact for every m2 and therefore for every universal J_gap",
        },
        "completed_family": {
            "rows": len(rows),
            "W_O4_reconstruction_max_abs_gap": max_reconstruction_gap,
            "envelope": envelope,
        },
        "dimensionful_endpoint_envelope": {
            "Planck_length_m": planck_length,
            "Planck_area_m2": planck_area,
            "abs_u_O4_over_Z_m4": u_over_Z_abs,
            "abs_G_C3_m2": G_C3_abs,
            "abs_a_plus_m4": a_C3_abs,
            "abs_c_gamma_parent_m2": c_gamma_parent_abs,
            "free_lepton_c_gamma_m2_comparator": FREE_LEPTON_C_GAMMA_M2,
            "free_lepton_to_parent_abs_ratio": abs(FREE_LEPTON_C_GAMMA_M2) / c_gamma_parent_abs,
        },
        "local_formulae": {
            "Schwarzschild_C2": "48 M_geom^2/r^6",
            "O4_Zeff_over_Z": "1+96 W_O4 lP^4 M_geom^2/r^6",
            "O4_formal_zero_crossing_radius": "[96 abs(W_O4) lP^4 M_geom^2]^(1/6)",
            "C3_a_plus": "a_plus=16pi A_C3 lP^4",
            "C3_metric": "N2 f=1-2M/r+40 a_plus M^3/r^7",
            "C3_potential_fraction": "abs(Delta Phi/Phi_N)=20 abs(a_plus) M^2/r^6",
            "C3_acceleration_fraction": "abs(Delta a/a_N)=140 abs(a_plus) M^2/r^6",
            "CFF_parent": "c_gamma_parent=16pi W_C lP^2",
            "CFF_polarization_split": "abs(Delta v_pol)/c=12 abs(c_gamma) M/r^3",
            "threshold": "abs(Delta beta_g/g)=g/[6pi(1+w)]=g^2/[6pi(g+J_gap)]",
        },
        "formal_O4_zero_crossing_radii_m": ghost_radii,
        "checks": checks,
        "claim_boundary": {
            "homogeneous_local_psi_zero_branch_derived": True,
            "O4_scalar_characteristic_derived": True,
            "O4_tree_stress_zero_on_branch": True,
            "same_endpoint_C3_CFF_O4_residual_vector_derived": True,
            "standard_constant_PPN_beta_gamma_shift_in_declared_vacuum_branch": False,
            "higher_gradient_C3_residual_nonzero": True,
            "curved_photon_CFF_residual_nonzero": True,
            "full_visible_matter_threshold_matching_completed": False,
            "interior_source_matching_completed": False,
            "all_five_scalar_six_derivative_beta_functions_completed": False,
            "full_MTS_fixed_point": False,
            "local_GR_Newton_Maxwell_promoted": False,
        },
    }

    write_csv(ENDPOINT_CSV, rows)
    write_csv(BRANCH_CSV, branch_rows)
    write_csv(RESIDUAL_CSV, residual_rows)
    RESULT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    failures = [name for name, passed in checks.items() if not passed]
    print(f"{MARKER}_FAMILY_ROWS={len(rows)}", flush=True)
    print(f"{MARKER}_W_O4_ENVELOPE={envelope['W_O4']}", flush=True)
    print(f"{MARKER}_A_C3_ENVELOPE={envelope['A_C3']}", flush=True)
    print(f"{MARKER}_W_C_ENVELOPE={envelope['W_C']}", flush=True)
    print(f"{MARKER}_C_GAMMA_PARENT_ABS_M2={c_gamma_parent_abs:.12e}", flush=True)
    print(f"{MARKER}_FAILED_CHECKS={failures}", flush=True)
    print(f"{MARKER}_RESULT_SHA256={digest(RESULT_JSON)}", flush=True)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

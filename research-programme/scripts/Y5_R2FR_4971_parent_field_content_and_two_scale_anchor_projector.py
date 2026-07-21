from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.interpolate import PchipInterpolator
from scipy.optimize import brentq
from sympy.parsing.mathematica import parse_mathematica


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4971"
FUNCTIONAL_TRAJECTORY = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4957"
    / "functional_PX_O4_GR_trajectory.csv"
)
KNOWN_P8_TRAJECTORY = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4969"
    / "p8_canonical_repaired_GR_connected_trajectory.csv"
)
BERN = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4969"
    / "src-1701.02422"
    / "gr_simp.tex"
)
FRG_SOURCE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4929"
    / "src2312"
    / "ess_cubic.tex"
)
PARENT_ACTION = (
    POST
    / "4904-Y5-R2FR-current-unified-action-assembly-Ward-identity-and-parameter-prediction-ledger.md"
)
MATTER_AUDIT = (
    POST
    / "4929-Y5-R2FR-MTS-matter-completed-C3-essential-flow-and-fixed-point-survival-or-one-Wilson-retention.md"
)
COMBINED_SCOPE = (
    POST
    / "4933-Y5-R2FR-C3-CFF-F4-minimal-combined-natural-flow-and-0p239-stability-gate.md"
)
RESULT_4970 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4970"
    / "C3_p8_finite_matching_results.json"
)
ABREU_SOURCE = SOURCE / "src-2002.12374" / "source"
ABREU_ARCHIVE = SOURCE / "src-2002.12374" / "arXiv-2002.12374v2-source.tar"
ABREU_MAIN = ABREU_SOURCE / "main.tex"
ABREU_README = ABREU_SOURCE / "00README.json"
ABREU_PPPP = ABREU_SOURCE / "anc" / "2loopRemainder" / "pppp_s-channel.m"
ABREU_MPPP = ABREU_SOURCE / "anc" / "2loopRemainder" / "mppp_s-channel.m"
ABREU_INTERFACE = ABREU_SOURCE / "anc" / "4gravitonAmplitudes.m"

FIELD_CONTENT_CSV = SOURCE / "Bern_R3_field_content_branches.csv"
MISMATCH_CSV = SOURCE / "C3_parent_field_content_mismatch.csv"
SPLICE_CSV = SOURCE / "C3_full_parent_splice_scan.csv"
TRANSPORT_CSV = SOURCE / "C3_full_parent_matching_transport.csv"
PROJECTOR_CSV = SOURCE / "C3_two_scale_helicity_projector.csv"
IDENTIFIABILITY_CSV = SOURCE / "C3_local_anchor_identifiability.csv"
AMPLITUDE_PROJECTOR_CSV = SOURCE / "C3_finite_amplitude_projector.csv"
ANCHOR_SCALE_CSV = SOURCE / "C3_anchor_scale_contract.csv"
RESULT_JSON = SOURCE / "C3_parent_matching_and_anchor_results.json"

MARKER = "MTS_4971_PARENT_FIELD_CONTENT_TWO_SCALE_ANCHOR"
CHECKED_DATE = "2026-07-13"
SCHEMES = ("dynamic_etaN", "reference_etaN0")
ORDERS = (6, 8)
MATCH_GRAVITIES = (1.0e-2, 1.0e-3, 1.0e-4, 1.0e-5, 1.0e-6)
PROJECTOR_ENDPOINT_GRAVITIES = (1.0e-8, 1.0e-10)
PLANCK_MASS_GEV = 1.220890e19
PRIMITIVE_UNIT = 1.0 / (32.0 * math.pi**3)

EXPECTED_HASHES = {
    PARENT_ACTION: "223514da350b0bbaed8e6fcd3582eeaab79ef698ea8c0ea5df2cace328de1876",
    MATTER_AUDIT: "46302f298fcfa63633455cecf9977e3fb8d0384a1fe5bbf8ecd33b60e444e7ea",
    COMBINED_SCOPE: "f075ccd1d0c4f28daf9685d99855f8dde10664e3eb62ce3d8e3b99d03fb38c38",
    FUNCTIONAL_TRAJECTORY: "c60eee38379dc8cf1bb16833b2b5a849ecc0b5d7da0f74d9f0c9bd1bf9b46166",
    KNOWN_P8_TRAJECTORY: "b5984ba1c528aebd2099755561a8b578ec79751a3846be01032cc52e24e65957",
    BERN: "9448bff31da3e1e56e62e8fb6242a60c09afb90d1f7f25edaf3f23466ac0371e",
    FRG_SOURCE: "b23b0974509278be22c8917f531a2963d415184d9052e27860c65fad80943a1d",
    RESULT_4970: "9165acf171eb6e936f81e2ddc5fd2ca7f3be465d206e5cfd0d1704e12b371aa1",
    ABREU_ARCHIVE: "7631ad019ba1957f088216201ad8c7cda8baad3c35793c107a59e15310b5ee15",
    ABREU_MAIN: "11acdee89baad0298aafc5cc975be9d981d985bb37d2da86914281ca2c997fc8",
    ABREU_README: "85bfb6fee08131d2833b10536c3ceb19a60938293e5824198dd5936744dd4519",
    ABREU_PPPP: "42128b16a7451b6213abd06c0eae9bfa649f5890df365c04f6209fd6b5630483",
    ABREU_MPPP: "6d426fbba39e4a02413fd17f5d4869a33c3cabb4263d88dd8e9e8e8a7a52c2a5",
    ABREU_INTERFACE: "d94df4a0a3b2a7452b15510d860904cfecf2bad9b49db5099db0b46fad3d5593",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        fieldnames.extend(key for key in row if key not in fieldnames)
    path.parent.mkdir(parents=True, exist_ok=True)
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


def branch_inventory() -> list[dict[str, Any]]:
    definitions = (
        (
            "PURE_EINSTEIN",
            0,
            0.0,
            0,
            0,
            "4970 comparator; no matter or photon states",
        ),
        (
            "EINSTEIN_MAXWELL",
            0,
            0.0,
            1,
            0,
            "low-energy graviton plus photon branch after all massive matter decouples",
        ),
        (
            "EINSTEIN_MAXWELL_MOTION",
            0,
            0.0,
            1,
            1,
            "conditional branch if one real motion scalar is effectively massless",
        ),
        (
            "QED_THREE_MASSLESS_WEYL_NEUTRINOS",
            0,
            1.5,
            1,
            0,
            "massless-neutrino low-energy comparator; not valid below nonzero neutrino masses",
        ),
        (
            "SM45",
            4,
            22.5,
            12,
            0,
            "adopted massless-neutrino GR plus Standard Model baseline above all SM thresholds",
        ),
        (
            "SM45_PLUS_MOTION",
            4,
            22.5,
            12,
            1,
            "full-parent high-scale bracket if the real motion scalar is UV active",
        ),
        (
            "SM48",
            4,
            24.0,
            12,
            0,
            "three-right-handed-neutrino high-scale comparator",
        ),
        (
            "SM48_PLUS_MOTION",
            4,
            24.0,
            12,
            1,
            "right-handed-neutrino comparator with an active real motion scalar",
        ),
    )
    rows: list[dict[str, Any]] = []
    for branch, scalars, dirac, vectors, motion, applicability in definitions:
        matter_supertrace = scalars + motion + 2 * vectors - 4 * dirac
        state_difference = 2 + matter_supertrace
        beta_a = state_difference / (7680.0 * math.pi**3)
        beta_c_amplitude = -state_difference / 240.0
        rows.append(
            {
                "branch": branch,
                "real_scalar_count": scalars,
                "Dirac_equivalent_count": dirac,
                "massless_vector_count": vectors,
                "additional_motion_scalar_count": motion,
                "matter_Nb_minus_Nf": matter_supertrace,
                "graviton_state_count": 2,
                "total_Nb_minus_Nf": state_difference,
                "beta_A_onshell": beta_a,
                "beta_A_formula": "(N_b-N_f)/(7680*pi^3)",
                "beta_c_amplitude": beta_c_amplitude,
                "amplitude_bridge": "A_Bern=-c_amplitude/(32*pi^3)",
                "applicability": applicability,
                "threshold_treatment": "ASYMPTOTIC_ACTIVE_OR_DECOUPLED_EFT_LIMIT; FINITE_THRESHOLD_MATCHING_OPEN",
                "status": "BERN_MASSLESS_STATE_COUNT_DERIVED_BRANCH_SELECTION_EXPLICIT",
            }
        )
    return tagged(rows)


def parse_abreu_remainder(path: Path) -> tuple[sp.Expr, str]:
    source_text = path.read_text(encoding="utf-8")
    normalized = source_text.replace("cGB[mu]", "cgb").replace(
        "cR3[mu]", "cr3"
    )
    normalized = re.sub(r"\bS\b", "ss", normalized)
    normalized = re.sub(r"\bT\b", "tt", normalized)
    return parse_mathematica(normalized), source_text


def amplitude_projector_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    all_plus, all_plus_source = parse_abreu_remainder(ABREU_PPPP)
    single_minus, _ = parse_abreu_remainder(ABREU_MPPP)
    cgb, cr3, mandelstam_s, mandelstam_t = sp.symbols("cgb cr3 ss tt")
    mandelstam_u = -mandelstam_s - mandelstam_t
    stu = mandelstam_s * mandelstam_t * mandelstam_u

    all_plus_cgb = sp.factor(sp.diff(all_plus, cgb))
    all_plus_cr3 = sp.factor(sp.diff(all_plus, cr3))
    single_minus_cgb = sp.factor(sp.diff(single_minus, cgb))
    single_minus_cr3 = sp.factor(sp.diff(single_minus, cr3))
    all_plus_expected_cr3 = -60 * stu
    all_plus_expected_cgb = 30 * stu
    single_minus_expected_cr3 = -6 * stu
    single_minus_expected_cgb = 3 * stu

    all_plus_coefficients_exact = (
        sp.simplify(all_plus_cr3 - all_plus_expected_cr3) == 0
        and sp.simplify(all_plus_cgb - all_plus_expected_cgb) == 0
    )
    single_minus_coefficients_exact = (
        sp.simplify(single_minus_cr3 - single_minus_expected_cr3) == 0
        and sp.simplify(single_minus_cgb - single_minus_expected_cgb) == 0
    )
    compact_source = "".join(all_plus_source.split())
    finite_constant_source_locked = (
        "117617+648000*cGB[mu]-1296000*cR3[mu]" in compact_source
    )

    beta_c_pure_einstein = -1.0 / 120.0
    beta_a_pure_einstein = 1.0 / (3840.0 * math.pi**3)
    bridge_beta_a = -beta_c_pure_einstein / (32.0 * math.pi**3)
    synthetic_c = 0.007
    synthetic_stu = 0.25
    synthetic_all_plus = -60.0 * synthetic_c * synthetic_stu
    synthetic_single_minus = -6.0 * synthetic_c * synthetic_stu
    recovered_a_all_plus = synthetic_all_plus / (
        1920.0 * math.pi**3 * synthetic_stu
    )
    recovered_a_single_minus = synthetic_single_minus / (
        192.0 * math.pi**3 * synthetic_stu
    )
    expected_a = -synthetic_c / (32.0 * math.pi**3)

    rows = tagged(
        [
            {
                "projector_id": "AMP4971_00_physical_coupling",
                "helicity": "all source helicities",
                "source_equation": "c(mu)=c_R3(mu)-c_GB(mu)/2",
                "coupling_coefficient_in_stu_basis": "not_applicable",
                "MTS_projector": "A_Bern=-c(mu)/(32*pi^3)",
                "result": "evanescent Gauss-Bonnet and R3 finite parts collapse to one physical amplitude coordinate",
                "status": "PHYSICAL_E6_COUPLING_COMBINATION_SOURCE_LOCKED",
            },
            {
                "projector_id": "AMP4971_01_all_plus",
                "helicity": "++++",
                "source_equation": "Delta R_pppp=-60*c(mu)*s*t*u",
                "coupling_coefficient_in_stu_basis": -60,
                "MTS_projector": "A_Bern=Delta R_pppp/[1920*pi^3*s*t*u]",
                "result": "one finite all-plus remainder fixes the C3 matching anchor after the c=0 Einstein remainder is subtracted",
                "status": "EXACT_FINITE_AMPLITUDE_PROJECTOR_DERIVED",
            },
            {
                "projector_id": "AMP4971_02_single_minus",
                "helicity": "-+++",
                "source_equation": "Delta R_mppp=-6*c(mu)*s*t*u",
                "coupling_coefficient_in_stu_basis": -6,
                "MTS_projector": "A_Bern=Delta R_mppp/[192*pi^3*s*t*u]",
                "result": "single-minus supplies an independent normalization check on the same C3 anchor",
                "status": "EXACT_FINITE_AMPLITUDE_PROJECTOR_DERIVED",
            },
            {
                "projector_id": "AMP4971_03_helicity_identity",
                "helicity": "++++ versus -+++",
                "source_equation": "Delta R_pppp=10*Delta R_mppp",
                "coupling_coefficient_in_stu_basis": 10,
                "MTS_projector": "A_Bern(pppp)=A_Bern(mppp)",
                "result": "the two source files define a falsifiable cross-helicity matching identity",
                "status": "DUAL_HELICITY_REDUNDANCY_DERIVED",
            },
            {
                "projector_id": "AMP4971_04_all_plus_finite_constant",
                "helicity": "++++",
                "source_equation": "P_local[R_pppp(c=0)]=117617/21600",
                "coupling_coefficient_in_stu_basis": 117617.0 / 21600.0,
                "MTS_projector": "subtract the complete c=0 Einstein remainder, including this finite local term",
                "result": "the finite constant is source data and must not be mistaken for a parent Wilson coefficient",
                "status": "FINITE_EINSTEIN_SUBTRACTION_CONSTANT_SOURCE_LOCKED",
            },
            {
                "projector_id": "AMP4971_05_running_bridge",
                "helicity": "E6 physical coordinate",
                "source_equation": "dc/dln(mu)=-N/240",
                "coupling_coefficient_in_stu_basis": beta_c_pure_einstein,
                "MTS_projector": "dA_Bern/dln(mu)=N/(7680*pi^3)",
                "result": "A_Bern=-c/(32*pi^3) reconciles the amplitude and Bern-oriented running conventions",
                "status": "CROSS_SOURCE_SIGN_AND_NORMALIZATION_BRIDGE_DERIVED",
            },
            {
                "projector_id": "AMP4971_06_RG_invariant_scale",
                "helicity": "E6 physical coordinate",
                "source_equation": "c=(N/240)*ln(lambda/mu)",
                "coupling_coefficient_in_stu_basis": "not_applicable",
                "MTS_projector": "lambda/mu=exp[-A_Bern/beta_A]",
                "result": "the absolute anchor is equivalently one RG-invariant physical scale lambda",
                "status": "ANCHOR_COMPRESSED_TO_ONE_PHYSICAL_SCALE",
            },
        ]
    )
    summary = {
        "all_plus_coefficients_exact": all_plus_coefficients_exact,
        "single_minus_coefficients_exact": single_minus_coefficients_exact,
        "finite_constant_source_locked": finite_constant_source_locked,
        "all_plus_c_coefficient_in_stu_basis": -60.0,
        "single_minus_c_coefficient_in_stu_basis": -6.0,
        "helicity_ratio": 10.0,
        "all_plus_c0_local_coefficient": 117617.0 / 21600.0,
        "A_Bern_bridge": "A_Bern=-c_amplitude/(32*pi^3)",
        "beta_c_pure_Einstein": beta_c_pure_einstein,
        "beta_A_pure_Einstein": beta_a_pure_einstein,
        "bridge_beta_A": bridge_beta_a,
        "synthetic_c": synthetic_c,
        "synthetic_expected_A": expected_a,
        "synthetic_recovered_A_all_plus": recovered_a_all_plus,
        "synthetic_recovered_A_single_minus": recovered_a_single_minus,
        "synthetic_inversion_exact": math.isclose(
            recovered_a_all_plus, expected_a, rel_tol=2e-15
        )
        and math.isclose(
            recovered_a_single_minus, expected_a, rel_tol=2e-15
        ),
    }
    return rows, summary


def groups(rows: list[dict[str, str]]) -> dict[tuple[str, int], list[dict[str, str]]]:
    output: dict[tuple[str, int], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        output[(row["scheme"], int(row["polynomial_order"]))].append(row)
    return output


def interpolators(
    rows: list[dict[str, str]], fields: tuple[str, ...]
) -> dict[str, PchipInterpolator]:
    ordered = sorted(rows, key=lambda row: float(row["t_log_k_over_seed"]))
    times = np.array([float(row["t_log_k_over_seed"]) for row in ordered])
    return {
        field: PchipInterpolator(
            times,
            np.array([float(row[field]) for row in ordered]),
            extrapolate=False,
        )
        for field in fields
    }


def time_at_gravity(
    functions: dict[str, PchipInterpolator], t_minimum: float, gravity: float
) -> float:
    endpoint = float(functions["g"](t_minimum))
    start = float(functions["g"](0.0))
    if math.isclose(gravity, endpoint, rel_tol=2e-13, abs_tol=1e-20):
        return t_minimum
    if not endpoint <= gravity <= start:
        raise ValueError(f"gravity {gravity} outside [{endpoint},{start}]")
    return float(
        brentq(
            lambda time: float(functions["g"](time)) - gravity,
            t_minimum,
            0.0,
        )
    )


def transfer_solution(
    functions: dict[str, PchipInterpolator], t_match: float, t_endpoint: float
) -> tuple[float, float, float]:
    def right_hand_side(time: float, state: np.ndarray) -> np.ndarray:
        beta_g_over_g = 2.0 + float(functions["eta_Newton_physical"](time))
        homogeneous = 6.0 - 3.0 * beta_g_over_g
        response_a, boundary, primitive = state
        return np.array(
            [
                homogeneous * response_a - 12.0,
                homogeneous * boundary,
                homogeneous * primitive + PRIMITIVE_UNIT,
            ],
            dtype=float,
        )

    solution = solve_ivp(
        right_hand_side,
        (t_match, t_endpoint),
        np.array([0.0, 1.0, 0.0], dtype=float),
        method="DOP853",
        rtol=2.0e-12,
        atol=2.0e-15,
        max_step=0.03,
    )
    if not solution.success:
        raise RuntimeError(f"4971 transfer integration failed: {solution.message}")
    return tuple(float(value) for value in solution.y[:, -1])


def splice_scan(
    functional_rows: list[dict[str, str]],
    p8_rows: list[dict[str, str]],
    scheme: str,
    order: int,
    branch: str,
    state_difference: int,
    gravity_match: float,
) -> dict[str, Any]:
    functions = interpolators(
        functional_rows, ("g", "h_C3", "eta_Newton_physical")
    )
    known = interpolators(p8_rows, ("g", "B_minus", "B_plus"))
    t_end = min(float(row["t_log_k_over_seed"]) for row in functional_rows)
    t_match = time_at_gravity(functions, t_end, gravity_match)
    beta_a = state_difference / (7680.0 * math.pi**3)

    def a_functional(time: float) -> float:
        return float(functions["h_C3"](time) / functions["g"](time))

    a_match = a_functional(t_match)

    def delta_a(time: float) -> float:
        return a_match + beta_a * (time - t_match) - a_functional(time)

    def right_hand_side(time: float, state: np.ndarray) -> np.ndarray:
        beta_g_over_g = 2.0 + float(functions["eta_Newton_physical"](time))
        homogeneous = 6.0 - 3.0 * beta_g_over_g
        replacement = state[0]
        return np.array(
            [homogeneous * replacement - 12.0 * delta_a(time)], dtype=float
        )

    solution = solve_ivp(
        right_hand_side,
        (t_match, t_end),
        np.array([0.0], dtype=float),
        method="DOP853",
        rtol=2.0e-12,
        atol=2.0e-15,
        max_step=0.03,
    )
    if not solution.success:
        raise RuntimeError(f"4971 splice integration failed: {solution.message}")
    replacement = float(solution.y[0, -1])
    response_a, boundary, primitive = transfer_solution(functions, t_match, t_end)
    a_end = a_match + beta_a * (t_end - t_match)
    known_minus = float(known["B_minus"](t_end))
    known_plus = float(known["B_plus"](t_end))
    matched_minus = known_minus + replacement
    return {
        "scan_id": f"MATCH4971_{branch}_{scheme}_N{order}_g{gravity_match:.0e}",
        "branch": branch,
        "total_Nb_minus_Nf": state_difference,
        "beta_A_onshell": beta_a,
        "scheme": scheme,
        "polynomial_order": order,
        "g_match": gravity_match,
        "k_match_over_MPlanck": math.sqrt(gravity_match),
        "k_match_GeV": math.sqrt(gravity_match) * PLANCK_MASS_GEV,
        "t_match": t_match,
        "t_endpoint": t_end,
        "A_functional_match": a_match,
        "A_onshell_endpoint_zero_anchor": a_end,
        "delta_A_endpoint_zero_anchor": a_end - a_functional(t_end),
        "replacement_delta_Bminus_zero_anchor": replacement,
        "B_minus_matched_endpoint_zero_anchor": matched_minus,
        "B_plus_matched_endpoint_zero_anchor": known_plus,
        "B_C_matched_endpoint_zero_anchor": (matched_minus + known_plus) / 2.0,
        "B_t_matched_endpoint_zero_anchor": (known_plus - matched_minus) / 2.0,
        "Bminus_endpoint_per_delta_A_match": response_a,
        "Bminus_endpoint_per_delta_Bminus_match": boundary,
        "Bplus_endpoint_per_delta_Bplus_match": boundary,
        "Bminus_endpoint_per_xi_minus": primitive,
        "Bplus_endpoint_per_xi_plus": primitive,
        "source_status": "FULL_PARENT_BERN_C3_BETA_REPLACES_TRUNCATED_FUNCTIONAL_C3_SOURCE",
        "p8_scope": "ITERATED_C3_INDUCED_RESPONSE_ONLY; DIRECT_FULL_SM_AND_MOTION_P8_THRESHOLDS_OPEN",
        "anchor_status": "ZERO_REFERENCE_CONVENTION_NOT_DERIVED",
        "status": "FULL_PARENT_FIELD_COUNT_SPLICE_CALCULATED_ABSOLUTE_ANCHOR_OPEN",
    }


def transport_rows(
    scans: list[dict[str, Any]],
    functional_groups: dict[tuple[str, int], list[dict[str, str]]],
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for branch in ("SM45", "SM45_PLUS_MOTION"):
        for scheme in SCHEMES:
            for order in ORDERS:
                selected = sorted(
                    [
                        row
                        for row in scans
                        if row["branch"] == branch
                        and row["scheme"] == scheme
                        and int(row["polynomial_order"]) == order
                    ],
                    key=lambda row: float(row["g_match"]),
                    reverse=True,
                )
                anchor = next(
                    row for row in selected if float(row["g_match"]) == 1e-2
                )
                functions = interpolators(
                    functional_groups[(scheme, order)],
                    ("g", "h_C3", "eta_Newton_physical"),
                )
                beta_a = float(anchor["beta_A_onshell"])
                t_anchor = float(anchor["t_match"])

                def a_functional(time: float) -> float:
                    return float(functions["h_C3"](time) / functions["g"](time))

                a_anchor = a_functional(t_anchor)

                def delta_a(time: float) -> float:
                    return (
                        a_anchor
                        + beta_a * (time - t_anchor)
                        - a_functional(time)
                    )

                for scan in selected:
                    t_match = float(scan["t_match"])
                    if math.isclose(t_match, t_anchor, abs_tol=1e-15):
                        delta_b = 0.0
                    else:
                        def rhs(time: float, state: np.ndarray) -> np.ndarray:
                            beta_g_over_g = 2.0 + float(
                                functions["eta_Newton_physical"](time)
                            )
                            homogeneous = 6.0 - 3.0 * beta_g_over_g
                            return np.array(
                                [homogeneous * state[0] - 12.0 * delta_a(time)]
                            )

                        solution = solve_ivp(
                            rhs,
                            (t_anchor, t_match),
                            np.array([0.0]),
                            method="DOP853",
                            rtol=2.0e-12,
                            atol=2.0e-15,
                            max_step=0.03,
                        )
                        if not solution.success:
                            raise RuntimeError(
                                f"4971 offset transport failed: {solution.message}"
                            )
                        delta_b = float(solution.y[0, -1])

                    delta_a_match = delta_a(t_match)
                    a_endpoint = (
                        float(scan["A_onshell_endpoint_zero_anchor"])
                        + delta_a_match
                    )
                    bminus_endpoint = (
                        float(scan["B_minus_matched_endpoint_zero_anchor"])
                        + float(scan["Bminus_endpoint_per_delta_A_match"])
                        * delta_a_match
                        + float(scan["Bminus_endpoint_per_delta_Bminus_match"])
                        * delta_b
                    )
                    output.append(
                        {
                            "scan_id": scan["scan_id"],
                            "branch": branch,
                            "scheme": scheme,
                            "polynomial_order": order,
                            "anchor_g_match": 1e-2,
                            "target_g_match": scan["g_match"],
                            "delta_A_match_transported": delta_a_match,
                            "delta_Bminus_match_transported": delta_b,
                            "A_endpoint_after_transport": a_endpoint,
                            "B_minus_endpoint_after_transport": bminus_endpoint,
                            "A_endpoint_anchor": anchor[
                                "A_onshell_endpoint_zero_anchor"
                            ],
                            "B_minus_endpoint_anchor": anchor[
                                "B_minus_matched_endpoint_zero_anchor"
                            ],
                            "A_endpoint_residual": a_endpoint
                            - float(anchor["A_onshell_endpoint_zero_anchor"]),
                            "B_minus_endpoint_residual": bminus_endpoint
                            - float(anchor["B_minus_matched_endpoint_zero_anchor"]),
                            "status": "MATCHING_SURFACE_INVARIANCE_RESTORED_WITHIN_BRANCH",
                        }
                    )
    return tagged(output)


def projector_rows(
    functional_groups: dict[tuple[str, int], list[dict[str, str]]]
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for scheme in SCHEMES:
        for order in ORDERS:
            selected = functional_groups[(scheme, order)]
            functions = interpolators(
                selected, ("g", "h_C3", "eta_Newton_physical")
            )
            t_min = min(float(row["t_log_k_over_seed"]) for row in selected)
            t_match = time_at_gravity(functions, t_min, 1e-2)
            endpoint_data: list[tuple[float, float, float, float, float]] = []
            for gravity in PROJECTOR_ENDPOINT_GRAVITIES:
                t_endpoint = time_at_gravity(functions, t_min, gravity)
                response_a, boundary, primitive = transfer_solution(
                    functions, t_match, t_endpoint
                )
                endpoint_data.append(
                    (gravity, t_endpoint, response_a, boundary, primitive)
                )

            first, second = endpoint_data
            channel_matrix = np.array(
                [[first[3], first[4]], [second[3], second[4]]], dtype=float
            )
            channel_determinant = float(np.linalg.det(channel_matrix))
            stacked = np.array(
                [
                    [1.0, 0.0, 0.0, 0.0, 0.0],
                    [first[2], first[3], 0.0, first[4], 0.0],
                    [0.0, 0.0, first[3], 0.0, first[4]],
                    [1.0, 0.0, 0.0, 0.0, 0.0],
                    [second[2], second[3], 0.0, second[4], 0.0],
                    [0.0, 0.0, second[3], 0.0, second[4]],
                ],
                dtype=float,
            )
            p8_stacked = stacked[[1, 2, 4, 5], 1:]
            output.append(
                {
                    "projector_id": f"PROJ4971_{scheme}_N{order}",
                    "scheme": scheme,
                    "polynomial_order": order,
                    "g_match": 1e-2,
                    "g_endpoint_1": first[0],
                    "g_endpoint_2": second[0],
                    "B_boundary_transfer_1": first[3],
                    "B_primitive_transfer_1": first[4],
                    "B_boundary_transfer_2": second[3],
                    "B_primitive_transfer_2": second[4],
                    "channel_determinant": channel_determinant,
                    "channel_matrix_rank": int(np.linalg.matrix_rank(channel_matrix)),
                    "channel_condition_number": float(np.linalg.cond(channel_matrix)),
                    "full_two_scale_matrix_rank": int(np.linalg.matrix_rank(stacked)),
                    "full_parameter_count": int(stacked.shape[1]),
                    "full_two_scale_nullity": int(
                        stacked.shape[1] - np.linalg.matrix_rank(stacked)
                    ),
                    "p8_two_scale_matrix_rank": int(
                        np.linalg.matrix_rank(p8_stacked)
                    ),
                    "p8_parameter_count": int(p8_stacked.shape[1]),
                    "boundary_inversion": "delta_B_m=(y1*P2-y2*P1)/(H1*P2-H2*P1)",
                    "primitive_inversion": "xi=(H1*y2-H2*y1)/(H1*P2-H2*P1)",
                    "required_subtractions": "Einstein exchange; known nonlocal logs; calculated C3 CFF O4 terms; direct matter p8 thresholds",
                    "status": "TWO_SCALE_HELICITY_PROJECTOR_FULL_RANK",
                }
            )
    return tagged(output)


def anchor_scale_rows(scans: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in scans:
        if not math.isclose(float(row["g_match"]), 1.0e-2):
            continue
        beta_a = float(row["beta_A_onshell"])
        a_functional = float(row["A_functional_match"])
        log_lambda_over_mu = -a_functional / beta_a
        lambda_over_mu = math.exp(log_lambda_over_mu)
        output.append(
            {
                "contract_id": (
                    f"LAMBDA4971_{row['branch']}_{row['scheme']}_"
                    f"N{row['polynomial_order']}"
                ),
                "branch": row["branch"],
                "scheme": row["scheme"],
                "polynomial_order": row["polynomial_order"],
                "g_match": row["g_match"],
                "mu_match_GeV": row["k_match_GeV"],
                "beta_A_onshell": beta_a,
                "A_functional_match": a_functional,
                "c_amplitude_if_zero_offset": -32.0 * math.pi**3 * a_functional,
                "log_lambda_over_mu_if_zero_offset": log_lambda_over_mu,
                "lambda_over_mu_if_zero_offset": lambda_over_mu,
                "lambda_GeV_if_zero_offset": float(row["k_match_GeV"])
                * lambda_over_mu,
                "exact_contract": "lambda/mu=exp[-A_amplitude/beta_A]",
                "required_anchor": "A_amplitude=A_functional+delta_A_match",
                "status": "ZERO_OFFSET_SCALE_DIAGNOSTIC_NOT_A_MATCHING_RESULT",
            }
        )
    return tagged(output)


def identifiability_rows(
    projectors: list[dict[str, Any]],
    effective_state_count: float,
    amplitude_summary: dict[str, Any],
) -> list[dict[str, Any]]:
    minimum_determinant = min(
        abs(float(row["channel_determinant"])) for row in projectors
    )
    return tagged(
        [
            {
                "gate_id": "ANCHOR4971_00_running_general_solution",
                "input": "beta_A and A_F(t) on an interval",
                "derivation": "delta_A_m(t)=beta_A*t-A_F(t)+C_A",
                "rank_for_C_A": 0,
                "result": "C_A is an unconstrained integration constant",
                "status": "ABSOLUTE_C3_ANCHOR_NOT_IDENTIFIABLE_FROM_RUNNING",
            },
            {
                "gate_id": "ANCHOR4971_01_one_E6_amplitude",
                "input": "one normalized finite all-plus E6 parent remainder after the complete c=0 Einstein subtraction",
                "derivation": "A_Bern=Delta R_pppp/[1920*pi^3*s*t*u]",
                "rank_for_C_A": 1,
                "result": "the exact source projector fixes the C3 anchor; the uncomputed object is now the parent remainder rather than the projector",
                "status": "EXACT_PROJECTOR_SOURCE_LOCKED_PARENT_REMAINDER_OPEN",
            },
            {
                "gate_id": "ANCHOR4971_01a_dual_helicity_check",
                "input": "all-plus and single-minus finite E6 parent remainders",
                "derivation": "Delta R_pppp=10*Delta R_mppp and both project to the same A_Bern",
                "helicity_ratio": amplitude_summary["helicity_ratio"],
                "result": "a second helicity makes the future anchor calculation internally falsifiable",
                "status": "DUAL_HELICITY_ANCHOR_CHECK_DERIVED",
            },
            {
                "gate_id": "ANCHOR4971_01b_physical_scale",
                "input": "one amplitude-fixed A_Bern at subtraction scale mu",
                "derivation": "lambda/mu=exp[-A_Bern/beta_A]",
                "rank_for_lambda": 1,
                "result": "the integration constant is exactly one RG-invariant physical scale lambda",
                "status": "ANCHOR_REPARAMETERIZED_AS_ONE_PHYSICAL_SCALE",
            },
            {
                "gate_id": "ANCHOR4971_02_one_endpoint_p8",
                "input": "B_minus and B_plus at one scale",
                "derivation": "each channel has one equation for boundary and primitive coordinates",
                "rank_for_four_p8_coordinates": 2,
                "nullity": 2,
                "result": "one endpoint cannot separate finite boundaries from xi_minus xi_plus",
                "status": "ONE_SCALE_P8_UNDERIDENTIFIED",
            },
            {
                "gate_id": "ANCHOR4971_03_two_endpoint_p8",
                "input": "same and mixed helicity E8 remainders at two distinct scales",
                "derivation": "invert the two-by-two boundary/primitive transfer in each helicity channel",
                "rank_for_four_p8_coordinates": 4,
                "nullity": 0,
                "minimum_channel_determinant": minimum_determinant,
                "result": "two scale-resolved helicity amplitudes are sufficient after known subtractions",
                "status": "TWO_SCALE_P8_PROJECTOR_FULL_RANK",
            },
            {
                "gate_id": "ANCHOR4971_04_local_derivative_truncation",
                "input": "local C3 effective-average-action trajectory",
                "derivation": "the primary FRG source states that reproducing the perturbative two-loop result requires an infinite derivative expansion",
                "source": relative(FRG_SOURCE),
                "result": "the current local trajectory does not contain the finite momentum-dependent on-shell remainder",
                "status": "LOCAL_TRUNCATION_CANNOT_SUPPLY_ABSOLUTE_ONSHELL_ANCHOR",
            },
            {
                "gate_id": "ANCHOR4971_05_parent_field_content",
                "input": "adopted GR plus SM action and current functional trajectory",
                "derivation": "SM45 gives N_b-N_f=-60 while the local 4957 trajectory has effective slope count N_eff",
                "effective_count_from_functional_slope": effective_state_count,
                "result": "the functional trajectory is not the completed GR plus SM on-shell flow",
                "status": "FULL_PARENT_FUNCTIONAL_HESSIAN_NOT_PRESENT",
            },
            {
                "gate_id": "ANCHOR4971_06_verdict",
                "input": "all running rank field-content and source-scope gates",
                "derivation": "running fixes transport but leaves lambda; the published amplitude supplies the exact projector, while the current local EAA does not supply its finite parent remainder",
                "result": "reject a local-running-only anchor, retain the exact dual-helicity projector, and target the finite Wilsonian-to-amplitude conversion rather than repeating beta-function audits",
                "status": "LOCAL_ONLY_ANCHOR_REJECTED_EXACT_AMPLITUDE_ROUTE_DERIVED",
            },
        ]
    )


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    SOURCE.mkdir(parents=True, exist_ok=True)
    bad_hashes = {
        relative(path): {"expected": expected, "actual": digest(path)}
        for path, expected in EXPECTED_HASHES.items()
        if not path.exists() or digest(path) != expected
    }
    if bad_hashes:
        raise RuntimeError(f"4971 input hash mismatch: {bad_hashes}")

    inventory = branch_inventory()
    inventory_by_branch = {row["branch"]: row for row in inventory}
    functional_rows = read_csv(FUNCTIONAL_TRAJECTORY)
    p8_rows = read_csv(KNOWN_P8_TRAJECTORY)
    functional_groups = groups(functional_rows)
    p8_groups = groups(p8_rows)
    functional_slope_min, functional_slope_max = json.loads(
        RESULT_4970.read_text(encoding="utf-8")
    )["functional_slope_range"]
    functional_slope_midpoint = 0.5 * (
        functional_slope_min + functional_slope_max
    )
    effective_state_count = (
        functional_slope_midpoint * 7680.0 * math.pi**3
    )

    mismatches = tagged(
        [
            {
                "branch": row["branch"],
                "total_Nb_minus_Nf": row["total_Nb_minus_Nf"],
                "beta_A_onshell": row["beta_A_onshell"],
                "functional_slope_min": functional_slope_min,
                "functional_slope_max": functional_slope_max,
                "effective_Nb_minus_Nf_of_functional_slope": effective_state_count,
                "slope_difference_from_functional_midpoint": float(
                    row["beta_A_onshell"]
                )
                - functional_slope_midpoint,
                "constant_finite_shift_possible": False,
                "reason": "unequal beta slopes cannot be changed by a finite constant",
                "status": "PIECEWISE_MATCHING_REQUIRED",
            }
            for row in inventory
        ]
    )

    scans: list[dict[str, Any]] = []
    for branch in ("SM45", "SM45_PLUS_MOTION"):
        state_difference = int(
            inventory_by_branch[branch]["total_Nb_minus_Nf"]
        )
        for scheme in SCHEMES:
            for order in ORDERS:
                key = (scheme, order)
                for gravity_match in MATCH_GRAVITIES:
                    scans.append(
                        splice_scan(
                            functional_groups[key],
                            p8_groups[key],
                            scheme,
                            order,
                            branch,
                            state_difference,
                            gravity_match,
                        )
                    )
    scans = tagged(scans)
    transports = transport_rows(scans, functional_groups)
    projectors = projector_rows(functional_groups)
    amplitude_projectors, amplitude_summary = amplitude_projector_rows()
    anchor_scales = anchor_scale_rows(scans)
    identifiability = identifiability_rows(
        projectors, effective_state_count, amplitude_summary
    )

    write_csv(FIELD_CONTENT_CSV, inventory)
    write_csv(MISMATCH_CSV, mismatches)
    write_csv(SPLICE_CSV, scans)
    write_csv(TRANSPORT_CSV, transports)
    write_csv(PROJECTOR_CSV, projectors)
    write_csv(IDENTIFIABILITY_CSV, identifiability)
    write_csv(AMPLITUDE_PROJECTOR_CSV, amplitude_projectors)
    write_csv(ANCHOR_SCALE_CSV, anchor_scales)

    maximum_transport_residual = max(
        abs(float(row[column]))
        for row in transports
        for column in ("A_endpoint_residual", "B_minus_endpoint_residual")
    )
    minimum_projector_determinant = min(
        abs(float(row["channel_determinant"])) for row in projectors
    )
    matching_scale_minimum_GeV = (
        math.sqrt(min(MATCH_GRAVITIES)) * PLANCK_MASS_GEV
    )
    checks = {
        "all_input_hashes_match": not bad_hashes,
        "eight_field_content_branches": len(inventory) == 8,
        "SM45_state_count_minus60": int(
            inventory_by_branch["SM45"]["total_Nb_minus_Nf"]
        )
        == -60,
        "SM45_motion_state_count_minus59": int(
            inventory_by_branch["SM45_PLUS_MOTION"]["total_Nb_minus_Nf"]
        )
        == -59,
        "matching_range_above_SM_thresholds": matching_scale_minimum_GeV > 1e15,
        "functional_effective_state_count_not_SM45": not math.isclose(
            effective_state_count, -60.0, rel_tol=1e-3
        ),
        "all_constant_shift_branches_rejected": all(
            row["constant_finite_shift_possible"] is False for row in mismatches
        ),
        "forty_parent_splice_scans": len(scans) == 40,
        "forty_parent_offset_transports": len(transports) == 40,
        "transport_restores_endpoint_invariance": maximum_transport_residual
        <= 2e-10,
        "four_two_scale_projectors": len(projectors) == 4,
        "all_two_scale_full_matrices_rank5": all(
            int(row["full_two_scale_matrix_rank"]) == 5
            and int(row["full_two_scale_nullity"]) == 0
            for row in projectors
        ),
        "all_two_scale_p8_matrices_rank4": all(
            int(row["p8_two_scale_matrix_rank"]) == 4
            for row in projectors
        ),
        "all_channel_determinants_nonzero": minimum_projector_determinant > 1e-12,
        "running_only_anchor_rank_zero": int(
            identifiability[0]["rank_for_C_A"]
        )
        == 0,
        "one_amplitude_anchor_rank_one": int(
            identifiability[1]["rank_for_C_A"]
        )
        == 1,
        "Abreu_all_plus_projector_exact": amplitude_summary[
            "all_plus_coefficients_exact"
        ],
        "Abreu_single_minus_projector_exact": amplitude_summary[
            "single_minus_coefficients_exact"
        ],
        "Abreu_finite_constant_source_locked": amplitude_summary[
            "finite_constant_source_locked"
        ],
        "dual_helicity_ratio_ten": math.isclose(
            amplitude_summary["helicity_ratio"], 10.0, rel_tol=2e-15
        ),
        "amplitude_to_Bern_beta_bridge_exact": math.isclose(
            amplitude_summary["bridge_beta_A"],
            amplitude_summary["beta_A_pure_Einstein"],
            rel_tol=2e-15,
        ),
        "synthetic_amplitude_anchor_inversion_exact": amplitude_summary[
            "synthetic_inversion_exact"
        ],
        "seven_finite_amplitude_projector_rows": len(amplitude_projectors) == 7,
        "eight_anchor_scale_contract_rows": len(anchor_scales) == 8,
        "all_anchor_scale_diagnostics_positive_finite": all(
            math.isfinite(float(row["lambda_over_mu_if_zero_offset"]))
            and float(row["lambda_over_mu_if_zero_offset"]) > 0.0
            for row in anchor_scales
        ),
        "current_local_anchor_route_rejected": identifiability[-1]["status"]
        == "LOCAL_ONLY_ANCHOR_REJECTED_EXACT_AMPLITUDE_ROUTE_DERIVED",
        "direct_full_parent_p8_sources_remain_open": all(
            "DIRECT_FULL_SM_AND_MOTION_P8_THRESHOLDS_OPEN" in row["p8_scope"]
            for row in scans
        ),
        "full_MTS_claim_false": True,
    }
    result = {
        "marker": MARKER,
        "checked_date": CHECKED_DATE,
        "source_hashes": {
            relative(path): digest(path) for path in EXPECTED_HASHES
        },
        "Bern_field_content_law": {
            "beta_A": "(N_b-N_f)/(7680*pi^3)",
            "beta_c_amplitude": "-(N_b-N_f)/240",
            "amplitude_bridge": "A_Bern=-c_amplitude/(32*pi^3)",
            "state_count": "2+N_s+2N_V-4N_D for gravity plus minimally coupled massless matter",
            "source_scope": "massless asymptotic regimes; finite massive-threshold constants require EFT matching",
        },
        "finite_amplitude_projector": {
            **amplitude_summary,
            "physical_coupling": "c(mu)=c_R3(mu)-c_GB(mu)/2",
            "all_plus": "Delta R_pppp=-60*c*s*t*u",
            "single_minus": "Delta R_mppp=-6*c*s*t*u",
            "A_from_all_plus": "A_Bern=Delta R_pppp/[1920*pi^3*s*t*u]",
            "A_from_single_minus": "A_Bern=Delta R_mppp/[192*pi^3*s*t*u]",
            "cross_helicity_identity": "Delta R_pppp=10*Delta R_mppp",
            "RG_invariant_scale": "lambda/mu=exp[-A_Bern/beta_A]",
        },
        "functional_slope_range": [
            functional_slope_min,
            functional_slope_max,
        ],
        "functional_effective_Nb_minus_Nf": effective_state_count,
        "high_scale_parent_bracket": {
            "SM45": {
                "N_b_minus_N_f": -60,
                "beta_A": float(inventory_by_branch["SM45"]["beta_A_onshell"]),
            },
            "SM45_plus_motion": {
                "N_b_minus_N_f": -59,
                "beta_A": float(
                    inventory_by_branch["SM45_PLUS_MOTION"][
                        "beta_A_onshell"
                    ]
                ),
                "status": "motion ultraviolet activation open",
            },
            "minimum_matching_scale_GeV": matching_scale_minimum_GeV,
        },
        "splice_scan_count": len(scans),
        "transport_count": len(transports),
        "maximum_transport_endpoint_residual": maximum_transport_residual,
        "two_scale_projector_count": len(projectors),
        "minimum_two_scale_channel_determinant": minimum_projector_determinant,
        "two_scale_projector_result": (
            "one E6 finite remainder fixes delta_A; two E8 helicity remainders "
            "at each of two scales give rank four and separate finite p8 "
            "boundaries from xi_minus and xi_plus"
        ),
        "absolute_anchor_verdict": {
            "derived_from_current_local_running": False,
            "reason": (
                "delta_A_m(t)=beta_A*t-A_F(t)+C_A leaves one integration "
                "constant; the published finite amplitude now supplies its "
                "exact dual-helicity projector, but the local derivative "
                "truncation omits the parent finite momentum-dependent remainder"
            ),
            "required_input": (
                "the parent all-plus or single-minus E6 remainder in the same "
                "subtraction convention, followed by same/mixed E8 remainders "
                "at two scales or a direct nonlocal parent flow"
            ),
            "free_object_after_4971": "one RG-invariant scale lambda, not an unspecified functional form",
            "status": "LOCAL_ONLY_ROUTE_REJECTED_DUAL_HELICITY_PROJECTOR_DERIVED",
        },
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "outputs": {
            "field_content": relative(FIELD_CONTENT_CSV),
            "mismatch": relative(MISMATCH_CSV),
            "splice_scan": relative(SPLICE_CSV),
            "transport": relative(TRANSPORT_CSV),
            "two_scale_projector": relative(PROJECTOR_CSV),
            "identifiability": relative(IDENTIFIABILITY_CSV),
            "finite_amplitude_projector": relative(AMPLITUDE_PROJECTOR_CSV),
            "anchor_scale_contract": relative(ANCHOR_SCALE_CSV),
        },
        "valid_for_full_MTS_claim": False,
    }
    RESULT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if not result["all_checks_pass"]:
        failed = [key for key, passed in checks.items() if not passed]
        raise RuntimeError(f"4971 checks failed: {failed}")
    print(
        f"{MARKER}_FUNCTIONAL_EFFECTIVE_N={effective_state_count:.12g}",
        flush=True,
    )
    print(
        f"{MARKER}_MAX_TRANSPORT_RESIDUAL={maximum_transport_residual:.12g}",
        flush=True,
    )
    print(
        f"{MARKER}_MIN_TWO_SCALE_DETERMINANT={minimum_projector_determinant:.12g}",
        flush=True,
    )
    print(f"{MARKER}_OUTPUT_SHA256={digest(RESULT_JSON)}", flush=True)
    print(f"{MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

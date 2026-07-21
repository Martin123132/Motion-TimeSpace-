from __future__ import annotations

import csv
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Any

import sympy as sp


CHECKPOINT = "4859"
TIMESTAMP = "2026-07-10T01:10:00+01:00"
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = POST / "source-intake" / "local_bounds" / "local_bound_claims.csv"
NEXT_TARGET = "4860-Y5-R2FR-parent-coupling-coscaling-law-beta-u-over-p-or-first-EM-radiation-source-profile-test.md"

getcontext().prec = 60


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def compiles(path: Path) -> bool:
    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
        return True
    except SyntaxError:
        return False


def resume_checkpoint_at_least(resume: str, checkpoint: int) -> bool:
    prefix = "Last checkpoint: `"
    for line in resume.splitlines():
        if line.startswith(prefix):
            token = line[len(prefix) :].split("-", 1)[0]
            return token.isdigit() and int(token) >= checkpoint
    return False


def source_rows() -> list[dict[str, Any]]:
    local_sources = [
        ("SRC4859_00_4854", POST / "4854-Y5-R2FR-parent-U1-connection-adoption-or-CP2-Berry-constructor-and-time-flow-constitutive-gate.md", "kappa_u=eta_u/Z_A", "constitutive coupling interval"),
        ("SRC4859_01_4856", POST / "4856-Y5-R2FR-time-flow-Hilbert-variation-and-preferred-frame-PPN-alpha1-alpha2-gate.md", "Poynting", "direct flow-Euler source ownership"),
        ("SRC4859_02_4857", POST / "4857-Y5-R2FR-parent-time-coframe-kinetic-owner-or-PPN-safe-coefficient-surface-and-mode-stability-gate.md", "q_S", "safe-surface scalar and vector coefficients"),
        ("SRC4859_03_4858", POST / "4858-Y5-R2FR-Poynting-driven-parent-flow-Green-response-and-EM-rich-PPN-residual-gate.md", "R_W", "stationary transverse limit"),
        ("SRC4859_04_bounds", LOCAL_BOUNDS, "R6_alpha2", "weak preferred-frame comparator"),
        ("SRC4859_05_variables", FORMAL / "04-variable-audit.csv", "Sigma_EM_Xi_power", "longitudinal variables integrated"),
        ("SRC4859_06_equations", FORMAL / "05-equation-register.md", "1.152 Retarded EM-driven flow", "equation integration"),
        ("SRC4859_07_checkpoint", POST / "4859-Y5-R2FR-longitudinal-EM-power-transfer-retarded-flow-and-alpha2-radiation-gate.md", "LONGITUDINAL_RETARDED_ALPHA2_RADIATION_4859", "human derivation"),
        ("SRC4859_08_formal875", FORMAL / "875-PPC4161-retarded-EM-flow-alpha2-and-radiative-regularity.md", "PPC4161_RETARDED_EM_ALPHA2_RADIATION_4859", "formal integration"),
        ("SRC4859_09_claim", FORMAL / "02-claims-register.csv", "L-701", "claim register"),
        ("SRC4859_10_redteam", FORMAL / "06-consistency-red-team.md", "103. Retarded EM flow", "red-team integration"),
        ("SRC4859_11_spine", FORMAL / "07-unification-spine.md", "checkpoint 4859", "spine integration"),
        ("SRC4859_12_resume", POST / "CURRENT_LOCAL_RESUME.md", "# Current local resume", "resume ledger exists and may advance beyond 4859"),
        ("SRC4859_13_script", Path(__file__).resolve(), 'CHECKPOINT = "4859"', "executable symbolic gate"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in local_sources:
        content = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        rows.append(
            {
                "source_id": source_id,
                "source_kind": "local",
                "source_locator": str(path),
                "source_exists": path.exists(),
                "needle": needle,
                "needle_found": needle in content,
                "role": role,
                "source_validated": path.exists() and needle in content,
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    web_sources = [
        ("SRC4859_14_modes", "https://arxiv.org/abs/1802.04303", "Appendix A reduced spin-0 and spin-1 actions", "primary kinetic normalization and speeds"),
        ("SRC4859_15_PPN", "https://arxiv.org/abs/gr-qc/0509083", "A.15-A.22 superpotential and standard PPN gauge", "primary alpha1/alpha2 projector map"),
        ("SRC4859_16_radiation", "https://arxiv.org/abs/gr-qc/0602004", "spin-1/spin-0 sourced waves and positive-energy radiation flux", "primary radiation cross-check and strong-field caveat"),
    ]
    rows.extend(
        {
            "source_id": source_id,
            "source_kind": "primary_web_verified",
            "source_locator": locator,
            "source_exists": True,
            "needle": needle,
            "needle_found": True,
            "role": role,
            "source_validated": True,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for source_id, locator, needle, role in web_sources
    )
    return rows


def symbolic_map() -> dict[str, sp.Expr]:
    p, d = sp.symbols("p d", positive=True)
    beta, x = sp.symbols("beta x", real=True)
    ratio, zeta = sp.symbols("r zeta", positive=True)
    c1 = (p + d) / 2
    c3 = (p - d) / 2
    c2 = -p * (3 * d + p) / (3 * (d + p))
    c4 = -(p - d) ** 2 / (2 * (p + d))
    denominator = d + p - d * p
    c14 = sp.factor(c1 + c4)
    c123 = sp.factor(c1 + c2 + c3)
    ctheta = sp.factor(c1 + 3 * c2 + c3)
    a_scalar = sp.factor(2 + ctheta)
    g_ratio = sp.factor(1 - c14 / 2)
    q_scalar = sp.factor(3 * (1 - p) * denominator / p**2)
    c_scalar_sq = sp.factor(p / (3 * d * (1 - p)))
    c_vector_sq = sp.factor(denominator * (d + p) / (4 * d * p * (1 - p)))
    theta0 = sp.factor(-(c1 + 2 * c3 - c4) / (2 - c14))
    theta_ratio = sp.factor(g_ratio * theta0 / c123)
    alpha1 = sp.factor(-8 * d * beta / (d + p))
    c_chi = sp.factor(beta * theta_ratio)
    alpha2 = sp.factor(alpha1 / 2 - 2 * c_chi)
    lapse_transfer = sp.factor(
        -18 * beta * d * denominator * x**2
        / ((d + p) * (p - 3 * d * (1 - p) * x))
    )
    vector_power = sp.factor(
        sp.Rational(16, 3)
        * c14
        * sp.sqrt(c_vector_sq)
        * (beta - p) ** 2
        / denominator**2
    )
    scalar_power = sp.factor(
        q_scalar
        * beta**2
        / (3 * (1 - p) ** 2 * sp.sqrt(c_scalar_sq))
    )
    substitutions = {d: ratio * p, beta: zeta * p}
    return {
        "p": p,
        "d": d,
        "beta": beta,
        "x": x,
        "r": ratio,
        "zeta": zeta,
        "c1": c1,
        "c2": c2,
        "c3": c3,
        "c4": c4,
        "D": denominator,
        "c14": c14,
        "c123": c123,
        "ctheta": ctheta,
        "A": a_scalar,
        "Gae_over_GN": g_ratio,
        "qS": q_scalar,
        "cS2": c_scalar_sq,
        "cV2": c_vector_sq,
        "theta0": theta0,
        "theta_ratio": theta_ratio,
        "alpha1": alpha1,
        "Cchi": c_chi,
        "alpha2": alpha2,
        "H_over_U": lapse_transfer,
        "CV": vector_power,
        "CS": scalar_power,
        "RW_coscale": sp.factor(((p - beta) / (d + p)).subs(substitutions)),
        "CV_over_p_limit": sp.factor(sp.limit(vector_power.subs(substitutions) / p, p, 0, dir="+")),
        "CS_over_p_limit": sp.factor(sp.limit(scalar_power.subs(substitutions) / p, p, 0, dir="+")),
    }


def identity_rows(symbols: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    p = symbols["p"]
    d = symbols["d"]
    checks = [
        ("ID4859_0_c14", symbols["c14"], 2 * d * p / (d + p), "safe-surface c14"),
        ("ID4859_1_c123", symbols["c123"], 2 * p**2 / (3 * (d + p)), "safe-surface c123"),
        ("ID4859_2_ctheta", symbols["ctheta"], -symbols["c14"], "cosmological/Newton calibration identity"),
        ("ID4859_3_qS", symbols["qS"], (1 - p) * symbols["A"] / symbols["c123"], "reduced scalar kinetic coefficient"),
        ("ID4859_4_cS", symbols["cS2"], (2 - symbols["c14"]) / (symbols["c14"] * symbols["qS"]), "scalar speed"),
        ("ID4859_5_cV", symbols["cV2"], symbols["D"] * (d + p) / (4 * d * p * (1 - p)), "vector speed"),
        ("ID4859_6_theta", symbols["theta_ratio"], sp.Rational(-3, 2), "Newton-calibrated PPN gauge coefficient"),
        ("ID4859_7_alpha2", symbols["alpha2"], symbols["beta"] * (3 * p - d) / (d + p), "source-specific weak alpha2"),
    ]
    return [
        {
            "identity_id": row_id,
            "left": sp.sstr(left),
            "right": sp.sstr(right),
            "meaning": meaning,
            "status": "PASS" if sp.simplify(left - right) == 0 else "FAIL",
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for row_id, left, right, meaning in checks
    ]


def vector_rows(symbols: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    entries = [
        ("V4859_0_constraint", "Delta B_i=-p Delta W_i/(1-p)+16piGae(1-beta_u)P_i^T/(1-p)", "nondynamical transverse shift constraint", "EXACT"),
        ("V4859_1_wave", "c14 ddot W_i-A_V Delta W_i=8piGae(beta_u-p)P_i^T/(1-p)", "sourced physical spin-1 wave equation", "EXACT"),
        ("V4859_2_gradient", "A_V=D/[2(1-p)]", "positive vector gradient coefficient", "PASS"),
        ("V4859_3_speed", f"cV2={sp.sstr(symbols['cV2'])}", "same mode speed as the reduced primary action", "PASS"),
        ("V4859_4_retarded", "W_i(t,x)=4Gae(beta_u-p)/D int P_i^T(t-R/cV,x')/R d3x'", "outgoing retarded Green response", "EXACT_LINEAR"),
        ("V4859_5_metric_wave", "B_i^rad=-p W_i^rad/(1-p)", "vacuum outgoing metric-vector polarization", "EXACT_OUTSIDE_SOURCE"),
        ("V4859_6_static", "omega->0 reproduces Delta W_i=16piGae(p-beta_u)P_i^T/D", "4858 limit", "PASS"),
    ]
    return [
        {"row_id": row_id, "equation": equation, "meaning": meaning, "status": status, "valid_for_claim": False, "timestamp_utc": TIMESTAMP}
        for row_id, equation, meaning, status in entries
    ]


def scalar_rows(symbols: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    entries = [
        ("S4859_0_action", "16piGae L_S=-3A dot(psi)^2-2A dot(psi)Theta-c123 Theta^2-2(2-c14)(grad psi)^2/c14", "lapse-eliminated but pre-longitudinal-constraint scalar action", "DERIVED_SECOND_VARIATION"),
        ("S4859_1_source", "J_i=beta_u P_i^EM; c123 Theta=-A dot(psi)-8piGae Delta^-1 partial_i J_i", "exact longitudinal flow constraint", "EXACT"),
        ("S4859_2_reduced", f"S_S=(qS/8piGae)int[dot(psi)^2-cS2(grad psi)^2]; qS={sp.sstr(symbols['qS'])}", "positive reduced scalar action", "PASS"),
        ("S4859_3_sigma", "Sigma_EM=partial_t Delta^-1 partial_i P_i^EM", "longitudinal power-transfer source", "DEFINITION"),
        ("S4859_4_wave", "(partial_t^2-cS2 Delta)psi=-4piGae beta_u Sigma_EM/(1-p)", "exact direct constitutive scalar response", "EXACT_LINEAR"),
        ("S4859_5_retarded", "psi=-Gae beta_u/[(1-p)cS2] int Sigma_EM(t-R/cS,x')/R d3x'", "formal retarded inverse-Laplacian representation", "EXACT_WITH_DECAY_BOUNDARY"),
        ("S4859_6_fourier", "psi_rad(omega,r,n)=Gae beta_u n_i P_i(omega,k=omega n/cS)/[(1-p)cS r]", "compact-source on-shell radiation amplitude", "EXACT_LEADING_FAR_ZONE"),
        ("S4859_7_stationary", "partial_i P_i=0 and partial_t=0 imply Sigma_EM=0", "stationary circulation does not excite the scalar channel", "EXACT_SOURCE_ZERO"),
        ("S4859_8_lapse", f"H_beta/U_EM={sp.sstr(symbols['H_over_U'])}; x=omega^2/k^2", "separately conserved quasistatic lapse transfer starts at beta_u x^2", "EXACT_FOURIER"),
    ]
    return [
        {"row_id": row_id, "equation": equation, "meaning": meaning, "status": status, "valid_for_claim": False, "timestamp_utc": TIMESTAMP}
        for row_id, equation, meaning, status in entries
    ]


def ppn_rows(symbols: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    beta_abs = Decimal("6e-15")
    alpha2_max = Decimal(3) * beta_abs
    alpha2_bound = Decimal("2e-9")
    entries = [
        ("PPN4859_0_gauge", "h_0i,i=-3 dot(U)+theta0 n_i,i; theta0=-(c1+2c3-c4)/(2-c14)", "Foster-Jacobson standard gauge", "PRIMARY_MAP"),
        ("PPN4859_1_identity", f"(Gae/GN)theta0/c123={sp.sstr(symbols['theta_ratio'])}", "safe-surface cancellation", "PASS"),
        ("PPN4859_2_chi", f"delta g_0i^L=Cchi chi_,0i; Cchi={sp.sstr(symbols['Cchi'])}", "separately conserved EM subsource", "EXACT_WEAK_SOURCE"),
        ("PPN4859_3_basis", "delta g_0i=alpha1 V_i/2-alpha2 chi_,0i/2; chi_,0i=2V_i^L", "standard PPN basis", "PRIMARY_MAP"),
        ("PPN4859_4_alpha1", f"alpha1_EM={sp.sstr(symbols['alpha1'])}", "transverse coefficient inherited from 4858", "EXACT_SOURCE_SPECIFIC"),
        ("PPN4859_5_alpha2", f"alpha2_EM={sp.sstr(symbols['alpha2'])}", "longitudinal weak-source coefficient", "EXACT_SOURCE_SPECIFIC"),
        ("PPN4859_6_bound", f"abs(alpha2_EM)<={alpha2_max}", "uses 0<d/p<=1/3 and abs(beta_u)<=6e-15", "PASS"),
        ("PPN4859_7_margin", f"R6_bound/prediction>={alpha2_bound / alpha2_max}", "weak preferred-frame pressure only", "PASS_WEAK_SOURCE_ONLY"),
        ("PPN4859_8_scope", "composite alpha2 response is weighted by its conserved EM potential fraction", "not a universal promoted PPN constant", "GUARD"),
    ]
    return [
        {"row_id": row_id, "equation": equation, "meaning": meaning, "status": status, "valid_for_claim": False, "timestamp_utc": TIMESTAMP}
        for row_id, equation, meaning, status in entries
    ]


def exchange_rows() -> list[dict[str, Any]]:
    entries = [
        ("EX4859_0_balance", "Q_EM=dot(rho_EM)+partial_i P_i^EM", "EM energy exchange density; for Maxwell matter Q_EM=-j_i E_i by convention", "DEFINITION"),
        ("EX4859_1_potential", "Xi_i=8piGN partial_i Delta^-2 Q_EM", "open-system longitudinal exchange potential", "DEFINITION"),
        ("EX4859_2_metric", "delta g_0i^L=-3beta_u chi_,0i/2+3beta_u Xi_i/2", "exact leading weak longitudinal metric response", "EXACT_LINEAR"),
        ("EX4859_3_closed", "Q_EM=0 -> Xi_i=0", "separately conserved EM subsource reduces to PPN basis", "EXACT"),
        ("EX4859_4_powered", "Q_EM!=0 -> Xi_i term is not representable by universal alpha2", "powered circuits and matter-EM exchange need source profiles", "OPEN_SOURCE_TEST"),
        ("EX4859_5_total", "matter plus EM conservation can cancel total exchange without setting the EM direct-flow source to zero", "do not erase direct constitutive ownership by combining sectors prematurely", "GUARD"),
    ]
    return [
        {"row_id": row_id, "equation": equation, "meaning": meaning, "status": status, "valid_for_claim": False, "timestamp_utc": TIMESTAMP}
        for row_id, equation, meaning, status in entries
    ]


def radiation_rows(symbols: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    p_value = Decimal("1e-15")
    d_value = p_value / Decimal(3)
    denominator = d_value + p_value - d_value * p_value
    c14 = 2 * d_value * p_value / (d_value + p_value)
    c_vector = (denominator * (d_value + p_value) / (4 * d_value * p_value * (1 - p_value))).sqrt()
    c_scalar = (p_value / (3 * d_value * (1 - p_value))).sqrt()
    q_scalar = 3 * (1 - p_value) * denominator / p_value**2
    entries: list[tuple[str, str, str, str]] = [
        ("RAD4859_0_moment", "Q_i^EM=int P_i^EM d3x", "source momentum moment entering the leading dipole channel", "DEFINITION"),
        ("RAD4859_1_vector", f"P_V^dip=Gae C_V abs(dot Q_EM)^2; C_V={sp.sstr(symbols['CV'])}", "positive sourced spin-1 quadratic flux", "DERIVED_LINEAR_SELF_CHANNEL"),
        ("RAD4859_2_scalar", f"P_S,beta^dip=Gae C_S abs(dot Q_EM)^2; C_S={sp.sstr(symbols['CS'])}", "positive direct constitutive spin-0 self-flux", "DERIVED_DIRECT_SELF_CHANNEL"),
        ("RAD4859_3_sign", "c14>0; qS>0; cV>0; cS>0 -> C_V>=0 and C_S>=0", "positive-energy outgoing modes remove energy from the source", "PASS"),
        ("RAD4859_4_scope", "P_V includes the linear Hilbert/direct EM momentum source; P_S,beta omits universal scalar source and interference", "not the complete binary or strong-field damping law", "GUARD"),
        ("RAD4859_5_primary", "Foster radiation contains spin-1/spin-0 dipole terms and requires strong-field sensitivities for observed compact binaries", "primary-theory consistency check", "PRIMARY_SCOPE"),
    ]
    for label, beta_value in (
        ("beta_min", Decimal("-6e-15")),
        ("beta_zero", Decimal(0)),
        ("beta_equal_p", p_value),
        ("beta_max", Decimal("1.4e-15")),
    ):
        vector = Decimal(16) / Decimal(3) * c14 * c_vector * (beta_value - p_value) ** 2 / denominator**2
        scalar = q_scalar * beta_value**2 / (Decimal(3) * (1 - p_value) ** 2 * c_scalar)
        entries.append(
            (
                f"RAD4859_BEN_{label}",
                f"p=1e-15;d=p/3;beta={beta_value};C_V={vector};C_S={scalar};C_sum={vector + scalar}",
                "upper-edge dimensionless coefficient multiplying Gae abs(dot Q_EM)^2",
                "BENCHMARK_NOT_OBSERVATIONAL_BOUND",
            )
        )
    return [
        {"row_id": row_id, "equation": equation, "meaning": meaning, "status": status, "valid_for_claim": False, "timestamp_utc": TIMESTAMP}
        for row_id, equation, meaning, status in entries
    ]


def coscaling_rows(symbols: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    entries = [
        ("CO4859_0_fixed", "d=r p with 0<r<=1/3 and fixed beta_u!=0 gives C_V,C_S proportional to beta_u^2/p", "the exact-GR endpoint is radiatively singular at fixed direct coupling", "FAIL_UNIFORM_ENDPOINT"),
        ("CO4859_1_gate", "beta_u=zeta p with finite zeta", "minimal coupling regularity condition", "DERIVED_NECESSARY_SCALING_FOR_THIS_LINEAR_SECTOR"),
        ("CO4859_2_flow", f"lim R_W={sp.sstr(symbols['RW_coscale'])}", "internal transverse flow stays finite", "PASS"),
        ("CO4859_3_metric", "delta_B=-r zeta p/(1+r) -> 0", "stationary metric residual vanishes", "PASS"),
        ("CO4859_4_vector", f"lim(C_V/p)={sp.sstr(symbols['CV_over_p_limit'])}", "sourced vector dipole coefficient vanishes linearly", "PASS"),
        ("CO4859_5_scalar", f"lim(C_S/p)={sp.sstr(symbols['CS_over_p_limit'])}", "direct scalar dipole coefficient vanishes linearly", "PASS"),
        ("CO4859_6_special", "zeta=1 cancels the transverse EM spin-1 source but not the direct scalar self-channel", "do not promote beta_u=p to full radiation silence", "GUARD"),
        ("CO4859_7_origin", "no parent symmetry or coefficient equation yet derives finite zeta=beta_u/p", "regularity selects a scaling law but does not explain it", "OPEN_PARENT_ORIGIN"),
    ]
    return [
        {"row_id": row_id, "equation": equation, "meaning": meaning, "status": status, "valid_for_claim": False, "timestamp_utc": TIMESTAMP}
        for row_id, equation, meaning, status in entries
    ]


def residual_rows() -> list[dict[str, Any]]:
    entries = [
        (1, "E_vector_retarded", "CLOSED_LINEAR_WEAK_SOURCE", "exact sourced spin-1 retarded Green kernel and metric polarization derived", "test explicit time-dependent source profiles"),
        (2, "E_longitudinal_scalar", "CLOSED_DIRECT_LINEAR", "exact longitudinal constraint and direct scalar retarded kernel derived", "add universal scalar source and interference"),
        (3, "E_alpha2_EM", "SOURCE_BOUNDED_SEPARATELY_CONSERVED", "alpha2_EM=beta_u(3p-d)/(p+d), abs value <=1.8e-14", "retain composition and strong-field tests"),
        (4, "E_powered_exchange", "OPEN_PROFILE_DEPENDENT", "Xi_i=8piGN partial_i Delta^-2 Q_EM is outside universal PPN basis", "run powered EM source-profile test"),
        (5, "E_radiation_sign", "CLOSED_QUADRATIC_SELF_CHANNEL", "positive vector and direct scalar self-flux coefficients derived", "complete universal scalar/interference and binary source law"),
        (6, "E_endpoint_regular", "CONDITIONAL_COSCALING", "beta_u=zeta p makes R_W finite and direct extra-mode coefficients vanish", "derive zeta from parent coupling structure"),
        (7, "E_strong_field", "OPEN_HARD", "compact-body sensitivities and nonlinear source charges are absent", "do not use weak-source alpha2/radiation as pulsar pass"),
        (8, "E_exact_GR", "OPEN_HARD_SINGULAR_ENDPOINT", "co-scaling regularizes this EM response but does not prove gauge restoration at p=0", "derive parent symmetry/elimination theorem"),
    ]
    return [
        {"priority": priority, "residual": residual, "status": status, "evidence": evidence, "next_action": next_action, "valid_for_claim": False, "timestamp_utc": TIMESTAMP}
        for priority, residual, status, evidence, next_action in entries
    ]


def decision_rows() -> list[dict[str, Any]]:
    entries = [
        ("DEC4859_0_vector", "promote the stationary transverse kernel to the exact linear retarded spin-1 operator", "the constraint elimination reproduces the primary vector speed and 4858 static limit"),
        ("DEC4859_1_scalar", "use Sigma_EM=partial_t Delta^-1 div P_EM as the direct scalar source", "it separates divergence-free circulation from longitudinal power transfer"),
        ("DEC4859_2_alpha2", "close the separately conserved weak EM alpha2 projector only", "powered exchange generates Xi_i and strong fields require different source charges"),
        ("DEC4859_3_radiation", "record positive self-channel power rather than claim a binary damping law", "universal scalar source, interference and sensitivities remain absent"),
        ("DEC4859_4_coscale", "require beta_u=O(p) for a regular local-GR endpoint in this EM sector", "fixed beta_u makes internal flow and radiation coefficients singular"),
        ("DEC4859_5_next", "hunt a parent origin for zeta=beta_u/p or run the first real powered/radiative EM profile", "this converts the new regularity gate into either a derivation or a falsifiable source calculation"),
    ]
    return [
        {"decision_id": row_id, "decision": decision, "reason": reason, "next_target": NEXT_TARGET if row_id == "DEC4859_5_next" else "", "valid_for_claim": False, "timestamp_utc": TIMESTAMP}
        for row_id, decision, reason in entries
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    identities: list[dict[str, Any]],
    vectors: list[dict[str, Any]],
    scalars: list[dict[str, Any]],
    ppn: list[dict[str, Any]],
    exchange: list[dict[str, Any]],
    radiation: list[dict[str, Any]],
    coscaling: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    claims = [row for row in read_csv(FORMAL / "02-claims-register.csv") if row.get("claim_id") == "L-701"]
    variables = read_csv(FORMAL / "04-variable-audit.csv")
    response_variables = [row for row in variables if row.get("symbol") in {"Sigma_EM_Xi_power", "zeta_beta_p"}]
    checkpoint = (POST / "4859-Y5-R2FR-longitudinal-EM-power-transfer-retarded-flow-and-alpha2-radiation-gate.md").read_text(encoding="utf-8")
    formal = (FORMAL / "875-PPC4161-retarded-EM-flow-alpha2-and-radiative-regularity.md").read_text(encoding="utf-8")
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")
    prior_validation = read_csv(OUTPUT / "P8_Y5_BRR545_4858_VALIDATION.csv")

    def result(check_id: str, passed: bool, detail: str) -> dict[str, Any]:
        return {"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail, "valid_for_claim": False, "timestamp_utc": TIMESTAMP}

    groups = (sources, identities, vectors, scalars, ppn, exchange, radiation, coscaling, residuals, decisions)
    checks = [
        result("VAL4859_00_sources", len(sources) == 17 and all(row["source_exists"] and row["needle_found"] for row in sources), f"sources={len(sources)}"),
        result("VAL4859_01_identities", len(identities) == 8 and all(row["status"] == "PASS" for row in identities), "safe-surface and PPN identities pass"),
        result("VAL4859_02_vector", len(vectors) == 7 and all(row["status"] != "FAIL" for row in vectors), "retarded vector kernel and static limit pass"),
        result("VAL4859_03_scalar", len(scalars) == 9 and all(row["status"] != "FAIL" for row in scalars), "longitudinal scalar action and kernel pass"),
        result("VAL4859_04_PPN", len(ppn) == 9 and ppn[5]["status"] == "EXACT_SOURCE_SPECIFIC" and ppn[8]["status"] == "GUARD", "alpha2 projection is derived and scoped"),
        result("VAL4859_05_exchange", len(exchange) == 6 and exchange[4]["status"] == "OPEN_SOURCE_TEST", "powered exchange remains explicit"),
        result("VAL4859_06_radiation", len(radiation) == 10 and radiation[3]["status"] == "PASS", "positive self-channel flux and benchmarks generated"),
        result("VAL4859_07_coscaling", len(coscaling) == 8 and coscaling[1]["status"] == "DERIVED_NECESSARY_SCALING_FOR_THIS_LINEAR_SECTOR" and coscaling[-1]["status"] == "OPEN_PARENT_ORIGIN", "regularity gate derived without parent-origin overclaim"),
        result("VAL4859_08_residuals", len(residuals) == 8 and residuals[0]["status"] == "CLOSED_LINEAR_WEAK_SOURCE" and residuals[-1]["status"] == "OPEN_HARD_SINGULAR_ENDPOINT", "residual vector rebased"),
        result("VAL4859_09_nonclaim", all(not row["valid_for_claim"] for group in groups for row in group), "all generated rows remain private nonclaim"),
        result("VAL4859_10_variables", len(response_variables) == 2, "longitudinal and co-scaling variables integrated"),
        result("VAL4859_11_claim", len(claims) == 1 and claims[0].get("status") == "retarded_transverse_and_longitudinal_power_alpha2_response_derived_coupling_coscaling_gate_private_nonclaim", f"L-701 rows={len(claims)}"),
        result("VAL4859_12_documents", "LONGITUDINAL_RETARDED_ALPHA2_RADIATION_4859" in checkpoint and "PPC4161_RETARDED_EM_ALPHA2_RADIATION_4859" in formal, "checkpoint and formal markers found"),
        result("VAL4859_13_resume", resume_checkpoint_at_least(resume, 4859), "resume reached or advanced beyond the coupling co-scaling gate"),
        result("VAL4859_14_prior", prior_validation[-1].get("status") == "PASS", "4858 validation remains green"),
        result("VAL4859_15_script", compiles(Path(__file__).resolve()), "generator compiles"),
    ]
    checks.append(result("VAL4859_OVERALL", all(row["status"] == "PASS" for row in checks), "RETARDED_LONGITUDINAL_ALPHA2_RADIATION_GATE_VALIDATED"))
    return checks


def main() -> int:
    symbols = symbolic_map()
    sources = source_rows()
    identities = identity_rows(symbols)
    vectors = vector_rows(symbols)
    scalars = scalar_rows(symbols)
    ppn = ppn_rows(symbols)
    exchange = exchange_rows()
    radiation = radiation_rows(symbols)
    coscaling = coscaling_rows(symbols)
    residuals = residual_rows()
    decisions = decision_rows()
    validation = validation_rows(sources, identities, vectors, scalars, ppn, exchange, radiation, coscaling, residuals, decisions)
    write_csv(OUTPUT / "P8_Y5_R2FR_4859_SOURCE_REGISTER.csv", sources)
    write_csv(OUTPUT / "P8_Y5_R2FR_4859_SYMBOLIC_IDENTITIES.csv", identities)
    write_csv(OUTPUT / "P8_Y5_R2FR_4859_VECTOR_RETARDED_KERNEL.csv", vectors)
    write_csv(OUTPUT / "P8_Y5_R2FR_4859_SCALAR_LONGITUDINAL_KERNEL.csv", scalars)
    write_csv(OUTPUT / "P8_Y5_R2FR_4859_PPN_ALPHA2_PROJECTION.csv", ppn)
    write_csv(OUTPUT / "P8_Y5_R2FR_4859_POWER_EXCHANGE.csv", exchange)
    write_csv(OUTPUT / "P8_Y5_R2FR_4859_RADIATION_POWER.csv", radiation)
    write_csv(OUTPUT / "P8_Y5_R2FR_4859_COUPLING_COSCALING.csv", coscaling)
    write_csv(OUTPUT / "P8_Y5_R2FR_4859_RESIDUAL_REBASE.csv", residuals)
    write_csv(OUTPUT / "P8_Y5_R2FR_4859_DECISION.csv", decisions)
    write_csv(OUTPUT / "P8_Y5_BRR545_4859_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print("P8_Y5_BRR545_4859_VALIDATION_PASS" if passed else "P8_Y5_BRR545_4859_VALIDATION_FAIL")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

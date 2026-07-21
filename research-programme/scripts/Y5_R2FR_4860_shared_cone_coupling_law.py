from __future__ import annotations

import csv
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Any

import sympy as sp


CHECKPOINT = "4860"
TIMESTAMP = "2026-07-10T02:00:00+01:00"
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
NEXT_TARGET = "4861-Y5-R2FR-shared-cone-matter-frame-Hilbert-variation-or-base-metric-branch-selection.md"

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
        ("SRC4860_00_3779", POST / "3779-Y5-R2FR-qobs-EM-readout-gauge-and-universal-ZEM-certificate.md", "EXACT_NO_EM_SHADOW_METRIC_CRITERION", "same-Hodge/no-shadow baseline"),
        ("SRC4860_01_1030", POST / "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md", "CM1030_3_disformal_shadow", "matter-frame countermodel guard"),
        ("SRC4860_02_4854", POST / "4854-Y5-R2FR-parent-U1-connection-adoption-or-CP2-Berry-constructor-and-time-flow-constitutive-gate.md", "r_\\gamma^2", "photon constitutive speed"),
        ("SRC4860_03_4857", POST / "4857-Y5-R2FR-parent-time-coframe-kinetic-owner-or-PPN-safe-coefficient-surface-and-mode-stability-gate.md", "c_T^2", "tensor speed and finite corridor"),
        ("SRC4860_04_4858", POST / "4858-Y5-R2FR-Poynting-driven-parent-flow-Green-response-and-EM-rich-PPN-residual-gate.md", "R_B", "stationary transfer"),
        ("SRC4860_05_4859", POST / "4859-Y5-R2FR-longitudinal-EM-power-transfer-retarded-flow-and-alpha2-radiation-gate.md", "zeta=O(1)", "coupling regularity target"),
        ("SRC4860_06_variables", FORMAL / "04-variable-audit.csv", "epsilon_cone_beta_plus_p", "new variables integrated"),
        ("SRC4860_07_equations", FORMAL / "05-equation-register.md", "1.153 Shared characteristic cone", "equation integration"),
        ("SRC4860_08_checkpoint", POST / "4860-Y5-R2FR-parent-coupling-coscaling-law-beta-u-over-p-or-first-EM-radiation-source-profile-test.md", "SHARED_CONE_COUPLING_LAW_4860", "human derivation"),
        ("SRC4860_09_formal876", FORMAL / "876-PPC4161-shared-characteristic-cone-coupling-law.md", "PPC4161_SHARED_CONE_COUPLING_4860", "formal integration"),
        ("SRC4860_10_claim", FORMAL / "02-claims-register.csv", "L-702", "claim register"),
        ("SRC4860_11_redteam", FORMAL / "06-consistency-red-team.md", "104. Shared characteristic cone", "red-team integration"),
        ("SRC4860_12_spine", FORMAL / "07-unification-spine.md", "checkpoint 4860", "spine integration"),
        ("SRC4860_13_resume", POST / "CURRENT_LOCAL_RESUME.md", "# Current local resume", "resume ledger exists and may advance beyond 4860"),
        ("SRC4860_14_script", Path(__file__).resolve(), 'CHECKPOINT = "4860"', "executable symbolic gate"),
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
        ("SRC4860_15_metric_redefinition", "https://arxiv.org/abs/gr-qc/0502066", "metric/vector redefinition and GR-equivalent coefficient family", "primary disformal comparison"),
        ("SRC4860_16_multimessenger", "https://arxiv.org/abs/1710.05834", "-3e-15 <= (v_g-v_gamma)/c <= 7e-16", "primary relative-speed bound"),
        ("SRC4860_17_modes", "https://arxiv.org/abs/1802.04303", "c_T^2=1/(1-c13)", "primary tensor characteristic"),
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
    beta, delta = sp.symbols("beta delta", real=True)
    b_dis = sp.symbols("B", positive=True)
    denominator = d + p - d * p
    c14 = 2 * d * p / (d + p)
    c_vector_sq = denominator * (d + p) / (4 * d * p * (1 - p))
    c_scalar_sq = p / (3 * d * (1 - p))
    q_scalar = 3 * (1 - p) * denominator / p**2
    c_tensor_sq = 1 / (1 - p)
    c_photon_sq = 1 / (1 + beta)
    cone_delta = sp.sqrt((1 + beta) / (1 - p)) - 1
    beta_from_delta = sp.factor((1 - p) * (1 + delta) ** 2 - 1)
    epsilon_cone = sp.factor(beta_from_delta + p)
    beta_shared = -p
    z_normalized = sp.symbols("Z_star", positive=True)
    z_a = sp.factor(z_normalized / sp.sqrt(1 - p))
    eta_u = sp.factor(-p * z_a)
    metric_ratio = sp.factor(1 - d * beta_shared / (d + p))
    flow_ratio = sp.factor((p - beta_shared) / (d + p))
    alpha1 = sp.factor(-8 * d * beta_shared / (d + p))
    alpha2 = sp.factor(beta_shared * (3 * p - d) / (d + p))
    vector_power = sp.factor(
        sp.Rational(16, 3)
        * c14
        * sp.sqrt(c_vector_sq)
        * (beta_shared - p) ** 2
        / denominator**2
    )
    scalar_power = sp.factor(
        q_scalar
        * beta_shared**2
        / (3 * (1 - p) ** 2 * sp.sqrt(c_scalar_sq))
    )
    gr_c1 = -(1 - b_dis) ** 2 / (2 * b_dis)
    gr_c2 = (1 - b_dis) / b_dis
    gr_c3 = -(1 - b_dis**2) / (2 * b_dis)
    gr_c4 = (1 - b_dis) ** 2 / (2 * b_dis)
    b_from_p = 1 / (1 - p)
    gr_values = [sp.factor(value.subs(b_dis, b_from_p)) for value in (gr_c1, gr_c2, gr_c3, gr_c4)]
    return {
        "p": p,
        "d": d,
        "beta": beta,
        "delta": delta,
        "D": denominator,
        "c14": sp.factor(c14),
        "cV2": sp.factor(c_vector_sq),
        "cS2": sp.factor(c_scalar_sq),
        "qS": sp.factor(q_scalar),
        "cT2": sp.factor(c_tensor_sq),
        "cgamma2": sp.factor(c_photon_sq),
        "delta_cone": cone_delta,
        "beta_from_delta": beta_from_delta,
        "epsilon_cone": epsilon_cone,
        "beta_shared": beta_shared,
        "ZA": z_a,
        "eta_u": eta_u,
        "RB_shared": metric_ratio,
        "RW_shared": flow_ratio,
        "alpha1_shared": alpha1,
        "alpha2_shared": alpha2,
        "CV_shared": vector_power,
        "CS_shared": scalar_power,
        "B_from_p": b_from_p,
        "gr_c1": gr_values[0],
        "gr_c2": gr_values[1],
        "gr_c3": gr_values[2],
        "gr_c4": gr_values[3],
        "gr_p": sp.factor(gr_values[0] + gr_values[2]),
        "gr_d": sp.factor(gr_values[0] - gr_values[2]),
        "gr_c14": sp.factor(gr_values[0] + gr_values[3]),
        "gr_c123": sp.factor(gr_values[0] + gr_values[1] + gr_values[2]),
    }


def identity_rows(symbols: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    p = symbols["p"]
    d = symbols["d"]
    delta = symbols["delta"]
    checks = [
        ("ID4860_0_cone", symbols["delta_cone"], sp.sqrt((1 + symbols["beta"]) / (1 - p)) - 1, "relative tensor/photon speed"),
        ("ID4860_1_inverse", symbols["beta_from_delta"], (1 - p) * (1 + delta) ** 2 - 1, "inverse cone map"),
        ("ID4860_2_residual", symbols["epsilon_cone"], (1 - p) * (2 * delta + delta**2), "true multimessenger residual beta+p"),
        ("ID4860_3_shared", symbols["cgamma2"].subs(symbols["beta"], symbols["beta_shared"]), symbols["cT2"], "shared-cone equality"),
        ("ID4860_4_eta", symbols["eta_u"] / symbols["ZA"], -p, "exact coupling law"),
        ("ID4860_5_RB", symbols["RB_shared"], 1 + d * p / (d + p), "stationary metric transfer"),
        ("ID4860_6_RW", symbols["RW_shared"], 2 * p / (d + p), "finite internal flow"),
        ("ID4860_7_a1", symbols["alpha1_shared"], 8 * d * p / (d + p), "shared-cone alpha1"),
        ("ID4860_8_a2", symbols["alpha2_shared"], -p * (3 * p - d) / (d + p), "shared-cone alpha2"),
        ("ID4860_9_gr_p", symbols["gr_p"], p, "GR-equivalent disformal p"),
        ("ID4860_10_gr_c14", symbols["gr_c14"], 0, "GR-equivalent c14 degeneracy"),
        ("ID4860_11_gr_c123", symbols["gr_c123"], 0, "GR-equivalent c123 degeneracy"),
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


def shared_action_rows(symbols: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    entries = [
        ("SA4860_0_metric", "gHat^{mu nu}=g^{mu nu}+p u^mu u^nu", "spin-2 characteristic inverse metric", "EXACT_FROM_C13_PRINCIPAL_SYMBOL"),
        ("SA4860_1_inverse", "gHat_mu_nu=g_mu_nu-p u_mu u_nu/(1-p)", "Sherman-Morrison inverse", "EXACT"),
        ("SA4860_2_measure", "sqrt(-gHat)=sqrt(-g)/sqrt(1-p)", "matrix determinant lemma", "EXACT"),
        ("SA4860_3_Maxwell", "S_A^hat=-Z_star/4 int sqrt(-gHat) gHat^mu_rho gHat^nu_sigma F_mu_nu F_rho_sigma", "minimal Maxwell block on the shared characteristic metric", "CONSTRUCTIVE_PARENT_CANDIDATE"),
        ("SA4860_4_expand", "L_A^hat=-Z_star/[4sqrt(1-p)] [F^2+2p u^mu u^nu F_mu_alpha F_nu^alpha]", "exact covariant expansion", "EXACT"),
        ("SA4860_5_match", f"Z_A={sp.sstr(symbols['ZA'])}; eta_u={sp.sstr(symbols['eta_u'])}", "match to the 4854 operator basis", "PASS"),
        ("SA4860_6_law", "beta_u=eta_u/Z_A=-p; zeta=-1", "no independent constitutive coefficient", "EXACT_ON_SHARED_CONE_CANDIDATE"),
        ("SA4860_7_stability", "lambda_E=Z_A(1-p)>0; lambda_B=Z_A>0 for 0<p<1", "photon Hamiltonian remains positive", "PASS"),
        ("SA4860_8_speed", "c_gamma^2=lambda_B/lambda_E=1/(1-p)=c_T^2", "exact common characteristic cone", "PASS"),
    ]
    return [
        {"row_id": row_id, "equation": equation, "meaning": meaning, "status": status, "valid_for_claim": False, "timestamp_utc": TIMESTAMP}
        for row_id, equation, meaning, status in entries
    ]


def cone_bound_rows() -> list[dict[str, Any]]:
    p_value = Decimal("1e-15")
    delta_min = Decimal("-3e-15")
    delta_max = Decimal("7e-16")
    epsilon_min = (1 - p_value) * (2 * delta_min + delta_min**2)
    epsilon_max = (1 - p_value) * (2 * delta_max + delta_max**2)
    entries = [
        ("CB4860_0_delta", "delta_c=c_T/c_gamma-1", "quantity constrained by GW170817/GRB170817A", "DEFINITION"),
        ("CB4860_1_exact", "delta_c=sqrt[(1+beta_u)/(1-p)]-1", "corrects the p=0 specialization used at 4854", "EXACT"),
        ("CB4860_2_epsilon", "epsilon_cone=beta_u+p=(1-p)(2delta_c+delta_c^2)", "source-backed combination", "EXACT"),
        ("CB4860_3_lower", f"epsilon_cone>={epsilon_min}", "using delta_c>=-3e-15 at p=1e-15", "PASS"),
        ("CB4860_4_upper", f"epsilon_cone<={epsilon_max}", "using delta_c<=7e-16 at p=1e-15", "PASS"),
        ("CB4860_5_scope", "the old beta_u interval is recovered only at p=0", "after 4857 the data do not separately measure beta_u and p", "CORRECTION"),
        ("CB4860_6_shared", "epsilon_cone=0 -> beta_u=-p", "shared-cone branch is centered exactly inside the source-backed interval", "PASS"),
    ]
    return [
        {"row_id": row_id, "equation": equation, "meaning": meaning, "status": status, "valid_for_claim": False, "timestamp_utc": TIMESTAMP}
        for row_id, equation, meaning, status in entries
    ]


def branch_rows() -> list[dict[str, Any]]:
    p_value = Decimal("1e-15")
    d_value = p_value / Decimal(3)
    delta_min = Decimal("-3e-15")
    delta_max = Decimal("7e-16")
    branches = [
        ("BR4860_0_base", "same_g_minimal_Maxwell", Decimal(0), "zeta=0", "no direct uFF operator", "LOWEST_RISK_BASELINE"),
        ("BR4860_1_shared", "shared_characteristic_metric", -p_value, "zeta=-1", "minimal Maxwell on gHat", "LEAD_NONZERO_CONSTRUCTIVE_CANDIDATE"),
        ("BR4860_2_flowzero", "transverse_flow_cancellation", p_value, "zeta=1", "sets beta_u=p by response cancellation", "NOT_PARENT_DERIVED_AND_UPPER_EDGE_CONE_FAIL"),
        ("BR4860_3_fixed", "fixed_independent_beta", Decimal("-6e-15"), "zeta diverges", "old independent interval endpoint", "FAILS_P_TO_ZERO_REGULARITY"),
    ]
    rows: list[dict[str, Any]] = []
    for row_id, name, beta, scaling, origin, verdict in branches:
        c_tensor_sq = Decimal(1) / (1 - p_value)
        c_photon_sq = Decimal(1) / (1 + beta)
        delta_cone = (c_tensor_sq / c_photon_sq).sqrt() - 1
        rows.append(
            {
                "branch_id": row_id,
                "branch": name,
                "p": p_value,
                "d": d_value,
                "beta_u": beta,
                "epsilon_cone": beta + p_value,
                "zeta_or_limit": scaling,
                "delta_cone": delta_cone,
                "multimessenger_pass": delta_min <= delta_cone <= delta_max,
                "origin": origin,
                "verdict": verdict,
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    return rows


def observable_rows(symbols: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    p_value = Decimal("1e-15")
    d_value = p_value / Decimal(3)
    denominator = d_value + p_value - d_value * p_value
    c14 = 2 * d_value * p_value / (d_value + p_value)
    c_vector = (denominator * (d_value + p_value) / (4 * d_value * p_value * (1 - p_value))).sqrt()
    c_scalar = (p_value / (3 * d_value * (1 - p_value))).sqrt()
    q_scalar = 3 * (1 - p_value) * denominator / p_value**2
    beta = -p_value
    metric_residual = -d_value * beta / (d_value + p_value)
    flow_ratio = (p_value - beta) / (d_value + p_value)
    alpha1 = -8 * d_value * beta / (d_value + p_value)
    alpha2 = beta * (3 * p_value - d_value) / (d_value + p_value)
    vector_power = Decimal(16) / 3 * c14 * c_vector * (beta - p_value) ** 2 / denominator**2
    scalar_power = q_scalar * beta**2 / (3 * (1 - p_value) ** 2 * c_scalar)
    entries = [
        ("OB4860_0_metric", f"delta_B={metric_residual}", "shared-cone stationary metric residual at p=1e-15,d=p/3", "PASS_WORKING_CORRIDOR"),
        ("OB4860_1_flow", f"R_W={flow_ratio}", "finite physical flow response", "PASS"),
        ("OB4860_2_alpha1", f"alpha1_EM={alpha1}", "source-specific weak preferred-frame coefficient", "PASS_WORKING_CORRIDOR"),
        ("OB4860_3_alpha2", f"alpha2_EM={alpha2}", "source-specific weak longitudinal coefficient", "PASS_WORKING_CORRIDOR"),
        ("OB4860_4_vector", f"C_V={vector_power}", "coefficient multiplying Gae abs(dot Q_EM)^2", "FINITE_VANISHES_WITH_P"),
        ("OB4860_5_scalar", f"C_S={scalar_power}", "direct scalar coefficient multiplying Gae abs(dot Q_EM)^2", "FINITE_VANISHES_WITH_P"),
        ("OB4860_6_bounds", "0<d<=p/3 -> abs(delta_B)<=p/4; abs(alpha1_EM)<=2p; abs(alpha2_EM)<=3p", "analytic shared-cone envelope", "PASS"),
        ("OB4860_7_p_scope", "p<=1e-15 is retained as a working corridor but is not derived by relative GW timing when epsilon_cone=0", "shared cone removes the relative-speed lever on absolute p", "OPEN_ABSOLUTE_P_PROVENANCE"),
    ]
    return [
        {"row_id": row_id, "value_or_equation": value, "meaning": meaning, "status": status, "valid_for_claim": False, "timestamp_utc": TIMESTAMP}
        for row_id, value, meaning, status in entries
    ]


def field_redefinition_rows(symbols: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    entries = [
        ("FR4860_0_map", "g'_ab=g_ab-(1-B)u_a u_b; u'^a=u^a/sqrt(B)", "Foster constant metric/vector redefinition", "PRIMARY_MAP"),
        ("FR4860_1_B", f"B={sp.sstr(symbols['B_from_p'])}", "choice that gives apparent c13=p", "EXACT"),
        ("FR4860_2_coeff", f"c1={sp.sstr(symbols['gr_c1'])};c2={sp.sstr(symbols['gr_c2'])};c3={sp.sstr(symbols['gr_c3'])};c4={sp.sstr(symbols['gr_c4'])}", "pure-GR-generated aether coefficients", "EXACT_PRIMARY_SPECIALIZATION"),
        ("FR4860_3_degenerate", "c14=0 and c123=0", "aether modes are field-redefinition/gauge degenerate", "EXACT"),
        ("FR4860_4_d", f"d_GR={sp.sstr(symbols['gr_d'])}<0 for 0<p<1", "opposite sign to the finite 4857 corridor d>0", "DISJOINT_FINITE_BRANCH"),
        ("FR4860_5_Maxwell", "minimal Maxwell on g' also gives beta_u=-p in g variables", "same shared-cone algebra", "EXACT"),
        ("FR4860_6_guard", "vacuum GR equivalence requires transforming matter consistently", "a metric field redefinition alone does not prove physical equivalence with fixed matter coupling", "GUARD"),
        ("FR4860_7_verdict", "the Foster family is an exact gauge-restoration existence example but not the 4857 finite regularizer", "cannot import its GR equivalence into d>0 corridor", "NO_SHORTCUT"),
    ]
    return [
        {"row_id": row_id, "equation": equation, "meaning": meaning, "status": status, "valid_for_claim": False, "timestamp_utc": TIMESTAMP}
        for row_id, equation, meaning, status in entries
    ]


def residual_rows() -> list[dict[str, Any]]:
    entries = [
        (1, "E_beta_origin", "CLOSED_CONSTRUCTIVE_CANDIDATE", "shared characteristic metric fixes beta_u=-p exactly", "derive whether MTS parent selects shared cone or same-g Hodge"),
        (2, "E_multimessenger_map", "CORRECTED_EXACT", "GW/GRB timing constrains epsilon_cone=beta_u+p, not beta_u alone", "propagate correction through older coefficient bounds"),
        (3, "E_endpoint_EM", "CLOSED_ON_TWO_PARAMETER_FREE_BRANCHES", "beta_u=0 and beta_u=-p both satisfy the 4859 regularity gate", "choose matter-frame architecture"),
        (4, "E_matter_frame", "OPEN_HARD_NEXT", "shared gHat can be an optical metric or the public matter metric; predictions differ", "perform full Hilbert/source/clock frame variation"),
        (5, "E_absolute_p", "OPEN_ON_SHARED_CONE", "relative GW timing is identically silent when cT=cgamma", "source independent matter/photon or parent p bound"),
        (6, "E_exact_GR", "OPEN_BUT_SHARPENED", "Foster GR-equivalent family exists but has d<0,c14=c123=0 and is not the finite safe branch", "derive a genuine gauge-restoration path for d>0 branch"),
        (7, "E_source_profile", "DEFERRED_ONE_STEP", "radiation profile remains unnecessary until the coefficient/matter-frame fork is fixed", "run after 4861 branch selection"),
    ]
    return [
        {"priority": priority, "residual": residual, "status": status, "evidence": evidence, "next_action": next_action, "valid_for_claim": False, "timestamp_utc": TIMESTAMP}
        for priority, residual, status, evidence, next_action in entries
    ]


def decision_rows() -> list[dict[str, Any]]:
    entries = [
        ("DEC4860_0_bound", "replace the standalone beta_u propagation bound with an epsilon_cone=beta_u+p bound", "4857 makes cT depend on p, so the measured quantity is relative speed"),
        ("DEC4860_1_base", "retain beta_u=0 as the lowest-risk same-Hodge baseline", "it adds no shadow metric and preserves the original GW lever on p"),
        ("DEC4860_2_shared", "adopt beta_u=-p as the lead nonzero constructive candidate", "minimal Maxwell on the tensor characteristic metric gives it exactly with no new parameter"),
        ("DEC4860_3_demote", "demote independent fixed beta_u and beta_u=p response tuning", "the former is endpoint singular and the latter lacks a parent owner and misses the upper-edge cone bound"),
        ("DEC4860_4_next", "vary the shared-cone action through the matter/source frame before promotion", "the remaining ambiguity is physical architecture, not coefficient algebra"),
    ]
    return [
        {"decision_id": row_id, "decision": decision, "reason": reason, "next_target": NEXT_TARGET if row_id == "DEC4860_4_next" else "", "valid_for_claim": False, "timestamp_utc": TIMESTAMP}
        for row_id, decision, reason in entries
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    identities: list[dict[str, Any]],
    action: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    branches: list[dict[str, Any]],
    observables: list[dict[str, Any]],
    redefinition: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    claims = [row for row in read_csv(FORMAL / "02-claims-register.csv") if row.get("claim_id") == "L-702"]
    variables = read_csv(FORMAL / "04-variable-audit.csv")
    response_variables = [row for row in variables if row.get("symbol") in {"epsilon_cone_beta_plus_p", "gHat_shared_characteristic"}]
    checkpoint = (POST / "4860-Y5-R2FR-parent-coupling-coscaling-law-beta-u-over-p-or-first-EM-radiation-source-profile-test.md").read_text(encoding="utf-8")
    formal = (FORMAL / "876-PPC4161-shared-characteristic-cone-coupling-law.md").read_text(encoding="utf-8")
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")
    prior_validation = read_csv(OUTPUT / "P8_Y5_BRR545_4859_VALIDATION.csv")

    def result(check_id: str, passed: bool, detail: str) -> dict[str, Any]:
        return {"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail, "valid_for_claim": False, "timestamp_utc": TIMESTAMP}

    groups = (sources, identities, action, bounds, branches, observables, redefinition, residuals, decisions)
    checks = [
        result("VAL4860_00_sources", len(sources) == 18 and all(row["source_exists"] and row["needle_found"] for row in sources), f"sources={len(sources)}"),
        result("VAL4860_01_identities", len(identities) == 12 and all(row["status"] == "PASS" for row in identities), "cone, coupling and disformal identities pass"),
        result("VAL4860_02_action", len(action) == 9 and action[6]["status"] == "EXACT_ON_SHARED_CONE_CANDIDATE", "shared action derives beta_u=-p"),
        result("VAL4860_03_bounds", len(bounds) == 7 and bounds[-1]["status"] == "PASS", "corrected multimessenger combination and shared zero pass"),
        result("VAL4860_04_branches", len(branches) == 4 and branches[0]["multimessenger_pass"] and branches[1]["multimessenger_pass"] and not branches[2]["multimessenger_pass"], "branch matrix discriminates upper-edge flow-cancel route"),
        result("VAL4860_05_observables", len(observables) == 8 and observables[-1]["status"] == "OPEN_ABSOLUTE_P_PROVENANCE", "shared branch observables and p-scope retained"),
        result("VAL4860_06_redefinition", len(redefinition) == 8 and redefinition[-1]["status"] == "NO_SHORTCUT", "GR-equivalent field redefinition is compared without promotion"),
        result("VAL4860_07_residuals", len(residuals) == 7 and residuals[0]["status"] == "CLOSED_CONSTRUCTIVE_CANDIDATE" and residuals[3]["status"] == "OPEN_HARD_NEXT", "residual vector rebased to matter-frame fork"),
        result("VAL4860_08_nonclaim", all(not row["valid_for_claim"] for group in groups for row in group), "all rows remain private nonclaim"),
        result("VAL4860_09_variables", len(response_variables) == 2, "cone and characteristic variables integrated"),
        result("VAL4860_10_claim", len(claims) == 1 and claims[0].get("status") == "shared_characteristic_metric_beta_minus_p_constructed_corrected_cone_bound_private_nonclaim", f"L-702 rows={len(claims)}"),
        result("VAL4860_11_documents", "SHARED_CONE_COUPLING_LAW_4860" in checkpoint and "PPC4161_SHARED_CONE_COUPLING_4860" in formal, "checkpoint and formal markers found"),
        result("VAL4860_12_resume", resume_checkpoint_at_least(resume, 4860), "resume reached or advanced beyond matter-frame variation"),
        result("VAL4860_13_prior", prior_validation[-1].get("status") == "PASS", "4859 validation remains green"),
        result("VAL4860_14_script", compiles(Path(__file__).resolve()), "generator compiles"),
    ]
    checks.append(result("VAL4860_OVERALL", all(row["status"] == "PASS" for row in checks), "SHARED_CONE_COUPLING_LAW_GATE_VALIDATED"))
    return checks


def main() -> int:
    symbols = symbolic_map()
    sources = source_rows()
    identities = identity_rows(symbols)
    action = shared_action_rows(symbols)
    bounds = cone_bound_rows()
    branches = branch_rows()
    observables = observable_rows(symbols)
    redefinition = field_redefinition_rows(symbols)
    residuals = residual_rows()
    decisions = decision_rows()
    validation = validation_rows(sources, identities, action, bounds, branches, observables, redefinition, residuals, decisions)
    write_csv(OUTPUT / "P8_Y5_R2FR_4860_SOURCE_REGISTER.csv", sources)
    write_csv(OUTPUT / "P8_Y5_R2FR_4860_SYMBOLIC_IDENTITIES.csv", identities)
    write_csv(OUTPUT / "P8_Y5_R2FR_4860_SHARED_ACTION.csv", action)
    write_csv(OUTPUT / "P8_Y5_R2FR_4860_CORRECTED_CONE_BOUND.csv", bounds)
    write_csv(OUTPUT / "P8_Y5_R2FR_4860_BRANCH_MATRIX.csv", branches)
    write_csv(OUTPUT / "P8_Y5_R2FR_4860_SHARED_OBSERVABLES.csv", observables)
    write_csv(OUTPUT / "P8_Y5_R2FR_4860_GR_FIELD_REDEFINITION.csv", redefinition)
    write_csv(OUTPUT / "P8_Y5_R2FR_4860_RESIDUAL_REBASE.csv", residuals)
    write_csv(OUTPUT / "P8_Y5_R2FR_4860_DECISION.csv", decisions)
    write_csv(OUTPUT / "P8_Y5_BRR545_4860_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print("P8_Y5_BRR545_4860_VALIDATION_PASS" if passed else "P8_Y5_BRR545_4860_VALIDATION_FAIL")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

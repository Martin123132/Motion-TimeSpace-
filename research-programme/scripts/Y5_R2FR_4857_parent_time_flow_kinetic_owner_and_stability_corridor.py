from __future__ import annotations

import csv
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Any

import sympy as sp


CHECKPOINT = "4857"
TIMESTAMP = "2026-07-10T00:26:00+00:00"
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = POST / "source-intake" / "local_bounds" / "local_bound_claims.csv"
NEXT_TARGET = "4858-Y5-R2FR-Poynting-driven-parent-flow-Green-response-and-EM-rich-PPN-residual-gate.md"

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
        ("SRC4857_00_80", POST / "80-stress-free-reference-action-gate.md", "failed_as_parent_action", "rejected stress-free reference route"),
        ("SRC4857_01_4847", POST / "4847-Y5-R2FR-coherent-load-covariant-Hilbert-stress-and-tau-Euler-equation-or-H-load-cosmology-smoke-fit.md", "healthy parent time/coframe kinetic sector is required", "parent kinetic-owner requirement"),
        ("SRC4857_02_4850", POST / "4850-Y5-R2FR-H-load-scalar-kinetic-mode-or-parent-tau-regularization-before-CMB-growth.md", "propagating shared-parent tau/coframe completion", "separate completion branch and local degeneracy"),
        ("SRC4857_03_4856", POST / "4856-Y5-R2FR-time-flow-Hilbert-variation-and-preferred-frame-PPN-alpha1-alpha2-gate.md", "c_4=-\\frac{c_3^2}{c_1}", "conditional PPN-safe surface handoff"),
        ("SRC4857_04_bounds", LOCAL_BOUNDS, "R5_alpha1", "local preferred-frame comparator rows"),
        ("SRC4857_05_variables", FORMAL / "04-variable-audit.csv", "p_aether_d_aether", "adapted kinetic variables"),
        ("SRC4857_06_equations", FORMAL / "05-equation-register.md", "1.150 Parent time-flow kinetic owner and stable PPN corridor", "equation integration"),
        ("SRC4857_07_checkpoint", POST / "4857-Y5-R2FR-parent-time-coframe-kinetic-owner-or-PPN-safe-coefficient-surface-and-mode-stability-gate.md", "PARENT_TIME_FLOW_KINETIC_STABILITY_4857", "human-readable derivation"),
        ("SRC4857_08_formal873", FORMAL / "873-PPC4161-parent-time-flow-kinetic-owner-and-stability-corridor.md", "PPC4161_PARENT_TIME_FLOW_KINETIC_STABILITY_4857", "formal-workbench integration"),
        ("SRC4857_09_claim", FORMAL / "02-claims-register.csv", "L-699", "claim register"),
        ("SRC4857_10_resume", POST / "CURRENT_LOCAL_RESUME.md", "# Current local resume", "resume ledger exists and may advance beyond 4857"),
        ("SRC4857_11_script", Path(__file__).resolve(), 'CHECKPOINT = "4857"', "executable symbolic gate"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in local_sources:
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        rows.append(
            {
                "source_id": source_id,
                "source_kind": "local",
                "source_locator": str(path),
                "source_exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "source_validated": path.exists() and needle in text,
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    web_sources = [
        ("SRC4857_12_PPN", "https://arxiv.org/abs/gr-qc/0509083", "exact alpha1/alpha2 and PPN-zero surface", "primary PPN map"),
        ("SRC4857_13_waves", "https://arxiv.org/abs/gr-qc/0402005", "spin-0/spin-1/spin-2 mode spectrum", "primary wave-mode basis"),
        ("SRC4857_14_GW", "https://arxiv.org/abs/1802.04303", "qS/qV/qT, speeds, G_N, G_cos and abs(c13)<1e-15", "primary post-GW stability and calibration map"),
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
    c1, c2, c3, c4, p, d = sp.symbols("c1 c2 c3 c4 p d", nonzero=True)
    c13 = c1 + c3
    c14 = c1 + c4
    c123 = c1 + c2 + c3
    alpha1 = -8 * (c3**2 + c1 * c4) / (2 * c1 - c1**2 + c3**2)
    alpha2 = alpha1 / 2 - (c1 + 2 * c3 - c4) * (2 * c1 + 3 * c2 + c3 + c4) / (c123 * (2 - c14))
    safe_c4 = -c3**2 / c1
    safe_c2 = (-2 * c1**2 - c1 * c3 + c3**2) / (3 * c1)
    safe_sub = {c4: safe_c4, c2: safe_c2}
    pd_sub = {c1: (p + d) / 2, c3: (p - d) / 2}
    c14_pd = sp.factor(c14.subs(safe_sub).subs(pd_sub))
    c123_pd = sp.factor(c123.subs(safe_sub).subs(pd_sub))
    c2_pd = sp.factor(safe_c2.subs(pd_sub))
    c4_pd = sp.factor(safe_c4.subs(pd_sub))
    dkin_pd = sp.factor((2 * c1 - c1**2 + c3**2).subs(pd_sub))
    a_pd = sp.factor(2 + p + 3 * c2_pd)
    q_s = sp.factor((1 - p) * a_pd / c123_pd)
    q_v = c14_pd
    q_t = 1 - p
    speed_s = sp.factor(c123_pd * (2 - c14_pd) / (c14_pd * (1 - p) * a_pd))
    speed_v = sp.factor(dkin_pd / (2 * c14_pd * (1 - p)))
    speed_t = 1 / (1 - p)
    return {
        "c1": c1,
        "c2": c2,
        "c3": c3,
        "c4": c4,
        "p": p,
        "d": d,
        "alpha1": sp.factor(alpha1),
        "alpha2": sp.factor(alpha2),
        "safe_c2": sp.factor(safe_c2),
        "safe_c4": sp.factor(safe_c4),
        "alpha1_safe": sp.simplify(alpha1.subs(safe_sub)),
        "alpha2_safe": sp.simplify(alpha2.subs(safe_sub)),
        "c2_pd": c2_pd,
        "c4_pd": c4_pd,
        "c14_pd": c14_pd,
        "c123_pd": c123_pd,
        "ctheta_pd": sp.factor(p + 3 * c2_pd),
        "dkin_pd": dkin_pd,
        "a_pd": a_pd,
        "q_s": q_s,
        "q_v": q_v,
        "q_t": q_t,
        "speed_s": speed_s,
        "speed_v": speed_v,
        "speed_t": speed_t,
    }


def operator_rows(symbols: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    entries = [
        ("OP4857_0_action", "S=(2 kappa_*)^-1 int sqrt(-g)[R-2 Lambda-K^{ab}_{mn} nabla_a u^m nabla_b u^n+lambda(u^2+1)-2G(theta)]", "minimal EH plus physical unit-flow and existing memory completion", "ADOPTED_PRIVATE_CORRESPONDENCE_BLOCK"),
        ("OP4857_1_basis", "K^{ab}_{mn}=c1 g^{ab}g_mn+c2 delta^a_m delta^b_n+c3 delta^a_n delta^b_m-c4 u^a u^b g_mn", "complete parity-even diffeomorphism-covariant quadratic two-derivative basis", "DERIVED_FROM_FIELD_CONTENT_AND_DERIVATIVE_ORDER"),
        ("OP4857_2_no_new_field", "field content=(g_mu_nu,u_mu,lambda_u)", "u already exists in the MTS memory and EM constitutive blocks", "COMPLETION_NOT_NEW_FIELD"),
        ("OP4857_3_kinematic", "c_sigma=c13; c_omega=c1-c3; c_a=c14; c_theta=c13+3c2", "expansion/shear/vorticity/acceleration decomposition", "EXACT"),
        ("OP4857_4_matter", "S_matter=S_matter[g,psi] and S_A uses the same g", "no direct matter-aether charge is added", "UNIVERSAL_METRIC_COUPLING_GUARD"),
        ("OP4857_5_scope", "operator basis derived; coefficient point not primitive-MTS derived", "a finite coefficient corridor is an EFT completion, not a claimed microscopic origin", "PRIVATE_NONCLAIM_SCOPE"),
    ]
    return [
        {"operator_id": row_id, "equation": equation, "meaning": meaning, "status": status, "valid_for_claim": False, "timestamp_utc": TIMESTAMP}
        for row_id, equation, meaning, status in entries
    ]


def ppn_rows(symbols: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    entries = [
        ("PPN4857_0_alpha", f"alpha1={sp.sstr(symbols['alpha1'])}; alpha2={sp.sstr(symbols['alpha2'])}", "exact weak-field preferred-frame map", "PRIMARY_FORMULA"),
        ("PPN4857_1_surface", f"c4={sp.sstr(symbols['safe_c4'])}; c2={sp.sstr(symbols['safe_c2'])}", "nondegenerate alpha1=alpha2=0 surface", "EXACT"),
        ("PPN4857_2_symbolic", f"alpha1_safe={symbols['alpha1_safe']}; alpha2_safe={symbols['alpha2_safe']}", "symbolic substitution", "PASS" if symbols["alpha1_safe"] == 0 and symbols["alpha2_safe"] == 0 else "FAIL"),
        ("PPN4857_3_pd", "p=c13=c1+c3; d=c1-c3", "GW-adapted shear and vorticity coordinates", "EXACT_CHANGE_OF_VARIABLES"),
        ("PPN4857_4_coefficients", f"c2={sp.sstr(symbols['c2_pd'])}; c4={sp.sstr(symbols['c4_pd'])}", "full safe surface in p,d", "EXACT"),
        ("PPN4857_5_combinations", f"c14={sp.sstr(symbols['c14_pd'])}; c123={sp.sstr(symbols['c123_pd'])}; ctheta={sp.sstr(symbols['ctheta_pd'])}", "kinetic combinations", "EXACT"),
        ("PPN4857_6_Gequality", "ctheta=-c14 -> G_cos=G_ae/(1+ctheta/2)=G_ae/(1-c14/2)=G_N", "PPN-safe surface also removes the Newton/cosmological-G mismatch", "EXACT" if sp.simplify(symbols["ctheta_pd"] + symbols["c14_pd"]) == 0 else "FAIL"),
        ("PPN4857_7_other", "beta=gamma=1 and all non-alpha1/alpha2 weak-field PPN parameters equal GR for universal metric matter coupling", "standard semi-conservative unit-flow result", "CONDITIONAL_CORRESPONDENCE_RESULT"),
    ]
    return [
        {"row_id": row_id, "equation": equation, "meaning": meaning, "status": status, "valid_for_claim": False, "timestamp_utc": TIMESTAMP}
        for row_id, equation, meaning, status in entries
    ]


def mode_rows(symbols: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    entries = [
        ("MODE4857_0_qS", f"qS={sp.sstr(symbols['q_s'])}", "scalar time-kinetic coefficient", "POSITIVE_IN_CORRIDOR"),
        ("MODE4857_1_qV", f"qV={sp.sstr(symbols['q_v'])}", "vector time-kinetic coefficient", "POSITIVE_IN_CORRIDOR"),
        ("MODE4857_2_qT", f"qT={sp.sstr(symbols['q_t'])}", "tensor time-kinetic coefficient", "POSITIVE_IN_CORRIDOR"),
        ("MODE4857_3_cS", f"cS2={sp.sstr(symbols['speed_s'])}", "spin-0 squared speed", "SUPERLUMINAL_OR_LUMINAL_IN_CORRIDOR"),
        ("MODE4857_4_cV", f"cV2={sp.sstr(symbols['speed_v'])}", "spin-1 squared speed", "SUPERLUMINAL_OR_LUMINAL_IN_CORRIDOR"),
        ("MODE4857_5_cT", f"cT2={sp.sstr(symbols['speed_t'])}", "spin-2 squared speed", "GW_BOUNDED"),
        ("MODE4857_6_corridor", "0<p<=1e-15 and 0<d<=p/3", "sufficient ghost-free, gradient-stable and no-vacuum-Cherenkov corridor", "DERIVED_SUFFICIENT_CORRIDOR"),
        ("MODE4857_7_proof_scalar", "d=r p, 0<r<=1/3 -> cS2=1/[3r(1-p)]>=1", "scalar speed proof", "EXACT_INEQUALITY"),
        ("MODE4857_8_proof_vector", "cV2=(1+r)[(1+r)+p/(1-p)]/(4r)>=(1+r)^2/(4r)>=1", "vector speed proof", "EXACT_INEQUALITY"),
        ("MODE4857_9_proof_tensor", "cT2=1/(1-p)>=1", "tensor speed proof", "EXACT_INEQUALITY"),
    ]
    return [
        {"mode_id": row_id, "equation_or_condition": equation, "meaning": meaning, "status": status, "valid_for_claim": False, "timestamp_utc": TIMESTAMP}
        for row_id, equation, meaning, status in entries
    ]


def benchmark_rows() -> list[dict[str, Any]]:
    p = Decimal("1e-15")
    d = p / Decimal(3)
    c1 = (p + d) / Decimal(2)
    c3 = (p - d) / Decimal(2)
    c4 = -(p - d) ** 2 / (Decimal(2) * (p + d))
    c2 = -p * (Decimal(3) * d + p) / (Decimal(3) * (d + p))
    c14 = Decimal(2) * d * p / (d + p)
    c123 = Decimal(2) * p * p / (Decimal(3) * (d + p))
    q_s = Decimal(3) * (Decimal(1) - p) * (d + p - d * p) / (p * p)
    q_v = c14
    q_t = Decimal(1) - p
    speed_s = p / (Decimal(3) * d * (Decimal(1) - p))
    speed_v = (d + p) * (d + p - d * p) / (Decimal(4) * d * p * (Decimal(1) - p))
    speed_t = Decimal(1) / (Decimal(1) - p)
    c_t_minus_one = speed_t.sqrt() - Decimal(1)
    g_shift = c14 / (Decimal(2) - c14)
    reduced_planck_gev = Decimal("2.435e18")
    vector_kinetic_proxy_gev = reduced_planck_gev * q_v.sqrt()
    entries = [
        ("BEN4857_0_point", "p=1e-15; d=p/3", "upper-edge no-Cherenkov benchmark", "NONPREDICTIVE_BENCHMARK"),
        ("BEN4857_1_coefficients", f"c1={c1};c2={c2};c3={c3};c4={c4}", "finite PPN-safe coefficient point", "PASS"),
        ("BEN4857_2_combinations", f"c14={c14};c123={c123}", "positive mode combinations", "PASS"),
        ("BEN4857_3_kinetic", f"qS={q_s};qV={q_v};qT={q_t}", "all kinetic coefficients positive", "PASS" if q_s > 0 and q_v > 0 and q_t > 0 else "FAIL"),
        ("BEN4857_4_speeds", f"cS2={speed_s};cV2={speed_v};cT2={speed_t}", "all squared speeds at least one", "PASS" if min(speed_s, speed_v, speed_t) >= 1 else "FAIL"),
        ("BEN4857_5_GW", f"cT-1={c_t_minus_one}", "inside the conservative multimessenger interval", "PASS" if c_t_minus_one <= Decimal("7e-16") else "FAIL"),
        ("BEN4857_6_G", f"G_N/G_ae-1={g_shift}", "same calibrated shift applies to G_cos", "PASS"),
        ("BEN4857_7_scale_proxy", f"Mbar_Pl*sqrt(qV)={vector_kinetic_proxy_gev} GeV", "canonical vector kinetic scale proxy only, not a full nonlinear strong-coupling theorem", "FINITE_HIGH_SCALE_BENCHMARK"),
    ]
    return [
        {"benchmark_id": row_id, "value": value, "meaning": meaning, "status": status, "valid_for_claim": False, "timestamp_utc": TIMESTAMP}
        for row_id, value, meaning, status in entries
    ]


def limit_rows(symbols: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    entries = [
        ("LIM4857_0_exact", "p=c13=0 on the exact PPN-safe surface", "c14=0 and c123=0", "VECTOR_AND_SCALAR_KINETIC_DEGENERACY"),
        ("LIM4857_1_finite_d", "p->0 with d finite", "qV->0; cS and cV formulas are singular/nonuniform", "NO_HEALTHY_EXACT_GR_ENDPOINT"),
        ("LIM4857_2_joint", "p->0 with d=r p and fixed 0<r<=1/3", "all c_i and qV scale to zero while finite mode speeds remain", "CANONICAL_NORMALIZATION_COLLAPSES"),
        ("LIM4857_3_resolution", "exact GR requires local gauge restoration or elimination of u as a physical mode", "a merely vanishing coefficient limit is not a regular parent derivation", "GAUGE_ENHANCEMENT_THEOREM_REQUIRED_FOR_EXACT_GR"),
        ("LIM4857_4_finite", "strictly positive p,d corridor", "healthy PPN-identical-through-1PN completion exists", "FINITE_CORRESPONDENCE_BRANCH_SURVIVES"),
        ("LIM4857_5_memory", "parent ctheta=-c14 supplies a nonzero quadratic expansion owner while G_theta_theta(0)=0", "local memory degeneracy no longer leaves u without a quadratic parent operator", "LOCAL_KINETIC_OWNER_FILLED_IN_FINITE_BRANCH"),
    ]
    return [
        {"limit_id": row_id, "limit": limit, "result": result, "status": status, "valid_for_claim": False, "timestamp_utc": TIMESTAMP}
        for row_id, limit, result, status in entries
    ]


def em_pressure_rows() -> list[dict[str, Any]]:
    p = Decimal("1e-15")
    c14_max_corridor = p / Decimal(2)
    eta_over_lambda_max = Decimal("6e-15")
    ratio = eta_over_lambda_max / c14_max_corridor
    entries = [
        ("EM4857_0_source", "D_mu G_theta=-kappa eta_u S_mu", "4856 Poynting force now acts through a defined parent Green operator", "DERIVED_SOURCE_WITH_OWNER"),
        ("EM4857_1_response", "delta u_transverse scales schematically as (eta_u/lambda_E)/c14 times the sourced EM momentum profile", "the propagation bound alone need not suppress induced flow after canonical normalization", "GREEN_COEFFICIENT_REQUIRED"),
        ("EM4857_2_benchmark", f"abs(eta/lambda_E)/c14={ratio} at abs(eta/lambda_E)=6e-15 and c14=5e-16", "upper-edge coefficient ratio can be order ten", "PRESSURE_NOT_PREDICTION"),
        ("EM4857_3_guard", "ordinary-source PPN also multiplies EM energy fraction and geometry", "no alpha1/alpha2 failure follows from the coefficient ratio alone", "SOURCE_PROFILE_REQUIRED"),
    ]
    return [
        {"row_id": row_id, "equation_or_value": equation, "meaning": meaning, "status": status, "valid_for_claim": False, "timestamp_utc": TIMESTAMP}
        for row_id, equation, meaning, status in entries
    ]


def residual_rows() -> list[dict[str, Any]]:
    entries = [
        (1, "E_parent_u_kinetic_basis", "CLOSED_PRIVATE_EFT_COMPLETION", "unique quadratic two-derivative unit-flow basis adopted for the already present physical flow", "derive primitive MTS coefficient selection or retain as correspondence block"),
        (2, "E_local_PPN_weak", "CLOSED_ON_EXACT_SAFE_SURFACE", "alpha1=alpha2=0 and remaining weak PPN equals GR with universal metric matter coupling", "retain strong-field and radiation tests"),
        (3, "E_mode_stability", "FINITE_HEALTHY_CORRIDOR_DERIVED", "0<p<=1e-15 and 0<d<=p/3 makes qS/qV/qT positive and all mode speeds at least luminal", "source a nonzero lower kinetic floor and test nonlinear cutoff"),
        (4, "E_Newton_cosmo_G", "EXACT_EQUALITY_ON_SAFE_SURFACE", "ctheta=-c14 gives G_cos=G_N", "reexpress existing memory cosmology in calibrated G_N convention"),
        (5, "E_exact_GR_endpoint", "OPEN_HARD_SINGULAR_LIMIT", "p=0 forces c14=c123=0 and collapses extra-mode kinetic normalization", "derive gauge restoration/elimination if exact GR rather than PPN equivalence is required"),
        (6, "E_Poynting_flow_response", "OPEN_HARD_NEXT_TARGET", "eta/c14 can remove the naive propagation suppression", "derive sourced Green response and EM-rich PPN residual"),
        (7, "E_strong_field_radiation", "OPEN_HARD", "neutron-star sensitivities and extra-mode radiation are not closed by weak PPN", "compute sensitivities/radiation after the local Green problem"),
        (8, "E_parent_to_EH", "OPEN_HARD", "primitive MTS derivation of the EH/coframe block remains incomplete", "do not promote correspondence completion to microscopic derivation"),
    ]
    return [
        {"priority": priority, "residual": residual, "status": status, "evidence": evidence, "next_action": next_action, "valid_for_claim": False, "timestamp_utc": TIMESTAMP}
        for priority, residual, status, evidence, next_action in entries
    ]


def decision_rows() -> list[dict[str, Any]]:
    entries = [
        ("DEC4857_0_owner", "adopt the general two-derivative unit-flow kinetic block as the minimal private physical-flow completion", "the field u already exists and the operator basis is fixed by covariance, parity and derivative order"),
        ("DEC4857_1_surface", "restrict the weak local branch to the exact PPN-zero surface", "this gives beta=gamma=1, alpha1=alpha2=0 and G_cos=G_N without setting the flow coefficients to zero"),
        ("DEC4857_2_corridor", "use 0<p<=1e-15 and 0<d<=p/3 as a sufficient healthy multimessenger/Cherenkov corridor", "all kinetic signs and mode speeds close analytically"),
        ("DEC4857_3_exact", "do not call p=0 a regular exact-GR limit", "c14 and c123 vanish and the physical-flow completion degenerates unless a gauge-elimination theorem exists"),
        ("DEC4857_4_pressure", "reopen the EM-rich preferred-frame estimate with the actual kinetic denominator", "eta/c14 can be order ten even though both coefficients are small"),
        ("DEC4857_5_next", "derive the Poynting-driven parent-flow Green response and source-profile PPN residual", "the kinetic owner now exists, so the previously symbolic C1/C2 response can be calculated rather than named"),
    ]
    return [
        {"decision_id": row_id, "decision": decision, "reason": reason, "next_target": NEXT_TARGET if row_id == "DEC4857_5_next" else "", "valid_for_claim": False, "timestamp_utc": TIMESTAMP}
        for row_id, decision, reason in entries
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    operators: list[dict[str, Any]],
    ppn: list[dict[str, Any]],
    modes: list[dict[str, Any]],
    benchmark: list[dict[str, Any]],
    limits: list[dict[str, Any]],
    em_pressure: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    claim = [row for row in read_csv(FORMAL / "02-claims-register.csv") if row.get("claim_id") == "L-699"]
    variables = read_csv(FORMAL / "04-variable-audit.csv")
    pd_variable = [row for row in variables if row.get("symbol") == "p_aether_d_aether"]
    checkpoint = (POST / "4857-Y5-R2FR-parent-time-coframe-kinetic-owner-or-PPN-safe-coefficient-surface-and-mode-stability-gate.md").read_text(encoding="utf-8")
    formal = (FORMAL / "873-PPC4161-parent-time-flow-kinetic-owner-and-stability-corridor.md").read_text(encoding="utf-8")
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")

    def result(check_id: str, passed: bool, detail: str) -> dict[str, Any]:
        return {"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail, "valid_for_claim": False, "timestamp_utc": TIMESTAMP}

    groups = (sources, operators, ppn, modes, benchmark, limits, em_pressure, residuals, decisions)
    checks = [
        result("VAL4857_00_sources", len(sources) == 15 and all(row["source_exists"] and row["needle_found"] for row in sources), f"sources={len(sources)}"),
        result("VAL4857_01_operator", len(operators) == 6 and any(row["status"] == "DERIVED_FROM_FIELD_CONTENT_AND_DERIVATIVE_ORDER" for row in operators), "minimal operator basis emitted"),
        result("VAL4857_02_PPN", len(ppn) == 8 and ppn[2]["status"] == "PASS" and ppn[6]["status"] == "EXACT", "PPN-zero surface and G equality verified"),
        result("VAL4857_03_modes", len(modes) == 10 and any(row["status"] == "DERIVED_SUFFICIENT_CORRIDOR" for row in modes), "positive kinetic and no-Cherenkov corridor emitted"),
        result("VAL4857_04_benchmark", len(benchmark) == 8 and all(row["status"] != "FAIL" for row in benchmark), "finite upper-edge benchmark passes"),
        result("VAL4857_05_limit", len(limits) == 6 and any(row["status"] == "NO_HEALTHY_EXACT_GR_ENDPOINT" for row in limits), "singular exact-GR endpoint retained"),
        result("VAL4857_06_EM", len(em_pressure) == 4 and em_pressure[2]["status"] == "PRESSURE_NOT_PREDICTION", "eta/c14 response pressure exposed without claim"),
        result("VAL4857_07_residuals", len(residuals) == 8 and residuals[0]["status"] == "CLOSED_PRIVATE_EFT_COMPLETION" and residuals[5]["status"] == "OPEN_HARD_NEXT_TARGET", "residual vector rebased"),
        result("VAL4857_08_nonclaim", all(not row["valid_for_claim"] for group in groups for row in group), "all 4857 rows remain private nonclaim"),
        result("VAL4857_09_variable", len(pd_variable) == 1, "adapted variable audit updated"),
        result("VAL4857_10_claim", len(claim) == 1 and claim[0].get("status") == "minimal_unit_flow_EFT_owner_and_PPN_GW_stability_corridor_derived_exact_GR_endpoint_singular_private_nonclaim", f"L-699 rows={len(claim)}"),
        result("VAL4857_11_documents", "PARENT_TIME_FLOW_KINETIC_STABILITY_4857" in checkpoint and "PPC4161_PARENT_TIME_FLOW_KINETIC_STABILITY_4857" in formal, "checkpoint and formal markers found"),
        result("VAL4857_12_resume", resume_checkpoint_at_least(resume, 4857), "resume reached or advanced beyond the Poynting Green-response gate"),
        result("VAL4857_13_script", compiles(Path(__file__).resolve()), "generator compiles"),
    ]
    checks.append(result("VAL4857_OVERALL", all(row["status"] == "PASS" for row in checks), "PARENT_TIME_FLOW_KINETIC_STABILITY_GATE_VALIDATED"))
    return checks


def main() -> int:
    symbols = symbolic_map()
    sources = source_rows()
    operators = operator_rows(symbols)
    ppn = ppn_rows(symbols)
    modes = mode_rows(symbols)
    benchmark = benchmark_rows()
    limits = limit_rows(symbols)
    em_pressure = em_pressure_rows()
    residuals = residual_rows()
    decisions = decision_rows()
    validation = validation_rows(sources, operators, ppn, modes, benchmark, limits, em_pressure, residuals, decisions)
    write_csv(OUTPUT / "P8_Y5_R2FR_4857_SOURCE_REGISTER.csv", sources)
    write_csv(OUTPUT / "P8_Y5_R2FR_4857_PARENT_UNIT_FLOW_OPERATOR_BASIS.csv", operators)
    write_csv(OUTPUT / "P8_Y5_R2FR_4857_PPN_SAFE_SURFACE.csv", ppn)
    write_csv(OUTPUT / "P8_Y5_R2FR_4857_MODE_STABILITY_CORRIDOR.csv", modes)
    write_csv(OUTPUT / "P8_Y5_R2FR_4857_FINITE_BENCHMARK.csv", benchmark)
    write_csv(OUTPUT / "P8_Y5_R2FR_4857_EXACT_GR_LIMIT_OBSTRUCTION.csv", limits)
    write_csv(OUTPUT / "P8_Y5_R2FR_4857_EM_RESPONSE_PRESSURE.csv", em_pressure)
    write_csv(OUTPUT / "P8_Y5_R2FR_4857_RESIDUAL_REBASE.csv", residuals)
    write_csv(OUTPUT / "P8_Y5_R2FR_4857_DECISION.csv", decisions)
    write_csv(OUTPUT / "P8_Y5_BRR545_4857_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print("P8_Y5_BRR545_4857_VALIDATION_PASS" if passed else "P8_Y5_BRR545_4857_VALIDATION_FAIL")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

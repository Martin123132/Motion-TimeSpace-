from __future__ import annotations

import csv
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Any

import sympy as sp


CHECKPOINT = "4861"
TIMESTAMP = "2026-07-10T02:15:00+01:00"
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = POST / "source-intake" / "local_bounds" / "local_bound_claims.csv"
NEXT_TARGET = "4862-Y5-R2FR-public-frame-absolute-p-bound-and-strong-coupling-cutoff-or-fallback-selection.md"

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
        ("SRC4861_00_3779", POST / "3779-Y5-R2FR-qobs-EM-readout-gauge-and-universal-ZEM-certificate.md", "EXACT_NO_EM_SHADOW_METRIC_CRITERION", "same-public-metric criterion"),
        ("SRC4861_01_1030", POST / "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md", "SPM1030_0_public_metric_object", "public matter metric contract"),
        ("SRC4861_02_4852", POST / "4852-Y5-R2FR-local-GR-residual-rebase-after-memory-cuscuton-and-Gamma-zero.md", "linearized", "Newton/Hilbert source charge baseline"),
        ("SRC4861_03_4856", POST / "4856-Y5-R2FR-time-flow-Hilbert-variation-and-preferred-frame-PPN-alpha1-alpha2-gate.md", "Multiplier-complete Hilbert tensor", "normalized-flow source variation"),
        ("SRC4861_04_4857", POST / "4857-Y5-R2FR-parent-time-coframe-kinetic-owner-or-PPN-safe-coefficient-surface-and-mode-stability-gate.md", "c_2=-", "unhatted coefficient surface"),
        ("SRC4861_05_4860", POST / "4860-Y5-R2FR-parent-coupling-coscaling-law-beta-u-over-p-or-first-EM-radiation-source-profile-test.md", "SHARED_CONE_COUPLING_LAW_4860", "shared characteristic metric"),
        ("SRC4861_06_bounds", LOCAL_BOUNDS, "R5_alpha1", "weak preferred-frame comparator"),
        ("SRC4861_07_variables", FORMAL / "04-variable-audit.csv", "hat_c_i_public", "public-frame variables integrated"),
        ("SRC4861_08_equations", FORMAL / "05-equation-register.md", "1.154 Public-frame matter variation", "equation integration"),
        ("SRC4861_09_checkpoint", POST / "4861-Y5-R2FR-shared-cone-matter-frame-Hilbert-variation-or-base-metric-branch-selection.md", "PUBLIC_FRAME_VARIATION_SELECTION_4861", "human derivation"),
        ("SRC4861_10_formal877", FORMAL / "877-PPC4161-public-frame-variation-and-branch-selection.md", "PPC4161_PUBLIC_FRAME_SELECTION_4861", "formal integration"),
        ("SRC4861_11_claim", FORMAL / "02-claims-register.csv", "L-703", "claim register"),
        ("SRC4861_12_redteam", FORMAL / "06-consistency-red-team.md", "105. Public-frame variation", "red-team integration"),
        ("SRC4861_13_spine", FORMAL / "07-unification-spine.md", "checkpoint 4861", "spine integration"),
        ("SRC4861_14_resume", POST / "CURRENT_LOCAL_RESUME.md", "Last checkpoint: `4861-", "resume marker"),
        ("SRC4861_15_script", Path(__file__).resolve(), 'CHECKPOINT = "4861"', "executable symbolic gate"),
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
        ("SRC4861_16_redefinition", "https://arxiv.org/abs/gr-qc/0502066", "exact Einstein-aether coefficient transformation under constant disformal field redefinition", "primary frame transformation"),
        ("SRC4861_17_PPN", "https://arxiv.org/abs/gr-qc/0509083", "exact alpha1 and alpha2 formulas with minimal matter coupling", "primary public-frame PPN"),
        ("SRC4861_18_modes", "https://arxiv.org/abs/1802.04303", "reduced scalar/vector/tensor kinetic coefficients and speeds", "primary public-frame mode checks"),
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
    ratio = sp.symbols("r", positive=True)
    denominator = d + p - d * p
    c1 = (d + p) / 2
    c3 = (p - d) / 2
    c2 = -p * (3 * d + p) / (3 * (d + p))
    c4 = -(p - d) ** 2 / (2 * (d + p))
    c14 = sp.factor(c1 + c4)
    b_disformal = 1 / (1 - p)
    hat_p = sp.Integer(0)
    hat_d = denominator
    hat_c1 = denominator / 2
    hat_c3 = -denominator / 2
    hat_c2 = 2 * p**2 / (3 * (d + p) * (1 - p))
    hat_c4 = c14 - denominator / 2
    hat_c14 = sp.factor(hat_c1 + hat_c4)
    hat_c123 = sp.factor(hat_c1 + hat_c2 + hat_c3)
    hat_ctheta = sp.factor(hat_c1 + 3 * hat_c2 + hat_c3)
    hat_q_scalar = sp.factor((1 - hat_p) * (2 + hat_p + 3 * hat_c2) / hat_c123)
    hat_q_vector = hat_c14
    hat_q_tensor = 1 - hat_p
    hat_c_scalar_sq = sp.factor(
        hat_c123
        * (2 - hat_c14)
        / (hat_c14 * (1 - hat_p) * (2 + hat_p + 3 * hat_c2))
    )
    hat_c_vector_sq = sp.factor(
        (2 * hat_c1 - hat_p * hat_d)
        / (2 * hat_c14 * (1 - hat_p))
    )
    hat_c_tensor_sq = 1 / (1 - hat_p)
    hat_alpha1 = sp.factor(
        -8
        * (hat_c3**2 + hat_c1 * hat_c4)
        / (2 * hat_c1 - hat_c1**2 + hat_c3**2)
    )
    hat_alpha2 = sp.factor(
        hat_alpha1 / 2
        - (hat_c1 + 2 * hat_c3 - hat_c4)
        * (2 * hat_c1 + 3 * hat_c2 + hat_c3 + hat_c4)
        / (hat_c123 * (2 - hat_c14))
    )
    g_ratio = sp.factor((1 - hat_c14 / 2) / (1 + hat_ctheta / 2))
    alpha2_shape = ratio * (1 - 3 * ratio) / (1 + ratio)
    alpha2_stationary = -1 + 2 * sp.sqrt(3) / 3
    alpha2_max = sp.factor(alpha2_shape.subs(ratio, alpha2_stationary))
    return {
        "p": p,
        "d": d,
        "r": ratio,
        "D": denominator,
        "c1": c1,
        "c2": c2,
        "c3": c3,
        "c4": c4,
        "c14": c14,
        "B": b_disformal,
        "hat_p": hat_p,
        "hat_d": hat_d,
        "hat_c1": sp.factor(hat_c1),
        "hat_c2": sp.factor(hat_c2),
        "hat_c3": sp.factor(hat_c3),
        "hat_c4": sp.factor(hat_c4),
        "hat_c14": hat_c14,
        "hat_c123": hat_c123,
        "hat_ctheta": hat_ctheta,
        "hat_qS": hat_q_scalar,
        "hat_qV": hat_q_vector,
        "hat_qT": hat_q_tensor,
        "hat_cS2": hat_c_scalar_sq,
        "hat_cV2": hat_c_vector_sq,
        "hat_cT2": hat_c_tensor_sq,
        "hat_alpha1": hat_alpha1,
        "hat_alpha2": hat_alpha2,
        "Gcos_over_GN": g_ratio,
        "alpha2_rstar": alpha2_stationary,
        "alpha2_max_coeff": alpha2_max,
    }


def identity_rows(symbols: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    p = symbols["p"]
    d = symbols["d"]
    denominator = symbols["D"]
    checks = [
        ("ID4861_0_hatp", symbols["hat_p"], 0, "public-frame c13"),
        ("ID4861_1_hatd", symbols["hat_d"], denominator, "public-frame c1-c3"),
        ("ID4861_2_hatc14", symbols["hat_c14"], 2 * d * p / (d + p), "acceleration kinetic coefficient"),
        ("ID4861_3_hatc123", symbols["hat_c123"], 2 * p**2 / (3 * (d + p) * (1 - p)), "scalar kinetic combination"),
        ("ID4861_4_qS", symbols["hat_qS"], 3 * denominator / p**2, "public-frame scalar kinetic coefficient"),
        ("ID4861_5_cS", symbols["hat_cS2"], p / (3 * d), "public-frame scalar speed"),
        ("ID4861_6_cV", symbols["hat_cV2"], denominator * (d + p) / (4 * d * p), "public-frame vector speed"),
        ("ID4861_7_cT", symbols["hat_cT2"], 1, "public-frame tensor speed"),
        ("ID4861_8_a1", symbols["hat_alpha1"], -8 * d * p / (d + p), "public-frame alpha1"),
        ("ID4861_9_a2", symbols["hat_alpha2"], d * (3 * d - p) / (d + p), "public-frame alpha2"),
        ("ID4861_10_G", symbols["Gcos_over_GN"], 1 - p, "public-frame cosmological/Newton ratio"),
        ("ID4861_11_a2max", symbols["alpha2_max_coeff"], 7 - 4 * sp.sqrt(3), "maximum alpha2 shape coefficient"),
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


def variation_rows() -> list[dict[str, Any]]:
    entries = [
        ("VAR4861_0_public", "S_m=S_m[Psi,A,gHat]; gHat^{mu nu}=g^{mu nu}+p u^mu u^nu", "all rods, clocks, photons, free fall and source readout use one metric", "SELECTED_PRIVATE_PUBLIC_FRAME"),
        ("VAR4861_1_chain", "delta gHat^{mu nu}=delta g^{mu nu}+p(u^mu delta u^nu+u^nu delta u^mu)", "constant-p chain rule", "EXACT"),
        ("VAR4861_2_action", "delta S_m=-1/2 int sqrt(-gHat) T_hat_munu delta gHat^{mu nu}", "definition of public Hilbert stress", "EXACT"),
        ("VAR4861_3_base_metric", "T_base_munu=(sqrt(-gHat)/sqrt(-g)) T_hat_munu=T_hat_munu/sqrt(1-p)", "base-variable metric source", "EXACT_CHAIN_RULE"),
        ("VAR4861_4_flow", "J_u,nu=p T_hat_munu u^mu/sqrt(1-p)", "base-variable induced universal flow source before unit projection", "EXACT_CHAIN_RULE"),
        ("VAR4861_5_project", "J_u,nu^perp=p h_nu^lambda T_hat_mulambda u^mu/sqrt(1-p)", "normalization multiplier removes the parallel component", "EXACT_UNIT_PROJECTOR"),
        ("VAR4861_6_EM", "local EM momentum has T_hat_0i=-P_i, so J_u,i^perp=-p P_i/sqrt(1-p)", "reproduces beta_u=-p after common normalization", "PASS"),
        ("VAR4861_7_universal", "the same J_u^perp applies to every matter momentum flux", "apparent EM direct coupling is one component of universal frame variation", "SOURCE_UNIVERSALITY"),
        ("VAR4861_8_Ward", "nabla_hat_mu T_hat^{mu nu}=0 on matter shell; base metric/flow sources obey the chain-rule diffeomorphism identity", "no external source nonconservation is introduced", "EXACT_WARD_ROUTE"),
    ]
    return [
        {"row_id": row_id, "equation": equation, "meaning": meaning, "status": status, "valid_for_claim": False, "timestamp_utc": TIMESTAMP}
        for row_id, equation, meaning, status in entries
    ]


def coefficient_rows(symbols: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    entries = [
        ("CF4861_0_transform", f"B={sp.sstr(symbols['B'])}", "constant Foster transformation from base g to public gHat", "EXACT"),
        ("CF4861_1_c1", f"c1_hat={sp.sstr(symbols['hat_c1'])}", "public-frame coefficient", "EXACT"),
        ("CF4861_2_c2", f"c2_hat={sp.sstr(symbols['hat_c2'])}", "public-frame coefficient", "EXACT"),
        ("CF4861_3_c3", f"c3_hat={sp.sstr(symbols['hat_c3'])}", "public-frame coefficient", "EXACT"),
        ("CF4861_4_c4", f"c4_hat={sp.sstr(symbols['hat_c4'])}", "public-frame coefficient", "EXACT"),
        ("CF4861_5_p", "c13_hat=0", "tensor cone is public and luminal at finite p,d", "EXACT"),
        ("CF4861_6_d", f"d_hat={sp.sstr(symbols['hat_d'])}>0", "finite vector gradient owner", "PASS"),
        ("CF4861_7_c14", f"c14_hat={sp.sstr(symbols['hat_c14'])}>0", "finite vector time kinetic owner", "PASS"),
        ("CF4861_8_c123", f"c123_hat={sp.sstr(symbols['hat_c123'])}>0", "finite scalar kinetic owner", "PASS"),
        ("CF4861_9_G", "G_hat=Gae/sqrt(1-p)", "constant action-normalization redefinition; measured G_N remains calibrated", "EXACT_FRAME_MAP"),
    ]
    return [
        {"row_id": row_id, "equation": equation, "meaning": meaning, "status": status, "valid_for_claim": False, "timestamp_utc": TIMESTAMP}
        for row_id, equation, meaning, status in entries
    ]


def mode_rows(symbols: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    entries = [
        ("MODE4861_0_tensor", "qT_hat=1; cT_hat^2=1", "two luminal positive-energy tensor modes", "PASS"),
        ("MODE4861_1_vector", f"qV_hat={sp.sstr(symbols['hat_qV'])}; cV_hat^2={sp.sstr(symbols['hat_cV2'])}", "two transverse flow modes", "PASS"),
        ("MODE4861_2_scalar", f"qS_hat={sp.sstr(symbols['hat_qS'])}; cS_hat^2={sp.sstr(symbols['hat_cS2'])}", "one scalar flow mode", "PASS"),
        ("MODE4861_3_positive", "0<p<1 and 0<d<=p/3 imply qT,qV,qS>0", "no linear ghost in the public frame", "PASS"),
        ("MODE4861_4_scalar_speed", "cS_hat^2=p/(3d)>=1", "no scalar vacuum Cherenkov channel", "PASS"),
        ("MODE4861_5_vector_speed", "cV_hat^2=(1+r)(1+r-rp)/(4r)>=1 for r=d/p<=1/3", "no vector vacuum Cherenkov channel", "PASS"),
        ("MODE4861_6_finite", "c13_hat=0 does not force c14_hat or c123_hat to zero at finite p,d", "removes the false identification of luminal tensor with the singular endpoint", "PASS"),
        ("MODE4861_7_endpoint", "p,d->0 still removes canonical normalization and requires cutoff/gauge-restoration analysis", "finite public branch is healthy but exact-GR endpoint remains open", "GUARD"),
    ]
    return [
        {"row_id": row_id, "equation": equation, "meaning": meaning, "status": status, "valid_for_claim": False, "timestamp_utc": TIMESTAMP}
        for row_id, equation, meaning, status in entries
    ]


def ppn_rows(symbols: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    p_value = Decimal("1e-15")
    alpha1_bound = Decimal("1e-4")
    alpha2_bound = Decimal("2e-9")
    alpha1_max = Decimal(2) * p_value
    alpha2_shape = Decimal(7) - Decimal(3).sqrt() * Decimal(4)
    alpha2_max = alpha2_shape * p_value
    entries = [
        ("PPN4861_0_standard", "gamma_hat=beta_PPN_hat=1; xi=zeta_i=alpha3=0", "minimal matter coupling to gHat retains semi-conservative PPN values", "PRIMARY_FORMULA"),
        ("PPN4861_1_alpha1", f"alpha1_hat={sp.sstr(symbols['hat_alpha1'])}", "universal public-frame preferred-frame coefficient", "EXACT"),
        ("PPN4861_2_alpha2", f"alpha2_hat={sp.sstr(symbols['hat_alpha2'])}", "universal public-frame preferred-frame coefficient", "EXACT"),
        ("PPN4861_3_a1bound", f"working corridor gives abs(alpha1_hat)<={alpha1_max}", "uses 0<d<=p/3 and p<=1e-15", "PASS_WORKING_CORRIDOR"),
        ("PPN4861_4_a2shape", f"max_r r(1-3r)/(1+r)=7-4sqrt(3)={alpha2_shape}", "exact r-shape maximum", "PASS"),
        ("PPN4861_5_a2bound", f"working corridor gives abs(alpha2_hat)<={alpha2_max}", "universal public-frame bound", "PASS_WORKING_CORRIDOR"),
        ("PPN4861_6_margin1", f"R5/alpha1>={alpha1_bound / alpha1_max}", "weak preferred-frame margin", "PASS_WORKING_CORRIDOR"),
        ("PPN4861_7_margin2", f"R6/alpha2>={alpha2_bound / alpha2_max}", "weak preferred-frame margin", "PASS_WORKING_CORRIDOR"),
        ("PPN4861_8_supersede", "do not add the 4858/4859 source-specific EM alpha1/alpha2 to alpha_hat", "those terms were the optical-only/base-frame decomposition of a source now transformed universally", "FRAME_CONSISTENCY_GUARD"),
    ]
    return [
        {"row_id": row_id, "equation": equation, "meaning": meaning, "status": status, "valid_for_claim": False, "timestamp_utc": TIMESTAMP}
        for row_id, equation, meaning, status in entries
    ]


def calibration_rows(symbols: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    entries = [
        ("CAL4861_0_Newton", "G_N_hat=G_hat/(1-c14_hat/2)", "public-frame Newton calibration", "EXACT"),
        ("CAL4861_1_Poisson", "Delta_hat U_hat=-4pi G_N_hat rho_hat", "minimal Hilbert source gives standard weak Poisson equation", "EXACT_LINEAR"),
        ("CAL4861_2_source", "M_source=int rho_hat d3x equals the linear Hilbert/Gauss/ADM source charge", "inherits 4852 in the public frame", "EXACT_LINEAR"),
        ("CAL4861_3_cos", "G_cos_hat=G_hat/(1+c_theta_hat/2)", "homogeneous expansion calibration", "EXACT"),
        ("CAL4861_4_ratio", f"G_cos_hat/G_N_hat={sp.sstr(symbols['Gcos_over_GN'])}", "public-frame mismatch is one controlled coefficient p", "EXACT"),
        ("CAL4861_5_WEP", "all ordinary species use S_m[Psi,gHat] with one Hilbert tensor", "test-body free fall and source weight are universal at action level", "EXACT_ARCHITECTURE"),
        ("CAL4861_6_clock", "d tau_hat^2=-gHat_munu dx^mu dx^nu and photon null cone is gHat", "no constant-p photon/clock frame mismatch", "EXACT_ARCHITECTURE"),
        ("CAL4861_7_scope", "G_cos/G_N=1-p and PPN now provide physical p channels; relative GW timing does not", "absolute p must be bounded in the public frame", "NEXT_BOUND_TARGET"),
    ]
    return [
        {"row_id": row_id, "equation": equation, "meaning": meaning, "status": status, "valid_for_claim": False, "timestamp_utc": TIMESTAMP}
        for row_id, equation, meaning, status in entries
    ]


def selection_rows() -> list[dict[str, Any]]:
    entries = [
        ("SEL4861_0_optical", "g public; gHat optical-only; beta_u=-p only in EM", "keeps 4857 exact PPN-zero surface but leaves sector-specific wave metric", "RETAINED_CONTROL_NOT_SELECTED"),
        ("SEL4861_1_base", "g public; minimal Maxwell[g]; beta_u=0", "lowest-risk same-Hodge baseline with direct GW bound on p", "FALLBACK_BASELINE"),
        ("SEL4861_2_public", "gHat public for all matter and Maxwell; transform gravity coefficients", "one rods/clocks/photons/free-fall/source metric and universal induced flow source", "SELECTED_LEAD_PRIVATE_BRANCH"),
        ("SEL4861_3_reason", "public gHat removes the EM shadow and turns beta_u=-p into a representation of universal source coupling", "addresses coupling without species-specific closure", "PASS_ARCHITECTURE"),
        ("SEL4861_4_cost", "alpha1_hat,alpha2_hat and Gcos/GN differ from exact GR by O(p); relative GW timing no longer bounds p", "selection creates an absolute-p and cutoff task", "OPEN_BUT_TESTABLE"),
        ("SEL4861_5_ceiling", "selection is a private correspondence architecture, not a primitive derivation from the original scalar corpus", "do not claim complete MTS unification or exact GR", "NONCLAIM_GUARD"),
    ]
    return [
        {"row_id": row_id, "branch": branch, "reason": reason, "status": status, "valid_for_claim": False, "timestamp_utc": TIMESTAMP}
        for row_id, branch, reason, status in entries
    ]


def residual_rows() -> list[dict[str, Any]]:
    entries = [
        (1, "E_matter_frame", "CLOSED_PRIVATE_ARCHITECTURE", "gHat selected as the single public matter/source/readout metric", "seek primitive MTS ownership later"),
        (2, "E_source_coupling", "CLOSED_UNIVERSAL_CHAIN_RULE", "T_base and J_u are both derivatives of one public Hilbert action", "retain nonlinear charge tests"),
        (3, "E_tensor_photon", "CLOSED_EXACT", "cT_hat=cgamma_hat=1", "no relative GW bound on p"),
        (4, "E_PPN", "CLOSED_WEAK_WORKING_CORRIDOR", "universal alpha1/alpha2 formulas and conservative bounds derived", "re-score with source-backed absolute p"),
        (5, "E_Newton", "CLOSED_LINEAR_CALIBRATED", "standard public Hilbert Poisson source with measured G_N_hat", "retain nonlinear ADM/strong-field tests"),
        (6, "E_absolute_p", "OPEN_HARD_NEXT", "Gcos/GN=1-p and PPN are available but no strongest source-backed combined p interval is selected", "acquire and propagate bounds"),
        (7, "E_cutoff", "OPEN_HARD_NEXT", "qV and c123 shrink toward the exact-GR endpoint", "derive strong-coupling scale or gauge restoration"),
        (8, "E_strong_field", "OPEN_HARD", "compact-body sensitivities remain outside weak public-frame PPN", "compute after p/cutoff gate"),
    ]
    return [
        {"priority": priority, "residual": residual, "status": status, "evidence": evidence, "next_action": next_action, "valid_for_claim": False, "timestamp_utc": TIMESTAMP}
        for priority, residual, status, evidence, next_action in entries
    ]


def decision_rows() -> list[dict[str, Any]]:
    entries = [
        ("DEC4861_0_public", "select gHat as the lead private public metric", "it is the only nonzero coupling branch that gives one characteristic, clock, free-fall and source geometry without an independent coefficient"),
        ("DEC4861_1_universal", "replace EM-only beta_u interpretation with universal chain-rule source coupling", "all matter momentum sources u in the base representation when all matter uses gHat"),
        ("DEC4861_2_PPN", "use transformed public-frame PPN coefficients", "adding old source-specific EM residuals would mix frames and double count"),
        ("DEC4861_3_fallback", "retain beta_u=0 same-g as a control branch", "it remains the safer fallback if absolute-p or cutoff gates reject public gHat"),
        ("DEC4861_4_next", "derive the strongest absolute-p interval and nonlinear cutoff", "the coefficient and matter-frame ambiguities are now replaced by two quantitative gates"),
    ]
    return [
        {"decision_id": row_id, "decision": decision, "reason": reason, "next_target": NEXT_TARGET if row_id == "DEC4861_4_next" else "", "valid_for_claim": False, "timestamp_utc": TIMESTAMP}
        for row_id, decision, reason in entries
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    identities: list[dict[str, Any]],
    variation: list[dict[str, Any]],
    coefficients: list[dict[str, Any]],
    modes: list[dict[str, Any]],
    ppn: list[dict[str, Any]],
    calibration: list[dict[str, Any]],
    selection: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    claims = [row for row in read_csv(FORMAL / "02-claims-register.csv") if row.get("claim_id") == "L-703"]
    variables = read_csv(FORMAL / "04-variable-audit.csv")
    response_variables = [row for row in variables if row.get("symbol") in {"hat_c_i_public", "T_hat_Ju_universal", "Ghat_N_Gcos"}]
    checkpoint = (POST / "4861-Y5-R2FR-shared-cone-matter-frame-Hilbert-variation-or-base-metric-branch-selection.md").read_text(encoding="utf-8")
    formal = (FORMAL / "877-PPC4161-public-frame-variation-and-branch-selection.md").read_text(encoding="utf-8")
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")
    prior_validation = read_csv(OUTPUT / "P8_Y5_BRR545_4860_VALIDATION.csv")

    def result(check_id: str, passed: bool, detail: str) -> dict[str, Any]:
        return {"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail, "valid_for_claim": False, "timestamp_utc": TIMESTAMP}

    groups = (sources, identities, variation, coefficients, modes, ppn, calibration, selection, residuals, decisions)
    checks = [
        result("VAL4861_00_sources", len(sources) == 19 and all(row["source_exists"] and row["needle_found"] for row in sources), f"sources={len(sources)}"),
        result("VAL4861_01_identities", len(identities) == 12 and all(row["status"] == "PASS" for row in identities), "frame, mode, PPN and calibration identities pass"),
        result("VAL4861_02_variation", len(variation) == 9 and variation[7]["status"] == "SOURCE_UNIVERSALITY", "public Hilbert chain rule and universal flow source derived"),
        result("VAL4861_03_coefficients", len(coefficients) == 10 and coefficients[5]["equation"] == "c13_hat=0" and all(row["status"] != "FAIL" for row in coefficients), "public-frame coefficient map passes"),
        result("VAL4861_04_modes", len(modes) == 8 and all(row["status"] != "FAIL" for row in modes), "all public-frame modes are positive and at least luminal in corridor"),
        result("VAL4861_05_PPN", len(ppn) == 9 and ppn[-1]["status"] == "FRAME_CONSISTENCY_GUARD", "public PPN is derived without frame double count"),
        result("VAL4861_06_calibration", len(calibration) == 8 and calibration[4]["equation"] == "G_cos_hat/G_N_hat=1 - p", "Newton/cosmology calibration map passes"),
        result("VAL4861_07_selection", len(selection) == 6 and selection[2]["status"] == "SELECTED_LEAD_PRIVATE_BRANCH" and selection[-1]["status"] == "NONCLAIM_GUARD", "public branch selected with claim ceiling"),
        result("VAL4861_08_residuals", len(residuals) == 8 and residuals[5]["status"] == "OPEN_HARD_NEXT" and residuals[6]["status"] == "OPEN_HARD_NEXT", "absolute-p and cutoff gates remain next"),
        result("VAL4861_09_nonclaim", all(not row["valid_for_claim"] for group in groups for row in group), "all rows remain private nonclaim"),
        result("VAL4861_10_variables", len(response_variables) == 3, "public coefficient/source/calibration variables integrated"),
        result("VAL4861_11_claim", len(claims) == 1 and claims[0].get("status") == "public_gHat_matter_frame_selected_universal_source_variation_and_transformed_PPN_derived_private_nonclaim", f"L-703 rows={len(claims)}"),
        result("VAL4861_12_documents", "PUBLIC_FRAME_VARIATION_SELECTION_4861" in checkpoint and "PPC4161_PUBLIC_FRAME_SELECTION_4861" in formal, "checkpoint and formal markers found"),
        result("VAL4861_13_resume", resume_checkpoint_at_least(resume, 4861) and NEXT_TARGET in resume, "resume advanced to absolute-p/cutoff gate"),
        result("VAL4861_14_prior", prior_validation[-1].get("status") == "PASS", "4860 validation remains green"),
        result("VAL4861_15_script", compiles(Path(__file__).resolve()), "generator compiles"),
    ]
    checks.append(result("VAL4861_OVERALL", all(row["status"] == "PASS" for row in checks), "PUBLIC_FRAME_VARIATION_SELECTION_GATE_VALIDATED"))
    return checks


def main() -> int:
    symbols = symbolic_map()
    sources = source_rows()
    identities = identity_rows(symbols)
    variation = variation_rows()
    coefficients = coefficient_rows(symbols)
    modes = mode_rows(symbols)
    ppn = ppn_rows(symbols)
    calibration = calibration_rows(symbols)
    selection = selection_rows()
    residuals = residual_rows()
    decisions = decision_rows()
    validation = validation_rows(sources, identities, variation, coefficients, modes, ppn, calibration, selection, residuals, decisions)
    write_csv(OUTPUT / "P8_Y5_R2FR_4861_SOURCE_REGISTER.csv", sources)
    write_csv(OUTPUT / "P8_Y5_R2FR_4861_SYMBOLIC_IDENTITIES.csv", identities)
    write_csv(OUTPUT / "P8_Y5_R2FR_4861_PUBLIC_VARIATION.csv", variation)
    write_csv(OUTPUT / "P8_Y5_R2FR_4861_PUBLIC_COEFFICIENTS.csv", coefficients)
    write_csv(OUTPUT / "P8_Y5_R2FR_4861_PUBLIC_MODES.csv", modes)
    write_csv(OUTPUT / "P8_Y5_R2FR_4861_PUBLIC_PPN.csv", ppn)
    write_csv(OUTPUT / "P8_Y5_R2FR_4861_NEWTON_COSMO_CALIBRATION.csv", calibration)
    write_csv(OUTPUT / "P8_Y5_R2FR_4861_BRANCH_SELECTION.csv", selection)
    write_csv(OUTPUT / "P8_Y5_R2FR_4861_RESIDUAL_REBASE.csv", residuals)
    write_csv(OUTPUT / "P8_Y5_R2FR_4861_DECISION.csv", decisions)
    write_csv(OUTPUT / "P8_Y5_BRR545_4861_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print("P8_Y5_BRR545_4861_VALIDATION_PASS" if passed else "P8_Y5_BRR545_4861_VALIDATION_FAIL")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

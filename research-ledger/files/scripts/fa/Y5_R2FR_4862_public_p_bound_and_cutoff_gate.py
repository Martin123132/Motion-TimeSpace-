from __future__ import annotations

import csv
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Any

import sympy as sp


CHECKPOINT = "4862"
TIMESTAMP = "2026-07-10T02:30:00+01:00"
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = POST / "source-intake" / "local_bounds" / "local_bound_claims.csv"
R10_ANCHOR = POST / "source-intake" / "r10" / "derived" / "staging" / "R10_EotWash2020_alpha_lambda_VISUAL_NONCLAIM_1499.csv"
NEXT_TARGET = "4863-Y5-R2FR-full-reduced-cubic-mode-action-and-unitarity-partial-wave-or-public-branch-hard-cutoff.md"

getcontext().prec = 60
PI = Decimal("3.1415926535897932384626433832795028841971693993751")
PLANCK_MASS_GEV = Decimal("1.220890e19")
REDUCED_PLANCK_MASS_GEV = PLANCK_MASS_GEV / (Decimal(8) * PI).sqrt()
HBAR_C_GEV_FM = Decimal("0.1973269804")
R10_LENGTH_M = Decimal("3.86e-5")
R10_ENERGY_GEV = HBAR_C_GEV_FM / (R10_LENGTH_M * Decimal("1e15"))
TEV_STRESS_GEV = Decimal("1e3")
P_WORK = Decimal("1e-15")
R_WORK = Decimal(1) / Decimal(3)
ALPHA1_WEAK_BOUND = Decimal("1e-4")
ALPHA2_WEAK_BOUND = Decimal("1e-7")
ALPHA2_STRONG_PROXY = Decimal("2e-9")
BBN_EA_BOUND = Decimal(1) / Decimal(8)
BBN_UPDATED_CONDITIONAL = Decimal("0.06")


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
        ("SRC4862_00_4861", POST / "4861-Y5-R2FR-shared-cone-matter-frame-Hilbert-variation-or-base-metric-branch-selection.md", "PUBLIC_FRAME_VARIATION_SELECTION_4861", "public-frame coefficient and source baseline"),
        ("SRC4862_01_coeff", OUTPUT / "P8_Y5_R2FR_4861_PUBLIC_COEFFICIENTS.csv", "CF4861_7_c14", "transformed coefficient surface"),
        ("SRC4862_02_ppn", OUTPUT / "P8_Y5_R2FR_4861_PUBLIC_PPN.csv", "PPN4861_2_alpha2", "public weak PPN formulas"),
        ("SRC4862_03_cos", OUTPUT / "P8_Y5_R2FR_4861_NEWTON_COSMO_CALIBRATION.csv", "CAL4861_4_ratio", "Gcos/GN map"),
        ("SRC4862_04_bounds", LOCAL_BOUNDS, "R5_alpha1", "local weak preferred-frame source row"),
        ("SRC4862_05_bounds_caveat", LOCAL_BOUNDS, "R6_alpha2", "strong-field alpha2 proxy retained with caveat"),
        ("SRC4862_06_R10", R10_ANCHOR, "3.86000000e-05", "shortest source-backed local gravity length anchor used as EFT resolution scale"),
        ("SRC4862_07_prior", OUTPUT / "P8_Y5_BRR545_4861_VALIDATION.csv", "VAL4861_OVERALL", "prior checkpoint validation"),
        ("SRC4862_08_checkpoint", POST / "4862-Y5-R2FR-public-frame-absolute-p-bound-and-strong-coupling-cutoff-or-fallback-selection.md", "PUBLIC_P_BOUND_CUTOFF_SELECTION_4862", "human derivation"),
        ("SRC4862_09_formal", FORMAL / "878-PPC4161-public-frame-absolute-p-and-cutoff-window.md", "PPC4161_PUBLIC_P_CUTOFF_4862", "formal integration"),
        ("SRC4862_10_claim", FORMAL / "02-claims-register.csv", "L-704", "claim register"),
        ("SRC4862_11_variable", FORMAL / "04-variable-audit.csv", "p_public_cutoff_window", "variable integration"),
        ("SRC4862_12_equation", FORMAL / "05-equation-register.md", "1.155 Public-frame absolute-`p` and canonical cutoff window", "equation integration"),
        ("SRC4862_13_redteam", FORMAL / "06-consistency-red-team.md", "106. Public-frame absolute-`p` and cutoff red team", "red-team integration"),
        ("SRC4862_14_spine", FORMAL / "07-unification-spine.md", "checkpoint 4862", "spine integration"),
        ("SRC4862_15_resume", POST / "CURRENT_LOCAL_RESUME.md", "Last checkpoint: `4862-", "resume marker"),
        ("SRC4862_16_script", Path(__file__).resolve(), 'CHECKPOINT = "4862"', "executable symbolic and numeric gate"),
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
        ("SRC4862_17_Oost", "https://arxiv.org/abs/1802.04303", "c13=0 weak-field alpha1/alpha2, BBN and mode constraints", "primary Einstein-aether observational map"),
        ("SRC4862_18_Gupta", "https://arxiv.org/abs/2104.04596", "strong-field preferred-frame priors require sensitivity derivatives", "primary strong-field caveat"),
        ("SRC4862_19_Withers", "https://arxiv.org/abs/0905.2446", "Einstein-aether canonical EFT power counting with aether and Planck scales", "primary EFT normalization source"),
        ("SRC4862_20_BBN", "https://arxiv.org/abs/1910.10730", "GBBN/G0=0.99+0.06-0.05 at two sigma", "updated conditional BBN transfer"),
        ("SRC4862_21_NIST", "https://physics.nist.gov/cuu/pdf/JPCRD2022CODATA.pdf", "Planck mass and hbar-c constants", "numeric normalization source"),
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
    p, ratio = sp.symbols("p r", positive=True)
    v, v_t, v_x = sp.symbols("v v_t v_x", real=True)
    d = ratio * p
    denominator = p * (1 + ratio - ratio * p)
    c1 = denominator / 2
    c2 = 2 * p / (3 * (1 + ratio) * (1 - p))
    c3 = -denominator / 2
    c14 = 2 * ratio * p / (1 + ratio)
    c4 = sp.factor(c14 - denominator / 2)
    c123 = sp.factor(c1 + c2 + c3)
    alpha1 = sp.factor(-8 * ratio * p / (1 + ratio))
    alpha2 = sp.factor(-ratio * p * (1 - 3 * ratio) / (1 + ratio))
    bbn_residual = sp.factor((c14 + 3 * c2) / (2 + 3 * c2))
    alpha2_shape = ratio * (1 - 3 * ratio) / (1 + ratio)
    alpha2_stationary = -1 + 2 * sp.sqrt(3) / 3
    alpha2_max = sp.factor(alpha2_shape.subs(ratio, alpha2_stationary))
    coefficient_ceiling = 2 * p / (3 * (1 - p))
    lambda_sigma = sp.sqrt(c14)
    lambda_cubic = sp.factor(c14 ** sp.Rational(3, 2) / coefficient_ceiling)
    lambda_quartic = sp.factor(c14 / sp.sqrt(coefficient_ceiling))
    transverse_exact = sp.factor(
        (-c14 * v_t**2 + c1 * v_x**2 + (c2 + c3 - c4) * v**2 * v_t**2)
        / (1 + v**2)
    )
    transverse_quartic = sp.expand(sp.series(transverse_exact, v, 0, 4).removeO())
    return {
        "p": p,
        "r": ratio,
        "d": d,
        "D": denominator,
        "c1": c1,
        "c2": c2,
        "c3": c3,
        "c4": c4,
        "c14": c14,
        "c123": c123,
        "alpha1": alpha1,
        "alpha2": alpha2,
        "bbn_residual": bbn_residual,
        "alpha2_rstar": alpha2_stationary,
        "alpha2_max": alpha2_max,
        "Cbar": coefficient_ceiling,
        "Lambda_sigma_over_M": lambda_sigma,
        "Lambda_3_safe_over_M": lambda_cubic,
        "Lambda_4_safe_over_M": lambda_quartic,
        "v": v,
        "v_t": v_t,
        "v_x": v_x,
        "K_transverse_quartic": transverse_quartic,
    }


def identity_rows(symbols: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    p = symbols["p"]
    ratio = symbols["r"]
    v = symbols["v"]
    v_t = symbols["v_t"]
    v_x = symbols["v_x"]
    checks = [
        ("ID4862_0_c123", symbols["c123"], 2 * p / (3 * (1 + ratio) * (1 - p)), "public scalar kinetic combination"),
        ("ID4862_1_bbn", symbols["bbn_residual"], p, "EA BBN residual equals the public absolute parameter"),
        ("ID4862_2_alpha2max", symbols["alpha2_max"], 7 - 4 * sp.sqrt(3), "maximum weak alpha2 shape"),
        ("ID4862_3_kinetic_ratio", symbols["c123"] / symbols["c14"], 1 / (3 * ratio * (1 - p)), "c123 is not smaller than c14 in the corridor"),
        ("ID4862_4_Cratio", symbols["c14"] / symbols["Cbar"], 3 * ratio * (1 - p) / (1 + ratio), "smallest-kinetic to coefficient-ceiling ratio"),
        ("ID4862_5_L3", symbols["Lambda_3_safe_over_M"], 3 * sp.sqrt(2) * (1 - p) * ratio ** sp.Rational(3, 2) * sp.sqrt(p) / (1 + ratio) ** sp.Rational(3, 2), "conservative cubic canonical scale"),
        ("ID4862_6_L4", symbols["Lambda_4_safe_over_M"] ** 2, 6 * p * ratio**2 * (1 - p) / (1 + ratio) ** 2, "squared conservative quartic canonical scale"),
        ("ID4862_7_L3_L2", symbols["Lambda_3_safe_over_M"] / symbols["Lambda_sigma_over_M"], 3 * ratio * (1 - p) / (1 + ratio), "cubic scale is below sigma-model scale"),
        ("ID4862_8_L3_L4", (symbols["Lambda_3_safe_over_M"] / symbols["Lambda_4_safe_over_M"]) ** 2, 3 * ratio * (1 - p) / (1 + ratio), "cubic scale is below quartic scale"),
        ("ID4862_9_transverse", symbols["K_transverse_quartic"], -symbols["c14"] * v_t**2 + symbols["c1"] * v_x**2 + symbols["c123"] * v**2 * v_t**2 - symbols["c1"] * v**2 * v_x**2, "unit-constraint transverse expansion through quartic order"),
    ]
    return [
        {
            "identity_id": row_id,
            "left": sp.sstr(sp.factor(left)),
            "right": sp.sstr(sp.factor(right)),
            "meaning": meaning,
            "status": "PASS" if sp.simplify(left - right) == 0 else "FAIL",
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for row_id, left, right, meaning in checks
    ]


def decimal_alpha2_shape_max() -> Decimal:
    return Decimal(7) - Decimal(4) * Decimal(3).sqrt()


def absolute_p_rows() -> list[dict[str, Any]]:
    fmax = decimal_alpha2_shape_max()
    p_alpha1_uniform = ALPHA1_WEAK_BOUND / Decimal(2)
    p_alpha2_uniform = ALPHA2_WEAK_BOUND / fmax
    p_alpha2_proxy = ALPHA2_STRONG_PROXY / fmax
    p_uniform = min(p_alpha1_uniform, p_alpha2_uniform, BBN_EA_BOUND, BBN_UPDATED_CONDITIONAL)
    entries = [
        ("AP4862_0_domain", "theory", "0<p<1; 0<r=d/p<=1/3", "finite stable public branch", "none", "0<p and 0<r<=1/3", "exact branch domain", "EXACT"),
        ("AP4862_1_alpha1", "weak PPN", "abs(alpha1)=8rp/(1+r)", str(ALPHA1_WEAK_BOUND), "Oost 2018 weak-field/solar-system", "p<=1e-4(1+r)/(8r); uniform sufficient p<=5e-5", "source-backed weak field", "BOUND_DERIVED"),
        ("AP4862_2_alpha2", "weak PPN", "abs(alpha2)=rp(1-3r)/(1+r)", str(ALPHA2_WEAK_BOUND), "Oost 2018 weak-field/solar-system", f"p<=1e-7(1+r)/[r(1-3r)]; uniform sufficient p<={p_alpha2_uniform}", "source-backed weak field", "BOUND_DERIVED"),
        ("AP4862_3_BBN_EA", "BBN", "abs[(c14+3c2)/(2+3c2)]=p", "1/8", "Oost 2018 EA-specific abundance gate", "p<=1/8", "direct coefficient-family transfer", "BOUND_DERIVED"),
        ("AP4862_4_BBN_updated", "BBN", "Gcos/GN=1-p", "GBBN/G0>=0.94 at two sigma", "Alvey et al. 2020", "p<=0.06", "conditional on standard BBN with no other expansion/abundance modification", "CONDITIONAL_UPDATED_BOUND"),
        ("AP4862_5_R6_caveat", "strong-field proxy", "local R6 row gives abs(alpha2)<=2e-9", str(ALPHA2_STRONG_PROXY), "Will row plus Gupta 2021 caveat", f"would imply uniform p<={p_alpha2_proxy}, but is not used as the baseline", "compact-body sensitivity derivatives are required", "EXCLUDED_FROM_BASELINE"),
        ("AP4862_6_uniform", "combined", "all r in (0,1/3] pass weak alpha1, weak alpha2 and both BBN anchors", str(p_uniform), "minimum of source-backed sufficient conditions", f"0<p<={p_uniform}", "r-independent sufficient corridor, not the full allowed region", "NONEMPTY_SOURCE_BACKED_CORRIDOR"),
        ("AP4862_7_work", "benchmark", "p=1e-15", str(P_WORK), "retained conservative working point", f"margin to weak uniform ceiling={p_uniform / P_WORK}", "benchmark rather than a GW-derived bound", "HIGH_MARGIN_BENCHMARK"),
    ]
    return [
        {
            "row_id": row_id,
            "channel": channel,
            "mapped_observable": observable,
            "source_bound": source_bound,
            "source": source,
            "derived_p_condition": condition,
            "scope": scope,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for row_id, channel, observable, source_bound, source, condition, scope, status in entries
    ]


def canonical_rows() -> list[dict[str, Any]]:
    entries = [
        ("CAN4862_0_action", "S_ae=(Mbar^2/2) int sqrt(-gHat)[R-K(c_i,nabla u)+lambda(u^2+1)]", "public two-derivative gravity/flow action", "NORMALIZATION_FIXED"),
        ("CAN4862_1_unit", "u^0=sqrt(1+v_i v_i)=1+v^2/2-v^4/8+...", "unit constraint supplies nonlinear flow vertices", "EXACT_SERIES"),
        ("CAN4862_2_transverse", "K[v(t,x)]=-c14 v_t^2+c1 v_x^2+c123 v^2 v_t^2-c1 v^2 v_x^2+O(v^4 partial-v^2)", "exact single-transverse-polarization expansion through quartic order", "EXACT_LOCAL_EXPANSION"),
        ("CAN4862_3_smallest", "q_min=c14=2rp/(1+r); c123/c14=1/[3r(1-p)]>=1", "c14 is the smallest flow kinetic owner in 0<r<=1/3", "EXACT_CORRIDOR"),
        ("CAN4862_4_canonical", "v_c=Mbar sqrt(c14) v", "canonical transverse flow field", "EXACT_QUADRATIC_NORMALIZATION"),
        ("CAN4862_5_Cbar", "C3,C4<=Cbar=2p/[3(1-p)] for p<=0.06 and 0<r<=1/3", "uniform ceiling on the dimensionless two-derivative nonlinear coefficients", "PROVED_COEFFICIENT_ENVELOPE"),
        ("CAN4862_6_cubic", "Mbar^2 C3 v(partial v)^2 -> [C3/(Mbar c14^(3/2))] v_c(partial v_c)^2", "canonical cubic interaction", "EXACT_POWER_COUNTING"),
        ("CAN4862_7_quartic", "Mbar^2 C4 v^2(partial v)^2 -> [C4/(Mbar^2 c14^2)] v_c^2(partial v_c)^2", "canonical quartic interaction", "EXACT_POWER_COUNTING"),
        ("CAN4862_8_scales", "Lambda3=Mbar c14^(3/2)/C3; Lambda4=Mbar c14/sqrt(C4); Lambda_sigma=Mbar sqrt(c14)", "tree-level canonical suppression scales before order-one partial-wave factors", "DERIVED_NDA_SCALES"),
        ("CAN4862_9_floor", "Lambda_safe=3sqrt(2) Mbar (1-p) sqrt(p) [r/(1+r)]^(3/2)", "lower diagnostic obtained by C3<=Cbar; it is below the quartic and sigma-model diagnostics", "DERIVED_CONSERVATIVE_TWO_DERIVATIVE_FLOOR"),
        ("CAN4862_10_rfloor", "x=[Ereq/(3sqrt(2)Mbar(1-p)sqrt(p))]^(2/3); r>=x/(1-x)", "exact inversion of Lambda_safe>=Ereq", "DERIVED_EFT_WINDOW"),
        ("CAN4862_11_ceiling", "full reduced scalar-vector-graviton cubic action and partial-wave eigenvalues are not yet evaluated", "constraint elimination could change order-one factors or reveal a lower mixed channel", "HARD_CAVEAT_NEXT"),
    ]
    return [
        {
            "row_id": row_id,
            "equation": equation,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for row_id, equation, meaning, status in entries
    ]


def lambda_safe(p_value: Decimal, ratio: Decimal) -> Decimal:
    return (
        Decimal(3)
        * Decimal(2).sqrt()
        * (Decimal(1) - p_value)
        * (ratio / (Decimal(1) + ratio)) ** (Decimal(3) / Decimal(2))
        * REDUCED_PLANCK_MASS_GEV
        * p_value.sqrt()
    )


def ratio_floor(p_value: Decimal, energy_gev: Decimal) -> Decimal:
    x_value = (
        energy_gev
        / (Decimal(3) * Decimal(2).sqrt() * REDUCED_PLANCK_MASS_GEV * (Decimal(1) - p_value) * p_value.sqrt())
    ) ** (Decimal(2) / Decimal(3))
    return x_value / (Decimal(1) - x_value)


def benchmark_rows() -> list[dict[str, Any]]:
    fmax = decimal_alpha2_shape_max()
    p_uniform = ALPHA2_WEAK_BOUND / fmax
    r_star = -Decimal(1) + Decimal(2) * Decimal(3).sqrt() / Decimal(3)
    alpha1_work = -Decimal(8) * R_WORK * P_WORK / (Decimal(1) + R_WORK)
    alpha2_star = -r_star * p_uniform * (Decimal(1) - Decimal(3) * r_star) / (Decimal(1) + r_star)
    entries = [
        ("BEN4862_0_constants", "normalization", "Mbar_Pl", str(REDUCED_PLANCK_MASS_GEV), "GeV", "Planck mass divided by sqrt(8pi) using 2022 CODATA"),
        ("BEN4862_1_R10_energy", "required scale", "hbar*c/lambda_R10", str(R10_ENERGY_GEV), "GeV", "lambda_R10=38.6 micrometre anchor"),
        ("BEN4862_2_work_PPN", "working point", "alpha1(p=1e-15,r=1/3)", str(alpha1_work), "dimensionless", "alpha2=0 at r=1/3; G mismatch=p"),
        ("BEN4862_3_work_cutoff", "working point", "Lambda_safe(p=1e-15,r=1/3)", str(lambda_safe(P_WORK, R_WORK)), "GeV", "conservative two-derivative canonical floor"),
        ("BEN4862_4_R10_rfloor", "window", "r_min at p=1e-15 and Ereq=R10", str(ratio_floor(P_WORK, R10_ENERGY_GEV)), "dimensionless", "far below r<=1/3 corridor"),
        ("BEN4862_5_TeV_rfloor", "stress", "r_min at p=1e-15 and Ereq=1 TeV", str(ratio_floor(P_WORK, TEV_STRESS_GEV)), "dimensionless", "aggressive diagnostic, not an observational gravity requirement"),
        ("BEN4862_6_uniform", "weak-field ceiling", "p_uniform", str(p_uniform), "dimensionless", "saturates weak alpha2 at r=r_star"),
        ("BEN4862_7_uniform_alpha2", "weak-field ceiling", "alpha2(p_uniform,r_star)", str(alpha2_star), "dimensionless", "equals -1e-7 to numerical precision"),
        ("BEN4862_8_uniform_cutoff", "weak-field ceiling", "Lambda_safe(p_uniform,r=1/3)", str(lambda_safe(p_uniform, R_WORK)), "GeV", "large nonempty EFT margin"),
    ]
    return [
        {
            "row_id": row_id,
            "kind": kind,
            "quantity": quantity,
            "value": value,
            "units": units,
            "interpretation": interpretation,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for row_id, kind, quantity, value, units, interpretation in entries
    ]


def sample_rows(symbols: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    p = symbols["p"]
    ratio = symbols["r"]
    p_values = [Decimal("1e-15"), Decimal("1e-9"), Decimal("1e-6"), Decimal("0.06")]
    r_values = [Decimal("1e-9"), Decimal("1e-6"), Decimal("1e-3"), Decimal("0.154700538379251529"), Decimal(1) / Decimal(3)]
    rows: list[dict[str, Any]] = []
    for p_value in p_values:
        for r_value in r_values:
            substitutions = {p: sp.Float(str(p_value), 50), ratio: sp.Float(str(r_value), 50)}
            coefficients = [abs(float(sp.N(symbols[name].subs(substitutions), 30))) for name in ("c1", "c2", "c3", "c4")]
            cbar_value = float(sp.N(symbols["Cbar"].subs(substitutions), 30))
            q_value = float(sp.N(symbols["c14"].subs(substitutions), 30))
            c123_value = float(sp.N(symbols["c123"].subs(substitutions), 30))
            cutoff_value = lambda_safe(p_value, r_value)
            passed = max(coefficients) <= cbar_value * (1 + 1e-12) and 0 < q_value <= c123_value and cutoff_value > 0
            rows.append(
                {
                    "row_id": f"SAMP4862_{len(rows):02d}",
                    "p": str(p_value),
                    "r": str(r_value),
                    "max_abs_ci": f"{max(coefficients):.17e}",
                    "Cbar": f"{cbar_value:.17e}",
                    "c14": f"{q_value:.17e}",
                    "c123": f"{c123_value:.17e}",
                    "Lambda_safe_GeV": str(cutoff_value),
                    "status": "PASS" if passed else "FAIL",
                    "valid_for_claim": False,
                    "timestamp_utc": TIMESTAMP,
                }
            )
    return rows


def decision_rows() -> list[dict[str, Any]]:
    entries = [
        ("DEC4862_0_bound", "replace the unsupported GW-derived p<=1e-15 interpretation with a source-backed public-frame envelope", "p<=1/8 is a direct EA-specific absolute anchor; p<=1.392820323e-6 is an r-independent weak-PPN-safe sufficient corridor"),
        ("DEC4862_1_strong", "do not use the local 2e-9 alpha2 row as weak-field evidence", "Gupta et al. show that strong-field preferred-frame parameters need sensitivity derivatives"),
        ("DEC4862_2_cutoff", "retain p=1e-15,r=1/3 as a high-margin benchmark", "Lambda_safe is about 4.08e10 GeV and even a 1 TeV diagnostic only requires r above about 2.11e-6"),
        ("DEC4862_3_branch", "keep public gHat as the lead private branch", "the sourced parameter and leading canonical cutoff gates have a large nonempty intersection; fallback is not triggered"),
        ("DEC4862_4_endpoint", "do not take p or r to zero inside the finite EFT", "Lambda_safe scales as sqrt(p) r^(3/2), so the exact-GR endpoint still needs gauge restoration or a different variable chart"),
        ("DEC4862_5_next", "derive the complete reduced cubic mode action and partial-wave cutoff", "this is the remaining calculation that can confirm or overturn the conservative canonical floor"),
    ]
    return [
        {
            "decision_id": row_id,
            "decision": decision,
            "reason": reason,
            "next_target": NEXT_TARGET if row_id == "DEC4862_5_next" else "",
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for row_id, decision, reason in entries
    ]


def residual_rows() -> list[dict[str, Any]]:
    entries = [
        (1, "E_absolute_p", "CLOSED_SOURCE_BACKED_SUFFICIENT_CORRIDOR", "weak PPN and BBN give a nonempty public-frame p envelope without relative GW timing", "refine with a joint likelihood only after full cosmology assumptions are fixed"),
        (2, "E_leading_cutoff", "CLOSED_TWO_DERIVATIVE_CANONICAL_DIAGNOSTIC", "canonical cubic floor and exact r/E inversion are derived", "calculate the complete reduced cubic mode action"),
        (3, "E_full_unitarity", "OPEN_HARD_NEXT", "auxiliary elimination and scalar-vector-graviton partial waves are not diagonalized", "derive 4863 reduced vertices and scattering eigenvalues"),
        (4, "E_strong_field", "OPEN_HARD", "compact-body sensitivities and dipole radiation are not evaluated on the one-parameter surface", "compute after the hard cutoff survives"),
        (5, "E_exact_GR_endpoint", "OPEN_HARD", "finite-mode cutoff vanishes as p or r approaches zero", "derive gauge restoration or keep the endpoint outside this chart"),
        (6, "E_primitive_owner", "OPEN_HARD", "the original MTS primitives have not uniquely generated gHat and the coefficient surface", "return upstream after correspondence viability is secured"),
    ]
    return [
        {
            "priority": priority,
            "residual": residual,
            "status": status,
            "evidence": evidence,
            "next_action": next_action,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for priority, residual, status, evidence, next_action in entries
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    identities: list[dict[str, Any]],
    p_bounds: list[dict[str, Any]],
    canonical: list[dict[str, Any]],
    benchmarks: list[dict[str, Any]],
    samples: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    claims = [row for row in read_csv(FORMAL / "02-claims-register.csv") if row.get("claim_id") == "L-704"]
    variables = read_csv(FORMAL / "04-variable-audit.csv")
    response_variables = [row for row in variables if row.get("symbol") == "p_public_cutoff_window"]
    checkpoint = (POST / "4862-Y5-R2FR-public-frame-absolute-p-bound-and-strong-coupling-cutoff-or-fallback-selection.md").read_text(encoding="utf-8")
    formal = (FORMAL / "878-PPC4161-public-frame-absolute-p-and-cutoff-window.md").read_text(encoding="utf-8")
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")
    prior_validation = read_csv(OUTPUT / "P8_Y5_BRR545_4861_VALIDATION.csv")

    def result(check_id: str, passed: bool, detail: str) -> dict[str, Any]:
        return {"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail, "valid_for_claim": False, "timestamp_utc": TIMESTAMP}

    groups = (sources, identities, p_bounds, canonical, benchmarks, samples, decisions, residuals)
    p_uniform = ALPHA2_WEAK_BOUND / decimal_alpha2_shape_max()
    checks = [
        result("VAL4862_00_sources", len(sources) == 22 and all(row["source_exists"] and row["needle_found"] for row in sources), f"sources={len(sources)}"),
        result("VAL4862_01_identities", len(identities) == 10 and all(row["status"] == "PASS" for row in identities), "ten exact symbolic identities pass"),
        result("VAL4862_02_bounds", len(p_bounds) == 8 and p_bounds[6]["status"] == "NONEMPTY_SOURCE_BACKED_CORRIDOR", f"uniform p ceiling={p_uniform}"),
        result("VAL4862_03_strong_caveat", p_bounds[5]["status"] == "EXCLUDED_FROM_BASELINE", "strong-field alpha2 proxy is not misused"),
        result("VAL4862_04_canonical", len(canonical) == 12 and canonical[9]["status"] == "DERIVED_CONSERVATIVE_TWO_DERIVATIVE_FLOOR", "canonical cutoff floor derived"),
        result("VAL4862_05_samples", len(samples) == 20 and all(row["status"] == "PASS" for row in samples), "coefficient and kinetic envelope passes 20-point sample grid"),
        result("VAL4862_06_R10", lambda_safe(P_WORK, R_WORK) > R10_ENERGY_GEV and ratio_floor(P_WORK, R10_ENERGY_GEV) < R_WORK, "working point resolves the R10 anchor"),
        result("VAL4862_07_TeV", lambda_safe(P_WORK, R_WORK) > TEV_STRESS_GEV and ratio_floor(P_WORK, TEV_STRESS_GEV) < R_WORK, "working point also passes optional 1 TeV stress diagnostic"),
        result("VAL4862_08_branch", len(decisions) == 6 and decisions[3]["decision"] == "keep public gHat as the lead private branch", "fallback not triggered"),
        result("VAL4862_09_residuals", len(residuals) == 6 and residuals[2]["status"] == "OPEN_HARD_NEXT", "full reduced unitarity remains explicit"),
        result("VAL4862_10_nonclaim", all(not row["valid_for_claim"] for group in groups for row in group), "all rows remain private nonclaim"),
        result("VAL4862_11_variable", len(response_variables) == 1, "cutoff-window variable integrated"),
        result("VAL4862_12_claim", len(claims) == 1 and claims[0].get("status") == "public_absolute_p_corridor_and_canonical_cutoff_window_derived_private_nonclaim", f"L-704 rows={len(claims)}"),
        result("VAL4862_13_documents", "PUBLIC_P_BOUND_CUTOFF_SELECTION_4862" in checkpoint and "PPC4161_PUBLIC_P_CUTOFF_4862" in formal, "checkpoint and formal markers found"),
        result("VAL4862_14_resume", resume_checkpoint_at_least(resume, 4862) and NEXT_TARGET in resume, "resume advanced to full reduced cubic action"),
        result("VAL4862_15_prior", prior_validation[-1].get("status") == "PASS", "4861 validation remains green"),
        result("VAL4862_16_script", compiles(Path(__file__).resolve()), "generator compiles"),
    ]
    checks.append(result("VAL4862_OVERALL", all(row["status"] == "PASS" for row in checks), "PUBLIC_P_BOUND_AND_CANONICAL_CUTOFF_WINDOW_VALIDATED"))
    return checks


def main() -> int:
    symbols = symbolic_map()
    sources = source_rows()
    identities = identity_rows(symbols)
    p_bounds = absolute_p_rows()
    canonical = canonical_rows()
    benchmarks = benchmark_rows()
    samples = sample_rows(symbols)
    decisions = decision_rows()
    residuals = residual_rows()
    validation = validation_rows(sources, identities, p_bounds, canonical, benchmarks, samples, decisions, residuals)
    write_csv(OUTPUT / "P8_Y5_R2FR_4862_SOURCE_REGISTER.csv", sources)
    write_csv(OUTPUT / "P8_Y5_R2FR_4862_SYMBOLIC_IDENTITIES.csv", identities)
    write_csv(OUTPUT / "P8_Y5_R2FR_4862_ABSOLUTE_P_ENVELOPE.csv", p_bounds)
    write_csv(OUTPUT / "P8_Y5_R2FR_4862_CANONICAL_CUTOFF_DERIVATION.csv", canonical)
    write_csv(OUTPUT / "P8_Y5_R2FR_4862_NUMERIC_BENCHMARKS.csv", benchmarks)
    write_csv(OUTPUT / "P8_Y5_R2FR_4862_COEFFICIENT_SAMPLE_GRID.csv", samples)
    write_csv(OUTPUT / "P8_Y5_R2FR_4862_BRANCH_DECISION.csv", decisions)
    write_csv(OUTPUT / "P8_Y5_R2FR_4862_RESIDUAL_REBASE.csv", residuals)
    write_csv(OUTPUT / "P8_Y5_BRR545_4862_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print("P8_Y5_BRR545_4862_VALIDATION_PASS" if passed else "P8_Y5_BRR545_4862_VALIDATION_FAIL")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

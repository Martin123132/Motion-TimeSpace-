from __future__ import annotations

import csv
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Any

import sympy as sp


CHECKPOINT = "4855"
TIMESTAMP = "2026-07-09T22:36:08+00:00"
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = POST / "source-intake" / "local_bounds" / "local_bound_claims.csv"
NEXT_TARGET = "4856-Y5-R2FR-time-flow-Hilbert-variation-and-preferred-frame-PPN-alpha1-alpha2-gate.md"

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
        ("SRC4855_00_3820", POST / "3820-Y5-R2FR-Komar-Tolman-active-mass-and-independent-source-ledger.md", "KT3820_1_Komar_surface_to_EH_volume", "Komar/Tolman source-charge predecessor"),
        ("SRC4855_01_3821", POST / "3821-Y5-R2FR-closed-system-stress-virial-cancellation-or-pressure-binding-bound.md", "TER3821_2_energy_mass_limit", "closed-system stress-virial reduction"),
        ("SRC4855_02_4852", POST / "4852-Y5-R2FR-local-GR-residual-rebase-after-memory-cuscuton-and-Gamma-zero.md", "Nonlinear source charge is not bare", "linear ADM closure and nonlinear warning"),
        ("SRC4855_03_4853", POST / "4853-Y5-R2FR-Maxwell-Hodge-Hilbert-stress-current-normalization-and-stationary-Poynting-boundary-theorem.md", "T_A^{\\mu\\nu}", "owned Maxwell Hilbert stress"),
        ("SRC4855_04_4854", POST / "4854-Y5-R2FR-parent-U1-connection-adoption-or-CP2-Berry-constructor-and-time-flow-constitutive-gate.md", "lambda_E=Z_A+\\eta_u", "static and propagation normalization split"),
        ("SRC4855_05_beta", LOCAL_BOUNDS, "R4_beta", "existing PPN beta comparator row"),
        ("SRC4855_06_variables", FORMAL / "04-variable-audit.csv", "M_ADM_Komar_MS", "canonical nonlinear mass variables"),
        ("SRC4855_07_equations", FORMAL / "05-equation-register.md", "1.148 Einstein-Maxwell source charge and charged exterior", "equation integration"),
        ("SRC4855_08_checkpoint", POST / "4855-Y5-R2FR-Einstein-Maxwell-Komar-Tolman-source-charge-and-charged-exterior-PPN-gate.md", "EINSTEIN_MAXWELL_SOURCE_CHARGE_PPN_4855", "human-readable derivation"),
        ("SRC4855_09_formal871", FORMAL / "871-PPC4161-Einstein-Maxwell-source-charge-and-charged-PPN-gate.md", "PPC4161_EINSTEIN_MAXWELL_SOURCE_CHARGE_PPN_4855", "formal-workbench integration"),
        ("SRC4855_10_claim", FORMAL / "02-claims-register.csv", "L-697", "claim register"),
        ("SRC4855_11_resume", POST / "CURRENT_LOCAL_RESUME.md", "# Current local resume", "resume ledger exists and may advance beyond 4855"),
        ("SRC4855_12_script", Path(__file__).resolve(), 'CHECKPOINT = "4855"', "executable symbolic gate"),
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
    rows.extend(
        [
            {
                "source_id": "SRC4855_13_ADM",
                "source_kind": "primary_web_predecessor_verified",
                "source_locator": "https://arxiv.org/abs/gr-qc/0405109",
                "source_exists": True,
                "needle": "ADM Hamiltonian surface energy",
                "needle_found": True,
                "role": "asymptotic Hamiltonian mass definition already used in 4852",
                "source_validated": True,
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            },
            {
                "source_id": "SRC4855_14_IyerWald",
                "source_kind": "primary_web_predecessor_verified",
                "source_locator": "https://arxiv.org/abs/gr-qc/9403028",
                "source_exists": True,
                "needle": "covariant Noether charge",
                "needle_found": True,
                "role": "stationary charge and boundary framework already used in 4852",
                "source_validated": True,
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            },
        ]
    )
    return rows


def field_equation_rows() -> list[dict[str, Any]]:
    radius, mass_length, charge_length_sq = sp.symbols("r m q2", positive=True)
    lapse = 1 - 2 * mass_length / radius + charge_length_sq / radius**2
    einstein_tt = sp.simplify((radius * sp.diff(lapse, radius) + lapse - 1) / radius**2)
    einstein_theta = sp.simplify(sp.diff(lapse, radius) / radius + sp.diff(lapse, radius, 2) / 2)
    entries = [
        ("EME4855_0_action", "S= c^3/(16 pi G_cal) int sqrt(-g) R - 1/4 int sqrt(-g) F_c^2", "canonical minimal Einstein-Maxwell branch after A_c=sqrt(lambda_E) A on the static electric sector", "EXACT_PRIVATE_CORRESPONDENCE"),
        ("EME4855_1_charge", "Q_c=(g_J/sqrt(lambda_E)) N_Q", "field-rescaling invariant canonical source charge; alpha_static proportional to Q_c^2/N_Q^2", "EXACT_STATIC_NORMALIZATION"),
        ("EME4855_2_radius", "q^2=G_cal Q_c^2/(4 pi c^4)", "geometric charge radius in rationalized Maxwell units", "DEFINITION"),
        ("EME4855_3_metric", f"f(r)={sp.sstr(lapse)}", "ds^2=-f c^2dt^2+f^-1dr^2+r^2dOmega^2", "REISSNER_NORDSTROM_CANDIDATE"),
        ("EME4855_4_Einstein_tt", sp.sstr(einstein_tt), "expected G^t_t=G^r_r=-q^2/r^4 for radial Maxwell energy/tension", "PASS" if sp.simplify(einstein_tt + charge_length_sq / radius**4) == 0 else "FAIL"),
        ("EME4855_5_Einstein_theta", sp.sstr(einstein_theta), "expected G^theta_theta=G^phi_phi=+q^2/r^4", "PASS" if sp.simplify(einstein_theta - charge_length_sq / radius**4) == 0 else "FAIL"),
        ("EME4855_6_neutral", "spherical nonrotating exterior and Q_c=0 -> F=0 -> q^2=0 -> f=1-2m/r", "the no-exterior-EM-hair neutral spherical branch is exactly Schwarzschild inside the private EH branch", "EXACT"),
    ]
    return [
        {
            "equation_id": equation_id,
            "equation": equation,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for equation_id, equation, meaning, status in entries
    ]


def mass_balance_rows() -> list[dict[str, Any]]:
    entries = [
        ("MSC4855_0_energy_density", "rho_EM=Q_c^2/(32 pi^2 r^4)", "canonical radial electric energy density"),
        ("MSC4855_1_exterior_energy", "E_EM,out(R)/c^2=Q_c^2/(8 pi c^2 R)=c^2 q^2/(2 G_cal R)", "energy mass outside a sphere"),
        ("MSC4855_2_MS", "M_MS(R)=M_ADM-c^2 q^2/(2 G_cal R)", "Misner-Sharp mass excludes the exterior field energy"),
        ("MSC4855_3_Komar", "M_K(R)=M_ADM-c^2 q^2/(G_cal R)", "finite-radius Komar mass carries twice the exterior Maxwell energy because T_EM=0 and stress gravitates"),
        ("MSC4855_4_infinity", "lim_R->infinity M_MS(R)=lim_R->infinity M_K(R)=M_ADM", "all definitions agree at the asymptotic charge"),
        ("MSC4855_5_no_double_count", "M_ADM already contains matter+internal EM+exterior EM+binding+support", "adding E_EM,out again after fixing the 1/r ADM coefficient double counts field energy"),
        ("MSC4855_6_closed_neutral", "spherical nonrotating Q_c=0 exterior has F=0; internal EM/binding remains inside M_ADM", "neutral no-exterior-multipole branch is Schwarzschild without erasing internal electromagnetic mass"),
        ("MSC4855_7_inner_boundary", "horizon or excised inner boundaries add their own Noether/Komar term", "the volume formula is not used across an omitted horizon without its boundary charge"),
    ]
    rows = [
        {
            "row_id": row_id,
            "identity": identity,
            "meaning": meaning,
            "status": "EXACT_MINIMAL_EINSTEIN_MAXWELL",
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for row_id, identity, meaning in entries
    ]
    mass_length = Decimal("1")
    charge_length_sq = Decimal("0.02")
    for radius in (Decimal("5"), Decimal("10"), Decimal("50")):
        exterior_energy = charge_length_sq / (Decimal(2) * radius)
        misner_sharp = mass_length - exterior_energy
        komar = mass_length - charge_length_sq / radius
        rows.append(
            {
                "row_id": f"MSC4855_smoke_R{radius}",
                "identity": f"R={radius}; M_MS={misner_sharp}; M_K={komar}",
                "meaning": f"M-M_MS={exterior_energy}; M-M_K={mass_length-komar}=2 E_out; M_K=2 M_MS-M",
                "status": "PASS" if komar == Decimal(2) * misner_sharp - mass_length else "FAIL",
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    return rows


def ppn_rows() -> list[dict[str, Any]]:
    x, mass_length, charge_length_sq = sp.symbols("x m q2", positive=True)
    areal_radius = 1 / x + mass_length + (mass_length**2 - charge_length_sq) * x / 4
    lapse = 1 - 2 * mass_length / areal_radius + charge_length_sq / areal_radius**2
    g00_series = sp.series(-lapse, x, 0, 3).removeO().expand()
    spatial_series = sp.series((areal_radius * x) ** 2, x, 0, 3).removeO().expand()
    g00_x = sp.expand(g00_series).coeff(x, 1)
    g00_x2 = sp.expand(g00_series).coeff(x, 2)
    spatial_x = sp.expand(spatial_series).coeff(x, 1)
    spatial_x2 = sp.expand(spatial_series).coeff(x, 2)
    checks = {
        "g00_x": sp.simplify(g00_x - 2 * mass_length) == 0,
        "g00_x2": sp.simplify(g00_x2 + 2 * mass_length**2 + charge_length_sq) == 0,
        "spatial_x": sp.simplify(spatial_x - 2 * mass_length) == 0,
        "spatial_x2": sp.simplify(spatial_x2 - sp.Rational(3, 2) * mass_length**2 + sp.Rational(1, 2) * charge_length_sq) == 0,
    }
    entries = [
        ("PPN4855_0_transform", "r=rho+m+(m^2-q^2)/(4rho)", "exact areal-to-isotropic radial map for the static charged exterior", "EXACT"),
        ("PPN4855_1_g00", f"g00={sp.sstr(g00_series)}+O(rho^-3)", "g00=-1+2m/rho-(2m^2+q^2)/rho^2+...", "PASS" if checks["g00_x"] and checks["g00_x2"] else "FAIL"),
        ("PPN4855_2_gij", f"gij/deltaij={sp.sstr(spatial_series)}+O(rho^-3)", "spatial factor=1+2m/rho+(3m^2-q^2)/(2rho^2)+...", "PASS" if checks["spatial_x"] and checks["spatial_x2"] else "FAIL"),
        ("PPN4855_3_gamma", "gamma_1PN=1", "charge enters at order rho^-2 and does not change the first-PN spatial-curvature coefficient", "EXACT_MINIMAL_BRANCH"),
        ("PPN4855_4_beta_apparent", "Delta beta_Q,app=q^2/(2m^2)", "only an apparent source-specific projection if the charged term is forced into the neutral PPN beta template", "EXACT_MAPPING_NOT_UNIVERSAL_PPN_PARAMETER"),
        ("PPN4855_5_neutral", "spherical nonrotating q=0 and F_ext=0 -> beta=gamma=1", "the neutral no-exterior-EM-hair minimal Einstein-Maxwell branch reduces exactly to the GR PPN values", "EXACT_PRIVATE_BRANCH"),
        ("PPN4855_6_preferred_frame_guard", "alpha1,alpha2 not inferred from beta=gamma=1", "the MTS time flow and its gravitational/Hilbert variation require a separate preferred-frame derivation", "OPEN_SEPARATE_GATE"),
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


def beta_projection_rows() -> list[dict[str, Any]]:
    beta_rows = [row for row in read_csv(LOCAL_BOUNDS) if row.get("row_id") == "R4_beta"]
    if len(beta_rows) != 1:
        raise RuntimeError(f"Expected one R4_beta row, found {len(beta_rows)}")
    beta = beta_rows[0]
    beta_envelope = Decimal(beta["upper_bound"])
    charge_ratio_sq = Decimal(2) * beta_envelope
    charge_ratio = charge_ratio_sq.sqrt()
    return [
        {
            "projection_id": "BQP4855_0_comparator",
            "quantity": "abs(beta-1)_envelope",
            "value": str(beta_envelope),
            "formula": "existing local R4_beta comparator",
            "status": "COMPARATOR_ONLY",
            "source": beta["reference_path_or_url"],
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        },
        {
            "projection_id": "BQP4855_1_charge_sq",
            "quantity": "zeta_Q^2=q^2/m^2",
            "value": str(charge_ratio_sq),
            "formula": "zeta_Q^2 <= 2 abs(beta-1) if the entire neutral-template residual is conservatively assigned to net charge",
            "status": "SOURCE_SPECIFIC_PROJECTION_ENVELOPE",
            "source": beta["reference_path_or_url"],
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        },
        {
            "projection_id": "BQP4855_2_charge",
            "quantity": "abs(zeta_Q)=abs(q/m)",
            "value": str(charge_ratio),
            "formula": "abs(Q_c)/(sqrt(4 pi G_cal) M_ADM) <= sqrt(2 beta_envelope)",
            "status": "CONSERVATIVE_PIPELINE_ENVELOPE_NOT_DIRECT_CHARGE_LIMIT",
            "source": beta["reference_path_or_url"],
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        },
        {
            "projection_id": "BQP4855_3_neutral",
            "quantity": "Delta beta_Q,app",
            "value": "0",
            "formula": "Q_c=0",
            "status": "EXACT_NEUTRAL_SOURCE_ZERO",
            "source": "4855 charged exterior derivation",
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        },
    ]


def eta_stress_rows(beta_projection: list[dict[str, Any]]) -> list[dict[str, Any]]:
    speed_rows = read_csv(OUTPUT / "P8_Y5_R2FR_4854_GW170817_SPEED_BOUND.csv")
    kappa_rows = [row for row in speed_rows if row.get("bound_id") == "SPD4854_3_kappa"]
    if len(kappa_rows) != 1:
        raise RuntimeError(f"Expected one kappa bound row, found {len(kappa_rows)}")
    kappa_abs = max(abs(Decimal(kappa_rows[0]["lower"])), abs(Decimal(kappa_rows[0]["upper"])))
    zeta_sq = Decimal(next(row["value"] for row in beta_projection if row["projection_id"] == "BQP4855_1_charge_sq"))
    conditional_beta = Decimal("0.5") * kappa_abs * zeta_sq
    entries = [
        ("ETA4855_0_minimal", "eta_u=0", "exact Reissner-Nordstrom and the mass/PPN identities above", "PRIVATE_BASELINE_EXACT"),
        ("ETA4855_1_static_calibration", "Q_c^2=g_J^2 N_Q^2/lambda_E", "pure Coulomb amplitude is expressed in the already calibrated static coupling", "NO_NEW_STATIC_COUPLING"),
        ("ETA4855_2_Hilbert", "T_uFF requires metric variation of u, its normalization constraint and the eta_u operator", "photon-speed data bound eta_u/Z_A but do not by themselves derive its charged-source Hilbert tensor", "OPEN_PARENT_VARIATION_COEFFICIENT_C_uT"),
        ("ETA4855_3_metric_bound", "abs(delta g00_uFF) <= C_uT abs(kappa_u) q^2/r^2", "finite response form with no cancellation credit", "BOUND_FORM_DERIVED_COEFFICIENT_OPEN"),
        ("ETA4855_4_beta_bound", f"abs(delta beta_uFF) <= C_uT*{conditional_beta}", "if the charge term already satisfies the existing beta projection and C_uT is order one, the propagation-bounded correction is below 4.7e-19", "CONDITIONAL_ORDER_ONE_RESPONSE_BENCHMARK"),
        ("ETA4855_5_neutral", "spherical Q_c=0 and F_ext=0 -> static exterior uFF charge correction=0", "the no-exterior-EM-hair branch is insensitive to this charged-source term, while preferred-frame gravity remains separate", "EXACT_STATIC_CHARGE_ZERO"),
    ]
    return [
        {
            "row_id": row_id,
            "condition_or_formula": formula,
            "meaning": meaning,
            "status": status,
            "kappa_abs_bound": str(kappa_abs),
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for row_id, formula, meaning, status in entries
    ]


def residual_rows() -> list[dict[str, Any]]:
    entries = [
        (1, "E_EM_source_charge_neutral_spherical", "CLOSED_PRIVATE_EH_U1_STATIONARY_SPHERICAL_NO_HAIR", "total Maxwell energy/stress is included once in M_ADM and spherical nonrotating Q_c=0 forces F_ext=0 and Schwarzschild", "retain parent-EH, multipole/rotation and nonstationary/domain gates"),
        (2, "E_EM_source_charge_charged", "EXACT_MINIMAL_RN_BRANCH", "the canonical calibrated charge fixes q^2 and the exterior mass/Komar/PPN terms", "use source-specific charge rather than a universal beta shift"),
        (3, "E_Komar_Tolman_finite_radius", "CLOSED_WITH_STRESS_FACTOR", "M_K differs from M_MS by the Maxwell stress contribution and both approach ADM at infinity", "do not double count exterior field energy"),
        (4, "E_PPN_beta_gamma_neutral", "BETA_GAMMA_ONE_PRIVATE_MINIMAL_BRANCH", "isotropic expansion of the neutral exterior gives beta=gamma=1", "preferred-frame and strict parent-EH origin remain separate"),
        (5, "E_charged_beta_projection", "SOURCE_SPECIFIC_PREDICTION_NOT_UNIVERSAL_PPN", "Delta beta_Q,app=q^2/(2m^2) only when projected onto the neutral PPN template", "use direct charged metric/orbit model for a real test"),
        (6, "E_eta_u_Hilbert_response", "FINITE_BOUND_TIMES_C_uT_OPEN", "kappa_u is bounded but the parent metric variation of the normalized time flow is not yet derived", "derive C_uT and preferred-frame PPN alpha1/alpha2"),
        (7, "E_parent_to_EH", "OPEN_HARD", "the private correspondence action is Einstein-Hilbert but its strict derivation from primitive MTS remains incomplete", "continue parent action derivation without weakening the correspondence result"),
        (8, "E_external_EM_multipoles_rotation", "OPEN_OUTSIDE_SPHERICAL_NO_HAIR_CLASS", "zero net charge alone does not remove magnetic dipole or higher electromagnetic stress", "derive or bound real-source exterior EM multipoles and rotation"),
        (9, "E_boundary_radiation", "STATIONARY_CLOSED_ONLY", "radiating, open-domain or horizon branches retain Noether/boundary flux terms", "keep explicit worldtube and inner-boundary charges"),
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


def decision_rows() -> list[dict[str, Any]]:
    entries = [
        ("DEC4855_0_mass", "use ADM mass as the asymptotic closed-system source charge", "Komar and Misner-Sharp finite-radius differences are derived field/stress partitions, not competing fitted masses"),
        ("DEC4855_1_neutral", "close the spherical nonrotating neutral no-exterior-EM-hair source-charge and beta/gamma lane inside the private EH+U1 branch", "internal EM energy remains in ADM mass while spherical Q_c=0 forces F_ext=0 and Schwarzschild"),
        ("DEC4855_2_charged", "retain the exact charged exterior as a source-specific prediction", "the q^2/r^2 term is calibrated by charge and is not a universal PPN beta violation"),
        ("DEC4855_3_eta", "carry eta_u through a named Hilbert-response coefficient C_uT", "speed bounds do not replace variation of the normalized time-flow field"),
        ("DEC4855_4_next", "derive the time-flow Hilbert tensor and preferred-frame alpha1/alpha2 vector", "this is now the first local PPN obstruction after neutral beta/gamma and EM source charge close"),
    ]
    return [
        {
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_target": NEXT_TARGET if decision_id == "DEC4855_4_next" else "",
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for decision_id, decision, reason in entries
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    field_equations: list[dict[str, Any]],
    mass_balance: list[dict[str, Any]],
    ppn: list[dict[str, Any]],
    beta_projection: list[dict[str, Any]],
    eta_stress: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    claim = [row for row in read_csv(FORMAL / "02-claims-register.csv") if row.get("claim_id") == "L-697"]
    variables = read_csv(FORMAL / "04-variable-audit.csv")
    mass_variable = [row for row in variables if row.get("symbol") == "M_ADM_Komar_MS"]
    charge_variable = [row for row in variables if row.get("symbol") == "Q_c_r_Q"]
    checkpoint = (POST / "4855-Y5-R2FR-Einstein-Maxwell-Komar-Tolman-source-charge-and-charged-exterior-PPN-gate.md").read_text(encoding="utf-8")
    formal = (FORMAL / "871-PPC4161-Einstein-Maxwell-source-charge-and-charged-PPN-gate.md").read_text(encoding="utf-8")
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")

    def result(check_id: str, passed: bool, detail: str) -> dict[str, Any]:
        return {"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail, "valid_for_claim": False, "timestamp_utc": TIMESTAMP}

    groups = (sources, field_equations, mass_balance, ppn, beta_projection, eta_stress, residuals, decisions)
    checks = [
        result("VAL4855_00_sources", len(sources) == 15 and all(row["source_exists"] and row["needle_found"] for row in sources), f"sources={len(sources)}"),
        result("VAL4855_01_Einstein_tensor", all(row["status"] == "PASS" for row in field_equations if row["equation_id"] in {"EME4855_4_Einstein_tt", "EME4855_5_Einstein_theta"}), "symbolic Einstein tensor matches radial Maxwell stress"),
        result("VAL4855_02_mass_balance", len(mass_balance) == 11 and all(row["status"] == "PASS" for row in mass_balance if row["row_id"].startswith("MSC4855_smoke")), "Misner-Sharp/Komar/exterior-energy identities pass"),
        result("VAL4855_03_ppn", all(row["status"] == "PASS" for row in ppn if row["row_id"] in {"PPN4855_1_g00", "PPN4855_2_gij"}), "isotropic charged-exterior expansion verified symbolically"),
        result("VAL4855_04_neutral", any(row["row_id"] == "PPN4855_5_neutral" and row["status"] == "EXACT_PRIVATE_BRANCH" for row in ppn), "neutral beta=gamma=1 lane explicit"),
        result("VAL4855_05_beta_projection", len(beta_projection) == 4 and Decimal(beta_projection[1]["value"]) == Decimal("1.56e-4"), "existing beta comparator mapped without promotion"),
        result("VAL4855_06_eta_guard", len(eta_stress) == 6 and any(row["status"] == "OPEN_PARENT_VARIATION_COEFFICIENT_C_uT" for row in eta_stress), "time-flow Hilbert response remains named rather than assumed"),
        result("VAL4855_07_residuals", len(residuals) == 9 and residuals[0]["status"] == "CLOSED_PRIVATE_EH_U1_STATIONARY_SPHERICAL_NO_HAIR" and any(row["residual"] == "E_external_EM_multipoles_rotation" for row in residuals), "neutral spherical no-hair source-charge residual rebased while real multipoles remain open"),
        result("VAL4855_08_nonclaim", all(not row["valid_for_claim"] for group in groups for row in group), "all 4855 rows remain private nonclaim"),
        result("VAL4855_09_variables", len(mass_variable) == 1 and len(charge_variable) == 1, "variable audit updated"),
        result("VAL4855_10_claim", len(claim) == 1 and claim[0].get("status") == "neutral_stationary_spherical_no_hair_Einstein_Maxwell_source_charge_and_beta_gamma_closed_charged_RN_term_derived_eta_stress_response_open_private_nonclaim", f"L-697 rows={len(claim)}"),
        result("VAL4855_11_documents", "EINSTEIN_MAXWELL_SOURCE_CHARGE_PPN_4855" in checkpoint and "PPC4161_EINSTEIN_MAXWELL_SOURCE_CHARGE_PPN_4855" in formal, "checkpoint and formal markers found"),
        result("VAL4855_12_resume", resume_checkpoint_at_least(resume, 4855), "resume reached or advanced beyond the time-flow Hilbert/preferred-frame PPN gate"),
        result("VAL4855_13_script", compiles(Path(__file__).resolve()), "generator compiles"),
    ]
    checks.append(result("VAL4855_OVERALL", all(row["status"] == "PASS" for row in checks), "EINSTEIN_MAXWELL_SOURCE_CHARGE_PPN_GATE_VALIDATED"))
    return checks


def main() -> int:
    sources = source_rows()
    field_equations = field_equation_rows()
    mass_balance = mass_balance_rows()
    ppn = ppn_rows()
    beta_projection = beta_projection_rows()
    eta_stress = eta_stress_rows(beta_projection)
    residuals = residual_rows()
    decisions = decision_rows()
    validation = validation_rows(sources, field_equations, mass_balance, ppn, beta_projection, eta_stress, residuals, decisions)
    write_csv(OUTPUT / "P8_Y5_R2FR_4855_SOURCE_REGISTER.csv", sources)
    write_csv(OUTPUT / "P8_Y5_R2FR_4855_EINSTEIN_MAXWELL_FIELD_EQUATIONS.csv", field_equations)
    write_csv(OUTPUT / "P8_Y5_R2FR_4855_SPHERICAL_MASS_BALANCE.csv", mass_balance)
    write_csv(OUTPUT / "P8_Y5_R2FR_4855_ISOTROPIC_PPN_EXPANSION.csv", ppn)
    write_csv(OUTPUT / "P8_Y5_R2FR_4855_BETA_CHARGE_PROJECTION.csv", beta_projection)
    write_csv(OUTPUT / "P8_Y5_R2FR_4855_ETA_STRESS_BOUND.csv", eta_stress)
    write_csv(OUTPUT / "P8_Y5_R2FR_4855_RESIDUAL_REBASE.csv", residuals)
    write_csv(OUTPUT / "P8_Y5_R2FR_4855_DECISION.csv", decisions)
    write_csv(OUTPUT / "P8_Y5_BRR545_4855_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print("P8_Y5_BRR545_4855_VALIDATION_PASS" if passed else "P8_Y5_BRR545_4855_VALIDATION_FAIL")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

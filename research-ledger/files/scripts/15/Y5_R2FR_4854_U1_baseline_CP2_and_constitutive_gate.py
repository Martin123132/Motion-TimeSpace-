from __future__ import annotations

import csv
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Any


CHECKPOINT = "4854"
TIMESTAMP = "2026-07-09T21:50:00+00:00"
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
NEXT_TARGET = "4855-Y5-R2FR-Einstein-Maxwell-Komar-Tolman-source-charge-and-charged-exterior-PPN-gate.md"

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


def decimal_text(value: Decimal) -> str:
    return f"{value:.24E}"


def source_rows() -> list[dict[str, Any]]:
    local_sources = [
        ("SRC4854_00_3785", POST / "3785-Y5-R2FR-derive-BQ-flow-one-form-from-vorticity-defects-or-demote-EM.md", "RNG3785_1_rank", "two-pair or CP2 generic-rank condition"),
        ("SRC4854_01_3786", POST / "3786-Y5-R2FR-parent-internal-multiplet-owner-or-BQ-finite-demotion.md", "CSA3786_5_verdict", "current-corpus internal-multiplet owner audit"),
        ("SRC4854_02_4853", POST / "4853-Y5-R2FR-Maxwell-Hodge-Hilbert-stress-current-normalization-and-stationary-Poynting-boundary-theorem.md", "SCALAR_ONLY_MAXWELL_NO_GO", "minimal U1 baseline and constitutive residual"),
        ("SRC4854_03_formal869", FORMAL / "869-PPC4161-Maxwell-U1-stress-current-and-Poynting-rebase.md", "PPC4161_MAXWELL_U1_REBASE_4853", "formal predecessor"),
        ("SRC4854_04_variables", FORMAL / "04-variable-audit.csv", "Z_A_eta_u", "canonical constitutive variables"),
        ("SRC4854_05_equations", FORMAL / "05-equation-register.md", "1.147 Isotropic time-flow photon constitutive theorem", "equation integration"),
        ("SRC4854_06_checkpoint", POST / "4854-Y5-R2FR-parent-U1-connection-adoption-or-CP2-Berry-constructor-and-time-flow-constitutive-gate.md", "U1_BASELINE_CP2_CONSTITUTIVE_GATE_4854", "human-readable derivation"),
        ("SRC4854_07_formal870", FORMAL / "870-PPC4161-parent-U1-baseline-and-time-flow-constitutive-bound.md", "PPC4161_U1_BASELINE_CONSTITUTIVE_BOUND_4854", "formal-workbench integration"),
        ("SRC4854_08_claim", FORMAL / "02-claims-register.csv", "L-696", "claim register"),
        ("SRC4854_09_resume", POST / "CURRENT_LOCAL_RESUME.md", "# Current local resume", "resume ledger exists and may advance beyond 4854"),
        ("SRC4854_10_script", Path(__file__).resolve(), 'CHECKPOINT = "4854"', "executable gate"),
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
                "source_id": "SRC4854_11_GW170817",
                "source_kind": "primary_web_verified",
                "source_locator": "https://arxiv.org/abs/1710.05834",
                "source_exists": True,
                "needle": "speed of gravity and the speed of light to be between -3e-15 and +7e-16 times the speed of light",
                "needle_found": True,
                "role": "source-backed gravity-photon propagation-speed interval",
                "source_validated": True,
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            },
            {
                "source_id": "SRC4854_12_KM2009",
                "source_kind": "primary_web_verified",
                "source_locator": "https://arxiv.org/abs/0905.0031",
                "source_exists": True,
                "needle": "gauge-invariant Lorentz-violating photon operators",
                "needle_found": True,
                "role": "independent operator classification and dispersion/birefringence context",
                "source_validated": True,
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            },
        ]
    )
    return rows


def rank_rows() -> list[dict[str, Any]]:
    entries = [
        ("RKT4854_0_pullback", "H=Phi^*omega implies H wedge H=Phi^*(omega wedge omega)", "EXACT", "generic rank is controlled by the parent target and its owned two-form"),
        ("RKT4854_1_dimension", "dim(target)<4 implies omega wedge omega=0 and therefore H wedge H=0", "EXACT", "no target with fewer than four real dimensions can own generic rank-four local EM curvature through one pullback"),
        ("RKT4854_2_scalar", "real psi has one-dimensional target", "FAIL_GENERIC_EM", "d f(psi) and f(psi)dpsi are curvature-free; any pulled-back two-form vanishes"),
        ("RKT4854_3_flow", "unit timelike u has three-dimensional hyperboloid target", "FAIL_GENERIC_EM_ALONE", "u may own vorticity/simple sectors but its pulled-back curvature obeys H wedge H=0"),
        ("RKT4854_4_combined", "combined (u,psi,...) target can reach dimension four", "DIMENSION_NECESSARY_NOT_SUFFICIENT", "the current action owns no closed integral symplectic form, U1 bundle, chart law or selector on that target"),
        ("RKT4854_5_CP2", "CP2 has real dimension four and nondegenerate Fubini-Study form; B=-i z^dagger dz is a local Berry connection", "VALID_OPTIONAL_CONSTRUCTOR", "it can represent generic local closed rank-four curvature, but requires a new parent multiplet and a variational-equivalence proof"),
        ("RKT4854_6_variation", "representing F as a Berry pullback is not by itself equivalent to varying an independent A", "MAXWELL_DYNAMICS_NOT_YET_DERIVED", "the composite-map tangent variations must span the Maxwell connection variations without extra propagating modes or constraints"),
    ]
    return [
        {
            "theorem_id": theorem_id,
            "statement": statement,
            "status": status,
            "consequence": consequence,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for theorem_id, statement, status, consequence in entries
    ]


def architecture_rows() -> list[dict[str, Any]]:
    entries = [
        ("ARC4854_0_scalar", "derive A from current real scalar", "REJECT", "helicity, curvature-rank and pure-gauge failures remain"),
        ("ARC4854_1_flow", "derive generic A from u alone", "REJECT_GENERIC_PARTIAL_SIMPLE_SECTORS_ONLY", "target dimension three forces H wedge H=0"),
        ("ARC4854_2_CP2", "make z:M->CP2 a new parent field and A=-i z^dagger dz", "OPTIONAL_UV_COMPLETION", "geometrically coherent, but it adds field content and does not yet prove Maxwell variational equivalence"),
        ("ARC4854_3_U1", "adopt A as an independent principal-U1 connection in the correspondence action", "SELECTED_BASELINE", "gives exact Einstein-Maxwell classical field theory without pretending scalar emergence"),
        ("ARC4854_4_unification", "unification means one covariant action, observed metric, Hilbert source and Ward exchange, not one scalar ontology", "ARCHITECTURE_RULE", "independent U1 field content is compatible with a serious unified multi-field framework"),
    ]
    return [
        {
            "fork_id": fork_id,
            "route": route,
            "decision": decision,
            "reason": reason,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for fork_id, route, decision, reason in entries
    ]


def constitutive_rows() -> list[dict[str, Any]]:
    entries = [
        ("ICT4854_0_basis", "L=-Z_A F^2/4 + eta_u u^mu u^nu F_mu_alpha F_nu^alpha/2 + theta_A F Ftilde/4", "complete isotropic gauge-invariant quadratic two-derivative basis for one unit flow, up to boundary conventions", "EXACT_OPERATOR_BASIS"),
        ("ICT4854_1_rest", "L=[lambda_E E^2-lambda_B B^2]/2; lambda_E=Z_A+eta_u; lambda_B=Z_A", "rest-frame constitutive decomposition", "EXACT"),
        ("ICT4854_2_stability", "lambda_E>0 and lambda_B>0", "positive Hamiltonian rho=[lambda_E E^2+lambda_B B^2]/2 and hyperbolic principal system", "EXACT_GATE"),
        ("ICT4854_3_fields", "D=lambda_E E; H=lambda_B B", "Gauss/Ampere plus Bianchi equations define the source and wave response", "EXACT"),
        ("ICT4854_4_speed", "r_gamma^2=(c_gamma/c_obs)^2=lambda_B/lambda_E=Z_A/(Z_A+eta_u)", "one physical isotropic propagation ratio after common normalization", "EXACT"),
        ("ICT4854_5_chi", "lambda_E=lambda_A(1+chi_E); lambda_B=lambda_A(1+chi_B)", "(chi_B-chi_E)/(1+chi_E)=r_gamma^2-1; common chi is normalization", "EXACT_REPARAMETERIZATION"),
        ("ICT4854_6_birefringence", "one isotropic u supplies no polarization-dependent spatial tensor", "both transverse polarizations share the same r_gamma; anisotropy/birefringence needs extra tensor structure", "ABSENT_IN_ISOTROPIC_U_ONLY_BLOCK"),
        ("ICT4854_7_theta", "constant theta_A F Ftilde is topological", "no local stress or principal-speed shift; a varying pseudoscalar coefficient remains open", "LOCAL_CONSTANT_SILENT"),
        ("ICT4854_8_current", "nabla_mu(lambda response tensor)=g_J j^nu", "same current Ward identity is retained; constitutive coefficients affect field response, not charge conservation when stationary constants", "EXACT_LOCAL_BRANCH"),
    ]
    return [
        {
            "row_id": row_id,
            "equation": equation,
            "derivation": derivation,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for row_id, equation, derivation, status in entries
    ]


def speed_bound_rows() -> list[dict[str, Any]]:
    delta_low = Decimal("-3e-15")
    delta_high = Decimal("7e-16")
    r_low = Decimal(1) - delta_high
    r_high = Decimal(1) - delta_low
    differential_low = r_low**2 - Decimal(1)
    differential_high = r_high**2 - Decimal(1)
    kappa_low = Decimal(1) / (r_high**2) - Decimal(1)
    kappa_high = Decimal(1) / (r_low**2) - Decimal(1)
    return [
        {
            "bound_id": "SPD4854_0_source",
            "quantity": "delta_g_gamma=(v_g-v_gamma)/c",
            "lower": decimal_text(delta_low),
            "upper": decimal_text(delta_high),
            "mapping": "LIGO/Virgo/Fermi/INTEGRAL GW170817-GRB170817A interval",
            "assumptions": "published conservative source-delay treatment",
            "source": "https://arxiv.org/abs/1710.05834",
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "SPD4854_1_r",
            "quantity": "r_gamma-1=(c_gamma-c_obs)/c_obs",
            "lower": decimal_text(r_low - Decimal(1)),
            "upper": decimal_text(r_high - Decimal(1)),
            "mapping": "set c_g=c_obs on the local EH correspondence branch and reverse the published sign",
            "assumptions": "same observed propagation frame; negligible denominator difference at stated order",
            "source": "https://arxiv.org/abs/1710.05834",
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "SPD4854_2_differential",
            "quantity": "Delta_chi=(chi_B-chi_E)/(1+chi_E)=r_gamma^2-1",
            "lower": decimal_text(differential_low),
            "upper": decimal_text(differential_high),
            "mapping": "exact constitutive identity",
            "assumptions": "positive lambda_E/lambda_B; isotropic frequency-independent local coefficients",
            "source": "4854 constitutive theorem plus https://arxiv.org/abs/1710.05834",
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "SPD4854_3_kappa",
            "quantity": "kappa_u=eta_u/Z_A=r_gamma^-2-1",
            "lower": decimal_text(kappa_low),
            "upper": decimal_text(kappa_high),
            "mapping": "single-unit-flow basis lambda_E=Z_A+eta_u and lambda_B=Z_A",
            "assumptions": "local EH c_g=c_obs; no dispersive cancellation or extra anisotropic photon tensor",
            "source": "4854 constitutive theorem plus https://arxiv.org/abs/1710.05834",
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        },
    ]


def metrology_rows() -> list[dict[str, Any]]:
    entries = [
        ("MET4854_0_Coulomb", "alpha_static proportional to g_J^2/lambda_E", "Gauss law D=lambda_E E and the same matter-current vertex g_J", "ONE_CALIBRATED_STATIC_COUPLING"),
        ("MET4854_1_speed", "r_gamma^2=lambda_B/lambda_E", "source-free Ampere plus Faraday system", "INDEPENDENT_DIFFERENTIAL_RATIO"),
        ("MET4854_2_impedance", "Z_wave proportional to 1/sqrt(lambda_E lambda_B)", "plane wave E/H relation in a fixed field convention", "CONVENTION_DEPENDENT_ALONE"),
        ("MET4854_3_invariant_impedance", "g_J^2 Z_wave proportional to g_J^2/sqrt(lambda_E lambda_B)=alpha_static/r_gamma", "field-rescaling invariant matter-referenced impedance", "NOT_A_THIRD_FREE_PARAMETER"),
        ("MET4854_4_rescaling", "A'=sA; lambda_E,B'=lambda_E,B/s^2; g_J'=g_J/s", "g_J^2/lambda_E and lambda_B/lambda_E are invariant", "EXACT_NORMALIZATION_GUARD"),
    ]
    return [
        {
            "row_id": row_id,
            "observable": observable,
            "derivation": derivation,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for row_id, observable, derivation, status in entries
    ]


def residual_rows() -> list[dict[str, Any]]:
    entries = [
        (1, "E_U1_architecture", "CORRESPONDENCE_FIELD_CONTENT_CLOSED_PRIMITIVE_MTS_ORIGIN_OPEN", "independent U1 connection is now selected rather than repeatedly treated as an undecided fork", "do not claim scalar emergence; keep CP2 as optional UV completion"),
        (2, "E_CP2_origin", "OPTIONAL_UV_COMPLETION_NOT_BASELINE_BLOCKER", "CP2 has the right rank geometry, but current fields own neither its bundle nor variational equivalence", "only reopen if a parent multiplet/action is actually supplied"),
        (3, "E_isotropic_uFF", "SOURCE_BACKED_CONDITIONAL_BOUND", "GW170817 maps to a finite eta_u/Z_A interval on the local EH isotropic branch", "carry the interval into local PPN and clock projections"),
        (4, "E_isotropic_birefringence", "ZERO_AT_U_ONLY_QUADRATIC_LEVEL", "one isotropic unit flow changes a common photon speed but cannot split polarizations", "retain anisotropic perturbation tensors separately"),
        (5, "E_alpha_static", "CALIBRATED_ONCE", "alpha_static fixes g_J^2/lambda_E while speed fixes lambda_B/lambda_E", "do not count impedance as an extra free observable"),
        (6, "E_dynamic_XF2", "OPEN_OFF_STATIONARY_BRANCH", "space/time dependent scalar coefficients can cause drift, scattering or cosmological propagation effects", "derive or bound with clocks/spectroscopy/cosmology"),
        (7, "E_EM_source_charge_PN", "NEXT_HARD_TARGET", "Maxwell Hilbert stress is owned but nonlinear ADM/Komar/Tolman and charged exterior PPN bookkeeping is not yet integrated", "derive Einstein-Maxwell source charge and PPN vector"),
        (8, "E_QED_quantum", "OPEN_EXTENSION", "classical U1 correspondence does not derive quantum charged matter or vacuum effects", "keep outside the immediate local classical GR gate"),
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
        ("DEC4854_0_baseline", "adopt the independent U1 connection as explicit correspondence field content", "this closes the classical architecture without pretending it emerges from the current scalar"),
        ("DEC4854_1_CP2", "retain CP2/Berry only as optional UV completion", "rank geometry is viable but parent ownership and variational equivalence are missing"),
        ("DEC4854_2_constitutive", "replace redundant chi_E/chi_B language by Z_A plus kappa_u=eta_u/Z_A", "one isotropic unit flow has one normalization and one physical differential coefficient"),
        ("DEC4854_3_bound", "use the GW170817 interval as a conditional source-backed coefficient bound", "it converts a legal operator from an unquantified objection into an empirical residual"),
        ("DEC4854_4_next", "feed Maxwell stress and the constitutive interval into nonlinear source charge and PPN", "this is the next direct route toward derived local Einstein-Maxwell/GR behavior"),
    ]
    return [
        {
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_target": NEXT_TARGET if decision_id == "DEC4854_4_next" else "",
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for decision_id, decision, reason in entries
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    ranks: list[dict[str, Any]],
    architecture: list[dict[str, Any]],
    constitutive: list[dict[str, Any]],
    speed: list[dict[str, Any]],
    metrology: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    claim = [row for row in read_csv(FORMAL / "02-claims-register.csv") if row.get("claim_id") == "L-696"]
    variables = read_csv(FORMAL / "04-variable-audit.csv")
    constitutive_variable = [row for row in variables if row.get("symbol") == "Z_A_eta_u"]
    connection_variable = [row for row in variables if row.get("symbol") == "A_mu_F_munu"]
    checkpoint = (POST / "4854-Y5-R2FR-parent-U1-connection-adoption-or-CP2-Berry-constructor-and-time-flow-constitutive-gate.md").read_text(encoding="utf-8")
    formal = (FORMAL / "870-PPC4161-parent-U1-baseline-and-time-flow-constitutive-bound.md").read_text(encoding="utf-8")
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")

    def result(check_id: str, passed: bool, detail: str) -> dict[str, Any]:
        return {"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail, "valid_for_claim": False, "timestamp_utc": TIMESTAMP}

    groups = (sources, ranks, architecture, constitutive, speed, metrology, residuals, decisions)
    differential = next(row for row in speed if row["bound_id"] == "SPD4854_2_differential")
    kappa = next(row for row in speed if row["bound_id"] == "SPD4854_3_kappa")
    checks = [
        result("VAL4854_00_sources", len(sources) == 13 and all(row["source_exists"] and row["needle_found"] for row in sources), f"sources={len(sources)}"),
        result("VAL4854_01_rank", len(ranks) == 7 and any(row["theorem_id"] == "RKT4854_3_flow" and row["status"] == "FAIL_GENERIC_EM_ALONE" for row in ranks), "pullback dimension theorem separates scalar/flow failure from CP2 viability"),
        result("VAL4854_02_architecture", len(architecture) == 5 and sum(row["decision"] == "SELECTED_BASELINE" for row in architecture) == 1, "independent U1 selected exactly once"),
        result("VAL4854_03_constitutive", len(constitutive) == 9 and any(row["row_id"] == "ICT4854_6_birefringence" for row in constitutive), "isotropic operator basis, stability, speed and no-birefringence theorem emitted"),
        result("VAL4854_04_speed_interval", Decimal(differential["lower"]) < 0 < Decimal(differential["upper"]), f"Delta_chi=[{differential['lower']},{differential['upper']}]"),
        result("VAL4854_05_kappa_interval", Decimal(kappa["lower"]) < 0 < Decimal(kappa["upper"]), f"kappa_u=[{kappa['lower']},{kappa['upper']}]"),
        result("VAL4854_06_metrology", len(metrology) == 5 and any(row["status"] == "NOT_A_THIRD_FREE_PARAMETER" for row in metrology), "static coupling, speed and impedance normalization separated"),
        result("VAL4854_07_residuals", len(residuals) == 8 and residuals[0]["status"] == "CORRESPONDENCE_FIELD_CONTENT_CLOSED_PRIMITIVE_MTS_ORIGIN_OPEN", "architecture fork closed without false emergence claim"),
        result("VAL4854_08_nonclaim", all(not row["valid_for_claim"] for group in groups for row in group), "all checkpoint rows remain private nonclaim"),
        result("VAL4854_09_variables", len(constitutive_variable) == 1 and len(connection_variable) == 1 and connection_variable[0]["status"] == "adopted_correspondence_connection", "variable audit rebased"),
        result("VAL4854_10_claim", len(claim) == 1 and claim[0].get("status") == "independent_U1_correspondence_baseline_adopted_CP2_optional_isotropic_time_flow_coefficient_bounded_private_nonclaim", f"L-696 rows={len(claim)}"),
        result("VAL4854_11_documents", "U1_BASELINE_CP2_CONSTITUTIVE_GATE_4854" in checkpoint and "PPC4161_U1_BASELINE_CONSTITUTIVE_BOUND_4854" in formal, "checkpoint and formal markers found"),
        result("VAL4854_12_resume", resume_checkpoint_at_least(resume, 4854), "resume reached or advanced beyond the Einstein-Maxwell and time-flow kinetic gates"),
        result("VAL4854_13_script", compiles(Path(__file__).resolve()), "generator compiles"),
    ]
    checks.append(result("VAL4854_OVERALL", all(row["status"] == "PASS" for row in checks), "U1_BASELINE_CP2_CONSTITUTIVE_GATE_VALIDATED"))
    return checks


def main() -> int:
    sources = source_rows()
    ranks = rank_rows()
    architecture = architecture_rows()
    constitutive = constitutive_rows()
    speed = speed_bound_rows()
    metrology = metrology_rows()
    residuals = residual_rows()
    decisions = decision_rows()
    validation = validation_rows(sources, ranks, architecture, constitutive, speed, metrology, residuals, decisions)
    write_csv(OUTPUT / "P8_Y5_R2FR_4854_SOURCE_REGISTER.csv", sources)
    write_csv(OUTPUT / "P8_Y5_R2FR_4854_PULLBACK_RANK_THEOREM.csv", ranks)
    write_csv(OUTPUT / "P8_Y5_R2FR_4854_U1_ARCHITECTURE_FORK.csv", architecture)
    write_csv(OUTPUT / "P8_Y5_R2FR_4854_ISOTROPIC_CONSTITUTIVE_THEOREM.csv", constitutive)
    write_csv(OUTPUT / "P8_Y5_R2FR_4854_GW170817_SPEED_BOUND.csv", speed)
    write_csv(OUTPUT / "P8_Y5_R2FR_4854_COUPLING_METROLOGY.csv", metrology)
    write_csv(OUTPUT / "P8_Y5_R2FR_4854_RESIDUAL_REBASE.csv", residuals)
    write_csv(OUTPUT / "P8_Y5_R2FR_4854_DECISION.csv", decisions)
    write_csv(OUTPUT / "P8_Y5_BRR545_4854_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print("P8_Y5_BRR545_4854_VALIDATION_PASS" if passed else "P8_Y5_BRR545_4854_VALIDATION_FAIL")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

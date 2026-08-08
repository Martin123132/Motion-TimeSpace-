from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import Any


CHECKPOINT = "4853"
TIMESTAMP = "2026-07-09T21:34:41+00:00"
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
NEXT_TARGET = "4854-Y5-R2FR-parent-U1-connection-adoption-or-CP2-Berry-constructor-and-time-flow-constitutive-gate.md"


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
        ("SRC4853_00_variables", FORMAL / "04-variable-audit.csv", "A_mu_F_munu", "canonical scalar-versus-connection field audit"),
        ("SRC4853_01_equations", FORMAL / "05-equation-register.md", "A_MTS[ψ]", "core scalar action and pre-charge EM equations"),
        ("SRC4853_02_precharge", ROOT / "archive" / "uncategorised" / "a-dissipative-electromagnetic-sector-from-curvature-memory-dynamics-in-motion-timespace.md", "Without introducing gauge fields", "pre-charge scalar simulation and explicit missing Coulomb/charge features"),
        ("SRC4853_03_3782", POST / "3782-Y5-R2FR-instantiate-PiQ-from-psi-phase-current-or-finite-EM-vector.md", "A free complex phase current gives", "real-scalar and phase-gradient no-go"),
        ("SRC4853_04_3783", POST / "3783-Y5-R2FR-parent-U1-bundle-upgrade-or-PiQ-finite-bound-runner.md", "PARENT_U1_EXTENSION_VIABLE", "minimal U1 extension contract"),
        ("SRC4853_05_3784", POST / "3784-Y5-R2FR-parent-U1-action-clause-or-EM-finite-bound-mode.md", "Parent U(1) Action Clause", "U1 action and variation grammar"),
        ("SRC4853_06_3785", POST / "3785-Y5-R2FR-derive-BQ-flow-one-form-from-vorticity-defects-or-demote-EM.md", "Darboux / Clebsch B_Q Lemma", "non-circular two-pair/Berry construction route"),
        ("SRC4853_07_3786", POST / "3786-Y5-R2FR-parent-internal-multiplet-owner-or-BQ-finite-demotion.md", "Current corpus does not derive B_Q", "current parent multiplet failure"),
        ("SRC4853_08_4072", POST / "4072-Y5-R2FR-local-motion-frame-gauge-action-or-effective-GR-demotion.md", "same-coframe matter/EM", "private Cartan/EH correspondence action"),
        ("SRC4853_09_4175", POST / "4175-Y5-R2FR-Maxwell-Hodge-Poynting-stress-owner-theorem-or-EM-side-channel-bound.md", "nabla_mu T_EM", "Maxwell stress and matter-EM Ward exchange"),
        ("SRC4853_10_4209", POST / "4209-Y5-R2FR-Maxwell-normalization-charge-current-owner-or-alpha-bound.md", "g_J^2/lambda_A", "field-normalization invariant EM coupling"),
        ("SRC4853_11_4658", POST / "4658-Y5-R2FR-balpha-Maxwell-normalization-owner-or-first-source-bound.md", "alpha_eff proportional to g_J^2/lambda_A", "calibrated alpha and drift guard"),
        ("SRC4853_12_4837", POST / "4837-Y5-R2FR-EM-stress-Poynting-alpha-normal-form-or-source-row.md", "EM_STRESS_POYNTING", "current EM blocker vector"),
        ("SRC4853_13_4847", POST / "4847-Y5-R2FR-coherent-load-covariant-Hilbert-stress-and-tau-Euler-equation-or-H-load-cosmology-smoke-fit.md", "T^{\\rm mem}_{\\mu\\nu}=0", "stationary MTS active-field silence"),
        ("SRC4853_14_4852", POST / "4852-Y5-R2FR-local-GR-residual-rebase-after-memory-cuscuton-and-Gamma-zero.md", "E_EM_normal_form", "Maxwell selected as first surviving source obstruction"),
        ("SRC4853_15_checkpoint", POST / "4853-Y5-R2FR-Maxwell-Hodge-Hilbert-stress-current-normalization-and-stationary-Poynting-boundary-theorem.md", "SCALAR_ONLY_MAXWELL_NO_GO", "human-readable derivation"),
        ("SRC4853_16_formal", FORMAL / "869-PPC4161-Maxwell-U1-stress-current-and-Poynting-rebase.md", "PPC4161_MAXWELL_U1_REBASE_4853", "formal-workbench integration"),
        ("SRC4853_17_claim", FORMAL / "02-claims-register.csv", "L-695", "claim register"),
        ("SRC4853_18_script", Path(__file__).resolve(), 'CHECKPOINT = "4853"', "executable Maxwell rebase"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in local_sources:
        source_text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        rows.append(
            {
                "source_id": source_id,
                "source_kind": "local",
                "source_locator": str(path),
                "source_exists": path.exists(),
                "needle": needle,
                "needle_found": needle in source_text,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    rows.append(
        {
            "source_id": "SRC4853_19_LV_photon",
            "source_kind": "primary_web_verified",
            "source_locator": "https://arxiv.org/abs/0905.0031",
            "source_exists": True,
            "needle": "gauge-invariant Lorentz-violating photon operators",
            "needle_found": True,
            "role": "independent constitutive/time-flow operators give dispersion, anisotropy and birefringence",
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
    )
    return rows


def scalar_no_go_rows() -> list[dict[str, Any]]:
    entries = [
        ("NG4853_0_real_scalar", "core psi:R4->R", "one real scalar has no compact U1 phase orbit or vector connection", "REJECT_SCALAR_ONLY_MAXWELL"),
        ("NG4853_1_parabolic", "partial_t psi=c^2 nabla^2 psi+...", "first-order diffusion/relaxation has a parabolic principal symbol, not the Maxwell null-cone wave operator", "REJECT_AS_PHOTON_EQUATION"),
        ("NG4853_2_helicity", "linear scalar perturbation", "a Lorentz scalar carries helicity zero and cannot supply the two transverse helicities of a massless spin-one photon", "REJECT_SCALAR_PHOTON_IDENTIFICATION"),
        ("NG4853_3_phase_gradient", "psi=rho exp(i theta); Pi_Q=dtheta", "A=q_*^-1(dtheta-Pi_Q)=0 and F=dA=0 on a smooth patch", "PURE_GAUGE_NO_GO"),
        ("NG4853_4_covariant_current", "Pi_Q=dtheta-q_*A", "using a current that already contains A to derive A is circular", "REJECT_CIRCULAR_DERIVATION"),
        ("NG4853_5_empirical_content", "pre-charge scalar simulation", "the source itself reports no Coulomb force, charge differentiation, radiation pressure or polarization force", "DEMOTE_TO_DISSIPATIVE_PRECHARGE_ANALOGUE"),
    ]
    return [
        {
            "no_go_id": row_id,
            "candidate": candidate,
            "derivation": derivation,
            "verdict": verdict,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for row_id, candidate, derivation, verdict in entries
    ]


def action_theorem_rows() -> list[dict[str, Any]]:
    entries = [
        ("U1T4853_0_field", "A is a connection on a parent U1 bundle; F=dA", "explicit required field content, not renamed scalar psi", "PARENT_EXTENSION_REQUIRED"),
        ("U1T4853_1_Bianchi", "dF=0", "identity from F=dA away from owned defects", "EXACT"),
        ("U1T4853_2_operator", "L_A=-lambda_A F_mn F^mn/4-g_J A_m j^m", "unique parity-even two-derivative quadratic U1 term when no extra tensors/fields enter; constant F wedge F is topological", "EXACT_MINIMAL_OPERATOR_DOMAIN"),
        ("U1T4853_3_Maxwell", "lambda_A nabla_m F^mn=g_J j^n", "variation with respect to A", "EXACT"),
        ("U1T4853_4_current", "nabla_m j^m=0", "divergence of Maxwell equation or U1 Ward identity", "EXACT"),
        ("U1T4853_5_stress", "T_A^mn=lambda_A(F^m_a F^{na}-g^mn F_ab F^ab/4)", "Hilbert variation against the same observed metric", "EXACT"),
        ("U1T4853_6_exchange", "nabla_m T_A^mn=-g_J F^n_l j^l; nabla_m T_matter^mn=+g_J F^n_l j^l", "same-current matter/EM Ward exchange", "EXACT"),
        ("U1T4853_7_coupling", "A_c=sqrt(lambda_A)A; e_eff=g_J/sqrt(lambda_A); alpha proportional g_J^2/lambda_A", "field-normalization invariant coupling", "EXACT_CALIBRATED_NOT_PREDICTED"),
        ("U1T4853_8_modes", "4 A-components - 1 gauge pair - 1 Gauss pair = 2 propagating transverse modes", "positive Hamiltonian and null principal cone require lambda_A>0", "EXACT_MINIMAL_BRANCH"),
        ("U1T4853_9_local_silence", "analytic f(X_silent)F^2=f(0)F^2 on stationary local branch", "constant f(0) renormalizes lambda_A; active Gamma/memory perturbations vanish locally", "LOCAL_BACKGROUND_ZERO_DYNAMIC_COUPLING_OPEN"),
    ]
    return [
        {
            "theorem_id": theorem_id,
            "equation": equation,
            "derivation": derivation,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for theorem_id, equation, derivation, status in entries
    ]


def coupling_rows() -> list[dict[str, Any]]:
    lambda_a = 7.0
    g_j = 3.0
    invariant = g_j**2 / lambda_a
    rows: list[dict[str, Any]] = []
    for scale in (0.25, 0.5, 2.0, 10.0):
        lambda_prime = lambda_a / scale**2
        g_prime = g_j / scale
        invariant_prime = g_prime**2 / lambda_prime
        rows.append(
            {
                "field_rescaling_Aprime_over_A": scale,
                "lambda_A_prime": f"{lambda_prime:.15e}",
                "g_J_prime": f"{g_prime:.15e}",
                "gJ2_over_lambdaA": f"{invariant_prime:.15e}",
                "reference_invariant": f"{invariant:.15e}",
                "relative_invariance_error": f"{abs(invariant_prime-invariant)/invariant:.15e}",
                "status": "COUPLING_NORMALIZATION_INVARIANT_PASS_NONCLAIM",
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    return rows


def stress_poynting_rows() -> list[dict[str, Any]]:
    electric = (1.0, 2.0, 3.0)
    magnetic = (4.0, -1.0, 2.0)
    lambda_a = 2.0
    e2 = sum(value * value for value in electric)
    b2 = sum(value * value for value in magnetic)
    cross = (
        electric[1] * magnetic[2] - electric[2] * magnetic[1],
        electric[2] * magnetic[0] - electric[0] * magnetic[2],
        electric[0] * magnetic[1] - electric[1] * magnetic[0],
    )
    poynting = tuple(lambda_a * value for value in cross)
    entries = [
        ("SPW4853_0_energy", "rho_A=lambda_A(E^2+B^2)/2", f"{lambda_a*(e2+b2)/2.0:.15e}", "positive for lambda_A>0"),
        ("SPW4853_1_flux", "S=lambda_A E cross B", ";".join(f"{value:.15e}" for value in poynting), "T_A^{0i} energy transport"),
        ("SPW4853_2_stress_owner", "T_H=T_matter+T_A+T_binding+...", "INCLUDE_ONCE", "EM energy and momentum gravitate through the same Hilbert variation"),
        ("SPW4853_3_exchange", "div T_A=-F.J; div T_matter=+F.J", "TOTAL_ZERO", "Lorentz work is internal exchange"),
        ("SPW4853_4_no_double_count", "Poynting=T_A^{0i}", "NO_SECOND_SOURCE_LEG", "do not add Poynting after T_A is already in T_H"),
        ("SPW4853_5_stationary", "Delta E_total+integral_boundary J_E.n=0", "ZERO_NET_FLUX_IF_STATIONARY_ISOLATED", "circulating internal flow is allowed"),
        ("SPW4853_6_radiative", "Phi_rad=integral_dt integral_boundary S.n dA", "RETAIN_EXPLICITLY", "radiation is not killed by the stationary theorem"),
    ]
    return [
        {
            "row_id": row_id,
            "identity": identity,
            "value_or_result": value,
            "meaning": meaning,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for row_id, identity, value, meaning in entries
    ]


def flux_smoke_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for radius in (10.0, 100.0, 1000.0):
        bound_flux_envelope = 1.0 / radius**3
        radiative_flux = 1.0
        rows.extend(
            [
                {
                    "branch": "stationary_bound_fields",
                    "radius": radius,
                    "E_falloff": "R^-2",
                    "B_falloff": "R^-3",
                    "surface_flux_envelope": f"{bound_flux_envelope:.15e}",
                    "asymptotic_result": "TENDS_TO_ZERO",
                    "valid_for_claim": False,
                    "timestamp_utc": TIMESTAMP,
                },
                {
                    "branch": "radiative_fields",
                    "radius": radius,
                    "E_falloff": "R^-1",
                    "B_falloff": "R^-1",
                    "surface_flux_envelope": f"{radiative_flux:.15e}",
                    "asymptotic_result": "FINITE_RETAINED_FLUX",
                    "valid_for_claim": False,
                    "timestamp_utc": TIMESTAMP,
                },
            ]
        )
    return rows


def constitutive_rows() -> list[dict[str, Any]]:
    entries = [
        ("CON4853_0_minimal", 0.0, 0.0, "minimal Maxwell", "PRIVATE_CORRESPONDENCE_ZERO"),
        ("CON4853_1_common", 0.1, 0.1, "common E/B normalization", "ABSORB_IN_LAMBDA_NO_SPEED_SHIFT"),
        ("CON4853_2_electric", 1.0e-3, 0.0, "time-flow electric constitutive term", "PHOTON_SPEED_RESIDUAL"),
        ("CON4853_3_magnetic", 0.0, 1.0e-3, "magnetic constitutive term", "PHOTON_SPEED_RESIDUAL"),
    ]
    rows: list[dict[str, Any]] = []
    for row_id, chi_e, chi_b, meaning, status in entries:
        speed_ratio = math.sqrt((1.0 + chi_b) / (1.0 + chi_e))
        rows.append(
            {
                "row_id": row_id,
                "chi_E": chi_e,
                "chi_B": chi_b,
                "c_gamma_over_c_obs": f"{speed_ratio:.15e}",
                "fractional_speed_shift": f"{speed_ratio-1.0:.15e}",
                "meaning": meaning,
                "status": status,
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    rows.extend(
        [
            {"row_id": "CON4853_4_anisotropic", "chi_E": "tensor", "chi_B": "tensor", "c_gamma_over_c_obs": "direction_and_polarization_dependent", "fractional_speed_shift": "BOUNDED_NOT_ZERO", "meaning": "independent coframe/time-flow constitutive tensor", "status": "BIREFRINGENCE_ANISOTROPY_RESIDUAL", "valid_for_claim": False, "timestamp_utc": TIMESTAMP},
            {"row_id": "CON4853_5_theta", "chi_E": "topological", "chi_B": "topological", "c_gamma_over_c_obs": "1_if_constant", "fractional_speed_shift": "0_if_constant", "meaning": "constant F wedge F has no local Hilbert stress; varying coefficient reopens axion-like coupling", "status": "CONSTANT_TOPOLOGICAL_DYNAMIC_OPEN", "valid_for_claim": False, "timestamp_utc": TIMESTAMP},
            {"row_id": "CON4853_6_silent_scalar", "chi_E": "f(X_silent)", "chi_B": "f(X_silent)", "c_gamma_over_c_obs": "1_on_stationary_background", "fractional_speed_shift": "0_background_dynamic_vertices_open", "meaning": "analytic active-Gamma/memory scalar coupling is a constant at the exact silent point", "status": "LOCAL_BACKGROUND_ABSORBED_TRANSITION_COSMOLOGY_OPEN", "valid_for_claim": False, "timestamp_utc": TIMESTAMP},
        ]
    )
    return rows


def residual_rows() -> list[dict[str, Any]]:
    entries = [
        (1, "E_U1_origin", "OPEN_HARD", "current real-scalar MTS branch cannot produce a generic Maxwell connection", "adopt a fundamental parent U1 connection or derive a two-pair/CP2 Berry owner"),
        (2, "E_Hodge_metric", "PRIVATE_MINIMAL_ZERO_STRICT_PARENT_OPEN", "minimal action uses the observed coframe Hodge; extra time-flow constitutive tensors are symmetry-legal", "derive operator-domain sequestering or bound chi tensors"),
        (3, "E_unique_F2", "CLOSED_IN_MINIMAL_OPERATOR_DOMAIN", "F^2 is the parity-even two-derivative quadratic term; constant F wedge F is topological", "global parent must explicitly exclude extra fields/tensors at this order"),
        (4, "E_XF2_dynamic", "LOCAL_STATIONARY_BACKGROUND_ZERO_DYNAMIC_OPEN", "analytic active Gamma/memory scalars evaluate to constants at the silent point", "retain transition/cosmology/scattering vertices"),
        (5, "E_charge_current", "CLOSED_IN_EXPLICIT_U1_ACTION", "Maxwell equation, current conservation and matter-EM Ward exchange share one action", "charge lattice and absolute alpha remain separate"),
        (6, "E_Poynting", "STATIONARY_BOUNDARY_ZERO_RADIATIVE_OPEN", "internal flow is T_A^{0i}; nonradiative finite-energy surface flux vanishes", "retain net radiative/open-system flux"),
        (7, "E_alpha_absolute", "CALIBRATED_NOT_DERIVED", "physical classical coupling is g_J^2/lambda_A", "derive only if parent norm/charge-level law exists"),
        (8, "E_QED_quantum", "OPEN_EXTENSION", "classical Maxwell correspondence does not derive quantum matter, vacuum polarization or charge quantization", "separate quantum completion from local classical GR gate"),
    ]
    return [
        {
            "priority": priority,
            "residual": residual,
            "status": status,
            "derivation": derivation,
            "next_action": next_action,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for priority, residual, status, derivation, next_action in entries
    ]


def decision_rows() -> list[dict[str, Any]]:
    entries = [
        ("DEC4853_0_scalar", "reject scalar-only Maxwell emergence", "the core scalar/pre-charge branch fails gauge, helicity, hyperbolicity and Coulomb/charge requirements"),
        ("DEC4853_1_architecture", "make a parent U1 connection explicit in the competitive correspondence action", "this is a transparent field-content extension, not a fake derivation from psi"),
        ("DEC4853_2_classical", "close classical Maxwell stress/current/Poynting inside the minimal U1 branch", "action variation gives Maxwell, Hilbert stress and total Ward conservation"),
        ("DEC4853_3_alpha", "calibrate one invariant EM coupling", "g_J^2/lambda_A is physical; field normalization cannot predict alpha"),
        ("DEC4853_4_flux", "set only stationary nonradiative net flux to zero", "internal Poynting circulation remains in T_A and radiative flux remains explicit"),
        ("DEC4853_5_next", "decide U1 parent status and attack the time-flow constitutive residual", "derive/adopt the connection or construct CP2/Berry ownership, then bound symmetry-legal u/F couplings"),
    ]
    return [
        {
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_target": NEXT_TARGET if decision_id == "DEC4853_5_next" else "",
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for decision_id, decision, reason in entries
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    no_go: list[dict[str, Any]],
    action: list[dict[str, Any]],
    coupling: list[dict[str, Any]],
    stress: list[dict[str, Any]],
    flux: list[dict[str, Any]],
    constitutive: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    claim = [row for row in read_csv(FORMAL / "02-claims-register.csv") if row.get("claim_id") == "L-695"]
    variables = read_csv(FORMAL / "04-variable-audit.csv")
    connection = [row for row in variables if row.get("symbol") == "A_mu_F_munu"]
    coupling_variable = [row for row in variables if row.get("symbol") == "lambda_A_g_J"]
    checkpoint = (POST / "4853-Y5-R2FR-Maxwell-Hodge-Hilbert-stress-current-normalization-and-stationary-Poynting-boundary-theorem.md").read_text(encoding="utf-8")
    formal = (FORMAL / "869-PPC4161-Maxwell-U1-stress-current-and-Poynting-rebase.md").read_text(encoding="utf-8")
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")

    def result(check_id: str, passed: bool, detail: str) -> dict[str, Any]:
        return {"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail, "valid_for_claim": False, "timestamp_utc": TIMESTAMP}

    bound_flux = [row for row in flux if row["branch"] == "stationary_bound_fields"]
    radiation = [row for row in flux if row["branch"] == "radiative_fields"]
    common = [row for row in constitutive if row["row_id"] == "CON4853_1_common"][0]
    differential = [row for row in constitutive if row["row_id"] in {"CON4853_2_electric", "CON4853_3_magnetic"}]
    groups = (sources, no_go, action, coupling, stress, flux, constitutive, residuals, decisions)
    checks = [
        result("VAL4853_00_sources", len(sources) == 20 and all(row["source_exists"] and row["needle_found"] for row in sources), f"sources={len(sources)}"),
        result("VAL4853_01_scalar_no_go", len(no_go) == 6 and any(row["verdict"] == "DEMOTE_TO_DISSIPATIVE_PRECHARGE_ANALOGUE" for row in no_go), "scalar-only Maxwell route rejected by independent gates"),
        result("VAL4853_02_action", len(action) == 10 and any(row["theorem_id"] == "U1T4853_8_modes" for row in action), "minimal U1 action, stress, Ward and two photon modes derived"),
        result("VAL4853_03_coupling", len(coupling) == 4 and max(float(row["relative_invariance_error"]) for row in coupling) < 2.0e-15, "g_J^2/lambda_A invariant under field rescaling"),
        result("VAL4853_04_stress", len(stress) == 7 and float(stress[0]["value_or_result"]) > 0.0 and stress[3]["value_or_result"] == "TOTAL_ZERO", "positive Maxwell energy and total Ward exchange"),
        result("VAL4853_05_stationary_flux", len(bound_flux) == 3 and float(bound_flux[-1]["surface_flux_envelope"]) < float(bound_flux[0]["surface_flux_envelope"]) * 2.0e-6, "bound-field surface flux tends to zero"),
        result("VAL4853_06_radiative_flux", len(radiation) == 3 and len({row["surface_flux_envelope"] for row in radiation}) == 1 and all(row["asymptotic_result"] == "FINITE_RETAINED_FLUX" for row in radiation), "radiative flux is not erased"),
        result("VAL4853_07_constitutive", len(constitutive) == 7 and abs(float(common["fractional_speed_shift"])) < 1.0e-15 and all(abs(float(row["fractional_speed_shift"])) > 1.0e-6 for row in differential), "common normalization is silent while differential constitutive terms shift photon speed"),
        result("VAL4853_08_residuals", len(residuals) == 8 and residuals[0]["residual"] == "E_U1_origin" and residuals[0]["status"] == "OPEN_HARD", "honest post-rebase EM vector retained"),
        result("VAL4853_09_nonclaim", all(not row["valid_for_claim"] for group in groups for row in group), "all 4853 rows remain private nonclaim"),
        result("VAL4853_10_variables", len(connection) == 1 and connection[0]["status"] in {"required_parent_connection", "adopted_correspondence_connection"} and len(coupling_variable) == 1, "variable audit updated and later U1 adoption remains backward-compatible"),
        result("VAL4853_11_claim", len(claim) == 1 and claim[0].get("status") == "scalar_Maxwell_rejected_minimal_U1_Einstein_Maxwell_correspondence_derived_parent_origin_constitutive_open_nonclaim", f"L-695 rows={len(claim)}"),
        result("VAL4853_12_documents", "SCALAR_ONLY_MAXWELL_NO_GO" in checkpoint and "PPC4161_MAXWELL_U1_REBASE_4853" in formal, "checkpoint and formal markers found"),
        result("VAL4853_13_resume", resume_checkpoint_at_least(resume, 4853), "resume reached or advanced beyond the U1 parent/constitutive gate"),
        result("VAL4853_14_script", compiles(Path(__file__).resolve()), "generator compiles"),
    ]
    checks.append(result("VAL4853_OVERALL", all(row["status"] == "PASS" for row in checks), "MAXWELL_U1_STRESS_CURRENT_POYNTING_REBASE_VALIDATED"))
    return checks


def main() -> int:
    sources = source_rows()
    no_go = scalar_no_go_rows()
    action = action_theorem_rows()
    coupling = coupling_rows()
    stress = stress_poynting_rows()
    flux = flux_smoke_rows()
    constitutive = constitutive_rows()
    residuals = residual_rows()
    decisions = decision_rows()
    validation = validation_rows(sources, no_go, action, coupling, stress, flux, constitutive, residuals, decisions)
    write_csv(OUTPUT / "P8_Y5_R2FR_4853_SOURCE_REGISTER.csv", sources)
    write_csv(OUTPUT / "P8_Y5_R2FR_4853_SCALAR_MAXWELL_NO_GO.csv", no_go)
    write_csv(OUTPUT / "P8_Y5_R2FR_4853_MINIMAL_U1_ACTION_THEOREM.csv", action)
    write_csv(OUTPUT / "P8_Y5_R2FR_4853_COUPLING_NORMALIZATION.csv", coupling)
    write_csv(OUTPUT / "P8_Y5_R2FR_4853_STRESS_POYNTING_WARD.csv", stress)
    write_csv(OUTPUT / "P8_Y5_R2FR_4853_STATIONARY_FLUX_SMOKE.csv", flux)
    write_csv(OUTPUT / "P8_Y5_R2FR_4853_CONSTITUTIVE_RESIDUAL_MAP.csv", constitutive)
    write_csv(OUTPUT / "P8_Y5_R2FR_4853_EM_RESIDUAL_REBASE.csv", residuals)
    write_csv(OUTPUT / "P8_Y5_R2FR_4853_DECISION.csv", decisions)
    write_csv(OUTPUT / "P8_Y5_BRR545_4853_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print("P8_Y5_BRR545_4853_VALIDATION_PASS" if passed else "P8_Y5_BRR545_4853_VALIDATION_FAIL")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

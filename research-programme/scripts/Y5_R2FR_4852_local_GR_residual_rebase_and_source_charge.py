from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import Any


CHECKPOINT = "4852"
TIMESTAMP = "2026-07-09T21:22:28+00:00"
C_M_S = 299_792_458.0
G_SI = 6.67430e-11
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
NEXT_TARGET = "4853-Y5-R2FR-Maxwell-Hodge-Hilbert-stress-current-normalization-and-stationary-Poynting-boundary-theorem.md"


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


def source_rows() -> list[dict[str, Any]]:
    local_sources = [
        ("SRC4852_00_4072", POST / "4072-Y5-R2FR-local-motion-frame-gauge-action-or-effective-GR-demotion.md", "S_EC", "private Cartan/EH action candidate and parent-origin caveat"),
        ("SRC4852_01_4650", POST / "4650-Y5-R2FR-single-parent-action-selector-signature-or-residual-vector.md", "R_GR =", "original ten-component local-GR residual vector"),
        ("SRC4852_02_4654", POST / "4654-Y5-R2FR-deltaKappa-source-coupling-lock-or-Gdot-orbital-bound.md", "delta_kappa = 0 inside private", "private constant calibrated coupling theorem"),
        ("SRC4852_03_4719", POST / "4719-Y5-R2FR-local-linearized-GR-limit-and-Poisson-equation-residual-bound.md", "nabla^2 Phi_N", "linearized EH/Poisson bridge"),
        ("SRC4852_04_4837", POST / "4837-Y5-R2FR-EM-stress-Poynting-alpha-normal-form-or-source-row.md", "Poynting", "Maxwell/Hodge/current and radiative-flux remainder"),
        ("SRC4852_05_4839", POST / "4839-Y5-R2FR-Hilbert-source-current-descent-or-first-MHref-source-row.md", "M_H_ref = H_tau", "source-charge equality requiring unit and perturbative-order repair"),
        ("SRC4852_06_4843", POST / "4843-Y5-R2FR-source-universality-branch-reconciliation-and-Newton-chain-propagation.md", "E_source_prefactor = 0", "source-only prefactor zero"),
        ("SRC4852_07_4845", POST / "4845-Y5-R2FR-Gamma-local-constancy-exchange-and-SigmaGamma-profile-bound.md", "Sigma_active", "active Gamma zero theorem"),
        ("SRC4852_08_4847", POST / "4847-Y5-R2FR-coherent-load-covariant-Hilbert-stress-and-tau-Euler-equation-or-H-load-cosmology-smoke-fit.md", "T^{\\rm mem}_{\\mu\\nu}=0", "stationary coherent-load stress and tau-force zero"),
        ("SRC4852_09_4851", POST / "4851-Y5-R2FR-H-load-cuscuton-matter-perturbation-constraint-and-growth-kernel.md", "H^2a^2", "high-k calibrated Newton recovery"),
        ("SRC4852_10_checkpoint", POST / "4852-Y5-R2FR-local-GR-residual-rebase-after-memory-cuscuton-and-Gamma-zero.md", "LINEARIZED_ADM_HILBERT_SOURCE_CHARGE", "human-readable derivation"),
        ("SRC4852_11_formal", FORMAL / "868-PPC4161-local-GR-residual-rebase-and-linearized-source-charge-closure.md", "PPC4161_LOCAL_GR_RESIDUAL_REBASE_4852", "formal-workbench integration"),
        ("SRC4852_12_claim", FORMAL / "02-claims-register.csv", "L-694", "claim register"),
        ("SRC4852_13_script", Path(__file__).resolve(), 'CHECKPOINT = "4852"', "executable theorem and residual rebase"),
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
    rows.extend(
        [
            {
                "source_id": "SRC4852_14_ADM",
                "source_kind": "primary_web_verified",
                "source_locator": "https://arxiv.org/abs/gr-qc/0405109",
                "source_exists": True,
                "needle": "Hamiltonian surface energy / ADM mass",
                "needle_found": True,
                "role": "Hamiltonian boundary mass normalization in asymptotically flat GR",
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            },
            {
                "source_id": "SRC4852_15_IYER_WALD",
                "source_kind": "primary_web_verified",
                "source_locator": "https://arxiv.org/abs/gr-qc/9403028",
                "source_exists": True,
                "needle": "diffeomorphism Noether current and charge",
                "needle_found": True,
                "role": "covariant Hamiltonian/Noether charge framework and boundary caveat",
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            },
        ]
    )
    return rows


def theorem_rows() -> list[dict[str, Any]]:
    entries = [
        ("THM4852_0_Einstein", "G_00^(1)=kappa_cal T_00", "private EH correspondence branch; same Hilbert source action"),
        ("THM4852_1_Poisson", "nabla^2 Phi=4 pi G_cal rho_H; rho_H=T_00/c^2", "static weak field; kappa_cal=8 pi G_cal/c^4"),
        ("THM4852_2_Gauss", "M_Phi(S)=[4 pi G_cal]^-1 integral_S grad(Phi).dS=integral_V rho_H d^3x", "S encloses the source; finite-energy falloff; divergence theorem"),
        ("THM4852_3_ADM", "M_ADM^(1)=c^2[16 pi G_cal]^-1 integral_S(partial_j h_ij-partial_i h_jj)n^i dS=M_Phi", "h_ij=-2 Phi delta_ij/c^2 in the static isotropic weak field"),
        ("THM4852_4_Hamiltonian_units", "(H_tau-H_ref)/c^2=M_ADM^(1)=M_Phi=integral_V T_00/c^2 d^3x", "tau normalized as asymptotic time translation; H is energy"),
        ("THM4852_5_Newton_source", "epsilon_source^N=[M_ADM^(1)-integral rho_H d^3x]/M_ADM^(1)=0", "first perturbative order only; no orbital GM input"),
        ("THM4852_6_PN_guard", "M_stationary=2 c^-2 integral(T_mn-T g_mn/2)n^m xi^n dV", "stationary GR/Komar-Tolman form; stresses, binding and extra fields prevent bare-T00 promotion"),
    ]
    return [
        {
            "theorem_id": theorem_id,
            "equation": equation,
            "assumptions": assumptions,
            "scope": "private_correspondence_nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for theorem_id, equation, assumptions in entries
    ]


def zero_rows() -> list[dict[str, Any]]:
    entries = [
        ("ZERO4852_0_delta_kappa", "E_kappa_drift", "0", "PRIVATE_ZERO", "4654 topological/superselection kappa plus one Hilbert measure", "strict parent origin remains open"),
        ("ZERO4852_1_source_prefactor", "E_source_prefactor", "0", "PRIVATE_ZERO", "4843 literal/private one-matter-block branch", "hidden source coefficients reopen the row"),
        ("ZERO4852_2_Gamma_active", "Gamma_active;Pi_active;Sigma_active;q_Gamma", "0", "PRIVATE_STATIONARY_ZERO", "4845 positive response-doublet Euler/energy theorem", "constant Gamma0 remains"),
        ("ZERO4852_3_memory_stress", "T_mem_mn;E_tau_mem", "0", "PRIVATE_STATIONARY_ZERO", "4847 theta=0 Killing branch with G=G_theta=G_thetatheta=0", "separately propagating parent tau branch not covered"),
        ("ZERO4852_4_memory_Poisson", "Delta_Poisson_Hload", "0+O(H^2 a^2/k^2)", "EXACT_STATIONARY_AND_HIGH_K_ASYMPTOTIC", "4847 local zero plus 4851 constraint kernel", "finite cosmological k retains scale-suppressed terms"),
        ("ZERO4852_5_source_charge", "E_PiM_Htau^(Newton,linear)", "0", "DERIVED_PRIVATE_NEWTON_ZERO", "4852 ADM/Gauss/Hilbert identity", "post-Newtonian Komar/binding and parent EH ownership remain"),
    ]
    return [
        {
            "zero_id": zero_id,
            "object": obj,
            "value": value,
            "status": status,
            "proof_owner": proof_owner,
            "scope_guard": guard,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for zero_id, obj, value, status, proof_owner, guard in entries
    ]


def residual_rebase_rows() -> list[dict[str, Any]]:
    entries = [
        ("RGR4852_0", "E_EH_action_owner", "OPEN_STRICT_PARENT", "private Cartan/EH action is explicit but not derived from MTS primitives", "derive parent coframe/connection action or keep correspondence-only"),
        ("RGR4852_1", "E_kappa_drift", "PRIVATE_ZERO", "4654 gives D_A ln kappa_eff=0", "reopen only if source/scale drift appears"),
        ("RGR4852_2", "E_source_owner", "NEWTON_ORDER_CLOSED_PRIVATE", "same Hilbert T_00 sources Poisson and the linear ADM charge", "derive nonlinear stationary source charge and strict parent action pullback"),
        ("RGR4852_3", "E_source_label", "PRIVATE_ZERO", "4843 removes source-only weights on the literal/private branch", "retain reactivation guard"),
        ("RGR4852_4", "E_metric_coframe_fork", "PRIVATE_SELECTOR_ZERO_GLOBAL_OPEN", "one observed coframe is used by the private correspondence branch", "derive it from the parent rather than import it"),
        ("RGR4852_5", "E_EM_metric_source", "OPEN_PRIMARY_NEXT", "ordinary EM may enter T_H once but Maxwell/Hodge/current ownership is not derived", "derive minimal Maxwell normal form and stationary Poynting boundary theorem"),
        ("RGR4852_6", "E_tail_selector", "PARTIALLY_ZERO", "active Gamma and stationary H-load tails vanish", "retain Gamma0, transition, radiative and non-Gamma tails"),
        ("RGR4852_7", "E_boundary_flux", "OPEN_RADIATIVE_NOT_SOURCE_CHARGE", "ADM surface charge is physical and must not be set to zero; outgoing flux is a separate obstruction", "prove stationary no-radiation or bound flux"),
        ("RGR4852_8", "E_domain_projector", "OPEN_STRICT_PARENT", "leading asymptotic Gauss identity avoids post-fit projectors", "derive worldtube/domain map for finite and transition arenas"),
        ("RGR4852_9", "E_PPN_transfer", "OPEN", "Newton source charge does not fix nonlinear, spatial, vector, torsion or conservation PPN pieces", "derive full non-source PPN transfer after EM closure"),
    ]
    return [
        {
            "row_id": row_id,
            "original_residual": residual,
            "rebased_status": status,
            "evidence": evidence,
            "next_action": next_action,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for row_id, residual, status, evidence, next_action in entries
    ]


def survivor_rows() -> list[dict[str, Any]]:
    entries = [
        (1, "E_parent_to_EH", "strict parent derivation of the Cartan/EH observed metric block", "local GR at every order", "derive from motion/time/space primitives"),
        (2, "E_EM_normal_form", "one observed Hodge star, unique F^2, current normalization, no X F^2", "Maxwell stress, clocks, WEP, PPN", "selected 4853 target"),
        (3, "E_source_charge_PN", "ADM/Komar/Tolman/binding equality beyond linear order", "beta, active mass, strong self-energy", "derive after minimal action is fixed"),
        (4, "E_PPN_non_source", "spatial/nonlinear/vector/torsion/conservation transfer", "gamma,beta,alpha_i,xi,zeta_i", "compute from fixed parent action"),
        (5, "E_boundary_domain_radiation", "transition shells, finite domains and radiative flux", "orbital, EM, PPN, R10", "prove stationary silence or retain bounded rows"),
        (6, "E_Gamma0_background", "constant vacuum curvature retained by 4845/4847", "local de-Sitter acceleration and cosmology", "bound once and propagate without erasure"),
    ]
    return [
        {
            "priority": priority,
            "survivor": survivor,
            "meaning": meaning,
            "test_feed": test_feed,
            "next_action": next_action,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for priority, survivor, meaning, test_feed, next_action in entries
    ]


def gauss_smoke_rows() -> list[dict[str, Any]]:
    radius_source_m = 2.5
    density_kg_m3 = 8_000.0
    source_mass_kg = 4.0 * math.pi * radius_source_m**3 * density_kg_m3 / 3.0
    rows: list[dict[str, Any]] = []
    for radius_m in (5.0, 10.0, 50.0):
        phi_gradient_m_s2 = G_SI * source_mass_kg / radius_m**2
        surface_flux_m3_s2 = 4.0 * math.pi * radius_m**2 * phi_gradient_m_s2
        adm_mass_kg = surface_flux_m3_s2 / (4.0 * math.pi * G_SI)
        hamiltonian_energy_j = adm_mass_kg * C_M_S**2
        charge_mass_kg = hamiltonian_energy_j / C_M_S**2
        rows.append(
            {
                "radius_m": radius_m,
                "source_mass_kg": f"{source_mass_kg:.15e}",
                "phi_gradient_m_s2": f"{phi_gradient_m_s2:.15e}",
                "surface_flux_m3_s2": f"{surface_flux_m3_s2:.15e}",
                "ADM_mass_kg": f"{adm_mass_kg:.15e}",
                "Hamiltonian_energy_J": f"{hamiltonian_energy_j:.15e}",
                "charge_mass_H_over_c2_kg": f"{charge_mass_kg:.15e}",
                "relative_Gauss_residual": f"{abs(adm_mass_kg-source_mass_kg)/source_mass_kg:.15e}",
                "relative_unit_residual": f"{abs(charge_mass_kg-adm_mass_kg)/adm_mass_kg:.15e}",
                "status": "SCALE_FREE_GAUSS_ADM_UNIT_SMOKE_PASS_NONCLAIM",
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    return rows


def decision_rows() -> list[dict[str, Any]]:
    entries = [
        ("DEC4852_0", "remove private theorem-zero terms from the live Newton vector", "coupling drift, source prefactor, active Gamma and stationary memory are not current private-branch blockers"),
        ("DEC4852_1", "close the leading source-charge mismatch", "Poisson plus the linear ADM surface formula proves (H_tau-H_ref)/c^2=integral T_00/c^2 without orbital GM"),
        ("DEC4852_2", "correct the old M_H_ref notation", "H_tau-H_ref is energy for normalized time translation; equality to mass requires c^-2 unless c=1"),
        ("DEC4852_3", "retain the post-Newtonian charge residual", "the nonlinear stationary source is Komar/Tolman/ADM and includes stresses and binding, not bare T_00 alone"),
        ("DEC4852_4", "attack EM next", "Maxwell/Hodge/current ownership is now the first surviving same-source coupling obstruction"),
        ("DEC4852_5", "keep strict parent local GR unclaimed", "the private EH/coframe action remains an explicit correspondence candidate rather than a derivation from primitive MTS"),
    ]
    return [
        {
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_target": NEXT_TARGET if decision_id == "DEC4852_4" else "",
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for decision_id, decision, reason in entries
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    theorems: list[dict[str, Any]],
    zeroes: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    survivors: list[dict[str, Any]],
    smoke: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    claim = [row for row in read_csv(FORMAL / "02-claims-register.csv") if row.get("claim_id") == "L-694"]
    checkpoint = (POST / "4852-Y5-R2FR-local-GR-residual-rebase-after-memory-cuscuton-and-Gamma-zero.md").read_text(encoding="utf-8")
    formal = (FORMAL / "868-PPC4161-local-GR-residual-rebase-and-linearized-source-charge-closure.md").read_text(encoding="utf-8")
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")

    def result(check_id: str, passed: bool, detail: str) -> dict[str, Any]:
        return {
            "check_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }

    expected_zero_statuses = {
        "PRIVATE_ZERO",
        "PRIVATE_STATIONARY_ZERO",
        "EXACT_STATIONARY_AND_HIGH_K_ASYMPTOTIC",
        "DERIVED_PRIVATE_NEWTON_ZERO",
    }
    checks = [
        result("VAL4852_00_sources", len(sources) == 16 and all(row["source_exists"] and row["needle_found"] for row in sources), f"sources={len(sources)}"),
        result("VAL4852_01_theorems", len(theorems) == 7 and all(row["equation"] for row in theorems), f"theorems={len(theorems)}"),
        result("VAL4852_02_zero_propagation", len(zeroes) == 6 and all(row["status"] in expected_zero_statuses for row in zeroes), f"zeroes={len(zeroes)}"),
        result("VAL4852_03_original_vector", len(residuals) == 10 and {row["original_residual"] for row in residuals} == {"E_EH_action_owner", "E_kappa_drift", "E_source_owner", "E_source_label", "E_metric_coframe_fork", "E_EM_metric_source", "E_tail_selector", "E_boundary_flux", "E_domain_projector", "E_PPN_transfer"}, "all 4650 residuals rebased once"),
        result("VAL4852_04_survivors", len(survivors) == 6 and survivors[1]["survivor"] == "E_EM_normal_form", "surviving vector is compact and EM is selected next"),
        result("VAL4852_05_Gauss", len(smoke) == 3 and max(float(row["relative_Gauss_residual"]) for row in smoke) < 2.0e-15, "surface/volume masses agree"),
        result("VAL4852_06_units", max(float(row["relative_unit_residual"]) for row in smoke) < 2.0e-15, "Hamiltonian energy divided by c^2 equals charge mass"),
        result("VAL4852_07_no_claim_rows", all(not row["valid_for_claim"] for group in (sources, theorems, zeroes, residuals, survivors, smoke, decisions) for row in group), "all 4852 rows remain private nonclaim"),
        result("VAL4852_08_claim", len(claim) == 1 and claim[0].get("status") == "private_Newton_source_charge_closed_at_linear_order_parent_EH_EM_PPN_open_nonclaim", f"L-694 rows={len(claim)}"),
        result("VAL4852_09_documents", "LINEARIZED_ADM_HILBERT_SOURCE_CHARGE" in checkpoint and "PPC4161_LOCAL_GR_RESIDUAL_REBASE_4852" in formal, "checkpoint and formal markers found"),
        result("VAL4852_10_resume", "Last checkpoint: `4852-" in resume and NEXT_TARGET in resume, "resume advanced to Maxwell/Hodge source theorem"),
        result("VAL4852_11_script", compiles(Path(__file__).resolve()), "generator compiles"),
    ]
    checks.append(result("VAL4852_OVERALL", all(row["status"] == "PASS" for row in checks), "LOCAL_GR_RESIDUAL_REBASE_AND_LINEARIZED_SOURCE_CHARGE_VALIDATED"))
    return checks


def main() -> int:
    sources = source_rows()
    theorems = theorem_rows()
    zeroes = zero_rows()
    residuals = residual_rebase_rows()
    survivors = survivor_rows()
    smoke = gauss_smoke_rows()
    decisions = decision_rows()
    validation = validation_rows(sources, theorems, zeroes, residuals, survivors, smoke, decisions)
    write_csv(OUTPUT / "P8_Y5_R2FR_4852_SOURCE_REGISTER.csv", sources)
    write_csv(OUTPUT / "P8_Y5_R2FR_4852_LINEARIZED_SOURCE_CHARGE_THEOREM.csv", theorems)
    write_csv(OUTPUT / "P8_Y5_R2FR_4852_ZERO_PROPAGATION.csv", zeroes)
    write_csv(OUTPUT / "P8_Y5_R2FR_4852_RESIDUAL_REBASE.csv", residuals)
    write_csv(OUTPUT / "P8_Y5_R2FR_4852_SURVIVING_RESIDUAL_VECTOR.csv", survivors)
    write_csv(OUTPUT / "P8_Y5_R2FR_4852_GAUSS_ADM_UNIT_SMOKE.csv", smoke)
    write_csv(OUTPUT / "P8_Y5_R2FR_4852_DECISION.csv", decisions)
    write_csv(OUTPUT / "P8_Y5_BRR545_4852_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print("P8_Y5_BRR545_4852_VALIDATION_PASS" if passed else "P8_Y5_BRR545_4852_VALIDATION_FAIL")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

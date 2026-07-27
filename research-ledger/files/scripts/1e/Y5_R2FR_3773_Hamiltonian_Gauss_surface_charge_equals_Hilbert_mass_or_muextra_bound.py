import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3773"
BRANCH = "MTS_R2FR_Y5_HAMILTONIAN_GAUSS_SURFACE_CHARGE_EQUALS_HILBERT_MASS_OR_MUEXTRA_BOUND_3773"
PCW = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work"
)
RESIDUALS = PCW / "source-intake" / "mts_residuals"
FORMALIZATION = PCW.parent / "formalization-workbench"
DOC_PATH = PCW / "3773-Y5-R2FR-Hamiltonian-Gauss-surface-charge-equals-Hilbert-mass-or-muextra-bound.md"


OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3773_SOURCE_REGISTER.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_3773_HAMILTONIAN_GAUSS_SURFACE_THEOREM.csv",
    "zero_attempt": RESIDUALS / "P8_Y5_R2FR_3773_HAMILTONIAN_GAUSS_ZERO_ATTEMPT.csv",
    "channels": RESIDUALS / "P8_Y5_R2FR_3773_MUEXTRA_CHANNEL_AUDIT.csv",
    "residuals": RESIDUALS / "P8_Y5_R2FR_3773_MUEXTRA_RESIDUAL_COEFFICIENTS.csv",
    "bound_budget": RESIDUALS / "P8_Y5_R2FR_3773_MUEXTRA_BOUND_BUDGET.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_3773_CLAIM_GATES.csv",
    "decision_rows": RESIDUALS / "P8_Y5_R2FR_3773_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3773_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3773_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3773_VALIDATION.csv",
}


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(timestamp: str, valid_for_claim: bool = False) -> dict[str, object]:
    return {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH,
        "checkpoint_id": CHECKPOINT,
        "valid_for_claim": valid_for_claim,
    }


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_paths() -> dict[str, Path]:
    return {
        "SRC3773_0_3772_doc": PCW / "3772-Y5-R2FR-source-Hamiltonian-normalization-or-Newton-active-passive-GM-bound.md",
        "SRC3773_1_3772_theorem": RESIDUALS / "P8_Y5_R2FR_3772_NEWTON_SOURCE_HAMILTONIAN_THEOREM.csv",
        "SRC3773_2_3772_residuals": RESIDUALS / "P8_Y5_R2FR_3772_NEWTON_GM_RESIDUAL_COEFFICIENTS.csv",
        "SRC3773_3_3772_budget": RESIDUALS / "P8_Y5_R2FR_3772_NEWTON_GM_BOUND_BUDGET.csv",
        "SRC3773_4_Hamiltonian_charge_contract": RESIDUALS / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv",
        "SRC3773_5_Poisson_Gauss_contract": RESIDUALS / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
        "SRC3773_6_Newton_stack": RESIDUALS / "P8_source_normalized_Newton_branch_STACK.csv",
        "SRC3773_7_Hamiltonian_GM_glue": RESIDUALS / "P8_Y5_R2FR_3575_HAMILTONIAN_GM_GLUE_GATES.csv",
        "SRC3773_8_3652_GM_rows": RESIDUALS / "P8_Y5_R2FR_3652_GM_SOURCE_CALIBRATION_ROWS.csv",
        "SRC3773_9_3652_weak_field": RESIDUALS / "P8_Y5_R2FR_3652_WEAK_FIELD_HAMILTONIAN_THEOREM_ATTEMPT.csv",
        "SRC3773_10_3762_range_budget": RESIDUALS / "P8_Y5_R2FR_3762_RANGE_RADIAL_FRAME_RESIDUAL_BUDGET.csv",
        "SRC3773_11_3768_kappa_budget": RESIDUALS / "P8_Y5_R2FR_3768_KAPPA_BOUND_BUDGET.csv",
        "SRC3773_12_3761_ppn_eval": RESIDUALS / "P8_Y5_R2FR_3761_GAMMA_BETA_BOUND_EVALUATION.csv",
        "SRC3773_13_3759_wep_budget": RESIDUALS / "P8_Y5_R2FR_3759_WEP_BOUND_EVALUATION.csv",
        "SRC3773_14_3770_source_budget": RESIDUALS / "P8_Y5_R2FR_3770_SOURCE_ACTION_BOUND_BUDGET.csv",
        "SRC3773_15_3771_theta_budget": RESIDUALS / "P8_Y5_R2FR_3771_CONSTANT_MARKER_BOUND_BUDGET.csv",
    }


def source_register(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "source_id": source_id,
            "source_path": str(path),
            "source_exists": path.exists(),
            "role": "3773 Hamiltonian/Gauss surface charge and mu_extra bound input",
        }
        for source_id, path in source_paths().items()
    ]


def find_row(path: Path, key: str, value: str) -> dict[str, str]:
    for row in read_csv(path):
        if row.get(key) == value:
            return row
    raise KeyError(f"missing row {key}={value} in {path}")


def numeric_inputs() -> dict[str, str]:
    wep = find_row(source_paths()["SRC3773_13_3759_wep_budget"], "evaluation_id", "WB3759_2_max_allowed_residual")
    gamma = find_row(source_paths()["SRC3773_12_3761_ppn_eval"], "evaluation_id", "PGB3761_0_gamma_conditional_zero")
    beta = find_row(source_paths()["SRC3773_12_3761_ppn_eval"], "evaluation_id", "PGB3761_1_beta_conditional_zero")
    gdot = find_row(source_paths()["SRC3773_11_3768_kappa_budget"], "budget_id", "KBB3768_0_Gdot_total")
    return {
        "wep_bound": wep["bound_value"],
        "gamma_bound": gamma["bound_value"],
        "beta_bound": beta["bound_value"],
        "gdot_bound": gdot["bound_value"],
    }


def theorem_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "HGS3773_0_surface_charge_setup",
            "Let xi be the observed stationary/asymptotic time generator and H_xi=B_xi on shell with fixed reference subtraction.",
            "The Hamiltonian boundary variation is the conserved charge candidate only after the observed-time, integrability, and fixed-reference clauses hold.",
            "This makes the exterior mass a charge, not a fitted orbital parameter.",
            "EXACT_CONDITIONAL_SURFACE_CHARGE_SETUP",
        ),
        (
            "HGS3773_1_Hilbert_mass_current",
            "Define M_H[W]=int_{Sigma cap W} Pi_M J_H[tau], where J_H[tau] is the same q_obs Hilbert/coframe source current.",
            "This imports the 3770 same-source route and the Hamiltonian charge contract HC4.",
            "This is the source-side object the exterior surface charge must equal.",
            "EXACT_SOURCE_MASS_DEFINITION",
        ),
        (
            "HGS3773_2_charge_current_equality",
            "If delta B_xi/G_eff = delta int_S Pi_M J_H and the field-space curl, reference, and projector variations are silent, then B_xi/G_eff=M_H+constant.",
            "Integrate the equality of variations on the connected local branch; the fixed reference sets the constant.",
            "This is the Hamiltonian-to-Hilbert mass throat.",
            "EXACT_CONDITIONAL_CHARGE_CURRENT_THEOREM",
        ),
        (
            "HGS3773_3_Gauss_surface_equality",
            "If the EH/Poisson equation holds in the source-free exterior and d(Pi_M J_H)=0 outside compact support, then surface_integral grad Phi dot dS = 4*pi*G_eff M_H.",
            "Integrate nabla^2 Phi=4*pi*G_eff rho_H over the compact volume and apply Gauss/Stokes with no exterior flux or boundary leakage.",
            "This converts local source density into exterior monopole.",
            "EXACT_CONDITIONAL_GAUSS_THEOREM",
        ),
        (
            "HGS3773_4_no_extra_monopole_condition",
            "The measured monopole is mu_obs=G_eff M_H + mu_extra, where mu_extra collects boundary, projector, domain, memory, range, non-EH, coupling, readout, and non-descended EM/Poynting exterior energy channels.",
            "Any channel not varied inside the same Hilbert/coframe source or killed by the exterior constraints contributes an additive monopole residual.",
            "This is where hidden source charge is forced into rows instead of hidden inside G.",
            "EXACT_RESIDUAL_DECOMPOSITION",
        ),
        (
            "HGS3773_5_orbital_readout",
            "If mu_extra=0 and test bodies read the same observed Phi, then a_r=-G_eff M_H/r^2 and mu_fit=G_eff M_H.",
            "Use the slow-particle geodesic/readout limit in the same observed frame after Gauss equality.",
            "This is the final first-order Newton measured-GM step.",
            "EXACT_CONDITIONAL_ORBITAL_READOUT",
        ),
        (
            "HGS3773_6_derivative_hair_law",
            "If the exterior charge is source-clean, then partial_t mu_obs, partial_r mu_obs, partial_A mu_obs, partial_lambda mu_obs, and partial_frame mu_obs vanish; otherwise each derivative is a residual projection of mu_extra and G_eff.",
            "Differentiate mu_obs=G_eff M_H+mu_extra by time/radius/species/range/frame.",
            "This ties radial hair, Gdot, WEP, R10, and frame tests to the same exterior monopole.",
            "EXACT_DERIVATIVE_RESIDUAL_LAW",
        ),
        (
            "HGS3773_7_zero_route",
            "If HGS3773_0 through HGS3773_6 all hold with mu_extra=0, then the 3772 three-mass theorem promotes to a first-order Newton GM recovery theorem.",
            "Combine Hamiltonian-Hilbert charge equality, Gauss surface equality, no-extra-monopole, and orbital readout.",
            "This is not yet local GR, but it is the Newtonian measured-GM bridge.",
            "EXACT_CONDITIONAL_NEWTON_GM_PROMOTION",
        ),
    ]
    return [
        {
            **base(timestamp),
            "theorem_id": theorem_id,
            "statement": statement,
            "derivation": derivation,
            "meaning": meaning,
            "status": status,
            "parent_signed": False,
            "claim_allowed": False,
        }
        for theorem_id, statement, derivation, meaning, status in rows
    ]


def zero_attempt_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("HZA3773_0_theorem_route_emitted", "Hamiltonian/Gauss surface theorem route exists", "HGS3773_2/HGS3773_3/HGS3773_7 emitted", True, "the Newton exterior bridge is mathematically explicit"),
        ("HZA3773_1_observed_time_charge", "H_xi is generated by observed time and has fixed normalization", "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv:HC1 not parent-derived", False, "surface charge may be a reference/readout ambiguity"),
        ("HZA3773_2_integrable_fixed_reference", "H_xi is finite, integrable, and reference-subtraction silent", "HC2/3575 Htau/Href gates remain open or partial", False, "B_xi cannot yet be promoted to mass"),
        ("HZA3773_3_charge_equals_Hilbert_mass", "B_xi/G_eff equals projected Hilbert mass current", "HC4 and PG1 are not parent-derived", False, "epsilon_HH remains live"),
        ("HZA3773_4_closed_projected_flux", "d(Pi_M J_H)=0 and no projector commutator leak outside compact support", "SN4/HC6 not parent-derived", False, "source drift/radial hair remain live"),
        ("HZA3773_5_Gauss_surface_clean", "surface_integral grad Phi equals 4*pi*G_eff M_H with no boundary/domain volume residual", "PG4 not parent-derived", False, "epsilon_Gauss remains live"),
        ("HZA3773_6_no_extra_monopole", "non-EH, projector, boundary, domain, memory, range, coupling, readout, and EM/Poynting channels carry no unowned monopole", "HC5/HGM3575_6 fail open", False, "mu_extra remains live"),
        ("HZA3773_7_orbital_inverse_square", "slow orbital readout is pure inverse-square in same observed frame", "PG5/SN9 not parent-derived", False, "epsilon_orbit remains live"),
        ("HZA3773_8_verdict", "current MTS branch proves exterior GM equals Hilbert mass with mu_extra=0", "conditional theorem exists, but charge, Gauss, no-extra-monopole, and orbital readout clauses are unsigned", False, "do not claim Newton measured-GM closure"),
    ]
    return [
        {
            **base(timestamp),
            "attempt_id": attempt_id,
            "required_clause": required_clause,
            "evidence": evidence,
            "passes_clause": passes_clause,
            "consequence": consequence,
            "claim_allowed": False,
        }
        for attempt_id, required_clause, evidence, passes_clause, consequence in rows
    ]


def channel_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("MEC3773_0_boundary_reference", "Q_boundary_ref", "boundary/reference subtraction or nonintegrable Hamiltonian term", "HC2/HDC fixed-reference and integrability clauses", "MISSING_FIXED_REFERENCE_INTEGRABILITY"),
        ("MEC3773_1_projector_domain", "Q_projector_domain", "Pi_M variation, domain wall, or projector commutator stress", "HC6 and SN4 projected-flux closure", "MISSING_PROJECTOR_DOMAIN_SILENCE"),
        ("MEC3773_2_nonEH_operator", "Q_nonEH", "non-EH exterior constraint/operator contribution to mass charge", "HC0/PG3 and R11 residual route", "MISSING_EH_ONLY_EXTERIOR_OR_R11_VECTOR"),
        ("MEC3773_3_memory_bulk", "Q_memory_bulk", "bulk/memory/topological exterior charge not in the Hilbert source", "HC5 no extra hidden charge", "MISSING_MEMORY_BULK_MONOPOLE_ZERO"),
        ("MEC3773_4_range_fifth_force", "Q_range", "finite-range/Yukawa source charge that adds to inverse-square GM or R10 branch", "3652 alpha_ST/R10 same-source row", "MISSING_RANGE_SOURCE_CHARGE_VECTOR"),
        ("MEC3773_5_coupling_kappa", "Q_delta_kappa", "source/time/range/frame dependence of G_eff or kappa_eff", "3768 Gdot/kappa budgets", "MISSING_COUPLING_SUPERSELECTION_COMPONENTS"),
        ("MEC3773_6_readout_frame", "Q_readout_frame", "orbit/frame/readout mismatch between Phi source and test-body acceleration", "3769/3772 frame and orbit rows", "MISSING_ORBITAL_FRAME_READOUT_PROJECTION"),
        ("MEC3773_7_EM_Poynting", "Q_EM_Poynting", "EM field/Poynting/exterior stress not already included in the same descended Hilbert source", "3760/3770 same-source EM action requirement", "MISSING_EM_POYNTING_HILBERT_DESCENT_OR_ZERO"),
        ("MEC3773_8_source_theta", "Q_source_theta", "source-action or constants/material-marker leakage entering exterior monopole", "3770 source and 3771 theta gates", "MISSING_SOURCE_THETA_DESCENT"),
    ]
    return [
        {
            **base(timestamp),
            "channel_id": channel_id,
            "symbol": symbol,
            "definition": definition,
            "zero_route": zero_route,
            "current_status": current_status,
            "claim_allowed": False,
        }
        for channel_id, symbol, definition, zero_route, current_status in rows
    ]


def residual_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("MUR3773_0_Hamiltonian_Hilbert_gap", "epsilon_HH", "|B_xi/G_eff - M_H|/M_H", "Hamiltonian surface charge not equal to Hilbert mass current", "Newton GM;PPN;WEP", "MISSING_HAMILTONIAN_HILBERT_CHARGE_EQUALITY"),
        ("MUR3773_1_Gauss_gap", "epsilon_Gauss", "|surface_integral grad Phi/(4*pi*G_eff M_H)-1|", "Poisson source does not integrate to the exterior surface mass", "Newton GM;radial hair", "MISSING_GAUSS_SURFACE_EQUALITY"),
        ("MUR3773_2_mu_extra_total", "epsilon_mu_extra", "|mu_extra|/|G_eff M_H|", "total unowned exterior monopole", "Newton GM;PPN;R10;orbital", "MISSING_NO_EXTRA_MONOPOLE_THEOREM_OR_COMPONENTS"),
        ("MUR3773_3_boundary_reference", "epsilon_boundary_ref", "|Q_boundary_ref|/M_H", "boundary/reference/counterterm contribution to measured mass", "Newton GM;Gdot;radial", "MISSING_BOUNDARY_REFERENCE_COMPONENT"),
        ("MUR3773_4_projector_domain", "epsilon_projector_domain", "|Q_projector_domain|/M_H", "projector/domain stress contribution to measured mass", "Newton GM;radial;R10", "MISSING_PROJECTOR_DOMAIN_COMPONENT"),
        ("MUR3773_5_nonEH", "epsilon_nonEH_mass", "|Q_nonEH|/M_H", "non-EH exterior operator mass contribution", "PPN;Newton;R10", "MISSING_NON_EH_MASS_COMPONENT"),
        ("MUR3773_6_range", "epsilon_range_mass", "|Q_range|/M_H or alpha(lambda)", "finite-range source charge contribution", "R10;WEP;orbital", "MISSING_RANGE_MASS_COMPONENT"),
        ("MUR3773_7_EM_Poynting", "epsilon_EM_Poynting_mass", "|Q_EM_Poynting|/M_H", "EM/Poynting/exterior stress not inside same Hilbert source", "WEP;PPN;Newton GM", "MISSING_EM_POYNTING_HILBERT_DESCENT"),
        ("MUR3773_8_orbit", "epsilon_orbit_Gauss", "|mu_fit/(G_eff M_H)-1| after GM split", "orbital inverse-square readout residual", "orbital;Newton", "MISSING_ORBITAL_GAUSS_READOUT_COMPONENT"),
        ("MUR3773_9_derivative_hair", "epsilon_mu_derivatives", "|partial_t,r,A,lambda,frame ln mu_obs| bundle", "time/radial/species/range/frame derivative hair of measured mass", "Gdot;radial;WEP;R10;frame", "MISSING_DERIVATIVE_HAIR_COMPONENTS"),
    ]
    return [
        {
            **base(timestamp),
            "residual_id": residual_id,
            "symbol": symbol,
            "definition": definition,
            "physical_meaning": physical_meaning,
            "feeds_observables": feeds_observables,
            "candidate_value": candidate_value,
            "units": "dimensionless_or_listed_derivative",
            "score_ready": False,
            "claim_allowed": False,
        }
        for residual_id, symbol, definition, physical_meaning, feeds_observables, candidate_value in rows
    ]


def bound_budget_rows(timestamp: str, values: dict[str, str]) -> list[dict[str, object]]:
    rows = [
        ("MUB3773_0_GM_total", "delta_ln_mu_obs", "dimensionless", "delta ln mu_obs <= epsilon_HH + epsilon_Gauss + epsilon_mu_extra + epsilon_orbit_Gauss + |delta ln G_eff|", "MISSING_NEWTON_GM_RESIDUAL_BOUND_OR_COMPONENTS", "P8_Y5_R2FR_3772_NEWTON_GM_BOUND_BUDGET.csv:NBB3772_4_Newton_GM_residual", "main measured-GM nonclaim bound"),
        ("MUB3773_1_mu_extra", "epsilon_mu_extra", "dimensionless", "epsilon_mu_extra <= sum |Q_i|/M_H over boundary/projector/nonEH/memory/range/coupling/readout/EM/source-theta channels", "MISSING_MUEXTRA_CHANNEL_VALUES", "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv:HC5", "extra monopole must be zeroed or component-filled"),
        ("MUB3773_2_radial_hair", "partial_r_ln_mu_obs", "inverse_length_or_dimensionless_envelope", "partial_r ln mu_obs <= |partial_r ln G_eff| + |partial_r ln M_H| + |partial_r epsilon_mu_extra| + readout/range terms", "MISSING_RADIAL_PROFILE_OR_NO_HAIR_THEOREM", "P8_Y5_R2FR_3762_RANGE_RADIAL_FRAME_RESIDUAL_BUDGET.csv:RRF_BUD3762_1_radial_hair", "radial source/Gauss hair bound"),
        ("MUB3773_3_Gdot_mu", "dln_mu_obs_dt", "yr^-1", "dln mu_obs/dt <= |d_t ln G_eff| + |d_t ln M_H| + |d_t epsilon_mu_extra| + readout rates", values["gdot_bound"], "P8_Y5_R2FR_3768_KAPPA_BOUND_BUDGET.csv:KBB3768_0_Gdot_total", "Gdot/source mass rate envelope"),
        ("MUB3773_4_WEP_source_mass", "eta_source_AB", "dimensionless", "eta_source_AB <= composition projection of epsilon_HH, epsilon_mu_extra, epsilon_EM_Poynting_mass, theta/source residuals", values["wep_bound"], "P8_Y5_R2FR_3759_WEP_BOUND_EVALUATION.csv:WB3759_2_max_allowed_residual", "composition bound on source-mass mismatch"),
        ("MUB3773_5_gamma_Gauss", "delta_gamma_Gauss", "dimensionless", "delta_gamma_Gauss <= C_gamma_H epsilon_HH + C_gamma_G epsilon_Gauss + C_gamma_mu epsilon_mu_extra", values["gamma_bound"], "P8_Y5_R2FR_3761_GAMMA_BETA_BOUND_EVALUATION.csv:PGB3761_0_gamma_conditional_zero", "PPN gamma envelope for surface/source mismatch"),
        ("MUB3773_6_beta_muextra", "delta_beta_muextra", "dimensionless", "delta_beta_muextra <= C_beta_H epsilon_HH + C_beta_mu epsilon_mu_extra + C_beta_nonEH epsilon_nonEH_mass", values["beta_bound"], "P8_Y5_R2FR_3761_GAMMA_BETA_BOUND_EVALUATION.csv:PGB3761_1_beta_conditional_zero", "PPN beta envelope for nonlinear surface/source mismatch"),
        ("MUB3773_7_R10_same_monopole", "alpha(lambda)", "range-dependent", "alpha(lambda) <= source-charge projection of Q_range and Q_projector_domain", "MISSING_R10_BOUND_CURVE_AND_SOURCE_CHARGES", "P8_Y5_R2FR_3772_NEWTON_GM_BOUND_BUDGET.csv:NBB3772_6_R10_same_source", "range channel must be shared with R10"),
        ("MUB3773_8_orbital_readout", "Delta_orbital_MTS", "observable-dependent", "Delta_orbital_MTS = P_orb[epsilon_HH,epsilon_Gauss,epsilon_mu_extra,range,frame,preferred-frame terms]", "MISSING_ORBITAL_RESIDUAL_VECTOR", "P8_Y5_R2FR_3772_NEWTON_GM_BOUND_BUDGET.csv:NBB3772_7_orbital_readout", "orbital readout remains nonclaim until residual vector exists"),
    ]
    return [
        {
            **base(timestamp),
            "budget_id": budget_id,
            "target": target,
            "units": units,
            "bound_formula": bound_formula,
            "bound_value": bound_value,
            "source": source,
            "interpretation": interpretation,
            "claim_allowed": False,
        }
        for budget_id, target, units, bound_formula, bound_value, source, interpretation in rows
    ]


def claim_gate_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    sources_exist = all(Path(str(row["source_path"])).exists() for row in grouped["sources"])
    theorem_emitted = any(row["theorem_id"] == "HGS3773_7_zero_route" for row in grouped["theorem"])
    muextra_decomposed = len(grouped["channels"]) >= 9 and any(row["symbol"] == "Q_EM_Poynting" for row in grouped["channels"])
    zero_signed = any(row["attempt_id"] == "HZA3773_8_verdict" and row["passes_clause"] is True for row in grouped["zero_attempt"])
    numeric_budgets = all(
        any(str(row["bound_value"]) == value for row in grouped["bound_budget"])
        for value in {"2.8e-15", "2.3e-05", "7.8e-05", "9.6e-15"}
    )
    missing_rows = any(str(row["bound_value"]).startswith("MISSING_") for row in grouped["bound_budget"])
    rows = [
        ("CG3773_0_sources", "all 3773 source paths exist", sources_exist, "path hygiene"),
        ("CG3773_1_surface_theorem", "Hamiltonian/Gauss zero route emitted", theorem_emitted, "surface-to-Hilbert mass theorem exists"),
        ("CG3773_2_mu_extra_channels", "mu_extra channel audit emitted including EM/Poynting", muextra_decomposed, "extra monopole channels are named"),
        ("CG3773_3_current_zero_signed", "current branch signs mu_extra=0 and surface equality", zero_signed, "blocked by unsigned charge/Gauss/no-extra/orbit clauses"),
        ("CG3773_4_residual_vector_named", "mu_extra residual coefficient rows emitted", len(grouped["residuals"]) >= 10, "residuals are finite named rows"),
        ("CG3773_5_numeric_bound_envelopes", "WEP/PPN/Gdot envelopes emitted", numeric_budgets, "source-backed external envelopes are wired"),
        ("CG3773_6_missing_rows_nonclaim", "GM/radial/R10/orbital rows remain blockers", missing_rows, "no claim with placeholder components"),
        ("CG3773_7_Newton_GM_claim", "first-order measured-GM Newton claim allowed", False, "blocked until zero proof or numeric mu_extra vector"),
        ("CG3773_8_local_GR_claim", "local GR claim allowed", False, "blocked until measured GM bridge and second-order PPN/EH residuals close"),
    ]
    return [
        {
            **base(timestamp),
            "gate_id": gate_id,
            "gate": gate,
            "passed": passed,
            "details": details,
            "claim_allowed": False,
        }
        for gate_id, gate, passed, details in rows
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("DEC3773_0", "The exterior measured GM bridge is now a Hamiltonian/Gauss equality problem, not an undefined coupling problem.", "use HGS3773_2/HGS3773_3 as the proof route"),
        ("DEC3773_1", "Any unowned exterior energy or charge, including EM/Poynting stress not inside the same Hilbert source, is part of mu_extra.", "do not absorb it into fitted G or orbital GM"),
        ("DEC3773_2", "Current MTS has a theorem route but not a claim because observed-time charge, integrability/reference, charge-current equality, closed projected flux, Gauss equality, no-extra-monopole, and orbital readout are unsigned.", "close or bound these clauses in that order"),
        ("DEC3773_3", "The next least-circular proof target is the no-extra-monopole channel theorem because it tells us whether boundary/projector/range/EM/Poynting channels vanish or must be bounded.", "attack mu_extra channel zeros next"),
    ]
    return [
        {
            **base(timestamp),
            "decision_id": decision_id,
            "decision": decision,
            "action": action,
            "claim_allowed": False,
        }
        for decision_id, decision, action in rows
    ]


def next_target_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "next_id": "NEXT3773_0",
            "target_doc": "3774-Y5-R2FR-muextra-channel-zero-theorem-or-component-bound-vector.md",
            "target_script": "scripts/Y5_R2FR_3774_muextra_channel_zero_theorem_or_component_bound_vector.py",
            "objective": "prove boundary, projector/domain, non-EH, memory, range, coupling, readout, EM/Poynting, and source/theta exterior monopole channels vanish, or emit a component mu_extra bound vector",
            "reason": "3773 shows measured GM closes only if the exterior surface charge has no unowned monopole; the channel vector is now the highest-value proof/bound target",
            "claim_allowed": False,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "status": "HAMILTONIAN_GAUSS_SURFACE_THEOREM_DERIVED_MUEXTRA_CHANNEL_VECTOR_EMITTED_NOT_PARENT_SIGNED",
            "summary": "3773 derives the conditional exterior GM bridge: if the Hamiltonian surface charge equals the same q_obs Hilbert mass current, the EH/Poisson source integrates cleanly by Gauss, and no extra monopole channel survives, then mu_obs=G_eff M_H and first-order Newton measured-GM recovery follows from 3772. It also emits the mu_extra channel vector, including boundary, projector/domain, non-EH, memory, range, coupling, readout, EM/Poynting, and source/theta channels. Current MTS still cannot claim measured-GM closure because the charge, Gauss, no-extra-monopole, and orbital readout clauses are unsigned or missing components.",
            "claim_allowed": False,
        }
    ]


def validation_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks = [
        ("sources_exist", "all 3773 source paths exist", all(Path(str(row["source_path"])).exists() for row in grouped["sources"])),
        ("generated_csvs_parse", "all generated 3773 csvs parse", all(read_csv(path) for path in generated_csvs)),
        ("surface_theorem", "Hamiltonian/Gauss surface theorem emitted", any(row["theorem_id"] == "HGS3773_7_zero_route" for row in grouped["theorem"])),
        ("muextra_decomposition", "mu_extra decomposition emitted", any(row["theorem_id"] == "HGS3773_4_no_extra_monopole_condition" for row in grouped["theorem"])),
        ("poynting_channel", "EM/Poynting extra-monopole channel emitted", any(row["symbol"] == "Q_EM_Poynting" for row in grouped["channels"])),
        ("zero_not_claimed", "current branch keeps surface/GM closure unsigned", any(row["attempt_id"] == "HZA3773_8_verdict" and row["passes_clause"] is False for row in grouped["zero_attempt"])),
        ("residual_rows", "at least ten mu_extra residual coefficient rows emitted", len(grouped["residuals"]) >= 10),
        ("numeric_bound_envelopes", "WEP/PPN/Gdot numeric envelopes emitted", all(any(str(row["bound_value"]) == value for row in grouped["bound_budget"]) for value in {"2.8e-15", "2.3e-05", "7.8e-05", "9.6e-15"})),
        ("missing_rows_nonclaim", "GM/mu_extra/radial/R10/orbital blockers remain explicit", any(row["bound_value"] == "MISSING_NEWTON_GM_RESIDUAL_BOUND_OR_COMPONENTS" for row in grouped["bound_budget"]) and any(row["bound_value"] == "MISSING_MUEXTRA_CHANNEL_VALUES" for row in grouped["bound_budget"]) and any(row["bound_value"] == "MISSING_ORBITAL_RESIDUAL_VECTOR" for row in grouped["bound_budget"])),
        ("claim_gates_closed", "Newton/local-GR claims remain closed", all(row["passed"] is False for row in grouped["claim_gates"] if row["gate_id"] in {"CG3773_3_current_zero_signed", "CG3773_7_Newton_GM_claim", "CG3773_8_local_GR_claim"})),
        ("next_target", "3774 mu_extra channel target emitted", grouped["next_target"][0]["target_doc"] == "3774-Y5-R2FR-muextra-channel-zero-theorem-or-component-bound-vector.md"),
        ("no_formalization_leak", "no 3773 files written to formalization-workbench", not FORMALIZATION.exists() or not list(FORMALIZATION.rglob("*3773*"))),
    ]
    return [
        {
            **base(timestamp),
            "validation_id": validation_id,
            "description": description,
            "result": "PASS" if result else "FAIL",
            "details": "" if result else "check failed",
        }
        for validation_id, description, result in checks
    ]


def render_doc(grouped: dict[str, list[dict[str, object]]]) -> str:
    lines = [
        "# 3773 - Hamiltonian/Gauss Surface Charge Equals Hilbert Mass Or MuExtra Bound",
        "",
        "## Status",
        "",
        f"`{grouped['status'][0]['status']}`.",
        "",
        grouped["status"][0]["summary"],
        "",
        "## Result In Plain Terms",
        "",
        "3773 attacks the exterior measured-GM throat. The local source can be beautifully descended, but Newton still fails if the surface charge outside the body is not the same Hilbert mass, or if some hidden exterior monopole rides along. The theorem route is now explicit: Hamiltonian charge equals Hilbert mass, Gauss turns source density into surface flux, `mu_extra=0`, then orbital `GM` is real rather than fitted fog.",
        "",
        "## Hamiltonian/Gauss Surface Theorem",
    ]
    for row in grouped["theorem"]:
        lines.append(f"- `{row['theorem_id']}` `{row['status']}`: {row['statement']} Derivation: {row['derivation']}")
    lines.extend(["", "## Zero Proof Attempt"])
    for row in grouped["zero_attempt"]:
        lines.append(f"- `{row['attempt_id']}` pass=`{row['passes_clause']}`: {row['required_clause']}. Evidence: {row['evidence']}.")
    lines.extend(["", "## MuExtra Channel Audit"])
    for row in grouped["channels"]:
        lines.append(f"- `{row['channel_id']}` `{row['symbol']}`: {row['definition']} Status: `{row['current_status']}`.")
    lines.extend(["", "## Residual Coefficients"])
    for row in grouped["residuals"]:
        lines.append(f"- `{row['residual_id']}` `{row['symbol']}`: {row['definition']} Value: `{row['candidate_value']}`.")
    lines.extend(["", "## Bound Budget"])
    for row in grouped["bound_budget"]:
        lines.append(f"- `{row['budget_id']}` `{row['target']}`: {row['bound_formula']} <= `{row['bound_value']}` `{row['units']}`. Source: {row['source']}.")
    lines.extend(["", "## Claim Gates"])
    for row in grouped["claim_gates"]:
        lines.append(f"- `{row['gate_id']}` pass=`{row['passed']}`: {row['gate']} - {row['details']}")
    lines.extend(["", "## Decisions"])
    for row in grouped["decision_rows"]:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} Action: {row['action']}.")
    lines.extend(["", "## Next Target"])
    for row in grouped["next_target"]:
        lines.append(f"- `{row['target_doc']}`: {row['objective']}")
    lines.extend(["", "## Validation"])
    for row in grouped["validation"]:
        lines.append(f"- `{row['validation_id']}` `{row['result']}`: {row['description']}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    timestamp = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    values = numeric_inputs()

    grouped: dict[str, list[dict[str, object]]] = {
        "sources": source_register(timestamp),
        "theorem": theorem_rows(timestamp),
        "zero_attempt": zero_attempt_rows(timestamp),
        "channels": channel_rows(timestamp),
        "residuals": residual_rows(timestamp),
        "bound_budget": bound_budget_rows(timestamp, values),
        "decision_rows": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
    }
    grouped["claim_gates"] = claim_gate_rows(timestamp, grouped)

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["theorem"], grouped["theorem"])
    write_csv(OUTPUTS["zero_attempt"], grouped["zero_attempt"])
    write_csv(OUTPUTS["channels"], grouped["channels"])
    write_csv(OUTPUTS["residuals"], grouped["residuals"])
    write_csv(OUTPUTS["bound_budget"], grouped["bound_budget"])
    write_csv(OUTPUTS["claim_gates"], grouped["claim_gates"])
    write_csv(OUTPUTS["decision_rows"], grouped["decision_rows"])
    write_csv(OUTPUTS["next_target"], grouped["next_target"])
    write_csv(OUTPUTS["status"], grouped["status"])

    grouped["validation"] = validation_rows(timestamp, grouped)
    write_csv(OUTPUTS["validation"], grouped["validation"])

    DOC_PATH.write_text(render_doc(grouped), encoding="utf-8")

    cache = Path(__file__).resolve().parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    failures = [row for row in grouped["validation"] if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3773 validation failed: {failures}")
    print("wrote 3773 checkpoint: Hamiltonian/Gauss surface theorem and mu_extra channel vector emitted")


if __name__ == "__main__":
    main()

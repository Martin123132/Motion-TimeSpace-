import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3772"
BRANCH = "MTS_R2FR_Y5_SOURCE_HAMILTONIAN_NORMALIZATION_OR_NEWTON_ACTIVE_PASSIVE_GM_BOUND_3772"
PCW = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work"
)
RESIDUALS = PCW / "source-intake" / "mts_residuals"
FORMALIZATION = PCW.parent / "formalization-workbench"
DOC_PATH = PCW / "3772-Y5-R2FR-source-Hamiltonian-normalization-or-Newton-active-passive-GM-bound.md"


OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3772_SOURCE_REGISTER.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_3772_NEWTON_SOURCE_HAMILTONIAN_THEOREM.csv",
    "zero_attempt": RESIDUALS / "P8_Y5_R2FR_3772_NEWTON_SOURCE_HAMILTONIAN_ZERO_ATTEMPT.csv",
    "residuals": RESIDUALS / "P8_Y5_R2FR_3772_NEWTON_GM_RESIDUAL_COEFFICIENTS.csv",
    "bound_budget": RESIDUALS / "P8_Y5_R2FR_3772_NEWTON_GM_BOUND_BUDGET.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_3772_CLAIM_GATES.csv",
    "decision_rows": RESIDUALS / "P8_Y5_R2FR_3772_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3772_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3772_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3772_VALIDATION.csv",
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
        "SRC3772_0_3771_doc": PCW / "3771-Y5-R2FR-constants-material-marker-leak-zero-or-clock-WEP-alpha-bound.md",
        "SRC3772_1_3771_bound_budget": RESIDUALS / "P8_Y5_R2FR_3771_CONSTANT_MARKER_BOUND_BUDGET.csv",
        "SRC3772_2_3770_source_theorem": RESIDUALS / "P8_Y5_R2FR_3770_SOURCE_ACTION_ZERO_THEOREM.csv",
        "SRC3772_3_3770_source_budget": RESIDUALS / "P8_Y5_R2FR_3770_SOURCE_ACTION_BOUND_BUDGET.csv",
        "SRC3772_4_3759_source_universality": RESIDUALS / "P8_Y5_R2FR_3759_SOURCE_UNIVERSALITY_THEOREM.csv",
        "SRC3772_5_3759_wep_budget": RESIDUALS / "P8_Y5_R2FR_3759_WEP_BOUND_EVALUATION.csv",
        "SRC3772_6_3761_ppn_eval": RESIDUALS / "P8_Y5_R2FR_3761_GAMMA_BETA_BOUND_EVALUATION.csv",
        "SRC3772_7_3762_range_budget": RESIDUALS / "P8_Y5_R2FR_3762_RANGE_RADIAL_FRAME_RESIDUAL_BUDGET.csv",
        "SRC3772_8_3768_kappa_budget": RESIDUALS / "P8_Y5_R2FR_3768_KAPPA_BOUND_BUDGET.csv",
        "SRC3772_9_3652_weak_field_H": RESIDUALS / "P8_Y5_R2FR_3652_WEAK_FIELD_HAMILTONIAN_THEOREM_ATTEMPT.csv",
        "SRC3772_10_3652_GM_rows": RESIDUALS / "P8_Y5_R2FR_3652_GM_SOURCE_CALIBRATION_ROWS.csv",
        "SRC3772_11_source_normalized_Newton_stack": RESIDUALS / "P8_source_normalized_Newton_branch_STACK.csv",
        "SRC3772_12_Hamiltonian_charge_contract": RESIDUALS / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv",
        "SRC3772_13_Poisson_Gauss_contract": RESIDUALS / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
        "SRC3772_14_Hamiltonian_GM_glue": RESIDUALS / "P8_Y5_R2FR_3575_HAMILTONIAN_GM_GLUE_GATES.csv",
        "SRC3772_15_EH_Newtonian_theorem": RESIDUALS / "P8_Y5_PARENT_QLOC_1939_EH_NEWTONIAN_THEOREM.csv",
        "SRC3772_16_Newtonian_limit_derivation": RESIDUALS / "P8_Y5_PARENT_QLOC_1938_NEWTONIAN_LIMIT_DERIVATION.csv",
    }


def source_register(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "source_id": source_id,
            "source_path": str(path),
            "source_exists": path.exists(),
            "role": "3772 Newton source-Hamiltonian normalization and active/passive/GM bridge input",
        }
        for source_id, path in source_paths().items()
    ]


def find_row(path: Path, key: str, value: str) -> dict[str, str]:
    for row in read_csv(path):
        if row.get(key) == value:
            return row
    raise KeyError(f"missing row {key}={value} in {path}")


def numeric_inputs() -> dict[str, str]:
    wep = find_row(source_paths()["SRC3772_5_3759_wep_budget"], "evaluation_id", "WB3759_2_max_allowed_residual")
    gamma = find_row(source_paths()["SRC3772_6_3761_ppn_eval"], "evaluation_id", "PGB3761_0_gamma_conditional_zero")
    beta = find_row(source_paths()["SRC3772_6_3761_ppn_eval"], "evaluation_id", "PGB3761_1_beta_conditional_zero")
    gdot = find_row(source_paths()["SRC3772_8_3768_kappa_budget"], "budget_id", "KBB3768_0_Gdot_total")
    return {
        "wep_bound": wep["bound_value"],
        "gamma_bound": gamma["bound_value"],
        "beta_bound": beta["bound_value"],
        "gdot_bound": gdot["bound_value"],
    }


def theorem_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "NSH3772_0_same_action_NR_expansion",
            "A descended matter/source action in the observed metric has the nonrelativistic expansion L_NR = -M_eff c^2 + (1/2)M_eff v^2 - M_eff Phi_obs + internal/binding terms.",
            "Expand ds in g_00=-(1+2 Phi_obs/c^2), g_ij=delta_ij, and v^2/c^2<<1; the same M_eff multiplies kinetic and potential terms.",
            "This is the clean passive=inertial route without adding a new Newton axiom.",
            "EXACT_CONDITIONAL_NR_EXPANSION",
        ),
        (
            "NSH3772_1_passive_equals_inertial",
            "If the same q_obs-descended action supplies both kinetic motion and coupling to Phi_obs, then m_passive/m_inertial=1 up to retained binding/source residuals.",
            "The kinetic coefficient and potential coefficient are the same coefficient in L_NR.",
            "This is the local WEP mechanism inside the Newton bridge.",
            "EXACT_CONDITIONAL_PASSIVE_INERTIAL_THEOREM",
        ),
        (
            "NSH3772_2_active_equals_Hilbert",
            "The active source is rho_active=T_00/c^2 from the same Hilbert/coframe variation, so active mass equals the same M_eff if source action descent and theta silence hold.",
            "Vary the same source action with respect to g_obs/coframe; the slow-source limit gives T_00 ~= rho c^2.",
            "This turns source mass into an action variation, not a fitted arena knob.",
            "EXACT_CONDITIONAL_ACTIVE_SOURCE_THEOREM",
        ),
        (
            "NSH3772_3_EH_to_Poisson",
            "If the local operator is EH with kappa_eff=8*pi*G_eff/c^4 and no non-EH residual source, the 00 weak-field equation gives nabla^2 Phi_obs=4*pi*G_eff rho_active.",
            "Use the standard weak static limit of the EH equation, imported from the 1938/1939 rows.",
            "This is the GR-to-Newton left-hand bridge.",
            "EXACT_CONDITIONAL_POISSON_LIMIT",
        ),
        (
            "NSH3772_4_three_mass_identity",
            "If NSH3772_0 through NSH3772_3 hold and no extra monopole/boundary/range/source-normalization residual survives, then M_inertial=M_passive=M_active=M_eff and mu_obs=G_eff M_eff.",
            "Combine the same-action NR expansion, Hilbert source variation, Poisson equation, and Gauss/orbital readout.",
            "This is the precise local Newton recovery theorem the framework needs.",
            "EXACT_CONDITIONAL_NEWTON_GM_THEOREM",
        ),
        (
            "NSH3772_5_GM_degeneracy_guard",
            "Orbital agreement alone measures mu_fit=GM and cannot prove source normalization; delta ln mu_obs must be split before claiming Newton recovery.",
            "Kepler/orbital dynamics determine the product, so source, G, frame, range, and boundary residuals can hide inside mu_fit unless separated.",
            "This blocks the easy post-hoc fit trap.",
            "EXACT_GM_DEGENERACY_LAW",
        ),
        (
            "NSH3772_6_GM_residual_law",
            "delta ln mu_obs = delta ln G_eff + delta ln M_eff + q_metric + q_readout + q_boundary + q_source + q_theta + q_range + q_orbit.",
            "This is the no-cancellation split of the measured-GM calibration residual.",
            "The Newton gap is now a finite residual vector, not a vague failure.",
            "EXACT_RESIDUAL_DECOMPOSITION",
        ),
        (
            "NSH3772_7_cross_arena_closure",
            "The same source-normalization vector must feed WEP, R10, PPN, Gdot, and orbital rows; it cannot be refit separately in each arena.",
            "Same source charge is what makes the unified branch testable.",
            "This is the Mayweather route: consistent footwork across tests, not one knockout fit.",
            "CROSS_ARENA_CONSISTENCY_CONTRACT",
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
        ("NZA3772_0_NR_expansion_derived", "same-action nonrelativistic passive=inertial expansion is derived", "NSH3772_0/1 plus 3652 WFH3652_0", True, "Newton bridge has a real derivation route"),
        ("NZA3772_1_active_source_law_derived", "active source as Hilbert/coframe T00/c^2 is derived conditionally", "3770 source theorem and 3652 WFH3652_2", True, "active mass can be tied to the same action if source descent signs"),
        ("NZA3772_2_GM_degeneracy_guard_derived", "mu_fit=GM degeneracy and residual split are derived", "3652 WFH3652_1 and NSH3772_5/6", True, "orbital success cannot hide source residuals"),
        ("NZA3772_3_source_action_descended", "source action descends through q_obs", "3770 marks source descent unsigned", False, "active/passive/inertial identity remains conditional"),
        ("NZA3772_4_theta_silent", "constants/material markers are q_obs-owned or superselected", "3771 marks theta silence unsigned", False, "material/source normalization residual remains live"),
        ("NZA3772_5_EH_Poisson_signed", "local EH operator and Poisson coefficient are parent-signed", "1938/1939 and 3652 are conditional, not parent-derived", False, "Newton source equation remains conditional"),
        ("NZA3772_6_Hamiltonian_charge_equals_Hilbert_mass", "Hamiltonian boundary/source charge equals projected Hilbert mass current", "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv:HC4 not parent-derived", False, "exterior GM charge remains a live bridge"),
        ("NZA3772_7_Gauss_orbital_readout_clean", "Gauss surface and orbital inverse-square readout contain no extra monopole/range/frame residual", "Poisson/Gauss contract PG4-PG8 not parent-derived", False, "mu_extra/orbital residual remains live"),
        ("NZA3772_8_verdict", "current MTS branch derives local Newtonian GM", "conditional theorem exists but source descent, theta silence, EH/Poisson, Hamiltonian charge equality, and no-extra-monopole clauses are unsigned", False, "do not claim Newton/local-GR pass"),
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


def residual_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("NGR3772_0_passive_inertial", "epsilon_pi", "|ln(m_passive/m_inertial)|", "failure of same-action NR expansion or frame descent", "WEP;orbital", "MISSING_SOURCE_ACTION_DESCENT_OR_FRAME_LOCK"),
        ("NGR3772_1_active_inertial", "epsilon_ai", "|ln(M_active/M_inertial)|", "Hilbert active source differs from inertial source mass", "Newton;PPN;WEP", "MISSING_ACTIVE_INERTIAL_SOURCE_IDENTITY"),
        ("NGR3772_2_Hamiltonian_Hilbert_charge", "epsilon_HH", "|B_xi/G_eff - integral Pi_M J_H|/M_eff", "Hamiltonian surface charge not equal to projected Hilbert mass current", "Newton GM;Gauss;PPN", "MISSING_HAMILTONIAN_HILBERT_CHARGE_EQUALITY"),
        ("NGR3772_3_Poisson_coefficient", "epsilon_Poisson", "|C_Poisson/(4*pi*G_eff)-1|", "weak-field source coefficient mismatch", "Newton;gamma;beta", "MISSING_EH_POISSON_PARENT_SIGNATURE"),
        ("NGR3772_4_Gauss_surface", "epsilon_Gauss", "|surface_integral grad Phi/(4*pi G_eff M_eff)-1|", "volume/boundary/domain residual in source-to-surface map", "Newton GM;radial hair", "MISSING_GAUSS_SURFACE_EQUALITY"),
        ("NGR3772_5_mu_extra", "epsilon_mu_extra", "|mu_extra|/|G_eff M_eff|", "extra monopole from boundary, range, memory, projector, domain, or non-EH sector", "Newton;R10;orbital", "MISSING_NO_EXTRA_MONOPOLE_THEOREM"),
        ("NGR3772_6_orbital_readout", "epsilon_orbit", "|mu_fit/(G_eff M_eff)-1| after residual split", "orbital inverse-square readout differs from Poisson/Gauss source", "orbital;Newton", "MISSING_ORBITAL_READOUT_PROJECTION"),
        ("NGR3772_7_source_rate", "dot_epsilon_source_mass", "|d_t ln M_eff| + source flux terms", "source mass drift or source-current leakage", "Gdot;orbital", "MISSING_SOURCE_MASS_RATE_COMPONENTS"),
        ("NGR3772_8_range_source", "epsilon_range_source", "alpha(lambda) or finite-range source charge from same Hamiltonian vector", "unowned short-range/fifth-force source charge", "R10;WEP;orbital", "MISSING_R10_SOURCE_CHARGE_VECTOR"),
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
            "units": "dimensionless_or_listed_rate",
            "score_ready": False,
            "claim_allowed": False,
        }
        for residual_id, symbol, definition, physical_meaning, feeds_observables, candidate_value in rows
    ]


def bound_budget_rows(timestamp: str, values: dict[str, str]) -> list[dict[str, object]]:
    rows = [
        ("NBB3772_0_WEP_passive_inertial", "eta_source_AB", "dimensionless", "eta_source_AB <= composition projection of epsilon_pi, epsilon_ai, theta/source residuals", values["wep_bound"], "P8_Y5_R2FR_3759_WEP_BOUND_EVALUATION.csv:WB3759_2_max_allowed_residual", "WEP bound on source/passive/inertial mismatch"),
        ("NBB3772_1_gamma_source", "delta_gamma_source", "dimensionless", "delta_gamma_source <= C_gamma_P epsilon_Poisson + C_gamma_H epsilon_HH + C_gamma_src epsilon_ai", values["gamma_bound"], "P8_Y5_R2FR_3761_GAMMA_BETA_BOUND_EVALUATION.csv:PGB3761_0_gamma_conditional_zero", "PPN gamma envelope for Newton source bridge"),
        ("NBB3772_2_beta_source", "delta_beta_source", "dimensionless", "delta_beta_source <= C_beta_P epsilon_Poisson + C_beta_mu epsilon_mu_extra + C_beta_src epsilon_ai", values["beta_bound"], "P8_Y5_R2FR_3761_GAMMA_BETA_BOUND_EVALUATION.csv:PGB3761_1_beta_conditional_zero", "PPN beta envelope for nonlinear source bridge"),
        ("NBB3772_3_Gdot_source_mass", "dln_mu_obs_dt", "yr^-1", "dln_mu_obs_dt <= |d_t ln G_eff| + |d_t ln M_eff| + |d_t epsilon_mu_extra| + frame/readout rates", values["gdot_bound"], "P8_Y5_R2FR_3768_KAPPA_BOUND_BUDGET.csv:KBB3768_0_Gdot_total", "source mass/coupling rate envelope"),
        ("NBB3772_4_Newton_GM_residual", "delta_ln_mu_obs", "dimensionless", "delta ln mu_obs <= |delta ln G_eff|+|delta ln M_eff|+|q_metric|+|q_readout|+|q_boundary|+|q_source|+|q_theta|+|q_range|+|q_orbit|", "MISSING_NEWTON_GM_RESIDUAL_BOUND_OR_COMPONENTS", "P8_Y5_R2FR_3652_GM_SOURCE_CALIBRATION_ROWS.csv:GMC3652_1_delta_mu", "main Newton GM nonclaim row"),
        ("NBB3772_5_radial_hair", "partial_r_ln_mu_obs", "inverse_length_or_dimensionless_envelope", "partial_r ln mu_obs <= radial derivative of source, coupling, boundary, range, and readout residuals", "MISSING_RADIAL_PROFILE_OR_NO_HAIR_THEOREM", "P8_Y5_R2FR_3762_RANGE_RADIAL_FRAME_RESIDUAL_BUDGET.csv:RRF_BUD3762_1_radial_hair", "radial/source-hair Newton blocker"),
        ("NBB3772_6_R10_same_source", "alpha(lambda)", "range-dependent", "alpha(lambda) <= Hamiltonian source charge projection into R10 material leg", "MISSING_R10_BOUND_CURVE_AND_SOURCE_CHARGES", "P8_Y5_R2FR_3652_GM_SOURCE_CALIBRATION_ROWS.csv:GMC3652_4_alpha_ST", "same source vector must serve R10"),
        ("NBB3772_7_orbital_readout", "Delta_orbital_MTS", "observable-dependent", "Delta_orbital_MTS = P_orb[delta_ln_mu_obs, PPN, preferred-frame, boundary/domain, range terms]", "MISSING_ORBITAL_RESIDUAL_VECTOR", "P8_Y5_R2FR_3652_GM_SOURCE_CALIBRATION_ROWS.csv:GMC3652_7_orbital_vector", "orbits are not a proof unless GM degeneracy is split"),
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
    theorem_emitted = any(row["theorem_id"] == "NSH3772_4_three_mass_identity" for row in grouped["theorem"])
    residual_law = any(row["theorem_id"] == "NSH3772_6_GM_residual_law" for row in grouped["theorem"])
    zero_signed = any(row["attempt_id"] == "NZA3772_8_verdict" and row["passes_clause"] is True for row in grouped["zero_attempt"])
    numeric_budgets = all(
        any(str(row["bound_value"]) == value for row in grouped["bound_budget"])
        for value in {"2.8e-15", "2.3e-05", "7.8e-05", "9.6e-15"}
    )
    missing_rows = any(str(row["bound_value"]).startswith("MISSING_") for row in grouped["bound_budget"])
    rows = [
        ("CG3772_0_sources", "all 3772 source paths exist", sources_exist, "path hygiene"),
        ("CG3772_1_Newton_theorem", "three-mass Newton theorem emitted", theorem_emitted, "derivation route exists"),
        ("CG3772_2_GM_degeneracy_guard", "GM residual split emitted", residual_law, "orbits cannot launder source residuals"),
        ("CG3772_3_current_zero_signed", "current branch signs Newton GM closure", zero_signed, "blocked by source/theta/EH/Hamiltonian/Gauss/orbit clauses"),
        ("CG3772_4_residual_vector_named", "Newton GM residual vector rows emitted", len(grouped["residuals"]) >= 9, "residuals are finite named rows"),
        ("CG3772_5_numeric_bound_envelopes", "WEP/PPN/Gdot envelopes emitted", numeric_budgets, "source-backed external envelopes are wired"),
        ("CG3772_6_missing_rows_nonclaim", "Newton/R10/orbital rows remain blockers", missing_rows, "no claim with placeholder components"),
        ("CG3772_7_Newton_claim", "Newtonian mechanics recovery claim allowed", False, "blocked until zero proof or numeric residual vector"),
        ("CG3772_8_local_GR_claim", "local GR claim allowed", False, "blocked until Newton bridge plus PPN/EH residuals close"),
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
        ("DEC3772_0", "The active/passive/inertial equality can be derived conditionally from one descended source action; it does not need to be asserted as a plateau axiom.", "keep this as the preferred Newton bridge"),
        ("DEC3772_1", "Orbital agreement is necessary but not sufficient because fitted mu=GM can absorb source/coupling/readout residuals.", "always split measured GM before claiming Newton recovery"),
        ("DEC3772_2", "The current branch has a real Newton theorem route but not a Newton claim: source descent, theta silence, EH Poisson, Hamiltonian-Hilbert charge equality, Gauss, and orbital readout remain unsigned.", "close or bound those clauses in order"),
        ("DEC3772_3", "The next least-scrutinized leap is the Hamiltonian/Gauss surface equality because it converts the local Hilbert source into the exterior monopole measured as GM.", "attack surface charge equals Hilbert mass next"),
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
            "next_id": "NEXT3772_0",
            "target_doc": "3773-Y5-R2FR-Hamiltonian-Gauss-surface-charge-equals-Hilbert-mass-or-muextra-bound.md",
            "target_script": "scripts/Y5_R2FR_3773_Hamiltonian_Gauss_surface_charge_equals_Hilbert_mass_or_muextra_bound.py",
            "objective": "prove the Hamiltonian/Gauss exterior surface charge equals the same q_obs Hilbert mass current with no extra monopole, or emit mu_extra/radial/orbital residual bounds",
            "reason": "3772 derives the active/passive/inertial Newton bridge conditionally; the remaining hard bridge is converting local source density into the exterior measured GM monopole",
            "claim_allowed": False,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "status": "NEWTON_ACTIVE_PASSIVE_INERTIAL_THEOREM_DERIVED_CONDITIONALLY_GM_RESIDUAL_VECTOR_EMITTED_NOT_PARENT_SIGNED",
            "summary": "3772 derives the conditional local Newton bridge: one descended observed source action gives the same inertial, passive, and active source mass in the weak-field slow-source limit, and the EH 00 equation then gives Poisson/Newton if the operator and surface charge are clean. It also emits the measured-GM degeneracy guard and residual vector, so orbital success cannot be used as a hidden calibration claim. Current MTS still cannot claim Newton/local-GR recovery because source descent, theta silence, EH Poisson, Hamiltonian-Hilbert charge equality, Gauss surface equality, no-extra-monopole, and orbital readout are unsigned or missing numeric components.",
            "claim_allowed": False,
        }
    ]


def validation_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks = [
        ("sources_exist", "all 3772 source paths exist", all(Path(str(row["source_path"])).exists() for row in grouped["sources"])),
        ("generated_csvs_parse", "all generated 3772 csvs parse", all(read_csv(path) for path in generated_csvs)),
        ("newton_theorem", "three-mass Newton theorem emitted", any(row["theorem_id"] == "NSH3772_4_three_mass_identity" for row in grouped["theorem"])),
        ("GM_guard", "GM degeneracy/residual law emitted", any(row["theorem_id"] == "NSH3772_5_GM_degeneracy_guard" for row in grouped["theorem"]) and any(row["theorem_id"] == "NSH3772_6_GM_residual_law" for row in grouped["theorem"])),
        ("zero_not_claimed", "current branch keeps Newton GM closure unsigned", any(row["attempt_id"] == "NZA3772_8_verdict" and row["passes_clause"] is False for row in grouped["zero_attempt"])),
        ("residual_rows", "at least nine Newton residual coefficient rows emitted", len(grouped["residuals"]) >= 9),
        ("numeric_bound_envelopes", "WEP/PPN/Gdot numeric envelopes emitted", all(any(str(row["bound_value"]) == value for row in grouped["bound_budget"]) for value in {"2.8e-15", "2.3e-05", "7.8e-05", "9.6e-15"})),
        ("missing_rows_nonclaim", "Newton/R10/orbital blockers remain explicit", any(row["bound_value"] == "MISSING_NEWTON_GM_RESIDUAL_BOUND_OR_COMPONENTS" for row in grouped["bound_budget"]) and any(row["bound_value"] == "MISSING_R10_BOUND_CURVE_AND_SOURCE_CHARGES" for row in grouped["bound_budget"]) and any(row["bound_value"] == "MISSING_ORBITAL_RESIDUAL_VECTOR" for row in grouped["bound_budget"])),
        ("claim_gates_closed", "Newton/local-GR claims remain closed", all(row["passed"] is False for row in grouped["claim_gates"] if row["gate_id"] in {"CG3772_3_current_zero_signed", "CG3772_7_Newton_claim", "CG3772_8_local_GR_claim"})),
        ("next_target", "3773 Hamiltonian/Gauss surface-charge target emitted", grouped["next_target"][0]["target_doc"] == "3773-Y5-R2FR-Hamiltonian-Gauss-surface-charge-equals-Hilbert-mass-or-muextra-bound.md"),
        ("no_formalization_leak", "no 3772 files written to formalization-workbench", not FORMALIZATION.exists() or not list(FORMALIZATION.rglob("*3772*"))),
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
        "# 3772 - Source Hamiltonian Normalization Or Newton Active/Passive GM Bound",
        "",
        "## Status",
        "",
        f"`{grouped['status'][0]['status']}`.",
        "",
        grouped["status"][0]["summary"],
        "",
        "## Result In Plain Terms",
        "",
        "This checkpoint takes the leap into Newton rather than circling the word coupling. The conditional theorem is simple and strong: if one observed source action descends through `q_obs`, then the same coefficient that gives inertial motion also gives passive gravitational response; the same Hilbert/coframe source gives active mass; and the EH weak-field equation gives Poisson. What is not yet proven is the parent signature and exterior surface/GM calibration, so the branch remains nonclaim with a named residual vector.",
        "",
        "## Newton Source-Hamiltonian Theorem",
    ]
    for row in grouped["theorem"]:
        lines.append(f"- `{row['theorem_id']}` `{row['status']}`: {row['statement']} Derivation: {row['derivation']}")
    lines.extend(["", "## Zero Proof Attempt"])
    for row in grouped["zero_attempt"]:
        lines.append(f"- `{row['attempt_id']}` pass=`{row['passes_clause']}`: {row['required_clause']}. Evidence: {row['evidence']}.")
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
        raise SystemExit(f"3772 validation failed: {failures}")
    print("wrote 3772 checkpoint: Newton active/passive/inertial bridge and GM residual vector emitted")


if __name__ == "__main__":
    main()

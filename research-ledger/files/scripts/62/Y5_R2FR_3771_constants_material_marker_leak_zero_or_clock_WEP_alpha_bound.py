import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3771"
BRANCH = "MTS_R2FR_Y5_CONSTANTS_MATERIAL_MARKER_LEAK_ZERO_OR_CLOCK_WEP_ALPHA_BOUND_3771"
PCW = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work"
)
RESIDUALS = PCW / "source-intake" / "mts_residuals"
FORMALIZATION = PCW.parent / "formalization-workbench"
DOC_PATH = PCW / "3771-Y5-R2FR-constants-material-marker-leak-zero-or-clock-WEP-alpha-bound.md"


OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3771_SOURCE_REGISTER.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_3771_CONSTANT_MARKER_ZERO_THEOREM.csv",
    "zero_attempt": RESIDUALS / "P8_Y5_R2FR_3771_CONSTANT_MARKER_ZERO_ATTEMPT.csv",
    "unit_gauge": RESIDUALS / "P8_Y5_R2FR_3771_UNIT_GAUGE_AUDIT.csv",
    "coefficients": RESIDUALS / "P8_Y5_R2FR_3771_CONSTANT_MARKER_RESIDUAL_COEFFICIENTS.csv",
    "bound_budget": RESIDUALS / "P8_Y5_R2FR_3771_CONSTANT_MARKER_BOUND_BUDGET.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_3771_CLAIM_GATES.csv",
    "decision_rows": RESIDUALS / "P8_Y5_R2FR_3771_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3771_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3771_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3771_VALIDATION.csv",
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
        "SRC3771_0_3770_doc": PCW / "3770-Y5-R2FR-source-action-leak-zero-or-WEP-EM-PPN-bound.md",
        "SRC3771_1_3770_zero_attempt": RESIDUALS / "P8_Y5_R2FR_3770_SOURCE_ACTION_ZERO_ATTEMPT.csv",
        "SRC3771_2_3770_bound_budget": RESIDUALS / "P8_Y5_R2FR_3770_SOURCE_ACTION_BOUND_BUDGET.csv",
        "SRC3771_3_3767_leak_basis": RESIDUALS / "P8_Y5_R2FR_3767_LLEAK_OPERATOR_BASIS.csv",
        "SRC3771_4_3766_vertical_norms": RESIDUALS / "P8_Y5_R2FR_3766_VERTICAL_LEAKAGE_NORMS.csv",
        "SRC3771_5_3759_wep_budget": RESIDUALS / "P8_Y5_R2FR_3759_WEP_BOUND_EVALUATION.csv",
        "SRC3771_6_3760_em_budget": RESIDUALS / "P8_Y5_R2FR_3760_EM_SOURCE_RESIDUAL_BUDGET.csv",
        "SRC3771_7_3761_ppn_eval": RESIDUALS / "P8_Y5_R2FR_3761_GAMMA_BETA_BOUND_EVALUATION.csv",
        "SRC3771_8_3762_range_budget": RESIDUALS / "P8_Y5_R2FR_3762_RANGE_RADIAL_FRAME_RESIDUAL_BUDGET.csv",
        "SRC3771_9_3768_kappa_budget": RESIDUALS / "P8_Y5_R2FR_3768_KAPPA_BOUND_BUDGET.csv",
        "SRC3771_10_3769_shadow_budget": RESIDUALS / "P8_Y5_R2FR_3769_SHADOW_FRAME_BOUND_BUDGET.csv",
        "SRC3771_11_alpha_mass_clock_matrix": RESIDUALS / "P8_Y5_PARENT_QLOC_1805_ALPHA_MASS_CLOCK_BOUND_MATRIX.csv",
        "SRC3771_12_alpha_mass_clock_first_rows": RESIDUALS / "P8_Y5_PARENT_QLOC_1921_ALPHA_MASS_CLOCK_FIRST_ROWS_NONCLAIM.csv",
        "SRC3771_13_alphaEM_WEP_clock_R10_gate": RESIDUALS / "P8_Y5_R10_1396_ALPHAEM_WEP_CLOCK_R10_GATE.csv",
    }


def source_register(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "source_id": source_id,
            "source_path": str(path),
            "source_exists": path.exists(),
            "role": "3771 constant/material-marker zero theorem and clock/WEP/alpha bound input",
        }
        for source_id, path in source_paths().items()
    ]


def find_row(path: Path, key: str, value: str) -> dict[str, str]:
    for row in read_csv(path):
        if row.get(key) == value:
            return row
    raise KeyError(f"missing row {key}={value} in {path}")


def numeric_inputs() -> dict[str, str]:
    wep = find_row(source_paths()["SRC3771_5_3759_wep_budget"], "evaluation_id", "WB3759_2_max_allowed_residual")
    gamma = find_row(source_paths()["SRC3771_7_3761_ppn_eval"], "evaluation_id", "PGB3761_0_gamma_conditional_zero")
    beta = find_row(source_paths()["SRC3771_7_3761_ppn_eval"], "evaluation_id", "PGB3761_1_beta_conditional_zero")
    gdot = find_row(source_paths()["SRC3771_9_3768_kappa_budget"], "budget_id", "KBB3768_0_Gdot_total")
    em_wep = find_row(source_paths()["SRC3771_6_3760_em_budget"], "residual_id", "EMR3760_0_WEP_EM_binding")
    return {
        "wep_bound": wep["bound_value"],
        "gamma_bound": gamma["bound_value"],
        "beta_bound": beta["bound_value"],
        "gdot_bound": gdot["bound_value"],
        "em_wep_bound": em_wep["bound_value"],
    }


def theorem_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "CMT3771_0_theta_split",
            "Split theta into dimensionless physical constants c_I, material or representation labels m_A, binding/response coefficients b_A, and pure unit/common-scale conventions u.",
            "Only dimensionless readouts and source-normalized combinations can be physical; a unit convention alone cannot create or remove an observable force.",
            "This prevents the easy but invalid escape route of hiding constant leakage in units.",
            "EXACT_SPLIT",
        ),
        (
            "CMT3771_1_theta_leak_operator",
            "For E_A in ker(Dq_obs), define theta_{I,A}:=Lie_EA theta_I and L_leak_theta=zeta^A sum_I (partial L_src/partial theta_I) theta_{I,A}+O(zeta^2).",
            "This is the constants/material-marker component of the 3767 action-leak basis.",
            "The coupling problem is now a vertical derivative of observable constants and material labels.",
            "EXACT_OPERATOR",
        ),
        (
            "CMT3771_2_conditional_zero",
            "If every physical theta_I is q_obs-owned or superselected, Lie_EA theta_I=0 for all E_A in ker(Dq_obs), hence L_leak_theta=0.",
            "Substitute theta_{I,A}=0 into the operator definition.",
            "This is the clean route: no extra force, no WEP composition leak, no clock constant drift from the hidden fibre.",
            "EXACT_CONDITIONAL_ZERO_THEOREM",
        ),
        (
            "CMT3771_3_common_unit_mode",
            "A common unit rescaling is quotient-gauge only when all rods, clocks, source normalization, and kappa calibration descend through the same q_obs class.",
            "Dimensionless ratios cancel the common mode; Newtonian GM and absolute G do not cancel unless source calibration is also signed.",
            "This preserves local GR discipline without pretending absolute measured G has been derived.",
            "UNIT_GAUGE_CONDITION",
        ),
        (
            "CMT3771_4_clock_projection",
            "Clock ratios see only sensitivity-weighted dimensionless constant leakage: delta ln(nu_a/nu_b)=sum_I Delta K_I^{ab} delta ln theta_I plus readout-frame terms.",
            "Frequency units cancel; sensitivity differences survive.",
            "Clock rows become a direct bound on b_alpha, b_mu, nuclear, and clock-marker leakage.",
            "CLOCK_BOUND_INTERFACE",
        ),
        (
            "CMT3771_5_WEP_projection",
            "Composition tests see differential material response: eta_AB <= sum_I |Delta Q_I^{AB}| |b_I| tau_WEP plus EM/binding/source-current residuals.",
            "Universal common coupling cancels in eta_AB; composition-dependent constants and binding fractions do not.",
            "This connects the marker leak to MICROSCOPE/WEP rather than vibes.",
            "WEP_BOUND_INTERFACE",
        ),
        (
            "CMT3771_6_alpha_R10_projection",
            "Short-range rows see alpha_X(lambda_X) from material charges Qbar_source/test built from alpha, mass, nuclear, and clock-marker coefficients.",
            "A finite range mediator with nonzero material charge must be compared to alpha_bound(lambda).",
            "This prevents claiming R10/local closure without either a no-range theorem or real material-charge coefficients.",
            "R10_ALPHA_BOUND_INTERFACE",
        ),
        (
            "CMT3771_7_Newton_source_projection",
            "Newtonian mechanics requires the same source mass/charge normalization in inertial, passive, and active roles; theta common modes are safe only after this equality is signed.",
            "Otherwise delta ln mu_obs receives source-normalization and binding-marker leakage.",
            "This is the remaining bridge from field-theory coupling to Newtonian GM.",
            "NEWTON_SOURCE_INTERFACE",
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
        ("CZA3771_0_operator_identified", "L_leak_theta is present in the 3767 leak basis", "P8_Y5_R2FR_3767_LLEAK_OPERATOR_BASIS.csv:LOB3767_4_constants_markers", True, "the obstruction is now an explicit operator"),
        ("CZA3771_1_source_gate_requires_theta_silence", "3770 source descent requires constants/material markers silent", "P8_Y5_R2FR_3770_SOURCE_ACTION_ZERO_ATTEMPT.csv:SZA3770_4_constants_markers_silent", True, "the target is not invented; it is the blocker in the previous theorem"),
        ("CZA3771_2_unit_cheat_removed", "dimensionful unit rescaling is not counted as physical proof", "3771 unit-gauge audit splits common unit mode from dimensionless constants", True, "prevents fake closure by unit convention"),
        ("CZA3771_3_dimensionless_constants_superselected", "alpha_EM, mass ratios, charge ratios, and nuclear response coefficients are q_obs-owned or superselected", "current corpus has schemas and gates, but no parent superselection derivation", False, "b_alpha,b_mu,b_nuc remain live"),
        ("CZA3771_4_material_labels_superselected", "material/species labels and binding fractions are fixed representation or boundary labels invisible to ker(Dq_obs)", "current corpus has WEP/EM source budgets, but no parent material-label descent proof", False, "composition residuals remain live"),
        ("CZA3771_5_clock_markers_superselected", "clock transition response coefficients are q_obs-owned or source-backed constants", "clock product/source rows remain nonclaim or missing projection inputs", False, "clock bounds remain acquisition rows"),
        ("CZA3771_6_newton_source_common_mode_closed", "common mass/source normalization is harmless for Newtonian GM", "3770 still marks Newton active/passive source projection missing", False, "Newton local reduction remains blocked"),
        ("CZA3771_7_verdict", "L_leak_theta=0 for current MTS local branch", "conditional theorem exists, but parent superselection/material-marker/source-normalization proofs are unsigned", False, "do not claim constants/material-marker closure"),
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


def unit_gauge_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("UGA3771_0_dimensionful_mass_scale", "common dimensionful mass/energy scale", "unit_gauge_candidate", "cancels in dimensionless clock and WEP ratios only if all rods/clocks/source normalization co-descend", "Newton GM and absolute G calibration still need a source-normalization owner", False),
        ("UGA3771_1_alpha_EM", "fine-structure constant alpha_EM", "physical_dimensionless_constant", "cannot be removed by units; clocks, spectra, WEP binding, and R10 material charges can see it", "requires b_alpha=0 theorem or sourced b_alpha bound", False),
        ("UGA3771_2_mass_ratios", "dimensionless mass ratios such as m_e/m_p", "physical_dimensionless_constant", "cannot be removed by units; clock and matter responses can see it", "requires b_mu=0 theorem or sourced b_mu bound", False),
        ("UGA3771_3_charge_quantization", "charge ratios and gauge representation labels", "superselection_candidate", "safe only if gauge representation labels are fixed across q_obs fibres", "requires parent gauge/representation descent proof", False),
        ("UGA3771_4_material_identity", "material species labels and binding fractions", "boundary_or_representation_candidate", "safe only if material labels are not dynamical vertical fields", "requires material worldtube/source action descent proof", False),
        ("UGA3771_5_clock_transition_markers", "clock transition sensitivities and apparatus markers", "readout_marker_candidate", "safe only if apparatus/readout model descends through q_obs", "requires clock readout kernel and sensitivity source closure", False),
    ]
    return [
        {
            **base(timestamp),
            "audit_id": audit_id,
            "mode": mode,
            "classification": classification,
            "observable_rule": observable_rule,
            "remaining_requirement": remaining_requirement,
            "claim_allowed": claim_allowed,
        }
        for audit_id, mode, classification, observable_rule, remaining_requirement, claim_allowed in rows
    ]


def coefficient_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("CMC3771_0_total_theta", "epsilon_theta", "sup_A,I |zeta^A Lie_EA theta_I| after unit-gauge quotient", "aggregate constants/material-marker leakage", "WEP;clock;R10;PPN;Newton", "MISSING_PARENT_THETA_SUPERSELECTION"),
        ("CMC3771_1_b_alpha", "b_alpha", "E_A ln alpha_EM times zeta^A or local driver amplitude", "fine-structure leakage", "clock;EM spectra;WEP;R10", "MISSING_B_ALPHA_OR_PARENT_ZERO_THEOREM"),
        ("CMC3771_2_b_mu", "b_mu", "E_A ln(m_e/m_p) times zeta^A or local driver amplitude", "mass-ratio leakage", "clock;WEP;composition;source charge", "MISSING_B_MU_OR_PARENT_ZERO_THEOREM"),
        ("CMC3771_3_b_mA", "b_mA", "species/material mass response after removing pure common unit mode", "material/species mass marker leakage", "WEP;R10;Newton GM", "MISSING_MATERIAL_MASS_MARKER_DESCENT"),
        ("CMC3771_4_b_nuc", "b_nuc", "nuclear/binding response not captured by alpha or simple mass ratios", "binding and nuclear marker leakage", "clock;WEP;composition", "MISSING_NUCLEAR_BINDING_RESPONSE"),
        ("CMC3771_5_b_charge", "b_charge", "vertical derivative of charge/gauge representation labels or charge ratios", "charge-marker leakage", "EM;WEP;R10", "MISSING_GAUGE_REPRESENTATION_DESCENT"),
        ("CMC3771_6_b_clock", "b_clock_i", "vertical derivative of clock transition/readout marker after alpha/mass/nuclear projection", "clock apparatus marker leakage", "clock comparison;redshift/LPI", "MISSING_CLOCK_MARKER_DESCENT"),
        ("CMC3771_7_b_material_label", "b_material_label", "vertical derivative of material labels, composition fractions, or test-body identity markers", "composition-label leakage", "WEP;R10;source universality", "MISSING_MATERIAL_LABEL_SUPERSELECTION"),
        ("CMC3771_8_b_source_norm", "b_source_norm", "vertical derivative of source normalization common mode after observable calibration", "active/passive/inertial source mismatch", "Newton GM;Gdot;PPN source", "MISSING_NEWTON_SOURCE_NORMALIZATION_OWNER"),
    ]
    return [
        {
            **base(timestamp),
            "coefficient_id": coefficient_id,
            "symbol": symbol,
            "definition": definition,
            "physical_meaning": physical_meaning,
            "feeds_observables": feeds_observables,
            "candidate_value": candidate_value,
            "units": "dimensionless_or_normalized_vertical_derivative",
            "score_ready": False,
            "claim_allowed": False,
        }
        for coefficient_id, symbol, definition, physical_meaning, feeds_observables, candidate_value in rows
    ]


def bound_budget_rows(timestamp: str, values: dict[str, str]) -> list[dict[str, object]]:
    rows = [
        ("CBB3771_0_WEP_theta", "eta_theta_AB", "dimensionless", "eta_theta_AB <= sum_I |DeltaQ_I^AB| |b_I| tau_WEP + source/EM residuals", values["wep_bound"], "P8_Y5_R2FR_3759_WEP_BOUND_EVALUATION.csv:WB3759_2_max_allowed_residual", "strict composition budget for constant/material leakage"),
        ("CBB3771_1_EM_binding_WEP", "eta_EM_theta_AB", "dimensionless", "eta_EM_theta_AB <= |Delta_AB f_EM||b_alpha| + |Delta_AB b_bind| + EM source residuals", values["em_wep_bound"], "P8_Y5_R2FR_3760_EM_SOURCE_RESIDUAL_BUDGET.csv:EMR3760_0_WEP_EM_binding", "EM/binding marker contribution to WEP"),
        ("CBB3771_2_clock_ratio", "delta_ln_clock_ratio", "fractional_frequency_or_yr^-1", "delta ln(nu_a/nu_b)=sum_I DeltaK_I^ab b_I dX + readout residual", "MISSING_CLOCK_PRODUCT_BOUND_SOURCE_OR_PROJECTION", "P8_Y5_PARENT_QLOC_1805_ALPHA_MASS_CLOCK_BOUND_MATRIX.csv:BM1805_0_alpha_clock", "clock source-backed shape exists but MTS product coefficients remain missing"),
        ("CBB3771_3_clock_redshift", "alpha_clock_redshift", "dimensionless", "alpha_clock_redshift=P_clock[b_clock_i,metric_readout_residual,source potential map]", "MISSING_CLOCK_REDSHIFT_PROJECTION", "P8_Y5_PARENT_QLOC_1805_ALPHA_MASS_CLOCK_BOUND_MATRIX.csv:BM1805_1_clock_redshift", "LPI/redshift clock row remains nonclaim until projection is supplied"),
        ("CBB3771_4_R10_alpha", "alpha_X(lambda_X)", "range-dependent", "alpha_X(lambda_X) ~ K_X Qbar_source Qbar_test/(4*pi*Z_X*G_obs)", "MISSING_R10_FULL_CURVE_AND_MATERIAL_CHARGES", "P8_Y5_PARENT_QLOC_1805_ALPHA_MASS_CLOCK_BOUND_MATRIX.csv:BM1805_3_R10_yukawa", "R10 material charge route remains nonclaim"),
        ("CBB3771_5_gamma_theta", "delta_gamma_theta", "dimensionless", "delta_gamma_theta <= C_gamma_theta epsilon_theta + C_gamma_src epsilon_src", values["gamma_bound"], "P8_Y5_R2FR_3761_GAMMA_BETA_BOUND_EVALUATION.csv:PGB3761_0_gamma_conditional_zero", "PPN gamma envelope for constant/source normalization leakage"),
        ("CBB3771_6_beta_theta", "delta_beta_theta", "dimensionless", "delta_beta_theta <= C_beta_theta epsilon_theta + C_beta_bind b_nuc + C_beta_src epsilon_src", values["beta_bound"], "P8_Y5_R2FR_3761_GAMMA_BETA_BOUND_EVALUATION.csv:PGB3761_1_beta_conditional_zero", "PPN beta envelope for nonlinear material/source leakage"),
        ("CBB3771_7_Gdot_theta", "dln_Geff_dt_theta", "yr^-1", "dln_Geff_dt_theta <= |d_t epsilon_theta| + |d_t b_source_norm| + kappa/source calibration residuals", values["gdot_bound"], "P8_Y5_R2FR_3768_KAPPA_BOUND_BUDGET.csv:KBB3768_0_Gdot_total", "rate budget for time-varying constant/source-normalization leakage"),
        ("CBB3771_8_Newton_source_norm", "delta_ln_mu_obs_theta", "dimensionless", "delta ln mu_obs|_theta <= C_mu_theta epsilon_theta + b_source_norm + binding/source residuals", "MISSING_NEWTON_ACTIVE_PASSIVE_SOURCE_PROJECTION", "P8_Y5_R2FR_3770_SOURCE_ACTION_BOUND_BUDGET.csv:SAB3770_6_Newton_source", "main Newtonian mechanics blocker"),
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
    theorem_emitted = any(row["theorem_id"] == "CMT3771_2_conditional_zero" for row in grouped["theorem"])
    zero_signed = any(row["attempt_id"] == "CZA3771_7_verdict" and row["passes_clause"] is True for row in grouped["zero_attempt"])
    unit_cheat_removed = any(row["audit_id"] == "UGA3771_1_alpha_EM" for row in grouped["unit_gauge"])
    numeric_budgets = all(
        any(str(row["bound_value"]) == value for row in grouped["bound_budget"])
        for value in {"2.8e-15", "2.3e-05", "7.8e-05", "9.6e-15"}
    )
    missing_rows = any(str(row["bound_value"]).startswith("MISSING_") for row in grouped["bound_budget"])
    rows = [
        ("CG3771_0_sources", "all 3771 source paths exist", sources_exist, "path hygiene"),
        ("CG3771_1_theta_zero_theorem", "constant/material-marker conditional zero theorem emitted", theorem_emitted, "zero route exists"),
        ("CG3771_2_unit_cheat_removed", "dimensionful-unit escape is explicitly rejected", unit_cheat_removed, "dimensionless observables only"),
        ("CG3771_3_current_zero_signed", "current branch signs L_leak_theta=0", zero_signed, "blocked by unsigned superselection/material/source-normalization proofs"),
        ("CG3771_4_coefficients_named", "constant/material residual coefficient rows emitted", len(grouped["coefficients"]) >= 9, "b_alpha, b_mu, material, clock, and source-normalization rows named"),
        ("CG3771_5_numeric_bound_envelopes", "WEP/PPN/Gdot envelopes emitted", numeric_budgets, "source-backed external envelopes are wired"),
        ("CG3771_6_missing_rows_nonclaim", "clock/R10/Newton rows remain explicit blockers", missing_rows, "no claim with missing projection inputs"),
        ("CG3771_7_constants_material_claim", "constants/material-marker closure claim allowed", False, "blocked until zero proof or all coefficients are sourced and below bounds"),
        ("CG3771_8_local_gr_claim", "local GR/Newton claim allowed", False, "blocked by Newton active/passive source projection and remaining leak gates"),
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
        ("DEC3771_0", "The constants/material-marker problem is not generic vibes; it is exactly L_leak_theta=zeta^A sum_I (partial L_src/partial theta_I) Lie_EA theta_I.", "treat theta leakage as a vertical derivative problem"),
        ("DEC3771_1", "A pure unit/common-scale mode is not a physical force in dimensionless readouts, but it is not enough to close Newtonian GM.", "do not use unit rescaling to claim absolute G or source mass derivation"),
        ("DEC3771_2", "The clean derivation route is superselection or q_obs-ownership of alpha, mass ratios, charge/gauge labels, material labels, binding fractions, and clock markers.", "hunt for parent-action clauses that make Lie_EA theta_I=0"),
        ("DEC3771_3", "If zero proof fails, the empirical route is now specified: b_alpha, b_mu, b_mA, b_nuc, b_charge, b_clock, b_material_label, and b_source_norm must be sourced or bounded.", "do not claim clock/WEP/R10/Newton pass while these rows are placeholders"),
        ("DEC3771_4", "The next highest-value leap is Newtonian active/passive/inertial source normalization, because local GR is not meaningful until the same source charge gives Newtonian GM.", "attack source Hamiltonian normalization next"),
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
            "next_id": "NEXT3771_0",
            "target_doc": "3772-Y5-R2FR-source-Hamiltonian-normalization-or-Newton-active-passive-GM-bound.md",
            "target_script": "scripts/Y5_R2FR_3772_source_Hamiltonian_normalization_or_Newton_active_passive_GM_bound.py",
            "objective": "prove the local matter/source Hamiltonian gives the same inertial, passive, and active source charge in the q_obs branch, or emit a Newtonian GM/source-normalization residual bound",
            "reason": "3771 isolates theta/common-mode safety, but Newtonian mechanics still needs active/passive/inertial source normalization rather than only WEP/PPN envelopes",
            "claim_allowed": False,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "status": "CONSTANT_MARKER_ZERO_THEOREM_DERIVED_UNIT_CHEAT_REJECTED_BOUNDS_WIRED_NOT_PARENT_SIGNED",
            "summary": "3771 derives the exact constants/material-marker leak operator and its conditional zero theorem. It separates harmless unit/common-scale gauge from physical dimensionless constant and material-label leakage, wires WEP/clock/R10/PPN/Gdot/Newton bound interfaces, and keeps all claims closed because parent superselection, material-marker descent, clock projection, R10 material charges, and Newton active/passive source normalization are not signed.",
            "claim_allowed": False,
        }
    ]


def validation_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks = [
        ("sources_exist", "all 3771 source paths exist", all(Path(str(row["source_path"])).exists() for row in grouped["sources"])),
        ("generated_csvs_parse", "all generated 3771 csvs parse", all(read_csv(path) for path in generated_csvs)),
        ("theta_zero_theorem", "constant/material-marker zero theorem emitted", any(row["theorem_id"] == "CMT3771_2_conditional_zero" for row in grouped["theorem"])),
        ("theta_leak_operator", "L_leak_theta operator emitted", any(row["theorem_id"] == "CMT3771_1_theta_leak_operator" for row in grouped["theorem"])),
        ("unit_cheat_rejected", "dimensionful unit rescaling is not accepted as proof", any(row["audit_id"] == "UGA3771_0_dimensionful_mass_scale" and row["claim_allowed"] is False for row in grouped["unit_gauge"])),
        ("zero_not_claimed", "current branch keeps L_leak_theta zero unsigned", any(row["attempt_id"] == "CZA3771_7_verdict" and row["passes_clause"] is False for row in grouped["zero_attempt"])),
        ("coefficient_rows", "at least nine constants/material coefficient rows emitted", len(grouped["coefficients"]) >= 9),
        ("numeric_bound_envelopes", "WEP/PPN/Gdot numeric envelopes emitted", all(any(str(row["bound_value"]) == value for row in grouped["bound_budget"]) for value in {"2.8e-15", "2.3e-05", "7.8e-05", "9.6e-15"})),
        ("missing_rows_nonclaim", "clock/R10/Newton blockers remain explicit", any(row["bound_value"] == "MISSING_CLOCK_PRODUCT_BOUND_SOURCE_OR_PROJECTION" for row in grouped["bound_budget"]) and any(row["bound_value"] == "MISSING_R10_FULL_CURVE_AND_MATERIAL_CHARGES" for row in grouped["bound_budget"]) and any(row["bound_value"] == "MISSING_NEWTON_ACTIVE_PASSIVE_SOURCE_PROJECTION" for row in grouped["bound_budget"])),
        ("claim_gates_closed", "constants/local-GR claims remain closed", all(row["passed"] is False for row in grouped["claim_gates"] if row["gate_id"] in {"CG3771_3_current_zero_signed", "CG3771_7_constants_material_claim", "CG3771_8_local_gr_claim"})),
        ("next_target", "3772 Newton source-normalization target emitted", grouped["next_target"][0]["target_doc"] == "3772-Y5-R2FR-source-Hamiltonian-normalization-or-Newton-active-passive-GM-bound.md"),
        ("no_formalization_leak", "no 3771 files written to formalization-workbench", not FORMALIZATION.exists() or not list(FORMALIZATION.rglob("*3771*"))),
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
        "# 3771 - Constants/Material Marker Leak Zero Or Clock/WEP/Alpha Bound",
        "",
        "## Status",
        "",
        f"`{grouped['status'][0]['status']}`.",
        "",
        grouped["status"][0]["summary"],
        "",
        "## Result In Plain Terms",
        "",
        "This checkpoint attacks the coupling obstruction directly. If physical constants, masses, charges, clock markers, and material labels are fixed labels of the `q_obs` branch, then the hidden fibre cannot change them and `L_leak_theta=0`. If they can wiggle, the wiggle is no longer vague: it is a named vector of `b_alpha`, `b_mu`, material, binding, clock, and source-normalization coefficients that feeds WEP, clocks, R10, PPN, Gdot, and Newtonian GM.",
        "",
        "## Constants/Marker Theorem",
    ]
    for row in grouped["theorem"]:
        lines.append(f"- `{row['theorem_id']}` `{row['status']}`: {row['statement']} Derivation: {row['derivation']}")
    lines.extend(["", "## Zero Proof Attempt"])
    for row in grouped["zero_attempt"]:
        lines.append(f"- `{row['attempt_id']}` pass=`{row['passes_clause']}`: {row['required_clause']}. Evidence: {row['evidence']}.")
    lines.extend(["", "## Unit Gauge Audit"])
    for row in grouped["unit_gauge"]:
        lines.append(f"- `{row['audit_id']}` `{row['classification']}`: {row['mode']}. Rule: {row['observable_rule']}. Requirement: {row['remaining_requirement']}.")
    lines.extend(["", "## Residual Coefficients"])
    for row in grouped["coefficients"]:
        lines.append(f"- `{row['coefficient_id']}` `{row['symbol']}`: {row['definition']} Value: `{row['candidate_value']}`.")
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
        "unit_gauge": unit_gauge_rows(timestamp),
        "coefficients": coefficient_rows(timestamp),
        "bound_budget": bound_budget_rows(timestamp, values),
        "decision_rows": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
    }
    grouped["claim_gates"] = claim_gate_rows(timestamp, grouped)

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["theorem"], grouped["theorem"])
    write_csv(OUTPUTS["zero_attempt"], grouped["zero_attempt"])
    write_csv(OUTPUTS["unit_gauge"], grouped["unit_gauge"])
    write_csv(OUTPUTS["coefficients"], grouped["coefficients"])
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
        raise SystemExit(f"3771 validation failed: {failures}")
    print("wrote 3771 checkpoint: constants/material-marker leak theorem, unit audit, and bound interfaces emitted")


if __name__ == "__main__":
    main()

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3770"
BRANCH = "MTS_R2FR_Y5_SOURCE_ACTION_LEAK_ZERO_OR_WEP_EM_PPN_BOUND_3770"
PCW = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work"
)
RESIDUALS = PCW / "source-intake" / "mts_residuals"
FORMALIZATION = PCW.parent / "formalization-workbench"
DOC_PATH = PCW / "3770-Y5-R2FR-source-action-leak-zero-or-WEP-EM-PPN-bound.md"


OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3770_SOURCE_REGISTER.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_3770_SOURCE_ACTION_ZERO_THEOREM.csv",
    "zero_attempt": RESIDUALS / "P8_Y5_R2FR_3770_SOURCE_ACTION_ZERO_ATTEMPT.csv",
    "coefficients": RESIDUALS / "P8_Y5_R2FR_3770_SOURCE_ACTION_RESIDUAL_COEFFICIENTS.csv",
    "bound_budget": RESIDUALS / "P8_Y5_R2FR_3770_SOURCE_ACTION_BOUND_BUDGET.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_3770_CLAIM_GATES.csv",
    "decision_rows": RESIDUALS / "P8_Y5_R2FR_3770_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3770_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3770_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3770_VALIDATION.csv",
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
        "SRC3770_0_3769_doc": PCW / "3769-Y5-R2FR-shadow-metric-frame-leak-zero-or-PPN-clock-bound.md",
        "SRC3770_1_3769_next": RESIDUALS / "P8_Y5_R2FR_3769_NEXT_TARGET.csv",
        "SRC3770_2_3767_operator_basis": RESIDUALS / "P8_Y5_R2FR_3767_LLEAK_OPERATOR_BASIS.csv",
        "SRC3770_3_3764_source_theorem": RESIDUALS / "P8_Y5_R2FR_3764_SAME_TOTAL_SOURCE_VARIATION_THEOREM.csv",
        "SRC3770_4_3760_em_theorem": RESIDUALS / "P8_Y5_R2FR_3760_MAXWELL_EM_STRESS_SOURCE_THEOREM.csv",
        "SRC3770_5_3760_em_budget": RESIDUALS / "P8_Y5_R2FR_3760_EM_SOURCE_RESIDUAL_BUDGET.csv",
        "SRC3770_6_3759_wep_theorem": RESIDUALS / "P8_Y5_R2FR_3759_SOURCE_UNIVERSALITY_THEOREM.csv",
        "SRC3770_7_3759_wep_budget": RESIDUALS / "P8_Y5_R2FR_3759_WEP_BOUND_EVALUATION.csv",
        "SRC3770_8_3761_ppn_budget": RESIDUALS / "P8_Y5_R2FR_3761_PPN_RESIDUAL_BUDGET.csv",
        "SRC3770_9_3761_ppn_eval": RESIDUALS / "P8_Y5_R2FR_3761_GAMMA_BETA_BOUND_EVALUATION.csv",
        "SRC3770_10_3765_sector_residual": RESIDUALS / "P8_Y5_R2FR_3765_SECTOR_READOUT_RESIDUAL_MAP.csv",
    }


def source_register(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "source_id": source_id,
            "source_path": str(path),
            "source_exists": path.exists(),
            "role": "3770 source action zero theorem and WEP/EM/PPN bound input",
        }
        for source_id, path in source_paths().items()
    ]


def find_row(path: Path, key: str, value: str) -> dict[str, str]:
    for row in read_csv(path):
        if row.get(key) == value:
            return row
    raise KeyError(f"missing row {key}={value} in {path}")


def numeric_inputs() -> dict[str, float]:
    wep = find_row(source_paths()["SRC3770_7_3759_wep_budget"], "evaluation_id", "WB3759_2_max_allowed_residual")
    gamma = find_row(source_paths()["SRC3770_9_3761_ppn_eval"], "evaluation_id", "PGB3761_0_gamma_conditional_zero")
    beta = find_row(source_paths()["SRC3770_9_3761_ppn_eval"], "evaluation_id", "PGB3761_1_beta_conditional_zero")
    em_wep = find_row(source_paths()["SRC3770_5_3760_em_budget"], "residual_id", "EMR3760_0_WEP_EM_binding")
    em_gamma = find_row(source_paths()["SRC3770_5_3760_em_budget"], "residual_id", "EMR3760_1_gamma_EM_stress_projection")
    em_beta = find_row(source_paths()["SRC3770_5_3760_em_budget"], "residual_id", "EMR3760_2_beta_EM_nonlinear_source")
    return {
        "wep_bound": float(wep["bound_value"]),
        "gamma_bound": float(gamma["bound_value"]),
        "beta_bound": float(beta["bound_value"]),
        "em_wep_bound": float(em_wep["bound_value"]),
        "em_gamma_bound": float(em_gamma["bound_value"]),
        "em_beta_bound": float(em_beta["bound_value"]),
    }


def theorem_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "SAT3770_0_source_descent_condition",
            "The zero route is S_src[Phi,psi,A,theta]=Sbar_src[q_obs(Phi),psi,A,theta] with theta quotient-owned/superselected and one observed metric/coframe already selected.",
            "Then every source variation sees Phi only through q_obs.",
            "This is the non-smuggled same-source premise.",
            "SOURCE_DESCENT_CONDITION",
        ),
        (
            "SAT3770_1_vertical_source_current",
            "For E_A in ker(Dq_obs), define J_A^src := delta S_src/dzeta^A along the q_obs fibre.",
            "If S_src descends through q_obs and Lie_EA theta=0, then J_A^src=0.",
            "This is the action-level leak coefficient for source coupling.",
            "EXACT_SOURCE_CURRENT_DEFINITION",
        ),
        (
            "SAT3770_2_chain_rule_zero",
            "Lie_EA S_src = (delta Sbar_src/dq_obs)Dq_obs[E_A] + sum_i(partial Sbar_src/partial theta_i)Lie_EA theta_i = 0.",
            "Dq_obs[E_A]=0 and Lie_EA theta_i=0.",
            "This proves L_leak_src=0 if the parent signs source descent and constant/material-marker silence.",
            "EXACT_CONDITIONAL_ZERO_THEOREM",
        ),
        (
            "SAT3770_3_total_Hilbert_source",
            "If S_src descends, T_total^{ab}:=(2/sqrt(-g_eff))delta S_src/dg_eff_ab is one total source containing material, EM, binding, apparatus, and interaction stresses.",
            "Variation is linear in the same g_eff/coframe.",
            "This activates the 3764 same-total-source theorem.",
            "EXACT_CONDITIONAL_TOTAL_SOURCE_THEOREM",
        ),
        (
            "SAT3770_4_internal_exchange_cancellation",
            "For descended Maxwell/matter sectors, div T_EM=-FJ and div T_material=+FJ cancel inside div T_total; only parent exchange or non-Hilbert owner currents remain.",
            "Imported from 3760 and 3764 under the same action.",
            "This is why EM is not a separate gravitational charge when same-source descent is true.",
            "EXACT_CONDITIONAL_WARD_THEOREM",
        ),
        (
            "SAT3770_5_failure_leak_operator",
            "If source descent fails, L_leak_src = zeta^A J_A^src + O(zeta^2), with sector components J_A^matter, J_A^EM, J_A^binding, J_A^apparatus, and J_A^int.",
            "First-order fibre expansion of S_src along ker(Dq_obs).",
            "Failure becomes source-current coefficients, not a handwaved coupling problem.",
            "EXACT_FIRST_ORDER_RESIDUAL_DEFINITION",
        ),
        (
            "SAT3770_6_observable_projection",
            "Source-current residuals project into eta_source_AB, eta_EM_AB, delta_gamma_source, delta_beta_source, Gdot/source-conservation, and Newtonian GM/source calibration rows.",
            "Projection coefficients must be derived or sourced before any claim.",
            "This connects same-source descent directly to local tests.",
            "WEP_EM_PPN_BOUND_INTERFACE",
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
        ("SZA3770_0_qobs_and_metric_ready", "q_obs and one observed metric target exist", "3765/3769 provide q_obs and one-metric residual interface", True, "source descent can now be tested against a target geometry"),
        ("SZA3770_1_same_source_theorem_ready", "same-total-source theorem exists", "3764 proves the conditional variation theorem", True, "zero route is mathematically clear"),
        ("SZA3770_2_EM_ward_ready", "EM internal exchange cancellation theorem exists", "3760 proves Maxwell/matter Ward cancellation under same action", True, "EM bookkeeping can close if parent descent is signed"),
        ("SZA3770_3_source_action_descends", "S_src=Sbar_src(q_obs,psi,A,theta)", "3764 requires this but marks parent signature unsigned", False, "J_A^src remains live"),
        ("SZA3770_4_constants_markers_silent", "masses, charges, material labels, binding fractions, and clock/apparatus constants are quotient-owned or superselected", "3646/3767 retain constants/material marker leak as live", False, "J_A^theta and WEP source residuals remain live"),
        ("SZA3770_5_universal_no_species_kappa", "no species-labelled gravitational coupling in source action", "3759 requires same action/source-blindness but does not parent-sign it", False, "eta_source_AB remains live"),
        ("SZA3770_6_EM_same_source_descent", "EM low-energy stress descends to the same Hilbert/coframe source", "3760 marks MTS emergent EM descent required", False, "eta_EM_AB and EM PPN residuals remain live"),
        ("SZA3770_7_verdict", "L_leak_src=0 for current MTS local branch", "zero theorem exists but parent source descent/constants/EM descent are unsigned", False, "do not claim WEP/EM/PPN source closure"),
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


def coefficient_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("SRC3770_0_total_source_current", "epsilon_src", "sup_A |zeta^A J_A^src|/|L_src|", "total source action leakage along q_obs fibre", "WEP, EM, PPN source projection", "MISSING_SOURCE_ACTION_DESCENT"),
        ("SRC3770_1_matter_current", "epsilon_matter_src", "sup_A |zeta^A J_A^matter|/|L_matter|", "matter species/source current not q_obs-descended", "WEP/source universality", "MISSING_MATTER_SOURCE_DESCENT"),
        ("SRC3770_2_EM_current", "epsilon_EM_src", "sup_A |zeta^A J_A^EM|/|L_EM|", "EM field stress/source action not same-source descended", "eta_EM_AB, gamma_EM, beta_EM", "MISSING_EM_SOURCE_DESCENT"),
        ("SRC3770_3_binding_current", "epsilon_binding_src", "sup_A |zeta^A J_A^binding|/|L_binding|", "binding energy source not included in one total Hilbert source", "WEP, beta, composite-body source charge", "MISSING_BINDING_SOURCE_DESCENT"),
        ("SRC3770_4_apparatus_current", "epsilon_apparatus_src", "sup_A |zeta^A J_A^apparatus|/|L_apparatus|", "apparatus/readout stress not included in same source action", "calibrated source coupling, clock/readout residuals", "MISSING_APPARATUS_SOURCE_DESCENT"),
        ("SRC3770_5_interaction_current", "epsilon_int_src", "sup_A |zeta^A J_A^int|/|L_int|", "interaction exchange not internal to one total source", "source conservation, EM Ward exchange, Gdot", "MISSING_INTERACTION_SOURCE_DESCENT"),
        ("SRC3770_6_species_coupling", "epsilon_species_kappa", "sup_AB |Delta_AB ln kappa_eff| from source-action labels", "species-labelled gravitational coupling", "MICROSCOPE/WEP", "MISSING_NO_SPECIES_COUPLING_PROOF"),
        ("SRC3770_7_source_projection", "epsilon_PPN_source", "|Delta_source_projection|+|Delta_source_nonlinear|", "PPN source tensor mismatch from non-descended source action", "gamma,beta", "MISSING_PPN_SOURCE_PROJECTION_COEFFICIENT"),
        ("SRC3770_8_Newton_source_calibration", "epsilon_mu_source", "|delta ln mu_obs|_source", "Newtonian active/passive source calibration leak", "Newtonian mechanics, orbital GM, Gdot", "MISSING_NEWTON_SOURCE_PROJECTION"),
    ]
    return [
        {
            **base(timestamp),
            "coefficient_id": coefficient_id,
            "symbol": symbol,
            "definition": definition,
            "physical_meaning": physical_meaning,
            "feeds_observables": feeds_observables,
            "numeric_value": numeric_value,
            "units": "dimensionless_or_normalized_source_current",
            "claim_allowed": False,
        }
        for coefficient_id, symbol, definition, physical_meaning, feeds_observables, numeric_value in rows
    ]


def bound_budget_rows(timestamp: str, values: dict[str, float]) -> list[dict[str, object]]:
    rows = [
        ("SAB3770_0_WEP_total", "eta_source_AB", "dimensionless", "eta_source_AB <= C_m epsilon_matter_src + C_theta epsilon_theta + C_species epsilon_species_kappa + C_EM epsilon_EM_src + C_int epsilon_int_src", values["wep_bound"], "P8_Y5_R2FR_3759_WEP_BOUND_EVALUATION.csv:WB3759_2_max_allowed_residual", "strict WEP source-action envelope"),
        ("SAB3770_1_EM_WEP", "eta_EM_AB", "dimensionless", "eta_EM_AB <= |Delta_AB f_EM||delta_kappa_EM| + |Delta_AB ln Z_EM| + |Delta_AB q_EM_exchange| + C_EM epsilon_EM_src", values["em_wep_bound"], "P8_Y5_R2FR_3760_EM_SOURCE_RESIDUAL_BUDGET.csv:EMR3760_0_WEP_EM_binding", "EM/binding same-source WEP envelope"),
        ("SAB3770_2_gamma_source", "delta_gamma_source", "dimensionless", "delta_gamma_source <= C_gamma_src epsilon_PPN_source + C_gamma_EM epsilon_EM_src + C_gamma_frame epsilon_shadow", values["gamma_bound"], "P8_Y5_R2FR_3761_GAMMA_BETA_BOUND_EVALUATION.csv:PGB3761_0_gamma_conditional_zero", "Cassini/Shapiro source-projection envelope"),
        ("SAB3770_3_beta_source", "delta_beta_source", "dimensionless", "delta_beta_source <= C_beta_src epsilon_PPN_source + C_beta_binding epsilon_binding_src + C_beta_EM epsilon_EM_src", values["beta_bound"], "P8_Y5_R2FR_3761_GAMMA_BETA_BOUND_EVALUATION.csv:PGB3761_1_beta_conditional_zero", "PPN beta nonlinear source envelope"),
        ("SAB3770_4_EM_gamma", "delta_gamma_EM", "dimensionless", "delta_gamma_EM <= |epsilon_EM_metric| + |Pi_PPN q_EM_exchange| + |Delta_EM_source_frame| + C_gamma_EM epsilon_EM_src", values["em_gamma_bound"], "P8_Y5_R2FR_3760_EM_SOURCE_RESIDUAL_BUDGET.csv:EMR3760_1_gamma_EM_stress_projection", "EM stress projection envelope"),
        ("SAB3770_5_EM_beta", "delta_beta_EM", "dimensionless", "delta_beta_EM <= |epsilon_EM_nonlinear| + |Delta_EM_binding_second_order| + |Pi_beta q_EM_exchange| + C_beta_EM epsilon_EM_src", values["em_beta_bound"], "P8_Y5_R2FR_3760_EM_SOURCE_RESIDUAL_BUDGET.csv:EMR3760_2_beta_EM_nonlinear_source", "EM nonlinear/binding envelope"),
        ("SAB3770_6_Newton_source", "delta ln mu_obs|_source", "dimensionless", "delta ln mu_obs|_source <= C_mu_src epsilon_src + C_mu_binding epsilon_binding_src + C_mu_int epsilon_int_src", "MISSING_NEWTON_SOURCE_BOUND", "requires Newtonian active/passive source projection", "nonclaim Newtonian source calibration interface"),
        ("SAB3770_7_Gdot_source", "dln_Geff_dt_source", "yr^-1", "dln_Geff_dt_source <= |d_t epsilon_src| + |R_source_exchange| + |d_t Z_source|", "MISSING_SOURCE_RATE_COMPONENTS", "requires source-current rate coefficients", "nonclaim source-rate interface"),
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
    theorem_emitted = any(row["theorem_id"] == "SAT3770_2_chain_rule_zero" for row in grouped["theorem"])
    zero_signed = any(row["attempt_id"] == "SZA3770_7_verdict" and row["passes_clause"] is True for row in grouped["zero_attempt"])
    numeric_budgets = all(any(str(row["bound_value"]) == value for row in grouped["bound_budget"]) for value in {"2.8e-15", "2.3e-05", "7.8e-05"})
    rows = [
        ("CG3770_0_sources", "all 3770 source paths exist", sources_exist, "path hygiene"),
        ("CG3770_1_source_zero_theorem", "source action chain-rule zero theorem emitted", theorem_emitted, "same-source descent route exists"),
        ("CG3770_2_current_zero_signed", "current branch signs L_leak_src=0", zero_signed, "blocked by unsigned source/action/constants/EM descent"),
        ("CG3770_3_residual_coefficients", "source-current residual coefficient rows emitted", len(grouped["coefficients"]) >= 9, "J_A^src components are named"),
        ("CG3770_4_numeric_budgets", "WEP/EM/PPN numeric envelopes emitted", numeric_budgets, "source-backed WEP/EM/PPN envelopes exist"),
        ("CG3770_5_Newton_source_bound", "Newtonian source calibration bound sourced", False, "Newton active/passive projection remains missing"),
        ("CG3770_6_same_total_source_claim", "same total Hilbert/coframe source claim allowed", False, "blocked until zero proof or all source-current projections are below bounds"),
        ("CG3770_7_local_gr_claim", "local GR/Newton claim allowed", False, "blocked by remaining L_leak/constants/range/boundary/readout gates"),
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
        ("DEC3770_0", "Same observed metric and same total source are distinct requirements.", "do not claim local GR until both frame and source action descent are closed"),
        ("DEC3770_1", "The source-action leak is now the current J_A^src along ker(Dq_obs), with named matter/EM/binding/apparatus/interaction components.", "prove each source-current component zero or fill coefficient rows"),
        ("DEC3770_2", "WEP, EM, and PPN envelopes are sourced, but Newtonian active/passive source calibration and source-rate components remain missing.", "source or derive Newton/source-rate projections before any calibrated Newton claim"),
        ("DEC3770_3", "The next leak is constants/material markers because source descent still fails if masses, charges, clock ratios, or material labels see the vertical fibre.", "attack L_leak_theta next"),
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
            "next_id": "NEXT3770_0",
            "target_doc": "3771-Y5-R2FR-constants-material-marker-leak-zero-or-clock-WEP-alpha-bound.md",
            "target_script": "scripts/Y5_R2FR_3771_constants_material_marker_leak_zero_or_clock_WEP_alpha_bound.py",
            "objective": "prove constants/material markers are quotient-owned or superselected so L_leak_theta=0, or emit WEP/clock/alpha/mass-coefficient bounds for vertical dependence of masses, charges, clock ratios, material labels, and binding fractions",
            "reason": "3770 leaves source descent blocked mainly by theta/material-marker silence; this is the next source-coupling obstruction",
            "claim_allowed": False,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "status": "SOURCE_ACTION_ZERO_THEOREM_DERIVED_WEP_EM_PPN_BOUND_INTERFACE_EMITTED_NOT_PARENT_SIGNED",
            "summary": "3770 derives the source action chain-rule zero theorem: if S_src descends through q_obs and constants/material markers are silent, then J_A^src=0 and one total Hilbert/coframe source exists. The current branch does not sign source descent, so source-current components remain live with WEP/EM/PPN bound envelopes; Newton/source-rate projections remain missing.",
            "claim_allowed": False,
        }
    ]


def validation_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks = [
        ("sources_exist", "all 3770 source paths exist", all(Path(str(row["source_path"])).exists() for row in grouped["sources"])),
        ("generated_csvs_parse", "all generated 3770 csvs parse", all(read_csv(path) for path in generated_csvs)),
        ("source_zero_theorem", "source action zero theorem emitted", any(row["theorem_id"] == "SAT3770_2_chain_rule_zero" for row in grouped["theorem"])),
        ("source_leak_operator", "source leak operator emitted", any(row["theorem_id"] == "SAT3770_5_failure_leak_operator" for row in grouped["theorem"])),
        ("zero_not_claimed", "current branch keeps L_leak_src zero unsigned", any(row["attempt_id"] == "SZA3770_7_verdict" and row["passes_clause"] is False for row in grouped["zero_attempt"])),
        ("coefficient_rows", "at least nine source-current coefficient rows emitted", len(grouped["coefficients"]) >= 9),
        ("numeric_budgets", "WEP/EM/PPN numeric bound envelopes emitted", all(any(str(row["bound_value"]) == value for row in grouped["bound_budget"]) for value in {"2.8e-15", "2.3e-05", "7.8e-05"})),
        ("newton_rate_missing_nonclaim", "Newton/source-rate projections remain explicit blockers", any(row["bound_value"] == "MISSING_NEWTON_SOURCE_BOUND" for row in grouped["bound_budget"]) and any(row["bound_value"] == "MISSING_SOURCE_RATE_COMPONENTS" for row in grouped["bound_budget"])),
        ("claim_gates_closed", "same-source/local-GR claims remain closed", all(row["passed"] is False for row in grouped["claim_gates"] if row["gate_id"] in {"CG3770_2_current_zero_signed", "CG3770_6_same_total_source_claim", "CG3770_7_local_gr_claim"})),
        ("next_target", "3771 constants/material-marker target emitted", grouped["next_target"][0]["target_doc"] == "3771-Y5-R2FR-constants-material-marker-leak-zero-or-clock-WEP-alpha-bound.md"),
        ("no_formalization_leak", "no 3770 files written to formalization-workbench", not FORMALIZATION.exists() or not list(FORMALIZATION.rglob("*3770*"))),
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
        "# 3770 - Source Action Leak Zero Or WEP/EM/PPN Bound",
        "",
        "## Status",
        "",
        f"`{grouped['status'][0]['status']}`.",
        "",
        grouped["status"][0]["summary"],
        "",
        "## Result In Plain Terms",
        "",
        "This checkpoint separates one observed metric from one observed source. The source action leak is the vertical current `J_A^src = delta S_src/dzeta^A` along `ker(Dq_obs)`. If `S_src` descends through `q_obs` and constants/material markers are silent, `J_A^src=0` and one total Hilbert/coframe source follows. If not, WEP/EM/PPN/Newton residual coefficients stay live.",
        "",
        "## Source Action Theorem",
    ]
    for row in grouped["theorem"]:
        lines.append(f"- `{row['theorem_id']}` `{row['status']}`: {row['statement']} Derivation: {row['derivation']}")
    lines.extend(["", "## Zero Proof Attempt"])
    for row in grouped["zero_attempt"]:
        lines.append(f"- `{row['attempt_id']}` pass=`{row['passes_clause']}`: {row['required_clause']}. Evidence: {row['evidence']}.")
    lines.extend(["", "## Residual Coefficients"])
    for row in grouped["coefficients"]:
        lines.append(f"- `{row['coefficient_id']}` `{row['symbol']}`: {row['definition']} Value: `{row['numeric_value']}`.")
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
        raise SystemExit(f"3770 validation failed: {failures}")
    print("wrote 3770 checkpoint: source action zero theorem and WEP/EM/PPN bound interface emitted")


if __name__ == "__main__":
    main()

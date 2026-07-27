import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3769"
BRANCH = "MTS_R2FR_Y5_SHADOW_METRIC_FRAME_LEAK_ZERO_OR_PPN_CLOCK_BOUND_3769"
PCW = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work"
)
RESIDUALS = PCW / "source-intake" / "mts_residuals"
FORMALIZATION = PCW.parent / "formalization-workbench"
DOC_PATH = PCW / "3769-Y5-R2FR-shadow-metric-frame-leak-zero-or-PPN-clock-bound.md"


OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3769_SOURCE_REGISTER.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_3769_SHADOW_FRAME_ZERO_THEOREM.csv",
    "zero_attempt": RESIDUALS / "P8_Y5_R2FR_3769_SHADOW_FRAME_ZERO_ATTEMPT.csv",
    "coefficients": RESIDUALS / "P8_Y5_R2FR_3769_SHADOW_FRAME_RESIDUAL_COEFFICIENTS.csv",
    "bound_budget": RESIDUALS / "P8_Y5_R2FR_3769_SHADOW_FRAME_BOUND_BUDGET.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_3769_CLAIM_GATES.csv",
    "decision_rows": RESIDUALS / "P8_Y5_R2FR_3769_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3769_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3769_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3769_VALIDATION.csv",
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
        "SRC3769_0_3768_doc": PCW / "3768-Y5-R2FR-kappa-EH-coefficient-quotient-zero-or-Gdot-PPN-bound.md",
        "SRC3769_1_3768_next": RESIDUALS / "P8_Y5_R2FR_3768_NEXT_TARGET.csv",
        "SRC3769_2_3767_operator_basis": RESIDUALS / "P8_Y5_R2FR_3767_LLEAK_OPERATOR_BASIS.csv",
        "SRC3769_3_3765_sector_residual": RESIDUALS / "P8_Y5_R2FR_3765_SECTOR_READOUT_RESIDUAL_MAP.csv",
        "SRC3769_4_3764_frame_fallback": RESIDUALS / "P8_Y5_R2FR_3764_FRAME_SOURCE_FALLBACK_RESIDUALS.csv",
        "SRC3769_5_3761_ppn_bounds": RESIDUALS / "P8_Y5_R2FR_3761_GAMMA_BETA_BOUND_EVALUATION.csv",
        "SRC3769_6_3762_claim_matrix": RESIDUALS / "P8_Y5_R2FR_3762_LOCAL_GR_CLAIM_MATRIX.csv",
        "SRC3769_7_3764_quotient_theorem": RESIDUALS / "P8_Y5_R2FR_3764_PARENT_QUOTIENT_DESCENT_THEOREM.csv",
        "SRC3769_8_3765_qobs_candidate": RESIDUALS / "P8_Y5_R2FR_3765_QOBS_CANDIDATE_MAP.csv",
        "SRC3769_9_1003_frame_profile": PCW / "1003-Y5-R10-Bref-covariant-frame-theorem-or-Delta-ref-frame-profile-row.md",
        "SRC3769_10_observer_contract": PCW / "10-observer-map-symplectic-contract.md",
        "SRC3769_11_private_clock_heuristics": PCW / "000-private-fork-heuristics-for-martin-style-search.md",
    }


def source_register(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "source_id": source_id,
            "source_path": str(path),
            "source_exists": path.exists(),
            "role": "3769 shadow metric/frame zero theorem and bound input",
        }
        for source_id, path in source_paths().items()
    ]


def find_row(path: Path, key: str, value: str) -> dict[str, str]:
    for row in read_csv(path):
        if row.get(key) == value:
            return row
    raise KeyError(f"missing row {key}={value} in {path}")


def numeric_inputs() -> dict[str, float]:
    gamma_row = find_row(source_paths()["SRC3769_5_3761_ppn_bounds"], "evaluation_id", "PGB3761_0_gamma_conditional_zero")
    beta_row = find_row(source_paths()["SRC3769_5_3761_ppn_bounds"], "evaluation_id", "PGB3761_1_beta_conditional_zero")
    return {
        "gamma_bound": float(gamma_row["bound_value"]),
        "beta_bound": float(beta_row["bound_value"]),
    }


def theorem_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "SFT3769_0_sector_frame_split",
            "For each sector s, write the sector coframe as e_s = Lambda_s e_obs + L_xi_s e_obs + delta e_s^perp, where Lambda_s is local Lorentz, L_xi_s is diffeomorphism drag, and delta e_s^perp is orthogonal to q_obs gauge directions.",
            "This is a local decomposition of the frame mismatch into gauge and non-gauge parts.",
            "It separates harmless representation changes from a physical shadow frame.",
            "LOCAL_FRAME_DECOMPOSITION",
        ),
        (
            "SFT3769_1_metric_shadow",
            "The metric shadow is h_s^perp_ab := delta g_s_ab - L_xi_s g_obs_ab after local Lorentz gauge is removed; local Lorentz rotations do not change g_obs.",
            "delta g_s_ab = 2 eta_IJ e_obs_(a^I delta e_s,b)^J + O(delta e^2).",
            "Only h_s^perp can produce a physical one-metric failure.",
            "EXACT_FIRST_ORDER_SHADOW_DEFINITION",
        ),
        (
            "SFT3769_2_gauge_zero",
            "If delta e_s is only local Lorentz plus diffeomorphism plus q_obs-kernel gauge, the EH density and descended source/readout actions change only by boundary/gauge terms.",
            "delta_gauge L_EH = d(i_xi L_EH) and delta_Lorentz g=0; Dq_obs(E_A)=0 kills q_obs-owned readouts.",
            "This proves the no-shadow route without smuggling a plateau axiom.",
            "EXACT_CONDITIONAL_GAUGE_ZERO_THEOREM",
        ),
        (
            "SFT3769_3_shadow_leak_operator",
            "If h_s^perp is nonzero, L_leak_shadow_g contains E_EH^{ab} h_s^perp_ab plus source/readout frame terms.",
            "delta L_EH = E_EH^{ab} h_ab + d theta(h); source/readout pieces are delta S_src/dg_s times h_s^perp when the sector uses g_s.",
            "This is the action-level residual corresponding to frame/source mismatch.",
            "EXACT_FIRST_ORDER_LEAK_OPERATOR",
        ),
        (
            "SFT3769_4_single_metric_zero",
            "If h_s^perp=0 for matter, EM, light, clock, and orbital/source sectors, then Delta q_matter, Delta q_EM, Delta q_light, Delta q_clock, and Delta q_orbit_source have no metric-frame part.",
            "All sector frames factor through Obs_e(q_obs) up to gauge.",
            "This closes the metric part of delta_frame_source conditionally.",
            "EXACT_CONDITIONAL_SINGLE_METRIC_THEOREM",
        ),
        (
            "SFT3769_5_bound_identity",
            "If h_s^perp is not zero, define epsilon_shadow_s := sup_U ||h_s^perp||_g and propagate it by delta_frame_source <= sum_s w_s epsilon_shadow_s plus nonmetric sector residuals.",
            "Triangle inequality on the sector frame residual vector.",
            "The failure branch is a residual vector, not a hidden closure assumption.",
            "RESIDUAL_BOUND_INTERFACE",
        ),
        (
            "SFT3769_6_PPN_clock_projection",
            "PPN and clock observables see only projected combinations: |gamma-1|_shadow <= C_gamma^sh epsilon_shadow_light/source, |beta-1|_shadow <= C_beta^sh epsilon_shadow_source, and clock residual <= C_clock^sh epsilon_shadow_clock.",
            "Projection coefficients must be derived or sourced before any claim.",
            "This keeps Cassini/PPN, redshift/clocks, and preferred-frame tests attached without inventing coefficients.",
            "PPN_CLOCK_PROJECTION_INTERFACE",
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
        (
            "SZA3769_0_qobs_frame_available",
            "observed frame q_obs/e_obs candidate exists",
            "3765 provides Q_obs and Obs_e(q_obs)",
            True,
            "there is a target frame for comparison",
        ),
        (
            "SZA3769_1_gauge_decomposition_available",
            "local frame mismatch can be decomposed into Lorentz/diffeomorphism/q_obs-gauge plus perpendicular shadow",
            "standard local frame decomposition used in SFT3769_0-1",
            True,
            "the residual is mathematically identifiable",
        ),
        (
            "SZA3769_2_matter_frame_descends",
            "matter frame factors through q_obs up to gauge",
            "3764/3765 require this but do not parent-sign it",
            False,
            "Delta q_matter and h_matter^perp remain live",
        ),
        (
            "SZA3769_3_light_frame_descends",
            "light/null-cone frame factors through q_obs up to gauge",
            "3765 keeps Delta q_light live",
            False,
            "gamma/Shapiro/lensing residual remains live",
        ),
        (
            "SZA3769_4_clock_frame_descends",
            "clock time generator and transition readouts factor through q_obs up to gauge",
            "3765 keeps Delta q_clock and delta_tau_obs live",
            False,
            "clock/redshift/local Lorentz residual remains live",
        ),
        (
            "SZA3769_5_EM_frame_descends",
            "EM stress/readout frame factors through q_obs up to gauge",
            "3760/3765 keep EM same-source/frame descent unsigned",
            False,
            "EM-to-WEP/PPN residual remains live",
        ),
        (
            "SZA3769_6_source_orbit_frame_descends",
            "orbital/source monopole frame factors through q_obs up to gauge",
            "3765 keeps Delta q_orbit_source live",
            False,
            "Newtonian GM/source calibration frame residual remains live",
        ),
        (
            "SZA3769_7_verdict",
            "L_leak_shadow_g=0 for current MTS local branch",
            "zero theorem exists but sector factorization/no-shadow certificates are unsigned",
            False,
            "do not claim one observed metric yet; use bound interface",
        ),
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
        (
            "SFC3769_0_h_matter",
            "epsilon_shadow_matter",
            "sup_U ||h_matter^perp||_g",
            "matter rods/source material see a metric not gauge-equivalent to g_obs",
            "WEP, matter-source calibration",
            "MISSING_MATTER_FRAME_DESCENT",
        ),
        (
            "SFC3769_1_h_light",
            "epsilon_shadow_light",
            "sup_U ||h_light^perp||_g",
            "null cone/light sees a metric not gauge-equivalent to g_obs",
            "PPN gamma, Shapiro, lensing, preferred-frame",
            "MISSING_LIGHT_FRAME_DESCENT",
        ),
        (
            "SFC3769_2_h_clock",
            "epsilon_shadow_clock",
            "sup_U ||h_clock^perp||_g + |delta tau_obs|",
            "clock time generator or transition frequencies see a different frame",
            "clock redshift, local Lorentz, time-dilation residuals",
            "MISSING_CLOCK_FRAME_DESCENT",
        ),
        (
            "SFC3769_3_h_EM",
            "epsilon_shadow_EM",
            "sup_U ||h_EM^perp||_g",
            "EM stress/Poynting/readout frame differs from q_obs",
            "EM stress, WEP, PPN source projection",
            "MISSING_EM_FRAME_DESCENT",
        ),
        (
            "SFC3769_4_h_source_orbit",
            "epsilon_shadow_source",
            "sup_U ||h_source^perp||_g",
            "source monopole/orbital readout frame differs from q_obs",
            "Newtonian GM, orbit tests, Gdot calibration",
            "MISSING_SOURCE_ORBIT_FRAME_DESCENT",
        ),
        (
            "SFC3769_5_delta_frame_metric",
            "delta_frame_metric",
            "epsilon_shadow_matter + epsilon_shadow_light + epsilon_shadow_clock + epsilon_shadow_EM + epsilon_shadow_source",
            "metric part of the 3764/3765 frame residual",
            "single observed metric gate",
            "MISSING_SECTOR_FRAME_COMPONENTS",
        ),
        (
            "SFC3769_6_Lleak_shadow",
            "L_leak_shadow_g/L_EH",
            "C_EH^sh delta_frame_metric plus source/readout projections",
            "normalized action leak from non-gauge metric-frame directions",
            "kernel-null and local EH frame gate",
            "MISSING_PARENT_COEFFICIENT",
        ),
        (
            "SFC3769_7_preferred_frame",
            "epsilon_preferred_frame",
            "projection of h_s^perp onto preferred-frame PPN/readout structures",
            "frame residual that cannot be removed by coordinate or Lorentz gauge",
            "preferred-frame tests",
            "MISSING_PREFERRED_FRAME_PROJECTION",
        ),
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
            "units": "dimensionless_or_normalized_frame_norm",
            "claim_allowed": False,
        }
        for coefficient_id, symbol, definition, physical_meaning, feeds_observables, numeric_value in rows
    ]


def bound_budget_rows(timestamp: str, values: dict[str, float]) -> list[dict[str, object]]:
    rows = [
        (
            "SBB3769_0_frame_summary",
            "delta_frame_metric",
            "dimensionless",
            "delta_frame_metric <= epsilon_shadow_matter + epsilon_shadow_light + epsilon_shadow_clock + epsilon_shadow_EM + epsilon_shadow_source",
            "MISSING_SECTOR_FRAME_COMPONENTS",
            "3765 sector frame residual map",
            "symbolic no-cancellation residual vector",
        ),
        (
            "SBB3769_1_gamma_shadow",
            "C_gamma^sh epsilon_shadow_light/source",
            "dimensionless",
            "C_gamma^sh epsilon_shadow_light/source <= gamma_bound",
            values["gamma_bound"],
            "P8_Y5_R2FR_3761_GAMMA_BETA_BOUND_EVALUATION.csv:PGB3761_0_gamma_conditional_zero",
            "Cassini/Shapiro envelope for light/source frame mismatch",
        ),
        (
            "SBB3769_2_beta_shadow",
            "C_beta^sh epsilon_shadow_source",
            "dimensionless",
            "C_beta^sh epsilon_shadow_source <= beta_bound",
            values["beta_bound"],
            "P8_Y5_R2FR_3761_GAMMA_BETA_BOUND_EVALUATION.csv:PGB3761_1_beta_conditional_zero",
            "PPN beta envelope for nonlinear source-frame mismatch",
        ),
        (
            "SBB3769_3_unit_projection_smoke",
            "epsilon_shadow_unit_projection",
            "dimensionless",
            "epsilon_shadow <= min(gamma_bound,beta_bound) if C_gamma^sh=C_beta^sh=1",
            min(values["gamma_bound"], values["beta_bound"]),
            "smoke-only unit projection from 3761 bounds",
            "dry-run scale only until frame projection coefficients are derived",
        ),
        (
            "SBB3769_4_clock_bound",
            "C_clock^sh epsilon_shadow_clock",
            "dimensionless_or_fractional_frequency",
            "C_clock^sh epsilon_shadow_clock <= clock_redshift_or_LLI_bound",
            "MISSING_CLOCK_BOUND_SOURCE",
            "clock source row not yet acquired in current local corpus",
            "nonclaim source-acquisition row",
        ),
        (
            "SBB3769_5_preferred_frame_bound",
            "C_PF^sh epsilon_preferred_frame",
            "dimensionless",
            "C_PF^sh epsilon_preferred_frame <= preferred_frame_bound",
            "MISSING_PREFERRED_FRAME_BOUND_SOURCE",
            "preferred-frame source row not yet acquired in current local corpus",
            "nonclaim source-acquisition row",
        ),
        (
            "SBB3769_6_Newton_frame_calibration",
            "delta ln mu_obs|_frame",
            "dimensionless",
            "delta ln mu_obs|_frame <= C_source^sh epsilon_shadow_source + C_orbit^sh epsilon_shadow_source",
            "MISSING_NEWTON_FRAME_PROJECTION",
            "requires source/orbit frame projection coefficient",
            "nonclaim Newtonian calibration interface",
        ),
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
    theorem_emitted = any(row["theorem_id"] == "SFT3769_2_gauge_zero" for row in grouped["theorem"])
    zero_signed = any(row["attempt_id"] == "SZA3769_7_verdict" and row["passes_clause"] is True for row in grouped["zero_attempt"])
    ppn_budgets = any(row["budget_id"] == "SBB3769_1_gamma_shadow" and str(row["bound_value"]) == "2.3e-05" for row in grouped["bound_budget"])
    missing_clock_pf = any(row["bound_value"] == "MISSING_CLOCK_BOUND_SOURCE" for row in grouped["bound_budget"]) and any(row["bound_value"] == "MISSING_PREFERRED_FRAME_BOUND_SOURCE" for row in grouped["bound_budget"])
    rows = [
        ("CG3769_0_sources", "all 3769 source paths exist", sources_exist, "path hygiene"),
        ("CG3769_1_gauge_zero_theorem", "shadow-frame gauge-zero theorem emitted", theorem_emitted, "pure diffeo/Lorentz/q_obs gauge is harmless"),
        ("CG3769_2_current_zero_signed", "current branch signs L_leak_shadow_g=0", zero_signed, "blocked by unsigned sector frame factorization"),
        ("CG3769_3_residual_coefficients", "shadow frame residual coefficient rows emitted", len(grouped["coefficients"]) >= 8, "sector frame residues are named"),
        ("CG3769_4_ppn_bound_budget", "PPN gamma/beta bound envelopes emitted", ppn_budgets, "Cassini/PPN envelopes are source-backed"),
        ("CG3769_5_clock_preferred_sources", "clock and preferred-frame bound sources acquired", not missing_clock_pf, "missing clock/preferred-frame source rows retained as blockers"),
        ("CG3769_6_single_metric_claim", "single observed metric/frame claim allowed", False, "blocked until zero proof or all residual projections are sourced and below bounds"),
        ("CG3769_7_local_gr_claim", "local GR claim allowed", False, "blocked by remaining L_leak/source/readout/range gates"),
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
        (
            "DEC3769_0",
            "The one-metric problem is now a non-gauge shadow frame coefficient problem, not a slogan.",
            "work with h_s^perp and epsilon_shadow_s, not generic frame words",
        ),
        (
            "DEC3769_1",
            "Pure diffeomorphism, local Lorentz rotation, and q_obs-kernel gauge directions are harmless; only h_s^perp is physical.",
            "try to prove each sector has h_s^perp=0 before using bounds",
        ),
        (
            "DEC3769_2",
            "PPN gamma/beta envelopes are available, but clock and preferred-frame numerical sources are not yet acquired in this local branch.",
            "source clock/preferred-frame bounds before any claim involving those rows",
        ),
        (
            "DEC3769_3",
            "The next most dangerous action leak is source action descent, because even one metric does not guarantee one total Hilbert source.",
            "attack L_leak_src next",
        ),
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
            "next_id": "NEXT3769_0",
            "target_doc": "3770-Y5-R2FR-source-action-leak-zero-or-WEP-EM-PPN-bound.md",
            "target_script": "scripts/Y5_R2FR_3770_source_action_leak_zero_or_WEP_EM_PPN_bound.py",
            "objective": "prove the source action leak L_leak_src vanishes by descent S_src=Sbar_src(q_obs,psi,A,theta), or emit WEP/EM/PPN source-current residual coefficients for J_A^src",
            "reason": "3769 handles the metric-frame leak; the next local-GR gate is whether the same observed metric also sources one total Hilbert/coframe source",
            "claim_allowed": False,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "status": "SHADOW_FRAME_GAUGE_ZERO_THEOREM_DERIVED_PPN_BOUND_INTERFACE_EMITTED_CLOCK_PREFERRED_SOURCES_MISSING",
            "summary": "3769 derives the exact gauge-zero route for the shadow metric/frame leak: local Lorentz, diffeomorphism, and q_obs-kernel gauge parts do not count as physical frame leakage, while the orthogonal h_s^perp sector residues remain live. PPN gamma/beta envelopes are source-backed; clock and preferred-frame bound sources remain missing and nonclaim.",
            "claim_allowed": False,
        }
    ]


def validation_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks = [
        ("sources_exist", "all 3769 source paths exist", all(Path(str(row["source_path"])).exists() for row in grouped["sources"])),
        ("generated_csvs_parse", "all generated 3769 csvs parse", all(read_csv(path) for path in generated_csvs)),
        ("gauge_zero_theorem", "gauge-zero theorem emitted", any(row["theorem_id"] == "SFT3769_2_gauge_zero" for row in grouped["theorem"])),
        ("shadow_leak_operator", "shadow leak operator emitted", any(row["theorem_id"] == "SFT3769_3_shadow_leak_operator" for row in grouped["theorem"])),
        ("zero_not_claimed", "current branch keeps L_leak_shadow_g zero unsigned", any(row["attempt_id"] == "SZA3769_7_verdict" and row["passes_clause"] is False for row in grouped["zero_attempt"])),
        ("coefficient_rows", "at least eight shadow frame coefficients emitted", len(grouped["coefficients"]) >= 8),
        ("ppn_bounds", "PPN gamma and beta bound envelopes emitted", any(row["budget_id"] == "SBB3769_1_gamma_shadow" and float(row["bound_value"]) == 2.3e-05 for row in grouped["bound_budget"] if str(row["bound_value"]).replace('.', '', 1).replace('e-05', '').replace('-', '').isdigit()) and any(row["budget_id"] == "SBB3769_2_beta_shadow" and float(row["bound_value"]) == 7.8e-05 for row in grouped["bound_budget"] if str(row["bound_value"]).replace('.', '', 1).replace('e-05', '').replace('-', '').isdigit())),
        ("clock_pf_missing_nonclaim", "clock/preferred-frame sources remain explicit blockers", any(row["bound_value"] == "MISSING_CLOCK_BOUND_SOURCE" for row in grouped["bound_budget"]) and any(row["bound_value"] == "MISSING_PREFERRED_FRAME_BOUND_SOURCE" for row in grouped["bound_budget"])),
        ("claim_gates_closed", "single-metric/local-GR claims remain closed", all(row["passed"] is False for row in grouped["claim_gates"] if row["gate_id"] in {"CG3769_2_current_zero_signed", "CG3769_6_single_metric_claim", "CG3769_7_local_gr_claim"})),
        ("next_target", "3770 source action leak target emitted", grouped["next_target"][0]["target_doc"] == "3770-Y5-R2FR-source-action-leak-zero-or-WEP-EM-PPN-bound.md"),
        ("no_formalization_leak", "no 3769 files written to formalization-workbench", not FORMALIZATION.exists() or not list(FORMALIZATION.rglob("*3769*"))),
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
        "# 3769 - Shadow Metric/Frame Leak Zero Or PPN/Clock Bound",
        "",
        "## Status",
        "",
        f"`{grouped['status'][0]['status']}`.",
        "",
        grouped["status"][0]["summary"],
        "",
        "## Result In Plain Terms",
        "",
        "This checkpoint attacks the one-metric gate. A sector frame difference is harmless only if it is local Lorentz, diffeomorphism, or q_obs-kernel gauge. The physical residue is the orthogonal shadow metric `h_s^perp`. If all `h_s^perp` vanish, the metric part of `delta_frame_source` closes. If not, the residual must be bounded by PPN, clock, preferred-frame, and Newtonian calibration tests.",
        "",
        "## Shadow Frame Theorem",
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
        raise SystemExit(f"3769 validation failed: {failures}")
    print("wrote 3769 checkpoint: shadow metric/frame zero theorem and PPN/clock bound interface emitted")


if __name__ == "__main__":
    main()

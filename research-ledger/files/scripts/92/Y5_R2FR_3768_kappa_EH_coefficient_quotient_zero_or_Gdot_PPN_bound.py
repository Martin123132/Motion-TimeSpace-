import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3768"
BRANCH = "MTS_R2FR_Y5_KAPPA_EH_COEFFICIENT_QUOTIENT_ZERO_OR_GDOT_PPN_BOUND_3768"
PCW = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work"
)
RESIDUALS = PCW / "source-intake" / "mts_residuals"
FORMALIZATION = PCW.parent / "formalization-workbench"
DOC_PATH = PCW / "3768-Y5-R2FR-kappa-EH-coefficient-quotient-zero-or-Gdot-PPN-bound.md"


OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3768_SOURCE_REGISTER.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_3768_KAPPA_EH_COEFFICIENT_THEOREM.csv",
    "zero_attempt": RESIDUALS / "P8_Y5_R2FR_3768_KAPPA_ZERO_PROOF_ATTEMPT.csv",
    "coefficients": RESIDUALS / "P8_Y5_R2FR_3768_KAPPA_RESIDUAL_COEFFICIENTS.csv",
    "bound_budget": RESIDUALS / "P8_Y5_R2FR_3768_KAPPA_BOUND_BUDGET.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_3768_CLAIM_GATES.csv",
    "decision_rows": RESIDUALS / "P8_Y5_R2FR_3768_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3768_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3768_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3768_VALIDATION.csv",
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
        "SRC3768_0_3767_doc": PCW / "3767-Y5-R2FR-parent-action-pullback-decomposition-or-Lleak-first-bound.md",
        "SRC3768_1_3767_operator_basis": RESIDUALS / "P8_Y5_R2FR_3767_LLEAK_OPERATOR_BASIS.csv",
        "SRC3768_2_3767_bound_interface": RESIDUALS / "P8_Y5_R2FR_3767_LLEAK_BOUND_INTERFACE.csv",
        "SRC3768_3_3758_kappa_flux": RESIDUALS / "P8_Y5_R2FR_3758_KAPPA_QUOTIENT_FLUX_LAW.csv",
        "SRC3768_4_3758_gdot": RESIDUALS / "P8_Y5_R2FR_3758_GDOT_BOUND_EVALUATION.csv",
        "SRC3768_5_3761_ppn": RESIDUALS / "P8_Y5_R2FR_3761_GAMMA_BETA_BOUND_EVALUATION.csv",
        "SRC3768_6_3762_claim_matrix": RESIDUALS / "P8_Y5_R2FR_3762_LOCAL_GR_CLAIM_MATRIX.csv",
        "SRC3768_7_3763_action_ansatz": RESIDUALS / "P8_Y5_R2FR_3763_LOCAL_PARENT_ACTION_ANSATZ.csv",
        "SRC3768_8_3765_qobs_candidate": RESIDUALS / "P8_Y5_R2FR_3765_QOBS_CANDIDATE_MAP.csv",
        "SRC3768_9_3766_frame_bound": RESIDUALS / "P8_Y5_R2FR_3766_FIRST_FRAME_RESIDUAL_BOUND.csv",
    }


def source_register(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "source_id": source_id,
            "source_path": str(path),
            "source_exists": path.exists(),
            "role": "3768 kappa/EH coefficient zero theorem and bound input",
        }
        for source_id, path in source_paths().items()
    ]


def find_row(path: Path, key: str, value: str) -> dict[str, str]:
    for row in read_csv(path):
        if row.get(key) == value:
            return row
    raise KeyError(f"missing row {key}={value} in {path}")


def numeric_inputs() -> dict[str, float]:
    gdot_row = find_row(source_paths()["SRC3768_4_3758_gdot"], "evaluation_id", "GB3758_2_max_allowed_residual")
    gamma_row = find_row(source_paths()["SRC3768_5_3761_ppn"], "evaluation_id", "PGB3761_0_gamma_conditional_zero")
    beta_row = find_row(source_paths()["SRC3768_5_3761_ppn"], "evaluation_id", "PGB3761_1_beta_conditional_zero")
    return {
        "gdot_bound_yr": float(gdot_row["bound_value"]),
        "gamma_bound": float(gamma_row["bound_value"]),
        "beta_bound": float(beta_row["bound_value"]),
    }


def theorem_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "KET3768_0_EH_coefficient_variation",
            "Let L_EH^kappa := (1/(2 kappa_*)) sqrt(-g_eff) R[g_eff]. For E_A in ker(Dq_obs) and Lie_EA g_eff=0, the vertical EH-coefficient variation is Lie_EA L_EH^kappa = -(Lie_EA ln kappa_*) L_EH^kappa.",
            "Lie_EA(1/kappa_*)=-(Lie_EA ln kappa_*)/kappa_* and the metric part is handled by the separate shadow-frame leak.",
            "This identifies the precise coefficient of L_leak_kappa.",
            "EXACT_VERTICAL_VARIATION_IDENTITY",
        ),
        (
            "KET3768_1_quotient_zero",
            "If kappa_*=kappa_bar(q_obs(Phi)) or kappa_* is a global superselected constant, then Lie_EA kappa_*=0 for every E_A in ker(Dq_obs).",
            "Lie_EA kappa_bar(q_obs)=D kappa_bar[Dq_obs(E_A)]=0; superselection gives Lie_EA kappa_*=0 by definition.",
            "This proves L_leak_kappa=0 without tuning.",
            "EXACT_CONDITIONAL_ZERO_THEOREM",
        ),
        (
            "KET3768_2_action_leak_identity",
            "If the quotient-zero condition fails, define beta_kappa,A := Lie_EA ln kappa_* and L_leak_kappa = - beta_kappa,A zeta^A L_EH^kappa + O(zeta^2).",
            "This is the first-order fibre expansion of the EH coefficient leak from 3767.",
            "The missing coupling becomes a coefficient to prove zero or bound.",
            "EXACT_FIRST_ORDER_RESIDUAL_DEFINITION",
        ),
        (
            "KET3768_3_Gdot_bridge",
            "The local measured coupling drift satisfies d_t ln G_eff = d_t ln kappa_* + d_t ln C_G - d_t ln C_M + d_t ln Z_Poisson + d_t ln Z_frame.",
            "Imported from 3758, with charge-flux and calibration residuals kept separate.",
            "This turns beta_kappa,A dot zeta^A into a Gdot-bounded rate contribution.",
            "EXACT_CALIBRATION_IDENTITY",
        ),
        (
            "KET3768_4_no_cancellation_rate_bound",
            "|beta_kappa,A dot zeta^A| + |R_G| + |R_M| + |d_t ln Z_Poisson| + |d_t ln Z_frame| <= 9.6e-15 yr^-1.",
            "No cancellation credit between kappa, charge flux, Poisson, and frame calibration residuals.",
            "This is the strict local-rate bound branch when kappa_* is not parent-zeroed.",
            "NUMERIC_RATE_REQUIREMENT_DERIVED_FROM_3758",
        ),
        (
            "KET3768_5_PPN_amplitude_bound",
            "A static local amplitude epsilon_kappa := sup |beta_kappa,A zeta^A| is constrained by PPN only after projection coefficients are known: C_gamma^k epsilon_kappa <= 2.3e-5 and C_beta^k epsilon_kappa <= 7.8e-5.",
            "The PPN effect of an EH coefficient leak is not claimed universal without C_gamma^k,C_beta^k.",
            "This gives a source-ready PPN envelope without pretending the coefficients are one by theorem.",
            "PPN_BOUND_INTERFACE",
        ),
        (
            "KET3768_6_Newton_calibration_meaning",
            "In the Newtonian limit, a kappa coefficient leak is a local GM/G_eff calibration leak unless C_G,C_M,Z_Poisson,Z_frame absorb it through signed quotient identities.",
            "delta ln G_eff receives delta ln kappa_* plus already named charge/calibration terms.",
            "This is the Newtonian mechanics bridge: kappa_* cannot drift or be species/frame-dependent without appearing in calibrated source coupling.",
            "NEWTONIAN_CALIBRATION_INTERFACE",
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
            "KZA3768_0_EH_coefficient_identified",
            "L_leak_kappa coefficient is beta_kappa,A=Lie_EA ln kappa_*",
            "3767 operator basis and KET3768_0 identify the leak",
            True,
            "the residual target is precise",
        ),
        (
            "KZA3768_1_qobs_candidate_exists",
            "q_obs candidate and vertical directions exist",
            "3765/3766 provide q_obs_candidate and local fibre split",
            True,
            "can ask whether kappa_* descends through q_obs",
        ),
        (
            "KZA3768_2_kappa_quotient_owned",
            "kappa_*=kappa_bar(q_obs)",
            "current corpus has kappa quotient law but no parent-owned kappa_bar(q_obs) signature",
            False,
            "blocks L_leak_kappa=0 by quotient descent",
        ),
        (
            "KZA3768_3_kappa_superselected",
            "kappa_* is a global superselected constant of the parent branch",
            "3758 names the route but marks it not parent-signed",
            False,
            "blocks L_leak_kappa=0 by superselection",
        ),
        (
            "KZA3768_4_no_local_kappa_field",
            "no propagating/local kappa field or representative-dependent normalization remains",
            "no parent kinetic/constraint proof for kappa_* found",
            False,
            "keeps beta_kappa,A live",
        ),
        (
            "KZA3768_5_rate_bound_available",
            "Gdot envelope for beta_kappa,A dot zeta^A exists",
            "3758 provides 9.6e-15 yr^-1 residual budget",
            True,
            "can bound the rate combination nonclaim",
        ),
        (
            "KZA3768_6_amplitude_bound_available",
            "PPN gamma/beta envelopes for epsilon_kappa exist after projection coefficients",
            "3761 provides 2.3e-5 and 7.8e-5 bounds",
            True,
            "can bound the static amplitude combination nonclaim",
        ),
        (
            "KZA3768_7_verdict",
            "L_leak_kappa=0 for current MTS local branch",
            "zero routes are exact but unsigned; bound routes are emitted",
            False,
            "do not claim local GR/Newton calibration closure yet",
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
            "KRC3768_0_beta_kappa_A",
            "beta_kappa,A",
            "Lie_EA ln kappa_*",
            "vertical derivative of the EH/Newton coupling normalization",
            "zero if kappa_* is q_obs-owned or superselected",
            "MISSING_PARENT_DERIVATIVE",
            "dimensionless_per_vertical_coordinate",
        ),
        (
            "KRC3768_1_epsilon_kappa",
            "epsilon_kappa",
            "sup_U |beta_kappa,A zeta^A|",
            "static local EH coefficient amplitude leak",
            "bounded by PPN/Newton calibration once projection coefficients are sourced",
            "MISSING_VERTICAL_AMPLITUDE",
            "dimensionless",
        ),
        (
            "KRC3768_2_dot_epsilon_kappa",
            "dot_epsilon_kappa",
            "sup_U |beta_kappa,A dot zeta^A|",
            "time-rate contribution to Gdot/G from kappa_*",
            "bounded by the 3758 no-cancellation Gdot residual budget",
            "MISSING_VERTICAL_RATE",
            "yr^-1",
        ),
        (
            "KRC3768_3_Lleak_kappa",
            "L_leak_kappa/L_EH",
            "- beta_kappa,A zeta^A + O(zeta^2)",
            "normalized EH action leak",
            "zero iff epsilon_kappa=0",
            "MISSING_PARENT_COEFFICIENT",
            "dimensionless",
        ),
        (
            "KRC3768_4_delta_Geff_kappa",
            "delta ln G_eff|_kappa",
            "delta ln kappa_*",
            "Newtonian calibrated coupling amplitude due to kappa leak",
            "must be absorbed by signed C_G/C_M/Z identities or bounded directly",
            "MISSING_CALIBRATION_PROJECTION",
            "dimensionless",
        ),
        (
            "KRC3768_5_gamma_projection",
            "delta_gamma_kappa",
            "C_gamma^k epsilon_kappa",
            "PPN gamma projection of EH coefficient leak",
            "requires C_gamma^k from weak-field linearization",
            "MISSING_PPN_PROJECTION_COEFFICIENT",
            "dimensionless",
        ),
        (
            "KRC3768_6_beta_projection",
            "delta_beta_kappa",
            "C_beta^k epsilon_kappa",
            "PPN beta projection of EH coefficient leak",
            "requires C_beta^k from second-order weak-field linearization",
            "MISSING_PPN_PROJECTION_COEFFICIENT",
            "dimensionless",
        ),
    ]
    return [
        {
            **base(timestamp),
            "coefficient_id": coefficient_id,
            "symbol": symbol,
            "definition": definition,
            "physical_meaning": physical_meaning,
            "zero_or_bound_condition": zero_or_bound_condition,
            "numeric_value": numeric_value,
            "units": units,
            "claim_allowed": False,
        }
        for coefficient_id, symbol, definition, physical_meaning, zero_or_bound_condition, numeric_value, units in rows
    ]


def bound_budget_rows(timestamp: str, values: dict[str, float]) -> list[dict[str, object]]:
    gamma_unit_smoke = values["gamma_bound"]
    beta_unit_smoke = values["beta_bound"]
    ppn_unit_min = min(gamma_unit_smoke, beta_unit_smoke)
    rows = [
        (
            "KBB3768_0_Gdot_total",
            "dot_epsilon_kappa plus other rate residuals",
            "yr^-1",
            "|beta_kappa,A dot zeta^A| + |R_G| + |R_M| + |d_t ln Z_Poisson| + |d_t ln Z_frame|",
            values["gdot_bound_yr"],
            "P8_Y5_R2FR_3758_GDOT_BOUND_EVALUATION.csv:GB3758_2_max_allowed_residual",
            "strict no-cancellation total rate budget",
            False,
        ),
        (
            "KBB3768_1_kappa_rate_if_others_zero",
            "dot_epsilon_kappa",
            "yr^-1",
            "|beta_kappa,A dot zeta^A|",
            values["gdot_bound_yr"],
            "derived from KBB3768_0 by setting R_G,R_M,Z_Poisson,Z_frame to zero",
            "conditional upper budget, not a prediction",
            False,
        ),
        (
            "KBB3768_2_gamma_projection",
            "C_gamma^k epsilon_kappa",
            "dimensionless",
            "C_gamma^k epsilon_kappa",
            values["gamma_bound"],
            "P8_Y5_R2FR_3761_GAMMA_BETA_BOUND_EVALUATION.csv:PGB3761_0_gamma_conditional_zero",
            "Cassini/Shapiro gamma envelope for the kappa projection",
            False,
        ),
        (
            "KBB3768_3_beta_projection",
            "C_beta^k epsilon_kappa",
            "dimensionless",
            "C_beta^k epsilon_kappa",
            values["beta_bound"],
            "P8_Y5_R2FR_3761_GAMMA_BETA_BOUND_EVALUATION.csv:PGB3761_1_beta_conditional_zero",
            "PPN beta envelope for the kappa projection",
            False,
        ),
        (
            "KBB3768_4_unit_projection_smoke",
            "epsilon_kappa if C_gamma^k=C_beta^k=1",
            "dimensionless",
            "epsilon_kappa <= min(gamma_bound,beta_bound)",
            ppn_unit_min,
            "smoke-only unit projection from 3761 bounds",
            "use only as dry-run scale until C_gamma^k,C_beta^k are derived",
            False,
        ),
        (
            "KBB3768_5_Newton_absolute_calibration",
            "delta ln G_eff|_kappa",
            "dimensionless",
            "delta ln G_eff|_kappa = delta ln kappa_* after C_G/C_M/Z terms are signed silent",
            "MISSING_ABSOLUTE_CALIBRATION_BOUND",
            "requires selected absolute-G/Newtonian calibration source and projection",
            "not yet a numeric row",
            False,
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
            "claim_allowed": claim_allowed,
        }
        for budget_id, target, units, bound_formula, bound_value, source, interpretation, claim_allowed in rows
    ]


def claim_gate_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    sources_exist = all(Path(str(row["source_path"])).exists() for row in grouped["sources"])
    theorem_emitted = any(row["theorem_id"] == "KET3768_1_quotient_zero" for row in grouped["theorem"])
    zero_signed = any(row["attempt_id"] == "KZA3768_7_verdict" and row["passes_clause"] is True for row in grouped["zero_attempt"])
    budgets_emitted = len(grouped["bound_budget"]) >= 6
    numeric_rate_budget = any(str(row["bound_value"]) == "9.6e-15" for row in grouped["bound_budget"])
    rows = [
        ("CG3768_0_sources", "all 3768 source paths exist", sources_exist, "path hygiene"),
        ("CG3768_1_zero_theorem", "kappa quotient/superselection zero theorem emitted", theorem_emitted, "exact conditional theorem exists"),
        ("CG3768_2_current_zero_signed", "current branch signs L_leak_kappa=0", zero_signed, "blocked by unsigned kappa q_obs ownership/superselection"),
        ("CG3768_3_residual_coefficients", "kappa residual coefficient rows emitted", len(grouped["coefficients"]) >= 7, "beta_kappa,A is explicit"),
        ("CG3768_4_numeric_budgets", "Gdot/PPN numeric envelopes emitted", budgets_emitted and numeric_rate_budget, "rate and PPN envelopes are source-backed"),
        ("CG3768_5_Newton_GR_calibration_claim", "Newton/GR calibrated kappa closure claim allowed", False, "blocked until beta_kappa,A is zero or bounded with all projection coefficients"),
        ("CG3768_6_local_gr_claim", "local GR claim allowed", False, "blocked by remaining L_leak and q_obs/source/frame gates"),
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
            "DEC3768_0",
            "The EH/Newton coupling leak is now exactly beta_kappa,A=Lie_EA ln kappa_*.",
            "do not discuss kappa drift vaguely; prove beta_kappa,A=0 or fill its rate/amplitude rows",
        ),
        (
            "DEC3768_1",
            "The clean zero route is kappa_* as a q_obs-owned/superselected constant.",
            "search the parent action/current-chain branch for a real superselection or quotient-ownership proof",
        ),
        (
            "DEC3768_2",
            "The strict bound route is already numerically anchored for rate and PPN envelopes but not projection-complete.",
            "derive C_gamma^k,C_beta^k or keep PPN kappa rows nonclaim",
        ),
        (
            "DEC3768_3",
            "After kappa, the next largest local-GR risk is the shadow metric/frame leak.",
            "attack L_leak_shadow_g before claiming one observed metric",
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
            "next_id": "NEXT3768_0",
            "target_doc": "3769-Y5-R2FR-shadow-metric-frame-leak-zero-or-PPN-clock-bound.md",
            "target_script": "scripts/Y5_R2FR_3769_shadow_metric_frame_leak_zero_or_PPN_clock_bound.py",
            "objective": "prove the shadow metric/frame leak L_leak_shadow_g vanishes modulo diffeomorphism, local Lorentz, and q_obs gauge, or emit PPN/clock/preferred-frame bound coefficients for the residual metric-frame channel",
            "reason": "3768 isolates kappa; the next action-leak operator controls whether matter, light, clocks, and sources really share one observed metric",
            "claim_allowed": False,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "status": "KAPPA_EH_ZERO_THEOREM_DERIVED_BETA_KAPPA_BOUND_BUDGET_EMITTED_NOT_PARENT_SIGNED",
            "summary": "3768 derives the exact EH coefficient leak L_leak_kappa = - beta_kappa,A zeta^A L_EH with beta_kappa,A=Lie_EA ln kappa_*. If kappa_* is q_obs-owned or superselected, the leak vanishes. The current corpus does not sign that condition, so beta_kappa remains live with source-backed Gdot and PPN bound envelopes.",
            "claim_allowed": False,
        }
    ]


def validation_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks = [
        ("sources_exist", "all 3768 source paths exist", all(Path(str(row["source_path"])).exists() for row in grouped["sources"])),
        ("generated_csvs_parse", "all generated 3768 csvs parse", all(read_csv(path) for path in generated_csvs)),
        ("coefficient_identity", "beta_kappa coefficient identity emitted", any(row["theorem_id"] == "KET3768_2_action_leak_identity" for row in grouped["theorem"])),
        ("zero_not_claimed", "current branch keeps L_leak_kappa zero unsigned", any(row["attempt_id"] == "KZA3768_7_verdict" and row["passes_clause"] is False for row in grouped["zero_attempt"])),
        ("coefficient_rows", "at least seven kappa coefficient rows emitted", len(grouped["coefficients"]) >= 7),
        ("gdot_bound", "Gdot numeric rate budget is present", any(row["budget_id"] == "KBB3768_0_Gdot_total" and float(row["bound_value"]) == 9.6e-15 for row in grouped["bound_budget"] if str(row["bound_value"]) != "MISSING_ABSOLUTE_CALIBRATION_BOUND")),
        ("ppn_bounds", "PPN gamma and beta numeric budgets are present", any(row["budget_id"] == "KBB3768_2_gamma_projection" and float(row["bound_value"]) == 2.3e-05 for row in grouped["bound_budget"]) and any(row["budget_id"] == "KBB3768_3_beta_projection" and float(row["bound_value"]) == 7.8e-05 for row in grouped["bound_budget"])),
        ("claim_gates_closed", "Newton/GR and local-GR claims remain closed", all(row["passed"] is False for row in grouped["claim_gates"] if row["gate_id"] in {"CG3768_2_current_zero_signed", "CG3768_5_Newton_GR_calibration_claim", "CG3768_6_local_gr_claim"})),
        ("next_target", "3769 shadow metric/frame target emitted", grouped["next_target"][0]["target_doc"] == "3769-Y5-R2FR-shadow-metric-frame-leak-zero-or-PPN-clock-bound.md"),
        ("no_formalization_leak", "no 3768 files written to formalization-workbench", not FORMALIZATION.exists() or not list(FORMALIZATION.rglob("*3768*"))),
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
        "# 3768 - Kappa/EH Coefficient Quotient Zero Or Gdot/PPN Bound",
        "",
        "## Status",
        "",
        f"`{grouped['status'][0]['status']}`.",
        "",
        grouped["status"][0]["summary"],
        "",
        "## Result In Plain Terms",
        "",
        "`L_leak_kappa` is no longer vague. Its first-order coefficient is `beta_kappa,A = Lie_EA ln kappa_*`. If `kappa_*` is quotient-owned or superselected, this coefficient is zero. If not, its rate projection is bounded by the Gdot budget and its static weak-field projection is bounded by PPN gamma/beta after projection coefficients are supplied.",
        "",
        "## Kappa/EH Coefficient Theorem",
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
        raise SystemExit(f"3768 validation failed: {failures}")
    print("wrote 3768 checkpoint: kappa/EH coefficient zero theorem and Gdot/PPN bound emitted")


if __name__ == "__main__":
    main()

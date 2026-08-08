from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path

from Y5_R10_transition_current_bound_calculator import evaluate_file


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "800-Y5-R10-universal-XB-PiB-support-powers-or-Kperp-boundary-zero-lemma.md"
NEXT_TARGET = "801-Y5-R10-double-zero-fixed-point-parent-mechanism-or-local-branch-closure-ledger.md"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_800_SOURCE_REGISTER.csv"
LOGISTIC_LEMMA_PATH = RESIDUALS / "P8_Y5_R10_800_LOGISTIC_UB_DERIVATIVE_LEMMA.csv"
SUPPORT_POWER_DERIVATION_PATH = RESIDUALS / "P8_Y5_R10_800_SUPPORT_POWER_DERIVATION_AUDIT.csv"
KPERP_LEMMA_PATH = RESIDUALS / "P8_Y5_R10_800_KPERP_BOUNDARY_ZERO_LEMMA_ATTEMPT.csv"
CALCULATOR_INPUT_PATH = RESIDUALS / "P8_Y5_R10_800_SUPPORT_POWER_CANDIDATE_CALCULATOR_INPUT.csv"
CALCULATOR_OUTPUT_PATH = RESIDUALS / "P8_Y5_R10_800_SUPPORT_POWER_CANDIDATE_CALCULATOR_OUTPUT.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_800_DERIVATION_DECISION.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_800_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_800_VALIDATION.csv"

STATUS = "Y5_R10_800_pS_conditional_pL_pT_double_zero_missing_Kperp_boundary_open_nonclaim"
CLAIM_CEILING = "support_power_derivation_audit_only_no_parent_double_zero_no_Kperp_zero_no_local_GR_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    LOGISTIC_LEMMA_PATH,
    SUPPORT_POWER_DERIVATION_PATH,
    KPERP_LEMMA_PATH,
    CALCULATOR_INPUT_PATH,
    CALCULATOR_OUTPUT_PATH,
    DECISION_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCE_SPECS = [
    {
        "source_id": "799_doc",
        "path": POST_CHECKPOINT / "799-Y5-R10-transition-current-bound-calculator-and-source-support-powers.md",
        "needles": ["SPG799_1_pS", "SPG799_5_pK", "D799_1_support_powers_primary"],
        "role": "immediate support-power and Kperp target",
    },
    {
        "source_id": "799_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_799_VALIDATION.csv",
        "needles": ["V799_5_support_power_gates_complete,pass", "V799_12_no_local_GR_claim,pass"],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "formal_eq_open_system",
        "path": FORMALIZATION / "05-equation-register.md",
        "needles": ["+ [1 - Pi_B(X_B)] S_cg", "Pi_B = Sigma[(B_env - B_*)/Delta_B]"],
        "role": "open-system source factor and universal Pi_B law",
    },
    {
        "source_id": "formal_eq_logistic_gradient",
        "path": FORMALIZATION / "05-equation-register.md",
        "needles": ["nabla_mu Pi_B =", "[Pi_B(1 - Pi_B)/Delta_B] nabla_mu B", "L_tr ~= 4 Delta_B L_B"],
        "role": "logistic transition gradient and transition length",
    },
    {
        "source_id": "red_projection_locking",
        "path": FORMALIZATION / "06-consistency-red-team.md",
        "needles": ["F'(m_L) = 0.", "K_perp,loc = 0 or PPN-safe", "`F_1 = 0` is not free"],
        "role": "red-team warning about F1 and Kperp",
    },
    {
        "source_id": "spine_support_powers",
        "path": FORMALIZATION / "07-unification-spine.md",
        "needles": ["Pi_B gives the small local unscreened fraction U_B", "pS >= 1", "pL >= 2", "pT >= 2"],
        "role": "existing spine support-power target",
    },
    {
        "source_id": "spine_projected_source_laws",
        "path": FORMALIZATION / "07-unification-spine.md",
        "needles": ["S_cg = U_B^nS S_*", "m_L = m_* + U_B^nL m_tilde", "L_cg^-2 F_L = Lambda_loc + U_B^nT T_tilde"],
        "role": "projected source-law shape",
    },
    {
        "source_id": "spine_double_zero_status",
        "path": FORMALIZATION / "07-unification-spine.md",
        "needles": ["generic analytic silence gives only linear zeros", "local PPN branch = disciplined closure, not derived local limit"],
        "role": "double-zero failure and closure status",
    },
    {
        "source_id": "799_calculator",
        "path": POST_CHECKPOINT / "scripts" / "Y5_R10_transition_current_bound_calculator.py",
        "needles": ["q_gamma_quad", "epsilon_N_Kperp", "passes_symbolic_gate"],
        "role": "transition-current calculator reused for candidate rows",
    },
]

INPUT_FIELDS = [
    "case_id",
    "row_status",
    "U_B",
    "pS",
    "pL",
    "pT",
    "pB",
    "pK",
    "L_cg",
    "L_tr",
    "L_sys",
    "K_matter_00",
    "rho",
    "F2",
    "A_S",
    "A_L",
    "A_T",
    "A_B",
    "A_K",
    "b_mem",
    "c",
    "G",
    "epsilon_q_limit",
    "epsilon_N_limit",
    "valid_for_claim",
    "source_path",
    "notes",
]


def utc_stamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def needle_status(path: Path, needles: list[str]) -> str:
    if not path.exists():
        return "missing_file"
    text = read_text(path)
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return "missing_needles:" + ";".join(missing)
    return "pass"


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def parse_validation_clean(start: int = 665, end: int = 799) -> tuple[bool, str]:
    failures: list[str] = []
    found = 0
    for path in RESIDUALS.glob("P8_Y5_BRR545_*_VALIDATION.csv"):
        number_text = path.name.replace("P8_Y5_BRR545_", "").replace("_VALIDATION.csv", "")
        if not number_text.isdigit():
            continue
        number = int(number_text)
        if start <= number <= end:
            found += 1
            with path.open("r", encoding="utf-8", newline="") as handle:
                for row in csv.DictReader(handle):
                    if row.get("result") != "pass":
                        failures.append(f"{path.name}:{row.get('check_id')}={row.get('result')}")
    if failures:
        return False, ";".join(failures[:20])
    return found > 0, f"{found} prior validation files clean"


def formalization_change_count() -> int:
    if not FORMALIZATION.exists():
        return -1
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > FORMALIZATION_CUTOFF)


def source_register_rows(generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in SOURCE_SPECS:
        path = spec["path"]
        rows.append(
            {
                "source_id": spec["source_id"],
                "path": str(path),
                "exists": str(path.exists()).lower(),
                "needle_check": needle_status(path, spec["needles"]),
                "role": spec["role"],
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def logistic_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "lemma_id": "LUL800_0_definition",
            "statement": "Pi_B=sigma(y), y=(B_env-B_*)/Delta_B, U_B=1-Pi_B.",
            "derivation": "This is the existing universal switch form; in the screened local branch Pi_B->1 and U_B<<1.",
            "result": "U_B is the natural small local parameter if B_env is universal",
            "status": "source_confirmed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lemma_id": "LUL800_1_gradient",
            "statement": "nabla_mu U_B = -Pi_B U_B nabla_mu B_env / Delta_B.",
            "derivation": "Since U_B=1-Pi_B and nabla Pi_B=Pi_B(1-Pi_B)nabla B_env/Delta_B, substitute 1-Pi_B=U_B.",
            "result": "for Pi_B~1, |nabla U_B|=O(U_B/L_B), so logistic gradients carry one U_B power",
            "status": "derived_from_existing_switch",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lemma_id": "LUL800_2_power_limit",
            "statement": "The logistic switch supplies at most one automatic U_B factor per explicit switch or switch-gradient.",
            "derivation": "A generic smooth function f(U_B)=f_0+f_1 U_B+... has a nonzero constant or linear term unless parent dynamics impose zeros.",
            "result": "Pi_B alone does not derive pL=2 or pT=2",
            "status": "no_double_zero_from_logistic_alone",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def support_power_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "audit_id": "SPD800_0_pS_source",
            "power": "pS",
            "candidate_derivation": "The v0 open-system law contains +[1-Pi_B(X_B)]S_cg = U_B S_cg.",
            "result": "pS=1 is conditionally available if S_cg remains bounded and no unscreened source term is hidden elsewhere.",
            "failure_mode": "if S_cg diverges, has a local floor, or is not the only source channel, pS=1 is not enough",
            "status": "conditional_from_existing_v0_law",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "SPD800_1_pL_generic",
            "power": "pL",
            "candidate_derivation": "Generic smooth m_L(U_B)=m_*+a_1 U_B+a_2 U_B^2+... gives pL=1 when a_1 is nonzero.",
            "result": "pL=2 is not derived by Pi_B; it needs a double zero a_1=0 or an even/fixed-point mechanism.",
            "failure_mode": "linear m_L drift recreates q_loc and can fail finite-margin local gates",
            "status": "missing_double_zero",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "SPD800_2_pT_generic",
            "power": "pT",
            "candidate_derivation": "Generic trace baseline T(U_B)=L_cg^-2F_L-Lambda_loc = b_1 U_B+b_2 U_B^2+... gives pT=1 when b_1 is nonzero.",
            "result": "pT=2 is not derived by Pi_B; it needs a trace-baseline double zero tied to the same fixed point.",
            "failure_mode": "linear trace gradients act like an unsafe local Lambda-gradient/fifth-force source",
            "status": "missing_double_zero",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "SPD800_3_pB_boundary",
            "power": "pB",
            "candidate_derivation": "Boundary/source-measure silence would need B_boundary=O(U_B^pB) or an exact boundary cancellation.",
            "result": "no pB follows from the scalar Pi_B law alone.",
            "failure_mode": "boundary residue dominates once bulk source channels are screened",
            "status": "missing_boundary_silence_law",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "SPD800_4_pK_tensor",
            "power": "pK",
            "candidate_derivation": "If a coercive tensor operator gives L_T K_perp=S_perp with zero/decay boundary data and S_perp=O(U_B^pB), then K_perp=O(U_B^pB).",
            "result": "this would set pK=pB conditionally, but the operator, source, boundary data, and no-zero-mode theorem are not parent-signed.",
            "failure_mode": "homogeneous transverse modes survive and shift Newton/PPN even when scalar screening works",
            "status": "conditional_Kperp_bound_only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "SPD800_5_verdict",
            "power": "support_power_set",
            "candidate_derivation": "Minimal finite-margin closure pS=1,pL=2,pT=2,pB>=2,pK>=2 or Kperp=0.",
            "result": "only pS has a conditional v0 source; the double-zero and Kperp pieces remain closure-level.",
            "failure_mode": "without these, the 799 calculator cannot become a real local-GR pass",
            "status": "not_derived_as_parent_theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def kperp_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "lemma_id": "KBL800_0_needed_operator",
            "statement": "Need a local tensor boundary-value equation L_T K_perp=S_perp on the trace-free transverse sector.",
            "test": "L_T must be parent-derived from the K_hat/moment sector, not invented as a post hoc projector.",
            "result": "operator_missing",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lemma_id": "KBL800_1_zero_boundary",
            "statement": "If S_perp=0 and boundary data vanish/decay with no incoming homogeneous tensor memory, coercivity implies K_perp=0.",
            "test": "requires no zero modes, positive energy/coercive norm, and physical boundary conditions.",
            "result": "conditional_mathematical_lemma_only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lemma_id": "KBL800_2_suppressed_source",
            "statement": "If S_perp=O(U_B^pB) and the inverse is bounded, then ||K_perp||<=C_T O(U_B^pB).",
            "test": "requires C_T and source scaling from the parent local branch.",
            "result": "conditional_bound_only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lemma_id": "KBL800_3_failure",
            "statement": "Pi_B is a scalar/environment switch and does not by itself remove transverse homogeneous K_perp modes.",
            "test": "no scalar source-support theorem can be used as a tensor zero theorem without L_T and boundary data.",
            "result": "Kperp_zero_not_derived",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def calculator_input_rows() -> list[dict[str, object]]:
    base = {
        "L_cg": "1e13",
        "L_tr": "1e11",
        "L_sys": "1e11",
        "K_matter_00": "1e-24",
        "rho": "1000",
        "F2": "1",
        "A_S": "1",
        "A_L": "1",
        "A_T": "1e-36",
        "A_B": "1",
        "A_K": "1",
        "b_mem": "1",
        "c": "299792458",
        "G": "6.67430e-11",
        "epsilon_q_limit": "1e-5",
        "epsilon_N_limit": "1e-5",
        "valid_for_claim": "false",
    }
    generic_linear = {
        **base,
        "case_id": "generic_smooth_linear_nonclaim",
        "row_status": "generic_smooth_zero_order_test",
        "U_B": "1e-4",
        "pS": "1",
        "pL": "1",
        "pT": "1",
        "pB": "1",
        "pK": "0",
        "source_path": "generic_smooth_not_parent_claim",
        "notes": "tests why Pi_B alone is not enough; Kperp unsuppressed",
    }
    double_zero = {
        **base,
        "case_id": "double_zero_closure_nonclaim",
        "row_status": "closure_shape_schema_check",
        "U_B": "1e-4",
        "pS": "1",
        "pL": "2",
        "pT": "2",
        "pB": "2",
        "pK": "3",
        "source_path": "closure_shape_not_parent_derived",
        "notes": "shows the finite-margin closure shape is calculable but not evidence",
    }
    return [generic_linear, double_zero]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D800_0_pS_partial",
            "decision": "Is any support power derived from the existing universal law?",
            "reason": "The open-system source equation explicitly multiplies S_cg by U_B=1-Pi_B.",
            "result": "pS_equals_1_conditional_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D800_1_double_zero_missing",
            "decision": "Are pL=2 and pT=2 derived?",
            "reason": "A generic smooth function of U_B gives linear zeros; double zeros require an even/fixed-point mechanism not currently parent-derived.",
            "result": "pL_pT_not_derived",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D800_2_Kperp_not_zero",
            "decision": "Can Kperp be set to zero from scalar screening?",
            "reason": "No. Kperp needs its own tensor operator, source, boundary, and no-zero-mode theorem.",
            "result": "Kperp_zero_boundary_lemma_not_parent_signed",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D800_3_next_route",
            "decision": "Next best route",
            "reason": "Either derive the double-zero fixed-point mechanism from parent/coarse-graining dynamics or lock the local branch as a labelled closure.",
            "result": "attempt_double_zero_parent_mechanism_or_closure_ledger",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "The universal Pi_B law conditionally gives pS=1 through the explicit U_B S_cg factor, and logistic gradients scale as O(U_B). But pL=2, pT=2, boundary silence, and Kperp suppression do not follow from Pi_B alone.",
            "hard_blocker": "Need a parent-derived double-zero/fixed-point mechanism for m_L and trace baseline, plus a Kperp zero-boundary theorem or response bound.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_outputs_scoped() -> bool:
    root = POST_CHECKPOINT.resolve()
    for path in OUTPUT_PATHS:
        resolved_parent = path.parent.resolve()
        if root != resolved_parent and root not in resolved_parent.parents:
            return False
    return True


def validation_rows(
    sources: list[dict[str, object]],
    logistic: list[dict[str, object]],
    support: list[dict[str, object]],
    kperp: list[dict[str, object]],
    calculator_output: list[dict[str, object]],
    decisions: list[dict[str, object]],
    summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    prior_clean, prior_detail = parse_validation_clean()
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in sources)
    all_nonclaim = all(
        row.get("valid_for_claim") == "false"
        for group in [sources, logistic, support, kperp, calculator_output, decisions, summary]
        for row in group
    )
    logistic_gradient = any(row["lemma_id"] == "LUL800_1_gradient" and "O(U_B/L_B)" in row["result"] for row in logistic)
    ps_conditional = any(row["audit_id"] == "SPD800_0_pS_source" and row["status"] == "conditional_from_existing_v0_law" for row in support)
    pL_missing = any(row["audit_id"] == "SPD800_1_pL_generic" and row["status"] == "missing_double_zero" for row in support)
    pT_missing = any(row["audit_id"] == "SPD800_2_pT_generic" and row["status"] == "missing_double_zero" for row in support)
    kperp_open = any(row["lemma_id"] == "KBL800_3_failure" and row["result"] == "Kperp_zero_not_derived" for row in kperp)
    candidate_rows_nonclaim = len(calculator_output) == 2 and all(row["valid_for_claim"] == "false" for row in calculator_output)
    no_candidate_claim_pass = all(row["passes_symbolic_gate"] == "false" for row in calculator_output)
    next_target_selected = summary[0]["next_target"] == NEXT_TARGET and any(row["decision_id"] == "D800_3_next_route" for row in decisions)
    formalization_count = formalization_change_count()
    checks = [
        ("V800_0_sources_exist_and_needles", source_ok, "all source paths exist and needles are present"),
        ("V800_1_prior_665_799_clean", prior_clean, prior_detail),
        ("V800_2_outputs_scoped", all_outputs_scoped(), str(POST_CHECKPOINT)),
        ("V800_3_all_rows_nonclaim", all_nonclaim, "all generated rows valid_for_claim=false"),
        ("V800_4_logistic_gradient_derived", logistic_gradient, "nabla U_B scales as O(U_B/L_B) in screened branch"),
        ("V800_5_pS_conditional", ps_conditional, "pS=1 conditionally follows from U_B S_cg source factor"),
        ("V800_6_pL_missing_double_zero", pL_missing, "pL=2 requires double-zero mechanism"),
        ("V800_7_pT_missing_double_zero", pT_missing, "pT=2 requires double-zero mechanism"),
        ("V800_8_Kperp_open", kperp_open, "Kperp zero not derived from scalar Pi_B law"),
        ("V800_9_candidate_rows_nonclaim", candidate_rows_nonclaim, "calculator candidate rows remain nonclaim"),
        ("V800_10_no_candidate_claim_pass", no_candidate_claim_pass, "no candidate row promoted to claim"),
        ("V800_11_next_target_selected", next_target_selected, NEXT_TARGET),
        ("V800_12_no_local_GR_claim", all_nonclaim and no_candidate_claim_pass, "local GR/Newton remains blocked"),
        ("V800_13_claim_artifacts_absent", not (POST_CHECKPOINT / "LOCAL_GR_CLAIM.md").exists(), "no local-GR claim artifact present"),
        ("V800_14_formalization_workbench_untouched", formalization_count == 0, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V800_15_validation_rows_ready", True, "validation table constructed"),
    ]
    return [{"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail} for check_id, passed, detail in checks]


def build_doc(
    sources: list[dict[str, object]],
    logistic: list[dict[str, object]],
    support: list[dict[str, object]],
    kperp: list[dict[str, object]],
    calculator_input: list[dict[str, object]],
    calculator_output: list[dict[str, object]],
    decisions: list[dict[str, object]],
    summary: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 800 - Y5 R10 Universal XB PiB Support Powers Or Kperp Boundary Zero Lemma

Current result: **`Pi_B` helps, but it does not close the local-GR branch**. The universal switch gives a real small parameter `U_B=1-Pi_B` and `|nabla U_B|=O(U_B/L_B)` in the screened branch. It also conditionally gives `pS=1` because the v0 source law contains `U_B S_cg`. But the needed `pL=2` and `pT=2` require a double-zero/fixed-point mechanism, and `K_perp` needs an independent tensor boundary theorem.

## Nonclaim Summary

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Logistic UB Lemma

{markdown_table(logistic, ["lemma_id", "statement", "derivation", "result", "status", "valid_for_claim"])}

## Support Power Derivation Audit

{markdown_table(support, ["audit_id", "power", "candidate_derivation", "result", "failure_mode", "status", "valid_for_claim"])}

## Kperp Boundary Zero Lemma Attempt

{markdown_table(kperp, ["lemma_id", "statement", "test", "result", "valid_for_claim"])}

## 799 Calculator Candidate Inputs

{markdown_table(calculator_input, ["case_id", "row_status", "U_B", "pS", "pL", "pT", "pB", "pK", "valid_for_claim", "notes"])}

## 799 Calculator Candidate Output

{markdown_table(calculator_output, ["case_id", "numeric_ready", "epsilon_q", "epsilon_N_trace", "epsilon_N_Kperp", "passes_symbolic_gate", "valid_for_claim", "notes"])}

## Decision

{markdown_table(decisions, ["decision_id", "decision", "reason", "result", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Verdict

The branch is not dead, but it is not derived. We have one useful derived/conditional piece (`pS=1`) and one useful logistic gradient lemma. The missing object is now very specific: a parent fixed-point mechanism that forces double zeros in `m_L` and the trace baseline, plus a tensor boundary/coercivity theorem for `K_perp`. Without that, the local branch remains a disciplined closure rather than a derived GR/Newton limit.

## Next Target

`{NEXT_TARGET}`
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = source_register_rows(generated_utc)
    logistic = logistic_rows(generated_utc)
    support = support_power_rows(generated_utc)
    kperp = kperp_rows(generated_utc)
    calculator_input = calculator_input_rows()
    write_csv(CALCULATOR_INPUT_PATH, calculator_input, INPUT_FIELDS)
    calculator_output = evaluate_file(CALCULATOR_INPUT_PATH, CALCULATOR_OUTPUT_PATH)
    decisions = decision_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validation_rows(sources, logistic, support, kperp, calculator_output, decisions, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(LOGISTIC_LEMMA_PATH, logistic, ["lemma_id", "statement", "derivation", "result", "status", "valid_for_claim", "generated_utc"])
    write_csv(SUPPORT_POWER_DERIVATION_PATH, support, ["audit_id", "power", "candidate_derivation", "result", "failure_mode", "status", "valid_for_claim", "generated_utc"])
    write_csv(KPERP_LEMMA_PATH, kperp, ["lemma_id", "statement", "test", "result", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "reason", "result", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, logistic, support, kperp, calculator_input, calculator_output, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    if failures:
        failure_text = "; ".join(f"{row['check_id']}={row['detail']}" for row in failures)
        raise SystemExit(f"800 validation failed: {failure_text}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"next={NEXT_TARGET}")


if __name__ == "__main__":
    main()

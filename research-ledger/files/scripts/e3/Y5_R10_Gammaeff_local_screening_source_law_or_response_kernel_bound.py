from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "798-Y5-R10-Gammaeff-local-screening-source-law-or-response-kernel-bound.md"
NEXT_TARGET = "799-Y5-R10-transition-current-bound-calculator-and-source-support-powers.md"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_798_SOURCE_REGISTER.csv"
GAMMA_EXPANSION_PATH = RESIDUALS / "P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv"
SCREENING_ATTEMPT_PATH = RESIDUALS / "P8_Y5_R10_798_SCREENING_THEOREM_ATTEMPT.csv"
TRANSITION_CONTRACT_PATH = RESIDUALS / "P8_Y5_R10_798_TRANSITION_CURRENT_BOUND_CONTRACT.csv"
RESPONSE_KERNEL_PATH = RESIDUALS / "P8_Y5_R10_798_RESPONSE_KERNEL_FALLBACK.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_798_DERIVATION_DECISION.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_798_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_798_VALIDATION.csv"

STATUS = "Y5_R10_798_Gammaeff_source_expansion_conditional_screening_theorem_transition_current_open_nonclaim"
CLAIM_CEILING = "conditional_Gammaeff_screening_source_law_only_no_transition_bound_no_response_kernel_no_local_GR_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    GAMMA_EXPANSION_PATH,
    SCREENING_ATTEMPT_PATH,
    TRANSITION_CONTRACT_PATH,
    RESPONSE_KERNEL_PATH,
    DECISION_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCE_SPECS = [
    {
        "source_id": "797_doc",
        "path": POST_CHECKPOINT / "797-Y5-R10-parent-relaxation-source-action-contract-and-Gammaeff-screening-gate.md",
        "needles": ["RTL797_4_necessary_screening_condition", "D797_1_screening_required"],
        "role": "immediate Gamma_eff screening target",
    },
    {
        "source_id": "797_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_797_VALIDATION.csv",
        "needles": ["V797_7_screening_required,pass", "V797_12_no_local_GR_claim,pass"],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "formal_eq_Gamma",
        "path": FORMALIZATION / "05-equation-register.md",
        "needles": ["Gamma_eff = L_cg^-2 F(m)", "Local memory equilibrium screening", "Pi_B = Sigma[(B_env - B_*)/Delta_B]"],
        "role": "Gamma_eff memory screening equations",
    },
    {
        "source_id": "formal_eq_transition",
        "path": FORMALIZATION / "05-equation-register.md",
        "needles": ["transition-current gate is not checked", "gradients of `Pi_B`, `mu_B`, and `m_L`"],
        "role": "transition-current warning in equation register",
    },
    {
        "source_id": "red_transition",
        "path": FORMALIZATION / "06-consistency-red-team.md",
        "needles": ["L_cg^-2 |F'(m)| M_tr/L_tr", "F'(m_L) = 0 is not enough.", "No galaxy or cosmology evidence can rescue an unsafe q_loc^nu."],
        "role": "red-team transition-current and F1 warning",
    },
    {
        "source_id": "spine_source_laws",
        "path": FORMALIZATION / "07-unification-spine.md",
        "needles": ["F_1 = 0 is forced by first-order q_loc safety", "derive projected source laws:", "derive the support powers `pS`, `pL`, and `pT`"],
        "role": "spine source-law and support-power target",
    },
    {
        "source_id": "797_gamma_gate",
        "path": RESIDUALS / "P8_Y5_R10_797_GAMMAEFF_SCREENING_GATE.csv",
        "needles": ["GSG797_1_environmental_mass", "GSG797_4_response_kernel"],
        "role": "machine-readable Gamma_eff screening gate",
    },
    {
        "source_id": "797_tradeoff",
        "path": RESIDUALS / "P8_Y5_R10_797_RELAXATION_TRADEOFF_LEMMA.csv",
        "needles": ["RTL797_2_residual_tradeoff", "RTL797_4_necessary_screening_condition"],
        "role": "machine-readable relaxation tradeoff lemma",
    },
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


def parse_validation_clean(start: int = 665, end: int = 797) -> tuple[bool, str]:
    if not RESIDUALS.exists():
        return False, "residual directory missing"
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


def gamma_expansion_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "expansion_id": "GSE798_0_definition",
            "statement": "Gamma_eff = L_cg^-2 F(m).",
            "derivation_or_bound": "This is the memory-source object whose local projected gradient is s^nu=P_loc nabla^nu Gamma_eff.",
            "implication": "local GR needs this source vector to vanish, be bounded, or be observationally invisible",
            "status": "source_definition",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "expansion_id": "GSE798_1_gradient_expansion",
            "statement": "nabla_nu Gamma_eff = L_cg^-2 F'(m)nabla_nu m - 2 L_cg^-3 F(m)nabla_nu L_cg.",
            "derivation_or_bound": "ordinary product rule; if L_cg is fixed locally the second term drops, otherwise trace-baseline gradients re-enter q_loc.",
            "implication": "F'(m_L)=0 alone is insufficient when L_cg or m_L drifts",
            "status": "derived_identity",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "expansion_id": "GSE798_2_local_locked_expansion",
            "statement": "Let m=m_*+delta m and choose F'(m_*)=0. Then nabla Gamma_eff = L_*^-2 F_2 delta m nabla delta m - 2 L_*^-3 F_* nabla delta L + baseline-drift terms.",
            "derivation_or_bound": "Taylor expand F(m)=F_*+1/2 F_2 delta m^2+... around the locked local stationary point.",
            "implication": "the m-channel becomes quadratic only if the parent law locks the local state to a stationary point of F",
            "status": "conditional_quadratic_suppression",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "expansion_id": "GSE798_3_static_relaxation_source",
            "statement": "A v0 static local memory law has schematically (-D_m Delta + M_scr^2)delta m = U_B S_cg + drift(m_L,L_cg,Pi_B,mu_B) + boundary.",
            "derivation_or_bound": "Here U_B=1-Pi_B and M_scr^2~Pi_B/(D_m tau_L) or mu_B/D_m in the screened branch.",
            "implication": "delta m is small only if the universal local branch has Pi_B~1, large enough M_scr, and source/drift/boundary terms supported by powers of U_B",
            "status": "conditional_effective_law",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "expansion_id": "GSE798_4_screened_source_scaling",
            "statement": "If delta m=O(U_B^pS), nabla delta m=O(U_B^pS/L_tr), nabla m_L=O(U_B^pL/L_tr), and nabla(L_cg^-2 F_L)=O(U_B^pT/L_tr), then s=O(U_B^(2pS), U_B^pL, U_B^pT)/L_tr.",
            "derivation_or_bound": "The quadratic F_2 term gives the 2pS power; baseline and trace-drift terms enter linearly through pL and pT.",
            "implication": "local safety reduces to deriving pS, pL, pT and numerical U_B bounds, not merely saying screening occurs",
            "status": "conditional_scaling_law",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "expansion_id": "GSE798_5_source_law_verdict",
            "statement": "The route can make Gamma_eff gradients parametrically small, but only under unsigned source-support and transition-current assumptions.",
            "derivation_or_bound": "Without parent-derived pS, pL, pT, boundary decay, and K_perp control, the screening theorem is not claimable.",
            "implication": "transition-current calculator/support-power derivation is now the next concrete gate",
            "status": "not_adopted_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def screening_attempt_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "attempt_id": "STA798_0_F_stationary_lock",
            "condition": "parent relaxation locks local m_L to m_* with F'(m_*)=0",
            "why_needed": "removes the linear F_1 grad m contribution to s=P_loc grad Gamma_eff",
            "status": "conditional_not_parent_derived",
            "missing_input": "derive m_* from R(m;X_B) instead of choosing it",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "STA798_1_fast_local_relaxation",
            "condition": "M_scr L_loc >> 1 or tau_L << local observation/transition timescale",
            "why_needed": "drives delta m small in local tested systems",
            "status": "effective_law_not_action_derived",
            "missing_input": "universal mu_B/tau_L/D_m law from X_B",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "STA798_2_source_support",
            "condition": "U_B S_cg, m_L drift, trace-baseline drift, and boundary terms vanish with powers pS,pL,pT,pB",
            "why_needed": "prevents transition shells and baselines from recreating q_loc after the local plateau",
            "status": "support_powers_missing",
            "missing_input": "derive pS,pL,pT,pB from one universal X_B -> Pi_B law",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "STA798_3_large_scale_survival",
            "condition": "the same Pi_B law permits galaxy/FLRW memory where intended without dataset-specific tuning",
            "why_needed": "otherwise local screening deletes the empirical pillars or becomes a patchwork switch",
            "status": "not_checked_here",
            "missing_input": "joint local-galaxy-cosmology regime map after local safety is sourced",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "STA798_4_theorem_status",
            "condition": "all prior conditions plus PPN/clock/orbital/R10/WEP response bounds",
            "why_needed": "local GR/Newton requires observable safety, not just source algebra",
            "status": "theorem_not_closed",
            "missing_input": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def transition_contract_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "contract_id": "TCB798_0_U_B_definition",
            "quantity": "U_B=1-Pi_B",
            "needed_derivation": "universal local unscreened fraction from X_B/B_env, not dataset choice",
            "bound_form": "U_B(local tests) << 1 with sourced values for lab/Solar/clock/orbital systems",
            "current_status": "missing_numeric_universal_profile",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "TCB798_1_pS_source_support",
            "quantity": "pS",
            "needed_derivation": "S_cg support must scale as O(U_B^pS) in local systems",
            "bound_form": "quadratic Gamma source gives O(U_B^(2pS)); pS and source amplitude must beat q/PPN thresholds",
            "current_status": "missing_support_power",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "TCB798_2_pL_mL_drift",
            "quantity": "pL",
            "needed_derivation": "grad m_L and local stationary point drift must scale as O(U_B^pL/L_tr)",
            "bound_form": "linear drift terms must be at least as suppressed as the q_loc and Newton-source budgets require",
            "current_status": "missing_drift_power",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "TCB798_3_pT_trace_baseline",
            "quantity": "pT",
            "needed_derivation": "grad(L_cg^-2 F_L) and trace-baseline gradients must scale as O(U_B^pT/L_tr)",
            "bound_form": "constant Lambda-like branch is safe only if its gradients are suppressed below local bounds",
            "current_status": "missing_trace_power",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "TCB798_4_transition_width",
            "quantity": "ell_tr/L_cg and L_tr",
            "needed_derivation": "transition width must be parent-fixed and not arbitrarily widened to hide gradients",
            "bound_form": "|s|~L_cg^-2 times transition amplitude divided by L_tr must pass local response gates",
            "current_status": "missing_transition_geometry",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "TCB798_5_Kperp_boundary",
            "quantity": "K_perp and boundary source",
            "needed_derivation": "trace/longitudinal screening must not leave transverse tensor or boundary residue",
            "bound_form": "K_perp=0 theorem or response-vector bound",
            "current_status": "open_from_prior_gates",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def response_kernel_rows(generated_utc: str) -> list[dict[str, object]]:
    arenas = [
        ("RKF798_0_Newton", "Newton/source", "R_N[s,K]=0 or epsilon_N below bound"),
        ("RKF798_1_PPN", "PPN", "R_PPN[s,K]={delta_gamma,delta_beta,alpha_i,xi} below bounds"),
        ("RKF798_2_clock", "clock/redshift", "R_clock[s,K]=0 or below clock limits"),
        ("RKF798_3_orbital", "orbital", "R_orbital[s,K]=0 or below ephemeris/lunar/binary limits"),
        ("RKF798_4_R10", "short-range/R10", "alpha(lambda) map below bound"),
        ("RKF798_5_WEP", "WEP/readout", "eta_AB and matter-frame mismatch zero/bounded"),
    ]
    return [
        {
            "kernel_id": kernel_id,
            "arena": arena,
            "fallback_requirement": requirement,
            "result": "not_available",
            "why_not_claimable": "no sourced response matrix/kernel proof exists for non-small Gamma_eff source",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for kernel_id, arena, requirement in arenas
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D798_0_conditional_screening_only",
            "decision": "Does the Gamma_eff expansion prove local screening?",
            "reason": "It proves the route conditionally: F'(m_*)=0 plus source-support powers can suppress s, but those inputs are not parent-derived.",
            "result": "conditional_not_claimed",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D798_1_transition_current_selected",
            "decision": "Best next target",
            "reason": "The dangerous terms are now U_B support, m_L drift, trace-baseline drift, transition width, and K_perp/boundary residue.",
            "result": "build_transition_current_bound_calculator_and_support_power_gate",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D798_2_response_kernel_fallback_blocked",
            "decision": "Can response-kernel invisibility replace screening?",
            "reason": "No current source gives Newton/PPN/clock/orbital/R10/WEP kernel proof for non-small s.",
            "result": "fallback_retained_but_blocked",
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
            "main_result": "Gamma_eff=L_cg^-2F(m) yields a concrete local source expansion. A stationary-point lock F'(m_*)=0 gives quadratic m-channel suppression, but trace/baseline/transition terms remain linear unless support powers pS,pL,pT,pB are derived.",
            "hard_blocker": "Need universal X_B/Pi_B source-support powers, transition width, boundary/Kperp control, or a sourced response-kernel proof.",
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
    expansion: list[dict[str, object]],
    screening: list[dict[str, object]],
    transition: list[dict[str, object]],
    kernel: list[dict[str, object]],
    decisions: list[dict[str, object]],
    summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    prior_clean, prior_detail = parse_validation_clean()
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in sources)
    all_nonclaim = all(
        row.get("valid_for_claim") == "false"
        for group in [sources, expansion, screening, transition, kernel, decisions, summary]
        for row in group
    )
    gradient_identity = any(row["expansion_id"] == "GSE798_1_gradient_expansion" and "F'(m)nabla_nu m" in row["statement"] and "nabla_nu L_cg" in row["statement"] for row in expansion)
    quadratic_suppression = any(row["expansion_id"] == "GSE798_2_local_locked_expansion" and "F'(m_*)=0" in row["statement"] for row in expansion)
    support_scaling = any(row["expansion_id"] == "GSE798_4_screened_source_scaling" and "pS" in row["statement"] and "pL" in row["statement"] and "pT" in row["statement"] for row in expansion)
    theorem_not_closed = any(row["attempt_id"] == "STA798_4_theorem_status" and row["status"] == "theorem_not_closed" for row in screening)
    transition_complete = {row["contract_id"] for row in transition} == {
        "TCB798_0_U_B_definition",
        "TCB798_1_pS_source_support",
        "TCB798_2_pL_mL_drift",
        "TCB798_3_pT_trace_baseline",
        "TCB798_4_transition_width",
        "TCB798_5_Kperp_boundary",
    }
    kernel_blocked = len(kernel) == 6 and all(row["result"] == "not_available" for row in kernel)
    next_target_selected = summary[0]["next_target"] == NEXT_TARGET and any(row["decision_id"] == "D798_1_transition_current_selected" for row in decisions)
    no_claim = all_nonclaim and any(row["decision_id"] == "D798_0_conditional_screening_only" and row["result"] == "conditional_not_claimed" for row in decisions)
    formalization_count = formalization_change_count()

    checks = [
        ("V798_0_sources_exist_and_needles", source_ok, "all source paths exist and needles are present"),
        ("V798_1_prior_665_797_clean", prior_clean, prior_detail),
        ("V798_2_outputs_scoped", all_outputs_scoped(), str(POST_CHECKPOINT)),
        ("V798_3_all_rows_nonclaim", all_nonclaim, "all generated rows valid_for_claim=false"),
        ("V798_4_gradient_identity_derived", gradient_identity, "Gamma_eff gradient identity recorded"),
        ("V798_5_quadratic_suppression_condition", quadratic_suppression, "F'(m_*)=0 quadratic condition recorded"),
        ("V798_6_support_scaling_law", support_scaling, "pS/pL/pT scaling law recorded"),
        ("V798_7_screening_theorem_not_closed", theorem_not_closed, "screening theorem remains conditional"),
        ("V798_8_transition_contract_complete", transition_complete, "transition support rows complete"),
        ("V798_9_response_kernel_blocked", kernel_blocked, "response-kernel fallback remains unavailable"),
        ("V798_10_next_target_selected", next_target_selected, NEXT_TARGET),
        ("V798_11_no_local_GR_claim", no_claim, "local GR/Newton remains blocked"),
        ("V798_12_claim_artifacts_absent", not (POST_CHECKPOINT / "LOCAL_GR_CLAIM.md").exists(), "no local-GR claim artifact present"),
        ("V798_13_formalization_workbench_untouched", formalization_count == 0, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V798_14_validation_rows_ready", True, "validation table constructed"),
    ]
    return [{"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail} for check_id, passed, detail in checks]


def build_doc(
    sources: list[dict[str, object]],
    expansion: list[dict[str, object]],
    screening: list[dict[str, object]],
    transition: list[dict[str, object]],
    kernel: list[dict[str, object]],
    decisions: list[dict[str, object]],
    summary: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 798 - Y5 R10 Gammaeff Local Screening Source Law Or Response Kernel Bound

Current result: **`Gamma_eff` screening has a conditional derivation path, but not a theorem yet**. Expanding `Gamma_eff=L_cg^-2 F(m)` shows exactly how the local source appears: `grad Gamma_eff` contains an `F'(m) grad m` channel and an `L_cg`/trace-baseline channel. Locking the local state to `F'(m_*)=0` makes the `m` channel quadratic, but only if the universal source law also suppresses transition-current, baseline-drift, boundary, and `K_perp` terms.

## Nonclaim Summary

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Gamma Source Expansion

{markdown_table(expansion, ["expansion_id", "statement", "derivation_or_bound", "implication", "status", "valid_for_claim"])}

## Screening Theorem Attempt

{markdown_table(screening, ["attempt_id", "condition", "why_needed", "status", "missing_input", "valid_for_claim"])}

## Transition Current Bound Contract

{markdown_table(transition, ["contract_id", "quantity", "needed_derivation", "bound_form", "current_status", "valid_for_claim"])}

## Response Kernel Fallback

{markdown_table(kernel, ["kernel_id", "arena", "fallback_requirement", "result", "why_not_claimable", "valid_for_claim"])}

## Decision

{markdown_table(decisions, ["decision_id", "decision", "reason", "result", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Verdict

This is progress because the missing theorem is now explicit. The least-cheaty path is not to assert a plateau; it is to derive support powers for the universal `X_B -> Pi_B` law and show that the transition current, trace-baseline gradients, and `K_perp` boundary residue are all suppressed below local-test response bounds.

## Next Target

`{NEXT_TARGET}`
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = source_register_rows(generated_utc)
    expansion = gamma_expansion_rows(generated_utc)
    screening = screening_attempt_rows(generated_utc)
    transition = transition_contract_rows(generated_utc)
    kernel = response_kernel_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validation_rows(sources, expansion, screening, transition, kernel, decisions, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(GAMMA_EXPANSION_PATH, expansion, ["expansion_id", "statement", "derivation_or_bound", "implication", "status", "valid_for_claim", "generated_utc"])
    write_csv(SCREENING_ATTEMPT_PATH, screening, ["attempt_id", "condition", "why_needed", "status", "missing_input", "valid_for_claim", "generated_utc"])
    write_csv(TRANSITION_CONTRACT_PATH, transition, ["contract_id", "quantity", "needed_derivation", "bound_form", "current_status", "valid_for_claim", "generated_utc"])
    write_csv(RESPONSE_KERNEL_PATH, kernel, ["kernel_id", "arena", "fallback_requirement", "result", "why_not_claimable", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "reason", "result", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, expansion, screening, transition, kernel, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    if failures:
        failure_text = "; ".join(f"{row['check_id']}={row['detail']}" for row in failures)
        raise SystemExit(f"798 validation failed: {failure_text}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"next={NEXT_TARGET}")


if __name__ == "__main__":
    main()

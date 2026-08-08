from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "826-Y5-R10-parent-memory-action-coefficient-checklist.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_826_SOURCE_REGISTER.csv"
ACTION_ANSATZ_PATH = RESIDUALS / "P8_Y5_R10_826_PARENT_ACTION_ANSATZ.csv"
COEFFICIENT_LEDGER_PATH = RESIDUALS / "P8_Y5_R10_826_COEFFICIENT_LEDGER.csv"
F1_LEMMA_PATH = RESIDUALS / "P8_Y5_R10_826_F1_ZERO_LEMMA.csv"
WARD_AUDIT_PATH = RESIDUALS / "P8_Y5_R10_826_WARD_BIANCHI_AUDIT.csv"
LOCAL_COSMO_GATE_PATH = RESIDUALS / "P8_Y5_R10_826_LOCAL_COSMO_GATE.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_826_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_826_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_826_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_826_VALIDATION.csv"

STATUS = "Y5_R10_826_parent_memory_action_coefficients_F1_zero_conditional_XB_Khat_open_nonclaim"
CLAIM_CEILING = "conditional_parent_coefficient_lemma_only_no_local_GR_no_cosmology_claim"
NEXT_TARGET = "827-Y5-R10-XB-drift-and-Khat-bound-after-F1-zero.md"

SOURCE_SPECS = [
    {
        "source_id": "825_doc",
        "path": POST_CHECKPOINT / "825-Y5-R10-C2A-closure-contract-and-parent-route-reset.md",
        "needles": [
            "C2A is now an explicitly firewalled closure branch",
            "PR825_0_memory_action_coefficients",
            "826-Y5-R10-parent-memory-action-coefficient-checklist.md",
        ],
        "role": "immediate parent-route reset source",
    },
    {
        "source_id": "825_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_825_VALIDATION.csv",
        "needles": [
            "V825_4_parent_route_selected,pass",
            "V825_9_all_rows_nonclaim,pass",
            "V825_11_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "parent_equations_v1",
        "path": FORMALIZATION / "83-parent-equations-v1.md",
        "needles": [
            "nabla_mu (K_matter^{mu nu} + K_MTS^{mu nu}) = 0.",
            "E7 is effective open-system dynamics, not a closed-action derivation.",
            "partial_m Gamma_eff |_(m=m_L) = 0",
            "X_B cannot be selected differently for galaxies, cosmology, and local gravity after seeing the data.",
        ],
        "role": "parent conservation, memory, trace-lock, and X_B discipline",
    },
    {
        "source_id": "798_gamma_screening",
        "path": POST_CHECKPOINT / "798-Y5-R10-Gammaeff-local-screening-source-law-or-response-kernel-bound.md",
        "needles": [
            "STA798_0_F_stationary_lock",
            "GSE798_2_local_locked_expansion",
            "TCB798_5_Kperp_boundary",
            "D798_0_conditional_screening_only",
        ],
        "role": "Gamma_eff local source expansion and F1 lock warning",
    },
    {
        "source_id": "797_ward_contract",
        "path": POST_CHECKPOINT / "797-Y5-R10-parent-relaxation-source-action-contract-and-Gammaeff-screening-gate.md",
        "needles": [
            "PAC797_3_Ward_identity",
            "RTL797_4_necessary_screening_condition",
            "missing_stress_variation",
        ],
        "role": "Ward identity and local screening necessity",
    },
    {
        "source_id": "equation_register",
        "path": FORMALIZATION / "05-equation-register.md",
        "needles": [
            "q^nu = nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu}",
            "The real Solar branch remains open until `F_1`, `M_tr`, `ell_tr`, `L_cg`, boundary data, and `K_perp,loc` are derived.",
            "Source-support / boundary-amplitude law",
        ],
        "role": "q/Khat identity and remaining local branch obligations",
    },
    {
        "source_id": "XB_firewall",
        "path": FORMALIZATION / "85-coarse-graining-invariants-XB.md",
        "needles": [
            "If `X_B` is arbitrary",
            "transition shells remain local PPN obligations,",
            "source-power closure open.",
        ],
        "role": "universal X_B firewall",
    },
]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def check_needles(path: Path, needles: list[str]) -> str:
    if not path.exists():
        return "missing_path"
    text = path.read_text(encoding="utf-8", errors="replace")
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return "missing_needles:" + ";".join(missing)
    return "pass"


def validation_file_clean(path: Path) -> tuple[bool, str]:
    if not path.exists():
        return False, f"missing={path}"
    failures: list[str] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("result") != "pass":
                failures.append(f"{row.get('check_id')}={row.get('result')}")
    if failures:
        return False, ";".join(failures)
    return True, f"{path.name} clean"


def formalization_workbench_modified_count() -> int:
    command = (
        "$fw='"
        + str(FORMALIZATION).replace("'", "''")
        + "'; "
        + "$cutoff=[datetime]'2026-05-31T14:42:00'; "
        + "(Get-ChildItem -LiteralPath $fw -Recurse -File | "
        + "Where-Object { $_.LastWriteTime -gt $cutoff }).Count"
    )
    completed = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        check=True,
        capture_output=True,
        text=True,
        timeout=20,
    )
    return int(completed.stdout.strip() or "0")


def source_register_rows(generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in SOURCE_SPECS:
        path = spec["path"]
        rows.append(
            {
                "source_id": spec["source_id"],
                "path": str(path),
                "exists": str(path.exists()).lower(),
                "needle_check": check_needles(path, spec["needles"]),
                "role": spec["role"],
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def action_ansatz_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "ansatz_id": "AA826_0_closed_parent_template",
            "object": "S_parent = integral sqrt(-g)[(R-2Lambda0)/(2kappa) + L_psi + L_m + L_int + L_bath_if_needed]",
            "derivation_value": "diffeomorphism-invariant action can own T_MTS and the Ward identity",
            "danger": "if m dynamics is genuinely irreversible, a closed action is not enough unless bath variables or an open-system variational principle are included",
            "status": "template_not_adopted",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "ansatz_id": "AA826_1_memory_sector",
            "object": "L_m = -1/2 Z_m(X_B) nabla_mu m nabla^mu m - V_R(m;X_B) plus sourced/bath terms",
            "derivation_value": "gives a Hilbert stress for the memory scalar and a local equilibrium condition from partial_m V_R=0",
            "danger": "Z_m, V_R, X_B, and any dissipation/source terms remain unsigned parent coefficients",
            "status": "candidate_coefficient_scaffold",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "ansatz_id": "AA826_2_trace_projection_lock",
            "object": "Gamma_eff = L_cg^-2 [F_L(X_B) + a_F (R(m;X_B)-R(m_L;X_B))]",
            "derivation_value": "if m_L is an extremum of R, the linear m-channel in Gamma_eff vanishes automatically",
            "danger": "the trace projection must be derived from K_MTS, not imposed after the fact",
            "status": "conditional_F1_zero_route",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "ansatz_id": "AA826_3_no_domain_primitives",
            "object": "No D, J_rel, C_coh, or domain-wall term is allowed inside 826 as a parent primitive.",
            "derivation_value": "prevents the demoted C2A branch from re-entering through notation",
            "danger": "without domain variables, cosmology shape must come from m/X_B coefficients instead",
            "status": "firewall_rule",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def coefficient_ledger_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "coefficient_id": "C826_0_Zm",
            "symbol": "Z_m(X_B)",
            "needed_for": "memory kinetic stress, stability, perturbation speed",
            "current_status": "missing_parent_value",
            "acceptance_gate": "positive/no-ghost and same local/cosmology value rule",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "coefficient_id": "C826_1_R_potential",
            "symbol": "R(m;X_B)",
            "needed_for": "local attractor, F1 zero, memory source shape",
            "current_status": "functional_form_missing",
            "acceptance_gate": "source R from parent invariants or microscopic/coarse-grained theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "coefficient_id": "C826_2_mL",
            "symbol": "m_L(X_B)",
            "needed_for": "local equilibrium/plateau without axiom",
            "current_status": "conditional_definition",
            "acceptance_gate": "partial_m R(m_L;X_B)=0 with stable positive second derivative",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "coefficient_id": "C826_3_trace_coefficients",
            "symbol": "F_L(X_B), a_F, L_cg(X_B)",
            "needed_for": "Gamma_eff trace projection, drift terms, cosmology amplitude",
            "current_status": "missing_parent_values",
            "acceptance_gate": "derive or bound gradients and amplitude before data",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "coefficient_id": "C826_4_relaxation_source",
            "symbol": "mu_B/gamma_B/lambda_R, U_B, S_cg",
            "needed_for": "fast local relaxation and large-scale memory survival",
            "current_status": "effective_open_system_scaffold",
            "acceptance_gate": "derive from bath/coarse-graining with Ward-safe exchange",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "coefficient_id": "C826_5_Khat_response",
            "symbol": "K_hat^{mu nu}[m,X_B,psi]",
            "needed_for": "q^nu ownership, local PPN residuals, anisotropic stress",
            "current_status": "missing_response_tensor",
            "acceptance_gate": "div K_hat cancels/bounds trace gradients or is proven zero with boundary data",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "coefficient_id": "C826_6_matter_descent",
            "symbol": "matter coupling / frame descent",
            "needed_for": "WEP, clocks, local Newtonian readout",
            "current_status": "missing_species_independent_descent",
            "acceptance_gate": "ordinary matter sees one metric/frame or deviations are explicitly bounded",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def f1_lemma_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "lemma_id": "F826_0_setup",
            "statement": "Let Gamma_eff=L_cg(X_B)^-2 [F_L(X_B)+a_F(R(m;X_B)-R(m_L;X_B))] and define m_L by partial_m R(m_L;X_B)=0.",
            "derivation": "This ties the trace projection to the same parent potential whose extremum defines the local memory state.",
            "result": "setup_conditional",
            "remaining_blocker": "must derive R, F_L, a_F, L_cg, and X_B rather than choose them",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lemma_id": "F826_1_F1_zero",
            "statement": "partial_m Gamma_eff evaluated at m=m_L equals a_F L_cg^-2 partial_m R(m_L;X_B)=0.",
            "derivation": "Differentiate Gamma_eff with respect to m at fixed X_B; R(m_L;X_B) is constant in that partial derivative and the equilibrium condition kills the linear term.",
            "result": "F1_zero_conditional_derivation",
            "remaining_blocker": "trace projection lock itself is an ansatz until varied from K_MTS",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lemma_id": "F826_2_quadratic_memory_channel",
            "statement": "For m=m_L+delta m, R-R_L=1/2 R_mm delta m^2+O(delta m^3), so the m-channel contribution to Gamma_eff is quadratic.",
            "derivation": "Taylor expand R about the stable local extremum m_L.",
            "result": "quadratic_channel_conditional",
            "remaining_blocker": "need bound on delta m, grad delta m, and R_mm in tested systems",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lemma_id": "F826_3_drift_not_solved",
            "statement": "Even when F1=0, nabla Gamma_eff still receives X_B, F_L, L_cg, m_L-drift, source, boundary, and K_hat-response terms.",
            "derivation": "Take the full spacetime gradient; partial_m cancellation removes only one channel.",
            "result": "local_GR_not_closed",
            "remaining_blocker": "derive X_B/L_cg drift bounds and K_hat divergence response",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def ward_audit_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "audit_id": "W826_0_closed_action_Ward",
            "condition": "All variables in S_parent, including X_B ancestors and any bath fields, are varied.",
            "result": "Ward_identity_possible",
            "reason": "diffeomorphism invariance gives total conservation on the full equations of motion",
            "blocker": "full variable list and bath/open-system completion are not derived",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "W826_1_external_XB_spurion",
            "condition": "X_B is treated as an external profile rather than derived from fields.",
            "result": "fails_parent_gate",
            "reason": "external X_B gradients act like spurion sources in the Ward identity",
            "blocker": "derive X_B from covariant invariants and vary its ancestors or bound the spurion response",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "W826_2_open_system_memory",
            "condition": "m obeys irreversible E7-style relaxation without bath/stress owner.",
            "result": "fails_closed_action_gate",
            "reason": "effective damping/source terms need a compensating bath/exchange stress to preserve total conservation",
            "blocker": "construct bath/Onsager/Schwinger-Keldysh-style owner or keep as effective scaffold",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "W826_3_Khat_required",
            "condition": "Gamma_eff varies but K_hat response is omitted.",
            "result": "hidden_nonconservation_or_local_failure",
            "reason": "q^nu=nabla^nu Gamma_eff-nabla_mu K_hat^{mu nu}; variable trace alone is not a local-GR proof",
            "blocker": "derive K_hat tensor response or prove/bound q_loc directly",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def local_cosmo_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "LC826_0_local_F1",
            "arena": "local",
            "condition": "partial_m Gamma_eff|m_L=0 and stable R_mm>0",
            "status": "conditional_progress",
            "not_enough_because": "X_B/L_cg drift, boundary terms, K_hat response, and matter readout remain open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "LC826_1_local_residual_vector",
            "arena": "local",
            "condition": "q_loc^nu, delta g_PPN, clock, R10, orbital, WEP residuals are zero or bounded",
            "status": "missing",
            "not_enough_because": "no numeric/source-backed response vector exists from this action scaffold",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "LC826_2_cosmology_source",
            "arena": "cosmology",
            "condition": "same R/X_B/L_cg coefficients generate the background memory source and amplitude pre-data",
            "status": "missing",
            "not_enough_because": "F1 zero does not fix b_mem, source shape, or perturbation closure",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "LC826_3_galaxy_firewall",
            "arena": "galaxy",
            "condition": "same X_B rule decides whether galaxy transport is active without sector retuning",
            "status": "missing",
            "not_enough_because": "X_B coefficients and routing projectors remain open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D826_0",
            "decision": "F1=0 can be conditionally derived if Gamma_eff is trace-locked to the parent memory potential R",
            "reason": "the extremum condition partial_m R(m_L;X_B)=0 kills partial_m Gamma_eff at the local state",
            "claim_ceiling": CLAIM_CEILING,
            "runnable": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D826_1",
            "decision": "local GR is still not closed",
            "reason": "F1 zero removes one dangerous linear channel, but X_B/L_cg drift, K_hat divergence, boundaries, perturbations, and matter descent remain unsourced",
            "claim_ceiling": CLAIM_CEILING,
            "runnable": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def next_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "derive or bound the remaining X_B/L_cg drift and K_hat divergence terms after the conditional F1 zero, producing a q_loc residual contract",
            "allowed_work": "symbolic gradient expansion, Ward/spurion audit, K_hat response contract, local residual vector definitions",
            "forbidden_work": "local-GR claim, data run, C2A domain closure promotion, choosing X_B gradients by hand",
            "priority": "high",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_survived": "a conditional parent-coefficient route that derives F1=0 from the same potential R that locks the local memory state",
            "what_failed": "numeric/source-backed coefficients, X_B/L_cg drift suppression, K_hat response, perturbations, and local residual bounds",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def validation_rows(
    source_rows: list[dict[str, object]],
    ansatz_rows: list[dict[str, object]],
    coefficient_rows: list[dict[str, object]],
    lemma_rows: list[dict[str, object]],
    ward_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail})

    add(
        "V826_0_sources_exist_and_needles",
        all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows),
        "all source paths exist and needles are present",
    )
    clean_825, clean_825_detail = validation_file_clean(RESIDUALS / "P8_Y5_BRR545_825_VALIDATION.csv")
    add("V826_1_prior_825_clean", clean_825, clean_825_detail)
    add(
        "V826_2_no_domain_primitives",
        any(row["ansatz_id"] == "AA826_3_no_domain_primitives" and row["status"] == "firewall_rule" for row in ansatz_rows),
        "demoted C2A domain primitives excluded",
    )
    add(
        "V826_3_coefficient_ledger_complete",
        {"C826_0_Zm", "C826_1_R_potential", "C826_2_mL", "C826_3_trace_coefficients", "C826_4_relaxation_source", "C826_5_Khat_response", "C826_6_matter_descent"}.issubset({row["coefficient_id"] for row in coefficient_rows}),
        "key parent coefficients and tensors listed",
    )
    add(
        "V826_4_F1_zero_conditional_lemma_recorded",
        any(row["lemma_id"] == "F826_1_F1_zero" and row["result"] == "F1_zero_conditional_derivation" for row in lemma_rows),
        "conditional F1 zero derivation recorded",
    )
    add(
        "V826_5_drift_and_Khat_open_recorded",
        any(row["lemma_id"] == "F826_3_drift_not_solved" for row in lemma_rows)
        and any(row["audit_id"] == "W826_3_Khat_required" for row in ward_rows),
        "X_B/L_cg drift and K_hat response remain open",
    )
    add(
        "V826_6_Ward_spurion_audit_present",
        {"W826_0_closed_action_Ward", "W826_1_external_XB_spurion", "W826_2_open_system_memory"}.issubset({row["audit_id"] for row in ward_rows}),
        "Ward, X_B spurion, and open-system audits present",
    )
    add(
        "V826_7_local_cosmo_gates_nonclaim",
        {"LC826_0_local_F1", "LC826_1_local_residual_vector", "LC826_2_cosmology_source"}.issubset({row["gate_id"] for row in gate_rows}),
        "local and cosmology gates present",
    )
    add(
        "V826_8_decision_nonrunnable",
        all(row["runnable"] == "false" for row in decisions),
        "branch remains non-runnable",
    )
    add(
        "V826_9_next_target_selected",
        any(row["next_target"] == NEXT_TARGET for row in next_rows),
        NEXT_TARGET,
    )
    all_rows = source_rows + ansatz_rows + coefficient_rows + lemma_rows + ward_rows + gate_rows + decisions + next_rows + summary
    add(
        "V826_10_all_rows_nonclaim",
        all(row.get("valid_for_claim") == "false" for row in all_rows),
        "all generated rows valid_for_claim=false",
    )
    add(
        "V826_11_no_data_or_local_GR_claim",
        all("data run" in row["forbidden_work"] and "local-GR claim" in row["forbidden_work"] for row in next_rows),
        "no data or local-GR claim selected",
    )
    changed = formalization_workbench_modified_count()
    add(
        "V826_12_formalization_workbench_untouched",
        changed == 0,
        f"formalization_changed_after_cutoff={changed}",
    )
    add("V826_13_validation_rows_ready", True, "validation table constructed")
    return rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def render_document(
    generated_utc: str,
    source_rows: list[dict[str, object]],
    ansatz_rows: list[dict[str, object]],
    coefficient_rows: list[dict[str, object]],
    lemma_rows: list[dict[str, object]],
    ward_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    summary: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> str:
    return "\n\n".join(
        [
            "# 826 - Y5 R10 Parent Memory Action Coefficient Checklist",
            (
                "Current result: **there is a real conditional win: `F_1=0` follows if `Gamma_eff` is trace-locked to the same parent memory potential `R(m;X_B)` whose extremum defines the local state**. "
                "This is not a local-GR proof. It removes the linear `m` channel, while leaving `X_B/L_cg` drift, `K_hat` response, boundaries, perturbations, and matter descent open."
            ),
            f"Generated UTC: `{generated_utc}`",
            "## Nonclaim Summary\n\n" + markdown_table(summary, ["status", "claim_ceiling", "what_survived", "what_failed", "next_target", "valid_for_claim"]),
            "## Parent Action Ansatz\n\n" + markdown_table(ansatz_rows, ["ansatz_id", "object", "derivation_value", "danger", "status", "valid_for_claim"]),
            "## Coefficient Ledger\n\n" + markdown_table(coefficient_rows, ["coefficient_id", "symbol", "needed_for", "current_status", "acceptance_gate", "valid_for_claim"]),
            "## F1 Zero Lemma\n\n" + markdown_table(lemma_rows, ["lemma_id", "statement", "derivation", "result", "remaining_blocker", "valid_for_claim"]),
            "## Ward/Bianchi Audit\n\n" + markdown_table(ward_rows, ["audit_id", "condition", "result", "reason", "blocker", "valid_for_claim"]),
            "## Local/Cosmology Gates\n\n" + markdown_table(gate_rows, ["gate_id", "arena", "condition", "status", "not_enough_because", "valid_for_claim"]),
            "## Decision\n\n" + markdown_table(decisions, ["decision_id", "decision", "reason", "claim_ceiling", "runnable", "next_target", "valid_for_claim"]),
            "## Next Target\n\n" + markdown_table(next_rows, ["next_target", "objective", "allowed_work", "forbidden_work", "valid_for_claim"]),
            "## Source Register\n\n" + markdown_table(source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"]),
            "## Validation\n\n" + markdown_table(validation, ["check_id", "result", "detail"]),
            "## Verdict\n\n"
            "This is better than a plateau axiom: the linear trace derivative can be killed by an extremum of a parent potential, provided that potential really owns the trace projection. "
            "But the remaining drift and tensor-response terms are now the fight. The next checkpoint should derive or bound those terms directly rather than claiming victory from `F_1=0` alone.",
        ]
    )


def main() -> None:
    generated_utc = datetime.now(timezone.utc).isoformat(timespec="seconds")

    source_rows = source_register_rows(generated_utc)
    ansatz_rows = action_ansatz_rows(generated_utc)
    coefficient_rows = coefficient_ledger_rows(generated_utc)
    lemma_rows = f1_lemma_rows(generated_utc)
    ward_rows = ward_audit_rows(generated_utc)
    gate_rows = local_cosmo_gate_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    next_rows = next_target_rows(generated_utc)
    summary = nonclaim_summary_rows(generated_utc)
    validation = validation_rows(source_rows, ansatz_rows, coefficient_rows, lemma_rows, ward_rows, gate_rows, decisions, next_rows, summary)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(ACTION_ANSATZ_PATH, ansatz_rows, ["ansatz_id", "object", "derivation_value", "danger", "status", "valid_for_claim", "generated_utc"])
    write_csv(COEFFICIENT_LEDGER_PATH, coefficient_rows, ["coefficient_id", "symbol", "needed_for", "current_status", "acceptance_gate", "valid_for_claim", "generated_utc"])
    write_csv(F1_LEMMA_PATH, lemma_rows, ["lemma_id", "statement", "derivation", "result", "remaining_blocker", "valid_for_claim", "generated_utc"])
    write_csv(WARD_AUDIT_PATH, ward_rows, ["audit_id", "condition", "result", "reason", "blocker", "valid_for_claim", "generated_utc"])
    write_csv(LOCAL_COSMO_GATE_PATH, gate_rows, ["gate_id", "arena", "condition", "status", "not_enough_because", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "reason", "claim_ceiling", "runnable", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_rows, ["next_target", "objective", "allowed_work", "forbidden_work", "priority", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "what_survived", "what_failed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])

    OUTPUT_DOC.write_text(
        render_document(generated_utc, source_rows, ansatz_rows, coefficient_rows, lemma_rows, ward_rows, gate_rows, decisions, next_rows, summary, validation),
        encoding="utf-8",
    )

    failed = [row for row in validation if row["result"] != "pass"]
    if failed:
        details = "; ".join(f"{row['check_id']}={row['detail']}" for row in failed)
        raise SystemExit(f"826 validation failed: {details}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")


if __name__ == "__main__":
    main()

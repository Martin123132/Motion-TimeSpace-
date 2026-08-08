from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "797-Y5-R10-parent-relaxation-source-action-contract-and-Gammaeff-screening-gate.md"
NEXT_TARGET = "798-Y5-R10-Gammaeff-local-screening-source-law-or-response-kernel-bound.md"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_797_SOURCE_REGISTER.csv"
TRADEOFF_LEMMA_PATH = RESIDUALS / "P8_Y5_R10_797_RELAXATION_TRADEOFF_LEMMA.csv"
PARENT_CONTRACT_PATH = RESIDUALS / "P8_Y5_R10_797_PARENT_ACTION_CONTRACT.csv"
GAMMA_SCREENING_PATH = RESIDUALS / "P8_Y5_R10_797_GAMMAEFF_SCREENING_GATE.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_797_RELAXATION_ROUTE_DECISION.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_797_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_797_VALIDATION.csv"

STATUS = "Y5_R10_797_relaxation_tradeoff_derived_Gammaeff_screening_required_nonclaim"
CLAIM_CEILING = "operator_tradeoff_and_parent_action_contract_only_no_Gammaeff_screening_theorem_no_local_GR_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    TRADEOFF_LEMMA_PATH,
    PARENT_CONTRACT_PATH,
    GAMMA_SCREENING_PATH,
    DECISION_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCE_SPECS = [
    {
        "source_id": "796_doc",
        "path": POST_CHECKPOINT / "796-Y5-R10-KL-amplitude-PPN-budget-or-parent-relaxation-source.md",
        "needles": ["Current result", "PRS796_4_parent_action_contract", "D796_1_relaxation_route_selected"],
        "role": "immediate parent relaxation contract target",
    },
    {
        "source_id": "796_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_796_VALIDATION.csv",
        "needles": ["V796_6_relaxation_contract_written,pass", "V796_11_no_local_GR_claim,pass"],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "795_origin",
        "path": POST_CHECKPOINT / "795-Y5-R10-parent-origin-of-tracefree-Khat-solver-or-amplitude-bound.md",
        "needles": ["POA795_1_relaxation_source", "KAB795_0_scale_law"],
        "role": "parent-origin and amplitude warning",
    },
    {
        "source_id": "794_solver",
        "path": POST_CHECKPOINT / "794-Y5-R10-tracefree-longitudinal-Khat-solver-or-PPN-bound.md",
        "needles": ["TLS794_2_flat_cancellation", "TLS794_4_amplitude_warning"],
        "role": "trace-free solver and amplitude obstruction",
    },
    {
        "source_id": "793_relaxation_candidate",
        "path": POST_CHECKPOINT / "793-Y5-R10-Gamma-Khat-balance-source-equation-or-local-bound-inputs.md",
        "needles": ["GBS793_3_relaxation_fixed_point", "LBI793_3_amplitude_bound"],
        "role": "earlier relaxation fixed-point candidate",
    },
    {
        "source_id": "formal_eq_split",
        "path": FORMALIZATION / "05-equation-register.md",
        "needles": ["Gamma_eff = -1/4 K_MTS", "q^nu = nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu}"],
        "role": "core Gamma/Khat/q definition",
    },
    {
        "source_id": "formal_red_screening",
        "path": FORMALIZATION / "06-consistency-red-team.md",
        "needles": ["open-system memory relaxation", "transition current is now the screening deal-breaker"],
        "role": "screening and transition-current risk",
    },
    {
        "source_id": "formal_spine_relaxation",
        "path": FORMALIZATION / "07-unification-spine.md",
        "needles": ["effective-potential/relaxation-functional locking F(m; X_B)", "derive the relaxation functional `R(m; X_B)`"],
        "role": "spine route to relaxation-functional parent law",
    },
    {
        "source_id": "796_relaxation_csv",
        "path": RESIDUALS / "P8_Y5_R10_796_PARENT_RELAXATION_SOURCE_TEST.csv",
        "needles": ["PRS796_1_stationary_equation", "PRS796_3_Gammaeff_screening_need"],
        "role": "machine-readable 796 relaxation rows",
    },
    {
        "source_id": "796_budget_csv",
        "path": RESIDUALS / "P8_Y5_R10_796_KL_AMPLITUDE_PPN_BUDGET.csv",
        "needles": ["KLB796_1_elliptic_scale_estimate", "KLB796_5_acceptance_condition"],
        "role": "machine-readable 796 amplitude rows",
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


def parse_validation_clean(start: int = 665, end: int = 796) -> tuple[bool, str]:
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


def tradeoff_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "lemma_id": "RTL797_0_operator_setup",
            "statement": "Let H_TF be local trace-free symmetric tensors and V_loc be local projected exchange vectors. Define L K = P_loc nabla_mu K^{mu nu} and s = P_loc nabla^nu Gamma_eff.",
            "derivation": "Then q_loc = s - L K. The parent-relaxation candidate is the Tikhonov functional J[K]=1/2||L K-s||^2 + mu_K^2/2||K||^2 plus boundary/stability terms.",
            "result": "sets the exact balance problem into a controlled variational operator problem",
            "status": "formal_local_operator_lemma",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lemma_id": "RTL797_1_stationary_solution",
            "statement": "Varying K in the trace-free sector gives (L^dagger L + mu_K^2 I)K = L^dagger s.",
            "derivation": "For singular mode L e_i = sigma_i f_i, the stationary solution is K_i = sigma_i s_i/(sigma_i^2 + mu_K^2).",
            "result": "a parent relaxation source can be mathematically well-posed if L, L^dagger, P_loc, boundary data, and mu_K are parent-defined",
            "status": "formal_solution_not_parent_signed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lemma_id": "RTL797_2_residual_tradeoff",
            "statement": "The residual mode is q_i = s_i - sigma_i K_i = mu_K^2 s_i/(sigma_i^2 + mu_K^2).",
            "derivation": "Small mu_K makes q_i small only on modes with sigma_i not near zero; large mu_K suppresses K_i but leaves q_i near s_i.",
            "result": "relaxation gives a tradeoff, not a free q_loc zero theorem",
            "status": "no_free_lunch_tradeoff",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lemma_id": "RTL797_3_amplitude_bound",
            "statement": "The carrier amplitude obeys |K_i| = |sigma_i s_i|/(sigma_i^2 + mu_K^2) <= |s_i|/(2 mu_K) for mu_K>0.",
            "derivation": "The maximum of sigma/(sigma^2+mu_K^2) is 1/(2 mu_K). This bounds K but worsens the residual on weakly controlled modes.",
            "result": "amplitude control requires nonzero mu_K, but nonzero mu_K prevents exact q_loc cancellation unless s is itself small or in high-sigma modes",
            "status": "amplitude_bound_tradeoff",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "lemma_id": "RTL797_4_necessary_screening_condition",
            "statement": "To make both |q_loc| and |K_L| locally safe without tuning, the source s=P_loc grad Gamma_eff must be screened, projected out, or observationally invisible.",
            "derivation": "If s is order local curvature/source on low-sigma modes, either K is large enough to create PPN/Newton stress or q_loc remains large enough to create exchange/nonconservation residuals.",
            "result": "Gamma_eff local screening or response-kernel invisibility becomes the next hard theorem",
            "status": "screening_required",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def parent_contract_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "contract_id": "PAC797_0_covariant_fields",
            "requirement": "Define the parent variables whose trace-free sector contains K_hat or its coarse-grained moment ancestor.",
            "why_required": "prevents K_hat relaxation from being an external closure term",
            "current_status": "missing_parent_variable_map",
            "promotion_test": "explicit S_MTS[e,omega,Phi] variation produces the K_hat sector",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "PAC797_1_projectors",
            "requirement": "Define P_loc and Pi_TF covariantly or as controlled effective local-environment projectors.",
            "why_required": "local projector choices can otherwise hide preferred-frame/readout violations",
            "current_status": "missing_covariant_projector_definition",
            "promotion_test": "projectors commute with the local covariance/PPN assumptions or their leakage is bounded",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "PAC797_2_positive_operator",
            "requirement": "Provide a positive relaxation norm, boundary conditions, and operator adjoint L^dagger.",
            "why_required": "the tradeoff lemma only has meaning if the inner product and boundary terms are physical",
            "current_status": "missing_inner_product_and_boundary_law",
            "promotion_test": "J is positive in the effective local rest frame or replaced by a conservative hyperbolic parent with the same bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "PAC797_3_Ward_identity",
            "requirement": "Show the relaxation stress/exchange contribution preserves total diffeomorphism Ward identity and Bianchi consistency.",
            "why_required": "an arbitrary dissipative q_loc repair can violate conservation even if it solves a local equation",
            "current_status": "missing_stress_variation",
            "promotion_test": "delta_e S_relax and delta_Phi S_relax produce a conserved total stress/exchange split",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "PAC797_4_causality_stability",
            "requirement": "If relaxation is dynamical, prove positivity, stability, and no acausal or PPN-transient leakage.",
            "why_required": "open-system smoothing can look good statically but fail in clocks/orbits",
            "current_status": "missing_dynamical_completion",
            "promotion_test": "linearized modes are stable and all transients are below local bounds",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "PAC797_5_matter_readout",
            "requirement": "Prove ordinary matter does not couple directly to the relaxation variables except through e, omega[e], and owned gauge fields.",
            "why_required": "otherwise WEP, clocks, and PPN readout can fail even if q_loc is small",
            "current_status": "missing_no_spurion_signature",
            "promotion_test": "species-independent matter action descent or sourced charge bounds",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def gamma_screening_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "GSG797_0_source_definition",
            "gate": "local source vector",
            "condition": "s^nu = P_loc nabla^nu Gamma_eff must be small, projected out, or observationally kernel-invisible.",
            "derived_reason": "The relaxation tradeoff cannot make q_loc and K_L both safe for arbitrary s.",
            "current_status": "not_derived",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "GSG797_1_environmental_mass",
            "gate": "Gamma_eff screening mass",
            "condition": "A parent potential or relaxation law gives M_Gamma^2(X_B) L_loc^2 >> 1 in tested local systems while allowing controlled galaxy/FLRW memory.",
            "derived_reason": "large local screening mass can suppress delta Gamma_eff and therefore s=P_loc grad Gamma_eff.",
            "current_status": "candidate_from_spine_not_parent_derived",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "GSG797_2_constant_plateau",
            "gate": "local plateau",
            "condition": "Gamma_eff = Gamma_L + O(epsilon) and P_loc grad Gamma_eff = O(epsilon/L_loc) with epsilon below Newton/PPN tolerance.",
            "derived_reason": "a constant Gamma_eff can be absorbed into a tiny local Lambda-like background; gradients drive q_loc.",
            "current_status": "missing_plateau_theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "GSG797_3_transition_shell",
            "gate": "transition-current safety",
            "condition": "gradients across local-to-galaxy transition shells must not leak into P_loc observables or must have a response bound.",
            "derived_reason": "previous red-team notes identify transition current as the screening deal-breaker.",
            "current_status": "still_open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "GSG797_4_response_kernel",
            "gate": "observable kernel fallback",
            "condition": "If s is not small, prove the induced q/K response lies in the kernel of Newton, PPN, clock, orbital, R10, and WEP readouts.",
            "derived_reason": "this is the only alternative to true Gamma_eff source screening.",
            "current_status": "missing_response_kernel",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D797_0_relaxation_derivation_attempt",
            "decision": "Can a quadratic parent-relaxation functional close local GR by itself?",
            "reason": "The operator solution has an unavoidable residual-versus-amplitude tradeoff.",
            "result": "rejected_as_standalone_zero_proof",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D797_1_screening_required",
            "decision": "What is the least-cheaty next theorem?",
            "reason": "Both q_loc and K_L become safe only if s=P_loc grad Gamma_eff is locally screened, projected out, or in the observable kernel.",
            "result": "derive_Gammaeff_screening_or_response_kernel",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D797_2_parent_contract_retained",
            "decision": "Do we keep the relaxation route?",
            "reason": "Yes, but only as a parent-action contract with explicit covariance, Ward, stability, boundary, and matter-readout requirements.",
            "result": "retain_as_contract_not_claim",
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
            "main_result": "A Tikhonov-style relaxation source can be written and its stationary solution derived, but it produces a tradeoff: exact q_loc suppression wants small mu_K, while K_L amplitude suppression wants large mu_K.",
            "hard_blocker": "Need a parent-signed Gamma_eff local-screening/source law or an observable-kernel proof; otherwise either q_loc or K_L remains locally dangerous.",
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
    tradeoff: list[dict[str, object]],
    parent_contract: list[dict[str, object]],
    gamma_screening: list[dict[str, object]],
    decisions: list[dict[str, object]],
    summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    prior_clean, prior_detail = parse_validation_clean()
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in sources)
    all_nonclaim = all(
        row.get("valid_for_claim") == "false"
        for group in [sources, tradeoff, parent_contract, gamma_screening, decisions, summary]
        for row in group
    )
    stationary_solution = any(row["lemma_id"] == "RTL797_1_stationary_solution" and "K_i = sigma_i s_i/(sigma_i^2 + mu_K^2)" in row["derivation"] for row in tradeoff)
    residual_tradeoff = any(row["lemma_id"] == "RTL797_2_residual_tradeoff" and "mu_K^2 s_i/(sigma_i^2 + mu_K^2)" in row["statement"] for row in tradeoff)
    amplitude_bound = any(row["lemma_id"] == "RTL797_3_amplitude_bound" and "<= |s_i|/(2 mu_K)" in row["statement"] for row in tradeoff)
    screening_required = any(row["lemma_id"] == "RTL797_4_necessary_screening_condition" for row in tradeoff)
    parent_contract_complete = {row["contract_id"] for row in parent_contract} == {
        "PAC797_0_covariant_fields",
        "PAC797_1_projectors",
        "PAC797_2_positive_operator",
        "PAC797_3_Ward_identity",
        "PAC797_4_causality_stability",
        "PAC797_5_matter_readout",
    }
    gamma_gates_complete = {row["gate_id"] for row in gamma_screening} == {
        "GSG797_0_source_definition",
        "GSG797_1_environmental_mass",
        "GSG797_2_constant_plateau",
        "GSG797_3_transition_shell",
        "GSG797_4_response_kernel",
    }
    no_standalone_claim = any(row["decision_id"] == "D797_0_relaxation_derivation_attempt" and row["result"] == "rejected_as_standalone_zero_proof" for row in decisions)
    next_target_selected = summary[0]["next_target"] == NEXT_TARGET and any(row["decision_id"] == "D797_1_screening_required" for row in decisions)
    formalization_count = formalization_change_count()

    checks = [
        ("V797_0_sources_exist_and_needles", source_ok, "all source paths exist and needles are present"),
        ("V797_1_prior_665_796_clean", prior_clean, prior_detail),
        ("V797_2_outputs_scoped", all_outputs_scoped(), str(POST_CHECKPOINT)),
        ("V797_3_all_rows_nonclaim", all_nonclaim, "all generated rows valid_for_claim=false"),
        ("V797_4_stationary_solution_derived", stationary_solution, "operator stationary solution recorded"),
        ("V797_5_residual_tradeoff_derived", residual_tradeoff, "q_i residual tradeoff recorded"),
        ("V797_6_amplitude_bound_derived", amplitude_bound, "K_i amplitude bound recorded"),
        ("V797_7_screening_required", screening_required, "Gamma_eff screening/source suppression required"),
        ("V797_8_parent_contract_complete", parent_contract_complete, "parent action contract rows complete"),
        ("V797_9_gamma_gates_complete", gamma_gates_complete, "Gamma_eff screening gates complete"),
        ("V797_10_no_standalone_relaxation_claim", no_standalone_claim, "relaxation alone rejected as zero proof"),
        ("V797_11_next_target_selected", next_target_selected, NEXT_TARGET),
        ("V797_12_no_local_GR_claim", all_nonclaim and no_standalone_claim, "local GR/Newton remains blocked"),
        ("V797_13_claim_artifacts_absent", not (POST_CHECKPOINT / "LOCAL_GR_CLAIM.md").exists(), "no local-GR claim artifact present"),
        ("V797_14_formalization_workbench_untouched", formalization_count == 0, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V797_15_validation_rows_ready", True, "validation table constructed"),
    ]
    return [{"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail} for check_id, passed, detail in checks]


def build_doc(
    sources: list[dict[str, object]],
    tradeoff: list[dict[str, object]],
    parent_contract: list[dict[str, object]],
    gamma_screening: list[dict[str, object]],
    decisions: list[dict[str, object]],
    summary: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 797 - Y5 R10 Parent Relaxation Source Action Contract And Gammaeff Screening Gate

Current result: **the parent-relaxation route is useful but not sufficient by itself**. Writing the local problem as `J[K]=1/2||L K-s||^2+mu_K^2/2||K||^2` gives a clean stationary equation and a real amplitude bound, but it also proves the tradeoff: exact `q_loc` suppression and small `K_L` cannot both be guaranteed for arbitrary `s=P_loc grad Gamma_eff`. The next real theorem must suppress `Gamma_eff` gradients locally or prove they are invisible to tested observables.

## Nonclaim Summary

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Relaxation Tradeoff Lemma

{markdown_table(tradeoff, ["lemma_id", "statement", "derivation", "result", "status", "valid_for_claim"])}

## Parent Action Contract

{markdown_table(parent_contract, ["contract_id", "requirement", "why_required", "current_status", "promotion_test", "valid_for_claim"])}

## Gammaeff Screening Gate

{markdown_table(gamma_screening, ["gate_id", "gate", "condition", "derived_reason", "current_status", "valid_for_claim"])}

## Decision

{markdown_table(decisions, ["decision_id", "decision", "reason", "result", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Verdict

This is a useful tightening, not a pass. The relaxation route avoids a hand-tuned `K_L` counterterm, but the operator algebra itself says there is no free lunch: small residual wants small `mu_K`; small carrier amplitude wants large `mu_K`. Therefore local GR now hinges on deriving a parent-signed local `Gamma_eff` screening/source law or proving the remaining response lies in the observable kernel.

## Next Target

`{NEXT_TARGET}`
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = source_register_rows(generated_utc)
    tradeoff = tradeoff_rows(generated_utc)
    parent_contract = parent_contract_rows(generated_utc)
    gamma_screening = gamma_screening_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validation_rows(sources, tradeoff, parent_contract, gamma_screening, decisions, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(TRADEOFF_LEMMA_PATH, tradeoff, ["lemma_id", "statement", "derivation", "result", "status", "valid_for_claim", "generated_utc"])
    write_csv(PARENT_CONTRACT_PATH, parent_contract, ["contract_id", "requirement", "why_required", "current_status", "promotion_test", "valid_for_claim", "generated_utc"])
    write_csv(GAMMA_SCREENING_PATH, gamma_screening, ["gate_id", "gate", "condition", "derived_reason", "current_status", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "reason", "result", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, tradeoff, parent_contract, gamma_screening, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    if failures:
        failure_text = "; ".join(f"{row['check_id']}={row['detail']}" for row in failures)
        raise SystemExit(f"797 validation failed: {failure_text}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"next={NEXT_TARGET}")


if __name__ == "__main__":
    main()

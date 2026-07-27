from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work"
)
OUT = ROOT / "source-intake" / "mts_residuals"
SCRIPT_PATH = ROOT / "scripts" / "Y5_R10_WEP_source_normalization_or_common_geometry_zero_theorem.py"
DOC_PATH = ROOT / "652-Y5-R10-WEP-source-normalization-or-common-geometry-zero-theorem.md"

STATUS = "Y5_R10_WEP_common_geometry_zero_theorem_conditional_source_normalization_target_retained_nonclaim"
CLAIM_CEILING = "conditional_WEP_zero_theorem_and_beta_source_target_only_no_WEP_or_local_GR_claim"
NEXT_TARGET = "653-Y5-R10-parent-matter-functor-signature-or-WEP-closure-demotion.md"

ETA_MICROSCOPE_BOUND = 2.8e-15
PRODUCT_BOUND_ALPHA = 2.932961e-8
DELTA_Q_ALPHA_COULOMB = 1.989808886825e-3
DELTA_Q_SURFACE_BINDING = 3.306456347405e-3


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def beta_required(delta_q: float) -> float:
    return ETA_MICROSCOPE_BOUND / (PRODUCT_BOUND_ALPHA * delta_q)


def source_register_rows() -> list[dict[str, object]]:
    sources = [
        ("S652_0", "checkpoint_651_doc", ROOT / "651-Y5-R10-WEP-alpha-sensitivity-source-fill-or-screening-stress-test.md", "prior WEP alpha stress test"),
        ("S652_1", "validation_651", OUT / "P8_Y5_BRR545_651_VALIDATION.csv", "prior validation"),
        ("S652_2", "WEP_stress_651", OUT / "P8_Y5_R10_651_WEP_ALPHA_STRESS_TEST.csv", "unit-source WEP overshoot rows"),
        ("S652_3", "charge_estimate_651", OUT / "P8_Y5_R10_651_DAMOUR_DONOGHUE_CHARGE_ESTIMATE.csv", "Ti/Pt composition charge smoke rows"),
        ("S652_4", "screening_gates_651", OUT / "P8_Y5_R10_651_SCREENING_OPTION_GATES.csv", "zero theorem versus source-normalization fork"),
        ("S652_5", "cross_arena_contract_650", OUT / "P8_Y5_R10_650_CROSS_ARENA_CONTRACT.csv", "same-screen cross-arena contract"),
        ("S652_6", "screen_rule_650", OUT / "P8_Y5_R10_650_ULTRA_SCREENED_RULE.csv", "product-bound screen owner"),
        ("S652_7", "WEP_species_universality_371", ROOT / "371-WEP-species-universality-or-active-eta-runner.md", "species universality no-go"),
        ("S652_8", "WEP_observed_coframe_373", ROOT / "373-one-observed-coframe-parent-selector-or-WEP-closure.md", "one observed coframe closure contract"),
        ("S652_9", "WEP_common_F_388", ROOT / "388-WEP-species-symmetry-common-F-parent-selector-attempt.md", "species-blind geometry functor contract"),
        ("S652_10", "generator_script_652", SCRIPT_PATH, "this checkpoint generator"),
    ]
    return [
        {
            "source_id": source_id,
            "label": label,
            "path": rel(path),
            "exists": bool_text(path.exists()),
            "role": role,
            "valid_for_claim": "false",
        }
        for source_id, label, path, role in sources
    ]


def common_geometry_zero_theorem_rows() -> list[dict[str, object]]:
    return [
        {
            "theorem_id": "CGZ652",
            "name": "conditional common-geometry WEP alpha zero theorem",
            "statement": "If the parent matter action is a species-blind geometry functor S_m=sum_A S_A[Psi_A, ehat, omega[ehat], theta_A], theta_A is internal-only and chi_X-independent, and no alpha_EM(chi_X), m_A(chi_X), F_A(C_D), or representative matter vertex survives, then the WEP alpha/composition source charge difference vanishes: Delta alpha_AB^chi=0.",
            "proof_status": "proved_as_conditional_template",
            "parent_signed": "false",
            "what_it_would_close": "direct MICROSCOPE Ti/Pt alpha-composition WEP channel",
            "what_it_does_not_close": "universal metric fifth-force/PPN/source-normalization residuals and local-GR reduction",
            "valid_for_claim": "false",
        }
    ]


def proof_clause_audit_rows() -> list[dict[str, object]]:
    return [
        {
            "clause_id": "CGZ652_0_single_geometry_argument",
            "needed_statement": "All matter species use one observed coframe ehat and connection omega[ehat].",
            "mathematical_form": "S_m=sum_A S_A[Psi_A, ehat, omega[ehat], theta_A]",
            "current_support": "373 one observed coframe; 388 species-blind geometry functor",
            "current_status": "conditional_closure_not_parent_derived",
            "failure_if_missing": "species metrics or coframes reintroduce WEP violation",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "CGZ652_1_species_labels_internal_only",
            "needed_statement": "Species labels live only in ordinary internal constants/representations and not in class-sector spurions.",
            "mathematical_form": "theta_A={m_A,q_A,spin_A,rep_A} with partial_chi_X theta_A=0",
            "current_support": "388 contract",
            "current_status": "not_parent_derived",
            "failure_if_missing": "m_A(chi_X), q_A(chi_X), or alpha_A(chi_X) gives composition charges",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "CGZ652_2_no_alpha_or_mass_vertex",
            "needed_statement": "No local alpha_EM(chi_X), f_A(chi_X)F^2, m_A(chi_X), or binding-energy response is a direct matter argument.",
            "mathematical_form": "delta S_matter/d chi_X |_{ehat,theta_A}=0",
            "current_support": "649 no-alpha-vertex clause; 651 WEP stress target",
            "current_status": "unsigned_and_currently_the_hard_blocker",
            "failure_if_missing": "Damour-Donoghue composition charges become physically sourced",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "CGZ652_3_representative_vertices_forbidden",
            "needed_statement": "Matter cannot couple to representative data B_perp, b_2, Cperp, or local representative leakage.",
            "mathematical_form": "S_matter descends to quotient/class observables only",
            "current_support": "371 lifted-C representative invariance route",
            "current_status": "conditional_progress_but_not_enough_for_common_F",
            "failure_if_missing": "direct representative WEP forces return",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "CGZ652_4_selector_stress_ward_identity",
            "needed_statement": "Any selector enforcing ehat/common-F owns its stress in the total Ward identity.",
            "mathematical_form": "nabla_mu(T_matter+T_MTS+T_selector)^mu_nu=0",
            "current_support": "373 parent-action contract",
            "current_status": "open",
            "failure_if_missing": "zero theorem hides an unconserved selector force",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "CGZ652_5_local_domain_classifier",
            "needed_statement": "The local lab/source domain is selected before data and shares the 650 screen contract.",
            "mathematical_form": "D_parent(local source/test bodies) fixed before fitting eta_AB",
            "current_support": "650 no-special-pleading gate",
            "current_status": "not_parent_derived",
            "failure_if_missing": "WEP-specific screening becomes post-hoc special pleading",
            "valid_for_claim": "false",
        },
    ]


def source_normalization_target_rows() -> list[dict[str, object]]:
    rows = []
    for target_id, channel, delta_q in [
        ("BST652_0_alpha_Coulomb", "alpha/Coulomb composition charge", DELTA_Q_ALPHA_COULOMB),
        ("BST652_1_surface_binding", "nuclear surface/binding composition charge", DELTA_Q_SURFACE_BINDING),
    ]:
        beta = beta_required(delta_q)
        rows.append(
            {
                "target_id": target_id,
                "channel": channel,
                "eta_bound": f"{ETA_MICROSCOPE_BOUND:.6e}",
                "clock_product_bound_used": f"{PRODUCT_BOUND_ALPHA:.6e}",
                "delta_Q_abs": f"{delta_q:.12e}",
                "required_abs_beta_source_max": f"{beta:.12e}",
                "formula": "beta_source_max = eta_MICROSCOPE/(|kappa_alpha*S_lab_alpha|_max * |Delta Q_AB|)",
                "kappa_rescaling_status": "independent_of_kappa_if_clock_product_bound_is_saturated",
                "status": "numeric_target_not_derived",
                "valid_for_claim": "false",
            }
        )
    rows.append(
        {
            "target_id": "BST652_2_robust_target",
            "channel": "robust stricter of alpha/surface smoke channels",
            "eta_bound": f"{ETA_MICROSCOPE_BOUND:.6e}",
            "clock_product_bound_used": f"{PRODUCT_BOUND_ALPHA:.6e}",
            "delta_Q_abs": f"{max(DELTA_Q_ALPHA_COULOMB, DELTA_Q_SURFACE_BINDING):.12e}",
            "required_abs_beta_source_max": f"{min(beta_required(DELTA_Q_ALPHA_COULOMB), beta_required(DELTA_Q_SURFACE_BINDING)):.12e}",
            "formula": "use the smaller beta target until a full material model replaces the smoke estimate",
            "kappa_rescaling_status": "not_fixed_by_kappa_rescaling",
            "status": "recommended_nonclaim_stress_target",
            "valid_for_claim": "false",
        }
    )
    return rows


def parent_action_contract_rows() -> list[dict[str, object]]:
    return [
        {
            "contract_id": "PAC652_0_matter_functor",
            "required_parent_statement": "Matter action is a species-blind functor of one observed geometry.",
            "must_show": "all matter sectors receive ehat from the same parent map and species labels do not alter the map",
            "promotion_condition": "derived from parent action, not assumed as minimal coupling",
            "current_status": "unsigned",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "PAC652_1_constants_independent",
            "required_parent_statement": "Local matter constants and alpha_EM are not functions of chi_X/C_D in lab/source domains.",
            "must_show": "partial_chi_X theta_A=0 and no lambda_A f(chi_X)F^2 survives",
            "promotion_condition": "explicit operator exclusion or quotient descent proof",
            "current_status": "unsigned",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "PAC652_2_source_stress_accounting",
            "required_parent_statement": "Selector/source normalization stress is included in the conserved total stress ledger.",
            "must_show": "no hidden fifth force remains after imposing common geometry",
            "promotion_condition": "Ward identity closes with T_selector and T_MTS",
            "current_status": "open",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "PAC652_3_beta_source_owner",
            "required_parent_statement": "If common-geometry zero fails, beta_source_alpha is derived and below the robust target.",
            "must_show": f"abs(beta_source_alpha) <= {min(beta_required(DELTA_Q_ALPHA_COULOMB), beta_required(DELTA_Q_SURFACE_BINDING)):.3e}",
            "promotion_condition": "parent/source-normalization theorem or sourced empirical calibration",
            "current_status": "numeric_target_only",
            "valid_for_claim": "false",
        },
    ]


def decision_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "DG652_0_conditional_zero_theorem",
            "gate": "common-geometry WEP alpha zero theorem written",
            "result": "pass_template",
            "consequence": "exact clauses now exist for parent action to sign",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "DG652_1_parent_signed_zero",
            "gate": "all common-geometry clauses are parent-derived",
            "result": "fail_unsigned",
            "consequence": "WEP zero is not claimed",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "DG652_2_beta_target",
            "gate": "source-normalization target written",
            "result": "pass_nonclaim",
            "consequence": "finite-alpha branch has an exact beta_source target if zero theorem fails",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "DG652_3_kappa_rescale_escape",
            "gate": "change kappa_alpha to evade WEP while keeping clock product bound",
            "result": "fail_policy",
            "consequence": "WEP target uses |kappa_alpha*S_lab_alpha|, so kappa rescaling alone does not rescue the branch",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "DG652_4_public_WEP_claim",
            "gate": "claim WEP/local-GR pass",
            "result": "fail_policy",
            "consequence": "private theorem/bound contract only",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D652_0",
            "route": "common_geometry_zero",
            "decision": "conditional_theorem_written_not_parent_signed",
            "why": "it would kill the direct composition channel, but the parent matter functor and no-alpha-vertex clauses are still unsigned",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D652_1",
            "route": "source_normalization_bound",
            "decision": "retained_as_numeric_fallback_target",
            "why": "if zero theorem fails, beta_source_alpha must be below the 651/652 WEP target",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D652_2",
            "route": "next_parent_action_test",
            "decision": "try_to_sign_parent_matter_functor_or_demote_to_closure",
            "why": "this is the least handwavy WEP route and the one a serious referee would accept if derived",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def next_contract_rows() -> list[dict[str, object]]:
    return [
        {
            "contract_id": "NC652_0",
            "next_target": NEXT_TARGET,
            "work_item": "Try to sign the species-blind parent matter functor from the MTS parent action.",
            "acceptance_condition": "derive one ehat for all matter and show theta_A is internal-only/chi-independent",
        },
        {
            "contract_id": "NC652_1",
            "next_target": NEXT_TARGET,
            "work_item": "If parent signing fails, demote common geometry to an explicit WEP closure axiom.",
            "acceptance_condition": "closure label is explicit and WEP/local-GR claim remains blocked",
        },
        {
            "contract_id": "NC652_2",
            "next_target": NEXT_TARGET,
            "work_item": "Keep beta_source_alpha as the fallback numeric target.",
            "acceptance_condition": "future source-normalization theorem must beat the robust beta target, not just be small by assertion",
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, object]]:
    robust_beta = min(beta_required(DELTA_Q_ALPHA_COULOMB), beta_required(DELTA_Q_SURFACE_BINDING))
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "conditional_zero_theorem_written": "true",
            "parent_signed_zero": "false",
            "clock_product_bound_used": f"{PRODUCT_BOUND_ALPHA:.3e}",
            "robust_beta_source_alpha_target": f"{robust_beta:.3e}",
            "kappa_rescale_escape": "false",
            "WEP_claim": "false",
            "hardest_blocker": "parent matter functor/no-alpha-vertex/selector Ward clauses are unsigned",
            "next_target": NEXT_TARGET,
        }
    ]


def validation_rows(
    source_rows: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    clause_rows: list[dict[str, object]],
    beta_rows: list[dict[str, object]],
    contract_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decision: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V652_0_source_paths_exist", all(row["exists"] == "true" for row in source_rows), "all cited local source paths exist"))
    prior = read_csv(OUT / "P8_Y5_BRR545_651_VALIDATION.csv")
    checks.append(("V652_1_prior_651_validation_clean", all(row.get("result") == "pass" for row in prior), "651 validation remains clean"))
    checks.append(("V652_2_conditional_theorem_written", theorem_rows[0]["proof_status"] == "proved_as_conditional_template", "common-geometry zero theorem template is written"))
    checks.append(("V652_3_theorem_not_parent_signed", theorem_rows[0]["parent_signed"] == "false", "zero theorem remains parent-unsigned"))
    unsigned_statuses = {"conditional_closure_not_parent_derived", "not_parent_derived", "unsigned_and_currently_the_hard_blocker", "conditional_progress_but_not_enough_for_common_F", "open"}
    checks.append(("V652_4_unsigned_clauses_present", any(row["current_status"] in unsigned_statuses for row in clause_rows), "proof audit preserves unsigned blockers"))
    robust = [row for row in beta_rows if row["target_id"] == "BST652_2_robust_target"]
    checks.append(("V652_5_beta_target_strict", len(robust) == 1 and float(robust[0]["required_abs_beta_source_max"]) < 3e-5, "robust beta target is below 3e-5"))
    checks.append(("V652_6_kappa_rescale_rejected", any(row["gate_id"] == "DG652_3_kappa_rescale_escape" and row["result"] == "fail_policy" for row in gate_rows), "kappa rescale escape is blocked"))
    checks.append(("V652_7_parent_contract_unsigned", all(row["valid_for_claim"] == "false" and row["current_status"] in {"unsigned", "open", "numeric_target_only"} for row in contract_rows), "parent action contract remains unsigned/nonclaim"))
    checks.append(("V652_8_public_claim_blocked", any(row["gate_id"] == "DG652_4_public_WEP_claim" and row["result"] == "fail_policy" for row in gate_rows), "public WEP/local-GR claim is blocked"))
    checks.append(("V652_9_decisions_nonclaim", all(row["valid_for_claim"] == "false" for row in decision), "decision rows are nonclaim"))
    checks.append(("V652_10_next_target_653", all(row["next_target"] == NEXT_TARGET for row in decision + next_rows), "next target points to 653"))
    checks.append(("V652_11_summary_blocks_claim", summary[0]["parent_signed_zero"] == "false" and summary[0]["WEP_claim"] == "false", "summary blocks WEP claim"))

    fw = ROOT.parent / "formalization-workbench"
    cutoff = datetime(2026, 5, 31, 14, 42, 0).timestamp()
    changed_after_cutoff = 0
    if fw.exists():
        for path in fw.rglob("*"):
            if path.is_file() and path.stat().st_mtime > cutoff:
                changed_after_cutoff += 1
    checks.append(("V652_12_formalization_workbench_unchanged", changed_after_cutoff == 0, f"formalization files changed after cutoff: {changed_after_cutoff}"))

    return [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "generated_utc": now_iso(),
        }
        for check_id, passed, detail in checks
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            text = str(row.get(column, "")).replace("|", "\\|").replace("\n", " ")
            values.append(text)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    source_rows: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    clause_rows: list[dict[str, object]],
    beta_rows: list[dict[str, object]],
    contract_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decision: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    summary: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    robust_beta = min(beta_required(DELTA_Q_ALPHA_COULOMB), beta_required(DELTA_Q_SURFACE_BINDING))
    lines = [
        "# 652 Y5/R10 WEP Source Normalization or Common-Geometry Zero Theorem",
        "",
        "## Verdict",
        "",
        f"- Status: `{STATUS}`",
        f"- Claim ceiling: `{CLAIM_CEILING}`",
        "- A clean common-geometry zero theorem can be written: if all matter sees one species-blind geometry and no local `alpha_EM(chi_X)`/mass/class-response vertex survives, the differential WEP alpha charge is zero.",
        "- The theorem is still conditional, not parent-signed, because the current parent action has not derived the matter functor, no-alpha-vertex rule, or selector Ward identity.",
        f"- If the zero theorem fails, the source-normalization fallback must satisfy `|beta_source_alpha| <= {robust_beta:.3e}` in the stricter 651 smoke channel.",
        "- Rescaling `kappa_alpha` is not an escape, because clocks constrain the product `|kappa_alpha*S_lab_alpha|`, and WEP uses that same product.",
        "",
        "## Source Register",
        "",
        markdown_table(source_rows, ["source_id", "label", "path", "exists", "role"]),
        "",
        "## Common-Geometry Zero Theorem",
        "",
        markdown_table(theorem_rows, ["theorem_id", "name", "proof_status", "parent_signed", "what_it_would_close", "what_it_does_not_close"]),
        "",
        "## Proof Clause Audit",
        "",
        markdown_table(clause_rows, ["clause_id", "needed_statement", "mathematical_form", "current_status", "failure_if_missing"]),
        "",
        "## Source-Normalization Target",
        "",
        markdown_table(beta_rows, ["target_id", "channel", "eta_bound", "clock_product_bound_used", "delta_Q_abs", "required_abs_beta_source_max", "kappa_rescaling_status", "status"]),
        "",
        "## Parent Action Contract",
        "",
        markdown_table(contract_rows, ["contract_id", "required_parent_statement", "must_show", "promotion_condition", "current_status"]),
        "",
        "## Decision Gates",
        "",
        markdown_table(gate_rows, ["gate_id", "gate", "result", "consequence"]),
        "",
        "## Decision",
        "",
        markdown_table(decision, ["decision_id", "route", "decision", "why", "next_target"]),
        "",
        "## Next Contract",
        "",
        markdown_table(next_rows, ["contract_id", "work_item", "acceptance_condition"]),
        "",
        "## Validation",
        "",
        markdown_table(validation, ["check_id", "result", "detail"]),
        "",
        "## Interpretation",
        "",
        "- This is progress: WEP is no longer a vague danger; it is now either a clean geometry theorem or a precise source-normalization target.",
        "- The preferred route is still derivation, not tuning: prove the matter functor and no-alpha-vertex clauses from the parent action.",
        "- If that cannot be signed, the honest move is to mark WEP safety as closure and keep local-GR/WEP claims blocked.",
        "",
        "## Nonclaim Summary",
        "",
        markdown_table(summary, ["status", "conditional_zero_theorem_written", "parent_signed_zero", "clock_product_bound_used", "robust_beta_source_alpha_target", "kappa_rescale_escape", "WEP_claim", "hardest_blocker", "next_target"]),
        "",
    ]
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source_rows = source_register_rows()
    theorem_rows = common_geometry_zero_theorem_rows()
    clause_rows = proof_clause_audit_rows()
    beta_rows = source_normalization_target_rows()
    contract_rows = parent_action_contract_rows()
    gate_rows = decision_gate_rows()
    decision = decision_rows()
    next_rows = next_contract_rows()
    summary = nonclaim_summary_rows()
    validation = validation_rows(source_rows, theorem_rows, clause_rows, beta_rows, contract_rows, gate_rows, decision, next_rows, summary)

    write_csv(OUT / "P8_Y5_R10_652_SOURCE_REGISTER.csv", source_rows)
    write_csv(OUT / "P8_Y5_R10_652_COMMON_GEOMETRY_ZERO_THEOREM.csv", theorem_rows)
    write_csv(OUT / "P8_Y5_R10_652_PROOF_CLAUSE_AUDIT.csv", clause_rows)
    write_csv(OUT / "P8_Y5_R10_652_SOURCE_NORMALIZATION_TARGET.csv", beta_rows)
    write_csv(OUT / "P8_Y5_R10_652_PARENT_ACTION_CONTRACT.csv", contract_rows)
    write_csv(OUT / "P8_Y5_R10_652_DECISION_GATES.csv", gate_rows)
    write_csv(OUT / "P8_Y5_BRR545_652_DECISION.csv", decision)
    write_csv(OUT / "P8_Y5_R10_652_NEXT_CONTRACT.csv", next_rows)
    write_csv(OUT / "P8_Y5_R10_652_NONCLAIM_SUMMARY.csv", summary)
    write_csv(OUT / "P8_Y5_BRR545_652_VALIDATION.csv", validation)
    write_doc(source_rows, theorem_rows, clause_rows, beta_rows, contract_rows, gate_rows, decision, next_rows, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"wrote_doc={DOC_PATH}")
    print(f"wrote_csv_dir={OUT}")
    print(f"robust_beta_source_alpha_target={summary[0]['robust_beta_source_alpha_target']}")
    print(f"validation_rows={len(validation)}")
    print(f"validation_failures={len(failures)}")
    print(f"status={STATUS}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for row in failures:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()

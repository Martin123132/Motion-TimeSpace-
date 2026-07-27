from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work"
)
OUT = ROOT / "source-intake" / "mts_residuals"
SCRIPT_PATH = ROOT / "scripts" / "Y5_R10_parent_matter_functor_signature_or_WEP_closure_demotion.py"
DOC_PATH = ROOT / "653-Y5-R10-parent-matter-functor-signature-or-WEP-closure-demotion.md"

STATUS = "Y5_R10_parent_matter_functor_not_signed_WEP_common_geometry_demoted_to_explicit_closure_nonclaim"
CLAIM_CEILING = "explicit_WEP_closure_and_parent_signature_audit_only_no_WEP_PPN_or_local_GR_claim"
NEXT_TARGET = "654-Y5-R10-local-GR-reduction-spine-under-explicit-WEP-closure.md"

ROBUST_BETA_SOURCE_ALPHA_TARGET = 2.887280314062e-5
CLOCK_PRODUCT_BOUND_ALPHA = 2.932961e-8


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


def source_register_rows() -> list[dict[str, object]]:
    sources = [
        ("S653_0", "checkpoint_652_doc", ROOT / "652-Y5-R10-WEP-source-normalization-or-common-geometry-zero-theorem.md", "prior WEP zero theorem / beta target fork"),
        ("S653_1", "validation_652", OUT / "P8_Y5_BRR545_652_VALIDATION.csv", "prior validation"),
        ("S653_2", "parent_action_contract_652", OUT / "P8_Y5_R10_652_PARENT_ACTION_CONTRACT.csv", "unsigned parent action contract"),
        ("S653_3", "proof_clause_audit_652", OUT / "P8_Y5_R10_652_PROOF_CLAUSE_AUDIT.csv", "unsigned WEP zero theorem clauses"),
        ("S653_4", "source_normalization_target_652", OUT / "P8_Y5_R10_652_SOURCE_NORMALIZATION_TARGET.csv", "robust beta_source fallback target"),
        ("S653_5", "WEP_species_universality_371", ROOT / "371-WEP-species-universality-or-active-eta-runner.md", "species universality no-go"),
        ("S653_6", "WEP_observed_coframe_373", ROOT / "373-one-observed-coframe-parent-selector-or-WEP-closure.md", "one observed coframe closure contract"),
        ("S653_7", "WEP_common_F_388", ROOT / "388-WEP-species-symmetry-common-F-parent-selector-attempt.md", "species-blind geometry functor contract"),
        ("S653_8", "local_chiX_silence_649", ROOT / "649-Y5-R10-local-chiX-silence-theorem-or-ultra-screened-alpha-branch.md", "no-alpha-vertex clause remains unsigned"),
        ("S653_9", "cross_arena_contract_650", ROOT / "650-Y5-R10-ultra-screened-alpha-branch-cross-arena-contract.md", "no special pleading / shared screen contract"),
        ("S653_10", "WEP_stress_651", ROOT / "651-Y5-R10-WEP-alpha-sensitivity-source-fill-or-screening-stress-test.md", "WEP unit-source stress test"),
        ("S653_11", "generator_script_653", SCRIPT_PATH, "this checkpoint generator"),
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


def signature_requirement_rows() -> list[dict[str, object]]:
    return [
        {
            "requirement_id": "PMF653_0_explicit_parent_matter_functor",
            "required_signature": "S_parent contains S_matter=sum_A S_A[Psi_A, ehat, omega[ehat], theta_A]",
            "why_needed": "one geometry argument must be structural, not inferred after WEP pressure",
            "current_evidence": "373/388 write the conditional form but do not derive it from parent dynamics",
            "signature_status": "unsigned",
            "consequence": "common-geometry WEP zero remains closure",
            "valid_for_claim": "false",
        },
        {
            "requirement_id": "PMF653_1_geometry_map_species_blind",
            "required_signature": "ehat_A(Phi)=ehat(Phi) for every species A",
            "why_needed": "forbids F_A(C_D) and species-dependent coframe pullbacks",
            "current_evidence": "species-blind functor is identified as the right symmetry in 388",
            "signature_status": "not_parent_derived",
            "consequence": "Delta F_AB can still exist in allowed covariant actions",
            "valid_for_claim": "false",
        },
        {
            "requirement_id": "PMF653_2_theta_internal_only",
            "required_signature": "partial_chi_X theta_A=0 and no class-sector spurion sigma_A C_D O_A",
            "why_needed": "species labels may differ, but not through MTS class response",
            "current_evidence": "listed as parent contract in 652",
            "signature_status": "unsigned",
            "consequence": "m_A(chi_X), q_A(chi_X), or alpha_A(chi_X) remains an allowed WEP-risk operator",
            "valid_for_claim": "false",
        },
        {
            "requirement_id": "PMF653_3_no_alpha_mass_vertex",
            "required_signature": "delta S_matter/dchi_X | ehat,theta_A = 0 and no f_A(chi_X)F^2",
            "why_needed": "Damour-Donoghue composition charges become physical if alpha/mass vertices survive",
            "current_evidence": "649 and 652 flag no-alpha-vertex as unsigned hard blocker",
            "signature_status": "unsigned_hard_blocker",
            "consequence": "WEP alpha-composition channel cannot be claimed zero",
            "valid_for_claim": "false",
        },
        {
            "requirement_id": "PMF653_4_selector_Ward_identity",
            "required_signature": "nabla_mu(T_matter+T_MTS+T_selector)^mu_nu=0 after selecting ehat",
            "why_needed": "a selector that enforces one geometry must not hide an unconserved fifth force",
            "current_evidence": "373/652 identify the Ward ledger but do not close it",
            "signature_status": "open",
            "consequence": "even assumed common geometry does not yet prove local GR/PPN safety",
            "valid_for_claim": "false",
        },
        {
            "requirement_id": "PMF653_5_domain_selection_predata",
            "required_signature": "D_parent(local lab/source domains) is fixed before fitting WEP/clock data",
            "why_needed": "prevents WEP-specific screening or local/cosmology toggles",
            "current_evidence": "650 no-special-pleading gate",
            "signature_status": "not_parent_derived",
            "consequence": "lab screening remains a contract rather than evidence",
            "valid_for_claim": "false",
        },
    ]


def theorem_attempt_rows() -> list[dict[str, object]]:
    return [
        {
            "attempt_id": "TA653_0_diffeomorphism_invariance",
            "route": "derive matter functor from covariance alone",
            "verdict": "fail",
            "reason": "covariance permits species-indexed metrics or class functions such as S_A[Psi_A, exp(F_A(C_D))g]",
            "what_survives": "general covariance is necessary but not a WEP theorem",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "TA653_1_local_Lorentz_invariance",
            "route": "derive one ehat from local Lorentz symmetry",
            "verdict": "fail",
            "reason": "each species can be locally Lorentz invariant on its own ehat_A unless a parent selector forbids it",
            "what_survives": "local Lorentz constrains each geometry, not species universality",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "TA653_2_representative_invariance",
            "route": "derive species-blind geometry from quotient/representative descent",
            "verdict": "partial_fail",
            "reason": "representative vertices can be conditionally forbidden, but F_A(C_D) is already quotient-invariant",
            "what_survives": "useful no-representative-vertex control, not common-F",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "TA653_3_species_blind_functor",
            "route": "write S_matter as a species-blind geometry functor",
            "verdict": "conditional_pass_not_signed",
            "reason": "if inserted as parent structure it gives common geometry, but current corpus does not derive why it must be inserted",
            "what_survives": "best closure/theorem target",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "TA653_4_identity_coframe",
            "route": "set observed coframe equal to the local GR coframe",
            "verdict": "strongest_closure_not_derived",
            "reason": "identity coframe would remove the class pullback but has not been parent-selected",
            "what_survives": "usable explicit closure for private model-building only",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "TA653_5_naturalness_smallness",
            "route": "argue species couplings should be small",
            "verdict": "fail",
            "reason": "WEP needs a symmetry/selection theorem or a numerical source-normalization derivation, not taste",
            "what_survives": "none for claims",
            "valid_for_claim": "false",
        },
    ]


def closure_demotion_rows() -> list[dict[str, object]]:
    return [
        {
            "closure_id": "WCL653_0_one_observed_geometry",
            "closure_statement": "All matter, photons, clocks, rulers, and standards couple to one observed geometry ehat.",
            "mathematical_form": "ehat_A=ehat for every A",
            "why_it_is_closure": "not derived from parent MTS action in current corpus",
            "what_it_blocks": "species coframe / species metric WEP violation",
            "status": "explicit_closure_axiom",
            "valid_for_claim": "false",
        },
        {
            "closure_id": "WCL653_1_species_blind_geometry_map",
            "closure_statement": "The geometry map from MTS variables to ehat is species-blind.",
            "mathematical_form": "F_A(C_D)=F(C_D)",
            "why_it_is_closure": "representative invariance does not force common F",
            "what_it_blocks": "Delta F_AB class-metric WEP split",
            "status": "explicit_closure_axiom",
            "valid_for_claim": "false",
        },
        {
            "closure_id": "WCL653_2_no_chi_dependent_constants",
            "closure_statement": "Local matter constants and alpha_EM do not directly depend on chi_X/C_D.",
            "mathematical_form": "partial_chi_X theta_A=0 and partial_chi_X alpha_EM=0 locally",
            "why_it_is_closure": "no-alpha/no-mass vertex exclusion remains unsigned",
            "what_it_blocks": "Damour-Donoghue alpha/mass composition channel",
            "status": "explicit_closure_axiom",
            "valid_for_claim": "false",
        },
        {
            "closure_id": "WCL653_3_selector_stress_accounting",
            "closure_statement": "Any selector enforcing the observed geometry is included in total stress conservation.",
            "mathematical_form": "nabla_mu(T_matter+T_MTS+T_selector)^mu_nu=0",
            "why_it_is_closure": "selector Ward identity is not closed",
            "what_it_blocks": "hidden unconserved fifth force from the closure itself",
            "status": "explicit_closure_axiom_required_before_use",
            "valid_for_claim": "false",
        },
        {
            "closure_id": "WCL653_4_beta_source_fallback",
            "closure_statement": "If any direct alpha composition source survives, beta_source_alpha must be below the 652 robust target.",
            "mathematical_form": f"|beta_source_alpha| <= {ROBUST_BETA_SOURCE_ALPHA_TARGET:.3e}",
            "why_it_is_closure": "source-normalization theorem not derived",
            "what_it_blocks": "unit-source MICROSCOPE overshoot",
            "status": "numeric_fallback_target_not_claim",
            "valid_for_claim": "false",
        },
    ]


def residual_ledger_rows() -> list[dict[str, object]]:
    return [
        {
            "residual_id": "RL653_0_direct_alpha_WEP",
            "residual": "eta_AB^alpha ~ beta_source_alpha * DeltaQ_AB * |kappa_alpha*S_lab_alpha|",
            "control_if_closure_adopted": "zero if WCL653_2 is assumed",
            "control_if_closure_not_adopted": f"requires |beta_source_alpha| <= {ROBUST_BETA_SOURCE_ALPHA_TARGET:.3e}",
            "claim_status": "blocked",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RL653_1_species_metric_split",
            "residual": "eta_AB^F ~ Delta F_AB",
            "control_if_closure_adopted": "zero if WCL653_1 is assumed",
            "control_if_closure_not_adopted": "active WEP residual; no numeric score without parent coefficients",
            "claim_status": "blocked",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RL653_2_representative_leakage",
            "residual": "eta_AB^rep ~ epsilon_rep * c_AB",
            "control_if_closure_adopted": "conditional zero if quotient descent is parent-owned",
            "control_if_closure_not_adopted": "active representative-force residual",
            "claim_status": "conditional_only",
            "valid_for_claim": "false",
        },
        {
            "residual_id": "RL653_3_universal_metric_force",
            "residual": "universal scalar/metric pullback can affect PPN/R10 even if WEP differential channel is closed",
            "control_if_closure_adopted": "not solved by WEP closure",
            "control_if_closure_not_adopted": "active local-GR/PPN/R10 target",
            "claim_status": "separate_derivation_required",
            "valid_for_claim": "false",
        },
    ]


def decision_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "DG653_0_parent_signature_found",
            "gate": "current corpus derives the parent matter functor signature",
            "result": "fail_unsigned",
            "consequence": "WEP common-geometry zero cannot be promoted",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "DG653_1_closure_demotion_written",
            "gate": "WEP common geometry is explicitly demoted to closure",
            "result": "pass",
            "consequence": "future work cannot accidentally cite it as derived",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "DG653_2_beta_fallback_retained",
            "gate": "beta_source fallback remains active if direct alpha channel survives",
            "result": "pass_nonclaim",
            "consequence": "numeric WEP pressure is preserved",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "DG653_3_local_GR_claim",
            "gate": "claim local GR/PPN/WEP pass from closure",
            "result": "fail_policy",
            "consequence": "closure can organize the branch but cannot replace derivation",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "DG653_4_next_branch",
            "gate": "resume local-GR reduction with closure labels explicit",
            "result": "pass_next_contract",
            "consequence": "654 should build the local GR spine without hiding WEP closure",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D653_0",
            "route": "parent_matter_functor_signature",
            "decision": "not_signed_by_current_corpus",
            "why": "the exact species-blind functor is known, but no parent action derivation forces it",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D653_1",
            "route": "WEP_common_geometry",
            "decision": "demoted_to_explicit_closure",
            "why": "this keeps the branch usable privately without mislabeling WEP safety as derived",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D653_2",
            "route": "local_GR_reduction",
            "decision": "resume_under_closure_labels",
            "why": "WEP is now cleanly boxed; next pressure is whether the local metric/coframe sector actually reduces to GR",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def next_contract_rows() -> list[dict[str, object]]:
    return [
        {
            "contract_id": "NC653_0",
            "next_target": NEXT_TARGET,
            "work_item": "Build the local-GR reduction spine with WEP closure labels explicit.",
            "acceptance_condition": "separate derived, closure, and numeric-bound pieces before any PPN/local claim",
        },
        {
            "contract_id": "NC653_1",
            "next_target": NEXT_TARGET,
            "work_item": "Track whether identity coframe/common matter functor is assumed or parent-derived in every local-GR step.",
            "acceptance_condition": "validation fails any local-GR row that silently uses WEP closure as a theorem",
        },
        {
            "contract_id": "NC653_2",
            "next_target": NEXT_TARGET,
            "work_item": "Keep beta_source_alpha as a live fallback if direct alpha/mass source coupling returns.",
            "acceptance_condition": "future finite-alpha source branch must beat the robust beta target",
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "parent_matter_functor_signed": "false",
            "WEP_common_geometry_status": "explicit_closure",
            "direct_alpha_WEP_zero_claim": "false",
            "beta_source_alpha_target_retained": f"{ROBUST_BETA_SOURCE_ALPHA_TARGET:.3e}",
            "local_GR_claim": "false",
            "hardest_blocker": "species-blind matter functor/no-alpha-vertex/selector Ward identity are not parent-derived",
            "next_target": NEXT_TARGET,
        }
    ]


def validation_rows(
    source_rows: list[dict[str, object]],
    signature_rows: list[dict[str, object]],
    attempt_rows: list[dict[str, object]],
    closure_rows: list[dict[str, object]],
    residual_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decision: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V653_0_source_paths_exist", all(row["exists"] == "true" for row in source_rows), "all cited local source paths exist"))
    prior = read_csv(OUT / "P8_Y5_BRR545_652_VALIDATION.csv")
    checks.append(("V653_1_prior_652_validation_clean", all(row.get("result") == "pass" for row in prior), "652 validation remains clean"))
    checks.append(("V653_2_signature_unsigned", any(row["signature_status"] in {"unsigned", "not_parent_derived", "unsigned_hard_blocker", "open"} for row in signature_rows), "matter functor signature remains unsigned"))
    checks.append(("V653_3_no_successful_derivation", not any(row["verdict"] == "pass_signed" for row in attempt_rows), "no derivation route is marked parent-signed"))
    checks.append(("V653_4_closure_rows_written", len(closure_rows) >= 5 and all("closure" in row["status"] or "target" in row["status"] for row in closure_rows), "explicit WEP closure rows are written"))
    checks.append(("V653_5_beta_target_retained", any(str(ROBUST_BETA_SOURCE_ALPHA_TARGET)[:5] in row["mathematical_form"] or "2.887e-05" in row["mathematical_form"] for row in closure_rows), "robust beta target retained in closure/fallback ledger"))
    checks.append(("V653_6_residuals_block_claims", all(row["valid_for_claim"] == "false" and row["claim_status"] in {"blocked", "conditional_only", "separate_derivation_required"} for row in residual_rows), "residual ledger blocks claims"))
    checks.append(("V653_7_closure_demotion_gate_passes", any(row["gate_id"] == "DG653_1_closure_demotion_written" and row["result"] == "pass" for row in gate_rows), "closure demotion gate passes"))
    checks.append(("V653_8_local_GR_claim_blocked", any(row["gate_id"] == "DG653_3_local_GR_claim" and row["result"] == "fail_policy" for row in gate_rows), "local GR claim is blocked"))
    checks.append(("V653_9_decisions_nonclaim", all(row["valid_for_claim"] == "false" for row in decision), "decision rows are nonclaim"))
    checks.append(("V653_10_next_target_654", all(row["next_target"] == NEXT_TARGET for row in decision + next_rows), "next target points to 654"))
    checks.append(("V653_11_summary_demotes_closure", summary[0]["parent_matter_functor_signed"] == "false" and summary[0]["WEP_common_geometry_status"] == "explicit_closure", "summary demotes WEP common geometry to closure"))

    fw = ROOT.parent / "formalization-workbench"
    cutoff = datetime(2026, 5, 31, 14, 42, 0).timestamp()
    changed_after_cutoff = 0
    if fw.exists():
        for path in fw.rglob("*"):
            if path.is_file() and path.stat().st_mtime > cutoff:
                changed_after_cutoff += 1
    checks.append(("V653_12_formalization_workbench_unchanged", changed_after_cutoff == 0, f"formalization files changed after cutoff: {changed_after_cutoff}"))

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
    signature_rows: list[dict[str, object]],
    attempt_rows: list[dict[str, object]],
    closure_rows: list[dict[str, object]],
    residual_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decision: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    summary: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    lines = [
        "# 653 Y5/R10 Parent Matter Functor Signature or WEP Closure Demotion",
        "",
        "## Verdict",
        "",
        f"- Status: `{STATUS}`",
        f"- Claim ceiling: `{CLAIM_CEILING}`",
        "- The exact parent signature needed for WEP safety is known, but the current corpus does not derive it.",
        "- Therefore common-geometry WEP safety is demoted to an explicit closure axiom, not a theorem.",
        f"- The fallback numeric target remains live: `|beta_source_alpha| <= {ROBUST_BETA_SOURCE_ALPHA_TARGET:.3e}` if any direct alpha/mass source channel survives.",
        "- This is not a collapse of the branch; it is a quarantine label so later local-GR work cannot accidentally use WEP closure as proof.",
        "",
        "## Source Register",
        "",
        markdown_table(source_rows, ["source_id", "label", "path", "exists", "role"]),
        "",
        "## Parent Signature Requirements",
        "",
        markdown_table(signature_rows, ["requirement_id", "required_signature", "why_needed", "signature_status", "consequence"]),
        "",
        "## Theorem Attempt Audit",
        "",
        markdown_table(attempt_rows, ["attempt_id", "route", "verdict", "reason", "what_survives"]),
        "",
        "## WEP Closure Demotion",
        "",
        markdown_table(closure_rows, ["closure_id", "closure_statement", "mathematical_form", "why_it_is_closure", "what_it_blocks", "status"]),
        "",
        "## Residual Ledger",
        "",
        markdown_table(residual_rows, ["residual_id", "residual", "control_if_closure_adopted", "control_if_closure_not_adopted", "claim_status"]),
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
        "- This is the honest outcome: we found the right WEP-safe matter structure, but not the parent derivation of it.",
        "- The closure is still scientifically useful because it separates `assumed matter coupling` from `derived local gravity`.",
        "- Next we can build the local-GR reduction spine without smuggling WEP safety in through the side door.",
        "",
        "## Nonclaim Summary",
        "",
        markdown_table(summary, ["status", "parent_matter_functor_signed", "WEP_common_geometry_status", "direct_alpha_WEP_zero_claim", "beta_source_alpha_target_retained", "local_GR_claim", "hardest_blocker", "next_target"]),
        "",
    ]
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source_rows = source_register_rows()
    signature_rows = signature_requirement_rows()
    attempt_rows = theorem_attempt_rows()
    closure_rows = closure_demotion_rows()
    residual_rows = residual_ledger_rows()
    gate_rows = decision_gate_rows()
    decision = decision_rows()
    next_rows = next_contract_rows()
    summary = nonclaim_summary_rows()
    validation = validation_rows(source_rows, signature_rows, attempt_rows, closure_rows, residual_rows, gate_rows, decision, next_rows, summary)

    write_csv(OUT / "P8_Y5_R10_653_SOURCE_REGISTER.csv", source_rows)
    write_csv(OUT / "P8_Y5_R10_653_PARENT_SIGNATURE_REQUIREMENTS.csv", signature_rows)
    write_csv(OUT / "P8_Y5_R10_653_THEOREM_ATTEMPT_AUDIT.csv", attempt_rows)
    write_csv(OUT / "P8_Y5_R10_653_WEP_CLOSURE_DEMOTION.csv", closure_rows)
    write_csv(OUT / "P8_Y5_R10_653_RESIDUAL_LEDGER.csv", residual_rows)
    write_csv(OUT / "P8_Y5_R10_653_DECISION_GATES.csv", gate_rows)
    write_csv(OUT / "P8_Y5_BRR545_653_DECISION.csv", decision)
    write_csv(OUT / "P8_Y5_R10_653_NEXT_CONTRACT.csv", next_rows)
    write_csv(OUT / "P8_Y5_R10_653_NONCLAIM_SUMMARY.csv", summary)
    write_csv(OUT / "P8_Y5_BRR545_653_VALIDATION.csv", validation)
    write_doc(source_rows, signature_rows, attempt_rows, closure_rows, residual_rows, gate_rows, decision, next_rows, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"wrote_doc={DOC_PATH}")
    print(f"wrote_csv_dir={OUT}")
    print(f"WEP_common_geometry_status={summary[0]['WEP_common_geometry_status']}")
    print(f"beta_source_alpha_target={summary[0]['beta_source_alpha_target_retained']}")
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

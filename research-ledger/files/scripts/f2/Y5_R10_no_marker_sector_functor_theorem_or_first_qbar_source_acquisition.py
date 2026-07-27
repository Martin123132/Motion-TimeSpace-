from __future__ import annotations

import csv
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "980-Y5-R10-no-marker-sector-functor-theorem-or-first-qbar-source-acquisition.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def md_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body])


def source_path(relative_path: str) -> Path:
    return ROOT / relative_path


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "979_doc",
            "path": "979-Y5-R10-parent-action-spine-superselection-clause-or-first-qbar-prior-source.md",
            "role": "direct handoff selecting no-marker sector functor theorem",
            "needle": "DGT979_7_verdict",
        },
        {
            "source_id": "975_doc",
            "path": "975-Y5-R10-no-linear-marker-covector-proof-or-boundary-flux-source-acquisition.md",
            "role": "representation/covector no-marker theorem shape",
            "needle": "NLM975_7_verdict",
        },
        {
            "source_id": "413_doc",
            "path": "413-no-marker-parent-action-theorem-attempt.md",
            "role": "fixed spurion excluded but co-moving marker survives",
            "needle": "co_moving_marker_test",
        },
        {
            "source_id": "414_doc",
            "path": "414-local-quotient-invariant-algebra-triviality-gate.md",
            "role": "local invariant algebra triviality burden",
            "needle": "strong_local_triviality",
        },
        {
            "source_id": "573_doc",
            "path": "573-Y5-R10-primitive-minimal-no-natural-marker-theorem-or-finite-envelope.md",
            "role": "primitive-minimal reduction to invariant algebra triviality",
            "needle": "PM573_3_local_invariant_algebra",
        },
        {
            "source_id": "573_chain",
            "path": "source-intake/mts_residuals/P8_Y5_R10_573_NO_MARKER_REDUCTION_CHAIN.csv",
            "role": "no-marker reduction chain",
            "needle": "RC573_2_no_marker_functor",
        },
        {
            "source_id": "573_debt",
            "path": "source-intake/mts_residuals/P8_Y5_R10_573_INVARIANT_GENERATOR_DEBT.csv",
            "role": "surviving invariant generator debts",
            "needle": "IG573_4_species_constants",
        },
        {
            "source_id": "575_constant_lock",
            "path": "source-intake/mts_residuals/P8_Y5_R10_575_CONSTANT_SOURCE_LOCK_CONTRACT.csv",
            "role": "constant/source lock requirements",
            "needle": "CL575_1_trivial_MTS_action",
        },
        {
            "source_id": "448_doc",
            "path": "448-constant-sector-universality-theorem-attempt.md",
            "role": "theta_A(I_Q) counterexample",
            "needle": "theta_A(I_Q)",
        },
        {
            "source_id": "622_doc",
            "path": "622-Y5-R10-parent-matter-sector-contract-or-residual-prior-runner.md",
            "role": "parent matter sector contract and residual-prior runner",
            "needle": "PMC622_4_constant_superselection",
        },
        {
            "source_id": "417_boundary",
            "path": "417-boundary-exchange-nohair-theorem-attempt.md",
            "role": "alpha3/Gdot finite fallback anchors",
            "needle": "alpha3_flux",
        },
    ]
    rows: list[dict[str, str]] = []
    for spec in specs:
        path = source_path(spec["path"])
        text = read_text(path)
        rows.append(
            {
                **spec,
                "absolute_path": str(path),
                "exists": flag(path.exists()),
                "needle_found": flag(spec["needle"] in text),
                "generated_utc": stamp(),
            }
        )
    return rows


def theorem_attempt_rows() -> list[dict[str, str]]:
    return [
        {
            "attempt_id": "NMF980_0_target_statement",
            "statement": "Every admissible local MTS/quotient/material observable functor to global sector labels is constant.",
            "math_form": "Hom_nat(A_loc^MTS, Sigma_const)=Const",
            "result": "THEOREM_TARGET",
            "proof_or_obstruction": "would close the no-marker clause in 979 and support b_theta=b_kappa=0",
            "claim_effect": "none_yet",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "NMF980_1_fixed_spurion_exclusion",
            "statement": "Fixed labelled spurions are not parent quotient functions.",
            "math_form": "s_fixed notin O(Q_parent) if it is not orbit-constant",
            "result": "CONDITIONAL_PASS",
            "proof_or_obstruction": "strict quotient logic excludes fixed external masks once the quotient parent domain is signed",
            "claim_effect": "kills only fixed spurions, not co-moving markers",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "NMF980_2_scalar_obstruction_lemma",
            "statement": "Any surviving nonconstant local invariant scalar can select a continuous sector label.",
            "math_form": "if I in A_loc, dI != 0 and Sigma has an R-like coordinate s, then s=s0+epsilon I gives a nonconstant functor",
            "result": "OBSTRUCTION_PROVED",
            "proof_or_obstruction": "composition with a nonconstant invariant scalar is natural/quotient-compatible unless the parent forbids the target action",
            "claim_effect": "full no-marker functor theorem fails in the current corpus",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "NMF980_3_discrete_connected_branch_lemma",
            "statement": "Discrete sector labels can be forced constant only on connected/idempotent-free local branches.",
            "math_form": "continuous f: connected local branch -> discrete Sigma is constant; idempotents/domain selectors reopen f",
            "result": "HELPFUL_CONDITIONAL_LEMMA",
            "proof_or_obstruction": "this may protect representation species labels, but not continuous constants like alpha, masses, or kappa",
            "claim_effect": "suggests a narrower future proof route",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "NMF980_4_co_moving_marker_extension",
            "statement": "A co-moving material marker extends the quotient and survives quotient invariance.",
            "math_form": "Q_tilde=(Q_MTS,m)/G_rel; theta_A=theta_A(m) or kappa=kappa(m)",
            "result": "COUNTEREXAMPLE_SURVIVES",
            "proof_or_obstruction": "primitive minimality/no-extension is a contract, not yet a theorem",
            "claim_effect": "blocks no-marker promotion",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "NMF980_5_continuous_constant_sector",
            "statement": "Matter constants and gravitational coupling live in continuous target spaces.",
            "math_form": "theta_A in R^n, kappa in R_+; nonconstant I can feed theta_A(I) or kappa(I)",
            "result": "COUNTEREXAMPLE_SURVIVES",
            "proof_or_obstruction": "discrete-label connectedness cannot protect continuous numerical constants",
            "claim_effect": "b_theta and b_kappa finite priors remain live",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "NMF980_6_topological_kappa_limit",
            "statement": "Topological d kappa=0 kills local gradients but not all sector-selection/source-universality risks.",
            "math_form": "d kappa=0 on connected domains, while kappa_A or class-selected constant kappa remains possible without one-kappa/no-marker clauses",
            "result": "PARTIAL_PROTECTION_ONLY",
            "proof_or_obstruction": "gradient-zero and universality-zero are different statements",
            "claim_effect": "Gdot-like drift can be targeted, but WEP/source splitting remains unclosed",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "NMF980_7_verdict",
            "statement": "No-marker sector functor theorem status.",
            "math_form": "Hom_nat(A_loc^MTS,Sigma_const)=Const is false unless invariant algebra triviality plus no-extension/discrete-connectedness are parent-derived",
            "result": "NO_MARKER_FUNCTOR_REJECTED_CURRENT_CORPUS_REDUCED_TO_TRIVIALITY_OR_DISCRETE_CONNECTED_BRANCH",
            "proof_or_obstruction": "980 proves the obstruction clearly: one untrivialized invariant scalar is enough to build the forbidden functor",
            "claim_effect": "do not retire finite qbar/coupling priors",
            "valid_for_claim": "false",
        },
    ]


def counterexample_rows() -> list[dict[str, str]]:
    return [
        {
            "counterexample_id": "CEX980_0_theta_IQ",
            "form": "theta_A = theta_A(I_Q)",
            "source": "448-constant-sector-universality-theorem-attempt.md",
            "why_allowed": "I_Q is quotient-invariant, so quotient invariance alone does not force theta_A constant",
            "blocked_by": "local invariant algebra triviality plus trivial action on constants",
            "status": "active",
        },
        {
            "counterexample_id": "CEX980_1_theta_material_marker",
            "form": "theta_A = theta_A(m)",
            "source": "413/573 no-marker attempts",
            "why_allowed": "co-moving marker extension can descend to an extended quotient",
            "blocked_by": "primitive no-extension theorem",
            "status": "active",
        },
        {
            "counterexample_id": "CEX980_2_species_kappa",
            "form": "E_munu = sum_A kappa_A T_A_munu",
            "source": "979 and 575 coupling/source lock",
            "why_allowed": "constant kappa_A can satisfy local gradient tests while violating universal source coupling",
            "blocked_by": "one shared gravitational kappa sector plus universal Hilbert source theorem",
            "status": "active",
        },
        {
            "counterexample_id": "CEX980_3_domain_selector",
            "form": "sector label selected by chi_D or relative domain class",
            "source": "414/573 invariant generator debt",
            "why_allowed": "domain/class selectors remain untrivialized local invariant generators",
            "blocked_by": "connected/idempotent-free local branch or fixed-class closure explicitly labelled as closure",
            "status": "active",
        },
        {
            "counterexample_id": "CEX980_4_memory_class_scalar",
            "form": "theta_A or kappa depends on memory/class scalar",
            "source": "573 invariant generator debt",
            "why_allowed": "memory/class scalar is not silenced as a theorem",
            "blocked_by": "local value and gradient zero theorem or sourced finite residual",
            "status": "active",
        },
        {
            "counterexample_id": "CEX980_5_post_readout_projector",
            "form": "sector chosen by readout/reduced-action projector",
            "source": "622 branch purity and 975 readout lock",
            "why_allowed": "only excluded if readout-after-variation is enforced as parent-domain absence",
            "blocked_by": "parent variation before readout plus no post-readout EFT backreaction",
            "status": "conditionally_blocked_policy_only",
        },
        {
            "counterexample_id": "CEX980_6_boundary_flux",
            "form": "boundary/local projection source survives outside the sector functor argument",
            "source": "417 boundary alpha3/Gdot anchors",
            "why_allowed": "not exactly a sector-label functor, but still sources local residuals",
            "blocked_by": "boundary no-hair or sourced K_boundary_alpha3 bound",
            "status": "active",
        },
    ]


def target_classification_rows() -> list[dict[str, str]]:
    return [
        {
            "target_id": "TGT980_0_numeric_matter_constants",
            "sector_target": "alpha_EM, mass ratios, charges, theta_A numeric constants",
            "target_type": "continuous",
            "discrete_connected_lemma_helps": "false",
            "remaining_requirement": "trivial MTS action on representation constants",
        },
        {
            "target_id": "TGT980_1_gravitational_kappa",
            "sector_target": "kappa/G_eff coupling",
            "target_type": "continuous_positive",
            "discrete_connected_lemma_helps": "false",
            "remaining_requirement": "one shared kappa plus topological d kappa=0 plus source calibration",
        },
        {
            "target_id": "TGT980_2_species_representation_label",
            "sector_target": "species/representation family label",
            "target_type": "discrete",
            "discrete_connected_lemma_helps": "true_if_connected_idempotent_free",
            "remaining_requirement": "local branch connectedness and no domain/projector idempotents",
        },
        {
            "target_id": "TGT980_3_domain_boundary_class",
            "sector_target": "domain class, boundary class, chi_D",
            "target_type": "discrete_or_finite_projector",
            "discrete_connected_lemma_helps": "only_if_no_idempotents",
            "remaining_requirement": "domain selector as gauge/readout-only or fixed-class closure",
        },
        {
            "target_id": "TGT980_4_readout_projectors",
            "sector_target": "post-readout projector/mask",
            "target_type": "idempotent",
            "discrete_connected_lemma_helps": "false_if_projector_is_varied",
            "remaining_requirement": "readout after variation; no reduced action backreaction",
        },
    ]


def finite_prior_fallback_rows() -> list[dict[str, str]]:
    return [
        {
            "fallback_id": "FP980_0_b_kappa_species_split",
            "parameter": "species_source_weight_splitting",
            "component": "b_kappa",
            "source_status": "needs_external_bound_or_parent_universal_source_theorem",
            "local_anchor": "979 priority row QPRI979_0",
            "valid_for_claim": "false",
        },
        {
            "fallback_id": "FP980_1_Gdot_drift",
            "parameter": "d_ln_Geff_dt_or_dX",
            "component": "b_kappa",
            "source_status": "local_anchor_needs_source_hardening",
            "local_anchor": "417 row Gdot_drift = 9.600e-15 yr^-1",
            "valid_for_claim": "false",
        },
        {
            "fallback_id": "FP980_2_K_boundary_alpha3",
            "parameter": "K_boundary_alpha3",
            "component": "boundary_alpha3_flux",
            "source_status": "local_anchor_needs_source_hardening",
            "local_anchor": "417 row alpha3_flux = 4.000e-20",
            "valid_for_claim": "false",
        },
        {
            "fallback_id": "FP980_3_b_theta_alpha_mass",
            "parameter": "d_ln_alpha_EM_dXhat and d_ln_mass_ratio_dXhat",
            "component": "b_theta",
            "source_status": "needs_clock_EM_source_or_parent_constant_theorem",
            "local_anchor": "448/575/979 theta_A counterexamples",
            "valid_for_claim": "false",
        },
        {
            "fallback_id": "FP980_4_qbarXT_R10",
            "parameter": "P_A_qbarXT_vec with K_X Qbar_XH lambda_X",
            "component": "qbarXT_vec",
            "source_status": "needs parent coefficients and real alpha(lambda) bound curve",
            "local_anchor": "576/978 finite qbar runner rows",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE980_0_no_marker_functor",
            "claim": "Hom_nat(A_loc^MTS,Sigma_const)=Const is proven",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "scalar obstruction lemma plus active generator debts show the theorem is not true for the current corpus",
        },
        {
            "gate_id": "CGATE980_1_btheta_bkappa_zero",
            "claim": "b_theta and b_kappa can be set to theorem-zero",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "continuous target constants remain vulnerable to theta_A(I), kappa(I), and kappa_A",
        },
        {
            "gate_id": "CGATE980_2_qbar_rows_retired",
            "claim": "finite qbar/coupling prior rows can be retired",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "finite prior fallback rows stay active",
        },
        {
            "gate_id": "CGATE980_3_local_GR",
            "claim": "local GR/Newton/PPN/R10 branch passes",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "no-marker theorem fails and boundary/source priors are not sourced",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC980_0_main",
            "topic": "no-marker sector functor",
            "result": "rejected_as_full_current_theorem",
            "reason": "any surviving nonconstant invariant scalar can define a nonconstant functor into continuous sector labels",
            "next_action": "split the problem into continuous constants, discrete representation labels, and boundary/projector idempotents",
        },
        {
            "decision_id": "DEC980_1_positive_progress",
            "topic": "narrow proof route",
            "result": "discrete_connected_branch_lemma_available",
            "reason": "discrete labels can be constant on connected/idempotent-free branches",
            "next_action": "use this only for representation/domain labels, not numeric constants",
        },
        {
            "decision_id": "DEC980_2_empirical_fallback",
            "topic": "finite priors",
            "result": "source_acquisition_now_needed_for_continuous_constants",
            "reason": "continuous b_theta/b_kappa/qbar channels cannot be theorem-zeroed yet",
            "next_action": "source b_kappa/Gdot/alpha3 first because those hit local-GR viability hardest",
        },
        {
            "decision_id": "DEC980_3_best_next",
            "topic": "next checkpoint",
            "result": "continuous_constant_prior_source_or_discrete_branch_connectedness",
            "reason": "the theorem failed globally, so either bound continuous constants or prove the discrete branch lemma where it actually applies",
            "next_action": "write 981 finite coupling-prior source acquisition for b_kappa/Gdot/alpha3, with no claims",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "981-Y5-R10-finite-coupling-prior-source-acquisition-bkappa-Gdot-alpha3.md",
            "objective": "source and harden the first finite local coupling priors for b_kappa, Gdot, and alpha3 after the no-marker functor theorem fails globally",
            "include": "source-backed bound strings, local-anchor reconciliation, valid_for_claim=false until provenance/numeric units pass, no local-GR promotion",
            "exclude": "invented bounds, qbar theorem-zero, public claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
        }
    ]


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    start_ts = SCRIPT_START_UTC.timestamp()
    for dirpath, _, filenames in os.walk(FORMALIZATION):
        for filename in filenames:
            path = Path(dirpath) / filename
            try:
                if path.stat().st_mtime > start_ts:
                    count += 1
            except OSError:
                count += 1
    return count


def validation_rows(
    sources: list[dict[str, str]],
    theorem: list[dict[str, str]],
    counterexamples: list[dict[str, str]],
    targets: list[dict[str, str]],
    fallback: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    source_paths_ok = all(row["exists"] == "true" for row in sources)
    source_needles_ok = all(row["needle_found"] == "true" for row in sources)
    obstruction_ok = any(
        row["attempt_id"] == "NMF980_2_scalar_obstruction_lemma"
        and row["result"] == "OBSTRUCTION_PROVED"
        for row in theorem
    )
    verdict_ok = any(
        row["attempt_id"] == "NMF980_7_verdict"
        and row["result"] == "NO_MARKER_FUNCTOR_REJECTED_CURRENT_CORPUS_REDUCED_TO_TRIVIALITY_OR_DISCRETE_CONNECTED_BRANCH"
        for row in theorem
    )
    active_counterexamples_ok = any(row["status"] == "active" for row in counterexamples)
    continuous_targets_ok = any(
        row["target_type"].startswith("continuous")
        and row["discrete_connected_lemma_helps"] == "false"
        for row in targets
    )
    fallback_ok = all(row["valid_for_claim"] == "false" for row in fallback)
    claims_ok = all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claims)
    decisions_ok = any(
        row["decision_id"] == "DEC980_3_best_next"
        and row["result"] == "continuous_constant_prior_source_or_discrete_branch_connectedness"
        for row in decisions
    )
    next_ok = bool(next_target) and next_target[0]["valid_for_claim"] == "false"
    formalization_count = formalization_changed_after_start()
    checks = [
        {
            "check_id": "V980_0_source_paths_exist",
            "result": "pass" if source_paths_ok else "fail",
            "detail": "all cited local source paths exist" if source_paths_ok else "one or more cited local source paths are missing",
        },
        {
            "check_id": "V980_1_source_needles_found",
            "result": "pass" if source_needles_ok else "fail",
            "detail": "all source needles found" if source_needles_ok else "one or more source needles are missing",
        },
        {
            "check_id": "V980_2_scalar_obstruction_proved",
            "result": "pass" if obstruction_ok else "fail",
            "detail": "nonconstant invariant scalar obstruction is recorded",
        },
        {
            "check_id": "V980_3_no_marker_verdict_nonclaim",
            "result": "pass" if verdict_ok else "fail",
            "detail": "no-marker functor theorem is rejected for current corpus, not promoted",
        },
        {
            "check_id": "V980_4_counterexamples_active",
            "result": "pass" if active_counterexamples_ok else "fail",
            "detail": "active counterexample ledger remains visible",
        },
        {
            "check_id": "V980_5_continuous_targets_classified",
            "result": "pass" if continuous_targets_ok else "fail",
            "detail": "continuous theta/kappa targets are separated from discrete-label branch",
        },
        {
            "check_id": "V980_6_fallback_rows_nonclaim",
            "result": "pass" if fallback_ok else "fail",
            "detail": "all finite-prior fallback rows remain nonclaim",
        },
        {
            "check_id": "V980_7_claim_gates_false",
            "result": "pass" if claims_ok else "fail",
            "detail": "all theorem-zero/local-GR claims remain blocked",
        },
        {
            "check_id": "V980_8_decision_next_target",
            "result": "pass" if decisions_ok else "fail",
            "detail": "981 finite coupling-prior source acquisition selected",
        },
        {
            "check_id": "V980_9_next_target_written",
            "result": "pass" if next_ok else "fail",
            "detail": "next target row is present and nonclaim",
        },
        {
            "check_id": "V980_10_formalization_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization-workbench modified-file count since script start is {formalization_count}",
        },
    ]
    ready = all(row["result"] == "pass" for row in checks)
    return [
        {**row, "generated_utc": stamp()}
        for row in checks
    ] + [
        {
            "check_id": "V980_READY",
            "result": "pass" if ready else "fail",
            "detail": "980 checkpoint pack validation summary",
            "generated_utc": stamp(),
        }
    ]


def write_doc(
    sources: list[dict[str, str]],
    theorem: list[dict[str, str]],
    counterexamples: list[dict[str, str]],
    targets: list[dict[str, str]],
    fallback: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> None:
    lines = [
        "# 980 Y5 R10: No-Marker Sector Functor Theorem Or First Qbar Source Acquisition",
        "",
        "Status: `Y5_R10_980_no_marker_sector_functor_rejected_for_current_corpus_scalar_obstruction_proved_finite_coupling_priors_retained`",
        "",
        "Claim ceiling: no no-marker theorem, no `b_theta=0`, no `b_kappa=0`, no `qbar_XT=0`, no R10/WEP/PPN/local-GR pass, and no GitHub/public claim.",
        "",
        "## Readout",
        "",
        "980 is the honest fork. The desired theorem was:",
        "",
        "`Hom_nat(A_loc^MTS, Sigma_const)=Const`.",
        "",
        "That theorem is not true for the current corpus. The obstruction is simple and sharp: if the local invariant algebra contains any surviving nonconstant scalar `I`, and the sector target has a continuous coordinate such as `theta_A` or `kappa`, then `s=s0+epsilon I` is a nonconstant quotient-compatible sector selector unless the parent action explicitly forbids it.",
        "",
        "This is not bad news in the useless sense. It tells us exactly what is missing. The no-marker route reduces to either local invariant algebra triviality, or a narrower discrete connected-branch theorem for genuinely discrete labels. Continuous constants still need either a parent trivial-action theorem or sourced finite priors.",
        "",
        "## Source Register",
        "",
        md_table(sources, ["source_id", "role", "exists", "needle_found", "path"]),
        "",
        "## No-Marker Functor Attempt",
        "",
        md_table(theorem, ["attempt_id", "statement", "result", "proof_or_obstruction", "claim_effect", "valid_for_claim"]),
        "",
        "## Counterexample Ledger",
        "",
        md_table(counterexamples, ["counterexample_id", "form", "why_allowed", "blocked_by", "status"]),
        "",
        "## Sector Target Classification",
        "",
        md_table(targets, ["target_id", "sector_target", "target_type", "discrete_connected_lemma_helps", "remaining_requirement"]),
        "",
        "## Finite Prior Fallback",
        "",
        md_table(fallback, ["fallback_id", "parameter", "component", "source_status", "local_anchor", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        md_table(claims, ["gate_id", "claim", "gate_pass", "claim_allowed", "why_not"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decisions, ["decision_id", "topic", "result", "reason", "next_action"]),
        "",
        "## Validation",
        "",
        md_table(validation, ["check_id", "result", "detail", "generated_utc"]),
        "",
        "## Next Target",
        "",
        md_table(next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register()
    theorem = theorem_attempt_rows()
    counterexamples = counterexample_rows()
    targets = target_classification_rows()
    fallback = finite_prior_fallback_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, theorem, counterexamples, targets, fallback, claims, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_980_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_980_NO_MARKER_FUNCTOR_THEOREM_ATTEMPT.csv", theorem)
    write_csv(OUT / "P8_Y5_R10_980_COUNTEREXAMPLE_LEDGER.csv", counterexamples)
    write_csv(OUT / "P8_Y5_R10_980_SECTOR_TARGET_CLASSIFICATION.csv", targets)
    write_csv(OUT / "P8_Y5_R10_980_FINITE_PRIOR_FALLBACK.csv", fallback)
    write_csv(OUT / "P8_Y5_R10_980_CLAIM_GATE.csv", claims)
    write_csv(OUT / "P8_Y5_R10_980_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_980_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_980_VALIDATION.csv", validation)
    write_doc(sources, theorem, counterexamples, targets, fallback, claims, decisions, validation, next_target)


if __name__ == "__main__":
    main()

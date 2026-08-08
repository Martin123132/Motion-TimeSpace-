from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_parent_action_coupling_lock_conditional_theorem_written_Rsrc_zero_contract_unfilled_nonclaim"
CLAIM_CEILING = "parent_action_coupling_lock_contract_only_no_epsilon_G_zero_no_Rsrc_zero_no_Delta_Poisson_fill_no_Newton_no_PPN_no_R10_no_local_GR_claim"
NEXT_TARGET = "704-Y5-R10-EH-prefactor-constant-theorem-or-kappa-gradient-bound.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "703-Y5-R10-parent-action-coupling-lock-or-Rsrc-channel-zero-theorem.md"
FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

OUTPUT_PATHS = [
    DOC_PATH,
    RESIDUALS / "P8_Y5_R10_703_SOURCE_REGISTER.csv",
    RESIDUALS / "P8_Y5_R10_703_PARENT_ACTION_COUPLING_LOCK_AUDIT.csv",
    RESIDUALS / "P8_Y5_R10_703_ACTION_VARIATION_CONTRACT.csv",
    RESIDUALS / "P8_Y5_R10_703_RSRC_ZERO_THEOREM_AUDIT.csv",
    RESIDUALS / "P8_Y5_R10_703_DELTA_POISSON_UPDATE_ROW.csv",
    RESIDUALS / "P8_Y5_R10_703_EVALUATOR.csv",
    RESIDUALS / "P8_Y5_R10_703_CLAIM_GATE_EVALUATION.csv",
    RESIDUALS / "P8_Y5_R10_703_DECISION.csv",
    RESIDUALS / "P8_Y5_R10_703_NONCLAIM_SUMMARY.csv",
    RESIDUALS / "P8_Y5_BRR545_703_VALIDATION.csv",
]

SOURCE_PATHS = {
    "402_doc": ROOT / "402-EH-source-normalization-parent-pair.md",
    "424_doc": ROOT / "424-same-frame-EH-source-Poisson-reduction-gate.md",
    "429_doc": ROOT / "429-Ward-Bianchi-exchange-owner-for-Poisson-source.md",
    "440_doc": ROOT / "440-metric-only-second-order-sector-reduction-attempt.md",
    "443_doc": ROOT / "443-metric-compatibility-Levi-Civita-or-R11-connection-row.md",
    "523_doc": ROOT / "523-Y5-Gauss-orbital-calibration-or-source-normalization-residual-score.md",
    "529_doc": ROOT / "529-Y5-source-calibrated-EH-family-proof-stack-or-R11-beta-fill.md",
    "652_doc": ROOT / "652-Y5-R10-WEP-source-normalization-or-common-geometry-zero-theorem.md",
    "653_doc": ROOT / "653-Y5-R10-parent-matter-functor-signature-or-WEP-closure-demotion.md",
    "655_doc": ROOT / "655-Y5-R10-EH-operator-selection-under-WEP-closure-or-retained-R11-vector.md",
    "657_doc": ROOT / "657-Y5-R10-source-normalization-family-first-real-R11-fill.md",
    "696_doc": ROOT / "696-Y5-R10-MHref-same-frame-denominator-or-BTF-product-bound-guard.md",
    "701_doc": ROOT / "701-Y5-R10-Delta-Poisson-source-coefficient-fill-or-Gauss-orbit-bridge.md",
    "702_doc": ROOT / "702-Y5-R10-kappa-Gref-source-residual-coefficient-fill.md",
    "702_validation": RESIDUALS / "P8_Y5_BRR545_702_VALIDATION.csv",
    "702_kappa_lock": RESIDUALS / "P8_Y5_R10_702_KAPPA_GREF_LOCK_AUDIT.csv",
    "702_rsrc": RESIDUALS / "P8_Y5_R10_702_RSRC_CHANNEL_DECOMPOSITION.csv",
    "702_delta": RESIDUALS / "P8_Y5_R10_702_DELTA_POISSON_CANDIDATE_FILL.csv",
    "702_rhoh": RESIDUALS / "P8_Y5_R10_702_RHOH_FRAME_NORMALIZATION_PACK.csv",
    "701_source_pack": RESIDUALS / "P8_Y5_R10_701_DELTA_POISSON_SOURCE_COEFFICIENT_PACK.csv",
    "700_parent": RESIDUALS / "P8_Y5_R10_700_PARENT_PREMISE_AUDIT.csv",
    "pg_contract": RESIDUALS / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
    "source_norm_scorecard": RESIDUALS / "P8_Y5_SOURCE_NORMALIZATION_RESIDUAL_SCORECARD.csv",
    "657_channels": RESIDUALS / "P8_Y5_R10_657_CMU_EIGHT_CHANNEL_VECTOR.csv",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def source_list(*source_ids: str) -> str:
    return ";".join(str(SOURCE_PATHS[source_id]) for source_id in source_ids)


def validation_failures(source_id: str) -> list[dict[str, str]]:
    path = SOURCE_PATHS[source_id]
    if not path.exists():
        return [{"check_id": "missing", "result": "fail", "detail": str(path)}]
    return [row for row in read_csv(path) if row.get("result") != "pass"]


def formalization_changed_count() -> int:
    if not FORMALIZATION_WORKBENCH.exists():
        return -1
    return sum(
        1
        for candidate in FORMALIZATION_WORKBENCH.rglob("*")
        if candidate.is_file() and datetime.fromtimestamp(candidate.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def source_register_rows() -> list[dict[str, str]]:
    generated = now()
    roles = {
        "402_doc": "EH/source-normalization parent pair",
        "424_doc": "same-frame EH-source Poisson reduction gate",
        "429_doc": "Ward/Bianchi exchange owner for source residual",
        "440_doc": "metric-only second-order sector reduction attempt",
        "443_doc": "metric compatibility/Levi-Civita connection gate",
        "523_doc": "Gauss/orbital calibration residual scorecard",
        "529_doc": "source-calibrated EH proof stack",
        "652_doc": "WEP/common-geometry source-normalization theorem attempt",
        "653_doc": "parent matter functor signature predecessor",
        "655_doc": "EH operator selection under WEP closure",
        "657_doc": "source-normalization family and R11 vector",
        "696_doc": "M_H_ref denominator blocker",
        "701_doc": "Delta_Poisson conditional zero theorem",
        "702_doc": "kappa/Gref and R_src coefficient contract",
        "702_validation": "702 validation gate",
        "702_kappa_lock": "702 kappa/Gref lock audit",
        "702_rsrc": "702 R_src channel decomposition",
        "702_delta": "702 Delta_Poisson candidate fill",
        "702_rhoh": "702 rho_H/frame normalization pack",
        "701_source_pack": "701 source-coefficient pack",
        "700_parent": "700 parent-premise audit",
        "pg_contract": "Hamiltonian charge to Poisson/Gauss calibration contract",
        "source_norm_scorecard": "source-normalization residual scorecard",
        "657_channels": "eight source-normalization residual channels",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": "true" if path.exists() else "false",
            "role": roles[source_id],
            "generated_utc": generated,
        }
        for source_id, path in SOURCE_PATHS.items()
    ]


def parent_action_lock_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "PAL703_0_target_action",
            "constant EH prefactor",
            "S_grav = (c^4/(16*pi*G_ref)) int sqrt(-g_obs) (R[g_obs]-2 Lambda)",
            "parent action contains this term in the observed frame with constant coefficient",
            "template_written_not_parent_extracted",
            "no epsilon_G claim",
            source_list("402_doc", "424_doc", "702_kappa_lock"),
        ),
        (
            "PAL703_1_no_variable_prefactor",
            "no F(chi)R or F(theta)R",
            "delta S/dg must not generate kappa_eff(x,A,lambda)=kappa_ref/F",
            "parent theorem that scalar/memory/selector fields do not multiply R locally",
            "not_parent_signed",
            "blocks constant coupling",
            source_list("440_doc", "655_doc", "657_doc"),
        ),
        (
            "PAL703_2_matter_functor",
            "same observed matter geometry",
            "S_m = S_m[Psi_A, g_obs, omega[g_obs], theta_A] with no species-dependent metric map",
            "parent matter functor signed for all species",
            "conditional_not_parent_signed",
            "blocks species/frame-blind source coupling",
            source_list("652_doc", "653_doc", "700_parent"),
        ),
        (
            "PAL703_3_connection_lock",
            "Levi-Civita compatibility",
            "omega = omega[g_obs] and nonmetric/torsion exchange vanishes or is retained",
            "metric compatibility theorem or R11 connection residual bound",
            "not_parent_signed",
            "blocks clean EH/source variation",
            source_list("443_doc", "429_doc", "655_doc"),
        ),
        (
            "PAL703_4_auxiliary_no_renormalization",
            "auxiliary sectors do not renormalize EH coefficient",
            "delta(S_aux)/delta g contributes to T_aux/R_src, not to the EH prefactor",
            "on-shell auxiliary descent plus no local R-prefactor theorem",
            "not_parent_signed",
            "moves auxiliary effects into R_src instead of epsilon_G only if proved",
            source_list("429_doc", "655_doc", "657_channels"),
        ),
        (
            "PAL703_5_boundary_counterterm_guard",
            "boundary/counterterm harmlessness",
            "boundary terms do not subtract physical source mass or shift G_ref",
            "boundary no-hair and counterterm convention guard",
            "not_parent_signed",
            "keeps M_H_ref/G_ref circularity active",
            source_list("523_doc", "696_doc"),
        ),
        (
            "PAL703_6_independent_Gref",
            "independent G_ref",
            "G_ref is fixed before and outside the same Gauss/orbit readout used to test the branch",
            "independent reference coupling or parent coefficient source",
            "MISSING_INDEPENDENT_GREF_SOURCE",
            "prevents circular measured-GM calibration",
            source_list("523_doc", "696_doc", "702_kappa_lock"),
        ),
        (
            "PAL703_7_conditional_theorem",
            "conditional coupling lock theorem",
            "PAL703_0..PAL703_6 imply epsilon_G=0 and kappa_eff=kappa_ref in the local branch",
            "all clauses signed by parent action",
            "proved_as_conditional_template",
            "useful theorem shape but no claim credit",
            source_list("402_doc", "424_doc", "702_doc"),
        ),
        (
            "PAL703_8_verdict",
            "parent-action coupling lock",
            "epsilon_G=0 from the MTS parent action",
            "constant EH prefactor, no variable prefactor, same matter functor, LC connection, auxiliary/boundary harmlessness, independent G_ref",
            "fail_current_corpus",
            "epsilon_G remains unfilled",
            source_list("702_doc", "702_kappa_lock"),
        ),
    ]
    return [
        {
            "lock_id": lock_id,
            "clause": clause,
            "mathematical_form": form,
            "required_evidence": evidence,
            "current_status": status,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": paths,
            "generated_utc": generated,
        }
        for lock_id, clause, form, evidence, status, effect, paths in rows
    ]


def action_variation_contract_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "AVC703_0_variation",
            "metric variation",
            "delta S_parent/delta g_obs -> G_munu + Lambda g_munu = kappa_ref (T_munu^H + T_munu^aux + T_munu^boundary)",
            "derive from explicit parent action",
            "MISSING_PARENT_ACTION_VARIATION",
        ),
        (
            "AVC703_1_identify_kappa_eff",
            "coefficient readout",
            "kappa_eff = kappa_ref only if all non-EH prefactor terms are absent",
            "extract local coefficient from variation",
            "MISSING_COEFFICIENT_EXTRACTOR",
        ),
        (
            "AVC703_2_move_extra_to_Rsrc",
            "source residual ownership",
            "R_src := P00[T_aux,T_boundary,nonEH,projector,domain,nonmetric,density]",
            "show extras enter residual channels, not hidden kappa",
            "MISSING_RSRC_OWNER_MAP",
        ),
        (
            "AVC703_3_no_cancellation",
            "no cancellation policy",
            "epsilon_G and epsilon_src must be bounded separately before summing Delta_Poisson",
            "separate source paths for coefficient and source channels",
            "POLICY_ACTIVE_NOT_A_CLAIM",
        ),
        (
            "AVC703_4_claim_ready_row",
            "claim-ready coefficient row",
            "epsilon_G=0 or epsilon_G<=bound with source path, units, and parent equation reference",
            "claim-ready coefficient source row",
            "MISSING_CLAIM_READY_EPSILON_G_ROW",
        ),
    ]
    return [
        {
            "contract_id": contract_id,
            "step": step,
            "mathematical_form": form,
            "required_evidence": evidence,
            "current_status": status,
            "valid_for_claim": "false",
            "source_paths": source_list("402_doc", "424_doc", "429_doc", "702_kappa_lock", "702_rsrc"),
            "generated_utc": generated,
        }
        for contract_id, step, form, evidence, status in rows
    ]


def rsrc_zero_theorem_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "RZT703_0_total",
            "R_src zero theorem",
            "R_src = div(E_nonEH)+T_obs grad(kappa_eff)+E_Z grad(Z)+F_projector+F_boundary+F_domain+F_nonmetric+R_rho = 0",
            "all child channels zero or bounded without cancellation",
            "fail_current_corpus",
            "epsilon_src remains unfilled",
            source_list("429_doc", "702_rsrc"),
        ),
        (
            "RZT703_1_kappa_gradient",
            "T_obs grad(kappa_eff)",
            "if PAL703 coupling lock holds, grad(kappa_eff)=0",
            "parent coupling lock or derivative bound",
            "conditional_on_PAL703",
            "blocked by epsilon_G",
            source_list("429_doc", "702_kappa_lock"),
        ),
        (
            "RZT703_2_nonEH_divergence",
            "div(E_nonEH)",
            "zero if local exterior is metric-only second-order EH and retained R11 vector vanishes",
            "EH-only sector reduction plus R11 coefficient zero theorem",
            "not_parent_signed",
            "operator residual remains",
            source_list("440_doc", "655_doc", "657_channels"),
        ),
        (
            "RZT703_3_auxiliary",
            "E_Z grad(Z)",
            "zero if auxiliary equations are on shell and local projection has no residual force",
            "auxiliary on-shell/projection silence theorem",
            "not_parent_signed",
            "auxiliary force remains",
            source_list("429_doc", "657_doc"),
        ),
        (
            "RZT703_4_projector_domain",
            "F_projector+F_domain",
            "zero if local projection commutes with variation/divergence and domain terms are topological or silent",
            "projector/domain commutator theorem",
            "not_parent_signed",
            "preferred-frame/location residual remains",
            source_list("429_doc", "523_doc", "655_doc"),
        ),
        (
            "RZT703_5_boundary",
            "F_boundary",
            "zero if boundary/counterterm convention has no local source flux or mass subtraction",
            "boundary no-hair/counterterm guard",
            "not_parent_signed",
            "boundary flux residual remains",
            source_list("523_doc", "696_doc"),
        ),
        (
            "RZT703_6_nonmetric",
            "F_nonmetric",
            "zero if matter and gravity use one Levi-Civita observed geometry",
            "same-frame matter functor plus Levi-Civita theorem",
            "not_parent_signed",
            "nonmetric exchange remains",
            source_list("424_doc", "443_doc", "653_doc"),
        ),
        (
            "RZT703_7_density",
            "R_rho",
            "zero if rho_eff=rho_H and pressure/stress corrections are retained or bounded",
            "Hilbert density descent and compact nonrelativistic source limit",
            "not_parent_signed",
            "rho_H normalization remains",
            source_list("529_doc", "652_doc", "702_rhoh"),
        ),
        (
            "RZT703_8_conditional_theorem",
            "conditional R_src theorem",
            "RZT703_1..RZT703_7 zero imply epsilon_src=0",
            "all child channels signed",
            "proved_as_conditional_template",
            "useful theorem shape but no claim credit",
            source_list("429_doc", "702_rsrc"),
        ),
    ]
    return [
        {
            "theorem_id": theorem_id,
            "channel": channel,
            "mathematical_form": form,
            "required_evidence": evidence,
            "current_status": status,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": paths,
            "generated_utc": generated,
        }
        for theorem_id, channel, form, evidence, status, effect, paths in rows
    ]


def delta_update_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "DPU703_0_epsilon_G",
            "epsilon_G",
            "PAL703_0..PAL703_6 => epsilon_G=0",
            "CONDITIONAL_THEOREM_ONLY",
            "not_parent_signed",
            "MISSING_PARENT_COUPLING_LOCK_SOURCE_PATH",
        ),
        (
            "DPU703_1_epsilon_src",
            "epsilon_src",
            "RZT703_1..RZT703_7 => epsilon_src=0",
            "CONDITIONAL_THEOREM_ONLY",
            "not_parent_signed",
            "MISSING_RSRC_ZERO_SOURCE_PATH",
        ),
        (
            "DPU703_2_Delta_Poisson",
            "Delta_Poisson",
            "Delta_Poisson <= epsilon_G + epsilon_src + epsilon_rho + epsilon_frame + epsilon_operator + epsilon_boundary",
            "MISSING_NUMERIC_EPSILON_VECTOR",
            "still_unfilled_after_703",
            "MISSING_CLAIM_READY_DELTA_POISSON_SOURCE_PATH",
        ),
        (
            "DPU703_3_first_actionable_fill",
            "first actionable fill",
            "either prove constant EH prefactor/no-variable-prefactor, or fill kappa-gradient/R_src channel bound",
            "MISSING_SUBPROOF",
            "handoff_to_704",
            "MISSING_704_SOURCE_PATH",
        ),
    ]
    return [
        {
            "update_id": update_id,
            "target": target,
            "formula": formula,
            "value_or_bound": value_or_bound,
            "current_status": status,
            "source_path": source_path,
            "valid_for_claim": "false",
            "source_paths": source_list("702_delta", "702_kappa_lock", "702_rsrc"),
            "generated_utc": generated,
        }
        for update_id, target, formula, value_or_bound, status, source_path in rows
    ]


def evaluator_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("EVAL703_0_parent_lock", "Can the parent action lock kappa_eff=8*pi*G_ref/c^4 now?", "Not yet. 703 writes the exact theorem, but the current corpus has not extracted the constant EH prefactor from a signed parent action.", "fail_blocked", NEXT_TARGET),
        ("EVAL703_1_Rsrc_zero", "Can R_src=0 be proved instead?", "Not yet. R_src zero is conditional on the same coupling lock plus nonEH, auxiliary, projector/domain, boundary, nonmetric, and density-normalization zero theorems.", "fail_blocked", NEXT_TARGET),
        ("EVAL703_2_best_next", "Best next subproblem?", "Go after the EH prefactor/no-variable-prefactor clause first; it kills both epsilon_G and the kappa-gradient source channel if it lands.", "route_selected", NEXT_TARGET),
    ]
    return [
        {
            "eval_id": eval_id,
            "question": question,
            "answer": answer,
            "result": result,
            "next_action": next_action,
            "valid_for_claim": "false",
            "source_paths": source_list("702_doc", "702_kappa_lock", "702_rsrc"),
            "generated_utc": generated,
        }
        for eval_id, question, answer, result, next_action in rows
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("CG703_0_sources", "all source files load", "source register exists check", "pass_structure", "allows checkpoint only"),
        ("CG703_1_prior_702", "702 validation clean", "702 validation has no failures", "pass_structure", "inherits clean predecessor"),
        ("CG703_2_parent_action_lock", "parent action coupling lock", "conditional theorem only; parent clauses unsigned", "fail_blocked", "no epsilon_G zero claim"),
        ("CG703_3_Rsrc_zero", "R_src zero theorem", "conditional theorem only; child channels unsigned", "fail_blocked", "no epsilon_src zero claim"),
        ("CG703_4_Delta_Poisson", "Delta_Poisson fill", "MISSING_NUMERIC_EPSILON_VECTOR", "fail_blocked", "no local Poisson claim"),
        ("CG703_5_Gauss_orbit", "Gauss/orbit promotion", "Delta_Poisson and M_H_ref still missing", "fail_blocked", "no Newton/orbit claim"),
        ("CG703_6_local_GR", "PPN/R10/local-GR promotion", "not reached", "fail_blocked", "no PPN/R10/local-GR claim"),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate": gate,
            "observed_state": observed,
            "result": result,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("702_validation", "702_kappa_lock", "702_rsrc", "702_delta"),
            "generated_utc": generated,
        }
        for gate_id, gate, observed, result, effect in rows
    ]


def decision_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("D703_0_parent_lock", "parent action coupling lock", "conditional_theorem_written", "the exact action clauses that imply epsilon_G=0 are now explicit", NEXT_TARGET),
        ("D703_1_Rsrc_zero", "R_src channel zero theorem", "conditional_theorem_written", "the exact child-channel clauses that imply epsilon_src=0 are now explicit", NEXT_TARGET),
        ("D703_2_claim_status", "claim promotion", "rejected", "neither theorem is parent-signed, so Delta_Poisson remains unfilled", NEXT_TARGET),
        ("D703_3_next", "next target", "selected", "EH prefactor/no-variable-prefactor is the highest leverage clause because it also kills T_obs grad(kappa_eff)", NEXT_TARGET),
    ]
    return [
        {
            "decision_id": decision_id,
            "target": target,
            "result": result,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": "false",
            "generated_utc": generated,
        }
        for decision_id, target, result, reason, next_action in rows
    ]


def summary_rows() -> list[dict[str, str]]:
    generated = now()
    return [
        {
            "summary_id": "S703_0",
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "the parent-action route is now an exact conditional theorem: constant EH prefactor plus no variable prefactor, same matter functor, LC connection, harmless auxiliary/boundary terms, and independent G_ref imply epsilon_G=0",
            "hardest_blocker": "the current corpus has not parent-signed the constant EH prefactor/no-variable-prefactor clause or the R_src child-channel zero theorems",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated,
        }
    ]


def has_missing_marker(row: dict[str, str]) -> bool:
    return "MISSING" in " ".join(str(value) for value in row.values())


def validation_rows(source_rows, parent_lock, variation, rsrc_zero, delta_update, evaluator, gates, decisions, summary):
    generated = now()
    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    prior_failures = len(validation_failures("702_validation"))
    kappa_rows = read_csv(SOURCE_PATHS["702_kappa_lock"])
    rsrc_rows = read_csv(SOURCE_PATHS["702_rsrc"])
    kappa_still_blocked = any(row.get("lock_id") == "KG702_6_verdict" and row.get("current_status") == "fail_current_corpus" for row in kappa_rows)
    rsrc_still_blocked = any(row.get("channel_id") == "RSRC702_8_verdict" and row.get("current_status") == "fail_current_corpus" for row in rsrc_rows)
    conditional_parent = any(row["lock_id"] == "PAL703_7_conditional_theorem" and row["current_status"] == "proved_as_conditional_template" for row in parent_lock)
    parent_verdict_blocks = any(row["lock_id"] == "PAL703_8_verdict" and row["current_status"] == "fail_current_corpus" for row in parent_lock)
    conditional_rsrc = any(row["theorem_id"] == "RZT703_8_conditional_theorem" and row["current_status"] == "proved_as_conditional_template" for row in rsrc_zero)
    rsrc_verdict_blocks = any(row["theorem_id"] == "RZT703_0_total" and row["current_status"] == "fail_current_corpus" for row in rsrc_zero)
    delta_unfilled = any(row["update_id"] == "DPU703_2_Delta_Poisson" and has_missing_marker(row) for row in delta_update)
    no_claim = all(
        row.get("valid_for_claim") != "true"
        for group in [parent_lock, variation, rsrc_zero, delta_update, evaluator, gates, decisions, summary]
        for row in group
    )
    gates_block = all(row["valid_for_claim"] == "false" for row in gates) and any(row["result"] == "fail_blocked" for row in gates)
    scoped = all(str(path).startswith(str(ROOT)) for path in OUTPUT_PATHS)
    formalization_count = formalization_changed_count()
    checks = [
        ("V703_0_source_paths_exist", not missing_sources, "all cited source paths exist" if not missing_sources else "missing=" + ";".join(missing_sources)),
        ("V703_1_prior_702_clean", prior_failures == 0, f"702_validation_failures={prior_failures}"),
        ("V703_2_702_kappa_still_blocked", kappa_still_blocked, "KG702 verdict remains fail_current_corpus"),
        ("V703_3_702_Rsrc_still_blocked", rsrc_still_blocked, "RSRC702 verdict remains fail_current_corpus"),
        ("V703_4_parent_conditional_theorem_written", conditional_parent, "PAL703 conditional theorem present"),
        ("V703_5_parent_lock_not_promoted", parent_verdict_blocks, "PAL703 verdict blocks claim"),
        ("V703_6_Rsrc_conditional_theorem_written", conditional_rsrc, "RZT703 conditional theorem present"),
        ("V703_7_Rsrc_zero_not_promoted", rsrc_verdict_blocks, "RZT703 total remains blocked"),
        ("V703_8_Delta_Poisson_update_unfilled", delta_unfilled, "Delta_Poisson update keeps MISSING markers"),
        ("V703_9_gates_block_claim", gates_block, f"gate_rows={len(gates)}"),
        ("V703_10_no_claim_rows_promoted", no_claim, "all generated rows valid_for_claim=false"),
        ("V703_11_next_target_selected", summary[0]["next_target"] == NEXT_TARGET and decisions[-1]["next_action"] == NEXT_TARGET, NEXT_TARGET),
        ("V703_12_outputs_scoped", scoped, "all outputs under post-checkpoint-work"),
        ("V703_13_formalization_workbench_untouched", formalization_count == 0, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V703_14_status_nonclaim", "no_epsilon_G_zero" in CLAIM_CEILING and "no_local_GR_claim" in CLAIM_CEILING, CLAIM_CEILING),
    ]
    return [{"check_id": cid, "result": "pass" if ok else "fail", "detail": detail, "generated_utc": generated} for cid, ok, detail in checks]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body]) + "\n"


def write_doc(source_rows, parent_lock, variation, rsrc_zero, delta_update, evaluator, gates, decisions, summary, validation) -> None:
    doc = f"""# 703 - Y5 R10 Parent Action Coupling Lock Or Rsrc Channel Zero Theorem

## Verdict

703 gets the parent-action contract into theorem form, but it does not promote the branch.

The clean theorem is:

```text
If the parent action contains a constant observed-frame EH prefactor
  S_grav = (c^4/(16*pi*G_ref)) int sqrt(-g_obs) (R[g_obs]-2 Lambda),
and no scalar/memory/selector field multiplies R,
and all matter uses the same observed geometry,
and the connection is Levi-Civita,
and auxiliary/boundary sectors do not renormalize the EH coefficient,
and G_ref is independent rather than orbit-defined,
then kappa_eff = 8*pi*G_ref/c^4 and epsilon_G = 0.
```

That is the right lock. The problem is that the current corpus has the lock shape, not the signed parent-action key. The fallback `R_src=0` route also becomes exact, but every child channel still needs its own zero theorem or bound.

So 703 is progress by compression: the coupling problem is now mostly an EH-prefactor/no-variable-prefactor problem plus the retained `R_src` channel family.

| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Parent Action Coupling Lock Audit

{markdown_table(parent_lock, ["lock_id", "clause", "current_status", "claim_effect", "valid_for_claim"])}

## Action Variation Contract

{markdown_table(variation, ["contract_id", "step", "current_status", "valid_for_claim"])}

## Rsrc Zero-Theorem Audit

{markdown_table(rsrc_zero, ["theorem_id", "channel", "current_status", "claim_effect", "valid_for_claim"])}

## Delta Poisson Update Row

{markdown_table(delta_update, ["update_id", "target", "value_or_bound", "current_status", "source_path", "valid_for_claim"])}

## Evaluator

{markdown_table(evaluator, ["eval_id", "question", "answer", "result", "next_action", "valid_for_claim"])}

## Claim Gate Evaluation

{markdown_table(gates, ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim"])}

## Decision

{markdown_table(decisions, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(summary, ["summary_id", "status", "claim_ceiling", "main_result", "hardest_blocker", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(source_rows, ["source_id", "path", "exists", "role"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    parent_lock = parent_action_lock_rows()
    variation = action_variation_contract_rows()
    rsrc_zero = rsrc_zero_theorem_rows()
    delta_update = delta_update_rows()
    evaluator = evaluator_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    summary = summary_rows()
    validation = validation_rows(source_rows, parent_lock, variation, rsrc_zero, delta_update, evaluator, gates, decisions, summary)

    write_csv(RESIDUALS / "P8_Y5_R10_703_SOURCE_REGISTER.csv", source_rows, ["source_id", "path", "exists", "role", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_703_PARENT_ACTION_COUPLING_LOCK_AUDIT.csv", parent_lock, ["lock_id", "clause", "mathematical_form", "required_evidence", "current_status", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_703_ACTION_VARIATION_CONTRACT.csv", variation, ["contract_id", "step", "mathematical_form", "required_evidence", "current_status", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_703_RSRC_ZERO_THEOREM_AUDIT.csv", rsrc_zero, ["theorem_id", "channel", "mathematical_form", "required_evidence", "current_status", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_703_DELTA_POISSON_UPDATE_ROW.csv", delta_update, ["update_id", "target", "formula", "value_or_bound", "current_status", "source_path", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_703_EVALUATOR.csv", evaluator, ["eval_id", "question", "answer", "result", "next_action", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_703_CLAIM_GATE_EVALUATION.csv", gates, ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_703_DECISION.csv", decisions, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_703_NONCLAIM_SUMMARY.csv", summary, ["summary_id", "status", "claim_ceiling", "main_result", "hardest_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_BRR545_703_VALIDATION.csv", validation, ["check_id", "result", "detail", "generated_utc"])
    write_doc(source_rows, parent_lock, variation, rsrc_zero, delta_update, evaluator, gates, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"parent_lock_rows={len(parent_lock)}")
    print(f"rsrc_zero_rows={len(rsrc_zero)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()

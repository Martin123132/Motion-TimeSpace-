from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3416-Y5-R2FR-parent-normal-form-EH-selector-and-hidden-stress-exclusion-under-AX1090.md"

SOURCES = {
    "doc_3415": ROOT / "3415-Y5-R2FR-v-source-square-and-Textra-safe-class-proof-under-AX1090.md",
    "obstructions_3415": OUT / "P8_Y5_R2FR_3415_PARENT_OWNERSHIP_OBSTRUCTIONS.csv",
    "textra_3415": OUT / "P8_Y5_R2FR_3415_TEXTRA_SAFE_CLASS_PROOF.csv",
    "gates_3415": OUT / "P8_Y5_R2FR_3415_PROMOTION_GATES.csv",
    "selector_3405": OUT / "P8_Y5_R2FR_3405_EH_SELECTOR_PROOF_ATTEMPT.csv",
    "selector_result_3405": OUT / "P8_Y5_R2FR_3405_SELECTOR_RESULT.csv",
    "bound_law_3405": OUT / "P8_Y5_R2FR_3405_DERIVATIVE_ORDER_BOUND_LAW.csv",
    "hessian_theorem_3406": OUT / "P8_Y5_R2FR_3406_MODE_RANK_THEOREM.csv",
    "hessian_status_3406": OUT / "P8_Y5_R2FR_3406_HESSIAN_INPUT_STATUS.csv",
    "mode_triage_3406": OUT / "P8_Y5_R2FR_3406_MODE_FAMILY_TRIAGE.csv",
    "hrj_candidate_3407": OUT / "P8_Y5_R2FR_3407_CANDIDATE_HRJ_SOURCE_TABLE.csv",
    "hrj_claim_3407": OUT / "P8_Y5_R2FR_3407_CLAIM_READY_HRJ_TABLE.csv",
    "missing_3407": OUT / "P8_Y5_R2FR_3407_MISSING_INPUT_QUEUE.csv",
    "gr_pole_3408": OUT / "P8_Y5_R2FR_3408_MINIMUM_GR_POLE_ROW.csv",
    "blockers_3408": OUT / "P8_Y5_R2FR_3408_CLAIM_BLOCKER_AUDIT.csv",
    "denominator_3409": OUT / "P8_Y5_R2FR_3409_GR_POLE_DENOMINATOR.csv",
    "nonEH_3409": OUT / "P8_Y5_R2FR_3409_NON_EH_RESIDUE_CHANNELS.csv",
    "impact_3409": OUT / "P8_Y5_R2FR_3409_LOCAL_GR_IMPACT.csv",
    "ward_3411": OUT / "P8_Y5_R2FR_3411_WARD_ZERO_THEOREM.csv",
    "stress_identity_3411": OUT / "P8_Y5_R2FR_3411_STRESS_IDENTITY_PROOF.csv",
    "em_hilbert_3382": OUT / "P8_Y5_R2FR_3382_EM_POYNTING_HILBERT_STRESS_CHAIN.csv",
    "maxwell_3339": OUT / "P8_Y5_R2FR_3339_MAXWELL_EM_STRESS_COUPLING_ROUTE.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3416_SOURCE_REGISTER.csv",
    "selector_synthesis": OUT / "P8_Y5_R2FR_3416_SELECTOR_SYNTHESIS.csv",
    "hidden_stress_exclusion_gate": OUT / "P8_Y5_R2FR_3416_HIDDEN_STRESS_EXCLUSION_GATE.csv",
    "eh_promotion_audit": OUT / "P8_Y5_R2FR_3416_EH_PROMOTION_AUDIT.csv",
    "residual_demotion_matrix": OUT / "P8_Y5_R2FR_3416_RESIDUAL_DEMOTION_MATRIX.csv",
    "local_gr_status": OUT / "P8_Y5_R2FR_3416_LOCAL_GR_STATUS.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3416_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3416_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3416_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3416_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3416_VALIDATION.csv",
}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    fields = list(rows[0].keys())

    def clean(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "/")

    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(clean(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def source_register() -> list[dict[str, Any]]:
    roles = {
        "doc_3415": "v/source-square and T_extra safe-class handoff selecting 3416",
        "obstructions_3415": "parent EH selector, hidden stress and q_loc vector obstructions",
        "textra_3415": "safe/residual stress classifier",
        "gates_3415": "local-GR promotion blocked by selector/stress/q_loc gates",
        "selector_3405": "two-derivative q-basic metric normal-form selector",
        "selector_result_3405": "exact conditional EH selector result and fallback bound law",
        "bound_law_3405": "derivative-order residual laws if selector fails",
        "hessian_theorem_3406": "field-redefinition invariant public pole/mode-rank theorem",
        "hessian_status_3406": "missing H_AB/R/J and boundary/gauge input status",
        "mode_triage_3406": "mode family triage by pole channel",
        "hrj_candidate_3407": "candidate H_AB/R/J source table",
        "hrj_claim_3407": "claim-ready H_AB/R/J table refusing promotion",
        "missing_3407": "minimal missing input queue",
        "gr_pole_3408": "minimum massless GR pole row",
        "blockers_3408": "claim blockers for minimum GR pole",
        "denominator_3409": "conditional GR pole denominator",
        "nonEH_3409": "non-EH residue channels relative to GR pole",
        "impact_3409": "local-GR impact and coupling target",
        "ward_3411": "q_loc Ward-zero theorem, conditional only",
        "stress_identity_3411": "q_loc as projected divergence of T_GK",
        "em_hilbert_3382": "public Maxwell/Poynting Hilbert stress chain",
        "maxwell_3339": "hidden Hodge/current residual guard",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[source_id],
            "valid_for_claim": False,
        }
        for source_id, path in SOURCES.items()
    ]


def selector_synthesis() -> list[dict[str, Any]]:
    return [
        {
            "synthesis_id": "SYN3416_0_exact_math_selector",
            "claim": "If MTS reduces locally to one q-basic two-derivative metric action with universal Hilbert source, the EH operator follows.",
            "derivation": "3405 derives the scalar-density normal form S_eff^{<=2}=int sqrt(-g)(C0+C1 R)+dB; variation gives EH+Lambda.",
            "current_result": "EXACT_CONDITIONAL_MATH",
            "blocks_now": False,
            "valid_for_claim": False,
        },
        {
            "synthesis_id": "SYN3416_1_spin2_equivalence",
            "claim": "The same selector can be phrased as massless spin-2 consistency.",
            "derivation": "If the public Hessian has only a positive massless TT pole and universal Hilbert source, spin-2 bootstrap gives the nonlinear EH completion.",
            "current_result": "EXACT_CONDITIONAL_IF_TT_ONLY_RANK",
            "blocks_now": False,
            "valid_for_claim": False,
        },
        {
            "synthesis_id": "SYN3416_2_public_pole_test",
            "claim": "The mode-rank question is field-redefinition invariant.",
            "derivation": "3406: the observable exchange is G_pub=R H^{-1} R^T; pole residues of this object, not variable names, decide extra modes.",
            "current_result": "PUBLIC_TEST_DERIVED",
            "blocks_now": False,
            "valid_for_claim": False,
        },
        {
            "synthesis_id": "SYN3416_3_minimum_GR_pole",
            "claim": "The minimum massless GR pole row is written.",
            "derivation": "3408 gives H_hh=(k^2/kappa0)P^(2), R_h=identity, J_h=1/2 T_total and kappa0=8*pi*G_ref/c^4.",
            "current_result": "EXACT_CONDITIONAL_MINIMUM_ROW_NOT_PARENT_SIGNED",
            "blocks_now": True,
            "valid_for_claim": False,
        },
        {
            "synthesis_id": "SYN3416_4_nonEH_survival",
            "claim": "The selector is not promoted unless non-EH poles are absent, topological, gapped/source-silent or bounded.",
            "derivation": "3409 lists scalar, massive-spin2, connection, vector, domain/memory/bulk, boundary/projector, source/readout and q_loc residue channels relative to D_GR.",
            "current_result": "RESIDUAL_BOUND_INTERFACE_REQUIRED",
            "blocks_now": True,
            "valid_for_claim": False,
        },
        {
            "synthesis_id": "SYN3416_5_current_verdict",
            "claim": "MTS has an exact conditional EH selector route but not a current local-GR derivation.",
            "derivation": "Math selector + minimum GR pole are conditional; H_AB/R/J parent entries, zero-mode/boundary class and hidden stress exclusion remain unsigned.",
            "current_result": "SELECTOR_DEMOTED_TO_EXACT_CONDITIONAL_PLUS_RESIDUAL_GATE",
            "blocks_now": True,
            "valid_for_claim": False,
        },
    ]


def hidden_stress_exclusion_gate() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "HSE3416_0_public_Hilbert",
            "stress_class": "ordinary matter/EM/Poynting/surface Hilbert stress",
            "exclusion_rule": "not excluded; it is included on the ordinary source side if varied from the same public g_obs action before readout",
            "safe_if": "same kappa_MTS, public Hodge/current, no hidden weights, no double-counted Poynting force",
            "current_status": "SAFE_CLASS_CONDITIONAL",
            "residual_if_fail": "hidden_Hodge_or_current_source_residual",
            "valid_for_claim": False,
        },
        {
            "gate_id": "HSE3416_1_vertical_gauge",
            "stress_class": "pure vertical/gauge hidden sector",
            "exclusion_rule": "if Lie_vertical g_obs=0 and the hidden sector is gauge/constraint with no q-basic metric variation, its Hilbert stress is zero or constraint-exact",
            "safe_if": "parent Hessian zero modes are classified as gauge and no boundary charge survives",
            "current_status": "ZERO_MODE_CLASS_OPEN",
            "residual_if_fail": "physical_hidden_zero_mode_stress",
            "valid_for_claim": False,
        },
        {
            "gate_id": "HSE3416_2_topological_boundary",
            "stress_class": "topological/improvement/boundary stress",
            "exclusion_rule": "safe only if exact/topological with zero compact linking charge and fixed source-blind boundary reference",
            "safe_if": "B_zero_flux=0, Delta_symp=0, delta_g H_ref=0",
            "current_status": "CONDITIONAL_STOKES_NOT_PARENT_SIGNED",
            "residual_if_fail": "boundary_projector_beta_alpha3_xi_residual",
            "valid_for_claim": False,
        },
        {
            "gate_id": "HSE3416_3_gapped_nohair",
            "stress_class": "massive/gapped auxiliary hidden sector",
            "exclusion_rule": "if H_XX has positive mass gap, J_X=0, R_X=0 or source-silent, and boundary flux vanishes, local exterior stress is zero/suppressed",
            "safe_if": "Z_X>0, M_X^2>0, H_hX controlled, J_X=0, R_X=0 or bounded",
            "current_status": "MISSING_PARENT_HX_RX_JX_INPUTS",
            "residual_if_fail": "extra_field_residue_B_X",
            "valid_for_claim": False,
        },
        {
            "gate_id": "HSE3416_4_hidden_constitutive",
            "stress_class": "hidden/domain/projector/constitutive stress",
            "exclusion_rule": "not excluded by Bianchi conservation; it must be theorem-zero, topological, source-silent or explicitly bounded",
            "safe_if": "none currently; needs parent zero or bound rows",
            "current_status": "RETAIN_AS_RESIDUAL",
            "residual_if_fail": "T_hidden_projector_constitutive_residual",
            "valid_for_claim": False,
        },
        {
            "gate_id": "HSE3416_5_q_loc_TGK",
            "stress_class": "q_loc/Gamma-Khat effective stress",
            "exclusion_rule": "safe only if T_GK is Hilbert-owned, Khat is metric response of Gamma_eff, Euler/boundary/projector gates close through O(U^2), and alpha-vector projections vanish or pass bounds",
            "safe_if": "3411 Ward theorem plus 3412/3413 symbol/response gates plus alpha-vector split all pass",
            "current_status": "CONDITIONAL_NOT_SAFE_CURRENTLY",
            "residual_if_fail": "B_q_loc_beta_alpha_vector",
            "valid_for_claim": False,
        },
        {
            "gate_id": "HSE3416_6_exclusion_verdict",
            "stress_class": "all hidden stress",
            "exclusion_rule": "hidden stress is excluded only class-by-class; no blanket Bianchi or covariance argument is accepted",
            "safe_if": "HSE3416_1 through HSE3416_5 are all passed or bounded",
            "current_status": "GLOBAL_HIDDEN_STRESS_EXCLUSION_FAILS",
            "residual_if_fail": "retain absolute no-cancellation stress envelope",
            "valid_for_claim": False,
        },
    ]


def eh_promotion_audit() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "EPA3416_0_selector_math",
            "requirement": "two-derivative metric normal form selects EH",
            "evidence": "3405 selector proof",
            "status": "PASS_EXACT_MATH",
            "claim_effect": "necessary but not sufficient",
            "valid_for_claim": False,
        },
        {
            "audit_id": "EPA3416_1_parent_mode_rank",
            "requirement": "only positive massless TT public pole survives at long range",
            "evidence": "3406 pole formula, 3407 candidate table",
            "status": "FAIL_HRJ_NOT_CLAIM_READY",
            "claim_effect": "EH selector not parent-signed",
            "valid_for_claim": False,
        },
        {
            "audit_id": "EPA3416_2_minimum_GR_pole",
            "requirement": "H_hh/R_h/J_h/common G_ref minimum row is parent-owned",
            "evidence": "3408 minimum GR pole row",
            "status": "PASS_CONDITIONAL_FAIL_PARENT_SIGNATURE",
            "claim_effect": "usable denominator only",
            "valid_for_claim": False,
        },
        {
            "audit_id": "EPA3416_3_nonEH_residues",
            "requirement": "all non-EH residues zero, safe, or bounded",
            "evidence": "3409 non-EH residue channels",
            "status": "FAIL_MISSING_NUMERIC_OR_ZERO_INPUTS",
            "claim_effect": "local-GR promotion blocked",
            "valid_for_claim": False,
        },
        {
            "audit_id": "EPA3416_4_hidden_stress",
            "requirement": "hidden/projector/constitutive stress excluded or bounded",
            "evidence": "3415/3416 stress classifier",
            "status": "FAIL_GLOBAL_EXCLUSION_NOT_PROVED",
            "claim_effect": "Y6 promotion blocked",
            "valid_for_claim": False,
        },
        {
            "audit_id": "EPA3416_5_q_loc_vector",
            "requirement": "q_loc beta projection separated from alpha_i/alpha3/xi",
            "evidence": "3409 q_loc warning, 3411 Ward theorem conditional",
            "status": "FAIL_VECTOR_PROJECTION_UNSIGNED",
            "claim_effect": "full PPN blocked",
            "valid_for_claim": False,
        },
    ]


def residual_demotion_matrix() -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "RDM3416_0_selector_abs",
            "quantity": "Delta_EH_selector_abs",
            "formula_or_rule": "absolute envelope over failure of q-basic two-derivative TT-only normal form",
            "trigger": "PNF3405_1/2 or HRJ claim table fails",
            "current_status": "ACTIVE_NONCLAIM_RESIDUAL",
            "next_input": "claim-ready H_AB/R/J or mode residues",
            "valid_for_claim": False,
        },
        {
            "residual_id": "RDM3416_1_nonEH_poles",
            "quantity": "sum_i |B_i/D_GR|",
            "formula_or_rule": "no-cancellation sum over scalar, massive-spin2, connection, vector, domain/memory/bulk, boundary/projector, source/readout and q_loc residues",
            "trigger": "non-EH pole or hidden source/readout overlap survives",
            "current_status": "BOUND_INTERFACE_READY_VALUES_MISSING",
            "next_input": "H_i,R_i,J_i,m_i,source overlap, arena projection",
            "valid_for_claim": False,
        },
        {
            "residual_id": "RDM3416_2_hidden_stress",
            "quantity": "T_hidden_abs",
            "formula_or_rule": "absolute Hilbert stress/source projection from hidden/projector/constitutive sectors not in safe classes",
            "trigger": "HSE3416 global exclusion fails",
            "current_status": "RETAINED_RESIDUAL",
            "next_input": "safe-class proof or stress coefficient/profile/bound",
            "valid_for_claim": False,
        },
        {
            "residual_id": "RDM3416_3_q_loc_vector",
            "quantity": "B_q_loc_beta_alpha_vector",
            "formula_or_rule": "separate q_loc beta/gamma and alpha1/alpha2/alpha3/xi projections before scoring",
            "trigger": "Ward-zero or projection split not signed",
            "current_status": "HIGH_PRIORITY_RESIDUAL",
            "next_input": "q_loc U2 profile and alpha-vector projection matrix",
            "valid_for_claim": False,
        },
        {
            "residual_id": "RDM3416_4_source_common_G",
            "quantity": "Delta_Gref_source_readout",
            "formula_or_rule": "mismatch among field kappa, Hilbert/PiM source, PPN U, orbital mu and EM source normalization",
            "trigger": "minimum GR pole common G_ref lock not parent-signed",
            "current_status": "CONDITIONAL_COUPLING_RESIDUAL",
            "next_input": "H_tau-H_ref=Pi_M J_H with fixed G_ref",
            "valid_for_claim": False,
        },
    ]


def local_gr_status() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "LGS3416_0_Newton",
            "sector": "Newtonian mechanics/source coupling",
            "current_best": "minimum GR pole and source-calibrated G_ref chain are exact conditional",
            "still_missing": "parent-signed source/readout/H_tau/Pi_M/common G_ref through O(U^2)",
            "verdict": "PROMISING_CONDITIONAL_NOT_CLAIM",
            "valid_for_claim": False,
        },
        {
            "status_id": "LGS3416_1_GR_metric_core",
            "sector": "local EH/GR metric core",
            "current_best": "two-derivative q-basic selector and massless pole denominator are written",
            "still_missing": "TT-only parent Hessian mode rank and non-EH residue zero/bounds",
            "verdict": "EXACT_CONDITIONAL_SELECTOR_NOT_PROMOTED",
            "valid_for_claim": False,
        },
        {
            "status_id": "LGS3416_2_beta",
            "sector": "PPN beta",
            "current_best": "a_v=0 and B_source=A_source^2 are exact conditional; reduced envelope exists",
            "still_missing": "PiM, boundary, readout, operator, coupling and q_loc lanes",
            "verdict": "PARTIALLY_DERIVED_RETAINED_LANES_BLOCK",
            "valid_for_claim": False,
        },
        {
            "status_id": "LGS3416_3_EM",
            "sector": "Maxwell/EM stress",
            "current_best": "public Maxwell/Poynting Hilbert stress is safe-class conditional",
            "still_missing": "public Hodge/current parent normalization and no hidden constitutive/source weights",
            "verdict": "COUPLING_ROUTE_CLEAN_IF_PUBLIC_HILBERT",
            "valid_for_claim": False,
        },
        {
            "status_id": "LGS3416_4_hidden_stress",
            "sector": "Y6 extra stress",
            "current_best": "safe-class taxonomy exists",
            "still_missing": "global proof all live hidden stress is safe or bounded",
            "verdict": "RETAINED_RESIDUAL",
            "valid_for_claim": False,
        },
        {
            "status_id": "LGS3416_5_full_PPN",
            "sector": "full PPN/local GR",
            "current_best": "route is precise: selector + source + stress + q_loc vector gates",
            "still_missing": "alpha_i/alpha3/xi/zeta/readout/source-residue gates",
            "verdict": "BLOCKED_BUT_SHARPLY_LOCALIZED",
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PG3416_0_selector_math",
            "gate": "EH selector math is derived under q-basic two-derivative metric normal form",
            "current_result": "PASS_EXACT_CONDITIONAL",
            "promotes_if": "not a claim gate",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3416_1_minimum_GR_pole",
            "gate": "minimum massless GR pole row is parent-signed",
            "current_result": "FAIL_NOT_PARENT_SIGNED",
            "promotes_if": "action reduction, readout identity, Hilbert+EM source, boundary/gauge class and G_ref lock all sign together",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3416_2_TT_only",
            "gate": "TT-only long-range public mode rank",
            "current_result": "FAIL_HRJ_RESIDUES_NOT_READY",
            "promotes_if": "G_pub pole test shows no scalar/vector/connection/domain residue or all are bounded",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3416_3_hidden_stress",
            "gate": "all hidden/projector/constitutive stresses excluded or bounded",
            "current_result": "FAIL_GLOBAL_HIDDEN_STRESS_EXCLUSION",
            "promotes_if": "each live stress is public Hilbert, Lambda, topological, no-hair, or bounded",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3416_4_residual_bounds",
            "gate": "non-EH residual bound pack is score-ready",
            "current_result": "FAIL_VALUES_MISSING",
            "promotes_if": "H_i/R_i/J_i/range/projection rows are source-backed and pass no-cancellation locks",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3416_5_local_GR",
            "gate": "local GR/Newton/Maxwell/PPN branch is derived",
            "current_result": "BLOCKED",
            "promotes_if": "PG3416_1 through PG3416_4 plus q_loc vector/full PPN gates pass",
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3416_0_real_progress",
            "finding": "The EH selector is no longer vague.",
            "reason": "3405-3408 provide exact conditional selector math, public pole criterion and a minimum GR pole row.",
            "next_action": "treat the GR pole as conditional denominator, not as a local-GR claim",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3416_1_selector_verdict",
            "finding": "The selector is not promoted at current corpus state.",
            "reason": "claim-ready H_AB/R/J table is false and hidden/non-EH residues are not zero/bounded.",
            "next_action": "either source HRJ rows or score residual bounds",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3416_2_hidden_stress",
            "finding": "Hidden stress cannot be erased by saying Bianchi.",
            "reason": "public Hilbert stress is safe; hidden/projector/constitutive stress is residual unless class-by-class safe.",
            "next_action": "carry hidden stress as absolute residual unless safe-class proof exists",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3416_3_best_next",
            "finding": "The next useful move is q_loc U2/alpha-vector plus retained residue bound pack.",
            "reason": "parent selector needs HRJ source rows, while q_loc has partial beta information and the clearest alpha3 danger.",
            "next_action": "build 3417 q_loc U2/alpha-vector and retained beta/stress bound pack",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3417-Y5-R2FR-q_loc-U2-alpha-vector-and-retained-beta-stress-bound-pack-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3417_q_loc_U2_alpha_vector_and_retained_beta_stress_bound_pack.py",
            "objective": "derive or bound q_loc U2 beta/gamma versus alpha1/alpha2/alpha3/xi projections and connect the result to retained beta/stress residue bounds relative to the conditional GR pole",
            "why_next": "3416 shows the EH selector is exact conditional but not promoted; q_loc is the highest-risk retained channel with partial beta data and severe preferred-frame warning",
            "valid_for_claim": False,
        },
        {
            "target_id": "3418-Y5-R2FR-HRJ-source-row-extraction-for-TT-only-selector-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3418_HRJ_source_row_extraction_for_TT_only_selector.py",
            "objective": "try to source the missing parent H_AB/R/J rows directly from core parent-action documents to promote or reject TT-only mode rank",
            "why_next": "this is the constructive selector route if q_loc projection work does not resolve the retained local branch",
            "valid_for_claim": False,
        },
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3416_0",
            "script": str(Path(__file__).resolve()),
            "claim_status": "SELECTOR_SYNTHESIS_AND_DEMOTION_GATE_ONLY",
            "main_result": "EH selector math and minimum GR pole are exact conditional; hidden stress exclusion fails globally; local GR remains blocked and residual gates are explicit.",
            "valid_for_claim": False,
        }
    ]


def validation_rows(generated: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = generated["source_register"]
    output_paths = list(OUTPUTS.values()) + [DOC]
    source_exists = all(str(row["exists"]).lower() == "true" for row in source_rows)
    no_workbench = all("formalization-workbench" not in str(path) for path in output_paths)
    all_nonclaim = all(
        str(row.get("valid_for_claim", "False")).lower() == "false"
        for rows in generated.values()
        for row in rows
    )
    selector_pass = any(
        row.get("synthesis_id") == "SYN3416_0_exact_math_selector"
        and row.get("current_result") == "EXACT_CONDITIONAL_MATH"
        for row in generated["selector_synthesis"]
    )
    minimum_nonclaim = any(
        row.get("synthesis_id") == "SYN3416_3_minimum_GR_pole"
        and row.get("current_result") == "EXACT_CONDITIONAL_MINIMUM_ROW_NOT_PARENT_SIGNED"
        for row in generated["selector_synthesis"]
    )
    hidden_fail = any(
        row.get("gate_id") == "HSE3416_6_exclusion_verdict"
        and row.get("current_status") == "GLOBAL_HIDDEN_STRESS_EXCLUSION_FAILS"
        for row in generated["hidden_stress_exclusion_gate"]
    )
    local_blocked = any(
        row.get("gate_id") == "PG3416_5_local_GR"
        and row.get("current_result") == "BLOCKED"
        for row in generated["promotion_gates"]
    )
    residuals = any(
        row.get("residual_id") == "RDM3416_1_nonEH_poles"
        and row.get("current_status") == "BOUND_INTERFACE_READY_VALUES_MISSING"
        for row in generated["residual_demotion_matrix"]
    )
    next_qloc = "q_loc-U2-alpha-vector" in generated["next_target"][0]["target_id"]
    rows = [
        {
            "check_id": "VAL3416_0_sources_exist",
            "check": "every cited local source path exists",
            "passed": source_exists,
            "detail": f"{sum(str(row['exists']).lower() == 'true' for row in source_rows)}/{len(source_rows)} source paths exist",
        },
        {
            "check_id": "VAL3416_1_scope",
            "check": "no output path targets formalization-workbench",
            "passed": no_workbench,
            "detail": "all outputs are under post-checkpoint-work",
        },
        {
            "check_id": "VAL3416_2_all_nonclaim",
            "check": "all rows keep valid_for_claim=false",
            "passed": all_nonclaim,
            "detail": "3416 is selector synthesis/demotion gate, not a claim",
        },
        {
            "check_id": "VAL3416_3_selector_math",
            "check": "exact conditional EH selector math is preserved",
            "passed": selector_pass,
            "detail": "q-basic two-derivative metric normal form selects EH conditionally",
        },
        {
            "check_id": "VAL3416_4_minimum_pole_nonclaim",
            "check": "minimum GR pole remains nonclaim",
            "passed": minimum_nonclaim,
            "detail": "minimum row is exact conditional but not parent-signed",
        },
        {
            "check_id": "VAL3416_5_hidden_stress_fail",
            "check": "hidden stress is not globally excluded",
            "passed": hidden_fail,
            "detail": "safe classes are class-by-class only",
        },
        {
            "check_id": "VAL3416_6_residual_demotion",
            "check": "non-EH residual demotion rows are explicit",
            "passed": residuals,
            "detail": "bound interface ready but values missing",
        },
        {
            "check_id": "VAL3416_7_local_GR_blocked",
            "check": "local-GR promotion remains blocked",
            "passed": local_blocked,
            "detail": "selector, hidden stress, residual and q_loc gates remain open",
        },
        {
            "check_id": "VAL3416_8_next_target",
            "check": "next target attacks retained q_loc/vector risk",
            "passed": next_qloc,
            "detail": generated["next_target"][0]["target_id"],
        },
    ]
    overall = all(row["passed"] for row in rows)
    rows.append(
        {
            "check_id": "VAL3416_9_overall",
            "check": "3416 selector/stress gate is internally valid",
            "passed": overall,
            "detail": "PASS" if overall else "FAIL",
        }
    )
    return rows


def build_doc(generated: dict[str, list[dict[str, Any]]]) -> str:
    return "\n\n".join(
        [
            "# 3416 - Parent Normal-Form EH Selector and Hidden-Stress Exclusion",
            "## Summary\n"
            "- This checkpoint decides what the parent EH selector route really buys after 3405-3409 and 3415.\n"
            "- Result: the EH selector math is solid as an exact conditional theorem. If MTS owns a q-basic two-derivative metric normal form with universal Hilbert source, EH follows.\n"
            "- Result: the minimum GR pole row is also exact conditional, and is useful as a denominator for residue bounds.\n"
            "- But the selector is not promoted: claim-ready `H_AB/R/J` rows are missing, non-EH residues are live, hidden stress is not globally excluded, and q_loc vector projection remains dangerous.\n"
            "- Therefore the fair status is not failure and not victory: exact conditional selector plus explicit residual demotion gate.",
            "## Source Register\n" + md_table(generated["source_register"]),
            "## Selector Synthesis\n" + md_table(generated["selector_synthesis"]),
            "## Hidden-Stress Exclusion Gate\n" + md_table(generated["hidden_stress_exclusion_gate"]),
            "## EH Promotion Audit\n" + md_table(generated["eh_promotion_audit"]),
            "## Residual Demotion Matrix\n" + md_table(generated["residual_demotion_matrix"]),
            "## Local-GR Status\n" + md_table(generated["local_gr_status"]),
            "## Promotion Gates\n" + md_table(generated["promotion_gates"]),
            "## Decision Ledger\n" + md_table(generated["decision_ledger"]),
            "## Next Target\n" + md_table(generated["next_target"]),
            "## Runner Nonclaim\n" + md_table(generated["runner_nonclaim"]),
            "## Validation\n" + md_table(generated["validation"]),
            "## Bottom Line\n"
            "The theory now has a serious conditional route to EH rather than a hand-wave: q-basic two-derivative metric normal form plus universal Hilbert source selects GR. "
            "But MTS has not yet proved the parent really has only that public TT mode, nor excluded all hidden stress. "
            "So the next smart strike is the retained q_loc/vector and beta/stress bound pack while keeping the HRJ parent-source extraction as the constructive selector path.",
        ]
    ) + "\n"


def main() -> None:
    if "formalization-workbench" in str(ROOT):
        raise RuntimeError(f"Refusing to run from formalization-workbench: {ROOT}")

    generated: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register(),
        "selector_synthesis": selector_synthesis(),
        "hidden_stress_exclusion_gate": hidden_stress_exclusion_gate(),
        "eh_promotion_audit": eh_promotion_audit(),
        "residual_demotion_matrix": residual_demotion_matrix(),
        "local_gr_status": local_gr_status(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    generated["validation"] = validation_rows(generated)

    for key, rows in generated.items():
        write_csv(OUTPUTS[key], rows)

    DOC.write_text(build_doc(generated), encoding="utf-8")

    if not all(str(row["passed"]).lower() == "true" for row in generated["validation"]):
        failed = [row for row in generated["validation"] if str(row["passed"]).lower() != "true"]
        raise SystemExit(f"3416 validation failed: {failed}")

    print(f"wrote {len(generated)} CSV artefacts and {DOC}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3593"
BRANCH_ID = "MTS_R2FR_Y5_PIM_PROJECTOR_VARIATION_3593"
DOC = ROOT / "3593-Y5-R2FR-PiM-projector-variation-zero-or-DeltaPiM-bound.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
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
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def text_contains(path: Path, needle: str) -> bool:
    return needle in path.read_text(encoding="utf-8-sig", errors="replace")


def sources() -> dict[str, tuple[Path, str]]:
    return {
        "next_3592": (
            RESIDUALS / "P8_Y5_R2FR_3592_NEXT_TARGET.csv",
            "NEXT3592_0",
        ),
        "status_3592": (
            RESIDUALS / "P8_Y5_R2FR_3592_STATUS.csv",
            "PIM_HILBERT_EQUALITY_NOT_DERIVED_EPSILON_MU_INPUT_PACK_READY",
        ),
        "delta_identity_3592": (
            RESIDUALS / "P8_Y5_R2FR_3592_CHARGE_EQUALITY_RESIDUAL_IDENTITY.csv",
            "Delta_PiM",
        ),
        "epsilon_pack_3592": (
            RESIDUALS / "P8_Y5_R2FR_3592_EPSILON_MU_INPUT_PACK.csv",
            "epsilon_PiM",
        ),
        "validation_3592": (
            RESIDUALS / "P8_Y5_BRR545_3592_VALIDATION.csv",
            "VAL3592_12_formalization_workbench_untouched",
        ),
        "projector_naturality_3572": (
            RESIDUALS / "P8_Y5_R2FR_3572_PROJECTOR_NATURALITY_PROOF.csv",
            "PN3572_2_chain_rule_zero",
        ),
        "projector_norms_3572": (
            RESIDUALS / "P8_Y5_R2FR_3572_KPROJECTOR_OPERATOR_NORM_ROWS.csv",
            "KPROJ3572_2_metric_stress",
        ),
        "projector_status_3572": (
            RESIDUALS / "P8_Y5_projector_deltaGamma_naturality_status.csv",
            "CLOSED_INSIDE_Q_EOBS_TAU_BRANCH_NONCLAIM_PUBLIC",
        ),
        "naturality_theorem_3498": (
            RESIDUALS / "P8_Y5_R2FR_3498_PROJECTOR_NATURALITY_THEOREM.csv",
            "PNT3498_1_functor_chain_rule",
        ),
        "kprojector_3498": (
            RESIDUALS / "P8_Y5_R2FR_3498_KPROJECTOR_BOUND_ROW.csv",
            "KPB3498_1_metric_stress_not_same_gate",
        ),
        "projector_no_stress_3431": (
            RESIDUALS / "P8_Y5_R2FR_3431_PROJECTOR_VARIATION_NO_STRESS_THEOREM.csv",
            "DP3431_6_operator_bound",
        ),
        "stress_interface_3444": (
            RESIDUALS / "P8_Y5_R2FR_3444_PROJECTOR_STRESS_INTERFACE.csv",
            "PSI3444_1_hodge_domain_stress",
        ),
        "kernel_projector_3387": (
            RESIDUALS / "P8_Y5_R2FR_3387_KERNEL_PROJECTOR_COMMUTATOR_LAW.csv",
            "KL3387_3_variable_projector_bound",
        ),
        "parent_projector_identity_3305": (
            RESIDUALS / "P8_Y5_R2FR_3305_PARENT_PROJECTOR_IDENTITY_DERIVATION.csv",
            "PIP3305_1_matter_variation",
        ),
        "parent_projector_audit_3305": (
            RESIDUALS / "P8_Y5_R2FR_3305_PROJECTOR_PROOF_CLAUSE_AUDIT.csv",
            "PCA3305_4_EM_binding_Poynting_accounted",
        ),
        "pim_variation_contract": (
            RESIDUALS / "P8_PiM_projector_variation_stress_CONTRACT.csv",
            "PV0_product_variation_included",
        ),
        "pim_algebra_contract": (
            RESIDUALS / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
            "PM5_projector_variation_owned",
        ),
        "pim_flux_contract": (
            RESIDUALS / "P8_PiM_flux_closure_Ward_topological_CONTRACT.csv",
            "FC2_closed_mass_current_equation",
        ),
        "charge_residuals_old": (
            RESIDUALS / "P8_charge_current_equality_RESIDUAL_DECOMPOSITION.csv",
            "Delta_PiM",
        ),
        "em_pim_htau_law": (
            RESIDUALS / "P8_EM_PiM_Htau_commutator_residual_law.csv",
            "PHCR3514_4_C_domain",
        ),
        "em_hodge_bound_vector": (
            RESIDUALS / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv",
            "EMB3503_7_Delta_PiM_metric",
        ),
    }


def outputs() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3593_SOURCE_REGISTER.csv",
        "variation_split": RESIDUALS / "P8_Y5_R2FR_3593_DELTAPIM_VARIATION_SPLIT.csv",
        "zero_proof_audit": RESIDUALS / "P8_Y5_R2FR_3593_PIM_PROJECTOR_ZERO_PROOF_AUDIT.csv",
        "bound_pack": RESIDUALS / "P8_Y5_R2FR_3593_DELTAPIM_BOUND_INPUT_PACK.csv",
        "promotion_gates": RESIDUALS / "P8_Y5_R2FR_3593_PROMOTION_GATES.csv",
        "activation_gates": RESIDUALS / "P8_Y5_R2FR_3593_ACTIVATION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3593_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3593_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_DeltaPiM_projector_variation_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3593_VALIDATION.csv",
    }


def source_register_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    rows = []
    for source_id, (path, needle) in source_map.items():
        exists = path.exists()
        rows.append(
            {
                "timestamp_utc": now(),
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source_id,
                "source_path": str(path),
                "exists": exists,
                "needle": needle,
                "needle_found": exists and text_contains(path, needle),
                "valid_for_claim": False,
            }
        )
    return rows


def variation_split_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    path = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        {
            "split_id": "DPS3593_0_imported_target",
            "term": "Delta_PiM",
            "formula": "Delta_PiM := M_eff[(delta Pi_M)J_H] + M_eff[Pi_M J_H - J_M^parent]",
            "derivation": "3592 isolated this as the central source-coupling obstruction inside B_xi/G_ref - M_H[Pi_M J_H].",
            "status": "TARGET_IMPORTED_FROM_3592",
            "source_path": path["delta_identity_3592"],
        },
        {
            "split_id": "DPS3593_1_product_variation",
            "term": "delta(Pi_M J_H)",
            "formula": "delta(Pi_M J_H)=Pi_M delta J_H+(delta_Gamma Pi_M)J_H+(delta_g Pi_M)J_H+(D_D Pi_M)[delta D]J_H+(delta_read Pi_M)J_H",
            "derivation": "The product rule is exact; dropping any projector derivative is the smuggling route 3593 is closing.",
            "status": "EXACT_SPLIT",
            "source_path": path["pim_variation_contract"],
        },
        {
            "split_id": "DPS3593_2_Gamma_zero",
            "term": "Delta_PiM_Gamma",
            "formula": "delta_Gamma_ind Pi_M = D_q Pi_M D_Gamma q + D_e Pi_M D_Gamma e_obs + D_tau Pi_M D_Gamma tau + D_H Pi_M D_Gamma H_ref = 0",
            "derivation": "In the q/e_obs/tau-natural LC branch Pi_M has no independent Gamma slot, so every chain-rule factor vanishes at fixed q,e_obs,tau,H_ref/topology.",
            "status": "ZERO_DERIVED_INSIDE_Q_EOBS_TAU_BRANCH",
            "source_path": path["projector_naturality_3572"],
        },
        {
            "split_id": "DPS3593_3_metric_domain_retained",
            "term": "Delta_PiM_metric_domain",
            "formula": "M_eff[((delta_g Pi_M)J_H)+(D_D Pi_M)[delta D]J_H]",
            "derivation": "3572 separated Gamma naturality from metric/Hodge/domain projector stress; 3431 gives a no-go unless the projector is fixed-topological, analysis-only outside the action, or explicitly bounded.",
            "status": "NOT_ZERO_CURRENT_BRANCH",
            "source_path": path["projector_no_stress_3431"],
        },
        {
            "split_id": "DPS3593_4_parent_current_mismatch",
            "term": "Delta_PiM_parent",
            "formula": "M_eff[Pi_M J_H - J_M^parent]",
            "derivation": "Pi_M J_H must equal the parent-owned mass current before readout; 3305 gives a conditional Hilbert-source route, but the linearized projector and no-direct-hidden-coupling clauses are not signed.",
            "status": "NOT_PARENT_SIGNED",
            "source_path": path["parent_projector_identity_3305"],
        },
        {
            "split_id": "DPS3593_5_flux_commutator_retained",
            "term": "Delta_PiM_flux_comm",
            "formula": "integral_A [d,Pi_M]J_H",
            "derivation": "Gamma naturality does not imply d(Pi_M J_H)=0; flux closure still needs Ward/topological/Euler mass-current closure.",
            "status": "RETAINED_FOR_FLUX_CLOSURE",
            "source_path": path["pim_flux_contract"],
        },
        {
            "split_id": "DPS3593_6_em_poynting_accounting",
            "term": "Delta_PiM_EM_accounting",
            "formula": "Pi_M J_H_total must include matter + EM stress + Poynting/binding energy exactly once",
            "derivation": "The parent projector cannot win by omitting EM/Poynting stress from the Hilbert source or double-counting it as a hidden projector correction.",
            "status": "RETAINED_EXPLICITLY_NOT_DROPPED",
            "source_path": path["parent_projector_audit_3305"],
        },
        {
            "split_id": "DPS3593_7_bound_law",
            "term": "epsilon_PiM",
            "formula": "epsilon_PiM <= epsilon_PiM_Gamma + epsilon_PiM_metric + epsilon_PiM_domain + epsilon_PiM_parent + epsilon_PiM_flux + epsilon_PiM_EM + epsilon_PiM_readout",
            "derivation": "The Gamma piece is zero in the natural LC branch; all other pieces remain nonclaim inputs until zero theorems or numeric/source-backed bounds exist.",
            "status": "PARTIAL_ZERO_PLUS_BOUND_BRANCH",
            "source_path": path["epsilon_pack_3592"],
        },
    ]
    stamp = now()
    for row in rows:
        row.update(
            {
                "timestamp_utc": stamp,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "claim_allowed": False,
                "valid_for_claim": False,
            }
        )
    return rows


def zero_proof_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    path = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        (
            "ZPIM3593_0_same_frame_source",
            "same-frame Hilbert mass current exists before readout",
            "J_M=Pi_M J_H[e_obs]",
            "CONDITIONAL_SOURCE_PRESENT",
            "needed but not enough",
            "pim_flux_contract",
        ),
        (
            "ZPIM3593_1_Gamma_slot_absent",
            "Pi_M has no independent Gamma_ind argument slot in q/e_obs/tau LC branch",
            "D_Gamma_ind Pi_M=0",
            "PASS_PRIVATE_BRANCH",
            "kills Delta_PiM_Gamma only",
            "projector_naturality_3572",
        ),
        (
            "ZPIM3593_2_metric_domain_silence",
            "metric/Hodge/domain derivatives vanish or are outside action",
            "delta_g Pi_M=0 and D_D Pi_M=0",
            "FAIL_CURRENT_BRANCH",
            "keeps Delta_PiM_metric_domain live",
            "projector_no_stress_3431",
        ),
        (
            "ZPIM3593_3_parent_current_identity",
            "projected Hilbert mass current equals parent-owned mass current",
            "Pi_M J_H = J_M^parent",
            "FAIL_CURRENT_BRANCH",
            "keeps Delta_PiM_parent live",
            "parent_projector_identity_3305",
        ),
        (
            "ZPIM3593_4_flux_closure",
            "projected current is closed in compact local exterior",
            "d(Pi_M J_H)=0",
            "FAIL_CURRENT_BRANCH",
            "keeps dln_Meff_dt and partial_r ln mu_obs live",
            "pim_flux_contract",
        ),
        (
            "ZPIM3593_5_readout_masks",
            "readout/fitted masks never enter parent variation",
            "delta_read Pi_M=0 inside S_parent",
            "OPEN_GUARDED",
            "cannot be used as a post-fit cancellation",
            "pim_variation_contract",
        ),
        (
            "ZPIM3593_6_em_poynting_once",
            "EM stress, Poynting flux, and binding energy enter once through J_H_total",
            "Pi_M J_H_total is not matter-only and not double counted",
            "OPEN_RETAINED",
            "prevents a fake source-coupling win",
            "em_hodge_bound_vector",
        ),
        (
            "ZPIM3593_7_total_zero_verdict",
            "all pieces of Delta_PiM vanish",
            "Delta_PiM=0",
            "FAIL_CURRENT_TOTAL_ZERO",
            "only Delta_PiM_Gamma is zeroed; total epsilon_PiM stays active",
            "status_3592",
        ),
    ]
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "proof_id": proof_id,
            "clause": clause,
            "formula": formula,
            "status": status,
            "consequence": consequence,
            "source_path": path[source_id],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for proof_id, clause, formula, status, consequence, source_id in rows
    ]


def bound_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    path = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        (
            "DPB3593_0_epsilon_PiM_Gamma",
            "epsilon_PiM_Gamma",
            "abs(M_eff[(delta_Gamma_ind Pi_M)J_H])/abs(M_H_ref)",
            "dimensionless",
            "0 inside q/e_obs/tau-natural LC branch; otherwise K_projector_Gamma ||J_H||/abs(M_H_ref)",
            "q/e_obs/tau naturality theorem or K_projector_Gamma, ||J_H||, M_H_ref",
            "projector_naturality_3572",
            "ZERO_PRIVATE_BRANCH_NONCLAIM",
        ),
        (
            "DPB3593_1_epsilon_PiM_metric",
            "epsilon_PiM_metric",
            "abs(M_eff[(delta_g Pi_M)J_H])/abs(M_H_ref)",
            "dimensionless PPN/source-normalization envelope",
            "MISSING_ZERO_OR_NUMERIC_BOUND",
            "K_PiM_metric, weak-field projection coefficients, ||J_H||, M_H_ref, units",
            "projector_no_stress_3431",
            "BOUND_READY_VALUES_MISSING",
        ),
        (
            "DPB3593_2_epsilon_PiM_domain",
            "epsilon_PiM_domain",
            "abs(M_eff[(D_D Pi_M)[delta D]J_H])/abs(M_H_ref)",
            "dimensionless domain/worldtube/source-support envelope",
            "MISSING_ZERO_OR_NUMERIC_BOUND",
            "K_PiM_domain, deltaD norm, source support, M_H_ref, units",
            "stress_interface_3444",
            "BOUND_READY_VALUES_MISSING",
        ),
        (
            "DPB3593_3_epsilon_PiM_parent",
            "epsilon_PiM_parent",
            "abs(M_eff[Pi_M J_H - J_M^parent])/abs(M_H_ref)",
            "dimensionless current-identity envelope",
            "MISSING_PARENT_CURRENT_EQUALITY",
            "parent mass current definition, Pi_M Hilbert identity, no direct hidden matter coupling",
            "parent_projector_identity_3305",
            "IDENTITY_MISSING",
        ),
        (
            "DPB3593_4_epsilon_PiM_flux",
            "epsilon_PiM_flux",
            "abs(integral_A [d,Pi_M]J_H)/abs(M_H_ref)",
            "dimensionless radial/time mass-flux envelope",
            "MISSING_FLUX_CLOSURE_OR_NUMERIC_BOUND",
            "Ward/topological/Euler mass-current closure or dln_Meff_dt and partial_r ln mu_obs bounds",
            "pim_flux_contract",
            "BOUND_READY_VALUES_MISSING",
        ),
        (
            "DPB3593_5_epsilon_PiM_EM",
            "epsilon_PiM_EM_accounting",
            "abs(Pi_M[J_H_total - J_matter - J_EM - J_Poynting - J_bind])/abs(M_H_ref)",
            "dimensionless source-accounting envelope",
            "MISSING_ONCE_ONLY_EM_STRESS_ACCOUNTING",
            "Hilbert EM stress/Poynting/binding-energy source map and no-double-count proof",
            "em_hodge_bound_vector",
            "RETAINED_NOT_DROPPED",
        ),
        (
            "DPB3593_6_epsilon_PiM_readout",
            "epsilon_PiM_readout",
            "abs(M_eff[(delta_read Pi_M)J_H])/abs(M_H_ref)",
            "dimensionless readout-mask envelope",
            "MISSING_READOUT_OUTSIDE_ACTION_PROOF",
            "proof readout masks are post-variation only or source-backed operator norm",
            "pim_variation_contract",
            "BOUND_READY_VALUES_MISSING",
        ),
        (
            "DPB3593_7_epsilon_PiM_total",
            "epsilon_PiM",
            "epsilon_PiM_Gamma + epsilon_PiM_metric + epsilon_PiM_domain + epsilon_PiM_parent + epsilon_PiM_flux + epsilon_PiM_EM_accounting + epsilon_PiM_readout",
            "dimensionless source-coupling residual",
            "NOT_SCORE_READY_TOTAL",
            "all component zeros or numeric/source-backed component bounds",
            "epsilon_pack_3592",
            "TOTAL_BOUND_BRANCH_ACTIVE",
        ),
    ]
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "bound_id": bound_id,
            "symbol": symbol,
            "formula": formula,
            "units": units,
            "current_value": current_value,
            "required_inputs": required_inputs,
            "source_path": path[source_id],
            "score_status": score_status,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for bound_id, symbol, formula, units, current_value, required_inputs, source_id, score_status in rows
    ]


def promotion_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    path = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        ("PROM3593_0_gamma_component", "Delta_PiM_Gamma=0", "PASS_PRIVATE_BRANCH", "may reduce epsilon_PiM but is not a public local-GR claim", "projector_status_3572"),
        ("PROM3593_1_total_DeltaPiM_zero", "Delta_PiM=0", "FAIL_CURRENT_CLAIM", "metric/domain/parent-current/flux/readout pieces remain live", "projector_no_stress_3431"),
        ("PROM3593_2_bound_pack", "epsilon_PiM component bound rows exist", "PASS_NONCLAIM", "rows are source-owned but not score-ready", "epsilon_pack_3592"),
        ("PROM3593_3_em_poynting_guard", "EM/Poynting/binding stress not dropped", "PASS_GUARD", "source coupling cannot omit real EM stress", "parent_projector_audit_3305"),
        ("PROM3593_4_Newton_GM_guard", "measured GM/Newton/local-GR not claimed", "PASS_GUARD", "Delta_PiM remains active inside epsilon_mu", "status_3592"),
        ("PROM3593_5_next_derivation", "fixed-topological PiM or metric/domain coefficient route selected", "PASS_ROUTE_SELECTED", "next step attacks largest remaining projector pieces", "stress_interface_3444"),
    ]
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "consequence": consequence,
            "source_path": path[source_id],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for gate_id, gate, status, consequence, source_id in rows
    ]


def activation_rows() -> list[dict[str, object]]:
    rows = [
        ("ACT3593_0_sources", "all source files and needles are present", "PASS"),
        ("ACT3593_1_gamma_zero", "Delta_PiM_Gamma zero imported from 3572", "PASS_PRIVATE_BRANCH"),
        ("ACT3593_2_total_zero", "Delta_PiM total zero", "FAIL_CURRENT_CLAIM"),
        ("ACT3593_3_bound_pack", "epsilon_PiM component rows complete", "PASS_NONCLAIM"),
        ("ACT3593_4_score_ready", "all epsilon_PiM components have zeros or numeric source-backed bounds", "FAIL_CURRENT_SCORE"),
        ("ACT3593_5_no_local_gr_claim", "Newton/PPN/local-GR source coupling remains blocked", "PASS_GUARD"),
        ("ACT3593_6_next_target", "3594 route selected", "PASS"),
    ]
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "activation_id": activation_id,
            "condition": condition,
            "status": status,
            "valid_for_claim": False,
        }
        for activation_id, condition, status in rows
    ]


def status_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "DELTAPIM_GAMMA_ZERO_DERIVED_TOTAL_BOUND_BRANCH_ACTIVE",
            "strongest_result": "3593 imports the 3572 chain-rule theorem into the source-coupling gate: the independent-Gamma projector variation piece of Delta_PiM is zero in the q/e_obs/tau-natural LC branch. Total Delta_PiM is not zero because metric/Hodge/domain stress, parent-current identity, flux closure, readout masks, and EM/Poynting source accounting remain live.",
            "decision": "reduce epsilon_PiM by removing the Gamma component in the private LC branch; keep measured GM, Newtonian mechanics, PPN/local-GR, and public source-coupling claims blocked until remaining components are zeroed or bounded",
            "still_missing": "fixed-topological or identity PiM proof, metric/domain projector stress silence, Pi_M J_H = J_M^parent, d(Pi_M J_H)=0, EM/Poynting/binding once-only Hilbert accounting, readout-outside-action proof, numeric/source-backed bounds",
            "public_claim_allowed": False,
            "valid_for_claim": False,
            "source_path": str(source_map["projector_naturality_3572"][0]),
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3593_0",
            "target_doc": "3594-Y5-R2FR-fixed-topological-PiM-or-metric-domain-bound-coefficients.md",
            "target_script": "scripts/Y5_R2FR_3594_fixed_topological_PiM_or_metric_domain_bound_coefficients.py",
            "objective": "try to upgrade the remaining PiM metric/domain pieces to zero by constructing a fixed-topological or identity projector theorem; if that fails, produce source-ready K_PiM_metric and K_PiM_domain coefficient rows",
            "success_gate": "either delta_g Pi_M=D_D Pi_M=0 with parent/topological ownership and EM/Poynting source accounting, or epsilon_PiM_metric/domain get explicit operator coefficient, units, and bound-source rows without local-GR claims",
            "reason": "3593 removes the Gamma projector piece; the next largest PiM obstruction is metric/domain projector stress",
            "valid_for_claim": False,
        }
    ]


def validation_rows(
    source_map: dict[str, tuple[Path, str]],
    out_paths: dict[str, Path],
    split: list[dict[str, object]],
    zero: list[dict[str, object]],
    bounds: list[dict[str, object]],
    gates: list[dict[str, object]],
    activation: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[tuple[str, bool, str]] = []
    validations.append(
        (
            "VAL3593_0_sources_exist",
            all(path.exists() for path, _needle in source_map.values()),
            "all required 3593 source paths exist",
        )
    )
    validations.append(
        (
            "VAL3593_1_required_needles_found",
            all(path.exists() and text_contains(path, needle) for path, needle in source_map.values()),
            "all selected 3593 source anchors found",
        )
    )
    pre_validation = {key: path for key, path in out_paths.items() if key != "validation"}
    validations.append(
        (
            "VAL3593_2_outputs_exist",
            all(path.exists() for path in pre_validation.values()),
            "all pre-validation 3593 csv output files written",
        )
    )
    parse_ok = True
    parse_details: list[str] = []
    for output_id, path in pre_validation.items():
        if path.suffix.lower() != ".csv":
            continue
        try:
            parse_details.append(f"{output_id}:{len(read_csv(path))}")
        except Exception as exc:  # pragma: no cover - validation path
            parse_ok = False
            parse_details.append(f"{output_id}:ERROR:{exc}")
    validations.append(("VAL3593_3_csv_parse", parse_ok, "; ".join(parse_details)))
    validations.append(
        (
            "VAL3593_4_gamma_zero_present",
            any(row["term"] == "Delta_PiM_Gamma" and row["status"] == "ZERO_DERIVED_INSIDE_Q_EOBS_TAU_BRANCH" for row in split),
            "Gamma variation zero row is present",
        )
    )
    validations.append(
        (
            "VAL3593_5_total_zero_blocked",
            any(row["proof_id"] == "ZPIM3593_7_total_zero_verdict" and row["status"] == "FAIL_CURRENT_TOTAL_ZERO" for row in zero),
            "total Delta_PiM zero remains blocked",
        )
    )
    required_bounds = {
        "epsilon_PiM_Gamma",
        "epsilon_PiM_metric",
        "epsilon_PiM_domain",
        "epsilon_PiM_parent",
        "epsilon_PiM_flux",
        "epsilon_PiM_EM_accounting",
        "epsilon_PiM_readout",
        "epsilon_PiM",
    }
    validations.append(
        (
            "VAL3593_6_bound_pack_complete",
            required_bounds.issubset({str(row["symbol"]) for row in bounds}),
            "epsilon_PiM bound pack includes all required components",
        )
    )
    validations.append(
        (
            "VAL3593_7_em_poynting_retained",
            any(row["term"] == "Delta_PiM_EM_accounting" and row["status"] == "RETAINED_EXPLICITLY_NOT_DROPPED" for row in split),
            "EM/Poynting/binding source accounting is retained explicitly",
        )
    )
    validations.append(
        (
            "VAL3593_8_no_claim_flags",
            not any(str(row.get("valid_for_claim", "False")).lower() == "true" or str(row.get("claim_allowed", "False")).lower() == "true" for table in [split, zero, bounds, gates, status] for row in table),
            "all generated physics rows remain nonclaim",
        )
    )
    validations.append(
        (
            "VAL3593_9_score_blocked",
            any(row["activation_id"] == "ACT3593_4_score_ready" and row["status"] == "FAIL_CURRENT_SCORE" for row in activation),
            "score remains blocked until residual components have values or zero theorems",
        )
    )
    validations.append(
        (
            "VAL3593_10_no_local_gr_claim",
            any(row["activation_id"] == "ACT3593_5_no_local_gr_claim" and row["status"] == "PASS_GUARD" for row in activation),
            "Newton/PPN/local-GR claim guard is active",
        )
    )
    validations.append(
        (
            "VAL3593_11_next_target_selected",
            any(row["next_id"] == "NEXT3593_0" for row in next_target),
            "3594 fixed-topological PiM or metric/domain coefficient target selected",
        )
    )
    output_source_paths = []
    for table in [split, zero, bounds, gates, status]:
        for row in table:
            source_path = row.get("source_path")
            if source_path:
                output_source_paths.append(Path(str(source_path)))
    validations.append(
        (
            "VAL3593_12_generated_source_paths_exist",
            all(path.exists() for path in output_source_paths),
            "every generated row source_path exists",
        )
    )
    formal_hits = list(FORMALIZATION.rglob("*3593*")) if FORMALIZATION.exists() else []
    validations.append(
        (
            "VAL3593_13_formalization_workbench_untouched",
            len(formal_hits) == 0,
            "no 3593 checkpoint output appears in formalization-workbench",
        )
    )
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "validation_id": validation_id,
            "passes": passes,
            "status": "PASS" if passes else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
        }
        for validation_id, passes, detail in validations
    ]


def write_doc(
    split: list[dict[str, object]],
    zero: list[dict[str, object]],
    bounds: list[dict[str, object]],
    gates: list[dict[str, object]],
    activation: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    lines = [
        "# 3593 - PiM projector variation zero or DeltaPiM bound",
        "",
        "## Verdict",
        "`Delta_PiM=0` is not proved.  But 3593 does remove one real piece: in the q/e_obs/tau-natural LC branch, `delta_Gamma_ind Pi_M=0`, so the independent-connection projector-variation term is zero.",
        "",
        "The surviving obstruction is now sharper:",
        "",
        "`epsilon_PiM <= epsilon_PiM_Gamma + epsilon_PiM_metric + epsilon_PiM_domain + epsilon_PiM_parent + epsilon_PiM_flux + epsilon_PiM_EM_accounting + epsilon_PiM_readout`,",
        "",
        "with `epsilon_PiM_Gamma=0` only inside the private natural-projector branch.  The other terms remain nonclaim inputs.",
        "",
        "## Variation Split",
    ]
    for row in split:
        lines.append(f"- `{row['split_id']}` / `{row['term']}`: {row['status']} - {row['formula']}")
    lines.extend(["", "## Zero Proof Audit"])
    for row in zero:
        lines.append(f"- `{row['proof_id']}`: {row['status']} - {row['clause']}")
    lines.extend(["", "## DeltaPiM Bound Input Pack"])
    for row in bounds:
        lines.append(f"- `{row['bound_id']}` / `{row['symbol']}`: {row['score_status']} - {row['formula']}")
    lines.extend(["", "## Promotion Gates"])
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: {row['status']} - {row['consequence']}")
    lines.extend(["", "## Status"])
    for row in status:
        lines.append(f"- `{row['status']}`: {row['strongest_result']}")
        lines.append(f"- Decision: {row['decision']}")
        lines.append(f"- Still missing: {row['still_missing']}")
    lines.extend(["", "## Activation Gates"])
    for row in activation:
        lines.append(f"- `{row['activation_id']}`: {row['status']} - {row['condition']}")
    lines.extend(["", "## Validation"])
    for row in validation:
        lines.append(f"- `{row['validation_id']}`: {row['status']} ({row['detail']})")
    lines.extend(["", "## Next target"])
    for row in next_target:
        lines.append(f"- `{row['next_id']}` -> `{row['target_doc']}`")
        lines.append(f"- Objective: {row['objective']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    source_map = sources()
    out_paths = outputs()
    register = source_register_rows(source_map)
    split = variation_split_rows(source_map)
    zero = zero_proof_rows(source_map)
    bounds = bound_rows(source_map)
    gates = promotion_rows(source_map)
    activation = activation_rows()
    status = status_rows(source_map)
    next_target = next_target_rows()

    write_csv(out_paths["source_register"], register)
    write_csv(out_paths["variation_split"], split)
    write_csv(out_paths["zero_proof_audit"], zero)
    write_csv(out_paths["bound_pack"], bounds)
    write_csv(out_paths["promotion_gates"], gates)
    write_csv(out_paths["activation_gates"], activation)
    write_csv(out_paths["status"], status)
    write_csv(out_paths["next_target"], next_target)
    write_csv(out_paths["canonical_status"], status)

    validation = validation_rows(source_map, out_paths, split, zero, bounds, gates, activation, status, next_target)
    write_csv(out_paths["validation"], validation)
    write_doc(split, zero, bounds, gates, activation, status, next_target, validation)

    print(f"wrote {DOC}")
    for output_id, path in out_paths.items():
        print(f"{output_id}: {path}")


if __name__ == "__main__":
    main()

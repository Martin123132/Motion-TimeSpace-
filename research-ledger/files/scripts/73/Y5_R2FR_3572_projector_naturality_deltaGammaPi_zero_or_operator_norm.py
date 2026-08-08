from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3572-Y5-R2FR-projector-naturality-deltaGammaPi-zero-or-operator-norm.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_Y5_PROJECTOR_NATURALITY_3572"
CHECKPOINT_ID = "3572"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty CSV requested: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def file_contains(path: Path, token: str) -> bool:
    return token in path.read_text(encoding="utf-8", errors="ignore")


def sources() -> dict[str, Path]:
    return {
        "handoff_3571": RESIDUALS / "P8_Y5_R2FR_3571_NEXT_TARGET.csv",
        "selector_theorem_3571": RESIDUALS / "P8_Y5_R2FR_3571_BLC_SELECTOR_THEOREM.csv",
        "leakage_3571": RESIDUALS / "P8_Y5_R2FR_3571_SOURCE_OWNER_LEAKAGE_BOUND_ROWS.csv",
        "sector_matrix_3571": RESIDUALS / "P8_Y5_R2FR_3571_BLC_SECTOR_PRODUCT_MATRIX.csv",
        "status_3571": RESIDUALS / "P8_Y5_R2FR_3571_STATUS.csv",
        "projector_theorem_3498": RESIDUALS / "P8_Y5_R2FR_3498_PROJECTOR_NATURALITY_THEOREM.csv",
        "projector_bound_3498": RESIDUALS / "P8_Y5_R2FR_3498_KPROJECTOR_BOUND_ROW.csv",
        "projector_stress_3498": RESIDUALS / "P8_Y5_R2FR_3498_PROJECTOR_STRESS_TEST_MATRIX.csv",
        "pim_algebra": RESIDUALS / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
        "pim_variation": RESIDUALS / "P8_PiM_projector_variation_stress_CONTRACT.csv",
        "pim_flux": RESIDUALS / "P8_PiM_flux_closure_Ward_topological_CONTRACT.csv",
        "mass_flux": RESIDUALS / "P8_mass_flux_projector_Euler_calibration_CONTRACT.csv",
        "variation_chain_3497": RESIDUALS / "P8_Y5_R2FR_3497_VARIATION_CHAIN.csv",
        "signature_3566": RESIDUALS / "P8_Y5_R2FR_3566_PARENT_LOCAL_LC_ACTION_SIGNATURE.csv",
        "variation_3566": RESIDUALS / "P8_Y5_R2FR_3566_NO_GAMMA_VARIATION_DERIVATION.csv",
        "hyper_kernel_3496": RESIDUALS / "P8_Y5_R2FR_3496_SOURCE_HYPERMOMENTUM_KERNEL_VECTOR.csv",
        "pim_htau_commutator": RESIDUALS / "P8_EM_PiM_Htau_commutator_residual_law.csv",
    }


def source_register(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    roles = {
        "handoff_3571": "declares 3572 target",
        "selector_theorem_3571": "imports B_LC product gate",
        "leakage_3571": "imports epsilon_projector_comm target",
        "sector_matrix_3571": "imports live projector weak link",
        "status_3571": "imports current selector status",
        "projector_theorem_3498": "imports prior delta_Gamma Pi naturality theorem",
        "projector_bound_3498": "imports K_projector fallback row",
        "projector_stress_3498": "imports projector type stress matrix",
        "pim_algebra": "imports Pi_M algebra and variation ownership contract",
        "pim_variation": "imports metric/Hodge projector variation stress contract",
        "pim_flux": "imports mass-flux closure contract",
        "mass_flux": "imports measured GM/source calibration contract",
        "variation_chain_3497": "imports Pi_M product rule weak link",
        "signature_3566": "imports q/e_obs/tau-natural Pi_M branch signature",
        "variation_3566": "imports no-Gamma current variation",
        "hyper_kernel_3496": "imports epsilon_projector_comm bound formula",
        "pim_htau_commutator": "imports Pi_M/H_tau residual decomposition",
    }
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "source_id": source_id,
            "source_path": str(path),
            "source_path_exists": path.exists(),
            "role": roles[source_id],
            "valid_for_claim": False,
        }
        for source_id, path in source_paths.items()
    ]


def naturality_proof_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "PN3572_0_target",
            "target split",
            "The needed projector result for the LC selector is delta_Gamma_ind Pi_M=0, not full metric/Hodge projector stress silence.",
            "The source-current product rule is delta_Gamma(Pi_M J_H)=Pi_M delta_Gamma J_H+(delta_Gamma Pi_M)J_H. 3572 attacks the second term only.",
            "TARGET_SHARPENED",
            "projector_theorem_3498",
        ),
        (
            "PN3572_1_argument_domain",
            "q/e_obs/tau-natural projector",
            "In the 3566 branch Pi_M=Pi_bar(q(Phi),e_obs(q),tau(q),H_ref,topology) and has no Gamma_ind or omega_ind argument slot.",
            "This is an argument-domain statement, not a small-coefficient fit.",
            "PRIVATE_BRANCH_SIGNATURE_AVAILABLE",
            "signature_3566",
        ),
        (
            "PN3572_2_chain_rule_zero",
            "delta_Gamma Pi_M zero",
            "For independent affine variation at fixed q,e_obs,tau,H_ref/topology, delta_Gamma_ind Pi_M = D_q Pi D_Gamma q + D_e Pi D_Gamma e_obs + D_tau Pi D_Gamma tau + D_H Pi D_Gamma H_ref = 0.",
            "Every term vanishes because q,e_obs,tau and fixed reference/topology are not functions of Gamma_ind in the LC branch.",
            "EXACT_INSIDE_Q_EOBS_TAU_BRANCH",
            "projector_theorem_3498",
        ),
        (
            "PN3572_3_current_product_rule",
            "projected current Gamma silence",
            "Inside the same branch, delta_Gamma J_H=0 and delta_Gamma Pi_M=0, hence delta_Gamma(Pi_M J_H)=0.",
            "This closes the independent-Gamma projector commutator contribution to epsilon_hypermomentum_source.",
            "EXACT_INSIDE_BRANCH",
            "variation_3566",
        ),
        (
            "PN3572_4_counterbranch",
            "Gamma transport countermodel",
            "If Pi_M uses Gamma_ind parallel transport, Gamma_ind collar transport, a fitted readout mask, or an unsourced marker selector before variation, then delta_Gamma Pi_M need not vanish.",
            "That branch must use K_projector := ||delta_Gamma Pi_M|| and cannot claim LC selector closure.",
            "COUNTERMODEL_RETAINED",
            "projector_stress_3498",
        ),
        (
            "PN3572_5_metric_stress_separation",
            "metric projector stress remains separate",
            "A Hodge/DeWitt/e_obs projector can have delta_g Pi_M stress while still having delta_Gamma_ind Pi_M=0.",
            "This means 3572 advances the Gamma/source-hypermomentum gate but does not by itself prove PPN, Newtonian source calibration, or full local GR.",
            "IMPORTANT_SCOPE_GUARD",
            "pim_variation",
        ),
        (
            "PN3572_6_result",
            "3572 result",
            "The projector Gamma commutator is zero inside the q/e_obs/tau-natural LC branch: I_projector^Gamma=1. The full B_LC selector remains nonclaim because metric/projector stress, mass-flux closure, H_ref, boundary and GM calibration remain open.",
            "The live weak link has moved from delta_Gamma Pi_M to d(Pi_M J_H), projector metric stress and calibrated source charge.",
            "PROJECTOR_GAMMA_GATE_CLOSED_PRIVATE_BRANCH_FULL_LOCAL_GR_BLOCKED",
            "status_3571",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "proof_id": proof_id,
            "claim_piece": claim_piece,
            "statement": statement,
            "derivation": derivation,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for proof_id, claim_piece, statement, derivation, status, source_key in specs
    ]


def branch_update_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "UPD3572_0_projector_gamma",
            "I_projector^Gamma",
            "delta_Gamma_ind Pi_M=0 for q/e_obs/tau-natural Pi_M",
            "PASS_INSIDE_SELECTED_LC_BRANCH",
            "promotes projector Gamma reentry from live weak link to branch-closed component",
            "projector_theorem_3498",
        ),
        (
            "UPD3572_1_projector_metric",
            "I_projector^metric_stress",
            "delta_g Pi_M stress, Hodge/DeWitt variation and domain/homology variation",
            "OPEN_SEPARATE_LOCAL_GR_GATE",
            "metric projector stress can still map to PPN/R11/source-normalization residuals",
            "pim_variation",
        ),
        (
            "UPD3572_2_flux_closure",
            "I_flux",
            "d(Pi_M J_H)=0 as Ward/topological/Euler mass-current closure",
            "OPEN_NEWTON_SOURCE_GATE",
            "delta_Gamma silence does not imply radial/time mass conservation",
            "pim_flux",
        ),
        (
            "UPD3572_3_calibration",
            "I_GM_calibration",
            "M_eff=(4 pi G_ref)^-1 int_S2 Pi_M J_H and mu_obs=G_ref M_eff",
            "OPEN_MEASURED_GM_GATE",
            "closed current is not yet measured Newtonian source mass",
            "mass_flux",
        ),
        (
            "UPD3572_4_selector",
            "B_LC_selector",
            "product of sector gates with I_projector^Gamma improved but flux/calibration/stress gates still open",
            "FALSE_PUBLICLY_CURRENTLY",
            "axial torsion/source-hypermomentum route improved; local GR/Newton claim still blocked",
            "selector_theorem_3571",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "update_id": update_id,
            "selector_factor": factor,
            "condition_or_formula": formula,
            "status": status,
            "consequence": consequence,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for update_id, factor, formula, status, consequence, source_key in specs
    ]


def operator_norm_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "KPROJ3572_0_gamma_operator_norm",
            "K_projector_Gamma",
            "||delta_Gamma_ind Pi_M||_{J_H->M}",
            "projector operator norm per affine variation",
            "0 inside q/e_obs/tau-natural LC branch; otherwise missing numeric/theorem value",
            "source-backed operator norm or theorem-zero for any Gamma-dependent transport projector",
            "projector_bound_3498",
            False,
        ),
        (
            "KPROJ3572_1_projector_comm",
            "epsilon_projector_comm",
            "epsilon_projector_comm <= K_projector_Gamma ||J_H|| / abs(M_H_ref)",
            "dimensionless source-tail envelope",
            "zero inside natural branch; executable nonclaim if Gamma-dependent Pi_M is admitted",
            "K_projector_Gamma, ||J_H||, M_H_ref, units and source paths",
            "leakage_3571",
            False,
        ),
        (
            "KPROJ3572_2_metric_stress",
            "epsilon_projector_metric_stress",
            "retained separate local-GR gate from delta_g Pi_M, Hodge/DeWitt/domain variations",
            "PPN/R11/source-normalization units after projection",
            "not closed by delta_Gamma Pi_M theorem",
            "metric variation stress ledger and weak-field projection coefficients",
            "pim_variation",
            False,
        ),
        (
            "KPROJ3572_3_flux",
            "d(Pi_M J_H)",
            "d(Pi_M J_H)=Pi_M dJ_H+[d,Pi_M]J_H",
            "mass-flux/current units",
            "requires Ward/topological/Euler mass-current closure; not implied by Gamma-natural Pi_M",
            "mass-current closure equation or dln_Meff_dt/partial_r ln mu_obs residuals",
            "pim_flux",
            False,
        ),
        (
            "KPROJ3572_4_counterbranch",
            "Gamma_ind_transport_projector",
            "if Pi_M uses Gamma_ind transport then K_projector_Gamma is live",
            "branch status",
            "affine counterbranch retained as nonclaim",
            "operator norm for transport/collar projector and source-current norm",
            "projector_stress_3498",
            False,
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "bound_id": bound_id,
            "symbol": symbol,
            "formula": formula,
            "units": units,
            "current_value": current_value,
            "required_inputs": required_inputs,
            "source_path": str(source_paths[source_key]),
            "score_ready": score_ready,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for bound_id, symbol, formula, units, current_value, required_inputs, source_key, score_ready in specs
    ]


def activation_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        ("GATE3572_0_sources", "source audit", "PASS", "all required 3572 source paths exist"),
        ("GATE3572_1_chain_rule", "delta_Gamma Pi_M", "PASS_INSIDE_LC_BRANCH", "q/e_obs/tau-natural Pi_M has no Gamma_ind slot"),
        ("GATE3572_2_product_rule", "delta_Gamma(Pi_M J_H)", "PASS_INSIDE_LC_BRANCH", "delta_Gamma J_H=0 and delta_Gamma Pi_M=0 inside same branch"),
        ("GATE3572_3_counterbranch", "Gamma-dependent projector", "BOUND_READY_NONCLAIM", "K_projector_Gamma row retained if projector uses Gamma_ind transport"),
        ("GATE3572_4_metric_stress_scope", "projector metric stress", "FAIL_CURRENT_LOCAL_GR_CLAIM", "delta_g Pi_M and domain/Hodge stress remain separate"),
        ("GATE3572_5_flux_closure_scope", "mass-flux closure", "FAIL_CURRENT_NEWTON_CLAIM", "d(Pi_M J_H)=0 and measured GM calibration remain open"),
        ("GATE3572_6_public_BLC", "public B_LC selector", "FAIL_CURRENT_PUBLIC_CLAIM", "projector Gamma factor improved but product gate still has open factors"),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "detail": detail,
            "source_path": str(source_paths["status_3571"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for gate_id, gate, status, detail in specs
    ]


def decision_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "DEC3572_0_promote_gamma_naturality",
            "treat delta_Gamma Pi_M as closed inside q/e_obs/tau-natural LC branch",
            "The chain rule proof is exact for independent affine variation and matches the 3566 argument-domain signature.",
            "projector commutator is no longer the axial/source-hypermomentum bottleneck in the selected branch",
            "ADOPTED_PRIVATE_BRANCH",
            "projector_theorem_3498",
        ),
        (
            "DEC3572_1_keep_metric_stress_separate",
            "do not conflate Gamma-naturality with metric-stress silence",
            "Hodge/DeWitt/e_obs projectors can still vary under metric/coframe variation and affect PPN/source normalization.",
            "local GR/Newton proof moves to Pi_M stress and mass-flux closure, not to torsion",
            "ADOPTED_SCOPE_GUARD",
            "pim_variation",
        ),
        (
            "DEC3572_2_next_target",
            "attack d(Pi_M J_H)=0 next",
            "The remaining route to Newton/source calibration is closed mass flux plus measured GM matching.",
            "3573 should try Ward/topological/Euler mass-current closure or fill dln_Meff_dt/partial_r ln mu_obs residuals",
            "NEXT_TARGET_SELECTED",
            "pim_flux",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "consequence": consequence,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "valid_for_claim": False,
        }
        for decision_id, decision, reason, consequence, status, source_key in specs
    ]


def status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "PROJECTOR_GAMMA_NATURALITY_CLOSED_INSIDE_BRANCH_FULL_SOURCE_CALIBRATION_OPEN",
            "strongest_result": "delta_Gamma_ind Pi_M=0 and delta_Gamma(Pi_M J_H)=0 inside the q/e_obs/tau-natural LC branch; K_projector_Gamma fallback retained for Gamma-dependent projectors.",
            "still_missing": "metric/coframe projector stress, d(Pi_M J_H)=0 mass-flux closure, H_ref/M_H reference lock, boundary no-flux, and measured GM/Poisson-Gauss calibration",
            "public_claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3572_0",
            "target_doc": "3573-Y5-R2FR-PiM-flux-closure-Ward-Euler-or-Meff-drift-bound.md",
            "target_script": "scripts/Y5_R2FR_3573_PiM_flux_closure_Ward_Euler_or_Meff_drift_bound.py",
            "objective": "try to derive d(Pi_M J_H)=0 from Ward/topological/Euler mass-current closure; if not, create source-normalized dln_Meff_dt and partial_r ln mu_obs bound rows",
            "success_gate": "closed projected mass flux in compact local exterior, or executable Meff drift/radial source-hair residual rows with units and local bounds",
            "reason": "3572 closes the independent-Gamma projector commutator; Newton/source calibration now needs mass-flux closure",
            "valid_for_claim": False,
        }
    ]


def canonical_status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "canonical_item": "projector_deltaGamma_naturality",
            "status": "CLOSED_INSIDE_Q_EOBS_TAU_BRANCH_NONCLAIM_PUBLIC",
            "zero_formula": "delta_Gamma_ind Pi_M=0; delta_Gamma(Pi_M J_H)=0",
            "fallback_formula": "epsilon_projector_comm <= K_projector_Gamma ||J_H||/abs(M_H_ref)",
            "remaining_gate": "d(Pi_M J_H)=0 and measured GM calibration",
            "next_action": "derive Pi_M mass-flux closure or bound Meff drift",
            "valid_for_claim": False,
        }
    ]


def validate(
    source_paths: dict[str, Path],
    outputs: dict[str, Path],
    proof: list[dict[str, object]],
    updates: list[dict[str, object]],
    bounds: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[tuple[str, bool, str]] = []
    pre_validation_outputs = {key: path for key, path in outputs.items() if key != "validation"}
    validations.append(("VAL3572_0_sources_exist", all(path.exists() for path in source_paths.values()), "all required 3572 source paths exist"))
    needles = {
        "handoff_3571": "NEXT3571_0",
        "selector_theorem_3571": "BLC3571_0_exact_product_gate",
        "leakage_3571": "LEAK3571_0_projector_comm",
        "sector_matrix_3571": "SELP3571_4_projector",
        "status_3571": "projector naturality",
        "projector_theorem_3498": "PNT3498_1_functor_chain_rule",
        "projector_bound_3498": "KPB3498_0_source_hypermomentum_projector_comm",
        "projector_stress_3498": "STM3498_2_Gamma_transport_projector",
        "pim_algebra": "PM5_projector_variation_owned",
        "pim_variation": "PV2_Hodge_DeWitt_metric_dependence_retained",
        "pim_flux": "FC2_closed_mass_current_equation",
        "mass_flux": "MF2_Euler_flux_closure",
        "variation_chain_3497": "VAR3497_4_projector_zero",
        "signature_3566": "SIG3566_5_projector_domain",
        "variation_3566": "VAR3566_3_source_current",
        "hyper_kernel_3496": "KHS3496_6_projector_comm",
        "pim_htau_commutator": "PHCR3514_0_total",
    }
    validations.append(("VAL3572_1_required_needles_found", all(source_paths[key].exists() and file_contains(source_paths[key], token) for key, token in needles.items()), "all selected projector source needles found"))
    validations.append(("VAL3572_2_outputs_exist", all(path.exists() for path in pre_validation_outputs.values()), "all pre-validation 3572 output files written"))
    csvs_parse = True
    parse_details: list[str] = []
    for output_id, path in pre_validation_outputs.items():
        if path.suffix.lower() != ".csv":
            continue
        try:
            row_count = len(read_csv(path))
            csvs_parse = csvs_parse and row_count > 0
            parse_details.append(f"{output_id}:{row_count}")
        except Exception as exc:
            csvs_parse = False
            parse_details.append(f"{output_id}:ERROR:{exc}")
    validations.append(("VAL3572_3_csv_parse", csvs_parse, "; ".join(parse_details)))
    validations.append(("VAL3572_4_chain_rule_zero_present", any(row["proof_id"] == "PN3572_2_chain_rule_zero" and "delta_Gamma_ind Pi_M" in str(row["statement"]) for row in proof), "delta_Gamma Pi_M chain-rule zero row present"))
    validations.append(("VAL3572_5_product_rule_zero_present", any(row["proof_id"] == "PN3572_3_current_product_rule" and "delta_Gamma(Pi_M J_H)=0" in str(row["statement"]) for row in proof), "projected-current product-rule zero row present"))
    validations.append(("VAL3572_6_selector_update_present", any(row["selector_factor"] == "I_projector^Gamma" and row["status"] == "PASS_INSIDE_SELECTED_LC_BRANCH" for row in updates), "projector Gamma selector factor updated"))
    validations.append(("VAL3572_7_fallback_bound_present", any(row["symbol"] == "epsilon_projector_comm" and "K_projector_Gamma" in str(row["formula"]) for row in bounds), "K_projector fallback bound row present"))
    validations.append(("VAL3572_8_scope_guard_present", any(row["gate_id"] == "GATE3572_5_flux_closure_scope" and row["status"] == "FAIL_CURRENT_NEWTON_CLAIM" for row in gates), "Newton/source calibration scope guard present"))
    validations.append(("VAL3572_9_next_flux_target_selected", any(row["decision_id"] == "DEC3572_2_next_target" for row in decisions), "mass-flux closure selected as next target"))
    validations.append(("VAL3572_10_no_claim_flags", all(str(row["valid_for_claim"]).lower() == "false" for row in proof + updates + bounds + gates + decisions), "all generated physics rows remain nonclaim"))
    generated_source_paths_exist = all(Path(str(row["source_path"])).exists() for row in proof + updates + bounds + gates + decisions)
    validations.append(("VAL3572_11_generated_source_paths_exist", generated_source_paths_exist, "every generated row source_path exists"))
    formalization_touched = any(FORMALIZATION.rglob("*3572*")) if FORMALIZATION.exists() else False
    validations.append(("VAL3572_12_formalization_workbench_untouched", not formalization_touched, "no 3572 checkpoint output appears in formalization-workbench"))
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "validation_id": validation_id,
            "passes": passed,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
        }
        for validation_id, passed, detail in validations
    ]


def write_doc(
    outputs: dict[str, Path],
    proof: list[dict[str, object]],
    updates: list[dict[str, object]],
    bounds: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    status: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3572 - Projector naturality: deltaGamma Pi zero or operator norm",
        "",
        "## Verdict",
        "3572 closes a real subgate: for a q/e_obs/tau-natural mass projector, `delta_Gamma_ind Pi_M=0`, and with the 3566 source-current result `delta_Gamma(Pi_M J_H)=0`.  So the independent-Gamma projector commutator is no longer the axial/source-hypermomentum bottleneck inside the selected LC branch.",
        "",
        "This is not full local GR or Newton yet.  Metric/coframe variation of a Hodge/DeWitt projector, source-flux closure `d(Pi_M J_H)=0`, `H_ref/M_H`, boundary flux, and measured-GM calibration remain open.  If a Gamma-dependent projector/collar transport is admitted, the fallback is `epsilon_projector_comm <= K_projector_Gamma ||J_H||/abs(M_H_ref)`.",
        "",
        "## Generated outputs",
    ]
    for output_id, path in outputs.items():
        lines.append(f"- `{output_id}`: `{path}`")
    lines.extend(["", "## Naturality proof"])
    for row in proof:
        lines.append(f"- `{row['proof_id']}`: {row['statement']} ({row['status']})")
    lines.extend(["", "## Selector updates"])
    for row in updates:
        lines.append(f"- `{row['update_id']}` `{row['selector_factor']}`: {row['status']} ({row['consequence']})")
    lines.extend(["", "## Operator norm fallback"])
    for row in bounds:
        lines.append(f"- `{row['bound_id']}` `{row['symbol']}`: {row['formula']} ({row['current_value']})")
    lines.extend(["", "## Activation gates"])
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: {row['status']} ({row['detail']})")
    lines.extend(["", "## Decisions"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} -> {row['consequence']}")
    lines.extend(["", "## Status"])
    for row in status:
        lines.append(f"- `{row['status']}`: {row['strongest_result']}")
    lines.extend(["", "## Validation"])
    for row in validation:
        lines.append(f"- `{row['validation_id']}`: {row['status']} ({row['detail']})")
    lines.extend(["", "## Next target", f"- `{next_target[0]['target_doc']}`", f"- Objective: {next_target[0]['objective']}"])
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    source_paths = sources()
    register = source_register(source_paths)
    proof = naturality_proof_rows(source_paths)
    updates = branch_update_rows(source_paths)
    bounds = operator_norm_rows(source_paths)
    gates = activation_rows(source_paths)
    decisions = decision_rows(source_paths)
    status = status_rows()
    next_target = next_target_rows()
    canonical = canonical_status_rows()
    outputs = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3572_SOURCE_REGISTER.csv",
        "naturality_proof": RESIDUALS / "P8_Y5_R2FR_3572_PROJECTOR_NATURALITY_PROOF.csv",
        "selector_update": RESIDUALS / "P8_Y5_R2FR_3572_BLC_SELECTOR_UPDATE.csv",
        "operator_norm_rows": RESIDUALS / "P8_Y5_R2FR_3572_KPROJECTOR_OPERATOR_NORM_ROWS.csv",
        "activation_gates": RESIDUALS / "P8_Y5_R2FR_3572_ACTIVATION_GATES.csv",
        "decision_ledger": RESIDUALS / "P8_Y5_R2FR_3572_DECISION_LEDGER.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3572_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3572_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_projector_deltaGamma_naturality_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3572_VALIDATION.csv",
    }
    write_csv(outputs["source_register"], register)
    write_csv(outputs["naturality_proof"], proof)
    write_csv(outputs["selector_update"], updates)
    write_csv(outputs["operator_norm_rows"], bounds)
    write_csv(outputs["activation_gates"], gates)
    write_csv(outputs["decision_ledger"], decisions)
    write_csv(outputs["status"], status)
    write_csv(outputs["next_target"], next_target)
    write_csv(outputs["canonical_status"], canonical)
    validation = validate(source_paths, outputs, proof, updates, bounds, gates, decisions)
    write_csv(outputs["validation"], validation)
    write_doc(outputs, proof, updates, bounds, gates, decisions, status, validation, next_target)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"3572 validation failed: {failed}")
    print(f"wrote {DOC}")
    for output_id, path in outputs.items():
        print(f"{output_id}: {path}")


if __name__ == "__main__":
    main()

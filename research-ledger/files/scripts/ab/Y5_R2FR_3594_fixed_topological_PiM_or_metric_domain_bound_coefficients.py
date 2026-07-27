from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3594"
BRANCH_ID = "MTS_R2FR_Y5_FIXED_TOPOLOGICAL_PIM_3594"
DOC = ROOT / "3594-Y5-R2FR-fixed-topological-PiM-or-metric-domain-bound-coefficients.md"


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


def contains(path: Path, needle: str) -> bool:
    return needle in path.read_text(encoding="utf-8-sig", errors="replace")


def sources() -> dict[str, tuple[Path, str]]:
    return {
        "next_3593": (RESIDUALS / "P8_Y5_R2FR_3593_NEXT_TARGET.csv", "NEXT3593_0"),
        "status_3593": (
            RESIDUALS / "P8_Y5_R2FR_3593_STATUS.csv",
            "DELTAPIM_GAMMA_ZERO_DERIVED_TOTAL_BOUND_BRANCH_ACTIVE",
        ),
        "bound_3593": (RESIDUALS / "P8_Y5_R2FR_3593_DELTAPIM_BOUND_INPUT_PACK.csv", "epsilon_PiM_metric"),
        "zero_audit_3593": (
            RESIDUALS / "P8_Y5_R2FR_3593_PIM_PROJECTOR_ZERO_PROOF_AUDIT.csv",
            "ZPIM3593_2_metric_domain_silence",
        ),
        "validation_3593": (RESIDUALS / "P8_Y5_BRR545_3593_VALIDATION.csv", "ALL"),
        "top_closure_500": (RESIDUALS / "P8_TOPOLOGICAL_PIM_CLOSURE_CONDITIONS.csv", "TC500_0_metric_independence"),
        "top_failure_500": (RESIDUALS / "P8_TOPOLOGICAL_PIM_FAILURE_ANALYSIS.csv", "F500_0_conserved_wrong_object"),
        "top_clause_500": (RESIDUALS / "P8_TOPOLOGICAL_PIM_PARENT_CLAUSE_ATTEMPT.csv", "TP500_0_topological_data"),
        "top_decision_500": (RESIDUALS / "P8_TOPOLOGICAL_PIM_DECISION.csv", "D500_3_promotion"),
        "top_certificate_534": (RESIDUALS / "P8_Y5_PIM_TOPO_EQUALITY_CERTIFICATE.csv", "PTEC534_1_metric_independent_projector"),
        "top_acceptance_534": (RESIDUALS / "P8_Y5_PIM_TOPO_EQUALITY_ACCEPTANCE_GATES.csv", "AG534_3_projector_stress_guard"),
        "top_decision_534": (RESIDUALS / "P8_Y5_PIM_TOPO_EQUALITY_DECISION.csv", "D534_2_current_MTS"),
        "pim_variation_contract": (RESIDUALS / "P8_PiM_projector_variation_stress_CONTRACT.csv", "PV1_topological_absolute_charge_route"),
        "pim_algebra_contract": (RESIDUALS / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv", "PM0_fixed_exterior_topology"),
        "pim_flux_contract": (RESIDUALS / "P8_PiM_flux_closure_Ward_topological_CONTRACT.csv", "FC7_absolute_calibration_after_closure"),
        "parent_source_residuals": (RESIDUALS / "P8_PARENT_SOURCE_IDENTITY_RESIDUAL_DECOMPOSITION.csv", "S499_2_domain_projector"),
        "parent_noether": (RESIDUALS / "P8_PARENT_NOETHER_CLOSURE_THEOREM.csv", "T505_source_measure_matching"),
        "local_eh_reqs": (RESIDUALS / "P8_LOCAL_EH_REDUCTION_REQUIREMENTS.csv", "EH505_2_projector_constancy"),
        "min_local_gr_vector": (RESIDUALS / "P8_MIN_PARENT_LOCAL_GR_RESIDUAL_VECTOR.csv", "AR511_5_PiM_variation"),
        "em_hodge_bound": (RESIDUALS / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv", "EMB3503_7_Delta_PiM_metric"),
    }


def outputs() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3594_SOURCE_REGISTER.csv",
        "theorem_attempt": RESIDUALS / "P8_Y5_R2FR_3594_FIXED_TOPOLOGICAL_PIM_THEOREM_ATTEMPT.csv",
        "zero_audit": RESIDUALS / "P8_Y5_R2FR_3594_METRIC_DOMAIN_ZERO_AUDIT.csv",
        "coefficient_rows": RESIDUALS / "P8_Y5_R2FR_3594_KPIM_METRIC_DOMAIN_BOUND_ROWS.csv",
        "residual_update": RESIDUALS / "P8_Y5_R2FR_3594_EPSILON_PIM_RESIDUAL_UPDATE.csv",
        "promotion_gates": RESIDUALS / "P8_Y5_R2FR_3594_PROMOTION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3594_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3594_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_fixed_topological_PiM_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3594_VALIDATION.csv",
    }


def source_register_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    rows = []
    for source_id, (path, needle) in source_map.items():
        exists = path.exists()
        needle_found = exists and (needle == "ALL" or contains(path, needle))
        rows.append(
            {
                "timestamp_utc": now(),
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source_id,
                "source_path": str(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle_found,
                "valid_for_claim": False,
            }
        )
    return rows


def theorem_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        (
            "FTP3594_0_target",
            "remaining 3593 target",
            "Try to prove delta_g Pi_M = D_D Pi_M = 0 by making Pi_M fixed-topological/identity, otherwise bound K_PiM_metric/domain.",
            "3593 removed the independent-Gamma projector term but left metric/domain stress live.",
            "TARGET_IMPORTED",
            "next_3593",
        ),
        (
            "FTP3594_1_topological_definition",
            "fixed topological projector definition",
            "Pi_top J := ell_M(J) omega_M_top, with d omega_M_top=0 and integral_S2 omega_M_top=1 on a parent-selected S2 class.",
            "No Hodge star, DeWitt metric, Green operator, fitted mask, or orbital readout enters the projector definition.",
            "EXACT_DEFINITION_IF_PARENT_SELECTOR_EXISTS",
            "top_clause_500",
        ),
        (
            "FTP3594_2_metric_zero",
            "bulk metric variation zero",
            "delta_g Pi_top = 0",
            "If [S2] and omega_M_top are fixed cohomology data before readout, the local metric does not vary the projector; any metric variation belongs to J_H, not Pi_top.",
            "DERIVED_CONDITIONAL_ZERO",
            "top_certificate_534",
        ),
        (
            "FTP3594_3_domain_isotopy_zero",
            "homology-preserving domain variation",
            "D_D Pi_top[delta D]J = ell_M(J) d alpha_D and integral_boundary d alpha_D = 0 when no support crosses the representative.",
            "A smooth representative shift inside the same homology class changes omega_M_top by an exact form; paired with a closed/source-supported current it contributes only a boundary/support-crossing term.",
            "DERIVED_CONDITIONAL_EXACT_TERM",
            "pim_algebra_contract",
        ),
        (
            "FTP3594_4_identity_branch",
            "identity projector branch",
            "Pi_M = inclusion/identity on the Hilbert mass-current subcomplex implies delta Pi_M = 0 by definition.",
            "This branch kills independent projector stress but shifts the burden to proving the subcomplex itself is parent-owned and equals measured mass.",
            "DERIVED_CONDITIONAL_IDENTITY_ZERO",
            "pim_variation_contract",
        ),
        (
            "FTP3594_5_wrong_object_obstruction",
            "conserved wrong object obstruction",
            "dJ_M_top=0 does not imply Pi_M J_H = J_M_top.",
            "A closed topological current is not automatically the Newtonian/Hilbert source measured by local orbits.",
            "MAIN_BLOCKER_RETAINED",
            "top_failure_500",
        ),
        (
            "FTP3594_6_em_poynting_guard",
            "Hilbert source content guard",
            "J_H must include matter, EM stress, Poynting flux and binding energy exactly once before Pi_M.",
            "The topological branch cannot make source coupling look clean by projecting away real Hilbert stress or double-counting it as a hidden sector.",
            "RETAINED_EXPLICIT_GUARD",
            "em_hodge_bound",
        ),
        (
            "FTP3594_7_verdict",
            "3594 theorem verdict",
            "K_PiM_metric=K_PiM_domain=0 only inside a parent-selected fixed-topological or identity Pi_M branch; current corpus does not certify the parent selector or Hilbert equality.",
            "This advances the least-cheaty zero route but does not give measured-GM/Newton/PPN/local-GR credit.",
            "CONDITIONAL_STRESS_ZERO_TOTAL_CLAIM_BLOCKED",
            "top_decision_534",
        ),
    ]
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": theorem_id,
            "claim_piece": claim_piece,
            "statement": statement,
            "derivation": derivation,
            "status": status,
            "source_path": p[source_id],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for theorem_id, claim_piece, statement, derivation, status, source_id in rows
    ]


def zero_audit_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        ("ZA3594_0_parent_selected_topology", "parent action fixes Sigma_ext and [S2] before readout", "Sigma_ext ~= S2 x I; [S2]_M fixed", "CONDITIONAL_OPEN", "topology route allowed but not certificate-valid", "top_certificate_534"),
        ("ZA3594_1_metric_independent_representative", "Pi_M uses closed topological representative, not Hodge/DeWitt", "delta_g Pi_top=0", "PASS_IF_TOPOLOGICAL_BRANCH", "metric projector stress zero only in this branch", "top_closure_500"),
        ("ZA3594_2_homology_preserving_domain", "domain motion is isotopy/exact and no source support crosses boundary", "D_D Pi_top[delta D] gives exact zero-boundary term", "CONDITIONAL_OPEN", "domain stress remains live if source support or readout mask moves", "pim_variation_contract"),
        ("ZA3594_3_identity_subcomplex", "identity/inclusion projector on parent Hilbert mass subcomplex", "delta Pi_identity=0", "CONDITIONAL_OPEN", "requires parent-owned mass subcomplex", "local_eh_reqs"),
        ("ZA3594_4_hilbert_equality", "topological or identity current equals projected Hilbert source", "Pi_M J_H = J_M^parent or J_M_top + dB_zero", "FAIL_CURRENT_BRANCH", "wrong-conserved-object obstruction remains", "top_failure_500"),
        ("ZA3594_5_flux_calibration", "closed current is calibrated to measured GM", "mu_obs=G_parent Q_M with constant universal G_parent", "FAIL_CURRENT_BRANCH", "Newton/source normalization remains blocked", "pim_flux_contract"),
        ("ZA3594_6_em_poynting_once", "EM/Poynting/binding source accounting is included once", "J_H_total before Pi_M", "OPEN_RETAINED", "prevents matter-only source shortcut", "em_hodge_bound"),
        ("ZA3594_7_total_local_gr", "all local-GR projector/source gates pass", "epsilon_PiM_metric=epsilon_PiM_domain=epsilon_PiM_parent=epsilon_PiM_flux=0", "FAIL_CURRENT_TOTAL", "3594 is a conditional zero theorem plus coefficient pack, not local GR", "status_3593"),
    ]
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "audit_id": audit_id,
            "condition": condition,
            "formula": formula,
            "status": status,
            "consequence": consequence,
            "source_path": p[source_id],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for audit_id, condition, formula, status, consequence, source_id in rows
    ]


def coefficient_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        (
            "KMD3594_0_K_PiM_metric_topological",
            "K_PiM_metric",
            "||delta_g Pi_M||_{J_H->M}",
            "projector operator norm per metric variation",
            "0 if Pi_M=Pi_top or identity branch is parent-certified; else missing",
            "parent-selected fixed-topological/identity theorem, or explicit Hodge/DeWitt variation norm",
            "top_certificate_534",
            "CONDITIONAL_ZERO_OR_BOUND_REQUIRED",
        ),
        (
            "KMD3594_1_K_PiM_domain_topological",
            "K_PiM_domain",
            "||D_D Pi_M||_{J_H->M}",
            "projector operator norm per domain/homology variation",
            "0 for homology-preserving, source-support-silent topological branch; else missing",
            "domain isotopy theorem, no support crossing, or explicit domain/source-support norm",
            "pim_variation_contract",
            "CONDITIONAL_ZERO_OR_BOUND_REQUIRED",
        ),
        (
            "KMD3594_2_K_PiM_Hodge_counterbranch",
            "K_PiM_Hodge",
            "||delta_g Pi_Hodge/DeWitt/Green||_{J_H->M}",
            "projector operator norm per metric/Hodge implementation",
            "MISSING_IF_HODGE_BRANCH_USED",
            "weak-field Hodge/Green stress map, source norm, M_H_ref, local bounds",
            "pim_variation_contract",
            "BOUND_REQUIRED_IF_USED",
        ),
        (
            "KMD3594_3_K_PiM_support_crossing",
            "K_PiM_support",
            "||source support crossing/domain marker response||",
            "domain/source-support envelope",
            "MISSING_IF_DOMAIN_NOT_PARENT_TOPOLOGICAL",
            "source support collar, boundary flux, marker-free theorem, units",
            "parent_source_residuals",
            "BOUND_REQUIRED_IF_USED",
        ),
        (
            "KMD3594_4_epsilon_metric_domain",
            "epsilon_PiM_metric_domain",
            "epsilon_PiM_metric + epsilon_PiM_domain <= (K_PiM_metric ||delta g|| + K_PiM_domain ||delta D||) ||J_H||/abs(M_H_ref) + epsilon_support",
            "dimensionless source-coupling residual",
            "0 only in certified fixed-topological/identity branch; otherwise not score-ready",
            "K coefficients, perturbation norms, source norm, M_H_ref, source paths",
            "bound_3593",
            "TOTAL_METRIC_DOMAIN_BOUND_BRANCH_ACTIVE",
        ),
    ]
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "coefficient_id": coefficient_id,
            "symbol": symbol,
            "definition": definition,
            "units": units,
            "current_value": current_value,
            "required_inputs": required_inputs,
            "source_path": p[source_id],
            "score_status": score_status,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for coefficient_id, symbol, definition, units, current_value, required_inputs, source_id, score_status in rows
    ]


def residual_update_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        ("ERU3594_0_gamma", "epsilon_PiM_Gamma", "zero inside q/e_obs/tau-natural LC branch", "CARRIED_FROM_3593", "bound_3593"),
        ("ERU3594_1_metric_domain", "epsilon_PiM_metric_domain", "conditional zero in fixed-topological/identity branch, otherwise K coefficient bound", "PARTIAL_THEOREM_BOUND_BRANCH", "coefficient_rows"),
        ("ERU3594_2_parent_current", "epsilon_PiM_parent", "still requires Pi_M J_H = J_M^parent or topological-Hilbert equality", "OPEN_MAIN_BLOCKER", "top_failure_500"),
        ("ERU3594_3_flux_calibration", "epsilon_PiM_flux", "still requires d(Pi_M J_H)=0 and measured GM calibration", "OPEN_MAIN_BLOCKER", "pim_flux_contract"),
        ("ERU3594_4_em_poynting", "epsilon_PiM_EM_accounting", "retained until EM/Poynting/binding energy enters J_H_total once", "OPEN_RETAINED", "em_hodge_bound"),
        ("ERU3594_5_total", "epsilon_PiM", "metric/domain route sharpened but total source coupling remains not score-ready", "NOT_SCORE_READY_TOTAL", "status_3593"),
    ]
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "update_id": update_id,
            "symbol": symbol,
            "update": update,
            "status": status,
            "source_path": str(source_map[source_id][0]) if source_id != "coefficient_rows" else str(outputs()["coefficient_rows"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for update_id, symbol, update, status, source_id in rows
    ]


def promotion_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {key: str(value[0]) for key, value in source_map.items()}
    rows = [
        ("PROM3594_0_metric_domain_zero", "K_PiM_metric=K_PiM_domain=0", "PASS_CONDITIONAL_BRANCH_ONLY", "only if fixed-topological/identity parent selector is certified", "top_certificate_534"),
        ("PROM3594_1_total_DeltaPiM", "Delta_PiM=0", "FAIL_CURRENT_CLAIM", "wrong object, Hilbert equality, flux, calibration, EM accounting remain open", "top_failure_500"),
        ("PROM3594_2_bound_rows", "K_PiM coefficient rows exist", "PASS_NONCLAIM", "rows are source-ready but not numeric/score-ready", "bound_3593"),
        ("PROM3594_3_no_multiplier_cheat", "no late multiplier/source-normalization shortcut", "PASS_GUARD", "closure multiplier remains assumption unless independently owned", "top_closure_500"),
        ("PROM3594_4_no_local_gr_claim", "no Newton/PPN/local-GR promotion", "PASS_GUARD", "projector stress improved but source coupling not finished", "min_local_gr_vector"),
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
            "source_path": p[source_id],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for gate_id, gate, status, consequence, source_id in rows
    ]


def status_rows(source_map: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "FIXED_TOPOLOGICAL_PIM_STRESS_ZERO_CONDITIONAL_SOURCE_EQUALITY_BLOCKED",
            "strongest_result": "3594 derives the clean projector-stress route: if Pi_M is parent-selected fixed topological data, Pi_top J=ell_M(J) omega_M_top with closed normalized omega_M_top, then delta_g Pi_M=0 and homology-preserving domain variation is exact/boundary-silent. The identity subcomplex branch has the same projector-stress zero. Current MTS still lacks the parent selector and Hilbert/source equality, so the closed topological object may be the wrong conserved charge.",
            "decision": "use K_PiM_metric=K_PiM_domain=0 only as a conditional private branch; otherwise carry K_PiM_metric, K_PiM_domain, K_PiM_Hodge and K_PiM_support coefficient rows with no local-GR/Newton claim",
            "still_missing": "parent-selected topology/domain, Pi_M J_H=J_M^parent or J_M_top+dB_zero, d(Pi_M J_H)=0, Poisson/Gauss/orbital calibration, EM/Poynting once-only Hilbert source accounting, numeric coefficient rows for non-topological branches",
            "public_claim_allowed": False,
            "valid_for_claim": False,
            "source_path": str(source_map["top_certificate_534"][0]),
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3594_0",
            "target_doc": "3595-Y5-R2FR-Hilbert-source-to-topological-charge-glue-or-wrong-object-bound.md",
            "target_script": "scripts/Y5_R2FR_3595_Hilbert_source_to_topological_charge_glue_or_wrong_object_bound.py",
            "objective": "attack the conserved-wrong-object blocker: prove the fixed-topological/identity mass charge is the same Hilbert source charge measured by local orbits, or create explicit epsilon_PiM_parent/wrong-object bound rows",
            "success_gate": "Pi_M J_H = J_M^parent or J_M_top+dB_zero with zero boundary term and EM/Poynting included once; otherwise source-ready wrong-object residual rows remain nonclaim",
            "reason": "3594 conditionally kills projector metric/domain stress, leaving Hilbert/source equality as the dominant source-coupling obstruction",
            "valid_for_claim": False,
        }
    ]


def validation_rows(
    source_map: dict[str, tuple[Path, str]],
    out_paths: dict[str, Path],
    theorem: list[dict[str, object]],
    audit: list[dict[str, object]],
    coeffs: list[dict[str, object]],
    residual_update: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[tuple[str, bool, str]] = []
    validations.append(("VAL3594_0_sources_exist", all(path.exists() for path, _ in source_map.values()), "all required 3594 source paths exist"))
    validations.append(("VAL3594_1_needles_found", all(path.exists() and (needle == "ALL" or contains(path, needle)) for path, needle in source_map.values()), "all selected 3594 source anchors found"))
    pre_validation = {key: path for key, path in out_paths.items() if key != "validation"}
    validations.append(("VAL3594_2_outputs_exist", all(path.exists() for path in pre_validation.values()), "all pre-validation 3594 csv output files written"))
    parse_ok = True
    parse_details: list[str] = []
    for output_id, path in pre_validation.items():
        try:
            parse_details.append(f"{output_id}:{len(read_csv(path))}")
        except Exception as exc:
            parse_ok = False
            parse_details.append(f"{output_id}:ERROR:{exc}")
    validations.append(("VAL3594_3_csv_parse", parse_ok, "; ".join(parse_details)))
    validations.append(("VAL3594_4_metric_zero_conditional", any(row["theorem_id"] == "FTP3594_2_metric_zero" and row["status"] == "DERIVED_CONDITIONAL_ZERO" for row in theorem), "metric projector zero theorem row present"))
    validations.append(("VAL3594_5_domain_exact_conditional", any(row["theorem_id"] == "FTP3594_3_domain_isotopy_zero" and row["status"] == "DERIVED_CONDITIONAL_EXACT_TERM" for row in theorem), "domain isotopy exact-term row present"))
    validations.append(("VAL3594_6_wrong_object_blocked", any(row["audit_id"] == "ZA3594_4_hilbert_equality" and row["status"] == "FAIL_CURRENT_BRANCH" for row in audit), "wrong-object/Hilbert equality blocker remains explicit"))
    required_coeffs = {"K_PiM_metric", "K_PiM_domain", "K_PiM_Hodge", "K_PiM_support", "epsilon_PiM_metric_domain"}
    validations.append(("VAL3594_7_coefficients_complete", required_coeffs.issubset({str(row["symbol"]) for row in coeffs}), "metric/domain coefficient rows complete"))
    validations.append(("VAL3594_8_residual_update_complete", {"epsilon_PiM_metric_domain", "epsilon_PiM_parent", "epsilon_PiM_flux", "epsilon_PiM_EM_accounting", "epsilon_PiM"}.issubset({str(row["symbol"]) for row in residual_update}), "epsilon_PiM residual update includes main blockers"))
    validations.append(("VAL3594_9_no_claim_flags", not any(str(row.get("valid_for_claim", "False")).lower() == "true" or str(row.get("claim_allowed", "False")).lower() == "true" for table in [theorem, audit, coeffs, residual_update, gates, status] for row in table), "all generated physics rows remain nonclaim"))
    validations.append(("VAL3594_10_no_local_gr_claim", any(row["gate_id"] == "PROM3594_4_no_local_gr_claim" and row["status"] == "PASS_GUARD" for row in gates), "Newton/PPN/local-GR claim guard is active"))
    validations.append(("VAL3594_11_next_target_selected", any(row["next_id"] == "NEXT3594_0" for row in next_target), "3595 Hilbert-source/topological-charge glue target selected"))
    source_paths = [Path(str(row["source_path"])) for table in [theorem, audit, coeffs, residual_update, gates, status] for row in table if row.get("source_path")]
    validations.append(("VAL3594_12_generated_source_paths_exist", all(path.exists() for path in source_paths), "every generated row source_path exists"))
    formal_hits = list(FORMALIZATION.rglob("*3594*")) if FORMALIZATION.exists() else []
    validations.append(("VAL3594_13_formalization_workbench_untouched", len(formal_hits) == 0, "no 3594 checkpoint output appears in formalization-workbench"))
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


def write_doc(theorem, audit, coeffs, residual_update, gates, status, next_target, validation) -> None:
    lines = [
        "# 3594 - Fixed-topological PiM or metric/domain bound coefficients",
        "",
        "## Verdict",
        "3594 gets a useful conditional theorem: a parent-selected fixed-topological `Pi_M` or identity subcomplex projector has no independent metric/domain projector stress.  That means `K_PiM_metric=K_PiM_domain=0` is mathematically legal inside that branch.",
        "",
        "But it still does **not** prove source coupling, Newton, PPN, or local GR, because the fixed topological charge can still be the wrong conserved object unless it equals the Hilbert/source mass seen by local orbits.",
        "",
        "## Theorem Attempt",
    ]
    for row in theorem:
        lines.append(f"- `{row['theorem_id']}`: {row['status']} - {row['statement']}")
    lines.extend(["", "## Zero Audit"])
    for row in audit:
        lines.append(f"- `{row['audit_id']}`: {row['status']} - {row['condition']}")
    lines.extend(["", "## Coefficient Rows"])
    for row in coeffs:
        lines.append(f"- `{row['coefficient_id']}` / `{row['symbol']}`: {row['score_status']} - {row['definition']}")
    lines.extend(["", "## Residual Update"])
    for row in residual_update:
        lines.append(f"- `{row['update_id']}` / `{row['symbol']}`: {row['status']} - {row['update']}")
    lines.extend(["", "## Promotion Gates"])
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: {row['status']} - {row['consequence']}")
    lines.extend(["", "## Status"])
    for row in status:
        lines.append(f"- `{row['status']}`: {row['strongest_result']}")
        lines.append(f"- Decision: {row['decision']}")
        lines.append(f"- Still missing: {row['still_missing']}")
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
    theorem = theorem_rows(source_map)
    audit = zero_audit_rows(source_map)
    coeffs = coefficient_rows(source_map)
    residual_update = residual_update_rows(source_map)
    gates = promotion_rows(source_map)
    status = status_rows(source_map)
    next_target = next_target_rows()

    write_csv(out_paths["source_register"], register)
    write_csv(out_paths["theorem_attempt"], theorem)
    write_csv(out_paths["zero_audit"], audit)
    write_csv(out_paths["coefficient_rows"], coeffs)
    write_csv(out_paths["residual_update"], residual_update)
    write_csv(out_paths["promotion_gates"], gates)
    write_csv(out_paths["status"], status)
    write_csv(out_paths["next_target"], next_target)
    write_csv(out_paths["canonical_status"], status)

    validation = validation_rows(source_map, out_paths, theorem, audit, coeffs, residual_update, gates, status, next_target)
    write_csv(out_paths["validation"], validation)
    write_doc(theorem, audit, coeffs, residual_update, gates, status, next_target, validation)

    print(f"wrote {DOC}")
    for output_id, path in out_paths.items():
        print(f"{output_id}: {path}")


if __name__ == "__main__":
    main()

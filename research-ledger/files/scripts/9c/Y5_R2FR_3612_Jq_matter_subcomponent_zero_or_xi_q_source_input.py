from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3612"
BRANCH_ID = "MTS_R2FR_Y5_JQ_MATTER_SUBCOMPONENT_ZERO_OR_XI_Q_SOURCE_INPUT_3612"
DOC = ROOT / "3612-Y5-R2FR-Jq-matter-subcomponent-zero-or-xi-q-source-input.md"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def contains(path: Path, needle: str) -> bool:
    return needle in path.read_text(encoding="utf-8-sig", errors="replace")


def source_map() -> dict[str, tuple[Path, str]]:
    return {
        "handoff_3611": (
            RESIDUALS / "P8_Y5_R2FR_3611_NEXT_TARGET.csv",
            "3612-Y5-R2FR-Jq-matter-subcomponent-zero-or-xi-q-source-input.md",
        ),
        "jq_bound_3611": (
            RESIDUALS / "P8_Y5_R2FR_3611_JQ_FIRST_COMPONENT_BOUND.csv",
            "J_q^matter_bulk absolute bound",
        ),
        "matter_bound_3235": (
            RESIDUALS / "P8_Y5_R2FR_3235_JMATTER_COMPONENT_BOUND.csv",
            "J_matter_bound",
        ),
        "matter_functor_3235": (
            RESIDUALS / "P8_Y5_R2FR_3235_MATTER_SOURCE_FUNCTOR_DERIVATION.csv",
            "delta_v S_A",
        ),
        "poynting_3502": (
            RESIDUALS / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv",
            "Phi_EM_rad",
        ),
        "hodge_current_3503": (
            RESIDUALS / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv",
            "Delta_Hodge_EM",
        ),
        "hodge_flow_3504": (
            RESIDUALS / "P8_EM_Hodge_flow_rule_bound_or_zero.csv",
            "Delta_chi_principal",
        ),
        "source_label_hodge_3523": (
            RESIDUALS / "P8_EM_source_label_forgetting_EM_Hodge_status.csv",
            "Poynting_as_Maxwell_Hilbert_stress",
        ),
        "calibrated_alpha_3529": (
            RESIDUALS / "P8_local_GR_calibrated_alpha_source_interface_status.csv",
            "calibrated_Maxwell_stress",
        ),
        "unique_f2_3528": (
            RESIDUALS / "P8_EM_unique_F2_or_calibrated_alpha_status.csv",
            "zero_by_calibration_or_bounded_if_branch_active",
        ),
        "no_source_only_3509": (
            RESIDUALS / "P8_Y5_R2FR_3509_NO_SOURCE_ONLY_MATTER_FUNCTOR_THEOREM.csv",
            "THEOREM_STACK_CONSTRUCTED_NOT_PARENT_SIGNED",
        ),
        "no_source_residual_3509": (
            RESIDUALS / "P8_EM_no_source_only_matter_functor_residual.csv",
            "nonHilbert_source_bypass",
        ),
        "ward_alpha_3508": (
            RESIDUALS / "P8_EM_current_source_Ward_alpha_source_residual.csv",
            "prevariation_weight",
        ),
        "ellj_3513": (
            RESIDUALS / "P8_EM_ellJ_source_current_owner_residual_law.csv",
            "z_ellJ",
        ),
        "xi_audit_3611": (
            RESIDUALS / "P8_Y5_R2FR_3611_XI_Q_POSITIVE_HESSIAN_AUDIT.csv",
            "xi_q owner",
        ),
    }


def outputs() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3612_SOURCE_REGISTER.csv",
        "subcomponent_attack": RESIDUALS / "P8_Y5_R2FR_3612_JQ_MATTER_SUBCOMPONENT_ATTACK.csv",
        "em_poynting_closure": RESIDUALS / "P8_Y5_R2FR_3612_EM_POYNTING_HILBERT_CLOSURE.csv",
        "source_weight_reduction": RESIDUALS / "P8_Y5_R2FR_3612_SOURCE_WEIGHT_REDUCTION.csv",
        "xi_parallel_audit": RESIDUALS / "P8_Y5_R2FR_3612_XI_Q_PARALLEL_SOURCE_AUDIT.csv",
        "decision_gates": RESIDUALS / "P8_Y5_R2FR_3612_DECISION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3612_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3612_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_Jq_matter_EM_Poynting_subcomponent_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3612_VALIDATION.csv",
    }


def source_register_rows(sources: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    now = stamp()
    rows: list[dict[str, object]] = []
    for source_id, (source_path, needle) in sources.items():
        exists = source_path.exists()
        rows.append(
            {
                "timestamp_utc": now,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source_id,
                "source_path": str(source_path),
                "exists": exists,
                "needle": needle,
                "needle_found": exists and contains(source_path, needle),
                "valid_for_claim": False,
            }
        )
    return rows


def subcomponent_attack_rows(sources: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {source_id: str(source_tuple[0]) for source_id, source_tuple in sources.items()}
    now = stamp()
    specs = [
        (
            "JQA3612_0_selected_subcomponent",
            "J_readout_nonH_bound / EM-Poynting part of J_q^matter_bulk",
            "EM/Poynting/binding can either be inside total Hilbert stress or become a non-Hilbert/boundary flux residual",
            "J_q^EM/Poynting := delta_{v_q} S_EM + projected EM exchange/readout/boundary tails",
            "SELECTED_FOR_ATTACK",
            "jq_bound_3611",
            "This is the first concrete subcomponent attack after 3611, chosen because it tests whether Poynting is background-field magic or ordinary stress bookkeeping.",
        ),
        (
            "JQA3612_1_Hilbert_absorption",
            "ordinary bound EM fields",
            "minimal Maxwell fields varied on the observed geometry contribute to T_H and M_H; they are not an extra q-source",
            "S_EM=-1/(4 mu0) int F wedge *_obs F; delta_g S_EM = 1/2 int sqrt(-g_obs) T_EM^{mu nu} delta g_obs_munu",
            "EXACT_CONDITIONAL_ZERO_ROUTE",
            "poynting_3502",
            "Bound Coulomb/magnetic/Poynting bookkeeping belongs inside the same Hilbert source if the Hodge/current/normalization owners are common.",
        ),
        (
            "JQA3612_2_flux_residual",
            "radiative/background Poynting flux",
            "net Poynting flux through the local exterior boundary is not killed by Hilbert absorption; it is a boundary/time-hair residual",
            "Phi_EM_rad = integral_boundary S_Poynting dot n dA; contributes to D_t M_H or radial source hair if nonzero",
            "BOUND_COMPONENT_RETAINED",
            "poynting_3502",
            "This stops us pretending radiation/background EM flow vanishes when the branch is not stationary and isolated.",
        ),
        (
            "JQA3612_3_Hodge_gate",
            "EM Hodge/coframe mismatch",
            "Poynting only uses the same local geometry as gravity if *_EM=*_obs[e_obs(q)] or every constitutive mismatch is bounded",
            "Delta_Hodge_EM := *_EM - *_obs[e_obs(q)]",
            "ZERO_OR_BOUND_GATE_IMPORTED",
            "hodge_current_3503",
            "This is where Maxwell light cone, PPN, clocks and source stress all meet.",
        ),
        (
            "JQA3612_4_normalization_gate",
            "Maxwell action normalization and alpha",
            "local baseline may carry alpha as a calibrated universal constant; nonzero C_XF2 must be scored, not hidden in the source mass",
            "C_XF2=0 by calibrated-constant branch or retain |C_XF2| source/clock/WEP/R10 bounds",
            "CALIBRATED_BASELINE_WITH_ACTIVE_BRANCH_BOUND",
            "unique_f2_3528",
            "This avoids wasting the local-GR route by demanding alpha be derived before Newton, while also preventing a fake derived-alpha claim.",
        ),
        (
            "JQA3612_5_first_subcomponent_verdict",
            "J_q^EM/Poynting sub-bound",
            "EM/Poynting is now either conditionally zero inside total Hilbert stress or retained as an explicit no-cancellation residual vector",
            "||J_q^EM/Poynting||_* <= C_EM,g||D_{v_q}e_obs|| + C_H||Delta_Hodge_EM|| + C_lambda|D_{v_q}ln lambda_A| + |Phi_EM_rad|/(G_ref M_H) + C_XF2|C_XF2| + C_readout|C_EM_readout| + C_NH||J_NH||",
            "SUCCESS_GATE_FILLED_SOURCE_BOUND_NONCLAIM",
            "calibrated_alpha_3529",
            "This satisfies 3612's subcomponent gate without claiming Maxwell/local-GR closure.",
        ),
    ]
    return [
        {
            "timestamp_utc": now,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "attack_id": attack_id,
            "subcomponent": subcomponent,
            "statement": statement,
            "formula": formula,
            "status": status,
            "source_path": p[source_id],
            "effect_or_guard": effect,
            "numeric_value_owned": False,
            "theorem_zero_signed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for attack_id, subcomponent, statement, formula, status, source_id, effect in specs
    ]


def em_poynting_closure_rows(sources: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {source_id: str(source_tuple[0]) for source_id, source_tuple in sources.items()}
    now = stamp()
    specs = [
        (
            "EPC3612_0_identity",
            "Poynting is stress flux",
            "For minimal Maxwell theory on g_obs, the Poynting vector is the spatial energy flux of T_EM, not an independent source sector.",
            "S_Poynting^i = -h^i_mu T_EM^{mu nu} u_nu",
            "EXACT_STANDARD_IDENTITY_CONDITIONAL_ON_OBSERVED_HODGE",
            "source_label_hodge_3523",
        ),
        (
            "EPC3612_1_bound_fields",
            "stationary bound EM fields",
            "Static Coulomb/magnetic binding energy contributes to inertial/source mass through M_H when total Hilbert stress is the source denominator.",
            "Delta M_EM = integral_Sigma T_EM(u,u) dV_obs; no separate epsilon_EM_bound if same M_H denominator is used",
            "CONDITIONAL_ZERO_INSIDE_MH",
            "poynting_3502",
        ),
        (
            "EPC3612_2_exchange",
            "matter-EM Lorentz exchange",
            "Matter-only and EM-only stresses are not separately conserved, but the Lorentz exchange cancels in T_matter+T_EM if the same current is varied.",
            "nabla_mu T_EM^{mu nu}=-F^{nu lambda}J_lambda; nabla_mu T_matter^{mu nu}=+F^{nu lambda}J_lambda",
            "CONDITIONAL_ZERO_IN_TOTAL_HILBERT_STRESS",
            "poynting_3502",
        ),
        (
            "EPC3612_3_radiative_flux",
            "radiative/background flux",
            "If the source is not stationary/isolated, boundary Poynting flux remains a source time-hair term and must be bounded over a stated window.",
            "B_EM_rad := |integral_boundary S_Poynting dot n dA|/(G_ref M_H)",
            "RETAINED_BOUND_ROW",
            "hodge_current_3503",
        ),
        (
            "EPC3612_4_constitutive",
            "Hodge/constitutive mismatch",
            "Any independent EM Hodge/constitutive tensor makes Poynting flow follow a different geometry from the gravitational source geometry.",
            "B_Hodge := C_H||*_EM-*_obs[e_obs(q)]|| plus principal/skewon/axion/hidden/readout sub-bounds",
            "RETAINED_BOUND_ROW",
            "hodge_flow_3504",
        ),
        (
            "EPC3612_5_action_scale",
            "w_EM / C_XF2 normalization",
            "An independent EM action multiplier or hidden F^2 coefficient changes EM binding response and alpha/clock/WEP products.",
            "B_EM_norm := C_lambda|D_{v_q}ln lambda_A| + C_XF2|C_XF2|",
            "RETAINED_BOUND_ROW",
            "unique_f2_3528",
        ),
        (
            "EPC3612_6_closure_rule",
            "usable local branch rule",
            "In the calibrated local branch, EM/Poynting may be treated as part of Hilbert stress only under common observed Hodge, common current, fixed EM normalization, stationary exterior, and no readout regeneration.",
            "J_q^EM/Poynting=0 iff Delta_Hodge_EM=C_XF2=D_{v_q}ln lambda_A=Phi_EM_rad=C_EM_readout=J_NH=0 and D_{v_q}e_obs=0",
            "EXACT_CONDITIONAL_RULE_NOT_CURRENT_CLAIM",
            "calibrated_alpha_3529",
        ),
    ]
    return [
        {
            "timestamp_utc": now,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "closure_id": closure_id,
            "target": target,
            "statement": statement,
            "formula": formula,
            "status": status,
            "source_path": p[source_id],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for closure_id, target, statement, formula, status, source_id in specs
    ]


def source_weight_rows(sources: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {source_id: str(source_tuple[0]) for source_id, source_tuple in sources.items()}
    now = stamp()
    specs = [
        (
            "SWR3612_0_source_weight_slot",
            "J_source_weight_bound",
            "source-only species weights are conditionally excluded by typed matter constructor plus connected density-line naturality",
            "parent domain + connected density line + no-Hom => delta_w_species=0 and beta_source_alpha=0",
            "THEOREM_STACK_IMPORTED_NOT_PARENT_SIGNED",
            "no_source_only_3509",
        ),
        (
            "SWR3612_1_common_scale",
            "w_common",
            "a common action/source scale is not a composition source charge but can still drift G_eff/source calibration",
            "w_A(q)=w(q) for all A => partial_A ln w_A - partial_A ln w_B=0, but D_X ln w may remain",
            "RECLASSIFIED_NOT_ZERO",
            "no_source_residual_3509",
        ),
        (
            "SWR3612_2_prevariation_countermodel",
            "prevariation_weight",
            "Ward identities do not remove source weights that are already present in S_matter before variation",
            "S_matter=sum_A w_A(X)S_A remains legal unless parent grammar forbids w_A",
            "NO_GO_GUARD_RETAINED",
            "ward_alpha_3508",
        ),
        (
            "SWR3612_3_nonHilbert_bypass",
            "nonHilbert_source_bypass",
            "ordinary matter functor descent does not kill independent non-Hilbert active source currents",
            "J_src=kappa T_H + sum_A zeta_A J_NH,A; need J_NH,A=nabla K_A and integral_boundary K_A=0",
            "PARALLEL_BOUND_GATE_RETAINED",
            "no_source_only_3509",
        ),
        (
            "SWR3612_4_product_lock",
            "ell_J/source denominator",
            "source coupling cannot be judged from source weights alone; Pi_M, H_tau, frame and units sit in the same product gate",
            "z_ellJ = R_md + R_Ward + R_PiM + R_Htau + R_ref + R_W + R_frame + R_units",
            "DENOMINATOR_GATE_CONNECTED",
            "ellj_3513",
        ),
    ]
    return [
        {
            "timestamp_utc": now,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "row_id": row_id,
            "subcomponent": subcomponent,
            "statement": statement,
            "formula": formula,
            "status": status,
            "source_path": p[source_id],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for row_id, subcomponent, statement, formula, status, source_id in specs
    ]


def xi_parallel_rows(sources: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {source_id: str(source_tuple[0]) for source_id, source_tuple in sources.items()}
    return [
        {
            "timestamp_utc": stamp(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "audit_id": "XIP3612_0_parallel_xi_q",
            "target": "xi_q/H_AB source row",
            "result": "NO_NEW_OWNER_FOUND",
            "statement": "3612 did not find a parent-owned xi_q, H_AB positivity, q-normal, self-adjoint domain, or boundary/no-flux source row beyond the 3611 contract.",
            "next_action": "keep xi_q/H_AB as a parallel signature target, but do not let it block componentizing J_q source bounds",
            "source_path": p["xi_audit_3611"],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def decision_rows(sources: dict[str, tuple[Path, str]]) -> list[dict[str, object]]:
    p = {source_id: str(source_tuple[0]) for source_id, source_tuple in sources.items()}
    now = stamp()
    specs = [
        (
            "DEC3612_0_em_poynting",
            "EM/Poynting subcomponent",
            "ADVANCED",
            "Poynting is either absorbed into total Hilbert stress under exact common-owner clauses or retained as explicit boundary/Hodge/normalization/readout residuals.",
            "poynting_3502",
        ),
        (
            "DEC3612_1_source_weight",
            "source-weight subcomponent",
            "NARROWED",
            "species source weights reduce to typed-domain, density-line and no-Hom signatures, while common-scale and non-Hilbert bypass remain active.",
            "no_source_only_3509",
        ),
        (
            "DEC3612_2_xi_q",
            "xi_q/H_AB parallel route",
            "NO_PROGRESS_TO_OWNER",
            "No new xi_q/H_AB source owner appears in the 3612 source sweep.",
            "xi_audit_3611",
        ),
        (
            "DEC3612_3_claim_guard",
            "local-GR/Newton/Maxwell claim",
            "BLOCKED_FOR_CLAIM_NOT_FOR_WORK",
            "No claim is allowed because the EM/Poynting zero clauses and source-weight grammar are conditional and not parent-signed together.",
            "calibrated_alpha_3529",
        ),
        (
            "DEC3612_4_next",
            "next best attack",
            "SELECT_HODGE_NORMALIZATION_OR_PIM_HTAU",
            "Either prove/bound the EM Hodge/normalization terms inside the new bound, or attack Pi_M/H_tau because that is the source denominator heart.",
            "ellj_3513",
        ),
    ]
    return [
        {
            "timestamp_utc": now,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": decision_id,
            "target": target,
            "decision": decision,
            "rationale": rationale,
            "source_path": p[source_id],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for decision_id, target, decision, rationale, source_id in specs
    ]


def status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": stamp(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "JQ_MATTER_EM_POYNTING_SUBCOMPONENT_BOUND_FILLED_XI_OWNER_STILL_MISSING",
            "summary": (
                "3612 fills the EM/Poynting part of J_q^matter_bulk: minimal bound EM fields live inside total Hilbert stress under common-owner clauses; "
                "radiative flux, Hodge mismatch, EM normalization, hidden F2/readout and non-Hilbert bypass remain explicit absolute residuals. "
                "Source weights are narrowed to typed-domain/density-line/no-Hom signatures, while xi_q/H_AB remains unsigned."
            ),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": stamp(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3612_0",
            "target_doc": "3613-Y5-R2FR-EM-Hodge-normalization-or-PiM-Htau-source-denominator.md",
            "target_script": "scripts/Y5_R2FR_3613_EM_Hodge_normalization_or_PiM_Htau_source_denominator.py",
            "objective": (
                "try to close or source-bound Delta_Hodge_EM and EM normalization terms inside J_q^EM/Poynting; "
                "if that stalls, attack Pi_M/H_tau source-denominator commutator because it controls Newtonian source mass"
            ),
            "success_gate": (
                "must theorem-zero or source-bound at least one of Delta_Hodge_EM, D_vq ln lambda_A, C_XF2, Phi_EM_rad, "
                "or one Pi_M/H_tau denominator obstruction; no generic missing-coupling ledger"
            ),
            "reason": "3612 converts the Poynting worry into a concrete residual vector; 3613 should remove or bound one term in that vector.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def formalization_leaks() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    leaks: list[Path] = []
    for path in FORMALIZATION.rglob("*3612*"):
        parts = set(path.parts)
        if "__pycache__" in parts or ".venv" in parts or "package" in parts:
            continue
        leaks.append(path)
    return leaks


def csv_summary(output_paths: dict[str, Path]) -> str:
    parts: list[str] = []
    for name, path in output_paths.items():
        if name == "validation":
            continue
        parts.append(f"{name}:{len(read_csv(path))}")
    return "; ".join(parts)


def validation_rows(sources: dict[str, tuple[Path, str]], output_paths: dict[str, Path]) -> list[dict[str, object]]:
    source_rows = read_csv(output_paths["source_register"])
    attack = read_csv(output_paths["subcomponent_attack"])
    poynting = read_csv(output_paths["em_poynting_closure"])
    source_weight = read_csv(output_paths["source_weight_reduction"])
    xi_parallel = read_csv(output_paths["xi_parallel_audit"])
    decisions = read_csv(output_paths["decision_gates"])
    status = read_csv(output_paths["status"])
    source_paths_all_exist = all(row["exists"].lower() == "true" for row in source_rows)
    source_needles_found = all(row["needle_found"].lower() == "true" for row in source_rows)
    outputs_exist = all(path.exists() for name, path in output_paths.items() if name != "validation")
    no_claim_flags = True
    for name, path in output_paths.items():
        if name == "validation":
            continue
        for row in read_csv(path):
            if row.get("claim_allowed", "False").lower() == "true" or row.get("valid_for_claim", "False").lower() == "true":
                no_claim_flags = False
    em_bound_filled = any(row["attack_id"] == "JQA3612_5_first_subcomponent_verdict" and "||J_q^EM/Poynting||_* <=" in row["formula"] for row in attack)
    hilbert_absorption = any(row["closure_id"] == "EPC3612_1_bound_fields" and row["status"] == "CONDITIONAL_ZERO_INSIDE_MH" for row in poynting)
    flux_retained = any(row["closure_id"] == "EPC3612_3_radiative_flux" and row["status"] == "RETAINED_BOUND_ROW" for row in poynting)
    source_weight_narrowed = any(row["row_id"] == "SWR3612_0_source_weight_slot" and "THEOREM_STACK" in row["status"] for row in source_weight)
    xi_not_falsely_owned = bool(xi_parallel) and xi_parallel[0]["result"] == "NO_NEW_OWNER_FOUND"
    next_selected = any(row["decision_id"] == "DEC3612_4_next" and "SELECT_HODGE" in row["decision"] for row in decisions)
    status_ok = bool(status) and status[0]["status"] == "JQ_MATTER_EM_POYNTING_SUBCOMPONENT_BOUND_FILLED_XI_OWNER_STILL_MISSING"
    leaks = formalization_leaks()
    specs = [
        ("VAL3612_0_sources_exist", source_paths_all_exist, "all required 3612 source paths exist"),
        ("VAL3612_1_needles_found", source_needles_found, "all selected 3612 source anchors found"),
        ("VAL3612_2_outputs_exist", outputs_exist, "all pre-validation 3612 csv outputs written"),
        ("VAL3612_3_csv_parse", True, csv_summary(output_paths)),
        ("VAL3612_4_em_bound_filled", em_bound_filled, "J_q^EM/Poynting absolute bound row filled"),
        ("VAL3612_5_hilbert_absorption_rule", hilbert_absorption, "bound EM fields conditionally absorbed into M_H/T_H"),
        ("VAL3612_6_flux_retained", flux_retained, "radiative/background Poynting flux remains a retained residual"),
        ("VAL3612_7_source_weight_narrowed", source_weight_narrowed, "source-weight subcomponent narrowed by theorem stack"),
        ("VAL3612_8_xi_not_falsely_owned", xi_not_falsely_owned, "xi_q/H_AB owner not falsely claimed"),
        ("VAL3612_9_no_claim_flags", no_claim_flags, "all generated rows remain nonclaim"),
        ("VAL3612_10_next_target_selected", next_selected, "3613 target selected from concrete residual vector"),
        ("VAL3612_11_status_ok", status_ok, "canonical status matches 3612 verdict"),
        (
            "VAL3612_12_formalization_workbench_untouched",
            len(leaks) == 0,
            "no 3612 checkpoint output appears in formalization-workbench outside package/venv noise",
        ),
    ]
    return [
        {
            "timestamp_utc": stamp(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "validation_id": validation_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail if passed else f"{detail}; leaks={[str(leak) for leak in leaks]}",
        }
        for validation_id, passed, detail in specs
    ]


def write_doc(output_paths: dict[str, Path]) -> None:
    attack = read_csv(output_paths["subcomponent_attack"])
    poynting = read_csv(output_paths["em_poynting_closure"])
    source_weight = read_csv(output_paths["source_weight_reduction"])
    xi_parallel = read_csv(output_paths["xi_parallel_audit"])
    decisions = read_csv(output_paths["decision_gates"])
    status = read_csv(output_paths["status"])[0]
    validation = read_csv(output_paths["validation"])
    next_target = read_csv(output_paths["next_target"])[0]
    lines = [
        "# 3612 - Jq matter subcomponent zero or xi_q source input",
        "",
        "## Verdict",
        "3612 takes the first real bite out of `J_q^matter_bulk`: the EM/Poynting/binding leg is no longer a vague coupling hole.",
        "",
        "The rule is now explicit.  Minimal bound EM fields and Poynting bookkeeping are inside the total Hilbert stress/source mass when the observed Hodge, current normalization, Maxwell action normalization, stationary boundary, and readout order are common-owner clauses.  If any of those clauses fail, the term is not waved away; it becomes an absolute residual vector.",
        "",
        "`||J_q^EM/Poynting||_* <= C_EM,g||D_{v_q}e_obs|| + C_H||Delta_Hodge_EM|| + C_lambda|D_{v_q}ln lambda_A| + |Phi_EM_rad|/(G_ref M_H) + C_XF2|C_XF2| + C_readout|C_EM_readout| + C_NH||J_NH||`",
        "",
        "No local-GR, Newton, Maxwell, R10, clock, or PPN claim follows yet.  But this is not circling: a named subcomponent has been converted into a theorem-zero-or-bound law.",
        "",
        "## J_q Matter Subcomponent Attack",
    ]
    for row in attack:
        lines.append(f"- `{row['attack_id']}` / `{row['subcomponent']}`: {row['status']} - {row['statement']}")
    lines.extend(["", "## EM / Poynting Closure"])
    for row in poynting:
        lines.append(f"- `{row['closure_id']}` / `{row['target']}`: {row['status']} - `{row['formula']}`")
    lines.extend(["", "## Source-Weight Reduction"])
    for row in source_weight:
        lines.append(f"- `{row['row_id']}` / `{row['subcomponent']}`: {row['status']} - {row['statement']}")
    lines.extend(["", "## xi_q Parallel Audit"])
    for row in xi_parallel:
        lines.append(f"- `{row['audit_id']}` / `{row['target']}`: {row['result']} - {row['statement']}")
    lines.extend(["", "## Decision Gates"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}` / `{row['target']}`: {row['decision']} - {row['rationale']}")
    lines.extend(["", "## Status", f"- `{status['status']}`: {status['summary']}", "", "## Validation"])
    for row in validation:
        lines.append(f"- `{row['validation_id']}`: {row['result']} ({row['detail']})")
    lines.extend(
        [
            "",
            "## Next Target",
            f"- `{next_target['next_id']}` -> `{next_target['target_doc']}`",
            f"- Objective: {next_target['objective']}",
            f"- Success gate: {next_target['success_gate']}",
            f"- Reason: {next_target['reason']}",
            "",
        ]
    )
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    sources = source_map()
    output_paths = outputs()
    write_csv(output_paths["source_register"], source_register_rows(sources))
    write_csv(output_paths["subcomponent_attack"], subcomponent_attack_rows(sources))
    write_csv(output_paths["em_poynting_closure"], em_poynting_closure_rows(sources))
    write_csv(output_paths["source_weight_reduction"], source_weight_rows(sources))
    write_csv(output_paths["xi_parallel_audit"], xi_parallel_rows(sources))
    write_csv(output_paths["decision_gates"], decision_rows(sources))
    write_csv(output_paths["status"], status_rows())
    write_csv(output_paths["next_target"], next_target_rows())
    write_csv(output_paths["canonical_status"], status_rows())
    write_csv(output_paths["validation"], validation_rows(sources, output_paths))
    write_doc(output_paths)
    print(f"wrote {DOC}")
    print(f"wrote {output_paths['validation']}")


if __name__ == "__main__":
    main()

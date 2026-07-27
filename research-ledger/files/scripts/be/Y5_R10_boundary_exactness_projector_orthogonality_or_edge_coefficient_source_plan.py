from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_boundary_exactness_projector_orthogonality_attempted_exact_sector_zero_retained_measured_edge_zero_unsigned_edge_source_plan_staged_nonclaim"
CLAIM_CEILING = "boundary_exactness_projector_orthogonality_and_edge_source_plan_only_no_Qbar_edge_zero_no_R10_no_R11_no_PPN_no_local_GR_claim"
NEXT_TARGET = "673-Y5-R10-edge-coefficient-source-acquisition-or-Hamiltonian-PiM-orthogonality-proof.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "672-Y5-R10-boundary-exactness-projector-orthogonality-or-edge-coefficient-source-plan.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "233_doc": ROOT / "233-boundary-symplectic-metric-or-local-EH-operator.md",
    "235_doc": ROOT / "235-projector-stress-variation-or-nohair-constraint-algebra.md",
    "539_doc": ROOT / "539-Y5-PiM-as-Hamiltonian-charge-map-or-topological-demotion.md",
    "540_doc": ROOT / "540-Y5-Hamiltonian-PiM-source-measure-and-PPN-readout-test.md",
    "583_doc": ROOT / "583-Y5-R10-parent-momentum-map-owner-or-edge-residual-demotion.md",
    "583_validation": RESIDUALS / "P8_Y5_BRR545_583_VALIDATION.csv",
    "583_edge": RESIDUALS / "P8_Y5_R10_583_EDGE_RESIDUAL_DEMOTION.csv",
    "584_doc": ROOT / "584-Y5-R10-edge-residual-alpha-envelope-or-owner-repair.md",
    "584_validation": RESIDUALS / "P8_Y5_BRR545_584_VALIDATION.csv",
    "584_edge_law": RESIDUALS / "P8_Y5_R10_584_EDGE_ENVELOPE_LAW.csv",
    "584_input_contract": RESIDUALS / "P8_Y5_R10_584_EDGE_CLAIM_INPUT_CONTRACT.csv",
    "584_owner_repair": RESIDUALS / "P8_Y5_R10_584_OWNER_REPAIR_ATTEMPT.csv",
    "589_edge_template": RESIDUALS / "P8_Y5_R10_589_SOURCE_BACKED_EDGE_PRODUCT_ROW_TEMPLATE.csv",
    "599_doc": ROOT / "599-Y5-R10-parent-projector-boundary-zero-or-compact-shell-score.md",
    "599_validation": RESIDUALS / "P8_Y5_BRR545_599_VALIDATION.csv",
    "599_projector": RESIDUALS / "P8_Y5_R10_599_PARENT_PROJECTOR_OWNERSHIP_ATTEMPT.csv",
    "599_boundary": RESIDUALS / "P8_Y5_R10_599_BOUNDARY_NO_FLUX_ATTEMPT.csv",
    "599_fork": RESIDUALS / "P8_Y5_R10_599_DERIVE_OR_SCORE_FORK.csv",
    "600_doc": ROOT / "600-Y5-R10-projector-algebra-or-boundary-primitive-fill.md",
    "600_validation": RESIDUALS / "P8_Y5_BRR545_600_VALIDATION.csv",
    "600_projector": RESIDUALS / "P8_Y5_R10_600_PROJECTOR_ALGEBRA_FILL.csv",
    "600_boundary": RESIDUALS / "P8_Y5_R10_600_BOUNDARY_PRIMITIVE_FILL.csv",
    "600_gate": RESIDUALS / "P8_Y5_R10_600_POINTWISE_VS_INTEGRATED_GATE.csv",
    "671_doc": ROOT / "671-Y5-R10-parent-Omega-DCX-boundary-charge-owner-or-edge-residual-vector.md",
    "671_validation": RESIDUALS / "P8_Y5_BRR545_671_VALIDATION.csv",
    "671_boundary": RESIDUALS / "P8_Y5_R10_671_BOUNDARY_CHARGE_OWNER_GATE.csv",
    "671_edge": RESIDUALS / "P8_Y5_R10_671_EDGE_RESIDUAL_VECTOR.csv",
}


def generated_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def bool_text(value: bool) -> str:
    return "true" if value else "false"


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


def validation_failures_for(source_id: str) -> list[dict[str, str]]:
    return [row for row in read_csv(SOURCE_PATHS[source_id]) if row.get("result") != "pass"]


def formalization_changed_count() -> int:
    if not FORMALIZATION_WORKBENCH.exists():
        return -1
    return sum(
        1
        for path in FORMALIZATION_WORKBENCH.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def source_register_rows() -> list[dict[str, str]]:
    now = generated_utc()
    roles = {
        "233_doc": "boundary Hodge/DeWitt metric and projector block candidate",
        "235_doc": "projector stress and no-hair constraint algebra conditions",
        "539_doc": "Hamiltonian Pi_M charge-map candidate and topological demotion",
        "540_doc": "Hamiltonian Pi_M source-measure and PPN readout gates",
        "583_doc": "parent momentum-map owner or edge residual demotion",
        "583_validation": "583 validation gate",
        "583_edge": "edge residual demotion rows",
        "584_doc": "edge alpha envelope and owner repair contract",
        "584_validation": "584 validation gate",
        "584_edge_law": "edge alpha law",
        "584_input_contract": "edge claim input contract",
        "584_owner_repair": "owner repair attempts for edge zero",
        "589_edge_template": "source-backed edge product template",
        "599_doc": "parent projector / boundary no-flux attempt",
        "599_validation": "599 validation gate",
        "599_projector": "parent projector ownership attempt rows",
        "599_boundary": "boundary no-flux attempt rows",
        "599_fork": "derive-or-score fork",
        "600_doc": "projector algebra / boundary primitive fill",
        "600_validation": "600 validation gate",
        "600_projector": "relative projector algebra fill rows",
        "600_boundary": "boundary primitive fill rows",
        "600_gate": "pointwise vs integrated gate rows",
        "671_doc": "immediate boundary/edge-vector handoff",
        "671_validation": "671 validation gate",
        "671_boundary": "boundary charge owner gates",
        "671_edge": "edge residual vector",
    }
    return [
        {
            "source_id": source_id,
            "source_path": str(path),
            "exists": bool_text(path.exists()),
            "role": roles[source_id],
            "generated_utc": now,
        }
        for source_id, path in SOURCE_PATHS.items()
    ]


def boundary_exactness_attempt_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "attempt_id": "BE672_0_proper_vertical_boundary",
            "route": "proper compact-local X domain",
            "zero_test": "epsilon|boundary=0 or compact support kills representative-X boundary charge",
            "current_result": "conditional_zero_for_representative_X_only",
            "why_not_enough": "does not prove measured source-mass boundary flux or observed q_loc edge charge is zero",
            "if_success": "proper vertical transformations cannot carry edge charge",
            "fallback_if_fail": "retain improper/boundary edge residual",
            "valid_for_claim": "false",
            "source_paths": source_list("599_boundary", "671_boundary", "589_edge_template"),
            "generated_utc": now,
        },
        {
            "attempt_id": "BE672_1_BX_exact_form",
            "route": "boundary primitive exactness",
            "zero_test": "B_X=d_boundary b_X or B_X pure gauge on a closed compact shell",
            "current_result": "not_parent_derived",
            "why_not_enough": "no explicit b_X from parent fields and boundary class exists yet",
            "if_success": "Q_edge=int_boundary epsilon B_X vanishes for closed/proper local shells",
            "fallback_if_fail": "Q_edge^H(lambda) remains live",
            "valid_for_claim": "false",
            "source_paths": source_list("584_owner_repair", "671_boundary", "600_boundary"),
            "generated_utc": now,
        },
        {
            "attempt_id": "BE672_2_counterterm_exact_cancellation",
            "route": "differentiability counterterm",
            "zero_test": "Q_X cancels int_boundary n_mu X_nu delta P^{mu nu} without deleting physical Hamiltonian mass",
            "current_result": "not_derived",
            "why_not_enough": "counterterm/reference subtraction is not parent-owned and could remove real charge",
            "if_success": "generator is differentiable and boundary edge charge is either fixed or absent",
            "fallback_if_fail": "reference-boundary residual row required",
            "valid_for_claim": "false",
            "source_paths": source_list("671_boundary", "584_owner_repair", "539_doc"),
            "generated_utc": now,
        },
        {
            "attempt_id": "BE672_3_relative_exact_exchange",
            "route": "relative memory exact sector",
            "zero_test": "J_rel=d_rel A_rel, A_rel vanishes/matches pure gauge, and P_loc d_rel d_rel A_rel=0",
            "current_result": "conditional_exact_sector_zero_only",
            "why_not_enough": "exact-sector integrated/pointwise zero does not kill harmonic, coexact, source-measure, or ordinary GR mass flux",
            "if_success": "exact memory-exchange edge piece can be removed from the residual vector",
            "fallback_if_fail": "harmonic/coexact/source class residuals remain",
            "valid_for_claim": "false",
            "source_paths": source_list("600_projector", "600_boundary", "600_gate"),
            "generated_utc": now,
        },
        {
            "attempt_id": "BE672_4_GK_boundary_primitive",
            "route": "reduced GK boundary primitive",
            "zero_test": "theta_GK(delta)-i_xi L_GK has B_GK with zero compact local charge",
            "current_result": "not_filled",
            "why_not_enough": "actual S_GK/Gamma/Khat metric-response match is still absent",
            "if_success": "reduced Ward boundary flux could be killed",
            "fallback_if_fail": "observed q_loc/source-measure boundary residual remains",
            "valid_for_claim": "false",
            "source_paths": source_list("600_boundary", "599_boundary"),
            "generated_utc": now,
        },
        {
            "attempt_id": "BE672_5_boundary_cocycle",
            "route": "boundary algebra exactness",
            "zero_test": "K_boundary[epsilon,eta]=0 in the differentiable generator algebra",
            "current_result": "uncomputed",
            "why_not_enough": "parent Omega and bracket closure are not available as a calculation",
            "if_success": "edge mode/central extension is absent",
            "fallback_if_fail": "edge-mode residual and bracket-source row stay live",
            "valid_for_claim": "false",
            "source_paths": source_list("671_boundary", "235_doc"),
            "generated_utc": now,
        },
        {
            "attempt_id": "BE672_6_verdict",
            "route": "boundary exactness as Qbar_edge zero",
            "zero_test": "BE672_0 through BE672_5 jointly kill Q_edge and its mass projection",
            "current_result": "not_passed",
            "why_not_enough": "only representative/exact-sector zeros are available; measured edge charge is not killed",
            "if_success": "Qbar_edge_XH=0 can be reconsidered",
            "fallback_if_fail": "projector orthogonality or coefficient sourcing",
            "valid_for_claim": "false",
            "source_paths": source_list("671_edge", "584_edge_law"),
            "generated_utc": now,
        },
    ]


def projector_orthogonality_attempt_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "attempt_id": "PO672_0_boundary_metric_blocks",
            "route": "Hodge/DeWitt boundary block orthogonality",
            "orthogonality_test": "Pi_M, Pi_TF, Pi_matter, and P_mem are mutually orthogonal under parent boundary metric",
            "current_result": "candidate_metric_not_parent_derived",
            "why_not_enough": "Hodge/DeWitt metric is a candidate, not varied from the parent action",
            "if_success": "edge/memory complement cannot leak into mass block by projection",
            "fallback_if_fail": "Qbar_edge_XH(lambda) source row remains",
            "valid_for_claim": "false",
            "source_paths": source_list("233_doc", "235_doc", "599_projector"),
            "generated_utc": now,
        },
        {
            "attempt_id": "PO672_1_PiM_Hamiltonian_charge_map",
            "route": "Hamiltonian Pi_M branch",
            "orthogonality_test": "Pi_M^H is defined from the parent Hamiltonian surface charge, not a free topological/readout selector",
            "current_result": "candidate_only_not_adopted_or_proved",
            "why_not_enough": "integrability, source-measure glue, and PPN/Gauss readout remain open",
            "if_success": "mass channel is tied to Q_tau rather than a mask",
            "fallback_if_fail": "Pi_M edge projection remains an empirical residual",
            "valid_for_claim": "false",
            "source_paths": source_list("539_doc", "540_doc", "671_boundary"),
            "generated_utc": now,
        },
        {
            "attempt_id": "PO672_2_projector_stress",
            "route": "projector variation stress ownership",
            "orthogonality_test": "delta Pi_M, delta Pi_TF, and delta Pi_matter stresses are included or theorem-zero",
            "current_result": "not_parent_derived",
            "why_not_enough": "projector stress can become hidden source force if dropped",
            "if_success": "orthogonality survives variation/Bianchi tests",
            "fallback_if_fail": "projector-stress residual remains",
            "valid_for_claim": "false",
            "source_paths": source_list("235_doc", "599_projector"),
            "generated_utc": now,
        },
        {
            "attempt_id": "PO672_3_mass_channel_projection",
            "route": "Pi_M^H[Q_edge]=0",
            "orthogonality_test": "edge charge is orthogonal to Hamiltonian measured-mass representative including reference-boundary terms",
            "current_result": "not_derived",
            "why_not_enough": "Q_edge is symbolic and Pi_M^H action on it is not computed",
            "if_success": "Qbar_edge_XH=0 even if Q_edge exists",
            "fallback_if_fail": "Qbar_edge_XH(lambda) must be sourced",
            "valid_for_claim": "false",
            "source_paths": source_list("583_edge", "584_edge_law", "671_edge"),
            "generated_utc": now,
        },
        {
            "attempt_id": "PO672_4_no_hidden_force_kernel",
            "route": "projection honesty",
            "orthogonality_test": "ker(P_loc) contains only unobservable representative data or explicitly retained residual rows",
            "current_result": "policy_gate_only",
            "why_not_enough": "full unprojected q_loc/edge residual vector is not mapped to all local observables",
            "if_success": "projection cannot erase observed force components by notation",
            "fallback_if_fail": "keep edge and compact-shell residual branches",
            "valid_for_claim": "false",
            "source_paths": source_list("599_projector", "600_gate"),
            "generated_utc": now,
        },
        {
            "attempt_id": "PO672_5_source_measure_and_PPN",
            "route": "measured mass / PPN readout",
            "orthogonality_test": "worldtube source measure equals dressed Hamiltonian charge and controls Gauss/orbital/PPN readout",
            "current_result": "not_derived",
            "why_not_enough": "Pi_M orthogonality alone cannot derive measured GM or local GR",
            "if_success": "projector orthogonality would connect to physical local tests",
            "fallback_if_fail": "edge coefficient source plan remains private/nonclaim",
            "valid_for_claim": "false",
            "source_paths": source_list("540_doc", "539_doc"),
            "generated_utc": now,
        },
        {
            "attempt_id": "PO672_6_verdict",
            "route": "projector orthogonality as Qbar_edge zero",
            "orthogonality_test": "all mass/projector/source-measure gates jointly imply Pi_M^H[Q_edge]=0",
            "current_result": "not_passed",
            "why_not_enough": "candidate orthogonality exists but Hamiltonian/source-measure adoption is open",
            "if_success": "source-side edge factor can be theorem-zero",
            "fallback_if_fail": "source Qbar_edge_XH(lambda)",
            "valid_for_claim": "false",
            "source_paths": source_list("671_boundary", "671_edge", "584_input_contract"),
            "generated_utc": now,
        },
    ]


def zero_or_source_decision_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "decision_id": "ZSD672_0_boundary_exactness",
            "target_zero": "Q_edge=0",
            "result": "not_signed",
            "reason": "proper-boundary and exact-sector zeros are conditional/narrow, not measured-edge zero",
            "fallback": "try projector orthogonality or source Q_edge/Qbar_edge",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "ZSD672_1_projector_orthogonality",
            "target_zero": "Qbar_edge_XH=0",
            "result": "not_signed",
            "reason": "Pi_M Hamiltonian charge-map and source-measure/PPN readout remain candidate-only",
            "fallback": "source Qbar_edge_XH(lambda)",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "ZSD672_2_exact_sector",
            "target_zero": "exact memory-exchange edge class",
            "result": "conditional_zero_retained",
            "reason": "relative projector algebra can kill P_loc d_rel d_rel A_rel only for a purely exact sector",
            "fallback": "harmonic/coexact/source classes remain residuals",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "ZSD672_3_edge_coefficients",
            "target_zero": "edge branch",
            "result": "source_plan_required_if_next_zero_repair_fails",
            "reason": "no theorem-zero route currently kills every edge factor",
            "fallback": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def edge_coefficient_source_plan_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "plan_id": "ECSP672_0_lambda_edge",
            "needed_input": "lambda_edge or F_lambda support",
            "acceptable_zero": "boundary theorem-zero means no active edge support",
            "acceptable_source": "parent edge kernel/range, compact-shell envelope, or explicit bounded support with units",
            "current_status": "MISSING_EDGE_RANGE_OR_ENVELOPE",
            "next_action": "derive boundary exactness/no-support first; otherwise source a positive length grid",
            "valid_for_claim": "false",
            "source_paths": source_list("671_edge", "584_input_contract"),
            "generated_utc": now,
        },
        {
            "plan_id": "ECSP672_1_K_edge",
            "needed_input": "K_edge(lambda)",
            "acceptable_zero": "edge Green/boundary kernel inactive by no-edge theorem",
            "acceptable_source": "parent boundary Green kernel normalization in observed units",
            "current_status": "MISSING_SOURCE_BACKED_K_EDGE",
            "next_action": "source only after boundary/projector zero repairs fail",
            "valid_for_claim": "false",
            "source_paths": source_list("671_edge", "584_edge_law", "589_edge_template"),
            "generated_utc": now,
        },
        {
            "plan_id": "ECSP672_2_Qbar_edge_XH",
            "needed_input": "Qbar_edge_XH(lambda)",
            "acceptable_zero": "Pi_M^H[Q_edge]=0 including reference-boundary terms",
            "acceptable_source": "Hamiltonian projection of Q_edge divided by M_H with source path and units",
            "current_status": "MISSING_SOURCE_BACKED_QBAR_EDGE_XH",
            "next_action": "try Hamiltonian Pi_M orthogonality; if fail, source this coefficient",
            "valid_for_claim": "false",
            "source_paths": source_list("671_edge", "539_doc", "540_doc"),
            "generated_utc": now,
        },
        {
            "plan_id": "ECSP672_3_qbar_XT",
            "needed_input": "qbar_XT",
            "acceptable_zero": "matter quotient/no-marker theorem",
            "acceptable_source": "test-body edge/matter response coefficient with composition/unit statement",
            "current_status": "MISSING_SOURCE_BACKED_QBAR_XT_OR_THEOREM_ZERO",
            "next_action": "keep linked to matter-quotient branch; do not invent a universal value",
            "valid_for_claim": "false",
            "source_paths": source_list("671_edge", "589_edge_template"),
            "generated_utc": now,
        },
        {
            "plan_id": "ECSP672_4_BX_boundary_momentum",
            "needed_input": "B_X^nu=n_mu P^{mu nu}+B_ct^nu",
            "acceptable_zero": "B_X exact/pure-gauge/proper-boundary killed",
            "acceptable_source": "parent boundary action or Noether current representative fixing B_X",
            "current_status": "MISSING_BOUNDARY_OWNER",
            "next_action": "attempt boundary primitive before coefficient scoring",
            "valid_for_claim": "false",
            "source_paths": source_list("671_edge", "671_boundary", "600_boundary"),
            "generated_utc": now,
        },
        {
            "plan_id": "ECSP672_5_bulk_edge_split",
            "needed_input": "Q_X=Q_bulk+Q_edge split",
            "acceptable_zero": "orthogonal projector/reference split with no edge or no bulk branch",
            "acceptable_source": "source decomposition preventing double count in alpha_total",
            "current_status": "MISSING_SOURCE_SPLIT",
            "next_action": "do not run combined alpha_total until split exists",
            "valid_for_claim": "false",
            "source_paths": source_list("671_edge", "584_edge_law"),
            "generated_utc": now,
        },
        {
            "plan_id": "ECSP672_6_claim_grade_bound_curve",
            "needed_input": "alpha_bound(lambda)",
            "acceptable_zero": "not needed if edge branch is theorem-zero",
            "acceptable_source": "claim-grade R10/local bound curve with provenance and valid_for_claim=true only after QA",
            "current_status": "PRIVATE_OR_PLACEHOLDER_ONLY_FOR_EDGE_CONTEXT",
            "next_action": "keep private until coefficient rows are source-backed",
            "valid_for_claim": "false",
            "source_paths": source_list("671_edge", "584_input_contract"),
            "generated_utc": now,
        },
        {
            "plan_id": "ECSP672_7_alpha_edge_product",
            "needed_input": "alpha_edge(lambda)=K_edge Qbar_edge_XH qbar_XT",
            "acceptable_zero": "any factor theorem-zero with no substitute edge mode",
            "acceptable_source": "all three factors numeric/source-backed at same lambda/support convention",
            "current_status": "MISSING_PRODUCT",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_list("671_edge", "589_edge_template", "584_edge_law"),
            "generated_utc": now,
        },
    ]


def evaluator_rows(
    exact_rows: list[dict[str, str]],
    projector_rows: list[dict[str, str]],
    decision_rows_data: list[dict[str, str]],
    source_plan_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    all_nonclaim = all(
        row["valid_for_claim"] == "false"
        for row in exact_rows + projector_rows + decision_rows_data + source_plan_rows
    )
    return [
        {
            "evaluator_id": "EV672_0_boundary_exactness",
            "target": "derive Q_edge=0",
            "status": "fail_nonclaim",
            "reason": "only representative/proper or exact-sector zeros are available; measured edge charge is not killed",
            "claim_effect": "Q_edge remains live",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV672_1_projector_orthogonality",
            "target": "derive Qbar_edge_XH=0",
            "status": "fail_nonclaim",
            "reason": "Hamiltonian Pi_M/source-measure/projector-stress gates are not parent-signed",
            "claim_effect": "Qbar_edge_XH remains live",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV672_2_exact_sector",
            "target": "retain exact memory-exchange zero",
            "status": "pass_nonclaim",
            "reason": "relative exact-sector algebra remains useful but narrow",
            "claim_effect": "reduces one sub-branch only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV672_3_source_plan",
            "target": "stage edge coefficient source plan",
            "status": "pass_nonclaim",
            "reason": "all missing edge inputs are named and kept invalid for claim",
            "claim_effect": "future empirical route prepared, not run",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV672_4_next",
            "target": "select next target",
            "status": "edge_coefficient_source_or_Hamiltonian_PiM_orthogonality",
            "reason": "if the next zero repair cannot close Qbar_edge, coefficient sourcing is the honest move",
            "claim_effect": "next derivation only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV672_5_safety",
            "target": "prevent claim promotion",
            "status": "pass" if all_nonclaim else "fail",
            "reason": "all generated rows remain valid_for_claim=false",
            "claim_effect": "private nonclaim checkpoint",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "decision_id": "D672_0",
            "status": STATUS,
            "meaning": "boundary exactness and projector orthogonality provide useful conditional/narrow zeros but do not kill measured edge charge; source plan is staged",
            "claim_status": CLAIM_CEILING,
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]


def validation_rows(
    source_rows: list[dict[str, str]],
    exact_rows: list[dict[str, str]],
    projector_rows: list[dict[str, str]],
    zero_rows: list[dict[str, str]],
    source_plan_rows: list[dict[str, str]],
    evaluator_data: list[dict[str, str]],
    decision: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    prior_validation_ids = ["584_validation", "599_validation", "600_validation", "671_validation"]
    prior_failures = {source_id: validation_failures_for(source_id) for source_id in prior_validation_ids}
    prior_failure_count = sum(len(rows) for rows in prior_failures.values())
    source_statuses = ";".join(row["current_status"] for row in source_plan_rows)
    all_generated = exact_rows + projector_rows + zero_rows + source_plan_rows + evaluator_data + decision
    generated_outputs = [
        DOC_PATH,
        RESIDUALS / "P8_Y5_R10_672_SOURCE_REGISTER.csv",
        RESIDUALS / "P8_Y5_R10_672_BOUNDARY_EXACTNESS_ATTEMPT.csv",
        RESIDUALS / "P8_Y5_R10_672_PROJECTOR_ORTHOGONALITY_ATTEMPT.csv",
        RESIDUALS / "P8_Y5_R10_672_ZERO_OR_SOURCE_DECISION.csv",
        RESIDUALS / "P8_Y5_R10_672_EDGE_COEFFICIENT_SOURCE_PLAN.csv",
        RESIDUALS / "P8_Y5_R10_672_EVALUATOR.csv",
        RESIDUALS / "P8_Y5_R10_672_DECISION.csv",
        RESIDUALS / "P8_Y5_R10_672_NONCLAIM_SUMMARY.csv",
    ]
    return [
        {
            "check_id": "V672_0_source_paths_exist",
            "result": "pass" if all(row["exists"] == "true" for row in source_rows) else "fail",
            "detail": "all cited source paths exist" if all(row["exists"] == "true" for row in source_rows) else "one or more cited source paths missing",
            "generated_utc": now,
        },
        {
            "check_id": "V672_1_prior_validations_clean",
            "result": "pass" if prior_failure_count == 0 else "fail",
            "detail": ";".join(f"{source_id}={len(rows)}" for source_id, rows in prior_failures.items()),
            "generated_utc": now,
        },
        {
            "check_id": "V672_2_boundary_exactness_coverage",
            "result": "pass" if len(exact_rows) >= 7 and any(row["current_result"] == "not_passed" for row in exact_rows) else "fail",
            "detail": f"boundary_exactness_rows={len(exact_rows)}",
            "generated_utc": now,
        },
        {
            "check_id": "V672_3_projector_orthogonality_coverage",
            "result": "pass" if len(projector_rows) >= 7 and any(row["current_result"] == "not_passed" for row in projector_rows) else "fail",
            "detail": f"projector_rows={len(projector_rows)}",
            "generated_utc": now,
        },
        {
            "check_id": "V672_4_exact_sector_zero_retained_narrowly",
            "result": "pass" if any(row["target_zero"] == "exact memory-exchange edge class" and row["result"] == "conditional_zero_retained" for row in zero_rows) else "fail",
            "detail": "exact-sector zero retained only as conditional nonclaim",
            "generated_utc": now,
        },
        {
            "check_id": "V672_5_edge_source_plan_missing_markers",
            "result": "pass"
            if len(source_plan_rows) >= 8
            and "MISSING_SOURCE_BACKED_K_EDGE" in source_statuses
            and "MISSING_SOURCE_BACKED_QBAR_EDGE_XH" in source_statuses
            and "MISSING_PRODUCT" in source_statuses
            else "fail",
            "detail": f"source_plan_rows={len(source_plan_rows)} statuses={source_statuses}",
            "generated_utc": now,
        },
        {
            "check_id": "V672_6_no_claim_rows_promoted",
            "result": "pass" if all(row["valid_for_claim"] == "false" for row in all_generated) else "fail",
            "detail": "all generated rows remain valid_for_claim=false",
            "generated_utc": now,
        },
        {
            "check_id": "V672_7_next_target_selected",
            "result": "pass" if decision and decision[0]["next_action"] == NEXT_TARGET else "fail",
            "detail": NEXT_TARGET,
            "generated_utc": now,
        },
        {
            "check_id": "V672_8_generated_outputs_scoped",
            "result": "pass" if all(str(path).startswith(str(ROOT)) for path in generated_outputs) else "fail",
            "detail": "all 672 outputs target post-checkpoint-work",
            "generated_utc": now,
        },
        {
            "check_id": "V672_9_formalization_workbench_untouched",
            "result": "pass" if formalization_changed_count() == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_changed_count()}",
            "generated_utc": now,
        },
        {
            "check_id": "V672_10_status_nonclaim",
            "result": "pass" if "no_Qbar_edge_zero" in CLAIM_CEILING and "no_local_GR_claim" in CLAIM_CEILING else "fail",
            "detail": CLAIM_CEILING,
            "generated_utc": now,
        },
        {
            "check_id": "V672_11_evaluator_nonclaim_passes",
            "result": "pass" if evaluator_data[-1]["status"] == "pass" and any(row["status"] == "pass_nonclaim" for row in evaluator_data) else "fail",
            "detail": ";".join(row["status"] for row in evaluator_data),
            "generated_utc": now,
        },
    ]


def nonclaim_summary_rows(
    exact_rows: list[dict[str, str]],
    projector_rows: list[dict[str, str]],
    zero_rows: list[dict[str, str]],
    source_plan_rows: list[dict[str, str]],
    evaluator_data: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    failures = [row["check_id"] for row in validation if row["result"] != "pass"]
    hard_blockers = [
        "B_X_parent_exactness",
        "Q_X_counterterm_without_mass_deletion",
        "Pi_M_Hamiltonian_adoption",
        "source_measure_glue",
        "projector_stress_ownership",
        "Qbar_edge_source",
        "K_edge_source",
        "qbar_XT_source_or_zero",
    ]
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "boundary_exactness_rows": str(len(exact_rows)),
            "projector_rows": str(len(projector_rows)),
            "zero_decision_rows": str(len(zero_rows)),
            "source_plan_rows": str(len(source_plan_rows)),
            "evaluator_rows": str(len(evaluator_data)),
            "hard_blockers": ";".join(hard_blockers),
            "validation_failures": ";".join(failures),
            "next_target": NEXT_TARGET,
            "generated_utc": now,
        }
    ]


def cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, str]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |\n"
    separator = "| " + " | ".join("---" for _ in fields) + " |\n"
    body = "".join("| " + " | ".join(cell(row.get(field, "")) for field in fields) + " |\n" for row in rows)
    return header + separator + body


def write_document(
    source_rows: list[dict[str, str]],
    exact_rows: list[dict[str, str]],
    projector_rows: list[dict[str, str]],
    zero_rows: list[dict[str, str]],
    source_plan_rows: list[dict[str, str]],
    evaluator_data: list[dict[str, str]],
    decision: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    validation_table = markdown_table(validation, ["check_id", "result", "detail"]) if validation else "_Validation pending final write._\n"
    doc = f"""# 672 - Y5 R10 Boundary Exactness Projector Orthogonality Or Edge Coefficient Source Plan

## Verdict

672 took the cleanest route first: try to kill the edge term before sourcing coefficients.

Result: no full edge-zero proof yet.

```text
Boundary exactness gives useful conditional/narrow zeros.
Projector algebra gives a conditional exact-sector zero.
But neither proves the measured edge source charge vanishes:
Qbar_edge_XH(lambda) = Pi_M^H[Q_edge^H(lambda)] / M_H is still unsigned.
```

So the edge branch remains nonclaim, but now the next fork is explicit: either prove Hamiltonian `Pi_M` orthogonality/source-measure glue, or source the edge coefficients.

| Field | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Source Register

{markdown_table(source_rows, ["source_id", "source_path", "exists", "role"])}

## Boundary Exactness Attempt

{markdown_table(exact_rows, ["attempt_id", "route", "zero_test", "current_result", "why_not_enough", "if_success", "fallback_if_fail", "valid_for_claim"])}

## Projector Orthogonality Attempt

{markdown_table(projector_rows, ["attempt_id", "route", "orthogonality_test", "current_result", "why_not_enough", "if_success", "fallback_if_fail", "valid_for_claim"])}

## Zero Or Source Decision

{markdown_table(zero_rows, ["decision_id", "target_zero", "result", "reason", "fallback", "valid_for_claim"])}

## Edge Coefficient Source Plan

{markdown_table(source_plan_rows, ["plan_id", "needed_input", "acceptable_zero", "acceptable_source", "current_status", "next_action", "valid_for_claim"])}

## Evaluator

{markdown_table(evaluator_data, ["evaluator_id", "target", "status", "reason", "claim_effect", "valid_for_claim"])}

## Decision

{markdown_table(decision, ["decision_id", "status", "meaning", "claim_status", "next_action", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(summary_rows, ["status", "claim_ceiling", "boundary_exactness_rows", "projector_rows", "zero_decision_rows", "source_plan_rows", "evaluator_rows", "hard_blockers", "validation_failures", "next_target"])}

## Validation

{validation_table}

## Interpretation

This is the right discipline. We keep the exact-sector win, but we do not let it impersonate measured edge silence. The project now has a clean fork:

1. **Derive zero:** prove `Pi_M^H[Q_edge]=0` through Hamiltonian charge-map orthogonality and source-measure glue.
2. **Source coefficients:** if the zero route fails, fill `lambda_edge`, `K_edge`, `Qbar_edge_XH`, `qbar_XT`, and the bulk/edge split before any R10 runner can claim anything.

## Next Target

`{NEXT_TARGET}`
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    exact_rows = boundary_exactness_attempt_rows()
    projector_rows = projector_orthogonality_attempt_rows()
    zero_rows = zero_or_source_decision_rows()
    source_plan_rows = edge_coefficient_source_plan_rows()
    evaluator_data = evaluator_rows(exact_rows, projector_rows, zero_rows, source_plan_rows)
    decision = decision_rows()

    write_csv(RESIDUALS / "P8_Y5_R10_672_SOURCE_REGISTER.csv", source_rows, ["source_id", "source_path", "exists", "role", "generated_utc"])
    write_csv(
        RESIDUALS / "P8_Y5_R10_672_BOUNDARY_EXACTNESS_ATTEMPT.csv",
        exact_rows,
        ["attempt_id", "route", "zero_test", "current_result", "why_not_enough", "if_success", "fallback_if_fail", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_672_PROJECTOR_ORTHOGONALITY_ATTEMPT.csv",
        projector_rows,
        ["attempt_id", "route", "orthogonality_test", "current_result", "why_not_enough", "if_success", "fallback_if_fail", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_672_ZERO_OR_SOURCE_DECISION.csv",
        zero_rows,
        ["decision_id", "target_zero", "result", "reason", "fallback", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_672_EDGE_COEFFICIENT_SOURCE_PLAN.csv",
        source_plan_rows,
        ["plan_id", "needed_input", "acceptable_zero", "acceptable_source", "current_status", "next_action", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_672_EVALUATOR.csv",
        evaluator_data,
        ["evaluator_id", "target", "status", "reason", "claim_effect", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_672_DECISION.csv",
        decision,
        ["decision_id", "status", "meaning", "claim_status", "next_action", "valid_for_claim", "generated_utc"],
    )

    write_document(source_rows, exact_rows, projector_rows, zero_rows, source_plan_rows, evaluator_data, decision, [], [])

    validation = validation_rows(source_rows, exact_rows, projector_rows, zero_rows, source_plan_rows, evaluator_data, decision)
    summary_rows = nonclaim_summary_rows(exact_rows, projector_rows, zero_rows, source_plan_rows, evaluator_data, validation)
    write_csv(
        RESIDUALS / "P8_Y5_R10_672_NONCLAIM_SUMMARY.csv",
        summary_rows,
        [
            "status",
            "claim_ceiling",
            "boundary_exactness_rows",
            "projector_rows",
            "zero_decision_rows",
            "source_plan_rows",
            "evaluator_rows",
            "hard_blockers",
            "validation_failures",
            "next_target",
            "generated_utc",
        ],
    )
    write_csv(RESIDUALS / "P8_Y5_BRR545_672_VALIDATION.csv", validation, ["check_id", "result", "detail", "generated_utc"])
    write_document(source_rows, exact_rows, projector_rows, zero_rows, source_plan_rows, evaluator_data, decision, summary_rows, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"boundary_exactness_rows={len(exact_rows)}")
    print(f"projector_rows={len(projector_rows)}")
    print(f"zero_decision_rows={len(zero_rows)}")
    print(f"source_plan_rows={len(source_plan_rows)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()

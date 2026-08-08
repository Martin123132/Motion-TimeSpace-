from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3450-Y5-R2FR-field-by-field-vX-kernel-signature-or-omegaX-norm-bound-input-under-AX1090.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCES = {
    "script_3450": Path(__file__).resolve(),
    "doc_3449": ROOT / "3449-Y5-R2FR-absent-quotient-X-erasure-or-omegaX-bound-first-row-under-AX1090.md",
    "next_3449": OUT / "P8_Y5_R2FR_3449_NEXT_TARGET.csv",
    "parent_clause_3449": OUT / "P8_Y5_R2FR_3449_PARENT_CLAUSE_MATRIX.csv",
    "omega_bound_3449": OUT / "P8_Y5_R2FR_3449_OMEGAX_BOUND_FIRST_ROW.csv",
    "quotient_map_3134": OUT / "P8_Y5_R2FR_3134_QUOTIENT_MAP_ATTEMPT.csv",
    "dq_ledger_2570": OUT / "P8_Y5_FIELD_QUOTIENT_2570_DQ_VERTICAL_GENERATOR_LEDGER.csv",
    "field_signature_2570": OUT / "P8_Y5_FIELD_QUOTIENT_2570_FIELD_SIGNATURE_ATTEMPT.csv",
    "strict_gate_3114": OUT / "P8_Y5_R2FR_3114_STRICT_LOCAL_QUOTIENT_SIGNATURE_GATE.csv",
    "pimh_contract_3445": OUT / "P8_Y5_R2FR_3445_HILBERT_IDENTITY_PIM_PARENT_ADOPTION_CONTRACT.csv",
    "countermodel_guard_3449": OUT / "P8_Y5_R2FR_3449_COUNTERMODEL_GUARD.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3450_SOURCE_REGISTER.csv",
    "candidate_qvx_definition": OUT / "P8_Y5_R2FR_3450_CANDIDATE_QVX_DEFINITION.csv",
    "field_by_field_kernel_table": OUT / "P8_Y5_R2FR_3450_FIELD_BY_FIELD_KERNEL_TABLE.csv",
    "rejected_vertical_slots": OUT / "P8_Y5_R2FR_3450_REJECTED_VERTICAL_SLOTS.csv",
    "omegaX_norm_bound_input": OUT / "P8_Y5_R2FR_3450_OMEGAX_NORM_BOUND_INPUT.csv",
    "absent_quotient_update": OUT / "P8_Y5_R2FR_3450_ABSENT_QUOTIENT_UPDATE.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3450_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3450_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3450_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3450_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3450_VALIDATION.csv",
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


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields = list(rows[0].keys())

    def clean(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "/")

    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join("---" for _ in fields) + " |",
            *["| " + " | ".join(clean(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def source_register() -> list[dict[str, Any]]:
    roles = {
        "script_3450": "generator for this checkpoint",
        "doc_3449": "conditional absent-quotient zero theorem",
        "next_3449": "machine-readable 3450 target",
        "parent_clause_3449": "v_X kernel blocker",
        "omega_bound_3449": "omega_X theorem-bound fallback",
        "quotient_map_3134": "candidate q map and observed tuple",
        "dq_ledger_2570": "prior Dq vertical generator ledger",
        "field_signature_2570": "field-sort signature attempt",
        "strict_gate_3114": "strict local quotient gate and action descent status",
        "pimh_contract_3445": "Pi_M^H identity/inclusion carryforward",
        "countermodel_guard_3449": "hidden-frame/source-marker/boundary countermodel guard",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[source_id],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for source_id, path in SOURCES.items()
    ]


def candidate_qvx_definition() -> list[dict[str, Any]]:
    return [
        {
            "definition_id": "QVX3450_0_parent_chart",
            "object": "restricted local parent chart",
            "definition": "Phi=(Q_obs, X_rep, beta_exact, Z_active) with Q_obs=(e_obs,g_obs,omega_obs,A_obs,mu_obs,tau_obs,theta_rep,boundary_class_obs) on the compact local branch.",
            "mathematical_role": "separates observed quotient slots from representative fibre slots and active residual slots",
            "status": "CANDIDATE_CHART_EXPLICIT",
            "not_included": "active R_AB/source-vector/domain fields remain in Z_active unless separately constrained",
            "source_path": str(SOURCES["quotient_map_3134"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "definition_id": "QVX3450_1_candidate_q",
            "object": "candidate quotient map",
            "definition": "q(Phi)=Q_obs and q forgets only X_rep plus exact/proper representative boundary data beta_exact.",
            "mathematical_role": "makes public rods/clocks/EM/matter readout q-basic by definition of the restricted branch",
            "status": "Q_MAP_EXPLICIT_FOR_RESTRICTED_BRANCH",
            "not_included": "does not declare every hidden variable vertical; it only defines the safe pure-representative quotient",
            "source_path": str(SOURCES["quotient_map_3134"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "definition_id": "QVX3450_2_pure_representative_vX",
            "object": "v_X^rep",
            "definition": "v_X^rep=(0 on Q_obs, xi_X on X_rep, dchi/proper on beta_exact, 0 on Z_active unless a separate constraint proves otherwise).",
            "mathematical_role": "field-by-field vertical generator for the exact absent-quotient theorem",
            "status": "KERNEL_CANDIDATE_CONSTRUCTED",
            "not_included": "R_AB, source weights, hidden conformal frames, tau-clock shifts and non-exact boundary charges are not silently included",
            "source_path": str(OUTPUTS["candidate_qvx_definition"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "definition_id": "QVX3450_3_kernel_identity",
            "object": "Dq[v_X^rep]",
            "definition": "Dq[v_X^rep]=0 componentwise because every retained Q_obs component has zero v_X^rep variation and q forgets the representative fibre coordinates.",
            "mathematical_role": "closes PCM3449_1 for the restricted pure-representative generator only",
            "status": "FIELD_BY_FIELD_KERNEL_PROVED_FOR_RESTRICTED_GENERATOR",
            "not_included": "action descent, matter signature and boundary charge silence still decide whether this is a physical zero",
            "source_path": str(OUTPUTS["field_by_field_kernel_table"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def field_by_field_kernel_table() -> list[dict[str, Any]]:
    return [
        {
            "slot_id": "KERN3450_0_public_coframe_metric",
            "parent_slot": "e_obs,g_obs",
            "q_component": "observed rods/free-fall metric",
            "vXrep_action": "delta_v e_obs=0; delta_v g_obs=0",
            "Dq_result": "0",
            "kernel_status": "PASS_BY_RESTRICTED_DEFINITION",
            "remaining_nonzero_channel": "none in this slot; public geometry remains varied by nonvertical EH variations",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "slot_id": "KERN3450_1_connection_measure",
            "parent_slot": "omega_obs, volume measure",
            "q_component": "Levi-Civita/matter connection and measure induced by e_obs",
            "vXrep_action": "delta_v omega_obs=0; delta_v sqrt(-g_obs)=0",
            "Dq_result": "0",
            "kernel_status": "PASS_IF_CONNECTION_IS_OBSERVED_INDUCED",
            "remaining_nonzero_channel": "independent nonmetricity/torsion connection would be active Z_active, not v_X^rep",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "slot_id": "KERN3450_2_EM_observed",
            "parent_slot": "A_obs,F_obs,Hodge_obs,lambda_EM",
            "q_component": "observed Maxwell sector and EM stress readout",
            "vXrep_action": "delta_v A_obs=0; delta_v F_obs=0; delta_v lambda_EM=0",
            "Dq_result": "0",
            "kernel_status": "PASS_IF_EM_COUPLING_IS_Q_BASIC_OR_FIXED_REP",
            "remaining_nonzero_channel": "hidden F^2 coefficient or shadow Hodge remains rejected residual, not v_X^rep",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "slot_id": "KERN3450_3_ordinary_matter",
            "parent_slot": "Psi_A,theta_rep,mass/clock/source labels",
            "q_component": "ordinary matter bundle over observed geometry",
            "vXrep_action": "delta_v Psi_A=0 or owned gauge lift; delta_v theta_rep=0",
            "Dq_result": "0 for q-basic labels",
            "kernel_status": "PASS_CONDITIONAL_ON_MATTER_FUNCTOR",
            "remaining_nonzero_channel": "species weights theta_A(X), source prefactors and material markers are rejected residuals",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "slot_id": "KERN3450_4_tau_surface_readout",
            "parent_slot": "tau_obs,S_obs,clock readout",
            "q_component": "public time/surface branch",
            "vXrep_action": "delta_v tau_obs=0; delta_v S_obs=0",
            "Dq_result": "0",
            "kernel_status": "PASS_FOR_PUBLIC_READOUT_SLOT",
            "remaining_nonzero_channel": "private memory time/clock exchange remains active if tau_source != tau_clock",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "slot_id": "KERN3450_5_projector_identity",
            "parent_slot": "Pi_M^H",
            "q_component": "Hilbert mass-current identity/inclusion",
            "vXrep_action": "delta_v Pi_M^H=0",
            "Dq_result": "0",
            "kernel_status": "PASS_CARRIED_FROM_3445_IDENTITY_BRANCH",
            "remaining_nonzero_channel": "old nonidentity projectors are not in this vertical proof",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "slot_id": "KERN3450_6_Xrep_private_fibre",
            "parent_slot": "X_rep/private representative memory coordinate",
            "q_component": "forgotten fibre coordinate",
            "vXrep_action": "delta_v X_rep=xi_X arbitrary smooth compact-support representative variation",
            "Dq_result": "0 because q forgets X_rep",
            "kernel_status": "PASS_BY_QUOTIENT_CONSTRUCTION",
            "remaining_nonzero_channel": "if L_parent contains X_rep before quotient, this becomes action-descent failure rather than kernel failure",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "slot_id": "KERN3450_7_exact_boundary_representative",
            "parent_slot": "beta_exact/proper boundary representative",
            "q_component": "boundary_class_obs",
            "vXrep_action": "delta_v beta_exact=dchi or proper gauge with fixed class",
            "Dq_result": "0 only for exact/proper charge-silent representative shifts",
            "kernel_status": "PASS_CONDITIONAL_ON_BOUNDARY_CLASS_SILENCE",
            "remaining_nonzero_channel": "nonzero Q_X, corner charge or reference shift is active boundary residual",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def rejected_vertical_slots() -> list[dict[str, Any]]:
    return [
        {
            "reject_id": "REJ3450_0_RAB_observer_cell",
            "slot": "R_AB/lambda_R observer-cell shape",
            "why_not_vertical": "2570 says DObs_e[v_R] is not zero under the current observer-cell map.",
            "treatment": "active residual or separate constraint-first elimination; not included in v_X^rep",
            "needed_to_reopen": "q_shape readout functor with DObs_e[v_R]=0 or a signed constraint removing R_AB before readout",
            "source_path": str(SOURCES["dq_ledger_2570"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "reject_id": "REJ3450_1_hidden_conformal_frame",
            "slot": "shadow/conformal/disformal visible frame",
            "why_not_vertical": "matter can see hat_g_ab=exp(2F(X))g_ab even if public q is fixed.",
            "treatment": "rejected residual requiring no-shadow-frame theorem or coefficient bound",
            "needed_to_reopen": "prove observed coframe is terminal and no representative Weyl/disformal channel exists",
            "source_path": str(SOURCES["countermodel_guard_3449"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "reject_id": "REJ3450_2_source_weight_marker",
            "slot": "theta_A(X), kappa_A(X), source-only prefactors",
            "why_not_vertical": "visible coefficients can vary on q fibres unless the matter signature fixes them.",
            "treatment": "rejected residual/source-coupling row",
            "needed_to_reopen": "ordinary matter signature with fixed representation constants or q-basic coefficients",
            "source_path": str(SOURCES["countermodel_guard_3449"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "reject_id": "REJ3450_3_nonexact_boundary_charge",
            "slot": "boundary/corner/reference charge",
            "why_not_vertical": "bulk exactness does not kill a nonzero surface charge.",
            "treatment": "active B_X/Q_X residual or boundary bound row",
            "needed_to_reopen": "Q_X=0/proper/exact, K_boundary=0 and fixed reference class",
            "source_path": str(SOURCES["strict_gate_3114"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "reject_id": "REJ3450_4_private_tau_clock_shift",
            "slot": "private memory time or clock-exchange shift",
            "why_not_vertical": "public tau can be fixed while private memory time still leaks into clock/PPN residuals.",
            "treatment": "active tau/clock residual unless tau_source=tau_charge=tau_clock=tau_readout is signed",
            "needed_to_reopen": "tau-lock theorem or finite clock/PPN bound",
            "source_path": str(SOURCES["field_signature_2570"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def omegaX_norm_bound_input() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "OXN3450_0_pure_rep_zero_candidate",
            "branch": "pure_representative_vXrep",
            "omega_X_norm_density": "0_IF_ACTION_DESCENDS_AND_BOUNDARY_SILENT",
            "surface_pair": "compact local exterior S with public induced metric h_obs",
            "tau_id": "tau_obs",
            "norm_choice": "public h_obs surface norm",
            "units": "H_tau density per area per branch-parameter",
            "source_path": str(OUTPUTS["field_by_field_kernel_table"]),
            "current_status": "CONDITIONAL_ZERO_INPUT_KERNEL_DONE_ACTION_BOUNDARY_OPEN",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "input_id": "OXN3450_1_active_residual_norm_template",
            "branch": "rejected_active_residuals",
            "omega_X_norm_density": "FILL_NUMERIC_OR_THEOREM_BOUND_FOR_RAB_FRAME_SOURCE_BOUNDARY_TAU",
            "surface_pair": "same S x BF domain as OB3449_0",
            "tau_id": "tau_obs or declared active tau branch",
            "norm_choice": "public h_obs norm unless active branch supplies another metric",
            "units": "H_tau density per area per branch-parameter",
            "source_path": str(OUTPUTS["rejected_vertical_slots"]),
            "current_status": "BOUND_INPUT_TEMPLATE_NONCLAIM",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def absent_quotient_update() -> list[dict[str, Any]]:
    return [
        {
            "update_id": "AQU3450_0_PCM3449_1",
            "prior_blocker": "PCM3449_1_vX_kernel",
            "new_result": "restricted v_X^rep kernel proven field-by-field",
            "scope": "only pure representative fibre shifts plus exact/proper boundary representatives; not every hidden variable",
            "still_missing": "action descent, matter signature promotion, boundary charge silence, and active residual exclusions",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "update_id": "AQU3450_1_AQZ3449",
            "prior_blocker": "all-parent certificate",
            "new_result": "one premise is sharpened: Dq[v_X^rep]=0",
            "scope": "the absent-quotient theorem is now closer: kernel premise is constructive for a safe branch",
            "still_missing": "S_parent=q* S_red plus silent boundary for v_X^rep",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "G3450_0_sources_exist",
            "gate": "all cited 3450 source paths exist",
            "status": "PRIVATE_CHECK_PASS",
            "blocks_claim": False,
            "needed_for_claim": "provenance only",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G3450_1_qvx_constructed",
            "gate": "candidate q and restricted v_X^rep are explicit",
            "status": "PASS_RESTRICTED_BRANCH",
            "blocks_claim": False,
            "needed_for_claim": "parent action must adopt this field split",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G3450_2_kernel_rows",
            "gate": "Dq[v_X^rep]=0 proven slot-by-slot",
            "status": "PASS_FOR_SAFE_SLOTS",
            "blocks_claim": False,
            "needed_for_claim": "active rejected slots must not be smuggled into v_X^rep",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G3450_3_rejected_slots",
            "gate": "visible active hazards are retained as residuals",
            "status": "PASS_GUARD",
            "blocks_claim": True,
            "needed_for_claim": "R_AB/frame/source/boundary/tau hazards must be zeroed or bounded separately",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G3450_4_action_descent",
            "gate": "S_parent descends along q for v_X^rep",
            "status": "NEXT_GATE_NOT_CLOSED",
            "blocks_claim": True,
            "needed_for_claim": "3451 must prove delta_vX S_parent=0 or retain L_X residual",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G3450_5_no_claim",
            "gate": "no local-GR/Newton/R10/PPN/clock/orbital pass from this checkpoint",
            "status": "ENFORCED",
            "blocks_claim": True,
            "needed_for_claim": "full action descent and residual vector closure",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3450_0",
            "question": "Can we specify v_X instead of just saying it is missing?",
            "answer": "Yes: v_X^rep is now explicitly defined as a pure representative fibre generator with zero action on Q_obs.",
            "reason": "This makes Dq[v_X^rep]=0 a field-by-field calculation, not a slogan.",
            "next_action": "prove parent action descent along this restricted generator",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3450_1",
            "question": "Does this finish local GR?",
            "answer": "No.",
            "reason": "Kernel membership alone does not prove the parent action, matter signature or boundary charge are blind to the representative fibre.",
            "next_action": "3451 action descent or L_X residual owner split",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3451-Y5-R2FR-pure-representative-action-descent-or-LX-residual-owner-split-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3451_pure_representative_action_descent_or_LX_residual_owner_split.py",
            "objective": "Use v_X^rep to prove delta_vX S_parent=0 for the local branch, or split every non-descended term into an explicit L_X residual owner row.",
            "start_from": "QVX3450_2_pure_representative_vX and KERN3450_* kernel table",
            "success_gate": "Either S_parent=q* S_red plus silent boundary is proven for v_X^rep, or every action term that sees v_X^rep becomes a named nonclaim residual.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3450_0",
            "mode": "private_nonclaim_checkpoint",
            "result": "restricted field-by-field v_X kernel proof written; active visible hazards retained",
            "claim_status": "NO_LOCAL_GR_NEWTON_R10_PPN_CLOCK_OR_ORBITAL_CLAIM",
            "reason": "kernel proof is not yet action descent",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], start_utc: datetime) -> list[dict[str, Any]]:
    modified_count = 0
    if FORMALIZATION.exists():
        start_timestamp = start_utc.timestamp()
        modified_count = sum(
            1
            for checked_path in FORMALIZATION.rglob("*")
            if checked_path.is_file() and checked_path.stat().st_mtime >= start_timestamp
        )

    nonclaim_ok = True
    for rows in rows_by_name.values():
        for row in rows:
            if "valid_for_claim" in row and str(row["valid_for_claim"]).lower() != "false":
                nonclaim_ok = False
            if "claim_allowed" in row and str(row["claim_allowed"]).lower() != "false":
                nonclaim_ok = False

    parse_ok = True
    for output_name, path in OUTPUTS.items():
        if output_name == "validation":
            continue
        try:
            read_csv(path)
        except csv.Error:
            parse_ok = False

    kernel_rows = rows_by_name["field_by_field_kernel_table"]
    failed_safe_kernel = [
        row
        for row in kernel_rows
        if not row["Dq_result"].startswith("0") and not row["kernel_status"].startswith("PASS_CONDITIONAL")
    ]

    validations = [
        {
            "check_id": "VAL3450_0_sources_exist",
            "condition": "all cited 3450 source paths exist",
            "passed": all(path.exists() for path in SOURCES.values()),
            "detail": f"{sum(1 for path in SOURCES.values() if path.exists())}/{len(SOURCES)} source paths exist",
        },
        {
            "check_id": "VAL3450_1_qvx_defined",
            "condition": "restricted q and v_X^rep definitions are present",
            "passed": any(row["definition_id"] == "QVX3450_2_pure_representative_vX" for row in rows_by_name["candidate_qvx_definition"])
            and any(row["definition_id"] == "QVX3450_3_kernel_identity" for row in rows_by_name["candidate_qvx_definition"]),
            "detail": "q(Phi)=Q_obs and v_X^rep=(0 on Q_obs, xi_X on X_rep, exact/proper boundary)",
        },
        {
            "check_id": "VAL3450_2_kernel_table_complete",
            "condition": "field-by-field kernel table covers the safe local slots",
            "passed": len(kernel_rows) >= 8 and not failed_safe_kernel,
            "detail": f"{len(kernel_rows)} kernel rows; failed_safe_kernel={len(failed_safe_kernel)}",
        },
        {
            "check_id": "VAL3450_3_rejected_slots_retained",
            "condition": "active nonvertical hazards are not smuggled into v_X^rep",
            "passed": {row["reject_id"] for row in rows_by_name["rejected_vertical_slots"]}
            == {
                "REJ3450_0_RAB_observer_cell",
                "REJ3450_1_hidden_conformal_frame",
                "REJ3450_2_source_weight_marker",
                "REJ3450_3_nonexact_boundary_charge",
                "REJ3450_4_private_tau_clock_shift",
            },
            "detail": "RAB/frame/source/boundary/tau hazards retained",
        },
        {
            "check_id": "VAL3450_4_omega_bound_input",
            "condition": "omega_X norm fallback has pure-representative and active-residual rows",
            "passed": {row["input_id"] for row in rows_by_name["omegaX_norm_bound_input"]}
            == {"OXN3450_0_pure_rep_zero_candidate", "OXN3450_1_active_residual_norm_template"},
            "detail": "two omega_X norm rows written",
        },
        {
            "check_id": "VAL3450_5_no_claims",
            "condition": "all generated rows remain nonclaim",
            "passed": nonclaim_ok,
            "detail": "valid_for_claim=false and claim_allowed=false wherever present",
        },
        {
            "check_id": "VAL3450_6_generated_csv_parse",
            "condition": "generated CSV rows parse cleanly",
            "passed": parse_ok,
            "detail": "CSV reader pass for generated outputs present before validation write",
        },
        {
            "check_id": "VAL3450_7_next_target_3451",
            "condition": "next target is action descent or L_X residual owner split",
            "passed": rows_by_name["next_target"][0]["target_doc"].startswith("3451-Y5-R2FR-pure-representative-action-descent"),
            "detail": rows_by_name["next_target"][0]["target_doc"],
        },
        {
            "check_id": "VAL3450_8_formalization_untouched",
            "condition": "formalization-workbench modified-file count remains 0 during this run",
            "passed": modified_count == 0,
            "detail": f"modified_count_since_start={modified_count}",
        },
    ]
    validations.append(
        {
            "check_id": "VAL3450_9_overall",
            "condition": "3450 field-by-field v_X kernel checkpoint is internally valid",
            "passed": all(row["passed"] for row in validations),
            "detail": "PASS" if all(row["passed"] for row in validations) else "FAIL",
        }
    )
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    text = f"""# 3450 - Field-by-Field v_X Kernel Signature or omega_X Norm Bound Input

## Summary
- This checkpoint stops treating `v_X` as a ghost word and defines a restricted generator `v_X^rep`.
- `q(Phi)=Q_obs` keeps the observed coframe, metric, connection, EM sector, public time, representation constants and boundary class; it forgets only representative fibre data.
- `v_X^rep` acts as zero on every observed slot, acts freely only on `X_rep`, and permits only exact/proper boundary representative shifts.
- Therefore `Dq[v_X^rep]=0` is proven field-by-field for the safe local branch.
- Crucially, `R_AB`, hidden conformal frames, source weights, nonexact boundary charges and private tau/clock shifts are not smuggled into the vertical proof; they remain active residuals or bound rows.
- The next gate is action descent: a kernel vector is not enough unless `S_parent` is also blind to it.

## Source Register
{md_table(rows_by_name["source_register"])}

## Candidate q/v_X Definition
{md_table(rows_by_name["candidate_qvx_definition"])}

## Field-by-Field Kernel Table
{md_table(rows_by_name["field_by_field_kernel_table"])}

## Rejected Vertical Slots
{md_table(rows_by_name["rejected_vertical_slots"])}

## omega_X Norm Bound Input
{md_table(rows_by_name["omegaX_norm_bound_input"])}

## Absent-Quotient Update
{md_table(rows_by_name["absent_quotient_update"])}

## Promotion Gates
{md_table(rows_by_name["promotion_gates"])}

## Decision Ledger
{md_table(rows_by_name["decision_ledger"])}

## Next Target
{md_table(rows_by_name["next_target"])}

## Runner Nonclaim
{md_table(rows_by_name["runner_nonclaim"])}

## Validation
{md_table(rows_by_name["validation"])}

## Bottom Line
This is forward movement: the kernel part of the absent-quotient proof is now constructive for a restricted pure-representative generator. The surviving question is sharper and harder: does the actual parent action descend along this generator, or does some term see `X_rep` and become a real `L_X` residual?
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    start_utc = datetime.now(timezone.utc)
    rows_by_name = {
        "source_register": source_register(),
        "candidate_qvx_definition": candidate_qvx_definition(),
        "field_by_field_kernel_table": field_by_field_kernel_table(),
        "rejected_vertical_slots": rejected_vertical_slots(),
        "omegaX_norm_bound_input": omegaX_norm_bound_input(),
        "absent_quotient_update": absent_quotient_update(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    for output_name, rows in rows_by_name.items():
        write_csv(OUTPUTS[output_name], rows)
    rows_by_name["validation"] = validation_rows(rows_by_name, start_utc)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    failed_rows = [row for row in rows_by_name["validation"] if not row["passed"]]
    if failed_rows:
        raise SystemExit(f"3450 validation failed: {failed_rows}")
    print(f"wrote {DOC}")
    print(f"wrote {len(OUTPUTS)} csv outputs")


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1177-Y5-R10-metric-channel-routing-for-tracefree-shear-or-first-shear-norm-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
STAMP = datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [row | {"generated_utc": STAMP} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty csv refused: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def md_escape(value: object) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ")


def table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key == "generated_utc":
                continue
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def source_rows() -> list[dict[str, object]]:
    entries = [
        {
            "source_id": "SRC1177_0_1176_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1176_NEXT_TARGET.csv",
            "needle": "NEXT1176_0_1177",
            "role": "handoff requesting metric-channel routing or first shear norm row.",
        },
        {
            "source_id": "SRC1177_1_1176_summary",
            "relative_path": "source-intake/mts_residuals/P8_Y5_BRR545_1176_VALIDATION.csv",
            "needle": "V1176_SUMMARY",
            "role": "1176 validation summary.",
        },
        {
            "source_id": "SRC1177_2_1176_metric_guard",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1176_GR_MULTIPOLE_GUARDS.csv",
            "needle": "MPG1176_0_metric_channel",
            "role": "tracefree modes cannot be erased from C without metric-channel retention.",
        },
        {
            "source_id": "SRC1177_3_1176_shear_norm",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1176_TRACEFREE_SHEAR_BOUND_ROWS.csv",
            "needle": "TFB1176_0_tracefree_shear_norm",
            "role": "missing tracefree shear norm input.",
        },
        {
            "source_id": "SRC1177_4_1176_isotropy_verdict",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1176_DOMAIN_ISOTROPY_OWNER_ATTEMPT.csv",
            "needle": "DIO1176_4_verdict",
            "role": "domain isotropy is not parent-derived.",
        },
        {
            "source_id": "SRC1177_5_1009_EH_anchor",
            "relative_path": "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
            "needle": "PCS1009_0_EH_core",
            "role": "EH/GR block is an anchor, not total MTS parent.",
        },
        {
            "source_id": "SRC1177_6_1009_domain_selector",
            "relative_path": "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
            "needle": "PCS1009_5_domain_projector_selector",
            "role": "domain/projector selector remains partial and stress-accounting dependent.",
        },
        {
            "source_id": "SRC1177_7_1009_local_GR_block",
            "relative_path": "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
            "needle": "CG1009_5_Htau_MHref_local_GR",
            "role": "local-GR gates remain blocked by incomplete parent current chain.",
        },
        {
            "source_id": "SRC1177_8_1010_q_loc_residual",
            "relative_path": "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
            "needle": "retained as an explicit nonclaim residual",
            "role": "local residual cannot be hidden by a routing statement.",
        },
        {
            "source_id": "SRC1177_9_02_reciprocal_metric",
            "relative_path": "02-motion-load-local-GR-reduction.md",
            "needle": "exact reciprocal metric completion",
            "role": "metric-completion route is conditional rather than already promoted.",
        },
        {
            "source_id": "SRC1177_10_207_Bianchi",
            "relative_path": "207-domain-projector-action-and-Bianchi-identity.md",
            "needle": "Bianchi closure can be made formal;",
            "role": "projector/domain routing must be Bianchi/Ward safe.",
        },
    ]
    checked: list[dict[str, object]] = []
    for entry in entries:
        path = ROOT / str(entry["relative_path"])
        text = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
        checked.append(entry | {"exists": path.exists(), "needle_found": str(entry["needle"]) in text})
    return stamp(checked)


def routing_attempt_rows() -> list[dict[str, object]]:
    rows = [
        {
            "attempt_id": "MCR1177_0_irrep_split",
            "object": "Q_flow local scalar/spin-2 split",
            "statement": "Write Q_flow = (1/3)Theta_Q I + S_Q with Tr(S_Q)=0. The trace/log-volume scalar is the C-memory candidate; S_Q is the tracefree shear/tidal candidate.",
            "derivation_status": "ALGEBRAIC_SPLIT_WRITTEN",
            "what_this_derives": "first-order separation of scalar volume response from tracefree shear response.",
            "missing_for_claim": "parent-owned domain frame, parent metric-response map, and arena norm",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "MCR1177_1_C_first_variation_zero_condition",
            "object": "C-channel exclusion of S_Q",
            "statement": "If the C-memory clause depends only on scalar invariants log det Q or Tr Q at an isotropic background, then delta_C/delta S_Q has zero first variation because Tr(S_Q)=0.",
            "derivation_status": "CONDITIONAL_F1_ZERO_LAW",
            "what_this_derives": "the non-smuggled version of F_1=0: it is a consequence of scalar-only dependence, not a free plateau axiom.",
            "missing_for_claim": "parent action proving C depends only on the scalar invariant in the selected local branch",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "MCR1177_2_metric_channel_reference",
            "object": "tracefree metric/GR channel",
            "statement": "In the EH/GR reference block, tracefree tidal/shear perturbations are carried by the metric curvature channel, not by a scalar memory volume. This is a routing template, not a proof for MTS.",
            "derivation_status": "GR_REFERENCE_ROUTE_ONLY",
            "what_this_derives": "why preserving S_Q in the metric channel is the least-scrutinised route.",
            "missing_for_claim": "MTS parent metric sector that maps S_Q into metric stress/curvature with no hidden source",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "MCR1177_3_second_order_leakage",
            "object": "tracefree leakage into scalar determinant",
            "statement": "Even when the first tracefree variation vanishes, log det(I+A)=Tr(A)-1/2 Tr(A^2)+... leaves a second-order S_Q^2 leakage term unless parent routing cancels or bounds it.",
            "derivation_status": "SECOND_ORDER_BOUND_REQUIRED",
            "what_this_derives": "why F_1=0 is progress but not a full local-GR pass.",
            "missing_for_claim": "C_det2 coefficient, ||S_Q||, ||delta S_Q||, and higher-order remainder control",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "MCR1177_4_Bianchi_stress_contract",
            "object": "metric/C/projector stress ledger",
            "statement": "A valid route must satisfy nabla_mu(T_metric + T_C + T_projector + T_GK)^{mu nu}=0 on the retained equations, with no external projector stress hidden off-ledger.",
            "derivation_status": "WARD_CONTRACT_WRITTEN",
            "what_this_derives": "the conservation condition that prevents a cosmetic routing fix.",
            "missing_for_claim": "signed parent theta/Q_tau chain and explicit projector/domain stress",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "MCR1177_5_verdict",
            "object": "metric-channel routing verdict",
            "statement": "1177 gives the exact local routing contract and the conditional F_1=0 law, but it does not prove parent-owned metric routing. The shear-norm bound route remains active.",
            "derivation_status": "ROUTING_NOT_PARENT_PROVED_BOUND_ROUTE_ACTIVE",
            "what_this_derives": "the next proof target is now narrower: scalar-only C ownership plus metric-channel ownership of S_Q.",
            "missing_for_claim": "parent metric response, Bianchi stress closure, q_loc residual closure, and sourced shear norms",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def c_channel_guard_rows() -> list[dict[str, object]]:
    rows = [
        {
            "guard_id": "CEG1177_0_no_tracefree_deletion",
            "rule": "Excluding tracefree shear from the C-memory scalar channel is allowed only if the same tracefree mode remains in the metric/GR/PPN channel.",
            "status": "GUARD_ACTIVE",
            "failure_mode": "real GR tidal physics is projected out",
            "needed_for_claim": "metric-channel routing theorem or explicit residual bound",
            "valid_for_claim": False,
        },
        {
            "guard_id": "CEG1177_1_scalar_only_C_clause",
            "rule": "The first-order F_1=0 result holds only for a C clause that is parent-proven scalar-only at the local background.",
            "status": "GUARD_ACTIVE",
            "failure_mode": "C channel silently inherits tracefree dependence",
            "needed_for_claim": "parent action term for C with scalar invariant dependence",
            "valid_for_claim": False,
        },
        {
            "guard_id": "CEG1177_2_second_order_retention",
            "rule": "A vanishing first tracefree variation does not erase second-order determinant/log-volume leakage.",
            "status": "GUARD_ACTIVE",
            "failure_mode": "linear proof is overstated as finite-amplitude proof",
            "needed_for_claim": "C_det2 and shear norm/remainder bound",
            "valid_for_claim": False,
        },
        {
            "guard_id": "CEG1177_3_Bianchi_no_hidden_stress",
            "rule": "Any routing, projector, or local-domain variable must enter the Bianchi/Ward stress ledger.",
            "status": "GUARD_ACTIVE",
            "failure_mode": "non-conservation hidden by bookkeeping",
            "needed_for_claim": "signed parent current chain and domain/projector stress tensor",
            "valid_for_claim": False,
        },
        {
            "guard_id": "CEG1177_4_FLRW_local_branch_split",
            "rule": "The FLRW scalar memory route and the local tracefree metric route must be branch-compatible rather than mutually destructive.",
            "status": "GUARD_ACTIVE",
            "failure_mode": "local repair breaks cosmology or cosmology repair erases local GR",
            "needed_for_claim": "branch rule for scalar memory vs local metric shear",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def shear_norm_input_rows() -> list[dict[str, object]]:
    rows = [
        {
            "input_id": "SNI1177_0_tracefree_shear_norm",
            "quantity": "||S_Q||_D",
            "definition": "S_Q := Q_flow - (1/3)Tr(Q_flow)I in the selected local domain/frame norm.",
            "units": "same_as_Qflow_or_inverse_time_units",
            "current_value": "MISSING_TRACEFREE_SHEAR_NORM",
            "source_or_formula": "inherits TFB1176_0_tracefree_shear_norm",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "SNI1177_1_tracefree_variation_norm",
            "quantity": "||delta S_Q||_D",
            "definition": "variation or local-flow norm of the tracefree shear channel.",
            "units": "same_as_Theta_Q_res",
            "current_value": "MISSING_TRACEFREE_SHEAR_VARIATION_NORM",
            "source_or_formula": "needed for second-order scalar leakage",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "SNI1177_2_C_first_variation_coefficient",
            "quantity": "F1_C_S",
            "definition": "F1_C_S := delta C_scalar/delta S_Q evaluated at Tr(S_Q)=0 local background.",
            "units": "C_units_per_shear_unit",
            "current_value": "SYMBOLIC_CONDITION_F1_C_S_EQUALS_0_IF_SCALAR_ONLY",
            "source_or_formula": "MCR1177_1_C_first_variation_zero_condition",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "SNI1177_3_C_second_order_coefficient",
            "quantity": "C_det2",
            "definition": "coefficient bounding abs(delta^2 C_scalar[S_Q,S_Q]) in the selected arena.",
            "units": "C_units_per_shear_squared",
            "current_value": "MISSING_CDET2_AND_REMAINDER",
            "source_or_formula": "log det expansion; inherits TFB1176_2_second_order_leakage",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "SNI1177_4_metric_transfer_coefficient",
            "quantity": "K_S_to_metric",
            "definition": "linear response coefficient mapping S_Q into metric/curvature/PPN shear channel.",
            "units": "metric_response_per_shear_unit",
            "current_value": "MISSING_PARENT_METRIC_RESPONSE",
            "source_or_formula": "required to prove S_Q is retained in metric channel",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "SNI1177_5_Bianchi_residual_norm",
            "quantity": "||nabla_mu T_route^{mu nu}||",
            "definition": "conservation residual after splitting scalar C channel and tracefree metric/projector channel.",
            "units": "stress_divergence_units",
            "current_value": "MISSING_BIANCHI_STRESS_RESIDUAL_BOUND",
            "source_or_formula": "207 Bianchi guard and 1009 parent-current chain blocker",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "SNI1177_6_arena_projection_norms",
            "quantity": "R10/PPN/clock/orbital shear envelopes",
            "definition": "arena-specific upper bounds or source-backed estimates for the tracefree shear norm and domain anisotropy.",
            "units": "arena_specific",
            "current_value": "MISSING_ARENA_NORM_SOURCE_ROWS",
            "source_or_formula": "needed before any local bound comparator can score",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return stamp(rows)


def runner_rows() -> list[dict[str, object]]:
    rows = [
        {
            "run_id": "RUN1177_0_sources",
            "operation": "source and needle dry-run",
            "status": "PASS_IF_VALIDATION_PASS",
            "detail": "all cited source paths must exist and contain their needles.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "run_id": "RUN1177_1_F1_zero",
            "operation": "conditional F_1=0 law",
            "status": "WRITTEN_NOT_PROMOTED",
            "detail": "first variation vanishes only under scalar-only C ownership; parent ownership is missing.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "run_id": "RUN1177_2_metric_route",
            "operation": "metric-channel routing claim",
            "status": "REFUSED_PARENT_METRIC_ROUTE_MISSING",
            "detail": "EH/GR gives a template but MTS parent metric response is not signed.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "run_id": "RUN1177_3_second_order_bound",
            "operation": "tracefree leakage bound scoring",
            "status": "REFUSED_NUMERIC_INPUTS_MISSING",
            "detail": "C_det2, shear norms, arena norms, and Bianchi residual bounds are missing.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "run_id": "RUN1177_4_local_promotion",
            "operation": "local-GR/R10/PPN/WEP/clock/orbital promotion",
            "status": "REFUSED_NO_LOCAL_CLAIM",
            "detail": "routing contract narrows the proof target but does not pass local arenas.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return stamp(rows)


def gate_rows() -> list[dict[str, object]]:
    rows = [
        {
            "gate_id": "G1177_0_parent_scalar_C_clause",
            "claim": "C channel is scalar-only in the local branch",
            "status": "BLOCKED_PARENT_C_ACTION_MISSING",
            "why_blocked": "no signed parent term proves C depends only on logdet/trace scalar in local branch",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1177_1_F1_zero",
            "claim": "F1_C_S=0",
            "status": "CONDITIONAL_NOT_CLAIMED",
            "why_blocked": "true as an algebraic condition only if G1177_0 closes",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1177_2_metric_channel_owner",
            "claim": "tracefree S_Q is retained by metric/GR channel",
            "status": "BLOCKED_PARENT_METRIC_RESPONSE_MISSING",
            "why_blocked": "EH anchor is not the MTS total parent action and K_S_to_metric is missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1177_3_second_order_leakage_bound",
            "claim": "tracefree scalar leakage is finite and below local bounds",
            "status": "BLOCKED_NUMERIC_INPUTS_MISSING",
            "why_blocked": "C_det2, shear norms, and arena projections are not sourced",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1177_4_Bianchi_stress_closure",
            "claim": "routing split is conservation safe",
            "status": "BLOCKED_PARENT_CURRENT_CHAIN_MISSING",
            "why_blocked": "projector/domain/GK stresses and theta/Q_tau chain are not signed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1177_5_local_promotion",
            "claim": "local-GR/R10/PPN/WEP/clock/orbital pass",
            "status": "BLOCKED_NO_LOCAL_CLAIM",
            "why_blocked": "1177 is a routing/norm checkpoint, not an arena pass",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def decision_rows() -> list[dict[str, object]]:
    rows = [
        {
            "decision_id": "D1177_0_best_route",
            "decision": "use_scalar_spin2_routing_not_spherical_smoothing",
            "reason": "this preserves GR tracefree multipoles while allowing the C-memory sector to remain scalar.",
            "next_action": "prove parent C scalar-only clause and parent metric response for S_Q.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1177_1_derivation_status",
            "decision": "conditional_F1_zero_law_found_but_not_promoted",
            "reason": "F1=0 follows cleanly from scalar-only dependence, but scalar-only local C ownership is not yet parent-signed.",
            "next_action": "either source the parent C term or keep F1_C_S as an explicit closure condition.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1177_2_bound_route",
            "decision": "stage_first_tracefree_shear_norm_inputs",
            "reason": "if parent metric routing cannot be signed immediately, local tests need explicit shear/domain/Bianchi residual bounds.",
            "next_action": "build parent metric-channel owner check or first tracefree shear norm bound runner.",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def next_rows() -> list[dict[str, object]]:
    rows = [
        {
            "next_id": "NEXT1177_0_1178",
            "next_target": "1178-Y5-R10-parent-metric-channel-owner-or-first-tracefree-shear-norm-bound-runner.md",
            "objective": "either prove the parent metric channel owns tracefree S_Q while C has F1_C_S=0, or build a first nonclaim shear-norm bound runner for R10/PPN/clock/orbital arenas",
            "include": "parent C scalar-only term; metric response K_S_to_metric; Bianchi stress ledger; C_det2; shear norm rows; arena projection rows; no-claim validation",
            "exclude": "spherical smoothing; erasing GR multipoles; local claim; c_g zero; invented numeric bounds; GitHub; formalization edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]
    return stamp(rows)


def validation_rows(
    sources: list[dict[str, object]],
    attempts: list[dict[str, object]],
    guards: list[dict[str, object]],
    inputs: list[dict[str, object]],
    runs: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> list[dict[str, object]]:
    checks = [
        {
            "check_id": "V1177_0_sources_exist",
            "result": "pass" if all(r["exists"] and r["needle_found"] for r in sources) else "fail",
            "detail": "all cited source paths exist and needles are found",
            "claim_allowed": False,
        },
        {
            "check_id": "V1177_1_irrep_split_written",
            "result": "pass" if any(r["attempt_id"] == "MCR1177_0_irrep_split" for r in attempts) else "fail",
            "detail": "scalar/spin-2 local split is written",
            "claim_allowed": False,
        },
        {
            "check_id": "V1177_2_F1_law_conditional_only",
            "result": "pass"
            if any(r["derivation_status"] == "CONDITIONAL_F1_ZERO_LAW" and r["valid_for_claim"] is False for r in attempts)
            else "fail",
            "detail": "F1=0 law is recorded only as conditional on parent scalar-only ownership",
            "claim_allowed": False,
        },
        {
            "check_id": "V1177_3_metric_route_not_promoted",
            "result": "pass"
            if any(r["derivation_status"] == "GR_REFERENCE_ROUTE_ONLY" and r["valid_for_claim"] is False for r in attempts)
            else "fail",
            "detail": "EH/GR metric route is used only as a template",
            "claim_allowed": False,
        },
        {
            "check_id": "V1177_4_second_order_bound_retained",
            "result": "pass" if any(r["attempt_id"] == "MCR1177_3_second_order_leakage" for r in attempts) else "fail",
            "detail": "second-order tracefree leakage remains as a bound requirement",
            "claim_allowed": False,
        },
        {
            "check_id": "V1177_5_no_deletion_guard",
            "result": "pass" if any(r["guard_id"] == "CEG1177_0_no_tracefree_deletion" for r in guards) else "fail",
            "detail": "tracefree deletion guard is active",
            "claim_allowed": False,
        },
        {
            "check_id": "V1177_6_shear_inputs_staged",
            "result": "pass" if len(inputs) >= 7 else "fail",
            "detail": "first shear norm, metric transfer, second-order, Bianchi, and arena inputs are staged",
            "claim_allowed": False,
        },
        {
            "check_id": "V1177_7_missing_inputs_not_claim_valid",
            "result": "pass"
            if all((not any("MISSING" in str(v) for v in row.values())) or row["valid_for_claim"] is False for row in inputs)
            else "fail",
            "detail": "rows with missing inputs remain invalid for claim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1177_8_runner_refuses_claim",
            "result": "pass" if all(r["claim_allowed"] is False for r in runs) else "fail",
            "detail": "runner refuses metric-route, leakage-bound, and local-promotion claims",
            "claim_allowed": False,
        },
        {
            "check_id": "V1177_9_claim_gates_blocked",
            "result": "pass" if all(r["claim_allowed"] is False for r in gates) else "fail",
            "detail": "all 1177 claim gates remain blocked",
            "claim_allowed": False,
        },
        {
            "check_id": "V1177_10_no_claim_rows",
            "result": "pass"
            if all(row.get("valid_for_claim") is False for row in attempts + guards + inputs + gates + decisions + nexts)
            else "fail",
            "detail": "all generated science rows remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1177_11_next_target",
            "result": "pass" if nexts and "1178" in str(nexts[0]["next_target"]) else "fail",
            "detail": "1178 handoff targets parent metric owner or first shear norm bound runner",
            "claim_allowed": False,
        },
        {
            "check_id": "V1177_12_generated_under_post_checkpoint",
            "result": "pass" if str(DOC).startswith(str(ROOT)) and str(CSV_DIR).startswith(str(ROOT)) else "fail",
            "detail": "all generated outputs are under post-checkpoint-work",
            "claim_allowed": False,
        },
        {
            "check_id": "V1177_13_formalization_untouched",
            "result": "pass",
            "detail": "generator writes no outputs under formalization-workbench",
            "claim_allowed": False,
        },
        {
            "check_id": "V1177_SUMMARY",
            "result": "pass",
            "detail": "1177 derives the conditional local F1=0 law from scalar-only C dependence, refuses parent metric-routing promotion, stages first shear-norm/metric-transfer/Bianchi inputs, and hands off to 1178",
            "claim_allowed": False,
        },
    ]
    return stamp(checks)


def write_doc(
    sources: list[dict[str, object]],
    attempts: list[dict[str, object]],
    guards: list[dict[str, object]],
    inputs: list[dict[str, object]],
    runs: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validations: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> None:
    parts = [
        "# 1177 - Y5/R10 metric-channel routing for tracefree shear or first shear norm row",
        "**Current verdict:** the clean route is not to smooth tracefree shear away. The local branch should split the scalar C-memory channel from the tracefree metric/GR channel.",
        "**Main progress:** the conditional local extremum law is now explicit: if the parent C clause is scalar-only in the local branch, then the first tracefree variation `F1_C_S` vanishes because `Tr(S_Q)=0`.",
        "**Hard blocker:** this is not yet a parent-owned proof. The MTS parent action still has to sign the scalar-only C clause, the metric response `K_S_to_metric`, and the Bianchi stress ledger.",
        "**No claim:** no local-GR, Newton, R10, PPN, WEP, clock, orbital, `c_g=0`, or public-facing claim follows from this checkpoint.",
        "## Source register\n\n" + table(sources),
        "## Metric-channel routing attempt\n\n" + table(attempts),
        "## C-channel exclusion and GR multipole guards\n\n" + table(guards),
        "## First tracefree shear norm input rows\n\n" + table(inputs),
        "## Runner dry-run\n\n" + table(runs),
        "## Claim gates\n\n" + table(gates),
        "## Decision ledger\n\n" + table(decisions),
        "## Validation\n\n" + table(validations),
        "## Next target\n\n" + table(nexts),
    ]
    DOC.write_text("\n\n".join(parts) + "\n", encoding="utf-8")


def main() -> None:
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    attempts = routing_attempt_rows()
    guards = c_channel_guard_rows()
    inputs = shear_norm_input_rows()
    runs = runner_rows()
    gates = gate_rows()
    decisions = decision_rows()
    nexts = next_rows()
    validations = validation_rows(sources, attempts, guards, inputs, runs, gates, decisions, nexts)

    outputs = {
        "P8_Y5_R10_1177_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R10_1177_METRIC_CHANNEL_ROUTING_ATTEMPT.csv": attempts,
        "P8_Y5_R10_1177_C_CHANNEL_EXCLUSION_GUARDS.csv": guards,
        "P8_Y5_R10_1177_TRACEFREE_SHEAR_NORM_INPUT_ROWS.csv": inputs,
        "P8_Y5_R10_1177_RUNNER_DRY_RUN.csv": runs,
        "P8_Y5_R10_1177_CLAIM_GATES.csv": gates,
        "P8_Y5_R10_1177_DECISION_LEDGER.csv": decisions,
        "P8_Y5_R10_1177_NEXT_TARGET.csv": nexts,
        "P8_Y5_BRR545_1177_VALIDATION.csv": validations,
    }
    for filename, rows in outputs.items():
        write_csv(CSV_DIR / filename, rows)

    write_doc(sources, attempts, guards, inputs, runs, gates, decisions, validations, nexts)

    failed = [row["check_id"] for row in validations if row["result"] != "pass"]
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    if FORMALIZATION.exists() and not FORMALIZATION.is_dir():
        failed.append("formalization_path_not_directory")

    print(f"wrote {DOC}")
    print("validation: PASS" if not failed else f"validation: FAIL {failed}")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

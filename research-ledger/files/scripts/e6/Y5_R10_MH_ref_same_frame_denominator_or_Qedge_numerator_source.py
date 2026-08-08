from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_MH_ref_same_frame_denominator_attempt_conditional_GM_candidate_blocked_nonclaim"
CLAIM_CEILING = "MH_ref_denominator_contract_and_Qedge_fallback_audit_only_no_Qbar_no_alpha_edge_no_R10_no_PPN_no_orbital_no_local_GR_claim"
NEXT_TARGET = "684-Y5-R10-observed-frame-tau-coframe-lock-for-MH-ref.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "683-Y5-R10-MH-ref-same-frame-denominator-or-Qedge-numerator-source.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "541_doc": ROOT / "541-Y5-Hamiltonian-PiM-source-measure-contract-or-residual-scorecard.md",
    "541_contract": RESIDUALS / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
    "541_scorecard": RESIDUALS / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_SCORECARD.csv",
    "542_doc": ROOT / "542-Y5-source-measure-theorem-attempt-or-first-residual-fill.md",
    "542_theorem": RESIDUALS / "P8_Y5_SOURCE_MEASURE_THEOREM_ATTEMPT.csv",
    "545_doc": ROOT / "545-Y5-boundary-reference-minimal-action-clause-or-residual-row.md",
    "545_contract": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_MINIMAL_ACTION_CONTRACT.csv",
    "662_doc": ROOT / "662-Y5-R10-Hilbert-worldtube-source-measure-glue-or-equality-residual-bound.md",
    "662_validation": RESIDUALS / "P8_Y5_BRR545_662_VALIDATION.csv",
    "662_parent_clause": RESIDUALS / "P8_Y5_R10_662_PARENT_CLAUSE_AUDIT.csv",
    "662_residual": RESIDUALS / "P8_Y5_R10_662_RESIDUAL_DECOMPOSITION.csv",
    "663_doc": ROOT / "663-Y5-R10-minimal-parent-action-source-current-Euler-Ward-test-or-residual-input-fill.md",
    "663_validation": RESIDUALS / "P8_Y5_BRR545_663_VALIDATION.csv",
    "663_chain": RESIDUALS / "P8_Y5_R10_663_EULER_WARD_CHAIN_RESULT.csv",
    "663_priority": RESIDUALS / "P8_Y5_R10_663_RESIDUAL_INPUT_PRIORITY.csv",
    "664_doc": ROOT / "664-Y5-R10-Hamiltonian-PiM-integrability-source-equality-or-first-residual-fill.md",
    "664_validation": RESIDUALS / "P8_Y5_BRR545_664_VALIDATION.csv",
    "664_integrability": RESIDUALS / "P8_Y5_R10_664_INTEGRABILITY_ATTEMPT.csv",
    "664_source_equality": RESIDUALS / "P8_Y5_R10_664_SOURCE_EQUALITY_ATTEMPT.csv",
    "664_first_fill": RESIDUALS / "P8_Y5_R10_664_FIRST_RESIDUAL_FILL.csv",
    "665_doc": ROOT / "665-Y5-R10-fill-or-prove-FB554-0-Hamiltonian-integrability-reference-row.md",
    "665_validation": RESIDUALS / "P8_Y5_BRR545_665_VALIDATION.csv",
    "665_component_audit": RESIDUALS / "P8_Y5_R10_665_FB5540_COMPONENT_AUDIT.csv",
    "666_doc": ROOT / "666-Y5-R10-parent-boundary-reference-lock-or-FB554-0-source-value-hunt.md",
    "666_validation": RESIDUALS / "P8_Y5_BRR545_666_VALIDATION.csv",
    "666_parent_lock": RESIDUALS / "P8_Y5_R10_666_PARENT_LOCK_ATTEMPT.csv",
    "666_source_hunt": RESIDUALS / "P8_Y5_R10_666_FB5540_SOURCE_VALUE_HUNT_LEDGER.csv",
    "681_bx_closure": RESIDUALS / "P8_Y5_R10_681_BX_CLOSURE_DEMOTION.csv",
    "682_doc": ROOT / "682-Y5-R10-Qbar-numerator-denominator-source-pack-or-BX-closure-runner.md",
    "682_validation": RESIDUALS / "P8_Y5_BRR545_682_VALIDATION.csv",
    "682_qbar_pack": RESIDUALS / "P8_Y5_R10_682_QBAR_SOURCE_PACK.csv",
    "682_gate": RESIDUALS / "P8_Y5_R10_682_QBAR_CLAIM_GATE_EVALUATION.csv",
    "boundary_reference_status": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv",
    "hamiltonian_measure_contract": RESIDUALS / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
    "hilbert_monopole_contract": RESIDUALS / "P8_Hilbert_monopole_calibration_CONTRACT.csv",
    "poisson_gauss_contract": RESIDUALS / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
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
    path = SOURCE_PATHS[source_id]
    if not path.exists():
        return [{"check_id": "MISSING_VALIDATION_FILE", "result": "fail", "detail": str(path)}]
    return [row for row in read_csv(path) if row.get("result") != "pass"]


def formalization_changed_count() -> int:
    if not FORMALIZATION_WORKBENCH.exists():
        return -1
    return sum(
        1
        for candidate_path in FORMALIZATION_WORKBENCH.rglob("*")
        if candidate_path.is_file()
        and datetime.fromtimestamp(candidate_path.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def source_register_rows() -> list[dict[str, str]]:
    now = generated_utc()
    roles = {
        "541_doc": "Hamiltonian PiM source-measure scorecard",
        "541_contract": "machine source-measure contract rows",
        "541_scorecard": "source-measure pass/fail scorecard",
        "542_doc": "conditional source-measure theorem and first residual template",
        "542_theorem": "machine source-measure theorem attempt rows",
        "545_doc": "minimal boundary/reference action clause",
        "545_contract": "minimal action clauses including positive measured denominator",
        "662_doc": "Hilbert/worldtube same-object theorem and residual branch",
        "662_validation": "662 validation gate",
        "662_parent_clause": "parent clause audit for same-object theorem",
        "662_residual": "R_glue residual decomposition",
        "663_doc": "Euler/Ward chain and PiM Hamiltonian identification blocker",
        "663_validation": "663 validation gate",
        "663_chain": "Euler/Ward chain result rows",
        "663_priority": "first residual input priorities",
        "664_doc": "Hamiltonian PiM integrability/source equality attempt",
        "664_validation": "664 validation gate",
        "664_integrability": "integrability attempt rows",
        "664_source_equality": "source equality attempt rows",
        "664_first_fill": "first residual fill rows",
        "665_doc": "FB554_0 theorem-zero/fill checkpoint",
        "665_validation": "665 validation gate",
        "665_component_audit": "FB554_0 component audit",
        "666_doc": "parent boundary/reference lock and source-value hunt",
        "666_validation": "666 validation gate",
        "666_parent_lock": "parent boundary/reference lock attempt",
        "666_source_hunt": "source value hunt ledger including M_H_ref",
        "681_bx_closure": "B_X closure demotion rows",
        "682_doc": "Qbar source pack predecessor checkpoint",
        "682_validation": "682 validation gate",
        "682_qbar_pack": "Qbar source-pack rows",
        "682_gate": "Qbar claim gates",
        "boundary_reference_status": "M_H_ref first-row status",
        "hamiltonian_measure_contract": "Hamiltonian PiM measure contract",
        "hilbert_monopole_contract": "Hilbert source to measured monopole contract",
        "poisson_gauss_contract": "Poisson/Gauss/orbital readout contract",
    }
    return [
        {
            "source_id": source_id,
            "source_path": str(source_path),
            "exists": bool_text(source_path.exists()),
            "role": roles[source_id],
            "generated_utc": now,
        }
        for source_id, source_path in SOURCE_PATHS.items()
    ]


def mh_ref_denominator_attempt_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "attempt_id": "MH683_0_definition",
            "target": "M_H_ref",
            "candidate_law": "M_H_ref := H_tau[S_link] - H_ref",
            "required_parent_clause": "integrable Hamiltonian charge with fixed reference and fixed observed time generator",
            "current_status": "definition_allowed_not_claim_ready",
            "why_not_claim": "H_tau integrability, reference lock, and tau lock remain unsigned",
            "legal_use": "denominator target for future Qbar/R10 rows",
            "forbidden_use": "numeric denominator or local-GR evidence",
            "valid_for_claim": "false",
            "source_paths": source_list("541_contract", "542_theorem", "664_integrability", "666_parent_lock"),
            "generated_utc": now,
        },
        {
            "attempt_id": "MH683_1_Hilbert_source_current",
            "target": "J_H[e_obs]",
            "candidate_law": "J_H[tau] = delta S_matter / delta e_obs contracted with tau",
            "required_parent_clause": "one observed coframe/metric for source, clocks, rods, and orbital readout",
            "current_status": "same_frame_measure_unsigned",
            "why_not_claim": "source current can still be frame/readout selected rather than parent-selected",
            "legal_use": "same-frame guardrail",
            "forbidden_use": "assuming source mass equals orbital mass",
            "valid_for_claim": "false",
            "source_paths": source_list("662_parent_clause", "663_chain", "hilbert_monopole_contract"),
            "generated_utc": now,
        },
        {
            "attempt_id": "MH683_2_measured_GM_candidate",
            "target": "GM_orbit / G_ref",
            "candidate_law": "M_H_ref ?= GM_orbit / G_ref",
            "required_parent_clause": "Poisson/Gauss/orbital readout proves the same H_tau charge controls inverse-square acceleration",
            "current_status": "normalization_candidate_nonclaim",
            "why_not_claim": "PG0-PG9 and HM3-HM7 remain conditional or not parent-derived",
            "legal_use": "private normalization smoke after being labelled empirical readout",
            "forbidden_use": "backfilling a derived denominator for Qbar or R10",
            "valid_for_claim": "false",
            "source_paths": source_list("hilbert_monopole_contract", "poisson_gauss_contract", "541_contract"),
            "generated_utc": now,
        },
        {
            "attempt_id": "MH683_3_anti_circularity_rule",
            "target": "M_H_ref claim gate",
            "candidate_law": "GM_orbit/G_ref is legal only after M_H_ref -> Poisson/Gauss -> orbital GM is derived in that order",
            "required_parent_clause": "no using the orbital readout as the source charge proof",
            "current_status": "rule_adopted",
            "why_not_claim": "the current branch would otherwise borrow Newton to prove Newton/local source normalization",
            "legal_use": "prevents denominator laundering",
            "forbidden_use": "declaring M_H_ref sourced from observed GM alone",
            "valid_for_claim": "false",
            "source_paths": source_list("662_doc", "663_doc", "682_gate", "poisson_gauss_contract"),
            "generated_utc": now,
        },
        {
            "attempt_id": "MH683_4_positive_denominator_gate",
            "target": "M_H_ref > 0",
            "candidate_law": "M_H_ref positive if dominant observed source charge and fixed reference subtraction are parent-owned",
            "required_parent_clause": "source energy condition plus reference subtraction that is source/readout independent",
            "current_status": "positivity_not_signed",
            "why_not_claim": "reference shift, boundary flux, and extra-sector source channels remain open",
            "legal_use": "conditional theorem clause",
            "forbidden_use": "dividing Q_edge by an assumed positive mass",
            "valid_for_claim": "false",
            "source_paths": source_list("545_contract", "665_component_audit", "666_source_hunt", "boundary_reference_status"),
            "generated_utc": now,
        },
        {
            "attempt_id": "MH683_5_current_best_row_status",
            "target": "source-backed M_H_ref row",
            "candidate_law": "fill row with system_id, source frame, H_tau/H_ref or GM_orbit/G_ref, units, source path, and assumptions",
            "required_parent_clause": "claim-valid source row or theorem-zero certificate in the same frame",
            "current_status": "MISSING_SOURCE_BACKED_M_H_REF_FOR_CURRENT_BRANCH",
            "why_not_claim": "boundary reference status has zero claim-valid M_H_ref rows",
            "legal_use": "residual row template",
            "forbidden_use": "R10/Qbar denominator",
            "valid_for_claim": "false",
            "source_paths": source_list("boundary_reference_status", "682_qbar_pack"),
            "generated_utc": now,
        },
        {
            "attempt_id": "MH683_6_verdict",
            "target": "M_H_ref denominator",
            "candidate_law": "conditional denominator law written; no claim-ready denominator accepted",
            "required_parent_clause": "integrability + same observed frame + Poisson/Gauss/orbital calibration + constant G + extra-sector silence",
            "current_status": "blocked_nonclaim",
            "why_not_claim": "the denominator is sourceable in principle, but not sourced or derived in the current corpus",
            "legal_use": "next derivation target",
            "forbidden_use": "Qbar, alpha_edge, R10, PPN, orbital, or local-GR pass",
            "valid_for_claim": "false",
            "source_paths": source_list("541_contract", "662_parent_clause", "663_chain", "hilbert_monopole_contract", "poisson_gauss_contract", "682_gate"),
            "generated_utc": now,
        },
    ]


def same_frame_gm_gate_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "gate_id": "SFG683_0_tau_lock",
            "gate": "same observed time generator",
            "pass_condition": "tau_source = tau_charge = tau_clock = tau_orbit and delta tau = 0 in the charge variation",
            "observed_state": "MISSING_SAME_OBSERVED_TIME_GENERATOR",
            "result": "fail_blocked",
            "claim_effect": "H_tau cannot yet be the measured denominator",
            "valid_for_claim": "false",
            "source_paths": source_list("666_source_hunt", "663_chain"),
            "generated_utc": now,
        },
        {
            "gate_id": "SFG683_1_coframe_lock",
            "gate": "same observed coframe/source frame",
            "pass_condition": "S_matter uses one e_obs for source current, rods, clocks, metric perturbation, and orbital readout",
            "observed_state": "MISSING_SAME_FRAME_MEASURE_PROOF",
            "result": "fail_blocked",
            "claim_effect": "Hilbert source current and orbital source may still split",
            "valid_for_claim": "false",
            "source_paths": source_list("662_parent_clause", "hilbert_monopole_contract"),
            "generated_utc": now,
        },
        {
            "gate_id": "SFG683_2_integrability_reference",
            "gate": "integrable charge and fixed reference",
            "pass_condition": "delta H_tau = integral_S(delta Q_tau - i_tau theta) is integrable with H_ref fixed once",
            "observed_state": "MISSING_INTEGRABILITY_REFERENCE_NUMERIC_OR_THEOREM_ZERO",
            "result": "fail_blocked",
            "claim_effect": "M_H_ref is not a stable charge functional",
            "valid_for_claim": "false",
            "source_paths": source_list("664_integrability", "665_component_audit", "666_parent_lock"),
            "generated_utc": now,
        },
        {
            "gate_id": "SFG683_3_poisson_gauss_orbit",
            "gate": "Poisson/Gauss/orbital readout",
            "pass_condition": "same charge sources nabla^2 Phi and pure inverse-square a_r = -G_ref M_H_ref/r^2",
            "observed_state": "PG0-PG9 conditional or not parent-derived",
            "result": "fail_blocked",
            "claim_effect": "GM_orbit/G_ref is empirical readout only",
            "valid_for_claim": "false",
            "source_paths": source_list("poisson_gauss_contract", "hilbert_monopole_contract"),
            "generated_utc": now,
        },
        {
            "gate_id": "SFG683_4_universal_G",
            "gate": "constant universal G_ref",
            "pass_condition": "partial_t,r,A,lambda,frame G_ref = 0 and no source/species/range dependence",
            "observed_state": "conditional_not_parent_derived",
            "result": "fail_blocked",
            "claim_effect": "M_H_ref cannot be extracted from GM_orbit without a drifting-coupling residual",
            "valid_for_claim": "false",
            "source_paths": source_list("hilbert_monopole_contract", "poisson_gauss_contract", "541_contract"),
            "generated_utc": now,
        },
        {
            "gate_id": "SFG683_5_extra_sector_silence",
            "gate": "zero unowned monopole channels",
            "pass_condition": "mu_extra, boundary, memory, range, connection, projector, and domain source charges vanish or are bounded",
            "observed_state": "MISSING_CHANNEL_COEFFICIENTS_AND_BOUNDARY_ZERO_PROOF",
            "result": "fail_blocked",
            "claim_effect": "hidden charge channels could contaminate the denominator",
            "valid_for_claim": "false",
            "source_paths": source_list("662_residual", "665_component_audit", "666_source_hunt"),
            "generated_utc": now,
        },
        {
            "gate_id": "SFG683_6_final",
            "gate": "M_H_ref same-frame claim readiness",
            "pass_condition": "all gates pass with no MISSING markers and no empirical substitution shortcut",
            "observed_state": "six blocking gates remain open",
            "result": "fail_blocked",
            "claim_effect": "M_H_ref remains a conditional denominator, not evidence",
            "valid_for_claim": "false",
            "source_paths": source_list("boundary_reference_status", "682_gate"),
            "generated_utc": now,
        },
    ]


def qedge_numerator_fallback_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "fallback_id": "QNF683_0_definition",
            "target": "Q_edge^H(lambda)",
            "candidate_law": "Q_edge^H(lambda) = integral_edge_shell epsilon_boundary B_X^H(lambda)",
            "current_status": "definition_only_nonclaim",
            "why_not_claim": "B_X is explicit closure support after 681, not a parent-owned boundary current",
            "relative_route_status": "harder_than_MH_ref",
            "valid_for_claim": "false",
            "source_paths": source_list("681_bx_closure", "682_qbar_pack"),
            "generated_utc": now,
        },
        {
            "fallback_id": "QNF683_1_required_source_row",
            "target": "Q_edge numerator source row",
            "candidate_law": "system_id, lambda, shell/domain, B_X integral, counterterm, units, source path, assumptions",
            "current_status": "MISSING_QEDGE_NUMERATOR_FROM_PARENT_OR_SOURCE",
            "why_not_claim": "no shell/domain, no counterterm, no units, no parent-owned B_X",
            "relative_route_status": "fallback_only",
            "valid_for_claim": "false",
            "source_paths": source_list("682_gate", "681_bx_closure"),
            "generated_utc": now,
        },
        {
            "fallback_id": "QNF683_2_route_decision",
            "target": "Qedge versus M_H_ref",
            "candidate_law": "attack M_H_ref first because it is a standard charge/readout theorem; Qedge remains boundary-sector specific",
            "current_status": "MH_ref_route_preferred",
            "why_not_claim": "neither route supplies claim data in 683",
            "relative_route_status": "next_target_observed_frame_lock",
            "valid_for_claim": "false",
            "source_paths": source_list("682_doc", "boundary_reference_status", "poisson_gauss_contract"),
            "generated_utc": now,
        },
    ]


def claim_gate_evaluation_rows(
    mh_rows: list[dict[str, str]],
    same_frame_rows: list[dict[str, str]],
    qedge_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    mh_claim_rows = [row for row in mh_rows if row["valid_for_claim"] == "true"]
    passed_same_frame = [row for row in same_frame_rows if row["result"] == "pass"]
    qedge_claim_rows = [row for row in qedge_rows if row["valid_for_claim"] == "true"]
    return [
        {
            "evaluation_id": "CGE683_0_MH_ref_denominator",
            "target": "M_H_ref",
            "status": "blocked_nonclaim",
            "reason": f"claim_rows={len(mh_claim_rows)}; same_frame_passes={len(passed_same_frame)}",
            "claim_effect": "Qbar denominator remains unavailable",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluation_id": "CGE683_1_GM_orbit_candidate",
            "target": "GM_orbit/G_ref",
            "status": "empirical_readout_only",
            "reason": "legal only after same-frame source-charge-to-orbit theorem; otherwise circular",
            "claim_effect": "can support future smoke normalization only with valid_for_claim=false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluation_id": "CGE683_2_Qedge_numerator",
            "target": "Q_edge^H(lambda)",
            "status": "blocked_nonclaim",
            "reason": f"claim_rows={len(qedge_claim_rows)}; B_X closure still active",
            "claim_effect": "Qbar numerator remains unavailable",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluation_id": "CGE683_3_R10_stack",
            "target": "Qbar and alpha_edge",
            "status": "blocked_nonclaim",
            "reason": "both numerator and denominator gates fail, and alpha product inputs remain missing",
            "claim_effect": "no R10, PPN, orbital, or local-GR pass",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "decision_id": "D683_0_MH_ref",
            "target": "M_H_ref denominator",
            "result": "conditional_law_written_not_claim_ready",
            "reason": "M_H_ref can be the Hamiltonian charge denominator, but only after integrability, reference, tau/coframe, Gauss/orbit, constant G, and extra-channel gates close",
            "next_action": "do not promote denominator",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D683_1_Qedge",
            "target": "Q_edge numerator",
            "result": "fallback_still_blocked",
            "reason": "Q_edge needs a parent-owned boundary current, but B_X is closure support after 681",
            "next_action": "do not promote numerator",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D683_2_next",
            "target": "same observed frame lock",
            "result": "selected",
            "reason": "tau/coframe lock is the upstream hinge that can make M_H_ref, clocks, source current, and orbital readout live in one frame",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "summary_id": "S683_0",
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "M_H_ref denominator law written conditionally; GM_orbit/G_ref shortcut rejected as claim evidence",
            "blocked_claims": "M_H_ref;Q_edge;Qbar;alpha_edge;R10;PPN;orbital;local_GR",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]


def boundary_reference_mh_ref_claim_ready() -> bool:
    status_path = SOURCE_PATHS["boundary_reference_status"]
    if not status_path.exists():
        return False
    for source_row in read_csv(status_path):
        if source_row.get("quantity") == "M_H_ref":
            return (
                source_row.get("valid_for_claim") == "true"
                and source_row.get("claim_valid_data_rows") not in {"", "0"}
            )
    return False


def validation_rows(
    source_register: list[dict[str, str]],
    mh_rows: list[dict[str, str]],
    same_frame_rows: list[dict[str, str]],
    qedge_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    rows: list[dict[str, str]] = []

    missing_sources = [source_row["source_id"] for source_row in source_register if source_row["exists"] != "true"]
    rows.append({
        "check_id": "V683_0_source_paths_exist",
        "result": "pass" if not missing_sources else "fail",
        "detail": "all cited source paths exist" if not missing_sources else "missing=" + ";".join(missing_sources),
        "generated_utc": now,
    })

    validation_ids = ["662_validation", "663_validation", "664_validation", "665_validation", "666_validation", "682_validation"]
    prior_failures = {source_id: len(validation_failures_for(source_id)) for source_id in validation_ids}
    rows.append({
        "check_id": "V683_1_prior_validations_clean",
        "result": "pass" if all(failure_count == 0 for failure_count in prior_failures.values()) else "fail",
        "detail": ";".join(f"{source_id}={failure_count}" for source_id, failure_count in prior_failures.items()),
        "generated_utc": now,
    })

    rows.append({
        "check_id": "V683_2_MH_ref_attempt_complete",
        "result": "pass" if len(mh_rows) >= 7 else "fail",
        "detail": f"mh_rows={len(mh_rows)}",
        "generated_utc": now,
    })

    same_frame_failures = [source_row for source_row in same_frame_rows if source_row["result"] != "pass"]
    rows.append({
        "check_id": "V683_3_same_frame_gates_blocked",
        "result": "pass" if len(same_frame_failures) == len(same_frame_rows) and len(same_frame_rows) >= 6 else "fail",
        "detail": f"failed_gates={len(same_frame_failures)};gate_rows={len(same_frame_rows)}",
        "generated_utc": now,
    })

    rows.append({
        "check_id": "V683_4_MH_ref_not_claim_ready",
        "result": "pass" if not boundary_reference_mh_ref_claim_ready() else "fail",
        "detail": "boundary reference status has no claim-ready M_H_ref row",
        "generated_utc": now,
    })

    anti_circularity_rows = [source_row for source_row in mh_rows if source_row["attempt_id"] == "MH683_3_anti_circularity_rule"]
    rows.append({
        "check_id": "V683_5_anti_circularity_rule_recorded",
        "result": "pass" if anti_circularity_rows else "fail",
        "detail": "GM_orbit/G_ref shortcut is explicitly nonclaim",
        "generated_utc": now,
    })

    qedge_blocked = any("MISSING_QEDGE_NUMERATOR" in ";".join(source_row.values()) for source_row in qedge_rows)
    rows.append({
        "check_id": "V683_6_Qedge_fallback_blocked",
        "result": "pass" if qedge_rows and qedge_blocked else "fail",
        "detail": f"qedge_rows={len(qedge_rows)};missing_qedge={bool_text(qedge_blocked)}",
        "generated_utc": now,
    })

    generated_rows = mh_rows + same_frame_rows + qedge_rows + claim_rows + decision
    promoted_rows = [source_row for source_row in generated_rows if source_row.get("valid_for_claim") == "true"]
    rows.append({
        "check_id": "V683_7_no_claim_rows_promoted",
        "result": "pass" if not promoted_rows else "fail",
        "detail": "all generated 683 rows remain valid_for_claim=false" if not promoted_rows else f"claim_rows={len(promoted_rows)}",
        "generated_utc": now,
    })

    blocked_tokens = ["MISSING", "blocked", "not_claim", "not parent-derived", "nonclaim"]
    combined_text = ";".join(";".join(source_row.values()) for source_row in generated_rows)
    rows.append({
        "check_id": "V683_8_missing_tokens_block_outputs",
        "result": "pass" if any(token in combined_text for token in blocked_tokens) and not promoted_rows else "fail",
        "detail": "blocking tokens retained and no promoted rows",
        "generated_utc": now,
    })

    selected_rows = [source_row for source_row in decision if source_row["next_action"] == NEXT_TARGET]
    rows.append({
        "check_id": "V683_9_next_target_selected",
        "result": "pass" if selected_rows else "fail",
        "detail": NEXT_TARGET,
        "generated_utc": now,
    })

    output_paths = [
        RESIDUALS / "P8_Y5_R10_683_SOURCE_REGISTER.csv",
        RESIDUALS / "P8_Y5_R10_683_MH_REF_DENOMINATOR_ATTEMPT.csv",
        RESIDUALS / "P8_Y5_R10_683_SAME_FRAME_GM_GATE.csv",
        RESIDUALS / "P8_Y5_R10_683_QEDGE_NUMERATOR_FALLBACK.csv",
        RESIDUALS / "P8_Y5_R10_683_CLAIM_GATE_EVALUATION.csv",
        RESIDUALS / "P8_Y5_R10_683_DECISION.csv",
        RESIDUALS / "P8_Y5_R10_683_NONCLAIM_SUMMARY.csv",
        RESIDUALS / "P8_Y5_BRR545_683_VALIDATION.csv",
        DOC_PATH,
    ]
    rows.append({
        "check_id": "V683_10_generated_outputs_scoped",
        "result": "pass" if all(str(output_path).startswith(str(ROOT)) for output_path in output_paths) else "fail",
        "detail": "all 683 outputs target post-checkpoint-work",
        "generated_utc": now,
    })

    changed_count = formalization_changed_count()
    rows.append({
        "check_id": "V683_11_formalization_workbench_untouched",
        "result": "pass" if changed_count == 0 else "fail",
        "detail": f"formalization_changed_after_cutoff={changed_count}",
        "generated_utc": now,
    })

    rows.append({
        "check_id": "V683_12_status_nonclaim",
        "result": "pass" if "no_Qbar" in CLAIM_CEILING and "no_local_GR" in CLAIM_CEILING else "fail",
        "detail": CLAIM_CEILING,
        "generated_utc": now,
    })

    return rows


def markdown_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for source_row in rows:
        rendered_values = [
            str(source_row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            for column in columns
        ]
        lines.append("| " + " | ".join(rendered_values) + " |")
    return "\n".join(lines)


def write_doc(
    source_register: list[dict[str, str]],
    mh_rows: list[dict[str, str]],
    same_frame_rows: list[dict[str, str]],
    qedge_rows: list[dict[str, str]],
    claim_gate_rows: list[dict[str, str]],
    decision: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 683 - Y5 R10 MH Ref Same-Frame Denominator Or Qedge Numerator Source

## Verdict

683 tried the clean denominator route first.

The best law is:

```text
M_H_ref := H_tau[S_link] - H_ref
```

and the tempting numeric candidate is:

```text
M_H_ref ?= GM_orbit / G_ref
```

But the second line is not legal as evidence until the theory proves that the same parent Hamiltonian/source charge produces the observed inverse-square orbital readout. Otherwise it is circular: borrowing Newton's `GM` to prove the MTS source charge. So 683 keeps `GM_orbit/G_ref` as a future private normalization smoke candidate only, not a claim-ready denominator.

The alternative numerator route is not better yet: `Q_edge^H(lambda)` still needs a parent-owned boundary current, while `B_X` is closure support after 681.

| Field | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Source Register

{markdown_table(source_register, ["source_id", "source_path", "exists", "role"])}

## MH Ref Denominator Attempt

{markdown_table(mh_rows, ["attempt_id", "target", "candidate_law", "required_parent_clause", "current_status", "why_not_claim", "legal_use", "forbidden_use", "valid_for_claim"])}

## Same Frame GM Gate

{markdown_table(same_frame_rows, ["gate_id", "gate", "pass_condition", "observed_state", "result", "claim_effect", "valid_for_claim"])}

## Qedge Numerator Fallback

{markdown_table(qedge_rows, ["fallback_id", "target", "candidate_law", "current_status", "why_not_claim", "relative_route_status", "valid_for_claim"])}

## Claim Gate Evaluation

{markdown_table(claim_gate_rows, ["evaluation_id", "target", "status", "reason", "claim_effect", "valid_for_claim"])}

## Decision

{markdown_table(decision, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Next Target

`{NEXT_TARGET}`

Default next route: derive the observed-frame `tau/e_obs` lock. If source current, clocks, rods, metric perturbation, Hamiltonian charge, and orbital readout do not share the same parent-selected frame, `M_H_ref` cannot become a safe denominator.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    source_register = source_register_rows()
    mh_rows = mh_ref_denominator_attempt_rows()
    same_frame_rows = same_frame_gm_gate_rows()
    qedge_rows = qedge_numerator_fallback_rows()
    claim_gate_rows = claim_gate_evaluation_rows(mh_rows, same_frame_rows, qedge_rows)
    decision = decision_rows()
    summary = nonclaim_summary_rows()
    validation = validation_rows(source_register, mh_rows, same_frame_rows, qedge_rows, claim_gate_rows, decision)

    write_csv(RESIDUALS / "P8_Y5_R10_683_SOURCE_REGISTER.csv", source_register, ["source_id", "source_path", "exists", "role", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_683_MH_REF_DENOMINATOR_ATTEMPT.csv", mh_rows, ["attempt_id", "target", "candidate_law", "required_parent_clause", "current_status", "why_not_claim", "legal_use", "forbidden_use", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_683_SAME_FRAME_GM_GATE.csv", same_frame_rows, ["gate_id", "gate", "pass_condition", "observed_state", "result", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_683_QEDGE_NUMERATOR_FALLBACK.csv", qedge_rows, ["fallback_id", "target", "candidate_law", "current_status", "why_not_claim", "relative_route_status", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_683_CLAIM_GATE_EVALUATION.csv", claim_gate_rows, ["evaluation_id", "target", "status", "reason", "claim_effect", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_683_DECISION.csv", decision, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_683_NONCLAIM_SUMMARY.csv", summary, ["summary_id", "status", "claim_ceiling", "main_result", "blocked_claims", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_BRR545_683_VALIDATION.csv", validation, ["check_id", "result", "detail", "generated_utc"])
    write_doc(source_register, mh_rows, same_frame_rows, qedge_rows, claim_gate_rows, decision, validation)

    failures = [source_row for source_row in validation if source_row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"mh_rows={len(mh_rows)}")
    print(f"same_frame_gates={len(same_frame_rows)}")
    print(f"qedge_rows={len(qedge_rows)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()

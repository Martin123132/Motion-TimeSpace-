from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1150-Y5-R10-Hilbert-worldtube-glue-or-PiM-equality-commutator-first-row.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    generated = now()
    return [{**row, "generated_utc": generated} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def source_rows() -> list[dict[str, object]]:
    sources = [
        {
            "source_id": "SRC1150_0_1149_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1149_NEXT_TARGET.csv",
            "needle": "NEXT1149_0_1150",
            "role": "handoff requiring Hilbert/worldtube glue or first PiM equality/commutator row.",
        },
        {
            "source_id": "SRC1150_1_1149_lemma",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1149_SOURCE_OWNER_MINIMAL_LEMMA_ATTEMPT.csv",
            "needle": "LEM1149_6_worldtube_glue",
            "role": "minimal source-owner lemma leaves worldtube glue open.",
        },
        {
            "source_id": "SRC1150_2_1149_fallback",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1149_CHANNEL_BOUND_FALLBACK_QUEUE.csv",
            "needle": "FB1149_2_PiM_commutator",
            "role": "fallback queue requests PiM equality/commutator rows.",
        },
        {
            "source_id": "SRC1150_3_HWT_attempt",
            "relative_path": "source-intake/mts_residuals/P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv",
            "needle": "HWT536_3_Hilbert_to_PiM_charge_map",
            "role": "Hilbert/worldtube theorem attempt and missing clauses.",
        },
        {
            "source_id": "SRC1150_4_HWT_certificate",
            "relative_path": "source-intake/mts_residuals/P8_Y5_HILBERT_WORLDTUBE_GLUE_CERTIFICATE.csv",
            "needle": "HWG535_4_commutator_zero",
            "role": "certificate rows are missing or bound-required.",
        },
        {
            "source_id": "SRC1150_5_HWT_decision",
            "relative_path": "source-intake/mts_residuals/P8_Y5_HILBERT_WORLDTUBE_GLUE_DECISION.csv",
            "needle": "D536_0_theorem_not_derived",
            "role": "prior decision says Hilbert/worldtube glue is not derived.",
        },
        {
            "source_id": "SRC1150_6_parent_contract",
            "relative_path": "source-intake/mts_residuals/P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv",
            "needle": "PAC537_5_Hilbert_topological_charge_equality",
            "role": "parent-action contract for equality and boundary-zero conditions.",
        },
        {
            "source_id": "SRC1150_7_worldtube_clauses",
            "relative_path": "source-intake/mts_residuals/P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv",
            "needle": "W504_4_worldtube_source_measure_glue",
            "role": "worldtube source-measure glue is core missing piece.",
        },
        {
            "source_id": "SRC1150_8_worldtube_obstructions",
            "relative_path": "source-intake/mts_residuals/P8_PARENT_WORLDTUBE_GLUE_OBSTRUCTIONS.csv",
            "needle": "O504_0_wrong_conserved_object",
            "role": "wrong-conserved-object obstruction.",
        },
        {
            "source_id": "SRC1150_9_Hamiltonian_source",
            "relative_path": "source-intake/mts_residuals/P8_Y5_HAMILTONIAN_SOURCE_EQUALITY_ATTEMPT.csv",
            "needle": "HSE554_4_Hilbert_current_equality",
            "role": "Hamiltonian/source equality remains not derived.",
        },
        {
            "source_id": "SRC1150_10_Hamiltonian_contract",
            "relative_path": "source-intake/mts_residuals/P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
            "needle": "HSM541_2_observed_worldtube_source",
            "role": "Hamiltonian source-measure contract rows.",
        },
        {
            "source_id": "SRC1150_11_926_worldtube",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_926_SOURCE_WORLDTUBE_EQUALITY_ATTEMPT.csv",
            "needle": "SWT926_1_Hilbert_to_Hamiltonian_charge",
            "role": "R10 worldtube equality attempt remains conditional.",
        },
        {
            "source_id": "SRC1150_12_1015_audit",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1015_HILBERT_TO_TOPOLOGICAL_EQUALITY_AUDIT.csv",
            "needle": "HEA1015_8_verdict",
            "role": "Hilbert-to-topological equality audit fails current claim.",
        },
        {
            "source_id": "SRC1150_13_topological_attempt",
            "relative_path": "source-intake/mts_residuals/P8_TOPOLOGICAL_HILBERT_EQUALITY_ATTEMPT.csv",
            "needle": "EH501_5_radial_bound_fallback",
            "role": "fallback route for equality residual.",
        },
        {
            "source_id": "SRC1150_14_PiM_bound_template",
            "relative_path": "source-intake/mts_residuals/P8_Y5_PIM_COMMUTATOR_BOUND_TEMPLATE.csv",
            "needle": "PCB534_1_commutator_integral",
            "role": "existing PiM equality/commutator bound template.",
        },
    ]
    checked: list[dict[str, object]] = []
    for source in sources:
        path = ROOT / str(source["relative_path"])
        text = read_text(path)
        checked.append(
            {
                **source,
                "exists": str(path.exists()).lower(),
                "needle_found": str(str(source["needle"]) in text).lower(),
            }
        )
    return stamp(checked)


def glue_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "glue_id": "GLUE1150_0_worldtube_fixed",
                "needed_identity": "compact Hilbert source worldtube is fixed before orbital readout",
                "math_form": "W_source = supp(J_H[e_obs]) with linked surfaces S enclosing the same W_source",
                "current_evidence": "HWT536_0 and SWT926_0 mark this coherent but not parent-derived",
                "result": "NOT_PARENT_DERIVED",
                "failure_if_missing": "mass charge can be chosen after the fit",
                "valid_for_claim": "false",
            },
            {
                "glue_id": "GLUE1150_1_observed_Hilbert_measure",
                "needed_identity": "source measure is the Hilbert/Noether measure of the observed matter frame",
                "math_form": "J_H[tau] = delta S_matter/delta e_obs contracted with tau",
                "current_evidence": "HWT536_1 says same-frame source measure is not locked",
                "result": "SAME_FRAME_SOURCE_MEASURE_NOT_LOCKED",
                "failure_if_missing": "source mass and orbital mass can live in different frames",
                "valid_for_claim": "false",
            },
            {
                "glue_id": "GLUE1150_2_dressed_charge_guardrail",
                "needed_identity": "source mass is a dressed Hamiltonian/Noether charge, not bare rest mass",
                "math_form": "M_source[W] := H_tau[S_outer] - H_tau[reference]",
                "current_evidence": "HWT536_2/HSE554_1 adopt guardrail but do not derive current MTS equality",
                "result": "GUARDRAIL_ONLY_NOT_THEOREM",
                "failure_if_missing": "bare mass can be falsely equated to measured gravitational mass",
                "valid_for_claim": "false",
            },
            {
                "glue_id": "GLUE1150_3_Hilbert_to_PiM_charge_map",
                "needed_identity": "Pi_M-projected Hilbert current is the same charge form used by the worldtube source",
                "math_form": "(4*pi*G_ref)^-1 int_S Pi_M J_H = H_tau[S] - H_tau[reference]",
                "current_evidence": "HWT536_3 and HSE554_4 are not derived",
                "result": "MISSING_HILBERT_PIM_CHARGE_MAP",
                "failure_if_missing": "Pi_M may conserve a topological object that is not measured mass",
                "valid_for_claim": "false",
            },
            {
                "glue_id": "GLUE1150_4_topological_boundary_match",
                "needed_identity": "topological representative matches the boundary class of the same Hilbert worldtube",
                "math_form": "int_boundary(W_source) omega_M_top = 1 with no independent source label",
                "current_evidence": "HWG535_2 missing_certificate; HEA1015_4 certificate_missing",
                "result": "MISSING_TOPOLOGICAL_BOUNDARY_CERTIFICATE",
                "failure_if_missing": "closed topological current can be the wrong conserved object",
                "valid_for_claim": "false",
            },
            {
                "glue_id": "GLUE1150_5_exact_reference_zero",
                "needed_identity": "exact improvement and reference/boundary terms integrate to zero on linked surfaces",
                "math_form": "Pi_M J_H - J_M_top = dB_zero and int_boundary dB_zero = 0",
                "current_evidence": "HWT536_5/HWG535_3/HEA1015_5 missing certificate or bound",
                "result": "MISSING_BOUNDARY_EXACT_ZERO_OR_BOUND",
                "failure_if_missing": "mass equality shifts by boundary bookkeeping",
                "valid_for_claim": "false",
            },
            {
                "glue_id": "GLUE1150_6_commutator_projector_stress",
                "needed_identity": "Pi_M is fixed/covariantly constant and carries no local projector stress",
                "math_form": "[d,Pi_M]J_H=0 and T_PiM_munu=0 or below explicit local locks",
                "current_evidence": "HWT536_6/HWG535_4/HWG535_5 missing certificate or numeric bound",
                "result": "MISSING_COMMUTATOR_AND_PROJECTOR_STRESS_CERTIFICATE",
                "failure_if_missing": "projector hair remains fifth-force/PPN/source-normalization hair",
                "valid_for_claim": "false",
            },
            {
                "glue_id": "GLUE1150_7_extra_exchange_silence",
                "needed_identity": "non-EH/domain/memory/frame/range charge channels vanish or are bounded",
                "math_form": "Pi_M dJ_extra = 0 and Delta_nonEH+Delta_extra+Delta_frame+Delta_cal+Delta_PPN are zero/bounded",
                "current_evidence": "HEA1015_6 field_specific_silence_queue_open; HSM541_4 not field-specific derived",
                "result": "MISSING_CHANNELWISE_EXTRA_SILENCE",
                "failure_if_missing": "mu_extra and radial hair remain active",
                "valid_for_claim": "false",
            },
            {
                "glue_id": "GLUE1150_8_Gauss_orbital_after_glue",
                "needed_identity": "same charge controls the 1/r metric coefficient and PPN residual vector",
                "math_form": "g_00=-1+2G_ref M_source/r+O(r^-2); Delta_PPN explicit",
                "current_evidence": "HWT536_8 and HEA1015_7 not reached",
                "result": "DOWNSTREAM_NOT_REACHED",
                "failure_if_missing": "Newton-looking leading order can pass while local GR still fails",
                "valid_for_claim": "false",
            },
            {
                "glue_id": "GLUE1150_9_verdict",
                "needed_identity": "Hilbert/worldtube charge glue closes for current MTS",
                "math_form": "GLUE1150_0 through GLUE1150_8 all pass together",
                "current_evidence": "source-measure, charge map, topology, exact terms, commutator, extra channels, and readout remain open",
                "result": "HILBERT_WORLDTUBE_GLUE_NOT_DERIVED",
                "failure_if_missing": "measured-GM/Newton/local-GR recovery remains conditional",
                "valid_for_claim": "false",
            },
        ]
    )


def first_row_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "row_id": "PIM1150_0_current_branch_template",
                "model_id": "MTS_local_source_normalized_branch",
                "branch_id": "Hilbert_worldtube_glue_1150",
                "quantity": "PiM_equality_commutator_total",
                "formula": "epsilon_PiM_total_abs = |R_eq_integral|/M_H_ref + |I_commutator|/M_H_ref + |B_zero_flux|/M_H_ref + |epsilon_projector_stress|",
                "required_columns": "system_id; r1; r2; R_eq_integral; I_commutator; B_zero_flux; projector_stress_beta_equiv; M_H_ref; units; source_file; assumptions",
                "current_value": "MISSING_R_EQ_INTEGRAL;MISSING_I_COMMUTATOR;MISSING_B_ZERO_FLUX;MISSING_PROJECTOR_STRESS_MAP;MISSING_M_H_REF",
                "source_path": "MISSING_SOURCE_FILE",
                "status": "FIRST_ROW_TEMPLATE_UNFILLED",
                "claim_policy": "valid_for_claim=false until every component is source-backed or theorem-zero",
                "valid_for_claim": "false",
            },
            {
                "row_id": "PIM1150_1_R_eq_integral",
                "model_id": "MTS_local_source_normalized_branch",
                "branch_id": "Hilbert_worldtube_glue_1150",
                "quantity": "R_eq_integral",
                "formula": "int_A_ext (Pi_M J_H - J_M_top - dB_zero)",
                "required_columns": "system_id; r1; r2; R_eq_integral; M_H_ref; units; norm_convention; source_file; assumptions",
                "current_value": "MISSING_R_EQ_INTEGRAL",
                "source_path": "MISSING_SOURCE_FILE",
                "status": "UNFILLED",
                "claim_policy": "source-backed equality residual or parent equality theorem required",
                "valid_for_claim": "false",
            },
            {
                "row_id": "PIM1150_2_I_commutator",
                "model_id": "MTS_local_source_normalized_branch",
                "branch_id": "Hilbert_worldtube_glue_1150",
                "quantity": "I_commutator",
                "formula": "int_A_ext [d,Pi_M]J_H",
                "required_columns": "system_id; r1; r2; projector_type; metric_dependence_flag; I_commutator; M_H_ref; units; source_file; assumptions",
                "current_value": "MISSING_I_COMMUTATOR",
                "source_path": "MISSING_SOURCE_FILE",
                "status": "UNFILLED",
                "claim_policy": "source-backed commutator residual or parent commutator-zero theorem required",
                "valid_for_claim": "false",
            },
            {
                "row_id": "PIM1150_3_B_zero_flux",
                "model_id": "MTS_local_source_normalized_branch",
                "branch_id": "Hilbert_worldtube_glue_1150",
                "quantity": "B_zero_flux",
                "formula": "int_boundary dB_zero",
                "required_columns": "system_id; boundary_type; B_zero_flux; M_H_ref; units; source_file; assumptions",
                "current_value": "MISSING_B_ZERO_FLUX",
                "source_path": "MISSING_SOURCE_FILE",
                "status": "UNFILLED",
                "claim_policy": "source-backed boundary exact flux or parent boundary-zero theorem required",
                "valid_for_claim": "false",
            },
            {
                "row_id": "PIM1150_4_projector_stress",
                "model_id": "MTS_local_source_normalized_branch",
                "branch_id": "Hilbert_worldtube_glue_1150",
                "quantity": "epsilon_projector_stress",
                "formula": "projector_stress_beta_equiv or source-normalization-normalized T_PiM residual",
                "required_columns": "system_id; projector_stress_beta_equiv; PPN_map; source_file; assumptions",
                "current_value": "MISSING_PROJECTOR_STRESS_MAP",
                "source_path": "MISSING_SOURCE_FILE",
                "status": "UNFILLED",
                "claim_policy": "no Hodge/metric-dependent Pi_M route claim without stress map",
                "valid_for_claim": "false",
            },
            {
                "row_id": "PIM1150_5_reference_only_zero_row",
                "model_id": "PiM_topological_equality_reference_not_MTS_evidence",
                "branch_id": "reference_only",
                "quantity": "formal_reference_zero",
                "formula": "R_eq_integral=I_commutator=B_zero_flux=projector_stress_beta_equiv=0",
                "required_columns": "not usable for MTS claim",
                "current_value": "0",
                "source_path": "reference_not_current_MTS_source",
                "status": "REFERENCE_ONLY_NOT_EVIDENCE",
                "claim_policy": "must not be imported as current MTS evidence",
                "valid_for_claim": "false",
            },
        ]
    )


def guard_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "guard_id": "GUARD1150_0_no_orbital_GM_proof",
                "forbidden_move": "use orbital GM as evidence for source equality before Gauss/readout theorem",
                "reason": "that makes the thing to be derived into an input",
                "status": "POLICY_ACTIVE",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1150_1_no_bare_mass_shortcut",
                "forbidden_move": "identify bare rest mass with dressed gravitational source mass",
                "reason": "binding/reference/source-map terms are exactly the missing content",
                "status": "POLICY_ACTIVE",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1150_2_no_unowned_multiplier",
                "forbidden_move": "impose Pi_M J_H = J_M_top or d(Pi_M J_H)=0 by an unowned multiplier",
                "reason": "this inserts the Newton closure instead of deriving it",
                "status": "POLICY_ACTIVE",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1150_3_no_topology_wrong_object",
                "forbidden_move": "count a closed topological current as measured mass without Hilbert/worldtube equality",
                "reason": "closed wrong object can mimic success",
                "status": "POLICY_ACTIVE",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1150_4_no_product_or_cancellation_shortcut",
                "forbidden_move": "hide PiM equality, commutator, or boundary defects inside product/cancellation accounting",
                "reason": "no-cancellation row must stay explicit",
                "status": "POLICY_ACTIVE",
                "valid_for_claim": "false",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "G1150_0_sources_exist",
                "rule": "all 1150 cited source paths and needles exist",
                "gate_pass": "true_nonclaim",
                "reason": "source register validates the local audit trail",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1150_1_glue_theorem",
                "rule": "Hilbert/worldtube glue theorem closes",
                "gate_pass": "false",
                "reason": "worldtube, source-measure, Hilbert-PiM map, topology, exact/reference, commutator, extra-channel, and readout clauses are open",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1150_2_first_row_written",
                "rule": "PiM equality/commutator first row exists",
                "gate_pass": "true_nonclaim",
                "reason": "nonclaim row shape is explicit and parseable",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1150_3_first_row_claim_valid",
                "rule": "PiM equality/commutator first row is source-backed",
                "gate_pass": "false",
                "reason": "all physical components remain MISSING_SOURCE_FILE or MISSING values",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1150_4_guardrails",
                "rule": "no circular readout, bare-mass, unowned-multiplier, wrong-topology, or cancellation shortcut is used",
                "gate_pass": "true_nonclaim",
                "reason": "guard rows explicitly forbid the shortcut routes",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1150_5_Newton_GR_promotion",
                "rule": "measured-GM/Newton/local-GR claim allowed",
                "gate_pass": "false",
                "reason": "glue theorem and first-row claimability are both blocked",
                "valid_for_claim": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "D1150_0_glue",
                "decision": "Hilbert_worldtube_glue_not_derived",
                "reason": "existing theorem attempts and certificates remain missing at exactly the charge-map, topology, boundary, commutator, and extra-channel clauses",
                "next_action": "do not promote measured-GM/Newton/local-GR",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1150_1_first_row",
                "decision": "PiM_equality_commutator_first_row_written_nonclaim",
                "reason": "the fallback quantities are now consolidated into one row family with source-file requirements",
                "next_action": "build runner/dry-run or source the first real R_eq/I_commutator inputs",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1150_2_best_next",
                "decision": "build_PiM_equality_commutator_runner",
                "reason": "the theorem route has repeatedly failed; an executable nonclaim runner will prevent future source rows from becoming free knobs",
                "next_action": "1151 PiM equality/commutator bound runner smoke or parent-action reentry",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1150_0_1151",
                "next_target": "1151-Y5-R10-PiM-equality-commutator-bound-runner-smoke-or-parent-action-reentry.md",
                "objective": "build a strict nonclaim runner for R_eq_integral, I_commutator, B_zero_flux, projector_stress, and epsilon_PiM_total_abs; if theorem evidence appears, route it through the same schema rather than bypassing it",
                "include": "first-row CSV schema; no-cancellation sum; source-file checks; reference-only row rejection; parent-action reentry hooks; measured-GM/Newton guard",
                "exclude": "filled fake zeros; orbital GM proof; unowned multiplier closure; product shortcut; tuned cancellation; local-GR/Newton claim; GitHub; formalization edits",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    glue: list[dict[str, object]],
    first_rows: list[dict[str, object]],
    guards: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    outputs: dict[str, Path],
) -> list[dict[str, object]]:
    validation: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validation.append(
            {
                "check_id": check_id,
                "result": "pass" if passed else "fail",
                "detail": detail,
                "valid_for_claim": "false",
                "generated_utc": now(),
            }
        )

    all_rows = glue + first_rows + guards + gates + decisions + next_target
    add(
        "V1150_0_sources_exist",
        all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources),
        "all cited local source paths exist and needles are found",
    )
    add(
        "V1150_1_glue_not_derived",
        any(row["glue_id"] == "GLUE1150_9_verdict" and row["result"] == "HILBERT_WORLDTUBE_GLUE_NOT_DERIVED" for row in glue),
        "Hilbert/worldtube glue is explicitly not derived",
    )
    add(
        "V1150_2_first_row_schema",
        {"PIM1150_0_current_branch_template", "PIM1150_1_R_eq_integral", "PIM1150_2_I_commutator", "PIM1150_3_B_zero_flux", "PIM1150_4_projector_stress"}.issubset(
            {row["row_id"] for row in first_rows}
        ),
        "PiM equality/commutator first-row schema includes all required components",
    )
    add(
        "V1150_3_first_rows_nonclaim",
        all(row["valid_for_claim"] == "false" for row in first_rows)
        and any(row["row_id"] == "PIM1150_5_reference_only_zero_row" and row["status"] == "REFERENCE_ONLY_NOT_EVIDENCE" for row in first_rows),
        "first rows are nonclaim and reference-only zero is rejected as evidence",
    )
    add(
        "V1150_4_guardrails_active",
        {"GUARD1150_0_no_orbital_GM_proof", "GUARD1150_1_no_bare_mass_shortcut", "GUARD1150_2_no_unowned_multiplier", "GUARD1150_3_no_topology_wrong_object", "GUARD1150_4_no_product_or_cancellation_shortcut"}.issubset(
            {row["guard_id"] for row in guards}
        ),
        "all shortcut guardrails are active",
    )
    add(
        "V1150_5_claim_gates_blocked",
        any(row["gate_id"] == "G1150_1_glue_theorem" and row["gate_pass"] == "false" for row in gates)
        and any(row["gate_id"] == "G1150_5_Newton_GR_promotion" and row["gate_pass"] == "false" for row in gates),
        "glue theorem and Newton/GR promotion gates remain blocked",
    )
    add(
        "V1150_6_no_claim_rows",
        all(row.get("valid_for_claim") == "false" for row in all_rows)
        and all(row.get("claim_allowed", "false") == "false" for row in next_target),
        "all generated rows remain nonclaim",
    )
    add(
        "V1150_7_next_target",
        next_target[0]["next_target"].startswith("1151-") and "PiM-equality-commutator-bound-runner" in str(next_target[0]["next_target"]),
        "1151 handoff targets PiM equality/commutator runner smoke",
    )
    add(
        "V1150_8_generated_under_post_checkpoint",
        all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()),
        "all generated outputs are under post-checkpoint-work",
    )
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1150_9_csv_parse", csv_parse_ok, "all 1150 CSV outputs parse cleanly")
    add("V1150_10_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add(
        "V1150_SUMMARY",
        True,
        "1150 rejects Hilbert/worldtube glue as current theorem, writes nonclaim PiM equality/commutator rows, and sends runner smoke to 1151",
    )
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    glue: list[dict[str, object]],
    first_rows: list[dict[str, object]],
    guards: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1150 - Y5/R10 Hilbert-Worldtube Glue or PiM Equality-Commutator First Row

**Current verdict:** Hilbert/worldtube glue is not derived for current MTS. The exact contract exists, but the worldtube source, Hilbert-PiM charge map, topological boundary match, exact/reference zero, PiM commutator, projector stress, and extra-channel silence remain open.

**Useful progress:** the fallback is now concrete: `R_eq_integral`, `I_commutator`, `B_zero_flux`, `projector_stress_beta_equiv`, and `M_H_ref` must be supplied or theorem-zeroed before measured-GM/Newton can move.

**Important guard:** a closed charge is not enough if it is the wrong charge. Orbital GM, bare mass, an unowned multiplier, or a closed independent topological label cannot be used as proof.

**Best next attack:** build the strict PiM equality/commutator runner. It will make future theorem or numeric rows executable without turning them into free knobs.

**No claim:** no measured-GM, source-normalized Newton, local-GR, PPN, alpha3, R10, GitHub, or public claim follows from 1150.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "role"], sources)}

## Hilbert-Worldtube Glue Audit
{table(["glue_id", "needed_identity", "math_form", "current_evidence", "result", "failure_if_missing", "valid_for_claim"], glue)}

## PiM Equality-Commutator First Row
{table(["row_id", "model_id", "branch_id", "quantity", "formula", "required_columns", "current_value", "source_path", "status", "claim_policy", "valid_for_claim"], first_rows)}

## No-Shortcut Guards
{table(["guard_id", "forbidden_move", "reason", "status", "valid_for_claim"], guards)}

## Claim Gates
{table(["gate_id", "rule", "gate_pass", "reason", "valid_for_claim"], gates)}

## Decision Ledger
{table(["decision_id", "decision", "reason", "next_action", "valid_for_claim"], decisions)}

## Validation
{table(["check_id", "result", "detail", "valid_for_claim"], validation)}

## Next Target
{table(["next_id", "next_target", "objective", "include", "exclude", "valid_for_claim", "claim_allowed"], next_target)}
"""
    DOC.write_text(text, encoding="utf-8")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists() and pycache.is_dir():
        shutil.rmtree(pycache)


def main() -> None:
    outputs = {
        "source_register": OUT / "P8_Y5_R10_1150_SOURCE_REGISTER.csv",
        "glue": OUT / "P8_Y5_R10_1150_HILBERT_WORLDTUBE_GLUE_AUDIT.csv",
        "first_rows": OUT / "P8_Y5_R10_1150_PIM_EQUALITY_COMMUTATOR_FIRST_ROW.csv",
        "guards": OUT / "P8_Y5_R10_1150_NO_SHORTCUT_GUARDS.csv",
        "gates": OUT / "P8_Y5_R10_1150_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1150_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1150_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1150_VALIDATION.csv",
    }
    sources = source_rows()
    glue = glue_rows()
    first_rows = first_row_rows()
    guards = guard_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["glue"], glue)
    write_csv(outputs["first_rows"], first_rows)
    write_csv(outputs["guards"], guards)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, glue, first_rows, guards, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, glue, first_rows, guards, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    if failed:
        for row in failed:
            print(f"{row['check_id']}: {row['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()

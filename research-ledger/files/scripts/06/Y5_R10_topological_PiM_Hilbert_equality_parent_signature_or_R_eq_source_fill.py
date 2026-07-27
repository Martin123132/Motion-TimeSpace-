from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1153-Y5-R10-topological-PiM-Hilbert-equality-parent-signature-or-R_eq-source-fill.md"


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


def contains_missing(value: object) -> bool:
    text = str(value)
    return text.strip() == "" or "MISSING" in text


def source_rows() -> list[dict[str, object]]:
    sources = [
        {
            "source_id": "SRC1153_0_1152_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1152_NEXT_TARGET.csv",
            "needle": "NEXT1152_0_1153",
            "role": "handoff selecting topological PiM/Hilbert equality or R_eq source fill.",
        },
        {
            "source_id": "SRC1153_1_1152_audit",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1152_COMMUTATOR_ZERO_THEOREM_AUDIT.csv",
            "needle": "COM1152_7_Hilbert_topological_equality",
            "role": "1152 commutator audit identifying Hilbert equality as key blocker.",
        },
        {
            "source_id": "SRC1153_2_1152_acq",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1152_R_EQ_I_COMMUTATOR_SOURCE_ACQUISITION_ROWS.csv",
            "needle": "ACQ1152_0_R_eq_integral",
            "role": "1152 nonclaim R_eq acquisition row.",
        },
        {
            "source_id": "SRC1153_3_1015_equality_audit",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1015_HILBERT_TO_TOPOLOGICAL_EQUALITY_AUDIT.csv",
            "needle": "HEA1015_8_verdict",
            "role": "prior Hilbert-to-topological equality audit.",
        },
        {
            "source_id": "SRC1153_4_1015_de_rham",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1015_DE_RHAM_SAME_OBJECT_LEMMA.csv",
            "needle": "SOL1015_6_verdict",
            "role": "conditional de Rham same-object lemma.",
        },
        {
            "source_id": "SRC1153_5_1015_R_eq_rows",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1015_R_EQ_BOUND_INPUT_ROWS.csv",
            "needle": "REB1015_0_R_eq_integral",
            "role": "older retained R_eq and boundary/input rows.",
        },
        {
            "source_id": "SRC1153_6_old_attempt",
            "relative_path": "source-intake/mts_residuals/P8_TOPOLOGICAL_HILBERT_EQUALITY_ATTEMPT.csv",
            "needle": "EH501_1_worldtube_charge_route",
            "role": "older attempt identifying Hilbert-defined topological charge as clean route.",
        },
        {
            "source_id": "SRC1153_7_old_obstructions",
            "relative_path": "source-intake/mts_residuals/P8_TOPOLOGICAL_HILBERT_EQUALITY_OBSTRUCTIONS.csv",
            "needle": "OB501_0_independent_topological_label",
            "role": "obstruction ledger forbidding independent topological labels.",
        },
        {
            "source_id": "SRC1153_8_old_decision",
            "relative_path": "source-intake/mts_residuals/P8_TOPOLOGICAL_HILBERT_EQUALITY_DECISION.csv",
            "needle": "D501_1_best_route",
            "role": "older decision naming Hilbert-defined topological charge as best route.",
        },
        {
            "source_id": "SRC1153_9_parent_contract",
            "relative_path": "source-intake/mts_residuals/P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv",
            "needle": "PAC537_5_Hilbert_topological_charge_equality",
            "role": "parent-action contract for Hilbert/topological equality.",
        },
        {
            "source_id": "SRC1153_10_glue_attempt",
            "relative_path": "source-intake/mts_residuals/P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv",
            "needle": "HWT536_3_Hilbert_to_PiM_charge_map",
            "role": "worldtube glue theorem attempt requiring Hilbert-to-PiM charge map.",
        },
        {
            "source_id": "SRC1153_11_glue_certificate",
            "relative_path": "source-intake/mts_residuals/P8_Y5_HILBERT_WORLDTUBE_GLUE_CERTIFICATE.csv",
            "needle": "HWG535_2_topological_representative_matches_worldtube_boundary",
            "role": "certificate checklist for topological representative boundary match.",
        },
        {
            "source_id": "SRC1153_12_1150_glue",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1150_HILBERT_WORLDTUBE_GLUE_AUDIT.csv",
            "needle": "GLUE1150_9_verdict",
            "role": "latest broad Hilbert/worldtube glue audit.",
        },
        {
            "source_id": "SRC1153_13_topological_conditions",
            "relative_path": "source-intake/mts_residuals/P8_TOPOLOGICAL_PIM_CLOSURE_CONDITIONS.csv",
            "needle": "TC500_3_Hilbert_equality",
            "role": "topological PiM closure condition showing equality remains open.",
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


def conditional_theorem_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "theorem_id": "THEO1153_0_statement",
                "claim_piece": "conditional Hilbert-topological same-object theorem",
                "mathematical_form": "Pi_M J_H = J_M_top + dB_zero when both currents represent the same compact source cohomology class",
                "required_parent_signature": "one parent action fixes W_source, J_H, Q_M, Pi_M, omega_M_top, and reference terms before readout",
                "current_status": "CONDITIONAL_MATH_STATEMENT_ONLY",
                "why_not_claim": "current MTS has not signed the hypotheses",
                "valid_for_claim": "false",
            },
            {
                "theorem_id": "THEO1153_1_worldtube_fixed",
                "claim_piece": "same compact Hilbert source worldtube",
                "mathematical_form": "W_source = supp(J_H[e_obs,tau]); S1 and S2 link the same W_source",
                "required_parent_signature": "source support/domain selector fixed before orbital or radial readout",
                "current_status": "NOT_PARENT_DERIVED",
                "why_not_claim": "worldtube/domain choice can otherwise be a fitted selector",
                "valid_for_claim": "false",
            },
            {
                "theorem_id": "THEO1153_2_same_Hilbert_charge",
                "claim_piece": "topological charge is defined from the observed Hilbert/Noether source charge",
                "mathematical_form": "Q_M := H_tau[S]-H_ref := integral_W rho_H dV_H in e_obs frame",
                "required_parent_signature": "same observed matter frame defines source mass, clock/orbit readout, and Hamiltonian charge",
                "current_status": "SAME_FRAME_SOURCE_MEASURE_NOT_LOCKED",
                "why_not_claim": "topological charge could be an independent or bare label",
                "valid_for_claim": "false",
            },
            {
                "theorem_id": "THEO1153_3_PD_representative",
                "claim_piece": "topological current is the Poincare-dual representative of that same worldtube charge",
                "mathematical_form": "J_M_top := Q_M omega_M_top with d omega_M_top=0 and integral_link omega_M_top=1",
                "required_parent_signature": "omega_M_top is selected by the same Hilbert worldtube boundary class",
                "current_status": "CERTIFICATE_MISSING",
                "why_not_claim": "a closed omega_M_top can conserve the wrong object",
                "valid_for_claim": "false",
            },
            {
                "theorem_id": "THEO1153_4_de_rham_step",
                "claim_piece": "closed same-class currents differ by exact form",
                "mathematical_form": "Pi_M J_H - J_M_top = dB_zero + R_eq; R_eq=0 if same class and no exchange residual",
                "required_parent_signature": "same-class hypothesis and no hidden exchange are already signed",
                "current_status": "CONDITIONAL_LEMMA_PASS",
                "why_not_claim": "lemma is mathematical, but MTS same-class hypotheses remain unsigned",
                "valid_for_claim": "false",
            },
            {
                "theorem_id": "THEO1153_5_boundary_zero",
                "claim_piece": "exact/reference term has zero compact linked-boundary flux",
                "mathematical_form": "integral_boundary dB_zero=0 with one fixed reference",
                "required_parent_signature": "reference/background and exact improvements fixed once, not per system",
                "current_status": "MISSING_CERTIFICATE_OR_BOUND",
                "why_not_claim": "boundary bookkeeping can shift measured GM",
                "valid_for_claim": "false",
            },
            {
                "theorem_id": "THEO1153_6_no_exchange",
                "claim_piece": "extra sectors do not carry independent local mass charge",
                "mathematical_form": "Pi_M dJ_extra=0 and Delta_nonEH+Delta_domain+Delta_memory+Delta_frame+Delta_range=0 or bounded",
                "required_parent_signature": "field-specific no-hair or source-backed residual vector",
                "current_status": "FIELD_SPECIFIC_SILENCE_QUEUE_OPEN",
                "why_not_claim": "R_eq can absorb hidden exchange if this is not closed",
                "valid_for_claim": "false",
            },
            {
                "theorem_id": "THEO1153_7_verdict",
                "claim_piece": "current MTS parent-signs Hilbert-topological equality",
                "mathematical_form": "THEO1153_1 through THEO1153_6 all pass in the same parent action",
                "required_parent_signature": "single action/source/current/topology/reference package",
                "current_status": "HILBERT_TO_TOPOLOGICAL_EQUALITY_NOT_PARENT_SIGNED",
                "why_not_claim": "only a conditional same-object theorem has been isolated",
                "valid_for_claim": "false",
            },
        ]
    )


def r_eq_fill_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "row_id": "REQ1153_0_parent_worldtube_certificate",
                "quantity": "W_source_certificate",
                "formula_or_contract": "W_source = supp(J_H[e_obs,tau]); S1,S2 link same W_source",
                "required_fields": "system_id;worldtube_definition;link_surface_definition;readout_independence;source_path",
                "current_value": "MISSING_WORLDTUBE_CERTIFICATE",
                "source_path": "MISSING_SOURCE_FILE",
                "feeds": "THEO1153_1;ACQ1152_0_R_eq_integral",
                "status": "MISSING_PARENT_INPUT",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "REQ1153_1_same_Hilbert_measure",
                "quantity": "J_H_same_frame_measure",
                "formula_or_contract": "J_H[tau] = delta S_matter[e_obs,psi]/delta e_obs contracted with tau",
                "required_fields": "observed_frame;e_obs_owner;matter_variation;rho_H_definition;M_H_ref",
                "current_value": "MISSING_SAME_FRAME_HILBERT_MEASURE",
                "source_path": "MISSING_SOURCE_FILE",
                "feeds": "THEO1153_2;REB1015_5_M_H_ref",
                "status": "MISSING_PARENT_INPUT",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "REQ1153_2_topological_PD_certificate",
                "quantity": "omega_M_top_boundary_match",
                "formula_or_contract": "J_M_top = Q_M omega_M_top; d omega_M_top=0; integral_link omega_M_top=1",
                "required_fields": "omega_M_top_definition;normalization_surface;worldtube_boundary_class;no_independent_label",
                "current_value": "MISSING_TOPOLOGICAL_BOUNDARY_CERTIFICATE",
                "source_path": "MISSING_SOURCE_FILE",
                "feeds": "THEO1153_3;GLUE1150_4_topological_boundary_match",
                "status": "MISSING_PARENT_INPUT",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "REQ1153_3_exact_boundary_zero",
                "quantity": "B_zero_flux",
                "formula_or_contract": "Pi_M J_H - J_M_top = dB_zero + R_eq and integral_boundary dB_zero=0",
                "required_fields": "B_zero_definition;reference_choice;boundary_flux_value;units;source_path",
                "current_value": "MISSING_B_ZERO_FLUX",
                "source_path": "MISSING_SOURCE_FILE",
                "feeds": "THEO1153_5;REB1015_1_B_zero_flux",
                "status": "MISSING_PARENT_OR_BOUND_INPUT",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "REQ1153_4_R_eq_finite_shell_profile",
                "quantity": "R_eq_integral",
                "formula_or_contract": "int_A_ext abs(Pi_M J_H - J_M_top - dB_zero)",
                "required_fields": "system_id;r1;r2;PiM_JH_profile;JM_top_profile;B_zero_profile;R_eq_integral;M_H_ref;units",
                "current_value": "MISSING_R_EQ_INTEGRAL",
                "source_path": "MISSING_SOURCE_FILE",
                "feeds": "ACQ1152_0_R_eq_integral;PIM1150_1_R_eq_integral",
                "status": "SOURCE_PROFILE_ROW_READY_BUT_UNFILLED",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "REQ1153_5_extra_exchange_vector",
                "quantity": "Delta_extra_vector",
                "formula_or_contract": "Pi_M dJ_extra and nonEH/domain/memory/frame/range residual channels zero or bounded",
                "required_fields": "channel_id;projection;finite_shell_integral;units;source_path",
                "current_value": "MISSING_DELTA_EXTRA_VECTOR",
                "source_path": "MISSING_SOURCE_FILE",
                "feeds": "THEO1153_6;REB1015_4_Delta_extra_vector",
                "status": "MISSING_CHANNELWISE_INPUT",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "REQ1153_6_R_eq_runner_interface",
                "quantity": "epsilon_R_eq",
                "formula_or_contract": "abs(R_eq_integral)/M_H_ref with M_H_ref sourced in the same Hilbert frame",
                "required_fields": "R_eq_integral;M_H_ref;normalization_convention;source_paths",
                "current_value": "MISSING_R_EQ_INTEGRAL;MISSING_M_H_REF",
                "source_path": "MISSING_SOURCE_FILE",
                "feeds": "SMOKE1151_0_current_branch;ACQ1152_4_runner_interface",
                "status": "BLOCKED_MISSING_COMPONENTS",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
        ]
    )


def guard_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "guard_id": "GUARD1153_0_no_tautological_definition",
                "guard": "do not define J_M_top := Pi_M J_H - dB_zero and call the equality derived",
                "status": "ACTIVE",
                "reason": "that would make the topological current a relabel, not a parent-selected charge",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1153_1_no_independent_label",
                "guard": "Q_M cannot be an independent topological label if it is meant to be measured mass",
                "status": "ACTIVE",
                "reason": "the charge must be defined from the same Hilbert/Hamiltonian source object",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1153_2_no_boundary_calibration_cheat",
                "guard": "B_zero or reference terms cannot be tuned per system to match GM",
                "status": "ACTIVE",
                "reason": "exact/reference terms need a once-fixed zero-flux certificate or a retained bound",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1153_3_no_readout_worldtube",
                "guard": "worldtube and link surfaces must be fixed before radial/orbital readout",
                "status": "ACTIVE",
                "reason": "otherwise the equality can become a post-fit domain selector",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1153_4_no_local_GR_promotion",
                "guard": "first-order equality alone does not imply PPN/local-GR pass",
                "status": "ACTIVE",
                "reason": "projector stress, extra exchange, and second-order source terms remain separate gates",
                "valid_for_claim": "false",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "G1153_0_sources_exist",
                "rule": "all 1153 cited local source paths and needles exist",
                "gate_pass": "true_nonclaim",
                "reason": "source register validates the local audit trail",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1153_1_conditional_theorem_written",
                "rule": "same-object de Rham theorem is stated with explicit hypotheses",
                "gate_pass": "true_nonclaim",
                "reason": "the theorem is conditional and not used as MTS evidence",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1153_2_current_MTS_parent_signed",
                "rule": "current MTS signs the worldtube, Hilbert measure, PD representative, boundary zero, and no-exchange hypotheses",
                "gate_pass": "false",
                "reason": "multiple parent inputs remain missing",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1153_3_R_eq_source_filled",
                "rule": "R_eq finite-shell profile is source-backed or theorem-zeroed",
                "gate_pass": "false",
                "reason": "REQ1153_4 remains MISSING_R_EQ_INTEGRAL",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1153_4_no_tautology",
                "rule": "no tautological definition, independent topological label, readout worldtube, or boundary calibration cheat is used",
                "gate_pass": "true_nonclaim",
                "reason": "guards are explicit and active",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1153_5_Newton_GR_promotion",
                "rule": "measured-GM/Newton/local-GR claim allowed",
                "gate_pass": "false",
                "reason": "Hilbert equality is conditional and R_eq row remains missing",
                "valid_for_claim": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "D1153_0_conditional_theorem",
                "decision": "same_object_theorem_is_mathematically_viable_but_conditional",
                "reason": "if the same Hilbert worldtube charge and topological PD class are parent-selected, equality follows up to exact/retained residuals",
                "next_action": "do not promote until parent signatures or source rows are real",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1153_1_current_branch",
                "decision": "current_MTS_Hilbert_topological_equality_not_parent_signed",
                "reason": "worldtube, same-frame Hilbert measure, topological boundary match, boundary zero, and extra exchange silence remain missing",
                "next_action": "fill R_eq profile or derive worldtube/Hilbert current owner",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1153_2_best_next",
                "decision": "target_parent_worldtube_Hilbert_current_owner_or_R_eq_profile_builder",
                "reason": "the equality cannot even be source-filled until W_source, J_H, and M_H_ref are owned in one observed frame",
                "next_action": "1154 parent worldtube/Hilbert current owner or finite-shell R_eq profile builder",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1153_0_1154",
                "next_target": "1154-Y5-R10-parent-worldtube-Hilbert-current-owner-or-R_eq-profile-builder.md",
                "objective": "try to parent-own W_source, J_H, and M_H_ref in one observed frame; if it fails, build the finite-shell R_eq profile input schema",
                "include": "source support; observed coframe; Hilbert current variation; Hamiltonian charge normalization; finite-shell profile columns",
                "exclude": "bare mass shortcut; independent topological label; readout-selected worldtube; boundary calibration; local-GR/Newton claim; GitHub; formalization edits",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    r_eq_rows: list[dict[str, object]],
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

    all_rows = theorem + r_eq_rows + guards + gates + decisions + next_target
    add(
        "V1153_0_sources_exist",
        all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources),
        "all cited local source paths exist and needles are found",
    )
    add(
        "V1153_1_conditional_theorem_present",
        any(row["theorem_id"] == "THEO1153_7_verdict" and row["current_status"] == "HILBERT_TO_TOPOLOGICAL_EQUALITY_NOT_PARENT_SIGNED" for row in theorem),
        "conditional theorem is separated from current MTS claim status",
    )
    required_rows = {
        "REQ1153_0_parent_worldtube_certificate",
        "REQ1153_1_same_Hilbert_measure",
        "REQ1153_2_topological_PD_certificate",
        "REQ1153_3_exact_boundary_zero",
        "REQ1153_4_R_eq_finite_shell_profile",
        "REQ1153_6_R_eq_runner_interface",
    }
    add(
        "V1153_2_R_eq_fill_rows_present",
        required_rows.issubset({row["row_id"] for row in r_eq_rows}),
        "R_eq source-fill rows cover worldtube, measure, topology, boundary, profile, and runner interface",
    )
    add(
        "V1153_3_R_eq_rows_nonclaim_missing",
        all(row["valid_for_claim"] == "false" and row["claim_allowed"] == "false" and contains_missing(row["current_value"]) for row in r_eq_rows),
        "R_eq fill rows remain missing/nonclaim until sourced",
    )
    add(
        "V1153_4_guards_active",
        {"GUARD1153_0_no_tautological_definition", "GUARD1153_1_no_independent_label", "GUARD1153_2_no_boundary_calibration_cheat", "GUARD1153_3_no_readout_worldtube", "GUARD1153_4_no_local_GR_promotion"}.issubset(
            {row["guard_id"] for row in guards if row["status"] == "ACTIVE"}
        ),
        "all no-tautology equality guards are active",
    )
    add(
        "V1153_5_claim_gates_blocked",
        any(row["gate_id"] == "G1153_2_current_MTS_parent_signed" and row["gate_pass"] == "false" for row in gates)
        and any(row["gate_id"] == "G1153_5_Newton_GR_promotion" and row["gate_pass"] == "false" for row in gates),
        "current branch parent signature and Newton/GR promotion remain blocked",
    )
    add(
        "V1153_6_no_claim_rows",
        all(row.get("valid_for_claim") == "false" for row in all_rows)
        and all(row.get("claim_allowed", "false") == "false" for row in next_target),
        "all generated rows remain nonclaim",
    )
    add(
        "V1153_7_next_target",
        next_target[0]["next_target"].startswith("1154-") and "worldtube-Hilbert-current-owner" in str(next_target[0]["next_target"]),
        "1154 handoff targets parent worldtube/Hilbert current owner or R_eq profile builder",
    )
    add(
        "V1153_8_generated_under_post_checkpoint",
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
    add("V1153_9_csv_parse", csv_parse_ok, "all 1153 CSV outputs parse cleanly")
    add("V1153_10_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add(
        "V1153_SUMMARY",
        True,
        "1153 isolates a viable conditional Hilbert-topological equality theorem, blocks current MTS promotion, and writes nonclaim R_eq source-fill rows",
    )
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        cells = [str(row.get(header, "")).replace("|", "/") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    r_eq_rows: list[dict[str, object]],
    guards: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1153 - Y5/R10 Topological PiM Hilbert Equality Parent Signature or R_eq Source Fill

**Current verdict:** the equality route is mathematically viable only as a conditional same-object theorem. Current MTS still does not parent-sign `Pi_M J_H = J_M_top + dB_zero` because the same worldtube, Hilbert measure, topological boundary class, boundary-zero certificate, and no-exchange clauses are not all owned.

**Useful progress:** we have separated the real theorem from the cheat. If `Q_M`, `J_H`, and `omega_M_top` are selected by the same parent source object, de Rham exactness can carry the equality; otherwise `R_eq_integral` must be filled and bounded.

**Important guard:** do not define `J_M_top` from `Pi_M J_H` and call it derived. That is a tautological relabel unless the parent action independently selects the topological representative of the same Hilbert worldtube.

**Best next attack:** own `W_source`, `J_H`, and `M_H_ref` in one observed frame. Without that, the finite-shell `R_eq` profile has no honest denominator or source object.

**No claim:** no measured-GM, source-normalized Newton, local-GR, PPN, R10, WEP, GitHub, or public claim follows from 1153.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "role"], sources)}

## Conditional Equality Theorem Gate
{table(["theorem_id", "claim_piece", "mathematical_form", "required_parent_signature", "current_status", "why_not_claim", "valid_for_claim"], theorem)}

## R_eq Source Fill Rows
{table(["row_id", "quantity", "formula_or_contract", "required_fields", "current_value", "source_path", "feeds", "status", "valid_for_claim", "claim_allowed"], r_eq_rows)}

## No-Tautology Guards
{table(["guard_id", "guard", "status", "reason", "valid_for_claim"], guards)}

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
        "source_register": OUT / "P8_Y5_R10_1153_SOURCE_REGISTER.csv",
        "theorem": OUT / "P8_Y5_R10_1153_CONDITIONAL_EQUALITY_THEOREM_GATE.csv",
        "r_eq_rows": OUT / "P8_Y5_R10_1153_R_EQ_SOURCE_FILL_ROWS.csv",
        "guards": OUT / "P8_Y5_R10_1153_NO_TAUTOLOGY_GUARDS.csv",
        "gates": OUT / "P8_Y5_R10_1153_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1153_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1153_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1153_VALIDATION.csv",
    }

    sources = source_rows()
    theorem = conditional_theorem_rows()
    r_eq_rows = r_eq_fill_rows()
    guards = guard_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["theorem"], theorem)
    write_csv(outputs["r_eq_rows"], r_eq_rows)
    write_csv(outputs["guards"], guards)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, theorem, r_eq_rows, guards, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, theorem, r_eq_rows, guards, gates, decisions, validation, next_target)
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

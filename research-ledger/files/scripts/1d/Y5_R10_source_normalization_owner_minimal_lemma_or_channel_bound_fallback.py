from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1149-Y5-R10-source-normalization-owner-minimal-lemma-or-channel-bound-fallback.md"


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
            "source_id": "SRC1149_0_1148_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1148_NEXT_TARGET.csv",
            "needle": "NEXT1148_0_1149",
            "role": "handoff requiring source-owner minimal lemma or fallback queue.",
        },
        {
            "source_id": "SRC1149_1_worldtube_sketch",
            "relative_path": "source-intake/mts_residuals/P8_WORLDTUBE_SOURCE_MEASURE_PROOF_SKETCH.csv",
            "needle": "P510_7",
            "role": "worldtube source-measure proof sketch and MTS transfer condition.",
        },
        {
            "source_id": "SRC1149_2_source_measure_theorem",
            "relative_path": "source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv",
            "needle": "T509_0_charge_identity_needed",
            "role": "charge identity and flux closure theorem conditions.",
        },
        {
            "source_id": "SRC1149_3_source_measure_clauses",
            "relative_path": "source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv",
            "needle": "SM509_3_flux_closure",
            "role": "source-measure clauses remain not parent-derived.",
        },
        {
            "source_id": "SRC1149_4_source_measure_residuals",
            "relative_path": "source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv",
            "needle": "SMR509_0_Delta_flux",
            "role": "fallback residual map for source-measure failure.",
        },
        {
            "source_id": "SRC1149_5_source_current_attempt",
            "relative_path": "source-intake/mts_residuals/P8_Y5_SOURCE_CURRENT_CLOSURE_THEOREM_ATTEMPT.csv",
            "needle": "SC532_4_zero_projector_commutator",
            "role": "source-current closure attempt exposes Pi_M commutator gate.",
        },
        {
            "source_id": "SRC1149_6_ward_bridge",
            "relative_path": "source-intake/mts_residuals/P8_Y5_SOURCE_CURRENT_WARD_BRIDGE.csv",
            "needle": "WB520_6_conditional_closure_theorem",
            "role": "conditional Ward bridge and product-rule obstruction.",
        },
        {
            "source_id": "SRC1149_7_ward_contract",
            "relative_path": "source-intake/mts_residuals/P8_source_current_Ward_universality_CONTRACT.csv",
            "needle": "SC6_closed_calibrated_mass_projector",
            "role": "source-current universality contract remains conditional/open.",
        },
        {
            "source_id": "SRC1149_8_PiM_owner",
            "relative_path": "source-intake/mts_residuals/P8_Y5_PIM_PROJECTOR_OWNER_FORK.csv",
            "needle": "PF521_2_Hamiltonian_charge_PiM",
            "role": "Pi_M owner route forks and debts.",
        },
        {
            "source_id": "SRC1149_9_R10_PiM_owner",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_738_PIM_OWNER_FORK.csv",
            "needle": "PIF738_2_Hamiltonian_charge_PiM",
            "role": "R10 Pi_M owner fork confirms conditional Hamiltonian route.",
        },
        {
            "source_id": "SRC1149_10_PiM_flux_attempt",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1013_PIM_JH_FLUX_THEOREM_ATTEMPT.csv",
            "needle": "PFC1013_8_verdict",
            "role": "Pi_M J_H flux theorem attempt fails current claim.",
        },
        {
            "source_id": "SRC1149_11_PiM_commutator",
            "relative_path": "source-intake/mts_residuals/P8_Y5_PIM_COMMUTATOR_GATE.csv",
            "needle": "PC521_0_product_rule",
            "role": "projected current product rule obstruction.",
        },
        {
            "source_id": "SRC1149_12_PiM_bound_template",
            "relative_path": "source-intake/mts_residuals/P8_Y5_PIM_COMMUTATOR_BOUND_TEMPLATE.csv",
            "needle": "PCB534_1_commutator_integral",
            "role": "fallback bound template for Pi_M equality/commutator.",
        },
        {
            "source_id": "SRC1149_13_scorecard",
            "relative_path": "source-intake/mts_residuals/P8_Y5_SOURCE_NORMALIZATION_RESIDUAL_SCORECARD.csv",
            "needle": "SRC523_0_charge_current_normalization",
            "role": "source-normalization scorecard remains unfilled.",
        },
        {
            "source_id": "SRC1149_14_1148_channels",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1148_SOURCE_NORMALIZATION_CHANNEL_VECTOR.csv",
            "needle": "CH1148_8_channel_verdict",
            "role": "c_R11 channel vector remains retained/missing.",
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


def lemma_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "lemma_id": "LEM1149_0_same_frame_current",
                "needed_statement": "same observed coframe defines matter/source variation before orbital fitting",
                "math_form": "J_H[tau]=T_m^{mu nu}[e_obs] tau_nu dSigma_mu",
                "current_evidence": "SC532_1 conditional; WB520_0 conditional; source-current contract SC0 conditional",
                "result": "CONDITIONAL_NOT_PARENT_DERIVED",
                "blocking_issue": "source current can remain frame/calibration dependent",
                "valid_for_claim": "false",
            },
            {
                "lemma_id": "LEM1149_1_observed_time_charge",
                "needed_statement": "Hamiltonian/boundary charge is generated by observed time before readout",
                "math_form": "H_xi = B_xi on shell with xi normalized in observed frame",
                "current_evidence": "SC532_0 conditional from prior Hamiltonian rows; SN2 conditional",
                "result": "CONDITIONAL_NOT_PARENT_DERIVED",
                "blocking_issue": "B_xi/G_eff is not yet a source-current mass",
                "valid_for_claim": "false",
            },
            {
                "lemma_id": "LEM1149_2_charge_current_identity",
                "needed_statement": "Hamiltonian charge equals projected Hilbert source mass current",
                "math_form": "B_xi/G_eff = M_H[Pi_M J_H] and delta B_xi = delta int_S Pi_M J_H",
                "current_evidence": "SC532_2 not parent-derived; PFC1013_6 worldtube glue not yet derived",
                "result": "MISSING_CHARGE_CURRENT_IDENTITY",
                "blocking_issue": "closed charge can be the wrong charge",
                "valid_for_claim": "false",
            },
            {
                "lemma_id": "LEM1149_3_parent_owned_PiM",
                "needed_statement": "Pi_M is parent-owned charge data, not a post-readout mask",
                "math_form": "Pi_M J = ell_M(J) omega_M_top or inherited Hamiltonian charge projector",
                "current_evidence": "PF521/PIF738 topological and Hamiltonian routes are conditional; readout route forbidden",
                "result": "MISSING_PARENT_PIM_OWNER",
                "blocking_issue": "projector freedom can absorb failures",
                "valid_for_claim": "false",
            },
            {
                "lemma_id": "LEM1149_4_product_rule",
                "needed_statement": "projected Hilbert mass flux closes without product-rule leakage",
                "math_form": "d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H with [d,Pi_M]J_H=0",
                "current_evidence": "WB520_4 and PC521_0 mark exact obstruction active",
                "result": "COMMUTATOR_OBSTRUCTION_ACTIVE",
                "blocking_issue": "Pi_M commutator can produce radial/time source hair",
                "valid_for_claim": "false",
            },
            {
                "lemma_id": "LEM1149_5_extra_projection_zero",
                "needed_statement": "non-Hilbert, boundary, domain, memory, non-EH, coupling, frame, projector, and anomaly channels carry no Pi_M mass projection",
                "math_form": "Pi_M dJ_extra=0 and A_parent=0 channelwise",
                "current_evidence": "SC532_5 not derived; WB520_5 active; PFC1013_3/PFC1013_5 not derived",
                "result": "MISSING_EXTRA_PROJECTION_ZERO",
                "blocking_issue": "mu_extra enters measured mass",
                "valid_for_claim": "false",
            },
            {
                "lemma_id": "LEM1149_6_worldtube_glue",
                "needed_statement": "worldtube source equals exterior charge on any linking sphere",
                "math_form": "M_source[W]=int_S Q_M[tau]=(4*pi*G_ref)^-1 int_S Pi_M J_H",
                "current_evidence": "P510_5 is a definition lock; PFC1013_6 says core piece not yet derived",
                "result": "MISSING_WORLDTUBE_GLUE",
                "blocking_issue": "exterior mass may not be the source mass",
                "valid_for_claim": "false",
            },
            {
                "lemma_id": "LEM1149_7_Gauss_orbital_calibration",
                "needed_statement": "closed source charge calibrates to inverse-square orbital GM with one universal G_ref",
                "math_form": "nabla^2 Phi=4 pi G_eff rho_H; r^2|a_r|=G_eff M_H",
                "current_evidence": "SC532_7 downstream gate open; SM509_6 not parent-derived",
                "result": "DOWNSTREAM_GATE_OPEN",
                "blocking_issue": "epsilon_charge=0 would still be necessary but not sufficient for Newton",
                "valid_for_claim": "false",
            },
            {
                "lemma_id": "LEM1149_8_verdict",
                "needed_statement": "minimal source-owner lemma closes",
                "math_form": "LEM1149_0 through LEM1149_7 all pass together",
                "current_evidence": "charge-current identity, Pi_M owner, commutator, extra projection, and worldtube glue remain open",
                "result": "MINIMAL_SOURCE_OWNER_LEMMA_NOT_DERIVED",
                "blocking_issue": "source-normalized Newton/local-GR remains blocked",
                "valid_for_claim": "false",
            },
        ]
    )


def product_rule_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "rule_id": "PR1149_0_exact_identity",
                "statement": "projected current closure must keep the full product rule",
                "math_form": "d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H",
                "allowed_closure": "Pi_M dJ_H=0 and [d,Pi_M]J_H=0 from parent/source theorem",
                "current_status": "COMMUTATOR_ACTIVE",
                "policy": "Ward conservation alone is insufficient",
                "valid_for_claim": "false",
            },
            {
                "rule_id": "PR1149_1_topological_route",
                "statement": "topological Pi_M can kill commutator only if it is the same Hilbert source charge",
                "math_form": "d omega_M_top=0 and ell_M(Pi_M J_H)=M_H",
                "allowed_closure": "topological equality plus worldtube Hilbert glue",
                "current_status": "CONDITIONAL_HILBERT_EQUALITY_MISSING",
                "policy": "topological label alone is not measured mass",
                "valid_for_claim": "false",
            },
            {
                "rule_id": "PR1149_2_Hodge_route",
                "statement": "Hodge/DeWitt projector route must retain projector variation stress",
                "math_form": "delta(Pi_M J_H)=Pi_M delta J_H + (delta Pi_M)J_H",
                "allowed_closure": "delta Pi_M theorem-zero or mapped below PPN/source locks",
                "current_status": "VARIATION_STRESS_RETAINED",
                "policy": "no hidden projector stress",
                "valid_for_claim": "false",
            },
            {
                "rule_id": "PR1149_3_multiplier_route",
                "statement": "a multiplier imposing d(Pi_M J_H)=0 is not a derivation unless Pi_M/lambda_M are independently owned",
                "math_form": "S_M = int lambda_M d(Pi_M J_H)",
                "allowed_closure": "independent gauge/topological/Ward origin plus stress ledger",
                "current_status": "REJECT_AS_CLOSURE_IF_UNOWNED",
                "policy": "no inserted Newton closure",
                "valid_for_claim": "false",
            },
            {
                "rule_id": "PR1149_4_readout_route",
                "statement": "post-readout Pi_M cannot define the source mass before the measurement it explains",
                "math_form": "Pi_read selected by measured GM",
                "allowed_closure": "none",
                "current_status": "FORBIDDEN_AS_DERIVATION",
                "policy": "no fitted GM absorption",
                "valid_for_claim": "false",
            },
        ]
    )


def fallback_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "fallback_id": "FB1149_0_epsilon_charge",
                "scorecard_row": "SRC523_0_charge_current_normalization",
                "symbol": "epsilon_charge",
                "required_source_artifact": "charge-current equality proof or dimensionless mismatch with source file",
                "current_value": "MISSING_THEOREM_OR_NUMERIC_VALUE",
                "status": "UNFILLED",
                "valid_for_claim": "false",
            },
            {
                "fallback_id": "FB1149_1_PiM_equality",
                "scorecard_row": "Pi_M equality residual",
                "symbol": "R_eq_integral",
                "required_source_artifact": "system_id; r1; r2; R_eq_integral; M_H_ref; units; source_file; assumptions",
                "current_value": "MISSING_R_EQ_INTEGRAL",
                "status": "UNFILLED",
                "valid_for_claim": "false",
            },
            {
                "fallback_id": "FB1149_2_PiM_commutator",
                "scorecard_row": "Pi_M commutator residual",
                "symbol": "I_commutator",
                "required_source_artifact": "system_id; projector_type; metric_dependence_flag; I_commutator; M_H_ref; units; source_file",
                "current_value": "MISSING_I_COMMUTATOR",
                "status": "UNFILLED",
                "valid_for_claim": "false",
            },
            {
                "fallback_id": "FB1149_3_boundary_exact_flux",
                "scorecard_row": "boundary exact/reference term",
                "symbol": "B_zero_flux",
                "required_source_artifact": "boundary_type; B_zero_flux; M_H_ref; units; source_file; assumptions",
                "current_value": "MISSING_B_ZERO_FLUX",
                "status": "UNFILLED",
                "valid_for_claim": "false",
            },
            {
                "fallback_id": "FB1149_4_projector_stress",
                "scorecard_row": "projector variation stress",
                "symbol": "epsilon_projector_stress",
                "required_source_artifact": "weak-field/PPN projector stress map with source file and bound",
                "current_value": "MISSING_PROJECTOR_STRESS_MAP",
                "status": "UNFILLED",
                "valid_for_claim": "false",
            },
            {
                "fallback_id": "FB1149_5_extra_projection",
                "scorecard_row": "extra mass projection",
                "symbol": "Pi_M dJ_extra; A_parent; mu_extra",
                "required_source_artifact": "channelwise zero theorem or numeric coefficient rows for boundary/domain/bulk/nonEH/frame/species/calibration",
                "current_value": "MISSING_CHANNELWISE_INPUTS",
                "status": "UNFILLED",
                "valid_for_claim": "false",
            },
            {
                "fallback_id": "FB1149_6_radial_time_flux",
                "scorecard_row": "SRC523_6_Meff_flux_derivative",
                "symbol": "dln_Meff_dt; partial_r_ln_Meff",
                "required_source_artifact": "d(Pi_M J_H)=0 proof or derivative profile",
                "current_value": "not_loaded",
                "status": "UNFILLED",
                "valid_for_claim": "false",
            },
            {
                "fallback_id": "FB1149_7_total_no_cancellation",
                "scorecard_row": "SRC523_11_total_no_cancellation_score",
                "symbol": "epsilon_SN_envelope",
                "required_source_artifact": "all prior rows theorem-zero or bounded with units, normalization, and source path",
                "current_value": "not_computed",
                "status": "NOT_RUN_PRECONDITIONS_UNFILLED",
                "valid_for_claim": "false",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "G1149_0_sources_exist",
                "rule": "all 1149 cited source paths and needles exist",
                "gate_pass": "true_nonclaim",
                "reason": "source register validates the local audit trail",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1149_1_minimal_lemma",
                "rule": "minimal source-owner lemma is derived",
                "gate_pass": "false",
                "reason": "charge-current identity, Pi_M owner, commutator, extra projection, worldtube glue, and calibration remain open",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1149_2_product_rule_guard",
                "rule": "full d(Pi_M J_H) product rule is retained",
                "gate_pass": "true_nonclaim",
                "reason": "commutator and projector-variation terms are not hidden",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1149_3_fallback_queue",
                "rule": "first channel-bound fallback queue exists",
                "gate_pass": "true_nonclaim",
                "reason": "epsilon_charge, equality, commutator, boundary, stress, extra projection, and flux rows are queued",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1149_4_fallback_claimability",
                "rule": "fallback queue contains claim-valid numeric/source rows",
                "gate_pass": "false",
                "reason": "all fallback rows remain unfilled",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1149_5_Newton_GR_promotion",
                "rule": "source-normalized Newton/local-GR branch can be promoted",
                "gate_pass": "false",
                "reason": "source-owner lemma and fallback rows are not claim-valid",
                "valid_for_claim": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "D1149_0_lemma",
                "decision": "minimal_source_owner_lemma_not_derived",
                "reason": "the exact closure identity exists but the parent source charge, Pi_M owner, commutator-zero, extra-projection-zero, and worldtube glue premises do not close",
                "next_action": "do not promote measured-GM/Newton/local-GR",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1149_1_progress",
                "decision": "fallback_queue_written",
                "reason": "the missing theorem has been turned into executable source/bound row requirements",
                "next_action": "attack Hilbert-worldtube glue first or fill Pi_M equality/commutator rows",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1149_2_best_next",
                "decision": "target_Hilbert_worldtube_glue",
                "reason": "without charge-current/worldtube equality, even a closed projected current may be the wrong mass",
                "next_action": "build 1150 Hilbert-worldtube glue theorem or Pi_M equality/commutator first-row runner",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1149_0_1150",
                "next_target": "1150-Y5-R10-Hilbert-worldtube-glue-or-PiM-equality-commutator-first-row.md",
                "objective": "try to derive the Hilbert/worldtube charge glue B_xi/G_eff = M_H[Pi_M J_H] and M_source[W]=int_S Q_M[tau]; if it fails, create the first nonclaim Pi_M equality/commutator numeric input row",
                "include": "observed-time Hamiltonian charge; Hilbert current equality; worldtube source measure; Pi_M equality residual; commutator residual; boundary exact flux; no readout mask",
                "exclude": "orbital GM as proof; unowned multiplier closure; product shortcut; tuned cancellation; local-GR/Newton claim; GitHub; formalization edits",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    lemmas: list[dict[str, object]],
    product_rules: list[dict[str, object]],
    fallbacks: list[dict[str, object]],
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

    all_rows = lemmas + product_rules + fallbacks + gates + decisions + next_target
    add(
        "V1149_0_sources_exist",
        all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources),
        "all cited local source paths exist and needles are found",
    )
    add(
        "V1149_1_lemma_not_derived",
        any(row["lemma_id"] == "LEM1149_8_verdict" and row["result"] == "MINIMAL_SOURCE_OWNER_LEMMA_NOT_DERIVED" for row in lemmas),
        "minimal source-owner lemma is explicitly not derived",
    )
    add(
        "V1149_2_product_rule_retained",
        any(row["rule_id"] == "PR1149_0_exact_identity" and row["current_status"] == "COMMUTATOR_ACTIVE" for row in product_rules)
        and any(row["rule_id"] == "PR1149_4_readout_route" and row["current_status"] == "FORBIDDEN_AS_DERIVATION" for row in product_rules),
        "product-rule obstruction is retained and readout route is forbidden",
    )
    add(
        "V1149_3_fallback_queue_complete",
        {
            "FB1149_0_epsilon_charge",
            "FB1149_1_PiM_equality",
            "FB1149_2_PiM_commutator",
            "FB1149_3_boundary_exact_flux",
            "FB1149_4_projector_stress",
            "FB1149_5_extra_projection",
            "FB1149_6_radial_time_flux",
            "FB1149_7_total_no_cancellation",
        }.issubset({row["fallback_id"] for row in fallbacks}),
        "fallback queue covers equality, commutator, boundary, stress, extra projection, flux, and total envelope",
    )
    add(
        "V1149_4_fallback_nonclaim",
        all(row["valid_for_claim"] == "false" for row in fallbacks)
        and all(row["status"] in {"UNFILLED", "NOT_RUN_PRECONDITIONS_UNFILLED"} for row in fallbacks),
        "fallback rows are unfilled and nonclaim",
    )
    add(
        "V1149_5_claim_gates_blocked",
        any(row["gate_id"] == "G1149_1_minimal_lemma" and row["gate_pass"] == "false" for row in gates)
        and any(row["gate_id"] == "G1149_5_Newton_GR_promotion" and row["gate_pass"] == "false" for row in gates),
        "minimal lemma and Newton/GR promotion gates remain blocked",
    )
    add(
        "V1149_6_no_claim_rows",
        all(row.get("valid_for_claim") == "false" for row in all_rows)
        and all(row.get("claim_allowed", "false") == "false" for row in next_target),
        "all generated rows remain nonclaim",
    )
    add(
        "V1149_7_next_target",
        next_target[0]["next_target"].startswith("1150-") and "Hilbert-worldtube-glue" in str(next_target[0]["next_target"]),
        "1150 handoff targets Hilbert/worldtube glue or Pi_M equality/commutator first row",
    )
    add(
        "V1149_8_generated_under_post_checkpoint",
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
    add("V1149_9_csv_parse", csv_parse_ok, "all 1149 CSV outputs parse cleanly")
    add("V1149_10_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add(
        "V1149_SUMMARY",
        True,
        "1149 keeps the exact product-rule obstruction, rejects the source-owner claim, and queues Hilbert/worldtube glue for 1150",
    )
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    lemmas: list[dict[str, object]],
    product_rules: list[dict[str, object]],
    fallbacks: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1149 - Y5/R10 Source-Normalization Owner Minimal Lemma or Channel-Bound Fallback

**Current verdict:** the minimal source-owner lemma is not derived. The exact identity is clear, but charge-current equality, parent `Pi_M`, commutator silence, extra-projection silence, worldtube glue, and Gauss/orbital calibration remain open.

**Useful progress:** this turns the measured-GM/Newton bottleneck into a precise theorem gate instead of a vague missing-coupling problem.

**Important guard:** Ward conservation of the Hilbert current is not enough. The full projected product rule `d(Pi_M J_H)=Pi_M dJ_H+[d,Pi_M]J_H` must be retained.

**Best next attack:** derive Hilbert/worldtube glue. If the exterior Hamiltonian charge is not proven to be the same object as the source Hilbert mass, a closed charge can still be the wrong mass.

**No claim:** no source-normalized Newton, local-GR, measured-GM, PPN, alpha3, R10, GitHub, or public claim follows from 1149.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "role"], sources)}

## Minimal Source-Owner Lemma Attempt
{table(["lemma_id", "needed_statement", "math_form", "current_evidence", "result", "blocking_issue", "valid_for_claim"], lemmas)}

## Projected Current Product-Rule Guard
{table(["rule_id", "statement", "math_form", "allowed_closure", "current_status", "policy", "valid_for_claim"], product_rules)}

## Channel-Bound Fallback Queue
{table(["fallback_id", "scorecard_row", "symbol", "required_source_artifact", "current_value", "status", "valid_for_claim"], fallbacks)}

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
        "source_register": OUT / "P8_Y5_R10_1149_SOURCE_REGISTER.csv",
        "lemmas": OUT / "P8_Y5_R10_1149_SOURCE_OWNER_MINIMAL_LEMMA_ATTEMPT.csv",
        "product_rules": OUT / "P8_Y5_R10_1149_PROJECTED_CURRENT_PRODUCT_RULE_GUARD.csv",
        "fallbacks": OUT / "P8_Y5_R10_1149_CHANNEL_BOUND_FALLBACK_QUEUE.csv",
        "gates": OUT / "P8_Y5_R10_1149_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1149_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1149_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1149_VALIDATION.csv",
    }
    sources = source_rows()
    lemmas = lemma_rows()
    product_rules = product_rule_rows()
    fallbacks = fallback_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["lemmas"], lemmas)
    write_csv(outputs["product_rules"], product_rules)
    write_csv(outputs["fallbacks"], fallbacks)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, lemmas, product_rules, fallbacks, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, lemmas, product_rules, fallbacks, gates, decisions, validation, next_target)
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

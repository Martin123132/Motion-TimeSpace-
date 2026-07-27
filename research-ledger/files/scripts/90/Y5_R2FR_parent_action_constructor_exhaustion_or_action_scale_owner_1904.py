from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1904"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1904-Y5-R2FR-parent-action-constructor-exhaustion-or-action-scale-owner.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()


INPUTS = {
    "1903_doc": ROOT / "1903-Y5-R2FR-no-source-only-slot-parent-grammar-or-profile-map-input-fill.md",
    "1903_validation": OUT / "P8_Y5_BRR545_1903_VALIDATION.csv",
    "1903_grammar": OUT / "P8_Y5_PARENT_QLOC_1903_NO_SOURCE_ONLY_SLOT_PARENT_GRAMMAR_ATTEMPT.csv",
    "1903_constructor_gate": OUT / "P8_Y5_PARENT_QLOC_1903_NOHOM_CONSTRUCTOR_GATE.csv",
    "1903_profile_fill": OUT / "P8_Y5_PARENT_QLOC_1903_PROFILE_MAP_INPUT_FILL_NONCLAIM.csv",
    "1903_next": OUT / "P8_Y5_PARENT_QLOC_1903_NEXT_TARGET.csv",
    "1055_parent_action": OUT / "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv",
    "1220_typed_signature": OUT / "P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv",
    "1338_object_language": OUT / "P8_Y5_R10_1338_OBJECT_LANGUAGE_THEOREM_ATTEMPT.csv",
    "1694_variation_identity": OUT / "P8_Y5_PARENT_QLOC_1694_SOURCE_WEIGHT_VARIATION_IDENTITY.csv",
    "1887_action_scale_audit": OUT / "P8_Y5_PARENT_QLOC_1887_ACTION_SCALE_NORMALIZATION_AUDIT.csv",
    "1888_action_owner": OUT / "P8_Y5_PARENT_QLOC_1888_ACTION_SCALE_OWNER_PROOF_ATTEMPT.csv",
    "1897_action_readout": OUT / "P8_Y5_PARENT_QLOC_1897_ACTION_SCALE_READOUT_STABILITY_ATTEMPT.csv",
    "1067_action_scale": OUT / "P8_Y5_R10_1067_PARENT_ACTION_SCALE_OWNER_ATTEMPT.csv",
    "1230_universal_action_scale": OUT / "P8_Y5_R10_1230_ACTION_SCALE_OWNER_THEOREM_ATTEMPT.csv",
    "1107_exhaustion": OUT / "P8_Y5_R10_1107_OBJECT_LANGUAGE_EXHAUSTION_ATTEMPT.csv",
    "1114_no_hidden_visible": OUT / "P8_Y5_R10_1114_NO_HIDDEN_VISIBLE_MORPHISM_THEOREM_ATTEMPT.csv",
    "1092_invariant_triviality": OUT / "P8_Y5_R10_1092_HIDDEN_INVARIANT_TRIVIALITY_ATTEMPT.csv",
    "1901_gm_guard": OUT / "P8_Y5_PARENT_QLOC_1901_COMMON_MODE_ABSORPTION_ALGEBRA.csv",
}


SOURCE_NEEDLES = {
    "1903_doc": ["NEXT1903_0_primary", "1904-Y5-R2FR-parent-action-constructor-exhaustion-or-action-scale-owner.md"],
    "1903_validation": ["VAL1903_OVERALL,PASS"],
    "1903_grammar": ["NSG1903_7_verdict", "NO_SOURCE_ONLY_SLOT_PARENT_GRAMMAR_NOT_DERIVED"],
    "1903_constructor_gate": ["NHG1903_6_verdict", "NO_SOURCE_ONLY_SLOT_CLAIM_BLOCKED"],
    "1903_profile_fill": ["PF1903_7_verdict", "PROFILE_MAP_INPUTS_NOT_SCORE_READY"],
    "1903_next": ["NEXT1903_0_primary", "parent action generator"],
    "1055_parent_action": ["PAC1055_6_single_parent_action", "SCHEMA_WRITTEN_NOT_DERIVED_FROM_DEEPER_MTS"],
    "1220_typed_signature": ["PTOL1220_7_verdict", "PARENT_TYPED_OBJECT_LANGUAGE_SIGNATURE_NOT_DERIVED"],
    "1338_object_language": ["OLT1338_6_verdict", "NOT_DERIVED_CURRENT_CORPUS"],
    "1694_variation_identity": ["VAR1694_5_identity_verdict", "source-weight variation identity"],
    "1887_action_scale_audit": ["ASN1887_5_verdict", "ACTION_SCALE_OWNER_UNSIGNED"],
    "1888_action_owner": ["ASO1888_7_verdict", "ACTION_SCALE_OWNER_NOT_DERIVED"],
    "1897_action_readout": ["ASR1897_6_verdict", "ACTION_SCALE_READOUT_STABILITY_NOT_PARENT_DERIVED"],
    "1067_action_scale": ["ASO1067_5_verdict", "CONDITIONAL_NOT_PARENT_DERIVED"],
    "1230_universal_action_scale": ["UAS1230_5_verdict", "CONDITIONAL_THEOREM_ONLY_NOT_CLAIMABLE"],
    "1107_exhaustion": ["EXH1107_6_verdict", "OBJECT_LANGUAGE_EXHAUSTION_NOT_DERIVED"],
    "1114_no_hidden_visible": ["NHV1114_6_verdict", "NO_HIDDEN_VISIBLE_MORPHISM_NOT_DERIVED"],
    "1092_invariant_triviality": ["HIT1092_5_verdict", "TRIVIALITY_NOT_DERIVED"],
    "1901_gm_guard": ["ALG1901_3_claim_limit", "NO_CLAIM_PROMOTION"],
}


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1904_SOURCE_REGISTER.csv",
    "constructor_exhaustion": OUT / "P8_Y5_PARENT_QLOC_1904_PARENT_ACTION_CONSTRUCTOR_EXHAUSTION_ATTEMPT.csv",
    "action_scale_owner": OUT / "P8_Y5_PARENT_QLOC_1904_ACTION_SCALE_OWNER_ATTEMPT.csv",
    "finite_residual": OUT / "P8_Y5_PARENT_QLOC_1904_FINITE_SOURCE_WEIGHT_RESIDUAL_BRANCH_NONCLAIM.csv",
    "dryrun_cases": OUT / "P8_Y5_PARENT_QLOC_1904_ACTION_OWNER_DRYRUN_CASES.csv",
    "dryrun_results": OUT / "P8_Y5_PARENT_QLOC_1904_ACTION_OWNER_DRYRUN_RESULTS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1904_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1904_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1904_NEXT_TARGET.csv",
    "project_status": OUT / "P8_Y5_PARENT_QLOC_1904_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1904_VALIDATION.csv",
}


BRANCH_COPIES = {
    "constructor_exhaustion": SOURCE_WEIGHT_DOCS / "PARENT_ACTION_CONSTRUCTOR_EXHAUSTION_1904_NONCLAIM.csv",
    "action_scale_owner": MICROSCOPE_RESIDUALS / OUTPUTS["action_scale_owner"].name,
    "finite_residual": QUEUE / "JR1904_FINITE_SOURCE_WEIGHT_RESIDUAL_BRANCH_NONCLAIM.csv",
    "dryrun_results": QUARANTINE / OUTPUTS["dryrun_results"].name,
}


def ensure_dirs() -> None:
    for path in [OUT, MICROSCOPE_RESIDUALS, QUEUE, SOURCE_WEIGHT_DOCS, QUARANTINE]:
        path.mkdir(parents=True, exist_ok=True)


def bool_string(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value).strip().lower()


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
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


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path in INPUTS.items():
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        missing = [needle for needle in SOURCE_NEEDLES[source_id] if needle not in text]
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle_count": len(SOURCE_NEEDLES[source_id]),
                "missing_needles": "; ".join(missing),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing else "SOURCE_OR_NEEDLE_MISSING",
                "valid_for_claim": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def constructor_exhaustion_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "CE1904_0_target",
            "claim_piece": "parent action constructor exhaustion",
            "formal_statement": "Allowed ordinary-sector source coefficients are exhausted by ParentGenerate[q(Phi),theta_rep,topological level,universal calibration]; no extra source-only coefficient algebra exists.",
            "status": "TARGET_SHARP",
            "proof_or_obstruction": "if this is parent-signed, w_A is not merely set to one: the parent action has no constructor that can generate it",
            "source_anchor": "P8_Y5_PARENT_QLOC_1903_NEXT_TARGET.csv:NEXT1903_0_primary; P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv:PAC1055_6_single_parent_action",
            "conditional_theorem": True,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "CE1904_1_normal_form",
            "claim_piece": "single parent action normal form",
            "formal_statement": "S_parent = S_geom[Phi]+S_hidden[Phi]+S_EM[q(Phi),A_Q,ell]+sum_A S_A[Psi_A,e(qPhi),A_Q,theta_A]+S_boundary[q(Phi)].",
            "status": "EXACT_IF_NORMAL_FORM_PARENT_DERIVED",
            "proof_or_obstruction": "this normal form contains representation constants and ordinary matter fields, but no source-only species prefactor slot",
            "source_anchor": "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv:PAC1055_2_matter_functor;PAC1055_6_single_parent_action",
            "conditional_theorem": True,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "CE1904_2_chain_rule_zero",
            "claim_piece": "vertical/label derivative of allowed coefficients",
            "formal_statement": "If c_vis=cbar(q(Phi),theta_rep,ell) and Dq[v_label]=Dtheta[v_label]=Dell[v_label]=0, then Lie_v_label c_vis=0.",
            "status": "EXACT_CONDITIONAL_CHAIN_RULE",
            "proof_or_obstruction": "source-only labels cannot move allowed coefficients once those coefficients are proven to lie in the parent-generated image",
            "source_anchor": "P8_Y5_R10_1107_OBJECT_LANGUAGE_EXHAUSTION_ATTEMPT.csv:EXH1107_1_chain_rule; P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv:PTOL1220_1_visible_coefficient_domain",
            "conditional_theorem": True,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "CE1904_3_membership_gap",
            "claim_piece": "membership in Image(ParentGenerate)",
            "formal_statement": "Every coefficient that reaches source, clocks, masses, EM, and WEP readout is in Image(ParentGenerate), not in a larger EFT/readout coefficient algebra.",
            "status": "IMAGE_MEMBERSHIP_NOT_DERIVED",
            "proof_or_obstruction": "the chain rule is solid, but the present corpus still lacks the primitive-to-parent-generator construction",
            "source_anchor": "P8_Y5_R10_1107_OBJECT_LANGUAGE_EXHAUSTION_ATTEMPT.csv:EXH1107_6_verdict; P8_Y5_R10_1338_OBJECT_LANGUAGE_THEOREM_ATTEMPT.csv:OLT1338_2_MTS_primitive_constructor",
            "conditional_theorem": False,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "CE1904_4_hidden_marker_counterterms",
            "claim_piece": "no hidden/marker extensions",
            "formal_statement": "No hidden invariant, material marker, domain selector, or readout label extends the source coefficient domain.",
            "status": "HIDDEN_MARKER_EXTENSION_NOT_DERIVED",
            "proof_or_obstruction": "surviving invariant scalars and marker labels can still feed coefficient maps unless a no-extension theorem is signed",
            "source_anchor": "P8_Y5_R10_1114_NO_HIDDEN_VISIBLE_MORPHISM_THEOREM_ATTEMPT.csv:NHV1114_6_verdict; P8_Y5_R10_1092_HIDDEN_INVARIANT_TRIVIALITY_ATTEMPT.csv:HIT1092_5_verdict",
            "conditional_theorem": False,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "CE1904_5_verdict",
            "claim_piece": "promote constructor exhaustion",
            "formal_statement": "Current MTS parent primitives derive a complete constructor list that excludes source-only species weights.",
            "status": "PARENT_ACTION_CONSTRUCTOR_EXHAUSTION_NOT_DERIVED",
            "proof_or_obstruction": "single-action normal form and chain-rule zero are exact conditionally, but parent-generator membership and no-extension/no-marker closure remain unsigned",
            "source_anchor": "CE1904_0_target through CE1904_4_hidden_marker_counterterms",
            "conditional_theorem": True,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def action_scale_owner_rows() -> list[dict[str, Any]]:
    return [
        {
            "owner_id": "ASO1904_0_target",
            "claim_piece": "one action-density line and hbar owner",
            "formal_statement": "Ordinary matter actions are sections of one parent action-density line L_action with one hbar_parent; species labels are field/representation data, not automorphisms of L_action.",
            "status": "TARGET_SHARP",
            "proof_or_obstruction": "this is the clean non-post-hoc route to killing relative source weights",
            "source_anchor": "P8_Y5_R10_1230_ACTION_SCALE_OWNER_THEOREM_ATTEMPT.csv:UAS1230_0_target",
            "conditional_theorem": True,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "owner_id": "ASO1904_1_connected_naturality",
            "claim_piece": "connected matter category common-factor theorem",
            "formal_statement": "If w is a natural positive automorphism of the matter action-density functor over connected C_matter, then w_A=w_* for all ordinary species.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "proof_or_obstruction": "naturality across connected matter morphisms forces one common factor, and 1901 then permits only common calibration",
            "source_anchor": "P8_Y5_R10_1230_ACTION_SCALE_OWNER_THEOREM_ATTEMPT.csv:UAS1230_1_connected_naturality_lemma; P8_Y5_PARENT_QLOC_1901_COMMON_MODE_ABSORPTION_ALGEBRA.csv:ALG1901_3_claim_limit",
            "conditional_theorem": True,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "owner_id": "ASO1904_2_classical_eom_trap",
            "claim_piece": "classical EOM rescaling is not source universality",
            "formal_statement": "delta(w_A S_A)/delta Psi_A=w_A E_A can be divided by w_A, but delta(w_A S_A)/delta g=w_A T_A and J_phi gains partial_phi w_A terms.",
            "status": "FALSE_POSITIVE_REJECTED",
            "proof_or_obstruction": "this confirms the coupling seam is real: matter equations alone cannot certify local-GR source coupling",
            "source_anchor": "P8_Y5_PARENT_QLOC_1694_SOURCE_WEIGHT_VARIATION_IDENTITY.csv:VAR1694_0_matter_EOM;VAR1694_1_Hilbert_source;VAR1694_2_canonical_source",
            "conditional_theorem": False,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "owner_id": "ASO1904_3_measure_current_extension",
            "claim_piece": "measure/current/readout extension",
            "formal_statement": "The same owner must fix path/statistical measure, Hilbert/coframe current normalization, species-blind Jacobians, and readout transfer.",
            "status": "REQUIRED_EXTENSION_NOT_PARENT_SIGNED",
            "proof_or_obstruction": "otherwise J_A, hbar_A, or post-variation current rescaling recreates finite source weights",
            "source_anchor": "P8_Y5_PARENT_QLOC_1888_ACTION_SCALE_OWNER_PROOF_ATTEMPT.csv:ASO1888_5_current_owner; P8_Y5_PARENT_QLOC_1897_ACTION_SCALE_READOUT_STABILITY_ATTEMPT.csv:ASR1897_6_verdict",
            "conditional_theorem": False,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "owner_id": "ASO1904_4_parent_gap",
            "claim_piece": "current corpus signs the action-scale owner",
            "formal_statement": "Current MTS derives connected C_matter, L_action, hbar_parent, species-blind measure descent, and readout stability.",
            "status": "ACTION_SCALE_OWNER_NOT_PARENT_SIGNED",
            "proof_or_obstruction": "1067, 1230, 1888, and 1897 all keep owner/descent/readout premises conditional or unsigned",
            "source_anchor": "P8_Y5_R10_1067_PARENT_ACTION_SCALE_OWNER_ATTEMPT.csv:ASO1067_5_verdict; P8_Y5_PARENT_QLOC_1888_ACTION_SCALE_OWNER_PROOF_ATTEMPT.csv:ASO1888_7_verdict",
            "conditional_theorem": False,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "owner_id": "ASO1904_5_verdict",
            "claim_piece": "promote action-scale owner theorem",
            "formal_statement": "Current MTS parent primitives prove all relative source/action weights are absent or pure common mode.",
            "status": "ACTION_SCALE_OWNER_THEOREM_NOT_DERIVED",
            "proof_or_obstruction": "connected matter category, one action-density line, hbar/measure owner, current owner, and readout descent remain unsigned",
            "source_anchor": "ASO1904_0_target through ASO1904_4_parent_gap",
            "conditional_theorem": True,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def finite_residual_rows() -> list[dict[str, Any]]:
    return [
        {"residual_id": "FR1904_0_common_mode", "object": "w_common", "definition": "universal derivative-silent source/action scale", "current_status": "COMMON_CALIBRATION_ONLY", "required_for_claim": "prove every ordinary sector has only this common factor", "source_anchor": "P8_Y5_PARENT_QLOC_1694_SOURCE_WEIGHT_VARIATION_IDENTITY.csv:VAR1694_3_common_mode", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"residual_id": "FR1904_1_relative_weight", "object": "Delta_w_AB", "definition": "relative source/action weight contrast between ordinary sectors/materials", "current_status": "LIVE_IF_ACTION_OWNER_UNSIGNED", "required_for_claim": "theorem-zero from action owner or source-backed finite bound", "source_anchor": "P8_Y5_PARENT_QLOC_1694_SOURCE_WEIGHT_VARIATION_IDENTITY.csv:VAR1694_4_relative_mode", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"residual_id": "FR1904_2_field_dependence", "object": "beta_w,A", "definition": "hidden/parent-field derivative of source/action weight", "current_status": "LIVE_CANONICAL_SOURCE_LEG", "required_for_claim": "no hidden-visible coefficient morphism or finite residual coefficient", "source_anchor": "P8_Y5_PARENT_QLOC_1694_SOURCE_WEIGHT_VARIATION_IDENTITY.csv:VAR1694_2_canonical_source", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"residual_id": "FR1904_3_measure_jacobian", "object": "J_A or hbar_A", "definition": "species-dependent measure/action-scale/current normalization", "current_status": "LIVE_IF_MEASURE_OWNER_UNSIGNED", "required_for_claim": "species-blind measure/coframe descent theorem", "source_anchor": "P8_Y5_R10_1067_PARENT_ACTION_SCALE_OWNER_ATTEMPT.csv:ASO1067_4_species_blind_measure", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"residual_id": "FR1904_4_readout_transfer", "object": "R_readout source coefficient transfer", "definition": "post-variation or effective/readout map that regenerates source-only coefficients", "current_status": "LIVE_IF_READOUT_UNSIGNED", "required_for_claim": "typed endofunctor/readout no-reentry theorem", "source_anchor": "P8_Y5_PARENT_QLOC_1897_ACTION_SCALE_READOUT_STABILITY_ATTEMPT.csv:ASR1897_3_readout_gap", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"residual_id": "FR1904_5_verdict", "object": "finite source-weight residual branch", "definition": "explicit nonclaim branch retained until constructor exhaustion and action-scale owner close", "current_status": "FINITE_RESIDUAL_BRANCH_RETAINED_NONCLAIM", "required_for_claim": "FR1904_1 through FR1904_4 theorem-zero or source-backed values", "source_anchor": "FR1904_0_common_mode through FR1904_4_readout_transfer", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    return [
        {"case_id": "DRY1904_0_constructor_unsigned", "constructor_exhausted": False, "action_scale_owner": False, "measure_current_owner": False, "readout_stable": False, "uses_eom_division": False, "expected_status": "REFUSED_CONSTRUCTOR_EXHAUSTION_NOT_DERIVED", "valid_for_claim": False},
        {"case_id": "DRY1904_1_action_owner_unsigned", "constructor_exhausted": True, "action_scale_owner": False, "measure_current_owner": False, "readout_stable": False, "uses_eom_division": False, "expected_status": "REFUSED_ACTION_SCALE_OWNER_NOT_DERIVED", "valid_for_claim": False},
        {"case_id": "DRY1904_2_measure_unsigned", "constructor_exhausted": True, "action_scale_owner": True, "measure_current_owner": False, "readout_stable": False, "uses_eom_division": False, "expected_status": "REFUSED_MEASURE_CURRENT_OWNER_UNSIGNED", "valid_for_claim": False},
        {"case_id": "DRY1904_3_readout_unsigned", "constructor_exhausted": True, "action_scale_owner": True, "measure_current_owner": True, "readout_stable": False, "uses_eom_division": False, "expected_status": "REFUSED_READOUT_STABILITY_UNSIGNED", "valid_for_claim": False},
        {"case_id": "DRY1904_4_eom_division", "constructor_exhausted": False, "action_scale_owner": False, "measure_current_owner": False, "readout_stable": False, "uses_eom_division": True, "expected_status": "REFUSED_EOM_DIVISION_FALSE_POSITIVE", "valid_for_claim": False},
    ]


def validate_dryrun_case(row: dict[str, Any]) -> dict[str, Any]:
    if bool_string(row["uses_eom_division"]) == "true":
        status = "REFUSED_EOM_DIVISION_FALSE_POSITIVE"
    elif bool_string(row["constructor_exhausted"]) != "true":
        status = "REFUSED_CONSTRUCTOR_EXHAUSTION_NOT_DERIVED"
    elif bool_string(row["action_scale_owner"]) != "true":
        status = "REFUSED_ACTION_SCALE_OWNER_NOT_DERIVED"
    elif bool_string(row["measure_current_owner"]) != "true":
        status = "REFUSED_MEASURE_CURRENT_OWNER_UNSIGNED"
    elif bool_string(row["readout_stable"]) != "true":
        status = "REFUSED_READOUT_STABILITY_UNSIGNED"
    else:
        status = "WOULD_REQUIRE_FULL_PARENT_SIGNOFF_REVIEW"
    return {
        "case_id": row["case_id"],
        "computed_status": status,
        "expected_status": row["expected_status"],
        "status_match": status == row["expected_status"],
        "claim_allowed": False,
        "valid_for_claim": False,
        "generated_utc": GENERATED_UTC,
    }


def dryrun_result_rows(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [validate_dryrun_case(row) for row in cases]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {"gate_id": "CG1904_0_constructor", "condition": "parent action constructor exhaustion is signed", "current_status": "FAIL_PARENT_ACTION_CONSTRUCTOR_EXHAUSTION_NOT_DERIVED", "source_anchor": "P8_Y5_PARENT_QLOC_1904_PARENT_ACTION_CONSTRUCTOR_EXHAUSTION_ATTEMPT.csv:CE1904_5_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1904_1_action_owner", "condition": "one action-density line/hbar/measure/current owner is signed", "current_status": "FAIL_ACTION_SCALE_OWNER_THEOREM_NOT_DERIVED", "source_anchor": "P8_Y5_PARENT_QLOC_1904_ACTION_SCALE_OWNER_ATTEMPT.csv:ASO1904_5_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1904_2_residual", "condition": "finite source-weight residual branch has sourced values if theorem route fails", "current_status": "FAIL_FINITE_RESIDUAL_BRANCH_RETAINED_NONCLAIM", "source_anchor": "P8_Y5_PARENT_QLOC_1904_FINITE_SOURCE_WEIGHT_RESIDUAL_BRANCH_NONCLAIM.csv:FR1904_5_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1904_3_verdict", "condition": "1904 supports local-GR source universality", "current_status": "CLAIM_BLOCKED", "source_anchor": "CG1904_0_constructor through CG1904_2_residual", "gate_pass": False, "valid_for_claim": False},
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {"decision_id": "DEC1904_0_constructor", "decision": "do not promote constructor exhaustion", "reason": "single-action normal form and chain rule are exact conditionally, but Image(ParentGenerate) membership is not derived", "status": "CONSTRUCTOR_ROUTE_SHARP_BUT_UNSIGNED", "next_dependency": "derive parent generator from motion/time/space primitives", "valid_for_claim": False},
        {"decision_id": "DEC1904_1_action_owner", "decision": "do not promote action-scale owner", "reason": "connected naturality theorem is exact, but connected matter category, action-density line, hbar/measure owner, and readout descent are not parent-signed", "status": "ACTION_OWNER_ROUTE_SHARP_BUT_UNSIGNED", "next_dependency": "derive connected ordinary matter category and one action-density line", "valid_for_claim": False},
        {"decision_id": "DEC1904_2_residual", "decision": "retain finite source-weight residual branch", "reason": "w_A is a real coupling seam unless forbidden by parent grammar; it cannot be divided away using matter EOM", "status": "FINITE_RESIDUAL_BRANCH_RETAINED", "next_dependency": "Delta_w/beta_w/J_A/readout transfer values or theorem-zero proof", "valid_for_claim": False},
        {"decision_id": "DEC1904_3_next", "decision": "attack connected matter category/action-density line next", "reason": "this is the least post-hoc way to close the coupling gap: prove all ordinary species live under one source/action owner", "status": "NEXT_TARGET_SELECTED", "next_dependency": "1905 connected matter category/action-density line or finite Delta_w residual runner", "valid_for_claim": False},
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1904_0_primary",
            "selection_status": "selected",
            "target_doc": "1905-Y5-R2FR-connected-matter-category-action-density-line-or-deltaw-runner.md",
            "target_script": "scripts/Y5_R2FR_connected_matter_category_action_density_line_or_deltaw_runner_1905.py",
            "objective": "try to derive connected ordinary matter category plus one action-density-line owner; if not, emit a finite Delta_w/beta_w/J_A residual runner contract",
            "success_condition": "connected naturality theorem is parent-signed with measure/current/readout descent, or residual branch is executable only as nonclaim",
            "do_not": "do not use classical EOM division as source universality, do not treat the parent normal form as derived, and do not claim WEP/local-GR pass",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {"status_id": "STAT1904_0_result", "area": "coupling gap", "summary": "the coupling problem has reduced to a precise parent-action question: can the parent generator create relative source weights or not?", "risk_level": "CORE_COUPLING_SEAM_EXPOSED", "project_meaning": "this is progress, not failure; the weak point is now named and testable", "next_action": "derive connected matter/action-density owner", "valid_for_claim": False},
        {"status_id": "STAT1904_1_positive", "area": "conditional theorem", "summary": "if constructor exhaustion plus one action-density-line owner is signed, relative source weights collapse to common calibration", "risk_level": "PROMISING_CONDITIONAL_ROUTE", "project_meaning": "the local-GR route is mathematically coherent, but not yet parent-derived", "next_action": "prove parent primitives imply the owner theorem", "valid_for_claim": False},
        {"status_id": "STAT1904_2_fallback", "area": "finite residuals", "summary": "if the owner theorem fails, Delta_w, beta_w, measure Jacobian, and readout transfer remain explicit nonclaim residuals", "risk_level": "FALLBACK_NOT_SCORE_READY", "project_meaning": "no cheating: the source coupling either derives away or stays visible as a residual", "next_action": "build finite residual runner only after theorem attempt stalls", "valid_for_claim": False},
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    cases = dryrun_case_rows()
    return {
        "source_register": source_register_rows(),
        "constructor_exhaustion": constructor_exhaustion_rows(),
        "action_scale_owner": action_scale_owner_rows(),
        "finite_residual": finite_residual_rows(),
        "dryrun_cases": cases,
        "dryrun_results": dryrun_result_rows(cases),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "project_status": project_status_rows(),
    }


def copy_branch_artifacts() -> None:
    for key, target in BRANCH_COPIES.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(OUTPUTS[key], target)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def all_claim_flags_false(paths: list[Path]) -> tuple[bool, str]:
    fields = {"valid_for_claim", "claim_allowed", "valid_prediction_row", "score_ready", "gate_pass", "parent_signed"}
    bad: list[str] = []
    for path in paths:
        for index, row in enumerate(csv_rows(path), start=2):
            for field in fields.intersection(row.keys()):
                if bool_string(row[field]) == "true":
                    bad.append(f"{path.name}:{index}:{field}=true")
    return not bad, "; ".join(bad) if bad else "all generated claim/scoring/signature flags remain false"


def blocked_rows_not_ready(paths: list[Path]) -> tuple[bool, str]:
    markers = ["MISSING", "UNSIGNED", "NOT_DERIVED", "NOT_PARENT", "BLOCKED", "FAIL", "COUNTER", "NONCLAIM", "RETAINED", "REFUSED"]
    fields = {"valid_for_claim", "claim_allowed", "valid_prediction_row", "score_ready", "gate_pass", "parent_signed"}
    bad: list[str] = []
    for path in paths:
        for index, row in enumerate(csv_rows(path), start=2):
            text = " ".join(str(value) for value in row.values())
            if any(marker in text for marker in markers):
                for field in fields.intersection(row.keys()):
                    if bool_string(row[field]) == "true":
                        bad.append(f"{path.name}:{index}:{field}=true despite blocked marker")
    return not bad, "; ".join(bad) if bad else "blocked/unsigned/nonclaim rows are not score-ready"


def csv_parse_check(paths: list[Path]) -> tuple[bool, str]:
    bad: list[str] = []
    for path in paths:
        try:
            rows = csv_rows(path)
            if not rows:
                bad.append(f"{path.name}:empty")
        except Exception as exc:
            bad.append(f"{path.name}:{exc}")
    return not bad, "; ".join(bad) if bad else f"parsed {len(paths)} csv files"


def validation_rows() -> list[dict[str, Any]]:
    generated_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks: list[dict[str, Any]] = []
    source_rows_loaded = csv_rows(OUTPUTS["source_register"])
    checks.append({"validation_id": "VAL1904_00_sources", "status": "PASS" if all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows_loaded) else "FAIL", "detail": "all local source paths exist and needles found", "valid_for_claim": False})
    constructor_rows = csv_rows(OUTPUTS["constructor_exhaustion"])
    checks.append({"validation_id": "VAL1904_01_constructor_verdict", "status": "PASS" if any(row["attempt_id"] == "CE1904_5_verdict" and row["status"] == "PARENT_ACTION_CONSTRUCTOR_EXHAUSTION_NOT_DERIVED" for row in constructor_rows) else "FAIL", "detail": "constructor exhaustion remains unsigned", "valid_for_claim": False})
    owner_rows = csv_rows(OUTPUTS["action_scale_owner"])
    checks.append({"validation_id": "VAL1904_02_owner_verdict", "status": "PASS" if any(row["owner_id"] == "ASO1904_5_verdict" and row["status"] == "ACTION_SCALE_OWNER_THEOREM_NOT_DERIVED" for row in owner_rows) else "FAIL", "detail": "action-scale owner remains unsigned", "valid_for_claim": False})
    residual_rows = csv_rows(OUTPUTS["finite_residual"])
    checks.append({"validation_id": "VAL1904_03_residual_branch", "status": "PASS" if any(row["residual_id"] == "FR1904_5_verdict" and row["current_status"] == "FINITE_RESIDUAL_BRANCH_RETAINED_NONCLAIM" for row in residual_rows) and all(bool_string(row["valid_prediction_row"]) == "false" for row in residual_rows) else "FAIL", "detail": "finite residual branch retained nonclaim", "valid_for_claim": False})
    dry_rows = csv_rows(OUTPUTS["dryrun_results"])
    checks.append({"validation_id": "VAL1904_04_dryrun", "status": "PASS" if all(bool_string(row["status_match"]) == "true" and bool_string(row["claim_allowed"]) == "false" for row in dry_rows) else "FAIL", "detail": "dry-run refuses unsigned constructor/owner/readout and EOM shortcut", "valid_for_claim": False})
    gate_rows = csv_rows(OUTPUTS["claim_gate"])
    checks.append({"validation_id": "VAL1904_05_claim_gate", "status": "PASS" if any(row["gate_id"] == "CG1904_3_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in gate_rows) else "FAIL", "detail": "claim remains blocked", "valid_for_claim": False})
    next_rows = csv_rows(OUTPUTS["next_target"])
    checks.append({"validation_id": "VAL1904_06_next_target", "status": "PASS" if any(row["route_id"] == "NEXT1904_0_primary" and row["selection_status"] == "selected" for row in next_rows) else "FAIL", "detail": "1905 target selected", "valid_for_claim": False})
    flags_ok, flags_detail = all_claim_flags_false(generated_without_validation)
    checks.append({"validation_id": "VAL1904_07_claim_flags_false", "status": "PASS" if flags_ok else "FAIL", "detail": flags_detail, "valid_for_claim": False})
    blocked_ok, blocked_detail = blocked_rows_not_ready(generated_without_validation)
    checks.append({"validation_id": "VAL1904_08_blocked_markers_not_ready", "status": "PASS" if blocked_ok else "FAIL", "detail": blocked_detail, "valid_for_claim": False})
    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append({"validation_id": "VAL1904_09_csv_parse", "status": "PASS" if parse_ok else "FAIL", "detail": parse_detail, "valid_for_claim": False})
    checks.append({"validation_id": "VAL1904_10_branch_copies", "status": "PASS" if all(path.exists() for path in BRANCH_COPIES.values()) else "FAIL", "detail": "; ".join(str(path) for path in BRANCH_COPIES.values()), "valid_for_claim": False})
    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append({"validation_id": "VAL1904_11_pycache_absent", "status": "PASS" if not pycache.exists() else "FAIL", "detail": str(pycache), "valid_for_claim": False})
    formalization_hits = []
    if FORMALIZATION.exists():
        artifact_needles = [
            "1904-Y5-R2FR-parent-action-constructor-exhaustion",
            "P8_Y5_PARENT_QLOC_1904",
            "Y5_R2FR_parent_action_constructor_exhaustion_or_action_scale_owner_1904",
        ]
        formalization_hits = [
            path
            for path in FORMALIZATION.rglob("*")
            if path.is_file() and any(needle in path.name for needle in artifact_needles)
        ]
    checks.append({"validation_id": "VAL1904_12_formalization_untouched", "status": "PASS" if not formalization_hits else "FAIL", "detail": f"formalization_1904_artifact_count={len(formalization_hits)}", "valid_for_claim": False})
    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append({"validation_id": "VAL1904_OVERALL", "status": "PASS" if fail_count == 0 else "FAIL", "detail": "1904 parent action constructor exhaustion or action-scale owner", "valid_for_claim": False})
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 1904 - Parent Action Constructor Exhaustion Or Action-Scale Owner

## Purpose

This checkpoint asks whether relative source weights are impossible because the parent action cannot generate them, or whether they remain finite residual couplings.

## Result

- Constructor exhaustion is exact if all ordinary coefficients lie in the parent-generated image.
- One action-density-line / connected-matter-category owner would force relative source weights to a common calibration mode.
- The current corpus does not parent-sign either route yet.
- Classical EOM division is explicitly rejected: `w_A` can disappear from field equations while remaining in the Hilbert/coframe source.
- The finite `Delta_w`, `beta_w`, measure-Jacobian, and readout-transfer branch remains nonclaim.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Parent Action Constructor Exhaustion

{markdown_table(rows_by_name["constructor_exhaustion"])}

## Action-Scale Owner Attempt

{markdown_table(rows_by_name["action_scale_owner"])}

## Finite Residual Branch

{markdown_table(rows_by_name["finite_residual"])}

## Dry-Run Cases

{markdown_table(rows_by_name["dryrun_cases"])}

## Dry-Run Results

{markdown_table(rows_by_name["dryrun_results"])}

## Claim Gate

{markdown_table(rows_by_name["claim_gate"])}

## Decision Ledger

{markdown_table(rows_by_name["decision"])}

## Next Target

{markdown_table(rows_by_name["next_target"])}

## Project Status Snapshot

{markdown_table(rows_by_name["project_status"])}

## Validation

{markdown_table(validation)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows_by_name = build_rows()
    for key, rows in rows_by_name.items():
        write_csv(OUTPUTS[key], rows)
    copy_branch_artifacts()
    remove_pycache()
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()

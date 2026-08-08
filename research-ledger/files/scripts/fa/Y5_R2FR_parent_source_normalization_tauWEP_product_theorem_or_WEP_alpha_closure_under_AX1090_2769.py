from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_STARTED_UTC = datetime.now(timezone.utc)
ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
WORK = ROOT / "post-checkpoint-work"
MTS = WORK / "source-intake" / "mts_residuals"
RAB_QUEUE = WORK / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = WORK / "source-intake" / "beta-source" / "docs"
MICROSCOPE_DIR = WORK / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SCRIPTS = WORK / "scripts"
FORMALIZATION = ROOT / "formalization-workbench"
DOC = WORK / "2769-Y5-R2FR-parent-source-normalization-tauWEP-product-theorem-or-WEP-alpha-closure-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2769_SOURCE_REGISTER.csv",
    "theorem": MTS / "P8_Y5_R2FR_2769_PARENT_PRODUCT_THEOREM_ATTEMPT.csv",
    "premises": MTS / "P8_Y5_R2FR_2769_PREMISE_SIGNATURE_AUDIT.csv",
    "counterexamples": MTS / "P8_Y5_R2FR_2769_COUNTEREXAMPLE_SURVIVAL_LEDGER.csv",
    "closure": MTS / "P8_Y5_R2FR_2769_WEP_ALPHA_CLOSURE_DEMOTION.csv",
    "prediction": MTS / "P8_Y5_R2FR_2769_ALPHA_PRODUCT_PREDICTION_CLOSURE_ONLY.csv",
    "bounds": MTS / "P8_Y5_R2FR_2769_ALPHA_PRODUCT_BOUND_IMPORT.csv",
    "runner": MTS / "P8_Y5_R2FR_2769_PRODUCT_RUNNER_STATUS.csv",
    "comparisons": MTS / "P8_Y5_R2FR_2769_PRODUCT_COMPARISON_ROWS.csv",
    "gates": MTS / "P8_Y5_R2FR_2769_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2769_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2769_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2769_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2769_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "theorem_queue": RAB_QUEUE / "JR2769_PARENT_WEP_PRODUCT_THEOREM_ATTEMPT_NONCLAIM.csv",
    "closure_queue": RAB_QUEUE / "JR2769_WEP_ALPHA_CLOSURE_ONLY_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "PARENT_WEP_PRODUCT_THEOREM_2769_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "parent_wep_product_theorem_2769_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2769_SOURCE_LABEL_NOETHER_NEXT.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(WORK))
    except ValueError:
        return str(path)


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["valid_for_claim"] = False
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def csv_row_count(path: Path) -> int:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        cells = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def build_sources() -> list[dict[str, Any]]:
    specs = [
        ("SRC2769_00_2768_next", "2768_next", MTS / "P8_Y5_R2FR_2768_NEXT_TARGET.csv", ["NEXT2768_0_2769"], "2768 handoff"),
        ("SRC2769_01_2768_input", "2768_input_ledger", MTS / "P8_Y5_R2FR_2768_INPUT_FILL_LEDGER.csv", ["INF2768_3_beta_source_alpha"], "2768 WEP input debt ledger"),
        ("SRC2769_02_2768_derivation", "2768_derivation", MTS / "P8_Y5_R2FR_2768_BETA_TAU_DERIVATION_ATTEMPT.csv", ["DER2768_0_product_definition"], "2768 product derivation attempt"),
        ("SRC2769_03_2768_prediction", "2768_prediction", MTS / "P8_Y5_R2FR_2768_ALPHA_PRODUCT_PREDICTION_ATTEMPT_NONCLAIM.csv", ["PRED2768_0_WEP_alpha_material_convention_filled"], "2768 nonclaim prediction row"),
        ("SRC2769_04_2768_bound", "2768_bound", MTS / "P8_Y5_R2FR_2768_ALPHA_PRODUCT_BOUND_IMPORT.csv", ["BOUND2768_0_WEP_alpha_screened_product_target"], "2768 WEP alpha product target"),
        ("SRC2769_05_1054_zero_proof", "1054_zero_proof", MTS / "P8_Y5_R10_1054_FORMAL_ZERO_PROOF_ATTEMPT.csv", ["FP1054_4_WEP_consequence"], "conditional zero proof"),
        ("SRC2769_06_1054_clause_audit", "1054_clause_audit", MTS / "P8_Y5_R10_1054_ZERO_THEOREM_CLAUSE_AUDIT.csv", ["ZC1054_5_source_label_forgetting"], "unsigned source label clause"),
        ("SRC2769_07_1055_contract", "1055_contract", MTS / "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv", ["PAC1055_4_source_label_forgetting"], "parent action source-label clause"),
        ("SRC2769_08_1055_adoption", "1055_adoption", MTS / "P8_Y5_R10_1055_CONTRACT_ADOPTION_GATES.csv", ["ADG1055_3_source_label_forgetting"], "source-label adoption gate"),
        ("SRC2769_09_1055_consequence", "1055_consequence", MTS / "P8_Y5_R10_1055_THEOREM_CONSEQUENCES.csv", ["TC1055_2_beta_source_alpha"], "conditional beta_source_alpha zero consequence"),
        ("SRC2769_10_1055_counterexample", "1055_counterexample", MTS / "P8_Y5_R10_1055_COUNTEREXAMPLE_LEDGER.csv", ["CE1055_3_relative_source_weight"], "relative source-weight counterexample"),
        ("SRC2769_11_989_EM_lock", "989_EM_lock", MTS / "P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv", ["ELA989_2_current_owner"], "EM current/source owner audit"),
        ("SRC2769_12_989_parent_input", "989_parent_input", MTS / "P8_Y5_R10_989_PARENT_INPUT_CANDIDATE_LEDGER.csv", ["PIC989_2_Noether_current_owner"], "Noether current owner input"),
        ("SRC2769_13_990_contract", "990_contract", MTS / "P8_Y5_R10_990_PARENT_ACTION_CONTRACT.csv", ["PAC990_3_EM_lock"], "minimal parent action contract"),
        ("SRC2769_14_1044_pullback", "1044_pullback", MTS / "P8_Y5_R10_1044_MATTER_PULLBACK_DERIVATION.csv", ["MPD1044_7_exact_theorem_if_signed"], "matter pullback theorem"),
        ("SRC2769_15_1045_signature", "1045_signature", MTS / "P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv", ["MFS1045_6_verdict"], "matter functor signature audit"),
        ("SRC2769_16_953_source_functor", "953_source_functor", MTS / "P8_Y5_R10_953_SOURCE_FUNCTOR_THEOREM_ATTEMPT.csv", ["NSF953_5_verdict"], "source functor theorem attempt"),
        ("SRC2769_17_955_matter_lemma", "955_matter_lemma", MTS / "P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv", ["MMA955_6_verdict"], "minimal matter action lemma"),
        ("SRC2769_18_980_no_marker", "980_no_marker", MTS / "P8_Y5_R10_980_NO_MARKER_FUNCTOR_THEOREM_ATTEMPT.csv", ["NMF980_7_verdict"], "no-marker obstruction"),
        ("SRC2769_19_1063_precedent", "1063_precedent", WORK / "1063-Y5-R10-source-label-forgetting-Noether-current-owner-or-relative-weight-prior.md", ["THM1063_5_verdict"], "source-label/Noether next precedent"),
    ]
    rows = []
    for row_id, source_key, path, needles, role in specs:
        text = read_text(path)
        exists = path.exists()
        rows.append(nonclaim({
            "row_id": row_id,
            "source_key": source_key,
            "source_path": str(path),
            "exists": exists,
            "needle_spec": ";".join(needles),
            "needles_found": exists and all(needle in text for needle in needles),
            "source_role": role,
        }))
    return rows


def build_theorem_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "THM2769_0_target", "statement": "Target: derive P_WEP_alpha = 0 or a numeric parent product for MICROSCOPE WEP without assigning beta_source_alpha=1 or tau_WEP=1.", "formal_move": "P_WEP_alpha is treated as the observable product tested by eta_AB_alpha = DeltaQ_alpha_AB * P_WEP_alpha in the 2768 material convention.", "current_status": "TARGET_RESTATED", "proof_gap": "needs parent source/current/readout map", "claim_allowed": False}),
        nonclaim({"row_id": "THM2769_1_conditional_pullback_zero", "statement": "If visible EM, matter, source, and readout actions factor through q_loc and fixed representation/topological sectors, then vertical hidden motion cannot change alpha-sensitive source/test accelerations.", "formal_move": "Lie_v c_vis = D c_bar[Dq_loc[v]] = 0 and delta_v S_A = 0 on shell for all ordinary matter species.", "current_status": "EXACT_CONDITIONAL_THEOREM", "proof_gap": "q_loc/matter/current/no-marker clauses are not parent-signed", "claim_allowed": False}),
        nonclaim({"row_id": "THM2769_2_EM_source_owner", "statement": "If the EM generator, Maxwell kinetic coefficient, current normalization, and source/test coupling descend from one parent owner, the alpha-marker beta_source slot is absent.", "formal_move": "T_Q fixed and Lie_v alpha_EM=0; S_int=sum_A n_A int A_Q J_A has no hidden source-normalization coefficient.", "current_status": "BLOCKED_BY_EM_LOCK_UNSIGNED", "proof_gap": "independent f(Xhat)F_Q^2 and current rescaling counterexamples remain legal", "claim_allowed": False}),
        nonclaim({"row_id": "THM2769_3_source_label_forgetting", "statement": "If the parent source functor forgets species labels before coupling selection, relative source weights cannot be formed.", "formal_move": "F_src({T_A}) = kappa_univ sum_A T_A, with kappa_univ absorbed into measured G only after universality is proved.", "current_status": "CONDITIONAL_PROOF_NOT_PARENT_SIGNED", "proof_gap": "species-labelled constant weights w_A or kappa_A remain additive/covariant when labels survive", "claim_allowed": False}),
        nonclaim({"row_id": "THM2769_4_tau_WEP_projection", "statement": "If the same parent local geometry/readout map supplies the WEP differential acceleration, tau_WEP is not an arbitrary arena factor.", "formal_move": "tau_WEP becomes a derived functional of source worldtube, observed coframe, orbit average, and Xhat normalization.", "current_status": "PROJECTION_NOT_DERIVED", "proof_gap": "source worldtube, spacecraft/orbit averaging, material tensor, and observed-force readout are not supplied", "claim_allowed": False}),
        nonclaim({"row_id": "THM2769_5_WEP_product_consequence", "statement": "If either the alpha coefficient derivative or the alpha source marker is theorem-zero, then P_WEP_alpha=0 and the WEP alpha/Coulomb product target is beaten without tuning.", "formal_move": "eta_AB_alpha = DeltaQ_alpha_AB * beta_source_alpha*b_alpha*tau_WEP = 0.", "current_status": "CONDITIONAL_PASS_ONLY", "proof_gap": "zero premise is not signed and no numeric finite product is derived", "claim_allowed": False}),
        nonclaim({"row_id": "THM2769_6_verdict", "statement": "The parent WEP product theorem is mathematically coherent but not proved by the current corpus.", "formal_move": "Preserve it as the exact future action contract; demote current WEP alpha branch to closure-only/nonclaim.", "current_status": "THEOREM_NOT_CLOSED_CURRENT_CORPUS", "proof_gap": "EM owner, source-label forgetting, no-marker/operator classification, tau_WEP projection, and radiative/readout closure remain unsigned", "claim_allowed": False}),
    ]


def build_premise_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "PREM2769_0_q_vertical", "premise": "q_loc exists and WEP-relevant local vertical motion lies in ker(Dq_loc)", "source": "ZC1054_0_quotient_vertical; MFS1045_0_parent_field_quotient", "current_signature": "CONDITIONAL_SUPPORT_NOT_PARENT_COMPLETE", "signed_now": False, "if_signed": "hidden representative motion cannot change observed local geometry", "if_unsigned": "geometry/source leakage can re-enter tau_WEP"}),
        nonclaim({"row_id": "PREM2769_1_EM_owner", "premise": "alpha_EM/gauge kinetic normalization and current normalization are fixed by one parent owner", "source": "PAC1055_1_EM_owner; ELA989_2_current_owner; PAC990_3_EM_lock", "current_signature": "not_signed_unique_F2_counterexample_active", "signed_now": False, "if_signed": "b_alpha=0 or beta_source_alpha alpha-marker absent", "if_unsigned": "f(Xhat)F_Q^2 and source-current rescaling remain legal"}),
        nonclaim({"row_id": "PREM2769_2_matter_pullback", "premise": "ordinary matter descends through observed coframe and fixed representation constants", "source": "MPD1044_7_exact_theorem_if_signed; MFS1045_6_verdict", "current_signature": "exact_conditional_not_parent_signed", "signed_now": False, "if_signed": "ordinary matter has no hidden alpha/mass marker charge", "if_unsigned": "shadow matter frame and material marker counterexamples survive"}),
        nonclaim({"row_id": "PREM2769_3_source_label_forgetting", "premise": "source functor forgets species labels before coupling selection", "source": "NSF953_5_verdict; MMA955_6_verdict; PAC1055_4_source_label_forgetting", "current_signature": "conditional_lemma_not_parent_derivation", "signed_now": False, "if_signed": "relative source weights and beta_source_alpha slots are structurally unavailable", "if_unsigned": "constant species weights remain WEP-sensitive residuals"}),
        nonclaim({"row_id": "PREM2769_4_no_marker_no_mixed_coefficients", "premise": "hidden invariant algebra cannot feed visible continuous coefficients", "source": "ZC1054_3_no_hidden_visible_hom; NMF980_7_verdict; PAC1055_3_no_mixed_coefficients", "current_signature": "obstruction_survives_current_corpus", "signed_now": False, "if_signed": "f_X F^2, m_A(Xhat), and clock/source coefficient maps are forbidden", "if_unsigned": "one nonconstant invariant scalar can feed alpha/source constants"}),
        nonclaim({"row_id": "PREM2769_5_tau_WEP_readout", "premise": "WEP differential acceleration readout is derived from the same source-current/local-geometry map", "source": "DER2768_2_tau_WEP; PR650_1_WEP", "current_signature": "projection_not_derived", "signed_now": False, "if_signed": "tau_WEP becomes a derived product factor rather than an adjustable arena knob", "if_unsigned": "WEP product prediction cannot be scored"}),
        nonclaim({"row_id": "PREM2769_6_radiative_readout_closure", "premise": "effective action, loops, and clock/readout maps preserve quotient and constant-sector ownership", "source": "ZC1054_6_radiative_readout_closure; PAC1055_5_radiative_readout_closure", "current_signature": "unsigned", "signed_now": False, "if_signed": "tree-level zero survives effective reductions", "if_unsigned": "loop/readout-induced alpha/source terms can regenerate the coupling"}),
    ]


def build_counterexample_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "CE2769_0_gauge_kinetic_function", "surviving_term": "f(Xhat) F_Q^2", "why_survives": "gauge and diffeomorphism invariance allow scalar gauge kinetic functions unless the parent operator domain forbids them", "blocks": "b_alpha=0 and EM-lock alpha zero", "source": "CE1055_0_gauge_kinetic_function; PREM2769_1_EM_owner"}),
        nonclaim({"row_id": "CE2769_1_relative_source_weight", "surviving_term": "S_matter=sum_A w_A S_A or F((T_A,A))=kappa_A T_A", "why_survives": "constant species weights preserve covariance and additivity when species labels remain available", "blocks": "source-label forgetting and WEP source normalization", "source": "CE1055_3_relative_source_weight; NSF953_3_additivity_limit; MMA955_3_relative_prefactor"}),
        nonclaim({"row_id": "CE2769_2_hidden_invariant_marker", "surviving_term": "c(I_hid) O_vis", "why_survives": "one nonconstant invariant scalar can feed continuous visible coefficient spaces", "blocks": "no-marker/no-mixed-coefficient theorem", "source": "NMF980_2_scalar_obstruction_lemma; CE1055_1_hidden_invariant_scalar"}),
        nonclaim({"row_id": "CE2769_3_shadow_matter_frame", "surviving_term": "A_A(Xhat)^2 g_obs or m_A(Xhat) psi_bar psi", "why_survives": "ordinary covariance alone does not forbid hidden matter frames or mass maps", "blocks": "matter pullback zero and material beta zero", "source": "CE1055_2_shadow_matter_frame; MFS1045_4_no_shadow_frame"}),
        nonclaim({"row_id": "CE2769_4_readout_regeneration", "surviving_term": "loop/readout-induced f_X F^2 or clock_Xhat map", "why_survives": "bare action sequestering is not automatically stable under effective reductions", "blocks": "radiative/readout closure", "source": "CE1055_4_readout_regeneration; ZC1054_6_radiative_readout_closure"}),
    ]


def build_closure_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "CLOS2769_0_WEP_alpha_route_status", "route": "MICROSCOPE WEP alpha/Coulomb product route", "status": "closure_only_nonclaim", "reason": "conditional zero theorem is exact but parent premises are unsigned and numeric product is missing", "what_is_preserved": "material convention, product target, and theorem contract", "what_is_forbidden": "WEP pass, beta_source_alpha=1, tau_WEP=1, standalone b_alpha claim, public local-GR claim"}),
        nonclaim({"row_id": "CLOS2769_1_future_promotion_condition", "route": "promotion out of closure", "status": "requires_parent_signature_or_numeric_product", "reason": "either sign the parent product-zero theorem or supply a sourced numeric P_WEP_alpha below 4.797780522732e-05", "what_is_preserved": "single product scoring rule", "what_is_forbidden": "moving factors between beta_source_alpha, b_alpha, and tau_WEP after seeing the bound"}),
    ]


def build_prediction_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"prediction_id": "PRED2769_0_WEP_alpha_closure_zero_not_parent_derived", "arena": "MICROSCOPE_WEP", "product_symbol": "P_WEP_alpha", "product_value": "CLOSURE_ZERO_NOT_PARENT_DERIVED", "product_units": "dimensionless", "inputs_present": "conditional theorem clauses only", "required_inputs": "parent-signed product-zero theorem OR sourced numeric P_WEP_alpha", "derivation_status": "THEOREM_NOT_CLOSED_CURRENT_CORPUS", "comparison_allowed": False, "claim_allowed": False})
    ]


def build_bound_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"bound_id": "BOUND2769_0_WEP_alpha_screened_product_target", "arena": "MICROSCOPE_WEP", "product_symbol": "P_WEP_alpha", "bound_value": "4.797780522732e-05", "bound_units": "dimensionless", "bound_type": "screened_smoke_product_target_nonclaim"})
    ]


def is_numeric(value: Any) -> bool:
    try:
        float(str(value))
    except (TypeError, ValueError):
        return False
    return True


def has_missing_marker(row: dict[str, Any]) -> bool:
    text = " ".join(str(value) for value in row.values())
    return "MISSING" in text or "NOT_PARENT_DERIVED" in text


def run_product_runner(predictions: list[dict[str, Any]], bounds: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    valid_predictions = [
        row for row in predictions
        if row.get("comparison_allowed") is True
        and row.get("claim_allowed") is True
        and row.get("valid_for_claim") is True
        and is_numeric(row.get("product_value"))
        and not has_missing_marker(row)
    ]
    valid_bounds = [
        row for row in bounds
        if is_numeric(row.get("bound_value"))
        and float(str(row.get("bound_value"))) > 0.0
        and not has_missing_marker(row)
    ]
    comparisons = [nonclaim({
        "comparison_id": "PRODUCT_COMPARE_NO_VALID_PREDICTIONS",
        "arena": "",
        "product_symbol": "",
        "product_value": "",
        "bound_value": "",
        "comparison_status": "not_run",
        "pass_for_claim": False,
        "issues": "no valid MTS alpha product prediction rows",
    })] if not valid_predictions else []
    runner = [nonclaim({
        "runner_id": "APR2769_0_WEP_alpha_closure_product_runner",
        "prediction_rows": len(predictions),
        "bound_rows": len(bounds),
        "valid_prediction_rows": len(valid_predictions),
        "valid_bound_rows": len(valid_bounds),
        "comparison_rows": len(comparisons),
        "claim_allowed": False,
        "expected_result": "reject_closure_zero_as_nonclaim",
    })]
    return runner, comparisons


def build_gates() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "CG2769_0_parent_product_theorem", "claim": "parent action proves P_WEP_alpha=0", "gate_pass": False, "reason": "the theorem is exact only if unsigned EM/matter/source/readout premises are signed", "claim_allowed": False}),
        nonclaim({"row_id": "CG2769_1_numeric_WEP_product", "claim": "MTS has a numeric WEP alpha product prediction", "gate_pass": False, "reason": "closure zero is nonnumeric and runner valid_prediction_rows remain zero", "claim_allowed": False}),
        nonclaim({"row_id": "CG2769_2_WEP_pass", "claim": "MTS passes MICROSCOPE WEP alpha branch", "gate_pass": False, "reason": "product target exists, but no parent-derived product or theorem-zero exists", "claim_allowed": False}),
        nonclaim({"row_id": "CG2769_3_local_GR", "claim": "local GR/Newton follows", "gate_pass": False, "reason": "WEP alpha closure does not close EH/Newton/PPN/source normalization", "claim_allowed": False}),
    ]


def build_decision() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "DEC2769_0_theorem_shape", "decision": "parent WEP product theorem shape is retained", "because": "if the parent action signs the EM/matter/source/readout clauses, P_WEP_alpha=0 follows without tuning", "next_action": "use this as the exact contract for future parent action work"}),
        nonclaim({"row_id": "DEC2769_1_current_status", "decision": "current WEP alpha route is closure-only", "because": "surviving counterexamples are legal and tau_WEP/readout is not derived", "next_action": "do not score the WEP alpha branch yet"}),
        nonclaim({"row_id": "DEC2769_2_best_next", "decision": "attack source-label forgetting and Noether current owner directly", "because": "relative source weights are the cleanest live counterexample for WEP/source normalization", "next_action": "2770-Y5-R2FR-source-label-forgetting-Noether-current-owner-or-relative-weight-prior-under-AX1090.md"}),
    ]


def build_next() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "row_id": "NEXT2769_0_2770",
            "next_target": "2770-Y5-R2FR-source-label-forgetting-Noether-current-owner-or-relative-weight-prior-under-AX1090.md",
            "script": "scripts/Y5_R2FR_source_label_forgetting_Noether_current_owner_or_relative_weight_prior_under_AX1090_2770.py",
            "why": "the parent WEP product theorem is exact but unsigned; the live obstruction is relative source weights and an unsigned Noether/current source owner",
            "include": "source functor domain, same-action Hilbert source, relative w_A counterexample, Noether current owner, measured-G common-mode absorption, WEP/PPN/R10 product templates",
            "exclude": "assuming WEP, hiding relative weights in measured G, unity shortcuts, public local-GR/WEP/R10 claim, GitHub action, formalization-workbench edits",
        })
    ]


def copy_branch_outputs(
    theorem: list[dict[str, Any]],
    premises: list[dict[str, Any]],
    counterexamples: list[dict[str, Any]],
    closure: list[dict[str, Any]],
    prediction: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    theorem_rows = theorem + premises + counterexamples
    closure_rows = closure + prediction + gates
    beta_rows = theorem + premises + closure + next_rows
    microscope_rows = theorem + closure + prediction + gates + next_rows
    specs = [
        ("BR2769_0_theorem_queue", "theorem", theorem_rows, OUTPUTS["theorem"], BRANCH_OUTPUTS["theorem_queue"], "parent WEP product theorem attempt"),
        ("BR2769_1_closure_queue", "closure", closure_rows, OUTPUTS["closure"], BRANCH_OUTPUTS["closure_queue"], "WEP alpha closure-only demotion"),
        ("BR2769_2_beta_doc", "beta_doc", beta_rows, OUTPUTS["premises"], BRANCH_OUTPUTS["beta_doc"], "beta/source-facing parent WEP product copy"),
        ("BR2769_3_microscope_copy", "microscope", microscope_rows, OUTPUTS["prediction"], BRANCH_OUTPUTS["microscope_copy"], "MICROSCOPE WEP closure copy"),
        ("BR2769_4_next_queue", "next", next_rows, OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "source-label/Noether next target"),
    ]
    rows = []
    for copy_id, table_key, source_rows, source_table, copy_path, purpose in specs:
        write_csv(copy_path, source_rows)
        rows.append(nonclaim({
            "copy_id": copy_id,
            "table_key": table_key,
            "source_table": rel(source_table),
            "copy_path": rel(copy_path),
            "purpose": purpose,
            "exists": copy_path.exists(),
            "row_count": csv_row_count(copy_path) if copy_path.exists() else 0,
        }))
    return rows


def generated_files_under_work() -> bool:
    generated = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
    return all(WORK in path.parents or path == WORK for path in generated)


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and path.stat().st_mtime > RUN_STARTED_UTC.timestamp():
            return False
    return True


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if str(row.get("valid_for_claim", "False")).lower() == "true":
                return False
            if str(row.get("claim_allowed", "False")).lower() == "true":
                return False
            if str(row.get("allowed", "False")).lower() == "true":
                return False
            if str(row.get("pass_for_claim", "False")).lower() == "true":
                return False
    return True


def remove_pycache() -> None:
    pycache = SCRIPTS / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def build_validation(rows_by_name: dict[str, list[dict[str, Any]]], csv_paths: list[Path]) -> list[dict[str, Any]]:
    sources = rows_by_name["sources"]
    theorem = rows_by_name["theorem"]
    premises = rows_by_name["premises"]
    counterexamples = rows_by_name["counterexamples"]
    closure = rows_by_name["closure"]
    prediction = rows_by_name["prediction"]
    runner = rows_by_name["runner"]
    comparisons = rows_by_name["comparisons"]
    gates = rows_by_name["gates"]
    next_rows = rows_by_name["next"]
    branches = rows_by_name["branches"]
    checks = [
        ("VAL2769_0_sources", all(row["exists"] and row["needles_found"] for row in sources), "every cited source path exists and needles are found"),
        ("VAL2769_1_theorem_verdict_written", any(row["row_id"] == "THM2769_6_verdict" and row["current_status"] == "THEOREM_NOT_CLOSED_CURRENT_CORPUS" for row in theorem), "conditional theorem is written and not promoted"),
        ("VAL2769_2_premises_unsigned", all(row["signed_now"] is False for row in premises), "all required theorem premises remain unsigned"),
        ("VAL2769_3_counterexamples_recorded", len(counterexamples) >= 5 and any(row["row_id"] == "CE2769_1_relative_source_weight" for row in counterexamples), "surviving counterexamples are recorded"),
        ("VAL2769_4_closure_demotion_written", any(row["row_id"] == "CLOS2769_0_WEP_alpha_route_status" and row["status"] == "closure_only_nonclaim" for row in closure), "WEP alpha route demoted to closure-only/nonclaim"),
        ("VAL2769_5_closure_prediction_nonnumeric", prediction[0]["product_value"] == "CLOSURE_ZERO_NOT_PARENT_DERIVED" and prediction[0]["comparison_allowed"] is False, "closure zero is nonnumeric and cannot be scored"),
        ("VAL2769_6_product_runner_refuses_closure", runner[0]["valid_prediction_rows"] == 0 and comparisons[0]["comparison_status"] == "not_run", "product runner refuses closure-only zero"),
        ("VAL2769_7_claim_gates_blocked", all(row["gate_pass"] is False and row["claim_allowed"] is False for row in gates), "all claim gates remain blocked"),
        ("VAL2769_8_next_target_written", any(row["row_id"] == "NEXT2769_0_2770" and "source-label-forgetting" in row["next_target"] for row in next_rows), "next target selects source-label forgetting and Noether current owner"),
        ("VAL2769_9_branch_outputs", all(row["exists"] and int(row["row_count"]) > 0 for row in branches), "branch copies exist and contain rows"),
        ("VAL2769_10_csv_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2769_11_no_claim_flags", no_claim_flags(rows_by_name), "no generated row is valid_for_claim=true/claim_allowed=true/allowed=true/pass_for_claim=true"),
        ("VAL2769_12_generated_under_post_checkpoint", generated_files_under_work(), "all generated outputs are under post-checkpoint-work"),
        ("VAL2769_13_formalization_untouched", formalization_untouched(), "formalization-workbench modified-file count remains zero during this run"),
        ("VAL2769_14_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    rows = [{"validation_id": check_id, "passed": passed, "detail": detail, "timestamp_utc": ts()} for check_id, passed, detail in checks]
    rows.append({
        "validation_id": "VAL2769_OVERALL",
        "passed": all(row["passed"] for row in rows),
        "detail": "2769 writes the combined parent WEP product theorem in the current R2/f(R) branch, keeps it conditional because EM owner, matter/source functor, source-label forgetting, tau_WEP, and radiative/readout closure are unsigned, demotes WEP alpha to closure-only/nonclaim, verifies the runner refuses the closure-zero row, and selects source-label forgetting/Noether current owner as the next target.",
        "timestamp_utc": ts(),
    })
    return rows


def build_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> str:
    return "\n\n".join([
        "# 2769 - Y5 R2/f(R): Parent Source-Normalization tau_WEP Product Theorem Or WEP Alpha Closure Under AX1090",
        "## Private Verdict\n\nThe direct theorem has the right shape, but it is not signed by the present corpus. `P_WEP_alpha=0` remains a conditional parent-action theorem, not a live result.\n\nHard demotion: the WEP alpha/Coulomb route is closure-only/nonclaim until either the parent product-zero theorem is signed or a sourced numeric `P_WEP_alpha` is supplied.",
        "## Source Register\n\n" + markdown_table(rows_by_name["sources"], ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"]),
        "## Parent Product Theorem Attempt\n\n" + markdown_table(rows_by_name["theorem"], ["row_id", "statement", "formal_move", "current_status", "proof_gap", "claim_allowed", "valid_for_claim"]),
        "## Premise Signature Audit\n\n" + markdown_table(rows_by_name["premises"], ["row_id", "premise", "source", "current_signature", "signed_now", "if_signed", "if_unsigned", "valid_for_claim"]),
        "## Counterexample Survival Ledger\n\n" + markdown_table(rows_by_name["counterexamples"], ["row_id", "surviving_term", "why_survives", "blocks", "source", "valid_for_claim"]),
        "## Closure Demotion\n\n" + markdown_table(rows_by_name["closure"], ["row_id", "route", "status", "reason", "what_is_preserved", "what_is_forbidden", "valid_for_claim"]),
        "## Closure Prediction Row\n\n" + markdown_table(rows_by_name["prediction"], ["prediction_id", "arena", "product_symbol", "product_value", "product_units", "inputs_present", "required_inputs", "derivation_status", "comparison_allowed", "claim_allowed", "valid_for_claim"]),
        "## Bound Import\n\n" + markdown_table(rows_by_name["bounds"], ["bound_id", "arena", "product_symbol", "bound_value", "bound_units", "bound_type", "valid_for_claim"]),
        "## Product Runner Status\n\n" + markdown_table(rows_by_name["runner"], ["runner_id", "prediction_rows", "bound_rows", "valid_prediction_rows", "valid_bound_rows", "comparison_rows", "claim_allowed", "expected_result", "valid_for_claim"]),
        "## Product Comparison Rows\n\n" + markdown_table(rows_by_name["comparisons"], ["comparison_id", "arena", "product_symbol", "product_value", "bound_value", "comparison_status", "pass_for_claim", "issues", "valid_for_claim"]),
        "## Claim Gates\n\n" + markdown_table(rows_by_name["gates"], ["row_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
        "## Decision Ledger\n\n" + markdown_table(rows_by_name["decision"], ["row_id", "decision", "because", "next_action", "valid_for_claim"]),
        "## Next Target\n\n" + markdown_table(rows_by_name["next"], ["row_id", "next_target", "script", "why", "include", "exclude", "valid_for_claim"]),
        "## Branch Copies\n\n" + markdown_table(rows_by_name["branches"], ["copy_id", "table_key", "source_table", "copy_path", "purpose", "exists", "row_count", "valid_for_claim"]),
        "## Validation\n\n" + markdown_table(rows_by_name["validation"], ["validation_id", "passed", "detail", "timestamp_utc"]),
        "## Plain-English Read\n\nThis is the cleanest version of the WEP coupling gate: either the parent action removes the alpha/source product structurally, or WEP alpha stays closure-only. The next thing to hunt is source-label forgetting and the Noether current owner, because that is where relative source weights still sneak through the ropes.",
        "",
    ])


def main() -> None:
    ensure_dirs()
    sources = build_sources()
    theorem = build_theorem_rows()
    premises = build_premise_rows()
    counterexamples = build_counterexample_rows()
    closure = build_closure_rows()
    prediction = build_prediction_rows()
    bounds = build_bound_rows()
    runner, comparisons = run_product_runner(prediction, bounds)
    gates = build_gates()
    decision = build_decision()
    next_rows = build_next()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["premises"], premises)
    write_csv(OUTPUTS["counterexamples"], counterexamples)
    write_csv(OUTPUTS["closure"], closure)
    write_csv(OUTPUTS["prediction"], prediction)
    write_csv(OUTPUTS["bounds"], bounds)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["comparisons"], comparisons)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decision"], decision)
    write_csv(OUTPUTS["next"], next_rows)

    branches = copy_branch_outputs(theorem, premises, counterexamples, closure, prediction, gates, next_rows)
    write_csv(OUTPUTS["branches"], branches)
    remove_pycache()

    rows_by_name = {
        "sources": sources,
        "theorem": theorem,
        "premises": premises,
        "counterexamples": counterexamples,
        "closure": closure,
        "prediction": prediction,
        "bounds": bounds,
        "runner": runner,
        "comparisons": comparisons,
        "gates": gates,
        "decision": decision,
        "next": next_rows,
        "branches": branches,
    }
    csv_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    validation = build_validation(rows_by_name, csv_paths)
    rows_by_name["validation"] = validation
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(build_doc(rows_by_name), encoding="utf-8")
    remove_pycache()

    overall = next(row for row in validation if row["validation_id"] == "VAL2769_OVERALL")
    print(f"2769 complete: overall={overall['passed']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

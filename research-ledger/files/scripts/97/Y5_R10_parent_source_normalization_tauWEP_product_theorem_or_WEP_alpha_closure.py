from __future__ import annotations

import csv
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from Y5_R10_alpha_product_prediction_stub_runner_and_required_inputs import (
    BOUND_REQUIRED_COLUMNS,
    PRODUCT_REQUIRED_COLUMNS,
    run_product_runner,
)


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1062-Y5-R10-parent-source-normalization-tauWEP-product-theorem-or-WEP-alpha-closure.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1062-parent-source-normalization-tauWEP-product-theorem" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_CLOSURE = OUT / "P8_Y5_R10_1062_ALPHA_PRODUCT_PREDICTION_CLOSURE_ONLY.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1062_ALPHA_PRODUCT_BOUND_IMPORT.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |" for row in rows],
        ]
    ) + "\n"


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1062_0_1061_next", "source-intake/mts_residuals/P8_Y5_R10_1061_NEXT_TARGET.csv", "1062-Y5-R10-parent-source-normalization-tauWEP-product-theorem", "1061 handoff."),
        ("SRC1062_1_1061_input", "source-intake/mts_residuals/P8_Y5_R10_1061_INPUT_FILL_LEDGER.csv", "INF1061_3_beta_source_alpha", "1061 WEP input debt ledger."),
        ("SRC1062_2_1061_derivation", "source-intake/mts_residuals/P8_Y5_R10_1061_BETA_TAU_DERIVATION_ATTEMPT.csv", "DER1061_0_product_definition", "1061 product derivation attempt."),
        ("SRC1062_3_1061_prediction", "source-intake/mts_residuals/P8_Y5_R10_1061_ALPHA_PRODUCT_PREDICTION_ATTEMPT_NONCLAIM.csv", "PRED1061_0_WEP_alpha_material_convention_filled", "1061 nonclaim product prediction row."),
        ("SRC1062_4_1061_bound", "source-intake/mts_residuals/P8_Y5_R10_1061_ALPHA_PRODUCT_BOUND_IMPORT.csv", "BOUND1061_0_WEP_alpha_screened_product_target", "1061 WEP alpha product target."),
        ("SRC1062_5_1054_zero_proof", "source-intake/mts_residuals/P8_Y5_R10_1054_FORMAL_ZERO_PROOF_ATTEMPT.csv", "FP1054_4_WEP_consequence", "conditional zero proof."),
        ("SRC1062_6_1054_clause_audit", "source-intake/mts_residuals/P8_Y5_R10_1054_ZERO_THEOREM_CLAUSE_AUDIT.csv", "ZC1054_5_source_label_forgetting", "unsigned source label clause."),
        ("SRC1062_7_1055_contract", "source-intake/mts_residuals/P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv", "PAC1055_4_source_label_forgetting", "parent action source-label clause."),
        ("SRC1062_8_1055_adoption", "source-intake/mts_residuals/P8_Y5_R10_1055_CONTRACT_ADOPTION_GATES.csv", "ADG1055_3_source_label_forgetting", "source-label adoption gate."),
        ("SRC1062_9_1055_consequence", "source-intake/mts_residuals/P8_Y5_R10_1055_THEOREM_CONSEQUENCES.csv", "TC1055_2_beta_source_alpha", "conditional beta_source_alpha zero consequence."),
        ("SRC1062_10_1055_counterexample", "source-intake/mts_residuals/P8_Y5_R10_1055_COUNTEREXAMPLE_LEDGER.csv", "CE1055_3_relative_source_weight", "relative source-weight counterexample."),
        ("SRC1062_11_989_EM_lock", "source-intake/mts_residuals/P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv", "ELA989_2_current_owner", "EM current/source owner audit."),
        ("SRC1062_12_989_parent_input", "source-intake/mts_residuals/P8_Y5_R10_989_PARENT_INPUT_CANDIDATE_LEDGER.csv", "PIC989_2_Noether_current_owner", "Noether current owner input."),
        ("SRC1062_13_990_contract", "source-intake/mts_residuals/P8_Y5_R10_990_PARENT_ACTION_CONTRACT.csv", "PAC990_3_EM_lock", "minimal parent action contract."),
        ("SRC1062_14_1044_pullback", "source-intake/mts_residuals/P8_Y5_R10_1044_MATTER_PULLBACK_DERIVATION.csv", "MPD1044_7_exact_theorem_if_signed", "matter pullback theorem."),
        ("SRC1062_15_1045_signature", "source-intake/mts_residuals/P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv", "MFS1045_6_verdict", "matter functor signature audit."),
        ("SRC1062_16_953_source_functor", "source-intake/mts_residuals/P8_Y5_R10_953_SOURCE_FUNCTOR_THEOREM_ATTEMPT.csv", "NSF953_5_verdict", "source functor theorem attempt."),
        ("SRC1062_17_955_matter_lemma", "source-intake/mts_residuals/P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv", "MMA955_6_verdict", "minimal matter action lemma."),
        ("SRC1062_18_980_no_marker", "source-intake/mts_residuals/P8_Y5_R10_980_NO_MARKER_FUNCTOR_THEOREM_ATTEMPT.csv", "NMF980_7_verdict", "no-marker obstruction."),
    ]
    rows: list[dict[str, str]] = []
    for source_id, rel_path, needle, note in specs:
        path = source_path(rel_path)
        exists = path.exists()
        needle_found = exists and needle in read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "relative_path": rel_path,
                "absolute_path": str(path),
                "exists": str(exists).lower(),
                "needle": needle,
                "needle_found": str(needle_found).lower(),
                "note": note,
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def theorem_attempt_rows() -> list[dict[str, str]]:
    return [
        {
            "theorem_step": "THM1062_0_target",
            "statement": "Target: derive P_WEP_alpha = 0 or a numeric parent product for MICROSCOPE WEP without assigning beta_source_alpha=1 or tau_WEP=1.",
            "formal_move": "P_WEP_alpha is treated as the observable product tested by eta_AB_alpha = DeltaQ_alpha_AB * P_WEP_alpha in the 1061 material convention.",
            "current_status": "TARGET_RESTATED",
            "proof_gap": "needs parent source/current/readout map",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_step": "THM1062_1_conditional_pullback_zero",
            "statement": "If visible EM, matter, source, and readout actions factor through q_loc and fixed representation/topological sectors, then vertical hidden motion cannot change alpha-sensitive source/test accelerations.",
            "formal_move": "Lie_v c_vis = D c_bar[Dq_loc[v]] = 0 and delta_v S_A = 0 on shell for all ordinary matter species.",
            "current_status": "EXACT_CONDITIONAL_THEOREM",
            "proof_gap": "q_loc/matter/current/no-marker clauses are not parent-signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_step": "THM1062_2_EM_source_owner",
            "statement": "If the EM generator, Maxwell kinetic coefficient, current normalization, and source/test coupling descend from one parent owner, the alpha-marker beta_source slot is absent.",
            "formal_move": "T_Q fixed and Lie_v alpha_EM=0; S_int=sum_A n_A int A_Q J_A has no hidden source-normalization coefficient.",
            "current_status": "BLOCKED_BY_EM_LOCK_UNSIGNED",
            "proof_gap": "independent f(Xhat)F_Q^2 and current rescaling counterexamples remain legal",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_step": "THM1062_3_source_label_forgetting",
            "statement": "If the parent source functor forgets species labels before coupling selection, relative source weights cannot be formed.",
            "formal_move": "F_src({T_A}) = kappa_univ sum_A T_A, with kappa_univ absorbed into measured G only after universality is proved.",
            "current_status": "CONDITIONAL_PROOF_NOT_PARENT_SIGNED",
            "proof_gap": "species-labelled constant weights w_A or kappa_A remain additive/covariant when labels survive",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_step": "THM1062_4_tau_WEP_projection",
            "statement": "If the same parent local geometry/readout map supplies the WEP differential acceleration, tau_WEP is not an arbitrary arena factor.",
            "formal_move": "tau_WEP becomes a derived functional of source worldtube, observed coframe, orbit average, and Xhat normalization.",
            "current_status": "PROJECTION_NOT_DERIVED",
            "proof_gap": "source worldtube, spacecraft/orbit averaging, material tensor, and observed-force readout are not supplied",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_step": "THM1062_5_WEP_product_consequence",
            "statement": "If either the alpha coefficient derivative or the alpha source marker is theorem-zero, then P_WEP_alpha=0 and the WEP alpha/Coulomb product target is beaten without tuning.",
            "formal_move": "eta_AB_alpha = DeltaQ_alpha_AB * beta_source_alpha*b_alpha*tau_WEP = 0.",
            "current_status": "CONDITIONAL_PASS_ONLY",
            "proof_gap": "zero premise is not signed and no numeric finite product is derived",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_step": "THM1062_6_verdict",
            "statement": "The parent WEP product theorem is mathematically coherent but not proved by the current corpus.",
            "formal_move": "Preserve it as the exact future action contract; demote current WEP alpha branch to closure-only/nonclaim.",
            "current_status": "THEOREM_NOT_CLOSED_CURRENT_CORPUS",
            "proof_gap": "EM owner, source-label forgetting, no-marker/operator classification, tau_WEP projection, and radiative/readout closure remain unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def premise_audit_rows() -> list[dict[str, str]]:
    return [
        {
            "premise_id": "PREM1062_0_q_vertical",
            "premise": "q_loc exists and WEP-relevant local vertical motion lies in ker(Dq_loc)",
            "source": "ZC1054_0_quotient_vertical; MFS1045_0_parent_field_quotient",
            "current_signature": "CONDITIONAL_SUPPORT_NOT_PARENT_COMPLETE",
            "signed_now": "false",
            "if_signed": "hidden representative motion cannot change observed local geometry",
            "if_unsigned": "geometry/source leakage can re-enter tau_WEP",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "premise_id": "PREM1062_1_EM_owner",
            "premise": "alpha_EM/gauge kinetic normalization and current normalization are fixed by one parent owner",
            "source": "PAC1055_1_EM_owner; ELA989_2_current_owner; PAC990_3_EM_lock",
            "current_signature": "not_signed_unique_F2_counterexample_active",
            "signed_now": "false",
            "if_signed": "b_alpha=0 or beta_source_alpha alpha-marker absent",
            "if_unsigned": "f(Xhat)F_Q^2 and source-current rescaling remain legal",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "premise_id": "PREM1062_2_matter_pullback",
            "premise": "ordinary matter descends through observed coframe and fixed representation constants",
            "source": "MPD1044_7_exact_theorem_if_signed; MFS1045_6_verdict",
            "current_signature": "exact_conditional_not_parent_signed",
            "signed_now": "false",
            "if_signed": "ordinary matter has no hidden alpha/mass marker charge",
            "if_unsigned": "shadow matter frame and material marker counterexamples survive",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "premise_id": "PREM1062_3_source_label_forgetting",
            "premise": "source functor forgets species labels before coupling selection",
            "source": "NSF953_5_verdict; MMA955_6_verdict; PAC1055_4_source_label_forgetting",
            "current_signature": "conditional_lemma_not_parent_derivation",
            "signed_now": "false",
            "if_signed": "relative source weights and beta_source_alpha slots are structurally unavailable",
            "if_unsigned": "constant species weights remain WEP-sensitive residuals",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "premise_id": "PREM1062_4_no_marker_no_mixed_coefficients",
            "premise": "hidden invariant algebra cannot feed visible continuous coefficients",
            "source": "ZC1054_3_no_hidden_visible_hom; NMF980_7_verdict; PAC1055_3_no_mixed_coefficients",
            "current_signature": "obstruction_survives_current_corpus",
            "signed_now": "false",
            "if_signed": "f_X F^2, m_A(Xhat), and clock/source coefficient maps are forbidden",
            "if_unsigned": "one nonconstant invariant scalar can feed alpha/source constants",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "premise_id": "PREM1062_5_tau_WEP_readout",
            "premise": "WEP differential acceleration readout is derived from the same source-current/local-geometry map",
            "source": "DER1061_2_tau_WEP; PR650_1_WEP",
            "current_signature": "projection_not_derived",
            "signed_now": "false",
            "if_signed": "tau_WEP becomes a derived product factor rather than an adjustable arena knob",
            "if_unsigned": "WEP product prediction cannot be scored",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "premise_id": "PREM1062_6_radiative_readout_closure",
            "premise": "effective action, loops, and clock/readout maps preserve quotient and constant-sector ownership",
            "source": "ZC1054_6_radiative_readout_closure; PAC1055_5_radiative_readout_closure",
            "current_signature": "unsigned",
            "signed_now": "false",
            "if_signed": "tree-level zero survives effective reductions",
            "if_unsigned": "loop/readout-induced alpha/source terms can regenerate the coupling",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def counterexample_rows() -> list[dict[str, str]]:
    return [
        {
            "counterexample_id": "CE1062_0_gauge_kinetic_function",
            "surviving_term": "f(Xhat) F_Q^2",
            "why_survives": "gauge and diffeomorphism invariance allow scalar gauge kinetic functions unless the parent operator domain forbids them",
            "blocks": "b_alpha=0 and EM-lock alpha zero",
            "source": "CE1055_0_gauge_kinetic_function; PREM1062_1_EM_owner",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "counterexample_id": "CE1062_1_relative_source_weight",
            "surviving_term": "S_matter=sum_A w_A S_A or F((T_A,A))=kappa_A T_A",
            "why_survives": "constant species weights preserve covariance and additivity when species labels remain available",
            "blocks": "source-label forgetting and WEP source normalization",
            "source": "CE1055_3_relative_source_weight; NSF953_3_additivity_limit; MMA955_3_relative_prefactor",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "counterexample_id": "CE1062_2_hidden_invariant_marker",
            "surviving_term": "c(I_hid) O_vis",
            "why_survives": "one nonconstant invariant scalar can feed continuous visible coefficient spaces",
            "blocks": "no-marker/no-mixed-coefficient theorem",
            "source": "NMF980_2_scalar_obstruction_lemma; CE1055_1_hidden_invariant_scalar",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "counterexample_id": "CE1062_3_shadow_matter_frame",
            "surviving_term": "A_A(Xhat)^2 g_obs or m_A(Xhat) psi_bar psi",
            "why_survives": "ordinary covariance alone does not forbid hidden matter frames or mass maps",
            "blocks": "matter pullback zero and material beta zero",
            "source": "CE1055_2_shadow_matter_frame; MFS1045_4_no_shadow_frame",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "counterexample_id": "CE1062_4_readout_regeneration",
            "surviving_term": "loop/readout-induced f_X F^2 or clock_Xhat map",
            "why_survives": "bare action sequestering is not automatically stable under effective reductions",
            "blocks": "radiative/readout closure",
            "source": "CE1055_4_readout_regeneration; ZC1054_6_radiative_readout_closure",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def closure_rows() -> list[dict[str, str]]:
    return [
        {
            "closure_id": "CLOS1062_0_WEP_alpha_route_status",
            "route": "MICROSCOPE WEP alpha/Coulomb product route",
            "status": "closure_only_nonclaim",
            "reason": "conditional zero theorem is exact but parent premises are unsigned and numeric product is missing",
            "what_is_preserved": "material convention, product target, and theorem contract",
            "what_is_forbidden": "WEP pass, beta_source_alpha=1, tau_WEP=1, standalone b_alpha claim, public local-GR claim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "closure_id": "CLOS1062_1_future_promotion_condition",
            "route": "promotion out of closure",
            "status": "requires_parent_signature_or_numeric_product",
            "reason": "either sign the parent product-zero theorem or supply a sourced numeric P_WEP_alpha below 4.797780522732e-05",
            "what_is_preserved": "single product scoring rule",
            "what_is_forbidden": "moving factors between beta_source_alpha, b_alpha, and tau_WEP after seeing the bound",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1062_0_WEP_alpha_closure_zero_not_parent_derived",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_alpha",
            "product_value": "CLOSURE_ZERO_NOT_PARENT_DERIVED",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1062_PARENT_PRODUCT_THEOREM_ATTEMPT.csv",
            "inputs_present": "conditional theorem clauses only",
            "required_inputs": "parent-signed product-zero theorem OR sourced numeric P_WEP_alpha",
            "derivation_status": "THEOREM_NOT_CLOSED_CURRENT_CORPUS",
            "valid_for_claim": "false",
            "notes": "A closure zero is deliberately nonnumeric so the product runner refuses it.",
        }
    ]


def bound_rows() -> list[dict[str, str]]:
    return [
        {
            "bound_id": "BOUND1062_0_WEP_alpha_screened_product_target",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_alpha",
            "bound_value": "4.797780522732e-05",
            "bound_units": "dimensionless",
            "bound_source": "source-intake/mts_residuals/P8_Y5_R10_1061_ALPHA_PRODUCT_BOUND_IMPORT.csv",
            "source_row": "BOUND1061_0_WEP_alpha_screened_product_target",
            "bound_type": "screened_smoke_product_target_nonclaim",
            "valid_for_claim": "false",
            "notes": "Internal target only; no MTS score until theorem-zero or numeric product is parent-signed.",
        }
    ]


def product_status_rows(product_result: dict[str, Any]) -> list[dict[str, str]]:
    status = product_result["status"]
    return [
        {
            "runner_id": "APR1062_0_WEP_alpha_closure_product_runner",
            "prediction_rows": str(status.get("prediction_rows")),
            "bound_rows": str(status.get("bound_rows")),
            "valid_prediction_rows": str(status.get("valid_prediction_rows")),
            "valid_bound_rows": str(status.get("valid_bound_rows")),
            "comparison_rows": str(status.get("comparison_rows")),
            "claim_allowed": str(status.get("claim_allowed")).lower(),
            "expected_result": "reject_closure_zero_as_nonclaim",
            "status_path": str(PRODUCT_RUN_DIR / "alpha_product_runner_status.json"),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1062_0_parent_product_theorem",
            "claim": "parent action proves P_WEP_alpha=0",
            "gate_pass": "false",
            "reason": "the theorem is exact only if unsigned EM/matter/source/readout premises are signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1062_1_numeric_WEP_product",
            "claim": "MTS has a numeric WEP alpha product prediction",
            "gate_pass": "false",
            "reason": "closure zero is nonnumeric and runner valid_prediction_rows remain zero",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1062_2_WEP_pass",
            "claim": "MTS passes MICROSCOPE WEP alpha branch",
            "gate_pass": "false",
            "reason": "product target exists, but no parent-derived product or theorem-zero exists",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1062_3_local_GR",
            "claim": "local GR/Newton follows",
            "gate_pass": "false",
            "reason": "WEP alpha closure does not close EH/Newton/PPN/source normalization",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1062_0_theorem_shape",
            "decision": "parent WEP product theorem shape is retained",
            "because": "if the parent action signs the EM/matter/source/readout clauses, P_WEP_alpha=0 follows without tuning",
            "next_action": "use this as the exact contract for future parent action work",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1062_1_current_status",
            "decision": "current WEP alpha route is closure-only",
            "because": "surviving counterexamples are legal and tau_WEP/readout is not derived",
            "next_action": "do not score the WEP alpha branch yet",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1062_2_best_next",
            "decision": "attack source-label forgetting and Noether current owner directly",
            "because": "relative source weights are the cleanest live counterexample for WEP/source normalization",
            "next_action": "1063-Y5-R10-source-label-forgetting-Noether-current-owner-or-relative-weight-prior.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1063-Y5-R10-source-label-forgetting-Noether-current-owner-or-relative-weight-prior.md",
            "objective": "try to derive species-blind source-label forgetting and the Noether current owner that would remove relative source weights; if not derivable, write explicit relative-weight prior/product rows for WEP, PPN/Newton source normalization, and R10 without claiming a pass.",
            "include": "source functor domain, same-action Hilbert source, relative w_A counterexample, Noether current owner, measured-G common-mode absorption, claim/refusal gates",
            "exclude": "assuming WEP, hiding relative weights in measured G, unity shortcuts, public local-GR/WEP/R10 claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def count_formalization_modified_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    start_time = STARTED.timestamp()
    for path in FORMALIZATION.rglob("*"):
        try:
            if path.is_file() and path.stat().st_mtime > start_time:
                count += 1
        except OSError:
            continue
    return count


def validate_outputs(
    outputs: dict[str, Path],
    source_rows: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
    premise_rows: list[dict[str, str]],
    counterexamples: list[dict[str, str]],
    closure: list[dict[str, str]],
    prediction_rows_: list[dict[str, str]],
    product_result: dict[str, Any],
    claims: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()})

    sources_ok = source_rows and all(row["exists"] == "true" and row["needle_found"] == "true" for row in source_rows)
    add("V1062_1_sources_exist_and_needles", sources_ok, "every cited local source path exists and every source needle was found")
    theorem_ok = any(row["theorem_step"] == "THM1062_6_verdict" and row["current_status"] == "THEOREM_NOT_CLOSED_CURRENT_CORPUS" for row in theorem_rows)
    add("V1062_2_theorem_verdict_written", theorem_ok, "conditional theorem is written and not promoted")
    premise_blocked = premise_rows and all(row["signed_now"] == "false" for row in premise_rows)
    add("V1062_3_premises_unsigned", premise_blocked, "all required theorem premises remain unsigned")
    counterexamples_ok = len(counterexamples) >= 5 and all(row["valid_for_claim"] == "false" for row in counterexamples)
    add("V1062_4_counterexamples_recorded", counterexamples_ok, "surviving counterexamples are recorded")
    closure_ok = any(row["closure_id"] == "CLOS1062_0_WEP_alpha_route_status" and row["status"] == "closure_only_nonclaim" for row in closure)
    add("V1062_5_closure_demotion_written", closure_ok, "WEP alpha route demoted to closure-only/nonclaim")
    prediction_nonclaim = prediction_rows_ and all(row["valid_for_claim"] == "false" and "CLOSURE_ZERO" in row["product_value"] for row in prediction_rows_)
    add("V1062_6_closure_prediction_nonnumeric", prediction_nonclaim, "closure zero is nonnumeric and cannot be scored")
    product_refused = product_result["status"].get("valid_prediction_rows") == 0 and product_result["status"].get("claim_allowed") is False
    add("V1062_7_product_runner_refuses_closure", product_refused, "product runner refuses closure-only zero")
    claims_blocked = claims and all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claims)
    add("V1062_8_claim_gates_blocked", claims_blocked, "all claim gates remain blocked")
    next_ok = next_rows and next_rows[0]["next_target"].startswith("1063-Y5-R10-source-label-forgetting")
    add("V1062_9_next_target_written", bool(next_ok), "next target selects source-label forgetting and Noether current owner")
    generated_inside = all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in outputs.values())
    add("V1062_10_generated_files_in_post_checkpoint", generated_inside, "all generated files are under post-checkpoint-work")
    formalization_count = count_formalization_modified_since_start()
    add("V1062_11_formalization_untouched", formalization_count == 0, f"formalization-workbench modified-file count since script start is {formalization_count}")

    summary_pass = all(row["result"] == "pass" for row in checks)
    checks.insert(0, {"check_id": "V1062_SUMMARY", "result": "pass" if summary_pass else "fail", "detail": "1062 parent WEP product theorem / closure validation summary", "generated_utc": stamp()})
    return checks


def write_doc(
    source_rows: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
    premise_rows: list[dict[str, str]],
    counterexamples: list[dict[str, str]],
    closure: list[dict[str, str]],
    predictions: list[dict[str, str]],
    bounds: list[dict[str, str]],
    product_status: list[dict[str, str]],
    product_comparisons: list[dict[str, Any]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1062 - Parent Source-Normalization tau_WEP Product Theorem Or WEP Alpha Closure",
            "",
            "**Current verdict:** the direct theorem has the right shape, but it is not signed by the present corpus. `P_WEP_alpha=0` remains a conditional parent-action theorem, not a live result.",
            "",
            "**Hard demotion:** the WEP alpha/Coulomb route is closure-only/nonclaim until either the parent product-zero theorem is signed or a sourced numeric `P_WEP_alpha` is supplied.",
            "",
            "**Best next move:** attack source-label forgetting and Noether current ownership, because relative source weights are the cleanest WEP/source-normalization counterexample still alive.",
            "",
            "## Source Register",
            md_table(source_rows, ["source_id", "relative_path", "exists", "needle", "needle_found", "note"]),
            "",
            "## Parent Product Theorem Attempt",
            md_table(theorem_rows, ["theorem_step", "statement", "formal_move", "current_status", "proof_gap", "claim_allowed"]),
            "",
            "## Premise Signature Audit",
            md_table(premise_rows, ["premise_id", "premise", "source", "current_signature", "signed_now", "if_signed", "if_unsigned"]),
            "",
            "## Counterexample Survival Ledger",
            md_table(counterexamples, ["counterexample_id", "surviving_term", "why_survives", "blocks", "source"]),
            "",
            "## Closure Demotion",
            md_table(closure, ["closure_id", "route", "status", "reason", "what_is_preserved", "what_is_forbidden"]),
            "",
            "## Closure Prediction Row",
            md_table(predictions, ["prediction_id", "arena", "product_symbol", "product_value", "product_units", "inputs_present", "required_inputs", "derivation_status", "valid_for_claim"]),
            "",
            "## Bound Import",
            md_table(bounds, ["bound_id", "arena", "product_symbol", "bound_value", "bound_units", "bound_type", "valid_for_claim"]),
            "",
            "## Product Runner Status",
            md_table(product_status, ["runner_id", "prediction_rows", "bound_rows", "valid_prediction_rows", "valid_bound_rows", "comparison_rows", "claim_allowed", "expected_result"]),
            "",
            "## Product Comparison Rows",
            md_table(product_comparisons, ["comparison_id", "arena", "product_symbol", "product_value", "bound_value", "comparison_status", "pass_for_claim", "issues"]),
            "",
            "## Claim Gates",
            md_table(claims, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "",
            "## Decision Ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "",
            "## Validation",
            md_table(validation, ["check_id", "result", "detail", "generated_utc"]),
            "",
            "## Next Target",
            md_table(next_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    theorem = theorem_attempt_rows()
    premises = premise_audit_rows()
    counterexamples = counterexample_rows()
    closure = closure_rows()
    predictions = prediction_rows()
    bounds = bound_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    outputs = {
        "sources": OUT / "P8_Y5_R10_1062_SOURCE_REGISTER.csv",
        "theorem": OUT / "P8_Y5_R10_1062_PARENT_PRODUCT_THEOREM_ATTEMPT.csv",
        "premises": OUT / "P8_Y5_R10_1062_PREMISE_SIGNATURE_AUDIT.csv",
        "counterexamples": OUT / "P8_Y5_R10_1062_COUNTEREXAMPLE_SURVIVAL_LEDGER.csv",
        "closure": OUT / "P8_Y5_R10_1062_WEP_ALPHA_CLOSURE_DEMOTION.csv",
        "predictions": PREDICTION_CLOSURE,
        "bounds": BOUND_IMPORT,
        "runner_status": OUT / "P8_Y5_R10_1062_PRODUCT_RUNNER_STATUS.csv",
        "comparisons": OUT / "P8_Y5_R10_1062_PRODUCT_COMPARISON_ROWS.csv",
        "claims": OUT / "P8_Y5_R10_1062_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1062_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1062_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1062_VALIDATION.csv",
        "doc": DOC,
    }

    write_csv(outputs["sources"], sources)
    write_csv(outputs["theorem"], theorem)
    write_csv(outputs["premises"], premises)
    write_csv(outputs["counterexamples"], counterexamples)
    write_csv(outputs["closure"], closure)
    write_csv(outputs["predictions"], predictions, PRODUCT_REQUIRED_COLUMNS)
    write_csv(outputs["bounds"], bounds, BOUND_REQUIRED_COLUMNS)
    write_csv(outputs["claims"], claims)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_rows)

    product_result = run_product_runner(PREDICTION_CLOSURE, BOUND_IMPORT, PRODUCT_RUN_DIR)
    status_rows = product_status_rows(product_result)
    write_csv(outputs["runner_status"], status_rows)
    write_csv(outputs["comparisons"], product_result["comparisons"])

    validation = validate_outputs(
        outputs,
        sources,
        theorem,
        premises,
        counterexamples,
        closure,
        predictions,
        product_result,
        claims,
        next_rows,
    )
    write_csv(outputs["validation"], validation)
    write_doc(
        sources,
        theorem,
        premises,
        counterexamples,
        closure,
        predictions,
        bounds,
        status_rows,
        product_result["comparisons"],
        claims,
        decisions,
        validation,
        next_rows,
    )

    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()

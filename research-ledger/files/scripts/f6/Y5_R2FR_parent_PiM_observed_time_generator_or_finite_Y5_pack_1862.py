from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
MICROSCOPE_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1862"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1862-Y5-R2FR-parent-PiM-observed-time-generator-or-finite-Y5-pack.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1862_SOURCE_REGISTER.csv",
    "pim_chain_reintegration": RESIDUALS / "P8_Y5_PARENT_QLOC_1862_PIM_CHAIN_REINTEGRATION.csv",
    "source_measure_derivation": RESIDUALS / "P8_Y5_PARENT_QLOC_1862_SOURCE_MEASURE_DERIVATION_CONTRACT.csv",
    "delta_hsrc_status": RESIDUALS / "P8_Y5_PARENT_QLOC_1862_DELTA_HSRC_STATUS.csv",
    "current_live_lock": RESIDUALS / "P8_Y5_PARENT_QLOC_1862_CURRENT_LIVE_LOCK.csv",
    "finite_y5_policy": RESIDUALS / "P8_Y5_PARENT_QLOC_1862_FINITE_Y5_POLICY.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1862_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1862_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1862_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1862_VALIDATION.csv",
}


def as_bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _ in fields) + " |"
    body = [
        "| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def source_register() -> list[dict[str, Any]]:
    rows = [
        {
            "source_id": "SRC1862_0_1861_doc",
            "source_kind": "current_handoff",
            "source_path": ROOT / "1861-Y5-R2FR-source-functional-evenness-JZ-BZ-coupling-lock-or-profile-acquisition.md",
            "required_needle": "NEXT1861_0_primary",
            "use_in_1862": "1861 selects parent Pi_M observed-time/source-charge ownership as the Y5 primary route.",
        },
        {
            "source_id": "SRC1862_1_1794_doc",
            "source_kind": "prior_y5_checkpoint",
            "source_path": ROOT / "1794-Y5-R2FR-parent-PiM-observed-time-generator-or-finite-Y5-pack.md",
            "required_needle": "PIM_OBSERVED_TIME_NOT_PARENT_OWNED",
            "use_in_1862": "1794 proves the Pi_M/tau_obs gate is precisely specified but not parent-owned.",
        },
        {
            "source_id": "SRC1862_2_1795_doc",
            "source_kind": "prior_y5_checkpoint",
            "source_path": ROOT / "1795-Y5-R2FR-Hamiltonian-PiM-adoption-or-Delta-Hsrc-component-pack.md",
            "required_needle": "DELTA_HSRC_RETAINED_NONCLAIM",
            "use_in_1862": "1795 names Delta_Hsrc as the exact source-measure mismatch instead of hiding it in GM fitting.",
        },
        {
            "source_id": "SRC1862_3_1796_doc",
            "source_kind": "prior_y5_checkpoint",
            "source_path": ROOT / "1796-Y5-R2FR-Hamiltonian-charge-integrability-reference-or-first-Delta-Hsrc-row.md",
            "required_needle": "INTEGRABILITY_REFERENCE_NOT_PROVED",
            "use_in_1862": "1796 isolates the first Delta_Hsrc component: Hamiltonian integrability/reference lock.",
        },
        {
            "source_id": "SRC1862_4_1797_doc",
            "source_kind": "prior_y5_checkpoint",
            "source_path": ROOT / "1797-Y5-R2FR-Delta-integrability-source-acquisition-or-bound-row.md",
            "required_needle": "DELTA_INTEGRABILITY_ZERO_PROOF_NOT_CLOSED",
            "use_in_1862": "1797 maps all five Delta_integrability sub-inputs and shows zero/bound rows are not ready.",
        },
        {
            "source_id": "SRC1862_5_1798_doc",
            "source_kind": "prior_y5_checkpoint",
            "source_path": ROOT / "1798-Y5-R2FR-parent-Theta-Qtau-current-owner-or-deltaH-curl-component-pack.md",
            "required_needle": "PARENT_THETA_QTAU_OWNER_NOT_SIGNED",
            "use_in_1862": "1798 reduces the first sub-input to the parent Theta_total/Q_tau current-owner problem.",
        },
        {
            "source_id": "SRC1862_6_1799_doc",
            "source_kind": "prior_y5_checkpoint",
            "source_path": ROOT / "1799-Y5-R2FR-minimal-parent-current-action-skeleton-or-first-Ix-row.md",
            "required_needle": "RELATIVE_SKELETON_READY_PARENT_UNSIGNED",
            "use_in_1862": "1799 gives a useful X-sector action skeleton but does not parent-select it.",
        },
        {
            "source_id": "SRC1862_7_1800_doc",
            "source_kind": "prior_y5_checkpoint",
            "source_path": ROOT / "1800-Y5-R2FR-X-positive-operator-activation-or-Yukawa-fallback-row.md",
            "required_needle": "X_POSITIVE_OPERATOR_NOT_ACTIVATED",
            "use_in_1862": "1800 shows the X nohair route does not activate and the Yukawa fallback is still nonclaim.",
        },
        {
            "source_id": "SRC1862_8_1860_doc",
            "source_kind": "local_GR_gate",
            "source_path": ROOT / "1860-Y5-R2FR-Gamma-Khat-q-loc-action-existence-bridge-to-local-EH-fixed-point.md",
            "required_needle": "epsilon_GK_q_loc",
            "use_in_1862": "1860 keeps q_loc/local-GR inheritance blocked while coupling and source locks remain open.",
        },
        {
            "source_id": "SRC1862_9_1797_matrix",
            "source_kind": "csv_evidence",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1797_SOURCE_ACQUISITION_MATRIX.csv",
            "required_needle": "AQR1797_0_delta_H_tau_nonintegrable",
            "use_in_1862": "1797 matrix identifies delta_H_tau_nonintegrable as the highest-leverage Delta_integrability input.",
        },
        {
            "source_id": "SRC1862_10_1798_curl_pack",
            "source_kind": "csv_evidence",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1798_DELTAH_CURL_COMPONENT_PACK.csv",
            "required_needle": "DCC1798_1_I_X",
            "use_in_1862": "1798 curl pack splits delta_H_tau into I_X, I_projector, I_boundary, I_ref, I_tau, I_surface and I_Dq.",
        },
        {
            "source_id": "SRC1862_11_1800_next",
            "source_kind": "csv_decision",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1800_NEXT_TARGET.csv",
            "required_needle": "NEXT1800_0_primary",
            "use_in_1862": "1800 selects J_X source-zero/component bounds as the next concrete fork inside the X route.",
        },
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            **{key: str(value) if isinstance(value, Path) else value for key, value in row.items()},
            "valid_for_claim": as_bool_text(False),
        }
        for row in rows
    ]


def pim_chain_reintegration() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "chain_id": "PCR1862_0_1861_selection",
            "stage": "post-1861 route selection",
            "result": "Y5 source-charge ownership is the primary coupling-lock route",
            "mathematical_object": "mu_obs = G_ref M_H[Pi_M J_H] + mu_extra",
            "current_status": "SELECTED_NOT_CLOSED",
            "next_dependency": "parent Pi_M/tau_obs observed source charge",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "chain_id": "PCR1862_1_1794_PiM_tau",
            "stage": "Pi_M and observed-time gate",
            "result": "Pi_M/tau_obs must be parent selected before orbital/source readout",
            "mathematical_object": "B_local=(M_local,e_obs,B_clock,B_ref,orientation,domain_class); Pi_M:=Pi_M^H or equivalent",
            "current_status": "PIM_OBSERVED_TIME_NOT_PARENT_OWNED",
            "next_dependency": "tau_obs, clock normalization, same frame, pre-readout selection and Pi_M adoption",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "chain_id": "PCR1862_2_1795_Delta_Hsrc",
            "stage": "source-measure identity",
            "result": "all source-measure failure is compressed into Delta_Hsrc",
            "mathematical_object": "Delta_Hsrc := G_ref^-1 int_S Q_tau^MTS - H_ref - M_eff[Pi_M^H J_H^dress]",
            "current_status": "DELTA_HSRC_RETAINED_NONCLAIM",
            "next_dependency": "integrability, R_eq, commutator, boundary/reference, extra charge, tau/MHref and readout",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "chain_id": "PCR1862_3_1796_integrability",
            "stage": "first Delta_Hsrc component",
            "result": "Delta_integrability is the first nonclaim component",
            "mathematical_object": "Delta_integrability/M_H_ref = |delta_H_tau|/M_H_ref + |Delta_ref|/M_H_ref + |B_zero_flux|/M_H_ref + |Delta_symp|/M_H_ref",
            "current_status": "INTEGRABILITY_REFERENCE_NOT_PROVED",
            "next_dependency": "Theta_total/Q_tau owner, fixed reference, boundary/symplectic silence and tau/MHref lock",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "chain_id": "PCR1862_4_1797_source_matrix",
            "stage": "Delta_integrability source acquisition",
            "result": "all five sub-inputs are source-mapped but not theorem-zero or finite numeric",
            "mathematical_object": "delta_H_tau; Delta_ref; B_zero_flux; Delta_symp; tau_MHref_lock",
            "current_status": "DELTA_INTEGRABILITY_ZERO_PROOF_NOT_CLOSED",
            "next_dependency": "parent current owner and source-backed subcomponent rows",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "chain_id": "PCR1862_5_1798_current_owner",
            "stage": "parent current owner",
            "result": "Theta_total/Q_tau current owner is not signed; curl splits into seven component debts",
            "mathematical_object": "delta_H_tau/M_H_ref = (|I_X|+|I_projector|+|I_boundary|+|I_ref|+|I_tau|+|I_surface|+|I_Dq|)/M_H_ref",
            "current_status": "PARENT_THETA_QTAU_OWNER_NOT_SIGNED",
            "next_dependency": "I_X first, with projector/tau/Dq in parallel",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "chain_id": "PCR1862_6_1799_1800_X_route",
            "stage": "first non-EH curl component",
            "result": "X skeleton/nohair route is mathematically useful but not parent activated",
            "mathematical_object": "I_X/M_H_ref = |int_S i_tau omega_X + int_A C_X + boundary_X|/M_H_ref; alpha_X(lambda)=K_X Qbar_XH qbar_XT",
            "current_status": "X_ROUTE_RELATIVE_ONLY_NONCLAIM",
            "next_dependency": "J_X=0/source component bounds, operator sign/gap, boundary zero and Pi_M projection",
            "valid_for_claim": as_bool_text(False),
        },
    ]


def source_measure_derivation_contract() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "contract_id": "SMC1862_0_parent_charge",
            "required_statement": "the source mass is a parent Hamiltonian/covariant-phase-space charge",
            "mathematical_form": "M_H[S,tau] = G_ref^-1 int_S Q_tau^MTS - H_ref",
            "status": "FORMAL_TARGET_NOT_PARENT_SIGNED",
            "blocking_gap": "Theta_total/Q_tau^MTS are component scaffolds, not one varied parent current chain",
            "closes_if": "one parent action supplies L_parent, Theta_total, Q_tau^MTS, C_tau and fixed H_ref for all retained sectors",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "SMC1862_1_same_source",
            "required_statement": "the Hamiltonian charge reads the same dressed worldtube source used by matter/source/current",
            "mathematical_form": "M_H[W;S] = M_eff[Pi_M^H J_H^dress]",
            "status": "CONDITIONAL_LEMMA_SHAPE_ONLY",
            "blocking_gap": "source functor, worldtube glue, R_eq and boundary/reference terms are unsigned",
            "closes_if": "Pi_M^H source-measure lemma is parent signed with R_eq=0 and no hidden post-readout calibration",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "SMC1862_2_projector_commutator",
            "required_statement": "Pi_M does not create product-rule leakage on the physical Hilbert current",
            "mathematical_form": "d(Pi_M J_H)=Pi_M dJ_H+[d,Pi_M]J_H with [d,Pi_M]J_H=0",
            "status": "CONDITIONAL_CHAINMAP_ONLY",
            "blocking_gap": "fixed domain, physical current complex, exterior silence and tau/MHref lock are not signed",
            "closes_if": "parent-fixed chain map or finite I_commutator row with units/source paths",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "SMC1862_3_integrability",
            "required_statement": "the Hamiltonian mass one-form is exact on the allowed local branch",
            "mathematical_form": "curl_delta H_tau = 0, equivalently I_X+I_projector+I_boundary+I_ref+I_tau+I_surface+I_Dq = 0 as absolute theorem-zero components",
            "status": "NOT_DERIVED",
            "blocking_gap": "first component I_X is not zero/bounded, and parent current owner is unsigned",
            "closes_if": "all curl components theorem-zero or source-backed finite with common M_H_ref denominator",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "SMC1862_4_no_circular_GM",
            "required_statement": "orbital GM cannot be used to prove the source mass it is supposed to test",
            "mathematical_form": "M_orbit=G_ref M_H only after Delta_Hsrc=0/bounded and Gauss/PPN gates pass",
            "status": "GUARDRAIL_PASS_NO_CLAIM",
            "blocking_gap": "guardrail is installed, but source-normalized Newton is still downstream",
            "closes_if": "Delta_Hsrc closes first, then Gauss/orbital/PPN readout follows",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "SMC1862_5_verdict",
            "required_statement": "Y5 source-normalization owner theorem",
            "mathematical_form": "SMC1862_0 through SMC1862_4 close in one parent branch",
            "status": "Y5_SOURCE_OWNER_NOT_PROVED",
            "blocking_gap": "Pi_M/tau ownership has reduced to Delta_Hsrc, then Delta_integrability, then parent-current/I_X/J_X locks",
            "closes_if": "single parent current chain plus nohair/source-zero or finite empirical rows",
            "valid_for_claim": as_bool_text(False),
        },
    ]


def delta_hsrc_status() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "object_id": "DHS1862_0_Delta_Hsrc",
            "symbol": "Delta_Hsrc",
            "current_identity": "G_ref^-1 int_S Q_tau^MTS - H_ref - M_eff[Pi_M^H J_H^dress]",
            "status": "CENTRAL_Y5_RESIDUAL_RETAINED",
            "current_best_decomposition": "Delta_integrability + R_eq + I_commutator + B_ref + Delta_extra_charge + Delta_tau_MHref + Delta_Gauss_PPN",
            "zero_or_bound_status": "NOT_ZERO_NOT_SCORED",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "object_id": "DHS1862_1_Delta_integrability",
            "symbol": "Delta_integrability",
            "current_identity": "|delta_H_tau| + |Delta_ref| + |B_zero_flux| + |Delta_symp| normalized by M_H_ref",
            "status": "FIRST_COMPONENT_RETAINED",
            "current_best_decomposition": "delta_H_tau plus reference/boundary/symplectic/tau-MHref locks",
            "zero_or_bound_status": "SOURCE_MAPPED_NOT_FILLED",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "object_id": "DHS1862_2_delta_H_tau",
            "symbol": "delta_H_tau_nonintegrable",
            "current_identity": "(|I_X|+|I_projector|+|I_boundary|+|I_ref|+|I_tau|+|I_surface|+|I_Dq|)/M_H_ref",
            "status": "CURRENT_CURL_BLOCKER",
            "current_best_decomposition": "I_X is first target; projector, boundary/reference, tau/surface and Dq remain parallel debts",
            "zero_or_bound_status": "COMPONENT_PACK_REJECTED_NONCLAIM",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "object_id": "DHS1862_3_I_X",
            "symbol": "I_X",
            "current_identity": "|int_S i_tau omega_X + int_A C_X + boundary_X|/M_H_ref",
            "status": "FIRST_NON_EH_CURL_TARGET",
            "current_best_decomposition": "operator sign/gap + J_X source silence + boundary/zero-mode + Pi_M projection",
            "zero_or_bound_status": "NOHAIR_NOT_ACTIVATED_AND_YUKAWA_FALLBACK_NOT_SCOREABLE",
            "valid_for_claim": as_bool_text(False),
        },
    ]


def current_live_lock() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "lock_id": "LOCK1862_0_parent_current",
            "live_lock": "one signed parent current chain",
            "why_it_matters": "without one L_parent -> Theta_total -> Q_tau^MTS chain, Hamiltonian mass is only a component scaffold",
            "current_status": "PARENT_THETA_QTAU_OWNER_NOT_SIGNED",
            "best_next_move": "try a single-parent-current synthesis rather than another post-readout charge definition",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "lock_id": "LOCK1862_1_X_source",
            "live_lock": "J_X source silence or finite component bounds",
            "why_it_matters": "J_X=0 is the gate that activates the nohair route; if not, it supplies source/test charges for alpha_X(lambda)",
            "current_status": "JX_NOT_ZEROED_NOT_SOURCED",
            "best_next_move": "derive J_X=0 from matter/readout/boundary descent or emit J_matter/J_chiD/J_boundary/J_readout/J_history rows",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "lock_id": "LOCK1862_2_operator",
            "live_lock": "Z_X, M_X^2, sign/gap and zero-mode rule",
            "why_it_matters": "positive operator/nohair and finite Yukawa range both require these values or theorems",
            "current_status": "OPERATOR_SIGN_GAP_MISSING",
            "best_next_move": "keep parallel operator source row after J_X route is staged",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "lock_id": "LOCK1862_3_projection",
            "live_lock": "Pi_M^H projection of X/extras",
            "why_it_matters": "X may exist but not couple to Hamiltonian mass; projection must be theorem-zero or bounded",
            "current_status": "PIM_H_PROJECTION_MISSING",
            "best_next_move": "carry projection as required row in any I_X/J_X fallback",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "lock_id": "LOCK1862_4_q_loc",
            "live_lock": "q_loc/local-GR inheritance",
            "why_it_matters": "even if Y5 progresses, local GR remains blocked until q_loc/Y6/readout/coupling gates close jointly",
            "current_status": "LOCAL_GR_NOT_REOPENED",
            "best_next_move": "do not claim GR/Newton; feed Y5 result back into q_loc only after source owner closes",
            "valid_for_claim": as_bool_text(False),
        },
    ]


def finite_y5_policy() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "policy_id": "FYP1862_0_no_GM_hiding",
            "policy": "do not use orbital GM to define the source charge",
            "allowed_use": "orbital/Gauss/PPN readout after Delta_Hsrc is theorem-zero or source-bounded",
            "forbidden_use": "using fitted GM to set Pi_M, tau_obs, M_H_ref, H_ref or Delta_Hsrc=0",
            "status": "ACTIVE_GUARDRAIL",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "policy_id": "FYP1862_1_no_cancellation",
            "policy": "finite Y5 residuals use absolute envelopes",
            "allowed_use": "sum absolute component bounds with common units and positive same-frame M_H_ref",
            "forbidden_use": "cancellation between Delta_integrability, R_eq, I_commutator, boundary, extra charge and readout terms",
            "status": "ACTIVE_GUARDRAIL_VALUES_MISSING",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "policy_id": "FYP1862_2_theory_first_then_data",
            "policy": "run R10/PPN/orbital scoring only after parent coefficients exist",
            "allowed_use": "nonclaim runner smoke and schema validation",
            "forbidden_use": "treating placeholder alpha_X(lambda) or Delta_Hsrc rows as evidence",
            "status": "ACTIVE_NONCLAIM_POLICY",
            "valid_for_claim": as_bool_text(False),
        },
    ]


def claim_gate() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1862_0_chain_reintegrated",
            "claim": "Y5/PiM prior chain has been reintegrated into the post-1861 coupling-lock route",
            "gate_pass": as_bool_text(True),
            "reason": "sources 1794 through 1800 are imported and current residual hierarchy is explicit",
            "claim_allowed": as_bool_text(True),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1862_1_PiM_tau_parent_owned",
            "claim": "Pi_M/tau_obs source charge is parent-owned",
            "gate_pass": as_bool_text(False),
            "reason": "1794 gate remains PIM_OBSERVED_TIME_NOT_PARENT_OWNED",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1862_2_Delta_Hsrc_zero",
            "claim": "Delta_Hsrc=0",
            "gate_pass": as_bool_text(False),
            "reason": "Delta_integrability, R_eq, commutator, boundary/reference, extra charge and readout terms are not jointly closed",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1862_3_parent_current_owner",
            "claim": "Theta_total/Q_tau^MTS current owner is signed",
            "gate_pass": as_bool_text(False),
            "reason": "1798 verdict remains PARENT_THETA_QTAU_OWNER_NOT_SIGNED",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1862_4_I_X_zero_or_bounded",
            "claim": "first non-EH curl component I_X is zero or source-bounded",
            "gate_pass": as_bool_text(False),
            "reason": "1799/1800 keep X skeleton/nohair and Yukawa fallback nonclaim",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1862_5_source_normalized_Newton",
            "claim": "source-normalized Newton is derived",
            "gate_pass": as_bool_text(False),
            "reason": "Y5 source charge is still Delta_Hsrc-blocked",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1862_6_local_GR_Newton",
            "claim": "local GR/Newton inheritance is reopened",
            "gate_pass": as_bool_text(False),
            "reason": "Y5, Y6, q_loc, readout and coupling locks are not jointly closed",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1862_0_no_duplicate_PiM",
            "decision": "do not rerun the broad Pi_M/tau route as if 1794-1800 did not exist",
            "reason": "the chain already exists and narrows the problem to parent-current ownership and I_X/J_X",
            "next_action": "use 1862 as bridge and attack the live lock",
            "claim_allowed": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1862_1_Y5_status",
            "decision": "retain Delta_Hsrc as the central Y5 source-normalization blocker",
            "reason": "Pi_M/tau/source-measure/gauge/reference gaps are now named residuals, not vague GM language",
            "next_action": "try to close parent-current owner or demote Y5 local-GR route to finite residual rows",
            "claim_allowed": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1862_2_next_target",
            "decision": "select single-parent current chain synthesis with I_X/J_X demotion fallback",
            "reason": "this is the shortest honest path from Pi_M source ownership toward derived local Newton/GR",
            "next_action": "build 1863 single-parent current action synthesis or I_X/J_X demotion checkpoint",
            "claim_allowed": as_bool_text(False),
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1862_0_primary",
            "next_target": "1863-Y5-R2FR-single-parent-current-chain-synthesis-or-Ix-Jx-demotion.md",
            "script": "scripts/Y5_R2FR_single_parent_current_chain_synthesis_or_Ix_Jx_demotion_1863.py",
            "objective": "try to construct one parent current chain owning L_parent, Theta_total, Q_tau^MTS, tau/projectability, boundary/reference, matter descent and X source silence; if not, explicitly demote the local source-normalized GR route to finite nonclaim I_X/J_X rows",
            "selection_status": "SELECTED_PRIMARY",
            "success_condition": "parent current chain closes and I_X/J_X vanish, or strict finite residual rows are emitted with no claim",
            "valid_for_claim": as_bool_text(False),
            "claim_allowed": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1862_1_parallel_Y6",
            "next_target": "1863b-Y5-R2FR-Y6-topological-projector-null-stress-gate.md",
            "script": "scripts/Y5_R2FR_Y6_topological_projector_null_stress_gate_1863b.py",
            "objective": "keep Y6 stress silence as a parallel gate because Y5 progress alone cannot reopen local GR",
            "selection_status": "HELD_PARALLEL",
            "success_condition": "Y6 stress-zero theorem or source-backed finite PPN/source-stress rows",
            "valid_for_claim": as_bool_text(False),
            "claim_allowed": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1862_2_empirical_after_coefficients",
            "next_target": "1863c-Y5-R2FR-alphaX-R10-PPN-runner-only-after-parent-coefficients.md",
            "script": "scripts/Y5_R2FR_alphaX_R10_PPN_runner_after_parent_coefficients_1863c.py",
            "objective": "run empirical bound comparisons only after Z_X, M_X^2, Qbar_XH, qbar_XT, projection coefficients and real bound curves are sourced",
            "selection_status": "HELD_UNTIL_COEFFICIENTS",
            "success_condition": "nonclaim runner becomes claim-eligible only with sourced numeric rows and real bounds",
            "valid_for_claim": as_bool_text(False),
            "claim_allowed": as_bool_text(False),
        },
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register(),
        "pim_chain_reintegration": pim_chain_reintegration(),
        "source_measure_derivation": source_measure_derivation_contract(),
        "delta_hsrc_status": delta_hsrc_status(),
        "current_live_lock": current_live_lock(),
        "finite_y5_policy": finite_y5_policy(),
        "claim_gate": claim_gate(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
    }


def copy_outputs(include_validation: bool = False) -> None:
    keys = list(OUTPUTS)
    if not include_validation:
        keys = [key for key in keys if key != "validation"]
    for key in keys:
        src = OUTPUTS[key]
        if not src.exists():
            continue
        targets = [
            MICROSCOPE_RESIDUALS / src.name,
            QUARANTINE / src.name,
            RAB_QUEUE / f"JR1862_{src.name}",
        ]
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, target)


def check_sources(rows: list[dict[str, Any]]) -> tuple[bool, str]:
    failures: list[str] = []
    for row in rows:
        path = Path(str(row["source_path"]))
        if not path.exists():
            failures.append(f"{row['source_id']} missing path {path}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        needle = str(row["required_needle"])
        if needle not in text:
            failures.append(f"{row['source_id']} missing needle {needle}")
    return not failures, "; ".join(failures) if failures else "all source paths and needles found"


def check_csv_outputs() -> tuple[bool, str]:
    failures: list[str] = []
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        try:
            rows = read_csv(path)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{path.name}: {exc}")
            continue
        if not rows:
            failures.append(f"{path.name}: no rows")
    return not failures, "; ".join(failures) if failures else "all generated CSV outputs parse and have rows"


def check_branch_copies() -> tuple[bool, str]:
    missing: list[str] = []
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        for target in [
            MICROSCOPE_RESIDUALS / path.name,
            QUARANTINE / path.name,
            RAB_QUEUE / f"JR1862_{path.name}",
        ]:
            if not target.exists():
                missing.append(str(target))
    return not missing, "missing copies: " + "; ".join(missing) if missing else "branch/quarantine/queue copies exist"


def any_true_valid_for_claim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            if str(row.get("valid_for_claim", "False")).lower() == "true":
                return True
    return False


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    checks: list[tuple[str, bool, str]] = []
    ok, detail = check_sources(rows_map["source_register"])
    checks.append(("VAL1862_0_sources_found", ok, detail))
    ok, detail = check_csv_outputs()
    checks.append(("VAL1862_1_csv_outputs_parse", ok, detail))
    checks.append(
        (
            "VAL1862_2_chain_reintegrated",
            any(row["chain_id"] == "PCR1862_6_1799_1800_X_route" for row in rows_map["pim_chain_reintegration"]),
            "Y5 chain from Pi_M/tau through X route is represented",
        )
    )
    checks.append(
        (
            "VAL1862_3_source_owner_not_proved",
            any(row["contract_id"] == "SMC1862_5_verdict" and row["status"] == "Y5_SOURCE_OWNER_NOT_PROVED" for row in rows_map["source_measure_derivation"]),
            "Y5 source-owner theorem remains explicitly unproved",
        )
    )
    checks.append(
        (
            "VAL1862_4_delta_hsrc_retained",
            any(row["object_id"] == "DHS1862_0_Delta_Hsrc" and row["status"] == "CENTRAL_Y5_RESIDUAL_RETAINED" for row in rows_map["delta_hsrc_status"]),
            "Delta_Hsrc retained as central Y5 residual",
        )
    )
    checks.append(
        (
            "VAL1862_5_live_lock_selected",
            any(row["lock_id"] == "LOCK1862_1_X_source" for row in rows_map["current_live_lock"]),
            "I_X/J_X live lock is selected inside the parent-current route",
        )
    )
    blocked_claims = [
        row
        for row in rows_map["claim_gate"]
        if row["claim_id"] in {
            "CG1862_1_PiM_tau_parent_owned",
            "CG1862_2_Delta_Hsrc_zero",
            "CG1862_5_source_normalized_Newton",
            "CG1862_6_local_GR_Newton",
        }
    ]
    checks.append(
        (
            "VAL1862_6_claim_gates_blocked",
            len(blocked_claims) == 4 and all(row["gate_pass"] == "False" for row in blocked_claims),
            "Pi_M/Delta_Hsrc/Newton/local-GR claims remain blocked",
        )
    )
    checks.append(
        (
            "VAL1862_7_no_claim_rows_promoted",
            not any_true_valid_for_claim(rows_map),
            "no generated 1862 row has valid_for_claim=True",
        )
    )
    checks.append(
        (
            "VAL1862_8_next_target_selected",
            any(row["route_id"] == "NEXT1862_0_primary" and row["selection_status"] == "SELECTED_PRIMARY" for row in rows_map["next_target"]),
            "1863 single-parent-current synthesis/I_X-J_X demotion selected",
        )
    )
    ok, detail = check_branch_copies()
    checks.append(("VAL1862_9_branch_copies", ok, detail))
    pycache_path = ROOT / "scripts" / "__pycache__"
    checks.append(("VAL1862_10_pycache_absent", not pycache_path.exists(), "scripts __pycache__ absent"))
    formalization_outputs: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in [
            "*1862*",
            "P8_Y5_PARENT_QLOC_1862*",
            "P8_Y5_BRR545_1862*",
            "Y5_R2FR_parent_PiM_observed_time_generator_or_finite_Y5_pack_1862.py",
        ]:
            formalization_outputs.extend(FORMALIZATION.rglob(pattern))
    formalization_detail = (
        "found generated outputs: " + "; ".join(str(path) for path in formalization_outputs)
        if formalization_outputs
        else "no generated 1862 outputs found under formalization-workbench"
    )
    checks.append(("VAL1862_11_formalization_untouched", not formalization_outputs, formalization_detail))
    overall = all(result for _, result, _ in checks)
    validation_rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    validation_rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1862_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1862 Pi_M/Y5 chain reintegration checkpoint passes private validation" if overall else "one or more 1862 checks failed",
        }
    )
    return validation_rows


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, str]]) -> str:
    return "\n".join(
        [
            "# 1862 - Y5/R2FR Parent PiM Observed-Time Generator or Finite Y5 Pack",
            "",
            "**Current verdict:** the broad `Pi_M` route should not be rerun from scratch. The existing 1794-1800 chain already reduces Y5 source-normalization to a precise residual ladder: `Pi_M/tau_obs` ownership -> `Delta_Hsrc` -> `Delta_integrability` -> `delta_H_tau` curl -> `I_X/J_X` plus projector, boundary, reference, tau, surface and `Dq` debts. This is progress, but not closure. No source-normalized Newton or local-GR/Newton inheritance is claimed.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_kind", "source_path", "required_needle", "use_in_1862", "valid_for_claim"]),
            "",
            "## PiM Chain Reintegration",
            markdown_table(rows_map["pim_chain_reintegration"], ["chain_id", "stage", "result", "mathematical_object", "current_status", "next_dependency", "valid_for_claim"]),
            "",
            "## Source-Measure Derivation Contract",
            markdown_table(rows_map["source_measure_derivation"], ["contract_id", "required_statement", "mathematical_form", "status", "blocking_gap", "closes_if", "valid_for_claim"]),
            "",
            "## Delta_Hsrc Status",
            markdown_table(rows_map["delta_hsrc_status"], ["object_id", "symbol", "current_identity", "status", "current_best_decomposition", "zero_or_bound_status", "valid_for_claim"]),
            "",
            "## Current Live Lock",
            markdown_table(rows_map["current_live_lock"], ["lock_id", "live_lock", "why_it_matters", "current_status", "best_next_move", "valid_for_claim"]),
            "",
            "## Finite Y5 Policy",
            markdown_table(rows_map["finite_y5_policy"], ["policy_id", "policy", "allowed_use", "forbidden_use", "status", "valid_for_claim"]),
            "",
            "## Claim Gate",
            markdown_table(rows_map["claim_gate"], ["claim_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "",
            "## Decision Ledger",
            markdown_table(rows_map["decision_ledger"], ["decision_id", "decision", "reason", "next_action", "claim_allowed"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status", "success_condition", "claim_allowed"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "",
            "- The good bit: Y5 is now technically sharp. We are no longer arguing about a vague fitted `GM`; the exact residual is `Delta_Hsrc` and its first live piece is a parent-current / `I_X/J_X` problem.",
            "- The hard bit: that means the local-GR route still needs a real parent action/current chain. A formal charge, a topological projector, or an orbital fit is not enough.",
            "- The next attack is therefore `1863`: either synthesize one signed parent current chain, or explicitly demote this Y5 path to finite nonclaim residual rows.",
            "",
        ]
    )


def main() -> None:
    for directory in [RESIDUALS, MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
        directory.mkdir(parents=True, exist_ok=True)
    rows_map = build_rows()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs(include_validation=False)
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    copy_outputs(include_validation=True)
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1862 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()

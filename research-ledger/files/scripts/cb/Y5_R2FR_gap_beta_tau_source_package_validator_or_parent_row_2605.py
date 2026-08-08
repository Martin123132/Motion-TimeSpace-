from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_PACKAGE_VALIDATOR_REBASE_2605"
CHECKPOINT_ID = "2605"

DOC = ROOT / "2605-Y5-R2FR-gap-beta-tau-source-package-validator-or-parent-row.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PACKAGE_VALIDATOR_REBASE_2605_SOURCE_REGISTER.csv",
    "lineage_ledger": OUT / "P8_Y5_PACKAGE_VALIDATOR_REBASE_2605_LINEAGE_LEDGER.csv",
    "validator_spec": OUT / "P8_Y5_PACKAGE_VALIDATOR_REBASE_2605_VALIDATOR_SPEC.csv",
    "package_evaluation": OUT / "P8_Y5_PACKAGE_VALIDATOR_REBASE_2605_CURRENT_PACKAGE_EVALUATION.csv",
    "parent_zero_audit": OUT / "P8_Y5_PACKAGE_VALIDATOR_REBASE_2605_PARENT_ZERO_OR_SOURCE_AUDIT.csv",
    "gap_bridge": OUT / "P8_Y5_PACKAGE_VALIDATOR_REBASE_2605_GAP_AMPLITUDE_BRIDGE_THEOREM.csv",
    "candidate_rows": OUT / "P8_Y5_PACKAGE_VALIDATOR_REBASE_2605_MU_PHI_CANDIDATE_ROWS.csv",
    "acquisition_queue": OUT / "P8_Y5_PACKAGE_VALIDATOR_REBASE_2605_ACQUISITION_QUEUE.csv",
    "runner_refusal": OUT / "P8_Y5_PACKAGE_VALIDATOR_REBASE_2605_RUNNER_REFUSAL.csv",
    "claim_gates": OUT / "P8_Y5_PACKAGE_VALIDATOR_REBASE_2605_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_PACKAGE_VALIDATOR_REBASE_2605_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PACKAGE_VALIDATOR_REBASE_2605_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PACKAGE_VALIDATOR_REBASE_2605_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2605_VALIDATION.csv",
}

COPY_TARGETS = {
    "package_evaluation": LOCAL_BOUNDS / "Gap_beta_tau_package_validator_2605_NONCLAIM.csv",
    "candidate_rows": LOCAL_BOUNDS / "Mu_Phi_symbolic_candidate_rows_2605_NONCLAIM.csv",
    "next_target": QUEUE / "JR2605_PARENT_KINETIC_COEFFICIENT_OR_BOUNDARY_AMPLITUDE_NEXT.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def with_stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": utc_now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        **row,
    }


def row_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (list, tuple, set)):
        return ";".join(str(item) for item in value)
    if value is None:
        return ""
    return str(value)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row_value(row.get(field, "")) for field in fields})


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), len(rows), ""
    except Exception as exc:
        return False, 0, str(exc)


def path_has_needles(path: Path, needles: list[str]) -> list[str]:
    if not path.exists():
        return needles
    text = path.read_text(encoding="utf-8", errors="replace")
    return [needle for needle in needles if needle not in text]


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        {
            "source_id": "SRC2605_00_2604_handoff_doc",
            "source_path": ROOT / "2604-Y5-R2FR-screened-tail-derivative-law-or-finite-transition-wall-bound.md",
            "needles": ["NEXT2604_0_selected", "CPG2604_8_verdict", "VAL2604_OVERALL"],
            "role": "current branch handoff selecting gap-beta-tau source package validator",
        },
        {
            "source_id": "SRC2605_01_2604_package_gate",
            "source_path": OUT / "P8_Y5_TAIL_LAW_REBASE_2604_CANONICAL_PACKAGE_GATE.csv",
            "needles": ["CPG2604_1_gap", "CPG2604_3_coupling", "CPG2604_8_verdict"],
            "role": "current canonical package gate",
        },
        {
            "source_id": "SRC2605_02_2604_bridge",
            "source_path": OUT / "P8_Y5_TAIL_LAW_REBASE_2604_CANONICAL_SOURCE_BRIDGE.csv",
            "needles": ["CSR2604_0_mu_m2", "CSR2604_4_Delta_w_tau_WEP", "CSR2604_8_DeltaK"],
            "role": "current missing source bridge rows",
        },
        {
            "source_id": "SRC2605_03_1748_doc",
            "source_path": ROOT / "1748-Y5-R2FR-gap-beta-tau-source-package-validator-or-parent-row.md",
            "needles": ["EVAL1748_0_mu_m2", "PZA1748_6_verdict", "NEXT1748_0_primary", "VAL1748_OVERALL"],
            "role": "prior gap-beta-tau validator",
        },
        {
            "source_id": "SRC2605_04_1748_spec",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1748_PACKAGE_VALIDATOR_SPEC.csv",
            "needles": ["VSP1748_8_missing_guard", "VSP1748_9_zero_theorem", "VSP1748_10_verdict"],
            "role": "package validator policy and missing-row guard",
        },
        {
            "source_id": "SRC2605_05_1748_eval",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1748_CURRENT_PACKAGE_EVALUATION.csv",
            "needles": ["EVAL1748_0_mu_m2", "EVAL1748_4_delta_w_tau_bound", "EVAL1748_12_overall"],
            "role": "prior current package evaluation",
        },
        {
            "source_id": "SRC2605_06_1748_zero_audit",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1748_PARENT_ZERO_OR_SOURCE_ROW_AUDIT.csv",
            "needles": ["PZA1748_1_gap_theorem", "PZA1748_2_coupling_zero", "PZA1748_6_verdict"],
            "role": "parent zero/source-row audit",
        },
        {
            "source_id": "SRC2605_07_1748_acquisition",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1748_ACQUISITION_QUEUE.csv",
            "needles": ["ACQ1748_0_mu_m2", "ACQ1748_2_beta", "ACQ1748_11_parent_owner"],
            "role": "prior acquisition queue",
        },
        {
            "source_id": "SRC2605_08_1749_doc",
            "source_path": ROOT / "1749-Y5-R2FR-parent-gap-amplitude-row-or-tau-min-source-pack.md",
            "needles": ["MPC1749_0_mu_m2_gradient", "DEC1749_0_bridge_status", "NEXT1749_0_primary", "VAL1749_OVERALL"],
            "role": "prior parent gap/amplitude bridge attempt",
        },
        {
            "source_id": "SRC2605_09_1749_gap_bridge",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1749_GAP_AMPLITUDE_BRIDGE_THEOREM.csv",
            "needles": ["GBT1749_0_gradient_completion_to_canonical_gap", "GBT1749_1_boundary_amplitude_conversion", "GBT1749_5_verdict"],
            "role": "symbolic mu/Phi bridge theorem",
        },
        {
            "source_id": "SRC2605_10_1749_candidates",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1749_MU_PHI_CANDIDATE_ROWS.csv",
            "needles": ["MPC1749_0_mu_m2_gradient", "MPC1749_2_Phi_S_gradient", "MPC1749_5_Qalg_feed"],
            "role": "nonclaim mu/Phi candidate rows",
        },
        {
            "source_id": "SRC2605_11_1749_signature",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1749_PARENT_SIGNATURE_AUDIT.csv",
            "needles": ["SIG1749_0_action_slot", "SIG1749_4_boundary_class", "SIG1749_7_verdict"],
            "role": "parent signature audit for promotion",
        },
        {
            "source_id": "SRC2605_12_1749_tau_fallback",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1749_TAU_MIN_FALLBACK_SOURCE_PACK.csv",
            "needles": ["TFB1749_0_readout", "TFB1749_4_tau_min", "TFB1749_5_verdict"],
            "role": "tau-min fallback source pack",
        },
    ]
    rows: list[dict[str, Any]] = []
    for spec in specs:
        missing_needles = path_has_needles(spec["source_path"], spec["needles"])
        rows.append(
            with_stamp(
                {
                    "source_id": spec["source_id"],
                    "source_path": spec["source_path"],
                    "exists": spec["source_path"].exists(),
                    "missing_needles": missing_needles,
                    "source_pass": spec["source_path"].exists() and not missing_needles,
                    "role": spec["role"],
                    "valid_for_claim": False,
                }
            )
        )
    return rows


def lineage_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "step_id": "LIN2605_0_2604",
            "checkpoint": "2604",
            "question": "What remains after the conditional screened-tail derivative law?",
            "result": "Tail math is conditionally good, but source ownership is missing: gap, amplitude, coupling, tau, wall, projection and DeltaK.",
            "status": "CURRENT_HANDOFF_REBASED",
            "next_dependency": "canonical package validator or parent-owned row",
        },
        {
            "step_id": "LIN2605_1_1748",
            "checkpoint": "1748",
            "question": "Does the gap-beta-tau package contain any claim-grade prediction row?",
            "result": "No. One real external bound anchor exists, but every MTS prediction leg remains missing, conditional, symbolic or nonclaim.",
            "status": "PACKAGE_VALIDATOR_REBASED",
            "next_dependency": "mu_m2/Phi_S parent derivation first",
        },
        {
            "step_id": "LIN2605_2_1749",
            "checkpoint": "1749",
            "question": "Can mu_m2 and Phi_S be written as exact parent-action contracts?",
            "result": "Yes symbolically: mu_m2=F2/(kappa_m L0^2), ell_tr=sqrt(kappa_m L0^2/F2), Phi_S=sqrt(kappa_m)*abs(A_S).",
            "status": "SYMBOLIC_GAP_AMPLITUDE_CONTRACT_DERIVED_NONCLAIM",
            "next_dependency": "kappa_m/Z_m, F2/L0 and A_S boundary ownership",
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False, "claim_allowed": False}) for row in rows]


def validator_spec_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "spec_id": "VSP2605_0_branch",
            "field_or_gate": "same current branch",
            "requirement": "rows must belong to the current 2605 rebased local finite-source branch",
            "failure_rule": "reject blank, legacy-only or branch-mismatched rows",
        },
        {
            "spec_id": "VSP2605_1_quantity",
            "field_or_gate": "quantity and role",
            "requirement": "must name one of gap/amplitude/source leg/test leg/tau/product/tail/wall/projection/DeltaK",
            "failure_rule": "reject vague coupling symbols",
        },
        {
            "spec_id": "VSP2605_2_units",
            "field_or_gate": "units",
            "requirement": "must state concrete units compatible with declared role before scoring",
            "failure_rule": "reject missing, mixed or convention-only units",
        },
        {
            "spec_id": "VSP2605_3_source",
            "field_or_gate": "source path or parent derivation",
            "requirement": "must cite local source evidence or a parent derivation before promotion",
            "failure_rule": "reject unsourced templates, toy numbers and social proof",
        },
        {
            "spec_id": "VSP2605_4_missing_guard",
            "field_or_gate": "MISSING_* guard",
            "requirement": "any row containing MISSING_* must keep score_ready=false and claim_allowed=false",
            "failure_rule": "reject readiness on placeholder rows",
        },
        {
            "spec_id": "VSP2605_5_bound_anchor",
            "field_or_gate": "bound-only exception",
            "requirement": "external bounds can be retained as bound inputs with valid_prediction_row=false",
            "failure_rule": "reject promoting a bound anchor into an MTS prediction",
        },
        {
            "spec_id": "VSP2605_6_symbolic_contract",
            "field_or_gate": "symbolic bridge exception",
            "requirement": "symbolic mu/Phi contracts can guide derivation but cannot score until all coefficients are parent-signed",
            "failure_rule": "reject formula-only local-GR reentry",
        },
        {
            "spec_id": "VSP2605_7_zero_theorem",
            "field_or_gate": "parent zero route",
            "requirement": "zero rows need an explicit parent-signed theorem and boundary/readout silence",
            "failure_rule": "reject post-hoc setting of beta, tau, DeltaK or source weights to zero",
        },
        {
            "spec_id": "VSP2605_8_verdict",
            "field_or_gate": "validator policy",
            "requirement": "this checkpoint is a private nonclaim gate before any local score",
            "failure_rule": "no local-GR/Newton/PPN/R10/WEP claim from 2605",
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False}) for row in rows]


def package_evaluation_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "eval_id": "EVAL2605_0_mu_m2",
            "quantity": "mu_m^2",
            "definition": "canonical gap; ell_tr=1/sqrt(mu_m2)",
            "arena_role": "local screened-tail and PPN/R10 range",
            "current_status": "SYMBOLIC_PARENT_CONTRACT_ONLY",
            "source_anchor": "GBT1749_0/MPC1749_0 rebased",
            "missing_to_promote": "MISSING_KAPPA_M;MISSING_F2;MISSING_L0;MISSING_PARENT_ACTION_SOURCE;MISSING_SIGN_UNITS",
        },
        {
            "eval_id": "EVAL2605_1_Phi_S",
            "quantity": "Phi_S",
            "definition": "boundary/source amplitude for exterior tail",
            "arena_role": "local residual amplitude",
            "current_status": "SYMBOLIC_PARENT_CONTRACT_ONLY",
            "source_anchor": "GBT1749_1/MPC1749_2 rebased",
            "missing_to_promote": "MISSING_A_S;MISSING_BOUNDARY_CLASS;MISSING_NO_GROWING_BRANCH;MISSING_SOURCE_SUPPORT",
        },
        {
            "eval_id": "EVAL2605_2_domain_distance",
            "quantity": "d",
            "definition": "distance from local support to active transition/source boundary",
            "arena_role": "tail suppression exponent",
            "current_status": "MISSING_DOMAIN_DISTANCE",
            "source_anchor": "CSR2604_2/EVAL1748_2",
            "missing_to_promote": "MISSING_LOCAL_ARENA_WORLDTUBE;MISSING_SUPPORT_GEOMETRY",
        },
        {
            "eval_id": "EVAL2605_3_beta_source_test",
            "quantity": "beta_source*beta_test",
            "definition": "finite exchange coupling product if zero theorem fails",
            "arena_role": "R10/PPN/WEP/clock/orbital force residual",
            "current_status": "PRODUCT_LAW_READY_VALUES_MISSING",
            "source_anchor": "CSS1747_7/EVAL1748_3",
            "missing_to_promote": "MISSING_BETA_SOURCE;MISSING_BETA_TEST;MISSING_NORMALIZATION;MISSING_ZERO_THEOREM",
        },
        {
            "eval_id": "EVAL2605_4_delta_w_tau_bound",
            "quantity": "abs(Delta_w_TiPt*tau_WEP)",
            "definition": "external WEP product bound anchor",
            "arena_role": "WEP bound input only",
            "current_status": "EXPLICIT_BOUND_SOURCE_BACKED_NONPREDICTION",
            "source_anchor": "BAI1747_0/EVAL1748_4",
            "missing_to_promote": "MISSING_TAU_WEP_MAP;MISSING_MTS_DELTA_W_PREDICTION;MISSING_MATERIAL_MAP",
            "source_backed_bound_input": True,
        },
        {
            "eval_id": "EVAL2605_5_tau_WEP",
            "quantity": "tau_WEP",
            "definition": "branch-locked source/orbit/readout projection",
            "arena_role": "WEP product-to-Delta_w conversion",
            "current_status": "FORMAL_DEFINITION_ONLY_INPUTS_MISSING",
            "source_anchor": "EVAL1748_5/TFB1749_0",
            "missing_to_promote": "MISSING_OFFICIAL_READOUT;MISSING_SOURCE_WORLDTUBE;MISSING_MATERIAL_TENSOR;MISSING_PRODUCT_CONVENTION",
        },
        {
            "eval_id": "EVAL2605_6_tau_min",
            "quantity": "tau_min",
            "definition": "strict lower bound abs(tau_WEP)>=tau_min>0",
            "arena_role": "finite Delta_w amplitude law",
            "current_status": "NO_TAU_MIN_SOURCE",
            "source_anchor": "PZA1748_3/TFB1749_4",
            "missing_to_promote": "MISSING_ALIGNMENT_THEOREM;MISSING_NON_ORTHOGONALITY_DATA;MISSING_SOURCE",
        },
        {
            "eval_id": "EVAL2605_7_epsilon_tail",
            "quantity": "epsilon_tail",
            "definition": "hidden frame/readout/boundary/non-EH tail envelope",
            "arena_role": "tail theorem correction control",
            "current_status": "MISSING_TAIL_ENVELOPE",
            "source_anchor": "CSR2604_4/EVAL1748_7",
            "missing_to_promote": "MISSING_COMPONENT_BOUNDS;MISSING_BOUNDARY_READOUT_SILENCE",
        },
        {
            "eval_id": "EVAL2605_8_projection_norms",
            "quantity": "A_ref;N_div;N_G;N_D",
            "definition": "operator/projection/normalization bridge to observables",
            "arena_role": "observable residual vector",
            "current_status": "MISSING_OPERATOR_PROJECTION_NORMS",
            "source_anchor": "CSR2604_5/EVAL1748_8",
            "missing_to_promote": "MISSING_ARENA_OPERATOR_MAPS;MISSING_NORM_CONVENTION",
        },
        {
            "eval_id": "EVAL2605_9_wall_bound",
            "quantity": "Q_wall_grad;Q_shell_boundary",
            "definition": "finite transition-wall and boundary-shell residuals",
            "arena_role": "fallback when support intersects transition wall",
            "current_status": "BOUND_FORM_ONLY_NONCLAIM",
            "source_anchor": "TD2604_4/WBR1747",
            "missing_to_promote": "MISSING_L_WALL;MISSING_SUPPORT_OVERLAP;MISSING_C_WALL;MISSING_SHELL_PROJECTOR",
        },
        {
            "eval_id": "EVAL2605_10_DeltaK",
            "quantity": "S_Delta",
            "definition": "S_Delta^nu=-Pi_gamma[P_loc nabla_mu Delta_K^{mu nu}]",
            "arena_role": "PPN/local residual vector",
            "current_status": "SCHEMA_WRITTEN_COMPONENTS_MISSING",
            "source_anchor": "CSR2604_8/TLB2603_4",
            "missing_to_promote": "MISSING_DELTAK_COMPONENTS;MISSING_PROJECTORS;MISSING_UNITS;MISSING_OPERATOR_NORM",
        },
        {
            "eval_id": "EVAL2605_11_c_parent_zero",
            "quantity": "C_parent or action-measure owner",
            "definition": "zero theorem or finite parent coefficient in same branch",
            "arena_role": "coupling closure and local-GR reentry",
            "current_status": "MISSING_C_PARENT_OR_ZERO_CERTIFICATE",
            "source_anchor": "PZA1748_5/CPG2604_3",
            "missing_to_promote": "MISSING_COMMON_MEASURE;MISSING_CURRENT_OWNER;MISSING_NO_REPRESENTATIVE_WEIGHTS",
        },
        {
            "eval_id": "EVAL2605_12_overall",
            "quantity": "canonical local source package",
            "definition": "gap + amplitude + coupling + tau + tails + wall/projection + DeltaK rows",
            "arena_role": "local GR/Newton/PPN/R10/WEP reopening",
            "current_status": "PACKAGE_FAILS_CURRENT_CLAIM",
            "source_anchor": "2605 validator verdict",
            "missing_to_promote": "MISSING_PARENT_COEFFICIENTS;MISSING_SOURCE_SILENCE;MISSING_RESIDUAL_VECTOR",
        },
    ]
    return [
        with_stamp(
            {
                **row,
                "source_backed_bound_input": row.get("source_backed_bound_input", False),
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        for row in rows
    ]


def parent_zero_audit_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "audit_id": "PZA2605_0_tail_derivative",
            "target": "screened-tail derivative law",
            "current_status": "CONDITIONAL_THEOREM_AVAILABLE",
            "reason": "2604 derives the derivative law, but not parent ownership of mu_m2/Phi_S/source silence",
            "next_action": "retain conditional theorem; do not claim local q_loc=0",
        },
        {
            "audit_id": "PZA2605_1_gap_theorem",
            "target": "parent mass gap mu_m2",
            "current_status": "SYMBOLIC_PARENT_CONTRACT_ONLY",
            "reason": "1749 gives mu_m2=F2/(kappa_m L0^2), but kappa_m, F2, L0 and parent action provenance are unsigned",
            "next_action": "derive/source kappa_m or Z_m and F2/L0 from the parent quadratic action",
        },
        {
            "audit_id": "PZA2605_2_amplitude_theorem",
            "target": "Phi_S boundary/source amplitude",
            "current_status": "SYMBOLIC_PARENT_CONTRACT_ONLY",
            "reason": "1749 gives Phi_S=sqrt(kappa_m)*abs(A_S), but A_S, boundary class and no-growing-branch proof are unsigned",
            "next_action": "derive boundary amplitude theorem or source a finite amplitude bound",
        },
        {
            "audit_id": "PZA2605_3_coupling_zero",
            "target": "g_c=0 or beta_source beta_test zero",
            "current_status": "ZERO_THEOREM_NOT_CLOSED",
            "reason": "matter functor/action-weight/current-owner/boundary clauses remain unsigned",
            "next_action": "finite beta rows remain mandatory unless a parent zero theorem closes",
        },
        {
            "audit_id": "PZA2605_4_tau_lower_bound",
            "target": "abs(tau_WEP)>=tau_min>0",
            "current_status": "CONDITIONAL_ALIGNMENT_THEOREM_ONLY",
            "reason": "old tau branch gives a sufficient condition but not the needed alignment/source data",
            "next_action": "source tau factors or prove non-orthogonality",
        },
        {
            "audit_id": "PZA2605_5_action_measure_owner",
            "target": "single action-measure/current owner",
            "current_status": "ACTIVE_COUNTEREXAMPLE_RETAINED",
            "reason": "independent action-weight terms remain possible unless parent action excludes them",
            "next_action": "derive common measure/coframe/current descent or keep finite Delta_w",
        },
        {
            "audit_id": "PZA2605_6_verdict",
            "target": "parent-zero/source package route",
            "current_status": "NO_PARENT_ZERO_THEOREM_CLOSED_IN_2605",
            "reason": "2605 sharpens symbolic parent contracts but does not close local-GR reentry",
            "next_action": "attack kinetic coefficient and boundary amplitude ownership next",
        },
    ]
    return [with_stamp({**row, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False}) for row in rows]


def gap_bridge_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "theorem_id": "GBT2605_0_gradient_completion_to_canonical_gap",
            "route": "conditional gradient completion",
            "premise": "S_eta=-int sqrt(-g)[L0^-2 Fhat(m_*+eta)+(kappa_m/2) g^munu partial_mu eta partial_nu eta]",
            "derived_bridge": "for kappa_m>0, F2>0 and fixed L0, phi=sqrt(kappa_m) eta and mu_m2=F2/(kappa_m L0^2)",
            "promotion_status": "SYMBOLIC_PARENT_CONTRACT_ONLY",
        },
        {
            "theorem_id": "GBT2605_1_boundary_amplitude_conversion",
            "route": "conditional exponential branch",
            "premise": "eta(d)=A_S exp(-d/ell_tr)",
            "derived_bridge": "Phi_S=sqrt(kappa_m)*abs(A_S) in the canonical phi normalization",
            "promotion_status": "SYMBOLIC_PARENT_CONTRACT_ONLY",
        },
        {
            "theorem_id": "GBT2605_2_R_lock_stationary_diffusion_gap",
            "route": "R-lock stationary diffusion route",
            "premise": "D_m Delta_h delta_m - mu_B delta_m = source terms with mu_B=gamma_B lambda_R",
            "derived_bridge": "after division by D_m, the screening gap is mu_scr2=mu_B/D_m=gamma_B lambda_R/D_m",
            "promotion_status": "DIFFUSION_GAP_SEPARATED_FROM_HILBERT_MASS_GAP",
        },
        {
            "theorem_id": "GBT2605_3_PhiS_budget_law",
            "route": "source-support/boundary law",
            "premise": "M_tr <= M_bdy exp(-ell_tr/ell_scr)+M_src+M_mL+M_nl",
            "derived_bridge": "Phi_S can be bounded by a boundary/source budget only after C_phi, source support and boundary class are signed",
            "promotion_status": "BOUND_FORM_ONLY_NONCLAIM",
        },
        {
            "theorem_id": "GBT2605_4_Qalg_profile_feed",
            "route": "canonical q-profile feed",
            "premise": "nabla Gamma_eff = mu_m2 phi nabla phi + higher orders",
            "derived_bridge": "Q_alg <= A_ref^-1 mu_m2 Phi_S^2 exp(-2d/ell_tr)/ell_tr plus tails",
            "promotion_status": "BOUND_FORM_ONLY_NONCLAIM",
        },
        {
            "theorem_id": "GBT2605_5_verdict",
            "route": "2605 bridge theorem",
            "premise": "mu_m2 and Phi_S have exact symbolic parent-action contracts",
            "derived_bridge": "the current branch now knows which coefficients must be owned: kappa_m/Z_m, F2/L0 and A_S/boundary class",
            "promotion_status": "REAL_PROGRESS_NO_CLAIM_GRADE_ROW",
        },
    ]
    return [with_stamp({**row, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False}) for row in rows]


def candidate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "MPC2605_0_mu_m2_gradient",
            "quantity": "mu_m^2",
            "formula": "F2/(kappa_m L0^2)",
            "units": "length^-2",
            "route": "gradient-completion canonicalization",
            "current_status": "SYMBOLIC_PARENT_CONTRACT_ONLY",
            "missing_to_promote": "kappa_m;F2;L0;field_status;sign_units;parent_action_source",
        },
        {
            "row_id": "MPC2605_1_ell_tr_gradient",
            "quantity": "ell_tr",
            "formula": "sqrt(kappa_m L0^2/F2)",
            "units": "length",
            "route": "inverse canonical gap",
            "current_status": "SYMBOLIC_PARENT_CONTRACT_ONLY",
            "missing_to_promote": "same as mu_m2 plus positive gap",
        },
        {
            "row_id": "MPC2605_2_Phi_S_gradient",
            "quantity": "Phi_S",
            "formula": "sqrt(kappa_m)*abs(A_S)",
            "units": "canonical field units",
            "route": "boundary amplitude conversion",
            "current_status": "SYMBOLIC_PARENT_CONTRACT_ONLY",
            "missing_to_promote": "A_S;boundary_class;no_growing_branch;source_support",
        },
        {
            "row_id": "MPC2605_3_mu_scr_R_lock",
            "quantity": "mu_scr^2",
            "formula": "mu_B/D_m = gamma_B lambda_R/D_m",
            "units": "length^-2",
            "route": "stationary R-lock screening gap",
            "current_status": "SYMBOLIC_DIFFUSION_GAP_ONLY",
            "missing_to_promote": "D_m;gamma_B;lambda_R;variational_action_bridge",
        },
        {
            "row_id": "MPC2605_4_Phi_S_budget",
            "quantity": "Phi_S budget",
            "formula": "C_phi*(M_bdy exp(-ell_tr/ell_scr)+M_src+M_mL+M_nl)",
            "units": "canonical field units",
            "route": "source-support boundary amplitude law",
            "current_status": "BOUND_FORM_ONLY_NONCLAIM",
            "missing_to_promote": "C_phi;M_bdy;M_src;M_mL;M_nl;Kperp;trace_gradient",
        },
        {
            "row_id": "MPC2605_5_Qalg_feed",
            "quantity": "Q_alg profile",
            "formula": "A_ref^-1 mu_m2 Phi_S^2 exp(-2d/ell_tr)/ell_tr + tails",
            "units": "local residual units",
            "route": "observable profile feed",
            "current_status": "BOUND_FORM_ONLY_NONCLAIM",
            "missing_to_promote": "A_ref;d;epsilon_tail;projection_norms;stress_route",
        },
    ]
    return [with_stamp({**row, "symbolic_contract_ready": True, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False}) for row in rows]


def acquisition_queue_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "acq_id": "ACQ2605_0_kappa_m",
            "needed_artifact": "P_LOCAL_kappa_m_or_Zm_kinetic_coefficient.csv",
            "quantity": "kappa_m or Z_m",
            "required_fields": "parent action term; field normalization; sign; units; branch assumptions; source path",
            "route": "derivation_first",
            "priority": "highest",
        },
        {
            "acq_id": "ACQ2605_1_F2_L0",
            "needed_artifact": "P_LOCAL_F2_L0_gap_curvature_row.csv",
            "quantity": "F2/L0^2",
            "required_fields": "parent potential curvature; L0 convention; sign; units; expansion point; source path",
            "route": "derivation_first",
            "priority": "highest",
        },
        {
            "acq_id": "ACQ2605_2_A_S",
            "needed_artifact": "P_LOCAL_A_S_boundary_amplitude.csv",
            "quantity": "A_S and Phi_S",
            "required_fields": "boundary/source amplitude; exterior domain; no-growing-branch condition; uncertainty; source path",
            "route": "derivation_or_bound",
            "priority": "highest",
        },
        {
            "acq_id": "ACQ2605_3_source_silence",
            "needed_artifact": "P_LOCAL_source_silence_or_finite_J.csv",
            "quantity": "J_c;R_Xgrad;R_bdy;R_readout",
            "required_fields": "zero theorem or finite source rows; boundary/readout convention; units; source path",
            "route": "derive_or_bound",
            "priority": "highest",
        },
        {
            "acq_id": "ACQ2605_4_beta",
            "needed_artifact": "P_LOCAL_beta_source_test_row.csv",
            "quantity": "beta_source*beta_test",
            "required_fields": "source leg; test leg; normalization; units; parent coefficient or zero theorem",
            "route": "derivation_or_source",
            "priority": "highest",
        },
        {
            "acq_id": "ACQ2605_5_DeltaK",
            "needed_artifact": "P_LOCAL_DeltaK_component_operator_norm_bound.csv",
            "quantity": "S_Delta",
            "required_fields": "DeltaK components; Pi_gamma; P_loc; units; operator norm; residual limit",
            "route": "fallback_bound",
            "priority": "high_parallel",
        },
        {
            "acq_id": "ACQ2605_6_tau_min",
            "needed_artifact": "P_WEP_tau_min_lower_bound.csv",
            "quantity": "tau_min",
            "required_fields": "tau_min; confidence; derivation/source; assumptions; valid range; alignment guard",
            "route": "derivation_or_source",
            "priority": "high_fallback",
        },
        {
            "acq_id": "ACQ2605_7_projection",
            "needed_artifact": "P_LOCAL_operator_projection_norms.csv",
            "quantity": "A_ref;N_div;N_G;N_D",
            "required_fields": "arena operator maps; norm convention; uncertainty; units",
            "route": "derivation_or_numeric_bound",
            "priority": "medium",
        },
        {
            "acq_id": "ACQ2605_8_wall",
            "needed_artifact": "P_LOCAL_transition_wall_bound_inputs.csv",
            "quantity": "wall/shell residuals",
            "required_fields": "C_wall;A_S;U_B;L_wall;support overlap;projection norms",
            "route": "fallback_bound",
            "priority": "medium",
        },
    ]
    return [with_stamp({**row, "selection_status": "queued_nonclaim", "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False}) for row in rows]


def runner_refusal_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "runner_id": "RUN2605_0_package_score",
            "target": "score canonical local package",
            "verdict": "REFUSE_CLAIM_RUN",
            "failure_reasons": "MISSING_PARENT_COEFFICIENTS;MISSING_SOURCE_SILENCE;MISSING_BETA_TAU;MISSING_DELTAK;MISSING_PROJECTION_NORMS",
        },
        {
            "runner_id": "RUN2605_1_mu_phi_score",
            "target": "promote mu_m2/Phi_S symbolic bridge",
            "verdict": "REFUSE_CLAIM_RUN",
            "failure_reasons": "SYMBOLIC_CONTRACT_ONLY;MISSING_KAPPA_M;MISSING_F2;MISSING_L0;MISSING_A_S;MISSING_BOUNDARY_CLASS",
        },
        {
            "runner_id": "RUN2605_2_WEP_score",
            "target": "use Delta_w*tau bound as MTS prediction",
            "verdict": "REFUSE_CLAIM_RUN",
            "failure_reasons": "BOUND_ANCHOR_ONLY;MISSING_TAU_MAP;MISSING_DELTA_W_PREDICTION;MISSING_MATERIAL_MAP",
        },
        {
            "runner_id": "RUN2605_3_local_GR",
            "target": "local GR/Newton recovery",
            "verdict": "BLOCKED_NO_CLAIM",
            "failure_reasons": "NO_PARENT_SOURCE_PACKAGE;NO_DELTAK_BOUND;NO_FULL_PPN_VECTOR;NO_ARENA_PROJECTION",
        },
    ]
    return [with_stamp({**row, "accepted_for_scoring": False, "claim_allowed": False, "valid_for_claim": False}) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "CG2605_0_validator",
            "claim": "2605 package validator can score local rows",
            "gate_status": "BLOCKED_NO_CLAIM",
            "reason": "no accepted MTS prediction rows exist",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2605_1_bound_anchor",
            "claim": "external WEP product bound is an MTS prediction",
            "gate_status": "BLOCKED_NO_CLAIM",
            "reason": "bound anchor is source-backed input only, not a theory prediction",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2605_2_mu_phi_contract",
            "claim": "mu_m2/Phi_S bridge is parent-signed",
            "gate_status": "BLOCKED_NO_CLAIM",
            "reason": "symbolic contracts lack kappa_m/F2/L0/A_S/boundary ownership",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2605_3_beta_tau",
            "claim": "beta and tau package closes",
            "gate_status": "BLOCKED_NO_CLAIM",
            "reason": "beta legs, tau map and tau_min remain missing or conditional",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2605_4_parent_zero",
            "claim": "parent zero theorem closes local residuals",
            "gate_status": "BLOCKED_NO_CLAIM",
            "reason": "action-measure/current-owner and boundary/readout silence are unsigned",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2605_5_local_reentry",
            "claim": "local GR/Newton/PPN/R10/WEP branch can claim",
            "gate_status": "BLOCKED_NO_CLAIM",
            "reason": "local package, DeltaK and full PPN residual vector are not closed",
            "gate_pass": False,
        },
    ]
    return [with_stamp({**row, "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False}) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2605_0_validator_status",
            "decision": "package validator remains blocked for scoring",
            "reason": "2605 contains one external bound anchor and several symbolic contracts, but no claim-grade MTS prediction row",
            "effect": "do not reopen local-GR/Newton/PPN/R10/WEP scoring",
        },
        {
            "decision_id": "DEC2605_1_bridge_status",
            "decision": "accept mu_m2/Phi_S symbolic bridge as derivation contract",
            "reason": "the current branch now has exact formulas for the gap and amplitude in terms of parent coefficients",
            "effect": "stop asking vaguely for screening; hunt kappa_m/Z_m, F2/L0 and A_S/boundary class",
        },
        {
            "decision_id": "DEC2605_2_R_lock_status",
            "decision": "keep R-lock diffusion gap separated from Hilbert mass gap",
            "reason": "mu_scr2=gamma_B lambda_R/D_m is a useful screened gap but not automatically the canonical variational gap",
            "effect": "R-lock can support intuition but cannot substitute for parent kinetic ownership",
        },
        {
            "decision_id": "DEC2605_3_best_next",
            "decision": "select parent kinetic coefficient or boundary amplitude theorem",
            "reason": "the cleanest next derivation is to parent-sign kappa_m/Z_m and F2/L0, or derive Phi_S from boundary/source data",
            "effect": "2606 should attack coefficient provenance before more external WEP plumbing",
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False}) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2605_0_selected",
            "selection_status": "selected",
            "target_file": "2606-Y5-R2FR-parent-kinetic-coefficient-or-boundary-amplitude-theorem.md",
            "target_script": "scripts/Y5_R2FR_parent_kinetic_coefficient_or_boundary_amplitude_theorem_2606.py",
            "task": "try to parent-sign kappa_m/Z_m and F2/L0, or derive/source a boundary amplitude theorem for A_S/Phi_S; if neither closes, emit explicit finite residual rows",
            "success_condition": "one gap/amplitude leg becomes source-backed or parent-signed, without promoting local claims until the rest of the package closes",
            "fallback_condition": "stage official tau/readout/source/material rows only if parent coefficient route stalls",
            "guardrails": "no symbolic-contract-as-prediction; no R-lock gap as Hilbert mass gap; no local-GR claim; no GitHub; no formalization-workbench edits",
        },
        {
            "route_id": "NEXT2605_1_tau_fallback",
            "selection_status": "held_fallback",
            "target_file": "2606b-Y5-R2FR-WEP-tau-min-source-import-pack.md",
            "target_script": "scripts/Y5_R2FR_WEP_tau_min_source_import_pack_2606b.py",
            "task": "prepare official readout/source/material/product rows for tau_WEP and tau_min if derivation-first gap route stalls",
            "success_condition": "tau rows cite external sources and remain nonclaim until MTS prediction legs exist",
            "fallback_condition": "retain WEP as bound-anchor-only",
            "guardrails": "no tau=1 shortcut; no G absorption; no cancellation; no MTS prediction from external bound alone",
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False}) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for copy_id, target_path in COPY_TARGETS.items():
        source_path = OUTPUTS[copy_id]
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)
        rows.append(
            with_stamp(
                {
                    "copy_id": f"COPY2605_{copy_id}",
                    "source_path": source_path,
                    "target_path": target_path,
                    "source_exists": source_path.exists(),
                    "target_exists": target_path.exists(),
                    "valid_for_claim": False,
                }
            )
        )
    return rows


def generated_rows_have_no_claim_flags(data: dict[str, list[dict[str, Any]]]) -> bool:
    forbidden_true_fields = {
        "valid_for_claim",
        "claim_allowed",
        "score_ready",
        "accepted_for_scoring",
        "valid_prediction_row",
    }
    for rows in data.values():
        for row in rows:
            for field in forbidden_true_fields:
                if row.get(field) is True:
                    return False
    return True


def missing_rows_are_not_ready(data: dict[str, list[dict[str, Any]]]) -> bool:
    fields_to_scan = ("current_status", "missing_to_promote", "failure_reasons", "reason", "blocker")
    for rows in data.values():
        for row in rows:
            joined = ";".join(str(row.get(field, "")) for field in fields_to_scan)
            if "MISSING" in joined and (row.get("score_ready") is True or row.get("claim_allowed") is True or row.get("valid_prediction_row") is True):
                return False
    return True


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, condition: bool, notes: str, detail: str = "") -> None:
        rows.append(
            with_stamp(
                {
                    "check_id": check_id,
                    "status": "PASS" if condition else "FAIL",
                    "notes": notes,
                    "detail": detail,
                    "valid_for_claim": False,
                }
            )
        )

    add("VAL2605_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited source paths exist and needles are present")
    expected_lineage = {"LIN2605_0_2604", "LIN2605_1_1748", "LIN2605_2_1749"}
    add("VAL2605_01_lineage_complete", expected_lineage == {row["step_id"] for row in data["lineage"]}, "lineage ledger covers 2604 plus prior 1748-1749")
    add("VAL2605_02_validator_spec_guard", any(row["spec_id"] == "VSP2605_4_missing_guard" for row in data["validator_spec"]), "missing-row guard is explicit")
    expected_eval = {"mu_m^2", "Phi_S", "beta_source*beta_test", "tau_WEP", "S_Delta", "canonical local source package"}
    add("VAL2605_03_package_eval_complete", expected_eval.issubset({row["quantity"] for row in data["package_evaluation"]}), "package evaluation covers gap, amplitude, beta, tau, DeltaK and overall verdict")
    add("VAL2605_04_bound_anchor_safe", any(row["eval_id"] == "EVAL2605_4_delta_w_tau_bound" and row["source_backed_bound_input"] is True and row["valid_prediction_row"] is False for row in data["package_evaluation"]), "external bound anchor retained as nonprediction only")
    expected_zero = {"PZA2605_1_gap_theorem", "PZA2605_2_amplitude_theorem", "PZA2605_3_coupling_zero", "PZA2605_6_verdict"}
    add("VAL2605_05_parent_zero_audit_complete", expected_zero.issubset({row["audit_id"] for row in data["parent_zero_audit"]}), "parent zero/source audit covers gap, amplitude, coupling and verdict")
    expected_bridge = {"GBT2605_0_gradient_completion_to_canonical_gap", "GBT2605_1_boundary_amplitude_conversion", "GBT2605_5_verdict"}
    add("VAL2605_06_gap_bridge_recorded", expected_bridge.issubset({row["theorem_id"] for row in data["gap_bridge"]}), "symbolic gap/amplitude bridge theorem is recorded")
    expected_candidates = {"MPC2605_0_mu_m2_gradient", "MPC2605_2_Phi_S_gradient", "MPC2605_5_Qalg_feed"}
    add("VAL2605_07_candidate_rows_nonclaim", expected_candidates.issubset({row["row_id"] for row in data["candidate_rows"]}) and all(row["valid_prediction_row"] is False for row in data["candidate_rows"]), "mu/Phi candidate rows exist and remain nonclaim")
    add("VAL2605_08_acquisition_queue_ready", len(data["acquisition_queue"]) >= 8 and all(row["claim_allowed"] is False for row in data["acquisition_queue"]), "acquisition queue is populated and nonclaim")
    add("VAL2605_09_runner_refuses", all(row["accepted_for_scoring"] is False and row["claim_allowed"] is False for row in data["runner_refusal"]), "all runners refuse scoring")
    add("VAL2605_10_claim_gates_safe", all(row["claim_allowed"] is False and row["gate_pass"] is False for row in data["claim_gates"]), "all claim gates remain blocked")
    add("VAL2605_11_no_claim_flags", generated_rows_have_no_claim_flags(data), "no generated row promotes scoring or claim flags")
    add("VAL2605_12_missing_not_ready", missing_rows_are_not_ready(data), "no MISSING_* row is marked ready")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in (
            "*2605-Y5-R2FR-gap-beta*",
            "*Y5_R2FR_gap_beta_tau*2605*",
            "*P8_Y5_PACKAGE_VALIDATOR_REBASE_2605*",
            "*JR2605*",
        ):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add("VAL2605_13_no_formalization_artifacts", not formalization_artifacts, "no 2605 artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_artifacts))
    add("VAL2605_14_next_selected", any(row["route_id"] == "NEXT2605_0_selected" and "2606-Y5-R2FR-parent-kinetic-coefficient" in row["target_file"] for row in data["next"]), "2606 kinetic coefficient or boundary amplitude theorem selected")
    add("VAL2605_15_branch_copies", all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]), "nonclaim branch copies exist")

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2605_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2605_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2605_OVERALL",
        overall,
        "2605 rebases the gap-beta-tau validator, imports the symbolic mu/Phi bridge, blocks claims, and selects kinetic coefficient/boundary amplitude next",
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for row in rows:
        values = [row_value(row.get(column, "")).replace("\n", " ").replace("|", "/") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2605 Y5 R2FR gap beta tau source package validator or parent row",
        "",
        "**Status:** private nonclaim rebase checkpoint. The current 2604 tail theorem is fed into the gap-beta-tau package validator, and the earlier 1749 symbolic gap/amplitude bridge is imported so the next derivation target is no longer vague.",
        "",
        "**Main result:** the local branch still cannot claim GR/Newton/PPN/R10/WEP recovery, but it has moved forward. The package validator remains blocked because no complete MTS prediction row exists; however, the parent gap/amplitude route now has exact symbolic contracts: `mu_m2=F2/(kappa_m L0^2)`, `ell_tr=sqrt(kappa_m L0^2/F2)`, and `Phi_S=sqrt(kappa_m)*abs(A_S)`. The next real bottleneck is parent-signing `kappa_m/Z_m`, `F2/L0`, and the boundary amplitude `A_S/Phi_S`, while keeping beta, tau, projection, wall and `DeltaK` rows explicit.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role", "valid_for_claim"]),
        "",
        "## Lineage Ledger",
        markdown_table(data["lineage"], ["step_id", "checkpoint", "question", "result", "status", "next_dependency", "valid_for_claim", "claim_allowed"]),
        "",
        "## Validator Spec",
        markdown_table(data["validator_spec"], ["spec_id", "field_or_gate", "requirement", "failure_rule", "valid_for_claim"]),
        "",
        "## Current Package Evaluation",
        markdown_table(data["package_evaluation"], ["eval_id", "quantity", "definition", "arena_role", "current_status", "source_anchor", "missing_to_promote", "source_backed_bound_input", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Parent Zero Or Source Audit",
        markdown_table(data["parent_zero_audit"], ["audit_id", "target", "current_status", "reason", "next_action", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Gap Amplitude Bridge Theorem",
        markdown_table(data["gap_bridge"], ["theorem_id", "route", "premise", "derived_bridge", "promotion_status", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Mu Phi Candidate Rows",
        markdown_table(data["candidate_rows"], ["row_id", "quantity", "formula", "units", "route", "current_status", "missing_to_promote", "symbolic_contract_ready", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Acquisition Queue",
        markdown_table(data["acquisition_queue"], ["acq_id", "needed_artifact", "quantity", "required_fields", "route", "priority", "selection_status", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Runner Refusal",
        markdown_table(data["runner_refusal"], ["runner_id", "target", "verdict", "failure_reasons", "accepted_for_scoring", "claim_allowed", "valid_for_claim"]),
        "",
        "## Claim Gates",
        markdown_table(data["claim_gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect", "valid_for_claim"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "success_condition", "fallback_condition", "guardrails", "valid_for_claim"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists", "valid_for_claim"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail", "valid_for_claim"]),
        "",
        "## Practical Status",
        "",
        "This is the useful kind of narrowing. We did not solve the coupling problem, but we changed it from fog into a hit list. The theory now has a clear local route: sign the kinetic/gap coefficient and boundary amplitude, or keep the finite residual branch honest. No haymaker, no fake knockout; but that is a clean counterpunch.",
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)

    data = {
        "sources": source_register_rows(),
        "lineage": lineage_rows(),
        "validator_spec": validator_spec_rows(),
        "package_evaluation": package_evaluation_rows(),
        "parent_zero_audit": parent_zero_audit_rows(),
        "gap_bridge": gap_bridge_rows(),
        "candidate_rows": candidate_rows(),
        "acquisition_queue": acquisition_queue_rows(),
        "runner_refusal": runner_refusal_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["lineage_ledger"], data["lineage"])
    write_csv(OUTPUTS["validator_spec"], data["validator_spec"])
    write_csv(OUTPUTS["package_evaluation"], data["package_evaluation"])
    write_csv(OUTPUTS["parent_zero_audit"], data["parent_zero_audit"])
    write_csv(OUTPUTS["gap_bridge"], data["gap_bridge"])
    write_csv(OUTPUTS["candidate_rows"], data["candidate_rows"])
    write_csv(OUTPUTS["acquisition_queue"], data["acquisition_queue"])
    write_csv(OUTPUTS["runner_refusal"], data["runner_refusal"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])

    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])

    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)

    overall = next(row for row in data["validations"] if row["check_id"] == "VAL2605_OVERALL")
    print(f"{overall['check_id']} {overall['status']}: {overall['notes']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

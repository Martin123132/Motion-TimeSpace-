from __future__ import annotations

import csv
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_PARENT_BREF_SELECTOR_VARIATIONAL_EQUATION_OR_FINITE_COEFFICIENT_ROW_2453"
CHECKPOINT_ID = "2453"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
HAMILTONIAN = ROOT / "source-intake" / "hamiltonian-source"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"

DOC = ROOT / "2453-Y5-R2FR-parent-Bref-selector-variational-equation-or-finite-coefficient-row.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2453_SOURCE_REGISTER.csv",
    "selector_theorem": OUT / "P8_Y5_PARENT_QLOC_2453_PARENT_BREF_SELECTOR_VARIATIONAL_THEOREM.csv",
    "clause_audit": OUT / "P8_Y5_PARENT_QLOC_2453_SELECTOR_CLAUSE_AUDIT.csv",
    "ift_derivation": OUT / "P8_Y5_PARENT_QLOC_2453_IMPLICIT_FUNCTION_DERIVATION.csv",
    "finite_rows": OUT / "P8_Y5_PARENT_QLOC_2453_FINITE_COEFFICIENT_ROW_TEMPLATE.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2453_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_PARENT_QLOC_2453_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2453_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2453_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2453_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_theorem": QUEUE / "JR2453_PARENT_BREF_SELECTOR_VARIATIONAL_THEOREM_NONCLAIM.csv",
    "queue_coefficients": QUEUE / "JR2453_DELTA_REF_Q_SOURCE_FINITE_COEFFICIENT_TEMPLATE_NONCLAIM.csv",
    "hamiltonian_selector": HAMILTONIAN / "parent_Bref_selector_variational_theorem_2453_NONCLAIM.csv",
    "local_coefficients": LOCAL_BOUNDS / "Delta_ref_q_source_finite_coefficient_template_2453_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2453_00_2452_doc",
        "source_path": ROOT / "2452-Y5-R2FR-Delta-ref-q-source-strict-provenance-runner.md",
        "needles": ["NEXT2452_0_selected", "GATE2452_0_live_Delta_ref_q_source_rows", "VAL2452_OVERALL"],
        "role": "fresh handoff selecting the parent B_ref selector target",
    },
    {
        "source_id": "SRC2453_01_2452_runner",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2452_STRICT_PROVENANCE_RUNNER.csv",
        "needles": ["CIR2452_live_DCP2451_0_partial_q_derivative", "SMOKE_COMPUTED_NONCLAIM", "REFUSED_CURRENT_ROW"],
        "role": "strict runner whose rows future coefficients must pass",
    },
    {
        "source_id": "SRC2453_02_2451_contract",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2451_PARENT_SELECTOR_CONTRACT.csv",
        "needles": ["FBC2451_0_selector_function", "FBC2451_2_q_source_blind_derivatives", "MISSING_PARENT_SELECTOR"],
        "role": "machine-readable parent selector contract",
    },
    {
        "source_id": "SRC2453_03_2451_selector_attempt",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2451_BREF_FIXED_BRANCH_SELECTOR_ATTEMPT.csv",
        "needles": ["FBS2451_8_verdict", "FAIL_CURRENT_CLAIM", "parent-owned Sigma_ref"],
        "role": "failed fixed-branch selector attempt",
    },
    {
        "source_id": "SRC2453_04_2449_chain_rule",
        "source_path": ROOT / "2449-Y5-R2FR-Bref-derivative-vector-theorem-or-Delta-ref-source-row-for-S-Eq.md",
        "needles": ["BDT2449_1_chain_rule_zero", "DVC2449_0_q", "VAL2449_OVERALL"],
        "role": "conditional chain-rule theorem for B_ref derivative zero",
    },
    {
        "source_id": "SRC2453_05_2448_owner",
        "source_path": ROOT / "2448-Y5-R2FR-relative-boundary-class-and-Bref-owner-or-S-Eq-boundary-source-bound-pack.md",
        "needles": ["RBO2448_0_parent_boundary_action", "RBO2448_6_Bref_derivative_vector", "VAL2448_OVERALL"],
        "role": "relative boundary and B_ref owner contract",
    },
    {
        "source_id": "SRC2453_06_1009_parent_chain",
        "source_path": ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
        "needles": ["PCS1009_3_boundary_reference", "fixed_reference_missing", "CG1009_4_PiM_source_measure"],
        "role": "older parent current-chain contract and boundary reference gap",
    },
    {
        "source_id": "SRC2453_07_1018_owner_map",
        "source_path": ROOT / "1018-Y5-R10-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md",
        "needles": ["LOC1018_4_Bref_owner", "sector Lagrangian/boundary owner map", "CG1018_1_LX_owned"],
        "role": "older owner-map lock for B_ref and local-GR branch",
    },
    {
        "source_id": "SRC2453_08_1016_worldtube",
        "source_path": ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
        "needles": ["PSC1016_9_verdict", "W_source := closure(supp J_H[tau])", "fail_current_claim"],
        "role": "same-frame source/worldtube selector precedent",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def truth(value: bool) -> str:
    return "True" if value else "False"


def metadata(valid_for_claim: bool = False, claim_allowed: bool = False) -> dict[str, str]:
    return {
        "timestamp_utc": stamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": truth(valid_for_claim),
        "claim_allowed": truth(claim_allowed),
    }


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def cell(value: Any) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def table(columns: list[str], rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(cell(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        missing = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            {
                **metadata(),
                "source_id": source["source_id"],
                "source_path": str(path),
                "exists": truth(path.exists()),
                "needles": ";".join(source["needles"]),
                "missing_needles": ";".join(missing),
                "source_pass": truth(path.exists() and not missing),
                "role": source["role"],
            }
        )
    return rows


def selector_theorem_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "theorem_id": "PBT2453_0_parent_reference_functional",
            "claim": "define a reference-selector functional I_ref[Sigma;Phi]",
            "mathematical_form": "I_ref[Sigma;Phi]=I_boundary[gamma_Sigma,tau_Sigma,C_top,B_ct]+sum_A lambda_A C_A[Sigma;Pi_ref(Phi)]",
            "proof_step": "Sigma_ref is not chosen from data; it is a stationary point of a parent reference functional",
            "current_status": "CANDIDATE_FORM_WRITTEN_NOT_PARENT_SIGNED",
            "missing_signature": "explicit parent I_ref, Pi_ref, constraint set C_A, and allowed boundary variations",
            "would_close": "fixed-branch selector definition",
            "accepted_for_claim": "False",
        },
        {
            "theorem_id": "PBT2453_1_selector_equation",
            "claim": "Sigma_ref is selected by a variational equation",
            "mathematical_form": "E_Sigma := delta I_ref/delta Sigma = 0 with boundary/corner constraints C_A=0",
            "proof_step": "a fixed reference branch follows from Euler/stationarity/topological equations, not readout fitting",
            "current_status": "CONDITIONAL_EQUATION",
            "missing_signature": "source path/equation reference for E_Sigma=0 in the parent action",
            "would_close": "FBC2451_1 variation_or_constraint",
            "accepted_for_claim": "False",
        },
        {
            "theorem_id": "PBT2453_2_q_source_blind_inputs",
            "claim": "I_ref has no explicit q/source/material/readout slots",
            "mathematical_form": "D_q I_ref = D_source I_ref = D_{GM_obs,M_fit,kappa_A,composition_A} I_ref = 0 at fixed Sigma",
            "proof_step": "if the reference functional only sees parent quotient/topological data, q/source derivatives cannot enter explicitly",
            "current_status": "REQUIRED_NOT_SIGNED",
            "missing_signature": "parent projection Pi_ref proving q/source/material labels are absent",
            "would_close": "no-marker and no-GM clauses",
            "accepted_for_claim": "False",
        },
        {
            "theorem_id": "PBT2453_3_non_degenerate_selector",
            "claim": "the selector equation has an isolated branch modulo gauge",
            "mathematical_form": "H_Sigma := D_Sigma E_Sigma is invertible on the quotient ker(gauge)^perp",
            "proof_step": "implicit-function theorem is legal only after gauge directions and branch degeneracy are removed",
            "current_status": "REQUIRED_NOT_SIGNED",
            "missing_signature": "Hessian/nondegeneracy certificate and branch uniqueness domain",
            "would_close": "prevents drift to q/source-dependent nearby branches",
            "accepted_for_claim": "False",
        },
        {
            "theorem_id": "PBT2453_4_IFT_derivative_zero",
            "claim": "q/source derivatives of Sigma_ref vanish",
            "mathematical_form": "D_a Sigma_ref = - H_Sigma^{-1} D_a E_Sigma = 0 for a in {q,source}",
            "proof_step": "if PBT2453_2 and PBT2453_3 hold, D_a E_Sigma=0 and therefore D_a Sigma_ref=0",
            "current_status": "CONDITIONAL_THEOREM_PROVED_AS_CONTRACT",
            "missing_signature": "depends on unsigned PBT2453_2 and PBT2453_3",
            "would_close": "FBC2451_2 q/source blind derivatives",
            "accepted_for_claim": "False",
        },
        {
            "theorem_id": "PBT2453_5_Bref_derivative_zero",
            "claim": "B_ref is q/source-blind",
            "mathematical_form": "D_a B_ref = (delta B_ref/delta Sigma_ref) D_a Sigma_ref + (partial_a B_ref)_Sigma = 0",
            "proof_step": "composition with q/source-blind Sigma_ref plus no explicit q/source B_ref slot kills the derivative",
            "current_status": "CONDITIONAL_THEOREM_PROVED_AS_CONTRACT",
            "missing_signature": "needs B_ref=B_ref[Sigma_ref] and no explicit q/source counterterm slot",
            "would_close": "partial_q Delta_ref=partial_source Delta_ref=0",
            "accepted_for_claim": "False",
        },
        {
            "theorem_id": "PBT2453_6_same_frame_normalization",
            "claim": "Delta_ref/N_E becomes meaningful in the same frame",
            "mathematical_form": "tau_ref=tau_Q=tau_source and N_E=Q_tau[Sigma_ref]>0 before readout",
            "proof_step": "the zero theorem can feed the local residual only if the denominator and reference use one parent coframe/time generator",
            "current_status": "REQUIRED_NOT_SIGNED",
            "missing_signature": "same-frame N_E/Q_tau/Hamiltonian source certificate",
            "would_close": "Delta_ref q/source component normalization",
            "accepted_for_claim": "False",
        },
        {
            "theorem_id": "PBT2453_7_verdict",
            "claim": "parent B_ref selector variational theorem is a current MTS theorem",
            "mathematical_form": "PBT2453_0 through PBT2453_6 signed => D_q B_ref=D_source B_ref=0",
            "proof_step": "the route is mathematically viable, but current corpus has not supplied the parent projection, Hessian, counterterm, or N_E signatures",
            "current_status": "FAIL_CURRENT_CLAIM_BUT_DERIVATION_ROUTE_IDENTIFIED",
            "missing_signature": "Pi_ref/no-marker, Hessian branch uniqueness, counterterm convention, same-frame N_E",
            "would_close": "Delta_ref q/source theorem-zero route",
            "accepted_for_claim": "False",
        },
    ]
    return [{**metadata(), **row} for row in rows]


def clause_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("CLA2453_0_parent_Iref", "parent reference functional I_ref", "MISSING_PARENT_REFERENCE_FUNCTIONAL", "must be written as a parent action/constraint, not a narrative selector"),
        ("CLA2453_1_Piref", "projection Pi_ref removing q/source/readout slots", "MISSING_PARENT_PROJECTION", "needed for D_q I_ref=D_source I_ref=0"),
        ("CLA2453_2_allowed_variations", "allowed boundary/corner variations", "MISSING_VARIATION_DOMAIN", "prevents changing the surface class after readout"),
        ("CLA2453_3_Hessian", "H_Sigma invertible modulo gauge", "MISSING_HESSIAN_CERTIFICATE", "needed for implicit-function derivative zero"),
        ("CLA2453_4_no_marker", "no source/material marker clause", "MISSING_NO_MARKER_SELECTOR_CLAUSE", "excludes composition/source-labelled reference choice"),
        ("CLA2453_5_no_GM", "no observed-GM/fitted denominator import", "MISSING_NO_GM_CALIBRATION_CERTIFICATE", "prevents reference subtraction absorbing source mass"),
        ("CLA2453_6_counterterm", "counterterm convention fixed before readout", "MISSING_COUNTERTERM_CONVENTION", "blocks q/source counterterm cancellation"),
        ("CLA2453_7_same_frame_NE", "positive same-frame N_E", "MISSING_SAME_FRAME_N_E", "normalizes Delta_ref without orbital-GM shortcut"),
        ("CLA2453_8_source_path", "source paths/equation refs for all clauses", "MISSING_SOURCE_PATHS", "required before any row can become valid_for_claim=true"),
    ]
    return [
        {
            **metadata(),
            "clause_id": clause_id,
            "required_clause": required,
            "current_fill": current,
            "why_it_matters": why,
            "status": "BLOCKED_NONCLAIM",
        }
        for clause_id, required, current, why in rows
    ]


def ift_derivation_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "step_id": "IFT2453_0_stationary_equation",
            "statement": "E_Sigma(Sigma_ref, x)=0 where x denotes q/source/readout parameters",
            "derivation": "selector equation is posed before readout",
            "requires": "PBT2453_0 and PBT2453_1",
            "result": "formal stationary branch",
            "claim_status": "conditional",
        },
        {
            "step_id": "IFT2453_1_differentiate",
            "statement": "D_x E_Sigma + H_Sigma D_x Sigma_ref = 0",
            "derivation": "differentiate the selector equation with respect to x",
            "requires": "smooth branch and allowed variation domain",
            "result": "linear response equation",
            "claim_status": "conditional",
        },
        {
            "step_id": "IFT2453_2_cross_derivative_zero",
            "statement": "D_q E_Sigma = D_source E_Sigma = 0",
            "derivation": "follows if I_ref depends only on Pi_ref(Phi) and Pi_ref is q/source/readout blind",
            "requires": "PBT2453_2 parent projection/no-marker clause",
            "result": "no forcing term in selector response",
            "claim_status": "unsigned_current_MTS",
        },
        {
            "step_id": "IFT2453_3_invert_Hessian",
            "statement": "D_x Sigma_ref = -H_Sigma^{-1}D_x E_Sigma",
            "derivation": "implicit-function theorem after quotienting gauge directions",
            "requires": "PBT2453_3 Hessian/nondegeneracy certificate",
            "result": "D_q Sigma_ref=D_source Sigma_ref=0 if IFT2453_2 holds",
            "claim_status": "unsigned_current_MTS",
        },
        {
            "step_id": "IFT2453_4_chain_to_Bref",
            "statement": "D_x B_ref = B_ref,_Sigma D_x Sigma_ref + partial_x B_ref|Sigma",
            "derivation": "chain rule for B_ref[Sigma_ref]",
            "requires": "B_ref has no explicit q/source/counterterm slot",
            "result": "D_q B_ref=D_source B_ref=0",
            "claim_status": "conditional_theorem",
        },
        {
            "step_id": "IFT2453_5_local_residual_feed",
            "statement": "Delta_ref_q_source_over_N_E=0 only after same-frame N_E is signed",
            "derivation": "zero numerator must be normalized in the same Hamiltonian/coframe frame",
            "requires": "PBT2453_6",
            "result": "still blocked for current local-GR claim",
            "claim_status": "blocked_nonclaim",
        },
    ]
    return [{**metadata(), **row} for row in rows]


def finite_coefficient_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "FCR2453_0_partial_q_Delta_ref",
            "target_runner": "P8_Y5_PARENT_QLOC_2452_STRICT_PROVENANCE_RUNNER.csv",
            "field_bundle": "q_parameter;partial_q_Delta_ref;partial_q_units;Delta_q_scale;Delta_q_scale_units;source_path;equation_ref",
            "acceptance_rule": "finite numeric derivative or PARENT_SIGNED_TRUE theorem-zero; no MISSING markers",
            "current_value": "MISSING_NUMERIC_DERIVATIVE_OR_PARENT_SIGNED_ZERO",
            "score_ready": "False",
        },
        {
            "row_id": "FCR2453_1_partial_source_Delta_ref",
            "target_runner": "P8_Y5_PARENT_QLOC_2452_STRICT_PROVENANCE_RUNNER.csv",
            "field_bundle": "source_parameter;partial_source_Delta_ref;partial_source_units;Delta_source_scale;Delta_source_scale_units;source_path;equation_ref",
            "acceptance_rule": "finite numeric derivative or PARENT_SIGNED_TRUE theorem-zero; no MISSING markers",
            "current_value": "MISSING_NUMERIC_DERIVATIVE_OR_PARENT_SIGNED_ZERO",
            "score_ready": "False",
        },
        {
            "row_id": "FCR2453_2_Bref_rule",
            "target_runner": "P8_Y5_PARENT_QLOC_2452_STRICT_PROVENANCE_RUNNER.csv",
            "field_bundle": "B_ref_rule;fixed_branch_id;counterterm_convention;source_path;equation_ref",
            "acceptance_rule": "parent-owned fixed branch before q/source/readout; no observed-GM or fitted-source labels",
            "current_value": "MISSING_PARENT_BREF_RULE",
            "score_ready": "False",
        },
        {
            "row_id": "FCR2453_3_N_E",
            "target_runner": "P8_Y5_PARENT_QLOC_2452_STRICT_PROVENANCE_RUNNER.csv",
            "field_bundle": "N_E;N_E_units;denominator_origin;tau_id;coframe_id;source_path;equation_ref",
            "acceptance_rule": "finite positive same-frame denominator; no orbital-GM import",
            "current_value": "MISSING_SAME_FRAME_N_E",
            "score_ready": "False",
        },
        {
            "row_id": "FCR2453_4_component_sum",
            "target_runner": "P8_Y5_PARENT_QLOC_2452_STRICT_PROVENANCE_RUNNER.csv",
            "field_bundle": "abs(partial_q*Delta_q)+abs(partial_source*Delta_source) over N_E",
            "acceptance_rule": "absolute component sum with ABS_COMPONENT_SUM_NO_SIGN_CANCELLATION",
            "current_value": "MISSING_COMPONENT_INPUTS",
            "score_ready": "False",
        },
    ]
    return [{**metadata(), **row} for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GATE2453_0_conditional_derivation",
            "claim": "conditional parent-selector derivation is mathematically valid",
            "gate_status": "PASS_AS_CONTRACT",
            "reason": "implicit-function theorem route is explicit and identifies the required hypotheses",
            "gate_pass": "True",
        },
        {
            "gate_id": "GATE2453_1_current_selector_theorem",
            "claim": "current MTS has parent-signed B_ref/Sigma_ref selector",
            "gate_status": "BLOCKED",
            "reason": "Pi_ref/no-marker, Hessian, counterterm convention and same-frame N_E are missing",
            "gate_pass": "False",
        },
        {
            "gate_id": "GATE2453_2_q_source_zero",
            "claim": "partial_q Delta_ref=partial_source Delta_ref=0 is current theorem",
            "gate_status": "BLOCKED",
            "reason": "zero theorem depends on unsigned parent selector clauses",
            "gate_pass": "False",
        },
        {
            "gate_id": "GATE2453_3_finite_coefficient_fallback",
            "claim": "finite q/source coefficient rows can be scored now",
            "gate_status": "BLOCKED",
            "reason": "finite coefficient rows are templates with MISSING values",
            "gate_pass": "False",
        },
        {
            "gate_id": "GATE2453_4_local_GR",
            "claim": "Delta_ref/RCS2446_0/S_Eq/PPN/local-GR branch passes",
            "gate_status": "BLOCKED",
            "reason": "2453 supplies a derivation route, not a signed parent action or numerical bound",
            "gate_pass": "False",
        },
    ]
    return [{**metadata(), **row} for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2453_0_route_found",
            "decision": "keep the variational selector route",
            "reason": "the IFT chain gives a real derivation path for D_q B_ref=D_source B_ref=0",
            "effect": "do not demote B_ref selector to pure closure yet",
        },
        {
            "decision_id": "DEC2453_1_no_promotion",
            "decision": "do not promote current MTS selector theorem",
            "reason": "projection, Hessian, no-marker, counterterm and N_E certificates are missing",
            "effect": "Delta_ref q/source theorem-zero remains blocked",
        },
        {
            "decision_id": "DEC2453_2_fallback_ready",
            "decision": "keep finite coefficient fallback rows",
            "reason": "if the parent selector route fails, 2452 can score source-backed q/source coefficient rows",
            "effect": "future work has both a proof route and a data/provenance route",
        },
        {
            "decision_id": "DEC2453_3_next",
            "decision": "attack parent projection and Hessian certificates next",
            "reason": "these are the decisive unsigned hypotheses in the IFT proof",
            "effect": "2454 should try to construct Pi_ref and H_Sigma or demote selector route to finite-row-only",
        },
    ]
    return [{**metadata(), **row} for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            **metadata(),
            "route_id": "NEXT2453_0_selected",
            "selection_status": "selected",
            "target_file": "2454-Y5-R2FR-reference-projection-Hessian-certificate-or-selector-demotion.md",
            "target_script": "scripts/Y5_R2FR_reference_projection_Hessian_certificate_or_selector_demotion_2454.py",
            "task": "construct the parent projection Pi_ref and Hessian/nondegeneracy certificate needed by the 2453 implicit-function selector theorem, or demote B_ref selector zero route to finite coefficient sourcing only",
            "acceptance_target": "Pi_ref must be q/source/readout blind, marker-free, no observed-GM, and H_Sigma invertible modulo gauge; otherwise no theorem-zero promotion",
            "guardrails": "do not claim Delta_ref/RCS2446_0/S_Eq/local-GR; do not edit formalization-workbench; do not push GitHub",
        }
    ]


def copy_outputs() -> list[dict[str, Any]]:
    for target in COPY_TARGETS.values():
        target.parent.mkdir(parents=True, exist_ok=True)
    specs = [
        ("queue_theorem", OUTPUTS["selector_theorem"], COPY_TARGETS["queue_theorem"]),
        ("queue_coefficients", OUTPUTS["finite_rows"], COPY_TARGETS["queue_coefficients"]),
        ("hamiltonian_selector", OUTPUTS["selector_theorem"], COPY_TARGETS["hamiltonian_selector"]),
        ("local_coefficients", OUTPUTS["finite_rows"], COPY_TARGETS["local_coefficients"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in specs:
        if source.exists():
            shutil.copyfile(source, target)
        rows.append(
            {
                **metadata(),
                "copy_id": copy_id,
                "source_path": str(source),
                "target_path": str(target),
                "source_exists": truth(source.exists()),
                "target_exists": truth(target.exists()),
            }
        )
    return rows


def formalization_marker_hits() -> list[str]:
    if not FORMALIZATION.exists():
        return []
    markers = ["2453-", "_2453", "2453_", "P8_Y5_PARENT_QLOC_2453", "P8_Y5_BRR545_2453"]
    hits: list[str] = []
    for dirpath, _, filenames in os.walk(FORMALIZATION):
        for filename in filenames:
            if any(marker in filename for marker in markers):
                hits.append(str(Path(dirpath) / filename))
    return hits


def csv_parse_ok(path: Path) -> tuple[bool, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
    except Exception as exc:
        return False, repr(exc)
    return True, f"CSV parses with {len(rows)} rows"


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_ok = all(row["source_pass"] == "True" for row in data["source_register"])
    theorem_ids = {row["theorem_id"] for row in data["selector_theorem"]}
    required_theorem_ids = {
        "PBT2453_0_parent_reference_functional",
        "PBT2453_2_q_source_blind_inputs",
        "PBT2453_3_non_degenerate_selector",
        "PBT2453_4_IFT_derivative_zero",
        "PBT2453_7_verdict",
    }
    ift_ok = any(row["step_id"] == "IFT2453_4_chain_to_Bref" and row["claim_status"] == "conditional_theorem" for row in data["ift_derivation"])
    verdict_ok = any(row["theorem_id"] == "PBT2453_7_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM_BUT_DERIVATION_ROUTE_IDENTIFIED" for row in data["selector_theorem"])
    clauses_blocked = all(row["status"] == "BLOCKED_NONCLAIM" and str(row["current_fill"]).startswith("MISSING") for row in data["clause_audit"])
    finite_rows_blocked = all(row["score_ready"] == "False" and str(row["current_value"]).startswith("MISSING") for row in data["finite_rows"])
    claims_safe = all(row["claim_allowed"] == "False" for row in data["claim_gates"]) and any(row["gate_id"] == "GATE2453_0_conditional_derivation" and row["gate_pass"] == "True" for row in data["claim_gates"])
    next_ok = bool(data["next_target"]) and data["next_target"][0]["route_id"] == "NEXT2453_0_selected"
    copies_ok = all(row["target_exists"] == "True" for row in data["branch_copies"])
    no_formalization = not formalization_marker_hits()

    checks: list[dict[str, Any]] = [
        {"check_id": "VAL2453_00_sources_exist", "status": "PASS" if source_ok else "FAIL", "notes": "all cited source paths exist and needles are present", "detail": ""},
        {"check_id": "VAL2453_01_theorem_rows_present", "status": "PASS" if required_theorem_ids.issubset(theorem_ids) else "FAIL", "notes": "parent selector theorem rows cover functional/projection/Hessian/IFT/verdict", "detail": ""},
        {"check_id": "VAL2453_02_IFT_derivation_written", "status": "PASS" if ift_ok else "FAIL", "notes": "implicit-function chain-to-B_ref step is explicit", "detail": ""},
        {"check_id": "VAL2453_03_current_claim_not_promoted", "status": "PASS" if verdict_ok else "FAIL", "notes": "selector theorem is conditional and not promoted", "detail": ""},
        {"check_id": "VAL2453_04_missing_clauses_blocked", "status": "PASS" if clauses_blocked else "FAIL", "notes": "projection/Hessian/no-marker/counterterm/N_E clauses remain missing-marked", "detail": ""},
        {"check_id": "VAL2453_05_finite_rows_blocked", "status": "PASS" if finite_rows_blocked else "FAIL", "notes": "finite coefficient fallback rows remain templates", "detail": ""},
        {"check_id": "VAL2453_06_claim_gates_safe", "status": "PASS" if claims_safe else "FAIL", "notes": "conditional derivation passes only as contract; local-GR claims remain blocked", "detail": ""},
        {"check_id": "VAL2453_07_next_target_written", "status": "PASS" if next_ok else "FAIL", "notes": "2454 projection/Hessian certificate target selected", "detail": ""},
        {"check_id": "VAL2453_08_branch_copies", "status": "PASS" if copies_ok else "FAIL", "notes": "nonclaim branch copies exist", "detail": ""},
        {"check_id": "VAL2453_09_no_formalization_artifacts", "status": "PASS" if no_formalization else "FAIL", "notes": "no 2453 artifacts were written to formalization-workbench", "detail": ";".join(formalization_marker_hits()[:10])},
    ]
    csv_outputs = [
        OUTPUTS["source_register"],
        OUTPUTS["selector_theorem"],
        OUTPUTS["clause_audit"],
        OUTPUTS["ift_derivation"],
        OUTPUTS["finite_rows"],
        OUTPUTS["claim_gates"],
        OUTPUTS["decisions"],
        OUTPUTS["next_target"],
        OUTPUTS["branch_copies"],
    ]
    for path in csv_outputs:
        ok, detail = csv_parse_ok(path)
        checks.append(
            {
                "check_id": f"VAL2453_CSV_{path.stem}",
                "status": "PASS" if ok else "FAIL",
                "notes": detail,
                "detail": str(path),
            }
        )
    overall = all(row["status"] == "PASS" for row in checks)
    checks.append(
        {
            "check_id": "VAL2453_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "notes": "2453 proves the parent B_ref selector route as a conditional IFT contract but keeps current claims blocked",
            "detail": "",
        }
    )
    return [{**metadata(), **row} for row in checks]


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    content = f"""# 2453 Y5 R2FR Parent B_ref Selector Variational Equation Or Finite Coefficient Row

**Status:** derivation route identified but not promoted. The parent `B_ref/Sigma_ref` selector can kill q/source derivatives by an implicit-function theorem, but current MTS has not signed the parent projection, Hessian, counterterm, or same-frame `N_E` clauses.

**Private reading:** this is a real narrowing. We are not merely circling: the local-GR route now has a precise proof path and a precise fallback if the proof path fails.

## Source Register
{table(["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"], data["source_register"])}

## Parent B_ref Selector Variational Theorem
{table(["theorem_id", "claim", "mathematical_form", "proof_step", "current_status", "missing_signature", "would_close", "accepted_for_claim"], data["selector_theorem"])}

## Selector Clause Audit
{table(["clause_id", "required_clause", "current_fill", "why_it_matters", "status"], data["clause_audit"])}

## Implicit-Function Derivation
{table(["step_id", "statement", "derivation", "requires", "result", "claim_status"], data["ift_derivation"])}

## Finite Coefficient Fallback Rows
{table(["row_id", "target_runner", "field_bundle", "acceptance_rule", "current_value", "score_ready"], data["finite_rows"])}

## Claim Gates
{table(["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"], data["claim_gates"])}

## Decision Ledger
{table(["decision_id", "decision", "reason", "effect"], data["decisions"])}

## Next Target
{table(["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"], data["next_target"])}

## Branch Copies
{table(["copy_id", "source_path", "target_path", "source_exists", "target_exists"], data["branch_copies"])}

## Validation
{table(["check_id", "status", "notes", "detail"], data["validation"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    data: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "selector_theorem": selector_theorem_rows(),
        "clause_audit": clause_audit_rows(),
        "ift_derivation": ift_derivation_rows(),
        "finite_rows": finite_coefficient_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next_target": next_target_rows(),
    }
    for key in ["source_register", "selector_theorem", "clause_audit", "ift_derivation", "finite_rows", "claim_gates", "decisions", "next_target"]:
        write_csv(OUTPUTS[key], data[key])

    data["branch_copies"] = copy_outputs()
    write_csv(OUTPUTS["branch_copies"], data["branch_copies"])

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    data["validation"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validation"])
    write_doc(data)


if __name__ == "__main__":
    main()

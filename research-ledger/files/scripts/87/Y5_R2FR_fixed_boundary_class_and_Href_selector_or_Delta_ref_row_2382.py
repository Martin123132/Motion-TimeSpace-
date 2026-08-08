from __future__ import annotations

import csv
from pathlib import Path


BRANCH_ID = "MTS_R2FR_FIXED_BOUNDARY_CLASS_AND_HREF_SELECTOR_OR_DELTA_REF_ROW_2382"
PROJECT_ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main"
)
POST_ROOT = PROJECT_ROOT / "post-checkpoint-work"
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2382-Y5-R2FR-fixed-boundary-class-and-Href-selector-or-Delta-ref-row.md"
FORMALIZATION_WORKBENCH = PROJECT_ROOT / "formalization-workbench"


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def contains(path: Path, needle: str) -> bool:
    return needle in read_text(path)


def no_claim() -> str:
    return "false"


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register() -> list[dict[str, object]]:
    sources = [
        {
            "row_id": "SRC2382_00_2381_doc",
            "source_key": "2381_doc",
            "source_path": POST_ROOT / "2381-Y5-R2FR-boundary-term-classification-exact-vs-corner-reference.md",
            "needles": ["fixed boundary class plus `H_ref/B_ref` selector", "Delta_ref_over_MH"],
            "source_role": "current handoff selecting fixed-reference selector or Delta_ref row",
        },
        {
            "row_id": "SRC2382_01_2381_classification",
            "source_key": "2381_classification",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_2381_BOUNDARY_TERM_CLASSIFICATION.csv",
            "needles": ["BTC2381_4_fixed_reference", "PRIMARY_LIVE_REMAINDER"],
            "source_role": "machine-readable fixed-reference live remainder",
        },
        {
            "row_id": "SRC2382_02_999_doc",
            "source_key": "999_doc",
            "source_path": POST_ROOT / "999-Y5-R10-Bref-fixed-branch-selector-or-Delta-ref-source-coefficient-provenance.md",
            "needles": ["what parent rule forces the reference branch before source/readout exists?", "not a selector equation"],
            "source_role": "strict fixed-branch selector precedent",
        },
        {
            "row_id": "SRC2382_03_999_selector_attempt",
            "source_key": "999_selector_attempt",
            "source_path": RESIDUALS / "P8_Y5_R10_999_FIXED_BRANCH_SELECTOR_ATTEMPT.csv",
            "needles": ["FBS999_0_selector_definition", "FBS999_7_verdict"],
            "source_role": "fixed branch selector attempt rows",
        },
        {
            "row_id": "SRC2382_04_999_parent_contract",
            "source_key": "999_parent_contract",
            "source_path": RESIDUALS / "P8_Y5_R10_999_PARENT_SELECTOR_CONTRACT.csv",
            "needles": ["FBC999_0_selector_function", "FBC999_6_MHref_sidecar"],
            "source_role": "future parent selector contract",
        },
        {
            "row_id": "SRC2382_05_1000_schema",
            "source_key": "1000_schema",
            "source_path": RESIDUALS / "P8_Y5_R10_1000_STRICT_INPUT_SCHEMA.csv",
            "needles": ["SIS1000_2_Bref_rule", "SIS1000_5_no_cancellation"],
            "source_role": "strict Delta_ref provenance schema",
        },
        {
            "row_id": "SRC2382_06_1001_radius_audit",
            "source_key": "1001_radius_audit",
            "source_path": RESIDUALS / "P8_Y5_R10_1001_RADIUS_SURFACE_THEOREM_AUDIT.csv",
            "needles": ["RSA1001_1_surface_class", "RSA1001_4_reference_charge"],
            "source_role": "surface/domain/no-retune reference audit",
        },
        {
            "row_id": "SRC2382_07_545_doc",
            "source_key": "545_doc",
            "source_path": POST_ROOT / "545-Y5-boundary-reference-minimal-action-clause-or-residual-row.md",
            "needles": ["reference choice remains a contract", "not a parent result"],
            "source_role": "minimal boundary-reference action contract precedent",
        },
        {
            "row_id": "SRC2382_08_543_doc",
            "source_key": "543_doc",
            "source_path": POST_ROOT / "543-Y5-boundary-reference-residual-theorem-or-fill-first-row.md",
            "needles": ["reference choice and Hamiltonian boundary subtraction are not fixed", "next door is either a real boundary/reference theorem"],
            "source_role": "original boundary-reference residual failure",
        },
        {
            "row_id": "SRC2382_09_2379_doc",
            "source_key": "2379_doc",
            "source_path": POST_ROOT / "2379-Y5-R2FR-boundary-no-flux-theorem-or-Bzero-first-bound-row.md",
            "needles": ["fixed reference/counterterm", "positive same-frame M_H_ref"],
            "source_role": "current Bzero theorem dependency",
        },
    ]
    rows: list[dict[str, object]] = []
    for source in sources:
        path = Path(source["source_path"])
        needles = list(source["needles"])
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": source["row_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": str(path.exists()).lower(),
                "required": "true",
                "needles_found": str(all(contains(path, needle) for needle in needles)).lower(),
                "needles": "; ".join(needles),
                "source_role": source["source_role"],
                "valid_for_claim": no_claim(),
            }
        )
    return rows


def selector_theorem_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "FRT2382_0_selector_object",
            "theorem_step": "selector object",
            "statement": "Define a reference selector Sigma_ref assigning (gamma_ref,tau_ref,C_top,B_ct,S0) from boundary/topology/stationarity data.",
            "derivation": "H_ref and B_ref become functions of Sigma_ref rather than after-the-fact subtractions.",
            "required_for_zero": "named Sigma_ref with parent source/equation path",
            "current_status": "DEFINITION_CONTRACT_ONLY",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FRT2382_1_allowed_inputs",
            "theorem_step": "allowed selector inputs",
            "statement": "Sigma_ref may depend on fixed boundary class, topology/cohomology, orientation/corner convention, asymptotic coframe, tau convention and stationary/vacuum branch data.",
            "derivation": "These are pre-readout structural data, not measured source normalizations.",
            "required_for_zero": "input grammar has no source/material/GM labels",
            "current_status": "GRAMMAR_WRITTEN_NOT_PARENT_SIGNED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FRT2382_2_source_blind_chain_rule",
            "theorem_step": "source-blindness chain rule",
            "statement": "If D_source Sigma_ref=0, then D_source B_ref=(delta B_ref/delta Sigma_ref)D_source Sigma_ref=0 and D_source H_ref=0.",
            "derivation": "This is the exact chain-rule condition that would set the source component of Delta_ref to zero.",
            "required_for_zero": "componentwise D_source gamma_ref=tau_ref=C_top=B_ct=S0=0",
            "current_status": "CONDITIONAL_THEOREM_DERIVED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FRT2382_3_no_GM_laundering",
            "theorem_step": "no GM/fitted-source laundering",
            "statement": "Sigma_ref must satisfy partial_{GM_obs,M_fit,M_H_ref,kappa_A,composition_A} Sigma_ref=0 before the source-measure bridge is derived.",
            "derivation": "Otherwise the reference subtraction can absorb the charge we are trying to derive.",
            "required_for_zero": "no measured-GM, fitted mass, composition or M_H_ref labels in selector provenance",
            "current_status": "FORBIDDEN_INPUT_RULE_DERIVED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FRT2382_4_no_retune",
            "theorem_step": "no-retune surface/domain rule",
            "statement": "D_source S0=0 and linked surfaces remain in one parent boundary class; B_ref is not retuned as source, radius or readout changes.",
            "derivation": "Prevents source dependence from entering through a moving comparison surface rather than the B_ref integrand.",
            "required_for_zero": "surface class, corner convention, no-crossed-source and no-retune certificates",
            "current_status": "CONDITIONAL_ROUTE_NOT_SIGNED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FRT2382_5_MHref_sidecar",
            "theorem_step": "same-frame denominator sidecar",
            "statement": "Any Delta_ref/M_H_ref row requires finite positive M_H_ref in the same tau/coframe/frame as H_ref.",
            "derivation": "A source-blind H_ref is not enough if the denominator is imported from orbital GM or a different frame.",
            "required_for_zero": "M_H_ref source path, equation ref, units, tau_id, frame_id, no orbital-GM import",
            "current_status": "MISSING_POSITIVE_MHREF",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FRT2382_6_verdict",
            "theorem_step": "current theorem verdict",
            "statement": "The source-blindness criterion is derived, but the current corpus does not parent-sign Sigma_ref or M_H_ref.",
            "derivation": "FRT2382_0..5 give a sharp contract and refusal gate, not a completed reference theorem.",
            "required_for_zero": "parent selector equation plus same-frame M_H_ref",
            "current_status": "THEOREM_NOT_PROMOTED_RETAIN_DELTA_REF_ROW",
            "valid_for_claim": no_claim(),
        },
    ]


def selector_input_grammar_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SIG2382_0_boundary_class",
            "input": "fixed boundary class",
            "allowed": "true",
            "role": "selects which surfaces/corners/cohomology classes are admissible",
            "certificate_required": "boundary class id and no-retune rule",
            "violation_if_missing": "Delta_ref can change with source/readout surface",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SIG2382_1_topology",
            "input": "topology/cohomology/orientation/corner convention",
            "allowed": "true",
            "role": "fixes topological and corner reference data before source variation",
            "certificate_required": "C_top and corner convention source path",
            "violation_if_missing": "topological/corner charge can hide in H_ref",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SIG2382_2_frame_tau",
            "input": "asymptotic coframe and tau convention",
            "allowed": "true",
            "role": "locks the Hamiltonian generator and denominator frame",
            "certificate_required": "tau_id/frame_id/coframe_id shared by Q_tau, H_ref and M_H_ref",
            "violation_if_missing": "same-frame normalization fails",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SIG2382_3_stationary_vacuum_branch",
            "input": "stationary/vacuum reference branch data",
            "allowed": "conditional",
            "role": "can define zero-source comparison only if selected by parent equation rather than fit",
            "certificate_required": "selector equation or Ward/topological condition",
            "violation_if_missing": "reference-only zero is not MTS evidence",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SIG2382_4_observed_GM",
            "input": "observed GM/orbital mass/fitted source normalization",
            "allowed": "false",
            "role": "forbidden calibration input",
            "certificate_required": "absence proof in B_ref/H_ref provenance",
            "violation_if_missing": "borrow Newton/source normalization to prove Newton/source normalization",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SIG2382_5_material_labels",
            "input": "composition, material marker, source parameter kappa_A or m_A",
            "allowed": "false",
            "role": "forbidden source-label input",
            "certificate_required": "D_source Sigma_ref=0 and no marker labels",
            "violation_if_missing": "reference subtraction becomes source-dependent",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SIG2382_6_residual_sign",
            "input": "observed residual sign/magnitude",
            "allowed": "false",
            "role": "forbidden cancellation knob",
            "certificate_required": "timestamp/order: selector fixed before readout",
            "violation_if_missing": "post-hoc counterterm cancellation",
            "valid_for_claim": no_claim(),
        },
    ]


def delta_ref_bound_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DRR2382_0_source_component",
            "quantity": "Delta_ref_source_component_over_MH",
            "formula": "abs(partial_source_Delta_ref * Delta_source_scale)/M_H_ref",
            "required_inputs": "partial_source_Delta_ref;Delta_source_scale;B_ref_rule;M_H_ref;source_path;equation_ref;no_cancellation_guard",
            "current_value": "MISSING_NUMERIC_DERIVATIVE_OR_PARENT_SIGNED_ZERO;MISSING_SOURCE_SCALE;MISSING_PARENT_BREF_RULE;MISSING_M_H_REF",
            "status": "SCHEMA_READY_VALUES_MISSING",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DRR2382_1_surface_component",
            "quantity": "Delta_ref_surface_component_over_MH",
            "formula": "abs(partial_surface_Delta_ref * Delta_surface_profile)/M_H_ref",
            "required_inputs": "surface_class_id;partial_surface_Delta_ref;Delta_surface_profile;closed_B_ref_certificate;corner_certificate;M_H_ref",
            "current_value": "MISSING_SURFACE_CLASS_ID;MISSING_PARTIAL_SURFACE_DERIVATIVE;MISSING_M_H_REF",
            "status": "SCHEMA_READY_VALUES_MISSING",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DRR2382_2_counterterm_component",
            "quantity": "Delta_ref_counterterm_component_over_MH",
            "formula": "abs(Delta_B_ct_unfixed_or_retuned)/M_H_ref",
            "required_inputs": "B_ct formula;counterterm convention;pre-readout timestamp/source path;M_H_ref;no-cancellation guard",
            "current_value": "MISSING_COUNTERTERM_CONVENTION;MISSING_PRE_READOUT_SELECTOR;MISSING_M_H_REF",
            "status": "SCHEMA_READY_VALUES_MISSING",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DRR2382_3_total_absolute",
            "quantity": "Delta_ref_over_MH",
            "formula": "(abs(Delta_ref_source)+abs(Delta_ref_surface)+abs(Delta_ref_counterterm)+abs(Delta_ref_corner_top))/M_H_ref",
            "required_inputs": "all component numerators;positive same-frame M_H_ref;absolute no-cancellation rule",
            "current_value": "COMPONENTS_MISSING",
            "status": "PRIMARY_BOUND_ROW_STAGED_NONCLAIM",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2382_0_conditional_gain",
            "decision": "accept the source-blind selector criterion as a conditional theorem",
            "reason": "if Sigma_ref is fixed before source/readout and D_source Sigma_ref=0, then chain rule gives D_source H_ref=D_source B_ref=0",
            "consequence": "we now know exactly what a future parent action must sign",
            "status": "CONDITIONAL_SELECTOR_CRITERION_DERIVED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2382_1_no_promotion",
            "decision": "do not promote fixed-reference theorem",
            "reason": "the current corpus still lacks parent selector equation, no-marker/no-GM proof, surface no-retune certificate and same-frame M_H_ref",
            "consequence": "Delta_ref_over_MH remains staged as nonclaim",
            "status": "THEOREM_NOT_PARENT_SIGNED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2382_2_next",
            "decision": "attack parent selector equation next",
            "reason": "the missing object is not another table value; it is the equation or Ward/topological condition that fixes Sigma_ref",
            "consequence": "2383 should try to derive E_Sigma=0/topological selector, otherwise source-acquire Delta_ref components",
            "status": "SELECT_2383_PARENT_SELECTOR_EQUATION",
            "valid_for_claim": no_claim(),
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2382_0_selector_criterion",
            "gate": "source-blind selector chain-rule criterion",
            "gate_status": "PASS_CONDITIONAL_CRITERION_ONLY",
            "claim_effect": "defines what would make Delta_ref source component zero",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2382_1_parent_selector_equation",
            "gate": "parent equation or Ward/topological condition fixes Sigma_ref",
            "gate_status": "FAIL",
            "claim_effect": "fixed-reference theorem not promoted",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2382_2_no_GM_no_marker",
            "gate": "no GM/source/material labels in selector",
            "gate_status": "FAIL_UNSIGNED",
            "claim_effect": "source-blindness remains conditional",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2382_3_surface_no_retune",
            "gate": "surface/domain/corner no-retune certificate",
            "gate_status": "FAIL",
            "claim_effect": "surface Delta_ref component remains",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2382_4_MHref",
            "gate": "positive same-frame M_H_ref",
            "gate_status": "FAIL",
            "claim_effect": "Delta_ref_over_MH cannot be scored",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2382_5_local_GR_Newton",
            "gate": "local GR/Newton recovery",
            "gate_status": "FAIL_NONCLAIM",
            "claim_effect": "boundary/reference and source-measure gates remain open",
            "valid_for_claim": no_claim(),
        },
    ]


def refusal_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2382_0_reference_only_zero",
            "claim": "use reference-only zero as current MTS evidence",
            "allowed": "false",
            "reason": "reference-only zero is not a parent-signed MTS selector theorem",
            "blocking_rows": "FRT2382_0_selector_object;CG2382_1_parent_selector_equation",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2382_1_GM_selector",
            "claim": "let Sigma_ref depend on observed GM/fitted mass/M_H_ref",
            "allowed": "false",
            "reason": "this borrows source normalization before deriving it",
            "blocking_rows": "FRT2382_3_no_GM_laundering;SIG2382_4_observed_GM",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2382_2_posthoc_counterterm",
            "claim": "choose B_ct after reading the residual",
            "allowed": "false",
            "reason": "post-readout counterterms are cancellation knobs, not derived boundary data",
            "blocking_rows": "SIG2382_6_residual_sign;DRR2382_2_counterterm_component",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2382_3_score_delta_ref",
            "claim": "score Delta_ref_over_MH now",
            "allowed": "false",
            "reason": "component numerators, B_ref rule, source paths, equation refs, and M_H_ref are missing",
            "blocking_rows": "DRR2382_0_source_component;DRR2382_1_surface_component;DRR2382_2_counterterm_component;CG2382_4_MHref",
            "valid_for_claim": no_claim(),
        },
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2382_0_selected",
            "next_file": "2383-Y5-R2FR-parent-selector-equation-for-Sigma-ref-or-Delta-ref-source-pack.md",
            "success_condition": "derive a parent Euler/Ward/topological/stationarity equation that fixes Sigma_ref without source, GM, material or post-readout inputs",
            "fallback_condition": "fill Delta_ref component source pack with finite numerators, units, source paths, equation refs and valid_for_claim=false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2382_1_parallel",
            "next_file": "2383b-Y5-R2FR-MHref-same-frame-sidecar-or-denominator-row.md",
            "success_condition": "derive finite positive same-frame M_H_ref compatible with Sigma_ref",
            "fallback_condition": "keep all normalized boundary rows non-score-ready",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2382_2_parallel",
            "next_file": "2383c-Y5-R2FR-Hilbert-topological-source-equality-or-Req-row.md",
            "success_condition": "prove the Hamiltonian/topological charge is the Hilbert/source charge entering Poisson/Gauss",
            "fallback_condition": "retain R_eq/I_commutator rows",
            "valid_for_claim": no_claim(),
        },
    ]


CSV_BUILDERS = {
    "P8_Y5_PARENT_QLOC_2382_SOURCE_REGISTER.csv": source_register,
    "P8_Y5_PARENT_QLOC_2382_FIXED_REFERENCE_SELECTOR_THEOREM.csv": selector_theorem_rows,
    "P8_Y5_PARENT_QLOC_2382_SELECTOR_INPUT_GRAMMAR.csv": selector_input_grammar_rows,
    "P8_Y5_PARENT_QLOC_2382_DELTA_REF_BOUND_ROWS.csv": delta_ref_bound_rows,
    "P8_Y5_PARENT_QLOC_2382_DECISION_LEDGER.csv": decision_rows,
    "P8_Y5_PARENT_QLOC_2382_CLAIM_GATES.csv": claim_gate_rows,
    "P8_Y5_PARENT_QLOC_2382_REFUSAL_RUNNER.csv": refusal_rows,
    "P8_Y5_PARENT_QLOC_2382_NEXT_TARGET.csv": next_target_rows,
}


def check_no_positive_claim_flags(paths: list[Path]) -> bool:
    for path in paths:
        if not path.exists():
            continue
        for row in read_csv(path):
            if str(row.get("valid_for_claim", "")).strip().lower() == "true":
                return False
    return True


def validation_rows() -> list[dict[str, object]]:
    csv_paths = [RESIDUALS / name for name in CSV_BUILDERS]
    rows: list[dict[str, object]] = []

    def add(row_id: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "valid_for_claim": no_claim(),
            }
        )

    sources = source_register()
    add("VAL2382_00_sources_exist", all(row["exists"] == "true" for row in sources), "all required source paths exist")
    add("VAL2382_01_needles_found", all(row["needles_found"] == "true" for row in sources), "all source needles found")
    theorem = selector_theorem_rows()
    add(
        "VAL2382_02_chain_rule_criterion_present",
        any(row["row_id"] == "FRT2382_2_source_blind_chain_rule" and "CONDITIONAL" in row["current_status"] for row in theorem),
        "source-blindness chain-rule criterion present as conditional theorem",
    )
    grammar = selector_input_grammar_rows()
    add(
        "VAL2382_03_forbidden_inputs_present",
        {"observed GM/orbital mass/fitted source normalization", "composition, material marker, source parameter kappa_A or m_A", "observed residual sign/magnitude"}.issubset({row["input"] for row in grammar}),
        "forbidden GM/material/post-readout selector inputs present",
    )
    bounds = delta_ref_bound_rows()
    add(
        "VAL2382_04_delta_ref_rows_nonready",
        all(row["score_ready"] == "false" for row in bounds),
        "Delta_ref rows remain non-score-ready",
    )
    gates = claim_gate_rows()
    add(
        "VAL2382_05_global_claims_blocked",
        all(row["gate_status"] != "PASS" for row in gates if row["row_id"] != "CG2382_0_selector_criterion"),
        "global/local gates remain blocked",
    )
    add(
        "VAL2382_06_csv_parse",
        all(path.exists() and len(read_csv(path)) > 0 for path in csv_paths if path.exists()),
        "generated CSVs parse and have rows",
    )
    add("VAL2382_07_no_claim_flags", check_no_positive_claim_flags(csv_paths), "no generated row has valid_for_claim=true")
    add(
        "VAL2382_08_formalization_untouched_by_script",
        FORMALIZATION_WORKBENCH not in DOC_PATH.parents and all(FORMALIZATION_WORKBENCH not in path.parents for path in csv_paths),
        "script writes only post-checkpoint-work outputs",
    )
    add(
        "VAL2382_09_next_selected",
        any(row["row_id"] == "NEXT2382_0_selected" for row in next_target_rows()),
        "parent selector equation selected next",
    )
    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2382_OVERALL",
        overall,
        "2382 derives the conditional source-blind reference selector criterion, refuses promotion without parent selector/MHref, and stages Delta_ref rows nonclaim",
    )
    return rows


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def write_doc() -> None:
    source_rows = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2382_SOURCE_REGISTER.csv")
    theorem = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2382_FIXED_REFERENCE_SELECTOR_THEOREM.csv")
    grammar = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2382_SELECTOR_INPUT_GRAMMAR.csv")
    bounds = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2382_DELTA_REF_BOUND_ROWS.csv")
    decisions = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2382_DECISION_LEDGER.csv")
    gates = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2382_CLAIM_GATES.csv")
    refusals = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2382_REFUSAL_RUNNER.csv")
    next_rows = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2382_NEXT_TARGET.csv")
    validation = read_csv(RESIDUALS / "P8_Y5_BRR545_2382_VALIDATION.csv")

    body = f"""# 2382 - fixed boundary class and Href selector or Delta-ref row

## Result

2382 derives the exact *criterion* for a safe boundary/reference selector:

`Sigma_ref = Sigma_ref(boundary_class, topology, corner convention, asymptotic coframe, tau, stationary/vacuum branch)`

with no source/material/GM/readout/residual inputs.  If `D_source Sigma_ref = 0`, then by the chain rule

`D_source B_ref = (delta B_ref/delta Sigma_ref) D_source Sigma_ref = 0`

and likewise `D_source H_ref=0`.  That is the clean condition under which the source component of `Delta_ref` vanishes.

But the current corpus still does **not** supply the parent equation that fixes `Sigma_ref`, nor the no-marker/no-GM
certificate, nor the surface no-retune certificate, nor positive same-frame `M_H_ref`.  So the selector theorem is not
promoted.  `Delta_ref_over_MH` is staged as a nonclaim residual row.

No `B_zero_flux=0`, `Delta_ref=0`, `M_H_ref`, Newton, local-GR, PPN, orbital, clock, R10, or GitHub/public claim is made.

## Source Register

{markdown_table(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"])}

## Fixed Reference Selector Theorem

{markdown_table(theorem, ["row_id", "theorem_step", "statement", "derivation", "required_for_zero", "current_status", "valid_for_claim"])}

## Selector Input Grammar

{markdown_table(grammar, ["row_id", "input", "allowed", "role", "certificate_required", "violation_if_missing", "valid_for_claim"])}

## Delta Ref Bound Rows

{markdown_table(bounds, ["row_id", "quantity", "formula", "required_inputs", "current_value", "status", "score_ready", "valid_for_claim"])}

## Decision Ledger

{markdown_table(decisions, ["row_id", "decision", "reason", "consequence", "status", "valid_for_claim"])}

## Claim Gates

{markdown_table(gates, ["row_id", "gate", "gate_status", "claim_effect", "valid_for_claim"])}

## Refusal Runner

{markdown_table(refusals, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"])}

## Next Target

{markdown_table(next_rows, ["row_id", "next_file", "success_condition", "fallback_condition", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["row_id", "status", "detail", "valid_for_claim"])}

## Practical Status

This is another useful tightening.  The reference problem is no longer just "choose a boundary term carefully"; it is a
specific selector equation problem.  If the parent action can produce `Sigma_ref` from source-blind boundary/topological
data, `Delta_ref` gets a real zero route.  If not, the honest path is a finite `Delta_ref_over_MH` source pack.

The best next strike is therefore `2383`: try to derive the parent selector equation for `Sigma_ref`.  That is the
actual leap forward; another placeholder denominator row would be circling.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    for name, builder in CSV_BUILDERS.items():
        write_csv(RESIDUALS / name, builder())
    write_csv(RESIDUALS / "P8_Y5_BRR545_2382_VALIDATION.csv", validation_rows())
    write_doc()
    print(f"wrote {DOC_PATH}")
    print(f"wrote {RESIDUALS / 'P8_Y5_BRR545_2382_VALIDATION.csv'}")


if __name__ == "__main__":
    main()

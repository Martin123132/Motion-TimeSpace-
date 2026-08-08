from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path("source-intake/mts_residuals")

DOC_PATH = Path("1384-Y5-R10-RAB-Zm-parent-coefficient-law-derivation-attempt-or-F2-normalization-pivot.md")
SOURCE_REGISTER_PATH = SRC_DIR / "P8_Y5_R10_1384_SOURCE_REGISTER.csv"
CANONICAL_AUDIT_PATH = SRC_DIR / "P8_Y5_R10_1384_CANONICALIZATION_DERIVATION_AUDIT.csv"
INVARIANT_PIVOT_PATH = SRC_DIR / "P8_Y5_R10_1384_FIELD_REDEFINITION_INVARIANT_PIVOT.csv"
FIRST_FILL_PATH = SRC_DIR / "P8_Y5_R10_1384_FIRST_FILL_ROW_SELECTION.csv"
RUNNER_FEED_PATH = SRC_DIR / "P8_Y5_R10_1384_RUNNER_FEED_UPDATE.csv"
CLAIM_GATE_PATH = SRC_DIR / "P8_Y5_R10_1384_CLAIM_GATE.csv"
DECISION_LEDGER_PATH = SRC_DIR / "P8_Y5_R10_1384_DECISION_LEDGER.csv"
NEXT_TARGET_PATH = SRC_DIR / "P8_Y5_R10_1384_NEXT_TARGET.csv"
VALIDATION_PATH = SRC_DIR / "P8_Y5_BRR545_1384_VALIDATION.csv"

STATUS = (
    "Z_m_parent_law_derivation_attempt_completed_with_canonical_gap_coupling_pivot_"
    "no_numeric_local_claim"
)
CLAIM_CEILING = (
    "conditional_canonicalization_and_first_fill_selection_only_no_source_backed_mu_m2_"
    "no_canonical_coupling_no_numeric_ell_tr_no_PPN_no_R10_no_local_GR_pass"
)

SOURCE_ROWS = [
    {
        "source_id": "SRC1384_0_1383_doc",
        "source_path": "1383-Y5-R10-RAB-Zm-symbolic-prior-validator-and-transition-runner-dryrun.md",
        "required_anchor": "NEXT1383_0_1384",
        "purpose": "handoff from symbolic validator to Z_m/F2 derivation attempt",
    },
    {
        "source_id": "SRC1384_1_1383_next",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1383_NEXT_TARGET.csv",
        "required_anchor": "NEXT1383_0_1384",
        "purpose": "machine-readable 1384 target",
    },
    {
        "source_id": "SRC1384_2_1383_validator",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1383_SYMBOLIC_PRIOR_VALIDATOR.csv",
        "required_anchor": "ZPV1383_7_verdict",
        "purpose": "strict validator showing all numeric rows blocked",
    },
    {
        "source_id": "SRC1384_3_1383_dryrun",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1383_TRANSITION_INEQUALITY_DRYRUN.csv",
        "required_anchor": "TID1383_6_dryrun_verdict",
        "purpose": "transition inequality dry-run formulas",
    },
    {
        "source_id": "SRC1384_4_826_action_ansatz",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_826_PARENT_ACTION_ANSATZ.csv",
        "required_anchor": "AA826_1_memory_sector",
        "purpose": "candidate memory-sector action L_m=-1/2 Z_m(X_B)(nabla m)^2 - V_R",
    },
    {
        "source_id": "SRC1384_5_1304_operator",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1304_MEMORY_OPERATOR_OWNER_ATTEMPT.csv",
        "required_anchor": "OO1304_1_static_local_operator_map",
        "purpose": "static local operator map A_m^{ij}=Z_m h^{ij}",
    },
    {
        "source_id": "SRC1384_6_1379_formula_feed",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1379_CONDITIONAL_FORMULA_FEED.csv",
        "required_anchor": "Q_alg",
        "purpose": "closure-only formulas for ell_tr, U_B, Delta_m and Q_alg",
    },
    {
        "source_id": "SRC1384_7_970_positivity",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_970_QUADRATIC_MEMORY_ACTION_CONSTRUCTION.csv",
        "required_anchor": "QMA970_2_positivity",
        "purpose": "conditional positive-operator energy identity",
    },
    {
        "source_id": "SRC1384_8_1382_prior_pack",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1382_SYMBOLIC_PRIOR_PACK.csv",
        "required_anchor": "ZPP1382_5_F2_sign_value",
        "purpose": "prior rows showing F2 and Z_m normalizations unresolved",
    },
    {
        "source_id": "SRC1384_9_1383_validation",
        "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_1383_VALIDATION.csv",
        "required_anchor": "VAL1383_6_overall",
        "purpose": "previous checkpoint validation",
    },
    {
        "source_id": "SRC1384_10_this_script",
        "source_path": "scripts/Y5_R10_RAB_Zm_parent_coefficient_law_derivation_attempt_or_F2_normalization_pivot.py",
        "required_anchor": "STATUS",
        "purpose": "1384 generator",
    },
]


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "/")


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str] | None = None) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = columns or list(rows[0].keys())
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: clean(row.get(key, "")) for key in fieldnames})


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return ""
    fieldnames = columns or list(rows[0].keys())
    lines = [
        "| " + " | ".join(fieldnames) + " |",
        "| " + " | ".join("---" for _ in fieldnames) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(clean(row.get(column, "")) for column in fieldnames) + " |")
    return "\n".join(lines)


def anchor_found(path: Path, anchor: str) -> bool:
    if not path.exists():
        return False
    return anchor in path.read_text(encoding="utf-8", errors="ignore")


def source_register_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in SOURCE_ROWS:
        source_path = ROOT / row["source_path"]
        exists = source_path.exists()
        found = anchor_found(source_path, row["required_anchor"])
        rows.append(
            {
                **row,
                "exists": str(exists),
                "anchor_found": str(found),
                "valid_for_claim": "False",
                "claim_allowed": "False",
            }
        )
    return rows


def canonical_audit_rows() -> list[dict[str, str]]:
    return [
        {
            "audit_id": "CDA1384_0_starting_sector",
            "derivation_step": "start from candidate scalar-memory sector",
            "mathematical_statement": "L_m=-1/2 Z_m(X_B) nabla_mu m nabla^mu m - V_R(m;X_B) plus possible J/source/bath/boundary terms",
            "derived_result": "relative local expansion can be attempted from the existing action scaffold",
            "condition_or_gap": "parent adoption, field domain, source/bath, and boundary class remain unsigned",
            "status": "STARTING_POINT_AVAILABLE_NONCLAIM",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "CDA1384_1_local_background_freeze",
            "derivation_step": "choose local branch background",
            "mathematical_statement": "m=m_*+eta, X_B=X_0 plus corrections, partial_m V_R(m_*;X_0)=0",
            "derived_result": "quadratic local action exists if X_B gradients and source terms are separated into residuals",
            "condition_or_gap": "X_0 branch, extremum, and source-free or bounded local exterior are not parent-proven",
            "status": "CONDITIONAL_LOCAL_EXPANSION",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "CDA1384_2_quadratic_action",
            "derivation_step": "expand to quadratic order in eta",
            "mathematical_statement": "L_m^(2)=-1/2 Z_0 (nabla eta)^2 -1/2 L0^-2 F2 eta^2 + eta J_eta + residual_Xgrad",
            "derived_result": "Euler equation gives Z_0 Box eta - L0^-2 F2 eta = J_eta plus residual corrections",
            "condition_or_gap": "F2 sign/value/units, J_eta, and residual_Xgrad are missing",
            "status": "RELATIVE_EULER_FORM_DERIVED_INPUTS_MISSING",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "CDA1384_3_canonical_field",
            "derivation_step": "canonicalize the local fluctuation",
            "mathematical_statement": "phi=sqrt(Z_0) eta for Z_0>0 and locally frozen X_B",
            "derived_result": "L_m^(2)=-1/2 (nabla phi)^2 -1/2 mu_m^2 phi^2 + phi J_c + residual_Xgrad with mu_m^2=F2/(Z_0 L0^2)",
            "condition_or_gap": "requires Z_0>0 and a fixed local normalization; J_c=J_eta/sqrt(Z_0) must be sourced",
            "status": "CONDITIONAL_CANONICALIZATION_DERIVED",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "CDA1384_4_field_redefinition_invariance",
            "derivation_step": "test separate observability of Z_m and F2",
            "mathematical_statement": "under eta=a eta', Z_0 -> a^-2 Z_0 and F2 -> a^-2 F2, so F2/Z_0 is invariant",
            "derived_result": "separate Z_m and F2 values are partly field-normalization dependent; the local range is controlled by mu_m^2=F2/(Z_0 L0^2)",
            "condition_or_gap": "this does not remove the need for a canonical coupling or stress/source residual bounds",
            "status": "INVARIANT_PIVOT_DERIVED",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "CDA1384_5_transition_length",
            "derivation_step": "rewrite transition length invariantly",
            "mathematical_statement": "ell_tr=sqrt(Z_0 L0^2/F2)=1/sqrt(mu_m^2)",
            "derived_result": "numeric transition scoring should request mu_m^2 directly, not separate Z_m and F2 unless a parent normalization fixes both",
            "condition_or_gap": "mu_m^2(X_B) source-backed law is still missing",
            "status": "TRANSITION_LENGTH_PIVOT_READY_NONCLAIM",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "CDA1384_6_XB_gradient_correction",
            "derivation_step": "check nonconstant X_B",
            "mathematical_statement": "if Z_m=Z_m(X_B(x)), canonicalization produces correction scales controlled by nabla ln Z_m and nabla X_B",
            "derived_result": "local canonical branch is clean only when epsilon_Z=|nabla ln Z_m|/mu_m is small or parent-zero; otherwise residual_Xgrad must be retained",
            "condition_or_gap": "no epsilon_Z theorem or bound exists",
            "status": "XB_GRADIENT_RESIDUAL_RETAINED",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "CDA1384_7_law_derivation_failure",
            "derivation_step": "try to derive full Z_m(X_B) from covariance/action form alone",
            "mathematical_statement": "diffeomorphism invariance and positivity allow infinitely many positive functions Z_m(X_B)",
            "derived_result": "a unique Z_m law does not follow from the current scaffold; extra symmetry, UV/statistical principle, or empirical-source row is required",
            "condition_or_gap": "no parent symmetry or microscopic rule selecting Z_m(X_B) is present",
            "status": "FULL_ZM_LAW_NOT_DERIVED_PIVOT_TO_INVARIANTS",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "CDA1384_8_verdict",
            "derivation_step": "1384 result",
            "mathematical_statement": "replace the first numeric request Z_m,F2 with canonical invariant pair mu_m^2(X_B), g_c(X_B)",
            "derived_result": "canonical gap/coupling is the first-fill target; separate Z_m and F2 remain useful only after a parent field normalization is fixed",
            "condition_or_gap": "mu_m^2 law, canonical coupling, X_B gradient correction, source/boundary amplitude still missing",
            "status": "CANONICAL_GAP_COUPLING_PIVOT_SELECTED",
            "valid_for_claim": "False",
        },
    ]


def invariant_pivot_rows() -> list[dict[str, str]]:
    return [
        {
            "pivot_id": "IPV1384_0_old_inputs",
            "old_request": "Z_m_min, Z_m_bar, F2 sign/value/units separately",
            "problem": "separate values depend on field normalization unless the parent action fixes the normalization of m",
            "invariant_replacement": "mu_m^2(X_B)=F2/(Z_m L0^2)",
            "what_it_unlocks": "ell_tr=1/sqrt(mu_m^2) and support suppression targets",
            "remaining_gap": "source-backed mu_m^2 law and units",
            "status": "PIVOT_REDUCES_REDUNDANT_PRIORS",
            "valid_for_claim": "False",
        },
        {
            "pivot_id": "IPV1384_1_coupling",
            "old_request": "source amplitude/coupling hidden inside J_eta or boundary A_S",
            "problem": "local tests care about how strongly the canonical mode couples to matter/readout, not merely its range",
            "invariant_replacement": "g_c(X_B) or J_c=J_eta/sqrt(Z_m)",
            "what_it_unlocks": "R10 alpha(lambda), fifth-force, PPN residual amplitude, clock/orbital residuals",
            "remaining_gap": "parent matter descent/source map for canonical field",
            "status": "COUPLING_IDENTIFIED_AS_COEQUAL_FIRST_FILL",
            "valid_for_claim": "False",
        },
        {
            "pivot_id": "IPV1384_2_profile_amplitude",
            "old_request": "A_S in original m units",
            "problem": "A_S rescales with m and is not invariant alone",
            "invariant_replacement": "Phi_S=sqrt(Z_0) A_S or source-derived canonical boundary amplitude",
            "what_it_unlocks": "Delta_phi, gradient envelope, stress residual envelope",
            "remaining_gap": "source/boundary theorem or canonical amplitude bound",
            "status": "CANONICAL_AMPLITUDE_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "pivot_id": "IPV1384_3_X_gradient",
            "old_request": "assume local Z_m constant",
            "problem": "varying X_B creates derivative-coupling residuals after canonicalization",
            "invariant_replacement": "epsilon_Z=|nabla ln Z_m|/mu_m plus explicit residual_Xgrad row",
            "what_it_unlocks": "safe local plateau or bounded correction branch",
            "remaining_gap": "parent/local bound on X_B variation",
            "status": "XB_GRADIENT_CORRECTION_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "pivot_id": "IPV1384_4_verdict",
            "old_request": "derive Z_m(X_B) and F2 as independent physical laws",
            "problem": "current corpus cannot uniquely derive them and separate values are not invariant without normalization",
            "invariant_replacement": "derive/source mu_m^2(X_B), g_c(X_B), Phi_S/boundary, epsilon_Z",
            "what_it_unlocks": "a cleaner path to local residual scoring",
            "remaining_gap": "all invariant replacement rows are still nonclaim",
            "status": "FIELD_REDEFINITION_INVARIANT_PIVOT_READY_NONCLAIM",
            "valid_for_claim": "False",
        },
    ]


def first_fill_rows() -> list[dict[str, str]]:
    return [
        {
            "fill_id": "FFR1384_0_mu_m2",
            "candidate_input": "mu_m^2(X_B)",
            "definition": "mu_m^2=F2/(Z_m L0^2) in the locally canonical memory scalar branch",
            "why_first": "sets the physical local range ell_tr=1/sqrt(mu_m^2) without over-focusing on field-normalization-dependent Z_m and F2 separately",
            "required_source": "parent potential Hessian divided by kinetic normalization, or direct canonical mass-gap theorem",
            "unlocks": "transition length;support suppression inequalities;part of Q_alg target",
            "still_does_not_unlock": "coupling amplitude;R10 alpha;PPN residuals;local GR",
            "rank": "1A",
            "valid_for_claim": "False",
        },
        {
            "fill_id": "FFR1384_1_g_c",
            "candidate_input": "g_c(X_B) or canonical source coupling",
            "definition": "canonical matter/readout coupling to phi, e.g. J_c=J_eta/sqrt(Z_m) or derivative of matter metric/source map with respect to phi",
            "why_first": "local tests are coupling tests as much as range tests; a massive mode with zero/silent coupling is harmless, a light coupled mode is deadly",
            "required_source": "matter descent/source map in canonical variables with species/universality statement",
            "unlocks": "fifth-force amplitude;R10 alpha(lambda);PPN and clock/orbital residual amplitudes",
            "still_does_not_unlock": "range without mu_m^2;boundary/source profile without Phi_S",
            "rank": "1B",
            "valid_for_claim": "False",
        },
        {
            "fill_id": "FFR1384_2_Phi_S",
            "candidate_input": "Phi_S or canonical boundary/source amplitude",
            "definition": "canonical amplitude feeding the exterior profile, Phi_S=sqrt(Z_0) A_S when local normalization is fixed",
            "why_first": "converts suppression algebra into residual-size bounds once mu_m and g_c exist",
            "required_source": "boundary/source theorem, amplitude bound, or zero-source condition",
            "unlocks": "Delta_phi;gradient envelope;stress residual estimate",
            "still_does_not_unlock": "coupling/range if FFR1384_0 and FFR1384_1 missing",
            "rank": "2",
            "valid_for_claim": "False",
        },
        {
            "fill_id": "FFR1384_3_epsilon_Z",
            "candidate_input": "epsilon_Z=|nabla ln Z_m|/mu_m",
            "definition": "dimensionless local correction scale from X_B variation of kinetic normalization",
            "why_first": "separates true local plateau from hidden derivative-coupling residuals",
            "required_source": "X_B local variation theorem or bound",
            "unlocks": "controlled canonicalization beyond exactly frozen X_B",
            "still_does_not_unlock": "coupling/range/source amplitude",
            "rank": "3",
            "valid_for_claim": "False",
        },
        {
            "fill_id": "FFR1384_4_selection",
            "candidate_input": "first-fill verdict",
            "definition": "fill mu_m^2(X_B) and g_c(X_B) as a coupled pair before trying to score local claims",
            "why_first": "range without coupling and coupling without range are both insufficient; together they define the physical local channel",
            "required_source": "canonical parent mass-gap plus canonical matter/source coupling",
            "unlocks": "first meaningful R10/PPN/local residual runner design",
            "still_does_not_unlock": "claims until Phi_S, source/boundary, X-gradient, and arena projection rows also pass",
            "rank": "SELECTED",
            "valid_for_claim": "False",
        },
    ]


def runner_feed_rows() -> list[dict[str, str]]:
    return [
        {
            "feed_id": "RUF1384_0_replace_transition_length",
            "old_formula": "ell_tr=sqrt(Z_m L0^2/F2)",
            "new_formula": "ell_tr=1/sqrt(mu_m^2)",
            "status": "CANONICAL_FORMULA_READY_SYMBOLIC",
            "required_to_score": "source-backed mu_m^2(X_B)>0 in local branch",
            "claim_allowed": "False",
        },
        {
            "feed_id": "RUF1384_1_replace_amplitude",
            "old_formula": "Delta_m=A_S exp(-d/ell_tr)",
            "new_formula": "Delta_phi=Phi_S exp(-d sqrt(mu_m^2))",
            "status": "CANONICAL_AMPLITUDE_FORMULA_READY_VALUES_MISSING",
            "required_to_score": "Phi_S or source/boundary amplitude plus mu_m^2",
            "claim_allowed": "False",
        },
        {
            "feed_id": "RUF1384_2_replace_Q_alg",
            "old_formula": "Q_alg <= A_ref^-1 |F2| A_S^2 U_B^2/(L0^2 ell_tr)",
            "new_formula": "Q_alg_canon <= A_ref^-1 mu_m^2 Phi_S^2 exp(-2d sqrt(mu_m^2))/ell_tr plus residual_Xgrad/source/boundary terms",
            "status": "CANONICAL_Q_FORMULA_SKETCH_NONCLAIM",
            "required_to_score": "normalization of A_ref, canonical stress convention, Phi_S, mu_m^2, residual bounds",
            "claim_allowed": "False",
        },
        {
            "feed_id": "RUF1384_3_coupling_gate",
            "old_formula": "implicit coupling hidden in source rows",
            "new_formula": "local observable amplitude requires g_c(X_B) times canonical profile/residual",
            "status": "COUPLING_GATE_INSERTED",
            "required_to_score": "parent matter descent/source map in canonical variables",
            "claim_allowed": "False",
        },
        {
            "feed_id": "RUF1384_4_runner_verdict",
            "old_formula": "Z_m/F2 prior validator",
            "new_formula": "canonical gap-coupling validator should supersede separate Z_m/F2 scoring",
            "status": "RUNNER_PIVOT_READY_NO_NUMERIC_SCORE",
            "required_to_score": "1385 canonical mass-gap/coupling derivation or source rows",
            "claim_allowed": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "GATE1384_0_sources",
            "gate": "all cited sources exist and anchors are present",
            "status": "PASS",
            "reason": "source register validates against local corpus",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1384_1_canonicalization",
            "gate": "local canonicalization derivation exists",
            "status": "PASS_CONDITIONAL_DERIVATION",
            "reason": "CDA1384_3 derives phi=sqrt(Z_0) eta and mu_m^2=F2/(Z_0 L0^2) under frozen-X_B assumptions",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1384_2_full_Zm_law",
            "gate": "unique parent Z_m(X_B) law is derived",
            "status": "BLOCKED_NOT_DERIVED",
            "reason": "covariance/action form allows infinitely many positive Z_m functions without extra principle",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1384_3_first_fill",
            "gate": "first-fill target selected",
            "status": "PASS_SELECTED_MU_M2_AND_GC",
            "reason": "canonical mass-gap and coupling are the physical pair needed before local scoring",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1384_4_numeric",
            "gate": "numeric ell_tr / R10 / PPN scoring can run",
            "status": "BLOCKED_CANONICAL_INPUTS_MISSING",
            "reason": "mu_m^2, g_c, Phi_S, epsilon_Z, source/boundary and arena projection rows are not source-backed",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE1384_5_local_claim",
            "gate": "local GR / Newton / PPN / R10 pass can be claimed",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "1384 is a canonical pivot and first-fill selection, not a parent-signed GR reduction",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1384_0",
            "question": "Did the attempt derive a unique Z_m(X_B) law?",
            "answer": "No",
            "rationale": "The current parent scaffold plus covariance leaves infinitely many positive functions and does not fix field normalization.",
            "next_action": "stop treating separate Z_m and F2 as the first physical target",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC1384_1",
            "question": "Did the attempt derive something useful?",
            "answer": "Yes",
            "rationale": "The physical local range is controlled by the canonical invariant mu_m^2=F2/(Z_m L0^2), and local empirical visibility is controlled by canonical coupling g_c.",
            "next_action": "derive/source the canonical mass-gap and canonical coupling together",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC1384_2",
            "question": "Is coupling now officially central?",
            "answer": "Yes",
            "rationale": "A range without coupling cannot create a fifth force; a coupling without range cannot be scored. The local branch needs the pair.",
            "next_action": "make 1385 a canonical mass-gap/coupling parent-contract attempt",
            "claim_allowed": "False",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1384_0_1385",
            "next_doc": "1385-Y5-R10-RAB-canonical-mass-gap-and-coupling-parent-contract.md",
            "next_script": "scripts/Y5_R10_RAB_canonical_mass_gap_and_coupling_parent_contract.py",
            "task": "derive or explicitly contract the canonical memory mass-gap mu_m^2(X_B) and matter/readout coupling g_c(X_B), including source descent, universality, and local arena projection refusal gates",
            "success_condition": "either a parent-owned canonical gap/coupling derivation scaffold exists, or nonclaim first-fill rows for mu_m^2 and g_c are written with exact source requirements and local claims remain blocked",
            "do_not_claim": "local GR;Newton limit;PPN pass;R10 pass;q_loc=0;numeric ell_tr;GitHub-ready result",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        }
    ]


def validation_rows(
    sources: list[dict[str, str]],
    canonical: list[dict[str, str]],
    pivots: list[dict[str, str]],
    first_fill: list[dict[str, str]],
    gates: list[dict[str, str]],
) -> list[dict[str, str]]:
    all_sources_ok = all(row["exists"] == "True" and row["anchor_found"] == "True" for row in sources)
    canonical_pivot_exists = any(row["audit_id"] == "CDA1384_4_field_redefinition_invariance" and row["status"] == "INVARIANT_PIVOT_DERIVED" for row in canonical)
    full_law_blocked = any(row["audit_id"] == "CDA1384_7_law_derivation_failure" and row["status"] == "FULL_ZM_LAW_NOT_DERIVED_PIVOT_TO_INVARIANTS" for row in canonical)
    selected_pair = any(row["fill_id"] == "FFR1384_4_selection" and row["rank"] == "SELECTED" for row in first_fill)
    nonclaim = all(row.get("valid_for_claim", "False") == "False" for row in canonical + pivots + first_fill)
    local_blocked = any(row["gate_id"] == "GATE1384_5_local_claim" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates)
    outputs = [
        DOC_PATH,
        SOURCE_REGISTER_PATH,
        CANONICAL_AUDIT_PATH,
        INVARIANT_PIVOT_PATH,
        FIRST_FILL_PATH,
        RUNNER_FEED_PATH,
        CLAIM_GATE_PATH,
        DECISION_LEDGER_PATH,
        NEXT_TARGET_PATH,
        VALIDATION_PATH,
        Path("scripts/Y5_R10_RAB_Zm_parent_coefficient_law_derivation_attempt_or_F2_normalization_pivot.py"),
    ]
    outside_formalization = all("formalization-workbench" not in str(ROOT / path) for path in outputs)
    overall = all([all_sources_ok, canonical_pivot_exists, full_law_blocked, selected_pair, nonclaim, local_blocked, outside_formalization])
    return [
        {
            "validation_id": "VAL1384_0_sources",
            "check": "every cited local source path exists and anchor is found",
            "status": "PASS" if all_sources_ok else "FAIL",
            "details": "; ".join(f"{row['source_id']} exists={row['exists']} anchor={row['anchor_found']}" for row in sources),
        },
        {
            "validation_id": "VAL1384_1_canonical_pivot",
            "check": "field-redefinition invariant canonical pivot is derived",
            "status": "PASS" if canonical_pivot_exists else "FAIL",
            "details": "CDA1384_4 records F2/Z_m invariance under local field rescaling.",
        },
        {
            "validation_id": "VAL1384_2_full_law_refusal",
            "check": "full Z_m law is not falsely claimed",
            "status": "PASS" if full_law_blocked else "FAIL",
            "details": "CDA1384_7 blocks unique Z_m(X_B) derivation from covariance/action form alone.",
        },
        {
            "validation_id": "VAL1384_3_first_fill",
            "check": "first-fill target is selected",
            "status": "PASS" if selected_pair else "FAIL",
            "details": "FFR1384_4 selects mu_m^2(X_B) plus g_c(X_B) as the first physical pair.",
        },
        {
            "validation_id": "VAL1384_4_nonclaim",
            "check": "all derivation/pivot/fill rows remain nonclaim",
            "status": "PASS" if nonclaim else "FAIL",
            "details": "No canonical pivot row is valid_for_claim.",
        },
        {
            "validation_id": "VAL1384_5_local_refusal",
            "check": "local claims remain blocked",
            "status": "PASS" if local_blocked else "FAIL",
            "details": "GATE1384_5 keeps BLOCKED_NO_CLAIM.",
        },
        {
            "validation_id": "VAL1384_6_scope",
            "check": "generated outputs stay inside post-checkpoint-work and outside formalization-workbench",
            "status": "PASS" if outside_formalization else "FAIL",
            "details": f"ROOT={ROOT}; output_count={len(outputs)}; formalization_touched=False",
        },
        {
            "validation_id": "VAL1384_7_overall",
            "check": "overall 1384 validation",
            "status": "PASS" if overall else "FAIL",
            "details": "1384 derives the canonical invariant pivot and selects canonical mass-gap plus coupling as first-fill target.",
        },
    ]


def write_doc(
    sources: list[dict[str, str]],
    canonical: list[dict[str, str]],
    pivots: list[dict[str, str]],
    first_fill: list[dict[str, str]],
    runner: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    generated = datetime.now(timezone.utc).isoformat()
    body = f"""# 1384 - Y5 R10 RAB Z_m Parent Coefficient-Law Derivation Attempt Or F2 Normalization Pivot

**Generated:** {generated}

**Current verdict:** the full `Z_m(X_B)` law is **not** derived from the current parent scaffold. But the attempt produces a useful simplification: in a locally frozen branch, separate `Z_m` and `F2` are partly field-normalization dependent, while the canonical invariant `mu_m^2=F2/(Z_m L0^2)` controls the transition length.

**Discipline move:** pivot the local transition branch from separate `Z_m/F2` scoring to the canonical pair `mu_m^2(X_B)` and `g_c(X_B)`. The coupling is not decoration; it is coequal with the range because local tests measure coupled residuals, not naked fields.

**Claim ceiling:** {CLAIM_CEILING}

## Source Register

{md_table(sources)}

## Canonicalization Derivation Audit

{md_table(canonical)}

## Field-Redefinition Invariant Pivot

{md_table(pivots)}

## First-Fill Row Selection

{md_table(first_fill)}

## Runner Feed Update

{md_table(runner)}

## Claim Gates

{md_table(gates)}

## Decision Ledger

{md_table(decisions)}

## Next Target

{md_table(next_target)}

## Validation

{md_table(validation)}
"""
    (ROOT / DOC_PATH).write_text(body, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    canonical = canonical_audit_rows()
    pivots = invariant_pivot_rows()
    first_fill = first_fill_rows()
    runner = runner_feed_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, canonical, pivots, first_fill, gates)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(CANONICAL_AUDIT_PATH, canonical)
    write_csv(INVARIANT_PIVOT_PATH, pivots)
    write_csv(FIRST_FILL_PATH, first_fill)
    write_csv(RUNNER_FEED_PATH, runner)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_LEDGER_PATH, decisions)
    write_csv(NEXT_TARGET_PATH, next_target)
    write_csv(VALIDATION_PATH, validation)
    write_doc(sources, canonical, pivots, first_fill, runner, gates, decisions, next_target, validation)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"1384 validation failed: {failed}")
    print(STATUS)
    print(ROOT / DOC_PATH)
    print(ROOT / VALIDATION_PATH)


if __name__ == "__main__":
    main()

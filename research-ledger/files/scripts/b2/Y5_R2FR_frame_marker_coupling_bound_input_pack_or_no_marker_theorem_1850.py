from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
MICROSCOPE_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1850"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1850-Y5-R2FR-frame-marker-coupling-bound-input-pack-or-no-marker-theorem.md"


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1850_SOURCE_REGISTER.csv",
    "no_marker_theorem": RESIDUALS / "P8_Y5_PARENT_QLOC_1850_NO_MARKER_THEOREM_ATTEMPT.csv",
    "surviving_marker": RESIDUALS / "P8_Y5_PARENT_QLOC_1850_SURVIVING_MARKER_FAMILY_AUDIT.csv",
    "partial_theorem": RESIDUALS / "P8_Y5_PARENT_QLOC_1850_PARTIAL_NO_MARKER_THEOREM.csv",
    "bound_input": RESIDUALS / "P8_Y5_PARENT_QLOC_1850_FRAME_MARKER_BOUND_INPUT_PACK.csv",
    "projection": RESIDUALS / "P8_Y5_PARENT_QLOC_1850_ARENA_PROJECTION_ROWS.csv",
    "envelope": RESIDUALS / "P8_Y5_PARENT_QLOC_1850_QBARXT_TOTAL_ENVELOPE.csv",
    "dependency": RESIDUALS / "P8_Y5_PARENT_QLOC_1850_DEPENDENCY_LINKS.csv",
    "refusal": RESIDUALS / "P8_Y5_PARENT_QLOC_1850_PLACEHOLDER_REFUSAL_RUNNER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1850_CLAIM_GATE.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1850_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1850_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1850_VALIDATION.csv",
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def ensure_dirs() -> None:
    for path in [RESIDUALS, MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
        path.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def boolish(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def source_path(relative_path: str) -> str:
    return rel(ROOT / relative_path)


def build_rows_map() -> dict[str, list[dict[str, Any]]]:
    source_rows = [
        {
            "source_id": "SRC1850_0_1849_handoff",
            "source_path": source_path("1849-Y5-R2FR-qbarXT-source-zero-or-bounded-coupling-row.md"),
            "needle": "NEXT1849_0_primary",
            "use": "selected 1850 target and qbarXT component envelope handoff",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1850_1_1028_bound_pack",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_R10_1028_FRAME_MARKER_BOUND_INPUT_PACK.csv"),
            "needle": "FMB1028_10_total_qbarXT_envelope",
            "use": "older frame/marker bound-row schema",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1850_2_1028_no_marker",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_R10_1028_NO_MARKER_THEOREM_AUDIT.csv"),
            "needle": "NM1028_6_verdict",
            "use": "prior no-marker theorem gate",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1850_3_1046_constant_split",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_R10_1046_CONSTANT_MARKER_SPLIT_AUDIT.csv"),
            "needle": "CMA1046_5_verdict",
            "use": "constant and material marker split",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1850_4_1046_marker_coefficients",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_R10_1046_QBAR_MARKER_COEFFICIENT_ROWS.csv"),
            "needle": "QMC1046_3_qbar_marker_abs",
            "use": "marker coefficient row template",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1850_5_1676_object_language",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1676_OBJECT_LANGUAGE_NO_MARKER_THEOREM_ATTEMPT.csv"),
            "needle": "NoSourceOnlySpeciesSlot",
            "use": "object-language no source-only species-slot attempt",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1850_6_1757_no_linear_marker",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1757_NO_LINEAR_MARKER_THEOREM_ATTEMPT.csv"),
            "needle": "NLM1757_6_verdict",
            "use": "no-linear-marker theorem attempt",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1850_7_1761_direct_vertex",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1761_DIRECT_VERTEX_AND_NO_MARKER_AUDIT.csv"),
            "needle": "DV1761_5_verdict",
            "use": "direct matter/source vertex exclusion audit",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1850_8_1813_alpha_marker_schema",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1813_ALPHA_MARKER_RESIDUAL_ROW_SCHEMA.csv"),
            "needle": "AMR1813_5_total",
            "use": "alpha marker residual schema",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1850_9_965_countermodel_review",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_R10_965_MARKER_COUNTERMODEL_REVIEW.csv"),
            "needle": "MC965_5_post_readout_EFT_marker",
            "use": "surviving marker countermodels",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1850_10_974_counterexamples",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_R10_974_MARKER_COUNTEREXAMPLE_AUDIT.csv"),
            "needle": "MCE974_5_verdict",
            "use": "marker/source counterexample audit",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1850_11_975_classification",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_R10_975_MARKER_CLASSIFICATION.csv"),
            "needle": "MC975_6_verdict",
            "use": "marker family classification",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1850_12_980_functor",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_R10_980_NO_MARKER_FUNCTOR_THEOREM_ATTEMPT.csv"),
            "needle": "NMF980_7_verdict",
            "use": "functorial no-marker theorem attempt",
            "status": "FOUND",
            "valid_for_claim": False,
        },
    ]

    no_marker_rows = [
        {
            "attempt_id": "NMT1850_0_target",
            "claim_piece": "ordinary matter carries no independent X-marker",
            "formal_statement": "For every admissible ordinary matter sector A, S_A depends on X only through descended observed structures O(q(Phi)) and quotient-owned constants theta_A(q).",
            "derived_status": "TARGET_STATEMENT",
            "proof_status": "CONDITIONAL_ONLY",
            "missing_or_blocker": "parent matter functor, constant ownership, hidden frame silence and boundary support silence are not signed in one clause",
            "observable_impact": "would set qbar_constants=qbar_marker=qbar_source_weight=0",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "NMT1850_1_fixed_spurion_exclusion",
            "claim_piece": "fixed external covectors and active labels are illegal",
            "formal_statement": "A fixed active marker ell_X in E_X* is not a natural quotient functor and is excluded by parent object-language hygiene.",
            "derived_status": "PARTIAL_THEOREM",
            "proof_status": "SIGNED_AS_DESIGN_CONTRACT_NOT_FULL_PARENT_DERIVATION",
            "missing_or_blocker": "does not exclude co-moving material/domain/source markers",
            "observable_impact": "kills the weakest linear marker counterexample only",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "NMT1850_2_no_invariant_linear_covector",
            "claim_piece": "no invariant first-order X covector from empty vertical structure",
            "formal_statement": "If the vertical fibre has no parent-owned covector, F_1(v_X)=0 for fixed empty-background marker attempts.",
            "derived_status": "PARTIAL_THEOREM",
            "proof_status": "CONDITIONAL",
            "missing_or_blocker": "material constants and domain/readout data can supply covectors after matter is included",
            "observable_impact": "supports local extremum/amplitude route but not qbar_XT=0",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "NMT1850_3_co_moving_material_marker",
            "claim_piece": "material markers cannot source X",
            "formal_statement": "A material label m_A, isotope fraction, preparation marker, or readout class is either quotient-owned or absent from S_A.",
            "derived_status": "NOT_DERIVED",
            "proof_status": "COUNTERMODEL_SURVIVES",
            "missing_or_blocker": "co-moving material markers can descend with matter and still change source/test normalization",
            "observable_impact": "requires b_A and b_marker bound rows",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "NMT1850_4_constant_superselection",
            "claim_piece": "masses, charges, alpha_EM and clock constants are X-independent",
            "formal_statement": "Lie_v theta_A=0 for all constants used by ordinary matter, clocks and EM readout.",
            "derived_status": "NOT_PARENT_SIGNED",
            "proof_status": "OPEN",
            "missing_or_blocker": "constant-sector target spaces are continuous unless topological/superselection ownership is supplied",
            "observable_impact": "requires b_A and b_alpha rows for WEP/clocks/fine-structure",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "NMT1850_5_source_weight_and_boundary",
            "claim_piece": "source weights and boundary/support terms are absent",
            "formal_statement": "No kappa_A, domain class chi_D, support shift, boundary flux, non-Hilbert tail, or post-readout EFT term survives local projection.",
            "derived_status": "NOT_DERIVED",
            "proof_status": "COUNTERMODEL_SURVIVES",
            "missing_or_blocker": "source-only weights, support shifts and post-readout reductions are not eliminated by no-linear-marker hygiene",
            "observable_impact": "requires delta_kappa_A, q_nonH, Delta_W_support, q_domain and q_boundary rows",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "NMT1850_6_verdict",
            "claim_piece": "full no-marker theorem",
            "formal_statement": "NMT1850_1 and NMT1850_2 are useful partial results, but NMT1850_3 through NMT1850_5 remain live.",
            "derived_status": "FAIL_CURRENT_CLAIM",
            "proof_status": "NO_MARKER_THEOREM_NOT_CLOSED",
            "missing_or_blocker": "ordinary matter constants, material markers, source weights and boundary/source tails need theorem-zero or numeric bounds",
            "observable_impact": "stage frame/marker coupling bound input pack; do not claim local GR or R10 pass from zero",
            "valid_for_claim": False,
        },
    ]

    surviving_marker_rows = [
        {
            "marker_id": "SMF1850_0_fixed_spurion",
            "family": "fixed active external spurion/covector",
            "status_after_1850": "CONDITIONALLY_EXCLUDED",
            "why": "not a natural quotient-owned parent object and violates the object-language hygiene gate",
            "required_bound_or_theorem": "object-language exclusion row plus no hidden replacement marker",
            "blocks_full_zero_claim": False,
            "valid_for_claim": False,
        },
        {
            "marker_id": "SMF1850_1_common_frame",
            "family": "hidden common Weyl/conformal matter frame",
            "status_after_1850": "LIVE_UNLESS_CG_ZERO_OR_BOUNDED",
            "why": "a common A_g(X) can be WEP-blind while still moving R10/PPN/clock normalization",
            "required_bound_or_theorem": "c_g theorem-zero or numeric bound",
            "blocks_full_zero_claim": True,
            "valid_for_claim": False,
        },
        {
            "marker_id": "SMF1850_2_disformal_frame",
            "family": "hidden disformal/profile matter frame",
            "status_after_1850": "LIVE_UNLESS_BDIS_ZERO_OR_BOUNDED",
            "why": "disformal terms can vanish in one limit but survive in clocks/orbits/PPN projections",
            "required_bound_or_theorem": "b_dis theorem-zero or projection-specific bound",
            "blocks_full_zero_claim": True,
            "valid_for_claim": False,
        },
        {
            "marker_id": "SMF1850_3_material_constants",
            "family": "m_A, mass ratios, isotope/material labels, preparation markers",
            "status_after_1850": "LIVE_UNLESS_BA_ZERO_OR_BOUNDED",
            "why": "co-moving material labels can descend with matter and are not killed by fixed-spurion exclusion",
            "required_bound_or_theorem": "b_A/b_marker theorem-zero or source-backed sensitivity bounds",
            "blocks_full_zero_claim": True,
            "valid_for_claim": False,
        },
        {
            "marker_id": "SMF1850_4_alpha_clock_constants",
            "family": "alpha_EM, gauge/binding constants, clock transition markers",
            "status_after_1850": "LIVE_UNLESS_BALPHA_ZERO_OR_BOUNDED",
            "why": "clock/fine-structure observables directly constrain constant drift but do not prove zero without ownership",
            "required_bound_or_theorem": "b_alpha theorem-zero or clock/fine-structure bound",
            "blocks_full_zero_claim": True,
            "valid_for_claim": False,
        },
        {
            "marker_id": "SMF1850_5_source_boundary_tail",
            "family": "source-only weights, domain classes, support shifts, boundary/non-Hilbert current",
            "status_after_1850": "LIVE_UNLESS_SOURCE_TAIL_ZERO_OR_BOUNDED",
            "why": "these enter local source normalization even if geometry and matter functors look clean",
            "required_bound_or_theorem": "delta_kappa_A, q_nonH, Delta_W_support, q_domain, q_boundary bound rows",
            "blocks_full_zero_claim": True,
            "valid_for_claim": False,
        },
    ]

    partial_theorem_rows = [
        {
            "theorem_id": "PT1850_0_fixed_spurion_no_go",
            "theorem": "Fixed active marker no-go",
            "statement": "A non-dynamical labelled marker used only to generate a local X-force is not an admissible parent quotient functor.",
            "proof_sketch": "It is not pulled back from q(Phi), not varied as matter, and not a gauge redundancy; retaining it would add a new external background structure.",
            "scope": "fixed external labels and empty-background linear covectors",
            "what_it_does_not_prove": "does not remove co-moving material markers, common frame factors, constant sectors, or boundary/support tails",
            "status": "PARTIAL_PROGRESS",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "PT1850_1_first_order_empty_fibre",
            "theorem": "Empty-fibre first-order silence",
            "statement": "If the X-fibre has no parent-owned covector and the ordinary matter functor sees only quotient-owned observed structures, the empty-background F_1 term vanishes.",
            "proof_sketch": "There is no natural E_X* object to contract with v_X; the chain-rule variation factors through Dq(v_X)=0.",
            "scope": "geometric/source-zero theorem under strict functorial and constant-superselection assumptions",
            "what_it_does_not_prove": "does not sign those assumptions for the current MTS parent action",
            "status": "CONDITIONAL_PROGRESS",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "PT1850_2_no_claim_boundary",
            "theorem": "No hidden replacement theorem",
            "statement": "Any theorem-zero use must also forbid replacement markers: A_g(X), B_dis(X), theta_A(X), kappa_A(X), chi_D(X), q_nonH and boundary/support shifts.",
            "proof_sketch": "Otherwise qbar_XT can return under a different name while the visible matter action appears quotient-invariant.",
            "scope": "guardrail for future parent action clauses",
            "what_it_does_not_prove": "does not provide numeric values or external bounds",
            "status": "GUARDRAIL_ACTIVE",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]

    bound_input_rows = [
        {
            "row_id": "FMB1850_0_cg",
            "symbol": "c_g",
            "definition": "common Weyl/conformal derivative d ln A_g/dXhat for ordinary matter or source frame",
            "formula_or_bound": "|c_g| <= MISSING_COMMON_FRAME_BOUND",
            "current_value": "MISSING_CG_BOUND_OR_ZERO_THEOREM",
            "units": "dimensionless_per_normalized_Xhat",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_R10_1028_FRAME_MARKER_BOUND_INPUT_PACK.csv"),
            "observable_link": "R10;PPN;clock;WEP_common_mode",
            "status": "MISSING_FRAME_LEAK_ZERO_OR_NUMERIC_BOUND",
            "valid_for_claim": False,
        },
        {
            "row_id": "FMB1850_1_bdis",
            "symbol": "b_dis",
            "definition": "representative disformal/profile-normalized matter frame derivative",
            "formula_or_bound": "|b_dis| <= MISSING_DISFORMAL_BOUND",
            "current_value": "MISSING_BDIS_BOUND_OR_ZERO_THEOREM",
            "units": "dimensionless_or_declared_profile_units",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_R10_1046_QBAR_MARKER_COEFFICIENT_ROWS.csv"),
            "observable_link": "PPN;clock;orbital;R10",
            "status": "MISSING_DISFORMAL_ZERO_OR_NUMERIC_BOUND",
            "valid_for_claim": False,
        },
        {
            "row_id": "FMB1850_2_bA",
            "symbol": "b_A",
            "definition": "vertical derivative of material mass/species constants d ln m_A/dXhat or equivalent sensitivity",
            "formula_or_bound": "|b_A| <= MISSING_MATERIAL_CONSTANT_BOUND",
            "current_value": "MISSING_BA_BOUND_OR_ZERO_THEOREM",
            "units": "dimensionless_per_normalized_Xhat",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_R10_1046_CONSTANT_MARKER_SPLIT_AUDIT.csv"),
            "observable_link": "WEP;clock;R10;particle_mass",
            "status": "MISSING_MATERIAL_CONSTANT_ZERO_OR_NUMERIC_BOUND",
            "valid_for_claim": False,
        },
        {
            "row_id": "FMB1850_3_balpha",
            "symbol": "b_alpha",
            "definition": "vertical derivative of alpha_EM/gauge/binding/clock readout constants",
            "formula_or_bound": "|b_alpha| <= MISSING_ALPHA_CLOCK_BOUND",
            "current_value": "MISSING_BALPHA_BOUND_OR_ZERO_THEOREM",
            "units": "dimensionless_per_normalized_Xhat",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1813_ALPHA_MARKER_RESIDUAL_ROW_SCHEMA.csv"),
            "observable_link": "clock;fine_structure;EM;R10",
            "status": "MISSING_ALPHA_CONSTANT_ZERO_OR_NUMERIC_BOUND",
            "valid_for_claim": False,
        },
        {
            "row_id": "FMB1850_4_bmarker",
            "symbol": "b_marker",
            "definition": "vertical derivative of material/source/preparation/readout marker channel",
            "formula_or_bound": "|b_marker| <= MISSING_MARKER_CHANNEL_BOUND",
            "current_value": "MISSING_BMARKER_BOUND_OR_ZERO_THEOREM",
            "units": "dimensionless",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_R10_975_MARKER_CLASSIFICATION.csv"),
            "observable_link": "WEP_source_charge;R10;clock;readout",
            "status": "MISSING_NO_MARKER_THEOREM_OR_NUMERIC_BOUNDS",
            "valid_for_claim": False,
        },
        {
            "row_id": "FMB1850_5_delta_kappa_A",
            "symbol": "delta_kappa_A",
            "definition": "relative source-only matter prefactor or species/source current weight kappa_A/kappa_univ - 1",
            "formula_or_bound": "|delta_kappa_A| <= MISSING_SOURCE_WEIGHT_BOUND",
            "current_value": "MISSING_DELTA_KAPPA_A_BOUND_OR_ZERO_THEOREM",
            "units": "dimensionless",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1761_DIRECT_VERTEX_AND_NO_MARKER_AUDIT.csv"),
            "observable_link": "WEP_source_charge;orbital;R10_source_mass",
            "status": "MISSING_UNIVERSAL_SOURCE_CURRENT_OR_NUMERIC_BOUND",
            "valid_for_claim": False,
        },
        {
            "row_id": "FMB1850_6_qnonH",
            "symbol": "q_nonH",
            "definition": "ordinary source projection from non-Hilbert current, torsion/connection tail, projector, or memory exchange",
            "formula_or_bound": "|q_nonH| <= MISSING_NONHILBERT_SOURCE_BOUND",
            "current_value": "MISSING_QNONH_BOUND_OR_ZERO_THEOREM",
            "units": "dimensionless_after_source_normalization",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_R10_974_MARKER_COUNTEREXAMPLE_AUDIT.csv"),
            "observable_link": "R10;orbital;source_normalization;boundary",
            "status": "MISSING_HIDDEN_SOURCE_ZERO_OR_NUMERIC_BOUND",
            "valid_for_claim": False,
        },
        {
            "row_id": "FMB1850_7_Delta_W_support",
            "symbol": "Delta_W_support",
            "definition": "worldtube/support/domain shift under local projection or observed-frame choice",
            "formula_or_bound": "|Delta_W_support| <= MISSING_SUPPORT_SHIFT_BOUND",
            "current_value": "MISSING_SUPPORT_SHIFT_BOUND_OR_ZERO_THEOREM",
            "units": "dimensionless_or_projection_declared",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_R10_974_MARKER_COUNTEREXAMPLE_AUDIT.csv"),
            "observable_link": "orbital;R10;boundary;local_GR",
            "status": "MISSING_SUPPORT_SHIFT_ZERO_OR_NUMERIC_BOUND",
            "valid_for_claim": False,
        },
        {
            "row_id": "FMB1850_8_qdomain",
            "symbol": "q_domain",
            "definition": "domain class or chi_D selector contribution to source/test normalization",
            "formula_or_bound": "|q_domain| <= MISSING_DOMAIN_CLASS_BOUND",
            "current_value": "MISSING_QDOMAIN_BOUND_OR_ZERO_THEOREM",
            "units": "dimensionless",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_R10_965_MARKER_COUNTERMODEL_REVIEW.csv"),
            "observable_link": "WEP;R10;orbital;readout",
            "status": "MISSING_DOMAIN_MARKER_ZERO_OR_NUMERIC_BOUND",
            "valid_for_claim": False,
        },
        {
            "row_id": "FMB1850_9_qboundary",
            "symbol": "q_boundary",
            "definition": "boundary/local projection flux contribution to qbar_XT",
            "formula_or_bound": "|q_boundary| <= MISSING_BOUNDARY_FLUX_BOUND",
            "current_value": "MISSING_QBOUNDARY_BOUND_OR_ZERO_THEOREM",
            "units": "dimensionless_after_boundary_normalization",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_R10_974_MARKER_COUNTEREXAMPLE_AUDIT.csv"),
            "observable_link": "boundary;orbital;local_GR;R10",
            "status": "MISSING_BOUNDARY_FLUX_ZERO_OR_NUMERIC_BOUND",
            "valid_for_claim": False,
        },
        {
            "row_id": "FMB1850_10_total_qbarXT_envelope",
            "symbol": "qbar_XT_bound_abs",
            "definition": "absolute no-cancellation envelope over frame, marker, constants, source weight and non-Hilbert/support components",
            "formula_or_bound": "|qbar_XT| <= |tau_g c_g|+|tau_dis b_dis|+sum_A|s_A b_A|+|s_alpha b_alpha|+|b_marker|+|delta_kappa_A|+|q_nonH|+|Delta_W_support|+|q_domain|+|q_boundary|",
            "current_value": "MISSING_COMPONENT_VALUES",
            "units": "dimensionless_after_declared_normalization",
            "source_path": source_path("1849-Y5-R2FR-qbarXT-source-zero-or-bounded-coupling-row.md"),
            "observable_link": "R10;WEP;clock;PPN;orbital;local_GR",
            "status": "SCHEMA_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "row_id": "FMB1850_11_claim_gate",
            "symbol": "claim_gate",
            "definition": "no R10/local-GR/PPN/clock/orbital claim until every component is theorem-zero or source-backed numeric",
            "formula_or_bound": "claim_allowed iff all component rows are valid_for_claim=true and no MISSING_* markers remain",
            "current_value": "CLAIM_BLOCKED",
            "units": "gate",
            "source_path": source_path("1849-Y5-R2FR-qbarXT-source-zero-or-bounded-coupling-row.md"),
            "observable_link": "all local arenas",
            "status": "CLAIM_BLOCKED",
            "valid_for_claim": False,
        },
    ]

    projection_rows = [
        {
            "projection_id": "APR1850_0_tau_R10",
            "symbol": "tau_R10",
            "arena": "R10 short-range alpha(lambda)",
            "uses_components": "c_g;b_dis;b_A;b_alpha;b_marker;delta_kappa_A;q_nonH;Delta_W_support;q_domain;q_boundary",
            "formula_or_contract": "alpha_R10(lambda_X)=K_X Qbar_XH(lambda_X) qbar_XT_bound_abs tau_R10(lambda_X)",
            "current_value": "MISSING_TAU_R10_AND_COMPONENT_VALUES",
            "units": "dimensionless_projection_or_declared",
            "status": "MISSING_ARENA_PROJECTION",
            "valid_for_claim": False,
        },
        {
            "projection_id": "APR1850_1_tau_PPN",
            "symbol": "tau_PPN",
            "arena": "local weak-field/PPN",
            "uses_components": "c_g;b_dis;q_nonH;Delta_W_support;q_boundary",
            "formula_or_contract": "PPN_residual_vector <= tau_PPN dot absolute_component_vector",
            "current_value": "MISSING_TAU_PPN_AND_COMPONENT_VALUES",
            "units": "dimensionless_projection_or_declared",
            "status": "MISSING_ARENA_PROJECTION",
            "valid_for_claim": False,
        },
        {
            "projection_id": "APR1850_2_tau_clock",
            "symbol": "tau_clock",
            "arena": "clocks/fine-structure/EM readout",
            "uses_components": "c_g;b_A;b_alpha;b_marker;q_nonH",
            "formula_or_contract": "clock_residual <= tau_clock dot absolute_component_vector",
            "current_value": "MISSING_TAU_CLOCK_AND_COMPONENT_VALUES",
            "units": "dimensionless_projection_or_declared",
            "status": "MISSING_ARENA_PROJECTION",
            "valid_for_claim": False,
        },
        {
            "projection_id": "APR1850_3_tau_orbital",
            "symbol": "tau_orbital",
            "arena": "orbital/source-support systems",
            "uses_components": "delta_kappa_A;q_nonH;Delta_W_support;q_domain;q_boundary;c_g",
            "formula_or_contract": "orbital_residual <= tau_orbital dot absolute_component_vector",
            "current_value": "MISSING_TAU_ORBITAL_AND_COMPONENT_VALUES",
            "units": "dimensionless_projection_or_declared",
            "status": "MISSING_ARENA_PROJECTION",
            "valid_for_claim": False,
        },
        {
            "projection_id": "APR1850_4_tau_WEP",
            "symbol": "tau_WEP",
            "arena": "WEP/source charge",
            "uses_components": "b_A;b_marker;delta_kappa_A;q_domain",
            "formula_or_contract": "eta_AB <= tau_WEP dot absolute_differential_component_vector",
            "current_value": "MISSING_TAU_WEP_AND_COMPONENT_VALUES",
            "units": "dimensionless_projection_or_declared",
            "status": "MISSING_ARENA_PROJECTION",
            "valid_for_claim": False,
        },
        {
            "projection_id": "APR1850_5_tau_alphaEM",
            "symbol": "tau_alphaEM",
            "arena": "EM/fine-structure",
            "uses_components": "b_alpha;b_A;b_marker;c_g",
            "formula_or_contract": "alpha_EM_residual <= tau_alphaEM dot absolute_component_vector",
            "current_value": "MISSING_TAU_ALPHAEM_AND_COMPONENT_VALUES",
            "units": "dimensionless_projection_or_declared",
            "status": "MISSING_ARENA_PROJECTION",
            "valid_for_claim": False,
        },
    ]

    envelope_rows = [
        {
            "envelope_id": "ENV1850_0_component_vector",
            "quantity": "absolute_component_vector",
            "formula": "(|c_g|,|b_dis|,|b_A|,|b_alpha|,|b_marker|,|delta_kappa_A|,|q_nonH|,|Delta_W_support|,|q_domain|,|q_boundary|)",
            "rule": "all unknown signs are discarded",
            "status": "GUARDRAIL_ACTIVE",
            "valid_for_claim": False,
        },
        {
            "envelope_id": "ENV1850_1_no_cancellation",
            "quantity": "qbar_XT_bound_abs",
            "formula": "sum of absolute projected component magnitudes",
            "rule": "no cancellation between frame, marker, source and boundary tails may be used to pass local tests",
            "status": "GUARDRAIL_ACTIVE",
            "valid_for_claim": False,
        },
        {
            "envelope_id": "ENV1850_2_claim_block",
            "quantity": "local_claim",
            "formula": "claim_allowed=false while any component/projection has MISSING_* or valid_for_claim=false",
            "rule": "schema can guide work but cannot be scored as evidence",
            "status": "CLAIM_BLOCKED",
            "valid_for_claim": False,
        },
    ]

    dependency_rows = [
        {
            "dependency_id": "DEP1850_0_no_marker_to_qbar_zero",
            "quantity": "qbar_XT=0",
            "requires": "full no-marker theorem plus parent matter functor plus boundary/source silence",
            "status": "FAIL_CURRENT_CLAIM",
            "reason": "partial no-spurion theorem does not eliminate live marker families",
            "next_action": "do not set qbar_XT=0; retain bound envelope",
            "valid_for_claim": False,
        },
        {
            "dependency_id": "DEP1850_1_bound_pack_to_R10",
            "quantity": "alpha_R10(lambda_X)",
            "requires": "K_X;Qbar_XH(lambda_X);lambda_X;real alpha_bound(lambda);qbar_XT_bound_abs;tau_R10",
            "status": "BLOCKED_BY_COMPONENT_VALUES_AND_PROJECTION",
            "reason": "1850 supplies rows, not numeric bounds",
            "next_action": "source first real c_g/b_A/b_alpha/q_nonH/projection inputs",
            "valid_for_claim": False,
        },
        {
            "dependency_id": "DEP1850_2_local_GR_to_zero_or_bounds",
            "quantity": "local GR limit",
            "requires": "all frame/marker/source/boundary components theorem-zero or below local arena bounds",
            "status": "BLOCKED",
            "reason": "local GR cannot be declared from covariance alone if matter/source couplings are unsigned",
            "next_action": "use no-cancellation component envelope",
            "valid_for_claim": False,
        },
        {
            "dependency_id": "DEP1850_3_no_cancellation",
            "quantity": "total local coupling envelope",
            "requires": "absolute component sum",
            "status": "GUARDRAIL_ACTIVE",
            "reason": "unknown components cannot be hidden by sign choices",
            "next_action": "carry absolute envelopes into R10/WEP/clock/PPN/orbital runners",
            "valid_for_claim": False,
        },
    ]

    refusal_rows = [
        {
            "refusal_id": "REF1850_0_full_no_marker",
            "attempted_claim": "full no-marker theorem closes",
            "input_status": "FAIL_CURRENT_CLAIM",
            "runner_result": "BLOCKED",
            "blocked_by": "NMT1850_3_co_moving_material_marker;NMT1850_4_constant_superselection;NMT1850_5_source_weight_and_boundary",
            "score_eligible": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF1850_1_qbarXT_zero",
            "attempted_claim": "qbar_XT=0",
            "input_status": "NO_MARKER_THEOREM_NOT_CLOSED",
            "runner_result": "BLOCKED",
            "blocked_by": "NMT1850_6_verdict;DEP1850_0_no_marker_to_qbar_zero",
            "score_eligible": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF1850_2_bound_values",
            "attempted_claim": "qbar_XT_bound_abs numeric",
            "input_status": "SCHEMA_READY_VALUES_MISSING",
            "runner_result": "BLOCKED",
            "blocked_by": "FMB1850_0_cg through FMB1850_10_total_qbarXT_envelope;APR1850_0_tau_R10 through APR1850_5_tau_alphaEM",
            "score_eligible": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "refusal_id": "REF1850_3_local_GR",
            "attempted_claim": "local GR recovered",
            "input_status": "COUPLING_ROWS_UNSIGNED",
            "runner_result": "BLOCKED",
            "blocked_by": "matter/source coupling envelope not theorem-zero or source-bounded",
            "score_eligible": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]

    claim_gate_rows = [
        {
            "gate_id": "CG1850_0_fixed_spurion",
            "claim": "fixed active markers excluded",
            "gate_pass": True,
            "reason": "partial object-language hygiene supports this limited exclusion",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1850_1_no_marker_full",
            "claim": "all material/source/readout markers excluded",
            "gate_pass": False,
            "reason": "co-moving material, constants, source weights and boundary/source tails survive",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1850_2_bound_rows_complete",
            "claim": "frame/marker bound rows numeric and sourced",
            "gate_pass": False,
            "reason": "all component values are still MISSING_*",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1850_3_arena_projection_complete",
            "claim": "R10/PPN/clock/orbital/WEP projections complete",
            "gate_pass": False,
            "reason": "tau rows are schema-only",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1850_4_local_GR",
            "claim": "local GR branch passes",
            "gate_pass": False,
            "reason": "coupling rows are neither zero-proven nor source-bounded",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC1850_0_partial_win",
            "decision": "1850 proves a useful partial theorem only.",
            "because": "fixed external spurions and empty-background covectors can be excluded, but live matter/source markers remain.",
            "next_action": "keep the partial theorem as a guardrail, not as a local-GR claim",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1850_1_bound_pack",
            "decision": "The bound input pack is now the clean working object.",
            "because": "c_g, b_dis, b_A, b_alpha, b_marker, delta_kappa_A, q_nonH and support/domain/boundary tails are explicit rows with arenas.",
            "next_action": "source or theorem-zero the rows one by one",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1850_2_best_route",
            "decision": "Next route should source the first real local coupling bound inputs.",
            "because": "attempting another global no-marker theorem without new parent action clauses will likely loop.",
            "next_action": "1851-Y5-R2FR-first-real-local-coupling-bound-source-table.md",
            "valid_for_claim": False,
        },
    ]

    next_target_rows = [
        {
            "route_id": "NEXT1850_0_primary",
            "next_target": "1851-Y5-R2FR-first-real-local-coupling-bound-source-table.md",
            "script": "scripts/Y5_R2FR_first_real_local_coupling_bound_source_table_1851.py",
            "objective": "source or bound the first real c_g, b_A, b_alpha, q_nonH, support/domain/boundary and arena-projection rows without making a local-GR claim",
            "selection_status": "selected",
            "success_condition": "at least one component row becomes source-backed numeric or theorem-zero while all incomplete rows remain nonclaim",
        },
        {
            "route_id": "NEXT1850_1_parallel",
            "next_target": "1851b-Y5-R2FR-parent-action-no-marker-clause-signature.md",
            "script": "scripts/Y5_R2FR_parent_action_no_marker_clause_signature_1851b.py",
            "objective": "write the exact parent action clauses that would sign full no-marker/constant/source-tail silence",
            "selection_status": "held",
            "success_condition": "parent action explicitly forbids every surviving marker family without post-hoc deletion",
        },
    ]

    return {
        "source_register": source_rows,
        "no_marker_theorem": no_marker_rows,
        "surviving_marker": surviving_marker_rows,
        "partial_theorem": partial_theorem_rows,
        "bound_input": bound_input_rows,
        "projection": projection_rows,
        "envelope": envelope_rows,
        "dependency": dependency_rows,
        "refusal": refusal_rows,
        "claim_gate": claim_gate_rows,
        "decision": decision_rows,
        "next_target": next_target_rows,
    }


def copy_outputs(include_validation: bool = False) -> None:
    keys = list(OUTPUTS)
    if not include_validation:
        keys = [key for key in keys if key != "validation"]
    for key in keys:
        src = OUTPUTS[key]
        if not src.exists():
            continue
        for dst_dir in [MICROSCOPE_RESIDUALS, QUARANTINE]:
            shutil.copy2(src, dst_dir / src.name)
        shutil.copy2(src, RAB_QUEUE / f"JR1850_{src.name}")


def check_sources(source_rows: list[dict[str, Any]]) -> tuple[bool, str]:
    missing: list[str] = []
    for row in source_rows:
        path = ROOT / str(row["source_path"])
        if not path.exists():
            missing.append(str(row["source_path"]))
    return not missing, "missing: " + "; ".join(missing) if missing else "all cited source paths exist"


def check_needles(source_rows: list[dict[str, Any]]) -> tuple[bool, str]:
    missing: list[str] = []
    for row in source_rows:
        path = ROOT / str(row["source_path"])
        needle = str(row["needle"])
        if path.exists() and needle not in path.read_text(encoding="utf-8", errors="ignore"):
            missing.append(f"{row['source_path']}::{needle}")
    return not missing, "missing: " + "; ".join(missing) if missing else "all cited source needles are present"


def check_csv_parse() -> tuple[bool, str]:
    malformed: list[str] = []
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        try:
            read_csv(path)
        except Exception as exc:  # pragma: no cover - validation ledger records exact parse failure.
            malformed.append(f"{path.name}: {exc}")
    return not malformed, "malformed: " + "; ".join(malformed) if malformed else "all generated 1850 CSVs parse"


def check_branch_copies() -> tuple[bool, str]:
    missing: list[str] = []
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        expected = [
            MICROSCOPE_RESIDUALS / path.name,
            QUARANTINE / path.name,
            RAB_QUEUE / f"JR1850_{path.name}",
        ]
        for item in expected:
            if not item.exists():
                missing.append(str(item))
    return not missing, "missing copies: " + "; ".join(missing) if missing else "branch/quarantine/queue copies exist"


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = []

    ok, detail = check_sources(rows_map["source_register"])
    checks.append(("VAL1850_0_sources_exist", ok, detail))
    ok, detail = check_needles(rows_map["source_register"])
    checks.append(("VAL1850_1_needles_present", ok, detail))

    checks.append(
        (
            "VAL1850_2_no_marker_blocks",
            any(
                row["attempt_id"] == "NMT1850_6_verdict"
                and row["derived_status"] == "FAIL_CURRENT_CLAIM"
                and not boolish(row["valid_for_claim"])
                for row in rows_map["no_marker_theorem"]
            ),
            "full no-marker theorem remains blocked",
        )
    )
    checks.append(
        (
            "VAL1850_3_partial_theorem_limited",
            any(row["theorem_id"] == "PT1850_0_fixed_spurion_no_go" for row in rows_map["partial_theorem"])
            and all(not boolish(row["claim_allowed"]) for row in rows_map["partial_theorem"]),
            "partial theorem rows exist but do not allow local claims",
        )
    )
    checks.append(
        (
            "VAL1850_4_surviving_markers_block",
            all(
                not boolish(row["valid_for_claim"])
                and (
                    not boolish(row["blocks_full_zero_claim"])
                    or str(row["status_after_1850"]).startswith("LIVE_")
                )
                for row in rows_map["surviving_marker"]
            ),
            "surviving marker families remain nonclaim and live where relevant",
        )
    )
    checks.append(
        (
            "VAL1850_5_bound_rows_nonclaim",
            all(not boolish(row["valid_for_claim"]) for row in rows_map["bound_input"])
            and any(row["row_id"] == "FMB1850_10_total_qbarXT_envelope" and row["status"] == "SCHEMA_READY_VALUES_MISSING" for row in rows_map["bound_input"]),
            "bound input pack is staged but values-missing",
        )
    )
    checks.append(
        (
            "VAL1850_6_projection_rows_nonclaim",
            all(row["status"] == "MISSING_ARENA_PROJECTION" and not boolish(row["valid_for_claim"]) for row in rows_map["projection"]),
            "arena projection rows are schema-only",
        )
    )
    checks.append(
        (
            "VAL1850_7_no_cancellation_guard",
            any(row["envelope_id"] == "ENV1850_1_no_cancellation" and row["status"] == "GUARDRAIL_ACTIVE" for row in rows_map["envelope"]),
            "absolute no-cancellation envelope is active",
        )
    )
    checks.append(
        (
            "VAL1850_8_dependencies_block",
            any(row["dependency_id"] == "DEP1850_3_no_cancellation" and row["status"] == "GUARDRAIL_ACTIVE" for row in rows_map["dependency"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["dependency"]),
            "dependencies keep qbar/local-GR claims blocked",
        )
    )
    checks.append(
        (
            "VAL1850_9_refusal_runner_blocks",
            all(row["runner_result"] == "BLOCKED" and not boolish(row["claim_allowed"]) for row in rows_map["refusal"]),
            "placeholder/refusal runner blocks all claims",
        )
    )
    checks.append(
        (
            "VAL1850_10_claim_gates_blocked",
            all(not boolish(row["claim_allowed"]) for row in rows_map["claim_gate"]),
            "all claim gates keep claim_allowed=false",
        )
    )
    checks.append(
        (
            "VAL1850_11_decision_next",
            any(row["decision_id"] == "DEC1850_2_best_route" and "1851-Y5-R2FR-first-real-local-coupling-bound-source-table.md" in row["next_action"] for row in rows_map["decision"]),
            "decision ledger selects source-table route",
        )
    )
    checks.append(
        (
            "VAL1850_12_next_target_selected",
            any(row["route_id"] == "NEXT1850_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        )
    )
    checks.append(
        (
            "VAL1850_13_no_claim_flags",
            all(not boolish(row.get("valid_for_claim", False)) for rows in rows_map.values() for row in rows),
            "no valid_for_claim flags are true",
        )
    )
    checks.append(
        (
            "VAL1850_14_missing_rows_nonclaim",
            all(
                not boolish(row.get("valid_for_claim", False))
                for rows in rows_map.values()
                for row in rows
                if "MISSING_" in " ".join(str(value) for value in row.values())
            ),
            "MISSING_* rows stay nonclaim",
        )
    )
    ok, detail = check_csv_parse()
    checks.append(("VAL1850_15_csv_parse", ok, detail))
    ok, detail = check_branch_copies()
    checks.append(("VAL1850_16_branch_copies", ok, detail))

    pycache_path = ROOT / "scripts" / "__pycache__"
    checks.append(("VAL1850_17_pycache_absent", not pycache_path.exists(), "scripts __pycache__ absent"))

    formalization_outputs = list(FORMALIZATION.rglob("*1850*")) if FORMALIZATION.exists() else []
    checks.append(
        (
            "VAL1850_18_formalization_untouched",
            not formalization_outputs,
            "no 1850 outputs found under formalization-workbench",
        )
    )

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
            "check_id": "VAL1850_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1850 frame/marker coupling bound input pack or no-marker theorem",
        }
    )
    return validation_rows


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    lines = [header, sep]
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    return "\n".join(
        [
            "# 1850: Frame/Marker Coupling Bound Input Pack Or No-Marker Theorem",
            "",
            "**Current verdict:** the no-marker hunt makes real but limited progress. Fixed external spurions and empty-background linear covectors can be excluded as bad parent object-language, but co-moving material markers, constant sectors, common/hidden frames, source-only weights, post-readout reductions and boundary/support tails still survive. Therefore `qbar_XT=0`, local GR, R10, PPN, clock and orbital claims remain blocked until those rows are theorem-zero or source-backed numeric.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_path", "needle", "use", "status", "valid_for_claim"]),
            "",
            "## No-Marker Theorem Attempt",
            markdown_table(rows_map["no_marker_theorem"], ["attempt_id", "claim_piece", "formal_statement", "derived_status", "proof_status", "missing_or_blocker", "observable_impact", "valid_for_claim"]),
            "",
            "## Surviving Marker Families",
            markdown_table(rows_map["surviving_marker"], ["marker_id", "family", "status_after_1850", "why", "required_bound_or_theorem", "blocks_full_zero_claim", "valid_for_claim"]),
            "",
            "## Partial Theorems",
            markdown_table(rows_map["partial_theorem"], ["theorem_id", "theorem", "statement", "proof_sketch", "scope", "what_it_does_not_prove", "status", "claim_allowed", "valid_for_claim"]),
            "",
            "## Frame/Marker Bound Input Pack",
            markdown_table(rows_map["bound_input"], ["row_id", "symbol", "definition", "formula_or_bound", "current_value", "units", "source_path", "observable_link", "status", "valid_for_claim"]),
            "",
            "## Arena Projection Rows",
            markdown_table(rows_map["projection"], ["projection_id", "symbol", "arena", "uses_components", "formula_or_contract", "current_value", "units", "status", "valid_for_claim"]),
            "",
            "## Total Envelope",
            markdown_table(rows_map["envelope"], ["envelope_id", "quantity", "formula", "rule", "status", "valid_for_claim"]),
            "",
            "## Dependency Links",
            markdown_table(rows_map["dependency"], ["dependency_id", "quantity", "requires", "status", "reason", "next_action", "valid_for_claim"]),
            "",
            "## Refusal Runner",
            markdown_table(rows_map["refusal"], ["refusal_id", "attempted_claim", "input_status", "runner_result", "blocked_by", "score_eligible", "claim_allowed", "valid_for_claim"]),
            "",
            "## Claim Gates",
            markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "",
            "## Decisions",
            markdown_table(rows_map["decision"], ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This is not grim; it is finally pinned down. The coupling problem has stopped being a misty objection and become a row-by-row source table. The branch does not yet get to say 'derived local GR', but it now knows exactly which knobs must be zero by theorem or small by sourced bounds.",
            "",
        ]
    )


def main() -> None:
    ensure_dirs()
    rows_map = build_rows_map()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs(include_validation=False)
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    copy_outputs(include_validation=True)
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1850 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()

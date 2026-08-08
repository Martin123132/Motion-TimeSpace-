from __future__ import annotations

import csv
import shutil
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB = ROOT / "source-intake" / "rab-sector"
RAB_RAW = RAB / "raw"
RAB_ACCEPTED = RAB / "accepted"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1592"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1592-Y5-R2FR-transition-gradient-parent-signature-or-Qnorm-source-acquisition.md"

SOURCE_FILES = {
    "1591_doc": ROOT / "1591-Y5-R2FR-fixed-L0-cdb-memory-Qnorm-first-fill-or-cR2-bound-row.md",
    "1591_validation": OUT / "P8_Y5_BRR545_1591_VALIDATION.csv",
    "1591_transition_pack": OUT / "P8_Y5_PARENT_QLOC_1591_TRANSITION_CLOSURE_PACK.csv",
    "1591_qnorm": OUT / "P8_Y5_PARENT_QLOC_1591_QNORM_FIRST_FILL_SYNTHESIS.csv",
    "1380_kappa_zm": OUT / "P8_Y5_R10_1380_KAPPA_ZM_ORIGIN_COEFFICIENT_ROW.csv",
    "1381_zm_audit": OUT / "P8_Y5_R10_1381_ZM_SIGN_VALUE_UNIT_AUDIT.csv",
    "1384_canonical_audit": OUT / "P8_Y5_R10_1384_CANONICALIZATION_DERIVATION_AUDIT.csv",
    "1384_invariant_pivot": OUT / "P8_Y5_R10_1384_FIELD_REDEFINITION_INVARIANT_PIVOT.csv",
    "1385_gap_coupling": OUT / "P8_Y5_R10_1385_CANONICAL_GAP_COUPLING_CONTRACT.csv",
    "1385_finite_rows": OUT / "P8_Y5_R10_1385_FINITE_CHANNEL_ACQUISITION_ROWS.csv",
    "1386_package_matrix": OUT / "P8_Y5_R10_1386_PARENT_PACKAGE_CLAUSE_MATRIX.csv",
    "1386_gc_zero": OUT / "P8_Y5_R10_1386_GC_ZERO_THEOREM_ATTEMPT.csv",
    "1387_action_weights": OUT / "P8_Y5_R10_1387_ACTION_WEIGHT_EXCLUSION_AUDIT.csv",
    "1387_beta_fill": OUT / "P8_Y5_R10_1387_DELTA_W_SOURCE_BETA_FIRST_FILL.csv",
    "1540_selector": OUT / "P8_Y5_PARENT_QLOC_1540_COUPLING_SELECTOR_THEOREM_ATTEMPT.csv",
    "1541_kernel": OUT / "P8_Y5_PARENT_QLOC_1541_KERNEL_TEST.csv",
    "1584_gr_runner": OUT / "P8_Y5_PARENT_QLOC_1584_GR_REDUCTION_RUNNER.csv",
}

NEEDLES = {
    "1591_doc": ["NEXT_1592_TRANSITION_GRADIENT_PARENT_SIGNATURE_OR_QNORM_SOURCE_ACQUISITION", "gradient parent signature"],
    "1591_validation": ["VAL1591_OVERALL", "PASS"],
    "1591_transition_pack": ["TCP1591_13_verdict", "TRANSITION_CLOSURE_PACK_READY_NONCLAIM"],
    "1591_qnorm": ["QNF1591_6_Q_norm_total", "TOTAL_BOUND_FORM_READY_ALL_COMPONENT_VALUES_MISSING"],
    "1380_kappa_zm": ["KOR1380_0_identification", "SOURCE_BACKED_SYMBOLIC_COEFFICIENT_SLOT"],
    "1381_zm_audit": ["ZMS1381_7_verdict", "NO_SOURCE_BACKED_SIGN_VALUE_UNIT_ROW"],
    "1384_canonical_audit": ["CDA1384_8_verdict", "CANONICAL_GAP_COUPLING_PIVOT_SELECTED"],
    "1384_invariant_pivot": ["IPV1384_4_verdict", "FIELD_REDEFINITION_INVARIANT_PIVOT_READY_NONCLAIM"],
    "1385_gap_coupling": ["CGC1385_7_verdict", "CONTRACT_READY_ZERO_ROUTE_UNSIGNED"],
    "1385_finite_rows": ["FCA1385_6_tail_envelope", "MISSING_TAIL_ENVELOPE"],
    "1386_package_matrix": ["PCM1386_7_package_verdict", "PACKAGE_FAILS_CURRENT_CLAIM"],
    "1386_gc_zero": ["GCT1386_4_zero_verdict", "ZERO_THEOREM_NOT_CLOSED_CURRENT_CORPUS"],
    "1387_action_weights": ["AWE1387_7_verdict", "COUNTEREXAMPLE_SURVIVES_FIRST_FILL_REQUIRED"],
    "1387_beta_fill": ["DWB1387_6_first_fill_verdict", "NONCLAIM_FIRST_FILL_READY"],
    "1540_selector": ["CSEL1540_6_current_verdict", "THEOREM_NOT_CLOSED"],
    "1541_kernel": ["KTEST1541_4_kernel_verdict", "KERNEL_NOT_PROVED"],
    "1584_gr_runner": ["RUN1584_4_local_gr", "BLOCKED_NO_CLAIM"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1592_SOURCE_REGISTER.csv"
PARENT_SIGNATURE = OUT / "P8_Y5_PARENT_QLOC_1592_PARENT_SIGNATURE_AUDIT.csv"
CANONICAL_THEOREM = OUT / "P8_Y5_PARENT_QLOC_1592_CANONICAL_TRANSITION_THEOREM.csv"
SOURCE_ACQUISITION = OUT / "P8_Y5_PARENT_QLOC_1592_QNORM_CANONICAL_SOURCE_ACQUISITION.csv"
ARENA_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_1592_ARENA_PROJECTION_CONTRACT.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1592_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1592_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1592_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1592_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1592_VALIDATION.csv"

COPY_TARGETS = {
    PARENT_SIGNATURE: [
        QUARANTINE / "PARENT_SIGNATURE_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_transition_parent_signature_audit_nonclaim_1592.csv",
    ],
    CANONICAL_THEOREM: [
        QUARANTINE / "CANONICAL_TRANSITION_THEOREM_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_canonical_transition_theorem_nonclaim_1592.csv",
    ],
    SOURCE_ACQUISITION: [
        QUARANTINE / "QNORM_CANONICAL_SOURCE_ACQUISITION_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_qnorm_canonical_source_acquisition_nonclaim_1592.csv",
    ],
    ARENA_CONTRACT: [
        QUARANTINE / "ARENA_PROJECTION_CONTRACT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_arena_projection_contract_nonclaim_1592.csv",
    ],
    RUNNER: [
        QUARANTINE / "RUNNER_REFUSAL_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_runner_refusal_nonclaim_1592.csv",
    ],
    DECISION: [
        QUARANTINE / "DECISION_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_transition_gradient_or_qnorm_decision_nonclaim_1592.csv",
    ],
}


def false_flags() -> dict[str, bool]:
    return {
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def file_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    return all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for source_index, (source_key, source_path) in enumerate(SOURCE_FILES.items()):
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1592_{source_index}_{source_key}",
                "source_path": rel(source_path),
                "exists": source_path.exists(),
                "needle_found": file_contains(source_path, NEEDLES[source_key]),
                "needles": "; ".join(NEEDLES[source_key]),
                "purpose": "transition-gradient parent signature, canonical gap/coupling pivot, and Qnorm source acquisition",
                **false_flags(),
            }
        )
    return rows


def parent_signature_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "PSA1592_0_action_slot",
            "candidate scalar-memory kinetic action",
            "S_m contains -1/2 Z_m(X_B) nabla m nabla m - V_R(m;X_B) plus source/bath/boundary terms.",
            "Candidate slot exists from 826/1381, but parent adoption, field domain, source/bath and boundary class remain unsigned.",
            "CANDIDATE_ACTION_SLOT_NOT_PARENT_SIGNED",
            "parent-adopted local scalar-memory sector with variation-before-readout",
            "source-intake/mts_residuals/P8_Y5_R10_1381_ZM_SIGN_VALUE_UNIT_AUDIT.csv;source-intake/mts_residuals/P8_Y5_R10_1384_CANONICALIZATION_DERIVATION_AUDIT.csv",
        ),
        (
            "PSA1592_1_field_status",
            "eta=m-m_* as varied parent field",
            "The gradient branch needs eta or canonical phi to be a parent field varied before projection, not a post-readout metric/domain definition.",
            "m remains a candidate local field; metric-composite exclusion, quotient map and variation order are not signed.",
            "FIELD_STATUS_CANDIDATE_NOT_SIGNED",
            "Dq[v_phi] and field-by-field parent action map",
            "source-intake/mts_residuals/P8_Y5_R10_1379_GRADIENT_PARENT_SIGNATURE_AUDIT.csv;source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1541_KERNEL_TEST.csv",
        ),
        (
            "PSA1592_2_canonical_invariant_pivot",
            "phi=sqrt(Z0) eta and mu_m^2=F2/(Z0 L0^2)",
            "Separate Z_m and F2 are normalization-dependent; the invariant local range is controlled by mu_m^2 and ell_tr=1/sqrt(mu_m^2).",
            "This is a real simplification: the first physical target is the canonical gap, not arbitrary separate Z_m/F2 numbers.",
            "CANONICAL_INVARIANT_PIVOT_DERIVED_NONCLAIM",
            "source-backed mu_m^2(X_B) law and units",
            "source-intake/mts_residuals/P8_Y5_R10_1384_CANONICALIZATION_DERIVATION_AUDIT.csv;source-intake/mts_residuals/P8_Y5_R10_1384_FIELD_REDEFINITION_INVARIANT_PIVOT.csv",
        ),
        (
            "PSA1592_3_Euler_source_map",
            "canonical Euler equation",
            "The local quadratic action gives (Box - mu_m^2) phi = -J_c + R_Xgrad + R_boundary + R_readout in the chosen sign convention.",
            "The equation form is conditionally derived, but J_c, residual_Xgrad and boundary/readout terms are not parent-zero or sourced.",
            "EULER_FORM_DERIVED_SOURCE_MAP_MISSING",
            "matter/source descent or finite J_c/boundary/readout rows",
            "source-intake/mts_residuals/P8_Y5_R10_1384_CANONICALIZATION_DERIVATION_AUDIT.csv;source-intake/mts_residuals/P8_Y5_R10_1385_CANONICAL_GAP_COUPLING_CONTRACT.csv",
        ),
        (
            "PSA1592_4_coupling_zero_package",
            "g_c=0 / beta_source=beta_test=0",
            "If q-kernel, observed coframe descent, matter lift, constants, no action weights, current owner and boundary/readout silence all close, then delta_phi S_matter=0.",
            "The conditional theorem is sharp, but the package fails: q map/kernel, coframe, matter category, constants, action weights and boundary/readout remain unsigned.",
            "ZERO_COUPLING_ROUTE_UNSIGNED",
            "one parent-signed matter descent package before variation/readout",
            "source-intake/mts_residuals/P8_Y5_R10_1386_PARENT_PACKAGE_CLAUSE_MATRIX.csv;source-intake/mts_residuals/P8_Y5_R10_1386_GC_ZERO_THEOREM_ATTEMPT.csv;source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1540_COUPLING_SELECTOR_THEOREM_ATTEMPT.csv",
        ),
        (
            "PSA1592_5_action_weight_obstruction",
            "pre-variation source/action weights",
            "S_matter=sum_A w_A S_A is a live counterexample unless parent syntax/action measure proves w_A inadmissible, common, quotient-equivalent or null-projected.",
            "This is one of the hardest seams for Newton/common-matter recovery because isolated classical EOM do not kill w_A.",
            "COUNTEREXAMPLE_SURVIVES_FIRST_FILL_REQUIRED",
            "object-language/action-measure theorem or finite Delta_w/beta_w rows",
            "source-intake/mts_residuals/P8_Y5_R10_1387_ACTION_WEIGHT_EXCLUSION_AUDIT.csv;source-intake/mts_residuals/P8_Y5_R10_1387_DELTA_W_SOURCE_BETA_FIRST_FILL.csv",
        ),
        (
            "PSA1592_6_local_GR_reentry",
            "GR/Newton local branch",
            "Even with the canonical transition law, local GR still requires beta/common-matter/conservation/source-normalized Newton gates under the same parent action.",
            "1584 correctly refuses the local-GR upgrade while beta, conservation, common matter and source-normalized Newton gates remain open.",
            "LOCAL_GR_REENTRY_STILL_BLOCKED",
            "same-parent closure of canonical gap, coupling, conservation and Newton-source gates",
            "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1584_GR_REDUCTION_RUNNER.csv",
        ),
        (
            "PSA1592_7_verdict",
            "transition-gradient parent signature",
            "The branch can be written in canonical invariant form and gives useful exact conditional laws, but the parent signature is not closed.",
            "Do not adopt closure as derivation. Use mu_m^2, beta_source, beta_test, Phi_S and tail envelopes as explicit nonclaim acquisition rows.",
            "PARENT_SIGNATURE_NOT_CLOSED_CANONICAL_SOURCE_ACQUISITION_REQUIRED",
            "parent-sign coupling zero theorem or fill finite canonical rows",
            "aggregate_PSA1592_0_to_PSA1592_6",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "clause": clause,
            "required_statement": required_statement,
            "evidence_summary": evidence_summary,
            "status": status,
            "blocking_gap": blocking_gap,
            "source_paths": source_paths,
            "parent_signed": False,
            **false_flags(),
        }
        for audit_id, clause, required_statement, evidence_summary, status, blocking_gap, source_paths in rows
    ]


def canonical_theorem_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CTT1592_0_quadratic_action",
            "canonical local quadratic branch",
            "L_phi^(2)=-1/2 nabla_phi^2 -1/2 mu_m^2 phi^2 + phi J_c + R_Xgrad + R_bdy + R_readout",
            "conditional on Z0>0, locally frozen X_B, extremum m_*, and parent-adopted scalar-memory action",
            "CONDITIONAL_ACTION_CANONICALIZED",
        ),
        (
            "CTT1592_1_Euler_equation",
            "canonical field equation",
            "(Box - mu_m^2) phi = -J_c + R_Xgrad + R_bdy + R_readout",
            "J_c and residual terms must be parent-zero or finite sourced; sign convention must be locked",
            "CONDITIONAL_EULER_FORM_DERIVED",
        ),
        (
            "CTT1592_2_static_exterior_solution",
            "vacuum exterior profile",
            "For J_c=R_Xgrad=R_bdy=R_readout=0 and mu_m^2>0, normal-distance solutions contain decaying branch phi(d)=Phi_S exp(-d/ell_tr), ell_tr=1/sqrt(mu_m^2).",
            "requires boundary/source amplitude Phi_S and excludes growing branch by boundary condition/no-flux theorem",
            "CONDITIONAL_EXPONENTIAL_PROFILE_DERIVED",
        ),
        (
            "CTT1592_3_amplitude_law",
            "Delta_phi and gradient bound",
            "Delta_phi <= Phi_S exp(-d/ell_tr), and norm(nabla phi) <= Phi_S exp(-d/ell_tr)/ell_tr plus curvature/domain corrections.",
            "Phi_S, domain distance d, curvature corrections and boundary class are missing",
            "CONDITIONAL_AMPLITUDE_LAW_DERIVED",
        ),
        (
            "CTT1592_4_Qalg_bound",
            "algebraic residual bound",
            "Since nabla Gamma_eff = mu_m^2 phi nabla phi + higher orders, Q_alg <= A_ref^-1 mu_m^2 Phi_S^2 exp(-2d/ell_tr)/ell_tr plus higher-order/tail terms.",
            "A_ref, mu_m^2, Phi_S, d, ell_tr and higher-order cutoff are not source-backed",
            "CANONICAL_QALG_BOUND_DERIVED_NONCLAIM",
        ),
        (
            "CTT1592_5_memory_stress_bound",
            "canonical stress residual",
            "T_phi envelope scales like Phi_S^2 exp(-2d/ell_tr)(ell_tr^-2 + mu_m^2) plus source/boundary/readout tails; using the gradient law forbids deleting this stress.",
            "stress projection, trace reversal, A_ref and tail components remain source acquisition rows",
            "STRESS_ROUTING_GUARD_DERIVED_NONCLAIM",
        ),
        (
            "CTT1592_6_finite_coupling_law",
            "finite local exchange",
            "Observable finite scalar exchange uses beta_source*beta_test times profile/kernel factors; a single naked coupling coefficient is not enough.",
            "beta convention, source/test legs, G_N calibration and tail envelope remain missing",
            "PRODUCT_COUPLING_LAW_LOCKED_NONCLAIM",
        ),
        (
            "CTT1592_7_exact_zero_conditions",
            "zero-residual theorem conditions",
            "Need mu_m^2>0, J_c=0, Phi_S=0 or infinite suppression, R_Xgrad=R_bdy=R_readout=0, Q_cdb=0, and beta_source=beta_test=0 under the same parent action.",
            "current corpus does not close all conditions together",
            "ZERO_CONDITIONS_EXPLICIT_NOT_SATISFIED",
        ),
        (
            "CTT1592_8_verdict",
            "canonical transition theorem",
            "The canonical transition theorem is derived as a conditional branch and is a better language than the old Z_m/F2 split, but it is not a live claim.",
            "must parent-sign coupling/source/boundary package or fill finite source rows",
            "CONDITIONAL_CANONICAL_THEOREM_DERIVED_NONCLAIM",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": theorem_id,
            "object": obj,
            "derived_statement": derived_statement,
            "condition_or_gap": condition_or_gap,
            "status": status,
            "parent_signed": False,
            **false_flags(),
        }
        for theorem_id, obj, derived_statement, condition_or_gap, status in rows
    ]


def source_acquisition_rows() -> list[dict[str, Any]]:
    rows = [
        ("CSA1592_0_mu_m2", "mu_m^2(X_B)", "canonical memory mass gap controlling ell_tr=1/sqrt(mu_m^2)", "length^-2 or mass^2", "parent Hessian/kinetic ratio or direct canonical gap theorem", "range; transition length; R10 lambda; Q_alg profile", "MISSING_SOURCE_BACKED_CANONICAL_GAP"),
        ("CSA1592_1_beta_source", "beta_source", "source leg beta_s=partial_phi ln m_source_eff or equivalent source-current variation", "declared canonical beta units", "source worldtube and matter/source descent map", "R10 alpha; Newton source normalization; source-charge WEP", "MISSING_SOURCE_BETA"),
        ("CSA1592_2_beta_test", "beta_test", "test leg beta_t=partial_phi ln m_test_eff or equivalent test-body variation", "same beta convention as beta_source", "test-body matter action plus material/composition map", "R10 alpha; WEP; clock/orbital response", "MISSING_TEST_BETA"),
        ("CSA1592_3_beta_product", "beta_source*beta_test", "finite exchange amplitude product; universal branch gives beta^2 not beta", "dimensionless after convention lock", "beta convention, source/test rows, profile factors and measured-G guard", "all alpha(lambda) and local finite-force scoring", "PRODUCT_LAW_READY_VALUES_MISSING"),
        ("CSA1592_4_Phi_S", "Phi_S", "canonical boundary/source amplitude for exterior profile", "canonical field units", "boundary/source theorem or finite amplitude bound", "Delta_phi, gradient envelope, Q_alg, stress envelope", "MISSING_CANONICAL_AMPLITUDE"),
        ("CSA1592_5_epsilon_Z", "epsilon_Z", "norm(nabla ln Z_m)/mu_m correction to locally frozen canonicalization", "dimensionless", "X_B local variation theorem or bound", "safe local plateau beyond frozen-X_B approximation", "MISSING_XB_GRADIENT_BOUND"),
        ("CSA1592_6_epsilon_tail", "epsilon_tail", "hidden frame, readout, boundary, projector, source-normalization and non-EH tails with no-cancellation policy", "arena-dependent residual units", "tail component bounds or theorem-zero clauses", "R10/PPN/WEP/clock/orbital pass", "MISSING_TAIL_ENVELOPE"),
        ("CSA1592_7_A_ref", "A_ref", "normalization converting residual envelopes into Q_i", "declared local norm units", "parent local residual norm convention", "Q_alg/Q_cdb/Q_mem/Q_trans scoring", "MISSING_NORMALIZATION_CONVENTION"),
        ("CSA1592_8_Ndiv_NG_ND", "N_div;N_G;N_D", "operator/projection norms converting local residuals to observable gamma/arena bounds", "dimensionless or declared operator norm units", "projection/operator source rows", "PPN gamma and local arena contracts", "MISSING_OPERATOR_PROJECTION_NORMS"),
        ("CSA1592_9_Umin", "U_min", "minimum Newtonian potential scale in the PPN gamma bound", "SI potential units or declared c convention", "arena-specific PPN potential convention", "B_gamma <= c^2/(2U_min) N_G N_D Q_norm", "MISSING_ARENA_POTENTIAL_CONVENTION"),
        ("CSA1592_10_Delta_w_beta_w", "Delta_w_A; beta_w_source; beta_w_test", "action-weight counterexample rows for source normalization and finite exchange", "dimensionless or canonical beta units", "object-language/action-measure theorem or finite source rows", "Newton/common matter/WEP/R10", "FIRST_FILL_READY_VALUE_MISSING"),
        ("CSA1592_11_boundary_shell", "boundary/shell gate", "exact projector zero or explicit finite shell contribution", "logic gate plus residual units", "boundary/no-flux theorem, shell bound, or projector identity", "Q_bdy, Q_trans, Q_proj", "MISSING_SHELL_CLOSURE"),
        ("CSA1592_12_verdict", "canonical source pack", "all scoreable local rows now route through mu_m^2, beta_source, beta_test, Phi_S and epsilon_tail rather than raw closure variables", "not claim-grade", "source-backed values or exact zero theorems for every row", "local GR/Newton/PPN/R10/clock/orbital reopening", "CANONICAL_SOURCE_ACQUISITION_READY_NONCLAIM"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "row_id": row_id,
            "quantity": quantity,
            "definition": definition,
            "required_units": units,
            "required_source": required_source,
            "blocks_if_missing": blocks,
            "current_status": status,
            **false_flags(),
        }
        for row_id, quantity, definition, units, required_source, blocks, status in rows
    ]


def arena_contract_rows() -> list[dict[str, Any]]:
    rows = [
        ("APR1592_0_R10", "short-range R10", "lambda=1/sqrt(mu_m^2); alpha(lambda)=K_R10(lambda) beta_source beta_test + epsilon_tail(lambda)", "mu_m2;beta_source;beta_test;K_R10;tail;real bound curve", "BLOCKED_INPUTS_MISSING"),
        ("APR1592_1_PPN_gamma", "Cassini/PPN gamma", "B_gamma <= c^2/(2 U_min) N_G N_D Q_norm, with Q_norm using canonical Q_alg and retained CDB/memory/tails", "U_min;N_G;N_D;Q_i;A_ref;projection norm", "BLOCKED_INPUTS_MISSING"),
        ("APR1592_2_Newton_source", "Newton/source normalization", "common constant source factor may be absorbed into measured G only if Delta_w_A=0 and all derivative/range/frame dependence is silent", "w_common;Delta_w_A;derivative silence;GM calibration guard", "BLOCKED_ACTION_WEIGHT_COUNTEREXAMPLE"),
        ("APR1592_3_clock_orbital", "clock/orbital local residuals", "clock/orbital kernels require beta_test, source profile, tail envelope, and observable-specific projection matrix", "beta rows;source worldtube;clock/orbital kernels;tail envelope", "BLOCKED_INPUTS_MISSING"),
        ("APR1592_4_WEP_common_matter", "WEP/common matter", "zero route needs matter descent and no action weights; finite route needs material beta/Delta_w rows", "ordinary matter functor;constants;action weights;material map", "BLOCKED_PARENT_PACKAGE_UNSIGNED"),
        ("APR1592_5_cosmology_interface", "cosmology/local separation", "local canonical mu_m^2/g_c rows must not be imported into cosmology memory amplitudes without a shared parent projection law", "branch map;projection convention;no double counting", "GUARD_READY_NO_IMPORT"),
        ("APR1592_6_verdict", "arena projection", "all local arenas remain blocked but now have cleaner canonical input requirements", "all source acquisition rows plus arena kernels", "ARENA_CONTRACT_READY_NONCLAIM"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "arena_id": arena_id,
            "arena": arena,
            "projection_formula_or_rule": formula,
            "required_inputs": required_inputs,
            "status": status,
            **false_flags(),
        }
        for arena_id, arena, formula, required_inputs, status in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN1592_0_parent_signature", "accept parent-gradient derivation only if action slot, field status, Euler/source map, coupling package and boundary/readout all parent-sign", "PSA1592 verdict is parent signature not closed", "REJECT_PARENT_SIGNATURE_CLAIM", "transition branch remains conditional"),
        ("RUN1592_1_canonical_theorem", "accept canonical theorem as math contract but not empirical claim", "CTT1592 gives conditional laws with missing source/boundary/coupling clauses", "ACCEPT_CONDITIONAL_THEOREM_ONLY", "use canonical variables for future rows"),
        ("RUN1592_2_source_pack", "accept numeric runner only if mu_m2, beta_source, beta_test, Phi_S, epsilon_Z/tail, A_ref and arena maps are sourced", "source acquisition rows are missing values or theorem-zero certificates", "REJECT_NUMERIC_SCORING", "no PPN/R10/clock/orbital run"),
        ("RUN1592_3_coupling_zero", "accept g_c=0 only if q-kernel, observed coframe, matter lift, constants, action weights, current owner and boundary/readout close together", "1386/1540/1541 leave package unsigned and action-weight counterexample alive", "REJECT_ZERO_COUPLING_CLAIM", "next target should attack coupling package"),
        ("RUN1592_4_local_GR", "accept local GR/Newton only when beta/common matter/conservation/source-normalized Newton gates close under same parent action", "1584 refuses local GR upgrade", "REJECT_LOCAL_GR_REENTRY", "do not overclaim from transition success"),
        ("RUN1592_5_branch_lock", "accept future finite rows only if same_parent_branch_id matches and no MISSING/toy/proxy values remain", f"all 1592 rows use {BRANCH_ID}", "BRANCH_LOCK_OK_INPUTS_PENDING", "hygiene passes; physics pending"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "acceptance_rule": acceptance_rule,
            "input_state": input_state,
            "runner_result": runner_result,
            "effect": effect,
            **false_flags(),
        }
        for runner_id, acceptance_rule, input_state, runner_result, effect in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1592_0_parent_gradient", "parent-signed transition-gradient mechanism", "BLOCKED_NO_CLAIM", "candidate canonical action exists but parent package is unsigned"),
        ("GATE1592_1_canonical_range", "mu_m^2 / ell_tr numeric range", "BLOCKED_NO_CLAIM", "mu_m^2 law/value/units missing"),
        ("GATE1592_2_coupling_zero", "g_c=0 or beta_source=beta_test=0", "BLOCKED_NO_CLAIM", "matter descent/action-weight/source-current package not closed"),
        ("GATE1592_3_finite_beta", "finite beta_source beta_test score", "BLOCKED_NO_CLAIM", "source/test beta rows and profile kernels missing"),
        ("GATE1592_4_Qnorm", "Q_norm bound pass", "BLOCKED_NO_CLAIM", "canonical Q_i source rows remain missing"),
        ("GATE1592_5_R10_PPN_clock_orbital", "local empirical score", "BLOCKED_NO_CLAIM", "arena projections require missing canonical source pack"),
        ("GATE1592_6_GR_Newton", "local GR/Newton reduction", "BLOCKED_NO_CLAIM", "beta, common matter, conservation and Newton source gates remain open"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            **false_flags(),
        }
        for gate_id, claim, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC1592_0_canonical_pivot",
            "USE_CANONICAL_GAP_AND_COUPLING_LANGUAGE",
            "the invariant pair mu_m^2 and beta_source/beta_test removes arbitrary Z_m/F2 normalization ambiguity",
            "future local rows should ask for mu_m^2, beta legs, Phi_S and tails first",
        ),
        (
            "DEC1592_1_derivation_status",
            "CONDITIONAL_TRANSITION_THEOREM_DERIVED_NOT_PARENT_SIGNED",
            "the amplitude/suppression law follows cleanly once the canonical action is assumed, but the parent action package is still unsigned",
            "keep theorem as internal math contract; no live local-GR claim",
        ),
        (
            "DEC1592_2_main_bottleneck",
            "COUPLING_PACKAGE_IS_THE_NEXT_HARD_GATE",
            "range suppression alone is not enough; local tests turn on beta_source beta_test, action weights and tail envelopes",
            "attack matter descent/action-weight/source-current package next",
        ),
        (
            "DEC1592_3_next",
            "NEXT_1593_CANONICAL_COUPLING_ZERO_THEOREM_OR_FINITE_BETA_SOURCE_ROWS",
            "the least-scrutiny route is to prove g_c=0 from parent matter descent; if not, fill finite beta rows honestly",
            "derive q-kernel/coframe/matter/action-weight/current/boundary package or build beta_source beta_test acquisition rows",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            **false_flags(),
        }
        for decision_id, decision, reason, next_action in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1593-Y5-R2FR-canonical-coupling-zero-theorem-or-finite-beta-source-rows.md",
            "script": "scripts/Y5_R2FR_canonical_coupling_zero_theorem_or_finite_beta_source_rows.py",
            "objective": "try to prove the canonical mode has zero ordinary-matter coupling from q-kernel, observed coframe descent, matter lift, constant superselection, action-weight exclusion, current owner and boundary/readout silence; if not, create finite beta_source/beta_test/source-normalization acquisition rows",
            "success_condition": "parent-signed g_c=0 theorem under one matter package, or strict nonclaim beta_source beta_test and Delta_w rows ready for local arena runners",
            "do_not": "do not claim local GR, do not use range suppression as coupling suppression, do not score alpha/gamma from missing beta rows, do not edit formalization-workbench or GitHub",
            **false_flags(),
        }
    ]


def copy_outputs() -> None:
    for source_path, target_paths in COPY_TARGETS.items():
        for target_path in target_paths:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_path, target_path)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def generated_flags_false(generated_csvs: list[Path]) -> bool:
    flag_columns = {"score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed", "parent_signed"}
    for csv_path in generated_csvs:
        for row in read_csv(csv_path):
            for flag_column in flag_columns.intersection(row):
                if row[flag_column] != "False":
                    return False
    return True


def formalization_scope_clean(generated_csvs: list[Path]) -> bool:
    if any(FORMALIZATION in csv_path.parents for csv_path in generated_csvs):
        return False
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT.parent), "status", "--short", "--", "formalization-workbench"],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return True
    if result.returncode != 0:
        return True
    return len([line for line in result.stdout.splitlines() if line.strip()]) == 0


def has_1592_rows(folder: Path) -> bool:
    if not folder.exists():
        return False
    return any("1592" in csv_path.name for csv_path in folder.glob("*.csv"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    parent = read_csv(PARENT_SIGNATURE)
    theorem = read_csv(CANONICAL_THEOREM)
    acquisition = read_csv(SOURCE_ACQUISITION)
    arena = read_csv(ARENA_CONTRACT)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    required_quantities = {"mu_m^2(X_B)", "beta_source", "beta_test", "beta_source*beta_test", "Phi_S", "epsilon_Z", "epsilon_tail"}
    checks = [
        ("VAL1592_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1592 source paths exist"),
        ("VAL1592_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all 1592 source needles found"),
        (
            "VAL1592_2_parent_signature_not_closed",
            any(row["audit_id"] == "PSA1592_7_verdict" and row["status"] == "PARENT_SIGNATURE_NOT_CLOSED_CANONICAL_SOURCE_ACQUISITION_REQUIRED" for row in parent),
            "transition-gradient parent signature remains unsigned",
        ),
        (
            "VAL1592_3_canonical_theorem_derived_nonclaim",
            any(row["theorem_id"] == "CTT1592_8_verdict" and row["status"] == "CONDITIONAL_CANONICAL_THEOREM_DERIVED_NONCLAIM" for row in theorem),
            "canonical transition theorem is captured as conditional math, not claim",
        ),
        (
            "VAL1592_4_source_acquisition_quantities_present",
            required_quantities.issubset({row["quantity"] for row in acquisition}) and all(row["valid_for_claim"] == "False" for row in acquisition),
            "canonical gap/coupling/source acquisition rows are present and nonclaim",
        ),
        (
            "VAL1592_5_arena_contract_blocks_scores",
            any(row["arena_id"] == "APR1592_6_verdict" and row["status"] == "ARENA_CONTRACT_READY_NONCLAIM" for row in arena)
            and all(row["claim_allowed"] == "False" for row in arena),
            "arena projections are explicit but blocked pending inputs",
        ),
        (
            "VAL1592_6_runner_rejects_current_claims",
            any(row["runner_result"] == "REJECT_PARENT_SIGNATURE_CLAIM" for row in runner)
            and any(row["runner_result"] == "REJECT_ZERO_COUPLING_CLAIM" for row in runner)
            and any(row["runner_result"] == "REJECT_LOCAL_GR_REENTRY" for row in runner),
            "runner refuses parent-signature, zero-coupling and local-GR claims",
        ),
        (
            "VAL1592_7_claim_gates_closed",
            all(row["status"] == "BLOCKED_NO_CLAIM" and row["claim_allowed"] == "False" for row in gates),
            "all 1592 claim gates remain closed",
        ),
        (
            "VAL1592_8_decision_next",
            any(row["decision"] == "NEXT_1593_CANONICAL_COUPLING_ZERO_THEOREM_OR_FINITE_BETA_SOURCE_ROWS" for row in decisions),
            "decision selects canonical coupling zero theorem or finite beta source rows",
        ),
        ("VAL1592_9_csv_parse", all(len(read_csv(csv_path)) > 0 for csv_path in generated_csvs), "all generated 1592 CSVs parse cleanly"),
        ("VAL1592_10_claim_flags_false", generated_flags_false(generated_csvs), "all generated claim/prediction/parent-signed flags remain false"),
        ("VAL1592_11_no_raw_accepted", not has_1592_rows(RAB_RAW) and not has_1592_rows(RAB_ACCEPTED), "no 1592 rows written to raw/accepted finite directories"),
        ("VAL1592_12_branch_copies", all(target_path.exists() for target_paths in COPY_TARGETS.values() for target_path in target_paths), "branch/quarantine nonclaim copies written"),
        ("VAL1592_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1592_14_formalization_untouched", formalization_scope_clean(generated_csvs), "all generated 1592 paths are outside formalization-workbench; git status is clean when available"),
    ]
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1592_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1592 transition-gradient parent signature or Qnorm source acquisition validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = ["| " + " | ".join(str(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def write_doc(
    sources: list[dict[str, Any]],
    parent: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    acquisition: list[dict[str, Any]],
    arena: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1592 - R2/fR Transition-Gradient Parent Signature Or Qnorm Source Acquisition",
                "## Verdict\n"
                "- 1592 gets a real simplification: the transition-gradient branch should be written in canonical variables, with `phi=sqrt(Z0) eta`, `mu_m^2=F2/(Z0 L0^2)`, and `ell_tr=1/sqrt(mu_m^2)`.\n"
                "- This removes a lot of fake freedom in separate `Z_m`/`F2` choices. The physical local first-fill pair is now `mu_m^2(X_B)` plus the canonical coupling legs `beta_source`, `beta_test`.\n"
                "- The conditional suppression law is derived: if the canonical action is parent-adopted and source/boundary/tail terms vanish, `phi(d)=Phi_S exp(-d/ell_tr)`, `Delta_phi<=Phi_S exp(-d/ell_tr)`, and `Q_alg` is quadratically suppressed.\n"
                "- But the parent signature is still **not closed**: coupling/source descent, action-weight exclusion, boundary/readout silence, and common-matter/Newton gates remain live.\n"
                "- No local-GR, Newton, PPN, R10, clock, orbital, WEP, scalaron, coupling-zero or public claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## Parent Signature Audit",
                md_table(parent, ["audit_id", "clause", "required_statement", "evidence_summary", "status", "blocking_gap"]),
                "## Canonical Transition Theorem",
                md_table(theorem, ["theorem_id", "object", "derived_statement", "condition_or_gap", "status"]),
                "## Canonical Source Acquisition",
                md_table(acquisition, ["row_id", "quantity", "definition", "required_units", "required_source", "blocks_if_missing", "current_status"]),
                "## Arena Projection Contract",
                md_table(arena, ["arena_id", "arena", "projection_formula_or_rule", "required_inputs", "status"]),
                "## Runner Refusal",
                md_table(runner, ["runner_id", "acceptance_rule", "input_state", "runner_result", "effect"]),
                "## Claim Gates",
                md_table(gates, ["gate_id", "claim", "status", "reason"]),
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "reason", "next_action"]),
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "success_condition", "do_not"]),
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    parent = parent_signature_rows()
    theorem = canonical_theorem_rows()
    acquisition = source_acquisition_rows()
    arena = arena_contract_rows()
    runner = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        PARENT_SIGNATURE,
        CANONICAL_THEOREM,
        SOURCE_ACQUISITION,
        ARENA_CONTRACT,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(PARENT_SIGNATURE, parent)
    write_csv(CANONICAL_THEOREM, theorem)
    write_csv(SOURCE_ACQUISITION, acquisition)
    write_csv(ARENA_CONTRACT, arena)
    write_csv(RUNNER, runner)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, parent, theorem, acquisition, arena, runner, gates, decisions, validation, next_rows)


if __name__ == "__main__":
    main()

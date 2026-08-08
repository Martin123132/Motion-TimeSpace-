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
QUARANTINE = MICROSCOPE / "quarantine" / "1593"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1593-Y5-R2FR-canonical-coupling-zero-theorem-or-finite-beta-source-rows.md"

SOURCE_FILES = {
    "1592_doc": ROOT / "1592-Y5-R2FR-transition-gradient-parent-signature-or-Qnorm-source-acquisition.md",
    "1592_validation": OUT / "P8_Y5_BRR545_1592_VALIDATION.csv",
    "1592_parent_signature": OUT / "P8_Y5_PARENT_QLOC_1592_PARENT_SIGNATURE_AUDIT.csv",
    "1592_canonical_theorem": OUT / "P8_Y5_PARENT_QLOC_1592_CANONICAL_TRANSITION_THEOREM.csv",
    "1385_gap_coupling": OUT / "P8_Y5_R10_1385_CANONICAL_GAP_COUPLING_CONTRACT.csv",
    "1385_finite_rows": OUT / "P8_Y5_R10_1385_FINITE_CHANNEL_ACQUISITION_ROWS.csv",
    "1386_package_matrix": OUT / "P8_Y5_R10_1386_PARENT_PACKAGE_CLAUSE_MATRIX.csv",
    "1386_gc_zero": OUT / "P8_Y5_R10_1386_GC_ZERO_THEOREM_ATTEMPT.csv",
    "1387_action_weight_audit": OUT / "P8_Y5_R10_1387_ACTION_WEIGHT_EXCLUSION_AUDIT.csv",
    "1387_beta_fill": OUT / "P8_Y5_R10_1387_DELTA_W_SOURCE_BETA_FIRST_FILL.csv",
    "1045_functor_audit": OUT / "P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
    "1045_geom_zero": OUT / "P8_Y5_R10_1045_QBAR_GEOM_ZERO_ATTEMPT.csv",
    "1087_matter_descent": OUT / "P8_Y5_R10_1087_PARENT_MATTER_DESCENT_ATTEMPT.csv",
    "1229_source_theorem": OUT / "P8_Y5_R10_1229_LOCAL_GR_SOURCE_COUPLING_THEOREM_CONTRACT.csv",
    "1229_counterexamples": OUT / "P8_Y5_R10_1229_SOURCE_COUPLING_COUNTEREXAMPLE_LEDGER.csv",
    "1229_clause_audit": OUT / "P8_Y5_R10_1229_UNIVERSAL_SOURCE_COUPLING_CLAUSE_AUDIT.csv",
    "1540_selector": OUT / "P8_Y5_PARENT_QLOC_1540_COUPLING_SELECTOR_THEOREM_ATTEMPT.csv",
    "1541_kernel": OUT / "P8_Y5_PARENT_QLOC_1541_KERNEL_TEST.csv",
    "1584_gr_runner": OUT / "P8_Y5_PARENT_QLOC_1584_GR_REDUCTION_RUNNER.csv",
}

NEEDLES = {
    "1592_doc": ["NEXT_1593_CANONICAL_COUPLING_ZERO_THEOREM_OR_FINITE_BETA_SOURCE_ROWS", "beta_source beta_test"],
    "1592_validation": ["VAL1592_OVERALL", "PASS"],
    "1592_parent_signature": ["PSA1592_7_verdict", "PARENT_SIGNATURE_NOT_CLOSED_CANONICAL_SOURCE_ACQUISITION_REQUIRED"],
    "1592_canonical_theorem": ["CTT1592_6_finite_coupling_law", "PRODUCT_COUPLING_LAW_LOCKED_NONCLAIM"],
    "1385_gap_coupling": ["CGC1385_7_verdict", "CONTRACT_READY_ZERO_ROUTE_UNSIGNED"],
    "1385_finite_rows": ["FCA1385_3_beta_product", "PRODUCT_LAW_READY_VALUES_MISSING"],
    "1386_package_matrix": ["PCM1386_7_package_verdict", "PACKAGE_FAILS_CURRENT_CLAIM"],
    "1386_gc_zero": ["GCT1386_4_zero_verdict", "ZERO_THEOREM_NOT_CLOSED_CURRENT_CORPUS"],
    "1387_action_weight_audit": ["AWE1387_7_verdict", "COUNTEREXAMPLE_SURVIVES_FIRST_FILL_REQUIRED"],
    "1387_beta_fill": ["DWB1387_6_first_fill_verdict", "NONCLAIM_FIRST_FILL_READY"],
    "1045_functor_audit": ["MFS1045_6_verdict", "FAIL_CURRENT_CLAIM_PARENT_MATTER_FUNCTOR_NOT_SIGNED"],
    "1045_geom_zero": ["QG1045_4_current_verdict", "FAIL_CURRENT_CLAIM_QBAR_GEOM_ZERO_NOT_SIGNED"],
    "1087_matter_descent": ["PMD1087_6_verdict", "PARENT_MATTER_DESCENT_ZERO_NOT_SIGNED"],
    "1229_source_theorem": ["THM1229_2_countermodel", "OBSTRUCTION_ACTIVE"],
    "1229_counterexamples": ["CEX1229_0_action_multiplier", "ACTIVE"],
    "1229_clause_audit": ["CLC1229_8_verdict", "NOT_CLOSED"],
    "1540_selector": ["CSEL1540_6_current_verdict", "THEOREM_NOT_CLOSED"],
    "1541_kernel": ["KTEST1541_4_kernel_verdict", "KERNEL_NOT_PROVED"],
    "1584_gr_runner": ["RUN1584_4_local_gr", "BLOCKED_NO_CLAIM"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1593_SOURCE_REGISTER.csv"
ZERO_THEOREM = OUT / "P8_Y5_PARENT_QLOC_1593_CANONICAL_COUPLING_ZERO_THEOREM_ATTEMPT.csv"
PACKAGE_GATE = OUT / "P8_Y5_PARENT_QLOC_1593_MATTER_PACKAGE_CLAUSE_GATE.csv"
FINITE_BETA_ROWS = OUT / "P8_Y5_PARENT_QLOC_1593_FINITE_BETA_SOURCE_ROWS.csv"
SOURCE_RESIDUAL = OUT / "P8_Y5_PARENT_QLOC_1593_ACTION_WEIGHT_SOURCE_RESIDUAL.csv"
LOCAL_GR_IMPACT = OUT / "P8_Y5_PARENT_QLOC_1593_LOCAL_GR_IMPACT_MAP.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1593_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1593_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1593_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1593_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1593_VALIDATION.csv"

COPY_TARGETS = {
    ZERO_THEOREM: [
        QUARANTINE / "CANONICAL_COUPLING_ZERO_THEOREM_ATTEMPT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_canonical_coupling_zero_theorem_attempt_nonclaim_1593.csv",
    ],
    PACKAGE_GATE: [
        QUARANTINE / "MATTER_PACKAGE_CLAUSE_GATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_matter_package_clause_gate_nonclaim_1593.csv",
    ],
    FINITE_BETA_ROWS: [
        QUARANTINE / "FINITE_BETA_SOURCE_ROWS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_finite_beta_source_rows_nonclaim_1593.csv",
    ],
    SOURCE_RESIDUAL: [
        QUARANTINE / "ACTION_WEIGHT_SOURCE_RESIDUAL_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_action_weight_source_residual_nonclaim_1593.csv",
    ],
    LOCAL_GR_IMPACT: [
        QUARANTINE / "LOCAL_GR_IMPACT_MAP_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_local_gr_impact_map_nonclaim_1593.csv",
    ],
    RUNNER: [
        QUARANTINE / "RUNNER_REFUSAL_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_runner_refusal_nonclaim_1593.csv",
    ],
    DECISION: [
        QUARANTINE / "DECISION_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_canonical_coupling_decision_nonclaim_1593.csv",
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
                "source_id": f"SRC1593_{source_index}_{source_key}",
                "source_path": rel(source_path),
                "exists": source_path.exists(),
                "needle_found": file_contains(source_path, NEEDLES[source_key]),
                "needles": "; ".join(NEEDLES[source_key]),
                "purpose": "canonical coupling zero theorem or finite beta/source rows",
                **false_flags(),
            }
        )
    return rows


def zero_theorem_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "ZTH1593_0_chain_rule",
            "canonical matter variation",
            "delta_vphi S_matter = half integral sqrt_minus_g T_A^munu Lie_vphi gobs_munu plus source/current, constant, matter-lift, boundary and readout terms.",
            "If every term is zero before readout, then J_c=0 and beta_source=beta_test=0 for ordinary matter.",
            "STANDARD_CHAIN_RULE_CONDITIONAL",
            "all zero clauses below must close as one parent package",
        ),
        (
            "ZTH1593_1_q_kernel",
            "quotient-vertical canonical generator",
            "Dq_loc[v_phi]=0.",
            "Would make the canonical mode invisible to quotient-owned observed structures.",
            "UNSIGNED_KERNEL",
            "q_loc and v_phi are not jointly parent-signed; 1541 kernel test fails",
        ),
        (
            "ZTH1593_2_observed_coframe",
            "observed coframe and connection descent",
            "e_obs=Obs_e(q(Phi)), g_obs=e_obs^2, and omega_obs is coframe-owned or separately descended.",
            "Dq[v_phi]=0 would imply Lie_vphi g_obs=0 if no shadow frame or independent connection enters.",
            "SUFFICIENT_SIGNATURE_NOT_PARENT_SIGNED",
            "observed coframe functor/no-shadow-frame route remains unsigned",
        ),
        (
            "ZTH1593_3_matter_lift",
            "ordinary matter lift",
            "delta_vphi Psi_A is fixed, gauge, local Lorentz, diffeomorphism, or boundary-only.",
            "Matter Euler terms cannot create physical canonical charge if the lift is parent-owned.",
            "VERTICAL_LIFT_NOT_PARENT_SIGNED",
            "ordinary matter functor and vertical lift are not constructed for all species",
        ),
        (
            "ZTH1593_4_constants",
            "constant and representation blindness",
            "Lie_vphi theta_A=0 for ordinary masses, charges, alpha_EM, clocks and material labels.",
            "Prevents constants and standards from sourcing canonical beta rows.",
            "CONSTANT_SUPERSELECTION_UNSIGNED",
            "constant-sector theorem missing or must be finite residual rows",
        ),
        (
            "ZTH1593_5_no_action_weights",
            "no pre-variation source/action weights",
            "S_matter has no independent w_A S_A factors except a common quotient-equivalent calibration factor.",
            "Kills the live source-normalization counterexample needed for clean Newton/GR source side.",
            "ACTIVE_COUNTEREXAMPLE",
            "S_matter=sum_A w_A S_A remains legal in current corpus",
        ),
        (
            "ZTH1593_6_current_owner",
            "single Hilbert/source current owner",
            "delta S_matter over delta e_obs gives one common T_eff and descends with Noether/Bianchi closure.",
            "Needed so beta/source silence is compatible with conservation and local GR.",
            "CURRENT_OWNER_NOT_DERIVED",
            "source current owner and Bianchi descent remain contracts, not theorems",
        ),
        (
            "ZTH1593_7_boundary_readout",
            "boundary, projector and readout silence",
            "boundary terms, local projections and detector kernels do not reintroduce representative/species coefficients.",
            "Needed because a bulk zero theorem can be spoiled by local arena projection.",
            "BOUNDARY_READOUT_UNSIGNED",
            "boundary, shell, projector and readout tails remain finite rows",
        ),
        (
            "ZTH1593_8_verdict",
            "canonical coupling zero theorem",
            "All clauses ZTH1593_1 through ZTH1593_7 must close under one parent action before g_c=0 or beta_source=beta_test=0 is claim-grade.",
            "The theorem is exact as a conditional chain-rule result, but current parent evidence does not sign the package.",
            "ZERO_THEOREM_NOT_CLOSED_FINITE_BETA_ROWS_REQUIRED",
            "fill beta_source, beta_test, Delta_w, shadow-frame and tail rows or prove the package",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": theorem_id,
            "clause": clause,
            "required_statement": required_statement,
            "would_close": would_close,
            "status": status,
            "blocking_gap": blocking_gap,
            "theorem_closed": False,
            **false_flags(),
        }
        for theorem_id, clause, required_statement, would_close, status, blocking_gap in rows
    ]


def package_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("PKG1593_0_q_kernel", "Dq_loc[v_phi]=0", "PCM1386_0 and KTEST1541_0", "UNSIGNED_OR_FAIL_CURRENT_CERTIFICATE", "finite beta_geom/qbar_geom row retained"),
        ("PKG1593_1_observed_coframe", "e_obs=Obs_e(q) and no shadow frame", "MFS1045_1/MFS1045_4 and QG1045_3", "SHADOW_COUNTERMODEL_RETAINED", "finite beta_geom, b_A, d_A rows retained"),
        ("PKG1593_2_matter_functor", "Psi_A lives in parent-owned ordinary matter bundle", "MFS1045_2/MFS1045_3 and PMD1087_2", "MATTER_CATEGORY_NOT_PARENT_CONSTRUCTED", "finite matter-lift/source rows retained"),
        ("PKG1593_3_constants", "ordinary constants are phi-blind", "MFS1045_5 and PMD1087_3", "CONSTANT_SUPERSELECTION_UNSIGNED", "finite clock/alpha/material coefficient rows retained"),
        ("PKG1593_4_action_weights", "no independent w_A source/action multiplier", "AWE1387 and CEX1229", "ACTIVE_COUNTEREXAMPLE", "Delta_w and beta_w rows mandatory"),
        ("PKG1593_5_current_owner", "single Hilbert current with Noether/Bianchi descent", "CLC1229_6 and THM1229_3", "CONTRACT_WRITTEN_NOT_PROVED", "q_source residual vector retained"),
        ("PKG1593_6_boundary_readout", "boundary/projection/readout tails zero or bounded", "CLC1229_5 and PMD1087_5", "UNSIGNED_BOUNDARY_LOCAL_PROJECTION", "epsilon_tail rows mandatory"),
        ("PKG1593_7_measured_G_guard", "only common constant w_star may be absorbed into measured G_N", "CLC1229_7 and DWB1387_5", "GUARD_ACTIVE_INPUTS_MISSING", "no composition/range/frame absorption shortcut"),
        ("PKG1593_8_verdict", "whole matter package closes together", "PCM1386_7/GCT1386_4/CLC1229_8", "PACKAGE_FAILS_CURRENT_CLAIM", "zero-coupling claim blocked"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "required_clause": required_clause,
            "source_basis": source_basis,
            "current_status": status,
            "fallback": fallback,
            "clause_signed": False,
            **false_flags(),
        }
        for gate_id, required_clause, source_basis, status, fallback in rows
    ]


def finite_beta_rows() -> list[dict[str, Any]]:
    rows = [
        ("FBR1593_0_beta_source", "beta_source", "canonical source leg, beta_S = partial_phi ln m_source_eff or source-current variation", "declared canonical beta units", "source worldtube, matter descent map, current owner", "R10;Newton source;WEP source charge", "MISSING_SOURCE_BETA"),
        ("FBR1593_1_beta_test", "beta_test", "canonical test leg, beta_T = partial_phi ln m_test_eff or test-body variation", "same beta convention as beta_source", "test body matter action, material composition map, constants split", "R10;WEP;clock;orbital", "MISSING_TEST_BETA"),
        ("FBR1593_2_beta_product", "beta_source*beta_test", "finite exchange amplitude product; universal coupling gives beta squared, not a linear beta shortcut", "dimensionless after convention lock", "source/test beta rows, profile kernel, measured-G guard", "R10 alpha(lambda);local fifth force", "PRODUCT_FORMULA_READY_VALUES_MISSING"),
        ("FBR1593_3_beta_geom", "beta_geom", "visible geometry/shadow-frame coupling leg from Lie_vphi ghat_A", "canonical beta units", "q-kernel, observed coframe descent, no A(phi)/B(phi) shadow frame or finite b_A,d_A", "PPN;R10;WEP;clock", "MISSING_GEOMETRY_OR_SHADOW_FRAME_ROW"),
        ("FBR1593_4_beta_const", "beta_const", "mass, charge, alpha_EM, clock or material constant variation leg", "canonical beta units", "constant superselection theorem or finite material coefficient rows", "clock;WEP;alpha;particle", "MISSING_CONSTANT_SUPERSELECTION_OR_ROW"),
        ("FBR1593_5_beta_weight_source", "beta_w_source", "phi-dependence of source action weight w_S(phi)", "canonical beta units", "source action-weight function or exclusion theorem", "R10 source leg;Newton source;WEP", "MISSING_SOURCE_BETA_WEIGHT_FUNCTION"),
        ("FBR1593_6_beta_weight_test", "beta_w_test", "phi-dependence of test-body action weight w_T(phi)", "canonical beta units", "test material weight function or exclusion theorem", "R10 test leg;WEP;clock", "MISSING_TEST_BETA_WEIGHT_FUNCTION"),
        ("FBR1593_7_Delta_w_A", "Delta_w_A", "relative pre-variation source multiplier, Delta_w_A=w_A/w_star minus one", "dimensionless", "object-language/action-measure theorem or finite source/material bound", "Newton source universality;common matter;WEP", "FIRST_FILL_ROW_READY_VALUE_MISSING"),
        ("FBR1593_8_K_profile", "K_arena(lambda)", "arena profile/readout kernel multiplying beta_source beta_test", "arena-specific kernel units", "mu_m2, source/test geometry, worldtube/readout kernel, no double-counting convention", "R10;PPN;clock;orbital", "MISSING_PROFILE_KERNEL"),
        ("FBR1593_9_epsilon_tail", "epsilon_tail", "boundary, readout, projector, non-EH, CDB and source-normalization tail envelope with no cancellation", "arena-dependent residual units", "tail component bounds or exact zero clauses", "all local arenas", "MISSING_TAIL_ENVELOPE"),
        ("FBR1593_10_beta_acceptance", "finite beta row acceptance rule", "a row can score only with source path, units, extraction method, beta convention, branch id, arena map and no MISSING/toy/proxy markers", "logic gate", "all previous fields", "all local empirical runners", "ACCEPTANCE_CONTRACT_READY_NO_ROW_ACCEPTED"),
        ("FBR1593_11_verdict", "finite beta acquisition pack", "zero theorem failed for now, so beta/source rows are the honest fallback", "not claim-grade", "source-backed finite rows or exact zero theorem", "local GR/Newton/PPN/R10/WEP/clock/orbital", "FINITE_BETA_SOURCE_ROWS_READY_NONCLAIM"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "row_id": row_id,
            "quantity": quantity,
            "definition": definition,
            "required_units": units,
            "required_source": required_source,
            "observable_links": observable_links,
            "current_status": status,
            **false_flags(),
        }
        for row_id, quantity, definition, units, required_source, observable_links, status in rows
    ]


def source_residual_rows() -> list[dict[str, Any]]:
    rows = [
        ("SWR1593_0_common_factor", "w_star", "common constant factor may be absorbed into measured G_N only if derivative, species, range, frame and domain silence all hold", "MISSING_COMMON_ACTION_NORMALIZATION", "do not hide non-common weights in G_N"),
        ("SWR1593_1_relative_weight", "Delta_w_A", "q_source^nu includes P_loc nabla_mu sum_A Delta_w_A T_A^munu plus boundary/projector/readout terms", "FIRST_FILL_ROW_READY_VALUE_MISSING", "source-normalized Newton and common matter blocked"),
        ("SWR1593_2_phi_dependent_weight", "beta_w_A", "if w_A depends on phi, beta_w_A contributes to finite scalar exchange through beta_source beta_test products", "BETA_WEIGHT_FUNCTION_MISSING", "R10/PPN/WEP finite force rows blocked"),
        ("SWR1593_3_readout_weight", "readout kernel weight", "post-variation readout can reweight reported WEP/clock/orbital residuals unless variation-before-readout and projection silence close", "READOUT_PROJECTION_UNSIGNED", "arena-specific tails retained"),
        ("SWR1593_4_measure_jacobian", "measure/coframe descent weight", "species-dependent Jacobian or hidden frame can mimic action weights even if the bare action is common", "MEASURE_COFRAME_DESCENT_UNSIGNED", "beta_geom and epsilon_tail retained"),
        ("SWR1593_5_no_absorption_guard", "measured-G guard", "only w_A=w_star with no derivative or composition dependence is calibration; every relative or phi-dependent part is physics", "GUARD_ACTIVE_INPUTS_MISSING", "no measured-G shortcut"),
        ("SWR1593_6_verdict", "source residual vector", "action-weight/source residual is converted into explicit nonclaim rows instead of being silently deleted", "SOURCE_RESIDUAL_VECTOR_READY_NONCLAIM", "finite rows or parent theorem required"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "residual_id": residual_id,
            "quantity": quantity,
            "residual_law_or_guard": law,
            "current_status": status,
            "effect": effect,
            **false_flags(),
        }
        for residual_id, quantity, law, status, effect in rows
    ]


def local_gr_impact_rows() -> list[dict[str, Any]]:
    rows = [
        ("LGI1593_0_R10", "short-range alpha(lambda)", "requires alpha(lambda)=K(lambda) beta_source beta_test plus tails, with real bound curve", "BLOCKED_BETA_PRODUCT_MISSING", "no R10 score"),
        ("LGI1593_1_PPN_gamma", "PPN gamma", "range suppression cannot replace coupling suppression; Q_norm and beta/tail rows must be source-backed", "BLOCKED_QNORM_BETA_INPUTS_MISSING", "no Cassini score"),
        ("LGI1593_2_Newton", "Newton source side", "requires common source normalization, no relative w_A, and Bianchi-compatible current owner", "BLOCKED_ACTION_WEIGHT_COUNTEREXAMPLE", "no Newton-source promotion"),
        ("LGI1593_3_WEP_common_matter", "WEP/common matter", "requires zero or bounded material beta_const, beta_weight and readout kernels", "BLOCKED_MATTER_PACKAGE_UNSIGNED", "no common-matter theorem"),
        ("LGI1593_4_clocks", "clock/fine-structure", "constant superselection or finite beta_const rows required", "BLOCKED_CONSTANTS_UNSIGNED", "no clock claim"),
        ("LGI1593_5_orbital", "orbital/local dynamics", "requires source/test beta rows, worldtube/source profile and tail envelope", "BLOCKED_PROFILE_KERNELS_MISSING", "no orbital claim"),
        ("LGI1593_6_local_GR", "GR reduction", "local GR needs coupling zero/finite pass, conservation, common matter and source-normalized Newton under one parent action", "BLOCKED_NO_CLAIM", "1584 refusal remains correct"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "impact_id": impact_id,
            "arena": arena,
            "requirement": requirement,
            "status": status,
            "consequence": consequence,
            **false_flags(),
        }
        for impact_id, arena, requirement, status, consequence in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN1593_0_zero_theorem", "accept g_c=0 only if every package gate is signed", "ZTH1593 verdict is not closed and package gates fail", "REJECT_ZERO_COUPLING_CLAIM", "beta rows required"),
        ("RUN1593_1_finite_beta", "accept finite beta score only if beta_source, beta_test, kernel, tail, units, source paths and arena maps are present", "finite beta rows are first-fill templates with missing values", "REJECT_FINITE_BETA_SCORE", "no alpha/gamma score"),
        ("RUN1593_2_action_weights", "accept measured-G absorption only for common derivative-silent w_star", "Delta_w_A and beta_w rows missing/exclusion theorem unsigned", "REJECT_G_ABSORPTION_SHORTCUT", "Newton/common-matter branch blocked"),
        ("RUN1593_3_range_vs_coupling", "do not treat mu_m2 range suppression as coupling suppression", "1592 range law exists but beta package missing", "REJECT_RANGE_ONLY_CLAIM", "range and coupling stay separate"),
        ("RUN1593_4_local_GR", "accept local GR only if beta, common matter, conservation and Newton source gates close under same parent action", "1584 runner blocks local GR", "REJECT_LOCAL_GR_REENTRY", "continue derivation/source rows"),
        ("RUN1593_5_branch_lock", "future rows must carry same branch id and no MISSING/toy/proxy markers", f"all 1593 rows use {BRANCH_ID}", "BRANCH_LOCK_OK_INPUTS_PENDING", "hygiene passes; physics pending"),
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
        ("GATE1593_0_gc_zero", "canonical coupling zero theorem", "BLOCKED_NO_CLAIM", "matter package gates do not close"),
        ("GATE1593_1_beta_rows", "finite beta_source beta_test score", "BLOCKED_NO_CLAIM", "beta rows are first-fill templates with missing values"),
        ("GATE1593_2_action_weights", "action-weight exclusion", "BLOCKED_NO_CLAIM", "live pre-variation w_A counterexample survives"),
        ("GATE1593_3_Newton", "Newton source normalization", "BLOCKED_NO_CLAIM", "common factor/Delta_w and current-owner gates open"),
        ("GATE1593_4_R10_PPN", "R10/PPN local empirical score", "BLOCKED_NO_CLAIM", "beta product, kernels and tails missing"),
        ("GATE1593_5_WEP_clock_orbital", "WEP/clock/orbital pass", "BLOCKED_NO_CLAIM", "material constants, readout and tails remain unresolved"),
        ("GATE1593_6_local_GR", "local GR reduction", "BLOCKED_NO_CLAIM", "coupling, conservation, common matter and Newton gates not closed together"),
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
            "DEC1593_0_zero_route_status",
            "CANONICAL_COUPLING_ZERO_THEOREM_IS_SHARP_BUT_UNSIGNED",
            "the chain-rule theorem is mathematically clear, but q-kernel, coframe, matter lift, constants, action weights, current owner and boundary/readout do not close together",
            "do not claim g_c=0; keep theorem as the exact contract",
        ),
        (
            "DEC1593_1_finite_fallback",
            "FINITE_BETA_ROWS_ARE_NOW_MANDATORY_FALLBACK",
            "range suppression without beta_source beta_test cannot score local tests or prove GR reduction",
            "source beta_source, beta_test, Delta_w, beta_weight, kernels and tails before empirical scoring",
        ),
        (
            "DEC1593_2_main_next_gate",
            "ACTION_WEIGHT_AND_SOURCE_CURRENT_OWNER_ARE_HIGHEST_PRESSURE",
            "the w_A counterexample preserves classical-looking equations while breaking Hilbert source normalization",
            "attack parent action-measure/object-language/current-owner proof before data scoring",
        ),
        (
            "DEC1593_3_next",
            "NEXT_1594_ACTION_WEIGHT_EXCLUSION_OR_BETA_SOURCE_ACQUISITION_VALIDATOR",
            "the least-scrutiny route is to kill the w_A counterexample; otherwise build a validator that refuses all beta rows lacking source paths, units and arena maps",
            "derive action-measure/source-current theorem or implement strict beta acquisition validator",
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
            "next_target": "1594-Y5-R2FR-action-weight-exclusion-or-beta-source-acquisition-validator.md",
            "script": "scripts/Y5_R2FR_action_weight_exclusion_or_beta_source_acquisition_validator.py",
            "objective": "try to derive a parent action-measure/object-language/current-owner theorem that excludes independent pre-variation source weights w_A; if not, build a strict validator for finite beta_source, beta_test, Delta_w, kernel and tail rows",
            "success_condition": "parent-signed action-weight exclusion and common source normalization, or executable nonclaim validator that rejects every unsourced beta/local arena row",
            "do_not": "do not absorb relative/source-dependent weights into measured G, do not score local tests from beta templates, do not edit formalization-workbench or GitHub",
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
    flag_columns = {"score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed", "clause_signed", "theorem_closed"}
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


def has_1593_rows(folder: Path) -> bool:
    if not folder.exists():
        return False
    return any("1593" in csv_path.name for csv_path in folder.glob("*.csv"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    zero = read_csv(ZERO_THEOREM)
    package = read_csv(PACKAGE_GATE)
    beta = read_csv(FINITE_BETA_ROWS)
    source_residual = read_csv(SOURCE_RESIDUAL)
    impact = read_csv(LOCAL_GR_IMPACT)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    required_beta = {"beta_source", "beta_test", "beta_source*beta_test", "Delta_w_A", "epsilon_tail"}
    checks = [
        ("VAL1593_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1593 source paths exist"),
        ("VAL1593_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all 1593 source needles found"),
        (
            "VAL1593_2_zero_theorem_not_closed",
            any(row["theorem_id"] == "ZTH1593_8_verdict" and row["status"] == "ZERO_THEOREM_NOT_CLOSED_FINITE_BETA_ROWS_REQUIRED" for row in zero),
            "canonical coupling zero theorem remains conditional and unsigned",
        ),
        (
            "VAL1593_3_package_gates_fail",
            any(row["gate_id"] == "PKG1593_8_verdict" and row["current_status"] == "PACKAGE_FAILS_CURRENT_CLAIM" for row in package)
            and all(row["clause_signed"] == "False" for row in package),
            "matter package gates remain unsigned",
        ),
        (
            "VAL1593_4_finite_beta_rows_present_nonclaim",
            required_beta.issubset({row["quantity"] for row in beta}) and all(row["valid_for_claim"] == "False" for row in beta),
            "finite beta/source rows are present and nonclaim",
        ),
        (
            "VAL1593_5_source_residual_guard_present",
            any(row["residual_id"] == "SWR1593_6_verdict" and row["current_status"] == "SOURCE_RESIDUAL_VECTOR_READY_NONCLAIM" for row in source_residual),
            "action-weight/source residual vector guard is present",
        ),
        (
            "VAL1593_6_local_gr_impact_blocked",
            any(row["impact_id"] == "LGI1593_6_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in impact),
            "local GR impact map keeps GR/Newton blocked",
        ),
        (
            "VAL1593_7_runner_rejects_current_claims",
            any(row["runner_result"] == "REJECT_ZERO_COUPLING_CLAIM" for row in runner)
            and any(row["runner_result"] == "REJECT_FINITE_BETA_SCORE" for row in runner)
            and any(row["runner_result"] == "REJECT_G_ABSORPTION_SHORTCUT" for row in runner)
            and any(row["runner_result"] == "REJECT_LOCAL_GR_REENTRY" for row in runner),
            "runner refuses zero-coupling, finite beta, measured-G shortcut and local-GR claims",
        ),
        (
            "VAL1593_8_claim_gates_closed",
            all(row["status"] == "BLOCKED_NO_CLAIM" and row["claim_allowed"] == "False" for row in gates),
            "all 1593 claim gates remain closed",
        ),
        (
            "VAL1593_9_decision_next",
            any(row["decision"] == "NEXT_1594_ACTION_WEIGHT_EXCLUSION_OR_BETA_SOURCE_ACQUISITION_VALIDATOR" for row in decisions),
            "decision selects action-weight exclusion or beta source validator",
        ),
        ("VAL1593_10_csv_parse", all(len(read_csv(csv_path)) > 0 for csv_path in generated_csvs), "all generated 1593 CSVs parse cleanly"),
        ("VAL1593_11_claim_flags_false", generated_flags_false(generated_csvs), "all generated claim/prediction/theorem flags remain false"),
        ("VAL1593_12_no_raw_accepted", not has_1593_rows(RAB_RAW) and not has_1593_rows(RAB_ACCEPTED), "no 1593 rows written to raw/accepted finite directories"),
        ("VAL1593_13_branch_copies", all(target_path.exists() for target_paths in COPY_TARGETS.values() for target_path in target_paths), "branch/quarantine nonclaim copies written"),
        ("VAL1593_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1593_15_formalization_untouched", formalization_scope_clean(generated_csvs), "all generated 1593 paths are outside formalization-workbench; git status is clean when available"),
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
            "check_id": "VAL1593_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1593 canonical coupling zero theorem or finite beta source rows validation",
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
    zero: list[dict[str, Any]],
    package: list[dict[str, Any]],
    beta: list[dict[str, Any]],
    source_residual: list[dict[str, Any]],
    impact: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1593 - R2/fR Canonical Coupling Zero Theorem Or Finite Beta Source Rows",
                "## Verdict\n"
                "- 1593 proves the useful conditional statement: if the canonical mode is quotient-vertical, ordinary matter descends only through the quotient-owned observed coframe, constants are phi-blind, action weights are excluded, the current owner descends, and boundary/readout tails are silent, then `g_c=0` and `beta_source=beta_test=0`.\n"
                "- That is **not** yet a live theorem: the parent package fails on `Dq[v_phi]`, observed coframe/no-shadow-frame descent, matter lift, constant superselection, action-weight exclusion, source-current ownership, and boundary/readout silence.\n"
                "- The big gremlin is still the pre-variation source/action weight `w_A`: it can preserve classical-looking matter equations while changing the Hilbert source side, so it cannot be absorbed into measured `G_N` unless it is common and derivative-silent.\n"
                "- The honest fallback is now explicit finite rows for `beta_source`, `beta_test`, `beta_source*beta_test`, `Delta_w_A`, `beta_w`, profile kernels, and tail envelopes.\n"
                "- No local-GR, Newton, PPN, R10, WEP, clock, orbital, coupling-zero, common-matter or public claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## Coupling Zero Theorem Attempt",
                md_table(zero, ["theorem_id", "clause", "required_statement", "would_close", "status", "blocking_gap"]),
                "## Matter Package Clause Gate",
                md_table(package, ["gate_id", "required_clause", "source_basis", "current_status", "fallback"]),
                "## Finite Beta Source Rows",
                md_table(beta, ["row_id", "quantity", "definition", "required_units", "required_source", "observable_links", "current_status"]),
                "## Action-Weight Source Residual",
                md_table(source_residual, ["residual_id", "quantity", "residual_law_or_guard", "current_status", "effect"]),
                "## Local GR Impact Map",
                md_table(impact, ["impact_id", "arena", "requirement", "status", "consequence"]),
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
    zero = zero_theorem_rows()
    package = package_gate_rows()
    beta = finite_beta_rows()
    source_residual = source_residual_rows()
    impact = local_gr_impact_rows()
    runner = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        ZERO_THEOREM,
        PACKAGE_GATE,
        FINITE_BETA_ROWS,
        SOURCE_RESIDUAL,
        LOCAL_GR_IMPACT,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(ZERO_THEOREM, zero)
    write_csv(PACKAGE_GATE, package)
    write_csv(FINITE_BETA_ROWS, beta)
    write_csv(SOURCE_RESIDUAL, source_residual)
    write_csv(LOCAL_GR_IMPACT, impact)
    write_csv(RUNNER, runner)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, zero, package, beta, source_residual, impact, runner, gates, decisions, validation, next_rows)


if __name__ == "__main__":
    main()

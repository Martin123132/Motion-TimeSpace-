from __future__ import annotations

import math
from pathlib import Path

from Y5_R2FR_Dq_vX_observed_metric_zero_or_finite_DObs_leak_row_2025 import (
    BRANCH_WEP,
    OUT,
    QUEUE,
    ROOT,
    SOURCE_WEIGHT_DOCS,
    base_row,
    count_formalization_modified,
    csv_rows_parse,
    md_table,
    read_text,
    remove_pycache,
    write_csv,
)


DOC = ROOT / "2161-Y5-R2FR-parent-NX-lambda-extraction-or-PPN-vector-envelope.md"
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"

DOCS = {
    "2160": ROOT / "2160-Y5-R2FR-PPN-common-frame-cg-translation-and-normalization-gate.md",
    "2160_validation": OUT / "P8_Y5_BRR545_2160_VALIDATION.csv",
    "2160_next": OUT / "P8_Y5_PARENT_QLOC_2160_NEXT_TARGET.csv",
    "2160_ppn_vector": OUT / "P8_Y5_PARENT_QLOC_2160_PPN_RESIDUAL_VECTOR_ENVELOPE.csv",
    "1854": ROOT / "1854-Y5-R2FR-parent-Hessian-input-extraction-for-ZX-MX2.md",
    "1854_validation": OUT / "P8_Y5_BRR545_1854_VALIDATION.csv",
    "1855": ROOT / "1855-Y5-R2FR-minimal-parent-X-sector-action-clause-or-demotion.md",
    "1855_validation": OUT / "P8_Y5_BRR545_1855_VALIDATION.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2161_SOURCE_REGISTER.csv",
    "extraction": OUT / "P8_Y5_PARENT_QLOC_2161_NX_LAMBDA_EXTRACTION_ATTEMPT.csv",
    "hessian_audit": OUT / "P8_Y5_PARENT_QLOC_2161_PARENT_HESSIAN_INPUT_AUDIT.csv",
    "required_clause": OUT / "P8_Y5_PARENT_QLOC_2161_REQUIRED_PARENT_ACTION_CLAUSE.csv",
    "ppn_vector": OUT / "P8_Y5_PARENT_QLOC_2161_PPN_VECTOR_ENVELOPE.csv",
    "component_status": OUT / "P8_Y5_PARENT_QLOC_2161_VECTOR_COMPONENT_STATUS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2161_CLAIM_GATE.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2161_REFUSAL_RUNNER.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2161_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2161_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2161_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2161_VALIDATION.csv",
}

BRANCH_COPIES = {
    "source_weight": SOURCE_WEIGHT_DOCS / "AFRAME_NX_LAMBDA_PPN_VECTOR_2161_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2161_PPN_VECTOR_NONCLAIM.csv",
    "queue": QUEUE / "JR2161_PARENT_X_SECTOR_OR_PPN_VECTOR_QUEUE.csv",
}

CASSINI_DELTA_GAMMA_BOUND = 6.7e-5
CASSINI_ALPHA_PROXY = math.sqrt(CASSINI_DELTA_GAMMA_BOUND / (2.0 - CASSINI_DELTA_GAMMA_BOUND))


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid"}


def has_any(text: str, alternatives: list[str]) -> bool:
    return any(item in text for item in alternatives)


def find_line(path: Path, alternatives: list[str]) -> tuple[int, str]:
    text = read_text(path) if path.exists() else ""
    for line_number, line in enumerate(text.splitlines(), start=1):
        if has_any(line, alternatives):
            return line_number, line.strip()
    return 0, "MISSING_NEEDLE"


def formalization_has_2161_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2161-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2161*",
        "*P8_Y5_BRR545_2161*",
        "*Y5_R2FR_parent_NX_lambda_extraction_or_PPN_vector_envelope_2161*",
        "*AFRAME_NX_LAMBDA_PPN_VECTOR_2161*",
        "*JR2161*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2161_00_2160_handoff",
            DOCS["2160"],
            [["NEXT2160_0_2161"], ["NX2160_4_verdict"], ["PPV2160_6_total_abs_guard"]],
            "2160 selects parent N_X/lambda extraction with PPN vector fallback.",
        ),
        (
            "SRC2161_01_2160_validation",
            DOCS["2160_validation"],
            [["VAL2160_OVERALL"], ["PASS"]],
            "2160 validation passed as nonclaim.",
        ),
        (
            "SRC2161_02_2160_next_csv",
            DOCS["2160_next"],
            [["NEXT2160_0_2161"], ["parent Z_X"], ["M_X^2"]],
            "machine-readable 2161 handoff.",
        ),
        (
            "SRC2161_03_2160_vector_csv",
            DOCS["2160_ppn_vector"],
            [["PPV2160_6_total_abs_guard"], ["SCHEMA_READY_VALUES_MISSING"]],
            "active PPN vector schema to carry forward.",
        ),
        (
            "SRC2161_04_1854_hessian_scan",
            DOCS["1854"],
            [["HCA1854_6_verdict"], ["EXT1854_5_verdict"], ["NO_CLAIM_GRADE_ZX_OR_MX2_FOUND"]],
            "prior parent Hessian extraction attempt failed to source Z_X/M_X^2.",
        ),
        (
            "SRC2161_05_1854_validation",
            DOCS["1854_validation"],
            [["VAL1854_OVERALL"], ["PASS"]],
            "1854 validation passed as nonclaim.",
        ),
        (
            "SRC2161_06_1855_closure_clause",
            DOCS["1855"],
            [["MXA1855_2_quadratic_block"], ["LAW1855_1_canonical_field"], ["VAL1855_OVERALL"]],
            "1855 wrote a minimal X-sector closure candidate, not a derived parent result.",
        ),
        (
            "SRC2161_07_1855_validation",
            DOCS["1855_validation"],
            [["VAL1855_OVERALL"], ["PASS"]],
            "1855 validation passed as nonclaim.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle_groups, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles_found = exists and all(has_any(text, group) for group in needle_groups)
        rows.append(
            row(
                source_id=source_id,
                source_path=str(path),
                path_exists=exists,
                needles_found=needles_found,
                expected_needles="; ".join(" OR ".join(group) for group in needle_groups),
                role=role,
            )
        )
    return rows


def nx_lambda_extraction_rows() -> list[dict[str, object]]:
    data = [
        (
            "NLE2161_0_Xhat_owner",
            "Xhat",
            "same coordinate must own c_g, Z_X, M_X^2, J_X, tau_PPN and lambda_X",
            "NOT_PARENT_SIGNED",
            "1855 gives a closure clause only; no primitive motion/time/space derivation owns the coordinate",
        ),
        (
            "NLE2161_1_ZX",
            "Z_X",
            "kinetic Hessian coefficient in S_X^(2)",
            "MISSING_ZX",
            "formula appears, but no same-branch positive coefficient with units and source path is extracted",
        ),
        (
            "NLE2161_2_MX2",
            "M_X^2",
            "mass-gap/Hessian curvature in S_X^(2)",
            "MISSING_MX2",
            "no mass gap, zero-mass protection theorem, or finite eigenvalue extraction is parent-signed",
        ),
        (
            "NLE2161_3_NX_relation",
            "N_X",
            "N_X = 1/sqrt(Z_X)",
            "RELATION_ONLY_VALUES_MISSING",
            "canonical normalization is exact if Z_X is owned, but Z_X is missing",
        ),
        (
            "NLE2161_4_lambda_relation",
            "lambda_X",
            "lambda_X = sqrt(Z_X/M_X^2)",
            "RELATION_ONLY_VALUES_MISSING",
            "range routing is exact if Z_X and M_X^2 are owned, but both are missing",
        ),
        (
            "NLE2161_5_cassini_object",
            "alpha_eff_PPN",
            f"|tau_PPN S_PPN(lambda_X,env) c_g/sqrt(Z_X) + alpha_vec_tail| <= {CASSINI_ALPHA_PROXY:.15g}",
            "CONDITIONAL_OBJECT_ONLY",
            "Cassini pressure is real only on alpha_eff, not raw c_g",
        ),
        (
            "NLE2161_6_verdict",
            "parent N_X/lambda extraction",
            "N_X and lambda_X cannot be promoted from relations to inputs",
            "FAIL_CURRENT_CLAIM_NX_LAMBDA_NOT_EXTRACTED",
            "direct c_g, R10/local-GR/PPN pass, and finite-range routing remain blocked",
        ),
    ]
    return [
        row(extraction_id=extraction_id, target=target, formula_or_requirement=formula_or_requirement, status=status, consequence=consequence)
        for extraction_id, target, formula_or_requirement, status, consequence in data
    ]


def parent_hessian_audit_rows() -> list[dict[str, object]]:
    data = [
        (
            "PHA2161_0_quadratic_formula",
            "S_X^(2)=-1/2 int sqrt(-g) M_Pl^2 [Z_X (grad Xhat)^2 + M_X^2 Xhat^2] + int sqrt(-g) Xhat J_X",
            "CANDIDATE_CLOSURE_FORMULA",
            "not derived from parent MTS primitives",
        ),
        (
            "PHA2161_1_same_branch_lock",
            "one branch must supply Xhat, c_g, Z_X, M_X^2, J_X, tau_PPN, tau_R10 and boundary data",
            "MISSING_SAME_BRANCH_LOCK",
            "current rows mix formula templates, source proxies and closure assumptions",
        ),
        (
            "PHA2161_2_cross_block",
            "Hessian cross-blocks must vanish, be diagonalized, or be carried into a Schur-complement effective Z/M pair",
            "MISSING_CROSS_HESSIAN_BLOCK",
            "single-field c_g isolation is unsafe without the multi-component residual vector",
        ),
        (
            "PHA2161_3_source_boundary",
            "J_X, support, boundary, domain and readout terms must be declared before a local no-hair or PPN pass",
            "MISSING_SOURCE_BOUNDARY_LOCK",
            "source-free local GR cannot be claimed by silence",
        ),
        (
            "PHA2161_4_units_signs",
            "Z_X>0, M_X^2>=0 or protected zero, and unit conventions must be specified in one parent action",
            "MISSING_UNITS_AND_SIGN_SIGNATURE",
            "normalization and range are not numerically scoreable",
        ),
        (
            "PHA2161_5_verdict",
            "parent Hessian input audit: exact formulas are known, but parent-owned coefficients are not present",
            "FAIL_PARENT_HESSIAN_INPUTS_STILL_MISSING",
            "2161 must route to either a minimal parent X-sector derivation or a nonclaim PPN vector envelope",
        ),
    ]
    return [
        row(audit_id=audit_id, requirement=requirement, current_status=current_status, why_it_matters=why_it_matters)
        for audit_id, requirement, current_status, why_it_matters in data
    ]


def required_parent_action_clause_rows() -> list[dict[str, object]]:
    data = [
        (
            "PAC2161_0_field_owner",
            "Declare a primitive parent object Xhat with fixed normalization and branch identity.",
            "Xhat is not introduced post hoc to fit the test channel.",
            "REQUIRED_NEXT",
        ),
        (
            "PAC2161_1_quadratic_action",
            "Derive the quadratic block for Xhat from the parent action.",
            "Z_X, M_X^2, J_X and boundary terms share one source.",
            "REQUIRED_NEXT",
        ),
        (
            "PAC2161_2_second_variation",
            "Show delta^2 S_parent/dXhat^2 gives positive kinetic coefficient and signed mass/range term.",
            "N_X=1/sqrt(Z_X) and lambda_X=sqrt(Z_X/M_X^2) become physical inputs.",
            "REQUIRED_NEXT",
        ),
        (
            "PAC2161_3_cross_hessian",
            "Either prove block diagonalization or compute the Schur-complement effective X-sector.",
            "prevents hiding PPN tails in omitted variables.",
            "REQUIRED_NEXT",
        ),
        (
            "PAC2161_4_source_boundary",
            "Derive or explicitly carry J_X, support, boundary, domain and readout terms.",
            "local-vacuum/source-free claims require signed silence, not absence from notation.",
            "REQUIRED_NEXT",
        ),
        (
            "PAC2161_5_ppn_interface",
            "Derive tau_PPN, S_PPN(lambda_X,env), b_dis, q_nonH and calibration tails from the same action.",
            "Cassini/PPN comparison becomes a real MTS prediction rather than a scalar proxy.",
            "REQUIRED_NEXT",
        ),
        (
            "PAC2161_6_claim_rule",
            "Only allow claims if every row above is parent-owned or the missing term is bounded in the vector envelope.",
            "prevents one-parameter local-GR overclaims.",
            "ACTIVE_RULE",
        ),
    ]
    return [
        row(clause_id=clause_id, required_clause=required_clause, closes=closes, status=status)
        for clause_id, required_clause, closes, status in data
    ]


def ppn_vector_rows() -> list[dict[str, object]]:
    data = [
        (
            "PVE2161_0_cg",
            "common conformal coupling",
            "alpha_cg = tau_g S_PPN(lambda_X,env) c_g/sqrt(Z_X)",
            "MISSING_ZX_TAU_RANGE",
            "Cassini gamma/Shapiro leg cannot be reduced to raw c_g",
        ),
        (
            "PVE2161_1_disformal",
            "disformal/preferred-frame tail",
            "alpha_dis = tau_dis b_dis",
            "MISSING_DISFORMAL_PPN_PROJECTION",
            "preferred-frame and clock terms may survive even if alpha_cg is small",
        ),
        (
            "PVE2161_2_nonH",
            "non-Hilbert/source-current tail",
            "alpha_nonH = tau_nonH q_nonH",
            "MISSING_NONHILBERT_PPN_PROJECTION",
            "source normalization and conservation tails must not be silently cancelled",
        ),
        (
            "PVE2161_3_support",
            "support/domain local-projection tail",
            "alpha_support = tau_support Delta_W_support + tau_domain q_domain",
            "MISSING_SUPPORT_DOMAIN_PPN_PROJECTION",
            "finite-source and representative-domain choices can leak into PPN readout",
        ),
        (
            "PVE2161_4_boundary",
            "boundary/local flux tail",
            "alpha_boundary = tau_boundary q_boundary",
            "MISSING_BOUNDARY_PPN_PROJECTION",
            "local-vacuum plateau cannot be asserted while boundary flux is unsigned",
        ),
        (
            "PVE2161_5_readout",
            "measured-G/readout calibration tail",
            "alpha_readout = tau_readout C_readout",
            "MISSING_READOUT_PPN_PROJECTION",
            "observed GM/gamma extraction may absorb or expose the coupling",
        ),
        (
            "PVE2161_6_total_abs_guard",
            "absolute no-cancellation PPN envelope",
            "|alpha_PPN_total| <= |alpha_cg|+|alpha_dis|+|alpha_nonH|+|alpha_support|+|alpha_boundary|+|alpha_readout|",
            "SCHEMA_READY_VALUES_MISSING",
            "component rows now exist, but none are claim-grade numeric predictions",
        ),
        (
            "PVE2161_7_source_proxy_ceiling",
            "Cassini scalar proxy ceiling",
            f"|alpha_PPN_total| <= {CASSINI_ALPHA_PROXY:.15g} only after the vector is the actual MTS PPN observable",
            "SOURCE_PROXY_ONLY",
            "use as pressure/target, not as pass/fail claim",
        ),
    ]
    return [
        row(vector_id=vector_id, component=component, formula=formula, status=status, issue=issue)
        for vector_id, component, formula, status, issue in data
    ]


def vector_component_status_rows() -> list[dict[str, object]]:
    data = [
        (
            "VCS2161_0_cg_leg",
            "c_g/sqrt(Z_X)",
            "needs Z_X, tau_g, lambda_X, S_PPN and vector-tail subtraction/absolute envelope",
            "BLOCKED_MISSING_PARENT_INPUTS",
            False,
        ),
        (
            "VCS2161_1_disformal_leg",
            "b_dis",
            "needs matter metric expansion and preferred-frame projection",
            "BLOCKED_MISSING_ARENA_PROJECTION",
            False,
        ),
        (
            "VCS2161_2_nonH_leg",
            "q_nonH",
            "needs non-Hilbert current/source law and conservation accounting",
            "BLOCKED_MISSING_ARENA_PROJECTION",
            False,
        ),
        (
            "VCS2161_3_support_leg",
            "Delta_W_support/q_domain",
            "needs representative-domain and support-dependence theorem",
            "BLOCKED_MISSING_PARENT_INPUTS",
            False,
        ),
        (
            "VCS2161_4_boundary_leg",
            "q_boundary",
            "needs local flux/boundary condition signed by parent action",
            "BLOCKED_MISSING_PARENT_INPUTS",
            False,
        ),
        (
            "VCS2161_5_readout_leg",
            "C_readout",
            "needs map between varied metric, measured G, orbital GM and PPN gamma observable",
            "BLOCKED_MISSING_ARENA_PROJECTION",
            False,
        ),
        (
            "VCS2161_6_total",
            "alpha_PPN_total",
            "all legs must be zero by theorem or bounded without cancellation",
            "SCHEMA_READY_VALUES_MISSING",
            False,
        ),
    ]
    return [
        row(status_id=status_id, quantity=quantity, required_input=required_input, status=status, claim_ready=claim_ready)
        for status_id, quantity, required_input, status, claim_ready in data
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("CG2161_0_relations", "N_X and lambda_X relations are exact conditional formulas", True, "formulas follow from the quadratic block if it is parent-owned"),
        ("CG2161_1_ZX_parent_owned", "Z_X is parent-owned, positive and normalized", False, "MISSING_ZX"),
        ("CG2161_2_MX2_parent_owned", "M_X^2 is parent-owned or zero-protected", False, "MISSING_MX2"),
        ("CG2161_3_tau_range_owned", "tau_PPN and S_PPN(lambda_X,env) are derived", False, "MISSING_TAU_PPN_AND_RANGE_TRANSFER"),
        ("CG2161_4_vector_components", "PPN residual vector is zero or no-cancellation bounded", False, "SCHEMA_READY_VALUES_MISSING"),
        ("CG2161_5_direct_cg_bound", "raw c_g has a source-backed MTS bound", False, "raw c_g is not invariant; only c_g/sqrt(Z_X) enters"),
        ("CG2161_6_R10_PPN_local_pass", "R10/PPN/local-GR claims are allowed", False, "parent coefficients and vector projections missing"),
    ]
    return [row(gate_id=gate_id, claim=claim, gate_pass=gate_pass, reason=reason) for gate_id, claim, gate_pass, reason in data]


def refusal_rows() -> list[dict[str, object]]:
    data = [
        ("REF2161_0_promote_NX", "promote N_X=1/sqrt(Z_X) to numeric input", "MISSING_ZX", "BLOCKED", "relation-only until Z_X is parent-owned", False),
        ("REF2161_1_promote_lambda", "route local tests using lambda_X", "MISSING_ZX_MX2", "BLOCKED", "range cannot be classified without same-branch Hessian data", False),
        ("REF2161_2_raw_cg_bound", "bind raw c_g directly with Cassini", "NORMALIZATION_GAUGE_DEPENDENCE", "BLOCKED", "field rescaling changes raw c_g but not c_g/sqrt(Z_X)", False),
        ("REF2161_3_single_component_ppn", "score only the c_g leg", "VECTOR_TAILS_UNCONTROLLED", "BLOCKED", "disformal, non-Hilbert, support, boundary and readout tails remain", False),
        ("REF2161_4_local_gr_pass", "claim local GR/Newton recovered", "PPN_METRIC_AND_SOURCE_LIMITS_MISSING", "BLOCKED", "requires full local metric expansion plus conservation/source silence", False),
    ]
    return [
        row(refusal_id=refusal_id, attempted_claim=attempted_claim, input_status=input_status, runner_result=runner_result, blocked_by=blocked_by, score_eligible=score_eligible)
        for refusal_id, attempted_claim, input_status, runner_result, blocked_by, score_eligible in data
    ]


def decision_rows() -> list[dict[str, object]]:
    data = [
        (
            "DEC2161_0_extraction_result",
            "The active branch still does not extract parent-owned N_X or lambda_X.",
            "Z_X and M_X^2 remain relation-only closure quantities, not primitive MTS outputs.",
            "do not claim raw c_g, R10 routing, PPN pass, local GR or Newton limit",
        ),
        (
            "DEC2161_1_demote_raw_cg",
            "Raw c_g is demoted as a directly bound object.",
            "the invariant comparison object is c_g/sqrt(Z_X) inside the full PPN residual vector.",
            "score only alpha_eff_PPN or the no-cancellation vector once components are sourced",
        ),
        (
            "DEC2161_2_no_more_proxy_loop",
            "The Cassini proxy has done its job.",
            "repeating the scalar-tensor inversion will not fill Z_X, M_X^2, tau_PPN or tail terms.",
            "next work must either derive the parent X-sector clause or fill vector component bounds",
        ),
        (
            "DEC2161_3_next_choice",
            "Best next route is a minimal parent X-sector action clause attempt, with vector fill as fallback.",
            "this attacks the missing coupling/normalization at the source rather than circling the same bound.",
            "2162-Y5-R2FR-minimal-parent-X-sector-action-clause-or-PPN-vector-fill.md",
        ),
    ]
    return [row(decision_id=decision_id, decision=decision, because=because, next_action=next_action) for decision_id, decision, because, next_action in data]


def next_target_rows() -> list[dict[str, object]]:
    data = [
        (
            "NEXT2161_0_2162",
            "2162-Y5-R2FR-minimal-parent-X-sector-action-clause-or-PPN-vector-fill.md",
            "scripts/Y5_R2FR_minimal_parent_X_sector_action_clause_or_PPN_vector_fill_2162.py",
            "construct the smallest parent X-sector action clause that signs Xhat, Z_X, M_X^2, cross-Hessian/Schur, source and boundary; if not justified, fill PPN vector component rows as nonclaim",
            "selected",
            "either Z_X/M_X^2/tau/range become parent-owned enough to test, or the c_g route is explicitly closure/source-proxy only",
        ),
        (
            "NEXT2161_1_parallel",
            "2162b-Y5-R2FR-no-hidden-visible-hom-operator-domain-theorem.md",
            "scripts/Y5_R2FR_no_hidden_visible_hom_operator_domain_theorem_2162b.py",
            "try to prove shadow-frame/disformal/non-Hilbert/readout vector legs vanish by an operator-domain theorem",
            "held",
            "if proven, the PPN vector collapses and the clean c_g/sqrt(Z_X) route reopens",
        ),
    ]
    return [
        row(route_id=route_id, next_target=next_target, script=script, objective=objective, selection_status=selection_status, success_condition=success_condition)
        for route_id, next_target, script, objective, selection_status, success_condition in data
    ]


def write_branch_copies(
    extraction: list[dict[str, object]],
    hessian: list[dict[str, object]],
    ppn_vector: list[dict[str, object]],
    component_status: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        ("COPY2161_0_source_weight_docs", BRANCH_COPIES["source_weight"], extraction + hessian),
        ("COPY2161_1_branch_locked_wep", BRANCH_COPIES["branch_wep"], ppn_vector + component_status),
        ("COPY2161_2_acquisition_queue", BRANCH_COPIES["queue"], next_rows + component_status),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    extraction: list[dict[str, object]],
    hessian: list[dict[str, object]],
    required_clause: list[dict[str, object]],
    ppn_vector: list[dict[str, object]],
    component_status: list[dict[str, object]],
    gates: list[dict[str, object]],
    refusals: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    extraction_ok = any(item["extraction_id"] == "NLE2161_6_verdict" and item["status"] == "FAIL_CURRENT_CLAIM_NX_LAMBDA_NOT_EXTRACTED" for item in extraction)
    hessian_ok = any(item["audit_id"] == "PHA2161_5_verdict" and item["current_status"] == "FAIL_PARENT_HESSIAN_INPUTS_STILL_MISSING" for item in hessian)
    clause_ok = len(required_clause) == 7 and any(item["clause_id"] == "PAC2161_6_claim_rule" and item["status"] == "ACTIVE_RULE" for item in required_clause)
    vector_ok = any(item["vector_id"] == "PVE2161_6_total_abs_guard" and item["status"] == "SCHEMA_READY_VALUES_MISSING" for item in ppn_vector)
    component_ok = any(item["status_id"] == "VCS2161_6_total" and item["status"] == "SCHEMA_READY_VALUES_MISSING" and not truthy(item["claim_ready"]) for item in component_status)
    gate_ok = any(item["gate_id"] == "CG2161_0_relations" and truthy(item["gate_pass"]) for item in gates) and all(not truthy(item.get("claim_allowed", False)) for item in gates)
    refusal_ok = all(item["runner_result"] == "BLOCKED" and not truthy(item.get("score_eligible", False)) for item in refusals)
    decisions_ok = any(item["decision_id"] == "DEC2161_3_next_choice" and "2162" in str(item["next_action"]) for item in decisions)
    next_ok = any(item["route_id"] == "NEXT2161_0_2162" and item["selection_status"] == "selected" for item in next_rows)
    copies_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    missing_nonclaim = all(
        not truthy(item.get("valid_for_claim", False)) and not truthy(item.get("claim_allowed", False))
        for group in (extraction, hessian, ppn_vector, component_status, gates, refusals, decisions, next_rows)
        for item in group
        if "MISSING_" in " ".join(str(value) for value in item.values())
    )
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, extraction, hessian, required_clause, ppn_vector, component_status, gates, refusals, decisions, next_rows, copies)
        for item in group
    )
    direct_claims_blocked = all(
        any(item["gate_id"] == gate_id and not truthy(item["gate_pass"]) for item in gates)
        for gate_id in ("CG2161_1_ZX_parent_owned", "CG2161_2_MX2_parent_owned", "CG2161_5_direct_cg_bound", "CG2161_6_R10_PPN_local_pass")
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2161_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all(
        [
            sources_ok,
            extraction_ok,
            hessian_ok,
            clause_ok,
            vector_ok,
            component_ok,
            gate_ok,
            refusal_ok,
            decisions_ok,
            next_ok,
            copies_ok,
            csv_ok,
            missing_nonclaim,
            no_claim_flags,
            direct_claims_blocked,
            formalization_clean,
            pycache_clean,
        ]
    )
    checks = [
        ("VAL2161_00_sources", sources_ok, "2160, 1854 and 1855 source paths and needles validate"),
        ("VAL2161_01_extraction", extraction_ok, "N_X/lambda extraction attempt records the current fail state"),
        ("VAL2161_02_hessian_audit", hessian_ok, "parent Hessian input audit remains blocked"),
        ("VAL2161_03_required_clause", clause_ok, "required parent action clause is explicit"),
        ("VAL2161_04_ppn_vector", vector_ok, "PPN absolute vector envelope is carried forward"),
        ("VAL2161_05_component_status", component_ok, "component status rows keep all local arenas blocked"),
        ("VAL2161_06_claim_gates", gate_ok, "relations may pass as math, but no generated row allows a claim"),
        ("VAL2161_07_refusals", refusal_ok, "refusal runner blocks raw c_g, numeric N_X/lambda, one-component PPN and local-GR claims"),
        ("VAL2161_08_decision", decisions_ok, "decision ledger selects 2162 parent action/vector-fill target"),
        ("VAL2161_09_next", next_ok, "2162 next target selected"),
        ("VAL2161_10_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2161_11_csv_parse", csv_ok, "all generated 2161 CSVs parse cleanly"),
        ("VAL2161_12_missing_nonclaim", missing_nonclaim, "all MISSING_* rows remain nonclaim"),
        ("VAL2161_13_no_claim_flags", no_claim_flags, "no generated row has claim_allowed or valid_for_claim true"),
        ("VAL2161_14_direct_claims_blocked", direct_claims_blocked, "Z_X/M_X^2/direct c_g/local claims are explicitly blocked"),
        ("VAL2161_15_formalization_clean", formalization_clean, "formalization-workbench untouched by 2161"),
        ("VAL2161_16_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2161_OVERALL", all_ok, "2161 fails to extract parent N_X/lambda and promotes the PPN vector envelope as the honest next object."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    extraction: list[dict[str, object]],
    hessian: list[dict[str, object]],
    required_clause: list[dict[str, object]],
    ppn_vector: list[dict[str, object]],
    component_status: list[dict[str, object]],
    gates: list[dict[str, object]],
    refusals: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    line_2160, _ = find_line(DOCS["2160"], ["NEXT2160_0_2161"])
    line_1854, _ = find_line(DOCS["1854"], ["EXT1854_5_verdict"])
    line_1855, _ = find_line(DOCS["1855"], ["MXA1855_2_quadratic_block"])
    content = "\n\n".join(
        [
            "# 2161 - Y5/R2FR Parent N_X/Lambda Extraction Or PPN Vector Envelope",
            "## Current Verdict",
            "2161 does **not** extract parent-owned `N_X`, `lambda_X`, `Z_X`, `M_X^2`, a direct `c_g` bound, an R10/PPN pass, local GR/Newton recovery, or any public claim.",
            "It does sharpen the route: the invariant local comparison object is not raw `c_g`; it is the full PPN residual vector with `alpha_cg = tau_g S_PPN(lambda_X,env) c_g/sqrt(Z_X)` as only one component.",
            f"The Cassini scalar proxy remains a source-backed ceiling, `|alpha_PPN_total| <= {CASSINI_ALPHA_PROXY:.15g}`, only after the parent action proves the vector is the actual MTS PPN observable.",
            f"This implements the 2160 handoff at line {line_2160}, respects the 1854 failed Hessian extraction at line {line_1854}, and treats the 1855 X-sector action at line {line_1855} as a closure candidate rather than a derived parent theorem.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## N_X/Lambda Extraction Attempt",
            md_table(extraction, ["extraction_id", "target", "formula_or_requirement", "status", "consequence", "valid_for_claim"]),
            "## Parent Hessian Input Audit",
            md_table(hessian, ["audit_id", "requirement", "current_status", "why_it_matters", "valid_for_claim"]),
            "## Required Parent Action Clause",
            md_table(required_clause, ["clause_id", "required_clause", "closes", "status", "valid_for_claim"]),
            "## PPN Vector Envelope",
            md_table(ppn_vector, ["vector_id", "component", "formula", "status", "issue", "valid_for_claim"]),
            "## Vector Component Status",
            md_table(component_status, ["status_id", "quantity", "required_input", "status", "claim_ready", "valid_for_claim"]),
            "## Claim Gates",
            md_table(gates, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "## Refusal Runner",
            md_table(refusals, ["refusal_id", "attempted_claim", "input_status", "runner_result", "blocked_by", "score_eligible", "claim_allowed", "valid_for_claim"]),
            "## Decision Ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "## Next Target",
            md_table(next_rows, ["route_id", "next_target", "script", "objective", "selection_status", "success_condition", "valid_for_claim"]),
            "## Branch Copies",
            md_table(copies, ["copy_id", "destination", "path_exists", "row_count", "parse_ok", "valid_for_claim"]),
            "## Validation",
            md_table(validation, ["check_id", "status", "detail", "claim_allowed", "valid_for_claim"]),
            "## Working Interpretation",
            "This checkpoint stops the loop. The theory has the right *shape* for a serious local-test comparison, but the coupling sector is still not parent-owned. To move forward, we either derive the minimal X-sector action clause from the MTS primitives, including Hessian, source, boundary and PPN projection terms, or we explicitly score the full residual vector as a nonclaim closure model.",
        ]
    )
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    extraction = nx_lambda_extraction_rows()
    hessian = parent_hessian_audit_rows()
    required_clause = required_parent_action_clause_rows()
    ppn_vector = ppn_vector_rows()
    component_status = vector_component_status_rows()
    gates = claim_gate_rows()
    refusals = refusal_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["extraction"], extraction)
    write_csv(OUTPUTS["hessian_audit"], hessian)
    write_csv(OUTPUTS["required_clause"], required_clause)
    write_csv(OUTPUTS["ppn_vector"], ppn_vector)
    write_csv(OUTPUTS["component_status"], component_status)
    write_csv(OUTPUTS["claim_gate"], gates)
    write_csv(OUTPUTS["refusal"], refusals)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next_target"], next_rows)
    copies = write_branch_copies(extraction, hessian, ppn_vector, component_status, next_rows)
    write_csv(OUTPUTS["branch_copies"], copies)

    remove_pycache()
    csv_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    validation = validation_rows(sources, extraction, hessian, required_clause, ppn_vector, component_status, gates, refusals, decisions, next_rows, copies, csv_paths)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, extraction, hessian, required_clause, ppn_vector, component_status, gates, refusals, decisions, next_rows, copies, validation)
    remove_pycache()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"2161 validation {validation[-1]['status']}")


if __name__ == "__main__":
    main()

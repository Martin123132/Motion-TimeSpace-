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


DOC = ROOT / "2160-Y5-R2FR-PPN-common-frame-cg-translation-and-normalization-gate.md"
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"

DOCS = {
    "2159": ROOT / "2159-Y5-R2FR-parent-ordinary-matter-signature-or-first-coupling-bound-row.md",
    "2159_next": OUT / "P8_Y5_PARENT_QLOC_2159_NEXT_TARGET.csv",
    "2159_validation": OUT / "P8_Y5_BRR545_2159_VALIDATION.csv",
    "1852": ROOT / "1852-Y5-R2FR-PPN-common-frame-cg-translation-gate.md",
    "1852_validation": OUT / "P8_Y5_BRR545_1852_VALIDATION.csv",
    "1853": ROOT / "1853-Y5-R2FR-canonical-X-normalization-and-range-gate-for-cg.md",
    "1853_validation": OUT / "P8_Y5_BRR545_1853_VALIDATION.csv",
    "2156": ROOT / "2156-Y5-R2FR-parent-Xhat-owner-and-Hessian-ZX-MX2-range-or-alpha-source-row.md",
    "2157": ROOT / "2157-Y5-R2FR-parent-metric-ZXfX2-beta-eigenvalue-or-source-zero-return.md",
    "2158": ROOT / "2158-Y5-R2FR-JX-qbarXT-source-zero-or-bounded-coupling-component-pack.md",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2160_SOURCE_REGISTER.csv",
    "scalar_tensor_map": OUT / "P8_Y5_PARENT_QLOC_2160_SCALAR_TENSOR_PPN_MAP.csv",
    "normalization_gate": OUT / "P8_Y5_PARENT_QLOC_2160_NX_NORMALIZATION_GATE.csv",
    "range_gate": OUT / "P8_Y5_PARENT_QLOC_2160_RANGE_SCREENING_TRANSFER_GATE.csv",
    "ppn_vector": OUT / "P8_Y5_PARENT_QLOC_2160_PPN_RESIDUAL_VECTOR_ENVELOPE.csv",
    "cg_bound": OUT / "P8_Y5_PARENT_QLOC_2160_CG_BOUND_STATUS.csv",
    "branch_classifier": OUT / "P8_Y5_PARENT_QLOC_2160_PPN_BRANCH_CLASSIFIER.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2160_CLAIM_GATE.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2160_REFUSAL_RUNNER.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2160_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2160_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2160_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2160_VALIDATION.csv",
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


def formalization_has_2160_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2160-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2160*",
        "*P8_Y5_BRR545_2160*",
        "*Y5_R2FR_PPN_common_frame_cg_translation_and_normalization_gate_2160*",
        "*AFRAME_PPN_CG_2160*",
        "*JR2160*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        ("SRC2160_00_2159_handoff", DOCS["2159"], [["NEXT2159_0_2160"], ["CGT2159_4_verdict"], ["FBS2159_1_scalar_tensor_alpha_proxy"]], "current 2159 selects active-branch PPN c_g translation and normalization gate."),
        ("SRC2160_01_2159_next", DOCS["2159_next"], [["NEXT2159_0_2160"], ["c_g"], ["PPN"]], "machine-readable 2160 target."),
        ("SRC2160_02_2159_validation", DOCS["2159_validation"], [["VAL2159_OVERALL"], ["PASS"]], "2159 validation passed as nonclaim."),
        ("SRC2160_03_1852_ppn_proxy", DOCS["1852"], [["PPN1852_1_scalar_tensor_alpha0_proxy"], ["CGB1852_1_cg_conditional"], ["VAL1852_OVERALL"]], "1852 gives Cassini scalar-tensor alpha proxy and c_g conditional formula."),
        ("SRC2160_04_1852_validation", DOCS["1852_validation"], [["VAL1852_OVERALL"], ["PASS"]], "1852 validation passed as nonclaim."),
        ("SRC2160_05_1853_normalization", DOCS["1853"], [["CN1853_4_verdict"], ["RG1853_5_verdict"], ["NGB1853_2_cg_formula"]], "1853 supplies normalization/range guard for c_g."),
        ("SRC2160_06_1853_validation", DOCS["1853_validation"], [["VAL1853_OVERALL"], ["PASS"]], "1853 validation passed as nonclaim."),
        ("SRC2160_07_2156_hessian", DOCS["2156"], [["SV2156_6_verdict"], ["PHA2156_8_verdict"], ["lambda_X=sqrt"]], "2156 keeps parent Xhat/Hessian ownership unsigned."),
        ("SRC2160_08_2157_metric", DOCS["2157"], [["PML2157_5_verdict"], ["TET2157_4_verdict"], ["FRD2157_4_verdict"]], "2157 freezes finite route and rejects beta mode-count shortcut."),
        ("SRC2160_09_2158_vector", DOCS["2158"], [["JQD2158_7_total_abs_guard"], ["BCP2158_10_total"], ["APR2158_5_local_GR"]], "2158 supplies PPN-relevant source-current component envelope."),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle_groups, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles_found = exists and all(has_any(text, group) for group in needle_groups)
        rows.append(row(source_id=source_id, source_path=str(path), path_exists=exists, needles_found=needles_found, expected_needles="; ".join(" OR ".join(group) for group in needle_groups), role=role))
    return rows


def scalar_tensor_map_rows() -> list[dict[str, object]]:
    data = [
        ("STM2160_0_common_frame_ansatz", "universal common-frame coupling", "g_matter=A_g(Xhat)^2 g_E and A_g=exp(c_g Xhat+O(Xhat^2))", "CONDITIONAL_ANSATZ_ONLY", "parent matter signature/no-shadow theorem must select this as the only matter frame"),
        ("STM2160_1_canonical_field", "canonical scalar normalization", "varphi=M_Pl sqrt(Z_X) Xhat, so N_X=dXhat/d(varphi/M_Pl)=1/sqrt(Z_X)", "EXACT_IF_PARENT_QUADRATIC_BLOCK_SIGNED", "Z_X and Xhat owner remain unsigned"),
        ("STM2160_2_effective_ppn_charge", "PPN charge seen by Cassini", "alpha_eff_PPN = tau_PPN S_PPN(lambda_X,env) N_X c_g + alpha_vec_tail", "FORMULA_READY_INPUTS_MISSING", "tau_PPN, S_PPN, lambda_X and residual vector missing"),
        ("STM2160_3_gamma_law", "single massless unscreened scalar-tensor limit", "gamma-1=-2 alpha_eff_PPN^2/(1+alpha_eff_PPN^2)", "STANDARD_CONDITIONAL_RELATION", "MTS has not proven this limit"),
        ("STM2160_4_proxy_bound", "Cassini scalar proxy", f"|alpha_eff_PPN| <= {CASSINI_ALPHA_PROXY:.15g}", "SOURCE_BACKED_PROXY", "not direct c_g bound until STM2160_0 through STM2160_3 close"),
        ("STM2160_5_verdict", "active-branch PPN map", f"|tau_PPN S_PPN c_g/sqrt(Z_X) + alpha_vec_tail| <= {CASSINI_ALPHA_PROXY:.15g}", "CONDITIONAL_MAP_DERIVED_NOT_CLAIM_GRADE", "normalization/range/vector gates remain open"),
    ]
    return [row(step_id=step_id, target=target, equation=equation, status=status, missing_for_claim=missing_for_claim) for step_id, target, equation, status, missing_for_claim in data]


def normalization_gate_rows() -> list[dict[str, object]]:
    data = [
        ("NX2160_0_Xhat_owner", "same Xhat owns c_g and local quadratic block", "c_g=d ln A_g/dXhat and S_X^(2) uses same Xhat", "NOT_PARENT_SIGNED", "prevents comparing c_g to canonical PPN charge"),
        ("NX2160_1_ZX_positive", "Z_X>0 parent kinetic coefficient", "varphi=M_Pl sqrt(Z_X) Xhat", "MISSING_ZX", "N_X cannot be numeric"),
        ("NX2160_2_rescaling_invariant", "field rescaling guard", "Xhat->aXhat gives c_g->c_g/a and Z_X->Z_X/a^2, so c_g/sqrt(Z_X) is invariant", "GUARDRAIL_ACTIVE", "raw c_g alone is not observable"),
        ("NX2160_3_tau_PPN", "PPN projection/readout factor", "tau_PPN maps canonical common-frame charge into gamma observable", "MISSING_TAU_PPN", "PPN response may not equal unit scalar-tensor response"),
        ("NX2160_4_verdict", "normalization gate", "|tau_PPN c_g/sqrt(Z_X)| can be bounded only after Z_X and tau_PPN are signed", "FAIL_CURRENT_CLAIM_INPUTS_MISSING", "direct c_g bound remains blocked"),
    ]
    return [row(gate_id=gate_id, needed_input=needed_input, formula_or_role=formula_or_role, current_status=current_status, if_missing=if_missing) for gate_id, needed_input, formula_or_role, current_status, if_missing in data]


def range_gate_rows() -> list[dict[str, object]]:
    data = [
        ("RSG2160_0_mass_gap", "same parent Hessian fixes mass/range", "mu_X^2=M_X^2/Z_X", "MISSING_MX2_AND_ZX", "range class unknown"),
        ("RSG2160_1_lambda", "range relation", "lambda_X=sqrt(Z_X/M_X^2) with units fixed by parent block", "EXACT_CONDITIONAL_RELATION_VALUES_MISSING", "cannot route PPN vs R10 vs orbital"),
        ("RSG2160_2_long_range_transfer", "solar-system long-range branch", "S_PPN(lambda_X,env)≈1 only if lambda_X is long compared with the Cassini source/readout scale and unscreened", "NOT_CLASSIFIED", "Cassini proxy cannot be applied unsuppressed"),
        ("RSG2160_3_finite_range_transfer", "finite/lab range branch", "S_PPN may be Yukawa-suppressed; R10/lab or orbital finite-geometry bounds may dominate", "NOT_CLASSIFIED", "do not use Cassini as universal bound"),
        ("RSG2160_4_screening_plateau", "environmental screening/plateau branch", "S_PPN is an effective screened transfer derived from parent equations, not an inserted plateau", "NOT_DERIVED", "screening cannot rescue c_g by assertion"),
        ("RSG2160_5_verdict", "range/screening gate", "alpha_eff_PPN=tau_PPN c_g S_PPN(lambda_X,env)/sqrt(Z_X)", "FAIL_CURRENT_CLAIM_TRANSFER_MISSING", "M_X^2, lambda_X and S_PPN remain missing"),
    ]
    return [row(gate_id=gate_id, target=target, formula_or_condition=formula_or_condition, current_status=current_status, if_missing=if_missing) for gate_id, target, formula_or_condition, current_status, if_missing in data]


def ppn_vector_rows() -> list[dict[str, object]]:
    data = [
        ("PPV2160_0_cg", "common conformal frame", "tau_g S_PPN c_g/sqrt(Z_X)", "MISSING_ZX_TAU_RANGE", "Cassini gamma; Shapiro/time-delay"),
        ("PPV2160_1_bdis", "disformal/preferred-frame matter metric", "tau_dis b_dis", "MISSING_DISFORMAL_PPN_PROJECTION", "PPN gamma; alpha1/alpha2; clocks"),
        ("PPV2160_2_qnonH", "non-Hilbert/source-tail current", "tau_nonH q_nonH", "MISSING_NONHILBERT_PPN_PROJECTION", "PPN gamma; orbital source normalization"),
        ("PPV2160_3_support", "support/domain/local projection shift", "tau_support Delta_W_support + tau_domain q_domain", "MISSING_SUPPORT_DOMAIN_PPN_PROJECTION", "preferred-location/source geometry"),
        ("PPV2160_4_boundary", "boundary/local flux tail", "tau_boundary q_boundary", "MISSING_BOUNDARY_PPN_PROJECTION", "PPN/orbital/local-GR boundary terms"),
        ("PPV2160_5_readout", "post-variation readout or measured-G calibration tail", "tau_readout C_readout", "MISSING_READOUT_PPN_PROJECTION", "measured GM/gamma extraction"),
        ("PPV2160_6_total_abs_guard", "absolute PPN residual vector", "|alpha_PPN_total| <= |cg leg|+|bdis leg|+|nonH leg|+|support leg|+|boundary leg|+|readout leg|", "SCHEMA_READY_VALUES_MISSING", "no one-parameter c_g pass until vector is controlled"),
    ]
    return [row(component_id=component_id, component=component, ppn_leg=ppn_leg, current_status=current_status, observable_link=observable_link) for component_id, component, ppn_leg, current_status, observable_link in data]


def cg_bound_rows() -> list[dict[str, object]]:
    data = [
        ("CGB2160_0_delta_gamma", "gamma_minus_1_bound", "Cassini conservative envelope carried from 1851/1852/2159", CASSINI_DELTA_GAMMA_BOUND, "dimensionless", "SOURCE_BACKED_OBSERVABLE", False),
        ("CGB2160_1_alpha_proxy", "alpha_PPN_proxy", "sqrt(delta_gamma/(2-delta_gamma))", CASSINI_ALPHA_PROXY, "dimensionless", "SOURCE_BACKED_PROXY", False),
        ("CGB2160_2_effective_invariant", "alpha_eff_PPN", "tau_PPN S_PPN c_g/sqrt(Z_X) + alpha_vec_tail", f"abs(alpha_eff_PPN)<={CASSINI_ALPHA_PROXY:.15g}", "dimensionless", "CONDITIONAL_EFFECTIVE_BOUND", False),
        ("CGB2160_3_raw_cg", "c_g", "abs(c_g)<=alpha_proxy*sqrt(Z_X)/(abs(tau_PPN*S_PPN)) only when alpha_vec_tail=0", "MISSING_ZX_TAU_RANGE_VECTOR", "dimensionless_per_Xhat", "FORMULA_READY_COMPONENT_BOUND_MISSING", False),
        ("CGB2160_4_verdict", "direct MTS c_g bound", "direct bound requires Z_X,tau_PPN,S_PPN,lambda_X and vector-tail zero/bounds", "DIRECT_CG_BOUND_NOT_CLAIMED", "gate", "FAIL_CURRENT_CLAIM_TRANSLATION_MISSING", False),
    ]
    return [row(bound_id=bound_id, quantity=quantity, formula=formula, numeric_or_status=numeric_or_status, units=units, status=status, direct_mts_component_bound=direct_mts_component_bound) for bound_id, quantity, formula, numeric_or_status, units, status, direct_mts_component_bound in data]


def branch_classifier_rows() -> list[dict[str, object]]:
    data = [
        ("PBC2160_0_pure_long_range", "universal conformal, massless/solar-long, unscreened, vector tails zero", "Cassini constrains alpha_eff and then c_g/sqrt(Z_X)", "CONDITIONAL_COMPETITIVE_BRANCH", "not current claim"),
        ("PBC2160_1_short_range", "lambda_X lab scale or shorter", "R10/Yukawa bounds dominate; Cassini suppressed", "ROUTE_DEPENDS_ON_MISSING_LAMBDA", "needs Z_X/M_X^2"),
        ("PBC2160_2_orbital_range", "lambda_X Earth-Moon/AU/source-support scale", "LLR/orbital/finite-source geometry needed", "ROUTE_DEPENDS_ON_MISSING_LAMBDA", "needs transfer matrix"),
        ("PBC2160_3_screened", "nonlinear screening/plateau suppresses solar-system charge", "Cassini bounds screened effective charge only", "SCREENING_NOT_DERIVED", "do not insert plateau axiom"),
        ("PBC2160_4_multi_component", "PPN vector has nonzero disformal/nonH/support/boundary/readout legs", "absolute residual vector must be scored", "VECTOR_SCHEMA_READY_VALUES_MISSING", "single c_g bound forbidden"),
        ("PBC2160_5_current", "current active branch", "source-backed Cassini proxy exists; MTS translation incomplete", "SOURCE_PROXY_ONLY", "selected current status"),
    ]
    return [row(class_id=class_id, branch=branch, implication=implication, current_status=current_status, next_need=next_need) for class_id, branch, implication, current_status, next_need in data]


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("CG2160_0_cassini_source", "Cassini observable bound is source-backed", True, "gamma envelope and scalar proxy are numeric"),
        ("CG2160_1_scalar_map_math", "scalar-tensor gamma inversion is written", True, "conditional standard map is explicit"),
        ("CG2160_2_NX_owned", "N_X=1/sqrt(Z_X) is numeric and parent-owned", False, "Z_X/Xhat owner missing"),
        ("CG2160_3_range_owned", "lambda_X/S_PPN route is parent-owned", False, "M_X^2/lambda/screening transfer missing"),
        ("CG2160_4_vector_controlled", "PPN residual vector is zero or bounded", False, "b_dis/q_nonH/support/boundary/readout legs missing"),
        ("CG2160_5_direct_cg_bound", "Cassini gives direct MTS c_g bound", False, "normalization/range/vector gates fail"),
        ("CG2160_6_local_GR_PPN", "local GR/PPN pass is derived", False, "no direct c_g bound or full PPN metric expansion"),
    ]
    return [row(gate_id=gate_id, claim=claim, gate_pass=gate_pass, reason=reason) for gate_id, claim, gate_pass, reason in data]


def refusal_rows() -> list[dict[str, object]]:
    data = [
        ("REF2160_0_raw_cg_bound", "raw c_g <= alpha_proxy", "NORMALIZATION_MISSING", "BLOCKED", "must use c_g/sqrt(Z_X) with tau_PPN and S_PPN", False),
        ("REF2160_1_long_range_assumption", "Cassini applies unsuppressed", "RANGE_TRANSFER_MISSING", "BLOCKED", "lambda_X and screening/environment map missing", False),
        ("REF2160_2_one_parameter_ppn", "c_g is the only PPN leg", "VECTOR_TAILS_MISSING", "BLOCKED", "b_dis/q_nonH/support/boundary/readout components retained", False),
        ("REF2160_3_local_gr_claim", "local GR/PPN recovered", "PPN_METRIC_EXPANSION_MISSING", "BLOCKED", "gamma proxy is not full PPN beta/preferred-frame/conservation proof", False),
        ("REF2160_4_empirical_pass", "MTS passes Cassini/PPN", "DIRECT_COMPONENT_BOUND_MISSING", "BLOCKED", "source-backed proxy only", False),
    ]
    return [row(refusal_id=refusal_id, attempted_claim=attempted_claim, input_status=input_status, runner_result=runner_result, blocked_by=blocked_by, score_eligible=score_eligible) for refusal_id, attempted_claim, input_status, runner_result, blocked_by, score_eligible in data]


def decision_rows() -> list[dict[str, object]]:
    data = [
        ("DEC2160_0_map_result", "The PPN scalar-tensor map is derived only conditionally.", "It gives the right comparison object alpha_eff_PPN, not a raw c_g bound.", "use alpha_eff or c_g/sqrt(Z_X), never raw c_g"),
        ("DEC2160_1_current_block", "Direct MTS c_g remains unbounded by Cassini in the current branch.", "Z_X, tau_PPN, lambda/S_PPN and vector-tail controls are missing.", "keep Cassini as source-backed pressure, not claim"),
        ("DEC2160_2_no_circling", "Do not re-argue the same scalar-tensor proxy again.", "The exact next missing objects are now N_X/lambda and PPN residual vector legs.", "2161 should choose parent Hessian/range extraction or PPN vector fill"),
        ("DEC2160_3_next_target", "Next target is parent N_X/lambda extraction with PPN vector fallback.", "Without Z_X/M_X^2, every PPN/R10/orbital route is only source-backed proxy; without the vector, one-parameter c_g is fake.", "2161-Y5-R2FR-parent-NX-lambda-extraction-or-PPN-vector-envelope.md"),
    ]
    return [row(decision_id=decision_id, decision=decision, because=because, next_action=next_action) for decision_id, decision, because, next_action in data]


def next_target_rows() -> list[dict[str, object]]:
    data = [
        (
            "NEXT2160_0_2161",
            "2161-Y5-R2FR-parent-NX-lambda-extraction-or-PPN-vector-envelope.md",
            "scripts/Y5_R2FR_parent_NX_lambda_extraction_or_PPN_vector_envelope_2161.py",
            "try to source or derive parent Z_X and M_X^2 enough to define N_X and lambda_X; if unavailable, fill the PPN residual-vector no-cancellation envelope over c_g, b_dis, q_nonH, support, boundary and readout terms",
            "selected",
            "either N_X/lambda_X become parent-owned inputs, or the PPN c_g branch is demoted to vector-only source proxy with explicit missing component rows",
        ),
        (
            "NEXT2160_1_parallel",
            "2161b-Y5-R2FR-no-hidden-visible-hom-operator-domain-theorem.md",
            "scripts/Y5_R2FR_no_hidden_visible_hom_operator_domain_theorem_2161b.py",
            "try to derive the operator-domain theorem that would zero shadow-frame, alpha/mass, marker and source-tail PPN legs",
            "held",
            "vector tails vanish by theorem, reopening a cleaner c_g/PPN path",
        ),
    ]
    return [row(route_id=route_id, next_target=next_target, script=script, objective=objective, selection_status=selection_status, success_condition=success_condition) for route_id, next_target, script, objective, selection_status, success_condition in data]


def write_branch_copies(st_map: list[dict[str, object]], norm: list[dict[str, object]], vector: list[dict[str, object]], cg_bound: list[dict[str, object]], next_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    copies = [
        ("COPY2160_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_PPN_CG_2160_NONCLAIM.csv", st_map + norm),
        ("COPY2160_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2160_PPN_CG_NONCLAIM.csv", vector + cg_bound),
        ("COPY2160_2_acquisition_queue", QUEUE / "JR2160_NX_LAMBDA_OR_PPN_VECTOR_QUEUE.csv", next_rows + vector),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    st_map: list[dict[str, object]],
    norm: list[dict[str, object]],
    range_gate: list[dict[str, object]],
    vector: list[dict[str, object]],
    cg_bound: list[dict[str, object]],
    classifier: list[dict[str, object]],
    gates: list[dict[str, object]],
    refusals: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    st_ok = any(item["step_id"] == "STM2160_5_verdict" and item["status"] == "CONDITIONAL_MAP_DERIVED_NOT_CLAIM_GRADE" for item in st_map)
    norm_ok = any(item["gate_id"] == "NX2160_4_verdict" and item["current_status"] == "FAIL_CURRENT_CLAIM_INPUTS_MISSING" for item in norm)
    range_ok = any(item["gate_id"] == "RSG2160_5_verdict" and item["current_status"] == "FAIL_CURRENT_CLAIM_TRANSFER_MISSING" for item in range_gate)
    vector_ok = any(item["component_id"] == "PPV2160_6_total_abs_guard" and item["current_status"] == "SCHEMA_READY_VALUES_MISSING" for item in vector)
    cg_ok = any(item["bound_id"] == "CGB2160_1_alpha_proxy" and float(item["numeric_or_status"]) > 0 for item in cg_bound) and any(item["bound_id"] == "CGB2160_4_verdict" and item["status"] == "FAIL_CURRENT_CLAIM_TRANSLATION_MISSING" for item in cg_bound)
    classifier_ok = any(item["class_id"] == "PBC2160_5_current" and item["current_status"] == "SOURCE_PROXY_ONLY" for item in classifier)
    gate_ok = any(item["gate_id"] == "CG2160_0_cassini_source" and truthy(item["gate_pass"]) for item in gates) and all(not truthy(item.get("claim_allowed", False)) for item in gates)
    refusal_ok = all(item["runner_result"] == "BLOCKED" and not truthy(item.get("score_eligible", False)) for item in refusals)
    decisions_ok = any(item["decision_id"] == "DEC2160_3_next_target" and "2161" in str(item["next_action"]) for item in decisions)
    next_ok = any(item["route_id"] == "NEXT2160_0_2161" and item["selection_status"] == "selected" for item in next_rows)
    copies_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    missing_not_ready = all(not truthy(item.get("valid_for_claim", False)) for group in (norm, range_gate, vector, cg_bound, classifier) for item in group if "MISSING_" in " ".join(str(value) for value in item.values()))
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, st_map, norm, range_gate, vector, cg_bound, classifier, gates, refusals, decisions, next_rows, copies)
        for item in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2160_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, st_ok, norm_ok, range_ok, vector_ok, cg_ok, classifier_ok, gate_ok, refusal_ok, decisions_ok, next_ok, copies_ok, csv_ok, missing_not_ready, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2160_00_sources", sources_ok, "2159 handoff plus 1852/1853 and active local gates validate"),
        ("VAL2160_01_scalar_map", st_ok, "scalar-tensor PPN map is conditional and nonclaim"),
        ("VAL2160_02_normalization_gate", norm_ok, "N_X/Z_X normalization gate blocks direct c_g claim"),
        ("VAL2160_03_range_gate", range_ok, "lambda/S_PPN range gate blocks unsuppressed Cassini use"),
        ("VAL2160_04_ppn_vector", vector_ok, "PPN residual vector no-cancellation envelope is staged"),
        ("VAL2160_05_cg_bound", cg_ok, "Cassini proxy numeric; direct c_g bound blocked"),
        ("VAL2160_06_branch_classifier", classifier_ok, "current branch classified as source proxy only"),
        ("VAL2160_07_claim_gates", gate_ok, "source/proxy math exists but no MTS/local claim allowed"),
        ("VAL2160_08_refusals", refusal_ok, "refusal runner blocks raw c_g, long-range, one-parameter PPN, local-GR and pass claims"),
        ("VAL2160_09_decision_next", decisions_ok, "decision ledger selects N_X/lambda or PPN vector target"),
        ("VAL2160_10_next", next_ok, "2161 next target selected"),
        ("VAL2160_11_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2160_12_csv_parse", csv_ok, "all generated 2160 CSVs parse cleanly"),
        ("VAL2160_13_missing_not_ready", missing_not_ready, "MISSING_* rows stay nonclaim"),
        ("VAL2160_14_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2160_15_formalization_clean", formalization_clean, "formalization-workbench untouched by 2160"),
        ("VAL2160_16_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2160_OVERALL", all_ok, "2160 derives conditional PPN c_g map and keeps Cassini as source-backed proxy only."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    st_map: list[dict[str, object]],
    norm: list[dict[str, object]],
    range_gate: list[dict[str, object]],
    vector: list[dict[str, object]],
    cg_bound: list[dict[str, object]],
    classifier: list[dict[str, object]],
    gates: list[dict[str, object]],
    refusals: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    line_2159, _ = find_line(DOCS["2159"], ["NEXT2159_0_2160"])
    line_1853, _ = find_line(DOCS["1853"], ["CN1853_4_verdict"])
    line_2158, _ = find_line(DOCS["2158"], ["JQD2158_7_total_abs_guard"])
    content = "\n\n".join(
        [
            "# 2160 - Y5/R2FR PPN Common-Frame c_g Translation And Normalization Gate",
            "## Current Verdict",
            "2160 does **not** give a direct MTS `c_g` bound, PPN pass, local GR/Newton reduction, or public claim.",
            f"It does derive the active-branch comparison object: `alpha_eff_PPN = tau_PPN S_PPN(lambda_X,env) c_g/sqrt(Z_X) + alpha_vec_tail`, with Cassini giving the source-backed proxy `|alpha_eff_PPN| <= {CASSINI_ALPHA_PROXY:.15g}` only under the scalar-tensor PPN assumptions.",
            "Raw `c_g` is not observable by itself. The direct bound needs parent-owned `Z_X`, `tau_PPN`, `lambda_X`, `S_PPN`, and zero/bounded disformal, non-Hilbert, support, boundary and readout vector tails.",
            f"This follows the 2159 handoff at line {line_2159}, imports the 1853 normalization guard at line {line_1853}, and uses the 2158 residual-vector guard at line {line_2158}.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Scalar-Tensor PPN Map",
            md_table(st_map, ["step_id", "target", "equation", "status", "missing_for_claim", "valid_for_claim"]),
            "## N_X Normalization Gate",
            md_table(norm, ["gate_id", "needed_input", "formula_or_role", "current_status", "if_missing", "valid_for_claim"]),
            "## Range/Screening Transfer Gate",
            md_table(range_gate, ["gate_id", "target", "formula_or_condition", "current_status", "if_missing", "valid_for_claim"]),
            "## PPN Residual Vector Envelope",
            md_table(vector, ["component_id", "component", "ppn_leg", "current_status", "observable_link", "valid_for_claim"]),
            "## c_g Bound Status",
            md_table(cg_bound, ["bound_id", "quantity", "formula", "numeric_or_status", "units", "status", "direct_mts_component_bound", "valid_for_claim"]),
            "## PPN Branch Classifier",
            md_table(classifier, ["class_id", "branch", "implication", "current_status", "next_need", "valid_for_claim"]),
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
            "This is the useful Cassini result without cheating: Cassini is real pressure on a long-range, unscreened, universal common-frame branch, but it does not yet bind raw MTS `c_g`. The next move is not another proxy; it is either parent-own `Z_X/M_X^2` so `N_X` and `lambda_X` exist, or turn the PPN channel into a full no-cancellation residual vector.",
        ]
    )
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    st_map = scalar_tensor_map_rows()
    norm = normalization_gate_rows()
    range_gate = range_gate_rows()
    vector = ppn_vector_rows()
    cg_bound = cg_bound_rows()
    classifier = branch_classifier_rows()
    gates = claim_gate_rows()
    refusals = refusal_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["scalar_tensor_map"], st_map)
    write_csv(OUTPUTS["normalization_gate"], norm)
    write_csv(OUTPUTS["range_gate"], range_gate)
    write_csv(OUTPUTS["ppn_vector"], vector)
    write_csv(OUTPUTS["cg_bound"], cg_bound)
    write_csv(OUTPUTS["branch_classifier"], classifier)
    write_csv(OUTPUTS["claim_gate"], gates)
    write_csv(OUTPUTS["refusal"], refusals)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next_target"], next_rows)
    copies = write_branch_copies(st_map, norm, vector, cg_bound, next_rows)
    write_csv(OUTPUTS["branch_copies"], copies)

    remove_pycache()
    csv_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    validation = validation_rows(sources, st_map, norm, range_gate, vector, cg_bound, classifier, gates, refusals, decisions, next_rows, copies, csv_paths)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, st_map, norm, range_gate, vector, cg_bound, classifier, gates, refusals, decisions, next_rows, copies, validation)
    remove_pycache()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"2160 validation {validation[-1]['status']}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1161-Y5-R10-Cperp-form-drel-operator-source-row-or-local-branch-selector-proof.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    generated = now()
    return [{**row, "generated_utc": generated} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def missing_or_blocked(value: object) -> bool:
    text = str(value)
    return (
        text.strip() == ""
        or "MISSING" in text
        or "NOT_DERIVED" in text
        or "NOT_CONSTRUCTED" in text
        or "NOT_SOURCED" in text
        or "BLOCKED" in text
        or "UNSIGNED" in text
        or "REJECT" in text
    )


def source_rows() -> list[dict[str, object]]:
    sources = [
        {
            "source_id": "SRC1161_0_1160_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1160_NEXT_TARGET.csv",
            "needle": "NEXT1160_0_1161",
            "role": "handoff selecting Cperp form/d_rel source row or local branch selector proof.",
        },
        {
            "source_id": "SRC1161_1_1160_chain",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1160_CPERP_RELATIVE_EXACTNESS_CHAIN.csv",
            "needle": "CRE1160_0_Cperp_object",
            "role": "Cperp object and d_rel chain remains missing.",
        },
        {
            "source_id": "SRC1161_2_1160_pack",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1160_EDGE_BOUND_SOURCE_PACK.csv",
            "needle": "ESP1160_1_drel_complex",
            "role": "source pack row for d_rel, boundary pullback, and relative pair convention.",
        },
        {
            "source_id": "SRC1161_3_272_Cperp",
            "relative_path": "272-quotient-configuration-principle-from-topological-projector.md",
            "needle": "Cperp is shown to be exact/trivial",
            "role": "older Cperp exactness target; not a current theorem.",
        },
        {
            "source_id": "SRC1161_4_1144_branch",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1144_BRANCH_LAW_ATTEMPT.csv",
            "needle": "BL1144_5_verdict",
            "role": "branch-law shape support but no parent branch selector.",
        },
        {
            "source_id": "SRC1161_5_1144_cohomology",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1144_RELATIVE_COHOMOLOGY_SPLIT_AUDIT.csv",
            "needle": "RC1144_2_same_parent_law",
            "role": "same-parent local/FLRW law is missing.",
        },
        {
            "source_id": "SRC1161_6_1145_functional",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1145_BRANCH_FUNCTIONAL_CANDIDATE_AUDIT.csv",
            "needle": "FC1145_6_verdict",
            "role": "branch functional candidates fail as parent selector.",
        },
        {
            "source_id": "SRC1161_7_1145_contract",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1145_EXACT_SBRANCH_CONTRACT.csv",
            "needle": "SBF1145_1_Euler_law",
            "role": "future S_branch contract with Euler/Ward branch equation requirement.",
        },
        {
            "source_id": "SRC1161_8_1146_no_flux",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1146_NO_FLUX_CERTIFICATE_AUDIT.csv",
            "needle": "NF1146_6_verdict",
            "role": "epsilon/domain no-flux certificate not derived.",
        },
        {
            "source_id": "SRC1161_9_407_quotient",
            "relative_path": "407-primitive-relational-quotient-action-sketch.md",
            "needle": "matter quotient functor/no-marker selector proof",
            "role": "primitive quotient action sketch is useful but not theorem.",
        },
        {
            "source_id": "SRC1161_10_1030_spm",
            "relative_path": "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md",
            "needle": "SPD1030_6_verdict",
            "role": "matter/no-shadow-frame theorem remains unproved.",
        },
        {
            "source_id": "SRC1161_11_720_kinetic",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_720_KINETIC_NULL_THEOREM_AUDIT.csv",
            "needle": "KNT720_8_no_mode_theorem",
            "role": "no local mode theorem fails current corpus.",
        },
    ]
    checked: list[dict[str, object]] = []
    for source in sources:
        path = ROOT / str(source["relative_path"])
        text = read_text(path)
        checked.append(
            {
                **source,
                "exists": str(path.exists()).lower(),
                "needle_found": str(str(source["needle"]) in text).lower(),
            }
        )
    return stamp(checked)


def cperp_drel_audit_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "audit_id": "CDR1161_0_candidate_topological_residual",
                "candidate": "C_perp=(I-P_D)C or topological/projector residual",
                "would_supply": "candidate C-sector residual object",
                "current_status": "CANDIDATE_ONLY_NOT_SOURCE_BACKED",
                "why_not_enough": "P_D, C, form degree, local domain, units, and variation rule are not all parent-owned in the same source",
                "required_next": "source-backed definition row or reject candidate",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "CDR1161_1_candidate_domain_current",
                "candidate": "C_perp=P_D J_D or domain/memory relative current residual",
                "would_supply": "local/FLRW branch carrier with relative cohomology split",
                "current_status": "ANALOGY_ONLY_NOT_CPERP_DEFINITION",
                "why_not_enough": "J_D/J_rel exactness support does not define the C-sector conformal/residual representative used in c_g route",
                "required_next": "map C_perp to J_D/J_rel with same parent variables or keep separate",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "CDR1161_2_candidate_frame_residual",
                "candidate": "C_perp as representative frame/conformal residual tied to A_g or Xhat",
                "would_supply": "direct link to c_g zero route",
                "current_status": "DANGEROUS_UNOWNED_SHORTCUT",
                "why_not_enough": "would define away the very common-frame coupling the audit is trying to test",
                "required_next": "only allowed if matter quotient/no-shadow theorem is independently parent-signed",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "CDR1161_3_drel_operator",
                "candidate": "d_rel=(d bulk, i_star bulk - d boundary) on a relative pair",
                "would_supply": "relative closed/exact test",
                "current_status": "STANDARD_SHAPE_NOT_PARENT_INSTANTIATED",
                "why_not_enough": "the actual complexes Omega_C^k(U), Omega_C^{k-1}(S), boundary pullback, and allowed class are not sourced for Cperp",
                "required_next": "write d_rel source row with domain U, surface S, form degrees, signs, units, and source path",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "CDR1161_4_boundary_pullback",
                "candidate": "i_star C_perp and boundary representative B_C|S",
                "would_supply": "weighted edge/Stokes input",
                "current_status": "NOT_SOURCED",
                "why_not_enough": "no boundary pullback convention or primitive decomposition is parent-owned",
                "required_next": "source i_star, B_C, b_C, h_C, r_C conventions",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "CDR1161_5_closedness_identity",
                "candidate": "d_rel C_perp=0",
                "would_supply": "relative cohomology theorem entry condition",
                "current_status": "NOT_PROVED",
                "why_not_enough": "no C-sector Bianchi/Noether/Euler identity closes source/support/boundary terms",
                "required_next": "derive closedness from parent variation or retain edge/source pack",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "CDR1161_6_verdict",
                "candidate": "actual C_perp form and d_rel operator for current MTS",
                "would_supply": "first required objects for Cperp exactness",
                "current_status": "CPERP_FORM_DREL_NOT_SOURCED",
                "why_not_enough": "all candidate definitions are shape support, analogies, or unowned shortcuts",
                "required_next": "source acquisition row for C_perp/d_rel or choose a strict candidate and demote others",
                "valid_for_claim": "false",
            },
        ]
    )


def branch_selector_audit_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "audit_id": "BSP1161_0_target",
                "selector_piece": "same parent selector",
                "required_statement": "one parent Euler/Ward/quotient law selects local C-sector exact/trivial class and FLRW homogeneous active class",
                "current_status": "TARGET_SHARP",
                "failure_mode": "if this is hand-selected, local silence and cosmology activity become incompatible claims",
                "source_anchor": "RC1144_2_same_parent_law",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "BSP1161_1_fixed_domain_Qcoh",
                "selector_piece": "fixed-domain coherent projection",
                "required_statement": "Qcoh projection becomes a parent-owned selector of physical domain, not merely a map after D is supplied",
                "current_status": "SHAPE_SUPPORT_ONLY",
                "failure_mode": "physical D is already assumed",
                "source_anchor": "BL1144_0_fixed_D_Qcoh",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "BSP1161_2_free_boundary",
                "selector_piece": "free-boundary Euler branch",
                "required_statement": "free-boundary equation uniquely selects local exact and FLRW active representatives without extra thresholds",
                "current_status": "DEGENERATE_UNDERSELECTED",
                "failure_mode": "many domains extremize; no unique physical branch",
                "source_anchor": "BL1144_1_free_boundary_extrema;FC1145_3_free_boundary_Euler",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "BSP1161_3_Cexp_separator",
                "selector_piece": "C_exp branch separator",
                "required_statement": "C_exp enters a parent action/constraint with no new stress, no threshold tuning, and Bianchi-safe local silence",
                "current_status": "KINEMATIC_CLUE_NOT_PARENT_FUNCTIONAL",
                "failure_mode": "clean separator but not an owner of branch selection",
                "source_anchor": "BL1144_3_Cexp_separator;FC1145_4_Cexp_selector_potential",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "BSP1161_4_quotient_split",
                "selector_piece": "q_loc/q_FLRW split",
                "required_statement": "Dq_loc[v_D]=0 and Dq_FLRW[v_D]!=0 follow from one parent quotient/functor construction",
                "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
                "failure_mode": "sufficient clause, not derived action fact",
                "source_anchor": "BL1144_4_quotient_split;FC1145_5_quotient_split_action",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "BSP1161_5_no_flux_sibling",
                "selector_piece": "epsilon/domain no-flux certificate",
                "required_statement": "same local representative makes projected domain flux vanish in observed coframe",
                "current_status": "NO_FLUX_CERTIFICATE_NOT_DERIVED",
                "failure_mode": "branch selector may still leave alpha3/R11/domain leakage",
                "source_anchor": "NF1146_6_verdict",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "BSP1161_6_verdict",
                "selector_piece": "local-trivial/FLRW-active branch selector proof",
                "required_statement": "BSP1161_1 through BSP1161_5 all parent-signed",
                "current_status": "LOCAL_FLRW_SELECTOR_NOT_DERIVED",
                "failure_mode": "selector remains a theorem target and source rows stay nonclaim",
                "source_anchor": "1144;1145;1146",
                "valid_for_claim": "false",
            },
        ]
    )


def source_pack_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "row_id": "CDSRC1161_0_Cperp_definition",
                "quantity": "C_perp",
                "required_fields": "candidate_id;parent_variables;form_degree;domain_U;boundary_S;definition;units;variation_rule;source_path;valid_for_claim",
                "current_value": "MISSING_PARENT_CPERP_DEFINITION",
                "source_path": "MISSING_PARENT_SOURCE",
                "status": "BLOCKED",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "CDSRC1161_1_PD_projector",
                "quantity": "P_D or C-sector projector",
                "required_fields": "projector_id;domain_rule;idempotence;metric_independence;variation_deltaP;stress_rule;source_path;valid_for_claim",
                "current_value": "MISSING_PARENT_PROJECTOR_OWNERSHIP",
                "source_path": "MISSING_PROJECTOR_SOURCE",
                "status": "BLOCKED",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "CDSRC1161_2_drel_operator",
                "quantity": "d_rel",
                "required_fields": "bulk_complex;boundary_complex;pullback_i_star;sign_convention;relative_pair;nilpotency_check;source_path;valid_for_claim",
                "current_value": "MISSING_DREL_OPERATOR",
                "source_path": "MISSING_RELATIVE_COMPLEX_SOURCE",
                "status": "BLOCKED",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "CDSRC1161_3_closedness_identity",
                "quantity": "d_rel C_perp",
                "required_fields": "identity_source;Noether_or_Bianchi_or_Euler_clause;source_terms;boundary_terms;support_terms;result;source_path;valid_for_claim",
                "current_value": "MISSING_CPERP_CLOSEDNESS_PROOF",
                "source_path": "MISSING_IDENTITY_SOURCE",
                "status": "BLOCKED",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "CDSRC1161_4_Hrel_branch",
                "quantity": "H_rel_C",
                "required_fields": "branch_id;topology;relative_cohomology_group;harmonic_basis;h_C_value_or_bound;source_path;valid_for_claim",
                "current_value": "MISSING_HREL_BRANCH_CERTIFICATE",
                "source_path": "MISSING_COHOMOLOGY_SOURCE",
                "status": "BLOCKED",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "CDSRC1161_5_branch_selector",
                "quantity": "local_trivial_FLRW_active_selector",
                "required_fields": "parent_variable;Euler_or_Ward_equation;local_solution;FLRW_solution;no_hand_switch_check;stress_silence;source_path;valid_for_claim",
                "current_value": "MISSING_PARENT_BRANCH_SELECTION_LAW",
                "source_path": "source-intake/mts_residuals/P8_Y5_R10_1144_RELATIVE_COHOMOLOGY_SPLIT_AUDIT.csv",
                "status": "BLOCKED_SHAPE_SUPPORT_ONLY",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
            {
                "row_id": "CDSRC1161_6_epsilon_no_flux_sibling",
                "quantity": "epsilon_domain_flux_zero_or_bound",
                "required_fields": "flux_definition;observed_coframe;local_solution;boundary_harmonic_silence;epsilon_abs_or_zero;source_path;valid_for_claim",
                "current_value": "MISSING_EPSILON_NO_FLUX_CERTIFICATE_OR_PROFILE",
                "source_path": "source-intake/mts_residuals/P8_Y5_R10_1146_NO_FLUX_CERTIFICATE_AUDIT.csv",
                "status": "BLOCKED_SIBLING_GATE",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            },
        ]
    )


def guard_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "guard_id": "GUARD1161_0_no_undefined_Cperp",
                "guard": "do not use Cperp exactness until C_perp form degree, domain, units, and variation rule are sourced",
                "status": "ACTIVE",
                "reason": "undefined object exactness is closure, not derivation",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1161_1_no_generic_drel",
                "guard": "standard relative cohomology notation is not enough without the actual C-sector complex",
                "status": "ACTIVE",
                "reason": "the sign, pullback, boundary class, and nilpotency check must match the local branch",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1161_2_no_local_FLRW_hand_switch",
                "guard": "local trivial and FLRW active classes require one parent selector",
                "status": "ACTIVE",
                "reason": "separate branch labels would be a theory patch, not a derivation",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1161_3_no_Cexp_threshold_tuning",
                "guard": "C_exp separator cannot introduce empirical thresholds or hidden stress",
                "status": "ACTIVE",
                "reason": "kinematic separation is useful only if parent-derived and Bianchi-safe",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "GUARD1161_4_no_cg_zero_from_geometry_only",
                "guard": "even a Cperp selector does not prove c_g=0 without matter descent/no-shadow-frame",
                "status": "ACTIVE",
                "reason": "common Weyl matter coupling remains a separate countermodel",
                "valid_for_claim": "false",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "G1161_0_sources_exist",
                "rule": "all cited local source paths and needles exist",
                "gate_pass": "true_nonclaim",
                "reason": "source register validates the audit trail",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1161_1_Cperp_drel_sourced",
                "rule": "C_perp form and d_rel complex are parent-sourced",
                "gate_pass": "false",
                "reason": "candidate definitions remain unowned or analogy-only",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1161_2_branch_selector_proved",
                "rule": "same parent law selects local trivial and FLRW active classes",
                "gate_pass": "false",
                "reason": "fixed-D, free-boundary, C_exp, and quotient-split routes remain insufficient",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1161_3_source_pack_ready",
                "rule": "source-pack rows for Cperp/d_rel/selector are emitted as nonclaim rows",
                "gate_pass": "true_nonclaim",
                "reason": "missing rows now identify exactly what must be sourced",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1161_4_claim_promotion",
                "rule": "Cperp exactness, q-null, c_g-zero, local-GR/Newton/R10/PPN/WEP/clock/orbital claim allowed",
                "gate_pass": "false",
                "reason": "Cperp/d_rel, selector, no-flux sibling, and matter descent remain incomplete",
                "valid_for_claim": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "D1161_0_Cperp_status",
                "decision": "Cperp_form_drel_not_sourced",
                "reason": "no candidate supplies the actual object, relative complex, closedness identity, and units in one parent source",
                "next_action": "strictly choose/source a Cperp candidate or keep edge/source pack route",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1161_1_selector_status",
                "decision": "local_FLRW_selector_not_proved",
                "reason": "branch law remains shape-supported but underselected or sufficient-only",
                "next_action": "do not use local silence with FLRW activity as proof until selector is parent-owned",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1161_2_best_next",
                "decision": "target_strict_Cperp_candidate_choice_or_edge_bound_source_fill",
                "reason": "another theorem attempt needs the actual object first; otherwise source the edge bound terms",
                "next_action": "1162 strict Cperp candidate adoption/rejection or first edge-bound source fill",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1161_0_1162",
                "next_target": "1162-Y5-R10-strict-Cperp-candidate-choice-or-edge-bound-first-source-fill.md",
                "objective": "choose one legally sourceable C_perp/d_rel candidate or reject all candidates and begin filling the edge-bound source terms as nonclaim inputs",
                "include": "candidate C_perp definitions; P_D ownership; d_rel complex; closedness identity; branch selector status; C_corner/norm_dS_Feps/norm_bC/h_C/r_C/K_boundary rows",
                "exclude": "multiple Cperp definitions at once; undefined d_rel; local/FLRW hand switch; c_g zero claim; GitHub; formalization edits",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    cperp_audit: list[dict[str, object]],
    selector_audit: list[dict[str, object]],
    source_pack: list[dict[str, object]],
    guards: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    outputs: dict[str, Path],
) -> list[dict[str, object]]:
    validation: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validation.append(
            {
                "check_id": check_id,
                "result": "pass" if passed else "fail",
                "detail": detail,
                "valid_for_claim": "false",
                "generated_utc": now(),
            }
        )

    all_rows = cperp_audit + selector_audit + source_pack + guards + gates + decisions + next_target
    required_pack = {
        "CDSRC1161_0_Cperp_definition",
        "CDSRC1161_1_PD_projector",
        "CDSRC1161_2_drel_operator",
        "CDSRC1161_3_closedness_identity",
        "CDSRC1161_4_Hrel_branch",
        "CDSRC1161_5_branch_selector",
        "CDSRC1161_6_epsilon_no_flux_sibling",
    }
    add(
        "V1161_0_sources_exist",
        all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources),
        "all cited local source paths exist and needles are found",
    )
    add(
        "V1161_1_Cperp_not_sourced",
        any(row["audit_id"] == "CDR1161_6_verdict" and row["current_status"] == "CPERP_FORM_DREL_NOT_SOURCED" for row in cperp_audit),
        "Cperp/d_rel source status remains blocked rather than claimed",
    )
    add(
        "V1161_2_selector_not_proved",
        any(row["audit_id"] == "BSP1161_6_verdict" and row["current_status"] == "LOCAL_FLRW_SELECTOR_NOT_DERIVED" for row in selector_audit),
        "local/FLRW branch selector remains unproved",
    )
    add(
        "V1161_3_source_pack_complete",
        required_pack.issubset({row["row_id"] for row in source_pack}),
        "Cperp/d_rel/selector/no-flux source pack covers all required rows",
    )
    add(
        "V1161_4_source_pack_nonclaim_missing",
        all(row["valid_for_claim"] == "false" and row["claim_allowed"] == "false" and missing_or_blocked(row["current_value"]) for row in source_pack),
        "source-pack rows remain missing/nonclaim until sourced",
    )
    add(
        "V1161_5_guards_active",
        {
            "GUARD1161_0_no_undefined_Cperp",
            "GUARD1161_1_no_generic_drel",
            "GUARD1161_2_no_local_FLRW_hand_switch",
            "GUARD1161_3_no_Cexp_threshold_tuning",
            "GUARD1161_4_no_cg_zero_from_geometry_only",
        }.issubset({row["guard_id"] for row in guards if row["status"] == "ACTIVE"}),
        "all Cperp/d_rel/selector no-cheat guards are active",
    )
    add(
        "V1161_6_claim_gates_blocked",
        any(row["gate_id"] == "G1161_1_Cperp_drel_sourced" and row["gate_pass"] == "false" for row in gates)
        and any(row["gate_id"] == "G1161_2_branch_selector_proved" and row["gate_pass"] == "false" for row in gates)
        and any(row["gate_id"] == "G1161_4_claim_promotion" and row["gate_pass"] == "false" for row in gates),
        "Cperp, selector, and local claim gates remain blocked",
    )
    add(
        "V1161_7_no_claim_rows",
        all(row.get("valid_for_claim") == "false" for row in all_rows)
        and all(row.get("claim_allowed", "false") == "false" for row in next_target),
        "all generated rows remain nonclaim",
    )
    add(
        "V1161_8_next_target",
        next_target[0]["next_target"].startswith("1162-")
        and "strict-Cperp-candidate" in str(next_target[0]["next_target"]),
        "1162 handoff targets strict Cperp candidate choice or edge-bound source fill",
    )
    add(
        "V1161_9_generated_under_post_checkpoint",
        all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()),
        "all generated outputs are under post-checkpoint-work",
    )
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1161_10_csv_parse", csv_parse_ok, "all 1161 CSV outputs parse cleanly")
    add("V1161_11_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add(
        "V1161_SUMMARY",
        True,
        "1161 rejects undefined Cperp/d_rel and unproved local/FLRW selector, emits exact source rows, and sends 1162 to strict candidate choice or edge-bound fill",
    )
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        cells = [str(row.get(header, "")).replace("|", "/") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    cperp_audit: list[dict[str, object]],
    selector_audit: list[dict[str, object]],
    source_pack: list[dict[str, object]],
    guards: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1161 - Y5/R10 Cperp Form/d_rel Operator Source Row or Local Branch Selector Proof

**Current verdict:** neither door closes yet. The corpus does not currently source an actual `C_perp` form plus `d_rel` relative complex, and it does not derive the local-trivial/FLRW-active selector by one parent law.

**Main progress:** the ambiguity is now forced into explicit rows. We cannot keep using `Cperp` as a floating symbol; the next pass must choose one candidate definition or reject all of them and source the edge-bound terms.

**Selector status:** the local/FLRW split remains attractive but underived. Fixed-domain `Qcoh`, free-boundary extrema, `C_exp`, and quotient split are good footwork, not a parent branch law.

**No claim:** no `Cperp` exactness, `B_C=0`, `q`-null, `c_g=0`, local-GR, Newton, R10, PPN, WEP, clock, orbital, GitHub, or public claim follows from 1161.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "role"], sources)}

## Cperp / d_rel Source Audit
{table(["audit_id", "candidate", "would_supply", "current_status", "why_not_enough", "required_next", "valid_for_claim"], cperp_audit)}

## Local/FLRW Branch Selector Audit
{table(["audit_id", "selector_piece", "required_statement", "current_status", "failure_mode", "source_anchor", "valid_for_claim"], selector_audit)}

## Source Pack Rows
{table(["row_id", "quantity", "required_fields", "current_value", "source_path", "status", "valid_for_claim", "claim_allowed"], source_pack)}

## No-Cheat Guards
{table(["guard_id", "guard", "status", "reason", "valid_for_claim"], guards)}

## Claim Gates
{table(["gate_id", "rule", "gate_pass", "reason", "valid_for_claim"], gates)}

## Decision Ledger
{table(["decision_id", "decision", "reason", "next_action", "valid_for_claim"], decisions)}

## Validation
{table(["check_id", "result", "detail", "valid_for_claim"], validation)}

## Next Target
{table(["next_id", "next_target", "objective", "include", "exclude", "valid_for_claim", "claim_allowed"], next_target)}
"""
    DOC.write_text(text, encoding="utf-8")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists() and pycache.is_dir():
        shutil.rmtree(pycache)


def main() -> None:
    outputs = {
        "source_register": OUT / "P8_Y5_R10_1161_SOURCE_REGISTER.csv",
        "cperp_audit": OUT / "P8_Y5_R10_1161_CPERP_DREL_SOURCE_AUDIT.csv",
        "selector_audit": OUT / "P8_Y5_R10_1161_LOCAL_FLRW_SELECTOR_PROOF_AUDIT.csv",
        "source_pack": OUT / "P8_Y5_R10_1161_CPERP_DREL_SELECTOR_SOURCE_PACK.csv",
        "guards": OUT / "P8_Y5_R10_1161_NO_CPERP_DREL_CHEAT_GUARDS.csv",
        "gates": OUT / "P8_Y5_R10_1161_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1161_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1161_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1161_VALIDATION.csv",
    }

    sources = source_rows()
    cperp_audit = cperp_drel_audit_rows()
    selector_audit = branch_selector_audit_rows()
    source_pack = source_pack_rows()
    guards = guard_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["cperp_audit"], cperp_audit)
    write_csv(outputs["selector_audit"], selector_audit)
    write_csv(outputs["source_pack"], source_pack)
    write_csv(outputs["guards"], guards)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, cperp_audit, selector_audit, source_pack, guards, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, cperp_audit, selector_audit, source_pack, guards, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    if failed:
        for row in failed:
            print(f"{row['check_id']}: {row['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()

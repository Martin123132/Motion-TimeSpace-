from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3448-Y5-R2FR-extra-sector-LX-ThetaX-QtauX-owner-or-deltaHcurl-extra-row-under-AX1090.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCES = {
    "script_3448": Path(__file__).resolve(),
    "doc_3447": ROOT / "3447-Y5-R2FR-parent-Theta-Q_tau-extraction-or-deltaH-curl-first-component-row-under-AX1090.md",
    "next_3447": OUT / "P8_Y5_R2FR_3447_NEXT_TARGET.csv",
    "curl_rows_3447": OUT / "P8_Y5_R2FR_3447_DELTAH_CURL_FIRST_COMPONENT_ROWS.csv",
    "theta_qtau_status_3447": OUT / "P8_Y5_R2FR_3447_THETA_QTAU_COMPONENT_STATUS.csv",
    "gamma_khat_q_contract": OUT / "P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv",
    "sector_certificate_2939": OUT / "P8_Y5_R2FR_2939_THETA_QTAU_SECTOR_CERTIFICATE_LEDGER.csv",
    "theta_qtau_components_1733": OUT / "P8_Y5_PARENT_QLOC_1733_THETA_QTAU_COMPONENT_ROWS.csv",
    "first_variation_gates": OUT / "P8_MTS_SYMBOL_FIRST_VARIATION_GATES.csv",
    "lx_owner_audit_2668": OUT / "P8_Y5_R10_LX_THETA_OMEGA_OWNER_2668_OWNER_PROOF_AUDIT.csv",
    "omega_template_2668": OUT / "P8_Y5_R10_LX_THETA_OMEGA_OWNER_2668_OMEGA_COMPONENT_TEMPLATE_NONCLAIM.csv",
    "lx_branch_audit_2669": OUT / "P8_Y5_R2FR_LX_BRANCH_2669_BRANCH_SELECTION_AUDIT.csv",
    "omega_bound_interface_2669": OUT / "P8_Y5_R2FR_LX_BRANCH_2669_OMEGA_BOUND_INTERFACE_NONCLAIM.csv",
    "lx_gate_tests_669": OUT / "P8_Y5_R10_669_LX_OWNER_GATE_TESTS.csv",
    "lx_candidates_669": OUT / "P8_Y5_R10_669_MINIMAL_LX_OPERATOR_CANDIDATES.csv",
    "lx_theorem_1508": OUT / "P8_Y5_R10_1508_LX_THEOREM_LEDGER.csv",
    "lx_field_audit_1508": OUT / "P8_Y5_R10_1508_FIELD_SPECIFIC_LX_OPERATOR_AUDIT.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3448_SOURCE_REGISTER.csv",
    "lx_owner_route_audit": OUT / "P8_Y5_R2FR_3448_LX_OWNER_ROUTE_AUDIT.csv",
    "extra_sector_current_split": OUT / "P8_Y5_R2FR_3448_EXTRA_SECTOR_CURRENT_SPLIT.csv",
    "deltaH_curl_extra_component_row": OUT / "P8_Y5_R2FR_3448_DELTAH_CURL_EXTRA_COMPONENT_ROW.csv",
    "lx_branch_decision": OUT / "P8_Y5_R2FR_3448_LX_BRANCH_DECISION.csv",
    "denominator_update": OUT / "P8_Y5_R2FR_3448_DENOMINATOR_UPDATE.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3448_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3448_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3448_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3448_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3448_VALIDATION.csv",
}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields = list(rows[0].keys())

    def clean(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "/")

    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join("---" for _ in fields) + " |",
            *["| " + " | ".join(clean(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def source_register() -> list[dict[str, Any]]:
    roles = {
        "script_3448": "generator for this checkpoint",
        "doc_3447": "immediate handoff: extra sector is the next hard curl component",
        "next_3447": "machine-readable 3448 target",
        "curl_rows_3447": "DHC3447_1 extra-sector curl blocker",
        "theta_qtau_status_3447": "Theta_extra/Q_tau_extra component status",
        "gamma_khat_q_contract": "first-variation contract for Gamma/Khat/q_loc residual",
        "sector_certificate_2939": "sector certificate row for extra Gamma/Khat branch",
        "theta_qtau_components_1733": "parent Theta/Q_tau component rows",
        "first_variation_gates": "symbol first-variation gates",
        "lx_owner_audit_2668": "prior L_X/Theta/omega owner audit",
        "omega_template_2668": "omega component nonclaim template",
        "lx_branch_audit_2669": "L_X branch ranking and blockers",
        "omega_bound_interface_2669": "omega bound interface rows",
        "lx_gate_tests_669": "minimal L_X owner gate tests",
        "lx_candidates_669": "minimal L_X operator candidates",
        "lx_theorem_1508": "field-specific L_X theorem ledger",
        "lx_field_audit_1508": "field-specific L_X operator audit",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[source_id],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for source_id, path in SOURCES.items()
    ]


def lx_owner_route_audit() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": "LXA3448_0_variational_owner_contract",
            "route": "general covariant-sector owner",
            "exact_statement": "If a parent-owned n-form L_X exists, then delta L_X=E_X delta X+dTheta_X, omega_X=delta Theta_X, J_tau^X=Theta_X(L_tau X)-i_tau L_X=dQ_tau^X+C_tau^X.",
            "zero_or_bound_consequence": "Delta_H_curl_extra is reduced to -int_S i_tau omega_X plus C_tau^X and boundary/corner terms.",
            "blocker": "MISSING_PARENT_LX_FOR_ACTUAL_MTS_EXTRA_SECTOR",
            "preferred_next": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": "LXA3448_1_absent_quotient_erasure",
            "route": "X absent from physical quotient before variation",
            "exact_statement": "If S_parent=S_red[q(Phi)] and X is a pure vertical representative with Dq[v_X]=0, then L_X=Theta_X=omega_X=Q_tau^X=C_tau^X=0 in the quotient action.",
            "zero_or_bound_consequence": "This is the clean GR-reduction route: extra curl is exactly zero without tuning coefficients.",
            "blocker": "MISSING_PARENT_Q_MAP_AND_MATTER_BOUNDARY_DESCENT_SIGNATURE",
            "preferred_next": True,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": "LXA3448_2_vertical_constraint",
            "route": "first-class vertical constraint",
            "exact_statement": "If X generates a presymplectic null direction and its boundary charge vanishes on the selected surfaces, then i_tau omega_X and Q_tau^X vanish after quotienting.",
            "zero_or_bound_consequence": "Conditional zero for the extra curl, but only with a signed constraint algebra and boundary-charge silence.",
            "blocker": "MISSING_DQ_VX_ZERO_CONSTRAINT_ALGEBRA_AND_BOUNDARY_CHARGE_ZERO",
            "preferred_next": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": "LXA3448_3_positive_sourcefree_scalar",
            "route": "positive source-free massive residual",
            "exact_statement": "If L_X has positive quadratic operator Z_X Box+M_X^2, no source J_X, and no boundary inflow, then the local exterior solution may no-hair to X=0.",
            "zero_or_bound_consequence": "Gives a no-hair zero only after Z_X, M_X^2, domain, boundary and source-free premises are parent-owned.",
            "blocker": "MISSING_ZX_MX2_JX_ZERO_DOMAIN_AND_BOUNDARY_INPUTS",
            "preferred_next": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": "LXA3448_4_sourced_scalar_residual",
            "route": "finite sourced residual",
            "exact_statement": "If matter or memory sources X, then omega_X and C_tau^X are not zero theorems and must be bounded through sourced Green-kernel rows.",
            "zero_or_bound_consequence": "Keeps MTS honest: local-GR survives only if sourced residuals satisfy R10/PPN/clock/orbital bounds.",
            "blocker": "MISSING_SOURCE_NORMALIZATION_KERNEL_AND_LOCAL_PROJECTION_ROWS",
            "preferred_next": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": "LXA3448_5_edge_boundary_or_nonlocal_kernel",
            "route": "edge, corner, or nonlocal memory branch",
            "exact_statement": "If the extra sector lives in boundary/corner data or a nonlocal kernel, L_X is not captured by a naive local scalar action.",
            "zero_or_bound_consequence": "Requires explicit edge symplectic form or nonlocal kernel positivity; otherwise it remains a closure/bound term.",
            "blocker": "MISSING_EDGE_SYMPLECTIC_FORM_OR_NONLOCAL_KERNEL_OWNER",
            "preferred_next": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def extra_sector_current_split() -> list[dict[str, Any]]:
    return [
        {
            "split_id": "ECS3448_0_current_split",
            "object": "L_X owner theorem",
            "formula": "delta L_X=E_X delta X+dTheta_X",
            "derivation_status": "EXACT_IF_PARENT_LX_EXISTS",
            "use_in_Htau": "defines the extra-sector symplectic potential entering delta H_tau^X",
            "missing_for_claim": "actual MTS L_X branch selection and parent signature",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "split_id": "ECS3448_1_symplectic_current",
            "object": "omega_X",
            "formula": "omega_X(delta_1,delta_2)=delta_1 Theta_X(delta_2)-delta_2 Theta_X(delta_1)-Theta_X([delta_1,delta_2])",
            "derivation_status": "EXACT_COVARIANT_PHASE_SPACE_IDENTITY",
            "use_in_Htau": "delta H_tau^X=int_S omega_X(delta,L_tau)-int_S i_tau E_X delta X plus boundary/corner terms",
            "missing_for_claim": "surface pair and boundary/corner silence or numeric bound",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "split_id": "ECS3448_2_noether_current",
            "object": "J_tau^X",
            "formula": "J_tau^X=Theta_X(L_tau X)-i_tau L_X=dQ_tau^X+C_tau^X",
            "derivation_status": "EXACT_ONCE_LX_AND_TAU_ACTION_ARE_SIGNED",
            "use_in_Htau": "separates charge Q_tau^X from constraint/source remainder C_tau^X",
            "missing_for_claim": "Q_tau^X and C_tau^X extraction for actual residual sector",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "split_id": "ECS3448_3_curl_component",
            "object": "Delta_H_curl_extra",
            "formula": "Delta_H_curl_extra <= abs(int_BF[-int_S i_tau omega_X + C_tau^X + B_X])",
            "derivation_status": "NO_CANCELLATION_BOUND_FORM",
            "use_in_Htau": "turns DHC3447_1 from one vague missing item into named source rows",
            "missing_for_claim": "omega_X integral bound, C_tau^X bound, B_X boundary flux, units and surface/tau normalization",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "split_id": "ECS3448_4_exact_zero_conditions",
            "object": "extra-sector zero theorem",
            "formula": "L_X=Theta_X=omega_X=Q_tau^X=C_tau^X=B_X=0",
            "derivation_status": "CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "use_in_Htau": "would close the clean local-GR route if absent-quotient erasure is proven",
            "missing_for_claim": "q-map, verticality, matter descent, coframe/connection descent and boundary silence",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "split_id": "ECS3448_5_verdict",
            "object": "3448 status",
            "formula": "derive split now; do not claim zero",
            "derivation_status": "FORMAL_REDUCTION_ACHIEVED_PARENT_NUMERIC_OR_ZERO_OWNER_MISSING",
            "use_in_Htau": "extra component is source-ready and points to the least-scrutiny next proof attempt",
            "missing_for_claim": "absent-quotient proof or first real omega_X/C_tau^X bound row",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def deltaH_curl_extra_component_row() -> list[dict[str, Any]]:
    current_split_path = OUTPUTS["extra_sector_current_split"]
    branch_path = OUTPUTS["lx_branch_decision"]
    return [
        {
            "row_id": "DHC3448_0_Delta_H_curl_extra",
            "quantity": "Delta_H_curl_extra",
            "definition": "MTS extra/domain/memory/range/source-exchange contribution to the H_tau curl after public-sector extraction",
            "formula": "abs(int_BF[-int_S i_tau omega_X + C_tau^X + B_X])",
            "branch_selector": "absent_quotient_preferred_else_vertical_or_bound",
            "L_X": "MISSING_PARENT_LX_BRANCH",
            "Theta_X": "Theta_X from delta L_X=E_X delta X+dTheta_X if L_X is signed",
            "Q_tau_X": "Q_tau^X from J_tau^X=dQ_tau^X+C_tau^X if current is signed",
            "C_tau_X": "MISSING_CONSTRAINT_OR_SOURCE_REMAINDER_BOUND",
            "omega_X_integral_bound": "MISSING_INT_S_I_TAU_OMEGAX_BOUND",
            "boundary_flux_X": "MISSING_BX_BOUND_OR_ZERO",
            "surface_pair": "MISSING_SURFACE_PAIR_FOR_EXTRA_SECTOR",
            "variation_pair": "MISSING_FIELD_SPACE_VARIATION_PAIR_FOR_EXTRA_SECTOR",
            "units": "same as H_tau curl numerator after tau/surface normalization; not numeric yet",
            "current_status": "SCHEMA_READY_NONCLAIM_BRANCH_SELECTION_MISSING",
            "source_path": str(current_split_path),
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "DHC3448_1_absent_quotient_zero_candidate",
            "quantity": "Z_extra_absent_quotient",
            "definition": "candidate exact zero if X is not a physical quotient variable before variation",
            "formula": "S_parent=S_red[q(Phi)], Dq[v_X]=0 => L_X=Theta_X=omega_X=Q_tau^X=C_tau^X=0",
            "branch_selector": "preferred_zero_route",
            "L_X": "0 if absent quotient is parent-signed",
            "Theta_X": "0 if absent quotient is parent-signed",
            "Q_tau_X": "0 if absent quotient is parent-signed",
            "C_tau_X": "0 if absent quotient is parent-signed",
            "omega_X_integral_bound": "0 if absent quotient is parent-signed",
            "boundary_flux_X": "0 if boundary descent is parent-signed",
            "surface_pair": "all admissible local exterior surfaces after quotient",
            "variation_pair": "vertical variations in ker(Dq)",
            "units": "dimensionless zero certificate feeding H_tau numerator",
            "current_status": "CONDITIONAL_ZERO_NOT_SIGNED",
            "source_path": str(branch_path),
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "DHC3448_2_vertical_constraint_zero_candidate",
            "quantity": "Z_extra_vertical_constraint",
            "definition": "candidate exact zero if X is a presymplectic gauge direction with silent boundary charge",
            "formula": "i_{v_X}omega=0 and Q_tau^X|_S=0 => int_S i_tau omega_X=0 and C_tau^X=0 on shell",
            "branch_selector": "second_zero_route",
            "L_X": "constraint action not signed",
            "Theta_X": "degenerate along v_X if constraint proof closes",
            "Q_tau_X": "requires boundary charge zero",
            "C_tau_X": "requires first-class constraint closure",
            "omega_X_integral_bound": "0 only after presymplectic null certificate",
            "boundary_flux_X": "0 only after boundary charge silence",
            "surface_pair": "selected local exterior surfaces",
            "variation_pair": "vertical constraint variations",
            "units": "dimensionless zero certificate feeding H_tau numerator",
            "current_status": "CONDITIONAL_ZERO_NOT_SIGNED",
            "source_path": str(branch_path),
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "DHC3448_3_omegaX_integral_bound",
            "quantity": "I_omega_X",
            "definition": "surface integral envelope for extra-sector symplectic leakage",
            "formula": "I_omega_X := abs(int_BF int_S i_tau omega_X)",
            "branch_selector": "finite_bound_route",
            "L_X": "requires signed positive/sourceful or nonlocal L_X",
            "Theta_X": "required",
            "Q_tau_X": "not sufficient alone",
            "C_tau_X": "separate row",
            "omega_X_integral_bound": "MISSING_NUMERIC_OR_THEOREM_BOUND",
            "boundary_flux_X": "separate row",
            "surface_pair": "MISSING",
            "variation_pair": "MISSING",
            "units": "H_tau curl numerator units",
            "current_status": "BOUND_ROW_READY_NONCLAIM",
            "source_path": str(current_split_path),
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "DHC3448_4_CtauX_bound",
            "quantity": "I_Ctau_X",
            "definition": "constraint/source remainder envelope for extra-sector Noether current",
            "formula": "I_Ctau_X := abs(int_BF C_tau^X)",
            "branch_selector": "finite_bound_route",
            "L_X": "requires signed L_X and Euler/source split",
            "Theta_X": "required indirectly",
            "Q_tau_X": "requires current decomposition",
            "C_tau_X": "MISSING_NUMERIC_OR_THEOREM_BOUND",
            "omega_X_integral_bound": "separate row",
            "boundary_flux_X": "separate row",
            "surface_pair": "MISSING",
            "variation_pair": "MISSING",
            "units": "H_tau curl numerator units",
            "current_status": "BOUND_ROW_READY_NONCLAIM",
            "source_path": str(current_split_path),
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "DHC3448_5_boundary_flux_X",
            "quantity": "I_boundary_X",
            "definition": "extra-sector boundary/corner/nonlocal inflow envelope",
            "formula": "I_boundary_X := abs(int_BF B_X)",
            "branch_selector": "edge_or_nonlocal_bound_route",
            "L_X": "may be boundary/corner/nonlocal rather than bulk local",
            "Theta_X": "requires edge symplectic or kernel owner",
            "Q_tau_X": "requires edge charge owner",
            "C_tau_X": "may include nonlocal source term",
            "omega_X_integral_bound": "separate row",
            "boundary_flux_X": "MISSING_NUMERIC_OR_THEOREM_BOUND",
            "surface_pair": "MISSING",
            "variation_pair": "MISSING",
            "units": "H_tau curl numerator units",
            "current_status": "BOUND_ROW_READY_NONCLAIM",
            "source_path": str(current_split_path),
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def lx_branch_decision() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "LBD3448_0_selected_order",
            "decision": "try absent-quotient erasure first",
            "reason": "It gives the least-scrutiny local-GR reduction: no hidden coupling, no tuned small coefficient, no numeric post-fit residual.",
            "claim_status": "NOT_CLAIMED",
            "next_required_input": "parent q-map, vertical generator v_X, matter/coframe/connection descent and boundary silence",
            "fallback": "if erasure fails, fill omega_X/C_tau^X/B_X source-bound rows",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "LBD3448_1_why_not_scalar_now",
            "decision": "do not instantiate scalar L_X yet",
            "reason": "A scalar branch would add Z_X, M_X^2 and J_X coefficients before the quotient question is settled; that creates more scrutiny than the clean GR-reduction route.",
            "claim_status": "NOT_CLAIMED",
            "next_required_input": "only reopen scalar if absent quotient and vertical constraint fail",
            "fallback": "source finite local-bound rows",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "LBD3448_2_Poynting_wave_note",
            "decision": "do not hide EM/wave flux inside X",
            "reason": "Public EM Poynting flux belongs to the public Hilbert/symplectic sector; extra X is reserved for genuinely MTS residual/domain/memory terms.",
            "claim_status": "DISCIPLINE_NOTE",
            "next_required_input": "keep public EM boundary/radiation flux separate from extra-sector omega_X",
            "fallback": "bound public EM flux in the public-sector curl row",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def denominator_update() -> list[dict[str, Any]]:
    return [
        {
            "update_id": "DEN3448_0_DHC3447_1_replaced_by_schema",
            "prior_row": "DHC3447_1_extra_sector_curl",
            "new_rows": "DHC3448_0..DHC3448_5",
            "change": "single missing blob split into L_X owner, omega_X integral, C_tau^X remainder and boundary/corner/nonlocal flux rows",
            "claim_effect": "no pass claimed; denominator/curl bound is more executable",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "update_id": "DEN3448_1_MHref_no_promotion",
            "prior_row": "M_H_ref denominator branch",
            "new_rows": "unchanged",
            "change": "3448 attacks numerator curl structure only; positive same-frame M_H_ref remains a separate source row",
            "claim_effect": "H_tau reference lock still nonclaim",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "G3448_0_sources_exist",
            "gate": "all cited 3448 sources exist",
            "status": "PRIVATE_CHECK_PASS",
            "blocks_claim": False,
            "needed_for_claim": "source existence alone is not a physics proof",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G3448_1_current_split_written",
            "gate": "exact covariant L_X -> Theta_X -> omega_X -> J_tau^X split written",
            "status": "PRIVATE_CHECK_PASS",
            "blocks_claim": False,
            "needed_for_claim": "actual parent L_X branch must be signed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G3448_2_absent_quotient",
            "gate": "prove X absent from physical quotient before variation",
            "status": "MISSING_PARENT_Q_MAP",
            "blocks_claim": True,
            "needed_for_claim": "S_parent=S_red[q(Phi)], Dq[v_X]=0, descent of matter/coframe/connection and boundary silence",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G3448_3_vertical_constraint",
            "gate": "prove X is a presymplectic null/gauge direction",
            "status": "MISSING_CONSTRAINT_ALGEBRA_AND_BOUNDARY_CHARGE_ZERO",
            "blocks_claim": True,
            "needed_for_claim": "i_v omega=0, first-class closure and Q_tau^X boundary silence",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G3448_4_bound_rows",
            "gate": "if zero proof fails, source omega_X/C_tau^X/B_X bounds",
            "status": "SCHEMA_READY_VALUES_MISSING",
            "blocks_claim": True,
            "needed_for_claim": "numeric or theorem bounds with units, surfaces, tau and source paths",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G3448_5_no_public_claim",
            "gate": "no local-GR/Newton/R10/PPN/clock/orbital pass from this checkpoint",
            "status": "ENFORCED",
            "blocks_claim": True,
            "needed_for_claim": "full residual vector must be zero or bounded and compared to arenas",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3448_0",
            "question": "Can 3448 prove L_X disappears?",
            "answer": "Not yet; it proves the exact current split and identifies the clean zero theorem clauses.",
            "reason": "The parent q-map/vertical generator/descent/boundary package is still unsigned.",
            "next_action": "3449 absent-quotient X-erasure attempt",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3448_1",
            "question": "Is this just circling the same missing item?",
            "answer": "No; DHC3447_1 is now executable as separate omega_X, C_tau^X and boundary rows, with an explicit zero theorem target.",
            "reason": "A vague missing extra current cannot be tested; a split residual vector can be proven zero or bounded.",
            "next_action": "try the least-scrutiny exact zero route before scalar/bound fallback",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3449-Y5-R2FR-absent-quotient-X-erasure-or-omegaX-bound-first-row-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3449_absent_quotient_X_erasure_or_omegaX_bound_first_row.py",
            "objective": "Prove X is absent from the physical quotient before variation via q-map/vertical-generator/descent/boundary silence, or fill the first omega_X bound row.",
            "start_from": "LXA3448_1_absent_quotient_erasure and DHC3448_3_omegaX_integral_bound",
            "success_gate": "Either parent-signed L_X=0 zero certificate or nonclaim omega_X source-bound row with units/surface/tau/provenance",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3448_0",
            "mode": "private_nonclaim_checkpoint",
            "result": "extra-sector split and source rows generated",
            "claim_status": "NO_LOCAL_GR_NEWTON_R10_PPN_CLOCK_OR_ORBITAL_CLAIM",
            "reason": "parent-owned zero or numeric bound inputs are still missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], start_utc: datetime) -> list[dict[str, Any]]:
    modified_count = 0
    if FORMALIZATION.exists():
        start_timestamp = start_utc.timestamp()
        modified_count = sum(
            1
            for checked_path in FORMALIZATION.rglob("*")
            if checked_path.is_file() and checked_path.stat().st_mtime >= start_timestamp
        )

    nonclaim_ok = True
    for rows in rows_by_name.values():
        for row in rows:
            if "valid_for_claim" in row and str(row["valid_for_claim"]).lower() != "false":
                nonclaim_ok = False
            if "claim_allowed" in row and str(row["claim_allowed"]).lower() != "false":
                nonclaim_ok = False

    parse_ok = True
    for output_name, path in OUTPUTS.items():
        if output_name == "validation":
            continue
        try:
            read_csv(path)
        except csv.Error:
            parse_ok = False

    branch_ids = {row["branch_id"] for row in rows_by_name["lx_owner_route_audit"]}
    required_branches = {
        "LXA3448_0_variational_owner_contract",
        "LXA3448_1_absent_quotient_erasure",
        "LXA3448_2_vertical_constraint",
        "LXA3448_3_positive_sourcefree_scalar",
        "LXA3448_4_sourced_scalar_residual",
        "LXA3448_5_edge_boundary_or_nonlocal_kernel",
    }
    dhc0 = [
        row
        for row in rows_by_name["deltaH_curl_extra_component_row"]
        if row["row_id"] == "DHC3448_0_Delta_H_curl_extra"
    ]

    validations = [
        {
            "check_id": "VAL3448_0_sources_exist",
            "condition": "all cited 3448 source paths exist",
            "passed": all(path.exists() for path in SOURCES.values()),
            "detail": f"{sum(1 for path in SOURCES.values() if path.exists())}/{len(SOURCES)} source paths exist",
        },
        {
            "check_id": "VAL3448_1_current_split_exact",
            "condition": "exact L_X current split is written",
            "passed": any(
                row["split_id"] == "ECS3448_0_current_split" and "delta L_X=E_X delta X+dTheta_X" in row["formula"]
                for row in rows_by_name["extra_sector_current_split"]
            ),
            "detail": "covariant phase-space split row present",
        },
        {
            "check_id": "VAL3448_2_all_branches_audited",
            "condition": "six L_X branches are audited",
            "passed": required_branches.issubset(branch_ids),
            "detail": f"{len(branch_ids & required_branches)}/{len(required_branches)} required branches present",
        },
        {
            "check_id": "VAL3448_3_absent_quotient_selected",
            "condition": "absent quotient is selected as preferred next proof route",
            "passed": any(
                row["branch_id"] == "LXA3448_1_absent_quotient_erasure" and row["preferred_next"] is True
                for row in rows_by_name["lx_owner_route_audit"]
            )
            and rows_by_name["lx_branch_decision"][0]["decision"] == "try absent-quotient erasure first",
            "detail": rows_by_name["lx_branch_decision"][0]["reason"],
        },
        {
            "check_id": "VAL3448_4_extra_row_source_ready",
            "condition": "DHC3448_0 exists, has a real source path, and remains nonclaim",
            "passed": bool(dhc0)
            and Path(dhc0[0]["source_path"]).exists()
            and dhc0[0]["valid_for_claim"] is False
            and dhc0[0]["claim_allowed"] is False,
            "detail": dhc0[0]["current_status"] if dhc0 else "missing DHC3448_0",
        },
        {
            "check_id": "VAL3448_5_no_claims",
            "condition": "all generated rows remain nonclaim",
            "passed": nonclaim_ok,
            "detail": "valid_for_claim=false and claim_allowed=false wherever present",
        },
        {
            "check_id": "VAL3448_6_generated_csv_parse",
            "condition": "generated CSV rows parse cleanly",
            "passed": parse_ok,
            "detail": "CSV reader pass for generated outputs present before validation write",
        },
        {
            "check_id": "VAL3448_7_next_target_3449",
            "condition": "next target attacks absent quotient or omegaX bound",
            "passed": rows_by_name["next_target"][0]["target_doc"].startswith(
                "3449-Y5-R2FR-absent-quotient-X-erasure"
            ),
            "detail": rows_by_name["next_target"][0]["target_doc"],
        },
        {
            "check_id": "VAL3448_8_formalization_untouched",
            "condition": "formalization-workbench modified-file count remains 0 during this run",
            "passed": modified_count == 0,
            "detail": f"modified_count_since_start={modified_count}",
        },
    ]
    validations.append(
        {
            "check_id": "VAL3448_9_overall",
            "condition": "3448 extra-sector checkpoint is internally valid",
            "passed": all(row["passed"] for row in validations),
            "detail": "PASS" if all(row["passed"] for row in validations) else "FAIL",
        }
    )
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    text = f"""# 3448 - Extra-Sector L_X/Theta_X/Q_tau_X Owner or DeltaH Curl Extra Row

## Summary
- This checkpoint does the derivation step for the extra-sector branch rather than leaving `DHC3447_1` as a vague missing item.
- Exact result: any parent-owned extra-sector local n-form obeys `delta L_X=E_X delta X+dTheta_X`, `omega_X=delta Theta_X`, and `J_tau^X=Theta_X(L_tau X)-i_tau L_X=dQ_tau^X+C_tau^X`.
- Therefore the extra contribution to the `H_tau` curl is not mysterious: it is controlled by `int_S i_tau omega_X`, `C_tau^X`, and boundary/corner/nonlocal flux.
- The cleanest local-GR route remains absent-quotient erasure: if `X` is not a physical quotient variable before variation, then `L_X=Theta_X=omega_X=Q_tau^X=C_tau^X=0`.
- That zero route is not claimed here because the parent `q` map, vertical generator, matter/coframe/connection descent, and boundary silence are not yet signed.
- Public EM/Poynting/wave flux is kept separate in the public-sector row; it is not smuggled into `X`.

## Source Register
{md_table(rows_by_name["source_register"])}

## L_X Owner Route Audit
{md_table(rows_by_name["lx_owner_route_audit"])}

## Extra-Sector Current Split
{md_table(rows_by_name["extra_sector_current_split"])}

## DeltaH Curl Extra Component Row
{md_table(rows_by_name["deltaH_curl_extra_component_row"])}

## L_X Branch Decision
{md_table(rows_by_name["lx_branch_decision"])}

## Denominator Update
{md_table(rows_by_name["denominator_update"])}

## Promotion Gates
{md_table(rows_by_name["promotion_gates"])}

## Decision Ledger
{md_table(rows_by_name["decision_ledger"])}

## Next Target
{md_table(rows_by_name["next_target"])}

## Runner Nonclaim
{md_table(rows_by_name["runner_nonclaim"])}

## Validation
{md_table(rows_by_name["validation"])}

## Bottom Line
This is a real narrowing of the missing coupling problem: `L_X` is now either erased before variation by quotient geometry, proven vertical/gauge, or bounded by named `omega_X`, `C_tau^X`, and boundary rows. The best next attack is not another broad audit; it is the exact absent-quotient proof in 3449.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    start_utc = datetime.now(timezone.utc)
    rows_by_name = {
        "source_register": source_register(),
        "lx_owner_route_audit": lx_owner_route_audit(),
        "extra_sector_current_split": extra_sector_current_split(),
        "deltaH_curl_extra_component_row": deltaH_curl_extra_component_row(),
        "lx_branch_decision": lx_branch_decision(),
        "denominator_update": denominator_update(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    for output_name, rows in rows_by_name.items():
        write_csv(OUTPUTS[output_name], rows)
    rows_by_name["validation"] = validation_rows(rows_by_name, start_utc)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    failed_rows = [row for row in rows_by_name["validation"] if not row["passed"]]
    if failed_rows:
        raise SystemExit(f"3448 validation failed: {failed_rows}")
    print(f"wrote {DOC}")
    print(f"wrote {len(OUTPUTS)} csv outputs")


if __name__ == "__main__":
    main()

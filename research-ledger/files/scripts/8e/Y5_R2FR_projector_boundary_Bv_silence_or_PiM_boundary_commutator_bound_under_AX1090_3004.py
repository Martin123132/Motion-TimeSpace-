from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "3004"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3004-Y5-R2FR-projector-boundary-Bv-silence-or-PiM-boundary-commutator-bound-under-AX1090.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3004_SOURCE_REGISTER.csv",
    "audit": RESIDUALS / "P8_Y5_R2FR_3004_PROJECTOR_BOUNDARY_SILENCE_AUDIT.csv",
    "commutator": RESIDUALS / "P8_Y5_R2FR_3004_PIM_BOUNDARY_COMMUTATOR_ROWS.csv",
    "bounds": RESIDUALS / "P8_Y5_R2FR_3004_EPSILON_BV_PROJECTOR_BOUNDARY_BOUND_ROWS.csv",
    "rebase": RESIDUALS / "P8_Y5_R2FR_3004_BV_REBASE_AFTER_PROJECTOR_BOUNDARY.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3004_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3004_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3004_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3004_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3004_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "audit_copy": PARENT_ACTION / "projector_boundary_Bv_silence_3004_NOT_SIGNED.csv",
    "bounds_copy": LOCAL_BOUNDS / "epsilon_Bv_projector_boundary_bound_rows_3004_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3004_MREF_DENOMINATOR_BV_NEXT_NONCLAIM.csv",
}

for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    path.parent.mkdir(parents=True, exist_ok=True)


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def anchors(path: Path, needles: list[str]) -> bool:
    haystack = text(path)
    return path.exists() and all(needle in haystack for needle in needles)


def missing_anchors(path: Path, needles: list[str]) -> str:
    haystack = text(path)
    return "; ".join(needle for needle in needles if needle not in haystack)


def base(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "control_only": True,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "generated_utc": RUN_UTC,
    }


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for output_row in output_rows:
        for key in output_row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)


def csv_ok(path: Path) -> bool:
    try:
        rows(path)
        return True
    except Exception:
        return False


def under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "passed"}


def md_table(output_rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, divider]
    for output_row in output_rows:
        cells = [str(output_row.get(column, "")).replace("\n", " ").replace("|", "/") for column in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


SOURCE_SPECS = [
    (
        "SRC3004_00_3003_next",
        RESIDUALS / "P8_Y5_R2FR_3003_NEXT_TARGET.csv",
        ["NEXT3003_0_3004", "epsilon_Bv_projector_boundary"],
        "3003 selects projector-boundary Bv silence/commutator next.",
    ),
    (
        "SRC3004_01_3003_rebase",
        RESIDUALS / "P8_Y5_R2FR_3003_BV_REBASE_AFTER_REFERENCE_SELECTOR.csv",
        ["REB3003_4_Bv_remainder", "MISSING_PROJECTOR_BOUNDARY_MREF_BOUNDS"],
        "3003 leaves projector-boundary and denominator as remaining Bv debts.",
    ),
    (
        "SRC3004_02_2991_clause",
        RESIDUALS / "P8_Y5_R2FR_2991_BOUNDARY_REFERENCE_CLAUSE_AUDIT.csv",
        ["BCA2991_6_projector_boundary", "MISSING_PROJECTOR_BOUNDARY_SILENCE"],
        "2991 names the missing projector/source-measure boundary silence clause.",
    ),
    (
        "SRC3004_03_2991_epsilon",
        RESIDUALS / "P8_Y5_R2FR_2991_EPSILON_BV_SOURCE_BOUND_ROWS_NONCLAIM.csv",
        ["EBV2991_06_projector_boundary", "BZ2447_5_projector_symplectic_silence"],
        "2991 defines epsilon_Bv_projector_boundary and its symplectic leakage interface.",
    ),
    (
        "SRC3004_04_2999_selection",
        RESIDUALS / "P8_Y5_R2FR_2999_COMPONENT_SELECTION_LEDGER.csv",
        ["SEL2999_4_projector_boundary", "requires Pi_M boundary stress and commutator control"],
        "2999 defers projector-boundary until Pi_M stress and commutator are controlled.",
    ),
    (
        "SRC3004_05_2447_gate",
        RESIDUALS / "P8_Y5_PARENT_QLOC_2447_BOUNDARY_REFERENCE_S_EQ_ZERO_THEOREM_GATE.csv",
        ["BZ2447_5_projector_symplectic_silence", "BLOCKED"],
        "2447 blocks projector boundary q-current silence.",
    ),
    (
        "SRC3004_06_550_fill",
        RESIDUALS / "P8_Y5_BRR545_COMMUTATOR_PROJECTOR_BOUND_FILL_ROW.csv",
        ["FB550_0_commutator_projector_bound", "MISSING_COMMUTATOR_NUMERIC_OR_THEOREM_ZERO"],
        "550 gives the strict commutator/projector-variation bound row template.",
    ),
    (
        "SRC3004_07_1518_commutator_doc",
        ROOT / "1518-Y5-parent-PiM-commutator-zero-theorem-or-R_eq-I_commutator-source-acquisition.md",
        ["COM1518_8_verdict", "PIM_COMMUTATOR_ZERO_NOT_PROVED"],
        "1518 audits the Pi_M commutator zero theorem and refuses promotion.",
    ),
    (
        "SRC3004_08_PiM_contract",
        RESIDUALS / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
        ["PM4_projector_algebra", "PM5_projector_variation_owned", "PM6_flux_closure_requires_Ward_or_Euler"],
        "Pi_M contract states algebra, variation ownership and flux closure requirements.",
    ),
    (
        "SRC3004_09_charge_direct",
        RESIDUALS / "P8_charge_current_equality_DIRECT_ATTEMPT.csv",
        ["CC4_boundary_variation_equals_projected_source_variation", "CC7_closed_flux_and_Gauss_calibration"],
        "charge-current route shows projector/boundary leakage blocks mass-source equality.",
    ),
    (
        "SRC3004_10_charge_residual",
        RESIDUALS / "P8_charge_current_equality_RESIDUAL_DECOMPOSITION.csv",
        ["Delta_PiM", "Delta_flux"],
        "charge-current decomposition retains Delta_PiM and flux residuals.",
    ),
    (
        "SRC3004_11_worldtube",
        RESIDUALS / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
        ["T510_0_EH_reference_glue", "not_yet_inherited"],
        "worldtube theorem supplies GR-style conditional reference, not yet MTS inherited.",
    ),
    (
        "SRC3004_12_2620_variation",
        RESIDUALS / "P8_Y5_EH_DOMINANCE_GATE_2620_SECTOR_VARIATION_AUDIT.csv",
        ["SVA2620_3_projector", "MISSING_PROJECTOR_VARIATION_COMMUTATOR_ZERO"],
        "2620 keeps projector action variation/commutator zero unsigned.",
    ),
    (
        "SRC3004_13_2620_operator",
        RESIDUALS / "P8_Y5_EH_DOMINANCE_GATE_2620_OPERATOR_COEFFICIENT_PACK.csv",
        ["OPC2620_2_projector", "MISSING_PROJECTOR_ACTION_VARIATION_OR_BOUND"],
        "2620 keeps projector operator coefficient/source bound missing.",
    ),
    (
        "SRC3004_14_2595_components",
        RESIDUALS / "P8_Y5_GM_TRANSFER_2595_COMPONENT_ROWS.csv",
        ["GMC2595_1_I_commutator", "GMC2595_3_projector_stress", "GMC2595_4_MHref"],
        "2595 has component rows for commutator, projector stress and M_H_ref denominator.",
    ),
    (
        "SRC3004_15_1843_projector",
        ROOT / "1843-Y5-R2FR-boundary-exactness-projector-orthogonality-or-source-pack.md",
        ["PO1843_5_verdict", "FAIL_CURRENT_CLAIM"],
        "1843 projector orthogonality precedent rejects current edge/source projector-zero claim.",
    ),
    (
        "SRC3004_16_2350_boundary",
        RESIDUALS / "P8_Y5_PARENT_QLOC_2350_BOUNDARY_IMPROVEMENT_ZERO_AUDIT.csv",
        ["BIC2350_5_projector_equality_gap", "MISSING_EQUALITY_AND_COMMUTATOR_THEOREMS"],
        "2350 identifies Hilbert/topological equality and projector commutator gap.",
    ),
]


def source_rows() -> list[dict[str, Any]]:
    return [
        base(
            {
                "source_id": source_id,
                "source_path": str(path),
                "path_exists": path.exists(),
                "required_anchors": "; ".join(needles),
                "anchors_found": anchors(path, needles),
                "missing_anchors": missing_anchors(path, needles),
                "role": role,
            }
        )
        for source_id, path, needles, role in SOURCE_SPECS
    ]


def audit_rows() -> list[dict[str, Any]]:
    data = [
        (
            "PBA3004_0_product_rule",
            "do not drop d(Pi_M J_H)=Pi_M dJ_H+[d,Pi_M]J_H",
            "IDENTITY_RETAINED",
            "dropping the commutator is algebraic handwaving",
            "COM1518_0_product_rule;FB550_0_commutator_projector_bound",
        ),
        (
            "PBA3004_1_parent_projector",
            "Pi_M is defined by the parent action before readout",
            "PARENT_PROJECTOR_NOT_DERIVED",
            "otherwise Pi_M can become a measured-GM/source mask",
            "PM3_charge_functional_before_readout;PM4_projector_algebra",
        ),
        (
            "PBA3004_2_same_domain",
            "q, Pi_M, Q_tau, J_H, boundary surface and readout use the same fixed domain",
            "MISSING_SAME_DOMAIN_HOMOLOGY_LOCK",
            "domain drift feeds annulus commutator and radial mass drift",
            "PM0_fixed_exterior_topology;GMC2595_5_surfaces",
        ),
        (
            "PBA3004_3_chainmap",
            "Pi_M is a chain-map on the physical Hilbert-current complex",
            "CONDITIONAL_LEMMA_ONLY",
            "chain-map proof can target a surrogate current if J_H domain is unsigned",
            "COM1518_1_conditional_chainmap;FCM1518_3_chainmap",
        ),
        (
            "PBA3004_4_projector_variation",
            "delta Pi_M is zero or owned in the Ward/source ledger",
            "MISSING_PROJECTOR_VARIATION_COMMUTATOR_ZERO",
            "metric/Hodge/DeWitt projector stress enters local source channel",
            "PM5_projector_variation_owned;SVA2620_3_projector",
        ),
        (
            "PBA3004_5_flux_closure",
            "d(Pi_M J_H)=0 follows from Ward/Euler/topological closure",
            "NOT_PARENT_DERIVED",
            "Pi_M algebra alone does not prove exterior mass flux closure",
            "PM6_flux_closure_requires_Ward_or_Euler;Delta_flux",
        ),
        (
            "PBA3004_6_exterior_silence",
            "annulus has no source/anomaly/boundary/projector support",
            "MISSING_EXTERIOR_SILENCE_THEOREM",
            "finite-shell I_commutator profile can be nonzero",
            "COM1518_5_exterior;T510_0_EH_reference_glue",
        ),
        (
            "PBA3004_7_tau_MHref",
            "same tau/source/charge/readout frame and positive M_H_ref denominator",
            "MISSING_TAU_MHREF_LOCK",
            "projector residual cannot be normalized claim-safely",
            "COM1518_6_tau_MHref;GMC2595_4_MHref",
        ),
        (
            "PBA3004_8_boundary_orthogonality",
            "boundary/edge/reference sectors are orthogonal to mass source projection",
            "FAIL_CURRENT_CLAIM",
            "edge/source mixing can feed R10/R11/PPN projector rows",
            "PO1843_5_verdict;BIC2350_5_projector_equality_gap",
        ),
        (
            "PBA3004_9_verdict",
            "epsilon_Bv_projector_boundary zero selector",
            "ZERO_NOT_PROMOTED_BOUND_ROWS_STAGED",
            "conditional route exists, but parent projector ownership/domain/commutator/stress clauses are unsigned",
            "all rows above",
        ),
    ]
    return [
        base(
            {
                "audit_id": audit_id,
                "projector_clause": projector_clause,
                "current_status": current_status,
                "failure_mode": failure_mode,
                "source_anchors": source_anchors,
                "parent_signed_now": False,
                "theorem_zero_now": False,
            }
        )
        for audit_id, projector_clause, current_status, failure_mode, source_anchors in data
    ]


def commutator_rows() -> list[dict[str, Any]]:
    data = [
        (
            "PIMC3004_0_zero_switch",
            "projector_boundary_zero_if_parent_chainmap",
            "0 if Pi_M is parent-defined, fixed-domain, chain-map, variation-owned, exterior-silent, and same-frame normalized",
            "CONDITIONAL_ZERO_NOT_PROMOTED",
            "COM1518_1_conditional_chainmap;PM4_projector_algebra;PM5_projector_variation_owned",
        ),
        (
            "PIMC3004_1_commutator_annulus",
            "I_commutator",
            "abs(int_A [d,Pi_M]J_H)/M_ref",
            "MISSING_I_COMMUTATOR",
            "GMC2595_1_I_commutator;FB550_0_commutator_projector_bound",
        ),
        (
            "PIMC3004_2_projector_variation_surface",
            "I_delta_PiM_boundary",
            "abs(int_S (delta Pi_M)J_H)/M_ref",
            "MISSING_PROJECTOR_VARIATION_NUMERIC_OR_THEOREM_ZERO",
            "PM5_projector_variation_owned;SVA2620_3_projector",
        ),
        (
            "PIMC3004_3_projector_stress",
            "epsilon_projector_stress",
            "abs(E_projector or metric-dependent Pi_M stress response) in source-normalized units",
            "MISSING_PROJECTOR_STRESS_MAP_OR_THEOREM_ZERO",
            "GMC2595_3_projector_stress;OPC2620_2_projector",
        ),
        (
            "PIMC3004_4_mass_current_mismatch",
            "R_eq_integral",
            "abs(int_S(Pi_M J_H - J_M_top - dB_zero))/M_ref",
            "MISSING_R_EQ_INTEGRAL",
            "CC4_boundary_variation_equals_projected_source_variation;BIC2350_5_projector_equality_gap",
        ),
        (
            "PIMC3004_5_flux_drift",
            "Delta_flux_projected_mass",
            "abs(int_A d(Pi_M J_H))/M_ref",
            "MISSING_WARD_EULER_FLUX_CLOSURE",
            "Delta_flux;PM6_flux_closure_requires_Ward_or_Euler",
        ),
        (
            "PIMC3004_6_total_absolute",
            "epsilon_projector_symplectic_abs",
            "sum_abs(PIMC3004_1..5) with no cancellation credit",
            "NOT_COMPUTED_COMPONENTS_MISSING",
            "FB550_0_commutator_projector_bound;GMC2595_4_MHref",
        ),
    ]
    return [
        base(
            {
                "row_id": row_id,
                "quantity": quantity,
                "bound_interface": bound_interface,
                "current_value": "NOT_ALLOWED_AS_VALUE" if "ZERO" in status else "MISSING_VALUE",
                "status": status,
                "units": "dimensionless_after_same_frame_M_ref",
                "source_anchors": source_anchors,
                "finite_numeric_value_present": False,
                "theorem_zero_now": False,
            }
        )
        for row_id, quantity, bound_interface, status, source_anchors in data
    ]


def bound_rows() -> list[dict[str, Any]]:
    data = [
        (
            "PBV3004_0_zero_switch",
            "epsilon_Bv_projector_boundary_zero_if_chainmap_silent",
            "0 if PIMC3004_0 is parent-signed and the surface/domain/M_ref frame is identical to q,Q_tau,readout",
            "CONDITIONAL_ZERO_NOT_PROMOTED",
            "BZ2447_5_projector_symplectic_silence;COM1518_8_verdict",
        ),
        (
            "PBV3004_1_commutator",
            "epsilon_Bv_projector_commutator_abs",
            "abs(int_A [d,Pi_M]J_H)/M_ref",
            "MISSING_COMMUTATOR_NUMERIC_OR_THEOREM_ZERO",
            "FB550_0_commutator_projector_bound;PIMC3004_1_commutator_annulus",
        ),
        (
            "PBV3004_2_delta_projector",
            "epsilon_Bv_delta_PiM_boundary_abs",
            "abs(int_S (delta Pi_M)J_H)/M_ref",
            "MISSING_PROJECTOR_VARIATION_NUMERIC_OR_THEOREM_ZERO",
            "FB550_0_commutator_projector_bound;PIMC3004_2_projector_variation_surface",
        ),
        (
            "PBV3004_3_projector_stress",
            "epsilon_Bv_projector_stress_abs",
            "abs(projector stress/source-normalization contribution)",
            "MISSING_PROJECTOR_STRESS_MAP_OR_THEOREM_ZERO",
            "GMC2595_3_projector_stress;OPC2620_2_projector",
        ),
        (
            "PBV3004_4_mass_current_mismatch",
            "epsilon_Bv_PiM_current_mismatch_abs",
            "abs(int_S(Pi_M J_H - J_M_parent_or_topological - dB_zero))/M_ref",
            "MISSING_R_EQ_INTEGRAL",
            "Delta_PiM;BIC2350_5_projector_equality_gap",
        ),
        (
            "PBV3004_5_total",
            "epsilon_Bv_projector_boundary",
            "sum_abs(PBV3004_1..4 plus any flux drift) with no observed-GM import",
            "MISSING_SOURCE_BACKED_UPPER_BOUND",
            "EBV2991_06_projector_boundary;PIMC3004_6_total_absolute",
        ),
    ]
    return [
        base(
            {
                "bound_id": bound_id,
                "symbol": symbol,
                "bound_interface": bound_interface,
                "current_value": "NOT_ALLOWED_AS_VALUE" if "ZERO" in status else "MISSING_VALUE",
                "status": status,
                "units": "dimensionless_after_same_frame_M_ref",
                "source_anchors": source_anchors,
                "finite_numeric_value_present": False,
                "theorem_zero_now": False,
            }
        )
        for bound_id, symbol, bound_interface, status, source_anchors in data
    ]


def rebase_rows() -> list[dict[str, Any]]:
    data = [
        ("REB3004_0_exact_fixed", "epsilon_Bv_exact_fixed_primitive", "0", "closed only as exact/fixed component by 2999"),
        ("REB3004_1_tau_surface", "epsilon_Bv_tau_surface_commutator_total_abs", "COMPONENTS_MISSING_NO_FINITE_VALUE", "demoted to explicit residual closure by 3001"),
        ("REB3004_2_corner_topological", "epsilon_Bv_corner_topological_total_abs", "MISSING_SOURCE_BACKED_UPPER_BOUND", "classified and staged by 3002"),
        ("REB3004_3_unfixed_reference", "epsilon_Bv_unfixed_reference", "MISSING_SOURCE_BACKED_UPPER_BOUND", "conditional selector only; staged by 3003"),
        ("REB3004_4_projector_boundary", "epsilon_Bv_projector_boundary", "MISSING_SOURCE_BACKED_UPPER_BOUND", "3004 finds conditional chain-map/silence route only; no theorem-zero or finite commutator value"),
        ("REB3004_5_Bv_remainder", "epsilon_Bv_remainder_after_3004", "MISSING_MREF_DENOMINATOR_BOUND", "projector-boundary is boxed as residual; denominator/normalization is now the sharp Bv bottleneck"),
        ("REB3004_6_kernel", "epsilon_kernel_charge_public_SRNG_rebased_3004", "MISSING_THETA_PARENT_QV_BV_REMAINDER_CV_ZERO_FLUX_MREF", "Bv narrower but full kernel charge remains open"),
    ]
    return [
        base(
            {
                "rebase_id": rebase_id,
                "symbol": symbol,
                "current_value": current_value,
                "status": status,
            }
        )
        for rebase_id, symbol, current_value, status in data
    ]


def gate_rows() -> list[dict[str, Any]]:
    data = [
        ("GATE3004_0_sources", "3004 source anchors exist", "PASS", True, False, "all required source anchors are present"),
        ("GATE3004_1_projector_zero", "epsilon_Bv_projector_boundary=0 can be promoted", "CONDITIONAL_ONLY_FAIL_CLOSED", False, False, "Pi_M parent ownership, same domain, variation ownership, chain-map, exterior silence and M_ref are unsigned"),
        ("GATE3004_2_finite_commutator", "finite projector-boundary bound exists", "BLOCKED_NONCLAIM", False, False, "I_commutator, delta Pi_M boundary, projector stress, R_eq and M_ref are missing"),
        ("GATE3004_3_no_observed_GM_import", "no observed-GM calibration used as denominator", "PASS_AS_GUARDRAIL", True, False, "3004 keeps same-frame M_ref/M_H_ref missing instead of importing orbital GM"),
        ("GATE3004_4_full_Bv_zero", "epsilon_Bv_ambiguity=0", "FAIL_CLOSED", False, False, "M_ref/denominator and earlier residual debts remain"),
        ("GATE3004_5_local_claims", "local GR/Newton/PPN/WEP/R10 claim allowed", "FAIL_CLOSED", False, False, "kernel charge and Bv denominator are still open"),
    ]
    return [
        base(
            {
                "gate_id": gate_id,
                "gate": gate,
                "gate_status": gate_status,
                "condition_passed": condition_passed,
                "promotion_allowed_now": promotion_allowed_now,
                "reason": reason,
            }
        )
        for gate_id, gate, gate_status, condition_passed, promotion_allowed_now, reason in data
    ]


def decision_rows() -> list[dict[str, Any]]:
    data = [
        (
            "DEC3004_0_keep_product_rule",
            "Retain the projector product-rule obstruction explicitly.",
            "[d,Pi_M]J_H and (delta Pi_M)J_H are real terms unless parent chain-map/variation silence is signed.",
            "commutator and projector-variation rows stay in the residual bill",
        ),
        (
            "DEC3004_1_no_zero",
            "Do not promote projector-boundary silence.",
            "Current MTS lacks parent projector ownership, same-domain lock, physical-current chain-map, exterior silence, projector stress theorem and M_ref.",
            "stage source-ready bound rows instead",
        ),
        (
            "DEC3004_2_no_value",
            "Do not compute a finite projector-boundary value.",
            "All numerator pieces and the same-frame denominator are missing; no cancellation or observed-GM import is allowed.",
            "all finite-value rows remain valid_for_claim=false",
        ),
        (
            "DEC3004_3_next",
            "Move to M_ref/M_H_ref denominator ownership next.",
            "After exact, tau/surface, corner/topology, unfixed-reference and projector-boundary routes are explicit, the denominator is the common bottleneck for scoring any Bv envelope.",
            "3005 should attack same-frame positive M_ref/M_H_ref without circular orbital-GM calibration",
        ),
    ]
    return [
        base(
            {
                "decision_id": decision_id,
                "decision": decision,
                "rationale": rationale,
                "next_effect": next_effect,
            }
        )
        for decision_id, decision, rationale, next_effect in data
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        base(
            {
                "next_id": "NEXT3004_0_3005",
                "priority": "selected_primary",
                "target_doc": "3005-Y5-R2FR-Mref-denominator-ownership-or-Bv-envelope-scoreability-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_Mref_denominator_ownership_or_Bv_envelope_scoreability_under_AX1090_3005.py",
                "mission": "Attack M_ref/M_H_ref denominator ownership: prove a positive same-frame parent Hamiltonian/reference denominator for Bv residuals without observed-GM import, or stage denominator acquisition rows with units/source paths.",
                "success_condition": "Bv residual envelope gains a parent-owned positive denominator or a source-ready denominator acquisition ledger; no local-GR claim unless numerator debts also close",
                "fallback_if_fail": "demote Bv scoring to explicit residual closure and move upstream to parent theta/Q_tau/H_tau extraction",
                "guardrails": "no full Bv zero claim; no epsilon_kernel_charge claim; no local-GR/Newton/PPN/WEP/R10 claim; no GitHub; no formalization-workbench edits",
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        base(
            {
                "copy_id": copy_id,
                "path": str(path),
                "path_exists": path.exists(),
                "row_count": len(rows(path)),
                "csv_parse_ok": csv_ok(path),
                "claim_flags_present": any(boolish(row.get("valid_for_claim")) or boolish(row.get("claim_allowed")) for row in rows(path)),
            }
        )
        for copy_id, path in BRANCH_OUTPUTS.items()
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    commutator: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    rebase: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    branches: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
    generated_rows = sources + audit + commutator + bounds + rebase + gates + decisions + next_target + branches
    targeted_formalization_hits = []
    if FORMALIZATION.exists():
        patterns = [
            "*Y5_R2FR_3004*",
            "*3004-Y5-R2FR*",
            "*projector_boundary_Bv_silence_3004*",
            "*epsilon_Bv_projector_boundary_bound_rows_3004*",
            "*JR3004_MREF_DENOMINATOR*",
        ]
        for pattern in patterns:
            targeted_formalization_hits.extend(FORMALIZATION.rglob(pattern))

    checks = [
        ("VAL3004_00_sources_exist", all(boolish(row["path_exists"]) for row in sources), "every cited source path exists", True),
        ("VAL3004_01_source_anchors", all(boolish(row["anchors_found"]) for row in sources), "every source has required anchors", True),
        ("VAL3004_02_projector_zero_not_promoted", any(row["audit_id"] == "PBA3004_9_verdict" for row in audit) and not any(boolish(row["theorem_zero_now"]) for row in audit), "projector silence remains conditional, not theorem-zero", True),
        ("VAL3004_03_missing_projector_clauses", all(expected in {row["current_status"] for row in audit} for expected in {"PARENT_PROJECTOR_NOT_DERIVED", "MISSING_SAME_DOMAIN_HOMOLOGY_LOCK", "MISSING_PROJECTOR_VARIATION_COMMUTATOR_ZERO", "MISSING_EXTERIOR_SILENCE_THEOREM", "MISSING_TAU_MHREF_LOCK", "FAIL_CURRENT_CLAIM"}), "projector audit preserves missing ownership/domain/stress clauses", True),
        ("VAL3004_04_commutator_rows_nonclaim", len(commutator) == 7 and all(not boolish(row["valid_for_claim"]) and not boolish(row["claim_allowed"]) for row in commutator), "Pi_M commutator rows are staged and nonclaim", True),
        ("VAL3004_05_bounds_nonclaim", len(bounds) == 6 and all(not boolish(row["valid_for_claim"]) and not boolish(row["claim_allowed"]) for row in bounds), "epsilon_Bv_projector_boundary bound rows are nonclaim", True),
        ("VAL3004_06_no_finite_values_fabricated", all("MISSING" in str(row.get("current_value", "")) or str(row.get("current_value")) == "NOT_ALLOWED_AS_VALUE" for row in bounds + commutator), "no finite projector-boundary value fabricated", True),
        ("VAL3004_07_local_claims_blocked", all(row["promotion_allowed_now"] is False for row in gates), "no local GR/Newton/PPN/WEP/R10 promotion allowed", True),
        ("VAL3004_08_next_target_Mref", len(next_target) == 1 and "M_ref" in next_target[0]["mission"], "3005 selects M_ref/M_H_ref denominator ownership next", True),
        ("VAL3004_09_branch_copies", len(branches) == 3 and all(boolish(row["path_exists"]) and boolish(row["csv_parse_ok"]) for row in branches) and not any(boolish(row["claim_flags_present"]) for row in branches), "branch copies exist, parse, and carry no claim flags", True),
        ("VAL3004_10_csv_parse", all(csv_ok(path) for path in OUTPUTS.values() if path.suffix == ".csv"), "all 3004 CSV outputs parse cleanly", True),
        ("VAL3004_11_paths_under_post_checkpoint", all(under(path, ROOT) for path in output_paths), "all generated outputs are under post-checkpoint-work", True),
        ("VAL3004_12_formalization_untouched", len(targeted_formalization_hits) == 0, "no targeted 3004 files exist under formalization-workbench", True),
        ("VAL3004_13_no_claim_flags", not any(boolish(row.get("valid_for_claim")) or boolish(row.get("claim_allowed")) for row in generated_rows), "all generated rows remain valid_for_claim=false and claim_allowed=false", True),
    ]
    preliminary = [
        base({"validation_id": validation_id, "passed": passed, "detail": detail, "required": required})
        for validation_id, passed, detail, required in checks
    ]
    overall = all(boolish(row["passed"]) for row in preliminary if boolish(row["required"]))
    preliminary.append(
        base(
            {
                "validation_id": "VAL3004_OVERALL",
                "passed": overall,
                "detail": "3004 refuses projector-boundary zero/value promotion, stages Pi_M commutator/projector-stress rows, and selects M_ref denominator ownership next",
                "required": True,
            }
        )
    )
    return preliminary


def write_doc(
    sources: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    commutator: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    rebase: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    branches: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    content = f"""# 3004 - Y5/R2FR Projector-Boundary Bv Silence Or PiM Boundary Commutator Bound Under AX1090

Status: `Y5_R2FR_3004_projector_boundary_conditional_chainmap_zero_not_promoted_commutator_rows_staged_3005_next`

Generated: `{RUN_UTC}`

## Current Verdict

3004 attacks `epsilon_Bv_projector_boundary`, the term that would vanish only if the mass/source projector is parent-owned, lives on the same boundary/domain as `q`, `Q_tau`, `J_H` and readout, and commutes with the exterior differential/current chain.

The useful mathematical route is exact: if `Pi_M` is a fixed parent chain-map on the physical Hilbert-current complex, `delta Pi_M=0` or is Ward-owned, the annulus is exterior-silent, and the same-frame denominator is positive, then `[d,Pi_M]J_H=0` and the projector-boundary leakage vanishes.

Current MTS does not yet sign those clauses. So this checkpoint refuses a projector-boundary zero and refuses a finite value. The gain is that the dangerous terms are now named: commutator annulus, projector-variation surface term, projector stress, mass-current mismatch, and flux drift.

## Source Register

{md_table(sources, ["source_id", "path_exists", "anchors_found", "missing_anchors", "role"])}

## Projector-Boundary Silence Audit

{md_table(audit, ["audit_id", "projector_clause", "current_status", "failure_mode", "source_anchors"])}

## Pi_M Boundary Commutator Rows

{md_table(commutator, ["row_id", "quantity", "bound_interface", "current_value", "status", "source_anchors"])}

## epsilon_Bv Projector-Boundary Bound Rows

{md_table(bounds, ["bound_id", "symbol", "bound_interface", "current_value", "status", "source_anchors"])}

## Bv Rebase After 3004

{md_table(rebase, ["rebase_id", "symbol", "current_value", "status"])}

## Promotion Gates

{md_table(gates, ["gate_id", "gate", "gate_status", "condition_passed", "promotion_allowed_now", "reason"])}

## Decision Ledger

{md_table(decisions, ["decision_id", "decision", "rationale", "next_effect"])}

## Next Target

{md_table(next_target, ["next_id", "target_doc", "mission", "success_condition", "guardrails"])}

## Branch Copies

{md_table(branches, ["copy_id", "path", "path_exists", "row_count", "csv_parse_ok", "claim_flags_present"])}

## Validation

{md_table(validation, ["validation_id", "passed", "detail", "required"])}

## Plain-English Takeaway

This is the projector version of the same discipline: no magic eraser. If `Pi_M` is just a readout choice, it cannot be used to delete source charge. If it is a parent object with chain-map, domain, stress and flux ownership, then it can become a real theorem. Right now we have the exact contract, not the signed theorem, so the route stays residual-only.

## Forbidden Claims From 3004

- `epsilon_Bv_projector_boundary=0`.
- `[d,Pi_M]J_H=0`.
- `(delta Pi_M)J_H=0`.
- `epsilon_projector_symplectic_abs` has a finite sourced value.
- `epsilon_Bv_ambiguity=0`.
- `epsilon_kernel_charge_public_SRNG=0`.
- Local GR/Newton/PPN/WEP/R10 pass.
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    sources = source_rows()
    audit = audit_rows()
    commutator = commutator_rows()
    bounds = bound_rows()
    rebase = rebase_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["audit"], audit)
    write_csv(OUTPUTS["commutator"], commutator)
    write_csv(OUTPUTS["bounds"], bounds)
    write_csv(OUTPUTS["rebase"], rebase)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    shutil.copyfile(OUTPUTS["audit"], BRANCH_OUTPUTS["audit_copy"])
    shutil.copyfile(OUTPUTS["bounds"], BRANCH_OUTPUTS["bounds_copy"])
    shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)
    validation = validation_rows(sources, audit, commutator, bounds, rebase, gates, decisions, next_target, branches)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, audit, commutator, bounds, rebase, gates, decisions, next_target, branches, validation)

    overall = next(row for row in validation if row["validation_id"] == "VAL3004_OVERALL")
    if not boolish(overall["passed"]):
        raise SystemExit("3004 validation failed; see P8_Y5_BRR545_3004_VALIDATION.csv")

    print(f"wrote {DOC}")
    print(f"validation {overall['passed']}: {overall['detail']}")


if __name__ == "__main__":
    main()

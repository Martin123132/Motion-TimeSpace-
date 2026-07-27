from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

DOC = ROOT / "2838-Y5-R2FR-second-class-auxiliary-block-parent-signature-or-finite-RAB-residual-under-AX1090.md"

SRC_2837_NEXT = RESIDUALS / "P8_Y5_R2FR_2837_NEXT_TARGET.csv"
SRC_2837_SELECTOR = RESIDUALS / "P8_Y5_R2FR_2837_RAB_OWNERSHIP_SELECTOR.csv"
SRC_2837_FINITE = RESIDUALS / "P8_Y5_R2FR_2837_FINITE_RESIDUAL_ACQUISITION_CARRYOVER_NONCLAIM.csv"
SRC_2260_CONTRACT = RESIDUALS / "P8_Y5_PARENT_QLOC_2260_PARENT_PROTECTION_CONTRACT.csv"
SRC_2260_THEOREM = RESIDUALS / "P8_Y5_PARENT_QLOC_2260_CONDITIONAL_THEOREM.csv"
SRC_2261_PRIMITIVE = BETA_DOCS / "RAB_PARENT_PRIMITIVE_DERIVATION_AUDIT_2261_NONCLAIM.csv"
SRC_2288_AUX = BETA_DOCS / "RAB_AUXILIARY_OR_FINITE_ZQ_2288_NONCLAIM.csv"
SRC_2236_FALLBACK = BETA_DOCS / "RAB_AUXILIARY_GRAMMAR_2236_NONCLAIM.csv"
SRC_2259 = ROOT / "2259-Y5-R2FR-RAB-compatibility-object-bridge-or-residual-demotion.md"
SRC_2240 = ROOT / "2240-Y5-R2FR-RAB-parent-protection-contract-or-live-finite-ZR-source-acquisition.md"
SRC_10 = ROOT / "10-observer-map-symplectic-contract.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2838_SOURCE_REGISTER.csv",
    "signature": RESIDUALS / "P8_Y5_R2FR_2838_SECOND_CLASS_SIGNATURE_AUDIT.csv",
    "calculus": RESIDUALS / "P8_Y5_R2FR_2838_AUXILIARY_ELIMINATION_CALCULUS.csv",
    "failure_map": RESIDUALS / "P8_Y5_R2FR_2838_FAILURE_TO_FINITE_RESIDUAL_MAP.csv",
    "finite_equation": RESIDUALS / "P8_Y5_R2FR_2838_FINITE_RAB_RESIDUAL_EQUATION_NONCLAIM.csv",
    "finite_rows": RESIDUALS / "P8_Y5_R2FR_2838_FINITE_RESIDUAL_ACQUISITION_ROWS_NONCLAIM.csv",
    "guards": RESIDUALS / "P8_Y5_R2FR_2838_GUARDS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2838_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2838_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2838_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2838_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2838_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "finite_equation_copy": LOCAL_BOUNDS / "RAB_finite_residual_equation_2838_NONCLAIM.csv",
    "signature_copy": SOURCE_WEIGHT / "RAB_second_class_signature_audit_2838_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2838_finite_RAB_residual_or_parent_signature_NEXT.csv",
    "portable_decision": BETA_DOCS / "RAB_SECOND_CLASS_SIGNATURE_OR_FINITE_RESIDUAL_2838_NONCLAIM.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    paths = {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["score_ready"] = False
    row["valid_prediction_row"] = False
    row["valid_for_claim"] = False
    row["claim_allowed"] = False
    row["generated_utc"] = ts()
    return row


def source_row(source_id: str, path: Path, anchors: str, role: str) -> dict[str, Any]:
    text = read_text(path)
    anchor_list = [anchor for anchor in anchors.split(";") if anchor]
    missing = [anchor for anchor in anchor_list if anchor not in text]
    return nonclaim(
        {
            "source_id": source_id,
            "source_path": str(path),
            "anchors": anchors,
            "role": role,
            "path_exists": path.exists(),
            "anchors_found": not missing,
            "missing_anchors": ";".join(missing),
        }
    )


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2838_0_2837_next", SRC_2837_NEXT, "NEXT2837_0_2838", "2837 selected this parent-signature target"),
        ("SRC2838_1_2837_selector", SRC_2837_SELECTOR, "SEL2837_1_second_class_auxiliary;SEL2837_3_physical_finite_field;SEL2837_4_current_verdict", "2837 route selector"),
        ("SRC2838_2_2837_finite", SRC_2837_FINITE, "FIN2837_0_ZR;FIN2837_4_projection;FIN2837_5_source_vector", "2837 finite residual carryover"),
        ("SRC2838_3_2260_contract", SRC_2260_CONTRACT, "CON2260_1_action_image;CON2260_5_operator_exclusion;CON2260_6_joint_contract", "2260 parent protection contract"),
        ("SRC2838_4_2260_theorem", SRC_2260_THEOREM, "THM2260_0_statement;THM2260_1_variation;THM2260_2_operator;THM2260_3_verdict", "2260 conditional second-class theorem"),
        ("SRC2838_5_2261_primitive", SRC_2261_PRIMITIVE, "CON2261_1_action_image;CON2261_2_matter_functor;CON2261_6_joint_contract", "2261 primitive derivation audit"),
        ("SRC2838_6_2288_aux", SRC_2288_AUX, "AUX2288_2_second_class;AUX2288_3_finite_escape", "2288 auxiliary/finite selector"),
        ("SRC2838_7_2236_fallback", SRC_2236_FALLBACK, "FALL2236_0_ZR;FALL2236_1_MR2;FALL2236_2_JR;FALL2236_3_BR;FALL2236_4_projection", "2236 finite coefficient fallback"),
        ("SRC2838_8_2259_doc", SRC_2259, "SC2259_0_parent_block;SC2259_5_total;DM2259_5_projection", "2259 second-class contract and demotion queue"),
        ("SRC2838_9_2240_doc", SRC_2240, "CON2240_1_action_image;THM2240_1_variation;ACQ2240_1_ZR", "2240 parent protection and source queue"),
        ("SRC2838_10_observer_contract", SRC_10, "R_AB = ln(T^2 S)", "observer-map definition of R_AB"),
    ]
    return [source_row(*spec) for spec in specs]


def signature_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "SIG2838_0_parent_field_status",
            "typed parent field status",
            "R_AB must be parent-typed as auxiliary/constraint data before matter/readout, not inferred from the desired local-GR endpoint.",
            "PARTIAL_SUPPORT_NOT_DERIVED",
            "2261 says psi/emergent metric exist but no primitive functor identifies R_AB as auxiliary rather than physical observer-cell strain.",
            "CON2261_0_parent_sorts;SEL2837_4_current_verdict",
            False,
        ),
        (
            "SIG2838_1_action_image",
            "algebraic auxiliary action image",
            "Parent action must contain only S_aux = integral mu_parent Lambda_R*(R_AB-C_AB[Q,theta,top]) for the R_AB block.",
            "NOT_PARENT_SIGNED",
            "2261 finds no displayed primitive action containing Lambda_R, C_AB[Q], or a no-derivative algebraic R_AB block.",
            "CON2261_1_action_image;CON2260_1_action_image;SC2259_0_parent_block",
            False,
        ),
        (
            "SIG2838_2_no_derivative_grammar",
            "no derivative or vertical-metric constructors",
            "ParentGenerate must forbid D R_AB, D Lambda_R, G_vert, nabla_vert, boundary derivative terms, and generated kinetic/mass terms.",
            "ABSENCE_NOT_GRAMMAR_PROOF",
            "absence of explicit R_AB derivatives is weaker than a typed grammar theorem excluding generated derivative operators.",
            "CON2261_5_operator_exclusion;THM2260_2_operator;FALL2236_0_ZR",
            False,
        ),
        (
            "SIG2838_3_source_descent",
            "matter/source descent",
            "S_matter must descend through Q and Psi only, so delta S_matter/delta R_AB=0 after the actual observed coframe map is fixed.",
            "CONDITIONAL_KERNEL_NOT_ACTIVATED",
            "if R_AB changes the observed coframe, matter varies with it; the chain-rule zero only works after actual R_AB verticality/basicity is proved.",
            "CON2261_2_matter_functor;SEL2837_1_second_class_auxiliary",
            False,
        ),
        (
            "SIG2838_4_boundary_silence",
            "boundary/corner descent",
            "Boundary data must descend through Q-boundary variables only, giving B_R=Pi_R=Q_R=0.",
            "NOT_DERIVED",
            "no primitive boundary generator or exact R_AB edge-current cancellation is displayed in the cited parent material.",
            "CON2261_3_boundary_functor;CON2260_3_boundary_functor;FALL2236_3_BR",
            False,
        ),
        (
            "SIG2838_5_readout_stability",
            "readout/effective closure",
            "Elimination must commute with readout/coarse-graining and must not regenerate b_R, d_R, endpoint, tau, or transfer channels.",
            "GUARDRAIL_NOT_THEOREM",
            "same-coframe guardrails forbid cheating but do not prove coarse-graining cannot regenerate finite R_AB channels.",
            "CON2261_4_readout_closure;CON2260_4_readout_closure;FALL2236_4_projection",
            False,
        ),
        (
            "SIG2838_6_joint_signature",
            "joint second-class parent signature",
            "All clauses must close as one parent-owned block before any J_R=0, Pi_R=0, Z_R=0, q_R=0, local GR or Newton claim.",
            "FAILED_CURRENT_PARENT_SIGNATURE",
            "the common missing premise is still R_AB ownership from primitives; pieces remain conditional/guardrail-level.",
            "CON2261_6_joint_contract;CON2260_6_joint_contract;THM2260_3_verdict",
            False,
        ),
    ]
    return [
        nonclaim(
            {
                "signature_id": row_id,
                "clause": clause,
                "required_statement": statement,
                "current_status": status,
                "proof_or_blocker": blocker,
                "source_anchors": anchors,
                "parent_signed": signed,
                "theorem_zero": False,
                "control_only": True,
            }
        )
        for row_id, clause, statement, status, blocker, anchors, signed in specs
    ]


def calculus_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "CALC2838_0_aux_action",
            "S_aux = integral mu Lambda_R (R_AB-C_AB[Q])",
            "This is the minimal second-class block needed to eliminate R_AB algebraically.",
            "FORMAL_OBJECT_CONDITIONAL",
            "only valid if the parent action image signs this block rather than us appending it as closure.",
        ),
        (
            "CALC2838_1_delta_lambda",
            "delta S/delta Lambda_R = R_AB-C_AB[Q] = 0",
            "The multiplier equation fixes the compatibility surface.",
            "FORMAL_PASS_WITHIN_CONTRACT",
            "does not prove the block exists in the parent action.",
        ),
        (
            "CALC2838_2_delta_R",
            "delta S/delta R_AB = Lambda_R + J_R + Pi_R + readout_regen + D_operator_terms = 0",
            "The R_AB equation solves Lambda_R only after source, boundary, readout, and derivative terms vanish.",
            "FORMAL_PASS_WITHIN_CONTRACT",
            "this is exactly where the missing protections enter; one surviving term makes Lambda_R finite.",
        ),
        (
            "CALC2838_3_exact_zero_case",
            "if J_R=Pi_R=readout_regen=D_operator_terms=0, then Lambda_R=0 and R_AB=C_AB[Q]",
            "This is the genuine local-GR route: not a plateau axiom, but algebraic elimination before readout.",
            "EXACT_IF_PARENT_SIGNATURE_SIGNED",
            "not claimable because parent signature and protections are not primitive-derived.",
        ),
        (
            "CALC2838_4_finite_case",
            "if any term survives, Lambda_R=-(J_R+Pi_R+readout_regen+D_operator_terms)",
            "The branch becomes a finite residual field/source problem rather than a zero theorem.",
            "LIVE_FALLBACK",
            "requires source-backed coefficients and arena projections before scoring.",
        ),
    ]
    return [
        nonclaim(
            {
                "calculus_id": row_id,
                "equation_or_step": equation,
                "meaning": meaning,
                "status": status,
                "claim_blocker": blocker,
                "control_only": True,
            }
        )
        for row_id, equation, meaning, status, blocker in specs
    ]


def failure_map_rows() -> list[dict[str, Any]]:
    specs = [
        ("FAIL2838_0_action_image", "algebraic parent block unsigned", "R_AB may be physical or closure-inserted", "must carry finite Z_R/M_R^2/J_R/B_R/projection rows", "SEL2837_3_physical_finite_field;FALL2236_0_ZR"),
        ("FAIL2838_1_operator", "no-derivative grammar unsigned", "Z_R or mixed derivative operators may survive", "source Z_R/Z_RR/Z_RY and Green-kernel normalization", "THM2260_2_operator;FALL2236_0_ZR"),
        ("FAIL2838_2_source", "matter descent unsigned", "J_R may source R_AB through observed coframe/matter labels", "source finite J_R or prove actual coframe basicity before matter coupling", "CON2261_2_matter_functor;FALL2236_2_JR"),
        ("FAIL2838_3_boundary", "boundary descent unsigned", "Pi_R or Q_R can carry exterior reciprocal hair", "source finite B_R/Pi_R/Q_R or prove no-edge-current theorem", "CON2261_3_boundary_functor;FALL2236_3_BR"),
        ("FAIL2838_4_readout", "readout stability unsigned", "tau/b_R/d_R/endpoint leakage can regenerate local residuals", "source arena projections tau_R10/tau_PPN/tau_clock/tau_orbital", "CON2261_4_readout_closure;FALL2236_4_projection"),
        ("FAIL2838_5_joint", "any one protection fails", "local GR reduction is not theorem-zero", "route to finite residual equation and nonclaim acquisition pack", "CON2261_6_joint_contract;SEL2837_4_current_verdict"),
    ]
    return [
        nonclaim(
            {
                "failure_id": row_id,
                "failed_clause": failed,
                "residual_meaning": meaning,
                "required_fallback": fallback,
                "source_anchors": anchors,
                "fallback_active": True,
                "control_only": True,
            }
        )
        for row_id, failed, meaning, fallback, anchors in specs
    ]


def finite_equation_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "FEQ2838_0_normal_form",
            "E_R^finite := -Div(Z_R Grad R_AB) + M_R^2 (R_AB-C_AB[Q]) + J_R + Pi_R + R_readout = 0",
            "canonical nonclaim finite residual normal form if the auxiliary theorem-zero route fails",
            "symbolic_no_numeric_values",
            "Z_R,M_R^2,J_R,Pi_R,R_readout,C_AB normalization",
        ),
        (
            "FEQ2838_1_green_solution",
            "R_AB-C_AB = G_R * (J_R + Pi_R + R_readout) plus boundary data",
            "defines the Green-kernel test object once Z_R/M_R^2/boundary conditions are sourced",
            "symbolic_no_numeric_values",
            "G_R normalization, boundary conditions, source normalization",
        ),
        (
            "FEQ2838_2_range",
            "ell_R = sqrt(Z_R/M_R^2) when Z_R>0 and M_R^2>0",
            "range/suppression scale for local tests; undefined until both parent coefficients are sourced",
            "symbolic_no_numeric_values",
            "Z_R, M_R^2, units, sign conditions",
        ),
        (
            "FEQ2838_3_zero_limit",
            "second-class theorem-zero is recovered only by parent signature, not by sending coefficients by hand",
            "prevents hiding an empirical failure inside arbitrary prior limits",
            "guardrail",
            "parent-signed auxiliary action image and protections",
        ),
    ]
    return [
        nonclaim(
            {
                "equation_id": row_id,
                "equation": equation,
                "meaning": meaning,
                "status": status,
                "required_inputs": required,
                "numeric_value_present": False,
                "source_backed": False,
                "control_only": True,
            }
        )
        for row_id, equation, meaning, status, required in specs
    ]


def finite_row_specs() -> list[dict[str, Any]]:
    specs = [
        ("ACQ2838_0_ZR", "Z_R", "finite R_AB gradient/stiffness coefficient", "internal_theory", "MISSING_THEOREM_ZERO_OR_SOURCE_BACKED_VALUE", "R10;PPN;clock;orbital", "FALL2236_0_ZR;FIN2837_0_ZR"),
        ("ACQ2838_1_MR2", "M_R^2", "R_AB mass-gap/screening Hessian", "internal_theory", "MISSING_PARENT_HESSIAN_OR_RANGE_SCALE", "R10;clock;orbital", "FALL2236_1_MR2;FIN2837_1_MR2"),
        ("ACQ2838_2_JR", "J_R", "direct matter/body source coupling", "internal_theory", "MISSING_MATTER_DESCENT_ZERO_OR_FINITE_COUPLING", "WEP;PPN;R10;local_GR", "FALL2236_2_JR;FIN2837_2_JR"),
        ("ACQ2838_3_PiR", "Pi_R/B_R/Q_R", "boundary/corner reciprocal charge", "internal_theory", "MISSING_BOUNDARY_NO_CHARGE_OR_FINITE_FLUX", "R10;PPN;orbital", "FALL2236_3_BR;FIN2837_3_BR"),
        ("ACQ2838_4_Rreadout", "R_readout/tau", "readout/coarse-graining regenerated residual", "mixed_internal_external", "MISSING_READOUT_STABILITY_OR_ARENA_PROJECTION", "R10;PPN;clock;orbital", "FALL2236_4_projection;FIN2837_4_projection"),
        ("ACQ2838_5_CAB", "C_AB[Q,theta,top]", "compatibility target map and normalization", "internal_theory", "MISSING_PARENT_NORMALIZATION", "all_local_arenas", "CON2260_1_action_image;R_AB = ln(T^2 S)"),
    ]
    return [
        nonclaim(
            {
                "acquisition_id": row_id,
                "symbol": symbol,
                "meaning": meaning,
                "source_class": source_class,
                "current_status": status,
                "observable_link": observable,
                "source_anchors": anchors,
                "numeric_value_present": False,
                "source_backed": False,
                "accepted_ready": False,
                "control_only": True,
            }
        )
        for row_id, symbol, meaning, source_class, status, observable, anchors in specs
    ]


def guard_rows() -> list[dict[str, Any]]:
    specs = [
        ("GUARD2838_0_no_closure_insert", "do not append Lambda_R(R_AB-C_AB) as closure", "the block must be parent-generated, not goal-generated", "signature remains failed unless source action signs it"),
        ("GUARD2838_1_no_partial_zero", "do not spend partial zero credit", "source, boundary, readout, and operator protections are coupled", "one unsigned protection keeps finite residual branch live"),
        ("GUARD2838_2_no_first_class_revival", "do not revive first-class gauge language", "2837/2288 rejected current first-class promotion", "second-class means algebraic elimination, not gauge magic"),
        ("GUARD2838_3_no_prior_edge_hiding", "do not set finite coefficients to zero by prior choice", "zero limit must be theorem-signed or empirically bounded", "finite rows stay nonclaim"),
        ("GUARD2838_4_no_local_claim", "do not claim local GR/Newton", "R_AB ownership and finite residual projections remain open", "claim gates remain closed"),
    ]
    return [
        nonclaim(
            {
                "guard_id": row_id,
                "guard": guard,
                "because": because,
                "effect": effect,
                "guard_active": True,
                "control_only": True,
            }
        )
        for row_id, guard, because, effect in specs
    ]


def gate_rows(rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    sources_ok = all(row["path_exists"] and row["anchors_found"] for row in rows["sources"])
    parent_signed = all(row["parent_signed"] for row in rows["signature"])
    finite_nonclaim = all((not row["numeric_value_present"]) and (not row["source_backed"]) for row in rows["finite_rows"])
    guards_active = all(row["guard_active"] for row in rows["guards"])
    specs = [
        ("GATE2838_0_sources", "all cited local source anchors resolve", sources_ok, "PASS_INTERNAL_NONCLAIM" if sources_ok else "BLOCKED", "audit trail is reproducible"),
        ("GATE2838_1_parent_signature", "second-class auxiliary block is parent-signed", parent_signed, "BLOCKED", "action image, operator exclusion, source, boundary, readout and joint ownership remain unsigned"),
        ("GATE2838_2_exact_zero", "J_R=Pi_R=Q_R=Z_R=readout_regen=0 theorem-zero", False, "BLOCKED", "zero only follows if the blocked parent signature closes"),
        ("GATE2838_3_finite_residual_pack", "finite residual acquisition pack is staged", finite_nonclaim, "PASS_INTERNAL_NONCLAIM" if finite_nonclaim else "BLOCKED", "rows exist but contain no numeric/source-backed values"),
        ("GATE2838_4_guardrails", "guardrails are active", guards_active, "PASS_GUARDRAIL" if guards_active else "BLOCKED", "no closure insertion, partial zero, first-class revival, or prior-edge hiding"),
        ("GATE2838_5_local_gr_newton", "local GR/Newton reduction is derived", False, "BLOCKED", "neither exact auxiliary zero nor finite residual bounds are claim-ready"),
    ]
    return [
        nonclaim(
            {
                "claim_gate_id": row_id,
                "claim": claim,
                "gate_passed": passed,
                "status": status,
                "reason": reason,
            }
        )
        for row_id, claim, passed, status, reason in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DEC2838_0_signature",
            "Do not claim second-class parent signature.",
            "FAILED_CURRENT_PARENT_SIGNATURE",
            "the exact algebra works only inside an unsigned contract; 2261 still blocks action image, source, boundary, readout and operator closure.",
            "promote finite residual normal form as the honest fallback",
        ),
        (
            "DEC2838_1_calculus",
            "Keep the auxiliary theorem as an exact conditional.",
            "EXACT_IF_SIGNED",
            "E_Lambda and E_R give a real algebraic elimination theorem if all protections close jointly.",
            "do not throw away the route; keep it as a parent-action contract requirement",
        ),
        (
            "DEC2838_2_finite",
            "Promote finite R_AB residual equation to the next nonclaim work object.",
            "FINITE_RESIDUAL_BRANCH_SELECTED_NONCLAIM",
            "if any protection fails, the residual must be bounded or sourced rather than hidden.",
            "derive/source Z_R, M_R^2, J_R, Pi_R and tau projections",
        ),
    ]
    return [
        nonclaim(
            {
                "decision_id": row_id,
                "decision": decision,
                "result": result,
                "because": because,
                "next_action": next_action,
            }
        )
        for row_id, decision, result, because, next_action in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2838_0_2839",
                "status": "selected_primary",
                "target_doc": "2839-Y5-R2FR-finite-RAB-residual-green-kernel-normalization-or-first-source-backed-row-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_finite_RAB_residual_green_kernel_normalization_or_first_source_backed_row_under_AX1090_2839.py",
                "mission": "normalize the finite R_AB residual Green-kernel equation, then either derive a theorem-zero for one component or stage the first source-backed nonclaim coefficient/projection row",
                "acceptance": "must preserve the exact auxiliary theorem as conditional, keep local-GR claims blocked, and require units/source paths/normalization before any finite residual score",
                "forbidden": "do not set coefficients to zero by preference; do not use GR target behavior as a premise; do not score placeholder rows",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("BR2838_0_finite_equation", OUTPUTS["finite_equation"], BRANCH_OUTPUTS["finite_equation_copy"], "local-bounds copy of finite RAB residual equation"),
        ("BR2838_1_signature", OUTPUTS["signature"], BRANCH_OUTPUTS["signature_copy"], "source-weight copy of second-class signature audit"),
        ("BR2838_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue for finite residual normalization or parent signature re-entry"),
        ("BR2838_3_decision", OUTPUTS["decision"], BRANCH_OUTPUTS["portable_decision"], "portable beta-source decision ledger"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_table, copy_path, purpose in specs:
        copy_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_table, copy_path)
        rows.append(
            nonclaim(
                {
                    "copy_id": copy_id,
                    "source_table": str(source_table),
                    "copy_path": str(copy_path),
                    "purpose": purpose,
                    "exists": copy_path.exists(),
                }
            )
        )
    return rows


def iter_cited_paths(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[Path]:
    keys = {"source_path", "source_table", "copy_path"}
    paths: list[Path] = []
    for rows in rows_by_name.values():
        for row in rows:
            for key in keys:
                value = row.get(key)
                if value is None:
                    continue
                for token in str(value).split(";"):
                    item = token.strip()
                    if not item or item.startswith("http") or item.startswith("MISSING_"):
                        continue
                    path = Path(item)
                    if not path.is_absolute():
                        path = ROOT / item
                    paths.append(path)
    return paths


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for name, rows in rows_by_name.items():
        if name == "validation":
            continue
        for row in rows:
            for key in ("score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if str(row.get(key, "")).lower() == "true":
                    return False
            for key in ("parent_signed", "theorem_zero", "source_backed", "accepted_ready"):
                if str(row.get(key, "")).lower() == "true":
                    return False
    return True


def no_numeric_predictions(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    numeric_keys = {
        "numeric_value",
        "predicted_value",
        "coefficient_value",
        "alpha_bound",
        "lambda_value",
        "accepted_value",
        "raw_value",
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key, value in row.items():
                if key in numeric_keys and str(value).strip():
                    return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    start = SCRIPT_START_UTC.timestamp()
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        try:
            if path.stat().st_mtime >= start:
                return False
        except OSError:
            return False
    return True


def under_root(paths: list[Path]) -> bool:
    root_text = str(ROOT.resolve()).lower()
    return all(str(path.resolve()).lower().startswith(root_text) for path in paths)


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_paths = [path for path in OUTPUTS.values() if path != OUTPUTS["validation"]]
    branch_paths = list(BRANCH_OUTPUTS.values())
    cited_paths = iter_cited_paths(rows_by_name)
    checks = [
        ("VAL2838_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2838_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2838_2_signature_not_signed", not any(row["parent_signed"] for row in rows_by_name["signature"]), "second-class signature remains unsigned"),
        ("VAL2838_3_no_theorem_zero", not any(row["theorem_zero"] for row in rows_by_name["signature"]), "no theorem-zero row was promoted"),
        ("VAL2838_4_calculus_conditional", any(row["calculus_id"] == "CALC2838_3_exact_zero_case" and row["status"] == "EXACT_IF_PARENT_SIGNATURE_SIGNED" for row in rows_by_name["calculus"]), "exact auxiliary theorem retained as conditional"),
        ("VAL2838_5_finite_map_active", all(row["fallback_active"] for row in rows_by_name["failure_map"]), "all failed clauses map to finite residual fallback"),
        ("VAL2838_6_finite_nonclaim", all((not row["numeric_value_present"]) and (not row["source_backed"]) for row in rows_by_name["finite_rows"]), "finite acquisition rows remain nonclaim"),
        ("VAL2838_7_guards_active", all(row["guard_active"] for row in rows_by_name["guards"]), "all 2838 guardrails are active"),
        ("VAL2838_8_claim_gates_block_scores", not any(row["claim_allowed"] for row in rows_by_name["gates"]), "no claim gate allows local-GR/source-silence scoring"),
        ("VAL2838_9_next_target_2839", any(row["next_id"] == "NEXT2838_0_2839" and row["selected"] for row in rows_by_name["next"]), "finite RAB residual normalization selected next"),
        ("VAL2838_10_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2838_11_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2838_12_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2838_13_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2838_14_no_claim_flags", no_claim_flags(rows_by_name), "no score/parent/theorem/source/claim flags are true"),
        ("VAL2838_15_no_numeric_predictions", no_numeric_predictions(rows_by_name), "no numeric prediction/coefficient/bound rows inserted"),
        ("VAL2838_16_generated_under_post_checkpoint", under_root(output_paths + branch_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2838_17_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2838_18_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [
        {
            "validation_id": validation_id,
            "passed": passed,
            "detail": detail,
            "timestamp_utc": ts(),
        }
        for validation_id, passed, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2838_OVERALL",
            "passed": overall,
            "detail": "2838 refuses to claim the second-class parent signature, preserves the exact algebraic elimination theorem as conditional, promotes the finite R_AB residual normal form as the honest nonclaim fallback, and selects Green-kernel/source-row normalization next.",
            "timestamp_utc": ts(),
        }
    )
    return rows


def md(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    content = f"""# 2838 - Y5 R2FR Second-Class Auxiliary Block Parent Signature Or Finite RAB Residual Under AX1090

Status: `Y5_R2FR_2838_second_class_signature_failed_finite_RAB_residual_promoted_nonclaim`

## Private Verdict

2838 tries the best remaining clean route: make `R_AB` a genuine second-class auxiliary block rather than a physical local scalar.

The algebra itself is good:

```text
S_aux = integral mu Lambda_R (R_AB - C_AB[Q])
delta_Lambda S = 0 -> R_AB = C_AB[Q]
delta_R S = 0 -> Lambda_R + J_R + Pi_R + readout_regen + D_operator_terms = 0
```

So if `J_R=Pi_R=readout_regen=D_operator_terms=0` is parent-signed, then the auxiliary sector dies cleanly before local readout. That would be the serious local-GR route.

But the parent signature still does **not** close. The current corpus does not yet derive the `Lambda_R(R_AB-C_AB)` block, the no-derivative grammar, source descent, boundary silence, and readout stability as one primitive-owned package. Therefore `R_AB=0`, `J_R=0`, `Pi_R=0`, `Z_R=0`, local GR/Newton, R10, PPN, clock, and orbital claims remain blocked.

The useful leap forward is that the fallback is now sharper: if any protection survives, the branch must be treated as the finite residual equation

```text
E_R^finite = -Div(Z_R Grad R_AB) + M_R^2 (R_AB-C_AB[Q]) + J_R + Pi_R + R_readout = 0
```

No scoring is allowed until `Z_R`, `M_R^2`, `J_R`, `Pi_R/B_R/Q_R`, `R_readout/tau`, and `C_AB` normalization have source paths, units, and arena projections.

## Source Register

{markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Second-Class Signature Audit

{markdown_table(rows["signature"], ["signature_id", "clause", "current_status", "proof_or_blocker", "parent_signed", "theorem_zero", "valid_for_claim"])}

## Auxiliary Elimination Calculus

{markdown_table(rows["calculus"], ["calculus_id", "equation_or_step", "meaning", "status", "claim_blocker", "valid_for_claim"])}

## Failure To Finite Residual Map

{markdown_table(rows["failure_map"], ["failure_id", "failed_clause", "residual_meaning", "required_fallback", "fallback_active", "valid_for_claim"])}

## Finite RAB Residual Equation

{markdown_table(rows["finite_equation"], ["equation_id", "equation", "meaning", "status", "required_inputs", "numeric_value_present", "valid_for_claim"])}

## Finite Residual Acquisition Rows

{markdown_table(rows["finite_rows"], ["acquisition_id", "symbol", "meaning", "current_status", "observable_link", "numeric_value_present", "source_backed", "valid_for_claim"])}

## Guards

{markdown_table(rows["guards"], ["guard_id", "guard", "because", "effect", "guard_active", "valid_for_claim"])}

## Claim Gates

{markdown_table(rows["gates"], ["claim_gate_id", "claim", "gate_passed", "status", "reason", "claim_allowed"])}

## Decision Ledger

{markdown_table(rows["decision"], ["decision_id", "decision", "result", "because", "next_action", "valid_for_claim"])}

## Next Target

{markdown_table(rows["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(rows["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(rows["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows: dict[str, list[dict[str, Any]]] = {}
    rows["sources"] = source_rows()
    rows["signature"] = signature_rows()
    rows["calculus"] = calculus_rows()
    rows["failure_map"] = failure_map_rows()
    rows["finite_equation"] = finite_equation_rows()
    rows["finite_rows"] = finite_row_specs()
    rows["guards"] = guard_rows()
    rows["gates"] = gate_rows(rows)
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in [
        "sources",
        "signature",
        "calculus",
        "failure_map",
        "finite_equation",
        "finite_rows",
        "guards",
        "gates",
        "decision",
        "next",
    ]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])

    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2838_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2838_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()

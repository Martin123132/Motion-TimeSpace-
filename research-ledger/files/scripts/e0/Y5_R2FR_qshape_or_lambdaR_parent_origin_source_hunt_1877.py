from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "1877"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / CHECKPOINT_ID
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1877-Y5-R2FR-qshape-or-lambdaR-parent-origin-source-hunt.md"

INPUTS = {
    "1876_next": OUT / "P8_Y5_PARENT_QLOC_1876_NEXT_TARGET.csv",
    "1876_validation": OUT / "P8_Y5_BRR545_1876_VALIDATION.csv",
    "1874_verticality": ROOT / "1874-Y5-R2FR-parent-domain-verticality-for-RAB-or-explicit-residual-field.md",
    "1875_vector": OUT / "P8_Y5_PARENT_QLOC_1875_RAB_RESIDUAL_OPERATOR_SOURCE_VECTOR.csv",
    "07_nonprop_constraint": ROOT / "07-nonpropagating-reciprocity-constraint.md",
    "10_observer_contract": ROOT / "10-observer-map-symplectic-contract.md",
    "1247_lambda_gate": ROOT / "1247-Y5-R10-parent-lambdaR-constraint-legitimacy-gate.md",
    "1248_lambda_ansatz": ROOT / "1248-Y5-R10-minimal-lambdaR-parent-action-ansatz-and-Dirac-check.md",
    "1576_quotient": ROOT / "1576-Y5-RAB-constraint-no-pole-or-quotient-map-construction.md",
    "1737_qmap": ROOT / "1737-Y5-R2FR-q-map-Dq-vertical-basis-source-row-or-coframe-functor-zero.md",
    "1867_object_language": ROOT / "1867-Y5-R2FR-object-language-radial-cell-constraint-or-finite-ZRJR-intake.md",
    "1868_typed_grammar": ROOT / "1868-Y5-R2FR-typed-parent-grammar-for-radial-cell-or-coefficient-bound-branch.md",
}

SOURCE_NEEDLES = {
    "1876_next": [
        "1877-Y5-R2FR-qshape-or-lambdaR-parent-origin-source-hunt.md",
        "selected",
    ],
    "1876_validation": [
        "VAL1876_OVERALL,PASS",
        "VAL1876_4_R10_route_separation,PASS",
    ],
    "1874_verticality": [
        "PARENT_DOMAIN_VERTICALITY_NOT_DERIVED",
        "RAB_CLASSIFIED_AS_EXPLICIT_RESIDUAL_FIELD_CURRENTLY",
    ],
    "1875_vector": [
        "RV1875_0_domain_visibility",
        "MISSING_PARENT_CONSTRAINT_ORIGIN",
    ],
    "07_nonprop_constraint": [
        "S_constraint = integral lambda_R R_AB.",
        "parent origin is still open",
    ],
    "10_observer_contract": [
        "J_q = T sqrt(S)",
        "R_AB = ln(T^2 S) = 2 ln(J_q).",
    ],
    "1247_lambda_gate": [
        "lambda_R is closure with formal clothes on",
        "MISSING_MULTIPLIER_ORIGIN",
    ],
    "1248_lambda_ansatz": [
        "REJECT_ZERO_THEOREM_UNDERIVED",
        "H_core and canonical brackets for T,S are not supplied",
    ],
    "1576_quotient": [
        "QUOTIENT_MAP_CONFLICT_IDENTIFIED",
        "R_AB=2 ln(J_q)",
    ],
    "1737_qmap": [
        "COFRAME_FUNCTOR_ZERO_NOT_SIGNED",
        "v_RAB/Jq",
    ],
    "1867_object_language": [
        "OBJECT_LANGUAGE_CONSTRAINT_NOT_DERIVED_CURRENT_CORPUS",
        "MISSING_TYPED_PARENT_GRAMMAR",
    ],
    "1868_typed_grammar": [
        "TYPED_PARENT_GRAMMAR_NOT_DERIVED_CURRENT_CORPUS",
        "MISSING_PARENT_CATEGORY_PRINCIPLE",
    ],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1877_SOURCE_REGISTER.csv",
    "route_audit": OUT / "P8_Y5_PARENT_QLOC_1877_QSHAPE_LAMBDAR_ROUTE_AUDIT.csv",
    "equivalence_no_go": OUT / "P8_Y5_PARENT_QLOC_1877_QSHAPE_LAMBDAR_EQUIVALENCE_NO_GO.csv",
    "parent_contract": OUT / "P8_Y5_PARENT_QLOC_1877_PARENT_CONTRACT_REQUIREMENTS.csv",
    "conditional_theorem": OUT / "P8_Y5_PARENT_QLOC_1877_CONDITIONAL_THEOREM_STATUS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1877_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1877_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1877_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_1877_VALIDATION.csv",
}


def ensure_dirs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)


def bool_string(value: Any) -> str:
    return str(value).strip().lower()


def path_has_needles(path: Path, needles: list[str]) -> tuple[bool, str]:
    if not path.exists():
        return False, "MISSING_SOURCE_PATH"
    text = path.read_text(encoding="utf-8", errors="ignore")
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return False, "MISSING_NEEDLES=" + ";".join(missing)
    return True, "OK"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path in INPUTS.items():
        ok, detail = path_has_needles(path, SOURCE_NEEDLES[source_id])
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source_id,
                "source_path": str(path),
                "required_needles": " ; ".join(SOURCE_NEEDLES[source_id]),
                "source_exists": path.exists(),
                "needle_check": detail,
                "usable_for_1877": ok,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def route_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "QSL1877_0_lambdaR_auxiliary",
            "route": "lambda_R C_R auxiliary constraint",
            "candidate_statement": "S_parent contains Lambda_R C_R with C_R=R_AB=ln(T^2 S), so delta_Lambda_R gives C_R=0.",
            "what_is_derived": "formal variational effect only",
            "what_is_not_derived": "Lambda_R parent origin, H_core/Dirac preservation, matter descent, boundary silence, readout stability",
            "status": "FORMAL_PASS_NOT_PARENT_SIGNED",
            "claim_effect": "cannot claim local_GR; can remain exact conditional route",
            "source_anchor": str(INPUTS["1248_lambda_ansatz"]),
            "proof_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "QSL1877_1_qshape_excludes_radial_cell",
            "route": "q_shape quotient excluding J_q/R_AB",
            "candidate_statement": "Let q_shape forget the reciprocal radial-cell volume so Dq_shape[v_R]=0.",
            "what_is_derived": "a possible quotient notation",
            "what_is_not_derived": "observed coframe/readout functor remains q_shape-basic after J_q is forgotten",
            "status": "COLLAPSES_TO_READOUT_OR_CONSTRAINT_PROBLEM",
            "claim_effect": "Dq_shape[v_R]=0 alone does not imply DObs_e[v_R]=0",
            "source_anchor": str(INPUTS["1737_qmap"]),
            "proof_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "QSL1877_2_constraint_first_quotient",
            "route": "constraint-first quotient",
            "candidate_statement": "First impose C_R=0, then R_AB is absent from the quotient fibre.",
            "what_is_derived": "logical consistency of the quotient after constraint",
            "what_is_not_derived": "the parent reason C_R=0 is imposed before readout",
            "status": "EQUIVALENT_TO_LAMBDAR_OR_CATEGORY_ROUTE",
            "claim_effect": "not an independent proof; it reuses the lambda/category burden",
            "source_anchor": str(INPUTS["1576_quotient"]),
            "proof_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "QSL1877_3_typed_compatibility_category",
            "route": "typed parent compatibility grammar",
            "candidate_statement": "C_R/R_AB is compatibility data only, so derivative/source/boundary operators on it are illegal.",
            "what_is_derived": "exact conditional theorem shape",
            "what_is_not_derived": "parent category principle forcing the grammar from motion/time/space primitives",
            "status": "BEST_CONDITIONAL_ROUTE_UNSIGNED",
            "claim_effect": "would kill Z_R, J_R and Q_R only if all premises close",
            "source_anchor": str(INPUTS["1868_typed_grammar"]),
            "proof_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "QSL1877_4_finite_residual_branch",
            "route": "finite R_AB residual field",
            "candidate_statement": "Treat R_AB as explicit residual with Z_R/M_R^2/J_R/Q_R/source/boundary/projection rows.",
            "what_is_derived": "safe executable branch schema",
            "what_is_not_derived": "any coefficient value, local-GR theorem-zero, or arena pass",
            "status": "FALLBACK_READY_NONCLAIM",
            "claim_effect": "all local arenas remain blocked until theorem-zero or sourced numeric rows exist",
            "source_anchor": str(INPUTS["1875_vector"]),
            "proof_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def equivalence_no_go_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "step_id": "EQ1877_0_identity",
            "statement": "J_q=T sqrt(S), C_R=R_AB=ln(T^2 S)=2 ln(J_q).",
            "consequence": "any vertical direction that changes R_AB changes the radial observer-cell Jacobian unless C_R is fixed first",
            "status": "IDENTITY_USED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "step_id": "EQ1877_1_observer_visible_map",
            "statement": "If q contains the observed radial cell or coframe data, then Dq[v_R] is nonzero for a direction that changes R_AB.",
            "consequence": "cheap verticality fails in the observer-cell map",
            "status": "VERTICALITY_REJECTED_FOR_OBSERVER_MAP",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "step_id": "EQ1877_2_shape_only_map",
            "statement": "If q_shape excludes J_q/R_AB, then Dq_shape[v_R]=0 can be made true by definition.",
            "consequence": "but local metric/readout claims require DObs_e[v_R]=0, not merely Dq_shape[v_R]=0",
            "status": "DOBS_E_BURDEN_REMAINS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "step_id": "EQ1877_3_readout_functor_test",
            "statement": "DObs_e[v_R]=DE|_q(Dq[v_R]) vanishes only if observed coframe/readout is a q-basic functor or C_R=0 before readout.",
            "consequence": "shape-only quotient must either prove a q-basic coframe functor or import the constraint-first route",
            "status": "QSHAPE_COLLAPSES_TO_FUNCTOR_OR_CONSTRAINT_GATE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "step_id": "EQ1877_4_lambda_equivalence",
            "statement": "Constraint-first q_shape and Lambda_R C_R produce the same no-pole target: remove R_AB before local observables can source/read it.",
            "consequence": "q_shape is not an independent escape; it is another language for the lambda/category theorem unless a separate readout-functor proof appears",
            "status": "QSHAPE_LAMBDAR_EQUIVALENCE_FOR_CURRENT_CORPUS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "step_id": "EQ1877_5_no_claim_verdict",
            "statement": "No current source signs q_shape, Lambda_R, parent category grammar, matter descent, boundary silence, and readout closure together.",
            "consequence": "R_AB remains an explicit residual vector in the current branch",
            "status": "NO_PARENT_ORIGIN_FOUND_CURRENT_CORPUS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def parent_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "contract_id": "PCR1877_0_primitives",
            "required_clause": "parent primitive list for motion/time/space before metric readout",
            "needed_evidence": "fields, constructors, and allowed operators showing C_R is not a free scalar",
            "current_status": "MISSING_PARENT_PRIMITIVE_LIST",
            "would_unlock": "category proof prerequisite",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "PCR1877_1_qshape",
            "required_clause": "explicit q_shape and Dq_shape kernel on v_R",
            "needed_evidence": "Dq_shape[v_R]=0 plus proof that all visible readouts descend through q_shape",
            "current_status": "MISSING_QSHAPE_READOUT_FUNCTOR",
            "would_unlock": "quotient route without posthoc deletion",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "PCR1877_2_observed_coframe",
            "required_clause": "observed coframe functor E(q_shape) or constraint-first readout",
            "needed_evidence": "DObs_e[v_R]=0 for coframe, clocks, rulers, photons, source and orbital readout",
            "current_status": "MISSING_DOBS_E_ZERO",
            "would_unlock": "local metric invisibility",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "PCR1877_3_lambda_owner",
            "required_clause": "Lambda_R has parent origin and closed Dirac/auxiliary chain",
            "needed_evidence": "S_parent/H_core, primary-secondary preservation, constraint class, degree count",
            "current_status": "MISSING_LAMBDAR_ORIGIN_DIRAC_CHAIN",
            "would_unlock": "constraint-first no-pole route",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "PCR1877_4_operator_ban",
            "required_clause": "no derivative/vertical-metric operator can act on C_R/R_AB",
            "needed_evidence": "operator grammar forbidding Z_R h^ij D_iR_ABD_jR_AB and readout regeneration",
            "current_status": "MISSING_PARENT_CATEGORY_PRINCIPLE",
            "would_unlock": "Z_R theorem-zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "PCR1877_5_matter_boundary",
            "required_clause": "matter descent and boundary/readout silence",
            "needed_evidence": "J_R=0, beta_source/test=0 or q-basic, Q_R/Pi_R/B_R proper/exact, tau readouts descend",
            "current_status": "MISSING_MATTER_BOUNDARY_READOUT_SILENCE",
            "would_unlock": "J_R/Q_R/source-tail theorem-zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "PCR1877_6_PPN_conservation",
            "required_clause": "PPN beta and Bianchi-like conservation after C_R removal",
            "needed_evidence": "second-order local solution, common matter coupling, and conservation identity",
            "current_status": "MISSING_BETA_CONSERVATION_COMMON_MATTER",
            "would_unlock": "local GR/Newton claim after gamma route",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def conditional_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "CT1877_0_statement",
            "name": "conditional q_shape/Lambda_R radial-cell no-pole theorem",
            "statement": "If C_R=R_AB=2ln(J_q) is parent compatibility data only; Lambda_R C_R or equivalent category constraint is parent-owned; observed coframe/readout descends through q_shape after C_R removal; and derivative/source/boundary operators on C_R are illegal, then C_R=Z_R=J_R=Q_R=0 before local readout.",
            "proof_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "missing_premises": "PCR1877_0;PCR1877_1;PCR1877_2;PCR1877_3;PCR1877_4;PCR1877_5;PCR1877_6",
            "local_gr_claim": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "CT1877_1_no_go",
            "name": "shape-only quotient no-go for current corpus",
            "statement": "Dq_shape[v_R]=0 is insufficient for local GR because the visible coframe/readout still needs DObs_e[v_R]=0; proving that either reintroduces the same parent constraint/category principle or requires a new readout-functor theorem.",
            "proof_status": "CURRENT_CORPUS_NO_GO_FOR_CHEAP_QSHAPE",
            "missing_premises": "PCR1877_1;PCR1877_2",
            "local_gr_claim": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1877_0_source_hunt",
            "claim": "1877 source hunt identifies the exact q_shape/lambda fork",
            "status": "ALLOW_INTERNAL_NONCLAIM_SYNTHESIS",
            "reason": "routes are source-anchored and all claims remain blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1877_1_qshape",
            "claim": "q_shape derives DObs_e[v_R]=0",
            "status": "BLOCKED",
            "reason": "shape-only quotient lacks observed coframe/readout functor proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1877_2_lambdaR",
            "claim": "Lambda_R parent-origin no-pole theorem",
            "status": "BLOCKED",
            "reason": "Lambda_R origin, H_core/Dirac chain, matter descent and boundary silence remain unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1877_3_ZR_JR_QR_zero",
            "claim": "Z_R, J_R, Q_R vanish by parent category",
            "status": "BLOCKED",
            "reason": "typed parent category principle is conditional but not derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1877_4_local_GR",
            "claim": "MTS derives local GR/Newton branch from q_shape/lambda route",
            "status": "BLOCKED",
            "reason": "C_R removal, PPN beta, conservation, matter/common-frame and boundary/readout gates remain open",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1877_0_result",
            "decision": "NO_PARENT_ORIGIN_FOUND_CURRENT_CORPUS",
            "basis": "q_shape, Lambda_R, and typed-compatibility routes are all exact conditional routes but none are parent-signed together",
            "consequence": "R_AB remains explicit residual vector for current runners",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1877_1_qshape",
            "decision": "QSHAPE_IS_NOT_INDEPENDENT_ESCAPE",
            "basis": "if q_shape forgets J_q, Dq can vanish but DObs_e still needs a q-basic coframe or C_R=0 before readout",
            "consequence": "future q_shape proof must target observed coframe/readout, not just quotient notation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1877_2_best_route",
            "decision": "PARENT_CATEGORY_OR_DOBS_E_KERNEL_SELECTED_NEXT",
            "basis": "the least slippery next proof is whether the observed coframe/readout is q_shape-basic or whether parent grammar makes C_R compatibility-only",
            "consequence": "try one focused readout-functor/category theorem before returning to finite coefficient rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1877_0_primary",
            "target_doc": "1878-Y5-R2FR-qshape-readout-functor-kernel-or-parent-category-principle.md",
            "target_script": "scripts/Y5_R2FR_qshape_readout_functor_kernel_or_parent_category_principle_1878.py",
            "objective": "prove DObs_e[v_R]=0 from an explicit q_shape readout functor or derive the parent category principle that makes C_R compatibility-only; if neither closes, stage the first finite DObs_e/C_R leak row.",
            "selection_status": "selected",
            "success_condition": "either a source-backed DObs_e kernel/category theorem, or a nonclaim finite coframe-leak row with local_GR/PPN gates blocked.",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1877_1_fallback",
            "target_doc": "1878b-Y5-R2FR-finite-DObs-qRhat-bound-row.md",
            "target_script": "scripts/Y5_R2FR_finite_DObs_qRhat_bound_row_1878b.py",
            "objective": "if the readout/category theorem fails, build finite coframe/Q_R leakage rows for PPN/orbital/local-GR blocking runners.",
            "selection_status": "held_fallback",
            "success_condition": "finite leak rows are source-ready, nonclaim, and refused unless numeric/source/projection inputs exist.",
            "valid_for_claim": False,
        },
    ]


def all_output_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "route_audit": route_audit_rows(),
        "equivalence_no_go": equivalence_no_go_rows(),
        "parent_contract": parent_contract_rows(),
        "conditional_theorem": conditional_theorem_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }


def all_claim_flags_false(paths: list[Path]) -> tuple[bool, str]:
    checked = 0
    for path in paths:
        for row_index, row in enumerate(csv_rows(path), start=2):
            for column in [
                "valid_for_claim",
                "claim_allowed",
                "proof_closed",
                "local_gr_claim",
            ]:
                if column in row:
                    checked += 1
                    if bool_string(row[column]) == "true":
                        return False, f"{path.name}:{row_index}:{column}=true"
    return checked > 0, f"checked={checked}"


def csv_parse_check(paths: list[Path]) -> tuple[bool, str]:
    details: list[str] = []
    for path in paths:
        rows = csv_rows(path)
        if not rows:
            return False, f"EMPTY_CSV={path.name}"
        details.append(f"{path.name}:{len(rows)}")
    return True, ";".join(details)


def copy_branch_artifacts() -> None:
    for path in OUTPUTS.values():
        if path.name.endswith("_VALIDATION.csv"):
            continue
        shutil.copy2(path, MICROSCOPE_RESIDUALS / path.name)
        shutil.copy2(path, QUARANTINE / path.name)
    shutil.copy2(OUTPUTS["equivalence_no_go"], QUEUE / "JR1877_QSHAPE_LAMBDAR_EQUIVALENCE_NO_GO_NONCLAIM.csv")
    shutil.copy2(OUTPUTS["parent_contract"], QUEUE / "JR1877_PARENT_CONTRACT_REQUIREMENTS_NONCLAIM.csv")
    shutil.copy2(OUTPUTS["next_target"], QUEUE / "JR1877_NEXT_TARGET_NONCLAIM.csv")


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows() -> list[dict[str, Any]]:
    generated_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    rows_by_name = {key: csv_rows(path) for key, path in OUTPUTS.items() if key != "validation"}
    checks: list[dict[str, Any]] = []

    sources = rows_by_name["source_register"]
    checks.append(
        {
            "validation_id": "VAL1877_0_sources",
            "status": "PASS" if all(bool_string(row["usable_for_1877"]) == "true" for row in sources) else "FAIL",
            "detail": "q_shape/lambda source chain exists and contains required needles",
            "valid_for_claim": False,
        }
    )

    route_statuses = {row["status"] for row in rows_by_name["route_audit"]}
    checks.append(
        {
            "validation_id": "VAL1877_1_route_audit",
            "status": "PASS"
            if {
                "FORMAL_PASS_NOT_PARENT_SIGNED",
                "COLLAPSES_TO_READOUT_OR_CONSTRAINT_PROBLEM",
                "EQUIVALENT_TO_LAMBDAR_OR_CATEGORY_ROUTE",
                "BEST_CONDITIONAL_ROUTE_UNSIGNED",
                "FALLBACK_READY_NONCLAIM",
            }.issubset(route_statuses)
            else "FAIL",
            "detail": "lambda, q_shape, constraint-first, category, and finite fallback routes audited",
            "valid_for_claim": False,
        }
    )

    equivalence_statuses = {row["status"] for row in rows_by_name["equivalence_no_go"]}
    checks.append(
        {
            "validation_id": "VAL1877_2_equivalence_no_go",
            "status": "PASS"
            if "QSHAPE_LAMBDAR_EQUIVALENCE_FOR_CURRENT_CORPUS" in equivalence_statuses
            and "NO_PARENT_ORIGIN_FOUND_CURRENT_CORPUS" in equivalence_statuses
            else "FAIL",
            "detail": "q_shape is shown to collapse to readout-functor or lambda/category gate in current corpus",
            "valid_for_claim": False,
        }
    )

    contracts = rows_by_name["parent_contract"]
    checks.append(
        {
            "validation_id": "VAL1877_3_parent_contract",
            "status": "PASS"
            if len(contracts) == 7
            and any(row["current_status"] == "MISSING_QSHAPE_READOUT_FUNCTOR" for row in contracts)
            and any(row["current_status"] == "MISSING_LAMBDAR_ORIGIN_DIRAC_CHAIN" for row in contracts)
            else "FAIL",
            "detail": "parent contract covers primitive, q_shape, coframe, lambda, operator, matter/boundary, and PPN/conservation gates",
            "valid_for_claim": False,
        }
    )

    theorem = rows_by_name["conditional_theorem"]
    checks.append(
        {
            "validation_id": "VAL1877_4_conditional_theorem_nonclaim",
            "status": "PASS"
            if any(row["proof_status"] == "EXACT_CONDITIONAL_NOT_PARENT_SIGNED" for row in theorem)
            and all(bool_string(row["claim_allowed"]) == "false" for row in theorem)
            else "FAIL",
            "detail": "conditional theorem is recorded but not promoted",
            "valid_for_claim": False,
        }
    )

    claim_gates = rows_by_name["claim_gate"]
    checks.append(
        {
            "validation_id": "VAL1877_5_claim_gates",
            "status": "PASS"
            if any(row["status"] == "ALLOW_INTERNAL_NONCLAIM_SYNTHESIS" for row in claim_gates)
            and all(bool_string(row["claim_allowed"]) == "false" for row in claim_gates)
            else "FAIL",
            "detail": "only internal nonclaim synthesis is allowed",
            "valid_for_claim": False,
        }
    )

    decisions = rows_by_name["decision"]
    checks.append(
        {
            "validation_id": "VAL1877_6_decision",
            "status": "PASS"
            if any(row["decision"] == "QSHAPE_IS_NOT_INDEPENDENT_ESCAPE" for row in decisions)
            and any(row["decision"] == "PARENT_CATEGORY_OR_DOBS_E_KERNEL_SELECTED_NEXT" for row in decisions)
            else "FAIL",
            "detail": "decision ledger selects q_shape readout/category theorem next",
            "valid_for_claim": False,
        }
    )

    next_targets = rows_by_name["next_target"]
    checks.append(
        {
            "validation_id": "VAL1877_7_next_target",
            "status": "PASS"
            if any(row["route_id"] == "NEXT1877_0_primary" and row["selection_status"] == "selected" for row in next_targets)
            else "FAIL",
            "detail": "1878 q_shape readout functor/category-principle target selected",
            "valid_for_claim": False,
        }
    )

    flags_ok, flags_detail = all_claim_flags_false(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1877_8_claim_flags_false",
            "status": "PASS" if flags_ok else "FAIL",
            "detail": flags_detail,
            "valid_for_claim": False,
        }
    )

    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1877_9_csv_parse",
            "status": "PASS" if parse_ok else "FAIL",
            "detail": parse_detail,
            "valid_for_claim": False,
        }
    )

    copied_paths = [
        MICROSCOPE_RESIDUALS / OUTPUTS["equivalence_no_go"].name,
        QUARANTINE / OUTPUTS["parent_contract"].name,
        QUEUE / "JR1877_QSHAPE_LAMBDAR_EQUIVALENCE_NO_GO_NONCLAIM.csv",
        QUEUE / "JR1877_PARENT_CONTRACT_REQUIREMENTS_NONCLAIM.csv",
    ]
    checks.append(
        {
            "validation_id": "VAL1877_10_branch_copies",
            "status": "PASS" if all(path.exists() for path in copied_paths) else "FAIL",
            "detail": ";".join(str(path) for path in copied_paths),
            "valid_for_claim": False,
        }
    )

    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append(
        {
            "validation_id": "VAL1877_11_pycache_absent",
            "status": "PASS" if not pycache.exists() else "FAIL",
            "detail": str(pycache),
            "valid_for_claim": False,
        }
    )

    formalization_hits = list(FORMALIZATION.rglob("*1877*")) if FORMALIZATION.exists() else []
    checks.append(
        {
            "validation_id": "VAL1877_12_formalization_untouched",
            "status": "PASS" if not formalization_hits else "FAIL",
            "detail": f"formalization_1877_count={len(formalization_hits)}",
            "valid_for_claim": False,
        }
    )

    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append(
        {
            "validation_id": "VAL1877_OVERALL",
            "status": "PASS" if fail_count == 0 else "FAIL",
            "detail": "1877 q_shape or lambda_R parent-origin source hunt",
            "valid_for_claim": False,
        }
    )
    return checks


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", " ") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 1877 - q_shape Or Lambda_R Parent-Origin Source Hunt

**Private status:** nonclaim derivation checkpoint. This narrows the local-GR route; it does not claim derived local GR.

## Result

The source hunt did not find a parent-signed `q_shape` or `Lambda_R` origin. It did find the important structural fact:

```text
J_q = T sqrt(S)
C_R = R_AB = ln(T^2 S) = 2 ln(J_q)
```

So a `v_R` direction that changes `R_AB` changes the observed radial cell unless the parent theory removes or silences that cell before readout.

That means `q_shape` is not an independent shortcut. If `q_shape` forgets `J_q`, then `Dq_shape[v_R]=0` is easy, but local GR needs the harder statement:

```text
DObs_e[v_R] = 0
```

That harder statement either requires a q-basic observed-coframe/readout functor or the same constraint/category theorem as the `Lambda_R C_R` route.

## Route Audit

{markdown_table(rows_by_name["route_audit"])}

## Equivalence / No-Go Ledger

{markdown_table(rows_by_name["equivalence_no_go"])}

## Parent Contract Requirements

{markdown_table(rows_by_name["parent_contract"])}

## Conditional Theorem Status

{markdown_table(rows_by_name["conditional_theorem"])}

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Claim Gate

{markdown_table(rows_by_name["claim_gate"])}

## Decision Ledger

{markdown_table(rows_by_name["decision"])}

## Next Target

{markdown_table(rows_by_name["next_target"])}

## Validation

{markdown_table(validation)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows_by_name = all_output_rows()
    for key, rows in rows_by_name.items():
        write_csv(OUTPUTS[key], rows)
    copy_branch_artifacts()
    remove_pycache()
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()

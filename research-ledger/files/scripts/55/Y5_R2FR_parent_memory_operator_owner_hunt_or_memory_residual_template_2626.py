from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2626-Y5-R2FR-parent-memory-operator-owner-hunt-or-memory-residual-template.md"

PREFIX = "P8_Y5_MEMORY_OWNER_GATE_2626"

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "lineage_ledger": RESIDUALS / f"{PREFIX}_LINEAGE_LEDGER.csv",
    "owner_audit": RESIDUALS / f"{PREFIX}_PARENT_MEMORY_OPERATOR_OWNER_AUDIT.csv",
    "zero_theorem": RESIDUALS / f"{PREFIX}_POSITIVE_OPERATOR_ZERO_THEOREM_ATTEMPT.csv",
    "residual_template": RESIDUALS / f"{PREFIX}_MEMORY_RESIDUAL_TEMPLATE.csv",
    "observable_queue": RESIDUALS / f"{PREFIX}_OBSERVABLE_COUPLING_QUEUE.csv",
    "countermodel": RESIDUALS / f"{PREFIX}_COUNTERMODEL_LEDGER.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2626_VALIDATION.csv",
}

SOURCES = [
    {
        "source_id": "SRC2626_00_2625_handoff_doc",
        "description": "2625 selects parent memory operator owner hunt",
        "path": ROOT / "2625-Y5-R2FR-field-by-field-parent-domain-certificate-or-readout-residual-closure.md",
        "needles": ["NEXT2625_0_primary", "PARENT_MEMORY_OPERATOR_OWNER_HUNT_IS_NEXT", "READOUT_ZERO_DEMOTED_TO_EXPLICIT_CLOSURE"],
    },
    {
        "source_id": "SRC2626_01_2625_validation",
        "description": "2625 validation passed and formalization stayed untouched",
        "path": RESIDUALS / "P8_Y5_BRR545_2625_VALIDATION.csv",
        "needles": ["VAL2625_OVERALL", "PASS", "VAL2625_11_formalization_untouched"],
    },
    {
        "source_id": "SRC2626_02_967_memory_lemma",
        "description": "relative positive-operator memory lemma and finite bound law",
        "path": ROOT / "967-Y5-R10-readout-after-variation-parent-schema-theorem-or-memory-positive-operator-lemma.md",
        "needles": ["MPO967_4_energy_identity", "MPO967_6_verdict", "MB967_0_gap"],
    },
    {
        "source_id": "SRC2626_03_968_memory_input_audit",
        "description": "memory operator activation inputs missing",
        "path": ROOT / "968-Y5-R10-parent-domain-signature-and-memory-operator-input-audit.md",
        "needles": ["MOI968_0_X_variable", "MOI968_8_verdict", "MZG968_7_verdict"],
    },
    {
        "source_id": "SRC2626_04_969_owner_hunt",
        "description": "historical memory operator owner hunt found no accepted owner",
        "path": ROOT / "969-Y5-R10-parent-memory-operator-owner-hunt-or-readout-domain-certificate.md",
        "needles": ["MOO969_7_verdict", "NO_PARENT_MEMORY_OPERATOR_OWNER_FOUND_CURRENT_CORPUS", "DEC969_3_best_next"],
    },
    {
        "source_id": "SRC2626_05_970_minimal_quadratic_candidate",
        "description": "minimal quadratic memory action candidate and strict residual schema",
        "path": ROOT / "970-Y5-R10-minimal-quadratic-memory-action-construction-or-strict-residual-runner.md",
        "needles": ["QMA970_7_verdict", "CONSTRUCTION_RELATIVE_NOT_PARENT_CLOSED", "RRS970_2_J_X_norm"],
    },
]


def ensure_dirs() -> None:
    for path in (RESIDUALS, LOCAL_BOUNDS, RAB_QUEUE):
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        text = read_text(source["path"])
        exists = source["path"].exists()
        needles_present = exists and all(needle in text for needle in source["needles"])
        rows.append(
            {
                "source_id": source["source_id"],
                "description": source["description"],
                "source_path": str(source["path"]),
                "exists": bool_text(exists),
                "needles_present": bool_text(needles_present),
                "needles": "; ".join(source["needles"]),
                "valid_for_claim": "False",
            }
        )
    return rows


def lineage_rows() -> list[dict[str, Any]]:
    return [
        {
            "lineage_id": "LIN2626_0_current_handoff",
            "input_checkpoint": "2625",
            "what_it_gave": "readout demoted to explicit closure and parent memory operator owner hunt selected",
            "current_use": "start the derivation-first memory route instead of claiming readout silence",
            "claim_status": "nonclaim_handoff",
            "valid_for_claim": "False",
        },
        {
            "lineage_id": "LIN2626_1_relative_lemma",
            "input_checkpoint": "967",
            "what_it_gave": "energy identity proves X=0 only if L_X is positive, J_X=0, and boundary/zero modes are killed",
            "current_use": "keep the theorem form, but demand actual parent owners",
            "claim_status": "relative_theorem_only",
            "valid_for_claim": "False",
        },
        {
            "lineage_id": "LIN2626_2_input_audit",
            "input_checkpoint": "968",
            "what_it_gave": "parent X, selected D, L_X, J_X, boundary data, and K_i couplings are missing",
            "current_use": "treat these as activation gates rather than prose objections",
            "claim_status": "activation_inputs_missing",
            "valid_for_claim": "False",
        },
        {
            "lineage_id": "LIN2626_3_owner_hunt",
            "input_checkpoint": "969",
            "what_it_gave": "no current source-backed parent memory operator owner found",
            "current_use": "avoid re-litigating the same owner hunt without new parent action evidence",
            "claim_status": "no_owner_found",
            "valid_for_claim": "False",
        },
        {
            "lineage_id": "LIN2626_4_quadratic_candidate",
            "input_checkpoint": "970",
            "what_it_gave": "minimal quadratic action varies to L_X X=J_X, but is a candidate not a parent-signed action",
            "current_use": "use it as a template for what the future parent action must own",
            "claim_status": "formal_candidate_not_parent_closed",
            "valid_for_claim": "False",
        },
    ]


def owner_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "MOA2626_0_parent_X",
            "object": "memory/class scalar X",
            "required_owner": "parent configuration variable or quotient scalar with an Euler-Lagrange equation owner",
            "current_status": "MISSING_PARENT_OWNER",
            "source_evidence": "968 names X as missing; 969 finds no accepted owner; 970 only constructs a candidate",
            "blocker": "no source-backed parent field/quotient object uniquely owns X",
            "next_action": "derive X from the parent quotient/action or demote X to retained residual input",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "MOA2626_1_domain_D",
            "object": "selected compact local exterior D",
            "required_owner": "parent-selected local domain with regular boundary and local branch conditions",
            "current_status": "MISSING_PARENT_SELECTED_DOMAIN",
            "source_evidence": "968 says D is missing; 970 says boundary/domain package is not derived",
            "blocker": "domain selector could create wall terms or circular local assumptions",
            "next_action": "source D, boundary, and zero-mode conditions from the same parent structure",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "MOA2626_2_operator_LX",
            "object": "operator L_X",
            "required_owner": "explicit L_X=-nabla_i(A^ij nabla_j)+m_X^2 from parent variation",
            "current_status": "CANDIDATE_EXISTS_NOT_PARENT_SIGNED",
            "source_evidence": "967 gives lemma form; 970 candidate action varies correctly but is not parent-closed",
            "blocker": "operator form is constructed as a template, not extracted from the accepted parent action",
            "next_action": "show the parent action contains the active quadratic X sector before local readout",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "MOA2626_3_positive_A",
            "object": "principal symbol A^ij",
            "required_owner": "positive definite or controlled semidefinite A^ij on D",
            "current_status": "MISSING_SIGN_CERTIFICATE",
            "source_evidence": "967/970 state positivity as a requirement; 968 says no sign certificate is present",
            "blocker": "without a sign certificate the energy identity does not force X=0",
            "next_action": "derive A^ij as a positive metric/coframe contraction or keep residual finite-bound branch",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "MOA2626_4_mass_gap",
            "object": "m_X^2 and lambda_gap",
            "required_owner": "nonnegative mass/gap plus zero-mode removal or positive first eigenvalue",
            "current_status": "MISSING_GAP_INPUTS",
            "source_evidence": "967 writes lambda_gap law; 968 and 970 keep inputs missing",
            "blocker": "massless constant modes and weak gaps remain legal",
            "next_action": "source m_X^2, lambda_1(D), and constant-mode treatment",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "MOA2626_5_JX_source_map",
            "object": "source J_X",
            "required_owner": "decomposition and zero theorem for matter, chi_D wall, boundary, readout, and history sources",
            "current_status": "MISSING_ZERO_SOURCE_THEOREM",
            "source_evidence": "968 says J_X=0 is missing; 970 source/boundary gates fail",
            "blocker": "a small nonzero source gives a finite memory residual rather than theorem-zero",
            "next_action": "derive or bound J_X component-by-component",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "MOA2626_6_boundary_zero_mode",
            "object": "boundary data and zero modes",
            "required_owner": "Dirichlet, zero flux plus zero mean, topological zero, or universal constant sector",
            "current_status": "MISSING_BOUNDARY_DATA",
            "source_evidence": "967 records boundary requirement; 968/970 say it is not derived",
            "blocker": "boundary hair can carry the local residual even when bulk source vanishes",
            "next_action": "prove boundary no-hair/exact-current condition or add boundary_lift_norm to residual runner",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "MOA2626_7_observable_couplings",
            "object": "K_i arena projection couplings",
            "required_owner": "clock, Gdot, R10, PPN, orbital, and WEP/source maps from X and grad X",
            "current_status": "MISSING_ARENA_PROJECTIONS",
            "source_evidence": "967 bound law is symbolic; 968/970 require K_i rows before scoring",
            "blocker": "even a finite X bound cannot be compared to experiments without projection coefficients",
            "next_action": "source K_i with units and bound links or keep each row valid_for_claim=false",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "MOA2626_8_no_tower",
            "object": "no integrated-out memory/scalar tower",
            "required_owner": "proof that solving or removing X does not regenerate R10/R11/f(R)-like leakage",
            "current_status": "MISSING_NO_TOWER_CERTIFICATE",
            "source_evidence": "970 keeps no-integrated-out tower as not derived",
            "blocker": "integrating out X can hide the same local residual in another sector",
            "next_action": "track the effective action after X elimination or keep tower residual rows live",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "MOA2626_9_verdict",
            "object": "current parent memory operator owner",
            "required_owner": "all rows MOA2626_0..8 pass with source paths",
            "current_status": "NO_PARENT_MEMORY_OPERATOR_OWNER_FOUND_CURRENT_CORPUS",
            "source_evidence": "967 relative lemma + 968 missing inputs + 969 no owner + 970 candidate not closed",
            "blocker": "the theorem is mathematically shaped but not parent-activated",
            "next_action": "hunt J_X/boundary source map next; otherwise score finite residuals only when sourced",
            "valid_for_claim": "False",
        },
    ]


def zero_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "ZPT2626_0_assumptions",
            "statement": "Assume X is a parent-owned memory scalar on D with L_X X=J_X",
            "math_status": "CONDITIONAL_SETUP",
            "required_inputs": "parent X; selected D; operator owner",
            "current_result": "setup not parent-signed",
            "claim_effect": "no theorem-zero",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "ZPT2626_1_energy_identity",
            "statement": "If L_X=-nabla_i(A^ij nabla_j)+m_X^2, A^ij positive, m_X^2>=0, J_X=0, and boundary term is zero/nonnegative, then int_D A^ij grad_i X grad_j X + m_X^2 X^2 = 0",
            "math_status": "RELATIVE_PROOF_OK",
            "required_inputs": "positive A^ij; nonnegative mass/gap; zero source; zero boundary flux",
            "current_result": "the algebraic proof is usable as a future gate",
            "claim_effect": "would force X=0 up to controlled constant modes if all premises are signed",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "ZPT2626_2_source_boundary_failure",
            "statement": "The current corpus has not proved J_X=0 or boundary/zero-mode silence",
            "math_status": "ACTIVATION_FAILS",
            "required_inputs": "J_matter=J_chiD=J_boundary=J_readout=J_history=0 plus boundary package",
            "current_result": "source/boundary gates remain unsigned",
            "claim_effect": "memory scalar stays retained residual",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "ZPT2626_3_constant_mode",
            "statement": "If m_X=0 and boundary/mean do not remove constants, X may be a constant mode",
            "math_status": "EXCEPTION_RETAINED",
            "required_inputs": "constant-sector universality/source-independence",
            "current_result": "constant mode is not killed",
            "claim_effect": "universal calibration route remains possible but not proven",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "ZPT2626_4_current_verdict",
            "statement": "Positive-operator memory zero is a relative theorem, not an activated local-GR proof",
            "math_status": "RELATIVE_THEOREM_READY_PARENT_INPUTS_UNSIGNED",
            "required_inputs": "all MOA2626 owner/source/boundary/projection rows",
            "current_result": "do not claim memory zero; use residual template",
            "claim_effect": "R10, PPN, clocks, orbital, WEP, Newton, and local-GR gates stay false",
            "valid_for_claim": "False",
        },
    ]


def residual_template_rows() -> list[dict[str, Any]]:
    return [
        {
            "template_id": "MRI2626_0_lambda_gap",
            "quantity": "lambda_gap",
            "formula_or_requirement": "lambda_gap >= a_min*lambda_1(D)+m_min^2 after zero-mode removal",
            "units": "1/length^2",
            "source_requirement": "a_min, lambda_1(D), m_X^2, boundary class",
            "placeholder_status": "MISSING_PARENT_INPUT",
            "valid_for_claim": "False",
        },
        {
            "template_id": "MRI2626_1_source_norm",
            "quantity": "||J_X||",
            "formula_or_requirement": "component source norm for matter, chi_D wall, boundary, readout, and history",
            "units": "operator-normalized source units",
            "source_requirement": "parent source map with units and zero/nonzero status",
            "placeholder_status": "MISSING_SOURCE_MAP",
            "valid_for_claim": "False",
        },
        {
            "template_id": "MRI2626_2_boundary_lift",
            "quantity": "boundary_lift_norm",
            "formula_or_requirement": "norm of nonzero boundary data or explicit zero certificate",
            "units": "same norm as X or boundary flux units",
            "source_requirement": "parent-selected D and no-hair/current source path",
            "placeholder_status": "MISSING_BOUNDARY_PACKAGE",
            "valid_for_claim": "False",
        },
        {
            "template_id": "MRI2626_3_L2_amplitude",
            "quantity": "||X||_L2",
            "formula_or_requirement": "||X||_L2 <= (||J_X||_L2 + boundary_lift_norm)/lambda_gap",
            "units": "X units times sqrt(volume)",
            "source_requirement": "lambda_gap plus source and boundary inputs",
            "placeholder_status": "MISSING_NUMERIC_BOUND_INPUTS",
            "valid_for_claim": "False",
        },
        {
            "template_id": "MRI2626_4_gradient",
            "quantity": "||grad X||_L2",
            "formula_or_requirement": "a_min||grad X||_L2^2 + m_min^2||X||_L2^2 <= ||J_X||_L2||X||_L2 plus boundary terms",
            "units": "X units / length times sqrt(volume)",
            "source_requirement": "operator signs and source/boundary norms",
            "placeholder_status": "MISSING_NUMERIC_BOUND_INPUTS",
            "valid_for_claim": "False",
        },
        {
            "template_id": "MRI2626_5_pointwise",
            "quantity": "||X||_infty",
            "formula_or_requirement": "||X||_infty <= C_ell(D,A,m)(||J_X||_Lp + boundary_norm)",
            "units": "X units",
            "source_requirement": "elliptic regularity constant, p-norm source, domain regularity",
            "placeholder_status": "MISSING_REGULARITY_CONSTANT",
            "valid_for_claim": "False",
        },
        {
            "template_id": "MRI2626_6_observable_vector",
            "quantity": "Delta O_i",
            "formula_or_requirement": "Delta O_i <= K_i||X|| + K_i_grad||grad X||",
            "units": "arena-specific",
            "source_requirement": "K_i and K_i_grad for each local arena with bound source",
            "placeholder_status": "MISSING_ARENA_PROJECTION",
            "valid_for_claim": "False",
        },
        {
            "template_id": "MRI2626_7_claim_policy",
            "quantity": "valid_for_claim",
            "formula_or_requirement": "false until lambda_gap, J_X, boundary data, K_i, units, and bound links are numeric and sourced",
            "units": "boolean",
            "source_requirement": "all previous rows pass and comparisons are run",
            "placeholder_status": "FORCED_FALSE_THIS_CHECKPOINT",
            "valid_for_claim": "False",
        },
    ]


def observable_queue_rows() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "OCQ2626_0_clock",
            "arena": "clock/redshift/time standards",
            "needed_projection": "K_clock and K_clock_grad from X or grad X to fractional frequency/time drift",
            "bound_source_needed": "clock/frequency comparison bound with units",
            "current_status": "MISSING_ARENA_PROJECTION",
            "valid_for_claim": "False",
        },
        {
            "queue_id": "OCQ2626_1_Gdot",
            "arena": "effective Gdot/time drift",
            "needed_projection": "K_Gdot from X to dG_eff/dt or static local drift proxy",
            "bound_source_needed": "Gdot or equivalent local time-variation bound",
            "current_status": "MISSING_ARENA_PROJECTION",
            "valid_for_claim": "False",
        },
        {
            "queue_id": "OCQ2626_2_R10",
            "arena": "short-range fifth force/Yukawa",
            "needed_projection": "K_R10 and lambda_X mapping X exchange to alpha(lambda)",
            "bound_source_needed": "real alpha_bound(lambda) curve or source-backed nonclaim anchors",
            "current_status": "MISSING_ARENA_PROJECTION",
            "valid_for_claim": "False",
        },
        {
            "queue_id": "OCQ2626_3_PPN",
            "arena": "solar-system PPN",
            "needed_projection": "K_PPN vector for gamma, beta, alpha1, alpha2, alpha3, xi",
            "bound_source_needed": "official or review-backed PPN bounds",
            "current_status": "MISSING_ARENA_PROJECTION",
            "valid_for_claim": "False",
        },
        {
            "queue_id": "OCQ2626_4_orbital",
            "arena": "perihelion/range/orbital systems",
            "needed_projection": "K_orbital from X profile to precession/range residual",
            "bound_source_needed": "orbital residual limits with units and system definition",
            "current_status": "MISSING_ARENA_PROJECTION",
            "valid_for_claim": "False",
        },
        {
            "queue_id": "OCQ2626_5_WEP_source",
            "arena": "WEP/source composition",
            "needed_projection": "species/source dependence of J_X and coupling universality",
            "bound_source_needed": "composition/WEP bound and source-dependence derivation",
            "current_status": "MISSING_ARENA_PROJECTION",
            "valid_for_claim": "False",
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "countermodel_id": "CM2626_0_nonzero_source",
            "countermodel": "J_X is small but nonzero from matter, chi_D wall, boundary, readout, or history",
            "effect": "positive operator gives finite X, not X=0",
            "retained": "True",
            "reason": "zero-source theorem is unsigned",
            "closure_needed": "component source map or numeric residual bound",
            "valid_for_claim": "False",
        },
        {
            "countermodel_id": "CM2626_1_boundary_hair",
            "countermodel": "bulk source vanishes but boundary lift or zero flux condition fails",
            "effect": "memory residual lives on boundary/zero-mode data",
            "retained": "True",
            "reason": "boundary package is missing",
            "closure_needed": "parent-selected D plus no-hair/exact-current proof",
            "valid_for_claim": "False",
        },
        {
            "countermodel_id": "CM2626_2_constant_mode",
            "countermodel": "m_X=0 with constant/topological mode not removed",
            "effect": "energy identity permits constant X",
            "retained": "True",
            "reason": "constant-sector universality is not proven",
            "closure_needed": "zero-mean/topological condition or universal calibration proof",
            "valid_for_claim": "False",
        },
        {
            "countermodel_id": "CM2626_3_integrated_out_tower",
            "countermodel": "X is solved out and reappears as curvature/scalar/nonlocal local residual",
            "effect": "R10/R11/f(R)-like leakage can be hidden rather than removed",
            "retained": "True",
            "reason": "no-tower certificate is missing",
            "closure_needed": "effective-action audit after eliminating X",
            "valid_for_claim": "False",
        },
        {
            "countermodel_id": "CM2626_4_wrong_double_zero_gate",
            "countermodel": "double-zero gate multiplies the kinetic operator itself in the local limit",
            "effect": "operator degenerates instead of proving X=0",
            "retained": "True",
            "reason": "970 found active-zero and double-zero decoupling are not interchangeable",
            "closure_needed": "parent split between active hidden operator and observed coupling",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE2626_0_parent_memory_owner",
            "claim": "parent L_X/J_X owner found",
            "current_evidence": "no accepted owner; candidate action only",
            "gate_pass": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE2626_1_active_memory_zero",
            "claim": "positive operator proves local X=0",
            "current_evidence": "positivity/source/boundary premises unsigned",
            "gate_pass": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE2626_2_finite_memory_residual_score",
            "claim": "memory residual can be numerically scored",
            "current_evidence": "lambda_gap, J_X, boundary lift, and K_i rows missing",
            "gate_pass": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE2626_3_R10_PPN_clock_orbital",
            "claim": "R10/PPN/clock/orbital local arenas pass from memory branch",
            "current_evidence": "arena projection queue is all nonclaim",
            "gate_pass": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE2626_4_local_GR_Newton",
            "claim": "memory branch helps complete local GR/Newton derivation",
            "current_evidence": "memory generator is not removed or bounded",
            "gate_pass": "False",
            "claim_allowed": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2626_0_owner_hunt",
            "topic": "parent memory operator owner",
            "decision": "NOT_FOUND_CURRENT_CORPUS",
            "reason": "the actual parent X, D, L_X, J_X, source/boundary, and coupling owners are not all present",
            "next_action": "do not loop the same owner hunt unless new parent-action text is introduced",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC2626_1_relative_math",
            "topic": "positive-operator zero theorem",
            "decision": "RELATIVE_PROOF_RETAINED",
            "reason": "the energy identity is real and valuable under signed premises",
            "next_action": "treat it as an acceptance gate, not as an achieved local-GR proof",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC2626_2_residual_path",
            "topic": "finite memory residual",
            "decision": "TEMPLATE_INSTALLED_NONCLAIM",
            "reason": "failed zero theorem now has concrete source/gap/boundary/coupling inputs",
            "next_action": "fill source-backed rows only; no symbolic coefficient gets claim credit",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC2626_3_best_next",
            "topic": "next derivation route",
            "decision": "PARENT_MEMORY_SOURCE_BOUNDARY_MAP_IS_NEXT",
            "reason": "the main blocker is no longer the energy identity; it is J_X=0, boundary/zero-mode silence, and arena projection ownership",
            "next_action": "derive or bound J_X components and boundary lift, then only later score local arenas",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": "2627-Y5-R2FR-parent-memory-source-boundary-map-or-finite-residual-bound-pack.md",
            "script": "scripts/Y5_R2FR_parent_memory_source_boundary_map_or_finite_residual_bound_pack_2627.py",
            "objective": "derive J_X source decomposition and boundary/zero-mode package for the memory operator; if derivation fails, create finite residual input rows without claims",
            "include": "J_matter, J_chiD, J_boundary, J_readout, J_history, boundary_lift_norm, lambda_gap, K_i projection queue",
            "exclude": "local-GR claim, R10/PPN/clock/orbital pass, invented numeric coefficients, GitHub action, formalization-workbench edits",
            "valid_for_claim": "False",
        }
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        rows = read_csv(path)
        return bool(rows)
    except Exception:
        return False


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_specs = [
        ("COPY2626_owner_audit", "memory_operator_owner_audit", OUTPUTS["owner_audit"], LOCAL_BOUNDS / "Memory_operator_owner_hunt_2626_NONCLAIM.csv"),
        ("COPY2626_zero_theorem", "memory_positive_operator_zero_theorem_attempt", OUTPUTS["zero_theorem"], LOCAL_BOUNDS / "Memory_positive_operator_zero_theorem_attempt_2626_NONCLAIM.csv"),
        ("COPY2626_residual_template", "memory_residual_template", OUTPUTS["residual_template"], LOCAL_BOUNDS / "Memory_residual_template_2626_NONCLAIM.csv"),
        ("COPY2626_observable_queue", "memory_observable_coupling_queue", OUTPUTS["observable_queue"], LOCAL_BOUNDS / "Memory_observable_coupling_queue_2626_NONCLAIM.csv"),
        ("COPY2626_next_target", "next_target", OUTPUTS["next_target"], RAB_QUEUE / "JR2626_PARENT_MEMORY_SOURCE_BOUNDARY_NEXT.csv"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, label, source, destination in copy_specs:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            {
                "copy_id": copy_id,
                "label": label,
                "source_path": str(source),
                "destination_path": str(destination),
                "destination_exists": bool_text(destination.exists()),
                "csv_parses": bool_text(csv_parses(destination)),
                "row_count": len(read_csv(destination)) if destination.exists() else 0,
            }
        )
    return rows


def no_claim_flags(paths: list[Path]) -> bool:
    for path in paths:
        for row in read_csv(path):
            if row.get("valid_for_claim", "False") != "False":
                return False
            if row.get("claim_allowed", "False") != "False":
                return False
            if row.get("gate_pass", "False") == "True":
                return False
    return True


def missing_rows_not_ready(paths: list[Path]) -> bool:
    for path in paths:
        for row in read_csv(path):
            joined = " ".join(str(value) for value in row.values())
            if "MISSING_" in joined and row.get("valid_for_claim", "False") != "False":
                return False
    return True


def validation_rows(generated_paths: list[Path], branch_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_rows = read_csv(OUTPUTS["source_register"])
    owner_rows = read_csv(OUTPUTS["owner_audit"])
    zero_rows = read_csv(OUTPUTS["zero_theorem"])
    residual_rows = read_csv(OUTPUTS["residual_template"])
    queue_rows = read_csv(OUTPUTS["observable_queue"])
    gate_rows = read_csv(OUTPUTS["claim_gates"])
    decision_rows_read = read_csv(OUTPUTS["decision_ledger"])
    formalization_patterns = [
        "2626-Y5-R2FR-parent-memory-operator-owner-hunt-or-memory-residual-template.md",
        "Y5_R2FR_parent_memory_operator_owner_hunt_or_memory_residual_template_2626.py",
        f"{PREFIX}*",
        "P8_Y5_BRR545_2626_VALIDATION.csv",
        "Memory_operator_owner_hunt_2626_NONCLAIM.csv",
        "Memory_positive_operator_zero_theorem_attempt_2626_NONCLAIM.csv",
        "Memory_residual_template_2626_NONCLAIM.csv",
        "Memory_observable_coupling_queue_2626_NONCLAIM.csv",
        "JR2626_PARENT_MEMORY_SOURCE_BOUNDARY_NEXT.csv",
    ]
    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in formalization_patterns:
            formalization_hits.extend(FORMALIZATION.rglob(pattern))
    pycache_path = ROOT / "scripts" / "__pycache__"
    checks = [
        (
            "VAL2626_00_sources_exist",
            all(row["exists"] == "True" and row["needles_present"] == "True" for row in source_rows),
            "all cited source paths exist and needles are present",
        ),
        (
            "VAL2626_01_owner_hunt_recorded",
            any(row["audit_id"] == "MOA2626_9_verdict" and row["current_status"] == "NO_PARENT_MEMORY_OPERATOR_OWNER_FOUND_CURRENT_CORPUS" for row in owner_rows),
            "owner audit records no current parent memory operator owner",
        ),
        (
            "VAL2626_02_zero_theorem_relative",
            any(row["theorem_id"] == "ZPT2626_4_current_verdict" and row["math_status"] == "RELATIVE_THEOREM_READY_PARENT_INPUTS_UNSIGNED" for row in zero_rows),
            "positive-operator theorem retained only as relative proof",
        ),
        (
            "VAL2626_03_required_inputs_missing",
            sum(1 for row in owner_rows if row["current_status"].startswith("MISSING_")) >= 6,
            "activation inputs remain explicitly missing",
        ),
        (
            "VAL2626_04_residual_template_nonclaim",
            all(row["valid_for_claim"] == "False" for row in residual_rows),
            "memory residual template rows remain nonclaim",
        ),
        (
            "VAL2626_05_observable_couplings_blocked",
            all(row["current_status"] == "MISSING_ARENA_PROJECTION" and row["valid_for_claim"] == "False" for row in queue_rows),
            "all arena coupling rows remain blocked",
        ),
        (
            "VAL2626_06_claim_gates_safe",
            all(row["gate_pass"] == "False" and row["claim_allowed"] == "False" for row in gate_rows),
            "all memory/local-arena claim gates are false",
        ),
        (
            "VAL2626_07_no_claim_flags",
            no_claim_flags([OUTPUTS["owner_audit"], OUTPUTS["zero_theorem"], OUTPUTS["residual_template"], OUTPUTS["observable_queue"], OUTPUTS["countermodel"], OUTPUTS["decision_ledger"], OUTPUTS["next_target"]]),
            "no generated claim-sensitive row is valid_for_claim=true or claim_allowed=true",
        ),
        (
            "VAL2626_08_missing_not_ready",
            missing_rows_not_ready([OUTPUTS["owner_audit"], OUTPUTS["residual_template"], OUTPUTS["observable_queue"]]),
            "no MISSING_* row is marked claim-ready",
        ),
        (
            "VAL2626_09_decision_next",
            any(row["decision_id"] == "DEC2626_3_best_next" and row["decision"] == "PARENT_MEMORY_SOURCE_BOUNDARY_MAP_IS_NEXT" for row in decision_rows_read),
            "decision selects source/boundary map as the next target",
        ),
        (
            "VAL2626_10_branch_copies",
            all(row["destination_exists"] == "True" and row["csv_parses"] == "True" for row in branch_rows),
            "local bound and queue copies exist and parse",
        ),
        (
            "VAL2626_11_formalization_untouched",
            len(formalization_hits) == 0,
            "no 2626 outputs found under formalization-workbench",
        ),
        (
            "VAL2626_12_csv_parse",
            all(csv_parses(path) for path in generated_paths),
            "all generated 2626 CSVs parse",
        ),
        (
            "VAL2626_13_pycache_absent",
            not pycache_path.exists(),
            "scripts __pycache__ absent",
        ),
    ]
    rows = [
        {
            "check_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": "False",
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL2626_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "2626 parent memory operator owner hunt or memory residual template",
            "valid_for_claim": "False",
        }
    )
    return rows


def escape_md(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(escape_md(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def build_doc(tables: dict[str, list[dict[str, Any]]]) -> str:
    generated_at = datetime.now(timezone.utc).isoformat()
    return f"""# 2626 — Y5 R2/f(R) Parent Memory Operator Owner Hunt Or Memory Residual Template

Generated: `{generated_at}`

Status: `Y5_R2FR_2626_parent_memory_operator_owner_not_found_positive_operator_relative_memory_residual_template_nonclaim`

Claim ceiling: no parent memory action owner, no memory theorem-zero, no finite memory residual score, no R10/PPN/clock/orbital/WEP pass, no EH/Newton/local-GR claim is made.

## Summary

This checkpoint stops the memory branch from becoming fog. The good news is that the positive-operator route is mathematically real: if the parent supplies a signed operator, zero source, and zero boundary/zero-mode package, the energy identity can kill the local memory scalar without a plateau axiom.

The bad-news-but-useful-news is that the current corpus still does not own the ingredients. The parent `X`, selected local domain `D`, active `L_X`, `J_X` source map, boundary package, and arena couplings are not source-signed. So the theorem remains a relative gate, not a claimed local-GR proof. Chume, this is not a defeat; it is the exact pressure point.

## Source Register

{markdown_table(tables["source_register"])}

## Lineage Ledger

{markdown_table(tables["lineage_ledger"])}

## Parent Memory Operator Owner Audit

{markdown_table(tables["owner_audit"])}

## Positive-Operator Zero Theorem Attempt

{markdown_table(tables["zero_theorem"])}

## Memory Residual Template

{markdown_table(tables["residual_template"])}

## Observable Coupling Queue

{markdown_table(tables["observable_queue"])}

## Countermodel Ledger

{markdown_table(tables["countermodel"])}

## Claim Gates

{markdown_table(tables["claim_gates"])}

## Decision Ledger

{markdown_table(tables["decision_ledger"])}

## Next Target

{markdown_table(tables["next_target"])}

## Branch Copies

{markdown_table(tables["branch_copies"])}

## Validation

{markdown_table(tables["validation"])}

## Plain-English Verdict

We are not circling for sport here: the memory route has been compressed to one sharp missing mechanism. Either the future parent action proves `J_X=0` plus boundary silence while keeping an active positive operator, or the memory scalar must be treated as a finite residual with real source/gap/projection rows.

Best next target: derive or bound the component source map `J_X = J_matter + J_chiD + J_boundary + J_readout + J_history` and the boundary lift. If that closes, the positive-operator theorem can finally bite. If it does not, we stop pretending and make the finite local residual scoreable.
"""


def main() -> None:
    ensure_dirs()
    tables = {
        "source_register": source_register_rows(),
        "lineage_ledger": lineage_rows(),
        "owner_audit": owner_audit_rows(),
        "zero_theorem": zero_theorem_rows(),
        "residual_template": residual_template_rows(),
        "observable_queue": observable_queue_rows(),
        "countermodel": countermodel_rows(),
        "claim_gates": claim_gate_rows(),
        "decision_ledger": decision_rows(),
        "next_target": next_target_rows(),
    }
    for name, rows in tables.items():
        write_csv(OUTPUTS[name], rows)
    branch_rows = copy_branch_outputs()
    tables["branch_copies"] = branch_rows
    write_csv(OUTPUTS["branch_copies"], branch_rows)
    generated_paths = [path for key, path in OUTPUTS.items() if key not in {"validation"}]
    validation = validation_rows(generated_paths, branch_rows)
    tables["validation"] = validation
    write_csv(OUTPUTS["validation"], validation)
    DOC_PATH.write_text(build_doc(tables), encoding="utf-8")
    print(DOC_PATH)
    print(OUTPUTS["validation"])


if __name__ == "__main__":
    main()

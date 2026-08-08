from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

BRANCH_ID = "MTS_R2FR_PARENT_QLOC_RAB_PRIMITIVE_DERIVATION_AUDIT_2261"
DOC = ROOT / "2261-Y5-R2FR-RAB-parent-contract-derivation-from-MTS-primitives-or-first-live-residual-row.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2261_00_2260_doc",
        "source_key": "2260_doc",
        "source_path": ROOT / "2260-Y5-R2FR-RAB-source-boundary-readout-operator-protection-or-residual-validator.md",
        "needles": ["CON2260_6_joint_contract", "THM2260_0_statement", "NEXT2260_0_primary"],
        "role": "handoff: parent contract written but unsigned",
    },
    {
        "source_id": "SRC2261_01_2260_validation",
        "source_key": "2260_validation",
        "source_path": OUT / "P8_Y5_BRR545_2260_VALIDATION.csv",
        "needles": ["VAL2260_OVERALL", "PASS"],
        "role": "confirms 2260 passed before 2261 starts",
    },
    {
        "source_id": "SRC2261_02_2260_contract",
        "source_key": "2260_contract",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2260_PARENT_PROTECTION_CONTRACT.csv",
        "needles": ["CON2260_0_parent_sorts", "CON2260_6_joint_contract"],
        "role": "machine-readable parent protection contract",
    },
    {
        "source_id": "SRC2261_03_2260_acquisition",
        "source_key": "2260_acquisition",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2260_LIVE_RESIDUAL_ACQUISITION_QUEUE.csv",
        "needles": ["ACQ2260_0_parent_contract", "ACQ2260_8_tau_orbital"],
        "role": "nonclaim acquisition queue carried into derivation attempt",
    },
    {
        "source_id": "SRC2261_04_motion_load_contract",
        "source_key": "motion_load_contract",
        "source_path": ROOT / "01-motion-load-route-contract.md",
        "needles": ["Primitive Scaffold To Test", "The contract is to derive `p=1`, not fit it.", "Required Local-GR Gate"],
        "role": "post-checkpoint motion/time/space primitive scaffold and local-GR gate",
    },
    {
        "source_id": "SRC2261_05_observer_contract",
        "source_key": "observer_contract",
        "source_path": ROOT / "10-observer-map-symplectic-contract.md",
        "needles": ["R_AB = ln(T^2 S)", "J_q = 1", "contract not satisfied"],
        "role": "observer-cell definition of R_AB and missing theorem",
    },
    {
        "source_id": "SRC2261_06_action_principle",
        "source_key": "action_principle",
        "source_path": PROJECT_ROOT / "core-mts-framework" / "action-principle" / "the-motion-timespace-action-principle.md",
        "needles": ["ψ : ℝ⁴ → ℝ", "g_{μν}(x)", "L_matter", "G_{μν} + Γ_G g_{μν} = κ T_{μν}"],
        "role": "legacy MTS action-principle primitive: psi to metric plus matter coupling",
    },
    {
        "source_id": "SRC2261_07_fundamental_action",
        "source_key": "fundamental_action",
        "source_path": PROJECT_ROOT / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md",
        "needles": ["ψ : ℝ⁴ → ℝ", "A_MTS[ψ]", "g_{μν}", "L_matter"],
        "role": "legacy microscopic psi action and emergent metric statement",
    },
    {
        "source_id": "SRC2261_08_637_qmap",
        "source_key": "qmap_637",
        "source_path": OUT / "P8_Y5_R10_637_QUOTIENT_MAP_DERIVATION.csv",
        "needles": ["QM637_2_vertical_kernel", "conditional_math_pass", "valid_for_claim"],
        "role": "conditional quotient-kernel theorem available but not parent-signed",
    },
    {
        "source_id": "SRC2261_09_637_obs",
        "source_key": "obs_637",
        "source_path": OUT / "P8_Y5_R10_637_OBS_FUNCTOR_DERIVATION.csv",
        "needles": ["OF637_1_chain_rule", "constant/material-marker term survives", "valid_for_claim"],
        "role": "conditional observer functor and matter chain-rule audit",
    },
    {
        "source_id": "SRC2261_10_863_coframe",
        "source_key": "coframe_863",
        "source_path": OUT / "P8_Y5_R10_863_COFRAME_ZERO_THEOREM.csv",
        "needles": ["CZT863_0_chain_rule_zero", "CZT863_5_zero_verdict", "not_proven"],
        "role": "conditional coframe-zero theorem and missing parent signature",
    },
    {
        "source_id": "SRC2261_11_943_contract",
        "source_key": "coframe_contract_943",
        "source_path": OUT / "P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv",
        "needles": ["CFC943_2_matter_functor", "CFC943_7_contract_verdict", "contract_exact_but_unsigned"],
        "role": "same-coframe/coupling contract exact but unsigned",
    },
    {
        "source_id": "SRC2261_12_same_coframe",
        "source_key": "same_coframe_519",
        "source_path": OUT / "P8_Y5_SAME_COFRAME_PARENT_CLAUSE.csv",
        "needles": ["UOC519_0_single_coframe_field", "UOC519_5_no_conformal_disformal_shadow_frame", "conditional_clause_written"],
        "role": "same-observed-coframe clauses and guardrails",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2261_SOURCE_REGISTER.csv",
    "primitive_map": OUT / "P8_Y5_PARENT_QLOC_2261_PRIMITIVE_SUPPORT_MAP.csv",
    "contract_audit": OUT / "P8_Y5_PARENT_QLOC_2261_CONTRACT_DERIVATION_AUDIT.csv",
    "obstruction_ledger": OUT / "P8_Y5_PARENT_QLOC_2261_OBSTRUCTION_LEDGER.csv",
    "conditional_kernels": OUT / "P8_Y5_PARENT_QLOC_2261_CONDITIONAL_KERNELS.csv",
    "first_live_row": OUT / "P8_Y5_PARENT_QLOC_2261_FIRST_LIVE_NONCLAIM_ROW.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2261_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2261_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2261_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2261_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2261_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2261_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_live_row": QUEUE / "JR2261_FIRST_LIVE_NONCLAIM_RAB_PARENT_GAP_ROW.csv",
    "queue_decision": QUEUE / "JR2261_PARENT_DERIVATION_DECISION_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "RAB_parent_primitive_derivation_refusal_2261.csv",
    "beta_docs": BETA_DOCS / "RAB_PARENT_PRIMITIVE_DERIVATION_AUDIT_2261_NONCLAIM.csv",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        try:
            return str(path.relative_to(PROJECT_ROOT)).replace("\\", "/")
        except ValueError:
            return str(path)


def validation_pass(path: Path) -> bool:
    if not path.exists():
        return False
    rows = read_csv(path)
    if not rows:
        return False
    id_key = next((key for key in ("check_id", "validation_id", "id") if key in rows[0]), "")
    result_key = next((key for key in ("result", "status") if key in rows[0]), "")
    if not result_key:
        return False
    overall = [row for row in rows if id_key and "overall" in row.get(id_key, "").lower()]
    return all(row.get(result_key, "").lower() == "pass" for row in (overall or rows))


def source_path(key: str) -> Path:
    return next(source["source_path"] for source in SOURCES if source["source_key"] == key)


def source_refs(*keys: str) -> str:
    return ";".join(rel(source_path(key)) for key in keys)


def false_flags() -> dict[str, bool]:
    return {
        "primitive_derived": False,
        "parent_signed": False,
        "theorem_zero": False,
        "source_backed": False,
        "score_ready": False,
        "accepted_ready": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCES:
        path = source["source_path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": rel(path),
                "exists": exists,
                "needles": ";".join(source["needles"]),
                "needles_present": exists and all(needle in text for needle in source["needles"]),
                "validation_overall_pass": validation_pass(path) if "validation" in source["source_key"] else "",
                "role": source["role"],
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def primitive_support_map_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "primitive_id": "PRIM2261_0_motion_load",
            "primitive_object": "motion-load, clock residue, spatial routing",
            "source_path": source_refs("motion_load_contract"),
            "supports": "local weak-field route and demand that p=1/gamma=1 be derived",
            "does_not_support": "typed parent quotient Q or auxiliary A_R=(R_AB,Lambda_R)",
            "status": "PRIMITIVE_SCAFFOLD_NOT_PARENT_GRAMMAR",
            "contract_use": "sets local-GR target but does not sign protection contract",
        },
        {
            "primitive_id": "PRIM2261_1_observer_cell",
            "primitive_object": "observer coframe T,S and R_AB=ln(T^2 S)",
            "source_path": source_refs("observer_contract"),
            "supports": "dimensionless R_AB target and exact equivalence R_AB=0 <=> p=1",
            "does_not_support": "origin of the constraint J_q=1 or Lambda_R multiplier",
            "status": "RAB_DEFINED_NOT_DERIVED_ZERO",
            "contract_use": "defines the residual that the parent contract must eliminate",
        },
        {
            "primitive_id": "PRIM2261_2_psi_metric",
            "primitive_object": "psi field and emergent metric/coframe candidate",
            "source_path": source_refs("action_principle", "fundamental_action"),
            "supports": "public geometric data can be treated as coarse-grained functions of psi",
            "does_not_support": "kernel/quotient split proving R_AB is representative-only",
            "status": "PARTIAL_PRIMITIVE_SUPPORT",
            "contract_use": "supports Q candidate but not A_R verticality",
        },
        {
            "primitive_id": "PRIM2261_3_macroscopic_action",
            "primitive_object": "Einstein-like action plus L_matter and Gamma_G",
            "source_path": source_refs("action_principle", "fundamental_action"),
            "supports": "ordinary matter couples through the emergent metric in the legacy action",
            "does_not_support": "delta S_matter/delta R_AB=0 if R_AB changes the same metric seen by matter",
            "status": "MATTER_COUPLING_SUPPORTS_SAME_FRAME_NOT_JR_ZERO",
            "contract_use": "helps same-coframe gate but not matter-source silence",
        },
        {
            "primitive_id": "PRIM2261_4_quotient_chain_rule",
            "primitive_object": "q map, observed functor, coframe chain rule",
            "source_path": source_refs("qmap_637", "obs_637", "coframe_863", "coframe_contract_943"),
            "supports": "exact conditional proof that vertical representative directions do not affect observed coframe/matter",
            "does_not_support": "parent identification of R_AB as such a vertical direction",
            "status": "CONDITIONAL_KERNEL_AVAILABLE_NOT_PARENT_SIGNED",
            "contract_use": "strongest non-circular kernel if R_AB verticality can be proved",
        },
        {
            "primitive_id": "PRIM2261_5_same_coframe",
            "primitive_object": "single observed coframe for matter, clocks, photons, orbits",
            "source_path": source_refs("same_coframe_519", "coframe_contract_943"),
            "supports": "forbids shadow-frame repairs and species-dependent local calibration",
            "does_not_support": "algebraic elimination of R_AB before readout",
            "status": "POLICY_CONTRACT_NOT_PRIMITIVE_THEOREM",
            "contract_use": "guardrail against cheating, not an active zero theorem",
        },
    ]
    return [{**{"branch_id": BRANCH_ID}, **entry, **false_flags()} for entry in entries]


def contract_derivation_audit_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "contract_id": "CON2261_0_parent_sorts",
            "contract_clause": "typed parent sorts",
            "2260_requirement": "fields split into Q, A_R=(R_AB,Lambda_R), Psi, fixed markers theta/top, and boundary data",
            "primitive_evidence": "psi and emergent metric are present; observer R_AB is defined from T,S",
            "derivation_status": "PARTIAL_SUPPORT_NOT_DERIVED",
            "why_not_closed": "no primitive functor identifies A_R as auxiliary/redundant rather than physical observer-cell strain",
            "next_needed": "derive R_AB as vertical representative data in ker(Dq_R), or keep it finite",
            "source_path": source_refs("observer_contract", "action_principle", "fundamental_action"),
        },
        {
            "contract_id": "CON2261_1_action_image",
            "contract_clause": "parent action image",
            "2260_requirement": "S_parent lies in ParentGenerate[Q,theta,top,Psi] plus algebraic Lambda_R(R_AB-C_AB[Q])",
            "primitive_evidence": "legacy actions contain psi kinetic/nonlinear terms and macroscopic R, Gamma_G, L_matter",
            "derivation_status": "NOT_DERIVED",
            "why_not_closed": "no displayed primitive action contains Lambda_R, C_AB[Q], or a no-derivative algebraic R_AB block",
            "next_needed": "construct the algebraic auxiliary block from the observer-cell current instead of appending it",
            "source_path": source_refs("action_principle", "fundamental_action", "observer_contract"),
        },
        {
            "contract_id": "CON2261_2_matter_functor",
            "contract_clause": "matter/source descent",
            "2260_requirement": "S_matter descends through Q and Psi only, so J_R=0",
            "primitive_evidence": "matter couples to the emergent metric; conditional quotient/coframe chain rule exists",
            "derivation_status": "CONDITIONAL_KERNEL_NOT_ACTIVATED",
            "why_not_closed": "if R_AB changes the observed metric/coframe, matter varies with it; J_R=0 follows only if R_AB is proven vertical before matter coupling",
            "next_needed": "prove Dq_R[v_R]=0 and e_obs=Obs(q_R(Phi)) for the actual R_AB direction",
            "source_path": source_refs("action_principle", "obs_637", "coframe_863", "coframe_contract_943"),
        },
        {
            "contract_id": "CON2261_3_boundary_functor",
            "contract_clause": "boundary/corner descent",
            "2260_requirement": "boundary terms descend through Q-boundary data only, so B_R=Pi_R=Q_R=0",
            "primitive_evidence": "local contract names boundary/no-hair as open; quotient files require boundary silence separately",
            "derivation_status": "NOT_DERIVED",
            "why_not_closed": "no primitive boundary generator or exact edge-current calculation for R_AB appears in the cited parent materials",
            "next_needed": "derive exact/proper R_AB boundary charge or keep finite boundary momentum row",
            "source_path": source_refs("observer_contract", "qmap_637", "coframe_863"),
        },
        {
            "contract_id": "CON2261_4_readout_closure",
            "contract_clause": "readout/effective closure",
            "2260_requirement": "readout/reduction preserve parent image and do not regenerate R_AB transfer/tau operators",
            "primitive_evidence": "same-coframe guardrail and no-shadow-frame clauses exist",
            "derivation_status": "GUARDRAIL_NOT_THEOREM",
            "why_not_closed": "the guardrail forbids cheating but does not prove coarse-graining cannot regenerate a finite R_AB tau channel",
            "next_needed": "prove readout functor commutes with elimination/projection for R_AB, or source tau rows",
            "source_path": source_refs("same_coframe_519", "coframe_contract_943", "observer_contract"),
        },
        {
            "contract_id": "CON2261_5_operator_exclusion",
            "contract_clause": "operator grammar exclusion",
            "2260_requirement": "no derivative/vertical-metric constructors for A_R exist",
            "primitive_evidence": "the displayed primitive actions do not introduce R_AB derivatives because R_AB is not displayed as a primitive field",
            "derivation_status": "ABSENCE_NOT_GRAMMAR_PROOF",
            "why_not_closed": "lack of an explicit R_AB term is weaker than a parent grammar theorem forbidding generated D R_AB or D Lambda_R operators",
            "next_needed": "write ParentGenerate as a typed grammar and prove closure under reduction excludes D A_R",
            "source_path": source_refs("action_principle", "fundamental_action", "observer_contract"),
        },
        {
            "contract_id": "CON2261_6_joint_contract",
            "contract_clause": "single parent protection contract",
            "2260_requirement": "CON2260_0 through CON2260_5 are one indivisible primitive derivation",
            "primitive_evidence": "several pieces exist as conditional kernels/guardrails",
            "derivation_status": "JOINT_CONTRACT_NOT_DERIVED",
            "why_not_closed": "the missing common premise is R_AB parent ownership: physical variable, vertical representative, or finite residual",
            "next_needed": "attack R_AB ownership directly before any new empirical scoring",
            "source_path": source_refs("2260_contract", "observer_contract", "qmap_637", "coframe_863"),
        },
    ]
    return [{**{"branch_id": BRANCH_ID}, **entry, **false_flags()} for entry in entries]


def obstruction_ledger_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "obstruction_id": "OBS2261_0_RAB_ownership",
            "obstruction": "R_AB ownership not fixed",
            "technical_form": "R_AB may be a physical observed-cell strain, a vertical representative coordinate, or a finite residual",
            "effect": "blocks typed parent sorts, matter silence, boundary silence, readout silence, and operator exclusion together",
            "severity": "FATAL_TO_LOCAL_GR_CLAIM",
            "repair_route": "derive R_AB in ker(Dq_R) before variation, or demote to finite residual envelope",
            "source_path": source_refs("observer_contract", "qmap_637", "coframe_863"),
        },
        {
            "obstruction_id": "OBS2261_1_lambda_origin",
            "obstruction": "Lambda_R multiplier origin missing",
            "technical_form": "algebraic constraint Lambda_R(R_AB-C_AB[Q]) is useful but not primitive-generated",
            "effect": "the exact 2260 theorem remains a closure rule unless Lambda_R has a parent origin",
            "severity": "FATAL_TO_AUXILIARY_THEOREM",
            "repair_route": "derive Lambda_R from conserved observer-cell current or parent constraint algebra",
            "source_path": source_refs("observer_contract", "2260_contract"),
        },
        {
            "obstruction_id": "OBS2261_2_matter_descent",
            "obstruction": "matter descent only conditional",
            "technical_form": "S_matter through g/e_obs supports same-frame coupling, but not J_R=0 unless R_AB is vertical",
            "effect": "WEP/clock/PPN source silence cannot be claimed",
            "severity": "HIGH",
            "repair_route": "activate the quotient chain-rule theorem with a parent-signed R_AB vertical generator",
            "source_path": source_refs("action_principle", "obs_637", "coframe_contract_943"),
        },
        {
            "obstruction_id": "OBS2261_3_boundary_charge",
            "obstruction": "boundary charge silence missing",
            "technical_form": "no exact/proper R_AB boundary generator or zero-flux proof is currently sourced",
            "effect": "local exterior hair cannot be ruled out",
            "severity": "HIGH",
            "repair_route": "compute boundary variation for R_AB or retain B_R/Pi_R finite row",
            "source_path": source_refs("observer_contract", "coframe_863"),
        },
        {
            "obstruction_id": "OBS2261_4_operator_grammar",
            "obstruction": "operator grammar not formalized",
            "technical_form": "absence of R_AB derivatives in legacy prose is not a typed closure theorem",
            "effect": "Z_R=0 cannot be promoted",
            "severity": "HIGH",
            "repair_route": "write ParentGenerate grammar and prove derivative constructors cannot target A_R",
            "source_path": source_refs("fundamental_action", "2260_contract"),
        },
    ]
    return [{**{"branch_id": BRANCH_ID}, **entry, **false_flags()} for entry in entries]


def conditional_kernel_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "kernel_id": "KER2261_0_chain_rule",
            "kernel": "coframe chain-rule zero",
            "exact_if": "q_R exists, v_R in ker(Dq_R), e_obs=Obs(q_R(Phi)), and markers descend/fix",
            "proof_status": "MATHEMATICALLY_CLEAN_CONDITIONAL",
            "blocked_by": "R_AB vertical generator and marker ownership not parent-signed",
            "potential_payoff": "J_R and clock/readout direct source pullbacks vanish by chain rule",
            "source_path": source_refs("coframe_863", "obs_637"),
        },
        {
            "kernel_id": "KER2261_1_same_coframe",
            "kernel": "single observed coframe",
            "exact_if": "all matter, clocks, photons, rods, and orbital readouts use e_obs with no shadow frame",
            "proof_status": "CONTRACT_EXACT_BUT_UNSIGNED",
            "blocked_by": "same-coframe rule is a policy/parent clause, not derived from primitives",
            "potential_payoff": "prevents fake Newton/PPN agreement by changing source/readout frames",
            "source_path": source_refs("same_coframe_519", "coframe_contract_943"),
        },
        {
            "kernel_id": "KER2261_2_observer_cell",
            "kernel": "R_AB=0 equivalent to p=1/J_q=1",
            "exact_if": "future parent action produces J_q=1 without GR import or fitting",
            "proof_status": "TARGET_DEFINED_NOT_PROVEN",
            "blocked_by": "missing conserved cell current, genuine constraint, or gauge redundancy",
            "potential_payoff": "local gamma=1 route becomes structurally connected to R_AB=0",
            "source_path": source_refs("observer_contract", "motion_load_contract"),
        },
    ]
    return [{**{"branch_id": BRANCH_ID}, **entry, **false_flags()} for entry in entries]


def first_live_nonclaim_row() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "LIVE2261_0_RAB_parent_ownership_gap",
            "from_acquisition_id": "ACQ2260_0_parent_contract",
            "target": "R_AB_parent_ownership_and_parent_protection_contract",
            "quantity": "R_AB=ln(T^2 S)",
            "units": "dimensionless",
            "normalization": "observer-cell normalization from theta_0=T c dt, theta_1=sqrt(S) dr; J_q=T sqrt(S); R_AB=2 ln J_q",
            "source_paths": source_refs("observer_contract", "motion_load_contract", "qmap_637", "coframe_863", "coframe_contract_943"),
            "source_anchor": "10 defines R_AB and missing J_q=1 theorem; 637/863/943 give conditional quotient/coframe kernels",
            "candidate_value": "THEOREM_ZERO_CANDIDATE_IF_RAB_VERTICAL_AND_PARENT_SIGNED",
            "current_value": "MISSING_PARENT_RAB_OWNERSHIP_SIGNATURE",
            "arena_projection": "R10;PPN;WEP;clock;orbital",
            "status": "SOURCE_BACKED_GAP_ROW_NONCLAIM",
            "failure_mode": "conditional zero cannot be scored because R_AB is not yet derived as vertical/auxiliary rather than observed physical strain",
            "accepted_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def refusal_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "refusal_id": "REF2261_0_promote_contract",
            "attempted_claim": "parent protection contract derived from primitives",
            "runner_result": "BLOCKED",
            "blocked_by": "CON2261_6_joint_contract=JOINT_CONTRACT_NOT_DERIVED",
            "score_eligible": False,
        },
        {
            "refusal_id": "REF2261_1_JR_zero",
            "attempted_claim": "J_R=0 from matter descent",
            "runner_result": "BLOCKED",
            "blocked_by": "R_AB verticality not parent-signed; matter sees observed metric/coframe",
            "score_eligible": False,
        },
        {
            "refusal_id": "REF2261_2_ZR_zero",
            "attempted_claim": "Z_R=0 from operator grammar",
            "runner_result": "BLOCKED",
            "blocked_by": "operator exclusion is absence evidence, not typed grammar theorem",
            "score_eligible": False,
        },
        {
            "refusal_id": "REF2261_3_local_GR",
            "attempted_claim": "derived local GR/Newton/PPN safety",
            "runner_result": "BLOCKED",
            "blocked_by": "R_AB=0/J_q=1 remains target, not derived theorem",
            "score_eligible": False,
        },
        {
            "refusal_id": "REF2261_4_score_live_row",
            "attempted_claim": "first live row can be scored",
            "runner_result": "BLOCKED",
            "blocked_by": "row is source-backed gap ledger, not a numeric finite residual or parent-signed zero",
            "score_eligible": False,
        },
    ]
    return [{**{"branch_id": BRANCH_ID}, **entry, "valid_for_claim": False, "claim_allowed": False} for entry in entries]


def claim_gate_rows() -> list[dict[str, Any]]:
    entries = [
        ("CG2261_0_parent_contract", "parent protection contract", False, "primitive audit does not derive joint contract"),
        ("CG2261_1_RAB_vertical", "R_AB is vertical representative in ker(Dq_R)", False, "R_AB ownership is the selected missing premise"),
        ("CG2261_2_matter_zero", "J_R=0", False, "chain-rule kernel conditional on unsigned R_AB verticality"),
        ("CG2261_3_boundary_zero", "B_R/Pi_R/Q_R=0", False, "no boundary generator/exactness proof"),
        ("CG2261_4_operator_zero", "Z_R=0", False, "typed ParentGenerate grammar missing"),
        ("CG2261_5_local_GR_Newton", "local GR/Newton/PPN safety", False, "R_AB=0/J_q=1 not derived"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": claim_id,
            "claim": claim,
            "gate_pass": gate_pass,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for claim_id, claim, gate_pass, reason in entries
    ]


def decision_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "decision_id": "DEC2261_0_status",
            "decision": "PRIMITIVE_DERIVATION_ATTEMPT_FAILS_CURRENTLY",
            "reason": "motion/time/space and psi->metric materials support the target geometry but do not derive the typed R_AB auxiliary/vertical parent contract",
            "next_action": "do not claim local GR; attack R_AB ownership directly",
        },
        {
            "decision_id": "DEC2261_1_keep_kernel",
            "decision": "KEEP_CONDITIONAL_QUOTIENT_KERNEL",
            "reason": "637/863/943 provide a clean chain-rule zero if R_AB can be made vertical before matter/readout",
            "next_action": "try R_AB-as-quotient-representative derivation next",
        },
        {
            "decision_id": "DEC2261_2_live_row",
            "decision": "FIRST_LIVE_NONCLAIM_GAP_ROW_WRITTEN",
            "reason": "the missing object is now source-backed with units, normalization, anchors, arena projections, and explicit failure mode",
            "next_action": "use it as the first acquisition row, not as evidence",
        },
        {
            "decision_id": "DEC2261_3_next",
            "decision": "RAB_OWNERSHIP_OR_FINITE_ENVELOPE_NEXT",
            "reason": "all protection clauses depend on whether R_AB is physical, vertical, or finite",
            "next_action": "2262-Y5-R2FR-RAB-ownership-as-quotient-representative-or-finite-residual-envelope.md",
        },
    ]
    return [{**{"branch_id": BRANCH_ID}, **entry, "valid_for_claim": False, "claim_allowed": False} for entry in entries]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2261_0_primary",
            "next_target": "2262-Y5-R2FR-RAB-ownership-as-quotient-representative-or-finite-residual-envelope.md",
            "script": "scripts/Y5_R2FR_RAB_ownership_as_quotient_representative_or_finite_residual_envelope_2262.py",
            "objective": "prove R_AB is a vertical representative direction in the parent quotient before matter/readout, or demote the local route to a finite residual envelope with sourced rows",
            "selection_status": "selected",
            "success_condition": "either Dq_R[v_R]=0 with e_obs and S_matter descending before variation, or a source-ready finite residual envelope replaces the zero claim",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2261_1_parallel",
            "next_target": "2262b-Y5-R2FR-RAB-typed-ParentGenerate-operator-grammar.md",
            "script": "scripts/Y5_R2FR_RAB_typed_ParentGenerate_operator_grammar_2262b.py",
            "objective": "formalize the allowed parent constructors and prove or reject D A_R operator exclusion",
            "selection_status": "held_parallel",
            "success_condition": "grammar proves Z_R=0 or creates finite Z_R/M_R^2 coefficient rows",
            "valid_for_claim": False,
        },
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "copy_id": "BC2261_live_row",
            "source_path": rel(OUTPUTS["first_live_row"]),
            "target_path": rel(COPY_TARGETS["queue_live_row"]),
            "target_exists": COPY_TARGETS["queue_live_row"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["queue_live_row"]) if COPY_TARGETS["queue_live_row"].exists() else False,
            "reason": "first source-backed nonclaim R_AB parent ownership gap row",
        },
        {
            "branch_id": BRANCH_ID,
            "copy_id": "BC2261_decision",
            "source_path": rel(OUTPUTS["decision"]),
            "target_path": rel(COPY_TARGETS["queue_decision"]),
            "target_exists": COPY_TARGETS["queue_decision"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["queue_decision"]) if COPY_TARGETS["queue_decision"].exists() else False,
            "reason": "portable 2261 decision ledger",
        },
        {
            "branch_id": BRANCH_ID,
            "copy_id": "BC2261_branch_wep",
            "source_path": rel(OUTPUTS["claim_gates"]),
            "target_path": rel(COPY_TARGETS["branch_wep"]),
            "target_exists": COPY_TARGETS["branch_wep"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["branch_wep"]) if COPY_TARGETS["branch_wep"].exists() else False,
            "reason": "branch-locked local/WEP refusal gates",
        },
        {
            "branch_id": BRANCH_ID,
            "copy_id": "BC2261_beta_docs",
            "source_path": rel(OUTPUTS["contract_audit"]),
            "target_path": rel(COPY_TARGETS["beta_docs"]),
            "target_exists": COPY_TARGETS["beta_docs"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["beta_docs"]) if COPY_TARGETS["beta_docs"].exists() else False,
            "reason": "portable primitive derivation audit",
        },
    ]


def table(headers: list[str], rows: list[dict[str, Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", " ") for header in headers) + " |")
    return "\n".join(lines)


def validation_rows() -> list[dict[str, Any]]:
    source_rows = read_csv(OUTPUTS["source_register"])
    primitive_rows = read_csv(OUTPUTS["primitive_map"])
    audit_rows = read_csv(OUTPUTS["contract_audit"])
    obstruction_rows = read_csv(OUTPUTS["obstruction_ledger"])
    kernel_rows = read_csv(OUTPUTS["conditional_kernels"])
    live_rows = read_csv(OUTPUTS["first_live_row"])
    refusal = read_csv(OUTPUTS["refusal"])
    gates = read_csv(OUTPUTS["claim_gates"])
    next_rows = read_csv(OUTPUTS["next_target"])
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks = [
        (
            "VAL2261_0_sources_exist",
            all(row["exists"].lower() == "true" for row in source_rows),
            "all cited source paths exist",
        ),
        (
            "VAL2261_1_needles_present",
            all(row["needles_present"].lower() == "true" for row in source_rows),
            "all cited source needles are present",
        ),
        (
            "VAL2261_2_prior_validation",
            any(row["source_key"] == "2260_validation" and row["validation_overall_pass"].lower() == "true" for row in source_rows),
            "2260 validation passes",
        ),
        (
            "VAL2261_3_primitives_mapped",
            len(primitive_rows) >= 6 and any("RAB_DEFINED_NOT_DERIVED_ZERO" in row["status"] for row in primitive_rows),
            "primitive support map separates target geometry from derivation",
        ),
        (
            "VAL2261_4_contract_all_clauses",
            {row["contract_id"] for row in audit_rows}
            >= {
                "CON2261_0_parent_sorts",
                "CON2261_1_action_image",
                "CON2261_2_matter_functor",
                "CON2261_3_boundary_functor",
                "CON2261_4_readout_closure",
                "CON2261_5_operator_exclusion",
                "CON2261_6_joint_contract",
            },
            "all 2260 parent contract clauses audited against primitives",
        ),
        (
            "VAL2261_5_joint_not_derived",
            any(row["contract_id"] == "CON2261_6_joint_contract" and row["derivation_status"] == "JOINT_CONTRACT_NOT_DERIVED" for row in audit_rows),
            "joint contract correctly remains not derived",
        ),
        (
            "VAL2261_6_RAB_obstruction",
            any(row["obstruction_id"] == "OBS2261_0_RAB_ownership" and row["severity"] == "FATAL_TO_LOCAL_GR_CLAIM" for row in obstruction_rows),
            "R_AB ownership isolated as fatal blocker",
        ),
        (
            "VAL2261_7_conditional_kernel_retained",
            any(row["kernel_id"] == "KER2261_0_chain_rule" and row["proof_status"] == "MATHEMATICALLY_CLEAN_CONDITIONAL" for row in kernel_rows),
            "clean conditional quotient/coframe kernel retained",
        ),
        (
            "VAL2261_8_first_live_row_nonclaim",
            len(live_rows) == 1
            and live_rows[0]["status"] == "SOURCE_BACKED_GAP_ROW_NONCLAIM"
            and live_rows[0]["valid_for_claim"].lower() == "false",
            "first source-backed nonclaim gap row exists and remains nonclaim",
        ),
        (
            "VAL2261_9_refusal_runner_blocks",
            all(row["runner_result"] == "BLOCKED" and row["claim_allowed"].lower() == "false" for row in refusal),
            "refusal runner blocks all attempted claims",
        ),
        (
            "VAL2261_10_claim_gates_blocked",
            all(row["gate_pass"].lower() == "false" and row["valid_for_claim"].lower() == "false" for row in gates),
            "claim gates remain blocked",
        ),
        (
            "VAL2261_11_next_selected",
            any(row["route_id"] == "NEXT2261_0_primary" and row["selection_status"] == "selected" for row in next_rows),
            "2262 R_AB ownership target selected",
        ),
        (
            "VAL2261_12_csv_parse",
            all(parse_csv(path) for path in generated_csvs),
            "all generated 2261 CSVs parse",
        ),
        (
            "VAL2261_13_no_claim_flags",
            not any(
                row.get(key, "").lower() == "true"
                for path in generated_csvs
                for row in read_csv(path)
                for key in ("primitive_derived", "parent_signed", "theorem_zero", "accepted_ready", "valid_for_claim", "claim_allowed")
            ),
            "no generated primitive/parent/theorem/source/claim flags are true",
        ),
        (
            "VAL2261_14_branch_copies",
            all(row["target_exists"].lower() == "true" and row["target_parses"].lower() == "true" for row in read_csv(OUTPUTS["branch_copies"])),
            "branch/queue copies exist and parse",
        ),
        (
            "VAL2261_15_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
        ),
        (
            "VAL2261_16_formalization_no_2261",
            not any(FORMALIZATION.rglob("*2261*")),
            "formalization-workbench has no 2261 outputs",
        ),
    ]
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2261_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "2261 audits primitive derivation honestly, refuses local claims, writes first source-backed nonclaim R_AB ownership gap row, and selects 2262",
        }
    )
    return rows


def write_doc() -> None:
    source_rows = read_csv(OUTPUTS["source_register"])
    primitive_rows = read_csv(OUTPUTS["primitive_map"])
    audit_rows = read_csv(OUTPUTS["contract_audit"])
    obstruction_rows = read_csv(OUTPUTS["obstruction_ledger"])
    kernel_rows = read_csv(OUTPUTS["conditional_kernels"])
    live_rows = read_csv(OUTPUTS["first_live_row"])
    refusal_rows_ = read_csv(OUTPUTS["refusal"])
    gate_rows = read_csv(OUTPUTS["claim_gates"])
    decision_rows_ = read_csv(OUTPUTS["decision"])
    next_rows = read_csv(OUTPUTS["next_target"])
    copy_rows = read_csv(OUTPUTS["branch_copies"])
    validation = read_csv(OUTPUTS["validation"])

    sections = [
        "# 2261 - Y5/R2FR R_AB Parent Contract Derivation From MTS Primitives Or First Live Residual Row",
        "",
        "## Verdict",
        "",
        "2261 tries the derivation route first. The current motion/time/space and `ψ -> g/e_obs` materials support the local target, the same-coframe discipline, and a clean conditional quotient/coframe chain-rule kernel. They do **not** yet derive the whole parent protection contract.",
        "",
        "The key blocker is now sharply isolated: `R_AB = ln(T^2 S)` has not been parent-owned. It must be proved to be a vertical representative coordinate in `ker(Dq_R)` before matter/readout, or retained as a finite residual. Therefore no `J_R=0`, `B_R=0`, `Z_R=0`, local-GR/Newton, R10, PPN, WEP, clock, or orbital claim is made.",
        "",
        "A first source-backed nonclaim acquisition row is written for the `R_AB` parent-ownership gap. It is useful evidence management, not evidence of a pass.",
        "",
        "## Source Register",
        table(["source_id", "source_key", "source_path", "exists", "needles_present", "validation_overall_pass", "role"], source_rows),
        "",
        "## Primitive Support Map",
        table(["primitive_id", "primitive_object", "supports", "does_not_support", "status", "contract_use", "valid_for_claim"], primitive_rows),
        "",
        "## Contract Derivation Audit",
        table(["contract_id", "contract_clause", "derivation_status", "why_not_closed", "next_needed", "source_path", "valid_for_claim"], audit_rows),
        "",
        "## Obstruction Ledger",
        table(["obstruction_id", "obstruction", "technical_form", "effect", "severity", "repair_route", "valid_for_claim"], obstruction_rows),
        "",
        "## Conditional Kernels Retained",
        table(["kernel_id", "kernel", "exact_if", "proof_status", "blocked_by", "potential_payoff", "valid_for_claim"], kernel_rows),
        "",
        "## First Live Nonclaim Row",
        table(["row_id", "from_acquisition_id", "target", "quantity", "units", "normalization", "source_anchor", "current_value", "status", "accepted_ready", "valid_for_claim"], live_rows),
        "",
        "## Refusal Runner",
        table(["refusal_id", "attempted_claim", "runner_result", "blocked_by", "score_eligible", "valid_for_claim"], refusal_rows_),
        "",
        "## Claim Gates",
        table(["claim_id", "claim", "gate_pass", "reason", "valid_for_claim"], gate_rows),
        "",
        "## Decision Ledger",
        table(["decision_id", "decision", "reason", "next_action", "valid_for_claim"], decision_rows_),
        "",
        "## Next Target",
        table(["route_id", "next_target", "script", "objective", "selection_status", "success_condition"], next_rows),
        "",
        "## Branch Copies",
        table(["copy_id", "source_path", "target_path", "target_exists", "target_parses", "reason"], copy_rows),
        "",
        "## Validation",
        table(["check_id", "result", "detail"], validation),
        "",
        "## Working Interpretation",
        "",
        "This is progress, but not a victory lap. The theory now has a narrow route to local GR that is not vibes: prove `R_AB` is quotient-representative data before matter sees it. If that works, the conditional chain-rule kernels become dangerous in the good way. If it fails, the honest programme is a finite residual envelope with real coefficients and arena projections.",
        "",
        "So the next dragon is not broadly 'coupling' anymore. It is more surgical: who owns `R_AB` in the parent theory?",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    for directory in (OUT, QUEUE, MICROSCOPE, BETA_DOCS):
        directory.mkdir(parents=True, exist_ok=True)

    write_csv(OUTPUTS["source_register"], source_register_rows())
    write_csv(OUTPUTS["primitive_map"], primitive_support_map_rows())
    write_csv(OUTPUTS["contract_audit"], contract_derivation_audit_rows())
    write_csv(OUTPUTS["obstruction_ledger"], obstruction_ledger_rows())
    write_csv(OUTPUTS["conditional_kernels"], conditional_kernel_rows())
    write_csv(OUTPUTS["first_live_row"], first_live_nonclaim_row())
    write_csv(OUTPUTS["refusal"], refusal_rows())
    write_csv(OUTPUTS["claim_gates"], claim_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next_target"], next_target_rows())

    shutil.copyfile(OUTPUTS["first_live_row"], COPY_TARGETS["queue_live_row"])
    shutil.copyfile(OUTPUTS["decision"], COPY_TARGETS["queue_decision"])
    shutil.copyfile(OUTPUTS["claim_gates"], COPY_TARGETS["branch_wep"])
    shutil.copyfile(OUTPUTS["contract_audit"], COPY_TARGETS["beta_docs"])
    write_csv(OUTPUTS["branch_copies"], branch_copy_rows())

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

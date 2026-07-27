from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_COUPLING_CHAIN_GATE_2610"
CHECKPOINT_ID = "2610"

DOC = ROOT / "2610-Y5-R2FR-coupling-chain-source-double-zero-proof-or-Achain-bound.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_COUPLING_CHAIN_GATE_2610_SOURCE_REGISTER.csv",
    "lineage_ledger": OUT / "P8_Y5_COUPLING_CHAIN_GATE_2610_LINEAGE_LEDGER.csv",
    "coupling_source": OUT / "P8_Y5_COUPLING_CHAIN_GATE_2610_COUPLING_SOURCE_AUDIT.csv",
    "double_zero": OUT / "P8_Y5_COUPLING_CHAIN_GATE_2610_DOUBLE_ZERO_ORIGIN_AUDIT.csv",
    "selector_independence": OUT / "P8_Y5_COUPLING_CHAIN_GATE_2610_SELECTOR_INDEPENDENCE_AUDIT.csv",
    "achain_interface": OUT / "P8_Y5_COUPLING_CHAIN_GATE_2610_ACHAIN_BOUND_INTERFACE.csv",
    "source_zero": OUT / "P8_Y5_COUPLING_CHAIN_GATE_2610_SOURCE_ZERO_STATUS.csv",
    "claim_gates": OUT / "P8_Y5_COUPLING_CHAIN_GATE_2610_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_COUPLING_CHAIN_GATE_2610_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_COUPLING_CHAIN_GATE_2610_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_COUPLING_CHAIN_GATE_2610_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2610_VALIDATION.csv",
}

COPY_TARGETS = {
    "coupling_source": LOCAL_BOUNDS / "Coupling_chain_source_audit_2610_NONCLAIM.csv",
    "achain_interface": LOCAL_BOUNDS / "Achain_bound_interface_2610_NONCLAIM.csv",
    "source_zero": LOCAL_BOUNDS / "Coupling_chain_source_zero_status_2610_NONCLAIM.csv",
    "next_target": QUEUE / "JR2610_MATTER_WORLDTUBE_DESCENT_NEXT.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def with_stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": utc_now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        **row,
    }


def row_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (list, tuple, set)):
        return ";".join(str(item) for item in value)
    if value is None:
        return ""
    return str(value)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row_value(row.get(field, "")) for field in fields})


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), len(rows), ""
    except Exception as exc:
        return False, 0, str(exc)


def path_has_needles(path: Path, needles: list[str]) -> list[str]:
    if not path.exists():
        return needles
    text = path.read_text(encoding="utf-8", errors="replace")
    return [needle for needle in needles if needle not in text]


def false_flags() -> dict[str, bool]:
    return {
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "accepted_for_scoring": False,
    }


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        {
            "source_id": "SRC2610_00_2609_handoff_doc",
            "source_path": ROOT / "2609-Y5-R2FR-primitive-minimality-invariant-algebra-or-Aaffine-bound.md",
            "needles": ["NEXT2609_0_selected", "DEC2609_4_best_next", "VAL2609_OVERALL"],
            "role": "current handoff selecting coupling-chain double-zero proof",
        },
        {
            "source_id": "SRC2610_01_2609_aaffine_interface",
            "source_path": OUT / "P8_Y5_PRIMITIVE_PACKAGE_GATE_2609_AAFFINE_BOUND_INTERFACE.csv",
            "needles": ["AAI2609_0_zero_condition", "AAI2609_4_R_source_affine", "AAI2609_5_R_affine_arena"],
            "role": "current source envelope context before coupling-chain source",
        },
        {
            "source_id": "SRC2610_02_1759_doc",
            "source_path": ROOT / "1759-Y5-R2FR-coupling-chain-source-double-zero-proof-or-Achain-bound.md",
            "needles": ["CCS1759_0_target", "DZ1759_1_linear_gate_rejected", "VAL1759_OVERALL"],
            "role": "prior coupling-chain source double-zero proof attempt",
        },
        {
            "source_id": "SRC2610_03_1759_coupling_source",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1759_COUPLING_CHAIN_SOURCE_ATTEMPT.csv",
            "needles": ["CCS1759_0_target", "CCS1759_3_double_zero_sufficiency", "CCS1759_5_verdict"],
            "role": "prior coupling-chain source audit rows",
        },
        {
            "source_id": "SRC2610_04_1759_double_zero",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1759_DOUBLE_ZERO_GATE_AUDIT.csv",
            "needles": ["DZ1759_0_power_condition", "DZ1759_1_linear_gate_rejected", "DZ1759_5_FLRW_normalization"],
            "role": "prior double-zero origin and normalization rows",
        },
        {
            "source_id": "SRC2610_05_1759_selector",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1759_CHID_INDEPENDENCE_AUDIT.csv",
            "needles": ["CHI1759_0_auxiliary_scalar", "CHI1759_1_local_zero", "CHI1759_4_R11_silence"],
            "role": "prior chi_D/domain selector independence rows",
        },
        {
            "source_id": "SRC2610_06_1759_achain",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1759_ACHAIN_BOUND_INTERFACE.csv",
            "needles": ["AC1759_0_zero_condition", "AC1759_3_A_chain", "AC1759_4_R_chain"],
            "role": "prior A_chain finite fallback interface",
        },
        {
            "source_id": "SRC2610_07_1760_doc",
            "source_path": ROOT / "1760-Y5-R2FR-matter-worldtube-quotient-descent-or-Amatter-bound.md",
            "needles": ["MWD1760_0_target", "DEC1760_3_best_next", "VAL1760_OVERALL"],
            "role": "prior next route: matter/worldtube quotient descent",
        },
    ]
    rows: list[dict[str, Any]] = []
    for spec in specs:
        missing_needles = path_has_needles(spec["source_path"], spec["needles"])
        rows.append(
            with_stamp(
                {
                    "source_id": spec["source_id"],
                    "source_path": spec["source_path"],
                    "exists": spec["source_path"].exists(),
                    "missing_needles": missing_needles,
                    "source_pass": spec["source_path"].exists() and not missing_needles,
                    "role": spec["role"],
                    **false_flags(),
                }
            )
        )
    return rows


def lineage_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "step_id": "LIN2610_0_2609",
            "checkpoint": "2609",
            "question": "Which hidden source follows affine-source failure?",
            "result": "The coupling chain source is next: J_chain=f'(0) C_obs partial_X chi_D + f(0) delta_X C_obs.",
            "status": "CURRENT_HANDOFF_REBASED",
            "next_dependency": "coupling double-zero or selector independence",
        },
        {
            "step_id": "LIN2610_1_1759_double_zero",
            "checkpoint": "1759",
            "question": "What exactly kills the chain source?",
            "result": "At chi_D=0, f(0)=0 kills the direct term, while f'(0)=0 or partial_X chi_D=0 kills the chain term.",
            "status": "EXACT_CONDITION_IMPORTED",
            "next_dependency": "parent origin of double-zero or selector independence",
        },
        {
            "step_id": "LIN2610_2_1759_linear_gate",
            "checkpoint": "1759",
            "question": "Can a linear selector f=chi_D work?",
            "result": "No. f(0)=0 but f'(0)=1, so hidden selector exchange returns unless partial_X chi_D=0 is parent-derived.",
            "status": "LINEAR_GATE_REJECTED",
            "next_dependency": "do not use p=1 gate for local-GR branch",
        },
        {
            "step_id": "LIN2610_3_1759_candidates",
            "checkpoint": "1759",
            "question": "Are there natural double-zero origins?",
            "result": "Determinant/current, norm-square/Z2, and topological pairing routes are plausible but not parent-owned; FLRW branch normalization remains open.",
            "status": "CANDIDATES_NOT_SIGNED",
            "next_dependency": "A_chain interface or later parent activation law",
        },
        {
            "step_id": "LIN2610_4_1760_preview",
            "checkpoint": "1760",
            "question": "What hidden source comes after coupling chain?",
            "result": "Matter/worldtube X vertex and quotient descent are next: prove matter descends through q or carry A_matter.",
            "status": "NEXT_ROUTE_IMPORTED",
            "next_dependency": "2611 matter/worldtube quotient descent or A_matter bound",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def coupling_source_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CCS2610_0_target",
            "coupling-chain source zero",
            "J_chain=f'(0) C_obs partial_X chi_D + f(0) delta_X C_obs at chi_D=0",
            "TARGET_EXACT",
            "ZERO_IF_DOUBLE_ZERO_OR_SELECTOR_INDEPENDENCE",
            "need parent-owned f(0)=f'(0)=0 or partial_X chi_D=0; neither is signed",
        ),
        (
            "CCS2610_1_direct_term",
            "direct observed-coupling term",
            "f(0) delta_X C_obs",
            "CONDITIONAL_ZERO_IF_F0_ZERO",
            "REQUIRED_BY_LOCAL_SILENCE_CONTRACT_NOT_PARENT_ORIGIN",
            "f(0)=0 is a necessary gate condition, not a derived parent activation law",
        ),
        (
            "CCS2610_2_chain_term",
            "chain derivative term",
            "f'(0) C_obs partial_X chi_D",
            "MAIN_OBSTRUCTION",
            "NOT_ZEROED",
            "linear gate f=chi_D fails; f'(0)=0 or partial_X chi_D=0 must be parent-derived",
        ),
        (
            "CCS2610_3_double_zero_sufficiency",
            "quadratic or higher gate",
            "f(chi_D)=O(chi_D^2) gives f(0)=f'(0)=0",
            "EXACT_SUFFICIENT_CONTRACT",
            "SUFFICIENT_NOT_PARENT_DERIVED",
            "determinant/norm-square/topological origins remain conditional and FLRW normalization is open",
        ),
        (
            "CCS2610_4_selector_independence",
            "selector-independent local memory variable",
            "partial_X chi_D=0 on the local branch",
            "ALTERNATIVE_ZERO_ROUTE",
            "NOT_PARENT_DERIVED",
            "chi_D/domain selector remains an uneliminated invariant generator from 2609",
        ),
        (
            "CCS2610_5_verdict",
            "coupling-chain theorem verdict",
            "J_chain=0 is theorem-shaped but not parent-signed",
            "THEOREM_CONTRACT_READY_PARENT_UNSIGNED",
            "A_CHAIN_RETAINED",
            "missing parent double-zero origin, local chi_D zero/independence, and same-branch FLRW normalization",
        ),
    ]
    return [
        with_stamp(
            {
                "audit_id": audit_id,
                "claim_piece": claim_piece,
                "mathematical_form": mathematical_form,
                "status": status,
                "proof_status": proof_status,
                "gap": gap,
                **false_flags(),
            }
        )
        for audit_id, claim_piece, mathematical_form, status, proof_status, gap in rows
    ]


def double_zero_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DZ2610_0_power_condition",
            "Taylor order p>=2 at chi_D=0",
            "f(0)=0 and f'(0)=0",
            "DERIVED_AS_REQUIREMENT",
            "kills direct term and selector exchange at local zero",
            "MISSING_PARENT_ORIGIN_OF_DOUBLE_ZERO",
        ),
        (
            "DZ2610_1_linear_gate_rejected",
            "reject p=1 gate",
            "f(chi_D)=chi_D has f(0)=0 but f'(0)=1",
            "FAILS_LOCAL_BRANCH",
            "hidden selector exchange returns",
            "LINEAR_GATE_REQUIRES_EXPLICIT_COEFFICIENT_BRANCH",
        ),
        (
            "DZ2610_2_determinant_candidate",
            "determinant/current route",
            "J_C ~ det(Q_coh) ~ amplitude^3",
            "CANDIDATE_NOT_PARENT_SIGNED",
            "could give p>=3 without hand insertion",
            "MISSING_COHERENT_VOLUME_PARENT_KINEMATICS_AND_NORMALIZATION",
        ),
        (
            "DZ2610_3_norm_square_candidate",
            "norm-square/Z2 route",
            "f(chi_D)=||A_D||^2 or chi_D^2 under chi_D -> -chi_D",
            "CANDIDATE_NOT_PARENT_SIGNED",
            "natural source of p=2 activation",
            "MISSING_SELECTOR_AMPLITUDE_Z2_OR_NORM_SQUARE_PARENT_OWNER",
        ),
        (
            "DZ2610_4_topological_pairing_candidate",
            "quadratic class pairing route",
            "f_D ~ <J_rel,J_rel>_D or ||Pi_rel J_B||^2",
            "CANDIDATE_NOT_PARENT_SIGNED",
            "could make double-zero topological rather than fitted",
            "MISSING_RELATIVE_CHAIN_COHOMOLOGY_PROJECTOR_OWNER",
        ),
        (
            "DZ2610_5_FLRW_normalization",
            "same gate keeps cosmology branch active with derived amplitude",
            "p>=2 local silence must not overstrong-zero the FLRW/cosmology memory branch",
            "NOT_PARENT_DERIVED",
            "prevents local repair from killing the unified-field spine",
            "MISSING_BRANCH_NORMALIZATION_AND_PARENT_SELECTOR_RULE",
        ),
        (
            "DZ2610_6_verdict",
            "double-zero origin verdict",
            "double-zero is required and sufficient as a contract but has no parent origin yet",
            "REQUIREMENT_DERIVED_PARENT_ORIGIN_MISSING",
            "A_chain remains live unless a candidate route is parent-owned",
            "MISSING_ACTIVATION_LAW",
        ),
    ]
    return [
        with_stamp(
            {
                "audit_id": audit_id,
                "route": route,
                "mathematical_form": mathematical_form,
                "current_status": current_status,
                "derived_effect": derived_effect,
                "gap": gap,
                **false_flags(),
            }
        )
        for audit_id, route, mathematical_form, current_status, derived_effect, gap in rows
    ]


def selector_independence_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CHI2610_0_auxiliary_scalar",
            "chi_D is auxiliary scalar with no kinetic/local vector term",
            "S_D includes lambda_D(chi_D-Sigma_D), no K_chi(g,nabla chi)",
            "ADMISSIBLE_CONTRACT_NOT_PARENT_DERIVED",
            "gradient/vector selector stress can survive locally",
        ),
        (
            "CHI2610_1_local_zero",
            "chi_local=0",
            "b_local=0 or c_local=0 => Sigma_local=chi_local=0",
            "NOT_PARENT_DERIVED",
            "local memory activation and selector stress remain finite",
        ),
        (
            "CHI2610_2_selector_independence",
            "partial_X chi_D=0",
            "local vertical variables do not move the domain selector",
            "NOT_PARENT_DERIVED",
            "would kill f'(0) C_obs partial_X chi_D without double-zero",
        ),
        (
            "CHI2610_3_generator_debt_link",
            "chi_D remains invariant-algebra generator debt",
            "2609 keeps chi_D/domain selector as legal local marker/source generator",
            "DEBT_RETAINED",
            "selector-independence cannot be assumed after primitive package failed",
        ),
        (
            "CHI2610_4_R11_silence",
            "domain source-normalization operator is zero or executable",
            "c_domain_source_normalization_operator=0 or coefficient vector fills all mapped rows",
            "FAIL_CURRENT_CORPUS",
            "domain selector can reintroduce PPN/Newton source-normalization residuals",
        ),
        (
            "CHI2610_5_verdict",
            "selector independence verdict",
            "partial_X chi_D=0 is a valid zero route but not parent-signed",
            "SELECTOR_INDEPENDENCE_NOT_CLOSED",
            "A_fprime remains live",
        ),
    ]
    return [
        with_stamp(
            {
                "audit_id": audit_id,
                "claim_piece": claim_piece,
                "mathematical_form": mathematical_form,
                "current_status": current_status,
                "gap": gap,
                **false_flags(),
            }
        )
        for audit_id, claim_piece, mathematical_form, current_status, gap in rows
    ]


def achain_interface_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "AC2610_0_zero_condition",
            "Z_chain",
            "Z_chain=True if f(0)=0 and either f'(0)=0 or partial_X chi_D=0, with parent-owned local chi_D=0",
            "FALSE_PARENT_UNSIGNED",
            "J_chain=0 condition",
        ),
        (
            "AC2610_1_A_f0",
            "A_f0",
            "||f(0) delta_X C_obs||_{E*} or theorem-zero from f(0)=0",
            "MISSING_F0_ZERO_OR_A_F0",
            "direct observed-coupling source term",
        ),
        (
            "AC2610_2_A_fprime",
            "A_fprime",
            "||f'(0) C_obs partial_X chi_D||_{E*} or theorem-zero from f'(0)=0/partial_X chi_D=0",
            "MISSING_FPRIME_ZERO_OR_CHI_INDEPENDENCE_OR_A_FPRIME",
            "chain derivative source term",
        ),
        (
            "AC2610_3_A_chain",
            "A_chain",
            "A_chain <= A_f0 + A_fprime in one declared E* norm",
            "MISSING_COMMON_ESTAR_NORM_AND_CHAIN_VALUES",
            "||J_chain||_{E*} <= A_chain",
        ),
        (
            "AC2610_4_R_source_chain",
            "R_source_chain",
            "||R_source,chain||_{E*} <= U_B A_chain",
            "MISSING_ACHAIN_AND_ESTAR_UNITS",
            "retains repaired p_total=1 for bounded chain source unless internal silence is separately proved",
        ),
        (
            "AC2610_5_R_chain_arena",
            "R_chain_arena",
            "||R_chain,arena|| <= U_B ||P_arena L_X^{-1}|| A_chain",
            "MISSING_OPERATOR_INVERSE_ARENA_PROJECTION_AND_UNITS",
            "source residual response to coupling-chain hidden current",
        ),
    ]
    return [
        with_stamp(
            {
                "interface_id": interface_id,
                "quantity": quantity,
                "definition": definition,
                "current_status": current_status,
                "notes": notes,
                **false_flags(),
            }
        )
        for interface_id, quantity, definition, current_status, notes in rows
    ]


def source_zero_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "SZ2610_0_chain",
            "J_chain",
            "NOT_ZEROED",
            "double-zero condition is exact but parent origin and chi_D independence/local-zero are unsigned",
            "A_chain remains missing/nonclaim",
        ),
        (
            "SZ2610_1_double_zero",
            "f(0)=f'(0)=0",
            "REQUIREMENT_DERIVED_NOT_PARENT_ORIGIN",
            "variation test rejects linear gate and accepts p>=2 as sufficient",
            "determinant/norm-square/topological origins and FLRW normalization not derived",
        ),
        (
            "SZ2610_2_selector_independence",
            "partial_X chi_D=0",
            "NOT_DERIVED",
            "chi_D remains a 2609 invariant-generator debt",
            "do not claim chain source zero via selector independence",
        ),
        (
            "SZ2610_3_Achain",
            "A_chain interface",
            "FINITE_INTERFACE_STAGED_NONCLAIM",
            "A_chain<=A_f0+A_fprime and ||R_source,chain||<=U_B A_chain",
            "numeric/source-backed E* values and projection norms missing",
        ),
        (
            "SZ2610_4_source_silence",
            "S_cg(D_L=0,Y)",
            "NOT_DERIVED",
            "affine and coupling-chain hidden sources are nonzero/nonclaim, and matter/worldtube/boundary/history/tower/mu/kernel channels remain",
            "J_hidden not zero; matter/worldtube vertex is next derivation target",
        ),
        (
            "SZ2610_5_GR_Newton",
            "local GR/Newton bridge",
            "CLOSER_BUT_BLOCKED",
            "coupling-chain source is exact-conditional and ledgered, but not zeroed",
            "matter/worldtube, boundary/history, tower, mu_even, kernel and projection rows remain open",
        ),
    ]
    return [
        with_stamp(
            {
                "status_id": status_id,
                "quantity": quantity,
                "current_status": current_status,
                "evidence": evidence,
                "remaining_gap": remaining_gap,
                **false_flags(),
            }
        )
        for status_id, quantity, current_status, evidence, remaining_gap in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2610_0_f0_zero", "f(0)=0 is parent-derived on the local branch", "BLOCKED_PARENT_ACTIVATION_LAW_MISSING"),
        ("GATE2610_1_double_zero", "f'(0)=0 is parent-derived or selector is independent", "BLOCKED_DOUBLE_ZERO_OR_SELECTOR_INDEPENDENCE_UNSIGNED"),
        ("GATE2610_2_linear_gate", "linear f=chi_D is acceptable for local-GR branch", "BLOCKED_LINEAR_GATE_FAILS_LOCAL_SOURCE_TEST"),
        ("GATE2610_3_FLRW_normalization", "double-zero gate preserves FLRW/cosmology branch with derived amplitude", "BLOCKED_BRANCH_NORMALIZATION_MISSING"),
        ("GATE2610_4_Achain_score", "A_chain can be scored in local arenas", "BLOCKED_ESTAR_OPERATOR_PROJECTION_UNITS_MISSING"),
        ("GATE2610_5_local_GR_Newton", "local GR/Newton/PPN/R10/WEP branch can claim", "BLOCKED_NO_LOCAL_REENTRY"),
    ]
    return [
        with_stamp(
            {
                "gate_id": gate_id,
                "claim": claim,
                "gate_pass": False,
                "status": "BLOCKED_NO_CLAIM",
                "blocker": blocker,
                **false_flags(),
            }
        )
        for gate_id, claim, blocker in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2610_0_double_zero",
            "decision": "double-zero is required and sufficient as a contract",
            "reason": "p>=2 kills both direct and chain selector exchange at chi_D=0; p=1 fails because f'(0)=1",
            "effect": "do not use a linear selector for the local-GR branch",
        },
        {
            "decision_id": "DEC2610_1_parent_origin",
            "decision": "double-zero origin is not parent-derived",
            "reason": "determinant, norm-square/Z2 and topological-pairing origins are plausible but not signed parent action derivations",
            "effect": "retain A_chain unless a parent activation law is derived",
        },
        {
            "decision_id": "DEC2610_2_selector_independence",
            "decision": "partial_X chi_D zero is not derived",
            "reason": "chi_D/domain selector remains an invariant-generator debt and local zero is not parent-signed",
            "effect": "do not claim chain source zero via selector independence",
        },
        {
            "decision_id": "DEC2610_3_Achain",
            "decision": "write A_chain interface as nonclaim residual",
            "reason": "chain zero theorem failed, so A_f0/A_fprime/A_chain must remain explicit residual inputs",
            "effect": "use A_chain interface only as nonclaim source-envelope plumbing",
        },
        {
            "decision_id": "DEC2610_4_best_next",
            "decision": "select matter/worldtube quotient descent or A_matter bound",
            "reason": "affine and coupling-chain sources are now ledgered; next hidden source in J_hidden is ordinary matter/worldtube X coupling",
            "effect": "2611 should prove matter descends through q with no direct X source, or carry A_matter explicitly",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2610_0_selected",
            "selection_status": "selected",
            "target_file": "2611-Y5-R2FR-matter-worldtube-quotient-descent-or-Amatter-bound.md",
            "target_script": "scripts/Y5_R2FR_matter_worldtube_quotient_descent_or_Amatter_bound_2611.py",
            "task": "try to prove ordinary matter/worldtube terms descend through q and carry no direct X vertex; otherwise carry A_matter",
            "success_condition": "matter/worldtube hidden source is theorem-zero or explicit finite A_matter residual in E* units",
            "fallback_condition": "if matter descent remains unsigned, attack no-direct-matter-X-vertex grammar or A_direct/A_worldtube coefficients",
            "guardrails": "do not hide material source charge inside readout definitions; no local-GR claim; no GitHub; no formalization-workbench edits",
        },
        {
            "route_id": "NEXT2610_1_Achain_fallback",
            "selection_status": "held_fallback",
            "target_file": "2611b-Y5-R2FR-Achain-E-star-bound-runner.md",
            "target_script": "scripts/Y5_R2FR_Achain_E_star_bound_runner_2611b.py",
            "task": "turn A_f0/A_fprime/A_chain into a runnable nonclaim source-envelope interface with units and operator/projection norms",
            "success_condition": "finite chain residual can be evaluated as nonclaim input",
            "fallback_condition": "local branch remains closure-only",
            "guardrails": "score only after units, E* norm, operator inverse and arena projections are real",
        },
        {
            "route_id": "NEXT2610_2_activation_fallback",
            "selection_status": "held_fallback",
            "target_file": "2611c-Y5-R2FR-parent-activation-law-for-double-zero.md",
            "target_script": "scripts/Y5_R2FR_parent_activation_law_for_double_zero_2611c.py",
            "task": "try to parent-own determinant, norm-square/Z2, or topological-pairing origin for f(0)=f'(0)=0",
            "success_condition": "double-zero is derived from parent action and FLRW normalization is preserved",
            "fallback_condition": "use A_chain finite residual only",
            "guardrails": "do not choose f only because it passes local tests",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, target in COPY_TARGETS.items():
        source = OUTPUTS[key]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        rows.append(
            with_stamp(
                {
                    "copy_id": f"COPY2610_{key}",
                    "source_path": source,
                    "target_path": target,
                    "source_exists": source.exists(),
                    "target_exists": target.exists(),
                    **false_flags(),
                }
            )
        )
    return rows


def generated_rows_have_no_claim_flags(data: dict[str, list[dict[str, Any]]]) -> bool:
    forbidden_true_fields = {"valid_for_claim", "claim_allowed", "score_ready", "accepted_for_scoring", "valid_prediction_row"}
    for rows in data.values():
        for row in rows:
            for field in forbidden_true_fields:
                if row.get(field) is True:
                    return False
    return True


def missing_rows_not_ready(data: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in data.values():
        for row in rows:
            joined = " ".join(row_value(value) for value in row.values())
            if "MISSING" in joined:
                if row.get("score_ready") is True or row.get("claim_allowed") is True or row.get("valid_prediction_row") is True:
                    return False
    return True


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, condition: bool, notes: str, detail: str = "") -> None:
        rows.append(with_stamp({"check_id": check_id, "status": "PASS" if condition else "FAIL", "notes": notes, "detail": detail, "valid_for_claim": False}))

    add("VAL2610_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited source paths exist and needles are present")
    add("VAL2610_01_lineage_complete", {"2609", "1759", "1760"}.issubset({row["checkpoint"] for row in data["lineage"]}), "lineage covers current handoff, prior chain route and next matter route")
    add("VAL2610_02_double_zero_condition", any(row["audit_id"] == "CCS2610_0_target" and "f'(0)" in row["mathematical_form"] for row in data["coupling_source"]), "coupling source condition is recorded")
    add("VAL2610_03_linear_gate_rejected", any(row["audit_id"] == "DZ2610_1_linear_gate_rejected" and row["current_status"] == "FAILS_LOCAL_BRANCH" for row in data["double_zero"]), "linear gate is rejected")
    add("VAL2610_04_parent_origin_missing", any(row["audit_id"] == "DZ2610_6_verdict" and row["current_status"] == "REQUIREMENT_DERIVED_PARENT_ORIGIN_MISSING" for row in data["double_zero"]), "double-zero origin remains parent unsigned")
    add("VAL2610_05_selector_independence_unsigned", any(row["audit_id"] == "CHI2610_5_verdict" and row["current_status"] == "SELECTOR_INDEPENDENCE_NOT_CLOSED" for row in data["selector_independence"]), "selector independence remains unclosed")
    add("VAL2610_06_FLRW_normalization_retained", any(row["audit_id"] == "DZ2610_5_FLRW_normalization" for row in data["double_zero"]), "FLRW/cosmology normalization blocker is retained")
    add("VAL2610_07_Achain_interface_nonclaim", all(row["valid_for_claim"] is False and row["claim_allowed"] is False for row in data["achain_interface"]), "A_chain interface remains nonclaim")
    add("VAL2610_08_U_B_power_retained", any(row["interface_id"] == "AC2610_4_R_source_chain" and "U_B A_chain" in row["definition"] for row in data["achain_interface"]), "explicit U_B source-residual factor retained")
    add("VAL2610_09_source_zero_blocked", any(row["status_id"] == "SZ2610_0_chain" and row["current_status"] == "NOT_ZEROED" for row in data["source_zero"]), "chain source zero remains blocked")
    add("VAL2610_10_source_silence_blocked", any(row["status_id"] == "SZ2610_4_source_silence" and row["current_status"] == "NOT_DERIVED" for row in data["source_zero"]), "source silence remains blocked")
    add("VAL2610_11_claim_gates_safe", all(row["claim_allowed"] is False and row["gate_pass"] is False for row in data["claim_gates"]), "all claim gates remain blocked")
    add("VAL2610_12_no_claim_flags", generated_rows_have_no_claim_flags(data), "no generated row promotes scoring or claim flags")
    add("VAL2610_13_missing_not_ready", missing_rows_not_ready(data), "no MISSING_* row is marked ready")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in ("*COUPLING_CHAIN_GATE_2610*", "2610-Y5-R2FR-coupling-chain-source-double-zero-proof-or-Achain-bound.md", "*JR2610_MATTER_WORLDTUBE_DESCENT_NEXT*"):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add("VAL2610_14_no_formalization_artifacts", not formalization_artifacts, "no 2610 coupling-chain artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_artifacts))
    add("VAL2610_15_decision_next", any(row["decision_id"] == "DEC2610_4_best_next" for row in data["decisions"]), "decision selects matter/worldtube source route")
    add("VAL2610_16_next_selected", any(row["route_id"] == "NEXT2610_0_selected" and row["selection_status"] == "selected" for row in data["next"]), "next target selected")
    add("VAL2610_17_branch_copies", all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]), "nonclaim branch copies exist")
    add("VAL2610_18_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent")

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2610_CSV_{path.stem}", parsed, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2610_COPY_CSV_{key}", parsed, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(with_stamp({"check_id": "VAL2610_OVERALL", "status": "PASS" if overall else "FAIL", "notes": "2610 coupling-chain gate derives double-zero requirement, keeps A_chain nonclaim and selects matter/worldtube next", "detail": "", "valid_for_claim": False}))
    return rows


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    divider = "| " + " | ".join("---" for _ in fields) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(row_value(row.get(field, "")).replace("|", "/") for field in fields) + " |")
    return "\n".join([header, divider, *body])


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 2610: R2FR Coupling-Chain Source Double-Zero Proof Or Achain Bound",
        "",
        "**Status:** private nonclaim current-branch coupling-chain checkpoint. This does not claim `J_chain=0`, source silence, local GR, Newton, PPN, R10, WEP, clocks, or orbital closure.",
        "",
        "**Main result:** the coupling-chain source has a crisp local law. At `chi_D=0`, `J_chain=f'(0) C_obs partial_X chi_D + f(0) delta_X C_obs`. Therefore `f(0)=0` kills the direct term, but a linear gate `f(chi_D)=chi_D` still fails because `f'(0)=1`. The local branch needs either a parent-owned double-zero `f(0)=f'(0)=0` or a parent-owned selector independence law `partial_X chi_D=0`. Neither is signed in the current corpus. Determinant/current, norm-square/Z2, and topological-pairing origins are promising candidate mechanisms, but they are not parent-derived and they must preserve the FLRW/cosmology branch normalization. So `A_f0`, `A_fprime`, and `A_chain<=A_f0+A_fprime` remain explicit nonclaim residual rows, with `||R_source,chain||<=U_B A_chain`.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role", "valid_for_claim"]),
        "",
        "## Lineage Ledger",
        markdown_table(data["lineage"], ["step_id", "checkpoint", "question", "result", "status", "next_dependency", "valid_for_claim", "claim_allowed"]),
        "",
        "## Coupling Source Audit",
        markdown_table(data["coupling_source"], ["audit_id", "claim_piece", "mathematical_form", "status", "proof_status", "gap", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Double-Zero Origin Audit",
        markdown_table(data["double_zero"], ["audit_id", "route", "mathematical_form", "current_status", "derived_effect", "gap", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Selector Independence Audit",
        markdown_table(data["selector_independence"], ["audit_id", "claim_piece", "mathematical_form", "current_status", "gap", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Achain Bound Interface",
        markdown_table(data["achain_interface"], ["interface_id", "quantity", "definition", "current_status", "notes", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Source-Zero Status",
        markdown_table(data["source_zero"], ["status_id", "quantity", "current_status", "evidence", "remaining_gap", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Claim Gates",
        markdown_table(data["claim_gates"], ["gate_id", "claim", "gate_pass", "status", "blocker", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect", "valid_for_claim"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "success_condition", "fallback_condition", "guardrails", "valid_for_claim"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists", "valid_for_claim"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail", "valid_for_claim"]),
        "",
        "## Private Verdict",
        "",
        "This is a real tightening step. The coupling cannot be left vague: a linear selector fails the local source test, and the double-zero route is now the exact gate. The theory can still use a quadratic/topological/determinant-style activation later, but only if the parent action derives it and the cosmology branch survives. Until then, `A_chain` is the honest object. Next best punch: matter/worldtube quotient descent.",
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def build_data() -> dict[str, list[dict[str, Any]]]:
    return {
        "sources": source_register_rows(),
        "lineage": lineage_rows(),
        "coupling_source": coupling_source_rows(),
        "double_zero": double_zero_rows(),
        "selector_independence": selector_independence_rows(),
        "achain_interface": achain_interface_rows(),
        "source_zero": source_zero_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }


def main() -> None:
    data = build_data()

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["lineage_ledger"], data["lineage"])
    write_csv(OUTPUTS["coupling_source"], data["coupling_source"])
    write_csv(OUTPUTS["double_zero"], data["double_zero"])
    write_csv(OUTPUTS["selector_independence"], data["selector_independence"])
    write_csv(OUTPUTS["achain_interface"], data["achain_interface"])
    write_csv(OUTPUTS["source_zero"], data["source_zero"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])

    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])

    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)

    overall = next(row for row in data["validations"] if row["check_id"] == "VAL2610_OVERALL")
    print(f"wrote {DOC}")
    print(f"validation={OUTPUTS['validation']}")
    print(f"overall={overall['status']}")


if __name__ == "__main__":
    main()

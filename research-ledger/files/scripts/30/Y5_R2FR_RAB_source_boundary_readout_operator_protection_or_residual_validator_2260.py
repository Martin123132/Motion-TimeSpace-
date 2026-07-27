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

BRANCH_ID = "MTS_R2FR_PARENT_QLOC_RAB_PROTECTION_VALIDATOR_2260"
DOC = ROOT / "2260-Y5-R2FR-RAB-source-boundary-readout-operator-protection-or-residual-validator.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2260_00_2259_doc",
        "source_key": "2259_doc",
        "source_path": ROOT / "2259-Y5-R2FR-RAB-compatibility-object-bridge-or-residual-demotion.md",
        "needles": ["SC2259_1_operator_exclusion", "SC2259_4_readout_stability", "NEXT2259_0_primary"],
        "role": "current handoff: second-class protections selected next",
    },
    {
        "source_id": "SRC2260_01_2259_validation",
        "source_key": "2259_validation",
        "source_path": OUT / "P8_Y5_BRR545_2259_VALIDATION.csv",
        "needles": ["VAL2259_OVERALL", "PASS"],
        "role": "confirms 2259 passed before 2260 starts",
    },
    {
        "source_id": "SRC2260_02_2239_doc",
        "source_key": "2239_doc",
        "source_path": ROOT / "2239-Y5-R2FR-RAB-source-boundary-readout-protection-or-finite-ZR-validator.md",
        "needles": ["PROT2239_0_JR_matter", "PROT2239_4_joint", "VAL2239_OVERALL"],
        "role": "prior protection validator: all four protections unsigned and finite rows hard-rejected",
    },
    {
        "source_id": "SRC2260_03_2239_validation",
        "source_key": "2239_validation",
        "source_path": OUT / "P8_Y5_BRR545_2239_VALIDATION.csv",
        "needles": ["VAL2239_OVERALL", "PASS"],
        "role": "confirms 2239 passed",
    },
    {
        "source_id": "SRC2260_04_2239_protection",
        "source_key": "2239_protection",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2239_PROTECTION_PROOF_AUDIT.csv",
        "needles": ["PROT2239_0_JR_matter", "PROT2239_3_operator", "JOINT_PROTECTION_NOT_CLOSED"],
        "role": "machine-readable protection failure audit",
    },
    {
        "source_id": "SRC2260_05_2239_joint",
        "source_key": "2239_joint",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2239_JB_READOUT_OPERATOR_JOINT_GATE.csv",
        "needles": ["JOINT2239_0_eliminate_auxiliary", "JOINT2239_3_verdict"],
        "role": "joint protection gate blocks local claim",
    },
    {
        "source_id": "SRC2260_06_2239_validator",
        "source_key": "2239_validator",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2239_FINITE_ZR_VALIDATOR_SUMMARY.csv",
        "needles": ["VS2239_0_scan_counts", "NO_ACCEPTED_SOURCE_READY_ROWS"],
        "role": "finite residual validator summary",
    },
    {
        "source_id": "SRC2260_07_2240_doc",
        "source_key": "2240_doc",
        "source_path": ROOT / "2240-Y5-R2FR-RAB-parent-protection-contract-or-live-finite-ZR-source-acquisition.md",
        "needles": ["CON2240_6_joint_contract", "THM2240_0_statement", "VAL2240_OVERALL"],
        "role": "prior parent protection contract and live source queue",
    },
    {
        "source_id": "SRC2260_08_2240_validation",
        "source_key": "2240_validation",
        "source_path": OUT / "P8_Y5_BRR545_2240_VALIDATION.csv",
        "needles": ["VAL2240_OVERALL", "PASS"],
        "role": "confirms 2240 passed",
    },
    {
        "source_id": "SRC2260_09_2240_contract",
        "source_key": "2240_contract",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2240_PARENT_PROTECTION_CONTRACT.csv",
        "needles": ["CON2240_0_parent_sorts", "CON2240_6_joint_contract"],
        "role": "single parent protection contract clauses",
    },
    {
        "source_id": "SRC2260_10_2240_audit",
        "source_key": "2240_audit",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2240_CONTRACT_PROOF_AUDIT.csv",
        "needles": ["AUD2240_0_JR", "AUD2240_4_joint", "FAILED_CURRENT_PARENT_PROOF"],
        "role": "contract proof audit remains unsigned",
    },
    {
        "source_id": "SRC2260_11_2240_acquisition",
        "source_key": "2240_acquisition",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2240_LIVE_SOURCE_ACQUISITION_QUEUE.csv",
        "needles": ["ACQ2240_0_parent_contract", "ACQ2240_8_tau_orbital"],
        "role": "live but nonclaim finite residual acquisition queue",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2260_SOURCE_REGISTER.csv",
    "protection_audit": OUT / "P8_Y5_PARENT_QLOC_2260_PROTECTION_STATUS_AUDIT.csv",
    "parent_contract": OUT / "P8_Y5_PARENT_QLOC_2260_PARENT_PROTECTION_CONTRACT.csv",
    "conditional_theorem": OUT / "P8_Y5_PARENT_QLOC_2260_CONDITIONAL_THEOREM.csv",
    "acquisition_queue": OUT / "P8_Y5_PARENT_QLOC_2260_LIVE_RESIDUAL_ACQUISITION_QUEUE.csv",
    "validator": OUT / "P8_Y5_PARENT_QLOC_2260_RESIDUAL_VALIDATOR_STATUS.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2260_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2260_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2260_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2260_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2260_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2260_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_contract": QUEUE / "JR2260_PARENT_PROTECTION_CONTRACT_NONCLAIM.csv",
    "queue_acquisition": QUEUE / "JR2260_LIVE_RESIDUAL_ACQUISITION_QUEUE_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "RAB_parent_protection_contract_nonclaim_2260.csv",
    "beta_docs": BETA_DOCS / "RAB_PARENT_PROTECTION_CONTRACT_2260_NONCLAIM.csv",
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


def false_flags() -> dict[str, bool]:
    return {
        "theorem_zero": False,
        "parent_signed": False,
        "source_backed": False,
        "score_ready": False,
        "raw_ready": False,
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


def src(*keys: str) -> str:
    by_key = {source["source_key"]: source["source_path"] for source in SOURCES}
    return ";".join(rel(by_key[key]) for key in keys)


def protection_audit_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "PROT2260_0_JR",
            "J_R matter/source silence",
            "delta S_matter/delta R_AB=0 from matter descent through Q, Psi, theta/top only",
            "UNSIGNED_MATTER_DESCENT",
            "finite J_R/w_R/beta_source rows remain required if not derived",
        ),
        (
            "PROT2260_1_BR",
            "B_R/Pi_R/Q_R boundary silence",
            "boundary/corner/worldtube terms have no R_AB functional and no reciprocal charge",
            "UNSIGNED_BOUNDARY_SILENCE",
            "finite boundary/exterior-hair rows remain required if not derived",
        ),
        (
            "PROT2260_2_readout",
            "readout stability",
            "readout/effective reduction preserves ParentGenerate image and cannot regenerate R_AB transfer/tau terms",
            "UNSIGNED_READOUT_STABILITY",
            "finite tau_R10/tau_PPN/tau_clock/tau_orbital rows remain required if not derived",
        ),
        (
            "PROT2260_3_operator",
            "operator exclusion",
            "ParentGenerate has no D R_AB, D Lambda_R, G_vert, nabla_vert, or vertical Sobolev constructor",
            "BLOCKED_EXACT_CONDITIONAL",
            "finite Z_R/M_R^2/cross rows remain required if not derived",
        ),
        (
            "PROT2260_4_joint",
            "joint protection package",
            "all four protections must close together before the second-class route can claim local silence",
            "JOINT_PROTECTION_NOT_CLOSED",
            "no local-GR credit from separate unsigned clauses",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "protection_id": protection_id,
            "quantity": quantity,
            "required_statement": required,
            "current_status": status,
            "fallback_if_missing": fallback,
            "source_paths": src("2239_protection", "2240_audit", "2259_doc"),
            **false_flags(),
        }
        for protection_id, quantity, required, status, fallback in entries
    ]


def parent_contract_rows() -> list[dict[str, Any]]:
    entries = [
        ("CON2260_0_parent_sorts", "typed parent sorts", "fields split into public quotient Q, auxiliary A_R=(R_AB,Lambda_R), matter/readout Psi, fixed markers theta/top, boundary data", "SCHEMA_VALID_NOT_PARENT_DERIVED"),
        ("CON2260_1_action_image", "parent action image", "S_parent is in Image(ParentGenerate[Q,theta,top,Psi]) plus algebraic Lambda_R(R_AB-C_AB[Q,theta,top])", "SCHEMA_VALID_NOT_PARENT_DERIVED"),
        ("CON2260_2_matter_functor", "matter/source descent", "S_matter descends through Q and Psi only, so J_R=0", "UNSIGNED_MATTER_DESCENT"),
        ("CON2260_3_boundary_functor", "boundary/corner descent", "B descends through Q-boundary data only, so B_R=Pi_R=Q_R=0", "UNSIGNED_BOUNDARY_SILENCE"),
        ("CON2260_4_readout_closure", "readout/effective closure", "readout and reduction preserve the parent image and do not generate R_AB derivative or transfer operators", "UNSIGNED_READOUT_STABILITY"),
        ("CON2260_5_operator_exclusion", "operator grammar exclusion", "no derivative/vertical-metric constructors for A_R exist", "BLOCKED_EXACT_CONDITIONAL"),
        ("CON2260_6_joint_contract", "single parent protection contract", "CON2260_0 through CON2260_5 are one indivisible derivation from primitives", "CONTRACT_WRITTEN_NOT_SIGNED"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "contract_id": contract_id,
            "contract_clause": clause,
            "required_statement": required,
            "current_status": status,
            "missing_for_claim": "derive this from motion/time/space primitives rather than local closure need",
            "source_paths": src("2240_contract", "2259_doc"),
            **false_flags(),
        }
        for contract_id, clause, required, status in entries
    ]


def conditional_theorem_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "THM2260_0_statement",
            "If CON2260_0-5 are parent-signed, then R_AB is algebraically eliminated before readout with J_R=B_R=readout_regen=Z_R=0.",
            "EXACT_IF_CONTRACT_PARENT_SIGNED",
            "not claimable because the contract is schema-valid but not primitive-derived",
        ),
        (
            "THM2260_1_variation",
            "E_Lambda gives R_AB=C_AB[Q,theta,top]; E_R gives Lambda_R+J_R+delta B/delta R_AB+readout_regen=0.",
            "FORMAL_PASS_WITHIN_CONTRACT",
            "requires source, boundary, and readout protections jointly",
        ),
        (
            "THM2260_2_operator",
            "If ParentGenerate lacks R_AB derivative constructors, Z_R |D R_AB|^2 is outside the parent image.",
            "EXACT_IF_OPERATOR_GRAMMAR_PARENT_SIGNED",
            "current operator exclusion is exact-conditional only",
        ),
        (
            "THM2260_3_verdict",
            "The second-class theorem is a real target, not a completed local-GR reduction.",
            "NOT_CLAIMABLE",
            "needs parent proof or finite source-backed rows",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": theorem_id,
            "statement": statement,
            "status": status,
            "why_not_claimed": why,
            "source_paths": src("2240_doc", "2240_contract"),
            **false_flags(),
        }
        for theorem_id, statement, status, why in entries
    ]


def acquisition_queue_rows() -> list[dict[str, Any]]:
    entries = [
        ("ACQ2260_0_parent_contract", "internal_theory", "parent_protection_contract", "derive typed ParentGenerate grammar from MTS primitives", "all", "MISSING_PARENT_PROTECTION_DERIVATION"),
        ("ACQ2260_1_ZR", "internal_theory", "Z_R", "operator-exclusion theorem-zero or finite coefficient with units/normalization", "R10;PPN;clock;orbital", "MISSING_ZR_THEOREM_OR_COEFFICIENT"),
        ("ACQ2260_2_MR2", "internal_theory", "M_R^2", "mass-gap/range row tied to same R_AB normalization", "R10;PPN;clock;orbital", "MISSING_MR2_SOURCE"),
        ("ACQ2260_3_JR", "internal_theory", "J_R", "matter-source zero theorem or finite source coupling", "WEP;R10;PPN;clock", "MISSING_JR_SOURCE_OR_ZERO"),
        ("ACQ2260_4_BR", "internal_theory", "B_R_or_Pi_Rn", "boundary/corner zero theorem or finite boundary momentum bound", "R10;PPN;orbital", "MISSING_BR_SOURCE_OR_ZERO"),
        ("ACQ2260_5_tau_R10", "mixed_internal_external", "tau_R10", "projection from finite R_AB residual to alpha(lambda) with external R10 bound source", "R10", "MISSING_TAU_R10_PROJECTION"),
        ("ACQ2260_6_tau_PPN", "mixed_internal_external", "tau_PPN", "projection from finite residual to gamma/beta/preferred-frame vector", "PPN", "MISSING_TAU_PPN_PROJECTION"),
        ("ACQ2260_7_tau_clock", "mixed_internal_external", "tau_clock", "projection from finite residual to fractional clock/readout observable", "clock", "MISSING_TAU_CLOCK_PROJECTION"),
        ("ACQ2260_8_tau_orbital", "mixed_internal_external", "tau_orbital", "projection from finite residual to acceleration/timing observable", "orbital", "MISSING_TAU_ORBITAL_PROJECTION"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "acquisition_id": acquisition_id,
            "source_class": source_class,
            "target": target,
            "needed_evidence": evidence,
            "arena_projection": arena,
            "current_status": status,
            "source_paths": src("2240_acquisition", "2259_doc"),
            **false_flags(),
        }
        for acquisition_id, source_class, target, evidence, arena, status in entries
    ]


def validator_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "validator_id": "VALR2260_0_source_ready",
            "raw_rows": 0,
            "accepted_rows": 0,
            "accepted_ready_rows": 0,
            "docs_templates_scoreable": False,
            "status": "NO_LIVE_SCORE_ROWS",
            "rule": "no finite residual row may be scored until source path, source anchor, units, normalization, coefficient value/theorem-zero, and arena projection are real",
            **false_flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "validator_id": "VALR2260_1_external_bounds",
            "raw_rows": 0,
            "accepted_rows": 0,
            "accepted_ready_rows": 0,
            "docs_templates_scoreable": False,
            "status": "EXTERNAL_ARENA_SOURCES_NONCLAIM_ONLY",
            "rule": "R10/PPN/WEP/clock/orbital external sources are comparator/bound inputs, not MTS coefficient evidence",
            **false_flags(),
        },
    ]


def refusal_rows() -> list[dict[str, Any]]:
    entries = [
        ("REF2260_0_joint", "joint source/boundary/readout/operator protection closes", "BLOCKED", "PROT2260_4_joint=JOINT_PROTECTION_NOT_CLOSED"),
        ("REF2260_1_contract", "parent protection contract is derived from primitives", "BLOCKED", "CON2260_6_joint_contract=CONTRACT_WRITTEN_NOT_SIGNED"),
        ("REF2260_2_theorem", "J_R=B_R=readout_regen=Z_R=0 theorem activates", "BLOCKED", "conditional theorem premises unsigned"),
        ("REF2260_3_finite", "finite residual row scoring", "BLOCKED", "no raw/accepted source-ready rows"),
        ("REF2260_4_local_GR", "derived local GR/Newton/PPN safety", "BLOCKED", "neither theorem-zero nor finite residual envelope is ready"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "refusal_id": refusal_id,
            "attempted_claim": claim,
            "runner_result": result,
            "blocked_by": blocked_by,
            "score_eligible": False,
            **false_flags(),
        }
        for refusal_id, claim, result, blocked_by in entries
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    entries = [
        ("CG2260_0_contract", "parent protection contract", "contract is written but not primitive-derived"),
        ("CG2260_1_joint_zero", "J_R=B_R=readout_regen=Z_R=0", "zero theorem conditional on unsigned contract"),
        ("CG2260_2_finite_rows", "finite residual rows source-ready", "raw/accepted rows remain empty"),
        ("CG2260_3_external_bounds", "external arena bounds as evidence for MTS", "bounds are comparator inputs only, not MTS coefficient sources"),
        ("CG2260_4_local_GR_Newton", "derived local GR/Newton/PPN safety", "theorem-zero and finite residual routes both incomplete"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": claim_id,
            "claim": claim,
            "gate_pass": False,
            "reason": reason,
            **false_flags(),
        }
        for claim_id, claim, reason in entries
    ]


def decision_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "DEC2260_0_status",
            "PROTECTION_CONTRACT_WRITTEN_NOT_SIGNED",
            "2260 imports 2239/2240: the joint contract is precise and sufficient if signed, but not derived from motion/time/space primitives.",
            "do not claim local GR",
        ),
        (
            "DEC2260_1_theorem",
            "EXACT_CONDITIONAL_THEOREM_RETAINED",
            "inside the contract, E_Lambda/E_R and operator exclusion kill the R_AB leak package together.",
            "preserve as derivation target",
        ),
        (
            "DEC2260_2_acquisition",
            "LIVE_RESIDUAL_ACQUISITION_QUEUE_RETAINED",
            "if primitive derivation fails, source-backed finite rows are required before any empirical score.",
            "carry nonclaim acquisition queue",
        ),
        (
            "DEC2260_3_next",
            "PARENT_CONTRACT_DERIVATION_OR_FIRST_LIVE_ROW_NEXT",
            "the next non-circular step is either derive the contract from primitives or fill one real finite/theorem-zero row.",
            "2261-Y5-R2FR-RAB-parent-contract-derivation-from-MTS-primitives-or-first-live-residual-row.md",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            **false_flags(),
        }
        for decision_id, decision, reason, next_action in entries
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2260_0_primary",
            "next_target": "2261-Y5-R2FR-RAB-parent-contract-derivation-from-MTS-primitives-or-first-live-residual-row.md",
            "script": "scripts/Y5_R2FR_RAB_parent_contract_derivation_from_MTS_primitives_or_first_live_residual_row_2261.py",
            "objective": "attempt to derive the typed parent protection contract from motion/time/space primitives; if not derivable, fill the first nonclaim source-backed finite row or theorem-zero row from the 2260 acquisition queue",
            "selection_status": "selected",
            "success_condition": "contract becomes primitive-derived without closure insertion, or one finite residual input gains source path, anchor, units, normalization and arena projection while still nonclaim",
            "forbidden_claims": "promoting contract schema; accepting docs templates; local-GR/Newton/R10/PPN pass; scoring external bounds as MTS predictions",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2260_1_parallel",
            "next_target": "2261b-Y5-R2FR-RAB-external-bound-source-cache-for-residual-comparators.md",
            "script": "scripts/Y5_R2FR_RAB_external_bound_source_cache_for_residual_comparators_2261b.py",
            "objective": "cache external R10/PPN/WEP/clock/orbital comparator sources separately from MTS coefficient rows",
            "selection_status": "held_parallel",
            "success_condition": "external sources are locally cached with provenance but not used as MTS coefficient evidence",
            "forbidden_claims": "bound-only MTS pass; threshold anchors as full curves",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def copy_branch_rows() -> list[dict[str, Any]]:
    copies = [
        ("contract", OUTPUTS["parent_contract"], COPY_TARGETS["queue_contract"], "parent protection contract nonclaim copy"),
        ("acquisition", OUTPUTS["acquisition_queue"], COPY_TARGETS["queue_acquisition"], "live residual acquisition queue nonclaim copy"),
        ("branch_wep", OUTPUTS["claim_gates"], COPY_TARGETS["branch_wep"], "branch-locked local/WEP refusal gates"),
        ("beta_docs", OUTPUTS["decision"], COPY_TARGETS["beta_docs"], "portable parent protection decision ledger"),
    ]
    rows = []
    for copy_id, source_path, target_path, reason in copies:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": f"BC2260_{copy_id}",
                "source_path": rel(source_path),
                "target_path": rel(target_path),
                "target_exists": target_path.exists(),
                "target_parses": parse_csv(target_path),
                "reason": reason,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def validation_rows(paths: list[Path]) -> list[dict[str, Any]]:
    source_rows = read_csv(OUTPUTS["source_register"])
    protection = read_csv(OUTPUTS["protection_audit"])
    contract = read_csv(OUTPUTS["parent_contract"])
    theorem = read_csv(OUTPUTS["conditional_theorem"])
    acquisition = read_csv(OUTPUTS["acquisition_queue"])
    validator = read_csv(OUTPUTS["validator"])
    refusals = read_csv(OUTPUTS["refusal"])
    claims = read_csv(OUTPUTS["claim_gates"])
    decisions = read_csv(OUTPUTS["decision"])
    next_targets = read_csv(OUTPUTS["next_target"])
    copies = read_csv(OUTPUTS["branch_copies"])

    def check(check_id: str, passed: bool, detail: str) -> dict[str, Any]:
        return {"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail}

    csv_parse_ok = True
    for path in paths:
        try:
            parse_csv(path)
        except Exception:
            csv_parse_ok = False

    formalization_2260 = []
    if FORMALIZATION.exists():
        formalization_2260 = [path for path in FORMALIZATION.rglob("*2260*") if path.is_file()]

    protection_ids = {row["protection_id"] for row in protection}
    contract_ids = {row["contract_id"] for row in contract}
    acquisition_targets = {row["target"] for row in acquisition}
    all_rows = [row for path in paths for row in read_csv(path)]

    rows = [
        check("VAL2260_0_sources_exist", all(row["exists"] == "True" for row in source_rows), "all cited source paths exist"),
        check("VAL2260_1_needles_present", all(row["needles_present"] == "True" for row in source_rows), "all cited source needles are present"),
        check("VAL2260_2_prior_validations", all(row["validation_overall_pass"] in ("", "True") for row in source_rows), "2259, 2239, and 2240 validations pass where checked"),
        check("VAL2260_3_protection_coverage", {"PROT2260_0_JR", "PROT2260_1_BR", "PROT2260_2_readout", "PROT2260_3_operator", "PROT2260_4_joint"}.issubset(protection_ids), "protection audit covers source, boundary, readout, operator and joint clauses"),
        check("VAL2260_4_parent_contract_coverage", {"CON2260_0_parent_sorts", "CON2260_1_action_image", "CON2260_2_matter_functor", "CON2260_3_boundary_functor", "CON2260_4_readout_closure", "CON2260_5_operator_exclusion", "CON2260_6_joint_contract"}.issubset(contract_ids), "parent protection contract includes all required clauses"),
        check("VAL2260_5_contract_not_signed", any(row["contract_id"] == "CON2260_6_joint_contract" and row["current_status"] == "CONTRACT_WRITTEN_NOT_SIGNED" for row in contract), "contract explicitly remains unsigned"),
        check("VAL2260_6_conditional_theorem", any(row["theorem_id"] == "THM2260_0_statement" and row["status"] == "EXACT_IF_CONTRACT_PARENT_SIGNED" for row in theorem), "conditional theorem retained without claim"),
        check("VAL2260_7_acquisition_queue", {"parent_protection_contract", "Z_R", "M_R^2", "J_R", "B_R_or_Pi_Rn", "tau_R10", "tau_PPN", "tau_clock", "tau_orbital"}.issubset(acquisition_targets), "live residual acquisition queue covers contract and local arenas"),
        check("VAL2260_8_no_score_rows", all(row["status"] in ("NO_LIVE_SCORE_ROWS", "EXTERNAL_ARENA_SOURCES_NONCLAIM_ONLY") for row in validator), "validator refuses scoring and treats external bounds as nonclaim comparator inputs"),
        check("VAL2260_9_runner_refuses", all(row["runner_result"] == "BLOCKED" for row in refusals), "refusal runner blocks all current claims"),
        check("VAL2260_10_claim_gates_blocked", all(row["gate_pass"] == "False" for row in claims), "claim gates are blocked"),
        check("VAL2260_11_decision_next", any(row["decision_id"] == "DEC2260_3_next" and row["decision"] == "PARENT_CONTRACT_DERIVATION_OR_FIRST_LIVE_ROW_NEXT" for row in decisions), "decision selects parent derivation or first live row next"),
        check("VAL2260_12_next_selected", any(row["route_id"] == "NEXT2260_0_primary" and row["selection_status"] == "selected" for row in next_targets), "next target selected"),
        check("VAL2260_13_csv_parse", csv_parse_ok, "all generated 2260 CSVs parse"),
        check("VAL2260_14_no_claim_flags", all(row.get("valid_for_claim", "False") != "True" and row.get("claim_allowed", "False") != "True" and row.get("theorem_zero", "False") != "True" and row.get("parent_signed", "False") != "True" and row.get("score_ready", "False") != "True" and row.get("source_backed", "False") != "True" and row.get("accepted_ready", "False") != "True" for row in all_rows), "no generated theorem/parent/source/score/claim flags are true"),
        check("VAL2260_15_branch_copies", all(row["target_exists"] == "True" and row["target_parses"] == "True" for row in copies), "branch/queue copies exist and parse"),
        check("VAL2260_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        check("VAL2260_17_formalization_no_2260", not formalization_2260, "formalization-workbench has no 2260 outputs"),
    ]
    rows.append(
        check(
            "VAL2260_OVERALL",
            all(row["result"] == "PASS" for row in rows),
            "2260 imports the protection validator, writes the current parent protection contract, refuses local claims, and selects primitive contract derivation or first live residual row next",
        )
    )
    return rows


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def build_doc(
    source_rows: list[dict[str, Any]],
    protection: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    acquisition: list[dict[str, Any]],
    validator: list[dict[str, Any]],
    refusals: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_targets: list[dict[str, Any]],
    copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 2260 - Y5/R2FR R_AB Source/Boundary/Readout/Operator Protection Or Residual Validator",
            "## Verdict\n\n2260 imports the prior 2239/2240 protection work into the current branch. The parent protection contract is precise and jointly sufficient if signed: typed parent sorts, action-image exhaustion, matter descent, boundary descent, readout closure, and operator exclusion would kill `J_R`, `B_R`, `readout_regen`, and `Z_R` together.\n\nBut it is still not derived from motion/time/space primitives. Therefore no `Z_R=0`, `q_R=0`, local-GR/Newton, R10, PPN, WEP, clock, or orbital claim is made. The fallback is a live nonclaim acquisition queue; external arena sources are comparator inputs only, not MTS coefficient evidence.",
            "## Source Register\n" + markdown_table(source_rows, ["source_id", "source_key", "source_path", "exists", "needles_present", "validation_overall_pass", "role"]),
            "## Protection Status Audit\n" + markdown_table(protection, ["protection_id", "quantity", "required_statement", "current_status", "fallback_if_missing", "valid_for_claim"]),
            "## Parent Protection Contract\n" + markdown_table(contract, ["contract_id", "contract_clause", "required_statement", "current_status", "missing_for_claim", "valid_for_claim"]),
            "## Conditional Theorem\n" + markdown_table(theorem, ["theorem_id", "statement", "status", "why_not_claimed", "valid_for_claim"]),
            "## Live Residual Acquisition Queue\n" + markdown_table(acquisition, ["acquisition_id", "source_class", "target", "needed_evidence", "arena_projection", "current_status", "accepted_ready"]),
            "## Residual Validator Status\n" + markdown_table(validator, ["validator_id", "status", "rule", "score_ready", "valid_for_claim"]),
            "## Refusal Runner\n" + markdown_table(refusals, ["refusal_id", "attempted_claim", "runner_result", "blocked_by", "score_eligible", "valid_for_claim"]),
            "## Claim Gates\n" + markdown_table(claims, ["claim_id", "claim", "gate_pass", "reason", "valid_for_claim"]),
            "## Decision Ledger\n" + markdown_table(decisions, ["decision_id", "decision", "reason", "next_action", "valid_for_claim"]),
            "## Next Target\n" + markdown_table(next_targets, ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "## Branch Copies\n" + markdown_table(copies, ["copy_id", "source_path", "target_path", "target_exists", "target_parses", "reason"]),
            "## Validation\n" + markdown_table(validation, ["check_id", "result", "detail"]),
            "## Working Interpretation\n\nThis is now the cleanest fork. To get local GR honestly, the parent contract has to be derived from primitives, not merely adopted as a closure rule. If that derivation fails, the programme becomes a finite-residual programme with real source rows and arena kernels. That is not a defeat; it is the difference between field theory and vibes wearing a lab coat.",
        ]
    ) + "\n"


def main() -> None:
    remove_pycache()

    source_rows = source_register_rows()
    protection = protection_audit_rows()
    contract = parent_contract_rows()
    theorem = conditional_theorem_rows()
    acquisition = acquisition_queue_rows()
    validator = validator_rows()
    refusals = refusal_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_targets = next_target_rows()

    write_csv(OUTPUTS["source_register"], source_rows)
    write_csv(OUTPUTS["protection_audit"], protection)
    write_csv(OUTPUTS["parent_contract"], contract)
    write_csv(OUTPUTS["conditional_theorem"], theorem)
    write_csv(OUTPUTS["acquisition_queue"], acquisition)
    write_csv(OUTPUTS["validator"], validator)
    write_csv(OUTPUTS["refusal"], refusals)
    write_csv(OUTPUTS["claim_gates"], claims)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next_target"], next_targets)

    copies = copy_branch_rows()
    write_csv(OUTPUTS["branch_copies"], copies)

    generated = [
        OUTPUTS["source_register"],
        OUTPUTS["protection_audit"],
        OUTPUTS["parent_contract"],
        OUTPUTS["conditional_theorem"],
        OUTPUTS["acquisition_queue"],
        OUTPUTS["validator"],
        OUTPUTS["refusal"],
        OUTPUTS["claim_gates"],
        OUTPUTS["decision"],
        OUTPUTS["next_target"],
        OUTPUTS["branch_copies"],
    ]

    validation = validation_rows(generated)
    write_csv(OUTPUTS["validation"], validation)
    remove_pycache()
    validation = validation_rows(generated)
    write_csv(OUTPUTS["validation"], validation)

    DOC.write_text(
        build_doc(source_rows, protection, contract, theorem, acquisition, validator, refusals, claims, decisions, next_targets, copies, validation),
        encoding="utf-8",
    )

    if not all(row["result"] == "PASS" for row in validation):
        raise SystemExit("2260 validation failed")

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

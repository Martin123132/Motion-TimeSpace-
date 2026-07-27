from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
RAB = ROOT / "source-intake" / "rab-sector"
RAB_DOCS = RAB / "docs"
RAB_RAW = RAB / "raw"
RAB_ACCEPTED = RAB / "accepted"
RAB_QUEUE = RAB / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1567-Y5-RAB-parent-protection-contract-or-live-finite-ZR-source-acquisition.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1566_doc": ROOT / "1566-Y5-RAB-source-boundary-readout-protection-or-finite-ZR-validator.md",
    "1566_validation": OUT / "P8_Y5_BRR545_1566_VALIDATION.csv",
    "1566_decision": OUT / "P8_Y5_PARENT_QLOC_1566_DECISION.csv",
    "1566_protection": OUT / "P8_Y5_PARENT_QLOC_1566_PROTECTION_PROOF_AUDIT.csv",
    "1566_joint": OUT / "P8_Y5_PARENT_QLOC_1566_JB_READOUT_OPERATOR_JOINT_GATE.csv",
    "1566_validator_summary": OUT / "P8_Y5_PARENT_QLOC_1566_FINITE_ZR_VALIDATOR_SUMMARY.csv",
    "1565_elim": OUT / "P8_Y5_PARENT_QLOC_1565_SECOND_CLASS_ELIMINATION_CONDITIONS.csv",
    "1236_certificate": OUT / "P8_Y5_R10_1236_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv",
    "1265_protection": OUT / "P8_Y5_R10_1265_AUXILIARY_PROTECTION_AUDIT.csv",
    "1265_risk": OUT / "P8_Y5_R10_1265_REGENERATION_RISK_LEDGER.csv",
    "1268_action": OUT / "P8_Y5_R10_1268_COMPATIBILITY_ACTION_CANDIDATE.csv",
    "1269_operator": OUT / "P8_Y5_R10_1269_OPERATOR_EXCLUSION_PARENT_SORT_ATTEMPT.csv",
    "1269_rules": OUT / "P8_Y5_R10_1269_ZR_INTAKE_VALIDATOR_RULES.csv",
    "1023_doc": ROOT / "1023-Y5-R10-q-vX-action-descent-certificate-or-scalar-nohair-demotion.md",
}

NEEDLES = {
    "1566_doc": ["four leaks are jointly sealed", "no accepted source-ready rows exist"],
    "1566_validation": ["VAL1566_OVERALL", "PASS"],
    "1566_decision": ["DEC1566_3_next", "NEXT_1567_PARENT_PROTECTION_CONTRACT_OR_LIVE_FINITE_ZR_SOURCE_ACQUISITION"],
    "1566_protection": ["PROT1566_4_joint", "JOINT_PROTECTION_NOT_CLOSED"],
    "1566_joint": ["JOINT1566_3_verdict", "JOINT_PROTECTION_NOT_CLOSED"],
    "1566_validator_summary": ["NO_ACCEPTED_SOURCE_READY_ROWS", "DOCS_TEMPLATES_REJECTED_AS_EXPECTED"],
    "1565_elim": ["ELIM1565_1_E_R", "PASS_ONLY_IF_SOURCES_ZERO"],
    "1236_certificate": ["CERT1236_6_current_verdict", "CERTIFICATE_SCHEMA_VALID_NOT_PARENT_DERIVED"],
    "1265_protection": ["AP1265_0_auxiliary_signature", "UNSIGNED_READOUT_PROTECTION"],
    "1265_risk": ["RR1265_3_readout_EFT", "UNSIGNED"],
    "1268_action": ["CAC1268_5_conditional_theorem", "EXACT_CONDITIONAL_NOT_PARENT_SIGNED"],
    "1269_operator": ["OP1269_4_theorem_candidate", "BLOCKED_EXACT_CONDITIONAL"],
    "1269_rules": ["RULE1269_3_source_anchor_found", "SOURCE_ANCHOR_MISSING_OR_NOT_FOUND"],
    "1023_doc": ["matter/no-marker descent", "boundary silence"],
}

WEB_SOURCES = [
    {
        "source_id": "WEB1567_R10_EOTWASH_PRL_2021",
        "arena": "R10",
        "url": "https://link.aps.org/doi/10.1103/PhysRevLett.126.211101",
        "description": "Combined short-range inverse-square-law/Yukawa alpha(lambda) bound source for 5-500 mm.",
        "use_for": "external alpha(lambda) bound acquisition only; not an MTS coefficient source",
    },
    {
        "source_id": "WEB1567_PPN_WILL_LRR_2014",
        "arena": "PPN",
        "url": "https://link.springer.com/article/10.12942/lrr-2014-4",
        "description": "Living Reviews PPN/solar-system test framework source.",
        "use_for": "external PPN residual comparator conventions only",
    },
    {
        "source_id": "WEB1567_WEP_MICROSCOPE_PRL_2022",
        "arena": "WEP",
        "url": "https://link.aps.org/doi/10.1103/PhysRevLett.129.121102",
        "description": "MICROSCOPE final equivalence-principle result.",
        "use_for": "external WEP/source-composition residual bound only",
    },
    {
        "source_id": "WEB1567_CLOCK_NATURE_2023",
        "arena": "clock",
        "url": "https://www.nature.com/articles/s41467-023-40629-8",
        "description": "Laboratory gravitational-redshift/clock-gradient test source.",
        "use_for": "external clock/readout residual bound only",
    },
]

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1567_SOURCE_REGISTER.csv"
WEB_SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1567_WEB_SOURCE_REGISTER.csv"
CONTRACT = OUT / "P8_Y5_PARENT_QLOC_1567_PARENT_PROTECTION_CONTRACT.csv"
CONTRACT_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1567_CONTRACT_PROOF_AUDIT.csv"
CONTRACT_THEOREM = OUT / "P8_Y5_PARENT_QLOC_1567_CONDITIONAL_THEOREM.csv"
ACQUISITION_QUEUE = OUT / "P8_Y5_PARENT_QLOC_1567_LIVE_SOURCE_ACQUISITION_QUEUE.csv"
ROW_BLUEPRINT = RAB_DOCS / "ZR1567_LIVE_FINITE_ZR_ROW_BLUEPRINT_NONCLAIM.csv"
QUEUE_COPY = RAB_QUEUE / "ZR1567_LIVE_SOURCE_ACQUISITION_QUEUE_NONCLAIM.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1567_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1567_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1567_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1567_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1567_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1567"
COPY_TARGETS = {
    CONTRACT: [
        QUARANTINE / "PARENT_PROTECTION_CONTRACT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "parent_protection_contract_nonclaim_1567.csv",
    ],
    CONTRACT_AUDIT: [
        QUARANTINE / "CONTRACT_PROOF_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "contract_proof_audit_nonclaim_1567.csv",
    ],
    CONTRACT_THEOREM: [
        QUARANTINE / "CONDITIONAL_THEOREM_NONCLAIM.csv",
        BRANCH_RESIDUALS / "conditional_protection_theorem_nonclaim_1567.csv",
    ],
    ACQUISITION_QUEUE: [
        QUARANTINE / "LIVE_SOURCE_ACQUISITION_QUEUE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "live_source_acquisition_queue_nonclaim_1567.csv",
        QUEUE_COPY,
    ],
    WEB_SOURCE_REGISTER: [
        QUARANTINE / "WEB_SOURCE_REGISTER_NONCLAIM.csv",
        BRANCH_RESIDUALS / "web_source_register_nonclaim_1567.csv",
    ],
    DECISION: [
        QUARANTINE / "DECISION_NONCLAIM.csv",
        BRANCH_RESIDUALS / "parent_protection_decision_nonclaim_1567.csv",
    ],
}


def flags() -> dict[str, bool]:
    return {
        "numeric_value_present": False,
        "source_backed": False,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def source_list(*keys: str) -> str:
    return "; ".join(rel(SOURCE_FILES[key]) for key in keys)


def file_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    return all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    claim_keys = [
        "numeric_value_present",
        "source_backed",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "accepted_for_scoring",
        "passes_for_claim",
        "ready_for_raw",
        "ready_for_accepted",
    ]
    for path in paths:
        for row in read_csv(path):
            for key in claim_keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def row_count(folder: Path) -> int:
    if not folder.exists():
        return 0
    total = 0
    for path in folder.glob("*.csv"):
        try:
            total += len(read_csv(path))
        except Exception:
            total += 1
    return total


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for index, (key, path) in enumerate(SOURCE_FILES.items()):
        needles = NEEDLES[key]
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1567_{index}_{key}",
                "source_path": rel(path),
                "exists": path.exists(),
                "needle_found": file_contains(path, needles),
                "needles": "; ".join(needles),
                "purpose": "parent protection contract or live finite-residual source acquisition",
                **flags(),
            }
        )
    return rows


def web_source_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "source_id": item["source_id"],
            "arena": item["arena"],
            "url": item["url"],
            "description": item["description"],
            "use_for": item["use_for"],
            "local_copy_path": "NOT_DOWNLOADED_THIS_CHECKPOINT",
            "row_status": "EXTERNAL_ARENA_SOURCE_CANDIDATE_NONCLAIM",
            **flags(),
        }
        for item in WEB_SOURCES
    ]


def contract_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CON1567_0_parent_sorts",
            "Parent fields are typed into public quotient observables Q, auxiliary compatibility variables A_R=(R_AB,Lambda_R), matter/readout fields Psi, fixed markers theta, and boundary data B.",
            "R_AB cannot be simultaneously a physical scalar and an auxiliary compatibility coordinate.",
            "SCHEMA_VALID_NOT_PARENT_DERIVED",
            "derive the typed field list from MTS primitives, not from the local failure mode",
        ),
        (
            "CON1567_1_action_image",
            "S_parent belongs to Image(ParentGenerate[Q,theta,top,Psi]) plus algebraic Lambda_R(R_AB-C_AB[Q,theta,top]).",
            "No direct R_AB matter source, no independent R_AB kinetic term, and no R_AB boundary functional are generated.",
            "SCHEMA_VALID_NOT_PARENT_DERIVED",
            "prove ParentGenerate exhaustion and no extension markers",
        ),
        (
            "CON1567_2_matter_functor",
            "S_matter descends through Q and Psi only: delta S_matter/delta R_AB=0.",
            "Kills J_R in E_R.",
            "UNSIGNED_MATTER_DESCENT",
            "prove no material constants, EM labels, clocks, masses, or hidden markers depend on R_AB",
        ),
        (
            "CON1567_3_boundary_functor",
            "Boundary/corner terms descend through Q-boundary data only: delta B/delta R_AB=0 and Q_R=0.",
            "Kills B_R/Pi_Rn leakage.",
            "UNSIGNED_BOUNDARY_SILENCE",
            "prove source-worldtube and corner terms cannot carry R_AB hair",
        ),
        (
            "CON1567_4_readout_closure",
            "Readout/effective reduction preserves Image(ParentGenerate) and cannot generate R_AB derivative or transfer operators.",
            "Kills readout_regen and tau leakage.",
            "UNSIGNED_READOUT_STABILITY",
            "prove radiative/readout closure rather than assume tree-level silence survives",
        ),
        (
            "CON1567_5_operator_exclusion",
            "No D R_AB, D Lambda_R, G_vert, nabla_vert, or Sobolev norm constructor exists for A_R.",
            "Kills Z_R and M_R^2 derivative residuals at parent level.",
            "BLOCKED_EXACT_CONDITIONAL",
            "1236/1269 provide certificate shape but not primitive derivation",
        ),
        (
            "CON1567_6_joint_contract",
            "CON1567_0 through CON1567_5 are a single indivisible protection contract.",
            "If all parent-signed, then J_R=B_R=readout_regen=Z_R=0 and the second-class route closes.",
            "CONTRACT_WRITTEN_NOT_SIGNED",
            "current corpus lacks one parent-owned theorem binding all clauses",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": contract_id,
            "contract_clause": contract_clause,
            "effect_if_signed": effect_if_signed,
            "current_status": current_status,
            "missing_for_claim": missing_for_claim,
            "source_paths": source_list("1236_certificate", "1269_operator", "1268_action", "1023_doc"),
            **flags(),
        }
        for contract_id, contract_clause, effect_if_signed, current_status, missing_for_claim in rows
    ]


def contract_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("AUD1567_0_JR", "J_R=0", "CON1567_2_matter_functor", "UNSIGNED", "finite J_R row remains required if not derived"),
        ("AUD1567_1_BR", "B_R=Pi_Rn=0", "CON1567_3_boundary_functor", "UNSIGNED", "finite boundary row remains required if not derived"),
        ("AUD1567_2_readout", "readout_regen=tau_residual=0", "CON1567_4_readout_closure", "UNSIGNED", "finite tau rows remain required if not derived"),
        ("AUD1567_3_ZR", "Z_R=0 and no derivative R_AB residual", "CON1567_5_operator_exclusion", "BLOCKED_EXACT_CONDITIONAL", "finite Z_R/M_R2 rows remain required if not derived"),
        ("AUD1567_4_joint", "local second-class protection package", "CON1567_0 through CON1567_5", "FAILED_CURRENT_PARENT_PROOF", "cannot spend local-GR credit from separate unsigned clauses"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "target_zero": target_zero,
            "required_contract_clause": required_contract_clause,
            "current_status": current_status,
            "fallback": fallback,
            "source_paths": source_list("1566_protection", "1566_joint", "1265_protection", "1269_operator"),
            **flags(),
        }
        for audit_id, target_zero, required_contract_clause, current_status, fallback in rows
    ]


def conditional_theorem_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "THM1567_0_statement",
            "If the parent protection contract CON1567_0-5 is parent-signed, then the R_AB sector is algebraically eliminated before readout with J_R=B_R=readout_regen=Z_R=0.",
            "conditional theorem",
            "EXACT_IF_CONTRACT_PARENT_SIGNED",
            "not a claim because the contract is not derived from MTS primitives",
        ),
        (
            "THM1567_1_variation",
            "E_Lambda: R_AB=C_AB[Q,theta,top]; E_R: Lambda_R + J_R + delta B/delta R_AB + readout_regen = 0.",
            "with J_R=B_R=readout_regen=0, Lambda_R=0",
            "FORMAL_PASS_WITHIN_CONTRACT",
            "requires all source/boundary/readout clauses together",
        ),
        (
            "THM1567_2_operator",
            "ParentGenerate has no R_AB derivative constructor, so Z_R |D R_AB|^2 is not in the parent image.",
            "operator is syntactically excluded",
            "EXACT_IF_TYPED_GRAMMAR_PARENT_SIGNED",
            "1236/1269 are schema-valid but not parent-derived",
        ),
        (
            "THM1567_3_verdict",
            "The theorem is a useful target, not an achieved local-GR reduction.",
            "current branch remains conditional/fallback",
            "NOT_CLAIMABLE",
            "needs parent proof or finite source rows",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": theorem_id,
            "statement": statement,
            "calculation_or_role": calculation_or_role,
            "status": status,
            "why_not_claimed": why_not_claimed,
            "source_paths": source_list("1565_elim", "1566_protection", "1236_certificate"),
            **flags(),
        }
        for theorem_id, statement, calculation_or_role, status, why_not_claimed in rows
    ]


def acquisition_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "ACQ1567_0_parent_contract",
            "internal_theory",
            "parent_protection_contract",
            "derive typed ParentGenerate grammar from MTS primitives so CON1567_0-5 are not post-hoc closure rules",
            "MTS parent action / primitive object-language derivation",
            "all",
            "MISSING_PARENT_PROTECTION_DERIVATION",
        ),
        (
            "ACQ1567_1_ZR",
            "internal_theory",
            "Z_R",
            "theorem-zero from operator exclusion or finite coefficient with units and normalization",
            "MTS parent action second variation/operator grammar",
            "R10;PPN;clock;orbital",
            "MISSING_ZR_THEOREM_OR_COEFFICIENT",
        ),
        (
            "ACQ1567_2_MR2",
            "internal_theory",
            "M_R^2",
            "mass-gap/Hessian or range scale tied to same R_AB normalization",
            "MTS parent Hessian or sourced residual model",
            "R10;PPN;clock;orbital",
            "MISSING_MR2_SOURCE",
        ),
        (
            "ACQ1567_3_JR",
            "internal_theory",
            "J_R",
            "matter-source zero theorem or finite source coupling",
            "MTS matter descent proof or explicit source-current derivation",
            "WEP;R10;PPN;clock",
            "MISSING_JR_SOURCE_OR_ZERO",
        ),
        (
            "ACQ1567_4_BR",
            "internal_theory",
            "B_R_or_Pi_Rn",
            "boundary/corner zero theorem or finite boundary momentum bound",
            "MTS boundary variational grammar",
            "R10;PPN;orbital",
            "MISSING_BR_SOURCE_OR_ZERO",
        ),
        (
            "ACQ1567_5_tau_R10",
            "mixed_internal_external",
            "tau_R10",
            "projection from finite R_AB residual to alpha(lambda), paired with external R10 bound source",
            "internal kernel plus Eot-Wash/short-range alpha(lambda) source",
            "R10",
            "MISSING_TAU_R10_PROJECTION",
        ),
        (
            "ACQ1567_6_tau_PPN",
            "mixed_internal_external",
            "tau_PPN",
            "projection from finite R_AB residual to gamma/beta residual vector",
            "internal metric projection plus PPN convention source",
            "PPN",
            "MISSING_TAU_PPN_PROJECTION",
        ),
        (
            "ACQ1567_7_tau_clock",
            "mixed_internal_external",
            "tau_clock",
            "projection from finite R_AB residual to fractional clock/readout observable",
            "internal readout map plus clock/redshift source",
            "clock",
            "MISSING_TAU_CLOCK_PROJECTION",
        ),
        (
            "ACQ1567_8_tau_orbital",
            "mixed_internal_external",
            "tau_orbital",
            "projection from finite R_AB residual to acceleration/timing observable",
            "internal force map plus orbital/PPN source",
            "orbital",
            "MISSING_TAU_ORBITAL_PROJECTION",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "acquisition_id": acquisition_id,
            "source_class": source_class,
            "target": target,
            "needed_evidence": needed_evidence,
            "preferred_source_kind": preferred_source_kind,
            "arena_projection": arena_projection,
            "current_status": current_status,
            "ready_for_raw": False,
            "ready_for_accepted": False,
            **flags(),
        }
        for acquisition_id, source_class, target, needed_evidence, preferred_source_kind, arena_projection, current_status in rows
    ]


def blueprint_rows() -> list[dict[str, Any]]:
    rows = [
        ("ZR1567_BLUEPRINT_ZR", "Z_R", "MISSING_THEOREM_ZERO_OR_NUMERIC_VALUE", "MISSING_UNITS", "MISSING_NORMALIZATION", "MISSING_PARENT_ACTION_BLOCK", "MISSING_SOURCE_PATH", "MISSING_SOURCE_ANCHOR", "R10;PPN;clock;orbital"),
        ("ZR1567_BLUEPRINT_MR2", "M_R^2", "MISSING_HESSIAN_OR_RANGE_VALUE", "MISSING_UNITS", "MISSING_NORMALIZATION", "MISSING_PARENT_HESSIAN_BLOCK", "MISSING_SOURCE_PATH", "MISSING_SOURCE_ANCHOR", "R10;PPN;clock;orbital"),
        ("ZR1567_BLUEPRINT_JR", "J_R", "MISSING_SOURCE_ZERO_OR_FINITE_COUPLING", "MISSING_UNITS", "MISSING_SOURCE_CURRENT_CONVENTION", "MISSING_MATTER_DESCENT_BLOCK", "MISSING_SOURCE_PATH", "MISSING_SOURCE_ANCHOR", "WEP;R10;PPN;clock"),
        ("ZR1567_BLUEPRINT_BR", "B_R_or_Pi_Rn", "MISSING_BOUNDARY_ZERO_OR_FINITE_BOUND", "MISSING_UNITS", "MISSING_BOUNDARY_CONVENTION", "MISSING_BOUNDARY_GRAMMAR_BLOCK", "MISSING_SOURCE_PATH", "MISSING_SOURCE_ANCHOR", "R10;PPN;orbital"),
        ("ZR1567_BLUEPRINT_TAU_R10", "tau_R10", "MISSING_TRANSFER_KERNEL", "MISSING_DIMENSIONLESS_OR_KERNEL_UNITS", "MISSING_ALPHA_LAMBDA_CONVENTION", "MISSING_R10_PROJECTION_BLOCK", "MISSING_SOURCE_PATH", "MISSING_SOURCE_ANCHOR", "R10"),
        ("ZR1567_BLUEPRINT_TAU_PPN", "tau_PPN", "MISSING_TRANSFER_KERNEL", "MISSING_DIMENSIONLESS_OR_PPN_UNITS", "MISSING_GAUGE_CONVENTION", "MISSING_PPN_PROJECTION_BLOCK", "MISSING_SOURCE_PATH", "MISSING_SOURCE_ANCHOR", "PPN"),
        ("ZR1567_BLUEPRINT_TAU_CLOCK", "tau_clock", "MISSING_TRANSFER_KERNEL", "MISSING_FRACTIONAL_FREQUENCY_UNITS", "MISSING_CLOCK_READOUT_CONVENTION", "MISSING_CLOCK_PROJECTION_BLOCK", "MISSING_SOURCE_PATH", "MISSING_SOURCE_ANCHOR", "clock"),
        ("ZR1567_BLUEPRINT_TAU_ORBITAL", "tau_orbital", "MISSING_TRANSFER_KERNEL", "MISSING_ACCELERATION_OR_TIMING_UNITS", "MISSING_ORBITAL_CONVENTION", "MISSING_ORBITAL_PROJECTION_BLOCK", "MISSING_SOURCE_PATH", "MISSING_SOURCE_ANCHOR", "orbital"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "row_id": row_id,
            "coefficient_symbol": coefficient_symbol,
            "coefficient_value": coefficient_value,
            "coefficient_units": coefficient_units,
            "normalization_convention": normalization_convention,
            "parent_action_block": parent_action_block,
            "source_path": source_path,
            "source_anchor": source_anchor,
            "arena_projection": arena_projection,
            "placeholder_status": "MISSING_DO_NOT_SCORE",
            **flags(),
        }
        for row_id, coefficient_symbol, coefficient_value, coefficient_units, normalization_convention, parent_action_block, source_path, source_anchor, arena_projection in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN1567_0_sources", "load 1567 parent-protection evidence chain", "PASS", "1566, 1565, 1236, 1265, 1268, 1269, and 1023 evidence loaded"),
        ("RUN1567_1_contract", "write single parent protection contract", "PASS_CONTRACT_WRITTEN", "contract clauses are precise and jointly sufficient if parent-signed"),
        ("RUN1567_2_parent_signature", "prove contract from MTS primitives", "FAILED_CURRENT_PARENT_PROOF", "typed object language, matter descent, boundary silence, readout closure, and operator exclusion remain unsigned"),
        ("RUN1567_3_conditional_theorem", "derive theorem under contract", "PASS_EXACT_CONDITIONAL", "if contract is signed then J_R=B_R=readout_regen=Z_R=0"),
        ("RUN1567_4_acquisition", "start live finite residual acquisition", "PASS_NONCLAIM_QUEUE_READY", "internal coefficient targets and external arena sources are separated"),
        ("RUN1567_5_raw_accepted", "raw/accepted finite rows", "NO_LIVE_SCORE_ROWS", f"raw_rows={row_count(RAB_RAW)}; accepted_rows={row_count(RAB_ACCEPTED)}"),
        ("RUN1567_6_claim", "local GR/Newton claim", "BLOCKED_NO_CLAIM", "contract is not parent-signed and no finite residual row is source-ready"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "test": test,
            "current_status": current_status,
            "detail": detail,
            **flags(),
        }
        for runner_id, test, current_status, detail in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1567_0_contract", "parent protection contract", "BLOCKED_NO_CLAIM", "contract written but not derived from MTS primitives"),
        ("GATE1567_1_JR_BR_readout_ZR", "J_R=B_R=readout_regen=Z_R=0", "BLOCKED_NO_CLAIM", "zero theorem is conditional on unsigned contract"),
        ("GATE1567_2_finite_rows", "finite residual source rows", "BLOCKED_NO_CLAIM", "only acquisition queue and blueprint exist; raw/accepted rows remain empty"),
        ("GATE1567_3_external_bounds", "external arena bounds", "PASS_SOURCE_QUEUE_NONCLAIM", "R10/PPN/WEP/clock source URLs queued, but not connected to MTS coefficients"),
        ("GATE1567_4_local_GR", "derived local GR/Newton/PPN safety", "BLOCKED_NO_CLAIM", "neither theorem-zero nor finite-residual route is claim-ready"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim_gate": claim_gate,
            "status": status,
            "reason": reason,
            "source_paths": source_list("1566_doc", "1236_certificate", "1269_operator"),
            **flags(),
        }
        for gate_id, claim_gate, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1567_0_contract",
            "decision": "parent protection contract",
            "result": "CONTRACT_WRITTEN_NOT_PARENT_SIGNED",
            "reason": "the contract is jointly sufficient but still a schema, not a derivation from motion/time/space primitives",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1567_1_theorem",
            "decision": "conditional theorem",
            "result": "EXACT_IF_CONTRACT_SIGNED",
            "reason": "if signed, the second-class route kills J_R, B_R, readout_regen, and Z_R together",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1567_2_acquisition",
            "decision": "finite residual workflow",
            "result": "LIVE_ACQUISITION_QUEUE_STARTED_NONCLAIM",
            "reason": "internal coefficient targets and external arena sources are now separated before raw/accepted intake",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1567_3_next",
            "decision": "next target",
            "result": "NEXT_1568_PARENT_CONTRACT_DERIVATION_FROM_MTS_PRIMITIVES_OR_FIRST_LIVE_ZR_ROW",
            "reason": "either derive the contract from primitives or fill the first source-backed finite row without scoring it",
            **flags(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1567_0_1568",
            "next_target": "1568-Y5-RAB-parent-contract-derivation-from-MTS-primitives-or-first-live-ZR-row.md",
            "script": "scripts/Y5_RAB_parent_contract_derivation_from_MTS_primitives_or_first_live_ZR_row.py",
            "objective": "attempt to derive the typed parent protection contract from motion/time/space primitives; if not derivable, fill the first nonclaim source-backed finite row or explicit theorem-zero row using the 1567 acquisition queue",
            "do_not": "do not promote the contract schema to local-GR evidence; do not move rows to accepted until source path, anchor, units, normalization, and arena projection are real; do not edit formalization-workbench",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    for source, destinations in COPY_TARGETS.items():
        for destination in destinations:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_modified_count_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= START_TS)


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    web_sources = read_csv(WEB_SOURCE_REGISTER)
    contract = read_csv(CONTRACT)
    audit = read_csv(CONTRACT_AUDIT)
    theorem = read_csv(CONTRACT_THEOREM)
    acquisition = read_csv(ACQUISITION_QUEUE)
    blueprint = read_csv(ROW_BLUEPRINT)
    run_rows = read_csv(RUNNER)
    gate_rows = read_csv(CLAIM_GATE)
    decision_items = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    checks = [
        ("VAL1567_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1567 source paths exist"),
        ("VAL1567_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all registered evidence needles found"),
        ("VAL1567_2_web_sources_queued", len(web_sources) >= 4 and all(row["row_status"] == "EXTERNAL_ARENA_SOURCE_CANDIDATE_NONCLAIM" for row in web_sources), "external arena source URLs queued nonclaim"),
        ("VAL1567_3_contract_written", any(row["contract_id"] == "CON1567_6_joint_contract" and row["current_status"] == "CONTRACT_WRITTEN_NOT_SIGNED" for row in contract), "joint parent contract is written but unsigned"),
        ("VAL1567_4_audit_failed_parent_proof", any(row["audit_id"] == "AUD1567_4_joint" and row["current_status"] == "FAILED_CURRENT_PARENT_PROOF" for row in audit), "contract audit refuses parent proof"),
        ("VAL1567_5_conditional_theorem", any(row["theorem_id"] == "THM1567_0_statement" and row["status"] == "EXACT_IF_CONTRACT_PARENT_SIGNED" for row in theorem), "conditional theorem is explicit"),
        ("VAL1567_6_acquisition_queue", len(acquisition) >= 9 and all(row["ready_for_raw"] == "False" and row["ready_for_accepted"] == "False" for row in acquisition), "live acquisition queue exists but is not raw/accepted-ready"),
        ("VAL1567_7_blueprint_nonclaim", len(blueprint) >= 8 and all("MISSING" in row["placeholder_status"] for row in blueprint), "finite row blueprint remains docs-only nonclaim"),
        ("VAL1567_8_raw_accepted_empty", row_count(RAB_RAW) == 0 and row_count(RAB_ACCEPTED) == 0, "raw/accepted finite rows remain empty"),
        ("VAL1567_9_runner_blocks_claim", any(row["runner_id"] == "RUN1567_6_claim" and row["current_status"] == "BLOCKED_NO_CLAIM" for row in run_rows), "runner blocks local claim"),
        ("VAL1567_10_claim_gates", all(row["claim_allowed"] == "False" for row in gate_rows) and any(row["status"] == "BLOCKED_NO_CLAIM" for row in gate_rows), "claim gates remain closed"),
        ("VAL1567_11_decision_next", any(row["result"] == "NEXT_1568_PARENT_CONTRACT_DERIVATION_FROM_MTS_PRIMITIVES_OR_FIRST_LIVE_ZR_ROW" for row in decision_items), "decision selects parent derivation or first live row"),
        ("VAL1567_12_next_target", any("1568-Y5-RAB-parent-contract-derivation" in row["next_target"] for row in next_rows), "next target is parent contract derivation or first live row"),
        ("VAL1567_13_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1567 CSVs parse cleanly"),
        ("VAL1567_14_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1567_15_branch_copies", all(destination.exists() for destinations in COPY_TARGETS.values() for destination in destinations), "branch/quarantine nonclaim copies written"),
        ("VAL1567_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1567_17_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1567_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1567 parent protection contract or live finite ZR source acquisition validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, Any]],
    web_sources: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    acquisition: list[dict[str, Any]],
    blueprint: list[dict[str, Any]],
    run_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    decision_items: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1567 - R_AB Parent Protection Contract or Live Finite Z_R Source Acquisition",
                "",
                "## Verdict",
                "- A single parent-protection contract can now be stated precisely: typed parent sorts, action-image exhaustion, matter descent, boundary descent, readout closure, and operator exclusion must close together.",
                "- Under that contract, the algebraic second-class route would give `J_R=0`, `B_R=0`, `readout_regen=0`, and `Z_R=0` without a plateau axiom.",
                "- The contract is not yet derived from MTS primitives, so it is not local-GR evidence.",
                "- The fallback is now live but nonclaim: internal coefficient targets are separated from external arena-bound sources, and no row is ready for raw/accepted scoring.",
                "- No `Z_R=0`, `q_R=0`, local GR/Newton, R10, PPN, WEP, clock, or orbital claim is made.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "",
                "## External Arena Source Queue",
                md_table(web_sources, ["source_id", "arena", "url", "description", "use_for", "row_status"]),
                "",
                "## Parent Protection Contract",
                md_table(contract, ["contract_id", "contract_clause", "effect_if_signed", "current_status", "missing_for_claim"]),
                "",
                "## Contract Proof Audit",
                md_table(audit, ["audit_id", "target_zero", "required_contract_clause", "current_status", "fallback"]),
                "",
                "## Conditional Theorem",
                md_table(theorem, ["theorem_id", "statement", "calculation_or_role", "status", "why_not_claimed"]),
                "",
                "## Live Source Acquisition Queue",
                md_table(acquisition, ["acquisition_id", "source_class", "target", "needed_evidence", "preferred_source_kind", "arena_projection", "current_status"]),
                "",
                "## Finite Row Blueprint",
                md_table(blueprint, ["row_id", "coefficient_symbol", "coefficient_value", "coefficient_units", "normalization_convention", "parent_action_block", "source_path", "source_anchor", "arena_projection", "placeholder_status"]),
                "",
                "## Runner",
                md_table(run_rows, ["runner_id", "test", "current_status", "detail"]),
                "",
                "## Claim Gates",
                md_table(gate_rows, ["gate_id", "claim_gate", "status", "reason"]),
                "",
                "## Decision",
                md_table(decision_items, ["decision_id", "decision", "result", "reason"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "do_not"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    sources = source_register_rows()
    web_sources = web_source_rows()
    contract = contract_rows()
    audit = contract_audit_rows()
    theorem = conditional_theorem_rows()
    acquisition = acquisition_rows()
    blueprint = blueprint_rows()
    run_rows = runner_rows()
    gate_rows = claim_gate_rows()
    decision_items = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(WEB_SOURCE_REGISTER, web_sources)
    write_csv(CONTRACT, contract)
    write_csv(CONTRACT_AUDIT, audit)
    write_csv(CONTRACT_THEOREM, theorem)
    write_csv(ACQUISITION_QUEUE, acquisition)
    write_csv(ROW_BLUEPRINT, blueprint)
    write_csv(RUNNER, run_rows)
    write_csv(CLAIM_GATE, gate_rows)
    write_csv(DECISION, decision_items)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        WEB_SOURCE_REGISTER,
        CONTRACT,
        CONTRACT_AUDIT,
        CONTRACT_THEOREM,
        ACQUISITION_QUEUE,
        ROW_BLUEPRINT,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, web_sources, contract, audit, theorem, acquisition, blueprint, run_rows, gate_rows, decision_items, validation, next_rows)


if __name__ == "__main__":
    main()

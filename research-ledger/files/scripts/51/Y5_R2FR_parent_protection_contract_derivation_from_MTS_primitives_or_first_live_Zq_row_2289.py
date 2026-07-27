from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

BRANCH_ID = "MTS_R2FR_PARENT_CONTRACT_DERIVATION_OR_FIRST_LIVE_ZQ_ROW_2289"
START_TS = datetime.now(timezone.utc).timestamp()
DOC = ROOT / "2289-Y5-R2FR-parent-protection-contract-derivation-from-MTS-primitives-or-first-live-Zq-row.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2289_00_2288_doc",
        "source_key": "2288_handoff",
        "source_path": ROOT / "2288-Y5-R2FR-RAB-auxiliary-parent-sort-no-derivative-or-finite-Zq-intake.md",
        "needles": ["PARENT_PROTECTION_CONTRACT_IS_THE_HINGE", "FINITE_ZQ_INTAKE_REMAINS_MANDATORY_FALLBACK", "2289-Y5-R2FR"],
        "role": "current hinge selecting primitive contract derivation or first finite row",
    },
    {
        "source_id": "SRC2289_01_2288_validation",
        "source_key": "2288_validation",
        "source_path": OUT / "P8_Y5_BRR545_2288_VALIDATION.csv",
        "needles": ["VAL2288_OVERALL", "PASS"],
        "role": "confirms 2288 passed before 2289",
    },
    {
        "source_id": "SRC2289_02_2288_contract",
        "source_key": "2288_contract_status",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2288_PARENT_CONTRACT_STATUS.csv",
        "needles": ["CON2288_0_parent_sorts", "CON2288_6_joint_contract", "CONTRACT_WRITTEN_NOT_PARENT_SIGNED"],
        "role": "current parent contract clauses to attempt deriving from primitives",
    },
    {
        "source_id": "SRC2289_03_2288_finite",
        "source_key": "2288_finite_intake",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2288_FINITE_ZQ_INTAKE_GATE.csv",
        "needles": ["FIN2288_0_Zq", "FIN2288_4_tau_R10", "MISSING_TAU_R10_PROJECTION"],
        "role": "finite Zq/tau intake gate",
    },
    {
        "source_id": "SRC2289_04_2241_doc",
        "source_key": "2241_primitive_recheck",
        "source_path": ROOT / "2241-Y5-R2FR-RAB-parent-contract-derivation-from-MTS-primitives-or-first-live-ZR-row.md",
        "needles": ["primitive route does not derive the sorted parent contract", "NO_INTERNAL_ROW_READY", "2242-Y5-R2FR"],
        "role": "recent same-fork checkpoint against older RAB naming",
    },
    {
        "source_id": "SRC2289_05_2241_validation",
        "source_key": "2241_validation",
        "source_path": OUT / "P8_Y5_BRR545_2241_VALIDATION.csv",
        "needles": ["VAL2241_OVERALL", "PASS"],
        "role": "confirms 2241 primitive/first-row gate passed as nonclaim",
    },
    {
        "source_id": "SRC2289_06_2241_primitive",
        "source_key": "2241_primitive_derivation_recheck",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2241_PRIMITIVE_DERIVATION_RECHECK.csv",
        "needles": ["PRIM2241_3_parent_contract", "DERIVATION_FAILS_CURRENT_EVIDENCE", "DEMOTE_TO_EXPLICIT_CLOSURE_OR_FINITE_RESIDUAL"],
        "role": "explicit primitive derivation failure",
    },
    {
        "source_id": "SRC2289_07_2241_gap",
        "source_key": "2241_contract_gap",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2241_CONTRACT_TO_PRIMITIVE_GAP.csv",
        "needles": ["GAP2241_0_sorts", "GAP2241_6_joint", "FAILED_CURRENT_PARENT_PROOF"],
        "role": "contract-to-primitive missing clauses",
    },
    {
        "source_id": "SRC2289_08_2241_external",
        "source_key": "2241_external_bound_row",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2241_FIRST_EXTERNAL_BOUND_SOURCE_ROW.csv",
        "needles": ["BOUND2241_R10_EOTWASH_PRL_2021", "external_arena_bound_only", "SOURCE_URL_IDENTIFIED_NEEDS_LOCAL_DIGITIZATION_OR_TABLE"],
        "role": "first external R10 bound source row queued but not MTS coefficient",
    },
    {
        "source_id": "SRC2289_09_2241_internal",
        "source_key": "2241_internal_coeff_status",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2241_FIRST_INTERNAL_COEFFICIENT_ROW_STATUS.csv",
        "needles": ["COEFF2241_0_ZR", "COEFF2241_3_tau_R10", "NO_INTERNAL_ROW_READY"],
        "role": "no internal Z_R/J_R/B_R/tau row ready",
    },
    {
        "source_id": "SRC2289_10_1237_doc",
        "source_key": "1237_primitive_demotion_doc",
        "source_path": ROOT / "1237-Y5-R10-MTS-primitives-to-sorted-parent-action-derivation-or-closure-demotion.md",
        "needles": ["does **not** derive the sorted parent action grammar", "DERIVATION_FAILS_CLOSURE_DEMOTION_REQUIRED", "FAIL_DEMOTE_TO_CLOSURE"],
        "role": "authoritative primitive-route demotion evidence",
    },
    {
        "source_id": "SRC2289_11_1237_chain",
        "source_key": "1237_sorted_chain",
        "source_path": OUT / "P8_Y5_R10_1237_SORTED_GRAMMAR_DERIVATION_CHAIN.csv",
        "needles": ["CHAIN1237_1_Chid_disjoint", "CHAIN1237_6_parent_action", "FAIL_DEMOTE_TO_CLOSURE"],
        "role": "sorted parent grammar chain failure",
    },
    {
        "source_id": "SRC2289_12_1237_local",
        "source_key": "1237_local_gr_status",
        "source_path": OUT / "P8_Y5_R10_1237_LOCAL_GR_CONNECTION_STATUS.csv",
        "needles": ["LGR1237_1_gamma", "CLOSURE_ONLY", "LGR1237_5_verdict"],
        "role": "local GR connection remains closure/partial, not derived",
    },
    {
        "source_id": "SRC2289_13_1237_validation",
        "source_key": "1237_validation",
        "source_path": OUT / "P8_Y5_BRR545_1237_VALIDATION.csv",
        "needles": ["VAL1237_12_overall", "PASS"],
        "role": "confirms 1237 demotion checkpoint passed",
    },
    {
        "source_id": "SRC2289_14_2240_web",
        "source_key": "2240_external_sources",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2240_WEB_SOURCE_REGISTER.csv",
        "needles": ["WEB2240_R10_EOTWASH_PRL_2021", "external alpha(lambda) bound acquisition only", "EXTERNAL_ARENA_SOURCE_CANDIDATE_NONCLAIM"],
        "role": "external arena source queue; not a parent coefficient source",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2289_SOURCE_REGISTER.csv",
    "primitive_recheck": OUT / "P8_Y5_PARENT_QLOC_2289_PRIMITIVE_CONTRACT_DERIVATION_RECHECK.csv",
    "contract_gap": OUT / "P8_Y5_PARENT_QLOC_2289_CONTRACT_TO_PRIMITIVE_GAP.csv",
    "external_bound": OUT / "P8_Y5_PARENT_QLOC_2289_FIRST_EXTERNAL_BOUND_SOURCE_ROW.csv",
    "internal_status": OUT / "P8_Y5_PARENT_QLOC_2289_FIRST_INTERNAL_COEFFICIENT_ROW_STATUS.csv",
    "runner": OUT / "P8_Y5_PARENT_QLOC_2289_RUNNER_NONCLAIM.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2289_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2289_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2289_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2289_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2289_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_internal_status": (OUTPUTS["internal_status"], QUEUE / "JR2289_FIRST_INTERNAL_ZQ_OR_TAUR10_ROW_NONCLAIM.csv"),
    "queue_contract_gap": (OUTPUTS["contract_gap"], QUEUE / "JR2289_CONTRACT_TO_PRIMITIVE_GAP_NONCLAIM.csv"),
    "branch_wep_refusal": (OUTPUTS["runner"], MICROSCOPE / "parent_contract_or_first_Zq_row_refusal_2289.csv"),
    "beta_docs": (OUTPUTS["internal_status"], BETA_DOCS / "FIRST_INTERNAL_ZQ_OR_TAUR10_ROW_2289_NONCLAIM.csv"),
}


def stringify(value: Any) -> str:
    if isinstance(value, bool):
        return "True" if value else "False"
    return str(value)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow({key: stringify(value) for key, value in row.items()})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def validation_pass(path: Path) -> bool:
    if not path.exists() or not csv_parses(path):
        return False
    rows = read_csv(path)
    if not rows:
        return False
    id_key = "check_id" if "check_id" in rows[0] else "validation_id"
    result_key = "result" if "result" in rows[0] else "status"
    overall_rows = [row for row in rows if "overall" in row.get(id_key, "").lower()]
    if overall_rows:
        return all(row.get(result_key, "").upper() == "PASS" for row in overall_rows)
    return all(row.get(result_key, "").upper() == "PASS" for row in rows)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def ignored_environment_path(path: Path) -> bool:
    ignored_parts = {".venv", ".venv-score", "__pycache__", "site-packages", ".git"}
    return any(part in ignored_parts for part in path.parts)


def formalization_has_2289_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    for candidate in FORMALIZATION.rglob("*2289*"):
        if candidate.is_file() and not ignored_environment_path(candidate.relative_to(FORMALIZATION)):
            return True
    return False


def formalization_touched_since_start() -> bool:
    if not FORMALIZATION.exists():
        return False
    for candidate in FORMALIZATION.rglob("*"):
        if candidate.is_file() and not ignored_environment_path(candidate.relative_to(FORMALIZATION)):
            if candidate.stat().st_mtime >= START_TS:
                return True
    return False


def table(headers: list[str], rows: list[dict[str, Any]]) -> str:
    def cell(value: Any) -> str:
        return stringify(value).replace("\n", " ").replace("|", "\\|")

    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        source_path = Path(source["source_path"])
        source_text = read_text(source_path)
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": source_path,
                "exists": source_path.exists(),
                "needles": "; ".join(needles),
                "needles_present": all(needle in source_text for needle in needles),
                "role": source["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def primitive_recheck_rows() -> list[dict[str, Any]]:
    return [
        {
            "recheck_id": "PRIM2289_0_motion_load",
            "primitive_route": "motion/load/local observer scaffold",
            "what_it_supplies": "partial Q_obs and Newtonian leading-lane support",
            "attempt_to_derive_contract": "try to derive typed sorts, action-image exhaustion, matter descent, boundary silence, readout closure, and operator exclusion",
            "result": "DOES_NOT_DERIVE_CONTRACT",
            "reason": "observer/load scaffold does not supply total parent action or sorted grammar",
            "valid_for_claim": False,
        },
        {
            "recheck_id": "PRIM2289_1_reciprocity",
            "primitive_route": "R_AB=0 / local reciprocity",
            "what_it_supplies": "useful closure benchmark for gamma-like local routing",
            "attempt_to_derive_contract": "try to turn reciprocity into parent-owned q-sector elimination",
            "result": "CLOSURE_ONLY_CURRENT_STATE",
            "reason": "1237 demotes local reciprocity to explicit closure; no zero reciprocal charge theorem",
            "valid_for_claim": False,
        },
        {
            "recheck_id": "PRIM2289_2_sorted_grammar",
            "primitive_route": "typed parent object language",
            "what_it_supplies": "exact rule that would protect hidden-visible coefficients and q-sector leakage",
            "attempt_to_derive_contract": "derive sorted ParentGenerate grammar from deeper MTS primitives",
            "result": "SCHEMA_VALID_NOT_PRIMITIVE_DERIVED",
            "reason": "1237 chain fails hidden disjointness, visible coefficient domain, readout closure, source forgetting, and total parent action",
            "valid_for_claim": False,
        },
        {
            "recheck_id": "PRIM2289_3_parent_contract",
            "primitive_route": "CON2288/2240 parent protection contract",
            "what_it_supplies": "jointly sufficient local q-sector protection if parent-signed",
            "attempt_to_derive_contract": "bind parent sorts, action image, matter, boundary, readout, and operator clauses into one primitive theorem",
            "result": "DERIVATION_FAILS_CURRENT_EVIDENCE",
            "reason": "current evidence reuses 1237/2241 failure: the contract is a clean target theorem or closure benchmark, not derived evidence",
            "valid_for_claim": False,
        },
        {
            "recheck_id": "PRIM2289_4_verdict",
            "primitive_route": "motion/time/space primitives to parent protection contract",
            "what_it_supplies": "would be the serious local-GR derivation route",
            "attempt_to_derive_contract": "derive exact second-class protection without importing GR or post-hoc closure",
            "result": "DEMOTE_TO_EXPLICIT_CLOSURE_OR_FINITE_RESIDUAL",
            "reason": "no inspected route derives the full contract from primitives",
            "valid_for_claim": False,
        },
    ]


def contract_gap_rows() -> list[dict[str, Any]]:
    entries = [
        ("GAP2289_0_sorts", "typed parent sorts", "CON2288_0_parent_sorts", "CHAIN1237_1/2 fail hidden disjointness and parent-generated visible coefficient domain", "MISSING_PRIMITIVE_SORT_DERIVATION"),
        ("GAP2289_1_action_image", "ParentGenerate image exhaustion", "CON2288_1_action_image", "CHAIN1237_6 total parent action fails", "MISSING_TOTAL_PARENT_ACTION"),
        ("GAP2289_2_matter", "J_q/J_R=0 matter descent", "CON2288_2_matter_descent", "CHAIN1237_5 source-label forgetting fails", "MISSING_MATTER_CATEGORY_DERIVATION"),
        ("GAP2289_3_boundary", "B_R/Pi_q/Q_R=0 boundary descent", "CON2288_3_boundary_descent", "1237 does not derive boundary/corner silence", "MISSING_BOUNDARY_GRAMMAR"),
        ("GAP2289_4_readout", "readout/radiative closure", "CON2288_4_readout_closure", "CHAIN1237_4 readout/radiative closure fails", "MISSING_READOUT_CLOSURE"),
        ("GAP2289_5_operator", "Z_q derivative operator exclusion", "CON2288_5_operator_exclusion", "CHAIN1237_2/6 and 1269 keep operator exclusion conditional", "MISSING_OPERATOR_EXHAUSTION"),
        ("GAP2289_6_joint", "second-class local protection package", "CON2288_6_joint_contract", "any missing gap leaves finite q residual route live", "FAILED_CURRENT_PARENT_PROOF"),
    ]
    return [
        {
            "gap_id": gap_id,
            "needed_contract_piece": needed,
            "contract_clause": clause,
            "current_evidence": evidence,
            "status": status,
            "valid_for_claim": False,
        }
        for gap_id, needed, clause, evidence, status in entries
    ]


def external_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "BOUND2289_R10_EOTWASH_PRL_2021",
            "row_type": "external_arena_bound_only",
            "arena": "R10",
            "quantity": "alpha(lambda) Yukawa bound",
            "source_url": "https://link.aps.org/doi/10.1103/PhysRevLett.126.211101",
            "source_title": "Combined Test of the Gravitational Inverse-Square Law at the Centimeter Scale",
            "extraction_status": "SOURCE_URL_IDENTIFIED_NEEDS_LOCAL_DIGITIZATION_OR_TABLE",
            "why_not_scoreable": "external bound is not an MTS Z_q/M_q^2/j_q/B_R/tau coefficient and no MTS projection kernel is supplied",
            "source_backed": False,
            "score_ready": False,
            "valid_for_claim": False,
        }
    ]


def internal_status_rows() -> list[dict[str, Any]]:
    entries = [
        ("COEFF2289_0_Zq", "Z_q", "no theorem-zero and no numeric parent gradient coefficient", "MISSING_INTERNAL_COEFFICIENT", "derive no-derivative theorem or source finite gradient coefficient"),
        ("COEFF2289_1_Mq2", "M_q^2", "no parent Hessian/mass gap in same q normalization", "MISSING_INTERNAL_COEFFICIENT", "source local q-sector Hessian or mass-gap scale"),
        ("COEFF2289_2_jq", "j_q/J_q", "matter descent not derived and no finite source-current row", "MISSING_INTERNAL_COEFFICIENT", "prove source zero or source finite coupling"),
        ("COEFF2289_3_boundary", "B_R/Pi_q/Q_R", "boundary silence not derived and no finite boundary row", "MISSING_INTERNAL_COEFFICIENT", "prove boundary no-hair or source boundary momentum"),
        ("COEFF2289_4_tau_R10", "tau_R10", "external R10 bound source exists, but no MTS residual-to-alpha projection kernel", "MISSING_PROJECTION_KERNEL", "derive tau_R10 mapping finite q profile to alpha(lambda) convention"),
        ("COEFF2289_5_verdict", "first live MTS finite row", "not filled; only first external bound-source row is queued", "NO_INTERNAL_ROW_READY", "next target must try Z_q theorem/finite coefficient or tau_R10 kernel"),
    ]
    return [
        {
            "status_id": status_id,
            "target": target,
            "current_evidence": evidence,
            "status": status,
            "next_input_needed": next_input,
            "numeric_value_present": False,
            "source_backed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
        }
        for status_id, target, evidence, status, next_input in entries
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        {"runner_id": "RUN2289_0_sources", "test": "load 2288/2241/1237 evidence chain", "current_status": "PASS", "detail": "all registered sources loaded with needles present", "score_ready": False, "valid_for_claim": False},
        {"runner_id": "RUN2289_1_primitive_contract", "test": "derive parent protection contract from primitives", "current_status": "FAILED_CURRENT_PARENT_PROOF", "detail": "1237/2241 already demote sorted grammar to closure under current evidence", "score_ready": False, "valid_for_claim": False},
        {"runner_id": "RUN2289_2_first_bound", "test": "queue first external R10 bound source row", "current_status": "PASS_NONCLAIM_SOURCE_URL_ROW", "detail": "R10 PRL source URL queued but not digitized/localized and not an MTS coefficient", "score_ready": False, "valid_for_claim": False},
        {"runner_id": "RUN2289_3_first_internal_coeff", "test": "fill first internal MTS finite row", "current_status": "NO_INTERNAL_ROW_READY", "detail": "Z_q/M_q^2/j_q/B_R/tau_R10 remain missing", "score_ready": False, "valid_for_claim": False},
        {"runner_id": "RUN2289_4_claim", "test": "local GR/Newton claim", "current_status": "BLOCKED_NO_CLAIM", "detail": "contract derivation failed and first bound row is external-only", "score_ready": False, "valid_for_claim": False},
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {"claim_id": "GATE2289_0_primitive_contract", "claim_gate": "contract derived from MTS primitives", "status": "BLOCKED_NO_CLAIM", "reason": "1237/2241 current-state evidence says derivation fails and demotes to closure", "valid_for_claim": False, "claim_allowed": False},
        {"claim_id": "GATE2289_1_theorem_zero", "claim_gate": "J_q/B_R/readout_regen/Z_q zero theorem", "status": "BLOCKED_NO_CLAIM", "reason": "zero theorem depends on unsigned parent protection contract", "valid_for_claim": False, "claim_allowed": False},
        {"claim_id": "GATE2289_2_external_bound", "claim_gate": "external R10 bound row", "status": "PASS_SOURCE_QUEUE_NONCLAIM", "reason": "source URL queued but not connected to MTS coefficient", "valid_for_claim": False, "claim_allowed": False},
        {"claim_id": "GATE2289_3_first_coeff", "claim_gate": "first internal finite residual coefficient/projection row", "status": "BLOCKED_NO_CLAIM", "reason": "no internal source-backed coefficient/projection row exists", "valid_for_claim": False, "claim_allowed": False},
        {"claim_id": "GATE2289_4_local_GR", "claim_gate": "derived local GR/Newton/PPN safety", "status": "BLOCKED_NO_CLAIM", "reason": "neither theorem-zero nor finite residual scoring is ready", "valid_for_claim": False, "claim_allowed": False},
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2289_0_derivation",
            "decision": "derive contract from primitives",
            "result": "FAILED_CURRENT_EVIDENCE_REUSE_1237_2241",
            "reason": "the primitive/sorted-grammar route has already been audited and demoted to explicit closure",
            "next_action": "do not spend local-GR theorem credit from the parent protection contract",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2289_1_bound",
            "decision": "first external bound source row",
            "result": "FIRST_EXTERNAL_BOUND_ROW_QUEUED_NONCLAIM",
            "reason": "R10 bound source URL exists but is not digitized and not an MTS coefficient/projection",
            "next_action": "keep as external comparator only",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2289_2_coeff",
            "decision": "first internal coefficient/projection row",
            "result": "NOT_READY",
            "reason": "Z_q/M_q^2/j_q/B_R/tau_R10 need parent theorem-zero, source-backed coefficients, or a real projection kernel",
            "next_action": "target Z_q theorem/finite coefficient or tau_R10 projection kernel next",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2289_3_next",
            "decision": "next target",
            "result": "NEXT_2290_FIRST_INTERNAL_ZQ_OR_TAUR10_PROJECTION_ROW",
            "reason": "the next executable move is narrower: either internal Z_q theorem/value or tau_R10 projection to the R10 comparator",
            "next_action": "2290-Y5-R2FR-first-internal-Zq-or-tauR10-projection-row.md",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2289_0_primary",
            "next_target": "2290-Y5-R2FR-first-internal-Zq-or-tauR10-projection-row.md",
            "script": "scripts/Y5_R2FR_first_internal_Zq_or_tauR10_projection_row_2290.py",
            "objective": "try to fill the first internal nonclaim row: either theorem-zero/numeric Z_q from parent grammar, or a tau_R10 projection kernel connecting finite q/R_AB residuals to the external R10 alpha(lambda) bound row",
            "do_not": "do not treat external bounds as MTS coefficients; do not move rows to accepted until local source path, source anchor, units, normalization, and projection are real; do not edit formalization-workbench",
            "valid_for_claim": False,
        }
    ]


def generated_claim_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    guarded_keys = {
        "numeric_value_present",
        "source_backed",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
    }
    for path in paths:
        for row in read_csv(path):
            for key, value in row.items():
                if key in guarded_keys and value.strip().lower() not in false_values:
                    return False
    return True


def copy_branch_files() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for copy_id, (source_path, target_path) in COPY_TARGETS.items():
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)
        rows.append(
            {
                "copy_id": copy_id,
                "source_path": source_path,
                "target_path": target_path,
                "target_exists": target_path.exists(),
                "target_parses": csv_parses(target_path),
                "reason": "branch copy for 2289 primitive-contract or first-live-Zq-row checkpoint",
            }
        )
    return rows


def validation_rows(all_generated_before_validation: list[Path], branch_copy_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_rows = read_csv(OUTPUTS["source_register"])
    primitive_rows = read_csv(OUTPUTS["primitive_recheck"])
    gap_rows = read_csv(OUTPUTS["contract_gap"])
    external_rows = read_csv(OUTPUTS["external_bound"])
    internal_rows = read_csv(OUTPUTS["internal_status"])
    runner_rows_local = read_csv(OUTPUTS["runner"])
    claim_rows = read_csv(OUTPUTS["claim_gates"])
    decision_rows_local = read_csv(OUTPUTS["decision"])
    next_rows = read_csv(OUTPUTS["next_target"])

    checks = [
        ("VAL2289_0_sources_exist", all(row["exists"] == "True" for row in source_rows), "all cited source paths exist"),
        ("VAL2289_1_needles_present", all(row["needles_present"] == "True" for row in source_rows), "all cited source needles are present"),
        (
            "VAL2289_2_prior_validations",
            validation_pass(OUT / "P8_Y5_BRR545_2288_VALIDATION.csv")
            and validation_pass(OUT / "P8_Y5_BRR545_2241_VALIDATION.csv")
            and validation_pass(OUT / "P8_Y5_BRR545_1237_VALIDATION.csv"),
            "2288, 2241, and 1237 validation files pass overall",
        ),
        (
            "VAL2289_3_primitive_derivation_fails",
            any(row["result"] == "DERIVATION_FAILS_CURRENT_EVIDENCE" for row in primitive_rows)
            and any(row["result"] == "DEMOTE_TO_EXPLICIT_CLOSURE_OR_FINITE_RESIDUAL" for row in primitive_rows),
            "primitive contract derivation is refused and demoted to closure/finite residual",
        ),
        (
            "VAL2289_4_contract_gaps_complete",
            {"MISSING_PRIMITIVE_SORT_DERIVATION", "MISSING_TOTAL_PARENT_ACTION", "MISSING_MATTER_CATEGORY_DERIVATION", "MISSING_BOUNDARY_GRAMMAR", "MISSING_READOUT_CLOSURE", "MISSING_OPERATOR_EXHAUSTION", "FAILED_CURRENT_PARENT_PROOF"}.issubset(
                {row["status"] for row in gap_rows}
            ),
            "contract-to-primitive gaps are complete",
        ),
        (
            "VAL2289_5_external_bound_nonclaim",
            any(row["row_type"] == "external_arena_bound_only" and row["score_ready"] == "False" for row in external_rows),
            "external R10 bound is queued as nonclaim comparator only",
        ),
        (
            "VAL2289_6_no_internal_row_ready",
            any(row["status"] == "NO_INTERNAL_ROW_READY" for row in internal_rows)
            and all(row["score_ready"] == "False" and row["valid_prediction_row"] == "False" for row in internal_rows),
            "no internal coefficient/projection row is ready",
        ),
        (
            "VAL2289_7_runner_blocks_claim",
            any(row["current_status"] == "FAILED_CURRENT_PARENT_PROOF" for row in runner_rows_local)
            and any(row["current_status"] == "BLOCKED_NO_CLAIM" for row in runner_rows_local),
            "runner blocks parent proof and local claim",
        ),
        (
            "VAL2289_8_claim_gates",
            any(row["claim_gate"] == "derived local GR/Newton/PPN safety" and row["status"] == "BLOCKED_NO_CLAIM" for row in claim_rows)
            and all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in claim_rows),
            "claim gates remain closed except nonclaim source queue",
        ),
        (
            "VAL2289_9_decision_next",
            any(row["result"] == "NEXT_2290_FIRST_INTERNAL_ZQ_OR_TAUR10_PROJECTION_ROW" for row in decision_rows_local)
            and any(row["next_target"] == "2290-Y5-R2FR-first-internal-Zq-or-tauR10-projection-row.md" for row in next_rows),
            "decision selects first internal Zq or tau_R10 projection row",
        ),
        ("VAL2289_10_csv_parse", all(csv_parses(path) for path in all_generated_before_validation), "all generated 2289 CSVs parse before validation file"),
        ("VAL2289_11_no_claim_flags", generated_claim_flags_false(all_generated_before_validation), "all generated prediction/claim flags remain false"),
        ("VAL2289_12_branch_copies", all(row["target_exists"] and row["target_parses"] for row in branch_copy_rows), "branch/queue copies exist and parse"),
        ("VAL2289_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL2289_14_formalization_no_2289", not formalization_has_2289_artifacts(), "formalization-workbench has no non-venv 2289 artifacts"),
        ("VAL2289_15_formalization_untouched", not formalization_touched_since_start(), "formalization-workbench untouched during 2289 run"),
    ]
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]
    overall_pass = all(row["result"] == "PASS" for row in rows)
    rows.append(
        {
            "check_id": "VAL2289_OVERALL",
            "result": "PASS" if overall_pass else "FAIL",
            "detail": "2289 refuses primitive contract derivation from current evidence, queues external R10 bound as nonclaim comparator, finds no internal coefficient row, and selects first internal Zq/tau_R10 projection next",
        }
    )
    return rows


def write_markdown(
    sources: list[dict[str, Any]],
    primitive_recheck: list[dict[str, Any]],
    contract_gap: list[dict[str, Any]],
    external_bound: list[dict[str, Any]],
    internal_status: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    claim_gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    branch_copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    content = f"""# 2289 - Y5/R2FR Parent Protection Contract Derivation from MTS Primitives or First Live Zq Row

## Verdict

2289 tries the honest leap and rejects it under current evidence: the parent protection contract is not yet derived from motion/time/space primitives.

That is not a collapse. It means the contract is a clean target theorem or closure benchmark, not something we can spend as local-GR evidence. The current primitive route inherits the 1237 failure: sorted grammar, matter descent, boundary silence, readout closure, operator exclusion, and one total parent action are not yet primitive-derived.

The first external R10 bound source remains queued as a comparator, but it is not an MTS coefficient. There is still no internal live `Z_q`, `M_q^2`, `j_q`, `B_R`, or `tau_R10` row. So the next real move is narrower: produce a genuine internal `Z_q` theorem/value, or define a `tau_R10` projection kernel that connects finite q/R_AB residuals to the external alpha(lambda) convention.

## Source Register
{table(["source_id", "source_key", "source_path", "exists", "needles_present", "role", "valid_for_claim"], sources)}

## Primitive Contract Derivation Recheck
{table(["recheck_id", "primitive_route", "what_it_supplies", "attempt_to_derive_contract", "result", "reason", "valid_for_claim"], primitive_recheck)}

## Contract To Primitive Gap
{table(["gap_id", "needed_contract_piece", "contract_clause", "current_evidence", "status", "valid_for_claim"], contract_gap)}

## First External Bound Source Row
{table(["row_id", "row_type", "arena", "quantity", "source_url", "source_title", "extraction_status", "why_not_scoreable", "source_backed", "score_ready", "valid_for_claim"], external_bound)}

## First Internal Coefficient Row Status
{table(["status_id", "target", "current_evidence", "status", "next_input_needed", "numeric_value_present", "source_backed", "score_ready", "valid_prediction_row", "valid_for_claim"], internal_status)}

## Runner
{table(["runner_id", "test", "current_status", "detail", "score_ready", "valid_for_claim"], runner)}

## Claim Gates
{table(["claim_id", "claim_gate", "status", "reason", "valid_for_claim", "claim_allowed"], claim_gates)}

## Decision Ledger
{table(["decision_id", "decision", "result", "reason", "next_action", "valid_for_claim"], decisions)}

## Next Target
{table(["next_id", "next_target", "script", "objective", "do_not", "valid_for_claim"], next_target)}

## Branch Copies
{table(["copy_id", "source_path", "target_path", "target_exists", "target_parses", "reason"], branch_copies)}

## Validation
{table(["check_id", "result", "detail"], validation)}

## Working Interpretation

This is the theory discipline doing its job. We tried the elegant route; current evidence says no. So we do not fake it. The project now needs either one real internal theorem/coefficient for `Z_q`, or a real projection kernel `tau_R10`. That is actually a cleaner battlefield than before: one internal row can start turning the local branch from philosophy back into testable physics.
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    remove_pycache()
    sources = source_register_rows()
    primitive_recheck = primitive_recheck_rows()
    contract_gap = contract_gap_rows()
    external_bound = external_bound_rows()
    internal_status = internal_status_rows()
    runner = runner_rows()
    claim_gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["primitive_recheck"], primitive_recheck)
    write_csv(OUTPUTS["contract_gap"], contract_gap)
    write_csv(OUTPUTS["external_bound"], external_bound)
    write_csv(OUTPUTS["internal_status"], internal_status)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["claim_gates"], claim_gates)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next_target"], next_target)

    branch_copies = copy_branch_files()
    write_csv(OUTPUTS["branch_copies"], branch_copies)

    generated_before_validation = [
        OUTPUTS["source_register"],
        OUTPUTS["primitive_recheck"],
        OUTPUTS["contract_gap"],
        OUTPUTS["external_bound"],
        OUTPUTS["internal_status"],
        OUTPUTS["runner"],
        OUTPUTS["claim_gates"],
        OUTPUTS["decision"],
        OUTPUTS["next_target"],
        OUTPUTS["branch_copies"],
    ]
    remove_pycache()
    validation = validation_rows(generated_before_validation, branch_copies)
    write_csv(OUTPUTS["validation"], validation)
    write_markdown(
        sources,
        primitive_recheck,
        contract_gap,
        external_bound,
        internal_status,
        runner,
        claim_gates,
        decisions,
        next_target,
        branch_copies,
        validation,
    )
    remove_pycache()

    failed = [row for row in validation if row["result"] != "PASS"]
    if failed:
        failed_ids = ", ".join(row["check_id"] for row in failed)
        raise SystemExit(f"2289 validation failed: {failed_ids}")
    print(f"Wrote {DOC}")
    print(f"Wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

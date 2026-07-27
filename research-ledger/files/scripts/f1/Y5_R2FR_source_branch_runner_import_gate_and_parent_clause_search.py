from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1682"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1682-Y5-R2FR-source-branch-runner-import-gate-and-parent-clause-search.md"
GATE_MODULE = ROOT / "scripts" / "Rsource_runner_gate_1682.py"

SOURCE_FILES = {
    "1681_doc": ROOT / "1681-Y5-R2FR-finite-Rsource-contract-validator-or-parent-action-owner-clause.md",
    "1681_validation": OUT / "P8_Y5_BRR545_1681_VALIDATION.csv",
    "1681_result_matrix": OUT / "P8_Y5_PARENT_QLOC_1681_VALIDATOR_RESULT_MATRIX.csv",
    "1681_arena_matrix": OUT / "P8_Y5_PARENT_QLOC_1681_ARENA_USE_REFUSAL_MATRIX.csv",
    "1681_owner_audit": OUT / "P8_Y5_PARENT_QLOC_1681_PARENT_ACTION_OWNER_CLAUSE_AUDIT.csv",
    "1681_next": OUT / "P8_Y5_PARENT_QLOC_1681_NEXT_TARGET.csv",
    "1680_clauses": OUT / "P8_Y5_PARENT_QLOC_1680_SOURCE_CURRENT_OWNER_ZERO_THEOREM_CLAUSES.csv",
    "1680_contract": OUT / "P8_Y5_PARENT_QLOC_1680_FINITE_RSOURCE_COEFFICIENT_CONTRACT_NONCLAIM.csv",
    "1680_countermodels": OUT / "P8_Y5_PARENT_QLOC_1680_COUNTERMODEL_MERGE_LEDGER.csv",
    "1338_theorem_attempt": OUT / "P8_Y5_R10_1338_OBJECT_LANGUAGE_THEOREM_ATTEMPT.csv",
    "1416_ban_attempt": OUT / "P8_Y5_R10_1416_SOURCE_SLOT_CURRENT_RESCALING_BAN_ATTEMPT.csv",
}

NEEDLES = {
    "1681_doc": ["no parent-action owner clause", "future tests now need real theorem-zero clauses"],
    "1681_validation": ["VAL1681_OVERALL", "PASS"],
    "1681_result_matrix": ["RFC1680_0", "REJECT_MISSING_ZERO_OR_VALUE_SOURCE_PATH_PARENT_BASIS_OR_ARENA_PROJECTION"],
    "1681_arena_matrix": ["AR1681_0_WEP", "REJECT_ARENA_USE", "AR1681_3_R11"],
    "1681_owner_audit": ["OCA1681_4_current_owner", "MISSING_CURRENT_OWNER"],
    "1681_next": ["1682-Y5-R2FR-source-branch-runner-import-gate-and-parent-clause-search.md"],
    "1680_clauses": ["CL1680_3", "NoSourceOnlySpeciesSlot", "CL1680_7", "radiative_readout_stability"],
    "1680_contract": ["RFC1680_5", "MISSING_BETA_SOURCE_ALPHA_OWNER_OR_COEFFICIENT"],
    "1680_countermodels": ["CM1680_2", "current_rescaling"],
    "1338_theorem_attempt": ["OLT1338_6_verdict", "NOT_DERIVED_CURRENT_CORPUS"],
    "1416_ban_attempt": ["BAN1416_6_verdict", "BAN_NOT_PROVED_FIRST_RSOURCE_ROW_REQUIRED"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1682_SOURCE_REGISTER.csv"
GATE_SPEC = OUT / "P8_Y5_PARENT_QLOC_1682_RUNNER_IMPORT_GATE_SPEC.csv"
GATE_DRY_RUN = OUT / "P8_Y5_PARENT_QLOC_1682_RUNNER_IMPORT_GATE_DRY_RUN.csv"
PARENT_SEARCH = OUT / "P8_Y5_PARENT_QLOC_1682_PARENT_CLAUSE_SEARCH_LEDGER.csv"
DOWNSTREAM_ADOPTION = OUT / "P8_Y5_PARENT_QLOC_1682_DOWNSTREAM_RUNNER_ADOPTION_MATRIX.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1682_DECISION.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1682_CLAIM_GATE.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1682_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1682_VALIDATION.csv"

GENERATED_CSV = [
    SOURCE_REGISTER,
    GATE_SPEC,
    GATE_DRY_RUN,
    PARENT_SEARCH,
    DOWNSTREAM_ADOPTION,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    GATE_SPEC,
    GATE_DRY_RUN,
    PARENT_SEARCH,
    DOWNSTREAM_ADOPTION,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

COPY_TARGETS = {
    GATE_SPEC: [
        QUARANTINE / "RUNNER_IMPORT_GATE_SPEC.csv",
        BRANCH_RESIDUALS / "R2FR_runner_import_gate_spec_1682.csv",
        QUEUE / "JR1682_RUNNER_IMPORT_GATE_SPEC.csv",
    ],
    GATE_DRY_RUN: [
        QUARANTINE / "RUNNER_IMPORT_GATE_DRY_RUN.csv",
        BRANCH_RESIDUALS / "R2FR_runner_import_gate_dry_run_1682.csv",
        QUEUE / "JR1682_RUNNER_IMPORT_GATE_DRY_RUN.csv",
    ],
    PARENT_SEARCH: [
        QUARANTINE / "PARENT_CLAUSE_SEARCH_LEDGER.csv",
        BRANCH_RESIDUALS / "R2FR_parent_clause_search_ledger_1682.csv",
        QUEUE / "JR1682_PARENT_CLAUSE_SEARCH_LEDGER.csv",
    ],
    DOWNSTREAM_ADOPTION: [
        QUARANTINE / "DOWNSTREAM_RUNNER_ADOPTION_MATRIX.csv",
        BRANCH_RESIDUALS / "R2FR_downstream_runner_adoption_matrix_1682.csv",
        QUEUE / "JR1682_DOWNSTREAM_RUNNER_ADOPTION_MATRIX.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_nonclaim_1682.csv",
        QUEUE / "JR1682_NEXT_TARGET_NONCLAIM.csv",
    ],
}

EXPECTED_ARENAS = {"WEP", "R10", "NEWTON_GM", "R11"}
EXPECTED_PARENT_CLAUSES = {
    "NoSourceOnlySpeciesSlot",
    "single_source_current_owner",
    "no_marker_readout_extension",
    "radiative_readout_stability",
}
SCORE_FLAGS = ["gate_pass", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed", "parent_clause_signed"]


def ensure_dirs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def bool_cell(value: object) -> bool:
    return str(value).strip().lower() == "true"


def blocked_marker(value: object) -> bool:
    text = str(value)
    markers = ["MISSING_", "NOT_", "BLOCKED", "REJECT", "FAIL", "DRY_RUN", "CONDITIONAL", "LIVE_COUNTER", "UNSIGNED", "NO_PASS"]
    return any(marker in text for marker in markers)


def source_register_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_key, source_path in SOURCE_FILES.items():
        exists = source_path.exists()
        body = read_text(source_path) if exists else ""
        needles_present = all(needle in body for needle in NEEDLES[source_key])
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_key": source_key,
                "source_path": str(source_path),
                "exists": exists,
                "needles_present": needles_present,
                "required_needles": "; ".join(NEEDLES[source_key]),
                "use_in_1682": "source-branch runner import gate and parent-clause search",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def gate_module_text() -> str:
    return '''from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
VALIDATION = OUT / "P8_Y5_BRR545_1681_VALIDATION.csv"
RESULT_MATRIX = OUT / "P8_Y5_PARENT_QLOC_1681_VALIDATOR_RESULT_MATRIX.csv"
ARENA_MATRIX = OUT / "P8_Y5_PARENT_QLOC_1681_ARENA_USE_REFUSAL_MATRIX.csv"
ALLOWED_ARENAS = {"WEP", "R10", "NEWTON_GM", "R11"}


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _truth(value: object) -> bool:
    return str(value).strip().lower() == "true"


def evaluate_source_branch_gate(arena: str | None = None, root: str | Path | None = None) -> dict[str, object]:
    base = Path(root) if root is not None else ROOT
    out = base / "source-intake" / "mts_residuals"
    validation_path = out / VALIDATION.name
    result_path = out / RESULT_MATRIX.name
    arena_path = out / ARENA_MATRIX.name
    missing_files = [str(path) for path in [validation_path, result_path, arena_path] if not path.exists()]
    if missing_files:
        return {
            "gate_pass": False,
            "arena": arena,
            "reason": "MISSING_GATE_FILES",
            "missing_files": missing_files,
            "valid_for_claim": False,
            "claim_allowed": False,
        }

    validation_rows = _read_csv(validation_path)
    result_rows = _read_csv(result_path)
    arena_rows = _read_csv(arena_path)
    overall_pass = any(row.get("check_id") == "VAL1681_OVERALL" and row.get("result") == "PASS" for row in validation_rows)
    component_pass = all(_truth(row.get("validator_pass", "False")) for row in result_rows)
    arena_rejections = {row.get("arena"): row for row in arena_rows if row.get("validator_result", "").startswith("REJECT")}
    arena_key = arena.upper() if isinstance(arena, str) else None
    if arena_key and arena_key not in ALLOWED_ARENAS:
        return {
            "gate_pass": False,
            "arena": arena,
            "reason": "UNKNOWN_SOURCE_ARENA",
            "known_arenas": sorted(ALLOWED_ARENAS),
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    arena_pass = arena_key is None and not arena_rejections
    if arena_key is not None:
        arena_pass = arena_key not in arena_rejections
    gate_pass = overall_pass and component_pass and arena_pass
    return {
        "gate_pass": gate_pass,
        "arena": arena_key,
        "reason": "PASS" if gate_pass else "SOURCE_BRANCH_GATE_REJECTED",
        "overall_1681_validation_pass": overall_pass,
        "component_rows_pass": component_pass,
        "arena_pass": arena_pass,
        "rejected_arenas": sorted(arena_rejections),
        "component_failures": [row.get("basis_component") for row in result_rows if not _truth(row.get("validator_pass", "False"))],
        "valid_for_claim": gate_pass,
        "claim_allowed": gate_pass,
    }


def require_source_branch_gate(arena: str | None = None, root: str | Path | None = None) -> dict[str, object]:
    result = evaluate_source_branch_gate(arena=arena, root=root)
    if not result["gate_pass"]:
        raise RuntimeError(f"source branch gate rejected: {result}")
    return result
'''


def write_gate_module() -> None:
    GATE_MODULE.write_text(gate_module_text(), encoding="utf-8")


def gate_spec_rows() -> list[dict[str, object]]:
    rows = [
        ("GATE1682_0_module", "Rsource_runner_gate_1682.py", "downstream runners import evaluate_source_branch_gate or require_source_branch_gate", "module written in scripts", "False"),
        ("GATE1682_1_inputs", "1681 validation/result/arena matrices", "gate reads current 1681 validator outputs before scoring", "source-backed local files required", "False"),
        ("GATE1682_2_component_rule", "all finite R_source rows must pass", "component_rows_pass requires validator_pass=true for every 1681 result row", "currently rejected", "False"),
        ("GATE1682_3_arena_rule", "arena-specific rejection", "WEP/R10/NEWTON_GM/R11 are refused if present in 1681 arena refusal matrix", "currently all rejected", "False"),
        ("GATE1682_4_fail_closed", "fail closed", "missing gate files, unknown arena, rejected components, or rejected arena return/raise failure", "active", "False"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "gate_object": gate_object,
            "enforcement_rule": enforcement_rule,
            "current_status": current_status,
            "gate_pass": gate_pass,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate_object, enforcement_rule, current_status, gate_pass in rows
    ]


def gate_dry_run_rows() -> list[dict[str, object]]:
    rows = []
    rejected_components = ";".join(row["basis_component"] for row in read_csv(SOURCE_FILES["1681_result_matrix"]) if row["validator_pass"].lower() != "true")
    for arena in ["WEP", "R10", "NEWTON_GM", "R11", "ALL"]:
        arena_value = None if arena == "ALL" else arena
        result = evaluate_gate_like_module(arena_value)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "dry_run_id": f"DRY1682_{arena}",
                "arena": arena,
                "gate_pass": result["gate_pass"],
                "reason": result["reason"],
                "rejected_arenas": ";".join(result["rejected_arenas"]),
                "component_failures": rejected_components,
                "expected_behavior": "REJECT_CURRENT_SOURCE_BRANCH",
                "accepted_for_scoring": False,
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def evaluate_gate_like_module(arena: str | None) -> dict[str, object]:
    result_rows = read_csv(SOURCE_FILES["1681_result_matrix"])
    arena_rows = read_csv(SOURCE_FILES["1681_arena_matrix"])
    validation_rows = read_csv(SOURCE_FILES["1681_validation"])
    overall_pass = any(row.get("check_id") == "VAL1681_OVERALL" and row.get("result") == "PASS" for row in validation_rows)
    component_pass = all(row.get("validator_pass", "False").lower() == "true" for row in result_rows)
    arena_rejections = {row["arena"]: row for row in arena_rows if row["validator_result"].startswith("REJECT")}
    arena_key = arena.upper() if isinstance(arena, str) else None
    arena_pass = arena_key is None and not arena_rejections
    if arena_key is not None:
        arena_pass = arena_key not in arena_rejections
    gate_pass = overall_pass and component_pass and arena_pass
    return {
        "gate_pass": gate_pass,
        "reason": "PASS" if gate_pass else "SOURCE_BRANCH_GATE_REJECTED",
        "rejected_arenas": sorted(arena_rejections),
    }


def parent_clause_search_rows() -> list[dict[str, object]]:
    rows = [
        ("PCS1682_0_no_source_slot", "NoSourceOnlySpeciesSlot", "Hom(SpeciesLabel,Coeff_active_source)=empty", "1338/1416 closure rows", "REJECT_AS_CLOSURE_NOT_PARENT_ACTION", "CLOS1338_2_no_source_only_species_slot;BAN1416_2_object_language"),
        ("PCS1682_1_current_owner", "single_source_current_owner", "one Hilbert/Noether current functor before readout", "1076/1681 current owner rows", "REJECT_MISSING_CURRENT_OWNER", "OWN1076_2_current_owner;OCA1681_4_current_owner"),
        ("PCS1682_2_no_marker", "no_marker_readout_extension", "no marker/domain/boundary/readout masks as coefficient arguments", "1513/1681 marker countermodels", "REJECT_MISSING_PARENT_PROOF", "CM1513_3_comoving_marker;OCA1681_6_no_marker"),
        ("PCS1682_3_radiative", "radiative_readout_stability", "S_eff/readout preserve source coefficient domain", "1338/1416 unsigned readout rows", "REJECT_UNSIGNED_PARALLEL_GATE", "OLT1338_5_readout_stability;BAN1416_5_readout_radiative"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "search_id": search_id,
            "candidate_clause": candidate_clause,
            "non_ad_hoc_test": non_ad_hoc_test,
            "current_evidence": current_evidence,
            "search_result": search_result,
            "source_anchor": source_anchor,
            "parent_clause_signed": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for search_id, candidate_clause, non_ad_hoc_test, current_evidence, search_result, source_anchor in rows
    ]


def downstream_adoption_rows() -> list[dict[str, object]]:
    rows = [
        ("ADOPT1682_0_WEP", "WEP", "future MICROSCOPE/WEP source runner", "from Rsource_runner_gate_1682 import require_source_branch_gate; require_source_branch_gate('WEP')", "REQUIRED_BEFORE_SCORING", "currently raises/rejects"),
        ("ADOPT1682_1_R10", "R10", "future R10 alpha(lambda) runner", "require_source_branch_gate('R10')", "REQUIRED_BEFORE_SCORING", "currently raises/rejects"),
        ("ADOPT1682_2_Newton", "NEWTON_GM", "future Newton-GM/source normalization runner", "require_source_branch_gate('NEWTON_GM')", "REQUIRED_BEFORE_SCORING", "currently raises/rejects"),
        ("ADOPT1682_3_R11", "R11", "future R11 source/operator runner", "require_source_branch_gate('R11')", "REQUIRED_BEFORE_SCORING", "currently raises/rejects"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "adoption_id": adoption_id,
            "arena": arena,
            "target_runner_class": target_runner_class,
            "import_contract": import_contract,
            "adoption_status": adoption_status,
            "current_behavior": current_behavior,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for adoption_id, arena, target_runner_class, import_contract, adoption_status, current_behavior in rows
    ]


def decision_rows() -> list[dict[str, object]]:
    rows = [
        ("D1682_0_gate", "RUNNER_IMPORT_GATE_WRITTEN", "importable fail-closed source branch gate module now exists", "future runners must call it before scoring"),
        ("D1682_1_current", "CURRENT_SOURCE_BRANCH_REJECTED", "1681 component and arena matrices still reject all source-side use", "no WEP/R10/Newton/R11 score"),
        ("D1682_2_clause", "NO_PARENT_CLAUSE_FOUND", "narrow search finds closure or missing-proof rows, not a non-ad-hoc parent action clause", "continue derivation hunt or fill finite values"),
        ("D1682_3_next", "FILL_FIRST_COEFFICIENT_OR_PROVE_OWNER", "gate is now enforceable; next progress needs either first coefficient acquisition or a real owner derivation", "move to 1683"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for decision_id, decision, reason, next_action in rows
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    rows = [
        ("CG1682_0_import_gate", "source runner import gate pass", "BLOCKED", "gate dry run rejects current source branch"),
        ("CG1682_1_parent_clause", "non-ad-hoc parent owner clause found", "BLOCKED", "parent clause search signs no candidate"),
        ("CG1682_2_WEP", "WEP source-side score", "BLOCKED", "require_source_branch_gate('WEP') currently rejects"),
        ("CG1682_3_R10", "R10 source-side score", "BLOCKED", "require_source_branch_gate('R10') currently rejects"),
        ("CG1682_4_Newton", "Newton-GM source-side score", "BLOCKED", "require_source_branch_gate('NEWTON_GM') currently rejects"),
        ("CG1682_5_R11", "R11 source-side score", "BLOCKED", "require_source_branch_gate('R11') currently rejects"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "gate": gate,
            "gate_pass": False,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate, status, reason in rows
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1683-Y5-R2FR-first-Rsource-coefficient-fill-or-source-current-owner-derivation.md",
            "script": "scripts/Y5_R2FR_first_Rsource_coefficient_fill_or_source_current_owner_derivation.py",
            "objective": "try the highest-leverage source-side advance: either derive the single source-current owner/NoSourceOnlySpeciesSlot from parent action data, or fill the first finite R_source coefficient row with units, sign, source path, and arena projection",
            "success_condition": "at least one R_source row becomes genuinely theorem-zero or source-backed numeric/symbolic with units and local source path, while the 1682 import gate continues to reject incomplete arenas",
            "why_next": "1682 wired the refusal gate; progress now requires either a real derivation or the first real finite coefficient input",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def copy_outputs() -> None:
    for source_path, target_paths in COPY_TARGETS.items():
        for target_path in target_paths:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, target_path)
    shutil.copy2(GATE_MODULE, QUARANTINE / GATE_MODULE.name)
    shutil.copy2(GATE_MODULE, QUEUE / f"JR1682_{GATE_MODULE.name}")


def validate(
    source_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    dry_rows: list[dict[str, object]],
    parent_rows: list[dict[str, object]],
    adoption_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claims: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    sources_ok = all(bool_cell(row["exists"]) and bool_cell(row["needles_present"]) for row in source_rows)
    module_written = GATE_MODULE.exists() and "def require_source_branch_gate" in read_text(GATE_MODULE)
    gate_spec_complete = {row["gate_id"] for row in gate_rows} == {"GATE1682_0_module", "GATE1682_1_inputs", "GATE1682_2_component_rule", "GATE1682_3_arena_rule", "GATE1682_4_fail_closed"}
    dry_run_all_reject = all(not bool_cell(row["gate_pass"]) and row["reason"] == "SOURCE_BRANCH_GATE_REJECTED" for row in dry_rows)
    parent_clause_exact = {row["candidate_clause"] for row in parent_rows} == EXPECTED_PARENT_CLAUSES
    parent_clause_none_signed = all(not bool_cell(row["parent_clause_signed"]) for row in parent_rows)
    adoption_exact = {row["arena"] for row in adoption_rows} == EXPECTED_ARENAS
    adoption_required = all(row["adoption_status"] == "REQUIRED_BEFORE_SCORING" for row in adoption_rows)
    decision_safe = any(row["decision"] == "CURRENT_SOURCE_BRANCH_REJECTED" for row in decisions)
    claim_gate_safe = all(not bool_cell(row["gate_pass"]) and not bool_cell(row["claim_allowed"]) for row in claims)
    next_target_selected = next_rows[0]["next_target"] == "1683-Y5-R2FR-first-Rsource-coefficient-fill-or-source-current-owner-derivation.md"
    csv_parse = all(path.exists() and len(read_csv(path)) >= 1 for path in GENERATED_CSV)
    branch_copies = all(target_path.exists() for target_paths in COPY_TARGETS.values() for target_path in target_paths) and (QUARANTINE / GATE_MODULE.name).exists()
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_clean = not any(FORMALIZATION.rglob("*1682*")) if FORMALIZATION.exists() else True

    no_claim_flags = True
    blocked_not_ready = True
    for generated_path in CLAIM_CHECKED:
        for generated_row in read_csv(generated_path):
            if generated_row.get("valid_for_claim", "False").lower() == "true" or generated_row.get("claim_allowed", "False").lower() == "true":
                no_claim_flags = False
            if any(blocked_marker(value) for value in generated_row.values()):
                for claim_key in SCORE_FLAGS:
                    if claim_key in generated_row and bool_cell(generated_row[claim_key]):
                        blocked_not_ready = False

    checks = [
        ("VAL1682_0_sources_exist", sources_ok, "all cited 1682 source paths exist and required needles are present"),
        ("VAL1682_1_module_written", module_written, "importable source runner gate module exists with require_source_branch_gate"),
        ("VAL1682_2_gate_spec_complete", gate_spec_complete, "gate spec covers module, inputs, components, arenas, and fail-closed behavior"),
        ("VAL1682_3_dry_run_all_reject", dry_run_all_reject, "gate dry run rejects current ALL/WEP/R10/Newton/R11 source branch use"),
        ("VAL1682_4_parent_clause_exact", parent_clause_exact, "parent clause search covers the intended four high-leverage clauses"),
        ("VAL1682_5_parent_clause_none_signed", parent_clause_none_signed, "no parent clause is signed"),
        ("VAL1682_6_adoption_exact", adoption_exact, "downstream adoption matrix covers WEP, R10, Newton-GM, and R11"),
        ("VAL1682_7_adoption_required", adoption_required, "all downstream runner classes require gate import before scoring"),
        ("VAL1682_8_decision_safe", decision_safe, "decision records current source branch rejection"),
        ("VAL1682_9_claim_gate_safe", claim_gate_safe, "all claim gates remain false"),
        ("VAL1682_10_no_claim_flags", no_claim_flags, "all generated rows keep claim flags false"),
        ("VAL1682_11_blocked_not_ready", blocked_not_ready, "no blocked/rejected row is marked claim/scoring ready"),
        ("VAL1682_12_next_target_selected", next_target_selected, "next target selects first coefficient fill or source-current owner derivation"),
        ("VAL1682_13_csv_parse", csv_parse, "all generated 1682 CSVs parse"),
        ("VAL1682_14_branch_copies", branch_copies, "branch/quarantine/queue copies exist"),
        ("VAL1682_15_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL1682_16_formalization_untouched", formalization_clean, "no 1682 outputs found under formalization-workbench"),
    ]
    overall = all(result for _, result, _ in checks)
    validation_rows = [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, result, detail in checks
    ]
    validation_rows.append(
        {
            "check_id": "VAL1682_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1682 source-branch runner import gate and parent-clause search validation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return validation_rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    table_rows = []
    for row in rows:
        table_rows.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, separator, *table_rows])


def write_doc(
    source_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    dry_rows: list[dict[str, object]],
    parent_rows: list[dict[str, object]],
    adoption_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    body = f"""# 1682 - Source-Branch Runner Import Gate And Parent-Clause Search

**Private status:** enforcement/wiring checkpoint. No `q_loc=0`, local-GR pass, Newton pass, PPN pass, WEP pass, R10 pass, R11 pass, clock pass, orbital pass, or public claim is made.

## Verdict

1682 writes an importable fail-closed runner gate: `scripts/Rsource_runner_gate_1682.py`.

Current dry runs reject ALL, WEP, R10, Newton-GM, and R11 source-side use. The parent-clause search also signs no non-ad-hoc zero theorem clause. This does not solve the local-GR problem, but it stops the framework from accidentally pretending the source side is clean.

## Source Register

{markdown_table(source_rows, ["source_key", "source_path", "exists", "needles_present", "use_in_1682"])}

## Runner Import Gate Spec

{markdown_table(gate_rows, ["gate_id", "gate_object", "enforcement_rule", "current_status", "gate_pass"])}

## Gate Dry Run

{markdown_table(dry_rows, ["dry_run_id", "arena", "gate_pass", "reason", "rejected_arenas", "expected_behavior"])}

## Parent-Clause Search

{markdown_table(parent_rows, ["search_id", "candidate_clause", "non_ad_hoc_test", "search_result", "source_anchor"])}

## Downstream Runner Adoption

{markdown_table(adoption_rows, ["adoption_id", "arena", "target_runner_class", "import_contract", "adoption_status", "current_behavior"])}

## Decisions

{markdown_table(decision_rows_, ["decision_id", "decision", "reason", "next_action"])}

## Claim Gates

{markdown_table(claim_rows, ["gate_id", "gate", "gate_pass", "status", "reason"])}

## Next Target

{markdown_table(next_rows, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Working Interpretation

The source branch is now gated like engineering, not vibes. The next real progress must be one of two things: derive the source-current owner properly, or fill the first finite `R_source` coefficient with units/sign/source path/projection. Until then, runners get a locked door instead of a polite suggestion.
"""
    DOC.write_text(body, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    write_gate_module()
    source_rows = source_register_rows()
    gate_rows = gate_spec_rows()
    dry_rows = gate_dry_run_rows()
    parent_rows = parent_clause_search_rows()
    adoption_rows = downstream_adoption_rows()
    decisions = decision_rows()
    claims = claim_gate_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, source_rows, ["branch_id", "source_key", "source_path", "exists", "needles_present", "required_needles", "use_in_1682", "valid_for_claim", "claim_allowed"])
    write_csv(GATE_SPEC, gate_rows, ["branch_id", "gate_id", "gate_object", "enforcement_rule", "current_status", "gate_pass", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(GATE_DRY_RUN, dry_rows, ["branch_id", "dry_run_id", "arena", "gate_pass", "reason", "rejected_arenas", "component_failures", "expected_behavior", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(PARENT_SEARCH, parent_rows, ["branch_id", "search_id", "candidate_clause", "non_ad_hoc_test", "current_evidence", "search_result", "source_anchor", "parent_clause_signed", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(DOWNSTREAM_ADOPTION, adoption_rows, ["branch_id", "adoption_id", "arena", "target_runner_class", "import_contract", "adoption_status", "current_behavior", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(DECISION, decisions, ["branch_id", "decision_id", "decision", "reason", "next_action", "valid_for_claim", "claim_allowed"])
    write_csv(CLAIM_GATE, claims, ["branch_id", "gate_id", "gate", "gate_pass", "status", "reason", "valid_for_claim", "claim_allowed"])
    write_csv(NEXT_TARGET, next_rows, ["branch_id", "next_target", "script", "objective", "success_condition", "why_next", "valid_for_claim", "claim_allowed"])

    copy_outputs()
    validation_rows = validate(source_rows, gate_rows, dry_rows, parent_rows, adoption_rows, decisions, claims, next_rows)
    write_csv(VALIDATION, validation_rows, ["check_id", "result", "detail", "valid_for_claim", "claim_allowed"])
    write_doc(source_rows, gate_rows, dry_rows, parent_rows, adoption_rows, decisions, claims, next_rows, validation_rows)

    failed_rows = [row for row in validation_rows if row["result"] != "PASS"]
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    print(f"wrote {GATE_MODULE}")
    if failed_rows:
        for failed_row in failed_rows:
            print(f"FAIL {failed_row['check_id']}: {failed_row['detail']}")
        raise SystemExit(1)
    print("1682 validation PASS")


if __name__ == "__main__":
    main()

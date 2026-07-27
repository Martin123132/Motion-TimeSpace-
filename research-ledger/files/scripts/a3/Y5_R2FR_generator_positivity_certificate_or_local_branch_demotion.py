from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
QUARANTINE = MICROSCOPE / "quarantine" / "1615"
INPUT_1615 = QUARANTINE / "input"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1615-Y5-R2FR-generator-positivity-certificate-or-local-branch-demotion.md"

SOURCE_FILES = {
    "1614_doc": ROOT / "1614-Y5-R2FR-parent-cone-basis-or-official-CMSM-acquisition.md",
    "1614_validation": OUT / "P8_Y5_BRR545_1614_VALIDATION.csv",
    "1614_next": OUT / "P8_Y5_PARENT_QLOC_1614_NEXT_TARGET.csv",
    "1614_parent_cone": OUT / "P8_Y5_PARENT_QLOC_1614_PARENT_CONE_BASIS_THEOREM_ATTEMPT.csv",
    "1614_generator": OUT / "P8_Y5_PARENT_QLOC_1614_GENERATOR_POSITIVITY_CERTIFICATE_CONTRACT.csv",
    "1614_blockers": OUT / "P8_Y5_PARENT_QLOC_1614_PARENT_CONE_BLOCKER_AUDIT.csv",
    "1614_claim_gate": OUT / "P8_Y5_PARENT_QLOC_1614_CLAIM_GATE.csv",
    "1614_acquisition": OUT / "P8_Y5_PARENT_QLOC_1614_OFFICIAL_CMSM_ACQUISITION_STATUS.csv",
    "1010_q_loc": ROOT / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
    "1009_parent_contract": ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
    "02_motion_load": ROOT / "02-motion-load-local-GR-reduction.md",
}

NEEDLES = {
    "1614_doc": ["PARENT_CONE_BASIS_NOT_DERIVED", "NEXT_1615_GENERATOR_POSITIVITY_CERTIFICATE_OR_LOCAL_BRANCH_DEMOTION"],
    "1614_validation": ["VAL1614_OVERALL", "PASS"],
    "1614_next": ["1615-Y5-R2FR-generator-positivity-certificate-or-local-branch-demotion.md", "demote local-GR proof route"],
    "1614_parent_cone": ["PCB1614_5_verdict", "PARENT_CONE_BASIS_NOT_DERIVED"],
    "1614_generator": ["GPC1614_0_parent_basis", "MISSING_PARENT_BASIS"],
    "1614_blockers": ["PBL1614_5_official_files", "OPEN_BLOCKER"],
    "1614_claim_gate": ["CG1614_4_local_GR", "BLOCKED"],
    "1614_acquisition": ["OCA1614_1_CMSM_module", "AUTH_OR_TIMEOUT_NO_ROWS_CAPTURED"],
    "1010_q_loc": ["`q_loc` is retained as an explicit nonclaim residual", "CG1010_5_Htau_MHref_local_GR"],
    "1009_parent_contract": ["CG1009_5_Htau_MHref_local_GR", "total parent current chain remains incomplete"],
    "02_motion_load": ["yes conditionally, but not yet fundamentally", "motion_load_local_GR_reduction_conditional_not_promoted"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1615_SOURCE_REGISTER.csv"
GENERATOR_ATTEMPT = OUT / "P8_Y5_PARENT_QLOC_1615_GENERATOR_POSITIVITY_CERTIFICATE_ATTEMPT.csv"
DEMOTION_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1615_LOCAL_BRANCH_DEMOTION_LEDGER.csv"
CLAIM_CEILING = OUT / "P8_Y5_PARENT_QLOC_1615_CLAIM_CEILING_MATRIX.csv"
REOPEN_CONDITIONS = OUT / "P8_Y5_PARENT_QLOC_1615_REOPEN_CONDITIONS.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1615_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1615_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1615_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1615_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1615_VALIDATION.csv"

COPY_TARGETS = {
    GENERATOR_ATTEMPT: [
        QUARANTINE / "GENERATOR_POSITIVITY_CERTIFICATE_ATTEMPT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_generator_positivity_certificate_attempt_nonclaim_1615.csv",
    ],
    DEMOTION_LEDGER: [
        QUARANTINE / "LOCAL_BRANCH_DEMOTION_LEDGER_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_local_branch_demotion_ledger_nonclaim_1615.csv",
    ],
    CLAIM_CEILING: [
        QUARANTINE / "CLAIM_CEILING_MATRIX_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_claim_ceiling_matrix_nonclaim_1615.csv",
    ],
    REOPEN_CONDITIONS: [
        QUARANTINE / "REOPEN_CONDITIONS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_reopen_conditions_nonclaim_1615.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE_CLOSED.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_closed_1615.csv",
    ],
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (source_id, path) in enumerate(SOURCE_FILES.items()):
        text = read_text(path) if path.exists() else ""
        needles = NEEDLES[source_id]
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1615_{index}_{source_id}",
                "source_path": rel(path) if path.exists() else str(path),
                "exists": path.exists(),
                "needle_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "source_role": "1615_generator_positivity_or_local_branch_demotion_input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def generator_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "attempt_id": "GPA1615_0_exact_target",
            "certificate_piece": "parent generator positivity certificate",
            "required_statement": "there exists a parent basis B and generators g_i of C with K_CMSM(g_i)>=k_i>0 and signed covariance/no-hidden-tail rules",
            "current_status": "TARGET_EXACT_BUT_UNSIGNED",
            "what_would_follow": "C cap ker(K_CMSM)=empty and c_min>0",
            "blocking_gap": "basis, generators, readout lower bounds, material projection, covariance, and domain order remain unsigned",
            "certificate_signed": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "attempt_id": "GPA1615_1_parent_basis",
            "certificate_piece": "single parent basis B",
            "required_statement": "K_CMSM and V_source_material are represented in the same parent-owned component basis",
            "current_status": "MISSING_PARENT_BASIS",
            "what_would_follow": "inner product and cone distance are meaningful",
            "blocking_gap": "1614 basis duality blocker remains open",
            "certificate_signed": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "attempt_id": "GPA1615_2_generator_list",
            "certificate_piece": "allowed cone C=cone{g_i}",
            "required_statement": "ordinary source/material directions are nonnegative combinations of parent generators with no hidden signed component",
            "current_status": "MISSING_GENERATOR_LIST",
            "what_would_follow": "source/material positivity becomes a theorem in parent basis",
            "blocking_gap": "physical matter graph is not parent-owned and material tensor is missing",
            "certificate_signed": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "attempt_id": "GPA1615_3_readout_lower_bounds",
            "certificate_piece": "K_CMSM(g_i)>=k_i>0",
            "required_statement": "each generator has a positive readout lower bound after orbit/mask/correction terms",
            "current_status": "MISSING_K_GENERATOR_BOUNDS",
            "what_would_follow": "positive cone cannot silently cancel in the readout",
            "blocking_gap": "official K arrays or parent sign theorem absent",
            "certificate_signed": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "attempt_id": "GPA1615_4_material_covariance_domain",
            "certificate_piece": "material/covariance/domain-order closure",
            "required_statement": "Ti/Pt projection lies in C, omitted terms are nonnegative/bounded, and masks/windows are downstream-only",
            "current_status": "MISSING_MATERIAL_COVARIANCE_DOMAIN_CERTIFICATE",
            "what_would_follow": "generator proof would be physical rather than a basis trick",
            "blocking_gap": "full material tensor, covariance/no-double-counting, and downstream-domain proof absent",
            "certificate_signed": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "attempt_id": "GPA1615_5_verdict",
            "certificate_piece": "1615 generator positivity verdict",
            "required_statement": "all certificate pieces signed together",
            "current_status": "GENERATOR_POSITIVITY_CERTIFICATE_NOT_SIGNED",
            "what_would_follow": "local branch could reopen at c_min/tau gates",
            "blocking_gap": "at least six required clauses remain unsigned",
            "certificate_signed": False,
            "claim_allowed": False,
        },
    ]


def demotion_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "demotion_id": "LBD1615_0_status",
            "route": "local-GR via R2/fR WEP/source-normalization branch",
            "new_status": "CLOSURE_OR_SOURCE_DATA_DEPENDENT_NOT_DERIVED",
            "reason": "generator positivity, official CMSM c_min, q_loc action-zero, and source-measure bridges remain unclosed",
            "allowed_use": "private closure benchmark, source-data acquisition route, or future parent-theorem target",
            "forbidden_use": "derived Newton/GR/WEP/R10/PPN claim",
            "demoted": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "demotion_id": "LBD1615_1_closure",
            "route": "closure axiom / local plateau / SPM-like local lock",
            "new_status": "EXPLICIT_ASSUMPTION_ONLY",
            "reason": "closure can organize calculations but cannot count as derivation",
            "allowed_use": "labelled closure model or benchmark",
            "forbidden_use": "parent-action proof or local-GR theorem-zero",
            "demoted": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "demotion_id": "LBD1615_2_source_data",
            "route": "official CMSM/source-data route",
            "new_status": "OPEN_DATA_ROUTE_NONCLAIM",
            "reason": "official rows can compute c_min but are not captured",
            "allowed_use": "quarantine import and nonclaim c_min evaluation",
            "forbidden_use": "claim from pointer/template/surrogate rows",
            "demoted": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "demotion_id": "LBD1615_3_parent_theorem",
            "route": "parent generator/action theorem route",
            "new_status": "OPEN_DERIVATION_ROUTE_NOT_CLOSED",
            "reason": "exact certificate clauses are known but unsigned",
            "allowed_use": "future proof attempt with parent basis/generator/readout/material/covariance signatures",
            "forbidden_use": "claim from conditional lemmas alone",
            "demoted": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_ceiling_rows() -> list[dict[str, Any]]:
    rows = [
        ("CCM1615_0_private_math", "conditional theorem work", "ALLOWED", "conditional lemmas may be used as map-making tools"),
        ("CCM1615_1_empirical_closure", "labelled closure benchmark", "ALLOWED_NONCLAIM", "allowed only if described as fitted/closure, not derivation"),
        ("CCM1615_2_source_data", "quarantined official source-data computation", "ALLOWED_NONCLAIM", "allowed only with provenance and no promotion before gates pass"),
        ("CCM1615_3_derived_local_GR", "derived local GR/Newton recovery", "BLOCKED", "requires parent action/current, q_loc zero or residual bound, source-measure bridge, and c_min/tau gates"),
        ("CCM1615_4_WEP_R10_PPN", "WEP/R10/PPN/local claim", "BLOCKED", "requires official arrays or parent theorem plus all residual gates"),
        ("CCM1615_5_public_claim", "public claim that MTS reduces to GR", "BLOCKED", "current status is closure/source-data dependent, not theorem-derived"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "ceiling_id": ceiling_id,
            "claim_type": claim_type,
            "ceiling": ceiling,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for ceiling_id, claim_type, ceiling, reason in rows
    ]


def reopen_condition_rows() -> list[dict[str, Any]]:
    rows = [
        ("ROC1615_0_parent_basis", "same parent basis B for K_CMSM and V_source_material", "GPC1614_0", "MISSING"),
        ("ROC1615_1_generators", "parent generator list for allowed cone C", "GPC1614_1", "MISSING"),
        ("ROC1615_2_readout_bounds", "K_CMSM(g_i)>=k_i>0 or signed-margin interval certificate", "GPC1614_2", "MISSING"),
        ("ROC1615_3_material_projection", "Ti/Pt material/source projection into C with units and provenance", "GPC1614_3", "MISSING"),
        ("ROC1615_4_covariance", "covariance/no-hidden-cancellation rule for omitted corrections/tails", "GPC1614_4", "MISSING"),
        ("ROC1615_5_domain_order", "masks/orbit/windows proven downstream-only", "GPC1614_5", "MISSING"),
        ("ROC1615_6_q_loc", "q_loc derived zero or bounded residual from parent S_GK/Helmholtz/Euler chain", "1010", "MISSING"),
        ("ROC1615_7_source_measure", "worldtube/source-measure/GM bridge owned before orbital fitting", "1009", "MISSING"),
        ("ROC1615_8_official_arrays", "official CMSM readout/material/mask/alignment rows in quarantine", "1614 acquisition", "MISSING"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "condition_id": condition_id,
            "required_condition": condition,
            "source_anchor": anchor,
            "current_status": status,
            "reopens_local_claim": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for condition_id, condition, anchor, status in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1615_0_generator_certificate",
            "input_state": "all generator positivity certificate clauses unsigned",
            "runner_result": "REJECT_GENERATOR_POSITIVITY_CERTIFICATE",
            "effect": "no c_min/local branch proof promotion",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1615_1_demotion",
            "input_state": "generator certificate failed and official arrays absent",
            "runner_result": "DEMOTE_LOCAL_BRANCH_TO_CLOSURE_OR_SOURCE_DATA_DEPENDENCY",
            "effect": "prevents accidental derived-local-GR claim while preserving future routes",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG1615_0_generator_certificate", "parent generator positivity certificate", "BLOCKED", "certificate not signed"),
        ("CG1615_1_cmin", "positive c_min/tau_min theorem", "BLOCKED", "no generator certificate or official alignment result"),
        ("CG1615_2_q_loc", "q_loc zero/local residual closure", "BLOCKED", "1010 retains q_loc as explicit residual"),
        ("CG1615_3_source_measure", "source-measure/GM bridge", "BLOCKED", "1009 keeps parent current chain incomplete"),
        ("CG1615_4_derived_local_GR", "derived Newton/GR local branch", "BLOCKED", "branch demoted to closure/source-data dependency"),
        ("CG1615_5_public_claim", "public local-GR/WEP/R10/PPN claim", "BLOCKED", "claim ceiling remains private nonclaim only"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, claim, status, reason in gates
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1615_0_generator",
            "decision": "GENERATOR_POSITIVITY_CERTIFICATE_NOT_SIGNED",
            "reason": "parent basis, generators, readout lower bounds, material projection, covariance and domain-order clauses remain missing",
            "next_action": "do not reopen local-GR gates from generator positivity",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1615_1_demote",
            "decision": "LOCAL_BRANCH_DEMOTED_TO_CLOSURE_OR_SOURCE_DATA_DEPENDENCY",
            "reason": "the branch has exact conditional math but not a parent-signed derivation",
            "next_action": "treat local GR as an explicit closure/data route until reopen conditions are met",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1615_2_next",
            "decision": "NEXT_1616_LOCAL_BRANCH_STATUS_REGISTER_AND_REOPEN_ROADMAP",
            "reason": "after demotion, the project needs a central status register tying q_loc, source-measure, c_min, CMSM, and closure claims together",
            "next_action": "build a local-branch status register and choose the highest-leverage derivation target",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1616-Y5-R2FR-local-branch-status-register-and-reopen-roadmap.md",
            "script": "scripts/Y5_R2FR_local_branch_status_register_and_reopen_roadmap.py",
            "objective": "centralize the local-GR branch status after demotion and rank reopen routes: q_loc action, source-measure bridge, generator certificate, or official CMSM data",
            "success_condition": "one status register prevents claim drift and selects the next derivation target without local-GR promotion",
            "do_not": "do not use tau_eff=1, symbolic K alone, surrogate arrays, bound inversion, closure-only zero, measured-G absorption, or public/local-GR claims",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def csv_parses(paths: list[Path]) -> bool:
    try:
        for path in paths:
            read_csv(path)
    except Exception:
        return False
    return True


def no_claim_flags(paths: list[Path]) -> bool:
    for path in paths:
        for row in read_csv(path):
            for field in (
                "certificate_signed",
                "reopens_local_claim",
                "score_ready",
                "valid_prediction_row",
                "valid_for_claim",
                "claim_allowed",
            ):
                if truthy(row.get(field, "")):
                    return False
    return True


def no_formalization_1615() -> bool:
    if not FORMALIZATION.exists():
        return True
    artifact_markers = (
        "1615-Y5",
        "P8_Y5_PARENT_QLOC_1615",
        "P8_Y5_BRR545_1615",
        "Y5_R2FR_generator_positivity_certificate_or_local_branch_demotion",
        "R2FR_generator_positivity",
        "R2FR_local_branch_demotion",
        "R2FR_claim_ceiling_matrix",
    )
    return not any(any(marker in path.name for marker in artifact_markers) for path in FORMALIZATION.rglob("*"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    generator = read_csv(GENERATOR_ATTEMPT)
    demotion = read_csv(DEMOTION_LEDGER)
    ceiling = read_csv(CLAIM_CEILING)
    reopen = read_csv(REOPEN_CONDITIONS)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    copies = [target for targets in COPY_TARGETS.values() for target in targets]
    checks = [
        ("VAL1615_0_sources_exist", all(truthy(row["exists"]) for row in sources), "all cited 1615 local source paths exist"),
        ("VAL1615_1_needles_found", all(truthy(row["needle_found"]) for row in sources), "all required 1615 source needles found"),
        ("VAL1615_2_input_dir_ready", INPUT_1615.exists(), "1615 quarantine input directory exists"),
        ("VAL1615_3_generator_refused", any(row["attempt_id"] == "GPA1615_5_verdict" and row["current_status"] == "GENERATOR_POSITIVITY_CERTIFICATE_NOT_SIGNED" for row in generator), "generator positivity certificate remains unsigned"),
        ("VAL1615_4_demotion_written", any(row["demotion_id"] == "LBD1615_0_status" and row["new_status"] == "CLOSURE_OR_SOURCE_DATA_DEPENDENT_NOT_DERIVED" for row in demotion), "local branch demotion ledger written"),
        ("VAL1615_5_claim_ceiling_blocks_public", any(row["ceiling_id"] == "CCM1615_5_public_claim" and row["ceiling"] == "BLOCKED" for row in ceiling), "public/derived local claim ceiling blocked"),
        ("VAL1615_6_reopen_conditions_missing", len(reopen) >= 9 and all(row["current_status"] == "MISSING" for row in reopen), "all reopen conditions remain missing"),
        ("VAL1615_7_runner_demotes", any(row["runner_id"] == "RUN1615_1_demotion" and row["runner_result"] == "DEMOTE_LOCAL_BRANCH_TO_CLOSURE_OR_SOURCE_DATA_DEPENDENCY" for row in runner), "runner demotes local branch"),
        ("VAL1615_8_claim_gates_closed", gates and all(row["status"] == "BLOCKED" and row["claim_allowed"].lower() == "false" for row in gates), "all 1615 claim gates remain closed"),
        ("VAL1615_9_decision_next", any(row["decision"] == "NEXT_1616_LOCAL_BRANCH_STATUS_REGISTER_AND_REOPEN_ROADMAP" for row in decisions), "decision selects 1616 status register"),
        ("VAL1615_10_csv_parse", csv_parses(generated_csvs), "all generated 1615 CSVs parse"),
        ("VAL1615_11_claim_safety_flags", no_claim_flags(generated_csvs), "no generated 1615 rows are certificate-signed, reopened, score-ready, prediction rows, valid-for-claim, or claim-allowed"),
        ("VAL1615_12_branch_copies", all(path.exists() for path in copies), "branch/quarantine nonclaim copies exist"),
        ("VAL1615_13_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1615_14_formalization_untouched", no_formalization_1615(), "no 1615 outputs found under formalization-workbench"),
    ]
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if ok else "FAIL",
            "detail": detail,
        }
        for check_id, ok, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1615_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1615 generator positivity certificate or local branch demotion validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "/") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, Any]],
    generator: list[dict[str, Any]],
    demotion: list[dict[str, Any]],
    ceiling: list[dict[str, Any]],
    reopen: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1615 - R2/fR Generator Positivity Certificate Or Local Branch Demotion",
                "## Verdict\n"
                "- 1615 tries to sign the parent generator positivity certificate and cannot sign it from the current corpus.\n"
                "- The exact route remains alive: a parent basis, cone generators, positive readout lower bounds, material projection, covariance, and downstream-domain proof would reopen `c_min>0`.\n"
                "- Because those clauses are absent and official CMSM arrays are not captured, the local-GR/WEP/source-normalization route is demoted to `CLOSURE_OR_SOURCE_DATA_DEPENDENT_NOT_DERIVED`.\n"
                "- This is not a death sentence for MTS; it is a guardrail saying the current local branch may be used as closure benchmark or data-acquisition route, not as a derived GR/Newton theorem.\n"
                "- No WEP, R10, PPN, clock, orbital, Newton, local-GR, beta/coupling, or public claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## Generator Positivity Certificate Attempt",
                md_table(generator, ["attempt_id", "certificate_piece", "current_status", "what_would_follow", "blocking_gap", "certificate_signed"]),
                "## Local Branch Demotion Ledger",
                md_table(demotion, ["demotion_id", "route", "new_status", "reason", "allowed_use", "forbidden_use"]),
                "## Claim Ceiling Matrix",
                md_table(ceiling, ["ceiling_id", "claim_type", "ceiling", "reason"]),
                "## Reopen Conditions",
                md_table(reopen, ["condition_id", "required_condition", "source_anchor", "current_status", "reopens_local_claim"]),
                "## Runner",
                md_table(runner, ["runner_id", "input_state", "runner_result", "effect"]),
                "## Claim Gates",
                md_table(gates, ["gate_id", "claim", "status", "reason"]),
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "reason", "next_action"]),
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "success_condition", "do_not"]),
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    INPUT_1615.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    generator = generator_attempt_rows()
    demotion = demotion_rows()
    ceiling = claim_ceiling_rows()
    reopen = reopen_condition_rows()
    runner = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        GENERATOR_ATTEMPT,
        DEMOTION_LEDGER,
        CLAIM_CEILING,
        REOPEN_CONDITIONS,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(GENERATOR_ATTEMPT, generator)
    write_csv(DEMOTION_LEDGER, demotion)
    write_csv(CLAIM_CEILING, ceiling)
    write_csv(REOPEN_CONDITIONS, reopen)
    write_csv(RUNNER, runner)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, generator, demotion, ceiling, reopen, runner, gates, decisions, next_rows, validation)


if __name__ == "__main__":
    main()

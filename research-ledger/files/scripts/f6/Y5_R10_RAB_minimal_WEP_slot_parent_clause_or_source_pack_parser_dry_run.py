from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_ROOT = MICROSCOPE / "branch_locked_wep"
COEFFICIENT_ROOT = BRANCH_ROOT / "coefficients"
RESIDUAL_ROOT = BRANCH_ROOT / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1439-Y5-R10-RAB-minimal-WEP-slot-parent-clause-or-source-pack-parser-dry-run.md"

BRANCH_ID_FILE = BRANCH_ROOT / "branch_id.csv"
NEXT_1438 = OUT / "P8_Y5_R10_1438_NEXT_TARGET.csv"
VALIDATION_1438 = OUT / "P8_Y5_BRR545_1438_VALIDATION.csv"
ZERO_ATTEMPT_1438 = OUT / "P8_Y5_R10_1438_C_PARENT_WEP_SLOT_ZERO_ATTEMPT.csv"
SLOT_STATUS_1438 = OUT / "P8_Y5_R10_1438_C_PARENT_WEP_SLOT_STATUS.csv"
SOURCE_PACK_MANIFEST_1438 = OUT / "P8_Y5_R10_1438_OFFICIAL_MICROSCOPE_SOURCE_PACK_MANIFEST.csv"
SOURCE_PACK_FILE_SCHEMA_1438 = OUT / "P8_Y5_R10_1438_SOURCE_PACK_FILE_SCHEMA.csv"
RUNNER_1438 = OUT / "P8_Y5_R10_1438_SOURCE_PACK_RUNNER_DRYRUN_STATUS.csv"
PROMOTION_GATES_1438 = OUT / "P8_Y5_R10_1438_PROMOTION_GATES.csv"
BRANCH_C_PARENT_ATTEMPT_1438 = COEFFICIENT_ROOT / "C_parent_WEP_slot_zero_attempt.csv"
BRANCH_SOURCE_PACK_MANIFEST_1438 = RESIDUAL_ROOT / "official_microscope_source_pack_manifest.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1439_SOURCE_REGISTER.csv"
MINIMAL_PARENT_CLAUSE = OUT / "P8_Y5_R10_1439_MINIMAL_PARENT_CLAUSE.csv"
COUNTERMODEL_LEDGER = OUT / "P8_Y5_R10_1439_COUNTERMODEL_LEDGER.csv"
SOURCE_PACK_PARSER_DRYRUN = OUT / "P8_Y5_R10_1439_SOURCE_PACK_PARSER_DRYRUN.csv"
REQUIRED_COLUMN_AUDIT = OUT / "P8_Y5_R10_1439_REQUIRED_COLUMN_AUDIT.csv"
CLAIM_GATE = OUT / "P8_Y5_R10_1439_CLAIM_GATE.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1439_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1439_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1439_VALIDATION.csv"

BRANCH_MINIMAL_PARENT_CLAUSE = COEFFICIENT_ROOT / "C_parent_WEP_minimal_parent_clause.csv"
BRANCH_SOURCE_PACK_PARSER_DRYRUN = RESIDUAL_ROOT / "source_pack_parser_dryrun.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").replace("\r", " ").strip()


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows supplied for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: clean(row.get(key, "")) for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def text_has(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="ignore")


def md_cell(value: Any) -> str:
    return clean(value).replace("|", "\\|")


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def count_formalization_modified_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED
    )


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def branch_id() -> str:
    rows = read_csv(BRANCH_ID_FILE)
    if len(rows) != 1:
        raise ValueError(f"expected one branch row, got {len(rows)}")
    value = rows[0].get("same_parent_branch_id", "").strip()
    if not value:
        raise ValueError("same_parent_branch_id missing")
    return value


def source_register_rows(branch: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC1439_0_1438_next", NEXT_1438, "NEXT1438_0_1439", "1438 handoff selecting minimal clause and parser dry-run."),
        ("SRC1439_1_1438_validation", VALIDATION_1438, "VAL1438_12_overall", "1438 validation summary."),
        ("SRC1439_2_zero_attempt", ZERO_ATTEMPT_1438, "CZ1438_5_zero_certificate", "1438 C_parent zero attempt."),
        ("SRC1439_3_slot_status", SLOT_STATUS_1438, "CPS1438_0_WEP_C_parent", "1438 C_parent WEP slot status."),
        ("SRC1439_4_manifest", SOURCE_PACK_MANIFEST_1438, "PACK1438_5_C_parent_import", "1438 official source-pack manifest."),
        ("SRC1439_5_file_schema", SOURCE_PACK_FILE_SCHEMA_1438, "SFS1438_10", "1438 material/source file schema."),
        ("SRC1439_6_runner", RUNNER_1438, "RUN1438_1_source_pack", "1438 source-pack dry-run status."),
        ("SRC1439_7_gates", PROMOTION_GATES_1438, "GATE1438_6_no_shortcuts", "1438 promotion gates."),
        ("SRC1439_8_branch_id", BRANCH_ID_FILE, branch, "active branch lock."),
        ("SRC1439_9_branch_zero", BRANCH_C_PARENT_ATTEMPT_1438, "CZ1438_5_zero_certificate", "branch C_parent attempt copy."),
        ("SRC1439_10_branch_manifest", BRANCH_SOURCE_PACK_MANIFEST_1438, "PACK1438_5_C_parent_import", "branch source-pack manifest copy."),
    ]
    return [
        {
            "source_id": source_id,
            "source_path": str(path),
            "path_exists": path.exists(),
            "anchor": anchor,
            "anchor_found": text_has(path, anchor),
            "role": role,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for source_id, path, anchor, role in specs
    ]


def minimal_parent_clause_rows(branch: str) -> list[dict[str, Any]]:
    rows = [
        (
            "MPC1439_0_clause",
            "candidate sufficient parent clause",
            "On the local WEP branch, the parent matter action descends to a single observed metric/coframe and all ordinary material/source labels enter only through universal stress-energy; no independent species, composition, source, boundary, or readout functional survives the quotient.",
            "SUFFICIENT_IF_PARENT_DERIVED",
            "would force the Ti/Pt differential WEP-slot functional derivative to vanish",
        ),
        (
            "MPC1439_1_formal_zero",
            "formal consequence",
            "For any vertical/differential Ti/Pt material variation v_WEP in ker(Dq_obs), delta_v_WEP S_matter = 0 and delta_v_WEP S_source/readout = 0, so C_parent_WEP_TiPt = 0.",
            "CONDITIONAL_DERIVED_ZERO_SHAPE",
            "valid only if every descent/no-label premise is proved in the parent action",
        ),
        (
            "MPC1439_2_required_premises",
            "proof obligations",
            "matter descent; no species marker; source common-mode only; full material tensor quotient-blindness; readout/boundary silence; conservation/gauge compatibility",
            "UNPROVED_IN_CURRENT_CORPUS",
            "these are exactly the unsigned 1438 clauses in a compact parent-action form",
        ),
        (
            "MPC1439_3_strength_warning",
            "strength warning",
            "The clause is close to assuming metric universality/EEP for ordinary matter; adopting it without derivation would make WEP pass closure-only, not a derived MTS result.",
            "TOO_STRONG_AS_AXIOM_FOR_CLAIM",
            "use as proof target, not as public claim",
        ),
        (
            "MPC1439_4_verdict",
            "current verdict",
            "The minimal clause is stated as a sufficient theorem target, but is not adopted as a derived result and does not promote C_parent_WEP.",
            "NOT_ADOPTED_NOT_ZERO_CERTIFIED",
            "C_parent_WEP remains missing; source-pack route remains active",
        ),
    ]
    return [
        {
            "same_parent_branch_id": branch,
            "clause_id": clause_id,
            "clause_role": clause_role,
            "statement": statement,
            "status": status,
            "effect": effect,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for clause_id, clause_role, statement, status, effect in rows
    ]


def countermodel_rows(branch: str) -> list[dict[str, Any]]:
    rows = [
        (
            "CM1439_0_species_marker",
            "S_matter contains a tiny branch/source field multiplying a material label b_A, with b_TA6V != b_PtRh10.",
            "nonzero Ti/Pt differential derivative",
            "kills automatic C_parent_WEP=0 unless no-species-marker descent is proved",
        ),
        (
            "CM1439_1_source_weight",
            "Earth/source worldtube couples to a retained parent component with composition-dependent test-mass response.",
            "relative source acceleration survives measured-G common-mode subtraction",
            "kills source-common-mode shortcut",
        ),
        (
            "CM1439_2_readout_projection",
            "readout/orbit kernel projects a boundary/shear residual differently into the two test-mass channels.",
            "nonzero K_CMSM-weighted relative signal",
            "kills readout silence unless official kernel plus theorem proves cancellation",
        ),
        (
            "CM1439_3_basis_mismatch",
            "C_parent, material tensor, source vector, and readout kernel are assembled from different bases or surrogate rows.",
            "apparent zero/pass becomes convention artifact",
            "forces same-parent-branch classifier before scoring",
        ),
    ]
    return [
        {
            "same_parent_branch_id": branch,
            "countermodel_id": countermodel_id,
            "construction": construction,
            "result": result,
            "lesson": lesson,
            "claim_effect": "BLOCKS_DERIVED_ZERO_UNLESS_EXCLUDED_BY_PARENT_ACTION",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for countermodel_id, construction, result, lesson in rows
    ]


def parse_header(path: Path) -> list[str]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        return next(reader, [])


def parser_dryrun_rows(branch: str, manifest_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for manifest in manifest_rows:
        target_path = Path(manifest["target_path"])
        schema_path = Path(manifest["schema_path"])
        required_columns = [part.strip() for part in manifest["required_columns_or_fields"].split(";") if part.strip()]
        if not target_path.exists():
            header: list[str] = []
            missing_columns = required_columns
            parser_status = "REFUSED_TARGET_FILE_MISSING"
        else:
            header = parse_header(target_path)
            missing_columns = [column for column in required_columns if column not in header]
            parser_status = "PASS_HEADER_ONLY_NONCLAIM" if not missing_columns else "REFUSED_REQUIRED_COLUMNS_MISSING"
        rows.append(
            {
                "same_parent_branch_id": branch,
                "parser_id": f"PARSE1439_{len(rows)}",
                "manifest_id": manifest["manifest_id"],
                "pack_item": manifest["pack_item"],
                "target_path": str(target_path),
                "target_exists": target_path.exists(),
                "schema_path": str(schema_path),
                "schema_exists": schema_path.exists(),
                "required_column_count": len(required_columns),
                "header_column_count": len(header),
                "missing_columns": ";".join(missing_columns) if missing_columns else "NONE",
                "parser_status": parser_status,
                "promotion_effect": "REFUSE_SCORE_UNTIL_TARGET_FILE_EXISTS_AND_ALL_COLUMNS_PASS",
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def required_column_audit_rows(branch: str, manifest_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for manifest in manifest_rows:
        target_path = Path(manifest["target_path"])
        header = parse_header(target_path) if target_path.exists() else []
        for column in [part.strip() for part in manifest["required_columns_or_fields"].split(";") if part.strip()]:
            rows.append(
                {
                    "same_parent_branch_id": branch,
                    "audit_id": f"RCA1439_{len(rows)}",
                    "manifest_id": manifest["manifest_id"],
                    "pack_item": manifest["pack_item"],
                    "required_column_or_field": column,
                    "target_path": str(target_path),
                    "target_exists": target_path.exists(),
                    "column_present": column in header,
                    "audit_status": "WAITING_FOR_TARGET_FILE" if not target_path.exists() else ("PASS" if column in header else "MISSING_COLUMN"),
                    "valid_prediction_row": False,
                    "valid_for_claim": False,
                    "claim_allowed": False,
                }
            )
    return rows


def claim_gate_rows(branch: str) -> list[dict[str, Any]]:
    gates = [
        ("CG1439_0_clause_not_adopted", "minimal parent clause is a sufficient proof target, not an adopted axiom"),
        ("CG1439_1_countermodels_live", "countermodels remain live until excluded by the parent action"),
        ("CG1439_2_parser_refuses_missing", "source-pack parser must refuse missing target files"),
        ("CG1439_3_no_header_only_claim", "even a header pass would be nonclaim until numeric/provenance/branch checks pass"),
        ("CG1439_4_no_shortcuts", "no tau_eff=1, no measured-G absorption, no bound-as-prediction, no surrogate basis mixing"),
        ("CG1439_5_local_gr_blocked", "WEP/local-GR claim remains blocked while C_parent_WEP is missing"),
    ]
    return [
        {
            "same_parent_branch_id": branch,
            "gate_id": gate_id,
            "gate": gate,
            "gate_status": "LOCKED_CLAIM_FALSE",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate in gates
    ]


def decision_rows(branch: str) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": branch,
            "decision_id": "DEC1439_0_clause_target",
            "decision": "state minimal WEP-slot parent clause as sufficient but unproved",
            "why": "it identifies the exact theorem needed to derive C_parent_WEP=0 without smuggling in a claim",
            "consequence": "next proof work can attack named premises instead of vague coupling language",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": branch,
            "decision_id": "DEC1439_1_parser_ready",
            "decision": "source-pack parser dry-run is ready and refuses all missing official files",
            "why": "if derivation fails, empirical WEP scoring requires exact same-basis files and columns",
            "consequence": "next work can either prove/demote the clause or start official-file acquisition without changing gates",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1439_0_1440",
            "next_target": "1440-Y5-R10-RAB-minimal-WEP-parent-clause-proof-obligations-or-closure-demotion.md",
            "script": "scripts/Y5_R10_RAB_minimal_WEP_parent_clause_proof_obligations_or_closure_demotion.py",
            "objective": "try to prove the minimal WEP parent clause from existing parent-action/quotient machinery; if it cannot be derived, demote it to explicit closure and keep the source-pack route as the only scoring path.",
            "include": "premise-by-premise proof attempt; countermodel pressure; closure demotion test; no-claim gate",
            "exclude": "numeric WEP score; local-GR claim; source-pack target-file fabrication; formalization edits; GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def write_branch_files(minimal_clause: list[dict[str, Any]], parser_rows: list[dict[str, Any]]) -> None:
    write_csv(BRANCH_MINIMAL_PARENT_CLAUSE, minimal_clause)
    write_csv(BRANCH_SOURCE_PACK_PARSER_DRYRUN, parser_rows)


def validation_rows(
    sources: list[dict[str, Any]],
    minimal_clause: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    parser_rows: list[dict[str, Any]],
    column_audit: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    csvs = [
        SOURCE_REGISTER,
        MINIMAL_PARENT_CLAUSE,
        COUNTERMODEL_LEDGER,
        SOURCE_PACK_PARSER_DRYRUN,
        REQUIRED_COLUMN_AUDIT,
        CLAIM_GATE,
        DECISION_LEDGER,
        NEXT_TARGET,
        BRANCH_MINIMAL_PARENT_CLAUSE,
        BRANCH_SOURCE_PACK_PARSER_DRYRUN,
    ]
    parse_ok = True
    parse_errors: list[str] = []
    truthy_claim_flags: list[str] = []
    for path in csvs:
        try:
            parsed_rows = read_csv(path)
        except Exception as exc:
            parse_ok = False
            parse_errors.append(f"{path.name}:{type(exc).__name__}")
            continue
        for index, row in enumerate(parsed_rows, start=2):
            for key in ("claim_allowed", "valid_for_claim", "valid_prediction_row"):
                if (row.get(key) or "").strip().lower() == "true":
                    truthy_claim_flags.append(f"{path.name}:{index}:{key}=true")
    sources_ok = all(row["path_exists"] and row["anchor_found"] for row in sources)
    clause_stated_not_adopted = any(row["status"] == "NOT_ADOPTED_NOT_ZERO_CERTIFIED" for row in minimal_clause)
    countermodels_live = len(countermodels) >= 4 and all(row["claim_effect"] == "BLOCKS_DERIVED_ZERO_UNLESS_EXCLUDED_BY_PARENT_ACTION" for row in countermodels)
    parser_refuses_missing = all(row["parser_status"] == "REFUSED_TARGET_FILE_MISSING" for row in parser_rows)
    columns_waiting = all(row["audit_status"] == "WAITING_FOR_TARGET_FILE" for row in column_audit)
    gates_safe = all(row["gate_status"] == "LOCKED_CLAIM_FALSE" for row in gates) and not truthy_claim_flags
    branch_files_ok = BRANCH_MINIMAL_PARENT_CLAUSE.exists() and BRANCH_SOURCE_PACK_PARSER_DRYRUN.exists()
    formalization_count = count_formalization_modified_since_start()
    checks = [
        ("VAL1439_0_source_register", sources_ok, "all 1439 cited source paths and anchors resolve"),
        ("VAL1439_1_clause_not_adopted", clause_stated_not_adopted, "minimal clause is stated but not adopted as proof"),
        ("VAL1439_2_countermodels_live", countermodels_live, "countermodels remain visible and block automatic zero"),
        ("VAL1439_3_parser_refuses_missing", parser_refuses_missing, "source-pack parser refuses all missing target files"),
        ("VAL1439_4_columns_waiting", columns_waiting, "required-column audit waits for target files"),
        ("VAL1439_5_claim_gates", gates_safe, "all claim/valid/prediction flags remain false"),
        ("VAL1439_6_csv_parse", parse_ok, "all generated 1439 CSVs parse cleanly" if parse_ok else ";".join(parse_errors)),
        ("VAL1439_7_branch_files", branch_files_ok, "branch-locked minimal clause and parser dry-run written"),
        ("VAL1439_8_formalization_untouched", formalization_count == 0, f"formalization modified-file count since start={formalization_count}"),
        ("VAL1439_9_next_target", True, "1440 handoff written"),
    ]
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "generated_utc": stamp(),
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1439_10_overall",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1439 states the minimal WEP parent clause as unproved and dry-runs the source-pack parser without claims",
            "generated_utc": stamp(),
        }
    )
    return rows


def write_doc(sections: dict[str, list[dict[str, Any]]]) -> None:
    content = "\n\n".join(
        [
            "# 1439 - Minimal WEP-slot parent clause or source-pack parser dry-run",
            "**Current verdict:** the minimal clause that would force `C_parent_WEP=0` is now stated, but it is not derived or adopted. The source-pack parser also works as a dry-run and refuses every missing official target file.",
            "**Main progress:** the WEP coupling bottleneck has split into named proof obligations and a concrete parser contract. That means the next step can attack derivation honestly, while the empirical route remains executable but nonclaim.",
            "## Source register\n" + md_table(sections["sources"]),
            "## Minimal parent clause\n" + md_table(sections["minimal_clause"]),
            "## Countermodel ledger\n" + md_table(sections["countermodels"]),
            "## Source-pack parser dry-run\n" + md_table(sections["parser_rows"]),
            "## Required-column audit\n" + md_table(sections["column_audit"]),
            "## Claim gates\n" + md_table(sections["gates"]),
            "## Decision ledger\n" + md_table(sections["decisions"]),
            "## Validation\n" + md_table(sections["validation"]),
            "## Next target\n" + md_table(sections["next"]),
        ]
    )
    DOC.write_text(content + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    COEFFICIENT_ROOT.mkdir(parents=True, exist_ok=True)
    RESIDUAL_ROOT.mkdir(parents=True, exist_ok=True)
    branch = branch_id()
    manifest_rows = read_csv(SOURCE_PACK_MANIFEST_1438)
    sources = source_register_rows(branch)
    minimal_clause = minimal_parent_clause_rows(branch)
    countermodels = countermodel_rows(branch)
    parser_rows = parser_dryrun_rows(branch, manifest_rows)
    column_audit = required_column_audit_rows(branch, manifest_rows)
    gates = claim_gate_rows(branch)
    decisions = decision_rows(branch)
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(MINIMAL_PARENT_CLAUSE, minimal_clause)
    write_csv(COUNTERMODEL_LEDGER, countermodels)
    write_csv(SOURCE_PACK_PARSER_DRYRUN, parser_rows)
    write_csv(REQUIRED_COLUMN_AUDIT, column_audit)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_rows)
    write_branch_files(minimal_clause, parser_rows)

    validation = validation_rows(sources, minimal_clause, countermodels, parser_rows, column_audit, gates)
    write_csv(VALIDATION, validation)
    write_doc(
        {
            "sources": sources,
            "minimal_clause": minimal_clause,
            "countermodels": countermodels,
            "parser_rows": parser_rows,
            "column_audit": column_audit,
            "gates": gates,
            "decisions": decisions,
            "validation": validation,
            "next": next_rows,
        }
    )
    remove_pycache()
    print("Y5_R10_1439_minimal_WEP_clause_unproved_parser_refuses_missing_targets_nonclaim")


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_BRANCH = ROOT / "source-intake" / "microscope" / "branch_locked_wep"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1428-Y5-R10-RAB-branch-classifier-first-row-or-closure-adoption-consequence-ledger.md"
BRANCH_ID_FILE = MICROSCOPE_BRANCH / "branch_id.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1428_SOURCE_REGISTER.csv"
BRANCH_CLASSIFIER_ROW = OUT / "P8_Y5_R10_1428_BRANCH_CLASSIFIER_ROW.csv"
BRANCH_ID_FILE_AUDIT = OUT / "P8_Y5_R10_1428_BRANCH_ID_FILE_AUDIT.csv"
BRANCH_CONSISTENCY_RULES = OUT / "P8_Y5_R10_1428_BRANCH_CONSISTENCY_RULES.csv"
CLOSURE_CONSEQUENCE_LEDGER = OUT / "P8_Y5_R10_1428_CLOSURE_ADOPTION_CONSEQUENCE_LEDGER.csv"
RUNNER_REFUSAL = OUT / "P8_Y5_R10_1428_RUNNER_REFUSAL_STATUS.csv"
CLAIM_GATE = OUT / "P8_Y5_R10_1428_CLAIM_GATE.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1428_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1428_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1428_VALIDATION.csv"


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


def source_register_rows() -> list[dict[str, Any]]:
    schema_1336_doc = ROOT / "1336-Y5-R10-RAB-official-MICROSCOPE-readout-source-manifest-or-common-mode-pivot.md"
    specs = [
        ("SRC1428_0_1427_next", OUT / "P8_Y5_R10_1427_NEXT_TARGET.csv", "NEXT1427_0_1428", "1427 handoff selecting branch classifier or closure consequence ledger."),
        ("SRC1428_1_1427_validation", OUT / "P8_Y5_BRR545_1427_VALIDATION.csv", "VAL1427_7_overall", "1427 validation summary."),
        ("SRC1428_2_1427_manifest", OUT / "P8_Y5_R10_1427_BRANCH_LOCKED_WEP_INPUT_MANIFEST.csv", "MAN1427_0_branch_id", "branch_id file was declared as first manifest row."),
        ("SRC1428_3_1427_schema", OUT / "P8_Y5_R10_1427_BRANCH_LOCKED_WEP_SCHEMA.csv", "SCHEMA1427_0_branch_lock", "same-branch rule for future finite-WEP inputs."),
        ("SRC1428_4_1427_signature", OUT / "P8_Y5_R10_1427_PARENT_ACTION_SIGNATURE_CANDIDATE.csv", "SIG1427_4_verdict", "parent signature remains non-adopted."),
        ("SRC1428_5_1427_runner", OUT / "P8_Y5_R10_1427_RUNNER_REFUSAL_STATUS.csv", "RUN1427_1_branch_manifest", "runner remains waiting for source inputs."),
        ("SRC1428_6_1336_branch_schema_doc", schema_1336_doc, "BRANCHSCHEMA1336_0_same_parent_branch_id", "official branch-classifier schema anchor."),
        ("SRC1428_7_1336_product_schema_doc", schema_1336_doc, "PRODSCHEMA1336_6_branch_lock", "product convention must carry the same branch lock."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, anchor, role in specs:
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "path_exists": path.exists(),
                "anchor": anchor,
                "anchor_found": text_has(path, anchor),
                "role": role,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def branch_classifier_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428",
            "forbidden_mixing_rule": "refuse any finite-WEP product unless branch_id, C_parent, epsilon_e, dd_alpha_surface, R_source, R_material, K_CMSM, eta_product_convention, and measured_G_guard all declare this exact same_parent_branch_id; refuse surrogate, DD-only, tau=1, or measured-G-absorbed rows as claim inputs",
            "signature_option": "parent_action_signature_not_adopted__finite_source_manifest_route",
            "source_basis": "MTS parent coefficient/source basis pending; no DD-as-MTS substitution; no unit source proxy",
            "readout_basis": "official_or_reproducible_MICROSCOPE_CMSM_readout_pending; no surrogate readout promotion",
            "material_basis": "TA6V_minus_PtRh10 response tensor pending; no one-component electron shortcut",
            "product_basis": "eta product convention pending; tau_eff must be sourced and branch-locked",
            "branch_status": "BRANCH_LOCK_CREATED_INPUTS_PENDING",
            "source_path": str(DOC),
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def write_branch_id_file(rows: list[dict[str, Any]]) -> None:
    write_csv(BRANCH_ID_FILE, rows)


def branch_id_audit_rows(branch_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    parsed = read_csv(BRANCH_ID_FILE) if BRANCH_ID_FILE.exists() else []
    required_fields = [
        "same_parent_branch_id",
        "forbidden_mixing_rule",
        "signature_option",
        "source_basis",
        "readout_basis",
    ]
    fieldnames = set(parsed[0].keys()) if parsed else set()
    branch_id = parsed[0].get("same_parent_branch_id", "") if parsed else ""
    rows = [
        {
            "audit_id": "BIDA1428_0_file_exists",
            "target_path": str(BRANCH_ID_FILE),
            "result": "PASS" if BRANCH_ID_FILE.exists() else "FAIL",
            "detail": "branch_id.csv exists",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "BIDA1428_1_required_fields",
            "target_path": str(BRANCH_ID_FILE),
            "result": "PASS" if all(field in fieldnames for field in required_fields) else "FAIL",
            "detail": ";".join(required_fields),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "BIDA1428_2_single_row",
            "target_path": str(BRANCH_ID_FILE),
            "result": "PASS" if len(parsed) == 1 else "FAIL",
            "detail": f"row_count={len(parsed)}",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "BIDA1428_3_branch_id_nonempty",
            "target_path": str(BRANCH_ID_FILE),
            "result": "PASS" if bool(branch_id) and branch_id == branch_rows[0]["same_parent_branch_id"] else "FAIL",
            "detail": branch_id or "MISSING_BRANCH_ID",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return rows


def branch_consistency_rule_rows(branch_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    branch_id = branch_rows[0]["same_parent_branch_id"]
    return [
        {
            "rule_id": "BCR1428_0_same_id_required",
            "object": "same_parent_branch_id",
            "rule": f"future WEP source rows must carry {branch_id} exactly or be refused",
            "failure_status": "BRANCH_MISMATCH_REFUSE_SCORE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "BCR1428_1_no_tau_one_shortcut",
            "object": "tau_eff",
            "rule": "tau_eff must be sourced from product/readout/source projection; tau_eff=1 as a convenience shortcut is invalid",
            "failure_status": "TAU_SHORTCUT_REFUSE_SCORE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "BCR1428_2_no_DD_ontology_swap",
            "object": "DD comparator coefficients",
            "rule": "DD alpha-surface rows may be comparator/proxy rows only unless an MTS parent-to-DD map is sourced and signed",
            "failure_status": "DD_AS_MTS_REFUSE_CLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "BCR1428_3_no_measured_G_absorption",
            "object": "measured-G guard",
            "rule": "common-mode calibration may not absorb a relative Ti/Pt signal or erase an active-source residual",
            "failure_status": "MEASURED_G_ABSORPTION_REFUSE_CLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "BCR1428_4_no_surrogate_readout_promotion",
            "object": "MICROSCOPE/CMSM readout",
            "rule": "surrogate readout arrays can test schema only; official or reproducible mission-design readout is required for claim rows",
            "failure_status": "SURROGATE_READOUT_REFUSE_CLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def closure_consequence_rows() -> list[dict[str, Any]]:
    return [
        {
            "consequence_id": "CLOS1428_0_if_adopted",
            "closure_move": "adopt parent action signature as explicit closure",
            "would_gain": "common-mode WEP zero route becomes clean because active source-only prefactors are excluded by construction",
            "would_cost": "must label the result as closure/axiom until a parent admissibility theorem derives it",
            "current_status": "AVAILABLE_NOT_ADOPTED",
            "adopted_as_derivation": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "consequence_id": "CLOS1428_1_public_language",
            "closure_move": "use closure language honestly if adopted later",
            "would_gain": "a compact theory spine suitable for empirical stress tests",
            "would_cost": "cannot say local GR/WEP was derived solely from earlier primitives",
            "current_status": "LEDGER_ONLY",
            "adopted_as_derivation": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "consequence_id": "CLOS1428_2_current_route",
            "closure_move": "do not adopt closure in 1428",
            "would_gain": "keeps derivation-first discipline and avoids smuggling the answer",
            "would_cost": "finite WEP path needs real branch-locked coefficient/source/readout inputs",
            "current_status": "NOT_ADOPTED_BRANCH_MANIFEST_SELECTED",
            "adopted_as_derivation": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def runner_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN1428_0_branch_classifier",
            "target": "branch-locked finite WEP product",
            "input_status": "BRANCH_ID_READY_OTHER_INPUTS_MISSING",
            "runner_status": "REFUSE_SCORE_UNTIL_REQUIRED_INPUTS_POPULATED",
            "score_ready": False,
            "reason": "branch_id.csv exists, but C_parent/R_source/R_material/K_CMSM/product convention/measured-G guard rows are still missing",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RUN1428_1_closure_signature",
            "target": "parent action signature common-mode route",
            "input_status": "CLOSURE_AVAILABLE_NOT_ADOPTED_NOT_DERIVED",
            "runner_status": "REFUSED_AS_DERIVATION",
            "score_ready": False,
            "reason": "closure consequence ledger is written but not adopted as theorem or axiom",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG1428_0_branch_id",
            "claim_component": "same-branch finite WEP manifest",
            "gate_pass": True,
            "claim_allowed": False,
            "reason": "branch classifier row exists as a guard, not as physics evidence",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1428_1_finite_WEP_score",
            "claim_component": "finite Ti/Pt WEP prediction",
            "gate_pass": False,
            "claim_allowed": False,
            "reason": "C_parent/R_source/R_material/K_CMSM/product convention/measured-G guard are missing",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1428_2_parent_signature",
            "claim_component": "closure forbids active source prefactors",
            "gate_pass": False,
            "claim_allowed": False,
            "reason": "closure ledger is not adoption and not derivation",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1428_3_local_GR",
            "claim_component": "local-GR/Newton reduction",
            "gate_pass": False,
            "claim_allowed": False,
            "reason": "branch lock prevents sloppy WEP assembly but does not prove local GR",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1428_0_branch_first",
            "decision": "populate branch_id.csv first",
            "because": "this is the least speculative row and it prevents incompatible future WEP inputs being multiplied together",
            "effect": "finite WEP path now has a concrete same_parent_branch_id guard",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1428_1_closure_not_adopted",
            "decision": "write closure consequences but do not adopt closure",
            "because": "the user asked for derivable physics where possible, and 1427 did not prove the parent signature",
            "effect": "closure remains an honest fallback rather than hidden scaffolding",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1428_2_next",
            "decision": "next fill product convention and measured-G guard before numeric coefficient scoring",
            "because": "these are rule/guard rows that prevent later shortcuts before importing heavier data",
            "effect": "1429 should lock eta formula, tau_eff status, and common-mode/relative calibration guard",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1428_0_1429",
            "next_target": "1429-Y5-R10-RAB-product-convention-and-measured-G-guard-first-rows.md",
            "script": "scripts/Y5_R10_RAB_product_convention_and_measured_G_guard_first_rows.py",
            "objective": "populate branch-locked product-convention and measured-G guard rows, still nonclaim, before any finite WEP score runner is allowed.",
            "include": "eta formula; tau_eff definition status; orbit-average rule placeholder; allowed common-mode calibration; forbidden relative absorption; branch-id matching audit",
            "exclude": "numeric WEP score; tau=1; source proxy; DD-as-MTS ontology; official-data claim; formalization edits; GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
    branch_audit: list[dict[str, Any]],
    closure_rows: list[dict[str, Any]],
    claims: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    csvs = [
        SOURCE_REGISTER,
        BRANCH_CLASSIFIER_ROW,
        BRANCH_ID_FILE_AUDIT,
        BRANCH_CONSISTENCY_RULES,
        CLOSURE_CONSEQUENCE_LEDGER,
        RUNNER_REFUSAL,
        CLAIM_GATE,
        DECISION_LEDGER,
        NEXT_TARGET,
        BRANCH_ID_FILE,
    ]
    parse_ok = True
    parse_errors: list[str] = []
    truthy_claim_flags: list[str] = []
    for path in csvs:
        try:
            rows = read_csv(path)
        except Exception as exc:
            parse_ok = False
            parse_errors.append(f"{path.name}:{type(exc).__name__}")
            continue
        for index, row in enumerate(rows, start=2):
            for key in ("claim_allowed", "valid_for_claim", "valid_prediction_row", "adopted_as_derivation"):
                if (row.get(key) or "").strip().lower() == "true":
                    truthy_claim_flags.append(f"{path.name}:{index}:{key}=true")
    branch_id = branch_rows[0]["same_parent_branch_id"]
    branch_file_rows = read_csv(BRANCH_ID_FILE) if BRANCH_ID_FILE.exists() else []
    branch_file_ok = (
        len(branch_file_rows) == 1
        and branch_file_rows[0].get("same_parent_branch_id") == branch_id
        and all(row["result"] == "PASS" for row in branch_audit)
    )
    closure_not_adopted = all(str(row.get("adopted_as_derivation")).lower() == "false" for row in closure_rows)
    claims_safe = all(str(row.get("claim_allowed")).lower() == "false" for row in claims) and not truthy_claim_flags
    formalization_count = count_formalization_modified_since_start()
    checks = [
        ("VAL1428_0_sources", all(row["path_exists"] and row["anchor_found"] for row in sources), "all 1428 cited source paths and anchors resolve"),
        ("VAL1428_1_branch_file", branch_file_ok, f"branch_id.csv carries {branch_id} and required fields"),
        ("VAL1428_2_closure_not_adopted", closure_not_adopted, "closure consequence ledger is not adoption or derivation"),
        ("VAL1428_3_claim_gates", claims_safe, "all claim/valid/adopted flags remain false"),
        ("VAL1428_4_csv_parse", parse_ok, "all generated 1428 CSVs parse cleanly" if parse_ok else ";".join(parse_errors)),
        ("VAL1428_5_formalization_untouched", formalization_count == 0, f"formalization modified-file count since start={formalization_count}"),
        ("VAL1428_6_next_target", True, "1429 handoff written"),
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
            "check_id": "VAL1428_7_overall",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1428 creates the first branch-classifier row and logs closure consequences without adopting a claim",
            "generated_utc": stamp(),
        }
    )
    return rows


def write_doc(sections: dict[str, list[dict[str, Any]]]) -> None:
    content = "\n\n".join(
        [
            "# 1428 - Branch classifier first row or closure-adoption consequence ledger",
            "**Current verdict:** 1428 creates the first `branch_id.csv` row for the finite WEP route, but it remains a guardrail only. It does not prove WEP, local GR, or the parent action signature.",
            "**Main progress:** the branch-locked WEP path now has a concrete `same_parent_branch_id`, explicit no-mixing rules, and a closure consequence ledger that keeps the parent-signature shortcut visible but unadopted.",
            "## Source register\n" + md_table(sections["sources"]),
            "## Branch classifier row\n" + md_table(sections["branch"]),
            "## Branch id file audit\n" + md_table(sections["branch_audit"]),
            "## Branch consistency rules\n" + md_table(sections["rules"]),
            "## Closure adoption consequence ledger\n" + md_table(sections["closure"]),
            "## Runner refusal status\n" + md_table(sections["runner"]),
            "## Claim gates\n" + md_table(sections["claims"]),
            "## Decision ledger\n" + md_table(sections["decisions"]),
            "## Validation\n" + md_table(sections["validation"]),
            "## Next target\n" + md_table(sections["next"]),
        ]
    )
    DOC.write_text(content + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_BRANCH.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    branch = branch_classifier_rows()
    write_branch_id_file(branch)
    branch_audit = branch_id_audit_rows(branch)
    rules = branch_consistency_rule_rows(branch)
    closure = closure_consequence_rows()
    runner = runner_refusal_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(BRANCH_CLASSIFIER_ROW, branch)
    write_csv(BRANCH_ID_FILE_AUDIT, branch_audit)
    write_csv(BRANCH_CONSISTENCY_RULES, rules)
    write_csv(CLOSURE_CONSEQUENCE_LEDGER, closure)
    write_csv(RUNNER_REFUSAL, runner)
    write_csv(CLAIM_GATE, claims)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_rows)

    validation = validation_rows(sources, branch, branch_audit, closure, claims)
    write_csv(VALIDATION, validation)
    write_doc(
        {
            "sources": sources,
            "branch": branch,
            "branch_audit": branch_audit,
            "rules": rules,
            "closure": closure,
            "runner": runner,
            "claims": claims,
            "decisions": decisions,
            "validation": validation,
            "next": next_rows,
        }
    )
    remove_pycache()
    print("Y5_R10_1428_branch_classifier_first_row_written_closure_not_adopted_nonclaim")


if __name__ == "__main__":
    main()

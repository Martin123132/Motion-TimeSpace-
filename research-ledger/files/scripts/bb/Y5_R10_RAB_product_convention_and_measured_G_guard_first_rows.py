from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
BRANCH_ROOT = ROOT / "source-intake" / "microscope" / "branch_locked_wep"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1429-Y5-R10-RAB-product-convention-and-measured-G-guard-first-rows.md"
BRANCH_ID_FILE = BRANCH_ROOT / "branch_id.csv"
PRODUCT_FILE = BRANCH_ROOT / "product" / "eta_product_convention.csv"
GUARD_FILE = BRANCH_ROOT / "guards" / "measured_G_guard.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1429_SOURCE_REGISTER.csv"
PRODUCT_CONVENTION_ROW = OUT / "P8_Y5_R10_1429_PRODUCT_CONVENTION_ROW.csv"
MEASURED_G_GUARD_ROW = OUT / "P8_Y5_R10_1429_MEASURED_G_GUARD_ROW.csv"
BRANCH_MATCH_AUDIT = OUT / "P8_Y5_R10_1429_BRANCH_MATCH_AUDIT.csv"
RUNNER_REFUSAL = OUT / "P8_Y5_R10_1429_RUNNER_REFUSAL_STATUS.csv"
CLAIM_GATE = OUT / "P8_Y5_R10_1429_CLAIM_GATE.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1429_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1429_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1429_VALIDATION.csv"


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
        raise ValueError(f"expected exactly one branch_id row, got {len(rows)}")
    value = rows[0].get("same_parent_branch_id", "").strip()
    if not value:
        raise ValueError("same_parent_branch_id is missing")
    return value


def source_register_rows(branch: str) -> list[dict[str, Any]]:
    schema_1336_doc = ROOT / "1336-Y5-R10-RAB-official-MICROSCOPE-readout-source-manifest-or-common-mode-pivot.md"
    specs = [
        ("SRC1429_0_1428_next", OUT / "P8_Y5_R10_1428_NEXT_TARGET.csv", "NEXT1428_0_1429", "1428 handoff selecting product convention and measured-G guard."),
        ("SRC1429_1_1428_validation", OUT / "P8_Y5_BRR545_1428_VALIDATION.csv", "VAL1428_7_overall", "1428 validation summary."),
        ("SRC1429_2_1428_branch_row", OUT / "P8_Y5_R10_1428_BRANCH_CLASSIFIER_ROW.csv", branch, "branch classifier row."),
        ("SRC1429_3_branch_id_file", BRANCH_ID_FILE, branch, "actual branch_id.csv row."),
        ("SRC1429_4_1427_manifest_product", OUT / "P8_Y5_R10_1427_BRANCH_LOCKED_WEP_INPUT_MANIFEST.csv", "MAN1427_7_product_convention", "product convention target file."),
        ("SRC1429_5_1427_manifest_guard", OUT / "P8_Y5_R10_1427_BRANCH_LOCKED_WEP_INPUT_MANIFEST.csv", "MAN1427_8_measured_G_guard", "measured-G guard target file."),
        ("SRC1429_6_1336_product_eta", schema_1336_doc, "PRODSCHEMA1336_0_eta_formula", "product eta formula schema."),
        ("SRC1429_7_1336_branch_lock", schema_1336_doc, "PRODSCHEMA1336_6_branch_lock", "product branch-lock schema."),
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


def product_convention_rows(branch: str) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": branch,
            "eta_formula": "eta_AB = 2(a_A - a_B)/(a_A + a_B); body order and axis sign remain PENDING_OFFICIAL_MICROSCOPE_CONVENTION",
            "sign_convention": "PENDING_OFFICIAL_MICROSCOPE_BODY_ORDER_AND_SENSITIVE_AXIS",
            "tau_eff_definition": "tau_eff = branch_locked_orbit_average(K_CMSM * R_source * readout_mask); tau_eff=1 is forbidden as a shortcut",
            "orbit_average_rule": "PENDING_OFFICIAL_SESSION_MASK_OR_REPRODUCIBLE_CQG_ORBIT_WEIGHTING",
            "units": "dimensionless eta only after C_parent, R_source, R_material, and K_CMSM declare units and conversion factors",
            "source_path": str(DOC),
            "row_status": "PRODUCT_CONVENTION_GUARD_FIRST_ROW_OFFICIAL_DETAILS_PENDING",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def measured_g_guard_rows(branch: str) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": branch,
            "guard_id": "MGG1429_0_no_relative_absorption",
            "allowed_common_mode": "a universal measured-G/common acceleration calibration may rescale the common denominator shared by both test masses",
            "forbidden_relative_absorption": "do not absorb Ti/Pt relative acceleration, active-source residuals, or branch-specific C_parent*R_source*R_material terms into measured G",
            "calibration_equation": "a_A = a_common(G_meas) + delta_a_A; eta_AB = 2(delta_a_A - delta_a_B)/(2*a_common(G_meas) + delta_a_A + delta_a_B); setting delta_a_A-delta_a_B to zero by redefining G is forbidden",
            "source_path": str(DOC),
            "row_status": "MEASURED_G_GUARD_FIRST_ROW_FORMAL_RULE_PENDING_EXTERNAL_CALIBRATION_SOURCE",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def write_manifest_files(product_rows: list[dict[str, Any]], guard_rows: list[dict[str, Any]]) -> None:
    write_csv(PRODUCT_FILE, product_rows)
    write_csv(GUARD_FILE, guard_rows)


def branch_match_audit_rows(branch: str) -> list[dict[str, Any]]:
    targets = [
        ("BMA1429_0_branch_id", BRANCH_ID_FILE),
        ("BMA1429_1_product", PRODUCT_FILE),
        ("BMA1429_2_measured_G_guard", GUARD_FILE),
    ]
    rows: list[dict[str, Any]] = []
    for audit_id, path in targets:
        parsed = read_csv(path) if path.exists() else []
        branch_values = sorted({row.get("same_parent_branch_id", "") for row in parsed})
        rows.append(
            {
                "audit_id": audit_id,
                "target_path": str(path),
                "file_exists": path.exists(),
                "row_count": len(parsed),
                "branch_values": ";".join(branch_values),
                "result": "PASS" if path.exists() and len(parsed) == 1 and branch_values == [branch] else "FAIL",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def runner_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN1429_0_guard_rows",
            "target": "branch-locked finite WEP product",
            "input_status": "BRANCH_PRODUCT_AND_G_GUARDS_READY_OTHER_INPUTS_MISSING",
            "runner_status": "REFUSE_SCORE_UNTIL_C_PARENT_SOURCE_MATERIAL_READOUT_POPULATED",
            "score_ready": False,
            "reason": "product convention and measured-G guard exist, but C_parent, R_source, R_material, K_CMSM, and tau_eff source remain missing",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RUN1429_1_tau_eff",
            "target": "tau_eff projection",
            "input_status": "FORMULA_DECLARED_SOURCE_PENDING",
            "runner_status": "REFUSE_TAU_ONE_SHORTCUT",
            "score_ready": False,
            "reason": "tau_eff must be computed from branch-locked readout/source/orbit data, not set to unity",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG1429_0_product_convention",
            "claim_component": "eta product convention",
            "gate_pass": True,
            "claim_allowed": False,
            "reason": "guard row exists, but official sign/body/order and tau_eff data are pending",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1429_1_measured_G_guard",
            "claim_component": "measured-G non-absorption guard",
            "gate_pass": True,
            "claim_allowed": False,
            "reason": "formal guard exists, but external calibration/provenance is pending",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1429_2_finite_WEP_score",
            "claim_component": "finite Ti/Pt WEP prediction",
            "gate_pass": False,
            "claim_allowed": False,
            "reason": "C_parent/R_source/R_material/K_CMSM/tau_eff source rows are still missing",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1429_3_local_GR",
            "claim_component": "local-GR/Newton reduction",
            "gate_pass": False,
            "claim_allowed": False,
            "reason": "guard rows prevent shortcuts but do not derive local GR",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1429_0_product_first",
            "decision": "write product convention before numeric scoring",
            "because": "eta sign, tau_eff, and orbit averaging decide what any WEP product means",
            "effect": "future finite-WEP runner must refuse tau=1 and branch-mismatched product rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1429_1_measured_G_guard",
            "decision": "write measured-G guard before source coefficients",
            "because": "otherwise a relative residual can be hidden in a common-mode calibration",
            "effect": "future scorepack must keep common-mode and differential signals separate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1429_2_next",
            "decision": "hunt the C_parent coupling signature next",
            "because": "the coupling vector is the actual physics bottleneck once branch/product/guard rules exist",
            "effect": "1430 should try to derive/source C_parent or formally keep the finite WEP score blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1429_0_1430",
            "next_target": "1430-Y5-R10-RAB-C-parent-coupling-source-signature-or-refusal-ledger.md",
            "script": "scripts/Y5_R10_RAB_C_parent_coupling_source_signature_or_refusal_ledger.py",
            "objective": "try to derive or source the branch-locked C_parent coupling vector; if unsigned, keep the finite WEP runner explicitly blocked.",
            "include": "C_parent components; units/sign basis; parent-status; source path; branch-id match; refusal if coupling remains placeholder",
            "exclude": "numeric WEP claim; DD-as-MTS ontology; source proxy; measured-G absorption; local-GR claim; formalization edits; GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    branch_audit: list[dict[str, Any]],
    product_rows: list[dict[str, Any]],
    guard_rows: list[dict[str, Any]],
    claims: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    csvs = [
        SOURCE_REGISTER,
        PRODUCT_CONVENTION_ROW,
        MEASURED_G_GUARD_ROW,
        BRANCH_MATCH_AUDIT,
        RUNNER_REFUSAL,
        CLAIM_GATE,
        DECISION_LEDGER,
        NEXT_TARGET,
        PRODUCT_FILE,
        GUARD_FILE,
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
    product_has_tau_refusal = "tau_eff=1 is forbidden" in product_rows[0]["tau_eff_definition"]
    guard_has_relative_refusal = "do not absorb Ti/Pt relative acceleration" in guard_rows[0]["forbidden_relative_absorption"]
    branch_match_ok = all(row["result"] == "PASS" for row in branch_audit)
    claims_safe = all(str(row.get("claim_allowed")).lower() == "false" for row in claims) and not truthy_claim_flags
    formalization_count = count_formalization_modified_since_start()
    checks = [
        ("VAL1429_0_sources", all(row["path_exists"] and row["anchor_found"] for row in sources), "all 1429 cited source paths and anchors resolve"),
        ("VAL1429_1_branch_match", branch_match_ok, "branch_id, product convention, and measured-G guard share one branch id"),
        ("VAL1429_2_tau_shortcut_blocked", product_has_tau_refusal, "product row refuses tau_eff=1 shortcut"),
        ("VAL1429_3_measured_G_absorption_blocked", guard_has_relative_refusal, "guard row refuses relative-signal absorption into measured G"),
        ("VAL1429_4_claim_gates", claims_safe, "all claim/valid/adopted flags remain false"),
        ("VAL1429_5_csv_parse", parse_ok, "all generated 1429 CSVs parse cleanly" if parse_ok else ";".join(parse_errors)),
        ("VAL1429_6_formalization_untouched", formalization_count == 0, f"formalization modified-file count since start={formalization_count}"),
        ("VAL1429_7_next_target", True, "1430 handoff written"),
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
            "check_id": "VAL1429_8_overall",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1429 writes branch-locked product and measured-G guard rows while keeping finite WEP and local-GR claims blocked",
            "generated_utc": stamp(),
        }
    )
    return rows


def write_doc(sections: dict[str, list[dict[str, Any]]]) -> None:
    content = "\n\n".join(
        [
            "# 1429 - Product convention and measured-G guard first rows",
            "**Current verdict:** 1429 fills two guard rows in the branch-locked WEP manifest: `eta_product_convention.csv` and `measured_G_guard.csv`. They are rule rows, not evidence rows.",
            "**Main progress:** future finite-WEP scoring now has to respect a declared eta formula status, tau-eff source requirement, orbit-average placeholder, branch-id match, and no relative-signal absorption into measured G.",
            "## Source register\n" + md_table(sections["sources"]),
            "## Product convention row\n" + md_table(sections["product"]),
            "## Measured-G guard row\n" + md_table(sections["guard"]),
            "## Branch match audit\n" + md_table(sections["branch_audit"]),
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
    branch = branch_id()
    sources = source_register_rows(branch)
    product = product_convention_rows(branch)
    guard = measured_g_guard_rows(branch)
    write_manifest_files(product, guard)
    branch_audit = branch_match_audit_rows(branch)
    runner = runner_refusal_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(PRODUCT_CONVENTION_ROW, product)
    write_csv(MEASURED_G_GUARD_ROW, guard)
    write_csv(BRANCH_MATCH_AUDIT, branch_audit)
    write_csv(RUNNER_REFUSAL, runner)
    write_csv(CLAIM_GATE, claims)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_rows)

    validation = validation_rows(sources, branch_audit, product, guard, claims)
    write_csv(VALIDATION, validation)
    write_doc(
        {
            "sources": sources,
            "product": product,
            "guard": guard,
            "branch_audit": branch_audit,
            "runner": runner,
            "claims": claims,
            "decisions": decisions,
            "validation": validation,
            "next": next_rows,
        }
    )
    remove_pycache()
    print("Y5_R10_1429_product_convention_and_measured_G_guard_written_nonclaim")


if __name__ == "__main__":
    main()

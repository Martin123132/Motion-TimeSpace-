from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2955"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2955-Y5-R2FR-JX-Phi-source-zero-proof-or-first-residual-coefficient-row-under-AX1090.md"

SRC_2954_DOC = ROOT / "2954-Y5-R2FR-field-space-normalization-beta-eigenvalue-or-residual-coefficient-intake-under-AX1090.md"
SRC_2954_NEXT = RESIDUALS / "P8_Y5_R2FR_2954_NEXT_TARGET.csv"
SRC_2954_INTAKE = RESIDUALS / "P8_Y5_R2FR_2954_RESIDUAL_COEFFICIENT_INTAKE_ROWS.csv"
SRC_1042_SOURCE_ZERO = RESIDUALS / "P8_Y5_R10_1042_SOURCE_ZERO_CLAUSE_AUDIT.csv"
SRC_1042_BOUNDARY = RESIDUALS / "P8_Y5_R10_1042_BOUNDARY_FLUX_PRIOR_FIRST_FILL.csv"
SRC_564_SOURCE_ZERO = RESIDUALS / "P8_Y5_R10_564_SOURCE_ZERO_THEOREM_ATTEMPT.csv"
SRC_2673_JX = RESIDUALS / "P8_Y5_R2FR_JX_QBARXT_2673_SOURCE_ZERO_AUDIT.csv"
SRC_1027_QZ = RESIDUALS / "P8_Y5_R10_1027_SOURCE_ZERO_PROOF_AUDIT.csv"
SRC_2879_ZERO = RESIDUALS / "P8_Y5_R2FR_2879_SOURCE_ZERO_THEOREM_AUDIT.csv"
SRC_2753_JEFF = RESIDUALS / "P8_Y5_R2FR_2753_JEFF_SOURCE_ZERO_THEOREM_ATTEMPT.csv"
SRC_2248_JR = RESIDUALS / "P8_Y5_PARENT_QLOC_2248_JR_SOURCE_ZERO_DECOMPOSITION.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2955_SOURCE_REGISTER.csv",
    "channels": RESIDUALS / "P8_Y5_R2FR_2955_JX_PHI_SOURCE_ZERO_CHANNEL_AUDIT.csv",
    "join": RESIDUALS / "P8_Y5_R2FR_2955_RHS_ZERO_JOIN_GATE.csv",
    "first_row": RESIDUALS / "P8_Y5_R2FR_2955_FIRST_RESIDUAL_COEFFICIENT_ROW.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2955_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2955_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2955_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2955_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2955_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "channels_copy": PARENT_ACTION / "JX_Phi_source_zero_channel_audit_2955_NOT_DERIVED.csv",
    "first_row_copy": LOCAL_BOUNDS / "first_residual_coefficient_row_qbarXT_2955_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2955_MATTER_PULLBACK_NO_MARKER_OR_QBARXT_ROW_NEXT_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv_rows(path)
        return True
    except Exception:
        return False


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": RUN_UTC,
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    selected = columns or list(rows[0].keys())
    header = "| " + " | ".join(selected) + " |"
    separator = "| " + " | ".join("---" for _ in selected) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in selected) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2955_00_2954_doc", SRC_2954_DOC, "NEXT2954_0_2955;Validation overall: `True`", "2954 handoff"),
        ("SRC2955_01_2954_next", SRC_2954_NEXT, "NEXT2954_0_2955", "machine-readable 2955 target"),
        ("SRC2955_02_2954_intake", SRC_2954_INTAKE, "INT2954_9_qbar_XT;INT2954_11_alphaX", "2954 coefficient intake rows"),
        ("SRC2955_03_1042_source_zero", SRC_1042_SOURCE_ZERO, "SZ1042_0_matter_pullback;SZ1042_5_verdict", "physical X source-zero channel audit"),
        ("SRC2955_04_1042_boundary", SRC_1042_BOUNDARY, "PBF1042_0_Phi_boundary_local_definition;PBF1042_2_numeric_prior_route", "Phi boundary prior/source row"),
        ("SRC2955_05_564_source_zero", SRC_564_SOURCE_ZERO, "SZ564_2_matter_pullback_zero;SZ564_5_verdict", "source-zero theorem attempt"),
        ("SRC2955_06_2673_JX", SRC_2673_JX, "JX2673_0_contract;JX2673_7_verdict", "J_X/qbar_XT source-zero audit"),
        ("SRC2955_07_1027_QZ", SRC_1027_QZ, "QZ1027_0_chain_rule;QZ1027_6_verdict", "qbar_XT proof audit"),
        ("SRC2955_08_2879_zero", SRC_2879_ZERO, "ZERO2879_0_JR_matter_silence;ZERO2879_5_joint_source_zero", "later source-zero theorem audit"),
        ("SRC2955_09_2753_Jeff", SRC_2753_JEFF, "JZ2753_0_definition;JZ2753_5_verdict", "J_eff component source audit"),
        ("SRC2955_10_2248_JR", SRC_2248_JR, "JR2248_0_matter;JR2248_6_total_verdict", "J_R component decomposition"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, source_path, anchors, role in specs:
        found, missing = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_type": "local_file",
                    "source_path": str(source_path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": source_path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def channel_rows() -> list[dict[str, Any]]:
    rows = [
        ("CHAN2955_0_chain_rule", "metric/coframe chain rule", "if Dq[v_X]=0 and matter sees only Obs(q), then visible matter pullback vanishes", "CONDITIONAL_MATH_VALID", "q/v/observed coframe parent certificate missing", False, "qbar_XT remains live"),
        ("CHAN2955_1_matter_markers", "ordinary matter constants/material markers", "Lie_vX(theta_A)=0 for constants, masses, clocks, EM constants, material labels and calibration markers", "MISSING_NO_MARKER_THEOREM", "1027/2673 keep markers and constants unsigned", False, "WEP/clock/material qbar_XT rows live"),
        ("CHAN2955_2_hidden_frame", "hidden Weyl/disformal/direct source frame", "any X-sensitive frame/source slot is excluded or source-bounded", "COUNTEREXAMPLE_FILTER_ONLY", "hidden-frame/direct-source rows are classified but not zeroed", False, "hidden qbar_XT and source-tail rows live"),
        ("CHAN2955_3_boundary_phi", "boundary/Phi flux", "Phi_boundary_local=0 or bounded with source path, units and no-cancellation policy", "BOUNDARY_FLUX_ZERO_NOT_DERIVED", "1042 defines Phi but theorem-zero/numeric value is missing", False, "Phi_boundary/alpha3/R10 edge row live"),
        ("CHAN2955_4_projector_domain", "projector/domain selectors", "projector/domain stress or source is topological, first-class, positive source-free, or bounded", "PROJECTOR_DOMAIN_SOURCE_OPEN", "1042/2673 retain projector/domain silence open", False, "preferred-frame and domain-tail rows live"),
        ("CHAN2955_5_memory_history", "memory/history kernel", "compact-local memory/history source is silent, screened, constant universal, or bounded", "MEMORY_SOURCE_OPEN", "1042 and 2753 keep memory/history tails open", False, "Gdot/alpha3/R10 memory tail live"),
        ("CHAN2955_6_source_normalization", "source normalization and PiM", "Pi_M^H source measure is orthogonal to X hair and measured GM uses same charge", "SOURCE_MEASURE_OPEN", "1042/2879 keep source normalization and PiM unresolved", False, "Qbar_XH and M_H_ref rows live"),
        ("CHAN2955_7_total", "J_X + Phi right-hand side", "all channels vanish or are absolutely bounded in one parent normalization ledger", "RHS_ZERO_NOT_DERIVED", "chain-rule math helps, but marker/hidden/boundary/projector/memory/source-normalization channels remain open", False, "finite residual coefficient intake required"),
    ]
    return [
        add_common(
            {
                "channel_id": channel_id,
                "channel": channel,
                "zero_condition": zero_condition,
                "current_status": status,
                "blocker": blocker,
                "theorem_zero_credit": credit,
                "residual_if_open": residual,
            }
        )
        for channel_id, channel, zero_condition, status, blocker, credit, residual in rows
    ]


def join_rows() -> list[dict[str, Any]]:
    rows = [
        ("JOIN2955_0_nohair_rhs", "source-free positive-X no-hair RHS", "J_X=0 and Phi_boundary_local=0 channelwise", "FAILED_CURRENT_CERTIFICATE", False),
        ("JOIN2955_1_matter_part", "ordinary matter pullback", "visible matter chain rule plus no-marker/no-hidden-frame clauses", "PARTIAL_CONDITIONAL_ONLY", False),
        ("JOIN2955_2_tail_part", "boundary/projector/memory/source tails", "all tail channels theorem-zero or bounded absolutely", "FAILED_CURRENT_CERTIFICATE", False),
        ("JOIN2955_3_no_cancellation", "no cancellation policy", "component zeros or absolute bounds, not cancellation between unknowns", "POLICY_RETAINED", True),
        ("JOIN2955_4_verdict", "2955 RHS-zero verdict", "right-hand side zero is not derived; first residual coefficient row must remain nonclaim", "RHS_ZERO_NOT_DERIVED_FIRST_ROW_EMITTED", False),
    ]
    return [
        add_common(
            {
                "join_id": join_id,
                "object": obj,
                "required_condition": required,
                "current_status": status,
                "join_pass": passed,
            }
        )
        for join_id, obj, required, status, passed in rows
    ]


def first_row_rows() -> list[dict[str, Any]]:
    source_path = str(SRC_2673_JX)
    boundary_path = str(SRC_1042_BOUNDARY)
    rows = [
        ("FIRST2955_0_qbar_XT_matter_marker", "qbar_XT", "ordinary matter/test charge under physical X after marker/hidden-frame checks", "dimensionless", source_path, SRC_2673_JX.exists(), "MISSING_NUMERIC_OR_THEOREM_ZERO", "JX2673_3_constants_markers;JX2673_4_hidden_frame", False),
        ("FIRST2955_1_Phi_boundary_local", "Phi_boundary_local", "boundary flux term in positive-X energy identity", "charge_or_flux", boundary_path, SRC_1042_BOUNDARY.exists(), "MISSING_NUMERIC_OR_THEOREM_ZERO", "PBF1042_0_Phi_boundary_local_definition", False),
    ]
    return [
        add_common(
            {
                "row_id": row_id,
                "symbol": symbol,
                "definition": definition,
                "units": units,
                "source_path": path,
                "source_path_exists": exists,
                "numeric_or_theorem_value": value,
                "source_anchor": anchor,
                "source_backed_value": source_backed,
                "accepted_for_scoring": False,
                "no_cancellation_policy": True,
            }
        )
        for row_id, symbol, definition, units, path, exists, value, anchor, source_backed in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2955_0_JX_zero", "J_X=0 channelwise", False, "JX_ZERO_NOT_DERIVED"),
        ("CG2955_1_Phi_zero", "Phi_boundary_local=0", False, "PHI_BOUNDARY_ZERO_NOT_DERIVED"),
        ("CG2955_2_RHS_zero", "positive-X no-hair RHS vanishes", False, "RHS_ZERO_NOT_DERIVED"),
        ("CG2955_3_first_row_score", "first residual coefficient row score-ready", False, "NUMERIC_OR_THEOREM_VALUE_MISSING"),
        ("CG2955_4_nohair", "positive physical-X no-hair closes", False, "NOHAIR_NOT_PARENT_SIGNED"),
        ("CG2955_5_local_GR", "local GR/Newton reduction allowed", False, "NO_LOCAL_GR_CLAIM"),
        ("CG2955_6_public", "public claim allowed", False, "PRIVATE_NONCLAIM_CHECKPOINT"),
    ]
    return [
        add_common(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "condition_passed": passed,
                "status": status,
            }
        )
        for gate_id, claim, passed, status in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2955_0_result", "right-hand-side zero is not derived", "conditional matter chain-rule pieces exist, but marker, hidden-frame, boundary, projector, memory and source-normalization channels remain open", "do not claim positive-X no-hair or local GR"),
        ("DEC2955_1_first_row", "first residual coefficient rows emitted as nonclaim", "qbar_XT and Phi_boundary_local are the first useful coefficient rows with real local source paths and units, but no values", "fill values only from parent theorem-zero or source-backed bound"),
        ("DEC2955_2_next", "next attack should target matter pullback/no-marker theorem or qbar_XT bound", "qbar_XT is the cleanest first source/test coefficient; if it zeroes, WEP/clock/R10 tails shrink", "build 2956 matter no-marker proof or qbar_XT source row"),
        ("DEC2955_3_claim_ceiling", "no local-GR/R10/WEP/PPN/public claim", "RHS zero and first residual row values are missing", "private discipline only"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": action,
            }
        )
        for decision_id, decision, because, action in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2955_0_2956",
                "priority": "selected_primary",
                "next_doc": "2956-Y5-R2FR-matter-pullback-no-marker-theorem-or-qbarXT-bound-row-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_matter_pullback_no_marker_theorem_or_qbarXT_bound_row_under_AX1090_2956.py",
                "objective": "Try to prove qbar_XT=0 by ordinary matter descent: observed coframe/metric depends only on quotient variables, material constants and markers are X-silent, and no hidden Weyl/disformal/direct source slot survives. If this fails, fill a nonclaim qbar_XT bound row with units, source path and no-cancellation policy.",
                "include": "matter pullback;observed coframe;material markers;EM/clocks/masses;hidden Weyl/disformal frame;direct source slot;qbar_XT units;source path;bound row",
                "exclude": "quotient/vertical no-pole rerun;beta prediction;direct lambda closure;alpha(lambda) scoring;I_X scoring;local-GR claim;public claim;formalization-workbench edits;GitHub action",
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = [
        ("channels_copy", OUTPUTS["channels"], BRANCH_OUTPUTS["channels_copy"]),
        ("first_row_copy", OUTPUTS["first_row"], BRANCH_OUTPUTS["first_row_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copies:
        shutil.copyfile(source, target)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source),
                    "copy_path": str(target),
                    "source_exists": source.exists(),
                    "copy_exists": target.exists(),
                }
            )
        )
    return rows


def validation_rows(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = all_rows["sources"]
    generated_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
    csv_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values())
    checks = [
        ("VAL2955_0_sources_exist", all(row["path_exists"] for row in source_rows), "all cited local source paths exist", True),
        ("VAL2955_1_anchors_found", all(row["anchors_found"] for row in source_rows), "all source anchors found", True),
        ("VAL2955_2_channel_verdict_blocked", any(row["channel_id"] == "CHAN2955_7_total" and row["theorem_zero_credit"] is False for row in all_rows["channels"]), "total RHS-zero channel verdict is blocked", True),
        ("VAL2955_3_join_blocked", any(row["join_id"] == "JOIN2955_4_verdict" and row["join_pass"] is False for row in all_rows["join"]), "join verdict is blocked and first row emitted", True),
        ("VAL2955_4_first_rows_nonclaim", all(row["accepted_for_scoring"] is False and row["valid_for_claim"] is False for row in all_rows["first_row"]), "first residual rows remain nonclaim", True),
        ("VAL2955_5_first_rows_have_paths", all(Path(row["source_path"]).exists() for row in all_rows["first_row"]), "first residual rows have existing source paths", True),
        ("VAL2955_6_claims_blocked", all(row["condition_passed"] is False and row["claim_allowed"] is False for row in all_rows["claims"]), "all claim gates are blocked", True),
        ("VAL2955_7_next_target_written", any(row["next_id"] == "NEXT2955_0_2956" for row in all_rows["next"]), "2956 next target selected", True),
        ("VAL2955_8_branches_exist", all(Path(row["copy_path"]).exists() for row in all_rows["branches"]), "branch copy files exist", True),
        ("VAL2955_9_csvs_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV files parse", True),
        ("VAL2955_10_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in generated_paths), "all generated outputs are under post-checkpoint-work", True),
        ("VAL2955_11_formalization_clean", not any(is_under(path, FORMALIZATION) for path in generated_paths), "no 2955 outputs were written to formalization-workbench", True),
    ]
    overall = all(passed == required for _, passed, _, required in checks)
    rows = [
        add_common(
            {
                "validation_id": validation_id,
                "passed": passed,
                "check": check,
                "required": required,
            }
        )
        for validation_id, passed, check, required in checks
    ]
    rows.append(
        add_common(
            {
                "validation_id": "VAL2955_OVERALL",
                "passed": overall,
                "check": "2955 validation overall",
                "required": True,
            }
        )
    )
    return rows


def write_markdown(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2955 - Y5 R2FR: J_X/Phi source-zero proof or first residual coefficient row under AX1090

Status: `Y5_R2FR_2955_rhs_zero_not_derived_first_qbarXT_Phi_rows_emitted_nonclaim`

Claim ceiling: `no_JX_zero_no_Phi_zero_no_RHS_zero_no_nohair_no_first_row_score_no_local_GR_no_Newton_no_R10_no_PPN_no_public_claim`

2955 attacks the right-hand side of the positive-`X` no-hair identity. The result is:

- The visible matter chain-rule theorem exists only conditionally; it still needs parent `q/v_X`, observed coframe, matter functor and no-marker constants.
- The full RHS-zero proof fails because material markers, hidden frames, boundary/Phi, projector/domain, memory/history and source-normalization/PiM channels remain open.
- The first useful nonclaim residual rows are now emitted with real local source paths and units: `qbar_XT` and `Phi_boundary_local`.
- No scoring or local-GR claim is allowed until those rows receive a theorem-zero value or a source-backed numeric bound.

## Source Register

{md_table(all_rows["sources"], ["source_id", "source_path", "path_exists", "anchors_found", "role"])}

## J_X / Phi Source-Zero Channel Audit

{md_table(all_rows["channels"], ["channel_id", "channel", "current_status", "theorem_zero_credit", "residual_if_open"])}

## RHS-Zero Join Gate

{md_table(all_rows["join"], ["join_id", "object", "current_status", "join_pass"])}

## First Residual Coefficient Row

{md_table(all_rows["first_row"], ["row_id", "symbol", "units", "source_path_exists", "numeric_or_theorem_value", "accepted_for_scoring"])}

## Claim Gates

{md_table(all_rows["claims"], ["claim_gate_id", "claim", "condition_passed", "status", "claim_allowed"])}

## Decision Ledger

{md_table(all_rows["decision"], ["decision_id", "decision", "because", "next_action"])}

## Next Target

{md_table(all_rows["next"], ["next_id", "priority", "next_doc", "next_script", "objective", "exclude"])}

## Branch Copies

{md_table(all_rows["branches"], ["copy_id", "source_path", "copy_path", "source_exists", "copy_exists", "valid_for_claim"])}

## Validation

{md_table(all_rows["validation"], ["validation_id", "passed", "check", "required"])}

Validation overall: `{all_rows["validation"][-1]["passed"]}`.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    all_rows: dict[str, list[dict[str, Any]]] = {
        "sources": source_register_rows(),
        "channels": channel_rows(),
        "join": join_rows(),
        "first_row": first_row_rows(),
        "claims": claim_gate_rows(),
        "decision": decision_rows(),
        "next": next_target_rows(),
    }

    for key, path in OUTPUTS.items():
        if key in {"branches", "validation"}:
            continue
        write_csv(path, all_rows[key])

    all_rows["branches"] = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], all_rows["branches"])

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)

    print(f"2955 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()

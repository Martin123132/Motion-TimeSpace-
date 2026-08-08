from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2993"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2993-Y5-R2FR-parent-extra-sector-source-normal-form-pack-or-first-epsilon-Qv-extra-numeric-row-under-AX1090.md"

SRC_2992_DOC = ROOT / "2992-Y5-R2FR-extra-double-zero-and-zero-odd-source-proof-or-epsilon-Qv-extra-bound-under-AX1090.md"
SRC_2992_NEXT = RESIDUALS / "P8_Y5_R2FR_2992_NEXT_TARGET.csv"
SRC_2992_CLAUSE = RESIDUALS / "P8_Y5_R2FR_2992_EXTRA_ZERO_ODD_SOURCE_CLAUSE_AUDIT.csv"
SRC_2992_EPSILON = RESIDUALS / "P8_Y5_R2FR_2992_EPSILON_QV_EXTRA_BOUND_ROWS_NONCLAIM.csv"
SRC_2990_NORMAL = RESIDUALS / "P8_Y5_R2FR_2990_SELECTED_PARENT_NORMAL_FORM_CONTRACT.csv"
SRC_2990_SECTOR = RESIDUALS / "P8_Y5_R2FR_2990_SECTOR_BY_SECTOR_THETA_NORMAL_FORM_CONTRACT.csv"
SRC_MIN_BLOCKS = RESIDUALS / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv"
SRC_2697_DOC = ROOT / "2697-Y5-R2FR-minimal-local-parent-action-fixed-point-ansatz-kappa-source-measure-EH.md"
SRC_2028_DOC = ROOT / "2028-Y5-R2FR-vZ-local-vacuum-double-zero-or-finite-jZB-bound.md"
SRC_2188_DOC = ROOT / "2188-Y5-R2FR-extra-sector-double-zero-and-PiM-lock-signature-or-residual-fill.md"
SRC_2189_DOC = ROOT / "2189-Y5-R2FR-parent-extra-sector-inventory-and-coupling-map-or-leakage-bounds.md"
SRC_2707_DOC = ROOT / "2707-Y5-R2FR-parent-action-coefficient-owner-extraction.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2993_SOURCE_REGISTER.csv",
    "source_pack": RESIDUALS / "P8_Y5_R2FR_2993_PARENT_EXTRA_SOURCE_PACK_AUDIT.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2993_SOURCE_PACK_CLAUSE_GATES.csv",
    "epsilon": RESIDUALS / "P8_Y5_R2FR_2993_FIRST_EPSILON_QV_EXTRA_NUMERIC_ROW_NONCLAIM.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2993_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2993_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2993_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2993_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "source_pack_copy": PARENT_ACTION / "parent_extra_sector_source_normal_form_pack_2993_NOT_SIGNED.csv",
    "epsilon_copy": LOCAL_BOUNDS / "epsilon_Qv_extra_first_numeric_row_2993_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2993_parent_extra_clause_source_or_epsilon_Qv_bound_next_NONCLAIM.csv",
}

for directory in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def anchors(path: Path, needles: list[str]) -> bool:
    haystack = text(path)
    return path.exists() and all(needle in haystack for needle in needles)


def add(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "control_only": True,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "generated_utc": RUN_UTC,
    }


def write_csv(path: Path, out_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in out_rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(out_rows)


def csv_ok(path: Path) -> bool:
    try:
        rows(path)
        return True
    except Exception:
        return False


def under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2993_00_2992_doc", SRC_2992_DOC, ["theorem is retained as a private derivation scaffold", "epsilon_Qv_extra_piece"], "imports 2992 verdict"),
        ("SRC2993_01_2992_next", SRC_2992_NEXT, ["NEXT2992_0_2993", "S_Z, Z0, K_AB"], "imports selected 2993 target"),
        ("SRC2993_02_2992_clause", SRC_2992_CLAUSE, ["ECA2992_0_parent_SZ", "ECA2992_8_total"], "imports missing parent/source clauses"),
        ("SRC2993_03_2992_epsilon", SRC_2992_EPSILON, ["EQE2992_01_parent_action", "EQE2992_11_total"], "imports epsilon_Qv_extra nonclaim rows"),
        ("SRC2993_04_2990_normal", SRC_2990_NORMAL, ["NF2990_3_extra_double_zero", "CONDITIONAL_NOT_SIGNED"], "imports normal-form extra clause"),
        ("SRC2993_05_2990_sector", SRC_2990_SECTOR, ["SNF2990_2_extra", "epsilon_Qv_extra_piece"], "imports sector theta normal-form clause"),
        ("SRC2993_06_min_blocks", SRC_MIN_BLOCKS, ["A511_3_extra_field_silence", "Hessian(V)>0"], "imports minimal action block"),
        ("SRC2993_07_2697_action", SRC_2697_DOC, ["ACT2697_5_extra_sector_silence", "ROUTE_BUILT_NOT_PROMOTED"], "imports fixed-point parent action ansatz"),
        ("SRC2993_08_2028_double_zero", SRC_2028_DOC, ["VDZ2028_7_verdict", "parent S_Z/local branch/source/boundary inputs missing"], "imports canonical S_Z theorem and missing inputs"),
        ("SRC2993_09_2188_double_zero", SRC_2188_DOC, ["DZ2188_7_verdict", "F1_extra_linear_leakage_norm"], "imports extra-sector double-zero leakage precedent"),
        ("SRC2993_10_2189_inventory", SRC_2189_DOC, ["EI2189_0_GK", "EI2189_1_response_memory", "LR2189_TOTAL"], "imports operator/coupling inventory"),
        ("SRC2993_11_2707_owner", SRC_2707_DOC, ["OWN2707_6_verdict", "DEMOTE_FINITE_LOCAL_XHAT_BRANCH_TO_CLOSURE_INPUT"], "imports coefficient-owner extraction failure"),
    ]
    return [
        add(
            {
                "source_id": source_id,
                "source_path": str(path),
                "role": role,
                "required_anchors": ";".join(needles),
                "exists": path.exists(),
                "anchors_found": anchors(path, needles),
            }
        )
        for source_id, path, needles, role in specs
    ]


def source_pack_rows() -> list[dict[str, Any]]:
    data = [
        (
            "PES2993_00_parent_action",
            "S_extra/S_Z source path and field list",
            "single parent action density with named extra fields, normalizations and sign conventions",
            "2697/2990 provide an ansatz/contract; 2028 gives a canonical prototype",
            "NOT_PARENT_SOURCED",
            "epsilon_extra_parent_action",
            "supply explicit S_extra line from parent corpus or demote source-pack route to closure",
        ),
        (
            "PES2993_01_branch_value",
            "Z0/Phi0 local branch",
            "constant local fixed point solving E_A=0 in the same variables as S_Z",
            "2028 and 2697 require Z0/Phi0 but do not source values or field map",
            "MISSING_BRANCH_VALUE",
            "epsilon_extra_bulk_C0",
            "source Z0/Phi0 and the local reference convention",
        ),
        (
            "PES2993_02_kinetic_metric",
            "K_AB/G_AB sign and units",
            "positive field-space kinetic metric in the local exterior with declared units",
            "2697/2028 require positivity; 2707 shows finite Xhat owner/units still fail",
            "MISSING_PARENT_SIGN_AND_UNITS",
            "epsilon_extra_positive_gap_hair",
            "extract K_AB/G_AB from parent action or retain positive-gap residual",
        ),
        (
            "PES2993_03_potential_derivatives",
            "V(Z0), partial_A V(Z0), Hessian/mass gap",
            "vacuum subtraction, stationary branch and positive Hessian all in one parent normalization",
            "2028 proves the condition exactly but records parent S_Z/local branch inputs missing",
            "MISSING_V0_VPRIME_HESSIAN",
            "epsilon_extra_bulk_C0;epsilon_extra_positive_gap_hair",
            "source V0, Vprime0 and Hessian/mass-gap rows",
        ),
        (
            "PES2993_04_Ci_Oi_inventory",
            "complete C_i/O_i coupling inventory",
            "all metric/source/readout/projector/memory/PiM/boundary couplings and first derivatives listed",
            "2189 inventories suspects but does not parent-sign all signatures or source equations",
            "PARTIAL_INVENTORY_NOT_SOURCE_PACK",
            "epsilon_extra_bulk_F1",
            "turn the 2189 inventory into a field-specific C_i/dC_i source table",
        ),
        (
            "PES2993_05_no_source_slot",
            "J_Z and exchange-odd source zero",
            "matter/readout/source action has no allowed linear odd source at the local branch",
            "2992 and 2028 keep the zero-odd-source theorem conditional",
            "MISSING_ZERO_ODD_SOURCE",
            "epsilon_extra_zero_odd_source",
            "derive no-source slot or create source-charge bound rows",
        ),
        (
            "PES2993_06_boundary_QZ",
            "Q_Z/theta_extra boundary no-flux",
            "extra symplectic potential/current and Hamiltonian boundary terms vanish or are fixed before readout",
            "2991 closed only exact fixed-boundary pieces; 2992 leaves extra boundary flux open",
            "MISSING_QZ_BOUNDARY_NO_FLUX",
            "epsilon_extra_boundary_flux",
            "source Q_Z/theta_extra boundary term or finite local flux bound",
        ),
        (
            "PES2993_07_metric_readout_lock",
            "Gamma/Khat/q_loc and observed PPN readout lock",
            "protected parent variable equals physical local residual/readout through first order",
            "2189 flags GK/q_loc as highest priority and 2992 leaves metric-response/Helmholtz open",
            "MISSING_GK_READOUT_LOCK",
            "epsilon_GK_metric_response;epsilon_extra_readout_linear",
            "derive GK metric-response Helmholtz/Euler closure or keep q_loc residual",
        ),
        (
            "PES2993_08_memory_response",
            "memory/response component map",
            "memory doublet variables mapped to physical local clock/PPN/orbital readout with no linear source",
            "2189 and 2992 leave the component map and PPN lock candidate-only",
            "MISSING_MEMORY_COMPONENT_MAP",
            "epsilon_memory_response_doublet",
            "source memory component map or bound memory response residual",
        ),
        (
            "PES2993_09_Mref",
            "positive same-frame M_ref",
            "positive denominator in the same local frame for no-cancellation scoring",
            "2992 keeps M_ref missing for epsilon_Qv_extra scoring",
            "MISSING_POSITIVE_SAME_FRAME_MREF",
            "epsilon_extra_Mref",
            "define M_ref from a parent Hamiltonian/source charge or block score-ready rows",
        ),
        (
            "PES2993_10_total",
            "parent extra source-normal-form pack",
            "all clauses PES2993_00 through PES2993_09 close together",
            "no current source closes the whole package in one branch",
            "SOURCE_PACK_NOT_SIGNED",
            "epsilon_Qv_extra_piece_total_abs",
            "do not claim local GR/Newton; attack field-specific source rows next",
        ),
    ]
    return [
        add(
            {
                "pack_id": pack_id,
                "required_input": required_input,
                "success_condition": success_condition,
                "best_current_evidence": evidence,
                "current_status": status,
                "residual_symbol_if_open": residual,
                "next_action": next_action,
                "clause_signed_now": False,
            }
        )
        for pack_id, required_input, success_condition, evidence, status, residual, next_action in data
    ]


def gate_rows() -> list[dict[str, Any]]:
    data = [
        ("GATE2993_0_source_action", "S_extra/S_Z source action and field list parent-signed", False, "NOT_PARENT_SOURCED"),
        ("GATE2993_1_branch", "Z0/Phi0 branch and reference convention sourced", False, "MISSING_BRANCH_VALUE"),
        ("GATE2993_2_positive_gap", "K_AB/G_AB positive and Hessian/mass gap signed", False, "MISSING_SIGNED_POSITIVE_GAP"),
        ("GATE2993_3_couplings", "complete C_i/O_i inventory has C_i0=dC_i0=0 or bounds", False, "PARTIAL_INVENTORY_ONLY"),
        ("GATE2993_4_no_source", "J_Z/B_Z/source slot zero signed", False, "MISSING_ZERO_ODD_SOURCE"),
        ("GATE2993_5_boundary", "Q_Z/theta_extra no-flux signed", False, "MISSING_BOUNDARY_NO_FLUX"),
        ("GATE2993_6_readout", "GK/q_loc/readout/PPN lock signed", False, "MISSING_READOUT_LOCK"),
        ("GATE2993_7_Mref", "positive same-frame M_ref signed", False, "MISSING_MREF"),
        ("GATE2993_8_promote_epsilon_zero", "epsilon_Qv_extra_piece=0 can be promoted", False, "SOURCE_PACK_NOT_SIGNED"),
        ("GATE2993_9_promote_local_GR", "local GR/Newton branch can be promoted from this route", False, "NO_LOCAL_GR_PROMOTION"),
    ]
    return [
        add(
            {
                "gate_id": gate_id,
                "gate": gate,
                "condition_passed": passed,
                "status": status,
                "promotion_allowed_now": False,
            }
        )
        for gate_id, gate, passed, status in data
    ]


def epsilon_rows() -> list[dict[str, Any]]:
    data = [
        {
            "epsilon_id": "EQE2993_00_target",
            "symbol": "epsilon_Qv_extra_piece_total_abs",
            "row_role": "total residual target",
            "definition": "source-ready absolute envelope for extra-sector local theta/current/readout residuals",
            "numeric_value": "MISSING_NUMERIC_UPPER_BOUND",
            "numeric_value_present": False,
            "units": "dimensionless_after_M_ref",
            "source_path": str(OUTPUTS["source_pack"]),
            "source_anchor": "PES2993_10_total",
            "reason_not_numeric": "parent source-normal-form pack not signed",
        },
        {
            "epsilon_id": "EQE2993_01_first_acquisition_row",
            "symbol": "epsilon_extra_parent_action",
            "row_role": "first numeric-row acquisition slot",
            "definition": "guard row for absence of parent S_extra/S_Z source and field-list normalization",
            "numeric_value": "MISSING_NUMERIC_UPPER_BOUND",
            "numeric_value_present": False,
            "units": "boolean_or_action_norm_guard",
            "source_path": str(OUTPUTS["source_pack"]),
            "source_anchor": "PES2993_00_parent_action",
            "reason_not_numeric": "no explicit parent action density, field normalization or M_ref denominator exists",
        },
        {
            "epsilon_id": "EQE2993_02_first_if_parent_found",
            "symbol": "epsilon_extra_bulk_F1",
            "row_role": "next value if S_extra appears",
            "definition": "operator norm of first derivative leakage from C_i/dC_i/readout/source couplings at the local branch",
            "numeric_value": "MISSING_CI_DCI_NUMERIC_VALUES",
            "numeric_value_present": False,
            "units": "dimensionless_operator_norm",
            "source_path": str(OUTPUTS["source_pack"]),
            "source_anchor": "PES2993_04_Ci_Oi_inventory",
            "reason_not_numeric": "C_i/O_i inventory exists only as suspects, not parent-signed coefficients",
        },
    ]
    return [add(row) for row in data]


def decision_rows() -> list[dict[str, Any]]:
    data = [
        (
            "DEC2993_0_source_pack_rejected_for_now",
            "Do not activate the parent extra-sector source pack.",
            "The corpus has a coherent ansatz and conditional theorem, but not a single sourced parent package with S_Z, branch data, coupling inventory, source silence, boundary silence and M_ref.",
            "retain epsilon_Qv_extra_piece_total_abs as a live nonclaim residual",
        ),
        (
            "DEC2993_1_no_fake_numeric_row",
            "Do not fabricate the first epsilon_Qv_extra numeric value.",
            "A numeric row without parent S_extra/S_Z and M_ref would be a false precision move.",
            "stage the exact acquisition row with numeric_value_present=false",
        ),
        (
            "DEC2993_2_next",
            "Next target should source one concrete clause rather than re-prove the generic theorem.",
            "The most valuable leap is to either source the parent S_extra line or take the 2189 GK/q_loc sector and derive its metric-response/source/boundary package.",
            "build 2994 around parent S_extra line hunt versus GK/q_loc source-pack extraction",
        ),
    ]
    return [
        add({"decision_id": decision_id, "decision": decision, "because": because, "next_action": next_action})
        for decision_id, decision, because, next_action in data
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add(
            {
                "next_id": "NEXT2993_0_2994",
                "priority": "selected_primary",
                "next_doc": "2994-Y5-R2FR-parent-Sextra-line-hunt-or-GK-q-loc-source-pack-extraction-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_parent_Sextra_line_hunt_or_GK_q_loc_source_pack_extraction_under_AX1090_2994.py",
                "objective": "Search for an explicit parent S_extra/S_Z action line and field normalization; if absent, take the concrete GK/q_loc sector from 2189 and try to source its metric response, source current, boundary term and readout lock as the first epsilon_Qv_extra component row.",
                "include": "S_extra line;field list;Gamma/Khat/q_loc source pack;C_GK;dC_GK;J_GK;B_GK;M_ref;nonclaim coefficient row",
                "exclude": "generic double-zero re-proof;local-GR claim;Newton claim;PPN/R10 pass;GitHub action;formalization-workbench edits",
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        add({"copy": key, "path": str(path), "exists": path.exists()})
        for key, path in BRANCH_OUTPUTS.items()
    ]


def validation(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_files = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
    checks = [
        ("VAL2993_0_sources_exist", all(row["exists"] for row in all_rows["sources"]), "all cited local source paths exist", True),
        ("VAL2993_1_anchors_found", all(row["anchors_found"] for row in all_rows["sources"]), "all cited source anchors found", True),
        ("VAL2993_2_source_pack_not_signed", any(row["pack_id"] == "PES2993_10_total" and row["current_status"] == "SOURCE_PACK_NOT_SIGNED" for row in all_rows["source_pack"]), "source pack total remains not signed", True),
        ("VAL2993_3_no_clause_signed", all(not row["clause_signed_now"] for row in all_rows["source_pack"]), "no source-pack clause is falsely signed", True),
        ("VAL2993_4_epsilon_nonclaim", all(not row["valid_for_claim"] and not row["claim_allowed"] for row in all_rows["epsilon"]), "epsilon acquisition rows remain nonclaim", True),
        ("VAL2993_5_no_fake_numeric", all(not row["numeric_value_present"] for row in all_rows["epsilon"]), "no numeric epsilon value fabricated", True),
        ("VAL2993_6_no_promotion", all(not row["promotion_allowed_now"] for row in all_rows["gates"]), "no local-GR/Newton promotion allowed", True),
        ("VAL2993_7_next_written", len(all_rows["next"]) == 1 and all_rows["next"][0]["next_id"] == "NEXT2993_0_2994", "2994 next target written", True),
        ("VAL2993_8_branches_exist", all(row["exists"] for row in all_rows["branches"]), "branch copies exist", True),
        ("VAL2993_9_csvs_parse", all(csv_ok(path) for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) if path.suffix == ".csv"), "all generated CSVs parse", True),
        ("VAL2993_10_outputs_under_post", all(under(path, ROOT) for path in output_files), "all generated outputs under post-checkpoint-work", True),
        ("VAL2993_11_formalization_clean", len(list(FORMALIZATION.rglob("*2993*"))) == 0 if FORMALIZATION.exists() else True, f"no 2993 outputs in formalization-workbench (count={len(list(FORMALIZATION.rglob('*2993*'))) if FORMALIZATION.exists() else 0})", True),
        ("VAL2993_12_doc_written", DOC.exists(), "2993 markdown checkpoint exists", True),
    ]
    out = [
        add(
            {
                "validation_id": validation_id,
                "passed": bool(passed),
                "check": check,
                "required": required,
            }
        )
        for validation_id, passed, check, required in checks
    ]
    out.append(
        add(
            {
                "validation_id": "VAL2993_OVERALL",
                "passed": all(row["passed"] for row in out),
                "check": "2993 validation overall",
                "required": True,
            }
        )
    )
    return out


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def table(out_rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |" for row in out_rows]
    return "\n".join([header, sep, *body])


def write_markdown(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        f"""# 2993 - Parent Extra-Sector Source Normal-Form Pack or First epsilon_Qv_extra Numeric Row

Status: `Y5_R2FR_2993_parent_extra_source_pack_not_signed_first_epsilon_Qv_extra_acquisition_rows_staged_nonclaim`

Claim ceiling: `no_parent_extra_source_pack_claim_no_epsilon_Qv_extra_zero_no_local_GR_no_Newton_no_WEP_no_R10_no_PPN_no_clock_no_orbital_no_public_claim`

## Summary

- The route is sharper now: the needed parent package is no longer vague. It is `S_extra/S_Z` plus branch data, positive gap, complete `C_i/O_i` inventory, zero source slot, boundary silence, readout lock and `M_ref`.
- Current files provide a coherent ansatz and conditional theorem, not a signed parent source-normal-form package.
- No numeric epsilon value was fabricated. The first acquisition row is staged with `numeric_value_present=false`.
- The next useful leap is either finding the explicit parent `S_extra/S_Z` line, or taking the concrete `Gamma/Khat/q_loc` sector as the first field-specific source pack.

## Generated Outputs

{table(branch_rows_for_outputs(), ["output", "path", "exists"])}

## Branch Copies

{table(all_rows["branches"], ["copy", "path", "exists"])}

## Source Register

{table(all_rows["sources"], ["source_id", "role", "exists", "anchors_found"])}

## Parent Extra Source-Pack Audit

{table(all_rows["source_pack"], ["pack_id", "required_input", "current_status", "residual_symbol_if_open", "next_action"])}

## Clause Gates

{table(all_rows["gates"], ["gate_id", "gate", "condition_passed", "status", "promotion_allowed_now"])}

## First epsilon_Qv_extra Numeric-Row Acquisition

{table(all_rows["epsilon"], ["epsilon_id", "symbol", "row_role", "numeric_value", "numeric_value_present", "reason_not_numeric"])}

## Decision Ledger

{table(all_rows["decision"], ["decision_id", "decision", "because", "next_action"])}

## Next Target

{table(all_rows["next"], ["next_id", "priority", "next_doc", "next_script", "objective", "exclude"])}

## Validation

{table(all_rows["validation"], ["validation_id", "passed", "check", "required"])}

Validation overall: `{all_rows["validation"][-1]["passed"]}`.
""",
        encoding="utf-8",
    )


def branch_rows_for_outputs() -> list[dict[str, Any]]:
    return [
        {"output": key, "path": str(path), "exists": path.exists()}
        for key, path in OUTPUTS.items()
        if key != "validation"
    ]


def main() -> None:
    all_rows: dict[str, list[dict[str, Any]]] = {
        "sources": source_rows(),
        "source_pack": source_pack_rows(),
        "gates": gate_rows(),
        "epsilon": epsilon_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
    }
    for key, path in OUTPUTS.items():
        if key in {"branches", "validation"}:
            continue
        write_csv(path, all_rows[key])
    shutil.copyfile(OUTPUTS["source_pack"], BRANCH_OUTPUTS["source_pack_copy"])
    shutil.copyfile(OUTPUTS["epsilon"], BRANCH_OUTPUTS["epsilon_copy"])
    shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])
    all_rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], all_rows["branches"])
    all_rows["validation"] = validation(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)
    all_rows["validation"] = validation(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)
    print(f"2993 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()

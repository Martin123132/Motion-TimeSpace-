from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LAB_R10 = ROOT / "source-intake" / "lab-r10"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
RAW = RAB_SECTOR / "raw"
ACCEPTED = RAB_SECTOR / "accepted"
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1659"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1659-Y5-R2FR-LD-mapping-rule-or-conservative-geometry-bound.md"

PRIMARY_TEXT = LAB_R10 / "Lee_Adelberger_2020_arXiv_2002_11761.txt"

SOURCE_FILES = {
    "1658_doc": ROOT / "1658-Y5-R2FR-lab-R10-geometry-extraction-ledger.md",
    "1658_validation": OUT / "P8_Y5_BRR545_1658_VALIDATION.csv",
    "1658_next": OUT / "P8_Y5_PARENT_QLOC_1658_NEXT_TARGET.csv",
    "1658_geometry": OUT / "P8_Y5_PARENT_QLOC_1658_LAB_R10_GEOMETRY_EXTRACTION_LEDGER.csv",
    "1658_ld_gate": OUT / "P8_Y5_PARENT_QLOC_1658_LD_CANDIDATE_GATE.csv",
    "1658_nablaploc": OUT / "P8_Y5_PARENT_QLOC_1658_NABLAPLOC_GEOMETRY_TEMPLATE.csv",
    "primary_text": PRIMARY_TEXT,
}

NEEDLES = {
    "1658_doc": ["hole-pattern diameter: 52 mm", "none of those fields is automatically the finite-domain `L_D`"],
    "1658_validation": ["VAL1658_OVERALL", "PASS"],
    "1658_next": ["1659-Y5-R2FR-LD-mapping-rule-or-conservative-geometry-bound.md", "L_D rule"],
    "1658_geometry": ["GEO1658_2_hole_pattern_diameter", "SOURCE_BACKED_APPARATUS_SCALE_NOT_LD"],
    "1658_ld_gate": ["LDG1658_5_selection_verdict", "NOT_SELECTED"],
    "1658_nablaploc": ["MISSING_LD_SELECTION_RULE", "GEOMETRY_EXTRACTED_LD_NOT_SELECTED"],
    "primary_text": ["The hole pattern diameter is 52 mm", "separations between 52 µm and 3.0 mm"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1659_SOURCE_REGISTER.csv"
INTAKE_SCAN = OUT / "P8_Y5_PARENT_QLOC_1659_INTAKE_SCAN.csv"
LD_RULE_CANDIDATES = OUT / "P8_Y5_PARENT_QLOC_1659_LD_RULE_CANDIDATES.csv"
CONSERVATIVE_LD_ROW = OUT / "P8_Y5_PARENT_QLOC_1659_CONSERVATIVE_LD_ROW.csv"
NABLAPLOC_READY_TEMPLATE = OUT / "P8_Y5_PARENT_QLOC_1659_NABLAPLOC_READY_TEMPLATE.csv"
RULE_REFUSAL_RUNNER = OUT / "P8_Y5_PARENT_QLOC_1659_LD_RULE_REFUSAL_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1659_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1659_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1659_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1659_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    INTAKE_SCAN,
    LD_RULE_CANDIDATES,
    CONSERVATIVE_LD_ROW,
    NABLAPLOC_READY_TEMPLATE,
    RULE_REFUSAL_RUNNER,
    CLAIM_GATE,
    DECISION,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    LD_RULE_CANDIDATES,
    CONSERVATIVE_LD_ROW,
    NABLAPLOC_READY_TEMPLATE,
    RULE_REFUSAL_RUNNER,
    CLAIM_GATE,
    DECISION,
    NEXT_TARGET,
]

COPY_TARGETS = {
    LD_RULE_CANDIDATES: [
        QUARANTINE / "LD_RULE_CANDIDATES_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_LD_rule_candidates_nonclaim_1659.csv",
        QUEUE / "JR1659_LD_RULE_CANDIDATES_NONCLAIM.csv",
    ],
    CONSERVATIVE_LD_ROW: [
        QUARANTINE / "CONSERVATIVE_LD_ROW_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_conservative_LD_row_nonclaim_1659.csv",
        QUEUE / "JR1659_CONSERVATIVE_LD_ROW_NONCLAIM.csv",
    ],
    NABLAPLOC_READY_TEMPLATE: [
        QUARANTINE / "NABLAPLOC_READY_TEMPLATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_nablaPloc_ready_template_nonclaim_1659.csv",
        QUEUE / "JR1659_NABLAPLOC_READY_TEMPLATE_NONCLAIM.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_nonclaim_1659.csv",
        QUEUE / "JR1659_NEXT_TARGET_NONCLAIM.csv",
    ],
}


def ensure_dirs() -> None:
    for directory_path in [OUT, QUARANTINE, BRANCH_RESIDUALS, RAW, ACCEPTED, QUEUE]:
        directory_path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def bool_string(value: object) -> str:
    return str(value).strip().lower()


def all_claim_flags_false(paths: list[Path]) -> bool:
    flag_names = {
        "accepted_for_scoring",
        "claim_allowed",
        "claim_ready",
        "score_allowed",
        "score_ready",
        "valid_for_claim",
        "valid_for_mts_claim",
        "valid_for_runner",
    }
    for path in paths:
        for row in csv_rows(path):
            for flag_name in flag_names.intersection(row):
                if bool_string(row[flag_name]) == "true":
                    return False
    return True


def find_line(pattern: str) -> int:
    for index, line in enumerate(read_text(PRIMARY_TEXT).splitlines(), start=1):
        if pattern in line:
            return index
    return -1


def source_register_rows() -> list[dict[str, object]]:
    rows = []
    for source_id, path in SOURCE_FILES.items():
        text = read_text(path)
        needles = NEEDLES[source_id]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path.exists(),
                "needles_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "role": "1659 L_D mapping rule or conservative geometry bound",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def intake_scan_rows() -> list[dict[str, object]]:
    scans = [
        ("SCAN1659_0_raw", RAW, "raw_live_candidate_folder"),
        ("SCAN1659_1_accepted", ACCEPTED, "accepted_live_candidate_folder"),
        ("SCAN1659_2_queue", QUEUE, "nonclaim_acquisition_queue"),
    ]
    rows = []
    for scan_id, folder, role in scans:
        csv_count = len(list(folder.glob("*.csv"))) if folder.exists() else 0
        if folder == RAW and csv_count == 0:
            status = "NO_RAW_LIVE_ROWS"
        elif folder == ACCEPTED and csv_count == 0:
            status = "NO_ACCEPTED_LIVE_ROWS"
        elif folder == QUEUE and csv_count:
            status = "QUEUE_PRESENT_NONCLAIM"
        else:
            status = "LIVE_ROWS_REQUIRE_REVIEW"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "scan_id": scan_id,
                "folder_role": role,
                "folder_path": str(folder),
                "csv_count": csv_count,
                "status": status,
                "source_ready": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def ld_rule_candidate_rows() -> list[dict[str, object]]:
    rows = [
        ("LDRULE1659_0_min_gap", "L_D = 52 µm minimum separation", "REJECT", "underestimates full support; 1658 explicitly forbids equating separation floor with L_D"),
        ("LDRULE1659_1_vertical_scan", "L_D = 3.0 mm maximum separation", "DEFER", "vertical scan span is source-backed but does not cover horizontal patterned support"),
        ("LDRULE1659_2_full_support_radius", "L_D_upper = 52 mm / 2 = 26 mm", "SELECT_CONSERVATIVE_NONCLAIM", "covers full patterned support disk if compact Fermi tube is required over the apparatus support"),
        ("LDRULE1659_3_material_thickness", "L_D = max(54 µm,99 µm)", "DEFER", "material thickness alone ignores lateral support and separation"),
        ("LDRULE1659_4_multi_scale", "carry separate L_parallel, L_perp, L_thickness", "FUTURE_REFINEMENT", "best long-run option but not a single-row L_D for current bound runner"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "rule_id": rule_id,
            "candidate_rule": candidate_rule,
            "decision": decision,
            "reason": reason,
            "method_backed": decision == "SELECT_CONSERVATIVE_NONCLAIM",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for rule_id, candidate_rule, decision, reason in rows
    ]


def conservative_ld_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CLD1659_0_full_support_upper_bound",
            "domain_id": "lab_R10_compact_fermi_tube",
            "rule": "full_support_Fermi_tube_upper_bound",
            "source_field": "hole_pattern_diameter",
            "source_value": "52 mm",
            "source_line": find_line("The hole pattern diameter is 52 mm"),
            "L_D_rule": "L_D_upper = D_pattern/2",
            "L_D_m": "2.6e-2",
            "why_conservative": "uses full patterned support radius rather than minimum gap; likely overbounds projector drift but avoids under-covering apparatus support",
            "limitations": "not a derived parent-domain theorem; may be too conservative; must be replaced by multi-scale domain if needed",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def nablaploc_template_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NPLR1659_0_conservative_LD_template",
            "domain_id": "lab_R10_compact_fermi_tube",
            "formula": "nabla_Ploc_Linf <= C_Fermi*(2.6e-2 m)*Riemann_norm + C_Fermi2*(2.6e-2 m)^2*nabla_Riemann_norm + frame_terms",
            "L_D_m": "2.6e-2",
            "Riemann_norm_m2": "MISSING",
            "nabla_Riemann_norm_m3": "MISSING",
            "C_Fermi": "MISSING",
            "C_Fermi2": "MISSING",
            "frame_terms": "MISSING",
            "current_status": "LD_UPPER_SELECTED_NONCLAIM_LOWER_INPUTS_MISSING",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def refusal_rows() -> list[dict[str, object]]:
    rows = [
        ("RUN1659_0_LD_rule", "conservative L_D upper-bound rule", "PASS_AS_INTERNAL_METHOD_ONLY", "L_D_upper=26mm is method-backed by geometry but not score-ready or claim-ready"),
        ("RUN1659_1_min_gap", "52 µm as L_D", "REFUSE", "explicitly rejected as under-defined shortcut"),
        ("RUN1659_2_nabla", "nabla_Ploc numeric bound", "REFUSE_SCORING", "curvature norms, constants, and frame terms missing"),
        ("RUN1659_3_local", "local_GR_Newton_PPN_R10_WEP", "REFUSE_SCORING", "L_D method row is nonclaim and no normalized residual bound exists"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "run_id": run_id,
            "quantity": quantity,
            "runner_decision": decision,
            "reason": reason,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for run_id, quantity, decision, reason in rows
    ]


def claim_rows() -> list[dict[str, object]]:
    rows = [
        ("CG1659_0_LD_method", "conservative L_D upper-bound row exists", "INTERNAL_METHOD_ONLY", "NONCLAIM", "method row is not a parent-domain theorem"),
        ("CG1659_1_nabla", "nabla_Ploc numeric/source row is accepted", False, "BLOCKED", "curvature/constants/frame terms missing"),
        ("CG1659_2_MHref", "M_H_ref denominator is accepted", False, "BLOCKED", "still missing from prior gates"),
        ("CG1659_3_local", "local GR/Newton/PPN/R10/WEP follows", False, "NO_CLAIM", "no normalized local residual bound exists"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": gate_pass,
            "status": status,
            "blocker": blocker,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, claim, gate_pass, status, blocker in rows
    ]


def decision_rows() -> list[dict[str, object]]:
    rows = [
        ("DEC1659_0_LD_upper", "SELECT_CONSERVATIVE_LD_UPPER_NONCLAIM", "full-support pattern radius is source-backed and avoids underestimating finite-domain projector drift", "use L_D=2.6e-2 m as an internal upper-bound method row only"),
        ("DEC1659_1_min_gap", "REJECT_52UM_AS_LD", "minimum separation is not the domain radius", "keep 52 µm only as source-test separation scale"),
        ("DEC1659_2_next", "NEXT_1660_CURVATURE_FRAME_INPUTS", "nabla_Ploc can now wait on curvature/frame/constants rather than L_D mapping", "build conservative-LD curvature/frame lower-input runner"),
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


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1660-Y5-R2FR-conservative-LD-curvature-frame-input-runner.md",
            "script": "scripts/Y5_R2FR_conservative_LD_curvature_frame_input_runner.py",
            "objective": "with L_D_upper=2.6e-2 m as nonclaim method row, source or block Riemann_norm, nabla_Riemann_norm, C_Fermi, C_Fermi2, and lab frame terms for the nabla_Ploc bound",
            "success_condition": "lower inputs become source-backed with units or remain explicit MISSING_* while scoring stays blocked",
            "forbidden_shortcuts": "no local-GR/PPN/R10/WEP claim; no M_H_ref substitution; no treating L_D method row as parent theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        }
    ]


def validation_rows(source_rows, intake_rows, rules, conservative, nablaploc, refusal, claim, decisions, next_targets):
    generated_csv_parse = True
    try:
        for generated_path in GENERATED:
            csv_rows(generated_path)
    except Exception:
        generated_csv_parse = False

    formalization_dirty = any((FORMALIZATION / path.name).exists() for path in [DOC, *GENERATED, VALIDATION]) if FORMALIZATION.exists() else False

    checks = [
        ("VAL1659_0_sources_exist", all(row["path_exists"] and row["needles_found"] for row in source_rows), "all cited 1659 source paths exist and needles are present"),
        ("VAL1659_1_intake_scanned", any(row["status"] == "NO_RAW_LIVE_ROWS" for row in intake_rows) and any(row["status"] == "NO_ACCEPTED_LIVE_ROWS" for row in intake_rows), "raw and accepted live source folders are scanned"),
        ("VAL1659_2_min_gap_rejected", any(row["rule_id"] == "LDRULE1659_0_min_gap" and row["decision"] == "REJECT" for row in rules), "52 um separation is rejected as L_D"),
        ("VAL1659_3_conservative_rule_selected", conservative[0]["L_D_m"] == "2.6e-2" and int(conservative[0]["source_line"]) > 0, "conservative L_D upper row sourced from hole-pattern diameter"),
        ("VAL1659_4_nabla_template_ready_nonclaim", nablaploc[0]["current_status"] == "LD_UPPER_SELECTED_NONCLAIM_LOWER_INPUTS_MISSING" and nablaploc[0]["valid_for_claim"] is False, "nabla_Ploc template carries L_D_upper but remains nonclaim"),
        ("VAL1659_5_refusal_runner_blocks", any(row["runner_decision"] == "REFUSE_SCORING" for row in refusal), "refusal runner blocks scoring"),
        ("VAL1659_6_claim_gates_safe", all(row["claim_allowed"] is False and row["valid_for_claim"] is False for row in claim), "all claim gates keep MTS claims false"),
        ("VAL1659_7_next_target_selected", next_targets[0]["next_target"] == "1660-Y5-R2FR-conservative-LD-curvature-frame-input-runner.md", "next target selects conservative-LD curvature/frame inputs"),
        ("VAL1659_8_csv_parse", generated_csv_parse, "all generated 1659 CSVs parse"),
        ("VAL1659_9_no_mts_claim_flags", all_claim_flags_false(CLAIM_CHECKED), "all 1659 generated rows keep MTS claim/no-score flags false"),
        ("VAL1659_10_branch_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" not in str(target)), "branch/quarantine copies exist"),
        ("VAL1659_11_queue_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" in str(target)), "acquisition queue nonclaim copies exist"),
        ("VAL1659_12_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1659_13_formalization_untouched", not formalization_dirty, "no 1659 outputs found under formalization-workbench"),
    ]
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1659_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1659 L_D mapping rule/conservative geometry bound validation",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row[column]) for column in columns) + " |")
    return "\n".join(lines)


def write_doc(source_rows, intake_rows, rules, conservative, nablaploc, refusal, claim, decisions, next_targets, validation) -> None:
    text = f"""# 1659 - L_D Mapping Rule Or Conservative Geometry Bound

**Private status:** nonclaim method checkpoint. No `nabla_Ploc` numeric bound, `M_H_ref`, R10 pass, local-GR pass, Newton pass, PPN pass, WEP pass, or public claim is made.

## Verdict

`1659` rejects the tempting shortcut and selects only a conservative internal method row:

```text
rejected: L_D = 52 µm minimum separation
selected nonclaim method row: L_D_upper = 52 mm / 2 = 2.6e-2 m
```

The reason is simple: the minimum detector-attractor gap is not a finite-domain support radius. If the Fermi tube must cover the full patterned support, the source-backed hole-pattern radius is a conservative upper scale. It likely overbounds projector drift, but it avoids under-covering the apparatus and remains noncircular.

This still does not score anything. Curvature norms, frame terms, constants, and `M_H_ref` remain missing.

## Source Register

{markdown_table(source_rows, ["source_id", "path", "path_exists", "needles_found", "role"])}

## Intake Scan

{markdown_table(intake_rows, ["scan_id", "folder_role", "folder_path", "csv_count", "status"])}

## L_D Rule Candidates

{markdown_table(rules, ["rule_id", "candidate_rule", "decision", "reason"])}

## Conservative L_D Row

{markdown_table(conservative, ["row_id", "rule", "source_field", "source_value", "source_line", "L_D_rule", "L_D_m", "limitations"])}

## nablaPloc Ready Template

{markdown_table(nablaploc, ["row_id", "formula", "L_D_m", "Riemann_norm_m2", "nabla_Riemann_norm_m3", "current_status"])}

## Refusal Runner

{markdown_table(refusal, ["run_id", "quantity", "runner_decision", "reason"])}

## Claim Gates

{markdown_table(claim, ["gate_id", "claim", "gate_pass", "status", "blocker"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Next Target

{markdown_table(next_targets, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Working Interpretation

The local projector branch has its first conservative geometry scale. This is not a win condition, but it turns the next job into a lower-input problem: source or bound curvature, frame motion, and constants for a concrete `L_D_upper`.
"""
    DOC.write_text(text, encoding="utf-8")


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)


def main() -> None:
    ensure_dirs()
    source_rows = source_register_rows()
    intake_rows = intake_scan_rows()
    rules = ld_rule_candidate_rows()
    conservative = conservative_ld_rows()
    nablaploc = nablaploc_template_rows()
    refusal = refusal_rows()
    claim = claim_rows()
    decisions = decision_rows()
    next_targets = next_rows()

    for path, rows in [
        (SOURCE_REGISTER, source_rows),
        (INTAKE_SCAN, intake_rows),
        (LD_RULE_CANDIDATES, rules),
        (CONSERVATIVE_LD_ROW, conservative),
        (NABLAPLOC_READY_TEMPLATE, nablaploc),
        (RULE_REFUSAL_RUNNER, refusal),
        (CLAIM_GATE, claim),
        (DECISION, decisions),
        (NEXT_TARGET, next_targets),
    ]:
        write_csv(path, rows)

    copy_outputs()
    validation = validation_rows(source_rows, intake_rows, rules, conservative, nablaploc, refusal, claim, decisions, next_targets)
    write_csv(VALIDATION, validation)
    write_doc(source_rows, intake_rows, rules, conservative, nablaploc, refusal, claim, decisions, next_targets, validation)

    if any(row["result"] == "FAIL" for row in validation):
        raise SystemExit("1659 validation failed; see P8_Y5_BRR545_1659_VALIDATION.csv")

    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    print("1659 validation PASS")


if __name__ == "__main__":
    main()

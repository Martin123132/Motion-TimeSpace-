from __future__ import annotations

import csv
from pathlib import Path

from Y5_R2FR_Dq_vX_observed_metric_zero_or_finite_DObs_leak_row_2025 import (
    BRANCH_WEP,
    OUT,
    QUEUE,
    ROOT,
    SOURCE_WEIGHT_DOCS,
    base_row,
    count_formalization_modified,
    csv_rows_parse,
    md_table,
    read_text,
    remove_pycache,
    write_csv,
)


DOC = ROOT / "2035-Y5-R2FR-quotient-factorisation-exhaustion-or-row-null-hessian-source.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCAN_ROOTS = [OUT, QUEUE, BRANCH_WEP, SOURCE_WEIGHT_DOCS]


def formalization_has_2035_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        return any(FORMALIZATION.rglob("*2035*quotient*")) or any(FORMALIZATION.rglob("*2035*hessian*")) or any(FORMALIZATION.rglob("*2035*finite*Z*"))
    except Exception:
        return False


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    try:
        with path.open("r", newline="", encoding="utf-8", errors="replace") as handle:
            return list(csv.DictReader(handle))
    except Exception:
        return []


def boolish(value: object) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid"}


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2035_00_2034_handoff",
            ROOT / "2034-Y5-R2FR-Lcore-theta-current-fill-or-first-finite-Z-source.md",
            ["NEXT2034_0_2035", "LCORE2034_4_required_law", "VAL2034_OVERALL"],
            "2034 selects quotient-factorisation exhaustion or row-null Hessian source acquisition.",
        ),
        (
            "SRC2035_01_2034_next",
            OUT / "P8_Y5_PARENT_QLOC_2034_NEXT_TARGET.csv",
            ["NEXT2034_0_2035"],
            "machine-readable 2035 target.",
        ),
        (
            "SRC2035_02_1107_exhaustion",
            ROOT / "1107-Y5-R10-parent-object-language-exhaustion-derivation-or-alpha-coefficient-source-row.md",
            ["EXH1107_6_verdict", "OBJECT_LANGUAGE_EXHAUSTION_NOT_DERIVED"],
            "broad object-language exhaustion was previously rejected as not derived.",
        ),
        (
            "SRC2035_03_1107_exhaustion_csv",
            OUT / "P8_Y5_R10_1107_OBJECT_LANGUAGE_EXHAUSTION_ATTEMPT.csv",
            ["EXH1107_0_target", "EXH1107_6_verdict"],
            "machine-readable exhaustion attempt.",
        ),
        (
            "SRC2035_04_968_domain",
            ROOT / "968-Y5-R10-parent-domain-signature-and-memory-operator-input-audit.md",
            ["PDS968_0_conf_parent_field_list", "PDS968_6_verdict", "NOT_PARENT_SIGNED_CURRENT_CORPUS"],
            "parent-domain/readout exclusion signature is written but not signed.",
        ),
        (
            "SRC2035_05_1022_quotient",
            ROOT / "1022-Y5-R10-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice.md",
            ["VQC1022_0_q_map", "VQC1022_1_action_descent"],
            "quotient map/action descent is conditional only.",
        ),
        (
            "SRC2035_06_1023_action_descent",
            ROOT / "1023-Y5-R10-q-vX-action-descent-certificate-or-scalar-nohair-demotion.md",
            ["QVC1023_2_action_descent", "DEC1023_0_certificate_result"],
            "single q/v_X/action certificate does not close.",
        ),
        (
            "SRC2035_07_1265_auxiliary",
            ROOT / "1265-Y5-R10-RAB-auxiliary-constraint-protection-or-finite-ZR-bound-runner.md",
            ["AP1265_1_no_derivatives", "AET1265_0_auxiliary_elimination", "VAL1265_11_overall"],
            "auxiliary elimination theorem remains conditional on parent-signed protection clauses.",
        ),
        (
            "SRC2035_08_1868_grammar",
            ROOT / "source-intake" / "microscope" / "quarantine" / "1868" / "P8_Y5_PARENT_QLOC_1868_CANDIDATE_PARENT_GRAMMAR.csv",
            ["CPG1868_0_parent_primitives", "CPG1868_2_no_independent_RAB", "CPG1868_3_derivative_permission"],
            "candidate primitive grammar for no-independent-RAB and derivative permissions.",
        ),
    ]
    rows = []
    for source_id, path, needles, note in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        ok = exists and all(needle in text for needle in needles)
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "status": "EXISTS_NEEDLES_CONFIRMED" if ok else "MISSING_OR_NEEDLE_FAIL",
                "needles": ";".join(needles),
                "note": note,
            }
        )
        rows.append(row)
    return rows


def exhaustion_gate_rows() -> list[dict[str, object]]:
    data = [
        (
            "EXH2035_0_target",
            "prove u=R_AB and D_mu u are absent from L_phys, S_matter, and B except Lambda_R u",
            "would activate THM2034_3 and set Z_R=J_R=Q_R=B_R=0",
            "TARGET_SHARP",
            "n/a",
        ),
        (
            "EXH2035_1_domain",
            "closed Conf_parent excludes readout variables as action arguments",
            "needed before u can be removed from the parent language",
            "FAIL_UNSIGNED",
            "PDS968_0/PDS968_6 say domain signature is not parent-signed",
        ),
        (
            "EXH2035_2_generator_image",
            "ParentGenerate image contains y/e_pub/theta/topological levels but not independent u or Du targets",
            "the actual no-extension/exhaustion claim",
            "FAIL_UNSIGNED",
            "EXH1107_6 says object-language exhaustion is not derived",
        ),
        (
            "EXH2035_3_action_descent",
            "S_parent descends before variation: S_parent[Phi]=S_red[q(Phi)]+silent boundary/topological terms",
            "would make row-null Hessian automatic",
            "FAIL_UNSIGNED",
            "QVC1023_2 remains conditional only",
        ),
        (
            "EXH2035_4_no_Du_constructor",
            "no vertical metric, vertical connection, Sobolev norm, or derivative constructor can form G_vert(Du,Du)",
            "forbids Z_R and Z_RY at tree level",
            "FAIL_UNSIGNED",
            "AP1265_1 remains unsigned grammar protection",
        ),
        (
            "EXH2035_5_matter_descent",
            "ordinary matter factors through e_pub/theta and not u or source-only shadows",
            "would set J_R=0",
            "FAIL_UNSIGNED",
            "matter functor/object language not parent-signed",
        ),
        (
            "EXH2035_6_boundary_descent",
            "boundary functional B has no u dependence and no R boundary momentum",
            "would set Q_R=B_R=0",
            "FAIL_UNSIGNED",
            "boundary/domain terms not proved silent",
        ),
        (
            "EXH2035_7_readout_stability",
            "effective/readout maps cannot regenerate a u-dependent local EFT branch after variation",
            "protects the theorem beyond tree-level wording",
            "FAIL_UNSIGNED",
            "EXH1107_5 radiative/readout stability unsigned",
        ),
        (
            "EXH2035_8_verdict",
            "quotient-factorisation exhaustion is not derived in the current corpus",
            "exact route remains open as a theorem target, but finite row-null sourcing must stay live",
            "QUOTIENT_FACTORISATION_EXHAUSTION_NOT_DERIVED",
            "need a parent generator/domain certificate or numeric finite residual coefficients",
        ),
    ]
    rows = []
    for row_id, clause, consequence, status, evidence in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "clause": clause,
                "consequence": consequence,
                "status": status,
                "evidence": evidence,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def scan_symbol_candidates(symbols: list[str]) -> list[dict[str, object]]:
    rows = []
    csv_paths: list[Path] = []
    for root in SCAN_ROOTS:
        if root.exists():
            csv_paths.extend(root.rglob("*.csv"))
    for symbol in symbols:
        valid_hits = []
        nonclaim_hits = 0
        for path in csv_paths:
            for csv_row in read_csv_dicts(path):
                values = [str(value) for value in csv_row.values()]
                if not any(symbol in value for value in values):
                    continue
                if boolish(csv_row.get("valid_for_claim", False)) or boolish(csv_row.get("claim_allowed", False)):
                    valid_hits.append(path)
                else:
                    nonclaim_hits += 1
        row = base_row()
        row.update(
            {
                "symbol": symbol,
                "valid_candidate_count": len(set(valid_hits)),
                "nonclaim_reference_count": nonclaim_hits,
                "valid_candidate_paths": ";".join(str(path) for path in sorted(set(valid_hits))[:8]),
                "status": "VALID_SOURCE_ROW_FOUND_REVIEW_REQUIRED" if valid_hits else "NO_VALID_SOURCE_ROW_FOUND",
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def finite_source_requirement_rows() -> list[dict[str, object]]:
    data = [
        ("REQ2035_0_ZRR", "Z_RR^{mu nu}", "parent kinetic Hessian projected by J_u^A J_u^B", "numeric tensor or theorem-zero row with source path and units"),
        ("REQ2035_1_ZRY", "Z_RY^{mu nu}", "cross kinetic row-null failure", "numeric cross tensor or theorem-zero row; scalar projection alone is insufficient"),
        ("REQ2035_2_MR2", "M_R^2", "parent Hessian/effective mass for u", "numeric mass scale or signed absence theorem"),
        ("REQ2035_3_JR", "J_R", "matter/core source Euler projection onto u", "matter descent theorem or finite source coefficient"),
        ("REQ2035_4_QR_BR", "Q_R/B_R", "boundary charge and boundary functional derivative", "boundary silence theorem or finite flux coefficient"),
        ("REQ2035_5_tau", "tau_R10/tau_PPN/tau_clock/tau_orbital", "arena projection maps", "sourced maps into experimental residual vectors"),
        ("REQ2035_6_no_cancellation", "absolute component guard", "score sum/vector norm before cancellations", "all components listed with signs and magnitudes"),
    ]
    rows = []
    for row_id, symbol, definition, acceptance in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "symbol": symbol,
                "definition": definition,
                "acceptance_requirement": acceptance,
                "status": "SOURCE_REQUIRED_NONCLAIM",
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def route_decision_rows(scan_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    any_valid = any(int(row["valid_candidate_count"]) > 0 for row in scan_rows)
    data = [
        (
            "DEC2035_0_exhaustion_result",
            "Reject current proof of quotient-factorisation exhaustion.",
            "The exact theorem target is sharp, but existing corpus evidence says parent-domain, generator image, action descent, matter, boundary, and readout stability are unsigned.",
        ),
        (
            "DEC2035_1_not_dead",
            "This does not kill the local-GR route.",
            "It says the route must be closed by a parent generator/domain certificate, not by repeated verbal no-hair claims.",
        ),
        (
            "DEC2035_2_finite_scan",
            "Scan for valid finite row-null Hessian/source candidates completed.",
            "At least one valid row needs review." if any_valid else "No valid claim-ready finite Z/J/Q/B row was found in scanned source-intake queues.",
        ),
        (
            "DEC2035_3_best_next",
            "Next target should build the minimal parent generator/domain certificate specifically for u=R_AB.",
            "If that certificate cannot be constructed, stop derivation-first on this branch and run finite residual acquisition against R10/PPN/clock/orbital.",
        ),
    ]
    rows = []
    for row_id, decision, rationale in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "decision": decision,
                "rationale": rationale,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows(scan_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    any_valid = any(int(row["valid_candidate_count"]) > 0 for row in scan_rows)
    data = [
        ("GATE2035_0_exhaustion", "quotient-factorisation exhaustion proven", "FAIL_UNSIGNED", "EXH2035_8 rejects current proof"),
        ("GATE2035_1_row_null_hessian", "row-null Hessian evaluated from parent coefficients", "FAIL_MISSING_VALUES", "no parent Z_AB tensor supplied"),
        ("GATE2035_2_source_boundary", "J_R=Q_R=B_R zero or finite values sourced", "FAIL_MISSING_VALUES", "matter/boundary clauses unsigned"),
        ("GATE2035_3_candidate_scan", "finite source scan found reviewable rows", "PASS_REVIEW_REQUIRED" if any_valid else "PASS_NO_VALID_ROWS_FOUND", "scan completed under source-intake queues"),
        ("GATE2035_4_local_GR_claim", "local GR/Newton/R10/PPN/clock/orbital pass", "FAIL_BLOCKED", "neither exhaustion theorem nor finite residual bound is claim-valid"),
    ]
    rows = []
    for row_id, gate, status, detail in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "gate": gate,
                "status": status,
                "detail": detail,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def next_target_rows() -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "target_id": "NEXT2035_0_2036",
            "target_doc": "2036-Y5-R2FR-minimal-u-domain-certificate-or-finite-local-residual-acquisition.md",
            "objective": "attempt the narrow parent-domain/generator certificate for u=R_AB: prove u and Du are not action arguments while Lambda_R u is parent-owned; if this fails, switch from derivation-first to finite local residual acquisition for Z_RR/Z_RY/J_R/Q_R/B_R and arena projections",
            "must_include": "typed Conf_parent; ParentGenerate_u image; no u/Du constructors; Lambda_R origin; matter descent; boundary silence; readout-after-variation stability; accepted finite coefficient schema if rejected",
            "excluded": "broad object-language proof; scalar projection only; local-GR claim; closure by taste; hidden GR import; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    exhaustion_rows: list[dict[str, object]],
    scan_rows: list[dict[str, object]],
    requirement_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2035_0_source_weight_exhaustion",
            SOURCE_WEIGHT_DOCS / "AFRAME_U_QUOTIENT_EXHAUSTION_2035_NONCLAIM.csv",
            exhaustion_rows,
        ),
        (
            "COPY2035_1_wep_scan",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2035_ROW_NULL_HESSIAN_SOURCE_SCAN_NONCLAIM.csv",
            scan_rows,
        ),
        (
            "COPY2035_2_rab_requirements",
            QUEUE / "JR2035_FINITE_ROW_NULL_REQUIREMENTS_NONCLAIM.csv",
            requirement_rows,
        ),
    ]
    rows = []
    for copy_id, path, data in copies:
        write_csv(path, data)
        row = base_row()
        row.update(
            {
                "copy_id": copy_id,
                "path": str(path),
                "rows": len(data),
                "status": "WRITTEN_NONCLAIM_COPY",
            }
        )
        rows.append(row)
    return rows


def validation_rows(
    source_rows: list[dict[str, object]],
    exhaustion_rows: list[dict[str, object]],
    scan_rows: list[dict[str, object]],
    requirement_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2035_00_sources_exist", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows), "all cited source paths and needles exist"))
    checks.append(("VAL2035_01_csv_parse", all(csv_rows_parse(path) for path in csv_paths), "all generated CSV files parse cleanly"))
    verdict = next(row for row in exhaustion_rows if row["row_id"] == "EXH2035_8_verdict")
    checks.append(("VAL2035_02_exhaustion_rejected", verdict["status"] == "QUOTIENT_FACTORISATION_EXHAUSTION_NOT_DERIVED", "current corpus does not derive quotient-factorisation exhaustion"))
    checks.append(("VAL2035_03_scan_executed", all("valid_candidate_count" in row for row in scan_rows) and len(scan_rows) >= 6, "finite row-null source scan executed for required symbols"))
    checks.append(("VAL2035_04_requirements_written", len(requirement_rows) >= 7 and all(row["status"] == "SOURCE_REQUIRED_NONCLAIM" for row in requirement_rows), "finite source requirements remain nonclaim"))
    checks.append(("VAL2035_05_claims_blocked", all(str(row.get("claim_allowed", "")).lower() == "false" for row in gate_rows), "all claim gates remain false"))
    checks.append(("VAL2035_06_next_selected", next_rows[0]["target_id"] == "NEXT2035_0_2036", "next target is selected"))
    checks.append(("VAL2035_07_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2035_08_no_formalization_2035_artifacts", not formalization_has_2035_artifacts(), "no 2035 quotient/hessian/finite-Z artifacts were written under formalization-workbench"))
    overall_ok = all(ok for _, ok, _ in checks)
    checks.append(("VAL2035_OVERALL", overall_ok, "2035 quotient-factorisation exhaustion checkpoint is internally valid and nonclaim"))
    rows = []
    for check_id, ok, detail in checks:
        row = base_row()
        row.update(
            {
                "check_id": check_id,
                "status": "PASS" if ok else "FAIL",
                "detail": detail,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def write_doc(
    source_rows: list[dict[str, object]],
    exhaustion_rows: list[dict[str, object]],
    scan_rows: list[dict[str, object]],
    requirement_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    branch_rows: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    sections = [
        "# 2035 Y5 R2FR Quotient Factorisation Exhaustion Or Row Null Hessian Source",
        "",
        "## Current Verdict",
        "",
        "The narrow exhaustion proof does not close from the current corpus. That is not a collapse; it is a useful fork. Exact local GR now requires a parent-domain/generator certificate proving `u=R_AB` and `D_mu u` are not legal action arguments, while `Lambda_R u` is parent-owned. Without that certificate, the branch must be tested as a finite residual problem using the row-null Hessian/source/boundary formulas.",
        "",
        "No local-GR, Newton, R10, PPN, WEP, clock, orbital, or public claim is made.",
        "",
        "## Source Register",
        md_table(source_rows, ["source_id", "source_path", "status", "note", "valid_for_claim"]),
        "## Exhaustion Gate",
        md_table(exhaustion_rows, ["row_id", "clause", "consequence", "status", "evidence", "claim_allowed"]),
        "## Finite Source Scan",
        md_table(scan_rows, ["symbol", "valid_candidate_count", "nonclaim_reference_count", "status", "valid_candidate_paths", "claim_allowed"]),
        "## Finite Source Requirements",
        md_table(requirement_rows, ["row_id", "symbol", "definition", "acceptance_requirement", "status", "claim_allowed"]),
        "## Decision Ledger",
        md_table(decision_rows_, ["row_id", "decision", "rationale", "claim_allowed"]),
        "## Claim Gate",
        md_table(gate_rows, ["row_id", "gate", "status", "detail", "claim_allowed"]),
        "## Next Target",
        md_table(next_rows, ["target_id", "target_doc", "objective", "must_include", "excluded", "claim_allowed"]),
        "## Branch Copies",
        md_table(branch_rows, ["copy_id", "path", "rows", "status", "valid_for_claim"]),
        "## Validation",
        md_table(validation_rows_, ["check_id", "status", "detail", "claim_allowed"]),
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    exhaustion_rows = exhaustion_gate_rows()
    scan_rows = scan_symbol_candidates(["Z_RR", "Z_RY", "Z_R", "M_R^2", "J_R", "Q_R", "B_R"])
    requirement_rows = finite_source_requirement_rows()
    decision_rows_ = route_decision_rows(scan_rows)
    gate_rows = claim_gate_rows(scan_rows)
    next_rows = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2035_SOURCE_REGISTER.csv",
        "exhaustion": OUT / "P8_Y5_PARENT_QLOC_2035_EXHAUSTION_GATE.csv",
        "scan": OUT / "P8_Y5_PARENT_QLOC_2035_FINITE_SOURCE_SCAN.csv",
        "requirements": OUT / "P8_Y5_PARENT_QLOC_2035_FINITE_SOURCE_REQUIREMENTS.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2035_DECISION_LEDGER.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2035_CLAIM_GATE.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2035_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2035_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2035_VALIDATION.csv",
    }
    write_csv(paths["sources"], source_rows)
    write_csv(paths["exhaustion"], exhaustion_rows)
    write_csv(paths["scan"], scan_rows)
    write_csv(paths["requirements"], requirement_rows)
    write_csv(paths["decision"], decision_rows_)
    write_csv(paths["gates"], gate_rows)
    write_csv(paths["next"], next_rows)
    branch_rows = write_branch_copies(exhaustion_rows, scan_rows, requirement_rows)
    write_csv(paths["branch"], branch_rows)
    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [Path(row["path"]) for row in branch_rows]
    validation_rows_ = validation_rows(
        source_rows,
        exhaustion_rows,
        scan_rows,
        requirement_rows,
        gate_rows,
        next_rows,
        csv_paths_without_validation,
    )
    write_csv(paths["validation"], validation_rows_)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in branch_rows]
    validation_rows_ = validation_rows(
        source_rows,
        exhaustion_rows,
        scan_rows,
        requirement_rows,
        gate_rows,
        next_rows,
        csv_paths,
    )
    write_csv(paths["validation"], validation_rows_)
    write_doc(
        source_rows,
        exhaustion_rows,
        scan_rows,
        requirement_rows,
        decision_rows_,
        gate_rows,
        next_rows,
        branch_rows,
        validation_rows_,
    )
    remove_pycache()


if __name__ == "__main__":
    main()

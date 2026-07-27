from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
MICROSCOPE_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1854"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1854-Y5-R2FR-parent-Hessian-input-extraction-for-ZX-MX2.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1854_SOURCE_REGISTER.csv",
    "scan_summary": RESIDUALS / "P8_Y5_PARENT_QLOC_1854_CORPUS_SCAN_SUMMARY.csv",
    "candidate_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1854_HESSIAN_CANDIDATE_AUDIT.csv",
    "required_clause": RESIDUALS / "P8_Y5_PARENT_QLOC_1854_PARENT_ACTION_CLAUSE_REQUIRED.csv",
    "extraction_result": RESIDUALS / "P8_Y5_PARENT_QLOC_1854_ZX_MX2_EXTRACTION_RESULT.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1854_CLAIM_GATE.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1854_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1854_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1854_VALIDATION.csv",
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def source_path(relative_path: str) -> str:
    return rel(ROOT / relative_path)


def ensure_dirs() -> None:
    for path in [RESIDUALS, MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
        path.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def boolish(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def scan_corpus() -> list[dict[str, Any]]:
    patterns = {
        "Z_X": "Z_X",
        "M_X2": "M_X2",
        "M_X^2": "M_X^2",
        "lambda_X": "lambda_X",
        "MISSING_PARENT_INPUT": "MISSING_PARENT_INPUT",
        "MISSING_ZX": "MISSING_ZX",
        "MISSING_MX2": "MISSING_MX2",
        "NOT_PARENT_SIGNED": "NOT_PARENT_SIGNED",
        "FORMULA_ONLY": "FORMULA_ONLY",
        "FAIL_CURRENT_CLAIM": "FAIL_CURRENT_CLAIM",
    }
    files: list[Path] = []
    for glob in ["*.md", "*.csv"]:
        files.extend(path for path in ROOT.rglob(glob) if "1854" not in path.name and "__pycache__" not in path.parts)
    files = sorted(set(files))
    rows: list[dict[str, Any]] = [
        {
            "scan_id": "SCAN1854_0_files_scanned",
            "pattern": "all_md_csv_excluding_1854",
            "hit_count": len(files),
            "sample_paths": ";".join(rel(path) for path in files[:8]),
            "interpretation": "scan scope for parent Hessian evidence",
            "valid_for_claim": False,
        }
    ]
    for scan_id, (label, pattern) in enumerate(patterns.items(), start=1):
        hit_paths: list[Path] = []
        for path in files:
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if pattern in text:
                hit_paths.append(path)
        rows.append(
            {
                "scan_id": f"SCAN1854_{scan_id}_{label.replace('^', '').replace('_', '')}",
                "pattern": pattern,
                "hit_count": len(hit_paths),
                "sample_paths": ";".join(rel(path) for path in hit_paths[:8]),
                "interpretation": "evidence found but must be audited for claim-grade ownership",
                "valid_for_claim": False,
            }
        )
    return rows


def build_rows_map() -> dict[str, list[dict[str, Any]]]:
    source_rows = [
        {
            "source_id": "SRC1854_0_1853_handoff",
            "source_path": source_path("1853-Y5-R2FR-canonical-X-normalization-and-range-gate-for-cg.md"),
            "needle": "NEXT1853_0_primary",
            "use": "selected parent Hessian extraction target",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1854_1_1036_parent_row",
            "source_path": source_path("1036-Y5-R10-parent-X-quadratic-action-and-beta-source-test-split.md"),
            "needle": "FAIL_CURRENT_CLAIM_PARENT_ROW_NOT_OWNED",
            "use": "prior parent finite-X row audit",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1854_2_1042_nohair",
            "source_path": source_path("1042-Y5-R10-sourcefree-positive-X-nohair-identity-or-alpha3-prior-first-fill.md"),
            "needle": "CONDITIONAL_THEOREM_DERIVED_FULL_CLAIM_BLOCKED",
            "use": "positive no-hair theorem remains conditional on Z/M/J/boundary inputs",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1854_3_1085_range",
            "source_path": source_path("1085-Y5-R10-WEP-range-owner-or-long-range-limit-theorem.md"),
            "needle": "MISSING_PARENT_HESSIAN_VALUES",
            "use": "range owner theorem failed due missing parent Hessian values",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1854_4_1847_hessian",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1847_PARENT_HESSIAN_AUDIT.csv"),
            "needle": "PHA1847_8_verdict",
            "use": "latest active parent Hessian ownership audit",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1854_5_1848_metric",
            "source_path": source_path("1848-Y5-R2FR-parent-metric-ZXfX2-beta-eigenvalue-or-source-zero-return.md"),
            "needle": "parent metric lock",
            "use": "parent metric/eigenvalue route remains unowned",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1854_6_1853_input_gate",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1853_ZX_MX2_INPUT_GATE.csv"),
            "needle": "ZMG1853_5_verdict",
            "use": "current Z_X/M_X^2 input gate",
            "status": "FOUND",
            "valid_for_claim": False,
        },
    ]

    candidate_rows = [
        {
            "candidate_id": "HCA1854_0_ZX_formula",
            "object": "Z_X",
            "best_evidence": "many formula/template rows define Z_X as kinetic Hessian coefficient",
            "claim_grade_evidence_found": False,
            "why_not_claim": "no parent-signed positive numeric/symbolic coefficient with units and same Xhat normalization",
            "status": "FORMULA_ONLY_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "candidate_id": "HCA1854_1_MX2_formula",
            "object": "M_X^2",
            "best_evidence": "many formula/template rows define M_X^2 as local Hessian curvature/mass gap",
            "claim_grade_evidence_found": False,
            "why_not_claim": "no parent-signed mass gap, zero-mass theorem, or eigenvalue extraction with units",
            "status": "FORMULA_ONLY_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "candidate_id": "HCA1854_2_lambda_relation",
            "object": "lambda_X",
            "best_evidence": "lambda_X=sqrt(Z_X/M_X^2) is repeatedly derived",
            "claim_grade_evidence_found": False,
            "why_not_claim": "relation is exact, but values and units for Z_X/M_X^2 are missing",
            "status": "RELATION_DERIVED_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "candidate_id": "HCA1854_3_massless_theorem",
            "object": "M_X^2=0 protected branch",
            "best_evidence": "massless/long-range route appears as a possible branch",
            "claim_grade_evidence_found": False,
            "why_not_claim": "no symmetry/no-pole theorem protects a zero mass while keeping local tests safe",
            "status": "MASSLESS_THEOREM_NOT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "candidate_id": "HCA1854_4_same_branch_lock",
            "object": "same-branch normalization",
            "best_evidence": "multiple ledgers demand one branch supplies Z_X, M_X^2, lambda_X, K_X and source charges",
            "claim_grade_evidence_found": False,
            "why_not_claim": "current rows still mix formula templates and missing source/coupling rows",
            "status": "SAME_BRANCH_LOCK_MISSING",
            "valid_for_claim": False,
        },
        {
            "candidate_id": "HCA1854_5_cross_Hessian",
            "object": "mixed Hessian/residual vector",
            "best_evidence": "cross-Hessian silence is listed as required",
            "claim_grade_evidence_found": False,
            "why_not_claim": "no block diagonalization or multi-component residual vector is parent-signed",
            "status": "MISSING_CROSS_HESSIAN_BLOCK",
            "valid_for_claim": False,
        },
        {
            "candidate_id": "HCA1854_6_verdict",
            "object": "Z_X/M_X^2 extraction",
            "best_evidence": "corpus contains the right contracts but no claim-grade inputs",
            "claim_grade_evidence_found": False,
            "why_not_claim": "extraction finds formulas and blockers, not owned coefficients",
            "status": "FAIL_CURRENT_CLAIM_PARENT_HESSIAN_INPUTS_NOT_EXTRACTED",
            "valid_for_claim": False,
        },
    ]

    required_clause_rows = [
        {
            "clause_id": "PAC1854_0_field_owner",
            "required_clause": "Declare one dimensionless parent field Xhat or quotient-normal coordinate e_X with fixed normalization.",
            "must_supply": "field_id;branch_id;definition;allowed redefinitions;source path",
            "why_required": "raw c_g, Z_X and M_X^2 are meaningless unless they refer to the same field coordinate",
            "current_status": "MISSING_PARENT_CLAUSE",
            "valid_for_claim": False,
        },
        {
            "clause_id": "PAC1854_1_quadratic_action",
            "required_clause": "S_parent contains 1/2 int sqrt(-g) M_Pl^2 [Z_X(q) (nabla Xhat)^2 + M_X^2(q) Xhat^2] with sign convention.",
            "must_supply": "Z_X;M_X2;units;sign convention;domain;source path",
            "why_required": "this is the only way to own N_X and lambda_X in the same branch",
            "current_status": "MISSING_PARENT_CLAUSE",
            "valid_for_claim": False,
        },
        {
            "clause_id": "PAC1854_2_hessian_extraction",
            "required_clause": "Z_X and M_X^2 are extracted as second-variation Hessian residues around the local GR/Newton branch.",
            "must_supply": "delta^2 S_parent/d(nabla Xhat)^2;delta^2 S_parent/dXhat^2;background;gauge fixing",
            "why_required": "prevents choosing range or normalization after seeing constraints",
            "current_status": "MISSING_EXTRACTION",
            "valid_for_claim": False,
        },
        {
            "clause_id": "PAC1854_3_cross_block",
            "required_clause": "Mixed Hessian terms with metric, matter, boundary/projector and memory variables are zero or included in a residual vector.",
            "must_supply": "cross-block proof or residual matrix entries",
            "why_required": "a one-component c_g bound is false if other components enter the same PPN/R10 channel",
            "current_status": "MISSING_BLOCK_DIAGONALIZATION",
            "valid_for_claim": False,
        },
        {
            "clause_id": "PAC1854_4_source_boundary",
            "required_clause": "J_X and boundary/support flux are theorem-zero or bounded in the same normalization.",
            "must_supply": "J_X;boundary_flux_X;support/domain terms;units;source paths",
            "why_required": "normalization/range alone do not recover GR if the X equation has an ordinary matter source",
            "current_status": "MISSING_SOURCE_BOUNDARY_LOCK",
            "valid_for_claim": False,
        },
        {
            "clause_id": "PAC1854_5_claim_rule",
            "required_clause": "No c_g/R10/PPN/local-GR claim until PAC1854_0 through PAC1854_4 are signed or source-bounded.",
            "must_supply": "claim gate with all required inputs present and valid_for_claim=true",
            "why_required": "keeps the theory from passing tests by coordinate rescaling or branch mixing",
            "current_status": "GUARDRAIL_ACTIVE",
            "valid_for_claim": False,
        },
    ]

    extraction_rows = [
        {
            "result_id": "EXT1854_0_ZX",
            "quantity": "Z_X",
            "extracted_value": "MISSING_ZX",
            "extraction_status": "NOT_EXTRACTED",
            "evidence": "formula/template rows only",
            "effect_on_cg": "N_X=1/sqrt(Z_X) remains numeric-missing",
            "valid_for_claim": False,
        },
        {
            "result_id": "EXT1854_1_MX2",
            "quantity": "M_X^2",
            "extracted_value": "MISSING_MX2",
            "extraction_status": "NOT_EXTRACTED",
            "evidence": "formula/template rows only",
            "effect_on_cg": "lambda_X and PPN/R10 range class remain missing",
            "valid_for_claim": False,
        },
        {
            "result_id": "EXT1854_2_lambda",
            "quantity": "lambda_X",
            "extracted_value": "sqrt(Z_X/M_X^2)",
            "extraction_status": "RELATION_ONLY",
            "evidence": "1847/1085 relation",
            "effect_on_cg": "cannot decide Cassini vs R10 vs orbital routing",
            "valid_for_claim": False,
        },
        {
            "result_id": "EXT1854_3_NX",
            "quantity": "N_X",
            "extracted_value": "1/sqrt(Z_X)",
            "extraction_status": "RELATION_ONLY",
            "evidence": "1853 canonical normalization",
            "effect_on_cg": "raw c_g remains unbounded; only c_g/sqrt(Z_X) is meaningful",
            "valid_for_claim": False,
        },
        {
            "result_id": "EXT1854_4_cg_bound",
            "quantity": "c_g",
            "extracted_value": "MISSING_ZX_TAU_PPN_RANGE_TRANSFER",
            "extraction_status": "CLAIM_BLOCKED",
            "evidence": "1852/1853 conditional proxy only",
            "effect_on_cg": "no direct Cassini c_g claim",
            "valid_for_claim": False,
        },
        {
            "result_id": "EXT1854_5_verdict",
            "quantity": "parent Hessian input extraction",
            "extracted_value": "NO_CLAIM_GRADE_ZX_OR_MX2_FOUND",
            "extraction_status": "FAIL_CURRENT_CLAIM",
            "evidence": "current corpus scan and source register",
            "effect_on_cg": "next work must add/sign parent action clause or keep c_g source-only",
            "valid_for_claim": False,
        },
    ]

    claim_rows = [
        {
            "gate_id": "CG1854_0_formula_contracts",
            "claim": "the needed Z_X/M_X^2 contracts are known",
            "gate_pass": True,
            "reason": "corpus has repeated formulas for Hessian, range and normalization",
            "claim_allowed": True,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1854_1_ZX_owned",
            "claim": "Z_X is parent-owned and positive",
            "gate_pass": False,
            "reason": "no claim-grade Z_X value/sign/units/source path found",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1854_2_MX2_owned",
            "claim": "M_X^2 or a protected massless theorem is parent-owned",
            "gate_pass": False,
            "reason": "no claim-grade mass gap, range value, or zero-mass protection found",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1854_3_cg_bound",
            "claim": "Cassini/R10 bounds can score c_g now",
            "gate_pass": False,
            "reason": "Z_X/M_X^2 extraction failed, so normalization/range are still missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1854_4_local_GR",
            "claim": "local GR/Newton reduction is derived",
            "gate_pass": False,
            "reason": "parent Hessian/source/boundary/coupling gates are still unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC1854_0_scan_result",
            "decision": "The current corpus has the right Hessian formulas but not the required parent-owned coefficients.",
            "because": "scan and source register find repeated MISSING/FORMULA_ONLY/NOT_PARENT_SIGNED statuses for Z_X and M_X^2.",
            "next_action": "do not score c_g; write or derive the parent X-sector action clause",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1854_1_no_rescaling_win",
            "decision": "Raw c_g remains unscoreable.",
            "because": "without Z_X, any raw c_g value can be changed by field normalization.",
            "next_action": "only compare c_g/sqrt(Z_X) after Z_X is parent-owned",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1854_2_best_next",
            "decision": "Next target is the minimal parent X-sector action clause.",
            "because": "extraction from existing rows failed; the theory needs the exact clause that would make the branch derivable.",
            "next_action": "1855-Y5-R2FR-minimal-parent-X-sector-action-clause-or-demotion.md",
            "valid_for_claim": False,
        },
    ]

    next_rows = [
        {
            "route_id": "NEXT1854_0_primary",
            "next_target": "1855-Y5-R2FR-minimal-parent-X-sector-action-clause-or-demotion.md",
            "script": "scripts/Y5_R2FR_minimal_parent_X_sector_action_clause_or_demotion_1855.py",
            "objective": "construct the smallest parent action clause that signs Xhat, Z_X, M_X^2, cross-Hessian, source and boundary requirements; if it cannot be justified, demote c_g finite/local branch to explicit closure-only",
            "selection_status": "selected",
            "success_condition": "a minimal parent X-sector clause is internally consistent and lists every assumption, or the finite c_g branch is demoted without local-GR claim",
        },
        {
            "route_id": "NEXT1854_1_parallel",
            "next_target": "1855b-Y5-R2FR-PPN-residual-vector-no-cancellation-envelope.md",
            "script": "scripts/Y5_R2FR_PPN_residual_vector_no_cancellation_envelope_1855b.py",
            "objective": "derive the PPN residual vector if one-field c_g isolation remains unavailable",
            "selection_status": "held",
            "success_condition": "PPN constraints become a multi-component absolute envelope",
        },
    ]

    return {
        "source_register": source_rows,
        "scan_summary": scan_corpus(),
        "candidate_audit": candidate_rows,
        "required_clause": required_clause_rows,
        "extraction_result": extraction_rows,
        "claim_gate": claim_rows,
        "decision": decision_rows,
        "next_target": next_rows,
    }


def copy_outputs(include_validation: bool = False) -> None:
    keys = list(OUTPUTS)
    if not include_validation:
        keys = [key for key in keys if key != "validation"]
    for key in keys:
        src = OUTPUTS[key]
        if not src.exists():
            continue
        for dst_dir in [MICROSCOPE_RESIDUALS, QUARANTINE]:
            shutil.copy2(src, dst_dir / src.name)
        shutil.copy2(src, RAB_QUEUE / f"JR1854_{src.name}")


def check_sources(source_rows: list[dict[str, Any]]) -> tuple[bool, str]:
    missing: list[str] = []
    for row in source_rows:
        path = ROOT / str(row["source_path"])
        if not path.exists():
            missing.append(str(row["source_path"]))
    return not missing, "missing: " + "; ".join(missing) if missing else "all cited source paths exist"


def check_needles(source_rows: list[dict[str, Any]]) -> tuple[bool, str]:
    missing: list[str] = []
    for row in source_rows:
        path = ROOT / str(row["source_path"])
        needle = str(row["needle"])
        if path.exists() and needle not in path.read_text(encoding="utf-8", errors="ignore"):
            missing.append(f"{row['source_path']}::{needle}")
    return not missing, "missing: " + "; ".join(missing) if missing else "all cited source needles are present"


def check_csv_parse() -> tuple[bool, str]:
    malformed: list[str] = []
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        try:
            read_csv(path)
        except Exception as exc:  # pragma: no cover
            malformed.append(f"{path.name}: {exc}")
    return not malformed, "malformed: " + "; ".join(malformed) if malformed else "all generated 1854 CSVs parse"


def check_branch_copies() -> tuple[bool, str]:
    missing: list[str] = []
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        expected = [
            MICROSCOPE_RESIDUALS / path.name,
            QUARANTINE / path.name,
            RAB_QUEUE / f"JR1854_{path.name}",
        ]
        for item in expected:
            if not item.exists():
                missing.append(str(item))
    return not missing, "missing copies: " + "; ".join(missing) if missing else "branch/quarantine/queue copies exist"


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = []
    ok, detail = check_sources(rows_map["source_register"])
    checks.append(("VAL1854_0_sources_exist", ok, detail))
    ok, detail = check_needles(rows_map["source_register"])
    checks.append(("VAL1854_1_needles_present", ok, detail))
    checks.append(
        (
            "VAL1854_2_scan_has_hits",
            any(row["pattern"] == "Z_X" and int(row["hit_count"]) > 0 for row in rows_map["scan_summary"])
            and any(row["pattern"] == "MISSING_PARENT_INPUT" and int(row["hit_count"]) > 0 for row in rows_map["scan_summary"]),
            "corpus scan found both Hessian formulas and missing-input ledgers",
        )
    )
    checks.append(
        (
            "VAL1854_3_candidate_audit_blocks",
            any(row["candidate_id"] == "HCA1854_6_verdict" and row["status"] == "FAIL_CURRENT_CLAIM_PARENT_HESSIAN_INPUTS_NOT_EXTRACTED" for row in rows_map["candidate_audit"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["candidate_audit"]),
            "candidate audit refuses parent Hessian extraction claim",
        )
    )
    checks.append(
        (
            "VAL1854_4_required_clause_complete",
            len(rows_map["required_clause"]) >= 6
            and any(row["clause_id"] == "PAC1854_5_claim_rule" and row["current_status"] == "GUARDRAIL_ACTIVE" for row in rows_map["required_clause"]),
            "required parent action clause rows are present",
        )
    )
    checks.append(
        (
            "VAL1854_5_extraction_result_blocks",
            any(row["result_id"] == "EXT1854_5_verdict" and row["extraction_status"] == "FAIL_CURRENT_CLAIM" for row in rows_map["extraction_result"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["extraction_result"]),
            "extraction result blocks c_g scoring",
        )
    )
    checks.append(
        (
            "VAL1854_6_claim_gates_safe",
            any(row["gate_id"] == "CG1854_0_formula_contracts" and boolish(row["gate_pass"]) for row in rows_map["claim_gate"])
            and any(row["gate_id"] == "CG1854_3_cg_bound" and not boolish(row["gate_pass"]) for row in rows_map["claim_gate"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["claim_gate"]),
            "formula contracts pass but c_g/local claims do not",
        )
    )
    checks.append(
        (
            "VAL1854_7_next_target_selected",
            any(row["route_id"] == "NEXT1854_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        )
    )
    checks.append(
        (
            "VAL1854_8_no_claim_flags",
            all(not boolish(row.get("valid_for_claim", False)) for rows in rows_map.values() for row in rows),
            "no valid_for_claim flags are true",
        )
    )
    checks.append(
        (
            "VAL1854_9_missing_rows_nonclaim",
            all(
                not boolish(row.get("valid_for_claim", False))
                for rows in rows_map.values()
                for row in rows
                if "MISSING_" in " ".join(str(value) for value in row.values())
            ),
            "MISSING_* rows stay nonclaim",
        )
    )
    ok, detail = check_csv_parse()
    checks.append(("VAL1854_10_csv_parse", ok, detail))
    ok, detail = check_branch_copies()
    checks.append(("VAL1854_11_branch_copies", ok, detail))
    pycache_path = ROOT / "scripts" / "__pycache__"
    checks.append(("VAL1854_12_pycache_absent", not pycache_path.exists(), "scripts __pycache__ absent"))
    formalization_outputs = list(FORMALIZATION.rglob("*1854*")) if FORMALIZATION.exists() else []
    checks.append(("VAL1854_13_formalization_untouched", not formalization_outputs, "no 1854 outputs found under formalization-workbench"))
    overall = all(result for _, result, _ in checks)
    validation_rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    validation_rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1854_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1854 parent Hessian input extraction for Z_X/M_X2",
        }
    )
    return validation_rows


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    lines = [header, sep]
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    return "\n".join(
        [
            "# 1854: Parent Hessian Input Extraction For Z_X/M_X2",
            "",
            "**Current verdict:** extraction fails in the useful way. The corpus contains many correct Hessian/range formulas, but no claim-grade parent-owned `Z_X` or `M_X^2` with units, sign, same-branch normalization, cross-Hessian handling, source current and boundary lock. So `lambda_X`, `N_X`, raw `c_g`, R10, PPN and local-GR claims remain blocked.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_path", "needle", "use", "status", "valid_for_claim"]),
            "",
            "## Corpus Scan Summary",
            markdown_table(rows_map["scan_summary"], ["scan_id", "pattern", "hit_count", "sample_paths", "interpretation", "valid_for_claim"]),
            "",
            "## Hessian Candidate Audit",
            markdown_table(rows_map["candidate_audit"], ["candidate_id", "object", "best_evidence", "claim_grade_evidence_found", "why_not_claim", "status", "valid_for_claim"]),
            "",
            "## Parent Action Clause Required",
            markdown_table(rows_map["required_clause"], ["clause_id", "required_clause", "must_supply", "why_required", "current_status", "valid_for_claim"]),
            "",
            "## Z_X/M_X2 Extraction Result",
            markdown_table(rows_map["extraction_result"], ["result_id", "quantity", "extracted_value", "extraction_status", "evidence", "effect_on_cg", "valid_for_claim"]),
            "",
            "## Claim Gates",
            markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "",
            "## Decisions",
            markdown_table(rows_map["decision"], ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This is the unpleasant but important answer: the coefficients are not hiding in the current private branch. The next honest move is not another bound table; it is to write the minimal parent X-sector action clause and decide whether it is truly part of MTS or only a closure assumption.",
            "",
        ]
    )


def main() -> None:
    ensure_dirs()
    rows_map = build_rows_map()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs(include_validation=False)
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    copy_outputs(include_validation=True)
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1854 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()

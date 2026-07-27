from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1544-Y5-Cqm-zero-theorem-or-finite-provenance-runner.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1543_doc": ROOT / "1543-Y5-Cqm-source-norm-local-projection-pack.md",
    "1543_validation": OUT / "P8_Y5_BRR545_1543_VALIDATION.csv",
    "1543_inputs": OUT / "P8_Y5_PARENT_QLOC_1543_FINITE_INPUT_PROVENANCE_PACK.csv",
    "1543_arenas": OUT / "P8_Y5_PARENT_QLOC_1543_ARENA_PROJECTION_PACK.csv",
    "1543_runner": OUT / "P8_Y5_PARENT_QLOC_1543_PROJECTION_RUNNER_NONCLAIM.csv",
    "1542_qdef": OUT / "P8_Y5_PARENT_QLOC_1542_Q_DEFINITION_AUDIT.csv",
    "1542_vmdef": OUT / "P8_Y5_PARENT_QLOC_1542_VM_DEFINITION_AUDIT.csv",
    "1542_cqm": OUT / "P8_Y5_PARENT_QLOC_1542_CQM_SOURCE_PACK_NONCLAIM.csv",
    "1541_qmap": OUT / "P8_Y5_PARENT_QLOC_1541_QMAP_CANDIDATE_LEDGER.csv",
    "1541_vgen": OUT / "P8_Y5_PARENT_QLOC_1541_VERTICAL_GENERATOR_AUDIT.csv",
    "1541_kernel": OUT / "P8_Y5_PARENT_QLOC_1541_KERNEL_TEST.csv",
    "1541_coupling": OUT / "P8_Y5_PARENT_QLOC_1541_DQVM_FINITE_COUPLING_ROW_NONCLAIM.csv",
    "1540_chain": OUT / "P8_Y5_PARENT_QLOC_1540_VARIATION_CHAIN_AUDIT.csv",
    "cg_no_shadow": ROOT / "1029-Y5-R10-cg-no-shadow-frame-theorem-or-first-numeric-coupling-row.md",
    "single_public_metric": ROOT / "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md",
    "local_bound_claims": LOCAL_BOUNDS / "local_bound_claims.csv",
    "r10_curve_candidate": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1544_SOURCE_REGISTER.csv"
CQM_ZERO_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1544_CQM_ZERO_THEOREM_AUDIT.csv"
CQM_PROVENANCE = OUT / "P8_Y5_PARENT_QLOC_1544_CQM_FINITE_PROVENANCE_REQUIREMENTS.csv"
CQM_DRY_RUNNER = OUT / "P8_Y5_PARENT_QLOC_1544_CQM_DRY_RUNNER_NONCLAIM.csv"
LOCAL_PROJECTION = OUT / "P8_Y5_PARENT_QLOC_1544_LOCAL_PROJECTION_CONTRACT.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1544_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1544_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1544_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1544_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1544"
QUAR_ZERO = QUARANTINE / "CQM_ZERO_THEOREM_AUDIT_NONCLAIM.csv"
QUAR_PROV = QUARANTINE / "CQM_FINITE_PROVENANCE_REQUIREMENTS_NONCLAIM.csv"
QUAR_RUNNER = QUARANTINE / "CQM_DRY_RUNNER_NONCLAIM.csv"
QUAR_PROJ = QUARANTINE / "LOCAL_PROJECTION_CONTRACT_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "DECISION_NONCLAIM.csv"
BRANCH_ZERO = BRANCH_RESIDUALS / "Cqm_zero_theorem_audit_nonclaim_1544.csv"
BRANCH_PROV = BRANCH_RESIDUALS / "Cqm_finite_provenance_requirements_nonclaim_1544.csv"
BRANCH_RUNNER = BRANCH_RESIDUALS / "Cqm_dry_runner_nonclaim_1544.csv"
BRANCH_PROJ = BRANCH_RESIDUALS / "Cqm_local_projection_contract_nonclaim_1544.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "Cqm_decision_nonclaim_1544.csv"


def flags() -> dict[str, bool]:
    return {
        "theorem_zero_adopted": False,
        "numeric_value_present": False,
        "source_backed": False,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def source_list(*keys: str) -> str:
    return "; ".join(rel(SOURCE_FILES[key]) for key in keys)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    claim_keys = [
        "theorem_zero_adopted",
        "numeric_value_present",
        "source_backed",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "accepted_for_scoring",
        "passes_for_claim",
    ]
    for path in paths:
        for row in read_csv(path):
            for key in claim_keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def source_register_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "source_id": f"SRC1544_{index}_{key}",
            "source_path": rel(path),
            "exists": path.exists(),
            "purpose": "input evidence for C_qm zero theorem or finite provenance runner",
            **flags(),
        }
        for index, (key, path) in enumerate(SOURCE_FILES.items())
    ]


def zero_audit_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "ZERO1544_0_definition",
            "C_qm definition",
            "C_qm := ||DObs_e[Dq[v_m]]||_loc",
            "definition only",
            "DEFINITION",
            "none",
        ),
        (
            "ZERO1544_1_parent_q",
            "parent q_loc theorem",
            "q_loc is parent-owned before tests and not post-hoc quotient deletion",
            "required for Dq[v_m] to be meaningful",
            "UNSIGNED",
            "1542 rejects illegal q deletion but does not derive q_loc",
        ),
        (
            "ZERO1544_2_vertical_generator",
            "v_m kernel theorem",
            "v_m is a parent null/gauge/representative direction and Dq[v_m]=0",
            "would kill the quotient derivative",
            "UNSIGNED",
            "1541/1542 leave v_m field-by-field action missing",
        ),
        (
            "ZERO1544_3_observed_functor",
            "observed coframe descent",
            "e_obs=Obs_e(q_loc(Phi)) and DObs_e[0]=0 with no independent shadow frame",
            "would kill visible metric/coframe response",
            "UNSIGNED",
            "1029/1030 isolate this as a conditional theorem, not parent-signed",
        ),
        (
            "ZERO1544_4_norm_normalization",
            "local norm and v_m normalization",
            "the norm used for C_qm is declared and cannot hide coefficient size in field units",
            "needed for finite or zero interpretation",
            "MISSING",
            "no source-backed local norm/v_m normalization row exists",
        ),
        (
            "ZERO1544_5_shortcut_rejections",
            "shortcut rejection",
            "covariance, WEP silence, and Ward identities alone do not imply C_qm=0",
            "prevents common-frame and field-relabel cheats",
            "REJECTED_SHORTCUTS",
            "1030 already shows these routes fail for c_g/single-public-metric",
        ),
        (
            "ZERO1544_6_verdict",
            "C_qm=0 verdict",
            "all zero clauses must close together",
            "C_qm remains nonzero/unknown for work purposes",
            "THEOREM_ZERO_NOT_CLOSED",
            "move to finite provenance unless a future parent action signs q/v_m/Obs_e",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "zero_id": zero_id,
            "clause": clause,
            "required_statement": statement,
            "effect_if_signed": effect,
            "current_status": status,
            "reason": reason,
            "source_paths": source_list("1543_inputs", "1542_qdef", "1542_vmdef", "1541_kernel", "cg_no_shadow", "single_public_metric"),
            **flags(),
        }
        for zero_id, clause, statement, effect, status, reason in rows
    ]


def provenance_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "PROV1544_0_value",
            "candidate_value",
            "finite numeric value or interval for C_qm",
            "MISSING_NUMERIC_VALUE_OR_INTERVAL",
            "must be nonnegative and tied to the declared v_m normalization",
        ),
        (
            "PROV1544_1_units",
            "units",
            "units/dimensions of C_qm after v_m normalization",
            "MISSING_UNITS",
            "dimension may be one over memory-field unit unless v_m is dimensionless",
        ),
        (
            "PROV1544_2_norm",
            "local_norm_definition",
            "definition of ||DObs_e[Dq[v_m]]||_loc and source dual pairing",
            "MISSING_NORM_DEFINITION",
            "must match the T_source_norm and S_cg_norm spaces",
        ),
        (
            "PROV1544_3_source",
            "source_path_and_row",
            "existing source file and row/equation that derives or bounds C_qm",
            "MISSING_SOURCE_PATH_AND_ROW",
            "no placeholder, inference-only, or chat-memory value may score",
        ),
        (
            "PROV1544_4_derivation_status",
            "derivation_status",
            "parent-derived, externally bounded, prior-only, or closure-only label",
            "MISSING_DERIVATION_STATUS",
            "closure-only rows remain valid_for_claim=false",
        ),
        (
            "PROV1544_5_projection_contract",
            "local_projection_contract",
            "how C_qm enters S_geom_m, N_pair, and arena projections",
            "MISSING_PROJECTION_CONTRACT",
            "must connect to 1543 R10/PPN/clock/orbital rows before testing",
        ),
        (
            "PROV1544_6_no_cancellation",
            "absolute_envelope_guard",
            "C_qm contribution cannot be canceled by unknown direct/source/boundary terms",
            "GUARD_ACTIVE",
            "absolute envelope is required in S_cg_norm",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "provenance_id": provenance_id,
            "required_field": field,
            "required_content": content,
            "current_status": status,
            "promotion_rule": rule,
            "source_paths": source_list("1543_inputs", "1543_arenas", "1541_coupling"),
            **flags(),
        }
        for provenance_id, field, content, status, rule in rows
    ]


def dry_runner_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DRY1544_0_zero_branch",
            "C_qm=0 theorem branch",
            "REJECTED_MISSING_PARENT_THEOREM",
            "missing parent q_loc, v_m kernel, observed coframe/no-shadow-frame theorem, norm normalization",
        ),
        (
            "DRY1544_1_finite_branch",
            "finite C_qm branch",
            "REJECTED_MISSING_PROVENANCE",
            "missing value, units, norm, source path, row id, derivation status, and projection contract",
        ),
        (
            "DRY1544_2_R10_use",
            "R10 use of C_qm",
            "REJECTED_NOT_SCORE_READY",
            "C_qm and Pi_R10/N_pair are missing; bound curve is nonclaim review candidate",
        ),
        (
            "DRY1544_3_PPN_clock_orbital_use",
            "PPN/clock/orbital use of C_qm",
            "REJECTED_NOT_SCORE_READY",
            "C_qm, N_lock, and arena response matrices are missing",
        ),
        (
            "DRY1544_4_local_GR_use",
            "local GR/Newton claim",
            "REJECTED_BLOCKED_NO_CLAIM",
            "neither exact q-kernel nor finite local residual bound closes",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "dryrun_id": dryrun_id,
            "branch": branch,
            "runner_result": result,
            "failure_reasons": reasons,
            **flags(),
        }
        for dryrun_id, branch, result, reasons in rows
    ]


def local_projection_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "LPC1544_0_source_geometry",
            "stress-mediated source term",
            "S_geom_m <= 1/2*T_source_norm*C_qm",
            "C_qm; T_source_norm; local dual norm",
            "BLOCKED_INPUTS_MISSING",
        ),
        (
            "LPC1544_1_Scg_envelope",
            "source coupling envelope",
            "S_cg_norm <= 1/2*T_source_norm*C_qm + S_direct_m + S_source_norm_extra + S_boundary_m",
            "C_qm branch plus direct/source/boundary inputs",
            "BLOCKED_INPUTS_MISSING",
        ),
        (
            "LPC1544_2_Npair",
            "first-pair local lock insertion",
            "N_pair <= U_B_max*S_cg_norm + C_inner*|Q_m^H|",
            "S_cg_norm; U_B_max; C_inner; Q_m^H",
            "BLOCKED_INPUTS_MISSING",
        ),
        (
            "LPC1544_3_arena_projection",
            "R10/PPN/clock/orbital projection",
            "observable residual <= Pi_arena*N_pair or Pi_arena*N_lock",
            "arena-specific Pi matrices and bound anchors",
            "BLOCKED_PROJECTIONS_MISSING",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "projection_id": projection_id,
            "projection": projection,
            "formula": formula,
            "required_inputs": inputs,
            "current_status": status,
            "source_paths": source_list("1543_inputs", "1543_arenas", "1543_runner"),
            **flags(),
        }
        for projection_id, projection, formula, inputs, status in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1544_0_zero_audit", "C_qm zero theorem audited", "PASS_NONCLAIM", "all zero clauses listed and current theorem rejected"),
        ("GATE1544_1_zero_claim", "C_qm=0", "BLOCKED", "parent q/v_m/Obs_e theorem and norm normalization missing"),
        ("GATE1544_2_finite_provenance", "finite C_qm score-ready", "BLOCKED", "numeric value/source/units/norm/projection missing"),
        ("GATE1544_3_R10_PPN_use", "local arena use of C_qm", "BLOCKED", "C_qm and arena projections missing"),
        ("GATE1544_4_local_GR", "local GR/Newton/PPN claim", "BLOCKED_NO_CLAIM", "C_qm route neither theorem-zero nor finite-bounded"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for gate_id, claim, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC1544_0_zero",
            "Do not claim C_qm=0.",
            "ZERO_THEOREM_NOT_CLOSED",
            "the exact theorem still lacks parent q, v_m kernel, observed coframe/no-shadow-frame, and norm normalization",
        ),
        (
            "DEC1544_1_finite",
            "Require finite C_qm provenance before scoring.",
            "FINITE_PROVENANCE_GATE_INSTALLED",
            "C_qm is allowed as a residual only with value, units, source row, derivation status, and projection contract",
        ),
        (
            "DEC1544_2_no_claim",
            "Keep all local claims blocked.",
            "CLAIM_BLOCKED",
            "dry runner rejects zero, finite, R10, PPN, clock, orbital, and local-GR uses",
        ),
        (
            "DEC1544_3_next",
            "Next target is the source norm/direct residual pack.",
            "NEXT_1545_SOURCE_NORM_DIRECT_RESIDUALS",
            "while C_qm waits for parent proof/provenance, the remaining terms can be made equally strict",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "result": result,
            "rationale": rationale,
            **flags(),
        }
        for decision_id, decision, result, rationale in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1544_0_1545",
            "next_target": "1545-Y5-source-norm-and-direct-memory-residual-provenance-pack.md",
            "script": "scripts/Y5_source_norm_and_direct_memory_residual_provenance_pack.py",
            "objective": "install provenance gates for T_source_norm, S_direct_m, S_source_norm_extra, and S_boundary_m so the full S_cg_norm envelope is source-ready even while C_qm remains unproved",
            "do_not": "do not insert placeholder values; do not cancel terms; do not claim local GR or arena passes",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (CQM_ZERO_AUDIT, QUAR_ZERO),
        (CQM_PROVENANCE, QUAR_PROV),
        (CQM_DRY_RUNNER, QUAR_RUNNER),
        (LOCAL_PROJECTION, QUAR_PROJ),
        (DECISION, QUAR_DECISION),
        (CQM_ZERO_AUDIT, BRANCH_ZERO),
        (CQM_PROVENANCE, BRANCH_PROV),
        (CQM_DRY_RUNNER, BRANCH_RUNNER),
        (LOCAL_PROJECTION, BRANCH_PROJ),
        (DECISION, BRANCH_DECISION),
    ]
    for source, destination in copies:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_modified_count_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= START_TS)


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    zero = read_csv(CQM_ZERO_AUDIT)
    provenance = read_csv(CQM_PROVENANCE)
    dry = read_csv(CQM_DRY_RUNNER)
    projection = read_csv(LOCAL_PROJECTION)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    required_provenance = {
        "candidate_value",
        "units",
        "local_norm_definition",
        "source_path_and_row",
        "derivation_status",
        "local_projection_contract",
    }
    provenance_fields = {row["required_field"] for row in provenance}
    checks = [
        ("VAL1544_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1544 source paths exist"),
        ("VAL1544_1_zero_verdict", any(row["zero_id"] == "ZERO1544_6_verdict" and row["current_status"] == "THEOREM_ZERO_NOT_CLOSED" for row in zero), "C_qm zero theorem not closed"),
        ("VAL1544_2_shortcuts_rejected", any(row["zero_id"] == "ZERO1544_5_shortcut_rejections" and row["current_status"] == "REJECTED_SHORTCUTS" for row in zero), "WEP/covariance/Ward shortcuts rejected"),
        ("VAL1544_3_provenance_fields", required_provenance.issubset(provenance_fields), "finite C_qm provenance requirements complete"),
        ("VAL1544_4_dry_runner_rejects", all(row["runner_result"].startswith("REJECTED") for row in dry), "dry runner rejects all current C_qm uses"),
        ("VAL1544_5_projection_contract", any(row["projection_id"] == "LPC1544_0_source_geometry" and "C_qm" in row["formula"] for row in projection), "local projection contract includes C_qm stress term"),
        ("VAL1544_6_claim_gates_block", any(row["gate_id"] == "GATE1544_4_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates), "local GR claim remains blocked"),
        ("VAL1544_7_decision_next", any(row["result"] == "NEXT_1545_SOURCE_NORM_DIRECT_RESIDUALS" for row in decisions), "decision selects source norm/direct residual provenance next"),
        ("VAL1544_8_next_target", any("1545-Y5-source-norm" in row["next_target"] for row in next_rows), "next target is source norm and direct memory residual provenance pack"),
        ("VAL1544_9_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1544 CSVs parse cleanly"),
        ("VAL1544_10_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1544_11_branch_copies", all(path.exists() for path in [QUAR_ZERO, QUAR_PROV, QUAR_RUNNER, QUAR_PROJ, QUAR_DECISION, BRANCH_ZERO, BRANCH_PROV, BRANCH_RUNNER, BRANCH_PROJ, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1544_12_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1544_13_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1544_14_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1544 refuses C_qm=0 without parent theorem, installs finite C_qm provenance requirements, rejects current scoring, keeps claims blocked, and selects source-norm/direct residual provenance next"
            if overall
            else "1544 validation failed; inspect failed rows before continuing",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    output = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        output.append(
            "| "
            + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns)
            + " |"
        )
    return "\n".join(output)


def write_doc(
    sources: list[dict[str, Any]],
    zero: list[dict[str, Any]],
    provenance: list[dict[str, Any]],
    dry: list[dict[str, Any]],
    projection: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1544 - C_qm Zero Theorem or Finite Provenance Runner",
                "",
                "## Verdict",
                "- `C_qm=0` is not proved: it needs parent `q_loc`, a true `v_m` kernel generator, observed-coframe/no-shadow-frame descent, and a declared local norm.",
                "- The usual shortcut proofs are explicitly rejected: covariance, WEP silence, and Ward identities do not force `C_qm=0`.",
                "- Finite `C_qm` is allowed only as a provenance-checked residual with value/interval, units, norm, source path, source row, derivation status, and projection contract.",
                "- The dry runner rejects current zero, finite, R10, PPN, clock, orbital, and local-GR uses.",
                "- No local GR/Newton/PPN/R10/clock/orbital claim is promoted.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "purpose"]),
                "",
                "## C_qm Zero Theorem Audit",
                md_table(zero, ["zero_id", "clause", "required_statement", "effect_if_signed", "current_status", "reason"]),
                "",
                "## Finite C_qm Provenance Requirements",
                md_table(provenance, ["provenance_id", "required_field", "required_content", "current_status", "promotion_rule"]),
                "",
                "## Dry Runner",
                md_table(dry, ["dryrun_id", "branch", "runner_result", "failure_reasons"]),
                "",
                "## Local Projection Contract",
                md_table(projection, ["projection_id", "projection", "formula", "required_inputs", "current_status"]),
                "",
                "## Claim Gates",
                md_table(gates, ["gate_id", "claim", "status", "reason"]),
                "",
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "result", "rationale"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_id", "next_target", "script", "objective", "do_not"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    sources = source_register_rows()
    zero = zero_audit_rows()
    provenance = provenance_rows()
    dry = dry_runner_rows()
    projection = local_projection_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(CQM_ZERO_AUDIT, zero)
    write_csv(CQM_PROVENANCE, provenance)
    write_csv(CQM_DRY_RUNNER, dry)
    write_csv(LOCAL_PROJECTION, projection)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        CQM_ZERO_AUDIT,
        CQM_PROVENANCE,
        CQM_DRY_RUNNER,
        LOCAL_PROJECTION,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, zero, provenance, dry, projection, gates, decisions, validation, next_rows)


if __name__ == "__main__":
    main()

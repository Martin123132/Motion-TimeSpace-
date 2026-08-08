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
DOC = ROOT / "1543-Y5-Cqm-source-norm-local-projection-pack.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1542_doc": ROOT / "1542-Y5-q-definition-or-Dqvm-coupling-coefficient-source-pack.md",
    "1542_validation": OUT / "P8_Y5_BRR545_1542_VALIDATION.csv",
    "1542_cqm": OUT / "P8_Y5_PARENT_QLOC_1542_CQM_SOURCE_PACK_NONCLAIM.csv",
    "1542_scg": OUT / "P8_Y5_PARENT_QLOC_1542_SCG_RUNNER_NONCLAIM.csv",
    "1541_coupling": OUT / "P8_Y5_PARENT_QLOC_1541_DQVM_FINITE_COUPLING_ROW_NONCLAIM.csv",
    "1540_chain": OUT / "P8_Y5_PARENT_QLOC_1540_VARIATION_CHAIN_AUDIT.csv",
    "1539_inputs": OUT / "P8_Y5_PARENT_QLOC_1539_FIRST_PAIR_INPUT_ACQUISITION_LEDGER.csv",
    "local_bound_claims": LOCAL_BOUNDS / "local_bound_claims.csv",
    "r10_curve_candidate": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
    "r10_runner": ROOT / "scripts" / "R10_alpha_lambda_bound_prediction_runner.py",
    "source_current": OUT / "P8_source_current_Ward_universality_CONTRACT.csv",
    "source_normalization_owner": OUT / "P8_Y5_SOURCE_NORMALIZATION_OWNER_THEOREM.csv",
    "source_measure_flux": OUT / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv",
    "boundary_certificate": OUT / "P8_Y5_PARENT_QLOC_1529_BOUNDARY_CERTIFICATE_AUDIT.csv",
    "cg_no_shadow": ROOT / "1029-Y5-R10-cg-no-shadow-frame-theorem-or-first-numeric-coupling-row.md",
    "single_public_metric": ROOT / "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md",
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1543_SOURCE_REGISTER.csv"
FINITE_INPUTS = OUT / "P8_Y5_PARENT_QLOC_1543_FINITE_INPUT_PROVENANCE_PACK.csv"
ARENA_PROJECTIONS = OUT / "P8_Y5_PARENT_QLOC_1543_ARENA_PROJECTION_PACK.csv"
BOUND_ANCHORS = OUT / "P8_Y5_PARENT_QLOC_1543_BOUND_ANCHOR_LINKS_NONCLAIM.csv"
PROJECTION_RUNNER = OUT / "P8_Y5_PARENT_QLOC_1543_PROJECTION_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1543_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1543_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1543_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1543_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1543"
QUAR_INPUTS = QUARANTINE / "FINITE_INPUT_PROVENANCE_PACK_NONCLAIM.csv"
QUAR_PROJ = QUARANTINE / "ARENA_PROJECTION_PACK_NONCLAIM.csv"
QUAR_BOUNDS = QUARANTINE / "BOUND_ANCHOR_LINKS_NONCLAIM.csv"
QUAR_RUNNER = QUARANTINE / "PROJECTION_RUNNER_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "DECISION_NONCLAIM.csv"
BRANCH_INPUTS = BRANCH_RESIDUALS / "Cqm_finite_input_provenance_pack_nonclaim_1543.csv"
BRANCH_PROJ = BRANCH_RESIDUALS / "Cqm_arena_projection_pack_nonclaim_1543.csv"
BRANCH_BOUNDS = BRANCH_RESIDUALS / "Cqm_bound_anchor_links_nonclaim_1543.csv"
BRANCH_RUNNER = BRANCH_RESIDUALS / "Cqm_projection_runner_nonclaim_1543.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "Cqm_projection_decision_nonclaim_1543.csv"


def flags() -> dict[str, bool]:
    return {
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
            "source_id": f"SRC1543_{index}_{key}",
            "source_path": rel(path),
            "exists": path.exists(),
            "purpose": "input evidence for C_qm source-norm and local arena projection pack",
            **flags(),
        }
        for index, (key, path) in enumerate(SOURCE_FILES.items())
    ]


def finite_input_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "FIN1543_0_C_qm",
            "C_qm",
            "||DObs_e[Dq[v_m]]|| in declared local norm",
            "zero theorem or finite coefficient with units and source path",
            "MISSING_DQVM_DERIVATIVE_OR_PARENT_ZERO",
            "highest leverage input; if zero, stress-mediated geometry coupling vanishes",
            source_list("1542_cqm", "1541_coupling", "cg_no_shadow", "single_public_metric"),
        ),
        (
            "FIN1543_1_T_source_norm",
            "T_source_norm",
            "||delta S_matter/delta q||_source for the compact body/worldtube",
            "source current normalization, compact-source profile, same-frame Hilbert/Noether current",
            "MISSING_SOURCE_NORM",
            "not expected to be zero for matter; needed to scale the C_qm leakage",
            source_list("1542_cqm", "source_current", "source_measure_flux"),
        ),
        (
            "FIN1543_2_S_direct_m",
            "S_direct_m",
            "direct memory dependence in matter/source action",
            "parent no-direct-memory theorem or finite residual coefficient",
            "MISSING_ACTION_DOMAIN_EXCLUSION_OR_VALUE",
            "if nonzero, q-kernel alone would not silence the source",
            source_list("1542_cqm", "source_current", "source_normalization_owner"),
        ),
        (
            "FIN1543_3_S_source_norm_extra",
            "S_source_norm_extra",
            "extra memory leakage in source calibration beyond Hilbert q-pullback",
            "source-normalization descent theorem or finite source-calibration residual",
            "MISSING_SOURCE_NORMALIZATION_RESIDUAL",
            "protects against hiding coupling in measured GM/calibration",
            source_list("1542_cqm", "source_normalization_owner", "source_measure_flux"),
        ),
        (
            "FIN1543_4_S_boundary_m",
            "S_boundary_m",
            "compact inner/domain/boundary memory leakage",
            "Q_m^H/C_inner/domain support theorem or finite boundary norm",
            "MISSING_BOUNDARY_CHARGE_AND_DOMAIN_NORM",
            "prevents exterior-vacuum language from erasing compact-source charge",
            source_list("1542_cqm", "1539_inputs", "boundary_certificate"),
        ),
        (
            "FIN1543_5_S_cg_norm",
            "S_cg_norm",
            "finite no-cancellation envelope",
            "S_cg_norm <= 1/2*T_source_norm*C_qm + S_direct_m + S_source_norm_extra + S_boundary_m",
            "SCHEMA_READY_INPUTS_MISSING",
            "feeds N_pair and then all local arena projections",
            source_list("1542_cqm", "1542_scg"),
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "input_id": input_id,
            "symbol": symbol,
            "definition_or_formula": definition,
            "needed_evidence": evidence,
            "current_status": status,
            "role": role,
            "source_paths": sources,
            **flags(),
        }
        for input_id, symbol, definition, evidence, status, role, sources in rows
    ]


def arena_projection_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "ARENA1543_0_R10",
            "R10 short-range inverse-square tests",
            "alpha_R10(lambda) <= Pi_R10(lambda) * [U_B_max*S_cg_norm + C_inner*|Q_m^H|]",
            "Pi_R10(lambda); lambda profile; K_X; U_B_max; C_inner; Q_m^H; valid bound curve",
            "MISSING_ARENA_PROJECTION",
            source_list("r10_curve_candidate", "r10_runner", "cg_no_shadow"),
        ),
        (
            "ARENA1543_1_PPN",
            "PPN gamma/beta/preferred-frame",
            "|Delta_PPN| <= Pi_PPN * N_lock with first-pair contribution inserted by S_cg_norm envelope",
            "Pi_PPN response matrix; gauge convention; weak-field metric map; hidden-kernel residuals",
            "MISSING_PPN_RESPONSE_MATRIX",
            source_list("local_bound_claims", "single_public_metric", "1542_scg"),
        ),
        (
            "ARENA1543_2_clock",
            "clock/redshift/fine-structure style tests",
            "|delta ln nu| <= Pi_clock * N_lock plus separate constant/readout sensitivity rows",
            "clock sensitivity matrix; calibration convention; no shadow-clock frame; constants split",
            "MISSING_CLOCK_PROJECTION",
            source_list("local_bound_claims", "cg_no_shadow", "single_public_metric"),
        ),
        (
            "ARENA1543_3_orbital",
            "orbital/source-GM/local acceleration systems",
            "|delta a/a| or |delta GM/GM| <= Pi_orbital * N_lock",
            "worldtube source profile; same-frame mass charge; orbital readout map; support/domain residuals",
            "MISSING_ORBITAL_SOURCE_PROJECTION",
            source_list("local_bound_claims", "source_measure_flux", "source_normalization_owner"),
        ),
        (
            "ARENA1543_4_local_GR",
            "local GR/Newton reduction gate",
            "local residual vector <= Pi_local * N_lock with all source, boundary, and hidden-kernel terms included",
            "N_lock; Kmetric conversion; PPN residual vector; q-kernel or finite coupling proof",
            "BLOCKED_NO_CLAIM",
            source_list("1542_scg", "1541_coupling", "source_current"),
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "arena_id": arena_id,
            "arena": arena,
            "projection_formula": formula,
            "required_inputs": inputs,
            "current_status": status,
            "source_paths": sources,
            **flags(),
        }
        for arena_id, arena, formula, inputs, status, sources in rows
    ]


def bound_anchor_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "BOUND1543_0_R10_curve_candidate",
            "R10 alpha(lambda)",
            "review-candidate/nonclaim curve available for smoke plumbing only",
            rel(SOURCE_FILES["r10_curve_candidate"]),
            "BOUND_AVAILABLE_NONCLAIM_MTS_PROJECTION_MISSING",
        ),
        (
            "BOUND1543_1_local_bound_claims",
            "PPN/WEP/clock/orbital local bound ledger",
            "local bound anchors exist but do not make MTS rows score-ready",
            rel(SOURCE_FILES["local_bound_claims"]),
            "ANCHORS_AVAILABLE_PROJECTIONS_MISSING",
        ),
        (
            "BOUND1543_2_R10_runner",
            "existing R10 comparator",
            "runner can reject placeholders once MTS projection rows are generated",
            rel(SOURCE_FILES["r10_runner"]),
            "RUNNER_AVAILABLE_INPUTS_MISSING",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "anchor_id": anchor_id,
            "observable": observable,
            "status_summary": summary,
            "source_path": source_path,
            "current_status": status,
            **flags(),
        }
        for anchor_id, observable, summary, source_path, status in rows
    ]


def projection_runner_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "RUN1543_0_Scg",
            "S_cg_norm",
            "1/2*T_source_norm*C_qm + S_direct_m + S_source_norm_extra + S_boundary_m",
            "NOT_COMPUTABLE",
            "finite source-pack inputs missing",
        ),
        (
            "RUN1543_1_Npair",
            "N_pair",
            "U_B_max*S_cg_norm + C_inner*|Q_m^H|",
            "NOT_COMPUTABLE",
            "first-pair inputs remain missing",
        ),
        (
            "RUN1543_2_R10",
            "alpha_R10(lambda)",
            "Pi_R10(lambda)*N_pair",
            "NOT_COMPUTABLE",
            "Pi_R10 and MTS N_pair missing; bound curve is nonclaim review candidate",
        ),
        (
            "RUN1543_3_PPN",
            "PPN residual vector",
            "Pi_PPN*N_lock",
            "NOT_COMPUTABLE",
            "response matrix and N_lock missing",
        ),
        (
            "RUN1543_4_clock_orbital",
            "clock/orbital residuals",
            "Pi_clock/orbital*N_lock",
            "NOT_COMPUTABLE",
            "arena projection rows missing",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "quantity": quantity,
            "formula": formula,
            "current_status": status,
            "reason": reason,
            **flags(),
        }
        for runner_id, quantity, formula, status, reason in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1543_0_inputs_named", "finite source inputs named", "PASS_NONCLAIM", "all C_qm/S_cg source-pack rows exist"),
        ("GATE1543_1_arenas_named", "local arenas named", "PASS_NONCLAIM", "R10, PPN, clock, orbital, and local-GR projection rows exist"),
        ("GATE1543_2_Scg_score", "S_cg_norm score-ready", "BLOCKED", "finite source inputs missing"),
        ("GATE1543_3_R10_score", "R10 score-ready", "BLOCKED", "MTS projection and valid bound comparison rows missing"),
        ("GATE1543_4_PPN_clock_orbital_score", "PPN/clock/orbital score-ready", "BLOCKED", "arena projections and N_lock missing"),
        ("GATE1543_5_local_GR", "local GR/Newton/PPN claim", "BLOCKED_NO_CLAIM", "no q-kernel, no finite source bound, and no arena projection pass"),
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
            "DEC1543_0_progress",
            "Local projection pack written.",
            "FINITE_ROUTE_NOW_TEST_SHAPED",
            "the finite coupling route now has source-side inputs and arena projection slots",
        ),
        (
            "DEC1543_1_priority",
            "Prioritize C_qm provenance or zero theorem.",
            "C_QM_FIRST",
            "C_qm is the unique coefficient that can kill the stress-mediated term before matter-source size enters",
        ),
        (
            "DEC1543_2_no_claim",
            "Do not run public/local claims.",
            "CLAIM_BLOCKED",
            "projection formulas are schema-only and values are missing",
        ),
        (
            "DEC1543_3_next",
            "Next target is C_qm zero/provenance runner.",
            "NEXT_1544_CQM_PROVENANCE",
            "settle whether C_qm is theorem-zero or a sourced finite coefficient",
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
            "next_id": "NEXT1543_0_1544",
            "next_target": "1544-Y5-Cqm-zero-theorem-or-finite-provenance-runner.md",
            "script": "scripts/Y5_Cqm_zero_theorem_or_finite_provenance_runner.py",
            "objective": "try to close C_qm=0 from a parent q/v_m/observed-coframe theorem; if not, require finite C_qm provenance with units, source path, normalization, and local projection contract",
            "do_not": "do not use WEP/covariance/Ward shortcuts; do not insert placeholder C_qm; do not claim R10/PPN/local GR",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (FINITE_INPUTS, QUAR_INPUTS),
        (ARENA_PROJECTIONS, QUAR_PROJ),
        (BOUND_ANCHORS, QUAR_BOUNDS),
        (PROJECTION_RUNNER, QUAR_RUNNER),
        (DECISION, QUAR_DECISION),
        (FINITE_INPUTS, BRANCH_INPUTS),
        (ARENA_PROJECTIONS, BRANCH_PROJ),
        (BOUND_ANCHORS, BRANCH_BOUNDS),
        (PROJECTION_RUNNER, BRANCH_RUNNER),
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
    inputs = read_csv(FINITE_INPUTS)
    arenas = read_csv(ARENA_PROJECTIONS)
    anchors = read_csv(BOUND_ANCHORS)
    runner = read_csv(PROJECTION_RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    required_inputs = {"C_qm", "T_source_norm", "S_direct_m", "S_source_norm_extra", "S_boundary_m", "S_cg_norm"}
    required_arenas = {"R10 short-range inverse-square tests", "PPN gamma/beta/preferred-frame", "clock/redshift/fine-structure style tests", "orbital/source-GM/local acceleration systems"}
    input_symbols = {row["symbol"] for row in inputs}
    arena_names = {row["arena"] for row in arenas}
    checks = [
        ("VAL1543_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1543 source paths exist"),
        ("VAL1543_1_inputs_complete", required_inputs.issubset(input_symbols), "finite source input rows are complete"),
        ("VAL1543_2_arenas_complete", required_arenas.issubset(arena_names), "R10/PPN/clock/orbital projection rows are complete"),
        ("VAL1543_3_bound_anchors", len(anchors) >= 3 and all(row["source_path"] for row in anchors), "bound anchor links written"),
        ("VAL1543_4_runner_blocked", any(row["runner_id"] == "RUN1543_2_R10" and row["current_status"] == "NOT_COMPUTABLE" for row in runner), "R10 runner remains not computable"),
        ("VAL1543_5_claim_gates_block", any(row["gate_id"] == "GATE1543_5_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates), "local GR claim remains blocked"),
        ("VAL1543_6_decision_next", any(row["result"] == "NEXT_1544_CQM_PROVENANCE" for row in decisions), "decision selects C_qm provenance next"),
        ("VAL1543_7_next_target", any("1544-Y5-Cqm-zero" in row["next_target"] for row in next_rows), "next target is C_qm zero theorem or finite provenance runner"),
        ("VAL1543_8_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1543 CSVs parse cleanly"),
        ("VAL1543_9_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1543_10_branch_copies", all(path.exists() for path in [QUAR_INPUTS, QUAR_PROJ, QUAR_BOUNDS, QUAR_RUNNER, QUAR_DECISION, BRANCH_INPUTS, BRANCH_PROJ, BRANCH_BOUNDS, BRANCH_RUNNER, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1543_11_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1543_12_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
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
            "check_id": "VAL1543_13_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1543 writes the finite C_qm source-norm and local arena projection pack, keeps all projections noncomputable/nonclaim, and selects C_qm zero/provenance next"
            if overall
            else "1543 validation failed; inspect failed rows before continuing",
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
    inputs: list[dict[str, Any]],
    arenas: list[dict[str, Any]],
    anchors: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1543 - C_qm Source-Norm Local Projection Pack",
                "",
                "## Verdict",
                "- The finite coupling route is now test-shaped: source-side inputs are separated from arena projection coefficients.",
                "- The source envelope remains `S_cg_norm <= 1/2*T_source_norm*C_qm + S_direct_m + S_source_norm_extra + S_boundary_m`.",
                "- R10, PPN, clock, orbital, and local-GR projections are explicit, but every one remains noncomputable because the MTS-side inputs/projections are missing.",
                "- `C_qm` is the best next target because it can theorem-zero the stress-mediated term before source-size normalization enters.",
                "- No R10, PPN, clock, orbital, local GR, or Newton claim is promoted.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "purpose"]),
                "",
                "## Finite Input Provenance Pack",
                md_table(inputs, ["input_id", "symbol", "definition_or_formula", "needed_evidence", "current_status", "role"]),
                "",
                "## Arena Projection Pack",
                md_table(arenas, ["arena_id", "arena", "projection_formula", "required_inputs", "current_status"]),
                "",
                "## Bound Anchor Links",
                md_table(anchors, ["anchor_id", "observable", "status_summary", "source_path", "current_status"]),
                "",
                "## Projection Runner",
                md_table(runner, ["runner_id", "quantity", "formula", "current_status", "reason"]),
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
    inputs = finite_input_rows()
    arenas = arena_projection_rows()
    anchors = bound_anchor_rows()
    runner = projection_runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(FINITE_INPUTS, inputs)
    write_csv(ARENA_PROJECTIONS, arenas)
    write_csv(BOUND_ANCHORS, anchors)
    write_csv(PROJECTION_RUNNER, runner)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        FINITE_INPUTS,
        ARENA_PROJECTIONS,
        BOUND_ANCHORS,
        PROJECTION_RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, inputs, arenas, anchors, runner, gates, decisions, validation, next_rows)


if __name__ == "__main__":
    main()

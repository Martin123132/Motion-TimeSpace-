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
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2903-Y5-R2FR-vertical-sector-variation-ledger-or-Qv-piece-leak-rows-under-AX1090.md"

SRC_2902_DOC = ROOT / "2902-Y5-R2FR-vertical-Noether-charge-Qv-extraction-or-kernel-charge-source-row-under-AX1090.md"
SRC_2902_NEXT = RESIDUALS / "P8_Y5_R2FR_2902_NEXT_TARGET.csv"
SRC_2902_SECTORS = RESIDUALS / "P8_Y5_R2FR_2902_VERTICAL_QV_SECTOR_PIECE_LEDGER.csv"
SRC_2902_ROWS = RESIDUALS / "P8_Y5_R2FR_2902_VERTICAL_QV_KERNEL_CHARGE_ROWS.csv"
SRC_2591_DOC = ROOT / "2591-Y5-R2FR-vertical-sector-variation-ledger-or-Qv-piece-leak-rows.md"
SRC_2591_LEDGER = RESIDUALS / "P8_Y5_VERTICAL_SECTOR_2591_VARIATION_LEDGER.csv"
SRC_2591_ROWS = RESIDUALS / "P8_Y5_VERTICAL_SECTOR_2591_QV_PIECE_LEAK_ROWS.csv"
SRC_2591_NEXT = RESIDUALS / "P8_Y5_VERTICAL_SECTOR_2591_NEXT_TARGET.csv"
SRC_1009_SECTORS = ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md"
SRC_EH_BLOCKS = RESIDUALS / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv"
SRC_PIM_CONTRACT = RESIDUALS / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv"
SRC_RESPONSE_DOUBLET = RESIDUALS / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv"
SRC_WORLDTUBE_GLUE = RESIDUALS / "P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv"
SRC_MATTER_DESCENT = ROOT / "1760-Y5-R2FR-matter-worldtube-quotient-descent-or-Amatter-bound.md"
SRC_HIDDEN_SOURCE = ROOT / "1756-Y5-R2FR-two-slot-source-free-owner-or-hidden-source-counterexample-ledger.md"
SRC_NOETHER_CHAIN = RESIDUALS / "P8_PARENT_NOETHER_CLOSURE_DERIVATION_CHAIN.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2903_SOURCE_REGISTER.csv",
    "ledger": RESIDUALS / "P8_Y5_R2FR_2903_VERTICAL_SECTOR_VARIATION_LEDGER.csv",
    "rows": RESIDUALS / "P8_Y5_R2FR_2903_VERTICAL_SECTOR_QV_PIECE_LEAK_ROWS.csv",
    "evaluator": RESIDUALS / "P8_Y5_R2FR_2903_VERTICAL_SECTOR_EVALUATOR.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2903_ACCEPTANCE_GATES.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2903_RUNNER_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2903_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2903_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2903_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2903_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "ledger_copy": RAB_QUEUE / "JR2903_VERTICAL_SECTOR_VARIATION_LEDGER_NONCLAIM.csv",
    "rows_copy": LOCAL_BOUNDS / "Vertical_sector_Qv_piece_leak_rows_2903_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2903_NON_EH_QV_SECTOR_ZERO_OR_SOURCE_PACK_NEXT.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now(),
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


def csv_parses(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2903_0_2902_doc", SRC_2902_DOC, "The next non-cheatable target is now sector bookkeeping;Current MTS has not extracted", "2902 selects sector bookkeeping"),
        ("SRC2903_1_2902_next", SRC_2902_NEXT, "NEXT2902_0_2903;derive sector pieces", "machine-readable 2903 handoff"),
        ("SRC2903_2_2902_sectors", SRC_2902_SECTORS, "QVP2902_6_total;TOTAL_NOT_PROMOTED", "current-chain sector ledger input"),
        ("SRC2903_3_2902_rows", SRC_2902_ROWS, "epsilon_Qv_piece_missing;Delta_vertical_Noether_charge_total_over_Mref", "current-chain Qv residual rows"),
        ("SRC2903_4_2591_doc", SRC_2591_DOC, "the sector ledger exposes the real local-GR bottleneck;No total `Q_v`", "prior sector ledger checkpoint"),
        ("SRC2903_5_2591_ledger", SRC_2591_LEDGER, "VSL2591_6_total;TOTAL_NOT_PROMOTED", "prior sector variation ledger"),
        ("SRC2903_6_2591_rows", SRC_2591_ROWS, "VSP2591_TOTAL;Delta_vertical_sector_Qv_total_over_MH", "prior sector Qv rows"),
        ("SRC2903_7_2591_next", SRC_2591_NEXT, "NEXT2591_0_selected;non-EH sector pieces", "prior non-EH sector target"),
        ("SRC2903_8_1009_sectors", SRC_1009_SECTORS, "Parent sector contract;PCS1009_0_EH_core", "parent sector action contract"),
        ("SRC2903_9_EH_blocks", SRC_EH_BLOCKS, "A511_0_EH_core;A511_3_extra_field_silence", "EH anchor plus local-silence action blocks"),
        ("SRC2903_10_projector", SRC_PIM_CONTRACT, "PM4_projector_algebra;conditional", "projector/source-measure symplectic algebra gap"),
        ("SRC2903_11_response", SRC_RESPONSE_DOUBLET, "RD516_4_zero_odd_source;not_derived_hard_block", "extra/response local charge risk"),
        ("SRC2903_12_worldtube", SRC_WORLDTUBE_GLUE, "W504_4_worldtube_source_measure_glue;not_yet_derived_core_missing_piece", "worldtube/source-measure glue gap"),
        ("SRC2903_13_matter", SRC_MATTER_DESCENT, "Current MTS does not yet parent-sign those clauses;A_matter", "matter/worldtube descent gap"),
        ("SRC2903_14_hidden_source", SRC_HIDDEN_SOURCE, "Every surviving hidden source is converted;explicit nonclaim finite-residual row", "hidden source-slot counterexample ledger"),
        ("SRC2903_15_noether_chain", SRC_NOETHER_CHAIN, "D505_3_exterior_derivative;C_projector", "constraint/current split warning"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, source_path, anchors, role in specs:
        anchors_found, missing_anchors = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(source_path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": source_path.exists(),
                    "anchors_found": anchors_found,
                    "missing_anchors": missing_anchors,
                }
            )
        )
    return rows


def ledger_rows() -> list[dict[str, Any]]:
    specs = [
        ("VSL2903_0_EH_reference", "EH/local geometry", "S_EH[g_obs;kappa0,Lambda0]", "delta S_EH=E_g delta g_obs + dTheta_EH; J_v^EH=dQ_v^EH+C_v^EH", "REFERENCE_TEMPLATE_ONLY", "all non-EH MTS sectors are parent-silent and v is an owned gauge degeneracy on g_obs", "EH anchor is not total MTS parent action", "epsilon_EH_reference_guard", SRC_EH_BLOCKS),
        ("VSL2903_1_boundary_reference", "boundary/reference/improvement", "S_GHY + fixed exact/topological boundary/reference terms", "Theta_boundary(v), mu_v^boundary, Q_v^boundary and B_v convention fixed before readout", "MISSING_FIXED_BV_CONVENTION", "reference subtraction and improvement ambiguity are fixed before readout and compact local boundary flux vanishes", "B_v can absorb or create apparent kernel charge", "epsilon_Bv_ambiguity", SRC_1009_SECTORS),
        ("VSL2903_2_extra_response", "extra motion/time/domain/memory", "S_extra or response doublet sector for local residual fields", "Theta_extra(v), mu_v^extra, Q_v^extra and C_v^extra", "MISSING_EXTRA_SECTOR_VARIATION_AND_ZERO_ODD_SOURCE", "local branch has even scalar density, positive operator, zero odd source, PPN lock and boundary no-flux", "MTS novelty can become local charge hair", "epsilon_Qv_extra_piece", SRC_RESPONSE_DOUBLET),
        ("VSL2903_3_projector_source_measure", "projector/source-measure Pi_M", "Pi_M/source-measure projector sector", "Theta_projector(v), delta Pi_M terms, Q_v^projector and C_v^projector", "MISSING_PROJECTOR_VARIATION_OWNER", "Pi_M is parent symplectic, variation-owned, and d(Pi_M J_H) follows from Ward/Euler closure", "projector algebra alone is not a variational source-current theorem", "epsilon_Qv_projector_piece;epsilon_Cv_constraint_missing", SRC_PIM_CONTRACT),
        ("VSL2903_4_matter_worldtube", "matter/source/worldtube", "S_matter + source/worldtube matching and mass-charge glue", "Theta_matter/source(v), Q_v^matter/source, support variation and source-current constraint", "CONDITIONAL_MATTER_DESCENT_NOT_PARENT_SIGNED", "matter descends through q/e_obs, no direct source slot exists, worldtube source measure equals exterior charge before fitting", "hidden source prefactors, markers, support and non-Hilbert currents remain legal", "epsilon_Qv_matter_source_piece;epsilon_matter_kernel;epsilon_hidden_source_slot", SRC_MATTER_DESCENT),
        ("VSL2903_5_constraint_total", "constraint / C_v total", "all sector Euler/Ward/Gauss constraints", "C_v=C_EH+C_extra+C_projector+C_matter+C_boundary is constraint-proportional or source-bounded", "MISSING_COMMON_CONSTRAINT_SPLIT", "each C_v piece is a parent EOM/proper constraint in the same branch or has a source-backed absolute bound", "Noether identities do not set the residual current to zero by themselves", "epsilon_Cv_constraint_missing", SRC_NOETHER_CHAIN),
        ("VSL2903_6_total", "total vertical Q_v", "S_parent=sum retained MTS sectors", "Theta_parent(v)=sum_i Theta_i(v), Q_v=sum_i Q_v^i, C_v=sum_i C_v^i", "TOTAL_NOT_PROMOTED", "VSL2903_0 through VSL2903_5 all pass in one parent branch with M_ref positive", "no sector-complete total Q_v extraction exists", "Delta_vertical_sector_Qv_total_over_Mref", SRC_2902_DOC),
    ]
    return [
        add_common(
            {
                "ledger_id": ledger_id,
                "sector": sector,
                "action_block": action_block,
                "variation_target": variation_target,
                "current_status": current_status,
                "would_close_if": would_close_if,
                "blocking_gap": blocking_gap,
                "residual": residual,
                "source_path": str(source_path),
                "source_path_exists": source_path.exists(),
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for ledger_id, sector, action_block, variation_target, current_status, would_close_if, blocking_gap, residual, source_path in specs
    ]


def piece_rows() -> list[dict[str, Any]]:
    specs = [
        ("VSP2903_0_EH_guard", "epsilon_EH_reference_guard", "1 if EH reference is used as total MTS Q_v before non-EH sector silence is proved else 0", "boolean guard", "EH_REFERENCE_ONLY_NON_EH_SILENCE_MISSING", SRC_EH_BLOCKS, "local_GR;Newton;PPN"),
        ("VSP2903_1_Bv", "epsilon_Bv_ambiguity", "abs(int_S delta B_v_unfixed)/M_ref", "dimensionless boundary-improvement ambiguity", "MISSING_FIXED_BV_CONVENTION;MISSING_ZERO_BOUNDARY_FLUX;MISSING_M_REF", SRC_1009_SECTORS, "boundary;clock;orbital;PPN"),
        ("VSP2903_2_extra", "epsilon_Qv_extra_piece", "abs(int_S(Q_v^extra+C_v^extra-i_v Theta_extra))/M_ref", "dimensionless extra-sector vertical charge", "MISSING_EXTRA_SECTOR_VARIATION;MISSING_ZERO_ODD_SOURCE;MISSING_BOUNDARY_NO_FLUX;MISSING_M_REF", SRC_RESPONSE_DOUBLET, "PPN;R10;clock;cosmology_branching"),
        ("VSP2903_3_projector", "epsilon_Qv_projector_piece", "abs(int_S(Q_v^projector+C_v^projector-i_v Theta_projector))/M_ref", "dimensionless projector/source-measure vertical charge", "MISSING_PROJECTOR_VARIATION_OWNER;MISSING_WARD_OR_EULER_CLOSURE;MISSING_M_REF", SRC_PIM_CONTRACT, "source_mass;Newton;orbital;PPN"),
        ("VSP2903_4_matter_source", "epsilon_Qv_matter_source_piece", "abs(int_S(Q_v^matter/source+C_v^matter-i_v Theta_matter/source))/M_ref", "dimensionless matter/source vertical charge", "MISSING_MATTER_DESCENT;MISSING_WORLDTUBE_GLUE;MISSING_NO_DIRECT_SOURCE_SLOT;MISSING_M_REF", SRC_MATTER_DESCENT, "WEP;source_mass;orbital;Newton"),
        ("VSP2903_5_constraint", "epsilon_Cv_constraint_missing", "abs(int_S C_v_nonconstraint_or_unbounded)/M_ref", "dimensionless constraint leakage", "MISSING_COMMON_CONSTRAINT_SPLIT;MISSING_PARENT_EOM_SOURCE;MISSING_M_REF", SRC_NOETHER_CHAIN, "Bianchi;conservation;source_current"),
        ("VSP2903_TOTAL", "Delta_vertical_sector_Qv_total_over_Mref", "sum_abs(VSP2903_0..VSP2903_5)", "dimensionless_after_M_ref", "COMPONENTS_MISSING", SRC_2902_DOC, "q_owner;Newton;local_GR;PPN;R10;clock;orbital"),
    ]
    return [
        add_common(
            {
                "row_id": row_id,
                "symbol": symbol,
                "definition": definition,
                "units": units,
                "current_value": current_value,
                "source_path": str(source_path),
                "source_path_exists": source_path.exists(),
                "observable_link": observable_link,
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for row_id, symbol, definition, units, current_value, source_path, observable_link in specs
    ]


def evaluator_rows() -> list[dict[str, Any]]:
    specs = [
        ("EVAL2903_0_total_Qv_claim", "strict_claim", "total_Qv_extracted = all(VSL2903_0..6 closed in one branch)", "NOT_EVALUATED", "REFUSED_NON_EH_SECTOR_GAPS", "boundary, extra, projector, matter/source and common-constraint pieces remain unsigned"),
        ("EVAL2903_1_EH_reference", "reference_control", "EH reference can be used only after VSP2903_1..5 are theorem-zero/fixed/bounded", "REFERENCE_ONLY", "EH_ONLY_TOTAL_REJECTED", "EH anchor is not total MTS charge"),
        ("EVAL2903_2_sector_envelope", "nonclaim_residual_envelope", "Delta_vertical_sector_Qv_total_over_Mref=sum_abs(EH_guard,Bv,extra,projector,matter,constraint)", "NOT_EVALUATED", "STAGED_MISSING_COMPONENT_VALUES", "rows have source paths and units but no theorem-zero or numeric values"),
    ]
    return [
        add_common(
            {
                "eval_id": eval_id,
                "mode": mode,
                "formula": formula,
                "computed_value": computed_value,
                "result": result,
                "reason": reason,
                "runner_ready": False,
            }
        )
        for eval_id, mode, formula, computed_value, result, reason in specs
    ]


def gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATE2903_0_sources", "all source paths and anchors exist", "PASS", "source register validation covers cited inputs", True),
        ("GATE2903_1_sector_ledger", "retained vertical Qv sectors are ledgered", "PASS_NONCLAIM", "EH, boundary, extra, projector, matter/source, constraint and total rows are separated", True),
        ("GATE2903_2_EH_total", "EH reference charge is total MTS vertical Qv", "REJECTED_SHORTCUT", "non-EH sector silence is not proved", False),
        ("GATE2903_3_non_EH_zero", "all non-EH vertical Qv pieces vanish", "FAIL", "boundary, extra, projector and matter/source sectors all retain unsigned pieces", False),
        ("GATE2903_4_constraint_total", "C_v total is constraint-proportional and harmless", "FAIL", "common constraint split and parent EOM source are missing", False),
        ("GATE2903_5_rows_source_ready", "sector Qv residual rows have units and source paths", "PASS_NONCLAIM", "rows are explicit and nonclaim", True),
        ("GATE2903_6_local_GR", "local GR/Newton follows from the sector ledger", "FAIL_CLOSED", "sector ledger exposes missing pieces; it does not close them", False),
        ("GATE2903_7_next", "non-EH Qv zero/source-pack is selected next", "PASS_NONCLAIM", "largest theory risk is whether MTS novelty is locally silent", True),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "criterion": criterion,
                "result": result,
                "reason": reason,
                "gate_passed": gate_passed,
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for gate_id, criterion, result, reason, gate_passed in specs
    ]


def runner_rows() -> list[dict[str, Any]]:
    specs = [
        ("RUN2903_0_total_sector_Qv", "REFUSED_NON_EH_SECTOR_GAPS", "EH reference; boundary Bv; extra response; projector source-measure; matter/worldtube; common constraints; M_ref", 0, "no sector-complete total Qv extraction exists"),
        ("RUN2903_1_piece_rows", "STAGED_NONCLAIM_ROWS", "epsilon_EH_reference_guard;epsilon_Bv_ambiguity;epsilon_Qv_extra_piece;epsilon_Qv_projector_piece;epsilon_Qv_matter_source_piece;epsilon_Cv_constraint_missing", 0, "piece rows are explicit but unfilled"),
        ("RUN2903_2_next_non_EH", "NEXT_TARGET_SELECTED", "non-EH sector Qv zero or source pack", 0, "the next fight is local silence of MTS novelty"),
    ]
    return [
        add_common(
            {
                "runner_id": runner_id,
                "status": status,
                "required_components": required_components,
                "components_evaluable": components_evaluable,
                "reason": reason,
                "runner_ready": False,
            }
        )
        for runner_id, status, required_components, components_evaluable, reason in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2903_0_sector_split", "SECTOR_QV_SPLIT_ACCEPTED", "a total zero theorem would be too easy to cheat without sector-owned Theta/mu/Q/C pieces", "every retained MTS sector must vanish by theorem or enter a residual row"),
        ("DEC2903_1_no_total_promotion", "TOTAL_QV_NOT_PROMOTED", "all non-EH sectors retain missing variation, charge, constraint or boundary data", "vertical kernel nullness, q/Obs_e and local-GR/Newton remain blocked"),
        ("DEC2903_2_next", "NON_EH_QV_SECTOR_ZERO_SELECTED_NEXT", "the largest theory risk is not the EH reference piece; it is whether MTS novelty is locally silent", "2904 should prove non-EH vertical charge zero or produce source-ready Qv sector rows"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": next_action,
            }
        )
        for decision_id, decision, because, next_action in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2903_0_2904",
                "status": "selected_primary",
                "target_doc": "2904-Y5-R2FR-non-EH-sector-Qv-zero-priority-gate-or-source-pack-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_non_EH_sector_Qv_zero_priority_gate_or_source_pack_under_AX1090_2904.py",
                "mission": "try to prove boundary, extra/response, projector/source-measure and matter/worldtube vertical Q_v pieces vanish or are constraint-proportional in one local branch",
                "success_condition": "non-EH sector pieces are theorem-zero/fixed-before-readout/constraint-proportional with no hidden source slot and no compact boundary flux",
                "fallback_condition": "produce source-ready nonclaim rows for epsilon_Bv_ambiguity, epsilon_Qv_extra_piece, epsilon_Qv_projector_piece, epsilon_Qv_matter_source_piece and epsilon_Cv_constraint_missing",
                "forbidden": "EH-only total charge; total-zero switch; post-readout counterterm; fitted M_ref; local-GR/Newton claim; GitHub action; formalization-workbench edit",
                "selected": True,
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    specs = [
        ("BR2903_0_ledger_copy", OUTPUTS["ledger"], BRANCH_OUTPUTS["ledger_copy"], "RAB queue copy of vertical sector ledger"),
        ("BR2903_1_rows_copy", OUTPUTS["rows"], BRANCH_OUTPUTS["rows_copy"], "local-bounds copy of sector Qv piece rows"),
        ("BR2903_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue copy of non-EH sector Qv target"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, destination, purpose in specs:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_table": str(source),
                    "copy_path": str(destination),
                    "purpose": purpose,
                    "exists": destination.exists(),
                }
            )
        )
    return rows


def formalization_touched() -> bool:
    if not FORMALIZATION.exists():
        return False
    start_timestamp = SCRIPT_START_UTC.timestamp()
    for candidate in FORMALIZATION.rglob("*"):
        try:
            if candidate.is_file() and candidate.stat().st_mtime >= start_timestamp:
                return True
        except OSError:
            return True
    return False


def validation_rows(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = all_rows["sources"]
    ledger_rows_data = all_rows["ledger"]
    piece_rows_data = all_rows["rows"]
    evaluator_rows_data = all_rows["evaluator"]
    gate_rows_data = all_rows["gates"]
    next_rows_data = all_rows["next"]
    branch_rows_data = all_rows["branches"]
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    required_symbols = {
        "epsilon_EH_reference_guard",
        "epsilon_Bv_ambiguity",
        "epsilon_Qv_extra_piece",
        "epsilon_Qv_projector_piece",
        "epsilon_Qv_matter_source_piece",
        "epsilon_Cv_constraint_missing",
        "Delta_vertical_sector_Qv_total_over_Mref",
    }
    found_symbols = {row["symbol"] for row in piece_rows_data}

    checks = [
        ("VAL2903_0_sources_exist", all(row["path_exists"] for row in source_rows), "all registered source paths exist"),
        ("VAL2903_1_source_anchors", all(row["anchors_found"] for row in source_rows), "all registered source anchors were found"),
        ("VAL2903_2_sector_ledger_complete", len(ledger_rows_data) == 7 and any(row["ledger_id"] == "VSL2903_6_total" for row in ledger_rows_data), "ledger covers every retained Qv sector"),
        ("VAL2903_3_source_paths_exist", all(row["source_path_exists"] for row in ledger_rows_data + piece_rows_data), "all sector ledger and piece rows have existing source paths"),
        ("VAL2903_4_piece_rows_present", required_symbols <= found_symbols, "all sector Qv piece leak rows are present"),
        ("VAL2903_5_piece_rows_nonclaim", all(not row["valid_for_claim"] and not row["accepted_for_scoring"] for row in piece_rows_data), "sector Qv rows remain nonclaim"),
        ("VAL2903_6_evaluator_refuses", any(row["eval_id"] == "EVAL2903_0_total_Qv_claim" and row["result"] == "REFUSED_NON_EH_SECTOR_GAPS" for row in evaluator_rows_data), "strict sector evaluator refuses non-EH gaps"),
        ("VAL2903_7_EH_shortcut_rejected", any(row["gate_id"] == "GATE2903_2_EH_total" and row["result"] == "REJECTED_SHORTCUT" for row in gate_rows_data), "EH-only shortcut rejected"),
        ("VAL2903_8_local_gr_fail_closed", any(row["gate_id"] == "GATE2903_6_local_GR" and row["result"] == "FAIL_CLOSED" for row in gate_rows_data), "local GR/Newton remains fail-closed"),
        ("VAL2903_9_next_target_2904", any(row["next_id"] == "NEXT2903_0_2904" and row["selected"] for row in next_rows_data), "2904 non-EH sector Qv zero/source-pack target selected"),
        ("VAL2903_10_branch_copies_exist", all(row["exists"] for row in branch_rows_data), "branch copies were written"),
        ("VAL2903_11_csv_outputs_parse", all(csv_parses(path) for path in csv_outputs), "all generated CSV outputs parse cleanly"),
        ("VAL2903_12_formalization_untouched_during_run", not formalization_touched(), "formalization-workbench was not touched during this run"),
    ]
    overall = all(passed for _, passed, _ in checks)
    checks.append(("VAL2903_OVERALL", overall, "2903 validation overall"))
    return [
        {
            "check_id": check_id,
            "passed": passed,
            "detail": detail,
            "generated_utc": now(),
        }
        for check_id, passed, detail in checks
    ]


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, separator, *body])


def write_doc(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 2903 - Y5 R2FR Vertical Sector Variation Ledger or Qv Piece Leak Rows Under AX1090",
        "",
        f"Run: `runs/{SCRIPT_START_UTC.strftime('%Y%m%d-%H%M%S')}-Y5-R2FR-vertical-sector-variation-ledger-or-Qv-piece-leak-rows-under-AX1090`",
        "Status: `Y5_R2FR_2903_sector_Qv_split_refreshed_non_EH_gaps_retained_2904_next`",
        "Claim ceiling: `sector_Qv_piece_nonclaim_only_no_total_Qv_q_kernel_source_complex_PiM_lock_epsilon_charge_Newton_beta_PPN_local_GR_R10_or_GitHub_claim`",
        "",
        "## Summary",
        "",
        "2903 refreshes the vertical `Q_v` sector split in the current 2900-chain. The result is clean but not yet victorious: EH/local geometry is a useful reference, not the total MTS charge.",
        "",
        "The retained non-EH sectors are the load-bearing problem: boundary/reference, extra response, projector/source-measure, matter/worldtube and common constraints. Each must be theorem-zero, fixed before readout, constraint-proportional or source-bounded in one parent branch before q/kernel or local-GR claims are reopened.",
        "",
        "So the route is not circling. It is now pointing at the exact places MTS novelty can leak local charge.",
        "",
        "## Source Register",
        "",
        md_table(all_rows["sources"], ["source_id", "source_path", "path_exists", "anchors_found", "role", "missing_anchors"]),
        "",
        "## Sector Variation Ledger",
        "",
        md_table(all_rows["ledger"], ["ledger_id", "sector", "action_block", "variation_target", "current_status", "blocking_gap", "residual", "valid_for_claim"]),
        "",
        "## Qv Piece Leak Rows",
        "",
        md_table(all_rows["rows"], ["row_id", "symbol", "definition", "units", "current_value", "source_path", "observable_link", "valid_for_claim"]),
        "",
        "## Evaluator",
        "",
        md_table(all_rows["evaluator"], ["eval_id", "mode", "computed_value", "result", "reason", "runner_ready", "valid_for_claim"]),
        "",
        "## Acceptance Gates",
        "",
        md_table(all_rows["gates"], ["gate_id", "criterion", "result", "reason", "gate_passed", "valid_for_claim"]),
        "",
        "## Runner Status",
        "",
        md_table(all_rows["runner"], ["runner_id", "status", "required_components", "components_evaluable", "reason", "runner_ready", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        md_table(all_rows["decision"], ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(all_rows["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(all_rows["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(all_rows["validation"], ["check_id", "passed", "detail", "generated_utc"]),
        "",
        "## Working Read",
        "",
        "This is a better fight than a global yes/no on the theory. If the non-EH sectors are locally silent, the GR-reduction route gets real teeth. If one sector survives, we have named the physical residual MTS must own instead of hiding it behind an EH reference calculation.",
        "",
        "## Forbidden Claims From 2903",
        "",
        "- EH reference charge is the total MTS vertical `Q_v`.",
        "- Boundary, extra, projector, matter/source or constraint sector `Q_v` pieces vanish.",
        "- Total `Q_v`, q/kernel ownership, source-complex ownership, `Pi_M` lock, `epsilon_charge=0`, measured `GM`, source-normalized Newton, beta, PPN, R10 or local GR is proved.",
    ]
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    all_rows: dict[str, list[dict[str, Any]]] = {}
    all_rows["sources"] = source_register_rows()
    all_rows["ledger"] = ledger_rows()
    all_rows["rows"] = piece_rows()
    all_rows["evaluator"] = evaluator_rows()
    all_rows["gates"] = gate_rows()
    all_rows["runner"] = runner_rows()
    all_rows["decision"] = decision_rows()
    all_rows["next"] = next_rows()

    for key in ["sources", "ledger", "rows", "evaluator", "gates", "runner", "decision", "next"]:
        write_csv(OUTPUTS[key], all_rows[key])

    all_rows["branches"] = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], all_rows["branches"])

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_doc(all_rows)

    overall = next(row["passed"] for row in all_rows["validation"] if row["check_id"] == "VAL2903_OVERALL")
    print(f"2903 validation overall: {overall}")
    print(DOC)


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_VERTICAL_SECTOR_QV_LEDGER_2591"
CHECKPOINT_ID = "2591"

DOC = ROOT / "2591-Y5-R2FR-vertical-sector-variation-ledger-or-Qv-piece-leak-rows.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_VERTICAL_SECTOR_2591_SOURCE_REGISTER.csv",
    "variation_ledger": OUT / "P8_Y5_VERTICAL_SECTOR_2591_VARIATION_LEDGER.csv",
    "piece_leak_rows": OUT / "P8_Y5_VERTICAL_SECTOR_2591_QV_PIECE_LEAK_ROWS.csv",
    "runner_refusal": OUT / "P8_Y5_VERTICAL_SECTOR_2591_RUNNER_REFUSAL.csv",
    "claim_gates": OUT / "P8_Y5_VERTICAL_SECTOR_2591_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_VERTICAL_SECTOR_2591_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_VERTICAL_SECTOR_2591_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_VERTICAL_SECTOR_2591_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2591_VALIDATION.csv",
}

COPY_TARGETS = {
    "variation_ledger": QUEUE / "JR2591_VERTICAL_SECTOR_VARIATION_LEDGER_NONCLAIM.csv",
    "piece_leak_rows": LOCAL_BOUNDS / "Vertical_sector_Qv_piece_leak_rows_2591_NONCLAIM.csv",
    "next_target": QUEUE / "JR2591_NON_EH_QV_SECTOR_ZERO_OR_SOURCE_PACK_NEXT.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def with_stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": utc_now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        **row,
    }


def row_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (list, tuple)):
        return ";".join(str(item) for item in value)
    if value is None:
        return ""
    return str(value)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row_value(row.get(field, "")) for field in fields})


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), len(rows), ""
    except Exception as exc:  # pragma: no cover - validation reports the error.
        return False, 0, str(exc)


def path_has_needles(path: Path, needles: list[str]) -> list[str]:
    if not path.exists():
        return needles
    text = path.read_text(encoding="utf-8", errors="replace")
    return [needle for needle in needles if needle not in text]


def source_register_rows() -> list[dict[str, Any]]:
    source_specs = [
        {
            "source_id": "SRC2591_00_2590_handoff",
            "source_path": ROOT / "2590-Y5-R2FR-vertical-Noether-charge-Qv-extraction-or-kernel-charge-source-row.md",
            "needles": ["NEXT2590_0_selected", "QVP2590_6_total", "VAL2590_OVERALL"],
            "role": "active handoff selecting vertical sector variation ledger",
        },
        {
            "source_id": "SRC2591_01_2590_next_queue",
            "source_path": QUEUE / "JR2590_VERTICAL_SECTOR_VARIATION_LEDGER_NEXT.csv",
            "needles": ["NEXT2590_0_selected", "2591-Y5-R2FR-vertical-sector-variation-ledger-or-Qv-piece-leak-rows.md"],
            "role": "machine-readable 2591 task and guardrails",
        },
        {
            "source_id": "SRC2591_02_1009_sector_contract",
            "source_path": ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
            "needles": ["PCS1009_0_EH_core", "PCS1009_6_mass_projector_PiM", "PCS1009_9_total_parent_contract"],
            "role": "parent current-chain sector contract and total-action guardrail",
        },
        {
            "source_id": "SRC2591_03_EH_blocks",
            "source_path": OUT / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
            "needles": ["A511_0_EH_core", "A511_3_extra_field_silence", "A511_6_metric_readout"],
            "role": "minimal local-GR action-block template: EH anchor plus required silence clauses",
        },
        {
            "source_id": "SRC2591_04_projector_contract",
            "source_path": OUT / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
            "needles": ["PM1_parent_boundary_symplectic_metric", "PM5_projector_variation_owned", "PM6_flux_closure_requires_Ward_or_Euler"],
            "role": "projector/source-measure symplectic algebra and variation gaps",
        },
        {
            "source_id": "SRC2591_05_response_doublet",
            "source_path": OUT / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv",
            "needles": ["RD516_1_even_scalar_density", "RD516_4_zero_odd_source", "RD516_6_boundary_no_flux"],
            "role": "extra/memory response doublet local-silence contract",
        },
        {
            "source_id": "SRC2591_06_worldtube_glue",
            "source_path": OUT / "P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv",
            "needles": ["W504_1_covariant_parent_Noether_identity", "W504_4_worldtube_source_measure_glue", "W504_5_calibration_and_limits"],
            "role": "worldtube/source-measure glue and Newton calibration clauses",
        },
        {
            "source_id": "SRC2591_07_matter_descent",
            "source_path": ROOT / "1760-Y5-R2FR-matter-worldtube-quotient-descent-or-Amatter-bound.md",
            "needles": ["MWD1760_1_conditional_theorem", "AM1760_8_A_matter", "VAL1760_OVERALL"],
            "role": "matter/worldtube descent theorem and A_matter nonclaim interface",
        },
        {
            "source_id": "SRC2591_08_hidden_source",
            "source_path": ROOT / "1756-Y5-R2FR-two-slot-source-free-owner-or-hidden-source-counterexample-ledger.md",
            "needles": ["HSC1756_9_verdict", "HSR1756_9_total", "VAL1756_OVERALL"],
            "role": "hidden source/direct-slot counterexample ledger",
        },
    ]
    rows: list[dict[str, Any]] = []
    for source in source_specs:
        source_path = source["source_path"]
        missing_needles = path_has_needles(source_path, source["needles"])
        rows.append(
            with_stamp(
                {
                    "source_id": source["source_id"],
                    "source_path": source_path,
                    "exists": source_path.exists(),
                    "missing_needles": missing_needles,
                    "source_pass": source_path.exists() and not missing_needles,
                    "role": source["role"],
                    "valid_for_claim": False,
                }
            )
        )
    return rows


def variation_ledger_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "ledger_id": "VSL2591_0_EH_reference",
            "sector": "EH/local geometry",
            "action_block": "S_EH[g_obs;kappa0,Lambda0]",
            "variation_target": "delta S_EH = E_g delta g_obs + dTheta_EH; J_v^EH=Theta_EH(v)-mu_v^EH=dQ_v^EH+C_v^EH",
            "current_status": "REFERENCE_TEMPLATE_ONLY",
            "would_close_if": "all non-EH MTS sectors are parent-silent and v acts as an owned diffeomorphism/local Lorentz/gauge degeneracy on g_obs",
            "blocking_gap": "EH anchor is not the total MTS parent action; residual sectors may carry Q_v",
            "residual": "epsilon_EH_reference_guard",
            "source_path": OUT / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
        },
        {
            "ledger_id": "VSL2591_1_boundary_reference",
            "sector": "boundary/reference/improvement",
            "action_block": "S_GHY + fixed exact/topological boundary/reference terms",
            "variation_target": "Theta_boundary(v), mu_v^boundary, Q_v^boundary and B_v convention fixed before readout",
            "current_status": "MISSING_FIXED_BV_CONVENTION",
            "would_close_if": "reference subtraction and improvement ambiguity are fixed before readout and compact local boundary flux vanishes",
            "blocking_gap": "B_v can absorb or create apparent kernel charge if not fixed",
            "residual": "epsilon_Bv_ambiguity",
            "source_path": ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
        },
        {
            "ledger_id": "VSL2591_2_extra_response",
            "sector": "extra motion/time/domain/memory",
            "action_block": "S_extra or response doublet sector for local residual fields",
            "variation_target": "Theta_extra(v), mu_v^extra, Q_v^extra and C_v^extra",
            "current_status": "MISSING_EXTRA_SECTOR_VARIATION_AND_ZERO_ODD_SOURCE",
            "would_close_if": "local branch has even scalar density, positive operator, zero odd source, PPN lock and boundary no-flux",
            "blocking_gap": "extra sector is where MTS novelty can become local charge hair",
            "residual": "epsilon_Qv_extra_piece",
            "source_path": OUT / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv",
        },
        {
            "ledger_id": "VSL2591_3_projector_source_measure",
            "sector": "projector/source-measure Pi_M",
            "action_block": "Pi_M/source-measure projector sector",
            "variation_target": "Theta_projector(v), delta Pi_M terms, Q_v^projector and C_v^projector",
            "current_status": "MISSING_PROJECTOR_VARIATION_OWNER",
            "would_close_if": "Pi_M is parent symplectic, its variation is owned, and d(Pi_M J_H) follows from Ward/Euler closure",
            "blocking_gap": "projector algebra alone is not a variational source-current theorem",
            "residual": "epsilon_Qv_projector_piece;epsilon_Cv_constraint_missing",
            "source_path": OUT / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
        },
        {
            "ledger_id": "VSL2591_4_matter_worldtube",
            "sector": "matter/source/worldtube",
            "action_block": "S_matter + source/worldtube matching and mass-charge glue",
            "variation_target": "Theta_matter/source(v), Q_v^matter/source, worldtube support variation and source-current constraint",
            "current_status": "CONDITIONAL_MATTER_DESCENT_NOT_PARENT_SIGNED",
            "would_close_if": "matter descends through q/e_obs, no direct source slot exists, worldtube source measure equals exterior charge before fitting",
            "blocking_gap": "hidden source prefactors, material markers, worldtube support and non-Hilbert currents remain legal",
            "residual": "epsilon_Qv_matter_source_piece;epsilon_matter_kernel;epsilon_hidden_source_slot",
            "source_path": ROOT / "1760-Y5-R2FR-matter-worldtube-quotient-descent-or-Amatter-bound.md",
        },
        {
            "ledger_id": "VSL2591_5_constraint_total",
            "sector": "constraint / C_v total",
            "action_block": "all sector Euler/Ward/Gauss constraints",
            "variation_target": "C_v=C_EH+C_extra+C_projector+C_matter+C_boundary is constraint-proportional or source-bounded",
            "current_status": "MISSING_COMMON_CONSTRAINT_SPLIT",
            "would_close_if": "each C_v piece is a parent EOM/proper constraint in the same branch or has a source-backed absolute bound",
            "blocking_gap": "Noether identities do not by themselves set the residual current to zero",
            "residual": "epsilon_Cv_constraint_missing",
            "source_path": OUT / "P8_PARENT_NOETHER_CLOSURE_DERIVATION_CHAIN.csv",
        },
        {
            "ledger_id": "VSL2591_6_total",
            "sector": "total vertical Q_v",
            "action_block": "S_parent=sum retained MTS sectors",
            "variation_target": "Theta_parent(v)=sum_i Theta_i(v), Q_v=sum_i Q_v^i, C_v=sum_i C_v^i",
            "current_status": "TOTAL_NOT_PROMOTED",
            "would_close_if": "VSL2591_0 through VSL2591_5 all pass in one parent branch with M_H_ref positive",
            "blocking_gap": "no sector-complete total Q_v extraction exists",
            "residual": "Delta_vertical_sector_Qv_total_over_MH",
            "source_path": ROOT / "2590-Y5-R2FR-vertical-Noether-charge-Qv-extraction-or-kernel-charge-source-row.md",
        },
    ]
    return [
        with_stamp(
            {
                **row,
                "source_path_exists": Path(row["source_path"]).exists(),
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        for row in rows
    ]


def piece_leak_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "VSP2591_0_EH_guard",
            "symbol": "epsilon_EH_reference_guard",
            "definition": "1 if EH reference is used as total MTS Q_v before non-EH sector silence is proved else 0",
            "units": "boolean guard",
            "current_value": "EH_REFERENCE_ONLY_NON_EH_SILENCE_MISSING",
            "source_path": OUT / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
            "observable_link": "local_GR;Newton;PPN",
        },
        {
            "row_id": "VSP2591_1_Bv",
            "symbol": "epsilon_Bv_ambiguity",
            "definition": "abs(int_S delta B_v_unfixed)/M_H_ref",
            "units": "dimensionless boundary-improvement ambiguity",
            "current_value": "MISSING_FIXED_BV_CONVENTION;MISSING_ZERO_BOUNDARY_FLUX;MISSING_M_H_REF",
            "source_path": ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
            "observable_link": "boundary;clock;orbital;PPN",
        },
        {
            "row_id": "VSP2591_2_extra",
            "symbol": "epsilon_Qv_extra_piece",
            "definition": "abs(int_S(Q_v^extra + C_v^extra - i_v Theta_extra))/M_H_ref",
            "units": "dimensionless extra-sector vertical charge",
            "current_value": "MISSING_EXTRA_SECTOR_VARIATION;MISSING_ZERO_ODD_SOURCE;MISSING_BOUNDARY_NO_FLUX;MISSING_M_H_REF",
            "source_path": OUT / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv",
            "observable_link": "PPN;R10;clock;cosmology_branching",
        },
        {
            "row_id": "VSP2591_3_projector",
            "symbol": "epsilon_Qv_projector_piece",
            "definition": "abs(int_S(Q_v^projector + C_v^projector - i_v Theta_projector))/M_H_ref",
            "units": "dimensionless projector/source-measure vertical charge",
            "current_value": "MISSING_PROJECTOR_VARIATION_OWNER;MISSING_WARD_OR_EULER_CLOSURE;MISSING_M_H_REF",
            "source_path": OUT / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
            "observable_link": "source_mass;Newton;orbital;PPN",
        },
        {
            "row_id": "VSP2591_4_matter_source",
            "symbol": "epsilon_Qv_matter_source_piece",
            "definition": "abs(int_S(Q_v^matter/source + C_v^matter - i_v Theta_matter/source))/M_H_ref",
            "units": "dimensionless matter/source vertical charge",
            "current_value": "MISSING_MATTER_DESCENT;MISSING_WORLDTUBE_GLUE;MISSING_NO_DIRECT_SOURCE_SLOT;MISSING_M_H_REF",
            "source_path": ROOT / "1760-Y5-R2FR-matter-worldtube-quotient-descent-or-Amatter-bound.md",
            "observable_link": "WEP;source_mass;orbital;Newton",
        },
        {
            "row_id": "VSP2591_5_constraint",
            "symbol": "epsilon_Cv_constraint_missing",
            "definition": "abs(int_S C_v_nonconstraint_or_unbounded)/M_H_ref",
            "units": "dimensionless constraint leakage",
            "current_value": "MISSING_COMMON_CONSTRAINT_SPLIT;MISSING_PARENT_EOM_SOURCE;MISSING_M_H_REF",
            "source_path": OUT / "P8_PARENT_NOETHER_CLOSURE_DERIVATION_CHAIN.csv",
            "observable_link": "Bianchi;conservation;source_current",
        },
        {
            "row_id": "VSP2591_TOTAL",
            "symbol": "Delta_vertical_sector_Qv_total_over_MH",
            "definition": "epsilon_EH_reference_guard + epsilon_Bv_ambiguity + epsilon_Qv_extra_piece + epsilon_Qv_projector_piece + epsilon_Qv_matter_source_piece + epsilon_Cv_constraint_missing",
            "units": "dimensionless after M_H_ref",
            "current_value": "COMPONENTS_MISSING",
            "source_path": ROOT / "2590-Y5-R2FR-vertical-Noether-charge-Qv-extraction-or-kernel-charge-source-row.md",
            "observable_link": "q_owner;Newton;local_GR;PPN;R10;clock;orbital",
        },
    ]
    return [
        with_stamp(
            {
                **row,
                "source_path_exists": Path(row["source_path"]).exists(),
                "score_ready": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        for row in rows
    ]


def runner_refusal_rows(leak_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in leak_rows:
        reasons = ["VALID_FOR_CLAIM_FALSE", "MISSING_ZERO_THEOREM_OR_NUMERIC_VALUE"]
        if not row["source_path_exists"]:
            reasons.append("MISSING_SOURCE_PATH")
        if row["symbol"] == "epsilon_EH_reference_guard":
            reasons.append("EH_REFERENCE_CANNOT_REPLACE_MTS_TOTAL_ACTION")
        if row["row_id"] == "VSP2591_TOTAL":
            reasons.append("SECTOR_ROWS_NOT_SCORE_READY")
        rows.append(
            with_stamp(
                {
                    "runner_id": f"VSR2591_{row['row_id']}",
                    "target_id": row["row_id"],
                    "symbol": row["symbol"],
                    "verdict": "REFUSED_NONCLAIM_SECTOR_QV_RESIDUAL",
                    "failure_reasons": reasons,
                    "score_ready": False,
                    "claim_allowed": False,
                    "valid_for_claim": False,
                }
            )
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "CG2591_0_sector_ledger_shape",
            "claim": "retained vertical Q_v sectors are explicitly ledgered",
            "gate_status": "PASS_NONCLAIM_STRUCTURE_ONLY",
            "reason": "EH, boundary, extra, projector, matter/source, constraint and total rows are separated",
            "gate_pass": True,
        },
        {
            "gate_id": "CG2591_1_EH_total_shortcut",
            "claim": "EH reference charge is the total MTS vertical Q_v",
            "gate_status": "REJECTED_SHORTCUT",
            "reason": "non-EH sector silence is not proved",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2591_2_non_EH_zero",
            "claim": "all non-EH vertical Q_v pieces vanish",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "boundary, extra, projector and matter/source sectors all retain unsigned pieces",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2591_3_constraint_total",
            "claim": "C_v total is constraint-proportional and harmless",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "common constraint split and parent EOM source are missing",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2591_4_local_GR_Newton",
            "claim": "local GR/Newton follows from the sector ledger",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "sector ledger exposes the missing pieces; it does not close them",
            "gate_pass": False,
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False, "claim_allowed": False}) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2591_0_sector_split_accepted",
            "decision": "SECTOR_QV_SPLIT_ACCEPTED",
            "reason": "a total zero theorem would be too easy to cheat without sector-owned Theta/mu/Q/C pieces",
            "effect": "every retained MTS sector must now either vanish by theorem or enter a residual row",
        },
        {
            "decision_id": "DEC2591_1_no_total_promotion",
            "decision": "TOTAL_QV_NOT_PROMOTED",
            "reason": "all non-EH sectors retain missing variation, charge, constraint or boundary data",
            "effect": "vertical kernel nullness, q/Obs_e and local-GR/Newton remain blocked",
        },
        {
            "decision_id": "DEC2591_2_next",
            "decision": "NON_EH_QV_SECTOR_ZERO_SELECTED_NEXT",
            "reason": "the largest theory risk is not the EH reference piece; it is whether MTS novelty is locally silent",
            "effect": "2592 should try to prove non-EH vertical charge zero or produce source-ready Qv sector rows",
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False}) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2591_0_selected",
            "selection_status": "selected",
            "target_file": "2592-Y5-R2FR-non-EH-sector-Qv-zero-priority-gate-or-source-pack.md",
            "target_script": "scripts/Y5_R2FR_non_EH_sector_Qv_zero_priority_gate_or_source_pack_2592.py",
            "task": "try to prove boundary, extra/response, projector/source-measure and matter/worldtube vertical Q_v pieces vanish or are constraint-proportional in one local branch",
            "success_condition": "non-EH sector pieces are theorem-zero/fixed-before-readout/constraint-proportional with no hidden source slot and no compact boundary flux",
            "fallback_condition": "produce source-ready nonclaim rows for epsilon_Bv_ambiguity, epsilon_Qv_extra_piece, epsilon_Qv_projector_piece, epsilon_Qv_matter_source_piece and epsilon_Cv_constraint_missing",
            "guardrails": "no EH-only total charge; no total-zero switch; no post-readout counterterm; no fitted M_H_ref; no local-GR/Newton claim; no GitHub; no formalization-workbench edits",
            "valid_for_claim": False,
        }
    ]
    return [with_stamp(row) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for copy_id, target_path in COPY_TARGETS.items():
        source_path = OUTPUTS[copy_id]
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)
        rows.append(
            with_stamp(
                {
                    "copy_id": f"COPY2591_{copy_id}",
                    "source_path": source_path,
                    "target_path": target_path,
                    "source_exists": source_path.exists(),
                    "target_exists": target_path.exists(),
                    "valid_for_claim": False,
                }
            )
        )
    return rows


def generated_rows_have_no_claim_flags(data: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in data.values():
        for row in rows:
            if row.get("valid_for_claim") is True or row.get("claim_allowed") is True:
                return False
    return True


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, condition: bool, notes: str, detail: str = "") -> None:
        rows.append(
            with_stamp(
                {
                    "check_id": check_id,
                    "status": "PASS" if condition else "FAIL",
                    "notes": notes,
                    "detail": detail,
                    "valid_for_claim": False,
                }
            )
        )

    add("VAL2591_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and needles are present")
    required_sectors = {"EH/local geometry", "boundary/reference/improvement", "extra motion/time/domain/memory", "projector/source-measure Pi_M", "matter/source/worldtube", "constraint / C_v total", "total vertical Q_v"}
    present_sectors = {row["sector"] for row in data["variation_ledger"]}
    add("VAL2591_01_sector_ledger_complete", required_sectors.issubset(present_sectors), "ledger covers every retained Q_v sector")
    add(
        "VAL2591_02_source_paths_exist",
        all(row["source_path_exists"] is True for row in data["variation_ledger"] + data["piece_leak_rows"]),
        "all sector ledger and leak rows have existing source paths",
    )
    required_symbols = {"epsilon_EH_reference_guard", "epsilon_Bv_ambiguity", "epsilon_Qv_extra_piece", "epsilon_Qv_projector_piece", "epsilon_Qv_matter_source_piece", "epsilon_Cv_constraint_missing", "Delta_vertical_sector_Qv_total_over_MH"}
    present_symbols = {row["symbol"] for row in data["piece_leak_rows"]}
    add("VAL2591_03_piece_rows_present", required_symbols.issubset(present_symbols), "all sector Q_v piece leak rows are present")
    add(
        "VAL2591_04_piece_rows_nonclaim",
        all(row["score_ready"] is False and row["valid_for_claim"] is False for row in data["piece_leak_rows"]),
        "sector Q_v rows remain non-score-ready and nonclaim",
    )
    add(
        "VAL2591_05_runner_refuses",
        all(row["score_ready"] is False and row["claim_allowed"] is False for row in data["runner_refusal"]),
        "runner refuses all unfilled sector Q_v residual rows",
    )
    add(
        "VAL2591_06_claim_gates_safe",
        all(row["claim_allowed"] is False for row in data["claim_gates"])
        and any(row["gate_id"] == "CG2591_1_EH_total_shortcut" and row["gate_status"] == "REJECTED_SHORTCUT" for row in data["claim_gates"]),
        "EH-only shortcut, local-GR and Newton claims remain blocked",
    )
    add("VAL2591_07_no_claim_flags", generated_rows_have_no_claim_flags(data), "no generated row sets valid_for_claim=true or claim_allowed=true")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in (
            "*2591-Y5-R2FR-vertical-sector*",
            "*Y5_R2FR_vertical_sector_variation*",
            "*P8_Y5_VERTICAL_SECTOR_2591*",
            "*JR2591*",
        ):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL2591_08_no_formalization_artifacts",
        not formalization_artifacts,
        "no 2591 artifacts were written to formalization-workbench",
        ";".join(str(path) for path in formalization_artifacts),
    )
    add(
        "VAL2591_09_next_selected",
        any(row["route_id"] == "NEXT2591_0_selected" and "2592-Y5-R2FR-non-EH-sector-Qv-zero" in row["target_file"] for row in data["next"]),
        "2592 non-EH sector Q_v zero/source-pack target selected next",
    )
    add(
        "VAL2591_10_branch_copies",
        all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]),
        "nonclaim branch copies exist",
    )

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2591_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2591_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2591_OVERALL",
        overall,
        "2591 splits vertical Q_v by retained sector, refuses EH-only total charge, keeps sector residuals nonclaim, and selects the non-EH Q_v zero/source-pack gate next",
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for row in rows:
        values = [row_value(row.get(column, "")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2591 Y5 R2FR vertical sector variation ledger or Qv piece leak rows",
        "",
        "**Status:** private nonclaim derivation checkpoint. The vertical `Q_v` obstruction is now split by retained sector. The EH piece is a useful reference, but current MTS cannot use it as the total charge until boundary, extra/response, projector/source-measure, matter/worldtube and constraint pieces are theorem-zero, fixed-before-readout or source-bounded.",
        "",
        "**Main result:** the sector ledger exposes the real local-GR bottleneck: MTS novelty must be locally silent in the same parent branch, not merely absent from an EH reference calculation. No total `Q_v`, kernel-nullness, q/Obs_e, Newton or local-GR claim is made.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role", "valid_for_claim"]),
        "",
        "## Sector Variation Ledger",
        markdown_table(data["variation_ledger"], ["ledger_id", "sector", "action_block", "variation_target", "current_status", "would_close_if", "blocking_gap", "residual", "source_path", "source_path_exists", "valid_for_claim", "claim_allowed"]),
        "",
        "## Qv Piece Leak Rows",
        markdown_table(data["piece_leak_rows"], ["row_id", "symbol", "definition", "units", "current_value", "source_path", "source_path_exists", "observable_link", "score_ready", "valid_for_claim", "claim_allowed"]),
        "",
        "## Runner Refusal",
        markdown_table(data["runner_refusal"], ["runner_id", "target_id", "symbol", "verdict", "failure_reasons", "score_ready", "claim_allowed", "valid_for_claim"]),
        "",
        "## Claim Gates",
        markdown_table(data["claim_gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "valid_for_claim", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect", "valid_for_claim"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "success_condition", "fallback_condition", "guardrails", "valid_for_claim"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists", "valid_for_claim"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail", "valid_for_claim"]),
        "",
        "## Practical Status",
        "",
        "The sector split is good news in the engineering sense: we now know where the load paths are. The route to derived local GR is not one magic line; it is proving the non-EH sectors carry no local vertical charge, or admitting exactly which one does. That is a cleaner fight than arguing about the whole theory at once.",
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)

    leak_rows = piece_leak_rows()
    data = {
        "sources": source_register_rows(),
        "variation_ledger": variation_ledger_rows(),
        "piece_leak_rows": leak_rows,
        "runner_refusal": runner_refusal_rows(leak_rows),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["variation_ledger"], data["variation_ledger"])
    write_csv(OUTPUTS["piece_leak_rows"], data["piece_leak_rows"])
    write_csv(OUTPUTS["runner_refusal"], data["runner_refusal"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])

    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])

    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)

    overall = next(row for row in data["validations"] if row["check_id"] == "VAL2591_OVERALL")
    print(f"{overall['check_id']} {overall['status']}: {overall['notes']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

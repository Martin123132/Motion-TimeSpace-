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
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

DOC = ROOT / "2830-Y5-R2FR-epsilon-vmq-response-kernels-and-source-acquisition-interface-under-AX1090.md"

SRC_2829_NEXT = RESIDUALS / "P8_Y5_R2FR_2829_NEXT_TARGET.csv"
SRC_2829_ACQ = RESIDUALS / "P8_Y5_R2FR_2829_EPSILON_VMQ_SOURCE_READY_ACQUISITION_ROWS.csv"
SRC_2829_KERNEL = RESIDUALS / "P8_Y5_R2FR_2829_EPSILON_VMQ_RESPONSE_KERNEL_REQUIREMENTS.csv"
SRC_2829_THEOREM = RESIDUALS / "P8_Y5_R2FR_2829_QBASIC_NO_SOURCE_PREFACTOR_THEOREM_AUDIT.csv"
SRC_2828_FINITE = RESIDUALS / "P8_Y5_R2FR_2828_FIRST_FINITE_VMQ_Q_SOURCE_ROW_NONCLAIM.csv"
SRC_2827_DERIVATION = RESIDUALS / "P8_Y5_R2FR_2827_DQVM_DERIVATION_LEDGER.csv"
SRC_2489_PPN_KERNEL = RESIDUALS / "P8_Y5_NO_SHADOW_2489_PPN_RESPONSE_KERNEL.csv"
SRC_2631_PPN_VECTOR = RESIDUALS / "P8_Y5_NO_SHADOW_PPN_VECTOR_2631_FULL_PPN_VECTOR_LEDGER.csv"
SRC_2192_R10 = RESIDUALS / "P8_Y5_PARENT_QLOC_2192_R10_RESPONSE_OPERATOR_ROW.csv"
SRC_1678_R10 = RESIDUALS / "P8_Y5_PARENT_QLOC_1678_R10_SOURCE_PROJECTION_ACQUISITION_TABLE_NONCLAIM.csv"
SRC_2675_CLOCK = RESIDUALS / "P8_Y5_R2FR_2675_SPECIES_CLOCK_FIRST_BOUND_FILL_NONCLAIM.csv"
SRC_2466_WEP = RESIDUALS / "P8_Y5_SOURCE_BRIDGE_2466_WEP_COMPOSITION_GUARDRAIL.csv"
SRC_ORBIT_GATES = RESIDUALS / "P8_Y5_GAUSS_ORBITAL_ACCEPTANCE_GATES.csv"
SRC_2488_COUNTER = RESIDUALS / "P8_Y5_NO_SHADOW_2488_COUNTERMODEL_LEDGER.csv"
SRC_2632_RESIDUAL = RESIDUALS / "P8_Y5_SOURCE_PREF_GR_ROLLFORWARD_2632_RESIDUAL_OWNER_LEDGER.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2830_SOURCE_REGISTER.csv",
    "kernel_interface": RESIDUALS / "P8_Y5_R2FR_2830_EPSILON_VMQ_RESPONSE_KERNEL_INTERFACE.csv",
    "source_contract": RESIDUALS / "P8_Y5_R2FR_2830_EPSILON_VMQ_SOURCE_ACQUISITION_CONTRACT.csv",
    "arena_queue": RESIDUALS / "P8_Y5_R2FR_2830_ARENA_PROJECTION_QUEUE_NONCLAIM.csv",
    "readiness": RESIDUALS / "P8_Y5_R2FR_2830_SCORE_READINESS_MATRIX.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2830_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2830_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2830_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2830_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2830_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "kernel_copy": SOURCE_WEIGHT / "epsilon_vmq_response_kernel_interface_2830_NONCLAIM.csv",
    "contract_copy": LOCAL_BOUNDS / "epsilon_vmq_source_acquisition_contract_2830_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2830_EPSILON_VMQ_FIRST_KERNEL_FILL_NEXT.csv",
}

BRANCH_ID = "MTS_R2FR_EPSILON_VMQ_RESPONSE_KERNEL_INTERFACE_2830"


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    paths = {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["score_ready"] = False
    row["valid_prediction_row"] = False
    row["valid_for_claim"] = False
    row["claim_allowed"] = False
    row["generated_utc"] = ts()
    return row


def source_row(source_id: str, path: Path, anchors: str, role: str) -> dict[str, Any]:
    text = read_text(path)
    anchor_list = [anchor for anchor in anchors.split(";") if anchor]
    missing = [anchor for anchor in anchor_list if anchor not in text]
    return nonclaim(
        {
            "source_id": source_id,
            "source_path": str(path),
            "anchors": anchors,
            "role": role,
            "path_exists": path.exists(),
            "anchors_found": not missing,
            "missing_anchors": ";".join(missing),
        }
    )


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2830_0_2829_next", SRC_2829_NEXT, "NEXT2829_0_2830", "2829 handoff selecting epsilon_vmq response-kernel/source-acquisition interface"),
        ("SRC2830_1_2829_acq", SRC_2829_ACQ, "ACQ2829_0_epsilon_vmq_total;ACQ2829_1_source_weight;ACQ2829_2_readout", "source-ready epsilon_vmq acquisition rows"),
        ("SRC2830_2_2829_kernel", SRC_2829_KERNEL, "KREQ2829_0_Cqm;KREQ2829_5_R10", "response-kernel requirements"),
        ("SRC2830_3_2829_theorem", SRC_2829_THEOREM, "THA2829_7_current_verdict", "theorem route failed so finite rows required"),
        ("SRC2830_4_2828_finite", SRC_2828_FINITE, "FVQ2828_0_first_row", "first finite epsilon_vmq row"),
        ("SRC2830_5_2827_derivation", SRC_2827_DERIVATION, "DER2827_6_matter_generator_condition", "exact Dq[v_m] kernel condition"),
        ("SRC2830_6_2489_ppn_kernel", SRC_2489_PPN_KERNEL, "PPNK2489_0_conformal_gamma_kernel;PPNK2489_4_endpoint_readout_tail_placeholder", "PPN response kernel scaffold"),
        ("SRC2830_7_2631_ppn_vector", SRC_2631_PPN_VECTOR, "PPNV2631_8_total_abs", "full PPN no-cancellation vector"),
        ("SRC2830_8_2192_r10", SRC_2192_R10, "R10RESP2192_0_first_schema_operator", "R10 response operator schema"),
        ("SRC2830_9_1678_r10", SRC_1678_R10, "R10S1678_4_verdict", "R10 source projection acquisition blockers"),
        ("SRC2830_10_2675_clock", SRC_2675_CLOCK, "FILL2675_CLK2675_1_tau_readout;FILL2675_CLK2675_3_shared_source_leg", "clock/readout source-leg rows"),
        ("SRC2830_11_2466_wep", SRC_2466_WEP, "WEP2466_3_composition_bound;WEP2466_4_coupling_unification", "WEP/source composition guardrail"),
        ("SRC2830_12_orbit_gates", SRC_ORBIT_GATES, "AG523_1_chain_complete;AG523_5_no_overclaim", "orbital acceptance gates and no-overclaim guard"),
        ("SRC2830_13_2488_counter", SRC_2488_COUNTER, "CM2488_2_source_prefactor;CM2488_3_endpoint_boundary", "source-prefactor and endpoint countermodels"),
        ("SRC2830_14_2632_residual", SRC_2632_RESIDUAL, "RES2632_0_Delta_w_eff;RES2632_4_DObs_e_R", "source-weight/readout residual owners"),
    ]
    return [source_row(*spec) for spec in specs]


def kernel_interface_rows() -> list[dict[str, Any]]:
    specs = [
        ("KI2830_0_Cqm", "C_qm", "epsilon_vmq", "C_qm = ||Dq[v_m]||_{E_q}", "E_q norm; v_m normalization; epsilon_vmq theorem-zero or value", "MISSING_EQ_NORM_AND_VALUE", "local_lock;local_GR", SRC_2829_KERNEL, "KREQ2829_0_Cqm"),
        ("KI2830_1_PPN_total", "PPN_vector", "epsilon_vmq;b_R_to_vmq;d_R_to_vmq;epsilon_endpoint_to_vmq", "Delta_PPN_abs includes all active epsilon_vmq-derived components with no cancellation", "component values/theorem-zeros; PPN response kernels; common source convention", "MISSING_PPN_VECTOR_VALUES", "PPN;local_GR_Newton", SRC_2631_PPN_VECTOR, "PPNV2631_8_total_abs"),
        ("KI2830_2_PPN_gamma", "PPN_gamma", "b_R_to_vmq plus delta_p/qR", "gamma_obs-1 kernel inherited from common-Weyl response, but only after b_R and delta_p are sourced", "b_R theorem-zero/value; delta_p value; no-other-channel guard", "KERNEL_CONDITIONAL_VALUE_MISSING", "PPN_gamma;light_time", SRC_2489_PPN_KERNEL, "PPNK2489_0_conformal_gamma_kernel"),
        ("KI2830_3_PPN_preferred", "PPN_preferred_frame", "d_R_to_vmq", "preferred-frame response requires normalized disformal/current/domain projection", "disformal ansatz; vector normalization; alpha_i response matrix", "MISSING_PREFERRED_FRAME_RESPONSE_KERNEL", "PPN_alpha1;PPN_alpha2;clocks", SRC_2489_PPN_KERNEL, "PPNK2489_3_disformal_preferred_frame_placeholder"),
        ("KI2830_4_R10", "R10_short_range", "epsilon_vmq", "alpha_R10_q(lambda)=c_q_alpha(lambda)*q_profile(lambda)", "c_q_alpha(lambda); q_profile(lambda); range kernel; units; real bound curve", "MISSING_R10_PROJECTION_KERNEL", "R10", SRC_2192_R10, "R10RESP2192_0_first_schema_operator"),
        ("KI2830_5_clock", "clock_response", "epsilon_vmq_readout;d_R_to_vmq", "clock residual needs tau/readout q leak mapped into observed time/frequency convention", "tau_clock_time; alpha/clock owner if EM; clock normalization theorem", "MISSING_CLOCK_KERNEL", "clocks", SRC_2675_CLOCK, "FILL2675_CLK2675_1_tau_readout"),
        ("KI2830_6_WEP_source", "WEP_source_leg", "epsilon_vmq_source_weight", "source-prefactor q leak maps into composition/source-normalization residual", "material/source tensor; WEP projection; source-leg owner", "MISSING_WEP_SOURCE_KERNEL", "WEP;source_normalization", SRC_2466_WEP, "WEP2466_3_composition_bound"),
        ("KI2830_7_orbital_endpoint", "orbital_light_time", "epsilon_endpoint_to_vmq;epsilon_vmq_readout", "endpoint/boundary/readout q leak maps into measured-GM/orbital/light-time residual", "endpoint silence theorem or orbital response kernel; source-normalized GM chain", "MISSING_ORBITAL_ENDPOINT_KERNEL", "orbital;light_time;local_GR", SRC_ORBIT_GATES, "AG523_4_PPN_source_stability"),
    ]
    return [
        nonclaim(
            {
                "kernel_interface_id": row_id,
                "kernel_family": family,
                "epsilon_input": eps_input,
                "interface_formula": formula,
                "required_inputs": required,
                "current_status": status,
                "test_arenas": arenas,
                "source_path": str(source_path),
                "source_anchor": anchor,
                "anchor_found": anchor in read_text(source_path),
                "kernel_ready": False,
                "value_ready": False,
                "theorem_zero_ready": False,
                "control_only": True,
            }
        )
        for row_id, family, eps_input, formula, required, status, arenas, source_path, anchor in specs
    ]


def source_contract_rows() -> list[dict[str, Any]]:
    specs = [
        ("SC2830_0_total", "epsilon_vmq", "total envelope", "derive theorem-zero from q-basic/no-source-prefactor theorem or source finite envelope from component rows", "MISSING_EQ_NORM;MISSING_VM_NORMALIZATION;MISSING_COMPONENT_VALUES", "must not be scored until all components share q_log/E_q/v_m convention", SRC_2829_ACQ, "ACQ2829_0_epsilon_vmq_total"),
        ("SC2830_1_source_weight", "epsilon_vmq_source_weight", "source-weight component", "derive no-source-prefactor/no-Hom or source finite source-weight residual", "MISSING_PARENT_NOHOM;MISSING_WEP_KERNEL;MISSING_SOURCE_LEG_OWNER", "maps to WEP/source-normalization/PPN source leg", SRC_2829_ACQ, "ACQ2829_1_source_weight"),
        ("SC2830_2_readout", "epsilon_vmq_readout", "readout/coframe component", "derive terminal public coframe/DObs kernel or source finite readout leak", "MISSING_TERMINAL_PUBLIC_COFRAME;MISSING_DOBS_KERNEL", "maps to PPN/clocks/orbital/local-GR readout tails", SRC_2829_ACQ, "ACQ2829_2_readout"),
        ("SC2830_3_common_weyl", "b_R_to_vmq", "common Weyl component", "derive no Weyl slot or source b_R response coefficient", "MISSING_PARENT_NO_SHADOW;MISSING_B_R_VALUE", "maps primarily to gamma/light-time and no-shadow vector", SRC_2829_ACQ, "ACQ2829_3_common_weyl"),
        ("SC2830_4_disformal", "d_R_to_vmq", "disformal/preferred-frame component", "derive no disformal slot or source d_R preferred-frame response", "MISSING_NO_DISFORMAL_SLOT;MISSING_D_R_VALUE;MISSING_ALPHA_I_KERNEL", "maps to preferred-frame PPN and clock channels", SRC_2829_ACQ, "ACQ2829_4_disformal"),
        ("SC2830_5_endpoint", "epsilon_endpoint_to_vmq", "endpoint/boundary component", "derive endpoint/boundary silence or source finite endpoint kernel", "MISSING_ENDPOINT_SILENCE;MISSING_BOUNDARY_KERNEL", "maps to orbital/light-time/R10/local projection tails", SRC_2829_ACQ, "ACQ2829_5_endpoint"),
    ]
    return [
        nonclaim(
            {
                "source_contract_id": row_id,
                "symbol": symbol,
                "component": component,
                "acquisition_rule": rule,
                "missing_inputs": missing,
                "claim_guard": guard,
                "source_path": str(source_path),
                "source_anchor": anchor,
                "anchor_found": anchor in read_text(source_path),
                "ready_for_manual_or_scripted_acquisition": True,
                "numeric_value_present": False,
                "source_backed_value": False,
                "theorem_zero": False,
                "control_only": True,
            }
        )
        for row_id, symbol, component, rule, missing, guard, source_path, anchor in specs
    ]


def arena_queue_rows() -> list[dict[str, Any]]:
    specs = [
        ("AQ2830_0_PPN", "PPN", "epsilon_vmq components -> Delta_PPN_abs", "fill response kernels for b_R,d_R,w_R,endpoint/readout and total no-cancellation vector", "P8_Y5_NO_SHADOW_PPN_VECTOR_2631_FULL_PPN_VECTOR_LEDGER.csv", SRC_2631_PPN_VECTOR, "PPNV2631_8_total_abs"),
        ("AQ2830_1_R10", "R10", "epsilon_vmq -> alpha_R10_q(lambda)", "fill q_profile(lambda), range kernel, c_q_alpha(lambda), units and real bound curve join", "P8_Y5_PARENT_QLOC_2192_R10_RESPONSE_OPERATOR_ROW.csv", SRC_2192_R10, "R10RESP2192_0_first_schema_operator"),
        ("AQ2830_2_clocks", "clocks", "epsilon_vmq_readout/d_R -> clock residual", "fill tau_clock_time, observed time vector, EM/clock owner if needed", "P8_Y5_R2FR_2675_SPECIES_CLOCK_FIRST_BOUND_FILL_NONCLAIM.csv", SRC_2675_CLOCK, "FILL2675_CLK2675_1_tau_readout"),
        ("AQ2830_3_WEP_source", "WEP/source_normalization", "epsilon_vmq_source_weight -> composition/source leg", "fill material/source tensor, WEP projection, source-leg owner", "P8_Y5_SOURCE_BRIDGE_2466_WEP_COMPOSITION_GUARDRAIL.csv", SRC_2466_WEP, "WEP2466_3_composition_bound"),
        ("AQ2830_4_orbital", "orbital/light_time", "epsilon_endpoint_to_vmq/readout -> orbital residual", "fill endpoint silence or orbital response kernel; keep measured-GM chain noncircular", "P8_Y5_GAUSS_ORBITAL_ACCEPTANCE_GATES.csv", SRC_ORBIT_GATES, "AG523_5_no_overclaim"),
    ]
    return [
        nonclaim(
            {
                "arena_queue_id": row_id,
                "arena": arena,
                "map": map_desc,
                "next_fill": next_fill,
                "target_interface": target,
                "source_path": str(source_path),
                "source_anchor": anchor,
                "anchor_found": anchor in read_text(source_path),
                "queue_status": "READY_FOR_NONCLAIM_SOURCE_ACQUISITION",
                "score_allowed": False,
                "control_only": True,
            }
        )
        for row_id, arena, map_desc, next_fill, target, source_path, anchor in specs
    ]


def readiness_rows() -> list[dict[str, Any]]:
    specs = [
        ("SR2830_0_source_values", "epsilon_vmq source values", "NOT_READY", "all epsilon_vmq values are missing or theorem-zero unsigned", False),
        ("SR2830_1_kernel_values", "response kernels", "NOT_READY", "kernel formulas are interfaces only; no complete arena kernel is score-ready", False),
        ("SR2830_2_Cqm", "C_qm/local lock", "NOT_READY", "E_q norm, v_m normalization and epsilon_vmq value/theorem-zero missing", False),
        ("SR2830_3_PPN", "PPN scoring", "NOT_READY", "full no-cancellation vector values/theorem-zeros missing", False),
        ("SR2830_4_R10", "R10 scoring", "NOT_READY", "alpha(lambda) mapping, q_profile, units and bound join missing", False),
        ("SR2830_5_clocks", "clock scoring", "NOT_READY", "tau/readout and clock normalization kernels missing", False),
        ("SR2830_6_orbital", "orbital scoring", "NOT_READY", "endpoint/orbital/light-time response and GM chain missing", False),
        ("SR2830_7_acquisition", "nonclaim acquisition", "READY", "symbols, blockers, anchors and arena queues are now explicit", False),
    ]
    return [
        nonclaim(
            {
                "readiness_id": row_id,
                "object": obj,
                "status": status,
                "reason": reason,
                "score_or_claim_allowed": allowed,
                "control_only": True,
            }
        )
        for row_id, obj, status, reason, allowed in specs
    ]


def gate_rows(rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    sources_ok = all(row["path_exists"] and row["anchors_found"] for row in rows["sources"])
    kernel_ok = all(row["anchor_found"] and not row["kernel_ready"] and not row["value_ready"] for row in rows["kernel_interface"])
    contract_ok = all(row["anchor_found"] and row["ready_for_manual_or_scripted_acquisition"] and not row["numeric_value_present"] for row in rows["source_contract"])
    queue_ok = all(row["anchor_found"] and not row["score_allowed"] for row in rows["arena_queue"])
    all_scores_blocked = not any(row["score_or_claim_allowed"] for row in rows["readiness"])
    specs = [
        ("CG2830_0_sources", "source anchors present", sources_ok, "all imported ledgers are reproducible"),
        ("CG2830_1_kernel_interface", "epsilon_vmq kernel interfaces written", kernel_ok, "interfaces cite sources but remain not ready/value-missing"),
        ("CG2830_2_source_contract", "epsilon_vmq acquisition contracts written", contract_ok, "contracts are ready for acquisition but contain no values"),
        ("CG2830_3_arena_queue", "arena projection queues written", queue_ok, "PPN/R10/clocks/WEP/orbital queues exist without scores"),
        ("CG2830_4_score_block", "all scoring blocked", all_scores_blocked, "readiness matrix allows acquisition only"),
        ("CG2830_5_Cqm", "C_qm promotable", False, "E_q/v_m/epsilon_vmq value still missing"),
        ("CG2830_6_local_GR", "local GR/Newton claim allowed", False, "finite coupling rows and response kernels are not sourced"),
        ("CG2830_7_PPN_R10", "PPN/R10/clock/orbital claim allowed", False, "arena queues are nonclaim interfaces only"),
    ]
    return [
        nonclaim(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "gate_passed": passed,
                "status": "PASS_NONCLAIM" if passed else "BLOCKED",
                "reason": reason,
            }
        )
        for gate_id, claim, passed, reason in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2830_0_kernel", "epsilon_vmq is now arena-routable.", "KERNEL_INTERFACE_BUILT", "PPN, R10, clocks, WEP/source and orbital queues know which component they need", "use queues for source/theorem-zero acquisition"),
        ("DEC2830_1_no_score", "No empirical score is allowed.", "VALUES_AND_KERNELS_MISSING", "all rows remain value-missing and nonclaim", "do not run PPN/R10/clock/orbital scoring"),
        ("DEC2830_2_Cqm", "C_qm remains blocked.", "NO_CQM_PROMOTION", "E_q norm, v_m normalization and epsilon_vmq value/theorem-zero are still missing", "do not reenter local-lock amplitude chain"),
        ("DEC2830_3_first_fill", "Best next fill is PPN/common-frame vector first.", "NEXT_2831_FIRST_KERNEL_FILL", "PPN vector has the richest existing response scaffold and catches Weyl, disformal, source and endpoint leaks at once", "attempt first theorem-zero/value fill for epsilon_vmq response components"),
    ]
    return [
        nonclaim(
            {
                "decision_id": decision_id,
                "decision": decision,
                "result": result,
                "because": because,
                "next_action": next_action,
            }
        )
        for decision_id, decision, result, because, next_action in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2830_0_2831",
                "status": "selected_primary",
                "target_doc": "2831-Y5-R2FR-first-epsilon-vmq-PPN-common-frame-kernel-fill-or-theorem-zero-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_first_epsilon_vmq_PPN_common_frame_kernel_fill_or_theorem_zero_under_AX1090_2831.py",
                "mission": "try the first epsilon_vmq response-kernel fill on the PPN/common-frame vector: prove theorem-zero for b_R/d_R/w_R/endpoint channels or keep source-ready finite rows without scoring",
                "acceptance": "must cite 2830 kernel interface and 2489/2631 PPN vector rows; no numeric placeholders; no cancellation shortcuts; no C_qm/local-GR/PPN claim; formalization-workbench untouched",
                "forbidden": "do not score Cassini/PPN from missing values; do not treat a single gamma kernel as full PPN; do not claim local GR",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("BR2830_0_kernel_copy", OUTPUTS["kernel_interface"], BRANCH_OUTPUTS["kernel_copy"], "source-weight copy of epsilon_vmq response-kernel interface"),
        ("BR2830_1_contract_copy", OUTPUTS["source_contract"], BRANCH_OUTPUTS["contract_copy"], "local-bounds copy of epsilon_vmq source-acquisition contract"),
        ("BR2830_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB acquisition queue for first epsilon_vmq PPN/common-frame kernel fill"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_table, copy_path, purpose in specs:
        copy_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_table, copy_path)
        rows.append(
            nonclaim(
                {
                    "copy_id": copy_id,
                    "source_table": str(source_table),
                    "copy_path": str(copy_path),
                    "purpose": purpose,
                    "exists": copy_path.exists(),
                }
            )
        )
    return rows


def iter_cited_paths(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[Path]:
    keys = {"source_path", "source_paths", "source_table", "copy_path"}
    paths: list[Path] = []
    for rows in rows_by_name.values():
        for row in rows:
            for key in keys:
                value = row.get(key)
                if value is None:
                    continue
                for token in str(value).split(";"):
                    item = token.strip()
                    if not item or item.startswith("http") or item.startswith("MISSING_"):
                        continue
                    path = Path(item)
                    if not path.is_absolute():
                        path = ROOT / item
                    paths.append(path)
    return paths


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for name, rows in rows_by_name.items():
        if name == "validation":
            continue
        for row in rows:
            for key in ("score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if str(row.get(key, "")).lower() == "true":
                    return False
    return True


def no_numeric_insertions(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    forbidden_numeric_keys = {"numeric_value", "coefficient", "alpha", "beta", "lambda_value"}
    for rows in rows_by_name.values():
        for row in rows:
            for key, value in row.items():
                if key in forbidden_numeric_keys and str(value).strip():
                    return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    start = SCRIPT_START_UTC.timestamp()
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            try:
                if path.stat().st_mtime >= start:
                    return False
            except OSError:
                return False
    return True


def under_root(paths: list[Path]) -> bool:
    root_text = str(ROOT.resolve()).lower()
    return all(str(path.resolve()).lower().startswith(root_text) for path in paths)


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_paths = [path for path in OUTPUTS.values() if path != OUTPUTS["validation"]]
    branch_paths = list(BRANCH_OUTPUTS.values())
    cited_paths = iter_cited_paths(rows_by_name)
    checks = [
        ("VAL2830_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2830_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2830_2_kernel_anchors", all(row["anchor_found"] for row in rows_by_name["kernel_interface"]), "all kernel-interface rows cite found anchors"),
        ("VAL2830_3_kernel_nonready", not any(row["kernel_ready"] or row["value_ready"] or row["theorem_zero_ready"] for row in rows_by_name["kernel_interface"]), "kernel interfaces remain value/theorem-zero not ready"),
        ("VAL2830_4_contract_ready_nonclaim", all(row["ready_for_manual_or_scripted_acquisition"] and not row["numeric_value_present"] and not row["source_backed_value"] for row in rows_by_name["source_contract"]), "source contracts are acquisition-ready but value-missing"),
        ("VAL2830_5_arena_queue_nonclaim", all(not row["score_allowed"] for row in rows_by_name["arena_queue"]), "arena queues do not allow scoring"),
        ("VAL2830_6_readiness_blocks_scores", not any(row["score_or_claim_allowed"] for row in rows_by_name["readiness"]), "readiness matrix blocks every score/claim"),
        ("VAL2830_7_claims_blocked", not any(row["claim_allowed"] for row in rows_by_name["gates"]), "no claim gate allows local GR/Newton/PPN/R10"),
        ("VAL2830_8_no_numeric_insertions", no_numeric_insertions(rows_by_name), "no numeric coefficients or prediction values inserted"),
        ("VAL2830_9_next_target_2831", any(row["next_id"] == "NEXT2830_0_2831" and row["selected"] for row in rows_by_name["next"]), "first epsilon_vmq PPN/common-frame kernel fill selected next"),
        ("VAL2830_10_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2830_11_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2830_12_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2830_13_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2830_14_no_claim_flags", no_claim_flags(rows_by_name), "no score_ready, valid_prediction_row, valid_for_claim, or claim_allowed flag is true"),
        ("VAL2830_15_generated_under_post_checkpoint", under_root(output_paths + branch_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2830_16_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2830_17_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [
        {
            "validation_id": validation_id,
            "passed": passed,
            "detail": detail,
            "timestamp_utc": ts(),
        }
        for validation_id, passed, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2830_OVERALL",
            "passed": overall,
            "detail": "2830 turns epsilon_vmq source-ready rows into nonclaim response-kernel and arena-acquisition interfaces, keeps all values/kernels missing, blocks C_qm/local-lock/arena scoring, and selects the first PPN/common-frame kernel fill next.",
            "timestamp_utc": ts(),
        }
    )
    return rows


def md(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    content = f"""# 2830 - Y5 R2FR epsilon_vmq Response Kernels And Source Acquisition Interface Under AX1090

Status: `Y5_R2FR_2830_epsilon_vmq_kernel_interfaces_written_no_scores`

## Private Verdict

2830 does the boring-but-essential plumbing: `epsilon_vmq` is now wired to the arenas that would eventually test it.

No physics score is produced. No coefficient is inserted. No `C_qm` promotion occurs.

The useful gain is that the coupling debt now has explicit response-kernel interfaces for PPN, R10, clocks, WEP/source-normalization, orbital/light-time, and local-GR gates. Each interface says what must be theorem-zero or source-backed before scoring.

## Source Register

{markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## epsilon_vmq Response Kernel Interface

{markdown_table(rows["kernel_interface"], ["kernel_interface_id", "kernel_family", "epsilon_input", "interface_formula", "current_status", "test_arenas", "kernel_ready", "value_ready", "valid_for_claim"])}

## epsilon_vmq Source Acquisition Contract

{markdown_table(rows["source_contract"], ["source_contract_id", "symbol", "component", "acquisition_rule", "missing_inputs", "ready_for_manual_or_scripted_acquisition", "numeric_value_present", "valid_for_claim"])}

## Arena Projection Queue

{markdown_table(rows["arena_queue"], ["arena_queue_id", "arena", "map", "next_fill", "queue_status", "score_allowed", "valid_for_claim"])}

## Score Readiness Matrix

{markdown_table(rows["readiness"], ["readiness_id", "object", "status", "reason", "score_or_claim_allowed", "valid_for_claim"])}

## Claim Gates

{markdown_table(rows["gates"], ["claim_gate_id", "claim", "gate_passed", "status", "reason", "claim_allowed"])}

## Decision Ledger

{markdown_table(rows["decision"], ["decision_id", "decision", "result", "because", "next_action", "valid_for_claim"])}

## Next Target

{markdown_table(rows["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(rows["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(rows["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows: dict[str, list[dict[str, Any]]] = {}
    rows["sources"] = source_rows()
    rows["kernel_interface"] = kernel_interface_rows()
    rows["source_contract"] = source_contract_rows()
    rows["arena_queue"] = arena_queue_rows()
    rows["readiness"] = readiness_rows()
    rows["gates"] = gate_rows(rows)
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "kernel_interface", "source_contract", "arena_queue", "readiness", "gates", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])

    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2830_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2830_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()

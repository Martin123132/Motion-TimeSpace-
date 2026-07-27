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

BRANCH_ID = "MTS_R2FR_MHREF_TAU_SURFACE_LOCK_2596"
CHECKPOINT_ID = "2596"

DOC = ROOT / "2596-Y5-R2FR-MHref-tau-source-frame-surface-lock-or-first-denominator-row.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_MHREF_2596_SOURCE_REGISTER.csv",
    "lock_audit": OUT / "P8_Y5_MHREF_2596_LOCK_AUDIT.csv",
    "denominator_rows": OUT / "P8_Y5_MHREF_2596_DENOMINATOR_ROWS.csv",
    "runner_refusal": OUT / "P8_Y5_MHREF_2596_RUNNER_REFUSAL.csv",
    "claim_gates": OUT / "P8_Y5_MHREF_2596_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_MHREF_2596_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_MHREF_2596_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_MHREF_2596_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2596_VALIDATION.csv",
}

COPY_TARGETS = {
    "lock_audit": QUEUE / "JR2596_MHREF_TAU_SURFACE_LOCK_AUDIT_NONCLAIM.csv",
    "denominator_rows": LOCAL_BOUNDS / "MHref_tau_surface_denominator_rows_2596_NONCLAIM.csv",
    "next_target": QUEUE / "JR2596_TAU_IDENTITY_OR_MHREF_SOURCE_ACQUISITION_NEXT.csv",
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
            "source_id": "SRC2596_00_2595_handoff",
            "source_path": ROOT / "2595-Y5-R2FR-GM-transfer-PiM-equality-commutator-or-source-normalization-bound.md",
            "needles": ["NEXT2595_0_selected", "GMT2595_6_MHref_tau_surface", "VAL2595_OVERALL"],
            "role": "active handoff selecting M_H_ref/tau/surface lock",
        },
        {
            "source_id": "SRC2596_01_2595_next_queue",
            "source_path": QUEUE / "JR2595_MHREF_TAU_FRAME_LOCK_NEXT.csv",
            "needles": ["NEXT2595_0_selected", "2596-Y5-R2FR-MHref-tau-source-frame-surface-lock-or-first-denominator-row.md"],
            "role": "machine-readable 2596 task and guardrails",
        },
        {
            "source_id": "SRC2596_02_1519_doc",
            "source_path": ROOT / "1519-Y5-parent-observed-coframe-tau-source-frame-lock-or-MHref-first-row.md",
            "needles": ["MHR1519_7_MHref", "MHR1519_8_surfaces", "VAL1519_14_overall"],
            "role": "prior M_H_ref first-row schema and observed-frame/tau lock",
        },
        {
            "source_id": "SRC2596_03_1519_schema",
            "source_path": OUT / "P8_Y5_PARENT_FRAME_1519_MHREF_FIRST_ROW_SCHEMA.csv",
            "needles": ["MHR1519_7_MHref", "MHR1519_10_acceptance"],
            "role": "machine M_H_ref first-row schema",
        },
        {
            "source_id": "SRC2596_04_1519_acquisition",
            "source_path": OUT / "P8_Y5_PARENT_FRAME_1519_DENOMINATOR_ACQUISITION_LEDGER.csv",
            "needles": ["ACQ1519_4_Htau_surface_charge", "ACQ1519_8_acceptance"],
            "role": "denominator/source acquisition ledger",
        },
        {
            "source_id": "SRC2596_05_1518_mhref_surface",
            "source_path": OUT / "P8_Y5_PARENT_PIM_1518_MHREF_SURFACE_LOCK.csv",
            "needles": ["MH1518_0_M_H_ref", "MH1518_4_tau_frame", "MH1518_7_acceptance"],
            "role": "PiM commutator denominator/surface lock rows",
        },
        {
            "source_id": "SRC2596_06_2390_same_frame",
            "source_path": ROOT / "2390-Y5-R2FR-observed-coframe-pullback-same-frame-lock-or-frame-source-leak-values.md",
            "needles": ["SFL2390_3_tau_lock", "SFL2390_5_MHref_link", "VAL2390_OVERALL"],
            "role": "same-frame coframe/tau/MHref anti-circularity gate",
        },
        {
            "source_id": "SRC2596_07_2588_observed_stack",
            "source_path": ROOT / "2588-Y5-R2FR-observed-stack-q-eobs-tau-parent-owner-or-source-leak-fill.md",
            "needles": ["OSA2588_5_tau_identity", "OSC2588_7_MHref", "VAL2588_OVERALL"],
            "role": "observed-stack q/e_obs/tau/MHref ownership gaps",
        },
        {
            "source_id": "SRC2596_08_1008_theta_qtau",
            "source_path": ROOT / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md",
            "needles": ["PVA1008_1_theta_MTS", "QTA1008_8_Q_total", "CG1008_1_Qtau_total"],
            "role": "theta_MTS/Q_tau total extraction still missing",
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


def lock_audit_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "lock_id": "MHL2596_0_system_worldtube",
            "lock_piece": "system and source worldtube identity",
            "required_identity": "system_id and source worldtube W_M are fixed before readout and shared by J_H, Q_M, S1/S2, A_ext and orbital readout",
            "current_status": "MISSING_SYSTEM_AND_WORLDTUBE_ID",
            "why_needed": "anonymous denominator rows cannot prove a source-transfer theorem",
            "residual_if_missing": "system_id;worldtube_id;source_support_lock",
        },
        {
            "lock_id": "MHL2596_1_observed_coframe",
            "lock_piece": "observed coframe/q/Obs_e",
            "required_identity": "e_obs/coframe_id is parent-owned through q/Obs_e before matter, source, clock, boundary and orbit readout",
            "current_status": "MISSING_PARENT_Q_OBS_E_OWNER",
            "why_needed": "M_H_ref must be in the same source frame as the equality/commutator rows",
            "residual_if_missing": "e_obs_coframe_lock;epsilon_q_owner;Delta_frame_source_over_MH",
        },
        {
            "lock_id": "MHL2596_2_tau_identity",
            "lock_piece": "single tau identity",
            "required_identity": "tau_source=tau_charge=tau_clock=tau_orbit=tau_boundary=tau_obs[e_obs]",
            "current_status": "MISSING_TAU_FRAME_LOCK",
            "why_needed": "different time generators can make the same charge look like different masses",
            "residual_if_missing": "tau_frame_lock;epsilon_tau_selector",
        },
        {
            "lock_id": "MHL2596_3_theta_Qtau",
            "lock_piece": "theta_MTS and Q_tau^MTS",
            "required_identity": "theta_MTS and Q_tau^MTS include EH, boundary, extra, projector and matter/source sectors",
            "current_status": "MISSING_THETA_QTAU_TOTAL",
            "why_needed": "EH-only Hamiltonian charge is not the MTS parent source charge",
            "residual_if_missing": "theta_MTS_source;Q_tau_MTS_source",
        },
        {
            "lock_id": "MHL2596_4_Htau_Href",
            "lock_piece": "H_tau-H_ref denominator",
            "required_identity": "M_H_ref=H_tau[S_outer]-H_ref is positive, finite, integrable and fixed before source/readout fitting",
            "current_status": "MISSING_H_TAU_H_REF_MHREF",
            "why_needed": "R_eq and I_commutator require a noncircular denominator",
            "residual_if_missing": "M_H_ref;H_tau;H_ref;delta_H_tau_curl",
        },
        {
            "lock_id": "MHL2596_5_surfaces_annulus",
            "lock_piece": "linked surfaces and annulus",
            "required_identity": "S1, S2, A_ext, r1, r2, homology class and source-free exterior are fixed before readout",
            "current_status": "MISSING_SURFACE_HOMOLOGY_LOCK",
            "why_needed": "post-readout surfaces can make commutator/equality residuals disappear by mask choice",
            "residual_if_missing": "surface_homology_lock;annulus_metadata",
        },
        {
            "lock_id": "MHL2596_6_units_positivity_acceptance",
            "lock_piece": "units, positivity and anti-circularity acceptance",
            "required_identity": "all rows have units/source paths/no MISSING markers and reject orbital GM, EH-only charge, fitted counterterms and post-readout frames",
            "current_status": "CLAIM_BLOCKED",
            "why_needed": "a denominator row is dangerous unless it is source-backed and noncircular",
            "residual_if_missing": "denominator_acceptance_gate",
        },
        {
            "lock_id": "MHL2596_7_verdict",
            "lock_piece": "current verdict",
            "required_identity": "MHL2596_0 through MHL2596_6 all pass in the same branch",
            "current_status": "MHREF_TAU_SURFACE_LOCK_NOT_DERIVED_CURRENT_CORPUS",
            "why_needed": "the PiM equality/commutator runner cannot be scored yet",
            "residual_if_missing": "Delta_MHref_tau_surface_total",
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False, "claim_allowed": False}) for row in rows]


def denominator_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "MHD2596_0_system",
            "symbol": "system_worldtube_lock",
            "definition": "unique system_id, source worldtube W_M and source support fixed before readout",
            "units": "identifier_and_support_metadata",
            "current_value": "MISSING_SYSTEM_ID;MISSING_WORLDTUBE_ID;MISSING_SOURCE_SUPPORT_LOCK",
            "source_path": ROOT / "1519-Y5-parent-observed-coframe-tau-source-frame-lock-or-MHref-first-row.md",
            "observable_link": "source_mass;GM_transfer",
        },
        {
            "row_id": "MHD2596_1_coframe",
            "symbol": "e_obs_coframe_lock",
            "definition": "observed coframe fixed by q/Obs_e before matter/source/clock/orbit/boundary readout",
            "units": "certificate",
            "current_value": "MISSING_COFRAME_ID;MISSING_PARENT_Q_OBS_E_OWNER",
            "source_path": ROOT / "2588-Y5-R2FR-observed-stack-q-eobs-tau-parent-owner-or-source-leak-fill.md",
            "observable_link": "same_frame;WEP;PPN;clock;orbital",
        },
        {
            "row_id": "MHD2596_2_tau",
            "symbol": "tau_frame_lock",
            "definition": "same tau for source, charge, clocks, orbit, boundary and readout",
            "units": "certificate",
            "current_value": "MISSING_TAU_LOCK",
            "source_path": ROOT / "2390-Y5-R2FR-observed-coframe-pullback-same-frame-lock-or-frame-source-leak-values.md",
            "observable_link": "clock;Hamiltonian_charge;source_mass;orbital",
        },
        {
            "row_id": "MHD2596_3_theta",
            "symbol": "theta_MTS_source",
            "definition": "full parent symplectic potential including EH/boundary/extra/projector/matter-source sectors",
            "units": "equation_source",
            "current_value": "MISSING_THETA_MTS_SOURCE",
            "source_path": ROOT / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md",
            "observable_link": "Hamiltonian_integrability;M_H_ref",
        },
        {
            "row_id": "MHD2596_4_Qtau",
            "symbol": "Q_tau_MTS_source",
            "definition": "total parent Hamiltonian/Noether charge form for tau",
            "units": "charge_form_source",
            "current_value": "MISSING_Q_TAU_MTS_SOURCE",
            "source_path": ROOT / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md",
            "observable_link": "Hamiltonian_charge;M_H_ref",
        },
        {
            "row_id": "MHD2596_5_MHref",
            "symbol": "M_H_ref",
            "definition": "positive finite H_tau-H_ref in same e_obs/tau/source branch, not orbital GM",
            "units": "mass_or_energy_units",
            "current_value": "MISSING_M_H_REF",
            "source_path": OUT / "P8_Y5_PARENT_FRAME_1519_MHREF_FIRST_ROW_SCHEMA.csv",
            "observable_link": "normalization;PiM_runner;GM_transfer",
        },
        {
            "row_id": "MHD2596_6_surfaces",
            "symbol": "surface_homology_lock",
            "definition": "S1/S2/A_ext/r1/r2/homology/source-free exterior fixed before readout",
            "units": "surface_and_topology_metadata",
            "current_value": "MISSING_SURFACE_HOMOLOGY",
            "source_path": OUT / "P8_Y5_PARENT_PIM_1518_MHREF_SURFACE_LOCK.csv",
            "observable_link": "I_commutator;R_eq_integral;radial_Meff",
        },
        {
            "row_id": "MHD2596_7_integrability",
            "symbol": "delta_H_tau_curl",
            "definition": "field-space curl/integrability defect of H_tau with fixed reference",
            "units": "dimensionless_or_charge_curl_units",
            "current_value": "MISSING_INTEGRABILITY_CERTIFICATE",
            "source_path": OUT / "P8_Y5_PARENT_FRAME_1519_MHREF_FIRST_ROW_SCHEMA.csv",
            "observable_link": "Hamiltonian_integrability;M_H_ref",
        },
        {
            "row_id": "MHD2596_TOTAL",
            "symbol": "Delta_MHref_tau_surface_total",
            "definition": "absolute nonclaim envelope over system, coframe, tau, theta, Q_tau, M_H_ref, surfaces and integrability gaps",
            "units": "mixed_gate_not_score_ready",
            "current_value": "COMPONENTS_MISSING",
            "source_path": DOC,
            "observable_link": "GM_transfer;PiM_runner;Newton;local_GR",
        },
    ]
    return [
        with_stamp(
            {
                **row,
                "source_path_exists": Path(row["source_path"]).exists() if row["source_path"] != DOC else True,
                "score_ready": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        for row in rows
    ]


def runner_refusal_rows(denominator_data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in denominator_data:
        reasons = ["VALID_FOR_CLAIM_FALSE", "MISSING_ZERO_THEOREM_OR_NUMERIC_VALUE"]
        if not row["source_path_exists"]:
            reasons.append("MISSING_SOURCE_PATH")
        if row["symbol"] == "M_H_ref":
            reasons.append("ORBITAL_GM_DENOMINATOR_REJECTED")
        if row["symbol"] == "tau_frame_lock":
            reasons.append("MULTI_TAU_SOURCE_CHARGE_CLOCK_ORBIT_RISK")
        if row["row_id"] == "MHD2596_TOTAL":
            reasons.append("DENOMINATOR_COMPONENTS_NOT_SCORE_READY")
        rows.append(
            with_stamp(
                {
                    "runner_id": f"MHR2596_{row['row_id']}",
                    "target_id": row["row_id"],
                    "symbol": row["symbol"],
                    "verdict": "REFUSED_NONCLAIM_MHREF_DENOMINATOR_ROW",
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
            "gate_id": "CG2596_0_schema",
            "claim": "M_H_ref/tau/surface first-row schema is explicit",
            "gate_status": "PASS_NONCLAIM_STRUCTURE_ONLY",
            "reason": "system, coframe, tau, theta, Q_tau, M_H_ref, surfaces and integrability rows are named",
            "gate_pass": True,
        },
        {
            "gate_id": "CG2596_1_EH_only",
            "claim": "EH Hamiltonian charge alone supplies MTS M_H_ref",
            "gate_status": "REJECTED_SHORTCUT",
            "reason": "theta_MTS/Q_tau^MTS retained sectors are not extracted or zeroed",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2596_2_orbital_GM",
            "claim": "observed orbital GM can be used as M_H_ref",
            "gate_status": "REJECTED_SHORTCUT",
            "reason": "orbital GM is the transfer target, not a denominator proof input",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2596_3_post_readout_surfaces",
            "claim": "surfaces/support can be chosen after seeing residuals",
            "gate_status": "REJECTED_SHORTCUT",
            "reason": "post-readout masks can erase equality/commutator residuals",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2596_4_denominator_score_ready",
            "claim": "R_eq/I_commutator denominator rows are score-ready",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "M_H_ref, tau, coframe, surfaces, theta/Qtau and integrability are missing",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2596_5_Newton_local_GR",
            "claim": "source-normalized Newton/local GR is derived",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "denominator/source-frame lock is upstream and unclosed",
            "gate_pass": False,
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False, "claim_allowed": False}) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2596_0_schema_retained",
            "decision": "MHREF_FIRST_ROW_SCHEMA_RETAINED",
            "reason": "the PiM runner cannot be scored without a positive same-frame noncircular denominator",
            "effect": "M_H_ref/tau/surface rows are promoted to the current bottleneck",
        },
        {
            "decision_id": "DEC2596_1_no_denominator_claim",
            "decision": "MHREF_TAU_SURFACE_LOCK_NOT_DERIVED",
            "reason": "system, q/Obs_e, tau, theta, Q_tau, H_tau/H_ref, surfaces and integrability are not source-backed",
            "effect": "R_eq/I_commutator and source-normalized Newton stay blocked",
        },
        {
            "decision_id": "DEC2596_2_next",
            "decision": "TAU_IDENTITY_OR_MHREF_SOURCE_ACQUISITION_SELECTED_NEXT",
            "reason": "same tau/source/charge/clock/orbit identity is the narrowest denominator lock and feeds every M_H_ref row",
            "effect": "2597 should attempt tau identity theorem or fill first source-backed M_H_ref/tau/surface acquisition rows",
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False}) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2596_0_selected",
            "selection_status": "selected",
            "target_file": "2597-Y5-R2FR-tau-identity-source-charge-clock-orbit-or-MHref-source-acquisition.md",
            "target_script": "scripts/Y5_R2FR_tau_identity_source_charge_clock_orbit_or_MHref_source_acquisition_2597.py",
            "task": "try to prove one parent tau generates source, Hamiltonian charge, clocks, orbit and boundary reference in the same q/e_obs branch; otherwise fill first source-backed M_H_ref/tau/surface acquisition rows",
            "success_condition": "tau_frame_lock and M_H_ref denominator rows become source-backed enough to start scoring R_eq/I_commutator",
            "fallback_condition": "nonclaim rows for tau_source/tau_charge/tau_clock/tau_orbit/tau_boundary, H_tau, H_ref, S1/S2/A_ext, units and source paths",
            "guardrails": "no orbital GM denominator; no EH-only tau charge; no post-readout frame/surface; no Newton/local-GR claim; no GitHub; no formalization-workbench edits",
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
                    "copy_id": f"COPY2596_{copy_id}",
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

    add("VAL2596_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and needles are present")
    required_lock_ids = {f"MHL2596_{idx}_{name}" for idx, name in [(0, "system_worldtube"), (1, "observed_coframe"), (2, "tau_identity"), (3, "theta_Qtau"), (4, "Htau_Href"), (5, "surfaces_annulus"), (6, "units_positivity_acceptance"), (7, "verdict")]}
    present_lock_ids = {row["lock_id"] for row in data["lock_audit"]}
    add("VAL2596_01_lock_audit_complete", required_lock_ids.issubset(present_lock_ids), "M_H_ref/tau/surface lock audit covers all required clauses")
    required_symbols = {"system_worldtube_lock", "e_obs_coframe_lock", "tau_frame_lock", "theta_MTS_source", "Q_tau_MTS_source", "M_H_ref", "surface_homology_lock", "delta_H_tau_curl", "Delta_MHref_tau_surface_total"}
    present_symbols = {row["symbol"] for row in data["denominator_rows"]}
    add("VAL2596_02_denominator_rows_present", required_symbols.issubset(present_symbols), "denominator rows cover system, frame, tau, charge, surfaces and total")
    add("VAL2596_03_denominator_sources_exist", all(row["source_path_exists"] is True for row in data["denominator_rows"]), "denominator rows point to existing local sources")
    add("VAL2596_04_rows_nonclaim", all(row["score_ready"] is False and row["valid_for_claim"] is False for row in data["denominator_rows"]), "denominator rows remain non-score-ready and nonclaim")
    add("VAL2596_05_runner_refuses", all(row["score_ready"] is False and row["claim_allowed"] is False for row in data["runner_refusal"]), "runner refuses all unfilled denominator rows")
    add(
        "VAL2596_06_claim_gates_safe",
        all(row["claim_allowed"] is False for row in data["claim_gates"])
        and any(row["gate_id"] == "CG2596_2_orbital_GM" and row["gate_status"] == "REJECTED_SHORTCUT" for row in data["claim_gates"]),
        "EH-only/orbital-GM/post-readout shortcuts and local-GR claims remain blocked",
    )
    add("VAL2596_07_no_claim_flags", generated_rows_have_no_claim_flags(data), "no generated row sets valid_for_claim=true or claim_allowed=true")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in (
            "*2596-Y5-R2FR-MHref*",
            "*Y5_R2FR_MHref_tau*",
            "*P8_Y5_MHREF_2596*",
            "*JR2596*",
        ):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL2596_08_no_formalization_artifacts",
        not formalization_artifacts,
        "no 2596 artifacts were written to formalization-workbench",
        ";".join(str(path) for path in formalization_artifacts),
    )
    add("VAL2596_09_next_selected", any(row["route_id"] == "NEXT2596_0_selected" and "2597-Y5-R2FR-tau-identity" in row["target_file"] for row in data["next"]), "2597 tau identity/source-acquisition target selected next")
    add("VAL2596_10_branch_copies", all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]), "nonclaim branch copies exist")

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2596_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2596_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2596_OVERALL",
        overall,
        "2596 refreshes the M_H_ref/tau/source-frame/surface first-row schema, rejects circular denominators and post-readout surfaces, keeps rows nonclaim, and selects tau identity/source acquisition next",
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
        "# 2596 Y5 R2FR MHref tau source-frame surface lock or first denominator row",
        "",
        "**Status:** private nonclaim derivation checkpoint. The denominator/source-frame schema is strict, but current MTS still does not parent-sign `M_H_ref`, one tau, one observed coframe, or fixed linked surfaces.",
        "",
        "**Main result:** the PiM equality and commutator rows cannot be scored until `M_H_ref=H_tau-H_ref` is positive, same-frame, source-backed, noncircular, and tied to fixed `S1/S2/A_ext` surfaces in one q/e_obs/tau branch. Orbital `GM`, EH-only charge, post-readout surfaces, and fitted references are rejected.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role", "valid_for_claim"]),
        "",
        "## Lock Audit",
        markdown_table(data["lock_audit"], ["lock_id", "lock_piece", "required_identity", "current_status", "why_needed", "residual_if_missing", "valid_for_claim", "claim_allowed"]),
        "",
        "## Denominator Rows",
        markdown_table(data["denominator_rows"], ["row_id", "symbol", "definition", "units", "current_value", "source_path", "source_path_exists", "observable_link", "score_ready", "valid_for_claim", "claim_allowed"]),
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
        "This is a boring-looking but crucial lock. A beautiful charge identity is useless if the denominator is circular or from another frame. The next best move is the tau identity: one parent time generator for source, Hamiltonian charge, clocks, orbit and boundary reference, or the first honest source-acquisition rows.",
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)

    denominator_data = denominator_rows()
    data = {
        "sources": source_register_rows(),
        "lock_audit": lock_audit_rows(),
        "denominator_rows": denominator_data,
        "runner_refusal": runner_refusal_rows(denominator_data),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["lock_audit"], data["lock_audit"])
    write_csv(OUTPUTS["denominator_rows"], data["denominator_rows"])
    write_csv(OUTPUTS["runner_refusal"], data["runner_refusal"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])

    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])

    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)

    overall = next(row for row in data["validations"] if row["check_id"] == "VAL2596_OVERALL")
    print(f"{overall['check_id']} {overall['status']}: {overall['notes']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

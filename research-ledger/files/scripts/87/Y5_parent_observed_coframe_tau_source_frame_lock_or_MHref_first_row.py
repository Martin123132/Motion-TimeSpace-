from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1519-Y5-parent-observed-coframe-tau-source-frame-lock-or-MHref-first-row.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1518_validation": OUT / "P8_Y5_BRR545_1518_VALIDATION.csv",
    "1518_next": OUT / "P8_Y5_PARENT_PIM_1518_NEXT_TARGET.csv",
    "1518_mhref": OUT / "P8_Y5_PARENT_PIM_1518_MHREF_SURFACE_LOCK.csv",
    "1361_doc": ROOT / "1361-Y5-R10-RAB-observed-coframe-tau-source-frame-lock-or-MHref-first-row.md",
    "1361_frame": OUT / "P8_Y5_R10_1361_FRAME_TAU_RESIDUAL_LEDGER.csv",
    "1361_mhref": OUT / "P8_Y5_R10_1361_MHREF_FIRST_ROW_SCHEMA.csv",
    "1362_doc": ROOT / "1362-Y5-R10-RAB-quotient-observed-coframe-parent-qObs-or-MHref-denominator-source-pack.md",
    "1362_qobs": OUT / "P8_Y5_R10_1362_QOBS_PARENT_CONSTRUCTION_ATTEMPT.csv",
    "1362_denominator": OUT / "P8_Y5_R10_1362_MHREF_DENOMINATOR_SOURCE_PACK.csv",
    "1363_doc": ROOT / "1363-Y5-R10-RAB-parent-qObs-current-chain-bridge-or-Htau-Href-first-source-row.md",
    "1363_bridge": OUT / "P8_Y5_R10_1363_QOBS_CURRENT_CHAIN_BRIDGE_ATTEMPT.csv",
    "1363_hrow": OUT / "P8_Y5_R10_1363_HTAU_HREF_FIRST_SOURCE_ROW.csv",
    "1364_doc": ROOT / "1364-Y5-R10-RAB-quotient-basic-parent-action-sector-audit-or-Htau-Href-source-acquisition.md",
    "1364_sector": OUT / "P8_Y5_R10_1364_QUOTIENT_BASIC_SECTOR_AUDIT.csv",
    "1364_acq": OUT / "P8_Y5_R10_1364_HTAU_HREF_SOURCE_ACQUISITION_LEDGER.csv",
    "1365_doc": ROOT / "1365-Y5-R10-RAB-Gamma-Khat-qbasic-sector-repair-or-q_loc-bound-source-row.md",
    "1365_qbound": OUT / "P8_Y5_R10_1365_QLOC_BOUND_SOURCE_ROW.csv",
    "1366_doc": ROOT / "1366-Y5-R10-RAB-Gamma-eff-scalar-density-definition-hunt-or-q_loc-envelope.md",
    "1366_hunt": OUT / "P8_Y5_R10_1366_GAMMA_EFF_SCALAR_DENSITY_HUNT_LEDGER.csv",
    "1366_env": OUT / "P8_Y5_R10_1366_QLOC_ENVELOPE_INTAKE_ROWS.csv",
    "1367_doc": ROOT / "1367-Y5-R10-RAB-Kmetric-memory-scalar-chain-kernel-or-q_loc-arena-thresholds.md",
    "1367_kernel": OUT / "P8_Y5_R10_1367_KMETRIC_CHAIN_KERNEL_ATTEMPT.csv",
    "1367_threshold": OUT / "P8_Y5_R10_1367_QLOC_ARENA_THRESHOLD_INTAKE.csv",
    "1368_doc": ROOT / "1368-Y5-R10-RAB-m-Lcg-parent-metric-response-kernels-or-q_loc-projection-map.md",
    "1368_lcg": OUT / "P8_Y5_R10_1368_M_LCG_KERNEL_HUNT.csv",
    "1368_projection": OUT / "P8_Y5_R10_1368_QLOC_TO_PPN_GAMMA_PROJECTION_REQUIREMENTS.csv",
    "1369_doc": ROOT / "1369-Y5-R10-RAB-Lcg-parent-definition-metric-silence-or-q_loc-gamma-projection-runner.md",
    "1369_lcg": OUT / "P8_Y5_R10_1369_LCG_PARENT_DEFINITION_HUNT.csv",
    "1369_runner": OUT / "P8_Y5_R10_1369_QLOC_GAMMA_RUNNER_SCHEMA.csv",
    "1369_next": OUT / "P8_Y5_R10_1369_NEXT_TARGET.csv",
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_FRAME_1519_SOURCE_REGISTER.csv"
COFRAME_LOCK_AUDIT = OUT / "P8_Y5_PARENT_FRAME_1519_COFRAME_TAU_LOCK_AUDIT.csv"
QOBS_ROUTE_AUDIT = OUT / "P8_Y5_PARENT_FRAME_1519_QOBS_ROUTE_AUDIT.csv"
MHREF_SCHEMA = OUT / "P8_Y5_PARENT_FRAME_1519_MHREF_FIRST_ROW_SCHEMA.csv"
DENOMINATOR_ACQUISITION = OUT / "P8_Y5_PARENT_FRAME_1519_DENOMINATOR_ACQUISITION_LEDGER.csv"
LOCAL_BLOCKER_ROLLUP = OUT / "P8_Y5_PARENT_FRAME_1519_LOCAL_HARD_BLOCKER_ROLLUP.csv"
REJECTION_LEDGER = OUT / "P8_Y5_PARENT_FRAME_1519_REJECTION_LEDGER.csv"
DECISION = OUT / "P8_Y5_PARENT_FRAME_1519_DECISION.csv"
LOCAL_STATUS = OUT / "P8_Y5_PARENT_FRAME_1519_LOCAL_GR_NEWTON_STATUS.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_FRAME_1519_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1519_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1519"
QUAR_COFRAME = QUARANTINE / "FRAME_COFRAME_TAU_LOCK_AUDIT_NONCLAIM.csv"
QUAR_MHREF = QUARANTINE / "FRAME_MHREF_FIRST_ROW_SCHEMA_NONCLAIM.csv"
QUAR_BLOCKER = QUARANTINE / "FRAME_LOCAL_HARD_BLOCKER_ROLLUP_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "FRAME_DECISION_NONCLAIM.csv"
BRANCH_COFRAME = BRANCH_RESIDUALS / "frame_coframe_tau_lock_audit_nonclaim_1519.csv"
BRANCH_MHREF = BRANCH_RESIDUALS / "frame_mhref_first_row_schema_nonclaim_1519.csv"
BRANCH_BLOCKER = BRANCH_RESIDUALS / "frame_local_hard_blocker_rollup_nonclaim_1519.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "frame_decision_nonclaim_1519.csv"


def flags() -> dict[str, bool]:
    return {
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
    rows = []
    for source_id, (key, path) in enumerate(SOURCE_FILES.items()):
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1519_{source_id}_{key}",
                "source_path": rel(path),
                "exists": path.exists(),
                "purpose": "input evidence for the 1519 observed-coframe/tau/MHref consolidation gate",
                **flags(),
            }
        )
    return rows


def coframe_lock_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "OCF1519_0_conditional_descent",
            "if e_obs=Obs_e(q(Phi)) and Dq(v)=0 then Lie_v e_obs=0",
            "VALID_CONDITIONAL_LEMMA",
            "good theorem route, but not live evidence until q, Obs_e, v in ker(Dq), and matter descent are parent-signed",
            source_list("1361_doc", "1362_qobs"),
        ),
        (
            "OCF1519_1_parent_q",
            "parent quotient map q: Phi_parent -> Q_obs",
            "NOT_PARENT_SIGNED",
            "representative variables can remain physically visible without a field list, equivalence relation, and kernel basis",
            source_list("1362_doc", "1362_qobs"),
        ),
        (
            "OCF1519_2_observed_coframe",
            "observed coframe functor Obs_e(q)",
            "NOT_CONSTRUCTED",
            "frame leakage b_g/b_dis can survive if coframe choice is made after readout",
            source_list("1361_frame", "1362_qobs"),
        ),
        (
            "OCF1519_3_matter_constants",
            "masses, charges, clock constants, material labels descend through q",
            "NOT_PARENT_SIGNED",
            "metric coframe descent alone does not prove universal coupling or clock/source normalization",
            source_list("1362_doc", "1364_sector"),
        ),
        (
            "OCF1519_4_tau_lock",
            "tau_source=tau_charge=tau_clock=tau_orbit=tau_boundary",
            "MISSING_TAU_LOCK",
            "H_tau, source support, clocks, and orbit can use different time readouts",
            source_list("1361_frame", "1364_acq"),
        ),
        (
            "OCF1519_5_no_shadow_frame",
            "no representative Weyl/disformal/source frame before quotient",
            "CLASSIFICATION_ONLY_NOT_ZERO_THEOREM",
            "representative frame coefficients stay as residual rows until no-shadow theorem or bounds exist",
            source_list("1361_frame", "1362_doc"),
        ),
        (
            "OCF1519_6_MHref_denominator",
            "positive same-frame M_H_ref = H_tau - H_ref",
            "MISSING_SOURCE_INPUT",
            "without H_tau/H_ref/Q_tau/theta/frame rows the commutator runner cannot normalize Newton-source transfer",
            source_list("1518_mhref", "1361_mhref", "1363_hrow"),
        ),
        (
            "OCF1519_7_verdict",
            "current MTS proves one observed coframe plus tau/source/charge/readout lock",
            "COFRAME_TAU_LOCK_NOT_PROVED",
            "keep M_H_ref as source-acquisition schema and do not claim local GR/Newton",
            source_list("1361_doc", "1362_doc", "1363_doc", "1364_doc"),
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "claim_piece": claim_piece,
            "current_status": status,
            "why_it_matters": why,
            "source_paths": sources,
            **flags(),
        }
        for audit_id, claim_piece, status, why, sources in rows
    ]


def qobs_route_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "QOR1519_0_qObs_descent",
            "q/Obs_e descent route",
            "CONDITIONAL_ROUTE_REAL",
            "chain-rule vertical blindness is valid but requires parent q, Obs_e, and Dq(v)=0",
            source_list("1362_qobs"),
        ),
        (
            "QOR1519_1_current_chain_bridge",
            "qObs-current-chain bridge",
            "EXACT_CONDITIONAL_BRIDGE_NOT_LIVE",
            "coframe descent cannot borrow EH Hamiltonian mass unless theta_MTS/Q_tau^MTS/fixed reference all descend",
            source_list("1363_bridge"),
        ),
        (
            "QOR1519_2_sector_audit",
            "quotient-basic total parent action",
            "TOTAL_NOT_PROMOTED",
            "EH is a reference anchor only; every retained MTS sector still lacks q-basic/current-chain ownership",
            source_list("1364_sector"),
        ),
        (
            "QOR1519_3_GK_hard_blocker",
            "Gamma_eff/K_hat/q_loc sector",
            "FIRST_HARD_LOCAL_FORCE_BLOCKER",
            "direct PPN/local-force observable map remains open without S_GK, K_metric, Helmholtz, double-zero, and no-flux",
            source_list("1364_acq", "1365_qbound"),
        ),
        (
            "QOR1519_4_formula_seed",
            "Gamma_eff=L_cg^-2 F(m)",
            "SOURCE_BACKED_FORMULA_SHAPE_NONCLAIM",
            "real progress for envelopes, not a claim-grade scalar density or local-GR proof",
            source_list("1366_hunt", "1366_env"),
        ),
        (
            "QOR1519_5_Kmetric_chain",
            "K_metric chain kernels",
            "SYMBOLIC_NOT_COMPUTABLE",
            "M_m/M_L/K_conn/K_domain/K_boundary/sign/units and live K_hat comparison are still missing",
            source_list("1367_kernel"),
        ),
        (
            "QOR1519_6_Mm_progress",
            "M_m fixed-field branch",
            "CONDITIONAL_RELATIVE_ZERO_ONLY",
            "delta_g m=0 is clean if m is a parent-independent scalar held fixed, but parent clauses remain unsigned",
            source_list("1368_lcg"),
        ),
        (
            "QOR1519_7_Lcg_progress",
            "L_cg fixed-parameter silence",
            "EXACT_CONDITIONAL_LEMMA_UNSIGNED",
            "delta_g L_cg=0 if L_cg is a parent-fixed scalar length parameter, but current sources do not sign that definition",
            source_list("1369_lcg"),
        ),
        (
            "QOR1519_8_qgamma_schema",
            "q_loc to PPN gamma runner",
            "SCHEMA_READY_NOT_SCORE_READY",
            "Cassini comparator exists, but q_loc_hat and C_qgamma are missing",
            source_list("1368_projection", "1369_runner"),
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "route_id": route_id,
            "route_piece": piece,
            "current_status": status,
            "meaning": meaning,
            "source_paths": sources,
            **flags(),
        }
        for route_id, piece, status, meaning, sources in rows
    ]


def mhref_schema_rows() -> list[dict[str, Any]]:
    rows = [
        ("MHR1519_0_system", "system_id", "unique local source/test body ID", "MISSING_SYSTEM_ID", "no anonymous denominator row"),
        ("MHR1519_1_coframe", "e_obs/coframe_id", "observed coframe fixed by q/Obs_e before readout", "MISSING_COFRAME_ID", "no post-readout frame choice"),
        ("MHR1519_2_tau", "tau_id", "same tau for source, charge, clocks, orbit, and boundary", "MISSING_TAU_LOCK", "no mixed time conventions"),
        ("MHR1519_3_theta", "theta_MTS", "full parent symplectic potential including EH, boundary, extra, projector, and matter/source sectors", "MISSING_THETA_MTS_SOURCE", "no EH-only import"),
        ("MHR1519_4_Qtau", "Q_tau^MTS", "total parent Hamiltonian/Noether charge form", "MISSING_Q_TAU_MTS_SOURCE", "no reference-only charge"),
        ("MHR1519_5_Htau", "H_tau", "surface Hamiltonian charge on outer linked surface in same frame/tau", "MISSING_H_TAU", "no orbital GM substitution"),
        ("MHR1519_6_Href", "H_ref", "fixed reference/counterterm chosen before source/readout fitting", "MISSING_H_REF", "no fitted counterterm"),
        ("MHR1519_7_MHref", "M_H_ref", "positive finite H_tau-H_ref with compatible units", "MISSING_M_H_REF", "no bare mass or reference-only one"),
        ("MHR1519_8_surfaces", "S1/S2/A_ext", "fixed linked surfaces and source-free annulus homology", "MISSING_SURFACE_HOMOLOGY", "no moving mask"),
        ("MHR1519_9_integrability", "delta_H_tau_curl", "integrability/fixed-reference certificate", "MISSING_INTEGRABILITY_CERTIFICATE", "no nonintegrable Hamiltonian charge"),
        ("MHR1519_10_acceptance", "promotion gate", "all fields source-backed, no MISSING markers, units compatible, anti-circularity true", "CLAIM_BLOCKED", "no local-GR/Newton scoring"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "row_id": row_id,
            "field": field,
            "required_value": required,
            "current_value": current,
            "anti_shortcut": guard,
            "source_paths": source_list("1518_mhref", "1361_mhref", "1362_denominator", "1363_hrow"),
            **flags(),
        }
        for row_id, field, required, current, guard in rows
    ]


def denominator_acquisition_rows() -> list[dict[str, Any]]:
    rows = [
        ("ACQ1519_0_q_basic_sector_table", "every retained sector has L_sector=Lbar(q)+dB_basic", "MISSING_SOURCE_EQUATION", "blocks total parent action"),
        ("ACQ1519_1_theta_Qtau_piece_table", "theta_MTS and Q_tau^MTS pieces for all sectors", "MISSING_SOURCE_EQUATION", "blocks H_tau/M_H_ref"),
        ("ACQ1519_2_tau_generator_lock", "tau_obs(q) and same tau action over all sectors", "MISSING_SOURCE_EQUATION", "blocks clock/source/orbit consistency"),
        ("ACQ1519_3_fixed_Href_reference", "fixed before-readout H_ref/counterterm policy", "MISSING_SOURCE_INPUT", "blocks denominator positivity and anti-circularity"),
        ("ACQ1519_4_Htau_surface_charge", "same-frame surface charge H_tau", "MISSING_SOURCE_INPUT", "blocks M_H_ref first row"),
        ("ACQ1519_5_GK_q_loc_source_or_zero", "q-basic S_GK or q_loc source/bound row", "MISSING_DERIVATION_OR_BOUND", "blocks local PPN/local-GR"),
        ("ACQ1519_6_PiM_worldtube_source_glue", "Pi_M/worldtube/source equality and I_commutator/R_eq rows", "MISSING_SOURCE_EQUATION", "blocks source mass denominator"),
        ("ACQ1519_7_matter_constant_descent", "masses/charges/clocks/material labels quotient-owned", "MISSING_SOURCE_EQUATION", "blocks universal coupling"),
        ("ACQ1519_8_acceptance", "all acquisition rows source-backed with no MISSING markers", "CLAIM_BLOCKED", "local branch remains private nonclaim"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "acquisition_id": acquisition_id,
            "needed_input": needed_input,
            "current_status": status,
            "blocks": blocks,
            "source_paths": source_list("1364_acq", "1518_mhref"),
            **flags(),
        }
        for acquisition_id, needed_input, status, blocks in rows
    ]


def local_blocker_rows() -> list[dict[str, Any]]:
    rows = [
        ("BLK1519_0_Newton_denominator", "M_H_ref", "MISSING", "Newton source normalization cannot use orbital GM or EH-only charge", source_list("1518_mhref", "1361_mhref")),
        ("BLK1519_1_qObs_chain", "q/Obs_e current-chain bridge", "CONDITIONAL_NOT_LIVE", "coframe descent route is exact but not current MTS evidence", source_list("1362_qobs", "1363_bridge")),
        ("BLK1519_2_total_parent_action", "quotient-basic sector ownership", "TOTAL_NOT_PROMOTED", "EH reference anchor is useful but insufficient", source_list("1364_sector")),
        ("BLK1519_3_q_loc", "Gamma/Khat q_loc residual", "RETAINED", "S_GK/K_metric/Helmholtz/double-zero/no-flux are not closed", source_list("1365_qbound")),
        ("BLK1519_4_Gamma_seed", "Gamma_eff=L_cg^-2 F(m)", "FORMULA_SHAPE_FOUND_NONCLAIM", "good seed for envelopes but units/profile/action status missing", source_list("1366_hunt")),
        ("BLK1519_5_Kmetric", "K_metric[Gamma_eff] chain kernels", "NOT_COMPUTABLE", "M_m/M_L/K_cdb and Khat comparison unresolved", source_list("1367_kernel")),
        ("BLK1519_6_Mm", "m fixed-field metric silence", "CONDITIONAL_RELATIVE_GAIN", "useful branch but parent m status unsigned", source_list("1368_lcg")),
        ("BLK1519_7_Lcg", "L_cg fixed-scale metric silence", "EXACT_CONDITIONAL_UNSIGNED", "next derivation candidate if covariance/readout contract can be signed", source_list("1369_lcg")),
        ("BLK1519_8_Cqgamma", "q_loc to PPN gamma coefficient", "MISSING_WEAK_FIELD_RESPONSE", "Cassini comparator cannot be used without C_qgamma or q_loc->q_R bridge", source_list("1368_projection", "1369_runner")),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "blocker_id": blocker_id,
            "quantity": quantity,
            "current_status": status,
            "effect": effect,
            "source_paths": sources,
            **flags(),
        }
        for blocker_id, quantity, status, effect, sources in rows
    ]


def rejection_rows() -> list[dict[str, Any]]:
    rows = [
        ("REJ1519_0_EH_only", "use EH Hamiltonian charge as total MTS H_tau", "REJECTED", "EH is a reference anchor unless all retained sectors are reduced/zeroed/bounded"),
        ("REJ1519_1_orbital_GM", "use orbital GM as M_H_ref", "REJECTED", "measured GM is what the source-transfer theorem must derive"),
        ("REJ1519_2_reference_one", "set M_H_ref=1 or bare mass by convention", "REJECTED", "denominator must be positive, same-frame, source-backed, and noncircular"),
        ("REJ1519_3_post_readout_frame", "choose coframe/tau after seeing residuals", "REJECTED", "frame and tau must be parent-owned before readout"),
        ("REJ1519_4_qR_import", "import q_R Cassini policy as q_loc PPN pass", "REJECTED", "q_loc lacks response coefficient and normalization bridge"),
        ("REJ1519_5_plateau", "set q_loc=0 by local plateau axiom", "REJECTED", "needs action/metric response/Euler double-zero/no-flux derivation"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "rejection_id": rejection_id,
            "shortcut": shortcut,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for rejection_id, shortcut, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC1519_0_fold_old_route", "Fold 1361-1369 coframe/qObs/Gamma chain into the parent sequence.", "ROUTE_CONSOLIDATED", "1519 avoids redoing old work and preserves its nonclaim gates."),
        ("DEC1519_1_frame_lock", "Do not claim one observed coframe/tau/source/charge/readout lock.", "COFRAME_TAU_LOCK_NOT_PROVED", "q/Obs_e, matter constants, tau lock, no-shadow, and M_H_ref remain unsigned."),
        ("DEC1519_2_mhref", "Keep M_H_ref as strict first-row/source-acquisition schema.", "MHREF_CLAIM_BLOCKED", "H_tau, H_ref, theta_MTS, Q_tau, surface homology, and positivity remain missing."),
        ("DEC1519_3_next", "Attack L_cg parent contract or q_loc weak-field response coefficient next.", "NEXT_1520_LCG_OR_CQGAMMA", "the sharpest remaining local-GR fork is to close M_L or make the Cassini q_loc runner scoreable."),
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


def local_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("LOCAL1519_0_Newton", "source-normalized Newtonian limit", "NOT_CLAIMED", "M_H_ref and PiM/source equality are still missing"),
        ("LOCAL1519_1_GR", "derived local GR", "NOT_CLAIMED", "qObs/current-chain, q_loc, and PPN followthrough remain open"),
        ("LOCAL1519_2_PPN", "PPN gamma/local residual", "NOT_CLAIMED", "Cassini comparator exists but C_qgamma/q_loc_hat are missing"),
        ("LOCAL1519_3_R10", "short-range/fifth-force local branch", "NOT_CLAIMED", "q_loc projection and bound rows remain source-acquisition only"),
        ("LOCAL1519_4_WEP_clock_orbital", "WEP/clock/orbital consistency", "ACTIVE_NONCLAIM", "tau/coframe/matter constants/source normalization are not parent-signed"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": status_id,
            "claim": claim,
            "current_status": status,
            "reason": reason,
            **flags(),
        }
        for status_id, claim, status, reason in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1519_0_1520",
            "next_target": "1520-Y5-parent-Lcg-contract-or-q_loc-weak-field-response-coefficient.md",
            "script": "scripts/Y5_parent_Lcg_contract_or_q_loc_weak_field_response_coefficient.py",
            "objective": "attempt to parent-sign L_cg as a fixed external/coarse-graining scale under Hilbert variation without covariance cheating; if not, derive the weak-field coefficient C_qgamma so q_loc can be projected to PPN gamma while remaining nonclaim until q_loc_hat is sourced",
            "do_not": "do not claim local GR, PPN, R10, clock, orbital, q_loc zero, or GitHub-ready result",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (COFRAME_LOCK_AUDIT, QUAR_COFRAME),
        (MHREF_SCHEMA, QUAR_MHREF),
        (LOCAL_BLOCKER_ROLLUP, QUAR_BLOCKER),
        (DECISION, QUAR_DECISION),
        (COFRAME_LOCK_AUDIT, BRANCH_COFRAME),
        (MHREF_SCHEMA, BRANCH_MHREF),
        (LOCAL_BLOCKER_ROLLUP, BRANCH_BLOCKER),
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
    coframe = read_csv(COFRAME_LOCK_AUDIT)
    qobs = read_csv(QOBS_ROUTE_AUDIT)
    mhref = read_csv(MHREF_SCHEMA)
    acq = read_csv(DENOMINATOR_ACQUISITION)
    blockers = read_csv(LOCAL_BLOCKER_ROLLUP)
    rejections = read_csv(REJECTION_LEDGER)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    checks = [
        ("VAL1519_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1519 input source paths exist"),
        ("VAL1519_1_coframe_lock_not_proved", any(row["audit_id"] == "OCF1519_7_verdict" and row["current_status"] == "COFRAME_TAU_LOCK_NOT_PROVED" for row in coframe), "observed coframe/tau lock remains unproved"),
        ("VAL1519_2_qobs_route_consolidated", any(row["route_id"] == "QOR1519_7_Lcg_progress" for row in qobs) and any(row["route_id"] == "QOR1519_8_qgamma_schema" for row in qobs), "qObs route is rolled forward through L_cg and q_loc-gamma blockers"),
        ("VAL1519_3_mhref_schema_missing", any(row["field"] == "M_H_ref" and "MISSING" in row["current_value"] for row in mhref) and any(row["field"] == "theta_MTS" and "MISSING" in row["current_value"] for row in mhref), "M_H_ref first row keeps missing theta/Q/H fields explicit"),
        ("VAL1519_4_acquisition_nonclaim", all(row["current_status"] in {"MISSING_SOURCE_EQUATION", "MISSING_SOURCE_INPUT", "MISSING_DERIVATION_OR_BOUND", "CLAIM_BLOCKED"} for row in acq), "denominator acquisition rows remain missing/blocked"),
        ("VAL1519_5_local_blockers_live", any(row["quantity"] == "L_cg fixed-scale metric silence" and "UNSIGNED" in row["current_status"] for row in blockers) and any(row["quantity"] == "q_loc to PPN gamma coefficient" and "MISSING" in row["current_status"] for row in blockers), "L_cg and C_qgamma remain live next blockers"),
        ("VAL1519_6_rejections_guardrails", len(rejections) >= 6 and all(row["status"] == "REJECTED" for row in rejections), "shortcuts and circular imports are rejected"),
        ("VAL1519_7_decision_next", any(row["result"] == "NEXT_1520_LCG_OR_CQGAMMA" for row in decisions), "decision selects L_cg contract or q_loc weak-field response"),
        ("VAL1519_8_next_target", any("1520-Y5-parent-Lcg-contract" in row["next_target"] for row in next_rows), "next target is parent L_cg contract or C_qgamma response"),
        ("VAL1519_9_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1519 CSVs parse cleanly"),
        ("VAL1519_10_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1519_11_branch_copies", all(path.exists() for path in [QUAR_COFRAME, QUAR_MHREF, QUAR_BLOCKER, QUAR_DECISION, BRANCH_COFRAME, BRANCH_MHREF, BRANCH_BLOCKER, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1519_12_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1519_13_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
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
            "check_id": "VAL1519_14_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1519 consolidates the observed-coframe/tau/MHref gate, keeps local/Newton claims blocked, and selects L_cg contract or C_qgamma as the next derivation fork"
            if overall
            else "1519 validation failed; inspect failed rows before continuing",
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
    coframe: list[dict[str, Any]],
    qobs: list[dict[str, Any]],
    mhref: list[dict[str, Any]],
    acq: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    rejections: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    local_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1519 - Parent Observed Coframe/Tau Source-Frame Lock or MHref First Row",
                "",
                "## Verdict",
                "- The observed-coframe/tau/source/charge/readout lock is not parent-signed for current MTS.",
                "- The q/Obs_e descent theorem and qObs-current-chain bridge are real conditional mathematics, but they cannot yet promote M_H_ref, Newton, PPN, R10, clock, orbital, or local-GR claims.",
                "- The older 1361-1369 chain is now folded into the parent sequence: the live derivation fork is L_cg parent silence versus q_loc -> PPN gamma response.",
                "- The next target is therefore to sign a defensible parent L_cg contract or derive the weak-field coefficient C_qgamma; both remain nonclaim until source-backed inputs exist.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "purpose"]),
                "",
                "## Coframe / Tau Lock Audit",
                md_table(coframe, ["audit_id", "claim_piece", "current_status", "why_it_matters"]),
                "",
                "## qObs Route Audit",
                md_table(qobs, ["route_id", "route_piece", "current_status", "meaning"]),
                "",
                "## MHref First Row Schema",
                md_table(mhref, ["row_id", "field", "required_value", "current_value", "anti_shortcut"]),
                "",
                "## Denominator Acquisition Ledger",
                md_table(acq, ["acquisition_id", "needed_input", "current_status", "blocks"]),
                "",
                "## Local Hard-Blocker Rollup",
                md_table(blockers, ["blocker_id", "quantity", "current_status", "effect"]),
                "",
                "## Rejection Ledger",
                md_table(rejections, ["rejection_id", "shortcut", "status", "reason"]),
                "",
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "result", "rationale"]),
                "",
                "## Local GR / Newton Status",
                md_table(local_rows, ["status_id", "claim", "current_status", "reason"]),
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
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    coframe = coframe_lock_rows()
    qobs = qobs_route_rows()
    mhref = mhref_schema_rows()
    acq = denominator_acquisition_rows()
    blockers = local_blocker_rows()
    rejections = rejection_rows()
    decisions = decision_rows()
    local_rows = local_status_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(COFRAME_LOCK_AUDIT, coframe)
    write_csv(QOBS_ROUTE_AUDIT, qobs)
    write_csv(MHREF_SCHEMA, mhref)
    write_csv(DENOMINATOR_ACQUISITION, acq)
    write_csv(LOCAL_BLOCKER_ROLLUP, blockers)
    write_csv(REJECTION_LEDGER, rejections)
    write_csv(DECISION, decisions)
    write_csv(LOCAL_STATUS, local_rows)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        COFRAME_LOCK_AUDIT,
        QOBS_ROUTE_AUDIT,
        MHREF_SCHEMA,
        DENOMINATOR_ACQUISITION,
        LOCAL_BLOCKER_ROLLUP,
        REJECTION_LEDGER,
        DECISION,
        LOCAL_STATUS,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, coframe, qobs, mhref, acq, blockers, rejections, decisions, local_rows, validation, next_rows)


if __name__ == "__main__":
    main()

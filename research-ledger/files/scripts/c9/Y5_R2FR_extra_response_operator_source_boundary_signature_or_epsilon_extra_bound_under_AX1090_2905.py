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

DOC = ROOT / "2905-Y5-R2FR-extra-response-operator-source-boundary-signature-or-epsilon-extra-bound-under-AX1090.md"

SRC_2904_DOC = ROOT / "2904-Y5-R2FR-non-EH-sector-Qv-zero-priority-gate-or-source-pack-under-AX1090.md"
SRC_2904_NEXT = RESIDUALS / "P8_Y5_R2FR_2904_NEXT_TARGET.csv"
SRC_2904_PACK = RESIDUALS / "P8_Y5_R2FR_2904_NON_EH_QV_SOURCE_PACK.csv"
SRC_2904_THEOREM = RESIDUALS / "P8_Y5_R2FR_2904_CONDITIONAL_NON_EH_SILENCE_THEOREM.csv"
SRC_2593_DOC = ROOT / "2593-Y5-R2FR-extra-response-Qv-zero-odd-source-or-extra-piece-bound.md"
SRC_2593_AUDIT = RESIDUALS / "P8_Y5_EXTRA_RESPONSE_QV_2593_ZERO_ODD_SOURCE_AUDIT.csv"
SRC_2593_BOUNDS = RESIDUALS / "P8_Y5_EXTRA_RESPONSE_QV_2593_BOUND_ROWS.csv"
SRC_2594_DOC = ROOT / "2594-Y5-R2FR-Y5-source-normalization-even-scalar-theorem-or-coefficient-fill.md"
SRC_2594_STACK = RESIDUALS / "P8_Y5_SOURCE_NORM_2594_THEOREM_STACK.csv"
SRC_2594_VECTOR = RESIDUALS / "P8_Y5_SOURCE_NORM_2594_CHANNEL_VECTOR.csv"
SRC_2595_DOC = ROOT / "2595-Y5-R2FR-GM-transfer-PiM-equality-commutator-or-source-normalization-bound.md"
SRC_2595_GATE = RESIDUALS / "P8_Y5_GM_TRANSFER_2595_TRANSFER_GATE.csv"
SRC_2595_COMPONENTS = RESIDUALS / "P8_Y5_GM_TRANSFER_2595_COMPONENT_ROWS.csv"
SRC_RESPONSE_DOUBLET = RESIDUALS / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv"
SRC_GAMMA_OWNER = ROOT / "516-Gamma-eff-scalar-density-owner-or-q_loc-bound-runner.md"
SRC_COMPONENT_MAP = ROOT / "494-exchange-doublet-component-map-or-coefficient-branch.md"
SRC_LOCAL_ACTION_BLOCKS = RESIDUALS / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv"
SRC_BOUNDARY_CONTRACT = ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2905_SOURCE_REGISTER.csv",
    "certificate": RESIDUALS / "P8_Y5_R2FR_2905_EXTRA_RESPONSE_SILENCE_CERTIFICATE.csv",
    "obstructions": RESIDUALS / "P8_Y5_R2FR_2905_EXTRA_RESPONSE_OBSTRUCTION_LEDGER.csv",
    "pack": RESIDUALS / "P8_Y5_R2FR_2905_EPSILON_EXTRA_BOUND_PACK.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2905_RUNNER_STATUS.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2905_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2905_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2905_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2905_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2905_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "certificate_copy": RAB_QUEUE / "JR2905_EXTRA_RESPONSE_SILENCE_CERTIFICATE_NONCLAIM.csv",
    "pack_copy": LOCAL_BOUNDS / "Extra_response_epsilon_bound_pack_2905_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2905_Y5_Y6_SOURCE_LOCK_OR_EXTRA_RESIDUAL_NEXT.csv",
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
        ("SRC2905_00_2904_doc", SRC_2904_DOC, "extra/response operator-source-boundary signature;NEXT2904_0_2905", "current-chain handoff selecting extra-response signature"),
        ("SRC2905_01_2904_next", SRC_2904_NEXT, "NEXT2904_0_2905;try to parent-sign the extra/response sector local silence conditions", "machine-readable 2905 target"),
        ("SRC2905_02_2904_pack", SRC_2904_PACK, "NES2904_1_extra;Delta_non_EH_Qv_total_over_Mref", "current non-EH source pack containing epsilon_Qv_extra_piece"),
        ("SRC2905_03_2904_theorem", SRC_2904_THEOREM, "THM2904_3_extra_zero;THM2904_7_current_verdict", "conditional non-EH theorem containing extra-zero clause"),
        ("SRC2905_04_2593_doc", SRC_2593_DOC, "response-doublet route remains the best-looking route;EXTRA_RESPONSE_QV_ZERO_NOT_PROVED_CURRENT_CORPUS", "prior extra-response zero attempt"),
        ("SRC2905_05_2593_audit", SRC_2593_AUDIT, "ERZ2593_1_even_density;ERZ2593_7_verdict", "zero-odd-source audit"),
        ("SRC2905_06_2593_bounds", SRC_2593_BOUNDS, "ERB2593_4_zero_odd_source;ERB2593_TOTAL", "extra-response residual component rows"),
        ("SRC2905_07_2594_doc", SRC_2594_DOC, "exchange oddness cannot kill measured `GM`;eight-channel `mu_extra` vector remains nonclaim", "Y5 source-normalization theorem stack"),
        ("SRC2905_08_2594_stack", SRC_2594_STACK, "YSN2594_3_mu_extra_zero;YSN2594_7_verdict", "machine Y5 theorem stack"),
        ("SRC2905_09_2594_vector", SRC_2594_VECTOR, "YSNC2594_4_nonEH;YSNC2594_TOTAL", "machine Y5 channel vector"),
        ("SRC2905_10_2595_doc", SRC_2595_DOC, "source-normalized Newton needs more than a conserved current;epsilon_PiM_total_abs", "GM-transfer/PiM equality obstruction"),
        ("SRC2905_11_2595_gate", SRC_2595_GATE, "GMT2595_2_commutator;GMT2595_8_total", "GM-transfer gate rows"),
        ("SRC2905_12_2595_components", SRC_2595_COMPONENTS, "GMC2595_1_I_commutator;GMC2595_TOTAL", "GM-transfer component rows"),
        ("SRC2905_13_response_contract", SRC_RESPONSE_DOUBLET, "RD516_3_positive_operator;RD516_6_boundary_no_flux", "response-doublet action contract"),
        ("SRC2905_14_gamma_owner", SRC_GAMMA_OWNER, "Gamma_eff;K_hat", "Gamma_eff and K_hat owner candidate"),
        ("SRC2905_15_component_map", SRC_COMPONENT_MAP, "Y5;Y6", "exchange-doublet component map hard blockers"),
        ("SRC2905_16_local_action_blocks", SRC_LOCAL_ACTION_BLOCKS, "A511_0_EH_core;A511_3_extra_field_silence", "minimal parent local-GR action blocks"),
        ("SRC2905_17_boundary_contract", SRC_BOUNDARY_CONTRACT, "PCS1009_7_memory_response_doublet;MISSING_FULL_DOUBLET_VARIATION", "parent sector contract for memory/response"),
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


def certificate_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "XRS2905_0_component_map",
            "full local leakage component map",
            "Every physical local leakage component Y0..Y6 is represented by exchange-odd parent variables Z^A=(R_+^A-R_-^A)/2 or explicitly excluded by a parent q-basic theorem.",
            "PARTIAL_ONLY",
            "Y2/Y3 routes exist conditionally, but Y0/Y1/Y4 and especially Y5 source normalization plus Y6 extra stress remain retained.",
            "epsilon_extra_component_map",
            SRC_COMPONENT_MAP,
        ),
        (
            "XRS2905_1_even_density",
            "even scalar density",
            "Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B+O(Z^4) with no linear Z term and with current MTS variables matched to Z.",
            "CANDIDATE_WRITTEN_NOT_CURRENT_MATCHED",
            "A formal even density kills F1 only after the current symbols and readout stack are mapped into it.",
            "epsilon_extra_even_density_match",
            SRC_GAMMA_OWNER,
        ),
        (
            "XRS2905_2_metric_response",
            "K_hat metric-response owner",
            "K_hat^{mu nu}=2/sqrt(-g) delta(sqrt(-g)Gamma_eff)/delta g_mu_nu in the same fixed volume/reference convention.",
            "NOT_PARENT_SIGNED",
            "Without Helmholtz/metric-response ownership, the extra sector can carry a stress defect even if Gamma_eff is even.",
            "epsilon_Khat_metric_response",
            SRC_GAMMA_OWNER,
        ),
        (
            "XRS2905_3_operator_domain",
            "positive self-adjoint operator",
            "M_AB and derivative pieces are positive self-adjoint on compact local collars after gauge, constraints, boundary conditions and quotient modes are removed.",
            "FORMAL_CANDIDATE_ONLY",
            "Positivity has not been upgraded to a domain/eigenvalue/constraint-quotient certificate.",
            "epsilon_extra_operator_positivity",
            SRC_RESPONSE_DOUBLET,
        ),
        (
            "XRS2905_4_zero_odd_source_Y5",
            "Y5 source-normalization silence",
            "Measured source normalization is pure even EH/Hilbert source plus zero or bounded non-EH mu_extra, with no fitted-GM absorption.",
            "HARD_BLOCK_RETAINED",
            "Y5 cannot be killed by exchange oddness; GM transfer/PiM equality and eight-channel mu_extra remain open.",
            "epsilon_extra_odd_source_Y5",
            SRC_2594_DOC,
        ),
        (
            "XRS2905_5_zero_odd_source_Y6",
            "Y6 extra-stress silence",
            "Extra stress is either exchange-odd and locally zero at Z=0, or constraint-proportional/source-bounded in the same branch.",
            "RETAINED_DEBT",
            "The corpus still allows conserved extra stress to survive the doublet symmetry.",
            "epsilon_extra_odd_source_Y6",
            SRC_COMPONENT_MAP,
        ),
        (
            "XRS2905_6_boundary_no_flux",
            "compact boundary no-flux",
            "Integrations by parts, metric-response boundary terms and reference terms carry no compact local force/mass flux on linked surfaces.",
            "OPEN",
            "Boundary silence is not the same as choosing a convenient reference after readout.",
            "epsilon_extra_boundary_flux",
            SRC_RESPONSE_DOUBLET,
        ),
        (
            "XRS2905_7_PPN_lock",
            "PPN/local residual lock",
            "Z^A equals the physical q_loc/PPN residual vector through beta, gamma, alpha_i, xi, Gdot, R10/R11 order in one observed frame.",
            "NOT_DERIVED",
            "The doublet can be a bookkeeping shadow unless it locks to measured local residuals.",
            "epsilon_extra_PPN_lock",
            SRC_2593_DOC,
        ),
        (
            "XRS2905_8_same_branch",
            "same branch and denominator",
            "All clauses above hold in the same q/e_obs/tau/M_ref branch used by 2904 non-EH silence and Y5 source normalization.",
            "MISSING_SAME_BRANCH_CERTIFICATE",
            "Sector-by-sector partial closures do not prove local GR if they use different normalizations.",
            "epsilon_extra_same_branch",
            SRC_2904_DOC,
        ),
        (
            "XRS2905_9_verdict",
            "extra-response Qv silence",
            "XRS2905_0 through XRS2905_8 pass; then epsilon_Qv_extra_piece can be theorem-zero or score-ready bounded.",
            "EXTRA_RESPONSE_QV_ZERO_NOT_PROVED_CURRENT_CORPUS",
            "The route remains alive but not promoted; the sharp next subtarget is the Y5/Y6 source lock.",
            "epsilon_Qv_extra_piece",
            SRC_2904_PACK,
        ),
    ]
    return [
        add_common(
            {
                "certificate_id": certificate_id,
                "clause": clause,
                "required_signature": required_signature,
                "current_status": current_status,
                "blocking_gap": blocking_gap,
                "residual_symbol": residual_symbol,
                "source_path": str(source_path),
                "source_path_exists": source_path.exists(),
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "same_branch_certified": False,
                "accepted_for_local_gr": False,
            }
        )
        for certificate_id, clause, required_signature, current_status, blocking_gap, residual_symbol, source_path in specs
    ]


def obstruction_rows() -> list[dict[str, Any]]:
    specs = [
        ("OBS2905_0_Y5_even_survival", "Y5 source normalization", "exchange-even measured GM and even non-EH source offsets survive Z -> -Z", "hard", "YSN2594_3_mu_extra_zero;YSN2594_5_GM_transfer", "source normalization must close before zero-odd-source can be claimed", SRC_2594_STACK),
        ("OBS2905_1_Y6_extra_stress", "Y6 extra stress", "conserved extra stress can survive as local charge hair", "hard", "ERZ2593_0_component_map;ERZ2593_4_zero_odd_source", "the response doublet needs a stress-silence theorem or bound row", SRC_2593_AUDIT),
        ("OBS2905_2_metric_response", "K_hat mismatch", "Gamma_eff evenness does not prove the observed K_hat is its metric response", "high", "ERZ2593_2_metric_response;ERB2593_2_metric_response", "stress/metric defect blocks Bianchi-safe local GR reduction", SRC_2593_BOUNDS),
        ("OBS2905_3_operator_positivity", "operator domain", "formal positivity lacks boundary/domain/constraint quotient proof", "medium", "RD516_3_positive_operator;ERZ2593_3_positive_operator", "double-zero minimum is not a theorem until the operator is controlled", SRC_RESPONSE_DOUBLET),
        ("OBS2905_4_boundary_flux", "boundary no-flux", "compact force/mass flux can re-enter through integration by parts or reference terms", "medium", "RD516_6_boundary_no_flux;ERB2593_6_boundary_flux", "local charge can hide in exact/reference bookkeeping", SRC_RESPONSE_DOUBLET),
        ("OBS2905_5_PPN_lock", "PPN lock", "Z variables are not yet proven to be measured q_loc/PPN residuals", "high", "ERZ2593_5_PPN_lock;NES2904_1_extra", "a silent bookkeeping variable does not imply silent physics", SRC_2593_AUDIT),
        ("OBS2905_6_same_branch", "same-branch compatibility", "extra-sector, Y5 source normalization and non-EH silence gates are not signed in one branch", "high", "THM2904_7_current_verdict;YSN2594_7_verdict", "local-GR reduction cannot mix unrelated normalizations", SRC_2904_THEOREM),
    ]
    return [
        add_common(
            {
                "obstruction_id": obstruction_id,
                "obstruction": obstruction,
                "mechanism": mechanism,
                "severity": severity,
                "source_anchor": source_anchor,
                "consequence": consequence,
                "source_path": str(source_path),
                "source_path_exists": source_path.exists(),
                "resolved": False,
            }
        )
        for obstruction_id, obstruction, mechanism, severity, source_anchor, consequence, source_path in specs
    ]


def bound_pack_rows() -> list[dict[str, Any]]:
    specs = [
        ("XRB2905_0_component_map", "epsilon_extra_component_map", "unmapped or unproved Y0-Y6 exchange-doublet components contributing to Q_v^extra", "dimensionless component-map defect", "Y0_Y1_Y4_UNRESOLVED;Y5_HARD_BLOCK;Y6_RETAINED_DEBT", SRC_COMPONENT_MAP, "PPN;R11;Newton;local_GR"),
        ("XRB2905_1_even_density", "epsilon_extra_even_density_match", "failure of current Gamma_eff to match an even quadratic scalar density with no linear Z term", "dimensionless density-matching defect", "CANDIDATE_WRITTEN_NOT_MATCHED_TO_CURRENT_MTS", SRC_GAMMA_OWNER, "q_loc;local_GR;PPN"),
        ("XRB2905_2_metric_response", "epsilon_Khat_metric_response", "norm(K_hat - metric_response(sqrt(-g) Gamma_eff)) in local branch", "stress/metric-response defect", "MISSING_KHAT_METRIC_RESPONSE_MATCH", SRC_GAMMA_OWNER, "Bianchi;conservation;local_GR"),
        ("XRB2905_3_operator", "epsilon_extra_operator_positivity", "negative/zero/unowned modes of M_AB or derivative operator after gauge/constraint quotient", "operator gap defect", "MISSING_OPERATOR_DOMAIN;MISSING_CONSTRAINT_QUOTIENT;MISSING_BOUNDARY_CONDITIONS", SRC_RESPONSE_DOUBLET, "stability;local_silence"),
        ("XRB2905_4_Y5_source", "epsilon_extra_odd_source_Y5", "odd-source leakage sourced by Y5 measured-GM/source-normalization channel", "dimensionless source-normalization leakage", "MISSING_Y5_GM_TRANSFER;MISSING_MU_EXTRA_ZERO;MISSING_NO_GM_ABSORPTION", SRC_2594_VECTOR, "Newton;source_mass;PPN;R11"),
        ("XRB2905_5_Y6_stress", "epsilon_extra_odd_source_Y6", "odd/even extra-stress leakage not removed by current exchange doublet", "dimensionless extra-stress leakage", "MISSING_Y6_EXTRA_STRESS_ZERO_OR_BOUND", SRC_COMPONENT_MAP, "PPN;local_GR;Bianchi"),
        ("XRB2905_6_boundary", "epsilon_extra_boundary_flux", "compact local boundary force/mass flux from extra-response integrations by parts or metric response", "dimensionless boundary-flux leakage", "MISSING_BOUNDARY_NO_FLUX_THEOREM", SRC_RESPONSE_DOUBLET, "clock;orbital;PPN"),
        ("XRB2905_7_PPN_lock", "epsilon_extra_PPN_lock", "failure of Z^A to equal physical q_loc/PPN residual vector through beta,gamma,alpha_i,xi,Gdot,R10/R11", "dimensionless PPN-lock defect", "MISSING_Z_TO_YLOC_LOCK;MISSING_Y5_Y6_THEOREMS", SRC_2593_BOUNDS, "PPN;R10;R11;local_GR"),
        ("XRB2905_8_branch", "epsilon_extra_same_branch", "branch mismatch between extra-response, source-normalization and non-EH silence certificates", "boolean branch-compatibility guard", "MISSING_SAME_BRANCH_COMPATIBILITY_PROOF", SRC_2904_DOC, "q_owner;same_frame;local_GR"),
        ("XRB2905_TOTAL", "epsilon_Qv_extra_piece", "absolute no-cancellation envelope over extra-response component residuals", "dimensionless after M_ref", "COMPONENTS_MISSING", SRC_2904_PACK, "PPN;R10;clock;cosmology_branching;local_GR"),
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


def runner_rows() -> list[dict[str, Any]]:
    specs = [
        ("RUN2905_0_signature_claim", "REFUSED_UNSIGNED_EXTRA_RESPONSE_CERTIFICATE", "component map; even density; Khat response; positive operator; Y5 source; Y6 stress; boundary no-flux; PPN lock; same branch", 0, "certificate clauses remain unsigned"),
        ("RUN2905_1_epsilon_pack", "STAGED_NONCLAIM_BOUND_PACK", "epsilon_extra_component_map;epsilon_extra_even_density_match;epsilon_Khat_metric_response;epsilon_extra_operator_positivity;epsilon_extra_odd_source_Y5;epsilon_extra_odd_source_Y6;epsilon_extra_boundary_flux;epsilon_extra_PPN_lock;epsilon_extra_same_branch", 0, "rows are source-backed but unfilled and nonclaim"),
        ("RUN2905_2_Y5_Y6_focus", "NEXT_TARGET_SELECTED", "Y5 source-normalization and Y6 extra-stress lock", 0, "these are the hard blockers preventing zero odd source"),
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


def claim_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2905_0_certificate_shape", "extra-response silence certificate is explicit", "PASS_NONCLAIM_STRUCTURE_ONLY", "all operator/source/boundary/PPN/same-branch clauses are separated", True),
        ("CG2905_1_extra_zero", "epsilon_Qv_extra_piece is theorem-zero", "BLOCKED_NONCLAIM", "Y5/Y6, metric response, operator domain, boundary no-flux and PPN lock are unsigned", False),
        ("CG2905_2_doublet_shortcut", "exchange doublet symmetry alone kills local source", "REJECTED_SHORTCUT", "Y5 measured GM and even non-EH offsets survive exchange oddness", False),
        ("CG2905_3_operator_positive", "formal positive operator proves local silence", "BLOCKED_NONCLAIM", "operator domain, quotient and boundary conditions are not parent-certified", False),
        ("CG2905_4_bound_route", "epsilon_Qv_extra_piece is score-ready bounded", "BLOCKED_NONCLAIM", "no numeric component values, M_ref, arena projections or same-branch lock", False),
        ("CG2905_5_local_GR_Newton", "local GR/Newton follows after 2905", "BLOCKED_NONCLAIM", "2905 sharpens the extra-sector residual; it does not close it", False),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "claim": claim,
                "gate_status": gate_status,
                "reason": reason,
                "gate_pass": gate_pass,
                "accepted_for_local_gr": False,
            }
        )
        for gate_id, claim, gate_status, reason, gate_pass in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2905_0_certificate_retained", "EXTRA_RESPONSE_SILENCE_CERTIFICATE_RETAINED", "the response doublet remains the best conditional route, but now has a full operator-source-boundary checklist", "future proof attempts must close these clauses in one branch"),
        ("DEC2905_1_no_zero_claim", "EXTRA_RESPONSE_QV_ZERO_NOT_CLAIMED", "Y5 source normalization, Y6 stress, Khat response, operator positivity, PPN lock and boundary no-flux remain unsigned", "epsilon_Qv_extra_piece remains active nonclaim residual"),
        ("DEC2905_2_next", "Y5_Y6_SOURCE_LOCK_SELECTED_NEXT", "zero odd source is the hard blocker; Y5 measured-GM/source normalization and Y6 extra stress are the two named routes by which local charge survives", "2906 should attack Y5/Y6 source lock or split epsilon_extra_odd_source into source-ready component rows"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "reason": reason,
                "effect": effect,
            }
        )
        for decision_id, decision, reason, effect in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "route_id": "NEXT2905_0_2906",
                "selection_status": "selected_primary",
                "target_file": "2906-Y5-R2FR-Y5-Y6-zero-odd-source-lock-or-epsilon-extra-source-split-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_Y5_Y6_zero_odd_source_lock_or_epsilon_extra_source_split_under_AX1090_2906.py",
                "task": "try to prove Y5 source-normalization and Y6 extra-stress do not source the exchange-odd extra-response mode in the same local branch; otherwise split epsilon_extra_odd_source into source-ready Y5 and Y6 bound rows",
                "success_condition": "epsilon_extra_odd_source_Y5=0 and epsilon_extra_odd_source_Y6=0 by parent signature in the same branch",
                "fallback_condition": "source-pack Y5/Y6 source coefficients with units, M_ref dependency, observable links, and valid_for_claim=false",
                "guardrails": "no exchange-odd shortcut; no fitted GM absorption; no orbital GM denominator; no local-GR/Newton claim; no GitHub; no formalization-workbench edits",
                "selected": True,
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    specs = [
        ("BR2905_0_certificate_copy", OUTPUTS["certificate"], BRANCH_OUTPUTS["certificate_copy"], "RAB queue copy of extra-response silence certificate"),
        ("BR2905_1_pack_copy", OUTPUTS["pack"], BRANCH_OUTPUTS["pack_copy"], "local-bounds copy of epsilon_extra bound pack"),
        ("BR2905_2_next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"], "RAB queue copy of 2906 Y5/Y6 source-lock target"),
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
    certificate_rows_data = all_rows["certificate"]
    obstruction_rows_data = all_rows["obstructions"]
    pack_rows_data = all_rows["pack"]
    runner_rows_data = all_rows["runner"]
    claim_rows_data = all_rows["claims"]
    next_rows_data = all_rows["next"]
    branch_rows_data = all_rows["branches"]
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    required_symbols = {
        "epsilon_extra_component_map",
        "epsilon_extra_even_density_match",
        "epsilon_Khat_metric_response",
        "epsilon_extra_operator_positivity",
        "epsilon_extra_odd_source_Y5",
        "epsilon_extra_odd_source_Y6",
        "epsilon_extra_boundary_flux",
        "epsilon_extra_PPN_lock",
        "epsilon_extra_same_branch",
        "epsilon_Qv_extra_piece",
    }
    found_symbols = {row["symbol"] for row in pack_rows_data}
    checks = [
        ("VAL2905_0_sources_exist", all(row["path_exists"] for row in source_rows), "all registered source paths exist"),
        ("VAL2905_1_source_anchors", all(row["anchors_found"] for row in source_rows), "all registered source anchors were found"),
        ("VAL2905_2_certificate_complete", len(certificate_rows_data) == 10 and any(row["certificate_id"] == "XRS2905_9_verdict" for row in certificate_rows_data), "extra-response silence certificate has all clauses"),
        ("VAL2905_3_certificate_nonclaim", all(not row["theorem_zero_adopted"] and not row["accepted_for_local_gr"] for row in certificate_rows_data), "certificate rows remain unsigned nonclaim"),
        ("VAL2905_4_obstructions_present", len(obstruction_rows_data) == 7 and all(not row["resolved"] for row in obstruction_rows_data), "obstruction ledger records unresolved blockers"),
        ("VAL2905_5_pack_symbols_present", required_symbols <= found_symbols, "epsilon_extra bound pack symbols are present"),
        ("VAL2905_6_pack_paths_exist", all(row["source_path_exists"] for row in pack_rows_data), "bound pack rows point to existing local sources"),
        ("VAL2905_7_rows_nonclaim", all(not row["valid_for_claim"] and not row["accepted_for_scoring"] for row in pack_rows_data), "epsilon_extra rows remain non-score-ready and nonclaim"),
        ("VAL2905_8_runner_refuses", any(row["runner_id"] == "RUN2905_0_signature_claim" and row["status"] == "REFUSED_UNSIGNED_EXTRA_RESPONSE_CERTIFICATE" for row in runner_rows_data), "runner refuses unsigned extra-response zero claim"),
        ("VAL2905_9_claim_gates_safe", all(not row["claim_allowed"] for row in claim_rows_data) and any(row["gate_id"] == "CG2905_5_local_GR_Newton" and row["gate_status"] == "BLOCKED_NONCLAIM" for row in claim_rows_data), "local-GR/Newton claims remain blocked"),
        ("VAL2905_10_next_target_2906", any(row["route_id"] == "NEXT2905_0_2906" and row["selected"] for row in next_rows_data), "2906 Y5/Y6 source lock target selected"),
        ("VAL2905_11_branch_copies_exist", all(row["exists"] for row in branch_rows_data), "branch copies were written"),
        ("VAL2905_12_csv_outputs_parse", all(csv_parses(path) for path in csv_outputs), "all generated CSV outputs parse cleanly"),
        ("VAL2905_13_formalization_untouched_during_run", not formalization_touched(), "formalization-workbench was not touched during this run"),
    ]
    overall = all(passed for _, passed, _ in checks)
    checks.append(("VAL2905_OVERALL", overall, "2905 validation overall"))
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
        "# 2905 - Y5 R2FR Extra-Response Operator Source Boundary Signature or Epsilon Extra Bound Under AX1090",
        "",
        f"Run: `runs/{SCRIPT_START_UTC.strftime('%Y%m%d-%H%M%S')}-Y5-R2FR-extra-response-operator-source-boundary-signature-or-epsilon-extra-bound-under-AX1090`",
        "Status: `Y5_R2FR_2905_extra_response_silence_certificate_built_Y5_Y6_hard_block_retained_2906_next`",
        "Claim ceiling: `extra_response_certificate_nonclaim_only_no_epsilon_Qv_extra_zero_no_source_normalized_Newton_no_PPN_no_R10_no_local_GR_no_GitHub_claim`",
        "",
        "## Summary",
        "",
        "2905 builds the full extra/response silence certificate in the current 2900-chain. It does not prove the extra sector is locally silent; it proves what must be signed before that statement is allowed.",
        "",
        "The response-doublet route is still alive: an even quadratic `Gamma_eff` can kill the linear `F_1` term if the current MTS variables really sit inside the doublet, the operator is positive, the source is odd-zero, the boundary is silent, and the same branch locks to PPN/local observables.",
        "",
        "The hard obstruction is now split cleanly: Y5 source normalization and Y6 extra stress are the source channels that can survive the doublet and leak local charge. So the next fair fight is not broad GR rhetoric; it is the Y5/Y6 zero-odd-source lock.",
        "",
        "## Source Register",
        "",
        md_table(all_rows["sources"], ["source_id", "source_path", "path_exists", "anchors_found", "role", "missing_anchors"]),
        "",
        "## Extra-Response Silence Certificate",
        "",
        md_table(all_rows["certificate"], ["certificate_id", "clause", "current_status", "required_signature", "blocking_gap", "residual_symbol", "valid_for_claim"]),
        "",
        "## Obstruction Ledger",
        "",
        md_table(all_rows["obstructions"], ["obstruction_id", "obstruction", "severity", "mechanism", "consequence", "valid_for_claim"]),
        "",
        "## Epsilon Extra Bound Pack",
        "",
        md_table(all_rows["pack"], ["row_id", "symbol", "definition", "units", "current_value", "source_path", "observable_link", "valid_for_claim"]),
        "",
        "## Runner Status",
        "",
        md_table(all_rows["runner"], ["runner_id", "status", "required_components", "components_evaluable", "reason", "runner_ready", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        md_table(all_rows["claims"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        md_table(all_rows["decision"], ["decision_id", "decision", "reason", "effect", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(all_rows["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "success_condition", "fallback_condition", "valid_for_claim"]),
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
        "This is progress of the engineering kind: the load path is visible. The extra/response sector can still be the elegant local-silence mechanism, but only if the Y5/Y6 source channels stop injecting charge into it.",
        "",
        "If 2906 closes Y5/Y6, the response-doublet route gets genuinely healthier. If it fails, `epsilon_Qv_extra_piece` becomes a real local residual that has to face PPN/R10/clock/orbital bounds.",
        "",
        "## Forbidden Claims From 2905",
        "",
        "- The extra/response sector is locally silent.",
        "- `epsilon_Qv_extra_piece=0` in current MTS.",
        "- Exchange-doublet symmetry alone kills measured source normalization.",
        "- Formal operator positivity proves a local-GR branch.",
        "- Source-normalized Newton, PPN, R10, clock, orbital or local GR is proved.",
    ]
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    all_rows: dict[str, list[dict[str, Any]]] = {}
    all_rows["sources"] = source_register_rows()
    all_rows["certificate"] = certificate_rows()
    all_rows["obstructions"] = obstruction_rows()
    all_rows["pack"] = bound_pack_rows()
    all_rows["runner"] = runner_rows()
    all_rows["claims"] = claim_gate_rows()
    all_rows["decision"] = decision_rows()
    all_rows["next"] = next_rows()

    for key in ["sources", "certificate", "obstructions", "pack", "runner", "claims", "decision", "next"]:
        write_csv(OUTPUTS[key], all_rows[key])

    all_rows["branches"] = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], all_rows["branches"])

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_doc(all_rows)

    overall = next(row["passed"] for row in all_rows["validation"] if row["check_id"] == "VAL2905_OVERALL")
    print(f"2905 validation overall: {overall}")
    print(DOC)


if __name__ == "__main__":
    main()

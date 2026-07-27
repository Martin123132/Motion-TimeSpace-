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
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2973"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2973-Y5-R2FR-Z-basis-physical-lock-map-and-NZ-normalization-or-q_loc-first-component-under-AX1090.md"

SRC_2972_DOC = ROOT / "2972-Y5-R2FR-DqZ-component-matrix-and-Z-basis-normalization-or-first-epsq-subrow-under-AX1090.md"
SRC_2972_NEXT = RESIDUALS / "P8_Y5_R2FR_2972_NEXT_TARGET.csv"
SRC_2972_BASIS = RESIDUALS / "P8_Y5_R2FR_2972_Z_BASIS_NORMALIZATION_AUDIT.csv"
SRC_2972_EPSQ = RESIDUALS / "P8_Y5_R2FR_2972_FIRST_EPSQ_SUBROWS_NONCLAIM.csv"
SRC_2972_ENVELOPE = RESIDUALS / "P8_Y5_R2FR_2972_DQZ_NO_CANCELLATION_ENVELOPE.csv"
SRC_2972_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2972_VALIDATION.csv"

SRC_1672_ZLOCK = RESIDUALS / "P8_Y5_PARENT_QLOC_1672_Z_TO_RPHYS_LOCK_MAP_ATTEMPT.csv"
SRC_1672_RANK = RESIDUALS / "P8_Y5_PARENT_QLOC_1672_FULL_RANK_COERCIVITY_GATE.csv"
SRC_1672_NULLSPACE = RESIDUALS / "P8_Y5_PARENT_QLOC_1672_PHYSICAL_NULLSPACE_LEDGER.csv"
SRC_1674_ZBASIS = RESIDUALS / "P8_Y5_PARENT_QLOC_1674_Z_BASIS_CANDIDATE.csv"
SRC_1674_MATRIX = RESIDUALS / "P8_Y5_PARENT_QLOC_1674_DQZ_COMPONENT_DERIVATIVE_MATRIX.csv"
SRC_2911_KERNEL = RESIDUALS / "P8_Y5_R2FR_2911_KERNEL_BASIS_ATTEMPT.csv"
SRC_2911_QMAP = RESIDUALS / "P8_Y5_R2FR_2911_Q_MAP_DERIVATIVE_AUDIT.csv"
SRC_2956_DESCENT = RESIDUALS / "P8_Y5_R2FR_2956_MATTER_PULLBACK_DESCENT_AUDIT.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2973_SOURCE_REGISTER.csv",
    "physical_lock": RESIDUALS / "P8_Y5_R2FR_2973_Z_BASIS_PHYSICAL_LOCK_ATTEMPT.csv",
    "nz_contract": RESIDUALS / "P8_Y5_R2FR_2973_NZ_NORMALIZATION_CONTRACT.csv",
    "rank_audit": RESIDUALS / "P8_Y5_R2FR_2973_FULL_RANK_COERCIVITY_AUDIT.csv",
    "qloc_row": RESIDUALS / "P8_Y5_R2FR_2973_QLOC_FIRST_COMPONENT_ROW_NONCLAIM.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2973_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2973_DERIVATION_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2973_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2973_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2973_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "physical_lock_copy": PARENT_ACTION / "Z_basis_physical_lock_2973_NOT_DERIVED.csv",
    "qloc_copy": LOCAL_BOUNDS / "q_loc_first_component_row_2973_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2973_q_loc_component_source_owner_next_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv_rows(path)
        return True
    except Exception:
        return False


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": RUN_UTC,
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


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    if columns is None:
        columns = list(rows[0].keys())
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2973_00_2972_doc", SRC_2972_DOC, "NEXT2972_0_2973;Dq_Z_norm", "2972 checkpoint selected this Z-basis/N_Z target"),
        ("SRC2973_01_2972_next", SRC_2972_NEXT, "NEXT2972_0_2973", "machine next-target row"),
        ("SRC2973_02_2972_basis", SRC_2972_BASIS, "BAS2972_0_q_loc;BAS2972_7_N_Z", "2972 basis and normalization audit"),
        ("SRC2973_03_2972_epsq", SRC_2972_EPSQ, "EPSQ2972_03_eps_Z_basis;EPSQ2972_04_eps_N_Z", "2972 eps subrows to refine"),
        ("SRC2973_04_2972_envelope", SRC_2972_ENVELOPE, "ENV2972_0_DqZ_norm;ENV2972_3_no_cancellation", "2972 no-cancellation envelope"),
        ("SRC2973_05_2972_validation", SRC_2972_VALIDATION, "VAL2972_OVERALL", "2972 validation"),
        ("SRC2973_06_1672_zlock", SRC_1672_ZLOCK, "LOCK1672_0_q_loc;LOCK1672_6_verdict", "physical residual lock map attempt"),
        ("SRC2973_07_1672_rank", SRC_1672_RANK, "RG1672_0_define_L;RG1672_5_verdict", "full-rank and coercivity gate"),
        ("SRC2973_08_1672_nullspace", SRC_1672_NULLSPACE, "NS1672_0_q_loc_only;NS1672_5_readout_coupling", "physical nullspace risks"),
        ("SRC2973_09_1674_zbasis", SRC_1674_ZBASIS, "ZB1674_0_q;ZB1674_5_coupling", "candidate Z basis rows"),
        ("SRC2973_10_1674_matrix", SRC_1674_MATRIX, "DQM1674_0_coframe_metric;DQM1674_5_operator_norm", "DqZ component derivative matrix"),
        ("SRC2973_11_2911_kernel", SRC_2911_KERNEL, "KB2911_0_Zq;KB2911_8_verdict", "kernel-basis attempt"),
        ("SRC2973_12_2911_qmap", SRC_2911_QMAP, "QMAP2911_5_Dq_residual_lock;QMAP2911_7_verdict", "q-map derivative audit"),
        ("SRC2973_13_2956_descent", SRC_2956_DESCENT, "DESC2956_1_parent_q;DESC2956_7_verdict", "matter/readout descent audit"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, anchors, role in specs:
        anchors_ok, missing = anchors_present(path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(path),
                    "exists": path.exists(),
                    "anchors_required": anchors,
                    "anchors_found": anchors_ok,
                    "missing_anchors": missing,
                    "role": role,
                }
            )
        )
    return rows


def physical_lock_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "LOCK2973_0_q_loc",
            "Z_q",
            "q_loc vector residual direction",
            "Z_q^nu := q_loc^nu/q_*",
            "q_loc^nu = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})",
            "CONDITIONAL_COMPONENT_ONLY",
            "Gamma_eff, K_hat, P_loc, local norm q_* and boundary silence are not parent-owned",
            SRC_1672_ZLOCK,
        ),
        (
            "LOCK2973_1_Y5",
            "Z_mu",
            "measured-GM/source normalization residual",
            "Z_mu := Delta(GM)_measured/(GM)_GR",
            "epsilon_mu source/current normalization residual",
            "NOT_LOCKED",
            "source-current zero and Gauss/orbital calibration are not derived",
            SRC_1674_ZBASIS,
        ),
        (
            "LOCK2973_2_Y6",
            "Z_T",
            "extra local stress/exterior metric residual",
            "Z_T := DeltaT_extra/T_*",
            "extra conserved stress and weak-field metric response",
            "NOT_LOCKED",
            "conserved exchange-even stress can survive q_loc=0",
            SRC_1672_NULLSPACE,
        ),
        (
            "LOCK2973_3_PPN",
            "Z_PPN",
            "PPN residual vector",
            "Z_PPN := DeltaPPN_A",
            "{gamma-1,beta-1,alpha_i,xi,zeta_i,Gdot,R11}",
            "NOT_LOCKED",
            "response operator and gauge/frame certificate missing",
            SRC_1672_RANK,
        ),
        (
            "LOCK2973_4_boundary",
            "Z_H",
            "boundary/harmonic/source-measure residual",
            "Z_H := q_H/H_* or boundary flux amplitude",
            "Hodge/projector/local-collar flux residual",
            "NOT_LOCKED",
            "boundary projector and no-flux theorem not closed",
            SRC_1672_NULLSPACE,
        ),
        (
            "LOCK2973_5_coupling",
            "Z_c",
            "matter/source/readout coupling residual",
            "Z_c := DeltaCoupling_A",
            "species/frame/source/photon/clock/orbit pullback residuals",
            "NOT_LOCKED",
            "quotient-invariant matter/readout descent is still unsigned",
            SRC_2956_DESCENT,
        ),
        (
            "LOCK2973_6_full_vector",
            "Z^A",
            "full physical residual vector",
            "Z^A = N^A_I R_phys^I + O(R_phys^2)",
            "R_phys={q_loc,Y5,Y6,DeltaPPN,q_H,DeltaCoupling}",
            "FULL_LOCK_NOT_PROVED",
            "full-rank/coercive physical residual map is missing",
            SRC_1672_RANK,
        ),
    ]
    return [
        add_common(
            {
                "lock2973_id": lock_id,
                "basis_symbol": symbol,
                "physical_channel": channel,
                "candidate_component": component,
                "residual_definition": residual,
                "status": status,
                "blocking_gap": gap,
                "source_path": str(source),
                "parent_signed": False,
                "component_live": lock_id == "LOCK2973_0_q_loc",
                "full_rank_component": False,
                "accepted_for_scoring": False,
            }
        )
        for lock_id, symbol, channel, component, residual, status, gap, source in rows
    ]


def nz_contract_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "NZ2973_0_norm_space",
            "local residual norm space",
            "Choose a compact collar U, observed coframe, measure dmu_g, and positive channel metric W_IJ.",
            "MISSING_OBSERVED_COFRAME_MEASURE_AND_CHANNEL_METRIC",
            "not_source_backed",
        ),
        (
            "NZ2973_1_qloc_scale",
            "q_* scale for q_loc",
            "q_* must carry units of q_loc so Z_q=q_loc/q_* is dimensionless.",
            "MISSING_QLOC_UNIT_SCALE",
            "not_source_backed",
        ),
        (
            "NZ2973_2_candidate_NZq",
            "q_loc first-component normalization",
            "N_Zq^2 := integral_U W_munu (q_loc^mu/q_*) (q_loc^nu/q_*) dmu_g.",
            "MISSING_W_MUNU_AND_QSTAR",
            "candidate_contract_only",
        ),
        (
            "NZ2973_3_full_NZ",
            "full residual-vector normalization",
            "N_Z^2 := integral_U R_phys^I W_IJ R_phys^J dmu_g.",
            "MISSING_FULL_CHANNEL_METRIC_AND_RESPONSE_RANK",
            "candidate_contract_only",
        ),
        (
            "NZ2973_4_coercive_bounds",
            "coercivity constants",
            "Need 0<c_-<=c_+<infty with c_-||R_phys||^2 <= <Z,MZ> <= c_+||R_phys||^2.",
            "MISSING_C_MINUS_C_PLUS",
            "not_proved",
        ),
        (
            "NZ2973_5_units",
            "units and dimensionless score",
            "Every channel requires a declared scale q_*,T_*,H_* or readout normalization before scoring.",
            "MISSING_CHANNEL_UNIT_SCALES",
            "not_claimable",
        ),
    ]
    return [
        add_common(
            {
                "nz_contract_id": nz_id,
                "object": obj,
                "candidate_definition": definition,
                "blocking_gap": gap,
                "status": status,
                "finite_numeric_value": False,
                "theorem_zero": False,
                "source_path": str(SRC_1672_RANK if "coercive" in nz_id else SRC_2972_BASIS),
            }
        )
        for nz_id, obj, definition, gap, status in rows
    ]


def rank_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("RG2973_0_response_operator", "L^I_A = partial R_phys^I / partial Z^A", "MISSING_SOURCE_BACKED_RESPONSE_OPERATOR", "cannot prove Z controls observed channels"),
        ("RG2973_1_rank", "rank(L)=dim(R_phys) after gauge quotient", "NOT_SATISFIED", "q_loc first component alone leaves Y5/Y6/PPN/boundary/coupling nullspaces"),
        ("RG2973_2_kernel", "ker(L) only gauge/quotient directions", "OPEN_KERNEL_RISK", "physical nullspace rows remain active"),
        ("RG2973_3_coercivity", "c_-||R_phys||^2 <= <Z,MZ>", "MISSING_COERCIVE_PHYSICAL_LOCK", "positive auxiliary norm not shown to control measured residuals"),
        ("RG2973_4_q_loc_implication", "q_loc=0 => local-GR/Newton residuals vanish", "FALSE_ON_CURRENT_EVIDENCE", "q_loc-only zero does not kill source, stress, boundary or readout residuals"),
        ("RG2973_5_verdict", "physical-lock theorem", "NOT_PROVED_SELECT_QLOC_FIRST_COMPONENT", "do not claim local GR; source q_loc component first"),
    ]
    return [
        add_common(
            {
                "rank_audit_id": audit_id,
                "criterion": criterion,
                "current_status": status,
                "failure_mode": failure,
                "source_path": str(SRC_1672_RANK),
                "passed": False,
            }
        )
        for audit_id, criterion, status, failure in rows
    ]


def qloc_component_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "QLOC2973_0_definition",
            "q_loc^nu",
            "P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})",
            "vector residual",
            "definition carried from 1672/2972; owner of Gamma_eff/K_hat/P_loc still needed",
            "MISSING_PARENT_OWNER",
        ),
        (
            "QLOC2973_1_candidate_zero_lemma",
            "q_loc^nu -> 0",
            "If local vacuum EL gives nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu}=0 and P_loc is q-basic, then q_loc^nu=0.",
            "conditional theorem",
            "requires parent action identity, q-basic projector and boundary silence",
            "CONDITIONAL_NOT_ADOPTED",
        ),
        (
            "QLOC2973_2_scale",
            "q_*",
            "declared local scale making Z_q=q_loc/q_* dimensionless",
            "same units as q_loc",
            "needed before any finite N_Zq or scoring",
            "MISSING_QSTAR",
        ),
        (
            "QLOC2973_3_norm",
            "N_Zq",
            "(integral_U W_munu Z_q^mu Z_q^nu dmu_g)^(1/2)",
            "dimensionless if q_* and W are declared",
            "candidate normalization only",
            "MISSING_W_AND_MEASURE",
        ),
        (
            "QLOC2973_4_boundary",
            "P_loc boundary/projector silence",
            "P_loc commutes with local derivative on compact collar and no harmonic/projector flux survives.",
            "theorem condition",
            "needed to stop q_loc from re-entering through boundary terms",
            "MISSING_BOUNDARY_SILENCE",
        ),
        (
            "QLOC2973_5_readout_link",
            "q_loc -> PPN/readouts",
            "Need source-backed response operator from q_loc component to weak-field/clock/orbit/EM readouts.",
            "operator row",
            "without this q_loc can be a clean component but not full local-GR proof",
            "MISSING_RESPONSE_OPERATOR",
        ),
        (
            "QLOC2973_6_bound_row",
            "eps_q_loc_component",
            "|Z_q| <= eps_q_loc_component",
            "dimensionless bound",
            "placeholder row until definition, scale, norm and boundary conditions are source-backed",
            "MISSING_SOURCE_BACKED_UPPER_BOUND",
        ),
    ]
    return [
        add_common(
            {
                "qloc_row_id": row_id,
                "symbol": symbol,
                "candidate_expression": expression,
                "units": units,
                "interpretation": interpretation,
                "status": status,
                "source_path": str(SRC_1672_ZLOCK if row_id == "QLOC2973_0_definition" else SRC_2911_QMAP),
                "finite_value_present": False,
                "theorem_zero": False,
                "accepted_for_scoring": False,
            }
        )
        for row_id, symbol, expression, units, interpretation, status in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2973_0_Zbasis", "full physical Z basis parent-signed", False, "FULL_Z_BASIS_NOT_PARENT_SIGNED"),
        ("CG2973_1_NZ", "N_Z finite and dimensionless", False, "NZ_NORMALIZATION_MISSING"),
        ("CG2973_2_full_rank", "full-rank/coercive physical lock", False, "FULL_RANK_COERCIVITY_NOT_PROVED"),
        ("CG2973_3_q_loc_zero", "q_loc zero theorem adopted", False, "QLOC_ZERO_CONDITIONAL_ONLY"),
        ("CG2973_4_local_GR", "local GR/Newton reduction", False, "LOCAL_GR_NOT_DERIVED"),
        ("CG2973_5_claims", "R10/PPN/clock/orbital/WEP claims", False, "NO_LOCAL_CLAIM_ALLOWED"),
    ]
    return [
        add_common(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "condition_passed": passed,
                "status": status,
            }
        )
        for gate_id, claim, passed, status in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC2973_0_full_lock",
            "full Z-basis lock rejected for now",
            "1672/1674/2911 agree that the candidate physical channels are not a live parent basis and not full-rank/coercive",
            "do not promote Z^A=N^A_I R_phys^I",
        ),
        (
            "DEC2973_1_qloc",
            "q_loc selected as first component",
            "it has the clearest residual formula and the closest path to a local vacuum identity",
            "source Gamma_eff, K_hat, P_loc, q_* and boundary silence",
        ),
        (
            "DEC2973_2_derivation",
            "conditional q_loc zero lemma written",
            "if the parent EL identity and q-basic projection hold then q_loc vanishes",
            "prove or bound the lemma in 2974",
        ),
        (
            "DEC2973_3_claims",
            "all claims blocked",
            "q_loc alone does not kill source/current, stress, PPN, boundary or readout nullspaces",
            "keep local-GR/Newton/R10/PPN/clock/orbital claims off",
        ),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "reason": reason,
                "next_action": next_action,
            }
        )
        for decision_id, decision, reason, next_action in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2973_0_2974",
                "priority": "selected_primary",
                "next_doc": "2974-Y5-R2FR-q_loc-component-owner-and-local-vacuum-identity-or-bound-row-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_q_loc_component_owner_and_local_vacuum_identity_or_bound_row_under_AX1090_2974.py",
                "objective": "Try to derive the q_loc first-component zero lemma by sourcing Gamma_eff, K_hat, P_loc, q_* and the compact-local boundary silence; if not, write the first finite eps_q_loc_component bound-input row.",
                "include": "Gamma_eff;K_hat;P_loc;q_*;local vacuum EL identity;compact collar;boundary silence;Z_q;N_Zq;eps_q_loc_component",
                "exclude": "full Z-basis scoring;Y5/Y6/PPN closure;CDB closure;M_AB signature proof;R10 alpha claim;PPN claim;clock/orbital claim;local-GR claim;GitHub action;formalization-workbench edits",
            }
        )
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "copy_id": "COPY2973_0_physical_lock",
                "source_output": str(OUTPUTS["physical_lock"]),
                "branch_copy": str(BRANCH_OUTPUTS["physical_lock_copy"]),
                "status": "copied",
            }
        ),
        add_common(
            {
                "copy_id": "COPY2973_1_qloc",
                "source_output": str(OUTPUTS["qloc_row"]),
                "branch_copy": str(BRANCH_OUTPUTS["qloc_copy"]),
                "status": "copied",
            }
        ),
        add_common(
            {
                "copy_id": "COPY2973_2_next",
                "source_output": str(OUTPUTS["next"]),
                "branch_copy": str(BRANCH_OUTPUTS["next_copy"]),
                "status": "copied",
            }
        ),
    ]


def validation_rows(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    sources = all_rows["sources"]
    physical_lock = all_rows["physical_lock"]
    nz_contract = all_rows["nz_contract"]
    rank_audit = all_rows["rank_audit"]
    qloc = all_rows["qloc_row"]
    claims = all_rows["claims"]
    next_rows = all_rows["next"]

    checks = [
        (
            "VAL2973_0_sources_exist",
            all(row["exists"] for row in sources),
            "all cited local source paths exist",
            True,
        ),
        (
            "VAL2973_1_anchors_found",
            all(row["anchors_found"] for row in sources),
            "all cited source anchors found",
            True,
        ),
        (
            "VAL2973_2_full_lock_blocked",
            any(row["lock2973_id"] == "LOCK2973_6_full_vector" and row["status"] == "FULL_LOCK_NOT_PROVED" for row in physical_lock),
            "full physical Z-basis remains blocked",
            True,
        ),
        (
            "VAL2973_3_qloc_selected",
            any(row["qloc_row_id"] == "QLOC2973_0_definition" for row in qloc),
            "q_loc first component row written",
            True,
        ),
        (
            "VAL2973_4_qloc_nonclaim",
            all(not row["valid_for_claim"] and not row["accepted_for_scoring"] for row in qloc),
            "q_loc component rows remain nonclaim",
            True,
        ),
        (
            "VAL2973_5_nz_not_promoted",
            all(not row["finite_numeric_value"] and not row["theorem_zero"] for row in nz_contract),
            "N_Z/N_Zq normalization not promoted without scale/norm",
            True,
        ),
        (
            "VAL2973_6_rank_fails",
            any(row["rank_audit_id"] == "RG2973_5_verdict" and row["current_status"] == "NOT_PROVED_SELECT_QLOC_FIRST_COMPONENT" for row in rank_audit),
            "full-rank/coercivity gate remains failed",
            True,
        ),
        (
            "VAL2973_7_claims_blocked",
            all(not row["condition_passed"] and not row["claim_allowed"] for row in claims),
            "all claim gates remain blocked",
            True,
        ),
        (
            "VAL2973_8_next_target_written",
            next_rows and next_rows[0]["next_id"] == "NEXT2973_0_2974",
            "2974 q_loc owner/identity next target selected",
            True,
        ),
        (
            "VAL2973_9_branches_exist",
            all(path.exists() for path in BRANCH_OUTPUTS.values()),
            "branch copy files exist",
            True,
        ),
        (
            "VAL2973_10_csvs_parse",
            all(csv_parses(path) for path in OUTPUTS.values() if path != OUTPUTS["validation"]) and all(csv_parses(path) for path in BRANCH_OUTPUTS.values()),
            "all generated CSV files parse",
            True,
        ),
        (
            "VAL2973_11_outputs_under_post_checkpoint",
            all(is_under(path, ROOT) for path in OUTPUTS.values()) and all(is_under(path, ROOT) for path in BRANCH_OUTPUTS.values()),
            "all generated outputs are under post-checkpoint-work",
            True,
        ),
        (
            "VAL2973_12_formalization_clean",
            not any(FORMALIZATION.rglob("*2973*")) if FORMALIZATION.exists() else True,
            "no 2973 outputs were written to formalization-workbench",
            True,
        ),
        (
            "VAL2973_13_doc_written",
            DOC.exists(),
            "2973 markdown checkpoint exists",
            True,
        ),
    ]
    rows = [
        add_common(
            {
                "validation_id": validation_id,
                "passed": bool(passed),
                "check": check,
                "required": required,
            }
        )
        for validation_id, passed, check, required in checks
    ]
    overall = all(row["passed"] for row in rows)
    rows.append(add_common({"validation_id": "VAL2973_OVERALL", "passed": overall, "check": "2973 validation overall", "required": True}))
    return rows


def write_markdown(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    output_rows = [
        {"output": key, "path": str(path), "exists": path.exists()}
        for key, path in OUTPUTS.items()
        if key != "validation"
    ]
    branch_rows = [
        {"copy": key, "path": str(path), "exists": path.exists()}
        for key, path in BRANCH_OUTPUTS.items()
    ]
    text = f"""# 2973 — Y5/R2FR Z-Basis Physical Lock Map and N_Z Normalization, or q_loc First Component

Status: `Y5_R2FR_2973_full_Z_lock_not_proved_q_loc_first_component_selected_nonclaim`

Claim ceiling: `no_full_Z_basis_no_NZ_score_no_q_loc_zero_theorem_no_local_GR_no_Newton_no_R10_no_PPN_no_clock_no_orbital_no_WEP_no_public_claim`

## Summary

- The full physical residual vector `Z^A = N^A_I R_phys^I + O(R_phys^2)` still cannot be adopted: the full-rank/coercive response map is missing.
- The useful move is narrower but sharper: select `q_loc^nu = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{{mu nu}})` as the first component row.
- A conditional zero lemma is now explicit: if the parent local-vacuum identity kills `nabla Gamma_eff - nabla K_hat`, and `P_loc` is q-basic with boundary silence, then `q_loc^nu -> 0`.
- This is not a local-GR proof yet because `q_loc=0` does not force Y5/Y6/PPN/boundary/coupling/readout residuals to vanish.
- Next target is therefore the parent ownership of `Gamma_eff`, `K_hat`, `P_loc`, `q_*`, and the compact-local boundary silence.

## Generated Outputs

{md_table(output_rows, ["output", "path", "exists"])}

## Branch Copies

{md_table(branch_rows, ["copy", "path", "exists"])}

## Physical Lock Attempt

{md_table(all_rows["physical_lock"], ["lock2973_id", "basis_symbol", "physical_channel", "candidate_component", "status", "blocking_gap", "component_live", "full_rank_component"])}

## N_Z / N_Zq Normalization Contract

{md_table(all_rows["nz_contract"], ["nz_contract_id", "object", "candidate_definition", "blocking_gap", "status"])}

## Full-Rank / Coercivity Audit

{md_table(all_rows["rank_audit"], ["rank_audit_id", "criterion", "current_status", "failure_mode", "passed"])}

## q_loc First Component Row

{md_table(all_rows["qloc_row"], ["qloc_row_id", "symbol", "candidate_expression", "units", "status", "accepted_for_scoring"])}

## Claim Gates

{md_table(all_rows["claims"], ["claim_gate_id", "claim", "condition_passed", "status", "claim_allowed"])}

## Decision Ledger

{md_table(all_rows["decision"], ["decision_id", "decision", "reason", "next_action"])}

## Next Target

{md_table(all_rows["next"], ["next_id", "priority", "next_doc", "next_script", "objective", "exclude"])}

## Validation

{md_table(all_rows["validation"], ["validation_id", "passed", "check", "required"])}

Validation overall: `{all_rows["validation"][-1]["passed"]}`.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    all_rows: dict[str, list[dict[str, Any]]] = {
        "sources": source_register_rows(),
        "physical_lock": physical_lock_rows(),
        "nz_contract": nz_contract_rows(),
        "rank_audit": rank_audit_rows(),
        "qloc_row": qloc_component_rows(),
        "claims": claim_gate_rows(),
        "decision": decision_rows(),
        "next": next_target_rows(),
    }

    for key, path in OUTPUTS.items():
        if key in {"branches", "validation"}:
            continue
        write_csv(path, all_rows[key])

    shutil.copyfile(OUTPUTS["physical_lock"], BRANCH_OUTPUTS["physical_lock_copy"])
    shutil.copyfile(OUTPUTS["qloc_row"], BRANCH_OUTPUTS["qloc_copy"])
    shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])
    all_rows["branches"] = branch_copy_rows()
    write_csv(OUTPUTS["branches"], all_rows["branches"])

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)

    print(f"2973 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()

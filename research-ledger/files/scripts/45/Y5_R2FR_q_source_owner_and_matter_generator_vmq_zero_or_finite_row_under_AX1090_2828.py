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

DOC = ROOT / "2828-Y5-R2FR-q-source-owner-and-matter-generator-vmq-zero-or-finite-row-under-AX1090.md"

SRC_2827_NEXT = RESIDUALS / "P8_Y5_R2FR_2827_NEXT_TARGET.csv"
SRC_2827_DERIVATION = RESIDUALS / "P8_Y5_R2FR_2827_DQVM_DERIVATION_LEDGER.csv"
SRC_2827_OUTCOMES = RESIDUALS / "P8_Y5_R2FR_2827_ZERO_NONZERO_DEMOTION_OUTCOME_LEDGER.csv"
SRC_2827_CQM = RESIDUALS / "P8_Y5_R2FR_2827_CQM_AND_LOCAL_LOCK_REENTRY_STATUS.csv"
SRC_2486_DQ = RESIDUALS / "P8_Y5_FIELD_QUOTIENT_2486_DQ_VERTICAL_GENERATOR_LEDGER.csv"
SRC_2486_THEOREM = RESIDUALS / "P8_Y5_FIELD_QUOTIENT_2486_THEOREM_ATTEMPT.csv"
SRC_2486_MATTER = RESIDUALS / "P8_Y5_FIELD_QUOTIENT_2486_MATTER_DESCENT_GATE.csv"
SRC_2486_RESIDUAL = RESIDUALS / "P8_Y5_FIELD_QUOTIENT_2486_RESIDUAL_OWNER_SPLIT.csv"
SRC_1938_WARD = RESIDUALS / "P8_Y5_PARENT_QLOC_1938_WARD_BIANCHI_CONSERVATION_THEOREM.csv"
SRC_1938_PASS = RESIDUALS / "P8_Y5_PARENT_QLOC_1938_CANDIDATE_PASS_MATRIX.csv"
SRC_1896_NOHOM = RESIDUALS / "P8_Y5_PARENT_QLOC_1896_PARENT_SORT_DISJOINTNESS_NOHOM_ATTEMPT.csv"
SRC_2466_HILBERT = RESIDUALS / "P8_Y5_SOURCE_BRIDGE_2466_HILBERT_CURRENT_DESCENT.csv"
SRC_2466_CANDIDATES = RESIDUALS / "P8_Y5_SOURCE_BRIDGE_2466_CURRENT_CANDIDATES.csv"
SRC_2466_WEP = RESIDUALS / "P8_Y5_SOURCE_BRIDGE_2466_WEP_COMPOSITION_GUARDRAIL.csv"
SRC_2467_DIV = RESIDUALS / "P8_Y5_HILBERT_CURRENT_2467_DIVERGENCE_IDENTITY.csv"
SRC_2481_THEOREM = RESIDUALS / "P8_Y5_SOURCE_NORM_2481_THEOREM_ATTEMPT.csv"
SRC_2481_ENORM = RESIDUALS / "P8_Y5_SOURCE_NORM_2481_ENORM_ROW.csv"
SRC_2632_FRONTIER = RESIDUALS / "P8_Y5_SOURCE_PREF_GR_ROLLFORWARD_2632_LOCAL_GR_FRONTIER_MATRIX.csv"
SRC_2632_ROLL = RESIDUALS / "P8_Y5_SOURCE_PREF_GR_ROLLFORWARD_2632_SOURCE_COUPLING_ROLLFORWARD.csv"
SRC_2632_RESIDUAL = RESIDUALS / "P8_Y5_SOURCE_PREF_GR_ROLLFORWARD_2632_RESIDUAL_OWNER_LEDGER.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2828_SOURCE_REGISTER.csv",
    "zero_audit": RESIDUALS / "P8_Y5_R2FR_2828_VMQ_ZERO_PROOF_AUDIT.csv",
    "owner": RESIDUALS / "P8_Y5_R2FR_2828_MATTER_SOURCE_OWNER_LEDGER.csv",
    "finite_row": RESIDUALS / "P8_Y5_R2FR_2828_FIRST_FINITE_VMQ_Q_SOURCE_ROW_NONCLAIM.csv",
    "reentry": RESIDUALS / "P8_Y5_R2FR_2828_CQM_REENTRY_AND_TEST_STATUS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2828_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2828_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2828_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2828_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2828_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "zero_audit_copy": SOURCE_WEIGHT / "vmq_zero_proof_audit_2828_NONCLAIM.csv",
    "finite_row_copy": LOCAL_BOUNDS / "first_finite_vmq_q_source_row_2828_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2828_QBASIC_PUBLIC_COFRAME_OR_FINITE_VMQ_NEXT.csv",
}

BRANCH_ID = "MTS_R2FR_Q_SOURCE_OWNER_MATTER_GENERATOR_VMQ_2828"


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
        ("SRC2828_0_2827_next", SRC_2827_NEXT, "NEXT2827_0_2828", "2827 handoff selecting q-source owner / matter-generator target"),
        ("SRC2828_1_2827_derivation", SRC_2827_DERIVATION, "DER2827_6_matter_generator_condition;DER2827_7_current_evidence", "exact Dq[v_m] kernel condition and unsigned v_m evidence"),
        ("SRC2828_2_2827_outcomes", SRC_2827_OUTCOMES, "OUT2827_1_zero_case;OUT2827_2_nonzero_case", "zero/nonzero outcomes from 2827"),
        ("SRC2828_3_2827_cqm", SRC_2827_CQM, "CQM2827_0_definition;CQM2827_4_next_input", "C_qm reentry blocker and next missing source owner"),
        ("SRC2828_4_2486_dq", SRC_2486_DQ, "DQ2486_1_public_metric;DQ2486_2_q_private", "public branch not vertical and q-private residual channels"),
        ("SRC2828_5_2486_theorem", SRC_2486_THEOREM, "THM2486_1_matter_blindness;THM2486_2_current_signature_application", "conditional matter blindness and failed current application"),
        ("SRC2828_6_2486_matter", SRC_2486_MATTER, "MD2486_0_chain_rule;MD2486_1_no_source_prefactor", "matter descent gate and source-prefactor blocker"),
        ("SRC2828_7_2486_residual", SRC_2486_RESIDUAL, "RS2486_1_q_source;RS2486_3_matter_descent", "q-source and matter-descent residual owners"),
        ("SRC2828_8_1938_ward", SRC_1938_WARD, "WB1938_0_matter_ward_identity;WB1938_3_conservation_verdict", "candidate Hilbert matter Ward theorem"),
        ("SRC2828_9_1938_pass", SRC_1938_PASS, "PASS1938_0_matter_source_owner;PASS1938_2_matter_Ward_conservation", "conditional matter source owner/pass matrix"),
        ("SRC2828_10_1896_nohom", SRC_1896_NOHOM, "NH1896_1_conditional_typed_proof;NH1896_5_verdict", "no-Hom/source-prefactor theorem remains unsigned"),
        ("SRC2828_11_2466_hilbert", SRC_2466_HILBERT, "HIL2466_0_define_T;HIL2466_4_matter_A_coupling", "Hilbert current descent and coupling unification blocker"),
        ("SRC2828_12_2466_candidates", SRC_2466_CANDIDATES, "CUR2466_A_Hilbert_energy_current;CUR2466_B_vertical_Noether_current", "Hilbert current primary, vertical Noether secondary risk"),
        ("SRC2828_13_2466_wep", SRC_2466_WEP, "WEP2466_0_hilbert_universal;WEP2466_3_composition_bound", "WEP guardrail for species-dependent residuals"),
        ("SRC2828_14_2467_div", SRC_2467_DIV, "DIV2467_0_define_current;DIV2467_5_generic_clock", "Hilbert current conservation conditions"),
        ("SRC2828_15_2481_theorem", SRC_2481_THEOREM, "THM2481_0_define_current;THM2481_5_zero_certificate_verdict", "Hilbert/worldtube control branch and full zero gap"),
        ("SRC2828_16_2481_enorm", SRC_2481_ENORM, "ENORM2481_0_E_norm", "source-normalization residual row"),
        ("SRC2828_17_2632_frontier", SRC_2632_FRONTIER, "GRF2632_0_matter_source;GRF2632_3_quotient_readout", "rollforward frontier matrix"),
        ("SRC2828_18_2632_roll", SRC_2632_ROLL, "CROLL2632_5_matter_source_side;CROLL2632_6_gravity_operator", "source side conditionally clean but full GR blocked"),
        ("SRC2828_19_2632_residual", SRC_2632_RESIDUAL, "RES2632_4_DObs_e_R;RES2632_2_e_kappaG", "readout and coupling residual owners"),
    ]
    return [source_row(*spec) for spec in specs]


def zero_audit_rows() -> list[dict[str, Any]]:
    specs = [
        ("ZPA2828_0_exact_gate", "Dq[v_m]=0 iff v_m^q=0", "DER2827_6", "CLOSED_CONDITION", "2827 derived the exact kernel condition but not generator membership", "does not by itself prove zero", SRC_2827_DERIVATION, "DER2827_6_matter_generator_condition"),
        ("ZPA2828_1_qbasic_matter", "S_matter factors only through q-basic public coframe/readout", "THM2486_1 + MD2486_0", "EXACT_CONDITIONAL_NOT_PARENT_SIGNED", "blocked by q_parent, q-basic readout functor, no-marker matter argument list, constants owner", "zero theorem cannot be promoted", SRC_2486_MATTER, "MD2486_0_chain_rule"),
        ("ZPA2828_2_no_source_prefactor", "no active source-only prefactor or species/hidden marker coefficient", "NH1896 + MD2486_1", "NOT_DERIVED", "no-Hom/product proof is conditional; counterexamples and readout/measure stability remain", "finite source-weight/q-source residual survives", SRC_1896_NOHOM, "NH1896_5_verdict"),
        ("ZPA2828_3_hilbert_source", "single Hilbert matter source", "1938 + 2466", "PASS_CONDITIONAL_NONCLAIM", "universal Hilbert stress exists as contract, but parent action signature, preservation, tau, ell_J and coupling unification remain unsigned", "supports route but not v_m^q zero", SRC_1938_PASS, "PASS1938_0_matter_source_owner"),
        ("ZPA2828_4_public_not_vertical", "public metric/coframe variations are not vertical", "DQ2486_1", "PUBLIC_BRANCH_NOT_ZERO", "Hilbert stress varies public geometry; public variations can have Dq_parent nonzero", "do not label matter generator vertical by declaration", SRC_2486_DQ, "DQ2486_1_public_metric"),
        ("ZPA2828_5_q_source_owner", "q_private/source-vector channels must be zeroed or bounded", "RS2486_1", "RESIDUAL_OWNER_RETAINED", "q first-class removal/source-vector zero/source-backed bound not supplied", "finite q-source row required", SRC_2486_RESIDUAL, "RS2486_1_q_source"),
        ("ZPA2828_6_verdict", "prove v_m^q=0 for actual matter/local generator", "ZPA2828_0..5", "ZERO_PROOF_FAILS_CURRENT_EVIDENCE", "strong conditional structure, but no parent-signed q-basic matter/coframe/no-prefactor theorem", "stage finite nonclaim v_m^q row", SRC_2827_OUTCOMES, "OUT2827_1_zero_case"),
    ]
    return [
        nonclaim(
            {
                "audit_id": audit_id,
                "clause": clause,
                "source_logic": logic,
                "status": status,
                "evidence": evidence,
                "effect": effect,
                "source_path": str(source_path),
                "source_anchor": anchor,
                "anchor_found": anchor in read_text(source_path),
                "zero_proved": False,
                "finite_row_required": audit_id == "ZPA2828_6_verdict",
                "control_only": True,
            }
        )
        for audit_id, clause, logic, status, evidence, effect, source_path, anchor in specs
    ]


def owner_rows() -> list[dict[str, Any]]:
    specs = [
        ("OWN2828_0_Hilbert", "Hilbert stress source", "T_matter^{mu nu}=-(2/sqrt(-g)) delta S_matter/delta g_mu_nu", "PRIMARY_CONDITIONAL_OWNER", "best universality route; passes Ward conservation conditionally", "parent matter action signature, public coframe descent, tau/ell_J, and coupling unification", SRC_2466_HILBERT, "HIL2466_0_define_T"),
        ("OWN2828_1_Hilbert_current", "Hilbert energy current", "J_M^nu=ell_J T_matter^{nu rho} tau_rho", "PRIMARY_CONTRACT_NOT_ZERO_THEOREM", "least circular source current and avoids fitted GM", "generic clock exchange and parent scale remain open", SRC_2466_CANDIDATES, "CUR2466_A_Hilbert_energy_current"),
        ("OWN2828_2_vertical_Noether", "vertical Noether current", "J_M^nu=c_A pi_Psi^nu R_M Psi", "SECONDARY_RISK_BRANCH", "matches vertical-generator language", "species charge/WEP risk unless R_M is universal/geometric", SRC_2466_CANDIDATES, "CUR2466_B_vertical_Noether_current"),
        ("OWN2828_3_q_source", "q-source residual owner", "c_q_source;B_qW;C_qT;tail_q", "RETAIN_FINITE_OWNER", "owns the missing v_m^q channel if zero theorem fails", "needs source-vector zero or source-backed bounds", SRC_2486_RESIDUAL, "RS2486_1_q_source"),
        ("OWN2828_4_matter_descent", "matter descent residual owner", "finite_WEP_source_weight;Pi_I_matter", "RETAIN_FINITE_OWNER", "owns active source-only weights if no-Hom fails", "needs no-source-prefactor theorem or WEP/source-normalization bounds", SRC_2486_RESIDUAL, "RS2486_3_matter_descent"),
        ("OWN2828_5_readout", "observed coframe/readout leak", "DObs_e_R", "RETAIN_FINITE_OWNER", "owns q/readout leakage if public coframe is not q-basic", "needs DObs_e[v_X]=0 or finite no-shadow/common-frame vector", SRC_2632_RESIDUAL, "RES2632_4_DObs_e_R"),
    ]
    return [
        nonclaim(
            {
                "owner_id": owner_id,
                "owner": owner,
                "formula_or_residual": formula,
                "status": status,
                "strength": strength,
                "remaining_debt": debt,
                "source_path": str(source_path),
                "source_anchor": anchor,
                "anchor_found": anchor in read_text(source_path),
                "zero_owner_closed": False,
                "finite_owner_retained": "RETAIN" in status,
                "control_only": True,
            }
        )
        for owner_id, owner, formula, status, strength, debt, source_path, anchor in specs
    ]


def finite_row_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "FVQ2828_0_first_row",
            "v_m^q finite source component",
            "epsilon_vmq",
            "epsilon_vmq := ||v_m^q||_{Q_log,*} or ||Dq[v_m]||_{E_q} once E_q and v_m normalization are signed",
            "q_log branch; selected exact Dq formula",
            "MISSING_NUMERIC_VALUE",
            "MISSING_EQ_NORM;MISSING_VM_NORMALIZATION;MISSING_QBASIC_PUBLIC_COFRAME;MISSING_NO_SOURCE_PREFACTOR",
            "PPN;R10;clocks;orbital;local_GR",
            SRC_2827_DERIVATION,
            "DER2827_6_matter_generator_condition",
        ),
        (
            "FVQ2828_1_source_weight_shadow",
            "matter source-prefactor q component",
            "epsilon_vmq_source_weight",
            "finite contribution if source-only weights or hidden/representative markers feed v_m^q",
            "no-Hom/source-prefactor residual",
            "MISSING_NUMERIC_VALUE",
            "MISSING_PARENT_NOHOM;MISSING_READOUT_MEASURE_STABILITY",
            "WEP;source_normalization;local_GR",
            SRC_1896_NOHOM,
            "NH1896_5_verdict",
        ),
        (
            "FVQ2828_2_readout_shadow",
            "public coframe/readout q leak",
            "epsilon_vmq_readout",
            "finite contribution if DObs_e_R or public coframe is not q-basic",
            "q-basic coframe/readout residual",
            "MISSING_NUMERIC_VALUE",
            "MISSING_DOBS_KERNEL;MISSING_TERMINAL_PUBLIC_COFRAME",
            "PPN;clocks;orbital;local_GR",
            SRC_2632_RESIDUAL,
            "RES2632_4_DObs_e_R",
        ),
    ]
    return [
        nonclaim(
            {
                "finite_row_id": row_id,
                "component": component,
                "symbol": symbol,
                "definition": definition,
                "branch_lock": branch_lock,
                "value_status": value_status,
                "blockers": blockers,
                "test_arenas": arenas,
                "source_path": str(source_path),
                "source_anchor": anchor,
                "anchor_found": anchor in read_text(source_path),
                "numeric_value_present": False,
                "source_backed_value": False,
                "theorem_zero": False,
                "control_only": True,
            }
        )
        for row_id, component, symbol, definition, branch_lock, value_status, blockers, arenas, source_path, anchor in specs
    ]


def reentry_rows() -> list[dict[str, Any]]:
    specs = [
        ("RE2828_0_Dq", "Dq[v_m]", "Dq[v_m]=v_m^q", "EXACT_FORMULA_FROM_2827", "formula known, source owner/value not known", False),
        ("RE2828_1_zero", "v_m^q=0", "q-basic matter/coframe + no source-prefactor + constants owner", "NOT_PROVED", "zero theorem fails under current evidence", False),
        ("RE2828_2_finite", "epsilon_vmq", "first finite q-source row staged", "STAGED_NONCLAIM", "ready for source acquisition/theorem-zero attempt, not a prediction", False),
        ("RE2828_3_Cqm", "C_qm", "C_qm=||Dq[v_m]||_{E_q}", "BLOCKED", "E_q, q dual norm, v_m normalization, and epsilon_vmq are missing", False),
        ("RE2828_4_local_lock", "N_lock/Delta_m/K_alg", "control chain from 2825", "NO_REENTRY", "C_qm and T_source_norm not source-backed", False),
        ("RE2828_5_tests", "PPN/R10/clock/orbital", "arena projections of epsilon_vmq", "NO_SCORE", "projection kernels and source-backed values missing", False),
    ]
    return [
        nonclaim(
            {
                "reentry_id": reentry_id,
                "object": obj,
                "formula_or_condition": formula,
                "status": status,
                "reason": reason,
                "reentry_allowed": allowed,
                "control_only": True,
            }
        )
        for reentry_id, obj, formula, status, reason, allowed in specs
    ]


def gate_rows(rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    sources_ok = all(row["path_exists"] and row["anchors_found"] for row in rows["sources"])
    zero_audit_ok = all(row["anchor_found"] for row in rows["zero_audit"])
    zero_failed_honestly = any(row["audit_id"] == "ZPA2828_6_verdict" and row["status"] == "ZERO_PROOF_FAILS_CURRENT_EVIDENCE" for row in rows["zero_audit"])
    finite_rows_ok = all(row["anchor_found"] and not row["numeric_value_present"] and not row["source_backed_value"] and not row["theorem_zero"] for row in rows["finite_row"])
    owner_ok = all(row["anchor_found"] and not row["zero_owner_closed"] for row in rows["owner"])
    reentry_blocked = not any(row["reentry_allowed"] for row in rows["reentry"])
    specs = [
        ("CG2828_0_sources", "source anchors present", sources_ok, "all imported ledgers are reproducible"),
        ("CG2828_1_zero_audit", "v_m^q zero audit completed", zero_audit_ok, "all zero-audit clauses cite source anchors"),
        ("CG2828_2_zero_theorem", "v_m^q=0 theorem proved", False, "matter descent/no-source-prefactor/public coframe clauses are conditional only"),
        ("CG2828_3_zero_not_overclaimed", "zero proof failure recorded honestly", zero_failed_honestly, "2828 does not call v_m vertical by declaration"),
        ("CG2828_4_owner", "source owner ledger complete", owner_ok, "owners retained as conditional/finite, not closed"),
        ("CG2828_5_finite_row", "finite v_m^q rows staged nonclaim", finite_rows_ok, "finite rows have no values and no theorem-zero status"),
        ("CG2828_6_Cqm", "C_qm promotable", False, "E_q, v_m normalization, and epsilon_vmq value are missing"),
        ("CG2828_7_reentry", "local-lock reentry allowed", reentry_blocked is False, "reentry remains blocked"),
        ("CG2828_8_reentry_blocked", "local-lock reentry blocked", reentry_blocked, "no source-backed C_qm or source norm"),
        ("CG2828_9_GR_Newton", "local GR/Newton claim allowed", False, "q=0 selector, Newton-source normalization, and v_m^q zero/value remain missing"),
        ("CG2828_10_PPN_R10", "PPN/R10/clock/orbital claim allowed", False, "arena projections and values missing"),
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
        ("DEC2828_0_zero", "The v_m^q=0 proof does not close.", "ZERO_PROOF_FAILS_CURRENT_EVIDENCE", "matter descent, no-source-prefactor, public coframe, constants owner, tau/ell_J and coupling unification are still conditional", "do not claim vertical silence"),
        ("DEC2828_1_gain", "The source owner is now explicit.", "Q_SOURCE_OWNER_RETAINED", "q-source, source-prefactor, readout, and Hilbert-current owners are separated", "attack the q-basic public coframe/no-source-prefactor theorem or source finite rows"),
        ("DEC2828_2_finite", "Stage finite v_m^q rows.", "FINITE_ROW_STAGED_NONCLAIM", "the theory must pay the coupling bill unless the next theorem-zero closes", "keep epsilon_vmq rows value-missing and nonclaim"),
        ("DEC2828_3_reentry", "Do not reenter local-lock scoring.", "CQM_REENTRY_BLOCKED", "C_qm cannot be computed without E_q/v_m normalization and epsilon_vmq value/theorem-zero", "no PPN/R10/clock/orbital score"),
        ("DEC2828_4_next", "Next target is q-basic public coframe/no-source-prefactor theorem or finite v_m^q acquisition.", "NEXT_2829_QBASIC_OR_FINITE", "this is the least-circular remaining route from the exact Dq gate to local GR discipline", "derive q-basic descent/no-Hom stability or build source-ready finite rows"),
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
                "next_id": "NEXT2828_0_2829",
                "status": "selected_primary",
                "target_doc": "2829-Y5-R2FR-qbasic-public-coframe-no-source-prefactor-or-finite-vmq-acquisition-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_qbasic_public_coframe_no_source_prefactor_or_finite_vmq_acquisition_under_AX1090_2829.py",
                "mission": "try to close the q-basic public coframe/no-source-prefactor theorem needed for v_m^q=0; if it fails, produce source-ready finite epsilon_vmq acquisition rows without claiming local GR/Newton/PPN/R10",
                "acceptance": "must cite 2828 finite rows, 2486 matter descent, 1896 no-Hom, 2466 Hilbert source, and 2632 readout residuals; no numeric placeholders; all claim flags false; formalization-workbench untouched",
                "forbidden": "do not call conditional Hilbert source a q-zero theorem; do not use fitted GM; do not mix q aliases or promote C_qm",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("BR2828_0_zero_audit_copy", OUTPUTS["zero_audit"], BRANCH_OUTPUTS["zero_audit_copy"], "source-weight copy of v_m^q zero proof audit"),
        ("BR2828_1_finite_row_copy", OUTPUTS["finite_row"], BRANCH_OUTPUTS["finite_row_copy"], "local-bounds copy of finite v_m^q q-source rows"),
        ("BR2828_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB acquisition queue for q-basic coframe/no-source-prefactor or finite v_mq target"),
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
        ("VAL2828_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2828_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2828_2_zero_audit_anchors", all(row["anchor_found"] for row in rows_by_name["zero_audit"]), "all zero-audit rows cite found anchors"),
        ("VAL2828_3_zero_not_proved", any(row["audit_id"] == "ZPA2828_6_verdict" and row["status"] == "ZERO_PROOF_FAILS_CURRENT_EVIDENCE" for row in rows_by_name["zero_audit"]), "v_m^q zero proof fails honestly"),
        ("VAL2828_4_owner_anchors", all(row["anchor_found"] for row in rows_by_name["owner"]), "all source-owner rows cite found anchors"),
        ("VAL2828_5_finite_rows_nonclaim", all(not row["numeric_value_present"] and not row["source_backed_value"] and not row["theorem_zero"] for row in rows_by_name["finite_row"]), "finite v_m^q rows are nonclaim and value-missing"),
        ("VAL2828_6_Cqm_blocked", not any(row["reentry_allowed"] for row in rows_by_name["reentry"]), "C_qm/local-lock reentry remains blocked"),
        ("VAL2828_7_claims_blocked", not any(row["claim_allowed"] for row in rows_by_name["gates"]), "no claim gate allows local GR/Newton/PPN/R10"),
        ("VAL2828_8_no_numeric_insertions", no_numeric_insertions(rows_by_name), "no numeric coefficients or prediction values inserted"),
        ("VAL2828_9_next_target_2829", any(row["next_id"] == "NEXT2828_0_2829" and row["selected"] for row in rows_by_name["next"]), "q-basic coframe/no-source-prefactor or finite v_mq target selected next"),
        ("VAL2828_10_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2828_11_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2828_12_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2828_13_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2828_14_no_claim_flags", no_claim_flags(rows_by_name), "no score_ready, valid_prediction_row, valid_for_claim, or claim_allowed flag is true"),
        ("VAL2828_15_generated_under_post_checkpoint", under_root(output_paths + branch_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2828_16_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2828_17_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
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
            "validation_id": "VAL2828_OVERALL",
            "passed": overall,
            "detail": "2828 tests the v_m^q=0 source-owner route, finds only conditional matter/Hilbert/no-Hom evidence, stages finite nonclaim epsilon_vmq rows, keeps C_qm/local-lock/arena claims blocked, and selects q-basic public coframe/no-source-prefactor or finite-vmq acquisition next.",
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
    content = f"""# 2828 - Y5 R2FR q Source Owner And Matter Generator vmq Zero Or Finite Row Under AX1090

Status: `Y5_R2FR_2828_vmq_zero_not_proved_finite_q_source_rows_staged_nonclaim`

## Private Verdict

2828 tests the best honest zero route for the coupling:

`Dq[v_m]=0  iff  v_m^q=0`.

The matter/Hilbert side is genuinely promising: there is a conditional Hilbert stress source, conditional Ward conservation, and a cleaner universal source-current route than species-tuned currents. But it still does **not** prove `v_m^q=0`, because the required q-basic public coframe/readout, no-source-prefactor/no-Hom theorem, constants owner, tau/ell_J ownership, and coupling unification are not parent-signed.

So the correct result is not "dead" and not "closed": the zero theorem fails under current evidence, and the theory must carry a finite nonclaim `epsilon_vmq` row until the q-basic/no-source-prefactor theorem is proved.

## Source Register

{markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## vmq Zero Proof Audit

{markdown_table(rows["zero_audit"], ["audit_id", "clause", "status", "evidence", "effect", "zero_proved", "finite_row_required", "valid_for_claim"])}

## Matter Source Owner Ledger

{markdown_table(rows["owner"], ["owner_id", "owner", "formula_or_residual", "status", "strength", "remaining_debt", "zero_owner_closed", "finite_owner_retained", "valid_for_claim"])}

## First Finite vmq q Source Row

{markdown_table(rows["finite_row"], ["finite_row_id", "component", "symbol", "definition", "value_status", "blockers", "test_arenas", "numeric_value_present", "theorem_zero", "valid_for_claim"])}

## Cqm Reentry And Test Status

{markdown_table(rows["reentry"], ["reentry_id", "object", "formula_or_condition", "status", "reason", "reentry_allowed", "valid_for_claim"])}

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
    rows["zero_audit"] = zero_audit_rows()
    rows["owner"] = owner_rows()
    rows["finite_row"] = finite_row_rows()
    rows["reentry"] = reentry_rows()
    rows["gates"] = gate_rows(rows)
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "zero_audit", "owner", "finite_row", "reentry", "gates", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])

    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2828_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2828_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()

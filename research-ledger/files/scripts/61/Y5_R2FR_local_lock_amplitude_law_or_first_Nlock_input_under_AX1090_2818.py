from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_STARTED_UTC = datetime.now(timezone.utc)
ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
WORK = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
MTS = WORK / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = WORK / "source-intake" / "local_bounds"
RAB_QUEUE = WORK / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = WORK / "source-intake" / "beta-source" / "docs"
MICROSCOPE_DIR = WORK / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SCRIPTS = WORK / "scripts"
DOC = WORK / "2818-Y5-R2FR-local-lock-amplitude-law-or-first-Nlock-input-under-AX1090.md"

SRC_2817_NEXT = MTS / "P8_Y5_R2FR_2817_NEXT_TARGET.csv"
SRC_2817_KILL = MTS / "P8_Y5_R2FR_2817_STRICT_DOUBLE_ZERO_COEFFICIENT_KILL.csv"
SRC_2817_BOUND = MTS / "P8_Y5_R2FR_2817_HILBERT_NORMALIZED_CHAIN_BOUND_SCHEMA.csv"
SRC_1534_NOHAIR = MTS / "P8_Y5_PARENT_QLOC_1534_LOCAL_LOCKING_NOHAIR_THEOREM.csv"
SRC_1534_LEAK = MTS / "P8_Y5_PARENT_QLOC_1534_QUADRATIC_LEAKAGE_BOUND_CONTRACT.csv"
SRC_1536_NLOCK = MTS / "P8_Y5_PARENT_QLOC_1536_NLOCK_ENVELOPE_CONTRACT.csv"
SRC_1536_SILENCE = MTS / "P8_Y5_PARENT_QLOC_1536_EXACT_SILENCE_AUDIT.csv"
SRC_1537_PRIORITY = MTS / "P8_Y5_PARENT_QLOC_1537_FIRST_PRIORITY_NORM_ROWS.csv"
SRC_1537_RUNNER = MTS / "P8_Y5_PARENT_QLOC_1537_NLOCK_RUNNER_INPUT_NONCLAIM.csv"
SRC_1538_NSRC = MTS / "P8_Y5_PARENT_QLOC_1538_N_SRC_THEOREM_OR_BOUND.csv"
SRC_1538_NINNER = MTS / "P8_Y5_PARENT_QLOC_1538_N_INNER_THEOREM_OR_BOUND.csv"
SRC_1538_PAIR = MTS / "P8_Y5_PARENT_QLOC_1538_PAIR_NORM_RUNNER.csv"
SRC_1539_INPUTS = MTS / "P8_Y5_PARENT_QLOC_1539_FIRST_PAIR_INPUT_ACQUISITION_LEDGER.csv"
SRC_1539_SCHEMA = MTS / "P8_Y5_PARENT_QLOC_1539_PAIR_BOUND_SCHEMA_NONCLAIM.csv"
SRC_2737_SOURCE = MTS / "P8_Y5_R2FR_2737_SOURCE_SUPPORT_ZERO_AUDIT.csv"
SRC_2737_INNER = MTS / "P8_Y5_R2FR_2737_INNER_CHARGE_ZERO_AUDIT.csv"
SRC_2737_PAIR = MTS / "P8_Y5_R2FR_2737_FIRST_PAIR_BOUND_CONTRACT.csv"
SRC_2737_ENV = MTS / "P8_Y5_R2FR_2737_TOTAL_SCG_ENVELOPE_ROWS.csv"
SRC_2738_CORE = MTS / "P8_Y5_R2FR_2738_WORLDTUBE_FIRST_PAIR_CORE_TEMPLATE.csv"
SRC_2738_TRACE = MTS / "P8_Y5_R2FR_2738_INNER_CHARGE_TRACE_BOUND_CONTRACT.csv"
SRC_2738_RUNNER = MTS / "P8_Y5_R2FR_2738_FIRST_PAIR_PROFILE_RUNNER_NONCLAIM.csv"
SRC_2739_HUNT = MTS / "P8_Y5_R2FR_2739_PARENT_QNORM_SOURCE_HUNT.csv"
SRC_2739_DUAL = MTS / "P8_Y5_R2FR_2739_DUAL_PAIRING_STATUS.csv"
SRC_2739_DEMOTION = MTS / "P8_Y5_R2FR_2739_LOCAL_CLOSURE_DEMOTION_GATE.csv"
SRC_2739_NEXT = MTS / "P8_Y5_R2FR_2739_NEXT_TARGET.csv"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2818_SOURCE_REGISTER.csv",
    "exact_lock": MTS / "P8_Y5_R2FR_2818_EXACT_LOCK_AUDIT.csv",
    "amplitude": MTS / "P8_Y5_R2FR_2818_LOCAL_LOCK_AMPLITUDE_LAW.csv",
    "first_pair": MTS / "P8_Y5_R2FR_2818_FIRST_NLOCK_INPUT_INTERFACE.csv",
    "chain_update": MTS / "P8_Y5_R2FR_2818_CHAIN_BOUND_UPDATE_WITH_NLOCK.csv",
    "gates": MTS / "P8_Y5_R2FR_2818_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2818_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2818_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2818_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2818_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "exact_queue": RAB_QUEUE / "JR2818_EXACT_LOCK_AUDIT_NONCLAIM.csv",
    "amplitude_queue": RAB_QUEUE / "JR2818_LOCAL_LOCK_AMPLITUDE_LAW_NONCLAIM.csv",
    "pair_queue": RAB_QUEUE / "JR2818_FIRST_NLOCK_INPUT_INTERFACE_NONCLAIM.csv",
    "chain_queue": RAB_QUEUE / "JR2818_CHAIN_BOUND_UPDATE_WITH_NLOCK_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2818_NEXT_PARENT_QSECTOR_NORM_EXTRACTION.csv",
    "beta_doc": BETA_DOCS / "LOCAL_LOCK_AMPLITUDE_LAW_2818_NONCLAIM.csv",
    "local_bound_copy": LOCAL_BOUNDS / "Local_lock_amplitude_law_2818_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_local_lock_amplitude_2818_nonclaim.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sp(path: Path) -> str:
    return str(path)


def ensure_dirs() -> None:
    directories = {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def anchor_found(path: Path, anchor: str) -> bool:
    return anchor in read_text(path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except csv.Error:
        return False


def local_path_tokens(value: Any) -> list[Path]:
    if value is None:
        return []
    paths: list[Path] = []
    for token in str(value).split(";"):
        item = token.strip()
        if not item or item == "MISSING" or item.startswith("http"):
            continue
        candidate = Path(item)
        if not candidate.is_absolute():
            candidate = WORK / item
        if candidate.suffix or candidate.drive:
            paths.append(candidate)
    return paths


def build_sources() -> list[dict[str, Any]]:
    entries = [
        ("SRC2818_0_2817_next", SRC_2817_NEXT, "NEXT2817_0_2818", "2818 handoff"),
        ("SRC2818_1_2817_kill", SRC_2817_KILL, "CK2817_1_exact_double_zero", "coefficient-kill lemma"),
        ("SRC2818_2_2817_bound", SRC_2817_BOUND, "HKB2817_2_Nlock_bridge", "Delta_m bridge target"),
        ("SRC2818_3_1534_nohair", SRC_1534_NOHAIR, "NH1534_3_exact_nohair", "exact no-hair theorem condition"),
        ("SRC2818_4_1534_leak", SRC_1534_LEAK, "LEAK1534_5_Kchain_bound", "leakage bound contract"),
        ("SRC2818_5_1536_nlock", SRC_1536_NLOCK, "NLOCK1536_5_lock_norm", "N_lock envelope"),
        ("SRC2818_6_1536_silence", SRC_1536_SILENCE, "SIL1536_6_exact_lock", "exact lock blocker"),
        ("SRC2818_7_1537_priority", SRC_1537_PRIORITY, "FP1537_4_pair_verdict", "first physical blockers"),
        ("SRC2818_8_1537_runner", SRC_1537_RUNNER, "NLR1537_3_local_lock", "local lock runner missing inputs"),
        ("SRC2818_9_1538_Nsrc", SRC_1538_NSRC, "NSRC1538_4_finite_bound", "N_src finite bound"),
        ("SRC2818_10_1538_Ninner", SRC_1538_NINNER, "NINNER1538_4_finite_bound", "N_inner finite bound"),
        ("SRC2818_11_1538_pair", SRC_1538_PAIR, "PAIR1538_1_finite_pair", "first pair finite formula"),
        ("SRC2818_12_1539_inputs", SRC_1539_INPUTS, "INPUT1539_0_U_B_max", "first-pair input acquisition"),
        ("SRC2818_13_1539_schema", SRC_1539_SCHEMA, "SCHEMA1539_1_finite_first_pair", "first-pair bound schema"),
        ("SRC2818_14_2737_source", SRC_2737_SOURCE, "SZ2737_5_verdict", "source zero not closed"),
        ("SRC2818_15_2737_inner", SRC_2737_INNER, "IC2737_5_verdict", "inner zero not closed"),
        ("SRC2818_16_2737_pair", SRC_2737_PAIR, "FP2737_3_Delta_m_insert", "Delta_m first-pair interface"),
        ("SRC2818_17_2737_env", SRC_2737_ENV, "ENV2737_4_Nsrc", "S_cg total source bound"),
        ("SRC2818_18_2738_core", SRC_2738_CORE, "CORE2738_5_Scg_total", "worldtube source-profile template"),
        ("SRC2818_19_2738_trace", SRC_2738_TRACE, "TR2738_3_Ninner_charge", "inner trace-dual bound"),
        ("SRC2818_20_2738_runner", SRC_2738_RUNNER, "RUN2738_2_first_pair", "first-pair runner not computable"),
        ("SRC2818_21_2739_hunt", SRC_2739_HUNT, "HUNT2739_5_verdict", "parent q-norm absent"),
        ("SRC2818_22_2739_dual", SRC_2739_DUAL, "DUAL2739_3_holder", "same-norm dual pairing"),
        ("SRC2818_23_2739_demotion", SRC_2739_DEMOTION, "DEM2739_4_reentry", "closure demotion and reentry condition"),
        ("SRC2818_24_2739_next", SRC_2739_NEXT, "NEXT2739_0_2740", "parent q-sector norm extraction target"),
    ]
    return [
        {
            "source_id": source_id,
            "path_or_url": sp(path),
            "anchor": anchor,
            "role": role,
            "path_exists": path.exists(),
            "anchor_found": anchor_found(path, anchor),
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": utc_now(),
        }
        for source_id, path, anchor, role in entries
    ]


def build_exact_lock_rows() -> list[dict[str, Any]]:
    rows = [
        ("ELA2818_0_energy_identity", "E_m(u)^2=<u,J_eff>+B_m", "ENERGY_IDENTITY_AVAILABLE", "1534/1536 give the local-lock energy identity.", SRC_1534_NOHAIR, "NH1534_2_energy_identity"),
        ("ELA2818_1_exact_nohair", "J_eff=0, B_m=0, positive operator, no zero mode => Delta_m=0", "CONDITIONAL_NOT_LIVE", "all exact silence premises remain unsigned.", SRC_1534_NOHAIR, "NH1534_3_exact_nohair"),
        ("ELA2818_2_source_silence", "J_src=0 and drift/history/mass-current silence", "BLOCKED", "1536 exact silence audit keeps all source-side components blocked.", SRC_1536_SILENCE, "SIL1536_6_exact_lock"),
        ("ELA2818_3_boundary_silence", "B_inner/no-flux/zero-mode/domain boundary work vanishes", "BLOCKED", "2737/2738 retain inner charge and domain/zero-mode terms.", SRC_2737_INNER, "IC2737_5_verdict"),
        ("ELA2818_4_exact_lock_verdict", "Delta_m=0", "NOT_CLAIMED", "exact no-hair is written but not live-proved; use finite amplitude law.", SRC_1534_NOHAIR, "NH1534_6_verdict"),
    ]
    return [
        {
            "audit_id": audit_id,
            "target_or_condition": target,
            "status": status,
            "finding": finding,
            "source_path": sp(source_path),
            "source_anchor": anchor,
            "anchor_found": anchor_found(source_path, anchor),
            "exact_lock_proved": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": utc_now(),
        }
        for audit_id, target, status, finding, source_path, anchor in rows
    ]


def build_amplitude_rows() -> list[dict[str, Any]]:
    rows = [
        ("ALA2818_0_energy_norm", "E_m(u)", "E_m(u)^2=int_A[D_m|grad u|^2+M_scr^2u^2]", "positive local memory energy norm", "D_m,M_scr,A,zero-mode convention", SRC_1534_LEAK, "LEAK1534_0_energy_norm"),
        ("ALA2818_1_Nlock", "N_lock", "if |<u,J_eff>+B_m|<=N_lock E_m(u), then E_m(u)<=N_lock", "Cauchy/dual-norm bound", "all N_lock component norms", SRC_1536_NLOCK, "NLOCK1536_5_lock_norm"),
        ("ALA2818_2_Delta_m", "Delta_m", "Delta_m:=||m-m_*||_D <= C_emb N_lock", "field amplitude bridge from energy norm to local sup/L2 domain norm", "C_emb/domain/operator constants", SRC_1534_LEAK, "LEAK1534_2_field_bound"),
        ("ALA2818_3_first_pair_insert", "N_lock", "N_lock <= N_pair + N_rest, N_pair:=N_src+N_inner", "first source/boundary pair becomes the first computable interface", "N_pair and N_rest inputs", SRC_2737_PAIR, "FP2737_2_Nlock_insert"),
        ("ALA2818_4_chain_insert", "K_alg^{00}", "||K_alg||_D <= L_min^-2 F2_bar C_emb N_lock M_m_bar + L_min^-3 F2_bar C_emb^2 N_lock^2 M_L_bar + higher-order terms", "2817 chain bound after substituting Delta_m<=C_emb N_lock", "F2_bar,L_min,C_emb,N_lock,M_m_bar,M_L_bar,same norm", SRC_2817_BOUND, "HKB2817_1_double_zero_leakage"),
    ]
    return [
        {
            "law_id": law_id,
            "quantity": quantity,
            "formula": formula,
            "meaning": meaning,
            "missing_to_score": missing,
            "source_path": sp(source_path),
            "source_anchor": anchor,
            "anchor_found": anchor_found(source_path, anchor),
            "derived_in_2818": law_id in {"ALA2818_2_Delta_m", "ALA2818_4_chain_insert"},
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": utc_now(),
        }
        for law_id, quantity, formula, meaning, missing, source_path, anchor in rows
    ]


def build_first_pair_rows() -> list[dict[str, Any]]:
    rows = [
        ("FPI2818_0_Nsrc", "N_src", "N_src <= U_B,max S_cg,total_norm", "source-support leakage", "U_B,max; S_cg,total_norm; E* norm; worldtube support", SRC_2737_ENV, "ENV2737_4_Nsrc"),
        ("FPI2818_1_Ninner", "N_inner,charge", "N_inner,charge <= C_inner ||Q_m^H||_{B*}", "inner compact-source trace contribution", "C_inner; Q_m^H; boundary trace space", SRC_2738_TRACE, "TR2738_3_Ninner_charge"),
        ("FPI2818_2_Npair", "N_pair", "N_pair <= U_B,max S_cg,total_norm + C_inner||Q_m^H||_{B*} + N_inner,domain + N_inner,zero_mode", "first source/boundary pair feeding N_lock", "all worldtube/profile/inner-charge inputs", SRC_2738_TRACE, "TR2738_5_first_pair_insert"),
        ("FPI2818_3_worldtube_inputs", "W_src,J_q,E_q,T_source_norm,U_B,max,S_cg,total,Q_m^H,C_inner", "one shared source/profile template must own every first-pair input", "prevents orbital-GM import and per-arena retuning", "source-backed profile and parent q norm", SRC_2738_CORE, "CORE2738_0_Wsrc"),
        ("FPI2818_4_qnorm_blocker", "E_q", "no parent q norm is accepted, so T_source_norm*C_qm and S_cg,total remain closure-only", "same-norm dual pairing is legal but not computable", "parent q-sector action/norm extraction", SRC_2739_HUNT, "HUNT2739_5_verdict"),
    ]
    return [
        {
            "interface_id": interface_id,
            "quantity": quantity,
            "formula_or_requirement": formula,
            "role": role,
            "missing_to_promote": missing,
            "source_path": sp(source_path),
            "source_anchor": anchor,
            "anchor_found": anchor_found(source_path, anchor),
            "numeric_value_present": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": utc_now(),
        }
        for interface_id, quantity, formula, role, missing, source_path, anchor in rows
    ]


def build_chain_update_rows() -> list[dict[str, Any]]:
    rows = [
        ("CBU2818_0_exact_route", "exact coefficient kill", "if Delta_m=0 and F(m_*)=F'(m_*)=0 then K_alg=0", "not live because exact lock/source-boundary silence is unsigned", "EXACT_ROUTE_BLOCKED_NONCLAIM", SRC_2817_KILL, "CK2817_1_exact_double_zero"),
        ("CBU2818_1_finite_route", "finite leakage", "||K_alg||_D <= L_min^-2 F2_bar C_emb(N_pair+N_rest)M_m_bar + L_min^-3 F2_bar C_emb^2(N_pair+N_rest)^2M_L_bar + ...", "turns first-pair work into the actual Kmetric algebraic-chain residual", "FINITE_ROUTE_FORMULA_READY_INPUTS_MISSING", SRC_2737_PAIR, "FP2737_3_Delta_m_insert"),
        ("CBU2818_2_first_pair_status", "N_pair", "N_pair is not computable because worldtube/profile/qnorm/inner-charge values are missing", "do not claim local lock or local GR", "NOT_COMPUTABLE", SRC_2738_RUNNER, "RUN2738_2_first_pair"),
        ("CBU2818_3_qnorm_status", "parent q norm", "finite first-pair branch is closure-only until E_q/J_q/Dq[v_m] are parent-extracted", "2819 should attack parent q-sector norm extraction", "REENTRY_REQUIRES_PARENT_QSECTOR", SRC_2739_DEMOTION, "DEM2739_4_reentry"),
    ]
    return [
        {
            "update_id": update_id,
            "object": obj,
            "formula_or_status": formula,
            "interpretation": interpretation,
            "status": status,
            "source_path": sp(source_path),
            "source_anchor": anchor,
            "anchor_found": anchor_found(source_path, anchor),
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": utc_now(),
        }
        for update_id, obj, formula, interpretation, status, source_path, anchor in rows
    ]


def build_gate_rows(sections: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    amplitude_law = any(row["law_id"] == "ALA2818_4_chain_insert" and row["derived_in_2818"] for row in sections["amplitude"])
    first_pair_interface = any(row["interface_id"] == "FPI2818_2_Npair" for row in sections["first_pair"])
    exact_lock = all(row["exact_lock_proved"] for row in sections["exact_lock"])
    rows = [
        ("CG2818_0_sources_anchored", "2818 source anchors are present", all(row["anchor_found"] for row in sections["sources"]), "all required anchors were found"),
        ("CG2818_1_exact_lock", "Delta_m=0 exact lock is proved", exact_lock, "source/boundary/operator/zero-mode premises remain unsigned"),
        ("CG2818_2_amplitude_law", "Delta_m/N_lock amplitude law is derived", amplitude_law, "Delta_m<=C_emb N_lock inserted into the 2817 chain bound"),
        ("CG2818_3_first_pair_interface", "first N_lock input interface is staged", first_pair_interface, "N_pair formula exists but values are missing"),
        ("CG2818_4_score_ready", "local-lock residual can be scored", False, "N_pair, N_rest, C_emb, kernels and q norm are not source-backed"),
        ("CG2818_5_local_claim", "local-GR/WEP/PPN/orbital claim can be made", False, "this is a nonclaim amplitude-law bridge only"),
    ]
    return [
        {
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": passed,
            "reason": reason,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for gate_id, claim, passed, reason in rows
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2818_0_exact_lock", "Do not claim exact local lock.", "No source-boundary silence theorem closes J_eff=0 and B_m=0.", "keep Delta_m=0 as theorem target only"),
        ("DEC2818_1_amplitude_law", "Use Delta_m<=C_emb N_lock as the live finite route.", "It connects the coefficient-kill branch to auditable source/profile inputs.", "make every future Kmetric chain bound pass through N_lock"),
        ("DEC2818_2_first_pair", "N_src/N_inner are the first physical N_lock inputs.", "2737/2738 isolate them without importing orbital GM or hiding inner charge.", "source worldtube/qnorm/inner-charge data next"),
        ("DEC2818_3_next", "Parent q-sector norm extraction is the next best attack.", "2739 shows the first-pair route is closure-only until E_q/J_q/Dq[v_m] are parent-owned.", "2819 should write/reopen the parent q-sector action norm contract"),
    ]
    return [
        {
            "decision_id": decision_id,
            "decision": decision,
            "because": because,
            "next_action": next_action,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": utc_now(),
        }
        for decision_id, decision, because, next_action in rows
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2818_0_2819",
            "next_target": "2819-Y5-R2FR-parent-qsector-action-norm-extraction-for-local-lock-reentry-under-AX1090.md",
            "script": "scripts/Y5_R2FR_parent_qsector_action_norm_extraction_for_local_lock_reentry_under_AX1090_2819.py",
            "objective": "extract or reject the parent q-sector norm E_q, source current J_q, and Dq[v_m] norm needed to make T_source_norm, C_qm, S_cg,total_norm, and the 2818 N_pair/N_lock amplitude law source-backed rather than closure-only",
            "include": "parent action slot; positive quadratic form or Hessian; quotient/gauge reduction; J_q; C_qm; boundary handling; units; same-norm guard",
            "exclude": "arena-convenient norm choice; mixed source/Cqm norms; local-GR/Newton/PPN/R10 claim; orbital GM import; GitHub; formalization-workbench edits",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": utc_now(),
        }
    ]


def copy_branches() -> list[dict[str, Any]]:
    copy_plan = [
        (OUTPUTS["exact_lock"], BRANCH_OUTPUTS["exact_queue"], "exact_queue"),
        (OUTPUTS["amplitude"], BRANCH_OUTPUTS["amplitude_queue"], "amplitude_queue"),
        (OUTPUTS["first_pair"], BRANCH_OUTPUTS["pair_queue"], "pair_queue"),
        (OUTPUTS["chain_update"], BRANCH_OUTPUTS["chain_queue"], "chain_queue"),
        (OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next_queue"),
        (OUTPUTS["amplitude"], BRANCH_OUTPUTS["beta_doc"], "beta_doc"),
        (OUTPUTS["amplitude"], BRANCH_OUTPUTS["local_bound_copy"], "local_bound_copy"),
        (OUTPUTS["gates"], BRANCH_OUTPUTS["microscope_copy"], "microscope_copy"),
    ]
    rows = []
    for source, destination, label in copy_plan:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            {
                "copy_id": f"BC2818_{label}",
                "source": sp(source),
                "destination": sp(destination),
                "exists": destination.exists(),
                "valid_for_claim": False,
                "claim_allowed": False,
                "generated_utc": utc_now(),
            }
        )
    return rows


def claim_flags_true(sections: dict[str, list[dict[str, Any]]]) -> bool:
    for key, rows in sections.items():
        if key == "validation":
            continue
        for row in rows:
            if str(row.get("valid_for_claim", "false")).lower() == "true":
                return True
            if str(row.get("claim_allowed", "false")).lower() == "true":
                return True
    return False


def cited_paths_exist(sections: dict[str, list[dict[str, Any]]]) -> bool:
    paths: list[Path] = []
    for rows in sections.values():
        for row in rows:
            for key in ("source_path", "source_paths", "source", "destination", "path_or_url"):
                paths.extend(local_path_tokens(row.get(key)))
    return all(path.exists() for path in paths)


def formalization_untouched_since_run() -> bool:
    if not FORMALIZATION.exists():
        return True
    threshold = RUN_STARTED_UTC.timestamp()
    return not any(path.is_file() and path.stat().st_mtime >= threshold for path in FORMALIZATION.rglob("*"))


def build_validation(sections: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    checks = [
        ("VAL2818_0_sources_exist", all(row["path_exists"] for row in sections["sources"]), "all source-register local paths exist"),
        ("VAL2818_1_source_anchors", all(row["anchor_found"] for row in sections["sources"]), "all source-register anchors were found"),
        ("VAL2818_2_exact_lock_not_claimed", all(not row["exact_lock_proved"] for row in sections["exact_lock"]), "exact Delta_m=0 lock remains unclaimed"),
        ("VAL2818_3_amplitude_law_derived", any(row["law_id"] == "ALA2818_4_chain_insert" and row["derived_in_2818"] for row in sections["amplitude"]), "N_lock amplitude law inserted into K_alg bound"),
        ("VAL2818_4_first_pair_interface", any(row["interface_id"] == "FPI2818_2_Npair" for row in sections["first_pair"]), "first Nlock input interface staged"),
        ("VAL2818_5_qnorm_blocker_retained", any(row["interface_id"] == "FPI2818_4_qnorm_blocker" for row in sections["first_pair"]), "parent q-norm blocker retained"),
        ("VAL2818_6_chain_update_nonclaim", all(not row["score_ready"] and not row["claim_allowed"] for row in sections["chain_update"]), "chain update rows remain nonclaim"),
        ("VAL2818_7_claim_gates_safe", all(str(row["claim_allowed"]).lower() == "false" for row in sections["gates"]), "all claim gates keep claims blocked"),
        ("VAL2818_8_next_target_2819", any(row["next_id"] == "NEXT2818_0_2819" for row in sections["next"]), "next target is 2819"),
        ("VAL2818_9_branch_outputs_exist", all(path.exists() for path in BRANCH_OUTPUTS.values()), "branch copies were written"),
        ("VAL2818_10_outputs_exist", all(path.exists() for path in generated_paths), "all generated output paths exist"),
        ("VAL2818_11_csv_parse", all(csv_parses(path) for path in generated_paths), "all generated CSV outputs parse"),
        ("VAL2818_12_cited_paths_exist", cited_paths_exist(sections), "all cited local file/copy paths in generated rows exist"),
        ("VAL2818_13_no_claim_flags", not claim_flags_true(sections), "no valid_for_claim or claim_allowed flag is true"),
        ("VAL2818_14_generated_under_post_checkpoint", all(str(path).startswith(str(WORK)) for path in generated_paths + [DOC]), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2818_15_formalization_untouched", formalization_untouched_since_run(), "formalization-workbench was not modified during this run"),
        ("VAL2818_16_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    rows = [{"validation_id": check_id, "passed": bool(passed), "detail": detail, "generated_utc": utc_now()} for check_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2818_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2818 keeps exact local lock unclaimed, derives the Delta_m<=C_emb N_lock amplitude bridge into the K_alg bound, and routes first N_lock inputs through N_pair plus the parent q-norm blocker.",
            "generated_utc": utc_now(),
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns)
        + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def build_doc(sections: dict[str, list[dict[str, Any]]]) -> str:
    lines = [
        "# 2818 - Y5 R2FR Local Lock Amplitude Law Or First Nlock Input Under AX1090",
        "",
        "## Private Verdict",
        "",
        "2818 does not prove exact local lock `Delta_m=0`. The exact no-hair route is still blocked by source silence, boundary/no-flux, zero-mode, and operator/domain ownership.",
        "",
        "The useful progress is the finite route: from the energy identity and dual-norm estimate, `Delta_m <= C_emb N_lock`. Substituting this into the 2817 strict-double-zero chain gives a concrete nonclaim algebraic-chain envelope in terms of `N_lock`.",
        "",
        "The first physical `N_lock` inputs are now explicit: `N_pair=N_src+N_inner`, with `N_src <= U_B,max S_cg,total_norm` and `N_inner <= C_inner ||Q_m^H||` plus domain/zero-mode terms. The live blocker is parent q-sector norm extraction, because `E_q`, `J_q`, and `Dq[v_m]` are still absent.",
        "",
        "## Exact Lock Audit",
        markdown_table(sections["exact_lock"], ["audit_id", "target_or_condition", "status", "finding"]),
        "",
        "## Local Lock Amplitude Law",
        markdown_table(sections["amplitude"], ["law_id", "quantity", "formula", "missing_to_score", "derived_in_2818"]),
        "",
        "## First Nlock Input Interface",
        markdown_table(sections["first_pair"], ["interface_id", "quantity", "formula_or_requirement", "missing_to_promote"]),
        "",
        "## Chain Bound Update",
        markdown_table(sections["chain_update"], ["update_id", "object", "status", "formula_or_status"]),
        "",
        "## Claim Gates",
        markdown_table(sections["gates"], ["gate_id", "claim", "gate_pass", "claim_allowed", "reason"]),
        "",
        "## Decision Ledger",
        markdown_table(sections["decision"], ["decision_id", "decision", "because", "next_action"]),
        "",
        "## Validation",
        markdown_table(sections["validation"], ["validation_id", "passed", "detail"]),
        "",
        "## Next Target",
        markdown_table(sections["next"], ["next_id", "next_target", "objective", "include", "exclude"]),
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    ensure_dirs()
    if (SCRIPTS / "__pycache__").exists():
        shutil.rmtree(SCRIPTS / "__pycache__")

    sections: dict[str, list[dict[str, Any]]] = {
        "sources": build_sources(),
        "exact_lock": build_exact_lock_rows(),
        "amplitude": build_amplitude_rows(),
        "first_pair": build_first_pair_rows(),
        "chain_update": build_chain_update_rows(),
    }
    sections["gates"] = build_gate_rows(sections)
    sections["decision"] = build_decision_rows()
    sections["next"] = build_next_rows()

    for key, rows in sections.items():
        if key in OUTPUTS:
            write_csv(OUTPUTS[key], rows)
    sections["branches"] = copy_branches()
    write_csv(OUTPUTS["branches"], sections["branches"])
    sections["validation"] = build_validation(sections)
    write_csv(OUTPUTS["validation"], sections["validation"])
    DOC.write_text(build_doc(sections), encoding="utf-8")
    print(f"wrote {DOC}")
    print(f"validation overall: {sections['validation'][-1]['passed']}")


if __name__ == "__main__":
    main()

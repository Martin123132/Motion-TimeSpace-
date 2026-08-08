from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3859"
BRANCH = "MTS_R2FR_Y5_TAU_H_CSTAR_PARENT_OWNERSHIP_FROM_QOBS_OR_FRAME_RESIDUAL_BOUND_3859"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3859-Y5-R2FR-tau-h-cstar-parent-ownership-from-qobs-or-frame-residual-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

CSV_3858_THEOREM = OUT / "P8_Y5_R2FR_3858_MTS_METRIC_BRIDGE_THEOREM.csv"
CSV_3858_AUDIT = OUT / "P8_Y5_R2FR_3858_SIGNATURE_CONDITION_AUDIT.csv"
CSV_3858_BOUND = OUT / "P8_Y5_R2FR_3858_METRIC_BRIDGE_RESIDUAL_BOUND.csv"
CSV_3858_GATES = OUT / "P8_Y5_R2FR_3858_CLAIM_GATES.csv"
CSV_3858_VALIDATION = OUT / "P8_Y5_BRR545_3858_VALIDATION.csv"
CSV_3846_THEOREM = OUT / "P8_Y5_R2FR_3846_METRIC_BRIDGE_THEOREM.csv"
CSV_3846_OWNER = OUT / "P8_Y5_R2FR_3846_MTS_PRIMITIVE_OWNERSHIP_AUDIT.csv"
CSV_3517_QMAP = OUT / "P8_EM_actual_q_map_vertical_basis_candidate.csv"
CSV_3765_QOBS = OUT / "P8_Y5_R2FR_3765_QOBS_CANDIDATE_MAP.csv"
CSV_3765_VERDICT = OUT / "P8_Y5_R2FR_3765_PARENT_QOBS_VERDICT.csv"
CSV_3764_QOBS = OUT / "P8_Y5_R2FR_3764_PARENT_QUOTIENT_DESCENT_THEOREM.csv"
CSV_3504_HODGE = OUT / "P8_Y5_R2FR_3504_HODGE_UNIQUENESS_THEOREM.csv"
CSV_3504_GATE = OUT / "P8_Y5_R2FR_3504_PARENT_SIGNATURE_GATE.csv"
CSV_FRAME_SPLIT = OUT / "P8_frame_source_split_residual_or_zero.csv"
CSV_2504_LAPSE = OUT / "P8_Y5_NO_SHADOW_2504_V_LAPSE_READOUT_BRIDGE.csv"
CSV_2505_PPN = OUT / "P8_Y5_NO_SHADOW_2505_PPN_READOUT_VECTOR.csv"
CSV_1030_CONTRACT = OUT / "P8_Y5_R10_1030_PUBLIC_METRIC_ACTION_CONTRACT.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3859_SOURCE_REGISTER.csv",
    "theorem": OUT / "P8_Y5_R2FR_3859_QBASIC_TAU_H_CSTAR_THEOREM.csv",
    "audit": OUT / "P8_Y5_R2FR_3859_TAU_H_CSTAR_OWNERSHIP_AUDIT.csv",
    "residual": OUT / "P8_Y5_R2FR_3859_FRAME_CLOCK_PREFERRED_RESIDUAL_BOUND.csv",
    "gates": OUT / "P8_Y5_R2FR_3859_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3859_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3859_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3859_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3859_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3859_00_3858_theorem", CSV_3858_THEOREM, "EXACT_CONDITIONAL_LORENTZIAN_BRIDGE", "3858 Lorentzian bridge theorem"),
    ("SRC3859_01_3858_audit", CSV_3858_AUDIT, "B_tau_owner", "3858 ownership audit"),
    ("SRC3859_02_3858_bound", CSV_3858_BOUND, "B_metric_bridge_3858", "3858 bridge residual"),
    ("SRC3859_03_3858_gates", CSV_3858_GATES, "PASS_3859_TAU_H_CSTAR_OWNERSHIP_TARGET", "3859 target selection"),
    ("SRC3859_04_3858_validation", CSV_3858_VALIDATION, "PASS", "previous validation"),
    ("SRC3859_05_3846_theorem", CSV_3846_THEOREM, "EXACT_CONDITIONAL_COFRAME_EMBEDDING", "older coframe bridge corroboration"),
    ("SRC3859_06_3846_owner", CSV_3846_OWNER, "LOCAL_RADIAL_TEMPLATE_NOT_FULL_PARENT_OBJECT", "older ownership audit"),
    ("SRC3859_07_3517_qmap", CSV_3517_QMAP, "CANDIDATE_VISIBLE_TAU_LOCK_UNSIGNED", "q-map tau/public geometry candidate"),
    ("SRC3859_08_3765_qobs", CSV_3765_QOBS, "q_obs_candidate", "q_obs candidate object"),
    ("SRC3859_09_3765_verdict", CSV_3765_VERDICT, "QOBS_CANDIDATE_CONSTRUCTED_BUT_NOT_PARENT_SIGNED", "q_obs verdict"),
    ("SRC3859_10_3764_qobs", CSV_3764_QOBS, "EXACT_CONDITIONAL_ZERO_THEOREM", "single-frame theorem"),
    ("SRC3859_11_3504_hodge", CSV_3504_HODGE, "conformally invariant", "coframe/Hodge scale caveat"),
    ("SRC3859_12_3504_gate", CSV_3504_GATE, "e_obs=e_bar(q)", "e_obs q-basic gate"),
    ("SRC3859_13_frame_split", CSV_FRAME_SPLIT, "SEEDED_NONCLAIM_3048_MISSING_SOURCE_VARIATION_FRAME_THEOREM", "frame/source residual fallback"),
    ("SRC3859_14_2504_lapse", CSV_2504_LAPSE, "v:=log(N_obs^2/c^2)", "lapse clock route"),
    ("SRC3859_15_2505_ppn", CSV_2505_PPN, "BETA_LAW_MATCHES_EH", "lapse beta readout"),
    ("SRC3859_16_1030_contract", CSV_1030_CONTRACT, "CONTRACT_READY_NOT_CURRENT_THEOREM", "public metric action contract"),
]

COFRAME_ROUTE = "e_obs=(theta^0,theta^i), tau_time=theta^0/c_*, h_space=delta_ij theta^i theta^j, g_obs=-theta^0 theta^0+delta_ij theta^i theta^j"
QBASIC_CHAIN = "if e_obs=e_bar(q_obs), c_*=c_bar(q_obs), and v in ker(Dq_obs), then D_v tau_time=0, D_v h_space=0, D_v c_*=0"
OWNERSHIP_THEOREM = (
    "If q_obs parent-owns one nondegenerate observed coframe e_obs, a positive q-basic conversion constant c_*, "
    "and all ordinary sector readouts factor through q_obs, then tau_time=e_obs^0/c_* and "
    "h_space=delta_ij e_obs^i e_obs^j are q_obs-basic same-stack parent objects. "
    "Therefore B_tau_owner=B_h_owner=B_cstar_owner=0 and the 3858 metric bridge is owned."
)
CURRENT_BLOCK = (
    "current corpus has public geometry/tau/coupling slots as candidates, but q_obs/e_obs/c_* are not parent-signed "
    "and sector factorization/source-frame descent remains unsigned"
)
RESIDUAL_BOUND = (
    "B_tau_h_cstar_owner_3859 <= "
    "B_qobs_parent_signature+B_eobs_basic+B_tau_clock_lock+B_cstar_superselection+"
    "B_spatial_triad_rank+B_sector_factorization+B_clock_scale+B_frame_source_split+"
    "B_preferred_frame_motion+B_EM_conformal_scale"
)


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PCW))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def source_register_rows(timestamp: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, path, needle, role in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "checkpoint": CHECKPOINT,
                "path": rel(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "claim_use": "nonclaim_qbasic_ownership_test",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "theorem_id": "QBO3859_0_coframe_route",
            "step": "coframe reconstruction route",
            "statement": COFRAME_ROUTE,
            "proof": "a nondegenerate observed coframe separates the time leg, spatial triad, metric, and volume data",
            "current_result": "EXACT_CONDITIONAL_CONSTRUCTION",
            "status": "COFRAME_ROUTE_WRITTEN",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "QBO3859_1_chain_rule",
            "step": "q-basic ownership chain rule",
            "statement": QBASIC_CHAIN,
            "proof": "D_v f_bar(q_obs(Phi)) = Df_bar[Dq_obs(v)] = 0 for every vertical v",
            "current_result": "EXACT_CHAIN_RULE_ZERO",
            "status": "EXACT_CONDITIONAL_QBASIC_ZERO_THEOREM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "QBO3859_2_owner_theorem",
            "step": "tau/h/c owner theorem",
            "statement": OWNERSHIP_THEOREM,
            "proof": "combine the coframe route with the q-basic chain rule and sector-factorization premise",
            "current_result": "THEOREM_DERIVED_CONDITIONALLY",
            "status": "EXACT_CONDITIONAL_OWNER_THEOREM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "QBO3859_3_conformal_caveat",
            "step": "scale no-overclaim guard",
            "statement": "EM/light-cone or Hodge agreement can fix a conformal class, but c_* and clock/source scale still need parent ownership.",
            "proof": "4D Hodge star on two-forms is conformally invariant, so null-cone agreement alone cannot derive all clock/source scale data",
            "current_result": "NO_LIGHTCONE_ONLY_VICTORY",
            "status": "SCALE_GUARD_ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "QBO3859_4_current_verdict",
            "step": "strict-current ownership test",
            "statement": CURRENT_BLOCK,
            "proof": "q-map/public tau/coupling rows are candidates; 3765 and 1030 say they are not parent-signed",
            "current_result": "TAU_H_CSTAR_NOT_CLAIMED_CURRENT_CORPUS",
            "status": "CURRENT_NONCLAIM_RESIDUAL_BOUND_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def audit_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "audit_id": "THC3859_0_qobs_signature",
            "object": "q_obs/e_obs parent signature",
            "required_identity": "e_obs=e_bar(q_obs) and q_obs is parent-signed",
            "current_evidence": "3765 q_obs candidate exists, 3517 public geometry slot exists, but both remain unsigned",
            "passes_current_branch": False,
            "residual_owner": "B_qobs_parent_signature+B_eobs_basic",
            "next_action": "derive e_obs basicness from parent pullback/kernel-null theorem or retain frame residual",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "THC3859_1_tau_clock",
            "object": "tau_time",
            "required_identity": "tau_time=e_obs^0/c_* and D_v tau_time=0 for v in ker(Dq_obs)",
            "current_evidence": "3517 names public tau clock; 2504 lapse readout is coherent; no parent-signed tau lock",
            "passes_current_branch": False,
            "residual_owner": "B_tau_clock_lock+B_clock_scale",
            "next_action": "prove single tau is used by H_tau, clocks, R10, orbit, and source support",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "THC3859_2_h_space",
            "object": "h_space",
            "required_identity": "h_space=delta_ij e_obs^i e_obs^j is rank-3 positive and q-basic",
            "current_evidence": "3846/3858 prove algebraic positivity if data supplied; spatial triad parent ownership remains unsigned",
            "passes_current_branch": False,
            "residual_owner": "B_spatial_triad_rank+B_h_owner",
            "next_action": "derive spatial triad/rank/positivity from MTS coframe or retain preferred-frame/spatial residual",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "THC3859_3_cstar",
            "object": "c_*",
            "required_identity": "c_*=c_bar(q_obs) is positive and superselected/quotient-owned",
            "current_evidence": "3517 coupling/matter constant slots include c_vis conditionally; no c_* superselection proof",
            "passes_current_branch": False,
            "residual_owner": "B_cstar_superselection+B_EM_conformal_scale",
            "next_action": "derive c_* as q-basic conversion constant or retain unit/clock/source scale residual",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "THC3859_4_sector_same_stack",
            "object": "sector factorization",
            "required_identity": "r_s=F_s o q_obs for matter, EM, clocks, photons, orbital/source readout",
            "current_evidence": "3764 gives exact conditional theorem and 1030 writes contract; parent signature still absent",
            "passes_current_branch": False,
            "residual_owner": "B_sector_factorization+B_frame_source_split",
            "next_action": "attach same parent pullback to source variation and matter/clock readout",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "THC3859_5_motion_preferred",
            "object": "motion flow",
            "required_identity": "u is the coframe time leg; no independent motion/preferred-frame metric survives",
            "current_evidence": "3538 says flow is clean if inherited from same stack; 3858 keeps preferred-frame motion residual",
            "passes_current_branch": False,
            "residual_owner": "B_preferred_frame_motion",
            "next_action": "prove u belongs to the same q_obs coframe stack or retain alpha_i/preferred-frame residuals",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def residual_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "FCB3859_0_tau_h_cstar_bound",
            "observable": "B_tau_h_cstar_owner_3859",
            "formula": RESIDUAL_BOUND,
            "meaning": "residual preventing tau_time, h_space, and c_* from being parent-owned same-stack bridge objects",
            "status": "NONCLAIM_BOUND_EXPLICIT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "FCB3859_1_metric_bridge_update",
            "observable": "B_metric_bridge_3858",
            "formula": "B_metric_bridge_3858 <= B_tau_h_cstar_owner_3859+B_nonLC_connection+B_units_orientation+B_preferred_frame_motion",
            "meaning": "3859 replaces the tau/h/c owner slots with a q-basic coframe ownership theorem or residual vector",
            "status": "METRIC_BRIDGE_BOUND_REFINED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "FCB3859_2_if_closed",
            "observable": "tau/h/c ownership",
            "formula": "if B_tau_h_cstar_owner_3859=0 then tau_time,h_space,c_* are q_obs-basic and the algebraic Lorentzian bridge is parent-owned up to nonLC/readout guards",
            "meaning": "this closes the first owner throat of the visible EH action route",
            "status": "EXACT_CONDITIONAL_WIN_PATH",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "FCB3859_3_fallback_rows",
            "observable": "frame/clock/preferred residual fallback",
            "formula": "F_frame=(delta_frame_source, alpha_clock_redshift, C_Hodge_hidden, Delta_conformal_scale, alpha1, alpha2, alpha3)",
            "meaning": "if parent ownership fails, the failure routes into existing empirical arenas instead of closure assumptions",
            "status": "EMPIRICAL_FALLBACK_VECTOR",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "GATE3859_0_sources",
            "gate": "source-backed tau/h/c inputs resolved",
            "status": "PASS_SOURCE_REGISTERED",
            "claim_allowed": False,
            "reason": "all tau/h/c ownership inputs are local source rows from 2504/2505/3504/3517/3764/3765/3846/3858/1030",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3859_1_chain_rule",
            "gate": "q-basic tau/h/c theorem",
            "status": "PASS_EXACT_CONDITIONAL_QBASIC_THEOREM",
            "claim_allowed": False,
            "reason": "if e_obs and c_* descend through q_obs, tau_time,h_space,c_* are vertical-silent by chain rule",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3859_2_current_owner",
            "gate": "current corpus owns tau/h/c",
            "status": "BLOCKED_TAU_H_CSTAR_NOT_PARENT_SIGNED",
            "claim_allowed": False,
            "reason": CURRENT_BLOCK,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3859_3_scale_guard",
            "gate": "no light-cone-only scale overclaim",
            "status": "PASS_CONFORMAL_SCALE_GUARD",
            "claim_allowed": False,
            "reason": "Hodge/light cone agreement does not by itself derive c_*, clock scale, source scale, or Newton normalization",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3859_4_local_GR",
            "gate": "strict-current metric/action/local-GR claim",
            "status": "BLOCKED_LOCAL_GR_CLAIM",
            "claim_allowed": False,
            "reason": "q_obs/e_obs parent signature, c_* superselection, sector factorization, source frame, and non-LC guards remain active",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3859_5_next",
            "gate": "next target selected",
            "status": "PASS_3860_COFRAME_BASICNESS_TARGET",
            "claim_allowed": False,
            "reason": "tau/h/c ownership now reduces to q_obs/e_obs coframe basicness or explicit frame-source residuals",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC3859_0",
            "decision": "tau/h/c ownership is derivable from a q_obs-owned coframe plus q-basic c_*",
            "consequence": "the next proof does not need to invent a new metric field; it needs coframe basicness",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3859_1",
            "decision": "strict current corpus does not yet sign tau/h/c ownership",
            "consequence": "metric bridge remains nonclaim, with explicit frame/clock/preferred residuals",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3859_2",
            "decision": "target q_obs/e_obs basicness next",
            "consequence": "3860 should prove public coframe basicness from parent pullback/kernel-null or retain the residual vector",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3859_0",
            "next_checkpoint": "3860-Y5-R2FR-coframe-basicness-from-parent-pullback-or-frame-source-residual-bound.md",
            "script": "scripts/Y5_R2FR_3860_coframe_basicness_from_parent_pullback_or_frame_source_residual_bound.py",
            "objective": "prove e_obs is q_obs-basic from parent action pullback/kernel-null conditions, or route the failure into frame/source/clock/preferred residual bounds",
            "reason": "3859 shows tau_time,h_space,c_* close by chain rule once the public coframe and c_* are parent-signed",
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "status": "PASS_NONCLAIM_EXACT_QBASIC_TAU_H_CSTAR_THEOREM_CURRENTLY_BLOCKED",
            "claim": "no tau/h/c ownership, g_obs adoption, visible EH action adoption, beta, PPN, Newton, EM, or local-GR claim",
            "result": "exact q-basic chain-rule owner theorem derived; current corpus blocked by q_obs/e_obs/c_* parent signature and sector/source-frame descent",
            "next": "3860 coframe basicness from parent pullback or frame-source residual bound",
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def write_doc(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    audit: list[dict[str, object]],
    residual: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    timestamp: str,
) -> None:
    text = f"""# 3859 - Tau H Cstar Parent Ownership From Qobs Or Frame Residual Bound

Private checkpoint. This attacks the ownership gap left by 3858: are `tau_time`, `h_space`, and `c_*` actually MTS/q_obs-owned, or just bridge ingredients we inserted?

Generated: `{timestamp}`

## Result

The coframe route is:

`{COFRAME_ROUTE}`.

The q-basic chain rule is:

`{QBASIC_CHAIN}`.

The exact conditional ownership theorem is:

`{OWNERSHIP_THEOREM}`.

The strict current result is still blocked:

`{CURRENT_BLOCK}`.

The finite ownership residual is:

`{RESIDUAL_BOUND}`.

This is a real narrowing. The next proof is not "derive the whole metric again"; it is to prove `e_obs` and `c_*` are parent-signed q_obs-basic objects. If that fails, the failure is already routed into frame/source, clock, EM conformal-scale, and preferred-frame residual rows.

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## Q-basic Tau/H/Cstar Theorem

{markdown_table(theorem, ["theorem_id", "step", "status", "current_result"])}

## Tau/H/Cstar Ownership Audit

{markdown_table(audit, ["audit_id", "object", "passes_current_branch", "residual_owner", "next_action"])}

## Frame Clock Preferred Residual Bound

{markdown_table(residual, ["row_id", "observable", "status", "formula"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "consequence"])}

## Bottom Line

3859 proves the exact q-basic chain-rule route: once `e_obs` and `c_*` are parent-owned, `tau_time`, `h_space`, and `c_*` stop being independent assumptions. Current MTS does not yet sign that ownership, so no local-GR claim opens. The next target is public coframe basicness from parent pullback/kernel-null conditions.

Next target: `3860-Y5-R2FR-coframe-basicness-from-parent-pullback-or-frame-source-residual-bound.md`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3858", "Current State After 3859", 1)
    text = "\n".join(
        line for line in text.splitlines() if not line.startswith("<!-- Generated by 3859 at ")
    )
    paragraph = (
        "`3859` attacks the parent-ownership throat for the metric bridge ingredients. "
        "It proves the q-basic chain-rule route: if `e_obs=e_bar(q_obs)` and `c_*=c_bar(q_obs)`, then for every vertical `v in ker(Dq_obs)`, `D_v tau_time=0`, `D_v h_space=0`, and `D_v c_*=0` with `tau_time=e_obs^0/c_*` and `h_space=delta_ij e_obs^i e_obs^j`. "
        "Thus `tau_time`, `h_space`, and `c_*` are not separate assumptions once the public coframe and conversion constant are parent-signed. "
        "The strict current corpus remains nonclaim because `q_obs/e_obs/c_*` parent signature, sector factorization, source-frame descent, clock scale, and preferred-frame silence are not all signed. "
        "The next target is public coframe basicness from parent action pullback/kernel-null conditions.\n\n"
    )
    if paragraph not in text and "## Next Best Gate" in text:
        text = text.replace("## Next Best Gate", paragraph + "## Next Best Gate", 1)
    old_gate = """`3859-Y5-R2FR-tau-h-cstar-parent-ownership-from-qobs-or-frame-residual-bound.md`

Target: prove `tau_time`, `h_space`, and `c_*` are q_obs-basic same-stack parent objects, or emit explicit frame/clock/preferred residual bounds.

This is the best next move because 3858 solves the algebraic Lorentzian bridge conditionally; the remaining hard proof is parent ownership of its ingredients."""
    new_gate = """`3860-Y5-R2FR-coframe-basicness-from-parent-pullback-or-frame-source-residual-bound.md`

Target: prove `e_obs` is q_obs-basic from parent action pullback/kernel-null conditions, or route failure into frame/source/clock/preferred residual bounds.

This is the best next move because 3859 shows `tau_time`, `h_space`, and `c_*` close by chain rule once the public coframe and conversion constant are parent-signed."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3859_QBASIC_TAU_H_CSTAR_THEOREM.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3859_TAU_H_CSTAR_OWNERSHIP_AUDIT.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3859_FRAME_CLOCK_PREFERRED_RESIDUAL_BOUND.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3859_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3859_QBASIC_TAU_H_CSTAR_THEOREM.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    text = text.rstrip() + f"\n\n<!-- Generated by 3859 at {timestamp} -->\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    audit: list[dict[str, object]],
    residual: list[dict[str, object]],
    gates: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "check": check,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "timestamp_utc": timestamp,
            }
        )

    all_text = " ".join(str(row) for row in theorem + audit + residual + gates)
    add(
        "VAL3859_0_sources",
        "all cited source paths exist and needles are found",
        all(row["exists"] and row["needle_found"] for row in sources),
        f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved",
    )
    add(
        "VAL3859_1_chain_rule",
        "q-basic chain rule theorem is explicit",
        "EXACT_CHAIN_RULE_ZERO" in all_text and "D_v tau_time=0" in all_text,
        "chain-rule zero route present",
    )
    add(
        "VAL3859_2_owner_theorem",
        "tau/h/c owner theorem is explicit",
        "EXACT_CONDITIONAL_OWNER_THEOREM" in all_text and "B_tau_owner=B_h_owner=B_cstar_owner=0" in all_text,
        "conditional owner theorem present",
    )
    add(
        "VAL3859_3_current_block",
        "strict-current ownership remains blocked",
        "TAU_H_CSTAR_NOT_CLAIMED_CURRENT_CORPUS" in all_text and "BLOCKED_TAU_H_CSTAR_NOT_PARENT_SIGNED" in all_text,
        "owner theorem not promoted to claim",
    )
    add(
        "VAL3859_4_residual_vector",
        "frame/clock/preferred residual vector is explicit",
        "B_tau_h_cstar_owner_3859" in all_text and "delta_frame_source" in all_text and "Delta_conformal_scale" in all_text,
        "fallback vector written",
    )
    add(
        "VAL3859_5_scale_guard",
        "conformal scale overclaim guard active",
        "NO_LIGHTCONE_ONLY_VICTORY" in all_text and "PASS_CONFORMAL_SCALE_GUARD" in all_text,
        "light cone/Hodge alone cannot fix cstar/source scale",
    )
    add(
        "VAL3859_6_nonclaim",
        "all rows remain nonclaim",
        all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in theorem + audit + residual + gates),
        "valid_for_claim/claim_allowed false throughout",
    )
    add(
        "VAL3859_7_next",
        "next target is 3860 coframe basicness",
        DOC_PATH.exists() and "3860-Y5-R2FR-coframe-basicness-from-parent-pullback-or-frame-source-residual-bound" in read_text(DOC_PATH),
        "3860 coframe basicness target visible",
    )
    for key, output_path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed = False
        detail = rel(output_path)
        if output_path.suffix == ".csv" and output_path.exists():
            count = len(read_csv_rows(output_path))
            parsed = count > 0
            detail += f" rows={count}"
        add(f"VAL3859_8_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add(
        "VAL3859_9_doc",
        "markdown checkpoint document exists",
        DOC_PATH.exists() and "The q-basic chain rule is" in read_text(DOC_PATH),
        rel(DOC_PATH),
    )
    formalization_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3859*", "P8_Y5_BRR545_3859*", "*Y5_R2FR_3859*", "3859-Y5-R2FR*"):
            formalization_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add(
        "VAL3859_10_formalization_clean",
        "formalization-workbench has no generated 3859 project files",
        len(formalization_hits) == 0,
        "; ".join(str(path) for path in formalization_hits) if formalization_hits else "no generated 3859 project file hits under formalization-workbench",
    )
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add(
        "VAL3859_11_pycache_removed",
        "scripts __pycache__ removed",
        len(pycache_hits) == 0,
        "; ".join(str(path) for path in pycache_hits) if pycache_hits else "no __pycache__ directories",
    )
    return rows


def main() -> int:
    timestamp = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows(timestamp)
    theorem = theorem_rows(timestamp)
    audit = audit_rows(timestamp)
    residual = residual_rows(timestamp)
    gates = gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["audit"], audit)
    write_csv(OUTPUTS["residual"], residual)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, theorem, audit, residual, gates, decisions, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, theorem, audit, residual, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_NONCLAIM_EXACT_QBASIC_TAU_H_CSTAR_THEOREM_CURRENTLY_BLOCKED")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3858"
BRANCH = "MTS_R2FR_Y5_MOTION_TIME_SPACE_VISIBLE_METRIC_BRIDGE_OR_SIGNATURE_NO_GO_3858"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3858-Y5-R2FR-motion-time-space-visible-metric-bridge-or-signature-no-go.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

CSV_3857_AUDIT = OUT / "P8_Y5_R2FR_3857_ACTION_PIECE_ADOPTION_AUDIT.csv"
CSV_3857_RESIDUAL = OUT / "P8_Y5_R2FR_3857_RESIDUAL_DECOMPOSITION_BOUND.csv"
CSV_3857_GATES = OUT / "P8_Y5_R2FR_3857_CLAIM_GATES.csv"
CSV_3857_VALIDATION = OUT / "P8_Y5_BRR545_3857_VALIDATION.csv"
CSV_3845_BRIDGE = OUT / "P8_Y5_R2FR_3845_METRIC_BRIDGE_CANDIDATE.csv"
CSV_3845_ACTION = OUT / "P8_Y5_R2FR_3845_VISIBLE_ACTION_CANDIDATE.csv"
CSV_3765_QOBS = OUT / "P8_Y5_R2FR_3765_QOBS_CANDIDATE_MAP.csv"
CSV_3765_VERDICT = OUT / "P8_Y5_R2FR_3765_PARENT_QOBS_VERDICT.csv"
CSV_3764_QOBS = OUT / "P8_Y5_R2FR_3764_PARENT_QUOTIENT_DESCENT_THEOREM.csv"
CSV_MTS_SYMBOL_MAP = OUT / "P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv"
CSV_FLOW_STATUS = OUT / "P8_local_GR_observed_flow_stationary_branch_status.csv"
CSV_ZERO_VARIATION = OUT / "P8_PARENT_LOCAL_ZERO_VARIATION_CHAIN.csv"
CSV_QCOH = OUT / "P8_QCOH_PROJECTOR_ALGEBRA_THEOREM.csv"
CSV_2504_LAPSE = OUT / "P8_Y5_NO_SHADOW_2504_V_LAPSE_READOUT_BRIDGE.csv"
CSV_2505_PPN = OUT / "P8_Y5_NO_SHADOW_2505_PPN_READOUT_VECTOR.csv"
CSV_1030_CONTRACT = OUT / "P8_Y5_R10_1030_PUBLIC_METRIC_ACTION_CONTRACT.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3858_SOURCE_REGISTER.csv",
    "theorem": OUT / "P8_Y5_R2FR_3858_MTS_METRIC_BRIDGE_THEOREM.csv",
    "audit": OUT / "P8_Y5_R2FR_3858_SIGNATURE_CONDITION_AUDIT.csv",
    "residual": OUT / "P8_Y5_R2FR_3858_METRIC_BRIDGE_RESIDUAL_BOUND.csv",
    "gates": OUT / "P8_Y5_R2FR_3858_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3858_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3858_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3858_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3858_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3858_00_3857_audit", CSV_3857_AUDIT, "B_qobs_signature+B_metric_bridge", "3857 first adoption residual"),
    ("SRC3858_01_3857_residual", CSV_3857_RESIDUAL, "B_action_adoption_3857", "action adoption bound"),
    ("SRC3858_02_3857_gates", CSV_3857_GATES, "PASS_3858_METRIC_BRIDGE_TARGET", "3858 target selection"),
    ("SRC3858_03_3857_validation", CSV_3857_VALIDATION, "PASS", "previous validation"),
    ("SRC3858_04_3845_bridge", CSV_3845_BRIDGE, "g_obs = h_space", "metric bridge schema"),
    ("SRC3858_05_3845_action", CSV_3845_ACTION, "S_candidate", "visible EH action target"),
    ("SRC3858_06_3765_qobs", CSV_3765_QOBS, "q_obs_candidate", "q_obs object/map"),
    ("SRC3858_07_3765_verdict", CSV_3765_VERDICT, "QOBS_CANDIDATE_CONSTRUCTED_BUT_NOT_PARENT_SIGNED", "q_obs verdict"),
    ("SRC3858_08_3764_qobs", CSV_3764_QOBS, "EXACT_CONDITIONAL_ZERO_THEOREM", "single-frame theorem"),
    ("SRC3858_09_symbol_map", CSV_MTS_SYMBOL_MAP, "u^mu / h_mu_nu / X", "MTS local symbol map"),
    ("SRC3858_10_flow_status", CSV_FLOW_STATUS, "conditional_same_stack_owner", "observed flow/coframe status"),
    ("SRC3858_11_zero_variation", CSV_ZERO_VARIATION, "u^mu u_mu=-1", "flow normalization variation"),
    ("SRC3858_12_qcoh", CSV_QCOH, "h_{mu nu}=g_{mu nu}+u_mu u_nu", "spatial projector algebra"),
    ("SRC3858_13_2504_lapse", CSV_2504_LAPSE, "v:=log(N_obs^2/c^2)", "lapse/coframe readout route"),
    ("SRC3858_14_2505_ppn", CSV_2505_PPN, "BETA_LAW_MATCHES_EH", "EH lapse beta readout"),
    ("SRC3858_15_1030_contract", CSV_1030_CONTRACT, "CONTRACT_READY_NOT_CURRENT_THEOREM", "public metric action contract"),
]

METRIC_FORMULA = "g_obs_ab = h_space_ab - c_*^2 tau_time_a tau_time_b"
INVERSE_FORMULA = "g_obs^ab = h_space^ab - c_*^-2 u^a u^b when tau_time(u)=1 and h_space_ab u^b=0"
BRIDGE_THEOREM = (
    "On a regular 4D local branch, if tau_time is a nonzero quotient-owned time one-form, "
    "u is a quotient-owned flow with tau_time(u)=1, h_space is rank-3 positive on ker(tau_time) and annihilates u, "
    "and c_*>0 is a quotient-owned conversion constant, then g_obs_ab=h_space_ab-c_*^2 tau_time_a tau_time_b is nondegenerate Lorentzian. "
    "In the adapted frame (u,e_i), g_obs has diagonal form (-c_*^2,h_ij), so its signature is (-,+,+,+)."
)
CURRENT_FAIL = (
    "current corpus has the bridge schema and conditional flow/coframe rows, but tau_time, h_space, c_*, q_obs signing, "
    "sector factorization, and non-LC connection silence are not all parent-owned"
)
BRIDGE_BOUND = (
    "B_metric_bridge_3858 <= "
    "B_tau_owner+B_h_owner+B_cstar_owner+B_Lorentz_signature+B_sector_factorization+"
    "B_nonLC_connection+B_units_orientation+B_preferred_frame_motion"
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
                "claim_use": "nonclaim_metric_bridge_derivation_test",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "theorem_id": "MBT3858_0_bridge_formula",
            "step": "metric construction",
            "statement": METRIC_FORMULA,
            "derivation": "combine one time covector, one spatial rank-3 metric, and one speed conversion constant",
            "current_result": "FORMULA_EXPLICIT",
            "status": "EXACT_CONSTRUCTION_FORMULA",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "MBT3858_1_signature_proof",
            "step": "Lorentzian signature theorem",
            "statement": BRIDGE_THEOREM,
            "derivation": "evaluate g_obs in an adapted frame and use positivity of h_space on ker(tau_time)",
            "current_result": "THEOREM_DERIVED_CONDITIONALLY",
            "status": "EXACT_CONDITIONAL_LORENTZIAN_BRIDGE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "MBT3858_2_inverse_connection",
            "step": "inverse and connection ownership",
            "statement": INVERSE_FORMULA + "; Gamma_obs is Levi-Civita[g_obs] only if C_nonLC=0 or source-bounded.",
            "derivation": "split tangent space into flow plus spatial rest space; then require non-LC silence for EH action adoption",
            "current_result": "INVERSE_CONDITIONAL_CONNECTION_RESIDUAL_RETAINED",
            "status": "CONDITIONAL_INVERSE_WITH_NONLC_GUARD",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "MBT3858_3_no_extra_motion_field",
            "step": "motion-field interpretation",
            "statement": "The motion field is harmless only when it is the normalized flow/readout direction of the same q_obs-owned tau_time,h_space,g_obs stack; otherwise it is a preferred-frame residual.",
            "derivation": "identify u as the time leg of the public coframe, not an independent force field",
            "current_result": "MOTION_AS_COFLOW_NOT_FORCE_IF_PARENT_OWNED",
            "status": "EXACT_GUARD_LEMMA",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "MBT3858_4_current_verdict",
            "step": "strict-current bridge test",
            "statement": CURRENT_FAIL,
            "derivation": "compare all bridge premises against 3845, 3765, 3538, 1030, and 3857 rows",
            "current_result": "METRIC_BRIDGE_NOT_CLAIMED_CURRENT_CORPUS",
            "status": "CONDITIONAL_BRIDGE_READY_PARENT_OWNERSHIP_BLOCKED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def audit_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "audit_id": "SCA3858_0_tau_owner",
            "condition": "tau_time nonzero and q_obs-owned",
            "mathematical_need": "tau_time in Omega^1(U), tau_time(u)=1, sector clocks use same tau_time",
            "current_evidence": "2504 lapse route and 3538 flow status are conditional; 3765 q_obs is not parent-signed",
            "passes_current_branch": False,
            "residual_owner": "B_tau_owner",
            "next_action": "prove tau_time descends through q_obs or retain clock/frame residual",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "SCA3858_1_h_owner",
            "condition": "h_space rank-3 positive spatial metric",
            "mathematical_need": "h_space positive on ker(tau_time), h_space_ab u^b=0",
            "current_evidence": "Qcoh/projector algebra uses h_mu_nu, but parent ownership and positivity/signature row are not signed",
            "passes_current_branch": False,
            "residual_owner": "B_h_owner+B_Lorentz_signature",
            "next_action": "derive h_space from MTS spatial/projector primitives with positivity and rank certificates",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "SCA3858_2_cstar_owner",
            "condition": "c_* positive quotient-owned conversion constant",
            "mathematical_need": "one c_* fixes time/space units before local PPN fitting",
            "current_evidence": "3845 names one observed c_*; no parent quotient/superselection proof in current bridge",
            "passes_current_branch": False,
            "residual_owner": "B_cstar_owner+B_units_orientation",
            "next_action": "derive c_* as quotient-owned/superselected or retain unit-calibration residual",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "SCA3858_3_sector_factorization",
            "condition": "matter, EM, clocks, photons, source, and orbital readouts use the same g_obs",
            "mathematical_need": "r_s=F_s o q_obs for all local sectors",
            "current_evidence": "3764 gives exact conditional theorem; 1030 contract is written not parent-signed",
            "passes_current_branch": False,
            "residual_owner": "B_sector_factorization",
            "next_action": "prove sector factorization or retain frame/source split residuals",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "SCA3858_4_connection",
            "condition": "Gamma_obs is Levi-Civita[g_obs] for local EH branch",
            "mathematical_need": "C_nonLC=0 or source-bounded before Lovelock/EH adoption",
            "current_evidence": "3845 keeps C_nonLC as retained residual",
            "passes_current_branch": False,
            "residual_owner": "B_nonLC_connection",
            "next_action": "derive torsion/nonmetricity silence or bounded non-LC residual",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "SCA3858_5_motion_preferred_frame",
            "condition": "motion flow is coframe/readout direction, not independent preferred-frame field",
            "mathematical_need": "u belongs to same q_obs/g_obs stack; no extra alpha_i vector survives",
            "current_evidence": "3538 says clean if inherited from same stack; current branch is not fully parent-signed",
            "passes_current_branch": False,
            "residual_owner": "B_preferred_frame_motion",
            "next_action": "prove u/tau/h same-stack ownership or retain alpha_i/preferred-frame residuals",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def residual_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "MRB3858_0_metric_bridge_bound",
            "observable": "B_metric_bridge_3858",
            "formula": BRIDGE_BOUND,
            "meaning": "residual preventing motion/time/space primitives from owning the public Lorentzian metric",
            "status": "NONCLAIM_BOUND_EXPLICIT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MRB3858_1_action_adoption_update",
            "observable": "B_action_adoption_3857",
            "formula": "B_action_adoption_3857 <= B_metric_bridge_3858+B_vertical_Lleak+B_operator_class+B_kappa_ownership+B_matter_descent+B_silent_variation+B_boundary_support+B_readout_gauge+B_RAB_beta_cross",
            "meaning": "3858 replaces the vague metric-bridge slot with a precise Lorentzian bridge residual vector",
            "status": "ACTION_ADOPTION_BOUND_REFINED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MRB3858_2_if_closed",
            "observable": "g_obs ownership",
            "formula": "if B_metric_bridge_3858=0 then g_obs=h_space-c_*^2 tau_time tau_time is parent-owned Lorentzian public geometry",
            "meaning": "closes the first visible EH action adoption residual",
            "status": "EXACT_CONDITIONAL_METRIC_WIN_PATH",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MRB3858_3_current_fail_vector",
            "observable": "strict-current metric bridge failure vector",
            "formula": "F_metric=(B_tau_owner,B_h_owner,B_cstar_owner,B_Lorentz_signature,B_sector_factorization,B_nonLC_connection,B_units_orientation,B_preferred_frame_motion)",
            "meaning": "parent ownership is the remaining issue, not the algebraic existence of a Lorentzian metric",
            "status": "FINITE_FAILURE_VECTOR",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "GATE3858_0_sources",
            "gate": "source-backed metric bridge inputs resolved",
            "status": "PASS_SOURCE_REGISTERED",
            "claim_allowed": False,
            "reason": "all metric bridge inputs are local source rows from 2504/2505/3538/3764/3765/3845/3857",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3858_1_signature",
            "gate": "Lorentzian signature theorem",
            "status": "PASS_EXACT_CONDITIONAL_SIGNATURE_THEOREM",
            "claim_allowed": False,
            "reason": "tau_time, h_space, and c_* imply a Lorentzian metric once their parent ownership and positivity clauses hold",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3858_2_current_bridge",
            "gate": "current corpus owns g_obs bridge",
            "status": "BLOCKED_METRIC_BRIDGE_NOT_PARENT_SIGNED",
            "claim_allowed": False,
            "reason": CURRENT_FAIL,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3858_3_no_motion_smuggle",
            "gate": "motion field not inserted as hidden preferred frame",
            "status": "PASS_GUARD_MOTION_IS_COFLOW_ONLY_IF_PARENT_OWNED",
            "claim_allowed": False,
            "reason": "independent motion flow remains B_preferred_frame_motion unless it is the q_obs coframe time direction",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3858_4_local_GR",
            "gate": "strict-current local-GR metric/action claim",
            "status": "BLOCKED_LOCAL_GR_CLAIM",
            "claim_allowed": False,
            "reason": "metric bridge, non-LC connection, action adoption, source, and readout guards remain active",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3858_5_next",
            "gate": "next target selected",
            "status": "PASS_3859_TAU_H_CSTAR_OWNERSHIP_TARGET",
            "claim_allowed": False,
            "reason": "the algebraic bridge is solved conditionally; next must prove tau_time/h_space/c_* are parent-owned or bound their frame residuals",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC3858_0",
            "decision": "the Lorentzian metric bridge is mathematically constructible from motion/time/space primitives",
            "consequence": "MTS does not need a separately inserted motion field if tau_time,h_space,c_* are parent-owned",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3858_1",
            "decision": "strict current bridge remains nonclaim",
            "consequence": "g_obs is not yet adopted because ownership/signature/sector-factorization clauses are unsigned",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3858_2",
            "decision": "target tau/h/c ownership next",
            "consequence": "3859 should prove tau_time,h_space,c_* are q_obs-basic/same-stack or write explicit residual rows",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3858_0",
            "next_checkpoint": "3859-Y5-R2FR-tau-h-cstar-parent-ownership-from-qobs-or-frame-residual-bound.md",
            "script": "scripts/Y5_R2FR_3859_tau_h_cstar_parent_ownership_from_qobs_or_frame_residual_bound.py",
            "objective": "prove tau_time, h_space, and c_* are q_obs-basic same-stack parent objects, or emit explicit frame/clock/preferred residual bounds",
            "reason": "3858 solves the algebraic Lorentzian bridge conditionally; the remaining hard proof is parent ownership of the bridge ingredients",
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "status": "PASS_NONCLAIM_EXACT_CONDITIONAL_METRIC_BRIDGE_PARENT_OWNERSHIP_BLOCKED",
            "claim": "no g_obs adoption, visible EH action adoption, beta, PPN, Newton, EM, or local-GR claim",
            "result": "exact Lorentzian bridge theorem derived from tau_time,h_space,c_*; current corpus blocked by parent ownership/signature/sector/connection clauses",
            "next": "3859 tau/h/cstar parent ownership from q_obs or frame residual bound",
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
    text = f"""# 3858 - Motion Time Space Visible Metric Bridge Or Signature No-Go

Private checkpoint. This attacks the first residual from 3857: can motion/time/space primitives actually build the visible metric, or are we inserting GR geometry by hand?

Generated: `{timestamp}`

## Result

The bridge formula is:

`{METRIC_FORMULA}`.

The exact conditional theorem is:

`{BRIDGE_THEOREM}`.

This is a genuine mathematical bridge. In an adapted frame, the metric matrix is `diag(-c_*^2,h_ij)`, so the signature is Lorentzian if `h_ij` is positive and `c_*>0`.

The current corpus still does not claim the bridge:

`{CURRENT_FAIL}`.

The finite bridge residual is:

`{BRIDGE_BOUND}`.

So the situation improves: the problem is not "how can time and space make a metric?" That algebra is now clean. The real proof target is whether `tau_time`, `h_space`, and `c_*` are parent-owned/q_obs-basic and used by all sectors without an independent preferred-frame motion field.

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## MTS Metric Bridge Theorem

{markdown_table(theorem, ["theorem_id", "step", "status", "current_result"])}

## Signature Condition Audit

{markdown_table(audit, ["audit_id", "condition", "passes_current_branch", "residual_owner", "next_action"])}

## Metric Bridge Residual Bound

{markdown_table(residual, ["row_id", "observable", "status", "formula"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "consequence"])}

## Bottom Line

3858 proves the algebraic motion/time/space to Lorentzian metric bridge conditionally. It does not yet prove MTS owns that bridge. The next target is to prove `tau_time`, `h_space`, and `c_*` are q_obs-basic same-stack parent objects, or keep explicit frame/clock/preferred-frame residuals.

Next target: `3859-Y5-R2FR-tau-h-cstar-parent-ownership-from-qobs-or-frame-residual-bound.md`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3857", "Current State After 3858", 1)
    text = "\n".join(
        line for line in text.splitlines() if not line.startswith("<!-- Generated by 3858 at ")
    )
    paragraph = (
        "`3858` attacks the first action-adoption residual, the motion/time/space to visible metric bridge. "
        "It proves the exact conditional Lorentzian construction: if `tau_time` is a nonzero q-owned time one-form, `u` is a q-owned flow with `tau_time(u)=1`, `h_space` is rank-3 positive on `ker(tau_time)` and annihilates `u`, and `c_*` is a positive q-owned conversion constant, then `g_obs_ab=h_space_ab-c_*^2 tau_time_a tau_time_b` is nondegenerate Lorentzian with signature `(-,+,+,+)`. "
        "This makes the bridge algebra clean while keeping the strict claim blocked: the corpus still has to prove ownership of `tau_time`, `h_space`, `c_*`, sector factorization, non-LC connection silence, and absence of an independent preferred-frame motion field. "
        "The next pressure point is parent ownership/q-basicness of the bridge ingredients.\n\n"
    )
    if paragraph not in text and "## Next Best Gate" in text:
        text = text.replace("## Next Best Gate", paragraph + "## Next Best Gate", 1)
    old_gate = """`3858-Y5-R2FR-motion-time-space-visible-metric-bridge-or-signature-no-go.md`

Target: derive or reject the MTS primitive bridge `M,T,S -> tau_time,h_space,c_* -> g_obs` with one quotient-owned Lorentzian public metric.

This is the best next move because 3857 shows the visible EH action cannot be MTS-owned until the metric bridge is parent-signed rather than inserted."""
    new_gate = """`3859-Y5-R2FR-tau-h-cstar-parent-ownership-from-qobs-or-frame-residual-bound.md`

Target: prove `tau_time`, `h_space`, and `c_*` are q_obs-basic same-stack parent objects, or emit explicit frame/clock/preferred residual bounds.

This is the best next move because 3858 solves the algebraic Lorentzian bridge conditionally; the remaining hard proof is parent ownership of its ingredients."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3858_MTS_METRIC_BRIDGE_THEOREM.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3858_SIGNATURE_CONDITION_AUDIT.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3858_METRIC_BRIDGE_RESIDUAL_BOUND.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3858_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3858_MTS_METRIC_BRIDGE_THEOREM.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    text = text.rstrip() + f"\n\n<!-- Generated by 3858 at {timestamp} -->\n"
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
        "VAL3858_0_sources",
        "all cited source paths exist and needles are found",
        all(row["exists"] and row["needle_found"] for row in sources),
        f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved",
    )
    add(
        "VAL3858_1_formula",
        "metric bridge formula is explicit",
        METRIC_FORMULA in all_text and "EXACT_CONSTRUCTION_FORMULA" in all_text,
        "g_obs formula present",
    )
    add(
        "VAL3858_2_signature_theorem",
        "Lorentzian signature theorem is explicit",
        "EXACT_CONDITIONAL_LORENTZIAN_BRIDGE" in all_text and "(-,+,+,+)" in all_text,
        "signature proof route present",
    )
    add(
        "VAL3858_3_current_block",
        "strict-current bridge remains blocked",
        "METRIC_BRIDGE_NOT_CLAIMED_CURRENT_CORPUS" in all_text and "BLOCKED_METRIC_BRIDGE_NOT_PARENT_SIGNED" in all_text,
        "bridge not promoted to claim",
    )
    add(
        "VAL3858_4_residual_vector",
        "metric bridge residual vector is explicit",
        "B_metric_bridge_3858" in all_text and "B_tau_owner" in all_text and "B_preferred_frame_motion" in all_text,
        "finite metric residual vector written",
    )
    add(
        "VAL3858_5_motion_guard",
        "motion field guard active",
        "MOTION_AS_COFLOW_NOT_FORCE_IF_PARENT_OWNED" in all_text and "PASS_GUARD_MOTION_IS_COFLOW_ONLY_IF_PARENT_OWNED" in all_text,
        "motion is not an independent preferred frame unless residualized",
    )
    add(
        "VAL3858_6_nonclaim",
        "all rows remain nonclaim",
        all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in theorem + audit + residual + gates),
        "valid_for_claim/claim_allowed false throughout",
    )
    add(
        "VAL3858_7_next",
        "next target is 3859 tau/h/c ownership",
        DOC_PATH.exists() and "3859-Y5-R2FR-tau-h-cstar-parent-ownership-from-qobs-or-frame-residual-bound" in read_text(DOC_PATH),
        "3859 tau/h/c ownership target visible",
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
        add(f"VAL3858_8_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add(
        "VAL3858_9_doc",
        "markdown checkpoint document exists",
        DOC_PATH.exists() and "The exact conditional theorem is" in read_text(DOC_PATH),
        rel(DOC_PATH),
    )
    formalization_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3858*", "P8_Y5_BRR545_3858*", "*Y5_R2FR_3858*", "3858-Y5-R2FR*"):
            formalization_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add(
        "VAL3858_10_formalization_clean",
        "formalization-workbench has no generated 3858 project files",
        len(formalization_hits) == 0,
        "; ".join(str(path) for path in formalization_hits) if formalization_hits else "no generated 3858 project file hits under formalization-workbench",
    )
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add(
        "VAL3858_11_pycache_removed",
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
    print(f"{CHECKPOINT} PASS_NONCLAIM_EXACT_CONDITIONAL_METRIC_BRIDGE_PARENT_OWNERSHIP_BLOCKED")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

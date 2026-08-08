from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3846"
BRANCH = "MTS_R2FR_Y5_MTS_TO_VISIBLE_METRIC_BRIDGE_3846"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3846-Y5-R2FR-MTS-to-visible-metric-bridge-or-action-candidate-reject.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_3845 = PCW / "3845-Y5-R2FR-visible-metric-parent-action-candidate-from-MTS-or-Lovelock-failure.md"
P_10_OBSERVER = PCW / "10-observer-map-symplectic-contract.md"
P_1030 = PCW / "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md"

CSV_3845_METRIC = OUT / "P8_Y5_R2FR_3845_METRIC_BRIDGE_CANDIDATE.csv"
CSV_3845_ACTION = OUT / "P8_Y5_R2FR_3845_VISIBLE_ACTION_CANDIDATE.csv"
CSV_3845_CLAUSE = OUT / "P8_Y5_R2FR_3845_LOVELOCK_CLAUSE_TEST.csv"
CSV_3845_EH2 = OUT / "P8_Y5_R2FR_3845_EH2_IMPLICATION_UPDATE.csv"
CSV_3845_VALIDATION = OUT / "P8_Y5_BRR545_3845_VALIDATION.csv"
CSV_943_COFRAME = OUT / "P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv"
CSV_863_COFRAME_ZERO = OUT / "P8_Y5_R10_863_COFRAME_ZERO_THEOREM.csv"
CSV_1031_TERMINAL = OUT / "P8_Y5_R10_1031_TERMINAL_PUBLIC_METRIC_PROOF_AUDIT.csv"
CSV_1045_MATTER = OUT / "P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3846_SOURCE_REGISTER.csv",
    "bridge_theorem": OUT / "P8_Y5_R2FR_3846_METRIC_BRIDGE_THEOREM.csv",
    "ownership": OUT / "P8_Y5_R2FR_3846_MTS_PRIMITIVE_OWNERSHIP_AUDIT.csv",
    "residuals": OUT / "P8_Y5_R2FR_3846_CONNECTION_READOUT_RESIDUALS.csv",
    "adoption": OUT / "P8_Y5_R2FR_3846_ACTION_ADOPTION_UPDATE.csv",
    "gates": OUT / "P8_Y5_R2FR_3846_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3846_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3846_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3846_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3846_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3846_0_3845_doc", P_3845, "required MTS-to-metric bridge"),
    ("SRC3846_1_3845_metric", CSV_3845_METRIC, "MB3845_0_metric_schema"),
    ("SRC3846_2_3845_action", CSV_3845_ACTION, "VAC3845_0_minimal_visible_EH_candidate"),
    ("SRC3846_3_3845_clause", CSV_3845_CLAUSE, "LCT3845_1_metric_bridge"),
    ("SRC3846_4_3845_eh2", CSV_3845_EH2, "B_metric_bridge=0"),
    ("SRC3846_5_3845_validation", CSV_3845_VALIDATION, "PASS"),
    ("SRC3846_6_observer_contract", P_10_OBSERVER, "theta_0 = T c dt"),
    ("SRC3846_7_943_coframe", CSV_943_COFRAME, "CFC943_1_observed_coframe_descent"),
    ("SRC3846_8_863_coframe_zero", CSV_863_COFRAME_ZERO, "CZT863_0_chain_rule_zero"),
    ("SRC3846_9_1031_terminal", CSV_1031_TERMINAL, "TPM1031_1_terminal_object"),
    ("SRC3846_10_1045_matter", CSV_1045_MATTER, "MFS1045_1_observed_coframe_functor"),
    ("SRC3846_11_1030_doc", P_1030, "single-public-metric parent action"),
]

METRIC_FORMULA = "g_obs_ab = h_ab - c_*^2 tau_a tau_b"
INVERSE_FORMULA = "g_obs^ab = h^ab - c_*^-2 u^a u^b"
BRIDGE_BOUND = (
    "B_metric_bridge <= B_tau_owner + B_h_owner + B_c_owner + B_signature "
    "+ B_coframe_descent + B_nonLC + B_motion_frame"
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
    rows = []
    for source_id, path, needle in SOURCE_SPECS:
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
                "role": "input_for_MTS_to_visible_metric_bridge",
                "claim_use": "nonclaim_bridge_theorem_and_ownership_audit_only",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def bridge_theorem_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "theorem_id": "MBT3846_0_data",
            "claim_piece": "metric-bridge data",
            "mathematical_statement": "Given a four-dimensional local arena with a nowhere-zero time one-form tau_a, observer vector u^a with tau_a u^a=1, spatial tensor h_ab with h_ab u^b=0 and positive rank-3 restriction on ker(tau), and c_*>0.",
            "derivation": "choose basis {u,e_i} with tau(e_i)=0; h_ab has block diag(0,h_ij) with h_ij positive definite",
            "result": "data are sufficient to test Lorentzian metric construction",
            "status": "EXACT_ALGEBRAIC_PREMISE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "MBT3846_1_metric",
            "claim_piece": "visible Lorentzian metric",
            "mathematical_statement": METRIC_FORMULA,
            "derivation": "in the adapted basis, g_obs has block diag(-c_*^2,h_ij)",
            "result": "g_obs is nondegenerate with signature (-,+,+,+)",
            "status": "EXACT_CONDITIONAL_LORENTZIAN_METRIC",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "MBT3846_2_inverse",
            "claim_piece": "inverse metric",
            "mathematical_statement": INVERSE_FORMULA + " with h^ac h_cb = delta^a_b - u^a tau_b and h^ab tau_b=0",
            "derivation": "multiply (h^ac-c_*^-2 u^a u^c)(h_cb-c_*^2 tau_c tau_b) and use projector identities",
            "result": "g_obs^ac g_obs_cb = delta^a_b",
            "status": "EXACT_CONDITIONAL_INVERSE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "MBT3846_3_coframe_special_case",
            "claim_piece": "observer coframe special case",
            "mathematical_statement": "theta^0 = c_* tau, h_ab = delta_ij theta^i_a theta^j_b gives g_obs = -theta^0 theta^0 + delta_ij theta^i theta^j",
            "derivation": "the old radial observer map theta_0=T c dt, theta_1=sqrt(S) dr is the 1+1/radial slice of the general coframe construction",
            "result": "the existing T,S observer-map intuition embeds into the visible metric bridge",
            "status": "EXACT_CONDITIONAL_COFRAME_EMBEDDING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "MBT3846_4_connection",
            "claim_piece": "connection ownership",
            "mathematical_statement": "Gamma_obs = Levi-Civita[g_obs] iff the observed connection is torsionless and metric-compatible with g_obs",
            "derivation": "fundamental theorem of pseudo-Riemannian geometry gives uniqueness of torsionless metric-compatible connection",
            "result": "non-Levi-Civita leakage is a named residual C_nonLC unless parent-signed zero",
            "status": "EXACT_CONDITIONAL_CONNECTION_LOCK",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "MBT3846_5_verdict",
            "claim_piece": "MTS-to-visible-metric bridge",
            "mathematical_statement": "M,T,S can own g_obs if and only if they parent-own tau_a, h_ab, u^a, c_*, coframe descent, and connection/readout locks on one branch",
            "derivation": "MBT3846_0 through MBT3846_4 provide the exact algebraic bridge; ownership clauses decide whether it is an MTS theorem",
            "result": "bridge theorem is proved conditionally but not adopted for current MTS",
            "status": "CONDITIONAL_BRIDGE_PROVED_CURRENT_OWNERSHIP_UNSIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def ownership_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "owner_id": "MBO3846_0_tau_time",
            "object": "tau_a",
            "required_owner": "time primitive T supplies a nowhere-zero clock one-form before fit/readout",
            "current_evidence": "10-observer map has theta_0=T c dt in radial setting",
            "current_status": "LOCAL_RADIAL_TEMPLATE_NOT_FULL_PARENT_OBJECT",
            "if_unsigned": "retain B_tau_owner",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "owner_id": "MBO3846_1_h_space",
            "object": "h_ab",
            "required_owner": "space primitive S supplies a rank-3 positive spatial metric on ker(tau)",
            "current_evidence": "10-observer map has theta_1=sqrt(S) dr as radial spatial leg",
            "current_status": "RADIAL_LEG_NOT_FULL_SPATIAL_TRIAD",
            "if_unsigned": "retain B_h_owner",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "owner_id": "MBO3846_2_c_star",
            "object": "c_*",
            "required_owner": "one observed conversion speed ties time and space units before local fitting",
            "current_evidence": "coframe notation uses c, but no parent constant/superselection proof is attached here",
            "current_status": "CONSTANT_OWNER_REQUIRED",
            "if_unsigned": "retain B_c_owner",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "owner_id": "MBO3846_3_signature",
            "object": "Lorentzian signature",
            "required_owner": "tau nonzero and h positive on ker(tau) hold on the local branch domain",
            "current_evidence": "3846 proves the algebraic signature result if the data are supplied",
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "if_unsigned": "retain B_signature",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "owner_id": "MBO3846_4_quotient_coframe",
            "object": "e_obs(q(Phi))",
            "required_owner": "observed coframe descends through q and is unique for ordinary observables",
            "current_evidence": "943/863/1031/1045 provide conditional contracts and counterexample guards",
            "current_status": "CONDITIONAL_CHAIN_RULE_NOT_PARENT_SIGNED",
            "if_unsigned": "retain B_coframe_descent",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "owner_id": "MBO3846_5_motion_frame",
            "object": "motion/readout congruence",
            "required_owner": "motion defines observer readout inside g_obs, not a second matter metric or shadow frame",
            "current_evidence": "1030/1045 keep no-shadow and matter functor clauses unsigned",
            "current_status": "READOUT_FRAME_LOCK_REQUIRED",
            "if_unsigned": "retain B_motion_frame",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "owner_id": "MBO3846_6_verdict",
            "object": "MTS metric bridge ownership",
            "required_owner": "MBO3846_0 through MBO3846_5 all pass on one parent branch",
            "current_evidence": "all pieces are now explicit, but no single source signs the full bridge",
            "current_status": "BRIDGE_NOT_ADOPTED_CURRENT_MTS",
            "if_unsigned": "visible action candidate remains a target, not the MTS action",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def residual_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "residual_id": "MBR3846_0_metric_bridge_total",
            "observable": "B_metric_bridge",
            "formula": BRIDGE_BOUND,
            "meaning": "finite residual if the MTS primitives fail to own a single public Lorentzian metric",
            "status": "CURRENT_NONCLAIM_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "residual_id": "MBR3846_1_nonLC",
            "observable": "B_nonLC",
            "formula": "B_nonLC <= ||Gamma_obs - LeviCivita[g_obs]||_local_ppn",
            "meaning": "torsion/nonmetricity/independent connection leakage into local PPN",
            "status": "RETAIN_UNTIL_CONNECTION_LOCK_SIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "residual_id": "MBR3846_2_motion_frame",
            "observable": "B_motion_frame",
            "formula": "B_motion_frame <= |delta g_matter/g_obs| + |A_g(Xhat)-1| + |B_g(Xhat)|",
            "meaning": "motion/readout becomes a physical shadow frame rather than observer congruence",
            "status": "RETAIN_UNTIL_NO_SHADOW_FRAME_SIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "residual_id": "MBR3846_3_action_adoption",
            "observable": "B_action_adoption",
            "formula": "B_action_adoption <= B_metric_bridge + B_action_descent + B_matter_source + B_silent_sector",
            "meaning": "visible EH action candidate cannot be adopted until bridge and action clauses close",
            "status": "ACTION_CANDIDATE_REMAINS_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def adoption_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "adoption_id": "AD3846_0_if_bridge_signed",
            "candidate": "3845 visible EH action candidate",
            "condition": "M,T,S parent-own tau_a,h_ab,u^a,c_* and observed coframe descent; Gamma_obs=LC[g_obs]; motion readout not shadow frame",
            "consequence": "metric bridge obstruction B_metric_bridge=0 and the action candidate may proceed to action-descent/source/silence tests",
            "current_status": "EXACT_CONDITIONAL_ADOPTION_STEP",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "adoption_id": "AD3846_1_current",
            "candidate": "3845 visible EH action candidate",
            "condition": "current corpus signs all 3846 bridge ownership rows",
            "consequence": "not satisfied; the action candidate remains unadopted",
            "current_status": "NOT_ADOPTED_BRIDGE_UNSIGNED",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "adoption_id": "AD3846_2_reject_condition",
            "candidate": "3845 visible EH action candidate",
            "condition": "MTS primitives cannot supply a unique Lorentzian g_obs without an independent frame/connection/source slot",
            "consequence": "reject Lovelock/EH visible-action route or retain it as explicit closure only",
            "current_status": "REJECTION_CONDITION_DEFINED_NOT_TRIGGERED",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "GATE3846_0_algebraic_bridge",
            "gate": "Lorentzian metric construction from tau/h/u/c",
            "status": "PASS_EXACT_CONDITIONAL_THEOREM",
            "claim_allowed": False,
            "reason": "g_obs has signature (-,+,+,+) if the MTS primitives supply the required clock/spatial data",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3846_1_MTS_ownership",
            "gate": "MTS owns tau,h,u,c as parent objects",
            "status": "BLOCKED_PARENT_OWNERSHIP_CERTIFICATES_REQUIRED",
            "claim_allowed": False,
            "reason": "radial T,S coframe exists, but full 4D tau/h/c ownership is not signed",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3846_2_connection_lock",
            "gate": "Gamma_obs is Levi-Civita of g_obs",
            "status": "BLOCKED_CONNECTION_LOCK_REQUIRED",
            "claim_allowed": False,
            "reason": "independent connection/torsion/nonmetricity leakage remains a named residual",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3846_3_no_shadow_motion_frame",
            "gate": "motion readout is not a second matter frame",
            "status": "BLOCKED_NO_SHADOW_FRAME_PARENT_SIGNATURE_REQUIRED",
            "claim_allowed": False,
            "reason": "ordinary matter/public coframe route is conditional but not parent-signed",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3846_4_action_adoption",
            "gate": "3845 visible action candidate can be adopted",
            "status": "BLOCKED_BRIDGE_UNSIGNED",
            "claim_allowed": False,
            "reason": "the bridge theorem is exact but not owned by current MTS",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3846_5_next_action",
            "gate": "next target is coframe completion",
            "status": "PASS_ACTIONABLE_NEXT",
            "claim_allowed": False,
            "reason": "3846 identifies the first missing owner: full 4D tau/h/c coframe completion from the radial T,S observer map",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC3846_0",
            "decision": "the metric bridge theorem is conditionally proved",
            "consequence": "the visible-action route is mathematically coherent if MTS owns the coframe data",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3846_1",
            "decision": "current MTS does not yet adopt the bridge",
            "consequence": "no EH action adoption, no local-GR claim, and no beta claim",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3846_2",
            "decision": "next work should derive the full 4D coframe from T,S/MTS primitives",
            "consequence": "3847 attacks the actual bridge owner rather than adding more beta ledgers",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3846_0",
            "next_checkpoint": "3847-Y5-R2FR-observer-coframe-completion-from-TS-or-metric-bridge-demotion.md",
            "script": "scripts/Y5_R2FR_3847_observer_coframe_completion_from_TS_or_metric_bridge_demotion.py",
            "objective": "derive a full 4D observed coframe/tau/h/c package from the existing T,S observer-map structure, or demote the metric bridge to closure-only",
            "reason": "3846 proves the algebraic metric theorem but shows the parent-owned coframe package is the first unsigned bridge component",
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "status": "PASS_NONCLAIM_CONDITIONAL_METRIC_BRIDGE_THEOREM",
            "claim": "no action adoption, EH2, beta, local-GR, Newton, or PPN claim",
            "next": "3847 observer coframe completion from T,S or metric bridge demotion",
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        vals = [str(row.get(col, "")).replace("\n", " ").replace("|", "\\|") for col in columns]
        body.append("| " + " | ".join(vals) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, object]],
    bridge_theorem: list[dict[str, object]],
    ownership: list[dict[str, object]],
    residuals: list[dict[str, object]],
    adoption: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    timestamp: str,
) -> None:
    text = f"""# 3846 - MTS to Visible Metric Bridge Or Action Candidate Reject

Private checkpoint. This attempts the bridge demanded by 3845: can motion/time/space produce one public Lorentzian metric `g_obs` strongly enough for the visible EH action candidate? It does not adopt the action or claim local GR.

Generated: `{timestamp}`

## Result

The algebraic bridge works conditionally:

`{METRIC_FORMULA}`

with inverse

`{INVERSE_FORMULA}`.

If `tau_a u^a=1`, `h_ab u^b=0`, `h_ab` is positive rank-3 on `ker(tau)`, and `c_*>0`, then in the adapted basis `{{u,e_i}}` the metric has block form `diag(-c_*^2,h_ij)` and is Lorentzian.

This is the good news: the motion/time/space-to-metric route is mathematically coherent. The bad news, honestly stated, is that current MTS has not yet parent-signed the full 4D `tau,h,u,c_*` package, connection lock, or no-shadow motion/readout frame. So the bridge is conditionally derived but not adopted.

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## Metric Bridge Theorem

{markdown_table(bridge_theorem, ["theorem_id", "claim_piece", "status", "result"])}

## MTS Primitive Ownership Audit

{markdown_table(ownership, ["owner_id", "object", "current_status", "if_unsigned"])}

## Residuals

{markdown_table(residuals, ["residual_id", "observable", "formula", "status"])}

## Action Adoption Update

{markdown_table(adoption, ["adoption_id", "candidate", "current_status", "consequence"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "consequence"])}

## Bottom Line

This is progress, not a pass. We now have the exact bridge theorem MTS needs: own `tau_a`, `h_ab`, `u^a`, and `c_*`, then `g_obs` follows. The next derivation should not wander: it should try to complete the old `T,S` observer coframe into a full 4D public coframe/metric package, or demote the visible-action route to closure-only.

Next target: `3847-Y5-R2FR-observer-coframe-completion-from-TS-or-metric-bridge-demotion.md`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3845", "Current State After 3846", 1)
    text = "\n".join(
        line for line in text.splitlines() if not line.startswith("<!-- Generated by 3846 at ")
    )
    paragraph = (
        "`3846` proves the MTS-to-visible-metric bridge as an exact conditional algebraic theorem: "
        "given a nowhere-zero time one-form `tau_a`, observer vector `u^a` with `tau_a u^a=1`, positive rank-3 spatial tensor `h_ab` on `ker(tau)`, and `c_*>0`, "
        "`g_obs_ab=h_ab-c_*^2 tau_a tau_b` has Lorentzian signature with inverse `g_obs^ab=h^ab-c_*^-2 u^a u^b`. "
        "This means the motion/time/space route to a public metric is mathematically coherent, but it is not yet adopted because current MTS has not parent-signed the full `tau,h,u,c_*` package, the Levi-Civita connection lock, or the no-shadow motion/readout frame. "
        "The bridge residual is now `B_metric_bridge <= B_tau_owner+B_h_owner+B_c_owner+B_signature+B_coframe_descent+B_nonLC+B_motion_frame`. "
        "Next target: complete the old `T,S` observer coframe into a full 4D coframe package or demote the metric bridge.\n\n"
    )
    anchor = "`3845` makes"
    if paragraph not in text and anchor in text:
        text = text.replace(anchor, paragraph + anchor, 1)
    old_gate = """`3846-Y5-R2FR-MTS-to-visible-metric-bridge-or-action-candidate-reject.md`

Target: derive or reject the bridge from motion/time/space primitives to one public Lorentzian metric `g_obs`.

This is the best next move because 3845 writes the action candidate and shows the metric bridge is the first adoption bottleneck."""
    new_gate = """`3847-Y5-R2FR-observer-coframe-completion-from-TS-or-metric-bridge-demotion.md`

Target: derive a full 4D observed coframe/tau/h/c package from the existing `T,S` observer-map structure, or demote the metric bridge to closure-only.

This is the best next move because 3846 proves the algebraic metric bridge and identifies coframe ownership as the first unsigned component."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3846_METRIC_BRIDGE_THEOREM.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3846_MTS_PRIMITIVE_OWNERSHIP_AUDIT.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3846_CONNECTION_READOUT_RESIDUALS.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3846_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3846_METRIC_BRIDGE_THEOREM.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    text = text.rstrip() + f"\n\n<!-- Generated by 3846 at {timestamp} -->\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    bridge_theorem: list[dict[str, object]],
    ownership: list[dict[str, object]],
    residuals: list[dict[str, object]],
    adoption: list[dict[str, object]],
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

    all_text = " ".join(str(row) for row in bridge_theorem + ownership + residuals + adoption + gates)
    add(
        "VAL3846_0_sources",
        "all cited local source paths exist and needles are found",
        all(row["exists"] and row["needle_found"] for row in sources),
        f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved",
    )
    add(
        "VAL3846_1_metric_formula",
        "metric and inverse formulas are present",
        METRIC_FORMULA in all_text and INVERSE_FORMULA in all_text,
        "g_obs and inverse formulas present",
    )
    add(
        "VAL3846_2_signature_proof",
        "Lorentzian signature proof is recorded",
        "block diag(-c_*^2,h_ij)" in all_text and "(-,+,+,+)" in all_text,
        "adapted-basis signature proof present",
    )
    add(
        "VAL3846_3_radial_embedding",
        "old T,S coframe is linked to bridge",
        "theta_0=T c dt" in all_text and "theta_1=sqrt(S) dr" in all_text,
        "radial observer coframe embedded in general theorem",
    )
    add(
        "VAL3846_4_bridge_bound",
        "metric bridge residual bound is present",
        BRIDGE_BOUND in all_text,
        "B_metric_bridge decomposition present",
    )
    add(
        "VAL3846_5_not_adopted",
        "visible action remains unadopted",
        "NOT_ADOPTED_BRIDGE_UNSIGNED" in all_text and "BLOCKED_BRIDGE_UNSIGNED" in all_text,
        "adoption/gate rows block claim",
    )
    add(
        "VAL3846_6_nonclaim",
        "all 3846 rows remain nonclaim",
        all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in bridge_theorem + ownership + residuals + adoption + gates),
        "valid_for_claim/claim_allowed false throughout",
    )
    add(
        "VAL3846_7_next_coframe",
        "next target attacks coframe completion",
        DOC_PATH.exists() and "3847-Y5-R2FR-observer-coframe-completion-from-TS-or-metric-bridge-demotion" in read_text(DOC_PATH),
        "3847 coframe target visible",
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
        add(f"VAL3846_8_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add(
        "VAL3846_9_doc",
        "markdown checkpoint document exists",
        DOC_PATH.exists() and "algebraic bridge works conditionally" in read_text(DOC_PATH),
        rel(DOC_PATH),
    )
    fwb_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3846*", "P8_Y5_BRR545_3846*", "*Y5_R2FR_3846*", "3846-Y5-R2FR*"):
            fwb_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add(
        "VAL3846_10_formalization_clean",
        "formalization-workbench has no generated 3846 project files",
        len(fwb_hits) == 0,
        "; ".join(str(path) for path in fwb_hits) if fwb_hits else "no generated 3846 project file hits under formalization-workbench",
    )
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add(
        "VAL3846_11_pycache_removed",
        "scripts __pycache__ removed",
        len(pycache_hits) == 0,
        "; ".join(str(path) for path in pycache_hits) if pycache_hits else "no __pycache__ directories",
    )
    return rows


def main() -> int:
    timestamp = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows(timestamp)
    bridge_theorem = bridge_theorem_rows(timestamp)
    ownership = ownership_rows(timestamp)
    residuals = residual_rows(timestamp)
    adoption = adoption_rows(timestamp)
    gates = gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["bridge_theorem"], bridge_theorem)
    write_csv(OUTPUTS["ownership"], ownership)
    write_csv(OUTPUTS["residuals"], residuals)
    write_csv(OUTPUTS["adoption"], adoption)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, bridge_theorem, ownership, residuals, adoption, gates, decisions, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, bridge_theorem, ownership, residuals, adoption, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_NONCLAIM_CONDITIONAL_METRIC_BRIDGE_THEOREM")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

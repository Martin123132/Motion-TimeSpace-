from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3845"
BRANCH = "MTS_R2FR_Y5_VISIBLE_METRIC_PARENT_ACTION_CANDIDATE_3845"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3845-Y5-R2FR-visible-metric-parent-action-candidate-from-MTS-or-Lovelock-failure.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_3844 = PCW / "3844-Y5-R2FR-parent-action-second-variation-EH2-vertex-proof-or-source-bound.md"
P_1030 = PCW / "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md"
P_1008 = PCW / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md"

CSV_3844_ROUTE = OUT / "P8_Y5_R2FR_3844_LOVELOCK_EH2_ROUTE.csv"
CSV_3844_CLAUSES = OUT / "P8_Y5_R2FR_3844_PARENT_CLAUSE_AUDIT.csv"
CSV_3844_UPDATE = OUT / "P8_Y5_R2FR_3844_EH2_BOUND_UPDATE.csv"
CSV_3844_VALIDATION = OUT / "P8_Y5_BRR545_3844_VALIDATION.csv"
CSV_1030_PUBLIC = OUT / "P8_Y5_R10_1030_PUBLIC_METRIC_ACTION_CONTRACT.csv"
CSV_637_PARENT = OUT / "P8_Y5_R10_637_PARENT_ACTION_DERIVATION_ATTEMPT.csv"
CSV_1008_PARENT = OUT / "P8_Y5_R10_1008_PARENT_VARIATION_AUDIT.csv"
CSV_3818_POISSON = OUT / "P8_Y5_R2FR_3818_WEAK_FIELD_POISSON_DERIVATION.csv"
CSV_3828_ZERO = OUT / "P8_Y5_R2FR_3828_ZERO_CONDITION_THEOREM.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3845_SOURCE_REGISTER.csv",
    "metric_bridge": OUT / "P8_Y5_R2FR_3845_METRIC_BRIDGE_CANDIDATE.csv",
    "action_candidate": OUT / "P8_Y5_R2FR_3845_VISIBLE_ACTION_CANDIDATE.csv",
    "clause_test": OUT / "P8_Y5_R2FR_3845_LOVELOCK_CLAUSE_TEST.csv",
    "eh2_implication": OUT / "P8_Y5_R2FR_3845_EH2_IMPLICATION_UPDATE.csv",
    "gates": OUT / "P8_Y5_R2FR_3845_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3845_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3845_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3845_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3845_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3845_0_3844_doc", P_3844, "Lovelock/EH uniqueness lock"),
    ("SRC3845_1_3844_route", CSV_3844_ROUTE, "LV3844_3_eh2_zero_if_clauses_pass"),
    ("SRC3845_2_3844_clauses", CSV_3844_CLAUSES, "LVC3844_2_local_second_order"),
    ("SRC3845_3_3844_update", CSV_3844_UPDATE, "EH2U3844_1_if_clauses_pass"),
    ("SRC3845_4_3844_validation", CSV_3844_VALIDATION, "PASS"),
    ("SRC3845_5_1030_doc", P_1030, "single-public-metric parent action"),
    ("SRC3845_6_1030_public", CSV_1030_PUBLIC, "SPM1030_0_public_metric_object"),
    ("SRC3845_7_637_parent", CSV_637_PARENT, "PA637_3_action_descent"),
    ("SRC3845_8_1008_doc", P_1008, "missing_explicit_current_chain"),
    ("SRC3845_9_1008_parent", CSV_1008_PARENT, "PVA1008_0_parent_action"),
    ("SRC3845_10_3818_poisson", CSV_3818_POISSON, "POI3818_0_linearized_00"),
    ("SRC3845_11_3828_beta_lock", CSV_3828_ZERO, "ZPPN3828_2_beta_lock"),
]

ACTION_FORMULA = (
    "S_candidate = (1/(2*kappa_MTS))*int sqrt(-g_obs(q(Phi)))"
    "*(R[g_obs]-2*Lambda_eff) + S_matter[Psi,g_obs(q(Phi)),theta(q)] "
    "+ S_GHY[g_obs] + S_silent[Phi_perp;q]"
)

METRIC_FORMULA = "g_obs = h_space(M,T,S) - c_*^2 tau_time(M,T,S) otimes tau_time(M,T,S)"


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
                "role": "input_for_visible_metric_parent_action_candidate",
                "claim_use": "nonclaim_candidate_and_adoption_gate_only",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def metric_bridge_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "bridge_id": "MB3845_0_metric_schema",
            "object": "g_obs",
            "candidate_formula": METRIC_FORMULA,
            "required_conditions": "tau_time nonzero; h_space rank-3 positive on ker(tau); Lorentzian nondegenerate signature; one observed c_* before fitting",
            "current_status": "SCHEMA_WRITTEN_NOT_PARENT_DERIVED",
            "would_close": "turns motion/time/space primitives into the public metric object needed by 3844",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bridge_id": "MB3845_1_connection",
            "object": "Gamma_obs",
            "candidate_formula": "Gamma_obs = Levi-Civita[g_obs] + C_nonLC",
            "required_conditions": "C_nonLC=0 or source-bounded before local PPN extraction",
            "current_status": "NONLC_RESIDUAL_RETAINED",
            "would_close": "blocks torsion/nonmetricity from masquerading as EH2 beta shift",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bridge_id": "MB3845_2_motion_readout",
            "object": "motion field / flow",
            "candidate_formula": "motion data defines observer congruence/readout on g_obs, not an independent matter frame",
            "required_conditions": "motion readout is quotient-owned and cannot introduce A_g(Xhat), B_g(Xhat), or arena-specific clocks",
            "current_status": "READOUT_NATURALITY_REQUIRED",
            "would_close": "keeps the action from becoming multi-frame after metric construction",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bridge_id": "MB3845_3_verdict",
            "object": "MTS-to-visible-metric bridge",
            "candidate_formula": "M,T,S -> (tau_time,h_space,c_*) -> g_obs",
            "required_conditions": "all MB3845_0 through MB3845_2 parent-signed on one branch",
            "current_status": "BRIDGE_NOT_CLAIMED_NEXT_TARGET",
            "would_close": "would let the visible action candidate be tested as MTS rather than imported GR notation",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def action_candidate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "candidate_id": "VAC3845_0_minimal_visible_EH_candidate",
            "candidate_name": "minimal visible MTS parent action candidate",
            "action_formula": ACTION_FORMULA,
            "variation_result_if_adopted": "G_mu_nu[g_obs]+Lambda_eff*g_mu_nu = kappa_MTS*T_mu_nu + R_silent_mu_nu",
            "second_variation_result_if_adopted": "if R_silent_mu_nu=0 and g_obs is parent-owned, delta^2 S_candidate|vis = delta^2 S_EH",
            "current_status": "CANDIDATE_WRITTEN_NOT_ADOPTED",
            "not_a_claim_because": "g_obs(M,T,S), kappa_MTS, matter functor domain, and S_silent silence are not parent-derived in current corpus",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "candidate_id": "VAC3845_1_silent_sector_rule",
            "candidate_name": "silent representative sector",
            "action_formula": "S_silent[Phi_perp;q] is allowed only if delta S_silent/delta g_obs=0 and D_v S_silent=0 on the local branch",
            "variation_result_if_adopted": "R_silent_mu_nu=0",
            "second_variation_result_if_adopted": "no hidden beta-order operator enters the visible EH2 vertex",
            "current_status": "SILENCE_CERTIFICATE_REQUIRED",
            "not_a_claim_because": "637/1008 do not yet supply the full parent action descent and boundary-domain silence",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "candidate_id": "VAC3845_2_no_smuggle_guard",
            "candidate_name": "not-GR-by-copying guard",
            "action_formula": "the candidate may be used only as an adoption target until MTS primitives derive g_obs and all retained sectors",
            "variation_result_if_adopted": "formal EH algebra is not enough for MTS ownership",
            "second_variation_result_if_adopted": "EH2 zero cannot be claimed from copied action notation alone",
            "current_status": "GUARD_ACTIVE",
            "not_a_claim_because": "candidate needs MTS-to-metric bridge and parent ownership before it becomes the theory action",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def clause_test_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "test_id": "LCT3845_0_formal_lovelock_shape",
            "clause": "candidate action has EH visible operator",
            "test_result": "PASS_IF_CANDIDATE_ADOPTED",
            "current_mts_status": "FORMAL_SHAPE_ONLY",
            "remaining_gap": "derive candidate from MTS primitives, not from GR preference",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "test_id": "LCT3845_1_metric_bridge",
            "clause": "M,T,S parent-derive one public metric g_obs",
            "test_result": "FAIL_CURRENT_CLAIM",
            "current_mts_status": "MB3845 schema exists but is not parent-signed",
            "remaining_gap": "prove tau_time, h_space, c_*, and nondegenerate Lorentzian metric from MTS",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "test_id": "LCT3845_2_action_descent",
            "clause": "S_parent descends to S_candidate plus silent sectors",
            "test_result": "FAIL_CURRENT_CLAIM",
            "current_mts_status": "637 action descent is conditional and 1008 says parent current-chain action is missing",
            "remaining_gap": "supply explicit parent Lagrangian/current chain or reject adoption",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "test_id": "LCT3845_3_matter_source",
            "clause": "matter couples only to g_obs with Hilbert source",
            "test_result": "FAIL_CURRENT_CLAIM",
            "current_mts_status": "1030 public-metric action contract is written but not parent-signed",
            "remaining_gap": "derive no shadow frame/no source-only weight/no marker constant clause",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "test_id": "LCT3845_4_silent_extra_sectors",
            "clause": "extra/projector/boundary sectors do not vary into visible beta vertex",
            "test_result": "FAIL_CURRENT_CLAIM",
            "current_mts_status": "silence certificates not supplied",
            "remaining_gap": "prove R_silent_mu_nu=0 or retain explicit EH2 residual",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "test_id": "LCT3845_5_newtonian_kappa",
            "clause": "kappa_MTS fixes G_ref before beta",
            "test_result": "CONDITIONAL_FROM_3818",
            "current_mts_status": "first-order Poisson bridge exists but source normalization guards remain",
            "remaining_gap": "same-source measure and no fitted GM smuggling",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "test_id": "LCT3845_6_verdict",
            "clause": "candidate can be adopted as current MTS parent action",
            "test_result": "NOT_ADOPTED_CURRENTLY",
            "current_mts_status": "constructive target written; adoption fails until bridge/action/source/silence clauses close",
            "remaining_gap": "3846 must derive or reject MTS-to-visible-metric bridge",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def eh2_implication_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "EHI3845_0_candidate_success",
            "observable": "B_EH2_vertex",
            "formula": "if VAC3845_0 is parent-adopted and LCT3845_1..5 pass, then B_EH2_vertex <= B_field_redef_gauge",
            "status": "EXACT_CONDITIONAL_EH2_COLLAPSE",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EHI3845_1_current_bound",
            "observable": "B_EH2_vertex",
            "formula": "B_EH2_vertex <= B_metric_bridge + B_action_descent + B_matter_source + B_silent_sector + B_kappa_source + B_field_redef_gauge",
            "status": "CURRENT_NONCLAIM_ADOPTION_FAILURE_BOUND",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EHI3845_2_bridge_focus",
            "observable": "B_metric_bridge",
            "formula": "B_metric_bridge=0 requires M,T,S -> tau_time,h_space,c_* -> g_obs to be parent-signed and unique",
            "status": "NEXT_PROOF_TARGET",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "GATE3845_0_candidate_written",
            "gate": "minimal visible action candidate exists",
            "status": "PASS_CANDIDATE_WRITTEN",
            "claim_allowed": False,
            "reason": "the action target is explicit instead of a vague missing parent action",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3845_1_metric_bridge",
            "gate": "MTS primitives derive g_obs",
            "status": "BLOCKED_MTS_TO_VISIBLE_METRIC_BRIDGE_NOT_PROVED",
            "claim_allowed": False,
            "reason": "tau_time, h_space, c_*, and Lorentzian nondegeneracy are schema-level only",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3845_2_action_adoption",
            "gate": "candidate is adopted as MTS parent action",
            "status": "BLOCKED_PARENT_DERIVATION_NOT_SIGNED",
            "claim_allowed": False,
            "reason": "current corpus has conditional descent contracts but not a signed current-chain Lagrangian",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3845_3_no_smuggle",
            "gate": "candidate is not used as copied-GR proof",
            "status": "PASS_GUARD",
            "claim_allowed": False,
            "reason": "all adoption rows remain nonclaim until MTS owns the bridge/action/source clauses",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3845_4_next_action",
            "gate": "next target attacks MTS-to-metric bridge",
            "status": "PASS_ACTIONABLE_NEXT",
            "claim_allowed": False,
            "reason": "the first adoption failure is the metric bridge from motion/time/space to g_obs",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC3845_0",
            "decision": "write the minimal visible action candidate but do not adopt it",
            "consequence": "we now know exactly what MTS must derive to reduce to GR locally",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3845_1",
            "decision": "the bridge from motion/time/space to one public Lorentzian metric is the next bottleneck",
            "consequence": "3846 should try to derive g_obs from MTS primitives before any more beta bookkeeping",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3845_2",
            "decision": "EH action shape is a target, not an imported proof",
            "consequence": "no local-GR claim until MTS owns the bridge, source, and silence clauses",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3845_0",
            "next_checkpoint": "3846-Y5-R2FR-MTS-to-visible-metric-bridge-or-action-candidate-reject.md",
            "script": "scripts/Y5_R2FR_3846_MTS_to_visible_metric_bridge_or_action_candidate_reject.py",
            "objective": "derive or reject the bridge M,T,S -> tau_time,h_space,c_* -> g_obs needed for the 3845 visible action candidate",
            "reason": "without the public Lorentzian metric bridge, the EH action candidate is just copied GR notation rather than MTS derivation",
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "status": "PASS_NONCLAIM_VISIBLE_ACTION_CANDIDATE_WRITTEN",
            "claim": "no action adoption, EH2, beta, local-GR, or PPN claim",
            "next": "3846 MTS-to-visible-metric bridge or action-candidate reject",
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
    metric_bridge: list[dict[str, object]],
    action_candidate: list[dict[str, object]],
    clause_test: list[dict[str, object]],
    eh2_implication: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    timestamp: str,
) -> None:
    text = f"""# 3845 - Visible Metric Parent Action Candidate From MTS Or Lovelock Failure

Private checkpoint. This tries the constructive route forced by 3844: write the minimal visible parent action candidate and test whether MTS currently owns it. It does not adopt the action or claim local GR.

Generated: `{timestamp}`

## Result

The minimal candidate is:

`{ACTION_FORMULA}`.

The required MTS-to-metric bridge is:

`{METRIC_FORMULA}`.

If MTS derives that bridge, the matter/source domain, and silent extra sectors, then the 3844 Lovelock route can collapse EH2. Current MTS does not yet own those clauses, so the candidate is a target, not a claim.

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## Metric Bridge Candidate

{markdown_table(metric_bridge, ["bridge_id", "object", "candidate_formula", "current_status", "would_close"])}

## Visible Action Candidate

{markdown_table(action_candidate, ["candidate_id", "candidate_name", "current_status", "not_a_claim_because"])}

## Lovelock Clause Test

{markdown_table(clause_test, ["test_id", "clause", "test_result", "current_mts_status", "remaining_gap"])}

## EH2 Implication

{markdown_table(eh2_implication, ["row_id", "observable", "formula", "status"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "consequence"])}

## Bottom Line

This is the cleanest leap forward so far on the GR-reduction branch: the action target is now explicit. The project has not proven it, but the next bottleneck is no longer vague. It is the bridge from motion/time/space primitives to one public Lorentzian metric `g_obs`. If that bridge closes, the EH/local-GR route becomes serious. If it fails, the visible-action route should be rejected cleanly.

Next target: `3846-Y5-R2FR-MTS-to-visible-metric-bridge-or-action-candidate-reject.md`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3844", "Current State After 3845", 1)
    text = "\n".join(
        line for line in text.splitlines() if not line.startswith("<!-- Generated by 3845 at ")
    )
    paragraph = (
        "`3845` makes the Lovelock/EH route constructive by writing the minimal visible parent action candidate: "
        "`S_candidate=(1/(2*kappa_MTS))*int sqrt(-g_obs)(R[g_obs]-2*Lambda_eff)+S_matter[Psi,g_obs,theta(q)]+S_GHY+S_silent`. "
        "The bridge target is `g_obs=h_space(M,T,S)-c_*^2 tau_time(M,T,S)otimes tau_time(M,T,S)`. "
        "This is not adopted as the MTS action because the metric bridge, parent action descent, public matter functor, source normalization, and silent-sector certificates are not parent-signed. "
        "The next proof bottleneck is therefore specific and constructive: derive or reject the motion/time/space-to-visible-metric bridge.\n\n"
    )
    anchor = "`3844` attacks"
    if paragraph not in text and anchor in text:
        text = text.replace(anchor, paragraph + anchor, 1)
    old_gate = """`3845-Y5-R2FR-visible-metric-parent-action-candidate-from-MTS-or-Lovelock-failure.md`

Target: construct the minimal visible parent action candidate from MTS motion/time/space objects and test every Lovelock/EH2 clause.

This is the best next move because 3844 turns EH2 into a constructive parent-action problem rather than another missing-row sweep."""
    new_gate = """`3846-Y5-R2FR-MTS-to-visible-metric-bridge-or-action-candidate-reject.md`

Target: derive or reject the bridge from motion/time/space primitives to one public Lorentzian metric `g_obs`.

This is the best next move because 3845 writes the action candidate and shows the metric bridge is the first adoption bottleneck."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3845_METRIC_BRIDGE_CANDIDATE.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3845_VISIBLE_ACTION_CANDIDATE.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3845_LOVELOCK_CLAUSE_TEST.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3845_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3845_METRIC_BRIDGE_CANDIDATE.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    text = text.rstrip() + f"\n\n<!-- Generated by 3845 at {timestamp} -->\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    metric_bridge: list[dict[str, object]],
    action_candidate: list[dict[str, object]],
    clause_test: list[dict[str, object]],
    eh2_implication: list[dict[str, object]],
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

    all_text = " ".join(str(row) for row in metric_bridge + action_candidate + clause_test + eh2_implication + gates)
    add(
        "VAL3845_0_sources",
        "all cited local source paths exist and needles are found",
        all(row["exists"] and row["needle_found"] for row in sources),
        f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved",
    )
    add(
        "VAL3845_1_action_candidate",
        "visible action candidate is explicit",
        ACTION_FORMULA in all_text,
        "action formula present",
    )
    add(
        "VAL3845_2_metric_bridge",
        "MTS-to-visible-metric bridge schema is explicit",
        METRIC_FORMULA in all_text and "M,T,S -> tau_time,h_space,c_* -> g_obs" in all_text,
        "metric bridge formula present",
    )
    add(
        "VAL3845_3_not_adopted",
        "candidate is not adopted as a claim",
        "CANDIDATE_WRITTEN_NOT_ADOPTED" in all_text and "NOT_ADOPTED_CURRENTLY" in all_text,
        "candidate/adoption gates block claim",
    )
    add(
        "VAL3845_4_eh2_implication",
        "EH2 conditional implication is present",
        "B_EH2_vertex <= B_field_redef_gauge" in all_text and "B_metric_bridge" in all_text,
        "EH2 implication rows present",
    )
    add(
        "VAL3845_5_nonclaim",
        "all 3845 rows remain nonclaim",
        all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in metric_bridge + action_candidate + clause_test + eh2_implication + gates),
        "valid_for_claim/claim_allowed false throughout",
    )
    add(
        "VAL3845_6_next_bridge",
        "next target attacks metric bridge",
        "3846-Y5-R2FR-MTS-to-visible-metric-bridge-or-action-candidate-reject" in read_text(DOC_PATH),
        "3846 bridge target visible",
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
        add(f"VAL3845_7_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add(
        "VAL3845_8_doc",
        "markdown checkpoint document exists",
        DOC_PATH.exists() and "minimal visible parent action candidate" in read_text(DOC_PATH),
        rel(DOC_PATH),
    )
    fwb_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3845*", "P8_Y5_BRR545_3845*", "*Y5_R2FR_3845*", "3845-Y5-R2FR*"):
            fwb_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add(
        "VAL3845_9_formalization_clean",
        "formalization-workbench has no 3845 files",
        len(fwb_hits) == 0,
        "; ".join(str(path) for path in fwb_hits) if fwb_hits else "no 3845 file hits under formalization-workbench",
    )
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add(
        "VAL3845_10_pycache_removed",
        "scripts __pycache__ removed",
        len(pycache_hits) == 0,
        "; ".join(str(path) for path in pycache_hits) if pycache_hits else "no __pycache__ directories",
    )
    return rows


def main() -> int:
    timestamp = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows(timestamp)
    metric_bridge = metric_bridge_rows(timestamp)
    action_candidate = action_candidate_rows(timestamp)
    clause_test = clause_test_rows(timestamp)
    eh2_implication = eh2_implication_rows(timestamp)
    gates = gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["metric_bridge"], metric_bridge)
    write_csv(OUTPUTS["action_candidate"], action_candidate)
    write_csv(OUTPUTS["clause_test"], clause_test)
    write_csv(OUTPUTS["eh2_implication"], eh2_implication)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, metric_bridge, action_candidate, clause_test, eh2_implication, gates, decisions, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, metric_bridge, action_candidate, clause_test, eh2_implication, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_NONCLAIM_VISIBLE_ACTION_CANDIDATE_WRITTEN")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

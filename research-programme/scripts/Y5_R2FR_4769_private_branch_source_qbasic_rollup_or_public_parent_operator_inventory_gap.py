from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4769"
CLAIM_ID = "L-611"
MARKER = "PPC4161_PRIVATE_BRANCH_SOURCE_QBASIC_ROLLUP_OR_PUBLIC_PARENT_OPERATOR_INVENTORY_GAP_4769"
PACKET_MARKER = "PPC4161_PACKET_PRIVATE_BRANCH_SOURCE_QBASIC_ROLLUP_OR_PUBLIC_PARENT_OPERATOR_INVENTORY_GAP_4769"
DECISION = "PRIVATE_SOURCE_QBASIC_ROLLUP_REDUCES_RESIDUAL_TO_SEVEN_NAMED_GATES_SOURCE_PREFACTOR_CLOSED_QEDGE_AND_QBAR_STILL_BLOCKED_BY_QBASIC_BOUNDARY_DENOMINATOR_PROJECTOR_NONCLAIM"
NEXT_TARGET = "4770-Y5-R2FR-private-source-qbasic-four-clause-closure-or-denominator-projector-first-values.md"

DOC_PATH = POST / "4769-Y5-R2FR-private-branch-source-qbasic-rollup-or-public-parent-operator-inventory-gap.md"
FORMAL_PATH = FORMAL / "785-PPC4161-private-branch-source-qbasic-rollup-or-public-parent-operator-inventory-gap.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4769_SOURCE_REGISTER.csv"
PRIVATE_ROLLUP_CSV = SOURCE_DIR / "P8_Y5_R2FR_4769_PRIVATE_SOURCE_QBASIC_RESIDUAL_ROLLUP.csv"
ZERO_LADDER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4769_QEDGE_ZERO_LADDER_AFTER_PRIVATE_ROLLUP.csv"
PUBLIC_GAP_CSV = SOURCE_DIR / "P8_Y5_R2FR_4769_PUBLIC_PARENT_OPERATOR_GAP.csv"
LOCAL_SCORING_GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4769_LOCAL_GR_SCORING_GATE_MATRIX.csv"
SOURCE_VALUE_LIST_CSV = SOURCE_DIR / "P8_Y5_R2FR_4769_SOURCE_VALUE_SHOPPING_LIST.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4769_ROUTE_SELECTION_MATRIX.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4769_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4769_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4769_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4769_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4769_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4769_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4769_0_4768_private_rollup", SOURCE_DIR / "P8_Y5_R2FR_4768_PRIVATE_SOURCE_QBASIC_ROLLUP.csv", "PBR4768_2_E_source_prefactor", "4768 private source-prefactor closure"),
    ("SRC4769_1_4768_public_gap", SOURCE_DIR / "P8_Y5_R2FR_4768_PUBLIC_PARENT_GAP_VECTOR.csv", "PGV4768_5_denominator_projector", "4768 public parent and denominator gaps"),
    ("SRC4769_2_4768_qedge_update", SOURCE_DIR / "P8_Y5_R2FR_4768_QEDGE_QBAR_SOURCE_CONTRACT_UPDATE.csv", "QQU4768_4_qbar_score", "4768 Qedge/Qbar status"),
    ("SRC4769_3_4768_poynting_candidate", SOURCE_DIR / "P8_Y5_R2FR_4768_POYNTING_WALL_FIRST_VALUE_CANDIDATE.csv", "PFV4768_5_total", "4768 Poynting zero candidate"),
    ("SRC4769_4_4767_contract", SOURCE_DIR / "P8_Y5_R2FR_4767_PARENT_SOURCE_QBASIC_CONTRACT.csv", "PSC4767_3_measure_qbasic", "4767 parent source-qbasic contract"),
    ("SRC4769_5_4767_residuals", SOURCE_DIR / "P8_Y5_R2FR_4767_SOURCE_QBASIC_RESIDUAL_VECTOR.csv", "SRV4767_8_total", "4767 residual envelope"),
    ("SRC4769_6_4766_support", SOURCE_DIR / "P8_Y5_R2FR_4766_SUPPORT_INVARIANCE_THEOREM.csv", "SIT4766_2_support_invariance", "4766 support-invariance theorem"),
    ("SRC4769_7_4766_poynting", SOURCE_DIR / "P8_Y5_R2FR_4766_POYNTING_WALL_FLUX_ROW.csv", "PWF4766_2_wall_flux_bound", "4766 Poynting wall flux row"),
    ("SRC4769_8_4765_qedge_shell", SOURCE_DIR / "P8_Y5_R2FR_4765_QEDGE_SHELL_ZERO_CERTIFICATE_AUDIT.csv", "ZQ4765_6_zero_theorem", "4765 Reynolds shell zero certificate"),
    ("SRC4769_9_4764_denominator_lemma", SOURCE_DIR / "P8_Y5_R2FR_4764_MLOWER_PIM_DENOMINATOR_LEMMA.csv", "DL4764_2_inverse_lock", "4764 denominator lemma"),
    ("SRC4769_10_4764_denominator_pack", SOURCE_DIR / "P8_Y5_R2FR_4764_DENOMINATOR_BOUND_PACK.csv", "DB4764_5_score_gate", "4764 denominator bound pack"),
    ("SRC4769_11_4714_em_owner", SOURCE_DIR / "P8_Y5_R2FR_4714_EM_STRESS_POYNTING_OWNER_THEOREM.csv", "EMP4714_4_no_double_count", "4714 EM/Poynting owner theorem"),
    ("SRC4769_12_4695_poynting_flux", SOURCE_DIR / "P8_Y5_R2FR_4695_POYNTING_FLUX_ROWS.csv", "FX4695_1_wall_flux_bound", "4695 Poynting flux bound"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    PRIVATE_ROLLUP_CSV,
    ZERO_LADDER_CSV,
    PUBLIC_GAP_CSV,
    LOCAL_SCORING_GATE_CSV,
    SOURCE_VALUE_LIST_CSV,
    ROUTE_MATRIX_CSV,
    PROMOTION_GATES_CSV,
    FIREWALL_CSV,
    DECISION_CSV,
    STATUS_CSV,
    NEXT_TARGET_CSV,
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path_object: Path) -> str:
    return path_object.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path_object: Path, content: str) -> None:
    path_object.parent.mkdir(parents=True, exist_ok=True)
    path_object.write_text(content, encoding="utf-8", newline="\n")


def write_csv(path_object: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path_object}")
    path_object.parent.mkdir(parents=True, exist_ok=True)
    with path_object.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path_object: Path) -> bool:
    with path_object.open("r", encoding="utf-8-sig", newline="") as handle:
        list(csv.DictReader(handle))
    return True


def append_once(path_object: Path, marker: str, block: str) -> None:
    existing = read_text(path_object) if path_object.exists() else ""
    if marker in existing:
        return
    separator = "" if not existing or existing.endswith("\n") else "\n"
    write_text(path_object, existing + separator + block.rstrip() + "\n")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row[column]).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, divider, *body])


def source_register(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path_object, needle, role in SOURCE_SPECS:
        exists = path_object.exists()
        text = read_text(path_object) if exists else ""
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path_object),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def private_rollup_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("PR4769_0_action_vertical", "E_action_vertical", "open", "direct source-action dependence not mediated by q", "requires parent source action descent PSC4767_0", "OPEN_PARENT_ACTION_DESCENT"),
        ("PR4769_1_constant_marker", "E_constant_marker", "open", "vertical masses, charges, alpha_EM, standards, or material labels", "requires fixed or quotient-owned theta branch", "OPEN_THETA_BRANCH"),
        ("PR4769_2_source_prefactor", "E_source_prefactor", "0_private", "source/species/material active-mass weight", "closed only inside private GR-parity no-prefactor branch from 4768", "CLOSED_PRIVATE_FROM_4768"),
        ("PR4769_3_matter_lift", "E_matter_lift", "open", "physical matter lift rather than gauge/on-shell/boundary silence", "requires lift owner, gauge proof, or proper-boundary theorem", "OPEN_LIFT_OR_BOUNDARY_SILENCE"),
        ("PR4769_4_Hodge_EM", "E_Hodge_EM", "conditional", "independent Maxwell-Hodge/current/constitutive owner", "same observed Hodge and current owner closes Hilbert EM placement", "OPEN_SAME_HODGE_BRANCH"),
        ("PR4769_5_Poynting_wall", "E_Poynting_wall", "zero_candidate_or_bound", "open/radiative EM flux crossing collar", "closed stationary collar gives zero; otherwise needs finite wall-flux values", "OPEN_INSTANCE_OR_VALUES"),
        ("PR4769_6_support_selector", "E_support_selector", "conditional", "support chosen after readout or fitted threshold", "pre-readout W_H=closure(supp mu_H) plus qbasic mu_H closes support motion", "OPEN_UNTIL_QBASIC_MEASURE_SIGNED"),
        ("PR4769_7_boundary_flux", "E_boundary_flux", "open_or_bound", "Hamiltonian/corner/radiative boundary leak", "needs boundary zero theorem or source-backed finite bound", "OPEN_BOUNDARY_OR_BOUND"),
        ("PR4769_8_private_envelope", "E_source_qbasic_private", "|E_action_vertical|+|E_constant_marker|+|E_matter_lift|+|E_Hodge_EM|+|E_Poynting_wall|+|E_support_selector|+|E_boundary_flux|", "no-cancellation residual after private source-prefactor closure", "this is the usable reduced target vector for the next derivation pass", "DERIVED_REDUCED_ENVELOPE_NONCLAIM"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "rollup_id": rollup_id,
            "symbol": symbol,
            "private_branch_value": value,
            "residual_meaning": meaning,
            "closure_condition": closure,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for rollup_id, symbol, value, meaning, closure, status in specs
    ]


def zero_ladder_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ZL4769_0_private_prefactor_removed", "E_source_prefactor=0_private", "4768 no-source-prefactor import", "DONE_PRIVATE", "removes one source-qbasic residual from the shell-zero problem"),
        ("ZL4769_1_action_descent", "S_src=Sbar_src[q(Phi),Psi,A,theta_bar(q)]+dB+S_top_silent", "parent action descent line", "OPEN", "needed to turn qbasicity into a theorem rather than a branch assumption"),
        ("ZL4769_2_fixed_theta", "theta is fixed or quotient-owned", "mass/charge/alpha/standard marker declaration", "OPEN", "needed to prevent hidden source or clock readout reentry"),
        ("ZL4769_3_same_Hodge", "Maxwell Hodge/current uses the same observed branch", "EM owner selector", "CONDITIONAL_OPEN", "needed so Poynting is Hilbert stress once or explicit wall flux, not both"),
        ("ZL4769_4_measure_qbasic", "mu_H=mu_bar_H[q(Phi)]", "follows from action descent plus observed geometry plus theta/Hodge ownership", "OPEN", "this is the exact support-invariance trigger"),
        ("ZL4769_5_support_preselected", "W_H=closure(supp mu_H) before readout", "support selector rule", "OPEN", "kills fitted worldtube motion when measure qbasicity is signed"),
        ("ZL4769_6_Qedge_shell_zero", "Q_edge_shell_abs=0", "measure qbasicity + support invariance + no birth/death", "BLOCKED_BY_ZL4769_1_TO_5", "not claimable yet"),
        ("ZL4769_7_boundary_routing", "Phi_wall_Poynting_abs=0 or finite bound", "closed stationary collar or wall values", "OPEN_INSTANCE_OR_VALUES", "routes waves into boundary row without hiding them in shell zero"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "ladder_id": ladder_id,
            "statement": statement,
            "required_evidence": evidence,
            "current_status": status,
            "effect_on_local_gr_route": effect,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for ladder_id, statement, evidence, status, effect in specs
    ]


def public_gap_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("PG4769_0_strict_grammar", "strict MTS primitive grammar uniqueness", "no public proof that the allowed grammar is the unique parent grammar", "would make no-Hom/no-source-prefactor public rather than private branch imported"),
        ("PG4769_1_component_graph_rank", "current parent-owned component graph rank", "signed parent edges for all matter components still absent", "would replace GR-parity import with internal MTS component ownership"),
        ("PG4769_2_one_parent_selector", "one parent action selector for source, Hodge, theta, support, and readout", "pieces exist conditionally but are not one signed parent branch", "blocks global source-qbasic theorem"),
        ("PG4769_3_no_shadow_frame", "no representative Weyl/disformal/source frame coefficients", "no-shadow/no-disformal leg not globally tied to source-qbasic branch", "blocks public local-GR/PPN promotion"),
        ("PG4769_4_boundary_silence", "boundary/corner/radiative silence or finite row", "Poynting zero is a branch candidate; open collars need values", "prevents hiding waves and apparatus in a false zero"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gap_id": gap_id,
            "public_parent_gap": gap,
            "why_still_open": why,
            "payoff_if_closed": payoff,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gap_id, gap, why, payoff in specs
    ]


def local_scoring_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("LSG4769_0_source_qbasic", "source qbasic measure", "E_source_qbasic_private=0 or bounded", "blocked by action/theta/lift/Hodge/support/Poynting/boundary legs", False, "NO_SCORE"),
        ("LSG4769_1_Qedge_shell", "Q_edge_shell_abs", "zero from exact qbasic support invariance or Reynolds bound with values", "blocked until source-qbasic ladder closes or values exist", False, "NO_SCORE"),
        ("LSG4769_2_Qedge_boundary", "Q_edge_boundary_abs", "boundary/corner/Poynting zero theorem or finite source-backed bound", "Poynting closed-collar zero is only a candidate; open values missing", False, "NO_SCORE"),
        ("LSG4769_3_denominator", "M_lower=M_0(1-epsilon_abs)>0", "M_0>0 and 0<=epsilon_abs<1 with same-frame source-backed values", "values missing from 4764 pack", False, "NO_SCORE"),
        ("LSG4769_4_projector", "P_M_bound and E_PiM_comm", "finite projector norm and zero/bounded commutator", "projector first values missing from 4764 pack", False, "NO_SCORE"),
        ("LSG4769_5_shadow", "Q_shadow_abs", "no-shadow theorem or finite residual", "not resolved by source-prefactor closure", False, "NO_SCORE"),
        ("LSG4769_6_qbar_product", "Qbar_XH local-GR score", "all numerator, edge, shadow, denominator and projector gates closed", "blocked by LSG4769_0..5", False, "PRODUCT_BLOCKED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "gate": gate,
            "needed_evidence": needed,
            "current_blocker": blocker,
            "score_fires_now": fires,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, gate, needed, blocker, fires, status in specs
    ]


def source_value_list_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SV4769_0_parent_action", "q-owned source action descent line", "symbolic theorem", "source-qbasic", "derive or demote to branch axiom", "highest"),
        ("SV4769_1_theta", "fixed/quotient-owned masses charges alpha_EM standards", "branch declaration or parent coefficient proof", "source-qbasic/time/EM", "derive from parent theta or keep constants external", "highest"),
        ("SV4769_2_matter_lift", "matter lift gauge/proper-boundary silence", "theorem or finite bound", "source-qbasic", "prove lift is gauge/on-shell/boundary or add residual", "high"),
        ("SV4769_3_same_Hodge", "same observed Hodge/current owner", "branch selector theorem", "EM/Poynting", "tie EM stress to Hilbert source exactly once", "high"),
        ("SV4769_4_support_selector", "W_H=closure(supp mu_H) before readout", "selector rule", "Qedge shell", "declare source support before fitting local tests", "high"),
        ("SV4769_5_closed_collar", "closed stationary Poynting collar or open wall values", "zero theorem or numeric bound", "EM/boundary", "choose source instance; do not hide radiation", "high"),
        ("SV4769_6_M0", "M_0 same-frame Hamiltonian denominator", "positive numeric/source-backed lower baseline", "Qbar denominator", "obtain first denominator value", "medium"),
        ("SV4769_7_epsilon_abs", "epsilon_abs denominator drift fraction", "numeric/source-backed <1 bound", "Qbar denominator", "obtain drift envelope or exact zero theorem", "medium"),
        ("SV4769_8_projector", "P_M_bound and E_PiM_comm", "finite operator norm and commutator zero/bound", "Qbar projector", "define fixed projector and source norm", "medium"),
        ("SV4769_9_boundary_shadow", "Q_edge_boundary_abs and Q_shadow_abs", "zero theorem or finite bound", "Qbar numerator", "separate boundary waves from shell/source support", "medium"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "value_id": value_id,
            "missing_input": missing,
            "required_form": required_form,
            "arena": arena,
            "next_action": action,
            "priority": priority,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for value_id, missing, required_form, arena, action, priority in specs
    ]


def route_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ROUTE4769_0_private_qbasic_first", "close the private source-qbasic four/five-clause ladder", "best chance of deriving Qedge shell zero rather than fitting it", "SELECTED_NEXT"),
        ("ROUTE4769_1_denominator_first_values", "source M_0, epsilon_abs, P_M_bound, E_PiM_comm", "needed before any Qbar/local-GR score can fire", "SECOND_PARALLEL"),
        ("ROUTE4769_2_public_parent_graph", "prove strict grammar uniqueness or parent component graph rank", "would convert private branch result into public parent theorem", "LONGER_ROUTE"),
        ("ROUTE4769_3_poynting_instance", "turn Poynting zero candidate into a declared source collar or finite value row", "prevents EM/wave leakage into fake shell zero", "PARALLEL_HIGH_VALUE"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "route_id": route_id,
            "route": route,
            "payoff": payoff,
            "selection_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for route_id, route, payoff, status in specs
    ]


def promotion_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("GATE4769_0_private_scope", "Do not promote E_source_prefactor=0_private to a public MTS theorem.", "keeps GR-parity import honest", False),
        ("GATE4769_1_no_cancellation", "All open residuals enter the private envelope by absolute value.", "prevents accidental cancellation claims", False),
        ("GATE4769_2_qedge_claim", "Q_edge_shell_abs=0 requires the qbasic measure/support ladder, not just no source-prefactor.", "blocks premature local-GR pass", False),
        ("GATE4769_3_poynting_owner", "Poynting is Hilbert EM stress once or explicit wall flux, never both.", "blocks EM double count", False),
        ("GATE4769_4_qbar_claim", "Qbar/local-GR score cannot fire until source, boundary, shadow, denominator, and projector gates are closed.", "blocks fake scoring", False),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "rule": rule,
            "enforced_effect": effect,
            "claim_allowed": allowed,
            "timestamp_utc": timestamp,
        }
        for gate_id, rule, effect, allowed in specs
    ]


def firewall_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("FW4769_0", "No local-GR/Newton/PPN/WEP/R10/clock/orbital pass from 4769.", "private rollup is an internal gate map only"),
        ("FW4769_1", "No source values may be inferred from desired local-GR success.", "prevents post-hoc coupling calibration"),
        ("FW4769_2", "No Poynting zero unless the source instance is closed, stationary, same-Hodge, and flux isolated.", "keeps waves visible"),
        ("FW4769_3", "No public parent theorem without one signed parent selector.", "keeps private branch separate from global claim"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": firewall_id,
            "firewall": firewall,
            "reason": reason,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for firewall_id, firewall, reason in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4769_0",
            "decision": DECISION,
            "summary": "4769 compresses the private branch into a reduced no-cancellation source-qbasic residual envelope. The source-prefactor leg is closed only inside the private GR-parity branch; the remaining gates are action descent, fixed theta, matter lift, same Hodge/current, Poynting wall handling, support selector, and boundary flux. Qedge shell zero and Qbar/local-GR scoring remain blocked until these gates or finite bounds are supplied.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4769_0",
            "state": "completed_nonclaim",
            "meaning": "Private branch rollup now has a reduced residual vector and explicit local scoring gates; no empirical/local-GR claim fires.",
            "next_target": NEXT_TARGET,
            "timestamp_utc": timestamp,
        }
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "Attack the remaining private source-qbasic clauses first, while keeping denominator/projector first values ready as the fallback scoring route.",
            "route_priority": "private_source_qbasic_four_clause_closure_then_denominator_projector_first_values",
            "timestamp_utc": timestamp,
        }
    ]


def write_docs(
    timestamp: str,
    private_rollup: list[dict[str, Any]],
    zero_ladder: list[dict[str, Any]],
    public_gap: list[dict[str, Any]],
    local_gates: list[dict[str, Any]],
    source_values: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4769: Private Branch Source-Qbasic Rollup or Public Parent Operator-Inventory Gap

Generated: `{timestamp}`

Marker: `{MARKER}`

## Result

- 4769 does **not** claim local GR, Newton, PPN, WEP, R10, clock, orbital, Maxwell, or source-coupling success.
- It does move the route forward by compressing the private branch after the 4768 no-source-prefactor result.
- Inside the private GR-parity branch, `E_source_prefactor=0_private`.
- Therefore the live private source-qbasic residual is reduced to:

```text
E_source_qbasic_private <=
  |E_action_vertical|
+ |E_constant_marker|
+ |E_matter_lift|
+ |E_Hodge_EM|
+ |E_Poynting_wall|
+ |E_support_selector|
+ |E_boundary_flux|.
```

- This is useful because the next derivation no longer has to fight the source-prefactor coupling; it has seven named gates with no cancellation allowed.

## Private Source-Qbasic Residual Rollup

{markdown_table(private_rollup, ["rollup_id", "symbol", "private_branch_value", "closure_condition", "status"])}

## Qedge Zero Ladder After Private Rollup

{markdown_table(zero_ladder, ["ladder_id", "statement", "required_evidence", "current_status", "effect_on_local_gr_route"])}

## Public Parent Operator Gap

{markdown_table(public_gap, ["gap_id", "public_parent_gap", "why_still_open", "payoff_if_closed"])}

## Local-GR Scoring Gate Matrix

{markdown_table(local_gates, ["gate_id", "gate", "needed_evidence", "current_blocker", "score_fires_now", "status"])}

## Source Value Shopping List

{markdown_table(source_values, ["value_id", "missing_input", "required_form", "arena", "next_action", "priority"])}

## Route Selection

{markdown_table(routes, ["route_id", "route", "payoff", "selection_status"])}

## Promotion Gates

{markdown_table(gates, ["gate_id", "rule", "enforced_effect", "claim_allowed"])}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)

    formal = f"""# PPC4161 4769: Private Source-Qbasic Rollup

Generated: `{timestamp}`

4769 compresses the current private local-GR route into the following no-cancellation envelope:

```text
E_source_qbasic_private <=
  |E_action_vertical|
+ |E_constant_marker|
+ |E_matter_lift|
+ |E_Hodge_EM|
+ |E_Poynting_wall|
+ |E_support_selector|
+ |E_boundary_flux|.
```

The `E_source_prefactor` leg is removed only inside the private GR-parity branch:

```text
E_source_prefactor = 0_private.
```

The route to Qedge shell zero is now sharply stated:

```text
parent action descent
 + fixed/quotient theta
 + same Maxwell-Hodge/current owner
 + qbasic Hilbert source measure
 + pre-readout support selector
 -> Q_edge_shell_abs = 0.
```

The Qbar/local-GR score still cannot fire because boundary/Poynting, shadow, denominator, and projector gates remain unsigned or value-missing.

Decision: `{DECISION}`

Next: `{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    spine_block = f"""

## {MARKER}

Generated: `{timestamp}`

- 4769 reduces the private branch source-qbasic residual vector by removing the source-prefactor leg: `E_source_prefactor=0_private`.
- The live private residual is now the no-cancellation envelope over action descent, constants/theta, matter lift, Hodge/current ownership, Poynting wall flux, support selector, and boundary flux.
- Qedge shell zero is now tied to a precise ladder: parent action descent plus fixed theta plus same Hodge/current plus qbasic Hilbert measure plus pre-readout support.
- Qbar/local-GR scoring remains blocked by source-qbasic, boundary/Poynting, shadow, denominator, and projector gates.
- Decision: `{DECISION}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""

## {PACKET_MARKER}

Generated: `{timestamp}`

4769 packet update: the private GR-parity branch is no longer fighting a source-prefactor coupling. The remaining source-qbasic problem has seven explicit legs and the Qedge/Qbar gates are separated so future work can attack derivation first and values second.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4769-Y5-R2FR-private-branch-source-qbasic-rollup-or-public-parent-operator-inventory-gap.md`

## Decision

`{DECISION}`

## What moved forward

- Reduced the private source-qbasic residual by removing `E_source_prefactor` inside the GR-parity branch.
- Derived the live no-cancellation envelope for `E_source_qbasic_private`.
- Separated the Qedge shell-zero ladder from boundary/Poynting, shadow, denominator, and projector gates.
- Produced a concrete source-value shopping list instead of a generic missing-input note.

## Current target

`{NEXT_TARGET}`

## Local-only note

No GitHub action was performed by this checkpoint.
"""
    write_text(RESUME_PATH, resume)


def add_claim_once(timestamp: str) -> None:
    existing = read_text(CLAIMS_PATH) if CLAIMS_PATH.exists() else ""
    if CLAIM_ID in existing:
        return
    row = [
        CLAIM_ID,
        "local_gr_private_source_qbasic_rollup",
        "4769 reduces the private source-qbasic residual after the no-source-prefactor import and identifies the exact remaining gates before Qedge/Qbar local-GR scoring.",
        "Generated source register, private source-qbasic residual rollup, Qedge zero ladder, public parent operator gap, local-GR scoring gate matrix, source value shopping list, route matrix, gates, firewalls, decision, status, next target and validation.",
        "private_source_qbasic_residual_reduced_source_prefactor_closed_qedge_qbar_blocked_nonclaim",
        NEXT_TARGET,
        "Treating the reduced private residual envelope as a proof that all source-qbasic clauses are closed.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need private source-qbasic four-clause closure or denominator/projector first values.",
        "Private branch source-qbasic rollup or public parent operator gap",
        f"{MARKER}; {DECISION}; generated {timestamp}",
    ]
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        csv.writer(handle).writerow(row)


def cleanup_pycache() -> None:
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(
    sources: list[dict[str, Any]],
    private_rollup: list[dict[str, Any]],
    zero_ladder: list[dict[str, Any]],
    public_gap: list[dict[str, Any]],
    local_gates: list[dict[str, Any]],
    source_values: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4769_0_sources_exist", "all cited source paths exist", all(row["exists"] for row in sources), str(SOURCE_REGISTER_CSV)))
    checks.append(("VAL4769_1_needles_found", "all source needles found", all(row["needle_found"] for row in sources), str(SOURCE_REGISTER_CSV)))
    for csv_path in GENERATED_CSVS:
        checks.append((f"VAL4769_csv_{csv_path.stem}", f"{csv_path.name} parses", csv_path.exists() and parse_csv(csv_path), str(csv_path)))

    envelope_rows = [row for row in private_rollup if row["symbol"] == "E_source_qbasic_private"]
    envelope_formula = envelope_rows[0]["private_branch_value"] if envelope_rows else ""
    checks.append(("VAL4769_2_prefactor_closed", "source-prefactor is closed only private", any(row["symbol"] == "E_source_prefactor" and row["private_branch_value"] == "0_private" for row in private_rollup), str(PRIVATE_ROLLUP_CSV)))
    checks.append(("VAL4769_3_reduced_envelope", "reduced envelope excludes E_source_prefactor and contains seven open legs", bool(envelope_rows) and "E_source_prefactor" not in envelope_formula and all(term in envelope_formula for term in ["E_action_vertical", "E_constant_marker", "E_matter_lift", "E_Hodge_EM", "E_Poynting_wall", "E_support_selector", "E_boundary_flux"]), str(PRIVATE_ROLLUP_CSV)))
    checks.append(("VAL4769_4_zero_ladder_blocked", "Qedge zero ladder remains blocked by open clauses", any(row["statement"] == "Q_edge_shell_abs=0" and "BLOCKED" in row["current_status"] for row in zero_ladder), str(ZERO_LADDER_CSV)))
    checks.append(("VAL4769_5_public_gap_retained", "public parent gap keeps one-parent selector and component graph", any("one parent" in row["public_parent_gap"] for row in public_gap) and any("component graph" in row["public_parent_gap"] for row in public_gap), str(PUBLIC_GAP_CSV)))
    checks.append(("VAL4769_6_local_score_blocked", "all local scoring gates are blocked", all(row["score_fires_now"] is False for row in local_gates), str(LOCAL_SCORING_GATE_CSV)))
    checks.append(("VAL4769_7_source_values_prioritized", "source value shopping list has highest and medium priorities", any(row["priority"] == "highest" for row in source_values) and any(row["priority"] == "medium" for row in source_values), str(SOURCE_VALUE_LIST_CSV)))
    checks.append(("VAL4769_8_route_selected", "route selects private qbasic closure first", any(row["selection_status"] == "SELECTED_NEXT" for row in routes), str(ROUTE_MATRIX_CSV)))
    checks.append(("VAL4769_9_gates_nonclaim", "promotion gates keep claims closed", all(row["claim_allowed"] is False for row in gates), str(PROMOTION_GATES_CSV)))
    checks.append(("VAL4769_10_docs_exist", "post and formal docs exist", DOC_PATH.exists() and FORMAL_PATH.exists(), f"{DOC_PATH}; {FORMAL_PATH}"))
    checks.append(("VAL4769_11_spine_marker", "spine marker appended", MARKER in read_text(SPINE_PATH), str(SPINE_PATH)))
    checks.append(("VAL4769_12_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_PATH), str(PACKET_PATH)))
    checks.append(("VAL4769_13_claim_row", "claim row L-611 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    resume_text = read_text(RESUME_PATH)
    checks.append(("VAL4769_14_resume", "resume points from 4769 to 4770", "4769-Y5" in resume_text and "4770-Y5" in resume_text, str(RESUME_PATH)))
    checks.append(("VAL4769_15_pycache_absent", "scripts __pycache__ removed", not (POST / "scripts" / "__pycache__").exists(), str(POST / "scripts")))

    overall = all(passed for _, _, passed, _ in checks)
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "validation_id": validation_id,
            "check": check,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for validation_id, check, passed, detail in checks
    ]
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "validation_id": "VAL4769_OVERALL",
            "check": "all 4769 private rollup/public gap checks pass",
            "status": "PASS" if overall else "FAIL",
            "detail": DECISION,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    )
    return rows


def main() -> None:
    timestamp = now()
    sources = source_register(timestamp)
    private_rollup = private_rollup_rows(timestamp)
    zero_ladder = zero_ladder_rows(timestamp)
    public_gap = public_gap_rows(timestamp)
    local_gates = local_scoring_gate_rows(timestamp)
    source_values = source_value_list_rows(timestamp)
    routes = route_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(PRIVATE_ROLLUP_CSV, private_rollup)
    write_csv(ZERO_LADDER_CSV, zero_ladder)
    write_csv(PUBLIC_GAP_CSV, public_gap)
    write_csv(LOCAL_SCORING_GATE_CSV, local_gates)
    write_csv(SOURCE_VALUE_LIST_CSV, source_values)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, private_rollup, zero_ladder, public_gap, local_gates, source_values, routes, gates)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, private_rollup, zero_ladder, public_gap, local_gates, source_values, routes, gates, timestamp))


if __name__ == "__main__":
    main()

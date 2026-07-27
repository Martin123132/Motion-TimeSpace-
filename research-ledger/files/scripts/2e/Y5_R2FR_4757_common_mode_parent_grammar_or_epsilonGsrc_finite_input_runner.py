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

CHECKPOINT = "4757"
CLAIM_ID = "L-599"
MARKER = "PPC4161_COMMON_MODE_PARENT_GRAMMAR_OR_EPSILONGSRC_FINITE_INPUT_RUNNER_4757"
PACKET_MARKER = "PPC4161_PACKET_COMMON_MODE_PARENT_GRAMMAR_OR_EPSILONGSRC_FINITE_INPUT_RUNNER_4757"
DECISION = "COMMON_MODE_GRAMMAR_CONDITIONAL_OWNER_NO_WA_UNSIGNED_EPSILONGSRC_FINITE_INPUT_RUNNER_STAGED_NONCLAIM"
NEXT_TARGET = "4758-Y5-R2FR-owner-no-wA-edge-activation-or-epsilonGsrc-projection-inputs.md"

DOC_PATH = POST / "4757-Y5-R2FR-common-mode-parent-grammar-or-epsilonGsrc-finite-input-runner.md"
FORMAL_PATH = FORMAL / "773-PPC4161-common-mode-parent-grammar-or-epsilonGsrc-finite-input-runner.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4757_SOURCE_REGISTER.csv"
COMMON_MODE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4757_COMMON_MODE_GRAMMAR_GATE.csv"
AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4757_COUNTERMODEL_AND_OWNER_THEOREM_AUDIT.csv"
FINITE_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4757_FINITE_INPUT_RUNNER.csv"
EPSILON_MAP_CSV = SOURCE_DIR / "P8_Y5_R2FR_4757_EPSILONGSRC_COMPONENT_MAP.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4757_ROUTE_SELECTION_MATRIX.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4757_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4757_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4757_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4757_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4757_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4757_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4757_0_4756_decision", SOURCE_DIR / "P8_Y5_R2FR_4756_DECISION.csv", "STRUCTURAL_NEWTON_BRIDGE_WITH_CALIBRATED_G_DERIVED_CONDITIONAL_EPSILON_GSRC_HAIR_BOUND_RETAINED_NONCLAIM", "4756 handoff decision"),
    ("SRC4757_1_4756_formal", FORMAL / "772-PPC4161-Htau-MHref-kappa-source-coupling-lock-or-transition-hair-bound.md", "q_tr -> q_0^H", "4756 common-mode formal handoff"),
    ("SRC4757_2_resume", RESUME_PATH, "4757-Y5-R2FR-common-mode-parent-grammar-or-epsilonGsrc-finite-input-runner.md", "current local resume target"),
    ("SRC4757_3_4357_theorem", SOURCE_DIR / "P8_Y5_R2FR_4357_THEOREM_ROWS.csv", "TH4357_0_common_mode_grammar", "common-mode grammar theorem"),
    ("SRC4757_4_4357_countermodel", SOURCE_DIR / "P8_Y5_R2FR_4357_COUNTEREXAMPLE_ROWS.csv", "CE4357_0_prevariation_wA", "pre-variation source-weight countermodel"),
    ("SRC4757_5_4357_finite", SOURCE_DIR / "P8_Y5_R2FR_4357_FINITE_INPUT_ROWS.csv", "FI4357_0_WEP_Delta_w_tau_anchor", "first WEP/R10 finite inputs"),
    ("SRC4757_6_4358_theorem", SOURCE_DIR / "P8_Y5_R2FR_4358_THEOREM_ROWS.csv", "TH4358_0_product_to_amplitude", "WEP product-to-amplitude law"),
    ("SRC4757_7_4358_delta", SOURCE_DIR / "P8_Y5_R2FR_4358_DELTA_W_AMPLITUDE_ROWS.csv", "DW4358_1_tau_min", "tau_min blocker row"),
    ("SRC4757_8_4359_tau", SOURCE_DIR / "P8_Y5_R2FR_4359_THEOREM_ROWS.csv", "TH4359_0_tau_min_sufficient", "tau lower-bound sufficient condition"),
    ("SRC4757_9_4360_decision", SOURCE_DIR / "P8_Y5_R2FR_4360_DECISION.csv", "OFFICIAL_MICROSCOPE_PORTAL_REPROBED", "official MICROSCOPE route state"),
    ("SRC4757_10_4361_theorem", SOURCE_DIR / "P8_Y5_R2FR_4361_THEOREM_ROWS.csv", "TH4361_3_full_owner_no_wA", "owner/no-wA conditional theorem"),
    ("SRC4757_11_4362_decision", SOURCE_DIR / "P8_Y5_R2FR_4362_DECISION.csv", "GRAPH_SIGNATURE_REJECTED", "parent graph route rejection"),
    ("SRC4757_12_4363_projection", SOURCE_DIR / "P8_Y5_R2FR_4363_WEPPRODUCT_PROJECTION_ROW.csv", "p_WEP_TiPt", "WEP product projection row"),
    ("SRC4757_13_4368_quarantine", SOURCE_DIR / "P8_Y5_R2FR_4368_DECISION.csv", "WEP_PRODUCT_FINAL_QUARANTINE", "WEP-only quarantine"),
    ("SRC4757_14_4370_bound_gate", SOURCE_DIR / "P8_Y5_R2FR_4370_DECISION.csv", "K_N(s)=min", "epsilon_Gsrc_perp Newton bound gate"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    COMMON_MODE_CSV,
    AUDIT_CSV,
    FINITE_INPUT_CSV,
    EPSILON_MAP_CSV,
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


def common_mode_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("CMG4757_0_no_prevariation_wA", "no independent source-only pre-variation action weight w_A S_A", "kills Delta_w_A/source-label hair before metric variation", "REQUIRED_PARENT_SIGNATURE_UNSIGNED"),
        ("CMG4757_1_one_action_measure_owner", "one universal action-measure owner for ordinary matter", "collapses source weights to a common calibration if graph and no-reentry clauses also hold", "REQUIRED_PARENT_SIGNATURE_UNSIGNED"),
        ("CMG4757_2_connected_ordinary_matter_graph", "parent-owned connected ordinary-matter graph with natural scalar action weights", "imports the 4361 conditional theorem w_A=w_* on the connected component", "EXACT_CONDITIONAL_THEOREM_GRAPH_UNSIGNED"),
        ("CMG4757_3_no_hidden_reentry", "no hidden reentry through readout, EFT source labels, theta markers, projector maps or EM-current weights", "prevents w_A from sneaking back after variation", "REQUIRED_EXTENSION_UNSIGNED"),
        ("CMG4757_4_no_independent_range_pole", "no independent finite-range pole/operator separate from Hilbert common mode", "kills Y_lambda/range hair without using R10 anchors as proof", "REQUIRED_PARENT_SIGNATURE_UNSIGNED"),
        ("CMG4757_5_q0H_common_mode", "stationary l=0 universal range-free same-metric Hilbert source dressing q_tr -> q_0^H", "only this branch can be treated as source-mass dressing rather than local-test residual", "CONDITIONAL_BRANCH_NOT_PARENT_SIGNED"),
        ("CMG4757_6_maxwell_poynting_once", "Maxwell-Hodge/Poynting momentum flux counted once as Hilbert stress or boundary flux", "keeps EM/charge route from double-counting a background source field", "IMPORTED_GUARD_CONDITIONAL"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "parent_grammar_clause": clause,
            "effect_if_signed": effect,
            "current_status": status,
            "zero_claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, clause, effect, status in specs
    ]


def audit_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("AUD4757_0_prevariation_wA", "S_matter -> sum_A w_A S_A before variation", "preserves isolated matter equations while scaling metric source", "ACTIVE_COUNTERMODEL", "Delta_w_A remains open"),
        ("AUD4757_1_current_owner_not_enough", "Hilbert current ownership after variation", "does not remove weights inserted before variation", "PROOF_SHORTCUT_REJECTED", "current-owner-only route blocked"),
        ("AUD4757_2_owner_no_wA_theorem", "single action-density owner + connected graph + species-blind measure + no-source-prefactor + no-reentry", "would derive Delta_w_A=0 and Xi_src_hidden=0", "EXACT_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED", "best zero route but not claim grade"),
        ("AUD4757_3_graph_signature_test", "parent-owned source graph searched in current corpus", "required source-relevant edges not parent-certified", "CURRENT_CORPUS_REJECTED", "cannot promote zero theorem now"),
        ("AUD4757_4_wep_product_quarantine", "|Delta_w_TiPt*tau_WEP| <= 2.8e-15", "source-backed WEP product only", "WEP_ONLY_NOT_EXPORTABLE", "does not close PPN/Newton/local-GR"),
        ("AUD4757_5_generic_nondegeneracy_fail", "readout/source projection has a kernel without signed parent basis", "nonzero ingredients do not imply tau_WEP nonzero", "TAU_MIN_ROUTE_BLOCKED", "need k_min,s_min,m_min,c_min,N_max"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "audit_id": audit_id,
            "object_checked": object_checked,
            "why_it_matters": why,
            "result": result,
            "residual_or_next_need": next_need,
            "zero_claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for audit_id, object_checked, why, result, next_need in specs
    ]


def finite_input_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("FI4757_0_WEP_product", "WEP/source-composition", "abs(Delta_w_TiPt*tau_WEP) <= 2.8e-15", "source-backed product anchor", "tau_min and MTS Delta_w projection missing", "NONCLAIM_BOUND_INPUT"),
        ("FI4757_1_tau_min_law", "WEP amplitude bridge", "tau_min = k_min*s_min*m_min*c_min/N_max", "exact sufficient lower-bound law", "k_min, s_min, m_min, c_min, N_max all unsourced", "BLOCKED_SYMBOLIC_INPUT"),
        ("FI4757_2_R10_2020_anchor", "short-range/R10", "alpha_bound(lambda=3.86e-5 m)=1", "Eot-Wash 2020 threshold anchor", "full alpha(lambda) curve and MTS coefficients missing", "ANCHOR_ONLY_NONCLAIM"),
        ("FI4757_3_R10_2007_anchor", "short-range/R10", "alpha_bound(lambda=5.6e-5 m)=1", "Eot-Wash 2007 continuity anchor", "full curve and parent coefficients missing", "ANCHOR_ONLY_NONCLAIM"),
        ("FI4757_4_Newton_perp_gate", "Newton/source-normalization", "E_perp <= delta_N/K_N(s); K_N(s)=min((1-s)^-2, 2s(1-s)^-3)", "derived zero-monopole geometry gate", "delta_N, R/r support map and E_perp coefficients missing", "TEMPLATE_READY_INPUTS_MISSING"),
        ("FI4757_5_Csrc_open_runner", "multi-arena source coupling", "T_open maps C_src_open into WEP, PPN, R10, clock, orbital, EM and Newton rows", "failure branch is now runnable without pretending zero", "arena projection coefficients remain to be sourced", "NONCLAIM_RUNNER"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "input_id": input_id,
            "arena": arena,
            "law_or_bound": law,
            "what_is_real_now": real,
            "what_is_missing": missing,
            "status": status,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for input_id, arena, law, real, missing, status in specs
    ]


def epsilon_map_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("EG4757_0_total", "epsilon_Gsrc", "epsilon_Gsrc <= epsilon_kappa + delta_H + Delta_ref + Delta_tau + Delta_boundary + epsilon_PiH + Delta_MHref + epsilon_tr_hair + C_src_open", "overall local source/coupling residual vector", "NO_CANCELLATION_SUM"),
        ("EG4757_1_kappa", "epsilon_kappa", "|D_A ln kappa_*| + |D_A delta_ZH|", "coupling/source-measure drift", "FINITE_IF_OWNER_NOT_SIGNED"),
        ("EG4757_2_Htau", "delta_H", "|I_MTS|/M_H_ref", "Hamiltonian integrability defect", "FINITE_IF_INTEGRABILITY_NOT_SIGNED"),
        ("EG4757_3_reference_tau_boundary", "Delta_ref + Delta_tau + Delta_boundary", "sum reference/time-frame/boundary flux residual ratios", "readout/source-charge closure residue", "FINITE_INPUTS_REQUIRED"),
        ("EG4757_4_PiH_MHref", "epsilon_PiH + Delta_MHref", "|ell_M(Pi_M^H J_H_total)-(H_tau-H_ref)|/|M_H^dress| + |delta_MHref|/M_H_ref", "Hamiltonian-selector and normalizer defects", "PRIVATE_ZERO_OR_FINITE_BOUND"),
        ("EG4757_5_transition_hair", "epsilon_tr_hair", "Y_nonHilbert + Delta_Wtr + Y_tau + Y_l>=1 + Y_species_frame_source + Y_lambda + Y_nonEH + Y_boundary", "transition hair if not pure q_0^H", "COMMON_MODE_OR_FINITE_HAIR"),
        ("EG4757_6_Csrc_open", "C_src_open", "Delta_w vector + Xi_open + source/readout hidden coupling", "explicit failure branch for unsigned owner/no-wA theorem", "ZERO_ONLY_IF_PARENT_OWNER_THEOREM_SIGNED"),
        ("EG4757_7_perp_gate", "epsilon_Gsrc_perp", "zero-monopole residual with Newton gate E_perp <= delta_N/K_N(s)", "coefficient-bound version of source-normalization hair", "BOUND_GATE_READY_INPUTS_MISSING"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "component_id": component_id,
            "component": component,
            "formula": formula,
            "meaning": meaning,
            "current_status": status,
            "zero_claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for component_id, component, formula, meaning, status in specs
    ]


def route_matrix_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ROUTE4757_0_zero_parent_grammar", "prove parent grammar forbids w_A and hidden reentry", "would close C_src_open and source-label hair", "BEST_ROUTE_BUT_UNSIGNED"),
        ("ROUTE4757_1_owner_edge_activation", "find parent-owned measure/current/readout/same-source-mass edges", "activates existing conditional theorem without new closure", "NEXT_DERIVATION_TARGET"),
        ("ROUTE4757_2_finite_projection_inputs", "source arena coefficients for epsilon_Gsrc_perp/T_open", "turns open coupling into bounded residuals", "BEST_EMPIRICAL_FALLBACK"),
        ("ROUTE4757_3_tau_min_route", "source k_min,s_min,m_min,c_min,N_max", "converts WEP product into Delta_w amplitude bound", "USEFUL_BUT_WEP_ONLY"),
        ("ROUTE4757_4_R10_curve_route", "digitize/source full alpha(lambda) curve and MTS coefficients", "tests range hair without overclaim", "SECONDARY_LOCAL_BOUND_ROUTE"),
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
        ("PG4757_0_no_claim_from_theorem_name", "conditional theorem cannot be promoted unless every premise is parent-signed", "BLOCKS_OWNER_NO_WA_OVERCLAIM"),
        ("PG4757_1_no_wep_export", "WEP product bound cannot be exported to PPN/Newton/local-GR", "BLOCKS_PRODUCT_SHORTCUT"),
        ("PG4757_2_no_tau_one", "tau_WEP cannot be set to one without source/readout derivation", "BLOCKS_TAU_SHORTCUT"),
        ("PG4757_3_no_r10_anchor_curve", "alpha=1 threshold anchors are not a full exclusion curve", "BLOCKS_R10_SHORTCUT"),
        ("PG4757_4_no_gr_claim", "local GR/Newton pass requires owner zero or source-backed finite epsilon_Gsrc projections", "BLOCKS_LOCAL_GR_CLAIM"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "rule": rule,
            "enforced_effect": effect,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, rule, effect in specs
    ]


def firewall_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("FW4757_0_private_not_public", "4757 is private discipline work, not a public local-GR/R10/WEP claim."),
        ("FW4757_1_source_coupling_not_zero", "Do not set source coupling residuals to zero by notation; prove owner/no-wA or carry C_src_open."),
        ("FW4757_2_em_once", "Poynting/Maxwell stress may motivate source flow, but must be counted once through Hilbert stress or boundary flux."),
        ("FW4757_3_calibrated_G", "The target is GR-style calibrated G with derivable source-blind coupling, not a fake numeric G_N prediction."),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": firewall_id,
            "rule": rule,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for firewall_id, rule in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision": DECISION,
            "meaning": "4757 converts the source-coupling bottleneck into a clean fork: parent common-mode owner/no-wA grammar remains the preferred derivation route, but it is unsigned; therefore epsilon_Gsrc/C_src_open finite-input plumbing is staged as the honest fallback.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STAT4757_0",
            "summary": "Common-mode grammar sharpened; w_A countermodel still active; finite epsilon_Gsrc input runner staged.",
            "claim_status": "NONCLAIM_PRIVATE_CHECKPOINT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "recommended_first_move": "Try to activate the owner/no-wA edge package from parent source/action text; if not, populate epsilon_Gsrc projection coefficients for Newton/PPN/WEP/R10.",
            "why": "This is the least hand-wavy route: either derive common source coupling, or explicitly bound the residual.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row[column]).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, divider, *body])


def write_docs(
    timestamp: str,
    common_rows: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    finite_rows: list[dict[str, Any]],
    epsilon_rows: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4757: Common-Mode Parent Grammar or epsilon_Gsrc Finite Input Runner

Generated: `{timestamp}`

Marker: `{MARKER}`

## Result

4757 does **not** claim local GR/Newton, WEP, PPN or R10 success. It makes the coupling bottleneck cleaner:

- The preferred derivation route is still the parent common-mode owner/no-`w_A` grammar.
- The `w_A` countermodel remains active because the current corpus has not parent-signed every owner/no-hidden-reentry premise.
- The fallback is now explicit: carry `epsilon_Gsrc`, `epsilon_Gsrc_perp` and `C_src_open` as finite residual inputs instead of hiding them.
- Poynting/Maxwell stress can be used as a source-flow clue only if counted once through Hilbert stress or boundary flux.

## Common-Mode Grammar Gate

{markdown_table(common_rows, ["gate_id", "parent_grammar_clause", "effect_if_signed", "current_status"])}

## Countermodel and Owner-Theorem Audit

{markdown_table(audit, ["audit_id", "object_checked", "result", "residual_or_next_need"])}

## Finite Input Runner

{markdown_table(finite_rows, ["input_id", "arena", "law_or_bound", "what_is_missing", "status"])}

## epsilon_Gsrc Component Map

{markdown_table(epsilon_rows, ["component_id", "component", "formula", "current_status"])}

## Route Selection

{markdown_table(routes, ["route_id", "route", "payoff", "selection_status"])}

## Promotion Gates

{markdown_table(gates, ["gate_id", "rule", "enforced_effect"])}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)

    formal = f"""# PPC4161 4757: Common-Mode Grammar / epsilon_Gsrc Fork

Generated: `{timestamp}`

## Formal Fork

The source-coupling problem is now the fork

```text
owner/no-w_A parent grammar signed
    => C_src_open = 0, Delta_w_A = 0, Xi_src_hidden = 0
else
    => epsilon_Gsrc carries C_src_open and epsilon_Gsrc_perp as finite local-test residuals.
```

The common-mode branch requires

```text
q_tr -> q_0^H
```

with stationary l=0, universal, range-free, same-metric Hilbert source dressing. Otherwise the no-cancellation bound remains

```text
epsilon_Gsrc <= epsilon_kappa + delta_H + Delta_ref + Delta_tau
              + Delta_boundary + epsilon_PiH + Delta_MHref
              + epsilon_tr_hair + C_src_open
```

The WEP product row remains only

```text
abs(Delta_w_TiPt*tau_WEP) <= 2.8e-15
```

and becomes an amplitude bound only with

```text
tau_min = k_min*s_min*m_min*c_min/N_max > 0.
```

The Newton/source-normalization finite branch uses

```text
E_perp <= delta_N/K_N(s),     K_N(s)=min((1-s)^-2, 2s(1-s)^-3).
```

Decision: `{DECISION}`

Next: `{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    spine_block = f"""

## {MARKER}

Generated: `{timestamp}`

- 4757 sharpens the source-coupling bottleneck into a fork: parent owner/no-`w_A` common-mode grammar, or finite `epsilon_Gsrc`/`C_src_open` residual inputs.
- The zero route remains conditional because the pre-variation `w_A` countermodel survives without parent-signed action-measure/no-reentry clauses.
- The finite route is now explicit: WEP product, tau-min law, R10 anchors, Newton `K_N(s)` gate, and multi-arena `T_open` projection are staged as nonclaim plumbing.
- Decision: `{DECISION}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""

## {PACKET_MARKER}

Generated: `{timestamp}`

4757 local packet update: source coupling is no longer a vague missing piece. It is either killed by parent owner/no-`w_A` grammar or carried as `epsilon_Gsrc`/`C_src_open` through explicit projection inputs.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4757-Y5-R2FR-common-mode-parent-grammar-or-epsilonGsrc-finite-input-runner.md`

## Decision

`{DECISION}`

## What moved forward

- Converted the coupling issue into a clean fork: prove parent owner/no-`w_A`, or carry finite `epsilon_Gsrc`.
- Kept the `w_A` countermodel alive because the parent action grammar is not fully signed.
- Staged the finite input runner for WEP product, `tau_min`, R10 anchors, Newton `K_N(s)`, `epsilon_Gsrc_perp`, and `C_src_open`.
- Preserved the Poynting/Maxwell clue as Hilbert stress or boundary flux only, not a second counted source.

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
        "local_gr_source_coupling_fork",
        "4757 stages the common-mode parent grammar versus finite epsilon_Gsrc/C_src_open source-coupling fork.",
        "Generated source register, grammar gate, countermodel audit, finite input runner, epsilon component map, route matrix, promotion gates, firewalls, decision, status, next target and validation.",
        "common_mode_parent_grammar_or_epsilonGsrc_finite_input_runner_nonclaim",
        NEXT_TARGET,
        "Claiming owner/no-wA zero, WEP amplitude, R10 pass, PPN pass or local-GR pass before parent signatures or finite projection inputs are supplied.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need owner/no-wA edge activation or source-backed epsilon_Gsrc projection inputs.",
        "common-mode parent grammar or epsilonGsrc finite input runner",
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
    common_rows: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    finite_rows: list[dict[str, Any]],
    epsilon_rows: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4757_0_sources_exist", "all cited source paths exist", all(row["exists"] for row in sources), str(SOURCE_REGISTER_CSV)))
    checks.append(("VAL4757_1_needles_found", "all source needles found", all(row["needle_found"] for row in sources), str(SOURCE_REGISTER_CSV)))
    for csv_path in GENERATED_CSVS:
        checks.append((f"VAL4757_csv_{csv_path.stem}", f"{csv_path.name} parses", csv_path.exists() and parse_csv(csv_path), str(csv_path)))
    checks.append(("VAL4757_2_common_mode", "grammar gate includes w_A and q_0^H", any("w_A" in row["parent_grammar_clause"] for row in common_rows) and any("q_0^H" in row["parent_grammar_clause"] for row in common_rows), str(COMMON_MODE_CSV)))
    checks.append(("VAL4757_3_countermodel", "audit keeps prevariation_wA active and owner theorem unsigned", any("prevariation_wA" in row["audit_id"] and "ACTIVE" in row["result"] for row in audit) and any("owner_no_wA" in row["audit_id"] and "NOT_PARENT_SIGNED" in row["result"] for row in audit), str(AUDIT_CSV)))
    checks.append(("VAL4757_4_finite_runner", "finite runner includes WEP product, tau_min, R10 anchors and K_N(s)", any("2.8e-15" in row["law_or_bound"] for row in finite_rows) and any("tau_min" in row["law_or_bound"] for row in finite_rows) and any("alpha_bound" in row["law_or_bound"] for row in finite_rows) and any("K_N(s)" in row["law_or_bound"] for row in finite_rows), str(FINITE_INPUT_CSV)))
    checks.append(("VAL4757_5_epsilon_map", "epsilon map includes epsilon_Gsrc total and epsilon_Gsrc_perp", any(row["component"] == "epsilon_Gsrc" for row in epsilon_rows) and any(row["component"] == "epsilon_Gsrc_perp" for row in epsilon_rows), str(EPSILON_MAP_CSV)))
    checks.append(("VAL4757_6_gates_nonclaim", "promotion gates keep claims closed", all(row["claim_allowed"] is False for row in gates), str(PROMOTION_GATES_CSV)))
    checks.append(("VAL4757_7_docs_exist", "post and formal docs exist", DOC_PATH.exists() and FORMAL_PATH.exists(), f"{DOC_PATH}; {FORMAL_PATH}"))
    checks.append(("VAL4757_8_spine_marker", "spine marker appended", MARKER in read_text(SPINE_PATH), str(SPINE_PATH)))
    checks.append(("VAL4757_9_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_PATH), str(PACKET_PATH)))
    checks.append(("VAL4757_10_claim_row", "claim row L-599 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    resume_text = read_text(RESUME_PATH)
    checks.append(("VAL4757_11_resume", "resume points from 4757 to 4758", "4757-Y5" in resume_text and "4758-Y5" in resume_text, str(RESUME_PATH)))
    checks.append(("VAL4757_12_pycache_absent", "scripts __pycache__ removed", not (POST / "scripts" / "__pycache__").exists(), str(POST / "scripts")))
    overall = all(item[2] for item in checks)
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
            "validation_id": "VAL4757_OVERALL",
            "check": "all 4757 common-mode/epsilonGsrc nonclaim checks pass",
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
    common_rows = common_mode_rows(timestamp)
    audit = audit_rows(timestamp)
    finite_rows = finite_input_rows(timestamp)
    epsilon_rows = epsilon_map_rows(timestamp)
    routes = route_matrix_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(COMMON_MODE_CSV, common_rows)
    write_csv(AUDIT_CSV, audit)
    write_csv(FINITE_INPUT_CSV, finite_rows)
    write_csv(EPSILON_MAP_CSV, epsilon_rows)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, common_rows, audit, finite_rows, epsilon_rows, routes, gates)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, common_rows, audit, finite_rows, epsilon_rows, gates, timestamp))


if __name__ == "__main__":
    main()

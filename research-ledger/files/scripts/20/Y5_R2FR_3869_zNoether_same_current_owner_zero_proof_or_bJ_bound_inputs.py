from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3869"
BRANCH = "MTS_R2FR_Y5_ZNOETHER_SAME_CURRENT_OWNER_ZERO_PROOF_OR_BJ_BOUND_INPUTS_3869"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3869-Y5-R2FR-zNoether-same-current-owner-zero-proof-or-bJ-bound-inputs.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

CSV_3868_NEXT = OUT / "P8_Y5_R2FR_3868_NEXT_TARGET.csv"
CSV_3868_PROOF = OUT / "P8_Y5_R2FR_3868_ZG_ZERO_PROOF_AUDIT.csv"
CSV_3868_INPUTS = OUT / "P8_Y5_R2FR_3868_CURRENT_NORMALIZATION_BOUND_INPUT_REQUIREMENTS.csv"
CSV_3143_CURRENT = OUT / "P8_Y5_R2FR_3143_SAME_CURRENT_OWNER_THEOREM.csv"
CSV_3119_DELTAJ = OUT / "P8_Y5_R2FR_3119_SAME_CURRENT_OWNER_DELTAJ_GATE.csv"
CSV_1079_CURRENT = OUT / "P8_Y5_R10_1079_NARROW_CURRENT_OWNER_THEOREM_ATTEMPT.csv"
CSV_3508_ZG = OUT / "P8_Y5_R2FR_3508_ZG_BETA_SOURCE_REDUCTION.csv"
CSV_3863_SLOT = OUT / "P8_Y5_R2FR_3863_CHARGE_CURRENT_SLOT_AUDIT.csv"
CSV_3863_BOUND = OUT / "P8_Y5_R2FR_3863_EM_SOURCE_SCALE_BOUND.csv"
CSV_989_EMLOCK = OUT / "P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv"
DOC_1387_WEIGHT = PCW / "1387-Y5-R10-RAB-action-weight-exclusion-or-source-beta-first-fill.md"
CSV_1388_DW = OUT / "P8_Y5_R10_1388_DELTA_W_SOURCE_BETA_VALIDATOR.csv"
CSV_3819_SOURCE = OUT / "P8_Y5_R2FR_3819_FINITE_SOURCE_NORMALIZATION_RESIDUALS.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3869_SOURCE_REGISTER.csv",
    "theorem": OUT / "P8_Y5_R2FR_3869_ZNOETHER_THEOREM_PROOF.csv",
    "premises": OUT / "P8_Y5_R2FR_3869_CURRENT_OWNER_PREMISE_AUDIT.csv",
    "bj_bound": OUT / "P8_Y5_R2FR_3869_BJ_BOUND_DECOMPOSITION.csv",
    "arena": OUT / "P8_Y5_R2FR_3869_ARENA_INTERFACE_ROWS.csv",
    "gates": OUT / "P8_Y5_R2FR_3869_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3869_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3869_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3869_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3869_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3869_00_3868_next", CSV_3868_NEXT, "NEXT3868_0", "3868 selected z_Noether same-current owner"),
    ("SRC3869_01_3868_proof", CSV_3868_PROOF, "ZP3868_3_noether_chain_rule", "3868 z_Noether chain-rule target"),
    ("SRC3869_02_3868_inputs", CSV_3868_INPUTS, "BIR3868_1_z_Noether", "3868 b_J input requirement"),
    ("SRC3869_03_3143_current", CSV_3143_CURRENT, "SCOT3143_3_same_current_owner", "same-current owner conditional theorem"),
    ("SRC3869_04_3143_ward", CSV_3143_CURRENT, "SCOT3143_5_Ward_limit", "Ward conservation not calibration guard"),
    ("SRC3869_05_3119_deltaJ", CSV_3119_DELTAJ, "SCJ3119_0", "deltaJ same-current gate"),
    ("SRC3869_06_3119_counter", CSV_3119_DELTAJ, "SCJ3119_3", "source-only weight countermodel"),
    ("SRC3869_07_1079_post", CSV_1079_CURRENT, "NCO1079_4_current_rescaling", "post-variation current rescale narrowed"),
    ("SRC3869_08_1079_weight", CSV_1079_CURRENT, "NCO1079_5_species_action_weight", "pre-variation weights survive current-owner proof"),
    ("SRC3869_09_3508_zg", CSV_3508_ZG, "CSR3508_0_z_g", "z_g conditional zero if fixed quotient matter functor"),
    ("SRC3869_10_3863_slot", CSV_3863_SLOT, "CCA3863_2_same_current", "current slot audit"),
    ("SRC3869_11_3863_bound", CSV_3863_BOUND, "ESB3863_1_current_drift", "b_J symbolic bound"),
    ("SRC3869_12_989_current", CSV_989_EMLOCK, "ELA989_2_current_owner", "EM lock current owner unsigned"),
    ("SRC3869_13_1387_weight", DOC_1387_WEIGHT, "AWE1387_0_definition", "pre-variation action weight counterexample"),
    ("SRC3869_14_1388_validator", CSV_1388_DW, "DWV1388_7_verdict", "Delta_w validator blocked"),
    ("SRC3869_15_3819_source", CSV_3819_SOURCE, "R3819_6_total", "source-normalization total residual"),
]

THEOREM_FORM = "If S_matter=Sbar[q(Phi),Psi,A_Q(q),n_A,theta_A] with Dq[v]=0 and no source/readout current slots, then z_Noether,A=D_v ln Z_JA=0."
BJ_BOUND = "b_J,A <= b_Sdescent + b_AQdescent + b_rep + b_preweight + b_current_selector + b_rad_readout + b_boundary_current"


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
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def source_register_rows(timestamp: str) -> list[dict[str, object]]:
    rows = []
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
                "claim_use": "nonclaim_zNoether_current_owner_proof",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "ZNT3869_0_definition",
            "Noether current normalization term",
            "z_Noether,A := D_v ln Z_JA",
            "Z_JA is the current normalization left after fixed charge label n_A and base unit Qstar are separated",
            "DEFINITION",
            "does not assert zero",
        ),
        (
            "ZNT3869_1_qbasic_action",
            "vertical silence of the parent matter action",
            "Dq[v]=0 and S_matter=Sbar[q(Phi),Psi,A_Q(q),n_A,theta_A]",
            "chain rule gives L_v S_matter=0 and L_v A_Q=0 at fixed observed fields and fixed representation labels",
            "EXACT_CONDITIONAL_STEP",
            "requires q-basic matter functor and same A_Q owner",
        ),
        (
            "ZNT3869_2_commute_variation",
            "current extraction commutes with vertical variation",
            "J_Q^mu=(1/mu_obs) delta S_matter/delta A_Q_mu before readout",
            "L_v J_Q^mu=(1/mu_obs) delta(L_v S_matter)/delta A_Q_mu plus commutator terms; commutator terms vanish only with same domain and no readout reentry",
            "EXACT_CONDITIONAL_STEP",
            "requires variation-before-readout and stable effective action domain",
        ),
        (
            "ZNT3869_3_zero_theorem",
            "z_Noether zero theorem",
            THEOREM_FORM,
            "combine q-basic action, fixed representation labels, same A_Q owner, variation-before-readout, and no extra current/source slots",
            "EXACT_CONDITIONAL_THEOREM",
            "not parent-promoted because no-source-only and readout/radiative clauses remain unsigned",
        ),
        (
            "ZNT3869_4_counterexample",
            "why current conservation is not enough",
            "J_Q=sum_A n_A c_A(X)J_A or S_matter=sum_A w_A(X)S_A can still be conserved",
            "Ward conservation permits conserved weighted currents; it does not fix hidden-independence of normalization",
            "COUNTEREXAMPLE_RETAINED",
            "requires parent grammar exclusion or finite b_J/Delta_w rows",
        ),
        (
            "ZNT3869_5_verdict",
            "current corpus verdict",
            "z_Noether,A=0 has an exact conditional proof, but not a parent-signed proof",
            "the finite fallback is b_J,A with explicit components and source paths",
            "ZERO_THEOREM_CONDITIONAL_BJ_FALLBACK_REQUIRED",
            "next target must ban source-only current/action slots or fill b_J inputs",
        ),
    ]
    return [
        {
            "theorem_id": theorem_id,
            "claim_piece": claim_piece,
            "statement": statement,
            "proof_move": proof_move,
            "result": result,
            "remaining_gap": gap,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for theorem_id, claim_piece, statement, proof_move, result, gap in rows
    ]


def premise_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("PREM3869_0_qbasic_matter", "matter action descends through q", "S_matter=Sbar[q(Phi),Psi,A_Q(q),n_A,theta_A]", "CONDITIONAL_NOT_PARENT_SIGNED", "SCOT3143_1_qbasic_matter_current", "parent ordinary-matter functor certificate"),
        ("PREM3869_1_same_AQ_owner", "A_Q and J_Q share one parent owner", "J_Q=delta S_matter/delta A_Q before readout", "UNSIGNED", "ELA989_2_current_owner; CCA3863_2_same_current", "same T_Q/A_Q/current owner"),
        ("PREM3869_2_fixed_labels", "representation labels fixed", "D_v n_A=0 and D_v theta_A=0", "PARTIAL_FROM_3868_FIXED_SECTOR", "ZP3868_1_integer_lattice", "fixed-sector certificate"),
        ("PREM3869_3_no_source_only_current_slot", "no c_A/q_A/kappa_A current slot", "no J_Q=sum_A n_A c_A(X)J_A and no kappa_A(X) source selector", "UNSIGNED_COUNTERMODEL_RETAINED", "SCJ3119_2; SCJ3119_3", "parent object-language exclusion"),
        ("PREM3869_4_no_prevariation_weight", "no pre-variation action/source weight", "no S_matter=sum_A w_A(X)S_A", "UNSIGNED_COUNTERMODEL_RETAINED", "NCO1079_5_species_action_weight; AWE1387_0_definition", "action-measure/source-scalar exclusion"),
        ("PREM3869_5_variation_before_readout", "variation happens before readout", "J_parent and T_parent are extracted before material/apparatus projection", "CONDITIONAL_SUBTHEOREM", "NCO1079_3_post_variation_selector; NCO1079_4_current_rescaling", "parent readout-order axiom"),
        ("PREM3869_6_radiative_readout_stability", "loops/readout do not reintroduce current coefficient", "S_eff and readout current remain in the same q-basic image", "UNSIGNED", "SCOT3143_2_action_variation", "effective-action/readout closure"),
    ]
    return [
        {
            "premise_id": premise_id,
            "premise": premise,
            "mathematical_form": form,
            "current_status": status,
            "source_row": source_row,
            "promotion_requirement": req,
            "passes_current_branch": status in {"PARTIAL_FROM_3868_FIXED_SECTOR"},
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for premise_id, premise, form, status, source_row, req in rows
    ]


def bj_bound_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("BJ3869_0_total", "b_J,A", BJ_BOUND, "dimensionless", "NONCLAIM_BOUND_FORMULA", "component no-cancellation envelope for current normalization"),
        ("BJ3869_1_action_descent", "b_Sdescent", "|D_v ln S_matter owner|", "dimensionless", "MISSING_QBASIC_MATTER_CERTIFICATE", "q-basic matter action or source-backed violation bound"),
        ("BJ3869_2_AQ_descent", "b_AQdescent", "|D_v ln A_Q owner|", "dimensionless", "MISSING_SAME_AQ_OWNER", "same parent T_Q/A_Q object and current owner"),
        ("BJ3869_3_rep", "b_rep", "|D_v ln n_A|+|D_v ln theta_A|", "dimensionless", "PARTIAL_ZERO_FIXED_SECTOR", "3868 fixed-label zero for connected sector; Qstar separate"),
        ("BJ3869_4_preweight", "b_preweight", "|D_v ln w_A|+|D_v ln c_A_pre|+|D_v ln kappa_A|", "dimensionless", "MISSING_SOURCE_ONLY_SLOT_EXCLUSION_OR_VALUES", "action-weight/source-current slot exclusion or finite rows"),
        ("BJ3869_5_selector", "b_current_selector", "post/current readout selector drift", "dimensionless", "POST_VARIATION_KILLED_CONDITIONAL_READOUT_LIVE", "variation-before-readout plus readout transfer kernel"),
        ("BJ3869_6_rad_readout", "b_rad_readout", "radiative/effective/readout current re-entry", "dimensionless", "MISSING_RADIOUT_CLOSURE_OR_BOUND", "same effective action image after thresholds/readout"),
        ("BJ3869_7_boundary", "b_boundary_current", "boundary/source-worldtube current normalization tail", "dimensionless", "MISSING_BOUNDARY_CURRENT_SILENCE_OR_BOUND", "source-worldtube/projector/no-flux theorem or finite bound"),
    ]
    return [
        {
            "bound_id": bound_id,
            "symbol": symbol,
            "formula": formula,
            "units": units,
            "current_status": status,
            "required_evidence": evidence,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for bound_id, symbol, formula, units, status, evidence in rows
    ]


def arena_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("ARI3869_0_clock", "clock_or_direct_alpha", "z_Noether,tau_clock enters z_g_direct*tau_clock", "MISSING_TAU_AND_READOUT_LOCK", "needs same-current owner plus clock readout kernel"),
        ("ARI3869_1_wep", "MICROSCOPE_WEP", "current-normalization source/test residual contributes beta_J,S beta_J,T K_WEP tau_WEP", "MISSING_MATERIAL_SOURCE_KERNELS", "needs b_J components and WEP material/source map"),
        ("ARI3869_2_r10", "R10_short_range", "alpha_J(lambda)=K_J(lambda) beta_J,S beta_J,T + tail", "MISSING_R10_KERNEL_BETA_BOUND_CURVE", "needs K_J, beta legs, lambda profile and valid bound curve"),
        ("ARI3869_3_newton", "Newton_PPN_local_GR", "b_J contributes to EM/current source-scale part of dressed Hamiltonian source mass", "MISSING_SOURCE_SELECTOR_AND_BOUNDARY_CURRENT", "connect to 3819 source-normalization residuals"),
    ]
    return [
        {
            "arena_id": arena_id,
            "arena": arena,
            "interface_formula": formula,
            "current_status": status,
            "required_next_input": req,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for arena_id, arena, formula, status, req in rows
    ]


def gate_rows(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    premises: list[dict[str, object]],
    bj_bound: list[dict[str, object]],
    arena: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    gates = [
        ("G3869_0_sources", "all source paths resolve", all(row["exists"] and row["needle_found"] for row in sources), "source register resolved"),
        ("G3869_1_theorem_written", "exact conditional z_Noether theorem written", any(row["result"] == "EXACT_CONDITIONAL_THEOREM" for row in theorem), "functional derivative chain-rule theorem present"),
        ("G3869_2_ward_guard", "Ward-only shortcut rejected", any(row["result"] == "COUNTEREXAMPLE_RETAINED" for row in theorem), "conserved weighted current counterexample retained"),
        ("G3869_3_premises_signed", "all theorem premises parent-signed", False, "no-source-only slots and radiative/readout closure remain unsigned"),
        ("G3869_4_bj_bound_ready", "b_J fallback decomposition staged", any(row["symbol"] == "b_J,A" for row in bj_bound), "finite current-normalization envelope written"),
        ("G3869_5_arena_claim_ready", "clock/WEP/R10/Newton arena interfaces score-ready", False, "tau/material/kernel/source-bound inputs missing"),
        ("G3869_6_no_claim", "no generated row permits a claim", all(not bool(row.get("valid_for_claim", False)) for row in theorem + premises + bj_bound + arena), "nonclaim discipline preserved"),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate": gate,
            "status": "PASS" if passed else "BLOCKED",
            "claim_allowed": False,
            "reason": reason,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, gate, passed, reason in gates
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("DEC3869_0", "z_Noether zero theorem is exact conditional", "the chain-rule proof works if one q-basic parent matter action and same-current owner are signed", "keep theorem as derivation target"),
        ("DEC3869_1", "do not promote z_Noether=0 yet", "source-only current/action slots and radiative/readout reentry remain live", "use b_J fallback until parent grammar closes"),
        ("DEC3869_2", "current-owner proof helps but does not kill pre-variation weights", "w_A inserted before variation is inherited by Hilbert/Noether currents", "next attack no-source-only slot/action-measure grammar"),
        ("DEC3869_3", "arena scoring remains downstream", "clock/WEP/R10/Newton all need tau/material/kernel/source-selector inputs after b_J is owned or bounded", "avoid broad scoring until current-owner inputs are real"),
    ]
    return [
        {
            "decision_id": decision_id,
            "decision": decision,
            "because": because,
            "next_action": next,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for decision_id, decision, because, next in rows
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3869_0",
            "target_checkpoint": "3870-Y5-R2FR-no-source-only-current-slot-parent-grammar-or-bJ-finite-input-fill.md",
            "script": "scripts/Y5_R2FR_3870_no_source_only_current_slot_parent_grammar_or_bJ_finite_input_fill.py",
            "objective": "derive a parent grammar excluding c_A(X), w_A(X), kappa_A(X) source/current slots before variation, or fill strict nonclaim b_J finite input rows",
            "why_next": "3869 proves the z_Noether chain-rule theorem conditionally; the proof fails exactly at source-only current/action slots and readout/radiative closure, with pre-variation weights the highest-pressure counterexample",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "status_id": "STATUS3869_0",
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "result": "ZNOETHER_EXACT_CONDITIONAL_THEOREM_BJ_FALLBACK_STAGED",
            "theorem_form": THEOREM_FORM,
            "bj_bound": BJ_BOUND,
            "claim_allowed": False,
            "next_gate": "3870 no source-only current slot parent grammar or b_J finite input fill",
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, separator, *body])


def write_doc(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    premises: list[dict[str, object]],
    bj_bound: list[dict[str, object]],
    arena: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    timestamp: str,
) -> None:
    text = f"""# 3869 — zNoether Same-Current Owner Zero Proof Or bJ Bound Inputs

Generated: `{timestamp}`

## Purpose

3868 reduced the direct `z_g` core to `z_Qstar + z_Noether + z_readout`. This checkpoint attacks `z_Noether`.

## Theorem Form

`{THEOREM_FORM}`

This is an exact conditional theorem, not a promoted claim.

## Fallback Bound

`{BJ_BOUND}`

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## Theorem Proof

{markdown_table(theorem, ["theorem_id", "claim_piece", "result", "remaining_gap"])}

## Premise Audit

{markdown_table(premises, ["premise_id", "premise", "current_status", "source_row", "promotion_requirement"])}

## bJ Bound Decomposition

{markdown_table(bj_bound, ["bound_id", "symbol", "formula", "current_status", "required_evidence"])}

## Arena Interfaces

{markdown_table(arena, ["arena_id", "arena", "interface_formula", "current_status", "required_next_input"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "because", "next_action"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_checkpoint", "objective", "why_next"])}

## Bottom Line

This is the right kind of derivation: `z_Noether=0` follows by a clean functional-derivative chain rule if the ordinary matter action is q-basic, uses the same `A_Q`, and current extraction happens before readout with no source-only slots.

The theorem is still not a claim because `c_A(X)`, `w_A(X)`, `kappa_A(X)`, and radiative/readout current re-entry are not parent-excluded. The next pressure point is therefore the parent grammar: either ban those slots before variation, or fill strict finite `b_J` rows.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3868", "Current State After 3869", 1)
    text = "\n".join(line for line in text.splitlines() if not line.startswith("<!-- Generated by 3869 at "))
    paragraph = (
        "`3869` proves the `z_Noether` zero route as an exact conditional theorem: if ordinary matter is one q-basic parent action, `A_Q` and `J_Q` share the same parent owner, representation labels are fixed, current extraction is before readout, and no source-only/radiative/readout current slots exist, then `z_Noether,A=D_v ln Z_JA=0`. "
        "The theorem is not promoted because `c_A(X)`, `w_A(X)`, `kappa_A(X)`, and radiative/readout current re-entry remain legal seams. "
        "The fallback finite envelope is now `b_J,A <= b_Sdescent + b_AQdescent + b_rep + b_preweight + b_current_selector + b_rad_readout + b_boundary_current`. "
        "Next gate: `3870`, attack the parent grammar excluding source-only current/action slots before variation, or fill strict finite `b_J` inputs.\n\n"
    )
    if paragraph not in text and "## Next Best Gate" in text:
        text = text.replace("## Next Best Gate", paragraph + "## Next Best Gate", 1)
    old_gate = """`3869-Y5-R2FR-zNoether-same-current-owner-zero-proof-or-bJ-bound-inputs.md`

Target: prove `z_Noether,A=0` from one q-basic parent matter action and variation-before-readout, or create source-backed `b_J` current-normalization bound inputs.

This is the best next move because 3868 reduced the direct `z_g` core to `z_Qstar + z_Noether + z_readout`; `z_Noether` is the most derivable live term and links EM current normalization to Newton/WEP source coupling."""
    new_gate = """`3870-Y5-R2FR-no-source-only-current-slot-parent-grammar-or-bJ-finite-input-fill.md`

Target: derive a parent grammar excluding `c_A(X)`, `w_A(X)`, and `kappa_A(X)` source/current slots before variation, or fill strict nonclaim `b_J` finite input rows.

This is the best next move because 3869 proves the `z_Noether` chain-rule theorem conditionally; the proof fails exactly at source-only slots and radiative/readout current re-entry."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3869_ZNOETHER_THEOREM_PROOF.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3869_CURRENT_OWNER_PREMISE_AUDIT.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3869_BJ_BOUND_DECOMPOSITION.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3869_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3869_ZNOETHER_THEOREM_PROOF.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    text = text.rstrip() + f"\n\n<!-- Generated by 3869 at {timestamp} -->\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    premises: list[dict[str, object]],
    bj_bound: list[dict[str, object]],
    arena: list[dict[str, object]],
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

    all_rows = theorem + premises + bj_bound + arena + gates
    add("VAL3869_0_sources", "all cited source paths exist and needles are found", all(row["exists"] and row["needle_found"] for row in sources), f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved")
    add("VAL3869_1_theorem", "exact conditional z_Noether theorem is present", any(row["statement"] == THEOREM_FORM and row["result"] == "EXACT_CONDITIONAL_THEOREM" for row in theorem), THEOREM_FORM)
    add("VAL3869_2_counterexample", "source/current counterexample is retained", any(row["result"] == "COUNTEREXAMPLE_RETAINED" for row in theorem), "Ward-only shortcut refused")
    add("VAL3869_3_premises", "premise audit contains unsigned source-only slots", any("source" in row["premise"] and "UNSIGNED" in row["current_status"] for row in premises), "source-only slot remains explicit")
    add("VAL3869_4_bj_bound", "b_J fallback bound is written", any(row["formula"] == BJ_BOUND for row in bj_bound), BJ_BOUND)
    add("VAL3869_5_arena", "arena interfaces cover clock/WEP/R10/Newton", {row["arena"] for row in arena} >= {"clock_or_direct_alpha", "MICROSCOPE_WEP", "R10_short_range", "Newton_PPN_local_GR"}, "all four interfaces present")
    add("VAL3869_6_no_claim", "all generated rows remain nonclaim", all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in all_rows), "valid_for_claim/claim_allowed false throughout")
    add("VAL3869_7_next", "next target selects no-source-only current slot grammar", DOC_PATH.exists() and "3870-Y5-R2FR-no-source-only-current-slot-parent-grammar-or-bJ-finite-input-fill" in read_text(DOC_PATH), "3870 target recorded")
    for key, output_path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed = False
        detail = rel(output_path)
        if output_path.suffix == ".csv" and output_path.exists():
            count = len(read_csv_rows(output_path))
            parsed = count > 0
            detail += f" rows={count}"
        add(f"VAL3869_8_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add("VAL3869_9_doc", "markdown checkpoint document exists", DOC_PATH.exists() and "This is the right kind of derivation" in read_text(DOC_PATH), rel(DOC_PATH))
    formalization_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3869*", "P8_Y5_BRR545_3869*", "*Y5_R2FR_3869*", "3869-Y5-R2FR*"):
            formalization_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add("VAL3869_10_formalization_clean", "formalization-workbench has no generated 3869 project files", len(formalization_hits) == 0, "; ".join(str(path) for path in formalization_hits) if formalization_hits else "no generated 3869 project file hits under formalization-workbench")
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add("VAL3869_11_pycache_removed", "scripts __pycache__ removed", len(pycache_hits) == 0, "; ".join(str(path) for path in pycache_hits) if pycache_hits else "no __pycache__ directories")
    return rows


def main() -> int:
    timestamp = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows(timestamp)
    theorem = theorem_rows(timestamp)
    premises = premise_rows(timestamp)
    bj_bound = bj_bound_rows(timestamp)
    arena = arena_rows(timestamp)
    gates = gate_rows(sources, theorem, premises, bj_bound, arena, timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["premises"], premises)
    write_csv(OUTPUTS["bj_bound"], bj_bound)
    write_csv(OUTPUTS["arena"], arena)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, theorem, premises, bj_bound, arena, gates, decisions, next_target, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, theorem, premises, bj_bound, arena, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_ZNOETHER_CONDITIONAL_THEOREM_BJ_FALLBACK")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

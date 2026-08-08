from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3870"
BRANCH = "MTS_R2FR_Y5_NO_SOURCE_ONLY_CURRENT_SLOT_PARENT_GRAMMAR_OR_BJ_FINITE_INPUT_FILL_3870"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3870-Y5-R2FR-no-source-only-current-slot-parent-grammar-or-bJ-finite-input-fill.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

CSV_3869_NEXT = OUT / "P8_Y5_R2FR_3869_NEXT_TARGET.csv"
CSV_3869_PREMISES = OUT / "P8_Y5_R2FR_3869_CURRENT_OWNER_PREMISE_AUDIT.csv"
CSV_3869_BJ = OUT / "P8_Y5_R2FR_3869_BJ_BOUND_DECOMPOSITION.csv"
CSV_3869_THEOREM = OUT / "P8_Y5_R2FR_3869_ZNOETHER_THEOREM_PROOF.csv"
CSV_1065_GRAMMAR = OUT / "P8_Y5_R10_1065_PARENT_GRAMMAR_AUDIT.csv"
CSV_1065_ALLOWED = OUT / "P8_Y5_R10_1065_ALLOWED_ACTION_GRAMMAR.csv"
CSV_1065_ZERO = OUT / "P8_Y5_R10_1065_WA_THEOREM_ZERO_CLAUSES.csv"
CSV_1066_SOURCE = OUT / "P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv"
CSV_1078_OBJECT = OUT / "P8_Y5_R10_1078_OBJECT_LANGUAGE_PROOF_ATTEMPT.csv"
CSV_1078_MEASURE = OUT / "P8_Y5_R10_1078_ACTION_MEASURE_PROOF_ATTEMPT.csv"
CSV_1078_COUNTER = OUT / "P8_Y5_R10_1078_COUNTEREXAMPLE_KILL_MATRIX.csv"
CSV_1079_CURRENT = OUT / "P8_Y5_R10_1079_NARROW_CURRENT_OWNER_THEOREM_ATTEMPT.csv"
CSV_1214_NO_SLOT = OUT / "P8_Y5_R10_1214_NO_SOURCE_ONLY_SLOT_SIGNATURE_AUDIT.csv"
CSV_1220_TYPED = OUT / "P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv"
CSV_1046_VERTEX = OUT / "P8_Y5_R10_1046_FORBIDDEN_VERTEX_CATALOG.csv"
CSV_1387_AUDIT = OUT / "P8_Y5_R10_1387_ACTION_WEIGHT_EXCLUSION_AUDIT.csv"
CSV_1387_FILL = OUT / "P8_Y5_R10_1387_DELTA_W_SOURCE_BETA_FIRST_FILL.csv"
CSV_1388_VALIDATOR = OUT / "P8_Y5_R10_1388_DELTA_W_SOURCE_BETA_VALIDATOR.csv"
CSV_3819_SOURCE = OUT / "P8_Y5_R2FR_3819_FINITE_SOURCE_NORMALIZATION_RESIDUALS.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3870_SOURCE_REGISTER.csv",
    "theorem": OUT / "P8_Y5_R2FR_3870_NO_SOURCE_SLOT_THEOREM.csv",
    "classification": OUT / "P8_Y5_R2FR_3870_SOURCE_SLOT_CLASSIFICATION.csv",
    "bj_inputs": OUT / "P8_Y5_R2FR_3870_BJ_FINITE_INPUT_ROWS.csv",
    "arena": OUT / "P8_Y5_R2FR_3870_ARENA_PROPAGATION_ROWS.csv",
    "gates": OUT / "P8_Y5_R2FR_3870_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3870_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3870_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3870_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3870_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3870_00_3869_next", CSV_3869_NEXT, "NEXT3869_0", "3869 selected no-source-only slot grammar"),
    ("SRC3870_01_3869_premises", CSV_3869_PREMISES, "PREM3869_3_no_source_only_current_slot", "3869 source-only current premise"),
    ("SRC3870_02_3869_bj", CSV_3869_BJ, "BJ3869_4_preweight", "3869 b_J source-slot component"),
    ("SRC3870_03_3869_theorem", CSV_3869_THEOREM, "ZNT3869_4_counterexample", "3869 counterexample guard"),
    ("SRC3870_04_1065_grammar", CSV_1065_GRAMMAR, "PGG1065_5_verdict", "parent grammar audit verdict"),
    ("SRC3870_05_1065_allowed", CSV_1065_ALLOWED, "AAG1065_4_source_only_species_scalar", "allowed action grammar source-only slot"),
    ("SRC3870_06_1065_zero", CSV_1065_ZERO, "WTZ1065_4_verdict", "w_A theorem-zero clauses"),
    ("SRC3870_07_1066_source", CSV_1066_SOURCE, "SSE1066_5_verdict", "source scalar exclusion lemma"),
    ("SRC3870_08_1078_object", CSV_1078_OBJECT, "OL1078_4_verdict", "object-language proof attempt"),
    ("SRC3870_09_1078_measure", CSV_1078_MEASURE, "AM1078_4_verdict", "action-measure proof attempt"),
    ("SRC3870_10_1078_counter", CSV_1078_COUNTER, "CEK1078_0_species_action_weight", "counterexample kill matrix"),
    ("SRC3870_11_1079_current", CSV_1079_CURRENT, "NCO1079_5_species_action_weight", "pre-variation weights survive current owner"),
    ("SRC3870_12_1214_no_slot", CSV_1214_NO_SLOT, "NSS1214_5_verdict", "no-source-only slot signature audit"),
    ("SRC3870_13_1220_typed", CSV_1220_TYPED, "PTOL1220_3_source_weight_exclusion", "parent typed signature source-weight clause"),
    ("SRC3870_14_1046_vertex", CSV_1046_VERTEX, "FV1046_6_source_only_weight", "forbidden source-only weight vertex"),
    ("SRC3870_15_1387_audit", CSV_1387_AUDIT, "AWE1387_7_verdict", "action-weight exclusion audit"),
    ("SRC3870_16_1387_fill", CSV_1387_FILL, "DWB1387_6_first_fill_verdict", "Delta_w/beta first-fill rows"),
    ("SRC3870_17_1388_validator", CSV_1388_VALIDATOR, "DWV1388_7_verdict", "Delta_w validator verdict"),
    ("SRC3870_18_3819_source", CSV_3819_SOURCE, "R3819_6_total", "source normalization residual total"),
]

THEOREM = (
    "If the parent ordinary-matter grammar is declared before readout with allowed arguments "
    "{g_obs/e_obs, matter fields, parent connections/currents, fixed representation data, measured matter constants, universal constants} "
    "and one parent action-scale/measure owner, then source-only slots c_A(X), w_A(X), and kappa_A(X) are ill-typed unless they are real fields/currents, q-basic common calibration, or retained residuals."
)
BJ_REFINED = (
    "b_J,A <= b_Sdescent + b_AQdescent + b_rep + b_slot[c_A,w_A,kappa_A] + b_readout + b_rad + b_boundary"
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
                "claim_use": "nonclaim_no_source_only_slot_theorem_or_bJ_input_fill",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "NST3870_0_allowed_domain",
            "positive parent matter grammar",
            "Allowed Arg(S_matter) = geometry/coframe, matter fields, parent connections/currents, fixed representations, measured constants, universal constants",
            "This is the typed domain in which ordinary matter may couple before readout.",
            "CONDITIONAL_DOMAIN_CONTRACT",
            "parent primitive constructor list not derived",
        ),
        (
            "NST3870_1_forbidden_source_slots",
            "source-only slots",
            "c_A(X), w_A(X), kappa_A(X) are forbidden when they only change active source/current strength and carry no field/current/representation/readout type",
            THEOREM,
            "EXACT_IF_PARENT_GRAMMAR_SIGNED",
            "not parent-signed by current corpus",
        ),
        (
            "NST3870_2_common_factor_policy",
            "common calibration exception",
            "w_A=w_* for all sectors can be calibration only if derivative/source/range/frame/material silent",
            "A common constant is not a WEP/source residual; any relative, time/range/frame/domain/species dependence is physical.",
            "GUARD_EXACT",
            "commonness and derivative silence not proved",
        ),
        (
            "NST3870_3_field_or_current_exception",
            "real field/current exception",
            "if c_A,w_A,kappa_A are generated by real parent fields/currents, they are not erased; they become explicit residual couplings",
            "The theorem forbids hidden inert slots, not real dynamics.",
            "RESIDUAL_EXCEPTION_RETAINED",
            "requires finite source rows if present",
        ),
        (
            "NST3870_4_current_owner_limit",
            "current owner limit",
            "variation-before-readout kills post-variation selectors but cannot kill weights inserted into S_matter before variation",
            "Hilbert/Noether variation inherits pre-variation w_A.",
            "COUNTEREXAMPLE_SURVIVES",
            "needs object-language/action-measure owner",
        ),
        (
            "NST3870_5_verdict",
            "no-source-only slot theorem status",
            "the typed exclusion theorem is sharp but remains conditional; finite b_J rows are required until parent grammar/action-measure owner is derived",
            "3870 does not claim local-GR/source coupling closure.",
            "THEOREM_CONDITIONAL_FINITE_ROWS_REQUIRED",
            "next target is action-measure owner or b_J first sourced rows",
        ),
    ]
    return [
        {
            "theorem_id": theorem_id,
            "claim_piece": claim_piece,
            "formal_statement": statement,
            "argument": argument,
            "result": result,
            "remaining_gap": gap,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for theorem_id, claim_piece, statement, argument, result, gap in rows
    ]


def classification_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("CLS3870_0_w_common", "w_*", "common action/source factor", "CALIBRATION_ONLY_IF_SILENT", "all sectors share the same constant and all t/r/range/frame/material derivatives vanish", "MISSING_COMMONNESS_AND_SILENCE_PROOF"),
        ("CLS3870_1_w_relative", "Delta_w_A", "relative pre-variation action/source multiplier", "LIVE_COUNTERMODEL", "parent no-source-slot grammar or source-backed value/bound", "MISSING_DELTA_W_A_VALUE_OR_ZERO"),
        ("CLS3870_2_w_phi", "beta_w_A", "field-dependent action/source multiplier", "LIVE_FINITE_FORCE_INPUT", "canonical field normalization plus source/test beta functions", "MISSING_BETA_WEIGHT_FUNCTIONS"),
        ("CLS3870_3_c_pre", "c_A_pre", "pre-variation current/source normalization", "LIVE_COUNTERMODEL", "same-current owner plus no source-only current slot", "MISSING_C_PRE_ZERO_OR_BOUND"),
        ("CLS3870_4_c_post", "c_A_post", "post-variation current/readout rescale", "KILLED_FOR_PARENT_CURRENT_CONDITIONAL", "variation-before-readout and readout kernel", "READOUT_KERNEL_STILL_MISSING"),
        ("CLS3870_5_kappa", "kappa_A", "active-source selector or source-current coefficient", "LIVE_COUNTERMODEL", "source selector grammar exclusion or finite source vector", "MISSING_KAPPA_ZERO_OR_BOUND"),
        ("CLS3870_6_marker", "marker/domain/boundary hidden label", "smuggled source-only coefficient", "LIVE_UNTIL_DOMAIN_SEALED", "no marker/domain/boundary extension theorem", "MISSING_NO_MARKER_DOMAIN_PROOF"),
    ]
    return [
        {
            "class_id": class_id,
            "slot": slot,
            "meaning": meaning,
            "status": status,
            "zero_or_promotion_requirement": requirement,
            "finite_input_status": finite_status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for class_id, slot, meaning, status, requirement, finite_status in rows
    ]


def bj_input_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("BJF3870_0_total", "b_J,A", BJ_REFINED, "dimensionless", "nonclaim envelope", "requires every component zero or numeric/source-backed"),
        ("BJF3870_1_b_slot", "b_slot[c_A,w_A,kappa_A]", "|D ln c_A_pre|+|D ln w_A|+|D ln kappa_A|", "dimensionless", "MISSING_SOURCE_ONLY_SLOT_EXCLUSION_OR_VALUES", "main 3870 live source-slot pack"),
        ("BJF3870_2_Delta_w_A", "Delta_w_A", "w_A/w_*-1", "dimensionless", "FIRST_FILL_ROW_READY_VALUE_MISSING", "material/source class value or upper bound"),
        ("BJF3870_3_beta_w_source", "beta_w_source", "partial_phi ln w_source(phi)", "canonical beta units", "MISSING_SOURCE_BETA_WEIGHT_FUNCTION", "canonical field and source weight function"),
        ("BJF3870_4_beta_w_test", "beta_w_test", "partial_phi ln w_test(phi)", "canonical beta units", "MISSING_TEST_BETA_WEIGHT_FUNCTION", "test material action/composition map"),
        ("BJF3870_5_c_A_pre", "c_A_pre", "pre-variation current/source coefficient", "dimensionless", "MISSING_CURRENT_SLOT_ZERO_OR_VALUE", "source/test current coefficient value or parent exclusion theorem"),
        ("BJF3870_6_kappa_A", "kappa_A", "active-source selector coefficient", "dimensionless", "MISSING_SOURCE_SELECTOR_ZERO_OR_VALUE", "source-current grammar theorem or finite source vector"),
        ("BJF3870_7_no_absorb", "absorption_guard", "only universal derivative-silent common factors may enter G_N calibration", "boolean+derivatives", "GUARD_READY_INPUTS_MISSING", "partial_t,r,A,lambda,frame ln slot = 0 and Delta_w_A=0"),
        ("BJF3870_8_kernel", "arena_kernel", "K_Arena for WEP/R10/PPN/clock/orbital projection", "arena units", "MISSING_ARENA_PROJECTIONS", "arena-specific kernel and source/material map"),
    ]
    return [
        {
            "input_id": input_id,
            "symbol": symbol,
            "formula": formula,
            "units": units,
            "current_status": status,
            "required_evidence": evidence,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for input_id, symbol, formula, units, status, evidence in rows
    ]


def arena_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("AP3870_0_Newton", "Newton/source normalization", "relative source slots alter M_H_ref or G_ref*M_H_ref unless common and derivative-silent", "BLOCKED_SOURCE_NORMALIZATION_TOTAL", "R3819_6_total plus BJF3870 rows"),
        ("AP3870_1_WEP", "WEP/MICROSCOPE", "Delta_w_A, beta_w_source/test, c_A_pre and kappa_A create composition source/test response", "BLOCKED_MATERIAL_SOURCE_MAP", "material/source classes and WEP kernel"),
        ("AP3870_2_R10", "R10_short_range", "finite source slot exchange must score as K(lambda) beta_source beta_test plus tail", "BLOCKED_KERNEL_BETA_BOUND_CURVE", "R10 kernel, beta legs, valid alpha(lambda) bound"),
        ("AP3870_3_PPN", "PPN/local_GR", "source slot residual propagates into source vector and Bianchi/current closure residuals", "BLOCKED_SOURCE_VECTOR", "weak-field source vector, boundary/current closure"),
        ("AP3870_4_clock", "clocks/readout", "common standards may hide readout normalization unless derivative/readout silence is proved", "BLOCKED_READOUT_SILENCE", "clock material/readout transfer kernel"),
    ]
    return [
        {
            "arena_id": arena_id,
            "arena": arena,
            "propagation_rule": rule,
            "current_status": status,
            "required_next_input": req,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for arena_id, arena, rule, status, req in rows
    ]


def gate_rows(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    classification: list[dict[str, object]],
    bj_inputs: list[dict[str, object]],
    arena: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    gates = [
        ("G3870_0_sources", "all source paths resolve", all(row["exists"] and row["needle_found"] for row in sources), "source register resolved"),
        ("G3870_1_theorem", "typed no-source-slot theorem is written", any(row["result"] == "EXACT_IF_PARENT_GRAMMAR_SIGNED" for row in theorem), "exact conditional theorem present"),
        ("G3870_2_parent_signed", "parent grammar/action-measure owner is signed", False, "current corpus marks object language/action measure unsigned"),
        ("G3870_3_countermodels", "live source-slot countermodels are preserved", any(row["status"] == "LIVE_COUNTERMODEL" for row in classification), "w_A/c_A/kappa_A retained unless theorem-zero or sourced"),
        ("G3870_4_finite_rows", "strict b_J finite input rows are staged", {"Delta_w_A", "c_A_pre", "kappa_A"} <= {row["symbol"] for row in bj_inputs}, "main source-only slots have explicit rows"),
        ("G3870_5_arena", "arena propagation rows cover target tests", {row["arena"] for row in arena} >= {"Newton/source normalization", "WEP/MICROSCOPE", "R10_short_range", "PPN/local_GR", "clocks/readout"}, "Newton/WEP/R10/PPN/clock covered"),
        ("G3870_6_no_claim", "no generated row permits a claim", all(not bool(row.get("valid_for_claim", False)) for row in theorem + classification + bj_inputs + arena), "nonclaim discipline preserved"),
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
        ("DEC3870_0", "do not claim no-source-slot closure", "the typed theorem depends on a parent grammar/action-measure certificate still unsigned", "keep theorem conditional"),
        ("DEC3870_1", "treat common factors separately from relative factors", "only universal derivative-silent common factors are calibration; relative/source/range dependence is physics", "keep absorption guard mandatory"),
        ("DEC3870_2", "collapse c_A/w_A/kappa_A into one b_slot pack", "they are the same source-only coefficient problem in different clothing before variation", "use BJF3870 rows for finite branch"),
        ("DEC3870_3", "next attack action-measure owner or source rows", "action-measure owner is the cleanest route to kill w_A; otherwise values/bounds are needed", "3871 action-measure owner or b_J first source rows"),
    ]
    return [
        {
            "decision_id": decision_id,
            "decision": decision,
            "because": because,
            "next_action": next_action,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for decision_id, decision, because, next_action in rows
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3870_0",
            "target_checkpoint": "3871-Y5-R2FR-parent-action-measure-owner-or-bJ-first-source-rows.md",
            "script": "scripts/Y5_R2FR_3871_parent_action_measure_owner_or_bJ_first_source_rows.py",
            "objective": "derive one parent action-scale/measure owner that kills relative w_A/c_A/kappa_A source slots, or fill the first strict source-backed b_J finite input rows",
            "why_next": "3870 gives the typed no-source-slot theorem but cannot parent-sign the grammar; action-measure ownership is the highest-pressure missing clause and the finite rows are now explicit",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "status_id": "STATUS3870_0",
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "result": "TYPED_NO_SOURCE_SLOT_THEOREM_CONDITIONAL_BJ_FINITE_ROWS_STAGED",
            "theorem": THEOREM,
            "bj_bound": BJ_REFINED,
            "claim_allowed": False,
            "next_gate": "3871 parent action-measure owner or b_J first source rows",
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
    classification: list[dict[str, object]],
    bj_inputs: list[dict[str, object]],
    arena: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    timestamp: str,
) -> None:
    text = f"""# 3870 — No Source-Only Current Slot Parent Grammar Or bJ Finite Input Fill

Generated: `{timestamp}`

## Purpose

3869 proved `z_Noether=0` conditionally and showed the proof fails at source-only current/action slots. 3870 attacks those slots directly.

## Typed Theorem

`{THEOREM}`

This is exact if the parent grammar/action-measure owner is signed. It is not currently promoted.

## Refined bJ Envelope

`{BJ_REFINED}`

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## No-Source-Slot Theorem

{markdown_table(theorem, ["theorem_id", "claim_piece", "result", "remaining_gap"])}

## Slot Classification

{markdown_table(classification, ["class_id", "slot", "meaning", "status", "finite_input_status"])}

## bJ Finite Input Rows

{markdown_table(bj_inputs, ["input_id", "symbol", "formula", "current_status", "required_evidence"])}

## Arena Propagation

{markdown_table(arena, ["arena_id", "arena", "propagation_rule", "current_status", "required_next_input"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "because", "next_action"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_checkpoint", "objective", "why_next"])}

## Bottom Line

3870 compresses the source-coupling problem: `c_A(X)`, `w_A(X)`, and `kappa_A(X)` are not three unrelated holes. Before variation they are the same forbidden active-source coefficient unless carried by real parent fields/currents, q-basic common calibration, or retained as finite residuals.

The theorem is sharp but still conditional because the parent object-language/action-measure owner is unsigned. The next best strike is the action-measure owner; if that fails, the `b_J` finite rows are now ready for source-backed filling.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3869", "Current State After 3870", 1)
    text = "\n".join(line for line in text.splitlines() if not line.startswith("<!-- Generated by 3870 at "))
    paragraph = (
        "`3870` compresses the source-only slot problem. "
        "It proves an exact conditional typed theorem: once the parent ordinary-matter grammar is fixed before readout and has one action-scale/measure owner, `c_A(X)`, `w_A(X)`, and `kappa_A(X)` are ill-typed active-source coefficients unless they are real parent fields/currents, q-basic common calibration, or retained residuals. "
        "The theorem is not promoted because the parent grammar/action-measure certificate remains unsigned. "
        "The finite fallback is now explicit: `b_J,A <= b_Sdescent + b_AQdescent + b_rep + b_slot[c_A,w_A,kappa_A] + b_readout + b_rad + b_boundary`, with strict rows for `Delta_w_A`, `beta_w_source`, `beta_w_test`, `c_A_pre`, `kappa_A`, absorption guards, and arena kernels. "
        "Next gate: `3871`, derive the parent action-measure owner or fill first source-backed `b_J` rows.\n\n"
    )
    if paragraph not in text and "## Next Best Gate" in text:
        text = text.replace("## Next Best Gate", paragraph + "## Next Best Gate", 1)
    old_gate = """`3870-Y5-R2FR-no-source-only-current-slot-parent-grammar-or-bJ-finite-input-fill.md`

Target: derive a parent grammar excluding `c_A(X)`, `w_A(X)`, and `kappa_A(X)` source/current slots before variation, or fill strict nonclaim `b_J` finite input rows.

This is the best next move because 3869 proves the `z_Noether` chain-rule theorem conditionally; the proof fails exactly at source-only slots and radiative/readout current re-entry."""
    new_gate = """`3871-Y5-R2FR-parent-action-measure-owner-or-bJ-first-source-rows.md`

Target: derive one parent action-scale/measure owner that kills relative `w_A/c_A/kappa_A` source slots, or fill the first strict source-backed `b_J` finite input rows.

This is the best next move because 3870 gives the typed no-source-slot theorem but cannot parent-sign the grammar; action-measure ownership is the highest-pressure missing clause and the finite rows are now explicit."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3870_NO_SOURCE_SLOT_THEOREM.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3870_SOURCE_SLOT_CLASSIFICATION.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3870_BJ_FINITE_INPUT_ROWS.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3870_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3870_NO_SOURCE_SLOT_THEOREM.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    text = text.rstrip() + f"\n\n<!-- Generated by 3870 at {timestamp} -->\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    classification: list[dict[str, object]],
    bj_inputs: list[dict[str, object]],
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

    all_rows = theorem + classification + bj_inputs + arena + gates
    add("VAL3870_0_sources", "all cited source paths exist and needles are found", all(row["exists"] and row["needle_found"] for row in sources), f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved")
    add("VAL3870_1_theorem", "typed no-source-slot theorem is present", any(row["argument"] == THEOREM and row["result"] == "EXACT_IF_PARENT_GRAMMAR_SIGNED" for row in theorem), THEOREM)
    add("VAL3870_2_parent_block", "parent grammar signature remains blocked", any(row["gate_id"] == "G3870_2_parent_signed" and row["status"] == "BLOCKED" for row in gates), "no parent grammar/action-measure promotion")
    add("VAL3870_3_slots", "slot classification covers c_A, w_A and kappa_A", {"Delta_w_A", "beta_w_A", "c_A_pre", "kappa_A"} <= {row["slot"] for row in classification}, "source-only slot family classified")
    add("VAL3870_4_bj_inputs", "finite b_J rows cover source-only slots", {"Delta_w_A", "beta_w_source", "beta_w_test", "c_A_pre", "kappa_A"} <= {row["symbol"] for row in bj_inputs}, "strict source-backed input rows staged")
    add("VAL3870_5_arena", "arena propagation covers major local tests", {row["arena"] for row in arena} >= {"Newton/source normalization", "WEP/MICROSCOPE", "R10_short_range", "PPN/local_GR", "clocks/readout"}, "local test propagation present")
    add("VAL3870_6_no_claim", "all generated rows remain nonclaim", all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in all_rows), "valid_for_claim/claim_allowed false throughout")
    add("VAL3870_7_next", "next target selects action-measure owner or b_J source rows", DOC_PATH.exists() and "3871-Y5-R2FR-parent-action-measure-owner-or-bJ-first-source-rows" in read_text(DOC_PATH), "3871 target recorded")
    for key, output_path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed = False
        detail = rel(output_path)
        if output_path.suffix == ".csv" and output_path.exists():
            count = len(read_csv_rows(output_path))
            parsed = count > 0
            detail += f" rows={count}"
        add(f"VAL3870_8_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add("VAL3870_9_doc", "markdown checkpoint document exists", DOC_PATH.exists() and "3870 compresses the source-coupling problem" in read_text(DOC_PATH), rel(DOC_PATH))
    formalization_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3870*", "P8_Y5_BRR545_3870*", "*Y5_R2FR_3870*", "3870-Y5-R2FR*"):
            formalization_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add("VAL3870_10_formalization_clean", "formalization-workbench has no generated 3870 project files", len(formalization_hits) == 0, "; ".join(str(path) for path in formalization_hits) if formalization_hits else "no generated 3870 project file hits under formalization-workbench")
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add("VAL3870_11_pycache_removed", "scripts __pycache__ removed", len(pycache_hits) == 0, "; ".join(str(path) for path in pycache_hits) if pycache_hits else "no __pycache__ directories")
    return rows


def main() -> int:
    timestamp = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows(timestamp)
    theorem = theorem_rows(timestamp)
    classification = classification_rows(timestamp)
    bj_inputs = bj_input_rows(timestamp)
    arena = arena_rows(timestamp)
    gates = gate_rows(sources, theorem, classification, bj_inputs, arena, timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["classification"], classification)
    write_csv(OUTPUTS["bj_inputs"], bj_inputs)
    write_csv(OUTPUTS["arena"], arena)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, theorem, classification, bj_inputs, arena, gates, decisions, next_target, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, theorem, classification, bj_inputs, arena, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_TYPED_NO_SOURCE_SLOT_CONDITIONAL_BJ_ROWS")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

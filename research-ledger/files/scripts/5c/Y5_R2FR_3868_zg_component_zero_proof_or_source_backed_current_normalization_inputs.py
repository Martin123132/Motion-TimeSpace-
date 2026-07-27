from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3868"
BRANCH = "MTS_R2FR_Y5_ZG_COMPONENT_ZERO_PROOF_OR_SOURCE_BACKED_CURRENT_NORMALIZATION_INPUTS_3868"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3868-Y5-R2FR-zg-component-zero-proof-or-source-backed-current-normalization-inputs.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

CSV_3867_NEXT = OUT / "P8_Y5_R2FR_3867_NEXT_TARGET.csv"
CSV_3867_CANDIDATES = OUT / "P8_Y5_R2FR_3867_SOURCE_BACKED_CANDIDATE_ROWS.csv"
CSV_3867_VALIDATION = OUT / "P8_Y5_BRR545_3867_VALIDATION.csv"
CSV_3680_ZG = OUT / "P8_Y5_R2FR_3680_ZG_COMPONENT_DECOMPOSITION_ROWS.csv"
CSV_3680_ZERO = OUT / "P8_Y5_R2FR_3680_ZG_ZERO_THEOREM_AUDIT.csv"
CSV_3508_ZG = OUT / "P8_Y5_R2FR_3508_ZG_BETA_SOURCE_REDUCTION.csv"
CSV_3143_CURRENT = OUT / "P8_Y5_R2FR_3143_SAME_CURRENT_OWNER_THEOREM.csv"
CSV_1079_CURRENT = OUT / "P8_Y5_R10_1079_NARROW_CURRENT_OWNER_THEOREM_ATTEMPT.csv"
DOC_1100_TQ = PCW / "1100-Y5-R10-parent-TQ-owner-fixed-charge-lattice-and-gauge-norm-signature.md"
CSV_989_EMLOCK = OUT / "P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv"
CSV_3863_SLOT = OUT / "P8_Y5_R2FR_3863_CHARGE_CURRENT_SLOT_AUDIT.csv"
CSV_3863_BOUND = OUT / "P8_Y5_R2FR_3863_EM_SOURCE_SCALE_BOUND.csv"
CSV_3819_SOURCE = OUT / "P8_Y5_R2FR_3819_FINITE_SOURCE_NORMALIZATION_RESIDUALS.csv"
CSV_3817_BIANCHI = OUT / "P8_Y5_R2FR_3817_BIANCHI_WARD_CURRENT_AUDIT.csv"
CSV_1388_DW = OUT / "P8_Y5_R10_1388_DELTA_W_SOURCE_BETA_VALIDATOR.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3868_SOURCE_REGISTER.csv",
    "component_law": OUT / "P8_Y5_R2FR_3868_ZG_COMPONENT_LAW.csv",
    "zero_proof": OUT / "P8_Y5_R2FR_3868_ZG_ZERO_PROOF_AUDIT.csv",
    "reduced_core": OUT / "P8_Y5_R2FR_3868_REDUCED_ZG_CORE_ROWS.csv",
    "bound_inputs": OUT / "P8_Y5_R2FR_3868_CURRENT_NORMALIZATION_BOUND_INPUT_REQUIREMENTS.csv",
    "gates": OUT / "P8_Y5_R2FR_3868_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3868_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3868_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3868_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3868_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3868_00_3867_next", CSV_3867_NEXT, "NEXT3867_0", "3867 selected z_g component proof as next gate"),
    ("SRC3868_01_3867_candidates", CSV_3867_CANDIDATES, "CAND3867_3_zg_decomposition", "3867 imported z_g decomposition candidate"),
    ("SRC3868_02_3867_validation", CSV_3867_VALIDATION, "PASS", "previous validation pass"),
    ("SRC3868_03_3680_components", CSV_3680_ZG, "ZGD3680_1_core_decomposition", "3680 z_g component decomposition"),
    ("SRC3868_04_3680_zero", CSV_3680_ZERO, "ZG3680_7_verdict", "3680 z_g zero verdict"),
    ("SRC3868_05_3508_reduction", CSV_3508_ZG, "CSR3508_0_z_g", "3508 current-owner reduction"),
    ("SRC3868_06_3143_current", CSV_3143_CURRENT, "SCOT3143_3_same_current_owner", "same-current owner theorem"),
    ("SRC3868_07_1079_post_current", CSV_1079_CURRENT, "NCO1079_4_current_rescaling", "narrow current owner post-variation rescale result"),
    ("SRC3868_08_1079_weight", CSV_1079_CURRENT, "NCO1079_5_species_action_weight", "pre-variation weight counterexample"),
    ("SRC3868_09_1100_lattice", DOC_1100_TQ, "TQS1100_1_fixed_charge_lattice", "fixed charge lattice and Qstar gap"),
    ("SRC3868_10_989_current", CSV_989_EMLOCK, "ELA989_2_current_owner", "EM lock current owner unsigned"),
    ("SRC3868_11_3863_slot", CSV_3863_SLOT, "CCA3863_2_same_current", "3863 same-current slot audit"),
    ("SRC3868_12_3863_bound", CSV_3863_BOUND, "ESB3863_1_current_drift", "current drift bound structure"),
    ("SRC3868_13_3819_source", CSV_3819_SOURCE, "R3819_6_total", "source-normalization residual total"),
    ("SRC3868_14_3817_bianchi", CSV_3817_BIANCHI, "BWA3817_2_EM_exchange", "Bianchi/EM exchange source-current audit"),
    ("SRC3868_15_1388_delta_w", CSV_1388_DW, "DWV1388_7_verdict", "Delta_w finite-source validator"),
]

CORE_LAW = "z_g_core,A = z_Qstar + z_lattice,A + z_Noether,A + z_cA_post,A + z_readout,A"
SOURCE_LAW = "z_source,A = z_g_core,A + z_Delta_w,A + z_Karena,A + z_nonHilbert,A"
REDUCED_DIRECT_LAW = "z_g_direct,A = z_Qstar + z_Noether,A + z_readout,A"


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
                "claim_use": "nonclaim_zg_component_zero_proof",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def component_law_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "ZC3868_0_product_decomposition",
            "z_g_core,A",
            CORE_LAW,
            "EXACT_LOG_DERIVATIVE_DECOMPOSITION",
            "If g_J,A = Qstar*n_A*Z_JA*c_A*R_A, then D ln g_J,A is the displayed sum.",
            "bookkeeping_identity",
            "none",
        ),
        (
            "ZC3868_1_base_unit",
            "z_Qstar",
            "z_Qstar = D_Xhat ln Qstar",
            "LIVE_BASE_UNIT_OR_GENERATOR_NORM_TERM",
            "Zero only if the parent fixes a nonrescalable charge unit/generator norm/level; compact U(1) alone does not fix this continuous normalization.",
            "not_zero_proved",
            "TQ/gauge norm owner or source-backed bound",
        ),
        (
            "ZC3868_2_lattice",
            "z_lattice,A",
            "z_lattice,A = D_Xhat ln n_A = 0 in a fixed representation sector",
            "DERIVED_FIXED_SECTOR_ZERO",
            "A smooth vertical derivative of an integer/representation label on a connected fixed sector vanishes; this fixes relative charge labels, not Qstar.",
            "component_zero_conditional",
            "fixed representation sector certificate",
        ),
        (
            "ZC3868_3_noether",
            "z_Noether,A",
            "z_Noether,A = D_Xhat ln Z_JA",
            "EXACT_CONDITIONAL_CHAIN_RULE_NOT_PARENT_SIGNED",
            "If the same q-basic parent matter action owns A_Q and J_Q before readout, then D_v J_Q=0; unsigned no c_A/w_A/source-marker/radiative reentry clauses keep this live.",
            "not_zero_proved",
            "same-current owner parent certificate or b_J bound",
        ),
        (
            "ZC3868_4_post_current",
            "z_cA_post,A",
            "z_cA_post,A = D_Xhat ln c_A",
            "KILLED_FOR_PARENT_CURRENT_IF_VARIATION_BEFORE_READOUT",
            "A post-variation current rescale cannot alter the parent current that varied the action; it must be classified as readout/calibration unless inserted before variation.",
            "component_zero_for_parent_current_conditional",
            "variation-before-readout certificate; otherwise move into z_readout/source tail",
        ),
        (
            "ZC3868_5_readout",
            "z_readout,A",
            "z_readout,A = D_Xhat ln R_A",
            "LIVE_READOUT_TRANSFER_TERM",
            "Clock/source readout can still map the parent current into a different measured normalization unless downstream quotient/readout stability is signed.",
            "not_zero_proved",
            "readout transfer kernel or theorem-zero",
        ),
        (
            "ZC3868_6_source_extension",
            "z_source,A",
            SOURCE_LAW,
            "SOURCE_ARENA_EXTENSION_LIVE",
            "WEP/R10/Newton source arenas see pre-action weights, arena kernels and non-Hilbert/source tails beyond the direct alpha-current leg.",
            "not_zero_proved",
            "Delta_w, K_arena and nonHilbert source rows",
        ),
    ]
    return [
        {
            "component_id": component_id,
            "symbol": symbol,
            "formula": formula,
            "result": result,
            "proof_or_reason": proof_or_reason,
            "zero_status": zero_status,
            "promotion_requirement": promotion_requirement,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for component_id, symbol, formula, result, proof_or_reason, zero_status, promotion_requirement in rows
    ]


def zero_proof_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "ZP3868_0_log_law",
            "component product law",
            "g_J,A = Qstar*n_A*Z_JA*c_A*R_A",
            "D ln product = sum D ln factors",
            "PROVED_BOOKKEEPING_IDENTITY",
            CORE_LAW,
            "does not make any component zero",
        ),
        (
            "ZP3868_1_integer_lattice",
            "fixed representation lattice",
            "n_A is an integer/representation label on a connected fixed matter sector",
            "a smooth integer-valued function is locally constant",
            "PROVED_FIXED_SECTOR_ZERO",
            "z_lattice,A=0",
            "does not fix Qstar or gauge norm",
        ),
        (
            "ZP3868_2_post_variation_current",
            "post-variation c_A",
            "J_parent is defined by variation before readout",
            "a later readout map cannot retroactively change the variational current",
            "PROVED_FOR_PARENT_CURRENT_CONDITIONAL",
            "z_cA_post,A=0 for parent-current leg",
            "if c_A is inserted pre-variation it becomes action/source weight, not this term",
        ),
        (
            "ZP3868_3_noether_chain_rule",
            "same Noether current owner",
            "S_matter=Sbar[q(Phi),Psi,A_Q(q),n_A,theta_A] and Dq[v]=0, no source-only slots",
            "functional derivative commutes with vertical variation of the same q-basic action",
            "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "z_Noether,A=0 if all premises sign",
            "c_A/w_A/source-marker/radiative/readout reentry clauses unsigned",
        ),
        (
            "ZP3868_4_prevariation_weight_counterexample",
            "pre-variation source/action weight",
            "S_matter=sum_A w_A(X) S_A before variation",
            "Hilbert/Noether variation inherits w_A rather than removing it",
            "COUNTEREXAMPLE_SURVIVES",
            "z_Delta_w,A remains source-arena live",
            "requires object-language/action-measure exclusion or finite bounds",
        ),
        (
            "ZP3868_5_verdict",
            "global z_g=0",
            "all components zero in one arena",
            "only z_lattice and post-variation parent-current leg are narrowed; Qstar, Noether owner and readout remain unsigned",
            "ZG_ZERO_NOT_PROVED_REDUCED_CORE_OBTAINED",
            REDUCED_DIRECT_LAW,
            "next target must attack z_Noether/current-owner or finite b_J inputs",
        ),
    ]
    return [
        {
            "proof_id": proof_id,
            "target": target,
            "premise": premise,
            "argument": argument,
            "result": result,
            "derived_or_reduced_form": derived,
            "remaining_gap": gap,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for proof_id, target, premise, argument, result, derived, gap in rows
    ]


def reduced_core_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "RZG3868_0_direct_clock_alpha",
            "clock_or_direct_alpha",
            REDUCED_DIRECT_LAW,
            "uses z_lattice=0 fixed-sector and moves post-variation c_A out of parent current",
            "BLOCKED_QSTAR_NOETHER_READOUT",
            "derive z_Noether=0 from same-current owner, then attack Qstar/readout",
        ),
        (
            "RZG3868_1_wep_source",
            "MICROSCOPE_WEP",
            "z_source,A = z_Qstar + z_Noether,A + z_readout,A + z_Delta_w,A + z_Karena,A + z_nonHilbert,A",
            "fixed charge labels and post-current parent leg do not remove source-weight/worldtube/non-Hilbert terms",
            "BLOCKED_SOURCE_EXTENSION_LIVE",
            "use Delta_w validator or parent action-measure/source-current theorem",
        ),
        (
            "RZG3868_2_r10_source",
            "R10_short_range",
            "z_R10 = reduced_core + beta_source/test/kernel/readout tails",
            "same current normalization must be tied to Yukawa/profile/material kernel before scoring",
            "BLOCKED_R10_KERNEL_AND_BETA_INPUTS",
            "do not score R10 until source/test beta and kernel rows exist",
        ),
        (
            "RZG3868_3_newton_local_gr",
            "Newton_PPN_local_GR",
            "z_source,total <= reduced_core + R_source_normalization_total + EM_source_scale_terms",
            "source-current normalization enters Newton/PPN through selected Hamiltonian/Hilbert source charge, not clock alpha alone",
            "BLOCKED_SOURCE_SELECTOR_AND_BIANCHI_GATES",
            "connect z_g/b_J to 3819 source-normalization residuals after current-owner theorem",
        ),
    ]
    return [
        {
            "row_id": row_id,
            "arena": arena,
            "reduced_formula": formula,
            "what_3868_proved": proved,
            "current_status": status,
            "next_action": next_action,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, arena, formula, proved, status, next_action in rows
    ]


def bound_input_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("BIR3868_0_z_Qstar", "z_Qstar", "D_Xhat ln Qstar or generator-norm/level derivative", "dimensionless", "TQ owner, fixed fibre norm/level/index or upper bound", "MISSING_QSTAR_OWNER_OR_BOUND"),
        ("BIR3868_1_z_Noether", "z_Noether,A", "D_Xhat ln Z_JA", "dimensionless", "same-current owner certificate or b_J component bound", "MISSING_CURRENT_OWNER_OR_BJ_BOUND"),
        ("BIR3868_2_z_readout", "z_readout,A", "D_Xhat ln R_A", "dimensionless", "clock/source readout transfer kernel or theorem-zero", "MISSING_READOUT_KERNEL_OR_ZERO"),
        ("BIR3868_3_z_Delta_w", "z_Delta_w,A", "D_Xhat ln w_A", "dimensionless", "action-measure/source-weight exclusion or sourced finite Delta_w", "MISSING_ACTION_WEIGHT_ZERO_OR_BOUND"),
        ("BIR3868_4_z_Karena", "z_Karena,A", "D_Xhat ln K_arena", "dimensionless", "arena projection/worldtube/readout kernel", "MISSING_ARENA_KERNEL"),
        ("BIR3868_5_z_nonHilbert", "z_nonHilbert,A", "projected non-Hilbert/source-tail current fraction", "dimensionless", "absence/exact-improvement/projection-silence theorem or bound", "MISSING_NONHILBERT_SILENCE_OR_BOUND"),
    ]
    return [
        {
            "input_id": input_id,
            "symbol": symbol,
            "definition": definition,
            "units": units,
            "required_evidence": required,
            "current_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for input_id, symbol, definition, units, required, status in rows
    ]


def gate_rows(
    sources: list[dict[str, object]],
    component_law: list[dict[str, object]],
    zero_proof: list[dict[str, object]],
    reduced_core: list[dict[str, object]],
    bound_inputs: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    gates = [
        ("G3868_0_sources", "all source paths resolve", all(row["exists"] and row["needle_found"] for row in sources), "source register resolved"),
        ("G3868_1_component_law", "z_g component law is explicit", any(row["formula"] == CORE_LAW for row in component_law), "log derivative product law written"),
        ("G3868_2_lattice_zero", "fixed-sector lattice derivative zero is proved", any(row["result"] == "PROVED_FIXED_SECTOR_ZERO" for row in zero_proof), "z_lattice,A=0 in fixed representation sector"),
        ("G3868_3_post_current_narrowed", "post-variation c_A cannot alter parent current", any(row["result"] == "PROVED_FOR_PARENT_CURRENT_CONDITIONAL" for row in zero_proof), "post-current term moved to readout/source if not parent-owned"),
        ("G3868_4_zg_global_zero", "global z_g=0 theorem", False, "Qstar, Noether owner, readout and source extensions remain unsigned"),
        ("G3868_5_source_arenas", "WEP/R10/Newton source extension closed", False, "Delta_w, K_arena and non-Hilbert/source residuals remain live"),
        ("G3868_6_bound_inputs", "finite bound input rows staged", len(bound_inputs) >= 6, "z_Qstar/z_Noether/z_readout/source tails listed as sourceable rows"),
        ("G3868_7_no_claim", "no generated row permits a claim", all(not bool(row.get("valid_for_claim", False)) for row in component_law + zero_proof + reduced_core + bound_inputs), "nonclaim discipline preserved"),
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
        ("DEC3868_0", "claim a narrow mathematical win, not z_g=0", "fixed integer charge labels give z_lattice=0 and variation-before-readout kills post-variation c_A for the parent current", "use the reduced direct law"),
        ("DEC3868_1", "do not use Ward conservation as calibration proof", "conservation survives current rescalings and pre-action weights", "require same-current owner or b_J bound"),
        ("DEC3868_2", "separate direct alpha current from source arenas", "WEP/R10/Newton see Delta_w, arena kernels and non-Hilbert tails beyond clock alpha", "keep source-normalization residuals explicit"),
        ("DEC3868_3", "next attack z_Noether before broad R10 scoring", "z_Noether is the most derivable live term via a functional-derivative chain rule", "build 3869 same-current owner proof or b_J source row"),
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
            "next_id": "NEXT3868_0",
            "target_checkpoint": "3869-Y5-R2FR-zNoether-same-current-owner-zero-proof-or-bJ-bound-inputs.md",
            "script": "scripts/Y5_R2FR_3869_zNoether_same_current_owner_zero_proof_or_bJ_bound_inputs.py",
            "objective": "prove z_Noether,A=0 from one q-basic parent matter action and variation-before-readout, or create source-backed b_J current-normalization bound inputs",
            "why_next": "3868 reduces the direct z_g core to z_Qstar+z_Noether+z_readout; z_Noether is the next most derivable term and also connects EM current normalization to Newton/WEP source coupling",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "status_id": "STATUS3868_0",
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "result": "ZG_GLOBAL_ZERO_NOT_PROVED_BUT_COMPONENT_CORE_REDUCED",
            "reduced_direct_law": REDUCED_DIRECT_LAW,
            "claim_allowed": False,
            "public_claim": False,
            "next_gate": "3869 z_Noether same-current owner zero proof or b_J bound inputs",
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
    component_law: list[dict[str, object]],
    zero_proof: list[dict[str, object]],
    reduced_core: list[dict[str, object]],
    bound_inputs: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    timestamp: str,
) -> None:
    text = f"""# 3868 — z_g Component Zero Proof Or Source-Backed Current-Normalization Inputs

Generated: `{timestamp}`

## Purpose

3867 showed the external clock/WEP evidence can be wired, but the joint runner is blocked by `z_g`. This checkpoint attacks `z_g` directly.

## Result In One Line

`z_g=0` is **not** proved, but the direct alpha/current core is reduced:

`{CORE_LAW}`

with fixed-sector `z_lattice,A=0` and post-variation `z_cA_post,A=0` for the parent-current leg, giving:

`{REDUCED_DIRECT_LAW}`

Source arenas still require:

`{SOURCE_LAW}`

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## Component Law

{markdown_table(component_law, ["component_id", "symbol", "result", "zero_status", "promotion_requirement"])}

## Zero-Proof Audit

{markdown_table(zero_proof, ["proof_id", "target", "result", "derived_or_reduced_form", "remaining_gap"])}

## Reduced Core Rows

{markdown_table(reduced_core, ["row_id", "arena", "reduced_formula", "current_status", "next_action"])}

## Bound Input Requirements

{markdown_table(bound_inputs, ["input_id", "symbol", "definition", "current_status", "required_evidence"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "because", "next_action"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_checkpoint", "objective", "why_next"])}

## Bottom Line

This is a genuine forward step: `z_lattice` is no longer fog, and the post-variation current-rescale loophole is pushed out of the parent current and into explicit readout/source terms. The live direct core is now `z_Qstar + z_Noether + z_readout`.

The best next strike is `z_Noether`: prove the same-current owner with one q-basic parent matter action, or stage a finite `b_J` current-normalization bound. That route touches both EM and Newton/local-GR source coupling, so it is the right pressure point.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3867", "Current State After 3868", 1)
    text = "\n".join(line for line in text.splitlines() if not line.startswith("<!-- Generated by 3868 at "))
    paragraph = (
        "`3868` makes a narrow but real derivation advance on the `z_g` coupling bottleneck. "
        "The product law `z_g_core,A=z_Qstar+z_lattice,A+z_Noether,A+z_cA_post,A+z_readout,A` is now split into theorem statuses: fixed integer representation labels give `z_lattice,A=0` on a connected fixed sector, and variation-before-readout kills a post-variation `c_A` rescale as a parent-current term. "
        "This does not prove global `z_g=0`; it reduces the direct alpha/current core to `z_Qstar+z_Noether,A+z_readout,A`, while WEP/R10/Newton source arenas keep `z_Delta_w`, `z_Karena`, and `z_nonHilbert` tails. "
        "The next best gate is `3869`: prove `z_Noether,A=0` from one q-basic parent matter action and same-current owner, or create source-backed `b_J` current-normalization bound inputs.\n\n"
    )
    if paragraph not in text and "## Next Best Gate" in text:
        text = text.replace("## Next Best Gate", paragraph + "## Next Best Gate", 1)
    old_gate = """`3868-Y5-R2FR-zg-component-zero-proof-or-source-backed-current-normalization-inputs.md`

Target: derive or source the `z_g` component products `z_Qstar`, `z_lattice`, `z_Noether`, `z_cA_post`, and `z_readout` in one local arena before any alpha/F2 claim.

This is the best next move because 3867 shows the external evidence side can be wired, but the joint runner is bottlenecked by unsigned current/coupling normalization."""
    new_gate = """`3869-Y5-R2FR-zNoether-same-current-owner-zero-proof-or-bJ-bound-inputs.md`

Target: prove `z_Noether,A=0` from one q-basic parent matter action and variation-before-readout, or create source-backed `b_J` current-normalization bound inputs.

This is the best next move because 3868 reduced the direct `z_g` core to `z_Qstar + z_Noether + z_readout`; `z_Noether` is the most derivable live term and links EM current normalization to Newton/WEP source coupling."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3868_ZG_COMPONENT_LAW.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3868_ZG_ZERO_PROOF_AUDIT.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3868_REDUCED_ZG_CORE_ROWS.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3868_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3868_ZG_COMPONENT_LAW.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    text = text.rstrip() + f"\n\n<!-- Generated by 3868 at {timestamp} -->\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    component_law: list[dict[str, object]],
    zero_proof: list[dict[str, object]],
    reduced_core: list[dict[str, object]],
    bound_inputs: list[dict[str, object]],
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

    all_rows = component_law + zero_proof + reduced_core + bound_inputs + gates
    add(
        "VAL3868_0_sources",
        "all cited source paths exist and needles are found",
        all(row["exists"] and row["needle_found"] for row in sources),
        f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved",
    )
    add(
        "VAL3868_1_component_law",
        "core z_g component law is explicit",
        any(row["formula"] == CORE_LAW for row in component_law),
        CORE_LAW,
    )
    add(
        "VAL3868_2_lattice_zero",
        "z_lattice fixed-sector zero proof is recorded",
        any(row["derived_or_reduced_form"] == "z_lattice,A=0" and row["result"] == "PROVED_FIXED_SECTOR_ZERO" for row in zero_proof),
        "integer/representation labels locally constant",
    )
    add(
        "VAL3868_3_post_current_narrow",
        "post-variation current rescale is narrowed",
        any(row["result"] == "PROVED_FOR_PARENT_CURRENT_CONDITIONAL" for row in zero_proof),
        "post-current c_A cannot redefine parent variational current",
    )
    add(
        "VAL3868_4_global_zero_blocked",
        "global z_g=0 is not claimed",
        any(row["result"] == "ZG_ZERO_NOT_PROVED_REDUCED_CORE_OBTAINED" for row in zero_proof)
        and any(row["gate_id"] == "G3868_4_zg_global_zero" and row["status"] == "BLOCKED" for row in gates),
        "reduced core retained as nonclaim",
    )
    add(
        "VAL3868_5_bound_inputs",
        "bound input rows cover live terms",
        {row["symbol"] for row in bound_inputs} >= {"z_Qstar", "z_Noether,A", "z_readout,A", "z_Delta_w,A", "z_Karena,A", "z_nonHilbert,A"},
        "live direct/source terms have input requirements",
    )
    add(
        "VAL3868_6_no_claim",
        "all generated rows remain nonclaim",
        all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in all_rows),
        "valid_for_claim/claim_allowed false throughout",
    )
    add(
        "VAL3868_7_next",
        "next target selects z_Noether same-current owner",
        DOC_PATH.exists() and "3869-Y5-R2FR-zNoether-same-current-owner-zero-proof-or-bJ-bound-inputs" in read_text(DOC_PATH),
        "3869 z_Noether target recorded",
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
        add(f"VAL3868_8_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add(
        "VAL3868_9_doc",
        "markdown checkpoint document exists",
        DOC_PATH.exists() and "This is a genuine forward step" in read_text(DOC_PATH),
        rel(DOC_PATH),
    )
    formalization_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3868*", "P8_Y5_BRR545_3868*", "*Y5_R2FR_3868*", "3868-Y5-R2FR*"):
            formalization_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add(
        "VAL3868_10_formalization_clean",
        "formalization-workbench has no generated 3868 project files",
        len(formalization_hits) == 0,
        "; ".join(str(path) for path in formalization_hits) if formalization_hits else "no generated 3868 project file hits under formalization-workbench",
    )
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add(
        "VAL3868_11_pycache_removed",
        "scripts __pycache__ removed",
        len(pycache_hits) == 0,
        "; ".join(str(path) for path in pycache_hits) if pycache_hits else "no __pycache__ directories",
    )
    return rows


def main() -> int:
    timestamp = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows(timestamp)
    component_law = component_law_rows(timestamp)
    zero_proof = zero_proof_rows(timestamp)
    reduced_core = reduced_core_rows(timestamp)
    bound_inputs = bound_input_rows(timestamp)
    gates = gate_rows(sources, component_law, zero_proof, reduced_core, bound_inputs, timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["component_law"], component_law)
    write_csv(OUTPUTS["zero_proof"], zero_proof)
    write_csv(OUTPUTS["reduced_core"], reduced_core)
    write_csv(OUTPUTS["bound_inputs"], bound_inputs)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, component_law, zero_proof, reduced_core, bound_inputs, gates, decisions, next_target, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, component_law, zero_proof, reduced_core, bound_inputs, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_ZG_COMPONENT_CORE_REDUCED_NONCLAIM")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

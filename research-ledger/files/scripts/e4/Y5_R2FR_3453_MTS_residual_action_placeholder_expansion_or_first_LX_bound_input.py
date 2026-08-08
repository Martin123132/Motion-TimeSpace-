from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3453-Y5-R2FR-MTS-residual-action-placeholder-expansion-or-first-LX-bound-input-under-AX1090.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCES = {
    "script_3453": Path(__file__).resolve(),
    "doc_3452": ROOT / "3452-Y5-R2FR-Xrep-action-line-absence-or-LX-residual-norm-bound-under-AX1090.md",
    "next_3452": OUT / "P8_Y5_R2FR_3452_NEXT_TARGET.csv",
    "scan_3452": OUT / "P8_Y5_R2FR_3452_ACTION_LINE_ABSENCE_SCAN.csv",
    "formation_3452": OUT / "P8_Y5_R2FR_3452_FORMATION_RULE_THEOREM.csv",
    "lx_bounds_3452": OUT / "P8_Y5_R2FR_3452_LX_RESIDUAL_NORM_BOUNDS.csv",
    "minimal_line_3378": OUT / "P8_Y5_R2FR_3378_MINIMAL_PARENT_ACTION_LINE.csv",
    "local_action_3382": OUT / "P8_Y5_R2FR_3382_LOCAL_ACTION_BLOCK_UNDER_UOC.csv",
    "minimal_candidate_3395": OUT / "P8_Y5_R2FR_3395_MINIMAL_PARENT_ACTION_LINE_CANDIDATE.csv",
    "parent_density_3424": OUT / "P8_Y5_R2FR_3424_PARENT_ACTION_DENSITY.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3453_SOURCE_REGISTER.csv",
    "placeholder_expansion_matrix": OUT / "P8_Y5_R2FR_3453_PLACEHOLDER_EXPANSION_MATRIX.csv",
    "first_lx_bound_input": OUT / "P8_Y5_R2FR_3453_FIRST_LX_BOUND_INPUT.csv",
    "active_residual_queue": OUT / "P8_Y5_R2FR_3453_ACTIVE_RESIDUAL_QUEUE.csv",
    "deltaH_feed_update": OUT / "P8_Y5_R2FR_3453_DELTAH_FEED_UPDATE.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3453_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3453_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3453_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3453_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3453_VALIDATION.csv",
}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields = list(rows[0].keys())

    def clean(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "/")

    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join("---" for _ in fields) + " |",
            *["| " + " | ".join(clean(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def source_register() -> list[dict[str, Any]]:
    roles = {
        "script_3453": "generator for this checkpoint",
        "doc_3452": "immediate placeholder-expansion handoff",
        "next_3452": "machine-readable 3453 target",
        "scan_3452": "selected action-line scan and broad placeholder verdict",
        "formation_3452": "anti-smuggling formation theorem",
        "lx_bounds_3452": "six residual norm-bound formulas",
        "minimal_line_3378": "L_MTS_silent and parent action line",
        "local_action_3382": "L_MTS_IR placeholder",
        "minimal_candidate_3395": "S_MTS placeholder",
        "parent_density_3424": "Z_residual sector",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[source_id],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for source_id, path in SOURCES.items()
    ]


def placeholder_expansion_matrix() -> list[dict[str, Any]]:
    return [
        {
            "expansion_id": "PEX3453_0_LMTS_silent_qbasic",
            "placeholder": "L_MTS_silent(Q,dQ;g_obs)",
            "allowed_subblock": "q-basic scalar density L_Q[q(Phi),d_Q q(Phi);g_obs]",
            "vXrep_variation": "0",
            "classification": "THEOREM_ZERO_SUBBLOCK",
            "anti_smuggling_requirement": "Q must be an observed quotient variable or fixed representation/topological class, not X_rep renamed Q",
            "feeds_bound": "LXB3452_0 theorem-zero input",
            "source_path": str(SOURCES["minimal_line_3378"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "expansion_id": "PEX3453_1_LMTS_silent_exact_boundary",
            "placeholder": "L_MTS_silent / boundary exact class",
            "allowed_subblock": "dB_exact or topological density with fixed local boundary class",
            "vXrep_variation": "0 if exact/proper and Q_X local projection is zero",
            "classification": "CONDITIONAL_BOUNDARY_ZERO_SUBBLOCK",
            "anti_smuggling_requirement": "nonzero corner/reference charge must move to boundary residual",
            "feeds_bound": "LXB3452_4 boundary zero candidate",
            "source_path": str(SOURCES["minimal_line_3378"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "expansion_id": "PEX3453_2_LMTS_silent_unexpanded_remainder",
            "placeholder": "L_MTS_silent remainder",
            "allowed_subblock": "none until expanded",
            "vXrep_variation": "MISSING",
            "classification": "ACTIVE_RESIDUAL_UNEXPANDED",
            "anti_smuggling_requirement": "the word silent gives no proof; write the term or bound it",
            "feeds_bound": "LXB3452_0_explicit_Xrep_bulk",
            "source_path": str(SOURCES["minimal_line_3378"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "expansion_id": "PEX3453_3_LMTS_IR_public_metric_only",
            "placeholder": "L_MTS_IR(Phi,g_obs)",
            "allowed_subblock": "public metric-only higher-derivative/non-EH operator R11[g_obs]",
            "vXrep_variation": "0 under v_Xrep, but it remains a left-hand local-GR/R11 residual",
            "classification": "NOT_XREP_BUT_R11_RESIDUAL",
            "anti_smuggling_requirement": "cannot count as extra-sector zero; must satisfy R11/local-GR operator gates",
            "feeds_bound": "R11 residual, not L_X",
            "source_path": str(SOURCES["local_action_3382"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "expansion_id": "PEX3453_4_LMTS_IR_hidden_X_remainder",
            "placeholder": "L_MTS_IR(Phi,g_obs) hidden part",
            "allowed_subblock": "none until hidden Phi-dependence is typed",
            "vXrep_variation": "MISSING",
            "classification": "ACTIVE_RESIDUAL_UNEXPANDED",
            "anti_smuggling_requirement": "expand Phi into q-basic variables versus X_rep/Z_active before claiming descent",
            "feeds_bound": "LXB3452_0 or LXB3452_1",
            "source_path": str(SOURCES["local_action_3382"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "expansion_id": "PEX3453_5_SMTS_psi_Gamma",
            "placeholder": "S_MTS[psi,Gamma,...]",
            "allowed_subblock": "Gamma/Khat/q_loc action only if q-basic or first-class/exact",
            "vXrep_variation": "MISSING until Gamma/Khat/q_loc are typed against v_Xrep",
            "classification": "ACTIVE_RESIDUAL_UNEXPANDED",
            "anti_smuggling_requirement": "Gamma/Khat cannot be called silent if it sources q_loc or C_tau^X",
            "feeds_bound": "LXB3452_0 explicit bulk or LXB3452_5 tau/clock if time-coupled",
            "source_path": str(SOURCES["minimal_candidate_3395"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "expansion_id": "PEX3453_6_Z_residual_sector",
            "placeholder": "Z_residual sector",
            "allowed_subblock": "Z_active residual kept outside v_Xrep kernel",
            "vXrep_variation": "0 only because v_Xrep is defined to act as 0 on Z_active; Z still affects local GR through its own Euler/stress equations",
            "classification": "ACTIVE_NON_XREP_LOCAL_RESIDUAL",
            "anti_smuggling_requirement": "Z residual must be zero/bounded in E_res/R11/PPN arenas, not erased by Xrep quotient",
            "feeds_bound": "R11/PPN residual queue rather than LXB3452_0",
            "source_path": str(SOURCES["parent_density_3424"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def first_lx_bound_input() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "FLX3453_0_qbasic_zero_input",
            "feeds_bound": "LXB3452_0_explicit_Xrep_bulk",
            "subblock": "PEX3453_0_LMTS_silent_qbasic",
            "E_Xrep_density": "0",
            "xi_X_norm_or_unit_generator": "arbitrary, coefficient multiplies zero",
            "Theta_Xrep_boundary_flux": "0 for q-basic bulk subblock",
            "units": "same as H_tau curl numerator density",
            "source_path": str(OUTPUTS["placeholder_expansion_matrix"]),
            "current_status": "REAL_THEOREM_ZERO_INPUT_FOR_QBASIC_SUBBLOCK_NOT_TOTAL",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "input_id": "FLX3453_1_unexpanded_remainder_input",
            "feeds_bound": "LXB3452_0_explicit_Xrep_bulk",
            "subblock": "PEX3453_2/4/5 unexpanded active remainders",
            "E_Xrep_density": "MISSING_RESIDUAL_ACTION_EXPANSION",
            "xi_X_norm_or_unit_generator": "MISSING_GENERATOR_NORMALIZATION",
            "Theta_Xrep_boundary_flux": "MISSING_BOUNDARY_FLUX",
            "units": "MISSING_UNITS_UNTIL_ACTION_DENSITY_TYPED",
            "source_path": str(OUTPUTS["placeholder_expansion_matrix"]),
            "current_status": "BOUND_INPUT_STILL_MISSING_FOR_ACTIVE_REMAINDER",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def active_residual_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "ARQ3453_0",
            "active_item": "hidden Phi-dependence inside L_MTS_IR",
            "why_active": "could contain X_rep or hidden frame/EM coefficient dependence",
            "next_test": "type every Phi argument as q-basic, Z_active, or X_rep",
            "fallback_bound": "LXB3452_0 or LXB3452_1",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "queue_id": "ARQ3453_1",
            "active_item": "Gamma/Khat/q_loc inside S_MTS",
            "why_active": "can source the local residual current and tau/clock branch",
            "next_test": "prove Gamma/Khat/q_loc are q-basic/first-class or fill C_tau^X/omega_X bound",
            "fallback_bound": "LXB3452_0 or LXB3452_5",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "queue_id": "ARQ3453_2",
            "active_item": "Z_residual local stress",
            "why_active": "not an Xrep-kernel failure, but still a local-GR left-hand residual",
            "next_test": "R11/E_res/PPN operator coefficient zero or bound",
            "fallback_bound": "R11/PPN residual rows",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def deltaH_feed_update() -> list[dict[str, Any]]:
    return [
        {
            "feed_id": "DHF3453_0_qbasic_subblock",
            "result": "q-basic L_MTS_silent subblock contributes zero to L_Xrep bound",
            "feeds": "FLX3453_0_qbasic_zero_input",
            "status": "PARTIAL_ZERO_FEED",
            "remaining": "unexpanded active remainders still block total Delta_H_curl_extra zero",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "feed_id": "DHF3453_1_total_placeholder",
            "result": "total placeholder action descent remains unpromoted",
            "feeds": "FLX3453_1_unexpanded_remainder_input",
            "status": "TOTAL_NONCLAIM",
            "remaining": "PEX3453_2, PEX3453_4, PEX3453_5 and Z/R11 queue",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "G3453_0_sources_exist",
            "gate": "all cited 3453 source paths exist",
            "status": "PRIVATE_CHECK_PASS",
            "blocks_claim": False,
            "needed_for_claim": "provenance only",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G3453_1_placeholders_classified",
            "gate": "all broad placeholders are split into q-basic/exact/active categories",
            "status": "PASS_CLASSIFICATION",
            "blocks_claim": False,
            "needed_for_claim": "active categories need expansion or bounds",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G3453_2_first_real_zero_input",
            "gate": "first L_X bound receives theorem-zero input for q-basic subblock",
            "status": "PASS_SUBBLOCK_ONLY",
            "blocks_claim": True,
            "needed_for_claim": "total active remainder must also be zero/bounded",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G3453_3_active_remainders",
            "gate": "unexpanded active remainders retained",
            "status": "BLOCKS_TOTAL_CLAIM",
            "blocks_claim": True,
            "needed_for_claim": "type hidden Phi/Gamma/Khat/Z terms",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G3453_4_no_claim",
            "gate": "no local-GR/Newton/R10/PPN/clock/orbital pass from this checkpoint",
            "status": "ENFORCED",
            "blocks_claim": True,
            "needed_for_claim": "full placeholder expansion and residual closure",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3453_0",
            "question": "Did placeholder expansion produce a real zero?",
            "answer": "Yes, but only for the q-basic subblock.",
            "reason": "A q-basic density has zero v_Xrep variation by the 3450 kernel theorem.",
            "next_action": "expand hidden Phi/Gamma/Khat/Z remainders",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3453_1",
            "question": "Can total action descent be promoted?",
            "answer": "No.",
            "reason": "The active remainders are still untyped and could contain the very local residuals being tested.",
            "next_action": "3454 type Gamma/Khat/q_loc and hidden Phi dependence or fill first active bound",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3454-Y5-R2FR-Gamma-Khat-q_loc-placeholder-typing-or-first-active-LX-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3454_Gamma_Khat_qloc_placeholder_typing_or_first_active_LX_bound.py",
            "objective": "Type Gamma/Khat/q_loc and hidden Phi arguments as q-basic, first-class, Z-active, or X_rep-active; if any remain active, fill the first bound input with units.",
            "start_from": "PEX3453_4_LMTS_IR_hidden_X_remainder and PEX3453_5_SMTS_psi_Gamma",
            "success_gate": "No hidden Phi/Gamma/Khat placeholder remains untyped, or at least one active L_X bound row has real theorem/numeric input.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3453_0",
            "mode": "private_nonclaim_checkpoint",
            "result": "broad MTS placeholders classified and first q-basic L_X zero input written",
            "claim_status": "NO_LOCAL_GR_NEWTON_R10_PPN_CLOCK_OR_ORBITAL_CLAIM",
            "reason": "active hidden Phi/Gamma/Khat/Z remainders still need typing or bounds",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], start_utc: datetime) -> list[dict[str, Any]]:
    modified_count = 0
    if FORMALIZATION.exists():
        start_timestamp = start_utc.timestamp()
        modified_count = sum(
            1
            for checked_path in FORMALIZATION.rglob("*")
            if checked_path.is_file() and checked_path.stat().st_mtime >= start_timestamp
        )

    nonclaim_ok = True
    for rows in rows_by_name.values():
        for row in rows:
            if "valid_for_claim" in row and str(row["valid_for_claim"]).lower() != "false":
                nonclaim_ok = False
            if "claim_allowed" in row and str(row["claim_allowed"]).lower() != "false":
                nonclaim_ok = False

    parse_ok = True
    for output_name, path in OUTPUTS.items():
        if output_name == "validation":
            continue
        try:
            read_csv(path)
        except csv.Error:
            parse_ok = False

    classifications = {row["classification"] for row in rows_by_name["placeholder_expansion_matrix"]}
    active_rows = [row for row in rows_by_name["placeholder_expansion_matrix"] if "ACTIVE" in row["classification"]]
    first_zero = [
        row
        for row in rows_by_name["first_lx_bound_input"]
        if row["input_id"] == "FLX3453_0_qbasic_zero_input"
    ]

    validations = [
        {
            "check_id": "VAL3453_0_sources_exist",
            "condition": "all cited 3453 source paths exist",
            "passed": all(path.exists() for path in SOURCES.values()),
            "detail": f"{sum(1 for path in SOURCES.values() if path.exists())}/{len(SOURCES)} source paths exist",
        },
        {
            "check_id": "VAL3453_1_placeholders_classified",
            "condition": "placeholder expansion matrix has zero, R11 and active classes",
            "passed": "THEOREM_ZERO_SUBBLOCK" in classifications
            and "ACTIVE_RESIDUAL_UNEXPANDED" in classifications
            and "NOT_XREP_BUT_R11_RESIDUAL" in classifications,
            "detail": f"classifications={';'.join(sorted(classifications))}",
        },
        {
            "check_id": "VAL3453_2_first_lx_zero_input",
            "condition": "first L_X bound input has a real q-basic theorem-zero row",
            "passed": bool(first_zero)
            and first_zero[0]["E_Xrep_density"] == "0"
            and first_zero[0]["current_status"] == "REAL_THEOREM_ZERO_INPUT_FOR_QBASIC_SUBBLOCK_NOT_TOTAL",
            "detail": first_zero[0]["current_status"] if first_zero else "missing zero input",
        },
        {
            "check_id": "VAL3453_3_active_remainders_retained",
            "condition": "active remainders remain explicit and block total claim",
            "passed": len(active_rows) >= 3
            and any(row["expansion_id"] == "PEX3453_5_SMTS_psi_Gamma" for row in active_rows),
            "detail": f"{len(active_rows)} active rows retained",
        },
        {
            "check_id": "VAL3453_4_no_claims",
            "condition": "all generated rows remain nonclaim",
            "passed": nonclaim_ok,
            "detail": "valid_for_claim=false and claim_allowed=false wherever present",
        },
        {
            "check_id": "VAL3453_5_generated_csv_parse",
            "condition": "generated CSV rows parse cleanly",
            "passed": parse_ok,
            "detail": "CSV reader pass for generated outputs present before validation write",
        },
        {
            "check_id": "VAL3453_6_next_target_3454",
            "condition": "next target types Gamma/Khat/q_loc or fills active bound",
            "passed": rows_by_name["next_target"][0]["target_doc"].startswith("3454-Y5-R2FR-Gamma-Khat-q_loc-placeholder"),
            "detail": rows_by_name["next_target"][0]["target_doc"],
        },
        {
            "check_id": "VAL3453_7_formalization_untouched",
            "condition": "formalization-workbench modified-file count remains 0 during this run",
            "passed": modified_count == 0,
            "detail": f"modified_count_since_start={modified_count}",
        },
    ]
    validations.append(
        {
            "check_id": "VAL3453_8_overall",
            "condition": "3453 placeholder expansion checkpoint is internally valid",
            "passed": all(row["passed"] for row in validations),
            "detail": "PASS" if all(row["passed"] for row in validations) else "FAIL",
        }
    )
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    text = f"""# 3453 - MTS Residual Action Placeholder Expansion or First L_X Bound Input

## Summary
- This checkpoint expands the broad MTS placeholders instead of letting names like `silent` do proof-work.
- The good news: the q-basic subblock of `L_MTS_silent(Q,dQ;g_obs)` has a real theorem-zero input for the `L_X` bound: `E_Xrep_density=0`.
- The careful news: this is only a subblock, not the whole residual action.
- `L_MTS_IR(Phi,g_obs)`, `S_MTS[psi,Gamma,...]`, and `Z_residual` still contain active or untyped parts.
- `Z_residual` is not an `X_rep` kernel failure if `v_Xrep` acts as zero on `Z_active`, but it remains a local-GR/R11/PPN residual and cannot be counted as GR.

## Source Register
{md_table(rows_by_name["source_register"])}

## Placeholder Expansion Matrix
{md_table(rows_by_name["placeholder_expansion_matrix"])}

## First L_X Bound Input
{md_table(rows_by_name["first_lx_bound_input"])}

## Active Residual Queue
{md_table(rows_by_name["active_residual_queue"])}

## DeltaH Feed Update
{md_table(rows_by_name["deltaH_feed_update"])}

## Promotion Gates
{md_table(rows_by_name["promotion_gates"])}

## Decision Ledger
{md_table(rows_by_name["decision_ledger"])}

## Next Target
{md_table(rows_by_name["next_target"])}

## Runner Nonclaim
{md_table(rows_by_name["runner_nonclaim"])}

## Validation
{md_table(rows_by_name["validation"])}

## Bottom Line
We got one real zero input, not a total pass. The q-basic part of the residual action is harmless under `v_Xrep`; the remaining live target is now narrower: type the hidden `Phi/Gamma/Khat/q_loc` placeholders or turn them into explicit bound rows.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    start_utc = datetime.now(timezone.utc)
    rows_by_name = {
        "source_register": source_register(),
        "placeholder_expansion_matrix": placeholder_expansion_matrix(),
        "first_lx_bound_input": first_lx_bound_input(),
        "active_residual_queue": active_residual_queue(),
        "deltaH_feed_update": deltaH_feed_update(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    for output_name, rows in rows_by_name.items():
        write_csv(OUTPUTS[output_name], rows)
    rows_by_name["validation"] = validation_rows(rows_by_name, start_utc)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    failed_rows = [row for row in rows_by_name["validation"] if not row["passed"]]
    if failed_rows:
        raise SystemExit(f"3453 validation failed: {failed_rows}")
    print(f"wrote {DOC}")
    print(f"wrote {len(OUTPUTS)} csv outputs")


if __name__ == "__main__":
    main()

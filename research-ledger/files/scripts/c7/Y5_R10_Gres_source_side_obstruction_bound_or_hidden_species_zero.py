from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1213"
TITLE = "1213-Y5-R10-Gres-source-side-obstruction-bound-or-hidden-species-zero"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
ZERO_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_SIDE_ZERO_AUDIT.csv"
BOUND_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_SIDE_BOUND_DECOMPOSITION.csv"
SOURCE_ROWS_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_SIDE_OBSTRUCTION_ROWS.csv"
FEED_PATH = OUT_DIR / f"{PACK_ID}_GRES_PROFILE_FEED_UPDATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1213_VALIDATION.csv"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = ROOT / relative_path
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def fmt(value: object) -> str:
    if isinstance(value, float):
        if value == 0:
            return "0"
        return f"{value:.12g}"
    return str(value)


def md_escape(value: object) -> str:
    return fmt(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join(["---"] * len(fields)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1213_0_1212_next",
            "local_path": "1212-Y5-R10-Gres-zero-source-side-EH-limit-or-first-profile-row.md",
            "needle": "NEXT1212_0_1213",
            "purpose": "handoff to source-side obstruction bound or hidden/species zero",
        },
        {
            "source_id": "SRC1213_1_1212_source_side",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1212_SOURCE_SIDE_ZERO_ATTEMPT.csv",
            "needle": "SSZ1212_4_source_side_verdict",
            "purpose": "source-side zero blocked and absolute bound formula",
        },
        {
            "source_id": "SRC1213_2_1212_profile",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1212_FIRST_GRES_BOUND_PROFILE_ROW.csv",
            "needle": "GRB1212_0_first_Gres_bound_profile",
            "purpose": "first Gres_bound profile row to feed",
        },
        {
            "source_id": "SRC1213_3_956_spine",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_956_SOURCE_SIDE_GR_NEWTON_SPINE.csv",
            "needle": "SSG956_5_source_side_verdict",
            "purpose": "source-side GR/Newton hidden/species residual spine",
        },
        {
            "source_id": "SRC1213_4_1031_spm_residuals",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1031_SPM_CLOSURE_BRANCH.csv",
            "needle": "SPMC1031_2_remaining_residuals",
            "purpose": "SPM closure leaves hidden/source/support residuals",
        },
        {
            "source_id": "SRC1213_5_1032_no_overclaim",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1032_SPM_CLOSURE_LEDGER.csv",
            "needle": "SPML1032_2_no_overclaim_policy",
            "purpose": "SPM closure cannot be used as local-GR source proof",
        },
        {
            "source_id": "SRC1213_6_1063_label_forgetting",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1063_SOURCE_FORGETTING_THEOREM_ATTEMPT.csv",
            "needle": "THM1063_5_verdict",
            "purpose": "source-label forgetting theorem remains conditional",
        },
        {
            "source_id": "SRC1213_7_1063_owner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1063_NOETHER_SOURCE_OWNER_AUDIT.csv",
            "needle": "NO1063_2_Noether_current_owner",
            "purpose": "Noether/source owner missing",
        },
        {
            "source_id": "SRC1213_8_1064_label_proof",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1064_LABEL_FORGETTING_PROOF_ATTEMPT.csv",
            "needle": "PLF1064_5_verdict",
            "purpose": "parent category label-forgetting proof conditional",
        },
        {
            "source_id": "SRC1213_9_1064_slot",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1064_NO_SOURCE_ONLY_SLOT_AUDIT.csv",
            "needle": "NSS1064_2_relative_weight",
            "purpose": "relative source weight lives unless no-source-only slot is parent-signed",
        },
        {
            "source_id": "SRC1213_10_1065_grammar",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1065_PARENT_GRAMMAR_AUDIT.csv",
            "needle": "PGG1065_5_verdict",
            "purpose": "no-source-only-slot grammar theorem not parent-derived",
        },
        {
            "source_id": "SRC1213_11_1065_zero_clauses",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1065_WA_THEOREM_ZERO_CLAUSES.csv",
            "needle": "WTZ1065_4_verdict",
            "purpose": "relative source-weight zero theorem not parent-signed",
        },
        {
            "source_id": "SRC1213_12_1013_obstruction",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1013_MEASURED_GM_OBSTRUCTION_VECTOR.csv",
            "needle": "OBS1013_0_projected_extra_current",
            "purpose": "measured-GM obstruction vector rows",
        },
        {
            "source_id": "SRC1213_13_1013_runner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1013_OBSTRUCTION_RUNNER.csv",
            "needle": "OBR1013_0_projected_extra_current",
            "purpose": "measured-GM obstruction runner refuses unfilled rows",
        },
    ]

    source_rows: list[dict[str, object]] = []
    for spec in source_specs:
        path_exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_rows.append(
            {
                **spec,
                "path_exists": path_exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    zero_audit = [
        {
            "audit_id": "SSA1213_0_hidden_public_metric",
            "component": "Delta_public_metric_frame",
            "zero_route": "derive single public metric/coframe plus ordinary matter/readout interface from parent action, not closure",
            "current_evidence": "SPM is explicit closure only; terminality-alone proof fails",
            "status": "ZERO_NOT_DERIVED",
            "bound_name": "B_public_metric_frame",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "SSA1213_1_nonHilbert_support",
            "component": "Delta_nonHilbert_plus_support",
            "zero_route": "prove non-Hilbert current, support shift, domain/boundary source tail, and hidden matter-frame channels vanish",
            "current_evidence": "1031/1032 keep q_nonH, Delta_W_support, b_A, b_alpha, and measured-GM as retained residuals",
            "status": "ZERO_NOT_DERIVED",
            "bound_name": "B_nonHilbert_support",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "SSA1213_2_species_weight",
            "component": "Delta_species_weight",
            "zero_route": "derive no-source-only-slot grammar: source functor must forget labels before coupling selection",
            "current_evidence": "1063/1064/1065 identify the theorem but keep it parent-unsigned; w_A counterexample survives",
            "status": "ZERO_NOT_DERIVED",
            "bound_name": "B_species_weight",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "SSA1213_3_measured_GM_flux",
            "component": "Delta_Meff_flux_plus_calibration",
            "zero_route": "derive compact-exterior d(Pi_M J_H)=0, worldtube glue, and absolute calibration before orbital/PPN readout",
            "current_evidence": "1013 obstruction vector remains retained/unfilled",
            "status": "ZERO_NOT_DERIVED",
            "bound_name": "B_Meff_flux_calibration",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "SSA1213_4_source_side_total",
            "component": "G_source_side",
            "zero_route": "all four source-side components close in one same-frame local domain",
            "current_evidence": "every component above remains unsigned or unfilled",
            "status": "SOURCE_SIDE_ZERO_BLOCKED",
            "bound_name": "G_source_side_bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    bound_rows = [
        {
            "bound_id": "SSB1213_0_absolute_source_side",
            "quantity": "G_source_side_bound",
            "bound_formula": "G_source_side_bound <= B_public_metric_frame + B_nonHilbert_support + B_species_weight + B_Meff_flux_calibration",
            "derivation_basis": "1212 source-side split plus absolute-sum/no-cancellation rule",
            "required_inputs": "B_public_metric_frame;B_nonHilbert_support;B_species_weight;B_Meff_flux_calibration;domain_id;norm_id",
            "status": "BOUND_FORM_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "SSB1213_1_species_weight",
            "quantity": "B_species_weight",
            "bound_formula": "B_species_weight <= C_species*(||Delta_w_AB|| + ||Delta_w_time|| + ||Delta_w_range|| + ||Delta_w_frame|| + ||tau_source_projection||)",
            "derivation_basis": "1063-1065 show relative source weights survive unless no-source-only-slot grammar is parent-signed; any finite branch must carry material/time/range/frame projections",
            "required_inputs": "C_species;Delta_w_AB;Delta_w_time;Delta_w_range;Delta_w_frame;tau_source_projection;source_path",
            "status": "BOUND_FORM_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "SSB1213_2_Meff_flux",
            "quantity": "B_Meff_flux_calibration",
            "bound_formula": "B_Meff_flux_calibration <= |-Pi_M dJ_extra| + |[d,Pi_M]J_H| + |A_parent| + |R_eq| + |B_zero_flux| + |T_PiM| + |flux_leak| + |Delta_cal_PPN|",
            "derivation_basis": "1013 exact obstruction vector for measured-GM/source-normalization closure",
            "required_inputs": "OBS1013_0..OBS1013_7 numeric values or theorem-zero certificates",
            "status": "BOUND_FORM_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "SSB1213_3_hidden_support",
            "quantity": "B_nonHilbert_support",
            "bound_formula": "B_nonHilbert_support <= ||q_nonH|| + ||Delta_W_support|| + ||B_boundary_source|| + ||Delta_domain_source||",
            "derivation_basis": "SPM closure excludes direct shadow frame only by branch definition; non-Hilbert/support/domain tails remain independent residuals unless signed",
            "required_inputs": "q_nonH_norm;Delta_W_support_norm;B_boundary_source_norm;Delta_domain_source_norm",
            "status": "BOUND_FORM_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    obstruction_rows = [
        {
            "row_id": "SSR1213_0_G_source_side_bound",
            "feeds": "GRB1212_0_first_Gres_bound_profile.source_side_bound",
            "formula": "B_public_metric_frame + B_nonHilbert_support + B_species_weight + B_Meff_flux_calibration",
            "B_public_metric_frame": "MISSING",
            "B_nonHilbert_support": "MISSING",
            "B_species_weight": "MISSING",
            "B_Meff_flux_calibration": "MISSING",
            "value": "MISSING",
            "units": "same_as_G_res_norm",
            "source_path": "MISSING_SOURCE_PATH",
            "current_status": "SOURCE_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "SSR1213_1_Delta_species_weight",
            "feeds": "SSR1213_0_G_source_side_bound.B_species_weight",
            "formula": "C_species*(Delta_w_AB + Delta_w_time + Delta_w_range + Delta_w_frame + tau_source_projection)",
            "B_public_metric_frame": "not_applicable",
            "B_nonHilbert_support": "not_applicable",
            "B_species_weight": "MISSING_DELTA_W_AND_PROJECTION",
            "B_Meff_flux_calibration": "not_applicable",
            "value": "MISSING",
            "units": "same_as_source_side_norm",
            "source_path": "MISSING_SOURCE_PATH",
            "current_status": "SOURCE_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "SSR1213_2_Meff_flux_calibration",
            "feeds": "SSR1213_0_G_source_side_bound.B_Meff_flux_calibration",
            "formula": "abs_sum(OBS1013_0..OBS1013_7)",
            "B_public_metric_frame": "not_applicable",
            "B_nonHilbert_support": "not_applicable",
            "B_species_weight": "not_applicable",
            "B_Meff_flux_calibration": "MISSING_OBS1013_VECTOR_VALUES",
            "value": "MISSING",
            "units": "same_as_source_side_norm",
            "source_path": "MISSING_SOURCE_PATH",
            "current_status": "SOURCE_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    feed_rows = [
        {
            "feed_id": "GUP1213_0_profile_update",
            "target_profile_row": "GRB1212_0_first_Gres_bound_profile",
            "field_to_fill": "source_side_bound",
            "source_row": "SSR1213_0_G_source_side_bound",
            "claim_policy": "valid only after all source-side components are numeric/source-backed or theorem-zero in same domain/norm",
            "current_status": "FEED_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    decisions = [
        {
            "decision_id": "DEC1213_0_zero_attempt",
            "condition": "Can G_source_side=0 be proved now?",
            "decision": "No. SPM remains closure-only, no-source-only-slot grammar is not parent-signed, and measured-GM flux obstructions are unfilled.",
            "result": "source-side zero blocked, but absolute bound decomposition is staged.",
            "next_action": "attack the no-source-only-slot parent signature first, because it directly targets Delta_species_weight.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1213_1_bound_row",
            "condition": "What feeds the 1212 Gres profile next?",
            "decision": "SSR1213_0 becomes the source-side input for GRB1212_0.",
            "result": "G_source_side is now a fillable row rather than a label.",
            "next_action": "1214 should derive or bound Delta_species_weight via no-source-only-slot grammar.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1213_0_public_metric_hidden_zero",
            "gate": "Delta_public_metric_frame=0 and Delta_nonHilbert_plus_support=0",
            "status": "BLOCKED",
            "reason": "SPM is closure-only and retained non-Hilbert/support residuals remain",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1213_1_species_weight_zero",
            "gate": "Delta_species_weight=0",
            "status": "BLOCKED",
            "reason": "no-source-only-slot grammar and current owner are not parent-signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1213_2_Meff_flux_zero",
            "gate": "Delta_Meff_flux_plus_calibration=0",
            "status": "BLOCKED",
            "reason": "1013 obstruction vector is retained/unfilled",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1213_3_source_side_numeric",
            "gate": "G_source_side_bound numeric",
            "status": "BLOCKED",
            "reason": "SSR1213 rows remain source-ready placeholders",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1213_4_local_GR_R10",
            "gate": "local-GR/R10 pass",
            "status": "BLOCKED",
            "reason": "1213 fills source-side plumbing only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_rows = [
        {
            "next_id": "NEXT1213_0_1214",
            "target_file": "1214-Y5-R10-no-source-only-slot-parent-signature-or-Delta-species-bound-fill.md",
            "target_script": "scripts/Y5_R10_no_source_only_slot_parent_signature_or_Delta_species_bound_fill.py",
            "task": "try to parent-sign the no-source-only-slot grammar that kills Delta_species_weight; if it fails, fill the first nonclaim Delta_species_weight bound row for SSR1213_1",
            "success_condition": "Delta_species_weight is theorem-zero, or a sourced/symbolic same-norm bound row exists with no cancellation and explicit WEP/PPN/R10/Gdot projections",
            "do_not_do": "do not absorb relative weights into measured G unless common/universal/range-time-frame independent; do not claim local GR; do not edit formalization-workbench; do not push GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    source_fields = ["source_id", "local_path", "needle", "purpose", "path_exists", "needle_found", "valid_for_claim", "claim_allowed"]
    audit_fields = ["audit_id", "component", "zero_route", "current_evidence", "status", "bound_name", "valid_for_claim", "claim_allowed"]
    bound_fields = ["bound_id", "quantity", "bound_formula", "derivation_basis", "required_inputs", "status", "valid_for_claim", "claim_allowed"]
    row_fields = ["row_id", "feeds", "formula", "B_public_metric_frame", "B_nonHilbert_support", "B_species_weight", "B_Meff_flux_calibration", "value", "units", "source_path", "current_status", "valid_for_claim", "claim_allowed"]
    feed_fields = ["feed_id", "target_profile_row", "field_to_fill", "source_row", "claim_policy", "current_status", "valid_for_claim", "claim_allowed"]
    decision_fields = ["decision_id", "condition", "decision", "result", "next_action", "valid_for_claim", "claim_allowed"]
    gate_fields = ["gate_id", "gate", "status", "reason", "valid_for_claim", "claim_allowed"]
    next_fields = ["next_id", "target_file", "target_script", "task", "success_condition", "do_not_do", "valid_for_claim", "claim_allowed"]

    write_csv(SOURCE_REGISTER_PATH, source_rows, source_fields)
    write_csv(ZERO_AUDIT_PATH, zero_audit, audit_fields)
    write_csv(BOUND_PATH, bound_rows, bound_fields)
    write_csv(SOURCE_ROWS_PATH, obstruction_rows, row_fields)
    write_csv(FEED_PATH, feed_rows, feed_fields)
    write_csv(DECISION_PATH, decisions, decision_fields)
    write_csv(CLAIM_GATES_PATH, claim_gates, gate_fields)
    write_csv(NEXT_PATH, next_rows, next_fields)

    formalization_recent = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*"):
            if path.is_file():
                mtime = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
                if mtime >= RUN_STARTED_UTC:
                    formalization_recent.append(path)

    csvs_to_parse = [
        SOURCE_REGISTER_PATH,
        ZERO_AUDIT_PATH,
        BOUND_PATH,
        SOURCE_ROWS_PATH,
        FEED_PATH,
        DECISION_PATH,
        CLAIM_GATES_PATH,
        NEXT_PATH,
    ]
    csv_parse_ok = True
    parse_details: list[str] = []
    for csv_path in csvs_to_parse:
        try:
            rows = load_csv(csv_path)
            parse_details.append(f"{csv_path.name}:{len(rows)}")
        except Exception as exc:  # noqa: BLE001
            csv_parse_ok = False
            parse_details.append(f"{csv_path.name}:ERROR:{exc}")

    all_sources_exist = all(bool(row["path_exists"]) for row in source_rows)
    all_needles_found = all(bool(row["needle_found"]) for row in source_rows)
    source_zero_blocked = any(row["audit_id"] == "SSA1213_4_source_side_total" and row["status"] == "SOURCE_SIDE_ZERO_BLOCKED" for row in zero_audit)
    absolute_bound_present = any(row["bound_id"] == "SSB1213_0_absolute_source_side" and " + " in row["bound_formula"] for row in bound_rows)
    obstruction_row_present = any(row["row_id"] == "SSR1213_0_G_source_side_bound" for row in obstruction_rows)
    feed_present = any(row["feed_id"] == "GUP1213_0_profile_update" for row in feed_rows)
    no_missing_claim_rows = all(not (row["valid_for_claim"] and "MISSING" in row["value"]) for row in obstruction_rows)
    no_claim = all(
        not bool(row.get("valid_for_claim")) and not bool(row.get("claim_allowed"))
        for row in zero_audit + bound_rows + obstruction_rows + feed_rows + decisions + claim_gates + next_rows
    )
    formalization_untouched = len(formalization_recent) == 0
    next_1214 = next_rows[0]["target_file"].startswith("1214-")

    validation_rows = [
        validation_row("VAL1213_0_sources_exist", "all cited local sources exist", all_sources_exist, f"{sum(bool(row['path_exists']) for row in source_rows)}/{len(source_rows)} sources exist"),
        validation_row("VAL1213_1_needles_found", "all cited source needles found", all_needles_found, f"{sum(bool(row['needle_found']) for row in source_rows)}/{len(source_rows)} needles found"),
        validation_row("VAL1213_2_source_zero_blocked", "source-side zero is not overclaimed", source_zero_blocked, "SSA1213_4 source-side total blocked"),
        validation_row("VAL1213_3_absolute_bound", "absolute source-side bound is present", absolute_bound_present, "SSB1213_0 present"),
        validation_row("VAL1213_4_obstruction_row", "source-side obstruction row is staged", obstruction_row_present, "SSR1213_0 present"),
        validation_row("VAL1213_5_profile_feed", "1212 Gres profile feed is staged", feed_present, "GUP1213_0 present"),
        validation_row("VAL1213_6_no_missing_claim_rows", "no row with MISSING is valid for claim", no_missing_claim_rows, "source-side rows remain nonclaim"),
        validation_row("VAL1213_7_nonclaim_policy", "all generated rows remain nonclaim", no_claim, "valid_for_claim=false and claim_allowed=false throughout"),
        validation_row("VAL1213_8_csv_parse", "all generated CSVs parse cleanly", csv_parse_ok, "; ".join(parse_details)),
        validation_row("VAL1213_9_formalization_untouched", "formalization-workbench untouched during run", formalization_untouched, f"formalization_recent_after_run_start_count={len(formalization_recent)}"),
        validation_row("VAL1213_10_next_target", "next target is staged", next_1214, next_rows[0]["target_file"]),
    ]
    validation_pass = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        validation_row(
            "VAL1213_11_overall",
            "overall 1213 validation",
            validation_pass,
            "1213 source-side obstruction bound pack is reproducible and nonclaim" if validation_pass else "one or more validation checks failed",
        )
    )
    validation_fields = ["check_id", "check", "status", "details", "valid_for_claim", "claim_allowed"]
    write_csv(VALIDATION_PATH, validation_rows, validation_fields)

    doc = f"""# 1213 Y5/R10 Gres Source-Side Obstruction Bound Or Hidden Species Zero

**Current verdict:** 1213 does **not** prove `G_source_side=0`. It stages the first absolute source-side obstruction bound that can feed `GRB1212_0_first_Gres_bound_profile`.

**Main progress:** the source-side debt is now `G_source_side_bound <= B_public_metric_frame + B_nonHilbert_support + B_species_weight + B_Meff_flux_calibration`. The leading derivation target is `B_species_weight`: kill it by parent-signing the no-source-only-slot grammar, or bound it explicitly.

**No hiding in measured G:** a common source normalization is calibration-only if universal and range/time/frame/species independent. Relative weights, non-Hilbert currents, support shifts, and measured-GM flux obstructions stay physical residuals.

## Source Register

{markdown_table(source_rows, source_fields)}

## Source-Side Zero Audit

{markdown_table(zero_audit, audit_fields)}

## Source-Side Bound Decomposition

{markdown_table(bound_rows, bound_fields)}

## Source-Side Obstruction Rows

{markdown_table(obstruction_rows, row_fields)}

## Gres Profile Feed Update

{markdown_table(feed_rows, feed_fields)}

## Decision Ledger

{markdown_table(decisions, decision_fields)}

## Claim Gates

{markdown_table(claim_gates, gate_fields)}

## Next Target

{markdown_table(next_rows, next_fields)}

## Validation

{markdown_table(validation_rows, validation_fields)}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")

    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"validation_pass={validation_pass}")
    print("G_source_side_zero_claimed=false")
    print("source_side_bound_row=SSR1213_0_G_source_side_bound")


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1212"
TITLE = "1212-Y5-R10-Gres-zero-source-side-EH-limit-or-first-profile-row"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
SOURCE_SIDE_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_SIDE_ZERO_ATTEMPT.csv"
LHS_PATH = OUT_DIR / f"{PACK_ID}_PARENT_LHS_EH_NEWTON_ATTEMPT.csv"
ZERO_SUMMARY_PATH = OUT_DIR / f"{PACK_ID}_GRES_ZERO_ATTEMPT_SUMMARY.csv"
PROFILE_PATH = OUT_DIR / f"{PACK_ID}_FIRST_GRES_BOUND_PROFILE_ROW.csv"
FEED_PATH = OUT_DIR / f"{PACK_ID}_CP_GRES_FEED_ROW.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1212_VALIDATION.csv"


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
            "source_id": "SRC1212_0_1211_next",
            "local_path": "1211-Y5-R10-Gres-norm-source-or-local-residual-zero-theorem.md",
            "needle": "NEXT1211_0_1212",
            "purpose": "handoff to G_res zero/source-side EH limit or first profile row",
        },
        {
            "source_id": "SRC1212_1_1211_decomposition",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1211_GRES_DEFINITION_AND_DECOMPOSITION.csv",
            "needle": "GDEF1211_1_decomposition",
            "purpose": "G_res component decomposition",
        },
        {
            "source_id": "SRC1212_2_1211_source_side",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1211_GRES_BOUND_DECOMPOSITION.csv",
            "needle": "GBD1211_3_source_side_residual",
            "purpose": "source-side residual bound form",
        },
        {
            "source_id": "SRC1212_3_1211_parent_LHS",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1211_GRES_BOUND_DECOMPOSITION.csv",
            "needle": "GBD1211_4_parent_left_hand_residual",
            "purpose": "parent left-hand EH/Newton residual bound form",
        },
        {
            "source_id": "SRC1212_4_956_source_spine",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_956_SOURCE_SIDE_GR_NEWTON_SPINE.csv",
            "needle": "SSG956_5_source_side_verdict",
            "purpose": "source-side GR/Newton spine says hidden/species residuals remain",
        },
        {
            "source_id": "SRC1212_5_1030_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1030_PUBLIC_METRIC_ACTION_CONTRACT.csv",
            "needle": "SPM1030_6_contract_verdict",
            "purpose": "single-public-metric source-side contract not current theorem",
        },
        {
            "source_id": "SRC1212_6_1031_nonproof",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1031_TERMINAL_PUBLIC_METRIC_PROOF_AUDIT.csv",
            "needle": "TPM1031_6_verdict",
            "purpose": "terminal-public-metric route not derived",
        },
        {
            "source_id": "SRC1212_7_1032_closure",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1032_SPM_CLOSURE_LEDGER.csv",
            "needle": "SPML1032_2_no_overclaim_policy",
            "purpose": "SPM closure cannot itself claim local GR/Newton",
        },
        {
            "source_id": "SRC1212_8_1013_flux",
            "local_path": "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md",
            "needle": "PFC1013_8_verdict",
            "purpose": "measured-GM/Pi_M J_H flux closure not derived",
        },
        {
            "source_id": "SRC1212_9_1008_EH_guard",
            "local_path": "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md",
            "needle": "CDS1008_2_EH_import_guard",
            "purpose": "EH import refused without MTS parent reduction",
        },
        {
            "source_id": "SRC1212_10_1008_theta_verdict",
            "local_path": "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md",
            "needle": "PVA1008_6_verdict",
            "purpose": "parent theta/Q_tau extraction fails current claim",
        },
        {
            "source_id": "SRC1212_11_1007_EH_guard",
            "local_path": "1007-Y5-R10-Htau-integrability-fixed-reference-theorem-or-symplectic-residual-row.md",
            "needle": "CG1007_1_EH_import_guard",
            "purpose": "EH covariant phase space cannot be used alone as MTS proof",
        },
        {
            "source_id": "SRC1212_12_04_vacuum_action",
            "local_path": "04-vacuum-reciprocity-action-contract.md",
            "needle": "vacuum_reciprocity_action_contract_locked_not_satisfied",
            "purpose": "motion-load local GR route still needs parent action theorem rather than imported Einstein equations",
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

    bridge_rows_in = load_csv(OUT_DIR / "P8_Y5_R10_1211_CP_GRES_PRESSURE_BRIDGE.csv")
    allowed_range = next(row for row in bridge_rows_in if row["bridge_id"] == "CPG1211_0_1210_range")["value_or_range"]

    source_side = [
        {
            "attempt_id": "SSZ1212_0_public_metric",
            "target_component": "DeltaJ_hidden",
            "needed_zero": "one parent-derived public coframe/metric for matter, source variation, clocks, photons, free fall, and readout",
            "evidence": "1030 writes the contract; 1031 rejects terminality-alone as proof; 1032 demotes SPM to explicit closure",
            "status": "NOT_DERIVED_CLOSURE_ONLY",
            "bound_if_not_zero": "Delta_public_metric_frame",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "SSZ1212_1_matter_functor",
            "target_component": "DeltaJ_hidden",
            "needed_zero": "ordinary matter functor factors only through terminal e_pub(q) with no shadow frame, marker, support, or non-Hilbert current slots",
            "evidence": "1031 counterexamples show matter can depend on non-terminal objects/labels unless parent action restricts the functor",
            "status": "NOT_DERIVED_EXTRA_MATTER_INTERFACE_PREMISE_MISSING",
            "bound_if_not_zero": "Delta_nonHilbert_plus_support",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "SSZ1212_2_species_weights",
            "target_component": "DeltaJ_species",
            "needed_zero": "source functor forgets species labels and excludes source-only relative weights",
            "evidence": "956 source spine is conditional; 1030/1031 keep source weights and labels as countermodels unless parent-signed",
            "status": "NOT_DERIVED_SOURCE_LABEL_FORGETTING_UNSIGNED",
            "bound_if_not_zero": "Delta_species_weight",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "SSZ1212_3_measured_GM",
            "target_component": "Delta_kappa_calibration",
            "needed_zero": "measured-GM/worldtube/source-normalization chain closes before orbital/PPN readout",
            "evidence": "1013 says d(Pi_M J_H)=0 and worldtube glue/calibration are not derived; obstruction rows remain unfilled",
            "status": "NOT_DERIVED_MEASURED_GM_FLUX_OBSTRUCTION_ACTIVE",
            "bound_if_not_zero": "Delta_Meff_flux_plus_calibration",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "SSZ1212_4_source_side_verdict",
            "target_component": "G_source_side",
            "needed_zero": "SSZ1212_0 through SSZ1212_3 all close in the same domain and same public metric",
            "evidence": "at least public metric, matter-interface restriction, species weights, and measured-GM closure remain unsigned",
            "status": "SOURCE_SIDE_ZERO_BLOCKED",
            "bound_if_not_zero": "||G_source_side|| <= ||Delta_public_metric_frame||+||Delta_nonHilbert_plus_support||+||Delta_species_weight||+||Delta_Meff_flux_plus_calibration||",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    parent_lhs = [
        {
            "attempt_id": "LHS1212_0_EH_operator",
            "target_component": "Delta_EH_operator",
            "needed_zero": "parent MTS field equation reduces to the Einstein-Hilbert/Newton operator in the selected local branch",
            "evidence": "1008 keeps EH as reference-only until MTS parent reduction/silence certificates are signed",
            "status": "NOT_DERIVED_EH_IMPORT_GUARD_ACTIVE",
            "bound_if_not_zero": "EH_limit_residual_norm",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "LHS1212_1_theta_Qtau",
            "target_component": "Delta_Qtau_parent",
            "needed_zero": "parent theta_MTS, J_tau, and Q_tau^MTS are extracted sector-by-sector with all retained pieces owned",
            "evidence": "1008 parent theta/Q_tau extraction verdict fails current claim; matter/source, projector, extra, boundary pieces remain unowned",
            "status": "NOT_DERIVED_PARENT_CHARGE_EXTRACTION_MISSING",
            "bound_if_not_zero": "theta_Qtau_extraction_residual",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "LHS1212_2_Bianchi_Ward",
            "target_component": "Delta_Bianchi_Ward",
            "needed_zero": "Bianchi/Ward identity is compatible with all retained sectors and does not merely assign ownership",
            "evidence": "older Noether/Ward gates state ownership is not a zero theorem; hidden/common-frame/source-weight countermodels remain legal",
            "status": "NOT_DERIVED_WARD_IDENTITY_NOT_ZERO_PROOF",
            "bound_if_not_zero": "Bianchi_Ward_residual_norm",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "LHS1212_3_motion_load_guard",
            "target_component": "Delta_GR_smuggling",
            "needed_zero": "motion-load/vacuum reciprocity action derives GR exterior stress balance instead of assuming Einstein equations",
            "evidence": "04-vacuum-reciprocity action contract remains locked-not-satisfied and warns against importing Einstein equations",
            "status": "NOT_DERIVED_GR_SMUGGLING_GUARD_ACTIVE",
            "bound_if_not_zero": "vacuum_reciprocity_parent_action_residual",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "LHS1212_4_parent_LHS_verdict",
            "target_component": "G_parent_LHS",
            "needed_zero": "LHS1212_0 through LHS1212_3 all close with source/equation paths and parent signatures",
            "evidence": "EH operator, parent charge extraction, Ward compatibility, and motion-load parent action theorem remain unsigned",
            "status": "PARENT_LHS_ZERO_BLOCKED",
            "bound_if_not_zero": "||G_parent_LHS|| <= ||Delta_EH_operator||+||Delta_Qtau_parent||+||Delta_Bianchi_Ward||+||Delta_GR_smuggling||+||higher_operator_tail||",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    zero_summary = [
        {
            "summary_id": "GZS1212_0_if_theorem",
            "statement": "If source-side zero, parent-LHS EH/Newton zero, scalar exactness, and boundary/harmonic silence all close in one domain, then G_res_norm=0.",
            "result": "FORMAL_IF_THEOREM_WRITTEN",
            "why_not_claim": "source-side and parent-LHS attempts fail here; scalar and boundary components were already blocked in 1211",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "summary_id": "GZS1212_1_actual_verdict",
            "statement": "Current corpus does not prove G_res_norm=0.",
            "result": "ZERO_THEOREM_FAILS_CURRENT_CORPUS",
            "why_not_claim": "SPM is closure-only, measured-GM flux closure fails, EH import is guarded, and parent theta/Q_tau is not extracted",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "summary_id": "GZS1212_2_fallback",
            "statement": "Use an absolute Gres_bound profile row, not a fitted residual or cancellation.",
            "result": "FIRST_PROFILE_ROW_STAGED",
            "why_not_claim": "all profile components remain MISSING or conditional, so row is a nonclaim source target",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    profile_rows = [
        {
            "profile_id": "GRB1212_0_first_Gres_bound_profile",
            "domain_id": "MISSING_LOCAL_DOMAIN",
            "norm_id": "MISSING_SAME_NORM_AS_DT_AND_PLOC",
            "coframe": "MISSING_PUBLIC_COFRAME",
            "gauge": "MISSING_GAUGE",
            "formula": "Gres_bound = P_loc_norm*(scalar_exactness_bound + source_side_bound + parent_LHS_bound + boundary_harmonic_bound + profile_remainder_bound)",
            "scalar_exactness_bound": "MISSING_SCALAR_EXACTNESS_DEFECT",
            "source_side_bound": "MISSING_SOURCE_SIDE_BOUND",
            "parent_LHS_bound": "MISSING_PARENT_LHS_BOUND",
            "boundary_harmonic_bound": "MISSING_BOUNDARY_HARMONIC_BOUND",
            "profile_remainder_bound": "MISSING_PROFILE_REMAINDER_BOUND",
            "Gres_bound_value": "MISSING",
            "units": "same_as_G_res_norm",
            "source_path": "MISSING_SOURCE_PATH",
            "current_status": "SOURCE_READY_NONCLAIM_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    feed_rows = [
        {
            "feed_id": "CGF1212_0_1210_product_feed",
            "input_row": "GRB1212_0_first_Gres_bound_profile",
            "target_quantity": "C_P*Gres_bound",
            "allowed_range_from_1211": allowed_range,
            "formula": "C_P*Gres_bound <= allowed_CpGres_product",
            "missing_inputs": "C_P;Gres_bound_value;domain/norm compatibility;units",
            "current_status": "FEED_SCHEMA_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    decisions = [
        {
            "decision_id": "DEC1212_0_verdict",
            "condition": "Can source-side + parent-LHS closure prove G_res=0 now?",
            "decision": "No. Both halves remain unsigned, and SPM is closure-only.",
            "result": "G_res zero theorem fails current corpus, but exact missing pieces are now named.",
            "next_action": "attack source-side obstruction first because existing 1013 rows give a concrete obstruction vector.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1212_1_profile",
            "condition": "If zero fails, what object feeds testing next?",
            "decision": "Use GRB1212_0_first_Gres_bound_profile as the same-norm nonclaim row feeding the 1210 C_P*G_res product map.",
            "result": "G_res is now test-plumbing ready once component bounds are filled.",
            "next_action": "derive or bound G_source_side components DeltaJ_hidden, DeltaJ_species, Delta_kappa_calibration, and Delta_Meff_flux.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1212_0_source_side_zero",
            "gate": "G_source_side=0",
            "status": "BLOCKED",
            "reason": "public metric theorem, source label forgetting, hidden current silence, and measured-GM closure are not parent-signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1212_1_parent_LHS_zero",
            "gate": "G_parent_LHS=0",
            "status": "BLOCKED",
            "reason": "EH import guard, parent theta/Q_tau extraction, Bianchi/Ward residual, and motion-load action theorem remain open",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1212_2_Gres_zero",
            "gate": "G_res_norm=0",
            "status": "BLOCKED",
            "reason": "source-side and parent-LHS closure fail, and scalar/boundary components remain blocked from 1211",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1212_3_Gres_profile_numeric",
            "gate": "numeric Gres_bound row",
            "status": "BLOCKED",
            "reason": "first profile row is source-ready but all component values remain missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1212_4_local_GR_R10",
            "gate": "local-GR/R10 pass",
            "status": "BLOCKED",
            "reason": "1212 is a theorem-failure/source-row checkpoint only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_rows = [
        {
            "next_id": "NEXT1212_0_1213",
            "target_file": "1213-Y5-R10-Gres-source-side-obstruction-bound-or-hidden-species-zero.md",
            "target_script": "scripts/Y5_R10_Gres_source_side_obstruction_bound_or_hidden_species_zero.py",
            "task": "derive G_source_side=0 from source functor/hidden-current/species-label/measured-GM closure, or fill the first source-side obstruction bound feeding GRB1212_0",
            "success_condition": "G_source_side is theorem-zero, or a nonclaim absolute bound row exists for DeltaJ_hidden, DeltaJ_species, Delta_kappa_calibration, and Delta_Meff_flux",
            "do_not_do": "do not treat SPM closure as derived, do not import EH/Newton or orbital GM to prove source normalization, do not edit formalization-workbench, do not push GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    source_fields = ["source_id", "local_path", "needle", "purpose", "path_exists", "needle_found", "valid_for_claim", "claim_allowed"]
    source_side_fields = ["attempt_id", "target_component", "needed_zero", "evidence", "status", "bound_if_not_zero", "valid_for_claim", "claim_allowed"]
    lhs_fields = ["attempt_id", "target_component", "needed_zero", "evidence", "status", "bound_if_not_zero", "valid_for_claim", "claim_allowed"]
    summary_fields = ["summary_id", "statement", "result", "why_not_claim", "valid_for_claim", "claim_allowed"]
    profile_fields = ["profile_id", "domain_id", "norm_id", "coframe", "gauge", "formula", "scalar_exactness_bound", "source_side_bound", "parent_LHS_bound", "boundary_harmonic_bound", "profile_remainder_bound", "Gres_bound_value", "units", "source_path", "current_status", "valid_for_claim", "claim_allowed"]
    feed_fields = ["feed_id", "input_row", "target_quantity", "allowed_range_from_1211", "formula", "missing_inputs", "current_status", "valid_for_claim", "claim_allowed"]
    decision_fields = ["decision_id", "condition", "decision", "result", "next_action", "valid_for_claim", "claim_allowed"]
    gate_fields = ["gate_id", "gate", "status", "reason", "valid_for_claim", "claim_allowed"]
    next_fields = ["next_id", "target_file", "target_script", "task", "success_condition", "do_not_do", "valid_for_claim", "claim_allowed"]

    write_csv(SOURCE_REGISTER_PATH, source_rows, source_fields)
    write_csv(SOURCE_SIDE_PATH, source_side, source_side_fields)
    write_csv(LHS_PATH, parent_lhs, lhs_fields)
    write_csv(ZERO_SUMMARY_PATH, zero_summary, summary_fields)
    write_csv(PROFILE_PATH, profile_rows, profile_fields)
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
        SOURCE_SIDE_PATH,
        LHS_PATH,
        ZERO_SUMMARY_PATH,
        PROFILE_PATH,
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
    source_side_blocked = any(row["attempt_id"] == "SSZ1212_4_source_side_verdict" and row["status"] == "SOURCE_SIDE_ZERO_BLOCKED" for row in source_side)
    lhs_blocked = any(row["attempt_id"] == "LHS1212_4_parent_LHS_verdict" and row["status"] == "PARENT_LHS_ZERO_BLOCKED" for row in parent_lhs)
    zero_fail_recorded = any(row["summary_id"] == "GZS1212_1_actual_verdict" and row["result"] == "ZERO_THEOREM_FAILS_CURRENT_CORPUS" for row in zero_summary)
    profile_ready = any(row["profile_id"] == "GRB1212_0_first_Gres_bound_profile" for row in profile_rows)
    feed_ready = any(row["feed_id"] == "CGF1212_0_1210_product_feed" for row in feed_rows)
    no_missing_claim_rows = all(not (row["valid_for_claim"] and "MISSING" in row["Gres_bound_value"]) for row in profile_rows)
    no_claim = all(
        not bool(row.get("valid_for_claim")) and not bool(row.get("claim_allowed"))
        for row in source_side + parent_lhs + zero_summary + profile_rows + feed_rows + decisions + claim_gates + next_rows
    )
    formalization_untouched = len(formalization_recent) == 0
    next_1213 = next_rows[0]["target_file"].startswith("1213-")

    validation_rows = [
        validation_row("VAL1212_0_sources_exist", "all cited local sources exist", all_sources_exist, f"{sum(bool(row['path_exists']) for row in source_rows)}/{len(source_rows)} sources exist"),
        validation_row("VAL1212_1_needles_found", "all cited source needles found", all_needles_found, f"{sum(bool(row['needle_found']) for row in source_rows)}/{len(source_rows)} needles found"),
        validation_row("VAL1212_2_source_side_blocked", "source-side zero is not overclaimed", source_side_blocked, "SSZ1212_4 source-side zero blocked"),
        validation_row("VAL1212_3_parent_lhs_blocked", "parent-LHS EH/Newton zero is not overclaimed", lhs_blocked, "LHS1212_4 parent-LHS zero blocked"),
        validation_row("VAL1212_4_zero_failure", "G_res zero theorem failure is recorded", zero_fail_recorded, "GZS1212_1 actual verdict"),
        validation_row("VAL1212_5_profile_row", "first Gres_bound profile row is staged", profile_ready, "GRB1212_0 present"),
        validation_row("VAL1212_6_cp_feed", "C_P*Gres feed row is staged", feed_ready, "CGF1212_0 present"),
        validation_row("VAL1212_7_no_missing_claim_rows", "no row with MISSING is valid for claim", no_missing_claim_rows, "profile row remains nonclaim"),
        validation_row("VAL1212_8_nonclaim_policy", "all generated rows remain nonclaim", no_claim, "valid_for_claim=false and claim_allowed=false throughout"),
        validation_row("VAL1212_9_csv_parse", "all generated CSVs parse cleanly", csv_parse_ok, "; ".join(parse_details)),
        validation_row("VAL1212_10_formalization_untouched", "formalization-workbench untouched during run", formalization_untouched, f"formalization_recent_after_run_start_count={len(formalization_recent)}"),
        validation_row("VAL1212_11_next_target", "next target is staged", next_1213, next_rows[0]["target_file"]),
    ]
    validation_pass = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        validation_row(
            "VAL1212_12_overall",
            "overall 1212 validation",
            validation_pass,
            "1212 G_res zero attempt and first profile row are reproducible and nonclaim" if validation_pass else "one or more validation checks failed",
        )
    )
    validation_fields = ["check_id", "check", "status", "details", "valid_for_claim", "claim_allowed"]
    write_csv(VALIDATION_PATH, validation_rows, validation_fields)

    doc = f"""# 1212 Y5/R10 Gres Zero Source-Side EH Limit Or First Profile Row

**Current verdict:** 1212 does **not** prove `G_res=0`. The proof fails for useful, named reasons: source-side closure is still not parent-derived, and the parent left-hand EH/Newton reduction is still guarded against GR import.

**Main progress:** the strong if-theorem is now explicit. `G_res=0` would follow if source-side hidden/species/calibration residuals vanish, the parent field equation reduces to EH/Newton, scalar exactness closes, and boundary/harmonic pieces vanish in one common domain. Since those gates do not close, `GRB1212_0_first_Gres_bound_profile` is staged as the first same-norm nonclaim bound row.

**Testing bridge:** `GRB1212_0` feeds the 1210/1211 product condition `C_P*Gres_bound <= allowed_CpGres_product`, whose current private bracket range is `{allowed_range}`. This remains nonclaim because `C_P`, units, and every profile component are still missing.

## Source Register

{markdown_table(source_rows, source_fields)}

## Source-Side Zero Attempt

{markdown_table(source_side, source_side_fields)}

## Parent LHS EH/Newton Attempt

{markdown_table(parent_lhs, lhs_fields)}

## G_res Zero Attempt Summary

{markdown_table(zero_summary, summary_fields)}

## First Gres Bound Profile Row

{markdown_table(profile_rows, profile_fields)}

## C_P Gres Feed Row

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
    print("G_res_zero_claimed=false")
    print("first_Gres_bound_profile_row=GRB1212_0_first_Gres_bound_profile")


if __name__ == "__main__":
    main()

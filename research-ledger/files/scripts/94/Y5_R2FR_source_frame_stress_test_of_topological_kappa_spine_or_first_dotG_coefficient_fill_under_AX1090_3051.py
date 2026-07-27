from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3051"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3051-Y5-R2FR-source-frame-stress-test-of-topological-kappa-spine-or-first-dotG-coefficient-fill-under-AX1090.md"
DOTG_TARGET = RESIDUALS / "P8_time_drift_residual_or_zero.csv"

SOURCE_PATHS = {
    "SRC3051_00_3050_doc": ROOT / "3050-Y5-R2FR-parent-topological-kappa-spine-with-Gref-lock-or-scalar-kappa-coefficient-fill-under-AX1090.md",
    "SRC3051_01_3050_spine": RESIDUALS / "P8_Y5_R2FR_3050_PARENT_TOPOLOGICAL_KAPPA_SPINE_CANDIDATE.csv",
    "SRC3051_02_3050_variation": RESIDUALS / "P8_Y5_R2FR_3050_VARIATION_AND_LOCAL_LIMIT_AUDIT.csv",
    "SRC3051_03_3050_gref": RESIDUALS / "P8_Y5_R2FR_3050_GREF_LOCK_AND_AW_NORMALIZATION_AUDIT.csv",
    "SRC3051_04_3050_gates": RESIDUALS / "P8_Y5_R2FR_3050_PARENT_SIGNATURE_GATES.csv",
    "SRC3051_05_3050_next": RESIDUALS / "P8_Y5_R2FR_3050_NEXT_TARGET.csv",
    "SRC3051_06_topological_clause": RESIDUALS / "P8_CONSTANT_KAPPA_TOPOLOGICAL_ZEROFORM_CLAUSE.csv",
    "SRC3051_07_global_contract": RESIDUALS / "P8_global_coupling_superselection_CONTRACT.csv",
    "SRC3051_08_constant_kappa_contract": RESIDUALS / "P8_constant_universal_Geff_kappa_CONTRACT.csv",
    "SRC3051_09_same_coframe_clause": RESIDUALS / "P8_Y5_SAME_COFRAME_PARENT_CLAUSE.csv",
    "SRC3051_10_same_coframe_variation": RESIDUALS / "P8_Y5_SAME_COFRAME_VARIATION_DERIVATION.csv",
    "SRC3051_11_same_coframe_bound": RESIDUALS / "P8_Y5_SAME_COFRAME_BOUND_UPDATE.csv",
    "SRC3051_12_single_frame_gate": PARENT_ACTION / "single_observed_frame_parent_action_gate_2959_NOT_DERIVED.csv",
    "SRC3051_13_matter_pullback": PARENT_ACTION / "matter_pullback_descent_audit_2956_NOT_DERIVED.csv",
    "SRC3051_14_source_readout": PARENT_ACTION / "source_readout_lock_theorem_attempt_3036_NOT_SIGNED.csv",
    "SRC3051_15_WPhi_readout": PARENT_ACTION / "W_equals_Phi_parent_readout_theorem_3042_NOT_SIGNED.csv",
    "SRC3051_16_zero_stress_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_2235_ZERO_STRESS_VARIATION_GATE.csv",
    "SRC3051_17_dotG_bound_source": RESIDUALS / "P8_Y5_R2FR_2933_COUPLING_BOUND_SOURCE_ACQUISITION.csv",
    "SRC3051_18_dotG_projection_gate": PARENT_ACTION / "DotG_to_kappa_projection_gate_2933_NONCLAIM.csv",
    "SRC3051_19_dotG_target": DOTG_TARGET,
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3051_SOURCE_REGISTER.csv",
    "stress_tests": RESIDUALS / "P8_Y5_R2FR_3051_TOPOLOGICAL_KAPPA_STRESS_TEST_MATRIX.csv",
    "source_frame": RESIDUALS / "P8_Y5_R2FR_3051_SOURCE_FRAME_READOUT_STRESS.csv",
    "topological_stress": RESIDUALS / "P8_Y5_R2FR_3051_TOPOLOGICAL_STRESS_AND_COMPANION_AUDIT.csv",
    "dotg_fill": RESIDUALS / "P8_Y5_R2FR_3051_DOTG_FIRST_COEFFICIENT_FILL_NONCLAIM.csv",
    "dotg_target_audit": RESIDUALS / "P8_Y5_R2FR_3051_DOTG_TARGET_UPDATE_AUDIT.csv",
    "claim_status": RESIDUALS / "P8_Y5_R2FR_3051_CLAIM_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3051_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3051_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3051_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3051_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "stress_copy": PARENT_ACTION / "topological_kappa_stress_test_matrix_3051_PARTIAL_CONDITIONAL.csv",
    "source_frame_copy": PARENT_ACTION / "source_frame_readout_stress_3051_NOT_SIGNED.csv",
    "topological_stress_copy": PARENT_ACTION / "topological_stress_and_companion_audit_3051_CONDITIONAL.csv",
    "dotg_fill_copy": LOCAL_BOUNDS / "dotG_first_coefficient_fill_3051_NONCLAIM.csv",
    "dotg_target_audit_copy": LOCAL_BOUNDS / "dotG_target_update_audit_3051_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3051_SOURCE_FRAME_READOUT_LOCK_OR_DOTG_NUMERIC_RUNNER_NEXT_NONCLAIM.csv",
}

for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC, DOTG_TARGET]:
    path.parent.mkdir(parents=True, exist_ok=True)


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def as_str(value: Any) -> str:
    return "" if value is None else str(value)


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y", "pass", "passed"}


def csv_ok(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        with path.open("r", newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for output_row in output_rows:
        for key in output_row:
            if key not in fieldnames:
                fieldnames.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for output_row in output_rows:
            writer.writerow({key: as_str(output_row.get(key, "")) for key in fieldnames})


def append_unique_csv(path: Path, new_row: dict[str, Any], key_field: str) -> tuple[bool, int]:
    existing = rows(path)
    if any(row.get(key_field) == as_str(new_row.get(key_field)) for row in existing):
        return False, len(existing)
    merged_rows: list[dict[str, Any]] = [*existing, new_row]
    write_csv(path, merged_rows)
    return True, len(merged_rows)


def under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def has_claim_true(input_rows: list[dict[str, str] | dict[str, Any]]) -> bool:
    claim_fields = {"valid_for_claim", "claim_allowed", "valid_prediction_row", "score_ready", "claim_active", "stress_passes_for_current_MTS"}
    return any(boolish(row.get(field, "false")) for row in input_rows for field in claim_fields)


def base(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "timestamp_utc": RUN_UTC,
        "score_ready": "false",
        "valid_prediction_row": "false",
        "valid_for_claim": "false",
        "claim_allowed": "false",
        **row,
    }


def md_table(table_rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not table_rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, sep]
    for row in table_rows:
        values = []
        for column in columns:
            value = as_str(row.get(column, "")).replace("\n", " ").replace("|", "/")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def copy_csv(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


source_register = [
    base(
        {
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "parse_ok": csv_ok(path) if path.suffix.lower() == ".csv" and path.exists() else "",
            "row_count": len(rows(path)) if path.suffix.lower() == ".csv" and path.exists() else "",
            "role": source_id.split("_", 2)[-1],
            "status": "PRESENT" if path.exists() else "MISSING_BLOCKER",
        }
    )
    for source_id, path in SOURCE_PATHS.items()
]

stress_rows = [
    base(
        {
            "test_id": "STRESS3051_0_active_parent",
            "gate": "active parent-action adoption",
            "candidate_internal_result": "CANDIDATE_WRITTEN",
            "current_MTS_result": "FAIL_NOT_ADOPTED",
            "reason": "3050 writes a candidate spine but does not promote it as active theory",
            "stress_passes_for_current_MTS": "false",
            "unlocks_if_signed": "allows d kappa_eff theorem to be used rather than only cited",
        }
    ),
    base(
        {
            "test_id": "STRESS3051_1_source_blindness",
            "gate": "matter/source blindness of kappa_eff",
            "candidate_internal_result": "PASS_IF_S_MATTER_DEPENDS_ONLY_ON_g_obs_AND_psi",
            "current_MTS_result": "FAIL_SOURCE_READOUT_NOT_SIGNED",
            "reason": "same-coframe/source-readout clauses exist as conditional rows, not active parent derivations",
            "stress_passes_for_current_MTS": "false",
            "unlocks_if_signed": "kills species/source/range labels on kappa_eff",
        }
    ),
    base(
        {
            "test_id": "STRESS3051_2_same_frame_readout",
            "gate": "same frame for G_ref/W/Phi/T_obs",
            "candidate_internal_result": "PASS_IF_G_REF_READOUT_USES_SAME_g_obs_AS_WEAK_FIELD_PHI",
            "current_MTS_result": "FAIL_W_PHI_AND_SOURCE_NORMALIZATION_NOT_SIGNED",
            "reason": "W=Phi and source readout lock remain conditional/not signed in 3042/3036/3050",
            "stress_passes_for_current_MTS": "false",
            "unlocks_if_signed": "turns G_ref lock into A_W=1 without denominator cheating",
        }
    ),
    base(
        {
            "test_id": "STRESS3051_3_topological_stress",
            "gate": "metric stress silence of integral kappa_eff dA_3",
            "candidate_internal_result": "PASS_IF_dA3_TERM_IS_TRUE_METRIC_INDEPENDENT_TOP_FORM",
            "current_MTS_result": "CONDITIONAL_NOT_PARENT_SIGNED",
            "reason": "as a top-form integral it has no metric stress, but the field/variation ownership is not active MTS",
            "stress_passes_for_current_MTS": "false",
            "unlocks_if_signed": "prevents hidden non-EH stress in the local branch",
        }
    ),
    base(
        {
            "test_id": "STRESS3051_4_kappa_companion",
            "gate": "kappa companion equation does not reintroduce local force",
            "candidate_internal_result": "PASS_IF_dA3_ABSORBS_GLOBAL_EH_DENSITY_AND_A3_HAS_NO_MATTER_READOUT",
            "current_MTS_result": "CONDITIONAL_UNRESOLVED",
            "reason": "delta kappa gives a companion equation; it is safe only if A3 remains topological/no-readout",
            "stress_passes_for_current_MTS": "false",
            "unlocks_if_signed": "keeps dA3 equation from becoming scalar fifth-force hair",
        }
    ),
    base(
        {
            "test_id": "STRESS3051_5_second_order",
            "gate": "second-order PPN/source-normalized beta silence",
            "candidate_internal_result": "NOT_TESTED_BY_MINIMAL_KAPPA_SPINE",
            "current_MTS_result": "DEFERRED_BLOCKER",
            "reason": "3050 only addresses coupling normalization; beta/source-normalized PPN still needs later expansion",
            "stress_passes_for_current_MTS": "false",
            "unlocks_if_signed": "needed before local GR rather than only Newton coefficient",
        }
    ),
]

source_frame_rows = [
    base(
        {
            "frame_test_id": "SF3051_0_same_coframe_clause",
            "object": "same observed coframe",
            "conditional_result": "delta_frame_source=0 if e_obs=e_matter=e_source=e_clock=e_photon=e_orbit is parent-adopted",
            "current_status": "CONDITIONAL_CLAUSE_WRITTEN_NOT_CURRENT_MTS_DERIVED",
            "blocking_source": str(SOURCE_PATHS["SRC3051_09_same_coframe_clause"]),
            "residual_if_failed": "delta_frame_source; dln_Geff_dt frame ambiguity",
        }
    ),
    base(
        {
            "frame_test_id": "SF3051_1_source_readout",
            "object": "source variation readout",
            "conditional_result": "source and matter variations use one g_obs/Hilbert source if source-readout lock is signed",
            "current_status": "NOT_SIGNED",
            "blocking_source": str(SOURCE_PATHS["SRC3051_14_source_readout"]),
            "residual_if_failed": "source-normalization and WEP-source-charge rows remain active",
        }
    ),
    base(
        {
            "frame_test_id": "SF3051_2_WPhi",
            "object": "W/Phi/G_ref readout",
            "conditional_result": "A_W=1 only if W and Phi_metric use the same source-normalized weak-field readout",
            "current_status": "NOT_SIGNED",
            "blocking_source": str(SOURCE_PATHS["SRC3051_15_WPhi_readout"]),
            "residual_if_failed": "epsilon_Gref; D_WPhi; A_W mismatch",
        }
    ),
]

topological_rows = [
    base(
        {
            "topo_test_id": "TOPO3051_0_metric_stress",
            "object": "integral_M kappa_eff dA_3",
            "calculation": "delta_g integral_M kappa_eff dA_3 = 0 if kappa_eff and A_3 are metric-independent differential forms and no Hodge star/metric volume is used",
            "candidate_result": "CONDITIONAL_STRESS_SILENCE_DERIVED",
            "current_status": "NOT_ACTIVE_PARENT_SIGNED",
            "remaining_risk": "metric-dependent representative, boundary mass-channel leakage, or hidden readout",
        }
    ),
    base(
        {
            "topo_test_id": "TOPO3051_1_kappa_companion",
            "object": "delta kappa_eff equation",
            "calculation": "delta_kappa S_parent gives dA_3 - (1/(2*kappa_eff^2))*epsilon_g R = 0 up to convention and boundary terms",
            "candidate_result": "SAFE_ONLY_IF_A3_IS_NO_READOUT_GLOBAL_FLUX",
            "current_status": "UNRESOLVED_COMPANION_EQUATION",
            "remaining_risk": "A3 flux becomes a local scalar/force/source-current channel",
        }
    ),
    base(
        {
            "topo_test_id": "TOPO3051_2_Bianchi",
            "object": "Bianchi/source conservation",
            "calculation": "with d kappa_eff=0, nabla_mu G^{mu nu}=0 implies nabla_mu T^{mu nu}=0 on matter shell; without adoption retain kappa_eff^-1 T nabla kappa_eff",
            "candidate_result": "CONDITIONAL_BIANCHI_EXCHANGE_ZERO",
            "current_status": "NOT_PARENT_DERIVED",
            "remaining_risk": "q_loc kappa exchange and source-normalization drift",
        }
    ),
]

dotg_fill_row = {
    "row_id": "TD3051_0_first_dotG_coefficient_fill_nonclaim",
    "component_id": "P8_Geff_time_drift",
    "observable": "Gdot_over_G",
    "symbol": "dln_Geff_dt",
    "formula": "dln_Geff_dt = D_t ln(kappa_eff c^4/(8*pi)) plus any unsigned source/frame readout drift",
    "candidate_value": "MISSING_PARENT_ZERO_OR_NUMERIC_DOTG_COEFFICIENT",
    "bound_or_target": "9.6e-15 yr^-1 internal local-GR lock; 4.0e-14 yr^-1 MESSENGER comparator recorded in 2933",
    "units": "yr^-1",
    "source_path": f"{SOURCE_PATHS['SRC3051_17_dotG_bound_source']};{SOURCE_PATHS['SRC3051_18_dotG_projection_gate']};{SOURCE_PATHS['SRC3051_19_dotG_target']}",
    "empirical_provenance": "2933 source-backed dotG/G comparator exists, but dotG-to-kappa projection remains unsigned",
    "derivation_status": "FIRST_DOTG_COEFFICIENT_FILL_NONCLAIM_AFTER_3051_STRESS_TEST",
    "score_ready": "false",
    "valid_prediction_row": "false",
    "valid_for_claim": "false",
    "claim_allowed": "false",
    "next_action": "derive source-frame/stress-safe topological kappa adoption or fill numeric dln_Geff_dt coefficient from parent scalar-kappa dynamics",
    "timestamp_utc": RUN_UTC,
}

appended, dotg_row_count = append_unique_csv(DOTG_TARGET, dotg_fill_row, "row_id")
dotg_target_rows = rows(DOTG_TARGET)

dotg_fill_rows = [
    base(
        {
            "fill_id": "DOTG3051_0_target_append",
            "target_file": str(DOTG_TARGET),
            "row_id": dotg_fill_row["row_id"],
            "appended_now": appended,
            "target_row_count": dotg_row_count,
            "candidate_value": dotg_fill_row["candidate_value"],
            "bound_or_target": dotg_fill_row["bound_or_target"],
            "source_path": dotg_fill_row["source_path"],
            "status": "NONCLAIM_FILL_ROW_PRESENT",
        }
    )
]

dotg_target_audit_rows = [
    base(
        {
            "audit_id": "DTA3051_0_parse",
            "target_file": str(DOTG_TARGET),
            "exists": DOTG_TARGET.exists(),
            "parse_ok": csv_ok(DOTG_TARGET),
            "row_count": len(dotg_target_rows),
            "contains_3051_row": any(row.get("row_id") == dotg_fill_row["row_id"] for row in dotg_target_rows),
            "claim_true_rows": sum(1 for row in dotg_target_rows if has_claim_true([row])),
            "missing_marker_rows": sum(1 for row in dotg_target_rows if "MISSING" in "\n".join(row.values()).upper()),
            "status": "DOTG_TARGET_UPDATED_NONCLAIM",
        }
    )
]

claim_rows = [
    base(
        {
            "claim_id": "CLAIM3051_0_topological_stress",
            "claim": "topological kappa stress silence is internally derived for the candidate",
            "status": "YES_CONDITIONAL_CANDIDATE_ONLY",
            "claim_active": "false",
            "reason": "metric-independent top-form has zero metric stress, but active parent adoption and no-readout clauses are unsigned",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3051_1_source_frame",
            "claim": "source/frame readout is solved",
            "status": "NO_NOT_SIGNED",
            "claim_active": "false",
            "reason": "same observed coframe/source readout clauses are conditional, not current-MTS derivations",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3051_2_AW_Newton",
            "claim": "A_W=1/Newton coefficient is active",
            "status": "NO_CONDITIONAL_ONLY",
            "claim_active": "false",
            "reason": "G_ref/W/Phi/source same-frame lock remains unsigned",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3051_3_dotG",
            "claim": "dln_Geff_dt passes the bound",
            "status": "NO_FILL_ROW_NONCLAIM",
            "claim_active": "false",
            "reason": "3051 adds a fill row but no parent zero or numeric coefficient",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3051_0_stress",
            "question": "Does the 3050 candidate spine survive stress testing internally?",
            "answer": "PARTIALLY_YES_AS_CONDITIONAL_CANDIDATE",
            "reason": "metric-independent topological stress and no-readout source blindness can work by construction",
            "action": "keep parent-spine route alive",
        }
    ),
    base(
        {
            "decision_id": "DEC3051_1_promotion",
            "question": "Can it be promoted to current MTS local GR?",
            "answer": "NO",
            "reason": "source/readout/same-frame/active-adoption gates remain unsigned",
            "action": "do not claim A_W/Newton/PPN/local-GR",
        }
    ),
    base(
        {
            "decision_id": "DEC3051_2_fallback",
            "question": "Did 3051 activate the dotG fallback?",
            "answer": "YES_NONCLAIM",
            "reason": "at least one stress gate fails for current MTS, so the first dln_Geff_dt fill row is now present",
            "action": "3052 should attack source-frame readout lock or fill numeric dotG coefficient",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3051_0_3052",
            "next_checkpoint": "3052-Y5-R2FR-source-frame-readout-lock-for-Gref-WPhi-or-dotG-numeric-coefficient-runner-under-AX1090.md",
            "script": "scripts/Y5_R2FR_source_frame_readout_lock_for_Gref_WPhi_or_dotG_numeric_coefficient_runner_under_AX1090_3052.py",
            "mission": "try to sign the same-frame G_ref/W/Phi/source readout lock under the topological kappa spine; if not, run the dln_Geff_dt numeric coefficient runner against the 3051 fill row",
            "starting_equation": "A_W = kappa_eff c^4/(8*pi*G_ref) = 1 only if G_ref, W, Phi_metric and T_obs share one source-normalized observed frame",
            "claim_policy": "no Newton/local-GR claim from conditional topological stress or dotG fill rows",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["stress_tests"], stress_rows)
write_csv(OUTPUTS["source_frame"], source_frame_rows)
write_csv(OUTPUTS["topological_stress"], topological_rows)
write_csv(OUTPUTS["dotg_fill"], dotg_fill_rows)
write_csv(OUTPUTS["dotg_target_audit"], dotg_target_audit_rows)
write_csv(OUTPUTS["claim_status"], claim_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["next"], next_rows)

copy_csv(OUTPUTS["stress_tests"], BRANCH_OUTPUTS["stress_copy"])
copy_csv(OUTPUTS["source_frame"], BRANCH_OUTPUTS["source_frame_copy"])
copy_csv(OUTPUTS["topological_stress"], BRANCH_OUTPUTS["topological_stress_copy"])
copy_csv(OUTPUTS["dotg_fill"], BRANCH_OUTPUTS["dotg_fill_copy"])
copy_csv(OUTPUTS["dotg_target_audit"], BRANCH_OUTPUTS["dotg_target_audit_copy"])
copy_csv(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

branch_rows = [
    base(
        {
            "copy_id": copy_id,
            "destination": str(path),
            "exists": path.exists(),
            "row_count": len(rows(path)) if path.exists() else 0,
            "description": "3051 branch copy",
        }
    )
    for copy_id, path in BRANCH_OUTPUTS.items()
]
write_csv(OUTPUTS["branches"], branch_rows)

if PYCACHE.exists():
    shutil.rmtree(PYCACHE)

non_validation_csv_paths = [
    OUTPUTS["sources"],
    OUTPUTS["stress_tests"],
    OUTPUTS["source_frame"],
    OUTPUTS["topological_stress"],
    OUTPUTS["dotg_fill"],
    OUTPUTS["dotg_target_audit"],
    OUTPUTS["claim_status"],
    OUTPUTS["decision"],
    OUTPUTS["next"],
    OUTPUTS["branches"],
    *BRANCH_OUTPUTS.values(),
    DOTG_TARGET,
]

all_output_rows: list[dict[str, str]] = []
for path in non_validation_csv_paths:
    all_output_rows.extend(rows(path))

generated_paths = [DOC, *OUTPUTS.values(), *BRANCH_OUTPUTS.values(), DOTG_TARGET]
formalization_generated_hits = [path for path in generated_paths if FORMALIZATION.exists() and under(path, FORMALIZATION)]

stress_current_failures = [row for row in stress_rows if not boolish(row["stress_passes_for_current_MTS"])]

validation_rows = [
    base({"validation_id": "VAL3051_00_sources_exist", "passed": all(boolish(row["exists"]) for row in source_register), "requirement": "all cited source paths exist", "evidence": OUTPUTS["sources"].name}),
    base({"validation_id": "VAL3051_01_csv_parse", "passed": all(csv_ok(path) for path in non_validation_csv_paths), "requirement": "all generated, branch-copy, and updated dotG CSVs parse cleanly", "evidence": "csv.DictReader parse check"}),
    base({"validation_id": "VAL3051_02_stress_tests_cover_gates", "passed": len(stress_rows) >= 6, "requirement": "source/frame/stress/companion/PPN stress gates are covered", "evidence": OUTPUTS["stress_tests"].name}),
    base({"validation_id": "VAL3051_03_candidate_partial_survives", "passed": any(row["test_id"] == "STRESS3051_3_topological_stress" and row["candidate_internal_result"].startswith("PASS_IF") for row in stress_rows), "requirement": "candidate topological stress route survives conditionally", "evidence": OUTPUTS["stress_tests"].name}),
    base({"validation_id": "VAL3051_04_current_claim_blocked", "passed": len(stress_current_failures) >= 1 and all(not boolish(row["stress_passes_for_current_MTS"]) for row in stress_rows), "requirement": "current MTS does not pass stress gates for claim", "evidence": OUTPUTS["stress_tests"].name}),
    base({"validation_id": "VAL3051_05_dotG_fallback_present", "passed": any(row.get("row_id") == dotg_fill_row["row_id"] for row in dotg_target_rows), "requirement": "first dotG coefficient fill row is present", "evidence": str(DOTG_TARGET)}),
    base({"validation_id": "VAL3051_06_dotG_nonclaim", "passed": all(not has_claim_true([row]) for row in dotg_target_rows), "requirement": "dotG target rows remain nonclaim", "evidence": str(DOTG_TARGET)}),
    base({"validation_id": "VAL3051_07_no_claim_rows", "passed": not has_claim_true(all_output_rows), "requirement": "no generated row is valid for claim", "evidence": "valid_for_claim/claim_allowed/score_ready/claim_active flags"}),
    base({"validation_id": "VAL3051_08_claim_status_nonactive", "passed": all(str(row["claim_active"]).lower() == "false" for row in claim_rows), "requirement": "conditional stress result is not promoted as active local-GR claim", "evidence": OUTPUTS["claim_status"].name}),
    base({"validation_id": "VAL3051_09_branch_copies", "passed": all(path.exists() and csv_ok(path) for path in BRANCH_OUTPUTS.values()), "requirement": "branch copies exist and parse", "evidence": OUTPUTS["branches"].name}),
    base({"validation_id": "VAL3051_10_output_scope", "passed": all(under(path, ROOT) for path in generated_paths), "requirement": "all generated outputs are inside post-checkpoint-work", "evidence": str(ROOT)}),
    base({"validation_id": "VAL3051_11_formalization_untouched", "passed": len(formalization_generated_hits) == 0, "requirement": "formalization-workbench modified-file target count remains 0", "evidence": f"generated outputs under formalization={len(formalization_generated_hits)}"}),
    base({"validation_id": "VAL3051_12_next_target", "passed": next_rows[0]["next_checkpoint"].startswith("3052-"), "requirement": "next target selects source-frame readout lock or dotG numeric runner", "evidence": OUTPUTS["next"].name}),
    base({"validation_id": "VAL3051_13_pycache_removed", "passed": not PYCACHE.exists(), "requirement": "scripts __pycache__ removed", "evidence": str(PYCACHE)}),
]
write_csv(OUTPUTS["validation"], validation_rows)

doc_text = f"""# 3051 - Source-Frame Stress Test of Topological Kappa Spine or First dotG Coefficient Fill

Status: `Y5_R2FR_3051_topological_spine_partially_survives_conditionally_dotG_fallback_filled_nonclaim`

Generated: `{RUN_UTC}`

## Verdict

3051 stress-tests the 3050 parent-action candidate instead of just circling it.

Important result: the candidate is **not dead**. If `integral_M kappa_eff dA_3` is a true metric-independent top-form term, then its metric stress is zero:

`delta_g integral_M kappa_eff dA_3 = 0`

and the `A_3` variation still gives:

`delta_A3 S -> d kappa_eff = 0`

But current MTS still cannot claim local GR/Newton, because the route is conditional rather than active. The remaining live blockers are source/readout adoption, same-frame `G_ref/W/Phi/T_obs`, the `kappa_eff` companion equation no-readout condition, and second-order PPN.

Because at least one stress gate fails for current MTS, 3051 also fills the first nonclaim `dln_Geff_dt` row in `P8_time_drift_residual_or_zero.csv`.

## Stress Test Matrix

{md_table(stress_rows, ["test_id", "gate", "candidate_internal_result", "current_MTS_result", "reason", "stress_passes_for_current_MTS", "unlocks_if_signed"])}

## Source-Frame Readout Stress

{md_table(source_frame_rows, ["frame_test_id", "object", "conditional_result", "current_status", "blocking_source", "residual_if_failed"])}

## Topological Stress and Companion Audit

{md_table(topological_rows, ["topo_test_id", "object", "calculation", "candidate_result", "current_status", "remaining_risk"])}

## dotG Fallback Fill

{md_table(dotg_fill_rows, ["fill_id", "target_file", "row_id", "appended_now", "target_row_count", "candidate_value", "bound_or_target", "status"])}

## dotG Target Audit

{md_table(dotg_target_audit_rows, ["audit_id", "target_file", "exists", "parse_ok", "row_count", "contains_3051_row", "claim_true_rows", "missing_marker_rows", "status"])}

## Claim Status

{md_table(claim_rows, ["claim_id", "claim", "status", "claim_active", "reason"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "question", "answer", "reason", "action"])}

## Next Target

{md_table(next_rows, ["next_id", "next_checkpoint", "mission", "starting_equation", "claim_policy"])}

## Source Register

{md_table(source_register, ["source_id", "exists", "parse_ok", "row_count", "role", "status"])}

## Branch Copies

{md_table(branch_rows, ["copy_id", "destination", "exists", "row_count", "description"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}
"""

DOC.write_text(doc_text, encoding="utf-8")

failures = [row for row in validation_rows if not boolish(row["passed"])]
if failures:
    raise SystemExit(f"3051 validation failed: {[row['validation_id'] for row in failures]}")

print(f"wrote {DOC}")
print(f"validation rows: {len(validation_rows)} passed")
print("claim status: topological spine conditionally survives stress; dotG fallback row filled nonclaim")

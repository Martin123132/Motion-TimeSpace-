from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1830"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
P4_RUN = ROOT / "runs" / "20260602-141500-metric-compatibility-Levi-Civita-or-R11-connection-row" / "results"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1830-Y5-R2FR-no-independent-connection-parent-grammar-or-P4-row-fill.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1830_0_1829_next",
        "source_key": "1829_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1829_NEXT_TARGET.csv",
        "needles": ["NEXT1829_0_primary", "selected"],
        "role": "1829 selects no-independent-connection grammar or P4 row fill.",
    },
    {
        "source_id": "SRC1830_1_1829_validation",
        "source_key": "1829_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1829_VALIDATION.csv",
        "needles": ["VAL1829_OVERALL", "PASS"],
        "role": "confirms 1829 passed as a nonclaim checkpoint.",
    },
    {
        "source_id": "SRC1830_2_1829_metric",
        "source_key": "1829_metric_only_attempt",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1829_METRIC_ONLY_CONNECTION_THEOREM_ATTEMPT.csv",
        "needles": ["MOC1829_6_verdict", "METRIC_ONLY_THEOREM_NOT_PARENT_SIGNED"],
        "role": "metric-only theorem is exact but not parent-signed.",
    },
    {
        "source_id": "SRC1830_3_1829_P4",
        "source_key": "1829_P4_pack",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1829_P4_CONNECTION_SOURCE_PACK.csv",
        "needles": ["P4SP1829_6_total", "P4_VECTOR_READY_SCHEMA_ONLY_NONCLAIM"],
        "role": "P4 source-pack rows are staged but nonclaim.",
    },
    {
        "source_id": "SRC1830_4_1829_hinge",
        "source_key": "1829_hinge_pack",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1829_HINGE_SOURCE_PACK.csv",
        "needles": ["HSP1829_4_total", "HINGE_SOURCE_PACK_READY_SCHEMA_ONLY_NONCLAIM"],
        "role": "hinge source-pack rows remain nonclaim.",
    },
    {
        "source_id": "SRC1830_5_P4_gate",
        "source_key": "P4_gate_tests",
        "source_path": P4_RUN / "P4_gate_tests.csv",
        "needles": ["independent_connection_absence_gate", "fail_open"],
        "role": "independent-connection absence gate remains open.",
    },
    {
        "source_id": "SRC1830_6_P4_demotions",
        "source_key": "P4_demotions",
        "source_path": P4_RUN / "connection_operator_demotions.csv",
        "needles": ["independent_connection_hypermomentum", "not_forbidden"],
        "role": "hypermomentum/source connection channel remains legal.",
    },
    {
        "source_id": "SRC1830_7_1542_qdef",
        "source_key": "1542_q_definition",
        "source_path": ROOT / "1542-Y5-q-definition-or-Dqvm-coupling-coefficient-source-pack.md",
        "needles": ["QDEF1542_1_minimal_visible_candidate", "CANDIDATE_ONLY"],
        "role": "visible quotient candidate includes omega_obs but remains candidate-only.",
    },
    {
        "source_id": "SRC1830_8_1045_matter",
        "source_key": "1045_matter_functor",
        "source_path": ROOT / "1045-Y5-R10-parent-matter-functor-descent-signature-or-qbar-component-fill.md",
        "needles": ["MFS1045_2_matter_bundle_functor", "QG1045_2_connection_stack"],
        "role": "matter functor shape uses omega[e_obs] conditionally.",
    },
    {
        "source_id": "SRC1830_9_1155_coframe",
        "source_key": "1155_geometry_stack",
        "source_path": ROOT / "1155-Y5-R10-single-observed-coframe-source-frame-owner-or-frame-residual-row.md",
        "needles": ["COF1155_3_geometry_stack", "NOT_PARENT_SIGNED"],
        "role": "geometry stack descent is not parent-signed.",
    },
    {
        "source_id": "SRC1830_10_1561_adoption",
        "source_key": "1561_adoption",
        "source_path": ROOT / "1561-Y5-minimal-parent-weak-field-action-ansatz-and-Euler-Ward-PPN-gate.md",
        "needles": ["ADOPT1561_2_MTS_matching", "MISSING_SYMBOL_MATCH"],
        "role": "minimal EH ansatz still lacks MTS symbol matching.",
    },
    {
        "source_id": "SRC1830_11_512_symbols",
        "source_key": "512_symbols",
        "source_path": ROOT / "512-match-MTS-symbols-to-local-GR-action-blocks.md",
        "needles": ["Gamma_eff", "no_symbol_fully_promotes_local_GR"],
        "role": "symbol map preserves Gamma/Khat/q_loc as hard obstruction.",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1830_SOURCE_REGISTER.csv",
    "grammar_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1830_NO_INDEPENDENT_CONNECTION_GRAMMAR_ATTEMPT.csv",
    "P4_row_fill_contract": RESIDUALS / "P8_Y5_PARENT_QLOC_1830_P4_ROW_FILL_CONTRACT.csv",
    "anti_smuggling_guard": RESIDUALS / "P8_Y5_PARENT_QLOC_1830_ANTI_SMUGGLING_GUARD.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1830_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1830_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1830_VALIDATION.csv",
}


def ensure_dirs() -> None:
    for directory in [RESIDUALS, MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
        directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        exists = path.exists()
        text = read_text(path) if exists else ""
        missing_needles = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": exists,
                "needles": ";".join(source["needles"]),
                "needles_present": exists and not missing_needles,
                "missing_needles": ";".join(missing_needles),
                "role": source["role"],
            }
        )
    return rows


def grammar_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "grammar_id": "NIC1830_0_target",
            "required_clause": "no independent connection slot",
            "test": "the parent field grammar lists only observed metric/coframe geometry, with omega/Gamma defined as omega[e_obs]",
            "current_status": "TARGET_ATTEMPTED",
            "failure_mode": "field inventory is not yet parent-signed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "grammar_id": "NIC1830_1_q_visible",
            "required_clause": "q_loc owns visible geometry before local tests",
            "test": "q_loc(Phi) includes e_obs, g_obs, omega_obs and forbids post-hoc deletion of failed couplings",
            "current_status": "CANDIDATE_ONLY",
            "failure_mode": "q definition remains a candidate and exact kernel route is not closed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "grammar_id": "NIC1830_2_omega_definition",
            "required_clause": "omega_obs is derivative-only",
            "test": "omega_obs := omega[e_obs] by parent grammar, not an independent field with its own Euler equation",
            "current_status": "NOT_PARENT_SIGNED",
            "failure_mode": "connection stack descent is conditional; independent Gamma is not excluded",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "grammar_id": "NIC1830_3_no_hypermomentum",
            "required_clause": "matter carries no independent connection charge",
            "test": "S_matter[Psi,e_obs,omega[e_obs],theta] and source/readout sectors have no delta-Gamma hypermomentum term",
            "current_status": "NOT_PARENT_SIGNED",
            "failure_mode": "spin, projective, source and non-Hilbert currents remain legal",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "grammar_id": "NIC1830_4_no_shadow_geometry",
            "required_clause": "no hidden connection/frame slot",
            "test": "measure, coframe, connection, derivative and readout all descend through the same observed q/e functor",
            "current_status": "NOT_PARENT_SIGNED",
            "failure_mode": "single geometry stack remains unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "grammar_id": "NIC1830_5_Gamma_eff_status",
            "required_clause": "Gamma_eff is reconciled",
            "test": "Gamma_eff is either omega[e_obs]/derived curvature data or a separate residual sector with P4/q_loc rows",
            "current_status": "RETAINED_RESIDUAL_IF_NOT_REDUCED",
            "failure_mode": "Gamma/Khat/q_loc symbol matching remains a hard obstruction",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "grammar_id": "NIC1830_6_verdict",
            "required_clause": "no-independent-connection theorem",
            "test": "NIC1830_0 through NIC1830_5 close in one parent field grammar",
            "current_status": "NO_INDEPENDENT_CONNECTION_GRAMMAR_NOT_PROVEN",
            "failure_mode": "must move to P4 row fill or deeper parent grammar construction",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def P4_row_fill_contract_rows() -> list[dict[str, Any]]:
    required_fields = "coefficient;units;operator_normalization;weak_field_map;observable_links;source_path;derivation_status;assumptions;valid_for_claim=false"
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4F1830_0_combined_TQ",
            "operator_family": "torsion_nonmetricity_combined",
            "required_fields": required_fields,
            "current_status": "MISSING_COEFFICIENTS_AND_MAPS",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4F1830_1_axial_spin",
            "operator_family": "axial_torsion_spin_coupling",
            "required_fields": required_fields,
            "current_status": "MISSING_SPIN_TORSION_SOURCE",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4F1830_2_projective",
            "operator_family": "torsion_trace_projective_mode",
            "required_fields": required_fields,
            "current_status": "MISSING_PROJECTIVE_INVARIANCE_OR_BOUND",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4F1830_3_weyl_Q",
            "operator_family": "nonmetricity_weyl_trace",
            "required_fields": required_fields,
            "current_status": "MISSING_CLOCK_ROD_MAP",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4F1830_4_shear_Q",
            "operator_family": "nonmetricity_shear_lightcone",
            "required_fields": required_fields,
            "current_status": "MISSING_LIGHTCONE_MAP",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4F1830_5_hypermomentum",
            "operator_family": "independent_connection_hypermomentum",
            "required_fields": required_fields,
            "current_status": "MISSING_HYPERMOMENTUM_ZERO_OR_BOUND",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "P4F1830_6_total",
            "operator_family": "P4_executable_connection_vector",
            "required_fields": "P4F1830_0 through P4F1830_5 all source-backed or theorem-zero",
            "current_status": "P4_ROW_FILL_CONTRACT_READY_NONCLAIM",
            "valid_for_claim": False,
        },
    ]


def anti_smuggling_guard_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "guard_id": "ASG1830_0_no_EH_import",
            "guard": "do not import EH/Levi-Civita as the proof",
            "reason": "that assumes the GR reduction rather than deriving it from MTS",
            "status": "ACTIVE",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "guard_id": "ASG1830_1_no_posthoc_q",
            "guard": "do not define q_loc by deleting connection couplings that fail",
            "reason": "q must be parent-owned before local tests",
            "status": "ACTIVE",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "guard_id": "ASG1830_2_no_spin_silence_by_word",
            "guard": "do not set spin/hypermomentum/projective residues to zero by wording",
            "reason": "these are known P4 escape routes unless parent-signed or bounded",
            "status": "ACTIVE",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "guard_id": "ASG1830_3_no_local_GR_promotion",
            "guard": "do not promote local GR from this checkpoint",
            "reason": "source, q_loc, PPN, matter descent and operator gates remain open",
            "status": "ACTIVE",
            "valid_for_claim": False,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1830_0_grammar_result",
            "decision": "NO_INDEPENDENT_CONNECTION_GRAMMAR_NOT_PROVEN",
            "reason": "current files have a visible-geometry candidate and conditional omega[e] use, but no parent field-inventory theorem excluding independent connection/hypermomentum",
            "next_action": "do not claim Levi-Civita compatibility",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1830_1_fallback",
            "decision": "P4_EXECUTABLE_ROW_FILL_REQUIRED_IF_GRAMMAR_FAILS",
            "reason": "torsion, nonmetricity, projective residue and hypermomentum remain legal modified-gravity channels",
            "next_action": "fill or theorem-zero P4 rows before any local-GR claim",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1830_2_best_next",
            "decision": "PARENT_FIELD_INVENTORY_CERTIFICATE_OR_FIRST_P4_NUMERIC_ROW_NEXT",
            "reason": "one more derivation-first attempt should certify the parent field inventory; if that fails, start numeric/source-backed P4 acquisition",
            "next_action": "1831-Y5-R2FR-parent-field-inventory-certificate-or-first-P4-numeric-row.md",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1830_0_primary",
            "next_target": "1831-Y5-R2FR-parent-field-inventory-certificate-or-first-P4-numeric-row.md",
            "script": "scripts/Y5_R2FR_parent_field_inventory_certificate_or_first_P4_numeric_row.py",
            "objective": "try to certify the parent field inventory excludes independent connection/hypermomentum; if not, fill the first executable P4 row with numeric/source-backed coefficient, units and weak-field map",
            "selection_status": "selected",
            "success_condition": "field inventory certificate parent-signed, or first P4 numeric/source row remains valid_for_claim=false with provenance",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1830_1_parallel",
            "next_target": "1831b-Y5-R2FR-hinge-cell-scale-source-pack-fill.md",
            "script": "scripts/Y5_R2FR_hinge_cell_scale_source_pack_fill.py",
            "objective": "parallel fill for cell complex, B_h/A_h, orientation, ell_cell and shape_factor",
            "selection_status": "held_parallel",
            "success_condition": "hinge source-pack rows become source-backed nonclaim inputs",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "grammar_attempt": grammar_attempt_rows(),
        "P4_row_fill_contract": P4_row_fill_contract_rows(),
        "anti_smuggling_guard": anti_smuggling_guard_rows(),
        "decision_ledger": decision_ledger_rows(),
        "next_target": next_target_rows(),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def copy_csvs(paths: list[Path]) -> None:
    for path in paths:
        for directory in [MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
            directory.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, directory / path.name)


def csv_parse_ok(paths: list[Path]) -> bool:
    try:
        for path in paths:
            with path.open("r", encoding="utf-8", newline="") as handle:
                list(csv.DictReader(handle))
    except Exception:
        return False
    return True


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    guarded_keys = {"valid_for_claim", "claim_allowed"}
    for rows in rows_map.values():
        for row in rows:
            for guarded_key in guarded_keys.intersection(row):
                if str(row[guarded_key]).lower() == "true":
                    return False
    return True


def no_formalization_outputs() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        name = path.name
        if "1830-Y5-R2FR" in name or name.startswith("P8_Y5_PARENT_QLOC_1830") or name.startswith("P8_Y5_BRR545_1830"):
            return False
    return True


def branch_copies_exist(paths: list[Path]) -> bool:
    for path in paths:
        for directory in [MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
            if not (directory / path.name).exists():
                return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]], copied_paths: list[Path]) -> list[dict[str, Any]]:
    source_rows = rows_map["source_register"]
    output_paths = [OUTPUTS[key] for key in rows_map.keys()]
    checks: list[tuple[str, bool, str]] = [
        ("VAL1830_0_sources_exist", all(str(row["exists"]).lower() == "true" for row in source_rows), "all cited source paths exist"),
        ("VAL1830_1_needles_present", all(str(row["needles_present"]).lower() == "true" for row in source_rows), "all cited source needles are present"),
        ("VAL1830_2_grammar_attempt_written", any(row["grammar_id"] == "NIC1830_0_target" for row in rows_map["grammar_attempt"]), "no-independent-connection grammar attempt is written"),
        (
            "VAL1830_3_grammar_not_promoted",
            any(row["grammar_id"] == "NIC1830_6_verdict" and row["current_status"] == "NO_INDEPENDENT_CONNECTION_GRAMMAR_NOT_PROVEN" for row in rows_map["grammar_attempt"]),
            "no-independent-connection grammar is not promoted",
        ),
        (
            "VAL1830_4_P4_contract_nonclaim",
            any(row["row_id"] == "P4F1830_6_total" and row["current_status"] == "P4_ROW_FILL_CONTRACT_READY_NONCLAIM" and row["valid_for_claim"] is False for row in rows_map["P4_row_fill_contract"]),
            "P4 row fill contract remains nonclaim",
        ),
        (
            "VAL1830_5_guards_active",
            all(row["status"] == "ACTIVE" and row["valid_for_claim"] is False for row in rows_map["anti_smuggling_guard"]),
            "anti-smuggling guards are active",
        ),
        (
            "VAL1830_6_decision_next",
            any(row["decision_id"] == "DEC1830_2_best_next" and row["decision"] == "PARENT_FIELD_INVENTORY_CERTIFICATE_OR_FIRST_P4_NUMERIC_ROW_NEXT" for row in rows_map["decision_ledger"]),
            "decision selects parent field inventory certificate or first P4 numeric row next",
        ),
        (
            "VAL1830_7_next_selected",
            any(row["route_id"] == "NEXT1830_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1830_8_no_claim_flags", no_claim_flags(rows_map), "no generated claim flags are true"),
        ("VAL1830_9_csv_parse", csv_parse_ok(output_paths), "all generated 1830 CSVs parse"),
        ("VAL1830_10_branch_copies", branch_copies_exist(copied_paths), "branch/quarantine/queue copies exist"),
        ("VAL1830_11_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1830_12_formalization_untouched", no_formalization_outputs(), "no 1830 outputs found under formalization-workbench"),
    ]
    rows = [{"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail} for check_id, passed, detail in checks]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1830_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1830 no-independent-connection parent grammar or P4 row fill checkpoint",
        }
    )
    return rows


def markdown_cell(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(markdown_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    return "\n".join(
        [
            "# 1830 Y5 R2FR no independent connection parent grammar or P4 row fill",
            "",
            "**Progress:** 1830 tests the cleanest Levi-Civita route at the grammar level. If the parent field inventory has no independent connection or hypermomentum slot, P4 closes kinematically. Current MTS does not yet prove that inventory; it has candidate `omega[e_obs]` language, but not the parent exclusion theorem.",
            "",
            "**Current verdict:** no connection theorem yet. The next target is a parent field-inventory certificate. If that certificate fails, the project should stop trying to win P4 by prose and fill the first executable torsion/nonmetricity/hypermomentum row with coefficient, units, weak-field map and source path.",
            "",
            "**Claim ceiling:** no Levi-Civita compatibility claim, no P4 pass, no `c2` score, no local GR/Newton promotion, no GitHub action, and no `formalization-workbench` edit is allowed from 1830.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "missing_needles", "role"]),
            "",
            "## No Independent Connection Grammar Attempt",
            markdown_table(rows_map["grammar_attempt"], ["grammar_id", "required_clause", "test", "current_status", "failure_mode", "claim_allowed", "valid_for_claim"]),
            "",
            "## P4 Row Fill Contract",
            markdown_table(rows_map["P4_row_fill_contract"], ["row_id", "operator_family", "required_fields", "current_status", "valid_for_claim"]),
            "",
            "## Anti-Smuggling Guard",
            markdown_table(rows_map["anti_smuggling_guard"], ["guard_id", "guard", "reason", "status", "valid_for_claim"]),
            "",
            "## Decision Ledger",
            markdown_table(rows_map["decision_ledger"], ["decision_id", "decision", "reason", "next_action"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This is a proper GR-reduction move. The project does not need to separately tune torsion and nonmetricity away if MTS can prove the parent never contains those independent degrees of freedom. But that proof has to be a real field-inventory theorem. If it is not available, P4 becomes an empirical residual-vector problem rather than a theorem-zero branch.",
            "",
        ]
    )


def main() -> None:
    ensure_dirs()
    rows_map = rows_by_key()
    nonvalidation_paths: list[Path] = []
    for key, rows in rows_map.items():
        path = OUTPUTS[key]
        write_csv(path, rows)
        nonvalidation_paths.append(path)
    copy_csvs(nonvalidation_paths)
    validation_rows = build_validation(rows_map, nonvalidation_paths)
    write_csv(OUTPUTS["validation"], validation_rows)
    copy_csvs([OUTPUTS["validation"]])
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1830 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()

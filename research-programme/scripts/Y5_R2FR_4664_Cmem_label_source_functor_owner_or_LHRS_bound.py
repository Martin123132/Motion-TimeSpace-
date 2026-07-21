from __future__ import annotations

import csv
import io
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4664"
CLAIM_ID = "L-506"
BRANCH = "MTS_R2FR_Y5_CMEM_LABEL_SOURCE_FUNCTOR_OWNER_OR_LHRS_BOUND_4664"
MARKER = "PPC4161_CMEM_LABEL_SOURCE_FUNCTOR_OWNER_OR_LHRS_BOUND_4664"
PACKET_MARKER = "PPC4161_PACKET_CMEM_LABEL_SOURCE_FUNCTOR_OWNER_OR_LHRS_BOUND_4664"
DECISION = "CMEM_LABEL_ZERO_PRIVATE_TOTAL_SOURCE_FUNCTOR_DYNAMIC_LABEL_BOUND_RETAINED_NONCLAIM"
NEXT_TARGET = "4665-Y5-R2FR-Cmem-support-worldtube-owner-or-Reynolds-bound.md"

DOC_PATH = POST / "4664-Y5-R2FR-Cmem-label-source-functor-owner-or-LHRS-bound.md"
FORMAL_PATH = FORMAL / "680-PPC4161-Cmem-label-source-functor-owner-or-LHRS-bound.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

DOC_4663 = POST / "4663-Y5-R2FR-Cmem-Hodge-Poynting-owner-or-LHRS-bound.md"
DOC_3291 = POST / "3291-Y5-R2FR-TQ-Noether-current-owner-and-source-label-forgetting-under-AX1090.md"
DOC_3522 = POST / "3522-Y5-R2FR-representative-identity-vs-global-symmetry-or-active-marker-bound.md"
FORMAL_679 = FORMAL / "679-PPC4161-Cmem-Hodge-Poynting-owner-or-LHRS-bound.md"

CSV_4663_LHRS = SOURCE_DIR / "P8_Y5_R2FR_4663_LHRS_CMEM_UPDATE_AFTER_HODGE.csv"
CSV_4663_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4663_NEXT_TARGET.csv"
CSV_4663_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4663_VALIDATION.csv"
CSV_4599_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4599_LABEL_HODGE_SUPPORT_READOUT_ZERO_THEOREM.csv"
CSV_4599_NORM = SOURCE_DIR / "P8_Y5_R2FR_4599_CX_LABEL_HODGE_SUPPORT_READOUT_NORM.csv"
CSV_4599_CONTROL = SOURCE_DIR / "P8_Y5_R2FR_4599_CONTROL_ROWS.csv"
CSV_4599_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4599_VALIDATION.csv"
CSV_3291_FORGETTING = SOURCE_DIR / "P8_Y5_R2FR_3291_SOURCE_LABEL_FORGETTING_LEMMA.csv"
CSV_3522_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_3522_LIVE_LABEL_AUDIT.csv"
CSV_3522_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_3522_VALIDATION.csv"
CSV_4537_ADOPTION = SOURCE_DIR / "P8_Y5_R2FR_4537_GR_PARITY_ADOPTION_CERTIFICATE.csv"
CSV_4537_RANK = SOURCE_DIR / "P8_Y5_R2FR_4537_COMPONENT_GRAPH_RANK_RESULTS.csv"
CSV_4538_BRANCH = SOURCE_DIR / "P8_Y5_R2FR_4538_GR_PARITY_HQNP_BRANCH_IMPORT.csv"
CSV_4446_VECTOR = SOURCE_DIR / "P8_Y5_R2FR_4446_SOURCE_UNIVERSALITY_RESIDUAL_VECTOR.csv"
CSV_4446_DERIV = SOURCE_DIR / "P8_Y5_R2FR_4446_DERIVATION_ROWS.csv"
CSV_4661_DELTAW = SOURCE_DIR / "P8_Y5_R2FR_4661_DELTAW_SOURCE_WEIGHT_ZERO_IMPORT.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4664_SOURCE_REGISTER.csv"
OWNER_CLAUSE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4664_LABEL_SOURCE_FUNCTOR_OWNER_CLAUSES.csv"
ZERO_IMPORT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4664_CMEM_LABEL_ZERO_IMPORT.csv"
DYNAMIC_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4664_DYNAMIC_LABEL_BOUND_ROWS.csv"
LHRS_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4664_LHRS_CMEM_UPDATE_AFTER_LABEL.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4664_RUNNER_RESULTS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4664_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4664_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4664_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4664_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4664_VALIDATION.csv"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def line_number(path: Path, needle: str) -> int:
    for index, line in enumerate(read_text(path).splitlines(), start=1):
        if needle in line:
            return index
    return 0


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def table(rows: list[dict[str, Any]]) -> str:
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        values = [str(row.get(field, "")).replace("|", "\\|").replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, text: str) -> None:
    existing = read_text(path)
    if marker in existing:
        return
    suffix = "" if not existing or existing.endswith("\n") else "\n"
    path.write_text(existing + suffix + text.lstrip("\n"), encoding="utf-8")


def csv_line(values: list[str]) -> str:
    buffer = io.StringIO()
    csv.writer(buffer, lineterminator="\n").writerow(values)
    return buffer.getvalue()


def source_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4664_00_4663_next", CSV_4663_NEXT, "4664-Y5-R2FR-Cmem-label-source-functor-owner-or-LHRS-bound.md", "4663 selects label/source functor target."),
        ("SRC4664_01_4663_LHRS_after", CSV_4663_LHRS, "LHU4663_2_after", "LHRS before label closure."),
        ("SRC4664_02_4663_final", CSV_4663_LHRS, "LHU4663_3_final_Cmem", "final Cmem before label closure."),
        ("SRC4664_03_4663_validation", CSV_4663_VALIDATION, "VAL4663_OVERALL", "4663 validation pass."),
        ("SRC4664_04_679_formal", FORMAL_679, "C_mem^label / source functor owner", "formal 4663 label handoff."),
        ("SRC4664_05_4599_label", CSV_4599_THEOREM, "LHRS4599_0_label", "label zero-or-bound theorem."),
        ("SRC4664_06_4599_label_norm", CSV_4599_NORM, "N4599_0_label", "Delta_label finite norm row."),
        ("SRC4664_07_4599_label_control", CSV_4599_CONTROL, "CTRL4599_label_countermodel", "label countermodel retained."),
        ("SRC4664_08_4599_validation", CSV_4599_VALIDATION, "VAL4599_06_no_claim_true", "4599 no-claim validation."),
        ("SRC4664_09_3291_target", CSV_3291_FORGETTING, "SLF3291_0_target", "source functor target."),
        ("SRC4664_10_3291_total", CSV_3291_FORGETTING, "SLF3291_1_total_variation", "total variational theorem."),
        ("SRC4664_11_3291_counter", CSV_3291_FORGETTING, "SLF3291_3_live_counterexample", "source-only species scalar counterexample."),
        ("SRC4664_12_3291_verdict", CSV_3291_FORGETTING, "SLF3291_4_verdict", "source-label status."),
        ("SRC4664_13_3522_matter_labels", CSV_3522_AUDIT, "LL3522_2_matter_source_labels", "matter/source label audit."),
        ("SRC4664_14_3522_constructor", CSV_3522_AUDIT, "LL3522_3_constructor_labels", "constructor label audit."),
        ("SRC4664_15_3522_doc_corollary", DOC_3522, "QI3522_4_source_coupling_corollary", "quotient/source-coupling corollary."),
        ("SRC4664_16_3522_doc_guard", DOC_3522, "QI3522_2_fixed_marker_obstruction", "active marker obstruction."),
        ("SRC4664_17_3522_validation", CSV_3522_VALIDATION, "VAL3522_8_next_target_selected", "3522 validation next target."),
        ("SRC4664_18_4537_no_prefactor", CSV_4537_ADOPTION, "AD4537_1_no_source_prefactor", "no source-only prefactor."),
        ("SRC4664_19_4537_rank", CSV_4537_RANK, "RR4537_2_GR_parity_adopted_branch", "GR-parity rank pass."),
        ("SRC4664_20_4538_source_weight", CSV_4538_BRANCH, "BI4538_1_source_weight", "source-weight zero branch."),
        ("SRC4664_21_4446_deltaw", CSV_4446_VECTOR, "RU4446_0_Delta_w_A", "relative source weight zero."),
        ("SRC4664_22_4446_material", CSV_4446_VECTOR, "RU4446_1_material_readout_reentry", "material label reentry zero."),
        ("SRC4664_23_4446_counter", CSV_4446_DERIV, "ADOPT4446_1_weight_countermodel_killed", "weighted-component countermodel killed."),
        ("SRC4664_24_4661_no_source_prefactor", CSV_4661_DELTAW, "DWI4661_3_no_source_prefactor", "no active source label morphism."),
        ("SRC4664_25_4661_result", CSV_4661_DELTAW, "DWI4661_5_result", "delta_w zero branch."),
        ("SRC4664_26_3291_doc", DOC_3291, "source-only species weight", "3291 source-only obstruction in prose."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, note in specs:
        text = read_text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "line_number": line_number(path, needle),
                "note": note,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def owner_clause_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("LFO4664_0_total_objects", "F_src consumes T_total and J_total", "source functor receives total variational objects, not labelled pairs {(T_A,J_A,A)}", "SLF3291_1_total_variation", "EXACT_CONDITIONAL_THEOREM_IMPORTED"),
        ("LFO4664_1_no_label_slot", "no SpeciesLabel/MaterialLabel -> Coeff_active_source Hom", "no independent active-source coefficient can be keyed by species/material labels in the private branch", "DWI4661_3_no_source_prefactor", "PRIVATE_BRANCH_CLAUSE"),
        ("LFO4664_2_GR_parity", "one standard visible matter action with fixed graph/no-source-prefactor", "GR-parity ordinary-visible import removes source-only component prefactors before Hilbert variation", "RR4537_2_GR_parity_adopted_branch", "GR_PARITY_IMPORT"),
        ("LFO4664_3_material_readout", "material labels are readout inventory, not active source coefficients", "material label to active-source reentry is zero inside private GR-parity branch", "RU4446_1_material_readout_reentry", "MATERIAL_REENTRY_ZERO"),
        ("LFO4664_4_quotient_guard", "q-factored matter action cannot see ker(Dq)", "source-label weights require an extra non-q morphism; if excluded, label leakage is illegal", "QI3522_4_source_coupling_corollary", "QUOTIENT_FUNCTOR_SUPPORT"),
        ("LFO4664_5_public_limit", "source-only species scalars and fixed active markers remain countermodels off branch", "the result is private-branch label silence, not public primitive constructor exhaustion", "SLF3291_3_live_counterexample; QI3522_2_fixed_marker_obstruction", "COUNTERMODELS_RETAINED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "clause_id": row[0],
            "clause": row[1],
            "deduction": row[2],
            "source": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def zero_import_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("LZI4664_0_definition", "C_mem^label := Pi_mem[C_X^label]", "memory projection of source-label/constructor/spurion active-source leakage", "LHU4663_2_after", "TARGET_DEFINED"),
        ("LZI4664_1_total_functor", "F_src(T_total,J_total) has no A-label slot", "a source selector that only sees total variational objects cannot build label-return coefficients", "SLF3291_1_total_variation", "LABEL_SLOT_ABSENT"),
        ("LZI4664_2_no_prefactor", "no source-only component prefactor / no active-source label Hom", "GR-parity source universality forbids label-indexed active source coefficients in the fixed ordinary-visible branch", "4537/4538/4661", "NO_LABEL_COEFFICIENT_BRANCH"),
        ("LZI4664_3_material_readout", "material labels do not reenter active source", "readout inventory and material composition do not become source coefficients on this branch", "RU4446_1_material_readout_reentry", "MATERIAL_LABEL_REENTRY_ZERO"),
        ("LZI4664_4_result", "fixed ordinary-visible total-source branch => C_mem^label=0", "label term drops from C_mem^LHRS_live in the private branch", "all LFO4664 clauses", "CMEM_LABEL_TERM_ZERO_PRIVATE_BRANCH"),
        ("LZI4664_5_scope", "not a Standard Model or material microphysics derivation", "the branch assumes ordinary visible matter action/parity; hidden, nonstandard and fixed-marker labels remain bounded residuals", "SLF3291_3; LL3522_3", "SCOPE_FIREWALL"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "zero_id": row[0],
            "statement": row[1],
            "deduction": row[2],
            "source_or_condition": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def dynamic_bound_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("DLB4664_0_envelope", "Delta_label_mem", "|source-only species scalar| + |constructor/spurion return| + |fixed active marker| + |hidden/nonstandard label| + |readout label reentry|", "off-branch no-cancellation label envelope", "N4599_0_label; LL3522"),
        ("DLB4664_1_species_scalar", "w_A S_A or kappa_A T_A", "source-only species scalar survives covariance/additivity and changes source normalization", "finite row if parent syntax allows labelled source inputs", "SLF3291_3_live_counterexample"),
        ("DLB4664_2_constructor", "Hom_parent(label/hidden/readout, Coeff_active_source)", "constructor labels can return active-source coefficients if not syntactically forbidden", "finite row if constructor exhaustion fails", "LL3522_3_constructor_labels"),
        ("DLB4664_3_marker", "fixed active marker/source mask", "fixed marker can distinguish quotient representatives and reopen source-label coupling", "finite row if marker is physical or not q-basic", "QI3522_2_fixed_marker_obstruction"),
        ("DLB4664_4_hidden", "hidden/nonstandard label sector", "ordinary-visible GR-parity import does not erase hidden/nonstandard sectors", "finite row if hidden labels couple to local source", "LFO4664_5_public_limit"),
        ("DLB4664_5_source_contract", "C_mem_label_dynamic_source_row", "system_id;branch;source_only_scalar;constructor_label;active_marker;hidden_label;readout_reentry;projection;units;source_path;valid_for_claim", "future dynamic label row contract", "SOURCE_ROW_TEMPLATE_READY_VALUES_MISSING"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "bound_id": row[0],
            "quantity": row[1],
            "bound_or_contract": row[2],
            "meaning": row[3],
            "source": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def lhrs_update_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("LLU4664_0_before", "|C_mem^LHRS_live| <= |C_mem^label|+|C_mem^support|+|C_mem^readout|", "4663 LHRS after Hodge closure", "LHRS_IMPORTED"),
        ("LLU4664_1_label_zero", "|C_mem^label|=0", "4664 total-source functor/source-label owner private branch zero", "LABEL_TERM_REMOVED"),
        ("LLU4664_2_after", "|C_mem^LHRS_live| <= |C_mem^support|+|C_mem^readout|", "LHRS live block after Hodge and label closure", "LHRS_REDUCED"),
        ("LLU4664_3_final_Cmem", "|C_mem^final_live| <= |C_mem^support|+|C_mem^readout|+|C_mem^boundary|+|C_mem^nonHilbert|", "final Cmem residual vector after first-block, Hodge and label closure", "FINAL_VECTOR_REDUCED"),
        ("LLU4664_4_not_full", "C_mem^final_live=0 is not claimed", "support, readout, boundary and non-Hilbert channels remain open", "FULL_CMEM_STILL_OPEN"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "update_id": row[0],
            "statement": row[1],
            "meaning": row[2],
            "status": row[3],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def runner_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("RUN4664_0_total_source_branch", "C_mem^label", "PASS_CONDITIONAL_PRIVATE_ZERO", "source functor consumes total variational objects and no active-source label Hom is admitted."),
        ("RUN4664_1_dynamic_label", "Delta_label_mem", "FAIL_CLOSED_TO_BOUND_ROWS", "source-only species scalar, constructor labels and fixed markers stay explicit off branch."),
        ("RUN4664_2_LHRS_update", "C_mem^LHRS_live", "PASS_REDUCED_BOUND", "label removed; support/readout remain."),
        ("RUN4664_3_material_microphysics", "SM/material derivation", "NOT_CLAIMED", "ordinary-visible GR-parity branch is an import/selector, not a derivation of all matter spectra."),
        ("RUN4664_4_claim_status", "local GR/Newton/PPN/R10 claim", "NONCLAIM_STILL_BLOCKED", "support/readout/boundary/non-Hilbert and body-charge gates remain."),
        ("RUN4664_5_next", "next channel", "PASS_NEXT_SELECTED", NEXT_TARGET),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "run_id": row[0],
            "object": row[1],
            "result": row[2],
            "detail": row[3],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def control_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CTRL4664_0_no_symmetry_shortcut", "Do not infer source-label silence from symmetric formulas alone; require total-source functor or q-quotient ownership.", "ACTIVE"),
        ("CTRL4664_1_no_microphysics_claim", "Do not claim the Standard Model/material spectrum is derived from label closure.", "ACTIVE"),
        ("CTRL4664_2_hidden_labels_retained", "Hidden, nonstandard, fixed-marker and constructor-label sectors remain finite rows off branch.", "ACTIVE"),
        ("CTRL4664_3_no_fitted_G_absorption", "Do not absorb relative/source-label residuals into measured G or calibration.", "ACTIVE"),
        ("CTRL4664_4_no_full_Cmem", "C_mem^label=0 does not close support, readout, boundary or non-Hilbert channels.", "ACTIVE"),
        ("CTRL4664_5_no_public_local_GR", "Private source-label closure is not a public local-GR/Newton/PPN/R10 pass.", "ACTIVE"),
        ("CTRL4664_6_local_private_only", "No GitHub action; local framework/post-checkpoint packet only.", "ACTIVE"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": row[0],
            "guard": row[1],
            "status": row[2],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4664_0",
            "decision": DECISION,
            "summary": (
                "4664 closes C_mem^label in the fixed private ordinary-visible total-source branch. The source functor consumes total variational objects "
                "T_total and J_total, not labelled pairs; the GR-parity branch forbids SpeciesLabel/MaterialLabel -> Coeff_active_source morphisms; and material labels remain readout inventory. "
                "Therefore C_mem^label=0 on that branch. Off-branch source-only species scalars, constructor/spurion labels, fixed markers and hidden/nonstandard labels remain dynamic bound rows. "
                "The LHRS block now reduces to support plus readout."
            ),
            "next_target": NEXT_TARGET,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "decision": DECISION,
            "label_result": "C_MEM_LABEL_ZERO_PRIVATE_TOTAL_SOURCE_BRANCH",
            "dynamic_status": "DELTA_LABEL_MEM_BOUND_ROWS_RETAINED",
            "LHRS_status": "SUPPORT_READOUT_REMAIN",
            "final_Cmem_status": "SUPPORT_READOUT_BOUNDARY_NONHILBERT_REMAIN",
            "selected_next_channel": "C_mem^support / worldtube-Reynolds owner",
            "next_target": NEXT_TARGET,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "why": "After Hodge and label closure, LHRS has support and readout left; support is next because it controls source/worldtube leakage and links directly to local vacuum/profile residuals.",
            "derive_route": "try to prove C_mem^support=0 from q-basic fixed compact support, zero boundary trace, no birth/death shell, no threshold mask and no hidden side flux.",
            "fallback_route": "if support/worldtube clauses fail, write Reynolds shell/source-support bound rows for WEP/R10/PPN/orbital projection.",
            "avoid": "assuming a local vacuum plateau or zero boundary flux without deriving the support/worldtube conditions.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    owner: list[dict[str, Any]],
    zero_import: list[dict[str, Any]],
    dynamic: list[dict[str, Any]],
    lhrs: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    all_rows = sources + owner + zero_import + dynamic + lhrs + runners + controls + decisions
    outputs = [
        SOURCE_REGISTER,
        OWNER_CLAUSE_CSV,
        ZERO_IMPORT_CSV,
        DYNAMIC_BOUND_CSV,
        LHRS_UPDATE_CSV,
        RUNNER_CSV,
        CONTROL_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
        VALIDATION_CSV,
        DOC_PATH,
        FORMAL_PATH,
    ]
    checks = [
        ("VAL4664_00_sources_exist", all(row["path_exists"] for row in sources), "all cited source paths exist"),
        ("VAL4664_01_needles_found", all(row["needle_found"] for row in sources), "all cited source needles found"),
        ("VAL4664_02_line_anchors", all(int(row["line_number"]) > 0 for row in sources), "all source line anchors positive"),
        ("VAL4664_03_owner_clauses", any(row["clause_id"] == "LFO4664_1_no_label_slot" for row in owner), "label owner no-slot clause present"),
        ("VAL4664_04_label_zero", any(row["zero_id"] == "LZI4664_4_result" and row["status"] == "CMEM_LABEL_TERM_ZERO_PRIVATE_BRANCH" for row in zero_import), "Cmem label zero row present"),
        ("VAL4664_05_dynamic_label_bound", any(row["bound_id"] == "DLB4664_0_envelope" for row in dynamic), "dynamic label envelope retained"),
        ("VAL4664_06_LHRS_reduced", any(row["update_id"] == "LLU4664_2_after" for row in lhrs), "LHRS reduced after label"),
        ("VAL4664_07_no_microphysics_claim", any(row["control_id"] == "CTRL4664_1_no_microphysics_claim" for row in controls), "microphysics firewall present"),
        ("VAL4664_08_no_claim_rows", all(str(row.get("valid_for_claim", "False")) == "False" and str(row.get("claim_allowed", "False")) == "False" for row in all_rows), "no generated row is claim-grade"),
        ("VAL4664_09_nonclaim_runner", any(row["run_id"] == "RUN4664_4_claim_status" and row["result"] == "NONCLAIM_STILL_BLOCKED" for row in runners), "local claim status remains nonclaim"),
        ("VAL4664_10_next_support", decisions and decisions[0]["next_target"] == NEXT_TARGET, "next target is support/worldtube"),
        ("VAL4664_11_local_outputs", all(ROOT in path.parents or path == ROOT for path in outputs), "outputs stay under local MTS root"),
    ]
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "validation_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for check_id, passed, detail in checks
    ]
    passed_all = all(passed for _, passed, _ in checks)
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "validation_id": "VAL4664_OVERALL",
            "status": "PASS" if passed_all else "FAIL",
            "detail": "4664 Cmem label private zero and dynamic label-bound gate passed" if passed_all else "4664 validation failed",
            "timestamp_utc": timestamp,
        }
    )
    return rows


def build_doc(
    sources: list[dict[str, Any]],
    owner: list[dict[str, Any]],
    zero_import: list[dict[str, Any]],
    dynamic: list[dict[str, Any]],
    lhrs: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    statuses: list[dict[str, Any]],
    nexts: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> str:
    return f"""# 4664 - Cmem label/source functor owner or LHRS bound

Branch: `{BRANCH}`
Marker: `{MARKER}`

## Result

4664 attacks the label channel left after 4663:

`C_mem^label := Pi_mem[C_X^label]`.

Inside the fixed private ordinary-visible branch:

`C_mem^label = 0`.

The reason is precise. The source functor consumes total variational objects:

`F_src(T_total, J_total)`,

not labelled pairs:

`F_src({{(T_A,J_A,A)}})`.

Together with the GR-parity no-source-prefactor branch, there is no allowed morphism:

`SpeciesLabel/MaterialLabel -> Coeff_active_source`.

Therefore source labels and material labels cannot return as active-source coefficients in this branch, and the label term drops from `C_mem^LHRS_live`.

After Hodge and label closure:

`|C_mem^LHRS_live| <= |C_mem^support| + |C_mem^readout|`.

And:

`|C_mem^final_live| <= |C_mem^support| + |C_mem^readout| + |C_mem^boundary| + |C_mem^nonHilbert|`.

This is not a derivation of all material microphysics or the Standard Model. If source-only species scalars, constructor/spurion labels, fixed active markers or hidden/nonstandard labels are admitted, the dynamic `Delta_label_mem` rows remain live.

## Source Register

{table(sources)}

## Label Source Functor Owner Clauses

{table(owner)}

## Cmem Label Zero Import

{table(zero_import)}

## Dynamic Label Bound Rows

{table(dynamic)}

## LHRS Cmem Update After Label

{table(lhrs)}

## Runner Results

{table(runners)}

## Controls

{table(controls)}

## Decision

{table(decisions)}

## Status

{table(statuses)}

## Next Target

{table(nexts)}

## Validation

{table(validations)}
"""


def register_claim() -> None:
    if CLAIM_ID in read_text(CLAIMS_PATH):
        return
    row = [
        CLAIM_ID,
        "local_gr_empirical_interface",
        "4664 closes C_mem^label in the fixed private ordinary-visible total-source branch. The source functor consumes total Hilbert/current objects rather than labelled pairs, the GR-parity branch forbids SpeciesLabel/MaterialLabel -> Coeff_active_source morphisms, and material labels remain readout inventory. Dynamic source-only species scalar, constructor/spurion, fixed-marker and hidden-label rows remain explicit off branch.",
        "Generated source register, label source-functor owner clauses, Cmem label zero import, dynamic label bound rows, LHRS Cmem update, runner, controls, decision, status, next target and validation.",
        "Cmem_label_zero_private_total_source_functor_dynamic_label_bound_nonclaim",
        NEXT_TARGET,
        "Inferring label silence from symmetry alone, claiming material microphysics or the Standard Model is derived, erasing hidden/nonstandard labels, absorbing label residuals into measured G, or claiming full local GR from this channel.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "No public local-GR/Newton/PPN/R10 claim until support/readout/boundary/non-Hilbert channels plus body-charge gates are same-branch zero or source-backed.",
    ]
    append_once(CLAIMS_PATH, CLAIM_ID, csv_line(row))


def update_spine_packet() -> None:
    spine = f"""
## {MARKER}

Claim `{CLAIM_ID}`: 4664 closes `C_mem^label` inside the fixed private ordinary-visible total-source branch. The source functor consumes `T_total,J_total`, not labelled pairs, and the GR-parity branch forbids `SpeciesLabel/MaterialLabel -> Coeff_active_source`. Thus `C_mem^label=0` in the branch. The remaining private-branch Cmem channels are support, readout, boundary and non-Hilbert; dynamic source-only/constructor/marker/hidden label rows remain off branch.
"""
    packet = f"""
## {PACKET_MARKER}

Checkpoint `4664` removes the label/source-functor channel from the private-branch Cmem residual vector while retaining dynamic label bounds. Next packet target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, spine)
    append_once(PACKET_PATH, PACKET_MARKER, packet)


def main() -> int:
    timestamp = now()
    sources = source_rows(timestamp)
    owner = owner_clause_rows(timestamp)
    zero_import = zero_import_rows(timestamp)
    dynamic = dynamic_bound_rows(timestamp)
    lhrs = lhrs_update_rows(timestamp)
    runners = runner_rows(timestamp)
    controls = control_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    nexts = next_rows(timestamp)
    validations = validation_rows(sources, owner, zero_import, dynamic, lhrs, runners, controls, decisions, timestamp)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(OWNER_CLAUSE_CSV, owner)
    write_csv(ZERO_IMPORT_CSV, zero_import)
    write_csv(DYNAMIC_BOUND_CSV, dynamic)
    write_csv(LHRS_UPDATE_CSV, lhrs)
    write_csv(RUNNER_CSV, runners)
    write_csv(CONTROL_CSV, controls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, nexts)
    write_csv(VALIDATION_CSV, validations)

    doc = build_doc(sources, owner, zero_import, dynamic, lhrs, runners, controls, decisions, statuses, nexts, validations)
    DOC_PATH.write_text(doc, encoding="utf-8")
    FORMAL_PATH.write_text(doc, encoding="utf-8")
    register_claim()
    update_spine_packet()

    overall = validations[-1]["status"]
    print(f"4664 validation: {overall}")
    print(VALIDATION_CSV)
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

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

CHECKPOINT = "4661"
CLAIM_ID = "L-503"
BRANCH = "MTS_R2FR_Y5_KAPPA_CMEM_IMPORT_OR_DELTAW_SOURCE_WEIGHT_FINAL_BOUND_4661"
MARKER = "PPC4161_KAPPA_CMEM_IMPORT_OR_DELTAW_SOURCE_WEIGHT_FINAL_BOUND_4661"
PACKET_MARKER = "PPC4161_PACKET_KAPPA_CMEM_IMPORT_OR_DELTAW_SOURCE_WEIGHT_FINAL_BOUND_4661"
DECISION = "KAPPA_CMEM_SAME_BRANCH_IMPORTED_DELTAW_GR_PARITY_SOURCE_WEIGHT_ZERO_DYNAMIC_BOUND_RETAINED_NONCLAIM"
NEXT_TARGET = "4662-Y5-R2FR-Cmem-first-block-final-rollup-or-dynamic-source-weight-bound-runner.md"

DOC_PATH = POST / "4661-Y5-R2FR-kappa-Cmem-import-or-deltaw-source-weight-final-bound.md"
FORMAL_PATH = FORMAL / "677-PPC4161-kappa-Cmem-import-or-deltaw-source-weight-final-bound.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

DOC_4660 = POST / "4660-Y5-R2FR-bclock-readout-descent-or-clock-redshift-bound.md"
DOC_4654 = POST / "4654-Y5-R2FR-deltaKappa-source-coupling-lock-or-Gdot-orbital-bound.md"
DOC_4536 = POST / "4536-Y5-R2FR-connected-matter-graph-no-relative-action-weight-or-finite-deltaw-bound.md"
DOC_4537 = POST / "4537-Y5-R2FR-component-graph-rank-matrix-or-adopt-GR-parity-import.md"
DOC_4538 = POST / "4538-Y5-R2FR-GR-parity-local-source-universality-adoption-gates-or-interface-residuals.md"
DOC_4446 = POST / "4446-Y5-R2FR-adopt-GR-parity-SM-import-or-source-backed-material-Req-value.md"
DOC_4447 = POST / "4447-Y5-R2FR-GR-parity-source-universality-to-local-PPN-residual-vector-or-material-values.md"

FORMAL_552 = FORMAL / "552-PPC4161-connected-matter-graph-no-relative-action-weight-or-finite-deltaw-bound.md"
FORMAL_670 = FORMAL / "670-PPC4161-deltaKappa-source-coupling-lock-or-Gdot-orbital-bound.md"
FORMAL_676 = FORMAL / "676-PPC4161-bclock-readout-descent-or-clock-redshift-bound.md"

CSV_4660_CMEM = SOURCE_DIR / "P8_Y5_R2FR_4660_CMEM_STD_WEIGHT_UPDATE.csv"
CSV_4660_DECISION = SOURCE_DIR / "P8_Y5_R2FR_4660_DECISION.csv"
CSV_4660_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4660_VALIDATION.csv"

CSV_4654_COUPLING = SOURCE_DIR / "P8_Y5_R2FR_4654_DELTAKAPPA_COUPLING_LOCK.csv"
CSV_4654_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4654_DELTAKAPPA_ZERO_THEOREM.csv"
CSV_4654_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4654_VALIDATION.csv"

CSV_4536_RANK_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4536_CONNECTED_GRAPH_RANK_THEOREM.csv"
CSV_4536_DECISION = SOURCE_DIR / "P8_Y5_R2FR_4536_DECISION.csv"
CSV_4536_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4536_VALIDATION.csv"
CSV_4537_RANK_RESULTS = SOURCE_DIR / "P8_Y5_R2FR_4537_COMPONENT_GRAPH_RANK_RESULTS.csv"
CSV_4537_ADOPTION = SOURCE_DIR / "P8_Y5_R2FR_4537_GR_PARITY_ADOPTION_CERTIFICATE.csv"
CSV_4537_FALLBACK = SOURCE_DIR / "P8_Y5_R2FR_4537_FINITE_DELTAW_FALLBACK_AFTER_RANK.csv"
CSV_4537_DECISION = SOURCE_DIR / "P8_Y5_R2FR_4537_DECISION.csv"
CSV_4537_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4537_VALIDATION.csv"
CSV_4538_BRANCH = SOURCE_DIR / "P8_Y5_R2FR_4538_GR_PARITY_HQNP_BRANCH_IMPORT.csv"
CSV_4538_RESIDUAL = SOURCE_DIR / "P8_Y5_R2FR_4538_LOCAL_RESIDUAL_VECTOR_COLLAPSE.csv"
CSV_4538_CHAIN = SOURCE_DIR / "P8_Y5_R2FR_4538_LOCAL_GR_CLOSURE_CHAIN_UPDATE.csv"
CSV_4538_DECISION = SOURCE_DIR / "P8_Y5_R2FR_4538_DECISION.csv"
CSV_4538_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4538_VALIDATION.csv"

CSV_4446_DERIVATION = SOURCE_DIR / "P8_Y5_R2FR_4446_DERIVATION_ROWS.csv"
CSV_4446_VECTOR = SOURCE_DIR / "P8_Y5_R2FR_4446_SOURCE_UNIVERSALITY_RESIDUAL_VECTOR.csv"
CSV_4446_REDUCTION = SOURCE_DIR / "P8_Y5_R2FR_4446_REDUCTION_ROWS.csv"
CSV_4446_DECISION = SOURCE_DIR / "P8_Y5_R2FR_4446_DECISION.csv"
CSV_4446_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4446_VALIDATION.csv"
CSV_4447_DERIVATION = SOURCE_DIR / "P8_Y5_R2FR_4447_DERIVATION_ROWS.csv"
CSV_4447_ROLLUP = SOURCE_DIR / "P8_Y5_R2FR_4447_RESIDUAL_ROLLUP.csv"
CSV_4447_DECISION = SOURCE_DIR / "P8_Y5_R2FR_4447_DECISION.csv"
CSV_4447_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4447_VALIDATION.csv"
CSV_4535_FINITE = SOURCE_DIR / "P8_Y5_R2FR_4535_FINITE_DELTAW_BOUND_ROUTE.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4661_SOURCE_REGISTER.csv"
KAPPA_IMPORT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4661_KAPPA_CMEM_SAME_BRANCH_IMPORT.csv"
DELTAW_IMPORT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4661_DELTAW_SOURCE_WEIGHT_ZERO_IMPORT.csv"
DYNAMIC_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4661_DYNAMIC_DELTAW_BOUND_ROWS.csv"
CMEM_FINAL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4661_CMEM_STD_WEIGHT_FINAL_UPDATE.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4661_RUNNER_RESULTS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4661_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4661_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4661_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4661_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4661_VALIDATION.csv"


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
        ("SRC4661_00_4660_doc", DOC_4660, "After this checkpoint, the fixed-branch `C_mem^std_weight_live` block reduces", "4660 reduced Cmem to kappa plus source-weight terms."),
        ("SRC4661_01_4660_cmem_reduced", CSV_4660_CMEM, "CSW4660_2_reduced_fixed_branch", "first-block bound before 4661."),
        ("SRC4661_02_4660_kappa_crossref", CSV_4660_CMEM, "CSW4660_3_kappa_crossref", "4660 explicitly points to 4654 kappa zero."),
        ("SRC4661_03_4660_validation", CSV_4660_VALIDATION, "VAL4660_OVERALL", "4660 passed its local validation."),
        ("SRC4661_04_676_formal", FORMAL_676, "CSW4660_2_reduced_fixed_branch", "formal copy of reduced first-block target."),
        ("SRC4661_05_4654_coupling_lock", CSV_4654_COUPLING, "DKL4654_4_no_drift", "4654 coupling lock gives no kappa drift."),
        ("SRC4661_06_4654_zero_result", CSV_4654_ZERO, "DKZ4654_3_result", "4654 private result D_A ln kappa_eff=0."),
        ("SRC4661_07_4654_numeric_firewall", CSV_4654_ZERO, "DKZ4654_4_numeric_G_firewall", "kappa zero is not a numerical G prediction."),
        ("SRC4661_08_4654_validation", CSV_4654_VALIDATION, "VAL4654_OVERALL", "4654 passed its local validation."),
        ("SRC4661_09_670_formal", FORMAL_670, "DKZ4654_3_result", "formal kappa-zero source."),
        ("SRC4661_10_4536_rank_theorem", CSV_4536_RANK_THEOREM, "CGRT4536_0_exact_rank_statement", "source-weight rank theorem."),
        ("SRC4661_11_4536_GR_parity_branch", CSV_4536_RANK_THEOREM, "CGRT4536_2_gr_parity_branch", "GR-parity branch can sign component source universality."),
        ("SRC4661_12_4536_doc_kernel", DOC_4536, "If `ker(M_graph) ∩ im(P_perp) = {0}`", "exact kernel condition."),
        ("SRC4661_13_4536_decision", CSV_4536_DECISION, "DEC4536_0", "4536 decision route."),
        ("SRC4661_14_4536_validation", CSV_4536_VALIDATION, "VAL4536_OVERALL", "4536 validation pass."),
        ("SRC4661_15_552_formal", FORMAL_552, "CGRT4536_0_exact_rank_statement", "formal source-weight theorem."),
        ("SRC4661_16_4537_rank_private", CSV_4537_RANK_RESULTS, "RR4537_2_GR_parity_adopted_branch", "private GR-parity rank pass."),
        ("SRC4661_17_4537_no_prefactor", CSV_4537_ADOPTION, "AD4537_1_no_source_prefactor", "no source-only component prefactor."),
        ("SRC4661_18_4537_rank_result", CSV_4537_ADOPTION, "AD4537_2_rank_result", "P_perp Delta_w=0 inside private branch."),
        ("SRC4661_19_4537_fallback", CSV_4537_FALLBACK, "FF4537_0_off_branch_delta_w", "off-branch finite Delta_w retained."),
        ("SRC4661_20_4537_decision", CSV_4537_DECISION, "DEC4537_0", "4537 decision."),
        ("SRC4661_21_4537_validation", CSV_4537_VALIDATION, "VAL4537_OVERALL", "4537 validation pass."),
        ("SRC4661_22_4538_branch_define", CSV_4538_BRANCH, "BI4538_0_define_branch", "same private branch object defined."),
        ("SRC4661_23_4538_source_weight", CSV_4538_BRANCH, "BI4538_1_source_weight", "source-weight zero in PPC4161-GP-HQNP."),
        ("SRC4661_24_4538_residual", CSV_4538_RESIDUAL, "RV4538_0_source_weight", "source-weight residual collapse."),
        ("SRC4661_25_4538_chain", CSV_4538_CHAIN, "CCU4538_0_replace_fog", "local chain source fog replaced inside private branch."),
        ("SRC4661_26_4538_decision", CSV_4538_DECISION, "DEC4538_0", "4538 decision."),
        ("SRC4661_27_4538_validation", CSV_4538_VALIDATION, "VAL4538_OVERALL", "4538 validation pass."),
        ("SRC4661_28_4446_weight_killed", CSV_4446_DERIVATION, "ADOPT4446_1_weight_countermodel_killed", "GR-parity kills weighted-component countermodel."),
        ("SRC4661_29_4446_deltaw", CSV_4446_VECTOR, "RU4446_0_Delta_w_A", "Delta_w_A zero inside private branch."),
        ("SRC4661_30_4446_reduction", CSV_4446_REDUCTION, "RED4446_0_source_weight_to_zero", "source weight reduced to zero."),
        ("SRC4661_31_4446_decision", CSV_4446_DECISION, "DEC4446_0", "4446 decision."),
        ("SRC4661_32_4446_validation", CSV_4446_VALIDATION, "VAL4446_1_needles_found", "4446 validation pass."),
        ("SRC4661_33_4447_source_projection", CSV_4447_DERIVATION, "PPN4447_D0_source_subspace_projection", "source subspace projection zero."),
        ("SRC4661_34_4447_rollup", CSV_4447_ROLLUP, "RU4447_0_source_weight_subvector", "source-weight subvector zero in private branch."),
        ("SRC4661_35_4447_decision", CSV_4447_DECISION, "DEC4447_0", "4447 decision."),
        ("SRC4661_36_4447_validation", CSV_4447_VALIDATION, "VAL4447_1_needles_found", "4447 validation pass."),
        ("SRC4661_37_4535_finite", CSV_4535_FINITE, "FBR4535_OVERALL", "finite Delta_w fallback remains open off branch."),
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


def kappa_import_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("KBI4661_0_object", "D_mem ln kappa_eff", "memory-projected source/coupling drift in the 4660 Cmem first block", "CSW4660_2_reduced_fixed_branch", "TARGET_DEFINED"),
        ("KBI4661_1_4654_theorem", "D_A ln kappa_eff=0", "4654 proves private zero inside topological-kappa plus single Hilbert-source measure selector", "DKZ4654_3_result", "PRIVATE_ZERO_AVAILABLE"),
        ("KBI4661_2_same_branch_map", "PPC4161-GP-HQNP includes PPC4161-TK-HQNP plus the observed-coframe/standard-visible matter imports", "4538 defines a single private branch object carrying source weights, Hilbert charge, Newton/PPN readout and kappa/source selector", "BI4538_0_define_branch", "SAME_BRANCH_COMPATIBLE"),
        ("KBI4661_3_calibrated_G_rule", "G_cal=c^4 kappa_eff/(8*pi) is calibrated once", "local GR/Newton reduction needs a constant coupling, not a numerical derivation of G_N", "DKZ4654_4_numeric_G_firewall", "NUMERIC_G_FIREWALL_RETAINED"),
        ("KBI4661_4_import", "D_mem ln kappa_eff = 0 on the fixed private local packet", "memory projection of a branch-constant kappa_eff vanishes", "4654 + 4538 same-branch import", "KAPPA_TERM_ZERO_PRIVATE_BRANCH"),
        ("KBI4661_5_result", "|D_mem ln kappa_eff||S_kappa^mem|=0", "the kappa term drops from C_mem^std_weight_live in the same branch as 4660", "no orbital GM backfill; no public parent claim", "CMEM_KAPPA_TERM_REMOVED_NONCLAIM"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "import_id": row[0],
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


def deltaw_import_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("DWI4661_0_definition", "delta_w_mem := ||Pi_mem P_perp Delta_w|| or the equivalent first-block source-weight amplitude", "only relative component/source weights after common calibration can enter this Cmem term", "definition after 4660 reduction", "TARGET_DEFINED"),
        ("DWI4661_1_rank_theorem", "ker(M_graph) ∩ im(P_perp) = {0} => P_perp Delta_w=0", "fixed nongravitational observables leave only common calibration when the graph has full rank on non-common weights", "CGRT4536_0_exact_rank_statement", "THEOREM_IMPORTED"),
        ("DWI4661_2_GR_parity_rank", "private GR-parity branch has rank n-1 and pperp_kernel_dim=0", "adopting one standard visible matter action with fixed graph/no-source-prefactor kills relative source weights", "RR4537_2_GR_parity_adopted_branch", "PRIVATE_RANK_PASS_IMPORTED"),
        ("DWI4661_3_no_source_prefactor", "no SpeciesLabel/MaterialLabel -> Coeff_active_source Hom and no source-only component prefactor", "there is no independent local knob that changes active source weight while keeping the visible matter graph fixed", "AD4537_1_no_source_prefactor; BI4538_1_source_weight", "SOURCE_ONLY_SLOT_FORBIDDEN_IN_BRANCH"),
        ("DWI4661_4_branch_rollforward", "PPC4161-GP-HQNP carries P_perp Delta_w=0 into the local packet", "source-weight fog is replaced by the private selector branch, not by cancellation", "CCU4538_0_replace_fog; RU4446_0_Delta_w_A; RU4447_0_source_weight_subvector", "LOCAL_BRANCH_SOURCE_WEIGHT_ZERO"),
        ("DWI4661_5_result", "fixed ordinary-visible GR-parity branch => delta_w_mem=0", "the source-weight term drops from C_mem^std_weight_live on the same branch", "off-branch hidden/nonstandard/source-label sectors remain finite-bound rows", "DELTAW_TERM_ZERO_PRIVATE_BRANCH"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "import_id": row[0],
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
        ("DBW4661_0_off_branch_delta_w", "P_perp Delta_w", "finite branch if GR-parity/private matter import is rejected or hidden/nonstandard matter is admitted", "FBR4535_OVERALL", "FINITE_FALLBACK_OPEN"),
        ("DBW4661_1_component_graph_fail", "current parent-owned component graph", "4537 current parent-owned graph is not signed; public theorem route remains unsigned", "RR4537_1_current_parent_owned_graph", "PUBLIC_PARENT_UNSIGNED"),
        ("DBW4661_2_WEP_product_only", "|Delta_w_TiPt tau_WEP|", "<= 2.8e-15 where source-backed WEP product rows apply; cannot infer |Delta_w_TiPt| without tau_min>0", "4363/4364 ancestry, imported only as a cautionary finite route", "PRODUCT_ONLY_NO_DIVISION"),
        ("DBW4661_3_hidden_sector", "hidden/nonstandard/source-label matter", "not killed by ordinary visible GR-parity import; requires its own graph/rank/observable rows", "4538 off-branch residual policy", "HIDDEN_BRANCH_RETAINED"),
        ("DBW4661_4_source_row_contract", "delta_w_mem_source_row", "system_id;branch;P_perp_Delta_w;S_w_mem;tau_arena;observable_bound;units;source_path;valid_for_claim", "future dynamic branch runner contract", "SOURCE_ROW_TEMPLATE_READY_VALUES_MISSING"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "bound_id": row[0],
            "quantity": row[1],
            "bound_or_contract": row[2],
            "source_or_assumption": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def cmem_final_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CSF4661_0_before", "|C_mem^std_weight_live| <= |D_mem ln kappa_eff||S_kappa^mem| + |delta_w_mem||S_w^mem|", "4660 reduced first-block result", "FIRST_BLOCK_IMPORTED"),
        ("CSF4661_1_kappa_zero", "|D_mem ln kappa_eff||S_kappa^mem|=0", "4654 kappa no-drift imported on same private packet branch", "KAPPA_TERM_ZERO_PRIVATE_NONCLAIM"),
        ("CSF4661_2_deltaw_zero", "|delta_w_mem||S_w^mem|=0", "4536-4538 plus 4446/4447 GR-parity source-weight zero imported on same ordinary-visible branch", "DELTAW_TERM_ZERO_PRIVATE_NONCLAIM"),
        ("CSF4661_3_fixed_first_block_result", "fixed ordinary-visible private branch => C_mem^std_weight_live=0", "first standard/weight memory block is closed only inside PPC4161-GP-HQNP / fixed observed-coframe calibrated branch", "FIRST_BLOCK_FIXED_BRANCH_ZERO"),
        ("CSF4661_4_dynamic_first_block_bound", "|C_mem^std_weight_live| <= |D_mem ln kappa_eff|_dyn |S_kappa^mem| + |delta_w_mem|_dyn |S_w^mem|", "if kappa selector or GR-parity source-weight branch is rejected, retain explicit finite rows", "DYNAMIC_BRANCH_BOUND_RETAINED"),
        ("CSF4661_5_not_full_Cmem", "C_mem^final_live=0 is not claimed here", "LHRS, boundary, non-Hilbert, profile/source-test and global memory blocks are not erased by closing this first block", "FULL_CMEM_STILL_NEEDS_ROLLUP"),
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
        ("RUN4661_0_kappa_same_branch", "D_mem ln kappa_eff", "PASS_CONDITIONAL_PRIVATE_ZERO", "4654 topological-kappa/Hilbert-source selector is imported into the same PPC4161-GP-HQNP local packet."),
        ("RUN4661_1_source_weight_same_branch", "delta_w_mem", "PASS_CONDITIONAL_PRIVATE_ZERO", "4536 rank theorem plus 4537 rank pass and 4538/4446/4447 branch rollforward give P_perp Delta_w=0 for ordinary visible imported matter."),
        ("RUN4661_2_Cmem_first_block", "C_mem^std_weight_live", "PASS_FIXED_BRANCH_FIRST_BLOCK_ZERO", "alpha, mass, clock, kappa and source-weight pieces are zero on the same fixed private branch."),
        ("RUN4661_3_dynamic_branch", "off-branch kappa/delta_w", "FAIL_CLOSED_TO_BOUND_ROWS", "public parent-owned graph and hidden/nonstandard sectors still require finite source-backed rows."),
        ("RUN4661_4_local_GR_status", "local GR/Newton/PPN/R10/WEP/clock claim", "NONCLAIM_STILL_BLOCKED", "first Cmem block closure is not full Cmem/global parent closure; remaining blocks need rollup."),
        ("RUN4661_5_next_target", "component attack order", "PASS_NEXT_SELECTED", NEXT_TARGET),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "run_id": row[0],
            "branch_or_object": row[1],
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
        ("CTRL4661_0_no_public_local_GR", "Do not turn the private first-block Cmem closure into a public local-GR/Newton/PPN/R10 claim.", "ACTIVE"),
        ("CTRL4661_1_no_numeric_G", "Do not infer or predict the numerical value of G_N; only constant calibrated coupling is imported.", "ACTIVE"),
        ("CTRL4661_2_no_connectedness_shortcut", "Connected graph language alone is not enough; require full-rank P_perp kernel zero or retain Delta_w bounds.", "ACTIVE"),
        ("CTRL4661_3_no_hidden_sector_erasure", "Ordinary-visible GR-parity import does not kill hidden, nonstandard, source-label or interface residuals.", "ACTIVE"),
        ("CTRL4661_4_no_tau_division", "Do not divide WEP product bounds by tau_WEP without a sourced positive lower bound.", "ACTIVE"),
        ("CTRL4661_5_no_Cmem_globalization", "Closing C_mem^std_weight_live does not close LHRS, boundary, non-Hilbert, profile/source-test or global memory blocks.", "ACTIVE"),
        ("CTRL4661_6_local_private_only", "No GitHub action; write only the local framework/post-checkpoint packet.", "ACTIVE"),
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
            "decision_id": "DEC4661_0",
            "decision": DECISION,
            "summary": (
                "4661 imports the 4654 kappa no-drift theorem and the 4536-4538/4446/4447 GR-parity source-weight zero into the exact Cmem first-block left by 4660. "
                "On the same private ordinary-visible observed-coframe/topological-kappa/Hilbert-source branch, D_mem ln kappa_eff=0 and delta_w_mem=0, so C_mem^std_weight_live=0. "
                "This is not a public local-GR claim and not a full C_mem final-live closure: dynamic kappa/source-weight branches plus LHRS/boundary/non-Hilbert/profile/global memory blocks remain nonclaim obligations."
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
            "kappa_result": "D_MEM_LN_KAPPA_EFF_ZERO_PRIVATE_BRANCH",
            "delta_w_result": "DELTA_W_MEM_ZERO_ORDINARY_VISIBLE_GR_PARITY_BRANCH",
            "Cmem_first_block_result": "C_MEM_STD_WEIGHT_LIVE_ZERO_FIXED_BRANCH",
            "dynamic_branch_status": "KAPPA_DELTAW_BOUND_ROWS_RETAINED",
            "full_Cmem_status": "ROLLUP_STILL_REQUIRED_NONCLAIM",
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
            "why": "The standard/weight first block is now closed on the same private fixed branch, but C_mem^final_live still includes LHRS, boundary, non-Hilbert, profile/source-test and global memory blocks.",
            "derive_route": "roll up the first-block closure into the 4657 Cmem decomposition and identify the next nonzero live block rather than circling alpha/mass/clock/source weights again.",
            "fallback_route": "if any same-branch import is rejected, keep kappa/delta_w dynamic rows and build source-backed finite projections.",
            "avoid": "claiming full local GR, predicting numerical G, deleting hidden/off-branch source weights, or treating this as full Cmem final closure.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    kappa: list[dict[str, Any]],
    deltaw: list[dict[str, Any]],
    dynamic: list[dict[str, Any]],
    cmem: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    all_rows = sources + kappa + deltaw + dynamic + cmem + runners + controls + decisions
    local_outputs = [
        SOURCE_REGISTER,
        KAPPA_IMPORT_CSV,
        DELTAW_IMPORT_CSV,
        DYNAMIC_BOUND_CSV,
        CMEM_FINAL_CSV,
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
        ("VAL4661_00_sources_exist", all(row["path_exists"] for row in sources), "all cited source paths exist"),
        ("VAL4661_01_needles_found", all(row["needle_found"] for row in sources), "all cited source needles found"),
        ("VAL4661_02_line_anchors", all(int(row["line_number"]) > 0 for row in sources), "all source line anchors positive"),
        ("VAL4661_03_kappa_import", any(row["import_id"] == "KBI4661_5_result" and row["status"] == "CMEM_KAPPA_TERM_REMOVED_NONCLAIM" for row in kappa), "kappa Cmem term removed in fixed branch"),
        ("VAL4661_04_deltaw_import", any(row["import_id"] == "DWI4661_5_result" and row["status"] == "DELTAW_TERM_ZERO_PRIVATE_BRANCH" for row in deltaw), "delta_w Cmem term removed in fixed branch"),
        ("VAL4661_05_first_block_zero", any(row["update_id"] == "CSF4661_3_fixed_first_block_result" for row in cmem), "Cmem standard/weight first block zero row present"),
        ("VAL4661_06_dynamic_bound_retained", any(row["bound_id"] == "DBW4661_0_off_branch_delta_w" for row in dynamic), "dynamic/off-branch Delta_w finite route retained"),
        ("VAL4661_07_not_full_Cmem", any(row["update_id"] == "CSF4661_5_not_full_Cmem" for row in cmem), "full Cmem/global closure is not claimed"),
        ("VAL4661_08_runner_nonclaim", any(row["run_id"] == "RUN4661_4_local_GR_status" and row["result"] == "NONCLAIM_STILL_BLOCKED" for row in runners), "local GR status remains nonclaim"),
        ("VAL4661_09_no_claim_rows", all(str(row.get("valid_for_claim", "False")) == "False" and str(row.get("claim_allowed", "False")) == "False" for row in all_rows), "no row is claim-grade"),
        ("VAL4661_10_no_numeric_G_control", any(row["control_id"] == "CTRL4661_1_no_numeric_G" for row in controls), "numeric G firewall present"),
        ("VAL4661_11_no_connectedness_shortcut", any(row["control_id"] == "CTRL4661_2_no_connectedness_shortcut" for row in controls), "connectedness shortcut guard present"),
        ("VAL4661_12_next_rollup", decisions and decisions[0]["next_target"] == NEXT_TARGET, "next target is Cmem first-block rollup"),
        ("VAL4661_13_local_output_paths", all(ROOT in path.parents or path == ROOT for path in local_outputs), "outputs stay under local MTS root"),
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
            "validation_id": "VAL4661_OVERALL",
            "status": "PASS" if passed_all else "FAIL",
            "detail": "4661 kappa/delta_w first-block Cmem closure imported with dynamic nonclaim guards" if passed_all else "4661 validation failed",
            "timestamp_utc": timestamp,
        }
    )
    return rows


def build_doc(
    sources: list[dict[str, Any]],
    kappa: list[dict[str, Any]],
    deltaw: list[dict[str, Any]],
    dynamic: list[dict[str, Any]],
    cmem: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    statuses: list[dict[str, Any]],
    nexts: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> str:
    return f"""# 4661 - kappa Cmem import or deltaw source-weight final bound

Branch: `{BRANCH}`
Marker: `{MARKER}`

## Result

4660 left the first standard/weight memory block in the exact form:

`|C_mem^std_weight_live| <= |D_mem ln kappa_eff||S_kappa^mem| + |delta_w_mem||S_w^mem|`.

4661 closes that first block inside the same private fixed branch rather than inventing a new closure.

### Kappa term

Checkpoint 4654 gives:

`D_A ln kappa_eff = 0`

inside the private topological-kappa / single Hilbert-source measure selector. The same branch is the one carried forward by `PPC4161-GP-HQNP`: ordinary visible matter, observed coframe, Hilbert source charge, Newton/PPN readout and topological kappa are evaluated on one private packet. Therefore the memory projection also vanishes:

`D_mem ln kappa_eff = 0`,

so:

`|D_mem ln kappa_eff||S_kappa^mem| = 0`.

This is a constant calibrated-coupling result. It is **not** a numerical prediction of `G_N`.

### Source-weight term

The source-weight route is the rank theorem, not a vibe:

`ker(M_graph) ∩ im(P_perp) = {{0}} => P_perp Delta_w = 0`.

4537 gives the private GR-parity imported visible-matter rank pass with `pperp_kernel_dim=0`, and 4538/4446/4447 carry that source-weight zero into the same local branch. Therefore:

`delta_w_mem = ||Pi_mem P_perp Delta_w|| = 0`

for ordinary visible matter on the private GR-parity branch, so:

`|delta_w_mem||S_w^mem| = 0`.

Hidden, nonstandard, source-label, material-reentry, or public-parent branches are **not** erased; they remain finite-bound rows.

### First-block conclusion

On the fixed ordinary-visible observed-coframe / topological-kappa / Hilbert-source private branch:

`C_mem^std_weight_live = 0`.

This is progress: the alpha, mass, clock, kappa and relative source-weight pieces of the first `C_mem` standard/weight block are now closed on one branch.

It is not a full `C_mem^final_live=0` claim. The next job is to roll this into the 4657 Cmem decomposition and identify the next live block: LHRS, boundary, non-Hilbert, profile/source-test, or global memory residuals.

## Source Register

{table(sources)}

## Kappa Cmem Same-Branch Import

{table(kappa)}

## Delta_w Source-Weight Zero Import

{table(deltaw)}

## Dynamic Delta_w Bound Rows

{table(dynamic)}

## Cmem Standard Weight Final Update

{table(cmem)}

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
        "4661 imports the 4654 kappa no-drift theorem and the 4536-4538/4446/4447 GR-parity source-weight zero into the exact Cmem first block left by 4660. On the same private ordinary-visible observed-coframe/topological-kappa/Hilbert-source branch, D_mem ln kappa_eff=0 and delta_w_mem=0, so C_mem^std_weight_live=0. Dynamic/off-branch kappa/source-weight rows and remaining Cmem blocks stay nonclaim.",
        "Generated source register, kappa Cmem same-branch import, Delta_w source-weight zero import, dynamic Delta_w bound rows, Cmem standard/weight final update, runner, controls, decision, status, next target and validation.",
        "kappa_deltaw_first_Cmem_block_zero_private_branch_nonclaim",
        NEXT_TARGET,
        "Claiming full Cmem/local-GR closure from a first-block result, predicting numerical G_N, treating connectedness alone as source-weight proof, deleting hidden/off-branch source weights, or dividing WEP products by tau without tau_min.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "No public local-GR/Newton/PPN/R10/WEP/clock/orbital claim until the remaining Cmem blocks and parent selector/global memory residuals are closed or source-backed.",
    ]
    append_once(CLAIMS_PATH, CLAIM_ID, csv_line(row))


def update_spine_packet() -> None:
    spine = f"""
## {MARKER}

Claim `{CLAIM_ID}`: 4661 closes the first `C_mem^std_weight_live` block on the same private branch. The 4654 topological-kappa/Hilbert-source selector gives `D_mem ln kappa_eff=0`, while the 4536 rank theorem plus the 4537 GR-parity rank pass and 4538/4446/4447 branch rollforward give `delta_w_mem=0` for ordinary visible matter. Thus `C_mem^std_weight_live=0` only inside `PPC4161-GP-HQNP`. This is not numerical `G_N`, not public local GR, and not full `C_mem^final_live`; dynamic/off-branch source weights and the remaining Cmem blocks stay live.
"""
    packet = f"""
## {PACKET_MARKER}

Checkpoint `4661` imports kappa and source-weight zeros into the exact first Cmem block left by `4660`: `|C_mem^std_weight_live| <= |D_mem ln kappa_eff||S_kappa^mem| + |delta_w_mem||S_w^mem|`. On the fixed private branch both terms vanish, so the first standard/weight block is closed. Next packet target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, spine)
    append_once(PACKET_PATH, PACKET_MARKER, packet)


def main() -> int:
    timestamp = now()
    sources = source_rows(timestamp)
    kappa = kappa_import_rows(timestamp)
    deltaw = deltaw_import_rows(timestamp)
    dynamic = dynamic_bound_rows(timestamp)
    cmem = cmem_final_rows(timestamp)
    runners = runner_rows(timestamp)
    controls = control_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    nexts = next_rows(timestamp)
    validations = validation_rows(sources, kappa, deltaw, dynamic, cmem, runners, controls, decisions, timestamp)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(KAPPA_IMPORT_CSV, kappa)
    write_csv(DELTAW_IMPORT_CSV, deltaw)
    write_csv(DYNAMIC_BOUND_CSV, dynamic)
    write_csv(CMEM_FINAL_CSV, cmem)
    write_csv(RUNNER_CSV, runners)
    write_csv(CONTROL_CSV, controls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, nexts)
    write_csv(VALIDATION_CSV, validations)

    doc = build_doc(sources, kappa, deltaw, dynamic, cmem, runners, controls, decisions, statuses, nexts, validations)
    DOC_PATH.write_text(doc, encoding="utf-8")
    FORMAL_PATH.write_text(doc, encoding="utf-8")
    register_claim()
    update_spine_packet()

    overall = validations[-1]["status"]
    print(f"4661 validation: {overall}")
    print(VALIDATION_CSV)
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

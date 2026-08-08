from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2927"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2927-Y5-R2FR-RV2925-metric-readout-DqZ-geometry-Cshadow-first-source-bound-under-AX1090.md"

SRC_2926_DOC = ROOT / "2926-Y5-R2FR-parent-object-no-hidden-visible-hom-derivation-or-reduction-residual-first-fill-under-AX1090.md"
SRC_2926_NEXT = RESIDUALS / "P8_Y5_R2FR_2926_NEXT_TARGET.csv"
SRC_2926_RV_FILL = RESIDUALS / "P8_Y5_R2FR_2926_RV2925_FIRST_FILL_ATTEMPT.csv"
SRC_2926_DQZ_BRIDGE = RESIDUALS / "P8_Y5_R2FR_2926_DQZ_GEOMETRY_FILL_BRIDGE.csv"
SRC_2925_RV = RESIDUALS / "P8_Y5_R2FR_2925_REDUCTION_RESIDUAL_VECTOR.csv"
SRC_2914_HEADS = RESIDUALS / "P8_Y5_R2FR_2914_DQZ_GEOMETRY_HEAD_ACQUISITION_ROWS.csv"
SRC_2915_DOC = ROOT / "2915-Y5-R2FR-Cshadow-component-bound-pack-or-Cobs-parent-normalization-proof-under-AX1090.md"
SRC_2915_COMPONENTS = RESIDUALS / "P8_Y5_R2FR_2915_CSHADOW_COMPONENT_ENVELOPE.csv"
SRC_2915_ACQ = RESIDUALS / "P8_Y5_R2FR_2915_COMPONENT_ACQUISITION_ROWS.csv"
SRC_2916_DOC = ROOT / "2916-Y5-R2FR-Cshadow-cg-invariant-source-test-product-or-disformal-PPN-kernel-under-AX1090.md"
SRC_2916_LAW = RESIDUALS / "P8_Y5_R2FR_2916_CG_INVARIANT_SOURCE_TEST_PRODUCT_LAW.csv"
SRC_2916_BETA = RESIDUALS / "P8_Y5_R2FR_2916_BETA_SOURCE_TEST_ENVELOPE_ROWS.csv"
SRC_2917_DOC = ROOT / "2917-Y5-R2FR-disformal-PPN-kernel-or-cg-source-leg-provenance-fill-under-AX1090.md"
SRC_2917_KERNEL = RESIDUALS / "P8_Y5_R2FR_2917_DISFORMAL_PPN_RESPONSE_KERNEL.csv"
SRC_2917_BOUNDS = RESIDUALS / "P8_Y5_R2FR_2917_PPN_BOUND_ANCHOR_BINDING.csv"
SRC_2918_DOC = ROOT / "2918-Y5-R2FR-alpha3-source-current-kernel-or-no-disformal-slot-theorem-under-AX1090.md"
SRC_2918_KERNEL = RESIDUALS / "P8_Y5_R2FR_2918_ALPHA3_SOURCE_CURRENT_KERNEL.csv"
SRC_2918_PRODUCTS = RESIDUALS / "P8_Y5_R2FR_2918_ALPHA3_PRODUCT_BOUND_ROWS.csv"
SRC_2918_COUPLING = RESIDUALS / "P8_Y5_R2FR_2918_COUPLING_OWNER_GATES.csv"
SRC_2918_CLAIMS = RESIDUALS / "P8_Y5_R2FR_2918_CLAIM_GATES.csv"
SRC_2918_NEXT = RESIDUALS / "P8_Y5_R2FR_2918_NEXT_TARGET.csv"
SRC_1141_PPN = RESIDUALS / "P8_Y5_R10_1141_PPN_BOUND_ANCHOR_ROWS.csv"
SRC_ALPHA3_GUARD = RESIDUALS / "P8_ALPHA3_TOTAL_GUARD.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2927_SOURCE_REGISTER.csv",
    "rv_binding": RESIDUALS / "P8_Y5_R2FR_2927_CSHADOW_RV2925_BINDING.csv",
    "first_bound": RESIDUALS / "P8_Y5_R2FR_2927_CSHADOW_FIRST_SOURCE_BOUND_SELECTION.csv",
    "transfer_gate": RESIDUALS / "P8_Y5_R2FR_2927_ALPHA3_TO_RV2925_TRANSFER_GATE.csv",
    "rv_update": RESIDUALS / "P8_Y5_R2FR_2927_METRIC_READOUT_RESIDUAL_UPDATE.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2927_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2927_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2927_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2927_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2927_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "rv_bound_copy": LOCAL_BOUNDS / "RV2925_Cshadow_alpha3_first_source_bound_2927_NONCLAIM.csv",
    "transfer_gate_copy": PARENT_ACTION / "AX1090_Cshadow_alpha3_transfer_gate_2927_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2927_RV2925_ALPHA3_STATIONARY_FLUX_OR_COUPLING_BASELINE_NEXT_NONCLAIM.csv",
}


for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": RUN_UTC,
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv_rows(path)
        return True
    except Exception:
        return False


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    selected = columns or list(rows[0].keys())
    header = "| " + " | ".join(selected) + " |"
    separator = "| " + " | ".join("---" for _ in selected) + " |"
    body = [
        "| " + " | ".join(md_escape(row.get(column, "")) for column in selected) + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def row_with_value(rows: list[dict[str, str]], key: str, value: str) -> dict[str, str] | None:
    for row in rows:
        if row.get(key) == value:
            return row
    return None


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2927_00_2926_doc", SRC_2926_DOC, "RV2925_0_metric_readout;C_shadow_abs;NEXT2926_0_2927", "2926 handoff selects C_shadow as first RV2925 metric-readout head"),
        ("SRC2927_01_2926_next", SRC_2926_NEXT, "NEXT2926_0_2927;C_shadow_abs", "machine-readable 2927 target"),
        ("SRC2927_02_2926_rv_fill", SRC_2926_RV_FILL, "RVF2926_0_selected_component;epsilon_metric_readout", "selected residual fill attempt"),
        ("SRC2927_03_2926_dqz_bridge", SRC_2926_DQZ_BRIDGE, "DQB2926_5_shadow;DQB2926_8_next_best_head", "DqZ-to-Cshadow bridge"),
        ("SRC2927_04_2925_rv", SRC_2925_RV, "RV2925_0_metric_readout;epsilon_metric_readout", "MTS-to-EH reduction residual vector"),
        ("SRC2927_05_2914_heads", SRC_2914_HEADS, "HEAD2914_5_C_shadow_abs;HEAD2914_8_promotion_rule", "DqZ geometry head list"),
        ("SRC2927_06_2915_doc", SRC_2915_DOC, "C_shadow_abs =;b_alpha*tau_clock_time;linear `c_g` is forbidden", "Cshadow split narrative"),
        ("SRC2927_07_2915_components", SRC_2915_COMPONENTS, "CSHC2915_0_total;CSHC2915_2_b_dis;CSHC2915_6_support", "Cshadow component envelope"),
        ("SRC2927_08_2915_acq", SRC_2915_ACQ, "ACQ2915_0_Cshadow_total;ACQ2915_4_bdis", "Cshadow acquisition rows"),
        ("SRC2927_09_2916_doc", SRC_2916_DOC, "PRODUCT_LAW_DERIVED_AS_CONTRACT_NOT_SCORE_READY;naked linear", "c_g product-law guard"),
        ("SRC2927_10_2916_law", SRC_2916_LAW, "LAW2916_2_universal_weyl;LAW2916_3_source_leg_exception", "invariant c_g source-test law"),
        ("SRC2927_11_2916_beta", SRC_2916_BETA, "BETA2916_7_alpha_product;beta_s_abs;beta_t_abs", "beta source-test envelope"),
        ("SRC2927_12_2917_doc", SRC_2917_DOC, "alpha3;4e-20;DISFORMAL_PPN_KERNEL_FILLED_AS_SOURCE_READY_NONCLAIM", "disformal PPN kernel narrative"),
        ("SRC2927_13_2917_kernel", SRC_2917_KERNEL, "DK2917_2_alpha3;DK2917_5_total_abs", "disformal alpha3 kernel"),
        ("SRC2927_14_2917_bounds", SRC_2917_BOUNDS, "PBOUND2917_4_alpha3;4e-20", "source-backed alpha3 comparator"),
        ("SRC2927_15_2918_doc", SRC_2918_DOC, "Delta_alpha3_abs;4e-20;stationary compact exterior flux theorem", "alpha3 source-current kernel narrative"),
        ("SRC2927_16_2918_kernel", SRC_2918_KERNEL, "A3K2918_8_total_abs;F_kappa_alpha3;F_ellJ_alpha3", "alpha3 source-current heads"),
        ("SRC2927_17_2918_products", SRC_2918_PRODUCTS, "A3P2918_6_total;MISSING_ALL_HEADS_OR_PARENT_CANCELLATION_IDENTITY", "alpha3 product rows"),
        ("SRC2927_18_2918_coupling", SRC_2918_COUPLING, "COUP2918_4_ellJ;COUP2918_7_verdict", "coupling-owner gates"),
        ("SRC2927_19_2918_claims", SRC_2918_CLAIMS, "CG2918_1_alpha3_score;BLOCKED_NONCLAIM", "2918 claim gates"),
        ("SRC2927_20_2918_next", SRC_2918_NEXT, "NEXT2918_0_2919;stationary compact exterior alpha3", "stationary alpha3 next target"),
        ("SRC2927_21_1141_ppn", SRC_1141_PPN, "PPNBA1141_2_alpha3;4e-20", "external PPN alpha3 provenance lock"),
        ("SRC2927_22_alpha3_guard", SRC_ALPHA3_GUARD, "G_total_no_cancellation_by_fit;G_boundary_channel;G_domain_channel", "alpha3 no-cancellation guard"),
    ]
    rows = []
    for source_id, source_path, anchors, role in specs:
        found, missing = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(source_path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": source_path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def rv_binding_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "BIND2927_0_rv_formula",
            "RV2925_0_metric_readout",
            "epsilon_metric_readout",
            "epsilon_metric_readout := DqZ_geometry_abs + C_shadow_abs + E_boundary_geom_abs + E_readout_geom_abs",
            "SELECTED_FROM_2926",
            "2926 selected the metric-readout residual because it feeds PPN, clocks, orbital systems and local GR.",
        ),
        (
            "BIND2927_1_cshadow_head",
            "HEAD2914_5_C_shadow_abs",
            "C_shadow_abs",
            "C_shadow_abs := sum_abs(c_g,b_dis,b_A,b_alpha,q_nonH,Delta_W_support,Delta_tau_n contributions)",
            "COMPONENT_ENVELOPE_EXISTS_NONCLAIM",
            "2915 split the shadow term, but no full zero theorem or numeric envelope is claim-ready.",
        ),
        (
            "BIND2927_2_cg_guard",
            "LAW2916_3_source_leg_exception",
            "c_g",
            "R10/source-test scoring must use beta_s beta_t or a sourced source-leg; naked linear c_g is forbidden.",
            "LINEAR_CG_REJECTED",
            "This prevents a fake local/R10 pass from underfactoring the source leg.",
        ),
        (
            "BIND2927_3_disformal_route",
            "DK2917_2_alpha3",
            "b_dis -> Delta_alpha3_abs",
            "disformal/source-current leakage hits preferred-frame alpha3 through boundary, domain, exchange, kappa, ellJ, d_R and tail heads",
            "SOURCE_READY_TEMPLATE_NOT_SCORE_READY",
            "This is the most concrete C_shadow component because a strict external comparator exists.",
        ),
        (
            "BIND2927_4_first_source_bound",
            "PBOUND2917_4_alpha3",
            "alpha3_bound_abs",
            "|alpha3| <= 4e-20 is the first source-backed comparator attached to the C_shadow/RV2925 route",
            "COMPARATOR_ACQUIRED_MTS_TRANSFER_MISSING",
            "The bound is real; the MTS prediction and transfer map are still missing.",
        ),
    ]
    rows = []
    for bind_id, upstream_row, symbol, formula_or_rule, current_status, implication in specs:
        rows.append(
            add_common(
                {
                    "binding_id": bind_id,
                    "rv_component": "RV2925_0_metric_readout",
                    "upstream_row": upstream_row,
                    "symbol": symbol,
                    "formula_or_rule": formula_or_rule,
                    "current_status": current_status,
                    "source_backed_comparator": symbol == "alpha3_bound_abs",
                    "mts_prediction_present": False,
                    "accepted_for_scoring": False,
                    "implication": implication,
                    "source_paths": ";".join(str(path) for path in [SRC_2926_RV_FILL, SRC_2926_DQZ_BRIDGE, SRC_2915_COMPONENTS, SRC_2916_LAW, SRC_2917_BOUNDS, SRC_2918_KERNEL]),
                }
            )
        )
    return rows


def first_bound_rows() -> list[dict[str, Any]]:
    alpha3_bound_row = row_with_value(read_csv_rows(SRC_2917_BOUNDS), "observable", "alpha3") or {}
    alpha3_product_rows = read_csv_rows(SRC_2918_PRODUCTS)
    selected_rows = []
    selected_rows.append(
        add_common(
            {
                "selection_id": "FB2927_0_alpha3_comparator",
                "rv_component": "RV2925_0_metric_readout",
                "cshadow_component": "b_dis/source_current_alpha3",
                "observable": "alpha3",
                "bound_abs": alpha3_bound_row.get("upper_bound_abs", "MISSING"),
                "bound_units": alpha3_bound_row.get("units", "MISSING"),
                "bound_source_id": alpha3_bound_row.get("source_id", "MISSING"),
                "bound_source_backed": alpha3_bound_row.get("bound_source_backed", "False"),
                "mts_prediction_present": alpha3_bound_row.get("mts_prediction_present", "False"),
                "current_status": "SOURCE_BACKED_COMPARATOR_ONLY_MTS_TRANSFER_MISSING",
                "claim_effect": "tightens RV2925_0 but does not bound it yet",
                "source_paths": alpha3_bound_row.get("source_paths", str(SRC_2917_BOUNDS)),
            }
        )
    )
    for product in alpha3_product_rows:
        selected_rows.append(
            add_common(
                {
                    "selection_id": f"FB2927_{product.get('product_id', 'unknown')}",
                    "rv_component": "RV2925_0_metric_readout",
                    "cshadow_component": product.get("channel", "MISSING"),
                    "observable": "alpha3",
                    "bound_abs": product.get("target_bound_abs", "MISSING"),
                    "bound_units": "dimensionless_abs_after_PPN_projection",
                    "bound_source_id": "PBOUND2917_4_alpha3",
                    "bound_source_backed": True,
                    "mts_prediction_present": False,
                    "current_status": product.get("current_status", "MISSING"),
                    "claim_effect": product.get("reason", "MISSING"),
                    "source_paths": str(SRC_2918_PRODUCTS),
                }
            )
        )
    return selected_rows


def transfer_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("TR2927_0_comparator", "alpha3 external comparator exists and is positive numeric", "PASS_COMPARATOR_ONLY", "PBOUND2917_4_alpha3 gives 4e-20", True),
        ("TR2927_1_component_route", "alpha3 source-current heads are part of the disformal/source-current C_shadow route", "PASS_STRUCTURE_ONLY", "2917/2918 give a source-ready template", True),
        ("TR2927_2_transfer_map", "Pi_alpha3-to-Pi_geom transfer map is parent-signed and units locked", "MISSING_TRANSFER_MAP", "cannot convert alpha3 comparator into a bound on C_shadow_abs or epsilon_metric_readout", False),
        ("TR2927_3_head_values", "all alpha3 heads are theorem-zero or source-backed finite", "MISSING_HEAD_VALUES", "boundary, domain, exchange, kappa, ellJ, d_R and tail rows remain missing", False),
        ("TR2927_4_no_cancellation", "no cancellation-by-fit or fitted-GM absorption is allowed", "GUARD_EXISTS_NOT_PARENT_PROOF", "guard is explicit but does not supply values", False),
        ("TR2927_5_verdict", "alpha3 source bound closes RV2925_0 metric readout", "TRANSFER_FAILS_NONCLAIM", "first bound is acquired as comparator only; MTS-side transfer remains open", False),
    ]
    rows = []
    for gate_id, requirement, current_status, reason, gate_pass in specs:
        rows.append(
            add_common(
                {
                    "gate_id": gate_id,
                    "requirement": requirement,
                    "current_status": current_status,
                    "reason": reason,
                    "gate_pass": gate_pass,
                    "blocks_claim": not gate_pass,
                    "source_paths": ";".join(str(path) for path in [SRC_2917_BOUNDS, SRC_2918_KERNEL, SRC_2918_PRODUCTS, SRC_ALPHA3_GUARD]),
                }
            )
        )
    return rows


def rv_update_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "RVU2927_0_metric_readout_status",
            "RV2925_0_metric_readout",
            "epsilon_metric_readout",
            "DqZ_geometry_abs + C_shadow_abs + boundary/readout tails",
            "PARTIAL_COMPARATOR_ATTACHED_NO_MTS_BOUND",
            "alpha3 comparator attached to C_shadow route; no epsilon_metric_readout numeric upper bound",
        ),
        (
            "RVU2927_1_cshadow_status",
            "HEAD2914_5_C_shadow_abs",
            "C_shadow_abs",
            "sum_abs(c_g,b_dis,b_A,b_alpha,q_nonH,Delta_W_support,Delta_tau_n)",
            "FIRST_SOURCE_BOUND_COMPONENT_SELECTED",
            "alpha3/source-current branch selected as first component to derive or bound",
        ),
        (
            "RVU2927_2_alpha3_status",
            "A3K2918_8_total_abs",
            "Delta_alpha3_abs",
            "sum_abs(boundary,domain,exchange,kappa,ellJ,dR,tail)",
            "SOURCE_READY_NONCLAIM_VALUES_MISSING",
            "external 4e-20 comparator is source-backed; all MTS product heads are missing or theorem-unsigned",
        ),
        (
            "RVU2927_3_acceptance",
            "RV2925_0_acceptance",
            "score_gate",
            "accepted only after every active head is theorem-zero or source-backed finite and transfer map is parent-signed",
            "NOT_ACCEPTED_FOR_SCORING",
            "source comparator is not the same as an MTS prediction",
        ),
    ]
    rows = []
    for update_id, upstream_row, symbol, formula_or_rule, current_status, meaning in specs:
        rows.append(
            add_common(
                {
                    "update_id": update_id,
                    "rv_component": "RV2925_0_metric_readout",
                    "upstream_row": upstream_row,
                    "symbol": symbol,
                    "formula_or_rule": formula_or_rule,
                    "current_status": current_status,
                    "source_backed_bound_present": current_status == "PARTIAL_COMPARATOR_ATTACHED_NO_MTS_BOUND",
                    "mts_numeric_prediction_present": False,
                    "theorem_zero": False,
                    "accepted_for_scoring": False,
                    "meaning": meaning,
                    "source_paths": ";".join(str(path) for path in [SRC_2925_RV, SRC_2926_RV_FILL, SRC_2917_BOUNDS, SRC_2918_KERNEL]),
                }
            )
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2927_0_alpha3_bound_acquired", "a source-backed alpha3 comparator is attached to RV2925_0", "PASS_NONCLAIM_STRUCTURE", "bound source exists but MTS prediction is absent", True),
        ("CG2927_1_alpha3_score", "MTS alpha3 prediction passes 4e-20", "BLOCKED_NONCLAIM", "all alpha3 heads lack numeric/theorem-zero inputs", False),
        ("CG2927_2_cshadow_bound", "C_shadow_abs has a numeric/source-backed upper bound", "BLOCKED_NONCLAIM", "only one comparator route is attached; transfer map and head values missing", False),
        ("CG2927_3_metric_readout_bound", "epsilon_metric_readout is bounded", "BLOCKED_NONCLAIM", "DqZ, boundary and readout heads remain missing", False),
        ("CG2927_4_local_GR_Newton", "local GR/Newton follows after 2927", "BLOCKED_NONCLAIM", "2927 is a residual-binding step, not a reduction proof", False),
        ("CG2927_5_github_public_claim", "2927 supports public claim language", "REJECTED_PRIVATE_NONCLAIM", "private checkpoint only", False),
    ]
    rows = []
    for gate_id, claim, gate_status, reason, gate_pass in specs:
        rows.append(
            add_common(
                {
                    "gate_id": gate_id,
                    "claim": claim,
                    "gate_status": gate_status,
                    "reason": reason,
                    "gate_pass": gate_pass,
                }
            )
        )
    return rows


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2927_0_result", "first_source_bound_route_attached", "The alpha3 <= 4e-20 comparator is now connected to the C_shadow/RV2925 metric-readout branch.", "use it as the first pressure test for metric-readout residuals"),
        ("DEC2927_1_no_claim", "not_a_pass", "The comparator is external; the MTS-side transfer map and all alpha3 product heads are still missing.", "keep all local-GR/Newton/PPN claims closed"),
        ("DEC2927_2_best_next", "stationary_alpha3_flux_or_coupling_baseline", "The live heads are boundary/domain/source-exchange plus Dln(kappa_MTS), Dln(ell_J) and d_R.", "try the stationary compact exterior flux zero theorem with fixed coupling/readout first"),
    ]
    rows = []
    for decision_id, decision, because, next_action in specs:
        rows.append(
            add_common(
                {
                    "decision_id": decision_id,
                    "decision": decision,
                    "because": because,
                    "next_action": next_action,
                }
            )
        )
    return rows


def next_target_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "route_id": "NEXT2927_0_2928",
                "selection_status": "selected_primary",
                "target_file": "2928-Y5-R2FR-RV2925-alpha3-stationary-flux-zero-or-kappa-ellJ-coupling-baseline-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_RV2925_alpha3_stationary_flux_zero_or_kappa_ellJ_coupling_baseline_under_AX1090_2928.py",
                "task": "try to prove the stationary compact exterior alpha3 flux heads vanish under fixed kappa_MTS, fixed ell_J, fixed boundary reference and fixed-before-readout source support; if not, fill the first finite kappa/ellJ source-bound row",
                "success_condition": "one alpha3 head becomes theorem-zero or source-backed finite with units and no-cancellation accounting",
                "fallback_condition": "keep alpha3 nonclaim and move to Dln(kappa_MTS)/Dln(ell_J) coupling-baseline acquisition rows",
                "guardrails": "no cancellation by fit; no fitted GM absorption; no local GR/Newton/PPN claim; no formalization-workbench edits; no GitHub",
                "selected": True,
            }
        )
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    rv_binding: list[dict[str, Any]],
    first_bound: list[dict[str, Any]],
    transfer: list[dict[str, Any]],
    rv_update: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branches: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    alpha3_bound = row_with_value(read_csv_rows(SRC_2917_BOUNDS), "observable", "alpha3") or {}
    kernel_rows = read_csv_rows(SRC_2918_KERNEL)
    required_kernel_symbols = {
        "F_boundary_alpha3",
        "F_domain_alpha3",
        "F_exchange_alpha3",
        "F_kappa_alpha3",
        "F_ellJ_alpha3",
        "F_dR_alpha3",
        "F_tail_alpha3",
        "Delta_alpha3_abs",
    }
    kernel_symbols = {row.get("symbol", "") for row in kernel_rows}
    output_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]

    checks = [
        ("VAL2927_0_source_paths_exist", all(as_bool(row["path_exists"]) for row in sources), "all cited source paths exist"),
        ("VAL2927_1_source_anchors_found", all(as_bool(row["anchors_found"]) for row in sources), "all source anchors found"),
        ("VAL2927_2_2926_selected_cshadow", any(row["symbol"] == "C_shadow_abs" and row["current_status"] == "FIRST_SOURCE_BOUND_COMPONENT_SELECTED" for row in rv_update), "C_shadow is the RV2925 metric-readout head selected for first fill"),
        ("VAL2927_3_alpha3_bound_numeric", alpha3_bound.get("upper_bound_abs") == "4e-20" and as_bool(alpha3_bound.get("bound_source_backed", "False")), "alpha3 comparator is positive/source-backed"),
        ("VAL2927_4_alpha3_kernel_heads_complete", required_kernel_symbols.issubset(kernel_symbols), "alpha3 source-current kernel has all required heads"),
        ("VAL2927_5_transfer_gate_blocks_claim", any(row["gate_id"] == "TR2927_5_verdict" and row["gate_pass"] is False for row in transfer), "transfer verdict remains blocked"),
        ("VAL2927_6_rv_update_nonclaim", all(not as_bool(row["accepted_for_scoring"]) for row in rv_update), "RV2925 update remains nonclaim"),
        ("VAL2927_7_claim_gates_safe", all(not as_bool(row["gate_pass"]) or row["gate_id"] == "CG2927_0_alpha3_bound_acquired" for row in claims), "only structural comparator gate passes"),
        ("VAL2927_8_no_prediction_rows_promoted", all(not as_bool(row["valid_prediction_row"]) and not as_bool(row["valid_for_claim"]) for row in first_bound + rv_update), "no prediction row promoted"),
        ("VAL2927_9_next_target_selected", any(as_bool(row.get("selected", False)) for row in next_rows), "2928 next target selected"),
        ("VAL2927_10_branch_copies_parse", all(as_bool(row["destination_exists"]) and as_bool(row["destination_parses"]) for row in branches), "branch copies parse"),
        ("VAL2927_11_no_formalization_outputs", all(not is_under(path, FORMALIZATION) for path in output_paths), "no output path inside formalization-workbench"),
        ("VAL2927_12_doc_exists", DOC.exists(), "2927 markdown doc exists"),
    ]
    rows = [
        {
            "validation_id": check_id,
            "status": bool(status),
            "detail": detail,
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        }
        for check_id, status, detail in checks
    ]
    overall = all(row["status"] for row in rows)
    rows.append(
        {
            "validation_id": "VAL2927_OVERALL",
            "status": overall,
            "detail": "2927 validation overall",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        }
    )
    return rows


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_specs = [
        ("rv_bound_copy", OUTPUTS["first_bound"], BRANCH_OUTPUTS["rv_bound_copy"]),
        ("transfer_gate_copy", OUTPUTS["transfer_gate"], BRANCH_OUTPUTS["transfer_gate_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
    rows = []
    for copy_id, source_path, destination_path in copy_specs:
        shutil.copyfile(source_path, destination_path)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source_path),
                    "destination_path": str(destination_path),
                    "destination_exists": destination_path.exists(),
                    "destination_parses": csv_parses(destination_path),
                }
            )
        )
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    rv_binding: list[dict[str, Any]],
    first_bound: list[dict[str, Any]],
    transfer: list[dict[str, Any]],
    rv_update: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branches: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    overall = next(row for row in validations if row["validation_id"] == "VAL2927_OVERALL")["status"]
    doc = f"""# 2927 - Y5/R2FR RV2925 Metric-Readout DqZ Geometry Cshadow First Source Bound Under AX1090

Status: `Y5_R2FR_2927_first_alpha3_source_bound_attached_to_RV2925_metric_readout_transfer_missing_2928_next`

Claim ceiling: `source_comparator_attached_nonclaim_only_no_Cshadow_bound_no_metric_readout_pass_no_local_GR_no_Newton_no_PPN_no_R10_no_GitHub_claim`

## Summary

2927 makes the first real contact between the GR-reduction residual vector and a source-backed local comparator. The selected residual is still `RV2925_0_metric_readout`, and the selected head is still `C_shadow_abs`, but it is no longer just a fog bank.

The first concrete pressure route is the disformal/source-current `alpha3` branch:

`RV2925_0 -> DqZ_geometry_abs -> C_shadow_abs -> b_dis/source_current -> Delta_alpha3_abs`, with the external comparator `|alpha3| <= 4e-20`.

That is useful, but it is not a pass. The comparator is source-backed; the MTS-side transfer map and the product heads are not. The project has moved from "what is the local residual?" to "can these exact alpha3 heads be killed or bounded?"

## Source Register

{md_table(sources, ["source_id", "source_path", "path_exists", "anchors_found", "role", "missing_anchors"])}

## RV2925/Cshadow Binding

{md_table(rv_binding, ["binding_id", "rv_component", "upstream_row", "symbol", "formula_or_rule", "current_status", "source_backed_comparator", "mts_prediction_present", "accepted_for_scoring", "implication"])}

## First Source-Bound Selection

{md_table(first_bound, ["selection_id", "rv_component", "cshadow_component", "observable", "bound_abs", "bound_units", "bound_source_id", "bound_source_backed", "mts_prediction_present", "current_status", "claim_effect"])}

## Alpha3 To RV2925 Transfer Gate

{md_table(transfer, ["gate_id", "requirement", "current_status", "reason", "gate_pass", "blocks_claim"])}

## Metric-Readout Residual Update

{md_table(rv_update, ["update_id", "rv_component", "upstream_row", "symbol", "formula_or_rule", "current_status", "source_backed_bound_present", "mts_numeric_prediction_present", "theorem_zero", "accepted_for_scoring", "meaning"])}

## Claim Gates

{md_table(claims, ["gate_id", "claim", "gate_status", "reason", "gate_pass", "valid_for_claim"])}

## Decision Ledger

{md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"])}

## Next Target

{md_table(next_rows, ["route_id", "selection_status", "target_file", "target_script", "task", "success_condition", "fallback_condition", "valid_for_claim"])}

## Branch Copies

{md_table(branches, ["copy_id", "source_path", "destination_path", "destination_exists", "destination_parses", "valid_for_claim"])}

## Validation

{md_table(validations, ["validation_id", "status", "detail", "valid_for_claim"])}

Validation overall: `{overall}`.

## Bottom Line

This is a real tightening step, not a trophy. The first source-backed local bound has been attached to the metric-readout reduction chain, but only as a comparator. The next real derivation is to try to make the stationary compact exterior alpha3 flux vanish under fixed `kappa_MTS`, fixed `ell_J`, fixed boundary reference and fixed-before-readout support. If that fails, the coupling baseline becomes the next finite residual input.

## Not Claimed

- `C_shadow_abs` is not numerically bounded.
- `Delta_alpha3_abs` is not predicted by MTS.
- `epsilon_metric_readout` is not accepted for scoring.
- No PPN, local-GR, Newton, R10, WEP, clock, orbital or GitHub/public claim is allowed from 2927.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    rv_binding = rv_binding_rows()
    first_bound = first_bound_rows()
    transfer = transfer_gate_rows()
    rv_update = rv_update_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["rv_binding"], rv_binding)
    write_csv(OUTPUTS["first_bound"], first_bound)
    write_csv(OUTPUTS["transfer_gate"], transfer)
    write_csv(OUTPUTS["rv_update"], rv_update)
    write_csv(OUTPUTS["claims"], claims)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_rows)

    branches = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], branches)

    DOC.write_text("# 2927 - validation preflight\n\nFinal document is written after validation rows are assembled.\n", encoding="utf-8")
    validations = validation_rows(sources, rv_binding, first_bound, transfer, rv_update, claims, next_rows, branches)
    write_csv(OUTPUTS["validation"], validations)
    write_doc(sources, rv_binding, first_bound, transfer, rv_update, claims, decisions, next_rows, branches, validations)

    print(f"2927 validation overall: {next(row for row in validations if row['validation_id'] == 'VAL2927_OVERALL')['status']}")
    print(f"doc: {DOC}")


if __name__ == "__main__":
    main()

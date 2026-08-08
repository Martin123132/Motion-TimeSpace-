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

CHECKPOINT = "2919"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2919-Y5-R2FR-stationary-alpha3-flux-zero-theorem-or-beta-source-normalization-kernel-under-AX1090.md"

SRC_2918_DOC = ROOT / "2918-Y5-R2FR-alpha3-source-current-kernel-or-no-disformal-slot-theorem-under-AX1090.md"
SRC_2918_NEXT = RESIDUALS / "P8_Y5_R2FR_2918_NEXT_TARGET.csv"
SRC_2918_KERNEL = RESIDUALS / "P8_Y5_R2FR_2918_ALPHA3_SOURCE_CURRENT_KERNEL.csv"
SRC_2918_PRODUCTS = RESIDUALS / "P8_Y5_R2FR_2918_ALPHA3_PRODUCT_BOUND_ROWS.csv"
SRC_2918_COUPLING = RESIDUALS / "P8_Y5_R2FR_2918_COUPLING_OWNER_GATES.csv"
SRC_STATIONARY_2468_HYP = RESIDUALS / "P8_Y5_STATIONARY_SOURCE_2468_THEOREM_HYPOTHESES.csv"
SRC_STATIONARY_2468_PROOF = RESIDUALS / "P8_Y5_STATIONARY_SOURCE_2468_PROOF_STEPS.csv"
SRC_STATIONARY_2468_RESULT = RESIDUALS / "P8_Y5_STATIONARY_SOURCE_2468_EXTERIOR_QLOC_RESULT.csv"
SRC_STATIONARY_2468_VERDICT = RESIDUALS / "P8_Y5_STATIONARY_SOURCE_2468_PROMOTION_VERDICT.csv"
SRC_STATIONARY_2558_HYP = RESIDUALS / "P8_Y5_NO_SHADOW_2558_STATIONARY_THEOREM_HYPOTHESES.csv"
SRC_STATIONARY_2558_PROOF = RESIDUALS / "P8_Y5_NO_SHADOW_2558_STATIONARY_PROOF_STEPS.csv"
SRC_STATIONARY_2558_RESULT = RESIDUALS / "P8_Y5_NO_SHADOW_2558_EXTERIOR_QLOC_RESULT.csv"
SRC_ROOT_LAW_2735 = RESIDUALS / "P8_Y5_R2FR_2735_STATIONARY_SOURCE_ROOT_LAW.csv"
SRC_VARIATION_2908 = RESIDUALS / "P8_Y5_R2FR_2908_VARIATION_AND_QLOC_DERIVATION.csv"
SRC_SELECTOR_BOUNDARY_2577 = RESIDUALS / "P8_Y5_SOURCE_SELECTOR_COUPLING_2577_BOUNDARY_ZERO_COUPLING_AUDIT.csv"
SRC_SELECTOR_LEDGER_2577 = RESIDUALS / "P8_Y5_SOURCE_SELECTOR_COUPLING_2577_RESIDUAL_INPUT_LEDGER.csv"
SRC_NOETHER_2615 = RESIDUALS / "P8_Y5_TOTAL_HILBERT_SOURCE_GATE_2615_NOETHER_EXCHANGE_COLLAPSE_THEOREM.csv"
SRC_DELTAW_2615 = RESIDUALS / "P8_Y5_TOTAL_HILBERT_SOURCE_GATE_2615_DELTAW_BLOCK_BOUND_INPUT.csv"
SRC_BETA_2574 = RESIDUALS / "P8_Y5_PPN_VECTOR_2574_BETA_SECOND_ORDER_COUPLING_GATE.csv"
SRC_BETA_LAW_2893 = RESIDUALS / "P8_Y5_R2FR_2893_BETA_SOURCE_NORMALIZED_COEFFICIENT_LAW.csv"
SRC_BETA_VECTOR_2893 = RESIDUALS / "P8_Y5_R2FR_2893_FINITE_BETA_VECTOR_ROW_NONCLAIM.csv"
SRC_BETA_ENV_2896 = RESIDUALS / "P8_Y5_R2FR_2896_BETA_ENVELOPE_COMPONENTS.csv"
SRC_NEWTON_GATE_2896 = RESIDUALS / "P8_Y5_R2FR_2896_SOURCE_NORMALIZED_NEWTON_PRECONDITION_GATE.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2919_SOURCE_REGISTER.csv",
    "flux_audit": RESIDUALS / "P8_Y5_R2FR_2919_STATIONARY_ALPHA3_FLUX_ZERO_AUDIT.csv",
    "head_reduction": RESIDUALS / "P8_Y5_R2FR_2919_ALPHA3_HEAD_REDUCTION_LEDGER.csv",
    "beta_fallback": RESIDUALS / "P8_Y5_R2FR_2919_BETA_SOURCE_NORMALIZATION_FALLBACK_KERNEL.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2919_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2919_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2919_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2919_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2919_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "flux_copy": PARENT_ACTION / "Stationary_alpha3_flux_zero_audit_2919_NONCLAIM.csv",
    "beta_copy": LOCAL_BOUNDS / "Beta_source_normalization_fallback_kernel_2919_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2919_BETA_SOURCE_NORMALIZATION_SECOND_ORDER_KERNEL_NEXT_NONCLAIM.csv",
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


def csv_parses(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


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


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2919_00_2918_doc", SRC_2918_DOC, "Delta_alpha3_abs;stationary compact exterior flux theorem", "2918 alpha3 kernel handoff"),
        ("SRC2919_01_2918_next", SRC_2918_NEXT, "NEXT2918_0_2919;stationary compact exterior alpha3", "machine-readable 2919 target"),
        ("SRC2919_02_2918_kernel", SRC_2918_KERNEL, "A3K2918_8_total_abs;A3K2918_9_verdict", "2918 alpha3 source-current heads"),
        ("SRC2919_03_2918_products", SRC_2918_PRODUCTS, "A3P2918_0_boundary;A3P2918_6_total", "2918 alpha3 product lock"),
        ("SRC2919_04_2918_coupling", SRC_2918_COUPLING, "COUP2918_7_verdict;COUPLING_OWNER_GATES_FAIL_CURRENT_MTS", "2918 coupling owner gates"),
        ("SRC2919_05_2468_hyp", SRC_STATIONARY_2468_HYP, "HYP2468_2_parent_scale_fixed;HYP2468_7_boundary_silent", "earlier stationary theorem hypotheses"),
        ("SRC2919_06_2468_proof", SRC_STATIONARY_2468_PROOF, "PRF2468_4_projected_q_zero;PRF2468_6_not_full_GR", "earlier stationary q_loc proof"),
        ("SRC2919_07_2468_result", SRC_STATIONARY_2468_RESULT, "EXT2468_0_stationary_q_zero;EXT2468_4_claim_limit", "earlier stationary result"),
        ("SRC2919_08_2468_verdict", SRC_STATIONARY_2468_VERDICT, "PV2468_0_stationary_theorem;PV2468_3_overall", "earlier promotion verdict"),
        ("SRC2919_09_2558_hyp", SRC_STATIONARY_2558_HYP, "HYP2558_7_boundary_silent;HYP2558_8_stress_not_claimed", "later stationary no-shadow hypotheses"),
        ("SRC2919_10_2558_proof", SRC_STATIONARY_2558_PROOF, "PRF2558_4_projected_q_zero;PRF2558_7_not_full_GR", "later stationary no-shadow proof"),
        ("SRC2919_11_2558_result", SRC_STATIONARY_2558_RESULT, "EXT2558_0_stationary_q_zero;EXT2558_5_metric_limit", "later stationary no-shadow result"),
        ("SRC2919_12_2735_root", SRC_ROOT_LAW_2735, "SSR2735_2_double_zero;SSR2735_4_verdict", "stationary source-root law"),
        ("SRC2919_13_2908_variation", SRC_VARIATION_2908, "VAR2908_0_delta_A_q_loc;VAR2908_6_boundary_worldtube;VAR2908_7_verdict", "variation/q_loc derivation and open boundary flux"),
        ("SRC2919_14_2577_boundary", SRC_SELECTOR_BOUNDARY_2577, "BZA2577_5_zero_flux_verdict;ZERO_BOUNDARY_FLUX_WITH_COUPLING_NOT_DERIVED", "boundary flux with coupling audit"),
        ("SRC2919_15_2577_residuals", SRC_SELECTOR_LEDGER_2577, "SRR2577_5_delta_kappa;SRR2577_6_delta_ellJ", "kappa/ellJ residual rows"),
        ("SRC2919_16_2615_noether", SRC_NOETHER_2615, "NEC2615_2_weight_collapse;NEC2615_5_current_verdict", "Noether exchange collapse"),
        ("SRC2919_17_2615_deltaw", SRC_DELTAW_2615, "DWB2615_0_delta_w_block;DWB2615_6_nonclaim_lock", "delta_w block residual"),
        ("SRC2919_18_2574_beta", SRC_BETA_2574, "BETA2574_2_source_coupling;BETA2574_4_verdict", "beta source-coupling fallback"),
        ("SRC2919_19_2893_beta_law", SRC_BETA_LAW_2893, "BSL2893_2_extract_beta;BSL2893_5_no_smuggling", "beta source-normalized coefficient law"),
        ("SRC2919_20_2893_beta_vector", SRC_BETA_VECTOR_2893, "FBR2893_0_delta_beta_source;FBR2893_6_Delta_beta_total_abs", "finite beta vector row"),
        ("SRC2919_21_2896_beta_env", SRC_BETA_ENV_2896, "ENV2896_0_Newton_precondition;ENV2896_7_q_loc_alpha3_guard", "beta envelope components"),
        ("SRC2919_22_2896_newton_gate", SRC_NEWTON_GATE_2896, "NG2896_5_precondition_verdict;FAIL_CLOSED", "source-normalized Newton precondition"),
    ]
    rows = []
    for source_id, path, anchors, role in specs:
        ok, missing = anchors_present(path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": path.exists(),
                    "anchors_found": ok,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def flux_audit_rows() -> list[dict[str, Any]]:
    specs = [
        ("SFA2919_0_stationary_hilbert_current", "stationary compact Hilbert-source exterior gives J_M=0 and q_loc=0", "PASS_CONDITIONAL_QLOC_HEAD_ONLY", "kills the pure Hilbert-current exterior q_loc head under HYP2468/HYP2558 hypotheses", True),
        ("SFA2919_1_alpha3_projection", "alpha3 is a spatial momentum/source-current projection of the retained residual vector", "DEFINITION_READY_NONCLAIM", "requires all alpha3 heads, not only q_loc, to vanish or be bounded", False),
        ("SFA2919_2_boundary_flux", "boundary/worldtube compact flux has no alpha3 spatial momentum projection", "MISSING_BOUNDARY_FLUX_ZERO_WITH_COUPLING", "B_zero_flux and K_boundary heads remain open", False),
        ("SFA2919_3_domain_projector", "domain/projector sector has no alpha3 momentum or preferred-frame leakage", "MISSING_DOMAIN_PROJECTOR_NOLEAK", "domain alpha3 and R11 projector rows remain open", False),
        ("SFA2919_4_source_exchange", "Noether exchange graph is one connected ordinary source block and no source-shadow current exists", "MISSING_EXCHANGE_CONNECTIVITY_AND_SOURCE_SHADOW_BAN", "delta_w_block/A_source_shadow/q_nonH remain active", False),
        ("SFA2919_5_kappa", "Dln(kappa_MTS)=0 on the local exterior comparison branch", "MISSING_PARENT_CONSTANT_KAPPA_PROOF_OR_VALUE", "coupling baseline can feed alpha3 and beta", False),
        ("SFA2919_6_ellJ", "Dln(ell_J)=0 on the local Hilbert-source current", "MISSING_PARENT_CONSTANT_ELLJ_PROOF_OR_VALUE", "source-current scale can feed alpha3 and beta", False),
        ("SFA2919_7_disformal_vector", "no disformal/preferred-vector current survives", "MISSING_NO_DISFORMAL_SLOT_OR_D_R_VALUE", "d_R/vector alpha3 head remains active", False),
        ("SFA2919_8_readout", "fixed-before-readout and fixed-GM transfer cannot absorb alpha3 heads", "MISSING_FIXED_BEFORE_READOUT_TRANSFER", "calibration/readout tail remains active", False),
        ("SFA2919_9_verdict", "stationary alpha3 flux-zero theorem for current MTS", "STATIONARY_ALPHA3_ZERO_FAILS_CURRENT_MTS_PARTIAL_QLOC_WIN_ONLY", "stationarity kills one head conditionally, not total alpha3", False),
    ]
    return [
        add_common(
            {
                "audit_id": audit_id,
                "condition": condition,
                "current_status": status,
                "effect": effect,
                "condition_passed": passed,
                "source_paths": f"{SRC_STATIONARY_2468_RESULT};{SRC_STATIONARY_2558_RESULT};{SRC_2918_KERNEL};{SRC_VARIATION_2908}",
            }
        )
        for audit_id, condition, status, effect, passed in specs
    ]


def head_reduction_rows() -> list[dict[str, Any]]:
    specs = [
        ("A3H2919_0_q_loc_hilbert", "q_loc_Hilbert_exterior", "conditional_zero", "stationary compact exterior gives J_M=0 -> q_loc=0", "PASS_CONDITIONAL_NOT_CLAIM", "not a total alpha3 pass"),
        ("A3H2919_1_boundary", "F_boundary_alpha3", "retained", "lim_S r^2 n_mu P_alpha3_nu K_boundary^{mu nu}", "MISSING_BOUNDARY_NOFLUX_THEOREM_OR_PRODUCT", "must prove zero or score product against 4e-20"),
        ("A3H2919_2_domain", "F_domain_alpha3", "retained", "lim_S r^2 n_mu P_alpha3_nu K_domain/projector^{mu nu}", "MISSING_DOMAIN_NOLEAK_THEOREM_OR_PRODUCT", "must prove no domain vector/projector leak or score product"),
        ("A3H2919_3_exchange", "F_exchange_alpha3", "retained", "Pi_alpha3[sum_C delta_w_C nabla_mu T_C^{mu nu}+source_shadow^nu]", "MISSING_EXCHANGE_GRAPH_CONNECTIVITY_OR_BOUND", "Noether collapse only conditional"),
        ("A3H2919_4_kappa", "F_kappa_alpha3", "retained", "K_alpha3_kappa Dln(kappa_MTS)", "MISSING_CONSTANT_KAPPA_PROOF_OR_VALUE", "coupling baseline still live"),
        ("A3H2919_5_ellJ", "F_ellJ_alpha3", "retained", "K_alpha3_ellJ Dln(ell_J)", "MISSING_CONSTANT_ELLJ_PROOF_OR_VALUE", "source-current scale still live"),
        ("A3H2919_6_dR", "F_dR_alpha3", "retained", "K_alpha3_dR d_R", "MISSING_NO_DISFORMAL_SLOT_OR_D_R_VALUE", "preferred-vector branch still live"),
        ("A3H2919_7_tail", "F_tail_alpha3", "retained", "endpoint/domain/readout tails", "MISSING_ENDPOINT_DOMAIN_READOUT_KERNELS", "not killed by stationary source proof"),
        ("A3H2919_8_total", "Delta_alpha3_abs", "retained_nonclaim", "sum_abs(active heads)", "TOTAL_ALPHA3_NOT_SCORE_READY", "no cancellation credit"),
    ]
    return [
        add_common(
            {
                "head_id": head_id,
                "symbol": symbol,
                "reduction_result": result,
                "formula_or_reason": formula,
                "current_status": status,
                "next_requirement": next_requirement,
                "target_bound_abs": "4e-20",
                "source_paths": f"{SRC_2918_KERNEL};{SRC_2918_PRODUCTS};{SRC_STATIONARY_2468_RESULT};{SRC_STATIONARY_2558_RESULT}",
                "head_zero_adopted": result == "conditional_zero",
                "score_input_present": False,
            }
        )
        for head_id, symbol, result, formula, status, next_requirement in specs
    ]


def beta_fallback_rows() -> list[dict[str, Any]]:
    specs = [
        ("BFB2919_0_beta_law", "beta_eff", "beta_eff = B_source/A_source^2", "DERIVED_KINEMATIC_LAW_FROM_2893", "needs A_source and B_source from parent/source-normalized field equation"),
        ("BFB2919_1_source_residual", "delta_beta_source", "B_source/A_source^2 - 1", "MISSING_A_SOURCE_B_SOURCE_OR_SQUARE_THEOREM", "next concrete beta source-normalization target"),
        ("BFB2919_2_Newton_precondition", "source_normalized_Newton_precondition", "measured_mu=G0*M_H with zero charge/current/source/range/time/frame/domain residuals", "FAIL_CLOSED_FROM_2896", "must close before beta/local-GR pass"),
        ("BFB2919_3_R11_operator", "delta_beta_operator", "second-order non-EH/R11 operator contribution", "MISSING_R11_COMPONENT_VALUES_OR_EH_NOHAIR", "cannot infer from gamma or stationary qloc"),
        ("BFB2919_4_boundary_domain", "delta_beta_boundary_domain", "boundary/domain/projector quadratic stress beta projection", "MISSING_BOUNDARY_DOMAIN_ZERO_OR_COEFFICIENT_MAP", "same source-current wound as alpha3 but through beta"),
        ("BFB2919_5_readout", "delta_beta_readout", "second-order observed U/readout/gauge mismatch", "MISSING_SAME_READOUT_THEOREM_THROUGH_O_U2", "fixed-before-readout still required"),
        ("BFB2919_6_epsilon_SN", "epsilon_SN", "(mu_obs-G_eff M_H)/(G_eff M_H)", "MISSING_GAUSS_ORBITAL_SOURCE_CURRENT_SCORECARD", "measured-GM cannot absorb source residuals"),
        ("BFB2919_7_total", "Delta_beta_total_abs", "sum_abs(beta active heads)", "BETA_SOURCE_NORMALIZATION_KERNEL_SELECTED_NONCLAIM", "2919 fallback target; no beta score"),
    ]
    return [
        add_common(
            {
                "fallback_id": fallback_id,
                "symbol": symbol,
                "formula_or_map": formula,
                "current_status": status,
                "next_requirement": next_requirement,
                "beta_bound_abs": "7.8e-05",
                "source_paths": f"{SRC_BETA_2574};{SRC_BETA_LAW_2893};{SRC_BETA_VECTOR_2893};{SRC_BETA_ENV_2896};{SRC_NEWTON_GATE_2896}",
                "promotion_allowed_now": False,
            }
        )
        for fallback_id, symbol, formula, status, next_requirement in specs
    ]


def claim_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2919_0_q_loc_stationary", "stationary q_loc exterior is conditionally zero", "PARTIAL_CONDITIONAL_NONCLAIM", "useful theorem contract but hypotheses are not parent-signed", False),
        ("CG2919_1_alpha3_zero", "stationary alpha3 flux vanishes", "BLOCKED_NONCLAIM", "boundary/domain/exchange/coupling/disformal/readout heads remain open", False),
        ("CG2919_2_alpha3_score", "alpha3 passes 4e-20 bound", "BLOCKED_NONCLAIM", "no product head has numeric/theorem-zero input", False),
        ("CG2919_3_beta_fallback", "beta/source-normalization is score-ready", "BLOCKED_NONCLAIM", "fallback kernel only; source coefficients missing", False),
        ("CG2919_4_local_GR_Newton", "local GR/Newton follows from stationary proof", "BLOCKED_NONCLAIM", "stationary proof kills one q_loc head only", False),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "claim": claim,
                "gate_status": status,
                "reason": reason,
                "gate_pass": gate_pass,
            }
        )
        for gate_id, claim, status, reason, gate_pass in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2919_0_gain", "stationary_q_loc_head_is_real_partial_win", "The existing stationary proof can be imported for the Hilbert-current/q_loc exterior head.", "carry as conditional theorem contract"),
        ("DEC2919_1_fail", "stationary_alpha3_zero_not_proved", "alpha3 is stricter than q_loc: boundary/domain/source-exchange/coupling/disformal/readout momentum heads survive.", "keep alpha3 nonclaim"),
        ("DEC2919_2_no_smuggling", "no_total_alpha3_cancellation_or_fitted_GM", "The alpha3 and beta rows both forbid cancellation/readout absorption unless parent identity signs it before data.", "keep no-cancellation envelope"),
        ("DEC2919_3_next", "beta_source_normalization_second_order_is_next", "If alpha3 stationary flux cannot close, the next local-GR gate is beta: B_source/A_source^2-1 and source-normalized Newton precondition.", "select 2920 beta/source-normalization kernel"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": next_action,
            }
        )
        for decision_id, decision, because, next_action in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "route_id": "NEXT2919_0_2920",
                "selection_status": "selected_primary",
                "target_file": "2920-Y5-R2FR-beta-source-normalization-second-order-kernel-or-parent-square-law-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_beta_source_normalization_second_order_kernel_or_parent_square_law_under_AX1090_2920.py",
                "task": "derive B_source=A_source^2 from the parent source-normalized local field equation, or build the finite beta source-normalization component kernel with no measured-GM absorption",
                "success_condition": "parent square law proves beta_eff=1 in the same observed-U convention, or all beta heads have source-backed finite rows under the 7.8e-05 bound",
                "fallback_condition": "keep beta nonclaim and move to source-normalized Newton/Gauss/orbital scorecard acquisition",
                "guardrails": "no Schwarzschild/EH beta import as axiom; no fitted-GM absorption; no cancellation credit; no local GR/Newton/PPN claim; no formalization-workbench edits; no GitHub",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("flux_copy", OUTPUTS["flux_audit"], BRANCH_OUTPUTS["flux_copy"]),
        ("beta_copy", OUTPUTS["beta_fallback"], BRANCH_OUTPUTS["beta_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
    rows = []
    for copy_id, source, destination in specs:
        if source.exists():
            shutil.copyfile(source, destination)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source),
                    "destination_path": str(destination),
                    "source_exists": source.exists(),
                    "destination_exists": destination.exists(),
                    "destination_parses": csv_parses(destination) if destination.exists() else False,
                }
            )
        )
    return rows


def validation_rows(
    source_rows: list[dict[str, Any]],
    flux_rows: list[dict[str, Any]],
    head_rows: list[dict[str, Any]],
    beta_rows: list[dict[str, Any]],
    claim_rows_: list[dict[str, Any]],
    next_rows_: list[dict[str, Any]],
    branch_rows_: list[dict[str, Any]],
    include_doc_check: bool,
) -> list[dict[str, Any]]:
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_outputs_with_validation = [*csv_outputs, OUTPUTS["validation"]]
    flux_verdict = next(row for row in flux_rows if row["audit_id"] == "SFA2919_9_verdict")
    qloc_head = next(row for row in head_rows if row["head_id"] == "A3H2919_0_q_loc_hilbert")
    total_head = next(row for row in head_rows if row["head_id"] == "A3H2919_8_total")
    beta_total = next(row for row in beta_rows if row["fallback_id"] == "BFB2919_7_total")
    required_heads = {
        "q_loc_Hilbert_exterior",
        "F_boundary_alpha3",
        "F_domain_alpha3",
        "F_exchange_alpha3",
        "F_kappa_alpha3",
        "F_ellJ_alpha3",
        "F_dR_alpha3",
        "F_tail_alpha3",
        "Delta_alpha3_abs",
    }
    head_symbols = {str(row["symbol"]) for row in head_rows}
    required_beta = {
        "beta_eff",
        "delta_beta_source",
        "source_normalized_Newton_precondition",
        "delta_beta_operator",
        "delta_beta_boundary_domain",
        "delta_beta_readout",
        "epsilon_SN",
        "Delta_beta_total_abs",
    }
    beta_symbols = {str(row["symbol"]) for row in beta_rows}
    generated_paths = [*OUTPUTS.values(), *BRANCH_OUTPUTS.values(), DOC]
    checks = [
        ("VAL2919_0_source_paths_exist", all(bool(row["path_exists"]) for row in source_rows), "all cited source paths exist"),
        ("VAL2919_1_source_anchors_found", all(bool(row["anchors_found"]) for row in source_rows), "all source anchors found"),
        ("VAL2919_2_csv_outputs_parse", all(csv_parses(path) for path in csv_outputs_with_validation if path.exists()), "generated CSV outputs parse cleanly"),
        ("VAL2919_3_partial_q_loc_win", qloc_head["reduction_result"] == "conditional_zero" and qloc_head["head_zero_adopted"] is True, "stationary q_loc head retained as conditional zero"),
        ("VAL2919_4_alpha3_total_not_zero", flux_verdict["current_status"] == "STATIONARY_ALPHA3_ZERO_FAILS_CURRENT_MTS_PARTIAL_QLOC_WIN_ONLY" and total_head["current_status"] == "TOTAL_ALPHA3_NOT_SCORE_READY", "stationary alpha3 theorem correctly fails current corpus"),
        ("VAL2919_5_alpha3_heads_complete", required_heads.issubset(head_symbols), "all alpha3 heads accounted for"),
        ("VAL2919_6_beta_fallback_complete", required_beta.issubset(beta_symbols) and beta_total["current_status"] == "BETA_SOURCE_NORMALIZATION_KERNEL_SELECTED_NONCLAIM", "beta/source-normalization fallback kernel complete"),
        ("VAL2919_7_claim_gates_safe", all(not bool(row["claim_allowed"]) and not bool(row["valid_for_claim"]) and not bool(row["gate_pass"]) for row in claim_rows_), "no claim gate is open"),
        ("VAL2919_8_next_target_selected", next_rows_[0]["route_id"] == "NEXT2919_0_2920" and bool(next_rows_[0]["selected"]), "2920 beta/source-normalization target selected"),
        ("VAL2919_9_branch_copies_parse", all(bool(row["destination_exists"]) and bool(row["destination_parses"]) for row in branch_rows_), "branch copies exist and parse"),
        ("VAL2919_10_no_formalization_outputs", not any(is_under(path, FORMALIZATION) for path in generated_paths), "no generated output path is inside formalization-workbench"),
        ("VAL2919_11_doc_written", DOC.exists() if include_doc_check else True, "markdown checkpoint exists"),
    ]
    rows: list[dict[str, Any]] = [
        {
            "validation_id": validation_id,
            "status": bool(status),
            "detail": detail,
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        }
        for validation_id, status, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2919_OVERALL",
            "status": all(bool(row["status"]) for row in rows),
            "detail": "2919 validation overall",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        }
    )
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    flux_rows: list[dict[str, Any]],
    head_rows: list[dict[str, Any]],
    beta_rows: list[dict[str, Any]],
    claim_rows_: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    next_rows_: list[dict[str, Any]],
    branch_rows_: list[dict[str, Any]],
    validation_rows_: list[dict[str, Any]],
) -> None:
    overall = next(row for row in validation_rows_ if row["validation_id"] == "VAL2919_OVERALL")
    text = f"""# 2919 - Y5/R2FR Stationary Alpha3 Flux-Zero Theorem Or Beta Source-Normalization Kernel Under AX1090

Status: `Y5_R2FR_2919_stationary_q_loc_partial_win_alpha3_zero_fails_beta_source_normalization_2920_next`

Claim ceiling: `stationary_q_loc_conditional_only_no_alpha3_pass_no_beta_pass_no_local_GR_no_Newton_no_PPN_no_R10_no_GitHub_claim`

Generated UTC: `{RUN_UTC}`

## Summary

2919 tries the derivation route first. The stationary compact exterior theorem does give one real partial win:

`J_M=0 -> q_loc^nu=0` in the exterior collar, under fixed `ell_J`, Killing/stationary `tau`, compact source support, parent-owned `P_loc`, and silent boundary hypotheses.

But `alpha3` is stricter than `q_loc`. It is a preferred-frame spatial momentum/source-current projection. The stationary proof does not silence boundary flux, domain/projector flux, source-exchange blocks, `Dln(kappa_MTS)`, `Dln(ell_J)`, disformal/vector current, or endpoint/readout tails.

So the theorem is useful, but not enough:

`Delta_alpha3_abs = sum_abs(active heads)` remains nonclaim against the `4e-20` lock.

Because the alpha3 stationary route fails at the total-head level, the next best route is the beta/source-normalization second-order kernel:

`beta_eff = B_source/A_source^2`, so `delta_beta_source = B_source/A_source^2 - 1`.

That is the next place to try for a parent square law, without smuggling in Schwarzschild/EH beta as an axiom.

## Source Register

{md_table(source_rows, ["source_id", "source_path", "anchors_found", "role", "missing_anchors"])}

## Stationary Alpha3 Flux-Zero Audit

{md_table(flux_rows, ["audit_id", "condition", "current_status", "effect", "condition_passed", "valid_for_claim"])}

## Alpha3 Head Reduction Ledger

{md_table(head_rows, ["head_id", "symbol", "reduction_result", "formula_or_reason", "current_status", "next_requirement", "target_bound_abs", "valid_for_claim"])}

## Beta Source-Normalization Fallback Kernel

{md_table(beta_rows, ["fallback_id", "symbol", "formula_or_map", "current_status", "next_requirement", "beta_bound_abs", "valid_for_claim"])}

## Claim Gates

{md_table(claim_rows_, ["gate_id", "claim", "gate_status", "reason", "gate_pass", "valid_for_claim"])}

## Decision Ledger

{md_table(decision_rows_, ["decision_id", "decision", "because", "next_action", "valid_for_claim"])}

## Next Target

{md_table(next_rows_, ["route_id", "selection_status", "target_file", "target_script", "task", "success_condition", "fallback_condition", "valid_for_claim"])}

## Branch Copies

{md_table(branch_rows_, ["copy_id", "source_path", "destination_path", "destination_exists", "destination_parses", "valid_for_claim"])}

## Validation

{md_table(validation_rows_, ["validation_id", "status", "detail", "valid_for_claim"])}

Validation overall: `{overall["status"]}`.

## Interpretation

This is a good kind of failure. The stationary theorem does not solve local GR, but it does remove the pure exterior Hilbert-current head from the suspect list under clear conditions. The remaining obstruction is sharper: alpha3 is carried by boundary/domain/coupling/disformal/readout source-current heads, not by the simple stationary bulk source.

The next derivation should attack beta because beta asks whether the second-order source coefficient is the square of the first-order measured source coefficient. That is exactly the “does this reduce to GR rather than merely fit Newton?” question in a cleaner scalar equation.

## Not Claimed

- no total alpha3 zero theorem is claimed;
- no alpha3 `4e-20` pass is claimed;
- no beta/source-normalization pass is claimed;
- no `Dln(kappa_MTS)=0` or `Dln(ell_J)=0` theorem is claimed;
- no local-GR/Newton/PPN/R10/WEP/clock/orbital pass is claimed;
- no file in `formalization-workbench` is modified by this checkpoint;
- no public/GitHub action is implied.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    flux_rows = flux_audit_rows()
    head_rows = head_reduction_rows()
    beta_rows = beta_fallback_rows()
    claim_rows_ = claim_rows()
    decision_rows_ = decision_rows()
    next_rows_ = next_rows()

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["flux_audit"], flux_rows)
    write_csv(OUTPUTS["head_reduction"], head_rows)
    write_csv(OUTPUTS["beta_fallback"], beta_rows)
    write_csv(OUTPUTS["claims"], claim_rows_)
    write_csv(OUTPUTS["decision"], decision_rows_)
    write_csv(OUTPUTS["next"], next_rows_)

    branch_rows_ = branch_rows()
    write_csv(OUTPUTS["branches"], branch_rows_)

    validation_rows_ = validation_rows(
        source_rows,
        flux_rows,
        head_rows,
        beta_rows,
        claim_rows_,
        next_rows_,
        branch_rows_,
        include_doc_check=False,
    )
    write_csv(OUTPUTS["validation"], validation_rows_)
    write_doc(
        source_rows,
        flux_rows,
        head_rows,
        beta_rows,
        claim_rows_,
        decision_rows_,
        next_rows_,
        branch_rows_,
        validation_rows_,
    )

    validation_rows_ = validation_rows(
        source_rows,
        flux_rows,
        head_rows,
        beta_rows,
        claim_rows_,
        next_rows_,
        branch_rows_,
        include_doc_check=True,
    )
    write_csv(OUTPUTS["validation"], validation_rows_)
    write_doc(
        source_rows,
        flux_rows,
        head_rows,
        beta_rows,
        claim_rows_,
        decision_rows_,
        next_rows_,
        branch_rows_,
        validation_rows_,
    )

    overall = next(row for row in validation_rows_ if row["validation_id"] == "VAL2919_OVERALL")
    if not bool(overall["status"]):
        raise SystemExit(1)


if __name__ == "__main__":
    main()

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

CHECKPOINT = "2918"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2918-Y5-R2FR-alpha3-source-current-kernel-or-no-disformal-slot-theorem-under-AX1090.md"

SRC_2917_DOC = ROOT / "2917-Y5-R2FR-disformal-PPN-kernel-or-cg-source-leg-provenance-fill-under-AX1090.md"
SRC_2917_NEXT = RESIDUALS / "P8_Y5_R2FR_2917_NEXT_TARGET.csv"
SRC_2917_KERNEL = RESIDUALS / "P8_Y5_R2FR_2917_DISFORMAL_PPN_RESPONSE_KERNEL.csv"
SRC_2917_ZERO = RESIDUALS / "P8_Y5_R2FR_2917_DISFORMAL_ZERO_PROOF_AUDIT.csv"
SRC_2917_BOUNDS = RESIDUALS / "P8_Y5_R2FR_2917_PPN_BOUND_ANCHOR_BINDING.csv"
SRC_ALPHA3_INPUT = RESIDUALS / "P8_ALPHA3_BOUND_PRODUCT_INPUT.csv"
SRC_ALPHA3_EVAL = RESIDUALS / "P8_ALPHA3_BOUND_PRODUCT_EVALUATION.csv"
SRC_ALPHA3_GATE = RESIDUALS / "P8_ALPHA3_THEOREM_ZERO_GATE.csv"
SRC_ALPHA3_TOTAL = RESIDUALS / "P8_ALPHA3_TOTAL_GUARD.csv"
SRC_ALPHA3_DECISION = RESIDUALS / "P8_ALPHA3_BOUND_DECISION.csv"
SRC_MU_ZERO = RESIDUALS / "P8_MU_EXTRA_ALPHA3_ZERO_ATTEMPT.csv"
SRC_MU_SKELETON = RESIDUALS / "P8_MU_EXTRA_ALPHA3_FILL_INPUT_SKELETON.csv"
SRC_MU_PRESSURE = RESIDUALS / "P8_MU_EXTRA_HIGHEST_PRESSURE_R7_ALPHA3_GATE.csv"
SRC_BOUNDARY_ATTEMPT = RESIDUALS / "P8_BOUNDARY_ALPHA3_NOFLUX_THEOREM_ATTEMPT.csv"
SRC_BOUNDARY_OWNER = RESIDUALS / "P8_BOUNDARY_ALPHA3_PREMISE_OWNERSHIP.csv"
SRC_DOMAIN_ATTEMPT = RESIDUALS / "P8_DOMAIN_ALPHA3_NOLEAK_THEOREM_ATTEMPT.csv"
SRC_DOMAIN_OWNER = RESIDUALS / "P8_DOMAIN_ALPHA3_PREMISE_OWNERSHIP.csv"
SRC_SELECTOR_LEDGER = RESIDUALS / "P8_Y5_SOURCE_SELECTOR_COUPLING_2577_RESIDUAL_INPUT_LEDGER.csv"
SRC_SELECTOR_THEOREM = RESIDUALS / "P8_Y5_SOURCE_SELECTOR_COUPLING_2577_WORLDTUBE_HILBERT_COUPLING_SELECTOR_THEOREM.csv"
SRC_SELECTOR_BOUNDARY = RESIDUALS / "P8_Y5_SOURCE_SELECTOR_COUPLING_2577_BOUNDARY_ZERO_COUPLING_AUDIT.csv"
SRC_HILBERT_AUDIT = RESIDUALS / "P8_Y5_TOTAL_HILBERT_SOURCE_GATE_2615_TOTAL_HILBERT_SOURCE_OWNER_AUDIT.csv"
SRC_NOETHER = RESIDUALS / "P8_Y5_TOTAL_HILBERT_SOURCE_GATE_2615_NOETHER_EXCHANGE_COLLAPSE_THEOREM.csv"
SRC_DELTAW = RESIDUALS / "P8_Y5_TOTAL_HILBERT_SOURCE_GATE_2615_DELTAW_BLOCK_BOUND_INPUT.csv"
SRC_ROLL_FRONTIER = RESIDUALS / "P8_Y5_SOURCE_PREF_GR_ROLLFORWARD_2632_LOCAL_GR_FRONTIER_MATRIX.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2918_SOURCE_REGISTER.csv",
    "no_disformal": RESIDUALS / "P8_Y5_R2FR_2918_NO_DISFORMAL_SLOT_THEOREM_AUDIT.csv",
    "kernel": RESIDUALS / "P8_Y5_R2FR_2918_ALPHA3_SOURCE_CURRENT_KERNEL.csv",
    "products": RESIDUALS / "P8_Y5_R2FR_2918_ALPHA3_PRODUCT_BOUND_ROWS.csv",
    "coupling": RESIDUALS / "P8_Y5_R2FR_2918_COUPLING_OWNER_GATES.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2918_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2918_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2918_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2918_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2918_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "no_disformal_copy": PARENT_ACTION / "No_disformal_slot_alpha3_source_current_2918_NONCLAIM.csv",
    "kernel_copy": LOCAL_BOUNDS / "Alpha3_source_current_kernel_2918_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2918_STATIONARY_ALPHA3_FLUX_ZERO_OR_BETA_SOURCE_NORMALIZATION_NEXT_NONCLAIM.csv",
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
        ("SRC2918_00_2917_doc", SRC_2917_DOC, "alpha3;Validation overall", "2917 alpha3 handoff"),
        ("SRC2918_01_2917_next", SRC_2917_NEXT, "NEXT2917_0_2918;alpha3 source-current", "machine-readable 2918 target"),
        ("SRC2918_02_2917_kernel", SRC_2917_KERNEL, "DK2917_2_alpha3;SOURCE_CURRENT_KERNEL_MISSING_ULTRATIGHT_BOUND", "2917 alpha3 disformal kernel"),
        ("SRC2918_03_2917_zero", SRC_2917_ZERO, "ZDIS2917_5_verdict;Z_BDIS_FALSE_UNSIGNED", "2917 no-disformal theorem status"),
        ("SRC2918_04_2917_bounds", SRC_2917_BOUNDS, "PBOUND2917_4_alpha3;4e-20", "2917 alpha3 bound anchor"),
        ("SRC2918_05_alpha3_input", SRC_ALPHA3_INPUT, "A3_boundary;A3_domain;A3_total", "older alpha3 product inputs"),
        ("SRC2918_06_alpha3_eval", SRC_ALPHA3_EVAL, "not_scoreable_inputs_missing;A3_total", "older alpha3 evaluator status"),
        ("SRC2918_07_alpha3_gate", SRC_ALPHA3_GATE, "TG_boundary_zero;TG_domain_zero;TG_total_cancellation", "theorem-zero gates"),
        ("SRC2918_08_alpha3_total", SRC_ALPHA3_TOTAL, "G_total_no_cancellation_by_fit;G_R11_dependency", "total no-cancellation guard"),
        ("SRC2918_09_alpha3_decision", SRC_ALPHA3_DECISION, "D4_promotion;forbidden", "older promotion decision"),
        ("SRC2918_10_mu_zero", SRC_MU_ZERO, "ZA0_alpha3_exchange_owner;ZA7_conclusion", "source-current alpha3 zero attempt"),
        ("SRC2918_11_mu_skeleton", SRC_MU_SKELETON, "S0_boundary_alpha3;S1_domain_alpha3;S2_total_alpha3_guard", "boundary/domain product skeleton"),
        ("SRC2918_12_mu_pressure", SRC_MU_PRESSURE, "HP1_highest_pressure_group_identified;HP4_zero_theorem_attempt", "highest pressure lock"),
        ("SRC2918_13_boundary_attempt", SRC_BOUNDARY_ATTEMPT, "T7_conclusion;conditional_zero_lemma_no_claim", "boundary no-flux attempt"),
        ("SRC2918_14_boundary_owner", SRC_BOUNDARY_OWNER, "P0_scalar_only_boundary_data;P4_Ward_flux_closure", "boundary premise ownership"),
        ("SRC2918_15_domain_attempt", SRC_DOMAIN_ATTEMPT, "N7_no_leak_verdict;fail_current_corpus", "domain no-leak attempt"),
        ("SRC2918_16_domain_owner", SRC_DOMAIN_OWNER, "P2_domain_selector_no_vector;P5_R11_operator_vector", "domain premise ownership"),
        ("SRC2918_17_selector_ledger", SRC_SELECTOR_LEDGER, "SRR2577_5_delta_kappa;SRR2577_6_delta_ellJ", "kappa/ellJ residual rows"),
        ("SRC2918_18_selector_theorem", SRC_SELECTOR_THEOREM, "WSC2577_6_coupling_baseline_zero;WSC2577_7_current_verdict", "coupling baseline theorem gate"),
        ("SRC2918_19_selector_boundary", SRC_SELECTOR_BOUNDARY, "BZA2577_5_zero_flux_verdict;delta_kappa;delta_ellJ", "boundary flux and coupling audit"),
        ("SRC2918_20_hilbert_audit", SRC_HILBERT_AUDIT, "THO2615_5_owner_verdict;CONTRACT_READY_PARENT_UNSIGNED", "total Hilbert source owner"),
        ("SRC2918_21_noether", SRC_NOETHER, "NEC2615_2_weight_collapse;NEC2615_5_current_verdict", "Noether exchange collapse"),
        ("SRC2918_22_deltaw", SRC_DELTAW, "DWB2615_0_delta_w_block;DWB2615_6_nonclaim_lock", "delta_w block bound rows"),
        ("SRC2918_23_roll_frontier", SRC_ROLL_FRONTIER, "GRF2632_4_full_PPN;BLOCKED_VECTOR_VALUES_MISSING", "full local GR PPN frontier"),
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


def no_disformal_rows() -> list[dict[str, Any]]:
    specs = [
        ("NDS2918_0_parent_slot", "parent matter action excludes D(C_R)u_mu u_nu", "MISSING_PARENT_NO_DISFORMAL_SLOT", "would set d_R=b_dis=0 before alpha_i projection"),
        ("NDS2918_1_current_owner", "no parent-owned preferred vector/current u_mu survives locally", "MISSING_VECTOR_CURRENT_OWNER_AND_GAUGE_PROOF", "would kill alpha1/alpha2/alpha3 disformal response"),
        ("NDS2918_2_boundary_flux", "boundary and compact support fluxes have no spatial momentum projection", "MISSING_BOUNDARY_FLUX_ZERO_WITH_COUPLING", "would remove B_zero_flux and source-exchange alpha3 heads"),
        ("NDS2918_3_domain_selector", "domain/projector sector has no vector, normal flow, or R11 operator leakage", "MISSING_DOMAIN_SELECTOR_NO_VECTOR_AND_R11_SILENCE", "would remove domain alpha3 and xi tails"),
        ("NDS2918_4_coupling_baseline", "Dln(kappa_MTS)=Dln(ell_J)=0 on the local exterior comparison branch", "MISSING_PARENT_CONSTANT_KAPPA_ELLJ_PROOF", "would prevent coupling drift entering alpha3/source normalization"),
        ("NDS2918_5_readout", "measured GM/readout is fixed before variation and cannot absorb source-current residuals", "MISSING_FIXED_BEFORE_READOUT_NO_ABSORPTION", "would stop fitted-GM masking"),
        ("NDS2918_6_verdict", "parent no-disformal/preferred-frame slot through PPN order", "Z_ALPHA3_DISFORMAL_FALSE_UNSIGNED", "no theorem-zero claim; keep alpha3 source-current kernel"),
    ]
    return [
        add_common(
            {
                "audit_id": audit_id,
                "zero_clause": clause,
                "current_status": status,
                "if_proved": effect,
                "source_paths": f"{SRC_2917_ZERO};{SRC_BOUNDARY_ATTEMPT};{SRC_DOMAIN_ATTEMPT};{SRC_SELECTOR_THEOREM}",
                "theorem_zero_adopted": False,
            }
        )
        for audit_id, clause, status, effect in specs
    ]


def alpha3_kernel_rows() -> list[dict[str, Any]]:
    common_sources = f"{SRC_2917_KERNEL};{SRC_MU_ZERO};{SRC_MU_SKELETON};{SRC_SELECTOR_LEDGER};{SRC_SELECTOR_THEOREM};{SRC_NOETHER}"
    specs = [
        (
            "A3K2918_0_definition",
            "Delta_alpha3_MTS",
            "alpha3 source-current residual",
            "Delta alpha3_MTS := Pi_alpha3[P_loc(nabla Gamma_eff - nabla_mu Khat^{mu nu})] + Pi_alpha3[disformal/source-current tails]",
            "PPN preferred-frame alpha3 is the spatial momentum/source-exchange projection; Ward ownership alone is not absence",
            "DEFINITION_FILLED_NONCLAIM",
        ),
        (
            "A3K2918_1_boundary_flux",
            "F_boundary_alpha3",
            "boundary compact-support momentum flux",
            "F_boundary_alpha3 := lim_S r^2 n_mu P_alpha3_nu K_boundary^{mu nu}/(G_eff M_eff)",
            "|Delta alpha3_boundary| <= |W_boundary_alpha3| |epsilon_boundary_flux|",
            "MISSING_BOUNDARY_NOFLUX_THEOREM_OR_PRODUCT",
        ),
        (
            "A3K2918_2_domain_flux",
            "F_domain_alpha3",
            "domain/projector momentum flux",
            "F_domain_alpha3 := lim_S r^2 n_mu P_alpha3_nu K_domain/projector^{mu nu}/(G_eff M_eff)",
            "|Delta alpha3_domain| <= |W_domain_alpha3| |epsilon_domain_flux|",
            "MISSING_DOMAIN_NOLEAK_THEOREM_OR_PRODUCT",
        ),
        (
            "A3K2918_3_source_exchange",
            "F_exchange_alpha3",
            "Noether exchange and disconnected source-block flux",
            "F_exchange_alpha3 := Pi_alpha3[sum_C delta_w_C nabla_mu T_C^{mu nu} + source_shadow^nu]",
            "|Delta alpha3_exchange| <= |K_exchange|(|delta_w_block|+|A_source_shadow|+|q_nonH|)",
            "MISSING_EXCHANGE_GRAPH_CONNECTIVITY_OR_FINITE_BLOCK_BOUND",
        ),
        (
            "A3K2918_4_kappa",
            "F_kappa_alpha3",
            "gravitational coupling baseline drift",
            "F_kappa_alpha3 := Pi_alpha3[Dln(kappa_MTS)] with source/readout fixed before fitting",
            "|Delta alpha3_kappa| <= |K_alpha3_kappa| |Dln(kappa_MTS)|",
            "MISSING_PARENT_CONSTANT_KAPPA_PROOF_OR_VALUE",
        ),
        (
            "A3K2918_5_ellJ",
            "F_ellJ_alpha3",
            "source-current scale drift",
            "F_ellJ_alpha3 := Pi_alpha3[Dln(ell_J)] in the Hilbert-source/current equation",
            "|Delta alpha3_ellJ| <= |K_alpha3_ellJ| |Dln(ell_J)|",
            "MISSING_PARENT_CONSTANT_ELLJ_PROOF_OR_VALUE",
        ),
        (
            "A3K2918_6_dR_vector",
            "F_dR_alpha3",
            "disformal/preferred-vector current",
            "F_dR_alpha3 := Pi_alpha3[D(C_R)u_mu u_nu source-current response]",
            "|Delta alpha3_dR| <= |K_alpha3_dR| |d_R|",
            "MISSING_NO_DISFORMAL_SLOT_OR_D_R_VALUE",
        ),
        (
            "A3K2918_7_tail",
            "F_tail_alpha3",
            "endpoint/readout/domain tail",
            "F_tail_alpha3 := Pi_alpha3[epsilon_endpoint_R + q_domain + epsilon_projector + delta_GM_readout]",
            "|Delta alpha3_tail| <= sum_abs(endpoint/domain/readout tail heads)",
            "MISSING_ENDPOINT_DOMAIN_READOUT_KERNELS",
        ),
        (
            "A3K2918_8_total_abs",
            "Delta_alpha3_abs",
            "no-cancellation alpha3 envelope",
            "Delta_alpha3_abs := sum_abs(A3K2918_1..A3K2918_7)",
            "claim-safe only if every head is theorem-zero or source-backed finite and individually under 4e-20 unless a parent identity forces cancellation",
            "SCHEMA_READY_VALUES_MISSING",
        ),
        (
            "A3K2918_9_verdict",
            "alpha3 source-current kernel",
            "2918 branch verdict",
            "alpha3 is now reduced to named source-current/coupling heads",
            "kernel is explicit but nonclaim; no head has value/theorem-zero strong enough for scoring",
            "ALPHA3_SOURCE_CURRENT_KERNEL_FILLED_AS_SOURCE_READY_NONCLAIM",
        ),
    ]
    return [
        add_common(
            {
                "kernel_id": kernel_id,
                "symbol": symbol,
                "component": component,
                "definition": definition,
                "bound_or_rule": rule,
                "current_status": status,
                "source_paths": common_sources,
                "observable_target": "alpha3",
                "target_bound_abs": "4e-20",
                "units": "dimensionless_abs_after_PPN_projection",
                "promotion_allowed_now": False,
            }
        )
        for kernel_id, symbol, component, definition, rule, status in specs
    ]


def product_rows() -> list[dict[str, Any]]:
    specs = [
        ("A3P2918_0_boundary", "boundary_monopole_shift", "alpha3_boundary = W_boundary_alpha3 * epsilon_boundary_flux", "4e-20", "MISSING_NUMERIC_PRODUCT_OR_THEOREM_ZERO", "conditional boundary scalar lemma not parent-owned"),
        ("A3P2918_1_domain", "domain_projector_mass", "alpha3_domain = W_domain_alpha3 * epsilon_domain_flux", "4e-20", "MISSING_NUMERIC_PRODUCT_OR_THEOREM_ZERO", "domain selector/R11 operator silence not parent-derived"),
        ("A3P2918_2_source_exchange", "source_exchange_block", "alpha3_exchange = K_exchange*(delta_w_block + A_source_shadow + q_nonH)", "4e-20", "MISSING_EXCHANGE_GRAPH_OR_BOUND", "Noether collapse is conditional; block graph/bounds missing"),
        ("A3P2918_3_kappa", "kappa_MTS_baseline", "alpha3_kappa = K_alpha3_kappa * Dln(kappa_MTS)", "4e-20", "MISSING_CONSTANT_KAPPA_PROOF_OR_VALUE", "coupling baseline not parent-derived"),
        ("A3P2918_4_ellJ", "ell_J_source_scale", "alpha3_ellJ = K_alpha3_ellJ * Dln(ell_J)", "4e-20", "MISSING_CONSTANT_ELLJ_PROOF_OR_VALUE", "source-current scale owner not parent-derived"),
        ("A3P2918_5_disformal_vector", "d_R_vector_current", "alpha3_dR = K_alpha3_dR * d_R", "4e-20", "MISSING_NO_DISFORMAL_SLOT_OR_D_R_VALUE", "no-disformal theorem unsigned"),
        ("A3P2918_6_total", "alpha3_total_abs", "abs_total = sum_abs(all active alpha3 heads)", "4e-20", "MISSING_ALL_HEADS_OR_PARENT_CANCELLATION_IDENTITY", "no post-fit cancellation allowed"),
    ]
    return [
        add_common(
            {
                "product_id": product_id,
                "channel": channel,
                "product_law": law,
                "target_bound_abs": bound,
                "current_status": status,
                "reason": reason,
                "source_paths": f"{SRC_ALPHA3_INPUT};{SRC_ALPHA3_EVAL};{SRC_ALPHA3_TOTAL};{SRC_2917_BOUNDS}",
                "abs_le_bound": False,
                "score_input_present": False,
            }
        )
        for product_id, channel, law, bound, status, reason in specs
    ]


def coupling_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("COUP2918_0_total_Hilbert_owner", "ordinary source is the total Hilbert/coframe derivative", "CONDITIONAL_OWNER_CLEAN_PARENT_UNSIGNED", "THO2615_5 owner verdict remains contract-ready but not exclusive"),
        ("COUP2918_1_Noether_exchange", "relative source prefactors collapse inside connected exchange components", "DERIVED_CONDITIONAL_PARENT_UNSIGNED", "NEC2615_2 exact but ordinary exchange graph/source-shadow ban unsigned"),
        ("COUP2918_2_delta_w_block", "disconnected source-block residual is zero or bounded", "MISSING_EXCHANGE_CONNECTIVITY_OR_NUMERIC_BOUND", "delta_w_block remains retained nonclaim"),
        ("COUP2918_3_kappa", "Dln(kappa_MTS)=0 or finite source-backed alpha3 projection", "MISSING_PARENT_CONSTANT_KAPPA_PROOF_OR_VALUE", "coupling baseline gate itself"),
        ("COUP2918_4_ellJ", "Dln(ell_J)=0 or finite source-backed alpha3 projection", "MISSING_PARENT_CONSTANT_ELLJ_PROOF_OR_VALUE", "source-current scale gate itself"),
        ("COUP2918_5_no_source_shadow", "no separate source-shadow functional bypasses the Hilbert current", "NOT_PARENT_EXCLUDED", "source-shadow countermodel survives"),
        ("COUP2918_6_no_fitted_GM", "measured GM/readout cannot absorb alpha3 source-current heads", "MISSING_FIXED_BEFORE_READOUT_TRANSFER", "prevents fake local-GR pass by calibration"),
        ("COUP2918_7_verdict", "alpha3 coupling owner gates are claim-safe now", "COUPLING_OWNER_GATES_FAIL_CURRENT_MTS", "retain all alpha3 source-current heads"),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "requirement": requirement,
                "current_status": status,
                "reason": reason,
                "source_paths": f"{SRC_SELECTOR_THEOREM};{SRC_HILBERT_AUDIT};{SRC_NOETHER};{SRC_DELTAW};{SRC_ROLL_FRONTIER}",
                "gate_pass": False,
            }
        )
        for gate_id, requirement, status, reason in specs
    ]


def claim_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2918_0_no_disformal", "no disformal/preferred-frame slot is proved", "BLOCKED_NONCLAIM", "parent no-disformal/current-owner theorem unsigned", False),
        ("CG2918_1_alpha3_score", "alpha3 source-current prediction passes 4e-20", "BLOCKED_NONCLAIM", "all product heads missing numeric/theorem-zero inputs", False),
        ("CG2918_2_coupling_owner", "kappa_MTS and ell_J are locally constant/source-owned", "BLOCKED_NONCLAIM", "coupling baseline not parent-derived", False),
        ("CG2918_3_total_alpha3", "total alpha3 can pass by cancellation", "REJECTED_NONCLAIM", "no parent cancellation identity; no tuned cancellation allowed", False),
        ("CG2918_4_local_GR_Newton", "local GR/Newton follows after alpha3 kernel", "BLOCKED_NONCLAIM", "2918 fills a nonclaim alpha3 kernel only", False),
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
        ("DEC2918_0_no_disformal", "no_disformal_slot_not_proved", "No parent clause excludes D(C_R)u_mu u_nu or the preferred current through PPN order.", "retain d_R/vector alpha3 head"),
        ("DEC2918_1_alpha3_kernel", "alpha3_kernel_now_has_named_heads", "Boundary, domain, exchange, kappa, ellJ, d_R and endpoint/readout heads are separated under a no-cancellation rule.", "use kernel as future acquisition template"),
        ("DEC2918_2_coupling", "coupling_is_now_explicit_in_alpha3", "Dln(kappa_MTS) and Dln(ell_J) are not background words anymore; they are explicit alpha3 source-current gates.", "attack coupling baseline or keep finite rows"),
        ("DEC2918_3_next", "stationary_alpha3_flux_zero_is_best_next_derivation", "If stationary compact flux can be proved zero with fixed coupling/readout, alpha3 pressure drops sharply; if not, beta/source-normalization is the fallback.", "select 2919 stationary alpha3 flux theorem or beta/source-normalization fallback"),
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
                "route_id": "NEXT2918_0_2919",
                "selection_status": "selected_primary",
                "target_file": "2919-Y5-R2FR-stationary-alpha3-flux-zero-theorem-or-beta-source-normalization-kernel-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_stationary_alpha3_flux_zero_theorem_or_beta_source_normalization_kernel_under_AX1090_2919.py",
                "task": "try to prove the stationary compact exterior alpha3 momentum/source-current flux vanishes with fixed kappa_MTS, ell_J, boundary reference and readout; if it fails, route to beta/source-normalization second-order kernel",
                "success_condition": "alpha3 source-current heads theorem-zero under parent-signed stationary/fixed-coupling hypotheses, or finite product rows are source-backed with units and no-cancellation accounting",
                "fallback_condition": "keep alpha3 nonclaim and build beta/source-normalization second-order kernel as the next local-GR blocker",
                "guardrails": "no alpha3 cancellation by fit; no fitted GM absorption; no local GR/Newton/PPN claim; no formalization-workbench edits; no GitHub",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("no_disformal_copy", OUTPUTS["no_disformal"], BRANCH_OUTPUTS["no_disformal_copy"]),
        ("kernel_copy", OUTPUTS["kernel"], BRANCH_OUTPUTS["kernel_copy"]),
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
    no_disformal_rows_: list[dict[str, Any]],
    kernel_rows_: list[dict[str, Any]],
    product_rows_: list[dict[str, Any]],
    coupling_rows_: list[dict[str, Any]],
    claim_rows_: list[dict[str, Any]],
    next_rows_: list[dict[str, Any]],
    branch_rows_: list[dict[str, Any]],
    include_doc_check: bool,
) -> list[dict[str, Any]]:
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_outputs_with_validation = [*csv_outputs, OUTPUTS["validation"]]
    no_disformal_verdict = next(row for row in no_disformal_rows_ if row["audit_id"] == "NDS2918_6_verdict")
    kernel_verdict = next(row for row in kernel_rows_ if row["kernel_id"] == "A3K2918_9_verdict")
    coupling_verdict = next(row for row in coupling_rows_ if row["gate_id"] == "COUP2918_7_verdict")
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
    kernel_symbols = {str(row["symbol"]) for row in kernel_rows_}
    required_products = {
        "boundary_monopole_shift",
        "domain_projector_mass",
        "source_exchange_block",
        "kappa_MTS_baseline",
        "ell_J_source_scale",
        "d_R_vector_current",
        "alpha3_total_abs",
    }
    product_channels = {str(row["channel"]) for row in product_rows_}
    generated_paths = [*OUTPUTS.values(), *BRANCH_OUTPUTS.values(), DOC]
    checks = [
        ("VAL2918_0_source_paths_exist", all(bool(row["path_exists"]) for row in source_rows), "all cited source paths exist"),
        ("VAL2918_1_source_anchors_found", all(bool(row["anchors_found"]) for row in source_rows), "all source anchors found"),
        ("VAL2918_2_csv_outputs_parse", all(csv_parses(path) for path in csv_outputs_with_validation if path.exists()), "generated CSV outputs parse cleanly"),
        ("VAL2918_3_no_disformal_unsigned", no_disformal_verdict["current_status"] == "Z_ALPHA3_DISFORMAL_FALSE_UNSIGNED" and not bool(no_disformal_verdict["theorem_zero_adopted"]), "no-disformal theorem not adopted"),
        ("VAL2918_4_alpha3_kernel_complete", required_kernel_symbols.issubset(kernel_symbols), "alpha3 kernel contains all required heads"),
        ("VAL2918_5_alpha3_kernel_nonclaim", kernel_verdict["current_status"] == "ALPHA3_SOURCE_CURRENT_KERNEL_FILLED_AS_SOURCE_READY_NONCLAIM", "alpha3 kernel filled as source-ready nonclaim"),
        ("VAL2918_6_product_rows_complete", required_products.issubset(product_channels) and all(row["target_bound_abs"] == "4e-20" for row in product_rows_), "alpha3 product rows cover all heads with 4e-20 bound"),
        ("VAL2918_7_coupling_gates_fail_safe", coupling_verdict["current_status"] == "COUPLING_OWNER_GATES_FAIL_CURRENT_MTS" and all(not bool(row["gate_pass"]) for row in coupling_rows_), "coupling owner gates remain closed"),
        ("VAL2918_8_claim_gates_safe", all(not bool(row["claim_allowed"]) and not bool(row["valid_for_claim"]) and not bool(row["gate_pass"]) for row in claim_rows_), "no claim gate is open"),
        ("VAL2918_9_next_target_selected", next_rows_[0]["route_id"] == "NEXT2918_0_2919" and bool(next_rows_[0]["selected"]), "2919 stationary alpha3 flux target selected"),
        ("VAL2918_10_branch_copies_parse", all(bool(row["destination_exists"]) and bool(row["destination_parses"]) for row in branch_rows_), "branch copies exist and parse"),
        ("VAL2918_11_no_formalization_outputs", not any(is_under(path, FORMALIZATION) for path in generated_paths), "no generated output path is inside formalization-workbench"),
        ("VAL2918_12_doc_written", DOC.exists() if include_doc_check else True, "markdown checkpoint exists"),
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
            "validation_id": "VAL2918_OVERALL",
            "status": all(bool(row["status"]) for row in rows),
            "detail": "2918 validation overall",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        }
    )
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    no_disformal_rows_: list[dict[str, Any]],
    kernel_rows_: list[dict[str, Any]],
    product_rows_: list[dict[str, Any]],
    coupling_rows_: list[dict[str, Any]],
    claim_rows_: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    next_rows_: list[dict[str, Any]],
    branch_rows_: list[dict[str, Any]],
    validation_rows_: list[dict[str, Any]],
) -> None:
    overall = next(row for row in validation_rows_ if row["validation_id"] == "VAL2918_OVERALL")
    text = f"""# 2918 - Y5/R2FR Alpha3 Source-Current Kernel Or No-Disformal-Slot Theorem Under AX1090

Status: `Y5_R2FR_2918_no_disformal_slot_unsigned_alpha3_source_current_kernel_filled_nonclaim_stationary_flux_2919_next`

Claim ceiling: `no_alpha3_pass_no_disformal_zero_no_coupling_baseline_zero_no_local_GR_no_Newton_no_PPN_no_R10_no_GitHub_claim`

Generated UTC: `{RUN_UTC}`

## Summary

2918 takes the hard `alpha3` pressure row and rewrites it as a source-current/coupling kernel. The parent no-disformal-slot theorem is still unsigned, so `d_R/b_dis` cannot be killed. The useful result is that `alpha3` now has named heads:

`Delta_alpha3_abs = sum_abs(F_boundary_alpha3, F_domain_alpha3, F_exchange_alpha3, F_kappa_alpha3, F_ellJ_alpha3, F_dR_alpha3, F_tail_alpha3)`.

The bound lock remains `|alpha3| <= 4e-20`, but no head is score-ready. This is not a pass; it is a much sharper object to derive against.

The strongest next derivation is the stationary compact exterior flux theorem: if fixed `kappa_MTS`, fixed `ell_J`, fixed boundary reference, and fixed-before-readout source support force the alpha3 momentum flux to vanish, the preferred-frame branch weakens sharply. If not, the fallback is the beta/source-normalization second-order kernel.

## Source Register

{md_table(source_rows, ["source_id", "source_path", "anchors_found", "role", "missing_anchors"])}

## No-Disformal-Slot Audit

{md_table(no_disformal_rows_, ["audit_id", "zero_clause", "current_status", "if_proved", "theorem_zero_adopted", "valid_for_claim"])}

## Alpha3 Source-Current Kernel

{md_table(kernel_rows_, ["kernel_id", "symbol", "component", "definition", "bound_or_rule", "current_status", "target_bound_abs", "valid_for_claim"])}

## Alpha3 Product Bound Rows

{md_table(product_rows_, ["product_id", "channel", "product_law", "target_bound_abs", "current_status", "reason", "abs_le_bound", "valid_for_claim"])}

## Coupling Owner Gates

{md_table(coupling_rows_, ["gate_id", "requirement", "current_status", "reason", "gate_pass", "valid_for_claim"])}

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

This is a real tightening step. `alpha3` is no longer a vague preferred-frame warning; it is a concrete source-current equation. That pushes the project toward GR reduction because GR survives PPN partly by having no such preferred momentum/source-current residual.

The result is also unforgiving: the theory needs a parent identity, not a fit, to silence these heads. The most promising route is to prove stationary compact exterior flux silence with fixed coupling and fixed source support.

## Not Claimed

- no `alpha3` pass is claimed;
- no no-disformal-slot theorem is claimed;
- no `Dln(kappa_MTS)=0` or `Dln(ell_J)=0` theorem is claimed;
- no total-alpha3 cancellation is allowed without a parent identity;
- no PPN, R10, WEP, clock, orbital, local-GR or Newtonian reduction pass is claimed;
- no file in `formalization-workbench` is modified by this checkpoint;
- no public/GitHub action is implied.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    no_disformal_rows_ = no_disformal_rows()
    kernel_rows_ = alpha3_kernel_rows()
    product_rows_ = product_rows()
    coupling_rows_ = coupling_gate_rows()
    claim_rows_ = claim_rows()
    decision_rows_ = decision_rows()
    next_rows_ = next_rows()

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["no_disformal"], no_disformal_rows_)
    write_csv(OUTPUTS["kernel"], kernel_rows_)
    write_csv(OUTPUTS["products"], product_rows_)
    write_csv(OUTPUTS["coupling"], coupling_rows_)
    write_csv(OUTPUTS["claims"], claim_rows_)
    write_csv(OUTPUTS["decision"], decision_rows_)
    write_csv(OUTPUTS["next"], next_rows_)

    branch_rows_ = branch_rows()
    write_csv(OUTPUTS["branches"], branch_rows_)

    validation_rows_ = validation_rows(
        source_rows,
        no_disformal_rows_,
        kernel_rows_,
        product_rows_,
        coupling_rows_,
        claim_rows_,
        next_rows_,
        branch_rows_,
        include_doc_check=False,
    )
    write_csv(OUTPUTS["validation"], validation_rows_)
    write_doc(
        source_rows,
        no_disformal_rows_,
        kernel_rows_,
        product_rows_,
        coupling_rows_,
        claim_rows_,
        decision_rows_,
        next_rows_,
        branch_rows_,
        validation_rows_,
    )

    validation_rows_ = validation_rows(
        source_rows,
        no_disformal_rows_,
        kernel_rows_,
        product_rows_,
        coupling_rows_,
        claim_rows_,
        next_rows_,
        branch_rows_,
        include_doc_check=True,
    )
    write_csv(OUTPUTS["validation"], validation_rows_)
    write_doc(
        source_rows,
        no_disformal_rows_,
        kernel_rows_,
        product_rows_,
        coupling_rows_,
        claim_rows_,
        decision_rows_,
        next_rows_,
        branch_rows_,
        validation_rows_,
    )

    overall = next(row for row in validation_rows_ if row["validation_id"] == "VAL2918_OVERALL")
    if not bool(overall["status"]):
        raise SystemExit(1)


if __name__ == "__main__":
    main()

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
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "3015"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3015-Y5-R2FR-PPN-kernel-from-local-closure-residual-envelope-under-AX1090.md"

SOURCE_PATHS = {
    "SRC3015_00_3014_doc": ROOT / "3014-Y5-R2FR-parent-source-current-owner-for-R10-kernel-or-rank-zero-local-closure-under-AX1090.md",
    "SRC3015_01_3014_next": RESIDUALS / "P8_Y5_R2FR_3014_NEXT_TARGET.csv",
    "SRC3015_02_3014_closure": RESIDUALS / "P8_Y5_R2FR_3014_LOCAL_CLOSURE_RESIDUAL_ENVELOPE.csv",
    "SRC3015_03_3014_ppn_handoff": RESIDUALS / "P8_Y5_R2FR_3014_PPN_HANDOFF_FROM_R10_DEMOTION.csv",
    "SRC3015_04_ppn_bounds_2513": RESIDUALS / "P8_Y5_NO_SHADOW_2513_PPN_BOUND_INTERFACE.csv",
    "SRC3015_05_ppn_kernel_2513": LOCAL_BOUNDS / "PPN_source_weight_response_kernel_2513_NONCLAIM.csv",
    "SRC3015_06_measured_GM_guard_2513": BETA_DOCS / "Measured_GM_no_absorb_guard_2513_NONCLAIM.csv",
    "SRC3015_07_normalized_ppn_inputs_1640": RESIDUALS / "P8_Y5_PARENT_QLOC_1640_NORMALIZED_PPN_BOUND_INPUTS.csv",
    "SRC3015_08_common_frame_kernel_2489": LOCAL_BOUNDS / "First_common_frame_PPN_response_kernel_2489_NONCLAIM.csv",
    "SRC3015_09_gk_ppn_2559": LOCAL_BOUNDS / "GK_PPN_residual_ledger_2559_NONCLAIM.csv",
    "SRC3015_10_ppn_bound_2631": LOCAL_BOUNDS / "PPN_bound_comparator_ledger_2631_NONCLAIM.csv",
    "SRC3015_11_rankzero_envelope_2968": LOCAL_BOUNDS / "rank_zero_residual_envelope_2968_NONCLAIM.csv",
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3015_SOURCE_REGISTER.csv",
    "ppn_kernel_contract": RESIDUALS / "P8_Y5_R2FR_3015_PPN_KERNEL_CONTRACT.csv",
    "ppn_residual_vector": RESIDUALS / "P8_Y5_R2FR_3015_PPN_RESIDUAL_VECTOR_TEMPLATE.csv",
    "comparator_links": RESIDUALS / "P8_Y5_R2FR_3015_PPN_COMPARATOR_LINKS.csv",
    "gm_guard": RESIDUALS / "P8_Y5_R2FR_3015_FIXED_GM_GUARD.csv",
    "blockers": RESIDUALS / "P8_Y5_R2FR_3015_BLOCKER_LEDGER.csv",
    "dryrun": RESIDUALS / "P8_Y5_R2FR_3015_DRYRUN_RESULTS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3015_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3015_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3015_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3015_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3015_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "kernel_copy": LOCAL_BOUNDS / "PPN_kernel_from_local_closure_envelope_3015_NONCLAIM.csv",
    "vector_copy": LOCAL_BOUNDS / "PPN_residual_vector_template_3015_NONCLAIM.csv",
    "gm_guard_copy": LOCAL_BOUNDS / "fixed_GM_guard_for_PPN_closure_3015_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3015_PPN_SOURCE_FRAME_AND_KERNEL_OWNER_NEXT.csv",
}

for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    path.parent.mkdir(parents=True, exist_ok=True)


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "passed"}


def as_str(value: Any) -> str:
    return "" if value is None else str(value)


def under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def base(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "control_only": True,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "generated_utc": RUN_UTC,
    }


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for output_row in output_rows:
        for key in output_row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)


def csv_ok(path: Path) -> bool:
    try:
        rows(path)
        return True
    except Exception:
        return False


def md_table(output_rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, divider]
    for output_row in output_rows:
        cells = [as_str(output_row.get(column, "")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


source_register = [
    base(
        {
            "source_id": source_id,
            "local_path": str(path),
            "exists": path.exists(),
            "role": {
                "SRC3015_00_3014_doc": "previous checkpoint R10 demotion and PPN route",
                "SRC3015_01_3014_next": "3015 target definition",
                "SRC3015_02_3014_closure": "local closure residual envelope",
                "SRC3015_03_3014_ppn_handoff": "PPN handoff and no-shortcut guard",
                "SRC3015_04_ppn_bounds_2513": "source-backed comparator rows",
                "SRC3015_05_ppn_kernel_2513": "existing PPN source-weight kernel skeleton",
                "SRC3015_06_measured_GM_guard_2513": "fixed measured-GM no-absorb guard",
                "SRC3015_07_normalized_ppn_inputs_1640": "older missing normalized PPN input ledger",
                "SRC3015_08_common_frame_kernel_2489": "common-frame conformal/disformal PPN kernel rows",
                "SRC3015_09_gk_ppn_2559": "GK stress PPN residual ledger",
                "SRC3015_10_ppn_bound_2631": "PPN comparator bound ledger",
                "SRC3015_11_rankzero_envelope_2968": "rank-zero residual projection envelope",
            }[source_id],
            "status": "PRESENT" if path.exists() else "MISSING_LOCAL_SOURCE",
        }
    )
    for source_id, path in SOURCE_PATHS.items()
]

ppn_kernel_contract = [
    base(
        {
            "kernel_id": "PPNK3015_0_gamma",
            "observable": "gamma_minus_1",
            "residual_law": "delta_gamma_abs <= |K_gamma_metric Pi_PPN[Delta_A]| + |K_gamma_readout Delta_readout| + |K_gamma_source Delta_w_eff|",
            "needed_kernel": "K_gamma_metric; weak-field spatial metric response; source frame; readout gauge",
            "closure_input": "CENV3014_2_PPN_projection; CENV3014_0_master",
            "comparator": "PBOUND2513_0_gamma = 2.3e-05 dimensionless",
            "status": "KERNEL_CONTRACT_WRITTEN_VALUES_MISSING",
            "blocks_claim": "MISSING_K_GAMMA; MISSING_SOURCE_FRAME; MISSING_READOUT_GAUGE",
        }
    ),
    base(
        {
            "kernel_id": "PPNK3015_1_beta",
            "observable": "beta_minus_1",
            "residual_law": "delta_beta_abs <= |K_beta_second_order Pi_PPN[Delta_A]| + |K_beta_NH J_NH| + |K_beta_readout Delta_readout| + |second_order_tail|",
            "needed_kernel": "second-order weak-field source equation; nonlinear metric response; fixed-GM convention",
            "closure_input": "CENV3014_0_master plus non-Hilbert/readout pieces",
            "comparator": "PBOUND2513_1_beta = 7.8e-05 dimensionless",
            "status": "SECOND_ORDER_KERNEL_MISSING",
            "blocks_claim": "MISSING_BETA_SECOND_ORDER_KERNEL; MISSING_SOURCE_NORMALIZATION",
        }
    ),
    base(
        {
            "kernel_id": "PPNK3015_2_alpha1",
            "observable": "alpha1",
            "residual_law": "alpha1_abs <= |K_alpha1_frame d_R| + |K_alpha1_source Delta_w_eff| + |K_alpha1_endpoint epsilon_endpoint|",
            "needed_kernel": "preferred-frame vector/disformal/source-frame kernel",
            "closure_input": "domain/readout/source-current closure components",
            "comparator": "PBOUND2513_2_alpha1 = 1e-04 dimensionless",
            "status": "PREFERRED_FRAME_KERNEL_MISSING",
            "blocks_claim": "MISSING_FRAME_VECTOR; MISSING_ENDPOINT_KERNEL",
        }
    ),
    base(
        {
            "kernel_id": "PPNK3015_3_alpha2",
            "observable": "alpha2",
            "residual_law": "alpha2_abs <= |K_alpha2_frame d_R| + |K_alpha2_boundary Q_edge| + |K_alpha2_projector Delta_mu_projector|",
            "needed_kernel": "spin/frame/domain/projector response matrix",
            "closure_input": "boundary and projector closure components",
            "comparator": "PBOUND2513_3_alpha2 = 2e-09 dimensionless",
            "status": "VECTOR_DOMAIN_KERNEL_MISSING",
            "blocks_claim": "MISSING_DOMAIN_PROJECTOR_KERNEL",
        }
    ),
    base(
        {
            "kernel_id": "PPNK3015_4_alpha3",
            "observable": "alpha3",
            "residual_law": "alpha3_abs <= |K_alpha3_exchange Delta_w_eff| + |K_alpha3_NH J_NH| + |K_alpha3_boundary Q_edge|",
            "needed_kernel": "source-current conservation/exchange response; no-Hilbert-current theorem or finite bound",
            "closure_input": "Hilbert/non-Hilbert/source-current closure components",
            "comparator": "PBOUND2513_4_alpha3 = 4e-20 dimensionless",
            "status": "SOURCE_EXCHANGE_KERNEL_ULTRATIGHT_MISSING",
            "blocks_claim": "MISSING_SOURCE_CURRENT_OWNER; ULTRATIGHT_BOUND_REQUIRES_THEOREM_ZERO_OR_STRONG_NUMERIC_BOUND",
        }
    ),
    base(
        {
            "kernel_id": "PPNK3015_5_xi",
            "observable": "xi",
            "residual_law": "xi_abs <= |K_xi_boundary Q_edge| + |K_xi_domain Delta_worldtube| + |K_xi_projective trace_projective|",
            "needed_kernel": "preferred-location/boundary/domain response",
            "closure_input": "boundary, worldtube and projector closure components",
            "comparator": "PBOUND2513_5_xi = 4e-09 dimensionless",
            "status": "BOUNDARY_DOMAIN_KERNEL_MISSING",
            "blocks_claim": "MISSING_BOUNDARY_DOMAIN_RESPONSE",
        }
    ),
    base(
        {
            "kernel_id": "PPNK3015_6_total",
            "observable": "PPN_abs_vector",
            "residual_law": "Delta_PPN_abs = componentwise abs vector over gamma,beta,alpha1,alpha2,alpha3,xi; no cancellation between components or source families",
            "needed_kernel": "all component kernels plus component values/zero theorems",
            "closure_input": "CENV3014_3_total_no_cancellation",
            "comparator": "componentwise PPN bounds",
            "status": "VECTOR_SCHEMA_READY_VALUES_MISSING",
            "blocks_claim": "MISSING_ALL_COMPONENT_VALUES_OR_ZERO_THEOREMS",
        }
    ),
]

ppn_residual_vector = [
    base(
        {
            "vector_id": "PVEC3015_0_template",
            "components": "gamma_minus_1_abs; beta_minus_1_abs; alpha1_abs; alpha2_abs; alpha3_abs; xi_abs",
            "formula": "Delta_PPN_abs = K_PPN[Delta_rankzero_source_abs_A, Delta_readout, Delta_w_eff, Q_edge, J_NH, projector_tail]",
            "required_units": "dimensionless componentwise residual vector",
            "source_frame": "MISSING_WEAK_FIELD_SOURCE_FRAME",
            "gauge": "MISSING_PPN_GAUGE_AND_READOUT_MAP",
            "fixed_GM_policy": "only one proven common universal scalar may be absorbed into measured GM",
            "status": "TEMPLATE_ONLY_NONCLAIM",
        }
    ),
    base(
        {
            "vector_id": "PVEC3015_1_no_cancellation",
            "components": "absolute component envelope",
            "formula": "each PPN component is bounded by an absolute sum of its source families; no cancellation credit unless a parent identity signs it",
            "required_units": "dimensionless",
            "source_frame": "same as PVEC3015_0",
            "gauge": "same as PVEC3015_0",
            "fixed_GM_policy": "relative/source/time/frame weights survive fixed-GM calibration",
            "status": "GUARD_ACTIVE_VALUES_MISSING",
        }
    ),
]

comparator_links = []
for bound_row in rows(SOURCE_PATHS["SRC3015_04_ppn_bounds_2513"]):
    comparator_links.append(
        base(
            {
                "link_id": f"CLINK3015_{len(comparator_links)}_{bound_row.get('observable', 'unknown')}",
                "bound_id": bound_row.get("bound_id", ""),
                "observable": bound_row.get("observable", ""),
                "upper_bound": bound_row.get("upper_bound", ""),
                "units": bound_row.get("units", ""),
                "source_dataset": bound_row.get("source_dataset", ""),
                "comparator_status": bound_row.get("comparator_status", ""),
                "needed_prediction_row": "matching PPNK3015 component numeric prediction in same fixed-GM/source-frame convention",
                "current_status": "COMPARATOR_ONLY_NOT_MTS_PREDICTION",
            }
        )
    )

gm_guard = [
    base(
        {
            "guard_id": "GMG3015_0_common_mode",
            "rule": "one constant, universal, range/time/species/frame independent source normalization may be absorbed into measured GM only after universality is proved",
            "mathematical_form": "U_obs := G_obs M_obs/r fixes one common multiplicative scale",
            "current_status": "CONDITIONAL_CALIBRATION_RULE_ONLY",
            "blocks": "absorbing relative/source/frame residuals into fitted GM",
        }
    ),
    base(
        {
            "guard_id": "GMG3015_1_relative_weight",
            "rule": "relative species/source weights survive fixed-GM calibration",
            "mathematical_form": "epsilon_A - epsilon_ref remains in observables after one GM quotient",
            "current_status": "LIVE_RESIDUAL",
            "blocks": "claiming WEP-clean or one-body calibrated source shifts are GR",
        }
    ),
    base(
        {
            "guard_id": "GMG3015_2_range_time_frame",
            "rule": "range/time/frame/source-profile dependence cannot be hidden in a constant GM fit",
            "mathematical_form": "delta U(r,t,frame)/U != constant over comparison domain",
            "current_status": "LIVE_RESIDUAL",
            "blocks": "PPN/R10/orbital consistency shortcuts",
        }
    ),
    base(
        {
            "guard_id": "GMG3015_3_readout",
            "rule": "PPN gauge/readout map must be fixed before comparing gamma/beta",
            "mathematical_form": "Delta_PPN_obs = Delta_PPN_field + T_readout[Delta_w_eff]",
            "current_status": "MISSING_READOUT_GAUGE_SOURCE_NORMALIZATION",
            "blocks": "fake beta/gamma closure by post-fit calibration",
        }
    ),
]

blockers = [
    base(
        {
            "blocker_id": "BLK3015_0_K_PPN",
            "blocking_condition": "MISSING_K_PPN_RESPONSE_KERNEL",
            "precise_missing_object": "linear and second-order weak-field response maps from closure residual components to gamma,beta,alpha_i,xi",
            "why_it_blocks": "PPN residual vector cannot be computed from Delta_rankzero_source_abs_A",
            "next_attack": "derive K_gamma first under fixed source frame, then beta second-order kernel",
        }
    ),
    base(
        {
            "blocker_id": "BLK3015_1_source_frame",
            "blocking_condition": "MISSING_WEAK_FIELD_SOURCE_FRAME_AND_PPN_GAUGE",
            "precise_missing_object": "observed coframe, PPN gauge, source mass convention and readout map",
            "why_it_blocks": "gamma/beta can be shifted by gauge/readout/GM calibration",
            "next_attack": "lock source frame and measured-GM convention before any numeric bound comparison",
        }
    ),
    base(
        {
            "blocker_id": "BLK3015_2_component_values",
            "blocking_condition": "MISSING_COMPONENT_VALUES_OR_ZERO_THEOREMS",
            "precise_missing_object": "eps_JH_Z_abs, eps_JNH_abs, eps_B_abs, Delta_readout_abs_A, Q_cdb_abs, eps_projector_abs, E_DqZ_A",
            "why_it_blocks": "closure envelope remains symbolic",
            "next_attack": "fill or theorem-zero closure residual components one by one",
        }
    ),
    base(
        {
            "blocker_id": "BLK3015_3_alpha3_ultratight",
            "blocking_condition": "ALPHA3_SOURCE_EXCHANGE_ULTRATIGHT",
            "precise_missing_object": "source-current conservation/exchange theorem or extremely small numeric bound",
            "why_it_blocks": "alpha3 bound is too tight for handwaving; needs theorem-level silence or explicit source-current control",
            "next_attack": "route alpha3 to source-current zero theorem or keep as leading PPN blocker",
        }
    ),
    base(
        {
            "blocker_id": "BLK3015_4_no_cancellation",
            "blocking_condition": "NO_CANCELLATION_VECTOR_NOT_NUMERIC",
            "precise_missing_object": "componentwise absolute PPN vector with no offsetting source families",
            "why_it_blocks": "local GR recovery must not depend on cancellation between gamma/beta/preferred-frame pieces",
            "next_attack": "keep componentwise absolute vector until a parent identity signs a cancellation",
        }
    ),
]

dryrun_results = [
    base(
        {
            "dryrun_id": "DR3015_0_comparators",
            "check": "PPN comparator rows are linked",
            "passed": len(comparator_links) >= 6,
            "observed": f"{len(comparator_links)} comparator rows linked",
            "result_status": "COMPARATOR_SIDE_READY_NONCLAIM",
        }
    ),
    base(
        {
            "dryrun_id": "DR3015_1_kernel_values",
            "check": "K_PPN numeric/source-signed kernel values exist",
            "passed": False,
            "observed": "kernel rows are contracts only; values missing",
            "result_status": "BLOCKED_NONCLAIM",
        }
    ),
    base(
        {
            "dryrun_id": "DR3015_2_fixed_GM",
            "check": "fixed measured-GM guard is active",
            "passed": True,
            "observed": "relative/range/time/frame residuals cannot be absorbed into fitted GM",
            "result_status": "GUARD_ACTIVE",
        }
    ),
    base(
        {
            "dryrun_id": "DR3015_3_prediction_row",
            "check": "valid PPN prediction row exists",
            "passed": False,
            "observed": "source frame, K_PPN and component values missing",
            "result_status": "BLOCKED_NONCLAIM",
        }
    ),
    base(
        {
            "dryrun_id": "DR3015_4_claim",
            "check": "PPN/local-GR claim allowed",
            "passed": False,
            "observed": "kernel/source frame/component values missing",
            "result_status": "CLAIM_FORBIDDEN",
        }
    ),
]

promotion_gates = [
    base(
        {
            "gate_id": "GATE3015_0_sources_exist",
            "gate": "all cited local source paths exist",
            "result": all(boolish(row["exists"]) for row in source_register),
            "notes": "3015 only cites current local ledgers",
        }
    ),
    base(
        {
            "gate_id": "GATE3015_1_comparators_linked",
            "gate": "PPN comparator bounds are linked",
            "result": len(comparator_links) >= 6,
            "notes": "comparator side is present but not an MTS prediction",
        }
    ),
    base(
        {
            "gate_id": "GATE3015_2_fixed_GM_guard",
            "gate": "fixed measured-GM no-absorb guard is active",
            "result": True,
            "notes": "only one proven common scalar can be absorbed",
        }
    ),
    base(
        {
            "gate_id": "GATE3015_3_kernel_values",
            "gate": "K_PPN values/source-signed kernels exist",
            "result": False,
            "notes": "kernel contracts written; values missing",
        }
    ),
    base(
        {
            "gate_id": "GATE3015_4_prediction_row",
            "gate": "valid PPN prediction row exists",
            "result": False,
            "notes": "source frame, gauge, component values and no-cancellation vector are missing",
        }
    ),
    base(
        {
            "gate_id": "GATE3015_5_PPN_claim",
            "gate": "PPN/local-GR pass claim allowed",
            "result": False,
            "notes": "PPN is now structured, not passed",
        }
    ),
]

decision = [
    base(
        {
            "decision_id": "DEC3015_0_status",
            "decision": "3015 builds the PPN kernel contract from the local-closure residual envelope, but no PPN pass is claimed.",
            "rationale": "The comparator side exists and the fixed-GM guard is active; the theory side still needs K_PPN, source frame, gauge/readout map and component values.",
            "claim_allowed_after_decision": False,
        }
    ),
    base(
        {
            "decision_id": "DEC3015_1_priority",
            "decision": "Gamma and alpha3 are the next sharpest PPN targets.",
            "rationale": "Gamma is the cleanest weak-field metric response entry; alpha3 is ultratight and forces source-current conservation discipline.",
            "claim_allowed_after_decision": False,
        }
    ),
]

next_target = [
    base(
        {
            "next_id": "NEXT3015_0_3016",
            "priority": "selected_primary",
            "target_doc": "3016-Y5-R2FR-gamma-and-alpha3-PPN-kernel-first-derivation-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_gamma_and_alpha3_PPN_kernel_first_derivation_under_AX1090_3016.py",
            "mission": "Try to derive the first two concrete PPN kernels from the closure envelope: gamma as weak-field metric response, alpha3 as source-current exchange/conservation guard.",
            "success_condition": "gamma and alpha3 rows either get source-signed kernel formulas with explicit missing coefficients, or are blocked by exact source-frame/current-conservation clauses; no PPN claim.",
            "fallback_if_fail": "demote gamma/alpha3 to explicit kernel-owner blockers and move to source-frame lock",
            "guardrails": "no PPN pass; no fitted-GM absorption; no hidden cancellation; no formalization-workbench edits; no GitHub action",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["ppn_kernel_contract"], ppn_kernel_contract)
write_csv(OUTPUTS["ppn_residual_vector"], ppn_residual_vector)
write_csv(OUTPUTS["comparator_links"], comparator_links)
write_csv(OUTPUTS["gm_guard"], gm_guard)
write_csv(OUTPUTS["blockers"], blockers)
write_csv(OUTPUTS["dryrun"], dryrun_results)
write_csv(OUTPUTS["gates"], promotion_gates)
write_csv(OUTPUTS["decision"], decision)
write_csv(OUTPUTS["next"], next_target)

branch_rows = []
for key, source_key in [
    ("kernel_copy", "ppn_kernel_contract"),
    ("vector_copy", "ppn_residual_vector"),
    ("gm_guard_copy", "gm_guard"),
    ("next_copy", "next"),
]:
    shutil.copy2(OUTPUTS[source_key], BRANCH_OUTPUTS[key])
    branch_rows.append(
        base(
            {
                "copy_id": f"COPY3015_{len(branch_rows)}",
                "source": str(OUTPUTS[source_key]),
                "destination": str(BRANCH_OUTPUTS[key]),
                "exists": BRANCH_OUTPUTS[key].exists(),
                "purpose": key,
            }
        )
    )
write_csv(OUTPUTS["branches"], branch_rows)

all_generated = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
all_csv = [path for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) if path.suffix == ".csv"]
claim_rows = (
    source_register
    + ppn_kernel_contract
    + ppn_residual_vector
    + comparator_links
    + gm_guard
    + blockers
    + dryrun_results
    + promotion_gates
    + decision
    + next_target
)

validation_rows = [
    {
        "validation_id": "VAL3015_00_sources_exist",
        "passed": all(boolish(row["exists"]) for row in source_register),
        "requirement": "every cited local source path exists",
        "evidence": OUTPUTS["sources"].name,
    },
    {
        "validation_id": "VAL3015_01_csv_parse",
        "passed": all(csv_ok(path) for path in all_csv),
        "requirement": "generated CSV rows parse cleanly",
        "evidence": "all generated CSV artifacts import with csv.DictReader",
    },
    {
        "validation_id": "VAL3015_02_comparators_linked",
        "passed": len(comparator_links) >= 6 and all(row["current_status"] == "COMPARATOR_ONLY_NOT_MTS_PREDICTION" for row in comparator_links),
        "requirement": "PPN comparator rows are linked but not promoted as predictions",
        "evidence": OUTPUTS["comparator_links"].name,
    },
    {
        "validation_id": "VAL3015_03_kernel_contracts_written",
        "passed": len(ppn_kernel_contract) >= 7 and all(row["residual_law"] and row["blocks_claim"] for row in ppn_kernel_contract),
        "requirement": "component PPN kernel contracts are explicit with blockers",
        "evidence": OUTPUTS["ppn_kernel_contract"].name,
    },
    {
        "validation_id": "VAL3015_04_fixed_GM_guard_active",
        "passed": any(row["gate_id"] == "GATE3015_2_fixed_GM_guard" and boolish(row["result"]) for row in promotion_gates),
        "requirement": "fixed measured-GM no-absorb guard is active",
        "evidence": OUTPUTS["gm_guard"].name,
    },
    {
        "validation_id": "VAL3015_05_prediction_not_valid",
        "passed": any(row["gate_id"] == "GATE3015_4_prediction_row" and not boolish(row["result"]) for row in promotion_gates),
        "requirement": "no valid PPN prediction row is claimed",
        "evidence": OUTPUTS["gates"].name,
    },
    {
        "validation_id": "VAL3015_06_claims_blocked",
        "passed": all(not boolish(row.get("claim_allowed")) for row in claim_rows)
        and any(row["gate_id"] == "GATE3015_5_PPN_claim" and not boolish(row["result"]) for row in promotion_gates),
        "requirement": "PPN/local-GR claims remain blocked",
        "evidence": OUTPUTS["gates"].name,
    },
    {
        "validation_id": "VAL3015_07_missing_markers_nonclaim",
        "passed": all(not boolish(row.get("valid_for_claim")) for row in claim_rows if "MISSING" in " ".join(map(str, row.values()))),
        "requirement": "rows with MISSING markers are never valid_for_claim=true",
        "evidence": "all 3015 generated ledgers",
    },
    {
        "validation_id": "VAL3015_08_outputs_scoped",
        "passed": all(under(path, ROOT) for path in all_generated),
        "requirement": "no generated file is outside post-checkpoint-work",
        "evidence": "generated path scope check",
    },
    {
        "validation_id": "VAL3015_09_formalization_not_targeted",
        "passed": not any(under(path, FORMALIZATION) for path in all_generated),
        "requirement": "formalization-workbench is not modified by this checkpoint",
        "evidence": "output target list excludes formalization-workbench",
    },
    {
        "validation_id": "VAL3015_10_next_target_selected",
        "passed": next_target[0]["target_doc"].startswith("3016-Y5-R2FR-gamma-and-alpha3"),
        "requirement": "next target selects gamma and alpha3 PPN kernel derivation",
        "evidence": OUTPUTS["next"].name,
    },
]

overall_pass = all(boolish(row["passed"]) for row in validation_rows)
validation_rows.append(
    {
        "validation_id": "VAL3015_99_overall",
        "passed": overall_pass,
        "requirement": "all 3015 validation checks pass",
        "evidence": "aggregate of VAL3015_00 through VAL3015_10",
    }
)
write_csv(OUTPUTS["validation"], validation_rows)

doc = f"""# 3015 — PPN Kernel from Local Closure Residual Envelope under AX1090

Status: `Y5_R2FR_3015_PPN_kernel_contract_staged_gamma_alpha3_next`

## Verdict

3015 moves us closer to the actual GR/Newton target. R10 is no longer the main boxing ring; PPN is.

The PPN comparator side is present, and the fixed measured-`GM` guard is active. But the MTS prediction side is still a kernel contract, not a score: `K_PPN`, weak-field source frame, PPN gauge/readout map, and closure-component values are missing.

The useful result is a componentwise PPN residual vector:

`Delta_PPN_abs = (|gamma-1|, |beta-1|, |alpha1|, |alpha2|, |alpha3|, |xi|)`.

Every component is tied to the local-closure envelope, and every component remains nonclaim until source-frame and kernel owners are signed.

## Source Register

{md_table(source_register, ["source_id", "exists", "role", "status"])}

## PPN Kernel Contract

{md_table(ppn_kernel_contract, ["kernel_id", "observable", "status", "blocks_claim"])}

## PPN Residual Vector

{md_table(ppn_residual_vector, ["vector_id", "components", "status", "fixed_GM_policy"])}

## Comparator Links

{md_table(comparator_links, ["link_id", "observable", "upper_bound", "source_dataset", "current_status"])}

## Fixed GM Guard

{md_table(gm_guard, ["guard_id", "rule", "current_status", "blocks"])}

## Blocker Ledger

{md_table(blockers, ["blocker_id", "blocking_condition", "precise_missing_object", "next_attack"])}

## Dry-Run Results

{md_table(dryrun_results, ["dryrun_id", "check", "passed", "result_status"])}

## Promotion Gates

{md_table(promotion_gates, ["gate_id", "gate", "result", "notes"])}

## Decision Ledger

{md_table(decision, ["decision_id", "decision", "rationale"])}

## Next Target

{md_table(next_target, ["next_id", "target_doc", "mission", "success_condition"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}

## Files Written

- `{OUTPUTS["sources"]}`
- `{OUTPUTS["ppn_kernel_contract"]}`
- `{OUTPUTS["ppn_residual_vector"]}`
- `{OUTPUTS["comparator_links"]}`
- `{OUTPUTS["gm_guard"]}`
- `{OUTPUTS["blockers"]}`
- `{OUTPUTS["dryrun"]}`
- `{OUTPUTS["gates"]}`
- `{OUTPUTS["decision"]}`
- `{OUTPUTS["next"]}`
- `{OUTPUTS["branches"]}`
- `{OUTPUTS["validation"]}`
- `{BRANCH_OUTPUTS["kernel_copy"]}`
- `{BRANCH_OUTPUTS["vector_copy"]}`
- `{BRANCH_OUTPUTS["gm_guard_copy"]}`
- `{BRANCH_OUTPUTS["next_copy"]}`

## Hard Guardrails Still Active

- No PPN/local-GR pass claim.
- No fitted-`GM` absorption of source residuals.
- No hidden cancellation between PPN components.
- No comparator-bound inversion into theory coefficients.
- No `formalization-workbench` edits.
- No GitHub action.
"""

DOC.write_text(doc, encoding="utf-8")

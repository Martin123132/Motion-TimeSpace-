from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2631-Y5-R2FR-current-branch-no-shadow-full-PPN-vector-or-residual-kernel-fill.md"

PREFIX = "P8_Y5_NO_SHADOW_PPN_VECTOR_2631"

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "no_shadow_gate": RESIDUALS / f"{PREFIX}_NO_SHADOW_GATE_AUDIT.csv",
    "ppn_vector": RESIDUALS / f"{PREFIX}_FULL_PPN_VECTOR_LEDGER.csv",
    "ppn_bounds": RESIDUALS / f"{PREFIX}_PPN_BOUND_COMPARATOR_LEDGER.csv",
    "kernel_queue": RESIDUALS / f"{PREFIX}_RESIDUAL_KERNEL_FILL_QUEUE.csv",
    "route_guards": RESIDUALS / f"{PREFIX}_ROUTE_GUARDS.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2631_VALIDATION.csv",
}

SOURCES = [
    {
        "source_id": "SRC2631_00_2630_frontier",
        "role": "current branch handoff selecting no-shadow/full PPN vector",
        "path": ROOT / "2630-Y5-R2FR-CR-zero-theorem-or-absolute-tail-bound-row.md",
        "needles": [
            "CURRENT_BRANCH_NO_SHADOW_FULL_PPN_VECTOR_SELECTED_NEXT",
            "RVI2630_4_ppn_full_vector",
            "DOBS_E_KERNEL_NOT_DERIVED_CURRENT_CORPUS",
        ],
    },
    {
        "source_id": "SRC2631_01_2630_validation",
        "role": "2630 validation pass",
        "path": RESIDUALS / "P8_Y5_BRR545_2630_VALIDATION.csv",
        "needles": ["VAL2630_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC2631_02_2489_no_shadow_ppn",
        "role": "first current-branch common-frame PPN response kernel and no-shadow blocker",
        "path": ROOT / "2489-Y5-R2FR-first-common-frame-PPN-response-kernel-or-parent-no-shadow-clause.md",
        "needles": [
            "PARENT_NO_SHADOW_CLAUSE_NOT_DERIVED_CURRENT_CORPUS",
            "GAMMA_ONLY_PASS_FORBIDDEN",
            "PPNV2489_7_total_abs",
        ],
    },
    {
        "source_id": "SRC2631_03_1883_full_vector",
        "role": "full PPN residual vector precedent",
        "path": ROOT / "1883-Y5-R2FR-reciprocal-lock-delta-p-zero-or-full-PPN-residual-vector.md",
        "needles": [
            "RECIPROCAL_LOCK_NOT_PARENT_DERIVED",
            "FULL_PPN_RESIDUAL_VECTOR_BUILT_NONCLAIM",
            "PPNV1883_7_total_no_cancellation",
        ],
    },
    {
        "source_id": "SRC2631_04_1884_delta_p_qrhat",
        "role": "no-boundary-charge/delta_p q_R_hat bridge",
        "path": ROOT / "1884-Y5-R2FR-no-boundary-charge-source-descent-or-delta-p-input-contract.md",
        "needles": [
            "NO_BOUNDARY_CHARGE_NOT_PARENT_DERIVED",
            "delta_p=-q_R_hat/2",
            "CG1884_0_conditional_lemma",
        ],
    },
    {
        "source_id": "SRC2631_05_1885_beta_source",
        "role": "beta second-order/source-coupling gate",
        "path": ROOT / "1885-Y5-R2FR-beta-second-order-source-coupling-gate-or-parent-zero-row.md",
        "needles": [
            "BETA_GATE_NOT_DERIVED_CURRENT_CORPUS",
            "NO_SOURCE_ONLY_SLOT_IS_NEXT_BEST_ATTACK",
            "BRC1885_6_delta_beta_total_abs",
        ],
    },
    {
        "source_id": "SRC2631_06_1886_source_weight",
        "role": "no-source-only slot proof attempt and finite w_R contract",
        "path": ROOT / "1886-Y5-R2FR-common-matter-no-source-only-slot-proof-or-finite-wR-row.md",
        "needles": [
            "NO_SOURCE_ONLY_SLOT_NOT_PARENT_DERIVED",
            "SOURCE_WEIGHT_SEAM_IS_REAL",
            "FWR1886_1_wR",
        ],
    },
    {
        "source_id": "SRC2631_07_1889_source_current",
        "role": "source-current Ward owner and real Delta_w basis",
        "path": ROOT / "1889-Y5-R2FR-source-current-Ward-owner-or-real-deltaw-component-basis.md",
        "needles": [
            "SOURCE_CURRENT_WARD_OWNER_NOT_DERIVED",
            "NO_SOURCE_PREFACTOR_PARENT_ACTION_CLAUSE_IS_NEXT",
            "CB1889_1_pre_action_species_prefactor",
        ],
    },
    {
        "source_id": "SRC2631_08_local_ppn_bounds",
        "role": "local comparator bounds only",
        "path": LOCAL_BOUNDS / "local_bound_claims.csv",
        "needles": [
            "Cassini_Shapiro_gamma_2003",
            "Will_2014_PPN_beta_table",
            "Will_2014_PPN_alpha1_table",
            "R1_WEP_source_charge",
        ],
    },
]


def ensure_dirs() -> None:
    for directory in (RESIDUALS, LOCAL_BOUNDS, RAB_QUEUE):
        directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"empty rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        return bool(read_csv(path))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["path"]
        text = read_text(path)
        exists = path.exists()
        needles_present = exists and all(needle in text for needle in source["needles"])
        rows.append(
            {
                "source_id": source["source_id"],
                "role": source["role"],
                "source_path": str(path),
                "exists": bool_text(exists),
                "needles_present": bool_text(needles_present),
                "needles": "; ".join(source["needles"]),
                "valid_for_claim": "False",
                "claim_allowed": "False",
            }
        )
    return rows


def no_shadow_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "NSG2631_0_DObs_e_kernel",
            "claim": "radial-cell/reciprocal representative is invisible to observed coframe and readout",
            "current_status": "DOBS_E_KERNEL_NOT_DERIVED_CURRENT_CORPUS",
            "imported_from": str(ROOT / "2630-Y5-R2FR-CR-zero-theorem-or-absolute-tail-bound-row.md"),
            "why_it_matters": "without DObs_e[v_R]=0, b_R,d_R,w_R,endpoint/readout tails may survive even if q_shape looks vertical",
            "missing_for_claim": "MISSING_PARENT_OBSERVER_FUNCTOR_KERNEL;MISSING_COFAME_READOUT_SILENCE;MISSING_NO_HIDDEN_VISIBLE_MORPHISM",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "NSG2631_1_terminal_public_coframe",
            "claim": "all ordinary matter and clocks factor through a terminal public coframe E(q(Phi))",
            "current_status": "NOT_PARENT_SIGNED",
            "imported_from": str(ROOT / "2489-Y5-R2FR-first-common-frame-PPN-response-kernel-or-parent-no-shadow-clause.md"),
            "why_it_matters": "would set common Weyl/disformal/source/endpoint shadow coefficients to theorem-zero",
            "missing_for_claim": "MISSING_ACTION_DOMAIN_EXCLUSION;MISSING_TERMINALITY;MISSING_READOUT_AFTER_VARIATION_STABILITY",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "NSG2631_2_no_weyl_disformal_slot",
            "claim": "no A_R(C_R), B_R(C_R)u_mu u_nu, or equivalent representative shadow enters observables",
            "current_status": "CLOSURE_ONLY_COUNTERMODEL_RETAINED",
            "imported_from": str(ROOT / "2489-Y5-R2FR-first-common-frame-PPN-response-kernel-or-parent-no-shadow-clause.md"),
            "why_it_matters": "otherwise gamma/preferred-frame components can be changed without breaking covariance language",
            "missing_for_claim": "MISSING_PARENT_NO_SHADOW_CLAUSE;MISSING_DISFORMAL_RESPONSE_ZERO;MISSING_NO_CANCELLATION_THEOREM",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "NSG2631_3_no_source_prefactor_slot",
            "claim": "ordinary matter action admits no pre-variation source-only prefactor w_A(X)S_A",
            "current_status": "NO_SOURCE_PREFACTOR_PARENT_ACTION_CLAUSE_NOT_DERIVED",
            "imported_from": str(ROOT / "1889-Y5-R2FR-source-current-Ward-owner-or-real-deltaw-component-basis.md"),
            "why_it_matters": "Ward conservation alone can keep equations neat while changing Hilbert source weights and beta/source residuals",
            "missing_for_claim": "MISSING_LABEL_FORGETTING_FUNCTOR;MISSING_NO_PRE_ACTION_PREFACATORS;MISSING_PROJECTED_MASS_FLUX_OWNER",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "NSG2631_4_verdict",
            "claim": "parent no-shadow package closes the local PPN branch",
            "current_status": "PARENT_NO_SHADOW_FULL_PPN_VECTOR_NOT_CLOSED",
            "imported_from": str(ROOT / "2630-Y5-R2FR-CR-zero-theorem-or-absolute-tail-bound-row.md"),
            "why_it_matters": "gamma-only or closure-only local GR would be a fake win",
            "missing_for_claim": "MISSING_DOBS_E_KERNEL;MISSING_DELTA_P_QRHAT_ZERO_OR_VALUE;MISSING_BETA_VECTOR;MISSING_DISFORMAL_KERNEL;MISSING_SOURCE_PREFACATOR_THEOREM;MISSING_ENDPOINT_READOUT_KERNEL",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def ppn_vector_rows() -> list[dict[str, Any]]:
    return [
        {
            "component_id": "PPNV2631_0_delta_p_qR",
            "symbol": "delta_p; q_R_hat",
            "channel": "reciprocal-lock/spatial-curvature residual",
            "observable_targets": "gamma_minus_1; beta_minus_1; local_GR_Newton",
            "current_status": "MISSING_PARENT_NO_BOUNDARY_CHARGE_OR_NUMERIC_QRHAT",
            "imported_source": str(ROOT / "1884-Y5-R2FR-no-boundary-charge-source-descent-or-delta-p-input-contract.md"),
            "relation_or_kernel": "delta_p=-q_R_hat/2 if exterior C_R=-Q_R/r and q_R_hat=Q_R c^2/(GM_source)",
            "missing_for_claim": "MISSING_BOUNDARY_CHARGE_ZERO_THEOREM;MISSING_SOURCE_DESCENT;MISSING_MATTER_READOUT_DESCENT;MISSING_ARENA_PROJECTION",
            "next_action": "derive no-boundary-charge/source-descent theorem or supply a source-normalized finite q_R_hat row",
            "score_ready": "False",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "component_id": "PPNV2631_1_bR",
            "symbol": "b_R",
            "channel": "common Weyl/coframe shadow",
            "observable_targets": "gamma_minus_1; light_time",
            "current_status": "CONDITIONAL_GAMMA_KERNEL_READY_VALUE_MISSING",
            "imported_source": str(ROOT / "2489-Y5-R2FR-first-common-frame-PPN-response-kernel-or-parent-no-shadow-clause.md"),
            "relation_or_kernel": "gamma_obs-1=(delta_p+4 b_R delta_p)/(1-2 b_R delta_p)",
            "missing_for_claim": "MISSING_b_R_VALUE_OR_ZERO;MISSING_DELTA_P_VALUE_OR_ZERO;MISSING_NO_OTHER_PPN_CHANNELS",
            "next_action": "prove no-Weyl slot or keep b_R in the no-cancellation vector",
            "score_ready": "False",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "component_id": "PPNV2631_2_beta",
            "symbol": "Delta_beta_total_abs",
            "channel": "second-order g00/source/operator/readout residual",
            "observable_targets": "beta_minus_1",
            "current_status": "MISSING_BETA_RESPONSE_KERNEL_AND_SOURCE_NORMALIZED_VECTOR",
            "imported_source": str(ROOT / "1885-Y5-R2FR-beta-second-order-source-coupling-gate-or-parent-zero-row.md"),
            "relation_or_kernel": "Delta_beta_total_abs=sum abs(delta_beta_source,operator,q_loc,boundary,readout,epsilon_SN)",
            "missing_for_claim": "MISSING_SECOND_ORDER_FIELD_EQUATION;MISSING_SOURCE_NORMALIZATION;MISSING_MATTER_DESCENT;MISSING_READOUT_GAUGE",
            "next_action": "derive beta=1 from a parent source-normalized EH-like package or source every beta component",
            "score_ready": "False",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "component_id": "PPNV2631_3_dR",
            "symbol": "d_R",
            "channel": "disformal/preferred-frame shadow",
            "observable_targets": "alpha1; alpha2; alpha3; xi; gamma",
            "current_status": "MISSING_DISFORMAL_PREFERRED_FRAME_PROJECTION",
            "imported_source": str(ROOT / "2489-Y5-R2FR-first-common-frame-PPN-response-kernel-or-parent-no-shadow-clause.md"),
            "relation_or_kernel": "g_obs=A(C_R)^2 g_pub + D(C_R) u_mu u_nu requires a preferred-frame response matrix",
            "missing_for_claim": "MISSING_DISFORMAL_METRIC_ANSATZ;MISSING_VECTOR_NORMALIZATION;MISSING_BOUNDARY_DOMAIN_PROJECTION",
            "next_action": "prove no-disformal slot or build d_R to alpha_i response rows",
            "score_ready": "False",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "component_id": "PPNV2631_4_wR",
            "symbol": "w_R; Delta_w; beta_w_source; beta_w_test",
            "channel": "source-only/action-weight and source-current residual",
            "observable_targets": "beta_minus_1; WEP; Newton_GM; R10_source_leg; alpha3",
            "current_status": "MISSING_NO_SOURCE_PREFACTOR_THEOREM_OR_FINITE_COMPONENT_VECTOR",
            "imported_source": str(ROOT / "1889-Y5-R2FR-source-current-Ward-owner-or-real-deltaw-component-basis.md"),
            "relation_or_kernel": "pre-action w_A S_A changes Hilbert source while Ward conservation can still hold",
            "missing_for_claim": "MISSING_NO_PRE_ACTION_PREFACATOR;MISSING_COMPONENT_BASIS;MISSING_PARENT_COEFFICIENT_VECTOR;MISSING_TAU_K_QBAR_PROJECTIONS",
            "next_action": "derive no-source-prefactor/no-double-counting matter-normalization clause or source the first component-basis row",
            "score_ready": "False",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "component_id": "PPNV2631_5_endpoint",
            "symbol": "epsilon_endpoint_R",
            "channel": "boundary/endpoint/local projection tail",
            "observable_targets": "xi; alpha3; orbital_light_time; gamma/beta readout tails",
            "current_status": "MISSING_ENDPOINT_SILENCE_OR_PROJECTION",
            "imported_source": str(ROOT / "2489-Y5-R2FR-first-common-frame-PPN-response-kernel-or-parent-no-shadow-clause.md"),
            "relation_or_kernel": "endpoint/domain terms must be theorem-zero or retained as additive PPN vector components",
            "missing_for_claim": "MISSING_ENDPOINT_SILENCE;MISSING_BOUNDARY_DOMAIN_KERNEL;MISSING_ORBITAL_LIGHT_TIME_PROJECTION",
            "next_action": "prove boundary endpoint silence or produce finite endpoint response rows",
            "score_ready": "False",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "component_id": "PPNV2631_6_readout_gauge",
            "symbol": "alpha_readout; delta_GM",
            "channel": "post-variation PPN gauge/measured-GM calibration tail",
            "observable_targets": "gamma_minus_1; beta_minus_1; Newton_GM; clocks",
            "current_status": "MISSING_READOUT_GAUGE_SOURCE_NORMALIZATION",
            "imported_source": str(ROOT / "2489-Y5-R2FR-first-common-frame-PPN-response-kernel-or-parent-no-shadow-clause.md"),
            "relation_or_kernel": "observed U=GM/r must be the same measured source mass used by the parent field equation",
            "missing_for_claim": "MISSING_GM_CALIBRATION_MAP;MISSING_PPN_GAUGE_TRANSFORM;MISSING_READOUT_AFTER_VARIATION_STABILITY",
            "next_action": "derive fixed-before-readout transfer theorem or source a readout tail bound",
            "score_ready": "False",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "component_id": "PPNV2631_7_q_loc_Khat",
            "symbol": "q_loc^nu; Khat^{mu nu}",
            "channel": "physical local residual projection",
            "observable_targets": "beta_minus_1; clock; orbital; local_GR_Newton",
            "current_status": "MISSING_QLOC_WARD_ZERO_PROFILE_OR_FINITE_KERNEL",
            "imported_source": str(ROOT / "2630-Y5-R2FR-CR-zero-theorem-or-absolute-tail-bound-row.md"),
            "relation_or_kernel": "q_loc^nu=P_loc(nabla^nu Gamma_eff - nabla_mu Khat^{mu nu}) must vanish through PPN order or be bounded",
            "missing_for_claim": "MISSING_WARD_ZERO_THROUGH_OU2;MISSING_KHAT_PROJECTION;MISSING_SOURCE_NORMALIZED_PROFILE",
            "next_action": "derive q_loc local PPN kernel or retain it as additive residual in beta/orbital rows",
            "score_ready": "False",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "component_id": "PPNV2631_8_total_abs",
            "symbol": "Delta_PPN_abs",
            "channel": "componentwise no-cancellation envelope",
            "observable_targets": "all_PPN; local_GR_Newton",
            "current_status": "SCHEMA_READY_VALUES_MISSING",
            "imported_source": str(ROOT / "1883-Y5-R2FR-reciprocal-lock-delta-p-zero-or-full-PPN-residual-vector.md"),
            "relation_or_kernel": "sum absolute active components unless a parent identity proves exact cancellation",
            "missing_for_claim": "MISSING_ALL_COMPONENT_VALUES_OR_THEOREM_ZEROS;MISSING_NO_CANCELLATION_IDENTITY",
            "next_action": "score only after every component is theorem-zero or finite/source-backed in the same convention",
            "score_ready": "False",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def ppn_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "PBOUND2631_0_gamma",
            "source": "Cassini_Shapiro_gamma_2003",
            "observable": "gamma_minus_1",
            "bound_abs": "2.3e-05",
            "units": "dimensionless",
            "use_in_2631": "comparator_only_for_delta_p/b_R_combo",
            "prediction_missing": "delta_p;q_R_hat;b_R;no_other_channels",
            "score_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "PBOUND2631_1_beta",
            "source": "Will_2014_PPN_beta_table",
            "observable": "beta_minus_1",
            "bound_abs": "7.8e-05",
            "units": "dimensionless",
            "use_in_2631": "comparator_only_for_full_beta_vector",
            "prediction_missing": "Delta_beta_total_abs;source_normalization;readout_gauge",
            "score_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "PBOUND2631_2_alpha1",
            "source": "Will_2014_PPN_alpha1_table",
            "observable": "alpha1",
            "bound_abs": "1e-04",
            "units": "dimensionless",
            "use_in_2631": "preferred-frame comparator only",
            "prediction_missing": "d_R_response_matrix",
            "score_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "PBOUND2631_3_alpha2",
            "source": "Will_2014_PPN_alpha2_table",
            "observable": "alpha2",
            "bound_abs": "2e-09",
            "units": "dimensionless",
            "use_in_2631": "preferred-frame comparator only",
            "prediction_missing": "d_R/vector_domain_projection",
            "score_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "PBOUND2631_4_alpha3",
            "source": "Will_2014_PPN_alpha3_table",
            "observable": "alpha3",
            "bound_abs": "4e-20",
            "units": "dimensionless",
            "use_in_2631": "source-current/momentum-flux comparator only",
            "prediction_missing": "source-current owner;endpoint;nonHilbert current kernel",
            "score_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "PBOUND2631_5_xi",
            "source": "Will_2014_PPN_xi_table",
            "observable": "xi",
            "bound_abs": "4e-09",
            "units": "dimensionless",
            "use_in_2631": "preferred-location/domain comparator only",
            "prediction_missing": "boundary/domain response kernel",
            "score_ready": "False",
            "valid_for_claim": "False",
        },
    ]


def kernel_queue_rows() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "KQ2631_0_delta_p_qRhat",
            "target_kernel": "no-boundary-charge/source-descent or finite q_R_hat row",
            "priority": "high",
            "why_priority": "first-order spatial curvature residual feeds the gamma combo directly",
            "proof_route": "Q_R=0 plus exterior silence and C_R(infinity)=0 gives C_R=0 and delta_p=0",
            "fallback_row": "source-normalized delta_p/q_R_hat row with GM convention",
            "status": "OPEN_NONCLAIM",
            "valid_for_claim": "False",
        },
        {
            "queue_id": "KQ2631_1_beta_vector",
            "target_kernel": "beta second-order source-normalized response",
            "priority": "high",
            "why_priority": "gamma cannot imply beta and local GR needs beta=1 or finite vector",
            "proof_route": "parent EH-like local operator plus universal matter coupling and measured-GM source conservation",
            "fallback_row": "Delta_beta_total_abs component row",
            "status": "OPEN_NONCLAIM",
            "valid_for_claim": "False",
        },
        {
            "queue_id": "KQ2631_2_source_prefactor",
            "target_kernel": "no-source-prefactor/no-double-counting parent action clause",
            "priority": "highest_current_surgical_attack",
            "why_priority": "Ward conservation is not species-blindness; w_A S_A is the coupling loophole that can spoil Newton/PPN quietly",
            "proof_route": "label-forgotten matter functor plus no pre-action prefactors plus projected mass owner",
            "fallback_row": "Delta_w/beta_w/w_R component-basis row with tau/K/Qbar/material projections",
            "status": "SELECTED_FOR_NEXT_TARGET",
            "valid_for_claim": "False",
        },
        {
            "queue_id": "KQ2631_3_disformal_preferred_frame",
            "target_kernel": "d_R preferred-frame response matrix",
            "priority": "high_held",
            "why_priority": "preferred-frame bounds are extremely tight and no-shadow cannot ignore d_R",
            "proof_route": "parent no-disformal slot in observed coframe/action domain",
            "fallback_row": "d_R to alpha1/alpha2/alpha3/xi response rows",
            "status": "HELD_SECONDARY_NONCLAIM",
            "valid_for_claim": "False",
        },
        {
            "queue_id": "KQ2631_4_endpoint_readout",
            "target_kernel": "endpoint/readout/radiative closure",
            "priority": "high_held",
            "why_priority": "post-variation GM/readout can fake or erase local residuals",
            "proof_route": "readout-after-variation plus no-hidden-visible coefficient morphism",
            "fallback_row": "epsilon_endpoint_R and alpha_readout/delta_GM rows",
            "status": "HELD_SECONDARY_NONCLAIM",
            "valid_for_claim": "False",
        },
        {
            "queue_id": "KQ2631_5_q_loc_Khat",
            "target_kernel": "physical q_loc/Khat local PPN projection",
            "priority": "medium_high",
            "why_priority": "beta/orbital/clock rows need the actual physical local residual profile, not a plateau axiom",
            "proof_route": "Ward-zero through O(U^2) or parent Khat projection silence",
            "fallback_row": "finite q_loc^nu profile coefficients",
            "status": "OPEN_NONCLAIM",
            "valid_for_claim": "False",
        },
    ]


def route_guard_rows() -> list[dict[str, Any]]:
    return [
        {
            "guard_id": "RG2631_0_no_gamma_only",
            "forbidden_shortcut": "gamma-only Cassini pass",
            "reason": "delta_p/b_R combo can look small while beta, disformal, source, endpoint and readout channels remain live",
            "machine_status": "FORBIDDEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "guard_id": "RG2631_1_no_closure_as_evidence",
            "forbidden_shortcut": "setting all PPN residuals to zero by closure/GR import",
            "reason": "closure benchmark is useful privately but not a parent MTS derivation",
            "machine_status": "FORBIDDEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "guard_id": "RG2631_2_no_fitted_GM_absorption",
            "forbidden_shortcut": "absorbing relative source weights into G_N or measured GM",
            "reason": "only universal derivative-silent common mode can be calibration; relative weights are observables",
            "machine_status": "FORBIDDEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "guard_id": "RG2631_3_no_cancellation_only",
            "forbidden_shortcut": "tuned cancellation between independent residual components",
            "reason": "component cancellations need a parent identity; otherwise use sum-absolute vector",
            "machine_status": "FORBIDDEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "guard_id": "RG2631_4_no_massless_R10",
            "forbidden_shortcut": "routing massless C_R/r PPN tail to finite-range R10 alpha(lambda)",
            "reason": "R10 needs finite Z/M^2/lambda/source-test couplings and real alpha(lambda) bounds",
            "machine_status": "FORBIDDEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "guard_id": "RG2631_5_no_Ward_only_species_blindness",
            "forbidden_shortcut": "using Ward conservation as proof of species-blind source coupling",
            "reason": "Ward conserves the current supplied by the action; it does not forbid pre-action w_A S_A",
            "machine_status": "FORBIDDEN",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG2631_0_internal_vector",
            "claim": "2631 may guide private local-PPN work",
            "gate_status": "ALLOW_INTERNAL_NONCLAIM",
            "why": "vector schema, source needles and comparator rows are consolidated",
            "gate_pass": "True",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG2631_1_parent_no_shadow",
            "claim": "parent no-shadow theorem closes b_R,d_R,w_R,endpoint/readout",
            "gate_status": "BLOCKED",
            "why": "DObs_e, terminal public coframe, no source-prefactor and readout/radiative clauses are unsigned",
            "gate_pass": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG2631_2_full_ppn_score",
            "claim": "MTS passes full PPN vector",
            "gate_status": "BLOCKED",
            "why": "no live theorem-zero or source-backed values exist for all active vector components",
            "gate_pass": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG2631_3_local_GR_Newton",
            "claim": "local GR/Newton reduction is derived",
            "gate_status": "BLOCKED",
            "why": "delta_p/q_R, beta, source-current, no-shadow/disformal, endpoint/readout and q_loc/Khat gates remain open",
            "gate_pass": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG2631_4_bound_comparator_score",
            "claim": "external PPN/WEP/R10 bounds can be scored as MTS predictions",
            "gate_status": "BLOCKED",
            "why": "bounds are pressure only until parent coefficients and arena projections are supplied",
            "gate_pass": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2631_0_vector_interface",
            "decision": "FULL_PPN_VECTOR_IS_CURRENT_BRANCH_INTERFACE",
            "rationale": "2630/2489/1883 agree that gamma-only is insufficient; every active local residual needs theorem-zero or finite source-backed status.",
            "consequence": "future local claims must pass delta_p/q_R, b_R, beta, d_R, w_R/source-current, endpoint, readout and q_loc/Khat gates.",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC2631_1_no_shadow",
            "decision": "NO_SHADOW_ROUTE_REMAINS_HIGH_VALUE_BUT_UNSIGNED",
            "rationale": "terminal public coframe/no-hidden-visible morphism would be powerful, but DObs_e and readout/radiative stability are not parent-derived.",
            "consequence": "keep no-shadow as theorem target, not as a closure axiom.",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC2631_2_delta_p_beta",
            "decision": "DELTA_P_AND_BETA_STAY_IN_VECTOR",
            "rationale": "no-boundary-charge gives an exact conditional route to delta_p=0, but Q_R=0 is unsigned; gamma does not determine beta.",
            "consequence": "do not score Cassini or beta until source-normalized rows exist.",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC2631_3_source_coupling",
            "decision": "SOURCE_PREFACTOR_COUPLING_IS_NEXT_BEST_LEAP",
            "rationale": "Ward is a bridge, not species-blindness; the w_A S_A countermodel is the coupling seam that can quietly break Newton/PPN while looking covariant.",
            "consequence": "attack no-source-prefactor/no-double-counting matter-normalization before more numerical local scoring.",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC2631_4_claim_policy",
            "decision": "NO_LOCAL_GR_OR_PPN_CLAIM_FROM_2631",
            "rationale": "this checkpoint is a consolidation and queue, not a derivation closure.",
            "consequence": "public-safe output remains work-in-progress/nonclaim.",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": "2632-Y5-R2FR-no-source-prefactor-parent-action-clause-or-PPN-component-basis-first-row.md",
            "script": "scripts/Y5_R2FR_no_source_prefactor_parent_action_clause_or_PPN_component_basis_first_row_2632.py",
            "objective": "try to derive the parent no-source-prefactor/no-double-counting matter-normalization clause that forbids w_A before variation; if it fails, stage the first nonclaim Delta_w/beta_w/w_R component-basis row with PPN/WEP/R10 projection requirements.",
            "include": "source-label forgetting; no pre-action species/source prefactors; source-current Ward bridge; projected mass flux; Delta_w component basis; tau/K/Qbar/material projections",
            "exclude": "Ward-only species-blindness, G_N/GM absorption of relative weights, WEP bound anchors as predictions, cancellation-only rows, local-GR/PPN claim",
            "selected": "True",
            "valid_for_claim": "False",
        },
        {
            "next_target": "2632b-Y5-R2FR-disformal-readout-PPN-kernel-or-parent-no-shadow-clause.md",
            "script": "scripts/Y5_R2FR_disformal_readout_PPN_kernel_or_parent_no_shadow_clause_2632b.py",
            "objective": "held secondary: prove no-disformal/readout shadow or build d_R/endpoint/readout response rows for preferred-frame and light-time tests.",
            "include": "d_R to alpha_i response; endpoint silence; readout-after-variation; no-hidden-visible morphism",
            "exclude": "gamma-only pass and closure-only no-shadow",
            "selected": "False",
            "valid_for_claim": "False",
        },
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_specs = [
        (
            "COPY2631_no_shadow_gate",
            "no_shadow_gate_audit",
            OUTPUTS["no_shadow_gate"],
            LOCAL_BOUNDS / "No_shadow_gate_audit_2631_NONCLAIM.csv",
        ),
        (
            "COPY2631_ppn_vector",
            "full_ppn_vector_ledger",
            OUTPUTS["ppn_vector"],
            LOCAL_BOUNDS / "Full_PPN_vector_ledger_2631_NONCLAIM.csv",
        ),
        (
            "COPY2631_ppn_bounds",
            "ppn_bound_comparator_ledger",
            OUTPUTS["ppn_bounds"],
            LOCAL_BOUNDS / "PPN_bound_comparator_ledger_2631_NONCLAIM.csv",
        ),
        (
            "COPY2631_kernel_queue",
            "kernel_fill_queue",
            OUTPUTS["kernel_queue"],
            RAB_QUEUE / "JR2631_CURRENT_BRANCH_PPN_KERNEL_FILL_QUEUE.csv",
        ),
        (
            "COPY2631_next",
            "next_target",
            OUTPUTS["next_target"],
            RAB_QUEUE / "JR2631_NO_SOURCE_PREFACTOR_OR_COMPONENT_BASIS_NEXT.csv",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, label, source_path, destination_path in copy_specs:
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, destination_path)
        rows.append(
            {
                "copy_id": copy_id,
                "label": label,
                "source_path": str(source_path),
                "destination_path": str(destination_path),
                "destination_exists": bool_text(destination_path.exists()),
                "csv_parses": bool_text(csv_parses(destination_path)),
                "row_count": len(read_csv(destination_path)) if destination_path.exists() else 0,
            }
        )
    return rows


def any_claim_promoted(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if row.get("valid_for_claim") == "True" or row.get("claim_allowed") == "True":
                return True
    return False


def missing_row_promoted(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    blocked_markers = ("MISSING_", "BLOCKED", "UNSIGNED", "CLOSURE_ONLY")
    for rows in rows_by_name.values():
        for row in rows:
            row_text = " ".join(str(value) for value in row.values())
            promoted = row.get("valid_for_claim") == "True" or row.get("claim_allowed") == "True"
            if promoted and any(marker in row_text for marker in blocked_markers):
                return True
    return False


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_paths = [path for name, path in OUTPUTS.items() if name != "validation"]
    source_rows = rows_by_name["source_register"]
    no_shadow_rows = rows_by_name["no_shadow_gate"]
    vector_rows = rows_by_name["ppn_vector"]
    bound_rows = rows_by_name["ppn_bounds"]
    queue_rows = rows_by_name["kernel_queue"]
    guard_rows = rows_by_name["route_guards"]
    gate_rows = rows_by_name["claim_gates"]
    decision_rows_local = rows_by_name["decision"]
    next_rows = rows_by_name["next_target"]
    branch_rows = rows_by_name["branch_copies"]

    required_components = {
        "PPNV2631_0_delta_p_qR",
        "PPNV2631_1_bR",
        "PPNV2631_2_beta",
        "PPNV2631_3_dR",
        "PPNV2631_4_wR",
        "PPNV2631_5_endpoint",
        "PPNV2631_6_readout_gauge",
        "PPNV2631_7_q_loc_Khat",
        "PPNV2631_8_total_abs",
    }
    observed_components = {row["component_id"] for row in vector_rows}

    checks: list[tuple[str, bool, str]] = [
        (
            "VAL2631_00_sources",
            all(row["exists"] == "True" and row["needles_present"] == "True" for row in source_rows),
            "all cited source paths exist and required needles are present",
        ),
        (
            "VAL2631_01_no_shadow_blocked",
            any(row["current_status"] == "PARENT_NO_SHADOW_FULL_PPN_VECTOR_NOT_CLOSED" for row in no_shadow_rows)
            and all(row["claim_allowed"] == "False" for row in no_shadow_rows),
            "parent no-shadow/full PPN closure remains blocked",
        ),
        (
            "VAL2631_02_full_vector_components",
            required_components.issubset(observed_components),
            f"full PPN vector components present: {len(observed_components)}",
        ),
        (
            "VAL2631_03_gamma_only_forbidden",
            any(row["forbidden_shortcut"] == "gamma-only Cassini pass" and row["machine_status"] == "FORBIDDEN" for row in guard_rows),
            "gamma-only pass is machine-forbidden",
        ),
        (
            "VAL2631_04_beta_source_blockers",
            any(row["component_id"] == "PPNV2631_2_beta" and "MISSING_BETA_RESPONSE_KERNEL" in row["current_status"] for row in vector_rows)
            and any(row["component_id"] == "PPNV2631_4_wR" and "MISSING_NO_SOURCE_PREFACTOR" in row["current_status"] for row in vector_rows),
            "beta and source-prefactor blockers are explicit",
        ),
        (
            "VAL2631_05_disformal_readout_blockers",
            any(row["component_id"] == "PPNV2631_3_dR" and "DISFORMAL" in row["current_status"] for row in vector_rows)
            and any(row["component_id"] == "PPNV2631_6_readout_gauge" and "READOUT" in row["current_status"] for row in vector_rows),
            "disformal and readout blockers are explicit",
        ),
        (
            "VAL2631_06_bounds_comparator_only",
            all(row["score_ready"] == "False" and row["valid_for_claim"] == "False" for row in bound_rows),
            "PPN bounds remain comparator-only",
        ),
        (
            "VAL2631_07_kernel_queue_next",
            any(row["status"] == "SELECTED_FOR_NEXT_TARGET" and "source-prefactor" in row["target_kernel"] for row in queue_rows),
            "source-prefactor/no-double-counting kernel selected as next best leap",
        ),
        (
            "VAL2631_08_claim_gates_safe",
            all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in gate_rows),
            "no claim gate promotes PPN/local-GR",
        ),
        (
            "VAL2631_09_decision_nonclaim",
            any(row["decision"] == "SOURCE_PREFACTOR_COUPLING_IS_NEXT_BEST_LEAP" for row in decision_rows_local)
            and all(row["valid_for_claim"] == "False" for row in decision_rows_local),
            "decision ledger records source coupling as next leap without claim promotion",
        ),
        (
            "VAL2631_10_next_target",
            any(row["selected"] == "True" and "2632" in row["next_target"] for row in next_rows),
            "2632 no-source-prefactor/component-basis target selected",
        ),
        (
            "VAL2631_11_no_claim_flags",
            not any_claim_promoted(rows_by_name),
            "no generated claim-sensitive row is promoted",
        ),
        (
            "VAL2631_12_missing_not_ready",
            not missing_row_promoted(rows_by_name),
            "no missing/blocked/unsigned/closure row is marked claim-ready",
        ),
        (
            "VAL2631_13_branch_copies",
            all(row["destination_exists"] == "True" and row["csv_parses"] == "True" for row in branch_rows),
            "branch/local/queue copies exist and parse",
        ),
        (
            "VAL2631_14_formalization_untouched",
            not any(str(path).startswith(str(FORMALIZATION)) for path in generated_paths + [DOC_PATH]),
            "no 2631 outputs are written under formalization-workbench",
        ),
        (
            "VAL2631_15_csv_parse",
            all(csv_parses(path) for path in generated_paths),
            "all generated 2631 CSVs parse",
        ),
        (
            "VAL2631_16_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
        ),
    ]
    rows = [
        {
            "check_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": "False",
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL2631_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "2631 current-branch no-shadow/full PPN vector consolidation",
            "valid_for_claim": "False",
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    generated_at = datetime.now(timezone.utc).isoformat()
    sections = [
        ("Source Register", rows_by_name["source_register"]),
        ("No-Shadow Gate Audit", rows_by_name["no_shadow_gate"]),
        ("Full PPN Vector Ledger", rows_by_name["ppn_vector"]),
        ("PPN Bound Comparator Ledger", rows_by_name["ppn_bounds"]),
        ("Residual Kernel Fill Queue", rows_by_name["kernel_queue"]),
        ("Route Guards", rows_by_name["route_guards"]),
        ("Claim Gates", rows_by_name["claim_gates"]),
        ("Decision Ledger", rows_by_name["decision"]),
        ("Next Target", rows_by_name["next_target"]),
        ("Branch Copies", rows_by_name["branch_copies"]),
        ("Validation", rows_by_name["validation"]),
    ]
    body = [
        "# 2631 - Y5 R2/f(R) Current-Branch No-Shadow Full PPN Vector Or Residual Kernel Fill",
        "",
        f"Generated: `{generated_at}`",
        "",
        "Status: `Y5_R2FR_2631_current_branch_no_shadow_full_PPN_vector_consolidated_source_prefactor_next_nonclaim`",
        "",
        "Claim ceiling: no local-GR/Newton reduction, no PPN pass, no Cassini/gamma-only pass, no source-current/Ward-only pass, no fitted-GM absorption, no cancellation-only rescue, no GitHub action, and no `formalization-workbench` edit is made.",
        "",
        "## Summary",
        "",
        "2631 rolls the local branch into one current-branch interface. The useful thing is not a new numerical score; it is a cleaner object-language target.",
        "",
        "The full local vector now has explicit live components: `delta_p/q_R_hat`, `b_R`, `Delta_beta_total_abs`, `d_R`, `w_R/Delta_w/beta_w`, endpoint tails, readout/GM gauge tails, physical `q_loc/Khat`, and the no-cancellation total.",
        "",
        "The strongest next leap is source-prefactor coupling. Ward conservation is real, but it does not prove species-blind source coupling; the surviving countermodel is `S_matter=sum_A w_A S_A`. So the next derivation should try to forbid that pre-variation slot from the parent action, or demote it into the first real finite component-basis row.",
        "",
    ]
    for title, rows in sections:
        body.extend([f"## {title}", "", markdown_table(rows), ""])
    body.extend(
        [
            "## Plain-English Verdict",
            "",
            "We are not circling the same object here; we have turned the local-GR problem into a checklist of exact couplings. The current bottleneck is the coupling seam: why ordinary matter cannot carry a hidden pre-variation source weight while still looking covariant after variation.",
            "",
            "If 2632 can parent-sign that no-source-prefactor/no-double-counting clause, several ugly residuals collapse at once: `w_R`, source-side beta leakage, WEP/source-current leakage, and part of the measured-GM ambiguity. If it cannot, the branch still improves because the finite component basis becomes explicit instead of hand-wavy.",
            "",
        ]
    )
    DOC_PATH.write_text("\n".join(body), encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "no_shadow_gate": no_shadow_gate_rows(),
        "ppn_vector": ppn_vector_rows(),
        "ppn_bounds": ppn_bound_rows(),
        "kernel_queue": kernel_queue_rows(),
        "route_guards": route_guard_rows(),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    rows_by_name["branch_copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)

    print(f"wrote {DOC_PATH}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

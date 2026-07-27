from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
COEFF = MICROSCOPE / "branch_locked_wep" / "coefficients"
QUARANTINE = MICROSCOPE / "quarantine" / "1474"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1474-Y5-R10-RAB-complete-Ci-parent-action-map-or-residual-vector-evaluator.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
START_TS = datetime.now(timezone.utc).timestamp()

PREV_NEXT = OUT / "P8_Y5_R10_1473_NEXT_TARGET.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1473_VALIDATION.csv"
PREV_THEOREM = OUT / "P8_Y5_R10_1473_PARENT_COUPLING_DOUBLE_ZERO_THEOREM_ATTEMPT.csv"
PREV_PREMISES = OUT / "P8_Y5_R10_1473_DOUBLE_ZERO_PREMISE_AUDIT.csv"
PREV_RESIDUALS = OUT / "P8_Y5_R10_1473_EXECUTABLE_LOCAL_RESIDUAL_VECTOR.csv"
PREV_HOOKS = OUT / "P8_Y5_R10_1473_RESIDUAL_HOOK_MAP.csv"

LOCAL_ACTION_511 = OUT / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv"
LOCAL_FIXED_511 = OUT / "P8_MIN_PARENT_LOCAL_GR_FIXED_POINT_CONDITIONS.csv"
LOCAL_RESIDUAL_511 = OUT / "P8_MIN_PARENT_LOCAL_GR_RESIDUAL_VECTOR.csv"
LOCAL_GATES_511 = OUT / "P8_MIN_PARENT_LOCAL_GR_GATE_TESTS.csv"
LOCAL_VECTOR_482 = OUT / "P8_LOCAL_GR_RESIDUAL_VECTOR_FROM_DOMAIN_SOURCE.csv"
LOCAL_PROMOTION_482 = OUT / "P8_LOCAL_GR_RESIDUAL_PROMOTION_GATES.csv"

SOURCE_COUPLING_1229 = OUT / "P8_Y5_R10_1229_LOCAL_GR_SOURCE_COUPLING_THEOREM_CONTRACT.csv"
WEP_OWNER_1077 = OUT / "P8_Y5_R10_1077_PARENT_WEP_COUPLING_OWNER_THEOREM_ATTEMPT.csv"
MATTER_COUPLING_716 = OUT / "P8_Y5_R10_716_MATTER_COUPLING_DERIVATION.csv"
FINITE_COUPLING_630 = OUT / "P8_Y5_R10_630_FINITE_COUPLING_DERIVATION.csv"
CPARENT_CONTRACT_1445 = OUT / "P8_Y5_R10_1445_C_PARENT_COUPLING_THEOREM_CONTRACT.csv"
UEM_1099 = OUT / "P8_Y5_R10_1099_EM_KINETIC_OWNER_THEOREM_ATTEMPT.csv"
SHARED_TAU_1402 = OUT / "P8_Y5_R10_1402_SHARED_TAU_TRANSFER_THEOREM_AUDIT.csv"
KX_ROWS_1035 = OUT / "P8_Y5_R10_1035_KX_FACTORIZATION_ROWS.csv"
R10_INPUT_1034 = OUT / "P8_Y5_R10_1034_PROJECTION_INPUT_PACK.csv"
NEWTON_SPINE_956 = OUT / "P8_Y5_R10_956_SOURCE_SIDE_GR_NEWTON_SPINE.csv"
NEWTON_LHS_956 = OUT / "P8_Y5_R10_956_LEFT_HAND_EH_NEWTON_GATE_MAP.csv"
NEWTON_LADDER_990 = OUT / "P8_Y5_R10_990_GR_NEWTON_REENTRY_LADDER.csv"
NEWTON_BLOCKERS_1339 = OUT / "P8_Y5_R10_1339_NEWTON_TRANSFER_BLOCKERS.csv"
PPN_GATE_1339 = OUT / "P8_Y5_R10_1339_PPN_COMPLETION_GATE.csv"

LIVE_CI_MAP = COEFF / "complete_Ci_parent_action_map_claim_rows.csv"
LIVE_EVALUATOR = COEFF / "Ci_residual_vector_evaluator_claim_rows.csv"
LIVE_LOCAL_GR = COEFF / "local_GR_claim_promotion_rows.csv"
LIVE_PPN = COEFF / "PPN_residual_vector_claim_rows.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1474_SOURCE_REGISTER.csv"
CI_MAP = OUT / "P8_Y5_R10_1474_COMPLETE_CI_PARENT_ACTION_MAP.csv"
DZ_OBLIGATIONS = OUT / "P8_Y5_R10_1474_CI_DOUBLE_ZERO_OBLIGATION_MAP.csv"
EVALUATOR_ROWS = OUT / "P8_Y5_R10_1474_CI_RESIDUAL_EVALUATOR_ROWS.csv"
EVALUATOR_SCHEMA = OUT / "P8_Y5_R10_1474_RESIDUAL_EVALUATOR_SCHEMA.csv"
LOCAL_COVERAGE = OUT / "P8_Y5_R10_1474_LOCAL_GR_COVERAGE_MATRIX.csv"
COUNTERMODELS = OUT / "P8_Y5_R10_1474_COUNTERMODEL_LEDGER.csv"
LIVE_GUARD = OUT / "P8_Y5_R10_1474_LIVE_IMPORT_GUARD.csv"
REDUCTION_GATES = OUT / "P8_Y5_R10_1474_REDUCTION_GATES.csv"
SIGNING_DECISION = OUT / "P8_Y5_R10_1474_PARENT_SIGNING_DECISION.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1474_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1474_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1474_VALIDATION.csv"

QUAR_CI_MAP = QUARANTINE / "COMPLETE_CI_PARENT_ACTION_MAP.csv"
QUAR_EVALUATOR = QUARANTINE / "CI_RESIDUAL_EVALUATOR_ROWS.csv"
BRANCH_CI_MAP = COEFF / "complete_Ci_parent_action_map_nonclaim_1474.csv"
BRANCH_EVALUATOR = COEFF / "Ci_residual_evaluator_rows_nonclaim_1474.csv"
BRANCH_SIGNING = COEFF / "complete_Ci_parent_action_signing_decision_1474.csv"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def truth(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
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
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def copy_branch(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)


def formalization_modified_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= START_TS)


def source_rows() -> list[dict[str, Any]]:
    local_sources = [
        ("SRC1474_0_1473_next", PREV_NEXT, "1473 handoff to complete C_i map or evaluator"),
        ("SRC1474_1_1473_validation", PREV_VALIDATION, "1473 validation baseline"),
        ("SRC1474_2_1473_theorem", PREV_THEOREM, "double-zero theorem attempt"),
        ("SRC1474_3_1473_premises", PREV_PREMISES, "double-zero premise audit"),
        ("SRC1474_4_1473_residuals", PREV_RESIDUALS, "executable residual vector"),
        ("SRC1474_5_1473_hooks", PREV_HOOKS, "residual hook map"),
        ("SRC1474_6_action_blocks", LOCAL_ACTION_511, "minimum parent local-GR action blocks"),
        ("SRC1474_7_fixed_point", LOCAL_FIXED_511, "fixed-point conditions"),
        ("SRC1474_8_residual_511", LOCAL_RESIDUAL_511, "minimum parent local-GR residual vector"),
        ("SRC1474_9_gate_511", LOCAL_GATES_511, "minimum parent local-GR gate tests"),
        ("SRC1474_10_vector_482", LOCAL_VECTOR_482, "existing local residual vector"),
        ("SRC1474_11_promotion_482", LOCAL_PROMOTION_482, "local residual promotion gates"),
        ("SRC1474_12_source_coupling", SOURCE_COUPLING_1229, "source coupling theorem contract"),
        ("SRC1474_13_wep_owner", WEP_OWNER_1077, "WEP coupling owner theorem attempt"),
        ("SRC1474_14_matter_coupling", MATTER_COUPLING_716, "matter-frame coupling derivation"),
        ("SRC1474_15_finite_coupling", FINITE_COUPLING_630, "finite coupling derivation"),
        ("SRC1474_16_Cparent", CPARENT_CONTRACT_1445, "C_parent coupling theorem contract"),
        ("SRC1474_17_UEM", UEM_1099, "EM kinetic owner theorem attempt"),
        ("SRC1474_18_tau", SHARED_TAU_1402, "shared tau transfer audit"),
        ("SRC1474_19_KX", KX_ROWS_1035, "K_X factorization rows"),
        ("SRC1474_20_R10_input", R10_INPUT_1034, "R10 projection input pack"),
        ("SRC1474_21_newton_spine", NEWTON_SPINE_956, "source-side GR/Newton spine"),
        ("SRC1474_22_newton_lhs", NEWTON_LHS_956, "left-hand EH/Newton gate map"),
        ("SRC1474_23_newton_ladder", NEWTON_LADDER_990, "GR/Newton reentry ladder"),
        ("SRC1474_24_newton_blockers", NEWTON_BLOCKERS_1339, "Newton transfer blockers"),
        ("SRC1474_25_ppn_gate", PPN_GATE_1339, "PPN completion gate"),
    ]
    return [
        {
            "source_id": source_id,
            "source_type": "local_file",
            "path_or_url": rel(path),
            "exists": path.exists(),
            "usage": usage,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for source_id, path, usage in local_sources
    ]


def ci_map_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "ci_id": "CI1474_0_alpha_EM",
            "coefficient": "C_alpha := ln Z_EM_eff or ln alpha_EM",
            "parent_action_block": "A511_3_extra_field_silence;A511_6_metric_readout",
            "action_slot": "Maxwell/EM kinetic and effective readout coefficient",
            "double_zero_test": "C_alpha(Phi0)=0 and partial_A C_alpha(Phi0)=0, modulo fixed representation constants",
            "observable_channels": "clock_alpha;WEP_alpha;R10_alpha_lambda;local_EM_PPN",
            "source_artifact": rel(UEM_1099),
            "source_anchor": "UEM1099_1_chain_rule;UEM1099_2_counterterm;UEM1099_3_verdict",
            "current_status": "THEOREM_TARGET_UNSIGNED",
            "route_if_not_proved": "ERV1473_0_alpha_EM_slope",
            "complete_for_1474": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "ci_id": "CI1474_1_source_weight",
            "coefficient": "C_source,A := delta w_A",
            "parent_action_block": "A511_2_universal_matter",
            "action_slot": "species/source multiplier in the Hilbert/coframe source",
            "double_zero_test": "delta w_A(Phi0)=0 and partial_B delta w_A(Phi0)=0, or all delta w_A lie in every local source/readout null kernel",
            "observable_channels": "Newton_source;WEP_eta;R10_source_leg;measured_GM",
            "source_artifact": rel(SOURCE_COUPLING_1229),
            "source_anchor": "THM1229_1_iff;THM1229_3_residual_vector",
            "current_status": "CONDITIONAL_ONLY",
            "route_if_not_proved": "ERV1473_1_source_weight",
            "complete_for_1474": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "ci_id": "CI1474_2_matter_frame_charge",
            "coefficient": "C_matter,Aa := Q_Aa",
            "parent_action_block": "A511_2_universal_matter;A511_6_metric_readout",
            "action_slot": "species-dependent matter-frame/mass/constant charge",
            "double_zero_test": "Q_Aa(Phi0)=0 with partial_B Q_Aa(Phi0)=0, or canonical mode absent",
            "observable_channels": "WEP_material;R10_test_source_charge;clock_mass_constants;Gdot",
            "source_artifact": rel(MATTER_COUPLING_716),
            "source_anchor": "MCD716_4_canonical_charge;MCD716_5_zero_condition;MCD716_6_current_corpus_verdict",
            "current_status": "ZERO_NOT_DERIVED",
            "route_if_not_proved": "ERV1473_2_matter_frame_charge",
            "complete_for_1474": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "ci_id": "CI1474_3_tau_readout_screen",
            "coefficient": "C_tau,a := Delta_tau_a",
            "parent_action_block": "A511_6_metric_readout;A511_5_boundary_reference",
            "action_slot": "clock/WEP/R10/orbit/boundary readout-time or screen map",
            "double_zero_test": "tau_a=T_a[D_parent] and partial_B(tau_a-T_a[D_parent])=0 for every arena a",
            "observable_channels": "clock_drift;WEP_projection;R10_tau;PPN_projection",
            "source_artifact": rel(SHARED_TAU_1402),
            "source_anchor": "DTT1402_5_no_arena_specific_screen;DTT1402_7_current_verdict",
            "current_status": "TRANSFER_BLOCKED",
            "route_if_not_proved": "ERV1473_3_tau_domain_screen",
            "complete_for_1474": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "ci_id": "CI1474_4_finite_mode_operator",
            "coefficient": "C_X := {Z_X,lambda_X,K_X,Qbar_source,Qbar_test}",
            "parent_action_block": "A511_3_extra_field_silence",
            "action_slot": "finite local response mode quadratic operator and source/test charges",
            "double_zero_test": "mode absent or Qbar_source=Qbar_test=0 to first order; otherwise Z_X>0, lambda_X, K_X, and charges are numeric source-backed",
            "observable_channels": "R10_alpha_lambda;finite_range_Newton;PPN_tail",
            "source_artifact": rel(KX_ROWS_1035),
            "source_anchor": "KXF1035_4_total",
            "current_status": "SYMBOLIC_ONLY_NUMERIC_MISSING",
            "route_if_not_proved": "ERV1473_4_finite_range_operator",
            "complete_for_1474": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "ci_id": "CI1474_5_PiM_mass_projector",
            "coefficient": "C_PiM := Pi_M-Pi_EH",
            "parent_action_block": "A511_5_boundary_reference;A511_6_metric_readout",
            "action_slot": "Hamiltonian/projected mass readout and measured-GM calibration",
            "double_zero_test": "Pi_M(Phi0)=Pi_EH and partial_A Pi_M(Phi0)=0 with no boundary/reference flux",
            "observable_channels": "measured_GM;Newton_source_normalization;mu_dot;orbital_calibration",
            "source_artifact": rel(NEWTON_LHS_956),
            "source_anchor": "LHG956_3_measured_GM_calibration;LHG956_4_constant_source_normalization",
            "current_status": "NOT_DERIVED",
            "route_if_not_proved": "ERV1473_5_PiM_measured_GM",
            "complete_for_1474": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "ci_id": "CI1474_6_metric_PPN_readout",
            "coefficient": "C_PPN,i := projection_i[g_readout-g_GR]",
            "parent_action_block": "A511_0_EH_core;A511_3_extra_field_silence;A511_6_metric_readout",
            "action_slot": "weak-field metric readout through O(U^2)",
            "double_zero_test": "gamma-1=0, beta-1=0, alpha_i=0, xi=0 or each residual is below bound from the same parent readout",
            "observable_channels": "gamma;beta;alpha1;alpha2;alpha3;xi;zeta_i",
            "source_artifact": rel(PPN_GATE_1339),
            "source_anchor": "PPN1339_0_gamma_beta;PPN1339_1_preferred_frame;PPN1339_3_readout_frame",
            "current_status": "NOT_FILLED",
            "route_if_not_proved": "ERV1473_6_metric_PPN_readout",
            "complete_for_1474": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "ci_id": "CI1474_7_transition_activation",
            "coefficient": "C_act := activation/local-cosmology transition functional",
            "parent_action_block": "A511_3_extra_field_silence;A511_4_domain_projector_selector",
            "action_slot": "operator-spectrum/source-scale/topological activation rule between local and cosmological regimes",
            "double_zero_test": "compact local branch gives C_act=0 and partial_A C_act=0 while FLRW/cosmology branch activates by parent-derived condition",
            "observable_channels": "ell_tr/L_cg;local_silence;cosmology_memory;galaxy_transition",
            "source_artifact": rel(LOCAL_FIXED_511),
            "source_anchor": "FP511_8_local_cosmology_transition_control",
            "current_status": "ACTION_DERIVED_TRANSITION_LAW_MISSING",
            "route_if_not_proved": "ERV1473_7_transition_activation",
            "complete_for_1474": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "ci_id": "CI1474_8_kappa_Geff",
            "coefficient": "C_kappa := d ln kappa_eff or d ln G_eff",
            "parent_action_block": "A511_1_kappa_topological",
            "action_slot": "local gravitational coupling/topological integration constant",
            "double_zero_test": "d kappa_eff=0 on connected local domains and partial_{t,r,A,lambda}G_eff=0 after measured-GM normalization",
            "observable_channels": "Gdot;radial_G;Newton_calibration;PPN_time_range",
            "source_artifact": rel(LOCAL_ACTION_511),
            "source_anchor": "A511_1_kappa_topological",
            "current_status": "TOPOLOGICAL_ROUTE_CONTRACT_NOT_PARENT_SIGNED_FOR_ALL_READOUTS",
            "route_if_not_proved": "ERV1474_8_kappa_Geff",
            "complete_for_1474": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "ci_id": "CI1474_9_domain_projector_stress",
            "coefficient": "C_D := projector/domain stress and STF selector leakage",
            "parent_action_block": "A511_4_domain_projector_selector",
            "action_slot": "domain/projector selector stress, preferred-frame, or source-normalization term",
            "double_zero_test": "X_D=0, Qcoh_D=0, projector stress=0, and partial_A of projector stress vanishes through PPN order",
            "observable_channels": "alpha1;alpha2;alpha3;xi;R11_source_normalization;Bianchi_stress",
            "source_artifact": rel(LOCAL_VECTOR_482),
            "source_anchor": "LRV_DOMAIN_R11_SOURCE_NORMALIZATION;LRV_PROJECTOR_STRESS_ACCOUNTING",
            "current_status": "RETAINED_DEBT",
            "route_if_not_proved": "ERV1474_9_domain_projector_stress",
            "complete_for_1474": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def obligation_rows(ci_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in ci_rows:
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "obligation_id": row["ci_id"].replace("CI1474", "DZO1474"),
                "ci_id": row["ci_id"],
                "coefficient": row["coefficient"],
                "zero_condition": row["double_zero_test"].split(" and ")[0],
                "first_variation_condition": "partial_A condition required by double-zero theorem",
                "parent_owner_required": row["parent_action_block"],
                "current_status": "OPEN_NONCLAIM",
                "if_closed": "route can be theorem-zero for listed observable channels",
                "if_not_closed": row["route_if_not_proved"],
                "source_artifact": row["source_artifact"],
                "source_anchor": row["source_anchor"],
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def evaluator_rows(ci_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    evaluator_specs = {
        "CI1474_0_alpha_EM": ("b_alpha_EM", "abs(b_alpha_EM*tau_clock), abs(DeltaQ*beta_source*b_alpha_EM*tau_WEP), alpha_R10(lambda)", "clock/WEP/R10/PPN alpha gates"),
        "CI1474_1_source_weight": ("delta_w_A", "norm(P_loc nabla_mu sum_A delta_w_A T_A^{mu nu})", "source-normalized Newton/WEP/R10 gates"),
        "CI1474_2_matter_frame_charge": ("Q_Aa", "max_Aa |Q_Aa| or material-pair contrasts", "WEP/R10/clock/Gdot gates"),
        "CI1474_3_tau_readout_screen": ("Delta_tau_a", "max_a |tau_a-T_a[D_parent]| in declared arena units", "shared tau/domain transfer gates"),
        "CI1474_4_finite_mode_operator": ("alpha_X(lambda)", "sup_lambda |alpha_X(lambda)|/alpha_bound(lambda)", "R10 and finite-range Newton/PPN gates"),
        "CI1474_5_PiM_mass_projector": ("delta_PiM", "abs(Pi_M-Pi_EH) plus first-variation/source-boundary flux", "measured-GM/Newton gates"),
        "CI1474_6_metric_PPN_readout": ("Delta_PPN_i", "vector of gamma-1,beta-1,alpha_i,xi,zeta_i", "PPN completion gates"),
        "CI1474_7_transition_activation": ("Delta_activation", "activation residual or missing ell_tr/L_cg law", "local/cosmology unification gate"),
        "CI1474_8_kappa_Geff": ("Delta_Geff", "partial_{t,r,A,lambda} ln G_eff", "Gdot/radial-G/Newton calibration gates"),
        "CI1474_9_domain_projector_stress": ("Delta_T_D", "projector stress and preferred-frame/source-normalization vector", "domain PPN/R11/Bianchi gates"),
    }
    rows: list[dict[str, Any]] = []
    for row in ci_rows:
        symbol, expression, gate = evaluator_specs[row["ci_id"]]
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "evaluator_id": row["ci_id"].replace("CI1474", "EVAL1474"),
                "ci_id": row["ci_id"],
                "residual_symbol": symbol,
                "evaluator_expression": expression,
                "required_inputs": "theorem_zero_certificate OR numeric coefficient/curve/vector with units, source path, sign convention, and no post-fit cancellation",
                "bound_or_gate": gate,
                "source_artifact": row["source_artifact"],
                "source_anchor": row["source_anchor"],
                "current_value": "MISSING_THEOREM_ZERO_OR_NUMERIC_INPUT",
                "passes_required_gate": False,
                "valid_for_Newton": False,
                "valid_for_PPN": False,
                "valid_for_local_GR": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def evaluator_schema_rows() -> list[dict[str, Any]]:
    required = [
        ("schema1474_0_ci_id", "ci_id", "stable C_i identifier", "required"),
        ("schema1474_1_residual_symbol", "residual_symbol", "symbol to score or theorem-zero", "required"),
        ("schema1474_2_value", "value_or_certificate", "numeric value, curve/vector, or theorem-zero certificate", "required"),
        ("schema1474_3_units", "units", "declared units compatible with gate", "required"),
        ("schema1474_4_source", "source_path_or_url", "local path or external DOI/URL for numeric/theorem source", "required"),
        ("schema1474_5_anchor", "source_anchor", "row/theorem/equation anchor", "required"),
        ("schema1474_6_gate", "bound_or_gate", "bound or proof gate to pass", "required"),
        ("schema1474_7_no_cancel", "no_cancellation_statement", "states no tuned cancellation unless parent identity proves it", "required"),
        ("schema1474_8_valid", "valid_for_claim", "true only after no missing theorem/numeric/source/unit fields", "required_false_until_complete"),
    ]
    return [
        {
            "schema_id": schema_id,
            "field": field,
            "meaning": meaning,
            "requirement": requirement,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for schema_id, field, meaning, requirement in required
    ]


def coverage_rows(ci_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in ci_rows:
        channels = row["observable_channels"]
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "coverage_id": row["ci_id"].replace("CI1474", "COV1474"),
                "ci_id": row["ci_id"],
                "blocks_clock": "clock" in channels,
                "blocks_WEP": "WEP" in channels or "eta" in channels,
                "blocks_R10": "R10" in channels,
                "blocks_Newton": "Newton" in channels or "measured_GM" in channels or "G_eff" in channels,
                "blocks_PPN": "PPN" in channels or "gamma" in channels or "alpha1" in channels or "xi" in channels or "Gdot" in channels,
                "blocks_local_GR": True,
                "coverage_statement": f"{row['ci_id']} routes to {row['route_if_not_proved']} if not double-zero proved",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CM1474_0_missing_Ci",
            "countermodel": "a coefficient not in the C_i inventory couples to readout after the double-zero theorem is claimed",
            "survives_why": "complete parent action map is still a workbench inventory, not a formal parent action proof",
            "killed_by_1474": False,
            "needed_to_kill": "derive C_i list from explicit S_parent grammar and variations",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CM1474_1_numeric_without_units",
            "countermodel": "a residual is numerically small only because units/normalization/source convention changed between arenas",
            "survives_why": "evaluator schema is written but not filled with source-backed values",
            "killed_by_1474": False,
            "needed_to_kill": "fill evaluator rows with units, sign convention, source anchor, and same-frame normalization",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CM1474_2_double_zero_by_bound_inversion",
            "countermodel": "empirical bound is used to choose C_i=0 rather than deriving C_i=0 from parent action",
            "survives_why": "1474 forbids promotion but parent proof is not yet supplied",
            "killed_by_1474": False,
            "needed_to_kill": "parent theorem-zero certificate or independent numeric prediction prior to comparison",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def live_guard_rows() -> list[dict[str, Any]]:
    guarded = [
        ("LG1474_0_Ci_map", LIVE_CI_MAP, "live complete C_i claim import"),
        ("LG1474_1_evaluator", LIVE_EVALUATOR, "live C_i residual evaluator claim rows"),
        ("LG1474_2_local_GR", LIVE_LOCAL_GR, "live local-GR claim promotion rows"),
        ("LG1474_3_PPN", LIVE_PPN, "live PPN claim rows"),
    ]
    return [
        {
            "guard_id": guard_id,
            "path": rel(path),
            "meaning": meaning,
            "exists_now": path.exists(),
            "would_write_in_1474": False,
            "status": "ABSENT_EXPECTED" if not path.exists() else "PRESENT_PREEXISTING_REVIEW_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for guard_id, path, meaning in guarded
    ]


def gate_rows(ci_rows: list[dict[str, Any]], obligations: list[dict[str, Any]], evaluators: list[dict[str, Any]], coverage: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ci_complete = len(ci_rows) >= 10 and all(truth(row["complete_for_1474"]) for row in ci_rows)
    all_mapped = {row["ci_id"] for row in ci_rows} == {row["ci_id"] for row in obligations} == {row["ci_id"] for row in evaluators}
    evaluator_nonclaim = all(not truth(row["passes_required_gate"]) and not truth(row["valid_for_claim"]) for row in evaluators)
    blocks_core = any(truth(row["blocks_Newton"]) for row in coverage) and any(truth(row["blocks_PPN"]) for row in coverage) and all(truth(row["blocks_local_GR"]) for row in coverage)
    return [
        {
            "gate_id": "GATE1474_0_Ci_inventory_written",
            "gate": "complete 1474 C_i inventory is written",
            "gate_pass": ci_complete,
            "claim_effect": "inventory only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1474_1_Ci_all_mapped",
            "gate": "every C_i has double-zero obligation and evaluator row",
            "gate_pass": all_mapped,
            "claim_effect": "routing complete for current inventory",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1474_2_parent_Ci_map_signed",
            "gate": "C_i map is derived from explicit parent action",
            "gate_pass": False,
            "claim_effect": "no complete-action claim",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1474_3_evaluators_nonclaim",
            "gate": "all evaluator rows remain nonclaim until filled",
            "gate_pass": evaluator_nonclaim,
            "claim_effect": "no numeric promotion",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1474_4_core_blockers_covered",
            "gate": "Newton/PPN/local-GR blockers are covered",
            "gate_pass": blocks_core,
            "claim_effect": "coverage not success",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1474_5_local_GR_claim",
            "gate": "local GR/Newton/PPN claim allowed",
            "gate_pass": False,
            "claim_effect": "explicitly forbidden in 1474",
            "valid_for_claim": False,
        },
    ]


def signing_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "SIGN1474_0_complete_Ci_map",
            "target": "complete C_i parent-action map and residual-vector evaluator rows",
            "Ci_inventory_written": True,
            "all_Ci_have_obligation_and_evaluator": True,
            "parent_action_derivation_signed": False,
            "evaluator_rows_filled": False,
            "theorem_zero_rows_filled": False,
            "Newton_transfer_allowed": False,
            "PPN_claim_allowed": False,
            "local_GR_claim_allowed": False,
            "decision": "REFUSE_COMPLETE_PARENT_ACTION_PROMOTION_KEEP_CI_EVALUATORS_NONCLAIM",
            "reason": "the inventory is complete for the current route, but the explicit parent action derivation and evaluator fills are still missing",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1474_0",
            "decision": "treat the C_i inventory as the active coupling spine",
            "why": "it gives a finite list of leak channels from parent action blocks to observables",
            "consequence": "future derivations should target named C_i rows instead of generic coupling language",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1474_1",
            "decision": "require either double-zero proof or evaluator fill",
            "why": "this mirrors engineering discipline: every path is either proved off or measured/bounded",
            "consequence": "no local-GR/Newton claim can bypass an unfilled C_i row",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1474_2",
            "decision": "next step should create a smoke evaluator",
            "why": "the schema is now explicit enough to test claim gates mechanically",
            "consequence": "1475 can compile the C_i rows into a pass/fail evaluator without long data runs",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1474_0_1475",
            "next_target": "1475-Y5-R10-RAB-Ci-residual-evaluator-smoke-runner-or-first-Ci-proof.md",
            "script": "scripts/Y5_R10_RAB_Ci_residual_evaluator_smoke_runner_or_first_Ci_proof.py",
            "objective": "build a smoke evaluator over the 1474 C_i rows that fails every unfilled theorem/numeric input, then optionally attack the first high-leverage C_i proof row",
            "include": "schema validation; no missing fields for claim rows; theorem-zero/numeric alternatives; Newton/PPN/local-GR aggregate gates",
            "exclude": "GitHub action; formalization-workbench edits; local-GR pass; WEP/R10/clock claim promotion; bound inversion",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def generated_csvs() -> list[Path]:
    return [
        SOURCE_REGISTER,
        CI_MAP,
        DZ_OBLIGATIONS,
        EVALUATOR_ROWS,
        EVALUATOR_SCHEMA,
        LOCAL_COVERAGE,
        COUNTERMODELS,
        QUAR_CI_MAP,
        QUAR_EVALUATOR,
        LIVE_GUARD,
        REDUCTION_GATES,
        SIGNING_DECISION,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]


def csv_parse_clean(paths: list[Path]) -> bool:
    try:
        return all(read_csv_rows(path) for path in paths)
    except Exception:
        return False


def branch_copies_exist() -> bool:
    return BRANCH_CI_MAP.exists() and BRANCH_EVALUATOR.exists() and BRANCH_SIGNING.exists()


def validation_rows(
    sources: list[dict[str, Any]],
    ci_rows: list[dict[str, Any]],
    obligations: list[dict[str, Any]],
    evaluators: list[dict[str, Any]],
    schema: list[dict[str, Any]],
    coverage: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    live_guard: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    signing: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    local_sources_exist = all(row["source_type"] != "local_file" or truth(row["exists"]) for row in sources)
    ci_sources_exist = all((ROOT / row["source_artifact"]).exists() for row in ci_rows)
    ci_inventory_complete = len(ci_rows) >= 10 and all(truth(row["complete_for_1474"]) for row in ci_rows)
    unique_ci = len({row["ci_id"] for row in ci_rows}) == len(ci_rows)
    map_sets_equal = {row["ci_id"] for row in ci_rows} == {row["ci_id"] for row in obligations} == {row["ci_id"] for row in evaluators} == {row["ci_id"] for row in coverage}
    obligations_open = all(row["current_status"] == "OPEN_NONCLAIM" and not truth(row["claim_allowed"]) for row in obligations)
    evaluator_sources_exist = all((ROOT / row["source_artifact"]).exists() for row in evaluators)
    evaluators_blocked = all(row["current_value"].startswith("MISSING") and not truth(row["passes_required_gate"]) and not truth(row["claim_allowed"]) for row in evaluators)
    schema_has_required = len(schema) >= 9 and all(row["requirement"] for row in schema)
    coverage_blocks_core = any(truth(row["blocks_Newton"]) for row in coverage) and any(truth(row["blocks_PPN"]) for row in coverage) and all(truth(row["blocks_local_GR"]) for row in coverage)
    countermodels_retained = all(not truth(row["killed_by_1474"]) for row in countermodels)
    live_paths_untouched = all(not truth(row["exists_now"]) and not truth(row["would_write_in_1474"]) for row in live_guard)
    safe_gate_pattern = truth(gates[0]["gate_pass"]) and truth(gates[1]["gate_pass"]) and not truth(gates[2]["gate_pass"]) and truth(gates[3]["gate_pass"]) and truth(gates[4]["gate_pass"]) and not truth(gates[5]["gate_pass"])
    signing_refuses = all(
        truth(row["Ci_inventory_written"])
        and truth(row["all_Ci_have_obligation_and_evaluator"])
        and not truth(row["parent_action_derivation_signed"])
        and not truth(row["evaluator_rows_filled"])
        and not truth(row["theorem_zero_rows_filled"])
        and not truth(row["Newton_transfer_allowed"])
        and not truth(row["PPN_claim_allowed"])
        and not truth(row["local_GR_claim_allowed"])
        for row in signing
    )
    generated_parse = csv_parse_clean(generated_csvs())
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_untouched = formalization_modified_count() == 0
    checks = [
        ("VAL1474_0_sources", local_sources_exist, "all cited local source paths exist"),
        ("VAL1474_1_ci_sources", ci_sources_exist, "all C_i source artifacts exist"),
        ("VAL1474_2_ci_inventory", ci_inventory_complete, "C_i inventory has complete_for_1474 rows"),
        ("VAL1474_3_unique_ci", unique_ci, "C_i identifiers are unique"),
        ("VAL1474_4_map_sets_equal", map_sets_equal, "C_i, obligation, evaluator, and coverage maps align"),
        ("VAL1474_5_obligations_open", obligations_open, "all double-zero obligations remain open nonclaim"),
        ("VAL1474_6_evaluator_sources", evaluator_sources_exist, "all evaluator source artifacts exist"),
        ("VAL1474_7_evaluators_blocked", evaluators_blocked, "all evaluator rows are missing theorem/numeric inputs and blocked"),
        ("VAL1474_8_schema", schema_has_required, "evaluator schema declares required fields"),
        ("VAL1474_9_coverage_blocks_core", coverage_blocks_core, "coverage matrix blocks Newton/PPN/local-GR explicitly"),
        ("VAL1474_10_countermodels", countermodels_retained, "all countermodels retained"),
        ("VAL1474_11_live_paths", live_paths_untouched, "critical live claim/import paths remain absent"),
        ("VAL1474_12_gate_pattern", safe_gate_pattern, "inventory/routing gates pass while claim gates fail"),
        ("VAL1474_13_signing_refuses", signing_refuses, "parent signing refuses complete-action/evaluator/local-GR promotion"),
        ("VAL1474_14_generated_csv_parse", generated_parse, "all generated 1474 CSVs parse cleanly"),
        ("VAL1474_15_branch_copies", branch_copies_exist(), "nonclaim branch/quarantine copies written"),
        ("VAL1474_16_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1474_17_formalization_untouched", formalization_untouched, f"formalization modified-file count since start={formalization_modified_count()}"),
    ]
    overall = all(result for _, result, _ in checks)
    checks.append(("VAL1474_18_overall", overall, "1474 builds the C_i parent-action map and evaluator routing without promoting claims"))
    generated = now()
    return [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "generated_utc": generated,
        }
        for check_id, result, detail in checks
    ]


def write_doc(
    sources: list[dict[str, Any]],
    ci_rows: list[dict[str, Any]],
    obligations: list[dict[str, Any]],
    evaluators: list[dict[str, Any]],
    coverage: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    signing: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> None:
    lines: list[str] = []
    lines.append("# 1474 - Y5 R10 RAB Complete Ci Parent Action Map Or Residual Vector Evaluator")
    lines.append("")
    lines.append("## Verdict")
    lines.append("- The active coupling spine is now a finite `C_i` inventory: alpha, source weights, matter-frame charge, tau/readout screens, finite-range mode, `Pi_M`, PPN readout, transition activation, `G_eff`, and domain/projector stress.")
    lines.append("- Every `C_i` has a double-zero proof obligation and a fallback evaluator row; none are parent-signed or score-ready.")
    lines.append("- This improves the GR/Newton route because local reduction now means closing or scoring named rows, not waving at 'the coupling'.")
    lines.append("")
    lines.append("## Complete C_i Map")
    lines.append("| ci_id | coefficient | current_status | route_if_not_proved |")
    lines.append("|---|---|---|---|")
    for row in ci_rows:
        lines.append(f"| {row['ci_id']} | {row['coefficient']} | {row['current_status']} | {row['route_if_not_proved']} |")
    lines.append("")
    lines.append("## Double-Zero Obligations")
    lines.append("| obligation_id | ci_id | current_status | if_not_closed |")
    lines.append("|---|---|---|---|")
    for row in obligations:
        lines.append(f"| {row['obligation_id']} | {row['ci_id']} | {row['current_status']} | {row['if_not_closed']} |")
    lines.append("")
    lines.append("## Evaluator Rows")
    lines.append("| evaluator_id | residual_symbol | current_value | bound_or_gate |")
    lines.append("|---|---|---|---|")
    for row in evaluators:
        lines.append(f"| {row['evaluator_id']} | {row['residual_symbol']} | {row['current_value']} | {row['bound_or_gate']} |")
    lines.append("")
    lines.append("## Coverage Matrix")
    lines.append("| ci_id | blocks_Newton | blocks_PPN | blocks_local_GR |")
    lines.append("|---|---:|---:|---:|")
    for row in coverage:
        lines.append(f"| {row['ci_id']} | {row['blocks_Newton']} | {row['blocks_PPN']} | {row['blocks_local_GR']} |")
    lines.append("")
    lines.append("## Gates")
    lines.append("| gate_id | gate_pass | claim_effect |")
    lines.append("|---|---:|---|")
    for row in gates:
        lines.append(f"| {row['gate_id']} | {row['gate_pass']} | {row['claim_effect']} |")
    lines.append("")
    lines.append("## Parent Signing Decision")
    for row in signing:
        lines.append(f"- `{row['decision_id']}`: `{row['decision']}` because {row['reason']}.")
    lines.append("")
    lines.append("## Decision Ledger")
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} - {row['consequence']}.")
    lines.append("")
    lines.append("## Validation")
    lines.append("| check_id | result | detail |")
    lines.append("|---|---|---|")
    for row in validation:
        lines.append(f"| {row['check_id']} | {row['result']} | {row['detail']} |")
    lines.append("")
    lines.append("## Source Register")
    lines.append("| source_id | exists | path_or_url | usage |")
    lines.append("|---|---:|---|---|")
    for row in sources:
        lines.append(f"| {row['source_id']} | {row['exists']} | `{row['path_or_url']}` | {row['usage']} |")
    lines.append("")
    lines.append("## Next Target")
    for row in next_target:
        lines.append(f"- `{row['next_target']}` via `{row['script']}`: {row['objective']}")
    lines.append("")
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    sources = source_rows()
    ci_rows = ci_map_rows()
    obligations = obligation_rows(ci_rows)
    evaluators = evaluator_rows(ci_rows)
    schema = evaluator_schema_rows()
    coverage = coverage_rows(ci_rows)
    countermodels = countermodel_rows()
    live_guard = live_guard_rows()
    gates = gate_rows(ci_rows, obligations, evaluators, coverage)
    signing = signing_decision_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(CI_MAP, ci_rows)
    write_csv(DZ_OBLIGATIONS, obligations)
    write_csv(EVALUATOR_ROWS, evaluators)
    write_csv(EVALUATOR_SCHEMA, schema)
    write_csv(LOCAL_COVERAGE, coverage)
    write_csv(COUNTERMODELS, countermodels)
    write_csv(QUAR_CI_MAP, ci_rows)
    write_csv(QUAR_EVALUATOR, evaluators)
    write_csv(LIVE_GUARD, live_guard)
    write_csv(REDUCTION_GATES, gates)
    write_csv(SIGNING_DECISION, signing)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_target)

    copy_branch(CI_MAP, BRANCH_CI_MAP)
    copy_branch(EVALUATOR_ROWS, BRANCH_EVALUATOR)
    copy_branch(SIGNING_DECISION, BRANCH_SIGNING)

    validation = validation_rows(sources, ci_rows, obligations, evaluators, schema, coverage, countermodels, live_guard, gates, signing)
    write_csv(VALIDATION, validation)
    write_doc(sources, ci_rows, obligations, evaluators, coverage, gates, signing, decisions, validation, next_target)
    print("Y5_R10_1474_complete_Ci_parent_action_map_residual_evaluator_nonclaim")


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1669"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1669-Y5-R2FR-Dq-leak-bound-source-pack-units-and-arena-projections.md"

SOURCE_FILES = {
    "1668_doc": ROOT / "1668-Y5-R2FR-constraint-first-Zphi-RAB-action-or-Dq-leak-source-pack.md",
    "1668_validation": OUT / "P8_Y5_BRR545_1668_VALIDATION.csv",
    "1668_source_pack": OUT / "P8_Y5_PARENT_QLOC_1668_DQ_LEAK_SOURCE_PACK_SCHEMA.csv",
    "1668_next_target": OUT / "P8_Y5_PARENT_QLOC_1668_NEXT_TARGET.csv",
    "local_bound_claims": LOCAL_BOUNDS / "local_bound_claims.csv",
    "local_residual_template": OUT / "MTS_local_residual_predictions_TEMPLATE.csv",
    "r10_formula_register": OUT / "P8_Y5_R10_1503_COUPLING_FORMULA_REGISTER.csv",
    "r10_bound_contract": OUT / "P8_Y5_R10_1503_COUPLING_CLOSURE_BOUND_ROW_CONTRACT.csv",
    "r10_verticality_contract": OUT / "P8_Y5_R10_1504_R10_RESIDUAL_VERTICALITY_CONTRACT.csv",
}

NEEDLES = {
    "1668_doc": ["Dq Leak Source Pack Schema", "1669-Y5-R2FR-Dq-leak-bound-source-pack-units-and-arena-projections.md"],
    "1668_validation": ["VAL1668_OVERALL", "PASS"],
    "1668_source_pack": ["DSP1668_7_Scg_envelope", "SCHEMA_READY_INPUTS_MISSING"],
    "1668_next_target": ["1669-Y5-R2FR-Dq-leak-bound-source-pack-units-and-arena-projections.md", "valid_for_claim"],
    "local_bound_claims": ["R10_fifth_force", "alpha(lambda)"],
    "local_residual_template": ["R10_fifth_force", "required_for_R10_R11"],
    "r10_formula_register": ["FORM1503_5_alpha_map", "alpha_a=-beta_a s_a c^2/(4 pi G_N Z_a)"],
    "r10_bound_contract": ["schema_version", "R10_COUPLING_CLOSURE_BOUND_1503"],
    "r10_verticality_contract": ["VC1504_5_acceptance", "BLOCKED"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1669_SOURCE_REGISTER.csv"
UNIT_CONVENTIONS = OUT / "P8_Y5_PARENT_QLOC_1669_DQ_LEAK_UNIT_CONVENTIONS.csv"
ARENA_PROJECTIONS = OUT / "P8_Y5_PARENT_QLOC_1669_ARENA_PROJECTION_MATRIX.csv"
R10_TEMPLATE = OUT / "P8_Y5_PARENT_QLOC_1669_R10_SOURCE_PACK_TEMPLATE.csv"
LOCAL_TEMPLATE = OUT / "P8_Y5_PARENT_QLOC_1669_PPN_WEP_CLOCK_ORBIT_SOURCE_PACK_TEMPLATE.csv"
BOUND_PLACEHOLDERS = OUT / "P8_Y5_PARENT_QLOC_1669_BOUND_COMPARISON_PLACEHOLDERS.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1669_DECISION.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1669_CLAIM_GATE.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1669_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1669_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    UNIT_CONVENTIONS,
    ARENA_PROJECTIONS,
    R10_TEMPLATE,
    LOCAL_TEMPLATE,
    BOUND_PLACEHOLDERS,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    UNIT_CONVENTIONS,
    ARENA_PROJECTIONS,
    R10_TEMPLATE,
    LOCAL_TEMPLATE,
    BOUND_PLACEHOLDERS,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

COPY_TARGETS = {
    ARENA_PROJECTIONS: [
        QUARANTINE / "DQ_LEAK_ARENA_PROJECTION_MATRIX_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_Dq_leak_arena_projection_matrix_nonclaim_1669.csv",
        QUEUE / "JR1669_DQ_LEAK_ARENA_PROJECTION_MATRIX_NONCLAIM.csv",
    ],
    R10_TEMPLATE: [
        QUARANTINE / "R10_SOURCE_PACK_TEMPLATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_R10_source_pack_template_nonclaim_1669.csv",
        QUEUE / "JR1669_R10_SOURCE_PACK_TEMPLATE_NONCLAIM.csv",
    ],
    LOCAL_TEMPLATE: [
        QUARANTINE / "PPN_WEP_CLOCK_ORBIT_SOURCE_PACK_TEMPLATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_PPN_WEP_clock_orbit_source_pack_template_nonclaim_1669.csv",
        QUEUE / "JR1669_PPN_WEP_CLOCK_ORBIT_SOURCE_PACK_TEMPLATE_NONCLAIM.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_nonclaim_1669.csv",
        QUEUE / "JR1669_CLAIM_GATE_NONCLAIM.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_nonclaim_1669.csv",
        QUEUE / "JR1669_NEXT_TARGET_NONCLAIM.csv",
    ],
}

LEAK_COMPONENTS = [
    {
        "source_pack_id": "DSP1668_0_Dq_Z",
        "component_id": "Dq_Z",
        "symbol": "Dq_Z_norm",
        "channel": "Z normal-form quotient leak",
        "unit_convention": "dimensionless only after q-basis and arena norm are parent-declared; otherwise arena-dependent",
        "missing_input": "q(Phi), Z basis, Dq[partial_Z], norm convention, arena projection",
        "first_theorem_zero_route": "prove Z is removed before q/readout or Dq[partial_Z]=0 by parent quotient construction",
        "first_bound_route": "derive finite Dq_Z_norm in observed-frame norm and project it into WEP/PPN/R10 rows",
    },
    {
        "source_pack_id": "DSP1668_1_Dq_phi",
        "component_id": "Dq_phi",
        "symbol": "Dq_phi_norm",
        "channel": "phi improvement quotient leak",
        "unit_convention": "dimensionless after phi normalization and boundary/domain convention; otherwise arena-dependent",
        "missing_input": "phi action, q dependence, Dq[partial_phi], boundary/domain convention",
        "first_theorem_zero_route": "prove phi is a pure improvement/auxiliary variable with no matter-visible readout after variation",
        "first_bound_route": "derive finite Dq_phi_norm and convert to clock/PPN/readout residuals",
    },
    {
        "source_pack_id": "DSP1668_2_Dq_RAB_Jq",
        "component_id": "Dq_RAB_Jq",
        "symbol": "Dq_RAB_or_Jq_norm",
        "channel": "R_AB/J_q cell-visible leak",
        "unit_convention": "dimensionless after cell-map normalization; otherwise arena-dependent",
        "missing_input": "q cell map or parent constraint that removes R_AB/J_q before matter/readout",
        "first_theorem_zero_route": "prove R_AB/J_q is a constrained internal cell object not visible to ordinary matter readout",
        "first_bound_route": "derive finite cell-visible leak norm and project to PPN/source-normalization rows",
    },
    {
        "source_pack_id": "DSP1668_3_C_qm",
        "component_id": "C_qm",
        "symbol": "C_qm=||DObs_e[Dq[v]]||",
        "channel": "geometry pullback/source stress",
        "unit_convention": "dimensionless coframe/Jacobian norm if variations are normalized to unit observed-frame displacement",
        "missing_input": "observed coframe functor, parent q map, local weak-field norm, v selection",
        "first_theorem_zero_route": "prove observed coframe descends through q and kills the retained vertical leak direction",
        "first_bound_route": "bound DObs_e[Dq[v]] directly and feed R0/R3/R4/R10 source-normalization rows",
    },
    {
        "source_pack_id": "DSP1668_4_S_direct",
        "component_id": "S_direct",
        "symbol": "S_direct",
        "channel": "direct matter/source dependence",
        "unit_convention": "E* forcing/action-gradient units until converted by a local Green/readout operator",
        "missing_input": "matter/source action domain exclusion or derivative bound",
        "first_theorem_zero_route": "prove ordinary matter action descends through the observed variables and has no fixed-coframe direct Dq vertex",
        "first_bound_route": "derive |delta_v S_matter| envelope and convert to WEP/source-charge residual",
    },
    {
        "source_pack_id": "DSP1668_5_S_boundary",
        "component_id": "S_boundary",
        "symbol": "S_boundary",
        "channel": "compact boundary/source-memory coupling",
        "unit_convention": "E* or boundary-charge units until boundary projector and arena conversion are fixed",
        "missing_input": "Q_X/B_X boundary charge, compact-support convention, projection norm",
        "first_theorem_zero_route": "prove boundary term is exact/proper/silent for local compact tests",
        "first_bound_route": "derive finite boundary-source envelope for alpha3, xi, orbital, and R10 rows",
    },
    {
        "source_pack_id": "DSP1668_6_marker",
        "component_id": "Dtheta_marker",
        "symbol": "Dtheta_marker_Dq_leak",
        "channel": "constants/material markers",
        "unit_convention": "dimensionless derivative of measured constants/material markers with respect to retained Dq direction",
        "missing_input": "mass/charge/clock constant owner or marker derivative bound",
        "first_theorem_zero_route": "prove material/constant markers are superselected or source-label forgotten in the parent matter functor",
        "first_bound_route": "derive finite marker derivative for WEP/clock/Gdot rows",
    },
    {
        "source_pack_id": "DSP1668_7_Scg_envelope",
        "component_id": "S_cg_envelope",
        "symbol": "S_cg_norm <= 0.5||T||_source*C_qm + S_direct + S_source_norm_extra + S_boundary",
        "channel": "absolute no-cancellation envelope",
        "unit_convention": "E* forcing units until every component and conversion operator is source-backed",
        "missing_input": "all component rows above, source stress norm, and no-cancellation conversion operator",
        "first_theorem_zero_route": "prove every positive component is theorem-zero in the same parent branch",
        "first_bound_route": "sum absolute component envelopes with no cancellation and compare each arena residual to its bound",
    },
]

ARENA_MAP = {
    "R0_identity_coframe_direct": {
        "projection_needs": "C_qm plus direct observed-coframe map for differential acceleration",
        "leak_components": "C_qm; Dq_Z; Dq_RAB_Jq",
        "projection_status": "MISSING_OBSERVED_COFRAME_DERIVATIVE",
        "arena_conversion": "eta_geom_AB = 2|a_geom(A)-a_geom(B)|/|a_geom(A)+a_geom(B)|",
    },
    "R1_WEP_source_charge": {
        "projection_needs": "S_direct, Dtheta_marker, and material/source tensor map",
        "leak_components": "S_direct; Dtheta_marker; S_cg_envelope",
        "projection_status": "MISSING_MATERIAL_SOURCE_MAP",
        "arena_conversion": "eta_source_AB from composition-dependent source response",
    },
    "R2_clock_redshift": {
        "projection_needs": "Dq_phi/readout marker derivative into clock frequency",
        "leak_components": "Dq_phi; Dtheta_marker; C_qm",
        "projection_status": "MISSING_CLOCK_READOUT_MAP",
        "arena_conversion": "Delta nu/nu = (1 + alpha_clock) Delta U/c^2",
    },
    "R3_gamma": {
        "projection_needs": "observed spatial metric response at O(c^-2)",
        "leak_components": "C_qm; Dq_RAB_Jq; Dq_Z",
        "projection_status": "MISSING_WEAK_FIELD_METRIC_RESPONSE",
        "arena_conversion": "gamma_minus_1 from g_ij = delta_ij(1 + 2 gamma U/c^2)",
    },
    "R4_beta": {
        "projection_needs": "observed temporal metric response at O(c^-4) after GM calibration",
        "leak_components": "C_qm; Dq_RAB_Jq; S_cg_envelope",
        "projection_status": "MISSING_POST_NEWTONIAN_SECOND_ORDER_RESPONSE",
        "arena_conversion": "beta_minus_1 from g_00 = -1 + 2U/c^2 - 2 beta U^2/c^4",
    },
    "R5_alpha1": {
        "projection_needs": "preferred-frame/vector leak in observed matter frame",
        "leak_components": "S_boundary; Dq_RAB_Jq; C_qm",
        "projection_status": "MISSING_VECTOR_FRAME_PROJECTION",
        "arena_conversion": "alpha1 extracted from g_0i/vector weak-field terms",
    },
    "R6_alpha2": {
        "projection_needs": "preferred-frame/vector anisotropy projection",
        "leak_components": "S_boundary; Dq_RAB_Jq; C_qm",
        "projection_status": "MISSING_ALPHA2_VECTOR_ANISOTROPY_MAP",
        "arena_conversion": "alpha2 preferred-frame coefficient",
    },
    "R7_alpha3": {
        "projection_needs": "momentum nonconservation/self-acceleration from boundary/domain exchange",
        "leak_components": "S_boundary; S_direct; Dtheta_marker",
        "projection_status": "MISSING_DOMAIN_EXCHANGE_ZERO_OR_BOUND",
        "arena_conversion": "alpha3-equivalent self-acceleration/momentum residual",
    },
    "R8_xi": {
        "projection_needs": "preferred-location/domain anisotropy coupling to external field",
        "leak_components": "S_boundary; Dq_RAB_Jq; Dtheta_marker",
        "projection_status": "MISSING_PREFERRED_LOCATION_PROJECTION",
        "arena_conversion": "xi extracted from anisotropic/domain coupling",
    },
    "R9_Gdot": {
        "projection_needs": "time derivative of measured GM/G_eff marker under Dq leak",
        "leak_components": "Dtheta_marker; S_direct; C_qm",
        "projection_status": "MISSING_LOCAL_TIME_DERIVATIVE_MAP",
        "arena_conversion": "d ln G_eff/dt or d ln mu_obs/dt",
    },
    "R10_fifth_force": {
        "projection_needs": "lambda, tau_R10, beta, source coupling, kinetic normalization, and alpha(lambda) curve",
        "leak_components": "Dq_Z; Dq_phi; Dq_RAB_Jq; C_qm; S_direct; S_boundary; Dtheta_marker",
        "projection_status": "MISSING_R10_FIELD_MAP_AND_BOUND_CURVE",
        "arena_conversion": "|sum_a alpha_a tau_R10_a(lambda_i) delta_w_a| <= alpha_bound(lambda_i)",
    },
    "R11_EH_operator_ledger": {
        "projection_needs": "non-EH operator coefficient vector and same-frame source normalization",
        "leak_components": "Dq_Z; Dq_phi; Dq_RAB_Jq; S_cg_envelope",
        "projection_status": "MISSING_OPERATOR_COEFFICIENT_VECTOR",
        "arena_conversion": "retained non-EH operator coefficients compared to EH-plus-Lambda target",
    },
}


def ensure_dirs() -> None:
    for directory_path in [OUT, QUARANTINE, BRANCH_RESIDUALS, QUEUE]:
        directory_path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def bool_string(value: object) -> str:
    return str(value).strip().lower()


def source_register_rows() -> list[dict[str, object]]:
    rows = []
    for source_id, path in SOURCE_FILES.items():
        text = read_text(path)
        needles = NEEDLES[source_id]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path.exists(),
                "needles_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "role": "1669 Dq leak unit/projection/source-pack input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def unit_convention_rows() -> list[dict[str, object]]:
    rows = []
    for component in LEAK_COMPONENTS:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_pack_id": component["source_pack_id"],
                "component_id": component["component_id"],
                "symbol": component["symbol"],
                "channel": component["channel"],
                "unit_convention": component["unit_convention"],
                "status": "UNIT_CONVENTION_STAGED_INPUTS_MISSING",
                "needed_source_inputs": component["missing_input"],
                "first_theorem_zero_route": component["first_theorem_zero_route"],
                "first_bound_route": component["first_bound_route"],
                "prediction_source_backed": False,
                "theorem_zero_closed": False,
                "accepted_for_scoring": False,
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def local_bound_rows() -> list[dict[str, str]]:
    return csv_rows(SOURCE_FILES["local_bound_claims"])


def arena_projection_rows(bounds: list[dict[str, str]]) -> list[dict[str, object]]:
    rows = []
    for bound in bounds:
        row_id = bound["row_id"]
        spec = ARENA_MAP[row_id]
        symbolic_bound = bound["upper_bound"] in {"alpha(lambda)", "symbolic"} or bound["upper_bound"] == ""
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "arena_row_id": row_id,
                "test_arena": bound["test_arena"],
                "observable": bound["observable"],
                "empirical_upper_bound": bound["upper_bound"],
                "empirical_units": bound["units"],
                "bound_reference": bound["reference_path_or_url"],
                "bound_source_recorded": True,
                "symbolic_bound_or_curve_required": symbolic_bound,
                "leak_components": spec["leak_components"],
                "projection_needs": spec["projection_needs"],
                "arena_conversion": spec["arena_conversion"],
                "projection_status": spec["projection_status"],
                "predicted_residual": "MISSING_NUMERIC_OR_THEOREM_ZERO",
                "comparison_status": "BLOCKED_PENDING_SOURCE_INPUTS",
                "arena_ready": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def r10_template_rows() -> list[dict[str, object]]:
    rows = []
    for component in LEAK_COMPONENTS:
        if component["component_id"] == "S_cg_envelope":
            parent_status = "CLOSURE_NONCLAIM_ENVELOPE_INPUTS_MISSING"
        else:
            parent_status = "CLOSURE_NONCLAIM_MISSING_R10_FIELD_MAP"
        rows.append(
            {
                "schema_version": "R10_COUPLING_CLOSURE_BOUND_1503",
                "same_parent_branch_id": BRANCH_ID,
                "component_id": component["component_id"],
                "lambda_value": "MISSING_R10_RANGE",
                "lambda_units": "m",
                "delta_w_a": "MISSING_DQ_LEAK_AMPLITUDE_OR_THEOREM_ZERO",
                "Z_a": "MISSING_KINETIC_NORMALIZATION_OR_THEOREM_ZERO",
                "s_a": "MISSING_SOURCE_COUPLING_OR_THEOREM_ZERO",
                "beta_a": "MISSING_MATTER_READOUT_COEFFICIENT_OR_THEOREM_ZERO",
                "alpha_predicted": "MISSING_NUMERIC_OR_THEOREM_ZERO",
                "tau_R10_a": "MISSING_FINITE_SOURCE_RESPONSE_OR_THEOREM_ZERO",
                "alpha_bound": "MISSING_DIGITIZED_ALPHA_LAMBDA_CURVE",
                "source_paths": "MISSING_PARENT_INPUTS_AND_R10_BOUND_CURVE",
                "parent_status": parent_status,
                "formula_reference": "FORM1503_5_alpha_map; FORM1503_6_R10_comparison",
                "current_failure_mode": "R10 cannot score until lambda, tau_R10, beta/s/Z, delta_w, and alpha(lambda) are all sourced or theorem-zero",
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def local_template_rows(bounds: list[dict[str, str]]) -> list[dict[str, object]]:
    rows = []
    for bound in bounds:
        row_id = bound["row_id"]
        if row_id == "R10_fifth_force":
            continue
        spec = ARENA_MAP[row_id]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "arena_row_id": row_id,
                "test_arena": bound["test_arena"],
                "observable": bound["observable"],
                "units": bound["units"],
                "empirical_bound": bound["upper_bound"],
                "bound_reference": bound["reference_path_or_url"],
                "required_leak_inputs": spec["leak_components"],
                "required_projection": spec["projection_needs"],
                "predicted_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
                "prediction_derivation_status": "SOURCE_PACK_TEMPLATE_NONCLAIM",
                "source_file": "MISSING_PARENT_Q_DQ_PROJECTION_INPUTS",
                "assumptions": "no-cancellation; same observed frame; compare against GR/null baseline when runnable",
                "comparison_status": "BLOCKED_PENDING_SOURCE_INPUTS",
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def bound_placeholder_rows(bounds: list[dict[str, str]]) -> list[dict[str, object]]:
    rows = []
    for bound in bounds:
        row_id = bound["row_id"]
        missing_curve = row_id == "R10_fifth_force"
        missing_operator = row_id == "R11_EH_operator_ledger"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "arena_row_id": row_id,
                "observable": bound["observable"],
                "bound_value": bound["upper_bound"],
                "bound_units": bound["units"],
                "bound_status": "CURVE_REQUIRED" if missing_curve else ("OPERATOR_LEDGER_REQUIRED" if missing_operator else "BOUND_SOURCE_RECORDED"),
                "predicted_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
                "prediction_units": bound["units"],
                "comparison_rule": "abs(predicted_value) <= bound_value after same-frame arena projection",
                "comparison_ready": False,
                "failure_mode_if_used_now": "WOULD_BE_PLACEHOLDER_OR_CLOSURE_CLAIM",
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def decision_rows() -> list[dict[str, object]]:
    rows = [
        (
            "D1669_0_pack_status",
            "DQ_LEAK_SOURCE_PACK_ARENA_READY_NONCLAIM",
            "1668 leak symbols now have unit conventions, source requirements, and R0-R11 projection placeholders",
            "do not score until parent-signed theorem-zero or numeric source rows exist",
        ),
        (
            "D1669_1_R10_status",
            "R10_REMAINS_CURVE_AND_COEFFICIENT_BLOCKED",
            "alpha(lambda), tau_R10, lambda, beta, source coupling, and kinetic normalization are all missing or symbolic",
            "use R10 template only as a nonclaim acquisition checklist",
        ),
        (
            "D1669_2_best_next_domino",
            "TARGET_CQM_OR_DQZ_FIRST",
            "C_qm and Dq_Z sit closest to observed coframe descent and therefore feed WEP, PPN, and R10 rather than one arena only",
            "attempt theorem-zero for observed coframe functor DObs_e[Dq[v]], and if it fails emit first finite C_qm/Dq_Z bound row",
        ),
        (
            "D1669_3_safety",
            "NO_LOCAL_GR_NEWTON_CLAIM",
            "a source pack is infrastructure, not a derivation of GR/Newton or an empirical pass",
            "keep all local claims false until bound comparison rows become real and pass gates",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for decision_id, decision, reason, next_action in rows
    ]


def claim_rows() -> list[dict[str, object]]:
    rows = [
        ("CG1669_0_Dq_numeric_or_zero", "each retained Dq leak has numeric source row or theorem-zero", False, "BLOCKED", "all retained leak rows still contain MISSING_* inputs"),
        ("CG1669_1_arena_projection", "each arena has source-backed projection from Dq leak to observable", False, "BLOCKED", "R0-R11 projection matrix is schema-only"),
        ("CG1669_2_R10", "R10 alpha(lambda) comparison can be scored", False, "NO_CLAIM", "R10 bound curve and parent coefficients missing"),
        ("CG1669_3_WEP_PPN_clock_orbit", "WEP/PPN/clock/orbital rows pass", False, "NO_CLAIM", "predicted residuals are placeholders"),
        ("CG1669_4_local_GR_Newton", "local GR/Newton reduction follows", False, "NO_CLAIM", "1669 only prepares leak bounds; it does not prove q_loc=0"),
        ("CG1669_5_public_claim", "public/local claim safe", False, "NO_CLAIM", "private checkpoint only"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": gate_pass,
            "status": status,
            "blocker": blocker,
            "local_gr_claim_allowed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, claim, gate_pass, status, blocker in rows
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1670-Y5-R2FR-Cqm-DqZ-observed-coframe-zero-or-first-finite-bound-row.md",
            "script": "scripts/Y5_R2FR_Cqm_DqZ_observed_coframe_zero_or_first_finite_bound_row.py",
            "objective": "try to prove DObs_e[Dq[v]]=0 for the retained C_qm/Dq_Z leak; if that fails, emit the first finite nonclaim C_qm/Dq_Z source row with arena projections",
            "success_condition": "either a parent-signed theorem-zero for C_qm/Dq_Z or a finite source-backed nonclaim row ready for WEP/PPN/R10 smoke comparison",
            "forbidden_shortcuts": "no cancellation; no invented Dq norm; no local GR/Newton/PPN/R10/WEP claim; no GitHub action",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        }
    ]


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)


def all_claim_flags_false(paths: list[Path]) -> bool:
    flag_names = {
        "accepted_for_scoring",
        "arena_ready",
        "claim_allowed",
        "claim_ready",
        "comparison_ready",
        "local_gr_claim_allowed",
        "prediction_source_backed",
        "score_allowed",
        "score_ready",
        "source_backed",
        "theorem_closed",
        "theorem_zero_closed",
        "valid_for_claim",
        "valid_for_mts_claim",
        "valid_prediction_row",
        "valid_for_runner",
    }
    for path in paths:
        for row in csv_rows(path):
            for flag_name in flag_names.intersection(row):
                if bool_string(row[flag_name]) == "true":
                    return False
    return True


def no_missing_marked_ready(paths: list[Path]) -> bool:
    readiness_flags = {
        "accepted_for_scoring",
        "arena_ready",
        "claim_allowed",
        "comparison_ready",
        "prediction_source_backed",
        "score_ready",
        "valid_for_claim",
        "valid_prediction_row",
    }
    for path in paths:
        for row in csv_rows(path):
            contains_missing = any("MISSING_" in value for value in row.values())
            if contains_missing and any(bool_string(row.get(flag, False)) == "true" for flag in readiness_flags):
                return False
    return True


def r10_template_has_contract_fields(rows: list[dict[str, object]]) -> bool:
    required = {
        "schema_version",
        "same_parent_branch_id",
        "component_id",
        "lambda_value",
        "lambda_units",
        "delta_w_a",
        "Z_a",
        "s_a",
        "beta_a",
        "alpha_predicted",
        "tau_R10_a",
        "alpha_bound",
        "source_paths",
        "parent_status",
        "valid_for_claim",
    }
    return required.issubset(rows[0])


def validation_rows(
    source_rows: list[dict[str, object]],
    unit_rows: list[dict[str, object]],
    arena_rows: list[dict[str, object]],
    r10_rows: list[dict[str, object]],
    local_rows_out: list[dict[str, object]],
    placeholders: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim: list[dict[str, object]],
    next_targets: list[dict[str, object]],
) -> list[dict[str, object]]:
    generated_csv_parse = True
    try:
        for generated_path in GENERATED:
            csv_rows(generated_path)
    except Exception:
        generated_csv_parse = False

    formalization_dirty = (
        any("1669" in path.name for path in FORMALIZATION.rglob("*1669*"))
        if FORMALIZATION.exists()
        else False
    )
    source_inputs_ok = all(row["path_exists"] and row["needles_found"] for row in source_rows)
    leak_units_complete = {row["component_id"] for row in unit_rows} == {component["component_id"] for component in LEAK_COMPONENTS}
    mapped_rows = {row["arena_row_id"] for row in arena_rows}
    all_arenas_mapped = mapped_rows == set(ARENA_MAP)
    all_rows_nonclaim = all_claim_flags_false(CLAIM_CHECKED)
    missing_safe = no_missing_marked_ready(CLAIM_CHECKED)
    r10_contract_ok = r10_template_has_contract_fields(r10_rows)
    local_rows_nonclaim = all(row["valid_for_claim"] is False and row["claim_allowed"] is False for row in local_rows_out)
    claim_gate_safe = all(row["gate_pass"] is False and row["claim_allowed"] is False for row in claim)
    branch_copies = all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" not in str(target))
    queue_copies = all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" in str(target))
    next_target_selected = next_targets[0]["next_target"] == "1670-Y5-R2FR-Cqm-DqZ-observed-coframe-zero-or-first-finite-bound-row.md"
    r10_blocked = all("MISSING_" in str(row["alpha_predicted"]) and row["valid_for_claim"] is False for row in r10_rows)
    no_numeric_claim = all(row["comparison_ready"] is False and row["claim_allowed"] is False for row in placeholders)

    checks = [
        ("VAL1669_0_sources_exist", source_inputs_ok, "all cited 1669 source paths exist and needles are present"),
        ("VAL1669_1_leak_units_complete", leak_units_complete, "all 1668 retained leak components have unit/source conventions"),
        ("VAL1669_2_all_arenas_mapped", all_arenas_mapped, "R0-R11 local arenas are mapped to Dq leak projection needs"),
        ("VAL1669_3_R10_contract_fields", r10_contract_ok, "R10 source-pack template includes the 1503 contract fields"),
        ("VAL1669_4_R10_remains_blocked", r10_blocked, "R10 rows remain blocked until parent coefficients and curve are real"),
        ("VAL1669_5_local_templates_nonclaim", local_rows_nonclaim, "PPN/WEP/clock/orbit source templates remain nonclaim"),
        ("VAL1669_6_bound_placeholders_nonclaim", no_numeric_claim, "bound comparison placeholders are not score-ready"),
        ("VAL1669_7_claim_gates_safe", claim_gate_safe, "all claim gates keep local claims false"),
        ("VAL1669_8_no_mts_claim_flags", all_rows_nonclaim, "all 1669 generated rows keep claim/no-score flags false"),
        ("VAL1669_9_missing_not_ready", missing_safe, "no row containing MISSING_* is marked source-backed, claim-ready, or score-ready"),
        ("VAL1669_10_next_target_selected", next_target_selected, "next target selects C_qm/Dq_Z theorem-zero or finite bound row"),
        ("VAL1669_11_csv_parse", generated_csv_parse, "all generated 1669 CSVs parse"),
        ("VAL1669_12_branch_copies", branch_copies, "branch/quarantine copies exist"),
        ("VAL1669_13_queue_copies", queue_copies, "acquisition queue nonclaim copies exist"),
        ("VAL1669_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1669_15_formalization_untouched", not formalization_dirty, "no 1669 outputs found under formalization-workbench"),
    ]
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1669_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1669 Dq leak source-pack units and arena projections validation",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row[column]).replace("\n", " ") for column in columns) + " |")
    return "\n".join(lines)


def write_doc(
    source_rows: list[dict[str, object]],
    unit_rows: list[dict[str, object]],
    arena_rows: list[dict[str, object]],
    r10_rows: list[dict[str, object]],
    local_rows_out: list[dict[str, object]],
    placeholders: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    r10_preview = r10_rows[:4]
    local_preview = local_rows_out[:8]
    text = f"""# 1669 - Dq Leak Bound Source Pack Units And Arena Projections

**Private status:** source-pack plumbing only. No `q_loc=0`, local-GR pass, Newton pass, PPN pass, R10 pass, WEP pass, clock pass, orbital pass, or public claim is made.

## Verdict

`1669` turns the retained `Dq` leak language from `1668` into an arena-ready acquisition pack.

```text
What improved:
each retained leak now has a unit convention,
each local arena R0-R11 has a projection requirement,
R10 has a 1503-compatible source-pack template,
and all rows are explicitly nonclaim/non-scoring.

What did not improve:
there is still no numeric Dq leak,
no parent-signed theorem-zero,
no R10 alpha(lambda) curve claim row,
and no local GR/Newton reduction.
```

This is useful because it stops the local branch from drifting into vibes. Every leak either has to die by theorem or enter the ring as a bounded residual.

## Source Register

{markdown_table(source_rows, ["source_id", "path", "path_exists", "needles_found", "role"])}

## Unit Conventions

{markdown_table(unit_rows, ["component_id", "symbol", "channel", "unit_convention", "status", "needed_source_inputs"])}

## Arena Projection Matrix

{markdown_table(arena_rows, ["arena_row_id", "observable", "empirical_upper_bound", "empirical_units", "leak_components", "projection_status", "predicted_residual"])}

## R10 Source Pack Template

The R10 rows are schema-valid but not claim-valid. The live comparison remains:

```text
alpha_a = - beta_a s_a c^2 / (4 pi G_N Z_a)
|sum_a alpha_a tau_R10_a(lambda_i) delta_w_a| <= alpha_bound(lambda_i)
```

{markdown_table(r10_preview, ["component_id", "lambda_value", "delta_w_a", "Z_a", "s_a", "beta_a", "alpha_predicted", "tau_R10_a", "alpha_bound", "parent_status"])}

## PPN/WEP/Clock/Orbit Template Preview

{markdown_table(local_preview, ["arena_row_id", "observable", "empirical_bound", "required_leak_inputs", "predicted_value", "comparison_status"])}

## Bound Comparison Placeholders

{markdown_table(placeholders, ["arena_row_id", "observable", "bound_value", "bound_status", "predicted_value", "comparison_ready", "claim_allowed"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Claim Gates

{markdown_table(claim, ["gate_id", "claim", "gate_pass", "status", "blocker"])}

## Next Target

{markdown_table(next_targets, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Working Interpretation

This is the clean empirical bridge, not the prize itself. The best next attack is `C_qm`/`Dq_Z`: either prove the observed coframe functor kills the retained vertical leak, or write the first finite nonclaim bound row. If `C_qm` goes to zero by theorem, several local arenas tighten at once. If it does not, we at least stop guessing and start measuring the leak.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    bounds = local_bound_rows()
    source_rows = source_register_rows()
    unit_rows = unit_convention_rows()
    arena_rows = arena_projection_rows(bounds)
    r10_rows = r10_template_rows()
    local_rows_out = local_template_rows(bounds)
    placeholders = bound_placeholder_rows(bounds)
    decisions = decision_rows()
    claim = claim_rows()
    next_targets = next_rows()

    for path, rows in [
        (SOURCE_REGISTER, source_rows),
        (UNIT_CONVENTIONS, unit_rows),
        (ARENA_PROJECTIONS, arena_rows),
        (R10_TEMPLATE, r10_rows),
        (LOCAL_TEMPLATE, local_rows_out),
        (BOUND_PLACEHOLDERS, placeholders),
        (DECISION, decisions),
        (CLAIM_GATE, claim),
        (NEXT_TARGET, next_targets),
    ]:
        write_csv(path, rows)

    copy_outputs()
    validation = validation_rows(source_rows, unit_rows, arena_rows, r10_rows, local_rows_out, placeholders, decisions, claim, next_targets)
    write_csv(VALIDATION, validation)
    write_doc(source_rows, unit_rows, arena_rows, r10_rows, local_rows_out, placeholders, decisions, claim, next_targets, validation)

    if any(row["result"] == "FAIL" for row in validation):
        raise SystemExit("1669 validation failed; see P8_Y5_BRR545_1669_VALIDATION.csv")

    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    print("1669 validation PASS")


if __name__ == "__main__":
    main()

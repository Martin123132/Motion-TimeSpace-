from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "2695"
BRANCH_ID = "Y5_R2FR_KAPPA_TOPOLOGICAL_SUPERSELECTION_PARENT_ADOPTION_OR_DRIFT_RESIDUAL_VALUES_2695"

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTAKE = ROOT / "source-intake"
RESIDUALS = SOURCE_INTAKE / "mts_residuals"
LOCAL_BOUNDS = SOURCE_INTAKE / "local_bounds"
WEP_RESIDUALS = SOURCE_INTAKE / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT = SOURCE_INTAKE / "source-weight"
RAB_QUEUE = SOURCE_INTAKE / "rab-sector" / "acquisition-queue"

DOC_PATH = ROOT / "2695-Y5-R2FR-kappa-topological-superselection-parent-adoption-or-drift-residual-values.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2695_SOURCE_REGISTER.csv",
    "parent_adoption_audit": RESIDUALS / "P8_Y5_R2FR_2695_KAPPA_TOPOLOGICAL_PARENT_ADOPTION_AUDIT.csv",
    "zero_form_derivation": RESIDUALS / "P8_Y5_R2FR_2695_ZERO_FORM_THREE_FORM_DERIVATION_CHECK.csv",
    "residual_requirements": RESIDUALS / "P8_Y5_R2FR_2695_KAPPA_RESIDUAL_VALUE_REQUIREMENTS_NONCLAIM.csv",
    "measured_gm_map": RESIDUALS / "P8_Y5_R2FR_2695_MEASURED_GM_CONTAMINATION_MAP.csv",
    "dryrun_cases": RESIDUALS / "P8_Y5_R2FR_2695_DRYRUN_CASES.csv",
    "dryrun_results": RESIDUALS / "P8_Y5_R2FR_2695_DRYRUN_RESULTS.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2695_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2695_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2695_NEXT_TARGET.csv",
    "project_status": RESIDUALS / "P8_Y5_R2FR_2695_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2695_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_parent_adoption_audit": LOCAL_BOUNDS / "kappa_topological_parent_adoption_audit_2695_NONCLAIM.csv",
    "local_kappa_residual_requirements": LOCAL_BOUNDS / "kappa_residual_value_requirements_2695_NONCLAIM.csv",
    "wep_kappa_residual_requirements": WEP_RESIDUALS / "kappa_residual_value_requirements_2695_NONCLAIM.csv",
    "source_weight_kappa_residual_requirements": SOURCE_WEIGHT / "KAPPA_RESIDUAL_VALUE_REQUIREMENTS_2695_NONCLAIM.csv",
    "rab_next": RAB_QUEUE / "JR2695_SOURCE_MEASURE_MEFF_FLUX_AFTER_KAPPA_NEXT.csv",
}

SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "source_id": "SRC2695_2694_DOC",
        "relative_path": "2694-Y5-R2FR-sector-positive-operator-silence-certificates-or-residual-values.md",
        "required_needles": ["NEXT2694_0_selected", "CERT2694_0_kappa", "VAL2694_OVERALL"],
        "purpose": "imports selected 2695 kappa target and no-claim ceiling",
    },
    {
        "source_id": "SRC2695_508_KAPPA",
        "relative_path": "508-constant-kappa-superselection-or-drift-residual.md",
        "required_needles": ["T508_1_topological_zeroform", "K508_3_metric_stress_silence", "KR508_0_time_drift"],
        "purpose": "imports topological zero-form/three-form route and kappa residual map",
    },
    {
        "source_id": "SRC2695_453_SUPERSELECTION",
        "relative_path": "453-global-coupling-superselection-parent-action-contract.md",
        "required_needles": ["P1_topological_zero_form", "GS0_configuration_factorization", "global_coupling_parent_derived"],
        "purpose": "imports global coupling superselection contract and parent-adoption failure",
    },
    {
        "source_id": "SRC2695_452_CONSTANT_KAPPA",
        "relative_path": "452-constant-universal-Geff-kappa-identity-attempt.md",
        "required_needles": ["CU1_global_coupling_status", "CU5_Bianchi_exchange_zero", "CU8_retained_residual_fallback"],
        "purpose": "imports constant universal G_eff/kappa identity and residual fallback",
    },
    {
        "source_id": "SRC2695_GS_CONTRACT",
        "relative_path": "source-intake/mts_residuals/P8_global_coupling_superselection_CONTRACT.csv",
        "required_needles": ["GS0_configuration_factorization", "GS4_no_range_radial_time_dependence", "GS7_scalar_branch_fallback"],
        "purpose": "imports machine-readable global/superselection kappa contract",
    },
    {
        "source_id": "SRC2695_CU_CONTRACT",
        "relative_path": "source-intake/mts_residuals/P8_constant_universal_Geff_kappa_CONTRACT.csv",
        "required_needles": ["CU1_global_coupling_status", "CU4_no_range_radial_running", "CU8_retained_residual_fallback"],
        "purpose": "imports constant universal kappa/G_eff contract rows",
    },
    {
        "source_id": "SRC2695_CONSTANT_GM_THEOREM",
        "relative_path": "source-intake/mts_residuals/P8_CONSTANT_GM_ZERO_THEOREM_ATTEMPT.csv",
        "required_needles": ["Z1_global_coupling_superselection", "Z5_no_radial_or_range_hair", "Z8_second_order_source_stability"],
        "purpose": "imports measured-GM zero theorem and open kappa/source blockers",
    },
    {
        "source_id": "SRC2695_DERIVATIVE_HAIR",
        "relative_path": "source-intake/mts_residuals/P8_CONSTANT_GM_DERIVATIVE_HAIR_GATE.csv",
        "required_needles": ["CGM0_master_identity", "CGM4_range_dependence", "retained_unfilled_no_claim"],
        "purpose": "imports derivative-hair scorecard for measured source normalization",
    },
    {
        "source_id": "SRC2695_LOCAL_RESIDUAL_INPUT",
        "relative_path": "source-intake/mts_residuals/P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv",
        "required_needles": ["P8_Geff_time_drift", "P8_range_dependence", "not_scoreable_prediction_missing"],
        "purpose": "imports currently unfilled local residual runner inputs",
    },
    {
        "source_id": "SRC2695_BOUND_MATRIX",
        "relative_path": "source-intake/mts_residuals/P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv",
        "required_needles": ["P8_Geff_time_drift", "P8_range_dependence", "score only"],
        "purpose": "imports bound/scoreability matrix for kappa residual rows",
    },
    {
        "source_id": "SRC2695_LOCAL_BOUNDS",
        "relative_path": "source-intake/local_bounds/local_bound_claims.csv",
        "required_needles": ["R1_WEP_source_charge", "R9_Gdot", "R10_fifth_force"],
        "purpose": "imports empirical locks touched by kappa drift/source/range hair",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def as_bool(value: bool) -> str:
    return "true" if value else "false"


def path_for(relative_path: str) -> Path:
    return ROOT / relative_path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            if not reader.fieldnames:
                return False, 0, "missing_header"
            return True, len(rows), "parsed"
    except Exception as exc:  # pragma: no cover
        return False, 0, f"{type(exc).__name__}: {exc}"


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        cells = [str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = path_for(spec["relative_path"])
        text = read_text(path)
        needles = list(spec["required_needles"])
        found = [needle for needle in needles if needle in text]
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "source_id": spec["source_id"],
                "relative_path": spec["relative_path"],
                "absolute_path": str(path),
                "exists": as_bool(path.exists()),
                "required_needles": ";".join(needles),
                "found_needles": ";".join(found),
                "missing_needles": ";".join(missing),
                "purpose": spec["purpose"],
                "valid_for_claim": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def parent_adoption_audit_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "KAD2695_0_configuration_factorization",
            "configuration category",
            "Q_parent = Q_dyn x K_top with kappa_eff in K_top, not in a local scalar bundle",
            "453/GS0 requires this but marks it not_parent_derived",
            "UNSIGNED_PARENT_FACTOR",
            "kappa_eff can still be a local scalar/source-normalization field",
            "dln_Geff_dt;partial_r_ln_Geff;partial_A_ln_Geff;alpha_kappa(lambda);delta_frame_source",
        ),
        (
            "KAD2695_1_field_content",
            "topological field content",
            "parent action contains metric-independent A_3 and zero-form kappa_eff in a global/topological sector",
            "508/K508_0 writes the clause; 453/P1 says promising future route, not in corpus",
            "CLAUSE_AVAILABLE_NOT_PARENT_SIGNED",
            "zero-gradient derivation has nowhere to live in the current parent action",
            "retain scalar-kappa branch and local-bound rows",
        ),
        (
            "KAD2695_2_variation_A3",
            "A_3 variation",
            "delta_{A_3} int kappa_eff dA_3 = -int d kappa_eff wedge delta A_3 + boundary",
            "mathematical variation is exact if A_3 is parent-owned and boundary variation is fixed/topological",
            "CONDITIONAL_ZERO_GRADIENT_DERIVATION",
            "without parent-owned A_3 this is a post-hoc plateau axiom",
            "d kappa_eff remains unowned",
        ),
        (
            "KAD2695_3_variation_kappa",
            "kappa companion equation",
            "delta_{kappa} S gives dA_3 plus only global/topological constraints",
            "508/K508_2 warns this must not become a local scalar force/source-current equation",
            "UNSIGNED_COMPANION_EQUATION",
            "the route becomes a dressed Lagrange multiplier patch",
            "new source/current/stress residual owner required",
        ),
        (
            "KAD2695_4_metric_stress_silence",
            "stress silence",
            "delta_g S_kappa_top = 0 in compact local exterior",
            "508/K508_3 states the needed metric independence but the current parent action does not sign it",
            "UNSIGNED_METRIC_STRESS_SILENCE",
            "constant kappa may be paid for by an unowned non-EH stress sector",
            "R11 operator/stress ledger stays active",
        ),
        (
            "KAD2695_5_matter_source_blindness",
            "source/species/range/frame blindness",
            "partial_A kappa_eff = partial_source kappa_eff = partial_m kappa_eff = partial_lambda kappa_eff = partial_frame kappa_eff = 0",
            "453/GS2-GS4 and 452/CU2-CU4 remain not_parent_derived",
            "UNSIGNED_SOURCE_BLINDNESS",
            "source-charge, range-hair, frame/domain coupling can survive even if a spacetime gradient is killed",
            "R1/R9/R10/R11 kappa residuals remain",
        ),
        (
            "KAD2695_6_boundary_projection_policy",
            "boundary and local projection silence",
            "boundary term from integration by parts is fixed/topological and cannot leak into measured mass/source flux",
            "508/K508_1 names the boundary condition; source-measure/Gauss closure is still held after kappa",
            "UNSIGNED_BOUNDARY_POLICY",
            "the zero-form derivation can move the problem into boundary mass flux",
            "source/Gauss M_eff branch remains next blocker",
        ),
        (
            "KAD2695_7_bianchi_exchange",
            "Bianchi/exchange term",
            "if d kappa_eff=0 and source blindness holds then P_loc[T_obs nabla kappa_eff]=0",
            "452/CU5 and 453/GS5 keep this as a conditional branch, not current promotion",
            "CONDITIONAL_ZERO_NOT_PROMOTED",
            "hidden exchange owner can impersonate conservation",
            "delta_kappa_source residual remains",
        ),
        (
            "KAD2695_8_verdict",
            "adoption verdict",
            "the topological route is a valid candidate parent mechanism but is not yet an earned theorem of current MTS",
            "all required adoption clauses are either conditional or unsigned",
            "PARENT_ADOPTION_FAILS_CURRENT_CORPUS",
            "no kappa/G_eff, measured-GM, Newton, PPN, local-GR, R10, WEP, clock, or orbital claim",
            "carry candidate clause only, or fill residual values",
        ),
    ]
    return [
        {
            "audit_id": row[0],
            "clause": row[1],
            "required_identity": row[2],
            "evidence_now": row[3],
            "current_status": row[4],
            "blocks_if_missing": row[5],
            "residual_if_missing": row[6],
            "parent_adopted": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def zero_form_derivation_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "ZFD2695_0_action",
            "write candidate sector",
            "S_kappa_top = int_M kappa_eff dA_3",
            "A_3 is a parent-owned topological three-form and kappa_eff is a zero-form sector variable",
            "candidate topological mechanism exists",
            "CONDITIONAL",
            True,
            False,
            "this is a clean parent-action clause, not evidence that old MTS already contained it",
        ),
        (
            "ZFD2695_1_integrate_by_parts",
            "vary A_3",
            "delta_A S = int kappa_eff d(delta A_3) = -int d kappa_eff wedge delta A_3 + boundary",
            "boundary variation is fixed/topological before source readout",
            "Euler equation can be d kappa_eff = 0",
            "MATHEMATICAL_STEP_VALID_CONDITIONAL",
            True,
            False,
            "this is the non-plateau route: the zero comes from a variational equation",
        ),
        (
            "ZFD2695_2_local_equation",
            "use arbitrary compact-support delta A_3",
            "d kappa_eff = 0",
            "compact local variations in a connected local domain are allowed and no boundary flux contributes",
            "kappa_eff is locally constant",
            "MATHEMATICAL_STEP_VALID_CONDITIONAL",
            True,
            False,
            "local constancy is conditional on the parent topological sector",
        ),
        (
            "ZFD2695_3_connected_domain",
            "convert closed zero-form to integration constant",
            "d kappa_eff = 0 on connected D implies kappa_eff = kappa_D",
            "domain label is global/superselected and not a local memory/range/source readout",
            "D_X kappa_eff = 0 for local spacetime directions",
            "CONDITIONAL_DOMAIN_CONSTANT",
            True,
            False,
            "domain superselection must not become preferred-location hair",
        ),
        (
            "ZFD2695_4_companion_equation",
            "vary kappa_eff",
            "delta_kappa S gives dA_3 plus any allowed global-sector constraint",
            "companion equation is global/topological rather than a local matter/source equation",
            "no scalar-tensor force is introduced",
            "UNSIGNED",
            False,
            False,
            "this is the main gap left by simply writing int kappa dA_3",
        ),
        (
            "ZFD2695_5_stress_silence",
            "vary metric/coframe",
            "delta_g S_kappa_top = 0",
            "the topological sector is metric independent or has an explicitly fixed subtraction",
            "no non-EH stress buys the constant",
            "UNSIGNED",
            False,
            False,
            "without this, kappa closure can reappear as an R11 operator/stress debt",
        ),
        (
            "ZFD2695_6_source_blindness",
            "act with source/material/range/frame selectors",
            "partial_A kappa_eff = partial_lambda kappa_eff = partial_frame kappa_eff = 0",
            "matter/source action sees only the same constant kappa_eff",
            "no source-charge or fifth-force kappa hair",
            "UNSIGNED",
            False,
            False,
            "killing spacetime gradient alone is not enough for local tests",
        ),
        (
            "ZFD2695_7_verdict",
            "derive-or-reject result",
            "S_kappa_top can derive d kappa_eff=0, but current MTS has not signed every parent clause",
            "all adoption clauses above must pass before claim credit",
            "candidate branch ready; claim branch blocked",
            "ROUTE_BUILT_NOT_PROMOTED",
            True,
            False,
            "this is progress, not a public win",
        ),
    ]
    return [
        {
            "step_id": row[0],
            "operation": row[1],
            "expression": row[2],
            "requirement": row[3],
            "result_if_requirement_met": row[4],
            "current_result": row[5],
            "mathematical_valid": as_bool(row[6]),
            "parent_signed": as_bool(row[7]),
            "valid_for_claim": "false",
            "notes": row[8],
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def residual_requirement_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "KRR2695_0_time_drift",
            "P8_Geff_time_drift",
            "dln_Geff_dt",
            "D_t",
            "Gdot_over_G",
            "9.6e-15",
            "yr^-1",
            "P8_time_drift_residual_or_zero.csv with separated G_eff, M_eff, epsilon_mu terms",
            "MISSING_TOPOLOGICAL_PARENT_ADOPTION_OR_NUMERIC_DRIFT",
            "KR508_0_time_drift;CGM1_time_drift;R9_Gdot",
        ),
        (
            "KRR2695_1_radial_hair",
            "P8_radial_source_hair",
            "partial_r_ln_Geff",
            "D_r",
            "gamma_minus_1;beta_minus_1;radial source hair",
            "zero radial hair or mapped local profile bound",
            "inverse_length_or_dimensionless_envelope",
            "P8_radial_mu_profile_or_zero.csv with source-normalized radius map",
            "MISSING_TOPOLOGICAL_PARENT_ADOPTION_OR_RADIAL_PROFILE",
            "KR508_1_radial_hair;CGM2_radial_hair",
        ),
        (
            "KRR2695_2_range_dependence",
            "P8_range_dependence",
            "alpha_kappa(lambda)",
            "D_lambda;finite_range",
            "R10_fifth_force",
            "verified alpha(lambda) curve or theorem-zero",
            "range-dependent",
            "R10_alpha_lambda_curve_MTS_source_normalization.csv with predicted and bound columns",
            "MISSING_TOPOLOGICAL_PARENT_ADOPTION_OR_ALPHA_CURVE",
            "KR508_2_range_dependence;CGM4_range_dependence;R10_fifth_force",
        ),
        (
            "KRR2695_3_species_source_charge",
            "P8_species_source_charge",
            "eta_source_AB;partial_A_ln_Geff",
            "D_A;Delta_AB",
            "R1_WEP_source_charge",
            "2.8e-15",
            "dimensionless",
            "P8_species_source_charge_residual_or_zero.csv with material/source assumptions",
            "MISSING_TOPOLOGICAL_PARENT_ADOPTION_OR_SOURCE_CHARGE_VALUE",
            "KR508_3_species_source_charge;GS3;CU3;R1_WEP_source_charge",
        ),
        (
            "KRR2695_4_frame_domain_split",
            "P8_frame_calibration_split",
            "delta_frame_source;partial_D_ln_Geff",
            "Delta_frame;D_domain",
            "WEP/clock/R11/domain rows",
            "one observed source frame or explicit residual below locks",
            "dimensionless",
            "P8_frame_source_split_residual_or_zero.csv with same-frame assumptions",
            "MISSING_TOPOLOGICAL_PARENT_ADOPTION_OR_FRAME_DOMAIN_VALUE",
            "KR508_4_frame_domain_split;CGM5_frame_domain_split",
        ),
        (
            "KRR2695_5_bianchi_exchange",
            "P8_Bianchi_kappa_exchange",
            "delta_kappa_source",
            "nabla_mu",
            "R4;R7;R9;R10;R11",
            "same-frame arbitrary-source conservation theorem or explicit exchange coefficient",
            "operator/source units",
            "P8_delta_kappa_source_exchange_residual.csv",
            "MISSING_TOPOLOGICAL_PARENT_ADOPTION_OR_EXCHANGE_COEFFICIENT",
            "KR508_5_Bianchi_exchange;CU5;GS5",
        ),
    ]
    return [
        {
            "residual_id": row[0],
            "component_id": row[1],
            "symbol": row[2],
            "derivative_channel": row[3],
            "observable_link": row[4],
            "target_bound_or_zero": row[5],
            "units": row[6],
            "required_artifact": row[7],
            "current_status": row[8],
            "source_anchor": row[9],
            "numeric_value_present": "false",
            "score_ready": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def measured_gm_map_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "MGM2695_0_master_identity",
            "mu_obs = G_eff M_eff(1+epsilon_mu)",
            "D_X ln mu_obs = D_X ln G_eff + D_X ln M_eff + D_X ln(1+epsilon_mu)",
            "kappa drift contaminates the measured source product and cannot be hidden in fitted GM",
            "Newton source normalization; PPN source rows",
            "KRR2695_0;KRR2695_1;KRR2695_2;KRR2695_3;KRR2695_4;KRR2695_5",
        ),
        (
            "MGM2695_1_time",
            "G_eff = kappa_eff c^4/(8 pi)",
            "dln_Geff_dt = dln_kappa_eff_dt",
            "local Gdot lock activates unless topological kappa closes or a numeric drift row is supplied",
            "R9_Gdot;clock/orbital drift",
            "KRR2695_0_time_drift",
        ),
        (
            "MGM2695_2_range",
            "G_eff(lambda) or Yukawa-like finite-range kappa hair",
            "alpha_kappa(lambda) must be zero by theorem or scored against R10 curve",
            "inverse-square law cannot be claimed from a symbolic constant-G sentence",
            "R10_fifth_force",
            "KRR2695_2_range_dependence",
        ),
        (
            "MGM2695_3_source",
            "kappa_eff(A, source, material)",
            "Delta_AB ln mu_obs includes partial_A ln G_eff",
            "direct coframe WEP is not enough if the active gravitational source charge varies by material/source label",
            "R1_WEP_source_charge;measured GM",
            "KRR2695_3_species_source_charge",
        ),
        (
            "MGM2695_4_frame_domain",
            "kappa_eff(frame, domain, boundary)",
            "Delta_frame ln mu_obs and partial_D ln G_eff survive",
            "constant in one representation is not automatically constant in the observed source/matter frame",
            "WEP;clock;R11;domain rows",
            "KRR2695_4_frame_domain_split",
        ),
        (
            "MGM2695_5_bianchi",
            "P_loc[T_obs nabla kappa_eff]",
            "Bianchi kills this only in the same-frame arbitrary-source branch with no hidden exchange owners",
            "source-normalization exchange can remain after EH algebra",
            "R4;R7;R9;R10;R11",
            "KRR2695_5_bianchi_exchange",
        ),
        (
            "MGM2695_6_verdict",
            "constant kappa is a prerequisite, not the whole Newton/GR proof",
            "even if kappa closes, M_eff/Gauss/source measure and non-EH operator rows remain",
            "kappa work can unlock the next gate but cannot itself promote local GR",
            "Newton;PPN;local_GR",
            "next_source_measure_Meff_flux_gate",
        ),
    ]
    return [
        {
            "contamination_id": row[0],
            "source_identity": row[1],
            "contamination_path": row[2],
            "if_kappa_not_constant": row[3],
            "affected_claim": row[4],
            "active_residuals": row[5],
            "decision": "block_claim_or_require_parent_zero/value",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    rows = [
        ("DRY2695_0_full_topological_parent", True, True, True, True, True, True, False, False, False, "CONDITIONAL_KAPPA_ZERO_ONLY_SOURCE_GAUSS_STILL_REQUIRED"),
        ("DRY2695_1_formula_only", True, False, True, True, True, False, False, False, False, "REJECT_PARENT_ADOPTION_UNSIGNED"),
        ("DRY2695_2_companion_missing", True, True, False, True, True, True, False, False, False, "REJECT_COMPANION_EQUATION_LOCAL_OR_MISSING"),
        ("DRY2695_3_stress_missing", True, True, True, False, True, True, False, False, False, "REJECT_UNOWNED_STRESS"),
        ("DRY2695_4_source_blind_missing", True, True, True, True, False, True, False, False, False, "REJECT_SOURCE_LABEL_HAIR"),
        ("DRY2695_5_boundary_missing", True, True, True, True, True, False, False, False, False, "REJECT_BOUNDARY_FLUX"),
        ("DRY2695_6_no_parent_no_values", False, False, False, False, False, False, False, False, False, "BLOCK_RESIDUAL_VALUES_MISSING"),
        ("DRY2695_7_residual_values_present", False, False, False, False, False, False, True, False, False, "NONCLAIM_SCOREABLE_RESIDUAL_BRANCH_ONLY"),
        ("DRY2695_8_cancellation_only", True, True, True, True, True, True, False, True, False, "REJECT_TUNED_CANCELLATION"),
        ("DRY2695_9_fitted_gm_backfill", True, True, True, True, True, True, False, False, True, "REJECT_FITTED_GM_BACKFILL"),
    ]
    return [
        {
            "case_id": row[0],
            "topological_clause_written": as_bool(row[1]),
            "topological_sector_in_parent": as_bool(row[2]),
            "companion_equation_global": as_bool(row[3]),
            "metric_stress_silent": as_bool(row[4]),
            "source_blind": as_bool(row[5]),
            "boundary_fixed": as_bool(row[6]),
            "residual_values_present": as_bool(row[7]),
            "cancellation_only": as_bool(row[8]),
            "fitted_gm_backfill": as_bool(row[9]),
            "expected_status": row[10],
            "expected_claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def evaluate_dryrun(case: dict[str, Any]) -> str:
    if case["cancellation_only"] == "true":
        return "REJECT_TUNED_CANCELLATION"
    if case["fitted_gm_backfill"] == "true":
        return "REJECT_FITTED_GM_BACKFILL"
    if case["topological_sector_in_parent"] == "false" and case["residual_values_present"] == "true":
        return "NONCLAIM_SCOREABLE_RESIDUAL_BRANCH_ONLY"
    if case["topological_sector_in_parent"] == "false" and case["topological_clause_written"] == "true":
        return "REJECT_PARENT_ADOPTION_UNSIGNED"
    if case["topological_sector_in_parent"] == "false":
        return "BLOCK_RESIDUAL_VALUES_MISSING"
    if case["companion_equation_global"] == "false":
        return "REJECT_COMPANION_EQUATION_LOCAL_OR_MISSING"
    if case["metric_stress_silent"] == "false":
        return "REJECT_UNOWNED_STRESS"
    if case["source_blind"] == "false":
        return "REJECT_SOURCE_LABEL_HAIR"
    if case["boundary_fixed"] == "false":
        return "REJECT_BOUNDARY_FLUX"
    return "CONDITIONAL_KAPPA_ZERO_ONLY_SOURCE_GAUSS_STILL_REQUIRED"


def dryrun_result_rows(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case in cases:
        actual = evaluate_dryrun(case)
        rows.append(
            {
                "case_id": case["case_id"],
                "expected_status": case["expected_status"],
                "actual_status": actual,
                "status_match": as_bool(actual == case["expected_status"]),
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2695_0_parent_sector", "topological kappa sector is actually in the parent action", "FAIL_PARENT_ADOPTION_UNSIGNED", "KAD2695_0;KAD2695_1;KAD2695_8"),
        ("CG2695_1_zero_gradient", "d kappa_eff=0 follows from parent A_3 variation", "PASS_CONDITIONAL_NOT_PROMOTED", "ZFD2695_1;ZFD2695_2"),
        ("CG2695_2_companion_stress", "kappa variation and metric variation introduce no local scalar force or stress", "FAIL_COMPANION_AND_STRESS_UNSIGNED", "ZFD2695_4;ZFD2695_5"),
        ("CG2695_3_source_blindness", "kappa carries no species/source/range/frame/domain labels", "FAIL_SOURCE_BLINDNESS_UNSIGNED", "KAD2695_5;ZFD2695_6"),
        ("CG2695_4_residual_values", "if parent zero fails, all drift/source/range/frame/domain values are sourced and scoreable", "FAIL_VALUES_MISSING", "KRR2695_0-KRR2695_5"),
        ("CG2695_5_source_gauss_after_kappa", "even with kappa controlled, M_eff is the conserved source/Gauss charge", "FAIL_HELD_NEXT_GATE", "MGM2695_6"),
        ("CG2695_6_verdict", "kappa branch proves local GR/Newton now", "CLAIM_BLOCKED", "all gates above"),
    ]
    return [
        {
            "gate_id": row[0],
            "pass_condition": row[1],
            "current_status": row[2],
            "evidence": row[3],
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC2695_0_zero_form_route",
            "ZERO_FORM_THREE_FORM_ROUTE_IS_MATH_VALID",
            "The action int kappa_eff dA_3 gives d kappa_eff=0 by A_3 variation if the parent owns A_3, kappa_eff, and boundary silence.",
            "REAL_PROGRESS",
            "keep as candidate parent mechanism",
        ),
        (
            "DEC2695_1_parent_adoption",
            "PARENT_ADOPTION_NOT_EARNED",
            "The current corpus still does not sign configuration factorization, companion equation, stress silence, source blindness, and boundary policy.",
            "NO_CLAIM",
            "do not call this a local-GR/Newton pass",
        ),
        (
            "DEC2695_2_residual_branch",
            "KAPPA_RESIDUALS_REMAIN_ACTIVE",
            "If kappa is not parent-topological/global, it must be carried as dln_Geff_dt, radial hair, alpha(lambda), source charge, frame/domain split, and Bianchi exchange rows.",
            "NONCLAIM_RESIDUALS",
            "fill values only if the parent clause is rejected",
        ),
        (
            "DEC2695_3_measured_GM",
            "MEASURED_GM_CANNOT_HIDE_KAPPA",
            "A fitted orbital GM cannot absorb derivative/source/range/frame dependence in G_eff.",
            "ANTI_CHEAT_GUARD",
            "score row by row or derive zero",
        ),
        (
            "DEC2695_4_best_route",
            "CARRY_CANDIDATE_KAPPA_CLAUSE_AND_ATTACK_SOURCE_MEASURE",
            "The useful leap is to carry the topological kappa sector as a candidate parent action clause while explicitly marking it unsigned, then test whether M_eff is a conserved source/Gauss charge.",
            "NEXT_ROUTE_SELECTED",
            "run 2696 source-measure/M_eff flux gate with kappa status imported as conditional",
        ),
    ]
    return [
        {
            "decision_id": row[0],
            "decision": row[1],
            "rationale": row[2],
            "status": row[3],
            "next_action": row[4],
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "NEXT2695_0_selected",
            "selected_conditional_route",
            "2696-Y5-R2FR-source-measure-Meff-flux-closure-after-conditional-kappa-gate.md",
            "scripts/Y5_R2FR_source_measure_Meff_flux_closure_after_conditional_kappa_gate_2696.py",
            "derive whether M_eff is the conserved parent source charge mapped to exterior Gauss/worldtube flux, importing kappa as a candidate topological parent clause rather than a claim",
            "M_eff=M_Hilbert=M_Gauss with no boundary/memory/source flux hair before orbital readout",
            "using orbital GM as premise; hiding kappa/source drift in fitted GM; promoting conditional kappa as public local-GR proof; GitHub action; formalization-workbench edits",
        ),
        (
            "NEXT2695_1_fallback",
            "fallback_if_topological_kappa_rejected",
            "2696b-Y5-R2FR-kappa-drift-source-range-residual-value-acquisition.md",
            "scripts/Y5_R2FR_kappa_drift_source_range_residual_value_acquisition_2696b.py",
            "fill dln_Geff_dt, partial_r_ln_Geff, alpha_kappa(lambda), source-charge, frame/domain, and Bianchi exchange values as nonclaim residual inputs",
            "all residual rows numeric/sourced/units-clean and scoreable while still nonclaim",
            "pretending missing residual values are zero",
        ),
    ]
    return [
        {
            "target_id": row[0],
            "selection_status": row[1],
            "target_doc": row[2],
            "target_script": row[3],
            "purpose": row[4],
            "acceptance_gate": row[5],
            "forbidden_shortcuts": row[6],
            "private_only": "true",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def project_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("STATUS2695_0_kappa_route", "kappa/G_eff", "CANDIDATE_TOPOLOGICAL_MECHANISM_BUILT_NOT_PARENT_CLAIMED", "d kappa_eff=0 can be derived from int kappa_eff dA_3 if parent-owned; current adoption unsigned", False, "carry as conditional or fill residual values"),
        ("STATUS2695_1_newton_source", "Newton/source normalization", "STILL_BLOCKED_BY_SOURCE_MEASURE_MEFF_FLUX", "constant kappa is only one prerequisite; source charge and Gauss flux remain", False, "run 2696 source-measure M_eff gate"),
        ("STATUS2695_2_local_bounds", "R1/R9/R10/R11 local tests", "ACTIVE_LOCKS_RETAINED", "Gdot, source charge, alpha(lambda), frame/domain and Bianchi exchange rows are still nonclaim", False, "do not score unless values or theorem-zero proof exist"),
        ("STATUS2695_3_project", "overall unified framework", "FORWARD_PROGRESS_NO_PUBLIC_CLAIM", "the kappa gap is sharpened into an exact parent contract rather than vague coupling language", False, "attack source measure next"),
        ("STATUS2695_4_github", "publication/GitHub", "NO_ACTION", "private checkpoint only", False, "no push"),
    ]
    return [
        {
            "status_id": row[0],
            "area": row[1],
            "current_state": row[2],
            "meaning": row[3],
            "claim_ready": as_bool(row[4]),
            "next_action": row[5],
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, path in BRANCH_OUTPUTS.items():
        ok, count, message = parse_csv(path)
        rows.append(
            {
                "branch_key": key,
                "absolute_path": str(path),
                "exists": as_bool(path.exists()),
                "csv_parse_ok": as_bool(ok),
                "row_count": count,
                "parse_message": message,
                "valid_for_claim": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def validation_rows(
    source_rows: list[dict[str, Any]],
    audit_rows: list[dict[str, Any]],
    derivation_rows: list[dict[str, Any]],
    residual_rows: list[dict[str, Any]],
    measured_gm_rows: list[dict[str, Any]],
    dryrun_results: list[dict[str, Any]],
    claim_gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC_PATH]
    sources_ok = all(row["exists"] == "true" and not row["missing_needles"] for row in source_rows)
    math_route_valid = any(row["step_id"] == "ZFD2695_2_local_equation" and row["mathematical_valid"] == "true" for row in derivation_rows)
    parent_not_promoted = any(
        row["audit_id"] == "KAD2695_8_verdict"
        and row["current_status"] == "PARENT_ADOPTION_FAILS_CURRENT_CORPUS"
        and row["parent_adopted"] == "false"
        for row in audit_rows
    )
    residuals_nonclaim = all(
        row["valid_for_claim"] == "false"
        and row["claim_allowed"] == "false"
        and row["numeric_value_present"] == "false"
        and row["score_ready"] == "false"
        for row in residual_rows
    )
    measured_gm_blocks_hiding = any(
        row["contamination_id"] == "MGM2695_0_master_identity" and "cannot be hidden" in row["if_kappa_not_constant"]
        for row in measured_gm_rows
    )
    dryrun_ok = all(row["status_match"] == "true" and row["claim_allowed"] == "false" for row in dryrun_results)
    claim_blocked = all(row["valid_for_claim"] == "false" and row["claim_allowed"] == "false" for row in claim_gates) and any(
        row["gate_id"] == "CG2695_6_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in claim_gates
    )
    csv_checks = {str(path): parse_csv(path) for path in list(OUTPUTS.values())[:-1]}
    branch_checks = {str(path): parse_csv(path) for path in BRANCH_OUTPUTS.values()}
    csv_ok = all(ok for ok, _, _ in csv_checks.values())
    branch_ok = all(ok for ok, _, _ in branch_checks.values())
    formalization_guard = all("formalization-workbench" not in str(path).lower() for path in output_paths)
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    next_target_ok = parse_csv(OUTPUTS["next_target"])[0] and "2696" in read_text(OUTPUTS["next_target"]) and "source_measure" in read_text(OUTPUTS["next_target"])
    no_public_claim = all("claim_allowed" not in row or row["claim_allowed"] == "false" for row in audit_rows + residual_rows + claim_gates)
    checks = [
        ("VAL2695_sources_exist_and_needles_found", sources_ok, "all cited source paths exist and required needles were found"),
        ("VAL2695_zero_form_derivation_math_valid", math_route_valid, "zero-form/three-form derivation of d kappa_eff=0 is mathematically valid conditional on parent ownership"),
        ("VAL2695_parent_adoption_not_promoted", parent_not_promoted, "current MTS parent adoption remains unsigned"),
        ("VAL2695_residual_requirements_nonclaim", residuals_nonclaim, "kappa residual rows remain nonclaim, nonnumeric, and not score-ready"),
        ("VAL2695_measured_GM_hiding_blocked", measured_gm_blocks_hiding, "measured GM cannot hide kappa derivative/source/range/frame dependence"),
        ("VAL2695_dryrun_refusals", dryrun_ok, "dry-run refuses formula-only, missing companion/stress/source/boundary, cancellation, and fitted-GM cases"),
        ("VAL2695_claim_gates_block_claims", claim_blocked, "claim gates block kappa/local-GR/Newton promotion"),
        ("VAL2695_csv_parse", csv_ok, f"parsed {len(csv_checks)} output CSVs"),
        ("VAL2695_branch_copies_parse", branch_ok, f"parsed {len(branch_checks)} branch-copy CSVs"),
        ("VAL2695_formalization_write_guard", formalization_guard, "no output path targets formalization-workbench"),
        ("VAL2695_pycache_absent_at_validation_time", pycache_absent, "scripts/__pycache__ absent when validation rows were built"),
        ("VAL2695_next_target_selected", next_target_ok, "2696 source-measure/M_eff target selected with kappa imported as conditional"),
        ("VAL2695_no_public_claim", no_public_claim, "no row allows a public or GitHub claim"),
    ]
    overall = all(ok for _, ok, _ in checks)
    rows = [
        {"check_id": check_id, "passed": as_bool(ok), "detail": detail, "timestamp_utc": stamp()}
        for check_id, ok, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL2695_OVERALL",
            "passed": as_bool(overall),
            "detail": "2695 builds the exact topological kappa candidate, refuses parent promotion, keeps residual values active, and selects source-measure/M_eff as the next conditional gate",
            "timestamp_utc": stamp(),
        }
    )
    return rows


def write_document(
    source_rows: list[dict[str, Any]],
    audit_rows: list[dict[str, Any]],
    derivation_rows: list[dict[str, Any]],
    residual_rows: list[dict[str, Any]],
    measured_gm_rows: list[dict[str, Any]],
    dry_cases: list[dict[str, Any]],
    dry_results: list[dict[str, Any]],
    claim_gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    status: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC_PATH.write_text(
        "\n".join(
            [
                "# 2695 - Y5/R2FR Kappa Topological Superselection Parent Adoption or Drift Residual Values",
                "",
                "## Private Verdict",
                "",
                "This checkpoint takes the best shot at the coupling gap. The clean mechanism is real: a parent topological zero-form/three-form sector",
                "",
                "`S_kappa_top = int_M kappa_eff dA_3`",
                "",
                "would derive `d kappa_eff=0` by varying `A_3`, provided `A_3`, `kappa_eff`, the companion equation, the boundary policy, and metric/source silence are all parent-owned.",
                "",
                "The route is therefore not rubbish and not hand-waving. But current MTS has not yet signed those parent clauses. So 2695 does not claim constant `G_eff`, Newton, PPN, local GR, R10, WEP, clock, orbital, GitHub, or public readiness. It promotes only a candidate parent-action mechanism and keeps the kappa drift/source/range/frame/domain residual rows alive.",
                "",
                "The useful forward leap is to carry this topological kappa sector as a conditional parent clause while attacking the next blocker: whether `M_eff` is the conserved source/Gauss/worldtube charge before orbital readout.",
                "",
                "## Source Register",
                "",
                markdown_table(source_rows),
                "",
                "## Kappa Topological Parent Adoption Audit",
                "",
                markdown_table(audit_rows),
                "",
                "## Zero-Form / Three-Form Derivation Check",
                "",
                markdown_table(derivation_rows),
                "",
                "## Kappa Residual Value Requirements",
                "",
                markdown_table(residual_rows),
                "",
                "## Measured-GM Contamination Map",
                "",
                markdown_table(measured_gm_rows),
                "",
                "## Dry-Run Cases",
                "",
                markdown_table(dry_cases),
                "",
                "## Dry-Run Results",
                "",
                markdown_table(dry_results),
                "",
                "## Claim Gates",
                "",
                markdown_table(claim_gates),
                "",
                "## Decisions",
                "",
                markdown_table(decisions),
                "",
                "## Next Target",
                "",
                markdown_table(next_target),
                "",
                "## Project Status Snapshot",
                "",
                markdown_table(status),
                "",
                "## Validation",
                "",
                markdown_table(validation),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    for path in [RESIDUALS, LOCAL_BOUNDS, WEP_RESIDUALS, SOURCE_WEIGHT, RAB_QUEUE]:
        path.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    audit_rows = parent_adoption_audit_rows()
    derivation_rows = zero_form_derivation_rows()
    residual_rows = residual_requirement_rows()
    measured_gm_rows = measured_gm_map_rows()
    dry_cases = dryrun_case_rows()
    dry_results = dryrun_result_rows(dry_cases)
    claim_gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    status = project_status_rows()

    write_csv(OUTPUTS["source_register"], source_rows)
    write_csv(OUTPUTS["parent_adoption_audit"], audit_rows)
    write_csv(OUTPUTS["zero_form_derivation"], derivation_rows)
    write_csv(OUTPUTS["residual_requirements"], residual_rows)
    write_csv(OUTPUTS["measured_gm_map"], measured_gm_rows)
    write_csv(OUTPUTS["dryrun_cases"], dry_cases)
    write_csv(OUTPUTS["dryrun_results"], dry_results)
    write_csv(OUTPUTS["claim_gates"], claim_gates)
    write_csv(OUTPUTS["decision_ledger"], decisions)
    write_csv(OUTPUTS["next_target"], next_target)
    write_csv(OUTPUTS["project_status"], status)

    write_csv(BRANCH_OUTPUTS["local_parent_adoption_audit"], audit_rows)
    write_csv(BRANCH_OUTPUTS["local_kappa_residual_requirements"], residual_rows)
    write_csv(BRANCH_OUTPUTS["wep_kappa_residual_requirements"], residual_rows)
    write_csv(BRANCH_OUTPUTS["source_weight_kappa_residual_requirements"], residual_rows)
    write_csv(BRANCH_OUTPUTS["rab_next"], next_target)

    branch_rows = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], branch_rows)

    validation = validation_rows(
        source_rows=source_rows,
        audit_rows=audit_rows,
        derivation_rows=derivation_rows,
        residual_rows=residual_rows,
        measured_gm_rows=measured_gm_rows,
        dryrun_results=dry_results,
        claim_gates=claim_gates,
    )
    write_csv(OUTPUTS["validation"], validation)
    write_document(
        source_rows=source_rows,
        audit_rows=audit_rows,
        derivation_rows=derivation_rows,
        residual_rows=residual_rows,
        measured_gm_rows=measured_gm_rows,
        dry_cases=dry_cases,
        dry_results=dry_results,
        claim_gates=claim_gates,
        decisions=decisions,
        next_target=next_target,
        status=status,
        validation=validation,
    )


if __name__ == "__main__":
    main()

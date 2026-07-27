from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1670"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1670-Y5-R2FR-Cqm-DqZ-observed-coframe-zero-or-first-finite-bound-row.md"

SOURCE_FILES = {
    "1669_doc": ROOT / "1669-Y5-R2FR-Dq-leak-bound-source-pack-units-and-arena-projections.md",
    "1669_validation": OUT / "P8_Y5_BRR545_1669_VALIDATION.csv",
    "1669_units": OUT / "P8_Y5_PARENT_QLOC_1669_DQ_LEAK_UNIT_CONVENTIONS.csv",
    "1669_arena": OUT / "P8_Y5_PARENT_QLOC_1669_ARENA_PROJECTION_MATRIX.csv",
    "1669_next": OUT / "P8_Y5_PARENT_QLOC_1669_NEXT_TARGET.csv",
    "1667_dq_tests": OUT / "P8_Y5_PARENT_QLOC_1667_DQ_ON_ZPHI_TESTS.csv",
    "1667_quotient": OUT / "P8_Y5_PARENT_QLOC_1667_QUOTIENT_MAP_AUDIT.csv",
    "1667_leaks": OUT / "P8_Y5_PARENT_QLOC_1667_RETAINED_DQ_LEAK_ROWS.csv",
    "1544_zero_audit": OUT / "P8_Y5_PARENT_QLOC_1544_CQM_ZERO_THEOREM_AUDIT.csv",
    "1544_provenance": OUT / "P8_Y5_PARENT_QLOC_1544_CQM_FINITE_PROVENANCE_REQUIREMENTS.csv",
    "1544_projection": OUT / "P8_Y5_PARENT_QLOC_1544_LOCAL_PROJECTION_CONTRACT.csv",
    "1155_coframe": OUT / "P8_Y5_R10_1155_SINGLE_OBSERVED_COFRAME_PROOF_AUDIT.csv",
    "1504_coframe_independence": OUT / "P8_Y5_R10_1504_OBSERVED_COFRAME_INDEPENDENCE_AUDIT.csv",
    "1519_coframe_tau": OUT / "P8_Y5_PARENT_FRAME_1519_COFRAME_TAU_LOCK_AUDIT.csv",
}

NEEDLES = {
    "1669_doc": ["best next attack is `C_qm`/`Dq_Z`", "VAL1669_OVERALL"],
    "1669_validation": ["VAL1669_OVERALL", "PASS"],
    "1669_units": ["Dq_Z_norm", "C_qm=||DObs_e[Dq[v]]||"],
    "1669_arena": ["R10_fifth_force", "MISSING_R10_FIELD_MAP_AND_BOUND_CURVE"],
    "1669_next": ["1670-Y5-R2FR-Cqm-DqZ-observed-coframe-zero-or-first-finite-bound-row.md", "no cancellation"],
    "1667_dq_tests": ["DQT1667_1_Z_normal_form", "MISSING_UNIFIED_Z_BASIS_AND_COMPONENT_LOCK"],
    "1667_quotient": ["QMA1667_6_verdict", "Q_NOT_COMPUTABLE_CURRENT_CORPUS"],
    "1667_leaks": ["DQL1667_0_Dq_Z", "RETAINED_NONCLAIM_DQ_LEAK_INPUT"],
    "1544_zero_audit": ["ZERO1544_6_verdict", "THEOREM_ZERO_NOT_CLOSED"],
    "1544_provenance": ["PROV1544_0_value", "MISSING_NUMERIC_VALUE_OR_INTERVAL"],
    "1544_projection": ["LPC1544_0_source_geometry", "BLOCKED_INPUTS_MISSING"],
    "1155_coframe": ["COF1155_0_conditional_chain_rule", "SINGLE_OBSERVED_COFRAME_NOT_DERIVED"],
    "1504_coframe_independence": ["OC1504_2_vertical_pullback", "NOT_PARENT_DERIVED"],
    "1519_coframe_tau": ["OCF1519_7_verdict", "COFRAME_TAU_LOCK_NOT_PROVED"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1670_SOURCE_REGISTER.csv"
CHAIN_RULE = OUT / "P8_Y5_PARENT_QLOC_1670_CQM_DQZ_CHAIN_RULE_THEOREM.csv"
ZERO_GATE = OUT / "P8_Y5_PARENT_QLOC_1670_ZERO_PROOF_GATE.csv"
PRODUCT_BOUND = OUT / "P8_Y5_PARENT_QLOC_1670_PRODUCT_BOUND_CONTRACT.csv"
FINITE_TEMPLATE = OUT / "P8_Y5_PARENT_QLOC_1670_FIRST_FINITE_ROW_TEMPLATE_NONCLAIM.csv"
ARENA_UPDATE = OUT / "P8_Y5_PARENT_QLOC_1670_ARENA_PROJECTION_UPDATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1670_DECISION.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1670_CLAIM_GATE.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1670_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1670_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    CHAIN_RULE,
    ZERO_GATE,
    PRODUCT_BOUND,
    FINITE_TEMPLATE,
    ARENA_UPDATE,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    CHAIN_RULE,
    ZERO_GATE,
    PRODUCT_BOUND,
    FINITE_TEMPLATE,
    ARENA_UPDATE,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

COPY_TARGETS = {
    CHAIN_RULE: [
        QUARANTINE / "CQM_DQZ_CHAIN_RULE_THEOREM_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_Cqm_DqZ_chain_rule_theorem_nonclaim_1670.csv",
        QUEUE / "JR1670_CQM_DQZ_CHAIN_RULE_THEOREM_NONCLAIM.csv",
    ],
    PRODUCT_BOUND: [
        QUARANTINE / "PRODUCT_BOUND_CONTRACT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_Cqm_DqZ_product_bound_contract_nonclaim_1670.csv",
        QUEUE / "JR1670_PRODUCT_BOUND_CONTRACT_NONCLAIM.csv",
    ],
    FINITE_TEMPLATE: [
        QUARANTINE / "FIRST_FINITE_ROW_TEMPLATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_Cqm_DqZ_first_finite_row_template_nonclaim_1670.csv",
        QUEUE / "JR1670_FIRST_FINITE_ROW_TEMPLATE_NONCLAIM.csv",
    ],
    ARENA_UPDATE: [
        QUARANTINE / "ARENA_PROJECTION_UPDATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_Cqm_DqZ_arena_projection_update_nonclaim_1670.csv",
        QUEUE / "JR1670_ARENA_PROJECTION_UPDATE_NONCLAIM.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_nonclaim_1670.csv",
        QUEUE / "JR1670_NEXT_TARGET_NONCLAIM.csv",
    ],
}

ARENA_PRIORITIES = [
    (
        "R0_identity_coframe_direct",
        "eta_WEP_direct_geometry",
        "primary",
        "C_qm and Dq_Z directly enter observed coframe differential acceleration if the source/readout map is common",
        "eta_geom_AB <= Pi_R0 * C_Obs_e * Dq_Z_norm plus source/readout residuals",
        "MISSING_PI_R0_AND_COBS_DQZ_INPUTS",
    ),
    (
        "R3_gamma",
        "gamma_minus_1",
        "primary",
        "spatial metric response is the cleanest weak-field coframe projection after Newton/source normalization",
        "|gamma-1| <= Pi_gamma * C_Obs_e * Dq_Z_norm plus R_AB/J_q and calibration residuals",
        "MISSING_WEAK_FIELD_METRIC_RESPONSE",
    ),
    (
        "R4_beta",
        "beta_minus_1",
        "primary",
        "second-order temporal metric response tests whether the same observed geometry survives beyond Poisson order",
        "|beta-1| <= Pi_beta * C_Obs_e * Dq_Z_norm plus S_cg/source-normalization residuals",
        "MISSING_POST_NEWTONIAN_SECOND_ORDER_RESPONSE",
    ),
    (
        "R10_fifth_force",
        "delta_G_or_fifth_force_yukawa",
        "primary",
        "short-range fifth-force comparison needs the same coframe derivative plus lambda/tau/beta/source coefficients",
        "|alpha_predicted(lambda)| <= Pi_R10(lambda) * C_Obs_e * Dq_Z_norm with full 1503 coefficient chain",
        "MISSING_R10_FIELD_MAP_AND_BOUND_CURVE",
    ),
    (
        "R2_clock_redshift",
        "alpha_clock_redshift",
        "secondary",
        "clock readout can inherit a common coframe leak even if Dq_phi/marker terms dominate",
        "|alpha_clock| <= Pi_clock * C_Obs_e * Dq_Z_norm plus marker/readout residuals",
        "MISSING_CLOCK_READOUT_MAP",
    ),
    (
        "R5_alpha1",
        "alpha1",
        "secondary",
        "preferred-frame vector terms can be induced if the coframe leak carries a frame direction",
        "|alpha1| <= Pi_alpha1 * C_Obs_e * Dq_Z_norm plus boundary/vector residuals",
        "MISSING_VECTOR_FRAME_PROJECTION",
    ),
    (
        "R6_alpha2",
        "alpha2",
        "secondary",
        "alpha2 is ultratight enough that even secondary coframe anisotropy must be bounded",
        "|alpha2| <= Pi_alpha2 * C_Obs_e * Dq_Z_norm plus boundary/vector residuals",
        "MISSING_ALPHA2_VECTOR_ANISOTROPY_MAP",
    ),
    (
        "R9_Gdot",
        "Gdot_over_G",
        "secondary",
        "time-varying coframe/source normalization can show up as local measured-G drift",
        "|Gdot/G| <= Pi_Gdot * d_t(C_Obs_e * Dq_Z_norm) plus marker/source residuals",
        "MISSING_LOCAL_TIME_DERIVATIVE_MAP",
    ),
]


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
                "role": "1670 C_qm/Dq_Z zero-proof or finite product-bound input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def chain_rule_rows() -> list[dict[str, object]]:
    rows = [
        (
            "CR1670_0_definition",
            "v_Z = a^A partial_ZA with ||v_Z||_Z=1 once the Z basis is parent-declared",
            "definition only",
            "needs unified Z basis and norm convention",
            "DEFINITION_STAGED",
            False,
        ),
        (
            "CR1670_1_quotient_derivative",
            "delta Q_vis = Dq|_Phi[v_Z]",
            "chain rule input",
            "requires computable parent quotient q(Phi)",
            "CONDITIONAL_NOT_COMPUTABLE",
            False,
        ),
        (
            "CR1670_2_coframe_derivative",
            "delta e_obs = DObs_e|_q[Dq|_Phi[v_Z]]",
            "exact Frechet/chain-rule identity",
            "requires e_obs=Obs_e(q(Phi)) and no shadow frame",
            "EXACT_CONDITIONAL_LEMMA",
            True,
        ),
        (
            "CR1670_3_product_bound",
            "C_qm_Z := ||delta e_obs||_loc <= ||DObs_e||_{q->e} ||Dq[v_Z]||_q",
            "operator-norm inequality",
            "requires q/e/Z/local norms in the same branch",
            "EXACT_CONDITIONAL_BOUND_FORM",
            True,
        ),
        (
            "CR1670_4_zero_routes",
            "C_qm_Z=0 if Dq[v_Z]=0 or DObs_e annihilates im(Dq[v_Z]) or Z is constraint-eliminated before q",
            "complete local zero-route classification for this channel",
            "requires one route parent-signed, not post-hoc",
            "CONDITIONAL_ZERO_ROUTES_ONLY",
            True,
        ),
        (
            "CR1670_5_counterguard",
            "Dq[v_Z]=0 for coframe is not enough if source/readout, constants, boundary, or shadow frame terms survive",
            "guard",
            "prevents beta/source/marker leakage from being hidden",
            "COUNTERMODEL_GUARD_ACTIVE",
            False,
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "chain_rule_id": chain_rule_id,
            "statement": statement,
            "math_role": math_role,
            "required_parent_input": required_parent_input,
            "status": status,
            "mathematically_valid_if_inputs_hold": mathematically_valid,
            "parent_signed": False,
            "theorem_zero_adopted": False,
            "prediction_source_backed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for chain_rule_id, statement, math_role, required_parent_input, status, mathematically_valid in rows
    ]


def zero_gate_rows() -> list[dict[str, object]]:
    rows = [
        (
            "ZG1670_0_q_parent",
            "q(Phi) is a parent-owned quotient map before matter/readout",
            "QMA1667_6 says q is not computable in the current corpus",
            "FAIL_CURRENT_LIVE_PROOF",
            "without q, Dq_Z is not a theorem object",
        ),
        (
            "ZG1670_1_Z_basis",
            "Z basis and component lock map Z to physical residual directions or remove it as auxiliary",
            "DQT1667_1 says unified Z basis and component lock are missing",
            "FAIL_CURRENT_LIVE_PROOF",
            "without the basis, Dq_Z_norm has no invariant size",
        ),
        (
            "ZG1670_2_kernel",
            "Dq[partial_Z]=0 or Z constraint-eliminated before q",
            "1667/1668 keep this as the best route but unsigned",
            "FAIL_CURRENT_LIVE_PROOF",
            "this is the clean kill route for C_qm_Z",
        ),
        (
            "ZG1670_3_observed_functor",
            "e_obs=Obs_e(q(Phi)) with no representative Weyl/disformal/shadow frame",
            "1155/1519/1544 say observed coframe descent is conditional only",
            "FAIL_CURRENT_LIVE_PROOF",
            "DObs_e can leak even if notation says one coframe",
        ),
        (
            "ZG1670_4_norm",
            "local q/e/Z operator norms are declared in the same source/source-dual space",
            "1544 provenance still has missing value, units, norm, and source path",
            "FAIL_CURRENT_LIVE_PROOF",
            "cannot turn product bound into a finite row",
        ),
        (
            "ZG1670_5_source_readout_silence",
            "source/readout/constants/boundary/projector maps do not reintroduce the Z leak",
            "1667 leak ledger retains Dsource, Dtheta, boundary/projector rows",
            "FAIL_CURRENT_LIVE_PROOF",
            "coframe-zero alone would not clear local GR/Newton",
        ),
        (
            "ZG1670_6_verdict",
            "C_qm_Z=0 current theorem",
            "chain-rule theorem is exact but parent signs are missing together",
            "THEOREM_ZERO_NOT_CLOSED_RETAIN_PRODUCT_BOUND",
            "move to product-bound/source-input acquisition",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "required_gate": required_gate,
            "evidence": evidence,
            "status": status,
            "effect": effect,
            "parent_signed": False,
            "theorem_zero_adopted": False,
            "prediction_source_backed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, required_gate, evidence, status, effect in rows
    ]


def product_bound_rows() -> list[dict[str, object]]:
    rows = [
        (
            "PB1670_0_DqZ",
            "Dq_Z_norm",
            "||Dq[partial_Z]||_q",
            "dimensionless after q/Z normalization",
            "MISSING_UNIFIED_Z_BASIS_AND_DQ_DERIVATIVE",
            "q(Phi), Z basis, Dq[partial_Z], q norm",
        ),
        (
            "PB1670_1_Cobs",
            "C_Obs_e",
            "||DObs_e||_{q->e}",
            "dimensionless operator norm after q/e normalization",
            "MISSING_OBSERVED_COFRAME_FUNCTOR_AND_NORM",
            "Obs_e(q), local coframe norm, no-shadow-frame certificate",
        ),
        (
            "PB1670_2_vZ",
            "N_Z",
            "||v_Z||_Z or selected unit direction",
            "dimensionless by convention if v_Z is unit-normalized",
            "MISSING_Z_DIRECTION_NORMALIZATION",
            "parent tangent direction and Z field units",
        ),
        (
            "PB1670_3_CqmZ",
            "C_qm_Z",
            "C_qm_Z <= C_Obs_e * Dq_Z_norm * N_Z",
            "coframe norm",
            "PRODUCT_BOUND_SCHEMA_READY_INPUTS_MISSING",
            "PB1670_0 through PB1670_2",
        ),
        (
            "PB1670_4_Sgeom",
            "S_geom_Z",
            "S_geom_Z <= 0.5*T_source_norm*C_qm_Z",
            "E* forcing units",
            "SOURCE_DUAL_PAIRING_MISSING",
            "T_source_norm and C_qm_Z in matched local dual norm",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "bound_id": bound_id,
            "symbol": symbol,
            "definition_or_bound": definition,
            "units": units,
            "current_status": status,
            "needed_source_inputs": needed,
            "theorem_zero_adopted": False,
            "finite_value_present": False,
            "prediction_source_backed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for bound_id, symbol, definition, units, status, needed in rows
    ]


def finite_template_rows() -> list[dict[str, object]]:
    rows = [
        (
            "FR1670_0_Cqm_DqZ_product",
            "C_qm_Z <= C_Obs_e * Dq_Z_norm * N_Z",
            "MISSING_NUMERIC_PRODUCT_FACTORS",
            "MISSING_COBS;MISSING_DQZ;MISSING_NZ",
            "R0;R3;R4;R10",
            "first finite row cannot be scored yet, but it is now a concrete acquisition target",
        ),
        (
            "FR1670_1_DqZ_theorem_zero_candidate",
            "Dq_Z_norm=0 if Z is quotient-vertical or constraint-eliminated before q",
            "MISSING_PARENT_THEOREM_ZERO",
            "MISSING_Q;MISSING_Z_BASIS;MISSING_CONSTRAINT_OR_KERNEL_PROOF",
            "R0;R3;R4;R10;R11",
            "preferred route because it removes the factor instead of bounding it",
        ),
        (
            "FR1670_2_Cobs_annihilator_candidate",
            "C_Obs_e_Z=0 if DObs_e annihilates the Z image",
            "MISSING_ANNIHILATOR_CERTIFICATE",
            "MISSING_OBS_E;MISSING_IMAGE_DQZ;MISSING_NO_SHADOW_FRAME",
            "R0;R3;R4;R10",
            "weaker than Dq_Z=0 but still mathematically clean",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "formula": formula,
            "current_status": current_status,
            "missing_inputs": missing_inputs,
            "priority_arenas": priority_arenas,
            "notes": notes,
            "candidate_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "units": "dimensionless/coframe norm after declared normalization",
            "source_paths": "MISSING_PARENT_Q_DQZ_OBS_E_SOURCE_PATHS",
            "derivation_status": "NONCLAIM_SOURCE_TEMPLATE",
            "theorem_zero_adopted": False,
            "finite_value_present": False,
            "prediction_source_backed": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for row_id, formula, current_status, missing_inputs, priority_arenas, notes in rows
    ]


def arena_update_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "arena_row_id": arena_row_id,
            "observable": observable,
            "priority": priority,
            "why_Cqm_DqZ_matters": why,
            "projection_bound_form": projection,
            "current_status": status,
            "required_inputs": "C_Obs_e; Dq_Z_norm; N_Z; arena response Pi; same-frame source/readout map; no-cancellation guard",
            "predicted_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "comparison_ready": False,
            "prediction_source_backed": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for arena_row_id, observable, priority, why, projection, status in ARENA_PRIORITIES
    ]


def decision_rows() -> list[dict[str, object]]:
    rows = [
        (
            "D1670_0_chain_rule",
            "CHAIN_RULE_DERIVED_CONDITIONALLY",
            "delta e_obs = DObs_e[Dq[v_Z]] and C_qm_Z <= C_Obs_e*Dq_Z_norm*N_Z are exact if q, Obs_e, Z basis, and norms are parent-owned",
            "keep the theorem as a conditional lemma, not a local-GR claim",
        ),
        (
            "D1670_1_zero_result",
            "ZERO_PROOF_FAILS_CURRENT_CORPUS",
            "q is not computable, Z basis/component lock is missing, observed coframe/no-shadow-frame is unsigned, and source/readout leakage remains",
            "retain C_qm_Z as a live product-bound channel",
        ),
        (
            "D1670_2_finite_row",
            "FINITE_ROW_TEMPLATE_STAGED_NOT_SCORED",
            "the first finite row is now a concrete product-factor acquisition target, but no numeric/theorem-zero factors exist",
            "do not run arena scoring until C_Obs_e, Dq_Z_norm, N_Z, and Pi_arena are real",
        ),
        (
            "D1670_3_next",
            "TARGET_DQZ_BASIS_OR_COBS_FIRST",
            "Dq_Z=0 is the cleanest kill route; C_Obs_e is the backup operator-norm route",
            "try to parent-sign the Z basis/kernel/constraint route before chasing numeric C_Obs_e",
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
        ("CG1670_0_Cqm_zero", "C_qm_Z=0 is proved", False, "NO_CLAIM", "parent q, Z basis/kernel, Obs_e, and source/readout silence are not signed together"),
        ("CG1670_1_DqZ_zero", "Dq_Z_norm=0 is proved", False, "NO_CLAIM", "Z basis/component lock and constraint-elimination route are unsigned"),
        ("CG1670_2_finite_bound", "finite C_qm_Z product bound can be scored", False, "BLOCKED", "C_Obs_e, Dq_Z_norm, N_Z, and arena Pi are missing"),
        ("CG1670_3_R10", "R10 smoke comparison can run", False, "NO_CLAIM", "R10 field map, tau, coefficients, and alpha(lambda) curve remain missing"),
        ("CG1670_4_PPN_WEP", "PPN/WEP/clock/orbit pass follows", False, "NO_CLAIM", "projection matrices and numeric residuals are placeholders"),
        ("CG1670_5_local_GR_Newton", "local GR/Newton reduction follows", False, "NO_CLAIM", "product-bound infrastructure is not a GR/Newton derivation"),
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
            "next_target": "1671-Y5-R2FR-DqZ-basis-kernel-or-Cobs-operator-norm-input.md",
            "script": "scripts/Y5_R2FR_DqZ_basis_kernel_or_Cobs_operator_norm_input.py",
            "objective": "try to parent-sign Dq_Z_norm=0 by constructing the Z basis/component lock and q-kernel/constraint route; if that fails, acquire C_Obs_e and Dq_Z_norm as separate nonclaim product factors",
            "success_condition": "either a parent-signed Dq_Z zero route or two separate source-ready factor rows for C_Obs_e and Dq_Z_norm with units and arena projections",
            "forbidden_shortcuts": "no invented product factors; no cancellation; no coframe-only local-GR claim; no GitHub action; no formalization-workbench edits",
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
        "claim_allowed",
        "claim_ready",
        "comparison_ready",
        "finite_value_present",
        "local_gr_claim_allowed",
        "numeric_value_present",
        "parent_signed",
        "prediction_source_backed",
        "score_allowed",
        "score_ready",
        "source_backed",
        "theorem_closed",
        "theorem_zero_adopted",
        "valid_for_claim",
        "valid_for_mts_claim",
        "valid_prediction_row",
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
        "claim_allowed",
        "comparison_ready",
        "finite_value_present",
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


def validation_rows(
    source_rows: list[dict[str, object]],
    chain: list[dict[str, object]],
    zero: list[dict[str, object]],
    product: list[dict[str, object]],
    finite: list[dict[str, object]],
    arena: list[dict[str, object]],
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
        any("1670" in path.name for path in FORMALIZATION.rglob("*1670*"))
        if FORMALIZATION.exists()
        else False
    )
    sources_ok = all(row["path_exists"] and row["needles_found"] for row in source_rows)
    chain_rule_present = any(row["chain_rule_id"] == "CR1670_3_product_bound" and row["status"] == "EXACT_CONDITIONAL_BOUND_FORM" for row in chain)
    zero_not_closed = any(row["gate_id"] == "ZG1670_6_verdict" and row["status"] == "THEOREM_ZERO_NOT_CLOSED_RETAIN_PRODUCT_BOUND" for row in zero)
    product_contract_present = any(row["bound_id"] == "PB1670_3_CqmZ" and "C_Obs_e * Dq_Z_norm" in row["definition_or_bound"] for row in product)
    finite_nonclaim = all(row["valid_for_claim"] is False and row["claim_allowed"] is False and row["candidate_value"] == "MISSING_NUMERIC_OR_THEOREM_ZERO" for row in finite)
    primary_arenas = {row["arena_row_id"] for row in arena if row["priority"] == "primary"}
    primary_arenas_ok = primary_arenas == {"R0_identity_coframe_direct", "R3_gamma", "R4_beta", "R10_fifth_force"}
    claim_gate_safe = all(row["gate_pass"] is False and row["claim_allowed"] is False for row in claim)
    branch_copies = all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" not in str(target))
    queue_copies = all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" in str(target))
    next_target_selected = next_targets[0]["next_target"] == "1671-Y5-R2FR-DqZ-basis-kernel-or-Cobs-operator-norm-input.md"

    checks = [
        ("VAL1670_0_sources_exist", sources_ok, "all cited 1670 source paths exist and needles are present"),
        ("VAL1670_1_chain_rule_bound", chain_rule_present, "C_qm/Dq_Z chain-rule product bound is written"),
        ("VAL1670_2_zero_not_closed", zero_not_closed, "C_qm_Z theorem-zero is not claimed"),
        ("VAL1670_3_product_contract", product_contract_present, "product-bound contract has C_Obs_e and Dq_Z factors"),
        ("VAL1670_4_finite_rows_nonclaim", finite_nonclaim, "finite row templates remain nonclaim with missing numeric/theorem-zero value"),
        ("VAL1670_5_primary_arenas", primary_arenas_ok, "R0, R3, R4, and R10 are marked primary C_qm/Dq_Z arenas"),
        ("VAL1670_6_claim_gate_safe", claim_gate_safe, "all claim gates keep local claims false"),
        ("VAL1670_7_no_mts_claim_flags", all_claim_flags_false(CLAIM_CHECKED), "all 1670 generated rows keep claim/no-score flags false"),
        ("VAL1670_8_missing_not_ready", no_missing_marked_ready(CLAIM_CHECKED), "no row containing MISSING_* is marked source-backed, claim-ready, or score-ready"),
        ("VAL1670_9_next_target_selected", next_target_selected, "next target selects Dq_Z basis/kernel or C_Obs operator norm input"),
        ("VAL1670_10_csv_parse", generated_csv_parse, "all generated 1670 CSVs parse"),
        ("VAL1670_11_branch_copies", branch_copies, "branch/quarantine copies exist"),
        ("VAL1670_12_queue_copies", queue_copies, "acquisition queue nonclaim copies exist"),
        ("VAL1670_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1670_14_formalization_untouched", not formalization_dirty, "no 1670 outputs found under formalization-workbench"),
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
            "check_id": "VAL1670_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1670 C_qm/Dq_Z coframe-zero or first finite product-bound validation",
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
    chain: list[dict[str, object]],
    zero: list[dict[str, object]],
    product: list[dict[str, object]],
    finite: list[dict[str, object]],
    arena: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 1670 - Cqm/DqZ Observed-Coframe Zero Or First Finite Bound Row

**Private status:** exact conditional derivation plus nonclaim product-bound scaffold. No `q_loc=0`, local-GR pass, Newton pass, PPN pass, R10 pass, WEP pass, clock pass, orbital pass, or public claim is made.

## Verdict

The clean theorem route is real but **not parent-signed**:

```text
v_Z = a^A partial_ZA
delta e_obs = DObs_e|_q [ Dq|_Phi[v_Z] ]
C_qm_Z <= C_Obs_e * Dq_Z_norm * N_Z

Therefore C_qm_Z = 0 if:
1. Dq[v_Z] = 0,
2. DObs_e annihilates im(Dq[v_Z]), or
3. Z is constraint-eliminated before q exists.
```

The current corpus does not prove any of those routes. So the honest result is: `C_qm/Dq_Z` is now reduced to a **product-bound acquisition problem**, not a vague coupling problem.

## Source Register

{markdown_table(source_rows, ["source_id", "path", "path_exists", "needles_found", "role"])}

## Chain-Rule Theorem

{markdown_table(chain, ["chain_rule_id", "statement", "math_role", "required_parent_input", "status", "mathematically_valid_if_inputs_hold"])}

## Zero-Proof Gate

{markdown_table(zero, ["gate_id", "required_gate", "evidence", "status", "effect"])}

## Product-Bound Contract

{markdown_table(product, ["bound_id", "symbol", "definition_or_bound", "units", "current_status", "needed_source_inputs"])}

## First Finite Row Template

{markdown_table(finite, ["row_id", "formula", "current_status", "missing_inputs", "priority_arenas", "candidate_value"])}

## Arena Projection Update

{markdown_table(arena, ["arena_row_id", "observable", "priority", "projection_bound_form", "current_status", "predicted_value"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Claim Gates

{markdown_table(claim, ["gate_id", "claim", "gate_pass", "status", "blocker"])}

## Next Target

{markdown_table(next_targets, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Working Interpretation

This is a good narrowing, not a defeat. `C_qm` is no longer a ghost word. It is either killed by `Dq_Z=0`, killed by an observed-coframe annihilator, or bounded by the product `C_Obs_e * Dq_Z_norm * N_Z`. The least-scrutiny route is still the first one: prove the Z direction is not visible to the quotient at all. If that fails, we acquire the product factors one at a time and make the local branch empirically accountable.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    source_rows = source_register_rows()
    chain = chain_rule_rows()
    zero = zero_gate_rows()
    product = product_bound_rows()
    finite = finite_template_rows()
    arena = arena_update_rows()
    decisions = decision_rows()
    claim = claim_rows()
    next_targets = next_rows()

    for path, rows in [
        (SOURCE_REGISTER, source_rows),
        (CHAIN_RULE, chain),
        (ZERO_GATE, zero),
        (PRODUCT_BOUND, product),
        (FINITE_TEMPLATE, finite),
        (ARENA_UPDATE, arena),
        (DECISION, decisions),
        (CLAIM_GATE, claim),
        (NEXT_TARGET, next_targets),
    ]:
        write_csv(path, rows)

    copy_outputs()
    validation = validation_rows(source_rows, chain, zero, product, finite, arena, decisions, claim, next_targets)
    write_csv(VALIDATION, validation)
    write_doc(source_rows, chain, zero, product, finite, arena, decisions, claim, next_targets, validation)

    if any(row["result"] == "FAIL" for row in validation):
        raise SystemExit("1670 validation failed; see P8_Y5_BRR545_1670_VALIDATION.csv")

    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    print("1670 validation PASS")


if __name__ == "__main__":
    main()

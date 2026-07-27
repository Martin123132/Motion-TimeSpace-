from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1710"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1710-Y5-R2FR-R2FR-parent-coefficient-source-hunt-or-scalar-branch-input-pack.md"

SOURCE_FILES = {
    "1709_doc": ROOT / "1709-Y5-R2FR-primitive-minimality-no-higher-derivative-or-first-R11-component-fill.md",
    "1709_validation": OUT / "P8_Y5_BRR545_1709_VALIDATION.csv",
    "1709_next": OUT / "P8_Y5_PARENT_QLOC_1709_NEXT_TARGET.csv",
    "1709_first_interface": OUT / "P8_Y5_PARENT_QLOC_1709_FIRST_R11_COMPONENT_INTERFACE.csv",
    "1709_scalaron_handoff": OUT / "P8_Y5_PARENT_QLOC_1709_R2FR_SCALARON_HANDOFF.csv",
    "1589_doc": ROOT / "1589-Y5-R2FR-parent-coefficient-source-hunt-or-curve-QA-promotion.md",
    "1589_validation": OUT / "P8_Y5_BRR545_1589_VALIDATION.csv",
    "1589_hunt": OUT / "P8_Y5_PARENT_QLOC_1589_COEFFICIENT_SOURCE_HUNT.csv",
    "1589_law": OUT / "P8_Y5_PARENT_QLOC_1589_EFFECTIVE_COEFFICIENT_LAW.csv",
    "1589_owner": OUT / "P8_Y5_PARENT_QLOC_1589_MEMORY_FIBRE_OWNER_STATUS.csv",
    "1590_doc": ROOT / "1590-Y5-R2FR-Gamma-Khat-Ploc-owner-bundle-or-cR2-finite-coefficient-row.md",
    "1590_validation": OUT / "P8_Y5_BRR545_1590_VALIDATION.csv",
    "1590_owner": OUT / "P8_Y5_PARENT_QLOC_1590_OWNER_BUNDLE_SYNTHESIS.csv",
    "1590_finite_template": OUT / "P8_Y5_PARENT_QLOC_1590_FINITE_COEFFICIENT_ROW_TEMPLATE.csv",
    "1591_doc": ROOT / "1591-Y5-R2FR-fixed-L0-cdb-memory-Qnorm-first-fill-or-cR2-bound-row.md",
    "1591_validation": OUT / "P8_Y5_BRR545_1591_VALIDATION.csv",
    "1591_cr2_interface": OUT / "P8_Y5_PARENT_QLOC_1591_CR2_BOUND_ROW_INTERFACE.csv",
    "1591_qnorm": OUT / "P8_Y5_PARENT_QLOC_1591_QNORM_FIRST_FILL_SYNTHESIS.csv",
    "962_trace": OUT / "P8_Y5_R10_962_TRACE_SCALAR_POLE_TEST.csv",
    "962_fallback": OUT / "P8_Y5_R10_962_SCALAR_BOUND_FALLBACK_ROWS.csv",
    "963_owner": OUT / "P8_Y5_R10_963_R2FR_COEFFICIENT_OWNER_AUDIT.csv",
    "963_runner": OUT / "P8_Y5_R10_963_R2FR_BOUND_RUNNER_SPEC.csv",
    "1588_curve": OUT / "P8_Y5_PARENT_QLOC_1588_FULL_CURVE_INTAKE_STATUS.csv",
}

NEEDLES = {
    "1709_doc": ["NEXT1709_0_primary", "parent-owned `c_R2/fRR` scalaron input pack"],
    "1709_validation": ["VAL1709_OVERALL", "PASS"],
    "1709_next": ["1710-Y5-R2FR-R2FR-parent-coefficient-source-hunt-or-scalar-branch-input-pack.md", "selected"],
    "1709_first_interface": ["FC1709_0_R2FR", "SOURCE_BACKED_VALUE_OR_THEOREM_ZERO_REQUIRED"],
    "1709_scalaron_handoff": ["SH1709_3_next_input_pack", "NEXT_INPUT_PACK"],
    "1589_doc": ["PARENT_COEFFICIENT_OWNER_STILL_MISSING", "c_R2_eff(k)=c_bare+1/2 B^T L^-1(k)B+c_measure+c_boundary"],
    "1589_validation": ["VAL1589_OVERALL", "PASS"],
    "1589_hunt": ["HUNT1589_7_verdict", "NO_CLAIM_READY_PARENT_COEFFICIENT_FOUND"],
    "1589_law": ["LAW1589_0_integrated_hidden_modes", "DERIVED_CONDITIONAL_COEFFICIENT_LAW"],
    "1589_owner": ["OWN1589_5_owner_verdict", "NO_CLAIM_READY_OWNER"],
    "1590_doc": ["FIXED_L0_DOUBLE_ZERO_IS_THE_BEST_CURRENT_LOCAL_BRANCH", "Q_norm"],
    "1590_validation": ["VAL1590_OVERALL", "PASS"],
    "1590_owner": ["OBS1590_5_owner_verdict", "OWNER_BUNDLE_NOT_CLOSED_CURRENT_CORPUS"],
    "1590_finite_template": ["FCR1590_0_cR2_eff", "MISSING_NUMERIC_OR_THEOREM_ZERO"],
    "1591_doc": ["Q_norm <= Q_alg + Q_cdb + Q_mem + Q_bdy + Q_trans + Q_proj", "FINITE_CR2_BOUND_ROW_INTERFACE_READY_NONCLAIM"],
    "1591_validation": ["VAL1591_OVERALL", "PASS"],
    "1591_cr2_interface": ["CBI1591_0_cR2_effective_law", "ACCEPTANCE_CONTRACT_READY_NO_ROW_ACCEPTED"],
    "1591_qnorm": ["QNF1591_6_Q_norm_total", "TOTAL_BOUND_FORM_READY_ALL_COMPONENT_VALUES_MISSING"],
    "962_trace": ["SP962_0_metric_fR_map", "MISSING_a_OR_fRR"],
    "962_fallback": ["R2B962_1_fR_unscreened_map", "formula_ready_missing_parent_input"],
    "963_owner": ["CO963_4_verdict", "NO_EXECUTABLE_OWNER_FOUND"],
    "963_runner": ["R2RUN963_4_decision_logic", "neither_condition_met"],
    "1588_curve": ["CURVE1588_1_review_candidate", "review_candidate_nonclaim"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1710_SOURCE_REGISTER.csv"
COEFFICIENT_HUNT = OUT / "P8_Y5_PARENT_QLOC_1710_COEFFICIENT_SOURCE_HUNT_REFRESH.csv"
INPUT_PACK_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_1710_CR2_INPUT_PACK_CONTRACT.csv"
SCALARON_MAP_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_1710_SCALARON_MAP_CONTRACT.csv"
QNONLOCAL_INTERFACE = OUT / "P8_Y5_PARENT_QLOC_1710_QNORM_CR2_INTERFACE_LINK.csv"
RUNNER_REFUSAL = OUT / "P8_Y5_PARENT_QLOC_1710_RUNNER_REFUSAL.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1710_NEXT_TARGET.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1710_CLAIM_GATE.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1710_VALIDATION.csv"

GENERATED_CSVS = [
    SOURCE_REGISTER,
    COEFFICIENT_HUNT,
    INPUT_PACK_CONTRACT,
    SCALARON_MAP_CONTRACT,
    QNONLOCAL_INTERFACE,
    RUNNER_REFUSAL,
    NEXT_TARGET,
    CLAIM_GATE,
]

CLAIM_CHECKED_CSVS = [
    COEFFICIENT_HUNT,
    INPUT_PACK_CONTRACT,
    SCALARON_MAP_CONTRACT,
    QNONLOCAL_INTERFACE,
    RUNNER_REFUSAL,
    NEXT_TARGET,
    CLAIM_GATE,
]

COPY_TARGETS = {
    COEFFICIENT_HUNT: [
        QUARANTINE / "COEFFICIENT_SOURCE_HUNT_REFRESH.csv",
        BRANCH_RESIDUALS / "R2FR_coefficient_source_hunt_refresh_1710.csv",
        QUEUE / "JR1710_COEFFICIENT_SOURCE_HUNT_REFRESH.csv",
    ],
    INPUT_PACK_CONTRACT: [
        QUARANTINE / "CR2_INPUT_PACK_CONTRACT.csv",
        BRANCH_RESIDUALS / "R2FR_cR2_input_pack_contract_1710.csv",
        QUEUE / "JR1710_CR2_INPUT_PACK_CONTRACT.csv",
    ],
    SCALARON_MAP_CONTRACT: [
        QUARANTINE / "SCALARON_MAP_CONTRACT.csv",
        BRANCH_RESIDUALS / "R2FR_scalaron_map_contract_1710.csv",
        QUEUE / "JR1710_SCALARON_MAP_CONTRACT.csv",
    ],
    QNONLOCAL_INTERFACE: [
        QUARANTINE / "QNORM_CR2_INTERFACE_LINK.csv",
        BRANCH_RESIDUALS / "R2FR_Qnorm_cR2_interface_link_1710.csv",
        QUEUE / "JR1710_QNORM_CR2_INTERFACE_LINK.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_1710.csv",
        QUEUE / "JR1710_NEXT_TARGET.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_1710.csv",
        QUEUE / "JR1710_CLAIM_GATE.csv",
    ],
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _field in fields) + " |",
    ]
    for row in rows:
        values = [str(row.get(field, "")).replace("|", "\\|").replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (source_key, path) in enumerate(SOURCE_FILES.items()):
        text = read_text(path) if path.exists() else ""
        needles = NEEDLES[source_key]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": f"SRC1710_{index}_{source_key}",
                "source_key": source_key,
                "source_path": str(path),
                "exists": path.exists(),
                "needles_present": all(needle in text for needle in needles),
                "required_needles": ";".join(needles),
                "use_in_1710": "R2/fR parent coefficient hunt and scalar branch input-pack gate",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def coefficient_hunt_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CH1710_0_parent_zero",
            "c_R2_or_fRR",
            "parent exact second-order/no-extra-scalar/no-integrated-tower theorem",
            "RELATIVE_THEOREM_READY_PARENT_SIGNATURE_MISSING",
            "no parent-owned activator found in 1709/1589/963",
            "would set R2/fR branch to theorem-zero",
        ),
        (
            "CH1710_1_bare_operator",
            "c_bare",
            "operator-domain exclusion of bare R^2/f(R)/R F(Box) R terms",
            "UNSIGNED_NO_BARE_HIGHER_CURVATURE_CLAUSE",
            "minimality/no-higher-derivative retest failed",
            "must be zero theorem or finite coefficient input",
        ),
        (
            "CH1710_2_memory_vertex",
            "B_mem",
            "Gamma_eff/Khat/Ploc owner plus memory branch extremum",
            "PRIVATE_CLOSURE_ONLY_NOT_PARENT_OWNED",
            "fixed-L0/double-zero closes algebraic m/L sector only",
            "retain finite B_mem or prove response bundle",
        ),
        (
            "CH1710_3_fibre_vertex",
            "B_h",
            "hidden-visible coefficient typing or fibre curvature vertex theorem",
            "FIBRE_CURVATURE_VERTEX_UNSIGNED",
            "no parent grammar/constraint signs zero",
            "retain finite fibre coefficient if not zeroed",
        ),
        (
            "CH1710_4_measure_boundary",
            "c_measure;c_boundary",
            "measure/Jacobian, boundary/corner and frame-transfer owner",
            "MISSING_MEASURE_BOUNDARY_FRAME_OWNER",
            "field-redefinition and topological safe cases are not certified",
            "retain finite residual terms",
        ),
        (
            "CH1710_5_numeric_owner",
            "c_R2/fRR numeric value",
            "complete finite scalar-mode residual row",
            "MISSING_PARENT_INPUT",
            "no value, units, sign, normalization, screening or source path exists",
            "would allow nonclaim R10/PPN comparison if bound rows also valid",
        ),
        (
            "CH1710_6_verdict",
            "R2/fR coefficient owner",
            "all registered coefficient source routes",
            "NO_EXECUTABLE_COEFFICIENT_FOUND_CURRENT_CORPUS",
            "formula/law exists but no source-backed MTS coefficient exists",
            "write strict input-pack blocker ledger",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "hunt_id": hunt_id,
            "coefficient_or_clause": coefficient,
            "candidate_owner": owner,
            "status": status,
            "evidence_summary": evidence,
            "effect_if_closed": effect,
            "parent_signed": False,
            "numeric_value_present": False,
            "source_backed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for hunt_id, coefficient, owner, status, evidence, effect in rows
    ]


def input_pack_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "IP1710_0_identity",
            "model_id;branch_id;operator_family",
            "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428;R2_fR_scalar_mode",
            "branch identity and model label",
            "READY_AS_CONTRACT_ONLY",
        ),
        (
            "IP1710_1_coefficient",
            "c_R2_or_fRR",
            "MISSING_PARENT_COEFFICIENT",
            "parent-owned value or theorem-zero certificate",
            "BLOCKING_FIELD",
        ),
        (
            "IP1710_2_units_sign",
            "coefficient_units;sign;normalization",
            "MISSING_UNITS_SIGN_NORMALIZATION",
            "length^2/inverse-mass-squared convention and non-tachyonic sign if finite branch",
            "BLOCKING_FIELD",
        ),
        (
            "IP1710_3_effective_law_components",
            "c_bare;B_X;L_inverse;M_X2;Z_X;c_measure;c_boundary",
            "MISSING_COMPONENT_VALUES",
            "fill c_R2_eff(k)=c_bare+1/2 B^T L^-1 B+c_measure+c_boundary",
            "BLOCKING_FIELD",
        ),
        (
            "IP1710_4_source_provenance",
            "source_path;source_anchor;equation_ref;extraction_method",
            "MISSING_SOURCE_PROVENANCE",
            "local source file or parent derivation row for every finite/theorem-zero field",
            "BLOCKING_FIELD",
        ),
        (
            "IP1710_5_branch_regime",
            "branch_context;screening_flag;matter_coupling_frame",
            "MISSING_REGIME_MAP",
            "simple unscreened metric f(R), screened, closure-only, or other declared branch",
            "BLOCKING_FIELD",
        ),
        (
            "IP1710_6_observable_maps",
            "R10_map;PPN_map;clock_map;orbital_map",
            "MISSING_ARENA_PROJECTIONS",
            "maps coefficient/scalaron variables into test observables without cancellation",
            "BLOCKING_FIELD",
        ),
        (
            "IP1710_7_bound_inputs",
            "R10_curve;PPN_bound;clock_bound;orbital_bound",
            "R10_REVIEW_CANDIDATE_NONCLAIM_PPN_MAP_MISSING",
            "claim-grade bounds or explicitly nonclaim smoke-only status",
            "BLOCKING_FIELD",
        ),
        (
            "IP1710_8_acceptance",
            "zero_theorem_signed OR complete finite row",
            "NEITHER_CONDITION_MET",
            "runner accepts only parent-signed zero or complete numeric/source-backed prediction row",
            "REJECT_CURRENT_INPUT_PACK",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "pack_id": pack_id,
            "required_field": field,
            "current_value": value,
            "purpose": purpose,
            "status": status,
            "parent_signed": False,
            "numeric_value_present": False,
            "source_backed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for pack_id, field, value, purpose, status in rows
    ]


def scalaron_map_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "SMC1710_0_flat_R_plus_aR2",
            "simple metric f(R)=R+aR^2 around flat background",
            "m_s^2=1/(6a); lambda_s=1/m_s; alpha_s=1/3 only in simple unscreened metric f(R)",
            "FORMULA_READY_PARENT_INPUT_MISSING",
            "a/c_R2/fRR is not supplied by MTS",
        ),
        (
            "SMC1710_1_general_fR",
            "general local f(R) expansion",
            "m_s^2=(f_R-R f_RR)/(3 f_RR) after declared normalization",
            "FORMULA_READY_NORMALIZATION_MISSING",
            "f_R, f_RR and background convention are not source-backed",
        ),
        (
            "SMC1710_2_zero_branch",
            "parent-signed second-order/no-extra-scalar branch",
            "c_R2=fRR=0 and finite scalaron branch absent",
            "ZERO_THEOREM_UNSIGNED",
            "relative theorem cannot be promoted without parent activator",
        ),
        (
            "SMC1710_3_screening",
            "screened/unscreened environmental regime",
            "alpha_s and lambda_s are scoreable only after screening and source/test coupling are declared",
            "MISSING_SCREENING_REGIME",
            "formula-only rows cannot feed R10/PPN",
        ),
        (
            "SMC1710_4_prediction_row",
            "MTS alpha/lambda prediction",
            "lambda_predicted, alpha_predicted, units, source_path, branch_context",
            "NOT_CREATED",
            "input pack incomplete",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "map_id": map_id,
            "map_piece": piece,
            "formula_or_rule": formula,
            "status": status,
            "blocking_gap": gap,
            "parent_signed": False,
            "numeric_value_present": False,
            "source_backed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for map_id, piece, formula, status, gap in rows
    ]


def qnorm_interface_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "QI1710_0_cR2_law",
            "c_R2_eff",
            "c_bare + 1/2 B^T L^-1 B + c_measure + c_boundary",
            "SYMBOLIC_LAW_READY_NUMERIC_OR_ZERO_MISSING",
            "feeds scalaron/R10 and R11 beta rows",
        ),
        (
            "QI1710_1_Qnorm_link",
            "Q_norm",
            "Q_alg + Q_cdb + Q_mem + Q_bdy + Q_trans + Q_proj",
            "SYMBOLIC_COMPONENT_FORM_READY_VALUES_MISSING",
            "feeds PPN gamma/Cassini and local residual envelope",
        ),
        (
            "QI1710_2_no_cancellation",
            "absolute component accounting",
            "abs components must pass separately or by declared no-cancellation envelope",
            "POLICY_READY_VALUES_MISSING",
            "prevents hiding large residuals through tuning",
        ),
        (
            "QI1710_3_arena_projection",
            "R10/PPN/clock/orbital maps",
            "each arena needs response matrix, units and bound source",
            "PROJECTION_BLOCKED",
            "no empirical pass can be claimed from symbolic rows",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "interface_id": interface_id,
            "quantity": quantity,
            "formula_or_policy": formula,
            "status": status,
            "role": role,
            "numeric_value_present": False,
            "source_backed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for interface_id, quantity, formula, status, role in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN1710_0_zero_theorem", "promote c_R2=fRR=0", "REFUSE_UNSIGNED_ZERO_THEOREM", "parent second-order/no-extra-scalar/minimality activator is still unsigned"),
        ("RUN1710_1_input_pack", "build finite scalaron prediction", "REJECT_INPUT_PACK_INCOMPLETE", "coefficient, units, sign, normalization, screening, source path and maps are missing"),
        ("RUN1710_2_R10_curve", "score against R10 curve", "REJECT_PREDICTION_MISSING", "curve side is secondary and no MTS alpha/lambda prediction exists"),
        ("RUN1710_3_anchor_backsolve", "infer coefficient from alpha=1 anchors", "FORBIDDEN_BACKSOLVE_REJECTED", "bounds constrain predictions; they do not generate MTS coefficients"),
        ("RUN1710_4_Qnorm_proxy", "use Qnorm symbolic interface as local-GR pass", "REJECT_SYMBOLIC_PROXY", "Q_i component values and arena maps are missing"),
        ("RUN1710_5_future_accept", "future fully sourced c_R2/fRR row", "WOULD_ACCEPT_IF_REAL_VALUES_AND_FILES_EXIST", "requires all fields, sources, units and maps; remains nonclaim until compared"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "case": case,
            "status": status,
            "reason": reason,
            "score_emitted": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for runner_id, case, status, reason in rows
    ]


def next_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "NEXT1710_0_primary",
            "1711-Y5-R2FR-Gamma-Khat-Ploc-owner-bundle-or-cR2-input-pack-smoke-runner.md",
            "scripts/Y5_R2FR_Gamma_Khat_Ploc_owner_bundle_or_cR2_input_pack_smoke_runner.py",
            "attack the Gamma_eff/K_hat/P_loc response owner as the theorem route; if it still fails, run a strict smoke validator that rejects the incomplete c_R2/fRR input pack",
            "selected",
        ),
        (
            "NEXT1710_1_parallel_connection",
            "1711b-Y5-R2FR-Levi-Civita-torsion-nonmetricity-source-row.md",
            "scripts/Y5_R2FR_Levi_Civita_torsion_nonmetricity_source_row.py",
            "parallel high-priority connection route for torsion/nonmetricity if c_R2 owner stalls",
            "held_parallel",
        ),
        (
            "NEXT1710_2_data",
            "1711c-Y5-R2FR-R10-curve-QA-only-after-cR2-prediction.md",
            "scripts/Y5_R2FR_R10_curve_QA_only_after_cR2_prediction.py",
            "curve QA remains held until prediction fields exist",
            "held_until_prediction",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": route_id,
            "next_target": target,
            "script": script,
            "objective": objective,
            "selection_status": status,
            "success_condition": "parent owner theorem closes or smoke runner rejects/accepts c_R2 input pack by strict schema",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for route_id, target, script, objective, status in rows
    ]


def claim_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG1710_0_cR2_zero", "c_R2/fRR theorem-zero", "BLOCKED_NO_CLAIM", "parent zero signature unsigned"),
        ("CG1710_1_cR2_input_pack", "finite c_R2/fRR prediction row", "BLOCKED_NO_CLAIM", "coefficient, units, source and maps missing"),
        ("CG1710_2_scalaron_R10", "R2/fR scalaron alpha/lambda score", "BLOCKED_NO_CLAIM", "no MTS prediction and no claim-grade curve pairing"),
        ("CG1710_3_Qnorm", "Qnorm/local residual bound pass", "BLOCKED_NO_CLAIM", "component values and arena projections missing"),
        ("CG1710_4_EH", "EH operator selected", "BLOCKED_NO_CLAIM", "R11 residual branch remains active"),
        ("CG1710_5_local_GR", "derived local GR/Newton reduction", "BLOCKED_NO_CLAIM", "operator/source/GM/PPN/R11 gates not closed together"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": claim_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for claim_id, claim, status, reason in rows
    ]


def parse_all(paths: list[Path]) -> bool:
    for path in paths:
        read_csv(path)
    return True


def claim_flags_false(paths: list[Path]) -> bool:
    checked_keys = {
        "accepted_for_scoring",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "gate_pass",
        "score_emitted",
        "parent_signed",
        "numeric_value_present",
        "source_backed",
    }
    for path in paths:
        for row in read_csv(path):
            for key, value in row.items():
                if key in checked_keys and truthy(value):
                    return False
    return True


def formalization_1710_hits() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    return [
        path
        for path in FORMALIZATION.rglob("*1710*")
        if path.is_file() and ".venv" not in path.parts and "__pycache__" not in path.parts
    ]


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(
    source_rows: list[dict[str, Any]],
    hunt_rows: list[dict[str, Any]],
    pack_rows: list[dict[str, Any]],
    scalaron_rows: list[dict[str, Any]],
    qnorm_rows: list[dict[str, Any]],
    runner_rows_: list[dict[str, Any]],
    next_rows_: list[dict[str, Any]],
    claim_rows_: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    remove_pycache()
    checks = [
        ("VAL1710_0_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL1710_1_needles_present", all(row["needles_present"] for row in source_rows), "required source needles are present"),
        (
            "VAL1710_2_no_coefficient_found",
            any(row["hunt_id"] == "CH1710_6_verdict" and row["status"] == "NO_EXECUTABLE_COEFFICIENT_FOUND_CURRENT_CORPUS" for row in hunt_rows),
            "coefficient hunt records no executable parent coefficient",
        ),
        (
            "VAL1710_3_input_pack_blocks",
            any(row["pack_id"] == "IP1710_8_acceptance" and row["status"] == "REJECT_CURRENT_INPUT_PACK" for row in pack_rows),
            "input pack rejects current incomplete row",
        ),
        (
            "VAL1710_4_scalaron_formula_nonclaim",
            any(row["map_id"] == "SMC1710_0_flat_R_plus_aR2" and row["status"] == "FORMULA_READY_PARENT_INPUT_MISSING" for row in scalaron_rows),
            "scalaron formula retained without MTS prediction promotion",
        ),
        (
            "VAL1710_5_qnorm_link_nonclaim",
            any(row["interface_id"] == "QI1710_1_Qnorm_link" for row in qnorm_rows),
            "Qnorm/cR2 interface link carried forward as nonclaim",
        ),
        (
            "VAL1710_6_runner_blocks",
            all("REJECT" in row["status"] or "REFUSE" in row["status"] or "FORBIDDEN" in row["status"] or "WOULD_ACCEPT" in row["status"] for row in runner_rows_),
            "runner refuses current zero/input-pack/curve/proxy shortcuts",
        ),
        (
            "VAL1710_7_next_selected",
            any(row["route_id"] == "NEXT1710_0_primary" and row["selection_status"] == "selected" for row in next_rows_),
            "next target selects Gamma/Khat/Ploc owner or cR2 smoke runner",
        ),
        (
            "VAL1710_8_claim_gates_blocked",
            all(row["status"] == "BLOCKED_NO_CLAIM" for row in claim_rows_),
            "all claim gates remain blocked",
        ),
        ("VAL1710_9_csv_parse", parse_all(GENERATED_CSVS), "all generated 1710 CSVs parse"),
        (
            "VAL1710_10_no_claim_flags",
            claim_flags_false(CLAIM_CHECKED_CSVS),
            "all generated scoring and claim flags remain false",
        ),
        (
            "VAL1710_11_branch_copies",
            all(target.exists() for targets in COPY_TARGETS.values() for target in targets),
            "branch/quarantine/queue copies exist",
        ),
        (
            "VAL1710_12_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
        ),
        (
            "VAL1710_13_formalization_untouched",
            not formalization_1710_hits(),
            "no 1710 outputs found under formalization-workbench",
        ),
    ]
    rows = [
        {"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail}
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1710_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1710 R2/fR parent coefficient hunt and scalar branch input-pack validation",
        }
    )
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    hunt_rows: list[dict[str, Any]],
    pack_rows: list[dict[str, Any]],
    scalaron_rows: list[dict[str, Any]],
    qnorm_rows: list[dict[str, Any]],
    runner_rows_: list[dict[str, Any]],
    next_rows_: list[dict[str, Any]],
    claim_rows_: list[dict[str, Any]],
    validation_rows_: list[dict[str, Any]],
) -> None:
    content = "\n\n".join(
        [
            "# 1710 - R2/fR Parent Coefficient Source Hunt Or Scalar Branch Input Pack",
            "## Verdict\n"
            "- The parent-owned `c_R2/fRR` coefficient is still not found.\n"
            "- This is not a vague failure: the coefficient target is now exact, `c_R2_eff(k)=c_bare+1/2 B^T L^-1(k)B+c_measure+c_boundary`.\n"
            "- Formula-only scalaron rows are refused as predictions until the MTS coefficient, units, sign, normalization, screening and source path exist.\n"
            "- The R10 curve side remains secondary; no anchor backsolve or review-candidate curve claim is allowed.\n"
            "- No R2/fR, R10, PPN, EH, Newton, WEP, clock, orbital or local-GR claim is made.",
            "## Source Register\n" + table(source_rows, ["source_id", "source_key", "source_path", "exists", "needles_present"]),
            "## Coefficient Source Hunt Refresh\n"
            + table(hunt_rows, ["hunt_id", "coefficient_or_clause", "candidate_owner", "status", "evidence_summary"]),
            "## cR2 Input Pack Contract\n"
            + table(pack_rows, ["pack_id", "required_field", "current_value", "purpose", "status"]),
            "## Scalaron Map Contract\n"
            + table(scalaron_rows, ["map_id", "map_piece", "formula_or_rule", "status", "blocking_gap"]),
            "## Qnorm/cR2 Interface Link\n"
            + table(qnorm_rows, ["interface_id", "quantity", "formula_or_policy", "status", "role"]),
            "## Runner Refusal\n" + table(runner_rows_, ["runner_id", "case", "status", "reason"]),
            "## Next Target\n" + table(next_rows_, ["route_id", "next_target", "script", "objective", "selection_status"]),
            "## Claim Gates\n" + table(claim_rows_, ["claim_id", "claim", "status", "reason"]),
            "## Validation\n" + table(validation_rows_, ["check_id", "result", "detail"]),
            "## Working Interpretation\n"
            "The local-GR route is now sitting on a very concrete coefficient bottleneck. If `c_R2/fRR` can be parent-zeroed, the EH route strengthens. If it can be given a real finite value, MTS gets a testable scalar residual. If neither happens, this branch stays a named blocker rather than fog.",
        ]
    )
    DOC.write_text(content + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    hunt_rows = coefficient_hunt_rows()
    pack_rows = input_pack_rows()
    scalaron_rows = scalaron_map_rows()
    qnorm_rows = qnorm_interface_rows()
    runner_rows_ = runner_rows()
    next_rows_ = next_rows()
    claim_rows_ = claim_rows()

    write_csv(SOURCE_REGISTER, source_rows)
    write_csv(COEFFICIENT_HUNT, hunt_rows)
    write_csv(INPUT_PACK_CONTRACT, pack_rows)
    write_csv(SCALARON_MAP_CONTRACT, scalaron_rows)
    write_csv(QNONLOCAL_INTERFACE, qnorm_rows)
    write_csv(RUNNER_REFUSAL, runner_rows_)
    write_csv(NEXT_TARGET, next_rows_)
    write_csv(CLAIM_GATE, claim_rows_)
    copy_outputs()

    validation_rows_ = validation_rows(
        source_rows,
        hunt_rows,
        pack_rows,
        scalaron_rows,
        qnorm_rows,
        runner_rows_,
        next_rows_,
        claim_rows_,
    )
    write_csv(VALIDATION, validation_rows_)
    write_doc(
        source_rows,
        hunt_rows,
        pack_rows,
        scalaron_rows,
        qnorm_rows,
        runner_rows_,
        next_rows_,
        claim_rows_,
        validation_rows_,
    )

    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    print(f"1710 validation {validation_rows_[-1]['result']}")


if __name__ == "__main__":
    main()

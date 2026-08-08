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
DOC_PATH = ROOT / "2639-Y5-R2FR-readout-residual-to-q-loc-response-map-or-R10-Yukawa-source-row.md"

PREFIX = "P8_Y5_READOUT_QLOC_R10_BRIDGE_2639"

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "bridge_gate": RESIDUALS / f"{PREFIX}_READOUT_TO_QLOC_BRIDGE_GATE.csv",
    "r10_source_row": RESIDUALS / f"{PREFIX}_R10_YUKAWA_SOURCE_ROW.csv",
    "quartet": RESIDUALS / f"{PREFIX}_R10_QUARTET_STATUS.csv",
    "score_refusal": RESIDUALS / f"{PREFIX}_ALPHA_SCORE_REFUSAL.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2639_VALIDATION.csv",
}

SOURCES = [
    {
        "source_id": "SRC2639_00_2638",
        "role": "immediate readout component source-bound handoff",
        "path": ROOT / "2638-Y5-R2FR-readout-residual-component-zero-or-source-bound-pack.md",
        "needles": ["READOUT_COMPONENT_ZERO_ATTEMPTS_DO_NOT_CLOSE", "QBR2638_3_readout_to_R10", "VAL2638_OVERALL"],
    },
    {
        "source_id": "SRC2639_01_2638_bounds_csv",
        "role": "machine-readable readout source-bound pack",
        "path": RESIDUALS / "P8_Y5_READOUT_COMPONENT_BOUND_2638_SOURCE_BOUND_PACK.csv",
        "needles": ["RB2638_0_E_readout_total", "RB2638_6_Delta_readout_abs"],
    },
    {
        "source_id": "SRC2639_02_2409",
        "role": "q_loc/Khat response frontier and R10 scaffold",
        "path": ROOT / "2409-Y5-R2FR-Gamma-eff-metric-variation-or-first-q-loc-response-operator-row.md",
        "needles": ["KHAT_IDENTITY_NOT_PARENT_SIGNED", "ROP2409_2_R10_yukawa_kernel_scaffold", "VAL2409_OVERALL"],
    },
    {
        "source_id": "SRC2639_03_2410",
        "role": "R10 q_loc-to-Yukawa source-map blocker",
        "path": ROOT / "2410-Y5-R2FR-R10-q-loc-Yukawa-source-map-or-bound-curve-blocker.md",
        "needles": ["SOURCE_MAP_GATE_TIGHTENED_NO_CLAIM", "SMG2410_4_q_loc_bridge_contract", "VAL2410_OVERALL"],
    },
    {
        "source_id": "SRC2639_04_563",
        "role": "real R10 anchors and bound-curve blocker",
        "path": ROOT / "563-Y5-R10-real-bound-curve-acquisition-and-alpha-row-smoke-runner.md",
        "needles": ["Y5_R10_real_bound_anchor_staged_nonclaim_smoke_runner_blocks_claim", "B563_0_no_full_bound_curve", "V563_10_no_overclaim"],
    },
    {
        "source_id": "SRC2639_05_1034",
        "role": "review-candidate bound curve not promoted",
        "path": ROOT / "1034-Y5-R10-alpha-bound-curve-digitization-and-projection-input-pack.md",
        "needles": ["R10P1034_0_alpha_bound_curve", "REVIEW_CANDIDATE_CURVE_PRESENT_NONCLAIM", "V1034_2_candidate_file_written"],
    },
    {
        "source_id": "SRC2639_06_1035",
        "role": "Yukawa Green kernel and source-test product law",
        "path": ROOT / "1035-Y5-R10-KX-green-kernel-normalization-and-profile-integral.md",
        "needles": ["KXD1035_1_static_green_function", "BETA1035_0_product_law", "V1035_1_green_kernel_contract"],
    },
    {
        "source_id": "SRC2639_07_2489",
        "role": "PPN readout tail/no-gamma-only guard",
        "path": ROOT / "2489-Y5-R2FR-first-common-frame-PPN-response-kernel-or-parent-no-shadow-clause.md",
        "needles": ["PPNV2489_6_readout_gauge", "GAMMA_ONLY_PASS_FORBIDDEN", "VAL2489_OVERALL"],
    },
    {
        "source_id": "SRC2639_08_2631",
        "role": "full PPN vector readout/GM tail",
        "path": ROOT / "2631-Y5-R2FR-current-branch-no-shadow-full-PPN-vector-or-residual-kernel-fill.md",
        "needles": ["PPNV2631_6_readout_gauge", "FULL_PPN_VECTOR_IS_CURRENT_BRANCH_INTERFACE", "VAL2631_OVERALL"],
    },
    {
        "source_id": "SRC2639_09_2408",
        "role": "R_eq/I_commutator finite source-normalization blockers",
        "path": ROOT / "2408-Y5-R2FR-topological-Hilbert-equality-R-eq-zero-or-epsilonM-bound-fill.md",
        "needles": ["REQ2408_0_R_eq", "REQ2408_2_I_commutator", "VAL2408_OVERALL"],
    },
]


def ensure_dirs() -> None:
    for directory in (RESIDUALS, LOCAL_BOUNDS, RAB_QUEUE):
        directory.mkdir(parents=True, exist_ok=True)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


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


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *[
                "| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |"
                for row in rows
            ],
        ]
    )


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        text = read_text(source["path"])
        exists = source["path"].exists()
        needles_present = exists and all(needle in text for needle in source["needles"])
        rows.append(
            {
                "timestamp_utc": now(),
                "source_id": source["source_id"],
                "role": source["role"],
                "source_path": str(source["path"]),
                "exists": bool_text(exists),
                "needles_present": bool_text(needles_present),
                "needles": "; ".join(source["needles"]),
                "valid_for_claim": "False",
            }
        )
    return rows


def bridge_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "bridge_id": "BRG2639_0_readout_metric_response",
            "source_components": "E_readout_total;projector_stress_beta_equiv",
            "target_object": "q_metric_response_defect",
            "required_bridge": "prove readout/projector metric-response terms are absent from S_parent or identical to the live K_hat/Gamma_eff metric-response convention",
            "current_status": "BLOCKED_KHAT_IDENTITY_NOT_PARENT_SIGNED",
            "missing_inputs": "live Gamma_eff density owner; K_hat identity; variation convention; units/readout projection",
            "passes_now": "False",
            "valid_for_claim": "False",
        },
        {
            "bridge_id": "BRG2639_1_projector_source_normalization",
            "source_components": "projector_norm;R_eq_integral;I_commutator;D_D_PiM",
            "target_object": "q_loc_response_operator;source_normalization",
            "required_bridge": "parent-owned physical current/domain/M_H_ref/tau map before projector mismatch is a scalar source or Newtonian mass tail",
            "current_status": "BLOCKED_R_EQ_MHREF_BZERO_UNFILLED",
            "missing_inputs": "R_eq value/zero; B_zero_flux; M_H_ref; tau_source=tau_readout; physical current complex",
            "passes_now": "False",
            "valid_for_claim": "False",
        },
        {
            "bridge_id": "BRG2639_2_no_direct_q_scalarization",
            "source_components": "Delta_readout_abs;q_loc_nu",
            "target_object": "rho_X_or_J_i",
            "required_bridge": "derive J_i = S_i[I_div^{-1}(q_loc)] or q_loc^nu=P_loc b_i^nu[(L_i X_i)-J_i]+boundary terms with all maps parent-owned",
            "current_status": "DIRECT_SCALARIZATION_REJECTED",
            "missing_inputs": "tau_i_nu; I_div_inverse/T_GK owner; b_i_nu; boundary terms; units",
            "passes_now": "False",
            "valid_for_claim": "False",
        },
        {
            "bridge_id": "BRG2639_3_readout_to_R10_alpha",
            "source_components": "E_readout_total;projector_norm;marker_readout;Delta_readout_abs",
            "target_object": "alpha_readout_R10(lambda)",
            "required_bridge": "finite-range parent mode with Z_i, M_i^2, lambda_i, source/test charges, R10 profile projection and external alpha_bound(lambda)",
            "current_status": "SCAFFOLD_READY_NOT_SCORE_READY",
            "missing_inputs": "Z_i;M_i_squared;J_i;lambda_i;Q_source;Q_test;K_R10;alpha_bound_curve;tail_envelope",
            "passes_now": "False",
            "valid_for_claim": "False",
        },
    ]


def r10_source_row_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "R10R2639_0_readout_alpha_source_row",
            "branch_id": "readout_residual_to_R10_Yukawa_nonclaim",
            "lambda_value": "MISSING_LAMBDA_I",
            "lambda_units": "m",
            "range_owner": "MISSING_Z_i_AND_M_i_SQUARED_OR_PARENT_SPECTRUM",
            "source_map": "MISSING_J_i_FROM_QLOC_OR_READOUT_RESIDUAL",
            "source_charge": "MISSING_Q_SOURCE_READOUT",
            "test_charge": "MISSING_Q_TEST_READOUT",
            "K_R10_lambda": "MISSING_K_R10_PROFILE_HARMONIC",
            "tail_envelope": "Delta_readout_abs_R10=MISSING_COMPONENT_VALUES",
            "alpha_predicted": "K_R10_lambda*Q_source_readout*Q_test_readout/(4*pi*G_obs*Z_i*m_source*m_test)+Delta_readout_abs_R10",
            "alpha_bound": "MISSING_PROMOTED_ALPHA_BOUND_LAMBDA",
            "bound_curve_source": "R10_alpha_lambda_bound_curve_DIGITIZED.csv currently placeholder; 1034 review candidate not promoted",
            "score_status": "NOT_SCORE_READY",
            "required_source_paths": "parent Z/M/J row; q_loc bridge row; R10 profile kernel; promoted alpha_bound(lambda) curve; readout component rows",
            "valid_for_claim": "False",
        },
        {
            "row_id": "R10R2639_1_zero_branch_placeholder",
            "branch_id": "readout_residual_theorem_zero_branch",
            "lambda_value": "NOT_APPLICABLE_IF_THEOREM_ZERO",
            "lambda_units": "m",
            "range_owner": "requires parent-signed Delta_readout_abs=0 and q_loc source silence",
            "source_map": "requires no readout/source leg and no hidden marker before variation",
            "source_charge": "0 only if parent-signed",
            "test_charge": "0 only if parent-signed",
            "K_R10_lambda": "not scored",
            "tail_envelope": "Delta_readout_abs_R10=0 only if RB2638_0..5 theorem-zero",
            "alpha_predicted": "0 only under parent-signed theorem-zero inputs",
            "alpha_bound": "not used until zero branch is parent-signed",
            "bound_curve_source": "not enough to claim without theorem-zero signature",
            "score_status": "THEOREM_ZERO_REJECTED_WITHOUT_PARENT_SIGNATURE",
            "required_source_paths": "closed readout parent-domain certificate; no-marker theorem; projector stress zero; apparatus ideal limit",
            "valid_for_claim": "False",
        },
    ]


def quartet_rows() -> list[dict[str, Any]]:
    return [
        {
            "quartet_id": "R10Q2639_0_source_map",
            "required_input": "readout/q_loc_to_Yukawa_source_map",
            "current_status": "CONDITIONAL_CONTRACT_WRITTEN_NOT_PARENT_SIGNED",
            "still_missing": "tau_i_nu;I_div_inverse;T_GK_owner;J_i;b_i_nu;boundary_terms;units",
            "score_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "quartet_id": "R10Q2639_1_range",
            "required_input": "lambda_i_from_parent_ZM_spectrum",
            "current_status": "RANGE_RELATION_KNOWN_VALUES_MISSING",
            "still_missing": "Z_i;M_i_squared;M_AB/Z_AB;eigenvectors;length units",
            "score_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "quartet_id": "R10Q2639_2_charge_norm",
            "required_input": "source_test_readout_charge_normalization",
            "current_status": "BLOCKED_SOURCE_TEST_PRODUCT_MISSING",
            "still_missing": "Q_source_readout;Q_test_readout;beta_s;beta_t;R10 material/profile convention",
            "score_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "quartet_id": "R10Q2639_3_external_bound_curve",
            "required_input": "claim-valid alpha_bound(lambda) curve",
            "current_status": "ANCHOR_AND_REVIEW_CANDIDATE_NONCLAIM",
            "still_missing": "official table or promoted digitized curve; interpolation policy; uncertainty/provenance QA",
            "score_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "quartet_id": "R10Q2639_4_prediction_row",
            "required_input": "numeric alpha_readout_R10(lambda)",
            "current_status": "BLOCKED_NUMERIC_ALPHA_MISSING",
            "still_missing": "numeric source map; numeric lambda; numeric charges; K_R10 profile; Delta_readout_abs values",
            "score_ready": "False",
            "valid_for_claim": "False",
        },
        {
            "quartet_id": "R10Q2639_5_tail_envelope",
            "required_input": "Delta_readout_abs_R10 no-cancellation vector",
            "current_status": "SCHEMA_READY_COMPONENT_VALUES_MISSING",
            "still_missing": "RB2638_0;RB2638_1;RB2638_3 numeric/source-backed rows or theorem-zero proofs",
            "score_ready": "False",
            "valid_for_claim": "False",
        },
    ]


def score_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "refusal_id": "REF2639_0_no_q_scalar",
            "attempted_shortcut": "rho_X := q_loc or |q_loc|",
            "verdict": "REJECTED",
            "reason": "q_loc is a vector/residual/divergence object; R10 needs a scalar finite-range source with parent-owned projection and units",
            "required_repair": "derive tau_i_nu and I_div_inverse/T_GK bridge or source finite current rows",
            "runner_must_return": "False",
            "valid_for_claim": "False",
        },
        {
            "refusal_id": "REF2639_1_no_readout_tail_zero",
            "attempted_shortcut": "drop Delta_readout_abs_R10 from alpha prediction",
            "verdict": "REJECTED",
            "reason": "2638 component zero attempts did not close; readout tails are additive until theorem-zero or numeric bounds exist",
            "required_repair": "close RB2638_0/RB2638_1/RB2638_3 or carry their absolute tail",
            "runner_must_return": "False",
            "valid_for_claim": "False",
        },
        {
            "refusal_id": "REF2639_2_no_anchor_curve_score",
            "attempted_shortcut": "use alpha=1 threshold anchor or review candidate curve as claim-valid alpha_bound(lambda)",
            "verdict": "REJECTED",
            "reason": "anchors and review candidate rows are nonclaim; live digitized curve remains placeholder",
            "required_repair": "promote a dense bound curve only after official table or validated digitization/provenance QA",
            "runner_must_return": "False",
            "valid_for_claim": "False",
        },
        {
            "refusal_id": "REF2639_3_no_linear_single_coupling",
            "attempted_shortcut": "alpha_readout proportional to one universal coupling without source/test split",
            "verdict": "REJECTED",
            "reason": "two-body Yukawa exchange requires source and test charge factors unless one leg is already packed into a sourced Qbar term",
            "required_repair": "split beta_source_readout and beta_test_readout or source the packed convention explicitly",
            "runner_must_return": "False",
            "valid_for_claim": "False",
        },
        {
            "refusal_id": "REF2639_4_no_placeholder_score",
            "attempted_shortcut": "score R10R2639 rows with MISSING_* fields",
            "verdict": "REJECTED",
            "reason": "source-map, range, charges, bound curve and tail envelope are missing",
            "required_repair": "replace every MISSING_* field with numeric/source-backed rows or parent-signed zero theorem",
            "runner_must_return": "False",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG2639_0_internal_bridge",
            "claim": "2639 may guide private q_loc/R10 source-map work",
            "status": "ALLOW_INTERNAL_NONCLAIM",
            "passed": "True",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG2639_1_readout_to_q_loc_bridge",
            "claim": "readout residuals are mapped into q_loc/Khat with parent-signed convention",
            "status": "BLOCKED",
            "passed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG2639_2_R10_alpha_row",
            "claim": "numeric alpha_readout_R10(lambda) is score-ready",
            "status": "BLOCKED_MISSING_SOURCE_MAP_RANGE_CHARGES_CURVE_TAILS",
            "passed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG2639_3_R10_bound",
            "claim": "claim-valid external alpha_bound(lambda) curve is available",
            "status": "BLOCKED_ANCHOR_OR_REVIEW_CANDIDATE_ONLY",
            "passed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG2639_4_local_GR_Newton",
            "claim": "local GR/Newton follows from the readout/R10 bridge",
            "status": "BLOCKED",
            "passed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2639_0_result",
            "decision": "READOUT_TO_QLOC_R10_BRIDGE_WRITTEN_NOT_CLOSED",
            "reason": "readout residual components can be placed into the q_loc/R10 response interface, but no parent-owned source map or Khat identity is signed",
            "consequence": "alpha_readout_R10(lambda) row is schema-ready only and must not score",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC2639_1_gain",
            "decision": "FIRST_READOUT_R10_ALPHA_ROW_CONTRACT_CREATED",
            "reason": "lambda, source map, source/test charges, K_R10, alpha_bound and tail envelope slots are explicit",
            "consequence": "future data/testing work has a row to fill rather than a vague R10 wish",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC2639_2_route",
            "decision": "PARENT_ZM_J_OWNER_WITH_READOUT_TAIL_SELECTED",
            "reason": "range and source cannot be separated; readout tail cannot be dropped; external data alone cannot rescue missing theory coefficients",
            "consequence": "next work should hunt one parent Z/M/J/readout source clause or keep R10 as nonclaim data-parallel branch",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": "2640-Y5-R2FR-parent-ZM-J-owner-with-readout-tail-or-R10-alpha-refusal-runner.md",
            "script": "scripts/Y5_R2FR_parent_ZM_J_owner_with_readout_tail_or_R10_alpha_refusal_runner_2640.py",
            "objective": "try to source-sign one parent finite-range row containing Z_i, M_i^2/lambda_i, J_i, beta_source_readout, beta_test_readout and Delta_readout_abs_R10; if absent, keep R10 alpha scoring refused and demote the finite-range readout branch to explicit nonclaim acquisition",
            "include": "2639 alpha row contract; 2410 Z/M/J source-map gate; 1035 source-test product law; 2638 readout tail envelope; 563/1034 bound-curve blockers",
            "exclude": "direct q_loc scalarization, invented lambda, unity coupling shortcut, anchor-curve scoring, placeholder alpha pass, local-GR/R10 claim, GitHub action",
            "selected": "True",
            "valid_for_claim": "False",
        }
    ]


def branch_copy_pairs() -> list[tuple[str, Path, Path]]:
    return [
        ("COPY2639_bridge", OUTPUTS["bridge_gate"], LOCAL_BOUNDS / "Readout_q_loc_R10_bridge_gate_2639_NONCLAIM.csv"),
        ("COPY2639_r10_row", OUTPUTS["r10_source_row"], LOCAL_BOUNDS / "Readout_R10_yukawa_source_row_2639_NONCLAIM.csv"),
        ("COPY2639_quartet", OUTPUTS["quartet"], LOCAL_BOUNDS / "Readout_R10_quartet_status_2639_NONCLAIM.csv"),
        ("COPY2639_refusal", OUTPUTS["score_refusal"], LOCAL_BOUNDS / "Readout_R10_alpha_score_refusal_2639_NONCLAIM.csv"),
        ("COPY2639_next", OUTPUTS["next_target"], RAB_QUEUE / "JR2639_PARENT_ZM_J_READOUT_TAIL_NEXT.csv"),
    ]


def copy_branch_artifacts() -> None:
    for _, source, target in branch_copy_pairs():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": copy_id,
            "source_path": str(source),
            "copy_path": str(target),
            "source_exists": bool_text(source.exists()),
            "copy_exists": bool_text(target.exists()),
            "valid_for_claim": "False",
        }
        for copy_id, source, target in branch_copy_pairs()
    ]


def formalization_has_2639_outputs() -> bool:
    if not FORMALIZATION.exists():
        return False
    for path in FORMALIZATION.rglob("*2639*"):
        if path.is_file():
            return True
    for path in FORMALIZATION.rglob("*READOUT_QLOC_R10_BRIDGE_2639*"):
        if path.is_file():
            return True
    return False


def validation_rows(generated: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    copy_paths = [target for _, _, target in branch_copy_pairs()]
    checks = [
        (
            "VAL2639_00_sources",
            all(row["exists"] == "True" and row["needles_present"] == "True" for row in generated["source_register"]),
            "all cited source paths exist and required needles are present",
        ),
        (
            "VAL2639_01_bridge_blocked",
            any(row["bridge_id"] == "BRG2639_3_readout_to_R10_alpha" and row["passes_now"] == "False" for row in generated["bridge_gate"])
            and all(row["valid_for_claim"] == "False" for row in generated["bridge_gate"]),
            "readout-to-R10 bridge is staged but not closed",
        ),
        (
            "VAL2639_02_r10_row_contract",
            any(row["row_id"] == "R10R2639_0_readout_alpha_source_row" and row["score_status"] == "NOT_SCORE_READY" for row in generated["r10_source_row"]),
            "first readout-to-R10 alpha row contract exists and refuses scoring",
        ),
        (
            "VAL2639_03_missing_inputs_visible",
            any("MISSING_LAMBDA_I" in row["lambda_value"] and "MISSING_J_i" in row["source_map"] for row in generated["r10_source_row"]),
            "lambda and source-map missing inputs are explicit",
        ),
        (
            "VAL2639_04_quartet_blocked",
            all(row["score_ready"] == "False" and row["valid_for_claim"] == "False" for row in generated["quartet"]),
            "all R10 quartet rows remain blocked",
        ),
        (
            "VAL2639_05_refusals",
            all(row["runner_must_return"] == "False" and row["valid_for_claim"] == "False" for row in generated["score_refusal"])
            and any(row["refusal_id"] == "REF2639_2_no_anchor_curve_score" for row in generated["score_refusal"]),
            "shortcut scoring refusals are active",
        ),
        (
            "VAL2639_06_claim_gates",
            all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in generated["claim_gates"]),
            "no claim gate allows local GR or R10 pass",
        ),
        (
            "VAL2639_07_next_target",
            any(row["selected"] == "True" and row["next_target"].startswith("2640-Y5-R2FR-parent-ZM-J-owner") for row in generated["next_target"]),
            "2640 parent Z/M/J with readout tail target selected",
        ),
        (
            "VAL2639_08_branch_copies",
            all(path.exists() and csv_parses(path) for path in copy_paths),
            "nonclaim local_bounds copies and acquisition queue exist and parse",
        ),
        (
            "VAL2639_09_csv_parse",
            all(path.exists() and csv_parses(path) for path in output_csvs),
            "all generated 2639 CSVs parse",
        ),
        (
            "VAL2639_10_formalization_untouched",
            not formalization_has_2639_outputs(),
            "no 2639 outputs are written under formalization-workbench",
        ),
        (
            "VAL2639_11_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
        ),
    ]
    overall = all(status for _, status, _ in checks)
    rows = [
        {"check_id": check_id, "status": "PASS" if status else "FAIL", "detail": detail, "valid_for_claim": "False"}
        for check_id, status, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL2639_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "2639 readout residual to q_loc/R10 bridge and alpha-row refusal runner",
            "valid_for_claim": "False",
        }
    )
    return rows


def write_markdown(generated: dict[str, list[dict[str, Any]]], validation: list[dict[str, Any]]) -> None:
    lines = [
        "# 2639 - Y5 R2/f(R) Readout Residual To q_loc Response Map Or R10 Yukawa Source Row",
        "",
        "Status: `Y5_R2FR_2639_readout_to_q_loc_R10_bridge_written_alpha_row_contract_nonclaim_score_refused`",
        "",
        "Claim ceiling: no readout-to-`q_loc` bridge claim, no numeric `alpha_readout_R10(lambda)`, no R10 score, no PPN/WEP/clock/orbital pass, no local-GR/Newton proof, no anchor-curve scoring, no placeholder scoring, no GitHub action, and no `formalization-workbench` edit is made.",
        "",
        "## Summary",
        "",
        "2639 connects the readout residual work to the existing `q_loc/Khat` response frontier. The bridge is useful but does not close: `q_loc` still cannot be treated as a scalar Yukawa source, and readout tails cannot be dropped after 2638 failed to zero them.",
        "",
        "The output is therefore a first source-ready readout-to-R10 alpha-row contract, not a score. It names the exact missing pieces: parent `Z/M/J`, `lambda_i`, source/test charges, R10 profile kernel, promoted `alpha_bound(lambda)` curve, and the `Delta_readout_abs_R10` no-cancellation tail.",
        "",
        "## Source Register",
        md_table(generated["source_register"]),
        "",
        "## Readout To q_loc Bridge Gate",
        md_table(generated["bridge_gate"]),
        "",
        "## R10 Yukawa Source Row",
        md_table(generated["r10_source_row"]),
        "",
        "## R10 Quartet Status",
        md_table(generated["quartet"]),
        "",
        "## Alpha Score Refusal",
        md_table(generated["score_refusal"]),
        "",
        "## Claim Gates",
        md_table(generated["claim_gates"]),
        "",
        "## Decision Ledger",
        md_table(generated["decision"]),
        "",
        "## Next Target",
        md_table(generated["next_target"]),
        "",
        "## Branch Copies",
        md_table(generated["branch_copies"]),
        "",
        "## Validation",
        md_table(validation),
        "",
        "## Plain-English Verdict",
        "",
        "This is another small but real tightening. The readout residual can now enter the R10/Yukawa machinery only through a legal parent source map and source/test product law. No scalar-proxy shortcut, no anchor-curve shortcut, no single-coupling shortcut.",
        "",
        "The next hard leap is parent ownership: find one branch that owns `Z_i`, `M_i^2/lambda_i`, `J_i`, the readout source/test legs, and the retained tail envelope together. If that branch cannot be found, the finite-range R10 path should remain an explicit nonclaim acquisition branch while we keep deriving the GR route elsewhere.",
        "",
    ]
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ensure_dirs()
    generated = {
        "source_register": source_register_rows(),
        "bridge_gate": bridge_gate_rows(),
        "r10_source_row": r10_source_row_rows(),
        "quartet": quartet_rows(),
        "score_refusal": score_refusal_rows(),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }
    for key, rows in generated.items():
        if key in OUTPUTS:
            write_csv(OUTPUTS[key], rows)
    copy_branch_artifacts()
    generated["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], generated["branch_copies"])
    validation = validation_rows(generated)
    write_csv(OUTPUTS["validation"], validation)
    write_markdown(generated, validation)
    print(f"wrote {DOC_PATH}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

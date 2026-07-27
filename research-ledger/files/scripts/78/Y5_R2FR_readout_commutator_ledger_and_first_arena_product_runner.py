from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1702"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "1702-Y5-R2FR-readout-commutator-ledger-and-first-arena-product-runner.md"

SOURCE_FILES = {
    "1701_doc": ROOT / "1701-Y5-R2FR-readout-effective-no-reentry-theorem-or-finite-product-map.md",
    "1701_validation": OUT / "P8_Y5_BRR545_1701_VALIDATION.csv",
    "1701_commutator": OUT / "P8_Y5_PARENT_QLOC_1701_READOUT_COMMUTATOR_AUDIT.csv",
    "1701_product_map": OUT / "P8_Y5_PARENT_QLOC_1701_ARENA_FINITE_PRODUCT_MAP.csv",
    "1701_queue": OUT / "P8_Y5_PARENT_QLOC_1701_READOUT_RESIDUAL_QUEUE.csv",
    "1701_next": OUT / "P8_Y5_PARENT_QLOC_1701_NEXT_TARGET.csv",
    "1014_commutator_doc": ROOT / "1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md",
    "1067_tau_wep_schema": OUT / "P8_Y5_R10_1067_TAU_WEP_ACQUISITION_SCHEMA.csv",
    "1029_tau_projection": OUT / "P8_Y5_R10_1029_TAU_PROJECTION_REQUIREMENTS.csv",
    "947_projection_fill": OUT / "P8_Y5_R10_947_PROJECTION_FILL_ATTEMPT.csv",
    "1669_source_pack": OUT / "P8_Y5_PARENT_QLOC_1669_PPN_WEP_CLOCK_ORBIT_SOURCE_PACK_TEMPLATE.csv",
    "1476_source_weight": MICROSCOPE / "branch_locked_wep" / "coefficients" / "Ci_source_weight_delta_w_input_nonclaim_1476.csv",
    "1469_alpha_runner": MICROSCOPE / "branch_locked_wep" / "coefficients" / "alpha_residual_product_runner_nonclaim_1469.csv",
}

NEEDLES = {
    "1701_doc": ["NEXT1701_0_primary", "Pure post-processing readout is safe"],
    "1701_validation": ["VAL1701_OVERALL", "PASS"],
    "1701_commutator": ["RC1701_0_define_residual", "GENERAL_NO_REENTRY_NOT_DERIVED"],
    "1701_product_map": ["FPM1701_0_WEP_source_weight", "FPM1701_4_PPN_frame_vector"],
    "1701_queue": ["RQ1701_0_C_R", "branch_readout_functor"],
    "1701_next": ["NEXT1701_0_primary", "first finite product runner"],
    "1014_commutator_doc": ["PCT1014_0_product_rule", "I_commutator remains unfilled"],
    "1067_tau_wep_schema": ["TAQ1067_3_direct_product_option", "REFUSAL_ACTIVE"],
    "1029_tau_projection": ["TAU1029_0_R10", "TAU1029_1_PPN_gamma_beta"],
    "947_projection_fill": ["PFA947_0_R10_projection", "PFA947_1_PPN_projection"],
    "1669_source_pack": ["R1_WEP_source_charge", "R3_gamma"],
    "1476_source_weight": ["DW1476_0_delta_w_A", "MISSING_TAU_WEP"],
    "1469_alpha_runner": ["APR1469_2_R10_alpha_lambda", "BLOCKED_MISSING_INPUTS"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1702_SOURCE_REGISTER.csv"
COMMUTATOR_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1702_COMMUTATOR_SOURCE_INTAKE_LEDGER.csv"
FIRST_PRODUCT_RUNNER = OUT / "P8_Y5_PARENT_QLOC_1702_FIRST_ARENA_PRODUCT_RUNNER.csv"
WEP_SOURCE_WEIGHT = OUT / "P8_Y5_PARENT_QLOC_1702_WEP_SOURCE_WEIGHT_PRODUCT_ROW.csv"
R10_PPN_PROJECTION = OUT / "P8_Y5_PARENT_QLOC_1702_R10_PPN_PROJECTION_ROWS.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1702_RUNNER_REFUSAL.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1702_NEXT_TARGET.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1702_CLAIM_GATE.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1702_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    COMMUTATOR_LEDGER,
    FIRST_PRODUCT_RUNNER,
    WEP_SOURCE_WEIGHT,
    R10_PPN_PROJECTION,
    RUNNER,
    NEXT_TARGET,
    CLAIM_GATE,
]

CLAIM_CHECKED = [
    COMMUTATOR_LEDGER,
    FIRST_PRODUCT_RUNNER,
    WEP_SOURCE_WEIGHT,
    R10_PPN_PROJECTION,
    RUNNER,
    NEXT_TARGET,
    CLAIM_GATE,
]

COPY_TARGETS = {
    COMMUTATOR_LEDGER: [
        QUARANTINE / "COMMUTATOR_SOURCE_INTAKE_LEDGER.csv",
        BRANCH_RESIDUALS / "R2FR_commutator_source_intake_ledger_1702.csv",
        QUEUE / "JR1702_COMMUTATOR_SOURCE_INTAKE_LEDGER.csv",
    ],
    FIRST_PRODUCT_RUNNER: [
        QUARANTINE / "FIRST_ARENA_PRODUCT_RUNNER.csv",
        BRANCH_RESIDUALS / "R2FR_first_arena_product_runner_1702.csv",
        QUEUE / "JR1702_FIRST_ARENA_PRODUCT_RUNNER.csv",
    ],
    WEP_SOURCE_WEIGHT: [
        QUARANTINE / "WEP_SOURCE_WEIGHT_PRODUCT_ROW.csv",
        BRANCH_RESIDUALS / "R2FR_WEP_source_weight_product_1702.csv",
        QUEUE / "JR1702_WEP_SOURCE_WEIGHT_PRODUCT_ROW.csv",
    ],
    R10_PPN_PROJECTION: [
        QUARANTINE / "R10_PPN_PROJECTION_ROWS.csv",
        BRANCH_RESIDUALS / "R2FR_R10_PPN_projection_rows_1702.csv",
        QUEUE / "JR1702_R10_PPN_PROJECTION_ROWS.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_1702.csv",
        QUEUE / "JR1702_NEXT_TARGET.csv",
    ],
}


def ensure_dirs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def bool_cell(value: object) -> bool:
    return str(value).strip().lower() == "true"


def list_cell(values: list[object] | tuple[object, ...]) -> str:
    return ";".join(str(value) for value in values)


def has_missing(value: object) -> bool:
    return "MISSING" in str(value).upper()


def markdown_table(rows: list[dict[str, object]], headers: list[str]) -> str:
    if not rows:
        return "_No rows._"
    table = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        table.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(table)


def source_register_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for key, path in SOURCE_FILES.items():
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles = NEEDLES[key]
        needles_present = exists and all(needle in text for needle in needles)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_key": key,
                "source_path": str(path),
                "exists": exists,
                "needles_present": needles_present,
                "required_needles": list_cell(needles),
                "use_in_1702": "commutator source-intake ledger and first arena product runner",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def commutator_ledger_rows() -> list[dict[str, object]]:
    rows = [
        (
            "CR1702_0_universal",
            "C_R[A]",
            "all",
            "Pi_CoeffSource([delta_parent,R_A]T_H)+Pi_CoeffSource(delta_pre R_A)+Pi_CoeffSource(delta_cal R_A)",
            "theorem C_R[A]=0 for map class A or finite product residual",
            "MISSING_MAP_CLASS_ZERO_OR_PRODUCT_ROW",
            "do not infer from pure postprocessing theorem",
        ),
        (
            "CR1702_1_projector",
            "I_commutator",
            "orbital;R10;PPN;local_GR",
            "finite-annulus integral of [d,Pi_M]J_H normalized by M_H_ref",
            "numeric numerator, M_H_ref denominator, linked surfaces, source path, units",
            "MISSING_I_COMMUTATOR_AND_MHREF",
            "1014/1359 source-intake route",
        ),
        (
            "CR1702_2_wep_source_weight",
            "Delta_w_TiPt*tau_WEP",
            "MICROSCOPE_WEP;local_GR",
            "P_WEP_source_weight = Delta_w_TiPt*tau_WEP or direct P_WEP_source",
            "Delta_w theorem/numeric row plus tau_WEP or direct sourced product",
            "MISSING_DELTA_W_TAU_WEP_OR_DIRECT_PRODUCT",
            "1476 and 1067 schemas",
        ),
        (
            "CR1702_3_r10_projection",
            "tau_R10",
            "R10_short_range",
            "alpha_R10(lambda)=K_X(lambda) Qbar_XH(lambda) qbar_XT(lambda) or c_g/tau_R10 branch",
            "lambda_X, Z_X, K_X, Qbar source/test, tau_R10, bound curve",
            "MISSING_R10_PROJECTION_INPUTS",
            "1029 and 947 projection rows",
        ),
        (
            "CR1702_4_ppn_projection",
            "tau_PPN",
            "PPN_weak_field",
            "gamma_minus_1,beta_minus_1=response_operator(profile,gauge)*tau_PPN*c_g plus retained tails",
            "M_gamma, M_beta, tau_PPN, gauge, weak-field profile, disformal/non-Hilbert split",
            "MISSING_PPN_RESPONSE_MATRIX",
            "1029 and 1669 PPN rows",
        ),
        (
            "CR1702_5_clock_projection",
            "tau_clock",
            "clock;EM",
            "P_clock_alpha=b_alpha_EM*tau_clock_time or direct clock product",
            "clock sensitivities, calibration convention, direct product or tau map, source path",
            "MISSING_CLOCK_READOUT_PRODUCT",
            "947 and 988 clock rows",
        ),
        (
            "CR1702_6_branch_transfer",
            "branch_readout_functor",
            "clock;WEP;R10;PPN;EM",
            "same parent branch classifier plus arena product maps before any bound transfer",
            "branch id, coefficient normalization, domain classifier, readout functor, arena kernels",
            "MISSING_CROSS_ARENA_PARENT_MAP",
            "1701 no-transfer guardrail",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "ledger_id": lid,
            "symbol": symbol,
            "affected_arenas": arenas,
            "definition": definition,
            "required_evidence": evidence,
            "current_status": status,
            "source_hint": hint,
            "numeric_input_present": False,
            "theorem_zero_present": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for lid, symbol, arenas, definition, evidence, status, hint in rows
    ]


def product_runner_rows() -> list[dict[str, object]]:
    rows = [
        (
            "PR1702_0_WEP_source_weight",
            "MICROSCOPE_WEP",
            "P_WEP_source_weight",
            "Delta_w_TiPt*tau_WEP or direct P_WEP_source",
            "2.8e-15",
            "dimensionless",
            "MISSING_DELTA_W_TIPT;MISSING_TAU_WEP;MISSING_OFFICIAL_READOUT",
            "BLOCKED_MISSING_INPUTS",
        ),
        (
            "PR1702_1_R10_alpha_lambda",
            "R10_short_range",
            "alpha_R10(lambda)",
            "K_X(lambda)*Qbar_source(lambda)*Qbar_test(lambda)/(4*pi*Z_X*G_obs)",
            "source-backed alpha_bound(lambda)",
            "dimensionless",
            "MISSING_LAMBDA_X;MISSING_Z_X;MISSING_K_X;MISSING_QBAR_SOURCE;MISSING_QBAR_TEST;MISSING_BOUND_CURVE",
            "BLOCKED_MISSING_INPUTS",
        ),
        (
            "PR1702_2_PPN_gamma_beta",
            "PPN_weak_field",
            "PPN_residual_vector",
            "M_gamma*tau_PPN*c_g + M_beta*tau_PPN*c_g + M_dis*b_dis + M_nonH*q_nonH",
            "Cassini/LLR/PPN normalized bounds",
            "dimensionless vector",
            "MISSING_M_GAMMA;MISSING_M_BETA;MISSING_TAU_PPN;MISSING_GAUGE;MISSING_PROFILE;MISSING_TAIL_SPLIT",
            "BLOCKED_MISSING_INPUTS",
        ),
        (
            "PR1702_3_clock_alpha",
            "clock_fine_structure",
            "P_clock_alpha",
            "b_alpha_EM*tau_clock_time or direct clock product",
            "2.1e-18 yr^-1 Yb product row",
            "yr^-1",
            "MISSING_B_ALPHA_EM;MISSING_TAU_CLOCK_OR_DIRECT_PRODUCT;MISSING_CLOCK_READOUT_MODEL",
            "BLOCKED_MISSING_INPUTS",
        ),
        (
            "PR1702_4_orbital_source",
            "orbital_Newton_GM",
            "P_orbital_source",
            "epsilon_radial_Meff or I_commutator/M_H_ref plus source-frame tails",
            "arena-dependent orbital/GM bounds",
            "dimensionless_or_yr^-1",
            "MISSING_I_COMMUTATOR;MISSING_M_H_REF;MISSING_TAU_ORBIT;MISSING_SOURCE_FRAME_LOCK",
            "BLOCKED_MISSING_INPUTS",
        ),
    ]
    output = []
    for rid, arena, observable, formula, bound, units, missing, status in rows:
        output.append(
            {
                "branch_id": BRANCH_ID,
                "runner_row_id": rid,
                "arena": arena,
                "observable": observable,
                "product_formula": formula,
                "comparison_bound": bound,
                "product_units": units,
                "missing_inputs": missing,
                "current_status": status,
                "numeric_input_present": False,
                "theorem_zero_present": False,
                "numeric_comparison_ready": False,
                "abs_predicted_le_bound": "not_evaluated",
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return output


def wep_source_weight_rows() -> list[dict[str, object]]:
    rows = [
        (
            "WEP1702_0_delta_w",
            "Delta_w_TiPt",
            "relative source/action weight after common normalization",
            "parent theorem-zero or numeric source-backed relative weight",
            "MISSING_THEOREM_ZERO_OR_NUMERIC_DELTA_W",
            "1476 DW1476_0",
        ),
        (
            "WEP1702_1_tau_WEP",
            "tau_WEP",
            "normalized local source/orbit/readout projection",
            "theorem-zero, numeric projection integral, or direct product route",
            "MISSING_TAU_WEP",
            "1067 TAQ1067_0..3",
        ),
        (
            "WEP1702_2_official_readout",
            "K_CMSM/P_WEP_readout",
            "official MICROSCOPE readout/design matrix and product convention",
            "CMSM/readout arrays, source worldtube, material tensor, product convention",
            "MISSING_OFFICIAL_MICROSCOPE_READOUT",
            "1699 request pack and 1482 parser blocker",
        ),
        (
            "WEP1702_3_direct_product",
            "P_WEP_source_weight",
            "direct parent product without Delta_w/tau split",
            "numeric/theorem direct product with units/source path",
            "MISSING_DIRECT_PRODUCT",
            "1067 TAQ1067_3",
        ),
        (
            "WEP1702_4_refusal",
            "WEP source-weight runner",
            "reject unity tau, G absorption, cancellation, or unsourced factor choices",
            "all required rows sourced, numeric or theorem-zero, no MISSING markers",
            "REFUSAL_ACTIVE",
            "1067 TAQ1067_4",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "wep_row_id": rid,
            "quantity": quantity,
            "definition": definition,
            "accepted_evidence": evidence,
            "current_status": status,
            "source_hint": hint,
            "numeric_input_present": False,
            "theorem_zero_present": False,
            "passes_required_gate": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for rid, quantity, definition, evidence, status, hint in rows
    ]


def r10_ppn_projection_rows() -> list[dict[str, object]]:
    rows = [
        (
            "RP1702_0_R10_lambda_mass",
            "R10_short_range",
            "lambda_X",
            "finite range from M_X^2/Z_X with units",
            "MISSING_LAMBDA_X",
            "R10 alpha(lambda) cannot be evaluated",
            "PFA947_0;TAU1029_0",
        ),
        (
            "RP1702_1_R10_source_test",
            "R10_short_range",
            "K_X,Qbar_source,Qbar_test,tau_R10",
            "source/test Yukawa profile, normalization, material convention, source path",
            "MISSING_R10_SOURCE_TEST_PROJECTION",
            "alpha_R10(lambda) remains symbolic",
            "PFA947_0;FPM1701_3",
        ),
        (
            "RP1702_2_R10_bound_curve",
            "R10_short_range",
            "alpha_bound(lambda)",
            "source-backed full curve or validated machine-readable table",
            "MISSING_CLAIM_VALID_BOUND_CURVE",
            "comparison cannot be claim-valid",
            "563/1034 bound-curve blockers",
        ),
        (
            "RP1702_3_PPN_response",
            "PPN_weak_field",
            "M_gamma,M_beta,tau_PPN",
            "weak-field response matrix with gauge/profile and tail separation",
            "MISSING_PPN_RESPONSE_MATRIX",
            "gamma/beta residual cannot score",
            "PFA947_1;TAU1029_1;1669 source pack",
        ),
        (
            "RP1702_4_PPN_tail_split",
            "PPN_weak_field",
            "b_dis,q_nonH,Delta_W_support",
            "disformal/non-Hilbert/support-shift residual split with no-cancellation envelope",
            "MISSING_TAIL_SPLIT",
            "PPN vector cannot be assigned to c_g alone",
            "1028/1031 finite fallback",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "projection_row_id": rid,
            "arena": arena,
            "quantity": quantity,
            "required_evidence": evidence,
            "current_status": status,
            "blocks": blocks,
            "source_hint": hint,
            "numeric_input_present": False,
            "theorem_zero_present": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for rid, arena, quantity, evidence, status, blocks, hint in rows
    ]


def runner_rows() -> list[dict[str, object]]:
    rows = [
        ("RUN1702_0_commutator_zero", "claim C_R[A]=0 generally", "REJECT_GENERAL_COMMUTATOR_ZERO", "C_R[A] ledger has missing theorem/product rows"),
        ("RUN1702_1_wep_score", "score WEP source-weight product", "REJECT_WEP_SCORE", "Delta_w, tau_WEP, official readout, and direct product are missing"),
        ("RUN1702_2_r10_score", "score R10 alpha(lambda)", "REJECT_R10_SCORE", "lambda, Z_X, K_X, Qbar source/test, tau_R10, and claim-valid bound curve missing"),
        ("RUN1702_3_ppn_score", "score PPN gamma/beta vector", "REJECT_PPN_SCORE", "M_gamma/M_beta/tau_PPN/gauge/profile/tail split missing"),
        ("RUN1702_4_arena_transfer", "transfer clock/WEP/R10/PPN bounds", "REJECT_ARENA_TRANSFER", "branch_readout_functor remains missing"),
        ("RUN1702_5_local_gr", "claim local GR/Newton", "BLOCKED_NO_CLAIM", "finite product runner is schema-only and source/right-left gates remain open"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": rid,
            "case": case,
            "status": status,
            "reason": reason,
            "can_score": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for rid, case, status, reason in rows
    ]


def next_target_rows() -> list[dict[str, object]]:
    rows = [
        (
            "NEXT1702_0_primary",
            "1703-Y5-R2FR-WEP-source-weight-product-first-fill-or-MICROSCOPE-parser-shell.md",
            "scripts/Y5_R2FR_WEP_source_weight_product_first_fill_or_MICROSCOPE_parser_shell.py",
            "attack the highest local-GR payoff product first: fill or hard-block Delta_w/tau_WEP/direct WEP product using MICROSCOPE source/readout requirements",
            "selected",
        ),
        (
            "NEXT1702_1_r10",
            "1703a-Y5-R2FR-R10-alpha-lambda-projection-fill-runner.md",
            "scripts/Y5_R2FR_R10_alpha_lambda_projection_fill_runner.py",
            "fill R10 lambda/Z/K/Qbar/tau and bound-curve gates after WEP product row",
            "held_fallback",
        ),
        (
            "NEXT1702_2_ppn",
            "1703b-Y5-R2FR-PPN-response-matrix-and-tail-split-runner.md",
            "scripts/Y5_R2FR_PPN_response_matrix_and_tail_split_runner.py",
            "fill PPN response matrices and no-cancellation tail split",
            "held_fallback",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": rid,
            "next_target": target,
            "script": script,
            "objective": objective,
            "selection_status": status,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for rid, target, script, objective, status in rows
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    rows = [
        ("CG1702_0_commutator", "C_R[A] general zero", "BLOCKED_NO_CLAIM", "ledger rows are missing theorem/product evidence"),
        ("CG1702_1_WEP_source_weight", "WEP source-weight product score", "BLOCKED_NO_CLAIM", "Delta_w/tau_WEP/direct product and official readout missing"),
        ("CG1702_2_R10_alpha", "R10 alpha(lambda) score", "BLOCKED_NO_CLAIM", "projection inputs and claim-valid bound curve missing"),
        ("CG1702_3_PPN_vector", "PPN gamma/beta score", "BLOCKED_NO_CLAIM", "response matrix and tail split missing"),
        ("CG1702_4_cross_arena", "cross-arena transfer", "BLOCKED_NO_CLAIM", "branch/readout functor missing"),
        ("CG1702_5_local_GR_Newton", "derived local GR/Newton reduction", "BLOCKED_NO_CLAIM", "product runner is nonclaim schema only"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": cid,
            "claim": claim,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for cid, claim, status, reason in rows
    ]


def all_claim_flags_false(paths: list[Path]) -> bool:
    for path in paths:
        for row in read_csv(path):
            for field in (
                "can_score",
                "accepted_for_scoring",
                "score_ready",
                "valid_prediction_row",
                "valid_for_claim",
                "claim_allowed",
                "numeric_input_present",
                "theorem_zero_present",
                "numeric_comparison_ready",
                "passes_required_gate",
            ):
                if field in row and bool_cell(row[field]):
                    return False
    return True


def copy_outputs() -> None:
    for source_path, target_paths in COPY_TARGETS.items():
        for target_path in target_paths:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, target_path)


def cleanup_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    hits = [
        path
        for path in FORMALIZATION.rglob("*1702*")
        if ".venv" not in path.parts and "__pycache__" not in path.parts
    ]
    return len(hits) == 0


def validate(
    source_rows_: list[dict[str, object]],
    ledger_rows: list[dict[str, object]],
    product_rows: list[dict[str, object]],
    wep_rows: list[dict[str, object]],
    projection_rows: list[dict[str, object]],
    runner_rows_: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    sources_ok = all(bool_cell(row["exists"]) and bool_cell(row["needles_present"]) for row in source_rows_)
    ledger_complete = {"C_R[A]", "I_commutator", "Delta_w_TiPt*tau_WEP", "tau_R10", "tau_PPN", "tau_clock", "branch_readout_functor"}.issubset({str(row["symbol"]) for row in ledger_rows})
    product_runner_complete = {"MICROSCOPE_WEP", "R10_short_range", "PPN_weak_field", "clock_fine_structure", "orbital_Newton_GM"}.issubset({str(row["arena"]) for row in product_rows})
    all_products_blocked = all(row["current_status"] == "BLOCKED_MISSING_INPUTS" and has_missing(row["missing_inputs"]) for row in product_rows)
    wep_schema_complete = {"Delta_w_TiPt", "tau_WEP", "K_CMSM/P_WEP_readout", "P_WEP_source_weight", "WEP source-weight runner"}.issubset({str(row["quantity"]) for row in wep_rows})
    wep_blocked = all(not bool_cell(row["passes_required_gate"]) for row in wep_rows)
    r10_ppn_complete = {"R10_short_range", "PPN_weak_field"}.issubset({str(row["arena"]) for row in projection_rows})
    r10_ppn_blocked = all(not bool_cell(row["score_ready"]) and has_missing(row["current_status"]) for row in projection_rows)
    no_scores = all(not bool_cell(row["score_ready"]) and not bool_cell(row["valid_prediction_row"]) for row in product_rows + wep_rows + projection_rows)
    runner_blocks = all(not bool_cell(row["can_score"]) for row in runner_rows_)
    next_selected = any(row["route_id"] == "NEXT1702_0_primary" and row["selection_status"] == "selected" for row in next_rows)
    local_gr_blocked = any(row["claim"] == "derived local GR/Newton reduction" and row["status"] == "BLOCKED_NO_CLAIM" for row in claim_rows)
    no_claim_flags = all_claim_flags_false(CLAIM_CHECKED)
    csv_parse = True
    for path in GENERATED:
        try:
            read_csv(path)
        except Exception:
            csv_parse = False
    branch_copies = all(target.exists() for targets in COPY_TARGETS.values() for target in targets)
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_ok = formalization_untouched()
    checks = [
        ("VAL1702_0_sources_exist", sources_ok, "all cited local source paths exist and required needles are present"),
        ("VAL1702_1_ledger_complete", ledger_complete, "commutator ledger covers C_R, I_commutator, tau, source-weight, and branch-transfer rows"),
        ("VAL1702_2_product_runner_complete", product_runner_complete, "first product runner covers WEP, R10, PPN, clock, and orbital rows"),
        ("VAL1702_3_products_blocked", all_products_blocked, "all product rows are explicitly blocked by missing inputs"),
        ("VAL1702_4_wep_schema_complete", wep_schema_complete, "WEP source-weight product row covers Delta_w, tau_WEP, readout, direct product, and refusal"),
        ("VAL1702_5_wep_blocked", wep_blocked, "WEP rows do not pass required gates"),
        ("VAL1702_6_r10_ppn_complete", r10_ppn_complete, "R10 and PPN projection rows are present"),
        ("VAL1702_7_r10_ppn_blocked", r10_ppn_blocked, "R10 and PPN rows are missing required projection inputs"),
        ("VAL1702_8_no_scores", no_scores, "no product row is score-ready or claim-valid"),
        ("VAL1702_9_runner_blocks", runner_blocks, "runner blocks commutator, WEP, R10, PPN, arena-transfer, and local-GR claims"),
        ("VAL1702_10_next_selected", next_selected, "next target selects WEP source-weight first fill or MICROSCOPE parser shell"),
        ("VAL1702_11_local_gr_blocked", local_gr_blocked, "local GR/Newton claim remains blocked"),
        ("VAL1702_12_no_claim_flags", no_claim_flags, "all generated scoring and claim flags remain false"),
        ("VAL1702_13_csv_parse", csv_parse, "all generated 1702 CSVs parse"),
        ("VAL1702_14_branch_copies", branch_copies, "branch/quarantine/queue copies exist"),
        ("VAL1702_15_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL1702_16_formalization_untouched", formalization_ok, "no MTS 1702 outputs found under formalization-workbench outside vendor/env folders"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [
        {
            "check_id": cid,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for cid, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1702_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1702 commutator source-intake ledger and first arena product runner validation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def write_doc(
    source_rows_: list[dict[str, object]],
    ledger_rows: list[dict[str, object]],
    product_rows: list[dict[str, object]],
    wep_rows: list[dict[str, object]],
    projection_rows: list[dict[str, object]],
    runner_rows_: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    body = f"""# 1702 - Readout Commutator Ledger And First Arena Product Runner

## Verdict

1702 turns the 1701 readout problem into a runner-shaped ledger. The important shift is that `C_R[A]` is no longer a slogan: every arena now has a named source-intake obstruction and a refusal rule.

The first product runner covers the highest-payoff local branches: WEP source-weight, R10 alpha(lambda), PPN response, clock alpha, and orbital/source normalization. Nothing scores yet. That is the point. Every row carries `MISSING_*` inputs until it has either a parent theorem-zero certificate or a numeric/source-backed product with units, source path, and no-cancellation guard.

The selected next move is WEP source-weight first fill, because it is closest to the coupling problem and already has MICROSCOPE request/parser machinery waiting.

## Source Register

{markdown_table(source_rows_, ["source_key", "source_path", "exists", "needles_present", "use_in_1702"])}

## Commutator Source-Intake Ledger

{markdown_table(ledger_rows, ["ledger_id", "symbol", "affected_arenas", "current_status"])}

## First Arena Product Runner

{markdown_table(product_rows, ["runner_row_id", "arena", "observable", "current_status"])}

## WEP Source-Weight Product Row

{markdown_table(wep_rows, ["wep_row_id", "quantity", "current_status", "source_hint"])}

## R10/PPN Projection Rows

{markdown_table(projection_rows, ["projection_row_id", "arena", "quantity", "current_status"])}

## Runner Refusal

{markdown_table(runner_rows_, ["runner_id", "case", "status", "reason"])}

## Next Target

{markdown_table(next_rows, ["route_id", "next_target", "objective", "selection_status"])}

## Claim Gates

{markdown_table(claim_rows, ["claim_id", "claim", "status", "reason"])}

## Validation

{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Working Interpretation

This is where the theory starts acting like an engineering test rig. The coupling branch is now a set of load paths: WEP has `Delta_w*tau_WEP` or direct product; R10 has `lambda/Z/K/Qbar/tau`; PPN has response matrices and tail split; orbital has `I_commutator/M_H_ref`; clocks have direct products. No more “maybe the readout handles it” fog. The next useful push is to try the WEP source-weight row first.
"""
    DOC.write_text(body, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    source_rows_ = source_register_rows()
    ledger_rows = commutator_ledger_rows()
    product_rows = product_runner_rows()
    wep_rows = wep_source_weight_rows()
    projection_rows = r10_ppn_projection_rows()
    runner_rows_ = runner_rows()
    next_rows = next_target_rows()
    claim_rows = claim_gate_rows()
    write_csv(SOURCE_REGISTER, source_rows_, ["branch_id", "source_key", "source_path", "exists", "needles_present", "required_needles", "use_in_1702", "valid_for_claim", "claim_allowed"])
    write_csv(COMMUTATOR_LEDGER, ledger_rows, ["branch_id", "ledger_id", "symbol", "affected_arenas", "definition", "required_evidence", "current_status", "source_hint", "numeric_input_present", "theorem_zero_present", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(FIRST_PRODUCT_RUNNER, product_rows, ["branch_id", "runner_row_id", "arena", "observable", "product_formula", "comparison_bound", "product_units", "missing_inputs", "current_status", "numeric_input_present", "theorem_zero_present", "numeric_comparison_ready", "abs_predicted_le_bound", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(WEP_SOURCE_WEIGHT, wep_rows, ["branch_id", "wep_row_id", "quantity", "definition", "accepted_evidence", "current_status", "source_hint", "numeric_input_present", "theorem_zero_present", "passes_required_gate", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(R10_PPN_PROJECTION, projection_rows, ["branch_id", "projection_row_id", "arena", "quantity", "required_evidence", "current_status", "blocks", "source_hint", "numeric_input_present", "theorem_zero_present", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(RUNNER, runner_rows_, ["branch_id", "runner_id", "case", "status", "reason", "can_score", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(NEXT_TARGET, next_rows, ["branch_id", "route_id", "next_target", "script", "objective", "selection_status", "valid_for_claim", "claim_allowed"])
    write_csv(CLAIM_GATE, claim_rows, ["branch_id", "claim_id", "claim", "status", "reason", "valid_for_claim", "claim_allowed"])
    copy_outputs()
    cleanup_pycache()
    validation_rows = validate(source_rows_, ledger_rows, product_rows, wep_rows, projection_rows, runner_rows_, next_rows, claim_rows)
    write_csv(VALIDATION, validation_rows, ["check_id", "result", "detail", "valid_for_claim", "claim_allowed"])
    write_doc(source_rows_, ledger_rows, product_rows, wep_rows, projection_rows, runner_rows_, next_rows, claim_rows, validation_rows)
    failed = [row for row in validation_rows if row["result"] != "PASS"]
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("1702 validation PASS")


if __name__ == "__main__":
    main()

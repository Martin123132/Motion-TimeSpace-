from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1701"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "1701-Y5-R2FR-readout-effective-no-reentry-theorem-or-finite-product-map.md"

SOURCE_FILES = {
    "1700_doc": ROOT / "1700-Y5-R2FR-parent-grammar-exhaustiveness-proof-or-readout-no-reentry.md",
    "1700_validation": OUT / "P8_Y5_BRR545_1700_VALIDATION.csv",
    "1700_readout_target": OUT / "P8_Y5_PARENT_QLOC_1700_READOUT_NO_REENTRY_TARGET.csv",
    "1700_signoff_contract": OUT / "P8_Y5_PARENT_QLOC_1700_PARENT_ACTION_SIGNOFF_CONTRACT.csv",
    "1014_commutator": ROOT / "1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md",
    "1454_variation_before_readout": MICROSCOPE / "branch_locked_wep" / "coefficients" / "variation_before_readout_theorem_attempt_1454.csv",
    "1469_alpha_product_runner": MICROSCOPE / "branch_locked_wep" / "coefficients" / "alpha_residual_product_runner_nonclaim_1469.csv",
    "1476_source_weight": MICROSCOPE / "branch_locked_wep" / "coefficients" / "Ci_source_weight_delta_w_input_nonclaim_1476.csv",
    "1028_frame_marker_pack": ROOT / "1028-Y5-R10-frame-marker-coupling-bound-input-pack-or-no-marker-theorem.md",
    "1029_cg_tau": ROOT / "1029-Y5-R10-cg-no-shadow-frame-theorem-or-first-numeric-coupling-row.md",
    "1031_spm_closure": ROOT / "1031-Y5-R10-quotient-naturality-terminal-public-metric-proof-or-spm-closure.md",
    "988_alpha_clock_wep": ROOT / "988-Y5-R10-alphaEM-WEP-clock-joint-prior-or-EM-lock-theorem.md",
}

NEEDLES = {
    "1700_doc": ["READOUT_NO_REENTRY_SELECTED", "1701-Y5-R2FR-readout-effective-no-reentry-theorem-or-finite-product-map.md"],
    "1700_validation": ["VAL1700_OVERALL", "PASS"],
    "1700_readout_target": ["RNR1700_2_commutator", "formula_target"],
    "1700_signoff_contract": ["SIG1700_5_readout_no_reentry", "selected_next"],
    "1014_commutator": ["PCT1014_0_product_rule", "PCT1014_5_no_readout_mask"],
    "1454_variation_before_readout": ["VBR1454_6_verdict", "CONDITIONAL_THEOREM_NOT_PARENT_SIGNED"],
    "1469_alpha_product_runner": ["APR1469_1_WEP_alpha", "BLOCKED_MISSING_INPUTS"],
    "1476_source_weight": ["DW1476_1_tau_WEP_dependency", "MISSING_TAU_WEP"],
    "1028_frame_marker_pack": ["FMB1028_1_tau_R10", "MISSING_ARENA_PROJECTION"],
    "1029_cg_tau": ["TAU1029_0_R10", "MISSING_TAU_R10_AND_PARENT_CG"],
    "1031_spm_closure": ["SPMC1031_0_closure_name", "AVAILABLE_AS_CLOSURE_ONLY"],
    "988_alpha_clock_wep": ["JAV988_1_clock_product", "source_backed_product_bound_nonclaim"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1701_SOURCE_REGISTER.csv"
COMMUTATOR_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1701_READOUT_COMMUTATOR_AUDIT.csv"
NO_REENTRY_THEOREM = OUT / "P8_Y5_PARENT_QLOC_1701_NO_REENTRY_THEOREM_ATTEMPT.csv"
FINITE_PRODUCT_MAP = OUT / "P8_Y5_PARENT_QLOC_1701_ARENA_FINITE_PRODUCT_MAP.csv"
RESIDUAL_QUEUE = OUT / "P8_Y5_PARENT_QLOC_1701_READOUT_RESIDUAL_QUEUE.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1701_RUNNER_REFUSAL.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1701_NEXT_TARGET.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1701_CLAIM_GATE.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1701_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    COMMUTATOR_AUDIT,
    NO_REENTRY_THEOREM,
    FINITE_PRODUCT_MAP,
    RESIDUAL_QUEUE,
    RUNNER,
    NEXT_TARGET,
    CLAIM_GATE,
]

CLAIM_CHECKED = [
    COMMUTATOR_AUDIT,
    NO_REENTRY_THEOREM,
    FINITE_PRODUCT_MAP,
    RESIDUAL_QUEUE,
    RUNNER,
    NEXT_TARGET,
    CLAIM_GATE,
]

COPY_TARGETS = {
    COMMUTATOR_AUDIT: [
        QUARANTINE / "READOUT_COMMUTATOR_AUDIT.csv",
        BRANCH_RESIDUALS / "R2FR_readout_commutator_audit_1701.csv",
        QUEUE / "JR1701_READOUT_COMMUTATOR_AUDIT.csv",
    ],
    NO_REENTRY_THEOREM: [
        QUARANTINE / "NO_REENTRY_THEOREM_ATTEMPT.csv",
        BRANCH_RESIDUALS / "R2FR_no_reentry_theorem_attempt_1701.csv",
        QUEUE / "JR1701_NO_REENTRY_THEOREM_ATTEMPT.csv",
    ],
    FINITE_PRODUCT_MAP: [
        QUARANTINE / "ARENA_FINITE_PRODUCT_MAP.csv",
        BRANCH_RESIDUALS / "R2FR_arena_finite_product_map_1701.csv",
        QUEUE / "JR1701_ARENA_FINITE_PRODUCT_MAP.csv",
    ],
    RESIDUAL_QUEUE: [
        QUARANTINE / "READOUT_RESIDUAL_QUEUE.csv",
        BRANCH_RESIDUALS / "R2FR_readout_residual_queue_1701.csv",
        QUEUE / "JR1701_READOUT_RESIDUAL_QUEUE.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_1701.csv",
        QUEUE / "JR1701_NEXT_TARGET.csv",
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
                "use_in_1701": "readout/effective no-reentry theorem attempt and finite product map",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def commutator_audit_rows() -> list[dict[str, object]]:
    rows = [
        (
            "RC1701_0_define_residual",
            "readout reentry residual",
            "C_R[A] := Pi_CoeffSource([delta_parent,R_A]T_H) + Pi_CoeffSource(delta_pre R_A) + Pi_CoeffSource(delta_cal R_A)",
            "definition_sharp",
            "names the source-coefficient part of a post-variation/effective map",
            "not zero by definition",
        ),
        (
            "RC1701_1_pure_postprocessing",
            "pure data map",
            "R_post: Sol(S_parent)/G -> Data_A with no arrow back to S_parent or E_H",
            "commutator_harmless_by_type",
            "cannot redefine the parent source; it only reports an observable",
            "requires strict no-feedback typing",
        ),
        (
            "RC1701_2_projection_operator",
            "projector/domain map",
            "d(Pi J)=Pi dJ + [d,Pi]J and delta Pi may carry stress/source terms",
            "retained_residual",
            "1014 shows product-rule obstruction is active unless chain map is signed",
            "I_commutator/projector-stress rows remain unfilled",
        ),
        (
            "RC1701_3_effective_action",
            "EFT/radiative map",
            "S_eff = S_parent + DeltaS_eff[R, cutoff, fields] before variation",
            "no_reentry_fails_if_prevariation",
            "effective coefficients can become real parent-source coefficients",
            "needs separate EFT coefficient-domain theorem",
        ),
        (
            "RC1701_4_calibration_feedback",
            "calibration/source-worldtube feedback",
            "calibration or source mask chosen from data then used as parent source normalizer",
            "forbidden_as_derivation",
            "would smuggle measured GM/WEP/readout into the source equation",
            "must be fixed before variation or retained finite",
        ),
        (
            "RC1701_5_material_or_clock_readout",
            "material/clock response map",
            "R_A depends on material constants, clock sensitivities, or alpha_EM coefficients",
            "arena_product_required",
            "cannot transfer clock/WEP/R10 constraints without a signed branch map",
            "finite product rows required",
        ),
        (
            "RC1701_6_verdict",
            "general readout no-reentry",
            "C_R[A]=0 for every readout/effective/arena map",
            "GENERAL_NO_REENTRY_NOT_DERIVED",
            "pure postprocessing is safe; general readout/effective maps are not theorem-zero",
            "split finite products by arena",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": aid,
            "map_class": cls,
            "formal_statement": statement,
            "result": result,
            "meaning": meaning,
            "remaining_requirement": requirement,
            "parent_derived": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for aid, cls, statement, result, meaning, requirement in rows
    ]


def no_reentry_theorem_rows() -> list[dict[str, object]]:
    rows = [
        (
            "NRE1701_0_type_theorem",
            "PurePostprocessingNoSourceReentry",
            "If R_post is only a map from already-solved parent states to data and is absent from S_parent, then delta S_parent/delta fields is unchanged by R_post.",
            "conditional_theorem_pass",
            "This is a type/order theorem, not a physics fit.",
            "does not cover S_eff, projection commutators, calibration feedback, or material maps",
        ),
        (
            "NRE1701_1_variation_order",
            "VariationBeforeReadout",
            "T_H := delta S_matter/delta e_obs is formed before material selector, orbit/readout kernel, calibration, or source-worldtube projection.",
            "conditional_from_1454",
            "post-selector c_A cannot become a parent source if it truly occurs after variation.",
            "parent action/domain owner and official readout model remain unsigned/absent",
        ),
        (
            "NRE1701_2_preaction_weights",
            "PreActionWeightsSurvive",
            "S_matter=sum_A w_A S_A or an effective action with source weights before variation gives T_H=sum_A w_A T_A.",
            "counterexample_active",
            "no readout-order theorem kills coefficients already inside the action.",
            "requires source-owner grammar/exhaustiveness or finite Delta_w row",
        ),
        (
            "NRE1701_3_projector_commutator",
            "ProjectorCommutatorSurvives",
            "If a readout/projector depends on fields, domains, or source support, [delta_parent,R] and [d,Pi] terms may source residuals.",
            "counterexample_active",
            "1014 keeps I_commutator and projector-stress residuals live.",
            "requires chain-map theorem or sourced residual row",
        ),
        (
            "NRE1701_4_arena_transfer",
            "NoArenaTransfer",
            "Clock, WEP, R10, PPN, orbital, and EM readouts are distinct product maps unless a parent branch/readout functor is signed.",
            "guardrail_pass",
            "prevents using one arena's bound as another arena's pass.",
            "requires arena-specific finite product maps",
        ),
        (
            "NRE1701_5_verdict",
            "NoReentryTheoremStatus",
            "Pure postprocessing no-reentry is conditionally safe; general readout/effective no-reentry is not derived.",
            "PURE_POSTPROCESSING_ONLY_GENERAL_BLOCKED",
            "This narrows the problem without closing local GR.",
            "finite product map becomes mandatory for scoring",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": tid,
            "theorem_piece": piece,
            "formal_statement": statement,
            "status": status,
            "what_it_gives": gives,
            "what_it_does_not_cover": misses,
            "parent_derived": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for tid, piece, statement, status, gives, misses in rows
    ]


def finite_product_map_rows() -> list[dict[str, object]]:
    rows = [
        (
            "FPM1701_0_WEP_source_weight",
            "MICROSCOPE_WEP",
            "P_WEP_source_weight = Delta_w_TiPt * tau_WEP or direct P_WEP_source",
            "Delta_w_TiPt;tau_WEP;official readout matrix;source worldtube;product convention",
            "eta_TiPt or direct WEP product",
            "1476 source-weight rows",
            "MISSING_DELTA_W_OR_TAU_WEP_OR_OFFICIAL_READOUT",
        ),
        (
            "FPM1701_1_clock_alpha",
            "clock_fine_structure",
            "P_clock_alpha = b_alpha_EM * tau_clock_time or direct clock product",
            "b_alpha_EM;tau_clock_time;clock sensitivities;calibration convention;source path",
            "clock drift product bound",
            "1469 APR1469_0 and 988 clock product",
            "MISSING_DIRECT_P_CLOCK_ALPHA",
        ),
        (
            "FPM1701_2_WEP_alpha",
            "MICROSCOPE_WEP_alpha",
            "P_WEP_alpha = DeltaQ_alpha_AB * beta_source_alpha * b_alpha_EM * tau_WEP",
            "DeltaQ_alpha_AB;beta_source_alpha;b_alpha_EM;tau_WEP;material/readout composition matrix",
            "dimensionless eta_alpha contribution",
            "1469 APR1469_1",
            "MISSING_BETA_SOURCE_ALPHA_TAU_WEP_MATERIAL_MAP",
        ),
        (
            "FPM1701_3_R10_alpha_lambda",
            "R10_short_range",
            "alpha_R10(lambda)=K_X(lambda)*Qbar_source(lambda)*Qbar_test(lambda)/(4*pi*Z_X*G_obs)",
            "lambda_X;Z_X;K_X;Qbar_source;Qbar_test;tau_R10;bound curve;units",
            "alpha(lambda) comparator",
            "1028/1029 tau_R10 rows and 1469 APR1469_2",
            "MISSING_ALPHA_LAMBDA_PREDICTION_OR_BOUND_CURVE",
        ),
        (
            "FPM1701_4_PPN_frame_vector",
            "PPN_weak_field",
            "P_PPN = M_gamma*tau_PPN*c_g + M_beta*tau_PPN*c_g + M_dis*b_dis + M_nonH*q_nonH",
            "c_g;tau_PPN;M_gamma;M_beta;gauge;profile;disformal split;q_nonH",
            "gamma,beta,preferred-frame residual vector",
            "1028/1029/1031 finite c_g/tau_PPN route",
            "MISSING_PPN_RESPONSE_MATRIX",
        ),
        (
            "FPM1701_5_orbital_GM_source",
            "orbital_Newton_GM",
            "P_orbital = dln_Geff_dt or epsilon_radial_Meff or I_commutator/M_H_ref envelope",
            "M_H_ref;I_commutator;R_eq;B_zero_flux;Delta_frame_source;tau_orbit;source path",
            "GM/Gdot/orbital residual",
            "1014 commutator and source-normalization ledgers",
            "MISSING_MHREF_AND_SOURCE_MEASURE_PROJECTION",
        ),
        (
            "FPM1701_6_EM_alpha_lock",
            "EM_fine_structure",
            "P_EM = b_alpha_EM with explicit parent EM-lock theorem or arena-specific clock/WEP/R10 products",
            "b_alpha_EM;EM kinetic owner theorem;counterterm/no-hidden proof;arena product map",
            "EM/alpha branch classifier",
            "1469/988 alpha rows",
            "MISSING_EM_LOCK_OR_NUMERIC_ALPHA_COEFFICIENT",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "product_id": pid,
            "arena": arena,
            "product_formula": formula,
            "required_inputs": inputs,
            "observable_link": observable,
            "source_hint": source,
            "current_status": status,
            "numeric_input_present": False,
            "theorem_zero_present": False,
            "numeric_comparison_ready": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for pid, arena, formula, inputs, observable, source, status in rows
    ]


def residual_queue_rows() -> list[dict[str, object]]:
    rows = [
        ("RQ1701_0_C_R", "C_R[A]", "readout/effective source-coefficient reentry residual", "all arenas", "must be theorem-zero for pure no-reentry or decomposed into product rows", "retained_nonclaim"),
        ("RQ1701_1_I_commutator", "I_commutator", "projector/product-rule commutator residual", "orbital;R10;PPN;local_GR", "1014 source-backed row still missing", "retained_nonclaim"),
        ("RQ1701_2_Delta_w_tau", "Delta_w_TiPt*tau_WEP", "relative source/action weight WEP product", "WEP;local_GR", "1476 tau_WEP and Delta_w missing", "retained_nonclaim"),
        ("RQ1701_3_tau_R10", "tau_R10", "R10 source/test projection factor", "R10", "1028/1029 projection missing", "retained_nonclaim"),
        ("RQ1701_4_tau_PPN", "tau_PPN", "weak-field response projection", "PPN;orbital;local_GR", "response matrix/gauge missing", "retained_nonclaim"),
        ("RQ1701_5_tau_clock", "tau_clock", "clock/EM readout projection", "clock;EM", "direct clock product or tau map missing", "retained_nonclaim"),
        ("RQ1701_6_arena_branch_map", "branch_readout_functor", "cross-arena transfer map", "clock;WEP;R10;PPN;EM", "no bound transfer until signed", "retained_nonclaim"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "queue_id": qid,
            "symbol": symbol,
            "meaning": meaning,
            "affected_arenas": arenas,
            "needed_evidence": evidence,
            "status": status,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for qid, symbol, meaning, arenas, evidence, status in rows
    ]


def runner_rows() -> list[dict[str, object]]:
    rows = [
        ("RUN1701_0_general_no_reentry", "claim general readout/effective no-reentry", "REJECT_GENERAL_NO_REENTRY", "only pure postprocessing theorem is conditionally safe"),
        ("RUN1701_1_pure_postprocess_as_local_GR", "use pure postprocessing theorem as local-GR proof", "REJECT_OVERPROMOTION", "pre-action, effective, projector, and finite arena maps remain open"),
        ("RUN1701_2_Delta_w_zero", "set Delta_w_A=0", "REJECT_DELTA_W_ZERO", "pre-action weights and source-owner grammar remain unsigned"),
        ("RUN1701_3_arena_transfer", "transfer clock/WEP/R10 bounds across arenas", "REJECT_ARENA_TRANSFER", "branch/readout functor is not signed"),
        ("RUN1701_4_score_products", "score finite product maps", "REJECT_SCORE", "all product rows are missing required numeric/theorem inputs"),
        ("RUN1701_5_local_gr", "claim local GR/Newton", "BLOCKED_NO_CLAIM", "right-hand source/readout and left-hand field-equation gates remain open"),
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
            "NEXT1701_0_primary",
            "1702-Y5-R2FR-readout-commutator-ledger-and-first-arena-product-runner.md",
            "scripts/Y5_R2FR_readout_commutator_ledger_and_first_arena_product_runner.py",
            "turn C_R[A] into an arena-by-arena source-intake ledger and build the first finite product runner, prioritizing WEP source-weight and R10/PPN projection fields",
            "selected",
        ),
        (
            "NEXT1701_1_theory",
            "1702a-Y5-R2FR-pure-postprocessing-readout-type-theorem.md",
            "scripts/Y5_R2FR_pure_postprocessing_readout_type_theorem.py",
            "formalize the safe pure-postprocessing theorem as a reusable lemma with explicit exclusions",
            "held_fallback",
        ),
        (
            "NEXT1701_2_empirical",
            "1702b-Y5-R2FR-arena-product-map-runner.md",
            "scripts/Y5_R2FR_arena_product_map_runner.py",
            "validate finite product rows for WEP, R10, PPN, clocks, orbital, and EM with refusal gates",
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
        ("CG1701_0_general_no_reentry", "general readout/effective no-reentry theorem", "BLOCKED_NO_CLAIM", "pure postprocessing only; effective/projector/calibration maps remain open"),
        ("CG1701_1_Delta_w", "Delta_w_A=0 theorem", "BLOCKED_NO_CLAIM", "pre-action/source-owner branch not closed"),
        ("CG1701_2_finite_products", "finite product maps scoreable", "BLOCKED_NO_CLAIM", "all product rows missing numeric/theorem inputs"),
        ("CG1701_3_arena_transfer", "cross-arena readout transfer", "BLOCKED_NO_CLAIM", "branch/readout functor not signed"),
        ("CG1701_4_WEP_R10_PPN_clock_orbital", "local arenas pass", "BLOCKED_NO_CLAIM", "readout products are schema-only"),
        ("CG1701_5_local_GR_Newton", "derived local GR/Newton reduction", "BLOCKED_NO_CLAIM", "source/readout and field-equation gates remain open"),
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
                "parent_derived",
                "numeric_input_present",
                "theorem_zero_present",
                "numeric_comparison_ready",
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


def validate(
    source_rows_: list[dict[str, object]],
    commutator_rows: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    product_rows: list[dict[str, object]],
    queue_rows: list[dict[str, object]],
    runner_rows_: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    sources_ok = all(bool_cell(row["exists"]) and bool_cell(row["needles_present"]) for row in source_rows_)
    commutator_defined = any(row["audit_id"] == "RC1701_0_define_residual" and row["result"] == "definition_sharp" for row in commutator_rows)
    pure_post_safe = any(row["theorem_id"] == "NRE1701_0_type_theorem" and row["status"] == "conditional_theorem_pass" for row in theorem_rows)
    general_blocked = any(row["audit_id"] == "RC1701_6_verdict" and row["result"] == "GENERAL_NO_REENTRY_NOT_DERIVED" for row in commutator_rows)
    preaction_counterexample = any(row["theorem_id"] == "NRE1701_2_preaction_weights" and row["status"] == "counterexample_active" for row in theorem_rows)
    arena_guardrail = any(row["theorem_id"] == "NRE1701_4_arena_transfer" and row["status"] == "guardrail_pass" for row in theorem_rows)
    required_arenas = {"MICROSCOPE_WEP", "clock_fine_structure", "MICROSCOPE_WEP_alpha", "R10_short_range", "PPN_weak_field", "orbital_Newton_GM", "EM_fine_structure"}
    finite_products_complete = required_arenas.issubset({str(row["arena"]) for row in product_rows})
    finite_products_nonclaim = all(
        not bool_cell(row["numeric_input_present"]) and not bool_cell(row["theorem_zero_present"]) and not bool_cell(row["score_ready"])
        for row in product_rows
    )
    queue_complete = {"C_R[A]", "I_commutator", "Delta_w_TiPt*tau_WEP", "tau_R10", "tau_PPN", "tau_clock", "branch_readout_functor"}.issubset({str(row["symbol"]) for row in queue_rows})
    runner_blocks = all(not bool_cell(row["can_score"]) for row in runner_rows_)
    next_selected = any(row["route_id"] == "NEXT1701_0_primary" and row["selection_status"] == "selected" for row in next_rows)
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
    if FORMALIZATION.exists():
        formalization_hits = [
            path
            for path in FORMALIZATION.rglob("*1701*")
            if ".venv" not in path.parts and "__pycache__" not in path.parts
        ]
        formalization_untouched = len(formalization_hits) == 0
    else:
        formalization_untouched = True
    checks = [
        ("VAL1701_0_sources_exist", sources_ok, "all cited local source paths exist and required needles are present"),
        ("VAL1701_1_commutator_defined", commutator_defined, "readout reentry commutator/residual is defined"),
        ("VAL1701_2_pure_postprocessing_safe", pure_post_safe, "pure postprocessing readout theorem is conditional-safe"),
        ("VAL1701_3_general_no_reentry_blocked", general_blocked, "general readout/effective no-reentry is not promoted"),
        ("VAL1701_4_preaction_counterexample", preaction_counterexample, "pre-action weights remain active counterexample"),
        ("VAL1701_5_arena_guardrail", arena_guardrail, "no cross-arena bound transfer is enforced"),
        ("VAL1701_6_finite_products_complete", finite_products_complete, "finite product maps cover WEP, clock, R10, PPN, orbital, and EM arenas"),
        ("VAL1701_7_finite_products_nonclaim", finite_products_nonclaim, "finite product maps remain missing-input nonclaim rows"),
        ("VAL1701_8_queue_complete", queue_complete, "readout residual queue includes commutator, tau, source-weight, and branch-map rows"),
        ("VAL1701_9_runner_blocks", runner_blocks, "runner blocks no-reentry, product scoring, arena transfer, and local-GR claims"),
        ("VAL1701_10_next_selected", next_selected, "next target selects commutator ledger and first arena product runner"),
        ("VAL1701_11_local_gr_blocked", local_gr_blocked, "local GR/Newton claim remains blocked"),
        ("VAL1701_12_no_claim_flags", no_claim_flags, "all generated scoring and claim flags remain false"),
        ("VAL1701_13_csv_parse", csv_parse, "all generated 1701 CSVs parse"),
        ("VAL1701_14_branch_copies", branch_copies, "branch/quarantine/queue copies exist"),
        ("VAL1701_15_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL1701_16_formalization_untouched", formalization_untouched, "no MTS 1701 outputs found under formalization-workbench outside vendor/env folders"),
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
            "check_id": "VAL1701_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1701 readout no-reentry theorem attempt and finite product map validation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def write_doc(
    source_rows_: list[dict[str, object]],
    commutator_rows: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    product_rows: list[dict[str, object]],
    queue_rows: list[dict[str, object]],
    runner_rows_: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    body = f"""# 1701 - Readout Effective No-Reentry Theorem Or Finite Product Map

## Verdict

1701 gets the useful half of the theorem and refuses the dangerous half.

Pure post-processing readout is safe by type: if a readout map is applied only after the parent equations are varied and solved, and it has no arrow back into `S_parent` or the field equation, it cannot redefine the parent source. Good. That kills a certain kind of fake post-selector coupling.

But general readout/effective no-reentry is **not** derived. Projection operators can have commutators, effective actions can introduce coefficients before variation, calibration/source masks can feed back if used as source definitions, and clock/WEP/R10/PPN/orbital/EM readouts are different product maps. So the safe statement is narrow, and the rest must become finite arena-specific products.

## Source Register

{markdown_table(source_rows_, ["source_key", "source_path", "exists", "needles_present", "use_in_1701"])}

## Readout Commutator Audit

{markdown_table(commutator_rows, ["audit_id", "map_class", "result", "remaining_requirement"])}

## No-Reentry Theorem Attempt

{markdown_table(theorem_rows, ["theorem_id", "theorem_piece", "status", "what_it_does_not_cover"])}

## Arena Finite Product Map

{markdown_table(product_rows, ["product_id", "arena", "product_formula", "current_status"])}

## Readout Residual Queue

{markdown_table(queue_rows, ["queue_id", "symbol", "affected_arenas", "status"])}

## Runner Refusal

{markdown_table(runner_rows_, ["runner_id", "case", "status", "reason"])}

## Next Target

{markdown_table(next_rows, ["route_id", "next_target", "objective", "selection_status"])}

## Claim Gates

{markdown_table(claim_rows, ["claim_id", "claim", "status", "reason"])}

## Validation

{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Working Interpretation

This is a good engineering checkpoint. We can now say exactly which readout move is harmless and exactly where the dragons still live. The next job is not another vague proof attempt; it is a commutator/product ledger with first arena-product runner rows. That will let us test the coupling branch without smuggling clock bounds into WEP, WEP bounds into R10, or readout choices into the parent action.
"""
    DOC.write_text(body, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    source_rows_ = source_register_rows()
    commutator_rows = commutator_audit_rows()
    theorem_rows = no_reentry_theorem_rows()
    product_rows = finite_product_map_rows()
    queue_rows = residual_queue_rows()
    runner_rows_ = runner_rows()
    next_rows = next_target_rows()
    claim_rows = claim_gate_rows()
    write_csv(SOURCE_REGISTER, source_rows_, ["branch_id", "source_key", "source_path", "exists", "needles_present", "required_needles", "use_in_1701", "valid_for_claim", "claim_allowed"])
    write_csv(COMMUTATOR_AUDIT, commutator_rows, ["branch_id", "audit_id", "map_class", "formal_statement", "result", "meaning", "remaining_requirement", "parent_derived", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(NO_REENTRY_THEOREM, theorem_rows, ["branch_id", "theorem_id", "theorem_piece", "formal_statement", "status", "what_it_gives", "what_it_does_not_cover", "parent_derived", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(FINITE_PRODUCT_MAP, product_rows, ["branch_id", "product_id", "arena", "product_formula", "required_inputs", "observable_link", "source_hint", "current_status", "numeric_input_present", "theorem_zero_present", "numeric_comparison_ready", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(RESIDUAL_QUEUE, queue_rows, ["branch_id", "queue_id", "symbol", "meaning", "affected_arenas", "needed_evidence", "status", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(RUNNER, runner_rows_, ["branch_id", "runner_id", "case", "status", "reason", "can_score", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(NEXT_TARGET, next_rows, ["branch_id", "route_id", "next_target", "script", "objective", "selection_status", "valid_for_claim", "claim_allowed"])
    write_csv(CLAIM_GATE, claim_rows, ["branch_id", "claim_id", "claim", "status", "reason", "valid_for_claim", "claim_allowed"])
    copy_outputs()
    cleanup_pycache()
    validation_rows = validate(source_rows_, commutator_rows, theorem_rows, product_rows, queue_rows, runner_rows_, next_rows, claim_rows)
    write_csv(VALIDATION, validation_rows, ["check_id", "result", "detail", "valid_for_claim", "claim_allowed"])
    write_doc(source_rows_, commutator_rows, theorem_rows, product_rows, queue_rows, runner_rows_, next_rows, claim_rows, validation_rows)
    failed = [row for row in validation_rows if row["result"] != "PASS"]
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("1701 validation PASS")


if __name__ == "__main__":
    main()

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
QUARANTINE = MICROSCOPE / "quarantine" / "1664"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1664-Y5-R2FR-Gamma-Khat-metric-response-source-formula-or-Helmholtz-obstruction.md"

EPSILON_FRAME_LEAK_M1 = 2.43238775e-13
CONDITIONAL_CURVATURE_BOUND_M1 = 1.23573661e-23
FRAME_RATIO = 1.96837071e10

SOURCE_FILES = {
    "1663_doc": ROOT / "1663-Y5-R2FR-parent-q_loc-tensor-action-clause-or-frame-leak-coefficient.md",
    "1663_validation": OUT / "P8_Y5_BRR545_1663_VALIDATION.csv",
    "515_match_audit": OUT / "P8_GK_METRIC_RESPONSE_MATCH_AUDIT.csv",
    "515_pass_fail": OUT / "P8_GK_METRIC_RESPONSE_PASS_FAIL.csv",
    "515_source_evidence": OUT / "P8_GK_METRIC_RESPONSE_SOURCE_EVIDENCE.csv",
    "514_candidates": OUT / "P8_GK_STRESS_ACTION_CANDIDATES.csv",
    "1526_variation": OUT / "P8_Y5_PARENT_QLOC_1526_VARIATION_DERIVATION.csv",
    "1527_khat_adoption": OUT / "P8_Y5_PARENT_QLOC_1527_KHAT_ADOPTION_ROW.csv",
    "1618_helmholtz": OUT / "P8_Y5_PARENT_QLOC_1618_HELMHOLTZ_AUDIT.csv",
    "1619_calculability": OUT / "P8_Y5_PARENT_QLOC_1619_METRIC_HELMHOLTZ_CALCULABILITY.csv",
    "1619_normal_form": OUT / "P8_Y5_PARENT_QLOC_1619_POSITIVE_AUXILIARY_NORMAL_FORM.csv",
    "1649_symbol_match": OUT / "P8_Y5_PARENT_QLOC_1649_REDUCED_GK_SYMBOL_MATCH_AUDIT.csv",
}

NEEDLES = {
    "1663_doc": ["K_hat is the metric response of sqrt(-g) Gamma_eff", "epsilon_frame_leak"],
    "1663_validation": ["VAL1663_OVERALL", "PASS"],
    "515_match_audit": ["MA515_0_Gamma_scalar_density_owner", "fail_for_current_claim"],
    "515_pass_fail": ["PF515_1_Gamma_owner_found", "fail"],
    "515_source_evidence": ["E515_4_source_current_audit", "promising_template"],
    "514_candidates": ["GK514_A_metric_response_scalar_density", "best_candidate_not_matched_to_existing_MTS"],
    "1526_variation": ["VAR1526_3_tracefree_projection", "EXACT_TRACEFREE_MATCH_DERIVED"],
    "1527_khat_adoption": ["KAD1527_4_verdict", "STAGED_NOT_PROMOTED"],
    "1618_helmholtz": ["HLA1618_5_verdict", "HELMHOLTZ_NOT_RUNNABLE_INPUTS_MISSING"],
    "1619_calculability": ["CAL1619_5_verdict", "FORMAL_CALCULABILITY_CLOSED_PARENT_SIGNATURE_OPEN"],
    "1619_normal_form": ["NF1619_6_verdict", "FORMAL_MECHANISM_EXISTS_NOT_PARENT_SIGNED"],
    "1649_symbol_match": ["RGM1649_7_verdict", "FAIL_CURRENT_CORPUS"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1664_SOURCE_REGISTER.csv"
SOURCE_FORMULA_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1664_GAMMA_KHAT_SOURCE_FORMULA_AUDIT.csv"
METRIC_RESPONSE_TEST = OUT / "P8_Y5_PARENT_QLOC_1664_METRIC_RESPONSE_TEST.csv"
HELMHOLTZ_OBSTRUCTION = OUT / "P8_Y5_PARENT_QLOC_1664_HELMHOLTZ_OBSTRUCTION.csv"
RESCUE_ROUTE_MATRIX = OUT / "P8_Y5_PARENT_QLOC_1664_RESCUE_ROUTE_MATRIX.csv"
RETAINED_COEFFICIENTS = OUT / "P8_Y5_PARENT_QLOC_1664_RETAINED_COEFFICIENTS.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1664_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1664_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1664_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1664_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    SOURCE_FORMULA_AUDIT,
    METRIC_RESPONSE_TEST,
    HELMHOLTZ_OBSTRUCTION,
    RESCUE_ROUTE_MATRIX,
    RETAINED_COEFFICIENTS,
    CLAIM_GATE,
    DECISION,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    SOURCE_FORMULA_AUDIT,
    METRIC_RESPONSE_TEST,
    HELMHOLTZ_OBSTRUCTION,
    RESCUE_ROUTE_MATRIX,
    RETAINED_COEFFICIENTS,
    CLAIM_GATE,
    DECISION,
    NEXT_TARGET,
]

COPY_TARGETS = {
    SOURCE_FORMULA_AUDIT: [
        QUARANTINE / "GAMMA_KHAT_SOURCE_FORMULA_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_gamma_khat_source_formula_audit_nonclaim_1664.csv",
        QUEUE / "JR1664_GAMMA_KHAT_SOURCE_FORMULA_AUDIT_NONCLAIM.csv",
    ],
    METRIC_RESPONSE_TEST: [
        QUARANTINE / "METRIC_RESPONSE_TEST_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_metric_response_test_nonclaim_1664.csv",
        QUEUE / "JR1664_METRIC_RESPONSE_TEST_NONCLAIM.csv",
    ],
    HELMHOLTZ_OBSTRUCTION: [
        QUARANTINE / "HELMHOLTZ_OBSTRUCTION_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_helmholtz_obstruction_nonclaim_1664.csv",
        QUEUE / "JR1664_HELMHOLTZ_OBSTRUCTION_NONCLAIM.csv",
    ],
    RESCUE_ROUTE_MATRIX: [
        QUARANTINE / "RESCUE_ROUTE_MATRIX_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_rescue_route_matrix_nonclaim_1664.csv",
        QUEUE / "JR1664_RESCUE_ROUTE_MATRIX_NONCLAIM.csv",
    ],
    RETAINED_COEFFICIENTS: [
        QUARANTINE / "RETAINED_COEFFICIENTS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_retained_coefficients_nonclaim_1664.csv",
        QUEUE / "JR1664_RETAINED_COEFFICIENTS_NONCLAIM.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_nonclaim_1664.csv",
        QUEUE / "JR1664_NEXT_TARGET_NONCLAIM.csv",
    ],
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


def all_claim_flags_false(paths: list[Path]) -> bool:
    flag_names = {
        "accepted_for_scoring",
        "claim_allowed",
        "claim_ready",
        "local_gr_claim_allowed",
        "parent_signed",
        "score_allowed",
        "score_ready",
        "theorem_closed_for_claim",
        "valid_for_claim",
        "valid_for_mts_claim",
        "valid_for_runner",
    }
    for path in paths:
        for row in csv_rows(path):
            for flag_name in flag_names.intersection(row):
                if bool_string(row[flag_name]) == "true":
                    return False
    return True


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
                "role": "1664 Gamma/Khat metric-response source-formula or Helmholtz obstruction input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def source_formula_audit_rows() -> list[dict[str, object]]:
    rows = [
        (
            "SFA1664_0_live_Gamma_owner",
            "Gamma_eff",
            "explicit covariant scalar density Gamma_eff(g,Phi,nablaPhi,D,topological data) with units and no fitted readout selector",
            "MA515_0 and RGM1649_1 say the current corpus still has symbols/templates, not a live source formula",
            "FAIL_CURRENT_CORPUS",
            "parent-sign an explicit gamma density or keep Gamma_eff as residual bookkeeping",
        ),
        (
            "SFA1664_1_live_Khat_operator",
            "K_hat^{mu nu}",
            "explicit tensor/operator expression before projection, including metric, derivative, boundary, projector, and domain terms",
            "MA515_1, HLA1618_2, and RGM1649_2 say no live K_hat operator is supplied",
            "FAIL_CURRENT_CORPUS",
            "compute K_gamma from a parent-signed gamma and compare tensor slots",
        ),
        (
            "SFA1664_2_improvement_candidate",
            "K_L trace-free improvement",
            "TF metric response of c_I int sqrt(-g) phi R gives K_L shape under 4D projection",
            "VAR1526_3 derives the algebra exactly, but VAR1526_5 and KAD1527_4 keep coefficient/sign/boundary/phi owner/live adoption unsigned",
            "DERIVED_CONDITIONAL_NOT_LIVE",
            "either promote with parent phi sector and boundary certificate, or keep as nonclaim adoption row",
        ),
        (
            "SFA1664_3_response_doublet_normal_form",
            "Z response doublet",
            "positive normal-form action supplies explicit scalar density and Hilbert-owned K_hat_normal",
            "NF1619_6 and CAL1619_5 show a real formal mechanism, but not parent-signed into current MTS symbols/observables",
            "FORMAL_MECHANISM_NOT_PARENT_SIGNED",
            "map Z to the actual vertical generator and prove source-current, boundary, projector, and normalization clauses",
        ),
        (
            "SFA1664_4_Ward_owner",
            "q_loc Ward identity",
            "diffeomorphism invariance owns the residual only after Gamma/Khat/P_loc/boundary are from the same action",
            "E515_3 and 1663 forbid Ward-ownership-as-zero",
            "NECESSARY_NOT_SUFFICIENT",
            "use Ward only after the source-formula match closes",
        ),
        (
            "SFA1664_5_verdict",
            "live Gamma/Khat source-formula match",
            "all live symbols are matched to one variational scalar density and operator pair",
            "current corpus fails Gamma owner and Khat operator, while formal rescue routes remain nonclaim",
            "FAIL_CURRENT_CORPUS",
            "retain explicit q_loc/frame-leak coefficients and move to parent-signing or demotion",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "target": target,
            "required_formula": required_formula,
            "current_evidence": current_evidence,
            "result": result,
            "repair_or_fallback": repair,
            "parent_signed": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for audit_id, target, required_formula, current_evidence, result, repair in rows
    ]


def metric_response_test_rows() -> list[dict[str, object]]:
    rows = [
        (
            "MRT1664_0_test_definition",
            "K_gamma^{mu nu} := 2/sqrt(-g) delta[sqrt(-g) Gamma_eff]/delta g_{mu nu}",
            "needs explicit Gamma_eff functional and fixed sign/volume convention",
            "TEST_DEFINED_NOT_RUNNABLE_ON_LIVE_SYMBOLS",
            "current Gamma_eff lacks source density",
        ),
        (
            "MRT1664_1_live_MTS",
            "compare live K_hat^{mu nu} to K_gamma^{mu nu}",
            "requires live K_hat operator and Gamma_eff density",
            "FAIL_INPUTS_MISSING",
            "MA515_0/1 and RGM1649_1/2 fail",
        ),
        (
            "MRT1664_2_tracefree_improvement",
            "TF[2(nabla^mu nabla^nu phi-g^{mu nu}Box phi)] = K_L^{mu nu}",
            "runs only on staged improvement route",
            "PASS_CONDITIONAL_ALGEBRA_ONLY",
            "phi owner, coefficient, sign, multiplier stress, and boundary terms remain unsigned",
        ),
        (
            "MRT1664_3_positive_normal_form",
            "define K_hat_normal as Hilbert response of the normal-form S_GK",
            "runs only inside constructed response-doublet normal form",
            "PASS_FORMAL_NORMAL_FORM_ONLY",
            "does not prove old K_hat equals K_hat_normal",
        ),
        (
            "MRT1664_4_verdict",
            "metric-response closure for current MTS",
            "live Gamma/Khat match must pass before q_loc silence",
            "METRIC_RESPONSE_NOT_CLOSED_CURRENT_CORPUS",
            "retain q_loc residual branch",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "test_id": test_id,
            "test": test,
            "runnable_if": runnable_if,
            "result": result,
            "blocker": blocker,
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for test_id, test, runnable_if, result, blocker in rows
    ]


def helmholtz_obstruction_rows() -> list[dict[str, object]]:
    rows = [
        (
            "HOB1664_0_exact_condition",
            "delta[sqrt(-g)T_GK^{mu nu}(x)]/delta g_{alpha beta}(y) equals the adjoint-exchanged second variation up to boundary/gauge terms",
            "condition is known and correctly stated",
            "CONDITION_RECORDED",
            "not an obstruction by itself",
        ),
        (
            "HOB1664_1_functional_gap",
            "S_GK or Gamma_eff(g,Phi,nablaPhi,D,...)",
            "HLA1618_1 and SFA1664_0: no live explicit functional",
            "OBSTRUCTION_INPUT_MISSING",
            "Helmholtz cannot be run on current symbols",
        ),
        (
            "HOB1664_2_operator_gap",
            "K_hat tensor/operator expression",
            "HLA1618_2 and SFA1664_1: K_hat appears as identity slot, not computed response",
            "OBSTRUCTION_INPUT_MISSING",
            "no second-variation comparison target",
        ),
        (
            "HOB1664_3_boundary_domain_gap",
            "self-adjoint local compact domain and boundary/improvement bookkeeping",
            "HLA1618_3/4 and RGM1649_5 keep boundary/source/domain terms open",
            "OBSTRUCTION_BOUNDARY_DOMAIN_OPEN",
            "formal bulk action could still leak through boundaries",
        ),
        (
            "HOB1664_4_normal_form_exception",
            "constructed positive response-doublet normal form",
            "CAL1619_3 passes Helmholtz for constructed normal form because it is action-defined",
            "FORMAL_EXCEPTION_NOT_LIVE_MTS",
            "exception does not promote current Gamma/Khat",
        ),
        (
            "HOB1664_5_verdict",
            "Helmholtz status for current MTS Gamma/Khat",
            "live inputs absent; formal route separate",
            "HELMHOLTZ_OBSTRUCTION_CURRENT_CORPUS",
            "not a no-go theorem, but strict no-claim",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "obstruction_id": obstruction_id,
            "required_clause": clause,
            "evidence": evidence,
            "result": result,
            "effect": effect,
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for obstruction_id, clause, evidence, result, effect in rows
    ]


def rescue_route_rows() -> list[dict[str, object]]:
    rows = [
        (
            "RRM1664_0_live_direct_match",
            "source explicit Gamma_eff and compute K_gamma; prove K_hat == K_gamma",
            "cleanest if source exists",
            "CURRENTLY_FAILS",
            "Gamma owner and Khat operator missing",
            "highest scrutiny but best if possible",
        ),
        (
            "RRM1664_1_tracefree_improvement",
            "adopt K_hat as trace-free metric response of int sqrt(-g)phi R",
            "already gives exact K_L algebra",
            "CONDITIONAL_RESCUE",
            "phi owner, coefficient, sign, boundary, multiplier stress, and live adoption missing",
            "less speculative if phi is already a parent auxiliary field",
        ),
        (
            "RRM1664_2_positive_response_doublet",
            "parent-sign the 1619 normal-form Z sector",
            "closes action/metric-response/Helmholtz/double-zero formally",
            "BEST_DERIVATION_ROUTE_IF_Z_MAPS_TO_ACTUAL_VERTICAL_GENERATOR",
            "Z-to-MTS variable map, source-current zero, boundary no-flux, projector descent, and normalization missing",
            "least hand-wavy route if coupling/vertical generator can be identified",
        ),
        (
            "RRM1664_3_topological_exact_sector",
            "make Gamma/Khat an exact/improvement stress with zero local boundary flux",
            "could silence bulk without propagating fields",
            "OPEN_HIGH_BOUNDARY_RISK",
            "boundary no-flux and linking-source subtraction not proved",
            "use only if boundary certificate becomes sharp",
        ),
        (
            "RRM1664_4_residual_demote",
            "stop trying to set q_loc=0; retain q_loc/frame coefficients and source bounds",
            "honest fallback",
            "AVAILABLE_NONCLAIM_FALLBACK",
            "does not deliver local GR derivation",
            "keeps theory testable if parent-signing fails",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": route_id,
            "route": route,
            "benefit": benefit,
            "status": status,
            "missing_to_promote": missing,
            "scrutiny_note": scrutiny_note,
            "parent_signed": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for route_id, route, benefit, status, missing, scrutiny_note in rows
    ]


def retained_coefficient_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "coefficient_id": "RC1664_0_epsilon_frame_leak_retained",
            "coefficient": "epsilon_frame_leak",
            "value_m1": f"{EPSILON_FRAME_LEAK_M1:.8e}",
            "conditional_curvature_bound_m1": f"{CONDITIONAL_CURVATURE_BOUND_M1:.8e}",
            "ratio_to_curvature_bound": f"{FRAME_RATIO:.8e}",
            "source": "1662/1663 retained max(a_earth/c^2, Omega_earth/c)",
            "reason_retained": "Gamma/Khat metric-response and apparatus transfer remain unsigned",
            "status": "RETAINED_NONCLAIM_COEFFICIENT",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "coefficient_id": "RC1664_1_q_loc_unmatched",
            "coefficient": "q_loc_unmatched",
            "value_m1": "MISSING_GAMMA_OWNER + MISSING_KHAT_RESPONSE + MISSING_HELMHOLTZ + MISSING_PLOC_TRANSFER",
            "conditional_curvature_bound_m1": "not_applicable",
            "ratio_to_curvature_bound": "not_applicable",
            "source": "SFA1664/HOB1664 obstruction rows",
            "reason_retained": "current q_loc cannot be reduced to a parent-signed variational zero",
            "status": "SYMBOLIC_RESIDUAL_RETAINED_NONCLAIM",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_rows() -> list[dict[str, object]]:
    rows = [
        ("CG1664_0_live_Gamma_density", "Gamma_eff live scalar density source formula exists", False, "BLOCKED", "SFA1664_0 fails current corpus"),
        ("CG1664_1_live_Khat_response", "K_hat equals metric response of live Gamma_eff", False, "BLOCKED", "SFA1664_1 and MRT1664_1 fail inputs"),
        ("CG1664_2_Helmholtz_current_symbols", "Helmholtz symmetry passes for current MTS Gamma/Khat", False, "BLOCKED", "HOB1664_5 obstruction"),
        ("CG1664_3_formal_normal_form_claim", "1619 normal form is accepted as actual MTS local sector", False, "BLOCKED", "formal mechanism not parent-signed"),
        ("CG1664_4_q_loc_zero", "q_loc^nu -> 0 locally", False, "NO_CLAIM", "metric-response route not closed"),
        ("CG1664_5_local_GR_Newton_PPN_R10_WEP", "local GR/Newton/PPN/R10/WEP pass follows", False, "NO_CLAIM", "retained q_loc/frame coefficients remain live"),
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


def decision_rows() -> list[dict[str, object]]:
    rows = [
        (
            "DEC1664_0_current_match",
            "FAIL_CURRENT_CORPUS",
            "live Gamma_eff and K_hat still do not have source formulas sufficient for metric-response/Helmholtz",
            "do not promote q_loc=0",
        ),
        (
            "DEC1664_1_real_progress",
            "FORMAL_MECHANISM_EXISTS",
            "trace-free improvement and positive response-doublet normal form are mathematically real candidate mechanisms",
            "separate formal mechanism from live MTS claim",
        ),
        (
            "DEC1664_2_retained_coefficients",
            "RETAIN_QLOC_AND_FRAME_LEAK",
            "epsilon_frame_leak and q_loc_unmatched are the honest fallback until parent signatures close",
            "carry them into any local bound/source runner",
        ),
        (
            "DEC1664_3_next",
            "NEXT_1665_PARENT_SIGN_OR_DEMOTE",
            "the least-foggy next step is to either map the normal-form Z/coupling to the actual vertical generator, or formally demote Gamma/Khat local route to closure-only",
            "build 1665 response-normal-form parent-signature/adoption gate",
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


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1665-Y5-R2FR-response-normal-form-parent-signature-or-live-GammaKhat-adoption.md",
            "script": "scripts/Y5_R2FR_response_normal_form_parent_signature_or_live_GammaKhat_adoption.py",
            "objective": "either parent-sign the response-doublet/trace-free-improvement mechanism as the actual MTS Gamma_eff/K_hat sector, including vertical generator, coupling, boundary, source-current, projector, and normalization clauses, or demote the local transition route to explicit closure-only residuals",
            "success_condition": "Z or phi route is signed into live MTS symbols with metric-response and Helmholtz readiness, or local q_loc=0 route is explicitly demoted",
            "forbidden_shortcuts": "no plateau axiom; no bookkeeping stress; no formal-normal-form-as-live-MTS claim; no local-GR/Newton/PPN/R10/WEP claim",
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


def validation_rows(
    source_rows: list[dict[str, object]],
    source_formula: list[dict[str, object]],
    metric_response: list[dict[str, object]],
    helmholtz: list[dict[str, object]],
    rescue: list[dict[str, object]],
    retained: list[dict[str, object]],
    claim: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
) -> list[dict[str, object]]:
    generated_csv_parse = True
    try:
        for generated_path in GENERATED:
            csv_rows(generated_path)
    except Exception:
        generated_csv_parse = False

    formalization_dirty = any(FORMALIZATION.rglob("*1664*")) if FORMALIZATION.exists() else False
    live_match_failed = any(row["audit_id"] == "SFA1664_5_verdict" and row["result"] == "FAIL_CURRENT_CORPUS" for row in source_formula)
    metric_response_blocked = any(row["test_id"] == "MRT1664_4_verdict" and row["result"] == "METRIC_RESPONSE_NOT_CLOSED_CURRENT_CORPUS" for row in metric_response)
    helmholtz_blocked = any(row["obstruction_id"] == "HOB1664_5_verdict" and row["result"] == "HELMHOLTZ_OBSTRUCTION_CURRENT_CORPUS" for row in helmholtz)
    formal_route_retained = any(row["route_id"] == "RRM1664_2_positive_response_doublet" and row["status"] == "BEST_DERIVATION_ROUTE_IF_Z_MAPS_TO_ACTUAL_VERTICAL_GENERATOR" for row in rescue)
    retained_nonclaim = all(row["claim_allowed"] is False and row["valid_for_claim"] is False for row in retained)
    next_target_selected = next_targets[0]["next_target"] == "1665-Y5-R2FR-response-normal-form-parent-signature-or-live-GammaKhat-adoption.md"

    checks = [
        ("VAL1664_0_sources_exist", all(row["path_exists"] and row["needles_found"] for row in source_rows), "all cited 1664 source paths exist and needles are present"),
        ("VAL1664_1_live_source_match_failed", live_match_failed, "live Gamma/Khat source-formula match remains failed for current corpus"),
        ("VAL1664_2_metric_response_blocked", metric_response_blocked, "current-symbol metric-response test remains blocked"),
        ("VAL1664_3_helmholtz_obstruction_recorded", helmholtz_blocked, "Helmholtz obstruction is recorded without treating it as a no-go theorem"),
        ("VAL1664_4_formal_route_retained_nonclaim", formal_route_retained, "positive response-doublet route is retained as a formal mechanism only"),
        ("VAL1664_5_retained_coefficients_nonclaim", retained_nonclaim, "q_loc/frame leak retained coefficients remain nonclaim"),
        ("VAL1664_6_claim_gates_safe", all(row["claim_allowed"] is False and row["valid_for_claim"] is False for row in claim), "all claim gates keep MTS local claims false"),
        ("VAL1664_7_decision_has_fail_current", any(row["decision"] == "FAIL_CURRENT_CORPUS" for row in decisions), "decision row records current corpus failure"),
        ("VAL1664_8_next_target_selected", next_target_selected, "next target selects response-normal-form parent signature or live Gamma/Khat adoption"),
        ("VAL1664_9_csv_parse", generated_csv_parse, "all generated 1664 CSVs parse"),
        ("VAL1664_10_no_mts_claim_flags", all_claim_flags_false(CLAIM_CHECKED), "all 1664 generated rows keep MTS claim/no-score flags false"),
        ("VAL1664_11_branch_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" not in str(target)), "branch/quarantine copies exist"),
        ("VAL1664_12_queue_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" in str(target)), "acquisition queue nonclaim copies exist"),
        ("VAL1664_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1664_14_formalization_untouched", not formalization_dirty, "no 1664 outputs found under formalization-workbench"),
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
            "check_id": "VAL1664_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1664 Gamma/Khat metric-response source-formula or Helmholtz obstruction validation",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row[column]) for column in columns) + " |")
    return "\n".join(lines)


def write_doc(
    source_rows: list[dict[str, object]],
    source_formula: list[dict[str, object]],
    metric_response: list[dict[str, object]],
    helmholtz: list[dict[str, object]],
    rescue: list[dict[str, object]],
    retained: list[dict[str, object]],
    claim: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 1664 - Gamma/Khat Metric-Response Source Formula Or Helmholtz Obstruction

**Private status:** metric-response obstruction checkpoint. No `q_loc=0`, local-GR pass, Newton pass, PPN pass, R10 pass, WEP pass, or public claim is made.

## Verdict

The live route still fails for the current corpus:

```text
FAIL_CURRENT_CORPUS:
Gamma_eff does not yet have a source-signed scalar-density formula.
K_hat does not yet have a live tensor/operator formula equal to the metric response of Gamma_eff.
The Helmholtz test is exact, but not runnable on the current live symbols.
```

This is not the same as "dead". Two real mechanisms remain on the board:

```text
1. Trace-free improvement:
   TF[delta int sqrt(-g) phi R] gives the K_L shape exactly, but phi owner/coefficient/sign/boundary/live adoption are unsigned.

2. Positive response-doublet normal form:
   a calculable Z-sector gives action, metric response, Helmholtz readiness, and double-zero formally, but Z is not yet parent-signed as the actual MTS vertical generator/coupling.
```

So the honest status is:

```text
FORMAL_MECHANISM_EXISTS_NOT_PARENT_SIGNED
q_loc=0 is not claimed.
epsilon_frame_leak = {EPSILON_FRAME_LEAK_M1:.8e} m^-1 remains retained.
```

## Source Register

{markdown_table(source_rows, ["source_id", "path", "path_exists", "needles_found", "role"])}

## Gamma/Khat Source Formula Audit

{markdown_table(source_formula, ["audit_id", "target", "required_formula", "current_evidence", "result", "repair_or_fallback"])}

## Metric Response Test

{markdown_table(metric_response, ["test_id", "test", "runnable_if", "result", "blocker"])}

## Helmholtz Obstruction

{markdown_table(helmholtz, ["obstruction_id", "required_clause", "evidence", "result", "effect"])}

## Rescue Route Matrix

{markdown_table(rescue, ["route_id", "route", "benefit", "status", "missing_to_promote", "scrutiny_note"])}

## Retained Coefficients

{markdown_table(retained, ["coefficient_id", "coefficient", "value_m1", "status", "reason_retained"])}

## Claim Gates

{markdown_table(claim, ["gate_id", "claim", "gate_pass", "status", "blocker"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Next Target

{markdown_table(next_targets, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Working Interpretation

This checkpoint is useful because it stops us pretending the metric-response bridge is already proved. The project has a mathematically respectable construction route, but not yet a parent-signed MTS route. The best attack is therefore the coupling/vertical-generator hunt: either `Z` or `phi` becomes the actual parent-owned variable that produces `Gamma_eff` and `K_hat`, or this local transition path gets demoted to closure-only residual bookkeeping.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    source_rows = source_register_rows()
    source_formula = source_formula_audit_rows()
    metric_response = metric_response_test_rows()
    helmholtz = helmholtz_obstruction_rows()
    rescue = rescue_route_rows()
    retained = retained_coefficient_rows()
    claim = claim_rows()
    decisions = decision_rows()
    next_targets = next_rows()

    for path, rows in [
        (SOURCE_REGISTER, source_rows),
        (SOURCE_FORMULA_AUDIT, source_formula),
        (METRIC_RESPONSE_TEST, metric_response),
        (HELMHOLTZ_OBSTRUCTION, helmholtz),
        (RESCUE_ROUTE_MATRIX, rescue),
        (RETAINED_COEFFICIENTS, retained),
        (CLAIM_GATE, claim),
        (DECISION, decisions),
        (NEXT_TARGET, next_targets),
    ]:
        write_csv(path, rows)

    copy_outputs()
    validation = validation_rows(source_rows, source_formula, metric_response, helmholtz, rescue, retained, claim, decisions, next_targets)
    write_csv(VALIDATION, validation)
    write_doc(source_rows, source_formula, metric_response, helmholtz, rescue, retained, claim, decisions, next_targets, validation)

    if any(row["result"] == "FAIL" for row in validation):
        raise SystemExit("1664 validation failed; see P8_Y5_BRR545_1664_VALIDATION.csv")

    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    print("1664 validation PASS")


if __name__ == "__main__":
    main()

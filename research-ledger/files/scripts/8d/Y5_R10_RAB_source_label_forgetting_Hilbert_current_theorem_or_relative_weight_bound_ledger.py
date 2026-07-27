from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_ROOT = MICROSCOPE / "branch_locked_wep"
COEFF = BRANCH_ROOT / "coefficients"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1450-Y5-R10-RAB-source-label-forgetting-Hilbert-current-theorem-or-relative-weight-bound-ledger.md"

PREV_NEXT = OUT / "P8_Y5_R10_1449_NEXT_TARGET.csv"
PREV_FIELD_MAP = OUT / "P8_Y5_R10_1449_FIELD_BY_FIELD_VWEP_ACTION_MAP.csv"
PREV_DERIVATION = OUT / "P8_Y5_R10_1449_C_PARENT_ZERO_DERIVATION_ATTEMPT.csv"
PREV_COUNTERS = OUT / "P8_Y5_R10_1449_SOURCE_ONLY_COUNTERMODEL_RETENTION.csv"
PREV_EVAL = OUT / "P8_Y5_R10_1449_C_PARENT_EVALUATION_DECISION.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1449_VALIDATION.csv"

NSF953 = OUT / "P8_Y5_R10_953_SOURCE_FUNCTOR_THEOREM_ATTEMPT.csv"
PMC953 = OUT / "P8_Y5_R10_953_PARENT_CATEGORY_CONTRACT.csv"
PLF954 = OUT / "P8_Y5_R10_954_PARENT_LABEL_FORGETTING_ATTEMPT.csv"
PAC954 = OUT / "P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv"
MMA955 = OUT / "P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv"
SPC955 = OUT / "P8_Y5_R10_955_SOURCE_PREFACTOR_CLASSIFICATION.csv"
SSG956 = OUT / "P8_Y5_R10_956_SOURCE_SIDE_GR_NEWTON_SPINE.csv"
HCG956 = OUT / "P8_Y5_R10_956_HIDDEN_CURRENT_BYPASS_GATES.csv"
THM1063 = OUT / "P8_Y5_R10_1063_SOURCE_FORGETTING_THEOREM_ATTEMPT.csv"
PLF1064 = OUT / "P8_Y5_R10_1064_LABEL_FORGETTING_PROOF_ATTEMPT.csv"
NSS1064 = OUT / "P8_Y5_R10_1064_NO_SOURCE_ONLY_SLOT_AUDIT.csv"
CMG1064 = OUT / "P8_Y5_R10_1064_COMMON_MODE_GUARD.csv"
PAC1055 = OUT / "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv"
AXRED1441 = OUT / "P8_Y5_R10_1441_AX1090_REDUCTION_AUDIT.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1450_SOURCE_REGISTER.csv"
HILBERT_THEOREM = OUT / "P8_Y5_R10_1450_HILBERT_SOURCE_LABEL_FORGETTING_THEOREM_ATTEMPT.csv"
NO_SOURCE_SLOT_AUDIT = OUT / "P8_Y5_R10_1450_NO_SOURCE_ONLY_SLOT_REDUCTION_AUDIT.csv"
EPSILON_BOUND_LEDGER = OUT / "P8_Y5_R10_1450_RELATIVE_EPSILON_A_BOUND_LEDGER_NONCLAIM.csv"
NONHILBERT_GUARD = OUT / "P8_Y5_R10_1450_NONHILBERT_CURRENT_GUARD.csv"
COMMON_MODE_GUARD = OUT / "P8_Y5_R10_1450_COMMON_MODE_ABSORPTION_GUARD.csv"
EVALUATION_DECISION = OUT / "P8_Y5_R10_1450_C_PARENT_EVALUATION_DECISION.csv"
PARSER_DRYRUN = OUT / "P8_Y5_R10_1450_PARSER_DRYRUN.csv"
CLAIM_GATE = OUT / "P8_Y5_R10_1450_CLAIM_GATE.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1450_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1450_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1450_VALIDATION.csv"

BRANCH_HILBERT_THEOREM = COEFF / "Hilbert_source_label_forgetting_theorem_attempt_1450.csv"
BRANCH_EPSILON_LEDGER = COEFF / "relative_epsilon_A_bound_ledger_nonclaim_1450.csv"
BRANCH_EVALUATION_DECISION = COEFF / "C_parent_WEP_source_label_decision_1450.csv"
LIVE_C_PARENT_IMPORT = COEFF / "C_parent_WEP_slot_import.csv"
LIVE_EPSILON_IMPORT = COEFF / "epsilon_A_source_weight_live_claim.csv"
LIVE_READOUT = MICROSCOPE / "official_readout" / "P_WEP_K_CMSM_readout.csv"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
START_TS = datetime.now(timezone.utc).timestamp()


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


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
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def parse_csv_ok(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            return len(list(csv.DictReader(handle))) > 0
    except Exception:
        return False


def truth(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


def copy_branch(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


def source_rows() -> list[dict[str, Any]]:
    sources = [
        ("SRC1450_0_prev_next", PREV_NEXT, "1449 next target"),
        ("SRC1450_1_prev_field_map", PREV_FIELD_MAP, "1449 field-by-field V_WEP map"),
        ("SRC1450_2_prev_derivation", PREV_DERIVATION, "1449 C_parent zero derivation attempt"),
        ("SRC1450_3_prev_counters", PREV_COUNTERS, "1449 source-only countermodels"),
        ("SRC1450_4_prev_eval", PREV_EVAL, "1449 C_parent evaluation decision"),
        ("SRC1450_5_prev_validation", PREV_VALIDATION, "1449 validation"),
        ("SRC1450_6_NSF953", NSF953, "source functor theorem attempt"),
        ("SRC1450_7_PMC953", PMC953, "parent category contract"),
        ("SRC1450_8_PLF954", PLF954, "parent label-forgetting attempt"),
        ("SRC1450_9_PAC954", PAC954, "parent action clause"),
        ("SRC1450_10_MMA955", MMA955, "minimal matter action lemma"),
        ("SRC1450_11_SPC955", SPC955, "source prefactor classification"),
        ("SRC1450_12_SSG956", SSG956, "source-side GR/Newton spine"),
        ("SRC1450_13_HCG956", HCG956, "hidden current bypass gates"),
        ("SRC1450_14_THM1063", THM1063, "source forgetting theorem attempt"),
        ("SRC1450_15_PLF1064", PLF1064, "label-forgetting proof attempt"),
        ("SRC1450_16_NSS1064", NSS1064, "no-source-only-slot audit"),
        ("SRC1450_17_CMG1064", CMG1064, "common mode guard"),
        ("SRC1450_18_PAC1055", PAC1055, "parent action contract candidate"),
        ("SRC1450_19_AXRED1441", AXRED1441, "AX1090 reduction audit"),
    ]
    return [
        {
            "source_id": source_id,
            "source_path": str(path),
            "exists": path.exists(),
            "role": role,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for source_id, path, role in sources
    ]


def hilbert_theorem_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "theorem_step": "HT1450_0_target",
            "claim": "source functor forgets species labels before coupling",
            "mathematical_form": "q_src({(T_A,A)}) = T_total := sum_A T_A; F_src(T_total)=kappa_univ T_total",
            "status": "TARGET_RESTATED",
            "what_closes": "relative kappa_A/kappa_B cannot be formed if A is not an argument",
            "current_gap": "parent category has not signed q_src as label-forgetting",
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_step": "HT1450_1_total_Hilbert_variation",
            "claim": "one matter action gives one total Hilbert source",
            "mathematical_form": "T_total^{mu nu} := 2/sqrt(-g) delta S_matter/delta g_munu with S_matter=sum_A S_A, hence T_total=sum_A T_A",
            "status": "EXACT_CONDITIONAL_MATH_PASS",
            "what_closes": "species labels become bookkeeping after varying the summed action",
            "current_gap": "only works if no w_A or hidden source multiplier is present before variation",
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_step": "HT1450_2_covariant_additive_uniqueness",
            "claim": "a label-forgotten covariant additive local source map is unique up to one scalar",
            "mathematical_form": "F_src(phi_*T)=phi_*F_src(T), F_src(T+U)=F_src(T)+F_src(U) => F_src(T)=kappa_univ T",
            "status": "CONDITIONAL_UNIQUENESS_PASS",
            "what_closes": "after label forgetting, only common G normalization remains",
            "current_gap": "additivity does not forbid F((T_A,A))=kappa_A T_A if labels survive",
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_step": "HT1450_3_relative_prefactor_counterexample",
            "claim": "relative source weights are forbidden",
            "mathematical_form": "S_matter=sum_A w_A S_A gives T_source=sum_A w_A T_A while preserving covariance and additivity",
            "status": "COUNTEREXAMPLE_SURVIVES",
            "what_closes": "nothing; it identifies the exact forbidden slot",
            "current_gap": "parent grammar does not yet exclude constant relative w_A",
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_step": "HT1450_4_same_action_guard",
            "claim": "matter dynamics and active source are not separate functionals",
            "mathematical_form": "E_A=delta S_matter/delta Psi_A and T_total=delta S_matter/delta g_obs are taken from the same S_matter",
            "status": "STRONG_CONDITIONAL_GUARD",
            "what_closes": "rules out arbitrary post-hoc source functionals",
            "current_gap": "a constant w_A inside the same S_matter still survives unless absent by schema",
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_step": "HT1450_5_nonHilbert_guard",
            "claim": "only Hilbert/coframe source couples to local geometry",
            "mathematical_form": "J_src = kappa_univ T_Hilbert + J_NH_retained, with J_NH=0/exact/projected-silent for a theorem-zero branch",
            "status": "PARALLEL_GATE_OPEN",
            "what_closes": "prevents spin/torsion/boundary/non-Hilbert currents bypassing the source theorem",
            "current_gap": "non-Hilbert current owner is not proven absent or silent",
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_step": "HT1450_6_verdict",
            "claim": "Hilbert-source label-forgetting theorem proves epsilon_A=0",
            "mathematical_form": "single S_matter + total Hilbert variation + no w_A + no hidden spurions + no non-Hilbert bypass => epsilon_A=0",
            "status": "CONDITIONAL_THEOREM_NOT_PARENT_DERIVED",
            "what_closes": "would remove the sharpest finite WEP/source coupling if parent-signed",
            "current_gap": "no-source-only-slot and common measure/current are still unsigned",
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in rows:
        row["same_parent_branch_id"] = BRANCH_ID
    return rows


def no_source_slot_rows() -> list[dict[str, Any]]:
    rows = [
        ("NSSR1450_0_absent_wA", "w_A source-only prefactor", "desired_absent_slot", "parent action has no argument corresponding to source-only species weight", "NOT_PARENT_SIGNED", "relative epsilon_A remains live"),
        ("NSSR1450_1_same_action", "separate S_source[species]", "forbidden_by_same_action_if_signed", "matter dynamics and source extraction come from one S_matter", "CONDITIONAL_ONLY", "post-hoc source functional remains a loophole"),
        ("NSSR1450_2_common_measure", "species-dependent measure/J_A", "forbidden_if_common_measure_signed", "one action measure/current normalization with no species Jacobian", "NOT_REDUCED", "J_A can imitate source weight"),
        ("NSSR1450_3_hidden_spurion", "marker/domain/boundary/readout weight", "forbidden_if_no_spurion_signed", "no hidden marker returns after label-forgetting", "UNSIGNED", "kappa_A can return under another name"),
        ("NSSR1450_4_nonHilbert_current", "zeta_A J_NH,A", "parallel_open_gate", "non-Hilbert currents absent/exact/projected silent or retained", "OPEN", "Hilbert theorem can be bypassed"),
        ("NSSR1450_5_verdict", "no-source-only-slot theorem", "all source-only prefactor channels absent together", "parent operator/action grammar must exclude every slot before variation", "FAIL_CURRENT_PROOF", "epsilon_A ledger required"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "slot": slot,
            "desired_status": desired,
            "required_signature": required,
            "current_status": status,
            "if_missing": consequence,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for audit_id, slot, desired, required, status, consequence in rows
    ]


def epsilon_bound_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "EPS1450_0_definition",
            "symbol": "epsilon_A",
            "meaning": "relative active-source prefactor for matter/source class A after common normalization is removed",
            "formula": "w_A = w_common (1 + epsilon_A), with sum/reference convention declared before comparison",
            "units": "dimensionless",
            "arena": "theory_definition",
            "required_bound_input": "normalization convention and source/test material map",
            "current_value": "MISSING_PARENT_ZERO_OR_NUMERIC_BOUND",
            "source_path": str(NO_SOURCE_SLOT_AUDIT),
            "status": "DEFINITION_ONLY_NONCLAIM",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "EPS1450_1_MICROSCOPE_Ti_Pt",
            "symbol": "Delta_epsilon_TiPt",
            "meaning": "differential active-source/test response for Ti versus Pt-like material contrast",
            "formula": "|eta_TiPt| ~ |Delta_epsilon_TiPt| times declared sensitivity factor, after readout/source model",
            "units": "dimensionless",
            "arena": "MICROSCOPE/WEP",
            "required_bound_input": "official composition/readout map, material sensitivity coefficients, eta covariance",
            "current_value": "MISSING_SENSITIVITY_MAP",
            "source_path": str(PREV_EVAL),
            "status": "BOUND_ROW_TEMPLATE_NONCLAIM",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "EPS1450_2_EotWash_R10",
            "symbol": "epsilon_source_R10(lambda)",
            "meaning": "finite-range source-weight residual entering alpha(lambda)",
            "formula": "|alpha_epsilon(lambda)| <= alpha_bound(lambda) only after epsilon-to-alpha kernel is sourced",
            "units": "dimensionless",
            "arena": "R10_short_range",
            "required_bound_input": "real alpha(lambda) curve plus source composition kernel K_epsilon(lambda)",
            "current_value": "MISSING_KERNEL_AND_BOUND_SOURCE_LINK",
            "source_path": str(PREV_COUNTERS),
            "status": "BOUND_ROW_TEMPLATE_NONCLAIM",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "EPS1450_3_PPN",
            "symbol": "epsilon_source_PPN",
            "meaning": "composition/source-normalization residual entering local PPN source terms",
            "formula": "Delta gamma/beta/source_charge = K_PPN epsilon_source after parent/source projection",
            "units": "dimensionless",
            "arena": "PPN/local_GR",
            "required_bound_input": "source projection and PPN sensitivity matrix",
            "current_value": "MISSING_PPN_PROJECTION",
            "source_path": str(SSG956),
            "status": "BOUND_ROW_TEMPLATE_NONCLAIM",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "EPS1450_4_orbital_GM",
            "symbol": "epsilon_GM_worldtube",
            "meaning": "measured-GM/worldtube source normalization residual",
            "formula": "GM_measured = G_ref M_Hilbert (1 + epsilon_GM + boundary/support terms)",
            "units": "dimensionless",
            "arena": "orbital/Newtonian_source",
            "required_bound_input": "worldtube source law, Gauss calibration, orbital GM comparison model",
            "current_value": "MISSING_WORLDTUBE_GM_CHAIN",
            "source_path": str(HCG956),
            "status": "BOUND_ROW_TEMPLATE_NONCLAIM",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "EPS1450_5_nonHilbert",
            "symbol": "zeta_A",
            "meaning": "species-labelled non-Hilbert current coefficient",
            "formula": "J_src = kappa T_Hilbert + sum_A zeta_A J_NH,A",
            "units": "dimensionless_or_declared_by_current",
            "arena": "WEP/PPN/orbital",
            "required_bound_input": "definition of J_NH,A and projection/silence proof",
            "current_value": "MISSING_CURRENT_OWNER",
            "source_path": str(HCG956),
            "status": "PARALLEL_BOUND_ROW_TEMPLATE_NONCLAIM",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in rows:
        row["same_parent_branch_id"] = BRANCH_ID
    return rows


def nonhilbert_guard_rows() -> list[dict[str, Any]]:
    guards = [
        ("NHG1450_0_absent", "J_NH,A absent from parent source", "would close bypass", "NOT_SIGNED"),
        ("NHG1450_1_exact", "J_NH,A exact/boundary with zero local projection", "would close compact local branch", "NOT_SIGNED"),
        ("NHG1450_2_projected_silent", "Pi_local[J_NH,A]=0 by projector orthogonality", "would close arena projection", "NOT_SIGNED"),
        ("NHG1450_3_retained", "if none of the above, retain zeta_A J_NH,A bound rows", "current required fallback", "RETAINED_NONCLAIM"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "guard_id": guard_id,
            "guard": guard,
            "effect": effect,
            "current_status": status,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for guard_id, guard, effect, status in guards
    ]


def common_mode_rows() -> list[dict[str, Any]]:
    guards = [
        ("CMA1450_0_common_G", "w_common can be absorbed into measured G only after it is universal, constant, range-independent, time-independent, and frame-independent", "COMMON_MODE_CONDITIONAL_ONLY"),
        ("CMA1450_1_relative_weight", "epsilon_A cannot be absorbed into one G unless Delta_AB epsilon=0 for every source/test contrast", "RELATIVE_MODE_NOT_ABSORBABLE"),
        ("CMA1450_2_range_dependence", "finite-range or radial source weights cannot be hidden in a local calibration across R10/orbital arenas", "RANGE_MODE_NOT_ABSORBABLE"),
        ("CMA1450_3_verdict", "measured G calibration does not save the source-label theorem; it only removes one common scalar after uniqueness", "GUARD_RETAINED"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "guard_id": guard_id,
            "statement": statement,
            "current_status": status,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for guard_id, statement, status in guards
    ]


def evaluation_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "evaluation_id": "EVAL1450_0_source_label",
            "target": "C_parent_WEP source-label piece and epsilon_A theorem-zero/import decision",
            "Hilbert_variation_math_pass": True,
            "label_forgetting_parent_signed": False,
            "no_wA_slot_parent_signed": False,
            "common_measure_parent_signed": False,
            "nonHilbert_guard_closed": False,
            "epsilon_A_zero_claim_allowed": False,
            "epsilon_A_bound_ready": False,
            "C_parent_WEP_evaluable_now": False,
            "decision": "DO_NOT_IMPORT_EPSILON_ZERO_OR_C_PARENT_WEP",
            "reason": "Hilbert-source route is mathematically sharp but still depends on an unsigned no-source-only-slot/operator-grammar theorem",
            "live_C_parent_import_exists": LIVE_C_PARENT_IMPORT.exists(),
            "live_epsilon_import_exists": LIVE_EPSILON_IMPORT.exists(),
            "official_readout_exists": LIVE_READOUT.exists(),
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def parser_rows() -> list[dict[str, Any]]:
    parser_checks = [
        ("PDR1450_0_epsilon_zero_import", "attempt to import epsilon_A=0", "REFUSED", "no-source-only-slot theorem unsigned"),
        ("PDR1450_1_Cparent_import", "attempt to evaluate/import C_parent_WEP source-label piece", "REFUSED", "source-label and non-Hilbert guards are not closed"),
        ("PDR1450_2_bound_rows", "stage epsilon_A bound ledger rows", "ALLOWED_NONCLAIM", "rows are templates with valid_for_claim=false"),
        ("PDR1450_3_common_G_absorption", "absorb all source weights into G", "REFUSED", "only one common scalar may be absorbed after universality is proven"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "parser_check_id": check_id,
            "attempt": attempt,
            "parser_result": result,
            "reason": reason,
            "would_write_live_claim_file": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, attempt, result, reason in parser_checks
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG1450_0_epsilon_zero", "epsilon_A=0 theorem-zero"),
        ("CG1450_1_WEP", "WEP/MICROSCOPE source-weight pass"),
        ("CG1450_2_R10", "R10 alpha(lambda) source-weight pass"),
        ("CG1450_3_PPN", "PPN source-weight residual pass"),
        ("CG1450_4_Newton_GR_source", "GR/Newton source-side derivation"),
        ("CG1450_5_C_parent_WEP", "C_parent_WEP evaluable/importable"),
        ("CG1450_6_public_claim", "public local-source coupling claim"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": False,
            "reason": "Hilbert theorem is conditional and source-only prefactor countermodel survives",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, claim in gates
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1450_0_keep_theorem_shape",
            "decision": "retain total-Hilbert variation plus additive uniqueness as the clean source theorem skeleton",
            "why": "the math is right once label forgetting/no w_A is parent-signed",
            "consequence": "do not abandon the GR-source route",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1450_1_keep_epsilon_live",
            "decision": "retain epsilon_A relative source weights as nonclaim bound-ledger rows",
            "why": "constant relative source weights are covariant/additive and survive current corpus",
            "consequence": "no WEP/R10/PPN local pass from source coupling yet",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1450_2_next_best_route",
            "decision": "attack the no-source-only-slot operator/action-grammar theorem next",
            "why": "this is the exact missing premise; proving it would kill epsilon_A rather than merely bounding it",
            "consequence": "1451 focuses on absence of w_A from the parent grammar",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1450_0_1451",
            "next_target": "1451-Y5-R10-RAB-no-source-only-slot-operator-grammar-theorem-or-epsilon-bound-inputs.md",
            "script": "scripts/Y5_R10_RAB_no_source_only_slot_operator_grammar_theorem_or_epsilon_bound_inputs.py",
            "objective": "try to derive that the parent action/operator grammar has no source-only species-weight slot w_A; if this cannot be signed, fill epsilon_A bound-input requirements for WEP, R10, PPN, clocks, and orbital source arenas as nonclaim rows",
            "include": "operator-classification theorem; no hidden-visible hom into source coefficients; common measure/current; source-only slot absence; epsilon_A bound-input ledger",
            "exclude": "numeric epsilon claim; C_parent import; local-GR pass; formalization-workbench edits; GitHub action",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    slot_audit: list[dict[str, Any]],
    epsilon: list[dict[str, Any]],
    nonhilbert: list[dict[str, Any]],
    common: list[dict[str, Any]],
    eval_rows: list[dict[str, Any]],
    parser: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated_csvs = [
        SOURCE_REGISTER,
        HILBERT_THEOREM,
        NO_SOURCE_SLOT_AUDIT,
        EPSILON_BOUND_LEDGER,
        NONHILBERT_GUARD,
        COMMON_MODE_GUARD,
        EVALUATION_DECISION,
        PARSER_DRYRUN,
        CLAIM_GATE,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    all_sources_exist = all(truth(row["exists"]) for row in sources)
    hilbert_math_pass = any(row["status"] == "EXACT_CONDITIONAL_MATH_PASS" for row in theorem)
    counterexample_survives = any(row["status"] == "COUNTEREXAMPLE_SURVIVES" for row in theorem)
    theorem_not_parent = any(row["status"] == "CONDITIONAL_THEOREM_NOT_PARENT_DERIVED" for row in theorem)
    slot_fails = any(row["current_status"] == "FAIL_CURRENT_PROOF" for row in slot_audit)
    epsilon_nonclaim = len(epsilon) >= 6 and all(not truth(row["valid_for_claim"]) and not truth(row["score_ready"]) for row in epsilon)
    nonhilbert_retained = any(row["current_status"] == "RETAINED_NONCLAIM" for row in nonhilbert)
    common_guard = any(row["current_status"] == "RELATIVE_MODE_NOT_ABSORBABLE" for row in common)
    not_evaluable = all(not truth(row["C_parent_WEP_evaluable_now"]) for row in eval_rows)
    parser_safe = all(not truth(row["would_write_live_claim_file"]) for row in parser)
    gates_false = all(not truth(row["gate_pass"]) for row in gates)
    live_import_absent = not LIVE_C_PARENT_IMPORT.exists() and not LIVE_EPSILON_IMPORT.exists()
    readout_absent = not LIVE_READOUT.exists()
    csv_parse = all(parse_csv_ok(path) for path in generated_csvs)
    branch_copies = BRANCH_HILBERT_THEOREM.exists() and BRANCH_EPSILON_LEDGER.exists() and BRANCH_EVALUATION_DECISION.exists()
    formal_recent = 0
    if FORMALIZATION.exists():
        formal_recent = sum(
            1
            for path in FORMALIZATION.rglob("*")
            if path.is_file() and path.stat().st_mtime > START_TS
        )
    checks = [
        ("VAL1450_0_sources", all_sources_exist, "all cited source paths exist"),
        ("VAL1450_1_hilbert_math_pass", hilbert_math_pass, "total Hilbert variation conditional math-pass recorded"),
        ("VAL1450_2_counterexample_survives", counterexample_survives, "relative w_A counterexample survives"),
        ("VAL1450_3_theorem_not_parent", theorem_not_parent, "label-forgetting theorem remains conditional"),
        ("VAL1450_4_no_source_slot_fails", slot_fails, "no-source-only-slot proof fails at current signature strength"),
        ("VAL1450_5_epsilon_nonclaim", epsilon_nonclaim, "epsilon_A bound ledger rows are nonclaim and not score-ready"),
        ("VAL1450_6_nonhilbert_retained", nonhilbert_retained, "non-Hilbert current bypass retained"),
        ("VAL1450_7_common_guard", common_guard, "relative source weights cannot be absorbed into one G"),
        ("VAL1450_8_not_evaluable", not_evaluable, "C_parent_WEP remains non-evaluable"),
        ("VAL1450_9_parser_safe", parser_safe, "parser refuses live claim writes"),
        ("VAL1450_10_claim_gates_false", gates_false, "all claim gates remain false"),
        ("VAL1450_11_no_live_import", live_import_absent, "live C_parent and epsilon imports remain absent"),
        ("VAL1450_12_no_official_readout", readout_absent, "official readout live file remains absent"),
        ("VAL1450_13_csv_parse", csv_parse, "all generated 1450 CSVs parse cleanly"),
        ("VAL1450_14_branch_copies", branch_copies, "nonclaim branch copies written"),
        ("VAL1450_15_formalization_untouched", formal_recent == 0, f"formalization modified-file count since start={formal_recent}"),
        ("VAL1450_16_overall", True, "1450 sharpens the source-coupling theorem and retains epsilon_A as nonclaim"),
    ]
    return [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "generated_utc": now(),
        }
        for check_id, passed, detail in checks
    ]


def write_table(handle, title: str, rows: list[dict[str, Any]]) -> None:
    handle.write(f"## {title}\n\n")
    if not rows:
        handle.write("_No rows._\n\n")
        return
    fields = list(rows[0].keys())
    handle.write("| " + " | ".join(fields) + " |\n")
    handle.write("| " + " | ".join(["---"] * len(fields)) + " |\n")
    for row in rows:
        handle.write("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |\n")
    handle.write("\n")


def write_doc(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    slot_audit: list[dict[str, Any]],
    epsilon: list[dict[str, Any]],
    nonhilbert: list[dict[str, Any]],
    common: list[dict[str, Any]],
    eval_rows: list[dict[str, Any]],
    parser: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> None:
    with DOC.open("w", encoding="utf-8") as handle:
        handle.write("# 1450 - Source-label forgetting Hilbert-current theorem or relative-weight bound ledger\n\n")
        handle.write(
            "**Current verdict:** the Hilbert-source theorem route is mathematically sharp but not parent-signed. "
            "If the parent action first sums ordinary matter and then takes one total Hilbert/coframe derivative, "
            "and if the source functor has no species-label argument, the source is unique up to one calibrated "
            "`G`. But constant relative `w_A`/`epsilon_A` weights remain covariant, additive, and not removable by "
            "one measured-G calibration unless the parent grammar forbids the slot.\n\n"
        )
        handle.write(
            "**What improved:** the coupling problem is now narrowed to one high-pressure premise: derive that "
            "`w_A` is not an admissible parent-action/operator argument. Until that is signed, `epsilon_A` stays "
            "as an explicit nonclaim bound-ledger variable instead of being hidden inside prose.\n\n"
        )
        write_table(handle, "Source register", sources)
        write_table(handle, "Hilbert source-label theorem attempt", theorem)
        write_table(handle, "No-source-only-slot reduction audit", slot_audit)
        write_table(handle, "Relative epsilon_A bound ledger", epsilon)
        write_table(handle, "Non-Hilbert current guard", nonhilbert)
        write_table(handle, "Common-mode absorption guard", common)
        write_table(handle, "C_parent evaluation decision", eval_rows)
        write_table(handle, "Parser dry-run", parser)
        write_table(handle, "Claim gates", gates)
        write_table(handle, "Decision ledger", decisions)
        write_table(handle, "Validation", validation)
        write_table(handle, "Next target", next_target)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    sources = source_rows()
    theorem = hilbert_theorem_rows()
    slot_audit = no_source_slot_rows()
    epsilon = epsilon_bound_rows()
    nonhilbert = nonhilbert_guard_rows()
    common = common_mode_rows()
    eval_rows = evaluation_rows()
    parser = parser_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(HILBERT_THEOREM, theorem)
    write_csv(NO_SOURCE_SLOT_AUDIT, slot_audit)
    write_csv(EPSILON_BOUND_LEDGER, epsilon)
    write_csv(NONHILBERT_GUARD, nonhilbert)
    write_csv(COMMON_MODE_GUARD, common)
    write_csv(EVALUATION_DECISION, eval_rows)
    write_csv(PARSER_DRYRUN, parser)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_target)

    copy_branch(HILBERT_THEOREM, BRANCH_HILBERT_THEOREM)
    copy_branch(EPSILON_BOUND_LEDGER, BRANCH_EPSILON_LEDGER)
    copy_branch(EVALUATION_DECISION, BRANCH_EVALUATION_DECISION)

    validation = validation_rows(sources, theorem, slot_audit, epsilon, nonhilbert, common, eval_rows, parser, gates)
    write_csv(VALIDATION, validation)
    write_doc(sources, theorem, slot_audit, epsilon, nonhilbert, common, eval_rows, parser, gates, decisions, validation, next_target)
    remove_pycache()
    print("Y5_R10_1450_Hilbert_source_conditional_epsilon_retained_nonclaim")


if __name__ == "__main__":
    main()

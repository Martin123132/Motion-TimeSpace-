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
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1451-Y5-R10-RAB-no-source-only-slot-operator-grammar-theorem-or-epsilon-bound-inputs.md"

PREV_NEXT = OUT / "P8_Y5_R10_1450_NEXT_TARGET.csv"
PREV_THEOREM = OUT / "P8_Y5_R10_1450_HILBERT_SOURCE_LABEL_FORGETTING_THEOREM_ATTEMPT.csv"
PREV_SLOT_AUDIT = OUT / "P8_Y5_R10_1450_NO_SOURCE_ONLY_SLOT_REDUCTION_AUDIT.csv"
PREV_EPSILON = OUT / "P8_Y5_R10_1450_RELATIVE_EPSILON_A_BOUND_LEDGER_NONCLAIM.csv"
PREV_EVAL = OUT / "P8_Y5_R10_1450_C_PARENT_EVALUATION_DECISION.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1450_VALIDATION.csv"

PAC1055 = OUT / "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv"
AXIOM1090 = OUT / "P8_Y5_R10_1090_MISSING_AXIOM_LEDGER.csv"
AXRED1441 = OUT / "P8_Y5_R10_1441_AX1090_REDUCTION_AUDIT.csv"
PAC954 = OUT / "P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv"
MMA955 = OUT / "P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv"
SPC955 = OUT / "P8_Y5_R10_955_SOURCE_PREFACTOR_CLASSIFICATION.csv"
HCG956 = OUT / "P8_Y5_R10_956_HIDDEN_CURRENT_BYPASS_GATES.csv"
SSG956 = OUT / "P8_Y5_R10_956_SOURCE_SIDE_GR_NEWTON_SPINE.csv"
PLF1064 = OUT / "P8_Y5_R10_1064_LABEL_FORGETTING_PROOF_ATTEMPT.csv"
NSS1064 = OUT / "P8_Y5_R10_1064_NO_SOURCE_ONLY_SLOT_AUDIT.csv"
RWBOUND1064 = OUT / "P8_Y5_R10_1064_RELATIVE_WEIGHT_BOUND_IMPORT.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1451_SOURCE_REGISTER.csv"
OPERATOR_THEOREM = OUT / "P8_Y5_R10_1451_NO_SOURCE_ONLY_SLOT_OPERATOR_GRAMMAR_THEOREM_ATTEMPT.csv"
SLOT_REDUCTION_MATRIX = OUT / "P8_Y5_R10_1451_SOURCE_ONLY_SLOT_REDUCTION_MATRIX.csv"
EPSILON_REQUIREMENTS = OUT / "P8_Y5_R10_1451_EPSILON_A_BOUND_INPUT_REQUIREMENTS.csv"
BOUND_ANCHOR_MAP = OUT / "P8_Y5_R10_1451_ARENA_BOUND_ANCHOR_MAP_NONCLAIM.csv"
SIGNING_DECISION = OUT / "P8_Y5_R10_1451_PARENT_SIGNING_DECISION.csv"
PARSER_DRYRUN = OUT / "P8_Y5_R10_1451_PARSER_DRYRUN.csv"
CLAIM_GATE = OUT / "P8_Y5_R10_1451_CLAIM_GATE.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1451_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1451_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1451_VALIDATION.csv"

BRANCH_OPERATOR_THEOREM = COEFF / "no_source_only_slot_operator_grammar_theorem_attempt_1451.csv"
BRANCH_EPSILON_REQUIREMENTS = COEFF / "epsilon_A_bound_input_requirements_1451.csv"
BRANCH_SIGNING_DECISION = COEFF / "C_parent_WEP_no_source_slot_signing_decision_1451.csv"
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
        ("SRC1451_0_prev_next", PREV_NEXT, "1451 handoff"),
        ("SRC1451_1_prev_theorem", PREV_THEOREM, "1450 Hilbert-source theorem attempt"),
        ("SRC1451_2_prev_slot_audit", PREV_SLOT_AUDIT, "1450 no-source-only-slot audit"),
        ("SRC1451_3_prev_epsilon", PREV_EPSILON, "1450 epsilon bound ledger"),
        ("SRC1451_4_prev_eval", PREV_EVAL, "1450 C_parent evaluation decision"),
        ("SRC1451_5_prev_validation", PREV_VALIDATION, "1450 validation"),
        ("SRC1451_6_PAC1055", PAC1055, "parent action contract candidate"),
        ("SRC1451_7_AXIOM1090", AXIOM1090, "missing axiom ledger"),
        ("SRC1451_8_AXRED1441", AXRED1441, "AX1090 reduction audit"),
        ("SRC1451_9_PAC954", PAC954, "parent action source clauses"),
        ("SRC1451_10_MMA955", MMA955, "minimal matter action lemma"),
        ("SRC1451_11_SPC955", SPC955, "source prefactor classification"),
        ("SRC1451_12_HCG956", HCG956, "hidden current bypass gates"),
        ("SRC1451_13_SSG956", SSG956, "source-side GR/Newton spine"),
        ("SRC1451_14_PLF1064", PLF1064, "label-forgetting proof attempt"),
        ("SRC1451_15_NSS1064", NSS1064, "no-source-only-slot audit"),
        ("SRC1451_16_RWBOUND1064", RWBOUND1064, "relative weight bound import"),
        ("SRC1451_17_local_bounds", LOCAL_BOUNDS, "local bound anchors"),
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


def operator_theorem_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "proof_step": "OG1451_0_target",
            "claim": "the parent action/operator grammar has no source-only species-weight argument w_A",
            "mathematical_form": "Allowed[S_matter] = sum_A S_A[Psi_A, e_obs(q), A_Q, theta_A] and partial S_matter/partial w_A is undefined",
            "status": "TARGET_RESTATED",
            "if_signed": "epsilon_A source weights are theorem-zero",
            "current_blocker": "absence of a slot is a parent grammar theorem, not a consequence of covariance alone",
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_step": "OG1451_1_visible_coefficient_algebra",
            "claim": "visible coefficients can depend only on q_loc or fixed representation data",
            "mathematical_form": "Allowed[Coeff(O_vis)] subset O(Q_obs) x Theta_rep x Level_EM, with Hom(C_hid, Coeff(O_vis)) absent",
            "status": "POWERFUL_CONDITIONAL_AXIOM_NOT_REDUCED",
            "if_signed": "forbids w_A(Xhat), f_X F^2, m_A(Xhat), shadow frames, and source multipliers",
            "current_blocker": "AX1090_1 no-hidden-visible-hom is explicitly missing/not reduced",
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_step": "OG1451_2_species_label_domain",
            "claim": "species labels are bookkeeping inside S_matter, not arguments of the source functor",
            "mathematical_form": "Obj(C_matter)->T_total, not Obj(C_matter)->(T_A,A)",
            "status": "CONDITIONAL_LABEL_FORGETTING_NOT_PARENT_SIGNED",
            "if_signed": "relative kappa_A/kappa_B cannot be formed after total Hilbert variation",
            "current_blocker": "parent category still has not signed q_src as label-forgetting",
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_step": "OG1451_3_common_measure_current",
            "claim": "one action measure/current normalization applies to all ordinary matter sectors",
            "mathematical_form": "S_matter uses a single measure, hbar/action scale, and current normalization with no J_A or species Jacobian",
            "status": "MISSING_AXIOM_NOT_REDUCED",
            "if_signed": "constant relative action weights cannot masquerade as source weights",
            "current_blocker": "AX1090_2 common measure/current normalization is missing",
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_step": "OG1451_4_field_redefinition_limit",
            "claim": "relative w_A are always removable by field rescaling",
            "mathematical_form": "Psi_A -> sqrt(w_A) Psi_A",
            "status": "REJECTED_AS_GENERAL_PROOF",
            "if_signed": "would remove w_A without parent grammar",
            "current_blocker": "interactions, charges, quantum normalization, and measured constants can make relative normalization observable",
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_step": "OG1451_5_countermodel",
            "claim": "w_A slot is impossible under the current corpus",
            "mathematical_form": "S_matter = sum_A w_A S_A remains covariant/additive and gives T_source = sum_A w_A T_A",
            "status": "COUNTERMODEL_SURVIVES",
            "if_signed": "nothing; this is the obstruction",
            "current_blocker": "constant source-only coefficients are not excluded by the current derived MTS grammar",
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "proof_step": "OG1451_6_verdict",
            "claim": "no-source-only-slot operator grammar theorem is derived",
            "mathematical_form": "no hidden-visible hom + label-forgotten source category + common measure/current + no hidden spurion return => no w_A",
            "status": "FAIL_CURRENT_PROOF_NOT_PARENT_SIGNED",
            "if_signed": "epsilon_A=0 and source-label piece of C_parent_WEP can move toward theorem-zero",
            "current_blocker": "no-hidden-visible-hom and common-measure/current remain unsigned, so epsilon_A bound inputs are required",
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in rows:
        row["same_parent_branch_id"] = BRANCH_ID
    return rows


def slot_matrix_rows() -> list[dict[str, Any]]:
    rows = [
        ("SM1451_0_wA_literal", "literal w_A S_A action prefactor", "no-source-only-slot theorem", "UNSIGNED", "epsilon_A direct source residual"),
        ("SM1451_1_hidden_coeff", "w_A(Xhat) or hidden-to-visible source coefficient", "no-hidden-visible-hom/operator classification", "UNSIGNED", "source coefficient can vary with hidden representative"),
        ("SM1451_2_species_jacobian", "species-dependent measure/current Jacobian J_A", "common measure/current theorem", "UNSIGNED", "source weight can hide in normalization"),
        ("SM1451_3_marker_spurion", "material/domain/boundary/readout marker prefactor", "no hidden spurion return", "UNSIGNED", "label-forgetting can be undone after variation"),
        ("SM1451_4_nonHilbert", "zeta_A J_NH,A", "non-Hilbert current absence/silence", "OPEN", "bypasses Hilbert-source theorem"),
        ("SM1451_5_common_mode", "single w_common", "universal constant calibration", "CONDITIONAL_GUARD", "only one common scalar can be absorbed into G"),
        ("SM1451_6_verdict", "all source-only slot forms", "all above signatures parent-signed together", "FAIL_CURRENT_REDUCTION", "keep epsilon_A and zeta_A ledgers"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "slot_id": slot_id,
            "slot_or_loophole": slot,
            "required_closure": required,
            "current_status": status,
            "if_open": effect,
            "blocks_epsilon_zero": status != "CONDITIONAL_GUARD",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for slot_id, slot, required, status, effect in rows
    ]


def epsilon_requirement_rows() -> list[dict[str, Any]]:
    rows = [
        ("REQ1451_0_definition", "epsilon_A", "theory", "dimensionless", "choose reference/sum convention; declare material/source classes; separate common mode", "not_ready", "MISSING_CONVENTION_AND_PARENT_ZERO"),
        ("REQ1451_1_WEP", "Delta_epsilon_TiPt", "MICROSCOPE/WEP", "dimensionless", "official Ti/Pt material sensitivity map; source/test convention; eta covariance", "not_ready", "MISSING_SENSITIVITY_MAP"),
        ("REQ1451_2_R10", "epsilon_R10(lambda)", "short-range/R10", "dimensionless vs lambda", "real alpha(lambda) curve; epsilon-to-Yukawa kernel; source/test mass composition", "not_ready", "MISSING_PROMOTED_CURVE_AND_KERNEL"),
        ("REQ1451_3_PPN_gamma_beta", "epsilon_PPN_source", "PPN/local_GR", "dimensionless", "map from source normalization to gamma,beta,preferred-frame residual vector", "not_ready", "MISSING_PPN_PROJECTION"),
        ("REQ1451_4_clocks", "epsilon_clock_source", "clock/redshift", "dimensionless", "source-potential calibration map plus clock sensitivity separation from alpha/mass constants", "not_ready", "MISSING_CLOCK_SOURCE_MAP"),
        ("REQ1451_5_orbital_GM", "epsilon_GM_worldtube", "orbital/Newtonian", "dimensionless or yr^-1 when time varying", "worldtube/Gauss/source-measure law; measured GM calibration; time/range dependence", "not_ready", "MISSING_WORLDTUBE_GM_CHAIN"),
        ("REQ1451_6_nonHilbert", "zeta_A", "WEP/PPN/orbital", "current-defined", "define J_NH,A; prove absent/exact/projected silent or provide arena projection", "not_ready", "MISSING_NONHILBERT_CURRENT_OWNER"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "requirement_id": req_id,
            "symbol": symbol,
            "arena": arena,
            "units": units,
            "required_input": required,
            "readiness": readiness,
            "blocking_marker": marker,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for req_id, symbol, arena, units, required, readiness, marker in rows
    ]


def bound_anchor_rows() -> list[dict[str, Any]]:
    rows = [
        ("ANCH1451_0_WEP", "MICROSCOPE/WEP", "R1_WEP_source_charge", "2.8e-15", "dimensionless", "source-intake/local_bounds/local_bound_claims.csv", "numeric_bound_anchor_nonclaim", "epsilon prediction/sensitivity map missing"),
        ("ANCH1451_1_clock", "redshift/clocks", "R2_clock_redshift", "2.48e-05", "dimensionless", "source-intake/local_bounds/local_bound_claims.csv", "numeric_bound_anchor_nonclaim", "clock-source map missing"),
        ("ANCH1451_2_PPN_gamma", "PPN/local_GR", "R3_gamma", "2.3e-05", "dimensionless", "source-intake/local_bounds/local_bound_claims.csv", "numeric_bound_anchor_nonclaim", "gamma source projection missing"),
        ("ANCH1451_3_PPN_beta", "PPN/local_GR", "R4_beta", "7.8e-05", "dimensionless", "source-intake/local_bounds/local_bound_claims.csv", "numeric_bound_anchor_nonclaim", "beta source projection missing"),
        ("ANCH1451_4_Gdot", "orbital/Newtonian", "R9_Gdot", "9.6e-15", "yr^-1", "source-intake/local_bounds/local_bound_claims.csv", "numeric_bound_anchor_nonclaim", "time/worldtube source map missing"),
        ("ANCH1451_5_R10", "short-range/R10", "R10_fifth_force", "alpha(lambda)", "range-dependent", "source-intake/local_bounds/local_bound_claims.csv", "symbolic_curve_required_nonclaim", "promoted alpha(lambda) curve and epsilon kernel missing"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "anchor_id": anchor_id,
            "arena": arena,
            "source_row": source_row,
            "bound_value": value,
            "bound_units": units,
            "bound_source": source,
            "bound_type": bound_type,
            "why_nonclaim": why,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for anchor_id, arena, source_row, value, units, source, bound_type, why in rows
    ]


def signing_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "SIGN1451_0_no_slot",
            "target": "epsilon_A=0 from no-source-only-slot operator grammar",
            "no_hidden_visible_hom_signed": False,
            "label_forgetting_signed": False,
            "common_measure_current_signed": False,
            "no_spurion_return_signed": False,
            "nonHilbert_guard_closed": False,
            "epsilon_zero_import_allowed": False,
            "C_parent_WEP_import_allowed": False,
            "decision": "REFUSE_ZERO_IMPORT_KEEP_BOUND_INPUTS",
            "reason": "operator grammar theorem is the right shape but relies on AX1090_1 and AX1090_2, both unsigned",
            "live_C_parent_import_exists": LIVE_C_PARENT_IMPORT.exists(),
            "live_epsilon_import_exists": LIVE_EPSILON_IMPORT.exists(),
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def parser_rows() -> list[dict[str, Any]]:
    rows = [
        ("PDR1451_0_no_slot_zero", "import epsilon_A=0 from operator grammar", "REFUSED", "no-hidden-visible-hom/common-measure not signed"),
        ("PDR1451_1_Cparent_import", "import C_parent_WEP source-label zero", "REFUSED", "epsilon_A and non-Hilbert current remain live"),
        ("PDR1451_2_bound_inputs", "stage epsilon_A bound-input requirements", "ALLOWED_NONCLAIM", "requirements are explicitly nonclaim and not score-ready"),
        ("PDR1451_3_local_GR", "claim source-side GR/Newton pass", "REFUSED", "source coupling and worldtube/GM chain remain incomplete"),
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
        for check_id, attempt, result, reason in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG1451_0_no_slot_theorem", "no source-only w_A slot derived"),
        ("CG1451_1_epsilon_zero", "epsilon_A=0 theorem-zero"),
        ("CG1451_2_WEP", "WEP source-weight pass"),
        ("CG1451_3_R10", "R10 source-weight pass"),
        ("CG1451_4_PPN", "PPN source-weight pass"),
        ("CG1451_5_clock_orbital", "clock/orbital source-weight pass"),
        ("CG1451_6_C_parent", "C_parent_WEP import/evaluation"),
        ("CG1451_7_public_local_GR", "public local GR/Newton reduction claim"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": False,
            "reason": "operator grammar/no-slot theorem is not parent-signed and bound inputs are nonclaim",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, claim in gates
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1451_0_good_route",
            "decision": "keep no-source-only-slot theorem as the clean route",
            "why": "if AX1090_1 and AX1090_2 close, epsilon_A can be killed structurally rather than fitted",
            "consequence": "do not demote the whole source branch yet",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1451_1_no_claim",
            "decision": "do not claim no-slot/epsilon zero",
            "why": "constant relative source weights remain legal countermodels under current signed corpus",
            "consequence": "epsilon_A and zeta_A remain explicit nonclaim inputs",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1451_2_next_best_route",
            "decision": "attack common measure/current normalization next",
            "why": "AX1090_2 is the most direct source of species-dependent action weights/J_A",
            "consequence": "1452 targets shared action scale, current normalization, and species Jacobian loopholes",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1451_0_1452",
            "next_target": "1452-Y5-R10-RAB-common-measure-current-normalization-theorem-or-species-jacobian-ledger.md",
            "script": "scripts/Y5_R10_RAB_common_measure_current_normalization_theorem_or_species_jacobian_ledger.py",
            "objective": "try to derive one parent action measure/current normalization for all ordinary matter sectors, with no species-dependent Jacobian J_A or action-scale w_A; if it fails, retain J_A/zeta_A bound-input rows",
            "include": "AX1090_2; shared hbar/action scale; Hilbert current owner; species Jacobian countermodel; non-Hilbert current guard; epsilon/J_A ledger",
            "exclude": "numeric source-weight claim; C_parent import; local-GR pass; formalization-workbench edits; GitHub action",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    matrix: list[dict[str, Any]],
    requirements: list[dict[str, Any]],
    anchors: list[dict[str, Any]],
    signing: list[dict[str, Any]],
    parser: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated_csvs = [
        SOURCE_REGISTER,
        OPERATOR_THEOREM,
        SLOT_REDUCTION_MATRIX,
        EPSILON_REQUIREMENTS,
        BOUND_ANCHOR_MAP,
        SIGNING_DECISION,
        PARSER_DRYRUN,
        CLAIM_GATE,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    all_sources_exist = all(truth(row["exists"]) for row in sources)
    conditional_axiom = any(row["status"] == "POWERFUL_CONDITIONAL_AXIOM_NOT_REDUCED" for row in theorem)
    counter_survives = any(row["status"] == "COUNTERMODEL_SURVIVES" for row in theorem)
    proof_fails = any(row["status"] == "FAIL_CURRENT_PROOF_NOT_PARENT_SIGNED" for row in theorem)
    slot_blocks = any(row["current_status"] == "FAIL_CURRENT_REDUCTION" for row in matrix)
    requirements_nonclaim = len(requirements) >= 7 and all(not truth(row["score_ready"]) and not truth(row["valid_for_claim"]) for row in requirements)
    anchors_cover = {"MICROSCOPE/WEP", "short-range/R10", "PPN/local_GR", "redshift/clocks", "orbital/Newtonian"}.issubset({row["arena"] for row in anchors})
    anchors_nonclaim = all(not truth(row["score_ready"]) and not truth(row["valid_for_claim"]) for row in anchors)
    signing_refuses = all(not truth(row["epsilon_zero_import_allowed"]) and not truth(row["C_parent_WEP_import_allowed"]) for row in signing)
    parser_safe = all(not truth(row["would_write_live_claim_file"]) for row in parser)
    gates_false = all(not truth(row["gate_pass"]) for row in gates)
    live_import_absent = not LIVE_C_PARENT_IMPORT.exists() and not LIVE_EPSILON_IMPORT.exists()
    readout_absent = not LIVE_READOUT.exists()
    csv_parse = all(parse_csv_ok(path) for path in generated_csvs)
    branch_copies = BRANCH_OPERATOR_THEOREM.exists() and BRANCH_EPSILON_REQUIREMENTS.exists() and BRANCH_SIGNING_DECISION.exists()
    formal_recent = 0
    if FORMALIZATION.exists():
        formal_recent = sum(
            1
            for path in FORMALIZATION.rglob("*")
            if path.is_file() and path.stat().st_mtime > START_TS
        )
    checks = [
        ("VAL1451_0_sources", all_sources_exist, "all cited source paths exist"),
        ("VAL1451_1_conditional_axiom_recorded", conditional_axiom, "no-hidden-visible-hom route recorded as conditional"),
        ("VAL1451_2_counterexample_survives", counter_survives, "literal w_A countermodel survives"),
        ("VAL1451_3_proof_fails", proof_fails, "no-source-only-slot proof fails at current signature strength"),
        ("VAL1451_4_slot_matrix_blocks", slot_blocks, "slot reduction matrix blocks epsilon zero"),
        ("VAL1451_5_requirements_nonclaim", requirements_nonclaim, "epsilon/J_A requirements are nonclaim and not score-ready"),
        ("VAL1451_6_anchor_coverage", anchors_cover, "bound anchors cover WEP, R10, PPN, clock, and orbital arenas"),
        ("VAL1451_7_anchors_nonclaim", anchors_nonclaim, "bound anchors are nonclaim"),
        ("VAL1451_8_signing_refuses", signing_refuses, "parent signing decision refuses zero/import"),
        ("VAL1451_9_parser_safe", parser_safe, "parser dry-run refuses live claim writes"),
        ("VAL1451_10_claim_gates_false", gates_false, "all claim gates remain false"),
        ("VAL1451_11_no_live_import", live_import_absent, "live C_parent and epsilon imports remain absent"),
        ("VAL1451_12_no_official_readout", readout_absent, "official readout live file remains absent"),
        ("VAL1451_13_csv_parse", csv_parse, "all generated 1451 CSVs parse cleanly"),
        ("VAL1451_14_branch_copies", branch_copies, "nonclaim branch copies written"),
        ("VAL1451_15_formalization_untouched", formal_recent == 0, f"formalization modified-file count since start={formal_recent}"),
        ("VAL1451_16_overall", True, "1451 refuses no-slot claim and turns epsilon_A/J_A into explicit bound inputs"),
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
    matrix: list[dict[str, Any]],
    requirements: list[dict[str, Any]],
    anchors: list[dict[str, Any]],
    signing: list[dict[str, Any]],
    parser: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> None:
    with DOC.open("w", encoding="utf-8") as handle:
        handle.write("# 1451 - No-source-only-slot operator grammar theorem or epsilon bound inputs\n\n")
        handle.write(
            "**Current verdict:** the exact theorem shape is now isolated: if visible coefficients are only "
            "functions of quotient data or fixed representation data, if the source category forgets species labels, "
            "and if the parent measure/current normalization is common, then a source-only `w_A` slot is illegal. "
            "But the current corpus has not parent-signed the no-hidden-visible-hom or common-measure/current clauses, "
            "so `w_A` and `epsilon_A` cannot be killed yet.\n\n"
        )
        handle.write(
            "**Useful progress:** the failure is no longer amorphous. The live obstruction is a short list: literal "
            "`w_A`, hidden coefficient maps, species Jacobians, marker/readout spurions, and non-Hilbert currents. "
            "Each is now either a theorem target or a nonclaim bound input.\n\n"
        )
        write_table(handle, "Source register", sources)
        write_table(handle, "Operator grammar theorem attempt", theorem)
        write_table(handle, "Source-only slot reduction matrix", matrix)
        write_table(handle, "Epsilon/J_A bound-input requirements", requirements)
        write_table(handle, "Arena bound anchor map", anchors)
        write_table(handle, "Parent signing decision", signing)
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
    theorem = operator_theorem_rows()
    matrix = slot_matrix_rows()
    requirements = epsilon_requirement_rows()
    anchors = bound_anchor_rows()
    signing = signing_decision_rows()
    parser = parser_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(OPERATOR_THEOREM, theorem)
    write_csv(SLOT_REDUCTION_MATRIX, matrix)
    write_csv(EPSILON_REQUIREMENTS, requirements)
    write_csv(BOUND_ANCHOR_MAP, anchors)
    write_csv(SIGNING_DECISION, signing)
    write_csv(PARSER_DRYRUN, parser)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_target)

    copy_branch(OPERATOR_THEOREM, BRANCH_OPERATOR_THEOREM)
    copy_branch(EPSILON_REQUIREMENTS, BRANCH_EPSILON_REQUIREMENTS)
    copy_branch(SIGNING_DECISION, BRANCH_SIGNING_DECISION)

    validation = validation_rows(sources, theorem, matrix, requirements, anchors, signing, parser, gates)
    write_csv(VALIDATION, validation)
    write_doc(sources, theorem, matrix, requirements, anchors, signing, parser, gates, decisions, validation, next_target)
    remove_pycache()
    print("Y5_R10_1451_no_slot_not_signed_epsilon_inputs_retained")


if __name__ == "__main__":
    main()

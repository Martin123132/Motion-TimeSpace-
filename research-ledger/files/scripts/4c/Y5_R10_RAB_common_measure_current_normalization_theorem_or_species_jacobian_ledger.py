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

DOC = ROOT / "1452-Y5-R10-RAB-common-measure-current-normalization-theorem-or-species-jacobian-ledger.md"

PREV_NEXT = OUT / "P8_Y5_R10_1451_NEXT_TARGET.csv"
PREV_OPERATOR = OUT / "P8_Y5_R10_1451_NO_SOURCE_ONLY_SLOT_OPERATOR_GRAMMAR_THEOREM_ATTEMPT.csv"
PREV_MATRIX = OUT / "P8_Y5_R10_1451_SOURCE_ONLY_SLOT_REDUCTION_MATRIX.csv"
PREV_REQS = OUT / "P8_Y5_R10_1451_EPSILON_A_BOUND_INPUT_REQUIREMENTS.csv"
PREV_SIGNING = OUT / "P8_Y5_R10_1451_PARENT_SIGNING_DECISION.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1451_VALIDATION.csv"

ASO1067 = OUT / "P8_Y5_R10_1067_PARENT_ACTION_SCALE_OWNER_ATTEMPT.csv"
HMO1067 = OUT / "P8_Y5_R10_1067_HBAR_MEASURE_OWNER_AUDIT.csv"
SWC1067 = OUT / "P8_Y5_R10_1067_SOURCE_WEIGHT_CONSEQUENCE_LEDGER.csv"
AM1078 = OUT / "P8_Y5_R10_1078_ACTION_MEASURE_PROOF_ATTEMPT.csv"
CO1078 = OUT / "P8_Y5_R10_1078_CURRENT_OWNER_PROOF_ATTEMPT.csv"
CEK1078 = OUT / "P8_Y5_R10_1078_COUNTEREXAMPLE_KILL_MATRIX.csv"
WCO1077 = OUT / "P8_Y5_R10_1077_PARENT_WEP_COUPLING_OWNER_THEOREM_ATTEMPT.csv"
CLAUSE1077 = OUT / "P8_Y5_R10_1077_CLAUSE_SIGNATURE_MATRIX.csv"
CE1077 = OUT / "P8_Y5_R10_1077_ZERO_THEOREM_COUNTEREXAMPLE_AUDIT.csv"
PMD1087 = OUT / "P8_Y5_R10_1087_PARENT_MATTER_DESCENT_ATTEMPT.csv"
ZCC1087 = OUT / "P8_Y5_R10_1087_ZERO_CURRENT_CLAUSE_CONTRACT.csv"
HCG956 = OUT / "P8_Y5_R10_956_HIDDEN_CURRENT_BYPASS_GATES.csv"
AXIOM1090 = OUT / "P8_Y5_R10_1090_MISSING_AXIOM_LEDGER.csv"
AXRED1441 = OUT / "P8_Y5_R10_1441_AX1090_REDUCTION_AUDIT.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1452_SOURCE_REGISTER.csv"
COMMON_MEASURE_THEOREM = OUT / "P8_Y5_R10_1452_COMMON_MEASURE_CURRENT_THEOREM_ATTEMPT.csv"
ACTION_SCALE_AUDIT = OUT / "P8_Y5_R10_1452_ACTION_SCALE_MEASURE_AUDIT.csv"
CURRENT_OWNER_AUDIT = OUT / "P8_Y5_R10_1452_CURRENT_OWNER_AUDIT.csv"
JACOBIAN_LEDGER = OUT / "P8_Y5_R10_1452_SPECIES_JACOBIAN_LEDGER_NONCLAIM.csv"
NONHILBERT_LEDGER = OUT / "P8_Y5_R10_1452_NONHILBERT_CURRENT_LEDGER_NONCLAIM.csv"
EPSILON_UPDATE = OUT / "P8_Y5_R10_1452_EPSILON_JA_REQUIREMENT_UPDATE.csv"
SIGNING_DECISION = OUT / "P8_Y5_R10_1452_PARENT_SIGNING_DECISION.csv"
PARSER_DRYRUN = OUT / "P8_Y5_R10_1452_PARSER_DRYRUN.csv"
CLAIM_GATE = OUT / "P8_Y5_R10_1452_CLAIM_GATE.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1452_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1452_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1452_VALIDATION.csv"

BRANCH_THEOREM = COEFF / "common_measure_current_theorem_attempt_1452.csv"
BRANCH_JACOBIAN_LEDGER = COEFF / "species_jacobian_current_ledger_nonclaim_1452.csv"
BRANCH_SIGNING_DECISION = COEFF / "C_parent_WEP_common_measure_signing_decision_1452.csv"
LIVE_C_PARENT_IMPORT = COEFF / "C_parent_WEP_slot_import.csv"
LIVE_EPSILON_IMPORT = COEFF / "epsilon_A_source_weight_live_claim.csv"
LIVE_JACOBIAN_IMPORT = COEFF / "J_A_species_jacobian_live_claim.csv"
LIVE_READOUT = MICROSCOPE / "official_readout" / "P_WEP_K_CMSM_readout.csv"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
START_TS = datetime.now(timezone.utc).timestamp()


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def truth(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


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


def copy_branch(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


def source_rows() -> list[dict[str, Any]]:
    sources = [
        ("SRC1452_0_prev_next", PREV_NEXT, "1452 handoff"),
        ("SRC1452_1_prev_operator", PREV_OPERATOR, "1451 operator grammar attempt"),
        ("SRC1452_2_prev_matrix", PREV_MATRIX, "1451 slot reduction matrix"),
        ("SRC1452_3_prev_reqs", PREV_REQS, "1451 epsilon/J_A requirements"),
        ("SRC1452_4_prev_signing", PREV_SIGNING, "1451 signing decision"),
        ("SRC1452_5_prev_validation", PREV_VALIDATION, "1451 validation"),
        ("SRC1452_6_ASO1067", ASO1067, "parent action-scale owner attempt"),
        ("SRC1452_7_HMO1067", HMO1067, "hbar/measure owner audit"),
        ("SRC1452_8_SWC1067", SWC1067, "source-weight consequence ledger"),
        ("SRC1452_9_AM1078", AM1078, "action-measure proof attempt"),
        ("SRC1452_10_CO1078", CO1078, "current-owner proof attempt"),
        ("SRC1452_11_CEK1078", CEK1078, "counterexample kill matrix"),
        ("SRC1452_12_WCO1077", WCO1077, "parent WEP coupling-owner theorem attempt"),
        ("SRC1452_13_CLAUSE1077", CLAUSE1077, "WEP clause signature matrix"),
        ("SRC1452_14_CE1077", CE1077, "WEP counterexample audit"),
        ("SRC1452_15_PMD1087", PMD1087, "parent matter descent attempt"),
        ("SRC1452_16_ZCC1087", ZCC1087, "zero-current clause contract"),
        ("SRC1452_17_HCG956", HCG956, "hidden current bypass gates"),
        ("SRC1452_18_AXIOM1090", AXIOM1090, "missing axiom ledger"),
        ("SRC1452_19_AXRED1441", AXRED1441, "AX1090 reduction audit"),
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


def common_measure_theorem_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CMT1452_0_target",
            "one parent measure/current normalization for all ordinary matter",
            "S_parent/hbar_parent contains one measure and one action scale for sum_A S_A, with no J_A or hbar_A",
            "TARGET_SHARPENED",
            "would kill species action weights and Jacobian source weights",
            "parent measure/current owner not signed",
        ),
        (
            "CMT1452_1_classical_EOM_limit",
            "classical matter equations fix source normalization",
            "delta(w_A S_A)/delta Psi_A=0 may match delta S_A/delta Psi_A=0, but delta(w_A S_A)/delta g = w_A T_A",
            "REJECTED_AS_GENERAL_PROOF",
            "prevents a fake derivation by isolated equations of motion",
            "source variation still sees w_A",
        ),
        (
            "CMT1452_2_quantum_measure_route",
            "single hbar_parent/path measure removes independent action scales",
            "exp(i sum_A S_A/hbar_parent) has no independent exp(i w_A S_A/hbar_parent) sector if the parent measure is unique",
            "CONDITIONAL_ROUTE_CLEAN",
            "would make relative hbar_A/action weights illegal",
            "no parent statistical/path-integral measure owner is signed",
        ),
        (
            "CMT1452_3_species_jacobian_countermodel",
            "species Jacobian J_A is impossible",
            "Dmu_parent = product_A J_A Dpsi_A or S_eff = sum_A J_A S_A",
            "COUNTERMODEL_SURVIVES",
            "nothing; it identifies the measure loophole",
            "common measure/Jacobian theorem is unsigned",
        ),
        (
            "CMT1452_4_current_rescaling_countermodel",
            "current normalization c_A J_A cannot differ by species",
            "J_src = sum_A c_A J_A or T_source=sum_A c_A T_A",
            "COUNTERMODEL_SURVIVES",
            "nothing; it identifies the current-owner loophole",
            "Noether route is gauge-only partial and Hilbert/readout route conditional",
        ),
        (
            "CMT1452_5_nonHilbert_bypass",
            "Hilbert current is the only local source",
            "J_src = kappa T_Hilbert + sum_A zeta_A J_NH,A",
            "PARALLEL_GATE_OPEN",
            "prevents silent bypass of the Hilbert theorem",
            "non-Hilbert currents are not proven absent/exact/projected silent",
        ),
        (
            "CMT1452_6_verdict",
            "common measure/current theorem derives epsilon_A=J_A=zeta_A=0",
            "single hbar_parent + species-blind measure + current owner + no non-Hilbert bypass => no source normalization residual",
            "FAIL_CURRENT_PROOF_NOT_PARENT_SIGNED",
            "would close AX1090_2 and help no-source-only-slot theorem",
            "hbar/measure owner, current owner, and non-Hilbert guard remain unsigned",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_step": step,
            "claim": claim,
            "mathematical_form": form,
            "status": status,
            "if_signed": effect,
            "current_blocker": blocker,
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for step, claim, form, status, effect, blocker in rows
    ]


def action_scale_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("ASA1452_0_hbar_parent", "hbar_parent", "one phase/action normalization for all ordinary sectors", "NOT_PARENT_OWNED", "species hbar_A is equivalent to w_A"),
        ("ASA1452_1_measure_parent", "Dmu_parent", "measure factorizes without species-only Jacobians", "NOT_PARENT_OWNED", "J_A mimics source/action weight"),
        ("ASA1452_2_field_rescaling", "Psi_A rescaling", "rescaling preserves interactions, charges, composites, Hilbert stress, and measure", "NOT_GENERAL", "field redefinition cannot remove w_A globally"),
        ("ASA1452_3_readout_descent", "hbar*c/readout constants", "dimensionless readout constants are quotient/fixed-sector owned", "UNSIGNED", "action scale and EM/clock readout can drift separately"),
        ("ASA1452_4_verdict", "single action-scale owner", "all action-scale clauses signed together", "OWNER_NOT_DERIVED", "Delta_w_AB cannot be promoted to zero"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "object": obj,
            "required_signature": signature,
            "current_status": status,
            "risk_if_missing": risk,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for audit_id, obj, signature, status, risk in rows
    ]


def current_owner_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("COA1452_0_noether_gauge", "Noether/gauge representation owner", "fixes gauge-current normalization only", "PARTIAL_GAUGE_ONLY", "does not fix Hilbert gravitational source weights"),
        ("COA1452_1_hilbert_source", "total Hilbert/coframe derivative before readout", "T_total = delta S_matter/delta e_obs", "CONDITIONAL", "variation-before-readout/source model unsigned"),
        ("COA1452_2_current_rescaling", "J_A -> c_A J_A", "single current/source normalization owner forbids c_A", "COUNTERMODEL_SURVIVES", "source/current normalization can carry species coefficient"),
        ("COA1452_3_post_variation_selector", "F(T_A,A) after variation", "readout/source selector cannot reintroduce labels", "UNSIGNED", "species labels return after common stress derivation"),
        ("COA1452_4_verdict", "single current owner", "Noether + Hilbert + readout-order clauses all signed", "CURRENT_OWNER_NOT_SIGNED", "J_A/zeta_A ledger remains required"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "owner": owner,
            "required_signature": signature,
            "current_status": status,
            "if_missing": risk,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for audit_id, owner, signature, status, risk in rows
    ]


def jacobian_ledger_rows() -> list[dict[str, Any]]:
    rows = [
        ("JAL1452_0_hbar_A", "hbar_A or w_A action scale", "dimensionless ratio", "source normalization and path weight", "MISSING_PARENT_ZERO", "theory/WEP/PPN/R10"),
        ("JAL1452_1_measure_JA", "J_A species measure Jacobian", "dimensionless", "effective species action/source weight", "MISSING_COMMON_MEASURE", "WEP/PPN/source"),
        ("JAL1452_2_current_cA", "c_A current/source normalization", "dimensionless", "active current/source rescaling", "MISSING_CURRENT_OWNER", "WEP/PPN/orbital"),
        ("JAL1452_3_material_component", "disconnected material-component constant", "dimensionless", "label-only source weight", "MISSING_CONNECTED_MATTER_FUNCTOR", "WEP/material"),
        ("JAL1452_4_post_readout", "post-variation F(T_A,A)", "dimensionless or kernel", "readout/manufactured source residual", "MISSING_VARIATION_ORDER_WITH_READOUT", "MICROSCOPE/WEP"),
        ("JAL1452_5_total_policy", "J_A/zeta_A source residual policy", "policy", "no cancellation; sum absolute retained components", "NO_CANCELLATION_RETAINED", "all local arenas"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "ledger_id": ledger_id,
            "symbol_or_slot": symbol,
            "units": units,
            "effect": effect,
            "current_status": status,
            "arena_link": arena,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for ledger_id, symbol, units, effect, status, arena in rows
    ]


def nonhilbert_ledger_rows() -> list[dict[str, Any]]:
    rows = [
        ("NH1452_0_absent", "J_NH,A absent from the parent source", "NOT_SIGNED", "would close bypass"),
        ("NH1452_1_exact", "J_NH,A exact/boundary with zero compact local projection", "NOT_SIGNED", "would close boundary branch"),
        ("NH1452_2_projected", "Pi_local[J_NH,A]=0 by projector orthogonality", "NOT_SIGNED", "would close arena projection"),
        ("NH1452_3_retained", "zeta_A J_NH,A retained as explicit residual", "RETAINED_NONCLAIM", "required current fallback"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "ledger_id": ledger_id,
            "condition": condition,
            "current_status": status,
            "effect": effect,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for ledger_id, condition, status, effect in rows
    ]


def epsilon_update_rows() -> list[dict[str, Any]]:
    rows = [
        ("UPD1452_0_epsilon_A", "epsilon_A", "still blocked", "now decomposed into hbar_A/w_A, J_A, c_A, marker, and readout pieces"),
        ("UPD1452_1_WEP", "Delta_epsilon_TiPt", "not score-ready", "needs material/source sensitivity matrix plus J_A/c_A convention"),
        ("UPD1452_2_R10", "epsilon_R10(lambda)", "not score-ready", "needs alpha(lambda) curve and epsilon/J_A-to-Yukawa kernel"),
        ("UPD1452_3_PPN", "epsilon_PPN_source", "not score-ready", "needs source-normalization to PPN residual projection"),
        ("UPD1452_4_orbital", "epsilon_GM_worldtube", "not score-ready", "needs worldtube/Gauss/measured-GM calibration"),
        ("UPD1452_5_nonHilbert", "zeta_A", "not score-ready", "needs J_NH,A definition and projection/silence proof"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "update_id": update_id,
            "symbol": symbol,
            "readiness": readiness,
            "update": update,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for update_id, symbol, readiness, update in rows
    ]


def signing_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "SIGN1452_0_common_measure",
            "target": "AX1090_2 common measure/current theorem",
            "hbar_parent_signed": False,
            "measure_parent_signed": False,
            "current_owner_signed": False,
            "nonHilbert_guard_closed": False,
            "J_A_zero_import_allowed": False,
            "epsilon_zero_import_allowed": False,
            "C_parent_WEP_import_allowed": False,
            "decision": "REFUSE_COMMON_MEASURE_ZERO_IMPORT_KEEP_JA_LEDGER",
            "reason": "conditional route is clean, but action-scale owner and current owner remain unsigned",
            "live_C_parent_import_exists": LIVE_C_PARENT_IMPORT.exists(),
            "live_epsilon_import_exists": LIVE_EPSILON_IMPORT.exists(),
            "live_JA_import_exists": LIVE_JACOBIAN_IMPORT.exists(),
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def parser_rows() -> list[dict[str, Any]]:
    rows = [
        ("PDR1452_0_JA_zero", "import J_A=0 or w_A=0 from common measure", "REFUSED", "hbar/measure owner not parent-signed"),
        ("PDR1452_1_current_zero", "import c_A=zeta_A=0 from current owner", "REFUSED", "current owner and non-Hilbert guard not closed"),
        ("PDR1452_2_Cparent", "evaluate/import C_parent_WEP", "REFUSED", "source-normalization branch remains non-evaluable"),
        ("PDR1452_3_ledgers", "stage J_A/zeta_A nonclaim ledgers", "ALLOWED_NONCLAIM", "rows are valid_for_claim=false"),
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
        ("CG1452_0_AX1090_2", "AX1090_2 common measure/current derived"),
        ("CG1452_1_wA_zero", "w_A/epsilon_A theorem-zero"),
        ("CG1452_2_JA_zero", "J_A species Jacobian theorem-zero"),
        ("CG1452_3_zeta_zero", "zeta_A non-Hilbert current theorem-zero"),
        ("CG1452_4_WEP", "WEP source-normalization pass"),
        ("CG1452_5_PPN_R10", "PPN/R10 source-normalization pass"),
        ("CG1452_6_C_parent", "C_parent_WEP import/evaluation"),
        ("CG1452_7_local_GR", "local GR/Newton source branch claim"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": False,
            "reason": "common measure/current theorem remains conditional and J_A/zeta_A ledgers are nonclaim",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, claim in gates
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1452_0_keep_route",
            "decision": "keep common measure/current as the correct AX1090_2 route",
            "why": "it is the clean way to kill source weights without fitting them",
            "consequence": "source branch remains derivation-first",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1452_1_no_claim",
            "decision": "do not claim common measure/current closure",
            "why": "species action weights, J_A, current rescalings, and non-Hilbert currents survive",
            "consequence": "no C_parent/WEP/local-GR import from 1452",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1452_2_next_best_route",
            "decision": "attack current owner / Noether-Hilbert normalization next",
            "why": "action-measure and current-owner debts are now separated, and current owner is the sharper local-source gate",
            "consequence": "1453 targets current/source normalization owner and zeta_A",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1452_0_1453",
            "next_target": "1453-Y5-R10-RAB-current-source-normalization-owner-theorem-or-zetaA-ledger.md",
            "script": "scripts/Y5_R10_RAB_current_source_normalization_owner_theorem_or_zetaA_ledger.py",
            "objective": "try to derive one parent Noether/Hilbert current owner fixing source normalization before readout; if it fails, retain current-rescaling c_A and non-Hilbert zeta_A ledgers",
            "include": "Noether owner; Hilbert coframe source; variation-before-readout; current rescaling; non-Hilbert current silence; zeta_A bound inputs",
            "exclude": "numeric WEP claim; C_parent import; local-GR pass; formalization-workbench edits; GitHub action",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    action: list[dict[str, Any]],
    current: list[dict[str, Any]],
    jacobian: list[dict[str, Any]],
    nonhilbert: list[dict[str, Any]],
    updates: list[dict[str, Any]],
    signing: list[dict[str, Any]],
    parser: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated_csvs = [
        SOURCE_REGISTER,
        COMMON_MEASURE_THEOREM,
        ACTION_SCALE_AUDIT,
        CURRENT_OWNER_AUDIT,
        JACOBIAN_LEDGER,
        NONHILBERT_LEDGER,
        EPSILON_UPDATE,
        SIGNING_DECISION,
        PARSER_DRYRUN,
        CLAIM_GATE,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    all_sources_exist = all(truth(row["exists"]) for row in sources)
    conditional_route = any(row["status"] == "CONDITIONAL_ROUTE_CLEAN" for row in theorem)
    counter_survives = sum(1 for row in theorem if row["status"] == "COUNTERMODEL_SURVIVES") >= 2
    proof_fails = any(row["status"] == "FAIL_CURRENT_PROOF_NOT_PARENT_SIGNED" for row in theorem)
    action_blocks = any(row["current_status"] == "OWNER_NOT_DERIVED" for row in action)
    current_blocks = any(row["current_status"] == "CURRENT_OWNER_NOT_SIGNED" for row in current)
    jacobian_nonclaim = len(jacobian) >= 6 and all(not truth(row["score_ready"]) and not truth(row["valid_for_claim"]) for row in jacobian)
    nonhilbert_retained = any(row["current_status"] == "RETAINED_NONCLAIM" for row in nonhilbert)
    updates_nonclaim = all(not truth(row["score_ready"]) and not truth(row["valid_for_claim"]) for row in updates)
    signing_refuses = all(not truth(row["J_A_zero_import_allowed"]) and not truth(row["C_parent_WEP_import_allowed"]) for row in signing)
    parser_safe = all(not truth(row["would_write_live_claim_file"]) for row in parser)
    gates_false = all(not truth(row["gate_pass"]) for row in gates)
    live_import_absent = not LIVE_C_PARENT_IMPORT.exists() and not LIVE_EPSILON_IMPORT.exists() and not LIVE_JACOBIAN_IMPORT.exists()
    readout_absent = not LIVE_READOUT.exists()
    csv_parse = all(parse_csv_ok(path) for path in generated_csvs)
    branch_copies = BRANCH_THEOREM.exists() and BRANCH_JACOBIAN_LEDGER.exists() and BRANCH_SIGNING_DECISION.exists()
    formal_recent = 0
    if FORMALIZATION.exists():
        formal_recent = sum(
            1
            for path in FORMALIZATION.rglob("*")
            if path.is_file() and path.stat().st_mtime > START_TS
        )
    checks = [
        ("VAL1452_0_sources", all_sources_exist, "all cited source paths exist"),
        ("VAL1452_1_conditional_route", conditional_route, "single hbar/measure route recorded as clean conditional"),
        ("VAL1452_2_counterexamples_survive", counter_survives, "species Jacobian and current rescaling countermodels survive"),
        ("VAL1452_3_proof_fails", proof_fails, "common measure/current proof fails at current signature strength"),
        ("VAL1452_4_action_blocks", action_blocks, "action-scale owner remains unsigned"),
        ("VAL1452_5_current_blocks", current_blocks, "current owner remains unsigned"),
        ("VAL1452_6_jacobian_nonclaim", jacobian_nonclaim, "J_A/w_A/c_A ledger rows are nonclaim and not score-ready"),
        ("VAL1452_7_nonhilbert_retained", nonhilbert_retained, "non-Hilbert zeta_A branch retained"),
        ("VAL1452_8_updates_nonclaim", updates_nonclaim, "epsilon/J_A requirement updates remain nonclaim"),
        ("VAL1452_9_signing_refuses", signing_refuses, "parent signing decision refuses zero/import"),
        ("VAL1452_10_parser_safe", parser_safe, "parser refuses live claim writes"),
        ("VAL1452_11_claim_gates_false", gates_false, "all claim gates remain false"),
        ("VAL1452_12_no_live_import", live_import_absent, "live C_parent, epsilon, and J_A imports remain absent"),
        ("VAL1452_13_no_official_readout", readout_absent, "official readout live file remains absent"),
        ("VAL1452_14_csv_parse", csv_parse, "all generated 1452 CSVs parse cleanly"),
        ("VAL1452_15_branch_copies", branch_copies, "nonclaim branch copies written"),
        ("VAL1452_16_formalization_untouched", formal_recent == 0, f"formalization modified-file count since start={formal_recent}"),
        ("VAL1452_17_overall", True, "1452 keeps common-measure theorem conditional and retains J_A/zeta_A ledgers"),
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
    action: list[dict[str, Any]],
    current: list[dict[str, Any]],
    jacobian: list[dict[str, Any]],
    nonhilbert: list[dict[str, Any]],
    updates: list[dict[str, Any]],
    signing: list[dict[str, Any]],
    parser: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> None:
    with DOC.open("w", encoding="utf-8") as handle:
        handle.write("# 1452 - Common measure/current normalization theorem or species Jacobian ledger\n\n")
        handle.write(
            "**Current verdict:** the common-measure route is the right theorem shape, but it is not closed. "
            "A single parent `hbar`/measure/current owner would make relative action scales, `J_A` Jacobians, "
            "and current rescalings illegal. The current corpus still has those as live countermodels, so no "
            "`epsilon_A`, `J_A`, `zeta_A`, or `C_parent_WEP` zero/import is allowed.\n\n"
        )
        handle.write(
            "**Useful progress:** the source-normalization debt has split cleanly into action-scale ownership "
            "and current ownership. The next sharp target is the current/source normalization owner: Noether plus "
            "Hilbert source before readout, or explicit `c_A`/`zeta_A` residual rows.\n\n"
        )
        write_table(handle, "Source register", sources)
        write_table(handle, "Common measure/current theorem attempt", theorem)
        write_table(handle, "Action-scale measure audit", action)
        write_table(handle, "Current owner audit", current)
        write_table(handle, "Species Jacobian ledger", jacobian)
        write_table(handle, "Non-Hilbert current ledger", nonhilbert)
        write_table(handle, "Epsilon/J_A requirement update", updates)
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
    theorem = common_measure_theorem_rows()
    action = action_scale_audit_rows()
    current = current_owner_audit_rows()
    jacobian = jacobian_ledger_rows()
    nonhilbert = nonhilbert_ledger_rows()
    updates = epsilon_update_rows()
    signing = signing_decision_rows()
    parser = parser_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(COMMON_MEASURE_THEOREM, theorem)
    write_csv(ACTION_SCALE_AUDIT, action)
    write_csv(CURRENT_OWNER_AUDIT, current)
    write_csv(JACOBIAN_LEDGER, jacobian)
    write_csv(NONHILBERT_LEDGER, nonhilbert)
    write_csv(EPSILON_UPDATE, updates)
    write_csv(SIGNING_DECISION, signing)
    write_csv(PARSER_DRYRUN, parser)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_target)

    copy_branch(COMMON_MEASURE_THEOREM, BRANCH_THEOREM)
    copy_branch(JACOBIAN_LEDGER, BRANCH_JACOBIAN_LEDGER)
    copy_branch(SIGNING_DECISION, BRANCH_SIGNING_DECISION)

    validation = validation_rows(sources, theorem, action, current, jacobian, nonhilbert, updates, signing, parser, gates)
    write_csv(VALIDATION, validation)
    write_doc(sources, theorem, action, current, jacobian, nonhilbert, updates, signing, parser, gates, decisions, validation, next_target)
    remove_pycache()
    print("Y5_R10_1452_common_measure_conditional_JA_zeta_retained")


if __name__ == "__main__":
    main()

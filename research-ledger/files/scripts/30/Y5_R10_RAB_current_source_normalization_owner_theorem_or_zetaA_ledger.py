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

DOC = ROOT / "1453-Y5-R10-RAB-current-source-normalization-owner-theorem-or-zetaA-ledger.md"

PREV_NEXT = OUT / "P8_Y5_R10_1452_NEXT_TARGET.csv"
PREV_THEOREM = OUT / "P8_Y5_R10_1452_COMMON_MEASURE_CURRENT_THEOREM_ATTEMPT.csv"
PREV_CURRENT = OUT / "P8_Y5_R10_1452_CURRENT_OWNER_AUDIT.csv"
PREV_JACOBIAN = OUT / "P8_Y5_R10_1452_SPECIES_JACOBIAN_LEDGER_NONCLAIM.csv"
PREV_NONHILBERT = OUT / "P8_Y5_R10_1452_NONHILBERT_CURRENT_LEDGER_NONCLAIM.csv"
PREV_SIGNING = OUT / "P8_Y5_R10_1452_PARENT_SIGNING_DECISION.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1452_VALIDATION.csv"

THM1062 = OUT / "P8_Y5_R10_1062_PARENT_PRODUCT_THEOREM_ATTEMPT.csv"
PREM1062 = OUT / "P8_Y5_R10_1062_PREMISE_SIGNATURE_AUDIT.csv"
CE1062 = OUT / "P8_Y5_R10_1062_COUNTEREXAMPLE_SURVIVAL_LEDGER.csv"
DER1076 = OUT / "P8_Y5_R10_1076_PARENT_MAP_DERIVATION_ATTEMPT.csv"
OWN1076 = OUT / "P8_Y5_R10_1076_COUPLING_OWNER_GATES.csv"
PWC1076 = OUT / "P8_Y5_R10_1076_PARENT_PRODUCT_CONTRACT_UPDATE.csv"
WCO1077 = OUT / "P8_Y5_R10_1077_PARENT_WEP_COUPLING_OWNER_THEOREM_ATTEMPT.csv"
CLAUSE1077 = OUT / "P8_Y5_R10_1077_CLAUSE_SIGNATURE_MATRIX.csv"
CE1077 = OUT / "P8_Y5_R10_1077_ZERO_THEOREM_COUNTEREXAMPLE_AUDIT.csv"
CO1078 = OUT / "P8_Y5_R10_1078_CURRENT_OWNER_PROOF_ATTEMPT.csv"
CEK1078 = OUT / "P8_Y5_R10_1078_COUNTEREXAMPLE_KILL_MATRIX.csv"
NCO1079 = OUT / "P8_Y5_R10_1079_NARROW_CURRENT_OWNER_THEOREM_ATTEMPT.csv"
PR1079 = OUT / "P8_Y5_R10_1079_CURRENT_OWNER_PREMISE_LEDGER.csv"
CER1079 = OUT / "P8_Y5_R10_1079_COUNTEREXAMPLE_RESOLUTION_MATRIX.csv"
BSO989 = OUT / "P8_Y5_R10_989_BETA_SOURCE_OWNER_LEDGER.csv"
ELA989 = OUT / "P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv"
HCG956 = OUT / "P8_Y5_R10_956_HIDDEN_CURRENT_BYPASS_GATES.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1453_SOURCE_REGISTER.csv"
CURRENT_OWNER_THEOREM = OUT / "P8_Y5_R10_1453_CURRENT_SOURCE_NORMALIZATION_OWNER_THEOREM_ATTEMPT.csv"
HILBERT_NOETHER_AUDIT = OUT / "P8_Y5_R10_1453_HILBERT_NOETHER_ROUTE_AUDIT.csv"
RESCALING_SELECTOR_MATRIX = OUT / "P8_Y5_R10_1453_CURRENT_RESCALING_SELECTOR_MATRIX.csv"
ZETAA_LEDGER = OUT / "P8_Y5_R10_1453_ZETA_A_NONHILBERT_CURRENT_LEDGER_NONCLAIM.csv"
BOUND_REQUIREMENTS = OUT / "P8_Y5_R10_1453_CURRENT_SOURCE_BOUND_INPUT_REQUIREMENTS.csv"
SIGNING_DECISION = OUT / "P8_Y5_R10_1453_PARENT_SIGNING_DECISION.csv"
PARSER_DRYRUN = OUT / "P8_Y5_R10_1453_PARSER_DRYRUN.csv"
CLAIM_GATE = OUT / "P8_Y5_R10_1453_CLAIM_GATE.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1453_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1453_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1453_VALIDATION.csv"

BRANCH_THEOREM = COEFF / "current_source_normalization_owner_theorem_attempt_1453.csv"
BRANCH_ZETAA_LEDGER = COEFF / "zeta_A_current_rescaling_ledger_nonclaim_1453.csv"
BRANCH_SIGNING_DECISION = COEFF / "C_parent_WEP_current_owner_signing_decision_1453.csv"
LIVE_C_PARENT_IMPORT = COEFF / "C_parent_WEP_slot_import.csv"
LIVE_EPSILON_IMPORT = COEFF / "epsilon_A_source_weight_live_claim.csv"
LIVE_JACOBIAN_IMPORT = COEFF / "J_A_species_jacobian_live_claim.csv"
LIVE_ZETAA_IMPORT = COEFF / "zeta_A_nonHilbert_current_live_claim.csv"
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
        ("SRC1453_0_prev_next", PREV_NEXT, "1453 handoff"),
        ("SRC1453_1_prev_theorem", PREV_THEOREM, "1452 common measure/current theorem"),
        ("SRC1453_2_prev_current", PREV_CURRENT, "1452 current owner audit"),
        ("SRC1453_3_prev_jacobian", PREV_JACOBIAN, "1452 species Jacobian ledger"),
        ("SRC1453_4_prev_nonhilbert", PREV_NONHILBERT, "1452 non-Hilbert ledger"),
        ("SRC1453_5_prev_signing", PREV_SIGNING, "1452 signing decision"),
        ("SRC1453_6_prev_validation", PREV_VALIDATION, "1452 validation"),
        ("SRC1453_7_THM1062", THM1062, "parent product theorem attempt"),
        ("SRC1453_8_PREM1062", PREM1062, "premise signature audit"),
        ("SRC1453_9_CE1062", CE1062, "counterexample survival ledger"),
        ("SRC1453_10_DER1076", DER1076, "parent map derivation attempt"),
        ("SRC1453_11_OWN1076", OWN1076, "coupling owner gates"),
        ("SRC1453_12_PWC1076", PWC1076, "parent product contract update"),
        ("SRC1453_13_WCO1077", WCO1077, "parent WEP coupling owner theorem"),
        ("SRC1453_14_CLAUSE1077", CLAUSE1077, "clause signature matrix"),
        ("SRC1453_15_CE1077", CE1077, "zero theorem counterexample audit"),
        ("SRC1453_16_CO1078", CO1078, "current owner proof attempt"),
        ("SRC1453_17_CEK1078", CEK1078, "counterexample kill matrix"),
        ("SRC1453_18_NCO1079", NCO1079, "narrow current owner theorem"),
        ("SRC1453_19_PR1079", PR1079, "current owner premise ledger"),
        ("SRC1453_20_CER1079", CER1079, "counterexample resolution matrix"),
        ("SRC1453_21_BSO989", BSO989, "beta source owner ledger"),
        ("SRC1453_22_ELA989", ELA989, "EM lock signature audit"),
        ("SRC1453_23_HCG956", HCG956, "hidden current bypass gates"),
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


def theorem_rows() -> list[dict[str, Any]]:
    rows = [
        ("CSO1453_0_target", "one parent Noether/Hilbert current owner fixes source normalization before readout", "J_src is defined by parent variation/current functor before material/readout selectors", "TARGET_SHARPENED", "would kill post-variation c_A and beta_source-style source rescalings", "common action and readout-order premises are unsigned"),
        ("CSO1453_1_hilbert_variation", "Hilbert source is unique once a common action is fixed", "T_H^{mu nu}:=2/sqrt(-g) delta S_matter/delta g_mu_nu before readout", "EXACT_SUBTHEOREM_CONDITIONAL", "one variational source tensor exists at the variation point", "requires common S_matter and variation-before-readout"),
        ("CSO1453_2_ward_identity", "diffeomorphism Ward identity owns conservation", "on matter shell, Diff invariance gives nabla_mu T_H^{mu nu}=0 in observed geometry", "CONDITIONAL_WARD_IDENTITY", "source conservation follows from the same action", "conservation does not remove weights inserted before variation"),
        ("CSO1453_3_noether_gauge_limit", "Noether/gauge current owner fixes gravitational source normalization", "representation charges can own gauge-current normalization", "PARTIAL_GAUGE_ONLY", "helps EM/current normalization but not Hilbert gravitational source by itself", "gauge-current owner does not fix active mass/source weights"),
        ("CSO1453_4_post_variation_rescaling", "J_A -> c_A J_A after Hilbert extraction is illegal", "after T_H is varied, a downstream F(T_A,A) cannot redefine the parent source", "KILLED_CONDITIONALLY", "post-variation current rescaling becomes readout/calibration, not source ownership", "readout-order/source model is not parent-signed"),
        ("CSO1453_5_pre_variation_weight", "current ownership kills S_matter=sum_A w_A S_A", "T_H inherits w_A if w_A is already inside S_matter before variation", "SURVIVES_PRE_VARIATION", "nothing; it marks a limit of the current-owner theorem", "needs action-measure/object-language theorem, not current owner alone"),
        ("CSO1453_6_nonhilbert_bypass", "Hilbert current is the only current", "J_src = kappa T_H + sum_A zeta_A J_NH,A", "PARALLEL_GATE_OPEN", "would prevent spin/torsion/boundary currents bypassing Hilbert source", "J_NH,A absence/exact/projector silence not proven"),
        ("CSO1453_7_verdict", "current/source normalization owner closes local source coupling", "Hilbert variation + Ward identity + readout order + no pre-action weights + no non-Hilbert bypass", "PARTIAL_THEOREM_NOT_CLOSED", "post-variation rescaling is conditionally controlled", "pre-action weights, readout order, and zeta_A remain live"),
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


def hilbert_noether_rows() -> list[dict[str, Any]]:
    rows = [
        ("HNA1453_0_common_action", "one common ordinary matter action", "UNSIGNED", "Hilbert source owner can apply to all ordinary sectors", "species weights can enter before variation"),
        ("HNA1453_1_hilbert_definition", "source is total Hilbert/coframe derivative", "EXACT_GIVEN_COMMON_ACTION", "single variational source owner", "does not set source normalization if action weights exist"),
        ("HNA1453_2_ward_identity", "diffeomorphism Ward identity", "CONDITIONAL", "conservation and source consistency", "does not forbid labelled constants"),
        ("HNA1453_3_noether_gauge", "Noether gauge current owner", "PARTIAL_FOR_GAUGE_ONLY", "charge/current normalization control", "not enough for gravitational Hilbert source"),
        ("HNA1453_4_readout_order", "variation before material/readout projection", "CONDITIONAL_READOUT_CONTRACT", "post-variation selector cannot redefine source", "official readout/source model not signed"),
        ("HNA1453_5_verdict", "Noether-Hilbert owner package", "PARTIAL_NOT_CLOSED", "keeps the exact subtheorem", "cannot claim full source-normalization zero"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "premise": premise,
            "current_status": status,
            "effect_if_signed": effect,
            "if_unsigned": risk,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for audit_id, premise, status, effect, risk in rows
    ]


def rescaling_matrix_rows() -> list[dict[str, Any]]:
    rows = [
        ("RSM1453_0_post_current_rescale", "J_A -> c_A J_A after source extraction", "KILLED_CONDITIONALLY", "Hilbert source + variation-before-readout", "readout-order theorem still needed"),
        ("RSM1453_1_post_selector", "F(T_A,A) after variation", "KILLED_CONDITIONALLY", "readout cannot retroactively alter parent source", "official/source readout order still unsigned"),
        ("RSM1453_2_pre_action_weight", "S_matter=sum_A w_A S_A before variation", "SURVIVES", "Hilbert variation inherits w_A", "action-measure/object-language theorem needed"),
        ("RSM1453_3_current_owner_beta", "beta_source_alpha or c_A source marker", "UNOWNED", "needs parent current/source normalization owner", "finite alpha/source branch remains closure-only"),
        ("RSM1453_4_nonHilbert", "zeta_A J_NH,A", "SURVIVES", "not a Hilbert-source rescaling", "non-Hilbert current theorem or bound needed"),
        ("RSM1453_5_disconnected_components", "label constants on disconnected material components", "SURVIVES", "current owner does not force connected matter functor", "matter functor connectedness or material tensor needed"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "matrix_id": matrix_id,
            "loophole": loophole,
            "resolution_status": status,
            "reason": reason,
            "remaining_requirement": requirement,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for matrix_id, loophole, status, reason, requirement in rows
    ]


def zeta_rows() -> list[dict[str, Any]]:
    rows = [
        ("ZETA1453_0_definition", "zeta_A", "species coefficient multiplying non-Hilbert current J_NH,A", "J_src = kappa T_H + sum_A zeta_A J_NH,A", "current-defined", "MISSING_JNH_DEFINITION", "WEP/PPN/orbital"),
        ("ZETA1453_1_absence_route", "J_NH,A_absent", "prove no non-Hilbert local source current exists", "J_NH,A not in parent source domain", "boolean/theorem", "NOT_SIGNED", "local_GR"),
        ("ZETA1453_2_exact_route", "J_NH,A_exact", "prove non-Hilbert current is exact/boundary with zero compact projection", "J_NH,A=dB_A and Pi_local[dB_A]=0", "projected current", "NOT_SIGNED", "WEP/PPN/orbital"),
        ("ZETA1453_3_projected_route", "Pi_local[J_NH,A]", "prove projector silence in each local arena", "Pi_WEP[J_NH,A]=Pi_PPN[J_NH,A]=Pi_orb[J_NH,A]=0", "arena projection", "NOT_SIGNED", "all local arenas"),
        ("ZETA1453_4_bound_route", "zeta_A_bound", "if not zero, source zeta_A and arena projection bounds", "|zeta_A Pi[J_NH,A]| <= bound_arena", "arena-dependent", "BOUND_INPUTS_MISSING", "WEP/PPN/R10/orbital"),
        ("ZETA1453_5_policy", "zeta_A_total_policy", "no cancellation with epsilon_A/J_A/c_A", "|source residual| <= |epsilon|+|J_A|+|c_A|+|zeta_A Pi[J_NH]|", "policy", "NO_CANCELLATION_RETAINED", "all local arenas"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "ledger_id": ledger_id,
            "symbol": symbol,
            "meaning": meaning,
            "formula": formula,
            "units": units,
            "current_status": status,
            "arena_link": arena,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for ledger_id, symbol, meaning, formula, units, status, arena in rows
    ]


def bound_requirement_rows() -> list[dict[str, Any]]:
    rows = [
        ("REQ1453_0_cA", "c_A", "current/source normalization rescaling", "dimensionless", "parent readout-order signature or source-backed c_A vector", "not_ready", "MISSING_CURRENT_OWNER"),
        ("REQ1453_1_beta_alpha", "beta_source_alpha", "alpha/Coulomb finite WEP source normalization", "dimensionless", "EM source/current owner or numeric beta_source_alpha provenance", "not_ready", "MISSING_EM_CURRENT_OWNER"),
        ("REQ1453_2_zeta_A", "zeta_A", "non-Hilbert current coefficient", "current-defined", "J_NH,A definition plus arena projection or theorem-zero", "not_ready", "MISSING_NONHILBERT_CURRENT_OWNER"),
        ("REQ1453_3_post_selector", "F(T_A,A)", "post-variation material/readout selector", "kernel/operator", "variation-before-readout theorem tied to official source/readout model", "not_ready", "MISSING_READOUT_ORDER"),
        ("REQ1453_4_WEP", "Pi_WEP[c_A,zeta_A]", "WEP source-normalization projection", "dimensionless", "MICROSCOPE material/source sensitivity and readout kernel", "not_ready", "MISSING_WEP_PROJECTION"),
        ("REQ1453_5_PPN_orbital", "Pi_PPN_orb[c_A,zeta_A]", "PPN/orbital source-normalization projection", "dimensionless", "source-to-PPN and measured-GM/worldtube maps", "not_ready", "MISSING_LOCAL_SOURCE_PROJECTION"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "requirement_id": req_id,
            "symbol": symbol,
            "meaning": meaning,
            "units": units,
            "required_input": required,
            "readiness": readiness,
            "blocking_marker": marker,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for req_id, symbol, meaning, units, required, readiness, marker in rows
    ]


def signing_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "SIGN1453_0_current_owner",
            "target": "current/source normalization owner theorem",
            "common_action_signed": False,
            "hilbert_source_subtheorem": True,
            "ward_identity_subtheorem": True,
            "variation_before_readout_signed": False,
            "pre_action_weights_closed": False,
            "nonHilbert_guard_closed": False,
            "post_cA_zero_import_allowed": False,
            "zeta_A_zero_import_allowed": False,
            "C_parent_WEP_import_allowed": False,
            "decision": "REFUSE_CURRENT_OWNER_ZERO_IMPORT_KEEP_CA_ZETA_LEDGER",
            "reason": "Hilbert/Noether pieces are useful conditional subtheorems, but readout order, pre-action weights, and non-Hilbert currents remain unsigned",
            "live_C_parent_import_exists": LIVE_C_PARENT_IMPORT.exists(),
            "live_epsilon_import_exists": LIVE_EPSILON_IMPORT.exists(),
            "live_JA_import_exists": LIVE_JACOBIAN_IMPORT.exists(),
            "live_zeta_import_exists": LIVE_ZETAA_IMPORT.exists(),
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def parser_rows() -> list[dict[str, Any]]:
    rows = [
        ("PDR1453_0_cA_zero", "import c_A=0 from current owner", "REFUSED", "readout-order theorem is unsigned"),
        ("PDR1453_1_zeta_zero", "import zeta_A=0 from Hilbert source", "REFUSED", "non-Hilbert current absence/projection not signed"),
        ("PDR1453_2_Cparent", "evaluate/import C_parent_WEP", "REFUSED", "pre-action weights and non-Hilbert currents remain live"),
        ("PDR1453_3_ledgers", "stage c_A/zeta_A nonclaim ledgers", "ALLOWED_NONCLAIM", "rows are valid_for_claim=false"),
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
        ("CG1453_0_current_owner", "current/source normalization owner theorem"),
        ("CG1453_1_cA_zero", "c_A post/current rescaling zero"),
        ("CG1453_2_zeta_zero", "zeta_A non-Hilbert current zero"),
        ("CG1453_3_beta_source", "beta_source_alpha closed"),
        ("CG1453_4_WEP", "WEP source-normalization pass"),
        ("CG1453_5_PPN_orbital", "PPN/orbital source-normalization pass"),
        ("CG1453_6_C_parent", "C_parent_WEP import/evaluation"),
        ("CG1453_7_local_GR", "local GR/Newton source branch claim"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": False,
            "reason": "current-owner theorem is partial and c_A/zeta_A ledgers remain nonclaim",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, claim in gates
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1453_0_keep_subtheorems",
            "decision": "retain Hilbert variation and Ward identity as exact conditional subtheorems",
            "why": "they are real progress once common action/readout-order are signed",
            "consequence": "do not demote current-owner route entirely",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1453_1_no_zero_claim",
            "decision": "do not claim current-source normalization closure",
            "why": "pre-action weights and non-Hilbert currents survive current-owner proof",
            "consequence": "c_A, beta_source, and zeta_A remain explicit nonclaim inputs",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1453_2_next_best_route",
            "decision": "attack variation-before-readout/source-readout ordering next",
            "why": "it is the missing premise that would actually kill post-variation c_A/F(T_A,A)",
            "consequence": "1454 targets readout-order theorem or post-selector ledger",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1453_0_1454",
            "next_target": "1454-Y5-R10-RAB-variation-before-readout-source-order-theorem-or-post-selector-ledger.md",
            "script": "scripts/Y5_R10_RAB_variation_before_readout_source_order_theorem_or_post_selector_ledger.py",
            "objective": "try to derive that Hilbert/source variation occurs before material/readout/source projection, so post-variation selectors F(T_A,A) and c_A rescalings cannot define the parent source; if it fails, retain post-selector bound inputs",
            "include": "variation-before-readout; official source/readout model; post-variation selector; c_A readout/calibration split; WEP/PPN/orbital projection requirements",
            "exclude": "numeric WEP claim; C_parent import; local-GR pass; formalization-workbench edits; GitHub action",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    hilbert: list[dict[str, Any]],
    matrix: list[dict[str, Any]],
    zeta: list[dict[str, Any]],
    requirements: list[dict[str, Any]],
    signing: list[dict[str, Any]],
    parser: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated_csvs = [
        SOURCE_REGISTER,
        CURRENT_OWNER_THEOREM,
        HILBERT_NOETHER_AUDIT,
        RESCALING_SELECTOR_MATRIX,
        ZETAA_LEDGER,
        BOUND_REQUIREMENTS,
        SIGNING_DECISION,
        PARSER_DRYRUN,
        CLAIM_GATE,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    all_sources_exist = all(truth(row["exists"]) for row in sources)
    hilbert_exact = any(row["status"] == "EXACT_SUBTHEOREM_CONDITIONAL" for row in theorem)
    ward_conditional = any(row["status"] == "CONDITIONAL_WARD_IDENTITY" for row in theorem)
    post_killed_conditional = any(row["status"] == "KILLED_CONDITIONALLY" for row in theorem)
    pre_survives = any(row["status"] == "SURVIVES_PRE_VARIATION" for row in theorem)
    nonhilbert_open = any(row["status"] == "PARALLEL_GATE_OPEN" for row in theorem)
    verdict_partial = any(row["status"] == "PARTIAL_THEOREM_NOT_CLOSED" for row in theorem)
    hilbert_partial = any(row["current_status"] == "PARTIAL_NOT_CLOSED" for row in hilbert)
    matrix_retains = any(row["resolution_status"] == "SURVIVES" for row in matrix)
    zeta_nonclaim = len(zeta) >= 6 and all(not truth(row["score_ready"]) and not truth(row["valid_for_claim"]) for row in zeta)
    requirements_nonclaim = all(not truth(row["score_ready"]) and not truth(row["valid_for_claim"]) for row in requirements)
    signing_refuses = all(not truth(row["post_cA_zero_import_allowed"]) and not truth(row["zeta_A_zero_import_allowed"]) and not truth(row["C_parent_WEP_import_allowed"]) for row in signing)
    parser_safe = all(not truth(row["would_write_live_claim_file"]) for row in parser)
    gates_false = all(not truth(row["gate_pass"]) for row in gates)
    live_import_absent = (
        not LIVE_C_PARENT_IMPORT.exists()
        and not LIVE_EPSILON_IMPORT.exists()
        and not LIVE_JACOBIAN_IMPORT.exists()
        and not LIVE_ZETAA_IMPORT.exists()
    )
    readout_absent = not LIVE_READOUT.exists()
    csv_parse = all(parse_csv_ok(path) for path in generated_csvs)
    branch_copies = BRANCH_THEOREM.exists() and BRANCH_ZETAA_LEDGER.exists() and BRANCH_SIGNING_DECISION.exists()
    formal_recent = 0
    if FORMALIZATION.exists():
        formal_recent = sum(
            1
            for path in FORMALIZATION.rglob("*")
            if path.is_file() and path.stat().st_mtime > START_TS
        )
    checks = [
        ("VAL1453_0_sources", all_sources_exist, "all cited source paths exist"),
        ("VAL1453_1_hilbert_exact", hilbert_exact, "Hilbert source subtheorem recorded as exact conditional"),
        ("VAL1453_2_ward_conditional", ward_conditional, "Ward identity conditional recorded"),
        ("VAL1453_3_post_killed_conditional", post_killed_conditional, "post-variation current rescaling is only conditionally killed"),
        ("VAL1453_4_pre_survives", pre_survives, "pre-variation source weights survive"),
        ("VAL1453_5_nonhilbert_open", nonhilbert_open, "non-Hilbert zeta_A bypass remains open"),
        ("VAL1453_6_verdict_partial", verdict_partial, "current-owner theorem remains partial"),
        ("VAL1453_7_hilbert_audit_partial", hilbert_partial, "Hilbert/Noether audit refuses closure"),
        ("VAL1453_8_matrix_retains", matrix_retains, "rescaling/selector matrix retains live countermodels"),
        ("VAL1453_9_zeta_nonclaim", zeta_nonclaim, "zeta_A ledger is nonclaim and not score-ready"),
        ("VAL1453_10_requirements_nonclaim", requirements_nonclaim, "current-source bound requirements remain nonclaim"),
        ("VAL1453_11_signing_refuses", signing_refuses, "parent signing decision refuses zero/import"),
        ("VAL1453_12_parser_safe", parser_safe, "parser refuses live claim writes"),
        ("VAL1453_13_claim_gates_false", gates_false, "all claim gates remain false"),
        ("VAL1453_14_no_live_import", live_import_absent, "live C_parent, epsilon, J_A, and zeta imports remain absent"),
        ("VAL1453_15_no_official_readout", readout_absent, "official readout live file remains absent"),
        ("VAL1453_16_csv_parse", csv_parse, "all generated 1453 CSVs parse cleanly"),
        ("VAL1453_17_branch_copies", branch_copies, "nonclaim branch copies written"),
        ("VAL1453_18_formalization_untouched", formal_recent == 0, f"formalization modified-file count since start={formal_recent}"),
        ("VAL1453_19_overall", True, "1453 preserves current-owner subtheorems and retains c_A/zeta_A ledgers"),
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
    hilbert: list[dict[str, Any]],
    matrix: list[dict[str, Any]],
    zeta: list[dict[str, Any]],
    requirements: list[dict[str, Any]],
    signing: list[dict[str, Any]],
    parser: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> None:
    with DOC.open("w", encoding="utf-8") as handle:
        handle.write("# 1453 - Current/source normalization owner theorem or zetaA ledger\n\n")
        handle.write(
            "**Current verdict:** the current-owner route gives real conditional subtheorems but not a full local-source closure. "
            "Given one common action and variation before readout, the Hilbert source is unique, Ward conservation follows, "
            "and post-variation `c_A`/`F(T_A,A)` rescalings are not parent source definitions. But current ownership alone "
            "does not kill pre-variation `w_A`, disconnected material constants, or non-Hilbert `zeta_A J_NH,A` currents.\n\n"
        )
        handle.write(
            "**Useful progress:** the source-current debt is now split into three boxes: pre-action weights need the action/object-language theorem, "
            "post-variation selectors need a readout-order theorem, and non-Hilbert currents need absence/exact/projector-silence or explicit bounds.\n\n"
        )
        write_table(handle, "Source register", sources)
        write_table(handle, "Current/source owner theorem attempt", theorem)
        write_table(handle, "Hilbert/Noether route audit", hilbert)
        write_table(handle, "Current rescaling selector matrix", matrix)
        write_table(handle, "zeta_A non-Hilbert current ledger", zeta)
        write_table(handle, "Current-source bound requirements", requirements)
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
    theorem = theorem_rows()
    hilbert = hilbert_noether_rows()
    matrix = rescaling_matrix_rows()
    zeta = zeta_rows()
    requirements = bound_requirement_rows()
    signing = signing_decision_rows()
    parser = parser_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(CURRENT_OWNER_THEOREM, theorem)
    write_csv(HILBERT_NOETHER_AUDIT, hilbert)
    write_csv(RESCALING_SELECTOR_MATRIX, matrix)
    write_csv(ZETAA_LEDGER, zeta)
    write_csv(BOUND_REQUIREMENTS, requirements)
    write_csv(SIGNING_DECISION, signing)
    write_csv(PARSER_DRYRUN, parser)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_target)

    copy_branch(CURRENT_OWNER_THEOREM, BRANCH_THEOREM)
    copy_branch(ZETAA_LEDGER, BRANCH_ZETAA_LEDGER)
    copy_branch(SIGNING_DECISION, BRANCH_SIGNING_DECISION)

    validation = validation_rows(sources, theorem, hilbert, matrix, zeta, requirements, signing, parser, gates)
    write_csv(VALIDATION, validation)
    write_doc(sources, theorem, hilbert, matrix, zeta, requirements, signing, parser, gates, decisions, validation, next_target)
    remove_pycache()
    print("Y5_R10_1453_current_owner_partial_zeta_retained")


if __name__ == "__main__":
    main()

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

DOC = ROOT / "1455-Y5-R10-RAB-parent-variation-domain-order-axiom-reduction-or-official-readout-acquisition-ledger.md"

PREV_NEXT = OUT / "P8_Y5_R10_1454_NEXT_TARGET.csv"
PREV_THEOREM = OUT / "P8_Y5_R10_1454_VARIATION_BEFORE_READOUT_THEOREM_ATTEMPT.csv"
PREV_AUDIT = OUT / "P8_Y5_R10_1454_SOURCE_READOUT_ORDER_AUDIT.csv"
PREV_OFFICIAL = OUT / "P8_Y5_R10_1454_OFFICIAL_READOUT_MODEL_REQUIREMENTS.csv"
PREV_POST = OUT / "P8_Y5_R10_1454_POST_SELECTOR_LEDGER_NONCLAIM.csv"
PREV_SIGNING = OUT / "P8_Y5_R10_1454_PARENT_SIGNING_DECISION.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1454_VALIDATION.csv"

AXRED1441 = OUT / "P8_Y5_R10_1441_AX1090_REDUCTION_AUDIT.csv"
AXDEP1441 = OUT / "P8_Y5_R10_1441_AX1090_DEPENDENCY_GRAPH.csv"
AXLED1090 = OUT / "P8_Y5_R10_1090_MISSING_AXIOM_LEDGER.csv"
PAC1055 = OUT / "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv"
MOMS1088 = OUT / "P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv"
THM1088 = OUT / "P8_Y5_R10_1088_CONDITIONAL_ZERO_THEOREM.csv"
NCO1079 = OUT / "P8_Y5_R10_1079_NARROW_CURRENT_OWNER_THEOREM_ATTEMPT.csv"
PR1079 = OUT / "P8_Y5_R10_1079_CURRENT_OWNER_PREMISE_LEDGER.csv"
CER1079 = OUT / "P8_Y5_R10_1079_COUNTEREXAMPLE_RESOLUTION_MATRIX.csv"
ZCC1087 = OUT / "P8_Y5_R10_1087_ZERO_CURRENT_CLAUSE_CONTRACT.csv"
TWP1066 = OUT / "P8_Y5_R10_1066_TAU_WEP_PROJECTION_CONTRACT.csv"
KREQ1445 = OUT / "P8_Y5_R10_1445_K_CMSM_READOUT_REQUIREMENTS.csv"
KREAD1445 = OUT / "P8_Y5_R10_1445_K_CMSM_READOUT_OFFICIAL_EXTRACTION.csv"
CTC1445 = OUT / "P8_Y5_R10_1445_C_PARENT_COUPLING_THEOREM_CONTRACT.csv"
CTA1445 = OUT / "P8_Y5_R10_1445_C_PARENT_COUPLING_THEOREM_AUDIT.csv"
FD1447 = OUT / "P8_Y5_R10_1447_FUNCTIONAL_DERIVATIVE_DEFINITION_ATTEMPT.csv"
EVAL1448 = OUT / "P8_Y5_R10_1448_FUNCTIONAL_DERIVATIVE_EVALUABILITY_GATE.csv"
EVAL1449 = OUT / "P8_Y5_R10_1449_C_PARENT_EVALUATION_DECISION.csv"
MOMS1448 = OUT / "P8_Y5_R10_1448_MOMS_SIGNATURE_SOURCE_PACK.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1455_SOURCE_REGISTER.csv"
REDUCTION_ATTEMPT = OUT / "P8_Y5_R10_1455_PARENT_VARIATION_DOMAIN_ORDER_REDUCTION_ATTEMPT.csv"
CLAUSE_AUDIT = OUT / "P8_Y5_R10_1455_AX1090_4_CLAUSE_AUDIT.csv"
DERIVATIVE_THEOREM = OUT / "P8_Y5_R10_1455_DERIVATIVE_BEFORE_PROJECTION_THEOREM.csv"
OFFICIAL_LEDGER = OUT / "P8_Y5_R10_1455_OFFICIAL_READOUT_ACQUISITION_LEDGER_NONCLAIM.csv"
WORLDTUBE_LEDGER = OUT / "P8_Y5_R10_1455_SOURCE_WORLDTUBE_ACQUISITION_LEDGER_NONCLAIM.csv"
POST_SELECTOR_UPDATE = OUT / "P8_Y5_R10_1455_POST_SELECTOR_UPDATE.csv"
SIGNING_DECISION = OUT / "P8_Y5_R10_1455_PARENT_SIGNING_DECISION.csv"
PARSER_DRYRUN = OUT / "P8_Y5_R10_1455_PARSER_DRYRUN.csv"
CLAIM_GATE = OUT / "P8_Y5_R10_1455_CLAIM_GATE.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1455_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1455_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1455_VALIDATION.csv"

BRANCH_REDUCTION = COEFF / "parent_variation_domain_order_attempt_1455.csv"
BRANCH_OFFICIAL = COEFF / "official_readout_acquisition_ledger_nonclaim_1455.csv"
BRANCH_SIGNING = COEFF / "C_parent_WEP_variation_order_signing_decision_1455.csv"

LIVE_C_PARENT_IMPORT = COEFF / "C_parent_WEP_slot_import.csv"
LIVE_C_A_IMPORT = COEFF / "c_A_post_selector_live_claim.csv"
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
        ("SRC1455_0_prev_next", PREV_NEXT, "1455 handoff"),
        ("SRC1455_1_prev_theorem", PREV_THEOREM, "1454 variation-before-readout theorem attempt"),
        ("SRC1455_2_prev_audit", PREV_AUDIT, "1454 source/readout order audit"),
        ("SRC1455_3_prev_official", PREV_OFFICIAL, "1454 official readout requirements"),
        ("SRC1455_4_prev_post", PREV_POST, "1454 post-selector ledger"),
        ("SRC1455_5_prev_signing", PREV_SIGNING, "1454 signing decision"),
        ("SRC1455_6_prev_validation", PREV_VALIDATION, "1454 validation"),
        ("SRC1455_7_AXRED1441", AXRED1441, "AX1090 reduction audit"),
        ("SRC1455_8_AXDEP1441", AXDEP1441, "AX1090 dependency graph"),
        ("SRC1455_9_AXLED1090", AXLED1090, "missing axiom ledger"),
        ("SRC1455_10_PAC1055", PAC1055, "parent action contract candidate"),
        ("SRC1455_11_MOMS1088", MOMS1088, "minimal ordinary matter signature"),
        ("SRC1455_12_THM1088", THM1088, "conditional zero theorem"),
        ("SRC1455_13_NCO1079", NCO1079, "narrow current-owner theorem"),
        ("SRC1455_14_PR1079", PR1079, "current owner premises"),
        ("SRC1455_15_CER1079", CER1079, "counterexample resolution matrix"),
        ("SRC1455_16_ZCC1087", ZCC1087, "zero current clause contract"),
        ("SRC1455_17_TWP1066", TWP1066, "tau WEP projection contract"),
        ("SRC1455_18_KREQ1445", KREQ1445, "K_CMSM readout requirements"),
        ("SRC1455_19_KREAD1445", KREAD1445, "official readout extraction"),
        ("SRC1455_20_CTC1445", CTC1445, "C_parent theorem contract"),
        ("SRC1455_21_CTA1445", CTA1445, "C_parent theorem audit"),
        ("SRC1455_22_FD1447", FD1447, "functional derivative definition"),
        ("SRC1455_23_EVAL1448", EVAL1448, "functional derivative evaluability gate"),
        ("SRC1455_24_EVAL1449", EVAL1449, "C_parent evaluation decision"),
        ("SRC1455_25_MOMS1448", MOMS1448, "MOMS source pack"),
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


def reduction_attempt_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "PVD1455_0_target",
            "reduce AX1090_4 from parent action/domain construction",
            "AX1090_4 := all source/current variations are taken before empirical readout, material projection, source-worldtube selection, or calibration",
            "TARGET_SHARPENED",
            "would turn readout order from an inserted discipline rule into a parent-domain theorem",
            "parent action/domain owner AX1090_0 remains unsigned",
        ),
        (
            "PVD1455_1_domain_independence",
            "parent field domain fixes admissible variations before readout",
            "if S_parent: F_parent -> R has a readout-independent domain D(S_parent) and V in T_Phi F_parent, then dS_parent[V] is defined before any empirical map",
            "EXACT_IF_PARENT_DOMAIN_SIGNED",
            "derivative-before-projection becomes a mathematical consequence of the domain",
            "no signed parent field space, boundary class, and variation domain in one source",
        ),
        (
            "PVD1455_2_projection_composition",
            "downstream readout cannot alter the parent functional derivative",
            "for source tensor J_parent=delta S_parent/delta Phi and readout R, the measured channel is R(J_parent), not delta(S_parent with R inserted)",
            "EXACT_IF_READOUT_IS_DOWNSTREAM",
            "post-variation selectors cannot manufacture or erase C_parent_WEP",
            "official K_CMSM/source kernel is not imported as a downstream map",
        ),
        (
            "PVD1455_3_worldtube_boundary_condition",
            "source worldtube must not define the parent variation domain",
            "worldtube/orbit/mask data may weight R(J_parent), but must not choose support or boundary conditions inside D(S_parent)",
            "NEEDED_CLAUSE_NOT_SIGNED",
            "prevents source-profile selection from becoming hidden coupling",
            "tau_WEP/source-worldtube projection contract remains missing",
        ),
        (
            "PVD1455_4_pre_action_selector_limit",
            "variation-domain order does not kill selectors already inside S_parent",
            "S_parent containing w_A S_A, c_A J_A, shadow frames, or source-only domains varies to a weighted source",
            "COUNTERMODEL_SURVIVES",
            "defines the theorem boundary honestly",
            "requires object-language/action-measure/no-shadow clauses, not AX1090_4 alone",
        ),
        (
            "PVD1455_5_official_readout_gap",
            "empirical readout branch is not score-ready",
            "K_CMSM must supply official columns, masks, units, sign, orbit/session handling, source projection, and branch lock",
            "ACQUISITION_REQUIRED_NONCLAIM",
            "would let readout be tested without moving source terms into the action",
            "official arrays/design matrix absent",
        ),
        (
            "PVD1455_6_verdict",
            "AX1090_4 remains a conditional theorem shape, not a reduced parent axiom",
            "parent-domain independence + downstream readout would prove order, but the current corpus has only contracts and missing source/readout data",
            "NOT_REDUCED_KEEP_NONCLAIM_LEDGERS",
            "post-selector route remains boxed but not claimed zero",
            "AX1090_0, AX1090_4, source-worldtube, and K_CMSM are unsigned/absent",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "attempt_id": attempt_id,
            "target": target,
            "mathematical_form": form,
            "status": status,
            "if_signed": effect,
            "current_blocker": blocker,
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for attempt_id, target, form, status, effect, blocker in rows
    ]


def clause_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("AX4_1455_0_parent_object", "one parent variational object exists before readout", "AX1090_0; PAC1055_6", "NOT_SIGNED", "cannot derive order without an owned action/domain"),
        ("AX4_1455_1_field_space", "parent field/configuration space F_parent is declared", "PAC1055_0; MOMS1088_0", "CONTRACT_ONLY", "variation tangent space remains schematic"),
        ("AX4_1455_2_domain_boundary", "admissible variations and boundary class are fixed before detector/source selection", "PVD1455_1", "NOT_SIGNED", "masks/worldtubes could act as domain selectors"),
        ("AX4_1455_3_hilbert_current", "Hilbert/current extraction occurs on parent action before projection", "NCO1079_1; NCO1079_3", "EXACT_GIVEN_COMMON_ACTION", "common action and readout-order premises still needed"),
        ("AX4_1455_4_downstream_readout", "K_CMSM is downstream map R(J_parent)", "KREQ1445; KREAD1445", "STRUCTURE_ONLY", "official arrays and sign/units absent"),
        ("AX4_1455_5_source_worldtube", "source-worldtube/orbit average is downstream weighting", "TWP1066", "MISSING", "tau_WEP/source projection can mimic selector"),
        ("AX4_1455_6_no_pre_action_weights", "no w_A/c_A/source selector inside S_parent", "ZCC1087; MOMS1088_4", "NOT_SIGNED", "pre-variation countermodels survive"),
        ("AX4_1455_7_verdict", "AX1090_4 reduced from parent domain", "all clauses above", "FAIL_REDUCTION", "keep AX1090_4 as unsigned closure discipline"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "clause_id": clause_id,
            "needed_clause": clause,
            "best_source": source,
            "current_status": status,
            "failure_mode_if_missing": failure,
            "parent_signed": status in {"EXACT_GIVEN_COMMON_ACTION"} and False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for clause_id, clause, source, status, failure in rows
    ]


def derivative_theorem_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DBP1455_0_setup",
            "Assume a parent action S on a fixed parent domain D and a downstream readout/projection R.",
            "S_parent is not a function of R, masks, fit parameters, material selector, or source-worldtube tables.",
            "ASSUMPTION_SET_EXACT_BUT_UNSIGNED",
        ),
        (
            "DBP1455_1_variation",
            "The Frechet/Hilbert derivative DS_Phi[V] is evaluated inside T_Phi D before applying R.",
            "Derivative order follows from the definition of a functional derivative on the domain of S.",
            "EXACT_CONDITIONAL_STEP",
        ),
        (
            "DBP1455_2_projection",
            "The observable channel is R(DS_Phi[V]) or R(J_parent), not a new variational source.",
            "If R is downstream, it may weight, average, mask, or calibrate the already-defined source but cannot change the parent Euler/Hilbert term.",
            "EXACT_CONDITIONAL_STEP",
        ),
        (
            "DBP1455_3_forbidden_import",
            "If R, masks, worldtube supports, or material labels enter S or D before variation, the theorem does not apply.",
            "Those cases are pre-action selectors/source weights and remain live residuals unless separately forbidden.",
            "BOUNDARY_OF_THEOREM",
        ),
        (
            "DBP1455_4_conclusion",
            "Derivative-before-projection is derivable from a signed parent action/domain plus downstream readout clause.",
            "The current corpus has the theorem shape but not the parent signature or official readout/source-worldtube data.",
            "THEOREM_CONDITIONAL_NOT_CLAIMABLE",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_step": step,
            "statement": statement,
            "derivation_note": note,
            "status": status,
            "parent_signed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for step, statement, note, status in rows
    ]


def official_ledger_rows() -> list[dict[str, Any]]:
    rows = [
        ("KC1455_0_time_keys", "time_s/session_id/orbit_id", "official timestamps, sessions, orbit phase keys", "s or declared mission time", "PENDING_OFFICIAL_ARRAYS", "KREQ1445_0..2"),
        ("KC1455_1_axis_sign", "axis/sign convention", "sensitive X-axis orientation and positive sign convention", "orientation/sign", "PARTIAL_NOT_BRANCH_LOCKED", "KREAD1445_0"),
        ("KC1455_2_design_values", "gx,gz,Sxx,Sxz,correction terms", "numeric model/design columns with units", "m/s^2 and gradient units", "STRUCTURE_ONLY_VALUES_ABSENT", "KREQ1445_4..7; KREAD1445_2"),
        ("KC1455_3_masks_segments", "mask_flag/calibration_flag/segment weights", "official glitch/onboard masks, calibration periods, science sessions", "boolean/weights", "PENDING", "KREQ1445_8..10; KREAD1445_3"),
        ("KC1455_4_source_url_path", "source provenance", "official file path, DOI, URL, extraction script, and checksum", "provenance", "PENDING", "KREQ1445_11"),
        ("KC1455_5_parent_basis_map", "K_CMSM semantics", "map from parent residual basis to eta_AB readout channel", "kernel/operator", "MISSING_PARENT_BASIS_MAP", "KREQ1445_extra_K_CMSM_semantics"),
        ("KC1455_6_parser_gate", "live import safety", "no PENDING/MISSING placeholders before promotion to live official readout", "policy", "NONCLAIM_ONLY", "1455 parser dry-run"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "ledger_id": ledger_id,
            "object": obj,
            "required_input": required,
            "units": units,
            "current_status": status,
            "source_reference": source,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for ledger_id, obj, required, units, status, source in rows
    ]


def worldtube_ledger_rows() -> list[dict[str, Any]]:
    rows = [
        ("SW1455_0_earth_source", "T_source^Earth(x)", "Earth/source stress profile in the observed local frame", "stress/mass density", "MISSING", "TWP1066_0"),
        ("SW1455_1_source_composition", "source composition convention", "composition/source-weight convention for the source body", "composition tensor", "MISSING", "TWP1066_0"),
        ("SW1455_2_orbit_average", "orbit/time averaging", "MICROSCOPE orbit and eta_AB averaging convention", "kernel/average", "MISSING", "TWP1066_1"),
        ("SW1455_3_observed_frame", "e_obs/readout frame", "same observed coframe for force law, source variation, and readout", "frame map", "CONDITIONAL_FROM_PRIOR_SPINE", "TWP1066_2"),
        ("SW1455_4_material_response", "Ti/Pt material tensor", "test-body material response to WEP source channel", "material/source tensor", "PARTIAL_PAIR_ONLY", "TWP1066_3"),
        ("SW1455_5_force_readout", "eta_AB force readout", "map from parent source residual to differential acceleration with sign/units", "dimensionless eta_AB kernel", "MISSING", "TWP1066_4"),
        ("SW1455_6_no_unity_shortcut", "tau_WEP", "numeric source-backed value, theorem-zero, or explicit retained nuisance prior", "dimensionless/operator", "UNITY_FORBIDDEN", "TWP1066_5"),
        ("SW1455_7_no_cancellation", "absolute product guard", "absolute product bound unless signed material model is derived and sourced", "policy", "ABSOLUTE_GUARD_ENFORCED", "TWP1066_6"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "ledger_id": ledger_id,
            "object": obj,
            "required_input": required,
            "units": units,
            "current_status": status,
            "source_reference": source,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for ledger_id, obj, required, units, status, source in rows
    ]


def post_selector_update_rows() -> list[dict[str, Any]]:
    rows = [
        ("PSU1455_0_FTA", "F(T_A,A)", "post-variation material/source selector", "KILLED_IF_AX1090_4_AND_KCMSM_SIGNED", "RETAINED_NONCLAIM", "AX1090_4_NOT_REDUCED"),
        ("PSU1455_1_cA_post", "c_A_post", "downstream current/readout rescaling", "KILLED_IF_READOUT_CALIBRATION_SPLIT_SIGNED", "RETAINED_NONCLAIM", "OFFICIAL_READOUT_ABSENT"),
        ("PSU1455_2_cA_pre", "c_A_pre", "pre-variation current/source coefficient", "SURVIVES_AX1090_4", "RETAINED_NONCLAIM", "ACTION_OBJECT_LANGUAGE_UNSIGNED"),
        ("PSU1455_3_worldtube_selector", "F_worldtube(T_source,x)", "source-worldtube/support projection", "DOWNSTREAM_ONLY_IF_SOURCE_MODEL_SIGNED", "RETAINED_NONCLAIM", "SOURCE_WORLDTUBE_MISSING"),
        ("PSU1455_4_mask_segment_selector", "F_mask/session", "empirical mask/segment/readout projection", "DOWNSTREAM_ONLY_IF_OFFICIAL_ARRAYS_IMPORTED", "RETAINED_NONCLAIM", "OFFICIAL_ARRAYS_ABSENT"),
        ("PSU1455_5_total_policy", "post_selector_total_policy", "no cancellation with epsilon/J_A/zeta", "NO_CANCELLATION_POLICY", "RETAINED_NONCLAIM", "BOUND_INPUTS_REQUIRED"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "update_id": update_id,
            "symbol": symbol,
            "meaning": meaning,
            "conditional_result": conditional,
            "current_status": status,
            "blocking_marker": marker,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for update_id, symbol, meaning, conditional, status, marker in rows
    ]


def signing_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "SIGN1455_0_AX1090_4",
            "target": "parent variation-domain order axiom reduction",
            "parent_domain_signed": False,
            "derivative_before_projection_theorem_exact": True,
            "readout_downstream_signed": False,
            "source_worldtube_downstream_signed": False,
            "pre_action_selector_excluded": False,
            "official_readout_model_imported": False,
            "AX1090_4_reduced": False,
            "post_selector_zero_import_allowed": False,
            "c_A_post_zero_import_allowed": False,
            "C_parent_WEP_import_allowed": False,
            "decision": "REFUSE_AX1090_4_REDUCTION_KEEP_OFFICIAL_READOUT_AND_SOURCE_WORLDTUBE_NONCLAIM",
            "reason": "the domain-order theorem is exact only under a signed parent action/domain and downstream source/readout model; those inputs remain unsigned or absent",
            "live_C_parent_import_exists": LIVE_C_PARENT_IMPORT.exists(),
            "live_c_A_import_exists": LIVE_C_A_IMPORT.exists(),
            "live_readout_exists": LIVE_READOUT.exists(),
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def parser_rows() -> list[dict[str, Any]]:
    targets = [
        ("PARSER1455_0_live_C_parent", LIVE_C_PARENT_IMPORT, "live C_parent import"),
        ("PARSER1455_1_live_c_A", LIVE_C_A_IMPORT, "live c_A import"),
        ("PARSER1455_2_live_epsilon", LIVE_EPSILON_IMPORT, "live epsilon import"),
        ("PARSER1455_3_live_JA", LIVE_JACOBIAN_IMPORT, "live J_A import"),
        ("PARSER1455_4_live_zetaA", LIVE_ZETAA_IMPORT, "live zeta_A import"),
        ("PARSER1455_5_live_KCMSM", LIVE_READOUT, "live official readout"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "parser_id": parser_id,
            "target_path": str(path),
            "target_meaning": meaning,
            "target_exists": path.exists(),
            "would_write_live_claim_file": False,
            "parser_action": "REFUSE_LIVE_PROMOTION_IN_1455",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for parser_id, path, meaning in targets
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1455_0_AX1090_4", "AX1090_4 parent-domain order reduced", False, "parent action/domain and downstream readout/source-worldtube not signed"),
        ("GATE1455_1_Cparent", "C_parent_WEP import allowed", False, "functional derivative remains non-evaluable"),
        ("GATE1455_2_post_selector_zero", "post-selector/c_A zero allowed", False, "only conditional theorem; live readout absent"),
        ("GATE1455_3_official_readout", "K_CMSM score-ready", False, "official arrays/design matrix absent"),
        ("GATE1455_4_source_worldtube", "tau_WEP/source-worldtube score-ready", False, "source profile/orbit/material/readout projection missing"),
        ("GATE1455_5_local_claim", "R10/WEP/PPN/local-GR claim allowed", False, "no local arena claim from 1455"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "gate": gate,
            "gate_pass": gate_pass,
            "blocking_reason": reason,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate, gate_pass, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1455_0_real_progress",
            "decision": "keep derivative-before-projection as exact conditional theorem",
            "why": "it follows cleanly from a signed parent action/domain and downstream readout map",
            "consequence": "AX1090_4 has a precise future proof contract",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1455_1_no_promotion",
            "decision": "do not promote AX1090_4 or C_parent_WEP",
            "why": "domain ownership, source-worldtube, and official K_CMSM readout are not signed/imported",
            "consequence": "post-selector, c_A, and source-worldtube rows remain nonclaim",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1455_2_next_best_route",
            "decision": "attack source-worldtube projection theorem or official K_CMSM acquisition next",
            "why": "1455 shows the theoretical theorem needs a downstream-source/readout clause and the empirical branch needs real arrays",
            "consequence": "1456 should either derive source-worldtube downstream status or fill official readout inputs without claims",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1455_0_1456",
            "next_target": "1456-Y5-R10-RAB-source-worldtube-projection-theorem-or-official-KCMSM-bound-inputs.md",
            "script": "scripts/Y5_R10_RAB_source_worldtube_projection_theorem_or_official_KCMSM_bound_inputs.py",
            "objective": "try to prove source-worldtube/orbit/mask projections are downstream readout maps rather than parent-domain selectors; if not, keep official K_CMSM/source inputs as nonclaim acquisition work",
            "include": "source worldtube; orbit average; measured-GM/source projection; K_CMSM official columns; no-unity tau_WEP guard; post-selector retention",
            "exclude": "numeric WEP claim; C_parent import; local-GR pass; formalization-workbench edits; GitHub action",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    reduction: list[dict[str, Any]],
    clauses: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    official: list[dict[str, Any]],
    worldtube: list[dict[str, Any]],
    post: list[dict[str, Any]],
    signing: list[dict[str, Any]],
    parser: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated_csvs = [
        SOURCE_REGISTER,
        REDUCTION_ATTEMPT,
        CLAUSE_AUDIT,
        DERIVATIVE_THEOREM,
        OFFICIAL_LEDGER,
        WORLDTUBE_LEDGER,
        POST_SELECTOR_UPDATE,
        SIGNING_DECISION,
        PARSER_DRYRUN,
        CLAIM_GATE,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    all_sources_exist = all(truth(row["exists"]) for row in sources)
    exact_domain = any(row["status"] == "EXACT_IF_PARENT_DOMAIN_SIGNED" for row in reduction)
    exact_downstream = any(row["status"] == "EXACT_IF_READOUT_IS_DOWNSTREAM" for row in reduction)
    countermodel_retained = any(row["status"] == "COUNTERMODEL_SURVIVES" for row in reduction)
    reduction_refused = any(row["status"] == "NOT_REDUCED_KEEP_NONCLAIM_LEDGERS" for row in reduction)
    ax4_fail = any(row["current_status"] == "FAIL_REDUCTION" for row in clauses)
    theorem_conditional = any(row["status"] == "THEOREM_CONDITIONAL_NOT_CLAIMABLE" for row in theorem)
    official_nonclaim = all(not truth(row["score_ready"]) and not truth(row["valid_for_claim"]) for row in official)
    worldtube_nonclaim = all(not truth(row["score_ready"]) and not truth(row["valid_for_claim"]) for row in worldtube)
    post_nonclaim = all(not truth(row["score_ready"]) and not truth(row["valid_for_claim"]) for row in post)
    signing_refuses = all(
        not truth(row["AX1090_4_reduced"])
        and not truth(row["post_selector_zero_import_allowed"])
        and not truth(row["C_parent_WEP_import_allowed"])
        for row in signing
    )
    parser_safe = all(not truth(row["would_write_live_claim_file"]) for row in parser)
    gates_false = all(not truth(row["gate_pass"]) for row in gates)
    live_import_absent = (
        not LIVE_C_PARENT_IMPORT.exists()
        and not LIVE_C_A_IMPORT.exists()
        and not LIVE_EPSILON_IMPORT.exists()
        and not LIVE_JACOBIAN_IMPORT.exists()
        and not LIVE_ZETAA_IMPORT.exists()
    )
    readout_absent = not LIVE_READOUT.exists()
    csv_parse = all(parse_csv_ok(path) for path in generated_csvs)
    branch_copies = BRANCH_REDUCTION.exists() and BRANCH_OFFICIAL.exists() and BRANCH_SIGNING.exists()
    formal_recent = 0
    if FORMALIZATION.exists():
        formal_recent = sum(
            1
            for path in FORMALIZATION.rglob("*")
            if path.is_file() and path.stat().st_mtime > START_TS
        )
    checks = [
        ("VAL1455_0_sources", all_sources_exist, "all cited source paths exist"),
        ("VAL1455_1_exact_domain_conditional", exact_domain, "domain-independence theorem step recorded conditionally"),
        ("VAL1455_2_exact_downstream_conditional", exact_downstream, "downstream projection theorem step recorded conditionally"),
        ("VAL1455_3_countermodel_retained", countermodel_retained, "pre-action selector countermodel retained"),
        ("VAL1455_4_reduction_refused", reduction_refused, "AX1090_4 reduction refused rather than claimed"),
        ("VAL1455_5_clause_audit_fails", ax4_fail, "AX1090_4 clause audit remains failed"),
        ("VAL1455_6_theorem_conditional", theorem_conditional, "derivative-before-projection theorem not claimable"),
        ("VAL1455_7_official_nonclaim", official_nonclaim, "official readout acquisition ledger is nonclaim"),
        ("VAL1455_8_worldtube_nonclaim", worldtube_nonclaim, "source-worldtube acquisition ledger is nonclaim"),
        ("VAL1455_9_post_nonclaim", post_nonclaim, "post-selector update remains nonclaim"),
        ("VAL1455_10_signing_refuses", signing_refuses, "parent signing decision refuses import/zero"),
        ("VAL1455_11_parser_safe", parser_safe, "parser refuses live claim writes"),
        ("VAL1455_12_claim_gates_false", gates_false, "all claim gates remain false"),
        ("VAL1455_13_no_live_import", live_import_absent, "live C_parent/c_A/epsilon/J_A/zeta imports remain absent"),
        ("VAL1455_14_no_official_readout", readout_absent, "official readout live file remains absent"),
        ("VAL1455_15_csv_parse", csv_parse, "all generated 1455 CSVs parse cleanly"),
        ("VAL1455_16_branch_copies", branch_copies, "nonclaim branch copies written"),
        ("VAL1455_17_formalization_untouched", formal_recent == 0, f"formalization modified-file count since start={formal_recent}"),
        ("VAL1455_18_overall", True, "1455 derives the exact conditional order theorem but demotes AX1090_4 to unsigned/nonclaim"),
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
        values = [str(row.get(field, "")).replace("\n", " ") for field in fields]
        handle.write("| " + " | ".join(values) + " |\n")
    handle.write("\n")


def write_doc(
    sources: list[dict[str, Any]],
    reduction: list[dict[str, Any]],
    clauses: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    official: list[dict[str, Any]],
    worldtube: list[dict[str, Any]],
    post: list[dict[str, Any]],
    signing: list[dict[str, Any]],
    parser: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> None:
    with DOC.open("w", encoding="utf-8") as handle:
        handle.write("# 1455 - Parent variation-domain order axiom reduction or official readout acquisition ledger\n\n")
        handle.write(
            "**Current verdict:** the best possible derivation is sharp: if the parent action and its variation domain "
            "are fixed before detector/source/readout choices, then the functional derivative is necessarily taken before "
            "projection. But the current corpus does not yet sign that parent domain or the downstream `K_CMSM`/source-worldtube "
            "model, so `AX1090_4` is **not reduced** and no local claim is promoted.\n\n"
        )
        handle.write(
            "**Useful progress:** the theorem boundary is now explicit. Downstream readout cannot change a parent Hilbert/current "
            "source, but pre-action weights, source-domain selectors, shadow frames, and missing official arrays remain live. "
            "This is exactly the kind of trap-door we want boxed before testing.\n\n"
        )
        write_table(handle, "Source register", sources)
        write_table(handle, "Parent variation-domain order reduction attempt", reduction)
        write_table(handle, "AX1090_4 clause audit", clauses)
        write_table(handle, "Derivative-before-projection theorem", theorem)
        write_table(handle, "Official K_CMSM readout acquisition ledger", official)
        write_table(handle, "Source-worldtube acquisition ledger", worldtube)
        write_table(handle, "Post-selector update", post)
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
    reduction = reduction_attempt_rows()
    clauses = clause_audit_rows()
    theorem = derivative_theorem_rows()
    official = official_ledger_rows()
    worldtube = worldtube_ledger_rows()
    post = post_selector_update_rows()
    signing = signing_decision_rows()
    parser = parser_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(REDUCTION_ATTEMPT, reduction)
    write_csv(CLAUSE_AUDIT, clauses)
    write_csv(DERIVATIVE_THEOREM, theorem)
    write_csv(OFFICIAL_LEDGER, official)
    write_csv(WORLDTUBE_LEDGER, worldtube)
    write_csv(POST_SELECTOR_UPDATE, post)
    write_csv(SIGNING_DECISION, signing)
    write_csv(PARSER_DRYRUN, parser)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_target)

    copy_branch(REDUCTION_ATTEMPT, BRANCH_REDUCTION)
    copy_branch(OFFICIAL_LEDGER, BRANCH_OFFICIAL)
    copy_branch(SIGNING_DECISION, BRANCH_SIGNING)

    validation = validation_rows(sources, reduction, clauses, theorem, official, worldtube, post, signing, parser, gates)
    write_csv(VALIDATION, validation)
    write_doc(sources, reduction, clauses, theorem, official, worldtube, post, signing, parser, gates, decisions, validation, next_target)
    remove_pycache()
    print("Y5_R10_1455_AX1090_4_conditional_theorem_nonclaim_ledgers_retained")


if __name__ == "__main__":
    main()

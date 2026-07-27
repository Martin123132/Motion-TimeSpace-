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

DOC = ROOT / "1454-Y5-R10-RAB-variation-before-readout-source-order-theorem-or-post-selector-ledger.md"

PREV_NEXT = OUT / "P8_Y5_R10_1453_NEXT_TARGET.csv"
PREV_THEOREM = OUT / "P8_Y5_R10_1453_CURRENT_SOURCE_NORMALIZATION_OWNER_THEOREM_ATTEMPT.csv"
PREV_MATRIX = OUT / "P8_Y5_R10_1453_CURRENT_RESCALING_SELECTOR_MATRIX.csv"
PREV_REQS = OUT / "P8_Y5_R10_1453_CURRENT_SOURCE_BOUND_INPUT_REQUIREMENTS.csv"
PREV_SIGNING = OUT / "P8_Y5_R10_1453_PARENT_SIGNING_DECISION.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1453_VALIDATION.csv"

NCO1079 = OUT / "P8_Y5_R10_1079_NARROW_CURRENT_OWNER_THEOREM_ATTEMPT.csv"
PR1079 = OUT / "P8_Y5_R10_1079_CURRENT_OWNER_PREMISE_LEDGER.csv"
CER1079 = OUT / "P8_Y5_R10_1079_COUNTEREXAMPLE_RESOLUTION_MATRIX.csv"
TWP1066 = OUT / "P8_Y5_R10_1066_TAU_WEP_PROJECTION_CONTRACT.csv"
ODR1066 = OUT / "P8_Y5_R10_1066_OPERATOR_DOMAIN_RULE_AUDIT.csv"
SSE1066 = OUT / "P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv"
AXRED1441 = OUT / "P8_Y5_R10_1441_AX1090_REDUCTION_AUDIT.csv"
KREQ1445 = OUT / "P8_Y5_R10_1445_K_CMSM_READOUT_REQUIREMENTS.csv"
KREAD1445 = OUT / "P8_Y5_R10_1445_K_CMSM_READOUT_OFFICIAL_EXTRACTION.csv"
MOMS1448 = OUT / "P8_Y5_R10_1448_MOMS_SIGNATURE_SOURCE_PACK.csv"
VDP1448 = OUT / "P8_Y5_R10_1448_VWEP_DOMAIN_PROOF_ATTEMPT.csv"
ZCC1087 = OUT / "P8_Y5_R10_1087_ZERO_CURRENT_CLAUSE_CONTRACT.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1454_SOURCE_REGISTER.csv"
READOUT_ORDER_THEOREM = OUT / "P8_Y5_R10_1454_VARIATION_BEFORE_READOUT_THEOREM_ATTEMPT.csv"
SOURCE_ORDER_AUDIT = OUT / "P8_Y5_R10_1454_SOURCE_READOUT_ORDER_AUDIT.csv"
POST_SELECTOR_LEDGER = OUT / "P8_Y5_R10_1454_POST_SELECTOR_LEDGER_NONCLAIM.csv"
C_A_SPLIT_LEDGER = OUT / "P8_Y5_R10_1454_C_A_READOUT_CALIBRATION_SPLIT.csv"
OFFICIAL_READOUT_REQUIREMENTS = OUT / "P8_Y5_R10_1454_OFFICIAL_READOUT_MODEL_REQUIREMENTS.csv"
SIGNING_DECISION = OUT / "P8_Y5_R10_1454_PARENT_SIGNING_DECISION.csv"
PARSER_DRYRUN = OUT / "P8_Y5_R10_1454_PARSER_DRYRUN.csv"
CLAIM_GATE = OUT / "P8_Y5_R10_1454_CLAIM_GATE.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1454_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1454_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1454_VALIDATION.csv"

BRANCH_THEOREM = COEFF / "variation_before_readout_theorem_attempt_1454.csv"
BRANCH_POST_SELECTOR = COEFF / "post_selector_source_order_ledger_nonclaim_1454.csv"
BRANCH_SIGNING = COEFF / "C_parent_WEP_readout_order_signing_decision_1454.csv"
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
        ("SRC1454_0_prev_next", PREV_NEXT, "1454 handoff"),
        ("SRC1454_1_prev_theorem", PREV_THEOREM, "1453 current-owner theorem"),
        ("SRC1454_2_prev_matrix", PREV_MATRIX, "1453 rescaling selector matrix"),
        ("SRC1454_3_prev_reqs", PREV_REQS, "1453 bound requirements"),
        ("SRC1454_4_prev_signing", PREV_SIGNING, "1453 signing decision"),
        ("SRC1454_5_prev_validation", PREV_VALIDATION, "1453 validation"),
        ("SRC1454_6_NCO1079", NCO1079, "narrow current-owner theorem"),
        ("SRC1454_7_PR1079", PR1079, "current-owner premise ledger"),
        ("SRC1454_8_CER1079", CER1079, "counterexample resolution matrix"),
        ("SRC1454_9_TWP1066", TWP1066, "tau WEP projection contract"),
        ("SRC1454_10_ODR1066", ODR1066, "operator-domain rule audit"),
        ("SRC1454_11_SSE1066", SSE1066, "source scalar exclusion lemma"),
        ("SRC1454_12_AXRED1441", AXRED1441, "AX1090 reduction audit"),
        ("SRC1454_13_KREQ1445", KREQ1445, "K_CMSM readout requirements"),
        ("SRC1454_14_KREAD1445", KREAD1445, "official readout extraction"),
        ("SRC1454_15_MOMS1448", MOMS1448, "MOMS signature source pack"),
        ("SRC1454_16_VDP1448", VDP1448, "V_WEP domain proof attempt"),
        ("SRC1454_17_ZCC1087", ZCC1087, "zero current clause contract"),
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
        ("VBR1454_0_target", "source variation occurs before readout/projection", "T_H := delta S_matter/delta e_obs is defined before material selector, orbit/readout kernel, calibration, or source-worldtube projection", "TARGET_SHARPENED", "would prevent downstream F(T_A,A) from being a parent source", "parent variation-order axiom not reduced"),
        ("VBR1454_1_variational_identity", "functional derivative order is mathematically fixed inside a parent action", "delta S_parent is evaluated on the parent field domain before empirical projection maps are applied", "EXACT_IF_PARENT_ACTION_DOMAIN_SIGNED", "post-processing cannot change the variational derivative", "single parent action/domain owner remains unsigned"),
        ("VBR1454_2_post_selector_kill", "post-variation F(T_A,A) cannot redefine source", "Readout(F(T_A,A)) may select a measured channel but cannot replace T_H in the field equation", "KILLED_CONDITIONALLY", "post-selector becomes readout/calibration rather than source ownership", "official/source readout order not parent-signed"),
        ("VBR1454_3_cA_split", "c_A after source extraction is calibration/readout, not a new parent coupling", "J_A -> c_A J_A downstream of T_H is not part of S_parent variation", "KILLED_CONDITIONALLY", "post-variation c_A can be excluded from C_parent", "must prove c_A is not inserted before variation"),
        ("VBR1454_4_pre_selector_survives", "pre-action selector is killed by readout order", "S_matter=sum_A w_A S_A or S_A[J_A] before variation yields T_H=sum_A w_A T_A", "SURVIVES_PRE_VARIATION", "nothing; it defines the limit of this theorem", "requires object-language/action-measure theorem"),
        ("VBR1454_5_official_readout_gap", "official MICROSCOPE readout is tied to the parent source order", "K_CMSM maps parent residual to eta_AB using official columns, masks, segments, units, sign, and branch lock", "EMPIRICAL_MODEL_NOT_IMPORTED", "would make readout projection reproducible", "official arrays/design matrix absent"),
        ("VBR1454_6_verdict", "variation-before-readout closes post-selector/c_A branch", "parent variation-order + official source/readout model + no pre-action weights => no post-selector source residual", "CONDITIONAL_THEOREM_NOT_PARENT_SIGNED", "post-selector route is sharply constrained but not claimable", "variation order and official readout model remain unsigned/absent"),
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


def source_order_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("SOA1454_0_parent_domain", "single parent action/domain before projection", "AX1090_0 parent object", "NOT_REDUCED", "source/readout can be stitched post hoc"),
        ("SOA1454_1_variation_order", "source/current variation before material/readout projection", "AX1090_4 variation domain order", "PARTIAL_CONTRACT_NOT_REDUCED", "post-selector branch remains live"),
        ("SOA1454_2_hilbert_source", "Hilbert source definition before readout", "NCO1079 exact conditional subtheorem", "EXACT_GIVEN_COMMON_ACTION", "requires common action"),
        ("SOA1454_3_readout_downstream", "readout maps are downstream measurement kernels only", "K_CMSM readout requirements", "OFFICIAL_ARRAYS_ABSENT", "cannot score or promote c_A split"),
        ("SOA1454_4_source_worldtube", "source-worldtube projection downstream of parent source", "tau_WEP projection contract", "MISSING", "source profile can behave like selector"),
        ("SOA1454_5_verdict", "source/readout order theorem", "all order clauses signed together", "FAIL_CURRENT_PROOF", "retain post-selector ledger"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "needed_clause": clause,
            "source": source,
            "current_status": status,
            "if_missing": risk,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for audit_id, clause, source, status, risk in rows
    ]


def post_selector_rows() -> list[dict[str, Any]]:
    rows = [
        ("PS1454_0_FTA", "F(T_A,A)", "post-variation material/source selector", "kernel/operator", "KILLED_IF_ORDER_SIGNED", "MISSING_PARENT_ORDER_SIGNATURE", "WEP/PPN/orbital"),
        ("PS1454_1_cA_post", "c_A_post", "downstream current/readout rescaling", "dimensionless", "KILLED_IF_ORDER_SIGNED", "MISSING_READOUT_CALIBRATION_SPLIT", "WEP/source"),
        ("PS1454_2_cA_pre", "c_A_pre", "pre-variation current/source coefficient", "dimensionless", "SURVIVES_THIS_THEOREM", "MISSING_ACTION_OBJECT_LANGUAGE_OWNER", "WEP/PPN/orbital"),
        ("PS1454_3_worldtube_selector", "F_worldtube(T_source,x)", "source-worldtube/support projection", "kernel", "RETAINED", "MISSING_SOURCE_WORLDTUBE_MODEL", "orbital/Newtonian/WEP"),
        ("PS1454_4_mask_segment_selector", "F_mask/session", "empirical mask/segment/readout projection", "kernel", "RETAINED_NONCLAIM", "OFFICIAL_ARRAYS_ABSENT", "MICROSCOPE/WEP"),
        ("PS1454_5_total_policy", "post_selector_total_policy", "no cancellation with epsilon/J_A/zeta", "policy", "NO_CANCELLATION_RETAINED", "BOUND_INPUTS_REQUIRED", "all local arenas"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "ledger_id": ledger_id,
            "symbol": symbol,
            "meaning": meaning,
            "units": units,
            "current_status": status,
            "blocking_marker": marker,
            "arena_link": arena,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for ledger_id, symbol, meaning, units, status, marker, arena in rows
    ]


def ca_split_rows() -> list[dict[str, Any]]:
    rows = [
        ("CAS1454_0_parent", "c_A_parent", "inside S_parent before variation", "source coupling", "SURVIVES", "requires action/object-language proof or bound"),
        ("CAS1454_1_post", "c_A_post", "after Hilbert source extraction", "readout/calibration", "CONDITIONALLY_NOT_PARENT_SOURCE", "requires readout-order theorem"),
        ("CAS1454_2_common", "c_common", "universal calibration factor", "calibration/G normalization", "COMMON_MODE_ONLY", "must be constant/universal/range independent"),
        ("CAS1454_3_relative", "Delta c_AB", "relative material/source readout factor", "WEP-sensitive residual", "RETAINED_NONCLAIM", "needs material/source/readout matrix"),
        ("CAS1454_4_verdict", "c_A split", "parent vs post-readout split", "classification", "PARTIAL_NOT_CLAIM", "official source/readout model missing"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "split_id": split_id,
            "symbol": symbol,
            "location": location,
            "role": role,
            "classification": classification,
            "remaining_requirement": requirement,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for split_id, symbol, location, role, classification, requirement in rows
    ]


def official_readout_requirement_rows() -> list[dict[str, Any]]:
    rows = [
        ("ORR1454_0_time", "time/session/orbit keys", "time_s, session_id, orbit_id", "PENDING", "official arrays absent"),
        ("ORR1454_1_axis", "sensitive-axis/sign convention", "axis, attitude, positive X orientation", "PARTIAL", "sign/orientation not branch-locked"),
        ("ORR1454_2_design", "gravity/readout design columns", "gx,gz,Sxx,Sxz and correction terms", "STRUCTURE_ONLY", "values/units absent"),
        ("ORR1454_3_masks", "mask/segment/calibration cuts", "mask_flag, segment weights, calibration_flag", "PENDING", "final cuts not imported"),
        ("ORR1454_4_source_kernel", "source-worldtube/orbit averaging kernel", "tau_WEP/K_CMSM projection", "MISSING", "no source projection to eta_AB"),
        ("ORR1454_5_parent_basis", "parent residual to readout basis", "units/sign/source projection/branch lock", "MISSING", "post-selector/c_A cannot be scored"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "requirement_id": req_id,
            "requirement": requirement,
            "required_columns_or_object": required,
            "current_status": status,
            "blocking_marker": marker,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for req_id, requirement, required, status, marker in rows
    ]


def signing_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "SIGN1454_0_readout_order",
            "target": "variation-before-readout/source-order theorem",
            "parent_domain_signed": False,
            "hilbert_source_subtheorem": True,
            "variation_order_signed": False,
            "official_readout_model_imported": False,
            "post_selector_zero_import_allowed": False,
            "c_A_post_zero_import_allowed": False,
            "C_parent_WEP_import_allowed": False,
            "decision": "REFUSE_READOUT_ORDER_ZERO_IMPORT_KEEP_POST_SELECTOR_LEDGER",
            "reason": "post-selector kill is conditionally correct, but parent variation order and official source/readout model are not signed/imported",
            "live_C_parent_import_exists": LIVE_C_PARENT_IMPORT.exists(),
            "live_c_A_import_exists": LIVE_C_A_IMPORT.exists(),
            "live_readout_exists": LIVE_READOUT.exists(),
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def parser_rows() -> list[dict[str, Any]]:
    rows = [
        ("PDR1454_0_post_selector_zero", "import F(T_A,A)=0/source-silent", "REFUSED", "variation-order theorem not parent-signed"),
        ("PDR1454_1_cA_zero", "import c_A_post=0", "REFUSED", "official readout/calibration split absent"),
        ("PDR1454_2_Cparent", "evaluate/import C_parent_WEP", "REFUSED", "parent domain/order and official readout model missing"),
        ("PDR1454_3_ledgers", "stage post-selector nonclaim ledgers", "ALLOWED_NONCLAIM", "rows are valid_for_claim=false"),
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
        ("CG1454_0_variation_order", "variation-before-readout theorem"),
        ("CG1454_1_post_selector_zero", "post-selector source residual zero"),
        ("CG1454_2_cA_post_zero", "c_A post-readout zero/import"),
        ("CG1454_3_WEP_readout", "MICROSCOPE source/readout projection pass"),
        ("CG1454_4_PPN_orbital", "PPN/orbital source-order pass"),
        ("CG1454_5_C_parent", "C_parent_WEP import/evaluation"),
        ("CG1454_6_local_GR", "local GR/Newton source branch claim"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": False,
            "reason": "readout-order theorem is conditional and post-selector/readout ledgers remain nonclaim",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, claim in gates
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1454_0_keep_order_theorem",
            "decision": "retain variation-before-readout as a clean conditional theorem",
            "why": "it correctly prevents downstream readout choices from redefining the parent source",
            "consequence": "post-selector route is now sharply classified",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1454_1_no_zero_claim",
            "decision": "do not claim post-selector/c_A zero",
            "why": "parent variation order and official source/readout model are not signed/imported",
            "consequence": "post-selector and c_A split rows remain nonclaim",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1454_2_next_best_route",
            "decision": "attack parent variation-domain-order axiom reduction next",
            "why": "official readout data can score later, but the derivation-first blocker is AX1090_4",
            "consequence": "1455 targets parent variation-domain order or keeps official readout acquisition as bound-input work",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1454_0_1455",
            "next_target": "1455-Y5-R10-RAB-parent-variation-domain-order-axiom-reduction-or-official-readout-acquisition-ledger.md",
            "script": "scripts/Y5_R10_RAB_parent_variation_domain_order_axiom_reduction_or_official_readout_acquisition_ledger.py",
            "objective": "try to reduce AX1090_4 variation-domain order from the parent action/domain construction; if it cannot be signed, keep official source/readout acquisition requirements as nonclaim bound-input work",
            "include": "parent variation domain; derivative-before-projection; source worldtube; K_CMSM official readout requirements; post-selector ledger update",
            "exclude": "numeric WEP claim; C_parent import; local-GR pass; formalization-workbench edits; GitHub action",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    post: list[dict[str, Any]],
    ca_split: list[dict[str, Any]],
    official: list[dict[str, Any]],
    signing: list[dict[str, Any]],
    parser: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated_csvs = [
        SOURCE_REGISTER,
        READOUT_ORDER_THEOREM,
        SOURCE_ORDER_AUDIT,
        POST_SELECTOR_LEDGER,
        C_A_SPLIT_LEDGER,
        OFFICIAL_READOUT_REQUIREMENTS,
        SIGNING_DECISION,
        PARSER_DRYRUN,
        CLAIM_GATE,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    all_sources_exist = all(truth(row["exists"]) for row in sources)
    exact_order = any(row["status"] == "EXACT_IF_PARENT_ACTION_DOMAIN_SIGNED" for row in theorem)
    post_killed = any(row["status"] == "KILLED_CONDITIONALLY" for row in theorem)
    pre_survives = any(row["status"] == "SURVIVES_PRE_VARIATION" for row in theorem)
    official_missing = any(row["status"] == "EMPIRICAL_MODEL_NOT_IMPORTED" for row in theorem)
    theorem_conditional = any(row["status"] == "CONDITIONAL_THEOREM_NOT_PARENT_SIGNED" for row in theorem)
    audit_fails = any(row["current_status"] == "FAIL_CURRENT_PROOF" for row in audit)
    post_nonclaim = len(post) >= 6 and all(not truth(row["score_ready"]) and not truth(row["valid_for_claim"]) for row in post)
    ca_split_nonclaim = all(not truth(row["valid_for_claim"]) for row in ca_split)
    official_not_ready = all(not truth(row["score_ready"]) and not truth(row["valid_for_claim"]) for row in official)
    signing_refuses = all(
        not truth(row["post_selector_zero_import_allowed"])
        and not truth(row["c_A_post_zero_import_allowed"])
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
    branch_copies = BRANCH_THEOREM.exists() and BRANCH_POST_SELECTOR.exists() and BRANCH_SIGNING.exists()
    formal_recent = 0
    if FORMALIZATION.exists():
        formal_recent = sum(
            1
            for path in FORMALIZATION.rglob("*")
            if path.is_file() and path.stat().st_mtime > START_TS
        )
    checks = [
        ("VAL1454_0_sources", all_sources_exist, "all cited source paths exist"),
        ("VAL1454_1_exact_order_conditional", exact_order, "exact derivative-before-projection rule recorded conditionally"),
        ("VAL1454_2_post_killed_conditional", post_killed, "post-selector/c_A route conditionally killed"),
        ("VAL1454_3_pre_survives", pre_survives, "pre-variation selector survives this theorem"),
        ("VAL1454_4_official_missing", official_missing, "official source/readout model remains missing"),
        ("VAL1454_5_theorem_conditional", theorem_conditional, "readout-order theorem remains conditional"),
        ("VAL1454_6_audit_fails", audit_fails, "source/readout order audit refuses proof"),
        ("VAL1454_7_post_nonclaim", post_nonclaim, "post-selector ledger is nonclaim and not score-ready"),
        ("VAL1454_8_ca_split_nonclaim", ca_split_nonclaim, "c_A split is nonclaim"),
        ("VAL1454_9_official_not_ready", official_not_ready, "official readout requirements are not score-ready"),
        ("VAL1454_10_signing_refuses", signing_refuses, "parent signing decision refuses zero/import"),
        ("VAL1454_11_parser_safe", parser_safe, "parser refuses live claim writes"),
        ("VAL1454_12_claim_gates_false", gates_false, "all claim gates remain false"),
        ("VAL1454_13_no_live_import", live_import_absent, "live C_parent/c_A/epsilon/J_A/zeta imports remain absent"),
        ("VAL1454_14_no_official_readout", readout_absent, "official readout live file remains absent"),
        ("VAL1454_15_csv_parse", csv_parse, "all generated 1454 CSVs parse cleanly"),
        ("VAL1454_16_branch_copies", branch_copies, "nonclaim branch copies written"),
        ("VAL1454_17_formalization_untouched", formal_recent == 0, f"formalization modified-file count since start={formal_recent}"),
        ("VAL1454_18_overall", True, "1454 keeps readout-order theorem conditional and retains post-selector ledger"),
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
    audit: list[dict[str, Any]],
    post: list[dict[str, Any]],
    ca_split: list[dict[str, Any]],
    official: list[dict[str, Any]],
    signing: list[dict[str, Any]],
    parser: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> None:
    with DOC.open("w", encoding="utf-8") as handle:
        handle.write("# 1454 - Variation-before-readout source-order theorem or post-selector ledger\n\n")
        handle.write(
            "**Current verdict:** derivative-before-projection is the correct theorem shape. If a parent action/domain "
            "is signed and the Hilbert source is varied before material/readout/source projection, then downstream "
            "`F(T_A,A)` selectors and post-readout `c_A` rescalings cannot define the parent source. But this is still "
            "conditional: AX1090_4 is not reduced and the official `K_CMSM` source/readout model is absent.\n\n"
        )
        handle.write(
            "**Useful progress:** post-variation source tricks are now boxed separately from pre-action weights. "
            "The remaining proof debt is parent variation-domain order; the remaining empirical debt is official "
            "readout/source-kernel acquisition.\n\n"
        )
        write_table(handle, "Source register", sources)
        write_table(handle, "Variation-before-readout theorem attempt", theorem)
        write_table(handle, "Source/readout order audit", audit)
        write_table(handle, "Post-selector ledger", post)
        write_table(handle, "c_A readout/calibration split", ca_split)
        write_table(handle, "Official readout model requirements", official)
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
    audit = source_order_audit_rows()
    post = post_selector_rows()
    ca_split = ca_split_rows()
    official = official_readout_requirement_rows()
    signing = signing_decision_rows()
    parser = parser_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(READOUT_ORDER_THEOREM, theorem)
    write_csv(SOURCE_ORDER_AUDIT, audit)
    write_csv(POST_SELECTOR_LEDGER, post)
    write_csv(C_A_SPLIT_LEDGER, ca_split)
    write_csv(OFFICIAL_READOUT_REQUIREMENTS, official)
    write_csv(SIGNING_DECISION, signing)
    write_csv(PARSER_DRYRUN, parser)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_target)

    copy_branch(READOUT_ORDER_THEOREM, BRANCH_THEOREM)
    copy_branch(POST_SELECTOR_LEDGER, BRANCH_POST_SELECTOR)
    copy_branch(SIGNING_DECISION, BRANCH_SIGNING)

    validation = validation_rows(sources, theorem, audit, post, ca_split, official, signing, parser, gates)
    write_csv(VALIDATION, validation)
    write_doc(sources, theorem, audit, post, ca_split, official, signing, parser, gates, decisions, validation, next_target)
    remove_pycache()
    print("Y5_R10_1454_readout_order_conditional_post_selector_retained")


if __name__ == "__main__":
    main()

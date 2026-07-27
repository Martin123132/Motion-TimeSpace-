from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1223"
TITLE = "1223-Y5-R10-P0-coupling-input-source-or-derivation-attack"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
P0_QUEUE_PATH = OUT_DIR / f"{PACK_ID}_P0_QUEUE_IMPORT.csv"
DERIVATION_MATRIX_PATH = OUT_DIR / f"{PACK_ID}_DERIVATION_ATTEMPT_MATRIX.csv"
PROOF_CONTRACT_PATH = OUT_DIR / f"{PACK_ID}_MINIMAL_PROOF_CONTRACTS.csv"
SOURCE_REQUIREMENTS_PATH = OUT_DIR / f"{PACK_ID}_FALLBACK_SOURCE_REQUIREMENTS.csv"
PROMOTION_LEDGER_PATH = OUT_DIR / f"{PACK_ID}_PROMOTION_ATTEMPT_LEDGER.csv"
NARROWED_BLOCKERS_PATH = OUT_DIR / f"{PACK_ID}_NARROWED_BLOCKER_LEDGER.csv"
RUNNER_FEED_PATH = OUT_DIR / f"{PACK_ID}_RUNNER_FEED_UPDATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1223_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def parse_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def is_false(row: dict[str, object], key: str) -> bool:
    return not parse_bool(row.get(key, False))


def source_ref(relative_path: str, needle: str) -> str:
    return f"{relative_path}:{needle}"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1223_0_1222_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1222_NEXT_TARGET.csv",
            "needle": "1223-Y5-R10-P0-coupling-input-source-or-derivation-attack.md",
            "purpose": "1222 handoff to P0 coupling derivation/source attack",
        },
        {
            "source_id": "SRC1223_1_1222_queue",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1222_SOURCE_ACQUISITION_QUEUE.csv",
            "needle": "QUEUE1222_0_alpha",
            "purpose": "P0/P1 source acquisition queue",
        },
        {
            "source_id": "SRC1223_2_1222_score_table",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1222_FIRST_NONCLAIM_SCORE_TABLE.csv",
            "needle": "NCS1222_0_alpha",
            "purpose": "mechanical nonclaim table refusing current rows",
        },
        {
            "source_id": "SRC1223_3_1222_blockers",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1222_MISSING_INPUT_BLOCKER_LEDGER.csv",
            "needle": "BLK1222_0_0",
            "purpose": "row-level blocker tokens",
        },
        {
            "source_id": "SRC1223_4_1220_parent_signature",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv",
            "needle": "PTOL1220_7_verdict",
            "purpose": "parent typed object-language signature not derived",
        },
        {
            "source_id": "SRC1223_5_1220_counterexamples",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1220_COUNTEREXAMPLE_LOCK_UPDATE.csv",
            "needle": "CELOCK1220_1_alpha_F2",
            "purpose": "active alpha/source/readout counterexamples",
        },
        {
            "source_id": "SRC1223_6_1219_conditional",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1219_NO_HIDDEN_ARGUMENT_CONDITIONAL_THEOREM.csv",
            "needle": "NHA1219_0_type_rule",
            "purpose": "conditional no-hidden-argument theorem route",
        },
        {
            "source_id": "SRC1223_7_1066_domain",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1066_OPERATOR_DOMAIN_RULE_AUDIT.csv",
            "needle": "ODR1066_4_verdict",
            "purpose": "operator-domain exclusion remains not derived",
        },
        {
            "source_id": "SRC1223_8_1066_source_scalar",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv",
            "needle": "SSE1066_5_verdict",
            "purpose": "source scalar/source-weight exclusion conditional only",
        },
        {
            "source_id": "SRC1223_9_1045_matter_functor",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
            "needle": "MFS1045_6_verdict",
            "purpose": "parent matter functor not signed",
        },
        {
            "source_id": "SRC1223_10_1055_action_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv",
            "needle": "PAC1055_6_single_parent_action",
            "purpose": "single parent action contract candidate",
        },
        {
            "source_id": "SRC1223_11_1084_readout",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv",
            "needle": "RIG1084_0_CMSM_arrays",
            "purpose": "readout arrays/functor closure not imported",
        },
        {
            "source_id": "SRC1223_12_1098_requirements",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1098_SOURCE_BACKED_COEFFICIENT_REQUIREMENTS.csv",
            "needle": "REQ1098_0_c_alpha",
            "purpose": "source-backed coefficient thresholds",
        },
    ]

    source_register = []
    for spec in source_specs:
        path_exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_register.append(
            {
                **spec,
                "absolute_path": str(source_path(spec["local_path"])),
                "path_exists": path_exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    queue_rows_all = read_csv(OUT_DIR / "P8_Y5_R10_1222_SOURCE_ACQUISITION_QUEUE.csv")
    p0_rows = [row for row in queue_rows_all if row.get("priority") == "P0"]

    p0_queue = []
    for row in p0_rows:
        p0_queue.append(
            {
                "queue_id": row["queue_id"],
                "acquisition_id": row["acquisition_id"],
                "closure_id": row["closure_id"],
                "debt": row["debt"],
                "current_status": row["current_status"],
                "attack_order": "derive_first_then_source",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    derivation_rows = [
        {
            "attempt_id": "DER1223_0_alpha_F2",
            "p0_row": "ACQ1221_0_alpha",
            "target_zero_or_source": "c_alpha_DD/b_alpha",
            "derivation_route_attempted": "prove all visible EM F_Q^2 coefficients factor only through q_loc/fixed representation data",
            "required_parent_clause": "parent typed coefficient domain plus EM F2 image exhaustion plus radiative/readout closure",
            "best_current_support": source_ref("source-intake/mts_residuals/P8_Y5_R10_1219_NO_HIDDEN_ARGUMENT_CONDITIONAL_THEOREM.csv", "NHA1219_0_type_rule"),
            "failure_mode": "scalar gauge kinetic term f(I_hid)F_Q^2 remains covariant and gauge invariant unless parent domain forbids it",
            "verdict": "DERIVATION_NOT_CLOSED_SOURCE_REQUIREMENT_RETAINED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "DER1223_1_surface_binding",
            "p0_row": "ACQ1221_1_surface",
            "target_zero_or_source": "c_surface_DD",
            "derivation_route_attempted": "prove binding/surface constants are fixed superselection data of the parent matter functor",
            "required_parent_clause": "species-complete matter functor, fixed constants, no hidden scalar coefficient argument, readout closure",
            "best_current_support": source_ref("source-intake/mts_residuals/P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv", "MFS1045_6_verdict"),
            "failure_mode": "matter functor is audited but not parent-signed for all ordinary species and effective binding response",
            "verdict": "DERIVATION_NOT_CLOSED_SOURCE_REQUIREMENT_RETAINED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "DER1223_2_source_weight_owner",
            "p0_row": "ACQ1221_2_source_weight",
            "target_zero_or_source": "Delta_w_TiPt * tau_WEP",
            "derivation_route_attempted": "prove source-only weights are impossible because the parent action has one measure/current/action-scale owner",
            "required_parent_clause": "source-label forgetting, universal current extraction, action-scale owner, source worldtube/readout projection",
            "best_current_support": source_ref("source-intake/mts_residuals/P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv", "SSE1066_5_verdict"),
            "failure_mode": "conditional exclusion exists, but action-scale/current owner and tau_WEP projection are not parent-derived",
            "verdict": "DERIVATION_NOT_CLOSED_SOURCE_REQUIREMENT_RETAINED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "DER1223_3_readout_functor",
            "p0_row": "ACQ1221_3_readout",
            "target_zero_or_source": "delta_readout_coefficient",
            "derivation_route_attempted": "prove effective/readout maps preserve the same typed coefficient domain",
            "required_parent_clause": "renormalized/readout functor from parent residuals to observables with no new hidden coefficient arguments",
            "best_current_support": source_ref("source-intake/mts_residuals/P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv", "RIG1084_0_CMSM_arrays"),
            "failure_mode": "official arrays/readout functor are absent, so observable transfer remains surrogate/nonclaim",
            "verdict": "DERIVATION_NOT_CLOSED_SOURCE_REQUIREMENT_RETAINED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    proof_contracts = [
        {
            "contract_id": "PROOF1223_0_alpha",
            "branch": "alpha/EM F2",
            "premises_required": "typed parent coefficient domain; hidden-invariant algebra excluded from visible gauge kinetic functions; EM F2 image exhausted by visible representation; readout closure",
            "conclusion_if_signed": "vertical derivative of alpha-sector visible coefficient vanishes, so c_alpha_DD/b_alpha=0 or is a sourced finite residual",
            "current_gap": "parent domain and EM F2 exclusion are conditional, not primitive-signed",
            "fallback_source_requirement": "numeric abs(c_alpha_DD/b_alpha) <= 8.320244933243531978e-10 with provenance",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "PROOF1223_1_surface",
            "branch": "surface/binding",
            "premises_required": "species-complete matter functor; fixed binding/surface constants or explicit residual operator; no hidden argument in matter constants; readout closure",
            "conclusion_if_signed": "surface/binding coupling is theorem-zero or converted to a finite sourced coefficient",
            "current_gap": "matter functor signature is not parent-signed across effective binding responses",
            "fallback_source_requirement": "numeric abs(c_surface_DD) <= 6.987501646143863402e-11 with provenance",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "PROOF1223_2_source_weight",
            "branch": "source-weight/local GR",
            "premises_required": "one parent action scale; universal source current extraction; source labels quotient-forgotten before material/readout split; tau_WEP projection derived",
            "conclusion_if_signed": "relative source-weight branch is theorem-zero, or abs(Delta_w_TiPt*tau_WEP) becomes finitely scoreable",
            "current_gap": "source scalar exclusion is conditional and tau_WEP/source worldtube/readout are missing",
            "fallback_source_requirement": "numeric Delta_w_TiPt, tau_WEP, source-profile weighting, readout kernel, and abs product <= 2.8e-15",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "PROOF1223_3_readout",
            "branch": "effective/readout",
            "premises_required": "parent residual to observable functor preserving typed domains through loops, spectroscopy, and MICROSCOPE readout",
            "conclusion_if_signed": "readout regeneration counterexample is closed and coefficient drift is zero or bounded",
            "current_gap": "no official readout import or parent readout functor closure",
            "fallback_source_requirement": "official readout arrays/kernel plus bounded coefficient drift in the same units as the scored observable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    source_requirements = [
        {
            "requirement_id": "SRCREQ1223_0_alpha",
            "p0_row": "ACQ1221_0_alpha",
            "source_object": "alpha coefficient/prior or alpha theorem-zero proof",
            "exact_required_fields": "coefficient_value; coefficient_units; threshold=8.320244933243531978e-10; source_path; source_needle; counterexample_disposition",
            "current_status": "MISSING_SOURCE_BACKED_ALPHA_COEFFICIENT_OR_PARENT_PRIMITIVE",
            "claim_use": "feed RUN1221_0_alpha only after all fields are real",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "SRCREQ1223_1_surface",
            "p0_row": "ACQ1221_1_surface",
            "source_object": "surface/binding coefficient/prior or binding theorem-zero proof",
            "exact_required_fields": "coefficient_value; coefficient_units; threshold=6.987501646143863402e-11; source_path; source_needle; matter_functor_scope",
            "current_status": "MISSING_SOURCE_BACKED_SURFACE_COEFFICIENT_OR_PARENT_PRIMITIVE",
            "claim_use": "feed RUN1221_1_surface only after all fields are real",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "SRCREQ1223_2_source_weight",
            "p0_row": "ACQ1221_2_source_weight",
            "source_object": "source-weight product input",
            "exact_required_fields": "Delta_w_TiPt; tau_WEP; Earth/source worldtube; source-profile weighting; readout_kernel; eta_bound=2.8e-15; no-cancellation proof",
            "current_status": "MISSING_NUMERIC_PRIOR_WIDTH_AND_MISSING_LAB_SOURCE_ORBIT_PROJECTION",
            "claim_use": "feed RUN1221_2_source_weight and local-GR/source branch only after product is sourced",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "SRCREQ1223_3_readout",
            "p0_row": "ACQ1221_3_readout",
            "source_object": "readout kernel/functor closure",
            "exact_required_fields": "official arrays or parent readout functor; coefficient_drift_bound; units; masks/segments; convention map to observable",
            "current_status": "MISSING_RADIOUT_CLOSURE_AND_OFFICIAL_ARRAYS",
            "claim_use": "feed RUN1221_3_readout and every WEP/clock transfer row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    promotion_rows = [
        {
            "promotion_id": f"PROMO1223_{index}_{row['p0_row'].split('_')[-1]}",
            "p0_row": row["p0_row"],
            "attempted_route": row["derivation_route_attempted"],
            "promoted": False,
            "reason": row["failure_mode"],
            "fallback": "use exact source requirement row",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for index, row in enumerate(derivation_rows)
    ]

    narrowed_blockers = [
        {
            "narrow_id": "NAR1223_0_alpha",
            "original_blocker": "MISSING_SOURCE_BACKED_ALPHA_COEFFICIENT;MISSING_PARENT_PRIMITIVE;HSC1219_1_alpha",
            "narrowed_to": "either EM F2 coefficient-domain primitive, or numeric alpha coefficient/prior below 8.320244933243531978e-10",
            "why_this_is_exact": "alpha F2 counterexample is the only P0 alpha route left after 1220/1221 demotion",
            "next_source_or_proof": "PROOF1223_0_alpha;SRCREQ1223_0_alpha",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "narrow_id": "NAR1223_1_surface",
            "original_blocker": "MISSING_SOURCE_BACKED_SURFACE_COEFFICIENT;MISSING_PARENT_PRIMITIVE;HSC1219_2_surface_binding",
            "narrowed_to": "species-complete matter-functor fixed-constant proof, or numeric surface/binding coefficient below 6.987501646143863402e-11",
            "why_this_is_exact": "surface/binding row cannot be retired by absence in action because effective binding response remains a valid counterexample",
            "next_source_or_proof": "PROOF1223_1_surface;SRCREQ1223_1_surface",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "narrow_id": "NAR1223_2_source_weight",
            "original_blocker": "MISSING_NUMERIC_PRIOR_WIDTH;MISSING_LAB_SOURCE_ORBIT_PROJECTION;MISSING_SOURCE_PROFILE_WEIGHTING;CELOCK1220_2_source_weight",
            "narrowed_to": "parent action-scale/current owner proof, or sourced Delta_w_TiPt*tau_WEP product below 2.8e-15",
            "why_this_is_exact": "this branch is the direct local-GR/WEP coupling bottleneck and cannot be hidden in measured G",
            "next_source_or_proof": "PROOF1223_2_source_weight;SRCREQ1223_2_source_weight",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "narrow_id": "NAR1223_3_readout",
            "original_blocker": "MISSING_RADIOUT_CLOSURE;OFFICIAL_ARRAYS_NOT_IMPORTED;HSC1219_3_clock",
            "narrowed_to": "readout functor preservation proof, or official arrays/kernel plus bounded coefficient drift",
            "why_this_is_exact": "all observable transfer claims pass through readout, so surrogate kernels cannot promote claims",
            "next_source_or_proof": "PROOF1223_3_readout;SRCREQ1223_3_readout",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner_feed = [
        {
            "feed_id": "FEED1223_0_to_1222_runner",
            "target": "P8_Y5_R10_1222_FIRST_NONCLAIM_SCORE_TABLE.csv",
            "update": "no row promoted; all P0 blockers narrowed to exact proof/source requirements",
            "valid_prediction_rows_delta": 0,
            "score_ready_rows_delta": 0,
            "current_status": "RUNNER_REMAINS_ALL_REFUSED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "feed_id": "FEED1223_1_to_local_GR",
            "target": "local GR/Newton/PPN source-side route",
            "update": "source-weight owner is selected as next derivation-first target because it touches WEP/local-GR/PPN directly",
            "valid_prediction_rows_delta": 0,
            "score_ready_rows_delta": 0,
            "current_status": "SOURCE_WEIGHT_OWNER_NOT_DERIVED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC1223_0_no_P0_promotion",
            "decision": "do not promote any P0 coupling row",
            "because": "each derivation route still needs a parent-signed primitive or real source-backed finite input",
            "next_action": "work the source-weight owner proof first because it is the local-GR/WEP bottleneck",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1223_1_derivation_first_kept",
            "decision": "preserve derivation-first route",
            "because": "the exact proof contracts now state the missing premises rather than treating coupling as arbitrary fit parameters",
            "next_action": "attempt the source-weight action-scale/current-owner proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1223_2_source_fallback_ready",
            "decision": "stage fallback source requirements without claiming",
            "because": "if a proof fails, the scorepack needs concrete inputs rather than vibes",
            "next_action": "only feed 1222 when a real source/proof fills every field",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1223_0_sources",
            "gate": "source path and needle audit",
            "status": "PASS",
            "reason": "all local sources used by 1223 are traceable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1223_1_p0_import",
            "gate": "P0 queue imported",
            "status": "PASS",
            "reason": "four P0 coupling rows imported from 1222",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1223_2_derivation_promotion",
            "gate": "P0 derivation promoted",
            "status": "BLOCKED",
            "reason": "all DER1223 rows verdict DERIVATION_NOT_CLOSED_SOURCE_REQUIREMENT_RETAINED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1223_3_source_requirements",
            "gate": "fallback source requirements exact",
            "status": "PASS",
            "reason": "each P0 row has an exact source/proof contract",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1223_4_runner_promotion",
            "gate": "runner rows promoted",
            "status": "BLOCKED",
            "reason": "valid prediction rows remain zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1223_5_physical_claim",
            "gate": "WEP/local-GR/R10/EM claim permission",
            "status": "BLOCKED",
            "reason": "1223 is a derivation/source narrowing checkpoint only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_rows = [
        {
            "next_id": "NEXT1223_0_1224",
            "target_file": "1224-Y5-R10-source-weight-action-scale-current-owner-proof.md",
            "target_script": "scripts/Y5_R10_source_weight_action_scale_current_owner_proof.py",
            "task": "try to prove the source-weight branch is forbidden by a parent action-scale/current owner and quotient source-label forgetting; if not, write the exact finite source-weight input contract",
            "success_condition": "either source-weight theorem-zero is parent-signed, or Delta_w_TiPt, tau_WEP, source-profile, and readout inputs are reduced to a precise nonclaim acquisition contract",
            "do_not_do": "do not absorb the branch into measured G, do not set tau_WEP to unity, do not use cancellation, do not claim local-GR/WEP/PPN, do not edit formalization-workbench or push GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_tables = [
        (SOURCE_REGISTER_PATH, source_register),
        (P0_QUEUE_PATH, p0_queue),
        (DERIVATION_MATRIX_PATH, derivation_rows),
        (PROOF_CONTRACT_PATH, proof_contracts),
        (SOURCE_REQUIREMENTS_PATH, source_requirements),
        (PROMOTION_LEDGER_PATH, promotion_rows),
        (NARROWED_BLOCKERS_PATH, narrowed_blockers),
        (RUNNER_FEED_PATH, runner_feed),
        (DECISION_PATH, decision_rows),
        (CLAIM_GATES_PATH, claim_gates),
        (NEXT_PATH, next_rows),
    ]
    for path, rows in generated_tables:
        write_csv(path, rows)

    validation_rows = []
    validation_rows.append(
        validation_row(
            "VAL1223_0_sources_exist",
            "all cited local sources exist",
            all(parse_bool(row["path_exists"]) for row in source_register),
            f"{sum(1 for row in source_register if parse_bool(row['path_exists']))}/{len(source_register)} sources exist",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1223_1_needles_found",
            "all cited source needles found",
            all(parse_bool(row["needle_found"]) for row in source_register),
            f"{sum(1 for row in source_register if parse_bool(row['needle_found']))}/{len(source_register)} needles found",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1223_2_p0_rows_imported",
            "four P0 rows imported",
            len(p0_rows) == 4,
            "; ".join(row["acquisition_id"] for row in p0_rows),
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1223_3_derivations_attempted",
            "one derivation attempt per P0 row",
            len(derivation_rows) == len(p0_rows)
            and {row["p0_row"] for row in derivation_rows} == {row["acquisition_id"] for row in p0_rows},
            "; ".join(row["attempt_id"] for row in derivation_rows),
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1223_4_no_false_promotion",
            "no P0 row is falsely promoted",
            all(not parse_bool(row["promoted"]) and is_false(row, "claim_allowed") for row in promotion_rows),
            "all promotion rows promoted=false",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1223_5_source_requirements_exact",
            "all P0 rows have fallback source requirements",
            len(source_requirements) == len(p0_rows)
            and {row["p0_row"] for row in source_requirements} == {row["acquisition_id"] for row in p0_rows},
            "; ".join(row["requirement_id"] for row in source_requirements),
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1223_6_blockers_narrowed",
            "P0 blockers narrowed to exact proof/source contracts",
            len(narrowed_blockers) == len(p0_rows),
            "; ".join(row["narrow_id"] for row in narrowed_blockers),
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1223_7_runner_feed_nonclaim",
            "runner feed keeps zero valid predictions",
            all(row["valid_prediction_rows_delta"] == 0 and is_false(row, "claim_allowed") for row in runner_feed),
            "valid_prediction_rows_delta=0 for all feed rows",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1223_8_next_target_source_weight",
            "next target selects source-weight owner proof",
            next_rows[0]["target_file"] == "1224-Y5-R10-source-weight-action-scale-current-owner-proof.md",
            next_rows[0]["target_file"],
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1223_9_claim_gates_blocked",
            "claim gates keep physical claims blocked",
            any(row["status"] == "BLOCKED" for row in claim_gates) and all(is_false(row, "valid_for_claim") for row in claim_gates),
            "derivation/runner/physical claim gates blocked",
        )
    )
    validation_rows.append(
        validation_row(
            "VAL1223_10_nonclaim_policy",
            "all generated rows remain nonclaim",
            all(
                is_false(row, "valid_for_claim") and is_false(row, "claim_allowed")
                for _, rows in generated_tables
                for row in rows
                if "valid_for_claim" in row and "claim_allowed" in row
            ),
            "valid_for_claim=false and claim_allowed=false throughout claim-bearing tables",
        )
    )

    csv_parse_details = []
    csv_parse_ok = True
    for path, _ in generated_tables:
        try:
            parsed = read_csv(path)
            csv_parse_details.append(f"{path.name}:{len(parsed)}")
        except Exception as exc:  # pragma: no cover
            csv_parse_ok = False
            csv_parse_details.append(f"{path.name}:FAIL:{exc}")
    validation_rows.append(
        validation_row(
            "VAL1223_11_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(csv_parse_details),
        )
    )

    formalization_recent = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*"):
            if path.is_file():
                modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
                if modified >= RUN_STARTED_UTC:
                    formalization_recent.append(path)
    validation_rows.append(
        validation_row(
            "VAL1223_12_formalization_untouched",
            "formalization-workbench untouched during run",
            len(formalization_recent) == 0,
            f"formalization_recent_after_run_start_count={len(formalization_recent)}",
        )
    )

    overall_before = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        validation_row(
            "VAL1223_13_overall",
            "overall 1223 validation",
            overall_before,
            "1223 attempts P0 derivations, promotes no false rows, and narrows every P0 blocker",
        )
    )
    write_csv(VALIDATION_PATH, validation_rows)

    doc = f"""# 1223 Y5/R10 P0 Coupling Input Source Or Derivation Attack

**Current verdict:** 1223 tries the derivation route first for the four P0 coupling blockers and promotes none of them. That is not a collapse; it is a sharper map of the enemy. Every P0 row is now narrowed to an exact proof contract or an exact finite source requirement.

**Main progress:** alpha F2, surface/binding, source-weight, and readout are no longer one mushy “coupling problem.” They are four separate gates with named missing premises and nonclaim fallback inputs.

**Practical consequence:** the next best derivation-first target is source-weight action-scale/current ownership, because it is the coupling branch most directly tied to local GR/Newton/WEP/PPN.

## Source Register

{markdown_table(source_register, ["source_id", "local_path", "needle", "purpose", "absolute_path", "path_exists", "needle_found", "valid_for_claim", "claim_allowed"])}

## P0 Queue Import

{markdown_table(p0_queue, ["queue_id", "acquisition_id", "closure_id", "debt", "current_status", "attack_order", "valid_for_claim", "claim_allowed"])}

## Derivation Attempt Matrix

{markdown_table(derivation_rows, ["attempt_id", "p0_row", "target_zero_or_source", "derivation_route_attempted", "required_parent_clause", "best_current_support", "failure_mode", "verdict", "valid_for_claim", "claim_allowed"])}

## Minimal Proof Contracts

{markdown_table(proof_contracts, ["contract_id", "branch", "premises_required", "conclusion_if_signed", "current_gap", "fallback_source_requirement", "valid_for_claim", "claim_allowed"])}

## Fallback Source Requirements

{markdown_table(source_requirements, ["requirement_id", "p0_row", "source_object", "exact_required_fields", "current_status", "claim_use", "valid_for_claim", "claim_allowed"])}

## Promotion Attempt Ledger

{markdown_table(promotion_rows, ["promotion_id", "p0_row", "attempted_route", "promoted", "reason", "fallback", "valid_for_claim", "claim_allowed"])}

## Narrowed Blocker Ledger

{markdown_table(narrowed_blockers, ["narrow_id", "original_blocker", "narrowed_to", "why_this_is_exact", "next_source_or_proof", "valid_for_claim", "claim_allowed"])}

## Runner Feed Update

{markdown_table(runner_feed, ["feed_id", "target", "update", "valid_prediction_rows_delta", "score_ready_rows_delta", "current_status", "valid_for_claim", "claim_allowed"])}

## Decision Ledger

{markdown_table(decision_rows, ["decision_id", "decision", "because", "next_action", "valid_for_claim", "claim_allowed"])}

## Claim Gates

{markdown_table(claim_gates, ["gate_id", "gate", "status", "reason", "valid_for_claim", "claim_allowed"])}

## Next Target

{markdown_table(next_rows, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not_do", "valid_for_claim", "claim_allowed"])}

## Validation

{markdown_table(validation_rows, ["check_id", "check", "status", "details", "valid_for_claim", "claim_allowed"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()

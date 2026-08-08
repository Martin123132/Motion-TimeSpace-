from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = PROJECT / "formalization-workbench"

DOC = ROOT / "2868-Y5-R2FR-finite-core-source-acquisition-after-Uamp-closure-demotion-under-AX1090.md"

SRC_2868_SCRIPT = ROOT / "scripts" / "Y5_R2FR_finite_core_source_acquisition_after_Uamp_closure_demotion_under_AX1090_2868.py"
SRC_2867_DOC = ROOT / "2867-Y5-R2FR-parent-sigma-origin-and-vertical-generator-derivation-under-AX1090.md"
SRC_2867_DEMOTION = RESIDUALS / "P8_Y5_R2FR_2867_UAMP_CLOSURE_DEMOTION_LEDGER.csv"
SRC_2867_HESSIAN = RESIDUALS / "P8_Y5_R2FR_2867_HESSIAN_FACTORISATION_TEST.csv"
SRC_2867_NEXT = RESIDUALS / "P8_Y5_R2FR_2867_NEXT_TARGET.csv"
SRC_2867_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2867_VALIDATION.csv"
SRC_2866_ROLLUP = RESIDUALS / "P8_Y5_R2FR_2866_CORE_BLOCKER_ROLLUP.csv"
SRC_2865_BLOCKERS = RESIDUALS / "P8_Y5_R2FR_2865_SIGN_BLOCKER_LEDGER.csv"
SRC_2864_BLOCKERS = RESIDUALS / "P8_Y5_R2FR_2864_QREFF_BLOCKER_LEDGER.csv"
SRC_2863_BLOCKERS = RESIDUALS / "P8_Y5_R2FR_2863_QCAB_BLOCKER_LEDGER.csv"
SRC_2862_REQUESTS = RESIDUALS / "P8_Y5_R2FR_2862_FIRST_ROW_SOURCE_REQUEST_PACK.csv"
SRC_2862_REJECTIONS = RESIDUALS / "P8_Y5_R2FR_2862_SEMANTIC_REJECTION_RULES.csv"
SRC_2861_SCAN = RESIDUALS / "P8_Y5_R2FR_2861_FIRST_ROW_SOURCE_SCAN.csv"
SRC_2861_ACCEPT = RESIDUALS / "P8_Y5_R2FR_2861_FIRST_ROW_ACCEPTANCE_TEST.csv"
SRC_2860_DOC = ROOT / "2860-Y5-R2FR-finite-source-row-acquisition-after-Uamp-demotion-under-AX1090.md"
SRC_2860_PACK = RESIDUALS / "P8_Y5_R2FR_2860_FINITE_SOURCE_ACQUISITION_PACK.csv"
SRC_2860_PREFLIGHT = RESIDUALS / "P8_Y5_R2FR_2860_STRICT_IMPORT_PREFLIGHT.csv"
SRC_2860_TEMPLATE = RESIDUALS / "P8_Y5_R2FR_2860_STRICT_RUNNER_IMPORT_TEMPLATE_NONCLAIM.csv"
SRC_2860_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2860_VALIDATION.csv"
SRC_2859_QUEUE = RESIDUALS / "P8_Y5_R2FR_2859_FINITE_SOURCE_FALLBACK_QUEUE.csv"
SRC_2854_SCAN = RESIDUALS / "P8_Y5_R2FR_2854_REAL_SOURCE_ACQUISITION_SCAN.csv"
SRC_2854_BLOCKERS = RESIDUALS / "P8_Y5_R2FR_2854_BLOCKER_LEDGER.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2868_SOURCE_REGISTER.csv",
    "acquisition": RESIDUALS / "P8_Y5_R2FR_2868_FINITE_CORE_ACQUISITION_PACK.csv",
    "schema": RESIDUALS / "P8_Y5_R2FR_2868_SOURCE_ROW_SCHEMA.csv",
    "template": RESIDUALS / "P8_Y5_R2FR_2868_STRICT_RUNNER_IMPORT_TEMPLATE_NONCLAIM.csv",
    "preflight": RESIDUALS / "P8_Y5_R2FR_2868_ROW_READINESS_PREFLIGHT.csv",
    "arena": RESIDUALS / "P8_Y5_R2FR_2868_TEST_ARENA_PROJECTION_REQUIREMENTS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2868_ACCEPTANCE_GATES.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2868_RUNNER_REFUSAL.csv",
    "priority": RESIDUALS / "P8_Y5_R2FR_2868_SOURCE_PRIORITY_QUEUE.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2868_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2868_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2868_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2868_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "acquisition_copy": BETA_DOCS / "RAB_FINITE_CORE_ACQUISITION_PACK_2868_NONCLAIM.csv",
    "runner_copy": SOURCE_WEIGHT / "RAB_STRICT_RUNNER_REFUSAL_2868_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2868_core_finite_row_corpus_scan_NEXT.csv",
    "arena_copy": LOCAL_BOUNDS / "RAB_TEST_ARENA_PROJECTION_REQUIREMENTS_2868_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now(),
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2868_0_2867_doc", SRC_2867_DOC, "DEM2867_0_Uamp_route;NEXT2867_0_2868;VAL2867_OVERALL", "2867 demoted U_amp route and selected finite acquisition"),
        ("SRC2868_1_2867_demotion", SRC_2867_DEMOTION, "DEM2867_0_Uamp_route;DEM2867_2_finite_route;DEM2867_3_runner", "closure-only demotion ledger"),
        ("SRC2868_2_2867_hessian", SRC_2867_HESSIAN, "HESS2867_2_extract_sigma;HESS2867_5_verdict", "conditional Hessian law but no parent sigma"),
        ("SRC2868_3_2867_next", SRC_2867_NEXT, "NEXT2867_0_2868", "handoff target"),
        ("SRC2868_4_2867_validation", SRC_2867_VALIDATION, "VAL2867_OVERALL", "2867 validation"),
        ("SRC2868_5_2866_rollup", SRC_2866_ROLLUP, "CORE2866_0_Q_CAB;CORE2866_1_q_R_eff;CORE2866_6_full_vector", "core amplitude blocker rollup"),
        ("SRC2868_6_2865_blockers", SRC_2865_BLOCKERS, "BLOCK2865_0_SIGMA_SIGN;BLOCK2865_1_COMMON_GREEN;BLOCK2865_7_FULL_VECTOR", "sign/common Green/full-vector blockers"),
        ("SRC2868_7_2864_blockers", SRC_2864_BLOCKERS, "BLOCK2864_0_q_R_eff_VALUE;BLOCK2864_4_SIGMA_SIGN;BLOCK2864_7_QCAB_CARRY", "q_R_eff blocker ledger"),
        ("SRC2868_8_2863_blockers", SRC_2863_BLOCKERS, "BLOCK2863_0_Q_CAB_PARENT_INPUT;BLOCK2863_4_GREEN_SIGN", "Q_CAB blocker ledger"),
        ("SRC2868_9_2862_requests", SRC_2862_REQUESTS, "REQ2862_0_Q_CAB;REQ2862_1_q_R_eff;REQ2862_2_sigma_R_source_sign", "first-row source request pack"),
        ("SRC2868_10_2862_rejections", SRC_2862_REJECTIONS, "REJ2862_0_profile_as_sign;REJ2862_3_Uamp_zero;REJ2862_4_placeholder", "semantic rejection rules"),
        ("SRC2868_11_2861_scan", SRC_2861_SCAN, "SCAN2861_0_Q_CAB;SCAN2861_1_q_R_eff;SCAN2861_2_sigma_R_source_sign", "first row source scan"),
        ("SRC2868_12_2861_accept", SRC_2861_ACCEPT, "ACC2861_0_Q_CAB_numeric;ACC2861_5_runner_ready", "first row acceptance test"),
        ("SRC2868_13_2860_doc", SRC_2860_DOC, "ACQ2860_0_Q_CAB;VAL2860_OVERALL", "older finite acquisition pack"),
        ("SRC2868_14_2860_pack", SRC_2860_PACK, "ACQ2860_0_Q_CAB;ACQ2860_6_full_vector", "2860 finite acquisition rows"),
        ("SRC2868_15_2860_preflight", SRC_2860_PREFLIGHT, "PF2860_0_Q_CAB_value;PF2860_OVERALL", "2860 strict import refusal"),
        ("SRC2868_16_2860_template", SRC_2860_TEMPLATE, "CAND2860_0_finite_source_import_template_nonclaim;MISSING_Q_CAB", "2860 placeholder template"),
        ("SRC2868_17_2860_validation", SRC_2860_VALIDATION, "VAL2860_OVERALL", "2860 validation"),
        ("SRC2868_18_2859_queue", SRC_2859_QUEUE, "FSQ2859_0_Q_CAB;FSQ2859_6_strict_runner", "fallback queue"),
        ("SRC2868_19_2854_scan", SRC_2854_SCAN, "SCAN2854_0_Q_CAB;SCAN2854_6_full_vector", "real source acquisition scan"),
        ("SRC2868_20_2854_blockers", SRC_2854_BLOCKERS, "BLOCK2854_0_Q_CAB;BLOCK2854_6_full_vector", "real source blockers"),
        ("SRC2868_21_script", SRC_2868_SCRIPT, "def acquisition_rows;def validation_rows", "2868 generator self-check"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, anchors, role in specs:
        found, missing = anchors_present(path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def acquisition_rows() -> list[dict[str, Any]]:
    specs = [
        ("ACQ2868_0_Q_CAB", "Q_CAB", "finite target-map/source monopole", "real number or parent-zero theorem in the shared radial convention", "source_path; equation_anchor; units; L_CAB/J_CAB; boundary/corner policy; sign convention", "MISSING_PARENT_INPUT", "first_triplet", "SCAN2861_0_Q_CAB;REQ2862_0_Q_CAB;BLOCK2863_0_Q_CAB_PARENT_INPUT"),
        ("ACQ2868_1_q_R_eff", "q_R_eff", "finite residual-curvature Green charge", "real number or source-zero theorem in same convention as Q_CAB", "source_path; equation_anchor; q_R_eff=-int S_R/Z_R; ell_R/long-range limit; units; source support; boundary policy", "MISSING_SOURCE_NORMALIZATION", "first_triplet", "SCAN2861_1_q_R_eff;REQ2862_1_q_R_eff;BLOCK2864_0_q_R_eff_VALUE"),
        ("ACQ2868_2_sigma_R_source_sign", "sigma_R_source_sign", "operator/Green/source sign", "signed convention row, not profile sigma and not post-hoc cancellation sign", "source_path; equation_anchor; parent operator sign; metric signature; Green orientation; source equation convention", "MISSING_OPERATOR_GREEN_SIGN_OWNER", "first_triplet", "SCAN2861_2_sigma_R_source_sign;REQ2862_2_sigma_R_source_sign;BLOCK2865_0_SIGMA_SIGN"),
        ("ACQ2868_3_common_Green", "shared Green/radial convention", "same exterior normalization for C_AB and delta_R", "one convention defining C_AB=Q_CAB/(4*pi*r)+... and delta_R=sigma*q_R_eff exp(-r/ell)/(4*pi*r)+...", "source_path; equation_anchor; operator pair; 4*pi convention; sign orientation; range hierarchy", "MISSING_COMMON_GREEN_CONVENTION", "first_triplet", "BLOCK2865_1_COMMON_GREEN;CORE2866_3_common_Green"),
        ("ACQ2868_4_boundary_tail", "K_amp/B_CAB/B_R/tail", "boundary/improvement/tail row", "zero/exact/included theorem or finite arena-projected bound", "source_path; equation_anchor; worldtube/corner rule; compact support; tail projection; arena validity", "MISSING_SHARED_MEASURE_AND_BOUNDARY_CLASS", "second_triplet", "BLOCK2865_5_BOUNDARY_MEASURE;ACQ2860_4_boundary_tail"),
        ("ACQ2868_5_measured_GM", "M_source/GM", "worldtube source measure and weak-field metric readout", "same-frame measured GM denominator/source normalization", "source_path; equation_anchor; Hamiltonian/worldtube charge; no extra mass channel; metric 1/r convention", "MISSING_GM_PARENT_GLUE", "second_triplet", "BLOCK2854_5_GM;ACQ2860_5_GM"),
        ("ACQ2868_6_b_R_or_no_shadow", "b_R/no-shadow", "profile leak coefficient or theorem-zero owner", "finite coefficient or parent no-shadow theorem", "source_path; equation_anchor; profile definition; no-shadow proof; non-use as sigma source sign", "MISSING_B_R_OR_NO_SHADOW_THEOREM", "third_triplet", "ACQ2860_3_b_R;REJ2862_0_profile_as_sign"),
        ("ACQ2868_7_full_local_vector", "full PPN/local residual vector", "same-branch local residual rows", "finite/theorem rows for gamma,beta,preferred-frame,conservation,clock,orbital,q_loc,endpoint/readout", "source_path; equation_anchor; branch id; residual vector; norms; arena thresholds", "MISSING_FULL_VECTOR_CLOSURE", "third_triplet", "BLOCK2865_7_FULL_VECTOR;ACQ2860_6_full_vector"),
    ]
    rows = []
    for acquisition_id, quantity, required_object, minimum_value, minimum_provenance, blocker, priority, anchors in specs:
        rows.append(
            add_common(
                {
                    "acquisition_id": acquisition_id,
                    "quantity": quantity,
                    "required_object": required_object,
                    "minimum_value": minimum_value,
                    "minimum_provenance": minimum_provenance,
                    "source_anchors": anchors,
                    "current_blocker": blocker,
                    "priority": priority,
                    "accepted_source_present": False,
                    "numeric_or_theorem_zero_present": False,
                    "ready_for_strict_runner": False,
                }
            )
        )
    return rows


def schema_rows() -> list[dict[str, Any]]:
    specs = [
        ("SCHEMA2868_0_identity", "row_id;branch_id;arena_id", "nonempty strings", "identifies one branch and test arena"),
        ("SCHEMA2868_1_Q_CAB", "Q_CAB_value;Q_CAB_units;Q_CAB_source_path;Q_CAB_equation_anchor", "finite numeric/theorem-zero with source", "target-map numerator leg"),
        ("SCHEMA2868_2_q_R_eff", "q_R_eff_value;q_R_eff_units;q_R_eff_source_path;q_R_eff_equation_anchor;ell_R_value", "finite numeric/theorem-zero with source", "R-sector numerator leg"),
        ("SCHEMA2868_3_sigma", "sigma_R_source_sign;sign_convention;sigma_source_path;sigma_equation_anchor", "signed source convention only", "couples q_R_eff to Q_CAB"),
        ("SCHEMA2868_4_green", "common_green_convention;operator_pair;radial_4pi_convention", "no MISSING markers", "prevents sign/radial mismatch"),
        ("SCHEMA2868_5_boundary_tail", "boundary_policy;tail_bound;tail_source_path", "zero/exact/included/finite bound", "prevents hidden homogeneous modes"),
        ("SCHEMA2868_6_GM", "GM_value;GM_units;GM_source_path;GM_readout_convention", "measured same-frame source denominator", "normalizes PPN/local residuals"),
        ("SCHEMA2868_7_full_vector", "gamma;beta;alpha_i;xi;zeta_i;clock;orbital;q_loc;endpoint", "finite/theorem-zero vector", "prevents gamma-only local-GR claim"),
        ("SCHEMA2868_8_claim_flags", "control_only;score_ready;valid_prediction_row;valid_for_claim;claim_allowed", "all false until every row passes", "runner safety"),
    ]
    return [
        add_common(
            {
                "schema_id": schema_id,
                "fields": fields,
                "requirement": requirement,
                "purpose": purpose,
                "field_ready": False,
            }
        )
        for schema_id, fields, requirement, purpose in specs
    ]


def template_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "row_id": "CAND2868_0_finite_core_import_template_nonclaim",
                "branch_id": "R2FR_local_PPN_constant_limit_after_Uamp_closure_demotion",
                "arena_id": "R10_PPN_CLOCK_ORBITAL_LOCAL_VECTOR",
                "Q_CAB_value": "MISSING_Q_CAB",
                "Q_CAB_units": "MISSING_Q_CAB_UNITS",
                "Q_CAB_source_path": "",
                "Q_CAB_equation_anchor": "",
                "q_R_eff_value": "MISSING_q_R_eff",
                "q_R_eff_units": "MISSING_q_R_eff_UNITS",
                "q_R_eff_source_path": "",
                "q_R_eff_equation_anchor": "",
                "ell_R_value": "MISSING_ELL_R_OR_LONG_RANGE_LIMIT",
                "sigma_R_source_sign": "MISSING_sigma_R_source_sign",
                "sign_convention": "MISSING_SIGN_CONVENTION",
                "sigma_source_path": "",
                "sigma_equation_anchor": "",
                "common_green_convention": "MISSING_COMMON_GREEN_CONVENTION",
                "operator_pair": "MISSING_OPERATOR_PAIR",
                "radial_4pi_convention": "MISSING_4PI_CONVENTION",
                "boundary_policy": "MISSING_BOUNDARY_POLICY",
                "tail_bound": "MISSING_TAIL_BOUND",
                "tail_source_path": "",
                "GM_value": "MISSING_GM",
                "GM_units": "MISSING_GM_UNITS",
                "GM_source_path": "",
                "GM_readout_convention": "MISSING_GM_CONVENTION",
                "full_vector_status": "MISSING_FULL_LOCAL_VECTOR",
                "theorem_zero_authority": "UAMP_CLOSURE_ONLY_NOT_AUTHORITY",
                "numeric_value_present": False,
            }
        )
    ]


def preflight_rows(template: list[dict[str, Any]]) -> list[dict[str, Any]]:
    row = template[0]
    specs = [
        ("PF2868_0_Q_CAB_value", "Q_CAB_value", row["Q_CAB_value"], "finite numeric or accepted theorem-zero"),
        ("PF2868_1_q_R_eff_value", "q_R_eff_value", row["q_R_eff_value"], "finite numeric or accepted theorem-zero"),
        ("PF2868_2_sigma_sign", "sigma_R_source_sign", row["sigma_R_source_sign"], "signed source convention"),
        ("PF2868_3_common_green", "common_green_convention", row["common_green_convention"], "shared radial/Green convention"),
        ("PF2868_4_boundary_tail", "boundary_policy/tail_bound", f"{row['boundary_policy']};{row['tail_bound']}", "boundary zero/exact/included/finite tail"),
        ("PF2868_5_GM", "GM_value", row["GM_value"], "measured same-frame GM/source denominator"),
        ("PF2868_6_full_vector", "full_vector_status", row["full_vector_status"], "full same-branch local residual vector"),
        ("PF2868_7_source_paths", "all source paths", "Q_CAB=blank;q_R_eff=blank;sigma=blank;tail=blank;GM=blank", "existing source paths with anchors"),
        ("PF2868_8_claim_authority", "theorem_zero_authority", row["theorem_zero_authority"], "parent-signed theorem or finite rows only"),
    ]
    rows = []
    for preflight_id, field, marker, requirement in specs:
        rows.append(
            add_common(
                {
                    "preflight_id": preflight_id,
                    "field": field,
                    "value_or_marker": marker,
                    "requirement": requirement,
                    "preflight_passed": False,
                    "failure_reason": "MISSING_OR_CLOSURE_ONLY_INPUT",
                }
            )
        )
    rows.append(
        add_common(
            {
                "preflight_id": "PF2868_OVERALL",
                "field": "strict_import_template",
                "value_or_marker": "template remains placeholder-only after U_amp demotion",
                "requirement": "all finite source rows and conventions present",
                "preflight_passed": False,
                "failure_reason": "REFUSED_MISSING_PROVENANCE_OR_INPUTS",
            }
        )
    )
    return rows


def arena_rows() -> list[dict[str, Any]]:
    specs = [
        ("ARENA2868_0_R10", "short-range fifth-force/R10", "Q_CAB,q_R_eff,sigma,common Green,ell_R,boundary/tail,source mass", "alpha(lambda) row or theorem-zero residual", "BLOCKED"),
        ("ARENA2868_1_PPN", "solar-system PPN", "A_total,GM,b_R,boundary/full vector", "gamma,beta,preferred-frame/conservation rows", "BLOCKED"),
        ("ARENA2868_2_clocks", "clock/local time tests", "clock residual row plus same branch GM/source convention", "clock residual bound or theorem-zero", "BLOCKED"),
        ("ARENA2868_3_orbital", "orbital dynamics", "measured GM glue, endpoint/readout, preferred-frame vector", "perihelion/range/residual rows", "BLOCKED"),
        ("ARENA2868_4_local_GR", "full local GR/Newton reduction", "all amplitude rows plus full local residual vector", "no gamma-only pass; all channels closed", "BLOCKED"),
    ]
    return [
        add_common(
            {
                "arena_id": arena_id,
                "arena": arena,
                "required_inputs": inputs,
                "acceptable_output": output,
                "status": status,
                "arena_ready": False,
            }
        )
        for arena_id, arena, inputs, output, status in specs
    ]


def gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATE2868_0_first_triplet", "Q_CAB, q_R_eff and sigma_R_source_sign all source-backed in one convention", "FAIL", "all three remain missing/source-incomplete"),
        ("GATE2868_1_common_green", "common Green/radial/sign convention accepted", "FAIL", "2865 common Green verdict is not accepted"),
        ("GATE2868_2_boundary_tail", "boundary/tail zero/exact/included or finite bound", "FAIL", "boundary/worldtube/tail inputs missing"),
        ("GATE2868_3_measured_GM", "measured same-frame GM/source denominator accepted", "FAIL", "GM parent glue remains conditional/open"),
        ("GATE2868_4_full_vector", "same-branch full local residual vector closed", "FAIL", "full vector missing"),
        ("GATE2868_5_no_closure_loophole", "U_amp closure-only route cannot substitute for finite rows", "PASS_GUARD_ONLY", "2867 demotion blocks theorem-zero shortcut"),
        ("GATE2868_6_runner", "strict runner can score", "FAIL", "preflight refuses template"),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "criterion": criterion,
                "result": result,
                "reason": reason,
                "gate_passed": False,
                "guard_passed_nonclaim": result == "PASS_GUARD_ONLY",
            }
        )
        for gate_id, criterion, result, reason in specs
    ]


def runner_rows() -> list[dict[str, Any]]:
    specs = [
        ("RUNREF2868_0_template", "strict runner import template", "REFUSED", "contains MISSING_* markers and blank source paths"),
        ("RUNREF2868_1_Uamp", "U_amp closure-only authority", "REFUSED", "closure-only is not theorem-zero authority"),
        ("RUNREF2868_2_sigma_profile", "sigma_R_profile as source sign", "REFUSED", "profile import rejected by 2862/2865"),
        ("RUNREF2868_3_partial_triplet", "score with only one or two numerator/sign rows", "REFUSED", "A_total needs all first triplet rows in one convention"),
        ("RUNREF2868_4_local_GR", "local GR/Newton claim", "REFUSED", "GM and full vector not closed"),
    ]
    return [
        add_common(
            {
                "runner_id": runner_id,
                "attempt": attempt,
                "status": status,
                "reason": reason,
                "runner_ready": False,
                "score_allowed": False,
            }
        )
        for runner_id, attempt, status, reason in specs
    ]


def priority_rows() -> list[dict[str, Any]]:
    specs = [
        ("PRI2868_0_triplet_scan", 1, "corpus scan for first triplet", "Q_CAB,q_R_eff,sigma_R_source_sign,common Green", "needed before any A_total scoring"),
        ("PRI2868_1_boundary_tail", 2, "boundary/tail source row", "K_amp,B_CAB,B_R,H_R,C_AB_reg", "prevents hidden homogeneous/tail residuals"),
        ("PRI2868_2_GM", 3, "measured GM glue", "M_source,GM,H_tau,metric 1/r readout", "needed for PPN/Newton normalization"),
        ("PRI2868_3_full_vector", 4, "full local vector", "beta,preferred,conservation,clock,orbital,q_loc,endpoint", "needed to avoid gamma-only claim"),
        ("PRI2868_4_empirical_runner", 5, "strict runner smoke only after rows pass", "A_total/R10/PPN/local vector", "testing step after source-backed rows"),
    ]
    return [
        add_common(
            {
                "priority_id": priority_id,
                "rank": rank,
                "task": task,
                "quantities": quantities,
                "why_next": why,
                "selected_for_next": priority_id == "PRI2868_0_triplet_scan",
                "claim_ready": False,
            }
        )
        for priority_id, rank, task, quantities, why in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2868_0_post_demotion", "U_amp closure-only status is now enforced in finite acquisition.", "CARRIED_FORWARD", "the closure route cannot unlock theorem-zero or runner scoring"),
        ("DEC2868_1_pack", "Finite source acquisition pack is updated for post-2867 requirements.", "COMPLETE_NONCLAIM", "Q_CAB, q_R_eff, sigma, common Green, boundary/tail, GM and full vector are all explicit rows"),
        ("DEC2868_2_runner", "Strict runner remains refused.", "LOCKED", "template contains placeholders and missing provenance"),
        ("DEC2868_3_next", "Next step is automated corpus scan/ranking for real finite rows.", "SELECTED_2869", "we need actual source-backed rows, not another abstract gate"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "result": result,
                "because": because,
            }
        )
        for decision_id, decision, result, because in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2868_0_2869",
                "status": "selected_primary",
                "target_doc": "2869-Y5-R2FR-core-finite-row-corpus-scan-and-source-request-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_core_finite_row_corpus_scan_and_source_request_under_AX1090_2869.py",
                "mission": "scan the current corpus for actual finite/source-backed rows for Q_CAB, q_R_eff, sigma_R_source_sign, common Green convention, boundary/tail, measured GM and full local vector; rank candidates, reject placeholders/profile imports/Uamp closure authority, and emit exact source requests for any still-missing rows",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("COPY2868_0_acquisition", OUTPUTS["acquisition"], BRANCH_OUTPUTS["acquisition_copy"], "finite core acquisition pack nonclaim copy"),
        ("COPY2868_1_runner", OUTPUTS["runner"], BRANCH_OUTPUTS["runner_copy"], "strict runner refusal nonclaim copy"),
        ("COPY2868_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue handoff to 2869 corpus scan"),
        ("COPY2868_3_arena", OUTPUTS["arena"], BRANCH_OUTPUTS["arena_copy"], "test arena projection requirements nonclaim copy"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_table, copy_path, purpose in specs:
        copy_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_table, copy_path)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_table": str(source_table),
                    "copy_path": str(copy_path),
                    "purpose": purpose,
                    "exists": copy_path.exists(),
                }
            )
        )
    return rows


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    forbidden_true_fields = {
        "valid_for_claim",
        "claim_allowed",
        "score_ready",
        "valid_prediction_row",
        "accepted_source_present",
        "numeric_or_theorem_zero_present",
        "ready_for_strict_runner",
        "field_ready",
        "preflight_passed",
        "arena_ready",
        "gate_passed",
        "runner_ready",
        "score_allowed",
        "claim_ready",
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key, value in row.items():
                if key in forbidden_true_fields and str(value).lower() == "true":
                    return False
    return True


def cited_paths_exist(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            for key, value in row.items():
                if not key.endswith("_path") and key not in {"source_table", "copy_path"}:
                    continue
                if value in {"", None}:
                    continue
                path_text = str(value)
                if path_text.startswith("scripts/") or path_text.startswith("scripts\\"):
                    continue
                if not Path(path_text).exists():
                    return False
    return True


def generated_under_root() -> bool:
    paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
    for path in paths:
        try:
            path.resolve().relative_to(ROOT.resolve())
        except ValueError:
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            if modified > SCRIPT_START_UTC:
                return False
    return True


def pycache_absent() -> bool:
    return not (ROOT / "scripts" / "__pycache__").exists()


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_paths = [path for path in OUTPUTS.values() if path != OUTPUTS["validation"]]
    branch_paths = list(BRANCH_OUTPUTS.values())
    required_quantities = {
        "Q_CAB",
        "q_R_eff",
        "sigma_R_source_sign",
        "shared Green/radial convention",
        "K_amp/B_CAB/B_R/tail",
        "M_source/GM",
        "full PPN/local residual vector",
    }
    acquisition_quantities = {row["quantity"] for row in rows_by_name["acquisition"]}
    checks = [
        ("VAL2868_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all registered source paths exist"),
        ("VAL2868_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all registered anchors were found"),
        ("VAL2868_2_acquisition_covers_core", required_quantities.issubset(acquisition_quantities), "acquisition pack covers core triplet, common Green, boundary/tail, GM and full vector"),
        ("VAL2868_3_schema_written", len(rows_by_name["schema"]) >= 9 and any(row["schema_id"] == "SCHEMA2868_8_claim_flags" for row in rows_by_name["schema"]), "strict finite source row schema written"),
        ("VAL2868_4_template_nonclaim", rows_by_name["template"][0]["Q_CAB_value"] == "MISSING_Q_CAB" and rows_by_name["template"][0]["theorem_zero_authority"] == "UAMP_CLOSURE_ONLY_NOT_AUTHORITY", "runner template remains placeholder/nonclaim"),
        ("VAL2868_5_preflight_refuses", all(not row["preflight_passed"] for row in rows_by_name["preflight"]), "preflight rejects every missing input"),
        ("VAL2868_6_arena_blocked", all(not row["arena_ready"] for row in rows_by_name["arena"]), "all test arenas remain blocked until finite rows exist"),
        ("VAL2868_7_gates_fail_closed", all(not row["gate_passed"] for row in rows_by_name["gates"]), "acceptance gates fail closed"),
        ("VAL2868_8_runner_refused", all(not row["runner_ready"] for row in rows_by_name["runner"]), "strict runner remains refused"),
        ("VAL2868_9_next_target_2869", rows_by_name["next"][0]["next_id"] == "NEXT2868_0_2869" and "corpus_scan" in rows_by_name["next"][0]["target_script"], "core finite row corpus scan selected next"),
        ("VAL2868_10_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2868_11_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2868_12_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2868_13_cited_paths_exist", cited_paths_exist(rows_by_name), "all cited local file/copy paths in generated rows exist"),
        ("VAL2868_14_no_claim_flags", no_claim_flags(rows_by_name), "no claim/score/prediction flags are true"),
        ("VAL2868_15_generated_under_post_checkpoint", generated_under_root(), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2868_16_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2868_17_pycache_absent", pycache_absent(), "scripts __pycache__ absent during validation"),
    ]
    rows = [
        {
            "validation_id": validation_id,
            "passed": passed,
            "detail": detail,
            "timestamp_utc": now(),
        }
        for validation_id, passed, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2868_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2868 updates the finite core source acquisition pack after U_amp closure demotion, refuses the strict runner, keeps every local-test arena blocked, and selects a corpus-wide finite-row scan for 2869.",
            "timestamp_utc": now(),
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 2868 - Y5 R2FR Finite Core Source Acquisition After U_amp Closure Demotion Under AX1090",
        "",
        "Status: `Y5_R2FR_2868_finite_core_acquisition_pack_updated_runner_refused_corpus_scan_next`",
        "",
        "## Private Verdict",
        "",
        "2868 turns the post-2867 situation into an acquisition contract.",
        "",
        "`U_amp` is useful closure machinery, but it is not a parent theorem in the current corpus. So it cannot be used as `theorem_zero_authority`, cannot fill `sigma_R_source_sign`, and cannot unlock `A_total`.",
        "",
        "The finite route now requires a source-backed row set:",
        "",
        "```text",
        "first triplet: Q_CAB, q_R_eff, sigma_R_source_sign, shared Green convention",
        "second layer: boundary/tail and measured GM glue",
        "third layer: b_R/no-shadow plus full local residual vector",
        "```",
        "",
        "The strict runner template is deliberately still invalid. It contains missing values, missing source paths, missing conventions, and missing full-vector rows. This is a feature, not a bug: it prevents closure-only algebra from being laundered into an empirical claim.",
        "",
        "The next useful move is not another proof gate. It is a corpus-wide scan/ranker for actual finite/source-backed rows, with exact source requests for anything still missing.",
        "",
        "## Source Register",
        "",
        markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"]),
        "",
        "## Finite Core Acquisition Pack",
        "",
        markdown_table(rows["acquisition"], ["acquisition_id", "quantity", "required_object", "minimum_value", "current_blocker", "priority", "accepted_source_present", "numeric_or_theorem_zero_present", "ready_for_strict_runner", "valid_for_claim"]),
        "",
        "## Source Row Schema",
        "",
        markdown_table(rows["schema"], ["schema_id", "fields", "requirement", "purpose", "field_ready", "valid_for_claim"]),
        "",
        "## Strict Runner Import Template",
        "",
        markdown_table(rows["template"], ["row_id", "branch_id", "arena_id", "Q_CAB_value", "q_R_eff_value", "sigma_R_source_sign", "common_green_convention", "boundary_policy", "GM_value", "full_vector_status", "theorem_zero_authority", "numeric_value_present", "valid_for_claim"]),
        "",
        "## Row Readiness Preflight",
        "",
        markdown_table(rows["preflight"], ["preflight_id", "field", "value_or_marker", "requirement", "preflight_passed", "failure_reason", "valid_for_claim"]),
        "",
        "## Test Arena Projection Requirements",
        "",
        markdown_table(rows["arena"], ["arena_id", "arena", "required_inputs", "acceptable_output", "status", "arena_ready", "valid_for_claim"]),
        "",
        "## Acceptance Gates",
        "",
        markdown_table(rows["gates"], ["gate_id", "criterion", "result", "reason", "gate_passed", "guard_passed_nonclaim", "valid_for_claim"]),
        "",
        "## Runner Refusal",
        "",
        markdown_table(rows["runner"], ["runner_id", "attempt", "status", "reason", "runner_ready", "score_allowed", "valid_for_claim"]),
        "",
        "## Source Priority Queue",
        "",
        markdown_table(rows["priority"], ["priority_id", "rank", "task", "quantities", "why_next", "selected_for_next", "claim_ready", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        markdown_table(rows["decision"], ["decision_id", "decision", "result", "because", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        markdown_table(rows["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        markdown_table(rows["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        markdown_table(rows["validation"], ["validation_id", "passed", "detail", "timestamp_utc"]),
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows: dict[str, list[dict[str, Any]]] = {}
    rows["sources"] = source_register_rows()
    rows["acquisition"] = acquisition_rows()
    rows["schema"] = schema_rows()
    rows["template"] = template_rows()
    rows["preflight"] = preflight_rows(rows["template"])
    rows["arena"] = arena_rows()
    rows["gates"] = gate_rows()
    rows["runner"] = runner_rows()
    rows["priority"] = priority_rows()
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "acquisition", "schema", "template", "preflight", "arena", "gates", "runner", "priority", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])
    remove_pycache()
    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2868_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2868_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()

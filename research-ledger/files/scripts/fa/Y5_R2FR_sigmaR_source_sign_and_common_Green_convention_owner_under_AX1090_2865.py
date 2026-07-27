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

DOC = ROOT / "2865-Y5-R2FR-sigmaR-source-sign-and-common-Green-convention-owner-under-AX1090.md"

SRC_2864_DOC = ROOT / "2864-Y5-R2FR-qReff-first-source-row-or-parent-normalization-owner-under-AX1090.md"
SRC_2864_BLOCKERS = RESIDUALS / "P8_Y5_R2FR_2864_QREFF_BLOCKER_LEDGER.csv"
SRC_2864_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2864_VALIDATION.csv"
SRC_2863_BLOCKERS = RESIDUALS / "P8_Y5_R2FR_2863_QCAB_BLOCKER_LEDGER.csv"
SRC_2862_DICT = RESIDUALS / "P8_Y5_R2FR_2862_SIGMA_CANONICAL_DICTIONARY.csv"
SRC_2862_SCHEMA = RESIDUALS / "P8_Y5_R2FR_2862_STRICT_RUNNER_SCHEMA_SPLIT.csv"
SRC_2862_REJECT = RESIDUALS / "P8_Y5_R2FR_2862_SEMANTIC_REJECTION_RULES.csv"
SRC_2861_COLLISION = RESIDUALS / "P8_Y5_R2FR_2861_SIGMA_SYMBOL_COLLISION_AUDIT.csv"
SRC_2861_SCAN = RESIDUALS / "P8_Y5_R2FR_2861_FIRST_ROW_SOURCE_SCAN.csv"
SRC_2839_KERNEL = RESIDUALS / "P8_Y5_R2FR_2839_GREEN_KERNEL_NORMALIZATION.csv"
SRC_2840_PACK = RESIDUALS / "P8_Y5_R2FR_2840_NORMALIZATION_PACK_CONTRACT.csv"
SRC_2841_BRIDGE = RESIDUALS / "P8_Y5_R2FR_2841_QREFF_TO_QRHAT_CONDITIONAL_BRIDGE.csv"
SRC_2844_FLUX = RESIDUALS / "P8_Y5_R2FR_2844_CAB_GREEN_FLUX_IDENTITY.csv"
SRC_2844_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2844_PARENT_AMPLITUDE_CONTRACT.csv"
SRC_2850_MANUAL = RESIDUALS / "P8_Y5_R2FR_2850_MANUAL_SOURCE_LEDGER.csv"
SRC_2851_REQ = RESIDUALS / "P8_Y5_R2FR_2851_PARENT_SIGNATURE_REQUIREMENTS.csv"
SRC_2852_FALLBACK = RESIDUALS / "P8_Y5_R2FR_2852_FINITE_AMPLITUDE_FALLBACK_CONTRACT.csv"
SRC_2854_BLOCKER = RESIDUALS / "P8_Y5_R2FR_2854_BLOCKER_LEDGER.csv"
SRC_2855_DOC = ROOT / "2855-Y5-R2FR-parent-source-equation-draft-or-user-source-request-under-AX1090.md"
SRC_2855_DRAFT = RESIDUALS / "P8_Y5_R2FR_2855_PARENT_SOURCE_EQUATION_DRAFT.csv"
SRC_2855_STATUS = RESIDUALS / "P8_Y5_R2FR_2855_DERIVATION_STATUS_MATRIX.csv"
SRC_2855_REQUESTS = RESIDUALS / "P8_Y5_R2FR_2855_USER_SOURCE_REQUEST_LEDGER.csv"
SRC_2856_CLAUSES = RESIDUALS / "P8_Y5_R2FR_2856_VARIATIONAL_CLAUSE_AUDIT.csv"
SRC_2856_OBS = RESIDUALS / "P8_Y5_R2FR_2856_OBSTRUCTION_LEDGER.csv"
SRC_2857_OWNER = RESIDUALS / "P8_Y5_R2FR_2857_PARENT_OWNERSHIP_GATE.csv"
SRC_2858_GATE = RESIDUALS / "P8_Y5_R2FR_2858_CONSISTENCY_GATE_MATRIX.csv"
SRC_2859_QUEUE = RESIDUALS / "P8_Y5_R2FR_2859_FINITE_SOURCE_FALLBACK_QUEUE.csv"
SRC_2859_DOC = ROOT / "2859-Y5-R2FR-Uamp-parent-origin-or-finite-source-fallback-under-AX1090.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2865_SOURCE_REGISTER.csv",
    "evidence": RESIDUALS / "P8_Y5_R2FR_2865_SIGMA_SOURCE_SIGN_EVIDENCE_SCAN.csv",
    "green": RESIDUALS / "P8_Y5_R2FR_2865_COMMON_GREEN_CONVENTION_AUDIT.csv",
    "profile": RESIDUALS / "P8_Y5_R2FR_2865_PROFILE_IMPORT_REJECTION_AUDIT.csv",
    "acceptance": RESIDUALS / "P8_Y5_R2FR_2865_SIGMA_ACCEPTANCE_GATE.csv",
    "blockers": RESIDUALS / "P8_Y5_R2FR_2865_SIGN_BLOCKER_LEDGER.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2865_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2865_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2865_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2865_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "evidence_copy": LOCAL_BOUNDS / "RAB_SIGMA_SOURCE_SIGN_EVIDENCE_SCAN_2865_NONCLAIM.csv",
    "blocker_copy": SOURCE_WEIGHT / "RAB_SIGMA_SIGN_BLOCKER_LEDGER_2865_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2865_core_amplitude_parent_contract_NEXT.csv",
    "green_copy": BETA_DOCS / "RAB_SIGMA_COMMON_GREEN_CONVENTION_2865_NONCLAIM.csv",
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
        ("SRC2865_0_2864_doc", SRC_2864_DOC, "NEXT2864_0_2865;VAL2864_OVERALL", "2864 handoff to sigma/sign convention"),
        ("SRC2865_1_2864_blockers", SRC_2864_BLOCKERS, "BLOCK2864_4_SIGMA_SIGN;BLOCK2864_7_QCAB_CARRY;BLOCK2864_8_HANDOFF", "q_R_eff blockers and sigma handoff"),
        ("SRC2865_2_2864_validation", SRC_2864_VALIDATION, "VAL2864_OVERALL", "2864 validation"),
        ("SRC2865_3_2863_QCAB", SRC_2863_BLOCKERS, "BLOCK2863_0_Q_CAB_PARENT_INPUT;BLOCK2863_6_HANDOFF", "Q_CAB blocker carried into sign audit"),
        ("SRC2865_4_2862_dictionary", SRC_2862_DICT, "SIG2862_0_source_sign;SIG2862_1_profile;SIG2862_2_bridge", "canonical sigma split"),
        ("SRC2865_5_2862_schema", SRC_2862_SCHEMA, "SCHEMA2862_2_sigma_source_sign;SCHEMA2862_3_sigma_profile;SCHEMA2862_5_rejection_flag", "strict runner sigma slots"),
        ("SRC2865_6_2862_rejections", SRC_2862_REJECT, "REJ2862_0_profile_as_sign;REJ2862_2_gamma_bound_backsolve;REJ2862_4_placeholder", "semantic rejection rules"),
        ("SRC2865_7_2861_collision", SRC_2861_COLLISION, "COL2861_0_runner_sigma;COL2861_1_profile_sigma;COL2861_2_decision", "sigma collision audit"),
        ("SRC2865_8_2861_scan", SRC_2861_SCAN, "SCAN2861_2_sigma_R_source_sign;SCAN2861_3_sigma_R_profile_collision", "first-row sigma source scan"),
        ("SRC2865_9_2839_kernel", SRC_2839_KERNEL, "KER2839_1_normalized_operator;KER2839_3_solution;KER2839_4_compact_body", "delta_R Green orientation"),
        ("SRC2865_10_2840_pack", SRC_2840_PACK, "PACK2840_2_sign", "normalization-pack sign slot"),
        ("SRC2865_11_2841_bridge", SRC_2841_BRIDGE, "BRG2841_0_kernel_exterior;BRG2841_3_charge_map;BRG2841_4_qRhat_map", "conditional q_R bridge sign use"),
        ("SRC2865_12_2844_flux", SRC_2844_FLUX, "FLUX2844_3_deltaR_amplitude;FLUX2844_4_local_ppn_amplitude;FLUX2844_5_local_suppression_condition", "C_AB and delta_R amplitude combination"),
        ("SRC2865_13_2844_contract", SRC_2844_CONTRACT, "CONTRACT2844_0_operator;CONTRACT2844_5_sign", "parent common operator/sign contract"),
        ("SRC2865_14_2850_manual", SRC_2850_MANUAL, "MAN2850_3_sign_operator;MAN2850_4_identity", "manual source/sign ledger"),
        ("SRC2865_15_2851_requirements", SRC_2851_REQ, "REQ2851_3_operator_sign", "parent signature requirements"),
        ("SRC2865_16_2852_fallback", SRC_2852_FALLBACK, "FB2852_2_sigma_R", "finite amplitude fallback sigma slot"),
        ("SRC2865_17_2854_blocker", SRC_2854_BLOCKER, "BLOCK2854_2_sigma_R", "source acquisition blocker"),
        ("SRC2865_18_2855_doc", SRC_2855_DOC, "PEQ2855_2_sigma_sign;USR2855_3_sigma", "parent source equation draft for sigma"),
        ("SRC2865_19_2855_draft", SRC_2855_DRAFT, "PEQ2855_2_sigma_sign;PEQ2855_3_amp_current_identity", "draft sign/current equations"),
        ("SRC2865_20_2855_status", SRC_2855_STATUS, "STAT2855_2_sigma_sign", "draft sign remains unaccepted"),
        ("SRC2865_21_2855_requests", SRC_2855_REQUESTS, "USR2855_3_sigma", "open source request for sigma"),
        ("SRC2865_22_2856_clauses", SRC_2856_CLAUSES, "CLAUSE2856_1_vertical_generator;CLAUSE2856_3_source_split;CLAUSE2856_4_operator_side", "variational clauses needing sign/operator ownership"),
        ("SRC2865_23_2856_obstructions", SRC_2856_OBS, "OBS2856_2_operator;OBS2856_4_sign", "operator and sigma obstructions"),
        ("SRC2865_24_2857_ownership", SRC_2857_OWNER, "OWN2857_0_sigma;OWN2857_2_generator;OWN2857_4_boundary", "parent ownership gates"),
        ("SRC2865_25_2858_consistency", SRC_2858_GATE, "GATE2858_1_sigma_owner;GATE2858_6_matter_descent", "amplitude-doublet consistency gates"),
        ("SRC2865_26_2859_queue", SRC_2859_QUEUE, "FSQ2859_1_q_R_eff;FSQ2859_2_sigma_R", "finite fallback queue"),
        ("SRC2865_27_2859_doc", SRC_2859_DOC, "ORG2859_1_sigma_origin;DER2859_2_missing_origin", "U_amp origin demotion"),
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


def evidence_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "SIGEV2865_0_canonical_source_sign",
            "sigma_R_source_sign",
            "runner sign slot",
            SRC_2862_DICT,
            "SIG2862_0_source_sign",
            "A dimensionless sign/convention multiplying q_R_eff in A_total=(sigma_R_source_sign*q_R_eff+Q_CAB)/(4*pi).",
            "MISSING_OPERATOR_GREEN_SIGN_OWNER",
            "accepted source-sign row absent",
        ),
        (
            "SIGEV2865_1_profile_not_sign",
            "sigma_R_profile",
            "weak-field profile",
            SRC_2862_DICT,
            "SIG2862_1_profile",
            "The profile row is a symbolic weak-field/conformal-log profile, not the source sign convention.",
            "PROFILE_IMPORT_REJECTED",
            "requires separate bridge; cannot populate sigma_R_source_sign",
        ),
        (
            "SIGEV2865_2_collision_audit",
            "sigma_R",
            "symbol collision",
            SRC_2861_COLLISION,
            "COL2861_2_decision",
            "The runner sign and weak-field profile must remain separate before scoring.",
            "DISAMBIGUATED_BUT_UNSIGNED",
            "sign owner still missing",
        ),
        (
            "SIGEV2865_3_kernel_solution_sign",
            "delta_R Green sign",
            "kernel orientation",
            SRC_2839_KERNEL,
            "KER2839_3_solution",
            "The solution sign follows the finite E_R convention, but the observable/source sign must be fixed by a parent source convention.",
            "SYMBOLIC_KERNEL_SIGN_ONLY",
            "parent source equation and signature convention missing",
        ),
        (
            "SIGEV2865_4_pack_sign_slot",
            "sigma_R",
            "normalization-pack sign slot",
            SRC_2840_PACK,
            "PACK2840_2_sign",
            "The pack requires a sign that fixes whether a compact source raises or lowers delta_R.",
            "MISSING_SOURCE_SIGN",
            "source sign not derived or sourced",
        ),
        (
            "SIGEV2865_5_conditional_bridge",
            "sigma_R bridge",
            "conditional PPN bridge",
            SRC_2841_BRIDGE,
            "BRG2841_3_charge_map",
            "Q_R and q_R_hat maps depend on sigma_R and are conditional on the convention already being fixed.",
            "CONDITIONAL_MAP_ONLY",
            "cannot define sigma_R from the observable map",
        ),
        (
            "SIGEV2865_6_A_total_formula",
            "A_total",
            "amplitude formula",
            SRC_2844_FLUX,
            "FLUX2844_4_local_ppn_amplitude",
            "A_total=(sigma_R*q_R_eff+Q_CAB)/(4*pi) only after C_AB and delta_R share one radial convention.",
            "FORMULA_REQUIRES_COMMON_CONVENTION",
            "Q_CAB, q_R_eff, sigma_R are all unsigned/source-incomplete",
        ),
        (
            "SIGEV2865_7_parent_contract",
            "sigma_R",
            "parent action sign contract",
            SRC_2844_CONTRACT,
            "CONTRACT2844_5_sign",
            "The parent action must fix the sigma_R sign and Green convention.",
            "MISSING_SIGN_CONVENTION",
            "no parent-signed sign owner",
        ),
        (
            "SIGEV2865_8_manual_ledger",
            "sigma_R",
            "manual source ledger",
            SRC_2850_MANUAL,
            "MAN2850_3_sign_operator",
            "The manual ledger asks for sigma_R from the parent quadratic operator sign and Green kernel.",
            "MISSING_SIGMA_R_PARENT_SIGN",
            "manual request is not a source row",
        ),
        (
            "SIGEV2865_9_draft_sign_equation",
            "sigma_R",
            "parent equation draft",
            SRC_2855_DRAFT,
            "PEQ2855_2_sigma_sign",
            "A draft says sigma_R=sign(G_R) in a chosen Green convention, but it explicitly lacks the quadratic parent action and signature convention.",
            "DRAFT_SIGN_REQUEST_NOT_DERIVED",
            "draft cannot be promoted",
        ),
        (
            "SIGEV2865_10_variational_obstruction",
            "sigma_R",
            "Noether/current identity sign",
            SRC_2856_OBS,
            "OBS2856_4_sign",
            "The amplitude-current identity needs a parent Green sign convention, not a post-hoc choice.",
            "MISSING_SIGMA_R_SIGN_OWNER",
            "blocks sign-stable cancellation",
        ),
        (
            "SIGEV2865_11_origin_demoted",
            "U_amp sigma ratio",
            "parent-origin test",
            SRC_2859_DOC,
            "ORG2859_1_sigma_origin",
            "The U_amp ratio is not parent-owned; the attractive mechanism stays conditional.",
            "NOT_SOURCED",
            "cannot claim theorem-zero or local-GR branch",
        ),
    ]
    rows = []
    for evidence_id, quantity, candidate_type, source_path, source_anchor, evidence, status, missing in specs:
        rows.append(
            add_common(
                {
                    "evidence_id": evidence_id,
                    "quantity": quantity,
                    "candidate_type": candidate_type,
                    "source_path": str(source_path),
                    "source_anchor": source_anchor,
                    "evidence": evidence,
                    "status": status,
                    "missing_for_acceptance": missing,
                    "accepted_source_row": False,
                    "sign_owner_accepted": False,
                    "common_green_owner_accepted": False,
                }
            )
        )
    return rows


def green_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "GREEN2865_0_common_operator_pair",
            "Q_CAB and q_R_eff must be read from operators sharing one exterior radial coefficient convention.",
            "MISSING_PARENT_OPERATOR_PAIR",
            "CONTRACT2844_0_operator plus Q_CAB/q_R_eff source equations remain unsigned",
            False,
        ),
        (
            "GREEN2865_1_deltaR_orientation",
            "delta_R grammar has (-Laplace+ell_R^-2)delta_R=-S_R/Z_R and q_R_eff=-int S_R/Z_R d^3x.",
            "SYMBOLIC_DELTA_R_ORIENTATION_ONLY",
            "parent action/signature/source-density normalization still absent",
            False,
        ),
        (
            "GREEN2865_2_CAB_orientation",
            "C_AB would need a matching L_CAB C_AB=J_CAB convention and boundary/corner flux definition.",
            "MISSING_CAB_OPERATOR_AND_BOUNDARY_OWNER",
            "2863 keeps Q_CAB blocked",
            False,
        ),
        (
            "GREEN2865_3_radial_coefficient",
            "The shared exterior coefficient must define C_AB=Q_CAB/(4*pi*r)+... and delta_R=sigma_R q_R_eff exp(-r/ell_R)/(4*pi*r)+... in the same orientation.",
            "CONDITIONAL_CONVENTION_WRITTEN",
            "formula is usable only after sign/source owner is parent-signed",
            False,
        ),
        (
            "GREEN2865_4_worldtube_measure",
            "Both charges must integrate over the same oriented worldtube/source measure with explicit boundary terms.",
            "MISSING_SHARED_MEASURE_AND_BOUNDARY_SILENCE",
            "charge equality or cancellation cannot be inferred",
            False,
        ),
        (
            "GREEN2865_5_profile_import",
            "sigma_R_profile cannot supply sigma_R_source_sign.",
            "PROFILE_IMPORT_REJECTED",
            "profile/source-sign bridge absent",
            False,
        ),
        (
            "GREEN2865_6_verdict",
            "The common Green convention is not accepted as a parent-owned row.",
            "NOT_ACCEPTED",
            "operator pair, source signs, boundary class and measure are not parent-signed",
            False,
        ),
    ]
    return [
        add_common(
            {
                "green_id": green_id,
                "criterion": criterion,
                "status": status,
                "blocker": blocker,
                "common_green_owner_accepted": accepted,
            }
        )
        for green_id, criterion, status, blocker, accepted in specs
    ]


def profile_rows() -> list[dict[str, Any]]:
    specs = [
        ("PROF2865_0_profile_as_sign", "sigma_R_profile -> sigma_R_source_sign", "REJECT", "2862 explicitly split profile from runner/source sign"),
        ("PROF2865_1_symbol_only", "sigma_R symbol without parent operator/sign owner", "REJECT", "symbol names do not carry orientation or Green convention"),
        ("PROF2865_2_gamma_bound_backsolve", "infer sigma_R from a desired gamma/PPN bound", "REJECT", "would tune the sign from readout rather than derive it"),
        ("PROF2865_3_Uamp_closure_skip", "choose sigma_R only to make U_amp cancellation work", "REJECT", "closure-only unless parent owns the ratio before readout"),
        ("PROF2865_4_placeholder", "MISSING_sigma_R_source_sign placeholder row", "REJECT", "placeholder rows cannot score"),
        ("PROF2865_5_bridge_absent", "sigma_R_profile bridge to source sign", "OPEN_BLOCKER", "no source path derives the bridge"),
    ]
    return [
        add_common(
            {
                "profile_audit_id": audit_id,
                "attempted_import": attempted_import,
                "decision": decision,
                "reason": reason,
                "profile_import_accepted": False,
            }
        )
        for audit_id, attempted_import, decision, reason in specs
    ]


def acceptance_rows() -> list[dict[str, Any]]:
    specs = [
        ("ACC2865_0_parent_action_sign", "parent quadratic action fixes the sign of the R-sector operator", "FAIL", "no parent-signed S_R^(2), metric signature, or operator orientation"),
        ("ACC2865_1_Green_orientation", "Green function convention fixes whether compact source raises or lowers delta_R", "FAIL", "KER2839 gives symbolic orientation but defers observable sign to parent source convention"),
        ("ACC2865_2_common_operator", "Q_CAB and q_R_eff share one exterior Green/radial convention", "FAIL", "Q_CAB and q_R_eff source equations are still blocked"),
        ("ACC2865_3_profile_rejected", "sigma_R_profile is refused as sigma_R_source_sign", "PASS_GUARD_ONLY", "guard works, but it does not create the missing source-sign row"),
        ("ACC2865_4_draft_not_promoted", "PEQ2855_2 draft sign equation can be accepted", "FAIL", "the row is explicitly DRAFT_SIGN_REQUEST_NOT_DERIVED"),
        ("ACC2865_5_A_total_scoring", "A_total=(sigma_R*q_R_eff+Q_CAB)/(4*pi) can be scored", "FAIL", "all three numerator/sign inputs remain source-incomplete"),
        ("ACC2865_6_Uamp_reentry", "U_amp theorem-zero route reopens", "FAIL", "sigma origin and parent quotient/action owner remain unsourced"),
        ("ACC2865_7_runner_ready", "strict local finite runner can score", "FAIL", "Q_CAB, q_R_eff, sigma_R_source_sign, tail, GM and full vector remain blocked"),
    ]
    rows = []
    for acceptance_id, criterion, result, reason in specs:
        rows.append(
            add_common(
                {
                    "acceptance_id": acceptance_id,
                    "criterion": criterion,
                    "result": result,
                    "reason": reason,
                    "gate_passed": False,
                    "guard_passed_nonclaim": result == "PASS_GUARD_ONLY",
                    "runner_ready": False,
                }
            )
        )
    return rows


def blocker_rows() -> list[dict[str, Any]]:
    specs = [
        ("BLOCK2865_0_SIGMA_SIGN", "sigma_R_source_sign", "MISSING_OPERATOR_GREEN_SIGN_OWNER", "derive/source parent kinetic sign, metric signature and Green orientation", "blocks sign-stable A_total and U_amp ratio"),
        ("BLOCK2865_1_COMMON_GREEN", "Q_CAB/q_R_eff", "MISSING_COMMON_GREEN_CONVENTION", "derive common exterior operator/radial coefficient convention", "blocks numerator combination"),
        ("BLOCK2865_2_QCAB_CARRY", "Q_CAB", "MISSING_PARENT_INPUT", "carry 2863 Q_CAB source/zero owner blocker", "blocks A_total numerator"),
        ("BLOCK2865_3_QREFF_CARRY", "q_R_eff", "MISSING_SOURCE_NORMALIZATION", "carry 2864 q_R_eff finite/source normalization blocker", "blocks A_total numerator"),
        ("BLOCK2865_4_PROFILE_BRIDGE", "sigma_R_profile", "MISSING_PROFILE_TO_SOURCE_SIGN_BRIDGE", "derive a bridge if profile is ever to inform the source sign", "blocks profile import"),
        ("BLOCK2865_5_BOUNDARY_MEASURE", "worldtube/boundary", "MISSING_SHARED_MEASURE_AND_BOUNDARY_CLASS", "source boundary/corner terms and oriented measure", "blocks integrated charge identity"),
        ("BLOCK2865_6_PARENT_IDENTITY", "J_CAB+sigma_R J_R", "MISSING_PARENT_CURRENT_IDENTITY", "derive Noether/Bianchi/gauge identity before theorem-zero route", "blocks cancellation theorem"),
        ("BLOCK2865_7_FULL_VECTOR", "local residual vector", "MISSING_FULL_VECTOR_CLOSURE", "derive beta/preferred/source/endpoint/clock/orbital/q_loc channels in one branch", "blocks local-GR/Newton claim"),
        ("BLOCK2865_8_HANDOFF", "parent action contract", "NEXT_CORE_ROLLUP_AFTER_SIGN_BLOCKED", "roll Q_CAB, q_R_eff and sigma blockers into one minimal parent-action/local-amplitude contract", "opens 2866 without scoring"),
    ]
    return [
        add_common(
            {
                "blocker_id": blocker_id,
                "quantity": quantity,
                "blocker_code": code,
                "required_resolution": resolution,
                "blocks": blocks,
                "resolved": False,
            }
        )
        for blocker_id, quantity, code, resolution, blocks in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2865_0_sign_slot", "sigma_R_source_sign remains a real missing row.", "NO_ACCEPTED_SOURCE_SIGN", "there is a clean slot, but no parent action/signature/Green owner"),
        ("DEC2865_1_profile", "sigma_R_profile import is rejected.", "GUARD_CONFIRMED", "profile and source sign are different objects"),
        ("DEC2865_2_common_green", "A shared Green convention can be stated but not claimed.", "CONDITIONAL_ONLY", "same radial coefficient orientation requires parent source equations and boundary policy"),
        ("DEC2865_3_runner", "A_total scoring remains locked.", "LOCKED", "Q_CAB, q_R_eff and sigma_R_source_sign are all open"),
        ("DEC2865_4_next", "Move to core-amplitude blocker rollup and parent-action reentry contract.", "SELECTED_2866", "the next progress is not another local score; it is the exact parent contract that would own all three core rows together"),
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
                "next_id": "NEXT2865_0_2866",
                "status": "selected_primary",
                "target_doc": "2866-Y5-R2FR-core-amplitude-blocker-rollup-and-parent-action-reentry-contract-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_core_amplitude_blocker_rollup_and_parent_action_reentry_contract_under_AX1090_2866.py",
                "mission": "combine Q_CAB, q_R_eff and sigma_R_source_sign blockers into one minimal parent-action/local-amplitude contract; identify whether next progress is parent action synthesis, tail/GM/full-vector acquisition, or finite source rows; keep strict runner blocked until the parent owns the shared convention",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("COPY2865_0_evidence", OUTPUTS["evidence"], BRANCH_OUTPUTS["evidence_copy"], "sigma_R source-sign evidence scan nonclaim copy"),
        ("COPY2865_1_blockers", OUTPUTS["blockers"], BRANCH_OUTPUTS["blocker_copy"], "sigma/common Green blocker ledger nonclaim copy"),
        ("COPY2865_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue handoff to 2866 parent contract"),
        ("COPY2865_3_green", OUTPUTS["green"], BRANCH_OUTPUTS["green_copy"], "common Green convention audit nonclaim copy"),
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
        "accepted_source_row",
        "sign_owner_accepted",
        "common_green_owner_accepted",
        "profile_import_accepted",
        "gate_passed",
        "runner_ready",
        "field_ready",
        "accepted_for_runner",
        "accepted_ready",
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
    checks = [
        ("VAL2865_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all registered source paths exist"),
        ("VAL2865_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all registered anchors were found"),
        ("VAL2865_2_evidence_covers_sigma", len(rows_by_name["evidence"]) >= 10 and any(row["evidence_id"] == "SIGEV2865_0_canonical_source_sign" for row in rows_by_name["evidence"]), "sigma source-sign evidence scan covers canonical/draft/kernel/profile rows"),
        ("VAL2865_3_no_accepted_sign_owner", all(not row["sign_owner_accepted"] for row in rows_by_name["evidence"]), "no parent-owned sigma source sign accepted"),
        ("VAL2865_4_common_green_rejected", any(row["green_id"] == "GREEN2865_6_verdict" and row["status"] == "NOT_ACCEPTED" for row in rows_by_name["green"]), "common Green convention remains unsigned"),
        ("VAL2865_5_profile_import_rejected", all(not row["profile_import_accepted"] for row in rows_by_name["profile"]), "sigma_R_profile is not imported as source sign"),
        ("VAL2865_6_acceptance_gates_fail_closed", all(not row["gate_passed"] for row in rows_by_name["acceptance"]), "all sigma/common-Green acceptance gates fail closed"),
        ("VAL2865_7_QCAB_qReff_carried", any(row["blocker_id"] == "BLOCK2865_2_QCAB_CARRY" for row in rows_by_name["blockers"]) and any(row["blocker_id"] == "BLOCK2865_3_QREFF_CARRY" for row in rows_by_name["blockers"]), "Q_CAB and q_R_eff blockers carried forward"),
        ("VAL2865_8_next_target_2866", rows_by_name["next"][0]["next_id"] == "NEXT2865_0_2866" and "parent-action" in rows_by_name["next"][0]["target_doc"], "core parent-action contract target selected"),
        ("VAL2865_9_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2865_10_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2865_11_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2865_12_cited_paths_exist", cited_paths_exist(rows_by_name), "all cited local file/copy paths in generated rows exist"),
        ("VAL2865_13_no_claim_flags", no_claim_flags(rows_by_name), "no claim/score/prediction flags are true"),
        ("VAL2865_14_generated_under_post_checkpoint", generated_under_root(), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2865_15_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2865_16_pycache_absent", pycache_absent(), "scripts __pycache__ absent during validation"),
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
            "validation_id": "VAL2865_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2865 rejects profile-to-sign import, keeps sigma_R_source_sign/common Green convention unsigned, carries Q_CAB and q_R_eff blockers, and selects a core parent-action/local-amplitude contract for 2866.",
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
        "# 2865 - Y5 R2FR sigma_R Source Sign And Common Green Convention Owner Under AX1090",
        "",
        "Status: `Y5_R2FR_2865_sigma_source_sign_common_green_unsigned_profile_import_rejected`",
        "",
        "## Private Verdict",
        "",
        "2865 tried to close the coupling/sign problem directly: can `sigma_R_source_sign` be derived or sourced, and can `Q_CAB` and `q_R_eff` be put into one shared exterior Green convention?",
        "",
        "The answer is still no-claim, but it is a cleaner no. The formal sign slot is now sharp:",
        "",
        "```text",
        "C_AB(r) = Q_CAB/(4*pi*r) + C_AB_reg(r)",
        "delta_R(r) = sigma_R_source_sign*q_R_eff*exp(-r/ell_R)/(4*pi*r) + H_R(r)",
        "A_total = (Q_CAB + sigma_R_source_sign*q_R_eff)/(4*pi)",
        "```",
        "",
        "That convention is usable as a future contract, but it is not parent-owned yet. The corpus still does not supply the parent quadratic action sign, metric/signature convention, shared operator pair, source-density orientation, or boundary/worldtube measure needed to make the sign physical rather than chosen after the fact.",
        "",
        "`sigma_R_profile` is explicitly rejected as a substitute for `sigma_R_source_sign`. It may be a useful weak-field/profile object later, but without a bridge it cannot decide the source sign in the finite runner.",
        "",
        "So the strict `A_total` score remains locked. This is not a defeat; it identifies the coupling problem as one parent-action contract problem instead of three separate loose ends.",
        "",
        "## Source Register",
        "",
        markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"]),
        "",
        "## sigma_R Source Sign Evidence Scan",
        "",
        markdown_table(rows["evidence"], ["evidence_id", "quantity", "candidate_type", "source_anchor", "status", "missing_for_acceptance", "accepted_source_row", "sign_owner_accepted", "valid_for_claim"]),
        "",
        "## Common Green Convention Audit",
        "",
        markdown_table(rows["green"], ["green_id", "criterion", "status", "blocker", "common_green_owner_accepted", "valid_for_claim"]),
        "",
        "## Profile Import Rejection Audit",
        "",
        markdown_table(rows["profile"], ["profile_audit_id", "attempted_import", "decision", "reason", "profile_import_accepted", "valid_for_claim"]),
        "",
        "## sigma_R Acceptance Gate",
        "",
        markdown_table(rows["acceptance"], ["acceptance_id", "criterion", "result", "reason", "gate_passed", "guard_passed_nonclaim", "runner_ready", "valid_for_claim"]),
        "",
        "## Sign Blocker Ledger",
        "",
        markdown_table(rows["blockers"], ["blocker_id", "quantity", "blocker_code", "required_resolution", "blocks", "resolved", "valid_for_claim"]),
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
    rows["evidence"] = evidence_rows()
    rows["green"] = green_rows()
    rows["profile"] = profile_rows()
    rows["acceptance"] = acceptance_rows()
    rows["blockers"] = blocker_rows()
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "evidence", "green", "profile", "acceptance", "blockers", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])
    remove_pycache()
    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2865_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2865_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()

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

DOC = ROOT / "2866-Y5-R2FR-core-amplitude-blocker-rollup-and-parent-action-reentry-contract-under-AX1090.md"

SRC_2866_SCRIPT = ROOT / "scripts" / "Y5_R2FR_core_amplitude_blocker_rollup_and_parent_action_reentry_contract_under_AX1090_2866.py"
SRC_2865_DOC = ROOT / "2865-Y5-R2FR-sigmaR-source-sign-and-common-Green-convention-owner-under-AX1090.md"
SRC_2865_EVIDENCE = RESIDUALS / "P8_Y5_R2FR_2865_SIGMA_SOURCE_SIGN_EVIDENCE_SCAN.csv"
SRC_2865_GREEN = RESIDUALS / "P8_Y5_R2FR_2865_COMMON_GREEN_CONVENTION_AUDIT.csv"
SRC_2865_BLOCKERS = RESIDUALS / "P8_Y5_R2FR_2865_SIGN_BLOCKER_LEDGER.csv"
SRC_2865_NEXT = RESIDUALS / "P8_Y5_R2FR_2865_NEXT_TARGET.csv"
SRC_2865_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2865_VALIDATION.csv"
SRC_2864_DOC = ROOT / "2864-Y5-R2FR-qReff-first-source-row-or-parent-normalization-owner-under-AX1090.md"
SRC_2864_BLOCKERS = RESIDUALS / "P8_Y5_R2FR_2864_QREFF_BLOCKER_LEDGER.csv"
SRC_2863_DOC = ROOT / "2863-Y5-R2FR-QCAB-first-source-row-or-parent-zero-owner-under-AX1090.md"
SRC_2863_BLOCKERS = RESIDUALS / "P8_Y5_R2FR_2863_QCAB_BLOCKER_LEDGER.csv"
SRC_2859_DOC = ROOT / "2859-Y5-R2FR-Uamp-parent-origin-or-finite-source-fallback-under-AX1090.md"
SRC_2859_QUEUE = RESIDUALS / "P8_Y5_R2FR_2859_FINITE_SOURCE_FALLBACK_QUEUE.csv"
SRC_2858_GATE = RESIDUALS / "P8_Y5_R2FR_2858_CONSISTENCY_GATE_MATRIX.csv"
SRC_2857_OWNER = RESIDUALS / "P8_Y5_R2FR_2857_PARENT_OWNERSHIP_GATE.csv"
SRC_2857_DOC = ROOT / "2857-Y5-R2FR-vertical-generator-source-hunt-or-minimal-action-construction-under-AX1090.md"
SRC_2856_CLAUSES = RESIDUALS / "P8_Y5_R2FR_2856_VARIATIONAL_CLAUSE_AUDIT.csv"
SRC_2856_OBS = RESIDUALS / "P8_Y5_R2FR_2856_OBSTRUCTION_LEDGER.csv"
SRC_2855_DRAFT = RESIDUALS / "P8_Y5_R2FR_2855_PARENT_SOURCE_EQUATION_DRAFT.csv"
SRC_2855_REENTRY = RESIDUALS / "P8_Y5_R2FR_2855_PARENT_ACTION_REENTRY_CONTRACT.csv"
SRC_2851_ANSATZ = RESIDUALS / "P8_Y5_R2FR_2851_COMMON_CURRENT_ANSATZ.csv"
SRC_2851_PROOF = RESIDUALS / "P8_Y5_R2FR_2851_ALGEBRAIC_PROOF_ATTEMPT.csv"
SRC_2851_REQ = RESIDUALS / "P8_Y5_R2FR_2851_PARENT_SIGNATURE_REQUIREMENTS.csv"
SRC_2844_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2844_PARENT_AMPLITUDE_CONTRACT.csv"
SRC_2844_FLUX = RESIDUALS / "P8_Y5_R2FR_2844_CAB_GREEN_FLUX_IDENTITY.csv"
SRC_2839_KERNEL = RESIDUALS / "P8_Y5_R2FR_2839_GREEN_KERNEL_NORMALIZATION.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2866_SOURCE_REGISTER.csv",
    "rollup": RESIDUALS / "P8_Y5_R2FR_2866_CORE_BLOCKER_ROLLUP.csv",
    "contract": RESIDUALS / "P8_Y5_R2FR_2866_MINIMAL_PARENT_ACTION_CONTRACT.csv",
    "variation": RESIDUALS / "P8_Y5_R2FR_2866_VARIATIONAL_DERIVATION_CHECK.csv",
    "reentry": RESIDUALS / "P8_Y5_R2FR_2866_REENTRY_ACCEPTANCE_GATE.csv",
    "routes": RESIDUALS / "P8_Y5_R2FR_2866_ROUTE_DECISION_MATRIX.csv",
    "guards": RESIDUALS / "P8_Y5_R2FR_2866_CLAIM_GUARD.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2866_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2866_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2866_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2866_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "contract_copy": BETA_DOCS / "RAB_CORE_PARENT_ACTION_CONTRACT_2866_NONCLAIM.csv",
    "rollup_copy": SOURCE_WEIGHT / "RAB_CORE_AMPLITUDE_BLOCKER_ROLLUP_2866_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2866_parent_sigma_origin_vertical_generator_NEXT.csv",
    "guard_copy": LOCAL_BOUNDS / "RAB_CORE_LOCAL_GR_CLAIM_GUARD_2866_NONCLAIM.csv",
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
        ("SRC2866_0_2865_doc", SRC_2865_DOC, "NEXT2865_0_2866;VAL2865_OVERALL", "2865 selected core parent-action contract"),
        ("SRC2866_1_2865_evidence", SRC_2865_EVIDENCE, "SIGEV2865_0_canonical_source_sign;SIGEV2865_7_parent_contract;SIGEV2865_9_draft_sign_equation", "sigma source-sign evidence"),
        ("SRC2866_2_2865_green", SRC_2865_GREEN, "GREEN2865_0_common_operator_pair;GREEN2865_6_verdict", "common Green convention audit"),
        ("SRC2866_3_2865_blockers", SRC_2865_BLOCKERS, "BLOCK2865_0_SIGMA_SIGN;BLOCK2865_1_COMMON_GREEN;BLOCK2865_2_QCAB_CARRY;BLOCK2865_3_QREFF_CARRY", "core blocker set"),
        ("SRC2866_4_2865_next", SRC_2865_NEXT, "NEXT2865_0_2866", "handoff target"),
        ("SRC2866_5_2865_validation", SRC_2865_VALIDATION, "VAL2865_OVERALL", "2865 validation"),
        ("SRC2866_6_2864_doc", SRC_2864_DOC, "q_R_eff := - integral_body S_R/Z_R d^3x;NEXT2864_0_2865", "q_R_eff kernel grammar"),
        ("SRC2866_7_2864_blockers", SRC_2864_BLOCKERS, "BLOCK2864_0_q_R_eff_VALUE;BLOCK2864_4_SIGMA_SIGN;BLOCK2864_7_QCAB_CARRY", "q_R_eff blockers"),
        ("SRC2866_8_2863_doc", SRC_2863_DOC, "NEXT2863_0_2864;VAL2863_OVERALL", "Q_CAB source-row attempt"),
        ("SRC2866_9_2863_blockers", SRC_2863_BLOCKERS, "BLOCK2863_0_Q_CAB_PARENT_INPUT;BLOCK2863_6_HANDOFF", "Q_CAB blockers"),
        ("SRC2866_10_2859_doc", SRC_2859_DOC, "ORG2859_1_sigma_origin;DER2859_2_missing_origin;NEXT2859_0_2860", "U_amp origin demotion"),
        ("SRC2866_11_2859_queue", SRC_2859_QUEUE, "FSQ2859_0_Q_CAB;FSQ2859_1_q_R_eff;FSQ2859_2_sigma_R", "finite fallback queue"),
        ("SRC2866_12_2858_gate", SRC_2858_GATE, "GATE2858_1_sigma_owner;GATE2858_6_matter_descent", "U_amp consistency gates"),
        ("SRC2866_13_2857_doc", SRC_2857_DOC, "U_amp = delta_R - sigma_R C_AB;ANS2857_2_quotient_invariant", "minimal amplitude doublet ansatz"),
        ("SRC2866_14_2857_owner", SRC_2857_OWNER, "OWN2857_0_sigma;OWN2857_2_generator;OWN2857_4_boundary", "parent ownership gates"),
        ("SRC2866_15_2856_clauses", SRC_2856_CLAUSES, "CLAUSE2856_1_vertical_generator;CLAUSE2856_3_source_split;CLAUSE2856_4_operator_side", "variational clause audit"),
        ("SRC2866_16_2856_obs", SRC_2856_OBS, "OBS2856_0_generator;OBS2856_1_action;OBS2856_4_sign", "Noether/current identity obstructions"),
        ("SRC2866_17_2855_draft", SRC_2855_DRAFT, "PEQ2855_0_CAB_source;PEQ2855_1_R_source;PEQ2855_2_sigma_sign;PEQ2855_3_amp_current_identity", "parent source equation draft"),
        ("SRC2866_18_2855_reentry", SRC_2855_REENTRY, "RE2855_0_variational_identity;RE2855_1_finite_runner", "reentry conditions"),
        ("SRC2866_19_2851_ansatz", SRC_2851_ANSATZ, "ANS2851_0_general_source_doublet;ANS2851_1_candidate_owner_ratio", "common-current ansatz"),
        ("SRC2866_20_2851_proof", SRC_2851_PROOF, "ALG2851_3_identity;ALG2851_4_no_free_lunch", "algebraic current identity attempt"),
        ("SRC2866_21_2851_req", SRC_2851_REQ, "REQ2851_0_object_language;REQ2851_3_operator_sign", "parent signature requirements"),
        ("SRC2866_22_2844_contract", SRC_2844_CONTRACT, "CONTRACT2844_0_operator;CONTRACT2844_5_sign", "parent amplitude contract"),
        ("SRC2866_23_2844_flux", SRC_2844_FLUX, "FLUX2844_3_deltaR_amplitude;FLUX2844_4_local_ppn_amplitude;FLUX2844_5_local_suppression_condition", "amplitude flux identity"),
        ("SRC2866_24_2839_kernel", SRC_2839_KERNEL, "KER2839_1_normalized_operator;KER2839_3_solution;KER2839_4_compact_body", "R-sector Green kernel"),
        ("SRC2866_25_script", SRC_2866_SCRIPT, "def contract_rows;def variation_rows;def validation_rows", "2866 generator self-check"),
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


def rollup_rows() -> list[dict[str, Any]]:
    specs = [
        ("CORE2866_0_Q_CAB", "Q_CAB", "target-map/source amplitude", "MISSING_PARENT_INPUT", "needs L_CAB C_AB=J_CAB, source current, charge units and boundary/corner policy", "same parent amplitude action and worldtube measure"),
        ("CORE2866_1_q_R_eff", "q_R_eff", "R-sector Green charge", "MISSING_SOURCE_NORMALIZATION", "needs L_R delta_R=J_R, S_R/Z_R normalization, ell_R and boundary class", "same parent amplitude action and Green orientation"),
        ("CORE2866_2_sigma_R_source_sign", "sigma_R_source_sign", "coupling/sign convention", "MISSING_OPERATOR_GREEN_SIGN_OWNER", "needs parent quadratic sign, metric signature and Green orientation", "same parent kinetic/sign convention"),
        ("CORE2866_3_common_Green", "common exterior convention", "shared radial coefficient", "MISSING_COMMON_GREEN_CONVENTION", "needs C_AB and delta_R exterior coefficients in one convention", "same parent operator-pair contract"),
        ("CORE2866_4_boundary_measure", "boundary/worldtube measure", "integrated charge identity", "MISSING_SHARED_MEASURE_AND_BOUNDARY_CLASS", "needs oriented source measure and silent/included boundary terms", "same parent differentiability and boundary theorem"),
        ("CORE2866_5_current_identity", "J_CAB+sigma_R J_R", "theorem-zero route", "MISSING_PARENT_CURRENT_IDENTITY", "needs Noether/Bianchi/gauge identity before cancellation is claimed", "same parent action symmetry"),
        ("CORE2866_6_full_vector", "local residual vector", "GR/Newton reduction guard", "MISSING_FULL_VECTOR_CLOSURE", "needs non-gamma PPN, clock, orbital and q_loc channels", "same physical branch after amplitude contract"),
    ]
    rows = []
    for rollup_id, quantity, role, blocker, missing, common_owner in specs:
        rows.append(
            add_common(
                {
                    "rollup_id": rollup_id,
                    "quantity": quantity,
                    "role": role,
                    "blocker_code": blocker,
                    "missing_evidence": missing,
                    "common_owner_needed": common_owner,
                    "root_cause_group": "PARENT_LOCAL_AMPLITUDE_ACTION_CONTRACT",
                    "resolved": False,
                    "accepted_for_runner": False,
                }
            )
        )
    return rows


def contract_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "PACT2866_0_fields",
            "field content",
            "parent local amplitude fields include C_AB, delta_R, matter/source fields Psi, coframe/metric data theta and boundary data on an oriented worldtube W",
            "defines the objects being varied; prevents Q_CAB/q_R_eff from being sourced in different theories",
            "PARTIAL_SYMBOLIC_CONTRACT",
            "field-by-field parent map q(Phi) and matter lift remain unsigned",
            False,
        ),
        (
            "PACT2866_1_sigma_origin",
            "sign owner",
            "sigma_R_source_sign is fixed by the parent quadratic kinetic/source convention before any A_total or PPN readout",
            "forbids choosing the sign to force cancellation",
            "REQUIRED_OPEN",
            "quadratic action, metric signature and Green orientation not parent-signed",
            False,
        ),
        (
            "PACT2866_2_invariant",
            "minimal invariant",
            "U_amp := delta_R - sigma_R_source_sign*C_AB is the retained amplitude invariant; V_amp is the vertical/quotient direction",
            "if parent-owned, this gives one source current instead of two tuned source currents",
            "CANDIDATE_CONTRACT_NOT_PARENT_OWNED",
            "origin of U_amp and sigma ratio remains unsourced",
            False,
        ),
        (
            "PACT2866_3_action",
            "local amplitude action skeleton",
            "S_amp = 1/2 <U_amp, L_U U_amp> + <J_U, U_amp> + S_boundary[U_amp,W] plus quotient-silent terms",
            "variation yields locked source currents and a common operator convention",
            "DERIVATION_TEMPLATE_ONLY",
            "L_U, J_U, measure, boundary differentiability and matter descent are not sourced",
            False,
        ),
        (
            "PACT2866_4_source_split",
            "source equations",
            "variation must imply J_CAB=-sigma_R_source_sign*J_U and J_R=J_U in the same worldtube measure",
            "would make J_CAB+sigma_R_source_sign*J_R=0 up to boundary/improvement terms",
            "CONDITIONAL_ALGEBRA_VALID",
            "needs parent action provenance before acceptance",
            False,
        ),
        (
            "PACT2866_5_common_Green",
            "exterior Green convention",
            "C_AB=Q_CAB/(4*pi*r)+C_reg and delta_R=sigma_R_source_sign*q_R_eff*exp(-r/ell_R)/(4*pi*r)+H_R use one radial coefficient convention",
            "turns separate rows into a sign-stable A_total numerator",
            "CONDITIONAL_CONVENTION",
            "operator pair, range hierarchy and boundary class not parent-signed",
            False,
        ),
        (
            "PACT2866_6_boundary",
            "integrated charge theorem",
            "surface_integral_boundary(K_amp+B_CAB+sigma_R_source_sign*B_R)=0 or is included as an explicit charge row",
            "prevents hidden tail/boundary terms from faking local GR",
            "REQUIRED_OPEN",
            "boundary/corner silence theorem missing",
            False,
        ),
        (
            "PACT2866_7_matter_readout",
            "Newton/GR readout",
            "ordinary matter and measured GM must couple to quotient/readout variables, not to the vertical representative V_amp",
            "required to reduce to Newton/GR rather than merely cancel gamma",
            "REQUIRED_OPEN",
            "matter descent, source weights and GM glue remain unsigned",
            False,
        ),
        (
            "PACT2866_8_full_vector",
            "local branch closure",
            "after amplitude cancellation, beta/preferred-frame/conservation/clock/orbital/q_loc residuals must be derived in the same branch",
            "prevents gamma-only victory lap",
            "REQUIRED_OPEN",
            "full local residual vector remains missing",
            False,
        ),
        (
            "PACT2866_9_acceptance",
            "acceptance rule",
            "only a source-backed parent action or exact parent theorem can unlock A_total scoring; finite rows are fallback, not derivation",
            "keeps the route derivation-first while preserving empirical fallback",
            "CLAIM_LOCKED",
            "no parent-owned contract accepted in 2866",
            False,
        ),
    ]
    return [
        add_common(
            {
                "contract_id": contract_id,
                "clause": clause,
                "contract_statement": statement,
                "why_needed": why_needed,
                "status": status,
                "missing_for_acceptance": missing,
                "parent_owned": parent_owned,
                "contract_accepted": False,
            }
        )
        for contract_id, clause, statement, why_needed, status, missing, parent_owned in specs
    ]


def variation_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "VAR2866_0_define_U",
            "U_amp := delta_R - sigma_R*C_AB",
            "definition accepted as a conditional candidate",
            "CONDITIONAL_PASS",
            True,
            "sigma_R origin not parent-owned",
        ),
        (
            "VAR2866_1_vertical_generator",
            "v_amp = partial_C + sigma_R*partial_R gives v_amp[U_amp]=0",
            "the quotient-vertical algebra works if sigma_R is fixed first",
            "CONDITIONAL_PASS",
            True,
            "v_amp not proven to be the actual parent vertical generator",
        ),
        (
            "VAR2866_2_source_variation",
            "S_src=<J_U,U_amp> gives J_CAB=-sigma_R*J_U and J_R=J_U",
            "the source split algebraically gives J_CAB+sigma_R*J_R=0",
            "CONDITIONAL_PASS",
            True,
            "J_U, measure and sign convention not sourced",
        ),
        (
            "VAR2866_3_operator_variation",
            "S_kin=1/2<U_amp,L_U U_amp> gives operator equations locked by the same L_U",
            "would prevent independent L_CAB/L_R rescaling",
            "TEMPLATE_PASS_ONLY",
            True,
            "L_U and its relation to exterior Green kernels not parent-signed",
        ),
        (
            "VAR2866_4_integrated_charge",
            "integrating the current identity gives Q_CAB+sigma_R*q_R_eff=boundary/improvement",
            "leading A_total can vanish only if boundary/improvement is zero or included",
            "BOUNDARY_CONDITIONAL",
            True,
            "boundary/corner theorem missing",
        ),
        (
            "VAR2866_5_no_tuning",
            "the ratio in U_amp must be fixed before any PPN/A_total readout",
            "without this, the action is just a designed cancellation",
            "OPEN_GUARD",
            False,
            "timestamp/source hierarchy and parent owner missing",
        ),
        (
            "VAR2866_6_claim_status",
            "the derivation template does not prove local GR or Newton reduction",
            "it identifies the exact parent theorem needed next",
            "NO_CLAIM",
            False,
            "full local residual vector and matter readout remain open",
        ),
    ]
    return [
        add_common(
            {
                "variation_id": variation_id,
                "formal_step": formal_step,
                "result": result,
                "status": status,
                "algebraically_valid": algebraically_valid,
                "missing_for_theorem": missing,
                "parent_signed": False,
                "theorem_claimed": False,
            }
        )
        for variation_id, formal_step, result, status, algebraically_valid, missing in specs
    ]


def reentry_rows() -> list[dict[str, Any]]:
    specs = [
        ("RE2866_0_parent_action", "source-backed parent amplitude action with U_amp fixed before readout", "would reopen theorem-zero route", "OPEN_NOT_ACTIVE", "PACT2866_1 through PACT2866_7 must be parent-owned"),
        ("RE2866_1_sigma_origin", "sigma_R_source_sign derived from parent kinetic/Green convention", "would unlock sign-stable source equations", "OPEN_NOT_ACTIVE", "metric signature, operator sign and Green orientation missing"),
        ("RE2866_2_common_operator", "common L_U/operator-pair convention for C_AB and delta_R", "would unlock shared radial coefficient and A_total grammar", "OPEN_NOT_ACTIVE", "operator pair and boundary class missing"),
        ("RE2866_3_boundary", "boundary/improvement charge zero or explicitly included", "would allow integrated Q identity test", "OPEN_NOT_ACTIVE", "worldtube/corner theorem missing"),
        ("RE2866_4_matter_GM", "matter/readout and GM glue descend to quotient variables", "would connect to Newton/GR source side", "OPEN_NOT_ACTIVE", "matter descent and measured GM source measure missing"),
        ("RE2866_5_finite_rows", "source-backed Q_CAB, q_R_eff, sigma_R, tail, GM and full-vector rows", "would allow strict finite runner without theorem-zero claim", "FALLBACK_OPEN", "finite rows still missing/source-incomplete"),
    ]
    return [
        add_common(
            {
                "reentry_id": reentry_id,
                "trigger": trigger,
                "effect": effect,
                "status": status,
                "required_evidence": required,
                "reentry_active": False,
                "accepted_for_claim": False,
            }
        )
        for reentry_id, trigger, effect, status, required in specs
    ]


def route_rows() -> list[dict[str, Any]]:
    specs = [
        ("ROUTE2866_0_parent_action_synthesis", "derive/source parent amplitude action and sigma origin", 1, "BEST_NEXT_ROUTE", "attacks the common root cause instead of scoring placeholders", False),
        ("ROUTE2866_1_vertical_generator_origin", "derive v_amp from quotient/symplectic map and show Dq[v_amp]=0", 2, "TIGHT_DERIVATION_ROUTE", "needed to make U_amp non-tuned", False),
        ("ROUTE2866_2_boundary_measure", "prove boundary/improvement silence or include explicit boundary charge", 3, "REQUIRED_AFTER_ACTION", "needed before integrated Q identity", False),
        ("ROUTE2866_3_finite_source_acquisition", "supply finite Q_CAB/q_R_eff/sigma/tail/GM/full-vector rows", 4, "EMPIRICAL_FALLBACK", "can test without claiming derivation, but does not solve GR reduction alone", False),
        ("ROUTE2866_4_run_A_total_now", "score A_total with current placeholders", 99, "REJECT", "would be numerology; core rows are unsigned", False),
    ]
    return [
        add_common(
            {
                "route_id": route_id,
                "route": route,
                "rank": rank,
                "decision": decision,
                "reason": reason,
                "selected_for_claim": selected,
                "selected_for_next": route_id == "ROUTE2866_0_parent_action_synthesis",
            }
        )
        for route_id, route, rank, decision, reason, selected in specs
    ]


def guard_rows() -> list[dict[str, Any]]:
    specs = [
        ("GUARD2866_0_no_A_total_score", "do not score A_total", "Q_CAB, q_R_eff and sigma_R_source_sign remain unsigned", "ACTIVE"),
        ("GUARD2866_1_no_profile_import", "do not import sigma_R_profile as source sign", "profile/source-sign bridge absent", "ACTIVE"),
        ("GUARD2866_2_no_theorem_zero", "do not claim Q_CAB+sigma_R*q_R_eff=0", "parent action, sign and boundary theorem missing", "ACTIVE"),
        ("GUARD2866_3_no_local_GR", "do not claim local-GR/Newton reduction", "full residual vector and matter/GM readout not closed", "ACTIVE"),
        ("GUARD2866_4_no_finite_runner", "do not run strict finite runner as evidence", "finite/source rows remain placeholders", "ACTIVE"),
    ]
    return [
        add_common(
            {
                "guard_id": guard_id,
                "guard": guard,
                "reason": reason,
                "status": status,
                "guard_active": True,
                "claim_prevented": True,
            }
        )
        for guard_id, guard, reason, status in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2866_0_root_cause", "Treat Q_CAB, q_R_eff and sigma_R_source_sign as one parent-action problem.", "ACCEPTED_PRIVATE_STRUCTURE", "all three rows require the same sign/operator/source/boundary owner"),
        ("DEC2866_1_contract", "Use U_amp=delta_R-sigma_R*C_AB as the minimal candidate parent invariant.", "CONDITIONAL_BEST_ROUTE", "it algebraically locks source currents without independent rescaling"),
        ("DEC2866_2_no_claim", "Do not claim theorem-zero/local-GR from the contract.", "CLAIM_REJECTED", "the contract is a template, not source-backed parent action"),
        ("DEC2866_3_fallback", "Keep finite source rows as empirical fallback only.", "FALLBACK_RETAINED", "testing can proceed later, but derivation remains the main route"),
        ("DEC2866_4_next", "Attack the parent sigma origin and vertical generator next.", "SELECTED_2867", "this is the first clause that decides whether the route is derivation or closure-only"),
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
                "next_id": "NEXT2866_0_2867",
                "status": "selected_primary",
                "target_doc": "2867-Y5-R2FR-parent-sigma-origin-and-vertical-generator-derivation-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_parent_sigma_origin_and_vertical_generator_derivation_under_AX1090_2867.py",
                "mission": "try to derive sigma_R_source_sign and v_amp=partial_C+sigma_R partial_R from the parent quadratic action, quotient map, or symplectic/DCdagger generator before any A_total readout; if this fails, mark the U_amp parent-action route as closure-only and route to finite source acquisition",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("COPY2866_0_contract", OUTPUTS["contract"], BRANCH_OUTPUTS["contract_copy"], "minimal parent action contract nonclaim copy"),
        ("COPY2866_1_rollup", OUTPUTS["rollup"], BRANCH_OUTPUTS["rollup_copy"], "core amplitude blocker rollup nonclaim copy"),
        ("COPY2866_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue handoff to 2867"),
        ("COPY2866_3_guard", OUTPUTS["guards"], BRANCH_OUTPUTS["guard_copy"], "local-GR claim guard nonclaim copy"),
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
        "accepted_for_runner",
        "contract_accepted",
        "parent_owned",
        "parent_signed",
        "theorem_claimed",
        "reentry_active",
        "accepted_for_claim",
        "selected_for_claim",
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
        ("VAL2866_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all registered source paths exist"),
        ("VAL2866_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all registered anchors were found"),
        ("VAL2866_2_rollup_core_rows", len(rows_by_name["rollup"]) >= 7 and all(any(row["quantity"] == quantity for row in rows_by_name["rollup"]) for quantity in ["Q_CAB", "q_R_eff", "sigma_R_source_sign"]), "core blocker rollup covers Q_CAB, q_R_eff and sigma_R_source_sign"),
        ("VAL2866_3_contract_has_parent_clauses", len(rows_by_name["contract"]) >= 10 and any(row["contract_id"] == "PACT2866_3_action" for row in rows_by_name["contract"]), "minimal parent action contract written"),
        ("VAL2866_4_variation_conditional_only", any(row["variation_id"] == "VAR2866_2_source_variation" and row["algebraically_valid"] for row in rows_by_name["variation"]) and all(not row["theorem_claimed"] for row in rows_by_name["variation"]), "variation algebra is conditional and no theorem is claimed"),
        ("VAL2866_5_reentry_closed", all(not row["reentry_active"] for row in rows_by_name["reentry"]), "reentry gates remain inactive"),
        ("VAL2866_6_best_route_parent_action", any(row["route_id"] == "ROUTE2866_0_parent_action_synthesis" and row["selected_for_next"] for row in rows_by_name["routes"]), "parent-action synthesis selected over placeholder scoring"),
        ("VAL2866_7_claim_guards_active", all(row["guard_active"] for row in rows_by_name["guards"]), "local-GR/A_total/theorem-zero claim guards are active"),
        ("VAL2866_8_next_target_2867", rows_by_name["next"][0]["next_id"] == "NEXT2866_0_2867" and "sigma_origin" in rows_by_name["next"][0]["target_script"], "sigma-origin/vertical-generator derivation selected next"),
        ("VAL2866_9_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2866_10_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2866_11_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2866_12_cited_paths_exist", cited_paths_exist(rows_by_name), "all cited local file/copy paths in generated rows exist"),
        ("VAL2866_13_no_claim_flags", no_claim_flags(rows_by_name), "no claim/score/prediction flags are true"),
        ("VAL2866_14_generated_under_post_checkpoint", generated_under_root(), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2866_15_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2866_16_pycache_absent", pycache_absent(), "scripts __pycache__ absent during validation"),
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
            "validation_id": "VAL2866_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2866 rolls Q_CAB, q_R_eff and sigma_R_source_sign into one parent local-amplitude action contract, proves only conditional algebra, keeps all claim gates closed, and selects sigma-origin/vertical-generator derivation for 2867.",
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
        "# 2866 - Y5 R2FR Core Amplitude Blocker Rollup And Parent Action Reentry Contract Under AX1090",
        "",
        "Status: `Y5_R2FR_2866_core_amplitude_parent_contract_written_conditional_no_claim`",
        "",
        "## Private Verdict",
        "",
        "2866 converts the apparent three-row mess into one parent-action problem.",
        "",
        "`Q_CAB`, `q_R_eff`, and `sigma_R_source_sign` should not be hunted as independent knobs. The clean route is a single local amplitude contract where the parent action owns the field split, sign, source measure, Green convention, and boundary terms before any local readout.",
        "",
        "The minimal candidate is:",
        "",
        "```text",
        "U_amp := delta_R - sigma_R_source_sign*C_AB",
        "S_amp = 1/2 <U_amp, L_U U_amp> + <J_U, U_amp> + S_boundary[U_amp,W]",
        "v_amp = partial_C + sigma_R_source_sign*partial_R",
        "```",
        "",
        "If that is parent-owned, the source split follows without tuning:",
        "",
        "```text",
        "J_CAB = -sigma_R_source_sign*J_U",
        "J_R = J_U",
        "J_CAB + sigma_R_source_sign*J_R = 0",
        "Q_CAB + sigma_R_source_sign*q_R_eff = boundary/improvement",
        "```",
        "",
        "That is the leap-forward path. But 2866 does not claim the theorem, because the parent has not yet signed the sigma origin, quotient vertical generator, operator pair, boundary theorem, matter/GM readout, or full local residual vector.",
        "",
        "So the local-GR/Newton route is alive but not won. The next target is the first hard clause: derive `sigma_R_source_sign` and `v_amp` from the parent quadratic action, quotient map, or `DCdagger`/symplectic generator before any `A_total` readout.",
        "",
        "## Source Register",
        "",
        markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"]),
        "",
        "## Core Blocker Rollup",
        "",
        markdown_table(rows["rollup"], ["rollup_id", "quantity", "role", "blocker_code", "missing_evidence", "common_owner_needed", "resolved", "accepted_for_runner", "valid_for_claim"]),
        "",
        "## Minimal Parent Action Contract",
        "",
        markdown_table(rows["contract"], ["contract_id", "clause", "contract_statement", "status", "missing_for_acceptance", "parent_owned", "contract_accepted", "valid_for_claim"]),
        "",
        "## Variational Derivation Check",
        "",
        markdown_table(rows["variation"], ["variation_id", "formal_step", "result", "status", "algebraically_valid", "missing_for_theorem", "parent_signed", "theorem_claimed", "valid_for_claim"]),
        "",
        "## Reentry Acceptance Gate",
        "",
        markdown_table(rows["reentry"], ["reentry_id", "trigger", "effect", "status", "required_evidence", "reentry_active", "accepted_for_claim", "valid_for_claim"]),
        "",
        "## Route Decision Matrix",
        "",
        markdown_table(rows["routes"], ["route_id", "route", "rank", "decision", "reason", "selected_for_next", "selected_for_claim", "valid_for_claim"]),
        "",
        "## Claim Guard",
        "",
        markdown_table(rows["guards"], ["guard_id", "guard", "reason", "status", "guard_active", "claim_prevented", "valid_for_claim"]),
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
    rows["rollup"] = rollup_rows()
    rows["contract"] = contract_rows()
    rows["variation"] = variation_rows()
    rows["reentry"] = reentry_rows()
    rows["routes"] = route_rows()
    rows["guards"] = guard_rows()
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "rollup", "contract", "variation", "reentry", "routes", "guards", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])
    remove_pycache()
    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2866_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2866_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()

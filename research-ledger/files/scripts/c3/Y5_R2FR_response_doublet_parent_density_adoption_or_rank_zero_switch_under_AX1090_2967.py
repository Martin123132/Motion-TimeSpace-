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
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_SOURCE = ROOT / "source-intake" / "beta-source" / "docs"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2967"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2967-Y5-R2FR-response-doublet-parent-density-adoption-or-rank-zero-switch-under-AX1090.md"

SRC_2966_DOC = ROOT / "2966-Y5-R2FR-ZX-fX-field-metric-source-pack-or-NXhat-prior-runner-under-AX1090.md"
SRC_2966_NEXT = RESIDUALS / "P8_Y5_R2FR_2966_NEXT_TARGET.csv"
SRC_2966_ROUTE = RESIDUALS / "P8_Y5_R2FR_2966_PARENT_METRIC_ROUTE_TRIAGE.csv"
SRC_2966_PACK = RESIDUALS / "P8_Y5_R2FR_2966_ZX_FX_FIELD_METRIC_SOURCE_PACK_GATE.csv"
SRC_2966_DERIVATION = RESIDUALS / "P8_Y5_R2FR_2966_CONDITIONAL_DERIVATION_LEDGER.csv"
SRC_2966_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2966_VALIDATION.csv"
SRC_2217_RDP = BETA_SOURCE / "PARENT_QLOC_RESPONSE_DOUBLET_DENSITY_2217_NONCLAIM.csv"
SRC_2211_ZM = BETA_SOURCE / "PARENT_QLOC_ZM_OWNER_AUDIT_2211_NONCLAIM.csv"
SRC_2213_RANK_ZERO = BETA_SOURCE / "PARENT_QLOC_RANK_ZERO_SOURCE_CURRENT_2213_NONCLAIM.csv"
SRC_2206_WARD = BETA_SOURCE / "PARENT_QLOC_WARD_IDENTITY_2206_NONCLAIM.csv"
SRC_2807_FORCE = BETA_SOURCE / "PARENT_VARIATION_FORCE_SEED_2807_NONCLAIM.csv"
SRC_2799_ACTION = BETA_SOURCE / "GK_QLOC_ACTION_EXISTENCE_2799_NONCLAIM.csv"
SRC_2800_RDBOUND = BETA_SOURCE / "RESPONSE_DOUBLET_QLOC_BOUND_2800_NONCLAIM.csv"
SRC_2808_RESPONSE = RESIDUALS / "P8_Y5_R2FR_2808_METRIC_RESPONSE_DERIVATION_ATTEMPT.csv"
SRC_2808_UNITS = RESIDUALS / "P8_Y5_R2FR_2808_WARD_RESIDUAL_UNIT_CONTRACT.csv"
SRC_2815_KMETRIC = BETA_SOURCE / "KMETRIC_HILBERT_SIGN_DERIVATION_2815_NONCLAIM.csv"
SRC_2809_DELTAK = BETA_SOURCE / "DELTAK_COMPONENT_BOUND_2809_NONCLAIM.csv"
SRC_2812_QDELTAK = BETA_SOURCE / "CPLOC_CCOMM_QDELTAK_BOUND_2812_NONCLAIM.csv"
SRC_2733_BOUND = LOCAL_BOUNDS / "Khat_q_loc_residual_bound_2733_NONCLAIM.csv"
SRC_2699_VECTOR = LOCAL_BOUNDS / "GammaKhat_q_loc_official_residual_vector_2699_NONCLAIM.csv"
SRC_2912_CONSTRAINT = PARENT_ACTION / "Constraint_first_Z_elimination_2912_NONCLAIM.csv"
SRC_2798_SECTOR = BETA_SOURCE / "SECTOR_CERTIFICATE_PACK_2798_NONCLAIM.csv"
SRC_2940_SECTOR = PARENT_ACTION / "Sector_certificate_matrix_2940_NONCLAIM.csv"
SRC_2892_NEUTRAL = SOURCE_WEIGHT / "RAB_PARENT_ACTION_SOURCE_NEUTRALITY_SCHEMA_2892_NONCLAIM.csv"
SRC_516_TRIGGER = RESIDUALS / "P8_QLOC_BOUND_TRIGGER_LEDGER.csv"
SRC_516_SPEC = RESIDUALS / "P8_QLOC_BOUND_RUNNER_SPEC.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2967_SOURCE_REGISTER.csv",
    "adoption": RESIDUALS / "P8_Y5_R2FR_2967_RESPONSE_DOUBLET_ADOPTION_GATE.csv",
    "kinetic": RESIDUALS / "P8_Y5_R2FR_2967_KINETIC_PRINCIPAL_SYMBOL_AUDIT.csv",
    "rank_zero": RESIDUALS / "P8_Y5_R2FR_2967_RANK_ZERO_SWITCH_GATE.csv",
    "residual_pack": RESIDUALS / "P8_Y5_R2FR_2967_RANK_ZERO_RESIDUAL_PACK_REQUIREMENTS.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2967_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2967_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2967_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2967_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2967_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "adoption_copy": PARENT_ACTION / "response_doublet_parent_density_adoption_2967_NOT_PROMOTED.csv",
    "rank_zero_copy": LOCAL_BOUNDS / "rank_zero_algebraic_switch_2967_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2967_RANK_ZERO_RESIDUAL_PACK_NEXT_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv_rows(path)
        return True
    except Exception:
        return False


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": RUN_UTC,
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    selected = columns or list(rows[0].keys())
    header = "| " + " | ".join(selected) + " |"
    separator = "| " + " | ".join("---" for _ in selected) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in selected) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2967_00_2966_doc", SRC_2966_DOC, "NEXT2966_0_2967;response-doublet", "2966 handoff"),
        ("SRC2967_01_2966_next", SRC_2966_NEXT, "NEXT2966_0_2967", "machine-readable 2967 target"),
        ("SRC2967_02_2966_route", SRC_2966_ROUTE, "ROUTE2966_0_response_doublet;ROUTE2966_3_rank_zero", "route triage input"),
        ("SRC2967_03_2966_pack", SRC_2966_PACK, "PACK2966_7_verdict", "source-pack blocker"),
        ("SRC2967_04_2966_derivation", SRC_2966_DERIVATION, "DER2966_2_metric_amplitude_invariant;DER2966_4_schur_guard", "conditional derivation input"),
        ("SRC2967_05_2966_validation", SRC_2966_VALIDATION, "VAL2966_OVERALL", "2966 validation"),
        ("SRC2967_06_2217_RDP", SRC_2217_RDP, "RDP2217_0_parent_action_ansatz;RDP2217_3_Hessian_owner;RDP2217_4_density_verdict", "response-doublet density candidate"),
        ("SRC2967_07_2211_ZM", SRC_2211_ZM, "ZMO2211_2_Z_kinetic_principal_symbol;ZMO2211_5_verdict", "kinetic/principal-symbol audit"),
        ("SRC2967_08_2213_rank_zero", SRC_2213_RANK_ZERO, "RZS2213_0_strict_euler_identity;RZS2213_2_rank_zero_silence_theorem;RZS2213_4_verdict", "rank-zero theorem skeleton"),
        ("SRC2967_09_2206_Ward", SRC_2206_WARD, "WID2206_0_define_stress;WID2206_4_current_verdict", "Ward/stress route"),
        ("SRC2967_10_2807_force", SRC_2807_FORCE, "GKM2807_0_metric_response_identity;GKM2807_3_verdict", "Gamma/Khat force seed"),
        ("SRC2967_11_2799_action", SRC_2799_ACTION, "GKT2799_1_metric_response_identity;GKT2799_6_verdict", "GK action existence"),
        ("SRC2967_12_2800_bound", SRC_2800_RDBOUND, "RDT2800_5_positive_operator;RDT2800_7_verdict", "response-doublet bound theorem"),
        ("SRC2967_13_2808_response", SRC_2808_RESPONSE, "MRD2808_2_divergence_identity;MRD2808_5_current_symbol_match;MRD2808_6_verdict", "metric-response derivation"),
        ("SRC2967_14_2808_units", SRC_2808_UNITS, "UNIT2808_0_Gamma;UNIT2808_4_DeltaK", "Ward residual units"),
        ("SRC2967_15_2815_Kmetric", SRC_2815_KMETRIC, "KHS2815_0_stress_split;KHS2815_3_export_blocker", "Kmetric sign convention"),
        ("SRC2967_16_2809_DeltaK", SRC_2809_DELTAK, "DKB2809_0_DeltaK00;DKB2809_6_envelope", "Delta_K component rows"),
        ("SRC2967_17_2812_QDelta", SRC_2812_QDELTAK, "QBR2812_1_finite_bound_branch;QBR2812_3_score_gate", "q_DeltaK bound interface"),
        ("SRC2967_18_2733_bound", SRC_2733_BOUND, "QB2733_0_vector_envelope;QB2733_3_verdict", "q_loc residual bound"),
        ("SRC2967_19_2699_vector", SRC_2699_VECTOR, "QLOC2699_0_q_loc_vector;QLOC2699_7_total", "official q_loc residual vector"),
        ("SRC2967_20_2912_constraint", SRC_2912_CONSTRAINT, "CFP2912_4_rank_zero_algebraic;CFP2912_5_current_verdict", "constraint/rank-zero gate"),
        ("SRC2967_21_2798_sector", SRC_2798_SECTOR, "SEC2798_3_Gamma_Khat_q_loc;SEC2798_8_total", "sector certificate pack"),
        ("SRC2967_22_2940_sector", SRC_2940_SECTOR, "SEC2940_3_GK_q_loc;SEC2940_9_total", "sector certificate matrix"),
        ("SRC2967_23_2892_neutral", SRC_2892_NEUTRAL, "PAS2892_2_no_pole_parent;PAS2892_5_result", "no-pole source-neutral schema"),
        ("SRC2967_24_516_trigger", SRC_516_TRIGGER, "BT517_0_owner_match_fails;BT517_4_PPN_lock_missing", "q_loc bound triggers"),
        ("SRC2967_25_516_spec", SRC_516_SPEC, "QB516_3_PPN_metric_tail;QB516_4_R11_operator", "q_loc bound runner spec"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, source_path, anchors, role in specs:
        found, missing = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_type": "local_file",
                    "source_path": str(source_path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": source_path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def adoption_gate_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "RDA2967_0_density_ansatz",
            "response-doublet parent density",
            "S_GK=-int sqrt(-g) Gamma_eff with Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B+O(Z^4)",
            "CANDIDATE_WRITTEN_NOT_PARENT_SIGNED",
            "2217 writes the clean candidate, but not its parent adoption signature",
            True,
            False,
        ),
        (
            "RDA2967_1_double_zero",
            "double-zero skeleton",
            "exchange-even response doublets remove the linear Z term and give a Hessian candidate M_AB",
            "CONDITIONAL_DOUBLE_ZERO_ONLY",
            "good local theorem shape, but exchange symmetry is not signed for all source/readout channels",
            True,
            False,
        ),
        (
            "RDA2967_2_Khat_match",
            "K_hat=K_metric[Gamma_eff]",
            "current K_hat equals the Hilbert/metric response of the same Gamma_eff density",
            "MISSING_COMPONENT_MATCH",
            "2808 derives the obstruction identity; 2799/2807 keep the symbol match missing",
            True,
            False,
        ),
        (
            "RDA2967_3_Helmholtz",
            "variational integrability",
            "T_GK second metric variation is symmetric up to allowed boundary terms",
            "NOT_CHECKED_CURRENT_CLAIM",
            "without Helmholtz, the stress route can be bookkeeping rather than action-derived",
            False,
            False,
        ),
        (
            "RDA2967_4_units_domain",
            "units/domain/boundary convention",
            "Gamma_eff, K_metric, q_loc, domain D and boundary subtraction use one declared convention",
            "PARTIAL_UNIT_CONTRACT_ONLY",
            "2808 has units for the metric-response identity but not parent-signed domain/boundary",
            True,
            False,
        ),
        (
            "RDA2967_5_source_boundary_silence",
            "source/current/boundary silence",
            "matter, source, boundary, projector and readout terms are zero/proper or carried as residual rows",
            "NOT_DERIVED",
            "2800, 2206 and 2799 keep J_Z, B_Z, P_loc and boundary no-flux open",
            False,
            False,
        ),
        (
            "RDA2967_6_PPN_WEP_lock",
            "Z^A observable lock",
            "Z variables equal the physical q_loc/PPN/WEP/source-normalization residual vector or are projected with a sourced map",
            "NOT_DERIVED",
            "2800 and 516 explicitly block local-GR inheritance when the observable projection is missing",
            False,
            False,
        ),
        (
            "RDA2967_7_verdict",
            "response-doublet parent-density promotion",
            "RDA2967_0 through RDA2967_6 all close",
            "RESPONSE_DOUBLET_NOT_PARENT_PROMOTED",
            "keep as a strong conditional skeleton only; no local-GR/R10/PPN claim",
            False,
            False,
        ),
    ]
    return [
        add_common(
            {
                "adoption_id": adoption_id,
                "object": obj,
                "required_statement": statement,
                "current_status": status,
                "evidence_summary": evidence,
                "conditional_math_available": conditional,
                "parent_adopted": adopted,
            }
        )
        for adoption_id, obj, statement, status, evidence, conditional, adopted in rows
    ]


def kinetic_audit_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "KIN2967_0_Hessian",
            "M_AB / H_AB",
            "response-doublet Gamma_eff supplies an algebraic Hessian candidate at Z=0",
            "ALGEBRAIC_HESSIAN_CANDIDATE_ONLY",
            "usable for rank-zero algebraic elimination if parent-owned",
            True,
            False,
        ),
        (
            "KIN2967_1_ZAB",
            "Z_AB kinetic/principal symbol",
            "same parent branch contains a gradient/principal-symbol term giving -Z_AB Delta in the static operator",
            "NOT_FOUND_CURRENT_CLAIM",
            "without Z_AB there is no sourced lambda_i and no finite-range/Yukawa alpha row",
            False,
            False,
        ),
        (
            "KIN2967_2_Khat_route",
            "Khat metric-response route",
            "Khat/Gamma variation could in principle induce derivative/operator terms",
            "BLOCKED_BY_DELTA_K_AND_QCDB",
            "Delta_K components and CDB/domain/boundary leaks remain explicit residuals",
            True,
            False,
        ),
        (
            "KIN2967_3_positive_operator",
            "positive L_AB",
            "positive operator theorem for the response doublet",
            "FORMAL_CANDIDATE_ONLY",
            "2800 cannot activate positivity without J_Z and B_Z zeros",
            True,
            False,
        ),
        (
            "KIN2967_4_lambda",
            "lambda_i / finite range",
            "lambda_i=1/mu_i from a parent-owned principal symbol and Hessian eigenproblem",
            "FINITE_RANGE_REJECTED_CURRENT_CORPUS",
            "M_AB exists only as algebraic candidate and Z_AB is absent",
            False,
            False,
        ),
        (
            "KIN2967_5_verdict",
            "kinetic branch",
            "claim-grade finite-range response-doublet branch",
            "NO_KINETIC_BRANCH_PROMOTION",
            "switch to rank-zero algebraic residual pack unless a future principal symbol source appears",
            False,
            False,
        ),
    ]
    return [
        add_common(
            {
                "kinetic_id": kinetic_id,
                "object": obj,
                "required_statement": statement,
                "current_status": status,
                "evidence_summary": evidence,
                "conditional_math_available": conditional,
                "kinetic_branch_acquired": acquired,
            }
        )
        for kinetic_id, obj, statement, status, evidence, conditional, acquired in rows
    ]


def rank_zero_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "RZ2967_0_switch_condition",
            "no Z_AB principal symbol",
            "if the response-doublet branch remains algebraic, do not invent a finite range; use algebraic Euler balance",
            "SWITCH_CONDITION_MET_FOR_CURRENT_CORPUS",
            "2211 says Z_AB is not found and 2213 gives the algebraic normal form",
            True,
            False,
        ),
        (
            "RZ2967_1_algebraic_balance",
            "M_AB Z^B=J_A+B_A+C_A^CDB+R_A",
            "rank-zero local coordinate is solved by algebraic source/boundary/readout forcing",
            "EXACT_CONDITIONAL_NORMAL_FORM",
            "this is a better GR-reduction route than a fake Yukawa branch",
            True,
            False,
        ),
        (
            "RZ2967_2_silence_theorem",
            "Z^A=0 local invisibility",
            "if M_AB invertible and all forcing terms vanish/properly project out, then observed local residuals vanish",
            "CONDITIONAL_THEOREM_WRITTEN",
            "would be a genuine local-GR route, but current source/boundary/descent clauses do not close",
            True,
            False,
        ),
        (
            "RZ2967_3_residual_retention",
            "R_alg residual pack",
            "until silence clauses close, retain absolute residual rows for J_A, B_A, CDB, source/readout/projector and arena maps",
            "RESIDUAL_PACK_REQUIRED",
            "no cancellation or post-readout calibration allowed",
            True,
            False,
        ),
        (
            "RZ2967_4_verdict",
            "rank-zero switch",
            "finite-range route demoted and rank-zero residual pack becomes the next local-GR derivation target",
            "RANK_ZERO_SWITCH_SELECTED_NONCLAIM",
            "selected as next work path, not as local-GR proof",
            True,
            False,
        ),
    ]
    return [
        add_common(
            {
                "rank_zero_id": rank_id,
                "object": obj,
                "statement": statement,
                "current_status": status,
                "evidence_summary": evidence,
                "conditional_math_available": conditional,
                "theorem_zero_adopted": adopted,
            }
        )
        for rank_id, obj, statement, status, evidence, conditional, adopted in rows
    ]


def residual_pack_rows() -> list[dict[str, Any]]:
    source_paths = ";".join(str(path) for path in [SRC_2213_RANK_ZERO, SRC_2912_CONSTRAINT, SRC_2699_VECTOR, SRC_2733_BOUND, SRC_2809_DELTAK, SRC_2812_QDELTAK, SRC_516_SPEC])
    rows = [
        ("ALG2967_0_MAB_signature", "M_AB signature/invertibility", "parent-owned positive/invertible algebraic Hessian on physical quotient", "MISSING_PARENT_SIGNATURE", "mass_matrix_or_dimensionless_operator"),
        ("ALG2967_1_JA_source", "J_A", "ordinary matter/source-current forcing in Z direction", "MISSING_SOURCE_ZERO_OR_BOUND", "force_or_action_derivative"),
        ("ALG2967_2_BA_boundary", "B_A", "boundary/symplectic/corner forcing", "MISSING_BOUNDARY_ZERO_OR_BOUND", "force_or_boundary_flux"),
        ("ALG2967_3_CDB", "C_A^CDB", "connection/domain/bulk defect forcing", "MISSING_CDB_ZERO_OR_BOUND", "force_density"),
        ("ALG2967_4_R_src_readout_projector", "R_A^src/readout/projector", "source normalization, readout and projector residual forcing", "MISSING_READOUT_PROJECTOR_MAP", "arena_normalized_vector"),
        ("ALG2967_5_DqZ", "Dq_Z_norm", "observed quotient derivative in the Z direction", "MISSING_DQZ_ZERO_OR_BOUND", "dimensionless_or_operator_norm"),
        ("ALG2967_6_arena_projection", "Pi_arena[R_alg]", "map algebraic residual into PPN/R10/clock/orbital/WEP vectors", "MISSING_ARENA_PROJECTION", "arena_units"),
        ("ALG2967_7_total", "R_alg_abs_total", "absolute no-cancellation envelope over rank-zero algebraic residuals", "NONCLAIM_SOURCE_PACK_REQUIRED", "arena_normalized_vector"),
    ]
    return [
        add_common(
            {
                "requirement_id": req_id,
                "symbol": symbol,
                "required_payload": payload,
                "current_status": status,
                "units": units,
                "source_path": source_paths,
                "source_path_exists": all(Path(path).exists() for path in source_paths.split(";")),
                "accepted_for_scoring": False,
                "no_cancellation_policy": True,
            }
        )
        for req_id, symbol, payload, status, units in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2967_0_response_doublet", "response-doublet density parent-promoted", False, "RESPONSE_DOUBLET_NOT_PARENT_PROMOTED"),
        ("CG2967_1_kinetic", "Z_AB kinetic/principal symbol acquired", False, "NO_KINETIC_BRANCH_PROMOTION"),
        ("CG2967_2_finite_range", "finite-range lambda/Yukawa branch allowed", False, "FINITE_RANGE_REJECTED_CURRENT_CORPUS"),
        ("CG2967_3_rank_zero_zero", "rank-zero theorem-zero local silence claimed", False, "RANK_ZERO_RESIDUALS_OPEN"),
        ("CG2967_4_residual_pack", "rank-zero residual pack score-ready", False, "RESIDUAL_PACK_REQUIRED"),
        ("CG2967_5_local_tests", "R10/PPN/clock/orbital scoring allowed", False, "LOCAL_TEST_CLAIMS_BLOCKED"),
        ("CG2967_6_GR_Newton", "derived local GR/Newton reduction claimed", False, "NO_LOCAL_GR_OR_NEWTON_CLAIM"),
    ]
    return [
        add_common(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "condition_passed": passed,
                "status": status,
            }
        )
        for gate_id, claim, passed, status in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC2967_0_response_doublet",
            "response-doublet remains conditional skeleton",
            "the density and double-zero idea are useful, but parent adoption and Khat matching fail",
            "do not promote response-doublet density",
        ),
        (
            "DEC2967_1_kinetic",
            "finite-range branch rejected for current corpus",
            "no parent-signed Z_AB principal symbol exists, so lambda/Yukawa language would be invented",
            "do not score R10 alpha from this branch",
        ),
        (
            "DEC2967_2_rank_zero",
            "rank-zero algebraic switch selected",
            "M_AB exists as an algebraic Hessian candidate and 2213 gives the right Euler balance",
            "build the algebraic residual coefficient pack next",
        ),
        (
            "DEC2967_3_local_GR",
            "local GR route is still alive but not claimable",
            "if the residual pack zeros by descent/source/boundary/readout, local silence can be derived without a plateau axiom",
            "try to close or bound J_A, B_A, CDB, Dq_Z and arena projections",
        ),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": action,
            }
        )
        for decision_id, decision, because, action in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2967_0_2968",
                "priority": "selected_primary",
                "next_doc": "2968-Y5-R2FR-rank-zero-algebraic-residual-pack-or-source-silence-proof-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_rank_zero_algebraic_residual_pack_or_source_silence_proof_under_AX1090_2968.py",
                "objective": "Build the rank-zero algebraic residual coefficient pack M_AB Z^B=J_A+B_A+C_A^CDB+R_A, then try to theorem-zero or bound each source, boundary, CDB, Dq_Z and arena projection term without claiming local GR.",
                "include": "M_AB signature;J_A;B_A;C_A^CDB;R_src/readout/projector;Dq_Z;source-current descent;boundary no-flux;arena projections;absolute residual envelope",
                "exclude": "finite-range lambda claim;R10 alpha claim;PPN claim;clock/orbital claim;local-GR claim;GitHub action;formalization-workbench edits;post-readout cancellation;plateau axiom",
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = [
        ("adoption_copy", OUTPUTS["adoption"], BRANCH_OUTPUTS["adoption_copy"]),
        ("rank_zero_copy", OUTPUTS["rank_zero"], BRANCH_OUTPUTS["rank_zero_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copies:
        shutil.copyfile(source, target)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source),
                    "copy_path": str(target),
                    "source_exists": source.exists(),
                    "copy_exists": target.exists(),
                }
            )
        )
    return rows


def validation_rows(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = all_rows["sources"]
    generated_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
    csv_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values())
    checks = [
        ("VAL2967_0_sources_exist", all(row["path_exists"] for row in source_rows), "all cited local source paths exist", True),
        ("VAL2967_1_anchors_found", all(row["anchors_found"] for row in source_rows), "all cited source anchors found", True),
        ("VAL2967_2_response_not_promoted", any(row["adoption_id"] == "RDA2967_7_verdict" and row["parent_adopted"] is False for row in all_rows["adoption"]), "response-doublet parent density remains not promoted", True),
        ("VAL2967_3_kinetic_rejected", any(row["kinetic_id"] == "KIN2967_5_verdict" and row["kinetic_branch_acquired"] is False for row in all_rows["kinetic"]), "finite-range kinetic branch rejected for current corpus", True),
        ("VAL2967_4_rank_zero_selected", any(row["rank_zero_id"] == "RZ2967_4_verdict" and row["current_status"] == "RANK_ZERO_SWITCH_SELECTED_NONCLAIM" for row in all_rows["rank_zero"]), "rank-zero switch selected as nonclaim route", True),
        ("VAL2967_5_residual_pack_nonclaim", all(row["accepted_for_scoring"] is False and row["valid_for_claim"] is False for row in all_rows["residual_pack"]), "rank-zero residual pack remains nonclaim", True),
        ("VAL2967_6_residual_paths_exist", all(row["source_path_exists"] is True for row in all_rows["residual_pack"]), "residual pack rows cite existing paths", True),
        ("VAL2967_7_claims_blocked", all(row["condition_passed"] is False and row["claim_allowed"] is False for row in all_rows["claims"]), "all claim gates remain blocked", True),
        ("VAL2967_8_next_target_written", any(row["next_id"] == "NEXT2967_0_2968" for row in all_rows["next"]), "2968 next target selected", True),
        ("VAL2967_9_branches_exist", all(Path(row["copy_path"]).exists() for row in all_rows["branches"]), "branch copy files exist", True),
        ("VAL2967_10_csvs_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV files parse", True),
        ("VAL2967_11_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in generated_paths), "all generated outputs are under post-checkpoint-work", True),
        ("VAL2967_12_formalization_clean", not any(is_under(path, FORMALIZATION) for path in generated_paths), "no 2967 outputs were written to formalization-workbench", True),
        ("VAL2967_13_doc_written", DOC.exists(), "2967 markdown checkpoint exists", True),
    ]
    overall = all(passed == required for _, passed, _, required in checks)
    rows = [
        add_common(
            {
                "validation_id": validation_id,
                "passed": passed,
                "check": check,
                "required": required,
            }
        )
        for validation_id, passed, check, required in checks
    ]
    rows.append(add_common({"validation_id": "VAL2967_OVERALL", "passed": overall, "check": "2967 validation overall", "required": True}))
    return rows


def write_markdown(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2967 - Y5 R2FR: response-doublet parent-density adoption or rank-zero switch under AX1090

Status: `Y5_R2FR_2967_response_doublet_not_parent_promoted_no_kinetic_branch_rank_zero_switch_selected_nonclaim`

Claim ceiling: `no_response_doublet_promotion_no_finite_range_no_R10_PPN_clock_orbital_claim_no_local_GR_no_Newton_no_public_claim`

2967 tests whether the response-doublet route can own the parent density strongly enough to support `M_AB/Z_X f_X^2`.

- Result: the response-doublet density remains a strong conditional skeleton, not a parent-promoted action.
- The algebraic Hessian/double-zero structure survives; the kinetic/principal-symbol branch does not.
- Therefore finite-range/Yukawa `lambda_i` language is rejected for the current corpus.
- The honest route is now rank-zero algebraic local-GR work: `M_AB Z^B=J_A+B_A+C_A^CDB+R_A`, with every forcing term either theorem-zero or explicitly bounded.

## Source Register

{md_table(all_rows["sources"], ["source_id", "source_path", "path_exists", "anchors_found", "role"])}

## Response-Doublet Adoption Gate

{md_table(all_rows["adoption"], ["adoption_id", "object", "current_status", "conditional_math_available", "parent_adopted", "evidence_summary"])}

## Kinetic Principal-Symbol Audit

{md_table(all_rows["kinetic"], ["kinetic_id", "object", "current_status", "conditional_math_available", "kinetic_branch_acquired", "evidence_summary"])}

## Rank-Zero Switch Gate

{md_table(all_rows["rank_zero"], ["rank_zero_id", "object", "current_status", "conditional_math_available", "theorem_zero_adopted", "evidence_summary"])}

## Rank-Zero Residual Pack Requirements

{md_table(all_rows["residual_pack"], ["requirement_id", "symbol", "current_status", "units", "accepted_for_scoring", "no_cancellation_policy"])}

## Claim Gates

{md_table(all_rows["claims"], ["claim_gate_id", "claim", "condition_passed", "status", "claim_allowed"])}

## Decision Ledger

{md_table(all_rows["decision"], ["decision_id", "decision", "because", "next_action"])}

## Next Target

{md_table(all_rows["next"], ["next_id", "priority", "next_doc", "next_script", "objective", "exclude"])}

## Branch Copies

{md_table(all_rows["branches"], ["copy_id", "source_path", "copy_path", "source_exists", "copy_exists", "valid_for_claim"])}

## Validation

{md_table(all_rows["validation"], ["validation_id", "passed", "check", "required"])}

Validation overall: `{all_rows["validation"][-1]["passed"]}`.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    all_rows: dict[str, list[dict[str, Any]]] = {
        "sources": source_register_rows(),
        "adoption": adoption_gate_rows(),
        "kinetic": kinetic_audit_rows(),
        "rank_zero": rank_zero_rows(),
        "residual_pack": residual_pack_rows(),
        "claims": claim_gate_rows(),
        "decision": decision_rows(),
        "next": next_target_rows(),
    }

    for key, path in OUTPUTS.items():
        if key in {"branches", "validation"}:
            continue
        write_csv(path, all_rows[key])

    all_rows["branches"] = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], all_rows["branches"])

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)

    print(f"2967 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()

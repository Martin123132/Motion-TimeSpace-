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
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2913"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2913-Y5-R2FR-parent-auxiliary-constraint-origin-or-DqZ-geometry-bound-fill-under-AX1090.md"

SRC_2912_DOC = ROOT / "2912-Y5-R2FR-constraint-first-Z-elimination-or-first-DqZ-component-bound-under-AX1090.md"
SRC_2912_NEXT = RESIDUALS / "P8_Y5_R2FR_2912_NEXT_TARGET.csv"
SRC_2912_PROOF = RESIDUALS / "P8_Y5_R2FR_2912_CONSTRAINT_FIRST_PROOF_ATTEMPT.csv"
SRC_2912_AUX = RESIDUALS / "P8_Y5_R2FR_2912_AUXILIARY_ELIMINATION_SIGNATURE_AUDIT.csv"
SRC_2912_DQZ = RESIDUALS / "P8_Y5_R2FR_2912_FIRST_DQZ_COMPONENT_BOUND_INPUT_ROW.csv"
SRC_2912_CLAIMS = RESIDUALS / "P8_Y5_R2FR_2912_CLAIM_GATES.csv"
SRC_2634_GPR = RESIDUALS / "P8_Y5_PARENT_ACTION_GENERATOR_2634_GENERATING_PRINCIPLE_ATTEMPT.csv"
SRC_2634_PCH = RESIDUALS / "P8_Y5_PARENT_ACTION_GENERATOR_2634_PROOF_CHAIN_VERDICT.csv"
SRC_2634_UG = RESIDUALS / "P8_Y5_PARENT_ACTION_GENERATOR_2634_UNIVERSAL_PROPERTY_GAP.csv"
SRC_2697_BLOCKS = RESIDUALS / "P8_Y5_R2FR_2697_MINIMAL_PARENT_ACTION_BLOCKS.csv"
SRC_2731_SCAN = RESIDUALS / "P8_Y5_R2FR_2731_PARENT_ACTION_DEEP_SCAN.csv"
SRC_2751_SORT = RESIDUALS / "P8_Y5_R2FR_2751_PARENT_SORT_AUDIT.csv"
SRC_2751_GRAMMAR = RESIDUALS / "P8_Y5_R2FR_2751_NO_DERIVATIVE_GRAMMAR_GATE.csv"
SRC_2751_JOINT = RESIDUALS / "P8_Y5_R2FR_2751_JOINT_PROTECTION_CONTRACT.csv"
SRC_2838_SIGNATURE = RESIDUALS / "P8_Y5_R2FR_2838_SECOND_CLASS_SIGNATURE_AUDIT.csv"
SRC_2838_GUARDS = RESIDUALS / "P8_Y5_R2FR_2838_GUARDS.csv"
SRC_2866_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2866_MINIMAL_PARENT_ACTION_CONTRACT.csv"
SRC_2873_REQUEST = RESIDUALS / "P8_Y5_R2FR_2873_PARENT_ACTION_CLAUSE_REQUEST.csv"
SRC_2883_SYNTH = RESIDUALS / "P8_Y5_R2FR_2883_CONSTRAINT_FIRST_SYNTHESIS.csv"
SRC_2885_FACTOR = RESIDUALS / "P8_Y5_R2FR_2885_DQZ_FACTOR_VALUE_OR_BLOCKER_LEDGER.csv"
SRC_2886_COMPONENT = RESIDUALS / "P8_Y5_R2FR_2886_FIRST_FINITE_DQZ_COMPONENT_ROW_NONCLAIM.csv"
SRC_2911_DQZ = RESIDUALS / "P8_Y5_R2FR_2911_FINITE_DQZ_NORM_VECTOR.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2913_SOURCE_REGISTER.csv",
    "origin": RESIDUALS / "P8_Y5_R2FR_2913_PARENT_AUXILIARY_ORIGIN_AUDIT.csv",
    "action": RESIDUALS / "P8_Y5_R2FR_2913_ACTION_IMAGE_AND_GENERATOR_GATE.csv",
    "guards": RESIDUALS / "P8_Y5_R2FR_2913_NO_DERIVATIVE_AND_STRESS_GUARDS.csv",
    "dqz_contract": RESIDUALS / "P8_Y5_R2FR_2913_DQZ_GEOMETRY_ACQUISITION_CONTRACT.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2913_RUNNER_STATUS.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2913_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2913_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2913_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2913_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2913_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "origin_copy": PARENT_ACTION / "Parent_auxiliary_constraint_origin_2913_NONCLAIM.csv",
    "dqz_contract_copy": LOCAL_BOUNDS / "DqZ_geometry_acquisition_contract_2913_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2913_DQZ_GEOMETRY_SOURCE_ACQUISITION_NEXT_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


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


def csv_parses(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


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
    if columns is None:
        columns = list(rows[0].keys())
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2913_00_2912_doc", SRC_2912_DOC, "NEXT2912_0_2913;lambda_Z C_Z", "2912 handoff and magic multiplier guard"),
        ("SRC2913_01_2912_next", SRC_2912_NEXT, "NEXT2912_0_2913;parent action image supplies S_Z", "machine-readable 2913 target"),
        ("SRC2913_02_2912_proof", SRC_2912_PROOF, "CFP2912_1_magic_multiplier_guard;CFP2912_5_current_verdict", "constraint-first proof status"),
        ("SRC2913_03_2912_aux", SRC_2912_AUX, "AUX2912_0_parent_origin;AUX2912_6_verdict", "auxiliary origin blocker"),
        ("SRC2913_04_2912_dqz", SRC_2912_DQZ, "BDQZ2912_0_DqZ_geometry;Dq_Z_norm", "first DqZ geometry row"),
        ("SRC2913_05_2912_claims", SRC_2912_CLAIMS, "CG2912_7_local_GR_Newton;BLOCKED_NONCLAIM", "local claim ceiling"),
        ("SRC2913_06_2634_gpr", SRC_2634_GPR, "GPR2634_0_primitive_universal_property;GPR2634_1_closed_parent_domain", "parent generating-principle attempt"),
        ("SRC2913_07_2634_pch", SRC_2634_PCH, "PCH2634_1_conditional_success;PCH2634_2_failure_location", "parent proof-chain verdict"),
        ("SRC2913_08_2634_gap", SRC_2634_UG, "UG2634_1_initial_or_free_object;UG2634_4_parent_domain_certificate", "universal property/domain gap"),
        ("SRC2913_09_2697_blocks", SRC_2697_BLOCKS, "ACT2697_5_extra_sector_silence;ACT2697_9_residual_branch", "minimal action block map"),
        ("SRC2913_10_2731_scan", SRC_2731_SCAN, "SCAN2731_10_2710_AX1090;SCAN2731_2_137_auxiliary_owner", "deep scan of parent-action candidates"),
        ("SRC2913_11_2751_sort", SRC_2751_SORT, "SORT2751_1_auxiliary_coordinate;SORT2751_4_current_verdict", "parent sort audit"),
        ("SRC2913_12_2751_grammar", SRC_2751_GRAMMAR, "GRAM2751_0_no_DRAB;GRAM2751_5_current_verdict", "no-derivative grammar gate"),
        ("SRC2913_13_2751_joint", SRC_2751_JOINT, "CON2751_1_action_image;CON2751_6_joint_contract", "joint protection contract"),
        ("SRC2913_14_2838_signature", SRC_2838_SIGNATURE, "SIG2838_1_action_image;SIG2838_6_joint_signature", "second-class signature audit"),
        ("SRC2913_15_2838_guards", SRC_2838_GUARDS, "GUARD2838_0_no_closure_insert;GUARD2838_4_no_local_claim", "second-class guardrails"),
        ("SRC2913_16_2866_contract", SRC_2866_CONTRACT, "PACT2866_7_matter_readout;PACT2866_9_acceptance", "minimal parent action contract"),
        ("SRC2913_17_2873_request", SRC_2873_REQUEST, "REQ2873_0_rank_one_parent_action;REQ2873_2_boundary_green_readout", "needed parent action clauses"),
        ("SRC2913_18_2883_synth", SRC_2883_SYNTH, "SYN2883_1_magic_multiplier_guard;SYN2883_5_current_verdict", "constraint synthesis guard"),
        ("SRC2913_19_2885_factor", SRC_2885_FACTOR, "DQZF2885_0_Dq_Z_norm;DQZF2885_2_C_Obs_e", "DqZ factor blockers"),
        ("SRC2913_20_2886_component", SRC_2886_COMPONENT, "DQC2886_0_E_DqZ_coframe;MISSING_COMPONENT_VALUES", "finite DqZ component stub"),
        ("SRC2913_21_2911_dqz", SRC_2911_DQZ, "DQZ2911_1_DqZ_geometry;DQZ2911_TOTAL", "upstream DqZ finite vector"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, source_path, anchors, role in specs:
        found, missing = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
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


def origin_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "PAO2913_0_parent_sort",
            "typed auxiliary parent sort",
            "Z^A and Lambda_A are declared in Conf_parent as an auxiliary compatibility pair before q, matter, source normalization or readout maps are formed.",
            "CANDIDATE_NOT_PARENT_SIGNED",
            "2751/2838 give the correct sort signature, but no parent primitive/signature proves it.",
            "no theorem-zero credit for DqZ",
        ),
        (
            "PAO2913_1_action_image",
            "parent action image contains S_Z",
            "S_parent includes S_Z = integral_W mu_parent Lambda_A*(Z^A-C^A[Q_vis,theta,top]) from MTS primitives, not as a late closure appendage.",
            "MISSING_PARENT_ACTION_IMAGE",
            "2634 says the parent object/domain/universal property is still too strong for current evidence.",
            "magic multiplier guard remains active",
        ),
        (
            "PAO2913_2_compatibility_map",
            "compatibility map C^A is public-basic",
            "C^A[Q_vis,theta,top] contains no hidden source-only marker, fitted arena mask, representative Weyl/disformal tail or source-specific coefficient.",
            "MISSING_PUBLIC_BASIC_MAP_PROOF",
            "no complete q-factorization and no-source-slot certificate exists for this exact S_Z block.",
            "DqZ_geometry/source/readout can re-enter",
        ),
        (
            "PAO2913_3_multiplier_units_rank",
            "multiplier/rank/eigenbasis owner",
            "Lambda_A, Z^A and C^A have declared units; the compatibility Jacobian has a rank/null projector and a no-cancellation norm convention.",
            "MISSING_UNITS_RANK_SIGNATURE",
            "current rows stage symbols but do not source numeric operator norms or parent Hessian rank.",
            "no source-ready finite prediction row",
        ),
        (
            "PAO2913_4_variation_order",
            "variation order before readout",
            "delta_Lambda S_Z imposes Z^A=C^A before q, source, matter, clocks, PPN/orbits and boundary projectors are evaluated.",
            "FORMAL_PASS_INSIDE_CANDIDATE_ONLY",
            "this is algebraically true if S_Z is parent-owned, but the ownership premise is unsigned.",
            "cannot promote beyond conditional theorem",
        ),
        (
            "PAO2913_5_Z_equation_forcing",
            "Z-equation forcing silence",
            "delta_Z S_total gives Lambda_A+J_A+B_A+R_A^source+R_A^readout+R_A^boundary=0, and every forcing channel is zero/proper or separately bounded.",
            "UNSIGNED_FORCING_CHANNELS",
            "matter/source, boundary/corner and readout regeneration are precisely the channels still open.",
            "finite residual branch stays live",
        ),
        (
            "PAO2913_6_verdict",
            "parent auxiliary origin for current MTS",
            "current MTS derives the second-class auxiliary block from a parent action and can set Dq_Z_norm=0 by elimination-before-q.",
            "PARENT_AUXILIARY_ORIGIN_NOT_DERIVED",
            "the parent action image, generator/domain proof, compatibility map, units/rank and forcing silence do not close together.",
            "demote to DqZ_geometry acquisition contract",
        ),
    ]
    return [
        add_common(
            {
                "audit_id": audit_id,
                "clause": clause,
                "required_statement": statement,
                "current_status": status,
                "evidence_read": evidence,
                "if_open": consequence,
                "parent_signed": False,
                "theorem_zero_adopted": False,
            }
        )
        for audit_id, clause, statement, status, evidence, consequence in specs
    ]


def action_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "AIG2913_0_exact_candidate",
            "candidate second-class action image",
            "S_Z = integral_W mu_parent Lambda_A*(Z^A-C^A[Q_vis,theta,top])",
            "EXACT_CONDITIONAL_SHAPE",
            "would eliminate Z algebraically before visible physics if parent-owned",
            "shape alone is not provenance",
        ),
        (
            "AIG2913_1_generator_origin",
            "generating principle owns the block",
            "The parent generating rule forces this auxiliary block as the unique compatibility completion of motion-time-space data.",
            "FAIL_CURRENT_GENERATOR_PROOF",
            "2634 fails at universal property and closed parent-domain closure.",
            "do not append the block just because it is useful",
        ),
        (
            "AIG2913_2_domain_closure",
            "closed parent domain before variation",
            "Conf_parent and Args(S_parent) exclude readout/projector/fitted masks before variation.",
            "MISSING_DOMAIN_CERTIFICATE",
            "without it, readout-side choices can be back-smuggled into the parent action.",
            "keeps no-source-slot unpromoted",
        ),
        (
            "AIG2913_3_no_independent_operators",
            "no extra independent Z operators",
            "ParentGenerate forbids D Z, D Lambda, vertical metric, boundary derivative momenta and source-label prefactors in the same block.",
            "ABSENCE_NOT_GRAMMAR_PROOF",
            "2751/2838 write the desired grammar but do not prove exhaustion.",
            "finite kinetic/source residuals remain legal countermodels",
        ),
        (
            "AIG2913_4_matter_boundary_readout",
            "descent of matter, boundary and readout",
            "Ordinary matter, source worldtubes, clocks, EM/charge, PPN/orbital readouts and boundaries see Q_vis/the public coframe, not the vertical representative.",
            "UNSIGNED_DESCENT_AND_REGENERATION",
            "2838 and 2866 both keep matter/readout/boundary clauses conditional.",
            "Z may re-enter through source/readout tails",
        ),
        (
            "AIG2913_5_current_verdict",
            "action image and generator for current MTS",
            "current corpus proves S_Z is generated by the parent theory and is the only allowed local auxiliary completion.",
            "ACTION_IMAGE_NOT_PARENT_SIGNED",
            "the candidate is mathematically useful but still closure-only.",
            "move to finite DqZ_geometry acquisition",
        ),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "gate": gate,
                "target_statement": target,
                "current_status": status,
                "effect_if_signed": effect,
                "guardrail": guard,
                "gate_pass": status == "EXACT_CONDITIONAL_SHAPE",
                "promotes_claim": False,
            }
        )
        for gate_id, gate, target, status, effect, guard in specs
    ]


def guard_rows() -> list[dict[str, Any]]:
    specs = [
        ("NDS2913_0_no_DZ", "ban D_mu Z^A kinetic/gradient operators", "otherwise Z has exterior hair and DqZ_geometry is physical", "UNSIGNED_GRAMMAR"),
        ("NDS2913_1_no_DLambda", "ban D_mu Lambda_A kinetic/gradient operators", "otherwise the multiplier becomes a propagating field", "UNSIGNED_GRAMMAR"),
        ("NDS2913_2_no_vertical_metric", "ban hidden vertical metric/connection contractions", "otherwise representative energy can source local metric/readout", "UNSIGNED_GRAMMAR"),
        ("NDS2913_3_constraint_stress", "constraint stress vanishes after elimination", "Lambda_A must vanish, be q-basic/proper, or be carried as an explicit residual", "UNSIGNED_STRESS_SILENCE"),
        ("NDS2913_4_boundary_corner", "no boundary/corner derivative momentum for Z/Lambda", "otherwise the bulk algebraic zero leaves edge charge", "MISSING_BOUNDARY_CERTIFICATE"),
        ("NDS2913_5_readout_regen", "readout/coarse-graining cannot regenerate Z dependence", "otherwise post-elimination observables rebuild the residual", "MISSING_READOUT_STABILITY"),
        ("NDS2913_6_source_worldtube", "source worldtube and Hilbert current are public-basic", "otherwise ordinary matter supplies J_Z despite algebraic block", "MISSING_SOURCE_DESCENT"),
        ("NDS2913_7_verdict", "joint no-derivative/stress guard", "all guards above close in one parent action", "FAIL_CURRENT_JOINT_GUARD"),
    ]
    return [
        add_common(
            {
                "guard_id": guard_id,
                "guard": guard,
                "why_needed": why,
                "current_status": status,
                "guard_active": True,
                "clause_met": False,
            }
        )
        for guard_id, guard, why, status in specs
    ]


def dqz_contract_rows() -> list[dict[str, Any]]:
    specs = [
        ("DGC2913_00_formula", "DqZ_geometry", "E_DqZ_geometry <= Pi_geom*C_Obs_e*Dq_Z_norm*N_Z + E_shadow + E_boundary_geom + E_readout_geom", "dimensionless_frame_or_metric_response", "whole bound formula", "BDQZ2912_0_DqZ_geometry"),
        ("DGC2913_01_C_Obs_e", "C_Obs_e", "operator norm taking parent coframe/metric perturbations into observed geometry response", "dimensionless_operator_norm", "observed coframe functor and no readout-after-variation certificate", "DQZF2885_2_C_Obs_e"),
        ("DGC2913_02_Dq_Z_norm", "Dq_Z_norm", "operator norm of visible quotient derivative along the Z/auxiliary representative direction", "dimensionless_after_declared_qZ_norms", "parent q map, Dq matrix, Z basis, q/Z norms", "DQZF2885_0_Dq_Z_norm"),
        ("DGC2913_03_N_Z", "N_Z", "size/radius of allowed Z-basis perturbation in the local branch", "declared_Z_norm_units", "rank/eigenbasis and tangent-space normalization", "DQZ2911_TOTAL"),
        ("DGC2913_04_Pi_geom", "Pi_geom", "projection from quotient/coframe response to PPN/clock/orbital geometry observable", "arena_projection_norm", "PPN/clock/orbit observable map and units", "BDQZ2912_0_DqZ_geometry"),
        ("DGC2913_05_q_norm", "norm_q", "norm on visible quotient variables before interpolation/readout", "declared_q_units", "q map and public field chart", "QMAP2911_7_verdict"),
        ("DGC2913_06_e_norm", "norm_e", "norm on observed coframe/metric perturbations", "declared_frame_units", "public coframe functor and gauge convention", "DQC2886_0_E_DqZ_coframe"),
        ("DGC2913_07_Z_norm", "norm_Z", "norm on auxiliary/vertical Z components", "declared_Z_units", "parent auxiliary sort and kernel basis", "DQZ2911_1_DqZ_geometry"),
        ("DGC2913_08_coframe_functor", "F_obs_e", "observed coframe functor from parent public stack to measured geometry", "functor_certificate", "one public metric/coframe, no shadow-frame readout", "PACT2866_7_matter_readout"),
        ("DGC2913_09_no_shadow", "C_shadow", "upper bound on representative Weyl/disformal/shadow-frame leakage", "dimensionless_or_arena_specific", "no-shadow-frame theorem or numeric bound", "CM2708_2_shadow_frame"),
        ("DGC2913_10_boundary_tail", "E_boundary_geom", "geometry leakage from boundary/projector/source-support tails", "arena_geometry_units", "proper collar/boundary primitive/projector commutator", "REQ2873_2_boundary_green_readout"),
        ("DGC2913_11_readout_tail", "E_readout_geom", "geometry leakage regenerated by clocks/EM/orbit/PPN readout", "arena_geometry_units", "readout stability and marker silence", "SIG2838_5_readout_stability"),
        ("DGC2913_12_source_path", "source_path/equation_ref", "every numeric value must cite a local source path and equation/row anchor", "provenance_string", "source-backed row, not memory or taste", "VALIDATION_REQUIRED"),
        ("DGC2913_13_promotion_rule", "promotion_rule", "valid_for_claim can only become true when every input is numeric, positive where required, unit-locked, sourced and has no MISSING marker", "boolean_gate", "runner validation and no-cancellation guard", "VAL2913_REQUIRED"),
    ]
    return [
        add_common(
            {
                "contract_id": contract_id,
                "symbol": symbol,
                "definition_or_formula": definition,
                "units": units,
                "required_input_or_source": required,
                "upstream_anchor": anchor,
                "current_value": "MISSING_PARENT_OR_SOURCE_INPUT",
                "current_upper_bound": "MISSING_SOURCE_BACKED_UPPER_BOUND",
                "source_paths": ";".join(str(p) for p in [SRC_2912_DQZ, SRC_2885_FACTOR, SRC_2886_COMPONENT, SRC_2911_DQZ]),
                "status": "ACQUISITION_REQUIRED_NONCLAIM",
                "promotion_allowed_now": False,
            }
        )
        for contract_id, symbol, definition, units, required, anchor in specs
    ]


def runner_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    all_sources_ready = all(bool(row["path_exists"]) and bool(row["anchors_found"]) for row in source_rows)
    specs = [
        ("RUN2913_0_sources", "SOURCE_AUDIT_COMPLETE" if all_sources_ready else "SOURCE_AUDIT_HAS_BLOCKERS", "all cited source paths and anchors", all_sources_ready, "source evidence checked"),
        ("RUN2913_1_zero_proof", "PARENT_AUXILIARY_ZERO_PROOF_ATTEMPTED_NOT_SIGNED", "parent sort, S_Z origin, generator/domain, compatibility map, no-derivative grammar, forcing silence", False, "one unsigned parent clause blocks theorem-zero"),
        ("RUN2913_2_magic_guard", "MAGIC_MULTIPLIER_STILL_REJECTED", "lambda_Z C_Z only counts if parent-generated", True, "closure insertion is explicitly refused"),
        ("RUN2913_3_demotion", "LOCAL_BRANCH_DEMOTED_TO_DQZ_GEOMETRY_ACQUISITION", "finite metric/coframe leakage contract", False, "no claim; source-ready contract only"),
        ("RUN2913_4_next", "2914_DQZ_GEOMETRY_SOURCE_ACQUISITION_SELECTED", "C_Obs_e/no-shadow/coframe/DqZ geometry inputs", False, "next move is concrete source acquisition or first bound proof"),
    ]
    return [
        add_common(
            {
                "runner_id": runner_id,
                "status": status,
                "required_components": required,
                "components_evaluable": evaluable,
                "reason": reason,
            }
        )
        for runner_id, status, required, evaluable, reason in specs
    ]


def claim_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2913_0_conditional_shape", "the candidate S_Z algebraic shape is coherent", "PASS_CONDITIONAL_ONLY", "it is a useful theorem target, not a current theorem", True),
        ("CG2913_1_parent_origin", "S_Z is generated by the MTS parent action", "BLOCKED_NONCLAIM", "action image and generating principle remain unsigned", False),
        ("CG2913_2_auxiliary_zero", "Dq_Z_norm=0 by parent auxiliary elimination", "BLOCKED_NONCLAIM", "parent origin, q-factorization, forcing silence and guards do not close", False),
        ("CG2913_3_DqZ_geometry", "DqZ_geometry is source-ready and claim-valid", "BLOCKED_NONCLAIM", "all numeric/source inputs are missing", False),
        ("CG2913_4_R10_PPN_clock_orbit", "R10/PPN/clock/orbital branches pass", "BLOCKED_NONCLAIM", "2913 produces acquisition rows only", False),
        ("CG2913_5_local_GR_Newton", "local GR/Newton follows after 2913", "BLOCKED_NONCLAIM", "the local branch is still a derivation target or finite residual contract", False),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "claim": claim,
                "gate_status": status,
                "reason": reason,
                "gate_pass": gate_pass,
            }
        )
        for gate_id, claim, status, reason, gate_pass in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2913_0_result", "PARENT_AUXILIARY_ORIGIN_NOT_DERIVED", "The clean second-class route is still the right shape, but current MTS does not prove the parent action generates S_Z.", "do not claim Dq_Z_norm=0"),
        ("DEC2913_1_demote", "DEMOTE_THIS_ROUTE_TO_CONTRACT_UNTIL_SOURCE", "Because S_Z is not parent-signed, the local route must be treated as a DqZ_geometry acquisition problem rather than a theorem-zero result.", "fill C_Obs_e, Dq_Z_norm, N_Z, Pi_geom and tails"),
        ("DEC2913_2_best_attack", "C_OBS_NO_SHADOW_FIRST", "The most useful next choke point is observed-coframe/no-shadow response, because it controls whether hidden representative variation can leak into public metric tests.", "derive or source C_Obs_e/C_shadow first"),
        ("DEC2913_3_project_state", "PROGRESS_NOT_CLAIM", "The bottleneck has become narrower and more testable: parent-origin proof failed, but the finite residual contract is now explicit.", "continue derivation-first, source-bound second"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": next_action,
            }
        )
        for decision_id, decision, because, next_action in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "route_id": "NEXT2913_0_2914",
                "selection_status": "selected_primary",
                "target_file": "2914-Y5-R2FR-DqZ-geometry-source-acquisition-or-Cobs-no-shadow-bound-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_DqZ_geometry_source_acquisition_or_Cobs_no_shadow_bound_under_AX1090_2914.py",
                "task": "derive or source the first DqZ_geometry acquisition heads, prioritizing C_Obs_e, no-shadow-frame coefficient C_shadow, observed coframe functor, Dq_Z_norm and Pi_geom",
                "success_condition": "C_Obs_e/C_shadow/F_obs_e/Dq_Z_norm/Pi_geom are parent-derived theorem-zero or source-backed numeric upper bounds with units and no MISSING markers",
                "fallback_condition": "produce first source-ready numeric placeholder-free rows for DqZ_geometry while keeping valid_for_claim=false if any required input remains missing",
                "guardrails": "no theorem-zero without parent origin; no closure insertion; no source-less numeric values; no local GR/Newton/R10/PPN claim; no formalization-workbench edits; no GitHub",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("origin_copy", OUTPUTS["origin"], BRANCH_OUTPUTS["origin_copy"]),
        ("dqz_contract_copy", OUTPUTS["dqz_contract"], BRANCH_OUTPUTS["dqz_contract_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, destination in specs:
        shutil.copyfile(source, destination)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source),
                    "destination_path": str(destination),
                    "source_exists": source.exists(),
                    "destination_exists": destination.exists(),
                    "destination_parses": csv_parses(destination),
                }
            )
        )
    return rows


def validation_rows(
    source_rows: list[dict[str, Any]],
    origin_rows_: list[dict[str, Any]],
    action_rows_: list[dict[str, Any]],
    guard_rows_: list[dict[str, Any]],
    contract_rows_: list[dict[str, Any]],
    claim_rows_: list[dict[str, Any]],
    next_rows_: list[dict[str, Any]],
    branch_rows_: list[dict[str, Any]],
    include_doc_check: bool,
) -> list[dict[str, Any]]:
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_outputs_with_validation = [*csv_outputs, OUTPUTS["validation"]]
    origin_verdict = next(row for row in origin_rows_ if row["audit_id"] == "PAO2913_6_verdict")
    action_verdict = next(row for row in action_rows_ if row["gate_id"] == "AIG2913_5_current_verdict")
    guard_verdict = next(row for row in guard_rows_ if row["guard_id"] == "NDS2913_7_verdict")
    local_claim = next(row for row in claim_rows_ if row["gate_id"] == "CG2913_5_local_GR_Newton")
    required_contract_symbols = {
        "DqZ_geometry",
        "C_Obs_e",
        "Dq_Z_norm",
        "N_Z",
        "Pi_geom",
        "norm_q",
        "norm_e",
        "norm_Z",
        "F_obs_e",
        "C_shadow",
        "E_boundary_geom",
        "E_readout_geom",
        "source_path/equation_ref",
        "promotion_rule",
    }
    contract_symbols = {str(row["symbol"]) for row in contract_rows_}
    generated_paths = [*OUTPUTS.values(), *BRANCH_OUTPUTS.values(), DOC]
    checks = [
        ("VAL2913_0_source_paths_exist", all(bool(row["path_exists"]) for row in source_rows), "all cited source paths exist"),
        ("VAL2913_1_source_anchors_found", all(bool(row["anchors_found"]) for row in source_rows), "all source anchors found"),
        ("VAL2913_2_csv_outputs_parse", all(csv_parses(path) for path in csv_outputs_with_validation if path.exists()), "generated CSV outputs parse cleanly"),
        ("VAL2913_3_origin_not_promoted", origin_verdict["current_status"] == "PARENT_AUXILIARY_ORIGIN_NOT_DERIVED" and not bool(origin_verdict["theorem_zero_adopted"]), "parent auxiliary origin remains unpromoted"),
        ("VAL2913_4_action_image_blocked", action_verdict["current_status"] == "ACTION_IMAGE_NOT_PARENT_SIGNED", "action image/generator gate remains blocked"),
        ("VAL2913_5_guards_blocked", guard_verdict["current_status"] == "FAIL_CURRENT_JOINT_GUARD", "no-derivative/stress guards remain jointly unsigned"),
        ("VAL2913_6_contract_complete", required_contract_symbols.issubset(contract_symbols), "DqZ_geometry acquisition contract contains all required symbols"),
        (
            "VAL2913_7_contract_nonclaim",
            all(not bool(row["promotion_allowed_now"]) and not bool(row["valid_for_claim"]) for row in contract_rows_),
            "all DqZ contract rows remain nonclaim",
        ),
        (
            "VAL2913_8_claim_gates_safe",
            local_claim["gate_status"] == "BLOCKED_NONCLAIM"
            and all(not bool(row["claim_allowed"]) and not bool(row["valid_for_claim"]) for row in claim_rows_),
            "local GR/Newton and empirical claims remain blocked",
        ),
        ("VAL2913_9_next_target_selected", next_rows_[0]["route_id"] == "NEXT2913_0_2914" and bool(next_rows_[0]["selected"]), "2914 DqZ geometry source-acquisition target selected"),
        ("VAL2913_10_branch_copies_parse", all(bool(row["destination_exists"]) and bool(row["destination_parses"]) for row in branch_rows_), "branch copies exist and parse"),
        ("VAL2913_11_no_formalization_outputs", not any(is_under(path, FORMALIZATION) for path in generated_paths), "no generated output path is inside formalization-workbench"),
        ("VAL2913_12_doc_written", DOC.exists() if include_doc_check else True, "markdown checkpoint exists"),
    ]
    rows: list[dict[str, Any]] = [
        {
            "validation_id": validation_id,
            "status": bool(status),
            "detail": detail,
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        }
        for validation_id, status, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2913_OVERALL",
            "status": all(bool(row["status"]) for row in rows),
            "detail": "2913 validation overall",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        }
    )
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    origin_rows_: list[dict[str, Any]],
    action_rows_: list[dict[str, Any]],
    guard_rows_: list[dict[str, Any]],
    contract_rows_: list[dict[str, Any]],
    runner_rows_: list[dict[str, Any]],
    claim_rows_: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    next_rows_: list[dict[str, Any]],
    branch_rows_: list[dict[str, Any]],
    validation_rows_: list[dict[str, Any]],
) -> None:
    overall = next(row for row in validation_rows_ if row["validation_id"] == "VAL2913_OVERALL")
    text = f"""# 2913 - Y5/R2FR Parent Auxiliary Constraint Origin Or DqZ Geometry Bound Fill Under AX1090

Status: `Y5_R2FR_2913_parent_auxiliary_origin_not_derived_DqZ_geometry_acquisition_contract_staged_2914_next`

Claim ceiling: `parent_auxiliary_origin_nonclaim_only_no_DqZ_zero_no_local_GR_no_Newton_no_PPN_no_R10_no_GitHub_claim`

Generated UTC: `{RUN_UTC}`

## Summary

2913 tries the honest zero-proof first. The route would be beautiful if it closed: a parent-generated algebraic auxiliary block

`S_Z = integral_W mu_parent Lambda_A*(Z^A-C^A[Q_vis,theta,top])`

would remove the residual variable `Z` before the public quotient, matter action, source normalization, readouts and boundaries are built. In that case `Dq_Z_norm=0` would follow by absence, not by a plateau axiom.

The route does not close in the current corpus. The obstruction is not algebraic; it is ownership. Current MTS does not yet prove that the parent action itself generates `S_Z`, that the parent domain is closed before readout, that `C^A` is public-basic, that no derivative/stress/source channels survive, and that boundary/readout regeneration is silent.

So 2913 demotes this local transition route to a strict `DqZ_geometry` acquisition contract. This is not defeat; it is the correct pressure point. The next work is to derive or source the first metric/coframe response heads: `C_Obs_e`, `C_shadow`, `F_obs_e`, `Dq_Z_norm`, `N_Z`, `Pi_geom`, and the boundary/readout tails.

## Source Register

{md_table(source_rows, ["source_id", "source_path", "anchors_found", "role", "missing_anchors"])}

## Parent Auxiliary Origin Audit

{md_table(origin_rows_, ["audit_id", "clause", "current_status", "required_statement", "evidence_read", "if_open", "parent_signed", "theorem_zero_adopted", "valid_for_claim"])}

## Action Image And Generator Gate

{md_table(action_rows_, ["gate_id", "gate", "current_status", "target_statement", "effect_if_signed", "guardrail", "gate_pass", "promotes_claim", "valid_for_claim"])}

## No-Derivative And Stress Guards

{md_table(guard_rows_, ["guard_id", "guard", "current_status", "why_needed", "guard_active", "clause_met", "valid_for_claim"])}

## DqZ Geometry Acquisition Contract

{md_table(contract_rows_, ["contract_id", "symbol", "definition_or_formula", "units", "required_input_or_source", "current_value", "current_upper_bound", "status", "promotion_allowed_now", "valid_for_claim"])}

## Runner Status

{md_table(runner_rows_, ["runner_id", "status", "required_components", "components_evaluable", "reason", "valid_for_claim"])}

## Claim Gates

{md_table(claim_rows_, ["gate_id", "claim", "gate_status", "reason", "gate_pass", "valid_for_claim"])}

## Decision Ledger

{md_table(decision_rows_, ["decision_id", "decision", "because", "next_action", "valid_for_claim"])}

## Next Target

{md_table(next_rows_, ["route_id", "selection_status", "target_file", "target_script", "task", "success_condition", "fallback_condition", "valid_for_claim"])}

## Branch Copies

{md_table(branch_rows_, ["copy_id", "source_path", "destination_path", "destination_exists", "destination_parses", "valid_for_claim"])}

## Validation

{md_table(validation_rows_, ["validation_id", "status", "detail", "valid_for_claim"])}

Validation overall: `{overall["status"]}`.

## Interpretation

This is a sharper result than another broad "GR still blocked" note. The local branch now has a named fork:

1. prove the parent action owns the auxiliary block and get `Dq_Z_norm=0` by elimination-before-q; or
2. source the finite `DqZ_geometry` response contract and test whether the residual is small enough in PPN, clocks, orbit and R10 arenas.

2913 says current evidence supports route 2 for now. Route 1 remains the prize, but it cannot be won by inserting a multiplier after the fact.

## Not Claimed

- The parent action does not yet derive `S_Z`.
- `lambda_Z C_Z` is still rejected as proof unless parent-origin is supplied.
- `Dq_Z_norm=0`, `DqZ_geometry=0`, source/readout descent and boundary silence are not proved.
- Newton, PPN, R10, WEP, clock/EM, orbital or local-GR reduction is not claimed.
- No public/GitHub action is implied.
- No file in `formalization-workbench` is modified by this checkpoint.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    origin_rows_ = origin_rows()
    action_rows_ = action_rows()
    guard_rows_ = guard_rows()
    contract_rows_ = dqz_contract_rows()
    runner_rows_ = runner_rows(source_rows)
    claim_rows_ = claim_rows()
    decision_rows_ = decision_rows()
    next_rows_ = next_rows()

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["origin"], origin_rows_)
    write_csv(OUTPUTS["action"], action_rows_)
    write_csv(OUTPUTS["guards"], guard_rows_)
    write_csv(OUTPUTS["dqz_contract"], contract_rows_)
    write_csv(OUTPUTS["runner"], runner_rows_)
    write_csv(OUTPUTS["claims"], claim_rows_)
    write_csv(OUTPUTS["decision"], decision_rows_)
    write_csv(OUTPUTS["next"], next_rows_)

    branch_rows_ = branch_rows()
    write_csv(OUTPUTS["branches"], branch_rows_)

    validation_rows_ = validation_rows(
        source_rows,
        origin_rows_,
        action_rows_,
        guard_rows_,
        contract_rows_,
        claim_rows_,
        next_rows_,
        branch_rows_,
        include_doc_check=False,
    )
    write_csv(OUTPUTS["validation"], validation_rows_)
    write_doc(
        source_rows,
        origin_rows_,
        action_rows_,
        guard_rows_,
        contract_rows_,
        runner_rows_,
        claim_rows_,
        decision_rows_,
        next_rows_,
        branch_rows_,
        validation_rows_,
    )

    validation_rows_ = validation_rows(
        source_rows,
        origin_rows_,
        action_rows_,
        guard_rows_,
        contract_rows_,
        claim_rows_,
        next_rows_,
        branch_rows_,
        include_doc_check=True,
    )
    write_csv(OUTPUTS["validation"], validation_rows_)
    write_doc(
        source_rows,
        origin_rows_,
        action_rows_,
        guard_rows_,
        contract_rows_,
        runner_rows_,
        claim_rows_,
        decision_rows_,
        next_rows_,
        branch_rows_,
        validation_rows_,
    )

    overall = next(row for row in validation_rows_ if row["validation_id"] == "VAL2913_OVERALL")
    if not bool(overall["status"]):
        raise SystemExit(1)


if __name__ == "__main__":
    main()

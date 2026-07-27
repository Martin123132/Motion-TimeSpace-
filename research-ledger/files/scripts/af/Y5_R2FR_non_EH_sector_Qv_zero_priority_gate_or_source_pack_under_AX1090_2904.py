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
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2904-Y5-R2FR-non-EH-sector-Qv-zero-priority-gate-or-source-pack-under-AX1090.md"

SRC_2903_DOC = ROOT / "2903-Y5-R2FR-vertical-sector-variation-ledger-or-Qv-piece-leak-rows-under-AX1090.md"
SRC_2903_NEXT = RESIDUALS / "P8_Y5_R2FR_2903_NEXT_TARGET.csv"
SRC_2903_LEDGER = RESIDUALS / "P8_Y5_R2FR_2903_VERTICAL_SECTOR_VARIATION_LEDGER.csv"
SRC_2903_ROWS = RESIDUALS / "P8_Y5_R2FR_2903_VERTICAL_SECTOR_QV_PIECE_LEAK_ROWS.csv"
SRC_2902_DOC = ROOT / "2902-Y5-R2FR-vertical-Noether-charge-Qv-extraction-or-kernel-charge-source-row-under-AX1090.md"
SRC_2592_DOC = ROOT / "2592-Y5-R2FR-non-EH-sector-Qv-zero-priority-gate-or-source-pack.md"
SRC_2592_GATE = RESIDUALS / "P8_Y5_NON_EH_QV_2592_ZERO_PRIORITY_GATE.csv"
SRC_2592_PACK = RESIDUALS / "P8_Y5_NON_EH_QV_2592_SOURCE_PACK.csv"
SRC_1009_SECTORS = ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md"
SRC_RESPONSE_DOUBLET = RESIDUALS / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv"
SRC_PIM_CONTRACT = RESIDUALS / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv"
SRC_WORLDTUBE_GLUE = RESIDUALS / "P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv"
SRC_MATTER_DESCENT = ROOT / "1760-Y5-R2FR-matter-worldtube-quotient-descent-or-Amatter-bound.md"
SRC_HIDDEN_SOURCE = ROOT / "1756-Y5-R2FR-two-slot-source-free-owner-or-hidden-source-counterexample-ledger.md"
SRC_NOETHER_CHAIN = RESIDUALS / "P8_PARENT_NOETHER_CLOSURE_DERIVATION_CHAIN.csv"
SRC_2593_DOC = ROOT / "2593-Y5-R2FR-extra-response-Qv-zero-odd-source-or-extra-piece-bound.md"
SRC_2593_ZERO = RESIDUALS / "P8_Y5_EXTRA_RESPONSE_QV_2593_ZERO_ODD_SOURCE_AUDIT.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2904_SOURCE_REGISTER.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_2904_CONDITIONAL_NON_EH_SILENCE_THEOREM.csv",
    "gate": RESIDUALS / "P8_Y5_R2FR_2904_NON_EH_QV_ZERO_PRIORITY_GATE.csv",
    "pack": RESIDUALS / "P8_Y5_R2FR_2904_NON_EH_QV_SOURCE_PACK.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2904_RUNNER_STATUS.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2904_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2904_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2904_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2904_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2904_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "gate_copy": RAB_QUEUE / "JR2904_NON_EH_QV_ZERO_PRIORITY_GATE_NONCLAIM.csv",
    "pack_copy": LOCAL_BOUNDS / "Non_EH_Qv_source_pack_2904_NONCLAIM.csv",
    "theorem_copy": RAB_QUEUE / "JR2904_CONDITIONAL_NON_EH_SILENCE_THEOREM_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2904_EXTRA_RESPONSE_QV_ZERO_SIGNATURE_OR_BOUND_NEXT.csv",
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
            "branch_id": BRANCH_ID,
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
        ("SRC2904_00_2903_doc", SRC_2903_DOC, "retained non-EH sectors are the load-bearing problem;NEXT2903_0_2904", "current-chain handoff selecting non-EH sector zero/source gate"),
        ("SRC2904_01_2903_next", SRC_2903_NEXT, "NEXT2903_0_2904;try to prove boundary", "machine-readable 2904 target"),
        ("SRC2904_02_2903_ledger", SRC_2903_LEDGER, "VSL2903_1_boundary_reference;VSL2903_6_total", "current-chain sector ledger"),
        ("SRC2904_03_2903_piece_rows", SRC_2903_ROWS, "VSP2903_2_extra;VSP2903_TOTAL", "current-chain Qv piece rows"),
        ("SRC2904_04_2592_doc", SRC_2592_DOC, "non-EH local-silence gate is explicit;highest-leverage next target is the extra/response sector", "prior non-EH silence gate"),
        ("SRC2904_05_2592_gate", SRC_2592_GATE, "ZNE2592_1_extra_response;ZNE2592_6_verdict", "prior zero priority rows"),
        ("SRC2904_06_2592_pack", SRC_2592_PACK, "NES2592_1_extra;NES2592_TOTAL", "prior non-EH source pack"),
        ("SRC2904_07_1009_boundary", SRC_1009_SECTORS, "Parent sector contract;PCS1009_0_EH_core", "boundary/reference and parent sector contract"),
        ("SRC2904_08_extra_response", SRC_RESPONSE_DOUBLET, "RD516_4_zero_odd_source;not_derived_hard_block", "extra/response silence obstruction"),
        ("SRC2904_09_projector", SRC_PIM_CONTRACT, "PM4_projector_algebra;conditional", "projector variation owner obstruction"),
        ("SRC2904_10_worldtube", SRC_WORLDTUBE_GLUE, "W504_4_worldtube_source_measure_glue;not_yet_derived_core_missing_piece", "worldtube source-measure glue obstruction"),
        ("SRC2904_11_matter", SRC_MATTER_DESCENT, "Current MTS does not yet parent-sign those clauses;A_matter", "matter descent obstruction"),
        ("SRC2904_12_hidden_source", SRC_HIDDEN_SOURCE, "Every surviving hidden source is converted;explicit nonclaim finite-residual row", "hidden direct-source slot obstruction"),
        ("SRC2904_13_noether_chain", SRC_NOETHER_CHAIN, "D505_3_exterior_derivative;C_projector", "constraint/current split obstruction"),
        ("SRC2904_14_2593_doc", SRC_2593_DOC, "response-doublet route remains the best-looking route;EXTRA_RESPONSE_QV_ZERO_NOT_PROVED_CURRENT_CORPUS", "prior extra-response theorem attempt"),
        ("SRC2904_15_2593_zero", SRC_2593_ZERO, "ERZ2593_1_even_density;ERZ2593_7_verdict", "prior zero-odd-source audit"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, source_path, anchors, role in specs:
        anchors_found, missing_anchors = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(source_path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": source_path.exists(),
                    "anchors_found": anchors_found,
                    "missing_anchors": missing_anchors,
                }
            )
        )
    return rows


def theorem_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "THM2904_0_statement",
            "conditional_non_EH_silence",
            "For one parent branch B with q, observed stack O=q(Phi), compact local surface S, v in ker(Dq), and positive M_ref, Delta H_v^nonEH[S]=0 if every retained non-EH sector is q-basic/fixed exact, theorem-zero, constraint-proportional, or source-bounded with zero bound in the same branch.",
            "DEDUCED_CONDITIONALLY",
            "This is a theorem template, not a current MTS claim, because the parent branch signatures are not all present.",
            SRC_2903_DOC,
        ),
        (
            "THM2904_1_variational_identity",
            "sector_Hamiltonian_split",
            "For each sector i, delta H_v^i[S]=int_S(delta Q_v^i - i_v Theta_i + delta B_v^i)+int_S C_v^i_piece. The non-EH residual is the sum over boundary, extra, projector, matter/source and constraint pieces.",
            "DEDUCED_FROM_CPS_TEMPLATE",
            "Current corpus still lacks owned Theta_i, Q_v^i, B_v^i and C_v^i for all non-EH sectors in one branch.",
            SRC_2902_DOC,
        ),
        (
            "THM2904_2_boundary_zero",
            "fixed_basic_exact_boundary",
            "If boundary/reference terms are chosen before readout, q-basic under vertical v, and give only an exact corner contribution on closed S, then int_S delta B_v=0 and epsilon_Bv_ambiguity=0.",
            "CONDITIONAL_ZERO_LEMMA",
            "Not signed because fixed B_v convention, compact flux class and no post-readout counterterm are not parent-certified.",
            SRC_1009_SECTORS,
        ),
        (
            "THM2904_3_extra_zero",
            "even_positive_zero_odd_source",
            "If the extra/response density is even in the local vertical mode, its operator is positive self-adjoint, the odd source vanishes, the PPN lock holds, and boundary flux vanishes, then the extra minimizer is zero and Q_v^extra contributes no local charge.",
            "CONDITIONAL_ZERO_LEMMA",
            "Not signed because the zero-odd-source and full sector variation remain the hard missing part.",
            SRC_RESPONSE_DOUBLET,
        ),
        (
            "THM2904_4_projector_zero",
            "fixed_parent_symplectic_projector",
            "If Pi_M is a parent-fixed q-basic chain map and delta Pi_M has no vertical component, then d(Pi_M J_H) is a Ward/Euler consequence and projector vertical charge is constraint-proportional.",
            "CONDITIONAL_ZERO_LEMMA",
            "Not signed because projector algebra has not been upgraded into a parent variational/current theorem.",
            SRC_PIM_CONTRACT,
        ),
        (
            "THM2904_5_matter_zero",
            "matter_worldtube_descent",
            "If S_matter=Sbar[q(Phi),Psi,theta] and the worldtube source measure equals the exterior Noether charge before fitting, then vertical v changes no physical matter/source charge and hidden direct-source slots are forbidden.",
            "CONDITIONAL_ZERO_LEMMA",
            "Not signed because matter descent, worldtube glue and no-direct-source-slot are still conditional.",
            SRC_MATTER_DESCENT,
        ),
        (
            "THM2904_6_constraint_zero",
            "same_branch_constraint_split",
            "If every C_v^i is an Euler/Ward/Gauss constraint in the same parent branch, or has a sourced zero bound in the same norm, then the total constraint piece cannot fake a local force.",
            "CONDITIONAL_ZERO_LEMMA",
            "Not signed because the common constraint split is not yet extracted for the full MTS parent action.",
            SRC_NOETHER_CHAIN,
        ),
        (
            "THM2904_7_current_verdict",
            "conditional_theorem_not_parent_signed",
            "The derivation gives an exact contract for local GR reduction: prove THM2904_2 through THM2904_6 in one branch, or carry the corresponding non-EH residuals into PPN/R10/clock/orbital bounds.",
            "CURRENT_MTS_BLOCKED_NONCLAIM",
            "No local-GR/Newton claim follows from the theorem template alone.",
            SRC_2903_LEDGER,
        ),
    ]
    return [
        add_common(
            {
                "theorem_id": theorem_id,
                "clause": clause,
                "derived_statement": derived_statement,
                "status": status,
                "blocking_gap": blocking_gap,
                "source_path": str(source_path),
                "source_path_exists": source_path.exists(),
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "same_branch_certified": False,
                "accepted_for_local_gr": False,
            }
        )
        for theorem_id, clause, derived_statement, status, blocking_gap, source_path in specs
    ]


def zero_priority_gate_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "ZNE2904_0_boundary_Bv",
            3,
            "boundary/reference",
            "B_v and reference subtraction are fixed before readout, q-basic under v, and int_S delta B_v=0 on compact linked local surfaces",
            "CONDITIONAL_ZERO_AVAILABLE_NOT_PARENT_SIGNED",
            "It is likely a convention/functoriality closure, but it can still fake a total zero if left unsigned.",
            "epsilon_Bv_ambiguity remains in the local Qv budget",
            SRC_1009_SECTORS,
        ),
        (
            "ZNE2904_1_extra_response",
            1,
            "extra/response motion-time-memory",
            "extra response is even at the local branch, has positive self-adjoint operator, zero odd local source, PPN lock and no boundary flux",
            "HARD_BLOCK_MISSING_ZERO_ODD_SOURCE_AND_FULL_VARIATION",
            "This is the distinctive MTS channel most likely to carry local charge hair; if it fails, the local-GR branch fails or becomes bounded-residual only.",
            "epsilon_Qv_extra_piece must be bounded or the local-GR route fails",
            SRC_RESPONSE_DOUBLET,
        ),
        (
            "ZNE2904_2_projector_source_measure",
            2,
            "projector/source-measure Pi_M",
            "Pi_M is parent-fixed, symplectic, q-basic, variation-owned, and d(Pi_M J_H)=0 follows from Ward/Euler closure rather than algebra alone",
            "MISSING_PROJECTOR_VARIATION_AND_WARD_CLOSURE",
            "This is where source-normalized Newton can drift while looking algebraically clean.",
            "epsilon_Qv_projector_piece and epsilon_Cv_constraint_missing remain live",
            SRC_PIM_CONTRACT,
        ),
        (
            "ZNE2904_3_matter_worldtube",
            2,
            "matter/source/worldtube",
            "ordinary matter descends through q/e_obs, no direct source slot exists, and worldtube source measure equals exterior Noether charge before fitting",
            "MISSING_MATTER_DESCENT_STACK_AND_WORLDTUBE_GLUE",
            "Silent geometry still fails if source mass and exterior charge are not the same object.",
            "epsilon_Qv_matter_source_piece, epsilon_matter_kernel and epsilon_hidden_source_slot remain live",
            SRC_MATTER_DESCENT,
        ),
        (
            "ZNE2904_4_constraint_Cv",
            4,
            "constraint total",
            "C_v pieces are parent EOM/proper constraints in the same branch or are source-bounded in one declared norm",
            "MISSING_COMMON_CONSTRAINT_SPLIT",
            "Noether identity is not enough unless the residual current is shown to be pure constraint or bounded.",
            "epsilon_Cv_constraint_missing remains live",
            SRC_NOETHER_CHAIN,
        ),
        (
            "ZNE2904_5_same_branch",
            1,
            "same parent branch compatibility",
            "boundary, extra, projector, matter/worldtube and constraint clauses hold simultaneously with one q/e_obs/tau/M_ref branch",
            "MISSING_SAME_BRANCH_COMPATIBILITY_PROOF",
            "Sector-by-sector victories are not enough if they require different branches or normalizations.",
            "epsilon_non_EH_branch_mismatch remains live",
            SRC_2903_DOC,
        ),
        (
            "ZNE2904_6_verdict",
            1,
            "non-EH total",
            "all non-EH sectors above are theorem-zero, fixed-before-readout, constraint-proportional or source-bounded in one branch",
            "CONDITIONAL_THEOREM_DERIVED_BUT_NOT_SIGNED",
            "The current checkpoint improves the target from vague missing coupling to an exact parent-signature contract.",
            "Delta_non_EH_Qv_total_over_Mref remains nonclaim",
            SRC_2903_DOC,
        ),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "priority_rank": priority_rank,
                "sector": sector,
                "zero_condition": zero_condition,
                "current_status": current_status,
                "why_priority": why_priority,
                "if_not_zero": if_not_zero,
                "primary_source": str(primary_source),
                "source_path_exists": primary_source.exists(),
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "accepted_for_local_gr": False,
            }
        )
        for gate_id, priority_rank, sector, zero_condition, current_status, why_priority, if_not_zero, primary_source in specs
    ]


def source_pack_rows() -> list[dict[str, Any]]:
    specs = [
        ("NES2904_0_Bv", "epsilon_Bv_ambiguity", "abs(int_S delta B_v_unfixed)/M_ref", "dimensionless boundary-improvement ambiguity", "MISSING_FIXED_BV_CONVENTION;MISSING_ZERO_BOUNDARY_FLUX;MISSING_NO_POST_READOUT_COUNTERTERM;MISSING_M_REF", SRC_1009_SECTORS, "boundary;clock;orbital;PPN"),
        ("NES2904_1_extra", "epsilon_Qv_extra_piece", "abs(int_S(Q_v^extra + C_v^extra - i_v Theta_extra))/M_ref", "dimensionless extra-sector vertical charge", "MISSING_EXTRA_SECTOR_VARIATION;MISSING_ZERO_ODD_SOURCE;MISSING_PPN_LOCK;MISSING_BOUNDARY_NO_FLUX;MISSING_M_REF", SRC_RESPONSE_DOUBLET, "PPN;R10;clock;cosmology_branching"),
        ("NES2904_2_projector", "epsilon_Qv_projector_piece", "abs(int_S(Q_v^projector + C_v^projector - i_v Theta_projector))/M_ref", "dimensionless projector/source-measure vertical charge", "MISSING_PROJECTOR_VARIATION_OWNER;MISSING_WARD_OR_EULER_CLOSURE;MISSING_CHAIN_MAP_LOCK;MISSING_M_REF", SRC_PIM_CONTRACT, "source_mass;Newton;orbital;PPN"),
        ("NES2904_3_matter_source", "epsilon_Qv_matter_source_piece", "abs(int_S(Q_v^matter/source + C_v^matter - i_v Theta_matter/source))/M_ref", "dimensionless matter/source vertical charge", "MISSING_MATTER_DESCENT;MISSING_WORLDTUBE_GLUE;MISSING_NO_DIRECT_SOURCE_SLOT;MISSING_M_REF", SRC_MATTER_DESCENT, "WEP;source_mass;orbital;Newton"),
        ("NES2904_4_hidden_source", "epsilon_hidden_source_slot", "1 if a non-Hilbert/direct source slot can alter exterior charge after readout else 0", "boolean direct-source guard", "MISSING_PARENT_NO_DIRECT_SOURCE_SLOT;MISSING_SOURCE_CURRENT_OWNER", SRC_HIDDEN_SOURCE, "WEP;source_mass;Newton;local_GR"),
        ("NES2904_5_Cv", "epsilon_Cv_constraint_missing", "abs(int_S C_v_nonconstraint_or_unbounded)/M_ref", "dimensionless constraint leakage", "MISSING_COMMON_CONSTRAINT_SPLIT;MISSING_PARENT_EOM_SOURCE;MISSING_M_REF", SRC_NOETHER_CHAIN, "Bianchi;conservation;source_current"),
        ("NES2904_6_branch", "epsilon_non_EH_branch_mismatch", "1 if non-EH zero conditions require incompatible q/e_obs/tau/M_ref branches else 0", "boolean branch-compatibility guard", "MISSING_SAME_BRANCH_COMPATIBILITY_PROOF", SRC_2903_DOC, "q_owner;same_frame;local_GR"),
        ("NES2904_TOTAL", "Delta_non_EH_Qv_total_over_Mref", "epsilon_Bv_ambiguity + epsilon_Qv_extra_piece + epsilon_Qv_projector_piece + epsilon_Qv_matter_source_piece + epsilon_hidden_source_slot + epsilon_Cv_constraint_missing + epsilon_non_EH_branch_mismatch", "dimensionless after M_ref", "COMPONENTS_MISSING", SRC_2903_ROWS, "q_owner;Newton;local_GR;PPN;R10;clock;orbital"),
    ]
    return [
        add_common(
            {
                "row_id": row_id,
                "symbol": symbol,
                "definition": definition,
                "units": units,
                "current_value": current_value,
                "source_path": str(source_path),
                "source_path_exists": source_path.exists(),
                "observable_link": observable_link,
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for row_id, symbol, definition, units, current_value, source_path, observable_link in specs
    ]


def runner_rows() -> list[dict[str, Any]]:
    specs = [
        ("RUN2904_0_conditional_theorem", "THEOREM_TEMPLATE_DERIVED", "THM2904_2..6 in one parent branch", 0, "template is mathematical contract only; signatures are not present"),
        ("RUN2904_1_zero_claim", "REFUSED_UNSIGNED_NON_EH_SECTORS", "boundary;extra;projector;matter/source;hidden source;constraints;same branch", 0, "no non-EH sector is parent-signed theorem-zero in the current chain"),
        ("RUN2904_2_source_pack", "STAGED_NONCLAIM_SOURCE_PACK", "epsilon_Bv;epsilon_extra;epsilon_projector;epsilon_matter;epsilon_hidden_source;epsilon_Cv;epsilon_branch", 0, "rows are source-backed but unfilled and nonclaim"),
        ("RUN2904_3_next_extra", "NEXT_TARGET_SELECTED", "extra/response zero signature or bounded residual", 0, "highest-risk and highest-information sector is the MTS novelty channel"),
    ]
    return [
        add_common(
            {
                "runner_id": runner_id,
                "status": status,
                "required_components": required_components,
                "components_evaluable": components_evaluable,
                "reason": reason,
                "runner_ready": False,
            }
        )
        for runner_id, status, required_components, components_evaluable, reason in specs
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2904_0_conditional_theorem_shape", "conditional non-EH silence theorem is explicit", "PASS_NONCLAIM_STRUCTURE_ONLY", "the Hamiltonian-sector zero contract is stated with sector clauses", True),
        ("CG2904_1_non_EH_zero", "all non-EH vertical Q_v pieces vanish locally", "BLOCKED_NONCLAIM", "zero conditions are conditional and not parent-signed", False),
        ("CG2904_2_extra_response_zero", "MTS novelty channel is locally silent", "BLOCKED_NONCLAIM", "extra/response full variation, zero odd source, PPN lock and boundary no-flux remain unsigned", False),
        ("CG2904_3_projector_matter_source", "projector and matter/source sectors carry no vertical charge", "BLOCKED_NONCLAIM", "projector Ward/Euler closure and matter/worldtube glue are unsigned", False),
        ("CG2904_4_same_branch", "all zeroes hold in one q/e_obs/tau/M_ref branch", "BLOCKED_NONCLAIM", "same-branch compatibility is not proved", False),
        ("CG2904_5_local_GR_Newton", "local GR/Newton follows from non-EH gate", "BLOCKED_NONCLAIM", "conditional theorem is a contract, not a signed proof", False),
        ("CG2904_6_bound_route", "nonzero sectors are source-bounded and ready for PPN/R10/clock/orbital scoring", "BLOCKED_NONCLAIM", "numeric parent coefficients, M_ref and arena projections are missing", False),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "claim": claim,
                "gate_status": gate_status,
                "reason": reason,
                "gate_pass": gate_pass,
                "parent_signed": False,
                "accepted_for_local_gr": False,
            }
        )
        for gate_id, claim, gate_status, reason, gate_pass in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2904_0_theorem_contract", "CONDITIONAL_NON_EH_SILENCE_CONTRACT_ACCEPTED", "the derivation now says exactly what a future parent action must satisfy for MTS novelty to be locally silent", "use this as the local-GR reduction contract, not as a claim"),
        ("DEC2904_1_no_promotion", "NON_EH_QV_ZERO_NOT_PROMOTED", "the current corpus does not parent-sign boundary, extra, projector, matter/worldtube, hidden-source, constraint and same-branch clauses", "Delta_non_EH_Qv_total_over_Mref remains nonclaim"),
        ("DEC2904_2_best_next", "EXTRA_RESPONSE_SIGNATURE_SELECTED", "extra/response is both the distinctive MTS sector and the most likely local-charge leak", "2905 should attack the full extra-sector operator/source/boundary signature in the current 2900-chain"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "reason": reason,
                "effect": effect,
            }
        )
        for decision_id, decision, reason, effect in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "route_id": "NEXT2904_0_2905",
                "selection_status": "selected_primary",
                "target_file": "2905-Y5-R2FR-extra-response-operator-source-boundary-signature-or-epsilon-extra-bound-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_extra_response_operator_source_boundary_signature_or_epsilon_extra_bound_under_AX1090_2905.py",
                "task": "try to parent-sign the extra/response sector local silence conditions: even density, positive self-adjoint operator, zero odd source, PPN lock and compact boundary no-flux",
                "success_condition": "epsilon_Qv_extra_piece is theorem-zero in the same local branch and can be removed from Delta_non_EH_Qv_total_over_Mref",
                "fallback_condition": "source-pack epsilon_Qv_extra_piece with operator, source, boundary, PPN-lock and arena-bound rows, all valid_for_claim=false",
                "guardrails": "no local-GR claim; no EH-only shortcut; no total-zero switch; no hidden source cancellation; no fitted M_ref; no GitHub; no formalization-workbench edits",
                "selected": True,
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    specs = [
        ("BR2904_0_gate_copy", OUTPUTS["gate"], BRANCH_OUTPUTS["gate_copy"], "RAB queue copy of refreshed non-EH zero priority gate"),
        ("BR2904_1_pack_copy", OUTPUTS["pack"], BRANCH_OUTPUTS["pack_copy"], "local-bounds copy of refreshed non-EH Qv source pack"),
        ("BR2904_2_theorem_copy", OUTPUTS["theorem"], BRANCH_OUTPUTS["theorem_copy"], "RAB queue copy of conditional non-EH silence theorem"),
        ("BR2904_3_next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"], "RAB queue copy of 2905 extra-response target"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, destination, purpose in specs:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_table": str(source),
                    "copy_path": str(destination),
                    "purpose": purpose,
                    "exists": destination.exists(),
                }
            )
        )
    return rows


def formalization_touched() -> bool:
    if not FORMALIZATION.exists():
        return False
    start_timestamp = SCRIPT_START_UTC.timestamp()
    for candidate in FORMALIZATION.rglob("*"):
        try:
            if candidate.is_file() and candidate.stat().st_mtime >= start_timestamp:
                return True
        except OSError:
            return True
    return False


def validation_rows(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = all_rows["sources"]
    theorem_rows_data = all_rows["theorem"]
    gate_rows_data = all_rows["gate"]
    pack_rows_data = all_rows["pack"]
    runner_rows_data = all_rows["runner"]
    claim_rows_data = all_rows["claims"]
    next_rows_data = all_rows["next"]
    branch_rows_data = all_rows["branches"]
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    required_symbols = {
        "epsilon_Bv_ambiguity",
        "epsilon_Qv_extra_piece",
        "epsilon_Qv_projector_piece",
        "epsilon_Qv_matter_source_piece",
        "epsilon_hidden_source_slot",
        "epsilon_Cv_constraint_missing",
        "epsilon_non_EH_branch_mismatch",
        "Delta_non_EH_Qv_total_over_Mref",
    }
    found_symbols = {row["symbol"] for row in pack_rows_data}
    checks = [
        ("VAL2904_0_sources_exist", all(row["path_exists"] for row in source_rows), "all registered source paths exist"),
        ("VAL2904_1_source_anchors", all(row["anchors_found"] for row in source_rows), "all registered source anchors were found"),
        ("VAL2904_2_theorem_contract_present", len(theorem_rows_data) == 8 and any(row["theorem_id"] == "THM2904_7_current_verdict" for row in theorem_rows_data), "conditional non-EH silence theorem contract is present"),
        ("VAL2904_3_theorem_not_promoted", all(not row["theorem_zero_adopted"] and not row["accepted_for_local_gr"] for row in theorem_rows_data), "theorem rows remain conditional nonclaim"),
        ("VAL2904_4_priority_gate_complete", len(gate_rows_data) == 7 and any(row["gate_id"] == "ZNE2904_1_extra_response" and row["priority_rank"] == 1 for row in gate_rows_data), "zero priority gate covers non-EH sectors and selects extra as priority"),
        ("VAL2904_5_gate_source_paths_exist", all(row["source_path_exists"] for row in gate_rows_data), "all priority-gate rows have existing source paths"),
        ("VAL2904_6_source_pack_symbols_present", required_symbols <= found_symbols, "all refreshed non-EH source-pack symbols are present"),
        ("VAL2904_7_source_pack_paths_exist", all(row["source_path_exists"] for row in pack_rows_data), "source-pack rows point to existing local evidence"),
        ("VAL2904_8_rows_nonclaim", all(not row["valid_for_claim"] and not row["accepted_for_scoring"] for row in pack_rows_data), "non-EH source-pack rows remain non-score-ready and nonclaim"),
        ("VAL2904_9_runner_refuses", any(row["runner_id"] == "RUN2904_1_zero_claim" and row["status"] == "REFUSED_UNSIGNED_NON_EH_SECTORS" for row in runner_rows_data), "runner refuses unsigned non-EH zero claim"),
        ("VAL2904_10_claim_gates_safe", all(not row["claim_allowed"] for row in claim_rows_data) and any(row["gate_id"] == "CG2904_5_local_GR_Newton" and row["gate_status"] == "BLOCKED_NONCLAIM" for row in claim_rows_data), "local-GR/Newton claims remain blocked"),
        ("VAL2904_11_next_target_2905", any(row["route_id"] == "NEXT2904_0_2905" and row["selected"] for row in next_rows_data), "2905 extra-response signature/bound target selected"),
        ("VAL2904_12_branch_copies_exist", all(row["exists"] for row in branch_rows_data), "branch copies were written"),
        ("VAL2904_13_csv_outputs_parse", all(csv_parses(path) for path in csv_outputs), "all generated CSV outputs parse cleanly"),
        ("VAL2904_14_formalization_untouched_during_run", not formalization_touched(), "formalization-workbench was not touched during this run"),
    ]
    overall = all(passed for _, passed, _ in checks)
    checks.append(("VAL2904_OVERALL", overall, "2904 validation overall"))
    return [
        {
            "check_id": check_id,
            "passed": passed,
            "detail": detail,
            "generated_utc": now(),
        }
        for check_id, passed, detail in checks
    ]


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, separator, *body])


def write_doc(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 2904 - Y5 R2FR Non-EH Sector Qv Zero Priority Gate or Source Pack Under AX1090",
        "",
        f"Run: `runs/{SCRIPT_START_UTC.strftime('%Y%m%d-%H%M%S')}-Y5-R2FR-non-EH-sector-Qv-zero-priority-gate-or-source-pack-under-AX1090`",
        "Status: `Y5_R2FR_2904_conditional_non_EH_silence_theorem_derived_not_parent_signed_2905_next`",
        "Claim ceiling: `conditional_theorem_only_no_non_EH_zero_no_total_Qv_no_q_kernel_no_PiM_lock_no_Newton_no_PPN_no_R10_no_local_GR_no_GitHub_claim`",
        "",
        "## Summary",
        "",
        "2904 takes the non-EH sector problem one step forward: it derives the exact conditional contract a future parent action must satisfy for MTS novelty to be locally silent.",
        "",
        "The conditional theorem is simple in shape. For one parent branch with `v in ker(Dq)`, every retained non-EH sector must contribute either a fixed exact boundary term, a theorem-zero vertical charge, a same-branch constraint, or a sourced zero/bound before `Delta H_v^nonEH[S]` can vanish.",
        "",
        "Current MTS does **not** yet parent-sign those conditions. So this is progress, not victory: the gap has sharpened from vague coupling worry into named sector signatures.",
        "",
        "The highest-information next target is the extra/response sector, because that is the distinctive motion-time-memory channel most likely to leak local charge hair.",
        "",
        "## Source Register",
        "",
        md_table(all_rows["sources"], ["source_id", "source_path", "path_exists", "anchors_found", "role", "missing_anchors"]),
        "",
        "## Conditional Non-EH Silence Theorem",
        "",
        md_table(all_rows["theorem"], ["theorem_id", "clause", "status", "derived_statement", "blocking_gap", "valid_for_claim"]),
        "",
        "## Zero Priority Gate",
        "",
        md_table(all_rows["gate"], ["gate_id", "priority_rank", "sector", "zero_condition", "current_status", "if_not_zero", "valid_for_claim"]),
        "",
        "## Source Pack",
        "",
        md_table(all_rows["pack"], ["row_id", "symbol", "definition", "units", "current_value", "source_path", "observable_link", "valid_for_claim"]),
        "",
        "## Runner Status",
        "",
        md_table(all_rows["runner"], ["runner_id", "status", "required_components", "components_evaluable", "reason", "runner_ready", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        md_table(all_rows["claims"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        md_table(all_rows["decision"], ["decision_id", "decision", "reason", "effect", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(all_rows["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "success_condition", "fallback_condition", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(all_rows["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(all_rows["validation"], ["check_id", "passed", "detail", "generated_utc"]),
        "",
        "## Working Read",
        "",
        "This checkpoint is useful because it tells us exactly what would make the local-GR reduction respectable: not a verbal claim that MTS reduces to GR, but a same-branch covariant phase-space silence proof for the non-EH sectors.",
        "",
        "The boxing score: we have not won the round yet, but we have made the opponent stand in the middle of the ring. The next punch is not broad theory talk; it is the extra/response operator-source-boundary signature.",
        "",
        "## Forbidden Claims From 2904",
        "",
        "- Non-EH vertical `Q_v` pieces vanish in current MTS.",
        "- The conditional theorem is a parent-signed proof.",
        "- EH reference charge is the total MTS vertical charge.",
        "- `Delta_non_EH_Qv_total_over_Mref=0`, q/kernel ownership, `Pi_M` lock, source-normalized Newton, beta, PPN, R10, orbital, clock or local GR is proved.",
    ]
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    all_rows: dict[str, list[dict[str, Any]]] = {}
    all_rows["sources"] = source_register_rows()
    all_rows["theorem"] = theorem_rows()
    all_rows["gate"] = zero_priority_gate_rows()
    all_rows["pack"] = source_pack_rows()
    all_rows["runner"] = runner_rows()
    all_rows["claims"] = claim_gate_rows()
    all_rows["decision"] = decision_rows()
    all_rows["next"] = next_rows()

    for key in ["sources", "theorem", "gate", "pack", "runner", "claims", "decision", "next"]:
        write_csv(OUTPUTS[key], all_rows[key])

    all_rows["branches"] = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], all_rows["branches"])

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_doc(all_rows)

    overall = next(row["passed"] for row in all_rows["validation"] if row["check_id"] == "VAL2904_OVERALL")
    print(f"2904 validation overall: {overall}")
    print(DOC)


if __name__ == "__main__":
    main()

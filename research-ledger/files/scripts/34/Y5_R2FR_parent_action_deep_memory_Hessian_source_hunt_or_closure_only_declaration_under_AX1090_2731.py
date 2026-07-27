from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2731-Y5-R2FR-parent-action-deep-memory-Hessian-source-hunt-or-closure-only-declaration-under-AX1090.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2731_SOURCE_REGISTER.csv",
    "deep_scan": RESIDUALS / "P8_Y5_R2FR_2731_PARENT_ACTION_DEEP_SCAN.csv",
    "candidates": RESIDUALS / "P8_Y5_R2FR_2731_STRONGEST_CANDIDATE_AUDIT.csv",
    "closure": RESIDUALS / "P8_Y5_R2FR_2731_CLOSURE_ONLY_DECLARATION.csv",
    "reopen": RESIDUALS / "P8_Y5_R2FR_2731_REOPEN_CONDITIONS.csv",
    "residual": RESIDUALS / "P8_Y5_R2FR_2731_FINITE_RESIDUAL_HANDOFF.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2731_CLAIM_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_2731_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2731_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2731_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2731_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "closure": LOCAL_BOUNDS / "memory_closure_only_declaration_2731_NONCLAIM.csv",
    "reopen": SOURCE_WEIGHT / "memory_reopen_conditions_2731_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2731_LOCAL_GR_ROUTE_ROLLUP_NEXT.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()}:
        path.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def markdown_table(rows: list[dict[str, Any]], cols: list[str]) -> str:
    header = "| " + " | ".join(cols) + " |"
    sep = "| " + " | ".join("---" for _ in cols) + " |"
    body = [
        "| " + " | ".join(str(row.get(col, "")).replace("\n", " ") for col in cols) + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body])


def source_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "SRC2731_0_2730_handoff",
            "handoff selecting deep parent-action source hunt",
            DOC.parent / "2730-Y5-R2FR-memory-first-source-row-acquisition-or-local-test-refusal-smoke-under-AX1090-closure.md",
            ["NEXT2730_0_selected", "SCAN2730_5_HESSIAN_SIGNATURE_2216", "VAL2730_OVERALL"],
            "handoff",
        ),
        (
            "SRC2731_1_57_owner_contract",
            "early memory action-owner contract",
            DOC.parent / "57-memory-action-owner-contract.md",
            ["Memory Action-Owner Contract", "memory_action_owner_contract_written_not_satisfied", "does not yet have the employee"],
            "original_action_sketch",
        ),
        (
            "SRC2731_2_136_potential_owner",
            "memory potential owner attempt",
            DOC.parent / "136-memory-action-potential-owner-attempt.md",
            ["potential_map_reconstructed_not_parent_action", "Where the Parent Derivation Fails"],
            "original_action_sketch",
        ),
        (
            "SRC2731_3_137_auxiliary_owner",
            "auxiliary/geometric memory action owner attempt",
            DOC.parent / "137-auxiliary-geometric-memory-action-owner.md",
            ["auxiliary_geometric_contract_not_parent_derivation", "This is now the exact missing kernel"],
            "original_action_sketch",
        ),
        (
            "SRC2731_4_296_positive_cg",
            "positive coarse-graining parent action attempt",
            DOC.parent / "296-positive-coarse-graining-parent-action-attempt.md",
            ["A plain reversible action does not do it", "positive mobility is still a parent assumption unless derived"],
            "original_action_sketch",
        ),
        (
            "SRC2731_5_826_parent_action_ansatz",
            "candidate memory-sector action slot",
            RESIDUALS / "P8_Y5_R10_826_PARENT_ACTION_ANSATZ.csv",
            ["AA826_1_memory_sector", "candidate_coefficient_scaffold", "unsigned parent coefficients"],
            "candidate_action_row",
        ),
        (
            "SRC2731_6_970_quadratic_memory",
            "minimal quadratic memory action construction",
            DOC.parent / "970-Y5-R10-minimal-quadratic-memory-action-construction-or-strict-residual-runner.md",
            ["minimal action", "parent-signed", "strict retained residual runner"],
            "original_action_sketch",
        ),
        (
            "SRC2731_7_970_quadratic_csv",
            "machine-readable 970 construction",
            RESIDUALS / "P8_Y5_R10_970_QUADRATIC_MEMORY_ACTION_CONSTRUCTION.csv",
            ["QMA970_0_action", "FORMAL_CANDIDATE_CONSTRUCTED_NOT_PARENT_SIGNED", "QMA970_3_source_silence"],
            "candidate_action_row",
        ),
        (
            "SRC2731_8_1025_second_variation",
            "second variation contract for X-sector finite range",
            RESIDUALS / "P8_Y5_R10_1025_SECOND_VARIATION_DERIVATION.csv",
            ["SV1025_0_local_block", "CONDITIONAL_ANSATZ_ONLY", "SV1025_6_verdict"],
            "downstream_contract",
        ),
        (
            "SRC2731_9_1981_signature_hunt",
            "previous parent memory signature source hunt",
            DOC.parent / "1981-Y5-R2FR-parent-memory-action-signature-source-hunt-or-closure-activation.md",
            ["NO_CURRENT_PARENT_SIGNATURE_SOURCE", "closure-only", "HUNT1981_6_verdict"],
            "wider_hunt",
        ),
        (
            "SRC2731_10_1983_top_review",
            "top wider-corpus parent-action candidate review",
            DOC.parent / "1983-Y5-R2FR-top-parent-action-candidate-review.md",
            ["CRIT1983_1_action", "REJECT_AS_PARENT_MEMORY_SIGNATURE_SOURCE"],
            "wider_hunt",
        ),
        (
            "SRC2731_11_2216_hessian_signature",
            "parent Hessian signature extraction",
            DOC.parent / "2216-Y5-R2FR-parent-Hessian-signature-extraction-or-null-bound-rows.md",
            ["PHS2216_0_candidate_density_shape", "NOT_PARENT_SIGNED_CURRENT_CORPUS", "PHS2216_9_verdict"],
            "hessian_signature",
        ),
        (
            "SRC2731_12_2216_hessian_csv",
            "machine-readable parent Hessian signature extraction",
            RESIDUALS / "P8_Y5_PARENT_QLOC_2216_PARENT_HESSIAN_SIGNATURE_EXTRACTION.csv",
            ["PHS2216_0_candidate_density_shape", "NOT_FOUND_CURRENT_CORPUS", "parent_signed_now"],
            "hessian_signature",
        ),
        (
            "SRC2731_13_2710_parent_owner",
            "AX1090 parent action owner source hunt",
            DOC.parent / "2710-Y5-R2FR-parent-action-owner-construction-source-hunt-or-falsifier-test.md",
            ["OWNER_NOT_ACQUIRED", "AX1090_0_parent_object", "HUNT2710_7_verdict"],
            "parent_object_status",
        ),
        (
            "SRC2731_14_2712_local_EH_rollforward",
            "current local EH rollforward under AX1090 closure",
            DOC.parent / "2712-Y5-R2FR-A511-local-EH-fixed-point-rollforward-under-AX1090-closure.md",
            ["A511R2712_6_verdict", "FORMULA_SHELL_ONLY", "A511 local EH fixed point"],
            "local_gr_status",
        ),
        (
            "SRC2731_15_2728_memory_operator",
            "memory positive-operator local silence attempt",
            DOC.parent / "2728-Y5-R2FR-memory-positive-operator-local-silence-or-residual-row-under-AX1090-closure.md",
            ["RELATIVE_THEOREM_READY_ACTIVATION_FAILS", "EMEM2728_6_E_memory_scalar_generator", "VAL2728_OVERALL"],
            "direct_handoff",
        ),
        (
            "SRC2731_16_2729_parent_memory_signature",
            "parent memory signature contract plus finite residual interface",
            DOC.parent / "2729-Y5-R2FR-parent-memory-signature-contract-plus-finite-local-residual-interface-under-AX1090-closure.md",
            ["PMC2729_8_activation_verdict", "MFI2729_0_lambda_gap", "VAL2729_OVERALL"],
            "direct_handoff",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, description, path, needles, source_class in specs:
        exists = path.exists()
        text = path.read_text(encoding="utf-8", errors="ignore") if exists else ""
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "source_id": source_id,
                "description": description,
                "source_class": source_class,
                "source_path": str(path),
                "exists": exists,
                "needles_present": not missing,
                "missing_needles": ";".join(missing),
                "valid_for_claim": False,
            }
        )
    return rows


def deep_scan_rows() -> list[dict[str, Any]]:
    return [
        {
            "scan_id": "SCAN2731_0_57_owner_contract",
            "source": "57-memory-action-owner-contract.md",
            "target": "memory action/current owner",
            "positive_find": "contract for missing owner exists",
            "blocking_gap": "owner explicitly not satisfied",
            "classification": "CONTRACT_ONLY_NOT_SOURCE",
            "accepted_parent_signature": False,
            "valid_for_claim": False,
        },
        {
            "scan_id": "SCAN2731_1_136_potential_owner",
            "source": "136-memory-action-potential-owner-attempt.md",
            "target": "V(phi)/memory potential ownership",
            "positive_find": "canonical/EFT potential map can be reconstructed",
            "blocking_gap": "not a non-circular parent prediction and not a local source/boundary theorem",
            "classification": "EFT_RECONSTRUCTION_NOT_PARENT_ACTION",
            "accepted_parent_signature": False,
            "valid_for_claim": False,
        },
        {
            "scan_id": "SCAN2731_2_137_auxiliary_owner",
            "source": "137-auxiliary-geometric-memory-action-owner.md",
            "target": "auxiliary/geometric memory owner",
            "positive_find": "candidate auxiliary route names the missing kernel",
            "blocking_gap": "does not derive the required activation kernel/source package",
            "classification": "AUXILIARY_CONTRACT_NOT_DERIVED",
            "accepted_parent_signature": False,
            "valid_for_claim": False,
        },
        {
            "scan_id": "SCAN2731_3_296_positive_cg",
            "source": "296-positive-coarse-graining-parent-action-attempt.md",
            "target": "positive coarse-graining time/irreversibility",
            "positive_find": "open/influence action route is field-theory shaped",
            "blocking_gap": "positive mobility/noise kernel and environment sector are not derived from current parent action",
            "classification": "OPEN_SYSTEM_CONTRACT_UNSIGNED",
            "accepted_parent_signature": False,
            "valid_for_claim": False,
        },
        {
            "scan_id": "SCAN2731_4_826_memory_slot",
            "source": "P8_Y5_R10_826_PARENT_ACTION_ANSATZ.csv",
            "target": "memory-sector Lagrangian slot",
            "positive_find": "L_m=-1/2 Z_m(X_B) grad m grad m - V_R(m;X_B) plus sourced/bath terms is written",
            "blocking_gap": "Z_m, V_R, X_B and source/bath terms remain unsigned parent coefficients",
            "classification": "CANDIDATE_SLOT_PRESENT_NOT_PARENT_SIGNED",
            "accepted_parent_signature": False,
            "valid_for_claim": False,
        },
        {
            "scan_id": "SCAN2731_5_970_quadratic_action",
            "source": "970-Y5-R10-minimal-quadratic-memory-action-construction-or-strict-residual-runner.md",
            "target": "minimal positive operator action",
            "positive_find": "relative variation gives L_X X=J_X and energy identity if signs/source/boundary close",
            "blocking_gap": "X owner, A^ij, m_X^2, J_X, boundary class and no-tower package are not parent signed",
            "classification": "RELATIVE_ACTION_VALID_ACTIVATION_UNSIGNED",
            "accepted_parent_signature": False,
            "valid_for_claim": False,
        },
        {
            "scan_id": "SCAN2731_6_1025_second_variation",
            "source": "P8_Y5_R10_1025_SECOND_VARIATION_DERIVATION.csv",
            "target": "Z_X/M_X^2/lambda_X second variation",
            "positive_find": "exact relation lambda_X=sqrt(Z_X/M_X^2) and nohair identity are sharpened",
            "blocking_gap": "same-branch Z_X and M_X^2 signs/units/normalization remain absent",
            "classification": "EXACT_CONTRACT_VALUES_MISSING",
            "accepted_parent_signature": False,
            "valid_for_claim": False,
        },
        {
            "scan_id": "SCAN2731_7_1981_signature_hunt",
            "source": "1981-Y5-R2FR-parent-memory-action-signature-source-hunt-or-closure-activation.md",
            "target": "source-backed parent memory signature",
            "positive_find": "memory signature hunt already isolated Z_m/gap/source/boundary requirements",
            "blocking_gap": "no source-backed parent memory action signature found",
            "classification": "NO_CURRENT_PARENT_SIGNATURE_SOURCE",
            "accepted_parent_signature": False,
            "valid_for_claim": False,
        },
        {
            "scan_id": "SCAN2731_8_1983_top_candidate_review",
            "source": "1983-Y5-R2FR-top-parent-action-candidate-review.md",
            "target": "wider-corpus candidate rescue",
            "positive_find": "strict review criteria were defined and top wider-corpus hits were checked",
            "blocking_gap": "top hits rejected as parent memory signature sources",
            "classification": "WIDER_HITS_REJECTED",
            "accepted_parent_signature": False,
            "valid_for_claim": False,
        },
        {
            "scan_id": "SCAN2731_9_2216_response_doublet",
            "source": "2216-Y5-R2FR-parent-Hessian-signature-extraction-or-null-bound-rows.md",
            "target": "formal Hessian/response-doublet shape",
            "positive_find": "Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B+O(Z^4) is the best Hessian-like shape",
            "blocking_gap": "action density owner, Z basis, units/pairing, self-adjoint domain, rank/sign, source/boundary closure all unsigned",
            "classification": "FORMAL_HESSIAN_SHAPE_NOT_PARENT_SIGNED",
            "accepted_parent_signature": False,
            "valid_for_claim": False,
        },
        {
            "scan_id": "SCAN2731_10_2710_AX1090",
            "source": "2710-Y5-R2FR-parent-action-owner-construction-source-hunt-or-falsifier-test.md",
            "target": "parent action object",
            "positive_find": "AX1090_0 isolates the parent-action object as the irreducible missing object",
            "blocking_gap": "no single source signs the parent action object before readout/projection/fitting",
            "classification": "PARENT_OBJECT_NOT_ACQUIRED",
            "accepted_parent_signature": False,
            "valid_for_claim": False,
        },
        {
            "scan_id": "SCAN2731_11_2712_local_EH",
            "source": "2712-Y5-R2FR-A511-local-EH-fixed-point-rollforward-under-AX1090-closure.md",
            "target": "local EH fixed point and q_loc/Khat branch",
            "positive_find": "Gamma_eff formula shape and K_L00 formal component exist as nonclaim progress",
            "blocking_gap": "full Khat/Kmetric comparison, amplitude, units, domain and boundary terms missing",
            "classification": "LOCAL_EH_ROLLFORWARD_NOT_PROMOTION",
            "accepted_parent_signature": False,
            "valid_for_claim": False,
        },
    ]


def candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate_id": "CAND2731_0_memory_specific_strongest",
            "object": "826 memory-sector slot plus 970 quadratic memory action",
            "why_strongest": "it is the closest memory-specific action language and the variation theorem is mathematically usable",
            "what_it_gives": "candidate L_m/L_X form, Euler equation, energy identity, strict residual schema",
            "what_it_does_not_give": "parent adoption, coefficient laws, units, source-zero, boundary/no-tower, local/cosmology arena split",
            "promotion": "REJECT_PROMOTION_KEEP_AS_CONTRACT",
            "accepted_parent_signature": False,
            "valid_for_claim": False,
        },
        {
            "candidate_id": "CAND2731_1_Hessian_shape_strongest",
            "object": "2216 response-doublet Hessian M_AB",
            "why_strongest": "it is the sharpest formal Hessian shape in the current corpus",
            "what_it_gives": "Gamma_eff quadratic response shape and a concrete list of missing Hessian premises",
            "what_it_does_not_give": "accepted scalar density owner, Z basis, pairing/units, self-adjoint domain, rank/sign/coercivity, source compatibility",
            "promotion": "REJECT_PROMOTION_KEEP_AS_ACQUISITION_QUEUE",
            "accepted_parent_signature": False,
            "valid_for_claim": False,
        },
        {
            "candidate_id": "CAND2731_2_AX1090_parent_object",
            "object": "2710 parent-action owner hunt",
            "why_strongest": "it identifies the irreducible parent-object gap rather than another symptom",
            "what_it_gives": "normal form target and falsifier language for future derivation attempts",
            "what_it_does_not_give": "actual parent action variation or sector certificates",
            "promotion": "REJECT_PROMOTION_USE_AS_REOPEN_GATE",
            "accepted_parent_signature": False,
            "valid_for_claim": False,
        },
    ]


def closure_rows() -> list[dict[str, Any]]:
    return [
        {
            "closure_id": "CLOS2731_0_scope",
            "route": "memory_positive_operator_local_silence_route",
            "status": "CLOSURE_ONLY_UNDER_CURRENT_CORPUS",
            "scope_guard": "this demotes only the memory positive-operator zero route, not the whole MTS framework",
            "reason": "no parent-signed memory Hessian/source-current owner is found in original sketches, wider hunts, or downstream ledgers",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "closure_id": "CLOS2731_1_not_activated",
            "route": "local_GR_Newton_R10_PPN_WEP_clock_orbital",
            "status": "NO_CLAIM_OPENED",
            "scope_guard": "closure is a label for missing derivation evidence, not a substitute axiom for tests",
            "reason": "placeholder Z_X/M_X^2/J_X/boundary/projection rows still refuse scoring",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "closure_id": "CLOS2731_2_retained_working_value",
            "route": "finite_memory_residual_interface",
            "status": "ACTIVE_NONCLAIM",
            "scope_guard": "keep the residual vector explicit instead of hiding it",
            "reason": "E_memory_scalar_generator and finite residual rows remain the honest local-test interface",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def reopen_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition_id": "REOPEN2731_0_parent_action_owner",
            "required_input": "one parent action density or variational principle owning the memory/X sector before readout",
            "minimum_payload": "field variables, action density, metric/coframe dependence, variation order, source path",
            "current_status": "MISSING_PARENT_ACTION_OWNER",
            "reopens_route": True,
            "valid_for_claim": False,
        },
        {
            "condition_id": "REOPEN2731_1_field_basis",
            "required_input": "physical local residual basis for X or Z^A",
            "minimum_payload": "quotient basis, gauge/null split, map into q_loc/PPN/source directions",
            "current_status": "MISSING_FIELD_BASIS_AND_NULL_PROJECTOR",
            "reopens_route": True,
            "valid_for_claim": False,
        },
        {
            "condition_id": "REOPEN2731_2_units_pairing",
            "required_input": "inner product, measure, units and normalization ledger",
            "minimum_payload": "same units for Z_X/M_X^2/J_X/boundary/source projection and SI/natural-unit bridge",
            "current_status": "MISSING_UNITS_PAIRING",
            "reopens_route": True,
            "valid_for_claim": False,
        },
        {
            "condition_id": "REOPEN2731_3_positive_operator",
            "required_input": "positive gradient coefficient and strict/nonnegative mass-gap theorem",
            "minimum_payload": "Z_min>0, M2_min>=0 or gap floor after zero-mode removal, cross-Hessian Schur policy",
            "current_status": "MISSING_SIGN_AND_COERCIVITY_THEOREM",
            "reopens_route": True,
            "valid_for_claim": False,
        },
        {
            "condition_id": "REOPEN2731_4_source_silence_or_bound",
            "required_input": "J_X=0 theorem or finite source norm rows",
            "minimum_payload": "matter, chi_D wall, boundary exchange, readout and history source decomposition",
            "current_status": "MISSING_SOURCE_ZERO_OR_NUMERIC_BOUND",
            "reopens_route": True,
            "valid_for_claim": False,
        },
        {
            "condition_id": "REOPEN2731_5_boundary_no_tower",
            "required_input": "self-adjoint domain, boundary zero/no-flux, and no integrated-out tower certificate",
            "minimum_payload": "boundary class, zero-mode rule, projection leakage audit, effective-action tower audit",
            "current_status": "MISSING_BOUNDARY_AND_TOWER_PACKAGE",
            "reopens_route": True,
            "valid_for_claim": False,
        },
        {
            "condition_id": "REOPEN2731_6_observable_projection",
            "required_input": "arena projection coefficients for R10, PPN, clocks, orbital and source-mass tests",
            "minimum_payload": "K_R10, K_PPN, K_clock, K_orbital, qbar_XT/beta numerator with source paths",
            "current_status": "MISSING_ARENA_PROJECTION",
            "reopens_route": True,
            "valid_for_claim": False,
        },
    ]


def residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "handoff_id": "FRH2731_0_E_memory_scalar_generator",
            "residual_object": "E_memory_scalar_generator",
            "source_anchor": "2728/2729 finite residual interface",
            "status": "RETAIN_ACTIVE_NONCLAIM",
            "why": "memory silence did not activate, so local tests must see explicit residual rows",
            "next_input_needed": "lambda_gap, source norm, boundary norm, and arena projection coefficients",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "handoff_id": "FRH2731_1_R10_alpha",
            "residual_object": "memory alpha(lambda) smoke row",
            "source_anchor": "2729/2730 refusal smoke",
            "status": "REFUSE_UNTIL_PARENT_COEFFICIENTS",
            "why": "R10 scoring still lacks source-backed numerator and range inputs",
            "next_input_needed": "Z_X, M_X^2, K_X, Qbar_XH, qbar_XT, real bound curve",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "handoff_id": "FRH2731_2_local_GR",
            "residual_object": "q_loc/Khat/local EH branch",
            "source_anchor": "2712 local EH rollforward",
            "status": "KEEP_SEPARATE_FROM_MEMORY_CLOSURE",
            "why": "q_loc/Khat tensor side remains a distinct route and should not inherit memory closure credit",
            "next_input_needed": "Kmetric derivative/domain/boundary term or Delta_K amplitude row",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    claims = [
        ("GATE2731_0_memory_zero", "memory X=0 theorem-zero", "parent action owner/sign/source/boundary missing"),
        ("GATE2731_1_local_GR", "derived local GR/Newton", "A511/AX1090 parent object and q_loc/Khat remain unsigned"),
        ("GATE2731_2_R10", "R10 finite-range pass", "alpha(lambda) row lacks parent coefficients and real source-backed range"),
        ("GATE2731_3_PPN", "PPN pass", "projection coefficients and residual vector are missing"),
        ("GATE2731_4_WEP", "WEP pass", "matter functor/source-blind theorem remains conditional"),
        ("GATE2731_5_clock", "clock/time-drift pass", "K_clock/Gdot projection row missing"),
        ("GATE2731_6_orbital", "orbital/local system pass", "source mass/readout/boundary residual not bounded"),
        ("GATE2731_7_public", "public claim", "2731 is private closure/source-hunt discipline only"),
    ]
    return [
        {
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": False,
            "reason": reason,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for gate_id, claim, reason in claims
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2731_0_deep_hunt_result",
            "decision": "NO_PARENT_SIGNED_MEMORY_HESSIAN_SOURCE_FOUND",
            "because": "original sketches and later ledgers contain contracts/candidate actions, not a signed parent variation",
            "effect": "do not run/score local tests from placeholders",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2731_1_demote_route",
            "decision": "MEMORY_POSITIVE_OPERATOR_ROUTE_CLOSURE_ONLY",
            "because": "the relative theorem is good but activation premises are absent",
            "effect": "closure label is explicit and scoped; finite residual interface remains live",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2731_2_best_next",
            "decision": "LOCAL_GR_ROUTE_ROLLUP_AFTER_MEMORY_CLOSURE",
            "because": "to avoid circling, consolidate which derivation branch still has a live non-closure route",
            "effect": "choose next target between q_loc/Khat tensor work, parent-object grammar, or empirical residual rows",
            "valid_for_claim": False,
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2731_0_selected",
            "status": "selected_primary",
            "target_doc": "2732-Y5-R2FR-local-GR-route-rollup-after-memory-closure-only-or-next-derivation-branch.md",
            "target_script": "scripts/Y5_R2FR_local_GR_route_rollup_after_memory_closure_only_or_next_derivation_branch_2732.py",
            "mission": "stop circling the memory zero route; roll up the surviving local-GR branches and pick the next derivation route that is not already closure-only",
            "acceptance": "explicit branch ranking for q_loc/Khat, AX1090 parent object, source-measure/EH, and empirical residual rows",
            "forbidden": "promoting memory closure to local-GR evidence; GitHub action; formalization-workbench edits",
            "selected": True,
            "valid_for_claim": False,
        }
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": "COPY2731_0_closure",
            "source_table": str(OUTPUTS["closure"]),
            "copy_path": str(BRANCH_OUTPUTS["closure"]),
            "purpose": "local bounds branch receives scoped closure-only declaration",
            "exists": BRANCH_OUTPUTS["closure"].exists(),
            "valid_for_claim": False,
        },
        {
            "copy_id": "COPY2731_1_reopen",
            "source_table": str(OUTPUTS["reopen"]),
            "copy_path": str(BRANCH_OUTPUTS["reopen"]),
            "purpose": "source-weight branch receives exact reopen conditions",
            "exists": BRANCH_OUTPUTS["reopen"].exists(),
            "valid_for_claim": False,
        },
        {
            "copy_id": "COPY2731_2_next_queue",
            "source_table": str(OUTPUTS["next"]),
            "copy_path": str(BRANCH_OUTPUTS["next_queue"]),
            "purpose": "queues local-GR route rollup after memory closure-only decision",
            "exists": BRANCH_OUTPUTS["next_queue"].exists(),
            "valid_for_claim": False,
        },
    ]


def formalization_recent_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            if modified > SCRIPT_START_UTC:
                count += 1
    return count


def validation_rows(
    sources: list[dict[str, Any]],
    deep_scan: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    closure: list[dict[str, Any]],
    reopen: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_ok = all(row["exists"] is True and row["needles_present"] is True for row in sources)
    original_source_count = sum(row["source_class"] == "original_action_sketch" for row in sources)
    deep_scan_ok = len(deep_scan) >= 10 and all(row["accepted_parent_signature"] is False for row in deep_scan)
    candidate_ok = len(candidates) >= 3 and all(row["accepted_parent_signature"] is False for row in candidates)
    closure_scoped = any(
        row["route"] == "memory_positive_operator_local_silence_route"
        and row["status"] == "CLOSURE_ONLY_UNDER_CURRENT_CORPUS"
        and "not the whole MTS framework" in row["scope_guard"]
        for row in closure
    )
    residual_retained = any(row["residual_object"] == "E_memory_scalar_generator" for row in residual_rows())
    reopen_ok = len(reopen) >= 7 and all(row["reopens_route"] is True for row in reopen)
    gates_false = all(row["gate_pass"] is False and row["claim_allowed"] is False for row in gates)
    branch_ok = all(path.exists() for path in BRANCH_OUTPUTS.values())
    formalization_ok = formalization_recent_count() == 0
    csv_ok = True
    csv_bits = []
    for key, path in {**OUTPUTS, **BRANCH_OUTPUTS}.items():
        if key == "validation":
            continue
        try:
            rows = read_csv(path)
            csv_bits.append(f"{path.name}:{len(rows)}:ok")
        except Exception as exc:
            csv_ok = False
            csv_bits.append(f"{path.name}:ERROR:{exc}")
    rows = [
        {"validation_id": "VAL2731_0_sources", "passed": source_ok, "detail": "all source paths exist and needles are present", "timestamp_utc": ts()},
        {"validation_id": "VAL2731_1_original_sketch_coverage", "passed": original_source_count >= 5, "detail": f"original/action-sketch sources covered = {original_source_count}", "timestamp_utc": ts()},
        {"validation_id": "VAL2731_2_deep_scan_no_promotion", "passed": deep_scan_ok, "detail": "deep scan accepts no parent-signed memory Hessian/action source", "timestamp_utc": ts()},
        {"validation_id": "VAL2731_3_strongest_candidates_no_promotion", "passed": candidate_ok, "detail": "strongest memory/action/Hessian candidates are retained as contracts only", "timestamp_utc": ts()},
        {"validation_id": "VAL2731_4_closure_scoped", "passed": closure_scoped, "detail": "closure-only declaration is scoped to memory positive-operator route", "timestamp_utc": ts()},
        {"validation_id": "VAL2731_5_residual_retained", "passed": residual_retained, "detail": "finite memory residual interface remains active nonclaim", "timestamp_utc": ts()},
        {"validation_id": "VAL2731_6_reopen_conditions", "passed": reopen_ok, "detail": "reopen conditions are explicit and parent-action/source-ready", "timestamp_utc": ts()},
        {"validation_id": "VAL2731_7_claim_gates_false", "passed": gates_false, "detail": "all local/test/GR/public claim gates remain false", "timestamp_utc": ts()},
        {"validation_id": "VAL2731_8_branch_outputs", "passed": branch_ok, "detail": "branch copies exist", "timestamp_utc": ts()},
        {"validation_id": "VAL2731_9_csv_parse", "passed": csv_ok, "detail": "; ".join(csv_bits), "timestamp_utc": ts()},
        {"validation_id": "VAL2731_10_formalization_untouched", "passed": formalization_ok, "detail": f"formalization-workbench recent modified-file count since script start = {formalization_recent_count()}", "timestamp_utc": ts()},
    ]
    rows.append(
        {
            "validation_id": "VAL2731_OVERALL",
            "passed": all(row["passed"] is True for row in rows),
            "detail": "2731 finds no parent-signed memory Hessian/action source and demotes only the memory positive-operator route to closure-only",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        f"""# 2731 - Y5 R2/f(R): Parent-Action Deep Memory Hessian Source Hunt Or Closure-Only Declaration Under AX1090

Status: `Y5_R2FR_2731_memory_positive_operator_route_closure_only_current_corpus_nonclaim`

## Private Verdict

I went after the real thing: not another downstream placeholder scan, but the original/action-sketch material that could have owned the memory Hessian or source current.

The hunt does **not** find a parent-signed memory Hessian/action source. The best memory-specific material is still a candidate action slot plus a relative quadratic action. The best Hessian-like material is still the response-doublet shape. Both are useful; neither signs the parent action, units, source silence, boundary class, or positive/coercive operator package.

So 2731 makes the clean move: the **memory positive-operator local-silence route** is closure-only under the current corpus. This is deliberately scoped. It does not demote the whole MTS framework, and it does not stop the q_loc/Khat/local-GR route. It just stops us from pretending the memory zero theorem is derived when the parent signature is still absent.

No local-GR, Newton, R10, PPN, WEP, clock, orbital, or public claim follows from this checkpoint.

## Source Register

{markdown_table(data["sources"], ["source_id", "description", "source_class", "source_path", "exists", "needles_present", "missing_needles", "valid_for_claim"])}

## Parent-Action Deep Scan

{markdown_table(data["deep_scan"], ["scan_id", "source", "target", "positive_find", "blocking_gap", "classification", "accepted_parent_signature", "valid_for_claim"])}

## Strongest Candidate Audit

{markdown_table(data["candidates"], ["candidate_id", "object", "why_strongest", "what_it_gives", "what_it_does_not_give", "promotion", "accepted_parent_signature", "valid_for_claim"])}

## Closure-Only Declaration

{markdown_table(data["closure"], ["closure_id", "route", "status", "scope_guard", "reason", "claim_allowed", "valid_for_claim"])}

## Reopen Conditions

{markdown_table(data["reopen"], ["condition_id", "required_input", "minimum_payload", "current_status", "reopens_route", "valid_for_claim"])}

## Finite Residual Handoff

{markdown_table(data["residual"], ["handoff_id", "residual_object", "source_anchor", "status", "why", "next_input_needed", "score_ready", "valid_for_claim"])}

## Claim Gates

{markdown_table(data["gates"], ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"])}

## Decision Ledger

{markdown_table(data["decisions"], ["decision_id", "decision", "because", "effect", "valid_for_claim"])}

## Next Target

{markdown_table(data["next"], ["next_id", "status", "target_doc", "target_script", "mission", "acceptance", "forbidden", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(data["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(data["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}

## Plain-English Read

This is not a defeat; it is a boundary marker. We now know the memory-positive-operator route is not where the immediate leap is hiding unless new parent-action text appears. The useful next move is to roll up the remaining local-GR routes and choose the one that still has a derivable path rather than another closure loop.
""",
        encoding="utf-8",
    )


def main() -> None:
    ensure_dirs()
    sources = source_rows()
    deep_scan = deep_scan_rows()
    candidates = candidate_rows()
    closure = closure_rows()
    reopen = reopen_rows()
    residual = residual_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["deep_scan"], deep_scan)
    write_csv(OUTPUTS["candidates"], candidates)
    write_csv(OUTPUTS["closure"], closure)
    write_csv(OUTPUTS["reopen"], reopen)
    write_csv(OUTPUTS["residual"], residual)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    write_csv(BRANCH_OUTPUTS["closure"], closure)
    write_csv(BRANCH_OUTPUTS["reopen"], reopen)
    write_csv(BRANCH_OUTPUTS["next_queue"], next_target)
    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)

    validation = validation_rows(sources, deep_scan, candidates, closure, reopen, gates)
    write_csv(OUTPUTS["validation"], validation)

    data = {
        "sources": sources,
        "deep_scan": deep_scan,
        "candidates": candidates,
        "closure": closure,
        "reopen": reopen,
        "residual": residual,
        "gates": gates,
        "decisions": decisions,
        "next": next_target,
        "branches": branches,
        "validation": validation,
    }
    write_doc(data)

    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    if not all(row["passed"] is True for row in validation):
        failed = [row for row in validation if row["passed"] is not True]
        raise SystemExit(f"2731 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

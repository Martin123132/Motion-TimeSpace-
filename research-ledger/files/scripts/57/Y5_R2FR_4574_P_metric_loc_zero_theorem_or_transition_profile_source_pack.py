from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4574"
CLAIM_ID = "L-416"
BRANCH_ID = "MTS_R2FR_Y5_PMETRIC_LOC_ZERO_THEOREM_OR_PROFILE_SOURCE_PACK_4574"
MARKER = "PPC4161_PMETRIC_LOC_ZERO_THEOREM_OR_PROFILE_SOURCE_PACK_4574"
PACKET_MARKER = "PPC4161_PACKET_PMETRIC_LOC_ZERO_THEOREM_PROFILE_SOURCE_PACK_4574"
DECISION = "PMETRIC_ZERO_DERIVED_AS_GRAM_MOMENT_CRITERION_NOT_PARENT_SIGNED_PROFILE_SOURCE_PACK_READY_NONCLAIM"
NEXT_TARGET = "4575-Y5-R2FR-transition-moment-zero-law-or-first-source-profile-matrix.md"

FORMAL_PATH = FORMAL / "590-PPC4161-P-metric-loc-zero-theorem-or-transition-profile-source-pack.md"
DOC_PATH = POST / "4574-Y5-R2FR-P_metric-loc-zero-theorem-or-transition-profile-source-pack.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

DOC_4573_FORMAL = FORMAL / "589-PPC4161-transition-shell-source-lift-or-Sigma-metric-profile-runner.md"
CSV_4573_CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_4573_SOURCE_LIFT_ZERO_CONTRACT.csv"
CSV_4573_PROFILE = SOURCE_DIR / "P8_Y5_R2FR_4573_SIGMA_METRIC_PROFILE_RUNNER_ROWS.csv"
CSV_4573_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4573_NEXT_TARGET.csv"
DOC_133 = FORMAL / "133-exact-transition-cancellation-or-projector-theorem.md"
DOC_135 = FORMAL / "135-quarantine-projector-parent-origin.md"
DOC_136 = FORMAL / "136-metric-response-kernel-theorem.md"
DOC_137 = FORMAL / "137-transition-source-lift-action-block.md"
DOC_138 = FORMAL / "138-metric-null-action-block-contract.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
EQ_REGISTER = FORMAL / "05-equation-register.md"
DOC_102 = FORMAL / "102-transition-closure-observable-threshold-spec.md"
CSV_3498_NATURALITY = SOURCE_DIR / "P8_Y5_R2FR_3498_PROJECTOR_NATURALITY_THEOREM.csv"
CSV_3572_NATURALITY = SOURCE_DIR / "P8_Y5_R2FR_3572_PROJECTOR_NATURALITY_PROOF.csv"
CSV_4417_DERIVATION = SOURCE_DIR / "P8_Y5_R2FR_4417_DERIVATION_ROWS.csv"
CSV_4417_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4417_PROJECTOR_COMMUTATOR_OUTPUT.csv"
CSV_4292_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4292_TRANSITION_MEMBERSHIP_AUDIT.csv"
CSV_4295_PLEAK = SOURCE_DIR / "P8_Y5_R2FR_4295_PLEAK_DECOMPOSITION.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4574_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4574_GRAM_PROJECTOR_THEOREM.csv"
MOMENT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4574_MOMENT_ZERO_CONDITIONS.csv"
MATRIX_PACK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4574_SOURCE_PROFILE_MATRIX_PACK.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4574_PROJECTOR_MOMENT_CONTROL_ROWS.csv"
BRANCH_CSV = SOURCE_DIR / "P8_Y5_R2FR_4574_PROJECTOR_BRANCH_VERDICT.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4574_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4574_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4574_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4574_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4574_VALIDATION.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "\n"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>")
                for header in headers
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def append_once(path: Path, marker: str, block: str) -> None:
    existing = read_text(path)
    if marker in existing:
        return
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + block.strip() + "\n")


def source_rows() -> list[dict[str, Any]]:
    source_specs = [
        ("SRC4574_00_4573_formal", "4573 source-lift contract document", DOC_4573_FORMAL, "Sigma_metric[q_tr] :="),
        ("SRC4574_01_4573_contract", "4573 projector orthogonality row", CSV_4573_CONTRACT, "ZC4573_2_projector_orthogonality"),
        ("SRC4574_02_4573_profile", "4573 P_metric profile row", CSV_4573_PROFILE, "PR4573_1_pmetric_qtr"),
        ("SRC4574_03_4573_next", "4573 selected P_metric target", CSV_4573_NEXT, "P_metric-loc-zero-theorem"),
        ("SRC4574_04_133_projector", "133 exact transition projector gate", DOC_133, "P_metric_projector_suppression_parent_derived = false"),
        ("SRC4574_05_135_kernel", "135 kernel route identification", DOC_135, "q_tr in Ker(R_loc)"),
        ("SRC4574_06_136_response", "136 response chain and source lift", DOC_136, "Sigma_metric^{mu nu}[q_tr]"),
        ("SRC4574_07_137_action", "137 action/source-lift route", DOC_137, "q_tr couples to owner variables only"),
        ("SRC4574_08_138_contract", "138 metric-null action contract", DOC_138, "C4. Projector Partition"),
        ("SRC4574_09_redteam_kernel", "red-team projector kernel warning", RED_TEAM, "the only clean projector route is now identified as a metric-response kernel"),
        ("SRC4574_10_eq_threshold", "equation register P_metric threshold", EQ_REGISTER, "P_metric,loc <= 4.212667126774669e-17"),
        ("SRC4574_11_closure_observable", "102 no-leak observable threshold", DOC_102, "local_current_leak_norm = ||P_metric,loc q_tr||"),
        ("SRC4574_12_3498_naturality", "3498 projector naturality theorem", CSV_3498_NATURALITY, "PNT3498_1_functor_chain_rule"),
        ("SRC4574_13_3572_naturality", "3572 projector naturality proof", CSV_3572_NATURALITY, "PN3572_2_chain_rule_zero"),
        ("SRC4574_14_4417_derivation", "4417 projector commutator scope", CSV_4417_DERIVATION, "PROJ4417_1_scope_guard"),
        ("SRC4574_15_4417_output", "4417 metric stress separate flag", CSV_4417_OUTPUT, "metric_stress_separate"),
        ("SRC4574_16_4292_membership", "4292 transition membership audit", CSV_4292_AUDIT, "MA4292_0_parent_source_action"),
        ("SRC4574_17_4295_pleak", "4295 leak projector components", CSV_4295_PLEAK, "PLEAK4295_0"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, label, path, needle in source_specs:
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "label": label,
                "source_path": str(path),
                "exists": bool_text(path.exists()),
                "needle": needle,
                "needle_found": bool_text(needle in text),
                "role": "P_metric,loc Gram projector theorem and transition profile source pack",
                "valid_for_claim": "False",
            }
        )
    return rows


def theorem_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "GPT4574_0_response_space",
            "statement": "Define H_metric(W_loc) as the finite local metric-response source space spanned by arena basis tensors E_i^{mu nu}.",
            "formula": "G_ij := <E_i,E_j>_loc, with <A,B>_loc := integral_Wloc A_{mu nu} G_loc^{mu nu rho sigma} B_{rho sigma}",
            "proof_status": "DEFINITION_REDUCES_PROJECTOR_TO_LINEAR_ALGEBRA",
            "parent_signed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "GPT4574_1_projector_formula",
            "statement": "If G_ij is non-degenerate, the local metric projector is fixed by Gram projection rather than chosen by hand.",
            "formula": "P_metric,loc Sigma = sum_{i,j} E_i (G^{-1})^{ij} <E_j,Sigma_metric[q_tr]>_loc",
            "proof_status": "CONDITIONAL_EXACT_PROJECTOR_FORMULA",
            "parent_signed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "GPT4574_2_zero_equivalence",
            "statement": "P_metric,loc q_tr=0 is equivalent to all local metric moments of the lifted transition source vanishing.",
            "formula": "P_metric,loc Sigma_metric[q_tr]=0 iff M_i[q_tr] := <E_i,Sigma_metric[q_tr]>_loc = 0 for every i",
            "proof_status": "DERIVED_AS_GRAM_MOMENT_CRITERION",
            "parent_signed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "GPT4574_3_norm_bound",
            "statement": "If exact moment-zero fails, the same theorem gives a finite scoring law instead of a closure switch.",
            "formula": "||P_metric,loc Sigma||_loc^2 = M_i (G^{-1})^{ij} M_j <= epsilon_metric_tr^2",
            "proof_status": "FINITE_PROFILE_MATRIX_BOUND_DERIVED",
            "parent_signed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "GPT4574_4_variation_guard",
            "statement": "Projector naturality closes independent-Gamma commutators, but metric/coframe projector stress is a separate term.",
            "formula": "delta_g(P_metric Sigma)= (delta_g P_metric) Sigma + P_metric delta_g Sigma",
            "proof_status": "METRIC_VARIATION_GUARD_REQUIRED",
            "parent_signed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def moment_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "condition_id": "MZ4574_0_topological_boundary",
            "moment_zero_route": "topological or exact boundary transition source",
            "zero_law": "Sigma_metric[q_tr]=nabla_alpha U^{alpha mu nu} with zero W_loc boundary pairing",
            "moment_result": "M_i=0 by integration by parts/self-adjoint boundary silence",
            "current_status": "PRIVATE_SUPPORT_SEPARATED_ONLY",
            "next_input": "parent-owned U^{alpha mu nu} or boundary pullback proof",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "condition_id": "MZ4574_1_pure_gauge",
            "moment_zero_route": "pure gauge metric source lift",
            "zero_law": "Sigma_metric[q_tr]=E_loc[L_xi g] or a Ward-exact variation",
            "moment_result": "M_i=0 for gauge-invariant local arena readouts",
            "current_status": "WARD_ROUTE_NOT_PARENT_SIGNED",
            "next_input": "transition Ward identity and gauge-invariant arena basis",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "condition_id": "MZ4574_2_hilbert_monopole",
            "moment_zero_route": "same-worldtube Hilbert monopole absorption",
            "zero_law": "Sigma_metric[q_tr] contributes only to common l=0 calibrated M_H^dress, with no residual moment orthogonal to E_i",
            "moment_result": "all residual M_i vanish after universal common-mode mass calibration",
            "current_status": "UNSIGNED_FOR_RAW_TRANSITION",
            "next_input": "same source action, support-before-readout, once-only count, static l=0 and zero hair",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "condition_id": "MZ4574_3_symmetry_orthogonality",
            "moment_zero_route": "representation/symmetry orthogonality",
            "zero_law": "Sigma_metric[q_tr] lies in an irreducible sector orthogonal to all scalar/local PPN source tensors E_i",
            "moment_result": "M_i=0 by representation orthogonality, not by fitted suppression",
            "current_status": "NOT_SIGNED_FOR_TRANSITION_SOURCE",
            "next_input": "parent representation labels for Sigma_metric[q_tr] and E_i basis",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "condition_id": "MZ4574_4_numeric_profile",
            "moment_zero_route": "finite source-backed profile matrix",
            "zero_law": "M_i (G^{-1})^{ij} M_j <= (4.212667126774669e-17)^2",
            "moment_result": "PPN/R10/clock/orbital local leakage bounded if all profile/source rows are numeric and sourced",
            "current_status": "PROFILE_MATRIX_VALUES_MISSING",
            "next_input": "E_i, G_ij, M_i, Sigma_metric[q_tr], boundary and K_perp rows",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def matrix_pack_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "input_id": "SPM4574_0_basis",
            "required_object": "local metric response basis E_i^{mu nu}",
            "formula_or_schema": "E_i spans PPN gamma/beta/preferred-frame, R10 finite-range, clock and orbital readout source directions",
            "current_value": "MISSING_PARENT_RESPONSE_BASIS",
            "units": "metric source tensor basis",
            "status": "MISSING_ARENA_PROJECTION",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "input_id": "SPM4574_1_gram",
            "required_object": "Gram matrix G_ij",
            "formula_or_schema": "G_ij=<E_i,E_j>_loc",
            "current_value": "MISSING_NUMERIC_OR_SYMBOLIC_GRAM",
            "units": "arena source inner-product",
            "status": "MISSING_ARENA_PROJECTION",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "input_id": "SPM4574_2_source_lift",
            "required_object": "Sigma_metric[q_tr]",
            "formula_or_schema": "(2/sqrt(-g_obs)) delta S_tr[q_tr,g_obs]/delta g_obs",
            "current_value": "MISSING_PARENT_ACTION_OR_SOURCE_LIFT",
            "units": "metric stress/source response",
            "status": "MISSING_PARENT_INPUT",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "input_id": "SPM4574_3_moments",
            "required_object": "moment vector M_i[q_tr]",
            "formula_or_schema": "M_i=<E_i,Sigma_metric[q_tr]>_loc",
            "current_value": "MISSING_MOMENT_VECTOR",
            "units": "arena source pairing",
            "status": "MISSING_PROFILE_MATRIX",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "input_id": "SPM4574_4_projector_norm",
            "required_object": "projector leakage norm",
            "formula_or_schema": "epsilon_Pmetric^2=M_i (G^{-1})^{ij} M_j",
            "current_value": "MISSING_COMPUTABLE_MOMENT_NORM",
            "units": "dimensionless after M_H_ref normalization",
            "status": "MISSING_PROFILE_MATRIX",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "input_id": "SPM4574_5_variation_stress",
            "required_object": "metric/coframe projector stress row",
            "formula_or_schema": "S_i=(delta_g P_metric,loc Sigma)_i",
            "current_value": "MISSING_METRIC_VARIATION_ROW",
            "units": "PPN/tensor response",
            "status": "MISSING_METRIC_STRESS_BOUND",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "input_id": "SPM4574_6_boundary_Kperp",
            "required_object": "boundary and K_perp completion rows",
            "formula_or_schema": "B_boundary + K_perp <= arena budget or zero theorem",
            "current_value": "MISSING_BOUNDARY_OR_KPERP_THEOREM",
            "units": "PPN/tensor response",
            "status": "MISSING_BOUNDARY_KPERP_INPUT",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    controls = [
        ("CTRL4574_zero_moments", "all M_i=0", "0.0", "4.212667126774669e-17"),
        ("CTRL4574_below_threshold", "sqrt(M^T G^-1 M)", "1.0e-18", "4.212667126774669e-17"),
        ("CTRL4574_above_threshold", "sqrt(M^T G^-1 M)", "1.0e-10", "4.212667126774669e-17"),
        ("LIVE4574_missing_matrix", "sqrt(M^T G^-1 M)", "MISSING_PROFILE_MATRIX", "4.212667126774669e-17"),
    ]
    for control_id, quantity, value, threshold in controls:
        try:
            verdict = "CONTROL_PASS_NONCLAIM" if float(value) <= float(threshold) else "CONTROL_FAIL_NONCLAIM"
        except ValueError:
            verdict = "BLOCKED_PENDING_PROFILE_MATRIX"
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "branch": BRANCH_ID,
                "generated_utc": now,
                "control_id": control_id,
                "quantity": quantity,
                "value": value,
                "threshold": threshold,
                "verdict": verdict,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def branch_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "branch_id": "PB4574_0_projector_theorem_shape",
            "question": "Can P_metric,loc q_tr=0 be derived without setting P_metric,loc=0 by hand?",
            "answer": "Yes as a conditional theorem shape: all Gram moments M_i[q_tr] vanish.",
            "status": "CONDITIONAL_GRAM_MOMENT_CRITERION_DERIVED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "branch_id": "PB4574_1_parent_signature",
            "question": "Are the moment-zero clauses parent-signed for the raw transition shell?",
            "answer": "No. Current corpus signs only restricted support separation; raw shell source lift, basis and moments remain missing.",
            "status": "RAW_TRANSITION_NOT_PARENT_SIGNED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "branch_id": "PB4574_2_source_pack",
            "question": "If zero proof fails, is there now a finite scoring route?",
            "answer": "Yes. Fill E_i, G_ij, Sigma_metric[q_tr], M_i, metric-stress, boundary and K_perp rows.",
            "status": "PROFILE_SOURCE_PACK_READY",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def promotion_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "gate_id": "PG4574_0_exact_zero",
            "gate": "All M_i[q_tr]=0 by a parent-signed theorem.",
            "status": "FAIL",
            "reason": "The Gram criterion is derived, but no parent theorem currently supplies all moment zeros for the raw shell.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "gate_id": "PG4574_1_finite_bound",
            "gate": "M_i (G^{-1})^{ij} M_j <= (4.212667126774669e-17)^2 with sourced matrix rows.",
            "status": "FAIL",
            "reason": "E_i, G_ij, Sigma_metric and M_i rows are still missing.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "gate_id": "PG4574_2_nonclosure",
            "gate": "No fitted/tiny P_metric,loc switch is used.",
            "status": "PASS",
            "reason": "4574 replaces the switch with moment-zero identities or profile-matrix scoring.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "decision": DECISION,
            "gram_moment_criterion_derived": "True",
            "raw_shell_parent_signed": "False",
            "profile_source_pack_ready": "True",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "next_target": NEXT_TARGET,
        }
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "decision": DECISION,
            "status_id": "STATUS4574_0",
            "status": "PMETRIC_REDUCED_TO_MOMENT_ZERO_OR_PROFILE_MATRIX_NONCLAIM",
            "summary": "4574 derives the non-handwavy projector criterion: P_metric,loc Sigma_metric[q_tr]=0 iff all local metric response moments M_i=<E_i,Sigma_metric[q_tr]> vanish. The raw transition shell is not parent-signed yet, but the next test is now exact: prove the moment-zero law or fill the profile matrix.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "next_target": NEXT_TARGET,
            "reason": "The decisive object is now the moment vector M_i[q_tr]. Either derive M_i=0 from a parent source-lift/symmetry law, or build the first sourced E_i/G_ij/M_i profile matrix.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def doc_body(
    now: str,
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    moments: list[dict[str, Any]],
    matrix_pack: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    branches: list[dict[str, Any]],
    promotions: list[dict[str, Any]],
) -> str:
    return f"""# 4574 — P_metric,loc zero theorem or transition profile source pack

Marker: `{MARKER}`  
Generated: `{now}`  
Decision: `{DECISION}`

## Short verdict

This checkpoint makes a real forward move: `P_metric,loc q_tr=0` is no longer a hand-imposed switch.  It has an exact projector theorem shape.

Let `E_i^{{mu nu}}` span the local metric-response arena directions and define:

```text
G_ij := <E_i,E_j>_loc
M_i[q_tr] := <E_i,Sigma_metric[q_tr]>_loc
P_metric,loc Sigma_metric[q_tr]
  = sum_ij E_i (G^-1)^ij M_j[q_tr].
```

Therefore:

```text
P_metric,loc Sigma_metric[q_tr] = 0
iff
M_i[q_tr] = 0 for every local metric-response basis direction E_i.
```

That is the clean derivation.  What is not yet done is parent-signing the moment-zero law for the raw transition shell.

## Why this matters

The old closure said:

```text
P_metric,loc = 0.
```

The 4574 replacement says:

```text
the lifted transition source has zero pairing with every local metric response mode.
```

That can be proved by topology, gauge/Ward identity, same-worldtube Hilbert monopole absorption, representation orthogonality, or it can be tested by a finite profile matrix.  No tiny fitted projector is allowed.

## Gram projector theorem

{markdown_table(theorem)}

## Moment-zero routes

{markdown_table(moments)}

## Source profile matrix pack

{markdown_table(matrix_pack)}

## Control rows

{markdown_table(controls)}

## Branch verdict

{markdown_table(branches)}

## Promotion gates

{markdown_table(promotions)}

## Source register

{markdown_table(sources)}

## Next target

`{NEXT_TARGET}`

Reason: prove the moment-zero law `M_i[q_tr]=0`, or build the first sourced `E_i/G_ij/M_i` matrix.
"""


def spine_block(now: str) -> str:
    return f"""## PPC4161 4574 P_metric Gram/moment theorem

Marker: `{MARKER}`  
Generated: `{now}`

4574 replaces the closure switch `P_metric,loc=0` with an exact projector criterion.  In the local metric-response space with basis `E_i`, Gram matrix `G_ij=<E_i,E_j>_loc`, and moment vector `M_i[q_tr]=<E_i,Sigma_metric[q_tr]>_loc`, the theorem is
`P_metric,loc Sigma_metric[q_tr]=0 iff M_i[q_tr]=0 for every i`.  If exact zero fails, the finite source test is `M_i (G^-1)^ij M_j <= (4.212667126774669e-17)^2`.  The criterion is derived; raw-shell parent signing and numeric matrix rows are still missing.

Decision: `{DECISION}`.  Next target: `{NEXT_TARGET}`.
"""


def packet_block(now: str) -> str:
    return f"""## 4574 packet update — P_metric moment criterion

Marker: `{PACKET_MARKER}`  
Generated: `{now}`

The private local packet should no longer phrase transition safety as a naked `P_metric,loc=0` rule.  The admissible replacement is the Gram/moment condition `M_i[q_tr]=0` for all local metric response modes, or the finite profile-matrix bound `M_i (G^-1)^ij M_j`.  This keeps the transition route derivation-first while preserving a concrete empirical fallback.
"""


def append_claim() -> None:
    existing = read_text(CLAIMS_PATH)
    if CLAIM_ID in existing:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_signature",
        "claim": "4574 derives the exact Gram/moment criterion replacing the naked P_metric,loc=0 closure: local metric leakage vanishes iff all local response moments M_i[q_tr]=<E_i,Sigma_metric[q_tr]> vanish.",
        "current_evidence": "Generated source register, Gram projector theorem rows, moment-zero condition rows, source profile matrix pack, control rows, branch verdict, promotion gates, status and validation CSVs.",
        "status": DECISION.lower(),
        "next_test": NEXT_TARGET,
        "key_risk": "Treating the derived criterion as parent-signed for the raw transition shell before E_i/G_ij/Sigma_metric/M_i are supplied or moment-zero is proved.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "The projector theorem shape is real but nonclaim; raw-shell moment-zero law and profile matrix values remain missing.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writerow(row)


def validation_rows(
    outputs: list[Path],
    sources: list[dict[str, Any]],
    matrix_pack: list[dict[str, Any]],
    controls: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                "checkpoint": CHECKPOINT,
                "branch": BRANCH_ID,
                "check_id": check_id,
                "check": check,
                "passed": bool_text(passed),
                "detail": detail,
            }
        )

    for path in outputs:
        add(f"VAL4574_exists_{path.name}", "output path exists", path.exists(), str(path))
        if path.suffix == ".csv" and path.exists():
            rows = read_csv(path)
            add(f"VAL4574_csv_parse_{path.name}", "CSV parses with at least one row", len(rows) > 0, f"rows={len(rows)}")

    add("VAL4574_sources_exist", "all cited sources exist", all(row["exists"] == "True" for row in sources), "source register existence")
    add("VAL4574_needles_found", "all cited source needles found", all(row["needle_found"] == "True" for row in sources), "source register needles")
    add(
        "VAL4574_matrix_rows_nonclaim",
        "all source matrix rows remain nonclaim",
        all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in matrix_pack),
        "matrix pack firewalled",
    )
    add(
        "VAL4574_missing_inputs_explicit",
        "matrix pack explicitly records missing source inputs",
        any("MISSING" in row["current_value"] for row in matrix_pack),
        "missing matrix values visible",
    )
    add(
        "VAL4574_control_pass",
        "zero/below controls pass",
        any(row["control_id"] == "CTRL4574_zero_moments" and row["verdict"] == "CONTROL_PASS_NONCLAIM" for row in controls),
        "zero moment control",
    )
    add(
        "VAL4574_control_fail",
        "above-threshold control fails",
        any(row["control_id"] == "CTRL4574_above_threshold" and row["verdict"] == "CONTROL_FAIL_NONCLAIM" for row in controls),
        "above-threshold control",
    )
    add(
        "VAL4574_theorem_token",
        "Gram/moment theorem token recorded",
        "M_i[q_tr]" in read_text(DOC_PATH) and "Gram" in read_text(THEOREM_CSV),
        "moment criterion",
    )
    add(
        "VAL4574_decision_token",
        "decision token recorded",
        DECISION in read_text(DECISION_CSV) and DECISION in read_text(DOC_PATH),
        DECISION,
    )
    add(
        "VAL4574_next_target",
        "next target recorded",
        NEXT_TARGET in read_text(NEXT_CSV) and NEXT_TARGET in read_text(DOC_PATH),
        NEXT_TARGET,
    )
    add("VAL4574_claim_register", "claim register updated", CLAIM_ID in read_text(CLAIMS_PATH), CLAIM_ID)
    add(
        "VAL4574_spine_packet",
        "spine and packet markers present",
        MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH),
        f"{MARKER}; {PACKET_MARKER}",
    )
    return checks


def main() -> None:
    now = utc_now()
    sources = source_rows()
    theorem = theorem_rows(now)
    moments = moment_rows(now)
    matrix_pack = matrix_pack_rows(now)
    controls = control_rows(now)
    branches = branch_rows(now)
    promotions = promotion_rows(now)
    decisions = decision_rows(now)
    statuses = status_rows(now)
    next_targets = next_rows(now)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(THEOREM_CSV, theorem)
    write_csv(MOMENT_CSV, moments)
    write_csv(MATRIX_PACK_CSV, matrix_pack)
    write_csv(CONTROL_CSV, controls)
    write_csv(BRANCH_CSV, branches)
    write_csv(PROMOTION_CSV, promotions)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_targets)
    write_csv(STATUS_CSV, statuses)

    body = doc_body(now, sources, theorem, moments, matrix_pack, controls, branches, promotions)
    DOC_PATH.write_text(body, encoding="utf-8", newline="\n")
    FORMAL_PATH.write_text(body, encoding="utf-8", newline="\n")

    append_once(SPINE_PATH, MARKER, spine_block(now))
    append_once(PACKET_PATH, PACKET_MARKER, packet_block(now))
    append_claim()

    outputs = [
        SOURCE_REGISTER,
        THEOREM_CSV,
        MOMENT_CSV,
        MATRIX_PACK_CSV,
        CONTROL_CSV,
        BRANCH_CSV,
        PROMOTION_CSV,
        DECISION_CSV,
        NEXT_CSV,
        STATUS_CSV,
        DOC_PATH,
        FORMAL_PATH,
    ]
    validations = validation_rows(outputs, sources, matrix_pack, controls)
    write_csv(VALIDATION_PATH, validations)

    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validations if row["passed"] != "True"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"{CHECKPOINT} complete: {DECISION}")
    print(f"wrote: {DOC_PATH}")
    print(f"validation: {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
